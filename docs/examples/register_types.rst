Register custom message types
=============================

Out of the box rosbags only supports the message types that ship with a default ROS2 distribution. If you want to (de)serialize custom messages you need to add them to the type system manually.


From rosbag1
------------

.. literalinclude:: ./register_types_rosbag1.py


From definition string
----------------------

.. literalinclude:: ./register_types_string.py


From multiple files
-------------------

.. literalinclude:: ./register_types_files.py
