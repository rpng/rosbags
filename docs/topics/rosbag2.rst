Rosbag2
=======
The :py:mod:`rosbags.rosbag2` package provides a conformant implementation of rosbag2. It provides read-write access to raw message data saved inside rosbag2 containers, and supports all features present in the C++ reference implementation.

Supported Versions
------------------
All versions up to the current (ROS2 Foxy) version 4 are supported.

Supported Features
------------------
Rosbag2 is a flexible format that supports plugging different serialization methods, compression formats, and storage containers together. The rosbag2 C++ reference implementation is build around plugins that provide serialization, compression, and storage. This project implements all rosbag2 core plugins that are distributed with the C++ reference implementation.

:Serializers:
    - cdr (without wstring)

:Compressors:
    - zstd

:Storages:
    - sqlite3

Writing rosbag2
---------------
Instances of the :py:class:`Writer <rosbags.rosbag2.Writer>` class can create and write to new rosbag2 files. It is usually used as a context manager. Before the first message of a topic can be written, its topic must first be added to the bag. The following example shows the typical usage pattern:

.. code-block:: python

   from rosbags.rosbag2 import Writer
   from rosbags.serde import serialize_cdr
   from rosbags.typesys.types import std_msgs__msg__String as String

   # create writer instance and open for writing
   with Writer('/home/ros/rosbag_2020_03_24') as writer:
       # add new connection
       topic = '/chatter'
       msgtype = String.__msgtype__
       connection = writer.add_connection(topic, msgtype, 'cdr', '')

       # serialize and write message
       timestamp = 42
       message = String('hello world')
       writer.write(connection, timestamp, serialize_cdr(message, msgtype))

Reading rosbag2
---------------
Instances of the :py:class:`Reader <rosbags.rosbag2.Reader>` class are used to read rosbag2 metadata and its contents. Most of the metadata is available on Reader instances right away, messages can only be accessed after the bag has been opened. To this end it is recommended to use the Reader as a context manager. The following example shows the typical usage pattern:

.. code-block:: python

   from rosbags.rosbag2 import Reader
   from rosbags.serde import deserialize_cdr

   # create reader instance and open for reading
   with Reader('/home/ros/rosbag_2020_03_24') as reader:
       # topic and msgtype information is available on .connections dict
       for connection in reader.connections.values():
           print(connection.topic, connection.msgtype)

       # iterate over messages
       for connection, timestamp, rawdata in reader.messages():
           if connection.topic == '/imu_raw/Imu':
               msg = deserialize_cdr(rawdata, connection.msgtype)
               print(msg.header.frame_id)

       # messages() accepts connection filters
       connections = [x for x in reader.connections.values() if x.topic == '/imu_raw/Imu']
       for connection, timestamp, rawdata in reader.messages(connections=connections):
           msg = deserialize_cdr(rawdata, connection.msgtype)
           print(msg.header.frame_id)
