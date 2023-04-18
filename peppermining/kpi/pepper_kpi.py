import pandas as pd

from peppermining.utils.enum import KpiColumn


class PepperKpi():
    """The base class should be used to create the statistics and KPI (Key Performance Indicator) in Pepper Mining.

    In Pepper Mining, it is possible to calculate different statistics and KPI on top of event logs and cases.
    The PepperKpi declares common operations for the KPIs of Pepper Mining.
    Each implementation of PepperKpi it can has several specific methods.
    The Pepper Mining has various kpis implemented, such:
    (1) NumberOfEvents: Number of events per: Summary, Cases, Activities, Date (day, month, year), and Variant.
    (2) NumberOfActivities: Number of activities per: Summary, Cases, and Variant.
    (3) NumberOfCases: Number of cases per: Summary, Activities, Date (day, month, year), and Variant.
    (4) AverageEventsPerCase: Average events per case. Disponible in the Summary.
    (5) ThroughputTime: Throughput time per: Summary, Cases, Activities, Event Log, and Variant.
    (6) Rework: Rework per: Summary, Cases, and Activities.

    Attributes
    ----------
    _component
        PepperMining or PepperFilter object.
    _kpi_id : str
        KPI identifier.
    _kpi_name : str
        KPI name.

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
    get_summary_df
        Return standard DataFrame of summary.
    """
    # TODO: KPI - Number of variants (summary).
    # TODO: KPI - Total throughput time in days.
    # TODO: KPI - Ratio of cases flowing through an activity.
    # TODO: KPI - Ratio of cases with a certain process flow.
    # TODO: KPI - Cycle Time.
    # TODO: KPI - Waiting Time.
    # TODO: KPI - Concurrent Activities.
    # TODO: Validate pepper_data if is a PepperMining or PepperFilter object

    def __init__(self, pepper_data):
        """PepperKPI constructor.

        Parameters
        ----------
        pepper_data
            It this should be a PepperMining or PepperFilter object.
        """
        self._component = pepper_data
        self._kpi_id = None
        self._kpi_name = None

    def get_kpi(self) -> pd.DataFrame:
        """Return summary of KPI.

        Returns
        -------
        DataFrame
            DataFrame with the summary data.

        Warns
        ------
            Method not implemented for this KPI.
        """
        raise TypeError(f"Method not implemented for this KPI [{self._kpi_name}].")

    def get_kpi_event_log(self) -> pd.DataFrame:
        """Return KPI value per event log.

        Returns
        -------
        DataFrame
            DataFrame with the event log and KPI data.

        Warns
        ------
            Method not implemented for this KPI.
        """
        raise TypeError(f"Method not implemented for this KPI [{self._kpi_name}].")

    def get_kpi_cases(self) -> pd.DataFrame:
        """Return KPI value per case.

        Returns
        -------
        DataFrame
            DataFrame with the cases and and KPI data.

        Warns
        ------
            Method not implemented for this KPI.
        """
        raise TypeError(f"Method not implemented for this KPI [{self._kpi_name}].")

    def get_kpi_variants(self) -> pd.DataFrame:
        """Return KPI value per variant.

        Returns
        -------
        DataFrame
            DataFrame with the variants and and KPI data.

        Warns
        ------
            Method not implemented for this KPI.
        """
        raise TypeError(f"Method not implemented for this KPI [{self._kpi_name}].")

    def get_kpi_activities(self) -> pd.DataFrame:
        """Return KPI value per activity.

        Returns
        -------
        DataFrame
            DataFrame with the activities and KPI data.

        Warns
        ------
            Method not implemented for this KPI.
        """
        raise TypeError(f"Method not implemented for this KPI [{self._kpi_name}].")

    def get_summary_df(self, kpi_value) -> pd.DataFrame:
        """Return standard DataFrame of summary.

        Parameters
        ----------
        kpi_value
            Value of summary KPI.

        Returns
        -------
        DataFrame
            DataFrame formatted to summary data.
        """
        return pd.DataFrame({KpiColumn.KPI.value: self._kpi_name,
                            KpiColumn.VALUE.value: kpi_value}, index=[self._kpi_id])
