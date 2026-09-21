import argparse
import json
import os
import re
import sys
import time
import yaml
from datetime import datetime
from playwright.sync_api import sync_playwright

# Support des touches sous Windows
try:
    import msvcrt
except ImportError:
    msvcrt = None

LOGIN_URL = "https://www.wiki-masters.com/login"
PULLS_URL = "https://www.wiki-masters.com/pulls"
STATS_FILE = "stats.json"
CHECK_INTERVAL = 300  # 5 minutes


# --- STATISTIQUES PERSISTANTES ---

def load_stats():
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r", encoding="utf-8") as f:
                stats = json.load(f)
                stats.setdefault("total_packs", 0)
                stats.setdefault("total_cards", 0)
                stats.setdefault("total_checks", 0)
                stats.setdefault("total_seconds_run", 0)
                stats.setdefault("accounts", {})
                return stats
        except Exception:
            pass
            
    return {
        "total_packs": 0,
        "total_cards": 0,
        "total_checks": 0,
        "total_seconds_run": 0,
        "accounts": {}
    }


def save_stats(stats):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)


def format_duration(seconds):
    hours, remainder = divmod(int(seconds), 3600)
    minutes, secs = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    if days > 0:
        return f"{days}j {hours:02d}h {minutes:02d}m"
    return f"{hours:02d}h {minutes:02d}m {secs:02d}s"


def print_stats_summary(stats, session_start):
    current_session_time = time.time() - session_start
    total_time = stats.get("total_seconds_run", 0) + current_session_time
    uptime = format_duration(total_time)

    print("\n========================================")
    print("         📊 STATISTIQUES DU BOT         ")
    print("========================================")
    print(f"⏱️  Temps total d'utilisation : {uptime}")
    print(f"📦 Total paquets ouverts     : {stats['total_packs']}")
    print(f"🃏 Total cartes obtenues     : {stats['total_cards']} (est. 5/pack)")
    print(f"🔄 Vérifications effectuées : {stats['total_checks']}")
    print("----------------------------------------")
    print("Détails par compte :")
    for acc_name, data in stats.get("accounts", {}).items():
        print(f"  • {acc_name} : {data.get('packs', 0)} paquets ({data.get('cards', 0)} cartes)")
    print("========================================\n")


# --- BOT LOGIC ---

def ensure_logged_in_and_on_pulls(page, email, password):
    page.goto(PULLS_URL, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(1500)

    if page.url.startswith(LOGIN_URL):
        print(f"--> Connexion nécessaire pour : {email}")
        page.wait_for_selector("#email", timeout=10000)
        page.type("#email", email, delay=80)
        page.type("#password", password, delay=80)
        page.wait_for_timeout(500)
        page.press("#password", "Enter")
        page.wait_for_url(f"{PULLS_URL}", timeout=30000)


def get_available_packs(page):
    try:
        page.wait_for_selector("text=/\\d+ \\/ \\d+/", timeout=8000)
        text = page.locator("text=/\\d+ \\/ \\d+/").first.inner_text()
        match = re.search(r"(\d+)\s*/\s*(\d+)", text)
        return int(match.group(1)) if match else 0
    except Exception:
        return 0


def reveal_all_cards(page):
    right_chevron = page.locator("button:has(polyline[points='9 18 15 12 9 6'])").first
    for _ in range(4):
        right_chevron.click(timeout=5000)
        page.wait_for_timeout(600)

    continue_button = page.get_by_role("button", name="Continuer")
    continue_button.click(timeout=5000)
    page.wait_for_load_state("networkidle")


def open_all_packs(page):
    opened = 0
    while True:
        available = get_available_packs(page)
        if available <= 0:
            break

        print(f"--> Paquet disponible ({available} restant(s)) ! Ouverture...")
        page.get_by_role("button", name="Ouvrir un paquet").click()
        page.wait_for_timeout(1000)
        reveal_all_cards(page)
        opened += 1
        page.reload(wait_until="domcontentloaded")
    return opened


def load_accounts(path):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("accounts", [])


def check_keyboard_input(paused, stats, session_start):
    if msvcrt and msvcrt.kbhit():
        key = msvcrt.getch().decode("utf-8", errors="ignore").lower()
        if key == 'p':
            paused = not paused
            status = "EN PAUSE" if paused else "EN MARCHE"
            print(f"\n[CONTROL] Bot mis {status}. (Appuie sur 'P' pour reprendre)\n")
        elif key == 's':
            print_stats_summary(stats, session_start)
        elif key == 'q':
            print("\n[CONTROL] Arrêt du script demandé...")
            sys.exit(0)
    return paused


def countdown_with_controls(seconds, paused, stats, session_start):
    end_time = time.time() + seconds
    while time.time() < end_time or paused:
        paused = check_keyboard_input(paused, stats, session_start)
        time.sleep(0.2)
    return paused


def main():
    accounts = load_accounts("accounts.yaml")
    if not accounts:
        print("ERREUR : Aucun compte dans accounts.yaml !")
        return 1

    stats = load_stats()
    session_start = time.time()

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="./user_data",
            headless=False,
            slow_mo=100,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.pages[0] if context.pages else context.new_page()

        print("\n========================================")
        print("     🤖 WIKIMASTER BOT AUTOMATIQUE      ")
        print("========================================")
        print(" COMMANDES CONSOLE :")
        print("   [P] = Mettre en Pause / Relancer")
        print("   [S] = Afficher les Statistiques")
        print("   [Q] = Quitter proprement")
        print("========================================\n")

        paused = False

        try:
            while True:
                paused = check_keyboard_input(paused, stats, session_start)
                if paused:
                    time.sleep(0.5)
                    continue

                heure = datetime.now().strftime("%H:%M:%S")
                print(f"[{heure}] 🔄 Lancement de la vérification...")
                stats["total_checks"] += 1

                for account in accounts:
                    acc_name = account["name"]
                    if acc_name not in stats["accounts"]:
                        stats["accounts"][acc_name] = {"packs": 0, "cards": 0}

                    try:
                        ensure_logged_in_and_on_pulls(page, account["email"], account["password"])
                        opened = open_all_packs(page)

                        if opened > 0:
                            cards = opened * 5
                            stats["total_packs"] += opened
                            stats["total_cards"] += cards
                            stats["accounts"][acc_name]["packs"] += opened
                            stats["accounts"][acc_name]["cards"] += cards
                            save_stats(stats)
                            print(f"✨ SUCCESS [{acc_name}]: {opened} paquet(s) ouvert(s) (+{cards} cartes) !")
                        else:
                            print(f"ℹ️  INFO [{acc_name}]: Aucun paquet disponible.")
                    except Exception as e:
                        print(f"⚠️  ERREUR [{acc_name}]: {e}")

                # Mise à jour du temps cumulé
                stats["total_seconds_run"] += (time.time() - session_start)
                session_start = time.time()
                save_stats(stats)

                print(f"--> Attente de {CHECK_INTERVAL // 60} min avant la prochaine vérification...")
                paused = countdown_with_controls(CHECK_INTERVAL, paused, stats, session_start)

        except KeyboardInterrupt:
            print("\nArrêt du bot.")
        finally:
            stats["total_seconds_run"] += (time.time() - session_start)
            save_stats(stats)
            context.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
