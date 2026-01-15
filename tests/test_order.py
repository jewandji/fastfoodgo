import pytest
from fastfoodgo.order import calculate_order_total, validate_status_transition, OrderError

# --- Tests pour calculate_order_total ---

def test_calculate_total_nominal():
    items = [
        {'name': 'Burger', 'price': 10.0, 'quantity': 2},
        {'name': 'Fries', 'price': 5.0, 'quantity': 1}
    ]
    # 2*10 + 1*5 = 25
    assert calculate_order_total(items) == 25.0

def test_calculate_total_empty():
    assert calculate_order_total([]) == 0.0

def test_calculate_total_negative_price():
    items = [{'name': 'BadItem', 'price': -5.0, 'quantity': 1}]
    with pytest.raises(OrderError):
        calculate_order_total(items)

# --- Tests pour validate_status_transition ---

def test_transition_nominal():
    assert validate_status_transition("created", "paid") is True

def test_transition_invalid():
    # On ne peut pas passer directement de created à delivered
    assert validate_status_transition("created", "delivered") is False

def test_transition_unknown_status():
    with pytest.raises(OrderError):
        validate_status_transition("magical_status", "paid")