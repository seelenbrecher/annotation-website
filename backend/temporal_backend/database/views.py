from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
from database.serializers import DatabaseSerializer, ClaimSerializer, ClaimEvidenceSerializer, AnnotationSerializer
from database.models import Database, Claim, Evidence, TemporalClaimSection, Annotation, Justification
from user.models import CustomUser
import bcrypt
from django.db.models import Count
from django.http import JsonResponse
import json

# Generate database's secure accesskey with a salt
def hash_new_password(password):
    """
    Hash the provided password with a randomly-generated salt and return the
    salt and hash to store in the database.
    """
    bytePwd = password.encode('utf-8')
    # Generate salt
    mySalt = bcrypt.gensalt()
    # Hash password
    hash = bcrypt.hashpw(bytePwd, mySalt)   
    return hash.decode('utf-8')

def is_correct_password(pw_hash, password):
    """
    Given a previously-stored salt and hash, and a password provided by a user
    trying to log in, check whether the password is correct.
    """
    return bcrypt.checkpw(password.encode('utf-8'), pw_hash.encode('utf-8'))

# Check annotation password matches
class CheckAnnotationAPIView(APIView):
    # Disable administrator authentication and permission for annotation
    authentication_classes = []
    permission_classes = []
    """This endpoint makes sure users specify a correct access-key."""
    def post(self, request):
            providedKey = request.data.get('accessKey')
            db = request.data.get('databaseId')
            try:
                obj = Database.objects.get(id = db)
            except Database.DoesNotExist:
                raise NotFound("Specified database id does not exist!")
            if (obj.is_active == False):
                raise NotFound("Specified database is not ready for annotation yet.!")
            correct_password = is_correct_password(obj.accesskey, providedKey) 
            return Response({"validated": correct_password})

# Database
class ListDatabaseAPIView(ListAPIView):
    """This endpoint list all of the available databases"""
    queryset = Database.objects.all()
    serializer_class = DatabaseSerializer
    def get_queryset(self):
        """
        Return a list of all the databases
        for the currently authenticated user.
        """
        user = self.request.user
        filtered_queryset = Database.objects.filter(owner=user).annotate(
            num_claims=Count('claim')
        )
        return filtered_queryset
        

class CreateDatabaseAPIView(APIView):
    """This endpoint allows for creation of a database if it does not exist, or just returns the database id if it exists"""
    def post(self, request):
        reqOwner = request.data.get('owner')
        reqName = request.data.get('name')
        reqDescription = request.data.get('description')
        pw_hash = hash_new_password(request.data.get('accesskey'))
        reqIsTemporal = request.data.get('is_temporal')
        user = CustomUser.objects.get(id=reqOwner)

        obj, created = Database.objects.get_or_create(
        owner=user,
        name=reqName,
        defaults={'description': reqDescription, 'accesskey': pw_hash, 'is_temporal': reqIsTemporal})
        return Response({"id": obj.id, "created": created})

class UpdateDatabaseAPIView(UpdateAPIView):
    """This endpoint allows for updating a specific database by passing in the id of the database to update"""
    queryset = Database.objects.all()
    serializer_class = DatabaseSerializer

class DeleteDatabaseAPIView(DestroyAPIView):
    """This endpoint allows for deletion of a specific Database"""
    queryset = Database.objects.all()
    serializer_class = DatabaseSerializer

# Main function to add databases + claims + evidence + temporal arguments to reduce axios calls
class CreateDatabaseClaimEvidenceTemporalAPIView(APIView):
    # Disable administrator authentication and permission for annotation
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        reqNew = request.data.get('new')
        # Create database first
        if reqNew == True:
            reqOwner = request.data.get('owner')
            reqName = request.data.get('name')
            reqDescription = request.data.get('description')
            pw_hash = hash_new_password(request.data.get('accesskey'))
            reqIsTemporal = request.data.get('is_temporal')
            user = CustomUser.objects.get(id=reqOwner)
            databaseObj, databaseCreated = Database.objects.get_or_create(
            owner=user,
            name=reqName,
            defaults={'description': reqDescription, 'accesskey': pw_hash, 'is_temporal': reqIsTemporal})
        else:
            databaseObj = Database.objects.get(id = int(request.data.get('databaseId')))
        # Add Claim
        reqContent = request.data.get('claimContent')
        reqOriginalId = request.data.get('original_id')
        reqInitialLabel = request.data.get('initial_label')
        reqTrainTest = request.data.get('train_test_label')
        claim = Claim(
            database=databaseObj,
            content=reqContent,
            original_id=reqOriginalId,
            initial_label=reqInitialLabel,
            train_test_label=reqTrainTest
        )
        claim.save()
        # Add Temporal Argument
        reqClaim = claim
        reqTemporalContent = json.loads(request.data.get('temporalContent'))
        for temporalArg in reqTemporalContent:  
            obj, created = TemporalClaimSection.objects.get_or_create(
            claim=reqClaim,
            temporal_content=temporalArg)
            
        # Add Evidence
        reqEvidence = json.loads(request.data.get('evidence'))
        reqGoldenEvi = json.loads(request.data.get('golden_evi'))

        for idx in range(len(reqEvidence)):
            obj, created = Evidence.objects.get_or_create(
            claim=reqClaim,
            content=reqEvidence[idx]['evidence_content'],
            defaults={'title': reqEvidence[idx]['evidence_title'], 'golden_evi': reqGoldenEvi[idx]})
        return Response({"databaseId": databaseObj.pk, "claimId": claim.pk, "numTemporal": len(reqTemporalContent) , "numEvidence": len(reqEvidence)})

# Claims
class CreateClaimAPIView(APIView):
    """This endpoint allows for creation of a claim if it does not exist, or just returns the claim id if it exists"""
    def post(self, request):
        reqDatabase = request.data.get('database')
        reqContent = request.data.get('content')
        reqOriginalId = request.data.get('original_id')
        reqInitialLabel = request.data.get('initial_label')
        reqTrainTest = request.data.get('train_test_label')
        getDatabase = Database.objects.get(id=reqDatabase)

        claim = Claim(
            database=Database.objects.get(id=reqDatabase),
            content=reqContent,
            original_id=reqOriginalId,
            initial_label=reqInitialLabel,
            train_test_label=reqTrainTest
        )
        claim.save()

        # obj, created = Claim.objects.get_or_create(
        # database=getDatabase,
        # content=reqContent,
        # defaults={'original_id': reqOriginalId, 'initial_label': reqInitialLabel})
        # return Response({"id": obj.id, "created": created})
        return Response({"id": claim.id})

class ListClaimAPIView(ListAPIView):
    serializer_class = ClaimSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned claims to a given database,
        by filtering against a `databaseId` query parameter in the URL.
        """
        queryset = Claim.objects.all()
        databaseId = self.request.query_params.get('databaseId')
        databaseObj = Database.objects.get(id=databaseId)
        queryset = queryset.filter(database=databaseObj)
        return queryset

# Get single entry for annotation (instead of all for speed)
class ListClaimWithEvidenceAPIView(APIView):
    # Disable administrator authentication and permission for annotation
    authentication_classes = []
    permission_classes = []

    serializer_class = ClaimEvidenceSerializer
    def post(self, request):
        """
        Restricts the returned claims to a given database,
        by filtering against a `databaseId` query parameter in the URL.
        Also ensures that returned results have not been previously annotated already.
        """
        queryset = Claim.objects.all()
        databaseId = request.data.get('databaseId')
        annotatorEmail = request.data.get('annotatorEmail')
        if databaseId is not None and annotatorEmail is not None:
            databaseObj = Database.objects.get(id=databaseId)
            annotations_done = Annotation.objects.filter(annotator_email = annotatorEmail).values_list('claim')
            if annotations_done is not None:
                queryset = queryset.filter(database=databaseObj).exclude(id__in=annotations_done) 
                output = ClaimEvidenceSerializer(queryset.first(), many=False)
                return Response({"count": queryset.count(), "firstItem": output.data})
            else:
                queryset = queryset.filter(database=databaseObj)
                output = ClaimEvidenceSerializer(queryset.first(), many=False)
                return Response({"count": queryset.count(), "firstItem": output.data})
        elif not annotatorEmail:
            raise NotFound("Annotator email was not provided!")
        else:
            raise NotFound("Database ID must be provided!")

class DeleteClaimAPIView(DestroyAPIView):
    """This endpoint allows for deletion of a specific Claim"""
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer

 # Temporal Arguments
class CreateTemporalArgsAPIView(APIView):
    """This endpoint allows for creation of a temporal arg section if it does not exist, or just returns the section id if it exists"""
    def post(self, request):
        reqClaim = request.data.get('claim')
        reqContent = request.data.get('content')
        getClaim = Claim.objects.get(id=reqClaim)

        obj, created = TemporalClaimSection.objects.get_or_create(
        claim=getClaim,
        temporal_content=reqContent)
        return Response({"id": obj.id, "created": created})

# Evidences
class CreateEvidenceAPIView(APIView):
    """This endpoint allows for creation of an evidence if it does not exist, or just returns the evidence id if it exists"""
    def post(self, request):
        reqClaim = request.data.get('claim')
        reqTitle = request.data.get('title')
        reqContent = request.data.get('content')
        reqGoldenEvi = request.data.get('golden_evi')
        getClaim = Claim.objects.get(id=reqClaim)

        obj, created = Evidence.objects.get_or_create(
        claim=getClaim,
        content=reqContent,
        defaults={'title': reqTitle, 'golden_evi': reqGoldenEvi})
        return Response({"id": obj.id, "created": created})


# Annotation
class CreateAnnotationAPIView(APIView):
    """This endpoint allows for creation of an annotation"""
    # Disable administrator authentication and permission for annotation
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        claim = request.data.get('claimId')
        req_annotator_email = request.data.get('email')
        req_annotator_temporal_flag = request.data.get('overall_temporal_claim')
        req_temporal_label = request.data.get('temporal_flag')
        req_general_label = request.data.get('general_flag')
        req_overall_label = request.data.get('overall_flag')
        getClaim = Claim.objects.get(id=claim)

        obj = Annotation(
        claim=getClaim,
        annotator_email=req_annotator_email,
        annotator_temporal_flag=req_annotator_temporal_flag,
        temporal_label=req_temporal_label,
        general_label=req_general_label,
        overall_label=req_overall_label
        )
        obj.save()
        return Response({"id": obj.id})

class ListAnnotationAPIView(APIView):
    """This endpoint allows for listing of an annotation"""
    # Disable administrator authentication and permission for annotation
    authentication_classes = []
    permission_classes = []
    serializer_class = AnnotationSerializer
    def get(self, request):
        databaseId = request.query_params.get('databaseId')
        databaseObj = Database.objects.get(id=databaseId)
        getClaims = Claim.objects.filter(database=databaseObj)
        annotations = Annotation.objects.filter(claim__in=getClaims)
        output = AnnotationSerializer(annotations, many=True)
        return JsonResponse(output.data, safe=False)

# Justification
class CreateJustificationAPIView(APIView):
    """This endpoint allows for creation of a justification"""
    # Disable administrator authentication and permission for annotation
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        req_annotation = request.data.get('annotation')
        req_temporal = request.data.get('temporal')
        req_claimPart = request.data.get('claimPart')
        req_justification = request.data.get('justification')
        getAnnotation = Annotation.objects.get(id=req_annotation)
        if (req_claimPart == False):   
            req_evidence = request.data.get('evidence')
            getEvidence = Evidence.objects.get(id=req_evidence)
            obj = Justification(
            annotation=getAnnotation,
            evidence=getEvidence, temporal=req_temporal,
            justification=req_justification
            )
            obj.save()
            return Response({"id": obj.id})
        else:
            obj = Justification(
            annotation=getAnnotation, temporal=req_temporal,
            justification=req_justification
            )
            obj.save()
            return Response({"id": obj.id})