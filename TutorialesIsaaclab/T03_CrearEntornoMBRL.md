# Creaación de un entorno Manager Based RL
La clase [envs.ManagerBasedRLEnv](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.envs.html#isaaclab.envs.ManagerBasedRLEnv) expande las capacidades de su contraparte básica, con el objetivo de ser usada en tareas de aprendizaje por refuerzo. 

Se recomienda utilizar una clase [envs.ManagerBasedRLEnvCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.envs.html#isaaclab.envs.ManagerBasedRLEnvCfg) para crear dicha clase, separando así la implementación del entorno de la especificación de las tareas. 

En este tutorial se va a configurar el entorno cartpole mediante esta clase. Nos vamos a centrar únicamente en las partes de RL, ya que las de la clase básica se vieron en [T03_CrearEntornoManagerBased.md](T03_CrearEntornoManagerBased.md).

### Definición de recompensas.
Para manejar las recompensas del agente se utiliza la clase [managers.RewardManager](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.managers.html#isaaclab.managers.RewardManager). Esta clase, de igual manera que las anteriores, se configura usando la clase [managers.RewardTermCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.managers.html#isaaclab.managers.RewardTermCfg). Esta clase especifíca la función o clase que va a llamar para entregar las recompensas y el peso de dicha recompensa. También toma un diccionario de palabras "params", el cual pasa una seria de valores al llamarse a la recompensa.

Para el entorno de cartpole crearemos las siguientes recompensas:
- Alive Reward : Incita al agente a mantenerse activo el máximo tiempo posible.
- Terminating Reward : Penaliza la finalización del agente
- Pole Angle Reward : Incita al agente a mantener la palanca verticalmente hacia arriba.
- Cart Velocity Reward : Incita al agente a reducir su velocidad.
- Pole Velocity Reward : Incita al agente a mantener la velocidad de la palanca lo mínimo posible.

```python
@configclass
class RewardsCfg:
    """Reward terms for the MDP."""

    # (1) Constant running reward
    alive = RewTerm(func=mdp.is_alive, weight=1.0)
    # (2) Failure penalty
    terminating = RewTerm(func=mdp.is_terminated, weight=-2.0)
    # (3) Primary task: keep pole upright
    pole_pos = RewTerm(
        func=mdp.joint_pos_target_l2,
        weight=-1.0,
        params={"asset_cfg": SceneEntityCfg("robot", joint_names=["cart_to_pole"]), "target": 0.0},
    )
    # (4) Shaping tasks: lower cart velocity
    cart_vel = RewTerm(
        func=mdp.joint_vel_l1,
        weight=-0.01,
        params={"asset_cfg": SceneEntityCfg("robot", joint_names=["slider_to_cart"])},
    )
    # (5) Shaping tasks: lower pole angular velocity
    pole_vel = RewTerm(
        func=mdp.joint_vel_l1,
        weight=-0.005,
        params={"asset_cfg": SceneEntityCfg("robot", joint_names=["cart_to_pole"])},
    )
```

### Definición de la finalización
La mayoría de agentes en RL actúan en un tiempo finito llamado episodio. Esto ocurre ya que hay momentos en los cuales el agente se vuelve inestable, inseguro o tenemos suficiente información. En estos momentos debemos resetear el agente.

En este tutorial resetearemos el agente en dos casos:
- Finalización tiempo de episodio
- Carro fuera de márgenes

```python
@configclass
class TerminationsCfg:
    """Termination terms for the MDP."""

    # (1) Time out
    time_out = DoneTerm(func=mdp.time_out, time_out=True)
    # (2) Cart out of bounds
    cart_out_of_bounds = DoneTerm(
        func=mdp.joint_pos_out_of_manual_limit,
        params={"asset_cfg": SceneEntityCfg("robot", joint_names=["slider_to_cart"]), "bounds": (-3.0, 3.0)},
    )
```

### Definición de comandos
Existe un manejador de comandos [managers.CommandManager](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.managers.html#isaaclab.managers.CommandManager). Para tareas simples como esta no realizamos comandos, por lo que la dejamos en blanco.

Se puede observar estos comandos en tareas de locomoción o manipulación.

### Definición de un curriculum
A menudo un agente empieza a entrenar con una tarea sencilla, la cual luego incrementa su dificultad. Este incremento de la dificultad viene dado por la clase [managers.CommandManager](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.managers.html#isaaclab.managers.CommandManager).

Para este tutorial no utilizaremos esta clase, pero se puede observar en tareas de locomoción y manipulación.

### Combinación.
Se utiliza la misma estructura que su contraparte básica.
```python
@configclass
class CartpoleEnvCfg(ManagerBasedRLEnvCfg):
    """Configuration for the cartpole environment."""

    # Scene settings
    scene: CartpoleSceneCfg = CartpoleSceneCfg(num_envs=4096, env_spacing=4.0)
    # Basic settings
    observations: ObservationsCfg = ObservationsCfg()
    actions: ActionsCfg = ActionsCfg()
    events: EventCfg = EventCfg()
    # MDP settings
    rewards: RewardsCfg = RewardsCfg()
    terminations: TerminationsCfg = TerminationsCfg()

    # Post initialization
    def __post_init__(self) -> None:
        """Post initialization."""
        # general settings
        self.decimation = 2
        self.episode_length_s = 5
        # viewer settings
        self.viewer.eye = (8.0, 0.0, 5.0)
        # simulation settings
        self.sim.dt = 1 / 120
        self.sim.render_interval = self.decimation
```

### Ejecutar la simulación
De manera similar a la anterior también, eliminamos la necesidad de ejecutar pasos para todos los elementos. Ejucutamos unicamente los pasos de nuestro entorno.

```python
def main():
    """Main function."""
    # create environment configuration
    env_cfg = CartpoleEnvCfg()
    env_cfg.scene.num_envs = args_cli.num_envs
    # setup RL environment
    env = ManagerBasedRLEnv(cfg=env_cfg)

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
            obs, rew, terminated, truncated, info = env.step(joint_efforts)
            # print current orientation of pole
            print("[Env 0]: Pole joint: ", obs["policy"][0][1].item())
            # update counter
            count += 1

    # close the environment
    env.close()
```