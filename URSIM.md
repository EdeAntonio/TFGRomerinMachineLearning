# Instalación para el simulador URSIM

Al instalar el simulador URsim para ubuntu nos hemos encontrado con un problema en relación con varios aspectos de las dependencia, necesitando bibliotecas obsoletas en la versión actual de Ubuntu. Para solucionar este problema vamos a crear un contenedor en el cual se encontrará nuestro programa URSIM, con el cual nos comunicaremos a través de los archivos sim2real con el objetivo de controlar la simulación externamente.

### Dockerfile

Para crear el contenedor necesitamos un fichero dockerfile. Este fichero tiene la siguiente estructura:
- FROM: Definimos la imagen base en la que se asienta nuestro contenedor. En nuestro caso utilizaremos la versión de ubuntu:18.04 ya que tiene la dependencia libcurl13 necesaria para ejecutar la intalación.
- ENV: Define las varibles de entorno del contenedor. En este caso, definimos DEBIAN_FRONTEND como noninteractive, de modo que los diálogos no interrumpan el proceso de intalación.
- RUN: Se encarga de ejecutar comandos durante la construcción de la instalación. En esta parte realizamos tres cosas encadenadas. Primero, añadimos una arquitectura de 32 bits para algunas de las librerías que vamos a instalar; seguidamente, actualizamos los índices de los paquetes; y por último instalamos las librerías necesarias, incluyendo las dependencias de Java, librerías gráficas, redes, etc.
- RUN: Incluimos manualmente las librería que no nos permite instalar esta versión.
- RUN: En esta segundo comando RUN creamos un usuario para el contenedor, lo cual es necesario por temas de seguridad y aislamiento. Este usuario tendra la base de su shell basada en la bash y la home. 
- USER: Se cambia el usuario al recientemente creado.
- WORKDIR: Se establece el directorio en el que se va a trabajar.
- COPY: Se copia el archivo de instalación del directorio.
- RUN: Descomprimimos el archivo y ejecutamos la simulación.
- CMD: Se ejectua un primer comando BASH que se encarga de inciar la terminal.

### Creación del contenedor

Una vez tenermos creado nuestro dockerfile y lo tenemos almacenado en la carpeta del docker (en este caso urSIM), podemos proceder a crear el contenedor. Para ello, utilizamos el comando "docker build -t ursim-container ." el cual se encargará de leer y ejecutar el archivo Dockerfile. -t ursim-container da nombre al contenedor, mientras que el . indica el contexto del contenedor (lugar donde se encuentra el Dockerfile). Seguidamente, le permitos al contenedor acceder a xhost, de modo que pueda crear interfaces gráficas como ventanas. Por último, lanzamos el contenedor mediante la sentencia "docker run -it --rm --net=host -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix ursim-container". En esta sentencia, -it indican la continuadad de la entrada estándar stdin (-i interactive) y la asignación de una terminal (-t tty). Además, definimos el entorno de la pantalla host para que se muestren las app gráficas, establecemos el socket para la interfaz X (el canal de comunicación para los gráficos) y se conecta a la red del host para conectarse a servicios y simuladores sin problemas de red.
