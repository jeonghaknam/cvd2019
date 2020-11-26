# coding=utf-8
import re
import requests
from lxml import etree
from datetime import date
from cvd2019.models import WorldTotal, World


class Crawling:
    """전세계 데이터 수집
        run함수 실행시 리스트 값을 반환 type:리스트
        ** 크롤링 URL: https://www.worldometers.info/coronavirus/
                     (Worldometer)
    """
    def __init__(self):
        self.url_temp = "https://www.worldometers.info/coronavirus/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}

    def parse_url(self, url):
        """ 응답코드 반환 """
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def save_html(self, html_str):
        """ 필요한 데이터 필터링 및 반환 (type: list)
            * html_str = 응답코드
        """
        html = etree.HTML(html_str)
        item = []
        data = {}
        # 1: 총 합계 데이터를 수집
        data["total_cure"] =html.xpath('//*[@id="maincounter-wrap"][3]/div/span/text()')[0] if len(
            html.xpath('//*[@id="maincounter-wrap"][1]/div/span/text()')) > 0 else 'None'
        data["total_cumulative"] =html.xpath('//*[@id="maincounter-wrap"][1]/div/span/text()')[0] if len(
            html.xpath('//*[@id="maincounter-wrap"][1]/div/span/text()')) > 0 else 'None'
        data["total_death"] =html.xpath('//*[@id="maincounter-wrap"][2]/div/span/text()')[0] if len(
            html.xpath('//*[@id="maincounter-wrap"][2]/div/span/text()')) > 0 else 'None'
        data["total_quarantine"] = html.xpath('//*[@class="number-table-main"][1]/text()')[0] if len(
            html.xpath('//*[@class="number-table-main"][1]/text()')) > 0 else 'None'
        item.append(data)

        # 2. 각 나라별 데이터를 수집
        tr_list = html.xpath('//*[@id="main_table_countries_today"]/tbody[1]/tr')
        for i in tr_list:
            data = {}
            data["country"] = i.xpath('./td[2]/a/text()')[0] if len(i.xpath('./td[2]/a/text()')) > 0 else 'None'
            data["cure"] = i.xpath('./td[7]/text()')[0] if len(i.xpath('./td[7]/text()')) > 0 else 'None'
            data["cumulative"] = i.xpath('./td[3]/text()')[0] if len(i.xpath('./td[3]/text()')) > 0 else 'None'
            data["death"] = i.xpath('./td[5]/text()')[0] if len(i.xpath('./td[5]/text()')) > 0 else 'None'
            data["quarantine"] = i.xpath('./td[9]/text()')[0] if len(i.xpath('./td[9]/text()')) > 0 else 'None'
            item.append(data)

        return item

    def run(self):
        # 1.요청 응답코드-받기
        html_str = self.parse_url(self.url_temp)
        # 2.데이터 필터링
        covid19_data = self.save_html(html_str)
        # 3.데이터 반환
        return covid19_data


class MysqlSave:
    """수집한 데이터를 데이터베이스에 업데이트 및 생성
        0시 이전일 경우 데이터 없데이트
        0시 이후 새로운 데이터 생성
    """
    def total_data_update(self, data, today_objects):
        """전세계 토탈데이터 업데이트"""
        # 1.사망
        data_str = re.sub(r'[N/A,None, ]', '', data[0]['total_death'])
        today_objects.death = data_str if len(data_str) != 0 else 0
        # 2.격리해제
        data_str = re.sub(r'[N/A,None, ]', '', data[0]['total_cure'])
        today_objects.cure = data_str if len(data_str) != 0 else 0
        # 3.격리중
        data_str = re.sub(r'[N/A,None, ]', '', data[0]['total_quarantine'])
        today_objects.quarantine = data_str if len(data_str) != 0 else 0
        # 4.누적확진
        data_str = re.sub(r'[N/A,None, ]', '', data[0]['total_cumulative'])
        today_objects.cumulative = data_str if len(data_str) != 0 else 0
        # 5.저장
        today_objects.save()

        # 6.나머지 데이터를 반환
        return {'msg': '업데이트', 'data': data[1:]}

    def total_data_create(self, data):
        """전세계 토탈데이터 생성"""
        # 1.사망
        data_str = re.sub(r'[N/A,None, ]', '', data[0]['total_death'])
        data1 = data_str if len(data_str) != 0 else 0
        # 2.격리해제
        data_str = re.sub(r'[N/A,None, ]', '', data[0]['total_cure'])
        data2 = data_str if len(data_str) != 0 else 0
        # 3.격리중
        data_str = re.sub(r'[N/A,None, ]', '', data[0]['total_quarantine'])
        data3 = data_str if len(data_str) != 0 else 0
        # 4.누적확진
        data_str = re.sub(r'[N/A,None, ]', '', data[0]['total_cumulative'])
        data4 = data_str if len(data_str) != 0 else 0
        # 5.생성
        WorldTotal.objects.create(
                                    death=data1,
                                    cure=data2,
                                    quarantine=data3,
                                    cumulative=data4
        )

        # 7.나머지 데이터를 반환
        return {'msg': '생성', 'data': data[1:]}

    def data_update(self, data, today_objects):
        """나라별 데이터 업데이트"""
        # 1.지역이름
        today_objects.area_name = data['country']
        # 2.누적확진
        data_str = re.sub(r'[N/A,None, ]', '', data['cumulative'])
        today_objects.cumulative = data_str if len(data_str) != 0 else 0
        # 3.격리중
        data_str = re.sub(r'[N/A,None, ]', '', data['quarantine'])
        today_objects.quarantine = data_str if len(data_str) != 0 else 0
        # 4.격리해제
        data_str = re.sub(r'[N/A,None, ]', '', data['cure'])
        today_objects.cure = data_str if len(data_str) != 0 else 0
        # 5.사망자
        data_str = re.sub(r'[N/A,None, ]', '', data['death'])
        today_objects.death = data_str if len(data_str) != 0 else 0
        # 6.저장
        today_objects.save()

        return 1

    def data_create(self, data):
        """나라별 데이터 생성"""
        # 1.지역이름
        data1 = data['country']
        # 2.누적확진
        data_str = re.sub(r'[N/A,None, ]', '', data['cumulative'])
        data2 = data_str if len(data_str) != 0 else 0
        # 3.격리중
        data_str = re.sub(r'[N/A,None, ]', '', data['quarantine'])
        data3 = data_str if len(data_str) != 0 else 0
        # 4.격리해제
        data_str = re.sub(r'[N/A,None, ]', '', data['cure'])
        data4 = data_str if len(data_str) != 0 else 0
        # 5.사망자
        data_str = re.sub(r'[N/A,None, ]', '', data['death'])
        data5 = data_str if len(data_str) != 0 else 0
        # 6.저장
        World.objects.create(
                                area_name=data1,
                                cumulative=data2,
                                quarantine=data3,
                                cure=data4,
                                death=data5
        )

        return 1

    def run(self):
        '''실행'''
        # 1. 수집한 데이터값 받기
        all_data = Crawling().run()
        # 2. 나라별 총 합계 데이터 업데이트 or 생성
        try:
            today_objects = WorldTotal.objects.get(create_time=date.today())
            all_data = self.total_data_update(all_data, today_objects)
        except WorldTotal.DoesNotExist:
            all_data = self.total_data_create(all_data)
        total_msg = all_data['msg']

        update_count = 0
        create_count = 0
        # 3. 각 나라별 데이터 업데이트 or 생성
        for area_data in all_data['data']:
            if area_data['country'] is None:
                continue
            try:
                today_objects = World.objects.get(create_time=date.today(), area_name=area_data['country'])
                update_count += self.data_update(area_data, today_objects)
            except World.DoesNotExist:
                create_count += self.data_create(area_data)

        return '세계 total 데이터 {a} 완료\n'\
               '세계 각 나라 데이터 업데이트 {b}개, 생성{c}개'\
            .format(a=total_msg, b=update_count, c=create_count)



