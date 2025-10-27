# Entorno Directo Agente Ant

### Importaciones

Primeramente, importamos las distintas herramientas y bibliotecas que vamos a utilizar. Entre ellas estan las herramientas de simulación, las clases de configuración, etc.

## Clase de configuración.

Una vez hemos realizado las distintas importaciones, podemos proceder a crear la clase de configuración.

Recordatorio: La clase de configuración es necesaria para más adelante concretar la clase de entorno.

### Entorno
Para el entorno se definen distintas características:
- Una longitud de episodio de 15 segundos
- Una decimation de 2. Esto quiere decir que se toman observaciones cada 2 pasos físicos, regulando la resolución
- Action_Scale a 2. *MIRAR MÁS ADELANTE*
- Se situa la dimensión de las acciones a 8 (action_space = 8), lo que quiere decir que habrá 8 acciones a definir.
- Se situa la dimensión de observaciones a 36 (observation_space), lo cual quiere decir que habrá 36 observaciones a realizar.
- Se define la dimensión de los estados a 0, por lo que no se definirá ninguno.

### Simulación

Una vez definidas las distintas variables del entorno, procedemos a definir dos variables para la simulación sim y terrain.

Por un lado, sim toma valores SimulationCfg, es decir, contiene la configuración de la simulación. Los valores proporcionados indican el paso de tiempo, 1/120 segundos,  y la resolución (render_interval) que será igual a la decimación.

Por otro lado, se define una variable terrain que define la configuración del terreno sobre la cual se va a trabajar. A continuación, entramos a estudiar la clase y su instanciación.

La clase TerrainCfg viene de la librería [Terrain Importer](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.terrains.html#). El terrain importer se encarga precismanete de crear un terreno para toda la simulación y dividirlo en subterrenos más fáciles de manejar. Dentro de estos terrenos se podrán definir distintos obstaculos y agentes.

En el terreno del ejemplo Ant encontramos distintas instanciaciones. 
- Prim_Path, define la ruta absoluta del USD del prima del terreno.
- terrain_type, define el tipo de terreno. Este puede ser "plane", "usd" o "generate"
- collision_group, selecciona el grupo de objetos con el que puede colisionar. Al indicar -1 lo incluye en el grupo primario.
- physics_material, variable la cual define el tipo de material que se va a utilizar. Recordemos que este podía ser de varios tipos, como se ve en los tutorial de [Interactuar con objetos rígidos](TutorialesIsaaclab/T01_InteractuarObjetoRigido.md). Dentro de esta variable se definen sus carateríticas a través de la configuración de cuerpo rígido, indicando las características de la fricción y restitución.
- Debug_vis, determina si se pueden visualizar los origenes de los entornos.

### Escena

Seguidamente definimos la configuración de la escena principal, definiendo el número de entornos y el espacio entre ellos, replicando también sus físicas.

### Robot

La variable Robot es un tema clave dentro de esta configuración, ya que describe como es el robot que estamos utilizando. En este caso, para instanciar nuestro robot utilizamos una configuración importada. Esta configuración estás definida en isaaclab_assets.robots.ant. Esta configuración se explica en el archivo [ConfiguracionRobotAnt](AgenteAnt/ConfiguracionRobotAnt.md).

