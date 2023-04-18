from typing import Union

from peppermining.utils.enum import EventColumn
from peppermining.filters.pepper_filter import PepperFilter
from peppermining.peppermining import PepperMining
from peppermining.conformance.violation.pepper_violation import PepperViolation
from peppermining.conformance.process_model import ProcessModel


class UndesiredActivity(PepperViolation):
    """Violation: Undesired Activity.

    Where: activity_x is an undesired activity.

    Example
    -------
    >>> pm = PepperMining()
    >>> pm.read_event_log_csv("/tests/data/eventlog-example.csv", separator=';', format_date='%d/%m/%Y %H:%M')
    >>> pm.read_cases_csv("/tests/data/case-example.csv", separator=';')
    >>> data = {'activity': ['register request', 'check ticket', 'examine casually', 'decide', 'pay compensation'], 'sorting': [1, 2, 3, 4, 5]}
    >>> df = pd.DataFrame(data, columns=['activity', 'sorting'])
    >>> md = ProcessModel()
    >>> md.set_process_model(df)
    >>> v = UndesiredActivity(pm, md)
    >>> v.get_violation()
    """

    def __init__(self, data: Union[PepperMining, PepperFilter], models: Union[ProcessModel, list]) -> None:
        """Undesired Activity.

        Parameters
        ----------
        data : pd.DataFrame
            PepperMining or PepperFilter object.
        _models : list
            List of ProcessModel objects.
        """
        super().__init__(data, models, "UndesiredActivity")

    def detection(self) -> None:
        """Violation detection.
        """
        event_log = self._component.get_event_log()
        violation_log = event_log[~event_log[EventColumn.ACTIVITY.value].isin(self.get_model_activities())][[EventColumn.ACTIVITY.value, EventColumn.CASE_ID.value]]
        violation_log = violation_log.drop_duplicates(violation_log)
        # Add violation
        for key, row in violation_log.groupby(EventColumn.ACTIVITY.value, group_keys=False)[EventColumn.CASE_ID.value].apply(list).reset_index(name=EventColumn.CASE_ID.value).iterrows():
            self.add_violation(F'"{row[EventColumn.ACTIVITY.value]}" is an undesired activity', [row[EventColumn.ACTIVITY.value]], row[EventColumn.CASE_ID.value])
