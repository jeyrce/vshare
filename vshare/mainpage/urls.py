# coding = utf-8
# env    = python3.5.2
# author = lujianxin
# time   = 2018-03-20
# purpose= 首页路由

from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'search/', views.SearchView.as_view()),
    re_path(r'(\d+)', views.MainPage.as_view()),
    re_path(r'$', views.MainPage.as_view()),
]




if __name__ == '__main__':
    pass

