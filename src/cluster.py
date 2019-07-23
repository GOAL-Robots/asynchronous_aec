import numpy as np
import time
from asynchronous import make_experiment_path
import os



possible_values = \
    ["n_parameter_servers",
     "n_workers",
     "description",
     "tensorboard",
     "flush_every",
     "n_trajectories",
     "sequence_length",
     "update_per_episode",
     "restore_from",
     "model_learning_rate",
     "critic_learning_rate",
     "actor_learning_rate",
     "entropy_reg",
     "entropy_reg_decay"]


class ClusterQueue:
    def __init__(self, **kwargs):
        experiment_path = make_experiment_path(
            date=time.strftime("%Y_%m_%d-%H:%M:%S", time.localtime()),
            mlr=kwargs["model_learning_rate"] if "model_learning_rate" in kwargs else None,
            clr=kwargs["critic_learning_rate"] if "critic_learning_rate" in kwargs else None,
            alr=kwargs["actor_learning_rate"] if "actor_learning_rate" in kwargs else None,
            er=kwargs["entropy_reg"] if "entropy_reg" in kwargs else None,
            description=kwargs["description"])
        os.mkdir(experiment_path)
        os.mkdir(experiment_path + "/log")
        self.cmd = "sbatch --output {}/log/%N_%j.log".format(experiment_path)
        if "description" in kwargs:
            self.cmd += " --job-name {}".format(kwargs["description"])
        self.cmd += " cluster.sh"
        for k, v in kwargs.items():
            flag = self._key_to_flag(k)
            arg = self._to_arg(flag, v)
            self.cmd += arg
        self.cmd += self._to_arg("--experiment-path", experiment_path)
        os.system(self.cmd)
        time.sleep(60)

    def _key_to_flag(self, key):
        return "--" + key.replace("_", "-")

    def _to_arg(self, flag, v):
        return " {} {}".format(flag, v)


# ClusterQueue(n_trajectories=500000, description="replicate_after_code_update")
# ClusterQueue(n_trajectories=500000, description="shorter_episodes_10", sequence_length=10)
# ClusterQueue(n_trajectories=500000, description="shorter_episodes_20", sequence_length=20)
# ClusterQueue(n_trajectories=500000, description="updates_per_episode_01", update_per_episode=1)
# ClusterQueue(n_trajectories=500000, description="updates_per_episode_02", update_per_episode=2)
# ClusterQueue(n_trajectories=500000, description="updates_per_episode_05", update_per_episode=5)
# ClusterQueue(n_trajectories=500000, description="updates_per_episode_10", update_per_episode=10)
# ClusterQueue(n_trajectories=500000, description="updates_per_episode_20", update_per_episode=20)
# ClusterQueue(n_trajectories=500000, description="updates_per_episode_40", update_per_episode=40)
# ClusterQueue(n_trajectories=500000, description="tune_entropy_reg_0.1", entropy_reg=0.1)
# ClusterQueue(n_trajectories=500000, description="tune_entropy_reg_0.2", entropy_reg=0.2)
# ClusterQueue(n_trajectories=500000, description="tune_entropy_reg_0.3", entropy_reg=0.3)
# ClusterQueue(n_trajectories=500000, description="tune_entropy_reg_0.4", entropy_reg=0.4)
# ClusterQueue(n_trajectories=500000, description="tune_entropy_reg_0.5", entropy_reg=0.5)
# ClusterQueue(n_trajectories=500000, description="tune_actor_learning_rate_-6", actor_learning_rate=1e-6)
# ClusterQueue(n_trajectories=1000000, description="tune_temperature_0.1", actor_learning_rate=1e-5, softmax_temperature=0.1, update_per_episode=20, sequence_length=20)
# ClusterQueue(n_trajectories=1000000, description="tune_temperature_1.0", actor_learning_rate=1e-5, softmax_temperature=1.0, update_per_episode=20, sequence_length=20)
# ClusterQueue(n_trajectories=1000000, description="tune_temperature_5.0", actor_learning_rate=1e-5, softmax_temperature=5.0, update_per_episode=20, sequence_length=20)
# ClusterQueue(n_trajectories=1000000, description="tune_temperature_10.0", actor_learning_rate=1e-5, softmax_temperature=10.0, update_per_episode=20, sequence_length=20)
# ClusterQueue(n_trajectories=1000000, description="tune_temperature_20.0", actor_learning_rate=1e-5, softmax_temperature=20.0, update_per_episode=20, sequence_length=20)
# ClusterQueue(n_trajectories=1000000, description="tune_temperature_50.0", actor_learning_rate=1e-5, softmax_temperature=50.0, update_per_episode=20, sequence_length=20)
# ClusterQueue(n_trajectories=1000000, description="tune_temperature_100.0", actor_learning_rate=1e-5, softmax_temperature=100.0, update_per_episode=20, sequence_length=20)
# ClusterQueue(n_trajectories=500000, description="tune_actor_learning_rate_-4", actor_learning_rate=1e-4)


# entropy_reg_decay = np.exp(np.log(0.05 / 0.3) / (15000 * 20))
# ClusterQueue(n_trajectories=500000, description="decay_entropy_0.05", entropy_reg=0.3, update_per_episode=20, entropy_reg_decay=entropy_reg_decay)
# entropy_reg_decay = np.exp(np.log(0.1 / 0.3) / (15000 * 20))
# ClusterQueue(n_trajectories=500000, description="decay_entropy_0.1", entropy_reg=0.3, update_per_episode=20, entropy_reg_decay=entropy_reg_decay)
# entropy_reg_decay = np.exp(np.log(0.01 / 0.3) / (15000 * 20))
# ClusterQueue(n_trajectories=500000, description="decay_entropy_0.01", entropy_reg=0.3, update_per_episode=20, entropy_reg_decay=entropy_reg_decay)


# entropy_reg_decay = np.exp(np.log(0.2 / 0.3) / (12500 * 20))
# ClusterQueue(n_trajectories=2000000, description="decay_entropy_0.2", entropy_reg=0.3, update_per_episode=20, entropy_reg_decay=entropy_reg_decay, actor_learning_rate=1e-5, sequence_length=20)


# ClusterQueue(n_trajectories=1000000, description="gradient_descent_temperature_10.0_alr_1e-1", actor_learning_rate=1e-1, softmax_temperature=10.0, update_per_episode=20, sequence_length=20)
# ClusterQueue(n_trajectories=1000000, description="gradient_descent_temperature_10.0_alr_1e-2", actor_learning_rate=1e-2, softmax_temperature=10.0, update_per_episode=20, sequence_length=20)
# ClusterQueue(n_trajectories=1000000, description="gradient_descent_temperature_10.0_alr_1e-3", actor_learning_rate=1e-3, softmax_temperature=10.0, update_per_episode=20, sequence_length=20)
# ClusterQueue(n_trajectories=1000000, description="gradient_descent_temperature_10.0_alr_1e-4", actor_learning_rate=1e-4, softmax_temperature=10.0, update_per_episode=20, sequence_length=20)
# ClusterQueue(n_trajectories=1000000, description="gradient_descent_temperature_10.0_alr_1e-5", actor_learning_rate=1e-5, softmax_temperature=10.0, update_per_episode=20, sequence_length=20)

softmax_temperature_decay = np.exp(np.log(2 / 50) / (50000 * 20))
ClusterQueue(n_trajectories=1000000, description="decay_temperature_end_2.0", actor_learning_rate=1e-5, softmax_temperature=50.0, softmax_temperature_decay=softmax_temperature_decay, update_per_episode=20, sequence_length=20)
softmax_temperature_decay = np.exp(np.log(5 / 50) / (50000 * 20))
ClusterQueue(n_trajectories=1000000, description="decay_temperature_end_5.0", actor_learning_rate=1e-5, softmax_temperature=50.0, softmax_temperature_decay=softmax_temperature_decay, update_per_episode=20, sequence_length=20)
