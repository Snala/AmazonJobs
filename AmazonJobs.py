from csv import reader
from os import path, remove
from selenium import webdriver
from urllib import parse
from bs4 import BeautifulSoup


class JobsDictionary:
    """
    Jobs Dictionary simply keeps track of the various jobs that are found with the included searches.
    This controls also importing existing jobs from CSV file, and then exporting out the jobs when processes are done.
    """
    def __init__(self):
        """ Initialize the dictionary, but does nothing else at creation (yet)."""
        self.jobs_dictionary = dict()

    def check_exist(self, key):
        """ Check if the specified key exists (Return True), or not (Return False."""
        if key in self.jobs_dictionary.keys():
            return True
        else:
            return False

    def add_to_dict(self, job_id, job_title, job_location, job_post_date, job_category, job_team, job_interest=True,
                    job_status=True, job_next_step=""):
        """ Add the job posting into the dictionary, using a nested dictionary."""
        self.jobs_dictionary[int(str(job_id).strip())] = {
            "Title": str(job_title).strip(),
            "Location": str(job_location).strip(),
            "Posted": str(job_post_date).strip(),
            "Category": str(job_category).strip(),
            "Team": str(job_team).strip(),
            "Interest": str(job_interest).strip(),
            "New": str(job_status).strip(),
            "Next Step": str(job_next_step).strip()
        }

    def dump_dictionary(self):
        """ Simply prints out the contents of the dictionary to shell."""
        for i in self.jobs_dictionary:
            print(i, self.jobs_dictionary[i])

    def write_dictionary(self, file):
        """ Write out the dictionary to the specified file, overwriting it in the process."""
        exist = path.exists(file)
        if exist:
            remove(file)
            exist = path.exists(file)
        f = open(file, "a+")
        if exist is False:
            f.write("Job ID, Title, Location, Posted, Category, Team, Interest, New, Next Step\n")
        for i in self.jobs_dictionary:
            f.write(str(i)+","+str(self.jobs_dictionary[i]['Title'])+","+str(self.jobs_dictionary[i]['Location'])+"," +
                    str(self.jobs_dictionary[i]['Posted'])+","+str(self.jobs_dictionary[i]['Category'])+"," +
                    str(self.jobs_dictionary[i]['Team'])+","+str(self.jobs_dictionary[i]['Interest'])+"," +
                    str(self.jobs_dictionary[i]['New'])+"," + str(self.jobs_dictionary[i]['Next Step'])+"\n")

    def import_dictionary(self, file):
        """ Import the dictionary from the specified file"""
        exist = path.exists(file)
        if exist:
            # If file exists, import it.
            with open(file, "r") as csvfile:
                text = reader(csvfile)
                row_id = 0
                for row in text:
                    if row_id > 0:
                        # Set the new field to False for any imports, to distinguish between old and new entries.
                        self.add_to_dict(row[0], row[1], row[2], row[3], row[4], row[5], row[6], False, row[8])
                    else:
                        # Done to skip the header row
                        row_id = row_id+1
                csvfile.close()
            print("Dictionary import complete & successful.")
        else:
            # If path does not exist, it simply prints that it is skipping the file and continues without delay.
            print("No import file, skipping import")


class JobDetails:
    def __init__(self, jobid):
        job_specific_root_url = "https://amazon.jobs/en/jobs/"
        self.job_browser = webdriver.PhantomJS()
        job_url = job_specific_root_url + str(jobid).strip() + "/"
        self.job_browser.get(job_url)
        self.page = BeautifulSoup(self.job_browser.page_source, "html.parser")
        print("Getting Details for {}.".format(jobid))

    def get_job_category(self):
        """ Gathers the Job Category by looking up the given JobID."""
        job_category = self.page.find("div", class_="association job-category-icon col-12").find(text=True)
        if job_category == "None":
            job_category = ""
        return str(job_category).replace(',', '').strip()

    def get_job_team(self):
        """Gathers the Job team by looking up the given JobID"""
        try:
            team_icon = self.page.find("div", class_="association team-icon col-12").find(text=True)
        except AttributeError:
            team_icon = ""
        return str(team_icon).replace(',', '').strip()

    def get_job_description(self):
        """Gathers the Job Description by looking up the given JobID."""
        try:
            job_desc = self.page.find("div", class_="section description").find("p").find(text=True)
        except AttributeError:
            job_desc = ""
        return str(job_desc).replace(',', '').strip()

    def cleanup(self):
        self.job_browser.close()


def search_for_jobs(url, dictionary):
    """ Search for jobs using the specified URL as the query, and the specified dictionary as the output location."""
    offset = 0  # Set an initial offset of 0, increase from there.
    page_empty = False
    while page_empty is False:
        browser = webdriver.PhantomJS()
        browser.get(url.replace("<offset>", str(offset)))
        print("Getting Listing Page {}".format(offset))
        page = BeautifulSoup(browser.page_source, "html.parser")
        if page.find("div", id="search-empty"):
            break  # Break out of the loop if the page is empty.
        jobs_list = page.find_all("div", class_="job")
        for job in jobs_list:
            job_id = int(str(job.attrs.get('data-job-id', [])).strip())
            print('Checking if {} is in dictionary.'.format(job_id))
            offset = offset + 1
            if not dictionary.check_exist(job_id):
                print('Job ID: {} not found in dictionary.'.format(job_id))
                job_title = job.find("h3", class_="job-title").find(text=True).replace(',', '')
                job_location = job.find("p", class_="location-and-id").find(text=True).split('|')
                job_location = job_location[0].strip().replace(', ', '/')
                job_posted_date = job.find("h2", class_="posting-date").find(text=True).replace(',', '').strip(
                    'Posted ')
                job_details = JobDetails(job_id)
                job_category = job_details.get_job_category()
                job_team = job_details.get_job_team()
                job_details.cleanup()
                dictionary.add_to_dict(job_id, job_title, job_location, job_posted_date, job_category, job_team)
            else:
                print("Job {} exists, skipping.".format(job_id))
        browser.close()


def main():
    search_full_url = "https://amazon.jobs/en/search?base_query=replaceme&offset=<offset>&result_limit=10&sort=recent" \
                      "&job_type=Full-Time&loc_query=Greater+Seattle+Area%2C+WA%2C+United+States&latitude=&longitude=" \
                      "&loc_group_id=seattle-metro&invalid_location=false&country=&city=&region=&county="

    search_terms_list = ('Quality Assurance Engineer', 'QA Engineer', "Quality Assurance Technician",
                         "Hardware QA Lab Technician ", "Hardware Quality Engineer")
    # search_terms_list = ('Quality Assurance Engineer IMDb TV', 'Sr. QAE, IMDb TV')  # Test that yields few results
    file_to_use = 'amazon.csv'
    search_url_list = []
    full_jobs_dict = JobsDictionary()
    full_jobs_dict.import_dictionary(file_to_use)
    for term in search_terms_list:
        search_url_list.append(search_full_url.replace('replaceme', parse.quote_plus(term)))
    for url in search_url_list:
        search_for_jobs(url, full_jobs_dict)
    # full_jobs_dict.dump_dictionary()  # Use this line for debugging the dictionary output
    full_jobs_dict.write_dictionary(file_to_use)


if __name__ == '__main__':
    main()
