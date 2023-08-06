from refinitiv.data.delivery._data._endpoint_data_provider import EndpointRequestFactory


def test_endpoint_request_factory():
    # given
    factory = EndpointRequestFactory()
    body_params = {"key": "value"}
    expected_value = body_params

    # when
    testing_value = factory.extend_body_parameters(body_params)

    # then
    assert expected_value == testing_value
