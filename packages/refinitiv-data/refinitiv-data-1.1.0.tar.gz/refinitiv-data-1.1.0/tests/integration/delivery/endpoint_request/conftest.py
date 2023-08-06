from refinitiv.data.delivery import endpoint_request

definition = endpoint_request.Definition(
    url="/data/estimates/v1/view-actuals-kpi/annual",
    method=endpoint_request.RequestMethod.GET,
    query_parameters={"universe": "IBM"},
)
