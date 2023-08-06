from typing import Dict, Sequence, Union

class ColumnSummary:
    nbr_of_modification: int

class Summary:
    columns_summary: Dict[str, ColumnSummary]

class Reconciliation:
    def __init__(
        self,
        headers: Sequence[str],
        dataset_1: Sequence[Sequence[Union[int, float, str]]],
        dataset_2: Sequence[Sequence[Union[int, float, str]]],
        key: str,
    ) -> None: ...
    def summarise(self) -> Summary: ...
