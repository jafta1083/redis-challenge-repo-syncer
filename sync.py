import os

from github import Github

from repo_syncer import Syncer

if os.environ.get("LOCAL"):
    Syncer(None).sync_locally()
else:
    gh_client = Github(os.environ["GITHUB_TOKEN"])
    Syncer(gh_client).sync()
