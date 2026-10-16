"""Track configuration in millimeters and degrees; importing performs no I/O."""

from dataclasses import dataclass, fields
from math import isfinite, radians
import os
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class TrackConfig:
    length: float = 54.0
    turn_radius: float = 202.0
    turn_angle: float = 0.0
    rise: float = 0.0
    double_sided: bool = True
    ends: tuple[str, str] = ("female", "male")
    end_flat: float = 24.0

    def __post_init__(self) -> None:
        for name in ("length", "turn_radius", "turn_angle", "rise", "end_flat"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be a number, not {type(value).__name__}")
            if not isfinite(value):
                raise ValueError(f"{name} must be finite")
        if self.length <= 0 or self.turn_radius <= 0:
            raise ValueError("length and turn_radius must be positive")
        if self.end_flat < 0:
            raise ValueError("end_flat must be nonnegative")
        if abs(self.turn_angle) >= 180:
            raise ValueError("turn_angle must be strictly between -180 and 180 degrees")
        if type(self.double_sided) is not bool:
            raise ValueError("double_sided must be a boolean")
        if (not isinstance(self.ends, tuple) or len(self.ends) != 2
                or any(end not in ("female", "male") for end in self.ends)):
            raise ValueError("ends must be a pair of 'female' or 'male', ordered start/end")
        path_length = (self.turn_radius * radians(abs(self.turn_angle))
                       if self.turn_angle else self.length)
        if self.rise and path_length <= 2 * self.end_flat:
            raise ValueError("a graded track needs path length greater than twice end_flat")


def load_config() -> TrackConfig:
    """Load the selected TOML snapshot relative to this module, not the cwd."""
    path = Path(os.environ.get("BRIO_TRACK_CONFIG", "config.toml"))
    if not path.is_absolute():
        path = Path(__file__).resolve().parent / path
    with path.open("rb") as source:
        values = tomllib.load(source)
    unknown = set(values) - {field.name for field in fields(TrackConfig)}
    if unknown:
        raise ValueError(f"Unknown track configuration keys: {', '.join(sorted(unknown))}")
    if "ends" in values:
        if not isinstance(values["ends"], list):
            raise ValueError("ends must be a TOML array of two connector names")
        values["ends"] = tuple(values["ends"])
    return TrackConfig(**values)
