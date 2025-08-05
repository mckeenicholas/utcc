from rest_framework import serializers
from .models import Competition, Result


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ["id", "name", "date"]
        read_only_fields = ["id"]


class ResultCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = [
            "id",
            "name",
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
        # 'id', 'single', and 'average' are not expected in the input payload.
        read_only_fields = ["id", "single", "average"]


class ResultPersonSerializer(serializers.ModelSerializer):
    times = serializers.SerializerMethodField()

    class Meta:
        model = Result
        fields = ["id", "name", "times", "single", "average"]

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
    person = serializers.CharField(source="name")
    competition_name = serializers.CharField(source="competition.name")
    competition_id = serializers.IntegerField(source="competition.id")

    class Meta:
        model = Result
        fields = [
            "result",
            "times_list",
            "person",
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
