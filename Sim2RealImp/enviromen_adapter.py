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

from PolicyController import PolicyController
from Utils import EnvState
from IRobot import IRobot

class EnviromentAdapter(ABC):

    def __init__(self, action_scale : np.ndarray, _action_size: int, model_path: str, frecuency: int = 125, robot : IRobot.IRobot):
        self.controlador = PolicyController()
        self.model_dir = model_path
        self.controlador.load_policy(
            self.model_path / "policy.pt",
            self.model_path / "env.yaml")
        self._action_scale = action_scale
        self._policy_counter = 0
        self._previous_action = np.zeros(_action_size)

        self.robot = robot

        self.frecuency = frecuency

        self.has_joint_data = False
    
    @abstracmethod 
    def _compute_observation(self, state: EnvState) -> np.ndarray:
        pass

    @abstracmethod
    def _update_state(self):
        pass 
    

    def step(self):
        self._update_state()
        self.obs=self._compute_observation()
        pass
    

    