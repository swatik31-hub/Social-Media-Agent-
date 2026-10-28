"""
SocialMind — Agentic AI Social Media Assistant
Powered by IBM Granite LLM via IBM watsonx.ai
"""

from flask import Flask, request, jsonify, render_template
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
import json, re, random
from datetime import datetime, timedelta

app = Flask(__name__)

# ── IBM watsonx.ai Configuration ──────────────────────────────────────────────
PROJECT_ID   = "9384c26e-2697-469b-83aa-a9e78bd2d1a8"
API_KEY      = "hX73vEDUS0ovIQgfuXdt4AnPf-tqXpOMEyD-tvx9pLAr"
ENDPOINT_URL = "https://au-syd.ml.cloud.ibm.com"
MODEL_ID     = "meta-llama/llama-3-3-70b-instruct"

credentials = Credentials(url=ENDPOINT_URL, api_key=API_KEY)
client      = APIClient(credentials=credentials, project_id=PROJECT_ID)

generate_params = {
    GenParams.MAX_NEW_TOKENS:      1200,
    GenParams.MIN_NEW_TOKENS:      60,
    GenParams.TEMPERATURE:         0.75,
    GenParams.TOP_P:               0.92,
    GenParams.REPETITION_PENALTY:  1.1,
}

model = ModelInference(
    model_id=MODEL_ID,
    api_client=client,
    params=generate_params,
    project_id=PROJECT_ID,
)

# ── Ethical AI Guardrails ──────────────────────────────────────────────────────
HARMFUL_PATTERNS = [
    r"\b(hate speech|racism|sexism|discriminat)\b",
    r"\b(fake news|misinformation|deepfake)\b",
    r"\b(spam|scam|phishing|clickbait)\b",
    r"\b(violence|threaten|harass|bully)\b",
    r"\b(explicit|adult content|nsfw|pornograph)\b",
    r"\b(plagiari|copyright infringement)\b",
    r"\b(manipulat(e|ion)|deceiv|mislead)\b",
]

PENDING_POSTS = {}   # post_id -> post content awaiting human approval

def guardrail_check(text: str) -> bool:
    """Returns True if text contains harmful / unethical content."""
    lower = text.lower()
    return any(re.search(p, lower) for p in HARMFUL_PATTERNS)

ETHICS_DISCLAIMER = (
    "\n\n---\n"
    "⚠️ **AI Disclaimer:** This content is AI-generated for informational and "
    "creative purposes. Always review AI-generated posts before publishing. "
    "Actual engagement metrics are illustrative — validate with your real "
    "analytics platform. SocialMind does not guarantee campaign outcomes."
)

# ── Agentic Tool 1: Hashtag Generator ─────────────────────────────────────────
def generate_hashtags(brand: str, industry: str, platform: str, goal: str) -> list:
    """Agentic tool — generates relevant hashtags based on brand context."""
    base_tags = {
        "instagram": ["#Reels", "#InstagramMarketing", "#VisualContent", "#BrandStory"],
        "twitter":   ["#Marketing", "#BrandVoice", "#ContentMarketing", "#GrowthHacking"],
        "linkedin":  ["#B2B", "#ProfessionalDevelopment", "#ThoughtLeadership", "#IndustryInsights"],
        "facebook":  ["#FacebookMarketing", "#CommunityBuilding", "#SocialMedia", "#Engagement"],
        "tiktok":    ["#TikTokMarketing", "#ViralContent", "#TrendingNow", "#ForYouPage"],
    }
    goal_tags = {
        "brand awareness": ["#BrandAwareness", "#GetNoticed", "#NewBrand"],
        "lead generation": ["#LeadGen", "#BusinessGrowth", "#CallToAction"],
        "engagement":      ["#EngageWithUs", "#CommunityFirst", "#AskMeAnything"],
        "sales":           ["#ShopNow", "#LimitedOffer", "#ExclusiveDeal"],
        "education":       ["#DidYouKnow", "#LearnSomethingNew", "#Tips"],
    }
    plat_key  = platform.lower().split()[0] if platform else "instagram"
    goal_key  = goal.lower() if goal else "brand awareness"
    brand_tag = f"#{re.sub(r'[^a-zA-Z0-9]', '', brand)}" if brand else "#Brand"
    ind_tag   = f"#{re.sub(r'[^a-zA-Z0-9]', '', industry)}" if industry else "#Industry"
    tags = (
        [brand_tag, ind_tag]
        + base_tags.get(plat_key, base_tags["instagram"])
        + goal_tags.get(goal_key, goal_tags["brand awareness"])
    )
    return list(dict.fromkeys(tags))[:15]

# ── Agentic Tool 2: Content Calendar Generator ────────────────────────────────
def generate_content_calendar(brand: str, platforms: list, goal: str, weeks: int = 2) -> list:
    """Agentic tool — generates a posting schedule calendar."""
    content_types = [
        "Behind-the-scenes post", "Product spotlight", "Customer testimonial",
        "Educational tip", "Trending topic engagement", "Poll / Question",
        "Infographic share", "User-generated content feature", "Team introduction",
        "Industry news commentary", "Promotional offer", "Milestone celebration",
    ]
    best_times = {
        "instagram": "9:00 AM – 11:00 AM",
        "twitter":   "8:00 AM – 10:00 AM",
        "linkedin":  "7:30 AM – 9:00 AM (Tue–Thu)",
        "facebook":  "1:00 PM – 3:00 PM",
        "tiktok":    "7:00 PM – 9:00 PM",
    }
    calendar = []
    today = datetime.today()
    day_offset = 0
    for week in range(1, weeks + 1):
        for platform in (platforms or ["Instagram"]):
            for _ in range(3):
                day_offset += 1
                post_date = today + timedelta(days=day_offset)
                plat_key  = platform.lower().split()[0]
                calendar.append({
                    "week":     week,
                    "date":     post_date.strftime("%a, %d %b %Y"),
                    "platform": platform,
                    "type":     random.choice(content_types),
                    "time":     best_times.get(plat_key, "10:00 AM"),
                    "goal":     goal or "Brand Awareness",
                })
    return calendar

# ── Agentic Tool 3: Sentiment Analyzer (rule-based) ───────────────────────────
POSITIVE_WORDS = [
    "love", "great", "amazing", "excellent", "awesome", "fantastic", "wonderful",
    "best", "brilliant", "superb", "outstanding", "perfect", "happy", "excited",
]
NEGATIVE_WORDS = [
    "hate", "terrible", "awful", "bad", "worst", "horrible", "poor", "disappointing",
    "useless", "failure", "boring", "ugly", "sad", "angry", "frustrat",
]

def analyze_sentiment(text: str) -> dict:
    """Agentic tool — rule-based sentiment analysis."""
    lower = text.lower()
    pos = sum(1 for w in POSITIVE_WORDS if w in lower)
    neg = sum(1 for w in NEGATIVE_WORDS if w in lower)
    total = pos + neg or 1
    score = round((pos / total) * 100)
    if score >= 60:
        label = "Positive 😊"
    elif score >= 40:
        label = "Neutral 😐"
    else:
        label = "Negative 😞"
    return {
        "sentiment":      label,
        "positive_score": pos,
        "negative_score": neg,
        "overall_score":  score,
    }

# ── Agentic Tool 4: Engagement Estimator ──────────────────────────────────────
def estimate_engagement(platform: str, post_type: str, audience_size: int) -> dict:
    """Agentic tool — estimates engagement based on platform benchmarks."""
    benchmarks = {
        "instagram": {"likes": 0.045, "comments": 0.008, "shares": 0.003},
        "twitter":   {"likes": 0.025, "comments": 0.005, "shares": 0.012},
        "linkedin":  {"likes": 0.030, "comments": 0.010, "shares": 0.006},
        "facebook":  {"likes": 0.020, "comments": 0.004, "shares": 0.005},
        "tiktok":    {"likes": 0.080, "comments": 0.015, "shares": 0.020},
    }
    plat_key = platform.lower().split()[0] if platform else "instagram"
    rates    = benchmarks.get(plat_key, benchmarks["instagram"])
    base     = audience_size or 10000
    noise    = lambda r: round(base * r * random.uniform(0.8, 1.3))
    likes    = noise(rates["likes"])
    comments = noise(rates["comments"])
    shares   = noise(rates["shares"])
    reach    = round(base * random.uniform(1.1, 2.5))
    return {
        "platform":        platform,
        "estimated_likes": likes,
        "estimated_comments": comments,
        "estimated_shares":   shares,
        "estimated_reach":    reach,
        "engagement_rate":    f"{round((likes + comments + shares) / base * 100, 2)}%",
        "note":               "⚠️ Estimated figures — validate with real analytics.",
    }

# ── Prompt Builders ────────────────────────────────────────────────────────────
def build_post_prompt(brand: dict, hashtags: list) -> str:
    tags_str = " ".join(hashtags[:10])
    return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are SocialMind, an expert AI social media strategist.
You follow HAM principles: Helpful, Accurate, Mindful.
You craft engaging, ethical, brand-safe social media content.
Never produce hateful, deceptive, or misleading content.
<|eot_id|><|start_header_id|>user<|end_header_id|>
Create 3 unique, engaging social media posts for the following brand:

- Brand Name     : {brand.get('brand_name', 'Brand')}
- Industry       : {brand.get('industry', 'General')}
- Target Audience: {brand.get('target_audience', 'General public')}
- Platform       : {brand.get('platform', 'Instagram')}
- Brand Tone     : {brand.get('tone', 'Professional')}
- Campaign Goal  : {brand.get('goal', 'Brand Awareness')}
- Competitor Info: {brand.get('competitors', 'Not specified')}
- Suggested Tags : {tags_str}

For each post provide:
1. Post caption (engaging, platform-optimised)
2. Relevant hashtags (10–15)
3. Call-to-action (CTA)
4. Best posting time recommendation
5. Content type (image/video/carousel/story suggestion)

Make each post distinct in style. Be creative, brand-consistent, and audience-aware.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
## Social Media Posts for {brand.get('brand_name', 'Brand')}
"""


def build_campaign_prompt(brand: dict, calendar: list) -> str:
    cal_preview = json.dumps(calendar[:6], indent=2)
    return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are SocialMind, a professional AI campaign strategist.
Follow HAM principles. Be data-informed, ethical, and actionable.
<|eot_id|><|start_header_id|>user<|end_header_id|>
Create a detailed social media campaign strategy for:

- Brand          : {brand.get('brand_name', 'Brand')}
- Industry       : {brand.get('industry', 'General')}
- Target Audience: {brand.get('target_audience', 'General')}
- Platforms      : {brand.get('platforms', 'Instagram, LinkedIn')}
- Campaign Goal  : {brand.get('goal', 'Brand Awareness')}
- Campaign Period : {brand.get('period', '2 weeks')}
- Budget Range   : {brand.get('budget', 'Not specified')}
- Competitors    : {brand.get('competitors', 'None specified')}

Content Calendar Preview:
{cal_preview}

Provide:
1. Campaign Overview & Objectives
2. Content Pillars (3-4 themes)
3. Platform-Specific Strategy
4. KPIs & Success Metrics
5. Competitor Differentiation Strategy
6. Risk Mitigation & Ethical Guidelines
7. Weekly Action Plan

Be thorough, strategic, and actionable.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
## Campaign Strategy for {brand.get('brand_name', 'Brand')}
"""


def build_trend_prompt(industry: str, platform: str, region: str) -> str:
    return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are SocialMind, an AI social media trend analyst.
Follow HAM principles. Clearly distinguish actual trends from AI predictions.
Label predictions with [PREDICTED] and established trends with [TREND].
<|eot_id|><|start_header_id|>user<|end_header_id|>
Analyze current social media trends for:
- Industry  : {industry or 'General'}
- Platform  : {platform or 'All platforms'}
- Region    : {region or 'Global'}

Provide:
1. Top 5 Trending Content Formats [TREND/PREDICTED]
2. Trending Topics & Hashtags in this industry
3. Audience Behaviour Shifts
4. Competitor Strategy Patterns
5. Emerging Opportunities (with [PREDICTED] label)
6. Recommended Content Angles
7. Algorithm Tips for {platform or 'major platforms'}

Be specific, insightful, and actionable. Always label predictions clearly.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
## Social Media Trend Report: {industry or 'General'} on {platform or 'All Platforms'}
"""


def build_chatbot_prompt(query: str, brand_context: dict) -> str:
    ctx = ""
    if brand_context and brand_context.get("brand_name"):
        ctx = (
            f"Brand context — Name: {brand_context.get('brand_name', '')}, "
            f"Industry: {brand_context.get('industry', '')}, "
            f"Platform: {brand_context.get('platform', '')}, "
            f"Goal: {brand_context.get('goal', '')}.\n"
        )
    return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are SocialMind, an expert AI social media assistant.
Follow HAM principles: Helpful, Accurate, Mindful.
Answer social media marketing questions professionally.
If a question is off-topic, politely redirect to social media topics.
Never provide harmful, deceptive, or unethical advice.
<|eot_id|><|start_header_id|>user<|end_header_id|>
{ctx}
Question: {query}
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
Answer:
"""


# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/generate_posts", methods=["POST"])
def generate_posts():
    """Generate personalized social media posts."""
    data = request.get_json(silent=True) or {}

    # Validation
    for field in ["brand_name", "industry", "platform"]:
        if not str(data.get(field, "")).strip():
            return jsonify({"error": f"Field '{field}' is required."}), 400

    # Guardrail: input check
    combined = " ".join(str(v) for v in data.values())
    if guardrail_check(combined):
        return jsonify({"error": "Input contains potentially harmful content. Please revise."}), 400

    # Agentic Tool 1: Hashtag generation
    hashtags = generate_hashtags(
        data.get("brand_name", ""),
        data.get("industry", ""),
        data.get("platform", "Instagram"),
        data.get("goal", "brand awareness"),
    )

    # Agentic Tool 4: Engagement estimation
    audience = int(data.get("audience_size") or 10000)
    engagement = estimate_engagement(data.get("platform", "Instagram"), "post", audience)

    try:
        prompt   = build_post_prompt(data, hashtags)
        response = model.generate_text(prompt=prompt)
        posts    = response.strip()

        if guardrail_check(posts):
            posts = "Unable to generate safe content. Please revise your brand details."

        # Store for human approval
        post_id = f"post_{int(datetime.now().timestamp())}"
        PENDING_POSTS[post_id] = {"content": posts, "brand": data.get("brand_name"), "status": "pending"}

        posts += ETHICS_DISCLAIMER
        return jsonify({
            "posts":      posts,
            "hashtags":   hashtags,
            "engagement": engagement,
            "post_id":    post_id,
            "status":     "pending_approval",
        })
    except Exception as e:
        return jsonify({"error": f"Model error: {str(e)}"}), 500


@app.route("/api/campaign", methods=["POST"])
def generate_campaign():
    """Generate a full campaign strategy + content calendar."""
    data = request.get_json(silent=True) or {}

    for field in ["brand_name", "industry"]:
        if not str(data.get(field, "")).strip():
            return jsonify({"error": f"Field '{field}' is required."}), 400

    combined = " ".join(str(v) for v in data.values())
    if guardrail_check(combined):
        return jsonify({"error": "Input contains potentially harmful content."}), 400

    platforms_raw = data.get("platforms", "Instagram")
    platforms = [p.strip() for p in platforms_raw.split(",") if p.strip()]

    # Agentic Tool 2: Content calendar
    calendar = generate_content_calendar(
        data.get("brand_name", "Brand"),
        platforms,
        data.get("goal", "Brand Awareness"),
        weeks=2,
    )

    try:
        prompt   = build_campaign_prompt(data, calendar)
        response = model.generate_text(prompt=prompt)
        strategy = response.strip()

        if guardrail_check(strategy):
            strategy = "Unable to generate safe campaign strategy. Please revise your inputs."

        strategy += ETHICS_DISCLAIMER
        return jsonify({
            "strategy": strategy,
            "calendar": calendar,
        })
    except Exception as e:
        return jsonify({"error": f"Model error: {str(e)}"}), 500


@app.route("/api/trends", methods=["POST"])
def analyze_trends():
    """Analyze social media trends for an industry/platform."""
    data     = request.get_json(silent=True) or {}
    industry = str(data.get("industry", "General")).strip()
    platform = str(data.get("platform", "All Platforms")).strip()
    region   = str(data.get("region", "Global")).strip()

    if guardrail_check(industry + platform + region):
        return jsonify({"error": "Input contains potentially harmful content."}), 400

    # Agentic Tool 3: Sentiment on competitor info
    competitor_text = data.get("competitor_posts", "")
    sentiment = analyze_sentiment(competitor_text) if competitor_text else None

    try:
        prompt   = build_trend_prompt(industry, platform, region)
        response = model.generate_text(prompt=prompt)
        trends   = response.strip()

        if guardrail_check(trends):
            trends = "Unable to generate trend report. Please try again."

        trends += ETHICS_DISCLAIMER
        return jsonify({
            "trends":           trends,
            "sentiment_analysis": sentiment,
        })
    except Exception as e:
        return jsonify({"error": f"Model error: {str(e)}"}), 500


@app.route("/api/chat", methods=["POST"])
def chatbot():
    """AI-powered social media Q&A chatbot."""
    data          = request.get_json(silent=True) or {}
    user_query    = str(data.get("query", "")).strip()
    brand_context = data.get("brand_context", {})

    if not user_query:
        return jsonify({"error": "Query cannot be empty."}), 400

    if guardrail_check(user_query):
        return jsonify({
            "answer": (
                "I'm sorry, I can't assist with that request as it may involve "
                "unethical content. Please ask about social media marketing topics."
            )
        }), 200

    try:
        prompt   = build_chatbot_prompt(user_query, brand_context)
        response = model.generate_text(prompt=prompt)
        answer   = response.strip()

        if guardrail_check(answer):
            answer = "I'm unable to provide that response safely. Please consult a social media professional."

        answer += "\n\n*— SocialMind · AI-generated · Always apply professional judgment before acting.*"
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": f"Model error: {str(e)}"}), 500


@app.route("/api/sentiment", methods=["POST"])
def sentiment_endpoint():
    """Standalone sentiment analysis endpoint."""
    data = request.get_json(silent=True) or {}
    text = str(data.get("text", "")).strip()
    if not text:
        return jsonify({"error": "Text is required."}), 400
    result = analyze_sentiment(text)
    return jsonify(result)


@app.route("/api/hashtags", methods=["POST"])
def hashtags_endpoint():
    """Standalone hashtag generation endpoint."""
    data = request.get_json(silent=True) or {}
    tags = generate_hashtags(
        data.get("brand", ""),
        data.get("industry", ""),
        data.get("platform", "Instagram"),
        data.get("goal", "brand awareness"),
    )
    return jsonify({"hashtags": tags})


@app.route("/api/approve_post", methods=["POST"])
def approve_post():
    """Human approval endpoint — approve or reject a pending post."""
    data    = request.get_json(silent=True) or {}
    post_id = data.get("post_id", "")
    action  = data.get("action", "approve")  # "approve" | "reject"

    if post_id not in PENDING_POSTS:
        return jsonify({"error": "Post ID not found."}), 404

    PENDING_POSTS[post_id]["status"] = "approved" if action == "approve" else "rejected"
    return jsonify({
        "post_id": post_id,
        "status":  PENDING_POSTS[post_id]["status"],
        "message": f"Post has been {PENDING_POSTS[post_id]['status']}.",
    })


@app.route("/api/analytics", methods=["GET"])
def analytics_dashboard():
    """Returns simulated analytics dashboard data."""
    platforms = ["Instagram", "Twitter", "LinkedIn", "Facebook", "TikTok"]
    data = {
        "engagement_by_platform": [
            {"platform": p, "engagement_rate": round(random.uniform(1.5, 8.5), 2)}
            for p in platforms
        ],
        "posts_by_type": [
            {"type": "Image",    "count": random.randint(30, 80)},
            {"type": "Video",    "count": random.randint(20, 60)},
            {"type": "Carousel", "count": random.randint(10, 40)},
            {"type": "Story",    "count": random.randint(25, 70)},
            {"type": "Reel",     "count": random.randint(15, 50)},
        ],
        "weekly_reach": [
            {"week": f"Week {i+1}", "reach": random.randint(5000, 50000)}
            for i in range(8)
        ],
        "sentiment_breakdown": {
            "positive": random.randint(55, 75),
            "neutral":  random.randint(15, 25),
            "negative": random.randint(5, 15),
        },
        "top_hashtags": [
            {"tag": "#BrandMarketing",     "uses": random.randint(200, 800)},
            {"tag": "#ContentCreator",     "uses": random.randint(150, 700)},
            {"tag": "#SocialMediaTips",    "uses": random.randint(100, 600)},
            {"tag": "#DigitalMarketing",   "uses": random.randint(300, 900)},
            {"tag": "#GrowthHacking",      "uses": random.randint(80, 500)},
        ],
        "note": "⚠️ Figures are simulated for illustration. Connect your real analytics API for live data.",
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
