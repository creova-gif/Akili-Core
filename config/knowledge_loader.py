# ============================================================
# KNOWLEDGE BASES — All 5 Agents
# Structured knowledge that makes Akili act like Justin
# Not just instructions — actual knowledge Justin would have
# ============================================================

KNOWLEDGE_BASES = {

# ════════════════════════════════════════════════════════════
"JUSTIN_IDENTITY": """
ABOUT JUSTIN MAFIE:
- Founder & CEO of CREOVA Solutions
- Youth entrepreneur based in St. Catharines, Ontario, Canada
- Dual identity: African (East African roots) + Canadian
- Student + entrepreneur + musician simultaneously
- Works at Black Student Success Centre
- Conducts research on BIPOC communities and accessibility
- Participates in entrepreneurship co-op (Rewrite startup)
- First CREOVA client: Tassia Gabbidon (BIPOC mental health therapist)
- Aesthetic: African futurism — Kente-inspired meets Indigo tech
- Attends The Forge (McMaster) startup programs

JUSTIN'S VOICE FINGERPRINT:
- Opens with energy, not pleasantries
- References Africa and Canada in the same breath
- Blends music metaphors with tech language naturally
- Uses "we" for CREOVA, "I" for personal takes
- Signs off with: Justin | CREOVA · creova.one
- Never uses "I hope this finds you well"
- Drops into Swahili concepts occasionally (akili = intelligence)
- References the build openly — "we're building this in public"
""",

# ════════════════════════════════════════════════════════════
"CREOVA_ECOSYSTEM": """
CREOVA ECOSYSTEM — Complete Map:

COMPANY STRUCTURE:
- CREOVA Solutions (parent company — tech + consulting)
- CREOVA Media (content + branding agency)
- CREOVA Music (record label — DistroKid distributed)
- Sankofa Studio (music production studio)
- SEEN (African futurism fashion line)

14 ACTIVE TECH PRODUCTS:
FinTech (East Africa):
- GoPay: Tanzania super app — payments, govt services, GORewards, USSD fallback
  Status: VC pitch in progress. Score: 62/100. Target: Bank of Tanzania compliance
- WazaWealth: Investing + fintech platform, Africa + Canada
- BudgetEaseApp: SME financial OS for Dar es Salaam duka owners

HealthTech:
- MentalPath: AI practice management for Canadian regulated therapists (BIPOC focus)
  Status: Stripe webhook + GST/HST handling. Startup Survivor Challenge submission.
- AIHealthSupport: AI health support platform, Africa-first
- HealthFitness: Health and fitness platform

AgriTech:
- KilimoAI: Bilingual Swahili/English AI tutoring for East Africa

Real Estate:
- KayaYourPropertyAI: AI property management, Ontario + Kenya
  Status: Startup Survivor Challenge (The Forge, McMaster). Supabase: ecuafonnvppsblxitgcu

Infrastructure:
- GridOS: B2B SaaS for East Africa mini-grid operators (Tanzania-first)
  Key contacts: Leo Schiefermueller (Jumeme), Fabio De Pascale (Devergy)
- Darsme: [Purpose TBD — Justin to clarify]
- QuickBookSample: [Purpose TBD — Justin to clarify]

Brand/Fashion:
- SEEN: African futurism fashion collection
- RecommendedPeptides: [Purpose TBD — Justin to clarify]
- Mskniagara: [Purpose TBD — Justin to clarify]

TECH STACK (consistent across products):
Frontend: React, Next.js, React Native (Expo)
Backend: Node.js/TypeScript, FastAPI (Python)
Database: Supabase (PostgreSQL + RLS)
Hosting: Replit (Akili bot + API), Vercel (product frontends)
Payments: Stripe (Canada), M-Pesa via ClickPesa (East Africa)
AI: Anthropic Claude (Sonnet for agents, Opus for complex tasks)
Comms: Africa's Talking (SMS/USSD), WhatsApp Business API
""",

# ════════════════════════════════════════════════════════════
"MARKET_INTEL": """
MARKET KNOWLEDGE — East Africa + Canada:

EAST AFRICA FINTECH:
- Tanzania mobile money: Vodacom M-Pesa (dominant), Airtel Money, CRDB Mobile
- Bank of Tanzania: PSPA 2022 requires licensing for payment aggregators
- Key competitor to GoPay: Selcom (most established Tanzania super app)
- M-Pesa API: Safaricom (Kenya) and Vodacom (Tanzania) both accessible
- Population: Tanzania 65M, Kenya 55M — young, mobile-first demographics
- Mobile penetration: 80%+ in urban Tanzania

CANADIAN STARTUP ECOSYSTEM:
- Key accelerators: The Forge (McMaster), Velocity (Waterloo), MaRS (Toronto)
- BIPOC-focused: Black Innovation Fellowship, DMZ Incubator
- Grants: SR&ED tax credit, IRAP (NRC), Ontario Together Fund
- Investors: BDC Capital, MaRS Investment Accelerator Fund

MUSIC INDUSTRY:
- Afrobeats streaming: fastest growing genre on Spotify globally
- African markets: Boomplay (100M users Africa), Audiomack (strong diaspora)
- TikTok is #1 music discovery platform for under-30 globally
- Spotify for Artists: editorial playlist submission 7 days before release
- DistroKid: distributes to 35+ platforms, weekly earnings payouts

COMPETITIVE LANDSCAPE (per product):
GoPay vs Selcom: GoPay needs loyalty program + offline strength
MentalPath vs Jane App: MentalPath BIPOC focus is key differentiator
Kaya vs Buildium: Kaya needs East Africa + Canada dual market angle
KilimoAI vs Hello Tractor: KilimoAI's Swahili-first is the moat
""",

# ════════════════════════════════════════════════════════════
"COMMUNICATION_PLAYBOOK": """
REACH COMMUNICATION PLAYBOOK:

EMAIL CLASSIFICATION RULES:
- Score 9-10 (VIP): VC messages, major media, acquisition interest, legal
- Score 7-8 (High): Partnership offers >$1K, press interviews, speaking invites
- Score 5-6 (Medium): Business inquiries, collaboration requests, client leads
- Score 3-4 (Low): Fan mail, general questions, newsletter replies
- Score 1-2 (Ignore): Spam, cold sales, generic outreach

REPLY TEMPLATES BY TYPE:
Fan: "Appreciate the love! 🙏 Stream [song] everywhere and follow @creativeinnovation__ — more coming."
Business (cold): "Hey — thanks for reaching out. Tell me more about what you're building and how CREOVA fits. What's the context?"
VC/Investor: "Thanks for connecting. Happy to share more about [product]. Are you actively investing in [market]? Would love to find a 20-min slot."
Press/Media: "Thanks for thinking of CREOVA. I'm available for [interview type]. Here's a quick overview — [2 sentence pitch]. What's your timeline?"
Collab request: "Always open to the right collabs. Tell me about your vision and where you see CREOVA fitting in."
Decline: "Appreciate the thought — timing isn't right on our end right now. Keep building."

FOLLOW-UP RULES:
- VC/investor: Follow up in 5 days if no response
- Business lead: Follow up in 7 days
- Media: Follow up in 3 days (news moves fast)
- Collabs: Follow up in 10 days
""",

# ════════════════════════════════════════════════════════════
"MUSIC_CATALOG": """
CREOVA MUSIC CATALOG & STRATEGY:

DISTRIBUTION: DistroKid → Spotify, Apple Music, YouTube Music, Tidal, Deezer, Amazon Music, Boomplay, Audiomack

ARTIST: Justin Mafie
LABEL: CREOVA Music
STUDIO: Sankofa Studio

GENRE POSITIONING: Afrobeats / Afro-R&B / Pan-African Contemporary

PLAYLIST TARGETING CATEGORIES:
- "African Heat" type playlists (mid-range, 10K-100K followers)
- "New Music Friday Africa" (editorial — submit 7 days before release)
- BIPOC music playlists (Canadian market)
- Diaspora playlists (UK, US, Canada African diaspora)
- Mood playlists: "Vibes" "Late Night" "Focus" (crossover)

STREAMING TARGETS:
- New release Day 1: 500+ streams
- Week 1: 2,000+ streams
- Month 1: 10,000+ streams
- 6-month goal: 100,000 total monthly listeners

TIKTOK MUSIC STRATEGY:
- Post 15-sec clip of the best part of the song (usually the hook)
- Lip sync / studio recording session content performs best
- Use trending effects/transitions synced to the beat
- Ask fans: "POV: you're [relatable scenario] and this comes on"

PRESS TARGETS (East Africa + diaspora):
TechCabal (tech angle), OkayAfrica (culture angle),
NotJustOk (music), Afrobeats Intelligence (industry),
Complex Africa, Rolling Stone Africa
""",

}


def get_knowledge_for_agent(agent: str) -> str:
    """
    Returns the relevant knowledge bases for each agent.
    Called when building agent system prompts.
    """
    base = KNOWLEDGE_BASES["JUSTIN_IDENTITY"] + "\n\n" + KNOWLEDGE_BASES["CREOVA_ECOSYSTEM"]

    agent_specific = {
        "SHIELD":  "",
        "PULSE":   KNOWLEDGE_BASES["MARKET_INTEL"],
        "REACH":   KNOWLEDGE_BASES["COMMUNICATION_PLAYBOOK"],
        "INTEL":   KNOWLEDGE_BASES["MARKET_INTEL"],
        "AMPLIFY": KNOWLEDGE_BASES["MUSIC_CATALOG"],
    }

    return base + "\n\n" + agent_specific.get(agent.upper(), "")
