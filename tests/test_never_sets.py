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

if __name__ == "__main__":
    unittest.main(verbosity=2)
