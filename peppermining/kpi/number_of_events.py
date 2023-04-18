import pandas as pd

from peppermining.kpi.pepper_kpi import PepperKpi
from peppermining.utils.enum import EventColumn, Variant


class NumberOfEvents(PepperKpi):
    """KPI - Number of events.

    Compute number of event log per case, activity, variant, etc.

    Methods
    -------
    get_kpi
        Return summary of KPI.
    get_kpi_cases
        Return KPI value per case.
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

    Example
    -------
    >>> pm = PepperMining()
    >>> pm.read_event_log_csv("/tests/data/eventlog-example.csv", separator=';', format_date='%d/%m/%Y %H:%M')
    >>> pm.read_cases_csv("/tests/data/case-example.csv", separator=';')
    >>> f1 = CaseFilter(pm, [1, 5, 7, 8])
    >>> kp1 = NumberOfEvents(pm)
    >>> kp1.get_kpi()
    >>> kp2 = NumberOfEvents(f1)
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
        self._kpi_id = "NumberOfEvents"
        self._kpi_name = "Number of events"

    def get_kpi(self) -> pd.DataFrame:
        """Return summary of KPI.

        Returns
        -------
        DataFrame
            DataFrame with the summary data.
        """
        return self.get_summary_df(len(self._component.get_event_log()))

    def get_kpi_cases(self) -> pd.DataFrame:
        """Return KPI value per case.

        Returns
        -------
        DataFrame
            DataFrame with the cases and and KPI data.
        """
        return self._component.get_event_log().value_counts([EventColumn.CASE_ID.value]).reset_index(name=self._kpi_id)

    def get_kpi_activities(self) -> pd.DataFrame:
        """Return KPI value per activity.

        Returns
        -------
        DataFrame
            DataFrame with the activities and KPI data.
        """
        return self._component.get_event_log().value_counts([EventColumn.ACTIVITY.value]).reset_index(name=self._kpi_id)

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
        event_log = self._component.get_event_log()
        variants[self._kpi_id] = variants.apply(lambda row: event_log.case_id.isin(row[Variant.CASES.value]).value_counts()[True], axis=1)
        return variants[[Variant.KEY.value, self._kpi_id]]

    def get_kpi_per_year(self) -> pd.DataFrame:
        """Return KPI value per year.

        Returns
        -------
        DataFrame
            DataFrame with the year and and KPI data.
        """
        return pd.DataFrame({'year': self._component.get_event_log()[EventColumn.EVENT_TIME.value].dt.year}
                            ).groupby(['year'])['year'].count()

    def get_kpi_per_month(self) -> pd.DataFrame:
        """Return KPI value per month.

        Returns
        -------
        DataFrame
            DataFrame with the month and and KPI data.
        """
        return pd.DataFrame({'year': self._component.get_event_log()[EventColumn.EVENT_TIME.value].dt.year,
                             'month': self._component.get_event_log()[EventColumn.EVENT_TIME.value].dt.month}
                            ).groupby(['year', 'month'])['month'].count()

    def get_kpi_per_day(self) -> pd.DataFrame:
        """Return KPI value per day.

        Returns
        -------
        DataFrame
            DataFrame with the day and and KPI data.
        """
        return pd.DataFrame({'year': self._component.get_event_log()[EventColumn.EVENT_TIME.value].dt.year,
                             'month': self._component.get_event_log()[EventColumn.EVENT_TIME.value].dt.month,
                             'day': self._component.get_event_log()[EventColumn.EVENT_TIME.value].dt.day}
                            ).groupby(['year', 'month', 'day'])['day'].count()
