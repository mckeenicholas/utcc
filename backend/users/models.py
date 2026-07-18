from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models


class StudentDesignator(models.TextChoices):
    UTSG = "UTSG", "UTSG"
    UTM = "UTM", "UTM"
    UTSC = "UTSC", "UTSC"
    NON_UOFT = "Non-UofT", "Non-UofT"


class Person(models.Model):
    name = models.CharField(max_length=255, validators=[MinLengthValidator(1)])
    student_designator = models.CharField(
        max_length=20,
        choices=StudentDesignator.choices,
        default=StudentDesignator.UTSG,
    )

    def __str__(self) -> str:
        return f"{self.name} | ID: {self.id} | Designator: {self.student_designator}"

    def clean(self) -> None:
        if not self.name or not self.name.strip():
            msg = "Name cannot be empty"
            raise ValidationError(msg)
        self.name = self.name.strip()
