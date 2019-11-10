from dataclasses import dataclass

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
    repo: str
    files: [FileFromTemplate]


PYTHON_LANGUAGE = Language(
    name="Python",
    file_extension="py",
    repo="rohitpaulk/redis-solution-starter-py",
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
