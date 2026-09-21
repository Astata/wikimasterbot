# 🤖 Wikimaster Bot 24/7

[FR] Bot d'automatisation pour ouvrir vos paquets sur wiki-masters.com en continu 24h/24.  
[EN] Automation bot to open your card packs on wiki-masters.com continuously 24/7.

> **Credits:** Forked from the original project by [loiclovitana/wikimasterbot](https://github.com/loiclovitana/wikimasterbot).  
> **Development:** Extended & modified with the help of Gemini.

---

## 🇫🇷 Français

### ✨ Fonctionnalités
- **Mode 24/7** : Vérification automatique des paquets disponibles toutes les 5 minutes.
- **Multi-comptes** : Bascule automatique entre tous vos différents comptes configurés.
- **Statistiques persistantes** : Suivi des paquets ouverts, des cartes obtenues et du temps d'exécution total (sauvegardé en continu dans `stats.json`).
- **Contrôles au clavier** :
  - `P` : Mettre en pause / Relancer le bot.
  - `S` : Afficher le résumé des statistiques dans la console.
  - `Q` : Quitter le bot proprement et enregistrer les données.
- **Raccourci facile** : Lancement rapide en un clic via le fichier `run.bat`.

### 🚀 Configuration & Lancement

#### 1. Installation des dépendances
```bash
uv sync
uv run playwright install chromium
```

#### 2. Configuration des comptes
Dupliquez le fichier `accounts-template.yaml` en `accounts.yaml` et ajoutez vos identifiants :
```yaml
accounts:
  - name: MonCompte
    email: votre_email@example.com
    password: votre_mot_de_passe
```

> **Remarque :** Le fichier `accounts.yaml` est ignoré par Git (`.gitignore`) pour garantir que vos mots de passe ne soient jamais publiés sur GitHub.

#### 3. Démarrage du bot
Double-cliquez simplement sur **`run.bat`** (ou lancez via la console) :
```cmd
py main.py
```

---

## 🇬🇧 English

### ✨ Features
- **24/7 Automation**: Automatically checks for available packs every 5 minutes.
- **Multi-Account Support**: Seamlessly cycles through all configured accounts.
- **Persistent Statistics**: Tracks opened packs, estimated cards collected, total checks, and total uptime (saved continuously in `stats.json`).
- **Keyboard Controls**:
  - `P`: Pause / Resume the bot execution.
  - `S`: Display current statistics directly in the console.
  - `Q`: Safely terminate the bot and save all progress.
- **One-Click Launch**: Easily run the bot using `run.bat` without manual command-line entry.

### 🚀 Setup & Usage

#### 1. Install Dependencies
```bash
uv sync
uv run playwright install chromium
```

#### 2. Configure Credentials
Copy `accounts-template.yaml` to `accounts.yaml` and enter your login details:
```yaml
accounts:
  - name: Account1
    email: user1@example.com
    password: changeme
```

> **Note:** The `accounts.yaml` file is included in `.gitignore` to prevent private credentials from being committed to GitHub.

#### 3. Run the Bot
Simply double-click on **`run.bat`** (or execute from terminal):
```cmd
py main.py
```
