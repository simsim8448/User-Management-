from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from employees import views
from employees.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔹 لندینگ
    path('', views.landing, name='landing'),

    # 🔹 لاگین
    path(
        'login/',
        CustomLoginView.as_view(),
        name='login'
    ),

    # 🔹 لاگ‌اوت
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='login'),
        name='logout'
    ),

    # 🔹 ثبت‌نام
    path('signup/', views.signup, name='signup'),

    # 🔹 داشبورد
    path('home/', views.home, name='home'),

    # 🔹 employee crud
    path('add/', views.add, name='add'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)