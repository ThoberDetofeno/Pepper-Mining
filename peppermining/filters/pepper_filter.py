from typing import Union

from peppermining.pepper import Pepper


class PepperFilter(Pepper):
    """ The PepperFilter declares common operations for the Filters of PepperMining.

    PepperMining has various specific methods to filter an event log:
    (1) Case Filter: The case filter keeps only the cases included in a list.
    (2) Case Size Filter: The case size filter keeps only the cases in the log with a number of events included in a range specified.
    (3) Filter the cases between on time frame: Keep the cases that are starting in a specific interval time frame.
    (4) Filter on start activities: The filter keeps only the cases that start with specific activities.
    (5) Filter on end activities: The filter keeps only the cases that end with specific activities.
    (6) Activity selection: Select cases that flow or don't flow through specified activities.
    (7) Variant Filter: Keep the cases and logs that are in specified variants.

    Attributes
    ----------
    _component
        PepperMining or PepperFilter object.
    _mode : str
        Modality of filtering ('contain' or 'not contain').

    Methods
    -------
    component
        The Decorator delegates all work to the wrapped component.
    get_filter
        Decorator (get_filter) that call parent implementation of the operation, instead of calling the wrapped object directly.
    set_event_data_by_case_list
        Filters the event log that keeps only the cases included in case list.
    set_case_data_by_case_list
        Filters the cases data that included in case list.
    """
    # TODO: Filter - Attribute selection:  Select cases based on specified attributes.
    # TODO: Filter - Process flow selection: Select cases where a specified activity is or isn't followed by another specified activity.
    # TODO: Filter - Throughput time selection: Select cases where duration between two activities is faster/slower than defined period of time.
    # TODO: Filter - Rework selection: Select cases where an activity occurs less or more times than defined threshold.
    # TODO: Filter - Crop selection: Crop the cases to display only activities occurring inside the cropped area.

    _component: Pepper = None

    def __init__(self, pepper_data: Pepper):
        """PepperFilter constructor.

        Parameters
        ----------
        pepper_data
            It this should be a PepperMining or PepperFilter object.
        """
        super().__init__()
        self._component = pepper_data
        self._mode = 'contain'

    @property
    def component(self) -> Pepper:
        """The Decorator delegates all work to the wrapped component.

        Returns
        -------
        Pepper
            PepperMining or PepperFilter object.
        """
        return self._component

    def get_filter(self) -> str:
        """Decorator (get_filter) that call parent implementation of the operation, instead of calling the wrapped object directly.

        Returns
        -------
        String
            String with list the filters.
        """
        return self._component.get_filter()

    def set_event_data_by_case_list(self, case_list: Union[int, str]) -> None:
        """Filters the event log that keeps only the cases included in case list.

        Parameters
        ----------
        case_list: Union[int, str]
            List of cases that gonna filter.
        """
        self.event_data = self._component.get_event_log()[(self._component.get_event_log().case_id.isin(case_list),
                                                           ~self._component.get_event_log().case_id.isin(case_list))[self._mode == 'not contain']]

    def set_case_data_by_case_list(self, case_list: Union[int, str]) -> None:
        """Filters the cases data that included in case list.

        Parameters
        ----------
        case_list: Union[int, str]
            List of cases that gonna filter.
        """
        self.case_data = self._component.get_cases()[(self._component.get_cases().case_id.isin(case_list),
                                                      ~self._component.get_cases().case_id.isin(case_list))[self._mode == 'not contain']]
