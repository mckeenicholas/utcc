from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator


class Person(models.Model):
    name = models.CharField(max_length=255, validators=[MinLengthValidator(1)])
    is_uoft_student = models.BooleanField(default=True)

    def clean(self):
        if not self.name or not self.name.strip():
            raise ValidationError("Name cannot be empty")
        self.name = self.name.strip()

    def __str__(self):
        type = "Yes" if self.is_uoft_student else "No"
        return f"{self.name} | ID: {self.id} | UofT Student: {type}"
