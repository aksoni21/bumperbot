import rclpy
from rclpy.node import Node
from rcl_interfaces import SetParametersResult
from rclpy.parameter import Parameter


class SimpleParameter(Node):
    def __init__(self):
        super().__init__('simple_parameter')
        self.declare_parameter('simple_int_param', 28)
        self.declare_parameter('simple_string_param', "Ankur")
        
        self.add_on_set_parameters_callback('self.paramChangeCallback')#executed when parameter is changed during runtime
        
    def add_on_set_parameters_callback(self, params):
        result = SetParametersResult()
        
        for param in params:
            if param.name == 'simple_int_param' and param.type == Parameter.Type.INTEGER:
                self.get_logger('simple_int_param changed to %d' % param.value)
                result.successful = True
            elif param.name == 'simple_string_param' and param.type == Parameter.Type.STRING:
                self.get_logger('simple_string_param changed to %s' % param.value)
                result.successful=True
        
        return result

def main():
    rclpy.init()
    node = SimpleParameter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()