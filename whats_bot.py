from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse, parse_qs, quote, quote_plus
from Liberfly.functions.db import db
from Liberfly.functions.freshsales import fresh
import re
import time


def msg_by_subject(subject, client_name, closer_name, air_company):
    if subject == "Atraso de voo":
        msg = f"""Olá, {client_name}! Seja bem-vindo à experiência LiberFly!😃
Me chamo {closer_name}, faço parte do time de consultores da LiberFly e estou aqui para te ajudar em relação ao seu ATRASO DE VOO com a {air_company}. Para entender melhor o ocorrido, e chegar na maior compensação financeira, preciso das seguintes informações:

- Imagem da passagem original;
- Possui comprovante atraso do voo?"""
        return msg

    elif subject == "Cancelamento de voo":
        msg = f"""Olá, {client_name}! Seja bem-vindo à experiência LiberFly!😃
Me chamo {closer_name}, faço parte do time de consultores da LiberFly e estou aqui para te ajudar em relação ao seu CANCELAMENTO DE VOO com a {air_company}. Para entender melhor o ocorrido, e chegar na maior compensação financeira, preciso das seguintes informações:

- Imagem da passagem original;
- Imagem da passagem realocada;
- Possui comprovante do cancelamento?"""
        return msg

    elif subject == "Overbooking":
        msg = f"""Olá, {client_name}! Seja bem-vindo à experiência LiberFly!😃
Me chamo {closer_name}, faço parte do time de consultores da LiberFly e estou aqui para te ajudar em relação ao seu OVERBOOKING com a {air_company}. Para entender melhor o ocorrido, e chegar na maior compensação financeira, preciso das seguintes informações:

- Imagem da passagem original;
- Imagem da passagem realocada;
- Possui algum comprovante do impedimento de embarque?"""
        return msg

    elif subject == "Dano em bagagem":
        msg = f"""Olá, {client_name}! Seja bem-vindo à experiência LiberFly!😃
Me chamo {closer_name}, faço parte do time de consultores da LiberFly e estou aqui para te ajudar em relação ao seu dano de bagagem com a {air_company}. Para entender melhor o ocorrido, e chegar na maior compensação financeira, preciso das seguintes informações:
- Imagem da bagagem danificada
- Imagem da passagem original
- Você registrou alguma reclamação no balcão da companhia aérea e recebeu algum documento de registro?"""
        return msg

    elif subject == "Extravio de bagagem definitivo":
        msg = f"""Olá, {client_name}! Seja bem-vindo à experiência LiberFly!😃
Me chamo {closer_name}, faço parte do time de consultores da LiberFly e estou aqui para te ajudar em relação ao seu extravio de bagagem com a {air_company}. Para entender melhor o ocorrido, e chegar na maior compensação financeira, preciso das seguintes informações:

- Imagem da passagem original
- Você registrou alguma reclamação no balcão da companhia aérea e recebeu algum documento de registro?"""
        return msg

    elif subject == "Extravio de bagagem temporário":
        msg = f"""Olá, {client_name}! Seja bem-vindo à experiência LiberFly!😃
Me chamo {closer_name}, faço parte do time de consultores da LiberFly e estou aqui para te ajudar em relação ao seu extravio de bagagem com a {air_company}. Para entender melhor o ocorrido, e chegar na maior compensação financeira, preciso das seguintes informações:

- Imagem da passagem original
- Você registrou alguma reclamação no balcão da companhia aérea e recebeu algum documento de registro?"""
        return msg

    elif subject == "Bagagem furtada":
        msg = f"""Olá, {client_name}! Seja bem-vindo à experiência LiberFly!😃
Me chamo {closer_name}, faço parte do time de consultores da LiberFly e estou aqui para te ajudar em relação ao furto de bagagem com a {air_company}. Para entender melhor o ocorrido, e chegar na maior compensação financeira, preciso das seguintes informações:

- Imagem da passagem original
- Você registrou alguma reclamação no balcão da companhia aérea e recebeu algum documento de registro?"""
        return msg

    elif subject == "No-show":
        msg = f"""Olá, {client_name}! Seja bem-vindo à experiência LiberFly!😃
Me chamo {closer_name}, faço parte do time de consultores da LiberFly e estou aqui para te ajudar em relação ao seu NO-SHOW com a {air_company}. Para entender melhor o ocorrido, e chegar na maior compensação financeira, preciso das seguintes informações:

- Imagem da passagem original;
- Você tentou embarcar no voo que foi cancelado?
- Possui comprovante do cancelamento?"""
        return msg

    elif subject == "Outro":
        msg = f"""Olá, {client_name}! Seja bem-vindo à experiência LiberFly!😃
Me chamo {closer_name}, faço parte do time de consultores da LiberFly e estou aqui para te ajudar em relação ao seu transtorno com a {air_company}. Para entender melhor o ocorrido, e chegar na maior compensação financeira, preciso das seguintes informações:

- Imagem da passagem original;"""
        return msg

    elif subject == "Novo Coronavírus (COVID-19)":
        msg = f"""Olá, {client_name}! Seja bem-vindo à experiência LiberFly!😃
Me chamo {closer_name}, faço parte do time de consultores da LiberFly e estou aqui para te ajudar em relação ao seu transtorno com a {air_company}. Para entender melhor o ocorrido, e chegar na maior compensação financeira, preciso das seguintes informações:

- Imagem da passagem original;
- Qual foi a data em que adquiriu a passagem?"""
        return msg


def get_new_deals():
    return db().select(
        """
        SELECT d.deal_id, d.name, d.cf_assunto, 
        SUBSTRING_INDEX(SUBSTRING_INDEX(u.display_name, ' ', 1), ' ', -1) AS owner_name,
        u.mobile_number, ds.deal_stage_name, c.first_name, c.mobile_number AS client_mobile
        FROM liberfly.freshsales_deals d, liberfly.freshsales_deal_stages ds, liberfly.freshsales_users u, liberfly.freshsales_deal_contacts dc, liberfly.freshsales_contacts c
        WHERE d.deal_stage_id = ds.deal_stage_id
        AND dc.deal_id = d.deal_id
        AND c.contact_id = dc.contact_id
        AND d.owner_id = u.freshsales_user_id
        AND c.cf_agencia_intermediadora = 0
        AND c.cf_companhia_aerea = 0
        AND ds.deal_stage_name LIKE "Novo"
        """
    )


def get_owner_deals(deals, number):
    owner_deals = []

    for deal in deals:
        if deal['mobile_number'] == number:
            owner_deals.append(deal)

    return owner_deals


def get_owner_whatsapp_number():
    image_url = driver.find_element_by_xpath(
        "//*[@id='side']/header/div[1]/div/img")
    val = image_url.get_attribute("src")
    o = urlparse(val)
    query = parse_qs(o.query)
    number = query['u']
    number = re.sub('[^0-9]', '', number[0])
    return number


def blacklist(cf_assunto):
    for subject in cf_assunto:
        if subject == "Perdi compromisso, mas não consigo comprovar" or subject == "Perdi e tenho comprovantes" or subject == "Não perdi":
            cf_assunto.remove(subject)

    return cf_assunto


def format_client_number(number):
    return re.sub('[^0-9]', '', number)


def get_subject(subject):
    subject = deal['cf_assunto'].split(";")
    subject = blacklist(subject)
    if len(subject) > 1 and subject[0] == 'Outro':
        return subject[1]
    else:
        return subject[0]


def get_air_company(deal_id):
    air_company = db().select(
        f"""
    SELECT c.first_name
    FROM liberfly.freshsales_deals d, liberfly.freshsales_deal_stages ds, liberfly.freshsales_users u, liberfly.freshsales_deal_contacts dc, liberfly.freshsales_contacts c
    WHERE d.deal_stage_id = ds.deal_stage_id
    AND dc.deal_id = d.deal_id
    AND c.contact_id = dc.contact_id
    AND d.owner_id = u.freshsales_user_id
    AND c.cf_companhia_aerea = 1
    AND ds.deal_stage_name LIKE "Novo"
    AND d.deal_id = {deal_id}
    """
    )
    return air_company[0]['first_name']


if __name__ == "__main__":
    try:
        driver = webdriver.Chrome()
        deals = get_new_deals()
        driver.get("https://web.whatsapp.com/")
        driver.implicitly_wait(15)
        number = get_owner_whatsapp_number()
        owner_deals = get_owner_deals(deals, number)
        for deal in owner_deals:
            client_number = format_client_number(deal['client_mobile'])
            subject = get_subject(deal['cf_assunto'])
            msg = msg_by_subject(
                subject, deal['first_name'], deal['owner_name'], get_air_company(deal['deal_id']))
            msg = quote_plus(msg)
            driver.get(
                f"https://api.whatsapp.com/send?phone={client_number}&text={msg}")
            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                            'Timed out waiting for PA creation ' +
                                            'confirmation popup to appear.')

                alert = driver.switch_to.alert
                alert.accept()
                print("alert accepted")
            except TimeoutException:
                print("no alert")

            time.sleep(2)
            driver.find_element_by_class_name(
                "_whatsapp_www__block_action").click()
            time.sleep(2)
            driver.find_element_by_xpath(
                "//*[@id='fallback_block']/div/div/a").click()
            time.sleep(2)
            driver.find_element_by_xpath(
                "//*[@id='main']/footer/div[1]/div[3]/button/span").click()

            r = fresh().change_deal_stage(deal['deal_id'], 8000175215, deal_pipeline_id=8000024894)
            print(r)
    except:
        driver.close()