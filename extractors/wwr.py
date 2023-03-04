
from requests import get
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword):
  base_url = "https://weworkremotely.com/remote-jobs/search?&term="
  #get 요청
  response = get(f"{base_url}{keyword}")
  
  if response.status_code != 200:
    print("Can't request website")
  else:
    results = []
    #웹사이트를 구성하는 Html코드를 가져옴
    #response.text
    soup = BeautifulSoup(response.text, "html.parser")
    #find_all html코드에서 해당하는것을 다 찾아줌
    #class가 jobs인 section를 모두 찾아줌
    #keyword argument class_ = "jobs", 순서 상관없어짐
    jobs = soup.find_all('section', class_="jobs")
  
    for job_section in jobs:
      #li 태그만 가져옴
      job_posts = job_section.find_all('li') 
      #마지막 li태그에 들어간 view all 부분은 제외해줘야함
      job_posts.pop(-1)
      
      for post in job_posts:
        #a태그를 다 가져옴
        anchors = post.find_all('a')
        #a 태그 중 두번째, 필요한 것만 저장
        anchor = anchors[1]
        #html태그를 bs4 entity로 만들 수 있음
        #bs4 덕분에 dictionary 처럼 href에 url이 매칭되어 저장
        link = anchor['href']
  #회사명,포지션,지역 순서를 알기 때문에 이렇게 하기
        company, position, location = anchor.find_all('span', class_="company")
  #타이틀 얻기
        title = anchor.find('span',class_='title')
  #html태그 없이 데이터만 추출
        #print(company.string, position.string, location.string,title.string)
        
  #dictionary로 만들고 for Loop 밖에 저장하기
  #콤마를 제거한다
        job_data ={
          'link' : f"https://weworkremotely.com{link}",
          'company':company.string.replace(","," "),
          'location': location.string.replace(","," "),
          'position': title.string.replace(","," ") 
        }
        results.append(job_data)
        
    return results