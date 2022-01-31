"""Example: Register type from definition string."""

from rosbags.serde import serialize_cdr
from rosbags.typesys import get_types_from_msg, register_types

# Your custom message definition
STRIDX_MSG = """
string string
uint32 index
"""

register_types(get_types_from_msg(STRIDX_MSG, 'custom_msgs/msg/StrIdx'))

# Type import works only after the register_types call,
# the classname is derived from the msgtype name above

# pylint: disable=no-name-in-module,wrong-import-position
from rosbags.typesys.types import custom_msgs__msg__StrIdx as StrIdx  # type: ignore  # noqa

# pylint: enable=no-name-in-module,wrong-import-position

message = StrIdx(string='foo', index=42)

# Rawdata that can be passed to rosbag2.Writer.write
rawdata = serialize_cdr(message, message.__msgtype__)
