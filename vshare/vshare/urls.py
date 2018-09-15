"""vshare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import re_path, include
from django.conf import settings


urlpatterns = [
    # 各模块的路由包含到此
    re_path('admin/', admin.site.urls),
    re_path('^mainpage/', include('mainpage.urls')),
    re_path(r'^archive/', include('archive.urls')),
    re_path('^user_/', include('user_.urls')),
    re_path('^article/', include('article.urls')),
    re_path('^aboutsite/', include('aboutsite.urls')),
    re_path('^file/', include('file.urls')),
    re_path('^$', include('mainpage.urls')),
    re_path(r'^ueditor/', include('DjangoUeditor.urls')), # 编辑器
    # re_path(r'^controller/$', get_ueditor_controller),
]

# media 的使用
from django.views.static import serve
urlpatterns.append(re_path(r'media/(.*)', serve, {'document_root': settings.MEDIA_ROOT}))



