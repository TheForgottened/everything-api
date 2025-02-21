def query_params_01() -> list[tuple[str, str]]:
    return [("userHeightCm", "180"), ("userHeightCm", "170"), ("userHeightCm", "160"), ("userStatus", "Available")]


def query_params_02() -> list[tuple[str, str]]:
    return [("status", "error"), ("status", "in_queue"), ("status", "success")]


def query_params_03() -> list[tuple[str, str]]:
    return [("isAvailable", "true")]
