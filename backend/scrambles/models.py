from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from results.models import Competition, Result


class ScrambleSet(models.Model):
    competition = models.ForeignKey(
        Competition, related_name="scramble_sets", on_delete=models.CASCADE
    )
    event = models.CharField(max_length=10, choices=Result.Event.choices)
    round = models.IntegerField(validators=[MinValueValidator(1)])
    scramble_set = models.IntegerField(validators=[MinValueValidator(1)])

    generated_on = models.DateTimeField(default=timezone.now)
    visible = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "competition",
                    "event",
                    "round",
                    "scramble_set",
                ],
                name="unique_scramble_set_per_competition_event_round",
            )
        ]

    def __str__(self):
        return f"{self.competition.name}: ({self.get_event_display()}, Round {self.round}, Set {self.scramble_set})"


class Scramble(models.Model):
    scramble_set = models.ForeignKey(
        ScrambleSet, related_name="scrambles", on_delete=models.CASCADE
    )
    scramble_num = models.IntegerField(validators=[MinValueValidator(-2)])
    scramble = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "scramble_set",
                    "scramble_num",
                ],
                name="unique_scramble_per_set",
            )
        ]

    def __str__(self):
        scramble_name = (
            str(self.scramble_num) if self.scramble_num > 0 else f"E{-self.scramble_num}"
        )
        return f"{self.scramble_set}: Scramble {scramble_name}"
