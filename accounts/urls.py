from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'  # namespace fix

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),  # pk -> user_id
]
