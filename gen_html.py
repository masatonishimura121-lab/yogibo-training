import json

with open('/home/claude/data_v3.json') as f:
    d = json.load(f)

stores = d['stores']   # [(code, name, manager, area), ...]
meetings = d['meetings']
result = d['result']

js_stores   = json.dumps(stores,   ensure_ascii=False)
js_meetings = json.dumps(meetings, ensure_ascii=False)
js_result   = json.dumps(result,   ensure_ascii=False)

# エリア順ソート用
AREA_ORDER = ['関東','東海','関西','九州','中国','東北','北海道','四国','沖縄','北陸・甲信越','']

html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Yogibo 講座参加状況</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=IBM+Plex+Mono:wght@400;600&display=swap');
:root{{
  --bg:#0f1117;--sur:#181c27;--sur2:#1e2435;--bdr:#2a3045;
  --acc:#4f8ef7;--grn:#38d9a9;--orn:#ffa94d;--red:#ff6b6b;
  --txt:#e8eaf0;--dim:#7a8099;--mut:#4a5270;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Noto Sans JP',sans-serif;background:var(--bg);color:var(--txt);min-height:100vh}}
body::before{{content:'';position:fixed;inset:0;
  background-image:linear-gradient(rgba(79,142,247,.03)1px,transparent 1px),
  linear-gradient(90deg,rgba(79,142,247,.03)1px,transparent 1px);
  background-size:40px 40px;pointer-events:none;z-index:0}}
.wrap{{position:relative;z-index:1}}

/* Header */
header{{padding:18px 28px;border-bottom:1px solid var(--bdr);display:flex;align-items:center;gap:14px;
  background:rgba(15,17,23,.94);backdrop-filter:blur(8px);position:sticky;top:0;z-index:200}}
.logo{{font-size:24px}}
header h1{{font-size:17px;font-weight:700;letter-spacing:-.2px}}
header p{{font-size:11px;color:var(--dim);margin-top:2px}}
.hright{{margin-left:auto;display:flex;gap:8px}}

/* Main */
.main{{max-width:1400px;margin:0 auto;padding:24px 20px}}

/* Summary */
.summary{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:24px}}
.card{{background:var(--sur);border:1px solid var(--bdr);border-radius:11px;padding:14px 16px;text-align:center}}
.cv{{font-size:28px;font-weight:700;font-family:'IBM Plex Mono',monospace;line-height:1;margin-bottom:4px}}
.cl{{font-size:11px;color:var(--dim)}}
.g{{color:var(--grn)}}.o{{color:var(--orn)}}.r{{color:var(--red)}}.b{{color:var(--acc)}}

/* Controls */
.ctrl{{display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap;align-items:center}}
input[type=text]{{background:var(--sur);border:1px solid var(--bdr);border-radius:8px;color:var(--txt);
  padding:7px 12px;font-size:13px;font-family:'Noto Sans JP',sans-serif;outline:none;width:210px;
  transition:border-color .2s}}
input[type=text]:focus{{border-color:var(--acc)}}
select{{background:var(--sur);border:1px solid var(--bdr);border-radius:8px;color:var(--txt);
  padding:7px 12px;font-size:12px;font-family:'Noto Sans JP',sans-serif;outline:none;cursor:pointer;
  transition:border-color .2s}}
select:focus{{border-color:var(--acc)}}
.fb{{padding:7px 13px;border-radius:8px;border:1px solid var(--bdr);background:var(--sur);
  color:var(--txt);font-size:12px;font-family:'Noto Sans JP',sans-serif;cursor:pointer;transition:all .15s}}
.fb:hover{{background:var(--sur2);border-color:var(--acc);color:var(--acc)}}
.fb.on{{background:rgba(79,142,247,.15);border-color:var(--acc);color:var(--acc)}}
.btn{{padding:7px 14px;border-radius:8px;border:1px solid var(--bdr);background:var(--sur2);
  color:var(--txt);font-size:12px;font-weight:600;font-family:'Noto Sans JP',sans-serif;cursor:pointer}}
.btn:hover{{background:var(--bdr)}}

/* Legend */
.legend{{display:flex;gap:16px;margin-bottom:12px;font-size:12px;color:var(--dim);flex-wrap:wrap;align-items:center}}
.li{{display:flex;align-items:center;gap:5px}}
.ld{{width:8px;height:8px;border-radius:50%;flex-shrink:0}}

/* Table */
.twrap{{border:1px solid var(--bdr);border-radius:13px;overflow:auto;background:var(--sur);max-height:72vh}}
table{{width:100%;border-collapse:collapse}}
thead th{{background:var(--sur2);padding:10px 13px;text-align:left;font-size:10px;font-weight:600;
  color:var(--dim);text-transform:uppercase;letter-spacing:.6px;border-bottom:1px solid var(--bdr);
  white-space:nowrap;position:sticky;top:0;z-index:2}}

/* Sticky columns */
thead th:nth-child(1){{position:sticky;left:0;z-index:3;background:var(--sur2);min-width:56px;width:56px}}
thead th:nth-child(2){{position:sticky;left:56px;z-index:3;background:var(--sur2);min-width:190px}}
thead th:nth-child(3){{position:sticky;left:246px;z-index:3;background:var(--sur2);min-width:78px}}
thead th:nth-child(4){{position:sticky;left:324px;z-index:3;background:var(--sur2);min-width:90px;border-right:1px solid var(--bdr)}}

thead th.c{{text-align:center}}

tbody td{{padding:9px 13px;font-size:13px;border-bottom:1px solid var(--bdr);vertical-align:middle;transition:background .1s}}
tbody tr:last-child td{{border-bottom:none}}
tbody tr:hover td{{background:var(--sur2)}}

tbody td:nth-child(1){{position:sticky;left:0;background:var(--sur);z-index:1;
  font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--dim);width:56px}}
tbody td:nth-child(2){{position:sticky;left:56px;background:var(--sur);z-index:1;font-weight:500;white-space:nowrap}}
tbody td:nth-child(3){{position:sticky;left:246px;background:var(--sur);z-index:1;font-size:12px;color:var(--dim);white-space:nowrap}}
tbody td:nth-child(4){{position:sticky;left:324px;background:var(--sur);z-index:1;font-size:11px;
  color:var(--dim);white-space:nowrap;border-right:1px solid var(--bdr)}}

tbody tr:hover td:nth-child(1),tbody tr:hover td:nth-child(2),
tbody tr:hover td:nth-child(3),tbody tr:hover td:nth-child(4){{background:var(--sur2)}}

.cc{{text-align:center}}
.ci{{display:flex;flex-direction:column;align-items:center;gap:1px}}
.ml{{font-size:10px;color:var(--dim);font-family:'IBM Plex Mono',monospace;display:none}}
.cross{{color:var(--mut);font-size:15px}}
.pb{{min-width:76px}}
.pl{{font-size:11px;font-family:'IBM Plex Mono',monospace;text-align:center;margin-bottom:3px}}
.pbar{{height:3px;background:var(--bdr);border-radius:2px;overflow:hidden}}
.pf{{height:100%;border-radius:2px}}

/* Row color coding via left border on col2 */
.ra td:nth-child(2){{border-left:3px solid var(--grn)}}
.rp td:nth-child(2){{border-left:3px solid var(--orn)}}
.rn td:nth-child(2){{border-left:3px solid var(--red)}}

/* Area group header */
.area-row td{{background:var(--sur2)!important;font-size:11px;font-weight:700;
  color:var(--acc);letter-spacing:.5px;padding:6px 13px;border-bottom:1px solid var(--bdr)}}

/* Note */
.note{{margin-top:16px;padding:12px 16px;background:rgba(79,142,247,.07);
  border:1px solid rgba(79,142,247,.2);border-radius:10px;font-size:12px;color:var(--dim);line-height:1.8}}
.note strong{{color:var(--acc)}}

::-webkit-scrollbar{{width:5px;height:5px}}
::-webkit-scrollbar-track{{background:transparent}}
::-webkit-scrollbar-thumb{{background:var(--bdr);border-radius:3px}}

@media print{{
  body{{background:#fff;color:#000}}body::before{{display:none}}
  header{{position:static;background:#fff;border-bottom:2px solid #ccc}}
  .ctrl,.btn{{display:none}}
  .twrap{{border:1px solid #ccc;max-height:none;overflow:visible}}
  thead th{{background:#f0f0f0!important;color:#333}}
  tbody td{{border-color:#ddd}}
  tbody td:nth-child(1),tbody td:nth-child(2),tbody td:nth-child(3),tbody td:nth-child(4){{background:#fff!important}}
  .area-row td{{background:#e8e8e8!important}}
}}
</style>
</head>
<body><div class="wrap">
<header>
  <div class="logo">📋</div>
  <div>
    <h1>Yogibo 講座参加状況</h1>
    <p>Zoomミーティング参加記録 × 店舗マスタ突合　｜　ミーティングID: 475 651 5009　｜　集計日: 2026/03/10</p>
  </div>
  <div class="hright">
    <a class="hbtn" href="yogibo_upload.html">📤 CSVアップロード</a>
    <button class="btn" onclick="exportCSV()">📥 CSV</button>
    <button class="btn" onclick="window.print()">🖨 印刷</button>
  </div>
</header>

<div class="main">
  <div class="summary" id="summary"></div>
  <div class="ctrl">
    <input type="text" id="fi" placeholder="🔍 店舗名・コード・店長で絞り込み…" oninput="render()">
    <select id="area-sel" onchange="render()">
      <option value="">全エリア</option>
      <option>北海道</option><option>東北</option><option>関東</option>
      <option>北陸・甲信越</option><option>東海</option><option>関西</option>
      <option>中国</option><option>四国</option><option>九州</option>
      <option>沖縄</option>
    </select>
    <select id="am-sel" onchange="render()">
      <option value="">全AM</option>
      <option>旭</option><option>才賀</option><option>内田</option>
      <option>佐伯</option><option>渡邊</option><option>花渕</option>
      <option>荒金</option><option>西村</option>
    </select>
    <select id="month-sel" onchange="render()">
      <option value="">全期間</option>
      <option value="2">2月</option>
      <option value="3">3月</option>
    </select>
    <select id="ops-sel" onchange="render()">
      <option value="">全運営</option>
      <option value="直営">直営</option>
      <option value="代行">代行</option>
      <option value="FC">FC</option>
    </select>
    <button class="fb on" id="f-all"  onclick="sf('all')">全店舗</button>
    <button class="fb"    id="f-some" onclick="sf('some')">一部参加</button>
    <button class="fb"    id="f-none" onclick="sf('none')">未参加</button>
    <button class="fb"    id="f-det"  onclick="toggleDet()">分数表示</button>
    <div style="margin-left:auto;display:flex;gap:6px">
      <button class="btn" onclick="sortBy('pct')">参加率順</button>
      <button class="btn" onclick="sortBy('am')">AM順</button>
        <button class="btn" onclick="sortBy('month')">月順</button>
        <button class="btn" onclick="sortBy('area')">エリア順</button>
      <button class="btn" onclick="sortBy('code')">コード順</button>
    </div>
  </div>
  <div class="legend">
    <div class="li"><div class="ld" style="background:var(--grn)"></div>全3回参加</div>
    <div class="li"><div class="ld" style="background:var(--orn)"></div>一部参加</div>
    <div class="li"><div class="ld" style="background:var(--red)"></div>未参加</div>
    <div style="margin-left:auto;font-size:11px;color:var(--mut)">有効参加：5分以上　主催者・管理者は除外済み</div>
  </div>
  <div class="twrap"><table id="tbl"><thead id="th"></thead><tbody id="tb"></tbody></table></div>
  <div class="note">
    <strong>名寄せ・表記ゆれ補正済み</strong>　店舗マスタ・スタッフリスト（店長名）と突合しました。<br>
    「AM川口店」→ イオンモール川口 ／ 「酒々井プレミアムアウトレット」→ 酒々井PREMIUM OUTLET ／
    「浜田 真梨絵」→ イオンモール京都桂川（店長名照合）／ 「yogibo長久手 高田」→ イオンモール長久手 など52名分を自動・手動補正。<br>
    <strong>注意</strong>：イオンモール川口・酒々井PREMIUM OUTLET・イオンモール須坂・イオンモール伊丹昆陽は店舗コードを仮割当しています。
  </div>
</div></div>

<script>
const STORES   = {js_stores};
const MEETINGS = {js_meetings};
const RESULT   = {js_result};

const AREA_ORDER = ['関東','東海','関西','九州','中国','東北','北海道','四国','沖縄','北陸・甲信越',''];

// store_map: code -> {{code,name,manager,area}}
const SM = {{}};
STORES.forEach(s => SM[s[0]] = {{code:s[0],name:s[1],manager:s[2],area:s[3]||'',am:s[4]||'',ops:s[5]||''}});

let fmode='all', showDet=false, sortMode='pct';

function getPct(code, mtgs){{ mtgs=mtgs||MEETINGS;
  const done = mtgs.filter(m => RESULT[code][m]!==null).length;
  return Math.round(done/mtgs.length*100);
}}

function sf(m){{
  fmode=m;
  ['all','all3','some','none'].forEach(x=>document.getElementById('f-'+x).classList.toggle('on',x===m));
  render();
}}

function toggleDet(){{
  showDet=!showDet;
  document.getElementById('f-det').classList.toggle('on',showDet);
  document.querySelectorAll('.ml').forEach(e=>e.style.display=showDet?'block':'none');
}}

function sortBy(m){{sortMode=m;render();}}

function render(){{
  const fi   = document.getElementById('fi').value.trim();
  const area = document.getElementById('area-sel').value;
  const am    = document.getElementById('am-sel').value;
  const ops   = document.getElementById('ops-sel').value;
  const month = document.getElementById('month-sel').value;
  const visibleMtgs = month ? MEETINGS.filter(m=>m.startsWith(month+'/')) : MEETINGS;

  let codes = Object.keys(RESULT).filter(code=>{{
    const s = SM[code];
    if(fi && !s.name.includes(fi) && !s.code.includes(fi) && !s.manager.includes(fi)) return false;
    if(area && s.area!==area) return false;
    if(am && s.am!==am) return false;
    if(ops && s.ops!==ops) return false;
    if(month) {{
      const hasParticipation = visibleMtgs.some(m=>RESULT[code][m]!==null);
      if(!hasParticipation) return false;
    }}
    const done = visibleMtgs.filter(m=>RESULT[code][m]!==null).length;
    if(fmode==='some') return done>0 && done<visibleMtgs.length;
    if(fmode==='none') return done===0;
    return true;
  }});

  // Sort
  if(sortMode==='pct')  codes.sort((a,b)=>getPct(b,visibleMtgs)-getPct(a,visibleMtgs)||a.localeCompare(b,'ja'));
  if(sortMode==='code') codes.sort((a,b)=>a.localeCompare(b));
  if(sortMode==='month') codes.sort((a,b)=>{{
    const getFirst=code=>MEETINGS.findIndex(m=>RESULT[code][m]!==null);
    return getFirst(a)-getFirst(b)||SM[a].name.localeCompare(SM[b].name,'ja');
  }});
  if(sortMode==='am')   codes.sort((a,b)=>SM[a].am.localeCompare(SM[b].am,'ja')||SM[a].name.localeCompare(SM[b].name,'ja'));
  if(sortMode==='area') codes.sort((a,b)=>{{
    const ai=AREA_ORDER.indexOf(SM[a].area), bi=AREA_ORDER.indexOf(SM[b].area);
    return (ai===-1?99:ai)-(bi===-1?99:bi)||SM[a].name.localeCompare(SM[b].name,'ja');
  }});

  // Summary (based on all stores, not filtered)
  const all = Object.keys(RESULT);
  const cs  = all.filter(c=>visibleMtgs.some(m=>RESULT[c][m]!==null)&&!visibleMtgs.every(m=>RESULT[c][m]!==null)).length;
  const cn  = all.filter(c=>visibleMtgs.every(m=>RESULT[c][m]===null)).length;
  document.getElementById('summary').innerHTML=`
    <div class="card"><div class="cv b">${{all.length}}</div><div class="cl">総店舗数</div></div>
    <div class="card"><div class="cv o">${{cs}}</div><div class="cl">一部参加</div></div>
    <div class="card"><div class="cv r">${{cn}}</div><div class="cl">未参加</div></div>
    <div class="card"><div class="cv">${{MEETINGS.length}}</div><div class="cl">ミーティング数</div></div>`;

  // Header
  document.getElementById('th').innerHTML=`<tr>
    <th>コード</th><th>店舗名</th><th>SM</th><th>エリア</th><th>AM</th><th>運営</th>
    ${{visibleMtgs.map(m=>`<th class="c">${{m}}</th>`).join('')}}
    <th class="c">参加率</th></tr>`;

  // Body
  let prevArea='__', prevAM='__', prevMonth='__', rows='';
  codes.forEach(code=>{{
    const s=SM[code];
    if(sortMode==='month'){{
      const firstMtg=MEETINGS.find(m=>RESULT[code][m]!==null)||'';
      const mLabel=firstMtg.split('/')[0]+'月';
      if(mLabel!==prevMonth){{
        rows+=`<tr class="area-row"><td colspan="${{6+visibleMtgs.length+1}}">${{mLabel}} 初回参加</td></tr>`;
        prevMonth=mLabel;
      }}
    }}
    if(sortMode==='am' && s.am!==prevAM){{
      rows+=`<tr class="area-row"><td colspan="${{6+visibleMtgs.length+1}}">AM: ${{esc(s.am)||'未設定'}}</td></tr>`;
      prevAM=s.am;
    }}
    if(sortMode==='area' && s.area!==prevArea){{
      rows+=`<tr class="area-row"><td colspan="${{6+visibleMtgs.length+1}}">${{s.area||'その他'}}</td></tr>`;
      prevArea=s.area;
    }}
    const done=visibleMtgs.filter(m=>RESULT[code][m]!==null).length;
    const pct=Math.round(visibleMtgs.length>0?done/visibleMtgs.length*100:0);
    const rc=done===visibleMtgs.length&&done>0?'ra':done>0?'rp':'rn';
    const bc=pct===100?'var(--grn)':pct>0?'var(--orn)':'var(--red)';
    const cells=visibleMtgs.map(m=>{{
      const v=RESULT[code][m];
      if(!v) return `<td class="cc"><span class="cross">−</span></td>`;
      return `<td class="cc"><div class="ci"><span style="font-size:16px">✅</span>
        <span class="ml" style="display:${{showDet?'block':'none'}}">${{v}}分</span></div></td>`;
    }}).join('');
    rows+=`<tr class="${{rc}}">
      <td>${{esc(code)}}</td><td>${{esc(s.name)}}</td>
      <td>${{esc(s.manager||'−')}}</td><td>${{esc(s.area||'−')}}</td><td style="font-size:12px;color:var(--dim)">${{esc(s.am||'−')}}</td>
      <td style="font-size:11px;font-weight:700;text-align:center;color:#888">${{esc(s.ops||'−')}}</td>
      ${{cells}}
      <td class="pb"><div class="pl" style="color:${{bc}}">${{pct}}%</div>
        <div class="pbar"><div class="pf" style="width:${{pct}}%;background:${{bc}}"></div></div></td>
    </tr>`;
  }});
  document.getElementById('tb').innerHTML=rows;
}}

function exportCSV(){{
  const rows=[['コード','店舗名','SM','エリア','AM','運営',...MEETINGS,'参加率(%)']];
  Object.keys(RESULT).sort().forEach(code=>{{
    const s=SM[code];
    const vals=MEETINGS.map(m=>RESULT[code][m]?`✓(${{RESULT[code][m]}}分)`:'');
    const pct=Math.round(MEETINGS.length>0?MEETINGS.filter(m=>RESULT[code][m]!==null).length/MEETINGS.length*100:0);
    rows.push([code,s.name,s.manager||'',s.area||'',s.am||'',s.ops||'',...vals,pct]);
  }});
  const bom='\uFEFF',csv=bom+rows.map(r=>r.map(v=>`"${{v}}"`).join(',')).join('\\n');
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([csv],{{type:'text/csv'}}));
  a.download='Yogibo研修参加状況.csv';a.click();
}}

function esc(s){{return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}}

render();
</script>
</body></html>"""

with open('/mnt/user-data/outputs/yogibo_training_v3.html','w',encoding='utf-8') as f:
    f.write(html)
print("完成")

# ===== 参加者詳細リスト画面を別ファイルで生成 =====
with open('/home/claude/data_v3.json') as f:
    d2 = json.load(f)

stores2   = d2['stores']
meetings2 = d2['meetings']
zoom_log  = d2['zoom_log']

SM2 = {s[0]: {'name':s[1],'manager':s[2],'area':s[3] if len(s)>3 else '','am':s[4] if len(s)>4 else '','ops':s[5] if len(s)>5 else ''} for s in stores2}

js_zoom_log = json.dumps(zoom_log, ensure_ascii=False)
js_sm2      = json.dumps({k:v for k,v in SM2.items()}, ensure_ascii=False)
js_mtgs2    = json.dumps(meetings2, ensure_ascii=False)

detail_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Yogibo 講座参加者詳細</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=IBM+Plex+Mono:wght@400;600&display=swap');
:root{{
  --bg:#0f1117;--sur:#181c27;--sur2:#1e2435;--bdr:#2a3045;
  --acc:#4f8ef7;--grn:#38d9a9;--orn:#ffa94d;--red:#ff6b6b;
  --txt:#e8eaf0;--dim:#7a8099;--mut:#4a5270;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Noto Sans JP',sans-serif;background:var(--bg);color:var(--txt);min-height:100vh}}
body::before{{content:'';position:fixed;inset:0;
  background-image:linear-gradient(rgba(79,142,247,.03)1px,transparent 1px),linear-gradient(90deg,rgba(79,142,247,.03)1px,transparent 1px);
  background-size:40px 40px;pointer-events:none;z-index:0}}
.wrap{{position:relative;z-index:1}}
header{{padding:18px 28px;border-bottom:1px solid var(--bdr);display:flex;align-items:center;gap:14px;
  background:rgba(15,17,23,.94);backdrop-filter:blur(8px);position:sticky;top:0;z-index:200}}
.logo{{font-size:24px}}
header h1{{font-size:17px;font-weight:700}}
header p{{font-size:11px;color:var(--dim);margin-top:2px}}
.hright{{margin-left:auto;display:flex;gap:8px}}
.main{{max-width:1200px;margin:0 auto;padding:24px 20px}}

/* Summary badges */
.badges{{display:flex;gap:10px;margin-bottom:22px;flex-wrap:wrap}}
.badge{{background:var(--sur);border:1px solid var(--bdr);border-radius:20px;padding:6px 14px;
  font-size:12px;cursor:pointer;transition:all .15s;display:flex;align-items:center;gap:6px}}
.badge:hover{{border-color:var(--acc);color:var(--acc)}}
.badge.on{{background:rgba(79,142,247,.15);border-color:var(--acc);color:var(--acc)}}
.badge-count{{font-family:'IBM Plex Mono',monospace;font-weight:700;font-size:13px}}

/* Controls */
.ctrl{{display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap;align-items:center}}
input[type=text]{{background:var(--sur);border:1px solid var(--bdr);border-radius:8px;color:var(--txt);
  padding:7px 12px;font-size:13px;font-family:'Noto Sans JP',sans-serif;outline:none;width:220px;transition:border-color .2s}}
input[type=text]:focus{{border-color:var(--acc)}}
select{{background:var(--sur);border:1px solid var(--bdr);border-radius:8px;color:var(--txt);
  padding:7px 12px;font-size:12px;font-family:'Noto Sans JP',sans-serif;outline:none;cursor:pointer}}
select:focus{{border-color:var(--acc)}}
.btn{{padding:7px 14px;border-radius:8px;border:1px solid var(--bdr);background:var(--sur2);
  color:var(--txt);font-size:12px;font-weight:600;font-family:'Noto Sans JP',sans-serif;cursor:pointer}}
.btn:hover{{background:var(--bdr)}}

/* View toggle */
.view-tabs{{display:flex;gap:0;background:var(--sur);border:1px solid var(--bdr);border-radius:8px;overflow:hidden;margin-bottom:18px}}
.vtab{{padding:8px 18px;font-size:12px;font-weight:600;cursor:pointer;transition:all .15s;
  font-family:'Noto Sans JP',sans-serif;border:none;background:transparent;color:var(--dim)}}
.vtab.on{{background:var(--acc);color:#fff}}

/* Store grouped view */
.store-group{{background:var(--sur);border:1px solid var(--bdr);border-radius:12px;margin-bottom:14px;overflow:hidden}}
.sg-header{{padding:14px 18px;display:flex;align-items:center;gap:12px;cursor:pointer;
  border-bottom:1px solid var(--bdr);transition:background .15s}}
.sg-header:hover{{background:var(--sur2)}}
.sg-code{{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--dim);min-width:40px}}
.sg-name{{font-weight:600;font-size:14px}}
.sg-manager{{font-size:12px;color:var(--dim);margin-left:4px}}
.sg-area{{font-size:11px;color:var(--mut);margin-left:auto}}
.sg-chips{{display:flex;gap:6px;margin-left:12px}}
.chip{{padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600}}
.chip-grn{{background:rgba(56,217,169,.15);color:var(--grn)}}
.chip-orn{{background:rgba(255,169,77,.15);color:var(--orn)}}
.sg-body{{padding:0}}
.sg-row{{display:flex;align-items:center;gap:12px;padding:10px 18px;border-bottom:1px solid var(--bdr);font-size:13px}}
.sg-row:last-child{{border-bottom:none}}
.sg-row:hover{{background:var(--sur2)}}
.zoom-name{{font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--dim);min-width:260px;word-break:break-all}}
.mtg-tag{{padding:3px 10px;border-radius:6px;font-size:11px;font-weight:600;white-space:nowrap}}
.mins-tag{{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--mut)}}
.collapsed .sg-body{{display:none}}
.arrow{{font-size:11px;color:var(--mut);transition:transform .2s;margin-left:4px}}
.collapsed .arrow{{transform:rotate(-90deg)}}

/* Timeline / flat list view */
.twrap{{border:1px solid var(--bdr);border-radius:13px;overflow:auto;background:var(--sur);max-height:72vh}}
table{{width:100%;border-collapse:collapse}}
thead th{{background:var(--sur2);padding:10px 14px;text-align:left;font-size:10px;font-weight:600;
  color:var(--dim);text-transform:uppercase;letter-spacing:.6px;border-bottom:1px solid var(--bdr);
  white-space:nowrap;position:sticky;top:0;z-index:2}}
thead th.c{{text-align:center}}
tbody td{{padding:10px 14px;font-size:13px;border-bottom:1px solid var(--bdr);vertical-align:middle}}
tbody tr:last-child td{{border-bottom:none}}
tbody tr:hover td{{background:var(--sur2)}}
.mono{{font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--dim)}}

::-webkit-scrollbar{{width:5px;height:5px}}
::-webkit-scrollbar-track{{background:transparent}}
::-webkit-scrollbar-thumb{{background:var(--bdr);border-radius:3px}}

@media print{{
  body{{background:#fff;color:#000}}body::before{{display:none}}
  header{{position:static;background:#fff;border-bottom:2px solid #ccc}}
  .ctrl,.btn,.view-tabs,.badges{{display:none}}
  .twrap{{max-height:none;overflow:visible;border:1px solid #ccc}}
  thead th{{background:#f0f0f0!important;color:#333}}
  tbody td{{border-color:#ddd}}
  .store-group{{border:1px solid #ccc;margin-bottom:10px}}
  .sg-header{{background:#f5f5f5!important;border-bottom:1px solid #ccc}}
  .collapsed .sg-body{{display:block!important}}
}}
</style>
</head>
<body><div class="wrap">
<header>
  <div class="logo">👥</div>
  <div>
    <h1>Yogibo 講座参加者詳細</h1>
    <p>Zoom表示名・参加研修・参加時間の一覧　｜　ミーティングID: 475 651 5009</p>
  </div>
  <div class="hright">
    <a class="hbtn" href="yogibo_upload.html">📤 CSVアップロード</a>
    <button class="btn" onclick="exportCSV()">📥 CSV</button>
    <button class="btn" onclick="window.print()">🖨 印刷</button>
    <button class="btn" onclick="window.open('yogibo_training_v3.html')">📋 参加状況表</button>
  </div>
</header>
<div class="main">

  <!-- 研修フィルターバッジ -->
  <div class="badges" id="badges"></div>

  <div class="ctrl">
    <input type="text" id="fi" placeholder="🔍 店舗名・Zoom表示名で絞り込み…" oninput="render()">
    <select id="area-sel" onchange="render()">
      <option value="">全エリア</option>
      <option>北海道</option><option>東北</option><option>関東</option>
      <option>北陸・甲信越</option><option>東海</option><option>関西</option>
      <option>中国</option><option>四国</option><option>九州</option>
      <option>沖縄</option>
    </select>
    <select id="am-sel" onchange="render()">
      <option value="">全AM</option>
      <option>旭</option><option>才賀</option><option>内田</option>
      <option>佐伯</option><option>渡邊</option><option>花渕</option>
      <option>荒金</option><option>西村</option>
    </select>
    <select id="ops-sel-d" onchange="render()">
      <option value="">全運営</option>
      <option value="直営">直営</option>
      <option value="代行">代行</option>
      <option value="FC">FC</option>
    </select>
    <select id="month-sel" onchange="render()">
      <option value="">全期間</option>
      <option value="2">2月</option>
      <option value="3">3月</option>
    </select>
  </div>

  <div class="view-tabs">
    <button class="vtab on" id="vt-store" onclick="setView('store')">🏪 店舗別</button>
    <button class="vtab" id="vt-mtg"   onclick="setView('mtg')">📅 研修別</button>
    <button class="vtab" id="vt-flat"  onclick="setView('flat')">📋 一覧</button>
  </div>

  <div id="content"></div>
</div></div>

<script>
const ZOOM_LOG = {js_zoom_log};
const SM       = {js_sm2};
const MEETINGS = {js_mtgs2};

const LECTURE_COLOR_MAP = {{
  '３笑':    {{bg:'rgba(255,107,107,.15)',  color:'#ff6b6b'}},
  '接客基礎': {{bg:'rgba(56,217,169,.15)',  color:'#38d9a9'}},
  'Cover':   {{bg:'rgba(79,142,247,.15)',  color:'#4f8ef7'}},
  'Premium': {{bg:'rgba(255,169,77,.15)',  color:'#ffa94d'}},
  'VIP':     {{bg:'rgba(192,132,252,.15)', color:'#c084fc'}},
}};
function getMtgColor(mtg) {{
  if(mtg.includes('３笑'))    return LECTURE_COLOR_MAP['３笑'];
  if(mtg.includes('接客基礎')) return LECTURE_COLOR_MAP['接客基礎'];
  if(mtg.includes('Cover'))   return LECTURE_COLOR_MAP['Cover'];
  if(mtg.includes('Premium')) return LECTURE_COLOR_MAP['Premium'];
  if(mtg.includes('VIP'))     return LECTURE_COLOR_MAP['VIP'];
  return {{bg:'rgba(122,128,153,.15)',color:'#7a8099'}};
}}
const MTG_COLORS = new Proxy({{}}, {{ get: (t,m) => getMtgColor(m) }});

let viewMode = 'store';
let filterMtg = '';

// Build badges
function buildBadges() {{
  const counts = {{}};
  MEETINGS.forEach(m => counts[m] = ZOOM_LOG.filter(r => r.mtg===m).length);
  const total = ZOOM_LOG.length;

  // 講座種別カウント
  const LECTURE_TYPES = ['３笑','接客基礎','Cover','Premium','VIP'];
  const LECTURE_COLORS = {{
    '３笑':    {{bg:'rgba(255,107,107,.15)',color:'#ff6b6b'}},
    '接客基礎': {{bg:'rgba(56,217,169,.15)', color:'#38d9a9'}},
    'Cover':   {{bg:'rgba(79,142,247,.15)',  color:'#4f8ef7'}},
    'Premium': {{bg:'rgba(255,169,77,.15)',  color:'#ffa94d'}},
    'VIP':     {{bg:'rgba(192,132,252,.15)', color:'#c084fc'}},
  }};
  const lectureCounts = {{}};
  LECTURE_TYPES.forEach(lt => {{
    lectureCounts[lt] = ZOOM_LOG.filter(r=>getLectureType(r.mtg)===lt).length;
  }});

  let html = `<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px">`;
  // 講座種別バッジ
  html += `<div class="badge ${{filterLecture===''&&filterMtg===''?'on':''}}" onclick="setLectureFilter('')">
    <span>全講座</span><span class="badge-count">${{total}}</span></div>`;
  LECTURE_TYPES.forEach(lt => {{
    const c = LECTURE_COLORS[lt];
    const cnt = lectureCounts[lt]||0;
    if(!cnt) return;
    html += `<div class="badge ${{filterLecture===lt?'on':''}}" onclick="setLectureFilter('${{lt}}')"
      style="${{filterLecture===lt?`background:${{c.bg}};border-color:${{c.color}};color:${{c.color}}`:''}}" >
      <span>${{lt}}</span><span class="badge-count">${{cnt}}</span></div>`;
  }});
  html += `</div><div style="display:flex;gap:8px;flex-wrap:wrap">`;
  // 個別ミーティングバッジ
  MEETINGS.forEach(m => {{
    const c = MTG_COLORS[m]||{{bg:'rgba(122,128,153,.15)',color:'#7a8099'}};
    html += `<div class="badge ${{filterMtg===m?'on':''}}" onclick="setMtgFilter('${{m}}')"
      style="${{filterMtg===m?`background:${{c.bg}};border-color:${{c.color}};color:${{c.color}}`:''}}" >
      <span>${{m}}</span><span class="badge-count">${{counts[m]}}</span></div>`;
  }});
  html += `</div>`;
  document.getElementById('badges').innerHTML = html;
}}

function setMtgFilter(m) {{ filterMtg=m; filterLecture=''; buildBadges(); render(); }}
function setLectureFilter(lt) {{ filterLecture=lt; filterMtg=''; buildBadges(); render(); }}
function setView(v) {{
  viewMode=v;
  ['store','mtg','flat'].forEach(x=>document.getElementById('vt-'+x).classList.toggle('on',x===v));
  render();
}}

function getLectureType(mtg) {{
  if(mtg.includes('３笑'))    return '３笑';
  if(mtg.includes('接客基礎')) return '接客基礎';
  if(mtg.includes('Cover'))   return 'Cover';
  if(mtg.includes('Premium')) return 'Premium';
  if(mtg.includes('VIP'))     return 'VIP';
  return 'その他';
}}

let filterLecture = '';

function filtered() {{
  const fi   = document.getElementById('fi').value.trim();
  const area = document.getElementById('area-sel').value;
  const am   = document.getElementById('am-sel').value;
  const opsD = document.getElementById('ops-sel-d').value;
  return ZOOM_LOG.filter(r => {{
    if(filterMtg && r.mtg!==filterMtg) return false;
    if(filterLecture && getLectureType(r.mtg)!==filterLecture) return false;
    const s = SM[r.store]||{{}};
    if(opsD && s.ops!==opsD) return false;
    if(fi && !r.zoom.includes(fi) && !(s.name||'').includes(fi)) return false;
    if(area && s.area!==area) return false;
    if(am && s.am!==am) return false;
    return true;
  }});
}}

function render() {{
  buildBadges();
  const data = filtered();
  if(viewMode==='store') renderStore(data);
  else if(viewMode==='mtg') renderMtg(data);
  else renderFlat(data);
}}

function renderStore(data) {{
  // Group by store
  const groups = {{}};
  data.forEach(r => {{
    if(!groups[r.store]) groups[r.store] = [];
    groups[r.store].push(r);
  }});
  const storeOrder = Object.keys(groups).sort((a,b)=>{{
    const sa=SM[a]||{{}}, sb=SM[b]||{{}};
    return (sa.name||a).localeCompare(sb.name||b,'ja');
  }});
  let html = '';
  storeOrder.forEach(code => {{
    const s = SM[code]||{{name:code,manager:'',area:''}};
    const rows = groups[code];
    const mtgs = [...new Set(rows.map(r=>r.mtg))];
    const chips = mtgs.map(m=>{{
      const c=MTG_COLORS[m]||{{bg:'rgba(122,128,153,.15)',color:'#7a8099'}};
      return `<span class="chip" style="background:${{c.bg}};color:${{c.color}}">${{m}}</span>`;
    }}).join('');
    const rowsHtml = rows.map(r=>{{
      const c=MTG_COLORS[r.mtg]||{{bg:'rgba(122,128,153,.15)',color:'#7a8099'}};
      return `<div class="sg-row">
        <span class="zoom-name">${{esc(r.zoom)}}</span>
        <span class="mtg-tag" style="background:${{c.bg}};color:${{c.color}}">${{r.mtg}}</span>
        <span class="mins-tag">${{r.mins}}分</span>
      </div>`;
    }}).join('');
    html += `<div class="store-group" id="sg-${{code}}">
      <div class="sg-header" onclick="toggleSG('${{code}}')">
        <span class="sg-code">${{esc(code)}}</span>
        <span class="sg-name">${{esc(s.name)}}</span>
        <span class="sg-manager">${{s.manager?'/ '+esc(s.manager):''}}</span>
        <div class="sg-chips">${{chips}}</div>
        <span class="sg-area">${{esc(s.area)}}</span>
        <span class="arrow">▼</span>
      </div>
      <div class="sg-body">${{rowsHtml}}</div>
    </div>`;
  }});
  document.getElementById('content').innerHTML = html || '<div style="padding:40px;text-align:center;color:var(--dim)">該当なし</div>';
}}

function toggleSG(code) {{
  document.getElementById('sg-'+code).classList.toggle('collapsed');
}}

function renderMtg(data) {{
  let html = '';
  MEETINGS.forEach(mtg => {{
    const rows = data.filter(r=>r.mtg===mtg);
    if(!rows.length) return;
    const c=MTG_COLORS[mtg]||{{bg:'rgba(122,128,153,.15)',color:'#7a8099'}};
    const rowsHtml = rows.map(r=>{{
      const s=SM[r.store]||{{name:r.store,manager:'',area:''}};
      return `<div class="sg-row">
        <span class="sg-code mono">${{esc(r.store)}}</span>
        <span style="font-weight:500;min-width:180px">${{esc(s.name)}}</span>
        <span class="zoom-name">${{esc(r.zoom)}}</span>
        <span class="mins-tag">${{r.mins}}分</span>
      </div>`;
    }}).join('');
    html += `<div class="store-group">
      <div class="sg-header" style="cursor:default">
        <span class="mtg-tag" style="background:${{c.bg}};color:${{c.color}};padding:5px 14px;border-radius:8px;font-size:13px;font-weight:700">${{mtg}}</span>
        <span style="font-size:12px;color:var(--dim);margin-left:8px">${{rows.length}}名参加</span>
      </div>
      <div class="sg-body">${{rowsHtml}}</div>
    </div>`;
  }});
  document.getElementById('content').innerHTML = html || '<div style="padding:40px;text-align:center;color:var(--dim)">該当なし</div>';
}}

function renderFlat(data) {{
  const rows = data.map(r=>{{
    const s=SM[r.store]||{{name:r.store,manager:'',area:''}};
    const c=MTG_COLORS[r.mtg]||{{bg:'rgba(122,128,153,.15)',color:'#7a8099'}};
    return `<tr>
      <td class="mono">${{esc(r.store)}}</td>
      <td style="font-weight:500">${{esc(s.name)}}</td>
      <td style="font-size:12px;color:var(--dim)">${{esc(s.manager||'−')}}</td>
      <td><span class="mtg-tag" style="background:${{c.bg}};color:${{c.color}}">${{r.mtg}}</span></td>
      <td class="mono" style="text-align:center">${{r.mins}}分</td>
      <td style="font-size:12px;color:var(--dim)">${{esc(r.zoom)}}</td>
    </tr>`;
  }}).join('');
  document.getElementById('content').innerHTML=`
    <div class="twrap"><table>
      <thead><tr>
        <th>コード</th><th>店舗名</th><th>SM</th>
        <th>研修</th><th class="c">参加時間</th><th>Zoom表示名</th>
      </tr></thead>
      <tbody>${{rows||'<tr><td colspan="6" style="text-align:center;padding:40px;color:var(--dim)">該当なし</td></tr>'}}</tbody>
    </table></div>`;
}}

function exportCSV() {{
  const data = filtered();
  const rows = [['コード','店舗名','SM','エリア','研修','参加時間(分)','Zoom表示名']];
  data.forEach(r=>{{
    const s=SM[r.store]||{{name:r.store,manager:'',area:''}};
    rows.push([r.store,s.name,s.manager||'',s.area||'',r.mtg,r.mins,r.zoom]);
  }});
  const bom='\uFEFF',csv=bom+rows.map(r=>r.map(v=>`"${{v}}"`).join(',')).join('\\n');
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([csv],{{type:'text/csv'}}));
  a.download='Yogibo研修参加者詳細.csv';a.click();
}}

function esc(s){{return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}}

render();
</script>
</body></html>"""

with open('/mnt/user-data/outputs/yogibo_training_detail.html','w',encoding='utf-8') as f:
    f.write(detail_html)
print("detail HTML完成")
