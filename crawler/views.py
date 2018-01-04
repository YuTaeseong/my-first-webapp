# Create your views here.
from .models import Site_Name
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
from django.http import JsonResponse


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
    site = Site_Name.objects.filter(users = user)

    if request.method == "POST":
        form = request.POST

        for site_id_ex in Site_Name.objects.filter(id__in=form.getlist('Site_Name')):
            site_id_ex.users.remove(user)

        return redirect('crawler')

    return render(request, 'crawler/add_site.html', {'site':site})

@login_required
def add_request(request):

    if request.method == "POST":
        url = request.POST['name']
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        link = soup.find_all(type="application/rss+xml")

        rss_list = []
        for i in link :
            rss_list.append(i.get('href'))

        if len(link) == 0 :
            html_head = soup.head
            html_head = str(html_head)
            html_head = re.sub('<head.*?>','', html_head)
            html_head = re.sub('</head.*?>','', html_head)
            html_head = re.sub('\n', '', html_head)
            html_head = re.sub('\r', '', html_head)

            html_head = re.sub(r'\\', '&bs', html_head)
            html_head = re.sub('\'', '&sq', html_head)

            html_head_final = html_head.split("</scri")

            html_body = soup.body
            html_body = str(html_body)
            html_body = re.sub('<body.*?>','', html_body)
            html_body = re.sub('</body.*?>','', html_body)
            html_body = re.sub('\n', '', html_body)
            html_body = re.sub('\r', '', html_body)

            html_body = re.sub(r'\\', '&bs', html_body)
            html_body = re.sub('\'', '&sq', html_body)

            html_body_final = html_body.split('</scri')
            #print(html_head_final)
            return render(request, 'crawler/add_request.html', { 'head' : html_head_final, 'body' : html_body_final, 'url' : url })

        return render(request, 'crawler/add_request.html', {'rss' : rss_list})

    return render(request, 'crawler/add_request.html', {})

@login_required
def crawler(request):
    sites = Site_Name.objects.filter(users=request.user)

    title_dic={}

    for i in sites :
        if i.detail :
            pass
        else :
            url = i.site

            req = requests.get(url)
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')

            title = soup.select('item > title')

            title_list = []
            for j in title:
                title_list.append(j.string);

            title_dic[i.title] = title_list

    return render(request, 'crawler/crawler.html', {'title':title_dic})

def ajax_data(request):

    url = request.GET.get('url',None)

    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.select('item > title')
    site_title = soup.select('channel > title')

    title_list=[]
    for i in title :
        title_list.append(i.string);

    site_title_string = site_title[0].string

    data = {
        'success' : title_list,
        'title' : site_title_string
    }

    return JsonResponse(data)

def add_complete(request) :
    site_url = request.GET.get('site_url',None)
    site_title = request.GET.get('site_title',None)

    if Site_Name.objects.filter(site = site_url).exists() == False :
        site = Site_Name()
        site.title = site_title
        site.site = site_url

        if request.GET.get('class',None) :
            site.detail = request.GET.get('class',None)

        site.save()
        site.users.add(request.user)
        site.save()

        data = {}
        return JsonResponse(data)

    else:
        site = Site_Name.objects.get(site = site_url)

        site.users.add(request.user)

        data = {}
        return JsonResponse(data)