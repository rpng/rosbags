FROM ros:rolling

RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y \
      python3-pip

RUN python3 -m pip install ruamel.yaml zstandard

COPY src/rosbags /opt/ros/rolling/lib/python3.8/site-packages/rosbags
COPY tools/bench/bench.py /

CMD ["/usr/bin/python3", "/bench.py", "/rosbag2"]
