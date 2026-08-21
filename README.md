# bmgo-wrapper

Blockman GO API wrapper with full x-sign authentication.
Compatible with Blockman GO v3.25.1.

## Installation

```bash
pip install -e .
```

Requires Python 3.10+, `requests`, `httpx`, `pycryptodome`.

## Quick Start

```python
from blockmango import BmgClient, Config

config = Config(verify_ssl=False)
accounts = [{"username": "your_email", "password": "your_pass"}]
client = BmgClient(accounts, config)

results = client.login_all()
acc = client.get()
profile = acc.user.get_own_profile()
print(f"Logged in as {profile.nick_name} (UID {profile.user_id})")

client.close_all()
```

## Async

```python
import asyncio
from blockmango import BmgClient

async def main():
    async with BmgClient([{"username": "u", "password": "p"}]) as client:
        await client.async_login_all()
        acc = await client.async_get()
        profile = await acc.user.async_get_own_profile()
        print(profile.nick_name)

asyncio.run(main())
```

## Submodules

- `acc.user` � profile, stats, lookup, nick/pass/email, details
- `acc.friends` � list, search, requests, block, unblock, alias
- `acc.clan` � join, leave, search, members, invite, tasks, mute, bulletin
- `acc.group` � create, invite, kick, admin, mute, transfer, quit
- `acc.decoration` � wardrobe, buy, equip, prices, skins
- `acc.activity` � sign-in, status, tasks, claim
- `acc.ranking` � user rank, global weekly
- `acc.rongcloud` � IM token

## Interactive Demo

```bash
python bmgo-auth-demo.py
```

## License

MIT
