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


def _get_class_ids(commits_classes):
    print("Get Class IDs")
    ids = {}
    for commit_class in commits_classes:
        if commit_class[3] not in ids.keys():
            ids[commit_class[3]] = commit_class[0].split('_')[0]
        if commit_class[2] == 'None':
            continue
        if commit_class[2] not in ids.keys():
            ids[commit_class[2]] = commit_class[0].split('_')[0]

    return ids


class ExperienceMetrics:

    def __init__(self, project):
        config = JSONHandler('').open_json('config.json')
        self.project = project['repo']
        self.path = config['output_path']

    def number_of_pull_requests(self):
        # Number of pull requests that contained changes to a class.
        mypath = self.path + self.project + '/'

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

        class_ids = _get_class_ids(commits_classes)

        pulls_by_class = {}
        for commit_class_key in commits_by_class.keys():
            commit_list = commits_by_class[commit_class_key]
            for commit in commit_list:
                if commit in commits_in_pulls.keys():
                    if commit_class_key not in pulls_by_class.keys():
                        pulls_by_class[commit_class_key] = []

                    pulls_by_class[commit_class_key].extend(commits_in_pulls[commit])

        num_pulls = [['class_id', 'num_pulls']]
        for key in pulls_by_class.keys():
            pulls = pulls_by_class[key]
            num_pulls.append([class_ids[key], len(set(pulls))])

        # TODO Save in CSV

        return commits_in_pulls, renames, commits_by_class, pulls_by_class, class_ids, num_pulls

    def number_associated_issues(self):
        # Number of issues associated to pull requests that contained changes to a class.

        mypath = self.path + self.project + '/'
        _, _, _, pulls_by_class, class_ids, _ = self.number_of_pull_requests()

        csv = CSVHandler()
        pulls_of_issues = csv.open_csv(mypath + self.project + '_pulls_of_issues.csv')

        associated_issues = {}

        for row in pulls_of_issues:
            if row[1] not in associated_issues.keys():
                associated_issues[row[1]] = set()

            associated_issues[row[1]].add(row[0])


        issues_by_class = {}
        for pull_class in pulls_by_class:
            pulls = pulls_by_class[pull_class]
            for pull in pulls:
                if pull_class not in issues_by_class.keys():
                    issues_by_class[pull_class] = 0

                if pull in associated_issues.keys():
                    issues_by_class[pull_class] += len(associated_issues[pull])
                else:
                    issues_by_class[pull_class] += 1

        issues_num = [['class_id', 'issue_num']]
        for key in issues_by_class.keys():
            issues = issues_by_class[key]
            issues_num.append([class_ids[key], issues])

        # TODO Save in CSV

        return issues_num

    def percentage_of_related_comments(self):
        # Percentage of messages related to a file on pull requests that contain modifications to that same file.
        pass

    def percentage_of_related_words(self):
        # Percentage of words of messages related to a file on pull requests that contain modifications to that same
        # file.
        pass
