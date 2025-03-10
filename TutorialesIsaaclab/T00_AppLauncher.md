# Vista en profundidad de AppLauncher
La clase AppLauncher es un wrapper de SimulationApp que simplifica el proceso de configuración. De este modo nos presenta con una interfaz capaz de manejar gran variedad de casos. Para ellos se utilizan CLI (mecanismos de comunicación con el sistema a través de teclado) y con banderas de variables entorno (envar flags) que se juntan con argumentos CLI definidos por el usuario, todo ello mientras se envian argumentos dirigidos a Simulation App.

### Añadir argumentos al argpaser
En este tutorial vamos a añadir tres argumentos especificados en el script a un argparse.ArgumentPaser. --height y --width son absorbidos por Simulation App mientras que --size se junta con la interfaz de AppLauncher. 

    import argparse

    from isaaclab.app import AppLauncher

    # create argparser
    parser = argparse.ArgumentParser(description="Tutorial on running IsaacSim via the AppLauncher.")
    parser.add_argument("--size", type=float, default=1.0, help="Side-length of cuboid")

    # SimulationApp arguments [nvidia simulation](https://docs.omniverse.nvidia.com/py/isaacsim/source/isaacsim.simulation_app/docs/index.html?highlight=simulationapp#isaacsim.simulation_app.SimulationApp)
    parser.add_argument(
        "--width", type=int, default=1280, help="Width of the viewport and generated images. Defaults to 1280"
    )
    parser.add_argument(
        "--height", type=int, default=720, help="Height of the viewport and generated images. Defaults to 720"
    )

    # append AppLauncher cli args
    AppLauncher.add_app_launcher_args(parser)

    # parse the arguments
    args_cli = parser.parse_args()

    # launch omniverse app
    app_launcher = AppLauncher(args_cli)
    simulation_app = app_launcher.app

### Utilización variables de entorno
Los argumentos de AppLauncher tienen variables de entorno por defecto, las cuales vienen detalladas en [isaaclab.app](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.app.html#module-isaaclab.app). 

El soporte de AppLauncher para estas variables es simplemente para poder configurar una configuración básica, no obstante, de incluir estos argumentos por CLI se sobreescribirán.

Estos argumentos se pueden utilizar para cualquier script que empiece configuranco el AppLauncher, a excepción de --enable_cameras. Esta configuración crea una pipeline para hacer el render offscreen. Sin embargo solo es compatible con isaaclab.sim.SimulationContext