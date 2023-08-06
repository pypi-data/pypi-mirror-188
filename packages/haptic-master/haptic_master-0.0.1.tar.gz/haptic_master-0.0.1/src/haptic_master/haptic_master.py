import socket
from typing import Tuple
from .spring import Spring
from .damper import Damper
from .bias_force import BiasForce


class HapticMaster:
    def __init__(self, ip: str, port: int, inertia_value: float) -> None:
        self._ip = ip
        self._port = port
        self._inertia = inertia_value
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    @property
    def address(self) -> Tuple[str, int]:
        return (self._ip, self._port)

    @property
    def inertia(self) -> float:
        return self._inertia

    @inertia.setter
    def inertia(self, new_inertia: float):
        self._inertia = new_inertia
        msg = 'set inertia ' + str(new_inertia)
        print(self.send_message(msg))
    
    def connect(self):
        try:
            # Connect to the robot
            self._socket.connect((self._ip, self._port))

            # Set the inertia
            self.inertia = self._inertia
        except socket.error:
            print('Connection error')

    def set_state(self, device_state):
        if device_state in ['init', 'off', 'force', 'position', 'home']:
            msg = 'set state ' + device_state
            return self.send_message(msg)
        else:
            raise ValueError('Wrong state name is given')

    def disconnect(self):
        # Clear all haptic effects
        msg = 'remove all'
        print(self.send_message(msg))

        # Close connection
        self._socket.close()

    def send_message(self, msg: str) -> str:
        self._socket.sendall(bytearray(self._hapticMaster_message(msg)))

        return self._hapticMaster_response(self._socket.recv(1024))

    def create_spring(self, spring: Spring) -> None:
        # Create the spring with the given name
        msg = 'create spring ' + spring.name
        print(self.send_message(msg))

        # Set the initial position of the spring
        msg = 'set ' + spring.name + ' pos ' + str(list(spring.position)).replace(' ', '')
        print(self.send_message(msg))

        # Set the spring constant
        msg = 'set ' + spring.name + ' stiffness ' + str(spring.stiffness)
        print(self.send_message(msg))

        # Set direction of the spring
        msg = 'set ' + spring.name + ' direction ' + str(list(spring.direction)).replace(' ', '')
        print(self.send_message(msg))

        # Set damping factor of the spring
        msg = 'set ' + spring.name + ' dampfactor ' + str(spring.damp_factor)
        print(self.send_message(msg))

        # Set the maximum spring force
        msg = 'set ' + spring.name + ' maxforce ' + str(spring.damp_factor)
        print(self.send_message(msg))

        # Enable the spring
        msg = 'set ' + spring.name + ' enable'
        print(self.send_message(msg))

    def create_damper(self, damper: Damper):
        # Create the damper with the given name
        msg = 'create damper ' + damper.name
        print(self.send_message(msg))

        # Set the damping coefficients
        msg = 'set ' + damper.name + ' dampcoef ' + str(list(damper.damping)).replace(' ', '')
        print(self.send_message(msg))

        # Enable the damper
        msg = 'set ' + damper.name + ' enable'
        print(self.send_message(msg))

    def create_bias_force(self, force: BiasForce):
        # Create the bias force with the given name
        msg = 'create biasforce ' + force.name
        print(self.send_message(msg))

        # Set the value of the bias force
        msg = 'set ' + force.name + ' force ' + str(list(force.force)).replace(' ', '')
        print(self.send_message(msg))

        # Enable the bias force
        msg = 'set ' + force.name + ' enable'
        print(self.send_message(msg))

    def move_spring(self, spring: Spring, new_position):
        # Update the spring position
        spring.position = new_position

        # Move the spring
        msg = 'set ' + spring.name + ' pos ' + str(list(spring.position)).replace(' ', '')
        print(msg)
        print(self.send_message(msg))
    
    def _hapticMaster_message(self, msg):
        hm_msg = [0, 0, 0, 0, 0, 0, 0, 0]
        
        # Convert msg to ascii dec
        decimal_msg = [ord(c) for c in msg]
        
        hm_msg[3] = len(decimal_msg)
        
        return hm_msg + decimal_msg

    def _hapticMaster_response(self, msg):
        # Decode the response from the server
        msg_str = msg.decode('utf-8')

        # Check if the response conveys error message
        if 'ERROR' in msg_str:
            raise ValueError(msg_str)
        else:
            # Check if the response is a vector
            if '$' in msg_str:
                return [float(s) for s in msg_str[msg_str.find('[')+1:msg_str.find(']')].split(',')]
            else:
                return "INFO: " + msg_str.replace('"', '')

    def getPosition(self) -> list:
        msg = 'get measpos'
        
        return self.send_message(msg)

    def getVelocity(self) -> list:
        msg = 'get modelvel'

        return self.send_message(msg)

    def getForce(self) -> list:
        msg = 'get measforce'

        return self.send_message(msg)
