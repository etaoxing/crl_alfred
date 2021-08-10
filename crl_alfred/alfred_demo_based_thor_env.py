import gym
from gym.utils import seeding
import copy
import os
import json
import numpy as np
from PIL import Image

from alfred.env.thor_env import ThorEnv
from alfred.utils import eval_util
from alfred.gen.game_states.game_state_base import GameStateBase

ALFRED_DEMO_DIR = os.environ['ALFRED_DATA_DIR']

# from alfred.gen.scripts.replay_checks
JSON_FILENAME = "traj_data.json"

# # these are not exactly the actions in traj_data.json
# ACTION_SPACE = copy.deepcopy(GameStateBase.static_action_space)
# ACTION_SPACE = list(filter(lambda x: x['action'] not in ['Terminate'], ACTION_SPACE))

# generated from crl_alfred.util.get_set_of_discrete_actions
DISCRETE_ACTION_SPACE = [
    'CloseObject',
    'LookDown_15',
    'LookUp_15',
    'MoveAhead_25',
    'OpenObject',
    'PickupObject',
    'PutObject',
    'RotateLeft_90',
    'RotateRight_90',
    'SliceObject',
    'ToggleObjectOff',
    'ToggleObjectOn',
]


class AlfredDemoBasedThorEnv(gym.Env):
    """
    References:
    https://ai2thor.allenai.org/ithor/documentation/environment-state/#agent-simulator-loop
    """
    def __init__(self, which_dataset, demo_name, x_display='0', max_fails=10):
        assert which_dataset in set(['train', 'val_seen', 'val_unseen', 'test_seen', 'test_unseen'])

        self.which_dataset = which_dataset
        self.demo_name = demo_name

        self.max_fails = max_fails  # see alfred.config.cfg_eval

        self.demo_dir = os.path.join(
            ALFRED_DEMO_DIR,
            self.which_dataset,
            self.demo_name,
        )

        json_file = os.path.join(self.demo_dir, JSON_FILENAME)
        with open(json_file, 'r') as f:
            self.traj_data = json.load(f)

        self.env = ThorEnv(x_display=x_display)

        self.seed()

    @property
    def observation_space(self):
        d = dict(
            frame=gym.spaces.Box(
                low=0, high=255,
                shape=(self.height, self.width, 3),
                dtype=np.uint8,
            )
        )
        d['goal_frame'] = copy.deepcopy(self.goal_frame)
        return gym.spaces.Dict(d)

    @property
    def action_space(self):
        return gym.spaces.Discrete(len(DISCRETE_ACTION_SPACE))

    def get_obs_dict(self):
        obs = dict(
            frame=self.env.last_event.frame,
            goal_frame=copy.deepcopy(self.goal_frame),
        )
        return obs

    def step(self, a):
        action = DISCRETE_ACTION_SPACE[a]

        # # from alfred.utils.eval_util.agent_step, obstruction_detection()
        # remove blocking actions
        # if action != 'MoveAhead_25':
        #     pass
        # if self.env.last_event.metadata['lastActionSuccess']:
        #     pass
        # dist_action = m_out['action'][0][0].detach().cpu()
        # idx_rotateR = vocab_out.word2index('RotateRight_90')
        # idx_rotateL = vocab_out.word2index('RotateLeft_90')
        # action = 'RotateLeft_90' if dist_action[idx_rotateL] > dist_action[idx_rotateR] else 'RotateRight_90'

        # # smooth_nav=True is only used in alfred.gen.render_trajs
        # _ = self.env.step(action, smooth_nav=False)
        # instead of calling env.step, we use thor_env.to_thor_api_exec as in va_interact
        try:
            if self.num_fails >= self.max_fails:
                raise Exception

            _, _ = self.env.to_thor_api_exec(
                action,
                object_id=self.api_action.get('objectId', ''),
                smooth_nav=False,
            )

            reward, done = self.env.get_transition_reward()

        except Exception as err:
            reward = 0.0
            done = False

            # as per alfred.utils.eval_util.agent_step
            self.num_fails += 1
            if self.num_fails >= self.max_fails:
                done = True
                reward = 0.0

        # info = self.env.last_event.metadata
        info = {}

        # this returns task.finished, not task.goal_idx
        # these goal indices are based on the high PDDL actions, not the low discrete actions
        # that the simulator takes
        curr_subgoal_idx = self.env.get_subgoal_idx()
        if self.prev_subgoal_idx != curr_subgoal_idx:
            self.prev_subgoal_idx = curr_subgoal_idx
            self.update_subgoal()

        # call this last since may need to update goal frame
        obs = self.get_obs_dict()

        return obs, reward, done, info

    def update_subgoal(self):
        # grab the last frame generated by the demo
        # that is associated with the current task.goal_idx
        # (since there may be intermediate frames rendered)
        c = self.env.task.goal_idx
        for i in range(len(self.traj_data['images']) - 1, -1, -1):  # start from the end
            if self.traj_data['images'][i]['high_idx'] == c:
                break

        image_path = os.path.join(
            self.demo_dir,
            'raw_images',
            self.traj_data['images'][i]['image_name'].replace('.png', '.jpg')
        )
        self.goal_frame = Image.open(image_path)

        self.low_idx = self.traj_data['images'][i]['low_idx']

        # grab the ground truth api action needed to complete the subgoal task.
        # we do this in place of generating interaction masks.
        # any type of actions like this should be a distinct PDDL high action, so high_idx
        # should have been incremented accordingly.
        self.api_action = self.traj_data['plan']['low_actions'][self.low_idx]['api_action']

    def reset(self):
        eval_util.setup_scene(
            self.env,
            self.traj_data,
            # sets reward and task
            reward_type='dense',
            test_split=False,
        )

        self.num_fails = 0

        self.prev_subgoal_idx = -1  # initialize as task.finished
        self.update_subgoal()
        return self.get_obs_dict()

    def render(self, mode='human'):
        raise NotImplementedError

    def close(self):
        self.env.stop()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]


if __name__ == '__main__':
    env = AlfredDemoBasedThorEnv('train', 'pick_clean_then_place_in_recep-LettuceSliced-None-Fridge-19/trial_T20190909_010053_518756')
    env.reset()
    env.step(0)
