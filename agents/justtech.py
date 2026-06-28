# ============================================================
# JUSTTECH — Faceless YouTube Production Agent (AKILI)
# Channel: @JustTech-m15 — B2B SaaS / Startups / Tech Economics
# Produces full episode packages and IMPROVES ITSELF over time:
#   • Reliability loop  → QA gate + retries on every generation
#   • Learning loop      → weekly retrospective rewrites lessons.md,
#                          which is injected into every future script
# ============================================================

import os
import re
import json
import asyncio
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from anthropic import AsyncAnthropic

ET = ZoneInfo("America/Toronto")
log = logging.getLogger("JUSTTECH")

SCRIPT_MODEL = "claude-sonnet-4-5"

BRAND = """
You are JUSTTECH, the head writer for a faceless YouTube documentary channel.

CHANNEL: JustTech (@JustTech-m15)
NICHE: B2B Software, Startups, Tech Economics.
AUDIENCE: Entrepreneurs, developers, professionals 18–44, high income.
POSITIONING: "The Wall Street Journal meets cinematic true crime."
VOICE: Authoritative, analytical, slightly skeptical, narrative-driven.

CONTENT PILLARS:
- THE AUTOPSY  → rise & fall of companies / SaaS bankruptcies
- THE ARCHITECT→ psychology & strategy of tech founders
- THE ENGINE   → unit economics & architecture of opaque tech monopolies

NON-NEGOTIABLE STRUCTURE: Hook → Context → Build-up/Tension → Payoff.
A pattern interrupt every ~10–15 seconds. Optimize for Average View Duration.

ANTI-"AI SLOP" RULES (YouTube demonetizes generic AI content):
- Original framing, diverse vocabulary, a distinct narrative arc.
- Specific numbers, names, dates — never vague filler.
- Never these phrases: "in today's video", "without further ado", "let's dive in",
  "in conclusion", "buckle up", "game-changer", "in this digital age".
- Cite real, checkable facts; flag anything uncertain as [VERIFY].
"""


class JustTechAgent:
    def __init__(self, api_key: str, memory, voice=None):
        self.client = AsyncAnthropic(api_key=api_key)
        self.memory = memory
        self.voice = voice                      # VoiceEngine for narration
        self.base = "akili-life/projects/justtech"
        os.makedirs(self.base, exist_ok=True)
        self.ledger = os.path.join(self.base, "episodes.jsonl")
        self.lessons_path = os.path.join(self.base, "lessons.md")
        self.last_script = ""                   # for the /jt voiceover step
        log.info("JUSTTECH agent initialized (self-improving pipeline)")

    # ── learning-loop input: lessons learned so far ───────────
    def _lessons(self) -> str:
        if os.path.exists(self.lessons_path):
            try:
                with open(self.lessons_path) as f:
                    txt = f.read().strip()
                    if txt:
                        return f"\nLESSONS FROM PAST EPISODES (apply these):\n{txt}\n"
            except Exception:
                pass
        return "\n(No past lessons yet — this is an early episode.)\n"

    # ── resilient Claude call with retries ────────────────────
    async def _ask(self, prompt: str, max_tokens: int, attempts: int = 3) -> str:
        last = ""
        for i in range(attempts):
            try:
                r = await self.client.messages.create(
                    model=SCRIPT_MODEL, max_tokens=max_tokens,
                    system=BRAND + self._lessons(),
                    messages=[{"role": "user", "content": prompt}],
                )
                return r.content[0].text
            except Exception as e:
                last = str(e)
                log.warning(f"[JUSTTECH] attempt {i+1}/{attempts} failed: {e}")
                await asyncio.sleep(2 * (i + 1))
        raise RuntimeError(f"Claude failed after {attempts} attempts: {last}")

    @staticmethod
    def _parse_json(text: str) -> dict:
        t = text.strip()
        t = re.sub(r"^```(?:json)?|```$", "", t.strip(), flags=re.MULTILINE).strip()
        a, b = t.find("{"), t.rfind("}")
        if a != -1 and b != -1:
            t = t[a:b + 1]
        return json.loads(t)

    # ── reliability loop: QA gate (credit-smart) ──────────────
    # Returns (ok, issues). `ok` is False only on HARD/structural problems
    # worth a (costly) regeneration. Minor shortfalls are logged as "(soft)"
    # notes and accepted, so we don't burn API credits on near-misses.
    @staticmethod
    def qa_gate(ep: dict) -> tuple[bool, list[str]]:
        issues, hard = [], False
        script = ep.get("script", "") or ""
        words = len(script.split())
        if words < 1000:
            issues.append(f"script too short ({words}w, need ≥1000)"); hard = True
        elif words < 1200:
            issues.append(f"script a touch short ({words}w; target ~1500) (soft)")
        hook = ep.get("hook", "") or ""
        if not hook:
            issues.append("missing hook"); hard = True
        elif len(re.split(r"(?<=[.!?])\s+", hook)) > 3:
            issues.append("hook longer than 3 sentences (soft)")
        if len(ep.get("scenes", []) or []) < 8:
            issues.append("fewer than 8 scenes"); hard = True
        if len(ep.get("shorts", []) or []) < 3:
            issues.append("fewer than 3 shorts"); hard = True
        md = ep.get("metadata", {}) or {}
        if len(md.get("tags", []) or []) < 8:
            issues.append("fewer than 8 tags (soft)")
        banned = ["in today's video", "without further ado", "let's dive in",
                  "buckle up", "game-changer", "in this digital age", "in conclusion"]
        hits = [b for b in banned if b in script.lower()]
        if hits:
            issues.append("AI-slop phrases: " + ", ".join(hits)); hard = True
        return (not hard, issues)

    # ── main: generate a full episode package ─────────────────
    async def generate_episode(self, topic: str) -> str:
        prompt = self._episode_prompt(topic)
        ep = None
        for attempt in range(2):
            raw = await self._ask(prompt, 8000)
            try:
                ep = self._parse_json(raw)
            except Exception as e:
                log.warning(f"[JUSTTECH] JSON parse failed: {e}")
                ep = None
            if ep:
                ok, issues = self.qa_gate(ep)
                if ok:
                    break
                log.info(f"[JUSTTECH] QA failed: {issues} — regenerating stricter")
                prompt = self._episode_prompt(topic, fix=issues)
        if not ep:
            return "⚠️ JUSTTECH — generation failed after retries. Try a sharper topic."

        self.last_script = ep.get("script", "")
        rec = self._log_episode(topic, ep)
        await self.memory.daily_log(f"[JUSTTECH] Episode #{rec['id']}: {topic[:50]}")
        return self._format(ep, rec["id"])

    def _episode_prompt(self, topic: str, fix: list[str] | None = None) -> str:
        fixline = f"\nThe previous draft FAILED QA for: {', '.join(fix)}. Fix all of these.\n" if fix else ""
        return f"""Create a complete JustTech episode on: "{topic}".{fixline}
Return ONLY valid JSON (no prose, no code fences) with EXACTLY this shape:
{{
  "pillar": "The Autopsy | The Architect | The Engine",
  "title": "<YouTube title, <70 chars, curiosity + specificity>",
  "hook": "<spoken first 15 seconds, 1-3 sentences, no fluff>",
  "script": "<full 1500-word narration, Hook→Context→Build-up→Payoff, pattern interrupts, specific numbers/names/dates, mark uncertain facts [VERIFY]>",
  "scenes": [
    {{"timecode":"0:00","visual":"<what's on screen: archival/B-roll/chart>","source":"<Archive.org / Pexels / NASA / chart via Remotion>"}}
  ],
  "thumbnail_prompt": "<Midjourney/Higgsfield prompt for a high-contrast cinematic thumbnail>",
  "thumbnail_text": "<3-5 word overlay>",
  "metadata": {{
    "title": "<SEO title>",
    "description": "<150-word description with timestamps + 1 CTA>",
    "tags": ["<10-15 SEO tags>"]
  }},
  "shorts": [
    {{"clip":"<which 30-45s of the script>","caption":"<hook caption>"}}
  ]
}}
Need ≥8 scenes, ≥3 shorts, ≥10 tags, script ≥1200 words. Use only public-domain/licensed visual sources.
"""

    def _format(self, ep: dict, ep_id: int) -> str:
        md = ep.get("metadata", {}) or {}
        scenes = ep.get("scenes", []) or []
        shorts = ep.get("shorts", []) or []
        lines = [
            f"🎬 JUSTTECH — Episode #{ep_id}",
            "━━━━━━━━━━━━━━━━━━━━",
            f"▸ Pillar: {ep.get('pillar','?')}",
            f"▸ Title: {ep.get('title','?')}",
            "",
            f"🎯 HOOK\n{ep.get('hook','')}",
            "",
            f"📝 SCRIPT ({len((ep.get('script','') or '').split())} words)",
            ep.get("script", ""),
            "",
            "🎞 SCENES",
        ]
        for s in scenes[:12]:
            lines.append(f"  ◦ {s.get('timecode','')} — {s.get('visual','')}  [{s.get('source','')}]")
        lines += [
            "",
            f"🖼 THUMBNAIL\n  prompt: {ep.get('thumbnail_prompt','')}\n  text: {ep.get('thumbnail_text','')}",
            "",
            "🔎 METADATA",
            f"  title: {md.get('title','')}",
            f"  tags: {', '.join(md.get('tags', []) or [])}",
            "",
            f"  description:\n{md.get('description','')}",
            "",
            "✂️ SHORTS",
        ]
        for i, sh in enumerate(shorts[:3], 1):
            lines.append(f"  {i}. {sh.get('caption','')} — {sh.get('clip','')}")
        lines += ["", "⚡ Next: I can narrate this (ElevenLabs/OpenAI VO) — reply with /jt to get the audio."]
        return "\n".join(lines)

    # ── ledger ────────────────────────────────────────────────
    def _log_episode(self, topic: str, ep: dict) -> dict:
        ep_id = self._next_id()
        rec = {
            "id": ep_id,
            "ts": datetime.now(ET).isoformat(),
            "topic": topic,
            "pillar": ep.get("pillar"),
            "title": ep.get("title"),
            "words": len((ep.get("script", "") or "").split()),
            "metrics": {},          # filled later via record_metrics
        }
        try:
            with open(self.ledger, "a") as f:
                f.write(json.dumps(rec) + "\n")
            with open(os.path.join(self.base, f"episode_{ep_id:03d}.json"), "w") as f:
                json.dump(ep, f, indent=2)
        except Exception as e:
            log.error(f"[JUSTTECH] ledger write failed: {e}")
        return rec

    def _next_id(self) -> int:
        if not os.path.exists(self.ledger):
            return 1
        try:
            with open(self.ledger) as f:
                return sum(1 for _ in f) + 1
        except Exception:
            return 1

    def _read_ledger(self) -> list[dict]:
        if not os.path.exists(self.ledger):
            return []
        out = []
        try:
            with open(self.ledger) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        out.append(json.loads(line))
        except Exception:
            pass
        return out

    async def record_metrics(self, ep_id: int, views: int, retention_pct: float,
                             ctr_pct: float = 0.0) -> str:
        rows = self._read_ledger()
        found = False
        for r in rows:
            if r.get("id") == ep_id:
                r["metrics"] = {"views": views, "retention_pct": retention_pct, "ctr_pct": ctr_pct}
                found = True
        if not found:
            return f"⚠️ JUSTTECH — no episode #{ep_id} in the ledger."
        try:
            with open(self.ledger, "w") as f:
                for r in rows:
                    f.write(json.dumps(r) + "\n")
        except Exception as e:
            return f"⚠️ JUSTTECH — failed to save metrics: {e}"
        return (f"📊 JUSTTECH — logged episode #{ep_id}: {views:,} views · "
                f"{retention_pct:.0f}% retention · {ctr_pct:.1f}% CTR.\n"
                f"⚡ Run /jt_retro to fold this into the next scripts.")

    # ── LEARNING LOOP: retrospective rewrites lessons.md ──────
    async def retrospective(self) -> str:
        rows = self._read_ledger()
        if not rows:
            return "🔁 JUSTTECH — no episodes logged yet. Generate a few first."
        scored = [r for r in rows if r.get("metrics")]
        summary = json.dumps(rows[-20:], indent=2)
        prompt = f"""You are optimizing the JustTech channel. Here are recent episodes
(with metrics where available — views, retention_pct, ctr_pct):

{summary}

Analyze what correlates with higher retention and CTR. Then output a concise
LESSONS file (markdown, <350 words) of CONCRETE do/don't rules for future scripts,
titles, hooks, and thumbnails. Be specific (e.g. "hooks that open on a dollar figure
beat hooks that open on a question"). If metrics are sparse, give principled defaults
for this niche. Output ONLY the markdown lessons, no preamble."""
        try:
            lessons = await self._ask(prompt, 1200)
        except Exception as e:
            return f"⚠️ JUSTTECH retrospective error: {e}"
        try:
            with open(self.lessons_path, "w") as f:
                f.write(f"# JustTech Lessons — updated {datetime.now(ET).date()}\n\n{lessons.strip()}\n")
        except Exception as e:
            log.error(f"[JUSTTECH] lessons write failed: {e}")
        await self.memory.daily_log("[JUSTTECH] retrospective updated lessons.md")
        n_scored = len(scored)
        return (f"🔁 JUSTTECH — Retrospective complete ({len(rows)} eps, {n_scored} with metrics).\n"
                f"Lessons updated and now applied to every future script.\n\n{lessons.strip()[:1500]}")

    async def suggest_topics(self, n: int = 3) -> str:
        recent = [r.get("title", "") for r in self._read_ledger()[-15:]]
        prompt = f"""Propose {n} fresh JustTech episode topics (avoid overlap with these recent ones:
{recent}). For each: pillar, working title (<70 chars), and a one-line hook.
Pick topics with real search demand and a clear narrative. Output as a tight numbered list."""
        try:
            out = await self._ask(prompt, 900)
        except Exception as e:
            return f"⚠️ JUSTTECH error: {e}"
        return f"🧠 JUSTTECH — Topic Queue\n━━━━━━━━━━━━━━━━━━━━\n{out}"

    async def make_voiceover(self, script: str | None = None) -> bytes | None:
        text = script or self.last_script
        if not text or not self.voice:
            return None
        return await self.voice.synthesize_long(text)

    async def handle(self, command: str) -> str:
        return await self.generate_episode(command)

    async def heartbeat_check(self):
        return None
