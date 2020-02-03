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
    source_file: str
    test_file: str
    required_executables: [str]

    files: [FileFromTemplate]


F = FileFromTemplate


PYTHON_LANGUAGE = Language(
    name="Python",
    file_extension="py",
    repo="codecrafters-io/redis-starter-py",
    source_file="app/main.py",
    test_file="tests/test_main.py",
    required_executables=["python (3.8)"],
    files=[
        F("README.md", "README.md"),
        F("codecrafters.yml", "codecrafters.yml"),
        F("app/main.py", "python/app/main.py"),
        F("Makefile", "python/Makefile"),
        F("Pipfile", "python/Pipfile"),
        F("Pipfile.lock", "python/Pipfile.lock"),
        F("spawn_redis_server.sh", "python/spawn_redis_server.sh", is_executable=True),
        F("tests/test_main.py", "python/tests/test_main.py"),
        F("tests/__init__.py", "python/tests/__init__.py"),
    ],
)

SWIFT_LANGUAGE = Language(
    name="Swift",
    file_extension="swift",
    repo="codecrafters-io/redis-starter-swift",
    source_file="app/main.swift",
    test_file="<not implemented>",
    required_executables=["swift (5.1)"],
    files=[
        F("README.md", "README.md"),
        F("codecrafters.yml", "codecrafters.yml"),
        F("app/main.swift", "swift/app/main.swift"),
        F("Makefile", "swift/Makefile"),
        F("spawn_redis_server.sh", "swift/spawn_redis_server.sh", is_executable=True),
    ],
)

GO_LANGUAGE = Language(
    name="Golang",
    file_extension="go",
    repo="codecrafters-io/redis-starter-golang",
    source_file="app/server.go",
    test_file="app/server_test.go",
    required_executables=["go"],
    files=[
        F("README.md", "README.md"),
        F("codecrafters.yml", "codecrafters.yml"),
        # TODO: Change!
        F("Makefile", "python/Makefile"),
        F("spawn_redis_server.sh", "go/spawn_redis_server.sh", is_executable=True),
        F("app/server.go", "go/app/server.go"),
    ],
)
