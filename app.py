import os
import sys
import json
import random
import datetime
import requests
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# Provided API Key from User
DEFAULT_API_KEY = "AQ.Ab8RN6Jutt5n2XU3lXNxEIUUrPb2-CHUwrEZOuc3eigG0JYLOQ"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", DEFAULT_API_KEY)

# 6 High-End Figma Color Themes
THEMES = [
    {
        "id": "cyber-cyan",
        "name": "Cyber Cyan",
        "bg": "#070b14",
        "card_bg": "rgba(13, 22, 38, 0.85)",
        "primary": "#00f2fe",
        "secondary": "#4facfe",
        "accent": "#38bdf8",
        "glow": "rgba(0, 242, 254, 0.25)",
        "badge_border": "rgba(0, 242, 254, 0.4)",
        "badge_bg": "rgba(0, 242, 254, 0.12)"
    },
    {
        "id": "royal-purple",
        "name": "Royal Purple",
        "bg": "#0c0817",
        "card_bg": "rgba(22, 14, 42, 0.85)",
        "primary": "#c084fc",
        "secondary": "#818cf8",
        "accent": "#a855f7",
        "glow": "rgba(168, 85, 247, 0.25)",
        "badge_border": "rgba(192, 132, 252, 0.4)",
        "badge_bg": "rgba(168, 85, 247, 0.12)"
    },
    {
        "id": "emerald-jade",
        "name": "Emerald Growth",
        "bg": "#04120a",
        "card_bg": "rgba(8, 31, 19, 0.85)",
        "primary": "#34d399",
        "secondary": "#10b981",
        "accent": "#059669",
        "glow": "rgba(52, 211, 153, 0.25)",
        "badge_border": "rgba(52, 211, 153, 0.4)",
        "badge_bg": "rgba(16, 185, 129, 0.12)"
    },
    {
        "id": "sunset-amber",
        "name": "Sunset Fire",
        "bg": "#140a04",
        "card_bg": "rgba(35, 17, 8, 0.85)",
        "primary": "#fbbf24",
        "secondary": "#f97316",
        "accent": "#ea580c",
        "glow": "rgba(249, 115, 22, 0.25)",
        "badge_border": "rgba(251, 191, 36, 0.4)",
        "badge_bg": "rgba(249, 115, 22, 0.12)"
    },
    {
        "id": "crimson-ruby",
        "name": "Crimson Alert",
        "bg": "#140508",
        "card_bg": "rgba(33, 10, 16, 0.85)",
        "primary": "#fb7185",
        "secondary": "#f43f5e",
        "accent": "#e11d48",
        "glow": "rgba(244, 63, 94, 0.25)",
        "badge_border": "rgba(251, 113, 133, 0.4)",
        "badge_bg": "rgba(244, 63, 94, 0.12)"
    },
    {
        "id": "electric-sapphire",
        "name": "Deep Sapphire",
        "bg": "#050d1a",
        "card_bg": "rgba(10, 24, 48, 0.85)",
        "primary": "#60a5fa",
        "secondary": "#3b82f6",
        "accent": "#2563eb",
        "glow": "rgba(59, 130, 246, 0.25)",
        "badge_border": "rgba(96, 165, 250, 0.4)",
        "badge_bg": "rgba(37, 99, 235, 0.12)"
    }
]

# Curated High-Retention SEO Topics
DAILY_POOL = [
    {
        "badge": "Technical SEO",
        "category": "#TechSEO #CoreWebVitals",
        "title": "Google Ranking <span class='hl'>Kyu Drop Hui?</span> Check 3 Hidden Fixes",
        "subtitle": "Traffic achanak down ho gaya hai? Panic mat karo, ye 3 technical checkpoints audit karo:",
        "cards": [
            {"num": "01", "heading": "Crawl Budget Waste", "text": "Robots.txt check karo — important pages kahin noindex ya junk URLs index to nahi ho rahe?"},
            {"num": "02", "heading": "Keyword Cannibalization", "text": "Aapke 2 alag pages same search intent ke liye aapas me compete kar rahe hain."},
            {"num": "03", "heading": "LCP & INP Score Spike", "text": "Heavy images aur uncompressed JS ki wajah se mobile score 40 se niche chala gaya."}
        ],
        "pro_tip": "Traffic drop hone par naya article likhne se pehle old content ka search intent audit karo!",
        "caption": """🚨 Google traffic achanak 30-40% drop ho gaya? Don't panic!

Har traffic drop Google Penalty nahi hota. 90% cases me ye 3 silent technical mistakes hoti hain:

1️⃣ Crawl Budget Leak:
Check karo Search Console me 'Discovered - currently not indexed'. Agar junk filter URLs index ho rahe hain to crawl budget waste ho raha hai.

2️⃣ Keyword Cannibalization:
Agar aapke 2 blog posts ek hi target keyword ke liye rank karne ki koshish kar rahe hain, to Google confuse ho jata hai aur dono ki ranking gira deta hai.

3️⃣ Core Web Vitals (INP/LCP):
March Core Update ke baad speed aur user interactivity sabse bada ranking factor ban chuka hai. Mobile speed < 2.5s hona mandatory hai.

👉 Quick Action Plan:
Google Search Console open karo > Performance tab me compare last 28 days > Dekho kaunse specific URLs drop hue hain.

Kya aapne recently traffic drop face kiya? Comments me apna query batao, let's audit together! 💬

#SEO #DigitalMarketing #GoogleAlgorithm #SearchEngineOptimization #TechSEO #ContentStrategy"""
    },
    {
        "badge": "On-Page SEO",
        "category": "#SearchIntent #OnPageSEO",
        "title": "Keyword Stuffing Band Karo, <span class='hl'>Semantic SEO</span> Sikho",
        "subtitle": "2026 me Google keywords nahi, topic ka context aur intent samajhta hai:",
        "cards": [
            {"num": "01", "heading": "Entity & Topical Authority", "text": "Ek keyword ko 10 baar repeat karne ke bajaye us topic se related sub-topics cover karo."},
            {"num": "02", "heading": "LSI & NLP Terms", "text": "Users search me jo natural synonyms aur conversational phrases bolte hain unka use karo."},
            {"num": "03", "heading": "Answer The First 3 Questions", "text": "User ke click karte hi pehle 100 words me primary question ka exact jawab milna chahiye."}
        ],
        "pro_tip": "Write for humans, optimize for entities — Google ka AI ab context padhta hai, frequency nahi!",
        "caption": """Stop stuffing keywords like it's 2012! ❌

Google ka search algorithm ab itna smart ho chuka hai ki agar aap 'best running shoes' 15 baar likhoge, to ranking boost nahi balki spam penalty mil sakti hai.

Ab game hai 'Semantic SEO' aur 'Topical Authority' ka. 🚀

Yahan hain 3 rules jo aapko follow karne chahiye:

🔹 1. Focus on Entities, Not Just Words:
Agar aap 'Python Course' par likh rahe ho, to 'Syntax', 'Data Types', 'Pandas', 'Career Scope' jaise related concepts cover hone chahiye.

🔹 2. Answer Directly in Intro:
People don't want 500 words ki background story. User ka primary question first paragraph me solve karo (Featured Snippet win karne ka shortcut!).

🔹 3. Search Intent > Keyword Volume:
10k volume wala broad keyword bekar hai agar user ka intent clear nahi hai. 500 volume wala high-intent commercial keyword zyada conversions dega.

Aapka On-Page SEO workflow kaisa hai? Tools rely karte ho ya manual search intent check karte ho?

#OnPageSEO #SemanticSEO #ContentMarketing #GoogleRanking #DigitalGrowth #SEOIndia"""
    },
    {
        "badge": "AI & Future of SEO",
        "category": "#AIOptimization #GoogleSGE",
        "title": "Google AI Overviews Se <span class='hl'>Traffic Kaise Bachayein?</span>",
        "subtitle": "Search results me AI summary aane ke baad CTR kam ho gaya? Ye strategy follow karo:",
        "cards": [
            {"num": "01", "heading": "Unique First-Party Data", "text": "Case studies, original experiments aur personal data share karo jo AI kabhi copy na kar sake."},
            {"num": "02", "heading": "Direct Quotable Snippets", "text": "Aapke answers concise definitions aur bullet points me hone chahiye taaki AI aapko source cite kare."},
            {"num": "03", "heading": "High Intent Bottom Funnel", "text": "Informational queries par AI answer de dega, lekin decision-making & comparisons par traffic aayega."}
        ],
        "pro_tip": "AI summary ke liye source bano, rival nahi — schema markup aur concise data citations add karo!",
        "caption": """Kya Google AI Overviews aapke website traffic ko kha raha hai? 🤖📉

Zero-click searches badh rahe hain, lekin iska matlab SEO dead nahi hai — game evolve ho gaya hai!

Agar aap abhi bhi generic AI-generated 1000-word articles likh rahe ho, to aapka traffic zero ho jayega kyunki Google wo summary khud generate kar leta hai.

To rank aur traffic kaise laye?
✅ 1. Share Real Human Experience (E-E-A-T):
Screenshots, live client results, personal mistakes share karo. AI experience invent nahi kar sakta.

✅ 2. Become The Primary Source:
Original research aur statistical survey publish karo. Google AI summary hamesha original source ko clickable citation link deta hai.

✅ 3. Target Long-Tail & Complex Queries:
Complex troubleshooting aur opinionated topics jahan human perspective chahiye, wahan log website click karte hain.

Aapke analytics me AI search ka koi impact dikha abhi tak? Share your experience!

#AISEO #GoogleSearch #AIOverwiews #DigitalMarketing #FutureOfSEO #ContentCreators"""
    },
    {
        "badge": "Off-Page SEO",
        "category": "#Backlinks #LinkBuilding",
        "title": "Toxic Backlinks vs <span class='hl'>Quality PR Links</span>",
        "subtitle": "Fiverr se 1000 backlinks khareedna band karo! 2026 me link building ka real truth:",
        "cards": [
            {"num": "01", "heading": "Relevance Beats Domain Rating", "text": "DA 80 ke unrelated niche link se 10x better hai DA 35 ki relevant industry website ka link."},
            {"num": "02", "heading": "Digital PR & Data Led Studies", "text": "Industry trends par short report banao — journalists aur bloggers khud natural backlink denge."},
            {"num": "03", "heading": "Unlinked Brand Mentions", "text": "Google Alerts lagao, jahan bhi aapka brand name mention ho par link na ho, polite outreach karo."}
        ],
        "pro_tip": "1 high-relevance editorial backlink = 500 spam PBN links. Quality always wins!",
        "caption": """Fiverr pe ₹500 me 1000 Backlinks milte hain... Par kya wo sach me rank karwate hain? ❌

Bilkul nahi! Ulta aapki website algorithmic penalty (Spam Brain) me phas sakti hai.

2026 me Backlink strategy aisi honi chahiye:

1️⃣ Relevancy is King:
Agar aapka blog Fitness par hai, to ek local gym blog ka link zyada valuable hai kisi unrelated general news site se.

2️⃣ Digital PR Campaign:
Industry ka chota sa data survey karo. Example: 'Survey of 100 Indian SaaS Websites SEO errors'. Is report ko LinkedIn aur Twitter pe share karo, log naturally quote karenge.

3️⃣ Claim Unlinked Mentions:
Aapka brand ya founder ka naam kahi mention hua ho bina hyperlink ke? Just unhe ek friendly message bhejo for link attribution.

Stop building links, start earning them! 🔥

What is your #1 link building tactic right now? Drop in comments!

#LinkBuilding #OffPageSEO #SEOStrategy #Backlinks #GrowthHacking #DigitalMarketingIndia"""
    },
    {
        "badge": "E-E-A-T Blueprint",
        "category": "#GoogleGuidelines #Authority",
        "title": "Google E-E-A-T Score <span class='hl'>Kaise Boost Karein?</span>",
        "subtitle": "Bina Experience aur Author Trust ke 2026 me Google rank nahi karega:",
        "cards": [
            {"num": "01", "heading": "Verified Author Bios", "text": "Har article ke niche author bio, LinkedIn profile aur niche credentials link karo."},
            {"num": "02", "heading": "First-Hand Proof & Images", "text": "Stock photos hatao, actual dashboards aur real workflow pictures use karo."},
            {"num": "03", "heading": "Citation & Scientific Sources", "text": "Stat claim karne se pehle research paper ya authoritative website link karo."}
        ],
        "pro_tip": "Google algorithm ab author ki digital footprint scan karta hai — build personal brand!",
        "caption": """Agar aapka content rank nahi ho raha, to problem keywords me nahi, E-E-A-T me ho sakti hai! 🔍

Google ke Quality Rater Guidelines me E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) sabse critical factor hai.

Agar website anonymous hai ya fake AI author bio lagaya hai, to Google ka Trust Algorithm rank drop kar deta hai.

3 Quick E-E-A-T Fixes Aaj Hi Karo:

📌 1. Real Author Pages Banao:
Har writer ka detailed page banao jisme unka experience, LinkedIn profile, aur past publications linked hon.

📌 2. Original Media Add Karo:
Stock images ki jagah khud ke banaye infographics, tools ke screenshots, ya loom video clips embed karo.

📌 3. Back Up Your Claims:
Koi bhi stat ya percentage bolo to reliable study ko source karo.

Trust earn karo, ranking apne aap follow karegi! 🚀

#EEAT #GoogleTrust #SEOIndia #ContentOptimization #SearchEngineOptimization #SEOStrategy"""
    }
]

def generate_via_gemini_api(api_key, count=2):
    """Uses Gemini API with multiple candidate models to generate daily posts."""
    candidate_models = ["gemini-1.5-flash", "gemini-2.5-flash", "gemini-flash-latest"]
    prompt = f"""Generate {count} distinct SEO educational LinkedIn posts in Hinglish.
Return valid JSON only in this exact format:
[
  {{
    "badge": "Technical SEO / On-Page / Link Building / etc",
    "category": "#Hashtag1 #Hashtag2",
    "title": "Catchy headline with <span class='hl'> tag for highlight like: Google Ranking <span class='hl'>Kyu Drop Hui?</span>",
    "subtitle": "Short subtitle in Hinglish explaining the problem",
    "cards": [
      {{"num": "01", "heading": "Heading 1", "text": "Hinglish explanation in 1-2 lines"}},
      {{"num": "02", "heading": "Heading 2", "text": "Hinglish explanation in 1-2 lines"}},
      {{"num": "03", "heading": "Heading 3", "text": "Hinglish explanation in 1-2 lines"}}
    ],
    "pro_tip": "One line golden rule in Hinglish",
    "caption": "Full high-converting LinkedIn post caption with emojis, hook, 3 points, CTA, and 5 hashtags in Hinglish."
  }}
]"""

    for model in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        try:
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=12)
            if res.status_code == 200:
                data = res.json()
                raw_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                if raw_text.startswith("```json"):
                    raw_text = raw_text[7:-3].strip()
                elif raw_text.startswith("```"):
                    raw_text = raw_text[3:-3].strip()
                parsed = json.loads(raw_text)
                if isinstance(parsed, list) and len(parsed) >= count:
                    return parsed[:count]
        except Exception:
            continue
    return None

def get_posts_for_today():
    day_num = datetime.datetime.now().timetuple().tm_yday
    # Select 2 distinct color themes for morning & evening
    theme1 = THEMES[day_num % len(THEMES)]
    theme2 = THEMES[(day_num + 3) % len(THEMES)]

    # Try Gemini API if key is present
    posts_data = None
    if GEMINI_API_KEY:
        posts_data = generate_via_gemini_api(GEMINI_API_KEY, 2)

    if not posts_data:
        idx1 = (day_num * 2) % len(DAILY_POOL)
        idx2 = (day_num * 2 + 1) % len(DAILY_POOL)
        posts_data = [DAILY_POOL[idx1], DAILY_POOL[idx2]]

    posts = [
        {
            "id": 1,
            "name": "Post #1 • Morning Insights",
            "theme": theme1,
            "data": posts_data[0]
        },
        {
            "id": 2,
            "name": "Post #2 • Evening Strategy",
            "theme": theme2,
            "data": posts_data[1]
        }
    ]
    return posts

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>LinkedIn Daily SEO Post Agent</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
  <style>
    :root {
      --bg: #090d16;
      --card-bg: rgba(18, 24, 38, 0.85);
      --border: rgba(255, 255, 255, 0.08);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background-color: var(--bg);
      background-image: 
        radial-gradient(circle at 10% 10%, rgba(56, 189, 248, 0.07) 0%, transparent 40%),
        radial-gradient(circle at 90% 90%, rgba(139, 92, 246, 0.07) 0%, transparent 40%);
      font-family: 'Plus Jakarta Sans', sans-serif;
      color: var(--text-main);
      min-height: 100vh;
      padding: 24px 16px;
      -webkit-font-smoothing: antialiased;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
    }

    /* Top Bar */
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 30px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .logo-badge {
      width: 44px;
      height: 44px;
      border-radius: 12px;
      background: linear-gradient(135deg, #38bdf8, #818cf8);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
      font-size: 18px;
      color: #090d16;
      box-shadow: 0 0 20px rgba(56, 189, 248, 0.35);
    }

    .title-group h1 {
      font-size: 22px;
      font-weight: 800;
      letter-spacing: -0.02em;
    }

    .title-group p {
      color: var(--text-muted);
      font-size: 13px;
    }

    .live-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      border-radius: 999px;
      background: rgba(16, 185, 129, 0.1);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: #34d399;
      font-size: 13px;
      font-weight: 700;
    }

    .live-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #34d399;
      box-shadow: 0 0 8px #34d399;
      animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
    }

    .theme-banner {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 12px 18px;
      margin-bottom: 25px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
      font-size: 14px;
      color: #cbd5e1;
    }

    /* Grid Layout */
    .posts-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
      gap: 30px;
      margin-bottom: 40px;
    }

    @media (max-width: 650px) {
      .posts-grid {
        grid-template-columns: 1fr;
      }
    }

    .post-panel {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      gap: 18px;
      box-shadow: 0 10px 40px -15px rgba(0, 0, 0, 0.6);
    }

    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }

    .panel-title {
      font-size: 15px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .theme-chip {
      font-size: 12px;
      padding: 4px 10px;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.08);
      color: var(--text-muted);
      font-family: 'JetBrains Mono', monospace;
    }

    /* FIGMA CARD CONTAINER (1080x1350 scale) */
    .render-wrapper {
      width: 100%;
      background: #000;
      border-radius: 16px;
      overflow: hidden;
      border: 1px solid var(--border);
      position: relative;
    }

    .figma-card {
      width: 1080px;
      height: 1350px;
      padding: 70px 65px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
      transform-origin: top left;
      /* Dynamic theme injected inline */
    }

    .figma-card .grid-lines {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background-size: 40px 40px;
      background-image: linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
                        linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
      pointer-events: none;
    }

    .figma-card .glow-orb {
      position: absolute;
      width: 500px;
      height: 500px;
      border-radius: 50%;
      filter: blur(120px);
      opacity: 0.28;
      pointer-events: none;
    }

    .figma-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: relative;
      z-index: 1;
    }

    .figma-badge {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 10px 22px;
      border-radius: 9999px;
      font-size: 16px;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    .figma-badge-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
    }

    .figma-category {
      font-family: 'JetBrains Mono', monospace;
      color: #94a3b8;
      font-size: 16px;
      font-weight: 600;
    }

    .figma-hero {
      margin: 25px 0;
      position: relative;
      z-index: 1;
    }

    .figma-title {
      font-size: 52px;
      font-weight: 900;
      line-height: 1.18;
      letter-spacing: -0.03em;
      margin-bottom: 18px;
      color: #ffffff;
    }

    .figma-subtitle {
      font-size: 22px;
      line-height: 1.5;
      color: #cbd5e1;
    }

    .figma-cards-list {
      display: flex;
      flex-direction: column;
      gap: 18px;
      margin: 15px 0;
      position: relative;
      z-index: 1;
    }

    .figma-item-card {
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 20px;
      padding: 22px 26px;
      display: flex;
      align-items: flex-start;
      gap: 20px;
      position: relative;
      overflow: hidden;
    }

    .figma-item-num {
      font-family: 'JetBrains Mono', monospace;
      font-size: 20px;
      font-weight: 800;
      width: 44px;
      height: 44px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    .figma-item-heading {
      font-size: 22px;
      font-weight: 800;
      color: #f1f5f9;
      margin-bottom: 6px;
    }

    .figma-item-text {
      font-size: 18px;
      line-height: 1.45;
      color: #94a3b8;
    }

    .figma-pro-tip {
      border-radius: 20px;
      padding: 22px 28px;
      display: flex;
      align-items: center;
      gap: 20px;
      position: relative;
      z-index: 1;
      border: 1px solid rgba(255, 255, 255, 0.12);
    }

    .figma-pro-badge {
      font-size: 15px;
      font-weight: 800;
      padding: 8px 16px;
      border-radius: 10px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      white-space: nowrap;
      color: #fff;
    }

    .figma-pro-text {
      font-size: 19px;
      font-weight: 600;
      color: #e2e8f0;
      line-height: 1.4;
    }

    .figma-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 25px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      position: relative;
      z-index: 1;
    }

    .figma-author-wrap {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .figma-avatar {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
      font-size: 20px;
      color: #0b0f19;
    }

    .figma-author-name {
      font-size: 20px;
      font-weight: 700;
      color: #f8fafc;
    }

    .figma-author-handle {
      font-size: 15px;
      color: #64748b;
    }

    .caption-box {
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px;
      font-size: 14px;
      line-height: 1.6;
      color: #e2e8f0;
      max-height: 220px;
      overflow-y: auto;
      white-space: pre-wrap;
    }

    .actions-row {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }

    .btn {
      flex: 1;
      min-width: 130px;
      padding: 12px 18px;
      border-radius: 10px;
      font-weight: 700;
      font-size: 14px;
      cursor: pointer;
      text-align: center;
      transition: all 0.2s;
      border: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }

    .btn-copy {
      background: rgba(255, 255, 255, 0.08);
      color: #f8fafc;
      border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .btn-copy:hover { background: rgba(255, 255, 255, 0.16); }

    .btn-download {
      background: linear-gradient(135deg, #2563eb, #38bdf8);
      color: #fff;
    }
    .btn-download:hover { opacity: 0.9; }

    .toast-active {
      background: #10b981 !important;
      color: #fff !important;
    }
  </style>
</head>
<body>
  <div class="container">
    <!-- Header -->
    <div class="header">
      <div class="brand">
        <div class="logo-badge">SEO</div>
        <div class="title-group">
          <h1>LinkedIn Daily SEO Post Agent</h1>
          <p>24/7 Cloud Automated • Dynamic Colors • Hinglish</p>
        </div>
      </div>
      <div class="live-badge">
        <span class="live-dot"></span>
        <span>24/7 Live Agent Active</span>
      </div>
    </div>

    <div class="theme-banner">
      <div>🎨 <strong>Dynamic Daily Theme Active:</strong> Har din visual colors automatically change hote hain!</div>
      <div>📅 Date: <strong>{{ date }}</strong></div>
    </div>

    <!-- Posts Grid -->
    <div class="posts-grid">
      {% for post in posts %}
      <div class="post-panel">
        <div class="panel-header">
          <div class="panel-title" style="color: {{ post.theme.accent }};">{{ post.name }}</div>
          <div class="theme-chip">{{ post.theme.name }} Theme</div>
        </div>

        <!-- Render Container (Responsive Scaled Preview) -->
        <div class="render-wrapper" id="wrapper-{{ post.id }}">
          <div class="figma-card" id="card-{{ post.id }}" style="
            background-color: {{ post.theme.bg }};
            background-image: 
              radial-gradient(circle at 15% 15%, {{ post.theme.glow }} 0%, transparent 40%),
              radial-gradient(circle at 85% 85%, {{ post.theme.glow }} 0%, transparent 40%);
          ">
            <div class="grid-lines"></div>
            <div class="glow-orb" style="top: -100px; right: -100px; background: {{ post.theme.secondary }};"></div>
            <div class="glow-orb" style="bottom: -100px; left: -100px; background: {{ post.theme.accent }};"></div>

            <!-- Top Header -->
            <div class="figma-header">
              <div class="figma-badge" style="
                background: {{ post.theme.badge_bg }};
                border: 1px solid {{ post.theme.badge_border }};
                color: {{ post.theme.primary }};
                box-shadow: 0 0 20px {{ post.theme.glow }};
              ">
                <span class="figma-badge-dot" style="background: {{ post.theme.primary }}; box-shadow: 0 0 10px {{ post.theme.primary }};"></span>
                <span>{{ post.data.badge }}</span>
              </div>
              <div class="figma-category">{{ post.data.category }}</div>
            </div>

            <!-- Main Hero Title -->
            <div class="figma-hero">
              <h1 class="figma-title">{{ post.data.title | safe }}</h1>
              <p class="figma-subtitle">{{ post.data.subtitle }}</p>
            </div>

            <!-- 3 Cards -->
            <div class="figma-cards-list">
              {% for card in post.data.cards %}
              <div class="figma-item-card" style="background: {{ post.theme.card_bg }};">
                <div style="position: absolute; left: 0; top: 0; width: 4px; height: 100%; background: linear-gradient(180deg, {{ post.theme.primary }}, {{ post.theme.secondary }});"></div>
                <div class="figma-item-num" style="
                  color: {{ post.theme.primary }};
                  background: {{ post.theme.badge_bg }};
                  border: 1px solid {{ post.theme.badge_border }};
                ">{{ card.num }}</div>
                <div>
                  <div class="figma-item-heading">{{ card.heading }}</div>
                  <div class="figma-item-text">{{ card.text }}</div>
                </div>
              </div>
              {% endfor %}
            </div>

            <!-- Pro Tip -->
            <div class="figma-pro-tip" style="background: {{ post.theme.card_bg }}; border-color: {{ post.theme.badge_border }};">
              <div class="figma-pro-badge" style="background: {{ post.theme.secondary }};">Golden Rule</div>
              <div class="figma-pro-text">"{{ post.data.pro_tip }}"</div>
            </div>

            <!-- Footer -->
            <div class="figma-footer">
              <div class="figma-author-wrap">
                <div class="figma-avatar" style="background: linear-gradient(135deg, {{ post.theme.primary }}, {{ post.theme.secondary }});">SEO</div>
                <div>
                  <div class="figma-author-name">Achhar Sharma</div>
                  <div class="figma-author-handle">Daily SEO Growth in Hinglish</div>
                </div>
              </div>
              <div style="font-size: 16px; color: {{ post.theme.primary }}; font-weight: 700;">Save for later 📌</div>
            </div>

          </div>
        </div>

        <!-- Caption Box -->
        <div class="caption-box" id="caption-{{ post.id }}">{{ post.data.caption }}</div>

        <!-- Action Buttons -->
        <div class="actions-row">
          <button class="btn btn-copy" onclick="copyCaption('caption-{{ post.id }}', this)">
            📋 Copy Caption
          </button>
          <button class="btn btn-download" onclick="downloadImage('card-{{ post.id }}', 'seo_post_{{ post.id }}_{{ date }}.png', this)">
            💾 Download HD Image
          </button>
        </div>

      </div>
      {% endfor %}
    </div>

  </div>

  <script>
    // Responsive Scaler for 1080x1350 Figma card to fit mobile & desktop preview perfectly
    function rescaleCards() {
      [1, 2].forEach(id => {
        const wrapper = document.getElementById('wrapper-' + id);
        const card = document.getElementById('card-' + id);
        if (wrapper && card) {
          const wrapperWidth = wrapper.clientWidth;
          const scale = wrapperWidth / 1080;
          card.style.transform = `scale(${scale})`;
          wrapper.style.height = (1350 * scale) + 'px';
        }
      });
    }

    window.addEventListener('resize', rescaleCards);
    window.addEventListener('DOMContentLoaded', rescaleCards);

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

    function downloadImage(cardId, fileName, btn) {
      const card = document.getElementById(cardId);
      const originalTransform = card.style.transform;
      const originalText = btn.innerHTML;
      btn.innerHTML = "⏳ Rendering 4K...";
      btn.disabled = true;

      // Reset transform temporarily to capture pure 1080x1350 pixel canvas
      card.style.transform = 'none';

      html2canvas(card, {
        width: 1080,
        height: 1350,
        scale: 2, // 2x Retina Resolution
        useCORS: true,
        backgroundColor: null
      }).then(canvas => {
        card.style.transform = originalTransform;
        btn.innerHTML = originalText;
        btn.disabled = false;

        const link = document.createElement('a');
        link.download = fileName;
        link.href = canvas.toDataURL('image/png');
        link.click();
      }).catch(err => {
        card.style.transform = originalTransform;
        btn.innerHTML = originalText;
        btn.disabled = false;
        alert('Export failed, please try again.');
      });
    }
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    posts = get_posts_for_today()
    return render_template_string(HTML_TEMPLATE, date=today_str, posts=posts)

@app.route("/api/today")
def api_today():
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    return jsonify({
        "date": today_str,
        "posts": get_posts_for_today()
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
