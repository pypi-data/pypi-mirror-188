from gymnasium.envs.registration import register

register(
    id='Moral_Hazard-v1',
    entry_point='cpagym.envs.moral_hazard_env:Moral_HazardEnv',
)