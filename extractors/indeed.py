from bs4 import BeautifulSoup
from selenium import webdriver 

def get_page_count(keyword):
  base_url = "https://kr.indeed.com/jobs"

  driver = webdriver.Chrome()
  driver.get(f"{base_url}?q={keyword}")
  soup = BeautifulSoup(driver.page_source,"html.parser")

  pagination = soup.find("nav", role="navigation")
  pages = pagination.find_all("div", recursive=False)
  count = len(pages)
  
  if count == 0:
    return 1
  elif 3<=count<=5:
    return count-1
  elif count >= 6:
    return 5
    
  """for page in pages:
    if page['aria-label']=="Previous Page":
      count -= 1
    if page['aria-label']=="Next Page":
      count -= 1
  """


def extract_indeed_jobs(keyword):
  pages = get_page_count(keyword)
  #print("Found",pages,"pages")
  results =[]
  for page in range(pages):
    base_url = "https://kr.indeed.com/jobs"
    #end_url = "&limit=50"
    final_url = f"{base_url}?q={keyword}&start={page*10}"
    #print("Requesting",final_url)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) 
    driver = webdriver.Chrome("./chromedriver.exe", options=options)
    driver.get(final_url)
    
    soup = BeautifulSoup(browser.page_source,"html.parser")
    job_list = soup.find("ul",class_="jobsearch-ResultsList")
    
    #한 단계만 검색하고 싶으면 recursive=False
    jobs = job_list.find_all('li',recursive=False)
    
    # mosaic-zone은 필요없는 정보
    for job in jobs:
      zone = job.find("div", class_="mosaic-zone")
      if zone == None:
        #h2 안에 있는 a 가져옴
        anchor = job.select_one("h2 a")
        title = anchor['aria-label']
        link = anchor['href']
        company = job.find("span", class_="companyName")
        location = job.find("div", class_="companyLocation")
        job_data ={
          'link' : f"https://kr.indeed.com{link}",
          'company':company.string.replace(","," "),
          'location': location.string.replace(","," "),
          'position': title.replace(","," ") 
        }
        results.append(job_data)
  
  return results
