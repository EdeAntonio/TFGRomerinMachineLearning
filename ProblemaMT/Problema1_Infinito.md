Se ha encontrado un problema en una de las recompensas en la tarea pull. Parece ser que una de estas se ha ido al infinito.

Para entrar a valorar donde esta el problema miraremos en los sensores de contacto, que podrían estar mal definidos, y en las recompensas, que podrían estar causando problemas.

Los archivos problemáticos son la task para el Robohabilis push object.

Al realizar la simulación en mi ordenador no se detecto el fallo que cancelaba la simulación, sin embargo se detectaron posibles ámbitos de mejora.
- Se detecta que la recompensa del empuje se genera mucho antes de que este se de. Habrá que entrar a valorar como se ejecuta y porque se activa.

### Planteamiento

Se debe confirmar con investigador que el problema sea de su ordenador y grabar el resultado para futuras aportaciones.

Se debe resolver los tres problemas propuestos sin perjudicar el funcionamiento actual.

### Empuje

Para encontrar el problema por el cual se activa la recompensa de empuje sin empujar o tener un contacto válido comenzamos a realizar un debugging.

El debugging se centrará en la definición de la función con la cual se valora la recompensa, la cual se encuentra dentro de la carpeta mdp. 

Encontramos que no esta definida la función Squeeze.

Se ha realizado un debugging de la recompensa. Analizando la ejecución del código podemos ver como la lógica de la programación estaba correctamente ejecutada. Esta se desarrollaba sin ninguna incongruencia. Finalmente, se ha detectado que el fallo se encontraba en la propia configuración  del sensor de contacto, ya que detectaba contacto antes de que este se produjese. Esto se solucionó aportando un valor para la variable force threshold de 2.3. Este permitía detectar el contacto y eliminar los falsos positivos.
