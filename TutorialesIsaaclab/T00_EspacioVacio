# Crear un espacio vacío
### Lanzar el simulador
Para scrips the python aislados (standalone scripts) lo primero que debemos hacer es lanzar la simulación. Esto se debe hacer al principio ya que hay módulos de Isaaclab que dependen de esto.

Para hacer esto debemos importar la clase [app.AppLauncher](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.app.html#isaaclab.app.AppLauncher), que utiliza la clase [isaacsim.SimulationApp](https://docs.omniverse.nvidia.com/py/isaacsim/source/extensions/omni.isaac.kit/docs/index.html#isaacsim.SimulationApp) para lanzar el simulador. Esta clase nos provee de mecanismos para configurar el simulador.

    import argparse
    from isaaclab.app import AppLauncher

    # create argparser
    parser = argparse.ArgumentParser(description="Tutorial on creating an empty stage.")

    # append AppLauncher cli args
    AppLauncher.add_app_launcher_args(parser)

    # parse the arguments
    args_cli = parser.parse_args() //Lo convierte en variable

    # launch omniverse app
    app_launcher = AppLauncher(args_cli)
    simulation_app = app_launcher.app

En este código usamos la clase [argparse.ArgumentParser](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser) con el comando [app.AppLauncher.add_app_launcher_args](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.app.html#isaaclab.app.AppLauncher.add_app_launcher_args), el cual incluye una serie de argumentos adicionales para configurar la simulación.

### Importar los modulos de Python
Una vez configurada la simulación se pueden incluir distintos módulos para utilizar. En este tutorial se importaron los modulos de [isaaclab.sim](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.sim.html#module-isaaclab.sim), un paquete para operaciones con el simulador.

### Configuración del contexto de la simulación
El contexto de la simulación sirve para controlar el flujo de la simulación (paradas, pasos, reproducciones, etc.) y configurar la [escena física](https://docs.omniverse.nvidia.com/prod_extensions/prod_extensions/ext_physics.html#physics-scene).

Para configurar este contexto se utiliza la clase [sim.SimulationContext](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.sim.html#isaaclab.sim.SimulationContext) que nos permite configurar el contexto a través de la clase [sim.SimulationCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.sim.html#isaaclab.sim.SimulationCfg)

    # Initialize the simulation context
    sim_cfg = SimulationCfg(dt=0.01)
    sim = SimulationContext(sim_cfg)

    # Set main camera
    sim.set_camera_view([2.5, 2.5, 2.5], [0.0, 0.0, 0.0])

En este código se configura el contexto para un tiempo de renderizado de 0.01 segundos. También se posiciona el punto de vista.

### Simulación
La primera cosa que debemos hacer después de configurar la escena es llamar a la función sim.SimulationContext.reset(). Este método comienza la linea de tiempo y inicializa las físicas. También existe el método sim.SimulationContext.play() que inicializa la linea de tiempo pero no las físicas. Para realizar un paso usamos el método [sim.SimulationContext.step()](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.sim.html#isaaclab.sim.SimulationContext.step), que a su vez toma una argumento render (por defecto true) que especifica si se actualiza la simulación.

    # Play the simulator
    sim.reset()

    # Now we are ready!
    print("[INFO]: Setup complete...")

    # Simulate physics
    while simulation_app.is_running():

        # perform step
        sim.step()

### Cerrar la simulación
Por último la simulación se cierra con el método [isaacsim.SimulationApp.close()](https://docs.omniverse.nvidia.com/py/isaacsim/source/extensions/omni.isaac.kit/docs/index.html#isaacsim.SimulationApp.close) 

    # close sim app
    simulation_app.close()

