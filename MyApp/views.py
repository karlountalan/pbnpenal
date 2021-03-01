from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json
from rest_framework.permissions import IsAuthenticated
import re

from bs4 import BeautifulSoup
import requests
from requests import get
import pandas as pd
import numpy as np
import time
import random
import os
import re
#import mysql.connector
from pandas.io import sql
#from sqlalchemy import create_engine
from itertools import cycle
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Create your views here.

user_agent_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.125',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/68.0.3440.106 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.173',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36 Edg/83.0.478.54',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.56',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.142',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36']

# db_connection = mysql.connector.connect(
#   host="52.7.60.221",
#   user="companies_api",
#   passwd="626gj46EfFk5s5zfXnLY43W",
#   database = 'companies_api_dev'
# )
# db_cursor = db_connection.cursor()
#
# sql = "SELECT * from proxylist"
# db_cursor.execute(sql)
# res = db_cursor.fetchall()
# column_names = [i[0] for i in db_cursor.description]
# prx = pd.DataFrame(res,columns=column_names)
# proxy_list = []
# for i in range(len(prx)):
#   proxy = {'http':'http://'+str(prx.iloc[i,:][0].split(':')[3])+':'+str(prx.iloc[i,:][0].split(':')[4])+'@'+str(prx.iloc[i,:][0].split(':')[1])+':'+str(prx.iloc[i,:][0].split(':')[2])+'/', 'https':'https://'+str(prx.iloc[i,:][0].split(':')[3])+':'+str(prx.iloc[i,:][0].split(':')[4])+'@'+str(prx.iloc[i,:][0].split(':')[1])+':'+str(prx.iloc[i,:][0].split(':')[2])+'/'}
#   proxy_list.append(proxy)

response = requests.get("https://api.limeproxies.com/v2/product/active" , headers={'Content-type': 'application/json','Authorization': 'Bearer 237e7e99d28d62e1f6996cfccbbd6b69532cfacd16fecaf7f9e8352c1fc9dec0'})
prod_id = response.json()[0]['id']
response = requests.get("https://api.limeproxies.com/v2/product/"+str(prod_id)+"/status" , headers={'Content-type': 'application/json','Authorization': 'Bearer 237e7e99d28d62e1f6996cfccbbd6b69532cfacd16fecaf7f9e8352c1fc9dec0'})
proxies_api = response.json()
prx = []
for i in proxies_api:
  prx.append(i['proxy'])
proxy_list = []
for i in prx:
  proxy = {'http':'http://user-62396:karlountalan09@'+str(i)+'/', 'https':'https://user-62396:karlountalan09@'+str(i)+'/'}
  proxy_list.append(proxy)
proxies = cycle(proxy_list)

def googlesearchURL(kw):
  encoded_kw = re.sub('[^A-Za-z0-9,\']+', '+', kw)
  main_gsearch_url = 'https://www.google.com/search?q='
  url = main_gsearch_url+encoded_kw
  return url


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def google_check(data):
    u_agent = random.choice(user_agent_list)
    proxy = random.choice(proxy_list)
    print('Using proxy: '+str(proxy))
    try:
        keyword = json.loads(data.body)['keyword']
        domain = json.loads(data.body)['domain']
        g_url = googlesearchURL(keyword)

        headers= {'User-Agent': u_agent, "Accept-Language": "en-US, en;q=0.5"}
        page = requests.get(g_url, headers=headers, proxies=proxy)
        soup = BeautifulSoup(page.text, 'html.parser')
        try:
          g_url = 'https://www.google.com'+soup.find('a',{'class':'spell_orig'})['href']
          page = requests.get(g_url, headers=headers, proxies=proxy)
          soup = BeautifulSoup(page.text, 'html.parser')
        except:
          pass

        n_results_string = soup.find('div', {'id':'result-stats'}).text
        for i,n in enumerate(n_results_string.split()):
            if n.replace(',','').isnumeric():
                n_results = int(n.replace(',',''))
                break

        ctr = 1
        top_rank = 0
        max_page = 5
        regex = '^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)'

        for page in range(1,max_page+1):
            if page > 1 :
                time.sleep(random.randint(1,2))
                headers= {'User-Agent': u_agent, "Accept-Language": "en-US, en;q=0.5"}
                page = requests.get(next_url, headers=headers, proxies=proxy)
                soup = BeautifulSoup(page.text, 'html.parser')

            results_soup = soup.find('div',{'id':'rso'})
            results = results_soup.find_all('div',{'class':'g'})
            for ii,row in enumerate(results):
              url = row.a['href']
              dom_url = re.findall(regex,url)[0]
              if dom_url == domain:
                  top_rank = ctr
                  break
              ctr+=1
            if top_rank != 0:
              break
            else:
                try:
                  next_url_add = soup.find('a',{'id':'pnnext'})['href']
                  next_url = 'https://www.google.com' + next_url_add
                except:
                  break

        return JsonResponse({'n_results':n_results,'top_rank':top_rank}, safe=True)
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)










# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# def IdealWeight(data):
#     try:
#         height = json.loads(data.body)['height']
#         weight = json.loads(data.body)['weight']
#         age = json.loads(data.body)['age']
#
#         return JsonResponse({'height':height, 'weight':weight, 'age':age}, safe=True)
#     except ValueError as e:
#         return Response(e.args[0],status.HTTP_400_BAD_REQUEST)


# class HelloView(APIView):
#     permission_classes = (IsAuthenticated,)
#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)
