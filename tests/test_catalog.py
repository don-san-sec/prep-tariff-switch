from datetime import date

import pytest

from tariffs.catalog import Catalog
from tariffs.models import Tariff, TariffKind


def fixed_12m() -> Tariff:
    return Tariff(
        "tariff_fixed12",
        TariffKind.FIXED,
        "Fixed 12M",
        10_500,
        2_500,
        date(2027, 5, 31),
    )


def test_add_then_get_returns_the_tariff() -> None:
    catalog = Catalog()
    tariff = fixed_12m()
    catalog.add(tariff)

    assert catalog.get("tariff_fixed12") is tariff


def test_list_returns_every_tariff() -> None:
    catalog = Catalog()
    catalog.add(fixed_12m())
    catalog.add(Tariff("tariff_flex", TariffKind.VARIABLE, "Flex Variable", 9_800))

    assert [t.tariff_id for t in catalog.list()] == ["tariff_fixed12", "tariff_flex"]


def test_get_unknown_tariff_id_raises() -> None:
    catalog = Catalog()

    with pytest.raises(KeyError):
        catalog.get("tariff_nope")
