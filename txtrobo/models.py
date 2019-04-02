from django.db import models


# Create your models here.
class Record(models.Model):
    """
    用于存储用户的聊天记录和问题分类
    """

    class Meta:
        verbose_name = '记录'
        verbose_name_plural = verbose_name

    txt_in = models.CharField('输入文本', max_length=100)
    answer = models.ForeignKey(
        'Answer', on_delete=models.CASCADE, related_name='record', null=True, blank=True)
    flow = models.ForeignKey('WorkFlow', on_delete=models.CASCADE,
                             related_name='record', null=True, blank=True)
    question = models.ForeignKey(
        'Question', on_delete=models.CASCADE, related_name='record', null=True, blank=True)
    pub_date = models.DateTimeField('提交时间', auto_now=True)


# 用于存储标准回答的表
class Answer(models.Model):
    class Meta:
        verbose_name = '标准回答'
        verbose_name_plural = verbose_name

    txt = models.TextField('答案文本', max_length=300)
    condition = models.CharField('条件', max_length=50, null=True, blank=True)
    question = models.ForeignKey(
        'Question', on_delete=models.CASCADE, related_name='answer', null=True, blank=True)

    # 你也可以在定义主表的外键的时候，给这个外键定义好一个名称，要用related_name

    def __str__(self):
        return self.txt


# 训练问题表
class Question(models.Model):
    """
    训练数据
    """

    class Meta:
        verbose_name = '问题训练数据'
        verbose_name_plural = verbose_name

    value = models.TextField()
    number = models.IntegerField('问题数量', default=1)
    flow = models.ForeignKey('WorkFlow', on_delete=models.CASCADE)

    def __str__(self):
        return self.value


# 工作流程表
class WorkFlow(models.Model):
    """
    业务流程
    """

    class Meta:
        verbose_name = '业务流程'
        verbose_name_plural = verbose_name

    name = models.CharField('业务分类', max_length=20)
    answer = models.ForeignKey(
        'Answer', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.name


# 停用词表
class StopWords(models.Model):
    """
    停用词
    """

    class Meta:
        verbose_name = '停用词'
        verbose_name_plural = verbose_name

    word = models.CharField('停用词', max_length=10)

    def __str__(self):
        return self.word


# 专业词汇表
class ProfessDict(models.Model):
    """
    专业词典数据
    """

    class Meta:
        verbose_name = '专业词典'
        verbose_name_plural = verbose_name

    word = models.CharField('专业词', max_length=10)

    def __str__(self):
        return self.word
