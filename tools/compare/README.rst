=======
Compare
=======

Check if the contents of a ``rosbag1`` and another ``rosbag1`` or ``rosbag2`` file are identical. The provided Dockerfile creates an execution environment for the script. Run from the root of this repository::

  $ docker build -t rosbags/compare -f tools/compare/Dockerfile .

The docker image expects that the first rosbag1 and second rosbag1 or rosbag2 files to be mounted at ``/rosbag1`` and ``/rosbag2`` respectively::

  $ docker run --rm -v /path/to/rosbag1.bag:/rosbag1 -v /path/to/rosbag2:/rosbag2 rosbags/compare
