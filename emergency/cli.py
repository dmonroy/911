import argparse

from emergency import db
from emergency.web import run_web


def main():  # pragma: no cover
    parser = argparse.ArgumentParser()

    commands = dict(
        create_database=db.create_database,
        drop_database=db.drop_database,
        migrate=db.run_migrations,
        web=run_web
    )

    cmd_help = "one of: %s" % ', '.join(sorted(commands.keys()))

    parser.add_argument(
        'command',
        help=cmd_help,
        type=lambda x: commands.get(x)
    )

    args = parser.parse_args()

    if args.command is None:
        raise SystemExit('Command must be ' + cmd_help)

    args.command()


if __name__ == '__main__':  # pragma: no cover
    main()
