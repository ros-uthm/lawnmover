import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro
from os.path import join

def generate_launch_description():

    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg_ros_gz_rbot = get_package_share_directory('lawnmover')


    robot_description_file = os.path.join(pkg_ros_gz_rbot, 'urdf', 'Robotic.xacro')
    ros_gz_bridge_config = os.path.join(pkg_ros_gz_rbot, 'config', 'ros_gz_bridge_gazebo.yaml')
    rviz_config_file = os.path.join(pkg_ros_gz_rbot, 'config', 'gazebo.rviz')

    rviz_arg = DeclareLaunchArgument(
        name='rviz',
        default_value='false'
    )
    show_rviz = LaunchConfiguration('rviz')
    
    robot_description_config = xacro.process_file(robot_description_file)
    robot_description = {'robot_description': robot_description_config.toxml()}

   
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description, {'use_sim_time': True}],
    )

   
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(join(pkg_ros_gz_sim, "launch", "gz_sim.launch.py")),
        launch_arguments={"gz_args": "-r -v 4 empty.sdf"}.items()
    )

    spawn_robot = TimerAction(
        period=5.0,  
        actions=[Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                "-topic", "/robot_description",
                "-name", "autonomous_lawn_mower",
                "-allow_renaming", "false",  # prevents "_1" duplicate
                "-x", "0.0",
                "-y", "0.0",
                "-z", "0.32",
                "-Y", "0.0"
            ],
            output='screen'
        )]
    )

    ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': ros_gz_bridge_config}],
        output='screen'
    )

    rviz_node = Node(
        condition=IfCondition(show_rviz),
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen',
        parameters=[{'use_sim_time': True}],
    )

    joint_state_broadcaster = TimerAction(
        period=8.0,
        actions=[
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=["joint_state_broadcaster"],
                output="screen",
            )
        ]
    )

    diff_drive_controller = TimerAction(
        period=10.0,
        actions=[
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=["diff_drive_controller"],
                output="screen",
            )
        ]
    )

    return LaunchDescription([
        rviz_arg,
        robot_state_publisher,
        gazebo,
        spawn_robot,
        ros_gz_bridge,
        joint_state_broadcaster,
        diff_drive_controller,
        rviz_node,
    ])	
        	 
