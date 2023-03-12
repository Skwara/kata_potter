import pytest


class PriceCalculator:
    DISCOUNTS = {1: 0, 2: 0.05, 3: 0.1, 4: 0.2, 5: 0.25, 6: 0.4}
    BOOK_PRICE = 8

    def __init__(self, basket: [str]):
        self.basket = basket

    def calculate_price(self):
        return sum([PriceCalculator.calc_set_price(book_set) for book_set in self.create_discount_sets()])

    def create_discount_sets(self):
        discount_sets = []
        ordered_discounts = PriceCalculator.order_discounts_by_score()

        score = PriceCalculator.discount_score(ordered_discounts[0])
        for discount in ordered_discounts:
            discount_score = PriceCalculator.discount_score(discount)
            assert discount_score <= score
            score = discount_score
            while self.basket:
                unique_set = set(self.basket)  # Consider created sets, but only with score equal or lower? Not really
                if discount[0] > len(unique_set):
                    break
                diff = len(unique_set) - discount[0]
                unique_set = list(unique_set)[diff:]
                discount_sets.append(unique_set)
                for book in unique_set:
                    self.basket.remove(book)
        return discount_sets

    @staticmethod
    def order_discounts_by_score() -> [()]:
        return sorted(PriceCalculator.DISCOUNTS.items(), key=lambda discount: PriceCalculator.discount_score(discount), reverse=True)

    @staticmethod
    def discount_score(discount):
        if not discount[0]:
            return -1
        return discount[1] / discount[0]

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


def test_discount_score_increase_after_equal_scores():
    assert PriceCalculator(["a", "b", "c", "d", "a", "b", "c", "e", "f"]).calculate_price() == 6 * 8 * 0.6 + 3 * 8 * 0.9


def test_method_order_discounts_by_score_simple():
    print(PriceCalculator.order_discounts_by_score())
    assert PriceCalculator.order_discounts_by_score() == [(6, 0.4), (4, 0.2), (5, 0.25), (3, 0.1), (2, 0.05), (1, 0)]
