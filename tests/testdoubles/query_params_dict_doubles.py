def query_params_dict_01() -> dict[str, list[str]]:
    return {"userHeightCm": ["180", "170", "160"], "userStatus": ["Available"]}


def query_params_dict_02() -> dict[str, list[str]]:
    return {"status": ["error", "in_queue", "success"]}


def query_params_dict_03() -> dict[str, list[str]]:
    return {"isAvailable": ["true"]}
