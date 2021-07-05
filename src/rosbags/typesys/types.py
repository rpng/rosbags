# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
#
# THIS FILE IS GENERATED, DO NOT EDIT
"""ROS2 message types."""

# flake8: noqa N801
# pylint: disable=invalid-name,too-many-instance-attributes,too-many-lines
# pylint: disable=unsubscriptable-object

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

    import numpy


@dataclass
class builtin_interfaces__msg__Time:
    """Class for builtin_interfaces/msg/Time."""

    sec: int
    nanosec: int


@dataclass
class builtin_interfaces__msg__Duration:
    """Class for builtin_interfaces/msg/Duration."""

    sec: int
    nanosec: int


@dataclass
class diagnostic_msgs__msg__DiagnosticStatus:
    """Class for diagnostic_msgs/msg/DiagnosticStatus."""

    level: int
    name: str
    message: str
    hardware_id: str
    values: list[diagnostic_msgs__msg__KeyValue]


@dataclass
class diagnostic_msgs__msg__DiagnosticArray:
    """Class for diagnostic_msgs/msg/DiagnosticArray."""

    header: std_msgs__msg__Header
    status: list[diagnostic_msgs__msg__DiagnosticStatus]


@dataclass
class diagnostic_msgs__msg__KeyValue:
    """Class for diagnostic_msgs/msg/KeyValue."""

    key: str
    value: str


@dataclass
class geometry_msgs__msg__AccelWithCovariance:
    """Class for geometry_msgs/msg/AccelWithCovariance."""

    accel: geometry_msgs__msg__Accel
    covariance: numpy.ndarray[Any, numpy.dtype[numpy.float64]]


@dataclass
class geometry_msgs__msg__Point32:
    """Class for geometry_msgs/msg/Point32."""

    x: float
    y: float
    z: float


@dataclass
class geometry_msgs__msg__Vector3:
    """Class for geometry_msgs/msg/Vector3."""

    x: float
    y: float
    z: float


@dataclass
class geometry_msgs__msg__Inertia:
    """Class for geometry_msgs/msg/Inertia."""

    m: float
    com: geometry_msgs__msg__Vector3
    ixx: float
    ixy: float
    ixz: float
    iyy: float
    iyz: float
    izz: float


@dataclass
class geometry_msgs__msg__PoseWithCovarianceStamped:
    """Class for geometry_msgs/msg/PoseWithCovarianceStamped."""

    header: std_msgs__msg__Header
    pose: geometry_msgs__msg__PoseWithCovariance


@dataclass
class geometry_msgs__msg__Twist:
    """Class for geometry_msgs/msg/Twist."""

    linear: geometry_msgs__msg__Vector3
    angular: geometry_msgs__msg__Vector3


@dataclass
class geometry_msgs__msg__Pose:
    """Class for geometry_msgs/msg/Pose."""

    position: geometry_msgs__msg__Point
    orientation: geometry_msgs__msg__Quaternion


@dataclass
class geometry_msgs__msg__Point:
    """Class for geometry_msgs/msg/Point."""

    x: float
    y: float
    z: float


@dataclass
class geometry_msgs__msg__Vector3Stamped:
    """Class for geometry_msgs/msg/Vector3Stamped."""

    header: std_msgs__msg__Header
    vector: geometry_msgs__msg__Vector3


@dataclass
class geometry_msgs__msg__Transform:
    """Class for geometry_msgs/msg/Transform."""

    translation: geometry_msgs__msg__Vector3
    rotation: geometry_msgs__msg__Quaternion


@dataclass
class geometry_msgs__msg__PolygonStamped:
    """Class for geometry_msgs/msg/PolygonStamped."""

    header: std_msgs__msg__Header
    polygon: geometry_msgs__msg__Polygon


@dataclass
class geometry_msgs__msg__Quaternion:
    """Class for geometry_msgs/msg/Quaternion."""

    x: float
    y: float
    z: float
    w: float


@dataclass
class geometry_msgs__msg__Pose2D:
    """Class for geometry_msgs/msg/Pose2D."""

    x: float
    y: float
    theta: float


@dataclass
class geometry_msgs__msg__InertiaStamped:
    """Class for geometry_msgs/msg/InertiaStamped."""

    header: std_msgs__msg__Header
    inertia: geometry_msgs__msg__Inertia


@dataclass
class geometry_msgs__msg__TwistStamped:
    """Class for geometry_msgs/msg/TwistStamped."""

    header: std_msgs__msg__Header
    twist: geometry_msgs__msg__Twist


@dataclass
class geometry_msgs__msg__PoseStamped:
    """Class for geometry_msgs/msg/PoseStamped."""

    header: std_msgs__msg__Header
    pose: geometry_msgs__msg__Pose


@dataclass
class geometry_msgs__msg__PointStamped:
    """Class for geometry_msgs/msg/PointStamped."""

    header: std_msgs__msg__Header
    point: geometry_msgs__msg__Point


@dataclass
class geometry_msgs__msg__Polygon:
    """Class for geometry_msgs/msg/Polygon."""

    points: list[geometry_msgs__msg__Point32]


@dataclass
class geometry_msgs__msg__PoseArray:
    """Class for geometry_msgs/msg/PoseArray."""

    header: std_msgs__msg__Header
    poses: list[geometry_msgs__msg__Pose]


@dataclass
class geometry_msgs__msg__AccelStamped:
    """Class for geometry_msgs/msg/AccelStamped."""

    header: std_msgs__msg__Header
    accel: geometry_msgs__msg__Accel


@dataclass
class geometry_msgs__msg__TwistWithCovarianceStamped:
    """Class for geometry_msgs/msg/TwistWithCovarianceStamped."""

    header: std_msgs__msg__Header
    twist: geometry_msgs__msg__TwistWithCovariance


@dataclass
class geometry_msgs__msg__QuaternionStamped:
    """Class for geometry_msgs/msg/QuaternionStamped."""

    header: std_msgs__msg__Header
    quaternion: geometry_msgs__msg__Quaternion


@dataclass
class geometry_msgs__msg__WrenchStamped:
    """Class for geometry_msgs/msg/WrenchStamped."""

    header: std_msgs__msg__Header
    wrench: geometry_msgs__msg__Wrench


@dataclass
class geometry_msgs__msg__AccelWithCovarianceStamped:
    """Class for geometry_msgs/msg/AccelWithCovarianceStamped."""

    header: std_msgs__msg__Header
    accel: geometry_msgs__msg__AccelWithCovariance


@dataclass
class geometry_msgs__msg__PoseWithCovariance:
    """Class for geometry_msgs/msg/PoseWithCovariance."""

    pose: geometry_msgs__msg__Pose
    covariance: numpy.ndarray[Any, numpy.dtype[numpy.float64]]


@dataclass
class geometry_msgs__msg__Wrench:
    """Class for geometry_msgs/msg/Wrench."""

    force: geometry_msgs__msg__Vector3
    torque: geometry_msgs__msg__Vector3


@dataclass
class geometry_msgs__msg__TransformStamped:
    """Class for geometry_msgs/msg/TransformStamped."""

    header: std_msgs__msg__Header
    child_frame_id: str
    transform: geometry_msgs__msg__Transform


@dataclass
class geometry_msgs__msg__Accel:
    """Class for geometry_msgs/msg/Accel."""

    linear: geometry_msgs__msg__Vector3
    angular: geometry_msgs__msg__Vector3


@dataclass
class geometry_msgs__msg__TwistWithCovariance:
    """Class for geometry_msgs/msg/TwistWithCovariance."""

    twist: geometry_msgs__msg__Twist
    covariance: numpy.ndarray[Any, numpy.dtype[numpy.float64]]


@dataclass
class libstatistics_collector__msg__DummyMessage:
    """Class for libstatistics_collector/msg/DummyMessage."""

    header: std_msgs__msg__Header


@dataclass
class lifecycle_msgs__msg__TransitionDescription:
    """Class for lifecycle_msgs/msg/TransitionDescription."""

    transition: lifecycle_msgs__msg__Transition
    start_state: lifecycle_msgs__msg__State
    goal_state: lifecycle_msgs__msg__State


@dataclass
class lifecycle_msgs__msg__State:
    """Class for lifecycle_msgs/msg/State."""

    id: int
    label: str


@dataclass
class lifecycle_msgs__msg__TransitionEvent:
    """Class for lifecycle_msgs/msg/TransitionEvent."""

    timestamp: int
    transition: lifecycle_msgs__msg__Transition
    start_state: lifecycle_msgs__msg__State
    goal_state: lifecycle_msgs__msg__State


@dataclass
class lifecycle_msgs__msg__Transition:
    """Class for lifecycle_msgs/msg/Transition."""

    id: int
    label: str


@dataclass
class nav_msgs__msg__MapMetaData:
    """Class for nav_msgs/msg/MapMetaData."""

    map_load_time: builtin_interfaces__msg__Time
    resolution: float
    width: int
    height: int
    origin: geometry_msgs__msg__Pose


@dataclass
class nav_msgs__msg__GridCells:
    """Class for nav_msgs/msg/GridCells."""

    header: std_msgs__msg__Header
    cell_width: float
    cell_height: float
    cells: list[geometry_msgs__msg__Point]


@dataclass
class nav_msgs__msg__Odometry:
    """Class for nav_msgs/msg/Odometry."""

    header: std_msgs__msg__Header
    child_frame_id: str
    pose: geometry_msgs__msg__PoseWithCovariance
    twist: geometry_msgs__msg__TwistWithCovariance


@dataclass
class nav_msgs__msg__Path:
    """Class for nav_msgs/msg/Path."""

    header: std_msgs__msg__Header
    poses: list[geometry_msgs__msg__PoseStamped]


@dataclass
class nav_msgs__msg__OccupancyGrid:
    """Class for nav_msgs/msg/OccupancyGrid."""

    header: std_msgs__msg__Header
    info: nav_msgs__msg__MapMetaData
    data: numpy.ndarray[Any, numpy.dtype[numpy.int8]]


@dataclass
class rcl_interfaces__msg__ListParametersResult:
    """Class for rcl_interfaces/msg/ListParametersResult."""

    names: list[str]
    prefixes: list[str]


@dataclass
class rcl_interfaces__msg__ParameterType:
    """Class for rcl_interfaces/msg/ParameterType."""

    structure_needs_at_least_one_member: int


@dataclass
class rcl_interfaces__msg__ParameterEventDescriptors:
    """Class for rcl_interfaces/msg/ParameterEventDescriptors."""

    new_parameters: list[rcl_interfaces__msg__ParameterDescriptor]
    changed_parameters: list[rcl_interfaces__msg__ParameterDescriptor]
    deleted_parameters: list[rcl_interfaces__msg__ParameterDescriptor]


@dataclass
class rcl_interfaces__msg__ParameterEvent:
    """Class for rcl_interfaces/msg/ParameterEvent."""

    stamp: builtin_interfaces__msg__Time
    node: str
    new_parameters: list[rcl_interfaces__msg__Parameter]
    changed_parameters: list[rcl_interfaces__msg__Parameter]
    deleted_parameters: list[rcl_interfaces__msg__Parameter]


@dataclass
class rcl_interfaces__msg__IntegerRange:
    """Class for rcl_interfaces/msg/IntegerRange."""

    from_value: int
    to_value: int
    step: int


@dataclass
class rcl_interfaces__msg__Parameter:
    """Class for rcl_interfaces/msg/Parameter."""

    name: str
    value: rcl_interfaces__msg__ParameterValue


@dataclass
class rcl_interfaces__msg__ParameterValue:
    """Class for rcl_interfaces/msg/ParameterValue."""

    type: int
    bool_value: bool
    integer_value: int
    double_value: float
    string_value: str
    byte_array_value: numpy.ndarray[Any, numpy.dtype[numpy.uint8]]
    bool_array_value: numpy.ndarray[Any, numpy.dtype[numpy.bool8]]
    integer_array_value: numpy.ndarray[Any, numpy.dtype[numpy.int64]]
    double_array_value: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    string_array_value: list[str]


@dataclass
class rcl_interfaces__msg__FloatingPointRange:
    """Class for rcl_interfaces/msg/FloatingPointRange."""

    from_value: float
    to_value: float
    step: float


@dataclass
class rcl_interfaces__msg__SetParametersResult:
    """Class for rcl_interfaces/msg/SetParametersResult."""

    successful: bool
    reason: str


@dataclass
class rcl_interfaces__msg__Log:
    """Class for rcl_interfaces/msg/Log."""

    stamp: builtin_interfaces__msg__Time
    level: int
    name: str
    msg: str
    file: str
    function: str
    line: int


@dataclass
class rcl_interfaces__msg__ParameterDescriptor:
    """Class for rcl_interfaces/msg/ParameterDescriptor."""

    name: str
    type: int
    description: str
    additional_constraints: str
    read_only: bool
    floating_point_range: list[rcl_interfaces__msg__FloatingPointRange]
    integer_range: list[rcl_interfaces__msg__IntegerRange]


@dataclass
class rmw_dds_common__msg__Gid:
    """Class for rmw_dds_common/msg/Gid."""

    data: numpy.ndarray[Any, numpy.dtype[numpy.uint8]]


@dataclass
class rmw_dds_common__msg__NodeEntitiesInfo:
    """Class for rmw_dds_common/msg/NodeEntitiesInfo."""

    node_namespace: str
    node_name: str
    reader_gid_seq: list[rmw_dds_common__msg__Gid]
    writer_gid_seq: list[rmw_dds_common__msg__Gid]


@dataclass
class rmw_dds_common__msg__ParticipantEntitiesInfo:
    """Class for rmw_dds_common/msg/ParticipantEntitiesInfo."""

    gid: rmw_dds_common__msg__Gid
    node_entities_info_seq: list[rmw_dds_common__msg__NodeEntitiesInfo]


@dataclass
class rosgraph_msgs__msg__Clock:
    """Class for rosgraph_msgs/msg/Clock."""

    clock: builtin_interfaces__msg__Time


@dataclass
class sensor_msgs__msg__Temperature:
    """Class for sensor_msgs/msg/Temperature."""

    header: std_msgs__msg__Header
    temperature: float
    variance: float


@dataclass
class sensor_msgs__msg__Range:
    """Class for sensor_msgs/msg/Range."""

    header: std_msgs__msg__Header
    radiation_type: int
    field_of_view: float
    min_range: float
    max_range: float
    range: float


@dataclass
class sensor_msgs__msg__RegionOfInterest:
    """Class for sensor_msgs/msg/RegionOfInterest."""

    x_offset: int
    y_offset: int
    height: int
    width: int
    do_rectify: bool


@dataclass
class sensor_msgs__msg__JoyFeedbackArray:
    """Class for sensor_msgs/msg/JoyFeedbackArray."""

    array: list[sensor_msgs__msg__JoyFeedback]


@dataclass
class sensor_msgs__msg__TimeReference:
    """Class for sensor_msgs/msg/TimeReference."""

    header: std_msgs__msg__Header
    time_ref: builtin_interfaces__msg__Time
    source: str


@dataclass
class sensor_msgs__msg__CompressedImage:
    """Class for sensor_msgs/msg/CompressedImage."""

    header: std_msgs__msg__Header
    format: str
    data: numpy.ndarray[Any, numpy.dtype[numpy.uint8]]


@dataclass
class sensor_msgs__msg__MultiEchoLaserScan:
    """Class for sensor_msgs/msg/MultiEchoLaserScan."""

    header: std_msgs__msg__Header
    angle_min: float
    angle_max: float
    angle_increment: float
    time_increment: float
    scan_time: float
    range_min: float
    range_max: float
    ranges: list[sensor_msgs__msg__LaserEcho]
    intensities: list[sensor_msgs__msg__LaserEcho]


@dataclass
class sensor_msgs__msg__LaserEcho:
    """Class for sensor_msgs/msg/LaserEcho."""

    echoes: numpy.ndarray[Any, numpy.dtype[numpy.float32]]


@dataclass
class sensor_msgs__msg__ChannelFloat32:
    """Class for sensor_msgs/msg/ChannelFloat32."""

    name: str
    values: numpy.ndarray[Any, numpy.dtype[numpy.float32]]


@dataclass
class sensor_msgs__msg__CameraInfo:
    """Class for sensor_msgs/msg/CameraInfo."""

    header: std_msgs__msg__Header
    height: int
    width: int
    distortion_model: str
    d: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    k: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    r: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    p: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    binning_x: int
    binning_y: int
    roi: sensor_msgs__msg__RegionOfInterest


@dataclass
class sensor_msgs__msg__RelativeHumidity:
    """Class for sensor_msgs/msg/RelativeHumidity."""

    header: std_msgs__msg__Header
    relative_humidity: float
    variance: float


@dataclass
class sensor_msgs__msg__FluidPressure:
    """Class for sensor_msgs/msg/FluidPressure."""

    header: std_msgs__msg__Header
    fluid_pressure: float
    variance: float


@dataclass
class sensor_msgs__msg__LaserScan:
    """Class for sensor_msgs/msg/LaserScan."""

    header: std_msgs__msg__Header
    angle_min: float
    angle_max: float
    angle_increment: float
    time_increment: float
    scan_time: float
    range_min: float
    range_max: float
    ranges: numpy.ndarray[Any, numpy.dtype[numpy.float32]]
    intensities: numpy.ndarray[Any, numpy.dtype[numpy.float32]]


@dataclass
class sensor_msgs__msg__BatteryState:
    """Class for sensor_msgs/msg/BatteryState."""

    header: std_msgs__msg__Header
    voltage: float
    temperature: float
    current: float
    charge: float
    capacity: float
    design_capacity: float
    percentage: float
    power_supply_status: int
    power_supply_health: int
    power_supply_technology: int
    present: bool
    cell_voltage: numpy.ndarray[Any, numpy.dtype[numpy.float32]]
    cell_temperature: numpy.ndarray[Any, numpy.dtype[numpy.float32]]
    location: str
    serial_number: str


@dataclass
class sensor_msgs__msg__Image:
    """Class for sensor_msgs/msg/Image."""

    header: std_msgs__msg__Header
    height: int
    width: int
    encoding: str
    is_bigendian: int
    step: int
    data: numpy.ndarray[Any, numpy.dtype[numpy.uint8]]


@dataclass
class sensor_msgs__msg__PointCloud:
    """Class for sensor_msgs/msg/PointCloud."""

    header: std_msgs__msg__Header
    points: list[geometry_msgs__msg__Point32]
    channels: list[sensor_msgs__msg__ChannelFloat32]


@dataclass
class sensor_msgs__msg__Imu:
    """Class for sensor_msgs/msg/Imu."""

    header: std_msgs__msg__Header
    orientation: geometry_msgs__msg__Quaternion
    orientation_covariance: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    angular_velocity: geometry_msgs__msg__Vector3
    angular_velocity_covariance: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    linear_acceleration: geometry_msgs__msg__Vector3
    linear_acceleration_covariance: numpy.ndarray[Any, numpy.dtype[numpy.float64]]


@dataclass
class sensor_msgs__msg__NavSatStatus:
    """Class for sensor_msgs/msg/NavSatStatus."""

    status: int
    service: int


@dataclass
class sensor_msgs__msg__Illuminance:
    """Class for sensor_msgs/msg/Illuminance."""

    header: std_msgs__msg__Header
    illuminance: float
    variance: float


@dataclass
class sensor_msgs__msg__Joy:
    """Class for sensor_msgs/msg/Joy."""

    header: std_msgs__msg__Header
    axes: numpy.ndarray[Any, numpy.dtype[numpy.float32]]
    buttons: numpy.ndarray[Any, numpy.dtype[numpy.int32]]


@dataclass
class sensor_msgs__msg__NavSatFix:
    """Class for sensor_msgs/msg/NavSatFix."""

    header: std_msgs__msg__Header
    status: sensor_msgs__msg__NavSatStatus
    latitude: float
    longitude: float
    altitude: float
    position_covariance: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    position_covariance_type: int


@dataclass
class sensor_msgs__msg__MultiDOFJointState:
    """Class for sensor_msgs/msg/MultiDOFJointState."""

    header: std_msgs__msg__Header
    joint_names: list[str]
    transforms: list[geometry_msgs__msg__Transform]
    twist: list[geometry_msgs__msg__Twist]
    wrench: list[geometry_msgs__msg__Wrench]


@dataclass
class sensor_msgs__msg__MagneticField:
    """Class for sensor_msgs/msg/MagneticField."""

    header: std_msgs__msg__Header
    magnetic_field: geometry_msgs__msg__Vector3
    magnetic_field_covariance: numpy.ndarray[Any, numpy.dtype[numpy.float64]]


@dataclass
class sensor_msgs__msg__JointState:
    """Class for sensor_msgs/msg/JointState."""

    header: std_msgs__msg__Header
    name: list[str]
    position: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    velocity: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    effort: numpy.ndarray[Any, numpy.dtype[numpy.float64]]


@dataclass
class sensor_msgs__msg__PointField:
    """Class for sensor_msgs/msg/PointField."""

    name: str
    offset: int
    datatype: int
    count: int


@dataclass
class sensor_msgs__msg__PointCloud2:
    """Class for sensor_msgs/msg/PointCloud2."""

    header: std_msgs__msg__Header
    height: int
    width: int
    fields: list[sensor_msgs__msg__PointField]
    is_bigendian: bool
    point_step: int
    row_step: int
    data: numpy.ndarray[Any, numpy.dtype[numpy.uint8]]
    is_dense: bool


@dataclass
class sensor_msgs__msg__JoyFeedback:
    """Class for sensor_msgs/msg/JoyFeedback."""

    type: int
    id: int
    intensity: float


@dataclass
class shape_msgs__msg__SolidPrimitive:
    """Class for shape_msgs/msg/SolidPrimitive."""

    type: int
    dimensions: numpy.ndarray[Any, numpy.dtype[numpy.float64]]


@dataclass
class shape_msgs__msg__Mesh:
    """Class for shape_msgs/msg/Mesh."""

    triangles: list[shape_msgs__msg__MeshTriangle]
    vertices: list[geometry_msgs__msg__Point]


@dataclass
class shape_msgs__msg__Plane:
    """Class for shape_msgs/msg/Plane."""

    coef: numpy.ndarray[Any, numpy.dtype[numpy.float64]]


@dataclass
class shape_msgs__msg__MeshTriangle:
    """Class for shape_msgs/msg/MeshTriangle."""

    vertex_indices: numpy.ndarray[Any, numpy.dtype[numpy.uint32]]


@dataclass
class statistics_msgs__msg__StatisticDataType:
    """Class for statistics_msgs/msg/StatisticDataType."""

    structure_needs_at_least_one_member: int


@dataclass
class statistics_msgs__msg__StatisticDataPoint:
    """Class for statistics_msgs/msg/StatisticDataPoint."""

    data_type: int
    data: float


@dataclass
class statistics_msgs__msg__MetricsMessage:
    """Class for statistics_msgs/msg/MetricsMessage."""

    measurement_source_name: str
    metrics_source: str
    unit: str
    window_start: builtin_interfaces__msg__Time
    window_stop: builtin_interfaces__msg__Time
    statistics: list[statistics_msgs__msg__StatisticDataPoint]


@dataclass
class std_msgs__msg__UInt8:
    """Class for std_msgs/msg/UInt8."""

    data: int


@dataclass
class std_msgs__msg__Float32MultiArray:
    """Class for std_msgs/msg/Float32MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.float32]]


@dataclass
class std_msgs__msg__Int8:
    """Class for std_msgs/msg/Int8."""

    data: int


@dataclass
class std_msgs__msg__Empty:
    """Class for std_msgs/msg/Empty."""

    structure_needs_at_least_one_member: int


@dataclass
class std_msgs__msg__String:
    """Class for std_msgs/msg/String."""

    data: str


@dataclass
class std_msgs__msg__MultiArrayDimension:
    """Class for std_msgs/msg/MultiArrayDimension."""

    label: str
    size: int
    stride: int


@dataclass
class std_msgs__msg__UInt64:
    """Class for std_msgs/msg/UInt64."""

    data: int


@dataclass
class std_msgs__msg__UInt16:
    """Class for std_msgs/msg/UInt16."""

    data: int


@dataclass
class std_msgs__msg__Float32:
    """Class for std_msgs/msg/Float32."""

    data: float


@dataclass
class std_msgs__msg__Int64:
    """Class for std_msgs/msg/Int64."""

    data: int


@dataclass
class std_msgs__msg__Int16MultiArray:
    """Class for std_msgs/msg/Int16MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.int16]]


@dataclass
class std_msgs__msg__Int16:
    """Class for std_msgs/msg/Int16."""

    data: int


@dataclass
class std_msgs__msg__Float64MultiArray:
    """Class for std_msgs/msg/Float64MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.float64]]


@dataclass
class std_msgs__msg__MultiArrayLayout:
    """Class for std_msgs/msg/MultiArrayLayout."""

    dim: list[std_msgs__msg__MultiArrayDimension]
    data_offset: int


@dataclass
class std_msgs__msg__UInt32MultiArray:
    """Class for std_msgs/msg/UInt32MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.uint32]]


@dataclass
class std_msgs__msg__Header:
    """Class for std_msgs/msg/Header."""

    stamp: builtin_interfaces__msg__Time
    frame_id: str


@dataclass
class std_msgs__msg__ByteMultiArray:
    """Class for std_msgs/msg/ByteMultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.uint8]]


@dataclass
class std_msgs__msg__Int8MultiArray:
    """Class for std_msgs/msg/Int8MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.int8]]


@dataclass
class std_msgs__msg__Float64:
    """Class for std_msgs/msg/Float64."""

    data: float


@dataclass
class std_msgs__msg__UInt8MultiArray:
    """Class for std_msgs/msg/UInt8MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.uint8]]


@dataclass
class std_msgs__msg__Byte:
    """Class for std_msgs/msg/Byte."""

    data: int


@dataclass
class std_msgs__msg__Char:
    """Class for std_msgs/msg/Char."""

    data: int


@dataclass
class std_msgs__msg__UInt64MultiArray:
    """Class for std_msgs/msg/UInt64MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.uint64]]


@dataclass
class std_msgs__msg__Int32MultiArray:
    """Class for std_msgs/msg/Int32MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.int32]]


@dataclass
class std_msgs__msg__ColorRGBA:
    """Class for std_msgs/msg/ColorRGBA."""

    r: float
    g: float
    b: float
    a: float


@dataclass
class std_msgs__msg__Bool:
    """Class for std_msgs/msg/Bool."""

    data: bool


@dataclass
class std_msgs__msg__UInt32:
    """Class for std_msgs/msg/UInt32."""

    data: int


@dataclass
class std_msgs__msg__Int64MultiArray:
    """Class for std_msgs/msg/Int64MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.int64]]


@dataclass
class std_msgs__msg__Int32:
    """Class for std_msgs/msg/Int32."""

    data: int


@dataclass
class std_msgs__msg__UInt16MultiArray:
    """Class for std_msgs/msg/UInt16MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.uint16]]


@dataclass
class stereo_msgs__msg__DisparityImage:
    """Class for stereo_msgs/msg/DisparityImage."""

    header: std_msgs__msg__Header
    image: sensor_msgs__msg__Image
    f: float
    t: float
    valid_window: sensor_msgs__msg__RegionOfInterest
    min_disparity: float
    max_disparity: float
    delta_d: float


@dataclass
class tf2_msgs__msg__TF2Error:
    """Class for tf2_msgs/msg/TF2Error."""

    error: int
    error_string: str


@dataclass
class tf2_msgs__msg__TFMessage:
    """Class for tf2_msgs/msg/TFMessage."""

    transforms: list[geometry_msgs__msg__TransformStamped]


@dataclass
class trajectory_msgs__msg__MultiDOFJointTrajectory:
    """Class for trajectory_msgs/msg/MultiDOFJointTrajectory."""

    header: std_msgs__msg__Header
    joint_names: list[str]
    points: list[trajectory_msgs__msg__MultiDOFJointTrajectoryPoint]


@dataclass
class trajectory_msgs__msg__JointTrajectory:
    """Class for trajectory_msgs/msg/JointTrajectory."""

    header: std_msgs__msg__Header
    joint_names: list[str]
    points: list[trajectory_msgs__msg__JointTrajectoryPoint]


@dataclass
class trajectory_msgs__msg__JointTrajectoryPoint:
    """Class for trajectory_msgs/msg/JointTrajectoryPoint."""

    positions: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    velocities: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    accelerations: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    effort: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    time_from_start: builtin_interfaces__msg__Duration


@dataclass
class trajectory_msgs__msg__MultiDOFJointTrajectoryPoint:
    """Class for trajectory_msgs/msg/MultiDOFJointTrajectoryPoint."""

    transforms: list[geometry_msgs__msg__Transform]
    velocities: list[geometry_msgs__msg__Twist]
    accelerations: list[geometry_msgs__msg__Twist]
    time_from_start: builtin_interfaces__msg__Duration


@dataclass
class unique_identifier_msgs__msg__UUID:
    """Class for unique_identifier_msgs/msg/UUID."""

    uuid: numpy.ndarray[Any, numpy.dtype[numpy.uint8]]


@dataclass
class visualization_msgs__msg__Marker:
    """Class for visualization_msgs/msg/Marker."""

    header: std_msgs__msg__Header
    ns: str
    id: int
    type: int
    action: int
    pose: geometry_msgs__msg__Pose
    scale: geometry_msgs__msg__Vector3
    color: std_msgs__msg__ColorRGBA
    lifetime: builtin_interfaces__msg__Duration
    frame_locked: bool
    points: list[geometry_msgs__msg__Point]
    colors: list[std_msgs__msg__ColorRGBA]
    text: str
    mesh_resource: str
    mesh_use_embedded_materials: bool


@dataclass
class visualization_msgs__msg__InteractiveMarkerInit:
    """Class for visualization_msgs/msg/InteractiveMarkerInit."""

    server_id: str
    seq_num: int
    markers: list[visualization_msgs__msg__InteractiveMarker]


@dataclass
class visualization_msgs__msg__MenuEntry:
    """Class for visualization_msgs/msg/MenuEntry."""

    id: int
    parent_id: int
    title: str
    command: str
    command_type: int


@dataclass
class visualization_msgs__msg__MarkerArray:
    """Class for visualization_msgs/msg/MarkerArray."""

    markers: list[visualization_msgs__msg__Marker]


@dataclass
class visualization_msgs__msg__InteractiveMarkerUpdate:
    """Class for visualization_msgs/msg/InteractiveMarkerUpdate."""

    server_id: str
    seq_num: int
    type: int
    markers: list[visualization_msgs__msg__InteractiveMarker]
    poses: list[visualization_msgs__msg__InteractiveMarkerPose]
    erases: list[str]


@dataclass
class visualization_msgs__msg__InteractiveMarker:
    """Class for visualization_msgs/msg/InteractiveMarker."""

    header: std_msgs__msg__Header
    pose: geometry_msgs__msg__Pose
    name: str
    description: str
    scale: float
    menu_entries: list[visualization_msgs__msg__MenuEntry]
    controls: list[visualization_msgs__msg__InteractiveMarkerControl]


@dataclass
class visualization_msgs__msg__InteractiveMarkerFeedback:
    """Class for visualization_msgs/msg/InteractiveMarkerFeedback."""

    header: std_msgs__msg__Header
    client_id: str
    marker_name: str
    control_name: str
    event_type: int
    pose: geometry_msgs__msg__Pose
    menu_entry_id: int
    mouse_point: geometry_msgs__msg__Point
    mouse_point_valid: bool


@dataclass
class visualization_msgs__msg__ImageMarker:
    """Class for visualization_msgs/msg/ImageMarker."""

    header: std_msgs__msg__Header
    ns: str
    id: int
    type: int
    action: int
    position: geometry_msgs__msg__Point
    scale: float
    outline_color: std_msgs__msg__ColorRGBA
    filled: int
    fill_color: std_msgs__msg__ColorRGBA
    lifetime: builtin_interfaces__msg__Duration
    points: list[geometry_msgs__msg__Point]
    outline_colors: list[std_msgs__msg__ColorRGBA]


@dataclass
class visualization_msgs__msg__InteractiveMarkerControl:
    """Class for visualization_msgs/msg/InteractiveMarkerControl."""

    name: str
    orientation: geometry_msgs__msg__Quaternion
    orientation_mode: int
    interaction_mode: int
    always_visible: bool
    markers: list[visualization_msgs__msg__Marker]
    independent_marker_orientation: bool
    description: str


@dataclass
class visualization_msgs__msg__InteractiveMarkerPose:
    """Class for visualization_msgs/msg/InteractiveMarkerPose."""

    header: std_msgs__msg__Header
    pose: geometry_msgs__msg__Pose
    name: str


FIELDDEFS = {
    'builtin_interfaces/msg/Time': [
        ('sec', [1, 'int32']),
        ('nanosec', [1, 'uint32']),
    ],
    'builtin_interfaces/msg/Duration': [
        ('sec', [1, 'int32']),
        ('nanosec', [1, 'uint32']),
    ],
    'diagnostic_msgs/msg/DiagnosticStatus': [
        ('level', [1, 'uint8']),
        ('name', [1, 'string']),
        ('message', [1, 'string']),
        ('hardware_id', [1, 'string']),
        ('values', [4, [2, 'diagnostic_msgs/msg/KeyValue']]),
    ],
    'diagnostic_msgs/msg/DiagnosticArray': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('status', [4, [2, 'diagnostic_msgs/msg/DiagnosticStatus']]),
    ],
    'diagnostic_msgs/msg/KeyValue': [
        ('key', [1, 'string']),
        ('value', [1, 'string']),
    ],
    'geometry_msgs/msg/AccelWithCovariance': [
        ('accel', [2, 'geometry_msgs/msg/Accel']),
        ('covariance', [3, 36, [1, 'float64']]),
    ],
    'geometry_msgs/msg/Point32': [
        ('x', [1, 'float32']),
        ('y', [1, 'float32']),
        ('z', [1, 'float32']),
    ],
    'geometry_msgs/msg/Vector3': [
        ('x', [1, 'float64']),
        ('y', [1, 'float64']),
        ('z', [1, 'float64']),
    ],
    'geometry_msgs/msg/Inertia': [
        ('m', [1, 'float64']),
        ('com', [2, 'geometry_msgs/msg/Vector3']),
        ('ixx', [1, 'float64']),
        ('ixy', [1, 'float64']),
        ('ixz', [1, 'float64']),
        ('iyy', [1, 'float64']),
        ('iyz', [1, 'float64']),
        ('izz', [1, 'float64']),
    ],
    'geometry_msgs/msg/PoseWithCovarianceStamped': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('pose', [2, 'geometry_msgs/msg/PoseWithCovariance']),
    ],
    'geometry_msgs/msg/Twist': [
        ('linear', [2, 'geometry_msgs/msg/Vector3']),
        ('angular', [2, 'geometry_msgs/msg/Vector3']),
    ],
    'geometry_msgs/msg/Pose': [
        ('position', [2, 'geometry_msgs/msg/Point']),
        ('orientation', [2, 'geometry_msgs/msg/Quaternion']),
    ],
    'geometry_msgs/msg/Point': [
        ('x', [1, 'float64']),
        ('y', [1, 'float64']),
        ('z', [1, 'float64']),
    ],
    'geometry_msgs/msg/Vector3Stamped': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('vector', [2, 'geometry_msgs/msg/Vector3']),
    ],
    'geometry_msgs/msg/Transform': [
        ('translation', [2, 'geometry_msgs/msg/Vector3']),
        ('rotation', [2, 'geometry_msgs/msg/Quaternion']),
    ],
    'geometry_msgs/msg/PolygonStamped': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('polygon', [2, 'geometry_msgs/msg/Polygon']),
    ],
    'geometry_msgs/msg/Quaternion': [
        ('x', [1, 'float64']),
        ('y', [1, 'float64']),
        ('z', [1, 'float64']),
        ('w', [1, 'float64']),
    ],
    'geometry_msgs/msg/Pose2D': [
        ('x', [1, 'float64']),
        ('y', [1, 'float64']),
        ('theta', [1, 'float64']),
    ],
    'geometry_msgs/msg/InertiaStamped': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('inertia', [2, 'geometry_msgs/msg/Inertia']),
    ],
    'geometry_msgs/msg/TwistStamped': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('twist', [2, 'geometry_msgs/msg/Twist']),
    ],
    'geometry_msgs/msg/PoseStamped': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('pose', [2, 'geometry_msgs/msg/Pose']),
    ],
    'geometry_msgs/msg/PointStamped': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('point', [2, 'geometry_msgs/msg/Point']),
    ],
    'geometry_msgs/msg/Polygon': [
        ('points', [4, [2, 'geometry_msgs/msg/Point32']]),
    ],
    'geometry_msgs/msg/PoseArray': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('poses', [4, [2, 'geometry_msgs/msg/Pose']]),
    ],
    'geometry_msgs/msg/AccelStamped': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('accel', [2, 'geometry_msgs/msg/Accel']),
    ],
    'geometry_msgs/msg/TwistWithCovarianceStamped': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('twist', [2, 'geometry_msgs/msg/TwistWithCovariance']),
    ],
    'geometry_msgs/msg/QuaternionStamped': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('quaternion', [2, 'geometry_msgs/msg/Quaternion']),
    ],
    'geometry_msgs/msg/WrenchStamped': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('wrench', [2, 'geometry_msgs/msg/Wrench']),
    ],
    'geometry_msgs/msg/AccelWithCovarianceStamped': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('accel', [2, 'geometry_msgs/msg/AccelWithCovariance']),
    ],
    'geometry_msgs/msg/PoseWithCovariance': [
        ('pose', [2, 'geometry_msgs/msg/Pose']),
        ('covariance', [3, 36, [1, 'float64']]),
    ],
    'geometry_msgs/msg/Wrench': [
        ('force', [2, 'geometry_msgs/msg/Vector3']),
        ('torque', [2, 'geometry_msgs/msg/Vector3']),
    ],
    'geometry_msgs/msg/TransformStamped': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('child_frame_id', [1, 'string']),
        ('transform', [2, 'geometry_msgs/msg/Transform']),
    ],
    'geometry_msgs/msg/Accel': [
        ('linear', [2, 'geometry_msgs/msg/Vector3']),
        ('angular', [2, 'geometry_msgs/msg/Vector3']),
    ],
    'geometry_msgs/msg/TwistWithCovariance': [
        ('twist', [2, 'geometry_msgs/msg/Twist']),
        ('covariance', [3, 36, [1, 'float64']]),
    ],
    'libstatistics_collector/msg/DummyMessage': [
        ('header', [2, 'std_msgs/msg/Header']),
    ],
    'lifecycle_msgs/msg/TransitionDescription': [
        ('transition', [2, 'lifecycle_msgs/msg/Transition']),
        ('start_state', [2, 'lifecycle_msgs/msg/State']),
        ('goal_state', [2, 'lifecycle_msgs/msg/State']),
    ],
    'lifecycle_msgs/msg/State': [
        ('id', [1, 'uint8']),
        ('label', [1, 'string']),
    ],
    'lifecycle_msgs/msg/TransitionEvent': [
        ('timestamp', [1, 'uint64']),
        ('transition', [2, 'lifecycle_msgs/msg/Transition']),
        ('start_state', [2, 'lifecycle_msgs/msg/State']),
        ('goal_state', [2, 'lifecycle_msgs/msg/State']),
    ],
    'lifecycle_msgs/msg/Transition': [
        ('id', [1, 'uint8']),
        ('label', [1, 'string']),
    ],
    'nav_msgs/msg/MapMetaData': [
        ('map_load_time', [2, 'builtin_interfaces/msg/Time']),
        ('resolution', [1, 'float32']),
        ('width', [1, 'uint32']),
        ('height', [1, 'uint32']),
        ('origin', [2, 'geometry_msgs/msg/Pose']),
    ],
    'nav_msgs/msg/GridCells': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('cell_width', [1, 'float32']),
        ('cell_height', [1, 'float32']),
        ('cells', [4, [2, 'geometry_msgs/msg/Point']]),
    ],
    'nav_msgs/msg/Odometry': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('child_frame_id', [1, 'string']),
        ('pose', [2, 'geometry_msgs/msg/PoseWithCovariance']),
        ('twist', [2, 'geometry_msgs/msg/TwistWithCovariance']),
    ],
    'nav_msgs/msg/Path': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('poses', [4, [2, 'geometry_msgs/msg/PoseStamped']]),
    ],
    'nav_msgs/msg/OccupancyGrid': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('info', [2, 'nav_msgs/msg/MapMetaData']),
        ('data', [4, [1, 'int8']]),
    ],
    'rcl_interfaces/msg/ListParametersResult': [
        ('names', [4, [1, 'string']]),
        ('prefixes', [4, [1, 'string']]),
    ],
    'rcl_interfaces/msg/ParameterType': [
        ('structure_needs_at_least_one_member', [1, 'uint8']),
    ],
    'rcl_interfaces/msg/ParameterEventDescriptors': [
        ('new_parameters', [4, [2, 'rcl_interfaces/msg/ParameterDescriptor']]),
        ('changed_parameters', [4, [2, 'rcl_interfaces/msg/ParameterDescriptor']]),
        ('deleted_parameters', [4, [2, 'rcl_interfaces/msg/ParameterDescriptor']]),
    ],
    'rcl_interfaces/msg/ParameterEvent': [
        ('stamp', [2, 'builtin_interfaces/msg/Time']),
        ('node', [1, 'string']),
        ('new_parameters', [4, [2, 'rcl_interfaces/msg/Parameter']]),
        ('changed_parameters', [4, [2, 'rcl_interfaces/msg/Parameter']]),
        ('deleted_parameters', [4, [2, 'rcl_interfaces/msg/Parameter']]),
    ],
    'rcl_interfaces/msg/IntegerRange': [
        ('from_value', [1, 'int64']),
        ('to_value', [1, 'int64']),
        ('step', [1, 'uint64']),
    ],
    'rcl_interfaces/msg/Parameter': [
        ('name', [1, 'string']),
        ('value', [2, 'rcl_interfaces/msg/ParameterValue']),
    ],
    'rcl_interfaces/msg/ParameterValue': [
        ('type', [1, 'uint8']),
        ('bool_value', [1, 'bool']),
        ('integer_value', [1, 'int64']),
        ('double_value', [1, 'float64']),
        ('string_value', [1, 'string']),
        ('byte_array_value', [4, [1, 'uint8']]),
        ('bool_array_value', [4, [1, 'bool']]),
        ('integer_array_value', [4, [1, 'int64']]),
        ('double_array_value', [4, [1, 'float64']]),
        ('string_array_value', [4, [1, 'string']]),
    ],
    'rcl_interfaces/msg/FloatingPointRange': [
        ('from_value', [1, 'float64']),
        ('to_value', [1, 'float64']),
        ('step', [1, 'float64']),
    ],
    'rcl_interfaces/msg/SetParametersResult': [
        ('successful', [1, 'bool']),
        ('reason', [1, 'string']),
    ],
    'rcl_interfaces/msg/Log': [
        ('stamp', [2, 'builtin_interfaces/msg/Time']),
        ('level', [1, 'uint8']),
        ('name', [1, 'string']),
        ('msg', [1, 'string']),
        ('file', [1, 'string']),
        ('function', [1, 'string']),
        ('line', [1, 'uint32']),
    ],
    'rcl_interfaces/msg/ParameterDescriptor': [
        ('name', [1, 'string']),
        ('type', [1, 'uint8']),
        ('description', [1, 'string']),
        ('additional_constraints', [1, 'string']),
        ('read_only', [1, 'bool']),
        ('floating_point_range', [4, [2, 'rcl_interfaces/msg/FloatingPointRange']]),
        ('integer_range', [4, [2, 'rcl_interfaces/msg/IntegerRange']]),
    ],
    'rmw_dds_common/msg/Gid': [
        ('data', [3, 24, [1, 'uint8']]),
    ],
    'rmw_dds_common/msg/NodeEntitiesInfo': [
        ('node_namespace', [1, 'string', [6, 256]]),
        ('node_name', [1, 'string', [6, 256]]),
        ('reader_gid_seq', [4, [2, 'rmw_dds_common/msg/Gid']]),
        ('writer_gid_seq', [4, [2, 'rmw_dds_common/msg/Gid']]),
    ],
    'rmw_dds_common/msg/ParticipantEntitiesInfo': [
        ('gid', [2, 'rmw_dds_common/msg/Gid']),
        ('node_entities_info_seq', [4, [2, 'rmw_dds_common/msg/NodeEntitiesInfo']]),
    ],
    'rosgraph_msgs/msg/Clock': [
        ('clock', [2, 'builtin_interfaces/msg/Time']),
    ],
    'sensor_msgs/msg/Temperature': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('temperature', [1, 'float64']),
        ('variance', [1, 'float64']),
    ],
    'sensor_msgs/msg/Range': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('radiation_type', [1, 'uint8']),
        ('field_of_view', [1, 'float32']),
        ('min_range', [1, 'float32']),
        ('max_range', [1, 'float32']),
        ('range', [1, 'float32']),
    ],
    'sensor_msgs/msg/RegionOfInterest': [
        ('x_offset', [1, 'uint32']),
        ('y_offset', [1, 'uint32']),
        ('height', [1, 'uint32']),
        ('width', [1, 'uint32']),
        ('do_rectify', [1, 'bool']),
    ],
    'sensor_msgs/msg/JoyFeedbackArray': [
        ('array', [4, [2, 'sensor_msgs/msg/JoyFeedback']]),
    ],
    'sensor_msgs/msg/TimeReference': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('time_ref', [2, 'builtin_interfaces/msg/Time']),
        ('source', [1, 'string']),
    ],
    'sensor_msgs/msg/CompressedImage': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('format', [1, 'string']),
        ('data', [4, [1, 'uint8']]),
    ],
    'sensor_msgs/msg/MultiEchoLaserScan': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('angle_min', [1, 'float32']),
        ('angle_max', [1, 'float32']),
        ('angle_increment', [1, 'float32']),
        ('time_increment', [1, 'float32']),
        ('scan_time', [1, 'float32']),
        ('range_min', [1, 'float32']),
        ('range_max', [1, 'float32']),
        ('ranges', [4, [2, 'sensor_msgs/msg/LaserEcho']]),
        ('intensities', [4, [2, 'sensor_msgs/msg/LaserEcho']]),
    ],
    'sensor_msgs/msg/LaserEcho': [
        ('echoes', [4, [1, 'float32']]),
    ],
    'sensor_msgs/msg/ChannelFloat32': [
        ('name', [1, 'string']),
        ('values', [4, [1, 'float32']]),
    ],
    'sensor_msgs/msg/CameraInfo': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('height', [1, 'uint32']),
        ('width', [1, 'uint32']),
        ('distortion_model', [1, 'string']),
        ('d', [4, [1, 'float64']]),
        ('k', [3, 9, [1, 'float64']]),
        ('r', [3, 9, [1, 'float64']]),
        ('p', [3, 12, [1, 'float64']]),
        ('binning_x', [1, 'uint32']),
        ('binning_y', [1, 'uint32']),
        ('roi', [2, 'sensor_msgs/msg/RegionOfInterest']),
    ],
    'sensor_msgs/msg/RelativeHumidity': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('relative_humidity', [1, 'float64']),
        ('variance', [1, 'float64']),
    ],
    'sensor_msgs/msg/FluidPressure': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('fluid_pressure', [1, 'float64']),
        ('variance', [1, 'float64']),
    ],
    'sensor_msgs/msg/LaserScan': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('angle_min', [1, 'float32']),
        ('angle_max', [1, 'float32']),
        ('angle_increment', [1, 'float32']),
        ('time_increment', [1, 'float32']),
        ('scan_time', [1, 'float32']),
        ('range_min', [1, 'float32']),
        ('range_max', [1, 'float32']),
        ('ranges', [4, [1, 'float32']]),
        ('intensities', [4, [1, 'float32']]),
    ],
    'sensor_msgs/msg/BatteryState': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('voltage', [1, 'float32']),
        ('temperature', [1, 'float32']),
        ('current', [1, 'float32']),
        ('charge', [1, 'float32']),
        ('capacity', [1, 'float32']),
        ('design_capacity', [1, 'float32']),
        ('percentage', [1, 'float32']),
        ('power_supply_status', [1, 'uint8']),
        ('power_supply_health', [1, 'uint8']),
        ('power_supply_technology', [1, 'uint8']),
        ('present', [1, 'bool']),
        ('cell_voltage', [4, [1, 'float32']]),
        ('cell_temperature', [4, [1, 'float32']]),
        ('location', [1, 'string']),
        ('serial_number', [1, 'string']),
    ],
    'sensor_msgs/msg/Image': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('height', [1, 'uint32']),
        ('width', [1, 'uint32']),
        ('encoding', [1, 'string']),
        ('is_bigendian', [1, 'uint8']),
        ('step', [1, 'uint32']),
        ('data', [4, [1, 'uint8']]),
    ],
    'sensor_msgs/msg/PointCloud': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('points', [4, [2, 'geometry_msgs/msg/Point32']]),
        ('channels', [4, [2, 'sensor_msgs/msg/ChannelFloat32']]),
    ],
    'sensor_msgs/msg/Imu': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('orientation', [2, 'geometry_msgs/msg/Quaternion']),
        ('orientation_covariance', [3, 9, [1, 'float64']]),
        ('angular_velocity', [2, 'geometry_msgs/msg/Vector3']),
        ('angular_velocity_covariance', [3, 9, [1, 'float64']]),
        ('linear_acceleration', [2, 'geometry_msgs/msg/Vector3']),
        ('linear_acceleration_covariance', [3, 9, [1, 'float64']]),
    ],
    'sensor_msgs/msg/NavSatStatus': [
        ('status', [1, 'int8']),
        ('service', [1, 'uint16']),
    ],
    'sensor_msgs/msg/Illuminance': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('illuminance', [1, 'float64']),
        ('variance', [1, 'float64']),
    ],
    'sensor_msgs/msg/Joy': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('axes', [4, [1, 'float32']]),
        ('buttons', [4, [1, 'int32']]),
    ],
    'sensor_msgs/msg/NavSatFix': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('status', [2, 'sensor_msgs/msg/NavSatStatus']),
        ('latitude', [1, 'float64']),
        ('longitude', [1, 'float64']),
        ('altitude', [1, 'float64']),
        ('position_covariance', [3, 9, [1, 'float64']]),
        ('position_covariance_type', [1, 'uint8']),
    ],
    'sensor_msgs/msg/MultiDOFJointState': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('joint_names', [4, [1, 'string']]),
        ('transforms', [4, [2, 'geometry_msgs/msg/Transform']]),
        ('twist', [4, [2, 'geometry_msgs/msg/Twist']]),
        ('wrench', [4, [2, 'geometry_msgs/msg/Wrench']]),
    ],
    'sensor_msgs/msg/MagneticField': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('magnetic_field', [2, 'geometry_msgs/msg/Vector3']),
        ('magnetic_field_covariance', [3, 9, [1, 'float64']]),
    ],
    'sensor_msgs/msg/JointState': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('name', [4, [1, 'string']]),
        ('position', [4, [1, 'float64']]),
        ('velocity', [4, [1, 'float64']]),
        ('effort', [4, [1, 'float64']]),
    ],
    'sensor_msgs/msg/PointField': [
        ('name', [1, 'string']),
        ('offset', [1, 'uint32']),
        ('datatype', [1, 'uint8']),
        ('count', [1, 'uint32']),
    ],
    'sensor_msgs/msg/PointCloud2': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('height', [1, 'uint32']),
        ('width', [1, 'uint32']),
        ('fields', [4, [2, 'sensor_msgs/msg/PointField']]),
        ('is_bigendian', [1, 'bool']),
        ('point_step', [1, 'uint32']),
        ('row_step', [1, 'uint32']),
        ('data', [4, [1, 'uint8']]),
        ('is_dense', [1, 'bool']),
    ],
    'sensor_msgs/msg/JoyFeedback': [
        ('type', [1, 'uint8']),
        ('id', [1, 'uint8']),
        ('intensity', [1, 'float32']),
    ],
    'shape_msgs/msg/SolidPrimitive': [
        ('type', [1, 'uint8']),
        ('dimensions', [4, [1, 'float64']]),
    ],
    'shape_msgs/msg/Mesh': [
        ('triangles', [4, [2, 'shape_msgs/msg/MeshTriangle']]),
        ('vertices', [4, [2, 'geometry_msgs/msg/Point']]),
    ],
    'shape_msgs/msg/Plane': [
        ('coef', [3, 4, [1, 'float64']]),
    ],
    'shape_msgs/msg/MeshTriangle': [
        ('vertex_indices', [3, 3, [1, 'uint32']]),
    ],
    'statistics_msgs/msg/StatisticDataType': [
        ('structure_needs_at_least_one_member', [1, 'uint8']),
    ],
    'statistics_msgs/msg/StatisticDataPoint': [
        ('data_type', [1, 'uint8']),
        ('data', [1, 'float64']),
    ],
    'statistics_msgs/msg/MetricsMessage': [
        ('measurement_source_name', [1, 'string']),
        ('metrics_source', [1, 'string']),
        ('unit', [1, 'string']),
        ('window_start', [2, 'builtin_interfaces/msg/Time']),
        ('window_stop', [2, 'builtin_interfaces/msg/Time']),
        ('statistics', [4, [2, 'statistics_msgs/msg/StatisticDataPoint']]),
    ],
    'std_msgs/msg/UInt8': [
        ('data', [1, 'uint8']),
    ],
    'std_msgs/msg/Float32MultiArray': [
        ('layout', [2, 'std_msgs/msg/MultiArrayLayout']),
        ('data', [4, [1, 'float32']]),
    ],
    'std_msgs/msg/Int8': [
        ('data', [1, 'int8']),
    ],
    'std_msgs/msg/Empty': [
        ('structure_needs_at_least_one_member', [1, 'uint8']),
    ],
    'std_msgs/msg/String': [
        ('data', [1, 'string']),
    ],
    'std_msgs/msg/MultiArrayDimension': [
        ('label', [1, 'string']),
        ('size', [1, 'uint32']),
        ('stride', [1, 'uint32']),
    ],
    'std_msgs/msg/UInt64': [
        ('data', [1, 'uint64']),
    ],
    'std_msgs/msg/UInt16': [
        ('data', [1, 'uint16']),
    ],
    'std_msgs/msg/Float32': [
        ('data', [1, 'float32']),
    ],
    'std_msgs/msg/Int64': [
        ('data', [1, 'int64']),
    ],
    'std_msgs/msg/Int16MultiArray': [
        ('layout', [2, 'std_msgs/msg/MultiArrayLayout']),
        ('data', [4, [1, 'int16']]),
    ],
    'std_msgs/msg/Int16': [
        ('data', [1, 'int16']),
    ],
    'std_msgs/msg/Float64MultiArray': [
        ('layout', [2, 'std_msgs/msg/MultiArrayLayout']),
        ('data', [4, [1, 'float64']]),
    ],
    'std_msgs/msg/MultiArrayLayout': [
        ('dim', [4, [2, 'std_msgs/msg/MultiArrayDimension']]),
        ('data_offset', [1, 'uint32']),
    ],
    'std_msgs/msg/UInt32MultiArray': [
        ('layout', [2, 'std_msgs/msg/MultiArrayLayout']),
        ('data', [4, [1, 'uint32']]),
    ],
    'std_msgs/msg/Header': [
        ('stamp', [2, 'builtin_interfaces/msg/Time']),
        ('frame_id', [1, 'string']),
    ],
    'std_msgs/msg/ByteMultiArray': [
        ('layout', [2, 'std_msgs/msg/MultiArrayLayout']),
        ('data', [4, [1, 'uint8']]),
    ],
    'std_msgs/msg/Int8MultiArray': [
        ('layout', [2, 'std_msgs/msg/MultiArrayLayout']),
        ('data', [4, [1, 'int8']]),
    ],
    'std_msgs/msg/Float64': [
        ('data', [1, 'float64']),
    ],
    'std_msgs/msg/UInt8MultiArray': [
        ('layout', [2, 'std_msgs/msg/MultiArrayLayout']),
        ('data', [4, [1, 'uint8']]),
    ],
    'std_msgs/msg/Byte': [
        ('data', [1, 'uint8']),
    ],
    'std_msgs/msg/Char': [
        ('data', [1, 'uint8']),
    ],
    'std_msgs/msg/UInt64MultiArray': [
        ('layout', [2, 'std_msgs/msg/MultiArrayLayout']),
        ('data', [4, [1, 'uint64']]),
    ],
    'std_msgs/msg/Int32MultiArray': [
        ('layout', [2, 'std_msgs/msg/MultiArrayLayout']),
        ('data', [4, [1, 'int32']]),
    ],
    'std_msgs/msg/ColorRGBA': [
        ('r', [1, 'float32']),
        ('g', [1, 'float32']),
        ('b', [1, 'float32']),
        ('a', [1, 'float32']),
    ],
    'std_msgs/msg/Bool': [
        ('data', [1, 'bool']),
    ],
    'std_msgs/msg/UInt32': [
        ('data', [1, 'uint32']),
    ],
    'std_msgs/msg/Int64MultiArray': [
        ('layout', [2, 'std_msgs/msg/MultiArrayLayout']),
        ('data', [4, [1, 'int64']]),
    ],
    'std_msgs/msg/Int32': [
        ('data', [1, 'int32']),
    ],
    'std_msgs/msg/UInt16MultiArray': [
        ('layout', [2, 'std_msgs/msg/MultiArrayLayout']),
        ('data', [4, [1, 'uint16']]),
    ],
    'stereo_msgs/msg/DisparityImage': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('image', [2, 'sensor_msgs/msg/Image']),
        ('f', [1, 'float32']),
        ('t', [1, 'float32']),
        ('valid_window', [2, 'sensor_msgs/msg/RegionOfInterest']),
        ('min_disparity', [1, 'float32']),
        ('max_disparity', [1, 'float32']),
        ('delta_d', [1, 'float32']),
    ],
    'tf2_msgs/msg/TF2Error': [
        ('error', [1, 'uint8']),
        ('error_string', [1, 'string']),
    ],
    'tf2_msgs/msg/TFMessage': [
        ('transforms', [4, [2, 'geometry_msgs/msg/TransformStamped']]),
    ],
    'trajectory_msgs/msg/MultiDOFJointTrajectory': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('joint_names', [4, [1, 'string']]),
        ('points', [4, [2, 'trajectory_msgs/msg/MultiDOFJointTrajectoryPoint']]),
    ],
    'trajectory_msgs/msg/JointTrajectory': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('joint_names', [4, [1, 'string']]),
        ('points', [4, [2, 'trajectory_msgs/msg/JointTrajectoryPoint']]),
    ],
    'trajectory_msgs/msg/JointTrajectoryPoint': [
        ('positions', [4, [1, 'float64']]),
        ('velocities', [4, [1, 'float64']]),
        ('accelerations', [4, [1, 'float64']]),
        ('effort', [4, [1, 'float64']]),
        ('time_from_start', [2, 'builtin_interfaces/msg/Duration']),
    ],
    'trajectory_msgs/msg/MultiDOFJointTrajectoryPoint': [
        ('transforms', [4, [2, 'geometry_msgs/msg/Transform']]),
        ('velocities', [4, [2, 'geometry_msgs/msg/Twist']]),
        ('accelerations', [4, [2, 'geometry_msgs/msg/Twist']]),
        ('time_from_start', [2, 'builtin_interfaces/msg/Duration']),
    ],
    'unique_identifier_msgs/msg/UUID': [
        ('uuid', [3, 16, [1, 'uint8']]),
    ],
    'visualization_msgs/msg/Marker': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('ns', [1, 'string']),
        ('id', [1, 'int32']),
        ('type', [1, 'int32']),
        ('action', [1, 'int32']),
        ('pose', [2, 'geometry_msgs/msg/Pose']),
        ('scale', [2, 'geometry_msgs/msg/Vector3']),
        ('color', [2, 'std_msgs/msg/ColorRGBA']),
        ('lifetime', [2, 'builtin_interfaces/msg/Duration']),
        ('frame_locked', [1, 'bool']),
        ('points', [4, [2, 'geometry_msgs/msg/Point']]),
        ('colors', [4, [2, 'std_msgs/msg/ColorRGBA']]),
        ('text', [1, 'string']),
        ('mesh_resource', [1, 'string']),
        ('mesh_use_embedded_materials', [1, 'bool']),
    ],
    'visualization_msgs/msg/InteractiveMarkerInit': [
        ('server_id', [1, 'string']),
        ('seq_num', [1, 'uint64']),
        ('markers', [4, [2, 'visualization_msgs/msg/InteractiveMarker']]),
    ],
    'visualization_msgs/msg/MenuEntry': [
        ('id', [1, 'uint32']),
        ('parent_id', [1, 'uint32']),
        ('title', [1, 'string']),
        ('command', [1, 'string']),
        ('command_type', [1, 'uint8']),
    ],
    'visualization_msgs/msg/MarkerArray': [
        ('markers', [4, [2, 'visualization_msgs/msg/Marker']]),
    ],
    'visualization_msgs/msg/InteractiveMarkerUpdate': [
        ('server_id', [1, 'string']),
        ('seq_num', [1, 'uint64']),
        ('type', [1, 'uint8']),
        ('markers', [4, [2, 'visualization_msgs/msg/InteractiveMarker']]),
        ('poses', [4, [2, 'visualization_msgs/msg/InteractiveMarkerPose']]),
        ('erases', [4, [1, 'string']]),
    ],
    'visualization_msgs/msg/InteractiveMarker': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('pose', [2, 'geometry_msgs/msg/Pose']),
        ('name', [1, 'string']),
        ('description', [1, 'string']),
        ('scale', [1, 'float32']),
        ('menu_entries', [4, [2, 'visualization_msgs/msg/MenuEntry']]),
        ('controls', [4, [2, 'visualization_msgs/msg/InteractiveMarkerControl']]),
    ],
    'visualization_msgs/msg/InteractiveMarkerFeedback': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('client_id', [1, 'string']),
        ('marker_name', [1, 'string']),
        ('control_name', [1, 'string']),
        ('event_type', [1, 'uint8']),
        ('pose', [2, 'geometry_msgs/msg/Pose']),
        ('menu_entry_id', [1, 'uint32']),
        ('mouse_point', [2, 'geometry_msgs/msg/Point']),
        ('mouse_point_valid', [1, 'bool']),
    ],
    'visualization_msgs/msg/ImageMarker': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('ns', [1, 'string']),
        ('id', [1, 'int32']),
        ('type', [1, 'int32']),
        ('action', [1, 'int32']),
        ('position', [2, 'geometry_msgs/msg/Point']),
        ('scale', [1, 'float32']),
        ('outline_color', [2, 'std_msgs/msg/ColorRGBA']),
        ('filled', [1, 'uint8']),
        ('fill_color', [2, 'std_msgs/msg/ColorRGBA']),
        ('lifetime', [2, 'builtin_interfaces/msg/Duration']),
        ('points', [4, [2, 'geometry_msgs/msg/Point']]),
        ('outline_colors', [4, [2, 'std_msgs/msg/ColorRGBA']]),
    ],
    'visualization_msgs/msg/InteractiveMarkerControl': [
        ('name', [1, 'string']),
        ('orientation', [2, 'geometry_msgs/msg/Quaternion']),
        ('orientation_mode', [1, 'uint8']),
        ('interaction_mode', [1, 'uint8']),
        ('always_visible', [1, 'bool']),
        ('markers', [4, [2, 'visualization_msgs/msg/Marker']]),
        ('independent_marker_orientation', [1, 'bool']),
        ('description', [1, 'string']),
    ],
    'visualization_msgs/msg/InteractiveMarkerPose': [
        ('header', [2, 'std_msgs/msg/Header']),
        ('pose', [2, 'geometry_msgs/msg/Pose']),
        ('name', [1, 'string']),
    ],
}
