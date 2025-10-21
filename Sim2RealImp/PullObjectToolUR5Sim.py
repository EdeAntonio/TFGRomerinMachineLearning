"""
PullObjectToolUR5Sim.py

Clase heredada de EnviromentAdapter. Especifica dicha clase para el problema de
arrastre de objeto con herramienta.
"""

import numpy as np

from . import EnviromentAdapter 

from ObservationHub import SensorHub
from IRobot import UR5Sim

import argparse
parser = argparse.ArgumentParser(description="Sim2Real: Ejercicio de arrastre objeto con herramienta.")
parser.add_argument("--policy_path", type=str, default=None, help="Direccion de la carpeta con la política y la configuración.")
args  = parser.parse_args()

class POTUR5Sim (EnviromentAdapter):
    def __init__(self):
        super.__init__(action_scale = 0.5, _action_size = 6, model_path=args.policy_path, robot = IRobot.UR5Sim("127.0.0.1", 30004))
        self.default_pos: np.ndarray = np.zeros(6)
    def _update_state(self):
        self.state.robot = self.robot.get_state()
        if self.state.robot == None:
            print("Problemas con el estado del Robot. Estado vacío...\n")
        self.state.object_pos = SensorHub.object_position_test()
        self.state.tool_pos = SensorHub.tool_position_test()

    def _compute_observation(self) -> np.ndarray:
        obs = np.zeros(37)
        obs[:8] = self.current_joint_position - self.robot.default_pos
        obs[8:16] = self.state.robot.current_joint_velocities
        obs[16:19] = self.state.tool_pos
        obs[19:22] = self.state.object_pos
        obs[22:29] = self.target_command
        obs[29:37] = self._previous_action
        return obs

    def _compute_action(self, obs : np.ndarray) -> np.ndarray:
        action = self.controlador._compute_action(obs)
        return action[:6]

    