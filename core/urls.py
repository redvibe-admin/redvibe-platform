from django.urls import path
from . import views as core_views

urlpatterns = [
    path('', core_views.home, name='home'),
    path('reels/', core_views.reels_view, name='reels'),
    path('upload/', core_views.upload_view, name='upload'),
    path('mark-watched/', core_views.mark_watched, name='mark-watched'),

    # Auth
    path('signup/', core_views.signup_view, name='signup'),
    path('login/', core_views.login_view, name='login'),
    path('profile/<int:user_id>/', core_views.profile_view, name='profile'),

    # Post view
    path('post/<int:pk>/', core_views.view_post, name='view_post'),

    # Comment/Like/Report
    path('post/<int:pk>/comment/', core_views.comment_view, name='comment'),
    path('post/<int:pk>/like/', core_views.like_view, name='like'),
    path('post/<int:pk>/report/', core_views.report_view, name='report'),
]
