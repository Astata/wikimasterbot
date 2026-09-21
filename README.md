# 🤖 Wikimaster Bot 24/7 

[FR] Bot d'automatisation pour ouvrir vos paquets sur wiki-masters.com en continu 24h/24.  
[EN] Automation bot to open your packs on wiki-masters.com continuously 24/7.

> **Credits:** Forked from the original project by [loiclovitana/wikimasterbot](https://github.com/loiclovitana/wikimasterbot).
Gemini AI
---

## 🇫🇷 Français

### ✨ Fonctionnalités
- **Mode 24/7** : Vérification automatique des paquets toutes les 5 minutes.
- **Multi-comptes** : Passage automatique d'un compte à un autre.
- **Statistiques persistantes** : Suivi des paquets ouverts, des cartes et du temps total (sauvegardé dans `stats.json`).
- **Contrôles au clavier** :
  - `P` : Mettre en pause / Relancer.
  - `S` : Afficher les statistiques dans la console.
  - `Q` : Quitter le bot proprement.
- **Raccourci facile** : Lancement direct via le fichier `run.bat`.

### 🚀 Configuration & Lancement
1. Renommez le fichier modèle `accounts-template.yaml` en `accounts.yaml`.
2. Ouvrez `accounts.yaml` et remplissez vos identifiants :
   ```yaml
   accounts:
     - name: MonCompte
       email: votre_email@example.com
       password: votre_mot_de_passe
   
 # 🤖 Wikimaster Bot 24/7 

 ## 🇬🇧 English

Automation bot to open your card packs on wiki-masters.com continuously 24/7.

> **Credits:** Forked from the original project by [loiclovitana/wikimasterbot](https://github.com/loiclovitana/wikimasterbot).

---

## ✨ Features
- **24/7 Automation**: Automatically checks for available packs every 5 minutes.
- **Multi-Account Support**: Seamlessly cycles through all configured accounts.
- **Persistent Statistics**: Tracks opened packs, estimated cards collected, total checks, and total uptime (saved continuously in `stats.json`).
- **Keyboard Controls**:
  - `P`: Pause / Resume the bot execution.
  - `S`: Display current statistics directly in the console.
  - `Q`: Safely terminate the bot and save all progress.
- **One-Click Launch**: Easily run the bot using `run.bat` without manual command-line entry.

Created using AI
---

## 🚀 Setup & Usage

### 1. Install Dependencies
```bash
uv sync
uv run playwright install chromium
