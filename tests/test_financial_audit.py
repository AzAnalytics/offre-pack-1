import pandas as pd
import numpy as np
import pytest
from scripts.financial_audit import load_pnl, load_cashflow, compute_kpis

# Fixtures for sample data
@pytest.fixture
def sample_pnl(tmp_path):
    data = {
        'Month': pd.date_range('2023-01-01', periods=3, freq='MS'),
        'Revenue': [1000, 2000, 3000],
        'COGS': [400, 800, 1200],
        'GrossProfit': [600, 1200, 1800],
        'Opex_RnD': [100, 100, 100],
        'Opex_SalesMarketing': [50, 50, 50],
        'Opex_GA': [25, 25, 25],
        'Opex_Total': [175, 175, 175],
        'EBITDA': [425, 1025, 1625],
    }
    df = pd.DataFrame(data)
    file = tmp_path / "pnl.csv"
    df.to_csv(file, index=False)
    return file

@pytest.fixture
def sample_cf(tmp_path):
    data = {
        'Month': pd.date_range('2023-01-01', periods=3, freq='MS'),
        'OperatingCF': [400, 800, 1200],
        'CAPEX': [-50, -50, -50],
        'Delta_BFR': [100, -100, 0],
        'NetCashFlow': [450, 650, 1150],
    }
    df = pd.DataFrame(data)
    file = tmp_path / "cash.csv"
    df.to_csv(file, index=False)
    return file


def test_load_pnl_returns_dataframe(sample_pnl):
    df = load_pnl(str(sample_pnl))
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == [
        'Month','Revenue','COGS','GrossProfit',
        'Opex_RnD','Opex_SalesMarketing','Opex_GA','Opex_Total','EBITDA'
    ]
    assert pd.api.types.is_datetime64_any_dtype(df['Month'])


def test_load_cashflow_returns_dataframe(sample_cf):
    df = load_cashflow(str(sample_cf))
    assert isinstance(df, pd.DataFrame)
    assert {'Month', 'OperatingCF', 'CAPEX', 'Delta_BFR', 'NetCashFlow'}.issubset(df.columns)


def test_compute_kpis(sample_pnl, sample_cf):
    pnl_df = load_pnl(str(sample_pnl))
    cf_df = load_cashflow(str(sample_cf))
    kpis = compute_kpis(pnl_df, cf_df)
    # Check keys
    assert 'total_revenue' in kpis
    assert 'gross_margin_pct' in kpis
    assert 'ebitda_margin_pct' in kpis
    # Validate numeric values
    assert pytest.approx(kpis['total_revenue'], rel=1e-3) == 6000
    assert pytest.approx(kpis['gross_margin_pct'], rel=1e-3) == (600+1200+1800)/6000
    assert pytest.approx(kpis['ebitda_margin_pct'], rel=1e-3) == (425+1025+1625)/6000
    assert pytest.approx(kpis['avg_operating_cf'], rel=1e-3) == np.mean([400,800,1200])