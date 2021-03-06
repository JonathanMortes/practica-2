#!/usr/bin/env python

import rospy
import roslib
import sys
import cv2
import numpy as np

from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib import SimpleActionClient

from tf import transformations

class Planning:

    def __init__(self):
        self.client = SimpleActionClient('/move_base', MoveBaseAction)
        self.goal = MoveBaseGoal()
        
        self.current_goal = 'home'
        self.goals = {'home': np.array([0.0,0.0]), 
                      'pos1': np.array([1.0,0.0]),
                      'pos2': np.array([1.0,1.0]),}
    
    def sendGoal(self,x_pos,y_pos,yaw):
        if abs(x_pos) <= 0.1:
            x_pos = 0.0
        if abs(y_pos) <= 0.1:
            y_pos = 0.0
        
#        quaternion = transformations.quaternion_from_euler(0, 0, yaw)
        
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        
        goal.target_pose.pose.position.x = x_pos
        goal.target_pose.pose.position.y = y_pos
        goal.target_pose.pose.position.z = 0.0
#        goal.target_pose.pose.orientation.x = quaternion[0]
#        goal.target_pose.pose.orientation.y = quaternion[1]
#        goal.target_pose.pose.orientation.z = quaternion[2]
        goal.target_pose.pose.orientation.w = 1.0 #quaternion[3]
        
        self.client.send_goal(goal)
        self.client.wait_for_result()
        print('Reached ' + self.current_goal)
        print(self.client.get_result())
            
    def computeNewGoal(self):
        if self.current_goal == 'pos2':
            self.current_goal = 'home'
        
        elif self.current_goal == 'pos1':
            self.current_goal = 'pos2'
        
        elif self.current_goal == 'home':
            self.current_goal = 'pos1'
        
        else:
            self.current_goal = 'home'
        
        self.sendGoal(self.goals[self.current_goal][0],self.goals[self.current_goal][1],0)
    
    def loop(self,rate):
        self.sendGoal(self.goals['home'][0],self.goals['home'][1],0)
        
        
        while not rospy.is_shutdown():
            self.computeNewGoal()
            rate.sleep()
    
def main():
    """
    Main function
    """
    rospy.init_node('planning_node', anonymous=True)
    rate = rospy.Rate(1) # 2hz
    plan = Planning()
    
    try:
        plan.client.wait_for_server()
        plan.loop(rate)
        
    except KeyboardInterrupt:
        print("Shutting down")
        pass  
    except rospy.ROSInterruptException:
        print("Shutting down")
        pass  

if __name__ == '__main__':
    main()
