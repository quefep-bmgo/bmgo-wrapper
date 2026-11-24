# Group chats, friend directories, and multi-account lookup

The wrapper separates two concerns:

1. **Blockman GO HTTP API** — group metadata, membership, and friend lists.
2. **RongCloud** — the actual group-chat message transport.

The HTTP API does not expose a group-message publish endpoint. The group
helpers handle discovery, membership, caching, and validation, while the
built-in pure-Python RongCloud transport publishes group text over WebSocket.
A custom transport can still be installed when an application already has its
own RongCloud client.

## Account social state

`login()` and `async_login()` now hydrate the account directory and start
sync. The snapshot contains every group the account belongs to and up to 500
friends. The background poller checks once every 60 seconds by default.

```python
from blockmango import BmgAccount

account = BmgAccount.from_env()
if not account.initialize():       # login + snapshot + polling
    raise SystemExit("login failed")

print([g.group_name for g in account.social.groups])
print([f.nick_name for f in account.social.friends])

def on_change(update):
    # Fires only when at least one entry was added or removed.
    print("groups +", update.group_ids_added)
    print("groups -", update.group_ids_removed)
    print("friends +", update.friend_ids_added)
    print("friends -", update.friend_ids_removed)

subscription = account.social.on_change(on_change)
...
subscription.unsubscribe()
account.close()                    # stops the polling thread
```

The state is also directly queryable without another request:

```python
group = account.social.get_group(123456)
friend = account.social.get_friend(654321)
groups = account.social.find_groups("clan")
friends = account.social.find_friends("alex")
```

For a one-shot script, wait for the next real change:

```python
update = account.social.wait_for_update(timeout=30)
if update is not None:
    print(update.groups_added, update.groups_removed)
```

Polling is opt-out and configurable:

```python
account.login(load_social=True, start_sync=True, sync_interval=30)
account.login(load_social=False, start_sync=False)  # no automatic requests

account.social.refresh()          # fetch and diff now
account.social.stop()             # stop the polling thread
```

If the directory request fails, login still succeeds. The error is available as
`account.social.last_error`, and the polling loop retries. After
`restore_session()`, call `account.initialize_social()` once:

```python
if account.restore_session(saved_session):
    account.initialize_social(start=True, interval=60)
```

Async accounts use the async directory calls:

```python
account = BmgAccount.from_env()
if not await account.async_initialize():
    raise SystemExit("login failed")

await account.social.async_refresh()
await account.social.async_start(interval=60)
...
await account.social.async_stop()
await account.async_close()
```

### Multiple accounts

`BmgClient.login_all()` hydrates every logged-in account and starts one polling
thread per account. The same `sync_interval` applies to all of them.

```python
client = BmgClient([
    {"username": "account-a", "password": "..."},
    {"username": "account-b", "password": "..."},
])
client.login_all(sync_interval=60)

for account in client.accounts:
    print(account.username, len(account.social.groups), len(account.social.friends))

client.start_social_sync(interval=60)   # idempotent
client.stop_social_sync()
client.close_all()
```

Use `client.start_social_sync()` / `stop_social_sync()` when you want to
suspend polling without closing the accounts. The async equivalents are
`async_start_social_sync()` and `async_stop_social_sync()`.

## Find groups

```python
from blockmango import BmgAccount

account = BmgAccount.from_env()
if not account.initialize():
    raise SystemExit("login failed")

groups = account.group.search_groups("clan")
for group in groups:
    print(group.group_id, group.group_name, group.member_count)

exact = account.group.find_group(name="My Clan")
by_id = account.group.find_group(group_id=123456)
members = account.group.get_members(123456)
```

`list_all_groups()` and `search_groups()` fetch one cached snapshot. The
snapshot is reused for 5 minutes and can be refreshed explicitly:

```python
account.group.refresh_groups()
account.group.invalidate_cache()
```

## Send a group text message

Sending is built in. `BmgAccount` installs a pure-Python
`RongCloudTransport`, so a normal login is all you need:

```python
from blockmango import BmgAccount

account = BmgAccount.from_env()
if not account.initialize():
    raise SystemExit("login failed")

group = account.social.groups[0]
result = account.group.send_text(group.group_id, "Hello group!")
print(result.message_uid, result.timestamp)
```

There is no Android app, emulator, ADB, or Frida requirement. The transport:

1. obtains a RongCloud token from the logged-in Blockman account,
2. resolves the RongCloud WebSocket host from the token's navi record,
3. connects with the account's `deviceId`, `clientId`, and `platform=android`, and
4. publishes a `pgMsgP` RongCloud message and waits for the `PubAck`.

`send_text()` validates the group ID, rejects empty text, and enforces the
10 KiB limit. `ext_content` is sent as RongCloud's `extra` field. Failures raise
`RongCloudTransportError` with the group ID and, where available, a status code.

You normally do not need to configure the transport. For a standalone account
or a custom token source, construct one explicitly:

```python
from blockmango import BmgAccount, RongCloudTransport

account = BmgAccount.from_env()
account.login(load_social=False, start_sync=False)

transport = RongCloudTransport(
    account,
    token="optional-explicit-token",
    device_id="optional-explicit-device-id",
)
account.group.set_transport(transport)
account.group.send_text(123456, "Hello group!")
```

### Custom transports

If you already have a RongCloud SDK or sidecar, use `FunctionGroupTransport`:

```python
from blockmango import FunctionGroupTransport, GroupMessageResult

def send_with_my_client(*, group_id, text, ext_content, timeout):
    return GroupMessageResult(group_id=group_id, message_uid="...")

account.group.set_transport(FunctionGroupTransport(send_with_my_client))
```

Any object with `send_text(...)` and `async_send_text(...)` can be installed
with `account.group.set_transport(...)`. Installing `None` disables sending and
restores the `GroupMessagingUnavailable` error.

## Incoming group messages

The built-in RongCloud transport can keep a persistent socket open and dispatch
incoming group messages:

```python
def on_message(message):
    print(message.group_id, message.sender_id)
    print(message.object_name, message.text, message.message_uid)

subscription = account.group.listen(
    on_message,
    group_ids=[123456],   # optional filter
)

account.group.send_text(123456, "hello while listening")
subscription.stop()
```

`message` is a `GroupMessage` with `group_id`, `sender_id`, `object_name`,
`text`, `content`, `message_uid`, `sent_at`, `is_self`, and `raw`. Text
messages fill `text`; image messages use `object_name="RC:ImgMsg"` and expose
their URL through `image_url`. Other RongCloud object names keep their decoded
JSON in `content`.

While the listener is active, `send_text()` uses the listener's connection
instead of opening a second RongCloud session. That matters because RongCloud
allows one active session per token.

The async form accepts an async callback:

```python
async def on_message(message):
    print(message.text)

subscription = await account.group.async_listen(on_message)
```

The listener reconnects on disconnect, sends heartbeats, and polls the
RongCloud sync cursor every second by default. `poll_interval` controls that
cadence. `backlog=True` requests older messages during the initial sync;
the default starts from the current time. `include_self=False` suppresses
messages sent by the account itself.

Stop the listener with `subscription.stop()`, `account.group.stop_listening()`,
or `account.close()`. A listener owns the account's RongCloud session, so use
one listener per account. The account's social-state polling is separate and
continues independently.

## Friend directories for up to 500 friends
## Friend directories for up to 500 friends

`account.friends` now keeps a deduplicated friend snapshot:

```python
friends = account.friends.list_all_friends()          # up to 500
alice = account.friends.find_friend("alice")
matches = account.friends.find_friends("ali")
by_id = account.friends.get_friend(123456789)
```

The helper fetches pages of 50, deduplicates by user ID, and caches the result
for 5 minutes. A second name or ID lookup does not make another request. Use
`refresh_friends()` to force an update, or `invalidate_cache()` after an
out-of-band friend change. Mutating helpers invalidate the snapshot
automatically.

## Multiple accounts without a request per friend

```python
from blockmango import BmgClient

client = BmgClient([
    {"username": "account-a", "password": "..."},
    {"username": "account-b", "password": "..."},
])
client.login_all()

matches = client.find_friends("alex")
for match in matches:
    print(match.username, match.friend.user_id, match.friend.nick_name)

client.send_group_text("account-a", 123456, "hello from account A")
```

Each account has its own cached snapshot. Cross-account searches use a bounded
thread pool (4 workers by default), not one request per friend and not one
unbounded thread per account. Accounts that are not logged in are skipped.
Use `client.get_account("account-a")` when you need the underlying
`BmgAccount`.

## Scope

The built-in transport covers group text publishing and incoming group-message
listening, including RongCloud authentication, navi lookup, RMTP framing,
`PubAck`/`PublishMessage` handling, heartbeats, and reconnect. Media messages,
message history sync, receipts, and typing indicators are separate RongCloud
features and are not part of this transport yet. The HTTP discovery layer,
account social state, friend/group caches, and multi-account helpers are
complete and usable independently.
