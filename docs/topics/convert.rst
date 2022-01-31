Convert rosbag versions
=======================

The :py:mod:`rosbags.convert` package includes a CLI tool to convert legacy rosbag1 files to rosbag2 and vice versa.

Features
--------

- Reasonably fast, as it converts raw ROS1 messages to raw CDR messages without going though deserialization and serialization
- Tries to match ROS1 message type names to registered ROS2 types
- Automatically registers unknown message types present in the legacy rosbag file for the conversion
- Handles differences of ``std_msgs/msg/Header`` between both ROS versions

Limitations
-----------

- Refuses to convert unindexed rosbag1 files, please reindex files before conversion
- Currently does not handle split bags
- Only ROS2 default message types are supported when converting rosbag2 to rosbag1

Usage
-----

.. code-block:: console

   # Convert "foo.bag", result will be "foo/"
   $ rosbags-convert foo.bag

   # Convert "bar", result will be "bar.bag"
   $ rosbags-convert bar

   # Convert "foo.bag", save the result as "bar"
   $ rosbags-convert foo.bag --dst /path/to/bar

   # Convert "bar", save the result as "foo.bag"
   $ rosbags-convert bar --dst /path/to/foo.bag
