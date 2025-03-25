# Registrar un entorno
En los tutoriales anteriores hemos visto como crear un entorno. Este entorno luego se instanciaba manualmente, importando la clase del entorno y su clase de configuración. Nuestro objetivo ahora, es utilizar la función gymnasium.register() para registrar entornos en un registro de gymnasium. Esto nos permite utilizar la función gymnasium.make() para crear los entornos.

La clase envs.ManagerBasedRLEnv hereda de [gymnasium.Env](https://gymnasium.farama.org/api/env/#gymnasium.Env). Sin embargo, envs.ManagerBasedRLEnv implementa un entorno vectorizado, lo que significa que puede instanciar múltiples entornos en un mismo proceso ejecutandose a la vez. De manera similar, envs.DirectRLEnv también hereda de gymnasium.ENV.

## Usar el registro del gym
### Manager-Based
Para registrar un entorno, utilizamos el método gymnasium.register(). Este nétodo toma el nombre del entorno, el punto de entrada a la clase del entorno y el punto de entrada a la configuración del entorno.

```python
import gymnasium as gym

from . import agents

##
# Register Gym environments.
##

gym.register(
    id="Isaac-Cartpole-RGB-TheiaTiny-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.cartpole_camera_env_cfg:CartpoleTheiaTinyCameraEnvCfg",
        "rl_games_cfg_entry_point": f"{agents.__name__}:rl_games_feature_ppo_cfg.yaml",
    },
)
```

La variable 'id' toma el nombre del entorno. Se incluye el prefijo "Isaac-" para facilitar su búsqueda, a la vez que un nombre y el número de la versión.

La variable 'entry_point' toma el punto de entrada a la clase del entrono. Este punto de entrada se da como una cadena formada por "module:class", como por ejemplo en este caso, "isaaclab.env:ManagerBasedRLEnv".

Por último, pasaremos un diccionario kwargs con la configuración del entorno y la librería de aprendizaje que vayamos a usar. Para ello, se le asigna a cada una, una cadena formateada python con el nombre del scrip sobreescrito.

### Direct 
Para entornos directos, creamos los entornos siguiendo una estructura similar.

```python
import gymnasium as gym

from . import agents

##
# Register Gym environments.
##

gym.register(
    id="Isaac-Cartpole-Direct-v0",
    entry_point=f"{__name__}.cartpole_env:CartpoleEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.cartpole_env:CartpoleEnvCfg",
        "rl_games_cfg_entry_point": f"{agents.__name__}:rl_games_ppo_cfg.yaml",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:CartpolePPORunnerCfg",
        "skrl_cfg_entry_point": f"{agents.__name__}:skrl_ppo_cfg.yaml",
        "sb3_cfg_entry_point": f"{agents.__name__}:sb3_ppo_cfg.yaml",
    },
)
```

Ahora, sin embargo, añadimos un sufijo direct y cambiamos el punto de entrada, que ahora será la implementación de la clase.

## Crear el entorno
Para esta tarea, primero debemos importar la extensión isaaclab_tasks, siempre al principio del script. Esto ejecutara el fichero  \_\_init\_\_.py, el cual itera el resto de subpaquetes y registros relacionados con el entorno.

Para este tutorial, leemos la tarea a realizar desde la línea de comandos. El nombre de la tarea sirve para pasar la configuración de este y crear la instancia del entorno. 

```python
    # create environment configuration
    env_cfg = parse_env_cfg(
        args_cli.task, device=args_cli.device, num_envs=args_cli.num_envs, use_fabric=not args_cli.disable_fabric
    )
    # create environment
    env = gym.make(args_cli.task, cfg=env_cfg)
```