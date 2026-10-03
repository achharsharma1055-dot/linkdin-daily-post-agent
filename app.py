import os
import sys
import json
import random
import datetime
import requests
from pathlib import Path
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent

DEFAULT_API_KEY = "AQ.Ab8RN6Jutt5n2XU3lXNxEIUUrPb2-CHUwrEZOuc3eigG0JYLOQ"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", DEFAULT_API_KEY)

# 6 DYNAMIC COLOR THEMES
PALETTES = [
    {
        "id": "cyber-blue",
        "primary": "#38bdf8",
        "secondary": "#818cf8",
        "bg": "#060a16",
        "radial": "radial-gradient(circle at 15% 15%, rgba(56, 189, 248, 0.22) 0%, transparent 45%), radial-gradient(circle at 85% 85%, rgba(129, 140, 248, 0.22) 0%, transparent 45%)",
        "card_bg": "rgba(15, 23, 42, 0.75)",
        "accent_grad": "linear-gradient(135deg, #38bdf8, #818cf8)",
        "pill_bg": "rgba(56, 189, 248, 0.12)",
        "pill_border": "rgba(56, 189, 248, 0.4)"
    },
    {
        "id": "sunset-flame",
        "primary": "#fb923c",
        "secondary": "#f43f5e",
        "bg": "#140508",
        "radial": "radial-gradient(circle at 85% 15%, rgba(251, 146, 60, 0.24) 0%, transparent 45%), radial-gradient(circle at 15% 85%, rgba(244, 63, 94, 0.24) 0%, transparent 45%)",
        "card_bg": "rgba(30, 10, 16, 0.75)",
        "accent_grad": "linear-gradient(135deg, #fb923c, #f43f5e)",
        "pill_bg": "rgba(251, 146, 60, 0.12)",
        "pill_border": "rgba(251, 146, 60, 0.4)"
    },
    {
        "id": "emerald-matrix",
        "primary": "#34d399",
        "secondary": "#10b981",
        "bg": "#031209",
        "radial": "radial-gradient(circle at 20% 20%, rgba(52, 211, 153, 0.24) 0%, transparent 45%), radial-gradient(circle at 80% 80%, rgba(16, 185, 129, 0.24) 0%, transparent 45%)",
        "card_bg": "rgba(6, 28, 17, 0.75)",
        "accent_grad": "linear-gradient(135deg, #34d399, #059669)",
        "pill_bg": "rgba(52, 211, 153, 0.12)",
        "pill_border": "rgba(52, 211, 153, 0.4)"
    },
    {
        "id": "hyper-purple",
        "primary": "#c084fc",
        "secondary": "#7c3aed",
        "bg": "#0c0618",
        "radial": "radial-gradient(circle at 20% 20%, rgba(192, 132, 252, 0.24) 0%, transparent 45%), radial-gradient(circle at 80% 80%, rgba(124, 58, 237, 0.24) 0%, transparent 45%)",
        "card_bg": "rgba(25, 12, 48, 0.75)",
        "accent_grad": "linear-gradient(135deg, #c084fc, #7c3aed)",
        "pill_bg": "rgba(192, 132, 252, 0.12)",
        "pill_border": "rgba(192, 132, 252, 0.4)"
    },
    {
        "id": "luxury-gold",
        "primary": "#facc15",
        "secondary": "#ca8a04",
        "bg": "#120e03",
        "radial": "radial-gradient(circle at 20% 20%, rgba(250, 204, 21, 0.22) 0%, transparent 45%), radial-gradient(circle at 80% 80%, rgba(202, 138, 4, 0.22) 0%, transparent 45%)",
        "card_bg": "rgba(35, 28, 8, 0.75)",
        "accent_grad": "linear-gradient(135deg, #facc15, #ca8a04)",
        "pill_bg": "rgba(250, 204, 21, 0.12)",
        "pill_border": "rgba(250, 204, 21, 0.4)"
    }
]

# RICH DIVERSE POST BANK WITH VARIED STRUCTURES & CONTENT
POST_ARCHIVE = [
    {
        "structure": "serp_stack",
        "badge": "TECHNICAL AUDIT • SEARCH BOT",
        "stat_pill": "📊 +84% Crawl Efficiency",
        "search_mockup": "google crawl budget optimization 2026",
        "serp_tag": "#1 TOP RANK",
        "title_main": "Google Ranking <span class='hl'>Kyu Drop Hui?</span>",
        "subtitle": "Search Console me sudden indexing drop hone par ye 3 checkpoints audit karo:",
        "cards": [
            {
                "tag": "CRAWL LEAK", "num": "01",
                "icon": """<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><path d="m10 15 5-3-5-3v6z"/></svg>""",
                "title": "Orphan URLs & Parameter Waste",
                "desc": "Junk URL filters aur e-commerce sorting parameters Googlebot ka daily crawl budget drain kar dete hain."
            },
            {
                "tag": "INTENT CONFLICT", "num": "02",
                "icon": """<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>""",
                "title": "Internal Keyword Cannibalization",
                "desc": "Aapke 2 alag blog posts ek hi primary keyword target karte hain — Google dono ki ranking gira deta hai."
            },
            {
                "tag": "CORE SPEED", "num": "03",
                "icon": """<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>""",
                "title": "INP & Server Response Spikes",
                "desc": "Heavy JavaScript execution aur slow TTFB response mobile interaction score 50ms se kharab kar deta hai."
            }
        ],
        "golden_rule": "Traffic drop hone par naya post mat likho, pehle search intent aur internal linking audit karo!",
        "caption": """🚨 Google Search Console me traffic sudden drop ho gaya? Don't panic!

Har traffic drop Google Penalty nahi hota. 90% websites me ye 3 technical leaks hote hain:

1️⃣ Crawl Budget Waste:
GSC me 'Discovered - Currently Not Indexed' URLs check karo. Agar useless filter URLs crawl ho rahe hain, to priority pages drop ho jaate hain.

2️⃣ Keyword Cannibalization:
Do alag articles agar same search intent serve kar rahe hain, to unhe merge karke ek master guide banao with 301 redirect.

3️⃣ Core Web Vitals (INP Score):
March Core Update ke baad mobile user interaction delay par direct ranking hit milta hai.

👉 Quick Action Step:
GSC Performance tab me Last 28 Days compare karo aur exact drop wale URLs identify karo.

Kya aapne recently search fluctuations face kiya? Comment me discuss karte hain! 💬

#SEO #TechnicalSEO #GoogleAlgorithm #SearchConsole #CoreWebVitals #DigitalGrowth"""
    },
    {
        "structure": "matrix_grid",
        "badge": "🔥 SGE & AI SEARCH MATRIX",
        "stat_pill": "⚡ 3.4x Higher Citation CTR",
        "alert_ribbon": "CRITICAL AI ALGORITHM SHIFT",
        "title_main": "Google AI Overviews <span class='hl'>Se Traffic Bachao!</span>",
        "subtitle": "Zero-click searches ke dauran website par targeted organic traffic laane ke 4 pillars:",
        "grid_cards": [
            {
                "tag": "PILLAR 1",
                "icon": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>""",
                "title": "First-Party Data Proof",
                "desc": "Original surveys, live test results aur screenshots share karo jo AI kabhi khud invent na kar sake."
            },
            {
                "tag": "PILLAR 2",
                "icon": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>""",
                "title": "Inverted Pyramid Hook",
                "desc": "Intro paragraph me direct 35-word crisp answer do — Google AI wahi se primary definition quote karta hai."
            },
            {
                "tag": "PILLAR 3",
                "icon": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>""",
                "title": "Structured HTML Tables",
                "desc": "Comparison tables aur FAQ schema add karo. AI algorithms tables ko fastest parse karte hain."
            },
            {
                "tag": "PILLAR 4",
                "icon": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 4.24 4.24M14.83 9.17l4.24-4.24M14.83 14.83l4.24 4.24M9.17 14.83l-4.24 4.24"/></svg>""",
                "title": "High-Intent Funnel",
                "desc": "Generic informational keywords ke bajaye decision-making aur commercial queries target karo."
            }
        ],
        "golden_rule": "AI summary ka rival mat bano, uska verified clickable source bano!",
        "caption": """Kya Google AI Overviews aapke website traffic ko kha raha hai? 🤖📉

Zero-click searches badh rahe hain, lekin iska matlab SEO dead nahi hai — game evolve ho gaya hai!

Top source banne ke 4 Pillars:

✅ 1. Share Real Human Experience (E-E-A-T):
Screenshots, live client results, personal mistakes share karo. AI experience invent nahi kar sakta.

✅ 2. Inverted Pyramid Structure:
H2 ke turant baad direct crisp answer do. AI wahi se context pull karta hai!

✅ 3. Use Comparison Tables:
HTML tables use karo with clear metrics. AI comparison tables ko sabse high relevance score deta hai.

✅ 4. Target Decision Intent:
Complex troubleshooting aur high-intent commercial keywords target karo.

Aapke analytics me AI search ka koi impact dikha abhi tak? Share your experience! 👇

#AISEO #GoogleSearch #AIOverwiews #DigitalMarketing #FutureOfSEO #ContentCreators"""
    }
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>LinkedIn SEO Studio • 100% Mobile Friendly</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600;700;800&display=swap" rel="stylesheet">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
  <style>
    :root {
      --bg: #030712;
      --card-bg: rgba(15, 23, 42, 0.9);
      --border: rgba(255, 255, 255, 0.1);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }

    html, body {
      width: 100%;
      overflow-x: hidden;
      background-color: var(--bg);
      background-image: 
        radial-gradient(circle at 10% 10%, rgba(56, 189, 248, 0.1) 0%, transparent 45%),
        radial-gradient(circle at 90% 90%, rgba(244, 63, 94, 0.1) 0%, transparent 45%);
      font-family: 'Plus Jakarta Sans', sans-serif;
      color: var(--text-main);
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }

    .container {
      width: 100%;
      max-width: 1250px;
      margin: 0 auto;
      padding: 16px 12px;
    }

    /* HEADER */
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      padding-bottom: 18px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 20px;
    }

    .brand { display: flex; align-items: center; gap: 12px; }

    .logo-vector {
      width: 42px;
      height: 42px;
      border-radius: 12px;
      background: linear-gradient(135deg, #38bdf8, #f43f5e);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
      font-size: 18px;
      color: #030712;
      flex-shrink: 0;
    }

    .title-group h1 { font-size: 20px; font-weight: 900; letter-spacing: -0.02em; }
    .title-group p { color: var(--text-muted); font-size: 12px; }

    /* GENERATOR HUB */
    .generator-hub {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(56, 189, 248, 0.25);
      border-radius: 16px;
      padding: 16px;
      margin-bottom: 25px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    @media (min-width: 600px) {
      .generator-hub {
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
      }
    }

    .hub-info h3 { font-size: 16px; font-weight: 800; color: #38bdf8; margin-bottom: 4px; }
    .hub-info p { font-size: 12px; color: var(--text-muted); }

    .btn-generate-fresh {
      background: linear-gradient(135deg, #0284c7 0%, #7c3aed 50%, #f43f5e 100%);
      background-size: 200% 200%;
      animation: grad 4s ease infinite;
      color: #fff;
      font-weight: 800;
      font-size: 14px;
      padding: 12px 20px;
      border-radius: 12px;
      border: none;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 4px 20px rgba(2, 132, 199, 0.45);
      width: 100%;
    }

    @media (min-width: 600px) {
      .btn-generate-fresh { width: auto; }
    }

    @keyframes grad {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }

    /* POSTS GRID */
    .posts-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 25px;
      margin-bottom: 40px;
      width: 100%;
    }

    @media (min-width: 900px) {
      .posts-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 30px;
      }
    }

    .post-panel {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      width: 100%;
      overflow: hidden;
    }

    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }

    .panel-tag {
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      padding: 5px 12px;
      border-radius: 6px;
    }

    /* ========================================================
       PERFECT RESPONSIVE CONTAINER (100% MOBILE SCREEN FIT)
       ======================================================== */
    .render-wrapper {
      width: 100%;
      border-radius: 14px;
      overflow: hidden;
      border: 1px solid var(--border);
      position: relative;
      background: #000;
      aspect-ratio: 1080 / 1350; /* Exact 4:5 LinkedIn portrait ratio */
    }

    /* Fixed 1080x1350 canvas that scales down inside wrapper smoothly */
    .canvas-artboard {
      width: 1080px;
      height: 1350px;
      padding: 65px 55px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: absolute;
      top: 0;
      left: 0;
      overflow: hidden;
      transform-origin: top left;
      font-family: 'Plus Jakarta Sans', sans-serif;
      color: #fff;
    }

    .mesh-grid {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background-size: 40px 40px;
      background-image: linear-gradient(to right, rgba(255, 255, 255, 0.035) 1px, transparent 1px),
                        linear-gradient(to bottom, rgba(255, 255, 255, 0.035) 1px, transparent 1px);
      pointer-events: none;
    }

    .hl {
      background: linear-gradient(135deg, var(--p-col, #38bdf8), var(--s-col, #818cf8));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    /* SEARCH BAR UI */
    .search-bar-ui {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.16);
      border-radius: 18px;
      padding: 16px 22px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 15px;
      margin: 20px 0;
    }

    .stack-card {
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 22px 24px;
      display: flex;
      align-items: flex-start;
      gap: 18px;
      position: relative;
      overflow: hidden;
      margin-bottom: 16px;
    }

    /* 2x2 MATRIX GRID */
    .matrix-grid-container {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
      margin-bottom: 20px;
    }

    .matrix-grid-card {
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 20px;
      padding: 24px 22px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      position: relative;
      overflow: hidden;
    }

    .golden-banner {
      border-radius: 18px;
      padding: 20px 24px;
      display: flex;
      align-items: center;
      gap: 18px;
      position: relative;
      z-index: 1;
    }

    .caption-box {
      background: rgba(0, 0, 0, 0.45);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px;
      font-size: 13px;
      line-height: 1.6;
      color: #e2e8f0;
      max-height: 200px;
      overflow-y: auto;
      white-space: pre-wrap;
      width: 100%;
    }

    .actions-row {
      display: flex;
      gap: 10px;
      flex-direction: column;
      width: 100%;
    }

    @media (min-width: 480px) {
      .actions-row {
        flex-direction: row;
      }
    }

    .btn {
      flex: 1;
      padding: 12px 16px;
      border-radius: 10px;
      font-weight: 700;
      font-size: 13px;
      cursor: pointer;
      text-align: center;
      border: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      width: 100%;
    }

    .btn-copy { background: rgba(255, 255, 255, 0.08); color: #f8fafc; border: 1px solid rgba(255, 255, 255, 0.15); }
    .btn-dl { background: linear-gradient(135deg, #0284c7, #2563eb); color: #fff; }
    .toast-active { background: #10b981 !important; color: #fff !important; }
  </style>
</head>
<body>
  <div class="container">
    <!-- Top Header -->
    <div class="header">
      <div class="brand">
        <div class="logo-vector">⚡</div>
        <div class="title-group">
          <h1>Achhar Sharma • SEO Studio</h1>
          <p>100% Mobile Responsive • 4K Vector Export</p>
        </div>
      </div>
      <div style="font-size: 12px; color: #34d399; font-weight: 700; display: flex; align-items: center; gap: 6px;">
        <span style="width: 8px; height: 8px; border-radius: 50%; background: #34d399;"></span>
        24/7 Cloud Active
      </div>
    </div>

    <!-- NEW GENERATE FRESH POST BUTTON HUB -->
    <div class="generator-hub">
      <div class="hub-info">
        <h3>✨ On-Demand Post & Color-Structure Generator</h3>
        <p>Har click par Naya Topic, Naya Color Theme aur Naya Post Structure aayega!</p>
      </div>
      <button class="btn-generate-fresh" onclick="generateNewBatch()" id="genBtn">
        🎲 Generate Fresh Topics & New Colors Now
      </button>
    </div>

    <!-- POSTS GRID -->
    <div class="posts-grid">
      {% for p in posts %}
      <div class="post-panel">
        <div class="panel-header">
          <div class="panel-tag" style="background: {{ p.theme.pill_bg }}; color: {{ p.theme.primary }}; border: 1px solid {{ p.theme.pill_border }};">
            POST {{ p.id }}: {{ p.theme.id | upper }}
          </div>
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--text-muted);">1080x1350 4K</div>
        </div>

        <!-- RESPONSIVE 100% FIT WRAPPER -->
        <div class="render-wrapper" id="wrapper-{{ p.id }}">
          <div class="canvas-artboard" id="canvas-{{ p.id }}" style="
            background-color: {{ p.theme.bg }};
            background-image: {{ p.theme.radial }};
            --p-col: {{ p.theme.primary }};
            --s-col: {{ p.theme.secondary }};
          ">
            <div class="mesh-grid"></div>

            <!-- Header Row -->
            <div style="display: flex; justify-content: space-between; align-items: center; position: relative; z-index: 1;">
              <div style="display: inline-flex; align-items: center; gap: 10px; padding: 10px 22px; border-radius: 999px; background: {{ p.theme.pill_bg }}; border: 1px solid {{ p.theme.pill_border }}; color: {{ p.theme.primary }}; font-size: 15px; font-weight: 800; text-transform: uppercase;">
                <span style="width: 9px; height: 9px; border-radius: 50%; background: {{ p.theme.primary }}; box-shadow: 0 0 10px {{ p.theme.primary }};"></span>
                <span>{{ p.data.badge }}</span>
              </div>
              <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 12px; padding: 9px 20px; font-family: 'JetBrains Mono', monospace; font-size: 16px; font-weight: 700; color: {{ p.theme.primary }};">
                {{ p.data.stat_pill }}
              </div>
            </div>

            {% if p.data.structure == 'serp_stack' %}
            <!-- STRUCTURE A: SEARCH BAR UI -->
            <div class="search-bar-ui" style="position: relative; z-index: 1;">
              <div style="display: flex; align-items: center; gap: 14px;">
                <svg width="26" height="26" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 17px; color: #e2e8f0; font-weight: 600;">{{ p.data.search_mockup }}</div>
              </div>
              <div style="background: {{ p.theme.primary }}; color: #000; font-size: 13px; font-weight: 800; padding: 6px 14px; border-radius: 8px;">{{ p.data.serp_tag }}</div>
            </div>
            {% else %}
            <!-- STRUCTURE B: ALERT RIBBON -->
            <div style="background: {{ p.theme.pill_bg }}; border: 1px solid {{ p.theme.pill_border }}; border-radius: 16px; padding: 14px 22px; display: flex; align-items: center; justify-content: space-between; margin: 20px 0; position: relative; z-index: 1;">
              <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 20px;">🚨</span>
                <span style="font-size: 16px; font-weight: 800; color: #f8fafc;">{{ p.data.alert_ribbon }}</span>
              </div>
              <div style="background: {{ p.theme.primary }}; color: #000; font-size: 12px; font-weight: 800; padding: 5px 12px; border-radius: 6px;">MUST KNOW</div>
            </div>
            {% endif %}

            <!-- Title -->
            <div style="position: relative; z-index: 1;">
              <h1 style="font-size: 52px; font-weight: 900; line-height: 1.15; letter-spacing: -0.03em; margin-bottom: 12px;">{{ p.data.title_main | safe }}</h1>
              <p style="font-size: 21px; line-height: 1.5; color: #cbd5e1;">{{ p.data.subtitle }}</p>
            </div>

            {% if p.data.structure == 'serp_stack' %}
            <!-- CARDS: STACK -->
            <div style="display: flex; flex-direction: column; gap: 16px; margin-bottom: 20px; position: relative; z-index: 1;">
              {% for c in p.data.cards %}
              <div class="stack-card" style="background: {{ p.theme.card_bg }};">
                <div style="position: absolute; left: 0; top: 0; width: 5px; height: 100%; background: {{ p.theme.primary }};"></div>
                <div style="width: 50px; height: 50px; border-radius: 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); display: flex; align-items: center; justify-content: center; flex-shrink: 0; color: {{ p.theme.primary }};">
                  {{ c.icon | safe }}
                </div>
                <div style="flex: 1;">
                  <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 800; color: {{ p.theme.primary }};">{{ c.tag }}</span>
                    <span style="color: rgba(255,255,255,0.2);">•</span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 13px; color: var(--text-muted);">STEP {{ c.num }}</span>
                  </div>
                  <div style="font-size: 22px; font-weight: 800; color: #f8fafc; margin-bottom: 6px;">{{ c.title }}</div>
                  <div style="font-size: 17px; line-height: 1.45; color: #94a3b8;">{{ c.desc }}</div>
                </div>
              </div>
              {% endfor %}
            </div>
            {% else %}
            <!-- CARDS: 2x2 MATRIX -->
            <div class="matrix-grid-container" style="position: relative; z-index: 1;">
              {% for card in p.data.grid_cards %}
              <div class="matrix-grid-card" style="background: {{ p.theme.card_bg }};">
                <div style="position: absolute; left: 0; top: 0; width: 4px; height: 100%; background: {{ p.theme.primary }};"></div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                  <div style="width: 48px; height: 48px; border-radius: 14px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.14); display: flex; align-items: center; justify-content: center; color: {{ p.theme.primary }};">
                    {{ card.icon | safe }}
                  </div>
                  <span style="font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 800; color: {{ p.theme.primary }};">{{ card.tag }}</span>
                </div>
                <div style="font-size: 22px; font-weight: 800; color: #fff;">{{ card.title }}</div>
                <div style="font-size: 16px; line-height: 1.45; color: #cbd5e1;">{{ card.desc }}</div>
              </div>
              {% endfor %}
            </div>
            {% endif %}

            <!-- Golden Banner -->
            <div class="golden-banner" style="background: rgba(15, 23, 42, 0.9); border: 1px solid {{ p.theme.pill_border }}; box-shadow: 0 0 30px {{ p.theme.pill_bg }};">
              <div style="background: {{ p.theme.accent_grad }}; color: #fff; font-size: 14px; font-weight: 800; padding: 8px 16px; border-radius: 10px; text-transform: uppercase;">Master Rule</div>
              <div style="font-size: 19px; font-weight: 600; color: #e2e8f0; line-height: 1.4;">"{{ p.data.golden_rule }}"</div>
            </div>

            <!-- Footer -->
            <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 24px; border-top: 1px solid rgba(255, 255, 255, 0.08); position: relative; z-index: 1;">
              <div style="display: flex; align-items: center; gap: 14px;">
                <div style="width: 46px; height: 46px; border-radius: 50%; background: {{ p.theme.accent_grad }}; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 18px; color: #030712;">AS</div>
                <div>
                  <div style="font-size: 19px; font-weight: 800; color: #f8fafc;">Achhar Sharma</div>
                  <div style="font-size: 14px; color: #64748b;">Daily SEO Growth in Hinglish</div>
                </div>
              </div>
              <div style="font-size: 16px; color: {{ p.theme.primary }}; font-weight: 700;">Save for later 📌</div>
            </div>

          </div>
        </div>

        <div class="caption-box" id="caption-{{ p.id }}">{{ p.data.caption }}</div>

        <div class="actions-row">
          <button class="btn btn-copy" onclick="copyCaption('caption-{{ p.id }}', this)">📋 Copy Caption</button>
          <button class="btn btn-dl" style="background: {{ p.theme.accent_grad }};" onclick="downloadImage('canvas-{{ p.id }}', 'seo_post_{{ p.id }}_{{ p.theme.id }}.png', this)">💾 Download 4K Graphic</button>
        </div>
      </div>
      {% endfor %}
    </div>

  </div>

  <script>
    // 100% Precision Auto-Scaler for Mobile, Tablet & Desktop
    function rescaleCanvas() {
      [1, 2].forEach(id => {
        const wrapper = document.getElementById('wrapper-' + id);
        const canvas = document.getElementById('canvas-' + id);
        if (wrapper && canvas) {
          const wrapperWidth = wrapper.getBoundingClientRect().width;
          const scale = wrapperWidth / 1080;
          canvas.style.transform = `scale(${scale})`;
          wrapper.style.height = (1350 * scale) + 'px';
        }
      });
    }

    window.addEventListener('resize', rescaleCanvas);
    window.addEventListener('orientationchange', rescaleCanvas);
    document.addEventListener('DOMContentLoaded', rescaleCanvas);
    setTimeout(rescaleCanvas, 300);

    function copyCaption(id, btn) {
      const text = document.getElementById(id).innerText;
      navigator.clipboard.writeText(text).then(() => {
        const originalText = btn.innerHTML;
        btn.innerHTML = "✅ Copied to Clipboard!";
        btn.classList.add('toast-active');
        setTimeout(() => {
          btn.innerHTML = originalText;
          btn.classList.remove('toast-active');
        }, 2000);
      });
    }

    function generateNewBatch() {
      const btn = document.getElementById('genBtn');
      btn.innerHTML = "⏳ Shuffling Colors, Structure & AI Topics...";
      btn.disabled = true;

      fetch('/api/shuffle', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
          if (data.status === 'ok') {
            window.location.reload();
          } else {
            alert('Error generating');
            btn.innerHTML = "🎲 Generate Fresh Topics & New Colors Now";
            btn.disabled = false;
          }
        })
        .catch(err => {
          window.location.reload();
        });
    }

    function downloadImage(canvasId, fileName, btn) {
      const canvas = document.getElementById(canvasId);
      const originalTransform = canvas.style.transform;
      const originalText = btn.innerHTML;
      btn.innerHTML = "⏳ Exporting 4K...";
      btn.disabled = true;

      canvas.style.transform = 'none';

      html2canvas(canvas, {
        width: 1080,
        height: 1350,
        scale: 2,
        useCORS: true,
        backgroundColor: null
      }).then(resCanvas => {
        canvas.style.transform = originalTransform;
        btn.innerHTML = originalText;
        btn.disabled = false;

        const link = document.createElement('a');
        link.download = fileName;
        link.href = resCanvas.toDataURL('image/png');
        link.click();
      }).catch(err => {
        canvas.style.transform = originalTransform;
        btn.innerHTML = originalText;
        btn.disabled = false;
        alert('Export error, please try again.');
      });
    }
  </script>
</body>
</html>
"""

STATE_FILE = BASE_DIR / "state.json"

def get_current_state():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"offset": 0}

def save_current_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

@app.route("/")
def index():
    state = get_current_state()
    offset = state.get("offset", 0)

    t1_idx = offset % len(POST_ARCHIVE)
    t2_idx = (offset + 1) % len(POST_ARCHIVE)

    p1_col = PALETTES[offset % len(PALETTES)]
    p2_col = PALETTES[(offset + 2) % len(PALETTES)]

    posts = [
        {"id": 1, "theme": p1_col, "data": POST_ARCHIVE[t1_idx]},
        {"id": 2, "theme": p2_col, "data": POST_ARCHIVE[t2_idx]}
    ]
    return render_template_string(HTML_TEMPLATE, posts=posts)

@app.route("/api/shuffle", methods=["POST"])
def api_shuffle():
    state = get_current_state()
    state["offset"] = (state.get("offset", 0) + 2) % 100
    save_current_state(state)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
