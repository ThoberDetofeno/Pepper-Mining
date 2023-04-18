import pandas as pd
import uuid

from typing import Optional

from peppermining.utils.enum import ModelColumn


class ProcessModel():
    """Process Model represent the ideal model that used in the identification of validations and conformance.

    A Process Model is a depiction of the flow of work and tasks for specific goals.
    Process Models are important because they document existing processes and provide process knowledge.
    In the Pepper Mining the Process Model represent the ideal model, or the model that defines when the cases are in compliance.
    Each Process Model represent a process with Start and End.

    Methods
    -------
    set_process_model
        Input Process Model data.
    read_process_model_csv
        Import the CSV to process model data.
    get_process_model
        Return Process Model data.
    clear_datas
        Clear Process Model.

    Example
    -------
    >>> data = {'activity': ['register request', 'check ticket', 'examine casually', 'decide', 'pay compensation'],
                'sorting': [1, 2, 3, 4, 5]}
    >>> df = pd.DataFrame(data, columns=['activity', 'sorting'])
    >>> md = ProcessModel()
    >>> md.set_process_model(df)
    >>> md.get_process_model()
    """

    def __init__(self) -> None:
        """Created Pepper Process Model object.
        """
        self.model_data = pd.DataFrame()
        self.id = uuid.uuid1().clock_seq_low

    def set_process_model(self, p_data: pd.DataFrame) -> None:
        """Input Process Model data.

        Parameters
        ----------
        p_data : pd.DataFrame
            DataFrame with 'activity' and 'sorting' columns.

        Example
        -------
        >>> data = {'activity': ['register request', 'check ticket', 'examine casually', 'decide', 'pay compensation'],
                    'sorting': [1, 2, 3, 4, 5]}
        >>> df = pd.DataFrame(data, columns=['activity', 'sorting'])
        >>> md = ProcessModel()
        >>> md.set_process_model(df)
        >>> md.get_process_model()
        """
        self.model_data = self.__validate_process_model(p_data)

    def get_process_model(self) -> pd.DataFrame:
        """Return Process Model data.

        Returns
        -------
        DataFrame
            DataFrame with the process model data.
        """
        return self.model_data

    def read_process_model_csv(self, file_path: str, separator: Optional[str] = ';') -> None:
        """Import the CSV to process model data.

        Import the CSV into a pandas DataFrame.
        Convert the CSV into an process model Pandas DataFrame.
        The first step is to import the CSV file and internal API validate and convert it to the process model.
        See more infomation in the pandas documentation.

        Parameters
        ----------
        file_path : str
            Any valid string path is acceptable.
        separator : str
            Delimiter used in CSV file.

        Example
        -------
        >>> md = ProcessModel()
        >>> md.read_process_model_csv("tests/data/processmodel-example.csv", separator=';')
        >>> md.get_process_model()

        See Also
        --------
        https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html?highlight=read_csv#

        """
        df = pd.read_csv(file_path, sep=separator)
        self.set_process_model(df)

    def clear_datas(self) -> None:
        """Clear Process Model.

        Remove all rows and columns.
        After this method is possible include a new Process Model to the object.

        """
        self.model_data = pd.DataFrame()

    def __validate_process_model(self, p_df: pd.DataFrame) -> pd.DataFrame:
        """Validate Process Model.

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
            (1) Only Pandas DataFrame are allowed in Process Model.
            (2) Has Process Model. It needs clear the datas.
            (3) Not exists the column activity, the column activity is mandatory.
            (4) Not exists the column sorting, the column sorting is mandatory.
        """
        if not (isinstance(p_df, pd.DataFrame)):
            raise TypeError("Only Pandas DataFrame are allowed in Process Model.")
        if not (self.model_data.empty):
            raise TypeError("Has event logs data. It needs clear the event logs. e.g. Use the method clear_datas.")
        if not (ModelColumn.ACTIVITY.value in p_df.columns):
            raise TypeError(f"Not exists the column {ModelColumn.ACTIVITY.value}, the column {ModelColumn.ACTIVITY.value} is mandatory.")
        if not (ModelColumn.SORTING.value in p_df.columns):
            raise TypeError(f"Not exists the column {ModelColumn.SORTING.value}, the column {ModelColumn.SORTING.value} is mandatory.")
        # Add ID in ProcessModel
        p_df[ModelColumn.ID.value] = self.id
        return p_df
