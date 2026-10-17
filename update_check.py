#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
import subprocess
import sys

def notify(notification_config = {}):

    notification_id = notification_config.get("notification_id", "0")
    title = notification_config.get("notification_title", "")
    message = notification_config.get("notification_message", "")
    switches = notification_config.get("notification_switches", "")

    return subprocess.run(['/usr/bin/notify-send'] + switches + ['-r', notification_id, '--print-id',  '--app-icon=package', '-a', 'Vertex Update', f"{title}", f"{message}"], capture_output=True)

def check_updates():
    try:
        temp_file = Path.home() / ".cache" / "update_check_notification_id"
        notification_id = "0"
        if temp_file.exists():
            notification_id = temp_file.read_text()
        if not notification_id.isdigit():
            notification_id = "0"

        now = datetime.now().strftime("%I:%M %p")
        result = subprocess.run(
            ["/usr/bin/checkupdates"],
            capture_output=True,
            text=True,
            check=False,
        )
        updates = result.stdout.strip()
        error = result.stderr.strip()
        if result.returncode == 0 and updates:
            print("\nUpdates available!\n")
            out = notify({
                "notification_title": "Updates available!",
                "notification_message": f"There are updates to install. Install them now?",
                "notification_switches": ['--icon=security-high', '--urgency=critical', '-A', 'Install Updates']
            })
            if out.stdout.splitlines()[-1] == b'0':
                subprocess.run(["xdg-terminal-exec", "vertex-update"])
        elif result.returncode in [0,1] and not error:
            print("\nSystem is up to date!\n")
            out = notify({
                "notification_id": notification_id,
                "notification_title": "System is Up to Date.",
                "notification_message": f"No updates where avalible at {now}.",
                "notification_switches": ['--urgency=low']
            })
            notification_id = out.stdout.splitlines()[0].decode("utf-8")
        else:
            print(f"\nFailed to check for updates.\n{error}\n")
            sys.exit(result.returncode)

        if notification_id.isdigit():
            with open(temp_file, "w") as f:
                f.write(notification_id)

    except subprocess.CalledProcessError as e:
        print(f"\nError checking updates: {e}\n")
        sys.exit(1)
    except FileNotFoundError:
        print("\npacman was not found.\n")
        sys.exit(1)


if __name__ == "__main__":
    check_updates()
