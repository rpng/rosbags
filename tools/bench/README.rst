=====
Bench
=====

Check and benchmark ``rosbags.rosbag2`` agains ``rosbag2_py``. The provided Dockerfile creates an execution environment for the script. Run from the root of this repository::

  $ docker build -t rosbags/bench -f tools/bench/Dockerfile .

The docker image expects that the rosbag2 file to benchmark is mounted under ``/rosbag2``::

  $ docker run --rm -v /path/to/bag:/rosbag2 rosbags/bench
