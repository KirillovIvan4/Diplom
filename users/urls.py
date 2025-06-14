from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, PasswordRecoveryView, email_verification, block_user, UserListView
from . import views
app_name = 'users'

urlpatterns = [
    path('', views.personal_account, name='personal_account'),
    path('login/', LoginView.as_view(template_name='users/login.html', next_page='table_reservation:home'), name='login'),
    path('logout/', LogoutView.as_view(next_page='table_reservation:home'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path("email-confirm/<str:token>/", email_verification, name="email_verification"),
    path('password_recovery/',PasswordRecoveryView.as_view(), name='password_recovery'),
    path("block_user/<int:pk>", block_user, name="block_user"),
    path('customuser_list/', UserListView.as_view(), name='user_list'),

]