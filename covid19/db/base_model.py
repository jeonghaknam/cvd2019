from django.db import models


class BaseModel(models.Model):
    '''추상 모델 클래스'''
    create_time = models.DateField(auto_now_add=True, verbose_name='작성일자')
    update_time = models.DateTimeField(auto_now=True, verbose_name='없데이트')
    is_delete = models.BooleanField(default=False, verbose_name='삭제')

    class Meta:
        abstract = True