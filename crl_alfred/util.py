import os
from glob import glob
import json
import collections

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../alfred/data/json_2.1.0'))


def get_set_of_discrete_actions():

    discrete_action_set = set()

    files = glob(os.path.join(DATA_DIR, 'train') + '/*/*/traj_data.json')
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


def create_task_sequence_of_set(which_set):
    tasks = set()
    demos = collections.defaultdict(list)

    files = glob(os.path.join(DATA_DIR, 'train') + '/*/*/traj_data.json')
    for f in files:
        demo_name = '/'.join(f.split('/')[-3:-1])
        task = demo_name.split('-')[0]
        tasks.add(task)
        demos[task].append(demo_name)

    for k in sorted(tasks):
        v = sorted(demos[k])
        demos[k] = v

    return demos


def create_task_sequences():
    d = {}
    for s in ['train', 'valid_seen', 'valid_unseen', 'test_seen', 'test_unseen']:
        demos = create_task_sequence_of_set(s)
        d[s] = demos

    with open('task_sequences.json', 'w') as f:
        json.dump(d, f, indent=2)


if __name__ == '__main__':
    # get_set_of_discrete_actions()
    create_task_sequences()
