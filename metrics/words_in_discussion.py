from os import listdir
from os.path import isfile, join

from utils.csv_handler import CSVHandler
from utils.json_handler import JSONHandler
from utils.text_processing import TextProcessing


class WordsInDiscussion:

    def __init__(self, project):
        config = JSONHandler('').open_json('config.json')
        self.project = project['repo']
        self.path = config['output_path']

    def get_words_in_discussion(self):

        _, words_in_discussion = self.get_comments_in_discussion()

        words_per_discussion = [['issue', 'number_words']]

        for key in words_in_discussion.keys():
            words_per_discussion.append([key, words_in_discussion[key]])

        csv = CSVHandler()
        csv.write_csv(self.path + '/' + self.project + '/metrics/',
                      self.project + '_words_in_discussion.csv',
                      words_per_discussion)

    def get_words_per_comment_in_discussion(self):
        comments_in_discussion, words_in_discussion = self.get_comments_in_discussion()

        words_per_comments_in_discussion = [['issue', 'number_words_per_comment']]

        for key in comments_in_discussion.keys():
            # print(str(key) + ': ' + str(comments_per_issue[key]))
            words_per_comments_in_discussion.append([key, str(words_in_discussion[key] / comments_in_discussion[key])])
        csv = CSVHandler()
        csv.write_csv(self.path + '/' + self.project + '/metrics/',
                      self.project + '_words_per_comments_in_discussion.csv',
                      words_per_comments_in_discussion)

    def get_comments_in_discussion(self):
        mypath = self.path + self.project + '/comments/individual/'
        json = JSONHandler(mypath)
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        words_in_discussion = {}
        comments_in_discussion = {}

        for file in onlyfiles:
            comments = json.open_json(file)
            for comment in comments:
                if 'issue_url' in comment.keys():
                    issue = comment['issue_url'].split('/')
                    issue = issue[len(issue) - 1]

                    if issue not in words_in_discussion.keys():
                        words_in_discussion[issue] = 0
                    if issue not in comments_in_discussion.keys():
                        comments_in_discussion[issue] = 0

                    tp = TextProcessing()
                    processed = tp.pre_process_text(comment['body'])
                    comment_text = ''
                    for token in processed:
                        comment_text += token + ' '
                    words_in_discussion[issue] += len(comment_text.split(' '))
                    comments_in_discussion[issue] += 1

        return comments_in_discussion, words_in_discussion
