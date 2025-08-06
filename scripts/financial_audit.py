import pandas as pd
from typing import Dict


def load_pnl(path: str) -> pd.DataFrame:
    """
    Charge et nettoie le P&L depuis un fichier CSV ou Excel.
    Attendu : colonnes ['Month','Revenue','COGS','GrossProfit',
    'Opex_RnD','Opex_SalesMarketing','Opex_GA','Opex_Total','EBITDA'].
    """
    # Lecture
    if path.lower().endswith('.csv'):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)
    # Typage et dates
    df['Month'] = pd.to_datetime(df['Month'])
    # Conversion numérique
    for col in ['Revenue','COGS','GrossProfit','Opex_RnD',
                'Opex_SalesMarketing','Opex_GA','Opex_Total','EBITDA']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


def load_cashflow(path: str) -> pd.DataFrame:
    """
    Charge et nettoie le cash-flow depuis un fichier CSV ou Excel.
    Attendu : colonnes ['Month','OperatingCF','CAPEX','Delta_BFR','NetCashFlow'].
    """
    if path.lower().endswith('.csv'):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)
    df['Month'] = pd.to_datetime(df['Month'])
    for col in ['OperatingCF','CAPEX','Delta_BFR','NetCashFlow']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


def compute_kpis(pnl: pd.DataFrame, cf: pd.DataFrame) -> Dict[str, float]:
    """
    Calcule les principaux KPIs à partir des DataFrames PnL et Cashflow.
    Renvoie un dict :
      - total_revenue
      - gross_margin_pct
      - ebitda_margin_pct
      - avg_operating_cf
      - avg_net_cashflow
    """
    total_revenue = pnl['Revenue'].sum()
    total_gross   = pnl['GrossProfit'].sum()
    total_ebitda  = pnl['EBITDA'].sum()
    # Marges
    gross_margin_pct  = total_gross / total_revenue if total_revenue else 0.0
    ebitda_margin_pct = total_ebitda / total_revenue if total_revenue else 0.0
    # Moyennes cash
    avg_operating_cf = cf['OperatingCF'].mean()
    avg_net_cashflow = cf['NetCashFlow'].mean()

    return {
        'total_revenue': total_revenue,
        'gross_margin_pct': gross_margin_pct,
        'ebitda_margin_pct': ebitda_margin_pct,
        'avg_operating_cf': avg_operating_cf,
        'avg_net_cashflow': avg_net_cashflow,
    }