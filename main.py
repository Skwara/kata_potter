import pytest


class PriceCalculator:
    DISCOUNTS = {1: 0, 2: 0.05, 3: 0.1, 4: 0.2, 5: 0.25}  # 6: 1
    BOOK_PRICE = 8

    def __init__(self, basket):
        self.basket = basket

    def calculate_price(self):
        return sum([PriceCalculator.calc_set_price(book_set) for book_set in self.create_discount_sets()])

    def create_discount_sets(self):
        discount_sets = []
        for book in self.basket:
            best_set = []
            for book_set in discount_sets:
                if book not in book_set:
                    if PriceCalculator.book_set_score(best_set + [book]) < PriceCalculator.book_set_score(book_set + [book]):
                        best_set = book_set
                    elif PriceCalculator.book_set_score(best_set + [book]) == PriceCalculator.book_set_score(book_set + [book]):
                        if len(best_set) > len(book_set):
                            best_set = book_set
            if not best_set:
                discount_sets.append(best_set)
            best_set.append(book)
        return discount_sets

    @staticmethod
    def book_set_score(book_set):
        if not book_set:
            return -1
        return PriceCalculator.DISCOUNTS[len(book_set)] / len(book_set)

    @staticmethod
    def calc_set_price(book_set):
        return len(book_set) * PriceCalculator.BOOK_PRICE * (1 - PriceCalculator.DISCOUNTS[len(book_set)])


def test_no_discounts():
    assert PriceCalculator([]).calculate_price() == 0 * 8
    assert PriceCalculator(["a"]).calculate_price() == 1 * 8
    assert PriceCalculator(["a", "a"]).calculate_price() == 2 * 8
    assert PriceCalculator(["a", "a", "a"]).calculate_price() == 3 * 8


def test_simple_discounts():
    assert PriceCalculator(["a", "b"]).calculate_price() == 2 * 8 * 0.95
    assert PriceCalculator(["a", "b", "c"]).calculate_price() == 3 * 8 * 0.9
    assert PriceCalculator(["a", "b", "c", "d"]).calculate_price() == 4 * 8 * 0.8
    assert PriceCalculator(["a", "b", "c", "d", "e"]).calculate_price() == 5 * 8 * 0.75
    assert PriceCalculator(["a", "b", "c", "d", "e"]*2).calculate_price() == 5 * 8 * 0.75 * 2
    assert PriceCalculator(["a", "b", "c", "d", "e"]*2 + ["a"]).calculate_price() == 5 * 8 * 0.75 * 2 + 8


def test_two_sets():
    assert PriceCalculator(["a", "b", "a", "b"]).calculate_price() == 2 * 8 * 0.95 * 2


def test_non_greedy_discount():
    assert PriceCalculator(["a", "b", "c", "d", "a", "b", "c", "e"]).calculate_price() == 2 * 4 * 8 * 0.8


def test_double_non_greedy_discount():
    assert PriceCalculator(["a", "b", "c", "d", "a", "b", "c", "a", "b", "c", "e", "d"]).calculate_price() == 3 * 4 * 8 * 0.8
    assert PriceCalculator(["a", "b", "c", "d", "a", "b", "c", "a", "b", "c", "e", "d", "a"]).calculate_price() == 3 * 4 * 8 * 0.8 + 8
