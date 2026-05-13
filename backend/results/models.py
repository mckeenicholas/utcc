from django.core.validators import MinValueValidator
from django.db import models

from users.models import Person

THREE_ATTEMPT_EVENTS = set(["666", "777", "333bf", "444bf", "555bf", "333fm"])


class CompetitionSession(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()

    def __str__(self):
        return f"{self.name}"


class Competition(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    session = models.ForeignKey(CompetitionSession, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} - {self.date}"


class Result(models.Model):
    class Event(models.TextChoices):
        C333 = "333", "3x3x3 Cube"
        C222 = "222", "2x2x2 Cube"
        C444 = "444", "4x4x4 Cube"
        C555 = "555", "5x5x5 Cube"
        C666 = "666", "6x6x6 Cube"
        C777 = "777", "7x7x7 Cube"
        C333BF = "333bf", "3x3x3 Blindfolded"
        C333FM = "333fm", "3x3x3 Fewest Moves"
        C333OH = "333oh", "3x3x3 One-handed"
        MINX = "minx", "Megaminx"
        PYRAM = "pyram", "Pyraminx"
        CLOCK = "clock", "Clock"
        SKEWB = "skewb", "Skewb"
        SQ1 = "sq1", "Square-One"
        C444BF = "444bf", "4x4x4 Blindfolded"
        C555BF = "555bf", "5x5x5 Blindfolded"

    class SpecialTime(models.IntegerChoices):
        DNF = -1, "DNF"
        DNS = -2, "DNS"
        NOT_ATTEMPTED = 0, "Not Attempted"

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, related_name="results", on_delete=models.CASCADE)
    event = models.CharField(max_length=10, choices=Event.choices)
    round = models.IntegerField(validators=[MinValueValidator(1)])

    time1 = models.IntegerField(
        default=SpecialTime.NOT_ATTEMPTED, validators=[MinValueValidator(-2)]
    )
    time2 = models.IntegerField(
        default=SpecialTime.NOT_ATTEMPTED, validators=[MinValueValidator(-2)]
    )
    time3 = models.IntegerField(
        default=SpecialTime.NOT_ATTEMPTED, validators=[MinValueValidator(-2)]
    )
    time4 = models.IntegerField(
        default=SpecialTime.NOT_ATTEMPTED, validators=[MinValueValidator(-2)]
    )
    time5 = models.IntegerField(
        default=SpecialTime.NOT_ATTEMPTED, validators=[MinValueValidator(-2)]
    )

    single = models.IntegerField(
        null=True,
        blank=True,
        help_text="Best single time in centiseconds (calculated automatically)",
    )
    average = models.IntegerField(
        null=True,
        blank=True,
        help_text="Attempt average/mean time in centiseconds (calculated automatically)",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["person", "competition", "event", "round"],
                name="unique_result_per_person",
            )
        ]

    def __str__(self):
        return f"{self.person.name}: ({self.competition.date} - {self.get_event_display()} - Round {self.round})"

    def get_times(self):
        if self.event in THREE_ATTEMPT_EVENTS:
            return [self.time1, self.time2, self.time3]
        else:
            return [self.time1, self.time2, self.time3, self.time4, self.time5]

    @staticmethod
    def sort_key(time):
        return float("inf") if time < 0 else time

    def calculate_single_and_average(self):
        times = self.get_times()
        valid_times = [t for t in times if t > 0]
        dnf_count = sum(1 for t in times if t < 0)

        # Calculate single
        if not valid_times:
            self.single = self.SpecialTime.DNF if dnf_count > 0 else self.SpecialTime.NOT_ATTEMPTED
        else:
            self.single = min(valid_times)

        # Calculate average
        num_attempts = len(times)
        if num_attempts == 3:  # Mean of 3
            if dnf_count > 0 or any(t == 0 for t in times):
                self.average = self.SpecialTime.DNF
            else:
                self.average = round(sum(times) / 3)
        else:  # Average of 5
            if dnf_count >= 2 or any(t == 0 for t in times):
                self.average = self.SpecialTime.DNF
            else:
                sorted_times = sorted(times, key=self.sort_key)
                trimmed_sum = sum(sorted_times[1:-1])
                self.average = round(trimmed_sum / 3)

    def save(self, *args, **kwargs):
        self.calculate_single_and_average()
        super().save(*args, **kwargs)
