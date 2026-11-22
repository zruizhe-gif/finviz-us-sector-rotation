import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
d = json.loads((ROOT / 'calculated-statistics.json').read_text(encoding='utf-8'))
expected = []
for key in ('all_stocks','sp500','dow30','nasdaq100','russell2000','themes'):
    b = d['ranges'][key]
    for dd in ('selected_up','selected_down'):
        for row in b[dd]:
            for x in row['extreme']:
                if x['ticker'] not in expected:
                    expected.append(x['ticker'])

R = json.loads((ROOT / 'catalyst-R.json').read_text(encoding='utf-8'))
missing = [t for t in expected if t not in R]
extra = [t for t in R if t not in expected]
print('expected:', len(expected), '| missing:', missing, '| extra:', extra)
assert not missing and not extra, 'MISMATCH'

lines = []
for t in expected:
    label, reason = R[t]['label'], R[t]['reason']
    reason = reason.replace('\\', '\\\\').replace('"', '\\"')
    lines.append('    "%s": ("%s", "%s"),' % (t, label, reason))
new_block = ('# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。\n'
             '# 事件时间口径：8月21日16:00 ET盘后事件可解释8月24日；8月24日16:00 ET后事件不得倒推。\n'
             'R = {\n' + '\n'.join(lines) + '\n}\n')
src = (ROOT / 'generate_outputs.py').read_text(encoding='utf-8')
src2 = re.sub(r'# R 催化字典.*?\nR = \{.*?\n\}\n', new_block, src, count=1, flags=re.DOTALL)
assert src2 != src, 'R block not found'
(ROOT / 'generate_outputs.py').write_text(src2, encoding='utf-8')
(ROOT / 'catalyst-cache.json').write_text(json.dumps(R, ensure_ascii=False, indent=2), encoding='utf-8')
print('R_BLOCK_REWRITTEN', len(expected), 'entries; catalyst-cache.json:', len(R))
