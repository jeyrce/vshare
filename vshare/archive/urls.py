# coding = utf-8
# env    = python3.5.2
# author = lujianxin
# time   = 2018-05-05
# purpose= 归档模块路由

from . import views
from django.urls import re_path

urlpatterns = [
    re_path(r'tag/(\d+)/(\d+)$', views.TagArchive.as_view()),
    re_path(r'tag/(\d+)$', views.TagArchive.as_view()),
    re_path(r'category/(\d+)/(\d+)$', views.CateArchive.as_view()),
    re_path(r'category/(\d+)$', views.CateArchive.as_view()),
    re_path(r'file/(\d+)$', views.FileArchive.as_view()),
    re_path(r'file/(\d+)/(\d+)$', views.FileArchive.as_view()),
]






if __name__ == '__main__':
    pass

