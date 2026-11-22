import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED_LABELS = {"直接", "联动", "结构", "单样本", "融资定价", "公司治理", "财报延续", "背离", "权重"}

data = json.loads((ROOT / "calculated-statistics.json").read_text(encoding="utf-8"))
expected = []
for key in ("all_stocks", "sp500", "dow30", "nasdaq100", "russell2000", "themes"):
    block = data["ranges"][key]
    for d in ("selected_up", "selected_down"):
        for row in block[d]:
            for x in row["extreme"]:
                if x["ticker"] not in expected:
                    expected.append(x["ticker"])

merged = {}
for part in sorted(ROOT.glob("catalyst-part-*.json")):
    merged.update(json.loads(part.read_text(encoding="utf-8")))

missing = [t for t in expected if t not in merged]
extra = [t for t in merged if t not in expected]
bad_label = {t: v["label"] for t, v in merged.items() if v["label"] not in EXPECTED_LABELS}
empty_reason = [t for t, v in merged.items() if not v.get("reason", "").strip()]
print("expected", len(expected), "merged", len(merged))
print("missing:", missing)
print("extra:", extra)
print("bad labels:", bad_label)
print("empty reasons:", empty_reason)
if missing or extra or bad_label or empty_reason:
    raise SystemExit("ASSEMBLE_BLOCKED")

lines = []
for t in expected:
    label = merged[t]["label"]
    reason = merged[t]["reason"].replace("\\", "\\\\").replace('"', '\\"')
    lines.append(f'    "{t}": ("{label}", "{reason}"),')
new_block = "# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。\n# 事件时间口径：8月17日16:00 ET盘后事件可解释8月18日；8月18日16:00 ET后事件不得倒推。\nR = {\n" + "\n".join(lines) + "\n}\n"

src = (ROOT / "generate_outputs.py").read_text(encoding="utf-8")
pattern = re.compile(r"# R 催化字典.*?\nR = \{.*?\n\}\n", re.DOTALL)
if not pattern.search(src):
    raise SystemExit("R_BLOCK_NOT_FOUND")
(ROOT / "generate_outputs.py").write_text(pattern.sub(new_block, src), encoding="utf-8")
print("R_BLOCK_REWRITTEN", len(expected), "entries")
