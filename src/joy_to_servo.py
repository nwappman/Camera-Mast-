import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import Int32

class JoyToRover(Node):
    def __init__(self):
        super().__init__('joy_to_rover')
        self.subscription = self.create_subscription(Joy, 'joy', self.joy_callback, 10)
        self.servo_pub = self.create_publisher(Int32, 'servo_angle', 10)
        self.stepper_pub = self.create_publisher(Int32, 'stepper_speed', 10)
        
        self.target_angle = 135
        self.target_speed = 0
        
        # 20Hz Heartbeat to prevent ESP32 buffer overflow
        self.timer = self.create_timer(0.05, self.timer_callback)

    def joy_callback(self, msg):
        # Right Stick Up/Down (Axis 4) -> Servo (0 to 270)
        self.target_angle = int(((msg.axes[4] + 1.0) / 2.0) * 270.0)
        
        # Right Stick Left/Right (Axis 3) -> Stepper Speed (-1000 to 1000)
        # We multiply by 1000 to get a meaningful step rate
        self.target_speed = int(msg.axes[3] * 1000)

    def timer_callback(self):
        # Publish Servo Angle
        s_msg = Int32()
        s_msg.data = self.target_angle
        self.servo_pub.publish(s_msg)
        
        # Publish Stepper Speed
        st_msg = Int32()
        st_msg.data = self.target_speed
        self.stepper_pub.publish(st_msg)

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(JoyToRover())
    rclpy.shutdown()

if __name__ == '__main__':
    main()

   