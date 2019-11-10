from typing import Dict, Optional
from dataclasses import dataclass

import github
from github import Github
from github import InputGitTreeElement
from jinja2 import Template, StrictUndefined


@dataclass
class FileFromTemplate:
    path: str
    template_path: str
    is_executable: bool = False

    def render(self, context: dict = None):
        if context is None:
            context = {}

        with open(f"repo_syncer/templates/{self.template_path}") as f:
            raw_contents = f.read()

        template = Template(raw_contents, undefined=StrictUndefined)
        return template.render(**context)


@dataclass
class Language:
    name: str
    file_extension: str
    files: [FileFromTemplate]


PYTHON_LANGUAGE = Language(
    name="Python",
    file_extension="py",
    files=[
        FileFromTemplate("README.md", "README.md"),
        FileFromTemplate("Makefile", "Makefile"),
        FileFromTemplate(".gitignore", "python/.gitignore"),
        FileFromTemplate(
            "spawn_redis_server.sh", "python/spawn_redis_server.sh", is_executable=True,
        ),
        FileFromTemplate("app/main.py", "python/app/main.py"),
    ],
)


class Syncer:
    def __init__(self, github_client: Github):
        self.github_client = github_client
        self.languages_and_repos = [
            (PYTHON_LANGUAGE, "rohitpaulk/redis-solution-starter-py")
        ]

    def sync(self):
        for language, repository in self.languages_and_repos:
            print(f"Syncing {language.name} ({repository})")
            pr_url = self.sync_language(language, repository)
            if pr_url:
                print(f" - {pr_url}")
            else:
                print(" - No changes")

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
                    path=file_from_template.path,
                    mode="100755" if file_from_template.is_executable else "100644",
                    type="blob",
                    content=file_from_template.render({"language_name": language.name}),
                )
                for file_from_template in language.files
            ]
        )
        commit = gh_repo.create_git_commit(commit_message, tree, [master])

        self._delete_ref_if_exists(gh_repo, "refs/heads/sync-with-syncer")
        gh_repo.create_git_ref("refs/heads/sync-with-syncer", commit.sha)
        pull = gh_repo.create_pull(
            f"Syncing {language.name} repository with redis-challenge-repo-syncer",
            "This repository is maintained via "
            + f"https://github.com/rohitpaulk/redis-challenge-repo-syncer.",
            "master",
            "sync-with-syncer",
        )
        return pull.html_url

    def _delete_ref_if_exists(self, gh_repo: github.Repository, ref: str):
        try:
            gh_repo.get_git_ref("heads/sync-with-syncer").delete()
        except github.GithubException as e:
            if e.data["message"] != "Not Found":
                raise
