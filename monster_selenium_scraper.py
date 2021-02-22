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
