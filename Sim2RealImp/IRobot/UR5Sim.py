"""
UR5SimPullTool.py

Interfaz para el control simulado del UR5. 
- Conexión a polyscope
- Recepción observaciones relacionadas con el robot
- Directrices para el robot

Autor: Enrique de Antonio
"""
import sys
sys.path.append("..")

import rtde.rtde as rtde
import rtde.rtde_config as rtde_config

import numpy as np

from . import IRobot as ir
from Utils import data

class UR5Sim(ir.IRobot):
    def __init__(self, ip: str, port: int):
        
        # Asignación de variables iniciales
        super().__init__(ip, port)
        self.default_pos = (0,0,0,0,0,0) #actualizar con valor inicial. Ver en código original.
        
        # Nombre del archivo con la configuración del RTDE
        self.config_filename = "UR5Sim_config.xml"

        # Extracción de valores relevantes del fichero
        self.conf = rtde_config.ConfigFile(self.config_filename)
        state_names, state_types = self.conf.get_recipe("state")
        setp_names, setp_types = self.conf.get_recipe("setp")
        watchdog_name, watchdog_types = self.conf.get_recipe("watchdog")

        #Conexión con el robot
        self.con = rtde.RTDE(self.ip, self.port)
        self.con.connect()

        # Configurar recetas
        self.con.send_output_setup(state_names, state_types)
        self.setp = self.con.send_input_setup(setp_names, setp_types)
        self.watchdog = self.con.send_input_setup(watchdog_name, watchdog_types)

        # Configuración registro inicial
        data.list_to_setp(self.setp, np.zeros(6))
        self.initialized = False
        self.watchdog.input_register_0 = 0

        # Realizar configuración
        self.initialized = self.con.send_start()

        # Función para actualizar el estado del robot
        def get_state(self) -> data.UR5SimRobotState:
            # Inicializamos la clase tipo
            robotstate = data.UR5SimRobotState(np.zeros(6), np.zeros(6), False)
            # Mandamos una actualización del estado
            self.state = self.con.receive()
            # Comprobamos la actualización
            if self.state is None:
                # Devolvemos clase a 0 y con estado online negado
                return robotstate
            # Asignamos los valores
            robotstate.joint_position= self.state.actual_q
            robotstate.joint_velocities = self.state.actual_qd
            robotstate.online = True
            # Entregamos el estado
            return robotstate

        def send_action(self, joint_pos: ndarray, state: UR5SimRobotState):
            # Comprobamos si el estado esta activo
            if robotstate.online is False:
                print("No hay datos actualizados del Robot.")
                self.watchdog.input_int_register_0 = 0
                self.con.send(watchdog)
                return False
            else:
                self.watchdog.input_int_register_0 = 1
                data.list_to_setp(self.setp, joint_pos)
                return self.con.send(self.setp)
        








