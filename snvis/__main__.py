import sys

from snvis import driver
from snvis import cli


def main():
    args = cli.parse_args()
    return driver.main(args)


if __name__ == "__main__":
    sys.exit(main())
