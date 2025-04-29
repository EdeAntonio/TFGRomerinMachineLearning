# Configuración del Robot Ant

En este documento se explica como se define la configuración del robot ant, la cual se utiliza en la configuración del entorno ant.

Antes de comenzar, se importan todas las dependencias que necesitaremos para configurar la articulación. Entre ellas se encuentro el nucleo central de isaaclab, de donde extraeremos el archivo usd, o las distiontas herramientas de simulación.

## Configuración de la articulación
Para definir dicha configuración se implementa la clase ArticulationCfg, la cual se estudió a fondo en el tutorial [T01_InteractuarArticulación](TutorialesIsaaclab/T01_InteractuarArticulacion.md).

Ahora vamos a estudiar esta instaciación concreta.

### Prim Path

Primero, como se acostrumbra hacer, se define la ruta en la cual se guradará el prim de la articulación. Como podemos ver se utiliza una cadena formateada para que se pueda utilizar en distintos entornos. La expresión {ENV_REGEX_NS} se sustituirá en cada implementación por el namespace del entorno donde se utilice.

### Spawn

Seguidamente se define el spawn, que define como se implementará la articulación. Para esta variable spawn se implementa la clase [UsdFileCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.sim.spawners.html#isaaclab.sim.spawners.from_files.UrdfFileCfg), ya que queremos importar la configuración del prim desde un archivo USD. 

Primero, asignamos la variable USD path al archivo usd de ant, situado dentro del nucleo de Isaac. Una vez definido el archivo pasamos a definir las propiedades rígidas de la articulación mediante la clase [RigidBodyProperties](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.sim.schemas.html#isaaclab.sim.schemas.RigidBodyPropertiesCfg). Dentro de esta propia configuración, se asegura de la existencia de gravedad, la velocidad máxima a la que se separan los objetos al colisionar (maximum_depenetration_velocity) y se habilitan las fuerzas giroscópicas.

Segundo, declaramos las propiedades de la articulación, mediante la clase [ArticulationRootPropertiesCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.sim.schemas.html#isaaclab.sim.schemas.ArticulationRootPropertiesCfg). Declaramos las siguientes caracterínticas:
- enabled_self_collisions : variable que indica si se permiten colisiones entre las propias partes del robot. 
- solver_position_iteration_count : define la cantidad de pasos de simulación en los que se intenta corregir errores físicos. Un valor alto mejora la calidad de la simulación pero aumenta el gasto computacional.
- solver_velocity_iteration_count : del mismo modo que la variable anterior, indica el numero de pasos de simulación en los que se intenta resolver problemas con la velocidad.
- sleep_threshold : energía kinética con masa normalizada por debajo de la cual se desactiva el actuador de la articulación.
- stabilization:_threashold : energía kinética con masa normalizada por debajo de la cual el motor físico tienede a estabilizar la articulación, evitando micro movimientos es posibles momentos de reposo.

Por último, definimos la variable copy_from_source. En este caso se le asigna un valor falso, lo que indica que se utiliza el archivo directamente sin realizar una copia. Esto es útil cuando queremos utilizar el archivo usd sin modificarlo. Si se quisiese modificar dinámicamente el archivo, debería asignarse un valor verdadero. De este modo se podría modificar el archivo sin comprometer su fuente original.

### Init State
La clase init_state, dentro de la clase ArticulationCfg, define el estado inicial de la configuración. En este caso definimos los siguientes atributos de la clase:
- pos : indica la posición del origen del robot dentro de la referencia de la simulación.
- joint_pos :  define la postura de la articulación definiendo la rotación en radianes de la articulación en radianes. Podemos ver como se indica la articulación y el valor de la rotación en un formato de diccionario. Cabe resaltar que al indicar ".*_leg" estamos asignando dicho valor a todas las articulaciones que terminen en _leg, cogiendo asi todas las piernas a la vez.

### Actuators
Por último, se debe definir los actuadores que se van a utilizar para cada articulación del robot. Estos actuadores se almacenan en un diccionario con los distintos grupos de actuadores. Como pudimos ver en la parte de actuadores del documento [ApuntesIsaacLabBases](../ApuntesIsaacLabBases.md), hay veces en el que merece la pena tener dos grupos de actuadores, como por ejemplo en un brazo robótico (uno para la cadena cinemática y otro para el gripper). En este caso solo tenemos un grupo, ya que todos los actuadores de la araña se comportan de manera similar.

En este caso, se utiliza la clase ImplicitAtuatorCfgm, ya que utilizaremos los actuadores ideales del siulador gráfico. Si quisiesemos importar modelos externos para los actuadores deberíamos utilizar los actuadores explicitos. Dentro de esta clase definimos distintos atributos atributos.
- joint_names_expr : Esta variable lista las articulaciones que se incluirán en este grupo de actuadores. En este caso, mediante la cadena ".*" incluimos todas las aticulaciones.
- stiffnes : Define la rigidez de los actuadores (p-gain). La rigidez es la fuerza necesaria de un actuador para realizar un desplazamiento.
- damping : Define el amortiguamiento de los actuadores. El amortiguamiento 



