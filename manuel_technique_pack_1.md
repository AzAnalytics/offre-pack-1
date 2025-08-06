# Manuel Technique — Outil Python Pack 1

*Version 1.0 — 6 août 2025*

Ce manuel décrit l’architecture, l’installation, l’utilisation et le développement de l’outil Python d’audit Pack 1.

---

## Table des matières

1. [Architecture du projet](#architecture-du-projet)
2. [Installation](#installation)
3. [Utilisation](#utilisation)
4. [Modules principaux](#modules-principaux)
   - [scripts/financial\_audit.py](#scriptsfinancial_auditpy)
   - [scripts/summary\_generator.py](#scriptssummary_generatorpy)
   - [scripts/docs\_export.py](#scriptsdocs_exportpy)
   - [main.py](#mainpy)
5. [Tests unitaires](#tests-unitaires)
6. [Personnalisation & extensions](#personnalisation--extensions)
7. [Dépannage](#dépannage)

---

## 1. Architecture du projet

```
pack1-audit-python/
├── data/                    # Sources de données
│   ├── pnl_fictif.csv       # P&L fictif (2023‑2024)
│   ├── cashflow_fictif.csv  # Cashflow fictif (2023‑2024)
│   ├── OnlineRetail.xlsx    # Ventes e‑commerce (Kaggle)
│   ├── GoogleAds_*.csv      # Dépenses pub & ROAS
│   └── deutsche_bank_*.csv  # Benchmark sectoriel
├── notebooks/               # Exploration interactive
│   └── audit_exploration.ipynb
├── scripts/                 # Modules audit et export
│   ├── __init__.py          # Package init
│   ├── financial_audit.py   # Chargement, nettoyage, KPIs
│   ├── summary_generator.py # Graphiques & résumé
│   └── docs_export.py       # Export Excel & Docx
├── tests/                   # Tests Pytest
│   ├── test_financial_audit.py
│   └── test_summary_generator.py
├── main.py                  # CLI orchestration
├── report_template.docx     # Modèle Word pour export
├── requirements.txt         # Dépendances
├── pyproject.toml           # Config projet (Poetry/Flit)
└── README.md                # Présentation du projet
```

---

## 2. Installation

1. **Cloner** le dépôt & aller dans le répertoire :
   ```bash
   git clone <url> && cd pack1-audit-python
   ```
2. **Créer un environnement virtuel** :
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # Windows: .venv\Scripts\activate
   ```
3. **Installer** les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

---

## 3. Utilisation

### CLI `main.py`

Orchestration complète du workflow :

```bash
# Audit financier → kpis.json
python main.py \
  --pnl data/pnl_fictif.csv \
  --cashflow data/cashflow_fictif.csv \
  --kpis_out output/kpis.json

# Résumé exécutif + graphiques → summary.md
python main.py --summary_out output/summary.md

# Rapport Word → rapport.docx
python main.py --report_out output/rapport.docx \
  --template report_template.docx
```

> **Astuce** : sans arguments, `main.py` utilise par défaut `data/pnl_fictif.csv` et `data/cashflow_fictif.csv` et génère les fichiers à la racine.

---

## 4. Modules principaux

### `scripts/financial_audit.py`

- `` : charge P&L (CSV/Excel), typage, dates.
- `` : charge cash-flow & BFR.
- `` : calcule
  - `total_revenue`, `gross_margin_pct`, `ebitda_margin_pct`,
  - `avg_operating_cf`, `avg_net_cashflow`.

### `scripts/summary_generator.py`

- `` : génère un chart waterfall (.png).
- `` : plots serie temporelles.
- `` : résumé en Markdown.

### `scripts/docs_export.py`

- `` : crée un fichier Excel multi-onglets.
- `` : rempli un `.docx` via DocxTemplate.
- `` *(optionnel)* : copie & remplit un Google Docs.

### `main.py`

Orchestre :

1. Chargement des datas.
2. Calcul des KPIs & sauvegarde JSON.
3. Génération des graphiques.
4. Résumé Markdown.
5. Export Excel & Word.

---

## 5. Tests unitaires

Lancer :

```bash
pytest -q
```

Couverture :

- `test_financial_audit.py` : load & compute
- `test_summary_generator.py` : plot & summary

---

## 6. Personnalisation & extensions

- **Données réelles** : remplacer `data/*.csv` par vos exports.
- **CLI** : ajouter flags `--output-dir`, `--verbose`.
- **Notebook** : prototyper dans `notebooks/audit_exploration.ipynb`.
- **Connecteurs** : SQL, BigQuery, API REST.

---

## 7. Dépannage

- **Module non trouvé** : assurez-vous d’avoir `scripts/__init__.py` et d’exécuter depuis la racine.
- **Template manquant** : placez `report_template.docx` ou modifiez `--template`.
- **Permission refusée** : vérifiez les droits d’écriture sur le dossier `output/`.

---

*Fin du manuel technique Pack 1*

