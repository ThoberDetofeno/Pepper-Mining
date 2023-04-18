import numpy as np

from typing import Union

from peppermining.utils.enum import EventColumn, ModelColumn
from peppermining.filters.pepper_filter import PepperFilter
from peppermining.peppermining import PepperMining
from peppermining.conformance.violation.pepper_violation import PepperViolation
from peppermining.conformance.process_model import ProcessModel


class UndesiredEnd(PepperViolation):
    """Violation: Undesired end activity.

    Where: activity_x executed as END activity.

    Example
    -------
    >>> pm = PepperMining()
    >>> pm.read_event_log_csv("/tests/data/eventlog-example.csv", separator=';', format_date='%d/%m/%Y %H:%M')
    >>> pm.read_cases_csv("/tests/data/case-example.csv", separator=';')
    >>> data = {'activity': ['register request', 'check ticket', 'examine casually', 'decide', 'pay compensation'], 'sorting': [1, 2, 3, 4, 5]}
    >>> df = pd.DataFrame(data, columns=['activity', 'sorting'])
    >>> md = ProcessModel()
    >>> md.set_process_model(df)
    >>> v = UndesiredEnd(pm, md)
    >>> v.get_violation()
    """

    def __init__(self, data: Union[PepperMining, PepperFilter], models: Union[ProcessModel, list]) -> None:
        """Undesired end activity.

        Parameters
        ----------
        data : pd.DataFrame
            PepperMining or PepperFilter object.
        _models : list
            List of ProcessModel objects.
       """
        super().__init__(data, models, "UndesiredEnd")

    def detection(self) -> None:
        """Violation detection.
        """
        event_log = self._component.get_event_log()
        event_log['next_activity'] = event_log.groupby(EventColumn.CASE_ID.value)[EventColumn.ACTIVITY.value].shift(-1)
        event_log = event_log.replace(np.nan, None)
        model_log = self.get_model_log()
        model_log['next_activity'] = model_log.groupby(ModelColumn.ID.value)[ModelColumn.ACTIVITY.value].shift(-1)
        model_log = model_log.replace(np.nan, None)
        end_list = list(model_log[model_log['next_activity'].isnull()][ModelColumn.ACTIVITY.value])
        violation_log = event_log[(event_log['next_activity'].isnull()) & (~event_log[EventColumn.ACTIVITY.value].isin(end_list))][[EventColumn.ACTIVITY.value, EventColumn.CASE_ID.value]]
        # Add violation
        for key, row in violation_log.groupby(EventColumn.ACTIVITY.value, group_keys=False)[EventColumn.CASE_ID.value].apply(list).reset_index(name=EventColumn.CASE_ID.value).iterrows():
            self.add_violation(F'"{row[EventColumn.ACTIVITY.value]}" executed as END activity', [row[EventColumn.ACTIVITY.value]], row[EventColumn.CASE_ID.value])
