from typing import Union, Optional

from peppermining.filters.pepper_filter import PepperFilter
from peppermining.peppermining import PepperMining


class CaseFilter(PepperFilter):
    """ Case Filter.

    The case filter keeps only the cases included in a list.

    Methods
    -------
    get_filter
        Return the filters apply in the object.

    Example
    -------
    >>> pm = PepperMining()
    >>> pm.read_event_log_csv("/tests/data/eventlog-example.csv", separator=';', format_date='%d/%m/%Y %H:%M')
    >>> pm.read_cases_csv("/tests/data/case-example.csv", separator=';')
    >>> f1 = CaseFilter(pm, [1, 5, 7, 8])
    >>> f1.get_event_log()
    >>> f2 = CaseFilter(f1, [1, 5], "not contain")
    >>> f2.get_event_log()
    >>> f2.get_filter()
    """

    def __init__(self, data: Union[PepperMining, PepperFilter], case_list: Union[int, str], mode: Optional[str] = 'contain'):
        """Filters the event log that keeps only the cases included in case list.

        Parameters
        ----------
        data: Union[PepperMining, PepperFilter]
            PepperMining or PepperFilter object.
        case_list: Union[int, str]
            List of cases that gonna filter.
        mode: str, Default: contain
            Modality of filtering (contain, not contain).
        """
        super().__init__(data)
        # Filter event and case data by case ID
        self.cases = case_list
        self._mode = mode
        self.set_event_data_by_case_list(case_list)
        self.set_case_data_by_case_list(case_list)

    def get_filter(self) -> str:
        """Return the filters apply in the object.

        Returns
        -------
        String
            String with list the filters.
        """
        return f"{self.component.get_filter()} [Filter by case {('', 'not')[self._mode == 'not contain']}({len(self.cases)} cases)]"
