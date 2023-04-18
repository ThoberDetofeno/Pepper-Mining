import numpy as np
import pandas as pd

from typing import Union

from peppermining.filters.pepper_filter import PepperFilter
from peppermining.peppermining import PepperMining
from peppermining.utils.enum import EventColumn


class CaseBetweenTimeFilter(PepperFilter):
    """ Filter the cases between on time frame.

    Keep the cases that are starting in a specific interval time frame.

    Methods
    -------
    get_filter
        Return the filters apply in the object.

    Example
    -------
    >>> pm = PepperMining()
    >>> pm.read_event_log_csv("/tests/data/eventlog-example.csv", separator=';', format_date='%d/%m/%Y %H:%M')
    >>> pm.read_cases_csv("/tests/data/case-example.csv", separator=';')
    >>> f1 = CaseBetweenTimeFilter(pm, '2022-02-02T00:00:00', '2022-02-04T23:59:59')
    >>> f1.get_event_log()
    >>> f2 = CaseFilter(f1, [4,5])
    >>> f2.get_filter()
    """

    def __init__(self, data: Union[PepperMining, PepperFilter],
                 start_time: np.datetime64 = np.datetime64(pd.Timestamp.min),
                 end_time: np.datetime64 = np.datetime64(pd.Timestamp.max)):
        """Filters the event log, keeping the cases having a length (number of events) included between min_size and max_size

        Parameters
        ----------
        data: Union[PepperMining, PepperFilter]
            PepperMining or PepperFilter object.
        start_time: Optional[int], default = pd.Timestamp.min
            Keeping the cases greater that this time.
        end_time: Optional[int], default = pd.Timestamp.max
            Keeping the cases less that this time.
        """
        super().__init__(data)
        self._start_time = np.datetime64(start_time)
        self._end_time = np.datetime64(end_time)
        grouped = data.get_event_log().groupby(EventColumn.CASE_ID.value)
        self.event_data = grouped.filter(lambda x: (x[EventColumn.EVENT_TIME.value].min() >= self._start_time) and (x[EventColumn.EVENT_TIME.value].min() <= self._end_time))
        self.case_data = data.get_cases()[data.get_cases().case_id.isin(list(self.event_data[EventColumn.CASE_ID.value].drop_duplicates()))]

    def get_filter(self) -> str:
        """Return the filters apply in the object.

        Returns
        -------
        String
            String with list the filters.
        """
        return f"{self.component.get_filter()} [Filter cases between {self._start_time} and {self._end_time}]"
