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

from abc import ABC, abstracmethod


class EnviromentAdapter(ABC):
    def __init__(self):
        pass
    
    @abstracmethod
    def _compute_observation(self):
        pass
    
    @abstracmethod 
    def step(self):
        pass
    

    