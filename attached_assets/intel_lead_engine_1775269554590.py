# ============================================================
# INTEL LEAD ENGINE — Phase 5 Upgrade
# Replaces Crunchbase with better free/cheap alternatives:
#
# OpenVC    → VC database (FREE, 9,000+ investors, Africa data)
# Apollo.io → Lead gen + contact data (FREE: 50 credits/month)
# Hunter.io → Email finder (FREE: 25 searches/month)
# Dealroom  → Startup intelligence (FREE community plan)
#
# Why these beat Crunchbase for CREOVA:
# - OpenVC: specifically built for founders pitching VCs ✅
# - Apollo: actual verified contact emails, not just company names ✅
# - Hunter: find decision-maker emails by domain ✅
# - All free tiers generous enough for INTEL's weekly cadence ✅
# ============================================================

import os
import logging
import aiohttp
import asyncio
from datetime import datetime
from anthropic import Anthropic
from skills.shared.telegram_formatter import formatter, DIVIDER

log = logging.getLogger("INTEL.LeadEngine")

ANTHROPIC_KEY   = os.environ["ANTHROPIC_API_KEY"]
APOLLO_API_KEY  = os.environ.get("APOLLO_API_KEY", "")     # free at apollo.io
HUNTER_API_KEY  = os.environ.get("HUNTER_API_KEY", "")     # free at hunter.io
OPENVC_API_KEY  = os.environ.get("OPENVC_API_KEY", "")     # free at openvc.com


class IntelLeadEngine:
    """
    INTEL's lead generation and VC intelligence layer.
    Uses Apollo, OpenVC, and Hunter instead of Crunchbase.
    All have free tiers generous enough for CREOVA's needs.
    """

    def __init__(self, telegram_app, memory):
        self.app    = telegram_app
        self.memory = memory
        self.client = Anthropic(api_key=ANTHROPIC_KEY)
        log.info("INTEL LeadEngine initialized — Apollo + OpenVC + Hunter")

    # ── Apollo.io lead search ─────────────────────────────────
    async def apollo_search(self, query: dict) -> list:
        """
        Search Apollo for leads.
        Free tier: 50 credits/month.
        Each search = 1 credit. Results include verified emails.

        query example:
        {
            "person_titles": ["CEO", "Founder", "Director"],
            "person_locations": ["Canada", "Kenya", "Tanzania"],
            "organization_industry_tag_ids": ["fintech", "health"],
            "q_keywords": "BIPOC health mental wellness"
        }
        """
        if not APOLLO_API_KEY:
            return []

        url = "https://api.apollo.io/v1/mixed_people/search"
        headers = {
            "Content-Type":  "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key":     APOLLO_API_KEY,
        }
        payload = {
            **query,
            "page":     1,
            "per_page": 10,
        }

        try:
            async with aiohttp.ClientSession() as s:
                async with s.post(url, json=payload, headers=headers,
                                  timeout=aiohttp.ClientTimeout(total=15)) as r:
                    if r.status == 200:
                        data = await r.json()
                        people = data.get("people", [])
                        log.info(f"[Apollo] Found {len(people)} leads")
                        return people
                    log.warning(f"[Apollo] Status {r.status}")
                    return []
        except Exception as e:
            log.error(f"[Apollo] Error: {e}")
            return []

    # ── Hunter.io email finder ────────────────────────────────
    async def hunter_find_email(self, domain: str, first_name: str = "",
                                 last_name: str = "") -> dict:
        """
        Find decision-maker email at a company domain.
        Free tier: 25 searches/month.
        Perfect for finding the right person at a target company.
        """
        if not HUNTER_API_KEY:
            return {}

        url = "https://api.hunter.io/v2/email-finder"
        params = {
            "domain":     domain,
            "first_name": first_name,
            "last_name":  last_name,
            "api_key":    HUNTER_API_KEY,
        }

        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(url, params=params,
                                  timeout=aiohttp.ClientTimeout(total=10)) as r:
                    if r.status == 200:
                        data = await r.json()
                        result = data.get("data", {})
                        log.info(f"[Hunter] Email found for {domain}: {result.get('email','none')}")
                        return result
                    return {}
        except Exception as e:
            log.error(f"[Hunter] Error: {e}")
            return {}

    async def hunter_domain_search(self, domain: str) -> list:
        """
        Get all public emails found at a domain.
        Great for finding the right contact at a target company.
        """
        if not HUNTER_API_KEY:
            return []

        url = "https://api.hunter.io/v2/domain-search"
        params = {"domain": domain, "api_key": HUNTER_API_KEY, "limit": 5}

        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(url, params=params,
                                  timeout=aiohttp.ClientTimeout(total=10)) as r:
                    if r.status == 200:
                        data = await r.json()
                        emails = data.get("data", {}).get("emails", [])
                        log.info(f"[Hunter] {len(emails)} emails found at {domain}")
                        return emails
                    return []
        except Exception as e:
            log.error(f"[Hunter] Error: {e}")
            return []

    # ── OpenVC investor search ────────────────────────────────
    async def openvc_search_investors(self, filters: dict = None) -> list:
        """
        Search OpenVC for investors relevant to CREOVA/GoPay.
        FREE — 9,000+ investors with Africa, fintech, healthtech data.
        Perfect for GoPay VC pitch targeting.

        OpenVC API is in beta — falls back to web search if unavailable.
        """
        if not OPENVC_API_KEY:
            # Fallback: use web search to find relevant VCs
            return await self._vc_web_search(filters or {})

        url    = "https://api.openvc.com/v1/investors"
        params = filters or {
            "stage":    "seed,pre-seed",
            "location": "Africa,Canada",
            "focus":    "fintech,healthtech",
        }
        headers = {"Authorization": f"Bearer {OPENVC_API_KEY}"}

        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(url, params=params, headers=headers,
                                  timeout=aiohttp.ClientTimeout(total=15)) as r:
                    if r.status == 200:
                        data = await r.json()
                        investors = data.get("investors", [])
                        log.info(f"[OpenVC] Found {len(investors)} investors")
                        return investors
                    # API might not be live yet — fall back
                    return await self._vc_web_search(params)
        except Exception as e:
            log.error(f"[OpenVC] Error: {e} — using web fallback")
            return await self._vc_web_search(filters or {})

    async def _vc_web_search(self, filters: dict) -> list:
        """Fallback: use Anthropic web search to find VC data."""
        focus    = filters.get("focus", "African tech fintech")
        stage    = filters.get("stage", "seed pre-seed")
        location = filters.get("location", "Africa Canada")

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=[{"role": "user", "content":
                f"Find 5 VCs actively investing in {focus} at {stage} stage in {location} in 2026. "
                f"For each: name, fund, check size, portfolio companies, best pitch angle, website."}]
        )
        result = ""
        for block in response.content:
            if block.type == "text":
                result += block.text
        return [{"source": "web_search", "data": result}]

    # ── Generate leads for CREOVA Solutions ──────────────────
    async def generate_creova_leads(self, service: str = "tech development",
                                     market: str = "Canada") -> str:
        """
        Generate real, actionable leads for CREOVA Solutions.
        Uses Apollo to find decision-makers, Hunter to get their emails.
        """
        log.info(f"[INTEL] Generating leads — {service} in {market}")

        # Define search params per service + market
        search_configs = {
            "tech development + Canada": {
                "person_titles":    ["CTO", "Founder", "CEO", "Head of Technology"],
                "person_locations": ["Canada", "Ontario", "Toronto"],
                "q_keywords":       "startup tech product build",
            },
            "branding + Canada": {
                "person_titles":    ["Founder", "CEO", "Marketing Director", "Creative Director"],
                "person_locations": ["Canada"],
                "q_keywords":       "BIPOC business brand identity",
            },
            "tech development + East Africa": {
                "person_titles":    ["Founder", "CEO", "CTO"],
                "person_locations": ["Kenya", "Tanzania", "Uganda"],
                "q_keywords":       "startup fintech agritech healthtech",
            },
        }

        key    = f"{service} + {market}"
        config = search_configs.get(key, search_configs["tech development + Canada"])
        people = await self.apollo_search(config)

        if not people:
            # No Apollo key or credits exhausted — use Claude + web search
            return await self._ai_lead_gen(service, market)

        # Format leads into a Telegram-ready report
        lead_lines = []
        for i, person in enumerate(people[:5], 1):
            name    = f"{person.get('first_name','')} {person.get('last_name','')}".strip()
            title   = person.get("title", "Unknown role")
            company = person.get("organization", {}).get("name", "Unknown company")
            email   = person.get("email", "")
            linkedin= person.get("linkedin_url", "")

            # Try to get verified email via Hunter if not in Apollo result
            if not email and person.get("organization", {}).get("website_url"):
                domain = person["organization"]["website_url"].replace("https://","").replace("http://","").split("/")[0]
                hunter_result = await self.hunter_find_email(
                    domain, person.get("first_name",""), person.get("last_name","")
                )
                email = hunter_result.get("email", "")

            lead_lines.append(
                f"  *{i}. {name}*\n"
                f"     {title} @ {company}\n"
                f"     📧 `{email or 'email not found'}`\n"
                f"     🔗 {linkedin or 'no LinkedIn'}\n"
                f"     💡 Angle: {self._outreach_angle(service, title, company)}"
            )

        self.memory.daily_log(f"[INTEL] Generated {len(people)} leads for {service} in {market}")

        return formatter.format("INTEL", "research", {
            "query":        f"Lead gen: {service} in {market}",
            "source_count": "Apollo + Hunter",
            "findings":     [f"Found {len(people)} qualified leads"] + lead_lines[:3],
            "creova_angle": f"CREOVA Solutions offers {service} — pitch directly to these decision-makers",
            "action":       "Reply OUTREACH [name] [company] to generate a personalized pitch",
            "confidence":   "High — Apollo verified contacts",
        })

    def _outreach_angle(self, service: str, title: str, company: str) -> str:
        """Generate a one-line outreach angle per lead."""
        angles = {
            "tech development": f"'{company} needs a tech partner who builds for real markets'",
            "branding":         f"'Position {company} with an identity that actually stands out'",
            "social media":     f"'Your social presence doesn't match the quality of what you build'",
            "music":            f"'CREOVA Music can help {company} reach new audiences through sound'",
        }
        for key, angle in angles.items():
            if key in service.lower():
                return angle
        return f"'CREOVA can accelerate {company}'s growth'"

    async def _ai_lead_gen(self, service: str, market: str) -> str:
        """Fallback: pure AI lead generation using web search."""
        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1200,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=[{"role": "user", "content":
                f"Find 5 specific potential clients for CREOVA Solutions' {service} service in {market}. "
                f"For each: company name, what they do, why they need CREOVA, who to contact (title), "
                f"and the best outreach angle. Be specific — real companies, real opportunities."}]
        )
        result = ""
        for block in response.content:
            if block.type == "text":
                result += block.text

        return await formatter.ai_enhance(
            f"🎯 LEADS — {service} · {market}\n\n{result}", "INTEL"
        )

    # ── GoPay VC tracker using OpenVC ────────────────────────
    async def gopay_vc_tracker(self) -> str:
        """
        Find the best VCs for GoPay pitch using OpenVC + web search.
        Sends a structured investor briefing to Justin.
        """
        investors = await self.openvc_search_investors({
            "focus":    "fintech,mobile money,emerging markets",
            "stage":    "seed,pre-seed,series-a",
            "location": "Africa,Canada,UK",
        })

        # Enrich with live web data
        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1500,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=[{"role": "user", "content":
                "Search for VCs who invested in African fintech or mobile money startups in 2024-2026. "
                "I need: fund name, recent Africa investments, check size, and best pitch angle for "
                "GoPay Tanzania — a mobile money super app targeting unbanked users. "
                "Include: Partech Africa, TLcom Capital, Novastar Ventures, Algebra Ventures, "
                "Y Combinator (Africa batch), Orange Ventures, Admazing. "
                "Which ones are actively deploying right now?"}]
        )
        result = ""
        for block in response.content:
            if block.type == "text":
                result += block.text

        self.memory.daily_log("[INTEL] GoPay VC tracker updated")
        return await formatter.ai_enhance(
            f"💰 GOPAY VC TRACKER\n\nLive data as of {datetime.now().strftime('%B %d, %Y')}\n\n{result}",
            "INTEL", "GoPay investor intelligence"
        )

    # ── Weekly lead digest ────────────────────────────────────
    async def weekly_lead_digest(self) -> str:
        """
        Every Monday: auto-generate leads across all CREOVA services.
        Sent to Justin as a structured weekly opportunity brief.
        """
        sections = []

        # Tech leads in Canada
        tech_canada = await self._ai_lead_gen("tech development", "Canada")
        sections.append(tech_canada[:800])

        # Branding leads (BIPOC businesses Canada)
        branding = await self._ai_lead_gen("branding", "BIPOC Canada")
        sections.append(branding[:800])

        # East Africa tech
        ea_tech = await self._ai_lead_gen("tech development", "East Africa")
        sections.append(ea_tech[:800])

        self.memory.daily_log("[INTEL] Weekly lead digest generated")

        header = (
            f"🎯 *INTEL — WEEKLY LEAD DIGEST*\n"
            f"`{datetime.now().strftime('%B %d, %Y')}`\n\n"
            f"{DIVIDER}\n\n"
        )
        return header + f"\n\n{DIVIDER}\n\n".join(sections)
