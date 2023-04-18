import numpy as np
import pandas as pd

from peppermining.kpi.pepper_kpi import PepperKpi
from peppermining.utils.enum import EventColumn, KpiColumn, Variant, Flowchart


class ThroughputTime(PepperKpi):
    """ KPI - Throughput time.

    Throughput time is the actual time an activity takes to be done. This includes the entire duration from start to end of the activity,
    which in many cases means the time a factory needs to convert raw materials into finished goods.
    Given an event log, it is possible to retrieve the list of all the durations of the cases (expressed in seconds).

    Methods
    -------
    get_kpi
        Return summary of KPI.
    get_kpi_event_log
        Return KPI value per event log.
    get_kpi_cases
        Return KPI value per case.
    get_kpi_variants
        Return KPI value per variant.
    get_kpi_activities
        Return KPI value per activity.
    get_kpi_process_flow
        Return the Throughput Time the a activity is followed by another specified activity.

    Example
    -------
    >>> pm = PepperMining()
    >>> pm.read_event_log_csv("/tests/data/eventlog-example.csv", separator=';', format_date='%d/%m/%Y %H:%M')
    >>> pm.read_cases_csv("/tests/data/case-example.csv", separator=';')
    >>> f1 = CaseFilter(pm, [1, 5, 7, 8])
    >>> kp1 = ThroughputTime(pm)
    >>> kp1.get_kpi()
    >>> kp2 = ThroughputTime(f1)
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
        self._kpi_id = "ThroughputTime"
        self._kpi_name = "Throughput time"

    def get_kpi(self) -> pd.DataFrame:
        """Return summary of KPI.

        Returns
        -------
        DataFrame
            DataFrame with the summary data.
        """
        _df = self.get_kpi_cases()[self._kpi_id]
        _id = self._kpi_id
        _nm = self._kpi_name
        return pd.DataFrame({KpiColumn.KPI.value: [_nm + ' (Max)', _nm + ' (Min)', _nm + ' (Mean)', _nm + ' (Median)', _nm + ' (Sum)', _nm + ' (StDev)'],
                             KpiColumn.VALUE.value: [_df.max(), _df.min(), _df.mean(), _df.median(), _df.sum(), _df.std()]},
                            index=[_id + 'Max', _id + 'Min', _id + 'Mean', _id + 'Median', _id + 'Sum', _id + 'StDev'])

    def get_kpi_event_log(self) -> pd.DataFrame:
        """Return KPI value per event log.

        Returns
        -------
        DataFrame
            DataFrame with the event log and KPI data.
        """
        df = self._component.get_event_log().copy()
        df['next_'] = df.groupby(EventColumn.CASE_ID.value)[EventColumn.EVENT_TIME.value].shift(-1)
        df[self._kpi_id] = np.where(df.next_.isnull(), 0, (df.next_ - df[EventColumn.EVENT_TIME.value]).dt.seconds)
        return df.replace({np.nan: None}).drop(columns=['next_'])

    def get_kpi_cases(self) -> pd.DataFrame:
        """Return KPI value per case.

        Returns
        -------
        DataFrame
            DataFrame with the cases and and KPI data.
        """
        df_min = self._component.get_event_log().groupby(EventColumn.CASE_ID.value)[EventColumn.EVENT_TIME.value].min().reset_index(name='min_')
        df_max = self._component.get_event_log().groupby(EventColumn.CASE_ID.value)[EventColumn.EVENT_TIME.value].max().reset_index(name='max_')
        df = df_min.merge(df_max, how='left', on=EventColumn.CASE_ID.value).replace(np.nan, None)
        df[self._kpi_id] = (df.min_ - df.max_).dt.seconds
        return df[[EventColumn.CASE_ID.value, self._kpi_id]]

    def get_kpi_activities(self) -> pd.DataFrame:
        """Return KPI Throughput time per activity.

        Returns
        -------
        DataFrame
            DataFrame with the activities and KPI data.
        """
        return self.get_kpi_event_log()[[EventColumn.ACTIVITY.value, self._kpi_id]].groupby([EventColumn.ACTIVITY.value]).\
            ThroughputTime.agg([("ThroughputTimeMin", "min"), ("ThroughputTimeMax", "max"), ("ThroughputTimeMean", "mean"),
                                ("ThroughputTimeMedian", "median"), ("ThroughputTimeSum", "sum"), ("ThroughputTimeStDev", "std")]).reset_index()

    def get_kpi_variants(self) -> pd.DataFrame:
        """Return KPI value per variant.

        Returns
        -------
        DataFrame
            DataFrame with the variants and and KPI data.
        """
        if not ("get_variants" in dir(self._component)):
            raise TypeError("This object is not a PepperVariant.")
        # Explode variants per Case
        variants = self._component.get_variants().copy()
        variants = variants.explode(Variant.CASES.value).reset_index(drop=True).rename(columns={Variant.CASES.value: EventColumn.CASE_ID.value})[[Variant.KEY.value, EventColumn.CASE_ID.value]]
        # Join value Throughput Time per Case
        variants = variants.merge(self.get_kpi_cases(), how='left', on=EventColumn.CASE_ID.value).replace(np.nan, None)
        # Calculate
        return variants[[Variant.KEY.value, self._kpi_id]].groupby([Variant.KEY.value]).ThroughputTime.\
            agg([("ThroughputTimeMin", "min"), ("ThroughputTimeMax", "max"), ("ThroughputTimeMean", "mean"), ("ThroughputTimeMedian", "median"),
                 ("ThroughputTimeSum", "sum"), ("ThroughputTimeStDev", "std")]).replace(np.nan, None).reset_index()

    def get_kpi_process_flow(self, activity_from, activity_to) -> pd.DataFrame:
        """Return the Throughput Time the a activity is followed by another specified activity.

        Parameters
        ----------
        activity_from : str
            String with activity name.
        activity_to : str
            String with activity name.

        Returns
        -------
        DataFrame
            DataFrame with the Throughput Time values.
        """
        _df = self.get_kpi_event_log()
        _id = self._kpi_id
        _nm = self._kpi_name
        _df[Flowchart.ACTIVITY_TO.value] = _df.groupby(EventColumn.CASE_ID.value)[EventColumn.ACTIVITY.value].shift(-1).replace(np.nan, Flowchart.PROCESS_END.value)
        # Filter process flow
        _df = _df[(_df[EventColumn.ACTIVITY.value] == activity_from) & (_df[Flowchart.ACTIVITY_TO.value] == activity_to)][self._kpi_id]
        return pd.DataFrame({KpiColumn.KPI.value: [_nm + ' (Max)', _nm + ' (Min)', _nm + ' (Mean)', _nm + ' (Median)', _nm + ' (Sum)', _nm + ' (StDev)'],
                             KpiColumn.VALUE.value: [_df.max(), _df.min(), _df.mean(), _df.median(), _df.sum(), _df.std()]},
                            index=[_id + 'Max', _id + 'Min', _id + 'Mean', _id + 'Median', _id + 'Sum', _id + 'StDev'])
