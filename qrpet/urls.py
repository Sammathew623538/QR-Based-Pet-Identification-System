from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pet.urls')),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon.ico"))),
]

# Serving static and media files during development
# IMPORTANT: In production (when DEBUG=False), your web server (Nginx/Apache/PythonAnywhere) 
# should be configured to serve these files.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Optional: Fallback for media serving when DEBUG=False (not for high traffic)
    # Most hosting providers like PythonAnywhere require separate static/media config in their panel.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
