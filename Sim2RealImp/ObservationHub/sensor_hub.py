"""
SensorHub: Clase para la creación de la conexión con los sensores. En este caso al
ser puramente para el ensayo de pruebas vamos a realizar una clase básica para generar
puntos en el espacio

""""

import numpy as np

class SensorHub:

    def __init__(self):
        pass

    @staticmethod
    def object_position_test(self):
        object_position = np.array([10, 10, 10])
        return object_position
    
    @staticmethod
   def tool_position_test(self):
        tool_position = np.array([10, 10, 10])
        return tool_position
    
        