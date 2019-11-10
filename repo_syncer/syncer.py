from typing import Dict, Optional

from github import Github
from github import InputGitTreeElement
from jinja2 import Template


class Language:
    def __init__(self, name: str, file_extension: str):
        self.name = name
        self.file_extension = file_extension

    def files(self) -> Dict[str, str]:
        """
        Returns a mapping from filename -> contents
        """
        return {"README.md": "# testing"}


class Syncer:
    def __init__(self, github_client: Github):
        self.github_client = github_client
        self.languages_and_repos = [
            (
                Language(name="Python", file_extension="py"),
                "rohitpaulk/redis-solution-starter-py",
            )
        ]

    def sync(self):
        for language, repository in self.languages_and_repos:
            self.sync_language(language, repository)

    def sync_language(self, language: Language, repository: str) -> Optional[str]:
        """
        Returns the pull request URL if a pull request was created.
        """
        gh_repo = self.github_client.get_repo(repository)

        master = gh_repo.get_commit("master")
        master = gh_repo.get_git_commit(master.sha)
        commit_message = "\n".join(
            [
                f"Syncing {language.name} repository with redis-challenge-repo-syncer",
                "\n",
                "Created by https://github.com/rohitpaulk/redis-challenge-repo-syncer.",
            ]
        )

        tree = gh_repo.create_git_tree(
            [
                InputGitTreeElement(
                    path="README.md",
                    mode="100644",
                    type="blob",
                    content=self.read_template(language, "README.md"),
                )
            ]
        )
        commit = gh_repo.create_git_commit(commit_message, tree, [master])
        gh_repo.create_git_ref("refs/heads/sync-with-syncer", commit.sha)
        pull = gh_repo.create_pull(
            "Sample title", "Sample body", "master", "sync-with-syncer"
        )
        return pull.html_url

    def read_template(self, language: Language, template_name: str):
        with open("repo_syncer/templates/{template_name}") as f:
            raw_contents = f.read()

        template = Template(raw_contents)
        return template.render(language_name=language.name)
