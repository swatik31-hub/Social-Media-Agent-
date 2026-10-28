# 📱 SocialMind — Agentic AI Social Media Assistant

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)](https://flask.palletsprojects.com/)
[![IBM watsonx.ai](https://img.shields.io/badge/IBM-watsonx.ai-054ADA?logo=ibm)](https://www.ibm.com/watsonx)
[![IBM Granite](https://img.shields.io/badge/IBM-Granite%20LLM-054ADA?logo=ibm)](https://www.ibm.com/granite)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> A **web-based Agentic AI Social Media Assistant** powered by **IBM Granite LLM** (via **IBM watsonx.ai**) that generates personalised social media posts, campaign strategies, content calendars, trend analysis, and an AI-powered chatbot — all with built-in ethical AI guardrails, human approval workflows, and an interactive analytics dashboard.

---

## 📸 Features at a Glance

| Tab | Feature |
|---|---|
| ✍️ **Content Generator** | Enter brand details → get 3 personalised AI-generated posts, hashtags, CTAs & engagement estimates |
| 📅 **Campaign Planner** | Full campaign strategy with content pillars, KPIs, and a 2-week auto-generated posting calendar |
| 📈 **Trend Analyzer** | Identify industry trends, audience behaviour, competitor patterns, and opportunities |
| 💬 **AI Chatbot** | Context-aware social media Q&A with suggested question chips |
| 📊 **Analytics Dashboard** | Interactive charts: engagement rates, sentiment, post types, reach trends, top hashtags |
| ℹ️ **About** | Feature overview, ethical guardrails summary, API reference, tech stack |

---

## 🏗️ Project Structure

```
social_media_ai/
├── app.py                  # Flask backend + IBM Granite LLM agentic logic
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules
├── README.md               # This file
└── templates/
    └── index.html          # Single-page web UI (6 tabs, dark theme, fully responsive)
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
      ├── /api/campaign        ──► Calendar Tool                  ──► Granite Prompt ──► Strategy
      ├── /api/trends          ──► Sentiment Tool                 ──► Granite Prompt ──► Trends
      ├── /api/chat            ──► Context-aware Q&A prompt       ──► Granite Answer
      ├── /api/sentiment       ──► Rule-based Sentiment Analyzer  ──► Score + Label
      ├── /api/hashtags        ──► Hashtag Generator              ──► Tag List
      ├── /api/approve_post    ──► Human Approval Workflow        ──► approved/rejected
      └── /api/analytics       ──► Simulated Analytics Data       ──► Dashboard JSON
                                            │
                                            ▼
                                IBM watsonx.ai
                                ibm/granite-3-3-8b-instruct
```

---

## 🤖 Agentic Tools

| Tool | Function | Trigger |
|---|---|---|
| **Hashtag Generator** | Platform + goal + industry optimised hashtags | Auto-runs on post generation & `/api/hashtags` |
| **Content Calendar** | 2-week posting schedule with best times | Auto-runs on campaign planning |
| **Sentiment Analyzer** | Rule-based positive/negative/neutral scoring | Competitor posts analysis & `/api/sentiment` |
| **Engagement Estimator** | Platform-benchmark engagement predictions | Auto-runs on post generation |
| **Post Generator** | 3 personalised AI posts with CTAs | `POST /api/generate_posts` |
| **Campaign Strategist** | Full strategy with KPIs and content pillars | `POST /api/campaign` |
| **Trend Analyst** | Industry/platform/region trend report | `POST /api/trends` |
| **Q&A Chatbot** | Context-aware social media assistant | `POST /api/chat` |

---

## ⚙️ Prerequisites

- Python **3.9** or higher
- `pip` package manager
- An active **IBM watsonx.ai** account with:
  - A valid **Project ID**
  - A valid **API Key**
  - Access to `ibm/granite-3-3-8b-instruct`

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/swatik31-hub/Project_Nutriant.git
cd Project_Nutriant/social_media_ai
```

### 2. (Optional) Create a virtual environment

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

Open [`app.py`](app.py) and update the credentials section (lines 14–17):

```python
PROJECT_ID   = "your-project-id"
API_KEY      = "your-api-key"
ENDPOINT_URL = "https://au-syd.ml.cloud.ibm.com"   # change region if needed
MODEL_ID     = "ibm/granite-3-3-8b-instruct"
```

> ⚠️ **Security tip:** For production, use environment variables instead of hardcoding credentials.
> Set `WATSONX_API_KEY`, `WATSONX_PROJECT_ID` as env vars and read them with `os.getenv()`.

### 5. Run the application

```bash
python app.py
```

### 6. Open in browser

```
http://localhost:5001
```

---

## 🔑 IBM watsonx.ai Configuration

| Setting | Value |
|---|---|
| Endpoint URL | `https://au-syd.ml.cloud.ibm.com` |
| Model | `ibm/granite-3-3-8b-instruct` |
| Max New Tokens | 1200 |
| Temperature | 0.75 |
| Top-P | 0.92 |
| Repetition Penalty | 1.1 |

---

## 🛡️ Ethical AI Guardrails

SocialMind is built with responsible AI principles at its core:

| Guardrail | Implementation |
|---|---|
| **Input Safety** | Regex scan of all user inputs — blocks hate speech, spam, deception, NSFW content |
| **Output Safety** | Regex scan of all AI outputs before displaying in browser |
| **Human Approval** | Every generated post must be explicitly approved/rejected before publishing |
| **Prediction Labels** | AI trend predictions clearly marked `[PREDICTED]`, confirmed trends marked `[TREND]` |
| **HAM Principle** | Every system prompt enforces: **H**elpful, **A**ccurate, **M**indful |
| **Data Privacy** | No user data persisted beyond in-memory session storage |
| **AI Disclaimer** | AI-generated label auto-appended to all content |
| **Off-topic Blocking** | Chatbot politely redirects non-social-media queries |
| **Scope Limiting** | Prompts explicitly forbid harmful, deceptive, or plagiarised content |

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
  "competitors": "Competitor A, Competitor B"
}
```

**Response:**
```json
{
  "posts": "## Social Media Posts for TechVibe\n...",
  "hashtags": ["#TechVibe", "#Ecommerce", "#InstagramMarketing", "..."],
  "engagement": { "estimated_likes": 675, "estimated_reach": 22000, "engagement_rate": "5.12%" },
  "post_id": "post_1718000000",
  "status": "pending_approval"
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
  "competitor_posts": "Optional competitor post samples..."
}
```

---

### `POST /api/chat`
Answers social media questions with optional brand context.

**Request body:**
```json
{
  "query": "What are the best times to post on Instagram?",
  "brand_context": { "brand_name": "TechVibe", "industry": "E-commerce" }
}
```

---

### `POST /api/approve_post`
Approves or rejects a pending generated post.

**Request body:**
```json
{ "post_id": "post_1718000000", "action": "approve" }
```

---

### `POST /api/sentiment`
Analyzes text sentiment.

**Request body:**
```json
{ "text": "This product is amazing! Best purchase ever." }
```

**Response:**
```json
{ "sentiment": "Positive 😊", "positive_score": 3, "negative_score": 0, "overall_score": 100 }
```

---

### `GET /api/analytics`
Returns dashboard analytics data (simulated).

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.9+, Flask 3.x |
| AI / LLM | IBM watsonx.ai — `ibm/granite-3-3-8b-instruct` |
| SDK | `ibm-watsonx-ai` |
| Frontend | HTML5, CSS3, Vanilla JavaScript (dark theme, no framework) |
| Analytics | Custom SVG-free bar chart rendering |
| Deployment | Local / Any Python-compatible host |

---

## ⚠️ Disclaimer

> This application is powered by AI and is intended for **creative and strategic guidance only**.
> AI-generated social media content should always be reviewed by a human before publishing.
> Engagement and analytics figures are **simulated estimates** — validate with your real platform analytics.
> Trend predictions are clearly labelled `[PREDICTED]` and may not reflect actual market conditions.
> **Never publish AI-generated content without human review.**

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🙏 Acknowledgements

- [IBM watsonx.ai](https://www.ibm.com/watsonx) for the AI platform
- [IBM Granite](https://www.ibm.com/granite) for the language model
- [Flask](https://flask.palletsprojects.com/) for the web framework
