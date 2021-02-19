# parser/indeed_parser.py
import requests, pprint
from bs4 import BeautifulSoup
# Get Search URL 
url = 'https://www.indeed.com/jobs?q=software+developer&l=United+States'
url_pagination = 'https://www.indeed.com/jobs?q=software+developer&l=United+States&start=10'

# Request page
page = requests.get(url)

# Parse page with BS4
soup = BeautifulSoup(page.content, 'html.parser')

# Find all Divs that cointain job information 
jobs = soup.find_all("div", class_="jobsearch-SerpJobCard")

# Re-Parse page with just jobs info 
soup2 = BeautifulSoup(str(jobs), 'html.parser')

# Get tags with class 'company'
companies = soup2.select(".company")
# Get tags with class 'title'
job_titles = soup2.select(".title > a")
# Get tags with class 'summary' from tags with class 'jobsearch_SerpJobCard' 
job_summaries = soup2.select(".jobsearch-SerpJobCard > .summary") # > ul") 
# Get tags with class 'salaryText'
job_salaries = soup2.select(".salaryText")
# Get tags with class 'location'
job_locations = soup2.select(".location")

 
# Find all span tags in the DOM that have class 'salaryText'
sal_list = soup2.find_all("span", class_="salaryText")
# Create a dictionary to hold companies that have salary values
comp_with_salary = {}
# Loop through salaries in the salary list 
for sal in sal_list:
    # Get company info tag from salary tag 
    company = sal.find_previous("div", class_="sjcl")
   
    # Get company name from company tag
    comp_name = company.select(".company")
    
    #Add the salary to the dictionary using the company name as a key 
    comp_with_salary[comp_name[0].text.lstrip()] = sal.text.lstrip()

# Print the dictionary of all companies that have salary info
print(comp_with_salary)

# Zip together and print titles, companies, summaries, and locations
for i, j, k, l in zip(job_titles, companies, job_summaries, job_locations):
    print(i.text.lstrip() + "\n" + j.text.lstrip() + "\n" + k.text.strip() + "\n" + l.text.lstrip() + "\n")
