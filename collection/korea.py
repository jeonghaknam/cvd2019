# coding=utf-8
import re
import requests
from lxml import etree
from datetime import date
from cvd2019.models import DomesticTotal, Domestic


class Crawling:
    """
    국내데이터 수집
    ** 크롤링 URL: http://ncov.mohw.go.kr/
                 (질병관리본부)
    """
    def __init__(self):
        self.url_temp = "http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}

    def get_url_list(self):
        '''url 리스트 생성'''
        return [self.url_temp.format(i) for i in [11, 13]]

    def parse_url(self, url):
        ''' 응답코드 반환'''
        response = requests.get(url, headers=self.headers)

        return response.content.decode()

    def save_html(self, html_str, page_num):
        ''' 필요한 데이터 필터링 및 반환 (type: list)
            * html_str = 응답코드
            * page_num = 1 or 2 (type: int)
        '''
        html = etree.HTML(html_str)
        item = []
        data1 = {}
        # 첫번째 페이지에서 해외유입 데이터만 수집
        if page_num == 1:
            data1["total_overseas"] = html.xpath('//*[@id="content"]/div/div[3]/table/tbody/tr[1]/td[2]/text()')[0] if len(
                html.xpath('//*[@id="content"]/div/div[3]/table/tbody/tr[1]/td[2]/text()')) > 0 else None
            item.append(data1)

            return item

        # 두번째 페이지에서 통합 및 각지역 데이터를 수집
        else:
            # 1. 총 합계 데이터
            data1["total_cumulative"] = html.xpath('//*[@id="mapAll"]/div/ul/li[1]/div[2]/span/text()')[0] if len(
                html.xpath('//*[@id="mapAll"]/div/ul/li[1]/div[2]/span/text()')) > 0 else None
            data1["total_cure"] = html.xpath('//*[@id="mapAll"]/div/ul/li[4]/div[2]/span/text()')[0] if len(
                html.xpath('//*[@id="mapAll"]/div/ul/li[4]/div[2]/span/text()')) > 0 else None
            data1["total_death"] = html.xpath('//*[@id="mapAll"]/div/ul/li[5]/div[2]/span/text()')[0] if len(
                html.xpath('//*[@id="mapAll"]/div/ul/li[5]/div[2]/span/text()')) > 0 else None
            data1["total_quarantine"] = html.xpath('//*[@id="mapAll"]/div/ul/li[3]/div[2]/span/text()')[0] if len(
                html.xpath('//*[@id="mapAll"]/div/ul/li[3]/div[2]/span/text()')) > 0 else None
            item.append(data1)

            # 2. 각 지역 데이터
            tr_list = html.xpath('//*[@id="content"]/div/div[5]/table/tbody/tr')
            for i in tr_list:
                data = {}
                data["country"] = i.xpath('./th/text()')[0] if len(i.xpath('./th/text()'))>0 else None
                data["cure"] = i.xpath('./td[6]/text()')[0] if len(i.xpath('./td[6]/text()'))>0 else None
                data["death"] = i.xpath('./td[7]/text()')[0] if len(i.xpath('./td[7]/text()')) > 0 else None
                data["quarantine"] = i.xpath('./td[5]/text()')[0] if len(i.xpath('./td[5]/text()')) > 0 else None
                data["cumulative"] = i.xpath('./td[4]/text()')[0] if len(i.xpath('./td[4]/text()'))>0 else None
                item.append(data)

            return item

    def run(self):
        # 1.url리스트 생성
        url_list = self.get_url_list()
        covid19_data = []
        for url in url_list:
            # 2.요청 응답코드-받기
            html_str = self.parse_url(url)
            # 3.크롤링한 페이지 순서 판단
            page_num = url_list.index(url) + 1
            # 4.데이터 필터링, 반환값 합치기
            covid19_data += self.save_html(html_str, page_num)

        return covid19_data


class MysqlSave:
    """수집한 데이터를 데이터베이스에 업데이트 및 생성
    0시 이전일 경우 데이터 업데이트
    0시 이후 새로운 데이터 생성
    """
    def total_data_update(self, data, today_objects):
        '''국내 토탈데이터 업데이트'''
        # 1.사망
        data_str = re.sub(r'[N/A, ]', '', data[1]['total_death'])
        today_objects.death = data_str if len(data_str) != 0 else 0
        # 2.누적확진
        data_str = re.sub(r'[N/A, ]', '', data[1]['total_cumulative'])
        today_objects.cumulative = data_str if len(data_str) != 0 else 0
        # 3.격리해제
        data_str = re.sub(r'[N/A, ]', '', data[1]['total_cure'])
        today_objects.cure = data_str if len(data_str) != 0 else 0
        # 4.격리중
        data_str = re.sub(r'[N/A, ]', '', data[1]['total_quarantine'])
        today_objects.quarantine = data_str if len(data_str) != 0 else 0
        # 5.해외유입
        data_str = re.sub(r'[N/A, ]', '', data[0]['total_overseas'])
        today_objects.overseas = data_str if len(data_str) != 0 else 0
        # 6.저장
        today_objects.save()

        # 7.나머지 데이터를 반환
        return {'msg': '업데이트', 'data': data[2:]}

    def total_data_create(self, data):
        '''국내 토탈데이터 생성'''
        # 1.사망
        data_str = re.sub(r'[N/A, ]', '', data[1]['total_death'])
        data1 = data_str if len(data_str) != 0 else 0
        # 2.누적확진
        data_str = re.sub(r'[N/A, ]', '', data[1]['total_cumulative'])
        data2 = data_str if len(data_str) != 0 else 0
        # 3.격리해제
        data_str = re.sub(r'[N/A, ]', '', data[1]['total_cure'])
        data3 = data_str if len(data_str) != 0 else 0
        # 4.격리중
        data_str = re.sub(r'[N/A, ]', '', data[1]['total_quarantine'])
        data4 = data_str if len(data_str) != 0 else 0
        # 5.해외유입
        data_str = re.sub(r'[N/A, ]', '', data[0]['total_overseas'])
        data5 = data_str if len(data_str) != 0 else 0
        # 6.생성
        DomesticTotal.objects.create(
                                    death=data1,
                                    cumulative=data2,
                                    cure=data3,
                                    quarantine=data4,
                                    overseas=data5
        )

        # 7.나머지 데이터를 반환
        return {'msg': '생성', 'data': data[2:]}

    def data_update(self, data, today_objects):
        '''국내 지역별 데이터 업데이트'''
        # 1.지역이름
        today_objects.area_name = data['country']
        # 2.누적확진
        data_str = re.sub(r'[N/A, ]', '', data['cumulative'])
        today_objects.cumulative = data_str if len(data_str) != 0 else 0
        # 3.격리중
        data_str = re.sub(r'[N/A, ]', '', data['quarantine'])
        today_objects.quarantine = data_str if len(data_str) != 0 else 0
        # 4.격리해제
        data_str = re.sub(r'[N/A, ]', '', data['cure'])
        today_objects.cure = data_str if len(data_str) != 0 else 0
        # 5.사망자
        data_str = re.sub(r'[N/A, ]', '', data['death'])
        today_objects.death = data_str if len(data_str) != 0 else 0
        # 6.저장
        today_objects.save()

        return 1

    def data_create(self, data):
        '''국내 지역별 데이터 생성'''
        # 1.지역이름
        data1 = data['country']
        # 2.누적확진
        data_str = re.sub(r'[N/A, ]', '', data['cumulative'])
        data2 = data_str if len(data_str) != 0 else 0
        # 3.격리중
        data_str = re.sub(r'[N/A, ]', '', data['quarantine'])
        data3 = data_str if len(data_str) != 0 else 0
        # 4.격리해제
        data_str = re.sub(r'[N/A, ]', '', data['cure'])
        data4 = data_str if len(data_str) != 0 else 0
        # 5.사망자
        data_str = re.sub(r'[N/A, ]', '', data['death'])
        data5 = data_str if len(data_str) != 0 else 0
        # 6.생성
        Domestic.objects.create(
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
        # 2. 지역별 합계 데이터 업데이트 or 생성
        try:
            today_total = DomesticTotal.objects.get(create_time=date.today())
            all_data = self.total_data_update(all_data, today_total)
        except DomesticTotal.DoesNotExist:
            all_data = self.total_data_create(all_data)
        total_msg = all_data['msg']

        update_count = 0
        create_count = 0
        # 3. 각 지역별 데이터 업데이트 or 생성
        for area_data in all_data['data']:
            if area_data['country'] is 'None':
                continue
            try:
                today_Domestic = Domestic.objects.get(create_time=date.today(), area_name=area_data['country'])
                update_count += self.data_update(area_data, today_Domestic)
            except Domestic.DoesNotExist:
                create_count += self.data_create(area_data)

        return '국내 total 데이터 {a} 완료\n' \
               '국내 각 지역 데이터 업데이트 {b}개, 생성{c}개'\
            .format(a=total_msg, b=update_count, c=create_count)


