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

# 12 DISTINCT HIGH-END COLOR PALETTES
PALETTES = [
    {"id": "cyan", "name": "Cyber Neon", "p": "#00f2fe", "s": "#38bdf8", "bg": "#060a14", "radial": "radial-gradient(circle at 15% 15%, rgba(0,242,254,0.25) 0%, transparent 45%), radial-gradient(circle at 85% 85%, rgba(56,189,248,0.2) 0%, transparent 45%)", "card_bg": "rgba(10,20,38,0.85)", "pill_bg": "rgba(0,242,254,0.12)", "border": "rgba(0,242,254,0.4)"},
    {"id": "flame", "name": "Sunset Fire", "p": "#fb923c", "s": "#f43f5e", "bg": "#140508", "radial": "radial-gradient(circle at 85% 15%, rgba(251,146,60,0.25) 0%, transparent 45%), radial-gradient(circle at 15% 85%, rgba(244,63,94,0.25) 0%, transparent 45%)", "card_bg": "rgba(35,12,18,0.85)", "pill_bg": "rgba(251,146,60,0.12)", "border": "rgba(251,146,60,0.4)"},
    {"id": "emerald", "name": "Matrix Jade", "p": "#34d399", "s": "#10b981", "bg": "#031209", "radial": "radial-gradient(circle at 20% 20%, rgba(52,211,153,0.25) 0%, transparent 45%), radial-gradient(circle at 80% 80%, rgba(16,185,129,0.2) 0%, transparent 45%)", "card_bg": "rgba(6,28,17,0.85)", "pill_bg": "rgba(52,211,153,0.12)", "border": "rgba(52,211,153,0.4)"},
    {"id": "purple", "name": "Hyper Violet", "p": "#c084fc", "s": "#7c3aed", "bg": "#0c0618", "radial": "radial-gradient(circle at 20% 20%, rgba(192,132,252,0.25) 0%, transparent 45%), radial-gradient(circle at 80% 80%, rgba(124,58,237,0.25) 0%, transparent 45%)", "card_bg": "rgba(26,12,48,0.85)", "pill_bg": "rgba(192,132,252,0.12)", "border": "rgba(192,132,252,0.4)"},
    {"id": "gold", "name": "Royal Gold", "p": "#facc15", "s": "#ca8a04", "bg": "#120e03", "radial": "radial-gradient(circle at 20% 20%, rgba(250,204,21,0.25) 0%, transparent 45%), radial-gradient(circle at 80% 80%, rgba(202,138,4,0.2) 0%, transparent 45%)", "card_bg": "rgba(36,28,8,0.85)", "pill_bg": "rgba(250,204,21,0.12)", "border": "rgba(250,204,21,0.4)"},
    {"id": "ruby", "name": "Blood Ruby", "p": "#fb7185", "s": "#e11d48", "bg": "#140407", "radial": "radial-gradient(circle at 80% 20%, rgba(251,113,133,0.25) 0%, transparent 45%), radial-gradient(circle at 20% 80%, rgba(225,29,72,0.25) 0%, transparent 45%)", "card_bg": "rgba(36,8,16,0.85)", "pill_bg": "rgba(251,113,133,0.12)", "border": "rgba(251,113,133,0.4)"},
    {"id": "sapphire", "name": "Deep Sapphire", "p": "#60a5fa", "s": "#2563eb", "bg": "#040916", "radial": "radial-gradient(circle at 15% 15%, rgba(96,165,250,0.25) 0%, transparent 45%), radial-gradient(circle at 85% 85%, rgba(37,99,235,0.2) 0%, transparent 45%)", "card_bg": "rgba(10,24,48,0.85)", "pill_bg": "rgba(96,165,250,0.12)", "border": "rgba(96,165,250,0.4)"},
    {"id": "lime", "name": "Electric Acid", "p": "#a3e635", "s": "#65a30d", "bg": "#081004", "radial": "radial-gradient(circle at 85% 15%, rgba(163,230,53,0.25) 0%, transparent 45%), radial-gradient(circle at 15% 85%, rgba(101,163,13,0.2) 0%, transparent 45%)", "card_bg": "rgba(18,28,8,0.85)", "pill_bg": "rgba(163,230,53,0.12)", "border": "rgba(163,230,53,0.4)"}
]

# 8 DIVERSE POST FORMATS & STRUCTURES (No two posts look the same!)
POST_STRUCTURE_DATABASE = [
    # STRUCTURE 1: THE BIG TYPOGRAPHY + 1 GIANT HERO STAT CARD
    {
        "layout": "hero_giant",
        "badge": "🚨 GOOGLE ALGORITHM SHIFT",
        "stat": "+84% CRAWL RATE",
        "title": "Search Console Me <span class='hl'>Indexing Zero?</span>",
        "subtitle": "90% creators panic me article delete karte hain, par asal galti ye single issue hoti hai:",
        "hero_card": {
            "tag": "CRITICAL BOTTLENECK",
            "val": "Orphan URLs & Filter Parameters",
            "desc": "Robots.txt check karo — hazaron sorting parameters Googlebot ka daily crawl budget drain kar dete hain, aur main pages unindexed reh jaate hain."
        },
        "points": [
            {"title": "Canonical Tag Missing", "desc": "Duplicate filter pages ko direct canonicalize karo."},
            {"title": "Internal Link Depth > 3", "desc": "Important pages tak pahuchne ke liye 3+ clicks lag rahe hain."}
        ],
        "golden_rule": "Traffic drop hone par naya article mat likho, pehle internal links audit karo!",
        "caption": """🚨 Search Console me 'Discovered - Currently Not Indexed' URLs badh rahe hain?

90% cases me content kharab nahi hota, crawl budget drain ho raha hota hai!

1️⃣ Filter URLs Trap:
E-commerce ya blog search filters hazaron useless URLs banate hain jo crawl limit kha jaate hain.

2️⃣ Orphan Pages:
Agar kisi page ko site me kahi se internal link nahi mila, to Googlebot use de-prioritize kar deta hai.

Fix: GSC > Performance tab me compare last 28 days! 💬

#SEO #TechnicalSEO #GoogleAlgorithm #SearchConsole #WebPerformance"""
    },

    # STRUCTURE 2: 2x2 SPLIT MATRIX QUADRANT (4 High-Impact Pillars)
    {
        "layout": "matrix_4",
        "badge": "⚡ SGE & AI SEARCH MATRIX",
        "stat": "3.4x CITATION CTR",
        "title": "Google AI Overviews Se <span class='hl'>Traffic Bachao!</span>",
        "subtitle": "Zero-click searches ke dauran website par targeted organic traffic laane ke 4 pillars:",
        "matrix": [
            {"num": "01", "tag": "FIRST-PARTY DATA", "title": "Real Test Case Studies", "desc": "Original data aur screenshot proof do jo AI generate na kar sake."},
            {"num": "02", "tag": "INVERTED PYRAMID", "title": "Direct 35-Word Hook", "desc": "H2 ke turant baad crisp answer do — AI wahi se quote karta hai."},
            {"num": "03", "tag": "COMPARISON TABLES", "title": "Structured HTML Tables", "desc": "Comparison tables aur FAQ schema AI sabse fast parse karta hai."},
            {"num": "04", "tag": "HIGH INTENT FUNNEL", "title": "Decision Keywords", "desc": "Broad keywords chhod kar commercial decision queries target karo."}
        ],
        "golden_rule": "AI summary ka rival mat bano, uska verified source bano!",
        "caption": """AI Overviews organic clicks kha raha hai? Game evolve ho gaya hai! 🤖📉

Google AI summaries me top source banne ke 4 Pillars:
1. First-Party Experiment Data
2. Inverted Pyramid Direct Answers
3. HTML Comparison Tables
4. Bottom-Funnel Search Intent

Aapka traffic AI updates ke baad badha ya kam hua? Share in comments! 👇

#AISEO #GoogleSearch #AIOverwiews #DigitalMarketing #FutureOfSEO"""
    },

    # STRUCTURE 3: HORIZONTAL 3-STEP FLOW CARDS + SEARCH BAR UI
    {
        "layout": "search_steps",
        "badge": "🔍 SEARCH INTENT MASTERY",
        "stat": "0% BOUNCE RATE",
        "search_ui": "search intent vs keyword density 2026",
        "title": "Keyword Stuffing Chhodo, <span class='hl'>Search Intent Sikho!</span>",
        "subtitle": "2026 me Google keywords nahi, topic ka complete context aur satisfaction score dekhta hai:",
        "steps": [
            {"num": "STEP 1", "title": "Analyze Top 3 Competitor Formats", "desc": "Dekho Google kis format ko reward kar raha hai: Guide, Table ya Tool?"},
            {"num": "STEP 2", "title": "First 100 Words Direct Resolution", "desc": "User ke click karte hi seedhe point par aao bina background story ke."},
            {"num": "STEP 3", "title": "Cover PAA (People Also Ask) Queries", "desc": "Related sub-questions solve karo taaki Featured Snippets win ho sakein."}
        ],
        "golden_rule": "Users ke satisfaction ke liye likho, search algorithms apne aap reward karenge!",
        "caption": """Keywords rank karwa liye, par dwell time zero hai? ❌

Kyunki aapne keyword to pakad liya, par Search Intent match nahi kiya!

🔹 1. Identify Format: User ko comparison table chahiye ya direct tutorial?
🔹 2. Answer in Intro: Pehle 20 seconds me primary doubt clear karo.
🔹 3. Solve PAA Queries: Featured Snippet win karne ka shortcut!

#SearchIntent #OnPageSEO #ContentMarketing #DigitalStrategy #SEOExpert"""
    },

    # STRUCTURE 4: BEFORE vs AFTER SPLIT COMPARISON (Mistake vs Pro Strategy)
    {
        "layout": "split_compare",
        "badge": "⚠️ LINK BUILDING TRUTH",
        "stat": "10x DOMAIN AUTHORITY",
        "title": "Spam PBN Backlinks <span class='hl'>vs Digital PR Links</span>",
        "subtitle": "Google SpamBrain AI ab paid guest post patterns ko 1 second me detect kar leta hai:",
        "compare": [
            {
                "type": "MISTAKE (OLD 2018)",
                "color": "#ef4444",
                "points": ["₹500 me 1000 bulk Fiverr links", "Irrelevant niche websites se links", "Manipulated exact-match anchor text"]
            },
            {
                "type": "WINNING STRATEGY (2026)",
                "color": "#10b981",
                "points": ["Original data study aur industry surveys", "Free micro-utility tool (e.g. ROI Calculator)", "Editorial context brand mentions"]
            }
        ],
        "golden_rule": "1 relevant editorial link = 500 spam links. Quality always wins!",
        "caption": """Fiverr pe ₹500 me 1000 Backlinks khareed rahe ho? Stop it! ❌

2026 me Backlink strategy aisi honi chahiye:
- Relevancy > Domain Rating
- Digital PR Studies launch karo
- Micro tools banao jise log natural link karein

Quality always beats quantity! 🚀

#LinkBuilding #OffPageSEO #SEOStrategy #Backlinks #GrowthHacking"""
    }
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>LinkedIn Multi-Structure SEO Studio</title>
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
      padding-bottom: 16px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 20px;
    }

    .brand { display: flex; align-items: center; gap: 12px; }

    .logo-vector {
      width: 44px;
      height: 44px;
      border-radius: 12px;
      background: linear-gradient(135deg, #00f2fe, #f43f5e);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
      font-size: 20px;
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
      background: linear-gradient(135deg, #00f2fe 0%, #7c3aed 50%, #f43f5e 100%);
      background-size: 200% 200%;
      animation: grad 4s ease infinite;
      color: #fff;
      font-weight: 800;
      font-size: 14px;
      padding: 13px 22px;
      border-radius: 12px;
      border: none;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 4px 20px rgba(0, 242, 254, 0.45);
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

    /* 100% FULL MOBILE VISIBLE CONTAINER */
    .canvas-viewport-box {
      width: 100%;
      position: relative;
      border-radius: 14px;
      overflow: hidden;
      border: 1px solid var(--border);
      background: #000;
      /* Precise container height calculation for mobile */
    }

    /* 1080x1350 Canvas Artboard */
    .artboard {
      width: 1080px;
      height: 1350px;
      padding: 65px 55px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: absolute;
      top: 0;
      left: 0;
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
      background: linear-gradient(135deg, var(--p-col), var(--s-col));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    /* CAPTION BOX & ACTIONS */
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
    .btn-dl { color: #fff; }
    .toast-active { background: #10b981 !important; color: #fff !important; }
  </style>
</head>
<body>
  <div class="container">
    <!-- Header -->
    <div class="header">
      <div class="brand">
        <div class="logo-vector">⚡</div>
        <div class="title-group">
          <h1>Achhar Sharma • Multi-Structure Studio</h1>
          <p>100% Mobile Full Screen Fit • Different Shapes & Colors</p>
        </div>
      </div>
      <div style="font-size: 12px; color: #34d399; font-weight: 700; display: flex; align-items: center; gap: 6px;">
        <span style="width: 8px; height: 8px; border-radius: 50%; background: #34d399;"></span>
        24/7 Cloud Active
      </div>
    </div>

    <!-- GENERATOR BUTTON -->
    <div class="generator-hub">
      <div class="hub-info">
        <h3>🎲 Infinite Design & Topic Shuffler</h3>
        <p>Click karte hi Naya Topic, Naya Layout Structure aur Naya Color Palette aayega!</p>
      </div>
      <button class="btn-generate-fresh" onclick="generateNewBatch()" id="genBtn">
        ✨ Generate Completely Different Post & Colors
      </button>
    </div>

    <!-- POSTS GRID -->
    <div class="posts-grid">
      {% for p in posts %}
      <div class="post-panel">
        <div class="panel-header">
          <div class="panel-tag" style="background: {{ p.theme.pill_bg }}; color: {{ p.theme.p }}; border: 1px solid {{ p.theme.border }};">
            POST {{ p.id }}: {{ p.theme.name }} • {{ p.data.layout | upper }}
          </div>
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--text-muted);">1080x1350 4K</div>
        </div>

        <!-- 100% MOBILE VISIBLE VIEWPORT WRAPPER -->
        <div class="canvas-viewport-box" id="viewport-{{ p.id }}">
          <div class="artboard" id="artboard-{{ p.id }}" style="
            background-color: {{ p.theme.bg }};
            background-image: {{ p.theme.radial }};
            --p-col: {{ p.theme.p }};
            --s-col: {{ p.theme.s }};
          ">
            <div class="mesh-grid"></div>

            <!-- Top Header Row -->
            <div style="display: flex; justify-content: space-between; align-items: center; position: relative; z-index: 1;">
              <div style="display: inline-flex; align-items: center; gap: 10px; padding: 10px 22px; border-radius: 999px; background: {{ p.theme.pill_bg }}; border: 1px solid {{ p.theme.border }}; color: {{ p.theme.p }}; font-size: 15px; font-weight: 800; text-transform: uppercase;">
                <span style="width: 9px; height: 9px; border-radius: 50%; background: {{ p.theme.p }}; box-shadow: 0 0 10px {{ p.theme.p }};"></span>
                <span>{{ p.data.badge }}</span>
              </div>
              <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 12px; padding: 9px 20px; font-family: 'JetBrains Mono', monospace; font-size: 16px; font-weight: 700; color: {{ p.theme.p }};">
                {{ p.data.stat }}
              </div>
            </div>

            <!-- ==============================================
                 LAYOUT 1: HERO GIANT CARD
                 ============================================== -->
            {% if p.data.layout == 'hero_giant' %}
            <div style="position: relative; z-index: 1; margin: 15px 0;">
              <h1 style="font-size: 54px; font-weight: 900; line-height: 1.15; letter-spacing: -0.03em; margin-bottom: 12px;">{{ p.data.title | safe }}</h1>
              <p style="font-size: 21px; line-height: 1.5; color: #cbd5e1;">{{ p.data.subtitle }}</p>
            </div>

            <!-- Giant Hero Box -->
            <div style="background: {{ p.theme.card_bg }}; border: 1.5px solid {{ p.theme.border }}; border-radius: 24px; padding: 32px 30px; position: relative; z-index: 1; box-shadow: 0 15px 40px rgba(0,0,0,0.5);">
              <div style="display: inline-block; background: {{ p.theme.p }}; color: #000; font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 900; padding: 6px 14px; border-radius: 8px; margin-bottom: 14px;">{{ p.data.hero_card.tag }}</div>
              <div style="font-size: 28px; font-weight: 900; color: #fff; margin-bottom: 10px;">{{ p.data.hero_card.val }}</div>
              <div style="font-size: 18px; line-height: 1.5; color: #cbd5e1;">{{ p.data.hero_card.desc }}</div>
            </div>

            <!-- 2 Mini Bullets -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; position: relative; z-index: 1;">
              {% for pt in p.data.points %}
              <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 18px 20px;">
                <div style="font-size: 18px; font-weight: 800; color: {{ p.theme.p }}; margin-bottom: 6px;">{{ pt.title }}</div>
                <div style="font-size: 15px; color: #94a3b8; line-height: 1.4;">{{ pt.desc }}</div>
              </div>
              {% endfor %}
            </div>

            <!-- ==============================================
                 LAYOUT 2: 2x2 MATRIX QUADRANT
                 ============================================== -->
            {% elif p.data.layout == 'matrix_4' %}
            <div style="position: relative; z-index: 1; margin: 15px 0;">
              <h1 style="font-size: 52px; font-weight: 900; line-height: 1.15; letter-spacing: -0.03em; margin-bottom: 10px;">{{ p.data.title | safe }}</h1>
              <p style="font-size: 20px; line-height: 1.45; color: #cbd5e1;">{{ p.data.subtitle }}</p>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 18px; position: relative; z-index: 1;">
              {% for m in p.data.matrix %}
              <div style="background: {{ p.theme.card_bg }}; border: 1px solid rgba(255,255,255,0.12); border-radius: 20px; padding: 24px 22px; position: relative; overflow: hidden;">
                <div style="position: absolute; left: 0; top: 0; width: 4px; height: 100%; background: {{ p.theme.p }};"></div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 800; color: {{ p.theme.p }}; margin-bottom: 8px;">{{ m.tag }} • {{ m.num }}</div>
                <div style="font-size: 21px; font-weight: 800; color: #fff; margin-bottom: 8px;">{{ m.title }}</div>
                <div style="font-size: 15px; line-height: 1.45; color: #cbd5e1;">{{ m.desc }}</div>
              </div>
              {% endfor %}
            </div>

            <!-- ==============================================
                 LAYOUT 3: SEARCH BAR + STEP CARDS
                 ============================================== -->
            {% elif p.data.layout == 'search_steps' %}
            <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.16); border-radius: 18px; padding: 16px 22px; display: flex; align-items: center; justify-content: space-between; margin: 15px 0; position: relative; z-index: 1;">
              <div style="display: flex; align-items: center; gap: 14px;">
                <svg width="26" height="26" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 17px; color: #e2e8f0; font-weight: 600;">{{ p.data.search_ui }}</div>
              </div>
              <div style="background: {{ p.theme.p }}; color: #000; font-size: 13px; font-weight: 800; padding: 6px 14px; border-radius: 8px;">#1 VERIFIED</div>
            </div>

            <div style="position: relative; z-index: 1; margin-bottom: 15px;">
              <h1 style="font-size: 50px; font-weight: 900; line-height: 1.15; letter-spacing: -0.03em; margin-bottom: 10px;">{{ p.data.title | safe }}</h1>
              <p style="font-size: 20px; line-height: 1.45; color: #cbd5e1;">{{ p.data.subtitle }}</p>
            </div>

            <div style="display: flex; flex-direction: column; gap: 14px; position: relative; z-index: 1;">
              {% for s in p.data.steps %}
              <div style="background: {{ p.theme.card_bg }}; border: 1px solid rgba(255,255,255,0.1); border-radius: 18px; padding: 20px 22px; display: flex; align-items: flex-start; gap: 16px;">
                <div style="background: {{ p.theme.pill_bg }}; color: {{ p.theme.p }}; border: 1px solid {{ p.theme.border }}; font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 800; padding: 6px 12px; border-radius: 8px;">{{ s.num }}</div>
                <div>
                  <div style="font-size: 20px; font-weight: 800; color: #fff; margin-bottom: 4px;">{{ s.title }}</div>
                  <div style="font-size: 16px; color: #94a3b8; line-height: 1.4;">{{ s.desc }}</div>
                </div>
              </div>
              {% endfor %}
            </div>

            <!-- ==============================================
                 LAYOUT 4: BEFORE vs AFTER SPLIT COMPARISON
                 ============================================== -->
            {% elif p.data.layout == 'split_compare' %}
            <div style="position: relative; z-index: 1; margin: 15px 0;">
              <h1 style="font-size: 52px; font-weight: 900; line-height: 1.15; letter-spacing: -0.03em; margin-bottom: 10px;">{{ p.data.title | safe }}</h1>
              <p style="font-size: 20px; line-height: 1.45; color: #cbd5e1;">{{ p.data.subtitle }}</p>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 18px; position: relative; z-index: 1;">
              {% for cp in p.data.compare %}
              <div style="background: {{ p.theme.card_bg }}; border: 1.5px solid {{ cp.color }}; border-radius: 22px; padding: 26px 22px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                <div style="background: {{ cp.color }}; color: #fff; font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 900; padding: 6px 12px; border-radius: 8px; display: inline-block; margin-bottom: 16px;">{{ cp.type }}</div>
                {% for pt in cp.points %}
                <div style="display: flex; align-items: flex-start; gap: 10px; margin-bottom: 14px; font-size: 17px; line-height: 1.45; color: #e2e8f0;">
                  <span style="color: {{ cp.color }}; font-weight: 900;">•</span>
                  <span>{{ pt }}</span>
                </div>
                {% endfor %}
              </div>
              {% endfor %}
            </div>
            {% endif %}

            <!-- Bottom Master Rule -->
            <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid {{ p.theme.border }}; border-radius: 18px; padding: 20px 24px; display: flex; align-items: center; gap: 16px; position: relative; z-index: 1;">
              <div style="background: linear-gradient(135deg, {{ p.theme.p }}, {{ p.theme.s }}); color: #000; font-size: 13px; font-weight: 900; padding: 6px 14px; border-radius: 8px; text-transform: uppercase;">Master Rule</div>
              <div style="font-size: 18px; font-weight: 600; color: #e2e8f0; line-height: 1.4;">"{{ p.data.golden_rule }}"</div>
            </div>

            <!-- Footer -->
            <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 22px; border-top: 1px solid rgba(255, 255, 255, 0.08); position: relative; z-index: 1;">
              <div style="display: flex; align-items: center; gap: 14px;">
                <div style="width: 46px; height: 46px; border-radius: 50%; background: linear-gradient(135deg, {{ p.theme.p }}, {{ p.theme.s }}); display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 18px; color: #030712;">AS</div>
                <div>
                  <div style="font-size: 19px; font-weight: 800; color: #f8fafc;">Achhar Sharma</div>
                  <div style="font-size: 13px; color: #64748b;">Daily SEO Growth in Hinglish</div>
                </div>
              </div>
              <div style="font-size: 15px; color: {{ p.theme.p }}; font-weight: 700;">Save for later 📌</div>
            </div>

          </div>
        </div>

        <div class="caption-box" id="caption-{{ p.id }}">{{ p.data.caption }}</div>

        <div class="actions-row">
          <button class="btn btn-copy" onclick="copyCaption('caption-{{ p.id }}', this)">📋 Copy Caption</button>
          <button class="btn btn-dl" style="background: linear-gradient(135deg, {{ p.theme.p }}, {{ p.theme.s }}); color: #000;" onclick="downloadImage('artboard-{{ p.id }}', 'seo_{{ p.theme.id }}_{{ p.data.layout }}.png', this)">💾 Download 4K Graphic</button>
        </div>
      </div>
      {% endfor %}
    </div>

  </div>

  <script>
    // EXACT VIEWPORT AUTO-CALCULATOR: Fits 100% full artboard inside mobile screen!
    function fitArtboardsToMobile() {
      [1, 2].forEach(id => {
        const vp = document.getElementById('viewport-' + id);
        const art = document.getElementById('artboard-' + id);
        if (vp && art) {
          const containerWidth = vp.getBoundingClientRect().width;
          const scale = containerWidth / 1080;
          art.style.transform = `scale(${scale})`;
          vp.style.height = (1350 * scale) + 'px';
        }
      });
    }

    window.addEventListener('resize', fitArtboardsToMobile);
    window.addEventListener('orientationchange', fitArtboardsToMobile);
    document.addEventListener('DOMContentLoaded', fitArtboardsToMobile);
    setTimeout(fitArtboardsToMobile, 250);
    setTimeout(fitArtboardsToMobile, 750);

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
      btn.innerHTML = "⏳ Shuffling Shapes, Colors & AI Topics...";
      btn.disabled = true;

      fetch('/api/shuffle', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
          window.location.reload();
        })
        .catch(err => {
          window.location.reload();
        });
    }

    function downloadImage(artboardId, fileName, btn) {
      const artboard = document.getElementById(artboardId);
      const originalTransform = artboard.style.transform;
      const originalText = btn.innerHTML;
      btn.innerHTML = "⏳ Exporting 4K...";
      btn.disabled = true;

      artboard.style.transform = 'none';

      html2canvas(artboard, {
        width: 1080,
        height: 1350,
        scale: 2,
        useCORS: true,
        backgroundColor: null
      }).then(resCanvas => {
        artboard.style.transform = originalTransform;
        btn.innerHTML = originalText;
        btn.disabled = false;

        const link = document.createElement('a');
        link.download = fileName;
        link.href = resCanvas.toDataURL('image/png');
        link.click();
      }).catch(err => {
        artboard.style.transform = originalTransform;
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

    # Pick 2 completely different structures & 2 completely different color palettes
    s1_idx = offset % len(POST_STRUCTURE_DATABASE)
    s2_idx = (offset + 1) % len(POST_STRUCTURE_DATABASE)

    p1_col = PALETTES[offset % len(PALETTES)]
    p2_col = PALETTES[(offset + 3) % len(PALETTES)]

    posts = [
        {"id": 1, "theme": p1_col, "data": POST_STRUCTURE_DATABASE[s1_idx]},
        {"id": 2, "theme": p2_col, "data": POST_STRUCTURE_DATABASE[s2_idx]}
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
