# Docker

## ¿Que es Docker?
Docker es una herramienta que se encarga de la creación de contenedores. Un contenedor se puede imaginar como una caja cerrada en la que están todos los elementos principales para ejecutar un programa. Además, mantine puede mantener una configuración de dicha aplicación, lo que permite ejecutar el programa de la misma manera en cualquier lugar.

Docker proporciona una serie de herramientas para manejar el ciclo de un contenedor: 
- Se desarrolla una aplicación y sus componentes usando contenedores.
- El contenedor se convierte en una unidad de distribución y pruebas para la aplicación.
- Una vez listo, se lleva a producción, es decir, se ejecuta en el entorno real donde debe funcionar.

## Arquitectura Docker
La arquitectura Docker esta basada en una arquitectura cliente servidor. El cliente llama a un proceso demonio que se encarga de crear , ejecutar y distribuir los contendores. El cliente y el demonio se comunican usando una REST API, a través de UNIX sockets.

![EstructuraDocker](ImagenesRelevantes\EstructuraDocker.png)

El demonio docker (dockerd) recibe peticiones y maneja los objetos Docker. 

El cliente Docker es a través del cual se controla los contenedores. Este control se realiza mediante distintos comandos.

El Docker Desktop es una aplicación necesaria en Windows y macOS para trabajar con Docker. Incluye el demonio, el cliente, docker compose, una interfaz gráfica y herramientas adicionales. En Linux esta herramienta no es necesaria ya que Docker se intala directamente.

Un registro Docker se encarga de guardar las imagenes. Docker Hub es un registro público habilitado para cualquiera y es donde se mira por defecto.

### Objetos Docker
Una imagen es una plantilla que contiene las instrucciones para la creación de contenedores. Se puede crear una imagen a partir de otras o utilizar unas ya creadas por otros usuarios. 

Para crear una imagen se debe crear un DockerFile en el cual, con una sitaxis sencilla, se define la forma en la que se crea y ejecuta el contenedor. Cada instrucción crea una nueva capa en la imagen y, cuando esta se modifica, solo se ejecutan las capas cambiadas.

Por otro lado, un contenedor es una instancia ejecutable de la imagen. Se puede crear, ejecutar, parar, mover o eliminador utilizando las APIs de Docker. Se puede conectar una o más redes virtuales, incorporarla un almacenamiento o crear una imagen a partir del estado actual del contenedor. 

Recordatorio: Una API es una forma estandarizada para la comunicación entre programas.

Un contenedor viene definido por su imagen y por el resto de configuraciones que implementes en la creación. Cuando se elimina un contenedor todos los cambios en su estado que no hayan sido guardados en el almacenamiento permanente también se eliminan.

## Comando Docker Rub

Vamos a estudiar que sucede cuando ejecutamos el siguiente comando run:
    $ docker run -i -t ubuntu /bin/bash
1. Si no se tiene la imagen ubuntu, se recoge de la lista configurada como si se hubiese ejecutado un docker pull ubuntu.
2. Docker crea un nuevo contenedor.
3. Se coloca un sistema de escritura lectura en la capa final del contendor para que este pueda interactuar con los archivos locales.
4. Al no especificar ninguna red, Docker crea una interfaz de red y la conecta a la estándar. El contendor también se puede conectar a redes externas usando la conexión a red de la máquina huésped.
5. Docker inicia el contendor y ejecuta /bin/bash. Al utilizar -i y -t el contenedor se ejecuta de manera interactiva y acoplada a la terminal.
6. Al ejecutar el comando exit se corta el comando /bin/bash y se para el contenedor sin eliminarse. Se puede empezar de nuevo o eliminarlo.
