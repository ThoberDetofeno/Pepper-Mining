import numpy as np
import pandas as pd
import pydot

from typing import Optional
from datetime import timedelta

from peppermining.utils.enum import EventColumn, Variant, Flowchart
from peppermining.kpi.pepper_kpi import PepperKpi
# TODO: Call the KPIs class of a dynamically imported module (__kpi)
from peppermining.kpi.number_of_cases import NumberOfCases
from peppermining.kpi.throughput_time import ThroughputTime
from peppermining.kpi.average_events_per_case import AverageEventsPerCase
from peppermining.kpi.number_of_events import NumberOfEvents
from peppermining.kpi.number_of_activities import NumberOfActivities
from peppermining.kpi.rework import Rework


class Pepper():
    """The Pepper class declares common operations for both PepperMining and the PepperFilter.

    As long as the client works with PepperMining using this class, you'll be able to pass it a proxy instead of a real subject.

    Attributes
    ----------
    event_data: pd.DataFrame
        Event logs data.
    case_data : pd.DataFrame
        Cases data.
    activity_data : pd.DataFrame
        Activities data.
    variant_data : pd.DataFrame
        Variants data.

    Methods
    -------
    get_event_log
        Return Event logs data.
    get_cases
        Return Cases data.
    get_activities
        Return Activities data.
    get_summary
        Return summary the events and cases.
    get_variants
        Return Variants data.
    get_filter
        Return the filter used.
    drawing
        Return the activity interaction graph of event data.
    """

    def __init__(self):
        """Constructor.
        """
        self.event_data = pd.DataFrame()
        self.case_data = pd.DataFrame()
        self.activity_data = pd.DataFrame()
        self.variant_data = pd.DataFrame()

    def get_event_log(self) -> pd.DataFrame:
        """Return Event Logs data.

        Returns
        -------
        DataFrame
            DataFrame with the event logs data.
        """
        return self.event_data

    def get_cases(self, kpi: Optional[list] = None) -> pd.DataFrame:
        """Return Cases data.

        Return the cases with metrics defined in the KPI module.

        Parameters
        ----------
        kpi : list(str)
            The a KPIs list. Choose the KPIs allow for the case data.
            kpi = ['NumberOfEvents', 'NumberOfActivities', 'ThroughputTime', 'Rework']

        Returns
        -------
        DataFrame
            DataFrame with the Cases data.
        """
        return self.case_data if kpi is None else self.__add_case_kpi(kpi)

    def get_activities(self, kpi: Optional[list] = None) -> pd.DataFrame:
        """Return Activities data.

        Return the activities with metrics defined in the KPI module.

        Parameters
        ----------
        kpi : list(str)
            The a KPIs list. Choose the KPIs allow for the activities data.
            kpi = ['NumberOfEvents', 'NumberOfCases', 'ThroughputTime', 'Rework']

        Returns
        -------
        DataFrame
            DataFrame with the Activities data.
        """
        if self.activity_data.empty:
            self.activity_data = self.get_event_log()[EventColumn.ACTIVITY.value].drop_duplicates().reset_index(drop=True).to_frame()
        return self.activity_data if kpi is None else self.__add_activity_kpi(kpi)

    def get_summary(self, kpi: Optional[list] = ['NumberOfEvents']) -> pd.DataFrame:
        """Return summary the events and cases.

        Parameters
        ----------
        kpi : list(str)
            The a KPIs list. Choose the KPIs allow for the summary.
            kpi = ['NumberOfEvents', 'NumberOfActivities', 'NumberOfCases', 'AverageEventsPerCase', 'ThroughputTime', 'Rework']

        Returns
        -------
        DataFrame
            DataFrame with the summary data.
        """
        return self.__add_kpi(kpi)

    def get_variants(self, kpi: Optional[list] = None) -> pd.DataFrame:
        """Return Variants data.

        Parameters
        ----------
        kpi: list(str)
            The a KPIs list. Choose the KPIs allow for the variants.
            kpi = ['NumberOfEvents', 'NumberOfActivities', 'NumberOfCases', 'ThroughputTime']

        Returns
        -------
        DataFrame
            DataFrame with the Variants data.
        """
        if self.variant_data.empty:
            self.variant_data = self.__set_variants()
        return self.variant_data if kpi is None else self.__add_variant_kpi(kpi)

    def get_filter(self) -> str:
        """Return the filter used.

        Returns
        -------
        String
            String with list the filters.
        """
        return "[None]"

    def drawing(self, label_kpi: Optional[str] = 'NumberOfCases') -> pydot.Dot:
        """Return the activity interaction graph of event data.

        Parameters
        ----------
        label_kpi : Optional[str]
                Choose a KPI allow for is showing in the edge.
                Options: NumberOfCases | ThroughputTimeMin | ThroughputTimeMax | ThroughputTimeMean | ThroughputTimeMedian | ThroughputTimeSum | ThroughputTimeStDev
                        'NumberOfCases' = Number of cases
                        'ThroughputTimeMin' = Throughput time (Min)
                        'ThroughputTimeMax' = Throughput time (Max)
                        'ThroughputTimeMean' = Throughput time (Mean)
                        'ThroughputTimeMedian' = Throughput time (Median)
                        'ThroughputTimeSum' = Throughput time (Sum)
                        'ThroughputTimeStDev' = Throughput time (StDev)
        Returns
        -------
        pydot.Dot
            Return a graph using pydot objects.
            The pydot package is an interface to Graphviz.

        Example
        -------
        >>> pm = PepperMining()
        >>> pm.read_event_log_csv("c:/Temp/base-peppermining/peppermining/tests/data/eventlog-example.csv", separator=';',
                                  format_date='%d/%m/%Y %H:%M')
        >>> pm.read_cases_csv("c:/Temp/base-peppermining/peppermining/tests/data/case-example.csv", separator=';')
        >>> pm.get_cases()
        >>> graph = pm.drawing()
        >>> graph.write_png('output.png')

        See Also
        --------
        https://pypi.org/project/pydot/
        """
        def edge_label(activity_from: str, activity_to: str) -> str:
            """Return edge label.
            """
            if label_kpi == 'NumberOfCases':
                kpi_number_of_cases = NumberOfCases(self)
                kpi_edge = kpi_number_of_cases.get_kpi_process_flow(activity_from, activity_to)
                return str(kpi_edge.Value.values[0])
            # Verify if exists the activities
            if not (activity_from in list(self.get_activities()[EventColumn.ACTIVITY.value])) or not (activity_to in list(self.get_activities()[EventColumn.ACTIVITY.value])):
                return ""
            # Take the throughput time
            kpi_throughput_time = ThroughputTime(self)
            kpi_edge = kpi_throughput_time.get_kpi_process_flow(activity_from, activity_to)
            throughput_time = kpi_edge.filter(items=[label_kpi], axis=0).Value.values[0]
            return str(timedelta(seconds=throughput_time))

        # Extract variant data
        graph_data = self.get_variants().copy()
        # Transform variant data
        graph_data = graph_data.explode(Variant.ACTIVITIES.value).reset_index(drop=True).rename(columns={Variant.ACTIVITIES.value: Flowchart.ACTIVITY.value})
        # CREATE GRAPH
        graph = pydot.Dot('pepper_graph', graph_type='digraph', bgcolor='white', directed=True, rankdir='LR')
        # ADD NODE
        # Add activities in flowchart in 3 steps. For the activity ever is NumberOfCases in box.
        # Step 1. Add START activity
        kpi_node = NumberOfCases(self)
        graph.add_node(pydot.Node(Flowchart.PROCESS_START.value,
                                  label=Flowchart.PROCESS_START.value + '(' + str(kpi_node.get_kpi().Value.values[0]) + ')',
                                  shape=Flowchart.START_SHAPE.value))
        # Step 2. Add activities
        activities = graph_data.drop_duplicates(subset=[Flowchart.ACTIVITY.value])
        for index, act in activities.iterrows():
            value = act[Flowchart.ACTIVITY.value]
            graph.add_node(pydot.Node(value,
                                      label=value + '(' + str(kpi_node.get_kpi_activities().query("activity == @value").NumberOfCases.values[0]) + ')',
                                      shape=Flowchart.ACTIVITY_SHAPE.value))
        # Step 3. Add END activity
        graph.add_node(pydot.Node(Flowchart.PROCESS_END.value,
                                  label=Flowchart.PROCESS_END.value + '(' + str(kpi_node.get_kpi().Value.values[0]) + ')',
                                  shape=Flowchart.END_SHAPE.value))
        # ADD EDGE
        # Add connections in flowchart in 3 steps
        # Step 1. Add START edge
        graph_data[Flowchart.ACTIVITY_FROM.value] = graph_data.groupby(Variant.KEY.value)[Flowchart.ACTIVITY.value].shift(1).replace(np.nan, Flowchart.PROCESS_START.value)
        conn_start = graph_data[graph_data[Flowchart.ACTIVITY_FROM.value] == Flowchart.PROCESS_START.value].drop_duplicates(subset=[Flowchart.ACTIVITY.value])[[Flowchart.ACTIVITY.value]]
        for index, edge in conn_start.iterrows():
            graph.add_edge(pydot.Edge(Flowchart.PROCESS_START.value,
                                      edge[Flowchart.ACTIVITY.value],
                                      label=edge_label(Flowchart.PROCESS_START.value, edge[Flowchart.ACTIVITY.value]),
                                      penwidth=Flowchart.EDGE_PENWIDTH.value,
                                      id=Flowchart.PROCESS_START.value + '->' + edge[Flowchart.ACTIVITY.value],
                                      color=Flowchart.EDGE_COLOR.value,
                                      arrowhead=Flowchart.EDGE_ARROWHEAD.value,
                                      arrowsize=Flowchart.EDGE_ARROWSIZE.value))
        # Step 2. Add edge
        connection = graph_data[graph_data[Flowchart.ACTIVITY_FROM.value] != Flowchart.PROCESS_START.value].drop_duplicates(subset=[Flowchart.ACTIVITY_FROM.value, Flowchart.ACTIVITY.value])
        for index, edge in connection.iterrows():
            graph.add_edge(pydot.Edge(edge[Flowchart.ACTIVITY_FROM.value],
                                      edge[Flowchart.ACTIVITY.value],
                                      label=edge_label(edge[Flowchart.ACTIVITY_FROM.value], edge[Flowchart.ACTIVITY.value]),
                                      penwidth=Flowchart.EDGE_PENWIDTH.value,
                                      id=edge[Flowchart.ACTIVITY_FROM.value] + '->' + edge[Flowchart.ACTIVITY.value],
                                      color=Flowchart.EDGE_COLOR.value,
                                      arrowhead=Flowchart.EDGE_ARROWHEAD.value,
                                      arrowsize=Flowchart.EDGE_ARROWSIZE.value))
        # Step 3. Add END edge
        graph_data[Flowchart.ACTIVITY_TO.value] = graph_data.groupby(Variant.KEY.value)[Flowchart.ACTIVITY.value].shift(-1).replace(np.nan, Flowchart.PROCESS_END.value)
        conn_end = graph_data[graph_data[Flowchart.ACTIVITY_TO.value] == Flowchart.PROCESS_END.value].drop_duplicates(subset=[Flowchart.ACTIVITY.value])[[Flowchart.ACTIVITY.value]]
        for index, edge in conn_end.iterrows():
            graph.add_edge(pydot.Edge(edge[Flowchart.ACTIVITY.value],
                                      Flowchart.PROCESS_END.value,
                                      label=edge_label(edge[Flowchart.ACTIVITY.value], Flowchart.PROCESS_END.value),
                                      penwidth=Flowchart.EDGE_PENWIDTH.value,
                                      id=Flowchart.PROCESS_END.value + '->' + edge[Flowchart.ACTIVITY.value],
                                      color=Flowchart.EDGE_COLOR.value,
                                      arrowhead=Flowchart.EDGE_ARROWHEAD.value,
                                      arrowsize=Flowchart.EDGE_ARROWSIZE.value))
        return graph

    def __add_kpi(self, kpi_list: list) -> pd.DataFrame:
        """Add KPI value in the summary

        Parameters
        ----------
        kpi_list : list(str)
            The a KPIs list.
        Returns
        -------
        DataFrame
            DataFrame with the KPI values.
        """
        try:
            dfsummary = pd.DataFrame()
            for kpi_id in kpi_list:
                df_kpi = self.__kpi(kpi_id).get_kpi()
                dfsummary = pd.concat([df_kpi, dfsummary.loc[:]])
            return dfsummary
        except Exception as e:
            raise TypeError(f'Only Pepper KPI are allowed.[{type(e)}]')

    def __add_case_kpi(self, kpi_list) -> pd.DataFrame:
        """Add KPI value in the cases

        Parameters
        ----------
        kpi_list : list(str)
            The a KPIs list.
        Returns
        -------
        DataFrame
            DataFrame with the cases data and KPI values.
        """
        try:
            dfcase = self.case_data
            for kpi_id in kpi_list:
                df_kpi = self.__kpi(kpi_id).get_kpi_cases()
                dfcase = dfcase.merge(df_kpi, how='left', on=EventColumn.CASE_ID.value).replace(np.nan, None)
            return dfcase
        except Exception as e:
            raise TypeError(f'Only Pepper KPI are allowed.[{type(e)}]')

    def __add_activity_kpi(self, kpi_list) -> pd.DataFrame:
        """Add KPI value in the activities

        Parameters
        ----------
        kpi_list : list(str)
            The a KPIs list.
        Returns
        -------
        DataFrame
            DataFrame with the activities data and KPI values.
        """
        try:
            dfactivity = self.activity_data
            for kpi_id in kpi_list:
                df_kpi = self.__kpi(kpi_id).get_kpi_activities()
                dfactivity = dfactivity.merge(df_kpi, how='left', on=EventColumn.ACTIVITY.value).replace(np.nan, None)
            return dfactivity
        except Exception as e:
            raise TypeError(f'Only Pepper KPI are allowed.[{type(e)}]')

    def __add_variant_kpi(self, kpi_list) -> pd.DataFrame:
        """Add KPI value in the variants

        Parameters
        ----------
        kpi_list : list(str)
            The a KPIs list.
        Returns
        -------
        DataFrame
            DataFrame with the Variants data and KPI values.
        """
        try:
            dfvariant = self.variant_data
            for kpi_id in kpi_list:
                df_kpi = self.__kpi(kpi_id).get_kpi_variants()
                dfvariant = dfvariant.merge(df_kpi, how='left', on=Variant.KEY.value).replace(np.nan, None)
            return dfvariant
        except Exception as e:
            raise TypeError(f'Only Pepper KPI are allowed.[{type(e)}]')

    def __set_variants(self) -> pd.DataFrame:
        """Discovery all variants of a event logs.

        Returns
        -------
        DataFrame
            DataFrame with the Variants data.
        """
        var = self.get_event_log()[[EventColumn.CASE_ID.value, EventColumn.ACTIVITY.value, EventColumn.EVENT_TIME.value]]
        # Create a key for each variant
        var = var.sort_values(EventColumn.EVENT_TIME.value).groupby(EventColumn.CASE_ID.value)[EventColumn.ACTIVITY.value].apply(lambda var: var.reset_index(drop=True)).unstack()
        var = var.replace(np.nan, None)
        var[Variant.KEY.value] = var[var.columns].apply(lambda row: Variant.SPLIT_SEP.value.join(row.values.astype(str)), axis=1).str.replace(str(Variant.SPLIT_SEP.value + 'None'), '')
        # Variant Discovery
        variant = var[Variant.KEY.value].reset_index().groupby(Variant.KEY.value)[EventColumn.CASE_ID.value].apply(list).reset_index().rename(columns={EventColumn.CASE_ID.value: Variant.CASES.value})
        # Add Activities for each Variant
        variant[Variant.ACTIVITIES.value] = variant[Variant.KEY.value].str.split(Variant.SPLIT_SEP.value)
        # Add Cases for each Variant
        variant[Variant.KEY.value] = variant[Variant.KEY.value].str.replace(Variant.SPLIT_SEP.value, Variant.ACT_CONN.value)
        #
        return variant

    def __kpi(self, kpi_id: str) -> PepperKpi:
        """ Return de object PepperKpi

        Parameters
        ----------
        kpi_id : str
            From a id kpi return the object.
            kpi_id = 'NumberOfCases'

        Returns
        -------
        PepperKpi
            PepperKpi object.
        """
        kpi = globals()[kpi_id]
        return kpi(self)
