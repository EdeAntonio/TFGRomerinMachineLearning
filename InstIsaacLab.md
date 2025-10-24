# Instalación de IsaacLab.

En este documento, se guiará a través de la instalación de IsaacLab. Esta guía viene derivada de la propia [documentación de IsaacLab](https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/pip_installation.html). Se relatará también a través de los problemas que se encuentren. Se usará la instalación mediante Pip dentro de un sistema Linux. Se intentará que las aplicaciones esten disponibles para todos los usuarios.

Si se quiere utilizar los entornos ya implementados, vaya al final de este documento.

# Requerimentos.

El primer paso es comprobar la versión de GLIBC. GLIBC es la biblioteca estándar del lenguaje C. Para comprobar la versión utilizamos el comando: ldd --version. La versión debe ser GLIBC 2.35++.

# Instalación de Conda.

Una buena práctica para respetar las dependencias de python y evitar posibles conflictos es usar entornos virtual. Los entornos virtuales confinan todas las instalaciones al entorno. Es decir, mientras estemos fuera de ese entorno, no se accederá a lo que hayamos instalado dentro de el. Esto hará que no podamos usar IsaacSim o IsaacLab fuera de este entorno. Sin embargo, de este modo evitaremos posibles conflictos de dependencias en python.

Para la creación y manejo de entornos usaremos Miniconda3. Instalaremos este paquete de modo que todos los usuarios tengan acceso a él y puedan utilizar y crear entornos. Primero, descargaremos de la red los paquetes referentes a este programa.

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

Una vez descargados los archivos, instalamos el programa con el comando Bash. Ejecutaremos dicha sentencia con priviligios de superusuario. Una vez comience la instalación, tomaremos como ruta el directorio /opt/miniconda. Le indicaremos al final yes, para que conda se active siempre que abramos una terminal.

```bash
sudo bash Miniconda3-latest-Linux-x86_64.sh
```

Lo siguiente que haremos será dar permisos a todos los usuarios. Esto es muy importante. Con los siguientes comandos haremos que todos los usuarios puedan usar conda, pero no alterar su instalación. También incluiremos un comando para que todos puedan crear entornos.

```bash
sudo chown -R root:root /opt/miniconda
sudo chmod -R a+rX /opt/miniconda
sudo chmod -R a+w /opt/miniconda/pkgs
```

Para que ahora podamos acceder a conda desde cualquier repositorio deberemos incluirlo en el path. Para ello deberemos modificar el archivo /etc/profile.d/conda.sh incluyendole la sentencia: 

```sh
#!/bin/bash
export PATH="/opt/miniconda/bin:$PATH"
```

Una vez incluido guardaremos el archivo y ejecutaremos un comando para que todos los usuarios tengan conda en su PATH automáticamente. Los comandos para hacerlo serán los siguientes:

```bash
sudo nano /etc/profile.d/conda.sh
sudo chmod +x /etc/profile.d/conda.sh
```

Una vez hayamos realizado esto, conda estará accesible para todos los usuarios. Para verificar esto, recargamos el entorno y verificamos la versión de conda.

```bash
source /etc/profile.d/conda.sh
conda --version
```

# Instalación de IsaacSim.

Ahora, vamos a instalar IsaacSim en un entorno aislado. Primero creamos un entorno en conda para este propósito. Una vez creado, entraremos en él y comenzaremos con la instalación.

```bash
conda create -n env_isaacsim python=3.11
conda activate env_isaacsim
```

Seguidamente, deberemos actualizar la versión de Pip.

```bash
pip install --upgrade pip
```

También deberemos instalar una versión de Cuda para pytorch. 

```bash
pip install torch==2.7.0 torchvision==0.22.0 --index-url https://download.pytorch.org/whl/cu128
```

Para este paso, y la consecuente instalación, debemos estar en posesión de una tarjeta gráfica nvidia y haber configurado correctamente los drives. En nuestro caso, utilizamos una tarjeta RTX 3060. Esta no es suficiente para poder ejecutar simulaciones grandes. El requerimento mínimo para IsaacLab es de una RTX 4080 y el recomendado una RTX 5080.

Si hemos podido intalar correctamente la versión Cuda, podemos continuar con la instalación de IsaacSim. Instalamos entonces los paquetes correspondientes.

```bash
pip install "isaacsim[all,extscache]==5.0.0" --extra-index-url https://pypi.nvidia.com
```

Una vez terminada la instalación, verificaremos que el simulador se ejecute correctamente. Usaremos para esto directamente el comando: isaacsim. Al ser la primera vez que se abre tardará un poco más de lo habitual. Si se abre correctamente, entonces estamos preparados para instalar IsaacSim.

# Instalación de IsaacLab.

Ahora crearemos un entorno llamado env_isaaclab donde instalaremos el programa. Para ello clonaremos el entorno anterior en uno nuevo llamado env_isaaclab. Para estos primeros entornos base usaremos clonación. Esta clonación mejora la velocidad y la robustez, sin embargo, ocupan mucho espacio. Para los entornos derivados de este los exportaremos directamente.

´´´bash
conda create -n env_isaaclab --clone env_isaacsim
´´´

Una vez configurado el entorno comenzamos la clonación. Primero, clonaremos el repositorio de IsaacLab en nuestro ordenador.

´´´bash
conda create -n env_isaaclab --clone env_isaacsim
´´´

IsaacLab provee de un archivo .sh para facilitar la instalación de esta extensión. Utilizaremos este fichero para instalarlo y apt para las dependencias. Todas estas instalaciones las haremos dentro de nuestro entorno virtual env_isaaclab.

´´´bash
conda activate env_isaaclab
sudo apt install cmake build-essential
cd IsaacLab
./isaaclab.sh --install # or "./isaaclab.sh -i"
´´´

Si la instalación se ha realizado correctamente, deberíamos poder verificar su funcionamiento y comenzar a trabajar en ello. Si se quisiese intalar más paquetes se recomienda crear un nuevo entorno para no comprometer el original. Veremos como hacer esto en el siguiente apartado.