---
title: "MuJoCo MPC for Humanoid Control: Evaluation on HumanoidBench"
date: "2024-08-01"
authors: "Moritz Meser; Aditya Bhatt; Boris Belousov; Jan Peters"
url: https://arxiv.org/abs/2408.00342
pdf: https://arxiv.org/pdf/2408.00342
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2408.00342)** / [論文ページ](https://arxiv.org/abs/2408.00342)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**MuJoCo MPC for Humanoid Control: Evaluation on HumanoidBench** 

Moritz Meser<sup>1,2</sup> , Aditya Bhatt<sup>2</sup> , Boris Belousov<sup>2</sup> and Jan Peters<sup>1,2,3,4</sup> 

**_Abstract_ — We tackle the recently introduced benchmark for whole-body humanoid control HumanoidBench [9] using MuJoCo MPC [6]. We find that sparse reward functions of HumanoidBench yield undesirable and unrealistic behaviors when optimized; therefore, we propose a set of regularization terms that stabilize the robot behavior across tasks. Current evaluations on a subset of tasks demonstrate that our proposed reward function allows achieving the highest HumanoidBench scores while maintaining realistic posture and smooth control signals. Our code is publicly available and will become a part of MuJoCo MPC**<sup>5</sup> **, enabling rapid prototyping of robot behaviors.** 

# I. INTRODUCTION AND RELATED WORK 

Designing dynamic behaviors for humanoid robots is a challenging problem [4], [5]. One promising approach is to craft task-specific reward functions and train policies via Reinforcement Learning (RL). To this end, [9] proposed HumanoidBench, a suite of 27 tasks for Unitree H1 robot based on MuJoCo [11], with 12 tasks assessing locomotion abilities and 15 tasks evaluating object manipulation skills. In [9], performances of four popular RL algorithms are reported: DreamerV3 [2], TD-MPC2 [3], SAC [1], PPO [8]. However, none of these methods is able to solve the tasks satisfactorily, producing jittery motions ill-suited for execution on real hardware. Therefore, we evaluate an alternative approach to humanoid behavior synthesis that exploits the power of simulation: Model Predictive Control (MPC). 

MPC does not require training; at each time-step, it selects the optimal action based on a multi-step lookahead search, and repeats this procedure at the next time-step in a receding-horizon manner [7]. MPC is a mature paradigm that admits various planning algorithms for this search, including iLQG [10] and even randomly sampled action sequences [6]. We apply MPC to a subset of the HumanoidBench locomotion and manipulation tasks using MuJoCo MPC (MJPC) [6], which implements the aforementioned planners. 

# II. MJPC WITH SHAPED REWARDS 

MPC repeatedly solves a finite-horizon optimal control problem min _u_ 0: _T_ � _Tt_ =0<sup>_c_(</sup><sup>_xt, ut_)where</sup><sup>_c_(</sup><sup>_xt, ut_)isthein-</sup> stantaneous cost. MJPC further decomposes the cost into a weighted sum _c_ ( _x, u_ ) =<sup>�</sup><sup>_M_</sup> _i_ =0<sup>_wi·ni_(</sup><sup>_ci_(</sup><sup>_x, u_))where</sup> _ci_ ( _x, u_ ) are (signed) residuals, _ni_ are twice-differentiable norm functions, and _wi_ are tunable non-negative weights [6]. 

> 1Intelligent Autonomous Systems Lab, Department of Computer Science, TU Darmstadt, Germany, moritz.meser@stud.tu-darmstadt.de 

> 2German Research Center for AI (DFKI) 

> 3Centre for Cognitive Science, Technical University of Darmstadt 

> 4Hessian Center for Artificial Intelligence (Hessian.AI), Darmstadt 

> We thank Hessisches Ministerium f¨ur Wissenschaft & Kunst for the DFKI grant and “The Adaptive Mind” grant. 

> 5https://github.com/google-deepmind/mujoco_mpc/pull/328 


Fig. 1: Performance comparison between the proposed controller _MPC-ours_ that leverages shaped reward functions and the baselines: _MPC-hb_ , which uses the HumanoidBench reward function, and the RL baselines. The _y_ -axis shows the HumanoidBench score given by the sum of rewards over a trajectory, with maximum 1000 for each task. For MPC methods, we employ the iLQG planner on the Stand and Walk tasks, and the Sampling planner on the Push task which involves a lot of contact interactions. Results from 6 runs of each MPC method are reported. RL baseline results are imported from [6] where 3 runs of each method are reported; we take the best policy from each run. _MPC-ours_ significantly outperforms the baselines across tasks. 

The HumanoidBench tasks are formulated in terms of rewards _r_ hb rather than costs. Therefore, we apply a transformation _c_ hb( _x, u_ ) = _|r_ max _− r_ hb _|_ before passing it to MJPC, where _r_ max is the maximum achievable instantaneous reward (set to _r_ max = 1) and the norm is approximated by kSmoothAbsLoss to ensure differentiability. 

We observed that _r_ hb alone yields physically undesirable behaviors (Fig. 2) and results in low rewards (Fig. 3). Therefore, we introduced a number of shaping terms that i) improve robot stability and ii) provide dense reward signal. 

_Stability-enhancing cost terms_ penalize excessively strong movements and promote postural balance: 1) height of the robot’s head from the ground; 2) height difference between the pelvis and the feet; 3) linear velocity of the center of mass (CoM); 4) ‘balance’ (projection of CoM between the feet); 5) deviation from a ‘canonical’ posture; 6) direction the robot is facing; 7) magnitude of the control signal. 

_Dense reward residuals_ : 1) distance between an object and its target location; 2) distance between the left hand and the object; 3) distance between the right hand and the object. Although some of these residuals are already encoded in the HumanoidBench reward, we find that providing them individually to the optimizer improves performance (Fig. 1). 


Fig. 2: Behavior comparison between _MPC-ours_ (top row) and _MPC-hb_ (bottom row) on the Push task. Unlike our shaped reward, which encourages posture maintenance and balance, the HumanoidBench reward puts all emphasis on reaching the target box location as fast as possible, driving the robot into unrecoverable postures and thereby precluding further tasks. 


Fig. 3: Influence of the episode length on evaluation scores shown on the Walk task over 6 runs. An episode would normally stop at the 2s mark (vertical dotted line), yielding a relatively high cumulative reward for _MPC-hb_ (green curve) thanks to good initial performance. However, when extended further, the median HumanoidBench reward drops almost to zero, while ours maintains the maximum value of 1. 

# III. EXTENDED TASK EVALUATION PROTOCOL 

Along with the pointed out uninformativeness of the reward function in HumanoidBench, we observe one further factor that impacts the generated behaviors and evaluations— namely, the _episode length_ . The evaluation period is very short—2 seconds for the Walk and Stand tasks; and for the Push task, the simulation terminates as soon as the box reaches its target location. Such short episode lengths result in policies that do not maintain balance at the end of the episode, not expecting further tasks (Fig. 2, bottom). We provide a quantitative evaluation of the impact of the episode length in Fig. 3 on the Walk task. A qualitative evaluation is provided in Fig. 2, where new targets are respawn, requiring the robot to perform the task repeatedly. Based on these evaluations, we argue for longer episode lengths and for repeated tasks with changing goals. 

# IV. ANALYSIS OF BEHAVIORS AND PLANNERS 

In this section, we analyze the generated behaviors in a quantitative manner, beyond only reporting the return value. 

|First,<br>we<br>evaluate|TABLE I|: Control sm|oothness cost:|
|---|---|---|---|
|the<br>smoothness<br>of|average s|quared joint|velocity.|
|trajectories<br>(energy<br>cost)asjudedb|**Task**|**MPC-ours**|**MPC-hb**|
|,  g y<br>theaveragesquared|Walk|**1.45** _±_ 0.13|1.67 _±_ 0.87|
|<br>joint<br>velocity<br>(Ta-|Stand|**0.01** _±_ 0.00|1.49 _±_ 0.23|
|ble I). Our reward|Push|1.60 _±_ 0.14|1.66 _±_ 0.05|


generates consistently smoother trajectories on the Stand and Walk tasks (while also achieving much higher reward— see Fig. 3). On the Push task, the cost is comparable due to the short episode duration. Analysis with respect to other criteria will be provided in an extended version of the article. 

TABLE II: Average inference times of planners. 

|**Task**|**Episode**<br>**Length**|**Planner**|**Num.**<br>**Iter.**|**Planning**<br>**Horizon**|**Inference**<br>**Time**|
|---|---|---|---|---|---|
|Walk|8.0s|iLQG|10|0.35s|1484.33s|
|Stand|2.0s|iLQG|2|0.35s|55.16s|
|Push|1.0s|Sampling|5|1.0s|38.93s|


While cheap at train-time (no pre-training needed), MPC is expensive at test-time because of online re-planning. Therefore, the choice of the i) planner, ii) planning horizon, and iii) number of planning iterations is crucial. Table II shows the run times of our experiments on a MacBook Air M1, 16GB, averaged over 12 runs. Each planner was given a fixed number of iterations to ensure a consistent comparison (normally, the planner would run as many iterations as possible within a real-time simulation timestep). 

# V. CONCLUSION 

In this paper, we made a step towards enabling easy experimentation with MPC for humanoid robot control in simulation. We ported HumanoidBench to MuJoCo MPC and provided evaluations on a subset of tasks. We showed that the current reward functions are insufficient and proposed shaping terms. Furthermore, we identified an issue with short episode lengths and argued for evaluating on repeated tasks with changing goals. Our results show superior performance of our method over MPC and RL baselines. 

REFERENCES 

- [1] Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine. Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor. In _International conference on machine learning_ , pages 1861–1870. PMLR, 2018. 

- [2] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

- [3] Nicklas Hansen, Hao Su, and Xiaolong Wang. Td-mpc2: Scalable, robust world models for continuous control. _arXiv preprint arXiv:2310.16828_ , 2023. 

- [4] Nicklas Hansen, Jyothir SV, Vlad Sobal, Yann LeCun, Xiaolong Wang, and Hao Su. Hierarchical world models as visual whole-body humanoid controllers. _arXiv preprint arXiv:2405.18418_ , 2024. 

- [5] Tairan He, Zhengyi Luo, Wenli Xiao, Chong Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Learning human-to-humanoid realtime whole-body teleoperation. _arXiv e-prints_ , pages arXiv–2403, 2024. 

- [6] Taylor Howell, Nimrod Gileadi, Saran Tunyasuvunakool, Kevin Zakka, Tom Erez, and Yuval Tassa. Predictive sampling: Real-time behaviour synthesis with mujoco. _arXiv preprint arXiv:2212.00541_ , 2022. 

- [7] Thomas M Moerland, Joost Broekens, Aske Plaat, Catholijn M Jonker, et al. Model-based reinforcement learning: A survey. _Foundations and Trends® in Machine Learning_ , 16(1):1–118, 2023. 

- [8] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [9] Carmelo Sferrazza, Dun-Ming Huang, Xingyu Lin, Youngwoon Lee, and Pieter Abbeel. Humanoidbench: Simulated humanoid benchmark for whole-body locomotion and manipulation. _arXiv preprint arXiv:2403.10506_ , 2024. 

- [10] Yuval Tassa, Tom Erez, and Emanuel Todorov. Synthesis and stabilization of complex behaviors through online trajectory optimization. In _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 4906–4913. IEEE, 2012. 

- [11] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ international conference on intelligent robots and systems_ , pages 5026–5033. IEEE, 2012. 

