"""
Test suite for Candidate data structures and validation.

Tests cover:
- Candidate 5-tuple structure (A, B, R, P, F)
- Invariant enforcement (non-empty predictions and failures)
- Representation preservation
- Admissibility pre-checks
"""

import pytest
from typing import Set, Dict, Any
from dataclasses import dataclass


@dataclass
class Candidate:
    """5-tuple candidate: (A, B, R, P, F)"""
    assumptions: Set[str]  # A: Explicit assumptions
    bounds: Dict[str, tuple]  # B: Parameter bounds
    relations: Dict[str, str]  # R: Structural relations
    predictions: Set[str]  # P: Testable predictions
    failures: Set[str]  # F: Failure conditions


class TestCandidateStructure:
    """Test Candidate 5-tuple structure and invariants."""

    def test_candidate_creation_valid(self):
        """Test creation of valid candidate."""
        c = Candidate(
            assumptions={"param_x > 0"},
            bounds={"x": (0, 100)},
            relations={"R": "linear"},
            predictions={"output: y ≈ 2x"},
            failures={"output: y ≈ 2x fails when x > 50"}
        )
        assert c.assumptions == {"param_x > 0"}
        assert c.bounds == {"x": (0, 100)}
        assert c.relations == {"R": "linear"}
        assert c.predictions == {"output: y ≈ 2x"}
        assert c.failures == {"output: y ≈ 2x fails when x > 50"}

    def test_candidate_invariant_non_empty_predictions(self):
        """Test invariant: P ≠ ∅ (predictions must be non-empty)."""
        with pytest.raises(ValueError, match="Predictions must be non-empty"):
            Candidate(
                assumptions={"param_x > 0"},
                bounds={"x": (0, 100)},
                relations={"R": "linear"},
                predictions=set(),  # INVALID: empty predictions
                failures={"output: y ≈ 2x fails when x > 50"}
            )

    def test_candidate_invariant_non_empty_failures(self):
        """Test invariant: F ≠ ∅ (failures must be non-empty)."""
        with pytest.raises(ValueError, match="Failures must be non-empty"):
            Candidate(
                assumptions={"param_x > 0"},
                bounds={"x": (0, 100)},
                relations={"R": "linear"},
                predictions={"output: y ≈ 2x"},
                failures=set()  # INVALID: empty failures
            )

    def test_candidate_multiple_predictions(self):
        """Test candidate with multiple testable predictions."""
        c = Candidate(
            assumptions={"param_x > 0", "param_y < 1"},
            bounds={"x": (0, 100), "y": (0, 1)},
            relations={"R": "linear", "S": "quadratic"},
            predictions={
                "output: y ≈ 2x",
                "rate: dy/dt > 0",
                "stability: eigenvalues < 0"
            },
            failures={
                "output: y ≈ 2x fails when x > 50",
                "rate: dy/dt > 0 fails when param_y > 0.5"
            }
        )
        assert len(c.predictions) == 3
        assert len(c.failures) == 2

    def test_candidate_multiple_assumptions_and_bounds(self):
        """Test candidate with complex assumptions and bounds."""
        c = Candidate(
            assumptions={
                "param_x > 0",
                "param_y < 1",
                "relation_type == 'linear'",
                "causality assumptions hold"
            },
            bounds={
                "x": (0, 100),
                "y": (0, 1),
                "z": (-10, 10),
                "scale": (1e-3, 1e3)
            },
            relations={
                "primary": "linear",
                "secondary": "quadratic",
                "tertiary": "exponential"
            },
            predictions={"prediction_1"},
            failures={"failure_1"}
        )
        assert len(c.assumptions) == 4
        assert len(c.bounds) == 4
        assert len(c.relations) == 3

    def test_candidate_empty_assumptions_allowed(self):
        """Test that empty assumptions are allowed (no invariant)."""
        c = Candidate(
            assumptions=set(),  # ALLOWED: no invariant on assumptions
            bounds={},
            relations={},
            predictions={"prediction_1"},
            failures={"failure_1"}
        )
        assert c.assumptions == set()

    def test_candidate_empty_bounds_allowed(self):
        """Test that empty bounds are allowed (no invariant)."""
        c = Candidate(
            assumptions={"assumption_1"},
            bounds={},  # ALLOWED: no invariant on bounds
            relations={},
            predictions={"prediction_1"},
            failures={"failure_1"}
        )
        assert c.bounds == {}

    def test_candidate_empty_relations_allowed(self):
        """Test that empty relations are allowed (no invariant)."""
        c = Candidate(
            assumptions={"assumption_1"},
            bounds={"x": (0, 1)},
            relations={},  # ALLOWED: no invariant on relations
            predictions={"prediction_1"},
            failures={"failure_1"}
        )
        assert c.relations == {}

    def test_candidate_equality(self):
        """Test candidate equality comparison."""
        c1 = Candidate(
            assumptions={"a1"},
            bounds={"x": (0, 1)},
            relations={"r1"},
            predictions={"p1"},
            failures={"f1"}
        )
        c2 = Candidate(
            assumptions={"a1"},
            bounds={"x": (0, 1)},
            relations={"r1"},
            predictions={"p1"},
            failures={"f1"}
        )
        assert c1 == c2

    def test_candidate_inequality_different_predictions(self):
        """Test that candidates with different predictions are unequal."""
        c1 = Candidate(
            assumptions={"a1"},
            bounds={"x": (0, 1)},
            relations={"r1"},
            predictions={"p1"},
            failures={"f1"}
        )
        c2 = Candidate(
            assumptions={"a1"},
            bounds={"x": (0, 1)},
            relations={"r1"},
            predictions={"p2"},  # Different
            failures={"f1"}
        )
        assert c1 != c2

    def test_candidate_copy_independence(self):
        """Test that copying a candidate doesn't share mutable state."""
        import copy
        c1 = Candidate(
            assumptions={"a1"},
            bounds={"x": (0, 1)},
            relations={"r1"},
            predictions={"p1"},
            failures={"f1"}
        )
        c2 = copy.deepcopy(c1)
        c2.predictions.add("p2")
        assert "p2" not in c1.predictions


class TestAdmissibilityPreChecks:
    """Test pre-checks for admissibility conditions."""

    def test_candidate_has_testable_predictions(self):
        """Test that candidate has at least one testable prediction."""
        c = Candidate(
            assumptions={"a1"},
            bounds={},
            relations={},
            predictions={"p1"},
            failures={"f1"}
        )
        assert len(c.predictions) > 0

    def test_candidate_has_falsifiable_failures(self):
        """Test that candidate has at least one falsifiable failure condition."""
        c = Candidate(
            assumptions={"a1"},
            bounds={},
            relations={},
            predictions={"p1"},
            failures={"f1"}
        )
        assert len(c.failures) > 0

    def test_candidate_bounds_sanity(self):
        """Test bounds are well-formed (lower < upper)."""
        def validate_bounds(bounds: Dict[str, tuple]) -> bool:
            for param, (lower, upper) in bounds.items():
                if lower >= upper:
                    return False
            return True

        c = Candidate(
            assumptions={"a1"},
            bounds={"x": (0, 1), "y": (-10, 10)},
            relations={},
            predictions={"p1"},
            failures={"f1"}
        )
        assert validate_bounds(c.bounds)

    def test_invalid_bounds_detected(self):
        """Test that invalid bounds (lower >= upper) are detected."""
        def validate_bounds(bounds: Dict[str, tuple]) -> bool:
            for param, (lower, upper) in bounds.items():
                if lower >= upper:
                    return False
            return True

        bounds = {"x": (1, 0)}  # Invalid: lower > upper
        assert not validate_bounds(bounds)


class TestCandidateRepresentation:
    """Test candidate representation and serialization."""

    def test_candidate_to_dict(self):
        """Test candidate serialization to dictionary."""
        c = Candidate(
            assumptions={"a1"},
            bounds={"x": (0, 1)},
            relations={"r1": "linear"},
            predictions={"p1"},
            failures={"f1"}
        )
        d = {
            "assumptions": c.assumptions,
            "bounds": c.bounds,
            "relations": c.relations,
            "predictions": c.predictions,
            "failures": c.failures
        }
        assert d["assumptions"] == {"a1"}
        assert d["predictions"] == {"p1"}

    def test_candidate_from_dict(self):
        """Test candidate creation from dictionary."""
        d = {
            "assumptions": {"a1"},
            "bounds": {"x": (0, 1)},
            "relations": {"r1": "linear"},
            "predictions": {"p1"},
            "failures": {"f1"}
        }
        c = Candidate(**d)
        assert c.assumptions == {"a1"}
        assert c.predictions == {"p1"}

    def test_candidate_string_representation(self):
        """Test candidate string representation."""
        c = Candidate(
            assumptions={"a1"},
            bounds={"x": (0, 1)},
            relations={"r1"},
            predictions={"p1"},
            failures={"f1"}
        )
        s = str(c)
        assert "Candidate" in s or "assumptions" in s.lower()


class TestCandidateDistinctness:
    """Test distinctness and discriminability of candidates."""

    def test_candidates_structurally_distinct(self):
        """Test that two candidates can be distinguished by structure."""
        c1 = Candidate(
            assumptions={"assumption_type_A"},
            bounds={"x": (0, 100)},
            relations={"primary": "linear"},
            predictions={"prediction_A"},
            failures={"failure_A"}
        )
        c2 = Candidate(
            assumptions={"assumption_type_B"},
            bounds={"x": (0, 100)},
            relations={"primary": "quadratic"},
            predictions={"prediction_B"},
            failures={"failure_B"}
        )
        # Different assumptions and relations
        assert c1.assumptions != c2.assumptions
        assert c1.relations != c2.relations

    def test_candidates_same_bounds_different_predictions(self):
        """Test candidates with same bounds but different predictions."""
        c1 = Candidate(
            assumptions={"a1"},
            bounds={"x": (0, 100)},
            relations={},
            predictions={"linear growth"},
            failures={"fails at x > 50"}
        )
        c2 = Candidate(
            assumptions={"a1"},
            bounds={"x": (0, 100)},
            relations={},
            predictions={"exponential growth"},
            failures={"fails at x > 50"}
        )
        assert c1.bounds == c2.bounds
        assert c1.predictions != c2.predictions


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
