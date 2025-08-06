#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Dict

def plot_waterfall(pnl: pd.DataFrame, out_path: str) -> None:
    """
    Génère un graphique waterfall pour l'EBITDA :
    - Revenue
    - COGS
    - Opex_Total
    - EBITDA
    Sauvegarde en PNG.
    Attendu : pnl contient colonnes ['Revenue','COGS','Opex_Total','EBITDA'].
    """
    steps = ['Revenue', 'COGS', 'Opex_Total', 'EBITDA']
    values = [
        pnl['Revenue'].sum(),
        -pnl['COGS'].sum(),
        -pnl['Opex_Total'].sum(),
        pnl['EBITDA'].sum()
    ]

    fig, ax = plt.subplots()

    # Spécifier hue pour la coloration + supprimer la légende
    sns.barplot(
        x=steps,
        y=values,
        hue=steps,
        palette='viridis',
        ax=ax,
        legend=False
    )
    # Au cas où seaborn ne gère pas legend=False
    if ax.get_legend() is not None:
        ax.get_legend().remove()

    ax.set_title('Waterfall EBITDA')
    ax.set_ylabel('Montant (€)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path)
    plt.close(fig)

def plot_timeseries(df: pd.DataFrame, metrics: List[str], out_dir: str) -> List[str]:
    """
    Trace des séries temporelles pour chaque metric dans df (colonne 'Month').
    Sauvegarde chaque figure dans out_dir et retourne les chemins.
    """
    os.makedirs(out_dir, exist_ok=True)
    paths: List[str] = []
    for metric in metrics:
        fig, ax = plt.subplots()
        ax.plot(df['Month'], df[metric])
        ax.set_title(f'{metric} over time')
        ax.set_xlabel('Month')
        ax.set_ylabel(metric)
        plt.xticks(rotation=45)
        plt.tight_layout()
        file_path = os.path.join(out_dir, f'{metric}.png')
        fig.savefig(file_path)
        plt.close(fig)
        paths.append(file_path)
    return paths


def generate_summary(kpis: Dict[str, float], image_paths: List[str], out_md: str) -> None:
    """
    Génère un résumé exécutif au format Markdown.
    - Liste des KPIs en bullet points
    - Intègre les images (charts) en markdown
    """
    lines = ["# Executive Summary", ""]
    for k, v in kpis.items():
        lines.append(f"- **{k.replace('_', ' ').title()}**: {v:,.2f}")
    lines.append("")
    for img in image_paths:
        lines.append(f"![{os.path.basename(img)}]({img})")
        lines.append("")
    # Assurer création du dossier seulement si nécessaire
    parent_dir = os.path.dirname(out_md)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
    with open(out_md, 'w', encoding='utf-8') as f:
        f.write("".join(lines))