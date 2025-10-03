import requests
from bs4 import BeautifulSoup

def scrape_supreme_court(case_type: str, case_number: int, year: int):
    url= f"https://main.sci.gov.in/judgements/case-status?caseType={case_type}&caseNo={case_number}&year={year}"

    response = requests.get(url, verify=False)
    if response.status_code != 200:
        return {"error": "Failed to fetch data from Supreme Court portal"}
    
    soup = BeautifulSoup(response.text, 'html.parser')

    parties = [p.text.strip() for p in soup.select(".case-parties")]
    filing_date = soup.select_one(".filing-date").text.strip() if soup.select_one(".filing-date") else ""
    next_hearing_date = soup.select_one(".next-hearing").text.strip() if soup.select_one(".next-hearing") else ""
    case_status = soup.select_one(".case-status").text.strip() if soup.select_one(".case-status") else ""

    judgements = []
    for link in soup.select(".judgements-downloads a"):
        judgements.append({
            "file_name":link.text.strip(),
            "download_url": link['href']
        })
    
    return {
        "parties": parties,
        "filing_date": filing_date,
        "next_hearing_date": next_hearing_date,
        "case_status": case_status,
        "judgements": judgements
    }