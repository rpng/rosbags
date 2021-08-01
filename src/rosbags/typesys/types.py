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
    from typing import Any, ClassVar

    import numpy

    from .base import Typesdict

@dataclass
class builtin_interfaces__msg__Time:
    """Class for builtin_interfaces/msg/Time."""

    sec: int
    nanosec: int
    __msgtype__: ClassVar[str] = 'builtin_interfaces/msg/Time'


@dataclass
class builtin_interfaces__msg__Duration:
    """Class for builtin_interfaces/msg/Duration."""

    sec: int
    nanosec: int
    __msgtype__: ClassVar[str] = 'builtin_interfaces/msg/Duration'


@dataclass
class diagnostic_msgs__msg__DiagnosticStatus:
    """Class for diagnostic_msgs/msg/DiagnosticStatus."""

    level: int
    name: str
    message: str
    hardware_id: str
    values: list[diagnostic_msgs__msg__KeyValue]
    OK: ClassVar[int] = 0
    WARN: ClassVar[int] = 1
    ERROR: ClassVar[int] = 2
    STALE: ClassVar[int] = 3
    __msgtype__: ClassVar[str] = 'diagnostic_msgs/msg/DiagnosticStatus'


@dataclass
class diagnostic_msgs__msg__DiagnosticArray:
    """Class for diagnostic_msgs/msg/DiagnosticArray."""

    header: std_msgs__msg__Header
    status: list[diagnostic_msgs__msg__DiagnosticStatus]
    __msgtype__: ClassVar[str] = 'diagnostic_msgs/msg/DiagnosticArray'


@dataclass
class diagnostic_msgs__msg__KeyValue:
    """Class for diagnostic_msgs/msg/KeyValue."""

    key: str
    value: str
    __msgtype__: ClassVar[str] = 'diagnostic_msgs/msg/KeyValue'


@dataclass
class geometry_msgs__msg__AccelWithCovariance:
    """Class for geometry_msgs/msg/AccelWithCovariance."""

    accel: geometry_msgs__msg__Accel
    covariance: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/AccelWithCovariance'


@dataclass
class geometry_msgs__msg__Point32:
    """Class for geometry_msgs/msg/Point32."""

    x: float
    y: float
    z: float
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/Point32'


@dataclass
class geometry_msgs__msg__Vector3:
    """Class for geometry_msgs/msg/Vector3."""

    x: float
    y: float
    z: float
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/Vector3'


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
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/Inertia'


@dataclass
class geometry_msgs__msg__PoseWithCovarianceStamped:
    """Class for geometry_msgs/msg/PoseWithCovarianceStamped."""

    header: std_msgs__msg__Header
    pose: geometry_msgs__msg__PoseWithCovariance
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/PoseWithCovarianceStamped'


@dataclass
class geometry_msgs__msg__Twist:
    """Class for geometry_msgs/msg/Twist."""

    linear: geometry_msgs__msg__Vector3
    angular: geometry_msgs__msg__Vector3
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/Twist'


@dataclass
class geometry_msgs__msg__Pose:
    """Class for geometry_msgs/msg/Pose."""

    position: geometry_msgs__msg__Point
    orientation: geometry_msgs__msg__Quaternion
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/Pose'


@dataclass
class geometry_msgs__msg__Point:
    """Class for geometry_msgs/msg/Point."""

    x: float
    y: float
    z: float
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/Point'


@dataclass
class geometry_msgs__msg__Vector3Stamped:
    """Class for geometry_msgs/msg/Vector3Stamped."""

    header: std_msgs__msg__Header
    vector: geometry_msgs__msg__Vector3
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/Vector3Stamped'


@dataclass
class geometry_msgs__msg__Transform:
    """Class for geometry_msgs/msg/Transform."""

    translation: geometry_msgs__msg__Vector3
    rotation: geometry_msgs__msg__Quaternion
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/Transform'


@dataclass
class geometry_msgs__msg__PolygonStamped:
    """Class for geometry_msgs/msg/PolygonStamped."""

    header: std_msgs__msg__Header
    polygon: geometry_msgs__msg__Polygon
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/PolygonStamped'


@dataclass
class geometry_msgs__msg__Quaternion:
    """Class for geometry_msgs/msg/Quaternion."""

    x: float
    y: float
    z: float
    w: float
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/Quaternion'


@dataclass
class geometry_msgs__msg__Pose2D:
    """Class for geometry_msgs/msg/Pose2D."""

    x: float
    y: float
    theta: float
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/Pose2D'


@dataclass
class geometry_msgs__msg__InertiaStamped:
    """Class for geometry_msgs/msg/InertiaStamped."""

    header: std_msgs__msg__Header
    inertia: geometry_msgs__msg__Inertia
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/InertiaStamped'


@dataclass
class geometry_msgs__msg__TwistStamped:
    """Class for geometry_msgs/msg/TwistStamped."""

    header: std_msgs__msg__Header
    twist: geometry_msgs__msg__Twist
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/TwistStamped'


@dataclass
class geometry_msgs__msg__PoseStamped:
    """Class for geometry_msgs/msg/PoseStamped."""

    header: std_msgs__msg__Header
    pose: geometry_msgs__msg__Pose
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/PoseStamped'


@dataclass
class geometry_msgs__msg__PointStamped:
    """Class for geometry_msgs/msg/PointStamped."""

    header: std_msgs__msg__Header
    point: geometry_msgs__msg__Point
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/PointStamped'


@dataclass
class geometry_msgs__msg__Polygon:
    """Class for geometry_msgs/msg/Polygon."""

    points: list[geometry_msgs__msg__Point32]
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/Polygon'


@dataclass
class geometry_msgs__msg__PoseArray:
    """Class for geometry_msgs/msg/PoseArray."""

    header: std_msgs__msg__Header
    poses: list[geometry_msgs__msg__Pose]
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/PoseArray'


@dataclass
class geometry_msgs__msg__AccelStamped:
    """Class for geometry_msgs/msg/AccelStamped."""

    header: std_msgs__msg__Header
    accel: geometry_msgs__msg__Accel
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/AccelStamped'


@dataclass
class geometry_msgs__msg__TwistWithCovarianceStamped:
    """Class for geometry_msgs/msg/TwistWithCovarianceStamped."""

    header: std_msgs__msg__Header
    twist: geometry_msgs__msg__TwistWithCovariance
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/TwistWithCovarianceStamped'


@dataclass
class geometry_msgs__msg__QuaternionStamped:
    """Class for geometry_msgs/msg/QuaternionStamped."""

    header: std_msgs__msg__Header
    quaternion: geometry_msgs__msg__Quaternion
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/QuaternionStamped'


@dataclass
class geometry_msgs__msg__WrenchStamped:
    """Class for geometry_msgs/msg/WrenchStamped."""

    header: std_msgs__msg__Header
    wrench: geometry_msgs__msg__Wrench
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/WrenchStamped'


@dataclass
class geometry_msgs__msg__AccelWithCovarianceStamped:
    """Class for geometry_msgs/msg/AccelWithCovarianceStamped."""

    header: std_msgs__msg__Header
    accel: geometry_msgs__msg__AccelWithCovariance
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/AccelWithCovarianceStamped'


@dataclass
class geometry_msgs__msg__PoseWithCovariance:
    """Class for geometry_msgs/msg/PoseWithCovariance."""

    pose: geometry_msgs__msg__Pose
    covariance: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/PoseWithCovariance'


@dataclass
class geometry_msgs__msg__Wrench:
    """Class for geometry_msgs/msg/Wrench."""

    force: geometry_msgs__msg__Vector3
    torque: geometry_msgs__msg__Vector3
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/Wrench'


@dataclass
class geometry_msgs__msg__TransformStamped:
    """Class for geometry_msgs/msg/TransformStamped."""

    header: std_msgs__msg__Header
    child_frame_id: str
    transform: geometry_msgs__msg__Transform
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/TransformStamped'


@dataclass
class geometry_msgs__msg__Accel:
    """Class for geometry_msgs/msg/Accel."""

    linear: geometry_msgs__msg__Vector3
    angular: geometry_msgs__msg__Vector3
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/Accel'


@dataclass
class geometry_msgs__msg__TwistWithCovariance:
    """Class for geometry_msgs/msg/TwistWithCovariance."""

    twist: geometry_msgs__msg__Twist
    covariance: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    __msgtype__: ClassVar[str] = 'geometry_msgs/msg/TwistWithCovariance'


@dataclass
class libstatistics_collector__msg__DummyMessage:
    """Class for libstatistics_collector/msg/DummyMessage."""

    header: std_msgs__msg__Header
    __msgtype__: ClassVar[str] = 'libstatistics_collector/msg/DummyMessage'


@dataclass
class lifecycle_msgs__msg__TransitionDescription:
    """Class for lifecycle_msgs/msg/TransitionDescription."""

    transition: lifecycle_msgs__msg__Transition
    start_state: lifecycle_msgs__msg__State
    goal_state: lifecycle_msgs__msg__State
    __msgtype__: ClassVar[str] = 'lifecycle_msgs/msg/TransitionDescription'


@dataclass
class lifecycle_msgs__msg__State:
    """Class for lifecycle_msgs/msg/State."""

    id: int
    label: str
    PRIMARY_STATE_UNKNOWN: ClassVar[int] = 0
    PRIMARY_STATE_UNCONFIGURED: ClassVar[int] = 1
    PRIMARY_STATE_INACTIVE: ClassVar[int] = 2
    PRIMARY_STATE_ACTIVE: ClassVar[int] = 3
    PRIMARY_STATE_FINALIZED: ClassVar[int] = 4
    TRANSITION_STATE_CONFIGURING: ClassVar[int] = 10
    TRANSITION_STATE_CLEANINGUP: ClassVar[int] = 11
    TRANSITION_STATE_SHUTTINGDOWN: ClassVar[int] = 12
    TRANSITION_STATE_ACTIVATING: ClassVar[int] = 13
    TRANSITION_STATE_DEACTIVATING: ClassVar[int] = 14
    TRANSITION_STATE_ERRORPROCESSING: ClassVar[int] = 15
    __msgtype__: ClassVar[str] = 'lifecycle_msgs/msg/State'


@dataclass
class lifecycle_msgs__msg__TransitionEvent:
    """Class for lifecycle_msgs/msg/TransitionEvent."""

    timestamp: int
    transition: lifecycle_msgs__msg__Transition
    start_state: lifecycle_msgs__msg__State
    goal_state: lifecycle_msgs__msg__State
    __msgtype__: ClassVar[str] = 'lifecycle_msgs/msg/TransitionEvent'


@dataclass
class lifecycle_msgs__msg__Transition:
    """Class for lifecycle_msgs/msg/Transition."""

    id: int
    label: str
    TRANSITION_CREATE: ClassVar[int] = 0
    TRANSITION_CONFIGURE: ClassVar[int] = 1
    TRANSITION_CLEANUP: ClassVar[int] = 2
    TRANSITION_ACTIVATE: ClassVar[int] = 3
    TRANSITION_DEACTIVATE: ClassVar[int] = 4
    TRANSITION_UNCONFIGURED_SHUTDOWN: ClassVar[int] = 5
    TRANSITION_INACTIVE_SHUTDOWN: ClassVar[int] = 6
    TRANSITION_ACTIVE_SHUTDOWN: ClassVar[int] = 7
    TRANSITION_DESTROY: ClassVar[int] = 8
    TRANSITION_ON_CONFIGURE_SUCCESS: ClassVar[int] = 10
    TRANSITION_ON_CONFIGURE_FAILURE: ClassVar[int] = 11
    TRANSITION_ON_CONFIGURE_ERROR: ClassVar[int] = 12
    TRANSITION_ON_CLEANUP_SUCCESS: ClassVar[int] = 20
    TRANSITION_ON_CLEANUP_FAILURE: ClassVar[int] = 21
    TRANSITION_ON_CLEANUP_ERROR: ClassVar[int] = 22
    TRANSITION_ON_ACTIVATE_SUCCESS: ClassVar[int] = 30
    TRANSITION_ON_ACTIVATE_FAILURE: ClassVar[int] = 31
    TRANSITION_ON_ACTIVATE_ERROR: ClassVar[int] = 32
    TRANSITION_ON_DEACTIVATE_SUCCESS: ClassVar[int] = 40
    TRANSITION_ON_DEACTIVATE_FAILURE: ClassVar[int] = 41
    TRANSITION_ON_DEACTIVATE_ERROR: ClassVar[int] = 42
    TRANSITION_ON_SHUTDOWN_SUCCESS: ClassVar[int] = 50
    TRANSITION_ON_SHUTDOWN_FAILURE: ClassVar[int] = 51
    TRANSITION_ON_SHUTDOWN_ERROR: ClassVar[int] = 52
    TRANSITION_ON_ERROR_SUCCESS: ClassVar[int] = 60
    TRANSITION_ON_ERROR_FAILURE: ClassVar[int] = 61
    TRANSITION_ON_ERROR_ERROR: ClassVar[int] = 62
    TRANSITION_CALLBACK_SUCCESS: ClassVar[int] = 97
    TRANSITION_CALLBACK_FAILURE: ClassVar[int] = 98
    TRANSITION_CALLBACK_ERROR: ClassVar[int] = 99
    __msgtype__: ClassVar[str] = 'lifecycle_msgs/msg/Transition'


@dataclass
class nav_msgs__msg__MapMetaData:
    """Class for nav_msgs/msg/MapMetaData."""

    map_load_time: builtin_interfaces__msg__Time
    resolution: float
    width: int
    height: int
    origin: geometry_msgs__msg__Pose
    __msgtype__: ClassVar[str] = 'nav_msgs/msg/MapMetaData'


@dataclass
class nav_msgs__msg__GridCells:
    """Class for nav_msgs/msg/GridCells."""

    header: std_msgs__msg__Header
    cell_width: float
    cell_height: float
    cells: list[geometry_msgs__msg__Point]
    __msgtype__: ClassVar[str] = 'nav_msgs/msg/GridCells'


@dataclass
class nav_msgs__msg__Odometry:
    """Class for nav_msgs/msg/Odometry."""

    header: std_msgs__msg__Header
    child_frame_id: str
    pose: geometry_msgs__msg__PoseWithCovariance
    twist: geometry_msgs__msg__TwistWithCovariance
    __msgtype__: ClassVar[str] = 'nav_msgs/msg/Odometry'


@dataclass
class nav_msgs__msg__Path:
    """Class for nav_msgs/msg/Path."""

    header: std_msgs__msg__Header
    poses: list[geometry_msgs__msg__PoseStamped]
    __msgtype__: ClassVar[str] = 'nav_msgs/msg/Path'


@dataclass
class nav_msgs__msg__OccupancyGrid:
    """Class for nav_msgs/msg/OccupancyGrid."""

    header: std_msgs__msg__Header
    info: nav_msgs__msg__MapMetaData
    data: numpy.ndarray[Any, numpy.dtype[numpy.int8]]
    __msgtype__: ClassVar[str] = 'nav_msgs/msg/OccupancyGrid'


@dataclass
class rcl_interfaces__msg__ListParametersResult:
    """Class for rcl_interfaces/msg/ListParametersResult."""

    names: list[str]
    prefixes: list[str]
    __msgtype__: ClassVar[str] = 'rcl_interfaces/msg/ListParametersResult'


@dataclass
class rcl_interfaces__msg__ParameterType:
    """Class for rcl_interfaces/msg/ParameterType."""

    structure_needs_at_least_one_member: int
    PARAMETER_NOT_SET: ClassVar[int] = 0
    PARAMETER_BOOL: ClassVar[int] = 1
    PARAMETER_INTEGER: ClassVar[int] = 2
    PARAMETER_DOUBLE: ClassVar[int] = 3
    PARAMETER_STRING: ClassVar[int] = 4
    PARAMETER_BYTE_ARRAY: ClassVar[int] = 5
    PARAMETER_BOOL_ARRAY: ClassVar[int] = 6
    PARAMETER_INTEGER_ARRAY: ClassVar[int] = 7
    PARAMETER_DOUBLE_ARRAY: ClassVar[int] = 8
    PARAMETER_STRING_ARRAY: ClassVar[int] = 9
    __msgtype__: ClassVar[str] = 'rcl_interfaces/msg/ParameterType'


@dataclass
class rcl_interfaces__msg__ParameterEventDescriptors:
    """Class for rcl_interfaces/msg/ParameterEventDescriptors."""

    new_parameters: list[rcl_interfaces__msg__ParameterDescriptor]
    changed_parameters: list[rcl_interfaces__msg__ParameterDescriptor]
    deleted_parameters: list[rcl_interfaces__msg__ParameterDescriptor]
    __msgtype__: ClassVar[str] = 'rcl_interfaces/msg/ParameterEventDescriptors'


@dataclass
class rcl_interfaces__msg__ParameterEvent:
    """Class for rcl_interfaces/msg/ParameterEvent."""

    stamp: builtin_interfaces__msg__Time
    node: str
    new_parameters: list[rcl_interfaces__msg__Parameter]
    changed_parameters: list[rcl_interfaces__msg__Parameter]
    deleted_parameters: list[rcl_interfaces__msg__Parameter]
    __msgtype__: ClassVar[str] = 'rcl_interfaces/msg/ParameterEvent'


@dataclass
class rcl_interfaces__msg__IntegerRange:
    """Class for rcl_interfaces/msg/IntegerRange."""

    from_value: int
    to_value: int
    step: int
    __msgtype__: ClassVar[str] = 'rcl_interfaces/msg/IntegerRange'


@dataclass
class rcl_interfaces__msg__Parameter:
    """Class for rcl_interfaces/msg/Parameter."""

    name: str
    value: rcl_interfaces__msg__ParameterValue
    __msgtype__: ClassVar[str] = 'rcl_interfaces/msg/Parameter'


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
    __msgtype__: ClassVar[str] = 'rcl_interfaces/msg/ParameterValue'


@dataclass
class rcl_interfaces__msg__FloatingPointRange:
    """Class for rcl_interfaces/msg/FloatingPointRange."""

    from_value: float
    to_value: float
    step: float
    __msgtype__: ClassVar[str] = 'rcl_interfaces/msg/FloatingPointRange'


@dataclass
class rcl_interfaces__msg__SetParametersResult:
    """Class for rcl_interfaces/msg/SetParametersResult."""

    successful: bool
    reason: str
    __msgtype__: ClassVar[str] = 'rcl_interfaces/msg/SetParametersResult'


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
    DEBUG: ClassVar[int] = 10
    INFO: ClassVar[int] = 20
    WARN: ClassVar[int] = 30
    ERROR: ClassVar[int] = 40
    FATAL: ClassVar[int] = 50
    __msgtype__: ClassVar[str] = 'rcl_interfaces/msg/Log'


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
    __msgtype__: ClassVar[str] = 'rcl_interfaces/msg/ParameterDescriptor'


@dataclass
class rmw_dds_common__msg__Gid:
    """Class for rmw_dds_common/msg/Gid."""

    data: numpy.ndarray[Any, numpy.dtype[numpy.uint8]]
    __msgtype__: ClassVar[str] = 'rmw_dds_common/msg/Gid'


@dataclass
class rmw_dds_common__msg__NodeEntitiesInfo:
    """Class for rmw_dds_common/msg/NodeEntitiesInfo."""

    node_namespace: str
    node_name: str
    reader_gid_seq: list[rmw_dds_common__msg__Gid]
    writer_gid_seq: list[rmw_dds_common__msg__Gid]
    __msgtype__: ClassVar[str] = 'rmw_dds_common/msg/NodeEntitiesInfo'


@dataclass
class rmw_dds_common__msg__ParticipantEntitiesInfo:
    """Class for rmw_dds_common/msg/ParticipantEntitiesInfo."""

    gid: rmw_dds_common__msg__Gid
    node_entities_info_seq: list[rmw_dds_common__msg__NodeEntitiesInfo]
    __msgtype__: ClassVar[str] = 'rmw_dds_common/msg/ParticipantEntitiesInfo'


@dataclass
class rosgraph_msgs__msg__Clock:
    """Class for rosgraph_msgs/msg/Clock."""

    clock: builtin_interfaces__msg__Time
    __msgtype__: ClassVar[str] = 'rosgraph_msgs/msg/Clock'


@dataclass
class sensor_msgs__msg__Temperature:
    """Class for sensor_msgs/msg/Temperature."""

    header: std_msgs__msg__Header
    temperature: float
    variance: float
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/Temperature'


@dataclass
class sensor_msgs__msg__Range:
    """Class for sensor_msgs/msg/Range."""

    header: std_msgs__msg__Header
    radiation_type: int
    field_of_view: float
    min_range: float
    max_range: float
    range: float
    ULTRASOUND: ClassVar[int] = 0
    INFRARED: ClassVar[int] = 1
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/Range'


@dataclass
class sensor_msgs__msg__RegionOfInterest:
    """Class for sensor_msgs/msg/RegionOfInterest."""

    x_offset: int
    y_offset: int
    height: int
    width: int
    do_rectify: bool
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/RegionOfInterest'


@dataclass
class sensor_msgs__msg__JoyFeedbackArray:
    """Class for sensor_msgs/msg/JoyFeedbackArray."""

    array: list[sensor_msgs__msg__JoyFeedback]
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/JoyFeedbackArray'


@dataclass
class sensor_msgs__msg__TimeReference:
    """Class for sensor_msgs/msg/TimeReference."""

    header: std_msgs__msg__Header
    time_ref: builtin_interfaces__msg__Time
    source: str
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/TimeReference'


@dataclass
class sensor_msgs__msg__CompressedImage:
    """Class for sensor_msgs/msg/CompressedImage."""

    header: std_msgs__msg__Header
    format: str
    data: numpy.ndarray[Any, numpy.dtype[numpy.uint8]]
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/CompressedImage'


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
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/MultiEchoLaserScan'


@dataclass
class sensor_msgs__msg__LaserEcho:
    """Class for sensor_msgs/msg/LaserEcho."""

    echoes: numpy.ndarray[Any, numpy.dtype[numpy.float32]]
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/LaserEcho'


@dataclass
class sensor_msgs__msg__ChannelFloat32:
    """Class for sensor_msgs/msg/ChannelFloat32."""

    name: str
    values: numpy.ndarray[Any, numpy.dtype[numpy.float32]]
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/ChannelFloat32'


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
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/CameraInfo'


@dataclass
class sensor_msgs__msg__RelativeHumidity:
    """Class for sensor_msgs/msg/RelativeHumidity."""

    header: std_msgs__msg__Header
    relative_humidity: float
    variance: float
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/RelativeHumidity'


@dataclass
class sensor_msgs__msg__FluidPressure:
    """Class for sensor_msgs/msg/FluidPressure."""

    header: std_msgs__msg__Header
    fluid_pressure: float
    variance: float
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/FluidPressure'


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
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/LaserScan'


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
    POWER_SUPPLY_STATUS_UNKNOWN: ClassVar[int] = 0
    POWER_SUPPLY_STATUS_CHARGING: ClassVar[int] = 1
    POWER_SUPPLY_STATUS_DISCHARGING: ClassVar[int] = 2
    POWER_SUPPLY_STATUS_NOT_CHARGING: ClassVar[int] = 3
    POWER_SUPPLY_STATUS_FULL: ClassVar[int] = 4
    POWER_SUPPLY_HEALTH_UNKNOWN: ClassVar[int] = 0
    POWER_SUPPLY_HEALTH_GOOD: ClassVar[int] = 1
    POWER_SUPPLY_HEALTH_OVERHEAT: ClassVar[int] = 2
    POWER_SUPPLY_HEALTH_DEAD: ClassVar[int] = 3
    POWER_SUPPLY_HEALTH_OVERVOLTAGE: ClassVar[int] = 4
    POWER_SUPPLY_HEALTH_UNSPEC_FAILURE: ClassVar[int] = 5
    POWER_SUPPLY_HEALTH_COLD: ClassVar[int] = 6
    POWER_SUPPLY_HEALTH_WATCHDOG_TIMER_EXPIRE: ClassVar[int] = 7
    POWER_SUPPLY_HEALTH_SAFETY_TIMER_EXPIRE: ClassVar[int] = 8
    POWER_SUPPLY_TECHNOLOGY_UNKNOWN: ClassVar[int] = 0
    POWER_SUPPLY_TECHNOLOGY_NIMH: ClassVar[int] = 1
    POWER_SUPPLY_TECHNOLOGY_LION: ClassVar[int] = 2
    POWER_SUPPLY_TECHNOLOGY_LIPO: ClassVar[int] = 3
    POWER_SUPPLY_TECHNOLOGY_LIFE: ClassVar[int] = 4
    POWER_SUPPLY_TECHNOLOGY_NICD: ClassVar[int] = 5
    POWER_SUPPLY_TECHNOLOGY_LIMN: ClassVar[int] = 6
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/BatteryState'


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
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/Image'


@dataclass
class sensor_msgs__msg__PointCloud:
    """Class for sensor_msgs/msg/PointCloud."""

    header: std_msgs__msg__Header
    points: list[geometry_msgs__msg__Point32]
    channels: list[sensor_msgs__msg__ChannelFloat32]
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/PointCloud'


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
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/Imu'


@dataclass
class sensor_msgs__msg__NavSatStatus:
    """Class for sensor_msgs/msg/NavSatStatus."""

    status: int
    service: int
    STATUS_NO_FIX: ClassVar[int] = -1
    STATUS_FIX: ClassVar[int] = 0
    STATUS_SBAS_FIX: ClassVar[int] = 1
    STATUS_GBAS_FIX: ClassVar[int] = 2
    SERVICE_GPS: ClassVar[int] = 1
    SERVICE_GLONASS: ClassVar[int] = 2
    SERVICE_COMPASS: ClassVar[int] = 4
    SERVICE_GALILEO: ClassVar[int] = 8
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/NavSatStatus'


@dataclass
class sensor_msgs__msg__Illuminance:
    """Class for sensor_msgs/msg/Illuminance."""

    header: std_msgs__msg__Header
    illuminance: float
    variance: float
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/Illuminance'


@dataclass
class sensor_msgs__msg__Joy:
    """Class for sensor_msgs/msg/Joy."""

    header: std_msgs__msg__Header
    axes: numpy.ndarray[Any, numpy.dtype[numpy.float32]]
    buttons: numpy.ndarray[Any, numpy.dtype[numpy.int32]]
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/Joy'


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
    COVARIANCE_TYPE_UNKNOWN: ClassVar[int] = 0
    COVARIANCE_TYPE_APPROXIMATED: ClassVar[int] = 1
    COVARIANCE_TYPE_DIAGONAL_KNOWN: ClassVar[int] = 2
    COVARIANCE_TYPE_KNOWN: ClassVar[int] = 3
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/NavSatFix'


@dataclass
class sensor_msgs__msg__MultiDOFJointState:
    """Class for sensor_msgs/msg/MultiDOFJointState."""

    header: std_msgs__msg__Header
    joint_names: list[str]
    transforms: list[geometry_msgs__msg__Transform]
    twist: list[geometry_msgs__msg__Twist]
    wrench: list[geometry_msgs__msg__Wrench]
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/MultiDOFJointState'


@dataclass
class sensor_msgs__msg__MagneticField:
    """Class for sensor_msgs/msg/MagneticField."""

    header: std_msgs__msg__Header
    magnetic_field: geometry_msgs__msg__Vector3
    magnetic_field_covariance: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/MagneticField'


@dataclass
class sensor_msgs__msg__JointState:
    """Class for sensor_msgs/msg/JointState."""

    header: std_msgs__msg__Header
    name: list[str]
    position: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    velocity: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    effort: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/JointState'


@dataclass
class sensor_msgs__msg__PointField:
    """Class for sensor_msgs/msg/PointField."""

    name: str
    offset: int
    datatype: int
    count: int
    INT8: ClassVar[int] = 1
    UINT8: ClassVar[int] = 2
    INT16: ClassVar[int] = 3
    UINT16: ClassVar[int] = 4
    INT32: ClassVar[int] = 5
    UINT32: ClassVar[int] = 6
    FLOAT32: ClassVar[int] = 7
    FLOAT64: ClassVar[int] = 8
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/PointField'


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
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/PointCloud2'


@dataclass
class sensor_msgs__msg__JoyFeedback:
    """Class for sensor_msgs/msg/JoyFeedback."""

    type: int
    id: int
    intensity: float
    TYPE_LED: ClassVar[int] = 0
    TYPE_RUMBLE: ClassVar[int] = 1
    TYPE_BUZZER: ClassVar[int] = 2
    __msgtype__: ClassVar[str] = 'sensor_msgs/msg/JoyFeedback'


@dataclass
class shape_msgs__msg__SolidPrimitive:
    """Class for shape_msgs/msg/SolidPrimitive."""

    type: int
    dimensions: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    BOX: ClassVar[int] = 1
    SPHERE: ClassVar[int] = 2
    CYLINDER: ClassVar[int] = 3
    CONE: ClassVar[int] = 4
    BOX_X: ClassVar[int] = 0
    BOX_Y: ClassVar[int] = 1
    BOX_Z: ClassVar[int] = 2
    SPHERE_RADIUS: ClassVar[int] = 0
    CYLINDER_HEIGHT: ClassVar[int] = 0
    CYLINDER_RADIUS: ClassVar[int] = 1
    CONE_HEIGHT: ClassVar[int] = 0
    CONE_RADIUS: ClassVar[int] = 1
    __msgtype__: ClassVar[str] = 'shape_msgs/msg/SolidPrimitive'


@dataclass
class shape_msgs__msg__Mesh:
    """Class for shape_msgs/msg/Mesh."""

    triangles: list[shape_msgs__msg__MeshTriangle]
    vertices: list[geometry_msgs__msg__Point]
    __msgtype__: ClassVar[str] = 'shape_msgs/msg/Mesh'


@dataclass
class shape_msgs__msg__Plane:
    """Class for shape_msgs/msg/Plane."""

    coef: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    __msgtype__: ClassVar[str] = 'shape_msgs/msg/Plane'


@dataclass
class shape_msgs__msg__MeshTriangle:
    """Class for shape_msgs/msg/MeshTriangle."""

    vertex_indices: numpy.ndarray[Any, numpy.dtype[numpy.uint32]]
    __msgtype__: ClassVar[str] = 'shape_msgs/msg/MeshTriangle'


@dataclass
class statistics_msgs__msg__StatisticDataType:
    """Class for statistics_msgs/msg/StatisticDataType."""

    structure_needs_at_least_one_member: int
    STATISTICS_DATA_TYPE_UNINITIALIZED: ClassVar[int] = 0
    STATISTICS_DATA_TYPE_AVERAGE: ClassVar[int] = 1
    STATISTICS_DATA_TYPE_MINIMUM: ClassVar[int] = 2
    STATISTICS_DATA_TYPE_MAXIMUM: ClassVar[int] = 3
    STATISTICS_DATA_TYPE_STDDEV: ClassVar[int] = 4
    STATISTICS_DATA_TYPE_SAMPLE_COUNT: ClassVar[int] = 5
    __msgtype__: ClassVar[str] = 'statistics_msgs/msg/StatisticDataType'


@dataclass
class statistics_msgs__msg__StatisticDataPoint:
    """Class for statistics_msgs/msg/StatisticDataPoint."""

    data_type: int
    data: float
    __msgtype__: ClassVar[str] = 'statistics_msgs/msg/StatisticDataPoint'


@dataclass
class statistics_msgs__msg__MetricsMessage:
    """Class for statistics_msgs/msg/MetricsMessage."""

    measurement_source_name: str
    metrics_source: str
    unit: str
    window_start: builtin_interfaces__msg__Time
    window_stop: builtin_interfaces__msg__Time
    statistics: list[statistics_msgs__msg__StatisticDataPoint]
    __msgtype__: ClassVar[str] = 'statistics_msgs/msg/MetricsMessage'


@dataclass
class std_msgs__msg__UInt8:
    """Class for std_msgs/msg/UInt8."""

    data: int
    __msgtype__: ClassVar[str] = 'std_msgs/msg/UInt8'


@dataclass
class std_msgs__msg__Float32MultiArray:
    """Class for std_msgs/msg/Float32MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.float32]]
    __msgtype__: ClassVar[str] = 'std_msgs/msg/Float32MultiArray'


@dataclass
class std_msgs__msg__Int8:
    """Class for std_msgs/msg/Int8."""

    data: int
    __msgtype__: ClassVar[str] = 'std_msgs/msg/Int8'


@dataclass
class std_msgs__msg__Empty:
    """Class for std_msgs/msg/Empty."""

    structure_needs_at_least_one_member: int
    __msgtype__: ClassVar[str] = 'std_msgs/msg/Empty'


@dataclass
class std_msgs__msg__String:
    """Class for std_msgs/msg/String."""

    data: str
    __msgtype__: ClassVar[str] = 'std_msgs/msg/String'


@dataclass
class std_msgs__msg__MultiArrayDimension:
    """Class for std_msgs/msg/MultiArrayDimension."""

    label: str
    size: int
    stride: int
    __msgtype__: ClassVar[str] = 'std_msgs/msg/MultiArrayDimension'


@dataclass
class std_msgs__msg__UInt64:
    """Class for std_msgs/msg/UInt64."""

    data: int
    __msgtype__: ClassVar[str] = 'std_msgs/msg/UInt64'


@dataclass
class std_msgs__msg__UInt16:
    """Class for std_msgs/msg/UInt16."""

    data: int
    __msgtype__: ClassVar[str] = 'std_msgs/msg/UInt16'


@dataclass
class std_msgs__msg__Float32:
    """Class for std_msgs/msg/Float32."""

    data: float
    __msgtype__: ClassVar[str] = 'std_msgs/msg/Float32'


@dataclass
class std_msgs__msg__Int64:
    """Class for std_msgs/msg/Int64."""

    data: int
    __msgtype__: ClassVar[str] = 'std_msgs/msg/Int64'


@dataclass
class std_msgs__msg__Int16MultiArray:
    """Class for std_msgs/msg/Int16MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.int16]]
    __msgtype__: ClassVar[str] = 'std_msgs/msg/Int16MultiArray'


@dataclass
class std_msgs__msg__Int16:
    """Class for std_msgs/msg/Int16."""

    data: int
    __msgtype__: ClassVar[str] = 'std_msgs/msg/Int16'


@dataclass
class std_msgs__msg__Float64MultiArray:
    """Class for std_msgs/msg/Float64MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    __msgtype__: ClassVar[str] = 'std_msgs/msg/Float64MultiArray'


@dataclass
class std_msgs__msg__MultiArrayLayout:
    """Class for std_msgs/msg/MultiArrayLayout."""

    dim: list[std_msgs__msg__MultiArrayDimension]
    data_offset: int
    __msgtype__: ClassVar[str] = 'std_msgs/msg/MultiArrayLayout'


@dataclass
class std_msgs__msg__UInt32MultiArray:
    """Class for std_msgs/msg/UInt32MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.uint32]]
    __msgtype__: ClassVar[str] = 'std_msgs/msg/UInt32MultiArray'


@dataclass
class std_msgs__msg__Header:
    """Class for std_msgs/msg/Header."""

    stamp: builtin_interfaces__msg__Time
    frame_id: str
    __msgtype__: ClassVar[str] = 'std_msgs/msg/Header'


@dataclass
class std_msgs__msg__ByteMultiArray:
    """Class for std_msgs/msg/ByteMultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.uint8]]
    __msgtype__: ClassVar[str] = 'std_msgs/msg/ByteMultiArray'


@dataclass
class std_msgs__msg__Int8MultiArray:
    """Class for std_msgs/msg/Int8MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.int8]]
    __msgtype__: ClassVar[str] = 'std_msgs/msg/Int8MultiArray'


@dataclass
class std_msgs__msg__Float64:
    """Class for std_msgs/msg/Float64."""

    data: float
    __msgtype__: ClassVar[str] = 'std_msgs/msg/Float64'


@dataclass
class std_msgs__msg__UInt8MultiArray:
    """Class for std_msgs/msg/UInt8MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.uint8]]
    __msgtype__: ClassVar[str] = 'std_msgs/msg/UInt8MultiArray'


@dataclass
class std_msgs__msg__Byte:
    """Class for std_msgs/msg/Byte."""

    data: int
    __msgtype__: ClassVar[str] = 'std_msgs/msg/Byte'


@dataclass
class std_msgs__msg__Char:
    """Class for std_msgs/msg/Char."""

    data: int
    __msgtype__: ClassVar[str] = 'std_msgs/msg/Char'


@dataclass
class std_msgs__msg__UInt64MultiArray:
    """Class for std_msgs/msg/UInt64MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.uint64]]
    __msgtype__: ClassVar[str] = 'std_msgs/msg/UInt64MultiArray'


@dataclass
class std_msgs__msg__Int32MultiArray:
    """Class for std_msgs/msg/Int32MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.int32]]
    __msgtype__: ClassVar[str] = 'std_msgs/msg/Int32MultiArray'


@dataclass
class std_msgs__msg__ColorRGBA:
    """Class for std_msgs/msg/ColorRGBA."""

    r: float
    g: float
    b: float
    a: float
    __msgtype__: ClassVar[str] = 'std_msgs/msg/ColorRGBA'


@dataclass
class std_msgs__msg__Bool:
    """Class for std_msgs/msg/Bool."""

    data: bool
    __msgtype__: ClassVar[str] = 'std_msgs/msg/Bool'


@dataclass
class std_msgs__msg__UInt32:
    """Class for std_msgs/msg/UInt32."""

    data: int
    __msgtype__: ClassVar[str] = 'std_msgs/msg/UInt32'


@dataclass
class std_msgs__msg__Int64MultiArray:
    """Class for std_msgs/msg/Int64MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.int64]]
    __msgtype__: ClassVar[str] = 'std_msgs/msg/Int64MultiArray'


@dataclass
class std_msgs__msg__Int32:
    """Class for std_msgs/msg/Int32."""

    data: int
    __msgtype__: ClassVar[str] = 'std_msgs/msg/Int32'


@dataclass
class std_msgs__msg__UInt16MultiArray:
    """Class for std_msgs/msg/UInt16MultiArray."""

    layout: std_msgs__msg__MultiArrayLayout
    data: numpy.ndarray[Any, numpy.dtype[numpy.uint16]]
    __msgtype__: ClassVar[str] = 'std_msgs/msg/UInt16MultiArray'


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
    __msgtype__: ClassVar[str] = 'stereo_msgs/msg/DisparityImage'


@dataclass
class tf2_msgs__msg__TF2Error:
    """Class for tf2_msgs/msg/TF2Error."""

    error: int
    error_string: str
    NO_ERROR: ClassVar[int] = 0
    LOOKUP_ERROR: ClassVar[int] = 1
    CONNECTIVITY_ERROR: ClassVar[int] = 2
    EXTRAPOLATION_ERROR: ClassVar[int] = 3
    INVALID_ARGUMENT_ERROR: ClassVar[int] = 4
    TIMEOUT_ERROR: ClassVar[int] = 5
    TRANSFORM_ERROR: ClassVar[int] = 6
    __msgtype__: ClassVar[str] = 'tf2_msgs/msg/TF2Error'


@dataclass
class tf2_msgs__msg__TFMessage:
    """Class for tf2_msgs/msg/TFMessage."""

    transforms: list[geometry_msgs__msg__TransformStamped]
    __msgtype__: ClassVar[str] = 'tf2_msgs/msg/TFMessage'


@dataclass
class trajectory_msgs__msg__MultiDOFJointTrajectory:
    """Class for trajectory_msgs/msg/MultiDOFJointTrajectory."""

    header: std_msgs__msg__Header
    joint_names: list[str]
    points: list[trajectory_msgs__msg__MultiDOFJointTrajectoryPoint]
    __msgtype__: ClassVar[str] = 'trajectory_msgs/msg/MultiDOFJointTrajectory'


@dataclass
class trajectory_msgs__msg__JointTrajectory:
    """Class for trajectory_msgs/msg/JointTrajectory."""

    header: std_msgs__msg__Header
    joint_names: list[str]
    points: list[trajectory_msgs__msg__JointTrajectoryPoint]
    __msgtype__: ClassVar[str] = 'trajectory_msgs/msg/JointTrajectory'


@dataclass
class trajectory_msgs__msg__JointTrajectoryPoint:
    """Class for trajectory_msgs/msg/JointTrajectoryPoint."""

    positions: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    velocities: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    accelerations: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    effort: numpy.ndarray[Any, numpy.dtype[numpy.float64]]
    time_from_start: builtin_interfaces__msg__Duration
    __msgtype__: ClassVar[str] = 'trajectory_msgs/msg/JointTrajectoryPoint'


@dataclass
class trajectory_msgs__msg__MultiDOFJointTrajectoryPoint:
    """Class for trajectory_msgs/msg/MultiDOFJointTrajectoryPoint."""

    transforms: list[geometry_msgs__msg__Transform]
    velocities: list[geometry_msgs__msg__Twist]
    accelerations: list[geometry_msgs__msg__Twist]
    time_from_start: builtin_interfaces__msg__Duration
    __msgtype__: ClassVar[str] = 'trajectory_msgs/msg/MultiDOFJointTrajectoryPoint'


@dataclass
class unique_identifier_msgs__msg__UUID:
    """Class for unique_identifier_msgs/msg/UUID."""

    uuid: numpy.ndarray[Any, numpy.dtype[numpy.uint8]]
    __msgtype__: ClassVar[str] = 'unique_identifier_msgs/msg/UUID'


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
    ARROW: ClassVar[int] = 0
    CUBE: ClassVar[int] = 1
    SPHERE: ClassVar[int] = 2
    CYLINDER: ClassVar[int] = 3
    LINE_STRIP: ClassVar[int] = 4
    LINE_LIST: ClassVar[int] = 5
    CUBE_LIST: ClassVar[int] = 6
    SPHERE_LIST: ClassVar[int] = 7
    POINTS: ClassVar[int] = 8
    TEXT_VIEW_FACING: ClassVar[int] = 9
    MESH_RESOURCE: ClassVar[int] = 10
    TRIANGLE_LIST: ClassVar[int] = 11
    ADD: ClassVar[int] = 0
    MODIFY: ClassVar[int] = 0
    DELETE: ClassVar[int] = 2
    DELETEALL: ClassVar[int] = 3
    __msgtype__: ClassVar[str] = 'visualization_msgs/msg/Marker'


@dataclass
class visualization_msgs__msg__InteractiveMarkerInit:
    """Class for visualization_msgs/msg/InteractiveMarkerInit."""

    server_id: str
    seq_num: int
    markers: list[visualization_msgs__msg__InteractiveMarker]
    __msgtype__: ClassVar[str] = 'visualization_msgs/msg/InteractiveMarkerInit'


@dataclass
class visualization_msgs__msg__MenuEntry:
    """Class for visualization_msgs/msg/MenuEntry."""

    id: int
    parent_id: int
    title: str
    command: str
    command_type: int
    FEEDBACK: ClassVar[int] = 0
    ROSRUN: ClassVar[int] = 1
    ROSLAUNCH: ClassVar[int] = 2
    __msgtype__: ClassVar[str] = 'visualization_msgs/msg/MenuEntry'


@dataclass
class visualization_msgs__msg__MarkerArray:
    """Class for visualization_msgs/msg/MarkerArray."""

    markers: list[visualization_msgs__msg__Marker]
    __msgtype__: ClassVar[str] = 'visualization_msgs/msg/MarkerArray'


@dataclass
class visualization_msgs__msg__InteractiveMarkerUpdate:
    """Class for visualization_msgs/msg/InteractiveMarkerUpdate."""

    server_id: str
    seq_num: int
    type: int
    markers: list[visualization_msgs__msg__InteractiveMarker]
    poses: list[visualization_msgs__msg__InteractiveMarkerPose]
    erases: list[str]
    KEEP_ALIVE: ClassVar[int] = 0
    UPDATE: ClassVar[int] = 1
    __msgtype__: ClassVar[str] = 'visualization_msgs/msg/InteractiveMarkerUpdate'


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
    __msgtype__: ClassVar[str] = 'visualization_msgs/msg/InteractiveMarker'


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
    KEEP_ALIVE: ClassVar[int] = 0
    POSE_UPDATE: ClassVar[int] = 1
    MENU_SELECT: ClassVar[int] = 2
    BUTTON_CLICK: ClassVar[int] = 3
    MOUSE_DOWN: ClassVar[int] = 4
    MOUSE_UP: ClassVar[int] = 5
    __msgtype__: ClassVar[str] = 'visualization_msgs/msg/InteractiveMarkerFeedback'


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
    CIRCLE: ClassVar[int] = 0
    LINE_STRIP: ClassVar[int] = 1
    LINE_LIST: ClassVar[int] = 2
    POLYGON: ClassVar[int] = 3
    POINTS: ClassVar[int] = 4
    ADD: ClassVar[int] = 0
    REMOVE: ClassVar[int] = 1
    __msgtype__: ClassVar[str] = 'visualization_msgs/msg/ImageMarker'


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
    INHERIT: ClassVar[int] = 0
    FIXED: ClassVar[int] = 1
    VIEW_FACING: ClassVar[int] = 2
    NONE: ClassVar[int] = 0
    MENU: ClassVar[int] = 1
    BUTTON: ClassVar[int] = 2
    MOVE_AXIS: ClassVar[int] = 3
    MOVE_PLANE: ClassVar[int] = 4
    ROTATE_AXIS: ClassVar[int] = 5
    MOVE_ROTATE: ClassVar[int] = 6
    MOVE_3D: ClassVar[int] = 7
    ROTATE_3D: ClassVar[int] = 8
    MOVE_ROTATE_3D: ClassVar[int] = 9
    __msgtype__: ClassVar[str] = 'visualization_msgs/msg/InteractiveMarkerControl'


@dataclass
class visualization_msgs__msg__InteractiveMarkerPose:
    """Class for visualization_msgs/msg/InteractiveMarkerPose."""

    header: std_msgs__msg__Header
    pose: geometry_msgs__msg__Pose
    name: str
    __msgtype__: ClassVar[str] = 'visualization_msgs/msg/InteractiveMarkerPose'


FIELDDEFS: Typesdict = {
    'builtin_interfaces/msg/Time': ([
    ], [
        ('sec', (1, 'int32')),
        ('nanosec', (1, 'uint32')),
    ]),
    'builtin_interfaces/msg/Duration': ([
    ], [
        ('sec', (1, 'int32')),
        ('nanosec', (1, 'uint32')),
    ]),
    'diagnostic_msgs/msg/DiagnosticStatus': ([
        ('OK', 'uint8', 0),
        ('WARN', 'uint8', 1),
        ('ERROR', 'uint8', 2),
        ('STALE', 'uint8', 3),
    ], [
        ('level', (1, 'uint8')),
        ('name', (1, 'string')),
        ('message', (1, 'string')),
        ('hardware_id', (1, 'string')),
        ('values', (4, ((2, 'diagnostic_msgs/msg/KeyValue'), None))),
    ]),
    'diagnostic_msgs/msg/DiagnosticArray': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('status', (4, ((2, 'diagnostic_msgs/msg/DiagnosticStatus'), None))),
    ]),
    'diagnostic_msgs/msg/KeyValue': ([
    ], [
        ('key', (1, 'string')),
        ('value', (1, 'string')),
    ]),
    'geometry_msgs/msg/AccelWithCovariance': ([
    ], [
        ('accel', (2, 'geometry_msgs/msg/Accel')),
        ('covariance', (3, ((1, 'float64'), 36))),
    ]),
    'geometry_msgs/msg/Point32': ([
    ], [
        ('x', (1, 'float32')),
        ('y', (1, 'float32')),
        ('z', (1, 'float32')),
    ]),
    'geometry_msgs/msg/Vector3': ([
    ], [
        ('x', (1, 'float64')),
        ('y', (1, 'float64')),
        ('z', (1, 'float64')),
    ]),
    'geometry_msgs/msg/Inertia': ([
    ], [
        ('m', (1, 'float64')),
        ('com', (2, 'geometry_msgs/msg/Vector3')),
        ('ixx', (1, 'float64')),
        ('ixy', (1, 'float64')),
        ('ixz', (1, 'float64')),
        ('iyy', (1, 'float64')),
        ('iyz', (1, 'float64')),
        ('izz', (1, 'float64')),
    ]),
    'geometry_msgs/msg/PoseWithCovarianceStamped': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('pose', (2, 'geometry_msgs/msg/PoseWithCovariance')),
    ]),
    'geometry_msgs/msg/Twist': ([
    ], [
        ('linear', (2, 'geometry_msgs/msg/Vector3')),
        ('angular', (2, 'geometry_msgs/msg/Vector3')),
    ]),
    'geometry_msgs/msg/Pose': ([
    ], [
        ('position', (2, 'geometry_msgs/msg/Point')),
        ('orientation', (2, 'geometry_msgs/msg/Quaternion')),
    ]),
    'geometry_msgs/msg/Point': ([
    ], [
        ('x', (1, 'float64')),
        ('y', (1, 'float64')),
        ('z', (1, 'float64')),
    ]),
    'geometry_msgs/msg/Vector3Stamped': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('vector', (2, 'geometry_msgs/msg/Vector3')),
    ]),
    'geometry_msgs/msg/Transform': ([
    ], [
        ('translation', (2, 'geometry_msgs/msg/Vector3')),
        ('rotation', (2, 'geometry_msgs/msg/Quaternion')),
    ]),
    'geometry_msgs/msg/PolygonStamped': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('polygon', (2, 'geometry_msgs/msg/Polygon')),
    ]),
    'geometry_msgs/msg/Quaternion': ([
    ], [
        ('x', (1, 'float64')),
        ('y', (1, 'float64')),
        ('z', (1, 'float64')),
        ('w', (1, 'float64')),
    ]),
    'geometry_msgs/msg/Pose2D': ([
    ], [
        ('x', (1, 'float64')),
        ('y', (1, 'float64')),
        ('theta', (1, 'float64')),
    ]),
    'geometry_msgs/msg/InertiaStamped': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('inertia', (2, 'geometry_msgs/msg/Inertia')),
    ]),
    'geometry_msgs/msg/TwistStamped': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('twist', (2, 'geometry_msgs/msg/Twist')),
    ]),
    'geometry_msgs/msg/PoseStamped': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('pose', (2, 'geometry_msgs/msg/Pose')),
    ]),
    'geometry_msgs/msg/PointStamped': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('point', (2, 'geometry_msgs/msg/Point')),
    ]),
    'geometry_msgs/msg/Polygon': ([
    ], [
        ('points', (4, ((2, 'geometry_msgs/msg/Point32'), None))),
    ]),
    'geometry_msgs/msg/PoseArray': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('poses', (4, ((2, 'geometry_msgs/msg/Pose'), None))),
    ]),
    'geometry_msgs/msg/AccelStamped': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('accel', (2, 'geometry_msgs/msg/Accel')),
    ]),
    'geometry_msgs/msg/TwistWithCovarianceStamped': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('twist', (2, 'geometry_msgs/msg/TwistWithCovariance')),
    ]),
    'geometry_msgs/msg/QuaternionStamped': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('quaternion', (2, 'geometry_msgs/msg/Quaternion')),
    ]),
    'geometry_msgs/msg/WrenchStamped': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('wrench', (2, 'geometry_msgs/msg/Wrench')),
    ]),
    'geometry_msgs/msg/AccelWithCovarianceStamped': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('accel', (2, 'geometry_msgs/msg/AccelWithCovariance')),
    ]),
    'geometry_msgs/msg/PoseWithCovariance': ([
    ], [
        ('pose', (2, 'geometry_msgs/msg/Pose')),
        ('covariance', (3, ((1, 'float64'), 36))),
    ]),
    'geometry_msgs/msg/Wrench': ([
    ], [
        ('force', (2, 'geometry_msgs/msg/Vector3')),
        ('torque', (2, 'geometry_msgs/msg/Vector3')),
    ]),
    'geometry_msgs/msg/TransformStamped': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('child_frame_id', (1, 'string')),
        ('transform', (2, 'geometry_msgs/msg/Transform')),
    ]),
    'geometry_msgs/msg/Accel': ([
    ], [
        ('linear', (2, 'geometry_msgs/msg/Vector3')),
        ('angular', (2, 'geometry_msgs/msg/Vector3')),
    ]),
    'geometry_msgs/msg/TwistWithCovariance': ([
    ], [
        ('twist', (2, 'geometry_msgs/msg/Twist')),
        ('covariance', (3, ((1, 'float64'), 36))),
    ]),
    'libstatistics_collector/msg/DummyMessage': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
    ]),
    'lifecycle_msgs/msg/TransitionDescription': ([
    ], [
        ('transition', (2, 'lifecycle_msgs/msg/Transition')),
        ('start_state', (2, 'lifecycle_msgs/msg/State')),
        ('goal_state', (2, 'lifecycle_msgs/msg/State')),
    ]),
    'lifecycle_msgs/msg/State': ([
        ('PRIMARY_STATE_UNKNOWN', 'uint8', 0),
        ('PRIMARY_STATE_UNCONFIGURED', 'uint8', 1),
        ('PRIMARY_STATE_INACTIVE', 'uint8', 2),
        ('PRIMARY_STATE_ACTIVE', 'uint8', 3),
        ('PRIMARY_STATE_FINALIZED', 'uint8', 4),
        ('TRANSITION_STATE_CONFIGURING', 'uint8', 10),
        ('TRANSITION_STATE_CLEANINGUP', 'uint8', 11),
        ('TRANSITION_STATE_SHUTTINGDOWN', 'uint8', 12),
        ('TRANSITION_STATE_ACTIVATING', 'uint8', 13),
        ('TRANSITION_STATE_DEACTIVATING', 'uint8', 14),
        ('TRANSITION_STATE_ERRORPROCESSING', 'uint8', 15),
    ], [
        ('id', (1, 'uint8')),
        ('label', (1, 'string')),
    ]),
    'lifecycle_msgs/msg/TransitionEvent': ([
    ], [
        ('timestamp', (1, 'uint64')),
        ('transition', (2, 'lifecycle_msgs/msg/Transition')),
        ('start_state', (2, 'lifecycle_msgs/msg/State')),
        ('goal_state', (2, 'lifecycle_msgs/msg/State')),
    ]),
    'lifecycle_msgs/msg/Transition': ([
        ('TRANSITION_CREATE', 'uint8', 0),
        ('TRANSITION_CONFIGURE', 'uint8', 1),
        ('TRANSITION_CLEANUP', 'uint8', 2),
        ('TRANSITION_ACTIVATE', 'uint8', 3),
        ('TRANSITION_DEACTIVATE', 'uint8', 4),
        ('TRANSITION_UNCONFIGURED_SHUTDOWN', 'uint8', 5),
        ('TRANSITION_INACTIVE_SHUTDOWN', 'uint8', 6),
        ('TRANSITION_ACTIVE_SHUTDOWN', 'uint8', 7),
        ('TRANSITION_DESTROY', 'uint8', 8),
        ('TRANSITION_ON_CONFIGURE_SUCCESS', 'uint8', 10),
        ('TRANSITION_ON_CONFIGURE_FAILURE', 'uint8', 11),
        ('TRANSITION_ON_CONFIGURE_ERROR', 'uint8', 12),
        ('TRANSITION_ON_CLEANUP_SUCCESS', 'uint8', 20),
        ('TRANSITION_ON_CLEANUP_FAILURE', 'uint8', 21),
        ('TRANSITION_ON_CLEANUP_ERROR', 'uint8', 22),
        ('TRANSITION_ON_ACTIVATE_SUCCESS', 'uint8', 30),
        ('TRANSITION_ON_ACTIVATE_FAILURE', 'uint8', 31),
        ('TRANSITION_ON_ACTIVATE_ERROR', 'uint8', 32),
        ('TRANSITION_ON_DEACTIVATE_SUCCESS', 'uint8', 40),
        ('TRANSITION_ON_DEACTIVATE_FAILURE', 'uint8', 41),
        ('TRANSITION_ON_DEACTIVATE_ERROR', 'uint8', 42),
        ('TRANSITION_ON_SHUTDOWN_SUCCESS', 'uint8', 50),
        ('TRANSITION_ON_SHUTDOWN_FAILURE', 'uint8', 51),
        ('TRANSITION_ON_SHUTDOWN_ERROR', 'uint8', 52),
        ('TRANSITION_ON_ERROR_SUCCESS', 'uint8', 60),
        ('TRANSITION_ON_ERROR_FAILURE', 'uint8', 61),
        ('TRANSITION_ON_ERROR_ERROR', 'uint8', 62),
        ('TRANSITION_CALLBACK_SUCCESS', 'uint8', 97),
        ('TRANSITION_CALLBACK_FAILURE', 'uint8', 98),
        ('TRANSITION_CALLBACK_ERROR', 'uint8', 99),
    ], [
        ('id', (1, 'uint8')),
        ('label', (1, 'string')),
    ]),
    'nav_msgs/msg/MapMetaData': ([
    ], [
        ('map_load_time', (2, 'builtin_interfaces/msg/Time')),
        ('resolution', (1, 'float32')),
        ('width', (1, 'uint32')),
        ('height', (1, 'uint32')),
        ('origin', (2, 'geometry_msgs/msg/Pose')),
    ]),
    'nav_msgs/msg/GridCells': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('cell_width', (1, 'float32')),
        ('cell_height', (1, 'float32')),
        ('cells', (4, ((2, 'geometry_msgs/msg/Point'), None))),
    ]),
    'nav_msgs/msg/Odometry': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('child_frame_id', (1, 'string')),
        ('pose', (2, 'geometry_msgs/msg/PoseWithCovariance')),
        ('twist', (2, 'geometry_msgs/msg/TwistWithCovariance')),
    ]),
    'nav_msgs/msg/Path': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('poses', (4, ((2, 'geometry_msgs/msg/PoseStamped'), None))),
    ]),
    'nav_msgs/msg/OccupancyGrid': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('info', (2, 'nav_msgs/msg/MapMetaData')),
        ('data', (4, ((1, 'int8'), None))),
    ]),
    'rcl_interfaces/msg/ListParametersResult': ([
    ], [
        ('names', (4, ((1, 'string'), None))),
        ('prefixes', (4, ((1, 'string'), None))),
    ]),
    'rcl_interfaces/msg/ParameterType': ([
        ('PARAMETER_NOT_SET', 'uint8', 0),
        ('PARAMETER_BOOL', 'uint8', 1),
        ('PARAMETER_INTEGER', 'uint8', 2),
        ('PARAMETER_DOUBLE', 'uint8', 3),
        ('PARAMETER_STRING', 'uint8', 4),
        ('PARAMETER_BYTE_ARRAY', 'uint8', 5),
        ('PARAMETER_BOOL_ARRAY', 'uint8', 6),
        ('PARAMETER_INTEGER_ARRAY', 'uint8', 7),
        ('PARAMETER_DOUBLE_ARRAY', 'uint8', 8),
        ('PARAMETER_STRING_ARRAY', 'uint8', 9),
    ], [
        ('structure_needs_at_least_one_member', (1, 'uint8')),
    ]),
    'rcl_interfaces/msg/ParameterEventDescriptors': ([
    ], [
        ('new_parameters', (4, ((2, 'rcl_interfaces/msg/ParameterDescriptor'), None))),
        ('changed_parameters', (4, ((2, 'rcl_interfaces/msg/ParameterDescriptor'), None))),
        ('deleted_parameters', (4, ((2, 'rcl_interfaces/msg/ParameterDescriptor'), None))),
    ]),
    'rcl_interfaces/msg/ParameterEvent': ([
    ], [
        ('stamp', (2, 'builtin_interfaces/msg/Time')),
        ('node', (1, 'string')),
        ('new_parameters', (4, ((2, 'rcl_interfaces/msg/Parameter'), None))),
        ('changed_parameters', (4, ((2, 'rcl_interfaces/msg/Parameter'), None))),
        ('deleted_parameters', (4, ((2, 'rcl_interfaces/msg/Parameter'), None))),
    ]),
    'rcl_interfaces/msg/IntegerRange': ([
    ], [
        ('from_value', (1, 'int64')),
        ('to_value', (1, 'int64')),
        ('step', (1, 'uint64')),
    ]),
    'rcl_interfaces/msg/Parameter': ([
    ], [
        ('name', (1, 'string')),
        ('value', (2, 'rcl_interfaces/msg/ParameterValue')),
    ]),
    'rcl_interfaces/msg/ParameterValue': ([
    ], [
        ('type', (1, 'uint8')),
        ('bool_value', (1, 'bool')),
        ('integer_value', (1, 'int64')),
        ('double_value', (1, 'float64')),
        ('string_value', (1, 'string')),
        ('byte_array_value', (4, ((1, 'uint8'), None))),
        ('bool_array_value', (4, ((1, 'bool'), None))),
        ('integer_array_value', (4, ((1, 'int64'), None))),
        ('double_array_value', (4, ((1, 'float64'), None))),
        ('string_array_value', (4, ((1, 'string'), None))),
    ]),
    'rcl_interfaces/msg/FloatingPointRange': ([
    ], [
        ('from_value', (1, 'float64')),
        ('to_value', (1, 'float64')),
        ('step', (1, 'float64')),
    ]),
    'rcl_interfaces/msg/SetParametersResult': ([
    ], [
        ('successful', (1, 'bool')),
        ('reason', (1, 'string')),
    ]),
    'rcl_interfaces/msg/Log': ([
        ('DEBUG', 'uint8', 10),
        ('INFO', 'uint8', 20),
        ('WARN', 'uint8', 30),
        ('ERROR', 'uint8', 40),
        ('FATAL', 'uint8', 50),
    ], [
        ('stamp', (2, 'builtin_interfaces/msg/Time')),
        ('level', (1, 'uint8')),
        ('name', (1, 'string')),
        ('msg', (1, 'string')),
        ('file', (1, 'string')),
        ('function', (1, 'string')),
        ('line', (1, 'uint32')),
    ]),
    'rcl_interfaces/msg/ParameterDescriptor': ([
    ], [
        ('name', (1, 'string')),
        ('type', (1, 'uint8')),
        ('description', (1, 'string')),
        ('additional_constraints', (1, 'string')),
        ('read_only', (1, 'bool')),
        ('floating_point_range', (4, ((2, 'rcl_interfaces/msg/FloatingPointRange'), None))),
        ('integer_range', (4, ((2, 'rcl_interfaces/msg/IntegerRange'), None))),
    ]),
    'rmw_dds_common/msg/Gid': ([
    ], [
        ('data', (3, ((1, 'uint8'), 24))),
    ]),
    'rmw_dds_common/msg/NodeEntitiesInfo': ([
    ], [
        ('node_namespace', (1, 'string')),
        ('node_name', (1, 'string')),
        ('reader_gid_seq', (4, ((2, 'rmw_dds_common/msg/Gid'), None))),
        ('writer_gid_seq', (4, ((2, 'rmw_dds_common/msg/Gid'), None))),
    ]),
    'rmw_dds_common/msg/ParticipantEntitiesInfo': ([
    ], [
        ('gid', (2, 'rmw_dds_common/msg/Gid')),
        ('node_entities_info_seq', (4, ((2, 'rmw_dds_common/msg/NodeEntitiesInfo'), None))),
    ]),
    'rosgraph_msgs/msg/Clock': ([
    ], [
        ('clock', (2, 'builtin_interfaces/msg/Time')),
    ]),
    'sensor_msgs/msg/Temperature': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('temperature', (1, 'float64')),
        ('variance', (1, 'float64')),
    ]),
    'sensor_msgs/msg/Range': ([
        ('ULTRASOUND', 'uint8', 0),
        ('INFRARED', 'uint8', 1),
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('radiation_type', (1, 'uint8')),
        ('field_of_view', (1, 'float32')),
        ('min_range', (1, 'float32')),
        ('max_range', (1, 'float32')),
        ('range', (1, 'float32')),
    ]),
    'sensor_msgs/msg/RegionOfInterest': ([
    ], [
        ('x_offset', (1, 'uint32')),
        ('y_offset', (1, 'uint32')),
        ('height', (1, 'uint32')),
        ('width', (1, 'uint32')),
        ('do_rectify', (1, 'bool')),
    ]),
    'sensor_msgs/msg/JoyFeedbackArray': ([
    ], [
        ('array', (4, ((2, 'sensor_msgs/msg/JoyFeedback'), None))),
    ]),
    'sensor_msgs/msg/TimeReference': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('time_ref', (2, 'builtin_interfaces/msg/Time')),
        ('source', (1, 'string')),
    ]),
    'sensor_msgs/msg/CompressedImage': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('format', (1, 'string')),
        ('data', (4, ((1, 'uint8'), None))),
    ]),
    'sensor_msgs/msg/MultiEchoLaserScan': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('angle_min', (1, 'float32')),
        ('angle_max', (1, 'float32')),
        ('angle_increment', (1, 'float32')),
        ('time_increment', (1, 'float32')),
        ('scan_time', (1, 'float32')),
        ('range_min', (1, 'float32')),
        ('range_max', (1, 'float32')),
        ('ranges', (4, ((2, 'sensor_msgs/msg/LaserEcho'), None))),
        ('intensities', (4, ((2, 'sensor_msgs/msg/LaserEcho'), None))),
    ]),
    'sensor_msgs/msg/LaserEcho': ([
    ], [
        ('echoes', (4, ((1, 'float32'), None))),
    ]),
    'sensor_msgs/msg/ChannelFloat32': ([
    ], [
        ('name', (1, 'string')),
        ('values', (4, ((1, 'float32'), None))),
    ]),
    'sensor_msgs/msg/CameraInfo': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('height', (1, 'uint32')),
        ('width', (1, 'uint32')),
        ('distortion_model', (1, 'string')),
        ('d', (4, ((1, 'float64'), None))),
        ('k', (3, ((1, 'float64'), 9))),
        ('r', (3, ((1, 'float64'), 9))),
        ('p', (3, ((1, 'float64'), 12))),
        ('binning_x', (1, 'uint32')),
        ('binning_y', (1, 'uint32')),
        ('roi', (2, 'sensor_msgs/msg/RegionOfInterest')),
    ]),
    'sensor_msgs/msg/RelativeHumidity': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('relative_humidity', (1, 'float64')),
        ('variance', (1, 'float64')),
    ]),
    'sensor_msgs/msg/FluidPressure': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('fluid_pressure', (1, 'float64')),
        ('variance', (1, 'float64')),
    ]),
    'sensor_msgs/msg/LaserScan': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('angle_min', (1, 'float32')),
        ('angle_max', (1, 'float32')),
        ('angle_increment', (1, 'float32')),
        ('time_increment', (1, 'float32')),
        ('scan_time', (1, 'float32')),
        ('range_min', (1, 'float32')),
        ('range_max', (1, 'float32')),
        ('ranges', (4, ((1, 'float32'), None))),
        ('intensities', (4, ((1, 'float32'), None))),
    ]),
    'sensor_msgs/msg/BatteryState': ([
        ('POWER_SUPPLY_STATUS_UNKNOWN', 'uint8', 0),
        ('POWER_SUPPLY_STATUS_CHARGING', 'uint8', 1),
        ('POWER_SUPPLY_STATUS_DISCHARGING', 'uint8', 2),
        ('POWER_SUPPLY_STATUS_NOT_CHARGING', 'uint8', 3),
        ('POWER_SUPPLY_STATUS_FULL', 'uint8', 4),
        ('POWER_SUPPLY_HEALTH_UNKNOWN', 'uint8', 0),
        ('POWER_SUPPLY_HEALTH_GOOD', 'uint8', 1),
        ('POWER_SUPPLY_HEALTH_OVERHEAT', 'uint8', 2),
        ('POWER_SUPPLY_HEALTH_DEAD', 'uint8', 3),
        ('POWER_SUPPLY_HEALTH_OVERVOLTAGE', 'uint8', 4),
        ('POWER_SUPPLY_HEALTH_UNSPEC_FAILURE', 'uint8', 5),
        ('POWER_SUPPLY_HEALTH_COLD', 'uint8', 6),
        ('POWER_SUPPLY_HEALTH_WATCHDOG_TIMER_EXPIRE', 'uint8', 7),
        ('POWER_SUPPLY_HEALTH_SAFETY_TIMER_EXPIRE', 'uint8', 8),
        ('POWER_SUPPLY_TECHNOLOGY_UNKNOWN', 'uint8', 0),
        ('POWER_SUPPLY_TECHNOLOGY_NIMH', 'uint8', 1),
        ('POWER_SUPPLY_TECHNOLOGY_LION', 'uint8', 2),
        ('POWER_SUPPLY_TECHNOLOGY_LIPO', 'uint8', 3),
        ('POWER_SUPPLY_TECHNOLOGY_LIFE', 'uint8', 4),
        ('POWER_SUPPLY_TECHNOLOGY_NICD', 'uint8', 5),
        ('POWER_SUPPLY_TECHNOLOGY_LIMN', 'uint8', 6),
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('voltage', (1, 'float32')),
        ('temperature', (1, 'float32')),
        ('current', (1, 'float32')),
        ('charge', (1, 'float32')),
        ('capacity', (1, 'float32')),
        ('design_capacity', (1, 'float32')),
        ('percentage', (1, 'float32')),
        ('power_supply_status', (1, 'uint8')),
        ('power_supply_health', (1, 'uint8')),
        ('power_supply_technology', (1, 'uint8')),
        ('present', (1, 'bool')),
        ('cell_voltage', (4, ((1, 'float32'), None))),
        ('cell_temperature', (4, ((1, 'float32'), None))),
        ('location', (1, 'string')),
        ('serial_number', (1, 'string')),
    ]),
    'sensor_msgs/msg/Image': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('height', (1, 'uint32')),
        ('width', (1, 'uint32')),
        ('encoding', (1, 'string')),
        ('is_bigendian', (1, 'uint8')),
        ('step', (1, 'uint32')),
        ('data', (4, ((1, 'uint8'), None))),
    ]),
    'sensor_msgs/msg/PointCloud': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('points', (4, ((2, 'geometry_msgs/msg/Point32'), None))),
        ('channels', (4, ((2, 'sensor_msgs/msg/ChannelFloat32'), None))),
    ]),
    'sensor_msgs/msg/Imu': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('orientation', (2, 'geometry_msgs/msg/Quaternion')),
        ('orientation_covariance', (3, ((1, 'float64'), 9))),
        ('angular_velocity', (2, 'geometry_msgs/msg/Vector3')),
        ('angular_velocity_covariance', (3, ((1, 'float64'), 9))),
        ('linear_acceleration', (2, 'geometry_msgs/msg/Vector3')),
        ('linear_acceleration_covariance', (3, ((1, 'float64'), 9))),
    ]),
    'sensor_msgs/msg/NavSatStatus': ([
        ('STATUS_NO_FIX', 'int8', -1),
        ('STATUS_FIX', 'int8', 0),
        ('STATUS_SBAS_FIX', 'int8', 1),
        ('STATUS_GBAS_FIX', 'int8', 2),
        ('SERVICE_GPS', 'uint16', 1),
        ('SERVICE_GLONASS', 'uint16', 2),
        ('SERVICE_COMPASS', 'uint16', 4),
        ('SERVICE_GALILEO', 'uint16', 8),
    ], [
        ('status', (1, 'int8')),
        ('service', (1, 'uint16')),
    ]),
    'sensor_msgs/msg/Illuminance': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('illuminance', (1, 'float64')),
        ('variance', (1, 'float64')),
    ]),
    'sensor_msgs/msg/Joy': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('axes', (4, ((1, 'float32'), None))),
        ('buttons', (4, ((1, 'int32'), None))),
    ]),
    'sensor_msgs/msg/NavSatFix': ([
        ('COVARIANCE_TYPE_UNKNOWN', 'uint8', 0),
        ('COVARIANCE_TYPE_APPROXIMATED', 'uint8', 1),
        ('COVARIANCE_TYPE_DIAGONAL_KNOWN', 'uint8', 2),
        ('COVARIANCE_TYPE_KNOWN', 'uint8', 3),
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('status', (2, 'sensor_msgs/msg/NavSatStatus')),
        ('latitude', (1, 'float64')),
        ('longitude', (1, 'float64')),
        ('altitude', (1, 'float64')),
        ('position_covariance', (3, ((1, 'float64'), 9))),
        ('position_covariance_type', (1, 'uint8')),
    ]),
    'sensor_msgs/msg/MultiDOFJointState': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('joint_names', (4, ((1, 'string'), None))),
        ('transforms', (4, ((2, 'geometry_msgs/msg/Transform'), None))),
        ('twist', (4, ((2, 'geometry_msgs/msg/Twist'), None))),
        ('wrench', (4, ((2, 'geometry_msgs/msg/Wrench'), None))),
    ]),
    'sensor_msgs/msg/MagneticField': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('magnetic_field', (2, 'geometry_msgs/msg/Vector3')),
        ('magnetic_field_covariance', (3, ((1, 'float64'), 9))),
    ]),
    'sensor_msgs/msg/JointState': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('name', (4, ((1, 'string'), None))),
        ('position', (4, ((1, 'float64'), None))),
        ('velocity', (4, ((1, 'float64'), None))),
        ('effort', (4, ((1, 'float64'), None))),
    ]),
    'sensor_msgs/msg/PointField': ([
        ('INT8', 'uint8', 1),
        ('UINT8', 'uint8', 2),
        ('INT16', 'uint8', 3),
        ('UINT16', 'uint8', 4),
        ('INT32', 'uint8', 5),
        ('UINT32', 'uint8', 6),
        ('FLOAT32', 'uint8', 7),
        ('FLOAT64', 'uint8', 8),
    ], [
        ('name', (1, 'string')),
        ('offset', (1, 'uint32')),
        ('datatype', (1, 'uint8')),
        ('count', (1, 'uint32')),
    ]),
    'sensor_msgs/msg/PointCloud2': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('height', (1, 'uint32')),
        ('width', (1, 'uint32')),
        ('fields', (4, ((2, 'sensor_msgs/msg/PointField'), None))),
        ('is_bigendian', (1, 'bool')),
        ('point_step', (1, 'uint32')),
        ('row_step', (1, 'uint32')),
        ('data', (4, ((1, 'uint8'), None))),
        ('is_dense', (1, 'bool')),
    ]),
    'sensor_msgs/msg/JoyFeedback': ([
        ('TYPE_LED', 'uint8', 0),
        ('TYPE_RUMBLE', 'uint8', 1),
        ('TYPE_BUZZER', 'uint8', 2),
    ], [
        ('type', (1, 'uint8')),
        ('id', (1, 'uint8')),
        ('intensity', (1, 'float32')),
    ]),
    'shape_msgs/msg/SolidPrimitive': ([
        ('BOX', 'uint8', 1),
        ('SPHERE', 'uint8', 2),
        ('CYLINDER', 'uint8', 3),
        ('CONE', 'uint8', 4),
        ('BOX_X', 'uint8', 0),
        ('BOX_Y', 'uint8', 1),
        ('BOX_Z', 'uint8', 2),
        ('SPHERE_RADIUS', 'uint8', 0),
        ('CYLINDER_HEIGHT', 'uint8', 0),
        ('CYLINDER_RADIUS', 'uint8', 1),
        ('CONE_HEIGHT', 'uint8', 0),
        ('CONE_RADIUS', 'uint8', 1),
    ], [
        ('type', (1, 'uint8')),
        ('dimensions', (4, ((1, 'float64'), None))),
    ]),
    'shape_msgs/msg/Mesh': ([
    ], [
        ('triangles', (4, ((2, 'shape_msgs/msg/MeshTriangle'), None))),
        ('vertices', (4, ((2, 'geometry_msgs/msg/Point'), None))),
    ]),
    'shape_msgs/msg/Plane': ([
    ], [
        ('coef', (3, ((1, 'float64'), 4))),
    ]),
    'shape_msgs/msg/MeshTriangle': ([
    ], [
        ('vertex_indices', (3, ((1, 'uint32'), 3))),
    ]),
    'statistics_msgs/msg/StatisticDataType': ([
        ('STATISTICS_DATA_TYPE_UNINITIALIZED', 'uint8', 0),
        ('STATISTICS_DATA_TYPE_AVERAGE', 'uint8', 1),
        ('STATISTICS_DATA_TYPE_MINIMUM', 'uint8', 2),
        ('STATISTICS_DATA_TYPE_MAXIMUM', 'uint8', 3),
        ('STATISTICS_DATA_TYPE_STDDEV', 'uint8', 4),
        ('STATISTICS_DATA_TYPE_SAMPLE_COUNT', 'uint8', 5),
    ], [
        ('structure_needs_at_least_one_member', (1, 'uint8')),
    ]),
    'statistics_msgs/msg/StatisticDataPoint': ([
    ], [
        ('data_type', (1, 'uint8')),
        ('data', (1, 'float64')),
    ]),
    'statistics_msgs/msg/MetricsMessage': ([
    ], [
        ('measurement_source_name', (1, 'string')),
        ('metrics_source', (1, 'string')),
        ('unit', (1, 'string')),
        ('window_start', (2, 'builtin_interfaces/msg/Time')),
        ('window_stop', (2, 'builtin_interfaces/msg/Time')),
        ('statistics', (4, ((2, 'statistics_msgs/msg/StatisticDataPoint'), None))),
    ]),
    'std_msgs/msg/UInt8': ([
    ], [
        ('data', (1, 'uint8')),
    ]),
    'std_msgs/msg/Float32MultiArray': ([
    ], [
        ('layout', (2, 'std_msgs/msg/MultiArrayLayout')),
        ('data', (4, ((1, 'float32'), None))),
    ]),
    'std_msgs/msg/Int8': ([
    ], [
        ('data', (1, 'int8')),
    ]),
    'std_msgs/msg/Empty': ([
    ], [
        ('structure_needs_at_least_one_member', (1, 'uint8')),
    ]),
    'std_msgs/msg/String': ([
    ], [
        ('data', (1, 'string')),
    ]),
    'std_msgs/msg/MultiArrayDimension': ([
    ], [
        ('label', (1, 'string')),
        ('size', (1, 'uint32')),
        ('stride', (1, 'uint32')),
    ]),
    'std_msgs/msg/UInt64': ([
    ], [
        ('data', (1, 'uint64')),
    ]),
    'std_msgs/msg/UInt16': ([
    ], [
        ('data', (1, 'uint16')),
    ]),
    'std_msgs/msg/Float32': ([
    ], [
        ('data', (1, 'float32')),
    ]),
    'std_msgs/msg/Int64': ([
    ], [
        ('data', (1, 'int64')),
    ]),
    'std_msgs/msg/Int16MultiArray': ([
    ], [
        ('layout', (2, 'std_msgs/msg/MultiArrayLayout')),
        ('data', (4, ((1, 'int16'), None))),
    ]),
    'std_msgs/msg/Int16': ([
    ], [
        ('data', (1, 'int16')),
    ]),
    'std_msgs/msg/Float64MultiArray': ([
    ], [
        ('layout', (2, 'std_msgs/msg/MultiArrayLayout')),
        ('data', (4, ((1, 'float64'), None))),
    ]),
    'std_msgs/msg/MultiArrayLayout': ([
    ], [
        ('dim', (4, ((2, 'std_msgs/msg/MultiArrayDimension'), None))),
        ('data_offset', (1, 'uint32')),
    ]),
    'std_msgs/msg/UInt32MultiArray': ([
    ], [
        ('layout', (2, 'std_msgs/msg/MultiArrayLayout')),
        ('data', (4, ((1, 'uint32'), None))),
    ]),
    'std_msgs/msg/Header': ([
    ], [
        ('stamp', (2, 'builtin_interfaces/msg/Time')),
        ('frame_id', (1, 'string')),
    ]),
    'std_msgs/msg/ByteMultiArray': ([
    ], [
        ('layout', (2, 'std_msgs/msg/MultiArrayLayout')),
        ('data', (4, ((1, 'uint8'), None))),
    ]),
    'std_msgs/msg/Int8MultiArray': ([
    ], [
        ('layout', (2, 'std_msgs/msg/MultiArrayLayout')),
        ('data', (4, ((1, 'int8'), None))),
    ]),
    'std_msgs/msg/Float64': ([
    ], [
        ('data', (1, 'float64')),
    ]),
    'std_msgs/msg/UInt8MultiArray': ([
    ], [
        ('layout', (2, 'std_msgs/msg/MultiArrayLayout')),
        ('data', (4, ((1, 'uint8'), None))),
    ]),
    'std_msgs/msg/Byte': ([
    ], [
        ('data', (1, 'uint8')),
    ]),
    'std_msgs/msg/Char': ([
    ], [
        ('data', (1, 'uint8')),
    ]),
    'std_msgs/msg/UInt64MultiArray': ([
    ], [
        ('layout', (2, 'std_msgs/msg/MultiArrayLayout')),
        ('data', (4, ((1, 'uint64'), None))),
    ]),
    'std_msgs/msg/Int32MultiArray': ([
    ], [
        ('layout', (2, 'std_msgs/msg/MultiArrayLayout')),
        ('data', (4, ((1, 'int32'), None))),
    ]),
    'std_msgs/msg/ColorRGBA': ([
    ], [
        ('r', (1, 'float32')),
        ('g', (1, 'float32')),
        ('b', (1, 'float32')),
        ('a', (1, 'float32')),
    ]),
    'std_msgs/msg/Bool': ([
    ], [
        ('data', (1, 'bool')),
    ]),
    'std_msgs/msg/UInt32': ([
    ], [
        ('data', (1, 'uint32')),
    ]),
    'std_msgs/msg/Int64MultiArray': ([
    ], [
        ('layout', (2, 'std_msgs/msg/MultiArrayLayout')),
        ('data', (4, ((1, 'int64'), None))),
    ]),
    'std_msgs/msg/Int32': ([
    ], [
        ('data', (1, 'int32')),
    ]),
    'std_msgs/msg/UInt16MultiArray': ([
    ], [
        ('layout', (2, 'std_msgs/msg/MultiArrayLayout')),
        ('data', (4, ((1, 'uint16'), None))),
    ]),
    'stereo_msgs/msg/DisparityImage': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('image', (2, 'sensor_msgs/msg/Image')),
        ('f', (1, 'float32')),
        ('t', (1, 'float32')),
        ('valid_window', (2, 'sensor_msgs/msg/RegionOfInterest')),
        ('min_disparity', (1, 'float32')),
        ('max_disparity', (1, 'float32')),
        ('delta_d', (1, 'float32')),
    ]),
    'tf2_msgs/msg/TF2Error': ([
        ('NO_ERROR', 'uint8', 0),
        ('LOOKUP_ERROR', 'uint8', 1),
        ('CONNECTIVITY_ERROR', 'uint8', 2),
        ('EXTRAPOLATION_ERROR', 'uint8', 3),
        ('INVALID_ARGUMENT_ERROR', 'uint8', 4),
        ('TIMEOUT_ERROR', 'uint8', 5),
        ('TRANSFORM_ERROR', 'uint8', 6),
    ], [
        ('error', (1, 'uint8')),
        ('error_string', (1, 'string')),
    ]),
    'tf2_msgs/msg/TFMessage': ([
    ], [
        ('transforms', (4, ((2, 'geometry_msgs/msg/TransformStamped'), None))),
    ]),
    'trajectory_msgs/msg/MultiDOFJointTrajectory': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('joint_names', (4, ((1, 'string'), None))),
        ('points', (4, ((2, 'trajectory_msgs/msg/MultiDOFJointTrajectoryPoint'), None))),
    ]),
    'trajectory_msgs/msg/JointTrajectory': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('joint_names', (4, ((1, 'string'), None))),
        ('points', (4, ((2, 'trajectory_msgs/msg/JointTrajectoryPoint'), None))),
    ]),
    'trajectory_msgs/msg/JointTrajectoryPoint': ([
    ], [
        ('positions', (4, ((1, 'float64'), None))),
        ('velocities', (4, ((1, 'float64'), None))),
        ('accelerations', (4, ((1, 'float64'), None))),
        ('effort', (4, ((1, 'float64'), None))),
        ('time_from_start', (2, 'builtin_interfaces/msg/Duration')),
    ]),
    'trajectory_msgs/msg/MultiDOFJointTrajectoryPoint': ([
    ], [
        ('transforms', (4, ((2, 'geometry_msgs/msg/Transform'), None))),
        ('velocities', (4, ((2, 'geometry_msgs/msg/Twist'), None))),
        ('accelerations', (4, ((2, 'geometry_msgs/msg/Twist'), None))),
        ('time_from_start', (2, 'builtin_interfaces/msg/Duration')),
    ]),
    'unique_identifier_msgs/msg/UUID': ([
    ], [
        ('uuid', (3, ((1, 'uint8'), 16))),
    ]),
    'visualization_msgs/msg/Marker': ([
        ('ARROW', 'int32', 0),
        ('CUBE', 'int32', 1),
        ('SPHERE', 'int32', 2),
        ('CYLINDER', 'int32', 3),
        ('LINE_STRIP', 'int32', 4),
        ('LINE_LIST', 'int32', 5),
        ('CUBE_LIST', 'int32', 6),
        ('SPHERE_LIST', 'int32', 7),
        ('POINTS', 'int32', 8),
        ('TEXT_VIEW_FACING', 'int32', 9),
        ('MESH_RESOURCE', 'int32', 10),
        ('TRIANGLE_LIST', 'int32', 11),
        ('ADD', 'int32', 0),
        ('MODIFY', 'int32', 0),
        ('DELETE', 'int32', 2),
        ('DELETEALL', 'int32', 3),
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('ns', (1, 'string')),
        ('id', (1, 'int32')),
        ('type', (1, 'int32')),
        ('action', (1, 'int32')),
        ('pose', (2, 'geometry_msgs/msg/Pose')),
        ('scale', (2, 'geometry_msgs/msg/Vector3')),
        ('color', (2, 'std_msgs/msg/ColorRGBA')),
        ('lifetime', (2, 'builtin_interfaces/msg/Duration')),
        ('frame_locked', (1, 'bool')),
        ('points', (4, ((2, 'geometry_msgs/msg/Point'), None))),
        ('colors', (4, ((2, 'std_msgs/msg/ColorRGBA'), None))),
        ('text', (1, 'string')),
        ('mesh_resource', (1, 'string')),
        ('mesh_use_embedded_materials', (1, 'bool')),
    ]),
    'visualization_msgs/msg/InteractiveMarkerInit': ([
    ], [
        ('server_id', (1, 'string')),
        ('seq_num', (1, 'uint64')),
        ('markers', (4, ((2, 'visualization_msgs/msg/InteractiveMarker'), None))),
    ]),
    'visualization_msgs/msg/MenuEntry': ([
        ('FEEDBACK', 'uint8', 0),
        ('ROSRUN', 'uint8', 1),
        ('ROSLAUNCH', 'uint8', 2),
    ], [
        ('id', (1, 'uint32')),
        ('parent_id', (1, 'uint32')),
        ('title', (1, 'string')),
        ('command', (1, 'string')),
        ('command_type', (1, 'uint8')),
    ]),
    'visualization_msgs/msg/MarkerArray': ([
    ], [
        ('markers', (4, ((2, 'visualization_msgs/msg/Marker'), None))),
    ]),
    'visualization_msgs/msg/InteractiveMarkerUpdate': ([
        ('KEEP_ALIVE', 'uint8', 0),
        ('UPDATE', 'uint8', 1),
    ], [
        ('server_id', (1, 'string')),
        ('seq_num', (1, 'uint64')),
        ('type', (1, 'uint8')),
        ('markers', (4, ((2, 'visualization_msgs/msg/InteractiveMarker'), None))),
        ('poses', (4, ((2, 'visualization_msgs/msg/InteractiveMarkerPose'), None))),
        ('erases', (4, ((1, 'string'), None))),
    ]),
    'visualization_msgs/msg/InteractiveMarker': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('pose', (2, 'geometry_msgs/msg/Pose')),
        ('name', (1, 'string')),
        ('description', (1, 'string')),
        ('scale', (1, 'float32')),
        ('menu_entries', (4, ((2, 'visualization_msgs/msg/MenuEntry'), None))),
        ('controls', (4, ((2, 'visualization_msgs/msg/InteractiveMarkerControl'), None))),
    ]),
    'visualization_msgs/msg/InteractiveMarkerFeedback': ([
        ('KEEP_ALIVE', 'uint8', 0),
        ('POSE_UPDATE', 'uint8', 1),
        ('MENU_SELECT', 'uint8', 2),
        ('BUTTON_CLICK', 'uint8', 3),
        ('MOUSE_DOWN', 'uint8', 4),
        ('MOUSE_UP', 'uint8', 5),
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('client_id', (1, 'string')),
        ('marker_name', (1, 'string')),
        ('control_name', (1, 'string')),
        ('event_type', (1, 'uint8')),
        ('pose', (2, 'geometry_msgs/msg/Pose')),
        ('menu_entry_id', (1, 'uint32')),
        ('mouse_point', (2, 'geometry_msgs/msg/Point')),
        ('mouse_point_valid', (1, 'bool')),
    ]),
    'visualization_msgs/msg/ImageMarker': ([
        ('CIRCLE', 'int32', 0),
        ('LINE_STRIP', 'int32', 1),
        ('LINE_LIST', 'int32', 2),
        ('POLYGON', 'int32', 3),
        ('POINTS', 'int32', 4),
        ('ADD', 'int32', 0),
        ('REMOVE', 'int32', 1),
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('ns', (1, 'string')),
        ('id', (1, 'int32')),
        ('type', (1, 'int32')),
        ('action', (1, 'int32')),
        ('position', (2, 'geometry_msgs/msg/Point')),
        ('scale', (1, 'float32')),
        ('outline_color', (2, 'std_msgs/msg/ColorRGBA')),
        ('filled', (1, 'uint8')),
        ('fill_color', (2, 'std_msgs/msg/ColorRGBA')),
        ('lifetime', (2, 'builtin_interfaces/msg/Duration')),
        ('points', (4, ((2, 'geometry_msgs/msg/Point'), None))),
        ('outline_colors', (4, ((2, 'std_msgs/msg/ColorRGBA'), None))),
    ]),
    'visualization_msgs/msg/InteractiveMarkerControl': ([
        ('INHERIT', 'uint8', 0),
        ('FIXED', 'uint8', 1),
        ('VIEW_FACING', 'uint8', 2),
        ('NONE', 'uint8', 0),
        ('MENU', 'uint8', 1),
        ('BUTTON', 'uint8', 2),
        ('MOVE_AXIS', 'uint8', 3),
        ('MOVE_PLANE', 'uint8', 4),
        ('ROTATE_AXIS', 'uint8', 5),
        ('MOVE_ROTATE', 'uint8', 6),
        ('MOVE_3D', 'uint8', 7),
        ('ROTATE_3D', 'uint8', 8),
        ('MOVE_ROTATE_3D', 'uint8', 9),
    ], [
        ('name', (1, 'string')),
        ('orientation', (2, 'geometry_msgs/msg/Quaternion')),
        ('orientation_mode', (1, 'uint8')),
        ('interaction_mode', (1, 'uint8')),
        ('always_visible', (1, 'bool')),
        ('markers', (4, ((2, 'visualization_msgs/msg/Marker'), None))),
        ('independent_marker_orientation', (1, 'bool')),
        ('description', (1, 'string')),
    ]),
    'visualization_msgs/msg/InteractiveMarkerPose': ([
    ], [
        ('header', (2, 'std_msgs/msg/Header')),
        ('pose', (2, 'geometry_msgs/msg/Pose')),
        ('name', (1, 'string')),
    ]),
}
