import pandas as pd

from typing import Union, Optional

from peppermining.utils.enum import EventColumn
from peppermining.filters.pepper_filter import PepperFilter
from peppermining.peppermining import PepperMining


def root_cause_analysis(data: Union[PepperMining, PepperFilter], top: Optional[int] = 5) -> pd.DataFrame:
    """Root Cause Analysis of an event log.

    The root cause analysis aims to find process errors and their causes and analyze them.
    These analyses make it possible to determine the proportion of errors found that have the same cause.
    Automated root cause analysis, consisting in analysing the cases attributes and return the most frequent datas.

    Parameters
    ----------
    pepper_data
        It this should be a PepperMining or PepperFilter object.
    top: int, Default: 5
        Choose the number of top frequent datas.

    Example
    -------
    >>> pm = PepperMining()
    >>> ...
    >>> root_cause_analysis(pm)
    """
    df_root_case = pd.DataFrame()
    case_data = data.get_cases()
    # Analysis Root Causes
    column_list = filter(lambda column: column not in [EventColumn.CASE_ID.value], list(case_data.columns))
    column_list = list(column_list)
    for col_name in column_list:
        root_cause = case_data.groupby(col_name)[EventColumn.CASE_ID.value].count().reset_index(name='number_of_case').sort_values(['number_of_case'], ascending=False)
        root_cause['percent_of_case'] = (root_cause[['number_of_case']] * 100) / sum(root_cause['number_of_case'])
        root_cause = root_cause.rename(columns={col_name: "values"})
        root_cause = root_cause.head(top)
        new_root_cause = pd.DataFrame([[col_name, root_cause]], index=[col_name], columns=['column', 'root_cause'])
        df_root_case = pd.concat([new_root_cause, df_root_case.loc[:]]).reset_index(drop=True)
    return df_root_case
