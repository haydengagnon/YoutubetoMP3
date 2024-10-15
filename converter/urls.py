from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("browse", views.browse_mp3, name="browse"),
    path("convert", views.convert, name="convert"),
    path("post_mp3/<path:mp3_file_url>", views.post_mp3, name="post_mp3"),
    path("delete_file", views.delete_file, name="delete_file"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)