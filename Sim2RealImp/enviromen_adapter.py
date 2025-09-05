"""
enviromen_adapter.py
---
Manejador principal del entorno a implementar mediante la política.

Esta clase tiene dos clases principales asignadas:
    PolicyController : Se encarga de manejar todo lo relacionado con la política. Desde cargarla y obtener los para-
    metros principales de la simulación hasta recibir las observaciones y computar la acción.
    IRobot : Clase a través de la cual se comunica con el robot, obteniendo las observaciones pertientes del robot
    y mandar las acciones generadas.

Además, para completar las observaciones se usará una clase observation hub, la cual tendrá asociada una serie de 
sensores para recibir el resto de inputs necesarios.

Autor: Enrique de Antonio
"""

import numpy as np
import PolicyController as pc
import IRobot as r
import ObservationHub as oh

class EnviromentAdapter:
    def __init__(self):
        pass
    _compute_observation(self) -> NotImplementedError:
        raise NotImplementedError ("_compute_observation debe ser implementada en la clase específica de 
            cada entorno")
    def step  (self, action: np.array) -> np.array
        pass
    