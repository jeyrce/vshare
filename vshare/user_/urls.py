# coding = utf-8
# env    = python3.5.2
# author = lujianxin
# time   = 201x-xx-xx 
# purpose= - - - 

from django.urls import re_path
from . import views

urlpatterns = [
    # 此模块下的路径映射
    re_path(r'usercenter$', views.UserCenter.as_view()),
    re_path(r'details/(\d+)$', views.UserDetails.as_view()),
    re_path(r'login$', views.Login.as_view()),
    re_path(r'regist$', views.Regist.as_view()),
    re_path(r'logout$', views.Logout.as_view()),
    re_path(r'securecenter$', views.SecureCenter.as_view()),
    re_path(r'write_article$', views.WriteArticle.as_view()),
    re_path(r'change_art/(\d+)$', views.ChangeArt.as_view()),
    re_path(r'cpwd$', views.ModifyPwd.as_view()),
    re_path(r'findpwd$', views.FindPwd.as_view()),
    re_path(r'cpwdsafe$', views.ModifyPwdSafe.as_view()),
]




if __name__ == '__main__':
    pass

