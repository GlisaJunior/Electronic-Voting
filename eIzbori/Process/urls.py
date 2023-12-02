from django.urls import include, path
from . import views

urlpatterns = [
    path('Voting/<str:key>/', views.voting_view, name = 'Voting'),
    path('Commission/', views.Commission_view, name = 'Commission' ),
    path('Login/', views.login_view, name = "Login"),
    path('Upload/', views.upload_csv, name='upload_csv')
]
