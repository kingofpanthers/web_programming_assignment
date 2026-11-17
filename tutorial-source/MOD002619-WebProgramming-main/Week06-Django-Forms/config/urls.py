from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from school import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('student/<int:pk>/', views.detail, name='detail'),
    path('student/<int:pk>/edit/', views.edit, name='edit'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
