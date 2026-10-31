---
title: "SONIC-K1: Porting a Universal Humanoid Motion Tracker to a Small Humanoid on a Single GPU"
date: "2026-10-29"
authors: "Kyrylo Kolesnichenko; Jong-Hoon Kim"
url: https://arxiv.org/abs/2610.39327
pdf: https://arxiv.org/pdf/2610.39327
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2610.39327)** / [論文ページ](https://arxiv.org/abs/2610.39327)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **SONIC-K1: Porting a Universal Humanoid Motion Tracker to a Small Humanoid on a Single GPU** 

Kyrylo Kolesnichenko<sup>1</sup><sup>_,_2</sup> and Jong-Hoon Kim<sup>2</sup> 


Fig. 1. A human reference motion (left) and SONIC-K1 tracking it on the Booster K1 in simulation (right). 

**_Abstract_ — We present SONIC-K1, to our knowledge the first open-weights whole-body motion tracker for the Booster K1 humanoid, obtained by adapting the SONIC framework to this smaller robot. The policy is trained from scratch on a single shared GPU with a small fraction of the compute reported for SONIC. In MuJoCo simulation, it tracks nearly all held-out motion clips and performs well on external benchmarks under SONIC’s success criterion. On the real K1, it tracks upperbody and slow motions, while stepping and turning remain less reliable, and simulation experiments show a sensitivity to action latency. These results show broad motion-tracking capability on a modest training budget and point to quantitative hardware evaluation as the main next step. Code, policy weights and evaluation tools are publicly available.** 

## I. INTRODUCTION 

A general motion tracker is a single policy that takes a reference trajectory and outputs joint commands. Once a robot has one, motion capture, pose estimation from video and teleoperation can all drive the same controller. SONIC [1] pushed this approach to 700 h of motion data and 128 GPUs. The code is open, but it is built for the Unitree G1, and most labs cannot afford to train it at that scale. 

Our lab works with the Booster K1 [2], a 22-DoF humanoid that is noticeably smaller than the G1, and we wanted a SONIC-style tracker for it on the hardware we have. We kept SONIC’s architecture, PPO settings and rewards, retargeted 9,991 Bones-SEED clips [3] to the K1 with 

> 1Kaunas Faculty, Vilnius University, Lithuania 

> 2Advanced Telerobotics Research Lab - Computer Science Department, Kent State University, Kent, OH 44242, USA jkim72@kent.edu 

UMR [4], and trained from scratch for 50,000 iterations on a single H100 that was shared with other users. The resulting model, SONIC-K1, is to our knowledge the first general motion tracker for the K1 with public weights. It tracks 97.4% of 1,985 held-out clips in MuJoCo [5] under SONIC’s success rule. We have also run it on the real robot. It works for many motions, though not all of them, and we go through where it fails. 

This report makes three contributions: 

- 1) SONIC-K1, the first open-weights general motion tracker for the Booster K1. It is trained with roughly 1–1.5% of SONIC’s compute, and we list every change we made to the original recipe. 

- 2) An evaluation in two simulators on a 1,985-clip holdout and on PHUMA, LAFAN1 and 100STYLE, plus a robustness sweep. 

- 3) A first test on the real K1, an honest list of weaknesses, and the released code (Apache-2.0), weights (CC BYNC 4.0) and evaluation tools. 

## II. RELATED WORK 

SONIC [1] trains a single tracker for the Unitree G1 on 700 h of motion data. It uses per-modality encoders, a quantized motion token and a shared decoder. We start from its public code and keep its architecture and training recipe. To give a sense of scale for our results, we also list numbers that the SONIC paper reports for BeyondMimic [6] and Any2Track [7], two other trackers for the G1. 

Our training data is the Bones-SEED motion-capture dataset [3], which we map to the K1 with UMR [4], a learned retargeting method for humanoid robots. Besides our own held-out Bones-SEED clips, we test on PHUMA [8], the external benchmark used in the SONIC paper, and on two standard human-motion datasets, LAFAN1 [9] and 100STYLE [10]. 

Training runs in Isaac Lab [11] with PPO [12]. We evaluate in MuJoCo [5], a different physics engine, to check that the policy does not depend on the training simulator. 

III. METHOD: PORTING SONIC TO THE K1 

## _A. Robot and data_ 

The K1 has 22 actuated joints: 2 in the head, 4 in each arm and 6 in each leg. It has no waist and no wrists. We use Booster’s official K1 ~~2~~ 2dof model for both retargeting and training. Bones-SEED contains 142,220 clips, all of which we retargeted to the K1 with UMR. An automatic check then removes clips with joint-limit violations, feet going through the floor, velocity spikes or NaNs, and tags each clip as 


Fig. 2. SONIC-K1 pipeline. Motion data is not redistributed; only the policy and code are released. 

TABLE I 

SONIC VS. SONIC-K1. 

||SONIC|SONIC-K1 (ours)|
|---|---|---|
|Robot<br>|Unitree G1, 29 DoF<br>|Booster K1, 22 DoF<br>|
|Training data|700 h in-house mocap|9,991 Bones-SEED clips|
|Compute|128 GPUs _× ∼_3 days<br>|1 shared H100, 135.4 h|
|Parallel envs<br>|_∼_524K|16,384<br>|
|Iterations|_∼_100K|50,000|
|Init. action std|0.05|0.5|
|Rewards|SONIC Table 3|+ head joint tracking|


feasible or not for the K1 (for example, motions that need a waist are not). We keep only clips that pass the check and are tagged feasible, which leaves 62,427. We trained on 9,991 of them and kept 1,985 aside as a test set, chosen before training started and with no overlap (Fig. 2). 

## _B. Policy and training_ 

The architecture is unchanged from SONIC. Encoders turn a reference motion into a 64-D quantized (FSQ) token, and an MLP decoder combines the token with proprioception to produce joint targets. A PD controller tracks those targets; the policy runs at 50 Hz and physics at 200 Hz. The actor has 25.1M parameters. We trained the robot-motion and teleoperation encoders. The SMPL encoder is in the network but never saw any data. 

PPO hyper-parameters, adaptive motion sampling and rewards are the same as in SONIC, and Table I lists what we changed. The biggest difference is scale. We ran 16,384 environments for 50,000 iterations on one H100 NVL, which took 135.4 h of wall-clock time because other jobs were sharing the GPU (about 103 h if it had been ours alone). That is roughly 1–1.5% of SONIC’s 128 GPUs _× ∼_ 3 days. We also raised the initial action standard deviation from 0.05 to 0.5, because with 0.05 the KL-adaptive scheme throttled the learning rate on the K1. Finally, we added a reward for tracking the head joints, since the K1 head is actuated, and scaled pushes and center-of-mass randomization by 0.7 for the smaller body. We did not model actuation delay. 

## _C. Evaluation protocol_ 

We use SONIC’s success rule: a rollout fails if the root or any end-effector ends up more than 0.25 m away in height from the reference. We also report two other rules. _Nofall_ only checks that the robot stays up (root height within 0.25 m, orientation within 1 rad). _Official_ , the stricter rule in the SONIC repository, also limits world-frame foot position to 0.2 m. Tracking error is MPJPE-L over 12 K1 links, in mm, averaged over successful clips. For the MuJoCo runs we use the robot-motion encoder and deterministic actions. 

## IV. EXPERIMENTS 

Unless stated otherwise, all results are for the released SONIC-K1 policy, use 10 s windows, and apply SONIC’s 0.25 m success rule. 

## _A. Benchmarks_ 

Table II shows the MuJoCo results. On the 1,985 heldout Bones-SEED clips the policy succeeds 97.4% of the time, with an MPJPE-L of 15.4 mm. PHUMA provides G1 trajectories, so we sampled 2,000 motions across its 15 sources and mapped them from the G1 to the K1 with our own inverse kinematics. Of these, 1,758 passed our checks, and the policy succeeds on 93.6%. On 100STYLE we used the forward walk and run of all 100 styles, and the policy succeeds on 99.0%. LAFAN1 was the hardest set, at 70.6% of 10 s windows; we come back to it in the limitations. 

The right side of Table II lists G1 numbers for SONIC, BeyondMimic and Any2Track, copied from the SONIC paper. We did not rerun these methods. The robot, data, retargeting and test clips are all different, so these columns are only there to give a sense of scale and should not be read as a head-to-head comparison. 

We also checked the same hold-out in Isaac Lab, the simulator we trained in. No-fall success is 98.7% there and 98.4% in MuJoCo, and official-rule success in Isaac Lab is 93.1%, so moving between simulators costs very little. The amount of training data makes a large difference. An earlier run trained on only 10 clips reached 63.6% official success on the same hold-out (33.5 mm MPJPE-L). The released 9,991-clip model reaches 93.1% (14.7 mm). 

## _B. Robustness_ 

Fig. 3 shows a perturbation sweep in MuJoCo with 200 held-out clips per setting, reported under the no-fall and official rules. No-fall success stays at 98.0% or higher with PD gains scaled anywhere from 0.6 to 1.4 _×_ , with 70% motor strength, with a 2 kg payload, with 3 _×_ observation noise and with Booster’s torque caps. Dense pushes up to 3 _×_ the training range still give 97.0%, and very low friction (0.2) costs about 5 points. Latency is the exception. Success is 98.5% at 20 ms of delay but falls to 56.0% at 40 ms. 

## _C. First test on the real K1_ 

We exported the policy to ONNX and ran it at 50 Hz on the robot’s onboard computer, with the robot on a safety belt, using the sample clips from the release kit. Upper-body clips, calm motions and slower whole-body motions such as squats ran smoothly. Clips with steps and turns were less reliable, with visible jitter in the legs. We do not have motion capture for the robot, so we cannot report tracking error on hardware. A proper real-robot evaluation is planned. 

TABLE II 

SONIC-K1 RESULTS IN MUJOCO. SUCCESS IN %, MPJPE-L IN MM. THE G1 COLUMNS ARE NUMBERS REPORTED IN THE SONIC PAPER [1], SHOWN FOR SCALE ONLY. 

|Test set|Clips|SONIC<br>SONIC rule|-K1 succe<br>No-fall|ss<br>Official|MPJPE-L|G1, <br>SONIC|reported (SONIC<br>BeyondMimic|rule)<br>Any2Track|
|---|---|---|---|---|---|---|---|---|
|Bones-SEED held-out|1,985|**97.4**|98.4|91.9|15.4|98.5|82.0|61.6|
|PHUMA|1,758|**93.6**|97.3|85.0|22.4|97.2|73.8|78.5|
|LAFAN1 (10 s windows)|1,390|**70.6**|75.5|45.0|31.9|–|–|–|
|LAFAN1 (full clips)|65|**18.5**|27.7|0.0|28.1|–|–|–|
|100STYLE|200|**99.0**|98.5|77.0|22.5|–|–|–|


Fig. 3. Perturbation sweep for SONIC-K1 in MuJoCo (200 held-out clips per setting). Latency is the only perturbation that causes a large drop. 

## V. WEAKNESSES AND LIMITATIONS 

The biggest problem is the legs on the real robot: stepping and turning motions are clearly less reliable than in simulation. One likely reason is that training had no actuation delay, and the robustness sweep shows that the policy is sensitive to latency between 20 and 40 ms. We have not yet measured this on hardware. 

Some motions are simply out of reach for now. On LAFAN1, falling and getting up succeeds in only 4.2% of windows and the obstacle clips in 36.5%, because both need floor contact or props that are not in our training data or simulation. Its locomotion-style windows, by comparison, reach 91.9%. Long clips are another issue: global drift builds up and one slip ends the episode, so full LAFAN1 clips of 1–4 min succeed only 18.5% of the time. On our own holdout, dancing (83.2%) and advanced locomotion (80.4%) are the weakest categories under the official rule. 

The evaluation has gaps too. Nearly everything is measured in simulation, and the hardware results are qualitative. The hold-out comes from the same dataset as the training clips, and the PHUMA and LAFAN1 numbers depend on our own retargeting. We trained one seed and ran no ablations. The 10-clip run also differs from the released one in iterations and number of environments, not just in data. Finally, the SMPL and video encoders are untrained, so any video or SMPL input has to be retargeted to the K1 first. 

## VI. CONCLUSION AND FUTURE WORK 

SONIC-K1 is the first open-weights general motion tracker for the Booster K1. SONIC was designed for 128 GPUs, but our port, trained on one GPU, still reaches 97.4% success on held-out motion under SONIC’s own rule. SONIC-K1 runs on the real K1, though its legs are not yet reliable on steps and turns. 

Our next step is a proper evaluation on the robot with tracking metrics. After that, we plan to make training match the hardware more closely by adding deployment torque caps, actuation delay and gain randomization, as several trackers that work well on hardware do. Further plans are a larger model trained on the full 62K-clip pool, whole-body teleoperation through the teleoperation encoder we already trained, and driving the robot from video. For video we currently estimate human pose and retarget it, and a trained SMPL encoder would remove the retargeting step. 

**Release.** The code is available under Apache-2.0 at https://github.com/Kyk0/sonic-k1, the weights under CC BY-NC 4.0 at https://huggingface.co/ Kyry10/sonic-k1, and the project page is https:// kyry.me/sonic-k1. The Booster K1 model is BSD-3Clause. Training data includes Motion Data by Bones Studio (https://bones.studio/). We do not redistribute the motion data, either raw or retargeted. 

## ACKNOWLEDGMENTS 

We thank NVIDIA GEAR for open-sourcing SONIC, Bones Studio for Bones-SEED, the UMR authors, and Booster Robotics for the K1 models. 

## REFERENCES 

- [1] Z. Luo, Y. Yuan, T. Wang, C. Li, F. Casta˜neda, S. Chen, Z.-A. Cao, J. Li, D. Minor, Q. Ben, J. Park, D. Sami, Z. Wang, X. Da, R. Ding, C. Hogg, L. Song, E. Lim, E. Jeong, T. He, H. Xue, W. Xiao, S. Yuen, J. Kautz, Y. Chang, U. Iqbal, L. Fan, and Y. Zhu, “SONIC: Supersizing motion tracking for natural humanoid whole-body control,” _arXiv preprint arXiv:2511.07820_ , 2025. 

- [2] Booster Robotics, “Booster K1 humanoid robot,” https://www.booster. tech/. 

- [3] Bones Studio, “Bones-SEED motion dataset,” https://huggingface.co/ datasets/bones-studio/seed, https://bones.studio/. 

- [4] H. Cao, Y. Fang, T. Kwon, R. Yu, J. Ma, J. Tan, Y. Zhou, B. Du, Y. Gu, Y. Gao, R. Dai, L. Han, and R. Xu, “Unified motion retargeting for humanoids with learned point cloud correspondence,” _arXiv preprint arXiv:2609.02134_ , 2026. 

- [5] E. Todorov, T. Erez, and Y. Tassa, “MuJoCo: A physics engine for model-based control,” in _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2012, pp. 5026–5033. 

- [6] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu, “BeyondMimic: From motion tracking to versatile humanoid control via guided diffusion,” _arXiv preprint arXiv:2508.08241_ , 2025. 

- [7] Z. Zhang, J. Guo, C. Chen, J. Wang, C. Lin, Y. Lian, H. Xue, Z. Wang, M. Liu, J. Lyu, H. Liu, H. Wang, and L. Yi, “Track any motions under any disturbances,” _arXiv preprint arXiv:2509.13833_ , 2025. 

- [8] K. Lee, S. Kim, Y. Lee, M. Park, H. Kim, D. Hwang, D. Kim, H. Lee, and J. Choo, “PHUMA: Physically reliable humanoid locomotion dataset,” _arXiv preprint arXiv:2510.26236_ , 2025. 

- [9] F. G. Harvey, M. Yurick, D. Nowrouzezahrai, and C. Pal, “Robust motion in-betweening,” _ACM Transactions on Graphics_ , vol. 39, no. 4, 2020. 

- [10] I. Mason, S. Starke, and T. Komura, “Real-time style modelling of human locomotion via feature-wise transformations and local motion phases,” _Proceedings of the ACM on Computer Graphics and Interactive Techniques_ , vol. 5, no. 1, pp. 1–18, 2022. 

- [11] NVIDIA, M. Mittal, P. Roth, J. Tigue, A. Richard, O. Zhang, P. Du, A. Serrano-Mu˜noz, X. Yao, R. Zurbr¨ugg, N. Rudin _et al._ , “Isaac Lab: A GPU-accelerated simulation framework for multi-modal robot learning,” _arXiv preprint arXiv:2511.04831_ , 2025. 

- [12] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

