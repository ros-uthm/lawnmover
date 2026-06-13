from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    # 1. Locate your package directory
    pkg_description = get_package_share_directory('lawnmover')
    
    # 2. Path to your main XACRO file instead of a raw URDF
    xacro_file = os.path.join(pkg_description, 'urdf', 'Robotic.xacro')
    
    # Process the xacro file into standard URDF string data
    robot_description_config = xacro.process_file(xacro_file)
    robot_desc = robot_description_config.toxml()

    # 3. Robot State Publisher Node
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    # 4. Include the Gazebo simulator launch file
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': 'empty.sdf -r'}.items()
    )

    # 5. Spawn Entity Node
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', '/robot_description',
            '-name', 'autonomous_lawn_mower',
            '-z', '0.3'
        ],
        output='screen'
    )

    ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
        ],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher,
        gazebo,
        spawn_robot,
        ros_gz_bridge
    ])
