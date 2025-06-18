### Fuente
Sim-to-Real Transfer in Deep Reinforcement Learning for Robotics: a Survey

### Randomización del dominio

La randomización del dominio es se basa en la idea de en vez de realizar un modelo detallado de la realidad, se podría randomizar los parametros de la simulación de modo que se contemplen todas la distribución del mundo real. 

Se puede dividir en dos tipos de randomización, visual o dinámica. La randomización visual tiene su implementación en el uso de cámaras para detectar, por ejemplo, la localización de objetos. En nuestro caso, al centrarnos principalmente en el movimiento del robot, tendremos en cuenta la randomización dinámica, que se ocupa de propiedades como la fricción o la rigidez.


### Isaaclab

Isaaclab provee de distintas funciones para hacer una randomización del dominio.
