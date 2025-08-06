import os
import pandas as pd
import pytest
from scripts.summary_generator import plot_waterfall, plot_timeseries, generate_summary

tmp_dir = None

@pytest.fixture(autouse=True)
def create_tmp_dir(tmp_path):
    global tmp_dir
    tmp_dir = tmp_path
    return tmp_path

@pytest.fixture
def sample_pnl(tmp_path):
    # Create minimal PnL DataFrame
    dates = pd.date_range('2023-01-01', periods=3, freq='MS')
    df = pd.DataFrame({
        'Month': dates,
        'Revenue': [1000, 2000, 1500],
        'COGS': [400, 800, 600],
        'Opex_Total': [200, 400, 300],
        'EBITDA': [400, 800, 600],
    })
    return df

@pytest.fixture
def sample_df(tmp_path):
    # Create DataFrame with time series columns
    dates = pd.date_range('2023-01-01', periods=3, freq='MS')
    df = pd.DataFrame({
        'Month': dates,
        'MetricA': [10, 20, 15],
        'MetricB': [5, 7, 6],
    })
    return df


def test_plot_waterfall_creates_file(sample_pnl):
    out_path = os.path.join(tmp_dir, 'waterfall.png')
    plot_waterfall(sample_pnl, out_path)
    assert os.path.isfile(out_path), 'Waterfall image not created'


def test_plot_timeseries_creates_files(sample_df):
    out_dir = tmp_dir / 'ts'
    metrics = ['MetricA', 'MetricB']
    paths = plot_timeseries(sample_df, metrics, str(out_dir))
    assert len(paths) == 2
    for path in paths:
        assert os.path.isfile(path), f'Time series image {path} not created'


def test_generate_summary_writes_markdown(sample_pnl):
    # Use compute_kpis-like dict
    kpis = {'total_revenue': 4500, 'gross_margin_pct': 0.55}
    image_paths = [os.path.join(tmp_dir, 'waterfall.png')]
    # create dummy image
    open(image_paths[0], 'a').close()
    out_md = os.path.join(tmp_dir, 'summary.md')
    generate_summary(kpis, image_paths, out_md)
    assert os.path.isfile(out_md)
    content = open(out_md).read()
    assert '# Executive Summary' in content
    assert '- **Total Revenue**: 4,500.00' in content
    assert f'![](waterfall.png)' in content or '![' in content