from rest_framework import serializers
from .models import Database, Claim, Evidence, Annotation

class DatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Database
        fields = "__all__"

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = "__all__"

class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = "__all__"

class ClaimEvidenceSerializer(serializers.ModelSerializer):
    evidences = EvidenceSerializer(many=True)

    class Meta:
        model = Claim
        fields = '__all__'
