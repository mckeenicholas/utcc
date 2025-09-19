from rest_framework import serializers

from .models import Scramble, ScrambleSet


class ScrambleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scramble
        fields = "__all__"
        read_only_fields = ["id"]


class ScrambleSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrambleSet
        fields = "__all__"
        read_only_fields = ["id"]


class CompetitionScramblesSerializer(serializers.ModelSerializer):
    scrambles = ScrambleSerializer(many=True, read_only=True)

    class Meta:
        model = ScrambleSet
        fields = ["scrambles"]
        read_only_fields = ["id"]
