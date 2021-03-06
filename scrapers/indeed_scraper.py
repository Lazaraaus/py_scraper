# parser/indeed_parser.py
import requests, pprint
from bs4 import BeautifulSoup
# Get Search URL 
url = 'https://www.indeed.com/jobs?'
#q=software+developer&l=United+States'

url_pagination = 'https://www.indeed.com/jobs?q=software+developer&l=United+States&start='

# Define scraper function 
def scraper(pages, location='&l=United+States', position='q=software+developer'):
    # Created variable to track returned results and variable for pagination
    results = (pages * 10) - 10
    returned_results = 0
    page_string = '&start='
    
    # Loop until  we've hit limit 
    while returned_results <= results:
        #Construct url
        r_url = url + position + location + page_string + str(returned_results) 

        # If not, Request Page 
        page = requests.get(r_url) 
        # DO THE SCRAPE STUFF
        # Parse page with BS4
        soup = BeautifulSoup(page.content, 'html.parser')

        # Find all Divs that cointain job information 
        job_info = soup.find_all("div", class_="jobsearch-SerpJobCard")

        # Re-Parse page with just jobs info 
        soup2 = BeautifulSoup(str(job_info), 'html.parser')

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

        # Zip together and print titles, companies, summaries, and locations
        for i, j, k, l in zip(job_titles, companies, job_summaries, job_locations):
            # Get key to comp_with_salary dict
            company_key = j.text.lstrip()
            # If key in dict, print salary info along with job info 
            if company_key in comp_with_salary.keys():
                print(i.text.lstrip() + "\n" + j.text.lstrip() + "\n" + comp_with_salary[company_key] + "\n" + k.text.strip() + "\n" + l.text.lstrip() + "\n")
            # Else just print job info
            else:
                print(i.text.lstrip() + "\n" + j.text.lstrip() + "\n" + k.text.strip() + "\n" + l.text.lstrip() + "\n")

        # Increment returned_results 
        returned_results += 10
    # We've hit the limit         
    else:
        # WE HAVE REACHED END OF DESIRED RESULTS 
        print("Its done!") 

scraper(2)

"""
Indeed is scraped extremely well by BS4 due to its non-dynamic nature. This section of code here will serve as a basis for the static web scraper functionality later on. 

Longitudinally this functionality is going to exist in a Django back-end that will serve a Vue front-end
"""
