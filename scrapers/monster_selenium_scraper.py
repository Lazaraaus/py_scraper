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
import json 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from config import (
    JOB_CARD_PATH,
    JOB_INFO_PATH,
    INFO_OPTIONS_PATH,
    COMPANY_INFO_BUTTON_PATH,
    COMPANY_INFO_PATH,
    COMPANY_PROFILE_LINK,
    COMPANY_FOOTER_INFO_PATH,
    HIGHLIGHT_INFO_BUTTON_PATH,
    HIGHLIGHT_SUMMARY_PATH,
    SPONSORED_OPPORTUNITY_INFO_PATH,
    SPONSORED_OPPORTUNITY_COMPANY_INFO,
    LOAD_MORE_JOBS)

# Function to create JOB_CARD_SUMMARY_PATH
def make_summary_path(position):
    first_half_path = "//div[@id='SearchResults']/section["
    second_half_path = "]/div/div[@class='summary']"
    path = first_half_path + str(position) + second_half_path
    return path 

# Function which extracts information from Monster job_card elements 
def extract_info(jobs, prev_position=0):
    """ Gets job information from list of jobcard elements """
    # Create references to our position in the jobs list and Xpaths node
    job_counter = 1
    job_section_counter = 1 
    # Create list of all jobs
    all_jobs_list = []
    # Create flag for company info presence
    COMPANY_INFO_EXISTS = False 
    # Create flag for sponsored opportunities
    SPONSORED_OPPORTUNITY = False 
    # Create flag for info option presence
    INFO_OPTIONS = False 
    # Loop through job_cards
    for job in job_cards[prev_position:]:
        print(f"\n\nStarting job cycle {job_counter - 1}") 
    # JOB INFORMATION  
    # Some Jobs will be non-active divs with no information and will return an Exception
    # Some jobs will be sponsored content divs aka job_card ads
    # Some jobs will be sponsored opportunities sometimes with info_options, sometimes w/o info_options 
        # Obtain attributes for sponsored content & sponsored opportunities 
        sponsored_content_attrib = job.get_attribute('data-mux')
        sponsored_opportunity_attrib = job.get_attribute('data-ssr')

        # If sponsored content, increment job_section_counter and skip this iteration 
        if (sponsored_content_attrib == 'searchResultsAds'):
            job_section_counter += 1
            continue 

        # If sponsored opportunity, set appropriate flag to True 
        # Unnecessary for its original intended purpose, but might be useful down the road so keeping Flag and check 
        elif (sponsored_opportunity_attrib == 'true'):
            # We have to skip checking for info_options 
            SPONSORED_OPPORTUNITY = True 

        try:
            # Click Job Card
            ActionChains(driver).move_to_element(job).click(job).perform()
        except Exception as ex:
            # Catch false section divs
            print(ex) 
            job_section_counter += 1 

        else:
            # Make summary_path
            summary_path = make_summary_path(job_section_counter)
            # Scrape Job summary 
            job_summary = driver.find_element_by_xpath(summary_path).text
            # Scrape Job detail info 
            job_details = driver.find_element_by_xpath(JOB_INFO_PATH).text
            # CHECK FOR INFO OPTIONS 
            try:
                info_options = driver.find_element_by_xpath(INFO_OPTIONS_PATH).text
            except Exception as ex:
                # ISSUE - Some problem with Selenium and selecting an element after an error occurs. Unable to select SPONSONRED_OPPORTUNITY_INFO_PATH after exception
                # even though Xpath has been confirmed good and element definitely exists in the DOM. Gonna make a thread on reddit and ask python Discord 
                print(ex)
                job_section_counter += 1
                continue 
            else: 
                INFO_OPTIONS = True 

        # COMPANY INFORMATION
            # Check for INFO_OPTIONS Flag       
            if (INFO_OPTIONS):
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

                    # Reset INFO_OPTIONS Flag 
                    INFO_OPTIONS = False 
        
                # No Company in info_options
                else:
                # SCRAPE HIGHLIGHT INFO
                    # Click Highlights button
                    highlight_info_button = driver.find_element_by_xpath(HIGHLIGHT_INFO_BUTTON_PATH)
                    ActionChains(driver).move_to_element(highlight_info_button).click(highlight_info_button).perform() 
                    # Get Highlight Info 
                    highlight_info = driver.find_element_by_xpath(HIGHLIGHT_SUMMARY_PATH).text

                    # Reset INFO_OPTIONS Flag
                    INFO_OPTIONS = False 
        
            else:
                # Get Job Details for sponsored opportunity 
                job_details = driver.find_element_by_xpath(SPONSORED_OPPORTUNITY_INFO_PATH).text 

        # PARSE INFO AND CONSTRUCT DS   
        # List -> Dict -> Dicts 
            # Create Dict to hold job data 
            Dict = {}

            # PARSE BASIC JOB INFO
            # Split job_summary to get [job, company, location]
            job_summary = job_summary.splitlines()
            # Add values to dict  
            Dict['Job'] = job_summary[0].strip()
            Dict['Company'] = job_summary[1].strip()
            Dict['Location'] = job_summary[2].strip()
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
            Dict['Description'] = job_details.strip() 
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
                Dict['Description'] = company_info.strip()
                Dict['Profile'] = company_profile_link.strip()      #   i          i + 1 
                # Parse company footer info which comes in format ['Website', 'COMPANY SITE', 'Industry', 'COMPANY INDUSTRY',....]
                # Step through list by increments of 2, Dict key is i, Dict value is i + 1 
                print(f"\nThe length of company footer information is {len(company_footer_info)}\n")
                print(company_footer_info)
                # Not all Companies have even-numbered footer data tables (URGH!), usually extra social media tags 
                # Check for even-ness
                if (len(company_footer_info) % 2) == 0: 
                    for i in range(0, len(company_footer_info), 2): 
                        Dict[company_footer_info[i].strip()] = company_footer_info[i + 1].strip() 
                    # Add Dict to job in jobs list
                    all_jobs_list[(job_counter - 1)]['Company Info'] = Dict 
                    # Set COMPANY_INFO_EXISTS flag to False
                    COMPANY_INFO_EXISTS = False
                else: 
                    del company_footer_info[10] # Delete extraneous info, temp fix 
                    for i in range(0, len(company_footer_info), 2):
                        Dict[company_footer_info[i].strip()] = company_footer_info[i + 1].strip()
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

    # Return collected and parsed information 
    return all_jobs_list 

# Function to return extracted information from Monster job_card elements 
def give_data(jobs):
    # GIVE DATA TO USER 
    # Set Up 
    KEEP_GOING = True
    END_OF_DATA = len(jobs)
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
            job_title = jobs[current_job]['Job']
            job_company = jobs[current_job]['Company']
            job_location = jobs[current_job]['Location']
            # Retrieve detailed job information 
            job_description = jobs[current_job]['Detail Info']['Description']
            job_requirements = jobs[current_job]['Detail Info']['Requirements']
            job_skills = jobs[current_job]['Detail Info']['Skills']
            # Check for presence of company information 
            if (jobs[current_job]['Company Info'] != 'None'):
                # Create list to hold company information 
                company_info_list = [] 
                # Set COMPANY_INFO to True
                COMPANY_INFO = True 
                # Loop through company information dict and retrieve company information 
                for key, value in jobs[current_job]['Company Info'].items():
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

# Function to get inputs (position, location) and create a URL for selenium driver 
def get_inputs():
    # Greet User and ask for Input
    print("\n\nHello, ready to get some job information?")
    print("\nFirst I'll need some things from you.")
    print("\nWhat kind of job are you looking for?")
    position = input("\n\tPosition: ") # Need to implement input checks
    print("\nOkay and how about location?")
    location = input("\n\tLocation: ") # Need to implement input checks
    print("\nOkay, building URL....")

    # Construct URL
    # Split position input for individual words 
    position = position.split()
    # Start the position_string with the non-input portion 
    position_string = '?q='
    # Get loop counter 
    counter = 0  
    for word in position:
        # if counter isn't at the last word, add '-'
        if not counter == len(position):
            position_string = position_string + word + '-'
        # If so, don't add '-'   
        elif counter == len(postion):
            position_string = position_string + word 

    # Split location input for individual words, same as above 
    location = location.split() 
    location_string = '&where='
    counter = 0
    for word in location:
        if not counter == len(location):
            location_string = location_string + word + '-'
        elif counter == len(position):
            locaiton_string = location_string + word 

    # Concatenate input strings to search URL 
    url = 'https://www.monster.com/jobs/search/' + position_string + location_string
    # Return  
    return url 

# Function to get number of pages 
def get_num_pages():
    print("\n\nWe have finished constructing the URL")
    pages = input("\nHow many pages of job information would you like?")
    print("Okey Dokey!") 
    return int(pages)
         
# CREATE WEBDRIVER AND URL 
# Create webdriver object
driver = webdriver.Chrome()
# Set implicit wait time
driver.implicitly_wait(5) # of seconds 

# Create url from inputs and get number of pages to scrape
url = get_inputs() 
pages = get_num_pages() 

# Navigate to URL 
driver.get(url)

# Grab jobcard elements 
#job_cards = driver.find_elements_by_xpath(JOB_CARD_PATH)

# List of jobs_data structures 
job_meta_list = [] 

# Get load more jobs button
load_more = driver.find_element_by_xpath(LOAD_MORE_JOBS)

# Variable for last position of job_card crawler 
last_position = 0

# Loop through pages, extract info 
for x in range(1, pages + 1):
    if x == 1:
        job_cards = driver.find_elements_by_xpath(JOB_CARD_PATH)
        jobs_data = extract_info(job_cards) 
        last_position = len(job_cards)
        job_meta_list.append(jobs_data) 
        ActionChains(driver).click(load_more).perform() 
    else:
        # Grab Job card elements
        job_cards = driver.find_elements_by_xpath(JOB_CARD_PATH) 
        # Get data 
        jobs_data = extract_info(job_cards, last_position) 
        # Append to master list 
        job_meta_list.append(jobs_data)
        # Load more job cards 
        ActionChains(driver).click(load_more).perform() 

# GET JOB INFORMATION 
#jobs_data = extract_info(job_cards)

# STORE JOB INFORMATION 
#filename = 'monster_jobs.json'
#with open(filename, 'w') as f:
#    json.dump(jobs_data, f)
#    print("All job data saved") 

# GIVE JOB INFORMATION
for jobs_data in job_meta_list: 
    print(len(job_meta_list))
    give_data(jobs_data) 

