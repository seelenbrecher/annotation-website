from django.urls import path
from database import views

urlpatterns = [
    path("",views.ListDatabaseAPIView.as_view(),name="database_list"),
    path("create/", views.CreateDatabaseAPIView.as_view(),name="database_create"),
    path("update/<int:pk>/",views.UpdateDatabaseAPIView.as_view(),name="update_database"),
    path("delete/<int:pk>/",views.DeleteDatabaseAPIView.as_view(),name="delete_database"),
    path("claims/create/", views.CreateClaimAPIView.as_view(),name="claim_create"),
    path("claims/list/", views.ListClaimAPIView.as_view(),name="claim_list_by_database"),
    path("claims/delete/<int:pk>/",views.DeleteClaimAPIView.as_view(),name="delete_claim"),
    path("evidence/create/", views.CreateEvidenceAPIView.as_view(),name="evidence_create"),
    path("temporalargs/create/", views.CreateTemporalArgsAPIView.as_view(),name="temporal_args_create"),
    path("annotation/check/", views.CheckAnnotationAPIView.as_view(),name="check_annotation"),
    path("annotation/get/", views.ListClaimWithEvidenceAPIView.as_view(),name="get_annotation"),
    path("annotation/add/", views.CreateAnnotationAPIView.as_view(),name="add_annotation"),
    path("annotation/add/justification/", views.CreateJustificationAPIView.as_view(),name="add_justification"),
]