.. _changes:

Changes
=======

0.9.5 - 2021-10-04
------------------
- Add string constant support to msg parser

0.9.4 - 2021-09-15
------------------
- Make reader1 API match reader2
- Fix connection mapping for reader2 messages


0.9.3 - 2021-08-06
------------------

- Add const fields to type classes
- Add CDR to ROS1 bytestream conversion
- Add ROS1 message definiton generator
- Use connection oriented APIs in readers and writers
- Add rosbag1 writer


0.9.2 - 2021-07-08
------------------

- Support relative type references in msg files


0.9.1 - 2021-07-05
------------------

- Use half-open intervals for time ranges
- Create appropriate QoS profiles for latched topics in converted bags
- Fix return value tuple order of messages() in documentation `#2`_
- Add type hints to message classes
- Remove non-default ROS2 message types
- Support multi-line comments in idl files
- Fix parsing of msg files on non-POSIX platforms `#4`_

.. _#2: https://gitlab.com/ternaris/rosbags/issues/2
.. _#4: https://gitlab.com/ternaris/rosbags/issues/4


0.9.0 - 2021-05-16
------------------

- Initial Release
