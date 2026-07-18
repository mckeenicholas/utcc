from django.db import migrations, models


def migrate_uoft_status(apps, schema_editor) -> None:
    Person = apps.get_model("users", "Person")
    for person in Person.objects.all():
        if person.is_uoft_student:
            person.student_designator = "UTSG"
        else:
            person.student_designator = "Non-UofT"
        person.save()


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_person_is_uoft_student_alter_person_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="student_designator",
            field=models.CharField(
                max_length=20,
                choices=[
                    ("UTSG", "UTSG"),
                    ("UTM", "UTM"),
                    ("UTSC", "UTSC"),
                    ("Non-UofT", "Non-UofT"),
                ],
                default="UTSG",
            ),
        ),
        migrations.RunPython(migrate_uoft_status),
        migrations.RemoveField(
            model_name="person",
            name="is_uoft_student",
        ),
    ]
