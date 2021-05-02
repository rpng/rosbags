Serialization and deserialization
=================================

The serialization and deserialization system :py:mod:`rosbags.serde` supports multiple raw message formats. For each format it provides a pair of functions, one for serialization and one for deserialization. In addition to the data to process each function usually only requires the message type name.

Deserialization
---------------

Deserialize a CDR bytes object using :py:func:`deserialize_cdr() <rosbags.serde.deserialize_cdr>`:

.. code-block:: python

   from rosbags.serde import deserialize_cdr

   # rawdata is of type bytes and contains serialized message
   msg = deserialize_cdr(rawdata, 'geometry_msgs/msg/Quaternion')

Serialization
---------------

Serialize a message with CDR using :py:func:`serialize_cdr() <rosbags.serde.serialize_cdr>`:
   
.. code-block:: python

   from rosbags.serde import serialize_cdr

   # serialize message with system endianess
   serialized = serialize_cdr(msg, 'geometry_msgs/msg/Quaternion')

   # serialize message with explicit endianess
   serialized = serialize_cdr(msg, 'geometry_msgs/msg/Quaternion', little_endian=False)
