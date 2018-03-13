#!/usr/bin/python3

import logging
import requests

SEARCH_URL = 'https://www.owler.com/iaApp/basicSearchCompanySuggestions.htm' \
             '?searchTerm=%s'
SEARCH_URL_COMPANY = 'https://www.owler.com/iaApp/fetchCompanyProfileData.htm'

# create logger
logger = logging.getLogger('akamai')
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# add ch to logger
logger.addHandler(ch)


def search_domain(url: str) -> None:
    response = requests.get(SEARCH_URL % url)

    if response.ok is not True:
        raise RuntimeError("search response is invalid")

    search_response = response.json()

    for company in search_response['results']:
        logger.info("Company ID: %s" % company['id'])
        logger.info("Company domain: %s" % company['primaryDomain'])
        logger.info(
            "Company SEO url: %s" % company['seoFriendlyCompanyProfileUrl']
        )

        if company['primaryDomain'] == url:
            search_company(int(company['id']))

            break


def search_company(company_id: int) -> None:
    request_data = {
        'companyId': company_id,
        'components': ['company_info', 'ceo', 'keystats', 'cp'],
        'section': 'cp'
    }

    response = requests.post(SEARCH_URL_COMPANY, json=request_data)

    if response.ok is not True:
        raise RuntimeError("company search response is invalid")

    response = response.json()

    ceo = response['ceo']['current_ceo']
    company = response['company_info']['company_details']

    logger.info("CEO: %s %s" % (ceo['first_name'], ceo['last_name']))
    logger.info("Founded: %s" % company['founded'])
    logger.info("Headquarters: %s" % company['hqAddress']['city'])
    logger.info("Employees: %s" % response['keystats']['total_employees'])


search_domain('akamai.com')
