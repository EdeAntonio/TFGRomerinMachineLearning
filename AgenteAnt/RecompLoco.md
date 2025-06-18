# Recompensas dentro de la configuración Ant

En el entrono directo de la configuración Ant "source/isaaclab_tasks/isaaclab_tasks/direct/ant/ant_env.py", observamos como se prepara la configuración básica del entorno, definiendo distintas variables como el robot o parametros de la simulación, pero en realidad, la estructura principal de nuestro entorno se define dentro de Locomotion.

Este pequeño apartado pretende explicar como funcionan las recompensas de locomoción en el caso directo. Estas recompensas se calculan a través de dos funciones principales.

En primer lugar, la función compute_intermidiate_values, ejecutadada dentro de la función de la clase LocomotionEnv, obtiene todos los valores necesarios para calcular las recompensas. A continuación, nombramos los valores más relevantes:
- to_target: Se calcula a partir de la diferencia entre el objetivo (targets) y la posición actual del torso (la cual se obtiene a partir de valores del robot.data). Cabe destacar que targets es un valor que se define en la función _init_ de la clase LocomotionEnv. En este caso simplemente ponen un punto lejos del target y llevan el robot hasta ahí. Seguidamente, iguala la z (:,2) a cero, para que no afecte en futuros cálculos.
- torso_quad: Es el cuaternario del torso, es decir su vector de rotación. Se calcula mediante la función compute_heading_and_up de isaacsim. Este cuaternario se basa en función a la variable to_target
- 

Recompensas:
- heading_reward: Da una recompensa siempre que heading_proj sea mayor de 0.8, sino da esa recompensa con un estándar de 0.8.
- up_reward: Da una recompensa si la proyección es mayor de 0.93, la cual es o el peso o nada, al inicializar a cero antes de calcular la recompensa.
- Coste energético
- Coste de acción
- Limite de grados de libertad
- Recompensa por estar vivo
- Recompensa por progresar: calculado a base de potenciales. Esto se calcula en compute_intermidiate rewards 
Todas las recompensas son del tipo (num env, 1).