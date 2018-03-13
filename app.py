import logging
import requests
from bs4 import BeautifulSoup

SEARCH_URL = 'https://www.owler.com/iaApp/basicSearchCompanySuggestions.htm?searchTerm=%s'
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
        logger.info("Company SEO url: %s" % company['seoFriendlyCompanyProfileUrl'])

        if company['primaryDomain'] == url:
            search_company(company['seoFriendlyCompanyProfileUrl'])

            break


def search_company(url: str) -> None:
    headers = {'user-agent': 'my-app'}
    request_data = {
        "companyId": "102240",
        "components": ["company_info", "ceo", "keystats", "cp"],
        "section": "cp"
    }

    company_page = requests.get(url, headers=headers)
    company_data = requests.post(SEARCH_URL_COMPANY, json=request_data)

    soup = BeautifulSoup(company_page.content, 'html.parser')

    logger.info("CEO: %s" % soup.find(itemprop="employee").get_text())
    logger.info("Founded: %s" % soup.find(itemprop="foundingDate").get_text())
    logger.info("Headquarters: %s" % soup.find(itemprop="foundingLocation").get_text())
    logger.info("Employees: %s" % soup.find(itemprop="numberOfEmployees").get_text())


search_domain('akamai.com')
