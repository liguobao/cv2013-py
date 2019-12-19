import requests
from bs4 import BeautifulSoup


def get_html(url):
    headers = {
        'Proxy-Connection': "keep-alive",
        'Cache-Control': "max-age=0",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8"
    }
    response = requests.request("GET", url, headers=headers)
    return response.text


def get_paper_detail(paper_url):
    paper_html = get_html(paper_url)
    paper_soup = BeautifulSoup(paper_html, "html.parser")
    paper_title = paper_soup.find("div", {"id": "papertitle"})
    paper_authors = paper_soup.find("div", {"id": "authors"})
    paper_abstract = paper_soup.find("div", {"id": "abstract"})
    if paper_title:
        paper_authors = paper_authors.text.split(";")[0].replace(
            "\n", "") if ";" in paper_authors.text else paper_authors.text.replace("\n", "")
        pdf_urls = [x["href"]
                    for x in paper_soup.find_all("a") if x.text == "pdf"]
        if pdf_urls:
            pdf_url = "http://openaccess.thecvf.com/" + pdf_urls[0]
        return {
            "paper_title": paper_title.text.replace("\n", ""),
            "paper_authors": paper_authors,
            "url": paper_url,
            "abstract": paper_abstract.text.replace("\n", ""),
            "pdf_url": pdf_url
        }
    return None


def get_paper_urls(index_url):
    htmlSoup = BeautifulSoup(get_html(index_url), "html.parser")
    all_paper_dts = htmlSoup.find_all("dt")
    all_paper_urls = []
    for dt in all_paper_dts:
        a_paper = dt.find("a")
        if a_paper:
            all_paper_urls.append(
                "http://openaccess.thecvf.com/"+a_paper["href"])


index_url = "http://openaccess.thecvf.com/ICCV2013.py"
all_paper_urls = get_paper_urls(index_url)

papers = []

for paper_url in all_paper_urls:
    print(f"crawl {paper_url} start.")
    paper_detail = get_paper_detail(paper_url)
    if paper_detail is None:
        print(f"crawl {paper_url} fail.")
        continue
    papers.append(paper_detail)
    print(f"crawl {paper_url} end.")
print(papers)
