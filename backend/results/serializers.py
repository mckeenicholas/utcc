from rest_framework import serializers
from .models import Competition, Result


class CompetitionSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        fields = ["id", "name", "date", "events"]
        read_only_fields = ["id", "events"]

    def get_events(self, obj):
        events = (
            Result.objects.filter(competition=obj)
            .values_list("event", flat=True)
            .distinct()
            .order_by("event")
        )
        return list(events)


class ResultCreateUpdateSerializer(serializers.ModelSerializer):
    person_name = serializers.CharField(source="person_id.name", read_only=True)
    
    class Meta:
        model = Result
        fields = [
            "id",
            "person_id",
            "person_name",
            "competition",
            "event",
            "round",
            "time1",
            "time2",
            "time3",
            "time4",
            "time5",
            "single",
            "average",
        ]
        read_only_fields = ["id", "single", "average", "person_name"]


class ResultPersonSerializer(serializers.ModelSerializer):
    times = serializers.SerializerMethodField()
    person_name= serializers.CharField(source="person_id.name", read_only=True)

    class Meta:
        model = Result
        fields = ["id", "person_id", "times", "single", "average", "person_name"]

    def get_times(self, obj):
        return obj.get_times()


class RoundSerializer(serializers.Serializer):
    round = serializers.IntegerField()
    results = ResultPersonSerializer(many=True)


class EventSerializer(serializers.Serializer):
    event = serializers.CharField()
    rounds = RoundSerializer(many=True)


class CompetitionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ["name", "date"]


class FullCompetitionResultsSerializer(serializers.Serializer):
    competition = CompetitionDetailSerializer()
    results = EventSerializer(many=True)


class RecordDetailSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()
    times_list = serializers.SerializerMethodField()
    person_name = serializers.CharField(source="person_id.name")
    person_id = serializers.IntegerField(source="person_id.id")
    competition_name = serializers.CharField(source="competition.name")
    competition_id = serializers.IntegerField(source="competition.id")

    class Meta:
        model = Result
        fields = [
            "result",
            "times_list",
            "person_name",
            "person_id",
            "competition_name",
            "competition_id",
        ]

    def get_times_list(self, obj):
        return obj.get_times()

    def get_result(self, obj):
        record_type = self.context.get("record_type")
        if record_type == "single":
            return obj.single
        elif record_type == "average":
            return obj.average
        return None
