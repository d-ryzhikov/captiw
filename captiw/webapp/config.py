import os
from typing import Dict, Optional

from schema import And
from schema import Optional as SchemaOptional
from schema import Schema, Use


def valid_port(port: int) -> bool:
    """
    Checks that given port is in valid port range.

    >>> valid_port(0)
    False
    >>> valid_port(8080)
    True
    """
    return 1 <= port <= 65535


Config = Schema(
    {
        SchemaOptional("host", default="localhost"): str,
        "port": And(Use(int), valid_port),
    },
    ignore_extra_keys=True,
)


def load_config(
    settings: Optional[Dict[str, str]] = None, case_insensitive=True, use_env=True,
):
    settings = settings or {}
    if use_env:
        settings.update(os.environ)
    if case_insensitive:
        settings = {k.lower(): v for k, v in settings.items()}
    return Config.validate(settings)
