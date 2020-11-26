from django.db import models
from db.base_model import BaseModel

# Create your models here.


class WorldTotal(BaseModel):
    '''total세계현황'''
    death = models.IntegerField(default=0, verbose_name='사망자')
    cure = models.IntegerField(default=0, verbose_name='격리해제')
    quarantine = models.IntegerField(default=0, verbose_name='격리중')
    cumulative = models.IntegerField(default=0, verbose_name='누적확진')


    class Meta:
        db_table = 'df_world_wide_total'
        verbose_name = 'total세계현황'
        verbose_name_plural = verbose_name


class World(BaseModel):
    '''세계 국가별현황'''
    area_name = models.CharField(max_length=30, verbose_name='지역이름')
    cumulative = models.IntegerField(default=0, verbose_name='누적확진')
    quarantine = models.IntegerField(default=0, verbose_name='격리중')
    cure = models.IntegerField(default=0, verbose_name='격리해제')
    death = models.IntegerField(default=0, verbose_name='사망자')


    class Meta:
        db_table = 'df_world_wide'
        verbose_name = '세계 국가별현황'
        verbose_name_plural = verbose_name


class DomesticTotal(BaseModel):
    '''total국내현황'''
    death = models.IntegerField(default=0, verbose_name='사망자')
    cure = models.IntegerField(default=0, verbose_name='격리해제')
    overseas = models.IntegerField(default=0, verbose_name='해외유입')
    quarantine = models.IntegerField(default=0, verbose_name='격리중')
    cumulative = models.IntegerField(default=0, verbose_name='누적확진')


    class Meta:
        db_table = 'df_domestic_total'
        verbose_name = 'total국내현황'
        verbose_name_plural = verbose_name


class Domestic(BaseModel):
    '''국내 지역현황'''
    area_name = models.CharField(max_length=30, verbose_name='지역이름')
    cumulative = models.IntegerField(default=0, verbose_name='누적확진')
    quarantine = models.IntegerField(default=0, verbose_name='격리중')
    cure = models.IntegerField(default=0, verbose_name='격리해제')
    death = models.IntegerField(default=0, verbose_name='사망자')


    class Meta:
        db_table = 'df_domestic'
        verbose_name = '국내지역현황'
        verbose_name_plural = verbose_name


class WorldName(models.Model):
    '''나라이름'''
    enname = models.CharField(max_length=30, unique=True, verbose_name='영문명칭')
    krname = models.CharField(max_length=30, unique=True, verbose_name='한글명칭')
    cnname = models.CharField(max_length=30, unique=True, verbose_name='한문명칭')


    class Meta:
        db_table = 'df_worldname'
        verbose_name = '나라이름'
        verbose_name_plural = verbose_name


class DomesticName(models.Model):
    '''국내 지역이름'''
    enname = models.CharField(max_length=30, unique=True, verbose_name='영문명칭')
    krname = models.CharField(max_length=30, unique=True, verbose_name='한글명칭')
    cnname = models.CharField(max_length=30, unique=True, verbose_name='한문명칭')


    class Meta:
        db_table = 'df_domesticname'
        verbose_name = '국내 지역이름'
        verbose_name_plural = verbose_name