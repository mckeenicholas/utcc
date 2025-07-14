from django.db import models

THREE_ATTEMPT_EVENTS = ["666", "777", "333bf", "444bf", "555bf", "333fm"]


class Competition(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.date}"


class Result(models.Model):
    EVENT_CHOICES = (
        ("222", "2x2x2 Cube"),
        ("333", "3x3x3 Cube"),
        ("444", "4x4x4 Cube"),
        ("555", "5x5x5 Cube"),
        ("666", "6x6x6 Cube"),
        ("777", "7x7x7 Cube"),
        ("333bf", "3x3x3 Blindfolded"),
        ("333fm", "3x3x3 Fewest Moves"),
        ("333oh", "3x3x3 One-handed"),
        ("minx", "Megaminx"),
        ("pyram", "Pyraminx"),
        ("clock", "Clock"),
        ("skewb", "Skewb"),
        ("sq1", "Square One"),
        ("444bf", "4x4x4 Blindfolded"),
        ("555bf", "5x5x5 Blindfolded"),
    )

    name = models.CharField(max_length=255)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    event = models.CharField(max_length=10, choices=EVENT_CHOICES)
    round = models.IntegerField()

    time1 = models.IntegerField()
    time2 = models.IntegerField()
    time3 = models.IntegerField()
    time4 = models.IntegerField()
    time5 = models.IntegerField()

    single = models.IntegerField(
        null=True, blank=True, help_text="Best single time in centiseconds"
    )
    average = models.IntegerField(
        null=True, blank=True, help_text="Attempt average/mean time"
    )

    def __str__(self):
        return f"{self.name}: {self.event} Round {self.round} - {self.competition.date}"

    def get_times(self):
        if self.event in THREE_ATTEMPT_EVENTS:
            return [self.time1, self.time2, self.time3]
        else:
            return [self.time1, self.time2, self.time3, self.time4, self.time5]

    @staticmethod
    def dnf_aware_sort_key(time):
        return float("inf") if time < 0 else time

    def calculate_single_and_average(self):
        times = self.get_times()

        if all(t == 0 for t in times):
            self.single = 0
            self.average = 0
            return

        non_dnf_times = [t for t in times if t > 0]
        self.single = min(non_dnf_times) if non_dnf_times else -1

        is_three_attempt = self.event in THREE_ATTEMPT_EVENTS

        if any(t == 0 for t in times):
            self.average = 0
            return

        num_dnfs = sum(1 for t in times if t < 0)

        if is_three_attempt:
            if num_dnfs > 0:
                self.average = -1
            else:
                average_sum = sum(times)
                self.average = int(average_sum / 3 + 0.5)
            return

        if num_dnfs >= 2:
            self.average = -1
            return

        sorted_times = sorted(times, key=self.dnf_aware_sort_key)

        trimmed_times = sorted_times[1:-1]
        average_sum = sum(trimmed_times)
        self.average = int(average_sum / 3 + 0.5)

    def save(self, *args, **kwargs):
        self.calculate_single_and_average()
        super().save(*args, **kwargs)
