from rest_framework import serializers
from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=255,
        help_text="Person's full name",
    )

    class Meta:
        model = Person
        fields = ["id", "name", "is_uoft_student"]
        read_only_fields = ["id"]

    def validate_name(self, value):
        """Ensure name is not just whitespace."""
        named_stripped = value.strip()
        if not value or named_stripped:
            raise serializers.ValidationError("Name cannot be empty or just whitespace")
        return named_stripped
