# 📱 SocialMind — Agentic AI Social Media Assistant

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)](https://flask.palletsprojects.com/)
[![IBM watsonx.ai](https://img.shields.io/badge/IBM-watsonx.ai-054ADA?logo=ibm)](https://www.ibm.com/watsonx)
[![IBM Granite](https://img.shields.io/badge/IBM%20Granite-3.3--8B-054ADA?logo=ibm)](https://www.ibm.com/granite)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> A **web-based Agentic AI Social Media Assistant** powered by **IBM Granite LLM** (`ibm/granite-3-3-8b-instruct`) via **IBM watsonx.ai** that generates personalised social media posts, campaign strategies, content calendars, trend analysis, and an AI-powered chatbot — all with built-in ethical AI guardrails, human approval workflows, sentiment analysis, image input support, and an interactive analytics dashboard.

---

## 📸 Features at a Glance

| Tab | Feature |
|---|---|
| ✍️ **Content Generator** | Brand details → 3 AI-generated posts, hashtags, CTAs, engagement estimates; supports image description & upload |
| 📅 **Campaign Planner** | Full campaign strategy with content pillars, KPIs, and a 2-week auto-generated posting calendar |
| 📈 **Trend Analyzer** | Identify industry trends, audience behaviour, competitor patterns, and opportunities with `[TREND]`/`[PREDICTED]` labels |
| 🎭 **Sentiment Lab** | Standalone sentiment analysis with SVG score ring, animated bars, keyword detection, and actionable recommendations |
| 💬 **AI Chatbot** | Context-aware social media Q&A with brand context and suggested question chips |
| 📊 **Analytics Dashboard** | SVG line chart, donut chart, horizontal bar charts: engagement rates, sentiment, post types, reach trends, top hashtags |
| 🛡️ **Ethics & About** | Detailed ethical AI guardrails, data privacy policy, API reference, and tech stack |

---

## 🏗️ Project Structure

```
social_media_ai/
├── app.py                  # Flask backend + IBM Granite LLM agentic logic
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules
├── README.md               # This file
└── templates/
    └── index.html          # Single-page web UI (7 tabs, dark theme, fully responsive)
```

---

## 🧠 Architecture

```
Browser (index.html)
      │
      │  HTTP POST/GET (JSON)
      ▼
Flask Backend (app.py)
      │
      ├── /api/generate_posts  ──► Hashtag Tool + Engagement Tool ──► Granite Prompt ──► Posts
      ├── /api/analyze_image   ──► Image Analysis Prompt          ──► Granite Answer  ──► Strategy
      ├── /api/campaign        ──► Calendar Tool                  ──► Granite Prompt ──► Strategy
      ├── /api/trends          ──► Sentiment Tool                 ──► Granite Prompt ──► Trends
      ├── /api/chat            ──► Context-aware Q&A prompt       ──► Granite Answer
      ├── /api/sentiment       ──► Rule-based Sentiment Analyzer  ──► Score + Label
      ├── /api/hashtags        ──► Hashtag Generator              ──► Tag List
      ├── /api/approve_post    ──► Human Approval Workflow        ──► approved/rejected
      └── /api/analytics       ──► Simulated Analytics Data       ──► Dashboard JSON
                                            │
                                            ▼
                                IBM watsonx.ai (au-syd)
                                ibm/granite-3-3-8b-instruct
```

---

## 🤖 Agentic Tools

| Tool | Function | Trigger |
|---|---|---|
| **Hashtag Generator** | Platform + goal + industry optimised hashtags | Auto on post generation & `/api/hashtags` |
| **Content Calendar** | 2-week posting schedule with best posting times | Auto on campaign planning |
| **Sentiment Analyzer** | Rule-based positive/negative/neutral scoring | Competitor analysis, Sentiment Lab & `/api/sentiment` |
| **Engagement Estimator** | Platform-benchmark engagement predictions | Auto on post generation |
| **Image Analyst** | Suitability score, captions, hashtags for uploaded images | `/api/analyze_image` |
| **Post Generator** | 3 personalised AI posts with CTAs | `POST /api/generate_posts` |
| **Campaign Strategist** | Full strategy with KPIs and content pillars | `POST /api/campaign` |
| **Trend Analyst** | Industry/platform/region trend report | `POST /api/trends` |
| **Q&A Chatbot** | Context-aware social media assistant | `POST /api/chat` |

---

## ⚙️ Prerequisites

- Python **3.9** or higher
- `pip` package manager
- An active **IBM Cloud** account with **IBM watsonx.ai** provisioned
  - A valid **Project ID**
  - A valid **API Key**
  - Access to `ibm/granite-3-3-8b-instruct` model

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/swatik31-hub/Social-Media-Agent-.git
cd Social-Media-Agent-
```

### 2. (Optional but recommended) Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure IBM watsonx.ai credentials

Open [`app.py`](app.py) and update the credentials section (lines 16–19):

```python
PROJECT_ID   = "your-project-id"
API_KEY      = "your-api-key"
ENDPOINT_URL = "https://au-syd.ml.cloud.ibm.com"   # change region if needed
MODEL_ID     = "ibm/granite-3-3-8b-instruct"
```

> ⚠️ **Security tip:** For production use, store credentials as environment variables:
> ```bash
> export WATSONX_API_KEY="your-key"
> export WATSONX_PROJECT_ID="your-project-id"
> ```
> Then read them in `app.py` with `os.getenv("WATSONX_API_KEY")`.

### 5. Run the application

```bash
python app.py
```

### 6. Open in your browser

```
http://localhost:5001
```

---

## 🔑 IBM watsonx.ai Configuration

| Setting | Value |
|---|---|
| Endpoint URL | `https://au-syd.ml.cloud.ibm.com` |
| Model | `ibm/granite-3-3-8b-instruct` |
| Max New Tokens | 1500 |
| Min New Tokens | 60 |
| Temperature | 0.75 |
| Top-P | 0.92 |
| Repetition Penalty | 1.1 |

---

## 🖼️ Image Input Support

The Content Generator supports two modes of image input:

1. **Describe Image** — Type a description of the image you intend to post (e.g. *"A vibrant product flatlay with coffee and laptop on a wooden desk"*). Granite will tailor posts for that visual.
2. **Upload Image** — Upload a JPG, PNG, or WebP file via click or drag-and-drop. The filename auto-populates the description field.

Click **🔍 Analyze Image** to get:
- Image suitability score (1–10) for the chosen platform
- Suggested caption and hashtags
- Visual enhancement tips
- Content repurposing ideas for other platforms
- Best posting time recommendation

---

## 🛡️ Ethical AI Guardrails

SocialMind is built with responsible AI at its core:

| Guardrail | Implementation |
|---|---|
| **Input Safety Screening** | Regex scan of all user inputs — blocks hate speech, spam, deception, NSFW, harassment |
| **Output Validation** | Regex scan of all AI outputs before display in browser |
| **Human Approval Workflow** | Every generated post is held as `pending` — must be explicitly approved/rejected before publishing |
| **Prediction Labelling** | AI trend predictions clearly marked `[PREDICTED]`; confirmed trends marked `[TREND]` |
| **HAM Principles** | Every system prompt enforces: **H**elpful, **A**ccurate, **M**indful |
| **Data Privacy** | No user data persisted beyond in-memory session storage; uploaded images processed in-browser only |
| **Mandatory AI Disclosure** | AI-generated disclaimer auto-appended to all content |
| **Off-topic Blocking** | Chatbot politely redirects non-social-media queries |
| **Content Category Blocking** | 7 blocked categories: hate speech, misinformation, spam/phishing, threats/bullying, explicit content, plagiarism, manipulation |
| **Secure API Integration** | IBM watsonx.ai credentials stored server-side only, never exposed to client |

---

## 🗂️ API Reference

### `POST /api/generate_posts`
Generates 3 personalised social media posts.

**Request body:**
```json
{
  "brand_name": "TechVibe",
  "industry": "E-commerce",
  "platform": "Instagram",
  "tone": "Casual & Friendly",
  "target_audience": "Young professionals aged 25-35",
  "goal": "Brand Awareness",
  "audience_size": 15000,
  "competitors": "Competitor A, Competitor B",
  "image_description": "A vibrant product flatlay on a wooden desk"
}
```

**Response:**
```json
{
  "posts": "## Social Media Posts for TechVibe\n...",
  "hashtags": ["#TechVibe", "#Ecommerce", "#InstagramMarketing"],
  "engagement": {
    "estimated_likes": 675,
    "estimated_reach": 22000,
    "engagement_rate": "5.12%"
  },
  "post_id": "post_1718000000",
  "status": "pending_approval"
}
```

---

### `POST /api/analyze_image`
Analyzes an image description for social media content strategy.

**Request body:**
```json
{
  "image_description": "Sunset over city skyline with product placement",
  "brand_name": "TechVibe",
  "industry": "E-commerce",
  "platform": "Instagram",
  "goal": "Brand Awareness"
}
```

**Response:**
```json
{
  "analysis": "## Image Content Analysis\n1. Suitability Score: 8/10..."
}
```

---

### `POST /api/campaign`
Generates a full campaign strategy + content calendar.

**Request body:**
```json
{
  "brand_name": "GreenLeaf Co.",
  "industry": "Sustainability",
  "platforms": "Instagram, LinkedIn, Facebook",
  "goal": "Brand Awareness",
  "period": "2 weeks",
  "target_audience": "Eco-conscious millennials",
  "budget": "$500 – $2,000"
}
```

---

### `POST /api/trends`
Analyzes social media trends for an industry/platform.

**Request body:**
```json
{
  "industry": "Fashion",
  "platform": "Instagram",
  "region": "Asia Pacific",
  "competitor_posts": "Optional competitor post samples for sentiment analysis..."
}
```

---

### `POST /api/chat`
Answers social media questions with optional brand context.

**Request body:**
```json
{
  "query": "What are the best times to post on Instagram?",
  "brand_context": {
    "brand_name": "TechVibe",
    "industry": "E-commerce",
    "platform": "Instagram",
    "goal": "Engagement"
  }
}
```

---

### `POST /api/approve_post`
Approves or rejects a pending generated post.

**Request body:**
```json
{ "post_id": "post_1718000000", "action": "approve" }
```

**Response:**
```json
{ "post_id": "post_1718000000", "status": "approved", "message": "Post has been approved." }
```

---

### `POST /api/sentiment`
Analyzes text sentiment using rule-based keyword analysis.

**Request body:**
```json
{ "text": "This product is amazing! Best purchase ever." }
```

**Response:**
```json
{
  "sentiment": "Positive 😊",
  "positive_score": 3,
  "negative_score": 0,
  "overall_score": 100
}
```

---

### `POST /api/hashtags`
Generates platform-optimised hashtags.

**Request body:**
```json
{
  "brand": "TechVibe",
  "industry": "E-commerce",
  "platform": "Instagram",
  "goal": "brand awareness"
}
```

---

### `GET /api/analytics`
Returns analytics dashboard data (simulated illustrative figures).

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.9+, Flask 3.x |
| AI / LLM | IBM watsonx.ai — `ibm/granite-3-3-8b-instruct` |
| SDK | `ibm-watsonx-ai >= 1.1.2` |
| Frontend | HTML5, CSS3, Vanilla JavaScript (dark theme, 7 tabs, fully responsive) |
| Charts | Custom inline SVG — line chart, donut chart, horizontal bar charts |
| Image Input | Browser FileReader API (in-browser preview, no server upload) |
| Deployment | Local / Any Python-compatible host (Render, Railway, Heroku, IBM Code Engine) |

---

## 🌐 Deployment Options

### Local
```bash
python app.py
# Visit http://localhost:5001
```

### Gunicorn (production)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### IBM Code Engine / Cloud Foundry
Set environment variables for credentials and use a `Procfile`:
```
web: gunicorn app:app
```

---

## ⚠️ Disclaimer

> This application is powered by AI and is intended for **creative and strategic guidance only**.
> AI-generated social media content should always be reviewed by a human before publishing.
> Engagement and analytics figures are **simulated estimates** — validate with your real platform analytics (Meta Business Suite, Twitter Analytics, LinkedIn Analytics).
> Trend predictions are clearly labelled `[PREDICTED]` and may not reflect actual market conditions.
> **Never publish AI-generated content without human review and approval.**

---

## 📄 License

This project is licensed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

## 🙏 Acknowledgements

- [IBM watsonx.ai](https://www.ibm.com/watsonx) — AI platform
- [IBM Granite](https://www.ibm.com/granite) — Open-source enterprise LLM
- [Flask](https://flask.palletsprojects.com/) — Python web framework
- [IBM Cloud](https://cloud.ibm.com/) — Cloud infrastructure
