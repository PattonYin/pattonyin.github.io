# Robot model attribution

| Assets | Source | Licence |
|--------|--------|---------|
| `panda/` arm | [MuJoCo Menagerie: franka_emika_panda](https://github.com/google-deepmind/mujoco_menagerie/tree/main/franka_emika_panda) | Apache 2.0 (`panda/LICENSE`) |
| `iiwa/` arm | [MuJoCo Menagerie: kuka_iiwa_14](https://github.com/google-deepmind/mujoco_menagerie/tree/main/kuka_iiwa_14) | BSD 3-Clause, via Drake (`iiwa/LICENSE`) |
| `robotiq-2f85/` | [MuJoCo Menagerie: robotiq_2f85](https://github.com/google-deepmind/mujoco_menagerie/tree/71f066ad0be9cd271f7ed58c030243ef157af9f4/robotiq_2f85) | BSD 2-Clause, ROS-Industrial (`robotiq-2f85/LICENSE`) |
| `kiwi-kuka/` | Owner-provided `ocean/hardware/kiwi_robot_share`, derived from [KIWI](https://lingfeng.moe/KIWI/) | No upstream geometry licence bundled; see `kiwi-kuka/PROVENANCE.md` |

## Conversion and mounting

Visual meshes are simplified and exported as compact GLBs; collision meshes,
raw CAD and source downloads are excluded from the website. Arm meshes use up
to 12,000 faces per source part; gripper simplification targets 6,000, or 12,000
for KIWI's detailed servo. KIWI parts retain
the supplied URDF colours. Shared geometry serves both KUKA arms,
with the original orange-and-gray finish on the left and white body panels on the right.

The Panda stock hand is replaced by a Robotiq 2F-85 at its 107 mm flange offset.
Its joint frames, offset follower pivots and closed linkage follow the source
MJCF. Sampled closure poses hold each coupler at its zero-angle stop and solve
the spring/follower angles, without a physics engine in the browser.

Both KUKA arms carry the KIWI robot-mounted assembly at the 45 mm flange offset.
The supplied `urdf/kiwi_gripper.urdf` defines mesh scale, adapter, camera position,
and two opposing revolute jaw axes. Each jaw keeps its own hinge frame and mesh;
the right jaw follows the left with equal angles on the opposite axis. The closed
contact TCP remains 220.756 mm beyond the mount face, with its supplied Y offset.

Arm angles retain the MJCF joint convention. For both KIWI and Robotiq, the
0-to-0.04 display command maps closed to open through coupled joint poses;
it is not a physical jaw distance or hardware command. KIWI's opening limit is
the supplied 0.770911 radians per jaw (approximately 44.17 degrees).

The KUKA visual model remains the iiwa 14 R820, as indicated in the caption.

## Regenerating

```powershell
pip install trimesh fast-simplification numpy scipy
python tools/convert_robots.py assets/robots
python tools/convert_grippers.py "X:/code/ocean/hardware/kiwi_robot_share"
python tools/generate_robot_motion.py
```

The local source folder must contain `urdf/kiwi_gripper.urdf` and its referenced
`meshes/` directory. Downloaded source files are cached under the ignored `.preview/`
directory. The gripper converter replaces any prior tool links; the obsolete
Panda `hand.glb`, `left_finger.glb` and `right_finger.glb` are not used.

Display motion uses full tool position and orientation IK with joint limits,
keeping the tools downward and the KIWI grippers facing opposite directions.
The generator checks orientation and position errors between playback samples
and closes each loop onto its starting joint posture.
