"""Example: Message instance conversion."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

import numpy

if TYPE_CHECKING:
    from typing import Any

NATIVE_CLASSES: dict[str, Any] = {}


def to_native(msg: Any) -> Any:  # noqa: ANN401
    """Convert rosbags message to native message.

    Args:
        msg: Rosbags message.

    Returns:
        Native message.

    """
    msgtype: str = msg.__msgtype__
    if msgtype not in NATIVE_CLASSES:
        pkg, name = msgtype.rsplit('/', 1)
        NATIVE_CLASSES[msgtype] = getattr(importlib.import_module(pkg.replace('/', '.')), name)

    fields = {}
    for name, field in msg.__dataclass_fields__.items():
        if 'ClassVar' in field.type:
            continue
        value = getattr(msg, name)
        if '__msg__' in field.type:
            value = to_native(value)
        elif isinstance(value, numpy.ndarray):
            value = value.tolist()
        fields[name] = value

    return NATIVE_CLASSES[msgtype](**fields)


if __name__ == '__main__':
    from rosbags.typesys.types import (
        builtin_interfaces__msg__Time,
        sensor_msgs__msg__Image,
        std_msgs__msg__Header,
    )

    image = sensor_msgs__msg__Image(
        std_msgs__msg__Header(
            builtin_interfaces__msg__Time(42, 666),
            '/frame',
        ),
        4,
        4,
        'rgb8',
        False,
        4 * 3,
        numpy.zeros(4 * 4 * 3, dtype=numpy.uint8),
    )

    native_image = to_native(image)
    # native_image can now be passed to the ROS stack
