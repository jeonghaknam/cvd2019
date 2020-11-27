import re
import os
import time
from newsapi import NewsApiClient
from django.conf import settings
from django.template import loader
from django.shortcuts import render
from django.views.generic import View
from datetime import date, timedelta, datetime
from .models import WorldTotal, World, DomesticTotal, Domestic, WorldName, DomesticName
from collection import korea, world


# Create your views here.

# 정적 페이지 생성
def create_static_page():
    """
    한국어,중국어,영어 세개의 홈페이지를 static/ 파일에 생성합니다.
    ----
    크롤링 ==> 데이터 필터링,저장 ==> 데이터 계산 처리 ==> 정적 홈페이지 생성

    :return: log (+크론탑 실행 및 크롤링)
    """
    korea_msg = korea.MysqlSave().run()
    world_msg = world.MysqlSave().run()

    languages = ['ko-kr', 'en-us', 'zh-hans']
    for language in languages:
        handle = Processing()
        context = handle.run(language)

        if language == 'ko-kr':
            temp = loader.get_template('kr_static_index.html')
            country = 'kr'
        elif language == 'en-us':
            temp = loader.get_template('en_static_index.html')
            country = 'en'
        else:
            temp = loader.get_template('cn_static_index.html')
            country = 'cn'

        index_html = temp.render(context)
        save_path = os.path.join(settings.BASE_DIR,
                                 'static/{}index.html'.format(country))

        with open(save_path, 'w', encoding="utf-8") as f:
            f.write(index_html)

    print('{a} 없데이트 완료\n{b}\n{c}\n'
          .format(a=time.strftime("%Y-%m-%d %H:%M:%S"), b=korea_msg, c=world_msg))


# 페이지에 필요한 데이터 처리
class Processing:

    # 사망률 계산
    def death_rate(self, model_obj):
        """
        :param model_obj: model object
        :return: model object (+사망률)
        """
        if model_obj.cumulative - model_obj.quarantine != model_obj.cure + model_obj.death:
            model_obj.death_rate = 'N/A'
        else:
            try:
                death_rate = model_obj.death / (model_obj.death + model_obj.cure) * 100
                if death_rate > 0:
                    model_obj.death_rate = '%.01f' % death_rate + '%'
                else:
                    model_obj.death_rate = '0%'
            except ZeroDivisionError:
                model_obj.death_rate = '0%'
                return model_obj

        return model_obj

    # 어제 대비 증가수치 계산
    def compare_data(self, model_obj, yesterday_model_obj):
        """
        :param model_obj: model object
        :param yesterday_model_obj: model object
        :return: model object (+증가된 수치)
        """
        # 1.격리해제+-
        model_obj.compare_cure = model_obj.cure - yesterday_model_obj.cure
        # 2.누적확진+-
        model_obj.compare_cumulative = model_obj.cumulative - yesterday_model_obj.cumulative
        # 3.사망자+-
        model_obj.compare_death = model_obj.death - yesterday_model_obj.death
        # 4.격리중+-
        model_obj.compare_quarantine = model_obj.quarantine - yesterday_model_obj.quarantine
        # * DomesticTotal일경우 해외유입 비교수치가 추가로 필요하다.
        if model_obj is DomesticTotal:
            model_obj.compare_overseas = model_obj.overseas - yesterday_model_obj.overseas

        return model_obj

    # 데이터베이스 값 요청
    def objects_method(self, method, model_class, day):
        """
        :param method: get or filter
        :param model_class: model class name
        :param day: int(number) 0=today, 1=yesterday ...
        :return: dict(result=1 or 0 or None, data=model object or QuerySet or None)
                :result=1 입력된 날짜의 데이터
                :result=0 입력된 날짜로부터 일주일 내의 데이터
                :result=None 데이터값 없거나 메소드 입력이 잘못됨
        """
        days = date.today() - timedelta(days=day)

        # get
        if method is 'get':
            try:
                data = model_class.objects.get(create_time=days)
                return dict(result=1, data=data)
            except model_class.DoesNotExist:
                for day_number in range(day + 1, 8):
                    days = date.today() - timedelta(days=day_number)

                    try:
                        data = model_class.objects.get(create_time=days)
                        return dict(result=0, data=data)
                    except model_class.DoesNotExist:
                        if day_number == 7:
                            return dict(result=None)
                        continue

        # filter
        elif method is 'filter':
            data = model_class.objects.filter(create_time=date.today())
            if len(data) != 0:
                return dict(result=1, data=data)
            else:
                for day_number in range(day + 1, 8):
                    days = date.today() - timedelta(days=day_number)
                    data = model_class.objects.filter(create_time=days)
                    if len(data) != 0:
                        return dict(result=0, data=data)

                return dict(result=None, data=None)

        else:
            return dict(result=None, data=None)

    # 페이지 언어를 판단하여 지역,나라 이름을 해당언어로 바꿔준다
    def language_name(self, name_model_class, model_obj):
        name_obj = WorldName if name_model_class == World else DomesticName

        try:
            # 영문명칭
            language = name_obj.objects.get(enname=model_obj.area_name)
        except name_obj.DoesNotExist:
            try:
                # 한글명칭
                language = name_obj.objects.get(krname=model_obj.area_name)
            except name_obj.DoesNotExist:
                try:
                    # 한문명칭
                    language = name_obj.objects.get(cnname=model_obj.area_name)
                except name_obj.DoesNotExist:
                    model_obj.lang_name = model_obj.area_name
                    return model_obj

        if self.language == 'zh-hans':
            model_obj.lang_name = language.cnname
        elif self.language == 'en-us':
            model_obj.lang_name = language.enname
        else:
            model_obj.lang_name = language.krname

        return model_obj

    # Page 헤드부분 Total 데이터
    def total_data(self, model_class):
        """
        :param model_class: model class name
        :return: model object (+total 종합 데이터)
                : 최근 7일 이내 데이터 없을경우 None 값 반환
        """
        today_dict = self.objects_method('get', model_class, 0)

        if today_dict['result'] == True:
            today_data = self.death_rate(today_dict['data'])

        elif today_dict['result'] == False:
            day_data = self.death_rate(today_dict['data'])
            return day_data

        else:
            return today_dict['result']

        # 오늘 데이터 있을경우만 증가된 데이터 계산
        yesterday_data = self.objects_method('get', model_class, 1)

        if yesterday_data['result'] == True:
            today_data = self.compare_data(today_data, yesterday_data['data'])
            return today_data

        else:
            return today_data

    # Page Table 데이터
    def table_data(self, model_class):
        """
        :param model_class: model class name
        :return: model object (+table 종합 데이터)
                : 최근 7일 이내 데이터 값이 없을경우 None 값 반환
        """
        today_dict = self.objects_method('filter', model_class, 0)

        if today_dict['result'] == False:
            week_data = today_dict['data']
            for area in week_data:
                day_data = self.death_rate(area)
                self.language_name(model_class, day_data)

            return week_data

        elif today_dict['result'] == True:
            today_data = today_dict['data']
            for area in today_data:
                day_data = self.death_rate(area)
                day_data = self.language_name(model_class, day_data)
                yesterday = date.today() - timedelta(days=1)

                try:
                    yesterday_data = model_class.objects.get(create_time=yesterday, area_name=area.area_name)
                    self.compare_data(day_data, yesterday_data)
                except model_class.DoesNotExist:
                    continue

            return today_data

        else:
            return today_dict['result']

    # Page Bar 차트 데이터
    def bar_data(self, model_class):
        """
        :param model_class: model class name
        :return: QuerySet (격리수치가 심각한 10개 지역 or 나라)
                : 최근 일주일 이내 데이터 없을시 None 값 반환
        """
        data = self.table_data(model_class)

        if data is not None:
            data = sorted(data, key=lambda keys: keys.quarantine)
            return data[-10:]
        else:
            return data

    # Page Line 차트 데이터
    def line_data(self, model_class):
        """
        :param model_class: model class name
        :return: QuerySet (+코로나 추세 종합 비교 수치 )
        """
        history_data = model_class.objects.all().order_by('create_time')

        for day_data in history_data:
            yesterday = day_data.create_time - timedelta(days=1)

            try:
                yesterday_date = model_class.objects.get(create_time=yesterday)
                self.compare_data(day_data, yesterday_date)
            except model_class.DoesNotExist:
                day_data.compare_cumulative = 0
                day_data.compare_cure = 0
                continue

        return history_data

    # Page News 데이터
    def news_data(self):
        """
        News API 무료버전  https://newsapi.org/
        회원가입 및 api_key 발급필요

        :return: list (최신 10개 뉴스)
        """
        yesterday = date.today() - timedelta(days=1)


        # api_key 발급후 #123456789 수정바람
        newsapi = NewsApiClient(api_key='#123456789')

        head_news = newsapi.get_everything(
            q='코로나',
            from_param=date.today(),
            to=yesterday,
            sort_by='relevancy',
            page=1
        )

        articles = head_news['articles']
        head_news = sorted(articles, key=lambda keys: keys['publishedAt'], reverse=True)
        head_news = head_news[:10]

        for i in head_news:
            news_dcp = i['description'][:150]
            i['description'] = re.sub(
                r'\(adsbygoogle = window.adsbygoogle \|\| \[\]\).push\(\{\}\)\;', '', news_dcp)

        return head_news

    # 실행
    def run(self, language):
        """
        :param language: 페이지 사용될 언어 'ko-kr', 'en-us', 'zh-hans'
        :return: 렌더링에 사용될 데이터 dict
        """
        self.language = language
        total_world = self.total_data(WorldTotal)
        total_domestic = self.total_data(DomesticTotal)
        data_country = self.table_data(World)
        data_area = self.table_data(Domestic)
        bar_world = self.bar_data(World)
        bar_domestic = self.bar_data(Domestic)
        line_world = self.line_data(WorldTotal)
        line_domestic = self.line_data(DomesticTotal)
        data_news = self.news_data()

        context = {
            'total_world': total_world,
            'total_domestic': total_domestic,
            'data_country': data_country,
            'data_area': data_area,
            'bar_world': bar_world,
            'bar_domestic': bar_domestic,
            'line_world': line_world,
            'line_domestic': line_domestic,
            'data_news': data_news
        }

        return context


# /index
class IndexView(View):

    def get(self, request):
        language = 'ko-kr'
        run = Processing()
        context = run.run(language)

        return render(request, 'kr_static_index.html', context)


