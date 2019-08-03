# AmazonJobs Search Tool
AmazonJobs is a tool for scraping data off of amazon.jobs site, matching against a search terms list you provide.

## To Run Job Search Tool:
Change the appropriate variables in main() of AmazonJobs.py, as you see fit:

    search_full_url = "https://amazon.jobs/en/search?base_query=replaceme&offset=<offset>&result_limit=10&sort=recent" \
                      "&job_type=Full-Time&loc_query=Greater+Seattle+Area%2C+WA%2C+United+States&latitude=&longitude=" \
                      "&loc_group_id=seattle-metro&invalid_location=false&country=&city=&region=&county="

    search_terms_list = ('Quality Assurance Engineer', 'QA Engineer', "Quality Assurance Technician",
                         "Hardware QA Lab Technician ", "Hardware Quality Engineer")
    file_to_use = 'amazon.csv'

## To Run Parser:
Change the appropriate fields in main(), as you see fit:

    file_name = "amazon.csv"
    banned_terms = ['manager', 'senior', 'sr', 'III', 'aerospace', 'salesforce', 'leader', 'head', 'tpm', 'robotics',
                    'management', 'mgr', 'robotic', 'buyer']

## Requirements:
    beautifulsoup4==4.8.0
    certifi==2019.6.16
    chardet==3.0.4
    idna==2.8
    phantomjs-binary==2.1.3
    requests==2.22.0
    selenium==3.141.0
    soupsieve==1.9.2
    urllib3==1.25.3
