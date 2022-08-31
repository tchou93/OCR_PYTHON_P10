from django.urls import path, include
from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter()
router.register(r'projects', views.ProjectView, basename='projects')

issues_router = routers.NestedSimpleRouter(router, r'projects', lookup='projects')
issues_router.register(r"issues", views.IssueView, basename="issues")

comments_router = routers.NestedSimpleRouter(issues_router, r'issues', lookup='issues')
comments_router.register(r"comments", views.CommentView, basename="comments")

contributors_router = routers.NestedSimpleRouter(router, r'projects', lookup='projects')
contributors_router.register(r"users", views.ContributorView, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(issues_router.urls)),
    path("", include(contributors_router.urls)),
    path("", include(comments_router.urls)),
]
