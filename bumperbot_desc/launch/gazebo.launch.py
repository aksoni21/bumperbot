from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, ExecuteProcess
import os
from os import pathsep
from ament_index_python.packages import get_package_share_directory, get_package_prefix
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    bumperbot_desc = get_package_share_directory("bumperbot_desc")
    bumperbot_desc_prefix = get_package_prefix("bumperbot_desc")

    model_path = os.path.join(bumperbot_desc, "models")
    model_path += pathsep + os.path.join(bumperbot_desc_prefix, "share")

    env_var = SetEnvironmentVariable("GAZEBO_MODEL_PATH", model_path)

    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(
            bumperbot_desc, "urdf", "bumperbot.urdf.xacro"),
        description="Absolute path to robot URDF file"
    )

    robot_desc = ParameterValue(
        Command(["xacro ", LaunchConfiguration("model")]), value_type=str)

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_desc}]
    )

    start_gazebo_server_cmd = ExecuteProcess(
        cmd=[
            'gzserver',
            '-s',
            'libgazebo_ros_init.so',
            '-s',
            'libgazebo_ros_factory.so',
            # '--verbose',

        ],
        output='screen',
    )
    start_gazebo_client_cmd = ExecuteProcess(
        cmd=[
            'gzclient',
            '-s',
            'libgazebo_ros_init.so',
            '-s',
            'libgazebo_ros_factory.so',
            # '--verbose',

        ],
        output='screen',
        # arguments=[os.path.join(get_package_prefix("my_robot_bringup"), "share","my_world.world")],
    )

    spawn_robot = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-entity", "bumperbot", "-topic", "robot_description"],
        output="screen"
    )

    return LaunchDescription([
        env_var,
        model_arg,
        robot_state_publisher,
        start_gazebo_server_cmd,
        start_gazebo_client_cmd,
        spawn_robot,
    ])
