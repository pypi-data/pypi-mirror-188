def check_all_packages_names_contain_keyword(response, keyword):
    for package in response.data.raw["value"]:
        assert (
            keyword.lower() in package["packageName"].lower()
        ), f"Found package which does not contain expected package name {keyword}: \n {package}"


def check_all_packages_types(response, package_type):
    for package in response.data.raw["value"]:
        assert (
            package_type.lower() == package["packageType"].lower()
        ), f"Found package which does not contain expected type {package_type}: \n {package}"


def check_bucket_name_in_all_packages(response, bucket_name):
    for package in response.data.raw["value"]:
        assert (
            bucket_name in package["bucketNames"]
        ), f"Found package which does not belong to expected bucket name {bucket_name}: \n {package}"


def check_included_total_result_in_response(response):
    assert (
        "totalResults" in response.data.raw.keys()
    ), f"Response does not contain totalResults property: \n{response}"


def check_included_entitlement_result_in_response(response):
    packages = response.data.raw["value"]
    for package in packages:
        assert (
            "isEntitled" in package.keys()
        ), f"Found package which does not have isEntitled property: {package}"


def check_packages_in_two_responses_are_not_the_same(response1, response2):
    for package in response1.data.raw["value"]:
        assert (
            package not in response2.data.raw["value"]
        ), f"Package from first request found in list of packages in the second request: \n {package}"


def check_packages_in_second_response_are_on_proper_position_in_first_response(
    response1, response2, page_size, page
):
    packages_first_chunk = response1.data.raw["value"]
    packages_second_chunk = response2.data.raw["value"]
    position_index = page_size * (page - 1)
    for package in packages_second_chunk:
        assert package == packages_first_chunk[position_index], (
            f"Package from requested page  does not match the package on position {position_index}. \n"
            f"Expected package:  {packages_first_chunk[position_index]}. \nRetrieved package: {package}"
        )
        position_index += 1
