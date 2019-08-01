import AmazonJobs
from textwrap import TextWrapper


def main():
    file_name = "amazon.csv"
    parse_dictionary = AmazonJobs.JobsDictionary()
    print("Attempting to import dictionary from {}".format(file_name))
    parse_dictionary.import_dictionary(file_name)
    reviewed = 0
    for job in parse_dictionary.jobs_dictionary:
        reviewed = reviewed + 1
        if parse_dictionary.jobs_dictionary[job]['Interest']:
            job_details = AmazonJobs.JobDetails(job)
            print("\nJob Title: {}, ID#: {}\n".format(str(parse_dictionary.jobs_dictionary[job]['Title']), str(job)))
            job_details.cleanup()
            wrapper = TextWrapper(width=100)
            description = job_details.get_job_description()
            if description == "":
                interest = "n"
            else:
                description = wrapper.wrap(description)
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
        print("You have reviewed {} jobs.\n".format(str(reviewed)))
    print("Complete, writing out result!")
    parse_dictionary.write_dictionary(file_name)


if __name__ == '__main__':
    main()