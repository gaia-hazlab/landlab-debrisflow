from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Config must be a YAML mapping: {path}")
    return data


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def resolve_config(base_path: str | Path, override_paths: list[str | Path] | None = None) -> dict[str, Any]:
    cfg = load_yaml(base_path)
    for path in override_paths or []:
        cfg = deep_merge(cfg, load_yaml(path))
    validate_config(cfg)
    return cfg


def validate_config(cfg: dict[str, Any]) -> None:
    required_top_level = ["project", "inputs", "grid", "outputs", "workflows"]
    missing = [key for key in required_top_level if key not in cfg]
    if missing:
        raise ValueError(f"Missing required config sections: {', '.join(missing)}")

    inputs = cfg["inputs"]
    if "asc_dir" not in inputs:
        raise ValueError("Config missing inputs.asc_dir")
    if "layers" not in inputs or not isinstance(inputs["layers"], dict):
        raise ValueError("Config missing inputs.layers mapping")

    outputs = cfg["outputs"]
    if "root_dir" not in outputs:
        raise ValueError("Config missing outputs.root_dir")

    workflows = cfg["workflows"]
    if not isinstance(workflows, dict) or not workflows:
        raise ValueError("Config must contain at least one workflow block")

    for workflow_name, workflow_cfg in workflows.items():
        if not isinstance(workflow_cfg, dict):
            raise ValueError(f"Workflow config must be a mapping: {workflow_name}")
        if "enabled" not in workflow_cfg:
            raise ValueError(f"Workflow missing enabled flag: {workflow_name}")


def dump_config(cfg: dict[str, Any], fmt: str) -> str:
    if fmt == "json":
        return json.dumps(cfg, indent=2)
    if fmt == "yaml":
        return yaml.safe_dump(cfg, sort_keys=False)
    raise ValueError(f"Unsupported format: {fmt}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resolve a base workflow config with optional YAML overrides."
    )
    parser.add_argument("--base", required=True, help="Base YAML config.")
    parser.add_argument(
        "--override",
        action="append",
        default=[],
        help="Override YAML config. Pass multiple times to layer scenarios.",
    )
    parser.add_argument(
        "--format",
        default="yaml",
        choices=["yaml", "json"],
        help="Output format for the resolved config.",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Optional output file. Prints to stdout if omitted.",
    )
    args = parser.parse_args()

    cfg = resolve_config(args.base, args.override)
    rendered = dump_config(cfg, args.format)

    if args.out:
        Path(args.out).write_text(rendered)
        print(f"Saved: {args.out}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
