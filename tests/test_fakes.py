from fakes import FakeNotifier


def test_send_records_customer_template_and_context() -> None:
    notifier = FakeNotifier()

    notifier.send(
        "cus_0001",
        "tariff_switch_confirmation",
        new_tariff="Flex Variable",
        exit_fee_pence=2_500,
    )

    assert len(notifier.sent) == 1
    sent = notifier.sent[0]
    assert sent.customer_id == "cus_0001"
    assert sent.template == "tariff_switch_confirmation"
    assert sent.context == {"new_tariff": "Flex Variable", "exit_fee_pence": 2_500}


def test_each_send_is_recorded_separately() -> None:
    notifier = FakeNotifier()

    notifier.send("cus_0001", "tariff_switch_confirmation", exit_fee_pence=0)
    notifier.send("cus_0002", "tariff_switch_confirmation", exit_fee_pence=2_500)

    assert [(s.customer_id, s.context) for s in notifier.sent] == [
        ("cus_0001", {"exit_fee_pence": 0}),
        ("cus_0002", {"exit_fee_pence": 2_500}),
    ]
