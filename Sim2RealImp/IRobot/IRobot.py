"""
IRobot.py

Interfaz del robot a implementar en Sim2Real. Su objetivo es definir los ditintos métodos que debe tener un robot, asi como una configuración básica.
- Constructor: Configuración inicial, conexión con puertos, obtener raiz del robot 
- Obtener estado del robot: posición de las articulaciones, velocidad, etc.
- Mandar acción al robot: mandar las posiciones o par que debe tomar el robot.

Autor: Enrique de Antonio
"""
from abc import ABC, abstracmethod
from Utils.dataclasses import RobotState

class IRobot(ABC):
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
    
    @abstractmethod
    def get_state(self) -> RobotState:
        pass
    
    @abstractmethod
    def send_action(self) -> int:
        pass

    @abstractmethod
    def disconnect(self) -> int:
        pass