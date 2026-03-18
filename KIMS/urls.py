from django.contrib import admin
from django.urls import path, include
from django.conf import settings # IMPORT THIS
from django.conf.urls.static import static # IMPORT THIS

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('management.urls')), 
]

# This part allows the browser to see the images in your 'media' folder
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)