#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Get the package directory
    pkg_anymal_b = FindPackageShare('anymal_b_simple_description')
    
    # Path to RViz config
    rviz_config_file = PathJoinSubstitution([
        pkg_anymal_b,
        'config',
        'rviz',
        'standalone.rviz'
    ])
    
    # Declare arguments
    use_gui = LaunchConfiguration('use_gui', default='true')
    
    # Load URDF file
    # Resolve the path at launch time
    urdf_path = os.path.join(
        get_package_share_directory('anymal_b_simple_description'),
        'urdf',
        'anymal.urdf'
    )
    
    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()
    
    # Robot State Publisher node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_desc
        }]
    )
    
    # Joint State Publisher GUI node
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen',
        condition=IfCondition(use_gui)
    )
    
    # RViz node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]
    )
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_gui',
            default_value='true',
            description='Use joint state publisher GUI'
        ),
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])

