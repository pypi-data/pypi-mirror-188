# This test is commented due to temporary removing of
# function from publick API
# https://jira.refinitiv.com/browse/EAPI-2233
# Uncomment it if function would be returned back

# """
# https://jira.refinitiv.com/browse/EAPI-2223
# """
#
# import inspect
#
# import pytest
#
# import refinitiv.data as rd
#
# unneeded_params = ["on_response", "session", "closure"]
#
#
# @pytest.mark.parametrize(
#     "testing_function",
#     [
#         getattr(rd.function, func_name)
#         for func_name in dir(rd.function)
#         if not func_name.startswith("_")
#     ],
# )
# def test_function(testing_function):
#     argspec = inspect.getfullargspec(testing_function)
#
#     testing_unneeded_params = filter(lambda arg: arg in unneeded_params, argspec.args)
#
#     assert list(testing_unneeded_params) == [], testing_function.__name__
