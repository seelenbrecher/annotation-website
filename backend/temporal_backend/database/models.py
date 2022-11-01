from uuid import uuid4
from django.utils import timezone
from django.db import models
from user.models import CustomUser

# Owner, name combi must be unique
class Database(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    accesskey = models.CharField(max_length=50)
    is_temporal= models.BooleanField()
    is_active= models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = ['owner', 'name', 'description', 'accesskey', 'is_temporal', 'is_active']

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'name'], name="labeller_database_unique")
        ]

    def __str__(self):
        return self.name

# Database and Claim content combi must be unique, no same claim in same database
class Claim(models.Model):
    database = models.ForeignKey(Database, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    original_id = models.IntegerField()
    initial_label= models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['database', 'content'], name="labeller_claim_unique")
        ]

    def __str___(self):
            return self.name

# claim and temporal_content must be unique
class TemporalClaimSection(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    temporal_content = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['claim', 'temporal_content'], name="labeller_temporal_claim_section_unique")
        ]

# Claim and content must be unique
class Evidence(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name="evidences")
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['claim', 'content'], name="labeller_evidence_unique")
        ]

# Annotation
class Annotation(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name="annotation")
    annotator_email = models.CharField(max_length=100)
    annotator_temporal_flag = models.BooleanField()
    temporal_label = models.CharField(max_length=30)
    general_label = models.CharField(max_length=30)
    overall_label = models.CharField(max_length=30)
    annotated_at = models.DateTimeField(default=timezone.now)
    manual_review_flag = models.BooleanField(default=False)
    manual_review_comments = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['claim', 'annotator_email'], name="annotation_unique")
        ]

# Justification
class Justification(models.Model):
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)
    # True means temporal, False means general
    temporal = models.BooleanField()
    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE, blank=True, null=True)
    justification = models.CharField(max_length=100)


