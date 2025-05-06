Se ha encontrado un problema en una de las recompensas en la tarea pull. Parece ser que una de estas se ha ido al infinito.

Para entrar a valorar donde esta el problema miraremos en los sensores de contacto, que podrían estar mal definidos, y en las recompensas, que podrían estar causando problemas.

Los archivos problemáticos son la task para el Robohabilis push object.

Al realizar la simulación en mi ordenador no se detecto el fallo que cancelaba la simulación, sin embargo se detectaron posibles ámbitos de mejora.
- El robot arrastra la herramienta. Se podría eliminar poniendo como condición que la herramienta este levantada para empujar o reajustando los pesos.
- Se detecta que la recompensa del empuje se genera mucho antes de que este se de. Habrá que entrar a valorar como se ejecuta y porque se activa.
- El robot contacta con el suelo impidiendole avanzar. Posibilidad de incluir una penalización por tocar el suelo.

### Planteamiento

Se debe confirmar con investigador que el problema sea de su ordenador y grabar el resultado para futuras aportaciones.

Se debe resolver los tres problemas propuestos sin perjudicar el funcionamiento actual.
