from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse, parse_qs, quote, quote_plus
# from Liberfly.functions.db import db
# from Liberfly.functions.freshsales import fresh
import pandas as pd
from datetime import datetime
import os
import re
import time

client_id = 0

def msg_for_client(client_id, number_client, name_client):
    """['Método de identificar cliente']
    
    client_id = 'Identificaçao do cliente'
    number_client = 'Número de telefone do cliente'
    name_client = 'Nome do cliente'
    
    return:
    sdr:. ['Mensagem para cliente']
    """

def client_whatsapp():
    """['Método que verifica se whatsapp do cliente esta certo, atraves do number_client']
    """
def __send_msg__(number_client):
    """['Método que envia mensagem para cliente']"""

