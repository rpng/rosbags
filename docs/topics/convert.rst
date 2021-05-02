Convert Rosbag1 to Rosbag2
==========================

The :py:mod:`rosbags.convert` package includes a CLI tool to convert legacy rosbag1 files to rosbag2.

Features
--------

- Reasonably fast, as it converts raw ROS1 messages to raw CDR messages without going though deserialization and serialization
- Tries to match ROS1 message type names to registered ROS2 types
- Automatically registers unknown message types present in the legacy rosbag file for the conversion
- Handles differences of ``std_msgs/msg/Header`` between both ROS versions

Limitations
-----------

- Refuses to convert unindexed rosbag files, please reindex files before conversion
- Currently does not handle split bags

Usage
-----

.. code-block:: console

   # Convert "foo.bag", result will be "foo/"
   $ rosbags-convert foo.bag

   # Convert "foo.bag", save the result as "bar"
   $ rosbags-convert foo.bag --dst /path/to/bar
