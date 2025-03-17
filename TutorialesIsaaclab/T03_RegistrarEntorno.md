# Registrar un entorno
En los tutoriales anteriores hemos visto como crear un entorno. Este entorno luego se instanciaba manualmente importando la clase del entorno y su clase de configuración. Nuestro objetivo ahora es utilizar la función gymnasium.register() para registrar entornos en un registro de gymnasium. Esto nos permite utilizar la función gymnasium.make() para crear los entornos.

La clase envs.ManagerBasedRLEnv hereda de [gymnasium.Env](https://gymnasium.farama.org/api/env/#gymnasium.Env). Sin embargo, envs.ManagerBasedRLEnv implementa un entorno vectorizado, lo que significa que puede instanciar múltiples entornos en un mismo proceso ejecutandose a la vez. De manera similar, envs.DirectRLEnv también hereda de gymnasium.ENV.

