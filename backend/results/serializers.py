from rest_framework import serializers

from scrambles.serializers import CompetitionScramblesSerializer
from .models import Competition, CompetitionSession, Result


class CompetitionSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionSession
        fields = "__all__"
        read_only_fields = ["id"]


class CompetitionSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()
    session_name = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        fields = ["id", "name", "date", "events", "session", "session_name"]
        read_only_fields = ["id", "events", "session_name"]

    def get_events(self, obj):
        return sorted(list({result.event for result in obj.results.all()}))

    def get_session_name(self, obj):
        if obj.session:
            return obj.session.name
        return None


class ResultCreateUpdateSerializer(serializers.ModelSerializer):
    person_name = serializers.CharField(source="person.name", read_only=True)
    person_id = serializers.IntegerField(source="person.id", read_only=True)

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
    person_name = serializers.CharField(source="person.name", read_only=True)
    person_id = serializers.IntegerField(source="person.id", read_only=True)
    is_uoft_student = serializers.BooleanField(
        source="person.is_uoft_student", read_only=True
    )

    class Meta:
        model = Result
        fields = [
            "id",
            "person_id",
            "times",
            "single",
            "average",
            "person_name",
            "is_uoft_student",
        ]

    def get_times(self, obj):
        return obj.get_times()


class RoundSerializer(serializers.Serializer):
    round = serializers.IntegerField()
    results = ResultPersonSerializer(many=True)
    scramble_sets = CompetitionScramblesSerializer(many=True)


class EventSerializer(serializers.Serializer):
    event = serializers.CharField()
    rounds = RoundSerializer(many=True)


class FullCompetitionResultsSerializer(serializers.Serializer):
    competition = CompetitionSerializer()
    results = EventSerializer(many=True)


class RecordDetailSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()
    times_list = serializers.SerializerMethodField()
    person_name = serializers.CharField(source="person.name")
    person_id = serializers.IntegerField(source="person.id")
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
