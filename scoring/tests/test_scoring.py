
# Path hackery
import os.path
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT)

from nose.tools import eq_

from score import Scorer, InvalidScoresheetException


TESTS = (
    ('', 0),
    ('U', 1),
    ('C', 1),
    ('BC', 0),
    ('BCC', 1),
    ('BBCC', 0),
    ('BBCCC', 1),
    ('BUC', 1),
    ('BUCD', 0),
    ('BUCC', 3),
    ('BUCCD', 2),
    ('CB', 1),
    ('CCB', 2),
    ('UCBCBCBCBC', 3),
)


def test_scorer_produces_scores_matching_test_vectors():
    for test_vector, expected_score in TESTS:
        yield check_scorer_result, test_vector, expected_score


def check_scorer_result(test_vector, expected_score):
    eq_(
        Scorer.calculate_game_points(test_vector),
        expected_score,
    )
