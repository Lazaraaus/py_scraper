# parser/app.py

import requests, pprint
from bs4 import BeautifulSoup

# Get search page URL for US software jobs  
url = 'https://www.monster.com/jobs/search/?'

URL = 'https://www.monster.com/jobs/search/?q=software-developer&where=United-States&intcid=skr_navigation_nhpso_searchMain&stpage=1&page=3'

def scraper_monster(pages, location='&where=United-States', position='q=software-development'):
    # Build page string variable and  URL
    page_string = '&page='
    r_url = url + position + location + page_string + str(pages) 

    # Request page 
    page = requests.get(r_url) 

    # Parse page with BS4
    soup = BeautifulSoup(page.content, 'html.parser')

    # Find all DOM elements that are div's with class 'summary'
    job_summaries = soup.find_all("div", class_="summary")

    # Find the total number of jobs returned by result 
    num_jobs = soup.find("h2", class_="figure")

    # Re-Parse job_summaries  
    soup2 = BeautifulSoup(str(job_summaries), 'html.parser')

    # Select text span from tags with class 'company'
    company = soup2.select(".company > span")
    # Select text span from tags with class 'location'
    locations = soup2.select(".location > span")
    # Select h2 tag with class 'title' from tags with class 'summary'
    titles = soup2.select(".title > a")

    # Zip together titles, job and location lists and print results 
    for i, j, k in zip(titles, company, locations):
        print(i.text + j.text + "," + k.text + "\n")

    # Print number of total jobs returned 
    print(num_jobs.string)
    print(f"The number of jobs in this list is {len(company)}")
    print(f"The number of locations in this list is {len(locations)}")
    print(f"The number of job titles in this list is {len(titles)}")

scraper_monster(5) 

"""
Gonna look into selenium for scraping Monster. Should be able to grab more information, salary, job info blurb, etc. This format works for indeed, but monster is going to need a dynamic scraper. The selenium scraper for monster will form the basis for the dynamic scraper functionality. 

Longintudinally this functionality will exist in a Django back-end serving a Vue front-end.
"""
