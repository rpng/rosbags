Rosbag1
=======

The :py:mod:`rosbags.rosbag1` package provides fast read-only access to raw messages stored in the legacy bag format. The rosbag1 support is built for a ROS2 world and some APIs and values perform normalizations to mimic ROS2 behavior and make messages originating from rosbag1 and rosbag2 behave identically. Most notably message types are internally renamed to match their ROS2 counterparts.

Writing rosbag1
---------------
Instances of the :py:class:`Writer <rosbags.rosbag1.Writer>` class can create and write to new rosbag1 files. It is usually used as a context manager. Before the first message of a topic can be written, its topic must first be added to the bag. The following example shows the typical usage pattern:

.. code-block:: python

   from rosbags.rosbag1 import Writer
   from rosbags.serde import cdr_to_ros1, serialize_cdr
   from rosbags.typesys.types import std_msgs__msg__String as String

   # create writer instance and open for writing
   with Writer('/home/ros/rosbag_2020_03_24.bag') as writer:
       # add new connection
       topic = '/chatter'
       msgtype = String.__msgtype__
       connection = writer.add_connection(topic, msgtype, latching=True)

       # serialize and write message
       message = String('hello world')
       timestamp = 42
       writer.write(connection, timestamp, cdr_to_ros1(serialize_cdr(message, msgtype), msgtype))

Reading rosbag1
---------------
Instances of the :py:class:`Reader <rosbags.rosbag2.Reader>` class are typically used as context managers and provide access to bag metadata and contents after the bag has been opened. The following example shows the typical usage pattern:

.. code-block:: python

   from rosbags.rosbag1 import Reader
   from rosbags.serde import deserialize_cdr, ros1_to_cdr


   # create reader instance
   with Reader('/home/ros/rosbag_2020_03_24.bag') as reader:
       # topic and msgtype information is available on .connections list
       for connection in reader.connections:
           print(connection.topic, connection.msgtype)

       # iterate over messages
       for connection, timestamp, rawdata in reader.messages():
           if connection.topic == '/imu_raw/Imu':
               msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
               print(msg.header.frame_id)

       # messages() accepts connection filters
       connections = [x for x in reader.connections if x.topic == '/imu_raw/Imu']
       for connection, timestamp, rawdata in reader.messages(connections=connections):
           msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
           print(msg.header.frame_id)
