# 2nd practical exercise
This repository containt the files related with the 2nd practical exercise of the Multi-Robot Systems, a subject of the 4th year from the Robotics Engineering Degree of the University of Alicante.

# Simulation
The final purpose is to implement multi-robot behaviours using Turtlebots robots. Our first goal is to archive a computer vision based leader-follower behavior. To archieve this, so far we have designed a **3D simulation** using ROS and Gazebo in which two Turtlebots are launched in an empty world, with their models modified so that they are equiped with a UST-10 LIDAR, an Orbbec Astra RGB-D camera and a green plate on their back. This way, they will be mostly identical to the devices we use in our laboratory:

![Basic simulation](https://github.com/sistemas-multirobot-grupo-2/practica-2/blob/master/multimedia/plain_simulation.png "Basic simulation")

This can be launched by adding our *turtlebot* folder in the *src* directory of a catkin workspace in a machine with a functional ROS installation by executing:
```bash
roslaunch a_multirob create_multi_robot.launch
```

For some tests, it might be useful to move the robot around using the terminal. This can be done by executing the following command (using "robot1" or "robot2" at the beggining of the topic to choose which robot to move):
```bash
rostopic pub -r 10 /robot2/mobile_base/commands/velocity geometry_msgs/Twist '{linear:  {x: 0.1, y: 0.0, z: 0.0}, angular: {x: 0.0,y: 0.0,z: 0.0}}'
```


# Perception
In order to launch the ***perception node***, it is necessary to use the *perception* package. The order to run it is:
```bash
rosrun perception perception
```
This node takes the images published in the */robot2/camera/rgb/image_raw* topic and gets the bounding box and centroid of the biggest green area on the frame. Now, it displays it in a window and publish relevant perception data in a topic (***/perception_data***, using the *perception/perception_data* custom message, which contains the **centroid and bounding box** coordinates of the biggest green area detected, this **area** and a measure of how much should a subscriber **trust** this data, between 0 and 100).

![Perception node](https://github.com/sistemas-multirobot-grupo-2/practica-2/blob/master/multimedia/perception.png "Perception node")

The ***perception_tester*** node can be used to test if everything is being properly published by the *perception* one. It prints in the default output device (screen) the data published by the *perception* node. The order to run it is:
```bash
rosrun perception perception_tester
```
