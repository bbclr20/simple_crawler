from bs4 import BeautifulSoup
import urllib.request as request
import json
from selenium import webdriver

class GetAllUrls:

    @staticmethod
    def get_url_dict():
        base_format ="https://ic.tpex.org.tw/introduce.php?ic="
        main_page = "https://ic.tpex.org.tw/introduce.php?ic=A300"
        doc = request.urlopen(main_page).read()
        soup = BeautifulSoup(doc.decode("utf-8"), "lxml")
        selection = soup.find("select", {"id": "ic_option"})
        options = selection.find_all("option")

        result = {}
        for option in options:
            result[option.get_text()] = base_format + option["value"]
        return result

class IndustryCrawler:

    @staticmethod
    def crawl(
            executable_path="drivers/mac/firefox/29/geckodriver",
            url="https://ic.tpex.org.tw/introduce.php?ic=D000", 
            industry_name="半導體",
            json_filename="result.json",
        ):
        def _get_titles(div_chain):
            div_titles = div_chain.find_all("div", {"class": "chain-title-panel"})
            return div_titles 

        def _get_company_chains(div_chain):
            company_chains = div_chain.find_all("div", {"class": "company-chain-panel"})
            return company_chains  
        #
        # main process
        #
        with webdriver.Firefox(executable_path="drivers/mac/firefox/29/geckodriver") as driver:
            driver.get(url)
            doc = request.urlopen(url).read()
            soup = BeautifulSoup(doc.decode("utf-8"), "lxml")
      
            result = {}
            result[industry_name] = {}
            for div_chain in soup.find_all("div", {"class": "chain"}):
                div_titles = _get_titles(div_chain)
                
                for div_title in div_titles:
                    result[industry_name][div_title.get_text()] = {}
                    company_chains = _get_company_chains(div_chain)
                    for company_chain in company_chains: 
                        result[industry_name][div_title.get_text()][company_chain.get_text()] = []
                        
                        # click the panel and find the company list
                        element_id = company_chain.get("id")
                        driver.find_element_by_xpath(f"//div[@id='{element_id}']").click()
                        
                        page_html_source = driver.page_source
                        page_soup = BeautifulSoup(page_html_source, "lxml")
                        # print(page_soup.prettify())
                        company_list = page_soup.find("div", {"class": "company-list"})
                        companies = company_list.find_all("a", {"class": "company-text-over"})
                        for company in companies:
                            result[industry_name][div_title.get_text()][company_chain.get_text()].append(company.get_text())
                        
            with open(json_filename, "w") as outfile:  
                json.dump(result, outfile, ensure_ascii=False)

if __name__ == "__main__":
#    IndustryCrawler.crawl()
#    IndustryCrawler.crawl(url="https://ic.tpex.org.tw/introduce.php?ic=A300", industry_name="電動車輛產業") 
   url_dict = GetAllUrls.get_url_dict()
   for i_name, url in url_dict.items():
       print(i_name, url)
       IndustryCrawler.crawl(url=url, industry_name=i_name, json_filename=i_name+".json")