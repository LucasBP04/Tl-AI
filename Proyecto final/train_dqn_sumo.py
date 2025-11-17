# train_dqn_sumo.py
from env_sumo_dqn_j5 import SumoEnvDQN_J5
from dqn_agent import DQNAgent
import os

def main():
    # Usa el nombre de tu archivo .sumocfg
    sumo_cfg = r"C:\Users\alber\OneDrive\Escritorio\universidad\Semestre 6\IA\Proyecto final\IA_gym.sumocfg"

    # use_gui=True si quieres ver la simulación, False para entrenar rápido
    env = SumoEnvDQN_J5(sumo_cfg_path=sumo_cfg, use_gui=True, delta_time=5)

    state_dim = 5    # [veh_norte, veh_este, veh_sur, veh_oeste, fase]
    action_dim = 2   # mantener, cambiar fase

    agent = DQNAgent(state_dim, action_dim)

    n_episodes = 200
    target_update_freq = 10

    for ep in range(n_episodes):
        state = env.reset()
        done = False
        total_reward = 0.0

        while not done:
            action = agent.select_action(state)
            next_state, reward, done, _ = env.step(action)

            agent.store(state, action, reward, next_state, done)
            agent.train_step()

            state = next_state
            total_reward += reward

        if (ep + 1) % target_update_freq == 0:
            agent.update_target()

        print(f"Episodio {ep+1}/{n_episodes} | Recompensa total: {total_reward:.2f} | epsilon: {agent.epsilon:.3f}")

if __name__ == "__main__":
    main()