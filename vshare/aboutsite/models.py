from django.db import models
from utils.page_breaker import pagebreaker
# from user_.models import User
# from django.db.models import Q
# Create your models here.

# 留言板
class MsgBoard(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    # user = models.ForeignKey(User, on_delete=True, limit_choices_to=Q(is_delet=0), verbose_name='用户id')
    create_time = models.CharField(max_length=19, verbose_name='留言时间')
    nickname = models.CharField(max_length=10, verbose_name='留言昵称')
    content = models.TextField(verbose_name='内容')
    email = models.CharField(max_length=30, verbose_name='邮箱')
    is_delet = models.IntegerField(default=0, verbose_name='是否已删除')

    class Meta:
        verbose_name_plural = '网站留言版'
        ordering = ['id']

    def __str__(self):
        return '%s, %s, %s, %s, %s'%(self.create_time, self.nickname, self.content, self.email, self.is_delet)

# 主页访问记录
class VisitDocument(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    host = models.CharField(max_length=20, verbose_name='主机ip')
    visit_time = models.CharField(max_length=19, verbose_name='访问时间')
    is_delet = models.IntegerField(default=0, verbose_name='是否已删除')

    class Meta:
        verbose_name_plural = '网站统计'
        ordering = ['id']

    def __str__(self):
        return '%s, %s, %s'%(self.host, self.visit_time, self.is_delet)

    # 获取整个记录数
    @classmethod
    def get_count_of_doc(cls):
        return cls.objects.count(is_delet=0)
# 置顶公告
class TopNotice(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    content = models.CharField(max_length=300, verbose_name='内容')
    create_time = models.CharField(max_length=19, verbose_name='发布时间')
    is_delet = models.IntegerField(default=0, verbose_name='是否已删除')

    class Meta:
        verbose_name_plural = '置顶公告'
        ordering = ['id']

    def __str__(self):
        return '%s, %s, %s'%(self.content, self.create_time, self.is_delet)

    # 获取最近一条记录
    @classmethod
    def get_most_recent_one(cls):
        notice = cls.objects.order_by('-id').filter(is_delet=0).first()
        # print(notice.content)
        return notice

    # 所有记录的分页获取,utils封装一个通用分页方法
    @classmethod
    def get_all(self, num=1, perpage=10):
        query_set = TopNotice.objects.order_by('-id').filter(is_delet=0)
        num_ = int(num)
        per_page = int(perpage)
        return pagebreaker(query_set, num, per_page)




