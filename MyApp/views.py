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
from itertools import cycle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Create your views here.

def googlesearchURL(kw):
  encoded_kw = re.sub('[^A-Za-z0-9,\']+', '+', kw)
  main_gsearch_url = 'https://www.google.com/search?q='
  url = main_gsearch_url+encoded_kw
  return url

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def google_check(data):
    try:
        keyword = json.loads(data.body)['keyword']
        domain = json.loads(data.body)['domain']
        g_url = googlesearchURL(keyword)

        chrome_options = webdriver.ChromeOptions()
        #caps = DesiredCapabilities().CHROME
        #caps["pageLoadStrategy"] = "none"
        chromedriver = '/Users/karlountalan/Desktop/FBBlocker/chromedriver'
        os.environ["webdriver.chrome.driver"] = chromedriver
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36")
        #driver= webdriver.Chrome('chromedriver',chrome_options=chrome_options, seleniumwire_options=proxy_options, desired_capabilities=caps)
        driver= webdriver.Chrome(chromedriver,chrome_options=chrome_options)

        driver.get(g_url)

        n_results_string = driver.find_element_by_xpath(r'//div[@id = "result-stats"]').get_attribute('innerHTML')
        print(n_results_string)

        for i,n in enumerate(n_results_string.split()):
            if n.replace(',','').isnumeric():
                n_results = int(n.replace(',',''))
                break

        ctr = 1
        top_rank = 0
        max_page = 5
        regex = '^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)'

        for page in range(1,max_page+1):
            results_ele = driver.find_element_by_xpath(r'//div[@id="rso"]')
            soup = BeautifulSoup(results_ele.get_attribute('innerHTML'), 'html.parser')
            results = soup.find_all('div',{'class':'g'})
            for ii,row in enumerate(results):
                url = row.a['href']
                dom_url = re.findall(regex,url)[0]
                print(dom_url)
                if dom_url == domain:
                    top_rank = ctr
                    break
                ctr+=1
            if top_rank != 0:
                break
            else:
                try:
                    next_button = driver.find_element_by_xpath(r'//a[@aria-label = "Page '+str(page+1)+'"]')
                    driver.execute_script("arguments[0].click();", next_button)
                except:
                    break


        driver.quit()

        return JsonResponse({'n_results':n_results,'top_rank':top_rank}, safe=True)
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)













@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def IdealWeight(data):
    try:
        height = json.loads(data.body)['height']
        weight = json.loads(data.body)['weight']
        age = json.loads(data.body)['age']

        return JsonResponse({'height':height, 'weight':weight, 'age':age}, safe=True)
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

# class IdealWeightView(APIView):
#     def POST(data):
#         try:
#             height = json.loads(data.body)['height']
#             weight = json.loads(data.body)['weight']
#             age = json.loads(data.body)['age']
#
#             return JsonResponse({'height':height, 'weight':weight, 'age':age}, safe=True)
#         except ValueError as e:
#             return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
