from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=255)
    is_uoft_student = models.BooleanField()

    def __str__(self):
        type = "UofT Student" if self.is_uoft_student else "Non-Uoft Student"
        return f"{self.name} | ID: {self.id} | Status: {type}"
