import requests
from bs4 import BeautifulSoup

def get_pages(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return len(soup.find("div", class_="pagination").find_all("span",class_="page"))

total_pages = get_pages("https://weworkremotely.com/remote-full-time-jobs?page=1")
  

all_jobs = []
def scrape_page(url):
    print(f"Scrapping {url}...")
    response = requests.get(url)
    #request를 이용하여 html을 가져옴

    #html parser로서 beautiful soup이용한다는 의미.

    soup = BeautifulSoup(response.content,
                        "html.parser"
    )

    jobs = soup.find("section", class_ = "jobs").find_all("li")[1:-1]
    #find로 가져온 jobs를 가진 section앨리먼트에서 find_all로 가진 list에서 슬라이싱.
    #양 끝 값이 html 분석해보니 의미 없는 값이라는 것을 알게 되어서

    #리스트를 언팩하는 메서드들. 변수를 리스트로 한번에 선언하는 것부터, 내부의 요소를 가져오는 메서드까지
    #가져온 요소들로 딕셔너리를 만든다. .text를 이용하면 태그 내부의 내용을 가져오고, []을 이용하면 attribute를 가져온다.
    for job in jobs:
        title = job.find("span", class_="title").text
        company, position, region = job.find_all("span", class_="company")
        url = job.find("div", class_="tooltip").next_sibling["href"]
        # next_sibling은 tooltip의 sibling을 가져오게 될 것이다. 개발자 도구 확인하기.
        job_data = {
            "title": title,
            "company": company.text,
            "position": position.text,
            "region": region.text,
            "url": f"https://weworkremotely.com/{url}"
        }
        all_jobs.append(job_data)


for x in range(total_pages):
    url = f"https://weworkremotely.com/remote-full-time-jobs?page={x+1}"
    scrape_page(url)

print(len(all_jobs))