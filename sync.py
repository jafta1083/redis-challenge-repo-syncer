import os

from github import Github

from repo_syncer import Syncer

gh_client = Github(os.environ["GITHUB_TOKEN"])
Syncer(gh_client).sync()
