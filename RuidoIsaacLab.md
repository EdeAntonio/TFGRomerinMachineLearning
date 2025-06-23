Una de las principales maneras en las que se resuelve el problema del ruido para el Sim2Real es con un metodo llamado "Domain Randomization". En este método se aletoriza distintos aspectos de la simulación, creando un rango de características en las que se entrenará la simulación. Todos los métodos que se encargan de realizar esta aleatorización son del tipo EventTerm, los cuales además se almacenan en un EventCfg. A continuación, te coloco los ejemplos que incluyen en los tutoriales.

///
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
///

En este caso se crean tres eventos que se encargaran de crear la randomización del dominio. La primera función permite randomizar propiedades de los cuerpos rígidos, la segunda para articulaciones y la tercera para la gravedad. En entornos directos, esta clase luego se incluye dentro de la configuración principal bajo la variable events. En manager based se incluye en el manejador de eventos. Depende de lo que se quiera randomizar, hay que buscar las funciones pertinentes dentro de isaaclab.envs.mdp.events (https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.envs.mdp.html#module-isaaclab.envs.mdp.events). Coméntame que sería lo más interesante randomizar y te preparo la configuración de los eventos. Comentándolo con Miguel, hablamos sobre que sería interesante randomizar la masa y las dimensiones de los objetos que se mueven y cogen.

A parte de la randomización del dominio, y en un tema más puro de ruido, existe la posibilidad de meter ruido tanto a las acciones como a las observaciones. Bastante interesante para tener en cuenta la tolerancia de los sensores y los motores. Para entornos directos, se debe incluir este ruido como una variable dentro de la clase de configuración principal. Tenemos por un lado para incluir ruido con sesgo y ruido gausiano puro.

///
@configclass
class MyTaskConfig:

    # at every time-step add gaussian noise + bias. The bias is a gaussian sampled at reset
    action_noise_model: NoiseModelWithAdditiveBiasCfg = NoiseModelWithAdditiveBiasCfg(
      noise_cfg=GaussianNoiseCfg(mean=0.0, std=0.05, operation="add"),
      bias_noise_cfg=GaussianNoiseCfg(mean=0.0, std=0.015, operation="abs"),
    )

    # at every time-step add gaussian noise + bias. The bias is a gaussian sampled at reset
    observation_noise_model: NoiseModelWithAdditiveBiasCfg = NoiseModelWithAdditiveBiasCfg(
      noise_cfg=GaussianNoiseCfg(mean=0.0, std=0.002, operation="add"),
      bias_noise_cfg=GaussianNoiseCfg(mean=0.0, std=0.0001, operation="abs"),
    )
***
@configclass
class MyTaskConfig:
  action_noise_model: GaussianNoiseCfg = GaussianNoiseCfg(mean=0.0, std=0.05, operation="add")
///

Por otro lado, en el entorno basado en manejadores se usan las mismas funciones pero se declaran dentro de la definición de las acciones. Los dos tipos anteriores de ruido son del tipo NoiseCfg, lo que permite incluirlos como una variable al declarar en las observaciones las observaciones. Este ruido se define dentro de los terminos de  las observaciones.

Para incluir ruido en las acciones en entornos basados por manejadores es más complicado, pues no se puede incluir en la definición. Sin embargo, se puede introducir manualmente mediante las clases de ruido o algunas de las funciones vistas. Invetigaré más acerca de este tema, porque no veo una forma concreta de incluirlos.
