from myutils import distance_function, generate_query_for_count, generate_query_for_clustering

#testing the generation of query for clustering with different parameters
def test_query_generation_for_clustering():
    only_dates_query = generate_query_for_clustering("2020-01-01","2020-02-02",0,0,0)
    assert "state" not in only_dates_query
    assert "province" not in only_dates_query
    assert "district" not in only_dates_query

    only_dates_and_state_query = generate_query_for_clustering("2020-01-01","2020-02-02",1,0,0)
    assert "state" in only_dates_and_state_query
    assert "province" not in only_dates_and_state_query
    assert "district" not in only_dates_and_state_query

    only_dates_and_province_and_state_query = generate_query_for_clustering("2020-01-01","2020-02-02",1,101,0)
    assert "state" not in only_dates_and_province_and_state_query
    assert "province" in only_dates_and_province_and_state_query
    assert "district" not in only_dates_and_province_and_state_query

#testing the generation of query for count with different parameters
def test_query_generation_for_count():
    only_dates_query = generate_query_for_count("2020-01-01","2020-02-02",0,0,0)
    assert "state" not in only_dates_query
    assert "province" not in only_dates_query
    assert "district" not in only_dates_query

    only_dates_and_state_query = generate_query_for_count("2020-01-01","2020-02-02",1,0,0)
    assert "state" in only_dates_and_state_query
    assert "province" not in only_dates_and_state_query
    assert "district" not in only_dates_and_state_query

    only_dates_and_province_and_state_query = generate_query_for_count("2020-01-01","2020-02-02",1,101,0)
    assert "state" not in only_dates_and_province_and_state_query
    assert "province" in only_dates_and_province_and_state_query
    assert "district" not in only_dates_and_province_and_state_query

#testing maximum distance value of two completely different objects, based on if columns were categorical (only different values) or if were numerical (extreme values)
def test_maximum_distance_from_distance_function():
    obj_a = [
        1,
        2,
        1,
        0,
        20,
        2,
        0,
        3,
        1,
        1,
        1,
        0,
        0,
        0,
        1,
        0,
        120,
        1,
        1,
        0,
        0
    ]
    obj_b = [
        0,
        1,
        0,
        20,
        0,
        1,
        1,
        4,
        5,
        0,
        2,
        1,
        1,
        1,
        2,
        1,
        0,
        0,
        0,
        1,
        1
    ]
    distance = distance_function(obj_a,obj_b)
    assert distance == 1

#testing minimum distance value of two completely different objects, based on if columns were categorical (only different values) or if were numerical (extreme values)
def test_minimum_distance_from_distance_function():
    obj_a = [
        1,
        2,
        1,
        0,
        20,
        2,
        0,
        3,
        1,
        1,
        1,
        0,
        0,
        0,
        1,
        0,
        120,
        1,
        1,
        0,
        0
    ]
    obj_b = [
        1,
        2,
        1,
        0,
        20,
        2,
        0,
        3,
        1,
        1,
        1,
        0,
        0,
        0,
        1,
        0,
        120,
        1,
        1,
        0,
        0
    ]
    distance = distance_function(obj_a,obj_b)
    assert distance == 0