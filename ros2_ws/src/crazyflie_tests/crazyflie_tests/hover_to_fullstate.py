#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node

from crazyflie_interfaces.msg import FullState, Hover
from geometry_msgs.msg import Quaternion


def angle_normalize(a: float) -> float:
    return math.atan2(math.sin(a), math.cos(a))


class HoverToFullState(Node):

    class State:
        def __init__(self):
            self.x: float = 0.0
            self.y: float = 0.0
            self.z: float = 0.5
            self.yaw: float = 0.0

    def __init__(self):
        super().__init__('hover_to_fullstate')

        # crazyflie id paramter
        self.declare_parameter('cf_id', 1)
        self.cf_id = (
            self.get_parameter('cf_id')
            .get_parameter_value()
            .integer_value
        )

        self.topic_hover = f'/cf{self.cf_id}/cmd_hover'
        self.topic_fullstate = f'/cf{self.cf_id}/cmd_full_state'

        # internal state
        self.state = self.State()
        self.last_hover = Hover()

        # limits
        self.x_limit = (-5.0, 5.0)
        self.y_limit = (-5.0, 5.0)
        self.z_limit = (0.0, 2.0)

        # ros2 interfaces
        self.create_subscription(
            Hover,
            self.topic_hover,
            self.hover_callback,
            10
        )

        self.pub = self.create_publisher(
            FullState,
            self.topic_fullstate,
            10
        )

        # periodic publishing
        self.DT = 0.05
        self.timer = self.create_timer(self.DT, self.timer_callback)

        self.get_logger().info(f'Subscribing: {self.topic_hover}')
        self.get_logger().info(f'Publishing: {self.topic_fullstate}')

    # ----------- Callbacks ------------

    def hover_callback(self, msg: Hover):
        self.last_hover = msg

    def timer_callback(self):
        prev_x = self.state.x
        prev_y = self.state.y
        prev_z = self.state.z

        self.state.x = max(
            min(self.state.x + self.last_hover.vx * self.DT, self.x_limit[1]),
            self.x_limit[0]
        )

        self.state.y = max(
            min(self.state.y + self.last_hover.vy * self.DT, self.y_limit[1]),
            self.y_limit[0]
        )

        self.state.z = max(
            min(self.last_hover.z_distance, self.z_limit[1]),
            self.z_limit[0]
        )

        self.state.yaw = angle_normalize(
            self.state.yaw + self.last_hover.yaw_rate * self.DT
        )

        msg = FullState()

        msg.pose.position.x = self.state.x
        msg.pose.position.y = self.state.y
        msg.pose.position.z = self.state.z

        msg.twist.linear.x = (self.state.x - prev_x) / self.DT
        msg.twist.linear.y = (self.state.y - prev_y) / self.DT
        msg.twist.linear.z = (self.state.z - prev_z) / self.DT

        msg.acc.x = 0.0
        msg.acc.y = 0.0
        msg.acc.z = 0.0

        # yaw → quaternion
        q = Quaternion()
        q.w = math.cos(self.state.yaw / 2.0)
        q.x = 0.0
        q.y = 0.0
        q.z = math.sin(self.state.yaw / 2.0)

        msg.pose.orientation = q

        msg.twist.angular.x = 0.0
        msg.twist.angular.y = 0.0
        msg.twist.angular.z = self.last_hover.yaw_rate

        self.pub.publish(msg)


def main():
    rclpy.init()
    node = HoverToFullState()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

