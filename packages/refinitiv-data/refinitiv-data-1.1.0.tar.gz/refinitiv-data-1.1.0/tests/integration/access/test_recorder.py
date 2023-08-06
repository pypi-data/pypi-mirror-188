import asyncio
import time

import allure
import pytest

from refinitiv.data import open_pricing_stream
from tests.integration.access.conftest import (
    check_stream_opened,
    check_stream_closed,
    check_stream_fields,
    check_df_recording_duration,
    check_df_recording_frequency,
    check_column_names_is_exist_in_response_and_df_not_empty,
    check_history_for_expected_amount_of_bars,
    is_universe_exist,
)
from tests.integration.helpers import (
    check_if_dataframe_is_not_none,
)


@allure.suite("FinCoder layer")
@allure.feature("FinCoder - Stream Recorder")
@allure.severity(allure.severity_level.CRITICAL)
class TestPricingStreamRecorder:
    @allure.title("Stream recording ohlc data with several universes and fields")
    @pytest.mark.parametrize(
        "universe,fields,expected_fields,frequency,duration,ticks_per_bar",
        [
            (
                ["EUR=", "GBP="],
                ["BID", "ASK"],
                [
                    ("EUR=", "ASK", "open"),
                    ("EUR=", "ASK", "high"),
                    ("EUR=", "ASK", "low"),
                    ("EUR=", "ASK", "close"),
                    ("EUR=", "BID", "open"),
                    ("EUR=", "BID", "high"),
                    ("EUR=", "BID", "low"),
                    ("EUR=", "BID", "close"),
                    ("GBP=", "ASK", "open"),
                    ("GBP=", "ASK", "high"),
                    ("GBP=", "ASK", "low"),
                    ("GBP=", "ASK", "close"),
                    ("GBP=", "BID", "open"),
                    ("GBP=", "BID", "high"),
                    ("GBP=", "BID", "low"),
                    ("GBP=", "BID", "close"),
                    ("ticks count", "", ""),
                ],
                "3s",
                "9s",
                "1",
            ),
            (
                ["GBP="],
                ["BID", "ASK"],
                [
                    ("GBP=", "ASK", "open"),
                    ("GBP=", "ASK", "high"),
                    ("GBP=", "ASK", "low"),
                    ("GBP=", "ASK", "close"),
                    ("GBP=", "BID", "open"),
                    ("GBP=", "BID", "high"),
                    ("GBP=", "BID", "low"),
                    ("GBP=", "BID", "close"),
                    ("ticks count", "", ""),
                ],
                "tick",
                "13s",
                "3",
            ),
        ],
    )
    @pytest.mark.caseid("39028006")
    def test_stream_recording_ohlc_data_with_several_universes_and_fields(
        self,
        open_desktop_session,
        universe,
        fields,
        expected_fields,
        frequency,
        duration,
        ticks_per_bar,
    ):
        stream = open_pricing_stream(universe, fields)

        check_stream_opened(stream)
        stream.recorder.record(
            frequency=frequency, duration=duration, ticks_per_bar=ticks_per_bar
        )

        history_response = stream.recorder.get_history()
        stream.close()
        check_stream_closed(stream)

        check_stream_fields(stream, universe[0], fields)
        check_column_names_is_exist_in_response_and_df_not_empty(
            history_response, expected_fields
        )
        check_if_dataframe_is_not_none(history_response)
        if ticks_per_bar != "1":
            dataframes = stream.recorder._ohlc_builder.dataframes
            for i in range(len(dataframes) - 1):
                assert len(dataframes[i]) == int(ticks_per_bar)
            assert len(dataframes[-1]) <= int(ticks_per_bar)

    @allure.title(
        "Recording a pricing stream updates with closed stream and get ConnectionError"
    )
    @pytest.mark.parametrize(
        "universe,fields,frequency,duration",
        [
            (
                ["EUR=", "GBP="],
                ["BID", "ASK"],
                "3s",
                "9s",
            )
        ],
    )
    @pytest.mark.caseid("40101747")
    def test_record_pricing_stream_updates_with_closed_stream(
        self, open_desktop_session, universe, fields, frequency, duration
    ):
        with pytest.raises(ConnectionError) as error:
            stream = open_pricing_stream(universe, fields)
            stream.close()
            stream.recorder.record(frequency=frequency, duration=duration)
        assert str(error.value) == "Stream is closed. Cannot record."

    @allure.title("Check if recorded history is empty after delete method was applied")
    @pytest.mark.parametrize(
        "universe,fields,frequency,duration",
        [
            (
                ["EUR=", "GBP="],
                ["BID", "ASK"],
                "2s",
                "6s",
            )
        ],
    )
    @pytest.mark.caseid("40101749")
    def test_check_if_history_is_empty_after_record_history_was_deleted(
        self, open_desktop_session, universe, fields, frequency, duration
    ):
        stream = open_pricing_stream(universe=universe, fields=fields)
        stream.recorder.record(frequency=frequency, duration=duration)
        history_response_01 = stream.recorder.get_history()
        check_history_for_expected_amount_of_bars(
            stream, history_response_01, frequency, duration
        )
        stream.recorder.delete()
        assert stream.recorder._ohlc_builder.ohlc_df is None

        stream.recorder.record(frequency=frequency, duration=duration)
        history_response_02 = stream.recorder.get_history()
        check_history_for_expected_amount_of_bars(
            stream, history_response_02, frequency, duration
        )
        stream.recorder.delete()
        assert stream.recorder._ohlc_builder.ohlc_df is None

        stream.recorder.record(frequency=frequency, duration=duration)
        history_response_03 = stream.recorder.get_history()
        check_history_for_expected_amount_of_bars(
            stream, history_response_03, frequency, duration
        )
        stream.recorder.delete()
        assert stream.recorder._ohlc_builder.ohlc_df is None

    @allure.title(
        "Recording a pricing stream ohlc data with few recorders and defined duration"
    )
    @pytest.mark.parametrize(
        "universe,fields,frequency,duration",
        [
            (
                ["EUR=", "GBP=", "JPY="],
                ["BID", "ASK"],
                "2s",
                "7s",
            )
        ],
    )
    @pytest.mark.caseid("40113562")
    def test_recording_pricing_stream_ohlc_data_with_few_recorders(
        self, open_desktop_session, universe, fields, frequency, duration
    ):
        stream = open_pricing_stream(universe=universe, fields=fields)

        stream.recorder.record(frequency=frequency, duration=duration)
        history_response_01 = stream.recorder.get_history()
        check_history_for_expected_amount_of_bars(
            stream, history_response_01, frequency, duration
        )

        stream.recorder.record(frequency=frequency, duration=duration)
        history_response_02 = stream.recorder.get_history()
        check_history_for_expected_amount_of_bars(
            stream, history_response_02, frequency, duration, recorders_amount=2
        )

        stream.recorder.record(frequency=frequency, duration=duration)
        history_response_03 = stream.recorder.get_history()
        check_history_for_expected_amount_of_bars(
            stream, history_response_03, frequency, duration, recorders_amount=3
        )

    @allure.title("Recording a pricing stream ohlc data with callbacks")
    @pytest.mark.parametrize(
        "universe,fields,frequency,duration,time_to_sleep",
        [("GBP=", ["BID"], "3s", "15s", 0), ("GBP=", ["BID"], "3s", None, 5)],
    )
    @pytest.mark.caseid("39028007")
    def test_recording_pricing_stream_ohlc_data_with_callbacks(
        self,
        open_desktop_session,
        universe,
        fields,
        frequency,
        duration,
        time_to_sleep,
    ):
        callback_history = []
        stream = open_pricing_stream(universe, fields)
        start_time = time.time()
        stream.recorder.record(
            frequency=frequency,
            duration=duration,
            on_data=lambda history, recorder: callback_history.append(history),
        )
        if duration == None:
            duration = 15
            asyncio.run(asyncio.sleep(duration))
            stream.recorder.stop()
            history_01 = stream.recorder.get_history()
            time.sleep(time_to_sleep)
            history_02 = stream.recorder.get_history()
            assert (
                history_02.shape == history_01.shape
            ), f"Recorder wasn't stopped, recordered additional updates after stop() method"

        elapsed_time_secs = time.time() - start_time - time_to_sleep
        history_response = stream.recorder.get_history()
        stream.close()

        check_history_for_expected_amount_of_bars(
            stream, history_response, frequency, duration
        )
        check_df_recording_duration(elapsed_time_secs, duration)
        check_df_recording_frequency(history_response, frequency)
        assert len(callback_history) == len(
            history_response.values
        ), f"Amount of callback updates is not suited with recorded history"
        for history_update in callback_history:
            assert (
                history_update.values in history_response.values
            ), f"Found update row '{history_update}' is not present in recorded history"

    @allure.title("Recording a pricing updates data during defined duration")
    @pytest.mark.parametrize(
        "universe,fields,expected_fields,frequency,duration",
        [
            (
                ["EUR=", "GBP="],
                ["BID", "ASK", "CF_NETCHNG"],
                [
                    ("GBP=", "CF_NETCHNG"),
                    ("EUR=", "BID"),
                    ("EUR=", "ASK"),
                    ("GBP=", "BID"),
                    ("EUR=", "CF_NETCHNG"),
                    ("GBP=", "ASK"),
                ],
                "tick",
                "5s",
            ),
            (
                ["EUR=", "GBP="],
                [],
                [],
                "tick",
                "5s",
            ),
        ],
    )
    @pytest.mark.caseid("39028009")
    def test_stream_recording_all_updates_until_duration_ends(
        self,
        open_desktop_session,
        universe,
        fields,
        expected_fields,
        duration,
        frequency,
    ):
        stream = open_pricing_stream(universe, fields)
        stream.recorder.record(duration=duration)
        stream.recorder.stop()
        stream.close()
        check_stream_closed(stream)
        history_response = stream.recorder.get_history()

        check_stream_fields(stream, universe, fields)
        check_column_names_is_exist_in_response_and_df_not_empty(
            history_response, expected_fields
        )
        check_if_dataframe_is_not_none(history_response)
        assert (
            stream.recorder._ohlc_builder is None
        ), f"There is inconsistency in recorded data"

    @allure.title("Stream recording with mix of valid and invalid parameters")
    @pytest.mark.parametrize(
        "universes,fields,expected_fields,frequency,duration",
        [
            (
                ["GBP=", "INVALID"],
                ["BID", "ASK", "INVALID"],
                [
                    ("GBP=", "BID"),
                    ("GBP=", "ASK"),
                ],
                "tick",
                "7s",
            ),
            (
                ["GBP=", "INVALID"],
                ["BID", "ASK", "INVALID"],
                [
                    ("GBP=", "ASK", "open"),
                    ("GBP=", "ASK", "high"),
                    ("GBP=", "ASK", "low"),
                    ("GBP=", "ASK", "close"),
                    ("GBP=", "BID", "open"),
                    ("GBP=", "BID", "high"),
                    ("GBP=", "BID", "low"),
                    ("GBP=", "BID", "close"),
                    ("ticks count", "", ""),
                ],
                "3s",
                "7s",
            ),
        ],
    )
    @pytest.mark.caseid("39028012")
    def test_stream_recording_with_mix_of_valid_and_invalid_params(
        self,
        open_desktop_session,
        universes,
        fields,
        expected_fields,
        frequency,
        duration,
    ):
        stream = open_pricing_stream(universes, fields)
        stream.recorder.record(frequency=frequency, duration=duration)
        stream.close()
        history_response = stream.recorder.get_history()

        check_column_names_is_exist_in_response_and_df_not_empty(
            history_response, expected_fields
        )
        check_if_dataframe_is_not_none(history_response)
        assert not is_universe_exist(
            history_response, universes[1:]
        ), f"Expected invalid universe was met in response dataframe"
        assert is_universe_exist(
            history_response, universes[:-1]
        ), f"Expected valid universe was not met in response dataframe"
