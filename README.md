# Tariff switching

Customers switch tariff in the Brightwatt Energy app: moving from the
variable tariff to a fixed deal, or from one fixed deal to another.

## Context

Brightwatt Energy is an app-first UK domestic energy supplier. About 180,000
customers pay a monthly bill. The billing period is the calendar month, and
every amount is stored in whole pence.

Each customer is on one tariff at a time. Electricity and gas are separate
fuels, and a customer can be on a tariff for one fuel or both (a "dual-fuel"
customer).

The ticket for this work is TARF-31:

> "Let customers switch tariff in the app."

## The product handbook's switching rules

These come from the product team's switching policy. The switch flow in the
app must match them exactly, or switches land mid-billing-period and the
monthly billing run breaks.

1. A switch records the customer moving from their current tariff to the new
   tariff.
2. **Effective date.** If the customer is **in contract** on a fixed tariff,
   the switch takes effect at the **start of the next billing period** — the
   1st of the next month. If the customer is out of contract (their fixed
   contract has ended, or they are on a variable tariff), the switch takes
   effect **immediately** — the same day.
3. **Exit fees.** Leaving a fixed tariff **before its contract end date**
   incurs the tariff's `exit_fee_pence` **per fuel**. Electricity and gas are
   separate fuels, so a dual-fuel customer pays two fees.
4. The exit fee is **waived** if the effective date is within 14 days of the
   contract end date (inclusive).
5. The customer must receive a **confirmation notification** stating the new
   tariff, the effective date, and any exit fee.
6. Switching to the tariff the customer is **already on** is rejected.

Worked examples from the handbook:

- A customer in contract on a fixed tariff ending 2027-05-31 switches on
  2027-03-04: the switch takes effect on **2027-04-01**, and the exit fee is
  due (per fuel).
- The same contract, with a switch effective **2027-05-20** — within 14 days
  of the contract end: the exit fee is **waived**.

## How it works

```
src/tariffs/
  models.py           Tariff, CustomerTariff; fuels and tariff kinds
  catalog.py          the in-memory tariff catalog: add / list / get
  notifications.py    the Notifier interface the app uses to reach customers
tests/
  fakes.py            FakeNotifier for tests
```

Switching itself isn't implemented yet. The app (not part of this service)
shows the catalog and collects the customer's choice; this service owns the
tariff models, the catalog, and — once TARF-31 lands — the switch.

## Running locally

```
uv sync
uv run pytest -q
```

## Your task

A colleague has opened a PR: https://github.com/don-san-sec/prep-tariff-switch/pull/1. You are the owner of this feature. Review the PR and decide whether to accept or reject it, and explain why.
