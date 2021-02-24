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
# IMPORTS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Helper function to create JOB_CARD_SUMMARY_PATH
def make_summary_path(position):
    first_half_path = "//div[@id='SearchResults']/section["
    second_half_path = "]/div/div[@class='summary']"
    path = first_half_path + str(position) + second_half_path
    return path 

# CREATE XPATH CONSTANTS 
# JobCard and JobCard Information Xpaths
JOB_CARD_PATH = "//div[@id='SearchResults']/section"
JOB_INFO_PATH = "//div[@id='JobDescription']"

# Option tabs for ContentContainer div [Details, Highlights, Company]
INFO_OPTIONS_PATH = "//ul[@role='tablist']"

# Company Info Button, Company Info Xpaths 
COMPANY_INFO_BUTTON_PATH = "//ul[@role='tablist']/li[3]"
COMPANY_INFO_PATH = "//div[@id='AboutCompanyDescription']"
COMPANY_PROFILE_LINK = "//a[@id='AboutCompanyProfileLink']"
COMPANY_FOOTER_INFO_PATH = "//div[@id='AboutCompany']/footer"

# Highlight Info Button, Highlight Summary Info Xpath
HIGHLIGHT_INFO_BUTTON_PATH = "//ul[@role='tablist']/li[2]"
HIGHLIGHT_SUMMARY_PATH = "//div[@id='JobSummary']"


# CREATE WEBDRIVER AND URL 
# Create webdriver object
driver = webdriver.Chrome()
# Set implicit wait time
driver.implicitly_wait(5) # of seconds 
# Navigate to URL 
driver.get("https://www.monster.com/jobs/search/?q=software-development&where=United-States")
# Grab jobcard elements
job_cards = driver.find_elements_by_xpath(JOB_CARD_PATH)


# GET JOB INFORMATION 
# Create references to our position in the jobs list and Xpaths node
job_counter = 1
job_section_counter = 1 
# Create list of all jobs
all_jobs_list = []
# Create flag for company info presence
COMPANY_INFO_EXISTS = False 
# Loop through job_cards
for job in job_cards:
    print(f"\n\nStarting job cycle {job_counter - 1}") 
# JOB INFORMATION
    # Some Jobs will be non-active divs with no information and will return an Exception
    try:
        # Click Job Card
        ActionChains(driver).move_to_element(job).click(job).perform()
    except Exception as ex:
        # Catch false section divs
        # selenium.common.exceptions.WebDriverException: TypeError: rect is undefined | selenium.common.exceptions.MoveTargetOutOfBoundsException
        print(ex) 
        job_section_counter += 1 

    else:
        # Make summary_path
        summary_path = make_summary_path(job_section_counter)
        # Scrape Job summary 
        job_summary = driver.find_element_by_xpath(summary_path).text
        # Scrape Job detail info 
        job_details = driver.find_element_by_xpath(JOB_INFO_PATH).text

    # COMPANY INFORMATION
        # Get string representing ContentContainer options
        info_options = driver.find_element_by_xpath(INFO_OPTIONS_PATH).text
        # Check if 'Company' is in info_options
        if 'Company' in info_options:
        # Set COMPANY_INFO_EXISTS flag
            COMPANY_INFO_EXISTS = True 
        # SCRAPE COMPANY INFO > HIGHLIGHT INFO 
            # Click Company Info Button
            company_info_button = driver.find_element_by_xpath(COMPANY_INFO_BUTTON_PATH)
            ActionChains(driver).move_to_element(company_info_button).click(company_info_button).perform() 
            # Get Company Info
            company_info = driver.find_element_by_xpath(COMPANY_INFO_PATH).text
            # Get Company Profile Link element, then get href attribute of element  
            company_profile_link = driver.find_element_by_xpath(COMPANY_PROFILE_LINK)
            company_profile_link = company_profile_link.get_attribute('href') 
            # Get Company Footer Information
            company_footer_info = driver.find_element_by_xpath(COMPANY_FOOTER_INFO_PATH).text 

            # Click Highlight Info Button
            highlight_info_button = driver.find_element_by_xpath(HIGHLIGHT_INFO_BUTTON_PATH)
            ActionChains(driver).move_to_element(highlight_info_button).click(highlight_info_button).perform() 
            # Get Highlight Info
            highlight_info = driver.find_element_by_xpath(HIGHLIGHT_SUMMARY_PATH).text
    
        # No Company in info_options
        else:
        # SCRAPE HIGHLIGHT INFO
            # Click Highlights button
            highlight_info_button = driver.find_element_by_xpath(HIGHLIGHT_INFO_BUTTON_PATH)
            ActionChains(driver).move_to_element(highlight_info_button).click(highlight_info_button).perform() 
            # Get Highlight Info 
            highlight_info = driver.find_element_by_xpath(HIGHLIGHT_SUMMARY_PATH).text
    

    # PARSE INFO AND CONSTRUCT DS   
    # List -> Dict -> Dicts
    # Going to be it's own .py and function set  
        # Create Dict to hold job data 
        Dict = {}

        # PARSE BASIC JOB INFO
        # Split job_summary to get [job, company, location]
        job_summary = job_summary.splitlines()
        # Add values to dict  
        Dict['Job'] = job_summary[0]
        Dict['Company'] = job_summary[1]
        Dict['Location'] = job_summary[2]
        # Add Job to list
        all_jobs_list.append(Dict)
        print("Basic Job Info appended to job list") 
        print(all_jobs_list[job_counter - 1])  
        # PARSE DETAIL INFO 
        # Going to need to split job_details into three categories
        # Description | Requirements | Skills 
        # Not all categories will be guaranteed to be represented
        # Zero Dict
        Dict = {}
        # DO SOME PARSING MAGIC (NLTK?, RE?) TO SPLIT TEXT AND ADD TO DICT, SIMPLE FOR NOW 
        Dict['Description'] = job_details 
        Dict['Requirements'] = 'SOME REQUIREMENTS TEXT'
        Dict['Skills'] = 'SOME SKILLS TEXT'
        # Add dict to job in jobs list  
        print(f"Attempting to add Job Detail info to job list at index: {job_counter} - 1")
        all_jobs_list[(job_counter - 1)]['Detail Info'] = Dict 

        # GET COMPANY INFO 
        # From: company_info, company_profile_link, company_footer_info
        # Split into following possible  categories:
        # Description | Profile | Website | Industry | Headquarters | Founded | Company Size 
        if (COMPANY_INFO_EXISTS): 
            # Zero Dict
            Dict = {}
            # Split Company Footer Info 
            company_footer_info = company_footer_info.splitlines() 
            # Add description and profile link to Dict
            Dict['Description'] = company_info
            Dict['Profile'] = company_profile_link             #   i          i + 1 
            # Parse company footer info which comes in format ['Website', 'COMPANY SITE', 'Industry', 'COMPANY INDUSTRY',....]
            # Step through list by increments of 2, Dict key is i, Dict value is i + 1 
            print(f"\nThe length of company footer information is {len(company_footer_info)}\n")
            print(company_footer_info)
            # Not all Companies have even-numbered footer data tables (URGH!), usually extra social media tags 
            # Check for even-ness
            if (len(company_footer_info) % 2) == 0: 
                for i in range(0, len(company_footer_info), 2): 
                    Dict[company_footer_info[i]] = company_footer_info[i + 1] 
                # Add Dict to job in jobs list
                all_jobs_list[(job_counter - 1)]['Company Info'] = Dict 
                # Set COMPANY_INFO_EXISTS flag to False
                COMPANY_INFO_EXISTS = False
            else: 
                del company_footer_info[10] # Delete extraneous info, temp fix 
                for i in range(0, len(company_footer_info), 2):
                    Dict[company_footer_info[i]] = company_footer_info[i + 1]
                # Add Dict to job in jobs list
                all_jobs_list[(job_counter - 1)]['Company Info'] = Dict
                # Set COMPANY_INFO_EXISTS flag to False
                COMPANY_INFO_EXISTS = False 

        else:
            # Info doesn't exist 
            all_jobs_list[(job_counter - 1)]['Company Info'] = 'None' 

    # increment reference counters
        job_counter += 1
        job_section_counter += 1 

# GIVE DATA TO USER 
# Set Up 
KEEP_GOING = True
END_OF_DATA = len(all_jobs_list)
COMPANY_INFO = False 
current_job = 0
# User Interaction Loop
while (KEEP_GOING and current_job < END_OF_DATA):
    # User Query & Response 
    print("\n\tDo you want to get job info?\n")
    ans = input("\n\t(yes)/(no)\n")
    # Yes 
    if (ans == 'yes'):
        # Retrieve basic job information 
        job_title = all_jobs_list[current_job]['Job']
        job_company = all_jobs_list[current_job]['Company']
        job_location = all_jobs_list[current_job]['Location']
        # Retrieve detailed job information 
        job_description = all_jobs_list[current_job]['Detail Info']['Description']
        job_requirements = all_jobs_list[current_job]['Detail Info']['Requirements']
        job_skills = all_jobs_list[current_job]['Detail Info']['Skills']
        # Check for presence of company information 
        if (all_jobs_list[current_job]['Company Info'] != 'None'):
            # Create list to hold company information 
            company_info_list = [] 
            # Set COMPANY_INFO to True
            COMPANY_INFO = True 
            # Loop through company information dict and retrieve company information 
            for key, value in all_jobs_list[current_job]['Company Info'].items():
                info = f"\n{key} - {value}" 
                # Append information to company information list 
                company_info_list.append(info)

        # Print Information 
        print(f"\nJob Title:\t{job_title}")
        print(f"\nCompany:\t{job_company}")
        print(f"\nLocation:\t{job_location}")
        print(f"\n\nDescription:\n\t{job_description}\n")
        print(f"\nRequirements:\n\t{job_requirements}\n")
        print(f"\nSkills:\n\t{job_skills}\n\n")
        if (COMPANY_INFO):
            print("\nCompany Info:")
            for info in company_info_list:
                print(info)
            
        # Increment job counter     
        current_job += 1
        # Set COMPANY_INFO to False
        COMPANY_INFO = False 
    # No         
    else:
        # Set exit flag 
        KEEP_GOING = False 
