# train_ppo_teams.py
from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env
from environment import TronParallelEnv

from ray.rllib.env.wrappers.pettingzoo_env import ParallelPettingZooEnv


import ray

def env_creator(_):
    return ParallelPettingZooEnv(TronParallelEnv())

register_env("tron_env", env_creator)

#Extrae espacios para definir las políticas
raw_env = TronParallelEnv()
first_agent = raw_env.possible_agents[0]
obs_space = raw_env.observation_space[first_agent]
act_space = raw_env.action_space[first_agent]

#Definir las políticas por equipo
def policy_mapping_fn(agent_id, episode=None, worker=None, **kwargs):
    if agent_id in ["player_1", "player_3"]:
        return "red_team_policy"
    else:
        return "blue_team_policy"

#Configurar PPO imitando el MAPPO xD
config = (
    PPOConfig()
    .environment("tron_env")
    .framework("torch")
    .rollouts(num_rollout_workers=1)
    .training(train_batch_size=2400)
    .multi_agent(
        policies={
            "red_team_policy": (None, obs_space, act_space, {}),
            "blue_team_policy": (None, obs_space, act_space, {})
        },
        policy_mapping_fn=policy_mapping_fn,
        policies_to_train=["red_team_policy", "blue_team_policy"]
    )
)

#Iniciar Ray y entrenar
ray.init(ignore_reinit_error=True)

algorithm = config.build()

for i in range(1000):
    results = algorithm.train()
    print(f"Iter {i}: reward_red_team = {results['policy_reward_mean'].get('red_team_policy')}, "
          f"reward_blue_team = {results['policy_reward_mean'].get('blue_team_policy')}")

# Guardar modelo
algorithm.save("tron_ppo_2team")
