import rclpy
from rclpy.node import Node

from distance_interfaces.msg import DistanceReading


class DistancePublisher(Node):
    def __init__(self):
        super().__init__('distance_publisher')

        # Per dichiarare i parametri del nodo
        self.declare_parameter('frequency_hz', 1.0)
        frequency_hz = self.get_parameter('frequency_hz').value
        if frequency_hz <= 0:
            raise ValueError('frequency_hz deve essere maggiore di zero')

        # Inviamo la lettura sul topic distance_reading, utilizzando il tipo DistanceReading
        self.publisher = self.create_publisher(
            DistanceReading, 'distance_readings', 10
        )
        self.sample_id = 0
        self.timer = self.create_timer(
            1.0 / frequency_hz, self.publish_reading
        )

    def publish_reading(self):
        reading = DistanceReading()
        reading.sample_id = self.sample_id
        # Simulazione di una misurazione che parte da 2.0 e arriva a 0.2
        reading.distance_m = 2.0 - 0.2 * (self.sample_id % 10)

        self.publisher.publish(reading)
        self.get_logger().info(
            f'Lettura {reading.sample_id}: {reading.distance_m:.2f} m'
        )
        self.sample_id += 1


def main(args=None):
    rclpy.init(args=args)
    node = DistancePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()