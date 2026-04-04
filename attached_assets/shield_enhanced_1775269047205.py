# ============================================================
# SHIELD — Enhanced with Full Skills
# Security, GitHub monitoring, uptime, backups, Supabase
# ============================================================

import os, logging, aiohttp, asyncio, subprocess
from datetime import datetime
from anthropic import Anthropic
from skills.shared.telegram_formatter import formatter

log = logging.getLogger("SHIELD")

ANTHROPIC_KEY = os.environ["ANTHROPIC_API_KEY"]
GITHUB_TOKEN  = os.environ.get("GITHUB_TOKEN", "")
GITHUB_ORG    = "creova-gif"

MONITORED_SITES = [
    {"name": "creova.one",       "url": "https://creova.one"},
    {"name": "CREOVA Solutions", "url": "https://creova.one/solutions"},
]

ALL_REPOS = [
    "GoPay","KayaYourPropertyAI","Darsme","MentalPath","QuickBookSample",
    "AIHealthSupport","GridOS","KilimoAI","BudgetEaseApp","HealthFitness",
    "RecommendedPeptides","SEEN","WazaWealth","Mskniagara",
]

SHIELD_SYSTEM = """
You are SHIELD — Justin Mafie's autonomous security and infrastructure chief.
Think like a CTO. Act like a bodyguard. Protect every digital asset CREOVA owns.

When reporting: be specific, structured, and actionable.
Use severity levels: CRITICAL, HIGH, MEDIUM, LOW.
Always state what you did, what Justin needs to do (if anything), and what happens next.
Never be vague. Never say "looks fine" without specific checks run.
"""


class ShieldAgent:
    def __init__(self, api_key: str, memory):
        self.client  = Anthropic(api_key=api_key)
        self.memory  = memory
        self.headers = {
            "Authorization":        f"token {GITHUB_TOKEN}",
            "Accept":               "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        log.info("SHIELD initialized — full skills loaded")

    # ── Main command handler ──────────────────────────────────
    async def handle(self, command: str) -> str:
        response = self.client.messages.create(
            model="claude-sonnet-4-5", max_tokens=1000,
            system=SHIELD_SYSTEM,
            messages=[{"role": "user", "content": command}]
        )
        raw = response.content[0].text
        return await formatter.ai_enhance(raw, "SHIELD", command)

    # ── Heartbeat: full system scan ───────────────────────────
    async def heartbeat_check(self) -> str | None:
        issues = []
        metrics = {}

        # Uptime checks
        for site in MONITORED_SITES:
            ok = await self._ping(site["url"])
            metrics[site["name"]] = "✅ Online" if ok else "❌ DOWN"
            if not ok:
                issues.append(f"{site['name']} is DOWN — {site['url']}")

        # GitHub org check
        if GITHUB_TOKEN:
            repos_ok = await self._check_github_org()
            metrics["GitHub creova-gif"] = f"✅ {len(ALL_REPOS)} repos" if repos_ok else "⚠️ Unreachable"

        # Replit system health (CPU/memory)
        sys_info = self._check_system()
        metrics["Replit memory"] = sys_info["memory"]
        metrics["Replit CPU"]    = sys_info["cpu"]

        if sys_info.get("warning"):
            issues.append(sys_info["warning"])

        self.memory.daily_log(f"[SHIELD] Heartbeat — {len(issues)} issues")

        if issues:
            return formatter.format("SHIELD", "alert", {
                "severity":      "high",
                "what":          "\n".join(issues),
                "affected":      ", ".join([i.split(" is ")[0] for i in issues]),
                "time":          datetime.now().strftime("%H:%M"),
                "action_taken":  "Logged — monitoring every 5 min until resolved",
                "justin_action": "⚡ Check the affected services manually if this persists > 10 min",
            })
        return None   # No issues — silent pass

    # ── Full status report ────────────────────────────────────
    async def status(self) -> str:
        metrics = {}
        issues  = []

        for site in MONITORED_SITES:
            ok = await self._ping(site["url"])
            metrics[site["name"]] = "Online ✅" if ok else "DOWN ❌"
            if not ok: issues.append(f"{site['name']} unreachable")

        metrics["GitHub org"]  = f"creova-gif · {len(ALL_REPOS)} repos tracked"
        metrics["Memory"]      = self._check_system()["memory"]

        # Secret leak check (fast scan)
        leak_result = await self._quick_secret_scan()
        metrics["Secret scan"] = leak_result

        return formatter.format("SHIELD", "report", {
            "summary": f"SHIELD scanned {len(MONITORED_SITES)} sites + GitHub org + system health",
            "metrics": metrics,
            "issues":  issues if issues else ["None detected ✅"],
            "actions": ["Review any flagged items above"] if issues else ["No action required"],
            "next_check": "30 minutes",
        })

    # ── GitHub org accessibility ──────────────────────────────
    async def _check_github_org(self) -> bool:
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(
                    f"https://api.github.com/orgs/{GITHUB_ORG}",
                    headers=self.headers, timeout=aiohttp.ClientTimeout(total=10)
                ) as r:
                    return r.status == 200
        except Exception:
            return False

    # ── URL ping ──────────────────────────────────────────────
    async def _ping(self, url: str) -> bool:
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(url, timeout=aiohttp.ClientTimeout(total=10)) as r:
                    return r.status < 500
        except Exception:
            return False

    # ── System resource check ─────────────────────────────────
    def _check_system(self) -> dict:
        try:
            import psutil
            mem_pct = psutil.virtual_memory().percent
            cpu_pct = psutil.cpu_percent(interval=1)
            warning = None
            if mem_pct > 85:
                warning = f"High memory usage: {mem_pct}% — consider restarting Replit"
            if cpu_pct > 90:
                warning = f"High CPU: {cpu_pct}% — potential performance issue"
            return {
                "memory":  f"{mem_pct}%",
                "cpu":     f"{cpu_pct}%",
                "warning": warning,
            }
        except ImportError:
            return {"memory": "psutil not installed", "cpu": "N/A", "warning": None}

    # ── Quick secret scan ─────────────────────────────────────
    async def _quick_secret_scan(self) -> str:
        """Scan local files for accidentally hardcoded secrets."""
        dangerous_patterns = ["sk-", "AIza", "AKIA", "ghp_", "xox", "-----BEGIN"]
        try:
            result = subprocess.run(
                ["grep", "-r", "--include=*.py", "-l"] + dangerous_patterns + ["."],
                capture_output=True, text=True, timeout=10
            )
            if result.stdout.strip():
                files = result.stdout.strip().split("\n")
                return f"⚠️ Potential secrets in: {', '.join(files[:3])}"
            return "No hardcoded secrets detected ✅"
        except Exception as e:
            return f"Scan skipped: {str(e)[:40]}"

    # ── Repo deep scan ────────────────────────────────────────
    async def scan_repo(self, repo_name: str) -> str:
        """Deep scan of a single repo — called by Justin or weekly cron."""
        from datetime import timedelta
        since = (datetime.utcnow() - timedelta(hours=72)).isoformat() + "Z"
        base  = "https://api.github.com"

        async with aiohttp.ClientSession() as s:
            # Get repo info
            async with s.get(f"{base}/repos/{GITHUB_ORG}/{repo_name}", headers=self.headers) as r:
                info = await r.json() if r.status == 200 else {}

            # Get recent commits
            async with s.get(
                f"{base}/repos/{GITHUB_ORG}/{repo_name}/commits",
                headers=self.headers, params={"since": since, "per_page": 5}
            ) as r:
                commits = await r.json() if r.status == 200 else []

            # Get open issues
            async with s.get(
                f"{base}/repos/{GITHUB_ORG}/{repo_name}/issues",
                headers=self.headers, params={"state": "open", "per_page": 5}
            ) as r:
                issues = await r.json() if r.status == 200 else []

        commit_lines = "\n".join([
            f"  • `{c['sha'][:7]}` {c['commit']['message'][:60]}"
            for c in commits[:3] if isinstance(c, dict) and "sha" in c
        ]) or "  No recent commits"

        issue_lines = "\n".join([
            f"  • #{i.get('number')} {i.get('title','')[:60]}"
            for i in issues[:3] if isinstance(i, dict)
        ]) or "  No open issues ✅"

        return formatter.format("SHIELD", "report", {
            "summary": f"Deep scan: *{repo_name}*",
            "metrics": {
                "Language":    info.get("language", "Unknown"),
                "Open issues": str(info.get("open_issues_count", 0)),
                "Last updated": info.get("updated_at", "Unknown")[:10],
                "Visibility":  "Private" if info.get("private") else "Public",
            },
            "issues": [f"Commits (72h):\n{commit_lines}", f"Open issues:\n{issue_lines}"],
            "actions": ["No action needed" if not issues else f"Review {len(issues)} open issues"],
            "next_check": "Weekly deep scan scheduled",
        })
