from datetime import date

import pytest

from fakes import FakeNotifier
from tariffs.catalog import Catalog
from tariffs.models import CustomerTariff, Fuel, Tariff, TariffKind
from tariffs.switching import (
    SWITCH_CONFIRMATION_TEMPLATE,
    SameTariffError,
    switch_tariff,
)


def make_catalog() -> Catalog:
    catalog = Catalog()
    catalog.add(
        Tariff(
            "tariff_fixed12",
            TariffKind.FIXED,
            "Fixed 12M",
            10_500,
            2_500,
            date(2027, 5, 31),
        )
    )
    catalog.add(Tariff("tariff_flex", TariffKind.VARIABLE, "Flex Variable", 9_800))
    return catalog


def elec_customer_on(tariff_id: str) -> CustomerTariff:
    return CustomerTariff("cus_0001", tariff_id, [Fuel.ELEC])


def test_in_contract_switch_takes_effect_same_day_and_charges_the_exit_fee() -> None:
    catalog = make_catalog()
    customer = elec_customer_on("tariff_fixed12")
    notifier = FakeNotifier()

    result = switch_tariff(
        catalog, customer, catalog.get("tariff_flex"), date(2027, 3, 4), notifier
    )

    assert result.effective_date == date(2027, 3, 4)
    assert result.exit_fee_pence == 2_500


def test_switch_sends_the_confirmation() -> None:
    catalog = make_catalog()
    customer = elec_customer_on("tariff_flex")
    notifier = FakeNotifier()

    switch_tariff(
        catalog, customer, catalog.get("tariff_fixed12"), date(2027, 3, 4), notifier
    )

    assert len(notifier.sent) == 1
    assert notifier.sent[0].customer_id == "cus_0001"
    assert notifier.sent[0].template == SWITCH_CONFIRMATION_TEMPLATE


def test_switching_to_the_tariff_already_on_is_rejected() -> None:
    catalog = make_catalog()
    customer = elec_customer_on("tariff_fixed12")
    notifier = FakeNotifier()

    with pytest.raises(SameTariffError):
        switch_tariff(
            catalog, customer, catalog.get("tariff_fixed12"), date(2027, 3, 4), notifier
        )


def test_switch_from_a_variable_tariff_charges_no_exit_fee() -> None:
    catalog = make_catalog()
    customer = elec_customer_on("tariff_flex")
    notifier = FakeNotifier()

    result = switch_tariff(
        catalog, customer, catalog.get("tariff_fixed12"), date(2027, 3, 4), notifier
    )

    assert result.effective_date == date(2027, 3, 4)
    assert result.exit_fee_pence == 0


def test_unknown_tariff_id_raises() -> None:
    catalog = make_catalog()
    customer = CustomerTariff("cus_0001", "tariff_retired", [Fuel.ELEC])
    notifier = FakeNotifier()

    with pytest.raises(KeyError):
        switch_tariff(
            catalog, customer, catalog.get("tariff_flex"), date(2027, 3, 4), notifier
        )
