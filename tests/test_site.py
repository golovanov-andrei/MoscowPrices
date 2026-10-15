import unittest

from app import app, stations


class SiteIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.payload = {"area": 50, "rooms": 2, "floor": 5, "minutes": 10, "metro": "Пушкинская"}

    def test_home_map_and_assets(self):
        for path in ["/", "/metro_map", "/static/moscow.css", "/static/images/house.png",
                     "/static/icons/telegram.svg", "/static/predict.js"]:
            with self.subTest(path=path):
                with self.client.get(path) as response:
                    self.assertEqual(response.status_code, 200)

    def test_station_list_matches_model_table(self):
        response = self.client.get("/stations")
        self.assertEqual(response.json, stations)
        self.assertIn(self.payload["metro"], response.json)

    def test_original_model_returns_positive_price(self):
        response = self.client.post("/predict", json=self.payload)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.json["prediction"], 0)

    def test_bad_inputs_return_readable_error(self):
        for changed in [{"metro": "unknown"}, {"area": -5}, {"rooms": 2.5}, {"minutes": None}]:
            with self.subTest(changed=changed):
                response = self.client.post("/predict", json={**self.payload, **changed})
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.json)

    def test_non_json_request(self):
        self.assertEqual(self.client.post("/predict", data="broken").status_code, 400)

    def test_health_and_legacy_url(self):
        self.assertEqual(self.client.get("/health").status_code, 200)
        self.assertEqual(self.client.get("/moscow.html").status_code, 302)


if __name__ == "__main__":
    unittest.main()
