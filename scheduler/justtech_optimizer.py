# ============================================================
# JUSTTECH OPTIMIZER — autonomous improvement loop
# Weekly: run retrospective (rewrite lessons) + propose next topics,
# then ping Justin on Telegram. This is the "always getting better" loop.
# ============================================================

import os
import asyncio
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/Toronto")
log = logging.getLogger("JT-OPTIMIZER")


class JustTechOptimizer:
    def __init__(self, app, justtech):
        self.app = app
        self.jt = justtech
        self.chat_id = os.environ.get("JUSTIN_CHAT_ID")
        self._last_run_date = None

    async def run(self):
        """Every Monday 07:00 ET: retrospective + topic queue → Telegram."""
        while True:
            try:
                now = datetime.now(ET)
                today = now.date()
                if now.weekday() == 0 and now.hour == 7 and self._last_run_date != today:
                    self._last_run_date = today
                    log.info("[JT-OPTIMIZER] weekly cycle running")
                    retro = await self.jt.retrospective()
                    topics = await self.jt.suggest_topics(3)
                    if self.app and self.chat_id:
                        for msg in (retro, topics):
                            for chunk in [msg[i:i+4000] for i in range(0, len(msg), 4000)]:
                                await self.app.bot.send_message(chat_id=self.chat_id, text=chunk)
            except Exception as e:
                log.error(f"[JT-OPTIMIZER] error: {e}")
            await asyncio.sleep(300)
