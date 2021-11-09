Type system
===========

Rosbags ships its own pure python typesystem :py:mod:`rosbags.typesys`. It uses parse trees to represent message definitions internally. It ships its own ``.idl`` and ``.msg`` definition parser to convert message definition files into the internal format.

Out of the box it supports the message types defined by the standard ROS2 distribution. Message types can be parsed and added on the fly during runtime without an additional build step.

Message instances
-----------------
The type system generates a dataclass for each message type. These dataclasses give direct read write access to all mutable fields of a message. Fields should be mutated with care as no type checking is applied during runtime.

.. note::

   Limitation: While the type system parses message definitions with array bounds and/or default values, neither bounds nor default values are enforced or assigned to message instances.

Extending the type system
-------------------------
Adding custom message types consists of two steps. First, message definitions are converted into parse trees using :py:func:`get_types_from_idl() <rosbags.typesys.get_types_from_idl>` or :py:func:`get_types_from_msg() <rosbags.typesys.get_types_from_msg>`, and second the types are registered in the type system via :py:func:`register_types() <rosbags.typesys.register_types>`. The following example shows how to add messages type definitions from ``.msg`` and ``.idl`` files:

.. code-block:: python

   from pathlib import Path

   from rosbags.typesys import get_types_from_idl, get_types_from_msg, register_types

   idl_text = Path('foo_msgs/msg/Foo.idl').read_text()
   msg_text = Path('bar_msgs/msg/Bar.msg').read_text()

   # plain dictionary to hold message definitions
   add_types = {}

   # add all definitions from one idl file
   add_types.update(get_types_from_idl(idl_text))

   # add definition from one msg file
   add_types.update(get_types_from_msg(msg_text, 'bar_msgs/msg/Bar'))

   # make types available to rosbags serializers/deserializers
   register_types(add_types)
