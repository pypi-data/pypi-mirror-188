from datetime import datetime


def check_amount_of_objects_in_response_not_bigger_than(expected_amount, response):
    values_list = response.data.raw["value"]
    values_list_size = len(values_list)
    assert values_list_size <= expected_amount, (
        f"Retrieved number of objects {values_list_size} "
        f"is bigger than expected: {expected_amount}"
    )


def convert_string_to_date_format(date_string, date_format):
    return datetime.strptime(date_string, date_format)


def check_no_objects_in_response(response):
    objects = response.data.raw["value"]
    assert not objects, f"Non-empty response.data.raw received: {response.data.raw}"
