from functools import reduce
import pandas as pd
from hestia_earth.schema import TermTermType
from hestia_earth.utils.model import find_primary_product
from hestia_earth.utils.tools import list_sum, list_average, flatten

INDEX_COLUMN = 'cycle.id'
YIELD_COLUMN = 'Grain yield (kg/ha)'
FERTILISER_COLUMNS = [
    'Nitrogen (kg N)',
    'Phosphorus (kg P2O5)',
    'Potash (kg K2O)',
    'Magnesium (kg Mg)'
    # 'Sulphur (kg S)'
]
FERTILISER_TERM_TYPES = [
    TermTermType.ORGANICFERTILISER.value,
    TermTermType.INORGANICFERTILISER.value
]


def get_input_group(input: dict):
    term_units = input.get('term', {}).get('units')
    return next((group for group in FERTILISER_COLUMNS if term_units in group), None)


def _group_inputs(inputs: list):
    def exec(group: dict, group_key: str):
        sum_inputs = list_sum(flatten([
            input.get('value', []) for input in inputs if get_input_group(input) == group_key
        ]), 0)
        return {**group, group_key: sum_inputs}
    return exec


def group_cycle_inputs(cycle: dict):
    yield_value = list_average(find_primary_product(cycle).get('value'))
    fertilisers = [
        i for i in cycle.get('inputs', []) if all([
            i.get('term', {}).get('termType') in FERTILISER_TERM_TYPES,
            list_sum(i.get('value', []), 0) > 0
        ])
    ]
    fertilisers_values = reduce(_group_inputs(fertilisers), FERTILISER_COLUMNS, {})
    return {
        INDEX_COLUMN: cycle['@id'],
        YIELD_COLUMN: yield_value,
        **fertilisers_values
    }


def cycle_yield_distribution(cycles: list):
    values = list(map(group_cycle_inputs, cycles))
    return pd.DataFrame.from_records(values, index=[INDEX_COLUMN])
