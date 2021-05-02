FROM ros:rolling

RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y \
      python3-pip \
      python3-rosbag

COPY tools/compare/compare.py /

CMD ["/usr/bin/python3", "/compare.py", "/rosbag1", "/rosbag2"]
