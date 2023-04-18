from typing import Union, Optional

from peppermining.filters.pepper_filter import PepperFilter
from peppermining.peppermining import PepperMining
from peppermining.utils.enum import EventColumn, Variant


class VariantFilter(PepperFilter):
    """ Variant Filter.

    The variant filter keeps only the variants included in a list.

    Methods
    -------
    get_filter
        Return the filters apply in the object.

    Example
    -------
    >>> pm = PepperMining()
    >>> pm.read_event_log_csv("tests/data/eventlog-example.csv", separator=';', format_date='%d/%m/%Y %H:%M')
    >>> pm.read_cases_csv("tests/data/case-example.csv", separator=';')
    >>> var = PepperVariant(pm)
    >>> variant_list = list(var.get_variants().iloc[0:2]['key'])
    >>> f1 = VariantFilter(var, variant_list)
    >>> f1.get_event_log()
    >>> variant_list = list(var.get_variants().iloc[0:1]['key'])
    >>> f2 = VariantFilter(f1, variant_list, "not contain")
    >>> f2.get_event_log()
    >>> f2.get_filter()
    """

    def __init__(self, data: Union[PepperMining, PepperFilter], variant_list: str, mode: Optional[str] = 'contain'):
        """Filters the event log that keeps only the cases included in case list.

        Parameters
        ----------
        data: Union[PepperMining, PepperFilter]
            PepperMining or PepperFilter object.
        variant_list: str
            List of variants key that gonna filter.
        mode: str, Default: contain
            Modality of filtering (contain, not contain).
        """
        super().__init__(data)
        self._mode = mode
        self.variant_list = variant_list
        # Data preparation
        variants = self._component.get_variants().copy()
        self.variant = variants[(variants[Variant.KEY.value].isin(variant_list), ~variants[Variant.KEY.value].isin(variant_list))[self._mode == 'not contain']]
        variants = variants.explode(Variant.CASES.value).reset_index(drop=True).rename(columns={Variant.CASES.value: EventColumn.CASE_ID.value})[[Variant.KEY.value, EventColumn.CASE_ID.value]]
        # Filter event and case data by Variant
        case_list = list(variants[variants[Variant.KEY.value].isin(variant_list)][EventColumn.CASE_ID.value])
        self.set_event_data_by_case_list(case_list)
        self.set_case_data_by_case_list(case_list)

    def get_filter(self) -> str:
        """Return the filters apply in the object.

        Returns
        -------
        String
            String with list the filters.
        """
        return f"{self.component.get_filter()} [Filter by variant {('', 'not')[self._mode == 'not contain']}({len(self.variant_list)} variants)]"
