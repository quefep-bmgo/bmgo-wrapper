"""Reply to group commands with the built-in RongCloud listener.

Set the usual BMG_* login values plus optional ``BMG_GROUP_IDS``
(comma-separated group IDs). Without a filter the listener receives every
group the account belongs to.

The listener owns the account's RongCloud session. Callbacks run on a worker
thread, so a reply from inside ``on_message`` does not block the socket.
"""

import os
import time

from blockmango import BmgAccount, GroupMessage


def group_ids_from_env() -> list[int] | None:
    raw = os.environ.get("BMG_GROUP_IDS", "").strip()
    if not raw:
        return None
    return [int(value) for value in raw.split(",") if value.strip()]


def main() -> None:
    account = BmgAccount.from_env()
    if not account.login(load_social=False, start_sync=False):
        raise SystemExit("Blockman GO login failed")

    def on_message(message: GroupMessage) -> None:
        if message.is_self or not message.text:
            return
        if message.text.strip().lower() == "!ping":
            account.group.send_text(message.group_id, "pong")

    subscription = account.group.listen(
        on_message,
        group_ids=group_ids_from_env(),
    )
    if not subscription.wait_connected(timeout=15):
        subscription.stop()
        account.close()
        raise SystemExit("RongCloud listener did not connect")

    print(f"Listening for group messages as {account.nick} ({account.uid}).")
    last_error = None
    try:
        while True:
            time.sleep(1)
            error = subscription.last_error
            if error is not None and str(error) != last_error:
                last_error = str(error)
                print(f"Listener error: {error}")
    except KeyboardInterrupt:
        pass
    finally:
        subscription.stop()
        account.close()
        print("Listener stopped.")


if __name__ == "__main__":
    main()
