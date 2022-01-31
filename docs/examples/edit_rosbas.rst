Edit rosbags
============

Rosbags does not support opening files in read-write mode, but implicitly enforces copy-on-write semantics. Apart from the mapping of reader to writer connections the process is fairly straightforward.


Remove topic
------------

.. literalinclude:: ./edit_rosbags_remove_topic.py


Edit timestamps
---------------

.. literalinclude:: ./edit_rosbags_edit_timestamps.py
