
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
        Scorer.calculate_game_points(test_vector),
        expected_score,
    )


TEST_INVALID = (
    'D',
    'UDD',
)


def test_scorer_rejects_impossible_event_sequences():
    for test_vector in TEST_INVALID:
        yield check_invalid, test_vector


def check_invalid(test_vector):
    with assert_raises(InvalidScoresheetException):
        Scorer.calculate_game_points(test_vector)
