# `crl_alfred`: An environment for continual learning using [ALFRED](https://github.com/askforalfred/alfred) and [AI2-THOR](https://github.com/allenai/ai2thor)

> Later versions of `ai2thor` introduce changes which may not be backwards compatible. The `ALFRED` code and its demonstration data are based on `ai2thor==2.1.0`. We regenerate the demo trajectories with the latest version (`ai2thor>=3.3.5`) and filter out any demos that cannot be reconstructed in the new version.

## Getting started
```
git clone $REPO
cd crl_alfred
export ALFRED_ROOT=$PWD
```

## Install and verify `ai2thor`

## Download ALFRED data

## Precomputing layouts
```
sudo apt-get install ffmpeg flex bison gcc-7
cd $ALFRED_ROOT/alfred/gen/ff_planner
make
cd $ALFRED_ROOT/alfred/layouts
python precompute_layout_locations.py 8
```

## Generating (valid) trajectories
```
cd $ALFRED_ROOT/alfred/gen
python scripts/generate_trajectories.py --save_path $ALFRED_ROOT/alfred/data/new_trajs/ --in_parallel --debug --num_threads 8 --only_traj_data --ignore_test_sets
```

## Playback demo in `crl_alfred` env

## Baselines
This code was developed for use in our [`continual_rl`](https://github.com/AGI-Labs/continual_rl) benchmark, if you are interested in open-source implementations of methods with baseline results using this environment.

## References 
```
 *Our paper, coming soon*
```

```
@inproceedings{ALFRED20,
  title ={{ALFRED: A Benchmark for Interpreting Grounded
           Instructions for Everyday Tasks}},
  author={Mohit Shridhar and Jesse Thomason and Daniel Gordon and Yonatan Bisk and
          Winson Han and Roozbeh Mottaghi and Luke Zettlemoyer and Dieter Fox},
  booktitle = {The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  year = {2020},
  url  = {https://arxiv.org/abs/1912.01734}
}
```

```
@article{ai2thor,
  author={Eric Kolve and Roozbeh Mottaghi and Winson Han and
          Eli VanderBilt and Luca Weihs and Alvaro Herrasti and
          Daniel Gordon and Yuke Zhu and Abhinav Gupta and
          Ali Farhadi},
  title={{AI2-THOR: An Interactive 3D Environment for Visual AI}},
  journal={arXiv},
  year={2017}
}
```
