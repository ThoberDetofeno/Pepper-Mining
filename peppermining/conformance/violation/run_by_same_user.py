from typing import Union

from peppermining.utils.enum import EventColumn
from peppermining.filters.pepper_filter import PepperFilter
from peppermining.peppermining import PepperMining
from peppermining.conformance.violation.pepper_violation import PepperViolation


class RunBySameUser(PepperViolation):
    """Violation: Activities executed by the same user.

    Where: activity_x and activity_y should be executed by two different users.

    Example
    -------
    >>> data = {'case_id': [1, 1, 1, 1, 1, 2, 2, 2, 2],
                'activity': ['register request', 'check ticket', 'examine thoroughly', 'decide', 'reject request', 'register request',
                             'check ticket', 'examine casually', 'decide'],
                'event_time': ['2022-02-01 11:02:00', '2022-02-02 10:06:00', '2022-02-02 15:12:00', '2022-02-03 11:18:00', '2022-02-03 14:24:00',
                               '2022-02-01 11:32:00', '2022-02-01 12:12:00', '2022-02-01 14:16:00', '2022-02-03 11:22:00'],
                'user': ['Pete', 'Sue', 'Mike', 'Sara', 'Pete', 'Mike', 'Mike', 'Sean', 'Sara']}
    >>> df = pd.DataFrame(data, columns=['case_id', 'activity', 'event_time', 'user'])
    >>> pm = PepperMining()
    >>> violation = RunBySameUser(pm, ['register request', 'check ticket', 'pay compensation'])
    >>> violation.get_violation()
    """

    def __init__(self, data: Union[PepperMining, PepperFilter], activities: list, user_key: str = EventColumn.USER.value) -> None:
        """Activities executed by the same user.

        Parameters
        ----------
        data : pd.DataFrame
            PepperMining or PepperFilter object.
        activities : list
            List of activities that should be executed per different users.
            activities = ['register request', 'check ticket', 'pay compensation']
        user_key : str, Default: 'user'
            attribute to be used as user identifier.
       """
        self._activities = activities
        self._user = user_key
        super().__init__(data, None, "RunBySameUser")

    def detection(self) -> None:
        """Violation detection.
        """
        if (len(list(dict.fromkeys(self._activities))) < 2):
            raise TypeError("Is mandatory two or more different activities.")
        event_log = self._component.get_event_log()
        if (self._user not in event_log.columns):
            raise TypeError(f"Not exists the column {self._user} in the event logs.")
        event_log = event_log[event_log[EventColumn.ACTIVITY.value].isin(self._activities)]
        event_log = event_log.groupby(['case_id', 'user'], group_keys=False).activity.apply(list)
        event_log = event_log.reset_index()
        event_log[EventColumn.ACTIVITY.value] = event_log.apply(lambda row: list(dict.fromkeys(row[EventColumn.ACTIVITY.value])), axis=1)
        event_log['number_activities'] = event_log.apply(lambda row: len(list(dict.fromkeys(row[EventColumn.ACTIVITY.value]))), axis=1)
        violation_log = event_log[event_log['number_activities'] > 1]
        # Add violation
        for key, row in violation_log.groupby(self._user, group_keys=False)[EventColumn.CASE_ID.value].apply(list).reset_index(name=EventColumn.CASE_ID.value).iterrows():
            self.add_violation(F'"{row[self._user]}" executed by two different activities', None, row[EventColumn.CASE_ID.value])
