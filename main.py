import argparse
import re
import sys

import yaml
from playwright.sync_api import sync_playwright

LOGIN_URL = "https://www.wiki-masters.com/login"
PULLS_URL = "https://www.wiki-masters.com/pulls"


def login(page, email, password):
    page.goto(LOGIN_URL, wait_until="networkidle", timeout=30000)
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("button[type=submit]")
    page.wait_for_url(f"{PULLS_URL}", timeout=30000)


def get_available_packs(page):
    text = page.locator("text=/\\d+ \\/ \\d+/").first.inner_text()
    match = re.search(r"(\d+)\s*/\s*(\d+)", text)
    return int(match.group(1))


def reveal_all_cards(page):
    right_chevron = page.locator("button:has(polyline[points='9 18 15 12 9 6'])").first
    for _ in range(4):
        right_chevron.click(timeout=5000)
        page.wait_for_timeout(800)

    continue_button = page.get_by_role("button", name="Continuer")
    continue_button.click(timeout=5000)
    page.wait_for_load_state("networkidle")


def open_all_packs(page):
    opened = 0
    while True:
        page.wait_for_load_state("networkidle")
        available = get_available_packs(page)
        if available <= 0:
            break

        page.get_by_role("button", name="Ouvrir un paquet").click()
        page.wait_for_timeout(1000)
        reveal_all_cards(page)
        opened += 1
    return opened


def load_accounts(path):
    with open(path) as f:
        data = yaml.safe_load(f)
    return data["accounts"]


def run_account(browser, account):
    page = browser.new_page()
    try:
        login(page, account["email"], account["password"])
        opened = open_all_packs(page)
        print(f"SUCCESS [{account['name']}]: opened {opened} pack(s)")
        return True
    except Exception as e:
        print(f"FAILURE [{account['name']}]: {e}")
        return False
    finally:
        page.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--accounts",
        default="accounts.yaml",
        help="Path to the accounts YAML file (default: accounts.yaml)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    accounts = load_accounts(args.accounts)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-dev-shm-usage", "--disable-gpu"],
        )
        results = [run_account(browser, account) for account in accounts]
        browser.close()

    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
