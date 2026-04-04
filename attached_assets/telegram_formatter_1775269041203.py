# ============================================================
# TELEGRAM FORMATTER — Shared Skill (All Agents)
# Every output is creative, clear, detailed, and on-brand
# This is what separates Akili from a basic chatbot
# ============================================================

import os
import logging
from datetime import datetime
from anthropic import Anthropic

log = logging.getLogger("AKILI.Formatter")
ANTHROPIC_KEY = os.environ["ANTHROPIC_API_KEY"]

# ── Telegram supports these markdown elements ─────────────────
# *bold* _italic_ `code` ```block``` [link](url)
# Max message length: 4096 chars

AGENT_HEADERS = {
    "SHIELD":  "🛡 *SHIELD* — Security & Infrastructure",
    "PULSE":   "📡 *PULSE* — Social Media & Content",
    "REACH":   "📨 *REACH* — Communications & Outreach",
    "INTEL":   "🔍 *INTEL* — Strategy & Intelligence",
    "AMPLIFY": "🔊 *AMPLIFY* — Music & Brand Growth",
    "CORE":    "⚡ *AKILI CORE* — Command Center",
    "CONTENT": "🗓 *CONTENT ENGINE* — Weekly Planner",
    "CRONS":   "🕐 *SCHEDULER* — Autonomous Operations",
}

DIVIDER       = "━━━━━━━━━━━━━━━━━━━━"
LIGHT_DIVIDER = "─ ─ ─ ─ ─ ─ ─ ─ ─ ─"


class TelegramFormatter:
    """
    Shared formatting layer used by all 5 agents.
    Every output gets structured, creative, and detailed treatment.
    No plain walls of text. No generic responses.
    """

    def __init__(self):
        self.client = Anthropic(api_key=ANTHROPIC_KEY)

    # ── Master formatter ──────────────────────────────────────
    def format(self, agent: str, content_type: str, data: dict) -> str:
        """
        Route to the correct formatter based on content type.
        content_type options:
          report, alert, approval, brief, campaign, research,
          reply_draft, post_ready, status, error, milestone
        """
        header  = AGENT_HEADERS.get(agent.upper(), f"⚡ *{agent}*")
        ts      = datetime.now().strftime("%H:%M")

        formatters = {
            "report":       self._format_report,
            "alert":        self._format_alert,
            "approval":     self._format_approval,
            "brief":        self._format_brief,
            "campaign":     self._format_campaign,
            "research":     self._format_research,
            "reply_draft":  self._format_reply_draft,
            "post_ready":   self._format_post_ready,
            "status":       self._format_status,
            "error":        self._format_error,
            "milestone":    self._format_milestone,
            "weekly_plan":  self._format_weekly_plan,
        }

        formatter = formatters.get(content_type, self._format_generic)
        body = formatter(data)
        return f"{header}\n`{ts}`\n\n{body}"

    # ── Report ────────────────────────────────────────────────
    def _format_report(self, d: dict) -> str:
        sections = []
        if d.get("summary"):
            sections.append(f"📋 *Summary*\n{d['summary']}")
        if d.get("metrics"):
            m = d["metrics"]
            metric_lines = "\n".join([f"  • {k}: `{v}`" for k, v in m.items()])
            sections.append(f"📊 *Metrics*\n{metric_lines}")
        if d.get("issues"):
            issue_lines = "\n".join([f"  ⚠️ {i}" for i in d["issues"]])
            sections.append(f"🚨 *Issues Detected*\n{issue_lines}")
        if d.get("actions"):
            action_lines = "\n".join([f"  {i+1}. {a}" for i, a in enumerate(d["actions"])])
            sections.append(f"⚡ *Required Actions*\n{action_lines}")
        if d.get("next_check"):
            sections.append(f"🕐 *Next check:* {d['next_check']}")
        return f"\n{DIVIDER}\n".join(sections)

    # ── Alert ─────────────────────────────────────────────────
    def _format_alert(self, d: dict) -> str:
        severity_icons = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
        icon = severity_icons.get(d.get("severity", "high"), "🟠")
        return (
            f"{icon} *{d.get('severity', 'HIGH').upper()} ALERT*\n\n"
            f"{DIVIDER}\n"
            f"*What happened:*\n{d.get('what', 'Unknown event')}\n\n"
            f"*Affected:* `{d.get('affected', 'Unknown')}`\n"
            f"*Detected at:* `{d.get('time', datetime.now().strftime('%H:%M'))}`\n\n"
            f"*Action taken:* {d.get('action_taken', 'Logged and monitoring')}\n\n"
            f"*Do you need to act?* {d.get('justin_action', 'No — Akili handling it')}\n"
            f"{DIVIDER}"
        )

    # ── Post approval ─────────────────────────────────────────
    def _format_approval(self, d: dict) -> str:
        platform_icons = {
            "instagram": "📸", "twitter": "🐦", "linkedin": "💼",
            "tiktok": "🎵", "facebook": "📘", "snapchat": "👻",
        }
        icon = platform_icons.get(d.get("platform", "").lower(), "📱")
        accounts_str = " · ".join([f"@{a}" for a in d.get("accounts", [])])
        hashtags_str = " ".join(d.get("hashtags", []))
        return (
            f"{icon} *{d.get('platform','').upper()} — POST READY FOR APPROVAL*\n\n"
            f"*Accounts:* {accounts_str}\n"
            f"*Theme:* _{d.get('theme', '')}_\n"
            f"*Best time to post:* `{d.get('best_time', 'Now')}`\n\n"
            f"{DIVIDER}\n"
            f"{d.get('caption', '')}\n\n"
            f"_{hashtags_str}_\n"
            f"{DIVIDER}\n\n"
            f"📸 *Visual:* {d.get('visual_note', 'Choose a strong on-brand image')}\n"
            f"🎯 *Goal:* {d.get('goal', 'Engagement + brand awareness')}\n\n"
            f"*Reply:*\n"
            f"✅ `POST {d.get('approval_id', '')}` — publish now\n"
            f"✏️ `EDIT {d.get('approval_id', '')} [your version]` — rewrite + publish\n"
            f"❌ `SKIP {d.get('approval_id', '')}` — drop this post"
        )

    # ── Morning brief ─────────────────────────────────────────
    def _format_brief(self, d: dict) -> str:
        day   = datetime.now().strftime("%A, %B %d")
        lines = [
            f"☀️ *GOOD MORNING, JUSTIN*\n_{day}_\n",
            f"{DIVIDER}\n",
        ]
        if d.get("yesterday"):
            lines.append(f"📊 *Yesterday's Highlights*\n{d['yesterday']}\n")
        if d.get("news"):
            news_items = "\n".join([f"  • {n}" for n in d["news"]])
            lines.append(f"🌍 *Market Intel*\n{news_items}\n")
        if d.get("priorities"):
            pri_items = "\n".join([f"  {i+1}. {p}" for i, p in enumerate(d["priorities"])])
            lines.append(f"🎯 *Today's Top 3*\n{pri_items}\n")
        if d.get("opportunity"):
            lines.append(f"💡 *Opportunity*\n{d['opportunity']}\n")
        if d.get("product_spotlight"):
            lines.append(f"📈 *Product Watch*\n{d['product_spotlight']}\n")
        lines.append(f"{DIVIDER}\n_Akili is running. You focus on what only you can do._")
        return "\n".join(lines)

    # ── Campaign summary ──────────────────────────────────────
    def _format_campaign(self, d: dict) -> str:
        return (
            f"🚀 *{d.get('title', 'CAMPAIGN')}*\n\n"
            f"{DIVIDER}\n"
            f"*What we're launching:* {d.get('what', '')}\n"
            f"*Target:* {d.get('target', '')}\n"
            f"*Timeline:* {d.get('timeline', '')}\n\n"
            f"*Phase 1 — {d.get('phase1_label','Pre-launch')}*\n"
            f"{d.get('phase1', '')}\n\n"
            f"*Phase 2 — {d.get('phase2_label','Launch')}*\n"
            f"{d.get('phase2', '')}\n\n"
            f"*Phase 3 — {d.get('phase3_label','Sustain')}*\n"
            f"{d.get('phase3', '')}\n\n"
            f"{DIVIDER}\n"
            f"🎯 *KPIs:*\n{d.get('kpis', '')}\n\n"
            f"⚡ *First action:* {d.get('first_action', 'Start now')}"
        )

    # ── Research result ───────────────────────────────────────
    def _format_research(self, d: dict) -> str:
        finding_lines = "\n".join([f"  {i+1}. {f}" for i, f in enumerate(d.get("findings", []))])
        source_lines  = " · ".join([f"[{s}]" for s in d.get("sources", [])[:4]])
        return (
            f"*Query:* _{d.get('query', '')}_\n"
            f"*Searched:* {d.get('source_count', '?')} sources\n\n"
            f"{DIVIDER}\n"
            f"📌 *Key Findings*\n{finding_lines}\n\n"
            f"💡 *CREOVA Angle*\n{d.get('creova_angle', '')}\n\n"
            f"⚡ *Recommended Action*\n{d.get('action', '')}\n\n"
            f"{DIVIDER}\n"
            f"_Confidence: {d.get('confidence', 'Medium')} | Sources: {source_lines}_"
        )

    # ── Reply draft ───────────────────────────────────────────
    def _format_reply_draft(self, d: dict) -> str:
        return (
            f"*From:* {d.get('from', 'Unknown')}\n"
            f"*Channel:* {d.get('channel', 'Email')}\n"
            f"*Type:* _{d.get('type', 'General')}_ | *Priority:* {d.get('priority', '5')}/10\n\n"
            f"{DIVIDER}\n"
            f"📩 *Their message:*\n_{d.get('their_message', '')[:200]}_\n\n"
            f"✍️ *My draft reply:*\n{d.get('draft', '')}\n"
            f"{DIVIDER}\n\n"
            f"Reply `SENDDRAFT` to send · `EDITDRAFT [your changes]` to modify\n"
            f"Or reply `SKIP` to handle manually"
        )

    # ── Status ────────────────────────────────────────────────
    def _format_status(self, d: dict) -> str:
        agent_lines = "\n".join([
            f"  {'✅' if v == 'active' else '⚠️'} *{k}:* {v}"
            for k, v in d.get("agents", {}).items()
        ])
        platform_lines = "\n".join([
            f"  {'🟢' if v else '🔴'} {k}"
            for k, v in d.get("platforms", {}).items()
        ])
        return (
            f"*System:* AKILI OS Phase 4\n"
            f"*Uptime:* {d.get('uptime', 'Running')}\n\n"
            f"{DIVIDER}\n"
            f"*Agents:*\n{agent_lines}\n\n"
            f"*Platforms:*\n{platform_lines}\n\n"
            f"{DIVIDER}\n"
            f"*Pending approvals:* {d.get('pending', 0)}\n"
            f"*Emails handled today:* {d.get('emails_today', 0)}\n"
            f"*Posts sent today:* {d.get('posts_today', 0)}\n"
            f"*Next heartbeat:* {d.get('next_heartbeat', '30 min')}"
        )

    # ── Error ─────────────────────────────────────────────────
    def _format_error(self, d: dict) -> str:
        return (
            f"⚠️ *Error Detected*\n\n"
            f"{DIVIDER}\n"
            f"*Agent:* {d.get('agent', 'Unknown')}\n"
            f"*What failed:* {d.get('what', 'Unknown error')}\n"
            f"*Error:* `{d.get('error', '')[:200]}`\n\n"
            f"*Auto-recovery:* {d.get('recovery', 'Logging and retrying in 30 min')}\n"
            f"*Do you need to act?* {d.get('justin_action', 'No — monitoring')}\n"
            f"{DIVIDER}\n"
            f"_Logged at {datetime.now().strftime('%H:%M')} · Full log in Replit console_"
        )

    # ── Milestone ─────────────────────────────────────────────
    def _format_milestone(self, d: dict) -> str:
        return (
            f"🎉 *MILESTONE HIT!*\n\n"
            f"{DIVIDER}\n"
            f"*{d.get('what', '')}*\n\n"
            f"_{d.get('context', '')}_\n\n"
            f"📱 *Celebration posts ready:*\n{d.get('posts_preview', '')}\n\n"
            f"{DIVIDER}\n"
            f"Reply `CELEBRATE` to post across all accounts now"
        )

    # ── Weekly plan ───────────────────────────────────────────
    def _format_weekly_plan(self, d: dict) -> str:
        header = (
            f"🗓 *WEEK AHEAD — {d.get('week_range', '')}*\n\n"
            f"{DIVIDER}\n"
            f"*Accounts covered:* 10 social accounts\n"
            f"*Posts planned:* {d.get('total_posts', 0)}\n"
            f"*Campaigns active:* {d.get('campaigns', 0)}\n\n"
        )
        day_previews = []
        for day_data in d.get("days", [])[:3]:   # First 3 days in summary
            day_previews.append(
                f"*{day_data.get('day')}* — _{day_data.get('theme')}_\n"
                f"  📸 IG: {day_data.get('ig_preview', '')[:80]}...\n"
                f"  🐦 X: {day_data.get('twitter_preview', '')[:60]}..."
            )
        return header + "\n\n".join(day_previews) + f"\n\n{DIVIDER}\n_Full week queued. Posts sent for approval at scheduled times._"

    # ── Generic fallback ──────────────────────────────────────
    def _format_generic(self, d: dict) -> str:
        content = d.get("content", d.get("text", str(d)))
        return f"{DIVIDER}\n{content}\n{DIVIDER}"

    # ── AI-enhanced formatting ────────────────────────────────
    async def ai_enhance(self, raw_text: str, agent: str, context: str = "") -> str:
        """
        Pass any raw agent output through Claude to make it
        more creative, clearer, and better structured.
        Used for complex outputs that don't fit standard templates.
        """
        prompt = f"""
You are formatting a response from the {agent} agent of AKILI — Justin Mafie's AI OS.

Raw output to format:
{raw_text}

Context: {context}

Rules:
1. Use Telegram markdown: *bold*, _italic_, `code`, ```blocks```
2. Structure with clear sections using headers
3. Use relevant emojis (not excessive — 1-2 per section max)
4. Keep CREOVA brand voice — visionary, authentic, African excellence
5. Use the divider ━━━━━━━━━━━━━━━━━━━━ between major sections
6. End with a clear action item or next step
7. Max 3800 chars (Telegram limit)
8. Make it feel premium — this is a founder's personal AI, not a chatbot

Return ONLY the formatted text. No explanation.
"""
        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()


# ── Global formatter instance ─────────────────────────────────
formatter = TelegramFormatter()
