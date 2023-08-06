import refinitiv.data as rd

IPA_ITEMS = [
    rd.content.ipa.curves.forward_curves.Definition,
    rd.content.ipa.dates_and_calendars.add_periods.Definition,
    rd.content.ipa.dates_and_calendars.count_periods.Definition,
    rd.content.ipa.dates_and_calendars.date_schedule.Definition,
    rd.content.ipa.dates_and_calendars.holidays.Definition,
    rd.content.ipa.dates_and_calendars.is_working_day.Definition,
    rd.content.ipa.financial_contracts.bond.Definition,
    rd.content.ipa.financial_contracts.cap_floor.Definition,
    rd.content.ipa.financial_contracts.cds.Definition,
    rd.content.ipa.financial_contracts.cross.Definition,
    rd.content.ipa.financial_contracts.option.Definition,
    rd.content.ipa.financial_contracts.repo.Definition,
    rd.content.ipa.financial_contracts.swap.Definition,
    rd.content.ipa.financial_contracts.swaption.Definition,
    rd.content.ipa.financial_contracts.term_deposit.Definition,
]


def test_ipa_creation_without_arguments():
    for definition in IPA_ITEMS:
        assert definition()
