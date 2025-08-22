from rest_framework import serializers
from .models import Person
from results.models import Result


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"
        read_only_fields = ["id"]


class ResultProfileSerializer(serializers.ModelSerializer):
    competition_name = serializers.CharField(source="competition.name")
    competition_id = serializers.IntegerField(source="competition.id")
    date = serializers.DateField(source="competition.date")
    times = serializers.SerializerMethodField()

    class Meta:
        model = Result
        fields = [
            "competition_name",
            "competition_id",
            "date",
            "times",
            "single",
            "average",
        ]
        read_only_fields = [
            "competition_name",
            "competition_id",
            "date",
            "times",
            "single",
            "average",
        ]

    def get_times(self, obj):
        return obj.get_times()
