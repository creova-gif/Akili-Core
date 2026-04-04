# ============================================================
# AKILI SKILLS AUDIT — Full Capability Map
# Every agent. Every skill. Source or build. Embed approach.
# ============================================================

"""
AUDIT STRUCTURE PER AGENT:
─────────────────────────────────────────────────────────────
1. Agent identity + who Justin is when this agent speaks
2. Required skills (what it needs to be able to do)
3. Source / Create recommendation per skill
4. Service embedding (creova.one services mapped in)
5. Knowledge bases to load
6. Telegram output format rules
─────────────────────────────────────────────────────────────

ASSUMPTION: creova.one offers:
- Creative agency services (branding, photography, video, social)
- Tech development (web apps, mobile apps, AI products)
- Media production (content, campaigns, storytelling)
- Strategic consulting (growth, go-to-market, brand strategy)
- Music production / label services (Sankofa Studio)
Proceeding with this interpretation. Justin to confirm and update.
"""

SKILLS_AUDIT = {

# ════════════════════════════════════════════════════════════
# AGENT 01 — SHIELD
# Identity: The silent guardian. Justin's digital security chief.
# ════════════════════════════════════════════════════════════
"SHIELD": {
    "identity": "You are SHIELD — Justin Mafie's autonomous security and infrastructure chief. You think like a CTO and act like a bodyguard. You protect every digital asset Justin owns.",
    "required_skills": [
        {
            "skill": "GitHub repo health monitoring",
            "description": "Scan all 14 creova-gif repos for open issues, stale branches, failed CI, exposed secrets, dependency vulnerabilities",
            "source": "BUILD — GitHubMonitor class already started. Extend with PyGitHub library for deeper scanning.",
            "library": "PyGitHub (pip install PyGitHub)",
            "effort": "Low — 2-3 hours",
        },
        {
            "skill": "Secret / API key leak detection",
            "description": "Scan repo commits and files for accidentally exposed API keys, tokens, passwords",
            "source": "SOURCE — use truffleHog or detect-secrets via CLI call",
            "library": "truffleHog3 (pip install trufflehog3)",
            "effort": "Low — install + configure",
        },
        {
            "skill": "Website uptime monitoring",
            "description": "Ping creova.one and all deployed Vercel/Railway apps every 30 min, alert Justin instantly on downtime",
            "source": "BUILD — aiohttp health check. Already scaffolded. Add SSL cert expiry check.",
            "library": "aiohttp + ssl (built-in)",
            "effort": "Done — extend only",
        },
        {
            "skill": "Dependency vulnerability scanning",
            "description": "Check all requirements.txt and package.json files for known CVEs",
            "source": "SOURCE — Safety (pip) + npm audit via subprocess",
            "library": "safety (pip install safety)",
            "effort": "Medium — 4 hours",
        },
        {
            "skill": "Replit environment health",
            "description": "Monitor Replit memory, CPU, ensure always-on is active",
            "source": "BUILD — psutil for system stats",
            "library": "psutil (pip install psutil)",
            "effort": "Low — 1 hour",
        },
        {
            "skill": "Automated backup system",
            "description": "Nightly backup of Akili memory files and critical configs to GitHub private repo",
            "source": "BUILD — git commit + push via subprocess",
            "library": "subprocess (built-in) + GitPython",
            "effort": "Medium — 3 hours",
        },
        {
            "skill": "Supabase database monitoring",
            "description": "Check all CREOVA product Supabase DBs for errors, failed queries, storage limits",
            "source": "SOURCE — Supabase Python client",
            "library": "supabase (pip install supabase)",
            "effort": "Medium — 4 hours",
        },
        {
            "skill": "Vercel deployment status",
            "description": "Monitor all Vercel deployments for build failures, edge function errors",
            "source": "SOURCE — Vercel REST API",
            "library": "aiohttp + VERCEL_TOKEN",
            "effort": "Low — 2 hours",
        },
    ],
    "knowledge_base": [
        "All 14 GitHub repo names, purposes, and tech stacks",
        "All API keys Akili manages (by name only, never values)",
        "All Supabase project IDs",
        "All Vercel project names",
        "CREOVA domain list and SSL expiry dates",
        "Justin's security rules (MEMORY.md)",
    ],
    "telegram_output_format": """
🛡 *SHIELD REPORT*

*Status:* ✅ All systems operational / ⚠️ Issues detected

*GitHub:* {n} repos scanned · {issues} open issues
*Uptime:* creova.one ✅ · {n} other sites checked
*Secrets:* No leaks detected ✅
*Supabase:* All DBs healthy ✅

*Action required:* [specific item if any]
*Next scan:* 30 minutes
""",
},

# ════════════════════════════════════════════════════════════
# AGENT 02 — PULSE
# Identity: Justin's creative director + social media operator
# Knows brand, knows voice, executes like a seasoned SMM team
# ════════════════════════════════════════════════════════════
"PULSE": {
    "identity": "You are PULSE — Justin Mafie's creative director and social media operator. You think like a seasoned brand strategist, write like a creative director, and execute like a marketing team. You know Justin's voice better than anyone.",
    "required_skills": [
        {
            "skill": "Platform-native content writing",
            "description": "Write content that feels native to each platform — Instagram hooks, Twitter punches, LinkedIn thought leadership, TikTok captions, Snapchat authenticity",
            "source": "BUILD — Platform-specific prompt templates. Already started. Expand with style guides per platform.",
            "effort": "Done — refine templates",
        },
        {
            "skill": "Hashtag intelligence",
            "description": "Research and rotate optimal hashtag sets per platform, track which sets drive most reach",
            "source": "SOURCE — RapidAPI Hashtag Generator or Hashtagify API",
            "library": "aiohttp + RapidAPI (free tier available)",
            "effort": "Low — 2 hours",
        },
        {
            "skill": "Image generation for posts",
            "description": "Generate on-brand visual concepts and actual images for posts (African futurism aesthetic)",
            "source": "SOURCE — DALL-E 3 via OpenAI API or Stability AI",
            "library": "openai (pip install openai) or stability-sdk",
            "effort": "Medium — 4 hours + API cost ~$0.04/image",
        },
        {
            "skill": "Caption A/B testing tracker",
            "description": "Track which caption styles get most engagement per platform, learn and improve",
            "source": "BUILD — Store post metadata + results in memory, weekly analysis",
            "effort": "Medium — 5 hours",
        },
        {
            "skill": "Content repurposing pipeline",
            "description": "Take one piece of content → auto-reformat for all 10 accounts in one shot",
            "source": "BUILD — Already in REACH. Move core repurpose logic into PULSE with platform rules.",
            "effort": "Low — refactor existing code",
        },
        {
            "skill": "Instagram carousel builder",
            "description": "Script multi-slide carousel posts (5-10 slides) for educational content and brand storytelling",
            "source": "BUILD — Generate slide text + visual direction for each slide",
            "effort": "Low — prompt engineering",
        },
        {
            "skill": "TikTok trend monitoring",
            "description": "Track trending sounds, challenges, formats relevant to music + tech on TikTok",
            "source": "SOURCE — TikTok Research API (requires TikTok developer account)",
            "library": "aiohttp + TikTok Research API",
            "effort": "Medium — 4 hours",
        },
        {
            "skill": "Optimal posting time calculator",
            "description": "Analyze engagement data per platform and account to find Justin's best posting windows",
            "source": "BUILD — Track post times + engagement in memory, run weekly regression",
            "effort": "Medium — 6 hours",
        },
        {
            "skill": "Snap Creator score tracking",
            "description": "Monitor Snapchat Creator program metrics, remind Justin of daily story requirement",
            "source": "BUILD — Manual tracking + reminder system (Snapchat API limited)",
            "effort": "Low — already started",
        },
        {
            "skill": "LinkedIn article writing",
            "description": "Write 600-1200 word thought leadership articles for publication on LinkedIn and Medium",
            "source": "BUILD — Long-form writing prompt with SEO structure",
            "effort": "Done — in solutions_marketing.py",
        },
    ],
    "creova_services_embedded": {
        "Branding": "PULSE promotes CREOVA's branding services via @creovasolutions posts — client case studies, before/after transformations, process videos",
        "Photography/Video": "PULSE creates content demonstrating CREOVA's production capabilities — behind-scenes shoots, client work highlights",
        "Social Media Management": "PULSE itself is the proof of concept — 'CREOVA managed @creovasolutions' becomes a case study for selling this service",
        "Strategic Consulting": "PULSE publishes Justin's strategic insights on LinkedIn as thought leadership, driving consulting leads to creova.one",
    },
    "knowledge_base": [
        "All 10 social account handles and their specific audiences",
        "Weekly content themes (Monday–Sunday)",
        "CREOVA brand voice guide",
        "Hashtag sets per vertical (music, tech, personal, studio)",
        "Best performing content formats per platform",
        "Cross-promotion rules and mandatory mentions",
        "African futurism aesthetic guidelines",
        "creova.one service list and value propositions",
    ],
    "telegram_output_format": """
📡 *PULSE — {platform} Post Ready*

*Account:* {handle}
*Theme:* {theme} | *Best time:* {time}

━━━━━━━━━━━━━━━━━━━━
{caption}

{hashtags}
━━━━━━━━━━━━━━━━━━━━

📸 *Visual direction:* {visual_note}
🎯 *Goal:* {engagement_goal}

Reply *POST {id}* · *EDIT {id} [text]* · *SKIP {id}*
""",
},

# ════════════════════════════════════════════════════════════
# AGENT 03 — REACH
# Identity: Justin's comms chief and relationship manager
# Speaks for Justin authentically across every channel
# ════════════════════════════════════════════════════════════
"REACH": {
    "identity": "You are REACH — Justin Mafie's communications chief and relationship manager. You speak for Justin authentically across every channel. You know who matters, who's a time-waster, and who needs VIP treatment. You build relationships, not just replies.",
    "required_skills": [
        {
            "skill": "Email classification and priority scoring",
            "description": "Score every incoming email 1-10 on urgency and strategic value, route accordingly",
            "source": "BUILD — Expand classify_email() with scoring system + contact relationship memory",
            "effort": "Low — 3 hours",
        },
        {
            "skill": "CRM-style contact memory",
            "description": "Remember who every contact is, their relationship to CREOVA, past interactions, follow-up needed",
            "source": "BUILD — Store contact profiles in ~/akili-life/contacts/ as entity files",
            "effort": "Medium — 5 hours",
        },
        {
            "skill": "WhatsApp Business API integration",
            "description": "Read and reply to WhatsApp Business messages automatically",
            "source": "SOURCE — Twilio WhatsApp API or WhatsApp Business Cloud API (Meta)",
            "library": "twilio (pip install twilio) or aiohttp + Meta API",
            "effort": "High — 8 hours + Meta Business verification",
        },
        {
            "skill": "Multi-language reply (English + French for Canada)",
            "description": "Detect message language and reply in same language — English, French for Canadian contacts",
            "source": "BUILD — Language detection via langdetect + Claude bilingual prompt",
            "library": "langdetect (pip install langdetect)",
            "effort": "Low — 2 hours",
        },
        {
            "skill": "Follow-up reminder system",
            "description": "Track conversations that need follow-up, remind Justin via Telegram if no response in N days",
            "source": "BUILD — Pending follow-ups tracked in memory with timestamps",
            "effort": "Medium — 4 hours",
        },
        {
            "skill": "Email campaign sending",
            "description": "Send bulk campaigns to segmented lists (fans, clients, investors) with tracking",
            "source": "SOURCE — Resend API (modern, generous free tier: 3,000/month)",
            "library": "resend (pip install resend)",
            "effort": "Medium — 4 hours",
        },
        {
            "skill": "Newsletter drafting",
            "description": "Auto-draft weekly CREOVA newsletter combining music updates + tech updates + personal story",
            "source": "BUILD — Weekly newsletter template + Claude generation",
            "effort": "Low — 3 hours",
        },
        {
            "skill": "Partnership outreach automation",
            "description": "Find and send initial outreach to potential partners (brands, labels, VCs) with personalized angles",
            "source": "BUILD — Combine INTEL lead list + REACH outreach generator",
            "effort": "Medium — 5 hours",
        },
        {
            "skill": "SMS via Twilio",
            "description": "Send and receive SMS for time-sensitive communications",
            "source": "SOURCE — Twilio SMS API",
            "library": "twilio (pip install twilio)",
            "effort": "Low — 2 hours",
        },
    ],
    "creova_services_embedded": {
        "Client Communications": "REACH handles all inbound client inquiries to @creovasolutions — qualifies leads, schedules calls, sends proposals",
        "Music Industry Outreach": "REACH sends playlist pitch emails, press kit emails, collaboration requests on behalf of CREOVA Music",
        "Investor Relations": "REACH manages GoPay investor outreach, tracks responses, schedules pitch calls",
        "Fan Engagement": "REACH maintains authentic fan relationships across all music platforms — never robotic, always Justin's voice",
    },
    "knowledge_base": [
        "Justin's voice and communication style per audience type",
        "CREOVA client list and relationship status",
        "Known contacts database (VCs, press, collaborators, clients)",
        "Email templates per scenario (fan, business, press, VC, collab)",
        "CREOVA Solutions pricing and service packages",
        "Music industry contacts (curators, labels, blogs)",
        "Partnership targets and outreach status",
        "Follow-up queue with timestamps",
    ],
    "telegram_output_format": """
📨 *REACH — {channel} Activity*

*From:* {sender}
*Type:* {classification} | *Priority:* {score}/10

*Their message:*
_{preview}_

*Action taken:* {action}
*My reply:*
━━━━━━━━━━━━━━━━━━━━
{reply_text}
━━━━━━━━━━━━━━━━━━━━

{urgent_flag}
*Follow-up needed:* {followup}
""",
},

# ════════════════════════════════════════════════════════════
# AGENT 04 — INTEL
# Identity: Justin's head of strategy and competitive intelligence
# Thinks 6 months ahead, knows every market, surfaces what matters
# ════════════════════════════════════════════════════════════
"INTEL": {
    "identity": "You are INTEL — Justin Mafie's head of strategy and competitive intelligence. You think 6 months ahead of the market. You know East Africa tech, Canadian startups, the music industry, and emerging markets better than any consultant. You surface only what Justin can act on.",
    "required_skills": [
        {
            "skill": "Live web search and synthesis",
            "description": "Search the web for real-time news, synthesize into actionable intelligence",
            "source": "BUILT — Anthropic web search tool already integrated in intel_live.py",
            "effort": "Done",
        },
        {
            "skill": "VC and investor database",
            "description": "Maintain a tracked list of 50+ VCs active in Africa and Canada tech, updated weekly",
            "source": "BUILD — ~/akili-life/resources/vcs/ entity files, updated by INTEL weekly",
            "effort": "Medium — build once, maintain weekly",
        },
        {
            "skill": "Crunchbase/LinkedIn scraping for leads",
            "description": "Find fresh leads for CREOVA Solutions from Crunchbase company lists",
            "source": "SOURCE — Crunchbase API (free tier) or Proxycurl for LinkedIn",
            "library": "aiohttp + Crunchbase API key",
            "effort": "Medium — 5 hours + API cost",
        },
        {
            "skill": "Trend detection and opportunity spotting",
            "description": "Identify emerging tech trends in Africa and Canada that CREOVA should position around",
            "source": "BUILD — Weekly synthesis from search results into opportunity radar",
            "effort": "Low — prompt engineering",
        },
        {
            "skill": "Product-market fit analysis",
            "description": "Analyze user feedback, market data, and competitor moves for each of the 14 products",
            "source": "BUILD — Template per product, updated monthly from search data",
            "effort": "Medium — 6 hours",
        },
        {
            "skill": "Podcast and media monitoring",
            "description": "Track when CREOVA, Justin Mafie, or CREOVA products are mentioned in podcasts or media",
            "source": "SOURCE — Listen Notes API for podcasts, Google Alerts via RSS",
            "library": "feedparser (pip install feedparser) + aiohttp",
            "effort": "Low — 3 hours",
        },
        {
            "skill": "Grant and funding opportunity finder",
            "description": "Find government grants, startup competitions, and non-dilutive funding for Canadian and African markets",
            "source": "BUILD — Weekly search for Canadian tech grants, AfriLabs competitions, etc.",
            "effort": "Medium — 4 hours",
        },
        {
            "skill": "Regulatory intelligence",
            "description": "Track Bank of Tanzania policy changes, FINTRAC Canada rules, health tech regulations — for GoPay, MentalPath, etc.",
            "source": "BUILD — Specific search queries for each product's regulatory environment",
            "effort": "Medium — 4 hours",
        },
        {
            "skill": "Competitor feature tracking",
            "description": "Monitor what competitors to GoPay, Kaya, MentalPath are shipping each week",
            "source": "SOURCE — G2 / Capterra API or direct web search per competitor",
            "effort": "Medium — 5 hours",
        },
    ],
    "creova_services_embedded": {
        "Market Research": "INTEL delivers the intelligence that makes CREOVA's strategic consulting credible — Justin pitches insights clients can't get elsewhere",
        "Go-to-Market Strategy": "INTEL builds the competitive landscape analysis that informs every CREOVA GTM plan for clients",
        "Investor Preparation": "INTEL generates GoPay-quality investor materials for CREOVA's own products AND potentially for startup clients as a service",
        "Grant Writing": "INTEL identifies funding opportunities that CREOVA Solutions can pursue for itself and sell as a service to African startup clients",
    },
    "knowledge_base": [
        "14 CREOVA product descriptions and target markets",
        "East Africa fintech landscape (M-Pesa, Airtel Money, competitors)",
        "Canadian startup ecosystem and key accelerators",
        "VC watch list with investment thesis per fund",
        "GoPay competitive analysis (Selcom, Tigo Pesa, CRDB Mobile)",
        "MentalPath competitive analysis (Canadian teletherapy market)",
        "African music streaming market (Boomplay, Audiomack, Spotify Africa)",
        "Regulatory bodies: Bank of Tanzania, FINTRAC, PHIPA Ontario",
        "Key media outlets: TechCabal, Disrupt Africa, BNN Bloomberg Canada",
        "CREOVA client ideal customer profiles per service",
    ],
    "telegram_output_format": """
🔍 *INTEL BRIEFING*

*Topic:* {topic}
*Searched:* {sources_count} sources | *Date:* {date}

━━━━━━━━━━━━━━━━━━━━
📌 *KEY FINDINGS*
{findings}

💡 *CREOVA OPPORTUNITY*
{opportunity}

⚡ *RECOMMENDED ACTION*
{action}

📎 *Sources:* {source_list}
━━━━━━━━━━━━━━━━━━━━
_Confidence: {confidence}_
""",
},

# ════════════════════════════════════════════════════════════
# AGENT 05 — AMPLIFY
# Identity: Justin's music label GM + growth hacker
# Lives in the data, drives streams, builds the CREOVA Music brand
# ════════════════════════════════════════════════════════════
"AMPLIFY": {
    "identity": "You are AMPLIFY — Justin Mafie's music label GM and growth hacker. You think like an A&R exec who also reads analytics dashboards. You grow streams, build the CREOVA Music brand, and find every opportunity to cross-pollinate audiences between music and tech.",
    "required_skills": [
        {
            "skill": "Spotify for Artists data tracking",
            "description": "Pull monthly listeners, stream counts, playlist adds, top cities for Justin Mafie on Spotify",
            "source": "SOURCE — Spotify Web API (requires Spotify for Artists OAuth)",
            "library": "spotipy (pip install spotipy)",
            "effort": "Medium — 5 hours",
        },
        {
            "skill": "DistroKid earnings and distribution tracking",
            "description": "Monitor release status, streaming platform distribution, earnings across platforms",
            "source": "SOURCE — DistroKid doesn't have a public API. Use web scraping with Playwright or Selenium.",
            "library": "playwright (pip install playwright)",
            "effort": "High — 8 hours + CAPTCHA handling",
        },
        {
            "skill": "TikTok sound tracking",
            "description": "Monitor how many TikTok videos are using Justin's songs as audio",
            "source": "SOURCE — TikTok Research API (apply at developers.tiktok.com)",
            "library": "aiohttp + TikTok Research API",
            "effort": "Medium — after API approval",
        },
        {
            "skill": "Playlist pitch automation",
            "description": "Generate personalized pitches to Spotify playlist curators, track opens and responses",
            "source": "BUILD — Playlist pitch generator (done) + Resend for sending + tracking",
            "effort": "Low — connect existing tools",
        },
        {
            "skill": "YouTube Music analytics",
            "description": "Track views, subscribers, and engagement on CREOVA Music YouTube presence",
            "source": "SOURCE — YouTube Data API v3 (free, generous quota)",
            "library": "google-api-python-client (already installed)",
            "effort": "Low — 3 hours",
        },
        {
            "skill": "Music blog and press tracker",
            "description": "Monitor music blogs and African music press for coverage opportunities and submission deadlines",
            "source": "BUILD — RSS feeds from TurnTable, OkayAfrica, NotJustOk, etc.",
            "library": "feedparser (pip install feedparser)",
            "effort": "Low — 3 hours",
        },
        {
            "skill": "Release schedule manager",
            "description": "Maintain the CREOVA Music release calendar, trigger campaigns automatically at T-21, T-7, T-1, release day",
            "source": "BUILD — Release schedule in memory + cron triggers",
            "effort": "Medium — 5 hours",
        },
        {
            "skill": "Collaboration opportunity finder",
            "description": "Find artists in compatible genres with similar followings for potential features/collabs",
            "source": "BUILD — Search for artists in African music space, filter by follower range and genre",
            "effort": "Medium — 4 hours",
        },
        {
            "skill": "Sync licensing opportunity tracker",
            "description": "Find TV, film, ad, and game sync licensing opportunities for CREOVA Music catalog",
            "source": "SOURCE — Music Gateway API or Musicbed (manual submission but AMPLIFY preps the materials)",
            "effort": "Medium — 4 hours",
        },
        {
            "skill": "Stream milestone alerting",
            "description": "Alert Justin when any song hits 100, 1K, 10K, 100K streams — trigger milestone post",
            "source": "BUILD — Poll Spotify API, compare to stored baseline, trigger if threshold crossed",
            "effort": "Low — 2 hours once Spotify API is connected",
        },
    ],
    "creova_services_embedded": {
        "Music Production": "AMPLIFY showcases Sankofa Studio's production quality through behind-scenes content, attracting artists to book the studio",
        "Artist Development": "AMPLIFY demonstrates CREOVA Music's artist development capabilities — Justin as the proof of concept",
        "Label Services": "AMPLIFY's release campaign system becomes a service CREOVA Music offers to signed artists",
        "Music Marketing": "AMPLIFY's campaign strategies are documented and sold as a consulting product to other African independent artists",
    },
    "knowledge_base": [
        "Full CREOVA Music catalog (song titles, release dates, genres)",
        "Spotify for Artists metrics baseline (updated weekly)",
        "Active release schedule and campaign status",
        "Playlist targets database (curator names, submission URLs, genres)",
        "Music press contact list (blogs, journalists, playlist curators)",
        "Collaboration targets (artists in range)",
        "Sync licensing submission portals and deadlines",
        "TikTok trending sounds in Afrobeats/R&B/African music",
        "YouTube Music channel analytics",
        "Snapchat Creator program score and targets",
    ],
    "telegram_output_format": """
🔊 *AMPLIFY — Music Intelligence*

*Artist:* Justin Mafie | CREOVA Music
*Period:* {period}

━━━━━━━━━━━━━━━━━━━━
🎵 *STREAMS*
Spotify: {spotify_streams} ({spotify_delta})
Apple Music: {apple_streams}
TikTok: {tiktok_uses} video uses

📊 *GROWTH*
Monthly listeners: {monthly_listeners}
Playlist adds: {playlist_adds}
New territories: {territories}

🎯 *ACTION ITEMS*
{action_items}

🚀 *NEXT RELEASE*
{next_release_info}
━━━━━━━━━━━━━━━━━━━━
_Campaign status: {campaign_status}_
""",
},

}
