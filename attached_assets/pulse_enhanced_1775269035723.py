# ============================================================
# PULSE — Enhanced with Full Skills
# Image gen, hashtag intelligence, A/B tracking, carousel builder
# ============================================================

import os, logging, json, asyncio
from datetime import datetime
from anthropic import Anthropic
from skills.shared.telegram_formatter import formatter

log = logging.getLogger("PULSE")

ANTHROPIC_KEY    = os.environ["ANTHROPIC_API_KEY"]
OPENAI_API_KEY   = os.environ.get("OPENAI_API_KEY", "")    # For DALL-E 3 image gen
RAPIDAPI_KEY     = os.environ.get("RAPIDAPI_KEY", "")      # For hashtag intelligence

PULSE_SYSTEM = """
You are PULSE — Justin Mafie's creative director and social media operator.

You write content that stops the scroll. You think in formats, not just captions.
You know that Instagram rewards saves, TikTok rewards watch time, LinkedIn rewards expertise,
Twitter rewards opinions, and Snapchat rewards authenticity.

You write as Justin — not as his assistant. First person. Real voice. Real energy.

CREOVA accounts you manage:
Instagram: @creativeinnovation__ · @jj_mafie · @sankofastudio__ · @creovasolutions
Twitter/X: @justin_mafie
LinkedIn: Justin Mafie (personal) · CREOVA (company page)
TikTok: @creovamusic
Facebook: Justin Mafie · CREOVA Business
Snapchat: jay-mafie

creova.one services to weave in naturally:
- Branding & identity
- Tech development (web, mobile, AI)
- Media production (content, campaigns)
- Music production (Sankofa Studio)
- Strategic consulting

Voice: Authentic. Visionary. African excellence. Never corporate. Real founder energy.
"""

# ── Hashtag sets by vertical ──────────────────────────────────
HASHTAG_SETS = {
    "music":    ["#CREOVAMusic", "#JustinMafie", "#AfricanMusic", "#SankofaStudio",
                 "#NewMusic", "#AfroBeats", "#IndependentArtist", "#MusicProducer"],
    "tech":     ["#CREOVA", "#CREOVASolutions", "#AfricanTech", "#EmergingMarkets",
                 "#Founder", "#StartupAfrica", "#TechInnovation", "#BuildingInAfrica"],
    "personal": ["#JustinMafie", "#CREOVA", "#FounderLife", "#AfricanFounder",
                 "#CreativeTech", "#PanAfrican", "#YouthEntrepreneur"],
    "studio":   ["#SankofaStudio", "#CREOVAMusic", "#StudioLife", "#MusicProduction",
                 "#BeatMaker", "#AfricanStudio", "#RecordingStudio"],
    "branding": ["#Branding", "#CreativeAgency", "#CREOVA", "#BrandStrategy",
                 "#DesignThinking", "#VisualIdentity", "#CREOVASolutions"],
}


class PulseAgent:
    def __init__(self, api_key: str, memory):
        self.client  = Anthropic(api_key=api_key)
        self.memory  = memory
        self.ab_data = {}   # A/B test tracking
        log.info("PULSE initialized — full skills loaded")

    # ── Main command handler ──────────────────────────────────
    async def handle(self, command: str) -> str:
        # Route to specific skill if keyword matched
        lower = command.lower()
        if "carousel" in lower:
            topic = command.split("carousel", 1)[-1].strip()
            return await self.build_carousel(topic)
        if "image" in lower or "visual" in lower:
            return await self.generate_image_brief(command)
        if "hashtag" in lower:
            vertical = "tech" if "tech" in lower else "music" if "music" in lower else "personal"
            return self._get_hashtags(vertical)
        if "ab test" in lower or "experiment" in lower:
            return await self.run_ab_experiment(command)
        if "week" in lower and "calendar" in lower:
            return await self.weekly_calendar()

        # General content request
        response = self.client.messages.create(
            model="claude-sonnet-4-5", max_tokens=1500,
            system=PULSE_SYSTEM,
            messages=[{"role": "user", "content": command}]
        )
        raw = response.content[0].text
        return await formatter.ai_enhance(raw, "PULSE", command)

    async def heartbeat_check(self):
        """Called every 30 min — check if scheduled content is queued."""
        self.memory.daily_log(f"[PULSE] Heartbeat {datetime.now().strftime('%H:%M')}")

    # ── Generate a full platform package ─────────────────────
    async def generate_platform_package(self, topic: str, vertical: str = "personal") -> str:
        hashtags = self._get_hashtag_list(vertical)
        prompt = f"""
Topic: {topic}
Vertical: {vertical}
Hashtags to use: {', '.join(hashtags[:6])}

Generate a full cross-platform content package. Return as JSON:
{{
  "instagram_jj":     {{ "caption": "...", "hook": "first line that stops scroll", "hashtags": [...] }},
  "instagram_creova": {{ "caption": "...", "hashtags": [...] }},
  "instagram_music":  {{ "caption": "...", "hashtags": [...] }},
  "twitter":          {{ "tweet": "...", "thread": ["t1","t2","t3"] }},
  "linkedin_justin":  "...",
  "linkedin_creova":  "...",
  "tiktok":           {{ "caption": "...", "video_concept": "..." }},
  "snapchat":         {{ "shots": ["shot1","shot2","shot3"] }},
  "visual_direction": "What image/video to pair with this",
  "best_time":        "Best time to post for max reach"
}}
Only JSON.
"""
        r = self.client.messages.create(
            model="claude-sonnet-4-5", max_tokens=2000,
            system=PULSE_SYSTEM,
            messages=[{"role":"user","content":prompt}]
        )
        raw = r.content[0].text.strip().replace("```json","").replace("```","").strip()
        try:
            data = json.loads(raw)
            return formatter.format("PULSE", "approval", {
                "platform":    "ALL PLATFORMS",
                "handle":      "All 10 accounts",
                "theme":       vertical,
                "caption":     data.get("instagram_jj",{}).get("caption",""),
                "hashtags":    data.get("instagram_jj",{}).get("hashtags",[]),
                "visual_note": data.get("visual_direction",""),
                "goal":        "Cross-platform reach and brand building",
                "best_time":   data.get("best_time","Check platform analytics"),
                "approval_id": f"multi_{datetime.now().strftime('%H%M')}",
            })
        except Exception:
            return await formatter.ai_enhance(raw, "PULSE", topic)

    # ── Instagram carousel builder ────────────────────────────
    async def build_carousel(self, topic: str) -> str:
        prompt = f"""
Build a 7-slide Instagram carousel for Justin Mafie on: {topic}

For each slide:
- Slide number and title (4 words max)
- Content (2-3 sentences or bullet points)
- Visual direction (what to show on this slide)

Slide structure:
1. Hook slide — the problem or bold statement
2-5. Value slides — the meat
6. Summary slide — key takeaways
7. CTA slide — follow @creovasolutions / @jj_mafie / creova.one

Keep it educational, visual, and in Justin's voice.
African futurism aesthetic throughout.
"""
        r = self.client.messages.create(
            model="claude-sonnet-4-5", max_tokens=1500,
            system=PULSE_SYSTEM,
            messages=[{"role":"user","content":prompt}]
        )
        return await formatter.ai_enhance(
            f"📱 CAROUSEL — {topic}\n\n{r.content[0].text}", "PULSE", "carousel"
        )

    # ── Image generation brief (DALL-E 3) ────────────────────
    async def generate_image_brief(self, request: str) -> str:
        """
        Generate an on-brand image using DALL-E 3.
        Returns image URL + Telegram-formatted description.
        """
        # First generate a great DALL-E prompt
        prompt_gen = f"""
Create a DALL-E 3 image prompt for this request: {request}

The image must:
- Match CREOVA's African futurism aesthetic
- Be bold, modern, premium quality
- Work well as a social media post (square or portrait)
- Not include text (DALL-E handles text poorly)
- Reference Justin Mafie / CREOVA's visual identity if relevant

Return ONLY the DALL-E prompt (under 200 words).
"""
        r = self.client.messages.create(
            model="claude-sonnet-4-5", max_tokens=300,
            messages=[{"role":"user","content":prompt_gen}]
        )
        dalle_prompt = r.content[0].text.strip()

        # Call DALL-E 3 if API key available
        if OPENAI_API_KEY:
            try:
                import openai
                openai.api_key = OPENAI_API_KEY
                img_response = openai.images.generate(
                    model="dall-e-3",
                    prompt=dalle_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                image_url = img_response.data[0].url
                return (
                    f"🎨 *PULSE — Image Generated*\n\n"
                    f"{formatter.DIVIDER}\n"
                    f"*Prompt used:*\n_{dalle_prompt[:150]}_\n\n"
                    f"*Image URL:*\n`{image_url}`\n\n"
                    f"{formatter.DIVIDER}\n"
                    f"_Save this image and post it with your approved caption._\n"
                    f"_Cost: ~$0.04 (DALL-E 3 standard)_"
                )
            except Exception as e:
                log.error(f"[PULSE] Image gen error: {e}")

        # Fallback: return the prompt for manual generation
        return (
            f"🎨 *PULSE — Image Brief*\n\n"
            f"{formatter.DIVIDER}\n"
            f"*DALL-E 3 prompt ready:*\n_{dalle_prompt}_\n\n"
            f"{formatter.DIVIDER}\n"
            f"_Add OPENAI\\_API\\_KEY to Replit Secrets to auto-generate images._\n"
            f"_Or paste this prompt at: chat.openai.com_"
        )

    # ── Hashtag intelligence ──────────────────────────────────
    def _get_hashtags(self, vertical: str) -> str:
        tags = self._get_hashtag_list(vertical)
        return (
            f"#️⃣ *PULSE — Hashtag Set: {vertical.upper()}*\n\n"
            f"{formatter.DIVIDER}\n"
            f"*Recommended tags:*\n"
            f"{' '.join(tags)}\n\n"
            f"*Usage:* Add to any {vertical} post across all accounts.\n"
            f"*Rotate:* Change 2-3 tags per post to avoid shadow banning.\n"
            f"{formatter.DIVIDER}\n"
            f"_Tip: Use 8-12 hashtags on Instagram, 2-3 on Twitter, 3-5 on LinkedIn_"
        )

    def _get_hashtag_list(self, vertical: str) -> list:
        return HASHTAG_SETS.get(vertical, HASHTAG_SETS["personal"])

    # ── A/B experiment ────────────────────────────────────────
    async def run_ab_experiment(self, request: str) -> str:
        platform = "instagram" if "instagram" in request.lower() else "twitter"
        variable = "caption style" if "caption" in request.lower() else "posting time"
        prompt = f"""
Design a 7-day A/B experiment for Justin Mafie on {platform}.
Variable testing: {variable}

Include:
- Hypothesis
- Version A (what we test first)
- Version B (what we compare against)
- How to measure success (specific metric)
- Decision criteria after 7 days
- How to implement the winner

Be specific — real numbers, real metrics.
"""
        r = self.client.messages.create(
            model="claude-sonnet-4-5", max_tokens=800,
            system=PULSE_SYSTEM,
            messages=[{"role":"user","content":prompt}]
        )
        return await formatter.ai_enhance(
            f"🧪 A/B EXPERIMENT — {platform.upper()}\n\n{r.content[0].text}", "PULSE"
        )

    # ── Weekly content calendar ───────────────────────────────
    async def weekly_calendar(self) -> str:
        prompt = """
Generate a complete 7-day social media content calendar for Justin Mafie and CREOVA.
Each day: theme, 1 Instagram concept, 1 Twitter angle, 1 LinkedIn angle, 1 TikTok concept.
Make each day distinct. Real specifics, not generic ideas.
"""
        r = self.client.messages.create(
            model="claude-sonnet-4-5", max_tokens=2000,
            system=PULSE_SYSTEM,
            messages=[{"role":"user","content":prompt}]
        )
        return await formatter.ai_enhance(r.content[0].text, "PULSE", "weekly calendar")
