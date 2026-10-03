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

# 7 MASTER FIGMA ARCHETYPES (BASED ON YOUR EXACT 7 PROMPTS)
# Pure White Background (#FFFFFF) | Deep Green (#064E3B) | Charcoal Black (#0F172A) | Soft Grey (#F1F5F9) | Subtle Gold (#D97706)
FIGMA_STYLES = [
    # 1. PREMIUM EDITORIAL SEO POST
    {
        "id": "style_1",
        "name": "1. Premium Editorial SEO Post",
        "tag": "EDITORIAL FIGMA SPEC",
        "badge": "SEO INTELLIGENCE • ISSUE #42",
        "headline_pre": "THE ALGORITHMIC SHIFT",
        "headline_main": "Why Traditional SEO <span class='green-hl'>Is Dying</span> (And What Replaces It)",
        "keyword_oversized": "SEMANTIC RELEVANCE",
        "data_nodes": [
            {"label": "ENTITY NODES", "val": "4.8x Depth", "desc": "Contextual cluster connection over single keyword stuffing."},
            {"label": "INDEX PRIORITY", "val": "#1 SERP", "desc": "Clean internal link architecture with zero crawl budget leaks."},
            {"label": "INFORMATION GAIN", "val": "+92% Score", "desc": "Original proprietary datasets rewarded by modern search engines."}
        ],
        "metric_badge": "🏆 99.4% TOPICAL AUTHORITY",
        "micro_label": "DATA FLOW ARCHITECTURE // V4.2",
        "golden_rule": "Search engines don't index pages anymore — they index topical authority entities.",
        "caption": """The Algorithmic Shift: Why Traditional SEO Is Dying! 📉✨

2026 me keywords repeat karna band karo. Modern algorithms 'Semantic Relevance' aur 'Entity Graphs' padhte hain.

Key Editorial Breakdown:
1️⃣ Entity Depth (4.8x): Single keyword ke bajaye complete cluster dominate karo.
2️⃣ Index Priority: Crawl budget ko orphan pages me waste mat hone do.
3️⃣ Information Gain (+92%): Jo data Google ke paas nahi hai, wo share karo.

Search engines don't index pages anymore — they index entities!

#SEOStrategy #SemanticSEO #TopicalAuthority #SearchEngineOptimization #DigitalGrowth"""
    },

    # 2. SEO DATA DASHBOARD STYLE
    {
        "id": "style_2",
        "name": "2. SEO Data Dashboard Style",
        "tag": "DASHBOARD ANALYTICS UI",
        "badge": "REAL-TIME SERP METRICS",
        "headline_pre": "PERFORMANCE PULSE",
        "headline_main": "Core Web Vitals <span class='green-hl'>INP Benchmark</span>",
        "keyword_oversized": "+340% TRAFFIC",
        "data_nodes": [
            {"label": "LCP SPEED", "val": "0.8s (PASS)", "desc": "Server-side rendering with critical image preloading."},
            {"label": "INP DELAY", "val": "42ms (OPTIMAL)", "desc": "Zero JavaScript main-thread blocking on user tap."},
            {"label": "INDEX EFFICIENCY", "val": "98.2%", "desc": "100% crawl budget directed to revenue-generating URLs."}
        ],
        "metric_badge": "⚡ GOOGLE SPEED SCORE: 100/100",
        "micro_label": "CONSOLE METRICS // LIVE AUDIT",
        "golden_rule": "Under 2.5s speed is good, but <100ms INP interactivity is what wins page 1 rankings.",
        "caption": """Core Web Vitals & INP: Real-Time Performance Dashboard ⚡📊

March Core Update ke baad agar mobile ranking drop hui hai, to INP check karo:

🔹 LCP: Under 1.2s hona mandatory hai
🔹 INP: <50ms interactivity without main-thread blocking
🔹 Index Ratio: 98%+ valid crawl efficiency

Speed user experience hai, aur user experience hi ranking factor hai! 🚀

#CoreWebVitals #TechSEO #PageSpeed #GoogleConsole #SEOPerformance"""
    },

    # 3. BOLD TYPOGRAPHY + MOTION GRAPHICS
    {
        "id": "style_3",
        "name": "3. Bold Typography + Motion Graphics",
        "tag": "KINETIC TYPOGRAPHY",
        "badge": "MOTION GRAPHIC FRAME #08",
        "headline_pre": "THE BRUTAL REALITY",
        "headline_main": "Content Fails When <span class='gold-hl'>It's Forgettable</span>",
        "keyword_oversized": "REUSE OR DIE",
        "data_nodes": [
            {"label": "STEP 01", "val": "Direct Resolution", "desc": "First 50 words must give the primary answer — zero introduction fluff."},
            {"label": "STEP 02", "val": "Proprietary Terminology", "desc": "Name your strategies so humans repeat and LLMs quote them."},
            {"label": "STEP 03", "val": "Structured Tables", "desc": "HTML comparison matrices get parsed 10x faster by AI bots."}
        ],
        "metric_badge": "🔥 3.4x HIGHER DWELL TIME",
        "micro_label": "ATTENTION CURVE // DYNAMICS",
        "golden_rule": "If people can't easily repeat what you said, search algorithms will never cite it.",
        "caption": """Most Content Fails Not Because It's Bad... But Because It's Forgettable! 💡🎯

AI search aur readers dono generic theory se thak chuke hain.

3 Kinetic Rules:
1. Direct Resolution: Intro paragraph me direct answer do.
2. Named Strategies: Apni methodology ka naam rakho taaki log quote karein.
3. Structured Matrices: Comparison tables use karo.

Be memorable, not just readable!

#ContentMarketing #PersonalBranding #SEO #DigitalStrategy #Creators"""
    },

    # 4. 3D SEO OBJECTS + INFORMATION CARDS
    {
        "id": "style_4",
        "name": "4. 3D SEO Objects + Information Cards",
        "tag": "SPATIAL 3D VECTOR UI",
        "badge": "SEARCH ENGINE ARCHITECTURE",
        "headline_pre": "ZERO-CLICK SEARCH",
        "headline_main": "How To Win <span class='green-hl'>Google AI Overviews</span>",
        "keyword_oversized": "TOP CITATION",
        "data_nodes": [
            {"label": "INVERTED HOOK", "val": "H2 Definition", "desc": "Direct 35-word crisp synopsis positioned above the fold."},
            {"label": "FIRST-PARTY DATA", "val": "Live Studies", "desc": "Original data points that LLMs cannot synthesize independently."},
            {"label": "FAQ SCHEMA", "val": "Schema Markup", "desc": "Valid JSON-LD structured data linking author credentials."}
        ],
        "metric_badge": "💎 +380% CITATION CLICKS",
        "micro_label": "SPATIAL CARDS // FIGMA 3D",
        "golden_rule": "Don't fight AI summaries — become their primary clickable data source.",
        "caption": """Zero-Click Searches: How To Win Google AI Overviews 🤖💎

AI summaries traffic de rahi hain, lekin sirf unhe jo primary source bante hain!

3 Strategic Cards:
✅ Inverted Hook: H2 ke niche direct definition
✅ First-Party Proof: Real client experiments
✅ Structured Schema: Machine-readable data

Become the citation source, not the generic follower! 🚀

#AISEO #GoogleSGE #FutureOfSearch #TechSEO #ContentGrowth"""
    },

    # 5. SEO BLUEPRINT / TECHNICAL DIAGRAM STYLE
    {
        "id": "style_5",
        "name": "5. SEO Blueprint / Technical Diagram Style",
        "tag": "SYSTEM BLUEPRINT SPEC",
        "badge": "TECHNICAL INFRASTRUCTURE",
        "headline_pre": "CRAWL TOPOLOGY",
        "headline_main": "Crawl Budget <span class='green-hl'>Zero-Waste Protocol</span>",
        "keyword_oversized": "CLEAN PIPELINE",
        "data_nodes": [
            {"label": "NODE A: ROBOTS.TXT", "val": "Block Filters", "desc": "Prevent bot access to pagination, session IDs & sort parameters."},
            {"label": "NODE B: CANONICALS", "val": "100% Self-Ref", "desc": "Enforce strict self-referential canonical tags on master URLs."},
            {"label": "NODE C: INTERNAL GRAPH", "val": "Depth ≤ 3 Clicks", "desc": "Ensure high-converting pages are reachable within 3 clicks."}
        ],
        "metric_badge": "🛡️ 100% HEALTH SCORE",
        "micro_label": "BLUEPRINT TOPOLOGY // SYS-88",
        "golden_rule": "Every crawl request wasted on a junk URL is a revenue page Googlebot ignores.",
        "caption": """Technical SEO Blueprint: Crawl Budget Zero-Waste Protocol 📐🛠️

Search Console me 'Discovered - Currently Not Indexed' aa raha hai? Blueprint check karo:

Node 1: Robots.txt me useless sorting parameters block karo.
Node 2: Canonicals strictly audit karo.
Node 3: Click depth under 3 clicks rakho.

Architecture matters more than keywords!

#TechnicalSEO #CrawlBudget #SearchConsole #WebArchitecture #SEOAudit"""
    },

    # 6. MODERN AI + SEO MOTION POST
    {
        "id": "style_6",
        "name": "6. Modern AI + SEO Motion Post",
        "tag": "NEURAL INTERFACE SPEC",
        "badge": "LLM OPTIMIZATION • 2026",
        "headline_pre": "NEURAL RETRIEVAL",
        "headline_main": "Generative Engine <span class='green-hl'>Optimization (GEO)</span>",
        "keyword_oversized": "LLM VISIBILITY",
        "data_nodes": [
            {"label": "VECTOR EMBEDDING", "val": "High Cosine Sim", "desc": "Semantic vectors matching common conversational prompts."},
            {"label": "CREDIBILITY SIGNALS", "val": "E-E-A-T Verified", "desc": "Author footprint indexed across authoritative knowledge graphs."},
            {"label": "CONVERSATIONAL INTENT", "val": "Multi-Turn", "desc": "Content structured to resolve multi-step complex workflows."}
        ],
        "metric_badge": "🔮 5.2x BRAND CITATIONS",
        "micro_label": "NEURAL GRAPH // V2.6",
        "golden_rule": "Traditional SEO targets rank position. GEO targets AI knowledge base inclusion.",
        "caption": """Generative Engine Optimization (GEO): The Next Frontier 🤖🌐

Rank 1 par aana kafi nahi hai — AI models aapko apni memory me rakhein, ye naya target hai.

3 GEO Dimensions:
🔹 Vector Embeddings: Natural conversational vocabulary
🔹 Author Footprint: Real verified E-E-A-T
🔹 Multi-Turn Content: Deep problem solving

Are you optimizing for search engines or for neural models?

#GEO #GenerativeAI #FutureOfSEO #AIOptimization #DigitalStrategy"""
    },

    # 7. "INFORMATION EXPLODED" FIGMA STYLE
    {
        "id": "style_7",
        "name": "7. Information Exploded Figma Style",
        "tag": "EXPLODED INFORMATION SYSTEM",
        "badge": "DISSECTED MECHANICS",
        "headline_pre": "THE ANATOMY OF A #1 RANK",
        "headline_main": "What Actually Drives <span class='gold-hl'>Organic Conversions</span>",
        "keyword_oversized": "EXPLODED SYSTEM",
        "data_nodes": [
            {"label": "COMPONENT 1", "val": "High-Intent Keyword", "desc": "500-volume commercial query > 50,000 broad informational term."},
            {"label": "COMPONENT 2", "val": "Above-The-Fold Value", "desc": "Pricing, comparison table or direct tool within first screen viewport."},
            {"label": "COMPONENT 3", "val": "Frictionless CTA", "desc": "Single clear next action without intrusive popup banners."}
        ],
        "metric_badge": "📈 +410% REVENUE CONVERSION",
        "micro_label": "SYSTEM DECONSTRUCTION // EXP-07",
        "golden_rule": "Traffic is a vanity metric; bottom-funnel organic conversion is the real business metric.",
        "caption": """The Exploded System: The Anatomy of a High-Converting #1 Rank! 💥📊

Traffic badh raha hai par revenue zero hai? Aapke system ka fault samjho:

1️⃣ High-Intent Keywords: Commercial searchers > Curiosity searchers
2️⃣ Above-the-Fold Value: 3 seconds me value deliver karo
3️⃣ Frictionless UX: Zero intrusive popups

Stop optimizing for clicks. Start optimizing for revenue! 🔥

#ConversionRate #SEOForBusiness #OrganicGrowth #DigitalMarketing #ROI"""
    }
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>Premium Figma White-Background SEO Studio</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600;700;800&display=swap" rel="stylesheet">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
  <style>
    :root {
      --deep-green: #064e3b;
      --emerald: #059669;
      --charcoal: #0f172a;
      --soft-grey: #f8fafc;
      --border-grey: #e2e8f0;
      --gold: #d97706;
      --gold-light: #fbbf24;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }

    body {
      background-color: #0b0f19;
      font-family: 'Plus Jakarta Sans', sans-serif;
      color: #f8fafc;
      min-height: 100vh;
      padding: 16px 12px;
      overflow-x: hidden;
    }

    .container {
      width: 100%;
      max-width: 1250px;
      margin: 0 auto;
    }

    /* TOP HEADER */
    .top-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      padding-bottom: 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      margin-bottom: 20px;
    }

    .brand-title {
      font-size: 20px;
      font-weight: 900;
      letter-spacing: -0.02em;
    }

    .brand-sub {
      font-size: 12px;
      color: #94a3b8;
    }

    /* SHUFFLER HUB */
    .shuffler-hub {
      background: rgba(18, 24, 38, 0.85);
      border: 1px solid rgba(5, 150, 105, 0.35);
      border-radius: 16px;
      padding: 16px;
      margin-bottom: 24px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    @media (min-width: 600px) {
      .shuffler-hub {
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
      }
    }

    .btn-shuffle {
      background: linear-gradient(135deg, #064e3b 0%, #059669 50%, #d97706 100%);
      color: #fff;
      font-weight: 800;
      font-size: 14px;
      padding: 13px 24px;
      border-radius: 12px;
      border: none;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 4px 20px rgba(5, 150, 105, 0.4);
      width: 100%;
    }

    @media (min-width: 600px) {
      .btn-shuffle { width: auto; }
    }

    /* POSTS FEED */
    .posts-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 30px;
      margin-bottom: 40px;
    }

    @media (min-width: 900px) {
      .posts-grid {
        grid-template-columns: repeat(2, 1fr);
      }
    }

    .post-panel {
      background: #111827;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      overflow: hidden;
    }

    .panel-top-tag {
      font-size: 13px;
      font-weight: 800;
      color: #34d399;
      display: flex;
      justify-content: space-between;
    }

    /* ========================================================
       100% PERFECT MOBILE FULL-SCREEN FIT VIEWPORT
       ======================================================== */
    .artboard-viewport {
      width: 100%;
      position: relative;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
      border: 1px solid rgba(255, 255, 255, 0.12);
      background: #ffffff;
    }

    /* ========================================================
       PURE WHITE FIGMA MASTER CANVAS (1080x1350)
       Clean White Canvas • Deep Green • Charcoal • Gold
       ======================================================== */
    .figma-master-canvas {
      width: 1080px;
      height: 1350px;
      background: #ffffff;
      padding: 70px 65px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: absolute;
      top: 0;
      left: 0;
      transform-origin: top left;
      font-family: 'Plus Jakarta Sans', sans-serif;
      color: #0f172a;
      overflow: hidden;
    }

    /* SUBTLE FIGMA TECHNICAL GRID LINES (WHITE BACKGROUND) */
    .figma-blueprint-grid {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background-size: 40px 40px;
      background-image: 
        linear-gradient(to right, rgba(15, 23, 42, 0.03) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(15, 23, 42, 0.03) 1px, transparent 1px);
      pointer-events: none;
    }

    /* HIGHLIGHT STYLING */
    .green-hl {
      color: #064e3b;
      position: relative;
      display: inline-block;
    }

    .green-hl::after {
      content: '';
      position: absolute;
      left: 0;
      bottom: 6px;
      width: 100%;
      height: 8px;
      background: rgba(5, 150, 105, 0.18);
      z-index: -1;
      border-radius: 4px;
    }

    .gold-hl {
      color: #b45309;
      position: relative;
      display: inline-block;
    }

    .gold-hl::after {
      content: '';
      position: absolute;
      left: 0;
      bottom: 6px;
      width: 100%;
      height: 8px;
      background: rgba(217, 119, 6, 0.2);
      z-index: -1;
      border-radius: 4px;
    }

    /* FIGMA BADGES & MICRO LABELS */
    .figma-badge-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: relative;
      z-index: 1;
    }

    .figma-badge-chip {
      background: #f0fdf4;
      border: 1.5px solid #86efac;
      color: #064e3b;
      font-family: 'JetBrains Mono', monospace;
      font-size: 14px;
      font-weight: 800;
      padding: 8px 18px;
      border-radius: 8px;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }

    .figma-badge-chip::before {
      content: '';
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #059669;
    }

    .figma-metric-pill {
      background: #f8fafc;
      border: 1.5px solid #e2e8f0;
      color: #0f172a;
      font-family: 'JetBrains Mono', monospace;
      font-size: 14px;
      font-weight: 700;
      padding: 8px 18px;
      border-radius: 8px;
    }

    /* HEADLINE AREA */
    .figma-headline-wrap {
      margin: 20px 0;
      position: relative;
      z-index: 1;
    }

    .figma-pre-title {
      font-family: 'JetBrains Mono', monospace;
      font-size: 15px;
      font-weight: 800;
      color: #059669;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .figma-pre-title::before {
      content: '//';
      color: #d97706;
    }

    .figma-headline-text {
      font-size: 58px;
      font-weight: 900;
      line-height: 1.1;
      letter-spacing: -0.03em;
      color: #0f172a;
    }

    /* OVERSIZED WATERMARK KEYWORD (PREMIUM FIGMA AGENCY TOUCH) */
    .figma-watermark-keyword {
      font-family: 'JetBrains Mono', monospace;
      font-size: 72px;
      font-weight: 900;
      color: rgba(15, 23, 42, 0.04);
      letter-spacing: -0.04em;
      line-height: 1;
      margin-top: -15px;
      margin-bottom: 10px;
      pointer-events: none;
      user-select: none;
    }

    /* 3 FLOATING HIGH-END FIGMA DATA CARDS */
    .figma-nodes-grid {
      display: flex;
      flex-direction: column;
      gap: 16px;
      position: relative;
      z-index: 1;
    }

    .figma-node-card {
      background: #ffffff;
      border: 1.5px solid #e2e8f0;
      border-radius: 18px;
      padding: 22px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
      box-shadow: 0 10px 25px rgba(15, 23, 42, 0.04);
      position: relative;
      overflow: hidden;
    }

    .figma-node-card::before {
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      width: 4px;
      height: 100%;
      background: #059669;
    }

    .figma-node-left {
      flex: 1;
    }

    .figma-node-label {
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      font-weight: 800;
      color: #059669;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      margin-bottom: 4px;
    }

    .figma-node-desc {
      font-size: 18px;
      font-weight: 600;
      color: #334155;
      line-height: 1.45;
    }

    .figma-node-val-badge {
      background: #0f172a;
      color: #f8fafc;
      font-family: 'JetBrains Mono', monospace;
      font-size: 18px;
      font-weight: 800;
      padding: 10px 18px;
      border-radius: 10px;
      white-space: nowrap;
      box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
    }

    /* GOLDEN RULE FOOTER BANNER */
    .figma-golden-rule-box {
      background: #f8fafc;
      border: 1.5px solid #cbd5e1;
      border-radius: 16px;
      padding: 20px 24px;
      display: flex;
      align-items: center;
      gap: 16px;
      position: relative;
      z-index: 1;
    }

    .figma-gold-tag {
      background: #d97706;
      color: #ffffff;
      font-size: 13px;
      font-weight: 900;
      padding: 6px 12px;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      white-space: nowrap;
    }

    .figma-rule-text {
      font-size: 18px;
      font-weight: 700;
      color: #0f172a;
      line-height: 1.4;
    }

    /* FOOTER SIGNATURE */
    .figma-footer-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 20px;
      border-top: 1.5px solid #f1f5f9;
      position: relative;
      z-index: 1;
    }

    .figma-author-wrap {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .figma-author-circle {
      width: 44px;
      height: 44px;
      border-radius: 10px;
      background: #064e3b;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
      font-size: 17px;
    }

    .figma-author-name {
      font-size: 18px;
      font-weight: 800;
      color: #0f172a;
    }

    .figma-author-title {
      font-size: 13px;
      color: #64748b;
    }

    .figma-micro-watermark {
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      font-weight: 700;
      color: #059669;
    }

    /* CAPTION BOX & ACTIONS */
    .caption-box {
      background: rgba(0, 0, 0, 0.45);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 12px;
      padding: 14px;
      font-size: 13px;
      line-height: 1.6;
      color: #e2e8f0;
      max-height: 200px;
      overflow-y: auto;
      white-space: pre-wrap;
    }

    .actions-row {
      display: flex;
      gap: 10px;
      flex-direction: column;
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
    }

    .btn-copy { background: rgba(255, 255, 255, 0.08); color: #f8fafc; border: 1px solid rgba(255, 255, 255, 0.15); }
    .btn-dl { background: linear-gradient(135deg, #064e3b, #059669); color: #fff; }
    .toast-active { background: #10b981 !important; color: #fff !important; }
  </style>
</head>
<body>
  <div class="container">
    <!-- Header -->
    <div class="top-header">
      <div>
        <div class="brand-title">Achhar Sharma • Figma Master SEO Studio</div>
        <div class="brand-sub">Pure White Canvas • Deep Green & Gold • 7 High-End Design Archetypes</div>
      </div>
      <div style="font-size: 12px; color: #34d399; font-weight: 700;">● 24/7 Cloud Active</div>
    </div>

    <!-- SHUFFLER BUTTON -->
    <div class="shuffler-hub">
      <div>
        <h3 style="font-size: 16px; font-weight: 800; color: #34d399; margin-bottom: 2px;">🎲 7 Figma Design Archetypes Shuffler</h3>
        <p style="font-size: 13px; color: #94a3b8;">Click karte hi Editorial, Data Dashboard, 3D Vector & Blueprint designs rotate honge!</p>
      </div>
      <button class="btn-shuffle" onclick="shuffleFigmaPost()" id="shufBtn">
        ✨ Generate Next Figma SEO Archetype
      </button>
    </div>

    <!-- FEED -->
    <div class="posts-grid">
      {% for p in posts %}
      <div class="post-panel">
        <div class="panel-top-tag">
          <span>{{ p.name }}</span>
          <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #94a3b8;">1080x1350 4K</span>
        </div>

        <!-- 100% MOBILE FULL VISIBLE VIEWPORT WRAPPER -->
        <div class="artboard-viewport" id="viewport-{{ loop.index }}">
          <div class="figma-master-canvas" id="canvas-{{ loop.index }}">
            <div class="figma-blueprint-grid"></div>

            <!-- 1. Top Badges Row -->
            <div class="figma-badge-row">
              <div class="figma-badge-chip">{{ p.badge }}</div>
              <div class="figma-metric-pill">{{ p.metric_badge }}</div>
            </div>

            <!-- 2. Headline & Pre-title -->
            <div class="figma-headline-wrap">
              <div class="figma-pre-title">{{ p.headline_pre }}</div>
              <h1 class="figma-headline-text">{{ p.headline_main | safe }}</h1>
            </div>

            <!-- 3. Oversized Keyword Typography (Subtle Background Touch) -->
            <div class="figma-watermark-keyword">{{ p.keyword_oversized }}</div>

            <!-- 4. 3 Floating Figma Data Cards -->
            <div class="figma-nodes-grid">
              {% for node in p.data_nodes %}
              <div class="figma-node-card">
                <div class="figma-node-left">
                  <div class="figma-node-label">{{ node.label }}</div>
                  <div class="figma-node-desc">{{ node.desc }}</div>
                </div>
                <div class="figma-node-val-badge">{{ node.val }}</div>
              </div>
              {% endfor %}
            </div>

            <!-- 5. Golden Rule Banner -->
            <div class="figma-golden-rule-box">
              <div class="figma-gold-tag">Strategic Rule</div>
              <div class="figma-rule-text">"{{ p.golden_rule }}"</div>
            </div>

            <!-- 6. Footer Signature -->
            <div class="figma-footer-row">
              <div class="figma-author-wrap">
                <div class="figma-author-circle">AS</div>
                <div>
                  <div class="figma-author-name">Achhar Sharma</div>
                  <div class="figma-author-title">SEO Architecture & Growth</div>
                </div>
              </div>
              <div class="figma-micro-watermark">{{ p.micro_label }}</div>
            </div>

          </div>
        </div>

        <div class="caption-box" id="caption-{{ loop.index }}">{{ p.caption }}</div>

        <div class="actions-row">
          <button class="btn btn-copy" onclick="copyCaption('caption-{{ loop.index }}', this)">📋 Copy Caption</button>
          <button class="btn btn-dl" onclick="downloadImage('canvas-{{ loop.index }}', 'figma_seo_post_{{ loop.index }}.png', this)">💾 Download 4K Graphic</button>
        </div>
      </div>
      {% endfor %}
    </div>

  </div>

  <script>
    // PRECISE AUTO-SCALER FOR MOBILE: Calculates viewport width and fits 1080x1350 perfectly!
    function fitFigmaArtboards() {
      [1, 2].forEach(id => {
        const vp = document.getElementById('viewport-' + id);
        const cv = document.getElementById('canvas-' + id);
        if (vp && cv) {
          const w = vp.getBoundingClientRect().width;
          const scale = w / 1080;
          cv.style.transform = `scale(${scale})`;
          vp.style.height = (1350 * scale) + 'px';
        }
      });
    }

    window.addEventListener('resize', fitFigmaArtboards);
    window.addEventListener('orientationchange', fitFigmaArtboards);
    document.addEventListener('DOMContentLoaded', fitFigmaArtboards);
    setTimeout(fitFigmaArtboards, 250);
    setTimeout(fitFigmaArtboards, 750);

    function copyCaption(id, btn) {
      const text = document.getElementById(id).innerText;
      navigator.clipboard.writeText(text).then(() => {
        const orig = btn.innerHTML;
        btn.innerHTML = "✅ Copied to Clipboard!";
        btn.classList.add('toast-active');
        setTimeout(() => {
          btn.innerHTML = orig;
          btn.classList.remove('toast-active');
        }, 2000);
      });
    }

    function shuffleFigmaPost() {
      const btn = document.getElementById('shufBtn');
      btn.innerHTML = "⏳ Shuffling Figma Archetype...";
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
        backgroundColor: '#ffffff'
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

    p1_idx = offset % len(FIGMA_STYLES)
    p2_idx = (offset + 1) % len(FIGMA_STYLES)

    posts = [FIGMA_STYLES[p1_idx], FIGMA_STYLES[p2_idx]]
    return render_template_string(HTML_TEMPLATE, posts=posts)

@app.route("/api/shuffle", methods=["POST"])
def api_shuffle():
    state = get_current_state()
    state["offset"] = (state.get("offset", 0) + 1) % len(FIGMA_STYLES)
    save_current_state(state)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
