# coding = utf-8
# env    = python3.5.2
# author = lujianxin
# time   = 201x-xx-xx 
# purpose= - - - 

from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'details/(\d+)/(\d+)/$', views.ArticleView.as_view()),
    re_path(r'details/(\d+)/$', views.ArticleView.as_view()),
    # discuss这个路由要定义一个中间件，核对登录状态
    re_path(r'discuss/$', views.DiscussView.as_view()),
]






if __name__ == '__main__':
    pass

