import pytest

from app.mappers import map_query_params_list_to_dict
from tests.testdoubles.query_params_dict_doubles import query_params_dict_01, query_params_dict_02, query_params_dict_03
from tests.testdoubles.query_params_doubles import query_params_01, query_params_02, query_params_03

pytestmark = pytest.mark.unit_test


@pytest.mark.parametrize(
    ("query_params", "expected_result"),
    [
        (query_params_01(), query_params_dict_01()),
        (query_params_02(), query_params_dict_02()),
        (query_params_03(), query_params_dict_03()),
    ],
)
def test_map_query_params_list_to_dict(query_params: list[tuple[str, str]], expected_result: dict[str, list[str]]):
    # When
    result = map_query_params_list_to_dict(query_params=query_params)

    # Then
    assert result == expected_result
