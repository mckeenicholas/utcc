from django.db import migrations


def populate_person_foreign_keys(apps, schema_editor) -> None:
    Result = apps.get_model("results", "Result")
    Person = apps.get_model("users", "Person")

    person_cache = {}

    for result in Result.objects.filter(person_id__isnull=True).iterator():
        if not result.name:
            continue

        if result.name in person_cache:
            person = person_cache[result.name]
        else:
            person, created = Person.objects.get_or_create(name=result.name)

            person_cache[result.name] = person

        result.person_id = person
        result.save(update_fields=["person_id"])


def unpopulate_person_foreign_keys(apps, schema_editor) -> None:
    Result = apps.get_model("results", "Result")
    Result.objects.update(person_id=None)


class Migration(migrations.Migration):
    dependencies = [
        ("results", "0006_result_person_id"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            populate_person_foreign_keys,
            reverse_code=unpopulate_person_foreign_keys,
        ),
    ]
