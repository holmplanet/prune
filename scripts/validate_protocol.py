#!/usr/bin/env python3
"""Validate a protocol document against a JSON Schema contract."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, SchemaError, ValidationError
from yaml import YAMLError


def load_document(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_document(document_path: Path, schema_path: Path) -> None:
    schema = load_document(schema_path)
    document = load_document(document_path)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(document)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path)
    parser.add_argument("--schema", required=True, type=Path)
    args = parser.parse_args()

    try:
        validate_document(args.document, args.schema)
    except (OSError, UnicodeError, SchemaError, YAMLError):
        print("protocol validation failed: unreadable or invalid schema/document", file=sys.stderr)
        return 1
    except ValidationError as error:
        print(
            f"protocol validation failed at {error.json_path}: {error.validator}",
            file=sys.stderr,
        )
        return 1

    print(f"valid: {args.document}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
