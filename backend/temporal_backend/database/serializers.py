from rest_framework import serializers
from .models import Database, Claim, Evidence, Annotation, Justification

class DatabaseSerializer(serializers.ModelSerializer):
    num_claims = serializers.SerializerMethodField()

    def get_num_claims(self, obj):
        try:
            return obj.num_claims
        except:
            return None

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

class JusstificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Justification
        fields = '__all__'

class AnnotationSerializer(serializers.ModelSerializer):
    claim = ClaimEvidenceSerializer(many=False)
    justifications = JusstificationSerializer(many=True)
    class Meta:
        model = Annotation
        fields = '__all__'

