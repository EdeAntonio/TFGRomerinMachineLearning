# Interactuar con una articulación
Este tutorial sirve para interactuar con un robot en una simulación. Siguiendo en la dinámica del tutorial anterior, vamos a ver como configurar una unión y aplicar acciones sobre un robot.
## Diseño
Primero, a parte de generar un plano inferior y una luz, vamos a introducir una articulación cartpole a partir de un archivo USD. Para este objeto vamos a utilizar su configuración por defecto, la cual viene instanciada en [assets.ArticulationCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.assets.html#isaaclab.assets.ArticulationCfg).
Esta clase contiene información sobre el comportamiento de dicha configuración. Más adelante en esta documentación se verá como escribir la configuración de un objeto. 

Como ya hemos visto antes podemos crear una instancia del objeto [assets.Articulation](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.assets.html#isaaclab.assets.Articulation) pasando su configuración a dicho objeto.

    ```python
    # Create separate groups called "Origin1", "Origin2"

    # Each group will have a robot in it
    origins = [[0.0, 0.0, 0.0], [-1.0, 0.0, 0.0]]

    # Origin 1
    prim_utils.create_prim("/World/Origin1", "Xform", translation=origins[0])

    # Origin 2
    prim_utils.create_prim("/World/Origin2", "Xform", translation=origins[1])

    # Articulation
    cartpole_cfg = CARTPOLE_CFG.copy()
    cartpole_cfg.prim_path = "/World/Origin.*/Robot"
    cartpole = Articulation(cfg=cartpole_cfg)
    ```

## Ejecutar la simulación
### Resetear la simulación
De manera similar a los objetos rígidos  debemos configurar también sus propiedades báscias (root_state). No obstante, en este caso, aparte de llamar a Articulation.write_root_pose_to_sim() y Articulation.write_root_velocity_to_sim(), también debemos llamar a la función Articulation.write_joint_state_to_sim().

    ```python
    # reset the scene entities
    # root state
    
    # we offset the root state by the origin since the states are written in simulation world frame
    # if this is not done, then the robots will be spawned at the (0, 0, 0) of the simulation world
    root_state = robot.data.default_root_state.clone()
    root_state[:, :3] += origins
    robot.write_root_pose_to_sim(root_state[:, :7])
    robot.write_root_velocity_to_sim(root_state[:, 7:])

    # set joint positions with some noise
    joint_pos, joint_vel = robot.data.default_joint_pos.clone(), robot.data.default_joint_vel.clone()
    joint_pos += torch.rand_like(joint_pos) * 0.1
    robot.write_joint_state_to_sim(joint_pos, joint_vel)
            
    # clear internal buffers
    robot.reset()
    ```

### Avanzar la simulación
Actuar sobre una articulación requiere:
- 1. Configurar el objetivo: Hay que marcar la posición, velocidad o esfuerzo objetivo para la articulación.
- 2. Registrar la información en el simulador

    ```python
    # Apply random action
    # -- generate random joint efforts
    efforts = torch.randn_like(robot.data.joint_pos) * 5.0
    # -- apply action to the robot
    robot.set_joint_effort_target(efforts)
    # -- write data to sim
    robot.write_data_to_sim()
    ```

### Actualizar el estado
Por último se actualiza el estado de la articulación.

    ```python
    # Update buffers
    robot.update(sim_dt)
    ```


