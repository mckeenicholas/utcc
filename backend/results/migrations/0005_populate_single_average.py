# Data migration to populate single and average for existing records

from django.db import migrations


def populate_single_average(apps, schema_editor) -> None:
    Result = apps.get_model("results", "Result")

    for result in Result.objects.all():
        result.save()


def reverse_populate_single_average(apps, schema_editor) -> None:
    Result = apps.get_model("results", "Result")
    Result.objects.update(single=None, average=None)


class Migration(migrations.Migration):
    dependencies = [
        ("results", "0004_result_average_result_single"),
    ]

    operations = [
        migrations.RunPython(populate_single_average, reverse_populate_single_average),
    ]
