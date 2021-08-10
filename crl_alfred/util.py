import os
from glob import glob
import json


def get_set_of_discrete_actions():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../alfred/data/json_2.1.0'))

    discrete_action_set = set()

    files = glob(os.path.join(data_dir, 'train') + '/*/*/traj_data.json')
    for json_file in files:
        with open(json_file, 'r') as f:
            traj_data = json.load(f)

        # for a in traj_data['plan']['low_actions']:
            # discrete_actions_set.add(a['discrete_action']['action'])

        for a in traj_data['plan']['high_pddl']:
            discrete_action_set.add(a['planner_action']['action'])

        # print(traj_data.keys())
        # print(traj_data['plan']['low_actions'])
        # print(traj_data['task_id'])
        # print(traj_data['task_type'])
        # exit()

    print(list(sorted(discrete_action_set)))
    # ['CloseObject', 'LookDown_15', 'LookUp_15', 'MoveAhead_25', 'OpenObject', 'PickupObject', 'PutObject', 'RotateLeft_90', 'RotateRight_90', 'SliceObject', 'ToggleObjectOff', 'ToggleObjectOn']


if __name__ == '__main__':
    get_set_of_discrete_actions()
