# This module is part of dstoolbox.
# Please refer to https://github.com/antobzzll/dstoolbox


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def distribution_analysis(series: pd.Series, 
                          label: str = None, 
                          binwidth: int = None):
    """
    Function that combines `distribution_stats()` and `distribution_plots()`.

    Args:
        series (pd.Series): Input pandas.Series
        label (str, optional): Label that describes the series. Defaults to None.
        binwidth (int, optional): Width of the histogram bins. Defaults to None.
    """
    if not label:
        label = series.name
    distribution_plots(series, label, binwidth)

    stats = distribution_stats(series)
    for k, v in stats.items():
        print(k, "\t", v)


def distribution_plots(series: pd.Series, label: str = None, binwidth=None):
    """
    Creates a distribution plot for a given series.
    It takes in two parameters: the series and an optional label. 
    The code then creates two subplots with a boxplot and a histogram 
    with kernel density estimation on the right. The binwidth parameter 
    can be used to adjust the bin size of the histogram.

    Args:
        series (pd.Series): Input pandas.Series
        label (str, optional): Label that describes the series. Defaults to None.
        binwidth ([type], optional): Width of the histogram bins. Defaults to None.
    """
    if not label:
        label = series.name
    # distribution plots
    fig, ax = plt.subplots(1, 2, figsize=(15, 5))
    sns.boxplot(ax=ax[0], x=series)
    sns.histplot(ax=ax[1], x=series, binwidth=binwidth, kde=True)
    plt.suptitle(f"Distribution of {label}")
    plt.show()


def distribution_stats(series: pd.Series):
    """
    Returns a dictionary with the most common statistics for 
    a given distribution.

    Args:
        series (pd.Series): [description]

    Returns:
        [type]: [description]
    """
    stats = series.describe()

    iqr = stats['75%'] - stats['25%']
    stats['IQR'] = iqr
    low_threshold = stats['25%'] - (1.5 * iqr)
    if low_threshold >= stats['min']:
        stats['lo-wh'] = low_threshold
    stats['hi-wh'] = stats['75%'] + (1.5 * iqr)
    stats['skew'] = series.skew()

    return stats


def obj_vars_unique(df: pd.DataFrame, verbose=False):
    cat_vars = [var for var in df.columns if df[var].dtype in ['object']]
    cat_vars_unique = {}

    for v in cat_vars:
        uniques = df[v].unique()
        cat_vars_unique[v] = uniques
        if verbose:
            print(f"{v}: {uniques}")

    if not verbose:
        return cat_vars_unique


def plot_corr(df: pd.DataFrame, var: str = None):
    corr = df.corr()
    if var:
        heatmap = sns.heatmap(corr[[var]].sort_values(by=var, ascending=False)[1:],
                              vmin=-1, vmax=1, annot=True, cmap='BrBG')
        heatmap.set_title(f'Features correlating with `{var}`')
    else:
        sns.heatmap(corr, vmin=-1, vmax=1,
                    # mask=mask,
                    annot=True, cmap='BrBG')
    plt.show()


def perc_missing_values(df: pd.DataFrame):
    missing = df.isnull().sum().sort_values(ascending=False)/df.shape[0]
    return missing[missing != 0]


def check_column(column: pd.Series):
    n_unique = len(column.unique())
    nulls = column.isnull().sum()
    non_nulls = column.shape[0] - nulls
    print(f'Dtype: {column.dtype}')
    print(f'NULL values: {nulls} ({nulls/column.shape[0]})')
    print(f'NON-NULL values: {non_nulls} ({non_nulls/column.shape[0]})')

    if column.dtype in (int, float):
        print(column.describe())
    else:
        print(f'Unique values: {n_unique} ({n_unique/non_nulls})')
        print(column.unique())
