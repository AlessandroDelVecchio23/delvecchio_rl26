import rclpy
from rclpy.node import Node

from distance_interfaces.msg import DistanceReading


class DistanceMonitor(Node):
    def __init__(self):
        super().__init__('distance_monitor')

        self.declare_parameter('threshold_m', 0.8)
        self.threshold_m = self.get_parameter('threshold_m').value

        self.subscription = self.create_subscription(
            DistanceReading,
            'distance_readings',
            self.on_reading,
            10,
        )

    def on_reading(self, reading):
        if reading.distance_m < self.threshold_m:
            self.get_logger().warn(
                f'Ostacolo vicino! Lettura {reading.sample_id}: '
                f'{reading.distance_m:.2f} m'
            )
        else:
            self.get_logger().info(
                f'Lettura {reading.sample_id}: '
                f'{reading.distance_m:.2f} m — distanza sicura'
            )


def main(args=None):
    rclpy.init(args=args)
    node = DistanceMonitor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()