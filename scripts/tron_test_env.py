from environment import TronParallelEnv  # Asegúrate que la ruta y nombre coincidan
import numpy as np
import time

# Crear entorno
env = TronParallelEnv()

# Resetear entorno
observations = env.reset()

# Número de pasos de prueba
n_steps = 100

total_rewards = {agent: 0.0 for agent in env.agents}

for step in range(n_steps):
    actions = {
        agent: env.action_space[agent].sample()
        for agent in env.agents
    }

    print(f"\n🔁 Step {step + 1}")
    observations, rewards, terminations, truncations, infos = env.step(actions)

    for agent in env.agents:
        r = rewards.get(agent, 0.0)
        total_rewards[agent] += r
        print(f"{agent} | Reward this step: {r} | Total accumulated: {total_rewards[agent]:.1f} | Done: {terminations[agent] or truncations[agent]}")


    # Mostrar un poco más lento si estás renderizando
    time.sleep(0.1)

    if all(terminations[agent] or truncations[agent] for agent in env.agents):
        print("\n✅ Juego terminado.")
        break

# Cerrar entorno
env.close()
