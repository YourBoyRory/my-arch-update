#!/usr/bin/env python3

from datetime import datetime
import subprocess
import sys

def notify(notification_config = {}):

    title = notification_config.get("notification_title", "")
    message = notification_config.get("notification_message", "")
    switches = notification_config.get("notification_switches", "")

    return subprocess.run(['/usr/bin/notify-send'] + switches + ['--app-icon=package', '-a', 'Vertex Update', f"{title}", f"{message}"], capture_output=True)

def check_updates():
    try:
        # Refresh repository databases happens in a system dameon

        now = datetime.now().strftime("%I:%M %p")
        result = subprocess.run(
            ["/usr/bin/pacman", "-Qu"],
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
            if out.stdout == b"0\n":
                subprocess.run(["xdg-terminal-exec", "vertex-update"])
        elif result.returncode in [0,1] and not error:
            print("\nSystem is up to date!\n")
            out = notify({
                "notification_title": "System is Up to Date.",
                "notification_message": f"No updates where avalible at {now}.",
                "notification_switches": ['--urgency=low']
            })
        else:
            print(f"\nFailed to check for updates.\n{error}\n")
            sys.exit(result.returncode)


    except subprocess.CalledProcessError as e:
        print(f"\nError checking updates: {e}\n")
        sys.exit(1)
    except FileNotFoundError:
        print("\npacman was not found.\n")
        sys.exit(1)


if __name__ == "__main__":
    check_updates()
