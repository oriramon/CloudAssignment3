import connectionController
from assertions import *
from restApiController import *


# tests for dish API
orange_id = None
spaghetti_id = None
applepie_id = None

def test_add_three_dishes():
    global orange_id
    global spaghetti_id
    global applepie_id
    orange_id = add_dish("orange")
    spaghetti_id = add_dish("spaghetti")
    applepie_id = add_dish("apple pie")

    assert orange_id != spaghetti_id
    assert orange_id != applepie_id
    assert applepie_id != spaghetti_id

def test_get_orange_by_ID():
    global orange_id
    response = connectionController.http_get(f"dishes/{orange_id}")
    sodium = int(response.json()["sodium"])
    
    assert (sodium >= .9) and (sodium <= 1.1)
    assert response.status_code == 200

def test_get_dishes():
    response = connectionController.http_get("dishes")
    dishes = response.json()
    assert len(dishes) == 3
    assert response.status_code == 200

def test_add_bad_dish():
    dish = {"name": "blah"}
    response = connectionController.http_post("dishes", dish)
    return_code = int(response.json())
    assert response.status_code == -3
    assert (return_code == 404) or (return_code == 400) or (return_code == 422)

def test_add_existing_dish():
    dish = {"name": "orange"}
    response = connectionController.http_post("dishes", dish)
    return_code = int(response.json())
    assert response.status_code == -2
    assert (return_code == 404) or (return_code == 400) or (return_code == 422)

def test_add_meal():
    global orange_id
    global spaghetti_id
    global applepie_id
    delicious_id = add_meal("delicious", orange_id, spaghetti_id, applepie_id)
    assert int(delicious_id) > 0

def test_get_meals():
    response = connectionController.http_get(f"meals")
    meal = response.json()
    cal = meal["cal"]
    assert len(meal) == 1
    assert (cal >= 400) and (cal <= 500)
    assert response.status_code == 200

def test_add_existing_meal():
    global orange_id
    global spaghetti_id
    global applepie_id
    meal = {
        "name": "delicious",
        "appetizer": orange_id,
        "main": spaghetti_id,
        "dessert": applepie_id
    }
    response = connectionController.http_post("meals", meal)
    return_code = int(response.json())
    
    assert (response.status_code == 400) or (response.status_code == 422)
    assert return_code == -2