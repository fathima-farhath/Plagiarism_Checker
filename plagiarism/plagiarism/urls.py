from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('profiles.urls')),
    path('class/',include('classroom.urls')),
    path('ML_model/',include('ML_model.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
