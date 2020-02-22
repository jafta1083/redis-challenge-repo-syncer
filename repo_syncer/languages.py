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
    required_executables: [str]

    files: [FileFromTemplate]


F = FileFromTemplate


PYTHON_LANGUAGE = Language(
    name="Python",
    file_extension="py",
    repo="codecrafters-io/redis-starter-py",
    source_file="app/main.py",
    required_executables=["python (3.8)"],
    files=[
        F("README.md", "README.md"),
        F("codecrafters.yml", "codecrafters.yml"),
        F("app/main.py", "python/app/main.py"),
        F("spawn_redis_server.sh", "python/spawn_redis_server.sh", is_executable=True),
    ],
)

# SWIFT_LANGUAGE = Language(
#     name="Swift",
#     file_extension="swift",
#     repo="codecrafters-io/redis-starter-swift",
#     source_file="app/main.swift",
#     required_executables=["swift (5.1)"],
#     files=[
#         F("README.md", "README.md"),
#         F("codecrafters.yml", "codecrafters.yml"),
#         F("app/main.swift", "swift/app/main.swift"),
#         F("Makefile", "swift/Makefile"),
#         F("spawn_redis_server.sh", "swift/spawn_redis_server.sh", is_executable=True),
#     ],
# )

GO_LANGUAGE = Language(
    name="Go",
    file_extension="go",
    repo="codecrafters-io/redis-starter-golang",
    source_file="app/server.go",
    required_executables=["go"],
    files=[
        F("README.md", "README.md"),
        F("codecrafters.yml", "codecrafters.yml"),
        F("spawn_redis_server.sh", "go/spawn_redis_server.sh", is_executable=True),
        F("app/server.go", "go/app/server.go"),
    ],
)

PHP_LANGUAGE = Language(
    name="PHP",
    file_extension="php",
    repo="codecrafters-io/redis-starter-php",
    source_file="app/main.php",
    required_executables=["php (7.4)"],
    files=[
        F("README.md", "README.md"),
        F("codecrafters.yml", "codecrafters.yml"),
        F("app/main.py", "php/app/main.py"),
        F("spawn_redis_server.sh", "php/spawn_redis_server.sh", is_executable=True),
    ],
)
