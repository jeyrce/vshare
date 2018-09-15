from django.db import models
from user_.models import User
from django.db.models import F

# Create your models here.
# 文件分类
class FileType(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(unique=True, max_length=20, verbose_name='类型名')
    filetype = models.CharField(max_length=20, unique=True, verbose_name='文件类型')
    is_delet = models.IntegerField(default=0, verbose_name='是否已删除')

    class Meta:
        verbose_name_plural = '文件类别'
        ordering = ['id']

    def __str__(self):
        return '%s, %s, %s' % (self.name, self.filetype, self.is_delet)


# 文件模型
class File(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, unique=True, verbose_name='文件名')
    path = models.CharField(max_length=200, verbose_name='文件所在路径')
    filetype = models.ForeignKey(FileType, on_delete=True, limit_choices_to={'is_delet': 0}, verbose_name='文件类型')
    content_type = models.CharField(max_length=50, verbose_name='文件content-type')
    upload_time = models.CharField(max_length=19, verbose_name='上传时间')
    user = models.ForeignKey(User, on_delete=False, limit_choices_to={'is_delet': 0}, verbose_name='上传人id')
    download = models.IntegerField(verbose_name='下载次数')
    is_delet = models.IntegerField(default=0, verbose_name='是否已删除')

    class Meta:
        verbose_name_plural = '文件表'
        ordering = ['id']

    def __str__(self):
        return '%s, %s, %s, %s, %s, %s'%(self.name, self.path, self.upload_time, self.download, self.user, self.is_delet)








