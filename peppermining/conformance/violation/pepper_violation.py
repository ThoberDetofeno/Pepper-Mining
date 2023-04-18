import pandas as pd

from typing import Union, Optional

from peppermining.utils.enum import ModelColumn, KpiColumn, ViolationColumn
from peppermining.filters.pepper_filter import PepperFilter
from peppermining.filters.case_filter import CaseFilter
from peppermining.peppermining import PepperMining
from peppermining.conformance.process_model import ProcessModel


class PepperViolation():
    """The PepperViolation interface declares common operations for the violation discovery of PepperMining.

    PepperViolation has various specific methods to discovery the violation of an event log:
    (1) UndesiredActivity - activity_x is an undesired activity.
    (2) UndesiredConnection - activity_x followed by activity_y.
    (3) UndesiredStart - activity_x executed as START activity.
    (4) UndesiredEnd - activity_x executed as END activity.
    (5) RunBySameUsers - activity_x and activity_y should be executed by two different users.

    Attributes
    ----------
    _type : str
        Type of violation.
    _violation_list : pd.DataFrame
        DataFrame with violation details.
    _component : pd.DataFrame
        PepperMining or PepperFilter object.
    _models : list
        List of ProcessModel objects.

    Methods
    -------
    detection
        Method that detect the violations.
    get_model_log
        Return logs of process models.
    get_model_activities
        Return all activities of process models.
    add_violation
        Add a violation in a dataframe with a list of violations.
    get_violation
        Return violations data with KPIs.
    """
    # TODO: Customized rule violation.

    def __init__(self, data: Union[PepperMining, PepperFilter], models: Union[ProcessModel, list], violation_type: str) -> None:
        """PepperViolation constructor.

        Parameters
        ----------
        data : pd.DataFrame
            PepperMining or PepperFilter object.
        _models : list
            List of ProcessModel objects.
        violation_type : str
            Type of violation.
        """
        self._type = violation_type
        self._violation_list = pd.DataFrame()
        self._component = data
        self._models = models
        self.detection()

    def detection(self) -> None:
        """Method should be implement each violation to discovery the undesired events.
        """
        pass

    def get_model_log(self) -> pd.DataFrame:
        """Return logs of process models.

        Returns
        -------
        DataFrame
            Logs of Process Models.
        """
        if not (type(self._models) is list):
            return self._models.get_process_model()
        # List of models
        dfmodel = pd.DataFrame()
        for model in self._models:
            dfmodel = pd.concat([model.get_process_model(), dfmodel.loc[:]])
        return dfmodel

    def get_model_activities(self) -> list:
        """Return all activities of process models.

        Returns
        -------
        List
            List of activities.
        """
        if not (type(self._models) is list):
            return list(self._models.get_process_model()[ModelColumn.ACTIVITY.value])
        # List of models
        activities = []
        for model in self._models:
            activities.extend(list(model.get_process_model()[ModelColumn.ACTIVITY.value]))
        return activities

    def add_violation(self, violation_name: str, activity, case) -> None:
        """Add a violation in a dataframe with a list of violations.

        Parameters
        ----------
        violation_name : str
            Description of validation.
        p_activity : list
            Activities of validation.
        case : pd.DataFrame
            Cases of validation.
        """
        new_row = pd.DataFrame({ViolationColumn.TYPE.value: self._type,
                                ViolationColumn.NAME.value: violation_name,
                                ViolationColumn.ACTIVITY.value: [activity],
                                ViolationColumn.CASES.value: [case]
                                }, index=[0])
        self._violation_list = pd.concat([new_row, self._violation_list.loc[:]]).reset_index(drop=True)

    def get_violation(self, kpi: Optional[list] = None) -> pd.DataFrame:
        """Return violations data with KPIs.

        Parameters
        ----------
        kpi : list(str)
            The a KPIs list. Choose the KPIs allow for the validation data.
            kpi = ['NumberOfEvents', 'NumberOfActivities', 'NumberOfCases', 'AverageEventsPerCase', 'ThroughputTime', 'Rework']

        Returns
        -------
        DataFrame
            DataFrame with the Violation data.
        """
        return self._violation_list if kpi is None else self.__add_violation_kpi(kpi)

    def __add_violation_kpi(self, kpi_list) -> pd.DataFrame:
        """Add KPIs per violation

        """
        kpi_df = pd.DataFrame()
        for key, row in self._violation_list.iterrows():
            violation = CaseFilter(self._component, row[ViolationColumn.CASES.value])
            kpi_values = violation.get_summary(kpi_list)[KpiColumn.VALUE.value]
            kpi_values = kpi_values.to_frame().T
            kpi_values = kpi_values.reset_index(drop=True).rename(index={0: key})
            kpi_df = pd.concat([kpi_values, kpi_df.loc[:]])
        # Merge on index the dataframes Violation and KPI
        return pd.merge(self._violation_list, kpi_df, left_index=True, right_index=True)
