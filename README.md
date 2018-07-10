# `pynotifyd`

Simple freedesktop notification daemon.

## Installation

Arch Linux: Install from [AUR](https://aur.archlinux.org/packages/pynotifyd/)

```shell
pip install pynotifyd
```

## Usage

`pynotifyd` outputs JSON-formatted notification events at the standard output
and debug information at `stderr`. Each notification is on exactly one line to
make it easier to be collected by shell scripts.

## Event types:

### `notify` - Notification has been emitted

```json
{
  "action": "notify",
  "notification": {
    "id": 3,
    "app_name": "KDE Connect",
    "app_icon": "kdeconnect",
    "summary": "WhatsApp",
    "body": "Tudor: Hi!",
    "urgency": 2
  }
}
```

### `delete` - Notification has been dismissed or expired

```json
{
  "action": "delete",
  "id": 1
}
```

## Example usage

Requires [jq](https://stedolan.github.io/jq/).

```bash
#!/bin/sh

pynotifyd 2>/dev/null | while read -r line; do
    action="$(echo "$line" | jq -r .action)"
    case "$action" in
        notify)
            app_name="$(echo "$line" | jq -r .notification.app_name)"
            echo "New notification from $app_name!"
            ;;
    esac
done
```
