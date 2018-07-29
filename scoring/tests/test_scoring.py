
# Path hackery
import os.path
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT)

from nose.tools import assert_raises, eq_

from score import Scorer, InvalidScoresheetException


TESTS = (
    ('', 0),
    ('U', 2),
    ('C', 6),
    ('BC', 0),
    ('BCC', 6),
    ('BBCC', 0),
    ('BBCCC', 6),
    ('BUC', 2),
    ('BUCD', 0),
    ('BUCC', 12),
    ('BUCCD', 10),
    ('CB', 6),
    ('CCB', 12),
    ('UC BC BC BC BC', 12),
)


def test_scorer_produces_scores_matching_test_vectors():
    for test_vector, expected_score in TESTS:
        yield check_scorer_result, test_vector, expected_score


def check_scorer_result(test_vector, expected_score):
    eq_(
        Scorer.calculate_game_points(test_vector, False),
        expected_score,
    )


TEST_INVALID = (
    'D',
    'UDD',
    'UUU UUU UU',
)


def test_scorer_rejects_impossible_event_sequences():
    for test_vector in TEST_INVALID:
        yield check_invalid, test_vector


def check_invalid(test_vector):
    with assert_raises(InvalidScoresheetException):
        Scorer.calculate_game_points(test_vector, False)


def test_invalid_when_holding_super_but_no_cans():
    with assert_raises(InvalidScoresheetException):
        Scorer.calculate_game_points('BUCD', True)


def test_noone_has_super_can():
    scores = Scorer({
        'ABC': {'events': 'C'},
        'DEF': {'events': 'C'},
    }, None).calculate_scores()

    eq_(scores, {'ABC': 6, 'DEF': 6})


def test_first_has_super_can():
    scores = Scorer({
        'ABC': {'events': 'CU', 'holding-super': True},
        'DEF': {'events': 'CU', 'holding-super': False},
    }, None).calculate_scores()

    eq_(scores, {'ABC': 8, 'DEF': 4})


def test_second_has_super_can():
    scores = Scorer({
        'ABC': {'events': 'CU', 'holding-super': False},
        'DEF': {'events': 'CU', 'holding-super': True},
    }, None).calculate_scores()

    eq_(scores, {'ABC': 4, 'DEF': 8})


def test_both_have_super_can():
    with assert_raises(InvalidScoresheetException):
        Scorer({
            'ABC': {'events': 'CU', 'holding-super': True},
            'DEF': {'events': 'CU', 'holding-super': True},
        }, None).calculate_scores()
