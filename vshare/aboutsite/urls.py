# coding = utf-8
# env    = python3.5.2
# author = lujianxin
# time   = 201x-xx-xx 
# purpose= - - - 
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'me_ljx$', views.MyInfoView.as_view()),
    re_path(r'msgboard$', views.MsgBoardView.as_view()),
    # 验证码生成和校验
    re_path(r'getcode/\d*', views.Code.as_view()),
    re_path(r'checkcode/$', views.CheckCode.as_view()),
]





if __name__ == '__main__':
    pass

