from datetime import datetime

from refinitiv.data.content import trade_data_service


def display_event(event, stream, event_type, triggered_events_list=None):
    current_time = datetime.now().time()
    if triggered_events_list is not None:
        triggered_events_list.append(event_type)
    print("----------------------------------------------------------")
    print(">>> {} event received at {}".format(event_type, current_time))
    print(event)


def display_event_complete(item_stream, triggered_events_list=None):
    current_time = datetime.now().time()
    if triggered_events_list is not None:
        triggered_events_list.append("Complete")
    print("----------------------------------------------------------")
    print(">>> {} event received at {}".format("Complete", current_time))


def create_trade_data_service_with_all_callbacks(
    universe=None,
    api=None,
    fields=None,
    universe_type=trade_data_service.UniverseTypes.UserID,
    extended_params=None,
    triggered_events_list=None,
    session=None,
):
    trade_data_service_stream = (
        trade_data_service.Definition(
            universe=universe,
            api=api,
            fields=fields,
            finalized_orders=trade_data_service.FinalizedOrders.P1D,
            events=trade_data_service.Events.Full,
            universe_type=universe_type,
            extended_params=extended_params,
        )
        .get_stream(session=session)
        .on_update(
            lambda event, stream: display_event(event, "Update", triggered_events_list)
        )
        .on_add(
            lambda event, item_stream: display_event(
                event, item_stream, "Add", triggered_events_list
            )
        )
        .on_state(
            lambda event, item_stream: display_event(
                event, item_stream, "State", triggered_events_list
            )
        )
        .on_complete(
            lambda item_stream: display_event_complete(
                item_stream, triggered_events_list
            )
        )
    )

    return trade_data_service_stream


def check_triggered_event_list(triggered_events_list):
    expected_events_list = [
        "Complete",
        "State",
    ]
    for event in expected_events_list:
        assert (
            event in triggered_events_list
        ), f"found event '{triggered_events_list}' not handled by handlers or not triggered"
