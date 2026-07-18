from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("results", "0013_alter_result_event"),
    ]

    operations = [
        migrations.AddField(
            model_name="competition",
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
    ]
