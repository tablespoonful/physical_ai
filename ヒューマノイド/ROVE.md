---
title: "ROVE: Unlocking Human Interventions for Humanoid Manipulation via Reinforcement Learning"
date: "2026-06-15"
authors: "Wei Xiao; Weiliang Tang; Yuying Ge; Hui Zhou; Yao Mu; Li Zhang"
url: https://arxiv.org/abs/2606.17011
pdf: https://arxiv.org/pdf/2606.17011
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.17011)** / [論文ページ](https://arxiv.org/abs/2606.17011)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **ROVE: Unlocking Human Interventions for Humanoid Manipulation via Reinforcement Learning** 

**Wei Xiao**<sup>1</sup><sup>_,_2</sup><sup>_,∗_</sup> **Weiliang Tang**<sup>1</sup><sup>_,_3</sup><sup>_,∗_</sup> **Yuying Ge**<sup>1</sup><sup>_,†_</sup> **Hui Zhou**<sup>1</sup> **Yao Mu**<sup>4</sup> **Li Zhang**<sup>2</sup> **Yixiao Ge**<sup>1</sup> 

1XPENG Robotics 2Fudan University 3The Chinese University of Hong Kong 

4Shanghai Jiao Tong University 

- _∗_ Equal contribution _†_ Corresponding author https://xpeng-robotics.github.io/rove 


Figure 1: **ROVE learns from imperfect humanoid interventions.** (Left) Our method recovers task progress through re-matching and re-erasing. (Middle) Human interventions after near-failure VLA rollouts can deviate from ideal corrections in humanoid manipulation; our method learns a value function from mixed-quality and cross-embodiment experience to extract a better VLA policy. (Right) It outperforms all baselines and consistently improves across multiple iterations. 

**Abstract:** Human interventions provide crucial corrective signals for posttraining Vision-Language-Action (VLA) models. However, enabling seamless humanoid interventions is a formidable systems challenge due to complex wholebody kinematics and dexterous-hand control. Consequently, the collected intervention trajectories are often suboptimal, and methods that rely on human interventions as expert supervision can absorb hesitant, inefficient, or even erroneous behaviors. To address both the system and algorithmic challenges, we propose ROVE, a reinforcement learning framework for humanoid VLA post-training with imperfect human interventions. First, ROVE introduces a human-in-the-loop pipeline capable of collecting deployment and intervention data for humanoid manipulation. Second, it utilizes Optimistic Value Estimation (OVE) to prioritize high-value behaviors from mixed-quality trajectories. To further robustify value estimation, we incorporate cross-embodiment human experience videos to provide rich supervision for long-tailed failure and recovery modes. The resulting critic yields informative advantage signals, steering the VLA actor to focus on highvalue behaviors rather than indiscriminately imitating all actions. On challenging real-world contact-rich and fine-grained humanoid manipulation tasks, ROVE outperforms experience-learning baselines and consistently improves across multiple rollout-intervention iterations. 

**Keywords:** Vision-Language-Action Model, Reinforcement Learning, Humanoid Manipulation 

## **1 Introduction** 

Vision-Language-Action (VLA) models provide a promising foundation for general-purpose robot policies by grounding language instructions and visual observations into actions [1, 2]. Most recent progress has been largely demonstrated on robot-arm manipulation with parallel-jaw grippers, while extending VLA to humanoid robots with dexterous hands substantially increases the complexity of the robot dynamics and kinematics. This inherent complexity makes the humanoid robot fragile to accumulated errors stemming from whole-body poses, systematic errors, object contacts, etc. As a result, VLA policies trained only on offline demonstrations often fail to reach satisfactory performance during deployment, struggling to handle deployment-time distribution shift. Consequently, we seek a post-training solution to harness the deployment data for policy improvement. Reinforcement learning (RL) [3] and interactive imitation learning (IIL) [4, 5] allow robots to collect autonomous rollouts, observe their own failures, and incorporate human corrections. Recent post-training methods for VLA have shown that the deployment experience can improve pretrained policies beyond the offline demonstration tuning. Yet extending this paradigm to humanoid manipulation introduces a new difficulty: human teleoperation itself can be suboptimal, and this issue becomes especially severe during intervention takeover. 

In a robot-arm with grippers setup, teleoperation interfaces such as 3D space mouse or leaderfollower arms can often provide smooth and effective corrective actions [6, 7]. In contrast, humanoid teleoperation with dexterous hands is harder to master due to difficulty in whole-body coordination, dexterous manipulation, and joint-limit handling under imperfect retargeting and limited force or tactile feedback. During the takeover, even skilled operators may hesitate, retract their hands, or spend a period of time adapting to the humanoid’s current configuration. Prior human-in-the-loop RL (e.g., HIL-SERL [6], RECAP [3]) and IIL (e.g., HG-DAgger [5]) methods typically assume that human interventions provide optimal corrective actions, so intervention data can be directly treated as expert supervision or positive improvement signals. This assumption becomes fragile in humanoid manipulation: due to the large teleoperation gap, the takeover phase often contains hesitant, redundant, or retargeting-induced actions. The key challenge is therefore how to learn from suboptimal data. 

In this work, we propose **ROVE** , an **R** L framework with **O** ptimistic **V** alue **E** stimation for humanoid VLA post-training. ROVE builds a human-in-the-loop data collection pipeline that supports wholebody and dexterous-hand intervention during VLA rollouts. To account for suboptimal collected data, we decompose intervention episodes into rollout, adaptation, and recovery stages, and construct value labels with a conservative boundary at the end of adaptation. We further learn a state value function with _Optimistic Value Estimation (OVE)_ , which combines TD bootstrapping with expectile regression to estimate high-value recoverable behavior from mixed-quality data. Beyond robot trajectories, the critic also learns from videos of humans, which provide cross-embodiment supervision for progress and recovery without requiring robot-aligned actions. The learned critic provides advantage labels for advantage-conditioned policy extraction, allowing the VLA actor to emphasize high-value actions instead of imitating all collected actions uniformly. As shown in Fig. 1, ROVE improves upon SFT and experience-learning baselines, including RL and IIL methods, and continues to gain performance over multiple rollout-intervention iterations. 

Our main contributions are summarized as follows: **(i) Human-in-the-loop data collection pipeline for humanoid manipulation.** We build a whole-body human-in-the-loop collection pipeline and model the suboptimality of humanoid teleoperation, especially the noisy adaptation phase during intervention takeover; **(ii) Optimistic value estimation for heterogeneous experience.** We propose a state-value learning recipe that combines robot rollouts, human intervention trajectories, and human experience videos, producing robust advantage signals for policy extraction; **(iii) Iterative VLA policy improvement in real-world tasks.** Real-world experiments on two manipulation tasks, illustrated in Fig. 2, show that ROVE improves VLA policies from demonstrations, experience, and multiple rounds of rollout-intervention data. 

2 


Figure 2: Task procedures for _Put the bread into the toaster_ (top) and _Erase the whiteboard_ (bottom). 

## **2 Preliminary** 

**Problem setting and notation.** We formulate the humanoid manipulation problem as a Markov Decision Process (MDP) _M_ = ( _S, A, P, r, γ_ ) in a standard RL setting [8], where _S_ is the environment state space, _O_ is the image observation space from humanoid’s ego-view, _L_ is the language space of the robot’s task instruction. _A_ is the action space of the robot, _P_ : _S × A →_ ∆( _S_ ) is the stochastic dynamics of the environment, _r_ : _S × A →_ R is the reward function, the discount factor _γ ∈_ [0 _,_ 1]. ROVE starts from a generalist VLA model as the initial policy _at_ : _t_ + _H−_ 1 _∼ π_ ( _·|st_ ), _st_ = ( _ot, l_ ), _ot ∈ O, l ∈L_ , _H_ is the action chunk horizon. We distinguish the environment state _xt ∈S_ from the critic input _st_ = ( _ot, l_ ). The actor additionally receives proprioceptive state, omitted from policy notation for brevity. Given the robot policy and environment’s transition _xt_ +1: _t_ + _H ∼ P_ ( _·|xt, at_ : _t_ + _H−_ 1), a set of trajectories is collected: _ξ_ = ( _s_ 0 _, a_ 0 _, r_ 0 _, s_ 1 _, · · · , aT −_ 1 _, rT −_ 1 _, sT , rT_ ) through interactions between the policy _π_ and environment, and the distribution of trajectories is _ρπ_ ( _ξ_ ). We can define the discounted cumulative reward, or return, as _R_ ( _ξ_ ) =<sup>�</sup><sup>_T_</sup> _t_ =0<sup>_γtrt_.The goal of RL is to maximize</sup> the expected discounted return: _J_ ( _π_ ) = E _ξ∼ρπ_ [ _R_ ( _ξ_ )] = E _ξ∼ρπ_ [<sup>�</sup><sup>_T_</sup> _t_ =0<sup>_γtrt_].</sup> 

**Value estimation.** For a policy _π_ , the value function _V_<sup>_π_</sup> ( _st_ ) is the expected future return E _ρπ_ ( _ξ_ )[<sup>�</sup> _i_<sup>_T_</sup> = _t_<sup>_γi−tri|st_].Then,wecandefinetheadvantageoftheactionchunk</sup><sup>_at_:</sup><sup>_t_+</sup><sup>_H−_1at</sup> state _st_ with _t_ + _H ≤ T_ as _A_<sup>_π_</sup> ( _st, at_ : _t_ + _H−_ 1) = E _ρπ_ ( _ξ_ )[<sup>�</sup> _i_<sup>_t_</sup> =<sup>+</sup> _t_<sup>_H−_1</sup> _γ_<sup>_i−t_</sup> _ri_ + _γ_<sup>_H_</sup> _V_<sup>_π_</sup> ( _st_ + _H_ ) _| st, at_ : _t_ + _H−_ 1] _− V_<sup>_π_</sup> ( _st_ ). In practice, we learn a parametric critic _Vϕ_ ( _st_ ) from collected trajectories to estimate future return. Monte-Carlo method (MC) regresses the critic toward the empirical discounted return, while Temporal-difference method (TD) bootstraps after the action chunk: 


where _V_ ¯ _ϕ_ denotes a target network or a stop-gradient copy of _Vϕ_ . MC estimates are unbiased when complete returns are observed but can have high variance, while TD estimates reduce variance at the cost of bootstrapping bias. 

## **3 Methodology** 

Fig. 3 summarizes the overall ROVE framework. The method first collects mixed-quality real-world experience on the humanoid robot, then learns a state-value critic from robot trajectories and human experience videos, and finally uses the resulting advantage signals to extract a stronger VLA policy. We describe these components in order. 

### **3.1 Human-in-the-loop data collection** 

**Pipeline overview.** We build a human-in-the-loop data collection pipeline that enables whole-body intervention during VLA policy rollouts. Each episode starts with autonomous execution, where the VLA policy predicts action chunks conditioned on the ego-view observation, task instruction, and proprioceptive state. When the supervisor detects a potential failure, the VLA action publisher is paused. Meanwhile, the motion-capture operator observes the robot state through a VR headset 

3 


Figure 3: **Overview of ROVE framework.** A VLA actor collects autonomous rollouts and triggers whole-body human intervention near failure. The resulting trajectories are decomposed into rollout, adaptation, and recovery stages, and combined with cross-embodiment human experience to train a state-value critic. The critic provides advantage conditions for policy extraction, guiding the actor toward high-value recovery behaviors from mixed-quality data. 

and aligns their body and hand pose with the current humanoid and dexterous hand configuration as closely as possible. 

Once the operator is ready, the supervisor switches the robot from autonomous execution to teleoperation. The teleoperation interface maps the operator’s whole-body and hand motion to humanoid control commands. Since the human pose and robot state may not be perfectly aligned at the takeover moment, we apply a command filter in the controller to smooth the transition and avoid abrupt changes in robot joint angles. The pause interval between policy rollout and human takeover is removed during post-processing. During takeover, the operator starts from the terminal state of the VLA rollout, which is typically close to failure, and provides corrective actions until the task is completed. To balance the data distribution and increase trajectory diversity, we also initialize data collection from different task progress stages rather than only from the beginning of each task [9]. 

**Teleoperation gap and intervention suboptimality.** Human-in-the-loop episodes are split into three stages: (1) Autonomous VLA rollout, (2) Intervention–adaptation, and (3) Intervention– recovery and task completion. Unlike prior human-in-the-loop settings on standard robot arms, whole-body humanoid intervention with dexterous hands introduces a much larger teleoperation gap. This gap arises from the higher complexity of the robot morphology, the lack of force and tactile feedback, imperfections in motion retargeting, operator skill differences, and robot joint limits. As a result, a seamless transition from policy rollout to human intervention is difficult to achieve in practice. Even for highly skilled motion-capture operators, the initial takeover phase often involves unstable or hesitant motion. Common behaviors in this phase include retracting the hand, continuing to manipulate from a near-failure state, or spending a period of time adapting to the robot’s current configuration. We refer to this transient phase as the _adaptation stage_ . After the operator significantly advances task progress, the trajectory enters the _recovery and completion stage_ , where the operator continues the task until the task is completed. 

**Reward design.** Following the stage decomposition above, we assign rewards according to both task outcome and intervention phase: 

4 


Here, _T_ denotes the terminal timestep of an episode, and _tr_ marks the end of the initial adaptation stage, after which intervention begins to produce sustained task progress. We therefore assign the penalty at _tr_ rather than at intervention onset; this conservative boundary avoids mixing adaptationstage alignment behavior into recovery labels (see Appendix B). During task fine-tuning, we set _C_ fail = _−_ 500. During pretraining, we set _C_ fail to the negative mean episode length of each task, which provides a task-normalized failure scale. We set _γ_ = 1 in our experiments. Except at the adaptation boundary, non-terminal steps receive a penalty of _rt_ = _−_ 1, encouraging shorter completion times. 

### **3.2 Value function training** 

**Data recipe and pretraining objective.** The value function is trained in stages. We first pretrain the critic on large-scale robot and egocentric human demonstrations [10] to learn a general notion of task progress, then fine-tune it for the downstream task. In later iterations, we train the critic on autonomous rollouts and intervention trajectories, with task-relevant human experience videos. These videos provide cross-embodiment examples of recovery and completion that are sparse in robot experience, improving value estimates on partial-progress and near-failure states. For pretraining, we use a Monte-Carlo regression objective to fit the cumulative return from each state: 


This objective estimates the average return of the dataset behavior distribution. It is stable for largescale pretraining on heterogeneous data from different tasks and embodiments, and provides a robust initialization for task-level fine-tuning. 

**Optimistic value estimation.** For fine-tuning, however, estimating only the average return can be overly conservative. Our training data contain many suboptimal teleoperated behaviors, failed autonomous rollouts, and transient adaptation segments after takeover. If the critic simply averages over these trajectories, the estimated value can be much lower than the value of the best recoverable behavior from the same state. 

To address this issue, we use _Optimistic Value Estimation (OVE)_ , combining an _H_ -step TD bootstrap [11] with expectile regression. Related expectile-based value-learning objectives have been studied in [12, 13, 14]. Given a transition segment of length _H_ , we define the bootstrapped target as 


where _V_ ¯ _ϕ_ is an EMA target critic updated from _Vϕ_ . Instead of fitting the bootstrapped target _V_<sup>ˆ</sup> _t_ with a symmetric squared loss, we use an expectile loss, where _τ_ controls the degree of optimism. When _τ_ = 0 _._ 5, the objective reduces to standard mean regression; as _τ_ approaches 1, the critic places more weight on higher-value outcomes. Thus, OVE estimates an in-distribution optimistic statistic: it favors better recoveries observed in the data without querying out-of-distribution actions. 

### **3.3 Policy improvement and implementation details** 

The VLA actor is trained with advantage conditioning to indicate whether an action chunk is predicted to improve task progress. Algorithm 1 summarizes the iterative loop. In each iteration, we 

5 


Figure 4: **Policy improvement results on two real-world humanoid manipulation tasks.** ROVE (Ours) outperforms SFT in the demonstration-only setting, achieves the best average performance among experience-learning methods, and consistently improves across multiple iterations of rollout and intervention data. 

update critic and actor sequentially: train the critic with _Dk_<sup>_critic_</sup> , compute advantage statistics on _Dk_<sup>_actor_</sup> , assign binary advantage via a threshold, and fine-tune the actor (details in Appendix F). Our experiments use the IRON-R01-1.11 humanoid robot with a 50-dimensional proprioceptive state and action space covering body joints and dexterous hands. With limited task-specific robot data, conditioning on the high-dimensional proprioceptive state can overfit to brittle joint-level cues. We therefore apply state dropout and perturbation during training to rely more on visual task progress (details in Appendix G). 

## **4 Experiments** 

Our experiments are conducted in two real-world humanoid manipulation tasks: a contact-rich task ( _Erase the whiteboard_ ) and a fine-grained task ( _Put the bread into the toaster_ ). The analysis is organized around two aspects: policy improvement and value estimation. 

### **4.1 Policy improvement results and analysis** 

**Learn from demonstrations.** We fine-tune the pretrained VLA with either standard SFT or ROVE using teleoperated demonstrations. Fig. 4 shows that ROVE improves over SFT on both tasks. This suggests that humanoid teleoperation demonstrations can be suboptimal due to the teleoperation gap and operator variability, and that value-guided extraction recovers higher-quality behavior than uniform imitation. 

**Learn from experience.** We compare ROVE with experience-learning baselines, including HGDAgger [5], Filtered BC, and RECAP [3] (details in Appendix E). Fig. 4 shows that ROVE achieves the best average success rate across tasks. A notable result is that HG-DAgger performs poorly, even below the base demonstration-only policy on both tasks, and its learned policy often exhibits hesitant behavior. This pattern reflects the suboptimality of directly imitating intervention data. Compared with RECAP, the remaining gap reflects the combined effect of critic quality and advantage assignment of post-adaptation intervention segments. Compared with Filtered BC, the gap suggests that RL-style policy learning provides additional gains beyond BC-style data filtering, particularly in how negative samples are incorporated during policy optimization. As a control, scaling up SFT 

6 


Figure 5: **Human experience improves value estimation.** Adding human experience helps the critic assign lower values to incomplete erasing states and better reflect true task progress. 


Figure 6: **OVE provides sharper value estimates than Monte-Carlo estimates** , producing clearer negative-advantage regions during failure and recovery. 

demonstrations yields additional gains, while the failure-recovery behaviors of ROVE are rarely observed in these demonstration-only policies at deployment. 

**Iterative improvement.** We collect a comparable amount of real-world rollout and intervention data in each iteration, then update the value function and policy from the previous iteration. As shown in Fig. 4, ROVE consistently improves across three iterations on both tasks. The success rate increases from 45.0% to 80.0% on _Erase the whiteboard_ , and from 56.7% to 86.7% on _Put the bread into the toaster_ . This demonstrates that it forms a closed-loop improvement process: better policies collect more informative experience, and the value function provides increasingly useful advantage signals for subsequent policy updates. 

### **4.2 Value estimation analysis** 

We then examine the value function behind policy gains, focusing on how human experience and optimistic value estimation affect the reliability and resolution of value estimates. 

**Human experience.** Fig. 5 compares two critics trained with and without human experience videos on the same held-out trajectory. Without human experience, the critic tends to overestimate intermediate states where the robot only partially erases the handwriting. In contrast, the critic trained with human experience assigns lower values to these incomplete states and produces a value curve that better follows actual task progress. Human trajectories provide examples of recovery from nearfailure or incomplete states that are rarely covered by autonomous rollouts, yielding more reliable advantage estimates for policy improvement. 

**Value learning objective.** Fig. 6 compares OVE with MC value estimation on a held-out trajectory containing both failure and recovery segments. The MC critic estimates the average return of the full data buffer and tends to produce noisy, less discriminative values when successful recoveries and failed rollouts are mixed. OVE instead produces a more structured value curve that better follows 

7 

task progress. In particular, during the erase-failure segment, OVE assigns lower values and yields negative-advantage regions, indicating that the critic recognizes actions that move the trajectory away from successful completion. When the robot later re-erases the board and recovers the task, the value increases accordingly. These observations are consistent with OVE providing a sharper training signal for policy extraction by distinguishing harmful actions from recoverable progress while remaining in-distribution over observed trajectories. 

## **5 Related work** 

**Reinforcement learning for VLA post-training.** Reinforcement learning has become a key route for improving VLA policies beyond imitation-only tuning. Prior work spans simulation-scale onpolicy RL [15, 16], real-world experience learning with advantage conditioning [3], world-modelbased policy improvement [17, 18, 19, 20], and fleet-scale offline-to-online adaptation [21]. Collectively, these results establish the importance of learning from deployment experience for VLA improvement. ROVE extends this paradigm to real-world humanoid manipulation with dexterous hands, where higher embodiment complexity makes experience distributions noisier and critic robustness more critical than in robot-arm settings. 

**Human-in-the-loop robot learning.** Human-in-the-loop learning improves data efficiency by letting humans recover policy failures during deployment [22, 6]. Recent work extends this idea to preference-style refinement [23], dexterous interventions [24], and seamless hand-arm takeover [25], often under assumptions that intervention corrections can be treated as high-quality supervision. As embodiment complexity increases, however, takeover misalignment and adaptation behavior naturally become more prominent in intervention trajectories. ROVE is designed for this regime by treating intervention data as mixed-quality and learning value signals that separate recovery behavior from naturally occurring takeover noise. 

A more comprehensive discussion is provided in Appendix A. 

## **6 Conclusion** 

We presented ROVE, an RL framework for post-training humanoid VLA policies from demonstrations, autonomous rollouts, human interventions, and human experience videos. The core challenge is that humanoid teleoperation data are not uniformly expert, especially during intervention. We address this with stage-aware intervention labeling, an optimistic state-value critic learned from heterogeneous experience, and advantage-conditioned actor training. Real-world experiments show that ROVE improves over SFT, compares favorably with experience-learning baselines, and continues to improve over rollout-intervention iterations. These results support ROVE as a practical path for robust humanoid VLA post-training from informative but imperfect deployment experience. 

## **7 Limitations** 

First, human experience is currently used only for value learning, not for direct policy learning. Future work could use representation-level supervision to let policies benefit from human videos. Second, our system lacks end-effector sensing such as wrist cameras and tactile feedback, which limits precise manipulation. Third, we have not yet extended ROVE to loco-manipulation. Future extensions will need to handle locomotion and intervention safety. Finally, ROVE is mainly an offline or iterative offline RL framework. Extending it to online RL would require efficient exploration and stable deployment-time updates. 

8 

## **References** 

- [1] J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint_ , 2025. 

- [2] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, M. Y. Galliker, D. Ghosh, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, D. LeBlanc, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, A. Z. Ren, L. X. Shi, L. Smith, J. T. Springenberg, K. Stachowicz, J. Tanner, Q. Vuong, H. R. Walke, A. Walling, H. Wang, L. Yu, and U. Zhilinsky. _π_ 0.5: a vision-language-action model with open-world generalization. In _CoRL_ , 2025. 

- [3] P. Intelligence, A. A. Amin, R. J. Aniceto, A. Balakrishna, K. Black, K. Conley, G. Connors, J. Darpinian, K. Dhabalia, J. DiCarlo, D. Driess, M. Equi, A. Esmail, Y. Fang, C. Finn, C. Glossop, T. Godden, I. Goryachev, L. Groom, H. Hancock, K. Hausman, G. Hussein, B. Ichter, S. Jakubczak, R. Jen, T. Jones, B. Katz, L. Ke, C. Kuchi, M. Lamb, D. LeBlanc, S. Levine, A. Li-Bell, Y. Lu, V. Mano, M. Mothukuri, S. Nair, K. Pertsch, A. Z. Ren, C. Sharma, L. X. Shi, L. Smith, J. T. Springenberg, K. Stachowicz, W. Stoeckle, A. Swerdlow, J. Tanner, M. Torne, Q. Vuong, A. Walling, H. Wang, B. Williams, S. Yoo, L. Yu, U. Zhilinsky, and Z. Zhou. _π_ *0.6: a vla that learns from experience. _arXiv preprint_ , 2025. 

- [4] S. Ross, G. Gordon, and D. Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _AISTATS_ , 2011. 

- [5] M. Kelly, C. Sidrane, K. Driggs-Campbell, and M. J. Kochenderfer. Hg-dagger: Interactive imitation learning with human experts. In _ICRA_ , 2019. 

- [6] J. Luo, C. Xu, J. Wu, and S. Levine. Precise and dexterous robotic manipulation via humanin-the-loop reinforcement learning. _Science Robotics_ , 2025. 

- [7] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn. Learning fine-grained bimanual manipulation with low-cost hardware. In _RSS_ , 2023. 

- [8] R. S. Sutton, A. G. Barto, et al. _Reinforcement learning: An introduction_ . MIT press Cambridge, 1998. 

- [9] I. Uchendu, T. Xiao, Y. Lu, B. Zhu, M. Yan, J. L. P. Sim´on, M. Bennice, C. Fu, C. Ma, J. Jiao, S. Levine, and K. Hausman. Jump-start reinforcement learning. _ICML_ , 2023. 

- [10] R. Hoque, P. Huang, D. J. Yoon, M. Sivapurapu, and J. Zhang. Egodex: Learning dexterous manipulation from large-scale egocentric video. In _ICLR_ , 2026. 

- [11] S. Park, K. Frans, D. Mann, B. Eysenbach, A. Kumar, and S. Levine. Horizon reduction makes rl scalable. In _NeurIPS_ , 2025. 

- [12] I. Kostrikov, A. Nair, and S. Levine. Offline reinforcement learning with implicit q-learning. In _ICLR_ , 2022. 

- [13] S. Park, D. Ghosh, B. Eysenbach, and S. Levine. HIQL: Offline goal-conditioned RL with latent states as actions. In _NeurIPS_ , 2023. doi:10.52202/075280-1515. 

- [14] H. Xu, L. Jiang, J. Li, and X. Zhan. A policy-guided imitation approach for offline reinforcement learning. In _NeurIPS_ , 2022. doi:10.52202/068431-0295. 

- [15] H. Li, Y. Zuo, J. Yu, Y. Zhang, Z. Yang, K. Zhang, X. Zhu, Y. Zhang, T. Chen, G. Cui, et al. Simplevla-rl: Scaling vla training via reinforcement learning. In _ICLR_ , 2026. 

- [16] G. Lu, W. Guo, C. Zhang, Y. Zhou, H. Jiang, Z. Gao, Y. Tang, and Z. Wang. Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning. _arXiv preprint_ , 2025. 

9 

- [17] J. Yang, K. Lin, J. Li, W. Zhang, T. Lin, L. Wu, Z. Su, H. Zhao, Y.-Q. Zhang, L. Chen, et al. Rise: Self-improving robot policy with compositional world model. _arXiv preprint_ , 2026. 

- [18] J. Zhang, Z. Huang, C. Gu, Z. Ma, and L. Zhang. Reinforcing action policies by prophesying. _arXiv preprint_ , 2025. 

- [19] F. Zhu, Z. Yan, Z. Hong, Q. Shou, X. Ma, and S. Guo. Wmpo: World model-based policy optimization for vision-language-action models. In _ICLR_ , 2026. 

- [20] H. Li, P. Ding, R. Suo, Y. Wang, Z. Ge, D. Zang, K. Yu, M. Sun, H. Zhang, D. Wang, and W. Su. Vla-rft: Vision-language-action reinforcement fine-tuning with verified rewards in world simulators. _arXiv preprint_ , 2025. 

- [21] Y. Wang, X. Li, P. Xie, P. Yang, B. Nie, Y. Cai, Q. Zhang, C. Qu, J. Wu, J. Song, et al. Learning while deploying: Fleet-scale reinforcement learning for generalist robot policies. _arXiv preprint_ , 2026. 

- [22] H. Liu, S. Nasiriany, L. Zhang, Z. Bao, and Y. Zhu. Robot learning on the job: Human-in-theloop autonomy and learning during deployment. In _RSS_ , 2023. 

- [23] W. Xia, Y. Yang, H. Wu, X. Ma, T. Kong, and D. Hu. Human-assisted robotic policy refinement via action preference optimization. In _NeurIPS_ , 2025. 

- [24] Y. Han, Z. Chen, Y. Zhao, C. Xu, Y. Shao, Y. Peng, Y. Mu, and W. Lian. Dexhil: A human-inthe-loop framework for vision-language-action model post-training in dexterous manipulation. _arXiv preprint_ , 2026. 

- [25] Z. Li, L. Huang, W. Xu, Z. Zhu, N. Lin, X. Ma, X. Sheng, and R. Wen. Hand-in-the-loop: Improving dexterous vla via seamless interventional correction. _arXiv preprint_ , 2026. 

- [26] J. Luo, Z. Hu, C. Xu, Y. L. Tan, J. Berg, A. Sharma, S. Schaal, C. Finn, A. Gupta, and S. Levine. Serl: A software suite for sample-efficient robotic reinforcement learning. In _ICRA_ , 2024. 

- [27] K. Lei, H. Li, D. Yu, Z. Wei, L. Guo, Z. Jiang, Z. Wang, S. Liang, and H. Xu. Rl-100: Performant robotic manipulation with real-world reinforcement learning. _arXiv preprint_ , 2025. 

- [28] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms. _arXiv preprint_ , 2017. 

- [29] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li, Y. Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint_ , 2024. 

- [30] C. Xu, J. T. Springenberg, M. Equi, A. Amin, A. Esmail, S. Levine, and L. Ke. Rl token: Bootstrapping online rl with vision-language-action models. _arXiv preprint_ , 2026. 

- [31] T. Johannink, S. Bahl, A. Nair, J. Luo, A. Kumar, M. Loskyll, J. A. Ojea, E. Solowjow, and S. Levine. Residual reinforcement learning for robot control. In _ICRA_ , 2019. 

- [32] Z. Gong, S. Lyu, P. Ding, W. Xiao, and D. Wang. Robust online residual refinement via koopman-guided dynamics modeling. _arXiv preprint_ , 2025. 

- [33] Y. Li, X. Ma, J. Xu, Y. Cui, Z. Cui, Z. Han, L. Huang, T. Kong, Y. Liu, H. Niu, et al. Gr-rl: Going dexterous and precise for long-horizon robotic manipulation. _arXiv preprint_ , 2025. 

- [34] A. Wagenmaker, M. Nakamoto, Y. Zhang, S. Park, W. Yagoub, A. Nagabandi, A. Gupta, and S. Levine. Steering your diffusion policy with latent space reinforcement learning. In _CoRL_ , 2025. 

- [35] S. Levine, A. Kumar, G. Tucker, and J. Fu. Offline reinforcement learning: Tutorial, review, and perspectives on open problems. _arXiv preprint_ , 2020. 

10 

- [36] A. Kumar, A. Zhou, G. Tucker, and S. Levine. Conservative q-learning for offline reinforcement learning. In _NeurIPS_ , 2020. 

- [37] H. Xu, L. Jiang, J. Li, Z. Yang, Z. Wang, V. Chan, and X. Zhan. Offline rl with no ood actions: In-sample learning via implicit value regularization. In _ICLR_ , 2023. 

- [38] K. Frans, S. Park, P. Abbeel, and S. Levine. Diffusion guidance is a controllable policy improvement operator. _arXiv preprint_ , 2025. 

- [39] J. Fu, A. Kumar, O. Nachum, G. Tucker, and S. Levine. D4rl: Datasets for deep data-driven reinforcement learning. _ArXiv_ , 2021. 

- [40] S. Zhai, Q. Zhang, T. Zhang, F. Huang, H. Zhang, M. Zhou, S. Zhang, L. Liu, S. Lin, and J. Pang. A vision-language-action-critic model for robotic real-world reinforcement learning. _arXiv preprint_ , 2025. 

- [41] A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv, C. Zheng, D. Liu, F. Zhou, F. Huang, F. Hu, H. Ge, H. Wei, H. Lin, J. Tang, J. Yang, J. Tu, J. Zhang, J. Yang, J. Yang, J. Zhou, J. Zhou, J. Lin, K. Dang, K. Bao, K. Yang, L. Yu, L.-C. Deng, M. Li, M. Xue, M. Li, P. Zhang, P. Wang, Q. Zhu, R. Men, R. Gao, S.-Q. Liu, S. Luo, T. Li, T. Tang, W. Yin, X. Ren, X. Wang, X. Zhang, X. Ren, Y. Fan, Y. Su, Y.-C. Zhang, Y. Zhang, Y. Wan, Y. Liu, Z. Wang, Z. Cui, Z. Zhang, Z. Zhou, and Z. Qiu. Qwen3 technical report. _arXiv preprint_ , 2025. 

- [42] W. S. Peebles and S. Xie. Scalable diffusion models with transformers. In _ICCV_ , 2023. 

11 

## **A Extended related work** 

This section provides an extended related-work discussion with additional representative directions and technical context. 

### **A.1 Reinforcement learning for VLA post-training** 

Reinforcement learning has shown the potential to improve robot policies beyond imitation learning by optimizing task outcomes from physical interaction. Recent systems demonstrate strong performance on real-world manipulation with efficient off-policy RL [26], human corrections [6], and carefully designed training pipelines [27]. In parallel, reinforcement post-training for VisionLanguage-Action (VLA) models has become an active direction. Li et al. [15], Lu et al. [16] improve VLAs via on-policy RL [28, 29] in simulation, while Intelligence et al. [3] shows experience learning with advantage conditioning in real-world deployment. Yang et al. [17], Zhang et al. [18], Zhu et al. [19], Li et al. [20] improve VLAs through imagined rollouts and value-based evaluation in learned world models, and Wang et al. [21] studies fleet-scale offline-to-online RL for continual adaptation of generalist policies. Additional interfaces include representation-level residual RL [30, 31, 32] and latent-space RL with progress-based filtering [33, 34]. Within this landscape, ROVE targets real-world humanoid post-training with dexterous hands, where embodiment complexity makes experience statistics and critic robustness especially important. 

### **A.2 Human-in-the-loop robot learning** 

Human-in-the-loop robot learning improves data efficiency by allowing humans to correct policy failures during deployment. Liu et al. [22] studies human-in-the-loop autonomy where assistance is used both for failure recovery and policy improvement over time. Luo et al. [6] integrates demonstrations and online corrections into real-world RL, showing substantial acceleration. Action preference optimization further uses human-assisted rollouts for preference-style refinement [23]. For dexterous settings, Han et al. [24] extends human-in-the-loop post-training to coordinated arm-hand interventions, while Li et al. [25] shows that takeover mismatch can cause abrupt gesture jumps and post-intervention degradation. Together, these studies highlight both the value of intervention data and the growing importance of takeover quality as embodiment complexity increases. ROVE follows this direction but treats intervention trajectories as inherently mixed-quality in high-complexity humanoid teleoperation, rather than assuming uniformly high-quality corrective supervision. 

### **A.3 Value learning for offline and off-policy data** 

Value learning is central to extracting improved behavior from offline and off-policy data, especially when datasets mix successful recoveries with suboptimal teleoperation and failed rollouts [35]. In classical offline RL, a state-action value function _Q_ ( _s, a_ ) is often trained on static or heterogeneous data, leading to distributional shift and overestimation of out-of-distribution actions. Kumar et al. [36] mitigates this issue by penalizing over-optimistic _Q_ -values, while in-sample methods such as Xu et al. [37], Kostrikov et al. [12] avoid querying unseen actions through implicit regularization. Recent robot and VLA post-training systems also increasingly use value or critic models to improve policies from deployment data: Lei et al. [27], Wang et al. [21] combine offline and online learning with IQL [12] or its distributional variant in real-world settings. ROVE follows this broad valuelearning motivation but learns a state value _V_ ( _s_ ) rather than a state-action value _Q_ ( _s, a_ ), allowing the critic to use robot rollouts, human intervention trajectories, and cross-embodiment human experience videos under a unified objective for optimistic state-value estimation. 

## **B Sensitivity of value-label construction** 

Table 1 studies two implementation choices in value-label construction: the horizon used for TD bootstrapping and advantage computation, and the timing _tr_ of the penalty reward. Increasing the 

12 

Table 1: Sensitivity of value-label construction. We vary critic horizon and penalty reward timing _tr_ while keeping all other settings fixed on the _Erase the whiteboard_ task. 

|Setting|Success rate|Change vs. default|
|---|---|---|
|**ROVE (default)**(_H_ = 16,_tr_ after adaptation)|**80%**|-|
|Long critic horizon (_H_ = 50)|65%|-15%|
|_tr_ at intervention start(_H_ = 50)|50%|-30%|


horizon from _H_ = 16 to _H_ = 50 reduces success from 80% to 65%, indicating that an overly long horizon makes advantage labels less responsive to local recovery progress. Moving the penalty reward to takeover start further reduces success to 50%, because adaptation-stage alignment behavior is then mixed into recovery labels. This result does not suggest that the boundary requires precise manual tuning; instead, it reveals an asymmetric risk in intervention data. A slightly delayed boundary is conservative and may omit some early recovery actions, whereas an overly early boundary introduces noisier adaptation-stage behavior into value targets. Since OVE preferentially propagates high-value continuations observed in data, this early-boundary noise can be amplified into misleadingly optimistic labels. We therefore place the boundary after the adaptation stage so OVE propagates value through cleaner recovery segments. 

## **C Comparison with IQL** 

IQL [12] is an offline RL method that learns an in-distribution optimistic value through expectile regression. In the standard IQL formulation, a state-action critic _Qθ_ ( _st, at_ ) is first trained with a Bellman backup: 


The value function is then fitted as an upper expectile of the action-value distribution under dataset actions: 


The resulting advantage is computed as 


and is then used for CFGRL-style policy extraction [38]. This design avoids explicitly querying out-of-distribution actions, but it still relies on a state-action value function whose action input must be well defined within a single embodiment and action space. 

We adopt the same principle of in-distribution optimism, but use it differently. Instead of learning _Q_ ( _st, at_ ), we directly learn a state value _Vϕ_ ( _st_ ) with a bootstrapped target: _V_<sup>ˆ</sup> _t_ = _rt_ + _γVϕ_ ¯( _st_ +1) _._ For brevity, we present the one-step TD form here to align with the IQL notation above. The expectile objective is applied between _V_<sup>ˆ</sup> _t_ and _Vϕ_ ( _st_ ), yielding an optimistic state-value estimator. This choice is important for our setting because the data used for value learning include robot rollouts, human intervention trajectories, and cross-embodiment human experience videos. These sources do not always share a compatible robot action representation, making a unified _Q_ ( _s, a_ ) difficult to define and prone to action-space overfitting. A state-value critic, in contrast, allows ROVE to use heterogeneous experience for value learning while still producing advantage labels for policy extraction. 

We additionally compare OVE with IQL on D4RL-AntMaze tasks [39] in Fig. 7. The results show that OVE achieves competitive performance across medium and large maze variants, supporting that state-value optimistic estimation can serve as a practical alternative to Q-based expectile learning. 

## **D Task description and evaluation protocol** 

Fig. 2 illustrates the manipulation procedure for each task. For _Put the bread into the toaster_ , the task begins with bread slices in a container and a two-slot toaster on the table. A trial proceeds 

13 


Figure 7: Performance comparison between OVE and IQL on D4RL-AntMaze tasks. 


Figure 8: Evaluation objects and layout for our tasks. 

through reaching into the container, grasping one slice, lifting and transporting it above the toaster slot, inserting the bread, releasing it, and retracting the hand. A trial is counted as successful if the bread is fully inserted into the toaster slot and remains stable. For _Erase the whiteboard_ , the task begins with an eraser on a tray and handwriting marks on the board. A trial proceeds through picking up the eraser, moving to the marked region, establishing contact, wiping across the assigned marks with sufficient coverage, and lifting the eraser after erasing. A trial is successful if all handwriting marks assigned to that trial are removed. To complete these tasks, a humanoid robot requires coordinated dexterous hand manipulation, head motion(e.g., locating handwriting on the board), and waist adjustment (left-right rotation or forward lean) to maintain effective contact and reachability. 

Fig. 8 summarizes the evaluation objects and scene layout used in our experiments. For _Erase the whiteboard_ , we draw twenty handwriting marks uniformly distributed on the whiteboard and run one evaluation trial per mark, for twenty trials in total. For _Put the bread into the toaster_ , we run thirty 

14 

independent trials per policy. Success rate is computed as the number of successful trials divided by the total number of trials. 

## **E Baselines** 

We compare ROVE against three experience-learning baselines, implemented on the same humanoid platform, data collection protocol, and VLA backbone. 

**HG-DAgger** [5, 4] follows the interactive imitation learning paradigm: during policy rollouts, a human operator takes over when the policy approaches failure, and the corrected trajectories are aggregated into the training set for behavior cloning. In our implementation, HG-DAgger uses the same rollout–intervention episodes as ours but treats all human-intervention actions as positive supervision. 

**RECAP** [3] follows the _π_ 0<sup>_∗_</sup> _._ 6<sup>-styleexperience-learningrecipe:acriticprovidesprogressorad-</sup> vantage signals from deployment experience, and the VLA actor is fine-tuned with advantageconditioned behavior cloning to prefer high-value action chunks over uniform imitation. For a controlled comparison with ROVE, RECAP uses the same robot data and the same reward-label construction pipeline; the key differences are that its critic training objective differs from OVE and its labeling strategy treats human intervention segments after the adaptation stage as uniformly positive advantages. 

**Filtered BC** filters rollout and intervention data before behavior cloning. Following progress-based data refinement ideas [33], we retain trajectory segments whose critic-estimated advantage exceeds a threshold and discard segments associated with failed or low-advantage states. To isolate the policylearning objective, Filtered BC uses the same critic checkpoint as ours for advantage scoring and performs thresholded data filtering plus standard BC. 

## **F Policy extraction via advantage conditioning** 

Advantage conditioning provides a supervised way to extract an improved policy from experience [38, 3]. Let _I_ denote an improvement event indicating that an action chunk is preferred over the typical behavior of a reference policy _π_ ref at the same state. Given an advantage estimate _A_<sup>_π_ref</sup> ( _st, at_ : _t_ + _H−_ 1), policy improvement can be written as a target action distribution that reweights the reference policy by the likelihood of improvement: 


Since the improvement event is determined by the advantage label, _p_ ( _I|A_<sup>_π_ref</sup> ) can be implemented as an additional condition on the action model. Equivalently, we train a conditional policy _πθ_ ( _at_ : _t_ + _H−_ 1 _|st, I_ ) by behavior cloning on trajectories annotated with discretized or binary advantage labels: 


In implementation, we instantiate the improvement event _I_ as a binary advantage label computed by the learned critic. Before actor training, we set the threshold _ηk_ to the 70th percentile of the advantage distribution. Each training action chunk is then labeled as positive if its advantage exceeds _ηk_ and negative otherwise. For CFGRL-style conditioning [38], we append a text condition to the instruction and train the VLA actor with the standard action prediction loss. At inference time, the actor uses classifier-free-guidance-style decoding: it predicts action velocities under both positive and negative conditions, and combines them as _v_ cfg = _v_ neg + _β_ ( _v_ pos _−v_ neg). This guides generation toward high-advantage actions rather than simply querying a single positive condition. 

## **G Additional training and implementation details** 

This appendix records the full policy-improvement procedure and the implementation settings that complement the main method description. 

15 

**Algorithm 1** ROVE: Iterative policy improvement 

- **Require:** Initial policy _πθ_ 0, initial actor and critic data buffers _D_ 0<sup>actor</sup> and _D_ 0<sup>critic</sup> , number of iterations _K_ 

- 1: **for** _k_ = 0 _, . . . , K −_ 1 **do** 2: Train critic _Vϕk_ on _Dk_<sup>_critic_</sup> with the OVE objective 

- 3: Compute advantages for each transition segment: 


- 4: Compute threshold _ηk_ from advantage statistics 

- 5: Assign binary improvement label 

- _It_ = **1** _{Aϕk_ ( _st, at_ : _t_ + _H−_ 1) _> ηk}_ 

- 6: Update actor to obtain _πθk_ +1 with advantage-conditioned policy extraction: max _θ_ E( _st,at_ : _t_ + _H−_ 1 _,It_ ) _∼Dkactor_ [log _πθ_ ( _at_ : _t_ + _H−_ 1 _|st, It_ )] 

- 7: Deploy _πθk_ +1 to collect new rollouts and human intervention trajectories 8: Update data buffer with robot experience _Dk_<sup>_actor_</sup> +1 9: Update data buffer with both robot and human experience _Dk_<sup>_critic_</sup> +1 

- 10: **end for** 

**Action chunk horizons.** At inference, and during critic training and advantage computation, we use a chunk horizon _H_ = 16. Specifically, the policy executes the first 16 steps of each predicted chunk before replanning; OVE bootstraps over 16-step segments when constructing TD targets; and advantage labels are assigned to ( _st, at_ : _t_ + _H−_ 1) pairs with _H_ = 16. We use a longer training chunk of 50 to improve temporal consistency during supervised learning, while the shorter operational horizon stabilizes value bootstrapping and makes advantage estimation more responsive to local progress changes during deployment and intervention data. 

**Model architecture.** We use a separate state-value critic and a VLA policy. The value model is initialized from the VLAC [40] checkpoint as its VLM backbone: we extract intermediate representations from transformer layer 23 (hidden dimension 2048) and regress a scalar value with a lightweight transformer value head. The policy is initialized from Qwen3-VL-4B-Instruct [41], consumes the final-layer backbone features (hidden dimension 2560), and outputs continuous action chunks with a flow-matching diffusion-transformer (DiT [42]) action decoder. For both models, we freeze the pretrained vision-language model and train only the value head and action head. 

**Critic training.** The critic is trained with TD bootstrapping and an expectile value loss with coefficient _τ_ = 0 _._ 7. Optimization uses 8000 steps on 8 GPUs with 140GB RAM, per-device batch size 64, and learning rate 1 _×_ 10<sup>_−_4</sup> for first iteration, and 1 _×_ 10<sup>_−_5</sup> for subsequent iterations. At iteration 0, the critic initializes from the pretrained value checkpoint; thereafter it initializes from the previous iteration’s critic. TD targets are normalized to [ _−_ 1 _,_ 0] before expectile regression. 

**Actor training.** The actor is fine-tuned with advantage conditioning for 8000 steps on 8 GPUs with 140GB RAM, per-device batch size 16, and learning rate 1 _×_ 10<sup>_−_4</sup> for first iteration, and 1 _×_ 10<sup>_−_5</sup> for subsequent iterations. At iteration 0, the actor starts from the pretrained VLA checkpoint; for _k >_ 0, it initializes from the policy checkpoint of iteration _k −_ 1. 

**Data buffers.** _Dk_<sup>_actor_</sup> stores robot experience used for policy learning: teleoperated demonstrations, autonomous rollouts, and human intervention trajectories. _Dk_<sup>_critic_</sup> extends this robot data with human experience videos for value learning. 

**State regularization.** State regularization is enabled only during training and disabled at evaluation. In the actor action head, full-state dropout is applied per sample with probability 0 _._ 3. Gaussian state noise is applied per sample with probability 0 _._ 4 and base standard deviation 0 _._ 01, with smaller scales 

16 

Table 2: Data scale used for iterative policy improvement. Counts report base-policy demonstration episodes and newly collected episodes at each iteration; intervention fraction denotes the fraction of episode time under human intervention, computed over rollout–intervention episodes. 

|Task|Demo episodes|Iter. 1|Iter.|2<br>Iter. 3|Intervention fraction|
|---|---|---|---|---|---|
|_Erase the whiteboard_|225|82|71|79|25.50%|
|_Put the bread into the toaster_|220|97|69|104|4.53%|


for head and waist state blocks and unit scale for arm, hand, and end-effector state blocks. In the data transform, perturbation adds Gaussian noise to configured state/action keys and clips the result to the original value range; dropout zeros the configured keys when sampled. These settings are applied to proprioceptive inputs rather than image tokens. 

**Data scale.** Table 2 summarizes episode growth across iterations and intervention-time fractions. The base policies are trained only on teleoperated demonstrations. For iterative training, each round adds newly collected robot experience from policy deployment and human intervention. For _Erase the whiteboard_ , interventions are typically triggered when the policy is about to fail in picking up the eraser, wipes in a direction that does not advance toward the handwriting, or leaves the whiteboard partially erased. For _Put the bread into the toaster_ , interventions mainly occur after the policy has made repeated insertion attempts 3 to 5 times but remains misaligned with the toaster slot. Since these autonomous alignment attempts can occupy a relatively long portion of the episode before takeover, the intervention fraction is lower than in _Erase the whiteboard_ . 

Beyond robot data, we additionally collect 180 ego-centric human experience videos per task using a head-mounted capture device, split evenly between successful and failed executions. These videos reproduce the behavior patterns observed in robot rollouts and interventions and further extend the coverage of partial-progress, near-failure, and recovery states, providing additional crossembodiment supervision for value learning. 

## **H Consecutive success examples** 

Fig. 9 and Fig. 10 visualize four consecutive successful trials from our policy on _Put the bread into the toaster_ and _Erase the whiteboard_ , respectively. 

17 


Figure 9: Four consecutive successful trials on _Put the bread into the toaster_ . Frames are arranged in a 7 _×_ 6 grid and read left to right, top to bottom, in temporal order. 

18 


Figure 10: Four consecutive successful trials on _Erase the whiteboard_ . Frames are arranged in a 7 _×_ 6 grid and read left to right, top to bottom, in temporal order. 

19 

