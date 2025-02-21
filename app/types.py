from typing import TypeAlias, TypeAliasType

JSONable: TypeAlias = TypeAliasType(
    "JSONable",
    dict[str, "JSONable"] | list["JSONable"] | str | int | float | bool | None,
)
