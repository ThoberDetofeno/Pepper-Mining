import numpy as np
import pandas as pd

from peppermining.kpi.pepper_kpi import PepperKpi
from peppermining.utils.enum import EventColumn, Variant, Flowchart


class NumberOfCases(PepperKpi):
    """KPI - Number of cases.

    Compute number of cases per activity, variant, etc.

    Methods
    -------
    get_kpi
        Return summary of KPI.
    get_kpi_variants
        Return KPI value per variant.
    get_kpi_activities
        Return KPI value per activity.
    get_kpi_per_year
        Return KPI value per year.
    get_kpi_per_month
        Return KPI value per month.
    get_kpi_per_day
        Return KPI value per day.
    get_kpi_process_flow
        Return the number of cases the a activity is followed by another specified activity.

    Example
    -------
    >>> pm = PepperMining()
    >>> pm.read_event_log_csv("/tests/data/eventlog-example.csv", separator=';', format_date='%d/%m/%Y %H:%M')
    >>> pm.read_cases_csv("/tests/data/case-example.csv", separator=';')
    >>> f1 = CaseFilter(pm, [1, 5, 7, 8])
    >>> kp1 = NumberOfCases(pm)
    >>> kp1.get_kpi()
    >>> kp2 = NumberOfCases(f1)
    >>> kp2.get_kpi()
    """

    def __init__(self, pepper_data):
        """Constructor.

        Parameters
        ----------
        pepper_data
            It this should be a PepperMining or PepperFilter object.
        """
        super().__init__(pepper_data)
        self._kpi_id = "NumberOfCases"
        self._kpi_name = "Number of cases"

    def get_kpi(self) -> pd.DataFrame:
        """Return summary of KPI.

        Returns
        -------
        DataFrame
            DataFrame with the summary data.
        """
        return self.get_summary_df(len(self._component.get_cases()))

    def get_kpi_activities(self) -> pd.DataFrame:
        """Return KPI value per activity.

        Returns
        -------
        DataFrame
            DataFrame with the activities and KPI data.
        """
        return self._component.get_event_log()[[EventColumn.CASE_ID.value, EventColumn.ACTIVITY.value]].\
            drop_duplicates().value_counts([EventColumn.ACTIVITY.value]).reset_index(name=self._kpi_id)

    def get_kpi_variants(self) -> pd.DataFrame:
        """Return KPI value per variant.

        Returns
        -------
        DataFrame
            DataFrame with the variants and and KPI data.
        """
        if not ("get_variants" in dir(self._component)):
            raise TypeError("This object is not a PepperVariant.")
        variants = self._component.get_variants().copy()
        variants[self._kpi_id] = variants.apply(lambda row: (len(row[Variant.CASES.value])), axis=1)
        return variants[[Variant.KEY.value, self._kpi_id]]

    def get_kpi_per_year(self) -> pd.DataFrame:
        """Return KPI value per year.

        Returns
        -------
        DataFrame
            DataFrame with the year and and KPI data.
        """
        return pd.DataFrame({'year': self._component.get_event_log().groupby([EventColumn.CASE_ID.value]).
                             agg({EventColumn.EVENT_TIME.value: ['min']})[EventColumn.EVENT_TIME.value]['min'].dt.year}
                            ).groupby(['year'])['year'].count()

    def get_kpi_per_month(self) -> pd.DataFrame:
        """Return KPI value per month.

        Returns
        -------
        DataFrame
            DataFrame with the month and and KPI data.
        """
        df = self._component.get_event_log().groupby([EventColumn.CASE_ID.value]).agg({EventColumn.EVENT_TIME.value: ['min']})[EventColumn.EVENT_TIME.value]['min']
        return pd.DataFrame({'year': df.dt.year,
                             'month': df.dt.month}
                            ).groupby(['year', 'month'])['month'].count()

    def get_kpi_per_day(self) -> pd.DataFrame:
        """Return KPI value per day.

        Returns
        -------
        DataFrame
            DataFrame with the day and and KPI data.
        """
        df = self._component.get_event_log().groupby([EventColumn.CASE_ID.value]).agg({EventColumn.EVENT_TIME.value: ['min']})[EventColumn.EVENT_TIME.value]['min']
        return pd.DataFrame({'year': df.dt.year,
                             'month': df.dt.month,
                             'day': df.dt.day}
                            ).groupby(['year', 'month', 'day'])['day'].count()

    def get_kpi_process_flow(self, activity_from, activity_to) -> pd.DataFrame:
        """Return the number of cases the a activity is followed by another specified activity.

        Parameters
        ----------
        activity_from : str
            String with activity name.
        activity_to : str
            String with activity name.

        Returns
        -------
        DataFrame
            DataFrame with the number of cases values.
        """
        _df = self._component.get_event_log().copy()
        if activity_from == Flowchart.PROCESS_START.value:
            _df[Flowchart.ACTIVITY_FROM.value] = _df.groupby(EventColumn.CASE_ID.value)[EventColumn.ACTIVITY.value].shift(1).replace(np.nan, Flowchart.PROCESS_START.value)
            flow_filter = (_df[Flowchart.ACTIVITY_FROM.value] == activity_from) & (_df[Flowchart.ACTIVITY.value] == activity_to)
        else:
            _df[Flowchart.ACTIVITY_TO.value] = _df.groupby(EventColumn.CASE_ID.value)[EventColumn.ACTIVITY.value].shift(-1).replace(np.nan, Flowchart.PROCESS_END.value)
            flow_filter = (_df[EventColumn.ACTIVITY.value] == activity_from) & (_df[Flowchart.ACTIVITY_TO.value] == activity_to)
        _df = _df[flow_filter]
        return self.get_summary_df(len(_df[EventColumn.CASE_ID.value].drop_duplicates()))
