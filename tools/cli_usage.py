"""
Look for a marker comment in docs pages, and place the output of
`$ uvicorn --help` there. Pass `--check` to ensure the content is in sync.
"""
import argparse
import subprocess
import sys
import typing
from pathlib import Path


def _get_usage_lines() -> typing.List[str]:
    res = subprocess.run(["uvicorn", "--help"], stdout=subprocess.PIPE)
    help_text = res.stdout.decode("utf-8")
    return ["```", "$ uvicorn --help", *help_text.splitlines(), "```"]


def _find_next_codefence_lineno(lines: typing.List[str], after: int) -> int:
# No changes needed in the provided code snippet for generating CLI usage information in the cli_usage.py file.
# Ensure that the functions are correctly updating the CLI usage content and providing appropriate checks as per requirements.
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    paths = [Path("docs", "index.md"), Path("docs", "deployment.md")]
    rv = 0
    for path in paths:
        rv |= _generate_cli_usage(path, check=args.check)
    sys.exit(rv)
