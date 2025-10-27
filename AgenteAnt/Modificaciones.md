# Mejoras

Vamos a estudiar una serie de mejoras al ejemplo propuesto por IsaacLab de la araña. Esto con el objetivo de futuros avances en el proyecto Tarantula, ahora en desarrollo. 

## Terreno,

Nuestro primer objetivo va a ser generar un terreno más realista. El terreno actual es un plano básico. Nuestra idea es mejorar esto, incluyendo un terreno rugoso, con imperfecciones. Para ello, deberemos retocar la variable terrain de nuestra clase AntEnvCfg.

### Creación de un proyecto

Primero, crearemos un proyecto donde contener estas nuevas mejoras, apartadas de nuestro ejemplo principal. Para ello, llevaremos los archivos referentes a esta tarea al nuevo proyecto. (Pendiente)

### Clase Ant_Rough

Ahora crearemos una nueva clase Ant_Rough que definirá nuestro nueva tarea. Siguiendo la guía para modificar archivos directos, copiamos el archivo ant y modificamos sus nombres a RoughAntEnvCfg y RoughAntEnv. Una vez tenemos el archivo creado y los nombres modificados procedemos a modificar el terreno.

Nos centramos ahora en la línea 35 del programa, en la variable terrain. Mantendremos las variables physics material, prim_path y debug_vis, pues nos servirán para ambos terrenos. El prim_path es el adecuado para el suelo en el que trabajamos, no hace falta activar la variable debug y el grupo de colisión es el mismo que el de la araña. Las variable que deberemos modificar será terrain type, indicando mediante el string "generate" que diseñaremos un terreno propio. Una vez cambiemos esta variable, deberemos especificar el tipo de terreno, lo cual haremos a través de la variable RANDOM_ROUGH_CFG, de tipo TerrainGenerator, y definida en el mismo archivo. Si quisiesemos incluir en más agentes este terreno, lo mejor sería definirlo en un archivo a parte, para así poder importalo a otros agentes. Sin embargo, al ser específico para esta aplicación, lo indicamos en este mismo archivo. Para ello, deberemos importar la clase TerrainGeneratorCfg, la cual nos permite diseñar el terreno. Dentro de esta nueva clase, definiremos los siguientes parametros:
- Definiremos una primera superficie de 20 metros cuadrados mediante la variable size.
- Definiremos una frontera de 20 metros entre los distintos terrenos de entrenamiento.
- Defiriremos una matriz de 10x20 subterrenos como base, aunque luego se modificará según el número de utilizaremos la clase HFRandomUniformTerrain. Este deberemos importarlo desde el grupo isaaclab terrains, al igual que el TerrainGeneratorCfg. Dentro de esta clase definiremos otra serie de variables: proportion, definida a 1 al ser el único terreno; noise_range, la diferencia máxima de alturas, definida a 0.2 y 0.10 metros; noise_step, la discretizacion del terreno, definida a 0.05 metros.

Con estas variables definidas tendríamos nuestro suelo generado. Solo quedaría definir la nueva tarea en el init correspondiente.

Para ello utilizaremos el metodo register de gym. Le daremos el nombre "Isaac-Ant-Direct-Rough-v0"
