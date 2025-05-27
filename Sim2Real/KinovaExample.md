# Ejemplo Kinova para sim2real

Se propone este ejemplo para valorar la implementicación de una política en un robot real.

https://github.com/louislelay/kinova_isaaclab_sim2real/tree/main?tab=readme-ov-file

La mécanica básica de este programa se centra en utilizar redes neuronales creadas en Isaaclab e implementarlas en ROS2 para ejecutarlas en un robot Kinova. La tarea que se utiliza para entrenar al robot es de alcance, donde el robot se mueve entre distintas posiciones.

### Ejecución de la tarea (run_task_reach)

En este primer archivo se configura el robot de modo que al mandarle posiciones vaya rotando entre ellas. En él se declara un callback que llamará a una función de la variable robot para calcular la posición en la que debe estar cada articulación todo el tiempo.

Esta variable robot se construye a partir de una reconstrucción de la política obtenida al entrenar.

### Reconstrucción de la política (gen3)

La política incluye tanto la política como tal, como distintas propiedades del robot.

En la inicialización de la clase principal del programa (Gen3ReachPolicy) se difinen el nombre de las articulaciones y la política que se va a cargar (acompañada de la configuración del entorno en yaml). La función que permite cargar la política (load_policy) se define en la clase padre. También se declaran otras variables como la escala de la acción, acción previa, commandos, etc.

Se define la forma de computar las observaciones, donde se declara la dimensión de las acciones en función del entorno de la política. También definimos de donde obtenemos estas observaciones.

Otra función importante en esta clase es la función forward, la cual se encarga de obtener las acciones pertinentes para realizar el siguiente paso del robot. Además, calcula la posición donde el robot debería encontrarse en función de la posición por defecto y la escala. También se muestra toda la información acerca de las acciones.También actualiza el contador de la política, el cual sirve para comparar con la decimación del simulador físico. Para calcular las acciones se utiliza la función _compute_action, la cual se define en la clase padre.

Por último, esta clase también tiene una función para actualuzar el estado de la postura del robot.
 
Esta clase hereda de la clase policy controller, la cual contiene el resto de funciones necesarias para controlar la política y utilizarla para calcular las acciones.

### Controlador de la política (policy_controller.py)

El controlador de políticas es la clase padre de la política especifica que hemos visto antes.

En esta clase se define la función load_policy. Esta clase recive la configuración del entorno y los pesos de la política obtenida (.yaml y .pt). Para ello, primero se abre el fichero del modelo .pt, cargándolo después con la función torch.jit.load() lo cual nos deja la red lista para utilizar. También se obtienen los distintos parametros para las articulaciones y el motor físico.

Una vez se tiene el archivo preparado el archivo se define el cálculo de las acciones. Para este, primero se trasforman las observaciones que se toman como parametros a tensor pyTorch, adpatando sus dimensiones. Luego estos se alimentan a la política para obtener las acciones a su salida, volviendo a adaptar sus dimensiones y combirtiendo de nuevo a numpy.


