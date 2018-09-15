from django.contrib import admin

# Register your models here.
# 注册自定义的表，方可在django后台使用
from user_.models import *
from aboutsite.models import *
from archive.models import *
from article.models import *
from file.models import *
from mainpage.models import *



admin.site.register([
    User,
    MsgBoard,
    TopNotice,
    VisitDocument,
    Article,
    Category,
    Discussion,
    Tag,
    File,
    FileType,


])
















