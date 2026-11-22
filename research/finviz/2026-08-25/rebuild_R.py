import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
cache = json.loads((ROOT / 'catalyst-cache.json').read_text(encoding='utf-8'))
R = {}
for t, rec in cache.items():
    if t == '_meta':
        continue
    if rec['status'] == 'DIRECT_SAME_DAY_CATALYST':
        label = '直接'
        reason = rec.get('direct_event') or ''
        et = rec.get('event_time_et') or ''
        if et:
            reason += f"（事件时间{et}）"
        for s in (rec.get('sources') or [])[:2]:
            url = s.get('url', '')
            title = (s.get('title', '') or '来源')[:40]
            if url.startswith('http'):
                reason += f" [{title}]({url})"
    else:
        label = '联动'
        reason = rec.get('confirmed_linkage') or rec.get('output_conclusion') or ''
        reason = reason.replace('暂未找到同日直接催化；', '')
        ms = rec.get('mechanical_screen', {})
        news = ms.get('news_in_window_count', 0)
        if news:
            reason = f"窗口内新闻{news}条经核验无同日直接事件；" + reason
    R[t] = (label, reason)

d = json.loads((ROOT / 'calculated-statistics.json').read_text(encoding='utf-8'))
expected = []
for key in ('all_stocks', 'sp500', 'dow30', 'nasdaq100', 'russell2000', 'themes'):
    b = d['ranges'][key]
    for dd in ('selected_up', 'selected_down'):
        for row in b[dd]:
            for x in row['extreme']:
                if x['ticker'] not in expected:
                    expected.append(x['ticker'])
missing = [t for t in expected if t not in R]
extra = [t for t in R if t not in expected]
print('expected:', len(expected), 'R:', len(R), 'missing:', missing, 'extra:', extra)
assert not missing and not extra

lines = []
for t in expected:
    label, reason = R[t]
    reason = reason.replace('\\', '\\\\').replace('"', '\\"')
    lines.append('    "%s": ("%s", "%s"),' % (t, label, reason))
new_block = ('# R 催化字典：TICKER -> (label, 原因文本)。label 见 11-evidence-and-output-boundaries。\n'
             '# 事件时间口径：8月22日16:00 ET盘后事件可解释8月25日；8月25日16:00 ET后事件不得倒推。\n'
             'R = {\n' + '\n'.join(lines) + '\n}\n')
src = (ROOT / 'generate_outputs.py').read_text(encoding='utf-8')
src2 = re.sub(r'# R 催化字典.*?\nR = \{.*?\n\}\n', new_block, src, count=1, flags=re.DOTALL)
assert src2 != src, 'R block not found'
(ROOT / 'generate_outputs.py').write_text(src2, encoding='utf-8')
print('R rebuilt from catalyst cache:', len(expected))
