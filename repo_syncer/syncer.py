from typing import Optional
import os

import github
from github import Github
from github import InputGitTreeElement

from .languages import PYTHON_LANGUAGE, GO_LANGUAGE, PHP_LANGUAGE, Language


class Syncer:
    def __init__(self, github_client: Github):
        self.github_client = github_client
        self.languages = [PYTHON_LANGUAGE, GO_LANGUAGE, PHP_LANGUAGE]

    def sync(self):
        for language in self.languages:
            print(f"Syncing {language.name} ({language.repo})")
            pr_url = self.sync_language(language)
            if pr_url:
                print(f" - {pr_url}")
            else:
                print(" - No changes")

    def sync_locally(self):
        for language in self.languages:
            print(f"Syncing {language.name} ({language.repo})")
            dir = self.sync_language_locally(language)
            print(f" - {dir}")

    def sync_language_locally(self, language: Language) -> str:
        """
        Returns the directory
        """
        dir = f"samples/{language.name}"
        for file_from_template in language.files:
            path = os.path.join(dir, file_from_template.path)
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))

            with open(path, "w") as f:
                f.write(self._file_content(file_from_template, language))

            if file_from_template.is_executable:
                os.chmod(path, 0o755)

        return dir

    def sync_language(self, language: Language) -> Optional[str]:
        """ Returns the pull request URL if a pull request was created.
        """
        gh_repo = self.github_client.get_repo(language.repo)

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
                    content=self._file_content(file_from_template, language),
                )
                for file_from_template in language.files
            ]
        )
        if tree == master.tree:
            # No changes
            return None

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

    def _file_content(self, file_from_template, language) -> str:
        return file_from_template.render(
            {
                "language": language.name,
                "required_executable": language.required_executables[0],
                "source_file": language.source_file,
            }
        )

    def _delete_ref_if_exists(self, gh_repo: github.Repository, ref: str):
        try:
            gh_repo.get_git_ref("heads/sync-with-syncer").delete()
        except github.GithubException as e:
            if e.data["message"] != "Not Found":
                raise
