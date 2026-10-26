"""Audit a curated set of read-only wrapper endpoints.

The script logs in with the environment credentials and calls only read-only
methods. It does not call POST/PUT/DELETE endpoints that change account state.

Run from the repository root:

    python tools/audit_readonly.py
    python tools/audit_readonly.py --format json
    python tools/audit_readonly.py --game g1046

Expected values:

    ok         method should return a successful envelope or a non-empty result
    empty-ok   method may return an empty list legitimately
    known      known limitation; a change from the observed result is reported

The exit code is 1 only for an unexpected failure. Known limitations do not
fail the audit.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from blockmango import BmgAccount, __version__  # noqa: E402
from blockmango.constants import APP_VERSION, APP_VERSION_NAME  # noqa: E402

PRODUCT_SAMPLE = "and.game.inner.novice.icebreaker.10006"


@dataclass(frozen=True)
class Check:
    name: str
    expected: str
    call: Callable[[BmgAccount, str], Any]


@dataclass
class Result:
    check: str
    expected: str
    status: str
    code: int | str | None
    detail: str


def _describe(value: Any) -> tuple[str, int | str | None, int | None, str]:
    if isinstance(value, dict):
        code = value.get("code")
        message = value.get("message")
        return "envelope", code, None, str(message or "")[:200]
    if isinstance(value, list):
        return "list", "list", len(value), f"{len(value)} rows"
    if isinstance(value, bool):
        return "bool", "bool", None, str(value)
    if value is None:
        return "none", None, None, "no value"
    return "object", type(value).__name__, None, type(value).__name__


def _classify(expected: str, kind: str, code: int | str | None,
              rows: int | None, detail: str) -> str:
    if expected == "ok":
        if kind == "envelope" and code == 1:
            return "pass"
        if kind == "list" and rows:
            return "pass"
        if kind == "bool" and detail == "True":
            return "pass"
        if kind == "object":
            return "pass"
        return "fail"
    if expected == "empty-ok":
        if kind == "envelope" and code == 1:
            return "pass"
        if kind == "list":
            return "pass"
        return "fail"
    if expected == "known":
        if kind == "envelope" and code == 1:
            return "changed"
        return "known"
    return "fail"


def _run_check(account: BmgAccount, game_id: str, check: Check) -> Result:
    try:
        value = check.call(account, game_id)
    except Exception as exc:
        return Result(check.name, check.expected, "fail", "exception", str(exc)[:200])
    kind, code, rows, detail = _describe(value)
    return Result(
        check.name,
        check.expected,
        _classify(check.expected, kind, code, rows, detail),
        code,
        detail,
    )


def _checks() -> list[Check]:
    return [
        Check("profile", "ok", lambda a, g: a.get_own_profile()),
        Check("session_valid", "ok", lambda a, g: a.session_valid()),
        Check("game_list", "ok", lambda a, g: a.game.get_game_list(page=0, size=5)),
        Check("game_details", "ok", lambda a, g: a.game.get_game_details(g)),
        Check("game_auth", "ok", lambda a, g: a.game.game_auth(g)),
        Check("party_auth", "ok", lambda a, g: a.game.party_auth_v3(g)),
        Check("open_parties", "ok", lambda a, g: a.game.get_all_open_parties()),
        Check("praise", "ok", lambda a, g: a.game.get_praise_online_info([g])),
        Check("my_rank_all", "ok", lambda a, g: a.game.get_game_my_rank(g, period="all")),
        Check("my_rank_week", "ok", lambda a, g: a.game.get_game_my_rank(g, period="week")),
        Check("my_rank_month", "ok", lambda a, g: a.game.get_game_my_rank(g, period="month")),
        Check("leaderboard_all", "ok", lambda a, g: a.ranking.get_game_leaderboard_entries(
            g, period="all", page=0, size=5
        )),
        Check("leaderboard_week", "ok", lambda a, g: a.ranking.get_game_leaderboard_entries(
            g, period="week", page=0, size=5
        )),
        Check("leaderboard_month", "ok", lambda a, g: a.ranking.get_game_leaderboard_entries(
            g, period="month", page=0, size=5
        )),
        Check("remote_config_version", "ok", lambda a, g: a.remote_config.check_version()),
        Check("rank_title_config", "ok", lambda a, g: a.remote_config.get_game_rank_title_config()),
        Check("game_resource_config", "known", lambda a, g: a.remote_config.get_game_resource_config()),
        Check("server_notice", "ok", lambda a, g: a.notice.get_server_notice_config()),
        Check("game_revision_combine", "ok", lambda a, g: a.extended.game_revision_combine(page=0, size=5)),
        Check("ping_server_list", "ok", lambda a, g: a.extended.ping_server_list()),
        Check("product_info", "ok", lambda a, g: a.extended.product_info_batch([PRODUCT_SAMPLE])),
        Check("friends_v3", "ok", lambda a, g: a.extended.friends_v3(page=0, size=50)),
        Check("user_details_v3", "ok", lambda a, g: a.extended.user_details_v3()),
        Check("clan_user_rank", "ok", lambda a, g: a.extended.clan_user_rank()),
        Check("security_settings", "known", lambda a, g: a.extended.security_settings()),
        Check("update_tip", "known", lambda a, g: a.game.get_update_tip(g)),
    ]


def _table(results: list[Result]) -> str:
    lines = [
        "| Check | Expected | Status | Code | Detail |",
        "| --- | --- | --- | --- | --- |",
    ]
    for result in results:
        detail = result.detail.replace("|", "\\|")
        lines.append(
            f"| `{result.check}` | {result.expected} | {result.status} | "
            f"`{result.code}` | {detail} |"
        )
    counts: dict[str, int] = {}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1
    lines.append("")
    lines.append(
        "Summary: " + ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit a curated set of read-only Blockman GO endpoints.",
        epilog="The audit never calls write, purchase, social, or inventory endpoints.",
    )
    parser.add_argument("--game", default="g1055", help="game ID used by the read checks")
    parser.add_argument("--format", choices=("table", "json"), default="table")
    args = parser.parse_args()
    if not re.fullmatch(r"g\d+", args.game):
        parser.error("--game must look like g1055")

    account = BmgAccount.from_env()
    try:
        if not account.login():
            print("login failed; check the credentials and device values", file=sys.stderr)
            return 2
        results = [_run_check(account, args.game, check) for check in _checks()]
        payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "wrapper_version": __version__,
            "target_app_version": APP_VERSION_NAME,
            "target_app_build": APP_VERSION,
            "game_id": args.game,
            "uid": account.uid,
            "region": account.region,
            "results": [asdict(result) for result in results],
        }
    finally:
        account.close()

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"wrapper {__version__}; target {APP_VERSION_NAME} ({APP_VERSION}); game {args.game}")
        print(_table(results))

    return 1 if any(result.status == "fail" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
