# coding = utf-8
# env    = python3.5.2
# author = lujianxin
# time   = 2018-04-30
# purpose= file模块路由

from django.urls import re_path
from .views import FileCenter, FileUpload, FileDownload


urlpatterns = [
    re_path(r'filecenter$', FileCenter.as_view()),
    re_path(r'upload$', FileUpload.as_view()),
    re_path(r'download$', FileDownload.as_view()),
]





if __name__ == '__main__':
    pass

