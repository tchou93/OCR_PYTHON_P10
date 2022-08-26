from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import CreateAPISignupView

urlpatterns = [
    path('signup/', CreateAPISignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login')
]
