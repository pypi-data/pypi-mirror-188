import pytest

from reconcile_core import Reconciliation, Summary


def test_can_create_simple_diff_list():
    reconciliation = Reconciliation(
        headers=["a", "b", "c"],
        dataset_1=[[1, 89.90, "before"]],
        dataset_2=[[1, 89.90, "after"]],
        key="a",
    )

    summary: Summary = reconciliation.summarise()

    assert summary.columns_summary["b"].nbr_of_modification == 0
    assert summary.columns_summary["c"].nbr_of_modification == 1


def test_can_create_simple_diff_tuple():
    reconciliation = Reconciliation(
        headers=["a", "b", "c"],
        dataset_1=[(1, 89.90, "before")],
        dataset_2=[(1, 89.90, "after")],
        key="a",
    )

    summary: Summary = reconciliation.summarise()

    assert summary.columns_summary["b"].nbr_of_modification == 0
    assert summary.columns_summary["c"].nbr_of_modification == 1


def test_raise_exception_on_unhandle_type():
    class Dummy:
        ...

    with pytest.raises(TypeError):
        Reconciliation(
            headers=["a"],
            dataset_1=[(Dummy())],
            dataset_2=[],
            key="a",
        )
