# Guía para crear un Docker de IsaacLab

Primero, debemos instalar Docker Engine o Docker compose. Seguir instrucciones en la [guía original](https://isaac-sim.github.io/IsaacLab/main/source/deployment/docker.html)

### Organización del directorio

Para poder utilizar Isaaclab en un contenedor es imprescindible tener el directorio Docker. Este directorio contiene:
- Dockerfile.base : Define la imagen base con Isaaclab y sobrepone las dependencias con la imagen contenedor.
- docker-compose.yaml : Sirve para poder editar el código fuera de la aplicación y dentro del contenedor.
- .env.base : Guarda variables clave para la creación de los procesos principales.
- container.py : Configura y crea la imagen.

### Ejecutar el contenedor
El fichero container.py implementa paralelamnete varios comandos de docker compose. Cada uno acepta un comando específico, el cual, si no se da, se sobreentenderá como la imagen base. estos comandos son:
- start : Construye la imagen y ajusta el contedor en modo desacoplado (detached mode)
- enter : Crea un nuevo proceso bash en un contendor Isaaclab, del cual se puede salir sin desconfigurar el contenedor.
- config : Muestra el archivo compose.yaml, el cual es el resultado de los inputs del container.py start. Este comando es útil para  
- copy : Este comando copia los elementos logs, data_storage y docs/_build de sus volumenes correspondientes al directorio docker/artifacts.
- stop: Desconfigura el contenedor y lo retira.

