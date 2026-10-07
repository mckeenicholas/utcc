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


class BlindfoldedResultModelTests(TestCase):
    def setUp(self):
        self.person = Person.objects.create(name="BF Solver", student_designator="UTSG")
        self.comp = Competition.objects.create(
            name="UTCC Open 2026",
            date=timezone.localdate(),
            student_designator="UTSG",
        )

    def test_333bf_5_attempts_calculates_single_and_average(self):
        result = Result.objects.create(
            person=self.person,
            competition=self.comp,
            event="333bf",
            round=1,
            time1=3000,
            time2=2500,
            time3=3200,
            time4=2800,
            time5=2700,
        )
        self.assertEqual(len(result.get_times()), 5)
        self.assertEqual(result.single, 2500)
        # Trimmed middle 3: 2700, 2800, 3000 -> 8500 / 3 = 2833
        self.assertEqual(result.average, 2833)

    def test_333bf_1_dnf_calculates_average(self):
        result = Result.objects.create(
            person=self.person,
            competition=self.comp,
            event="333bf",
            round=1,
            time1=3000,
            time2=-1,
            time3=3200,
            time4=2800,
            time5=2700,
        )
        self.assertEqual(result.single, 2700)
        # DNF dropped as worst, 2700 dropped as best -> middle 3: 2800, 3000, 3200 -> 3000
        self.assertEqual(result.average, 3000)

    def test_333bf_2_dnfs_gives_dnf_average(self):
        result = Result.objects.create(
            person=self.person,
            competition=self.comp,
            event="333bf",
            round=1,
            time1=3000,
            time2=-1,
            time3=-1,
            time4=2800,
            time5=2700,
        )
        self.assertEqual(result.single, 2700)
        self.assertEqual(result.average, Result.SpecialTime.DNF)

    def test_333bf_fewer_than_5_attempts_single_calculated_average_not_attempted(self):
        result = Result.objects.create(
            person=self.person,
            competition=self.comp,
            event="333bf",
            round=1,
            time1=2500,
            time2=0,
            time3=0,
            time4=0,
            time5=0,
        )
        self.assertEqual(result.single, 2500)
        self.assertEqual(result.average, Result.SpecialTime.NOT_ATTEMPTED)


class CompetitionRoundRankingsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.person_a = Person.objects.create(name="Alice", student_designator="UTSG")
        self.person_b = Person.objects.create(name="Bob", student_designator="UTSG")
        self.person_c = Person.objects.create(name="Charlie", student_designator="UTSG")

        self.comp = Competition.objects.create(
            name="UTCC Blind Tournament 2026",
            date=timezone.localdate(),
            student_designator="UTSG",
        )

    def test_333bf_round_results_sorted_by_single_primarily(self):
        # Alice: single 2500, average DNF (-1)
        Result.objects.create(
            person=self.person_a,
            competition=self.comp,
            event="333bf",
            round=1,
            time1=2500,
            time2=-1,
            time3=-1,
            time4=2600,
            time5=2700,
        )
        # Bob: single 3000, average 3200
        Result.objects.create(
            person=self.person_b,
            competition=self.comp,
            event="333bf",
            round=1,
            time1=3000,
            time2=3100,
            time3=3200,
            time4=3300,
            time5=3400,
        )
        # Charlie: single 2500, average 2800
        Result.objects.create(
            person=self.person_c,
            competition=self.comp,
            event="333bf",
            round=1,
            time1=2500,
            time2=2700,
            time3=2800,
            time4=2900,
            time5=3000,
        )

        response = self.client.get(f"/api/competitions/{self.comp.id}/results/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        bf_round = data["results"][0]["rounds"][0]["results"]
        # Charlie (2500, avg 2800) 1st, Alice (2500, avg DNF) 2nd, Bob (3000, avg 3200) 3rd
        self.assertEqual(bf_round[0]["person"], self.person_c.id)
        self.assertEqual(bf_round[1]["person"], self.person_a.id)
        self.assertEqual(bf_round[2]["person"], self.person_b.id)

    def test_333_round_results_sorted_by_average_primarily(self):
        # Normal 333: Alice has faster single (900) but slower average (1200)
        Result.objects.create(
            person=self.person_a,
            competition=self.comp,
            event="333",
            round=1,
            time1=900,
            time2=1200,
            time3=1200,
            time4=1200,
            time5=1500,
        )
        # Bob has slower single (1000) but faster average (1100)
        Result.objects.create(
            person=self.person_b,
            competition=self.comp,
            event="333",
            round=1,
            time1=1000,
            time2=1100,
            time3=1100,
            time4=1100,
            time5=1200,
        )

        response = self.client.get(f"/api/competitions/{self.comp.id}/results/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        cube_round = next(r for r in data["results"] if r["event"] == "333")["rounds"][0]["results"]
        # Bob (avg 1100) 1st, Alice (avg 1200) 2nd
        self.assertEqual(cube_round[0]["person"], self.person_b.id)
        self.assertEqual(cube_round[1]["person"], self.person_a.id)


class RankingsAPIViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.person_a = Person.objects.create(name="Alice", student_designator="UTSG")
        self.person_b = Person.objects.create(name="Bob", student_designator="UTSG")
        self.comp = Competition.objects.create(
            name="UTCC Open 2026",
            date=timezone.localdate(),
            student_designator="UTSG",
        )
        # Alice: single 2500, average 2900
        Result.objects.create(
            person=self.person_a,
            competition=self.comp,
            event="333bf",
            round=1,
            time1=2500,
            time2=2800,
            time3=2900,
            time4=3000,
            time5=3100,
        )
        # Bob: single 2200, average 3200
        Result.objects.create(
            person=self.person_b,
            competition=self.comp,
            event="333bf",
            round=1,
            time1=2200,
            time2=3100,
            time3=3200,
            time4=3300,
            time5=3400,
        )

    def test_333bf_single_rankings(self):
        response = self.client.get("/api/rankings/", {"event": "333bf", "type": "single"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertEqual(len(results), 2)
        # Bob (2200) rank 1, Alice (2500) rank 2
        self.assertEqual(results[0]["person"], self.person_b.id)
        self.assertEqual(results[0]["rank"], 1)
        self.assertEqual(results[0]["result"], 2200)
        self.assertEqual(results[1]["person"], self.person_a.id)
        self.assertEqual(results[1]["rank"], 2)
        self.assertEqual(results[1]["result"], 2500)

    def test_333bf_average_rankings(self):
        response = self.client.get("/api/rankings/", {"event": "333bf", "type": "average"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertEqual(len(results), 2)
        # Alice (2900) rank 1, Bob (3200) rank 2
        self.assertEqual(results[0]["person"], self.person_a.id)
        self.assertEqual(results[0]["rank"], 1)
        self.assertEqual(results[0]["result"], 2900)
        self.assertEqual(results[1]["person"], self.person_b.id)
        self.assertEqual(results[1]["rank"], 2)
        self.assertEqual(results[1]["result"], 3200)


class FTOTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.person_a = Person.objects.create(
            name="Alice Solver",
            student_designator="UTSG",
        )
        self.person_b = Person.objects.create(
            name="Bob Octa",
            student_designator="UTSG",
        )
        self.comp = Competition.objects.create(
            name="UTCC Octahedral 2026",
            date=timezone.localdate(),
            student_designator="UTSG",
        )

    def test_fto_model_solves_and_ao5_calculation(self):
        # 5 solves: 3000, 2500 (best), 3500 (worst), 2800, 3200
        # Trimmed: 2800, 3000, 3200 -> mean = 3000
        result = Result.objects.create(
            person=self.person_a,
            competition=self.comp,
            event="fto",
            round=1,
            time1=3000,
            time2=2500,
            time3=3500,
            time4=2800,
            time5=3200,
        )
        self.assertEqual(result.single, 2500)
        self.assertEqual(result.average, 3000)

    def test_fto_round_results_sorted_by_average_primarily(self):
        # Alice: single 2500, average 3000
        Result.objects.create(
            person=self.person_a,
            competition=self.comp,
            event="fto",
            round=1,
            time1=3000,
            time2=2500,
            time3=3500,
            time4=2800,
            time5=3200,
        )
        # Bob: single 2000 (faster single), average 3500 (slower average)
        Result.objects.create(
            person=self.person_b,
            competition=self.comp,
            event="fto",
            round=1,
            time1=2000,
            time2=3400,
            time3=3500,
            time4=3600,
            time5=4000,
        )
        response = self.client.get(f"/api/competitions/{self.comp.id}/results/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["event"], "fto")
        round_results = results[0]["rounds"][0]["results"]
        self.assertEqual(len(round_results), 2)
        # Alice ranks 1 (avg 3000), Bob ranks 2 (avg 3500) because FTO is average-primary
        self.assertEqual(round_results[0]["person"], self.person_a.id)
        self.assertEqual(round_results[1]["person"], self.person_b.id)

    def test_fto_scramble_generation_not_supported(self):
        from django.contrib.auth.models import User

        user = User.objects.create_user(username="admin", password="password")
        self.client.force_authenticate(user=user)
        response = self.client.post(
            f"/api/scrambles/{self.comp.id}/fto/1/generate/",
            {"count": 5, "numSets": 1},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Scrambles are not supported", response.json().get("error", ""))
