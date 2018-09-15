from django.db import models
from user_.models import User
from django.db.models import Q
import time
# Create your models here.

# 文章类型
class Category(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    category = models.CharField(unique=True, max_length=20, verbose_name='类别')
    is_delet = models.IntegerField(default=0, verbose_name='是否已删除')

    class Meta:
        verbose_name_plural = '文章类别'
        ordering = ['id']

    def __str__(self):
        return '%s, %s, %s'%(self.id, self.category, self.is_delet)

# 文章标签
class Tag(models.Model):

    id = models.IntegerField(primary_key=True, auto_created=True)
    tag = models.CharField(unique=True, max_length=20, verbose_name='文章标签')
    is_delet = models.IntegerField(default=0, verbose_name='是否已删除')

    class Meta:
        verbose_name_plural = '文章标签'
        ordering = ['id']

    def __str__(self):
        return '%s, %s, %s' % (self.id, self.tag, self.is_delet)

# 文章
class Article(models.Model):
    from DjangoUeditor.models import UEditorField

    id = models.IntegerField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=20,verbose_name='标题')
    category = models.ForeignKey(Category, on_delete=True, limit_choices_to=Q(is_delet=0),verbose_name='分类')
    tag = models.ForeignKey(Tag, on_delete=True, limit_choices_to=Q(is_delet=0), verbose_name='标签')
    author = models.ForeignKey(User, on_delete=True, limit_choices_to=Q(is_delet=0), verbose_name='作者')
    content = UEditorField(u"文章正文", height=300, width=1000, default=u'', blank=True, imagePath="uploads/blog/images/",
                           toolbars='besttome', filePath='uploads/blog/files/')
    create_time = models.CharField(max_length=19, verbose_name='发表时间')
    # content = models.TextField(blank=True, verbose_name='内容')
    read = models.IntegerField(default=0, verbose_name='阅读次数')
    discuss = models.IntegerField(default=0, verbose_name='评论数')
    is_delet = models.IntegerField(default=0, verbose_name='是否已删除')

    class Meta:
        verbose_name_plural = '文章详情'
        ordering = ['id']

    def __str__(self):
        return '%s, %s, %s, %s, %s, %s, %s, %s' % (self.title, self.category, self.tag, self.author, self.read, self.content, self.discuss, self.is_delet)

# 评论
class Discussion(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=True, limit_choices_to={'is_delet': 0}, verbose_name='用户id')
    create_time = models.CharField(max_length=19, verbose_name='评论时间')
    article = models.ForeignKey(Article, on_delete=True, limit_choices_to={'is_delet': 0}, verbose_name='文章id')
    content = models.TextField(blank=True, verbose_name='内容')
    is_delet = models.IntegerField(default=0, verbose_name='是否已删除')


    class Meta:
        verbose_name_plural = '文章评论'
        ordering = ['id']

    def __str__(self):
        return '%s, %s, %s, %s, %s'%(self.user, self.create_time, self.article, self.content, self.is_delet)

    # 按页码获取评论



