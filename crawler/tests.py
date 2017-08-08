from django.test import TestCase
import requests
from bs4 import BeautifulSoup
import re
# Create your tests here.
def hyuni_me():

    req = requests.get('http://hyuni.me/archive/')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')


    data_titles = soup.select('#sya_container > ul > li > div > a')
    data_dates = soup.find_all(class_='sya_date')

    p = re.compile('[0-9]+')

    data_box = []

    for i in range(len(data_titles)):
        data_box.append((data_titles[i], data_dates[i]))

    for i, j in data_box:
        real_date = p.findall(j.text)

        data = Data_SeongSu()
        data.title = i.text
        data.date = datetime.date(int(real_date[0]), int(real_date[1]), int(real_date[2]))
        data.site = Site_Name.objects.get(title='성수 메이커스페이스')

        if Data_SeongSu.objects.filter(date=data.date, site=data.site).exists() or time_compare(data.date,
                                                                                datetime.datetime.now().date()):
            pass
        else:
            data.save()

    datas_Seongsu = Data_SeongSu.objects.order_by('-date')

    return datas_Seongsu

hyuni_me()