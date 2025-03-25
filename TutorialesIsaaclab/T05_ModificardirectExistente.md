# Modificación de un entorno directo existente
Algunas veces no es necesario crear una tarea desde cero, sino que se puede modificar una tarea existente ajustándola a la situación. En este turorial se muestra como realizar estas modificaciones sin afectar al código principal.

### Duplicar el fichero y registrar una nueva tarea.
 Primero debemos duplicar el archivo y renombrar tanto las instancias del entorno como de la configuración del entorno para que no haya conflictos de nombre.

 Una vez hemos cambiado el registro procedemos a registrar la nueva tarea modificada. Para ello debemos modificar el fichero \_\_init\_\_.py. Recordemos que este fichero es el que se inicializa al importar la carpeta de las tareas.

 ```python
 gym.register(
    id="Isaac-H1-Direct-v0",
    entry_point="isaaclab_tasks.direct.humanoid:H1Env",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": H1EnvCfg,
        "rl_games_cfg_entry_point": f"{agents.__name__}:rl_games_ppo_cfg.yaml",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:HumanoidPPORunnerCfg",
        "skrl_cfg_entry_point": f"{agents.__name__}:skrl_ppo_cfg.yaml",
    },
)
```

### Cambiar el robot
La clase de configutación encapsula los valores de configuración del entorno. En este ejemplo la variable robot contine la dirección de la configuración de la articulación. Como en este caso el robot se encuentra dentro de la extensión isaaclab_assets, podemos simplemente importarla y remplazarla.

```python
robot: ArticulationCfg = H1_CFG.replace(prim_path="/World/envs/env_.*/Robot")
joint_gears: list = [
    50.0,  # left_hip_yaw
    50.0,  # right_hip_yaw
    50.0,  # torso
    50.0,  # left_hip_roll
    50.0,  # right_hip_roll
    50.0,  # left_shoulder_pitch
    50.0,  # right_shoulder_pitch
    50.0,  # left_hip_pitch
    50.0,  # right_hip_pitch
    50.0,  # left_shoulder_roll
    50.0,  # right_shoulder_roll
    50.0,  # left_knee
    50.0,  # right_knee
    50.0,  # left_shoulder_yaw
    50.0,  # right_shoulder_yaw
    50.0,  # left_ankle
    50.0,  # right_ankle
    50.0,  # left_elbow
    50.0,  # right_elbow
]
```
