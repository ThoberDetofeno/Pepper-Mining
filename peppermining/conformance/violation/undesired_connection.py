import numpy as np

from typing import Union

from peppermining.utils.enum import EventColumn, ModelColumn
from peppermining.filters.pepper_filter import PepperFilter
from peppermining.peppermining import PepperMining
from peppermining.conformance.violation.pepper_violation import PepperViolation
from peppermining.conformance.process_model import ProcessModel


class UndesiredConnection(PepperViolation):
    """Violation: Undesired Connection.

    Where: activity_x is followed by activity_y.

    Example
    -------
    >>> pm = PepperMining()
    >>> pm.read_event_log_csv("/tests/data/eventlog-example.csv", separator=';', format_date='%d/%m/%Y %H:%M')
    >>> pm.read_cases_csv("/tests/data/case-example.csv", separator=';')
    >>> data = {'activity': ['register request', 'check ticket', 'examine casually', 'decide', 'pay compensation'], 'sorting': [1, 2, 3, 4, 5]}
    >>> df = pd.DataFrame(data, columns=['activity', 'sorting'])
    >>> md = ProcessModel()
    >>> md.set_process_model(df)
    >>> v = UndesiredConnection(pm, md)
    >>> v.get_violation()
    """

    def __init__(self, data: Union[PepperMining, PepperFilter], models: Union[ProcessModel, list]) -> None:
        """Undesired Connection.

        Parameters
        ----------
        data : pd.DataFrame
            PepperMining or PepperFilter object.
        _models : list
            List of ProcessModel objects.
        """
        super().__init__(data, models, "UndesiredConnection")

    def detection(self) -> None:
        """Violation detection.
        """
        # Get eventdata without undesired activity
        event_log = self._component.get_event_log()
        event_log['next_activity'] = event_log.groupby(EventColumn.CASE_ID.value)[EventColumn.ACTIVITY.value].shift(-1)
        violation_log = event_log[event_log[EventColumn.ACTIVITY.value].isin(
            self.get_model_activities()) & event_log['next_activity'].notnull()][[EventColumn.ACTIVITY.value, EventColumn.CASE_ID.value]]
        # Check up new next activity
        violation_log['next_activity'] = violation_log.groupby('case_id')[EventColumn.ACTIVITY.value].shift(-1)
        violation_log = violation_log.replace(np.nan, None)
        # Get process model
        model_log = self.get_model_log()
        model_log['next_activity'] = model_log.groupby(ModelColumn.ID.value)[ModelColumn.ACTIVITY.value].shift(-1)
        model_log = model_log.replace(np.nan, None)
        # Discovery all transitions is not found in process models
        violation_log = violation_log.merge(model_log, on=['activity', 'next_activity'], how='left', indicator=True).query('_merge == "left_only"')
        violation_log = violation_log.drop(columns=['id', '_merge'])
        violation_log = violation_log[violation_log['next_activity'].notnull()]
        violation_log = violation_log.drop_duplicates()
        # Add violation
        for key, row in violation_log.groupby([EventColumn.ACTIVITY.value, 'next_activity'],
                                              group_keys=False)[EventColumn.CASE_ID.value].apply(list).reset_index(name=EventColumn.CASE_ID.value).iterrows():
            self.add_violation(f"{row[EventColumn.ACTIVITY.value]} is followed by {row['next_activity']}",
                               [row[EventColumn.ACTIVITY.value], row['next_activity']], row[EventColumn.CASE_ID.value])
