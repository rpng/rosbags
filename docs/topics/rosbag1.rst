Rosbag1
=======

The :py:mod:`rosbags.rosbag1` package provides fast read-only access to raw messages stored in the legacy bag format. The rosbag1 support is built for a ROS2 world and some APIs and values perform normalizations to mimic ROS2 behavior and make messages originating from rosbag1 and rosbag2 behave identically. Most notably message types are internally renamed to match their ROS2 counterparts.

Reading rosbag1
---------------
Instances of the :py:class:`Reader <rosbags.rosbag2.Reader>` class are typically used as context managers and provide access to bag metadata and contents after the bag has been opened. The following example shows the typical usage pattern:

.. code-block:: python

   from rosbags.rosbag1 import Reader

   # create reader instance
   with Reader('/home/ros/rosbag_2020_03_24.bag') as reader:
       # topic and msgtype information is available on .topics dictionary
       for topic, info in reader.topics.items():
           print(topic, info)

       # iterate over messages
       for topic, msgtype, rawdata, timestamp in reader.messages():
           if topic == '/imu_raw/Imu':
               print(timestamp)

       # messages() accepts topic filters
       for topic, msgtype, rawdata, timestamp in reader.messages(['/imu_raw/Imu']):
           print(timestamp)
