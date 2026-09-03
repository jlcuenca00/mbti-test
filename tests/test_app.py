import unittest

from app import app, calculate_result, questions


class FourfoldTestCase(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SECRET_KEY="test-key")
        self.client = app.test_client()

    def test_public_pages_render(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertEqual(self.client.get("/quiz").status_code, 200)
        self.assertEqual(self.client.get("/feedback").status_code, 200)

    def test_result_requires_a_completed_test(self):
        response = self.client.get("/result")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.endswith("/quiz"))

    def test_all_second_choices_return_infp(self):
        answers = {f"q{index}": question["b"][0] for index, question in enumerate(questions)}
        mbti, dimensions = calculate_result(answers)
        self.assertEqual(mbti, "INFP")
        self.assertTrue(all(item["right_percent"] == 100 for item in dimensions))

    def test_completed_quiz_renders_result_breakdown(self):
        answers = {f"q{index}": question["a"][0] for index, question in enumerate(questions)}
        response = self.client.post("/quiz", data=answers, follow_redirects=True)
        page = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("ESTJ", page)
        self.assertIn("The Coordinator", page)
        self.assertIn("100%", page)

    def test_feedback_confirmation_escapes_the_name(self):
        response = self.client.post(
            "/feedback",
            data={"name": "<Jake>", "message": "Looks good"},
            follow_redirects=True,
        )
        page = response.get_data(as_text=True)
        self.assertIn("&lt;Jake&gt;", page)
        self.assertNotIn("<Jake>", page)


if __name__ == "__main__":
    unittest.main()
