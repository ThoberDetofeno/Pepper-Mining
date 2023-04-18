import pandas as pd

from peppermining.kpi.pepper_kpi import PepperKpi
from peppermining.utils.enum import EventColumn, Variant


class NumberOfActivities(PepperKpi):
    """ KPI - Number of activities.

    Compute number of activities.

    Methods
    -------
    get_kpi
        Return summary of KPI.
    get_kpi_cases
        Return KPI value per case.
    get_kpi_variants
        Return KPI value per variant.

    Example
    -------
    >>> pm = PepperMining()
    >>> pm.read_event_log_csv("/tests/data/eventlog-example.csv", separator=';', format_date='%d/%m/%Y %H:%M')
    >>> pm.read_cases_csv("/tests/data/case-example.csv", separator=';')
    >>> f1 = CaseFilter(pm, [1, 5, 7, 8])
    >>> kp1 = NumberOfActivities(pm)
    >>> kp1.get_kpi()
    >>> kp2 = NumberOfActivities(f1)
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
        self._kpi_id = "NumberOfActivities"
        self._kpi_name = "Number of activities"

    def get_kpi(self) -> pd.DataFrame:
        """Return summary of KPI.

        Returns
        -------
        DataFrame
            DataFrame with the summary data.
        """
        return self.get_summary_df(len(self._component.get_event_log().groupby(EventColumn.ACTIVITY.value).nunique()))

    def get_kpi_cases(self) -> pd.DataFrame:
        """Return KPI value per case.

        Returns
        -------
        DataFrame
            DataFrame with the cases and and KPI data.
        """
        return self._component.get_event_log().groupby([EventColumn.CASE_ID.value])[EventColumn.ACTIVITY.value].nunique().reset_index(name=self._kpi_id)

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
        variants[self._kpi_id] = variants.apply(lambda row: (len(row[Variant.ACTIVITIES.value])), axis=1)
        return variants[[Variant.KEY.value, self._kpi_id]]
