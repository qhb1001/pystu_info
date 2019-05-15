from django.db import models
from django.utils import timezone

# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    stu_id = models.CharField('学号', max_length=200)
    stu_name = models.CharField('姓名', max_length=200)
    stu_tel = models.CharField('电话', max_length=200)
    stu_email = models.CharField('邮箱', max_length=200)
    stu_info = models.CharField('信息', max_length=1000, default="少年，我看好你哦,这学期的python成绩是balabalaballa!")
    stu_password = models.CharField('密码', max_length=200, default='123456')
    stu_intro = models.CharField('简介', max_length=1000, default='熟悉的城市啊~~~，我要金坷垃')
    stu_qq = models.CharField('QQ', max_length=200, default='')

    def __str__(self):
        return self.stu_name


class Work(models.Model):  # 作业
    id = models.AutoField(primary_key=True)
    desc = models.CharField('描述', max_length=100)
    is_show = models.IntegerField('是否展示,1展示,0不展示,2可以查看结果', default=1)
    addtime = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return self.desc


class Topic(models.Model):  # 题目
    id = models.AutoField(primary_key=True)
    desc = models.CharField('描述', max_length=1000)
    mark = models.FloatField('分数')
    result = models.CharField('答案', max_length=200, default='')
    work = models.ForeignKey(Work, on_delete=models.CASCADE)

    def __str__(self):
        return self.desc


class Usertopic(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    updatetime = models.DateTimeField(auto_now_add=True)
    answer = models.CharField('答案', max_length=200, default='')
    result = models.IntegerField('结果',default=0)
    mark = models.FloatField('分数',default=0)
    def __str__(self):
        return str(self.user)+'  =====  '+self.answer


class Log(models.Model):
    id = models.AutoField(primary_key=True)
    log_time = models.DateTimeField('日志时间', auto_now_add=True)
    log_info = models.CharField('日志内容', max_length=1000)
    log_ip = models.CharField("登陆IP", max_length=200, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.log_info


class Config(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField("配置 key", max_length=200)
    value = models.CharField("配置值", max_length=200)
    remarks = models.CharField("备注", max_length=200)
