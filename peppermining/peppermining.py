import numpy as np
import pandas as pd

from pandas.api.types import is_datetime64_any_dtype
from typing import Optional

from peppermining.utils.enum import EventColumn
from peppermining.pepper import Pepper


class PepperMining(Pepper):
    """PepperMining is a open source Process Mining platform.

    Process mining refers to discovering knowledge about business processes from the automatic analysis of event logs.
    The first step to using the Pepper Mining is create the PepperMining object and add event logs.

    Methods
    -------
    set_event_log
        Input the event logs data.
    set_cases
        Input the cases data.
    clear_datas
        Clear event log and cases.
    clear_cases
        Clear cases.
    read_event_log_csv
        Import the CSV to event logs data.
    read_cases_csv
        Import the CSV to cases data.

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
    >>> pm.set_event_log(df)
    >>> pm.get_event_data()
    """
    # TODO: Read IEEE XES files. http://www.xes-standard.org/

    def __init__(self):
        """Created PepperMining object.
        """
        super().__init__()
        self.__format_date_csv = None

    def set_event_log(self, event_log: pd.DataFrame) -> None:
        """Input the event logs data.

        Input the event logs of a pandas DataFrame.
        The DataFrame must be the columns: 'case_id', 'activity' and 'event_time'.
        The column 'user' is used in some functions, but this it not mandatory.

        Parameters
        ----------
        event_log : pd.DataFrame
            DataFrame with 'case_id', 'activity', and 'event_time' columns.

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
        >>> pm.set_event_log(df)
        >>> pm.get_event_data()
        """
        self.event_data = self.__validate_event_data(event_log)
        self.case_data = self.event_data[EventColumn.CASE_ID.value].drop_duplicates().reset_index(drop=True).to_frame()

    def set_cases(self, cases: pd.DataFrame) -> None:
        """Input cases to event logs.

        Input the cases of a pandas DataFrame.
        The DataFrame must be the column 'case_id'.
        Is not mandatory add cases to use the PepperMining.
        In order to have a good experience in the root cause analysis, it is important include more information for the cases.

        Parameters
        ----------
        cases : pd.DataFrame
            DataFrame with 'case_id' column.

        Example
        -------
        >>> data = {'case_id': [1, 2, 3, 4, 5, 6, 7, 8],
                    'product': ['Pumpkin', 'Carrots', 'Chilli peppers', 'Ginger', 'Mushrooms', 'Potatoes', 'Fresh herbs', 'Chokos']}
        >>> df = pd.DataFrame(data, columns=['case_id', 'product'])
        >>> pm.set_event_log(df)
        >>> pm.get_event_data()
        """
        self.case_data = self.__validate_case_data(cases)

    def clear_datas(self) -> None:
        """Clear event log and cases.

        Remove all rows and columns.
        After this method is possible include a new event logs to the peppermining object.
        """
        self.event_data = pd.DataFrame()
        self.case_data = pd.DataFrame()

    def clear_cases(self) -> None:
        """Clear cases.

        Reset the case data.
        After this method is possible include a new cases to the peppermining object.
        """
        self.case_data = self.event_data[EventColumn.CASE_ID.value].drop_duplicates().reset_index(drop=True)

    def read_event_log_csv(self, file_path: str, separator: Optional[str] = ';', format_date: Optional[str] = None) -> None:
        """Import the CSV to event logs data.

        Import the CSV into a pandas DataFrame.
        Convert the CSV into an event log Pandas DataFrame.
        The first step is to import the CSV file and internal API validate and convert it to the event log.
        See more infomation in the pandas documentation.

        Parameters
        ----------
        file_path : str
            Any valid string path is acceptable.
        separator : str
            Delimiter used in CSV file
        format_date : str
            The strftime to parse time, e.g. "%d/%m/%Y %H:%M". format='%d/%m/%Y %H:%M'
            If None then is used pd.to_datetime without format.
            See strftime documentation for more information on choices.
            https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

        Example
        -------
        >>> pm = PepperMining()
        >>> pm.read_event_log_csv("tests/data/eventlog-example.csv", separator=';', format_date='%d/%m/%Y %H:%M')
        >>> pm.get_event_data()

        See Also
        --------
        https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html?highlight=read_csv#
        """
        df = pd.read_csv(file_path, sep=separator)
        self.__format_date_csv = format_date
        self.set_event_log(df)

    def read_cases_csv(self, file_path: str, separator: Optional[str] = ';') -> None:
        """Import the CSV to cases data.

        Import the CSV into a pandas DataFrame.
        Convert the CSV into a Cases Pandas DataFrame.
        The first step is to import the CSV file and internal API validate and convert it to the event log.
        See more infomation in the pandas documentation.

        Parameters
        ----------
        file_path : str
            Any valid string path is acceptable.
        separator : str
            Delimiter used in CSV file.

        Example
        -------
        >>> pm = PepperMining()
        >>> pm.read_event_log_csv("c:/Temp/base-peppermining/peppermining/tests/data/eventlog-example.csv", separator=';',
                                  format_date='%d/%m/%Y %H:%M')
        >>> pm.read_cases_csv("c:/Temp/base-peppermining/peppermining/tests/data/case-example.csv", separator=';')
        >>> pm.get_cases()

        See Also
        --------
        https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html?highlight=read_csv#
        """
        df = pd.read_csv(file_path, sep=separator)
        self.set_cases(df)

    def __validate_event_data(self, p_df: pd.DataFrame) -> pd.DataFrame:
        """Validate event logs data.

        Parameters
        ----------
        p_df : pd.DataFrame
            DataFrame with case_id, activity, and event_time columns.

        Returns
        -------
        DataFrame
            DataFrame with the data valid and datetime format.

        Raises
        ------
        ValueError
            (1) Only Pandas DataFrame are allowed in Event logs.
            (2) Has event logs data. It needs clear the event log.
            (3) Not exists the column case_id, the column case_id is mandatory.
            (4) Not exists the column activity, the column activity is mandatory.
            (5) Not exists the column event_time, the column event_time is mandatory.
            (6) The column event_time is a datetime type invalid.
        """
        if not (isinstance(p_df, pd.DataFrame)):
            raise TypeError("Only Pandas DataFrame are allowed in Event logs.")
        if not (self.event_data.empty):
            raise TypeError("Has event logs data. It needs clear the event logs. e.g. Use the method clear_datas.")
        if not (EventColumn.CASE_ID.value in p_df.columns):
            raise TypeError(f"Not exists the column {EventColumn.CASE_ID.value}, the column {EventColumn.CASE_ID.value} is mandatory.")
        if not (EventColumn.ACTIVITY.value in p_df.columns):
            raise TypeError(f"Not exists the column {EventColumn.ACTIVITY.value}, the column {EventColumn.ACTIVITY.value} is mandatory.")
        if not (EventColumn.EVENT_TIME.value in p_df.columns):
            raise TypeError(f"Not exists the column {EventColumn.EVENT_TIME.value}, the column {EventColumn.EVENT_TIME.value} is mandatory.")
        # Format event_time to datetime valid
        p_df[EventColumn.EVENT_TIME.value] = pd.to_datetime(p_df[EventColumn.EVENT_TIME.value], format=self.__format_date_csv, errors='ignore')
        if not (is_datetime64_any_dtype(p_df[EventColumn.EVENT_TIME.value])):
            raise TypeError(f"The column {EventColumn.EVENT_TIME.value} is a datetime type invalid.")
        #
        return p_df

    def __validate_case_data(self, p_df: pd.DataFrame) -> pd.DataFrame:
        """Validate Cases data.

        Parameters
        ----------
        p_df : pd.DataFrame
            DataFrame with case_id and another columns.

        Returns
        -------
        DataFrame
            DataFrame with the data valid.

        Raises
        ------
        ValueError
            (1) Only Pandas DataFrame are allowed in Cases.
            (2) Has event Cases. It needs clear the datas.
            (3) Not exists the column case_id, the column case_id is mandatory.
            (4) Has not event logs data. Before add Cases data, is required has event logs.
            (5) Exists Case without event logs.
        """
        # TODO: Checking for duplicate keys
        if not (isinstance(p_df, pd.DataFrame)):
            raise TypeError("Only Pandas DataFrame are allowed in Cases.")
        if not (self.case_data.equals(self.event_data['case_id'].drop_duplicates().reset_index(drop=True).to_frame())):
            raise TypeError("Has cases data. It needs clear the datas. e.g. Use the method clear_cases.")
        if not (EventColumn.CASE_ID.value in p_df.columns):
            raise TypeError(f"Not exists the column {EventColumn.CASE_ID.value}, the column {EventColumn.CASE_ID.value} is mandatory.")
        if self.event_data.empty:
            raise TypeError("Has not event logs data. Before add Cases data, is required has event logs.")
        if False in (p_df[EventColumn.CASE_ID.value].isin(self.event_data[EventColumn.CASE_ID.value])).values:
            raise TypeError("Exists case without event logs. Is required to remove the cases without event logs.")
        # Exist event log without Case Then a merge is made
        if False in (self.event_data[EventColumn.CASE_ID.value].isin(p_df[EventColumn.CASE_ID.value])).values:
            p_df = p_df.merge(self.case_data, how='right', on='case_id').replace(np.nan, None)
        return p_df
