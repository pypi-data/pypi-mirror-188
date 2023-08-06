def check_document_title_contains_query(response, query):
    for search_item in response.data.hits:
        assert (
            query.lower() in search_item.DocumentTitle.lower()
        ), f"Found result which does not contain query: {search_item}"


def check_business_entity_for_every_document_in_response(
    response, expected_business_entity
):
    for hits_item in response.data.hits:
        assert (
            hits_item.BusinessEntity == expected_business_entity
        ), f"Found the document with BusinessEntity different from expected: {hits_item.BusinessEntit}"


def check_hits_and_dataframe_columns(response, hits_item_attributes):
    assert len(response.data.hits) == 10
    for attr in hits_item_attributes:
        assert hasattr(
            response.data.hits[0], attr
        ), f"{attr} is missing for HitsItem object"
        assert (
            attr in response.data.df.columns
        ), f"{attr} header is missing in DataFrame"


def check_navigator_entity_in_response(
    response,
    expected_navigator_entity,
    expected_sub_navigator=None,
    navigator_props=None,
    sub_navigator_props=None,
):
    def check_buckets_attrs(bucket, navigator_name):
        assert hasattr(
            bucket, "count"
        ), f"count attribute is missing for {navigator_name} bucket"
        assert hasattr(
            bucket, "label"
        ), f"label attribute is missing for {navigator_name} bucket"

    def check_navigator_props(bucket, props):
        for entity in props:
            assert bucket[entity] is not None, f"{entity} data is missing"

    assert (
        expected_navigator_entity in response.data.navigators
    ), f"{expected_navigator_entity} is missing in requested navigators"
    assert (
        response.data.navigators[expected_navigator_entity].name
        == expected_navigator_entity
    )

    if response.data.raw["Navigators"][expected_navigator_entity]["Buckets"]:
        navigator_buckets = response.data.navigators[expected_navigator_entity].buckets
        for bucket in navigator_buckets:
            check_buckets_attrs(bucket, expected_navigator_entity)

            if navigator_props:
                check_navigator_props(bucket, navigator_props)

            if expected_sub_navigator:
                assert (
                    bucket.navigator is not None
                ), f"navigator attribute is missing for {expected_navigator_entity} bucket"
                assert bucket.navigator.name == expected_sub_navigator

                for bucket_item in bucket.navigator.buckets:
                    check_buckets_attrs(bucket_item, expected_navigator_entity)
                    assert (
                        bucket_item.navigator is None
                    ), f"sub sub navigators are not expected"

                    if sub_navigator_props:
                        check_navigator_props(bucket_item, sub_navigator_props)
