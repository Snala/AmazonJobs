import AmazonJobs
from textwrap import TextWrapper


def main():
    file_name = "amazon.csv"
    banned_terms = ['manager', 'senior', 'sr', 'III', 'aerospace', 'salesforce', 'leader', 'head', 'tpm', 'robotics',
                    'management', 'mgr', 'robotic', 'buyer']
    parse_dictionary = AmazonJobs.JobsDictionary()
    print("Attempting to import dictionary from {}".format(file_name))
    parse_dictionary.import_dictionary(file_name)
    reviewed = 0
    for job in parse_dictionary.jobs_dictionary:
        reviewed = reviewed + 1
        if bool(parse_dictionary.jobs_dictionary[job]['Interest']):
            job_title = str(parse_dictionary.jobs_dictionary[job]['Title'])
            for term in banned_terms:
                if term.lower() in str(parse_dictionary.jobs_dictionary[job]['Title']).lower():
                    print("{} contains {}, skipping and marking no interest.".format(job_title, term))
                    parse_dictionary.jobs_dictionary[job]['Interest'] = False
            if bool(parse_dictionary.jobs_dictionary[job]['Interest']):
                wrapper = TextWrapper(width=100)
                job_details = AmazonJobs.JobDetails(job)
                description = job_details.get_job_description()
                description = wrapper.wrap(description)
                if not description:
                    parse_dictionary.jobs_dictionary[job]['Interest'] = False
                    print("Job has closed. Setting to no interest and moving on.")
                else:
                    print("\nJob Title: {}, ID#: {}\n".format(job_title, str(job)))
                    for i in description:
                        print(i)
                    interest = str()
                    while interest != "y" or interest != "n":
                        interest = str(input("\nAre you still interested? (y/n/save)")).lower()
                        if interest == "y":
                            parse_dictionary.jobs_dictionary[job]['Interest'] = True
                            break
                        elif interest == "n":
                            parse_dictionary.jobs_dictionary[job]['Interest'] = False
                            break
                        elif interest == "save":
                            parse_dictionary.write_dictionary(file_name)
                            print("Dictionary saved to {}".format(file_name))
                        else:
                            pass
                job_details.cleanup()
        else:
            print('Not Interested in JobID {}, skipping.'.format(str(job)))
        print("Processed {} jobs.\n".format(str(reviewed)))
    print("Complete, writing out result!")
    parse_dictionary.write_dictionary(file_name)


if __name__ == '__main__':
    main()
