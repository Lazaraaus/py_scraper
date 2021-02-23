"""
-> Scraper function inputs : job_position, location, pages*
-> Combine into url
-> Open webdriver and navigate to url
-> Grab all jobcard elements using xpaths
-> Loop through job cards until pages
  -> ACTION CHAINS
    - Move to and click 1st jobcard
    - Scrape job information
    - Move to and click Company info button
    - Scrape company info and profile link
    - Move to and click Company highlights
    - Check for 'Posted' text string in highlights info, scrape only that element
    - Move to next job card

*defaults: software developer, united states, all_pages
"""
# Imports 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Create Xpath Constants

# JobCard and JobCard Information Xpaths
JOB_CARD_PATH = "//div[@id='SearchResults']/section"
JOB_INFO_PATH = "//div[@id='JobDescription']"

# Option tabs for ContentContainer div [Details, Highlights, Company]
INFO_OPTIONS_PATH = "//ul[@role='tablist']"

# Company Info Button, Highlight Info Button w/ Company, Company Info Xpaths 
COMPANY_INFO_BUTTON = "//ul[@role='tablist']/li[3]"
COMPANY_INFO = "//div[@id='AboutCompanyDescription']"
COMPANY_PROFILE_LINK = "//a[@id='AboutCompanyProfileLink']"
COMPANY_FOOTER_INFO_PATH = "//div[@id='AboutCompany']/footer"
HIGHLIGHT_INFO_BUTTON_WITH_COMPANY = "//ul[@role='tablist']/li[2]"

# Highlight Info Button, Highlight Summary Info Xpath
HIGHLIGHT_INFO_BUTTON = "//ul[@role='tablist']/li[2]"
HIGHLIGHT_SUMMARY_INFO = "//div[@id='JobSummary']"

# Create webdriver object
driver = webdriver.Firefox()
# Navigate to URL 
driver.get("https://www.monster.com/jobs/search/?q=software-development&where=United-States")
# Grab jobcard elements
job_cards = driver.find_elements_by_xpath(JOB_CARD_PATH)


# Create reference to our position in the list/node for Xpaths
job_counter = 1
# Loop through job_cards
for job in job_cards:
# JOB INFORMATION    
    try:
        # MOVE TO AND CLICK JOBCARD
        ActionChains(driver).move_to_element(job).click(job).perform()
    except Exception as ex:
        # Catch false section divs
        # selenium.common.exceptions.WebDriverException: TypeError: rect is undefined | selenium.common.exceptions.MoveTargetOutOfBoundsException
        print(ex) 
    else:
        # Make summary_path
        summary_path = make_summary_path(job_counter)
        # Scrape Job summary 
        job_summary = driver.find_element_by_xpath(summary_path).text
        # Scrape Job detail info 
        job_details = driver.find_element_by_xpath(JOB_INFO_PATH).text

# COMPANY INFORMATION
    # Get string representing ContentContainer options
    info_options = driver.find_element_by_xpath(INFO_OPTIONS_PATH).text

    # Check if 'Company' is in info_options
    if 'Company' in info_options:
    # SCRAPE COMPANY INFO > HIGHLIGHT INFO 
        # Click Company Info Button
        ActionChains(driver).move_to_element(COMPANY_INFO_BUTTON).click(COMPANY_INFO_BUTTON).perform() 
        # Get Company Info
        company_info = driver.find_element_by_xpath(COMPANY_INFO).text
        # Get Company Profile Link element, then get href attribute of element  
        company_profile_link = driver.find_element_by_xpath(COMPANY_PROFILE_LINK)
        company_profile_link = company_profile_link.get_attribute('href') 
        # Get Company Footer Information
        company_footer_info = driver.find_element_by_xpath(COMPANY_FOOTER_INFO_PATH).text 

        # Click Highlight Info Button (w/ company)
        ActionChains(driver).move_to_element(HIGHLIGHT_INFO_BUTTON_WITH_COMPANY).click(HIGHLIGHT_INFO_BUTTON_WITH_COMPANY).perform() 
        # Get Highlight Info
        highlight_info = driver.find_element_by_xpath(HIGHLIGHT_SUMMARY_INFO).text
    
    # No Company in info_options
    else:
    # SCRAPE HIGHLIGHT INFO
        # Click Highlights button
        ActionChains(driver).move_to_element(HIGHLIGHT_INFO_BUTTON).click(HIGHLIGHT_INFO_BUTTON).perform() 
        # Get Highlight Info 
        highlight_info = driver.find_element_by_xpath(HIGHLIGHT_SUMMARY_INFO).text
    
# PARSE INFO AND CONSTRUCT DS   
# List -> Dict -> Dicts
# Going to be it's own .py and function 

    # Create list of jobs
    all_jobs_list = []

    # Basic Job Info
    # Split job_summary to get [job, company, location]
    job_summary = job_summary.splitlines()
    # Get split values  
    job = job_summary[0]
    company = job_summary[1]
    location = job_summary[2]
    
    # Detail Info
    # Going to need to split information into three categories
    # Description | Requirements | Skills 
    # Not all categories will be guaranteed to be represented
    # ****Could potentially split earlier to save on parsing
    detail_info = job_details

    # Company Info
    # Not guaranteed to be present 

    
# increment counter
    job_counter += 1

# Helper function to create JOB_CARD_SUMMARY_PATH
def make_summary_path(position):
    first_half_path = "//div[@id=SearchResults']/Section["
    second_half_path = "]/div/div[@class='summary']"
    path = first_half_path + str(position) + second_half_path
    return path 
