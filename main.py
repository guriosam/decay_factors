from metrics.experience import ExperienceMetrics
from utils.json_handler import JSONHandler


class Main:

    def __init__(self):
        self.config = JSONHandler('').open_json('config.json')
        self.projects = self.config['projects']

    def run(self):
        for project in self.projects:
            self.project_name = project['repo']

            if 'dubbo' not in self.project_name:
                print(self.project_name)
                continue

            print(self.project_name)

            # experience = ExperienceMetrics(project)
            # experience.number_of_pull_requests()
            # experience.number_associated_issues()
            words = WordsInDiscussion(project)



main = Main()
main.run()
