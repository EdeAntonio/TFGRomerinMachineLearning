# Añadir sensores a un robot

Añadir sensores a un robot es un metodo muy eficiente para obtener información acerca del entorno. Por ejemplo mediante un sensor de contacto se puede obtener información acerca de las colisiones con el entorno. 

## Explicación

En el tutorial T02_UtilizarEscenasInteractivas aprendimos a introducir elementos a la escena interactiva. Los sensoras se añaden de forma similar, heredando todos de la clase [sensors.SensorBase](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.sensors.html#isaaclab.sensors.SensorBase) y configurandose mediante sus propias clases de configuración. El tiempo de actualización, algo muy importante en los sensores, se define mediante la variable [sensors.SensorBaseCfg.update_period](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.sensors.html#isaaclab.sensors.SensorBaseCfg.update_period).

Los sensores pueden ser prims asociados con la escena o, como en el caso del sensor de contacto, estar asociados a un prim.

### Sensor de contacto

Los sensors de contacto se envuelven las fisicas de contacto de PhysX, comunicando a las API la información obtenida del robot. Para esto, el cuerpo rígido al que se adapta debe tener la posibilidad de transmitir esa información. Para ello se necesita declarar en true la variable [active_contact_sensors](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.sim.spawners.html#isaaclab.sim.spawners.RigidObjectSpawnerCfg.activate_contact_sensors) en la configuración del elemento.

