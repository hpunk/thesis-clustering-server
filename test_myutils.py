from myutils import distance_function

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