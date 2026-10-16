"""Parameterized BRIO-style track; configuration is read only on invocation."""

from build123d import Compound

from models.brio_duplo.track.config import load_config
from models.brio_duplo.track.geometry import build_track, check_track


def build() -> Compound:
    return build_track(load_config())


def check(shape: Compound) -> None:
    check_track(shape, load_config())
