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
    editable_file: str
    required_executables: [str]

    files: [FileFromTemplate]


F = FileFromTemplate


PYTHON_LANGUAGE = Language(
    name="Python",
    file_extension="py",
    repo="codecrafters/redis-starter-py",
    source_file="app/main.py",
    test_file="tests/test_main.py",
    required_executables=["python (3.8)"],
    files=[
        F("README.md", "README.md"),
        F("Makefile", "python/Makefile"),
        F("spawn_redis_server.sh", "python/spawn_redis_server.sh", is_executable=True),
        F("app/main.py", "python/app/main.py"),
        F("tests/test_main.py", "python/tests/test_main.py"),
        F("tests/__init__.py", "python/tests/__init__.py"),
    ],
)

GO_LANGUAGE = Language(
    name="Golang",
    file_extension="go",
    repo="codecrafters/redis-starter-golang",
    source_file="app/server.go",
    test_file="app/server_test.go",
    required_executables=["go"],
    files=[
        F("README.md", "README.md"),
        F("Makefile", "Makefile"),
        F("spawn_redis_server.sh", "go/spawn_redis_server.sh", is_executable=True),
        F("app/server.go", "go/app/server.go"),
    ],
)
