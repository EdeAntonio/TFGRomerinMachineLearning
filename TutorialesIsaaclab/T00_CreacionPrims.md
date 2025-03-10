# Introducir Primitivos a una simulación
La descripción de escenas en Isaaclab esta basada en un software y formato de fichero llamado USD, el cual nos permite describir objetos 3D.

Los principales conceptos de este sistema son:
- Primitivos (Prims): La unidad básica del USD. Pueden ser visto como nodos que pueden representar una malla (mesh), un punto de luz, una cámara o una transformación (transform). Estos primitivas se pueden juntar en grupos.
- Atributos: Son las propiedades de los prims.
- Relaciones: Son las conexiones entre los prims, que se pueden ver como punteros a otros prims.

Una colección de primitivos, con sus atributos y relaciones, se denomina escena USD (USD stage). Para facilitar la creación de escenarios isaaclab aporta encima de las USD APIs (recodermos que APIs son mecanismo de comunicación de software). Están incluidas en el módulo sim.spawners.

Cuando queremos introducir un prim a escena debemos primero configurarlo mediante la instanciación de una clase. Una vez configurada podemos prodecer a introducirlo en la simulación.

    # Create a configuration class instance
    cfg = MyPrimCfg()
    prim_path = "/path/to/prim"

    # Spawn the prim into the scene using the corresponding spawner function
    spawn_my_prim(prim_path, cfg, translation=[0, 0, 0], orientation=[1, 0, 0, 0], scale=[1, 1, 1])
    
    # OR

    # Use the spawner function directly from the configuration class
    cfg.func(prim_path, cfg, translation=[0, 0, 0], orientation=[1, 0, 0, 0], scale=[1, 1, 1])

### Crear un plano en el suelo.
Podemos crear un plano en el suelo a través de la clase [GroundPlaneCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.sim.spawners.html#isaaclab.sim.spawners.from_files.GroundPlaneCfg)

    # Ground-plane
    cfg_ground = sim_utils.GroundPlaneCfg()
    cfg_ground.func("/World/defaultGroundPlane", cfg_ground)

### Crear luces
Se pueden crear distintos tipos de pims de luces a nuestra escena, como se muestra en el siguiente [video](https://youtu.be/c7qyI8pZvF4?feature=shared). En este caso se crea una luz distante, es decir una luz que viene desde el infinito.

    # spawn distant light
    cfg_light_distant = sim_utils.DistantLightCfg(
        intensity=3000.0,
        color=(0.75, 0.75, 0.75),
    )
    cfg_light_distant.func("/World/lightDistant", cfg_light_distant, translation=(1, 0, 10))

### Creación de figuras primitivas
Para crear una figura primaria debemos crear primero un transform prim, el cual agrupa los prims formando objetos.

    # create a new xform prim for all objects to be spawned under
    prim_utils.create_prim("/World/Objects", "Xform")

Seguidamente podemos crear conos con la función [ConeCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.sim.spawners.html#isaaclab.sim.spawners.shapes.ConeCfg). Por defecto las propiedades físicas y de materiales estan desabilitadas. Estos primeros conos creados serán solamente visuales por lo tanto.

    # spawn a red cone
    cfg_cone = sim_utils.ConeCfg(
        radius=0.15,
        height=0.5,
        visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(1.0, 0.0, 0.0)),
    )
    cfg_cone.func("/World/Objects/Cone1", cfg_cone, translation=(-1.0, 1.0, 1.0))
    cfg_cone.func("/World/Objects/Cone2", cfg_cone, translation=(-1.0, -1.0, 1.0))

Para introducir un cono con físicas. Podemos especificar la masa, la fricción y la restitución del cono. Si no se especifican se dejan los valores por defecto de las físcas USD, lo importante es introducir las propiedades en rigid_props.

    # spawn a green cone with colliders and rigid body
    cfg_cone_rigid = sim_utils.ConeCfg(
        radius=0.15,
        height=0.5,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(),
        mass_props=sim_utils.MassPropertiesCfg(mass=1.0),
        collision_props=sim_utils.CollisionPropertiesCfg(),
        visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.0, 1.0, 0.0)),
    )
    cfg_cone_rigid.func(
        "/World/Objects/ConeRigid", cfg_cone_rigid, translation=(-0.2, 0.0, 2.0), orientation=(0.5, 0.0, 0.5, 0.0)
    )

Por último podemos incluir objetos deformables. Estos permiten movimiento entre sus vertices, lo cual puede ser útil para simular cuerpos blandos. Para simular estos objetos se necesita simular por GPU y un objeto de malla (mesh).

    # spawn a blue cuboid with deformable body
    cfg_cuboid_deformable = sim_utils.MeshCuboidCfg(
        size=(0.2, 0.5, 0.2),
        deformable_props=sim_utils.DeformableBodyPropertiesCfg(),
        visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.0, 0.0, 1.0)),
        physics_material=sim_utils.DeformableBodyMaterialCfg(),
    )
    cfg_cuboid_deformable.func("/World/Objects/CuboidDeformable", cfg_cuboid_deformable, translation=(0.15, 0.0, 2.0))

### Creación desde fichero externo
Por último es posible crear prims a través de ficheros externos como USD, URDF, o OBJ files. En este caso se introduce un archivo USD de una mesa.

    # spawn a usd file of a table into the scene
    cfg = sim_utils.UsdFileCfg(usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/Mounts/SeattleLabTable/table_instanceable.usd")
    cfg.func("/World/Objects/Table", cfg, translation=(0.0, 0.0, 1.05))