# ============================================================
# AKILI — REPLIT DEPLOYMENT GUIDE
# Deploy everything on Replit. No Vercel needed for the bot.
# ============================================================

# ── WHAT GOES WHERE ───────────────────────────────────────────

"""
REPLIT (your main Akili host):
  ✅ Akili Core (main.py + all agents)
  ✅ FastAPI server (api/server.py on port 8080)
  ✅ Akili Dashboard (index.html — static deploy)
  ✅ All integrations (Instagram, Twitter, Gmail, etc.)
  ✅ Memory system (~/akili-life/)
  ✅ All cron jobs and schedulers
  Cost: ~$20/month (Replit Core plan)

VERCEL (keep for CREOVA product frontends — free):
  ✅ GoPay landing page
  ✅ Kaya property platform
  ✅ MentalPath frontend
  ✅ creova.one website
  ✅ Any Next.js product frontends
  Cost: FREE (Vercel hobby tier handles all of these)

SUPABASE (already using — keep):
  ✅ All product databases
  Cost: Free tier for most, ~$25/month when scaling
"""


# ── STEP 1: UPGRADE REPLIT PLAN ───────────────────────────────
"""
Go to replit.com → your account → Billing
Upgrade to: Core plan ($20/month)

This gives you:
  - Reserved VM deployments (always-on)
  - Private projects
  - Custom domains
  - $25 in monthly deployment credits
  - No cold starts
"""


# ── STEP 2: DEPLOY THE BOT (Reserved VM) ─────────────────────
"""
In Replit, with your Akili project open:

1. Click "Deploy" button (top right)
2. Select: "Reserved VM"
3. Machine size: 0.5 vCPU / 512MB RAM (enough for Akili)
   → Cost: ~$7/month from your $25 credit
4. Click "Deploy"

Your bot is now at: https://your-repl-name.your-username.repl.co
It runs 24/7. Telegram commands work from your phone.

To redeploy after code changes:
  Click "Deploy" → "Redeploy" (takes ~30 seconds)
"""


# ── STEP 3: DEPLOY THE DASHBOARD (Static) ────────────────────
"""
The Akili dashboard (index.html) deploys as a static site.

Option A: Same Replit project (easiest)
  - FastAPI server already serves index.html at /
  - Access at: https://your-repl-name.your-username.repl.co
  - No extra deployment needed

Option B: Separate static deployment
  1. Create new Replit project
  2. Upload index.html only
  3. Click "Deploy" → "Static Deployment" → FREE
  4. Get URL: https://akili-dashboard.your-username.repl.co
  5. Add custom domain: dashboard.creova.one

Update index.html command bar URL to your Reserved VM URL:
  Replace: 'https://YOUR-REPLIT-URL.repl.co/command'
  With:    'https://your-actual-repl-name.your-username.repl.co/command'
"""


# ── STEP 4: CUSTOM DOMAIN (Optional) ─────────────────────────
"""
Connect creova.one subdomains to your Replit deployments:

In Replit deployment settings → Custom Domain:
  akili.creova.one → your Reserved VM (bot + API)
  dashboard.creova.one → your static dashboard

In your DNS (wherever creova.one is hosted):
  Add CNAME: akili → your-repl-name.your-username.repl.co
  Add CNAME: dashboard → your-dashboard-repl.your-username.repl.co

Done. Akili is now accessible at akili.creova.one
"""


# ── STEP 5: VERIFY DEPLOYMENT ────────────────────────────────
"""
After deploying, test each endpoint:

1. Bot test → Send /start to Akili on Telegram
   Expected: ⚡ AKILI OS — Phase 4 ACTIVE

2. API health check → Visit in browser:
   https://your-repl-name.your-username.repl.co/health
   Expected: {"status": "all_systems_operational", ...}

3. Platform status:
   https://your-repl-name.your-username.repl.co/status/platforms
   Expected: list of connected platforms with true/false

4. Dashboard → Open index.html URL
   Type a command in the command bar
   Expected: response appears in the feed
"""


# ── STEP 6: MONITOR YOUR DEPLOYMENT ──────────────────────────
"""
In Replit → Deployments tab:
  - View real-time logs
  - See CPU and memory usage
  - Restart if needed
  - View web analytics (requests per day)

SHIELD also monitors Replit health via psutil.
If memory or CPU spikes, SHIELD alerts Justin on Telegram.

To view logs from Telegram:
  Send Akili: "show system status"
  Akili returns: memory %, CPU %, uptime, last heartbeat
"""


# ── COST BREAKDOWN ────────────────────────────────────────────
"""
Monthly cost on Replit:

  Replit Core plan:          $20/month
  Reserved VM (0.5vCPU):    ~$7/month (from included $25 credit)
  Static dashboard:          FREE
  Custom domain:             FREE
  ─────────────────────────────
  TOTAL Replit:              ~$20/month (covered by plan credits)

  Anthropic API (Claude):    ~$30-80/month (pay as you go)
  ─────────────────────────────
  TOTAL Akili infrastructure: ~$50-100/month

  Compare to hiring a VA:    $400-1,000/month
  Compare to a social media manager: $1,500-3,000/month
  Compare to a marketing team: $5,000+/month

  Akili replaces all three.
"""


# ── ENVIRONMENT VARIABLES ON REPLIT ──────────────────────────
"""
All secrets stay in Replit Secrets tab (lock icon).
Never in files. Never in code.

Required secrets (you should already have these):
  TELEGRAM_TOKEN
  ANTHROPIC_API_KEY
  JUSTIN_CHAT_ID

Phase 2 (social platforms):
  IG_TOKEN_JJ, IG_USER_ID_JJ (+ other 3 accounts)
  TWITTER_API_KEY, TWITTER_API_SECRET, etc.
  LINKEDIN_ACCESS_TOKEN, etc.
  GMAIL_PERSONAL_ADDRESS, GMAIL_BUSINESS_ADDRESS
  GITHUB_TOKEN

Phase 3-4:
  AKILI_API_SECRET

Phase 5 (new — coming next):
  OPENVC_API_KEY (free — sign up at openvc.com)
  APOLLO_API_KEY (free tier — 50 credits/month)
  RESEND_API_KEY (free — 3,000 emails/month)
  OPENAI_API_KEY (optional — for DALL-E 3 images)
"""
