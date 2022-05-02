from django.urls import path
from . views import RegisterView, RetrieveUserView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('getuser', RetrieveUserView.as_view()),
]