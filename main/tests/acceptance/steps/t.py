import os

from behave import *
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

use_step_matcher("re")







@given('I am on the "(.*)" page')
def step(context, name):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    context.selenium = webdriver.Chrome(executable_path="/Users/ardyg/Desktop/chromedriver",   chrome_options=chrome_options)
    # Go to the route
    context.selenium.get(f'http://127.0.0.1:8000/{reverse(name)}')



    # username = context.selenium.find_element(By.XPATH, "//*[@id='id_username']")
    # password = context.selenium.find_element(By.XPATH, "//*[@id='id_password']")
    # email = context.selenium.find_element(By.XPATH, "//*[@id='id_email']")







