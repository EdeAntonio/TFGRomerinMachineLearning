# Entorno locomoción directo

El entorno de locomoción directo es el entorno padre para todos los entornos de locomoción de Isaaclab. Este entorno sirve como plantilla para el resto de entornos creados para este tipo de tarea. Como podemos ver en el entorno de la araña, a la hora de definir su entorno final, este hereda de este entorno padre. 

Esta clase a su vez, hereda de la clase DirectRLEnv, que establece las funcionalidades principales de este tipo de entornos.

Vamos a estudiar este entorno del cual luego entenderemos como funciona el entorno de la araña.

### Variable cfg

Primero de todo se crea una variable cfg que acepta únicamente clases DirectRLEnvCfg. De este modo, se utiliza una configuración como la vista anterior mente para configurar nuestro entorno dependiendo de la clase configuración.

### Función init

La función init es la función que se ejecuta al crear una clase de este tipo. De este modo, establecemos las variables que necesitará la clase para comenzar la simulación. Esta función recibe la propia clase, la configuración, el modo de renderización (que como estándar queda vacío) y el diccionario con los argumentos.

Más adelante entraremos a establecer para que sirve cada variable, en este momento únicamente se van a listar y como se obtienen.
- action_scale : establecida en la configuración.
- joint_gears : Se crea un tensor a partir de la variable joint_gears establecida en la configuración. Se utiliza un tipo de float de 32 bits. Se define también el dispositivo que se usa (CPU o GPU), el cual se almacena en los parametros de la simulación.
- motor_effort_ratio : se crea a partir del anterior, manteniendo su tamaño e instanciando a uno.
- _joint_dof_idx : se obtiene a partir de la función find_joints. Esta retorna un indice con todas las articulaciones, que se almacena en esta variable, y otra lista con metadatos que se ignora gracias al ", _".
- potentials : Almacena un tensor en 0 con dimensión igual al número de entornos y con formato float32. También define el dispositivo con el que se va a usar.
- prev_potentials : Almacena otro tensor creado a 0 en función de la dimensión del anterior.
- targets : almacena un tensor creado de la siguiente manera. Se crea un tensor a partir del arrat [1000, 0, 0], se repite este array 1 vez a través de un número de dimensiones igual al número de entornos, formando un tensor (num_envs, 3). Seguidamente se suma a este el origen de los entornos.
- start_rotation : Almacena un tensor del array [1, 0, 0, 0]
- up_vec : almacena un tensor del tipo (num_envs, 3) con el array [0, 0, 1]. Esta variable indicará más adelante la dirección que representara la altura.
- heading_vec : almacena un vector del tipo (num_envs, 3) con el array [1, 0, 0]. Esta variable indicará la dirección que las arañas deben seguir.
- inv_start_rot : Crea un tensor del tipo (num_envs, 4) a partir del tensor start_rotation con sus tres últimas posiciones en regativo.
- basis_vec0 : Se almacena una copia del tensor heading_vec
- basis_vec1 : Se almacena una copia del tensor up_vec.

### Función setup_scene
En la función set up se definen las variables principales de la escena del entorno. Primero se define la variable robot en función de la clase de configuración guardada en la configuración de la araña. Luego se termina de definir la clase Terrain con el número de entornos y el espacio entre entornos. Una vez definida la clase se define la variable terrain mediante la clase terrain de la de configuración. Se define también como se van a copiar y replicar los entornos, desactivando la variable copy_from_source. Se define también el robot dentro de la variable scene. Por último, se incluyen las luces.

### Función _pre_physics_step 
