"""Launch iiwa bringup and the KDL trajectory node with matching interfaces."""

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def _launch_setup(context):
    cmd_interface = LaunchConfiguration('cmd_interface').perform(context)
    traj_type = LaunchConfiguration('traj_type').perform(context)
    s_type = LaunchConfiguration('s_type').perform(context)

    # Position mode intentionally preserves iiwa.launch.py's own defaults.
    bringup_arguments = {}
    if cmd_interface in ('velocity', 'effort'):
        bringup_arguments = {
            'command_interface': cmd_interface,
            'robot_controller': f'{cmd_interface}_controller',
        }
    if cmd_interface == 'effort':
        bringup_arguments['use_sim'] = 'true'    

    bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('iiwa_bringup'),
                'launch',
                'iiwa.launch.py',
            )
        ),
        launch_arguments=bringup_arguments.items(),
    )

    params_file_arg = DeclareLaunchArgument(
        "params_file",
        default_value=PathJoinSubstitution([
            FindPackageShare("ros2_kdl_package"),
            "config",
            "kdl_param.yaml",
        ]),
        description="YAML with node parameters"
    )

    kdl_node = Node(
        package='ros2_kdl_package',
        executable='ros2_kdl_node',
        output='screen',
        parameters=[
            LaunchConfiguration("params_file"),
            {'cmd_interface': cmd_interface,
            'traj_type': traj_type,
            's_type': s_type,
        }],
    )

    return [bringup, params_file_arg, kdl_node]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'cmd_interface',
            default_value='position',
            choices=['position', 'velocity', 'effort'],
            description='Command interface shared by iiwa and the KDL node.',
        ),
        DeclareLaunchArgument(
            'traj_type',
            default_value='linear',
            choices=['linear', 'circular'],
            description='Geometric trajectory type.',
        ),
        DeclareLaunchArgument(
            's_type',
            default_value='trapezoidal',
            choices=['trapezoidal', 'cubic'],
            description='Trajectory time-scaling profile.',
        ),
        OpaqueFunction(function=_launch_setup),
    ])
