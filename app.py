# parser/app.py

import requests, pprint
from bs4 import BeautifulSoup

# Get search page URL for US software jobs  
url = 'https://www.monster.com/jobs/search/?q=software-developer&where=United-States&intcid=skr_navigation_nhpso_searchMain'

URL = 'https://www.monster.com/jobs/search/?q=software-developer&where=United-States&intcid=skr_navigation_nhpso_searchMain&stpage=1&page=3'
# Request page 
page = requests.get(URL) 

# Parse page with BS4
soup = BeautifulSoup(page.content, 'html.parser')

# Find all DOM elements that are div's with class 'summary'
job_summaries = soup.find_all("div", class_="summary")

# Find the total number of jobs returned by result 
num_jobs = soup.find("h2", class_="figure")

# Re-Parse job_summaries  
soup2 = BeautifulSoup(str(job_summaries), 'html.parser')

# Select text span from tags with class 'company'
jobs = soup2.select(".company > span")
# Select text span from tags with class 'location'
locations = soup2.select(".location > span")
# Select h2 tag with class 'title' from tags with class 'summary'
titles = soup2.select(".title > a")
 
# Zip together titles, job and location lists and print results 
for i, j, k in zip(titles, jobs, locations):
   print(i.text + j.text + "," + k.text + "\n")

# Print number of total jobs returned 
print(num_jobs.string)
print(f"The number of jobs in this list is {len(jobs)}")
print(f"The number of locations in this list is {len(locations)}")
print(f"The number of job titles in this list is {len(titles)}")
# Testing BS4 parsing ability
#company_results = soup.find_all("div", class_="company")
#location_results = soup.find_all("div", class_"location")
#for result in company_results:
#    pprint.pprint(result.span.text)
#print(len(company_results))

#for result in location_results[2:-1]:
#    pprint.pprint(result.span.text)
#print(len(location_results))


