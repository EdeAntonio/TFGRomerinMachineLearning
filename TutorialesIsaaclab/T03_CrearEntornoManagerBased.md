# Creación de un entorno Manager-Based
Los entornos (enviroments) juntan distintos elementos de la simulación, como la escena, las observaciones y los espacios de actuación, los eventos de reseteo, etc. Estos entornos se pueden crear a través de dos clases: [envs.ManagerBasedEnv](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.envs.html#isaaclab.envs.ManagerBasedRLEnv), la clase básica; y [envs.ManagerBasedRLEnv](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.envs.html#isaaclab.envs.ManagerBasedRLEnv), la clase para entornos RL con recompensas y terminaciones.

En este tutorial vamos a ver primero la opción básica.
### La clase base envs.ManagerBasedEnv
Esta clase provee de una interfaz para interactuar y simular el entorno. Se compone de:
- [scene.InteractiveScene](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.scene.html#isaaclab.scene.InteractiveScene) : La escena usada
- [managers.ActionManager](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.managers.html#isaaclab.managers.ActionManager) : El manejador de las acciones.
- [manager.ObservationManager](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.managers.html#isaaclab.managers.ObservationManager) : El manejador de las observaciones.
- [manager.EventManager](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.managers.html#isaaclab.managers.EventManager) : El manejador de los eventos como inicios, reseteos, intervalos, etc.

En este tutorial se van a estudiar cada componente y como debe configurarse.

### Diseñar la escena
La primera parte de crear un entorno es configurar su escena, lo cual ya se ha explicado en T02_UtilizarEscenasInteractivas.md. Se va a usar la misma configuración de escena que en dicho tutorial.

### Definir las acciones
En el tutorial anterior, T02_UtilizarEscenasInteractivas.md, se daban las acciones a través del método [assets.Articulation.set_joint_effort_target()](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.assets.html#isaaclab.assets.Articulation.set_joint_effort_target). En este tutorial en cambio se utiliza [managers.ActionManager](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.managers.html#isaaclab.managers.ActionManager) para manejar las acciones.

Este manejador puede contener distintos [managers.ActionTerm](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.managers.html#isaaclab.managers.ActionTerm), donde cada uno de estas clases maneja un aspecto específico del entorno. Por ejemplo, un brazo robot podría tener dos ActionTerm, uno para el brazo y otro para el gripper. Esto permite diseñar distintas estrategias de control para distintos aspectos del entorno.

En el entorno cartpole, queremos controlar la fuerza que se le aplica al carro para equilibrar la palanca. 

```python
    @configclass
    class ActionsCfg:
        """Action specifications for the environment."""

        joint_efforts = mdp.JointEffortActionCfg(asset_name="robot", joint_names=["slider_to_cart"], scale=5.0)
```

### Definir observaciones
Las observaciones definen los estados que el agente va a valorar para decidir que acciones tomar. Estas acciones en issaclab se computan a través de la clase [managers.ObservationManager](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.managers.html#isaaclab.managers.ObservationManager).

Al igual que manejador de acciones, pueden existir distintos términos de observación. Estos sirven para diferenciar espacios de observación dentro de un entorno.

Para este tutorial se va a declarar un grupo llamado "policy". Definimos un grupo heredando de la clase [managers.ObservationGroupCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.managers.html#isaaclab.managers.ObservationGroupCfg). Esta clase recoje distintos términos de observación y ayuda a definir propiedades comunes, permitiendo configurar la corrupción de ruido o la concatenación de las observaciones en un mismo tensor.

Los terminos individuales se obtienen utilizando la clase [managers.ObservationTermCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.managers.html#isaaclab.managers.ObservationTermCfg). Esta clase toma una variable func que especifica la clase o la función a la que se llama para observar.

```python
    @configclass
        class ObservationsCfg:
        """Observation specifications for the environment."""

        @configclass
        class PolicyCfg(ObsGroup):
            """Observations for policy group."""

            # observation terms (order preserved)
            joint_pos_rel = ObsTerm(func=mdp.joint_pos_rel)
            joint_vel_rel = ObsTerm(func=mdp.joint_vel_rel)

            def __post_init__(self) -> None:
                self.enable_corruption = False
                self.concatenate_terms = True

        # observation groups
        policy: PolicyCfg = PolicyCfg()
```

### Definir eventos
La idea general de estos componentes es crear una clase configuradora para luego pasarla a la clase manejadora. El manejador de eventos funciona de la misma manera. 

La clase [managers.EventManager](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.managers.html#isaaclab.managers.EventManager) es responsable de realizar los cambios pertinentes en el estado de la simulación. Cada evento está caracterizado por un [managers.EventTermCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.managers.html#isaaclab.managers.EventTermCfg), el cual toma [managers.EventTermCfg.func](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.managers.html#isaaclab.managers.EventTermCfg.func) que especifica la función o la clase a la cual se llama para ejecutar eventos.

Añadido a esto, se espera también el modo (mode), el cual define cuándo se da el evento. Para esto se debe adaptar la clase [ManagerBasedEnv](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.envs.html#isaaclab.envs.ManagerBasedEnv). No obstante, Isaaclab provee tres modos: 
- "startup" : Evento que toma lugar solo una vez al inicio de la simulación
- "reset" : Evento que se da en la terminación y reseteo del entorno
- "interval" : Evento que se da en un intervalo concreto, es decir, periodicamente al avanzar.

En este tutorial, se elige aleatoriamente el peso de la palanca en el inicio (startup) y la posición de la palanca en los reseteos (reset).

```python
@configclass
class EventCfg:
    """Configuration for events."""

    # on startup
    add_pole_mass = EventTerm(
        func=mdp.randomize_rigid_body_mass,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg("robot", body_names=["pole"]),
            "mass_distribution_params": (0.1, 0.5),
            "operation": "add",
        },
    )

    # on reset
    reset_cart_position = EventTerm(
        func=mdp.reset_joints_by_offset,
        mode="reset",
        params={
            "asset_cfg": SceneEntityCfg("robot", joint_names=["slider_to_cart"]),
            "position_range": (-1.0, 1.0),
            "velocity_range": (-0.1, 0.1),
        },
    )

    reset_pole_position = EventTerm(
        func=mdp.reset_joints_by_offset,
        mode="reset",
        params={
            "asset_cfg": SceneEntityCfg("robot", joint_names=["cart_to_pole"]),
            "position_range": (-0.125 * math.pi, 0.125 * math.pi),
            "velocity_range": (-0.01 * math.pi, 0.01 * math.pi),
        },
    )
```
### Unirlo todo
Una vez se han preparado todas las configuraciones de los manejadores, podemos pasar a definir la clase [envs.ManagerBasedEnvCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.envs.html#isaaclab.envs.ManagerBasedEnvCfg). Esta clase toma la escena, la acción, la observación y el configurador de eventos.

Además de estos, toma la [envs.ManagerBasedEnvCfg.sim](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.envs.html#isaaclab.envs.ManagerBasedEnvCfg.sim), que contiene parametros de la simulación como el valor de renderizción (timestep) o la gravedad. Es recomendable configurar esta variable a través de una función \_\_pos_init\_\_(self), el cual se llamará una vez se inicie la configuración.

```python
@configclass
class CartpoleEnvCfg(ManagerBasedEnvCfg):
    """Configuration for the cartpole environment."""

    # Scene settings
    scene = CartpoleSceneCfg(num_envs=1024, env_spacing=2.5)
    # Basic settings
    observations = ObservationsCfg()
    actions = ActionsCfg()
    events = EventCfg()

    def __post_init__(self):
        """Post initialization."""
        # viewer settings
        self.viewer.eye = [4.5, 0.0, 6.0]
        self.viewer.lookat = [0.0, 0.0, 2.0]
        # step settings
        self.decimation = 4  # env step every 4 sim steps: 200Hz / 4 = 50Hz
        # simulation settings
        self.sim.dt = 0.005  # sim step every 5ms: 200Hz

```

### Ejecución de la simulación
Por último, nos adentramos en el bucle de la simulación, ahora mucho más simplificado gracias a la clase envs.ManagerBasedEnv. En este caso solo tenemos que llamar a las propias funciones de esta clase para resetear y avanza la simulación.

La clase envs.ManagerBasedEnv no tiene nociones de terminaciones, ya que ese concepto es propio de tareas episódicas. En este tutorial se resetea a intervalos regulares.

```python
def main():
    """Main function."""
    # parse the arguments
    env_cfg = CartpoleEnvCfg()
    env_cfg.scene.num_envs = args_cli.num_envs
    # setup base environment
    env = ManagerBasedEnv(cfg=env_cfg)

    # simulate physics
    count = 0
    while simulation_app.is_running():
        with torch.inference_mode():
            # reset
            if count % 300 == 0:
                count = 0
                env.reset()
                print("-" * 80)
                print("[INFO]: Resetting environment...")
            # sample random actions
            joint_efforts = torch.randn_like(env.action_manager.action)
            # step the environment
            obs, _ = env.step(joint_efforts)
            # print current orientation of pole
            print("[Env 0]: Pole joint: ", obs["policy"][0][1].item())
            # update counter
            count += 1

    # close the environment
    env.close()
```

