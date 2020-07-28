import pandas as pd
import logging

log = logging.getLogger(__name__)


def detect_recurrent_tx(tx: pd.DataFrame, exact: bool = False):
    rv = None
    if not exact:
        raise NotImplemented
    else:
        out_counts = tx.groupby('out').count()

    return rv
