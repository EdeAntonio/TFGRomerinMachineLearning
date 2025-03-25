# Entrenamiento con un agente RL
Hasta ahora, hemos aprendido como definir una entorno de tarea RL, como registrarla en el 'gym' y a interactuar con ella usando agentes aleatorios. Ahora nuestro objetivo es que un agente RL resuelva una tarea.

Por un lado, aunque la clase [envs.ManagerBasedRLEnv](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.envs.html#isaaclab.envs.ManagerBasedRLEnv) se ajuste a la interfaz de [gymnasium.Env](https://gymnasium.farama.org/api/env/#gymnasium.Env), esta no es exactamente un entorno 'gym'. Esto es debido a que sus entradas y salidas son tensores, cuya primera dimensión depende del numero de instancias.

Además, las distintas librería de aprendizaje por refuerzo, tienen grandes variaciones entre ellas, por lo que no tiene sentido tener una interfaz común. Para solucionar este problema, se declaran una serie de wrappers, los cuales nos permitirán acceder a las distintas herramientas de estas librerías.

### Skrl Wrapper
La clase, la cual funciona como wrapper para esta librería, se llama [SkrlVecEnvWrapper](https://isaac-sim.github.io/IsaacLab/main/source/api/lab_rl/isaaclab_rl.html#isaaclab_rl.skrl.SkrlVecEnvWrapper).

```python
SkrlVecEnvWrapper(env[, ml_framework, wrapper])
```

Esta implementación solo sirve para mantener la compatibilidad con la librería. El entrenamiento se definirá luego mediante esta (estudio de la librería SKRL). Internamente esta llama a la función wrap_env()

Los parametros de esta función son:

- env : El entorno que envuelve.
- ml_framework : La herramienta de ML que se va a utilizar. Por defecto "torch"
- wrapper : El wrapper a utilizar, el cual por defecto será 'isaaclab'