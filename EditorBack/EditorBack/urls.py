"""
URL configuration for EditorBack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from app import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name="media"),
    path('admin/', admin.site.urls),
    path('sign-up/', views.signUp),
    path('sign-in/', views.signIn),
    path('user-profile/', views.getUserProfile),

    path('set-access-token/', views.setAccessToken),
    path('modify-password/', views.modifyPassword),

    path('translate/', views.translate),
    path('abstract/', views.abstract),
    path('decorate/', views.decorate),
    path('continue-write/', views.continueWrite),
    path('rewrite/', views.rewrite),
    path('improve-write/', views.improveWrite),
    path('summarize/', views.summarize),
    path('analysis/', views.analysis),
    path('ocr/', views.useOCR),
    path('voice-recognise/', views.voiceRecognise),
    path('video-recognise/', views.videoRecognise),
    path('project-document/', views.projectDocument),
    path('code-edit/', views.codeEdit),

]
