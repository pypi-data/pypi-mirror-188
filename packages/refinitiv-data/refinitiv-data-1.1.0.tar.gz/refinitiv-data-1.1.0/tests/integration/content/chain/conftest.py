from datetime import datetime
import refinitiv.data as rd
import tests.integration.conftest as global_conftest


def open_desktop_session_for_streaming_chain():
    return rd.open_session(config_name=global_conftest.conf, name="desktop.my-session")


def open_deployed_session_for_streaming_chain():
    return rd.open_session(
        config_name=global_conftest.conf, name="platform.deployed-cipsnylab2"
    )


def display_add(index, constituent, streaming_chain, triggered_events_list=None):
    if triggered_events_list is not None:
        triggered_events_list.append("Add performed")
    current_time = datetime.now().time()
    print(
        f"{current_time} - Add received for {streaming_chain.name}: {index} - {constituent}"
    )


def display_remove(index, constituent, streaming_chain, triggered_events_list=None):
    if triggered_events_list is not None:
        triggered_events_list.append("Remove performed")
    current_time = datetime.now().time()
    print(
        f"{current_time} - Remove received for {streaming_chain.name}: {index} - {constituent}"
    )


def display_update(
    index, old_constituent, new_constituent, streaming_chain, triggered_events_list=None
):
    if triggered_events_list is not None:
        triggered_events_list.append("Update performed")
    current_time = datetime.now().time()
    print(
        f"{current_time} - Update received for {streaming_chain.name}: "
        f"{index} - {old_constituent} to {new_constituent}"
    )


def display_complete_decoded(constituents, streaming_chain, triggered_events_list=None):
    if triggered_events_list is not None:
        triggered_events_list.append("Complete performed")
    current_time = datetime.now().time()
    print(
        f"{current_time} - StreamingChain {streaming_chain.name} is complete decoded."
        f" - constituents = {constituents}"
    )


def display_error(error, index, streaming_chain, triggered_events_list=None):
    if triggered_events_list is not None:
        triggered_events_list.append("Error received")
    current_time = datetime.now().time()
    print(f"{current_time} - Error received for Chain: {error}")


def create_chain_stream(name):
    chain = rd.content.pricing.chain.Definition(name)
    stream = chain.get_stream()
    stream.on_error(
        lambda streaming_chain, index, error: display_error(
            streaming_chain, index, error
        )
    )
    return stream


def create_chain_stream_with_callbacks(name, triggered_events, service=None):
    definition = rd.content.pricing.chain.Definition(name, service=service)
    stream = definition.get_stream()
    stream.on_add(
        lambda index, constituent, streaming_chain: display_add(
            index, constituent, streaming_chain, triggered_events
        )
    )
    stream.on_remove(
        lambda index, constituent, streaming_chain: display_remove(
            index, constituent, streaming_chain, triggered_events
        )
    )
    stream.on_update(
        lambda index, old_constituent, new_constituent, streaming_chain: display_update(
            index,
            old_constituent,
            not new_constituent,
            streaming_chain,
            triggered_events,
        )
    )
    stream.on_complete(
        lambda constituents, streaming_chain: display_complete_decoded(
            constituents, streaming_chain, triggered_events
        )
    )
    stream.on_error(
        lambda error, index, streaming_chain: display_error(
            error, index, streaming_chain, triggered_events
        )
    )
    return stream
