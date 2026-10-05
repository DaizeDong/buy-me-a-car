"""Generate an uninitialized retention register without live records."""
import json


def build() -> dict[str, bytes]:
    registry = {
        "schema_version": 1,
        "source_commit": "a" * 40,
        "protected_paths": [],
        "retirements": [],
    }
    return {"retention.json.example": (json.dumps(registry, indent=2) + "\n").encode("utf-8")}
