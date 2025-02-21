from itertools import groupby
from typing import Any


def map_query_params_list_to_dict(query_params: list[tuple[str, str]]) -> dict[str, list[str]]:
    def key_func(x: tuple) -> Any:
        return x[0]

    sorted_query_params = sorted(query_params, key=key_func)
    return {
        query_param: list(map(lambda x: x[1], values))
        for query_param, values in groupby(sorted_query_params, key=key_func)
    }
