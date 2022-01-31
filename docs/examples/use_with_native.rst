Use with native stack
=====================

Messages read with rosbags are simple dataclasses that mimic the native ROS2 interface. If you want to pass those messages to the native ROS2 stack, you need to convert them into native objects first.


Message instance conversion
---------------------------

.. literalinclude:: ./use_with_native.py
