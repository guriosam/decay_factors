from os import listdir
from os.path import isfile, join

from utils.csv_handler import CSVHandler
from utils.json_handler import JSONHandler


def _get_original_name(renames, class_name):
    while True:
        if class_name in renames.keys():
            class_name = renames[class_name]
        else:
            return class_name


def _get_renames(commits_classes):
    print("Get Renames")
    renames = {}
    for commit_class in commits_classes:

        if commit_class[2] == commit_class[3]:
            continue

        if commit_class[3] not in renames.keys() and commit_class[2] not in renames.keys():
            if commit_class[2] is not None:
                if 'None' not in commit_class[2]:
                    renames[commit_class[3]] = commit_class[2]
    return renames


def _get_commits_by_class(renames, commits_classes):
    print("Get Commits By Class")
    commits_by_class = {}
    for commit_class in commits_classes:
        class_name = _get_original_name(renames, commit_class[3])

        if class_name not in commits_by_class.keys():
            commits_by_class[class_name] = set()

        commits_by_class[class_name].add(commit_class[1])

    return commits_by_class


class ExperienceMetrics:

    def __init__(self, project):
        config = JSONHandler('').open_json('config.json')
        self.project = project['repo']
        self.path = config['output_path']

    def number_of_pull_requests(self):
        # Number of pull requests that contained changes to a class.
        mypath = self.path + self.project + '/'
        json = JSONHandler(mypath)

        csv = CSVHandler()
        pulls_commits = csv.open_csv(mypath + 'pulls_commits/' + self.project + '_commits_by_pull_request.csv')
        commits_classes = csv.open_csv(mypath + self.project + '.csv')

        commits_in_pulls = {}
        for pull_commit in pulls_commits:
            if pull_commit[1] not in commits_in_pulls.keys():
                commits_in_pulls[pull_commit[1]] = []

            commits_in_pulls[pull_commit[1]].append(pull_commit[0])

        renames = _get_renames(commits_classes)

        commits_by_class = _get_commits_by_class(renames, commits_classes)

        pulls_by_class = {}
        for commit_class_key in commits_by_class.keys():
            commit_list = commits_by_class[commit_class_key]
            for commit in commit_list:
                if commit in commits_in_pulls.keys():
                    if commit_class_key not in pulls_by_class.keys():
                        pulls_by_class[commit_class_key] = []

                    pulls_by_class[commit_class_key].extend(commits_in_pulls[commit])

        num_pulls = []
        for key in pulls_by_class.keys():
            pulls = pulls_by_class[key]
            num_pulls.append([key, len(set(pulls))])

        # Save in CSV
        print(num_pulls)

    def number_associated_issues(self):
        # Number of issues associated to pull requests that contained changes to a class.
        pass

    def percentage_of_related_comments(self):
        # Percentage of messages related to a file on pull requests that contain modifications to that same file.
        pass

    def percentage_of_related_words(self):
        # Percentage of words of messages related to a file on pull requests that contain modifications to that same
        # file.
        pass
