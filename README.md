Esta es un Ia que usa sumo-gui para recrear trafico de lineas 
  SE NECESITA TENER INSATALDO sumo y descargar los codigos siguientes del proyecto por ultimo
  Tiene varias warnings las cuales son las siguientes no afectan al codigo pero si son para mejorar la Ia
        1-faltan luces amarrillas en los intercambions estas no afectan para nada a la ia
        2-algunos cambios son repentinos lo cual hace que unos veiculos fenen de repente esto se mejora agregando mas tiempo al semaforo 

  por ultimo lo siguiente es una gran descrripcion de como funciona
    📁 Archivos principales
1. Mi_red.net.xml

Es la red de SUMO.

Define:

La intersección J5 (el semáforo).

Los edges (E3, E4, E5, E6.0, etc.).

El tlLogic del semáforo (fases, estados rojo/amarillo/verde).

Piensa en este archivo como “el mapa + semáforo” de tu ciudad miniatura.

2. IA_gym.rou.xml

Es el archivo de rutas y flujos de tráfico.

Contiene:

route → caminos que pueden seguir los vehículos (por qué calles pasan).

flow → cuánto tráfico llega desde cada dirección (periodo = cada cuántos segundos entra un coche).

Aquí decides de dónde viene mucho tráfico y de dónde viene poco (formas las colas).

3. IA_gym.sumocfg

Es el archivo de configuración de SUMO.

Le dice a SUMO:

Qué red cargar: Mi_red.net.xml.

Qué rutas/tráfico usar: IA_gym.rou.xml.

Es el archivo que se pasa a SUMO con la opción -c.

Es básicamente el “escenario” que se lanza en cada episodio.

4. env_sumo_dqn_j5.py

Define la clase SumoEnvDQN_J5, que es el entorno de RL.

Se encarga de:

Arrancar SUMO vía TraCI con IA_gym.sumocfg.

Leer el estado del cruce:

número de coches por dirección (N, E, S, O),

fase actual del semáforo.

Aplicar la acción de la IA:

0 → mantener fase.

1 → pasar a la siguiente fase.

Avanzar la simulación unos segundos (delta_time).

Calcular la recompensa (negativo del tiempo de espera total).

Indicar cuándo termina el episodio (cuando ya no quedan vehículos).

Es el puente entre SUMO y el agente DQN.

5. dqn_agent.py

Implementa el agente DQN usando PyTorch.

Contiene:

La red neuronal (DQN) que aproxima la Q-función.

El buffer de memoria (replay buffer).

La lógica de:

política ε-greedy (select_action),

guardar transiciones (store),

actualizar la red (train_step),

copiar pesos a la red target (update_target).

Es el “cerebro” que aprende a escoger fases del semáforo.

6. train_dqn_sumo.py

Es el script principal de entrenamiento.

Hace:

Crea el entorno SumoEnvDQN_J5.

Crea el agente DQNAgent.

Corre varios episodios:

state = env.reset()

action = agent.select_action(state)

next_state, reward, done, _ = env.step(action)

agent.store(...) y agent.train_step()

Cada episodio imprime la recompensa total y el valor de ε.

Es el archivo que ejecutas para entrenar:

python train_dqn_sumo.py

Cómo ejecutar

Asegúrate de que todos los archivos estén en la misma carpeta del proyecto.

Edita train_dqn_sumo.py para que sumo_cfg apunte a tu ruta completa de IA_gym.sumocfg.

Desde esa carpeta (o con la ruta absoluta ya puesta), ejecuta:

python train_dqn_sumo.py


Si quieres ver la simulación gráficamente, en env_sumo_dqn_j5.py usa:

env = SumoEnvDQN_J5(sumo_cfg_path=sumo_cfg, use_gui=True, delta_time=5)
