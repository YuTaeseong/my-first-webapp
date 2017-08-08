# Create your views here.
from .models import Data_Digital, Data_SeongSu, Site_Name, Data_Base, Data_Hyunime
from django.shortcuts import render, get_object_or_404
from .forms import CreateUserForm
from django.shortcuts import redirect
import requests
from bs4 import BeautifulSoup
import re
import datetime
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# from django.contrib.auth.forms import UserCreationForm


def page_header(request):
    return render(request, 'crawler/page_header.html', {})

def sign_up(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sign_up_ok')
    else:
        form = CreateUserForm()
    return render(request, 'crawler/sign_up.html', {'form': form})

def sign_up_ok(request) :
    return render(request, 'crawler/sign_up_ok.html', {})

@login_required
def add_site(request) :
    user = request.user
    site_names = Site_Name.objects.all()
    site_user = Site_Name.objects.filter(users = user)

    if request.method == "POST":
        form = request.POST

        for site_id_in in form.getlist('Site_Name'):
            Site_Name.objects.get(id = site_id_in).users.add(user)
        for site_id_ex in Site_Name.objects.exclude(id__in=form.getlist('Site_Name')):
            site_id_ex.users.remove(user)

        return redirect(reverse('crawler',kwargs = {'pk': user.username}))

    return render(request, 'crawler/add_site.html', {'site_names':site_names, 'site_user':site_user})

@login_required
def add_request(request):
    return render(request, 'crawler/add_request.html')

@login_required
def crawler(request, pk):
    user = request.user
    site_user = Site_Name.objects.filter(users=user)
    data_set = {}

    for i in site_user :
        if i.pk == 2 :
            #Seongsu makerspace
            data_set[i.title] = seongsu_crawler()

        elif i.pk == 1 :
            #digital dajanggan
            data_set[i.title] = digital_crawler()

        elif i.pk == 3 :
            #digital dajanggan
            data_set[i.title] = hyunime_crawler()

    return render(request, 'crawler/crawler.html', {'data_set_keys' :data_set.keys(), 'data_set':data_set})

# datetime 형식의 변수 비교
def time_compare(timelist1, timelist2) :

    if timelist2 - timelist1 > datetime.timedelta(days=30) :
        return True
    else:
        return False

def digital_crawler():

    req = requests.get('https://www.digital-blacksmithshop.com:46115/board/list/notice')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    data_titles = soup.select(
        'tr > td'
        )

    i = 1
    valid = [False, False]

    for title in data_titles:
        if i % 5 == 2 or i % 5 == 0 :
            if i % 5 == 2 :
                real_title = title.text
                valid[0] = True
            elif i % 5 == 0 :
                date = datetime.datetime.now()
                real_date = datetime.date(int(date.strftime('%Y')), int(title.text[0:2]), int(title.text[3:]))
                valid[1] = True

            if valid[0] == True and valid[1] == True:
                data = Data_Digital()
                data.title = real_title
                data.date = real_date
                data.site = Site_Name.objects.get(title = '디지털 대장간')

                if Data_Digital.objects.filter(date=data.date).exists() or time_compare(data.date, datetime.datetime.now().date()):
                    pass
                else :
                    data.save()

                valid = [False, False]
        i = i + 1

    datas_Digital = Data_Digital.objects.order_by('-date')

    return datas_Digital

def seongsu_crawler():

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    req = requests.get(
        'http://makers.sba.kr/category/%EA%B3%A0%EA%B0%9D%EC%84%BC%ED%84%B0/%EA%B3%B5%EC%A7%80%EC%82%AC%ED%95%AD',
        headers=headers)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    data_titles = soup.find_all(class_='tit_post')
    data_dates = soup.select('#mArticle > div > div')

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


def hyunime_crawler():
    req = requests.get('http://hyuni.me/archive/')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    data_titles = soup.select('#sya_container > ul > li > div > a')
    data_dates = soup.find_all(class_='sya_date')

    p = re.compile('[0-9]+')

    data_box = []

    date = datetime.datetime.now()

    for i in range(len(data_titles)):
        data_box.append((data_titles[i], data_dates[i]))

    for i, j in data_box:
        real_date = p.findall(j.text)

        data = Data_Hyunime()
        data.title = i.text
        data.date = datetime.date(int(date.strftime('%Y')), int(real_date[0]), int(real_date[1]))
        data.site = Site_Name.objects.get(title='hyuni_me')

        if Data_Hyunime.objects.filter(date=data.date, site=data.site).exists() or time_compare(data.date,
                                                                                                datetime.datetime.now().date()):
            pass
        else:
            data.save()

    datas_Hyunime = Data_Hyunime.objects.order_by('-date')

    return datas_Hyunime