import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from pathlib import Path

from launch_ros.actions import Node

def generate_launch_description():


    package_name='my_robot_description'
    world_name = DeclareLaunchArgument("world_name", default_value="simple_building.world")

    gz_resource_path = SetEnvironmentVariable(name='GAZEBO_MODEL_PATH', value=[
                                EnvironmentVariable('GAZEBO_MODEL_PATH', default_value=''),
                                '/usr/share/gazebo-11/models/:',
                                str(Path(get_package_share_directory('my_robot_description')).parent.resolve()),
                                ':',
                                str(Path(get_package_share_directory('my_robot_description')).parent.resolve()) + "/my_robot_description/models",
                    ])
     

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','upload.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={
                        "world": PathJoinSubstitution([
                                    FindPackageShare('my_robot_description'),
                                    'worlds',
                                    LaunchConfiguration('world_name'),
                ])}.items()
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot'],
                        output='screen')

    twist_mux_params = os.path.join(get_package_share_directory(package_name),'config','twist_mux.yaml')
    twist_mux = Node(
            package="twist_mux",
            executable="twist_mux",
            parameters=[twist_mux_params, {'use_sim_time': True}],
            remappings=[('/cmd_vel_out','/diff_cont/cmd_vel_unstamped')]
        )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )


    # Launch them all!
    return LaunchDescription([
        world_name,
        gz_resource_path,
        rsp,
        gazebo,
        spawn_entity,
        twist_mux,
        diff_drive_spawner,
        joint_broad_spawner
    ])