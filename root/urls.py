from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from root import settings

admin.site.site_header = "Login Admin"
admin.site.site_title = "UMSRA Admin Portal"
admin.site.index_title = "Welcome to UMSRA Researcher Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogs.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
