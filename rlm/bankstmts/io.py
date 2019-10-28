import logging
import warnings
import glob
import pandas as pd
from typing import Callable

log = logging.getLogger(__name__)


def read_tx_files(fpath_pattern, tx_file_reader: Callable[[str], pd.DataFrame]):
    """

    Loads a set of TX files from a glob pattern.

    All TX files must contain at least 'out', 'in', and 'balance' columns.

    :param fpath_pattern:
    :param tx_file_reader: a function that takes str, loads that file, and returns a DataFrame structured as above.
    :return: pd.DataFrame
    """
    df_list = []
    fpath_patterns = glob.glob(fpath_pattern)
    for fpath in fpath_patterns:
        df = tx_file_reader(fpath)
        df['fpath'] = fpath
        df_list += [df]

    if len(df_list) < 1:
        warn_str = 'no files found with pattern \'{}\''.format(fpath_pattern)
        warnings.warn(warn_str)
        log.warning(warn_str)
        df = None
    else:
        df = pd.concat(df_list).sort_values('Date')
        cols_subset = set(df.columns).difference({'fpath'})
        df = df[~df.duplicated(subset=cols_subset)]
        log.info(' |-> read {:d} unique transactions from {:d} files: from {} to {}'.format(
            len(df),
            len(df_list),
            df.Date.min(),
            df.Date.max()
        ))
    return df


def read_tx_accounts(fpath_patterns, tx_file_reader: Callable[[str], pd.DataFrame]):
    """
    Loads a set of sets of files, each set being multiple files identified with glob patterns.

    :param fpath_patterns: a dictionary mapping an account to a glob pattern.
    :param tx_file_reader: a function that takes str, loads that file, and returns a DataFrame structured as above.

    :return: pd.DataFrame
    """
    df_list = []
    for acct, fpath_pattern in fpath_patterns.items():
        df = read_tx_files(fpath_pattern, tx_file_reader)
        if df is not None:
            df['account'] = acct
            df_list += [df]

    if len(df_list) > 0:
        df = pd.concat(df_list).sort_values('Date')
        log.info('=> read {:d} transactions from {:d} accounts: from {} to {}'.format(
            len(df),
            len(df_list),
            df.Date.min(),
            df.Date.max()
        ))
    else:
        df = None

    return df
