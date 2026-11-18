
from rest_framework import serializers

from .models import (
    SystemARecord,
    SystemBRecord,
    ReconciliationResult
)


class SystemARecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemARecord
        fields = "__all__"


class SystemBRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemBRecord
        fields = "__all__"


class ReconciliationResultSerializer(serializers.ModelSerializer):

    system_a = SystemARecordSerializer(read_only=True)
    system_b = SystemBRecordSerializer(read_only=True)

    class Meta:
        model = ReconciliationResult
        fields = "__all__"
