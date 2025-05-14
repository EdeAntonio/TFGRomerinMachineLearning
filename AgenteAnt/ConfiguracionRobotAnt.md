# Configuración del Robot Ant

En este documento se explica como se define la configuración del robot ant, la cual se utiliza en la configuración del entorno ant.

Antes de comenzar, se importan todas las dependencias que necesitaremos para configurar la articulación. Entre ellas se encuentro el nucleo central de isaaclab, de donde extraeremos el archivo usd, o las distiontas herramientas de simulación.

### Configuración de la articulación
Para definir dicha configuración se implementa la clase ArticulationCfg, la cual se estudió a fondo en el tutorial [T01_InteractuarArticulación](TutorialesIsaaclab/T01_InteractuarArticulacion.md).

Ahora vamos a estudiar esta instaciación concreta.

Primero, como se acostrumbra hacer, se define la ruta en la cual se guradará el prim de la articulación. Como podemos ver se utiliza una cadena formateada para que se pueda utilizar en distintos entornos. La expresión {ENV_REGEX_NS} se sustituirá en cada implementación por el namespace del entorno donde se utilice.

Seguidamente se define el spawn, que define como se implementará la articulación. Para esta variable spawn se implementa la clase [UsdFileCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.sim.spawners.html#isaaclab.sim.spawners.from_files.UrdfFileCfg), ya que queremos importar la configuración del prim desde un archivo USD. Primero, asignamos la variable USD path al archivo usd de ant, situado dentro del nucleo de Isaac. Una vez definido el archivo pasamos a definir las propiedades rígidas de la articulación mediante la clase [RigidBodyProperties](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.sim.schemas.html#isaaclab.sim.schemas.RigidBodyPropertiesCfg). Dentro de esta propia configuración, se asegura de la existencia de gravedad, la velocidad máxima a la que se separan los objetos al colisionar (maximum_depenetration_velocity) y se habilitan las fuerzas giroscópicas.


Primero, como se acostrumbra hacer, se define la ruta en la cual se guradará el prim de la articulación. Como podemos ver se utiliza una cadena formateada para que se pueda utilizar en distintos entornos. La expresión {ENV_REGEX_NS} se sustituirá en cada implementación por el namespace del entorno donde se utilice.

Seguidamente se define el spawn, que define como se implementará la articulación. Para esta variable spawn se implementa la clase [UsdFileCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.sim.spawners.html#isaaclab.sim.spawners.from_files.UrdfFileCfg), ya que queremos importar la configuración del prim desde un archivo USD. Primero, asignamos la variable USD path al archivo usd de ant, situado dentro del nucleo de Isaac. Una vez definido el archivo pasamos a definir las propiedades rígidas de la articulación mediante la clase [RigidBodyProperties](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.sim.schemas.html#isaaclab.sim.schemas.RigidBodyPropertiesCfg). Dentro de esta propia configuración, se asegura de la existencia de gravedad, la velocidad máxima a la que se separan los objetos al colisionar (maximum_depenetration_velocity) y se habilitan las fuerzas giroscópicas.

