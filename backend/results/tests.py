from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from results.models import Competition, Result
from results.utils import is_falsy_param, is_truthy_param
from users.models import Person


class ParamUtilsTests(TestCase):
    def test_truthy_param(self):
        self.assertTrue(is_truthy_param("true"))
        self.assertTrue(is_truthy_param("True"))
        self.assertTrue(is_truthy_param("TRUE"))
        self.assertTrue(is_truthy_param("1"))
        self.assertTrue(is_truthy_param("t"))
        self.assertTrue(is_truthy_param("T"))
        self.assertTrue(is_truthy_param("yes"))
        self.assertTrue(is_truthy_param("YES"))
        self.assertTrue(is_truthy_param("y"))
        self.assertTrue(is_truthy_param(True))
        self.assertTrue(is_truthy_param(1))

        self.assertFalse(is_truthy_param("false"))
        self.assertFalse(is_truthy_param("0"))
        self.assertFalse(is_truthy_param("no"))
        self.assertFalse(is_truthy_param(None))
        self.assertFalse(is_truthy_param(""))
        self.assertFalse(is_truthy_param(False))
        self.assertFalse(is_truthy_param(0))
        self.assertFalse(is_truthy_param("random"))

    def test_falsy_param(self):
        self.assertTrue(is_falsy_param("false"))
        self.assertTrue(is_falsy_param("False"))
        self.assertTrue(is_falsy_param("FALSE"))
        self.assertTrue(is_falsy_param("0"))
        self.assertTrue(is_falsy_param("f"))
        self.assertTrue(is_falsy_param("F"))
        self.assertTrue(is_falsy_param("no"))
        self.assertTrue(is_falsy_param("NO"))
        self.assertTrue(is_falsy_param("n"))
        self.assertTrue(is_falsy_param(False))
        self.assertTrue(is_falsy_param(0))

        self.assertFalse(is_falsy_param("true"))
        self.assertFalse(is_falsy_param("1"))
        self.assertFalse(is_falsy_param("yes"))
        self.assertFalse(is_falsy_param(None))
        self.assertFalse(is_falsy_param(""))
        self.assertFalse(is_falsy_param(True))
        self.assertFalse(is_falsy_param(1))
        self.assertFalse(is_falsy_param("random"))


class CompetitionUpcomingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        today = timezone.localdate()

        self.person = Person.objects.create(
            name="Test Solver",
            student_designator="UTSG",
        )

        self.past_comp = Competition.objects.create(
            name="Past Tournament 2025",
            date=today - timedelta(days=14),
            student_designator="UTSG",
        )
        self.soon_comp = Competition.objects.create(
            name="Upcoming Tournament Soon",
            date=today + timedelta(days=5),
            student_designator="UTSC",
        )
        self.later_comp = Competition.objects.create(
            name="Upcoming Tournament Later",
            date=today + timedelta(days=25),
            student_designator="UTM",
        )

        # Add a result only to past_comp
        self.result = Result.objects.create(
            person=self.person,
            competition=self.past_comp,
            event="333",
            round=1,
            time1=1200,
            time2=1300,
            time3=1100,
            time4=1400,
            time5=1250,
            single=1100,
            average=1250,
        )

    def test_upcoming_competitions_filter(self):
        response = self.client.get("/api/competitions/", {"upcoming": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        results = data.get("results", data)
        self.assertEqual(len(results), 2)
        # Should be ordered by date ascending (soonest first)
        self.assertEqual(results[0]["id"], self.soon_comp.id)
        self.assertEqual(results[1]["id"], self.later_comp.id)

    def test_past_competitions_filter(self):
        response = self.client.get("/api/competitions/", {"upcoming": "false"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        results = data.get("results", data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.past_comp.id)

    def test_all_competitions_unfiltered(self):
        response = self.client.get("/api/competitions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        results = data.get("results", data)
        self.assertEqual(len(results), 3)

    def test_has_results_filter_true(self):
        response = self.client.get("/api/competitions/", {"has_results": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        results = data.get("results", data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.past_comp.id)
        self.assertTrue(results[0]["has_results"])
        self.assertEqual(results[0]["events"], ["333"])

    def test_has_results_filter_false(self):
        response = self.client.get("/api/competitions/", {"has_results": "false"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        results = data.get("results", data)
        self.assertEqual(len(results), 2)
        result_ids = {r["id"] for r in results}
        self.assertIn(self.soon_comp.id, result_ids)
        self.assertIn(self.later_comp.id, result_ids)
        for r in results:
            self.assertFalse(r["has_results"])
            self.assertEqual(r["events"], [])

    def test_latest_competition_results_prioritizes_comp_with_results(self):
        # Even though soon_comp and later_comp have later dates,
        # latest/results/ should return past_comp because it actually has results.
        response = self.client.get("/api/competitions/latest/results/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["competition"]["id"], self.past_comp.id)
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["event"], "333")
