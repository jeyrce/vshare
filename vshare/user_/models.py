from django.db import models

# Create your models here.

class User(models.Model):

    id = models.IntegerField(primary_key=True, auto_created=True)
    account = models.CharField(max_length=20, unique=True,verbose_name='账号')
    pwd = models.CharField(max_length=20, verbose_name='密码')
    question = models.CharField(max_length=40, verbose_name='密保问题')
    answer = models.CharField(max_length=20,verbose_name='密保答案')
    phone = models.CharField(max_length=11, verbose_name='电话')
    tip = models.CharField(max_length=40, verbose_name='签名')
    modified = models.CharField(max_length=19, verbose_name='变更时间')
    is_delet = models.IntegerField(verbose_name='是否删除',default=0)

    class Meta:
        verbose_name_plural = '账户'
        ordering = ['id']

    def __str__(self):
        info = '%s,%s,%s,%s,%s,%s,%s,%s'%(self.account, self.pwd,self.question, self.answer, self.phone, self.tip, self.modified, self.is_delet)
        return info














