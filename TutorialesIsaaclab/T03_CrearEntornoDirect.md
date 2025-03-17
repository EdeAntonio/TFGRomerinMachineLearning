# Crear un entorno Direct RL
Además de la clase envs.ManagerVasedRLEnv, existe la posibilidad de crear entornos mediante la clase [DirectRLEnv](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.envs.html#isaaclab.envs.DirectRLEnv). Esta clase permite un control más directo en la configuración y ejecución del entorno.

La clase [DirectRLEnv](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.envs.html#isaaclab.envs.DirectRLEnv) implementa las funciones de recompensa y observación directamente.

En este tutorial vamos a configurar el entorno cartpole mediante esta clase.

### ¡Atención!
Estos tutoriales T03, explican como se crean los entornos. Sin embargo, estos solo son las normas sobre las cuales se realizará el aprendizaje. Se definen observaciones, recompensas, acciones, condiciones de reseteo, formas de resteo, etc, pero no interactuan entre si, son solo normas. Como se reciben las recompensas, como se ejecutan las acciones. El verdadero entrenamiento por refuerzo se hace con las librerías.

### Configuración
De manera similar a los entornos Mager-Based, se necesita una clase de configuración, la [envs.DirectRLEnvCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.envs.html#isaaclab.envs.DirectRLEnvCfg) para definir la tarea. Para definir esta tarea, como no tenemos manejadores, deberemos definir cuantas acciones y observaciones tendremos en nuestro entorno.

```python
@configclass
class CartpoleEnvCfg(DirectRLEnvCfg):
   ...
   action_space = 1
   observation_space = 4
   state_space = 0
```

La clase de configuración también permite definir atributos relacionados con la tarea.

```python
@configclass
class CartpoleEnvCfg(DirectRLEnvCfg):
   ...
   # reset
   max_cart_pos = 3.0
   initial_pole_angle_range = [-0.25, 0.25]

   # reward scales
   rew_scale_alive = 1.0
   rew_scale_terminated = -2.0
   rew_scale_pole_pos = -1.0
   rew_scale_cart_vel = -0.01
   rew_scale_pole_vel = -0.005
```

Al crear un nuevo entorno este debe heredar de [DirectRLEnv](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.envs.html#isaaclab.envs.DirectRLEnv).

```python
class CartpoleEnv(DirectRLEnv):
   cfg: CartpoleEnvCfg

   def __init__(self, cfg: CartpoleEnvCfg, render_mode: str | None = None, **kwargs):
     super().__init__(cfg, render_mode, **kwargs) # Constructor de la clase padre
```

Esta clase también puede guardar variables accesibles para todas las funciones en la clase.

### Creación de la escena
Al contrario que en Manager-Based, los entornos Direct pemiten definir una función para la creación de la escena. Esto permite una mayor flexibilidad para crear la escena.

```python
    def _setup_scene(self):
        self.cartpole = Articulation(self.cfg.robot_cfg)
        # add ground plane
        spawn_ground_plane(prim_path="/World/ground", cfg=GroundPlaneCfg())
        # clone and replicate
        self.scene.clone_environments(copy_from_source=False)
        # add articulation to scene
        self.scene.articulations["cartpole"] = self.cartpole
        # add lights
        light_cfg = sim_utils.DomeLightCfg(intensity=2000.0, color=(0.75, 0.75, 0.75))
        light_cfg.func("/World/Light", light_cfg)
```

### Definir recompensas
La función de recompensa se debe definir en _get_rewards(self) API, el cual devuelve el buffer de recompensas como valor de retorno. En este caso se implementa una función Pytorch JIT para computar los distintos componentes de la recompensa.

```python
def _get_rewards(self) -> torch.Tensor:
     total_reward = compute_rewards(
         self.cfg.rew_scale_alive,
         self.cfg.rew_scale_terminated,
         self.cfg.rew_scale_pole_pos,
         self.cfg.rew_scale_cart_vel,
         self.cfg.rew_scale_pole_vel,
         self.joint_pos[:, self._pole_dof_idx[0]],
         self.joint_vel[:, self._pole_dof_idx[0]],
         self.joint_pos[:, self._cart_dof_idx[0]],
         self.joint_vel[:, self._cart_dof_idx[0]],
         self.reset_terminated,
     )
     return total_reward

@torch.jit.script
def compute_rewards(
    rew_scale_alive: float,
    rew_scale_terminated: float,
    rew_scale_pole_pos: float,
    rew_scale_cart_vel: float,
    rew_scale_pole_vel: float,
    pole_pos: torch.Tensor,
    pole_vel: torch.Tensor,
    cart_pos: torch.Tensor,
    cart_vel: torch.Tensor,
    reset_terminated: torch.Tensor,
):
    rew_alive = rew_scale_alive * (1.0 - reset_terminated.float())
    rew_termination = rew_scale_terminated * reset_terminated.float()
    rew_pole_pos = rew_scale_pole_pos * torch.sum(torch.square(pole_pos), dim=-1)
    rew_cart_vel = rew_scale_cart_vel * torch.sum(torch.abs(cart_vel), dim=-1)
    rew_pole_vel = rew_scale_pole_vel * torch.sum(torch.abs(pole_vel), dim=-1)
    total_reward = rew_alive + rew_termination + rew_pole_pos + rew_cart_vel + rew_pole_vel
    return total_reward
```

### Definir observaciones
 El buffer de observaciones se debe calcular con la funcion _get_observations(self). Al final de la API, se devuelve un diccionario con la palabra clave "policy" y el buffer de observaciones como valor. Para políticas asimétricas, se debería incluir también una palabra clave critic, con el buffer de estados como valor.

 ```python
     def _get_observations(self) -> dict:
        obs = torch.cat(
            (
                self.joint_pos[:, self._pole_dof_idx[0]].unsqueeze(dim=1),
                self.joint_vel[:, self._pole_dof_idx[0]].unsqueeze(dim=1),
                self.joint_pos[:, self._cart_dof_idx[0]].unsqueeze(dim=1),
                self.joint_vel[:, self._cart_dof_idx[0]].unsqueeze(dim=1),
            ),
            dim=-1,
        )
        observations = {"policy": obs}
        return observations
```

### Calcular los finales y realizar los resets
Para crear el buffer de finalizaciones se debe utilizar una función definida como _get_dones(self). Este método se define para que calcule los entornos que deben ser reiniciados.

```python
    def _get_dones(self) -> tuple[torch.Tensor, torch.Tensor]:
        self.joint_pos = self.cartpole.data.joint_pos
        self.joint_vel = self.cartpole.data.joint_vel

        time_out = self.episode_length_buf >= self.max_episode_length - 1
        out_of_bounds = torch.any(torch.abs(self.joint_pos[:, self._cart_dof_idx]) > self.cfg.max_cart_pos, dim=1)
        out_of_bounds = out_of_bounds | torch.any(torch.abs(self.joint_pos[:, self._pole_dof_idx]) > math.pi / 2, dim=1)
        return out_of_bounds, time_out
```

Una vez se calculan los indices de los entornos que necesitan un reset, se ejecuta la función de reset. Dentro de esta función, se definen los nuevos estados de las simulaciones.

```python
    def _reset_idx(self, env_ids: Sequence[int] | None):
        if env_ids is None:
            env_ids = self.cartpole._ALL_INDICES
        super()._reset_idx(env_ids)

        joint_pos = self.cartpole.data.default_joint_pos[env_ids]
        joint_pos[:, self._pole_dof_idx] += sample_uniform(
            self.cfg.initial_pole_angle_range[0] * math.pi,
            self.cfg.initial_pole_angle_range[1] * math.pi,
            joint_pos[:, self._pole_dof_idx].shape,
            joint_pos.device,
        )
        joint_vel = self.cartpole.data.default_joint_vel[env_ids]

        default_root_state = self.cartpole.data.default_root_state[env_ids]
        default_root_state[:, :3] += self.scene.env_origins[env_ids]

        self.joint_pos[env_ids] = joint_pos
        self.joint_vel[env_ids] = joint_vel

        self.cartpole.write_root_pose_to_sim(default_root_state[:, :7], env_ids)
        self.cartpole.write_root_velocity_to_sim(default_root_state[:, 7:], env_ids)
        self.cartpole.write_joint_state_to_sim(joint_pos, joint_vel, None, env_ids)
```

### Aplicar acciones
Hay dos APIs diseñadas para trabajar con acciones. Por un lado, la API _pre_physics_step(self, actions), la cual sirve para procesar el buffer de acciones antes de tomar un paso físico. Esta se llama una vez por paso de RL, antes de tomar cualquier tipo de paso físico.

```python
    def _pre_physics_step(self, actions: torch.Tensor) -> None:
        self.actions = self.action_scale * actions.clone()
```

Por otro lado, _apply_action(self), la cual se llama un número de veces definido en decimation, antes de tomar cualquier paso físico. Esto da la libertad de aplicar las acciones por cada paso físico.

### Aleatorización del dominio
En los entornos directos, se utiliza el módulo de [configclass](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.utils.html#module-isaaclab.utils.configclass) para especificar una configuración mediante variables [EventTermCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.managers.html#isaaclab.managers.EventTermCfg)

```python
@configclass
class EventCfg:
  robot_physics_material = EventTerm(
      func=mdp.randomize_rigid_body_material,
      mode="reset",
      params={
          "asset_cfg": SceneEntityCfg("robot", body_names=".*"),
          "static_friction_range": (0.7, 1.3),
          "dynamic_friction_range": (1.0, 1.0),
          "restitution_range": (1.0, 1.0),
          "num_buckets": 250,
      },
  )
  robot_joint_stiffness_and_damping = EventTerm(
      func=mdp.randomize_actuator_gains,
      mode="reset",
      params={
          "asset_cfg": SceneEntityCfg("robot", joint_names=".*"),
          "stiffness_distribution_params": (0.75, 1.5),
          "damping_distribution_params": (0.3, 3.0),
          "operation": "scale",
          "distribution": "log_uniform",
      },
  )
  reset_gravity = EventTerm(
      func=mdp.randomize_physics_scene_gravity,
      mode="interval",
      is_global_time=True,
      interval_range_s=(36.0, 36.0),  # time_s = num_steps * (decimation * dt)
      params={
          "gravity_distribution_params": ([0.0, 0.0, 0.0], [0.0, 0.0, 0.4]),
          "operation": "add",
          "distribution": "gaussian",
      },
  )
```

Cada objeto EventTerm es una clase [EventTermCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.managers.html#isaaclab.managers.EventTermCfg). Esta toma una func, a la cual se llama a la hora de randomizar; una variable mode, la cual indica cuando se realiza el evento; el diccionario params, que entrega los argumentos necesarios para ejecutar la funcion func.

Una vez configurada se debe añadir a la clase de configuración, bajo el nombre events.

```python
@configclass
class MyTaskConfig:
  events: EventCfg = EventCfg()
```

### Ruido de acciones y observaciones
Normalmente, para simular las imprecisiones tanto a la hora de observar como a la hora de realizar acciones, se introduce ruido a estas variables.

```python
@configclass
class MyTaskConfig:

    # a cada paso se añade ruido y sesgo gausiano. El sesgo se determina en el reset
    action_noise_model: NoiseModelWithAdditiveBiasCfg = NoiseModelWithAdditiveBiasCfg(
      noise_cfg=GaussianNoiseCfg(mean=0.0, std=0.05, operation="add"),
      bias_noise_cfg=GaussianNoiseCfg(mean=0.0, std=0.015, operation="abs"),
    )

    # a cada paso se añade ruido y sesgo gausiano. El sesgo se determina en el reset
    observation_noise_model: NoiseModelWithAdditiveBiasCfg = NoiseModelWithAdditiveBiasCfg(
      noise_cfg=GaussianNoiseCfg(mean=0.0, std=0.002, operation="add"),
      bias_noise_cfg=GaussianNoiseCfg(mean=0.0, std=0.0001, operation="abs"),
    )
```

[NoiseModelWithAdditiveBiasCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.utils.html#isaaclab.utils.noise.NoiseModelWithAdditiveBiasCfg), se puede utilizar para simular ruido no correlacionado (noise_cfg) y ruido correlacionado (bias_noise_cfg) que se recalcula en cada reset.

Si solo queremos ruido por paso del tiempo, se puede usar la función [GaussianNoiseCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.utils.html#isaaclab.utils.noise.GaussianNoiseCfg).

```python
@configclass
class MyTaskConfig:
  action_noise_model: GaussianNoiseCfg = GaussianNoiseCfg(mean=0.0, std=0.05, operation="add")
```
