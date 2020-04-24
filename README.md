# Topic To Publish To:
Robot Movement (Make robot move) - Topic: "/move_base_simple/goal"

source /home/[user]/catkin_ws/devel/setup.bash
	- if it tells you that such and such isn't a launch file

export TURTLEBOT3_MODEL=[burger/waffle/waffle_pi]
	- if it says that model isn't set

roslaunch turtlebot3_gazebo turtlebot3_world.launch
	- to launch turtlebot in gazebo

roslaunch turtlebot3_navigation turtelbot3_navigation.launch
	- to launch the navigation stack for turtlebot