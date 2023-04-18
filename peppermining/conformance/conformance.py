import pandas as pd

from deepdiff import DeepDiff
from typing import Union, Optional

from peppermining.utils.enum import EventColumn, ModelColumn
from peppermining.filters.pepper_filter import PepperFilter
from peppermining.filters.case_filter import CaseFilter
from peppermining.conformance.process_model import ProcessModel
from peppermining.peppermining import PepperMining


class Conformance():
    """Conformance Checker.

    The conformance checker allows you to automatically compare a reference process model with the actual process flows discovered from the data.
    The difference between the model and actual flows is returned in the dataframe with a diagnostics column.

    Attributes
    ----------
    _component : pd.DataFrame
        PepperMining or PepperFilter object.
    _models : list
        List of ProcessModel objects.
    _conformance_list : pd.DataFrame
        DataFrame with conformance details.

    Methods
    -------
    get_cases
        Return all cases that are in conformance with models.
    get_summary
        Return Conformance overview data.
    diagnostics
        Return the diagnostic per case.

    Example
    -------
    >>> pm = PepperMining()
    >>> pm.read_event_log_csv("/tests/data/eventlog-example.csv", separator=';', format_date='%d/%m/%Y %H:%M')
    >>> pm.read_cases_csv("/tests/data/case-example.csv", separator=';')
    >>> data = {'activity': ['register request', 'check ticket', 'examine casually', 'decide', 'pay compensation'], 'sorting': [1, 2, 3, 4, 5]}
    >>> df = pd.DataFrame(data, columns=['activity', 'sorting'])
    >>> md = ProcessModel()
    >>> md.set_process_model(df)
    >>> c = Conformance(pm, md)
    >>> c.get_cases()
    >>> c.get_summary()
    >>> c.diagnostics()
    """

    def __init__(self, data: Union[PepperMining, PepperFilter], models: Union[ProcessModel, list]) -> None:
        """Conformance constructor.

        Parameters
        ----------
        data : pd.DataFrame
            PepperMining or PepperFilter object.
        _models : list
            List of ProcessModel objects.
        """
        self._component = data
        self._models = models
        self._conformance_list = self.__conformance_discovery()

    def get_cases(self, kpi: Optional[list] = None) -> pd.DataFrame:
        """Return all cases that are in conformance with models.

        Parameters
        ----------
        kpi : list(str)
            The a KPIs list. Choose the KPIs allow for the cases data.
            kpi = ['NumberOfEvents', 'NumberOfActivities', 'Rework']

        Returns
        -------
        DataFrame
            DataFrame with the Cases data.
        """
        return self.__conformance_data().get_cases(kpi)

    def get_summary(self, kpi: Optional[list] = ['NumberOfCases']) -> pd.DataFrame:
        """Return Conformance overview data.

        Parameters
        ----------
        kpi : list(str)
            The a KPIs list. Choose the KPIs allow for the conformance data.
            kpi = ['NumberOfEvents', 'NumberOfActivities', 'NumberOfCases', 'AverageEventsPerCase', 'ThroughputTime', 'Rework']

        Returns
        -------
        DataFrame
            DataFrame with the Conformance data.
        """
        return self.__conformance_data().get_summary(kpi)

    def diagnostics(self) -> pd.DataFrame:
        """Return the diagnostic per case.

        Returns
        -------
        DataFrame
            DataFrame with the diagnosticas data.
            Columns:
            case_id: Case identification
            diagnostic: dictionary with DeepDiff results.
                More information in: https://zepworks.com/deepdiff/current/index.html
        """
        return self._conformance_list[[EventColumn.CASE_ID.value, 'diagnostic']]

    def __conformance_discovery(self) -> pd.DataFrame:
        """Compare process model with the event log and add a diagnostic.

        Returns
        -------
        DataFrame
            DataFrame with the Conformance analysis.
        """
        # Prepare data
        conf_list = self._component.get_event_log().groupby(EventColumn.CASE_ID.value, group_keys=False)[EventColumn.ACTIVITY.value].apply(list)
        conf_list = conf_list.to_frame().reset_index()
        conf_list['has_violation'] = 1
        conf_list['diagnostic'] = None
        model_list = self._models.get_process_model().groupby(ModelColumn.ID.value, group_keys=False)[ModelColumn.ACTIVITY.value].apply(list)
        model_list = model_list.to_frame().reset_index()
        # For each process model, compare process model with the event log using DeepDiff lib
        for key, row in model_list.iterrows():
            act_list = row[ModelColumn.ACTIVITY.value]
            conf_list['diagnostic'] = conf_list.apply(lambda row: {**({} if (row['diagnostic'] is None)
                                                                      else row['diagnostic']), **(DeepDiff(row[ModelColumn.ACTIVITY.value], act_list).to_dict())}, axis=1)
            conf_list['has_violation'] = conf_list.apply(lambda row: len(DeepDiff(row[ModelColumn.ACTIVITY.value], act_list)) if (row['has_violation'] > 0) else 0, axis=1)
        # Return the Conformance list
        return conf_list

    def __conformance_data(self) -> CaseFilter:
        """Return the cases without violation.

        Returns
        -------
        CaseFilter
            CaseFilter object.
        """
        return CaseFilter(self._component, list(self._conformance_list[self._conformance_list['has_violation'] == 0][EventColumn.CASE_ID.value]))
