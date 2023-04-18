import pandas as pd

from peppermining.kpi.pepper_kpi import PepperKpi


class AverageEventsPerCase(PepperKpi):
    """ KPI - Average events per case.

    Methods
    -------
    get_kpi
        Return summary of KPI.

     Example
     -------
     >>> pm = PepperMining()
     >>> pm.read_event_log_csv("/tests/data/eventlog-example.csv", separator=';', format_date='%d/%m/%Y %H:%M')
     >>> pm.read_cases_csv("/tests/data/case-example.csv", separator=';')
     >>> f1 = CaseFilter(pm, [1, 5, 7, 8])
     >>> kp1 = AverageEventsPerCase(pm)
     >>> kp1.get_kpi()
     >>> kp2 = AverageEventsPerCase(f1)
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
        self._kpi_id = "AverageEventsPerCase"
        self._kpi_name = "Average events per case"

    def get_kpi(self) -> pd.DataFrame:
        """Return summary of KPI.

        Returns
        -------
        DataFrame
            DataFrame with the summary data.
        """
        number_events = len(self._component.get_event_log())
        number_cases = len(self._component.get_cases())
        return self.get_summary_df(number_events / number_cases)
