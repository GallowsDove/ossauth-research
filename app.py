import json

import github
import os
from flask import Flask
from flask_cors import CORS
from github import Github

app = Flask(__name__)
CORS(app)
gh = Github(os.environ['GITHUB_TOKEN'])

@app.route('/<owner>/<project>')
def get_project(owner, project):
    try:
        project = f"{owner}/{project}"
        try:
            repo = gh.get_repo(project)
        except github.UnknownObjectException as e:
            print(gh.rate_limiting)
            if e.status == 404:
                return "Repository not found. Please check repository name, including upper/lowercase letters.", 404
            else:
                return e, 500
        data = dict()
        data['stargazers_count'] = repo.stargazers_count
        data['forks_count'] = repo.forks_count
        data['subscribers_count'] = repo.subscribers_count
        try:
            data['contributors_anon_count'] = repo.get_contributors(anon='true').totalCount
            data['contributors_count'] = repo.get_contributors(anon='false').totalCount
        except github.GithubException as e:
            if e.status == 403:
                data['contributors_anon_count'] = 0
                data['contributors_count'] = 0
            else:
                return e, 500
        data['commits_count'] = repo.get_commits().totalCount
        data['pull_requests_count'] = repo.get_pulls(state='all').totalCount
        data['pull_requests_open_count'] = repo.get_pulls(state='open').totalCount
        data['languages'] = repo.get_languages()
        data['first_commit'] = repo.get_commits().reversed[0].commit.committer.date.isoformat()
        print(gh.rate_limiting)
        return json.dumps(data)
    except github.RateLimitExceededException:
        return "Rate limit exceeded. Please try again later.", 429


if __name__ == '__main__':
    app.run()
