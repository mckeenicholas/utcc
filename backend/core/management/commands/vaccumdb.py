from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Run VACUUM on the database (supports --full for VACUUM FULL on Postgres)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--full",
            action="store_true",
            help="Run a full vacuum (PostgreSQL only).",
        )

    def handle(self, *args, **options):
        full = options["full"]

        if full:
            self.stdout.write(self.style.WARNING("Running VACUUM FULL on database..."))
            sql = "VACUUM FULL;"
        else:
            self.stdout.write(self.style.WARNING("Running VACUUM on database..."))
            sql = "VACUUM;"

        with connection.cursor() as cursor:
            cursor.execute(sql)

        self.stdout.write(self.style.SUCCESS("VACUUM completed."))
