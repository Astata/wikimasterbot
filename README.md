# wikimasterbot

Automates opening all available packs on wiki-masters.com, for one or several accounts.

## Setup

```bash
uv sync
uv run playwright install chromium
```

Copy `accounts-template.yaml` to `accounts.yaml` and fill in your account credentials:

```yaml
accounts:
  - name: account1
    email: user1@example.com
    password: changeme
```

## Usage

```bash
uv run main.py --accounts accounts.yaml
```

For each account, the bot logs in, opens every available pack, and prints a success or failure line.
