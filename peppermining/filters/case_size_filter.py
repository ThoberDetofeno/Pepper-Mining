from decimal import Decimal
from typing import Union, Optional

from peppermining.filters.pepper_filter import PepperFilter
from peppermining.peppermining import PepperMining
from peppermining.utils.enum import EventColumn


class CaseSizeFilter(PepperFilter):
    """ Case Size Filter.

    The case size filter keeps only the cases in the log with a number of events included in a range specified.

    Methods
    -------
    get_filter
        Return the filters apply in the object.

    Example
    -------
    >>> pm = PepperMining()
    >>> pm.read_event_log_csv("/tests/data/eventlog-example.csv", separator=';', format_date='%d/%m/%Y %H:%M')
    >>> pm.read_cases_csv("/tests/data/case-example.csv", separator=';')
    >>> f1 = CaseSizeFilter(pm, 8, 15)
    >>> f1.get_event_log()
    >>> f2 = CaseFilter(f1, [3])
    >>> f2.get_event_log()
    >>> f2.get_filter()
    """

    def __init__(self, data: Union[PepperMining, PepperFilter], min_size: Optional[int] = 0, max_size: Optional[int] = Decimal('Infinity')):
        """
        Filters the event log, keeping the cases having a length (number of events) included between min_size and max_size

        Parameters
        ----------
        data: Union[PepperMining, PepperFilter]
            PepperMining or PepperFilter object.
        min_size: Optional[int], default = None
            Minimum allowed number of events.
        max_size: Optional[int], default = Infinity
            Maximum allowed number of events.
        """
        super().__init__(data)
        self._min_size = min_size
        self._max_size = max_size
        grouped = data.get_event_log().groupby(EventColumn.CASE_ID.value)
        self.event_data = grouped.filter(lambda x: (x[EventColumn.CASE_ID.value].count() >= min_size) and (x[EventColumn.CASE_ID.value].count() <= max_size))
        self.case_data = data.get_cases()[data.get_cases().case_id.isin(list(self.event_data[EventColumn.CASE_ID.value].drop_duplicates()))]

    def get_filter(self) -> str:
        """Return the filters apply in the object.

        Returns
        -------
        String
            String with list the filters.
        """
        return f"{self.component.get_filter()} [Filter by case size ({self._min_size}, {self._max_size})]"
