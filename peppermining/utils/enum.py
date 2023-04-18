from enum import Enum


class EventColumn(Enum):
    """Event Logs standard columns
    """
    CASE_ID = 'case_id'
    ACTIVITY = 'activity'
    EVENT_TIME = 'event_time'
    USER = 'user'


class KpiColumn(Enum):
    """KPIs standard columns
    """
    KPI = 'KPI'
    VALUE = 'Value'


class Variant(Enum):
    """Variant starndard columns
    """
    KEY = 'key'
    ACTIVITIES = 'activities'
    CASES = 'cases'
    SPLIT_SEP = '#%pm%#'
    ACT_CONN = '->'


class Flowchart(Enum):
    """Parameters to create the process graph
    """
    PROCESS_START = 'Start'
    PROCESS_END = 'End'
    START_SHAPE = 'rect'
    END_SHAPE = 'rect'
    ACTIVITY_SHAPE = 'circle'
    ACTIVITY = 'activity'
    ACTIVITY_FROM = 'activity_from'
    ACTIVITY_TO = 'activity_to'
    EDGE_COLOR = 'black'
    EDGE_ARROWHEAD = 'normal'
    EDGE_ARROWSIZE = '1'
    EDGE_PENWIDTH = 2


class ModelColumn(Enum):
    """Process Model standard columns
    """
    ID = 'id'
    ACTIVITY = 'activity'
    SORTING = 'sorting'


class ViolationColumn(Enum):
    """Violation standard columns
    """
    TYPE = 'type'
    NAME = 'name'
    ACTIVITY = 'activity'
    CASES = 'cases'
