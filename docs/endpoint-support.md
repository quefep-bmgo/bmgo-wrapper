# Endpoint support

This page records what has actually been exercised against the live API. The
wrapper targets Blockman GO **3.29.3** (`appVersion 5753`). It is not a claim
that every public method works, and it is not a promise that an unlisted method
is supported.

## Status levels

| Status | Meaning |
| --- | --- |
| **Verified** | Called successfully in the read-only audit, or covered by an offline test |
| **Known limitation** | Expected to exist, but currently returns an error, an empty body, or account-specific data |
| **Unverified** | Wrapped from captured traffic but not recently exercised |
| **Write / unsafe** | Changes account, social, inventory, or payment state; not part of the read-only audit |
| **Removed** | Upstream endpoint is dead or the method has no remaining use |

## Verified read-only surface

The audit on 2026-10-26 covered these areas with a test account:

- login and session validation
- own profile
- game catalogue, details, game auth, party auth, open parties, and praise
- game leaderboards for `all`, `week`, and `month`
- current account rank for the same periods
- remote config version and rank-title config
- server notices
- game revision catalogue
- ping server list
- product info
- friends v3
- user details v3
- clan user rank

Run the same checks with:

```bash
python tools/audit_readonly.py
```

The audit is read-only. It logs in, calls a curated list of GET endpoints, and
does not call write, purchase, friend, clan, mailbox, or inventory mutations.
Use a test account.

## Known limitations

| Method | Observed result | Handling |
| --- | --- | --- |
| `RemoteConfigAPI.get_game_resource_config()` | `code 6`, `AUTH FAILED, EMPTY PARAM` | Kept for investigation. The capture had no query string, so it may need an uncaptured parameter rather than being dead. |
| `GameAPI.get_update_tip()` | Empty response body | Kept. The server may intentionally return no tip for this game/account. |
| `ExtendedAPI.security_settings()` | `code 122`, `user security settings not complete` | Account-dependent. A different account may return data. |
| `ExtendedAPI.using_decorations()` | Empty object without a `code` | Not enough evidence to remove. The endpoint may be account- or decoration-state dependent. |
| `ExtendedAPI.clan_rank()` | Empty object without a `code` | Not enough evidence to remove. The endpoint may require parameters. |
| `ExtendedAPI.auth_token(q)` | `code 3` with a stale captured `q` | Kept. It is a token endpoint, not a general-purpose read endpoint, and requires a valid challenge. |
| Game leaderboard `g1046` week/month | Empty list | Data is absent; the all-time list and game details work. This is not an endpoint failure. |

Raw capture replay also produced some non-1 responses that were not wrapper
failures: `/game/api/v3/games/g1046` needed the `language` header, and
`/user/api/v2/users/verify/user/security/settings` returned the same
account-specific `122`. A failed raw replay alone is not enough to delete a
typed method.

## Removed in this change

| Method | Endpoint | Evidence |
| --- | --- | --- |
| `ExtendedAPI.return_activity_info()` | `GET /activity/api/v1/return-activity/info` | Terminal `code 8085`, `activity not exist`; no call sites in the repository |

The method was unconditional: it had no parameters that could make the endpoint
valid. Pin the previous release if you need the call for historical work; the
server currently rejects it.

## Removal policy

A method is removed only when all of these are true:

1. The upstream endpoint returns a terminal response such as `404`, `8085`, or
   an equivalent "does not exist" error.
2. The failure is reproduced through the wrapper, not only through a raw capture
   replay.
3. There are no internal references, tests, examples, or documentation that
   depend on it.
4. There is enough evidence that changing parameters will not revive it.

Methods that are merely untested, account-dependent, empty, rate-limited, or
broken by a stale captured parameter stay in the package and are marked
unverified here. Removing public methods is a breaking change and should be
called out in the release notes.

## What is not covered

- Most write, purchase, social, clan, mailbox, and inventory methods.
- Endpoints that require event state, room state, a purchase flow, or a
  different account configuration.
- The full 3.30.x client. This repository has not verified 3.30.x.

The generated [API reference](api-reference.md) lists the surface area. It does
not mean every row has been validated. Use this page and the audit output as the
support signal.
