# Interactuar con un objeto rígido
En este tutorial se va a estudiar como se puede crear e interactuar con un objeto rígido. Esto se hará a través de la clase [assets.RigidObject](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.assets.html#isaaclab.assets.RigidObject).

Para esta tarea se va a dividir la función main en dos funciones separadas:
- Diseño de la escena
- Ejecución de la simulación

Se debe respetar este orden ya que después de introducir el reset e iniciarse la simulación no se pueden añadir más físicas.

## Diseño de la escena.
Al igual que en el tutorial anterior vamos a crear una escena con un plano inferior y un punto de luz. Además añadiremos un objeto rígido utilizando la clase [assets.RigidObject](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.assets.html#isaaclab.assets.RigidObject). Esta se encarga de crea el objeto y inicializar sus físicas.
En este caso vamos a utilizar la clase [assets.RigidObjectCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.assets.html#isaaclab.assets.RigidObjectCfg) para envolver las características de su creación. 
Se va a utilizar también un Xform prim padre que servirá para agrupar los objetos en un grupo. La expresión "/World/Origin.*/Cone se pasa a assets.RigidObject, creando todos los prims en las posiciones "/World/Origin{i}".

    # Create separate groups called "Origin1", "Origin2", "Origin3"

    # Each group will have a robot in it
    origins = [[0.25, 0.25, 0.0], [-0.25, 0.25, 0.0], [0.25, -0.25, 0.0], [-0.25, -0.25, 0.0]]
    for i, origin in enumerate(origins):
        prim_utils.create_prim(f"/World/Origin{i}", "Xform", translation=origin)

    # Rigid Object
    cone_cfg = RigidObjectCfg(
        prim_path="/World/Origin.*/Cone",
        spawn=sim_utils.ConeCfg(
            radius=0.1,
            height=0.2,
            rigid_props=sim_utils.RigidBodyPropertiesCfg(),
            mass_props=sim_utils.MassPropertiesCfg(mass=1.0),
            collision_props=sim_utils.CollisionPropertiesCfg(),
            visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.0, 1.0, 0.0), metallic=0.2),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(),
    )
    cone_object = RigidObject(cfg=cone_cfg)

Como queremos interactuar como queremos interactuar con dicho objeto rígido, devolvemos la entidad de la escena a la función pricipal. Esta entidad luego se usará en el bucle principal.

    # return the scene information
    scene_entities = {"cone": cone_object}
    return scene_entities, origins

## Ejecutación del bucle de la simulación
Para modificar la simulación se deben realizar tres tareas: resetear, avanzar y actualizar. Por convenencia en este tutorial se extrae el objeto.

### Resetear la simulación
Para resetear la simulación debemos darle a nuestro objeto rígido una posición y velocidad, que constituyen las propiedades pincipales del objeto. Esto sin embargo se hace en el entorno de la simulación y no en el Xform padre. Esto se debe a que el motor físico toma dichos valores desde ahí.

Para ello utilizamos el atributo assets.RigidObject.data.default_root_state para obtener su estado por defecto. Este estado estandar se puede configurar con el atributo [assets.RigidObjectCfg.init_state](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.assets.html#isaaclab.assets.RigidObjectCfg.init_state). Una vez obtenido modificamos dicho parametro configurando el estado raiz que queramos mediante [assets.RigidObject.write_root_velocity_to_sim()](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.assets.html#isaaclab.assets.RigidObject.write_root_velocity_to_sim) y [assets.RigidObject.write_root_pose_to_sim()](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.assets.html#isaaclab.assets.RigidObject.write_root_pose_to_sim)

    # reset root state
            root_state = cone_object.data.default_root_state.clone()
            # sample a random position on a cylinder around the origins
            root_state[:, :3] += origins
            root_state[:, :3] += math_utils.sample_cylinder(
                radius=0.1, h_range=(0.25, 0.5), size=cone_object.num_instances, device=cone_object.device
            )
            # write root state to simulation
            cone_object.write_root_pose_to_sim(root_state[:, :7])
            cone_object.write_root_velocity_to_sim(root_state[:, 7:])
            # reset buffers
            cone_object.reset()
        
### Avanzar la simulación
Para avanzar la simulación utilizamos el método [assets.RigidObject.write_data_to_sim()](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.assets.html#isaaclab.assets.RigidObject.write_data_to_sim). Este método actualiza datos externos al buffer de la simulación, como por ejemplo fuerzas externas.

    # apply sim data
    cone_object.write_data_to_sim()


### Actualizar el estado
Por último, debemos actualizar los estados de los objetos en [assets.RigidObject.data](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.assets.html#isaaclab.assets.RigidObject.data). Esto a la vez se hace mediante el método [assets.RigidObject.update()](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.assets.html#isaaclab.assets.RigidObject.update)

        # update buffers
        cone_object.update(sim_dt)