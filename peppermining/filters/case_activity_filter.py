from typing import Union, Optional

from peppermining.filters.pepper_filter import PepperFilter
from peppermining.peppermining import PepperMining
from peppermining.utils.enum import EventColumn


class CaseActivityFilter(PepperFilter):
    """ Filter on activities.

    The filter keeps only the cases that with specific activities.

    Methods
    -------
    get_filter
        Return the filters apply in the object.

    Example
    -------
    >>> pm = PepperMining()
    >>> pm.read_event_log_csv("/tests/data/eventlog-example.csv", separator=';', format_date='%d/%m/%Y %H:%M')
    >>> pm.read_cases_csv("/tests/data/case-example.csv", separator=';')
    >>> f1 = CaseActivityFilter(pm, ['examine casually', 'check ticket'])
    >>> f1.get_event_log()
    >>> f2 = CaseActivityFilter(f1, ['reject request'], 'not contain')
    >>> f2.get_event_log()
    >>> f2.get_filter()
    """

    def __init__(self, data: Union[PepperMining, PepperFilter], activities: Optional[list], mode: Optional[str] = 'contain'):
        """Filters the event log that keeps only the cases included in activities list.

        Parameters
        ----------
        data: Union[PepperMining, PepperFilter]
            PepperMining or PepperFilter object.
        activities: Optional[list]
            List of ativities that gonna filter.
        mode: str, Default: contain
            modality of filtering (contain, not contain).
        """
        super().__init__(data)

        self._activities = activities
        self._mode = mode
        case_list = list(data.get_event_log()[(data.get_event_log()[EventColumn.ACTIVITY.value].isin(activities))][EventColumn.CASE_ID.value])
        self.set_event_data_by_case_list(case_list)
        self.set_case_data_by_case_list(case_list)

    def get_filter(self) -> str:
        """Return the filters apply in the object.

        Returns
        -------
        String
            String with list the filters.
        """
        return f"{self.component.get_filter()} [Filter by activity {('', 'not')[self._mode == 'not contain']}({', '.join(self._activities)})]"
