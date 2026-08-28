"""The command line for everything that is not the server.

    uv run inferapi data-convert
    uv run inferapi train --max-depth 12 --output out/models/deep.joblib

A CLI instead of an `if __name__ == "__main__"` block at the bottom of train.py:
the entrypoint is then something you can name, document, `--help`, and call from a
bash script without knowing which module happens to hold the code today.

Flags beat every configuration source, including the environment, because whoever
typed the flag is standing right there.
"""

import argparse
import logging
from pathlib import Path
from typing import Any

from inferapi.config import TrainingSettings
from inferapi.data import csv_to_parquet, load_raw
from inferapi.logging_setup import setup_logging
from inferapi.train import training_procedure

logger = logging.getLogger(__name__)

# Flags accepted before the subcommand, and the settings field each one overrides.
# Subcommands declare their own map in set_defaults(config_flags=...) below.
GLOBAL_FLAGS = {"log_level": "logging.level"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="inferapi", description=__doc__.splitlines()[0])
    parser.add_argument("--log-level", help="override logging.level for this run")
    commands = parser.add_subparsers(dest="command", required=True)

    convert = commands.add_parser("data-convert", help="convert the downloaded CSV into parquet")
    convert.add_argument("--csv", type=Path, help="override data.csv_path")
    convert.add_argument("--parquet", type=Path, help="override data.parquet_path")
    convert.set_defaults(
        run=run_data_convert,
        config_flags={"csv": "data.csv_path", "parquet": "data.parquet_path"},
    )

    train = commands.add_parser("train", help="train the model and write the artifact")

    train.add_argument("--output", type=Path, required=True, help="where to write the artifact")
    # TODO(LAB): Implement the rest of the train parser with the following arguments:
    # --data
    train.add_argument("--data",type=Path)
    # --n-estimators
    train.add_argument("--n-estimators",type=int)
    # --max-depth
    train.add_argument("--max-depth", type=int)
    # --seed
    train.add_argument("--seed",type=int)
    # --decision-threshold
    train.add_argument("--decision-threshold", type=float)
    # --overwrite
    train.add_argument("--overwrite", action="store_true" )
    ...

    train.set_defaults(
        run=run_train,
        # --output and --overwrite are absent on purpose: they say what this run does
        # with its result, not what the project is configured to be.
        config_flags={
            "data": "data.parquet_path",
            "n_estimators": "training.n_estimators",
            "max_depth": "training.max_depth",
            "seed": "training.seed",
            "decision_threshold": "training.decision_threshold",
        },
    )

    return parser


def settings_from_args(args: argparse.Namespace) -> TrainingSettings:
    """Builds a TrainingSettings object based on overrides provided on CLI

    This function is here so that args provided on the command line are
    taken into account when instantiating a Training settings.
    """
    overrides: dict[str, dict[str, Any]] = {}
    for flag, path in (GLOBAL_FLAGS | args.config_flags).items():
        value = getattr(args, flag)
        if value is None:
            continue
        section, field = path.split(".")
        overrides.setdefault(section, {})[field] = value

    return TrainingSettings(**overrides)


def run_data_convert(args: argparse.Namespace, settings: TrainingSettings) -> int:
    csv_to_parquet(settings.data.csv_path, settings.data.parquet_path)
    return 0


# TODO(LAB): load the frame and hand it to training_procedure, with the output path
#            and the overwrite decision this invocation asked for.
def run_train(args: argparse.Namespace, settings: TrainingSettings) -> int: 
    training_procedure(train_config=settings, dataframe:Data, output_model_path="./data", overwrite_model=True)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    settings = settings_from_args(args)
    # Once, here, at the entrypoint: no imported module ever configures logging.
    setup_logging(settings.logging)

    logger.debug("cli_invoked command=%s settings=%s", args.command, settings.model_dump(mode="json"))
    return args.run(args, settings)


if __name__ == "__main__":
    raise SystemExit(main())
