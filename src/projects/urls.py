from django.urls import path, include
from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter()
router.register(r'projects', views.ProjectViewSet, basename='projects')

user_issue_project_router = routers.NestedSimpleRouter(router, r'projects', lookup='projects')
user_issue_project_router.register(r"issues", views.IssueViewSet, basename="issues")
# users_issues_router.register(r"users", , basename="users")

# issue_comment_router = routers.NestedSimpleRouter(user_issue_project_router, r"issues", lookup="issues")
# issue_comment_router.register(r"comments", , basename="comments")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(user_issue_project_router.urls)),
]
