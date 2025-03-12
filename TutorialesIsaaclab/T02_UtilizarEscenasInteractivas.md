# Utilizar escenas interactivas
Hasta el momento se han creado los elementos de manera separada. Ahora con la clase [scene.InteractiveScene](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.scene.html#isaaclab.scene.InteractiveScene) se podrá crear y manejer prims a través de una interfaz común y rápida. Los principales beneficios de utilizar una escena interactiva son:
- Aliviar la necesidad de crear objetos de manera separada.
- Permitir el clonado de escenas prim para múltiples ecosistemas.
- Recoger todas las escenas en un solo objeto, haciendolo más fácil de manejar.

En este tutorial reemplazamos la variabl design_scene por un objeto scene.InteractiveScene. Aunque en este momento no sea necesario, cuando se incluyan más sensores o elementos se vuelve bastante útil.

### Configuración de la escena.
Una escena esta compuesta de un conjunto de entidades, cada una con su propia configuración. Esta se especifica mediante una clase que hereda de [scene.InteractiveScenesCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.scene.html#isaaclab.scene.InteractiveSceneCfg). Esta configuración luego se pasa a scene.InteractiveScene, el cual crea la escena mediante el constructor.

Por ejemplo para el cartpole encontramos la siguiente clase.

    ```python
    class CartpoleSceneCfg(InteractiveSceneCfg):
        """Configuration for a cart-pole scene."""

        # ground plane
        ground = AssetBaseCfg(prim_path="/World/defaultGroundPlane", spawn=sim_utils.GroundPlaneCfg())

        # lights
        dome_light = AssetBaseCfg(
        prim_path="/World/Light", spawn=sim_utils.DomeLightCfg(intensity=3000.0, color=(0.75, 0.75, 0.75))
        )

        # articulation
        cartpole: ArticulationCfg = CARTPOLE_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")
    ```

El nombre de las variables sevirá para más adelante acceder a ellas atracés de scene.InteractiveScene. También se debe resaltar que se usan distintos objetos de configuración para distintos elementos. Por un lado se usa [assets.AssetBaseCfg](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.assets.html#isaaclab.assets.AssetBaseCfg), para aquellos elementos con los que no se va a interactuar durante la simulación. Por otro lado se usa assets.ArticulationCfg, para aquellos elementos con los que si que vamos a interactuar.

Otro tema a tener en cuenta son los caminos para los distintos prims:
- Ground plane: /World/defaultGroundPlane
- Light source: /World/Light
- Cartpole: {ENV_REGEX_NS}/Robot

Estos caminos se utilizan para determinar su posición dentro de la escena USD. Por un lado, Ground plane y Light source utilizan caminos absolutos. Mientras tanto, Cartpole utiliza un camino relativo, donde EGV_REGEX_NS se copiará para todos los entornos. Este camino luego será sustituido por el consiguiente /World/envs/env_{i}, donde i será el número del entorno.

### Instanciación de las escenas.
Antes llamabamos a la función desing_scene para crear la escena. Ahora solo necesitaremos instanciar la clase scene.InteractiveScene y pasar la configuración que hemos creado.

    ```python
    # Design scene
    scene_cfg = CartpoleSceneCfg(num_envs=args_cli.num_envs, env_spacing=2.0)
    scene = InteractiveScene(scene_cfg)
    ```

### Acceder a elementos de la escena.
Como ya habíamos mencionado se pueden extraer elementos de la escena. Esto se hace mediante el operador [] y utilizando la palabra clave. Por ejemplo para el caso de nuestra articulación la palabra clave sería "cartpole"
    ```python
    # Extract scene entities
    # note: we only do this here for readability.
    robot = scene["cartpole"]

### Ejecución del bucle de la simulación.
El resto del código repite la estructura de los anteriores cósigos, variando, eso sí, los métodos utilizados.

- assets.Articulation.reset() ⟶ scene.InteractiveScene.reset()
- assets.Articulation.write_data_to_sim() ⟶ scene.InteractiveScene.write_data_to_sim()
- assets.Articulation.update() ⟶ scene.InteractiveScene.update()

Dentro de estos métodos se llamará a los que sustituye. De este modo si tuvieramos más robots no tendríamos que ejecutarlos uno a uno, con este método se ejecutarían todos.
