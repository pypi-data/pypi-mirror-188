from argparse import ArgumentParser, _SubParsersAction

from dev.constants import ReturnCode
from dev.files import filter_not_unit_test_files, filter_python_files, get_repo_files
from dev.output import output
from dev.tasks.task import Task


class CountTask(Task):
    def _perform(self, exclude_tests: bool = False) -> int:
        filters = [filter_python_files]
        lines = 0

        if exclude_tests:
            filters.append(filter_not_unit_test_files)

        for file in get_repo_files(filters):
            with open(file, encoding="utf8") as reader:
                lines += sum(1 for _ in reader)

        output(lines)

        return ReturnCode.OK

    @classmethod
    def _add_task_parser(cls, subparsers: _SubParsersAction) -> ArgumentParser:
        parser = super()._add_task_parser(subparsers)
        parser.add_argument(
            "-e", "--exclude-tests", action="store_true", dest="exclude_tests"
        )

        return parser
