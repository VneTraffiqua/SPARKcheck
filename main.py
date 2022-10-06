from suds.client import Client
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import lxml


def get_spark_info(inn):
    company_risk_factors = client.service.GetCompanyRiskFactors(
        inn=inn
    )
    company_risk_factors_dict = Client.dict(company_risk_factors)
    company_stat = company_risk_factors_dict['xmlData']
    soup = BeautifulSoup(company_stat, 'lxml')
    company_name = soup.find('shortname')
    company_inn = soup.find('inn')
    company_status = soup.find('status')
    consolidated_company_indicator = soup.find(
        'consolidatedindicator'
    )
    diligence_indicator = soup.find(
        'addfield', {'name': 'IndexOfDueDiligence'}
    )
    failure_score_indicator = soup.find(
        'addfield', {'name': 'FailureScore'}
    )

    payment_indicator = soup.find(
        'addfield', {'name': 'PaymentIndex'}
    )
    risk_factors = soup.find_all('riskfactors')
    # print(soup.prettify())
    if company_stat:
        print('Название компании: ', company_name.text)
        print('ИНН компании: ', company_inn.text)
        print('Статус компании: ', company_status['text'])
    if consolidated_company_indicator:
        print('Сводный индикатор риска СПАРК: ',
              consolidated_company_indicator['description'])
    if diligence_indicator:
        print(' Индикатор должной осмотрительности: ',
              diligence_indicator.text)
    if failure_score_indicator:
        print(' Индикатор финансового риска: ',
              failure_score_indicator.text)
    if payment_indicator:
        print(' Индикатор платежной дисциплины: ', payment_indicator.text)
    print('Факторы риска:')
    for risk_factor in risk_factors:
        risk_soup = risk_factor.find('factor')
        risk = risk_soup['name']
        risk_id = risk_soup['id']
        print('id =', risk_id, ',', risk)
        print('Дополнительная информация по фактору:')
        addfield = risk_soup.find('addinfo').find_all('addfield')
        print(addfield)
    print('=======================================================')


if __name__ == '__main__':
    load_dotenv()
    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')

    inn_list = ['7813231543', '7838503686', '7707511820', '5024177951', '7743856281', '7719269331', '0814162716', '7801443529']

    url = 'http://sparkgatetest.interfax.ru/iFaxWebService'
    client = Client(url)
    session_open = client.service.Authmethod(
        Login=login, Password=password
    )
    print('session open =', session_open)
    try:
        for inn in inn_list:
            get_spark_info(inn)
        # get_spark_info('7707273453')
    except AttributeError:
        print('Данные не найдены')
    finally:
        session_closed = client.service.End()
        print('session closed = ', session_closed)

