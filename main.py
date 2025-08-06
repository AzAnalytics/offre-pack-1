#!/usr/bin/env python3

import warnings
# Masque le warning de dépréciation de pkg_resources dans docxcompose
warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API.*",
    module="docxcompose\\.properties"
)

import argparse
import json
from pathlib import Path
from datetime import datetime
from scripts.financial_audit import load_pnl, load_cashflow, compute_kpis
from scripts.summary_generator import plot_waterfall, plot_timeseries, generate_summary
from scripts.docs_export import export_excel, fill_docx


def main():
    repo_root = Path(__file__).parent

    parser = argparse.ArgumentParser(
        description="Pack 1 Audit: load data, compute KPIs, generate summary and report"
    )
    parser.add_argument(
        "--pnl",
        default=str(repo_root / "data" / "pnl_fictif.csv"),
        help="Path to P&L CSV/Excel"
    )
    parser.add_argument(
        "--cashflow",
        default=str(repo_root / "data" / "cashflow_fictif.csv"),
        help="Path to Cashflow CSV/Excel"
    )
    parser.add_argument(
        "--kpis_out",
        default="kpis.json",
        help="Output path for KPIs JSON"
    )
    parser.add_argument(
        "--summary_out",
        default="summary.md",
        help="Output path for summary Markdown"
    )
    parser.add_argument(
        "--report_out",
        default="rapport.docx",
        help="Output path for report Docx"
    )
    parser.add_argument(
        "--template",
        default=str(repo_root / "templates" / "report_template.docx"),
        help="Docx template path (default: templates/report_template.docx)"
    )

    args = parser.parse_args()

    # Vérification que le template existe
    template_path = Path(args.template)
    if not template_path.is_file():
        parser.error(f"Template not found: {template_path.resolve()}")

    # 1. Audit financier
    pnl_df = load_pnl(args.pnl)
    cf_df = load_cashflow(args.cashflow)
    kpis = compute_kpis(pnl_df, cf_df)

    # Save KPIs JSON
    with open(args.kpis_out, 'w', encoding='utf-8') as f:
        json.dump(kpis, f, ensure_ascii=False, indent=2)

    # 2. Génération des graphiques
    waterfall_path = 'output/waterfall.png'
    plot_waterfall(pnl_df, waterfall_path)
    ts_paths = plot_timeseries(
        pnl_df.merge(cf_df, on='Month'),
        ['EBITDA', 'NetCashFlow'],
        out_dir='output/timeseries'
    )

    # 3. Génération du résumé
    # On récupère le résumé textuel pour l'injecter dans le document
    executive_summary = generate_summary(kpis, [waterfall_path] + ts_paths, args.summary_out)

    # 4. Export Excel
    dataframes = {
        'P&L': pnl_df,
        'Cashflow': cf_df,
    }
    export_excel(kpis, dataframes, 'output/report.xlsx')

    # 5. Préparation du contexte pour le DOCX
    context = {
        'report_title': 'Pack 1 Audit Financier',
        'report_date': datetime.now().strftime('%Y-%m-%d'),
        'executive_summary': executive_summary,
        'kpis': kpis,
        'waterfall_image': waterfall_path,
        'timeseries_images': ts_paths,
        'dataframes': dataframes,
        'conclusion': 'Merci pour votre confiance. Voici nos recommandations.'
    }

    # 6. Génération du document Word
    fill_docx(str(template_path), context, args.report_out)

    print("Audit complet. KPI, résumé et rapport générés.")

if __name__ == '__main__':
    main()
