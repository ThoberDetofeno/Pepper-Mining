import pandas as pd

from peppermining.kpi.pepper_kpi import PepperKpi
from peppermining.utils.enum import EventColumn


class Rework(PepperKpi):
    """ KPI - Rework.

    The rework statistic can be useful to identify the cases in which many events are repetitions of activities that have already been performed.

    Methods
    -------
    get_kpi
        Return summary of KPI.
    get_kpi_cases
        Return KPI value per case.
    get_kpi_activities
        Return KPI value per activity.

    Example
    -------
    >>> pm = PepperMining()
    >>> pm.read_event_log_csv("/tests/data/eventlog-example.csv", separator=';', format_date='%d/%m/%Y %H:%M')
    >>> pm.read_cases_csv("/tests/data/case-example.csv", separator=';')
    >>> f1 = CaseFilter(pm, [1, 5, 7, 8])
    >>> kp1 = Rework(pm)
    >>> kp1.get_kpi()
    >>> kp2 = Rework(f1)
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
        self._kpi_id = "Rework"
        self._kpi_name = "Rework"

    def get_kpi(self) -> pd.DataFrame:
        """Return summary of KPI.

        Calculates the total number of activities that were repeated.

        Returns
        -------
        DataFrame
            DataFrame with the summary data.
        """
        return self.get_summary_df(sum(self.__rework_df()[self._kpi_id]))

    def get_kpi_cases(self) -> pd.DataFrame:
        """Return KPI Rework per case.

        We define as rework at the case level the number of events of a case having an activity which has appeared previously in the case.

        Returns
        -------
        DataFrame
            DataFrame with the cases and and KPI data.
        """
        return self.__rework_df().groupby([EventColumn.CASE_ID.value]).sum().reset_index()

    def get_kpi_activities(self) -> pd.DataFrame:
        """Compute KPI Rework per Activity

        The rework statistic permits to identify the activities which have been repeated during the same process execution.
        This shows the underlying inefficiencies in the process.

        Returns
        -------
        DataFrame
            DataFrame with the activities and KPI data.
        """
        return self.__rework_df().groupby([EventColumn.ACTIVITY.value])[self._kpi_id].sum().reset_index()

    def __rework_df(self) -> pd.DataFrame:
        """Compute the rework.

        Returns
        -------
        DataFrame
            DataFrame with the reworks data.
        """
        df = self._component.get_event_log().groupby([EventColumn.CASE_ID.value, EventColumn.ACTIVITY.value]).size().reset_index(name=self._kpi_id)
        df[self._kpi_id] = df[self._kpi_id] - 1
        return df
