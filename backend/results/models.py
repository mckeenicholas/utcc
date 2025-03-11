from django.db import models
from django.utils import timezone


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

    def __str__(self):
        return f"{self.name} - {self.event} - {self.competition.date}"

    def get_times(self):
        return [
            self.time1,
            self.time2,
            self.time3,
            self.time4,
            self.time5,
        ]
