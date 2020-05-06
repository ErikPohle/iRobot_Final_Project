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
	
Particle shooter plugin - Topic: "/particle_shooter"

	- message example: rostopic pub -1 /particle_shooter geometry_msgs/Pose '{position:  {x: 0.3, y: 0.3, z: 0.3}, orientation: {x: 0,y: 0,z: 1000}}'
	
	- postion: particle position {x_origin, y_origin, z_axis_force}
	
	- orientation: forces applied to the particle to be shoot {x_axis_force, y_axis_force, z_axis_force}
