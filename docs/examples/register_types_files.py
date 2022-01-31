"""Example: Register types from msg files."""

from pathlib import Path

from rosbags.typesys import get_types_from_msg, register_types

add_types = {}

msgdef = Path('/path/to/custom_msgs/msg/Speed.msg').read_text(encoding='utf-8')
add_types.update(get_types_from_msg(msgdef, 'custom_msgs/msg/Speed.msg'))

msgdef = Path('/path/to/custom_msgs/msg/Accel.msg').read_text(encoding='utf-8')
add_types.update(get_types_from_msg(msgdef, 'custom_msgs/msg/Accel.msg'))

register_types(add_types)

# Type import works only after the register_types call,
# the classname is derived from the msgtype names above

# pylint: disable=no-name-in-module,wrong-import-position
from rosbags.typesys.types import custom_msgs__msg__Speed as Speed  # type: ignore  # noqa
from rosbags.typesys.types import custom_msgs__msg__Accel as Accel  # type: ignore  # noqa

# pylint: enable=no-name-in-module,wrong-import-position
