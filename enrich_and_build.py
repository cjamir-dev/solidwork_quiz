# -*- coding: utf-8 -*-
"""Enrich questions and build feature-rich single-file quiz app."""
import json
import re
from pathlib import Path

ROOT = Path(r"d:\new app\quiz")
raw_path = ROOT / "_raw_qs.json"
bank_path = ROOT / "bank.json"
if raw_path.exists():
  raw = json.loads(raw_path.read_text(encoding="utf-8"))
elif bank_path.exists():
  raw = json.loads(bank_path.read_text(encoding="utf-8"))["questions"]
else:
  raw = json.loads((ROOT / "exams.json").read_text(encoding="utf-8"))
  # flatten unique from exams export
  seen = set()
  flat = []
  for e in raw:
    if e.get("id") == "bank-all":
      continue
    for q in e["questions"]:
      if q["text"] in seen:
        continue
      seen.add(q["text"])
      flat.append(q)
  raw = flat

TOPICS = {
  "sketch": "اسکچ",
  "part": "قطعه (Part)",
  "assembly": "مونتاژ",
  "drawing": "نقشه",
  "sheetmetal": "ورق‌کاری",
  "general": "عمومی",
}

TOPIC_RULES = [
  ("sheetmetal", r"sheet\s*metal|flatten|bend|hem|flange|ورق|خم|گسترده|insert bends"),
  ("drawing", r"drawing|slddrw|slddrt|section view|detail view|model items|balloon|annotation|نقشه|نما|تلرانس|callout|sheet format|projected view|crop view|auxiliary"),
  ("assembly", r"assembly|sldasm|mate|component|exploded|interference|مونتاژ|دمونتاژ|insert component|physical dynamics|cam\b|gear\b"),
  ("sketch", r"sketch|relation|dimension|under defined|construction|offset|trim|extend|collinear|concentric|equal|mid point|end point|arc\b|قید|اسکچ|ترسیم|خط |کمان|دایره"),
  ("part", r"extrude|revolve|sweep|loft|fillet|chamfer|shell|rib|pattern|feature|boss|axis\b|plane|helix|split|thin feature|mass|suppress|hole wizard|cosmos|simulation|render|material|قطعه|حجم|پوسته"),
]

DIFF_HARD = r"composite|table driven|broken-out|alternate position|multi-thickness|interference|physical dynamics|geometric tolerance|pierce|coradial|mate alignment"
DIFF_EASY = r"sldprt|sldasm|slddrw|extend|trim|extrude|mate\b|part ، assembly|نرم‌افزار solidworks شامل|پسوند"


def detect_topic(q):
  blob = (q["text"] + " " + " ".join(q["options"])).lower()
  for topic, pat in TOPIC_RULES:
    if re.search(pat, blob, re.I):
      return topic
  return "general"


def detect_diff(q):
  blob = (q["text"] + " " + " ".join(q["options"])).lower()
  if re.search(DIFF_HARD, blob, re.I):
    return "hard"
  if re.search(DIFF_EASY, blob, re.I):
    return "easy"
  return "medium"


def make_explain(q):
  ans = q["options"][q["correct"]]
  return "پاسخ درست «" + ans + "» است. این گزینه با تعریف و کاربرد استاندارد SolidWorks همخوانی دارد."


questions = []
for i, q in enumerate(raw, 1):
  topic = detect_topic(q)
  item = {
    "uid": "q" + str(i),
    "text": q["text"],
    "options": q["options"],
    "correct": q["correct"],
    "topic": topic,
    "difficulty": detect_diff(q),
    "explain": make_explain(q),
  }
  questions.append(item)

OVERRIDES = [
  ("ادامه دادن و رساندن یک خط", "sketch", "easy", "دستور Extend خط را تا برخورد با لبه یا خط دیگر ادامه می‌دهد."),
  ("هم‌مرکز کردن دو دایره", "sketch", "easy", "قید Concentric مراکز دو دایره یا کمان را روی هم منطبق می‌کند."),
  ("Part Mode", "general", "easy", "فایل قطعه با پسوند *.sldprt ذخیره می‌شود."),
  ("مقدار عددی Extrude", "part", "easy", "در حالت Blind مقدار عددی عمق Extrude را خودتان وارد می‌کنید."),
  ("دوطرفه از Sketch", "part", "medium", "Mid Plane اکسترود را به‌صورت متقارن از دو طرف صفحه اسکچ انجام می‌دهد."),
  ("به‌حالت ثابت (Fixed)", "assembly", "easy", "اولین قطعه واردشده در Assembly معمولاً Fixed است."),
  ("نرم‌افزار SolidWorks شامل", "general", "easy", "سه محیط اصلی SolidWorks عبارتند از Part، Assembly و Drawing."),
  ("Through All", "part", "easy", "Through All برش یا اکسترود را از تمام بدنه‌های مسیر عبور می‌دهد."),
]

for needle, topic, diff, explain in OVERRIDES:
  for q in questions:
    if needle in q["text"]:
      q["topic"] = topic
      q["difficulty"] = diff
      q["explain"] = explain
      break

topic_counts = {}
for q in questions:
  topic_counts[q["topic"]] = topic_counts.get(q["topic"], 0) + 1

DATA = {
  "questions": questions,
  "topics": TOPICS,
  "topicCounts": topic_counts,
  "total": len(questions),
}

(ROOT / "bank.json").write_text(json.dumps(DATA, ensure_ascii=False, indent=2), encoding="utf-8")
print("topics", topic_counts)

html = r'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0a3d3f">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="mobile-web-app-capable" content="yes">
<meta name="description" content="آزمون SolidWorks آفلاین برای موبایل">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<title>SolidWorks Quiz</title>
<style>
:root {
  --ink:#0b1f20;
  --muted:#3a5455;
  --brand:#0a3d3f;
  --brand2:#14686b;
  --brand-soft:#e6f3f2;
  --accent:#a85416;
  --accent-soft:#f8ebe1;
  --ok:#176b46;
  --bad:#a83232;
  --surface:#eef4f3;
  --card:#ffffff;
  --line:rgba(11,31,32,.14);
  --shadow:0 8px 28px rgba(16,42,43,.07);
  --radius:16px;
  --safe-b:env(safe-area-inset-bottom,0px);
  --safe-t:env(safe-area-inset-top,0px);
  --font:"Vazirmatn",Tahoma,sans-serif;
  --on-brand:#ffffff;
}
html[data-theme="dark"] {
  --ink:#f5fbfa;
  --muted:#d0e0df;
  --brand:#9fe3e4;
  --brand2:#5bc4c6;
  --brand-soft:rgba(159,227,228,.14);
  --accent:#f0b27a;
  --accent-soft:rgba(240,178,122,.16);
  --ok:#6edba5;
  --bad:#ff9a9a;
  --surface:#0a1213;
  --card:#172526;
  --line:rgba(245,251,250,.16);
  --shadow:0 10px 32px rgba(0,0,0,.4);
  --on-brand:#062223;
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;min-height:100%}
body{
  font-family:var(--font);color:var(--ink);line-height:1.7;
  background-color:var(--surface);
  background-image:
    linear-gradient(rgba(12,69,71,.035) 1px,transparent 1px),
    linear-gradient(90deg,rgba(12,69,71,.035) 1px,transparent 1px),
    radial-gradient(900px 480px at 100% -8%,rgba(24,117,120,.18),transparent 55%),
    radial-gradient(700px 420px at -10% 100%,rgba(184,97,31,.12),transparent 50%);
  background-size:28px 28px,28px 28px,auto,auto;
  background-attachment:fixed;
  padding:calc(12px + var(--safe-t)) 14px calc(20px + var(--safe-b));
  transition:background-color .25s ease,color .25s ease;
}
html[data-theme="dark"] body{
  background-image:
    linear-gradient(rgba(127,208,210,.05) 1px,transparent 1px),
    linear-gradient(90deg,rgba(127,208,210,.05) 1px,transparent 1px),
    radial-gradient(900px 480px at 100% -8%,rgba(58,174,177,.14),transparent 55%),
    radial-gradient(700px 420px at -10% 100%,rgba(224,154,92,.1),transparent 50%);
}
button,input{font:inherit}
.app{width:min(540px,100%);margin:0 auto}
.hidden{display:none!important}

.panel{
  background:rgba(255,255,255,.86);
  border:1px solid var(--line);
  border-radius:22px;
  box-shadow:var(--shadow);
  padding:18px 16px 16px;
  backdrop-filter:blur(10px);
  margin-bottom:12px;
  animation:rise .38s ease both;
}
html[data-theme="dark"] .panel{background:rgba(23,37,38,.94)}
.theme-btn{
  appearance:none;border:1px solid rgba(255,255,255,.28);background:rgba(255,255,255,.14);
  color:#fff;border-radius:14px;width:44px;height:44px;padding:0;
  cursor:pointer;display:grid;place-items:center;flex-shrink:0;
  transition:transform .2s ease,background .2s ease;
}
.theme-btn:active{transform:scale(.94)}
.theme-swap{
  position:relative;width:22px;height:22px;display:block;
}
.theme-swap svg{
  position:absolute;inset:0;width:22px;height:22px;
  transition:opacity .28s ease,transform .35s cubic-bezier(.2,.8,.2,1);
}
.theme-swap .icon-sun{
  opacity:0;transform:rotate(90deg) scale(.4);
}
.theme-swap .icon-star{
  opacity:1;transform:rotate(0) scale(1);
}
html[data-theme="dark"] .theme-swap .icon-sun{
  opacity:1;transform:rotate(0) scale(1);
}
html[data-theme="dark"] .theme-swap .icon-star{
  opacity:0;transform:rotate(-90deg) scale(.4);
}
html[data-theme="dark"] .theme-btn{
  border-color:rgba(159,227,228,.28);background:rgba(159,227,228,.12);color:#f5fbfa;
}
.hero-top{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;margin-bottom:10px}
html[data-theme="dark"] .hero{
  background:
    linear-gradient(145deg,rgba(8,28,30,.98),rgba(20,66,68,.94)),
    repeating-linear-gradient(-45deg,transparent,transparent 10px,rgba(255,255,255,.03) 10px,rgba(255,255,255,.03) 12px);
}
html[data-theme="dark"] .mode,
html[data-theme="dark"] .topic,
html[data-theme="dark"] .pills,
html[data-theme="dark"] .option,
html[data-theme="dark"] .chip,
html[data-theme="dark"] .stat,
html[data-theme="dark"] .review-item,
html[data-theme="dark"] .q-dot,
html[data-theme="dark"] .timer,
html[data-theme="dark"] .names input,
html[data-theme="dark"] .btn-secondary,
html[data-theme="dark"] .abort-btn,
html[data-theme="dark"] .modal-sheet,
html[data-theme="dark"] .about-entry{
  background:var(--card);
  color:var(--ink);
}
html[data-theme="dark"] .mode.hot.mode-cta,
html[data-theme="dark"] .mode.hot{
  background:linear-gradient(120deg,var(--card) 40%,rgba(240,178,122,.12));
}
html[data-theme="dark"] .flash{
  background:linear-gradient(160deg,var(--card),#1c3032);
}
html[data-theme="dark"] .btn-primary{
  background:#5bc4c6;color:#062223;
}
html[data-theme="dark"] .chip.active{
  background:#5bc4c6;border-color:#5bc4c6;color:#062223;
}
html[data-theme="dark"] .option .mark{
  background:#1c3032;border-color:rgba(245,251,250,.22);color:var(--muted);
}
html[data-theme="dark"] .option.selected .mark{
  background:var(--brand2);border-color:var(--brand2);color:#062223;
}
html[data-theme="dark"] .hint{
  background:rgba(159,227,228,.08);border-color:rgba(159,227,228,.22);color:var(--muted);
}
html[data-theme="dark"] .toggle{background:#2f4344}
html[data-theme="dark"] .modal-back{background:rgba(0,0,0,.66)}
html[data-theme="dark"] .mode.sim .mode-ico,
html[data-theme="dark"] .mode-ico,
html[data-theme="dark"] .topic-ico{
  background:var(--brand-soft);color:var(--brand);
}
html[data-theme="dark"] .mode.battle .mode-ico{
  background:rgba(255,154,154,.14);color:var(--bad);
}
html[data-theme="dark"] .mode.hot .mode-ico{
  background:var(--accent-soft);color:var(--accent);
}
html[data-theme="dark"] .q-num{
  background:var(--brand-soft);color:var(--brand);
}
html[data-theme="dark"] .badge{
  background:rgba(245,251,250,.08);color:var(--muted);
}
.about-entry{
  margin-top:14px;width:100%;text-align:right;border:1px solid var(--line);background:var(--card);
  border-radius:16px;padding:13px 12px;cursor:pointer;
  display:grid;grid-template-columns:44px 1fr auto;gap:12px;align-items:center;
}
.about-page{
  text-align:center;padding:8px 4px 4px;
}
.about-avatar{
  width:72px;height:72px;border-radius:20px;margin:0 auto 14px;
  display:grid;place-items:center;background:var(--brand-soft);color:var(--brand);
}
.about-avatar svg{width:34px;height:34px}
.about-name{margin:0 0 6px;font-size:1.25rem;font-weight:800;color:var(--ink)}
.about-role{margin:0 0 16px;color:var(--muted);font-size:.9rem;font-weight:600}
.about-body{
  text-align:right;color:var(--muted);font-size:.92rem;line-height:1.8;font-weight:500;
  background:rgba(11,31,32,.03);border:1px solid var(--line);border-radius:14px;padding:14px;
}
html[data-theme="dark"] .about-body{background:rgba(245,251,250,.04)}
html[data-theme="dark"] .about-entry{background:var(--card);color:var(--ink)}
.about-body strong{color:var(--ink);font-weight:700}
@keyframes rise{
  from{opacity:0;transform:translateY(10px)}
  to{opacity:1;transform:translateY(0)}
}
@keyframes pop{
  from{opacity:0;transform:scale(.96)}
  to{opacity:1;transform:scale(1)}
}

.hero{
  position:relative;overflow:hidden;border-radius:20px;padding:22px 18px 20px;
  background:
    linear-gradient(145deg,rgba(12,69,71,.96),rgba(24,117,120,.88)),
    repeating-linear-gradient(-45deg,transparent,transparent 10px,rgba(255,255,255,.03) 10px,rgba(255,255,255,.03) 12px);
  color:#fff;margin-bottom:14px;
}
.hero::after{
  content:"";position:absolute;inset:auto -20% -40% 40%;height:160px;
  background:radial-gradient(circle,rgba(255,255,255,.16),transparent 65%);pointer-events:none;
}
.hero-mark{
  width:48px;height:48px;border-radius:14px;display:grid;place-items:center;
  background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.2);margin:0;
}
.hero h1{
  margin:0;font-size:clamp(1.7rem,6.5vw,2.15rem);font-weight:800;letter-spacing:-.03em;line-height:1.2;
}
.hero p{margin:8px 0 0;opacity:.88;font-size:.92rem;font-weight:500;max-width:28ch}

.profile{
  display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:8px;
}
.pills{
  background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px 8px;text-align:center;
}
.pills b{display:block;font-size:1.2rem;color:var(--brand);font-weight:800;font-variant-numeric:tabular-nums}
.pills span{font-size:.72rem;color:var(--muted);font-weight:500}
.xp-wrap{margin:4px 0 4px}
.xp-label{display:flex;justify-content:space-between;font-size:.75rem;color:var(--muted);margin-bottom:6px}
.xp-bar{height:7px;background:rgba(12,69,71,.08);border-radius:8px;overflow:hidden}
.xp-bar>i{display:block;height:100%;background:linear-gradient(90deg,var(--brand),var(--brand2));width:0;transition:width .45s cubic-bezier(.2,.8,.2,1)}

.section-title{
  margin:18px 0 10px;font-size:.78rem;font-weight:700;color:var(--muted);
  letter-spacing:.04em;text-transform:uppercase;
}

.modes{display:grid;gap:9px}
.mode{
  width:100%;text-align:right;border:1px solid var(--line);background:var(--card);
  border-radius:16px;padding:13px 12px;cursor:pointer;
  display:grid;grid-template-columns:44px 1fr auto;gap:12px;align-items:center;
  transition:transform .15s ease,border-color .15s ease,box-shadow .15s ease;
}
.mode:active{transform:scale(.985)}
.mode:hover{border-color:rgba(24,117,120,.35);box-shadow:0 6px 18px rgba(16,42,43,.06)}
.mode-ico{
  width:44px;height:44px;border-radius:13px;display:grid;place-items:center;
  background:var(--brand-soft);color:var(--brand);flex-shrink:0;
}
.mode-ico svg{width:22px;height:22px}
.mode-body{display:grid;gap:2px;min-width:0}
.mode strong{color:var(--ink);font-size:.98rem;font-weight:700}
.mode .desc{color:var(--muted);font-size:.8rem;font-weight:500;line-height:1.45}
.mode-chevron{color:rgba(12,69,71,.35);font-size:1.2rem;padding-left:2px}
.mode .tag{
  display:inline-block;margin-top:4px;font-size:.68rem;padding:3px 8px;border-radius:8px;
  background:var(--accent-soft);color:var(--accent);width:fit-content;font-weight:700;
}
.mode.hot{
  border-color:rgba(184,97,31,.28);
  background:linear-gradient(120deg,#fff 55%,#fff7f0);
}
.mode.hot .mode-ico{background:var(--accent-soft);color:var(--accent)}
.mode.sim .mode-ico{background:#e8f5f4;color:var(--brand2)}
.mode.battle .mode-ico{background:#fdeeee;color:var(--bad)}
.mode.hot.mode-cta{
  grid-template-columns:44px 1fr;
  padding:16px 14px;
  margin-top:4px;
}
.mode.hot.mode-cta .mode-chevron{display:none}

.topics{display:grid;grid-template-columns:1fr 1fr;gap:9px}
.topic{
  border:1px solid var(--line);background:var(--card);border-radius:16px;padding:14px 12px;
  text-align:right;cursor:pointer;transition:transform .12s ease,border-color .15s;
  animation:pop .35s ease both;
}
.topic:active{transform:scale(.98)}
.topic .topic-ico{
  width:36px;height:36px;border-radius:11px;display:grid;place-items:center;
  background:var(--brand-soft);color:var(--brand);margin-bottom:10px;
}
.topic .topic-ico svg{width:18px;height:18px}
.topic strong{display:block;color:var(--ink);font-size:.92rem;font-weight:700}
.topic span{font-size:.75rem;color:var(--muted);font-weight:500}

.hint{
  font-size:.8rem;color:var(--muted);background:rgba(12,69,71,.04);
  border:1px dashed rgba(12,69,71,.14);border-radius:14px;padding:12px;margin-top:14px;line-height:1.55;
}
.field{margin-top:14px}
.field label{display:block;font-size:.8rem;color:var(--muted);margin-bottom:8px;font-weight:600}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{
  border:1px solid var(--line);background:var(--card);border-radius:12px;padding:10px 14px;
  cursor:pointer;font-weight:600;color:var(--ink);transition:background .15s,color .15s,border-color .15s;
}
.chip.active{background:var(--brand);color:var(--on-brand);border-color:var(--brand)}
.row{
  display:flex;justify-content:space-between;align-items:center;gap:10px;
  padding:14px 4px;border-top:1px solid var(--line);margin-top:8px;
}
.row strong{font-size:.92rem}
.toggle{
  width:50px;height:30px;border:none;border-radius:10px;background:#d5e0df;
  position:relative;cursor:pointer;transition:background .2s;
}
.toggle.on{background:var(--brand2)}
.toggle i{
  position:absolute;top:3px;right:3px;width:24px;height:24px;border-radius:8px;background:#fff;
  transition:right .2s cubic-bezier(.2,.8,.2,1);box-shadow:0 1px 4px rgba(0,0,0,.08);
}
.toggle.on i{right:23px}
.actions{display:grid;gap:8px;margin-top:16px}
.btn{
  appearance:none;border:none;border-radius:14px;padding:14px 16px;font-weight:700;cursor:pointer;
  transition:transform .12s ease,opacity .12s,filter .12s;
}
.btn:active{transform:scale(.985)}
.btn:disabled{opacity:.45}
.btn-primary{background:var(--brand);color:var(--on-brand)}
.btn-primary:hover{filter:brightness(1.06)}
.btn-secondary{background:var(--card);color:var(--brand);border:1px solid var(--line)}
.btn-accent{background:var(--accent);color:#fff}
.btn-ghost{background:transparent;color:var(--muted);font-weight:600}
.btn-danger{background:var(--bad);color:#fff}

.topbar{display:flex;gap:8px;align-items:center;margin-bottom:12px}
.progress-wrap{flex:1}
.progress-meta{display:flex;justify-content:space-between;font-size:.78rem;color:var(--muted);margin-bottom:6px;font-weight:600}
.bar{height:7px;background:rgba(12,69,71,.08);border-radius:8px;overflow:hidden}
.bar>i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--brand),#2a9b87);transition:width .3s cubic-bezier(.2,.8,.2,1)}
.timer{
  font-variant-numeric:tabular-nums;background:var(--card);border:1px solid var(--line);
  border-radius:12px;padding:7px 10px;font-size:.84rem;color:var(--brand);min-width:66px;text-align:center;font-weight:700;
}
.timer.warn{color:var(--accent);border-color:rgba(184,97,31,.35);background:var(--accent-soft)}
.timer.danger{color:var(--bad);border-color:rgba(182,59,59,.35);animation:pulse 1s infinite}
@keyframes pulse{50%{opacity:.55}}

.quiz-head{
  display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:12px;
}
.quiz-head .left{display:flex;align-items:center;gap:8px;min-width:0;flex-wrap:wrap}
.abort-btn{
  appearance:none;border:1px solid rgba(182,59,59,.28);background:#fff;color:var(--bad);
  border-radius:12px;padding:8px 12px;font-size:.8rem;font-weight:700;cursor:pointer;white-space:nowrap;
}
.abort-btn:active{transform:scale(.97)}
.flag-btn.on{
  background:var(--accent-soft)!important;border-color:rgba(184,97,31,.35)!important;color:var(--accent)!important;
}
.q-num{
  display:inline-block;background:var(--brand-soft);color:var(--brand);
  border-radius:10px;padding:5px 10px;font-size:.78rem;font-weight:700;
}
.q-meta{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px}
.badge{
  font-size:.7rem;padding:4px 9px;border-radius:8px;background:rgba(12,69,71,.06);
  color:var(--muted);font-weight:600;
}
.q-text{font-size:1.08rem;font-weight:700;margin:0 0 14px;line-height:1.65;letter-spacing:-.01em}
.options{display:grid;gap:9px}
.option{
  display:flex;gap:12px;align-items:flex-start;width:100%;text-align:right;
  padding:14px 13px;border-radius:14px;border:1.5px solid var(--line);background:var(--card);cursor:pointer;
  transition:border-color .15s,background .15s,transform .12s;
}
.option:active{transform:scale(.99)}
.option .mark{
  flex:0 0 30px;height:30px;border-radius:10px;border:1.5px solid rgba(11,31,32,.22);display:grid;place-items:center;
  font-size:.78rem;color:var(--muted);font-weight:700;background:rgba(11,31,32,.04);
}
.option.selected{border-color:var(--brand2);background:rgba(20,104,107,.08)}
.option.selected .mark{background:var(--brand2);border-color:var(--brand2);color:var(--on-brand)}
.option.correct{border-color:var(--ok);background:rgba(31,122,82,.08)}
.option.wrong{border-color:var(--bad);background:rgba(182,59,59,.07)}
.feedback{margin-top:10px;padding:12px;border-radius:12px;font-size:.88rem;display:none;font-weight:500;line-height:1.55}
.feedback.show{display:block;animation:rise .25s ease}
.feedback.ok{background:rgba(31,122,82,.1);color:var(--ok)}
.feedback.bad{background:rgba(182,59,59,.08);color:var(--bad)}
.nav{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:14px}

.q-map{
  display:flex;flex-wrap:wrap;gap:6px;margin:0 0 12px;padding:10px;border-radius:14px;
  background:rgba(12,69,71,.035);border:1px solid var(--line);
}
.q-dot{
  width:34px;height:34px;border-radius:10px;border:1px solid var(--line);background:#fff;
  font-size:.76rem;font-weight:700;color:var(--muted);cursor:pointer;
  display:grid;place-items:center;position:relative;transition:transform .12s;
}
.q-dot:not([disabled]):active{transform:scale(.94)}
.q-dot.answered{background:var(--brand-soft);border-color:rgba(24,117,120,.35);color:var(--brand)}
.q-dot.current{box-shadow:inset 0 0 0 2px var(--brand2)}
.q-dot.flagged::after{
  content:"";position:absolute;top:3px;left:3px;width:7px;height:7px;border-radius:50%;background:var(--accent);
}
.q-dot.locked{opacity:.5;cursor:default}
.flag-note{
  display:none;margin:0 0 10px;padding:9px 11px;border-radius:12px;font-size:.8rem;
  background:var(--accent-soft);color:var(--accent);font-weight:600;
}
.flag-note.show{display:block;animation:rise .25s ease}

.modal-back{
  position:fixed;inset:0;background:rgba(10,30,31,.48);z-index:50;
  display:flex;align-items:flex-end;justify-content:center;padding:16px;padding-bottom:calc(16px + var(--safe-b));
  animation:fade .2s ease;
}
@keyframes fade{from{opacity:0}to{opacity:1}}
.modal-sheet{
  width:min(520px,100%);background:#fff;border-radius:22px 22px 18px 18px;padding:20px 16px 14px;
  box-shadow:0 -10px 40px rgba(0,0,0,.16);animation:rise .28s ease;
}
.modal-sheet h3{margin:0 0 6px;color:var(--brand);font-size:1.12rem;font-weight:800}
.modal-sheet p{margin:0 0 14px;color:var(--muted);font-size:.9rem}
.modal-actions{display:grid;gap:8px}

.score-hero{text-align:center;padding:12px 0 4px}
.score-hero .pct{
  font-size:clamp(2.6rem,12vw,3.4rem);font-weight:800;color:var(--brand);line-height:1;
  letter-spacing:-.03em;
}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:16px 0}
.stat{
  background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 8px;text-align:center;
}
.stat b{display:block;font-size:1.35rem;font-weight:800}
.stat span{font-size:.72rem;color:var(--muted);font-weight:600}
.stat.ok b{color:var(--ok)} .stat.bad b{color:var(--bad)} .stat.skip b{color:var(--muted)}
.review-item{border:1px solid var(--line);border-radius:14px;padding:13px;margin-top:10px;background:var(--card)}
.flash{
  min-height:230px;border-radius:18px;border:1px solid var(--line);background:
    linear-gradient(160deg,#fff,#f3faf9);padding:20px;display:flex;flex-direction:column;justify-content:center;
  cursor:pointer;box-shadow:var(--shadow);transition:transform .15s;
}
.flash:active{transform:scale(.99)}
.flash .side{font-size:.75rem;color:var(--muted);margin-bottom:8px;font-weight:700;letter-spacing:.03em}
.flash .body{font-size:1.05rem;font-weight:700;line-height:1.7;white-space:pre-wrap}
.names{display:grid;gap:8px}
.names input{
  width:100%;padding:13px 14px;border-radius:12px;border:1px solid var(--line);background:#fff;font-weight:500;
}
.duel-banner{
  background:linear-gradient(135deg,var(--brand2),var(--brand));color:#fff;border-radius:14px;
  padding:12px;margin-bottom:12px;text-align:center;font-weight:700;
}
#shareCanvas{position:fixed;left:-9999px;top:0}
.page-title{margin:0 0 4px;font-size:1.2rem;font-weight:800;color:var(--brand)}
.page-sub{margin:0 0 14px;color:var(--muted);font-size:.9rem;font-weight:500}
@media (prefers-reduced-motion:reduce){
  .panel,.topic,.feedback,.flag-note,.modal-back,.modal-sheet{animation:none}
}
</style>
</head>
<body>
<div class="app" id="app">

<section id="screen-home" class="panel">
  <header class="hero">
    <div class="hero-top">
      <div class="hero-mark" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" width="26" height="26"><path d="M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3z" stroke="#fff" stroke-width="1.7"/><path d="M12 12l8-4.5M12 12v9M12 12L4 7.5" stroke="#fff" stroke-width="1.7"/></svg>
      </div>
      <button type="button" class="theme-btn" id="themeBtn" aria-label="تغییر تم روشن و تاریک" title="تغییر تم">
        <span class="theme-swap" aria-hidden="true">
          <svg class="icon-sun" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="1.8"/>
            <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
          </svg>
          <svg class="icon-star" viewBox="0 0 24 24" fill="none">
            <path d="M12 3.2l2.2 4.6 5.1.7-3.7 3.6.9 5.1L12 14.9 7.5 17.2l.9-5.1L4.7 8.5l5.1-.7L12 3.2z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>
          </svg>
        </span>
      </button>
    </div>
    <h1>SolidWorks Quiz</h1>
    <p>تمرین دقیق، آفلاین و مخصوص موبایل برای آمادگی آزمون</p>
  </header>

  <div class="profile">
    <div class="pills"><b id="lvlLabel">۱</b><span>سطح</span></div>
    <div class="pills"><b id="xpLabel">۰</b><span>امتیاز</span></div>
    <div class="pills"><b id="streakLabel">۰</b><span>روز پیاپی</span></div>
  </div>
  <div class="xp-wrap">
    <div class="xp-label"><span>پیشرفت سطح</span><span id="xpNeedLabel"></span></div>
    <div class="xp-bar"><i id="xpBar"></i></div>
  </div>

  <button type="button" class="mode hot mode-cta" data-mode="quick">
    <span class="mode-ico"><svg viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
    <span class="mode-body">
      <strong>شروع سریع</strong>
      <span class="desc">۱۰ سوال تصادفی — همین حالا شروع کنید</span>
      <span class="tag">پیشنهادی</span>
    </span>
  </button>

  <div class="section-title">حالت‌های تمرین</div>
  <div class="modes">
    <button type="button" class="mode" data-mode="topic">
      <span class="mode-ico"><svg viewBox="0 0 24 24" fill="none"><path d="M4 6h7v7H4V6zm9 0h7v4h-7V6zm0 6h7v6h-7v-6zM4 15h7v3H4v-3z" stroke="currentColor" stroke-width="1.7"/></svg></span>
      <span class="mode-body"><strong>تمرین موضوعی</strong><span class="desc">اسکچ، قطعه، مونتاژ، نقشه، ورق‌کاری</span></span>
      <span class="mode-chevron">‹</span>
    </button>
    <button type="button" class="mode sim" data-mode="exam">
      <span class="mode-ico"><svg viewBox="0 0 24 24" fill="none"><path d="M8 4h8v16H8V4z" stroke="currentColor" stroke-width="1.7"/><path d="M10 8h4M10 12h4M10 16h2" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg></span>
      <span class="mode-body"><strong>شبیه‌ساز امتحان</strong><span class="desc">تایمر · بدون برگشت · حس آزمون واقعی</span></span>
      <span class="mode-chevron">‹</span>
    </button>
    <button type="button" class="mode battle" data-mode="battle">
      <span class="mode-ico"><svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="8" stroke="currentColor" stroke-width="1.7"/><path d="M12 8v5l3 2" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg></span>
      <span class="mode-body"><strong>نبرد با زمان</strong><span class="desc">۱۰ سوال در ۳ دقیقه · امتیاز سرعت</span></span>
      <span class="mode-chevron">‹</span>
    </button>
    <button type="button" class="mode" data-mode="adaptive">
      <span class="mode-ico"><svg viewBox="0 0 24 24" fill="none"><path d="M4 18l5-5 3 3 8-8" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/><path d="M15 8h5v5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg></span>
      <span class="mode-body"><strong>سختی تطبیقی</strong><span class="desc">سوال بعدی با عملکرد شما تنظیم می‌شود</span></span>
      <span class="mode-chevron">‹</span>
    </button>
    <button type="button" class="mode" data-mode="duel">
      <span class="mode-ico"><svg viewBox="0 0 24 24" fill="none"><circle cx="8" cy="10" r="3" stroke="currentColor" stroke-width="1.7"/><circle cx="16" cy="10" r="3" stroke="currentColor" stroke-width="1.7"/><path d="M3 19c1.5-3 3.5-4 5-4s3.5 1 5 4M13 19c1-2 2.5-3.5 3-3.5s2.5 1 5 3.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg></span>
      <span class="mode-body"><strong>رقابت دونفره</strong><span class="desc">روی یک گوشی · مقایسه درصد</span></span>
      <span class="mode-chevron">‹</span>
    </button>
    <button type="button" class="mode" data-mode="cards" id="cardsModeBtn">
      <span class="mode-ico"><svg viewBox="0 0 24 24" fill="none"><rect x="5" y="5" width="11" height="14" rx="2" stroke="currentColor" stroke-width="1.7"/><path d="M9 5V4a1 1 0 011-1h8a1 1 0 011 1v14a1 1 0 01-1 1h-1" stroke="currentColor" stroke-width="1.7"/></svg></span>
      <span class="mode-body"><strong>کارت مرور غلط‌ها</strong><span class="desc" id="cardsHint">سوالات غلط را مثل فلش‌کارت مرور کنید</span></span>
      <span class="mode-chevron">‹</span>
    </button>
  </div>

  <button type="button" class="about-entry" id="aboutBtn">
    <span class="mode-ico"><svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="8" r="3.2" stroke="currentColor" stroke-width="1.7"/><path d="M5 19c1.8-3.2 4-4.5 7-4.5S17.2 15.8 19 19" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg></span>
    <span class="mode-body"><strong>درباره من</strong><span class="desc">معرفی سازنده اپ</span></span>
    <span class="mode-chevron">‹</span>
  </button>
</section>

<section id="screen-about" class="panel hidden">
  <div class="about-page">
    <div class="about-avatar" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="8" r="3.2" stroke="currentColor" stroke-width="1.7"/><path d="M5 19c1.8-3.2 4-4.5 7-4.5S17.2 15.8 19 19" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
    </div>
    <h2 class="about-name" id="aboutName">به‌زودی</h2>
    <p class="about-role" id="aboutRole">سازنده SolidWorks Quiz</p>
    <div class="about-body" id="aboutContent">
      <strong>نام:</strong> به‌زودی تکمیل می‌شود<br>
      <strong>توضیحات:</strong> این بخش برای معرفی سازنده اپ آماده شده. اطلاعات دقیق را بعداً اینجا می‌نویسیم.
    </div>
  </div>
  <div class="actions">
    <button type="button" class="btn btn-secondary" data-back="home">بازگشت</button>
  </div>
</section>

<section id="screen-topics" class="panel hidden">
  <h2 class="page-title">موضوع را انتخاب کنید</h2>
  <p class="page-sub">هر موضوع، بانک سوال مخصوص خودش را دارد.</p>
  <div class="topics" id="topicGrid"></div>
  <div class="actions"><button type="button" class="btn btn-secondary" data-back="home">بازگشت</button></div>
</section>

<section id="screen-setup" class="panel hidden">
  <h2 class="page-title" id="setupTitle">تنظیمات</h2>
  <p class="page-sub" id="setupSub"></p>
  <div class="field" id="countField">
    <label>تعداد سوالات</label>
    <div class="chips" id="countChips"></div>
  </div>
  <div class="names hidden" id="duelNames">
    <input id="p1Name" placeholder="نام بازیکن ۱" value="بازیکن ۱">
    <input id="p2Name" placeholder="نام بازیکن ۲" value="بازیکن ۲">
  </div>
  <div class="row" id="shuffleRow">
    <div><strong>سوالات تصادفی</strong><div style="font-size:.8rem;color:var(--muted)">ترتیب بانک به‌هم بریزد</div></div>
    <button type="button" class="toggle on" id="shuffleToggle"><i></i></button>
  </div>
  <div class="row" id="feedbackRow">
    <div><strong>بازخورد فوری</strong><div style="font-size:.8rem;color:var(--muted)">بعد از هر پاسخ، درست/غلط و توضیح</div></div>
    <button type="button" class="toggle on" id="feedbackToggle"><i></i></button>
  </div>
  <div class="actions">
    <button type="button" class="btn btn-primary" id="startBtn">شروع آزمون</button>
    <button type="button" class="btn btn-secondary" data-back="home">بازگشت</button>
  </div>
</section>

<section id="screen-quiz" class="panel hidden">
  <div class="quiz-head">
    <div class="left">
      <span class="q-num" id="qNum" style="margin:0">سوال ۱</span>
      <span id="modeChip" class="badge"></span>
    </div>
    <button type="button" class="abort-btn" id="abortBtn">لغو آزمون</button>
  </div>
  <div class="duel-banner hidden" id="duelBanner"></div>
  <div class="topbar">
    <div class="progress-wrap">
      <div class="progress-meta"><span id="progressText">۱ از ۱۰</span><span id="flagCountLabel"></span></div>
      <div class="bar"><i id="progressBar"></i></div>
    </div>
    <div class="timer hidden" id="timerBox">۰۰:۰۰</div>
  </div>
  <div class="q-map" id="qMap" aria-label="نقشه سوالات"></div>
  <div class="flag-note" id="flagNote">این سوال نشان‌گذاری شده — بعداً می‌توانید از نقشه بالا به آن برگردید.</div>
  <div class="q-meta" id="qMeta"></div>
  <p class="q-text" id="qText"></p>
  <div class="options" id="options"></div>
  <div class="feedback" id="feedback"></div>
  <div class="nav" id="quizNav">
    <button type="button" class="btn btn-secondary" id="prevBtn">قبلی</button>
    <button type="button" class="btn btn-secondary flag-btn" id="flagBtn">☆ نشان</button>
    <button type="button" class="btn btn-primary" id="nextBtn">بعدی</button>
  </div>
  <div class="actions"><button type="button" class="btn btn-accent" id="finishBtn">پایان و تصحیح</button></div>
</section>

<div id="abortModal" class="modal-back hidden">
  <div class="modal-sheet" role="dialog" aria-modal="true" aria-labelledby="abortTitle">
    <h3 id="abortTitle">لغو آزمون؟</h3>
    <p id="abortMsg">پیشرفت این آزمون ذخیره نمی‌شود و به صفحه اصلی برمی‌گردید.</p>
    <div class="modal-actions">
      <button type="button" class="btn btn-danger" id="abortConfirm">بله، لغو شود</button>
      <button type="button" class="btn btn-secondary" id="abortCancel">ادامه آزمون</button>
    </div>
  </div>
</div>

<section id="screen-result" class="panel hidden">
  <div class="score-hero">
    <div class="pct" id="scorePct">۰٪</div>
    <div id="scoreSub" style="color:var(--muted)"></div>
    <div id="xpGain" style="margin-top:8px;color:var(--brand2);font-weight:700"></div>
  </div>
  <div class="stats">
    <div class="stat ok"><b id="statOk">0</b><span>درست</span></div>
    <div class="stat bad"><b id="statBad">0</b><span>غلط</span></div>
    <div class="stat skip"><b id="statSkip">0</b><span>نزده</span></div>
  </div>
  <div id="duelCompare" class="hidden"></div>
  <div class="actions">
    <button type="button" class="btn btn-primary" id="shareBtn">اشتراک‌گذاری نتیجه (عکس)</button>
    <button type="button" class="btn btn-secondary" id="reviewWrongBtn">مرور اشتباهات</button>
    <button type="button" class="btn btn-secondary" id="retryBtn">دوباره با همین حالت</button>
    <button type="button" class="btn btn-ghost" id="homeBtn">صفحه اصلی</button>
  </div>
  <div id="reviewBox"></div>
  <canvas id="shareCanvas" width="720" height="980"></canvas>
</section>

<section id="screen-cards" class="panel hidden">
  <h2 class="page-title">کارت مرور غلط‌ها</h2>
  <p class="page-sub" id="cardProgress"></p>
  <div class="flash" id="flashCard">
    <div class="side" id="flashSide">روی کارت بزنید</div>
    <div class="body" id="flashBody"></div>
  </div>
  <div class="actions" style="margin-top:12px">
    <button type="button" class="btn btn-primary" id="cardNext">کارت بعدی</button>
    <button type="button" class="btn btn-secondary" id="cardKnew">بلدم — حذف از لیست</button>
    <button type="button" class="btn btn-ghost" data-back="home">بازگشت</button>
  </div>
</section>

</div>
<script>
__DATA__
</script>
<script>
(function () {
  const LABELS = ["الف", "ب", "ج", "د"]
  const KEYS = {
    profile: "swq_profile_v2",
    wrongs: "swq_wrongs_v2",
    theme: "swq_theme_v1",
  }
  const DIFF_ORDER = { easy: 0, medium: 1, hard: 2 }
  const MODE_META = {
    quick: { title: "شروع سریع", count: 10, timer: false, noBack: false, feedback: true, battle: false, adaptive: false, duel: false },
    topic: { title: "تمرین موضوعی", count: 15, timer: false, noBack: false, feedback: true, battle: false, adaptive: false, duel: false },
    exam: { title: "شبیه‌ساز امتحان", count: 20, timer: true, noBack: true, feedback: false, battle: false, adaptive: false, duel: false, secPerQ: 60 },
    battle: { title: "نبرد با زمان", count: 10, timer: true, noBack: true, feedback: false, battle: true, adaptive: false, duel: false, totalSec: 180 },
    adaptive: { title: "سختی تطبیقی", count: 15, timer: false, noBack: false, feedback: true, battle: false, adaptive: true, duel: false },
    duel: { title: "رقابت دونفره", count: 10, timer: false, noBack: false, feedback: false, battle: false, adaptive: false, duel: true },
  }

  const bank = window.BANK
  const $ = (id) => document.getElementById(id)
  const screens = ["home", "topics", "setup", "quiz", "result", "cards", "about"]

  const state = {
    mode: "quick",
    topic: null,
    countMode: 10,
    shuffle: true,
    feedbackOn: true,
    questions: [],
    answers: [],
    flags: [],
    locked: [],
    index: 0,
    startedAt: 0,
    endsAt: 0,
    timerId: null,
    adaptiveLevel: 1,
    duel: { active: false, turn: 1, p1: "بازیکن ۱", p2: "بازیکن ۲", score1: null, sharedQs: null },
    lastGrade: null,
    cards: [],
    cardIndex: 0,
    cardFlipped: false,
  }

  function show(name) {
    screens.forEach((s) => $("screen-" + s).classList.toggle("hidden", s !== name))
    window.scrollTo({ top: 0, behavior: "smooth" })
  }

  function loadProfile() {
    try {
      return Object.assign({ xp: 0, level: 1, streak: 0, lastDay: "" }, JSON.parse(localStorage.getItem(KEYS.profile) || "{}"))
    } catch (e) {
      return { xp: 0, level: 1, streak: 0, lastDay: "" }
    }
  }

  function saveProfile(p) {
    localStorage.setItem(KEYS.profile, JSON.stringify(p))
  }

  function xpForLevel(level) {
    return 80 + (level - 1) * 40
  }

  function todayKey() {
    const d = new Date()
    return d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate()
  }

  function yesterdayKey() {
    const d = new Date()
    d.setDate(d.getDate() - 1)
    return d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate()
  }

  function applyTheme(theme) {
    const next = theme === "dark" ? "dark" : "light"
    document.documentElement.setAttribute("data-theme", next)
    localStorage.setItem(KEYS.theme, next)
    const meta = document.querySelector('meta[name="theme-color"]')
    if (meta) meta.setAttribute("content", next === "dark" ? "#0a1213" : "#0a3d3f")
    const btn = $("themeBtn")
    if (btn) btn.setAttribute("aria-label", next === "dark" ? "فعال کردن حالت روشن" : "فعال کردن حالت تاریک")
  }

  function initTheme() {
    const saved = localStorage.getItem(KEYS.theme)
    if (saved === "dark" || saved === "light") {
      applyTheme(saved)
      return
    }
    const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
    applyTheme(prefersDark ? "dark" : "light")
  }

  function renderProfile() {
    const p = loadProfile()
    const need = xpForLevel(p.level)
    $("lvlLabel").textContent = String(p.level)
    $("xpLabel").textContent = String(p.xp)
    $("streakLabel").textContent = String(p.streak)
    $("xpBar").style.width = Math.min(100, Math.round((p.xp / need) * 100)) + "%"
    const needLabel = $("xpNeedLabel")
    if (needLabel) needLabel.textContent = p.xp + " / " + need
    const wrongs = loadWrongs()
    $("cardsHint").textContent = wrongs.length
      ? wrongs.length + " کارت برای مرور آماده است"
      : "سوالات غلط را مثل فلش‌کارت مرور کنید"
  }

  const TOPIC_ICONS = {
    sketch: '<svg viewBox="0 0 24 24" fill="none"><path d="M4 17l7-7 3 3 6-6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/><path d="M14 7h5v5" stroke="currentColor" stroke-width="1.7"/></svg>',
    part: '<svg viewBox="0 0 24 24" fill="none"><path d="M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3z" stroke="currentColor" stroke-width="1.7"/></svg>',
    assembly: '<svg viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="1.7"/><rect x="13" y="13" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="1.7"/><path d="M11 7h3v3M13 14V11h-2" stroke="currentColor" stroke-width="1.7"/></svg>',
    drawing: '<svg viewBox="0 0 24 24" fill="none"><path d="M6 4h9l3 3v13H6V4z" stroke="currentColor" stroke-width="1.7"/><path d="M9 11h6M9 15h4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>',
    sheetmetal: '<svg viewBox="0 0 24 24" fill="none"><path d="M4 8h12l4 4v8H4V8z" stroke="currentColor" stroke-width="1.7"/><path d="M4 12h16" stroke="currentColor" stroke-width="1.7"/></svg>',
    general: '<svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="8" stroke="currentColor" stroke-width="1.7"/><path d="M12 8v4l3 2" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>',
  }

  function renderTopics() {
    const grid = $("topicGrid")
    grid.innerHTML = Object.keys(bank.topics).map((key, idx) => {
      const n = bank.topicCounts[key] || 0
      if (!n) return ""
      const ico = TOPIC_ICONS[key] || TOPIC_ICONS.general
      return '<button type="button" class="topic" data-topic="' + key + '" style="animation-delay:' + (idx * 0.04) + 's">' +
        '<div class="topic-ico">' + ico + "</div>" +
        "<strong>" + bank.topics[key] + "</strong><span>" + n + " سوال</span></button>"
    }).join("")
    grid.querySelectorAll(".topic").forEach((btn) => btn.addEventListener("click", () => {
      state.topic = btn.dataset.topic
      openSetup("topic")
    }))
  }

  function loadWrongs() {
    try { return JSON.parse(localStorage.getItem(KEYS.wrongs) || "[]") } catch (e) { return [] }
  }

  function saveWrongs(list) {
    localStorage.setItem(KEYS.wrongs, JSON.stringify(list.slice(0, 80)))
  }

  function addWrong(q) {
    const list = loadWrongs().filter((x) => x.uid !== q.uid)
    list.unshift({ uid: q.uid, text: q.text, options: q.options, correct: q.correct, explain: q.explain, topic: q.topic })
    saveWrongs(list)
  }

  function removeWrong(uid) {
    saveWrongs(loadWrongs().filter((x) => x.uid !== uid))
  }

  function shuffle(arr) {
    const a = arr.slice()
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      const t = a[i]; a[i] = a[j]; a[j] = t
    }
    return a
  }

  function pad(n) { return String(n).padStart(2, "0") }
  function formatTime(ms) {
    const s = Math.max(0, Math.ceil(ms / 1000))
    return pad(Math.floor(s / 60)) + ":" + pad(s % 60)
  }

  function poolForMode() {
    let pool = bank.questions.slice()
    if (state.mode === "topic" && state.topic) {
      pool = pool.filter((q) => q.topic === state.topic)
    }
    return pool
  }

  function pickNextAdaptive(usedSet) {
    const want = state.adaptiveLevel <= 0 ? "easy" : state.adaptiveLevel >= 2 ? "hard" : "medium"
    const pool = shuffle(bank.questions.filter((q) => !usedSet.has(q.uid)))
    return pool.find((q) => q.difficulty === want) || pool[0] || null
  }

  function buildSession() {
    const meta = MODE_META[state.mode]
    let n = state.countMode === "all" ? poolForMode().length : Number(state.countMode)
    n = Math.max(1, Math.min(n, poolForMode().length || bank.questions.length))

    let qs
    if (state.mode === "adaptive") {
      state.adaptiveLevel = 1
      state.adaptiveTarget = n
      const used = new Set()
      const first = pickNextAdaptive(used)
      qs = first ? [first] : []
    } else if (state.duel.active && state.duel.turn === 2 && state.duel.sharedQs) {
      qs = state.duel.sharedQs
    } else {
      let pool = poolForMode()
      if (state.shuffle) pool = shuffle(pool)
      qs = pool.slice(0, n)
    }

    if (state.mode === "duel" && state.duel.turn === 1) {
      state.duel.sharedQs = qs
    }

    state.questions = qs
    state.answers = Array(qs.length).fill(null)
    state.flags = Array(qs.length).fill(false)
    state.locked = Array(qs.length).fill(false)
    state.index = 0
    state.startedAt = Date.now()
    state.feedbackOn = meta.feedback ? state.feedbackOn : false

    if (meta.battle) state.endsAt = state.startedAt + meta.totalSec * 1000
    else if (meta.timer) state.endsAt = state.startedAt + n * (meta.secPerQ || 60) * 1000
    else state.endsAt = 0
  }

  function stopTimer() {
    if (state.timerId) { clearInterval(state.timerId); state.timerId = null }
  }

  function startTimer() {
    stopTimer()
    const box = $("timerBox")
    if (!state.endsAt) { box.classList.add("hidden"); return }
    box.classList.remove("hidden")
    const tick = () => {
      const left = state.endsAt - Date.now()
      box.textContent = formatTime(left)
      box.classList.toggle("warn", left <= 60000)
      box.classList.toggle("danger", left <= 20000)
      if (left <= 0) { stopTimer(); finishQuiz(true) }
    }
    tick()
    state.timerId = setInterval(tick, 250)
  }

  function openSetup(mode, opts) {
    opts = opts || {}
    const keep = !!opts.keep
    state.mode = mode
    const meta = MODE_META[mode]
    if (!keep) {
      state.countMode = meta.count
      state.feedbackOn = !!meta.feedback
    }
    $("setupTitle").textContent = meta.title
    const available = poolForMode().length
    $("setupSub").textContent = mode === "topic" && state.topic
      ? ("موضوع: " + bank.topics[state.topic] + " · " + available + " سوال موجود")
      : ("بانک کل: " + available + " سوال موجود")
    $("duelNames").classList.toggle("hidden", !meta.duel)
    $("shuffleRow").classList.toggle("hidden", mode === "adaptive" || mode === "battle")
    $("feedbackRow").classList.toggle("hidden", meta.duel || mode === "exam" || mode === "battle")
    $("feedbackToggle").classList.toggle("on", state.feedbackOn)
    $("shuffleToggle").classList.toggle("on", state.shuffle)

    let presets = mode === "exam" ? [20, 30, 40, "all"]
      : mode === "battle" || mode === "quick" || mode === "duel" ? [10]
      : [10, 15, 20, 30]
    presets = presets.filter((c) => c === "all" || c <= available)
    if (!presets.length) presets = ["all"]
    if (state.countMode !== "all" && !presets.includes(state.countMode)) {
      state.countMode = presets[0] === "all" ? "all" : presets[0]
    }

    const chips = $("countChips")
    if (mode === "battle" || mode === "quick") {
      $("countField").classList.add("hidden")
    } else {
      $("countField").classList.remove("hidden")
      chips.innerHTML = presets.map((c) => {
        const label = c === "all" ? "همه (" + available + ")" : String(c)
        const active = state.countMode === c ? " active" : ""
        return '<button type="button" class="chip' + active + '" data-c="' + c + '">' + label + "</button>"
      }).join("")
      chips.querySelectorAll(".chip").forEach((btn) => btn.addEventListener("click", () => {
        const v = btn.dataset.c
        state.countMode = v === "all" ? "all" : Number(v)
        openSetup(mode, { keep: true })
      }))
    }
    show("setup")
  }

  function renderQMap() {
    const meta = MODE_META[state.mode]
    const map = $("qMap")
    const canJump = !meta.noBack && state.mode !== "adaptive" && !meta.battle
    const total = state.mode === "adaptive"
      ? Math.max(state.questions.length, state.adaptiveTarget || state.questions.length)
      : state.questions.length

    if (meta.battle) {
      map.classList.add("hidden")
      return
    }
    map.classList.remove("hidden")

    let html = ""
    for (let i = 0; i < total; i++) {
      const exists = i < state.questions.length
      let cls = "q-dot"
      if (!exists) cls += " locked"
      else {
        if (state.answers[i] !== null) cls += " answered"
        if (state.flags[i]) cls += " flagged"
        if (i === state.index) cls += " current"
        if (!canJump) cls += " locked"
      }
      html += '<button type="button" class="' + cls + '" data-qi="' + i + '"' +
        ((!exists || !canJump) ? " disabled" : "") + ">" + (i + 1) + "</button>"
    }
    map.innerHTML = html
    map.querySelectorAll(".q-dot:not([disabled])").forEach((btn) => {
      btn.addEventListener("click", () => {
        state.index = Number(btn.dataset.qi)
        renderQuiz()
      })
    })
  }

  function renderQuiz() {
    const meta = MODE_META[state.mode]
    const i = state.index
    const q = state.questions[i]
    const total = state.mode === "adaptive" ? (state.adaptiveTarget || state.questions.length) : state.questions.length
    const flaggedCount = state.flags.filter(Boolean).length
    $("progressText").textContent = (i + 1) + " از " + total
    $("progressBar").style.width = (((i + 1) / total) * 100) + "%"
    $("qNum").textContent = "سوال " + (i + 1)
    $("modeChip").textContent = meta.title
    $("flagCountLabel").textContent = flaggedCount ? (flaggedCount + " نشان‌دار") : ""
    $("qText").textContent = q.text
    $("qMeta").innerHTML = '<span class="badge">' + (bank.topics[q.topic] || q.topic) + "</span>" +
      '<span class="badge">' + ({ easy: "آسان", medium: "متوسط", hard: "سخت" }[q.difficulty] || "") + "</span>"
    $("flagNote").classList.toggle("show", !!state.flags[i])
    renderQMap()

    if (state.duel.active) {
      $("duelBanner").classList.remove("hidden")
      $("duelBanner").textContent = "نوبت " + (state.duel.turn === 1 ? state.duel.p1 : state.duel.p2)
    } else $("duelBanner").classList.add("hidden")

    const canPrev = !meta.noBack && i > 0 && state.mode !== "adaptive"
    $("prevBtn").disabled = !canPrev
    $("prevBtn").style.visibility = meta.noBack || state.mode === "adaptive" ? "hidden" : "visible"
    $("flagBtn").style.visibility = meta.battle ? "hidden" : "visible"
    $("flagBtn").textContent = state.flags[i] ? "★ برداشتن نشان" : "☆ نشان‌گذاری"
    $("flagBtn").classList.toggle("on", !!state.flags[i])
    $("nextBtn").textContent = (i === total - 1) ? "پایان" : "بعدی"
    $("finishBtn").classList.toggle("hidden", meta.noBack || meta.battle || state.mode === "adaptive")

    const locked = state.locked[i]
    const box = $("options")
    box.innerHTML = q.options.map((opt, oi) => {
      let cls = "option"
      if (state.answers[i] === oi) cls += " selected"
      if (locked) {
        if (oi === q.correct) cls += " correct"
        else if (state.answers[i] === oi && oi !== q.correct) cls += " wrong"
      }
      return '<button type="button" class="' + cls + '" data-oi="' + oi + '"' + (locked ? " disabled" : "") + ">" +
        '<span class="mark">' + LABELS[oi] + "</span><span>" + opt + "</span></button>"
    }).join("")

    const fb = $("feedback")
    if (locked && state.feedbackOn) {
      const ok = state.answers[i] === q.correct
      fb.className = "feedback show " + (ok ? "ok" : "bad")
      fb.textContent = (ok ? "درست. " : "غلط. ") + q.explain
    } else {
      fb.className = "feedback"
      fb.textContent = ""
    }

    box.querySelectorAll(".option").forEach((btn) => {
      btn.addEventListener("click", () => {
        if (state.locked[i]) return
        const oi = Number(btn.dataset.oi)
        state.answers[i] = oi
        if (state.feedbackOn || state.mode === "adaptive") {
          state.locked[i] = true
          if (oi !== q.correct) addWrong(q)
          if (state.mode === "adaptive") {
            if (oi === q.correct) state.adaptiveLevel = Math.min(2, state.adaptiveLevel + 1)
            else state.adaptiveLevel = Math.max(0, state.adaptiveLevel - 1)
          }
        }
        if (meta.battle || meta.noBack) {
          renderQuiz()
          setTimeout(() => advanceOrFinish(), state.feedbackOn ? 700 : 180)
          return
        }
        renderQuiz()
      })
    })
  }

  function openAbortModal() {
    const answered = state.answers.filter((a) => a !== null).length
    const total = state.mode === "adaptive" ? (state.adaptiveTarget || state.questions.length) : state.questions.length
    $("abortMsg").textContent = "تا اینجا " + answered + " از " + total +
      " سوال پاسخ داده شده. با لغو، نتیجه ثبت نمی‌شود و به صفحه اصلی برمی‌گردید."
    $("abortModal").classList.remove("hidden")
  }

  function closeAbortModal() {
    $("abortModal").classList.add("hidden")
  }

  function abortQuiz() {
    stopTimer()
    closeAbortModal()
    state.questions = []
    state.answers = []
    state.flags = []
    state.duel.active = false
    state.duel.score1 = null
    state.duel.sharedQs = null
    show("home")
    renderProfile()
  }

  function advanceOrFinish() {
    if (state.mode === "adaptive") {
      const target = state.adaptiveTarget || 15
      if (state.questions.length >= target && state.index >= state.questions.length - 1) {
        finishQuiz(false)
        return
      }
      if (state.index >= state.questions.length - 1 && state.questions.length < target) {
        const used = new Set(state.questions.map((q) => q.uid))
        const next = pickNextAdaptive(used)
        if (!next) { finishQuiz(false); return }
        state.questions.push(next)
        state.answers.push(null)
        state.flags.push(false)
        state.locked.push(false)
        state.index++
        renderQuiz()
        return
      }
    }
    if (state.index < state.questions.length - 1) {
      state.index++
      renderQuiz()
    } else finishQuiz(false)
  }

  function grade() {
    let ok = 0, bad = 0, skip = 0
    const details = []
    state.questions.forEach((q, i) => {
      const ans = state.answers[i]
      let status = "skip"
      if (ans === null) skip++
      else if (ans === q.correct) { ok++; status = "ok" }
      else { bad++; status = "bad"; addWrong(q) }
      details.push({ q, i, ans, status })
    })
    const total = state.questions.length
    const pct = total ? Math.round((ok / total) * 100) : 0
    const elapsed = Date.now() - state.startedAt
    return { ok, bad, skip, total, pct, details, elapsed }
  }

  function applyXp(g) {
    const p = loadProfile()
    let gain = g.ok * 10
    if (state.mode === "battle") {
      const left = Math.max(0, state.endsAt - Date.now())
      gain += Math.round(left / 1000)
    }
    if (state.mode === "exam") gain += 15
    if (g.pct === 100) gain += 25
    p.xp += gain
    while (p.xp >= xpForLevel(p.level)) {
      p.xp -= xpForLevel(p.level)
      p.level += 1
    }
    const day = todayKey()
    if (p.lastDay !== day) {
      if (p.lastDay === yesterdayKey()) p.streak += 1
      else p.streak = 1
      p.lastDay = day
    }
    saveProfile(p)
    return gain
  }

  function finishQuiz(fromTimer) {
    stopTimer()
    const g = grade()
    state.lastGrade = g

    if (state.duel.active && state.duel.turn === 1) {
      state.duel.score1 = g
      state.duel.turn = 2
      alert("نوبت " + state.duel.p1 + " تمام شد (" + g.pct + "٪). حالا گوشی را به " + state.duel.p2 + " بدهید.")
      buildSession()
      show("quiz")
      startTimer()
      renderQuiz()
      return
    }

    let gain = applyXp(g)
    if (state.duel.score1) {
      gain += applyXp(state.duel.score1)
    }
    $("scorePct").textContent = g.pct + "٪"
    let sub = MODE_META[state.mode].title
    if (fromTimer) sub += " · زمان تمام شد"
    if (state.mode === "battle") sub += " · " + formatTime(g.elapsed) + " زمان صرف‌شده"
    $("scoreSub").textContent = sub
    $("xpGain").textContent = "+" + gain + " امتیاز"
    $("statOk").textContent = String(g.ok)
    $("statBad").textContent = String(g.bad)
    $("statSkip").textContent = String(g.skip)
    $("reviewBox").innerHTML = ""

    const cmp = $("duelCompare")
    if (state.duel.active && state.duel.score1) {
      const s1 = state.duel.score1
      const s2 = g
      let winner = "مساوی!"
      if (s1.pct > s2.pct) winner = "برنده: " + state.duel.p1
      else if (s2.pct > s1.pct) winner = "برنده: " + state.duel.p2
      cmp.classList.remove("hidden")
      cmp.innerHTML = '<div class="panel" style="margin:0;box-shadow:none"><strong>' + winner + "</strong><div style='margin-top:8px'>" +
        state.duel.p1 + ": " + s1.pct + "٪ (" + s1.ok + "/" + s1.total + ")<br>" +
        state.duel.p2 + ": " + s2.pct + "٪ (" + s2.ok + "/" + s2.total + ")</div></div>"
      state.duel.active = false
    } else cmp.classList.add("hidden")

    renderProfile()
    show("result")
  }

  function renderReview() {
    const g = state.lastGrade
    if (!g) return
    const items = g.details.filter((d) => d.status !== "ok")
    if (!items.length) {
      $("reviewBox").innerHTML = '<div class="hint">آفرین! اشتباه یا نزده‌ای نبود.</div>'
      return
    }
    $("reviewBox").innerHTML = items.map((d) => {
      const your = d.ans === null ? "—" : LABELS[d.ans] + ") " + d.q.options[d.ans]
      const right = LABELS[d.q.correct] + ") " + d.q.options[d.q.correct]
      return '<div class="review-item"><strong>سوال ' + (d.i + 1) + "</strong><div style='margin-top:6px'>" + d.q.text +
        "</div><div style='margin-top:8px;font-size:.9rem'><b>پاسخ شما:</b> " + your +
        "</div><div style='font-size:.9rem'><b>پاسخ درست:</b> " + right +
        "</div><div style='margin-top:6px;font-size:.86rem;color:var(--muted)'>" + d.q.explain + "</div></div>"
    }).join("")
  }

  function shareImage() {
    const g = state.lastGrade
    if (!g) return
    const p = loadProfile()
    const c = $("shareCanvas")
    const ctx = c.getContext("2d")
    const w = c.width, h = c.height
    const grd = ctx.createLinearGradient(0, 0, w, h)
    grd.addColorStop(0, "#0c4547")
    grd.addColorStop(1, "#187578")
    ctx.fillStyle = grd
    ctx.fillRect(0, 0, w, h)
    ctx.fillStyle = "rgba(255,255,255,.08)"
    ctx.beginPath(); ctx.arc(560, 120, 180, 0, Math.PI * 2); ctx.fill()
    ctx.fillStyle = "#fff"
    ctx.textAlign = "center"
    ctx.font = "700 42px Tahoma, sans-serif"
    ctx.fillText("SolidWorks Quiz", w / 2, 110)
    ctx.font = "400 28px Tahoma, sans-serif"
    ctx.fillStyle = "rgba(255,255,255,.85)"
    ctx.fillText(MODE_META[state.mode].title, w / 2, 160)
    ctx.fillStyle = "#fff"
    ctx.font = "800 120px Tahoma, sans-serif"
    ctx.fillText(g.pct + "%", w / 2, 340)
    ctx.font = "600 30px Tahoma, sans-serif"
    ctx.fillText(g.ok + " درست  ·  " + g.bad + " غلط  ·  " + g.skip + " نزده", w / 2, 420)
    ctx.font = "500 26px Tahoma, sans-serif"
    ctx.fillStyle = "rgba(255,255,255,.9)"
    ctx.fillText("سطح " + p.level + "  |  استریک " + p.streak + " روز", w / 2, 500)
    ctx.fillStyle = "rgba(255,255,255,.2)"
    ctx.fillRect(90, 560, w - 180, 2)
    ctx.fillStyle = "rgba(255,255,255,.75)"
    ctx.font = "400 24px Tahoma, sans-serif"
    ctx.fillText(new Date().toLocaleDateString("fa-IR"), w / 2, 620)
    ctx.fillText("تمرین آفلاین SolidWorks", w / 2, 670)

    c.toBlob(async (blob) => {
      if (!blob) return
      const file = new File([blob], "solidworks-quiz.png", { type: "image/png" })
      try {
        if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
          await navigator.share({ files: [file], title: "نتیجه آزمون SolidWorks" })
          return
        }
      } catch (e) {}
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = "solidworks-quiz.png"
      a.click()
      URL.revokeObjectURL(url)
    })
  }

  function openCards() {
    state.cards = loadWrongs()
    if (!state.cards.length) {
      alert("هنوز کارت غلطی ذخیره نشده. بعد از پاسخ غلط، اینجا پر می‌شود.")
      return
    }
    state.cardIndex = 0
    state.cardFlipped = false
    renderCard()
    show("cards")
  }

  function renderCard() {
    const card = state.cards[state.cardIndex]
    if (!card) { show("home"); renderProfile(); return }
    $("cardProgress").textContent = "کارت " + (state.cardIndex + 1) + " از " + state.cards.length + " — برای دیدن جواب روی کارت بزنید"
    $("flashSide").textContent = state.cardFlipped ? "پاسخ" : "سوال"
    if (state.cardFlipped) {
      $("flashBody").textContent = LABELS[card.correct] + ") " + card.options[card.correct] + "\n\n" + card.explain
    } else {
      $("flashBody").textContent = card.text
    }
  }

  // events
  document.querySelectorAll("[data-mode]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const mode = btn.dataset.mode
      if (mode === "cards") return openCards()
      if (mode === "topic") { renderTopics(); show("topics"); return }
      if (mode === "duel") {
        state.duel = { active: true, turn: 1, p1: "بازیکن ۱", p2: "بازیکن ۲", score1: null, sharedQs: null }
      } else {
        state.duel.active = false
      }
      state.topic = null
      openSetup(mode)
    })
  })

  document.querySelectorAll("[data-back]").forEach((btn) => {
    btn.addEventListener("click", () => { stopTimer(); show(btn.dataset.back); renderProfile() })
  })

  $("shuffleToggle").addEventListener("click", () => {
    state.shuffle = !state.shuffle
    $("shuffleToggle").classList.toggle("on", state.shuffle)
  })
  $("feedbackToggle").addEventListener("click", () => {
    state.feedbackOn = !state.feedbackOn
    $("feedbackToggle").classList.toggle("on", state.feedbackOn)
  })

  $("startBtn").addEventListener("click", () => {
    if (state.mode === "duel") {
      state.duel.active = true
      state.duel.turn = 1
      state.duel.p1 = ($("p1Name").value || "بازیکن ۱").trim()
      state.duel.p2 = ($("p2Name").value || "بازیکن ۲").trim()
      state.duel.score1 = null
    }
    buildSession()
    if (!state.questions.length) { alert("برای این موضوع سوالی پیدا نشد."); return }
    show("quiz")
    startTimer()
    renderQuiz()
  })

  $("prevBtn").addEventListener("click", () => {
    if (MODE_META[state.mode].noBack) return
    if (state.index > 0) { state.index--; renderQuiz() }
  })
  $("nextBtn").addEventListener("click", () => {
    if (state.mode === "adaptive") {
      if (!state.locked[state.index] && state.answers[state.index] === null) {
        alert("اول یک گزینه را انتخاب کنید.")
        return
      }
      if (!state.locked[state.index] && state.answers[state.index] !== null) {
        state.locked[state.index] = true
        const q = state.questions[state.index]
        const oi = state.answers[state.index]
        if (oi !== q.correct) addWrong(q)
        if (oi === q.correct) state.adaptiveLevel = Math.min(2, state.adaptiveLevel + 1)
        else state.adaptiveLevel = Math.max(0, state.adaptiveLevel - 1)
      }
      advanceOrFinish()
      return
    }
    if (state.index < state.questions.length - 1) { state.index++; renderQuiz() }
    else finishQuiz(false)
  })
  $("flagBtn").addEventListener("click", () => {
    state.flags[state.index] = !state.flags[state.index]
    renderQuiz()
  })
  $("abortBtn").addEventListener("click", openAbortModal)
  $("abortCancel").addEventListener("click", closeAbortModal)
  $("abortConfirm").addEventListener("click", abortQuiz)
  $("abortModal").addEventListener("click", (e) => {
    if (e.target.id === "abortModal") closeAbortModal()
  })
  $("finishBtn").addEventListener("click", () => {
    const blank = state.answers.filter((a) => a === null).length
    const flaggedBlank = state.questions.reduce((n, _q, i) => {
      return n + (state.flags[i] && state.answers[i] === null ? 1 : 0)
    }, 0)
    let msg = ""
    if (blank > 0) msg += blank + " سوال بدون پاسخ است. "
    if (flaggedBlank > 0) msg += flaggedBlank + " سوال نشان‌دار هنوز جواب داده نشده. "
    if (msg && !confirm(msg + "آزمون تمام و تصحیح شود؟")) return
    finishQuiz(false)
  })
  $("reviewWrongBtn").addEventListener("click", renderReview)
  $("shareBtn").addEventListener("click", shareImage)
  $("retryBtn").addEventListener("click", () => {
    if (state.mode === "duel") {
      state.duel.turn = 1
      state.duel.score1 = null
      state.duel.sharedQs = null
      state.duel.active = true
    }
    openSetup(state.mode)
  })
  $("homeBtn").addEventListener("click", () => { show("home"); renderProfile() })
  $("flashCard").addEventListener("click", () => { state.cardFlipped = !state.cardFlipped; renderCard() })
  $("cardNext").addEventListener("click", () => {
    state.cardIndex = (state.cardIndex + 1) % state.cards.length
    state.cardFlipped = false
    renderCard()
  })
  $("cardKnew").addEventListener("click", () => {
    const card = state.cards[state.cardIndex]
    if (!card) return
    removeWrong(card.uid)
    state.cards = loadWrongs()
    if (!state.cards.length) { alert("همه کارت‌ها مرور شد."); show("home"); renderProfile(); return }
    state.cardIndex = state.cardIndex % state.cards.length
    state.cardFlipped = false
    renderCard()
  })

  $("aboutBtn").addEventListener("click", () => show("about"))

  $("themeBtn").addEventListener("click", () => {
    const cur = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light"
    applyTheme(cur === "dark" ? "light" : "dark")
  })

  initTheme()
  renderProfile()
  show("home")
})()
</script>
</body>
</html>
'''

out = html.replace("__DATA__", "window.BANK = " + json.dumps(DATA, ensure_ascii=False) + ";")
(ROOT / "solidworks-quiz.html").write_text(out, encoding="utf-8")

(ROOT / "manifest.webmanifest").write_text(json.dumps({
  "name": "SolidWorks Quiz",
  "short_name": "SW Quiz",
  "start_url": "solidworks-quiz.html",
  "display": "standalone",
  "background_color": "#f4f8f7",
  "theme_color": "#0c4547",
  "lang": "fa",
  "dir": "rtl",
  "icons": [{"src": "icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable"}],
}, ensure_ascii=False, indent=2), encoding="utf-8")

icon = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="#0c4547"/><stop offset="100%" stop-color="#187578"/>
</linearGradient></defs>
<rect width="128" height="128" rx="28" fill="url(#g)"/>
<path d="M34 84 L34 44 L64 28 L94 44 L94 84 L64 100 Z" fill="none" stroke="#fff" stroke-width="5"/>
<circle cx="64" cy="64" r="10" fill="#b8611f"/>
</svg>'''
(ROOT / "icon.svg").write_text(icon, encoding="utf-8")
print("done", DATA["total"], "bytes", len(out.encode("utf-8")))
print("wrote solidworks-quiz.html")
