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
       # topic and msgtype information is available on .connections dictionary
       for connection in reader.connections.values():
           print(connection.topic, connection.msgtype)

       # iterate over messages
       for connection, timestamp, rawdata in reader.messages():
           if connection.topic == '/imu_raw/Imu':
               print(timestamp)

       # messages() accepts connection filters
       connections = [x for x in reader.connections.values() if x.topic == '/imu_raw/Imu']
       for connection, timestamp, rawdata in reader.messages(connections=connections):
           print(timestamp)
