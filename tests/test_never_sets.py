import json
import math
import tempfile
import unittest
from pathlib import Path

from never_sets.core import check_never_sets
from never_sets.country_store import load_country, to_latlon_list

DATA = Path(__file__).resolve().parents[1] / "data" / "countries"

class TestNeverSets(unittest.TestCase):
    def test_france_passes_strict(self):
        c = load_country(DATA / "france.json")
        res = check_never_sets(to_latlon_list(c), visibility_limit_deg=0.0, decl_step_deg=0.25, hour_angle_step_deg=0.25)
        self.assertTrue(res.always_daylight_somewhere)

    def test_usa_fails_strict(self):
        c = load_country(DATA / "usa.json")
        res = check_never_sets(to_latlon_list(c), visibility_limit_deg=0.0, decl_step_deg=0.25, hour_angle_step_deg=0.25)
        self.assertFalse(res.always_daylight_somewhere)

    def test_result_has_witness(self):
        c = load_country(DATA / "france.json")
        res = check_never_sets(to_latlon_list(c), visibility_limit_deg=0.0, decl_step_deg=1.0, hour_angle_step_deg=1.0)
        self.assertIsInstance(res.witness.decl_deg, float)
        self.assertIsInstance(res.witness.hour_angle_deg, float)
        self.assertGreaterEqual(len(res.witness.best_point_indices), 1)

    def test_duplicate_points_return_multiple_witnesses(self):
        pts = [(0.0, 0.0), (0.0, 0.0)]
        res = check_never_sets(pts, decl_step_deg=10.0, hour_angle_step_deg=10.0, tie_tol=0.0)
        self.assertEqual(res.witness.best_point_indices, (0, 1))

    def test_duplicate_points_single_witness(self):
        pts = [(0.0, 0.0), (0.0, 0.0)]
        res = check_never_sets(
            pts,
            decl_step_deg=10.0,
            hour_angle_step_deg=10.0,
            tie_tol=0.0,
            return_multiple_best_points=False,
        )
        self.assertEqual(len(res.witness.best_point_indices), 1)

    def test_rejects_empty_points(self):
        with self.assertRaises(ValueError):
            check_never_sets([])

    def test_rejects_invalid_steps(self):
        pts = [(0.0, 0.0)]
        with self.assertRaises(ValueError):
            check_never_sets(pts, decl_step_deg=0.0)
        with self.assertRaises(ValueError):
            check_never_sets(pts, hour_angle_step_deg=0.0)

    def test_rejects_invalid_angles(self):
        pts = [(0.0, 0.0)]
        with self.assertRaises(ValueError):
            check_never_sets(pts, obliquity_deg=-1.0)
        with self.assertRaises(ValueError):
            check_never_sets(pts, visibility_limit_deg=100.0)

    def test_rejects_invalid_tie_tolerance(self):
        pts = [(0.0, 0.0)]
        with self.assertRaises(ValueError):
            check_never_sets(pts, tie_tol=-0.5)

    def test_rejects_non_finite_points(self):
        pts = [(math.nan, 0.0)]
        with self.assertRaises(ValueError):
            check_never_sets(pts)


class TestCountryStore(unittest.TestCase):
    def write_country(self, payload: dict) -> Path:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
            Path(tmp.name).write_text(json.dumps(payload), encoding="utf-8")
            return Path(tmp.name)

    def test_requires_id_and_points(self):
        path = self.write_country({"id": "x"})
        try:
            with self.assertRaises(ValueError):
                load_country(path)
        finally:
            path.unlink(missing_ok=True)

    def test_requires_non_empty_points(self):
        path = self.write_country({"id": "x", "points": []})
        try:
            with self.assertRaises(ValueError):
                load_country(path)
        finally:
            path.unlink(missing_ok=True)

    def test_rejects_non_numeric_points(self):
        path = self.write_country({"id": "x", "points": [{"label": "a", "lat": "bad", "lon": 0}]})
        try:
            with self.assertRaises(ValueError):
                load_country(path)
        finally:
            path.unlink(missing_ok=True)

    def test_loads_country(self):
        path = self.write_country({"id": "x", "name": "X", "points": [{"label": "a", "lat": 1, "lon": 2}]})
        try:
            country = load_country(path)
        finally:
            path.unlink(missing_ok=True)
        self.assertEqual(country.id, "x")
        self.assertEqual(country.name, "X")
        self.assertEqual(to_latlon_list(country), [(1.0, 2.0)])

if __name__ == "__main__":
    unittest.main(verbosity=2)
