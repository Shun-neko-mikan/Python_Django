from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from . import views

app_name = "YoutubeDL"

urlpatterns = [
    path("", views.Login, name = "login"),
    path("logout", views.Logout, name = "logout"),
    path("register/", views.AccountRegistration.as_view(), name="account_registration"),
    path("DLform/", views.DLformview.as_view(), name="DLform"),
    path("download/", views.file_download_view, name="download"),
    path("clean/", views.CLEAN_DIR, name="clean"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()