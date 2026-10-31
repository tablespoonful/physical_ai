---
title: "WoVR: World Models as Reliable Simulators for Post-Training VLA Policies with RL"
date: "2026-02-15"
authors: "Zhennan Jiang; Shangqing Zhou; Yutong Jiang; Zefang Huang; Mingjie Wei; Yuhui Chen"
venue: "CoRL 2026"
url: https://arxiv.org/abs/2602.13977
pdf: https://arxiv.org/pdf/2602.13977
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.13977)** / [論文ページ](https://arxiv.org/abs/2602.13977)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **WoVR: World Models as Reliable Simulators for Post-Training VLA Policies with RL** 

**Zhennan Jiang**<sup>2,3,4,*</sup> **Shangqing Zhou**<sup>2,3,*</sup> **Yutong Jiang**<sup>3</sup> **Zefang Huang**<sup>4</sup> **Mingjie Wei**<sup>4</sup> **Yuhui Chen**<sup>2,3</sup> **Tianxing Zhou**<sup>4</sup> **Zhen Guo**<sup>5</sup> **Hao Lin**<sup>5</sup> **Quanlu Zhang**<sup>5</sup> **Yu Wang**<sup>1</sup> **Haoran Li**<sup>2,3, †</sup> **Chao Yu**<sup>1, †</sup> **Dongbin Zhao**<sup>2,3,4</sup> 

> _∗_ Equal contribution 

> _†_ Corresponding authors 

1Tsinghua university 2University of Chinese Academy of Sciences 

3Institute of Automation, Chinese Academy of Sciences 4Zhongguancun Academy 5Infinigence AI https://huggingface.co/collections/RLinf/rlinf-wovr https://github.com/RLinf/RLinf 

**Abstract:** Reinforcement learning (RL) promises to unlock capabilities beyond imitation learning for Vision–Language–Action (VLA) models, but its requirement for massive real-world interaction prevents direct deployment on physical robots. Recent work attempts to use learned world models as simulators for policy optimization, yet closed-loop imagined rollouts inevitably suffer from hallucination and long-horizon error accumulation. Such errors not only degrade visual fidelity, but also mislead policy optimization by providing unreliable learning signals. We propose **WoVR** , a reliable world-model-based RL framework for posttraining VLA policies. Instead of assuming a faithful world model, WoVR explicitly regulates how RL interacts with imperfect imagined dynamics. It improves rollout stability through a controllable action-conditioned video world model, reshapes imagined interaction to reduce effective error depth via KeyframeInitialized Rollouts, and maintains policy–simulator alignment through World Model-Policy co-evolution. Extensive experiments demonstrate that WoVR enables stable long-horizon imagined rollouts and effective policy optimization, achieving superior LIBERO performance and consistent real-world gains across multiple robotic platforms. These results show that world models can serve as practical simulators for RL when hallucination is explicitly controlled. Additional visualization results are available at https://wovr-rlinf.github.io/. 

**Keywords:** World Model, Reinforcement Learning, Vision-Language-Action 

## **1 Introduction** 

Vision–Language–Action (VLA) models [1, 2, 3, 4] have been increasingly adopted for robotic manipulation, where actions are generated end-to-end by conditioning on language instructions and visual observations. Most existing VLA systems are trained via imitation learning. While effective in many downstream tasks, this paradigm fundamentally limits the performance ceiling of VLA policies, as it is tightly constrained by the quality and coverage of demonstration data. 

Recent VLA-RL methods [5, 6, 7, 8, 9, 10] improve beyond imitation learning [11]. However, applying RL to real-world VLA policies presents a fundamental dilemma: off-policy methods are generally more sample-efficient but often suffer from distribution shift and training instability, whereas on-policy updates [12, 13, 14] require massive parallel environment interaction for stable and efficient training, making them impractical for real robots due to costly data collection [15, 16]. Although simulation-based alternatives have been explored [7, 17], aligning simulators with real-world dynamics remains highly challenging. These constraints motivate replacing real-environment interaction with a learned world model that serves as a simulator for policy optimization. 


Figure 1: **Hallucination in Closed-Loop World Model Rollouts.** The world model imagines a successful grasp (green frames), but real-world execution fails (red frames).To address this critical mismatch, we propose three hallucination-aware mechanisms. 

This direction has become increasingly viable with the emergence of large-scale generative video models [18, 19]. Several works directly treat pretrained video generators as simulators and perform reinforcement learning entirely in imagination [20, 21]. **However, learned world models are not faithful simulators.** In this work, we define _hallucination_ as a systematic mismatch between imagined and real outcomes in closed-loop interaction. The world model may generate visually plausible yet physically incorrect rollouts, resulting in spurious success signals under the policy’s actions. In closed-loop autoregressive rollouts, prediction errors compound with horizon length due to: 

- Autoregressive feedback: the model conditions on its own generated frames, amplifying small early errors; 

- Distribution shift: as the policy evolves, its action distribution drifts away from the data used to train the world model, increasing out-of-distribution prediction failures. 

If hallucinated trajectories are directly used for policy optimization, RL is incentivized to exploit systematic model errors rather than true task progress. This leads to a critical question: 

_If world models inevitably hallucinate, how can RL remain reliable under imperfect imagined dynamics?_ 

We argue that using world models for RL is not primarily a modeling problem, but a reliability problem. To make world-model-based RL reliable, one must control hallucination at three interconnected levels: controllable simulator design, reliable interaction protocol, and policy–model alignment. To this end, we propose **WoVR** , a **Wo** rld-model-based framework for post-training **V** ision–Language– Action policies with **R** einforcement Learning. Rather than assuming the learned world model to be a faithful simulator, WoVR explicitly regulates how reinforcement learning interacts with imperfect imagined dynamics. We first strengthen the simulator itself by constructing a rollout-stable, action-controllable video world model with stabilized autoregressive context modeling, reducing long-horizon drift and structural collapse. To mitigate long-horizon prediction-error accumulation, we further introduce _Keyframe-Initialized Rollouts (KIR)_ , which start imagined rollouts from taskcritical states, shortening the effective prediction depth and reducing hallucination compounding. Finally, as policy optimization shifts the action distribution and induces distribution mismatch between the policy and the world model, we introduce _PACE_ , a policy-aligned co-evolution strategy that restores alignment by iteratively refining the world model under the evolving policy distribution, without requiring continuous online supervision. Together, these components form a unified hallucination-aware reinforcement learning framework that enables reliable policy optimization in imagination. In summary, our contributions are as follows. 

- We identify hallucination under closed-loop imagined interaction as a fundamental reliability challenge in world-model-based RL for VLA, showing that autoregressive error accumulation and policy-induced distribution shift can systematically corrupt optimization signals. 

- We propose WoVR, a hallucination-aware RL framework that jointly regulates controllable simulator design, reliable imagined interaction, and a policy-aligned co-evolution strategy, enabling stable on-policy optimization entirely in imagination. 

2 


Figure 2: **Overview of WoVR** . WoVR builds a reliability-driven reinforcement learning framework entirely around the learned world model. It first strengthens the world model as a controllable simulator, ensuring rollout-stable and action-responsive generation. On top of this simulator, it designs a reliable interaction protocol via Keyframe-Initialized Rollouts (KIR) to reduce effective error depth and prevent optimization on hallucinated success. Finally, it maintains policy–model alignment through PACE, which co-evolves the world model with the evolving policy to mitigate distribution shift and preserve simulator reliability. 

- WoVR achieves state-of-the-art world-model quality with strong perceptual and temporal consistency while maintaining high rollout efficiency at 23 FPS. More importantly, it consistently improves policy performance in both simulation and real-world deployment, boosting LIBERO success under different SFT initializations and improving success rates across multiple robotic platforms. 

## **2 Related Work** 

### **2.1 RL Fine-tuning for VLA Models** 

On-policy reinforcement learning [5, 12] has been increasingly adopted to fine-tune VLA models beyond imitation learning [5, 6]. However, directly transferring on-policy fine-tuning to real robots remains impractical, as such methods require large-scale parallel rollouts, repeated environment resets, and tightly coupled policy–environment interaction, which are difficult to support under realworld hardware. To mitigate this, some off-policy approaches [8, 22] introduce offline data reuse or human intervention, but often suffer from limited scalability and performance degradation during online updates. An alternative direction builds large-scale real-robot infrastructures, yet existing systems [23, 24] still cannot practically support fully on-policy algorithms at scale. These limitations suggest that the challenge of online RL for VLA is systemic rather than algorithmic, motivating world-model-based approaches that decouple policy optimization from real-world interaction. 

### **2.2 World Models for Policy Optimization** 

A growing body of work has begun to incorporate learned world models into VLA policy optimization [25, 26, 27]. One line of work uses world models primarily as reward or evaluation signals for post-training, where predicted future outcomes are used to construct preferences or guide policy improvement [28, 29, 30]. Another line improves VLA policies by generating synthetic rollouts with learned world models, reducing reliance on costly real-world interaction [31, 32, 33]. However, these works stop short of using world models as closed-loop RL simulators for policy optimization. 

3 

Prophet [34], World-Env [35] and WMPO [20] move in this direction by replacing real-environment interaction with imagined rollouts during reinforcement learning. Yet both largely treat the world model as a drop-in simulator, without explicitly addressing the central challenge of hallucinated dynamics: in closed-loop rollouts, prediction errors accumulate and can be exploited by the policy, ultimately misleading optimization. 

## **3 Methods** 

We propose WoVR, a reliability-driven world-model-based reinforcement learning framework for post-training VLA policies. As illustrated in Fig. 2, WoVR treats the world model as a generative simulator and controls hallucination across three levels: (1) Simulator-level control: we construct an action-controllable, rollout-stable video world model with dual-channel action injection and firstframe anchoring to suppress long-horizon drift. (2) Interaction-level reshaping: we redesign imagined interaction through Keyframe-Initialized Rollouts (KIR) to reduce effective error depth and prevent optimization on hallucinated success. (3) Alignment-level regulation: we introduce PACE, a policy–model co-evolution strategy that mitigates distribution shift by periodically aligning the world model with the evolving policy. 

### **3.1 Stabilized Action-Conditioned World Model** 

WoVR relies on a learned video world model as a generative simulator for closed-loop imagined interaction. However, long-horizon autoregressive generation can accumulate hallucinations, causing scene drift and appearance degradation. We therefore design the world model to be both _actioncontrollable_ and _rollout-stable_ , so that the simulated dynamics remain consistent under iterative, policy-driven generation. 


Figure 3: **Architecture of the proposed action-conditioned world model.** The world model is built upon a video diffusion backbone and conditioned on actions via a dual-channel action injection design, enabling frame-level controllability and stable chunk-by-chunk autoregressive generation for long-horizon imagined rollouts. 

Our world model is built on the Wan2.2-TI2V-5B video diffusion backbone [19] and reformulated as an action-conditioned generator. As shown in Fig. 3, actions are injected through two complementary pathways: they modulate denoising features through timestep-conditioned normalization and replace text embeddings in cross-attention to provide global action context. This _dual-channel design_ preserves the original DiT structure while enabling frame-level control. 

To stabilize closed-loop rollout, we additionally use a _first-frame–anchored_ context. At each autoregressive step, the model conditions on [ _o_ 0 _, ot−c_ : _t_ ], combining the initial frame with recent memory frames from the previous chunk. The fixed reference frame constrains global layout and appearance, while the memory frames preserve local dynamics, reducing drift and background collapse in long-horizon generation [36, 37, 38]. 

During training, we apply _noisy context augmentation_ : non-reference context frames are mildly noised, while the first-frame anchor remains clean. This makes the model robust to self-generated context at inference time and reduces brittle copying from previous predicted frames. 

4 

Together, dual-channel action conditioning, first-frame anchoring, and noisy context augmentation turn the video generator into a rollout-stable simulator for imagined RL. Given anchored context and policy actions, the model autoregressively predicts and appends video chunks, producing longhorizon trajectories entirely in imagination. More details are provided in Appendix B.1. 

When used as an RL simulator, the world model must also provide a reward signal. We support two modeling choices: a lightweight ResNet-based model for binary rewards, and a Qwen3-VL-based model for dense rewards. In practice, we find that the ResNet-based model is significantly more time-efficient while achieving comparable performance. Details are given in Appendix B.2. 

### **3.2 Hallucination-Aware Policy Optimization in Imagination** 

WoVR optimizes the VLA policy by interacting with the learned world model, which serves as a generative simulator for closed-loop imagined rollouts. The key difficulty is that, in long-horizon rollouts starting from the initial state, world-model errors accumulate early and can eventually produce visually plausible but physically incorrect transitions and even spurious success signals. If reinforcement learning naively trusts such rollouts, the policy is encouraged to optimize toward hallucinated outcomes rather than real task progress. 

To reduce the effective error depth of imagined interaction, we introduce Keyframe-Initialized Rollouts (KIR). As illustrated in Figure 4, instead of always initializing rollouts from the episode start _o_ 0, we initialize a portion of rollouts from keyframes _ok_ that lie near task-critical intermediate states, especially failure states encountered by the current policy. The motivation is that many decisive contacts and corrections happen locally around these states, whereas starting from _o_ 0 forces the world model to predict a long prefix before reaching them, during which compounding errors can already derail the rollout. 

We adopt GRPO to update the policy using imagined rollouts. The GRPO objective is defined as: 


Figure 4: **Illustration of Keyframe-Initialized Rollouts (KIR).** Long-horizon rollouts accumulate prediction errors in early stages, leading to hallucinated success that contradicts the ground-truth failure. In contrast, KIR initialize rollouts near critical states, enabling physically consistent predictions that correctly model failure. 


where _G_ is the number of imagined trajectories, _A_<sup>ˆ(</sup><sup>_i_)</sup> is the group-relative advantage. and _Ti_<sup>valid</sup> is the number of valid timesteps up to the first success. This objective also complements KIR: keyframe-initialized rollouts tend to reach task resolution with fewer valid steps, and trajectorylength normalization increases their per-timestep contribution, so gradients are dominated by short, task-critical segments rather than long, drift-prone continuations. 

### **3.3 PACE: Policy–Aligned Co-Evolution** 

While policy optimization proceeds entirely within the learned world model, the policy’s action distribution continuously evolves and drifts away from the data used to train the initial world model. This inherent distribution shift leads to accumulating mismatch between the simulator and the improving policy, ultimately degrading the reliability of imagined rollouts. 

5 

To address this issue, we introduce **PACE** , a World Model–Policy co-evolution strategy. Instead of treating the world model as a fixed, static simulator throughout policy optimization, PACE allows the world model and VLA policy to evolve together throughout training. 

Concretely, we realize this co-evolution through low-frequency, policy-driven refinement: we first train an initial world model, denoted as WMBase, using trajectories collected from the base VLA policy. After the first stage of policy optimization within WMBase, we collect a limited set of additional rollouts under the evolved policy and use them to further refine the world model. The refined model is referred to as WMEvo. Importantly, this refinement is performed at very low frequency, distinguishing _PACE_ from classical model-based reinforcement learning methods, which continuously update the dynamics model at high frequency during policy optimization. This low-frequency refinement provides two key advantages. First, unlike real-world online RL, it does not require continuous human supervision or environment resets during policy training, significantly reducing operational overhead. Second, by aligning the world model with the evolving policy distribution, _PACE_ mitigates compounding model errors and maintains simulator reliability without sacrificing training stability. 

## **4 Experiments** 

We conduct extensive experiments to evaluate the effectiveness of WoVR as a world-model-based reinforcement learning framework for post-training VLA policies. Our experimental design aims to systematically answer the following three questions: 

- **Q1:** Is the proposed world model stable, controllable, and efficient enough to serve as a simulator for closed-loop reinforcement learning? 

- **Q2:** Can WoVR effectively improve VLA task performance compared to existing world-modelbased reinforcement learning methods? 

- **Q3:** Do the policies optimized with WoVR reliably transfer to real-world manipulation tasks? 

To answer these questions, we evaluate both the quality of the learned world model and the downstream policy performance. For world model evaluation, we focus on long-horizon, actionconditioned video generation under closed-loop, chunk-by-chunk autoregressive inference. We adopt standard perceptual and distributional metrics, including **LPIPS** [39], **FID** [40], **FVD** [41] and **FloLPIPS** [42] (Detailed calculations are provided in the Appendix C.). We also report inference throughput ( **FPS** ) to quantify generation efficiency. For policy evaluation, we use task success rate ( **SR** ) as the primary metric. 

We compare WoVR against several representative baselines spanning both _world model quality_ and _policy optimization_ . For world model quality, we include EVAC [26], Cosmos-Predict2 [43] and OpenSora [44](the world-model backbone adopted in WMPO [20]). All compared models are evaluated under the same chunk-wise autoregressive generation protocol to ensure a fair comparison. For policy optimization, we consider OpenVLA-OFT [1], a base VLA policy trained purely with imitation learning; GRPO (Online) [14], trained with real-environment interaction under the same rollout budget; and WMPO [20], which performs reinforcement learning using OpenSora. 

### **4.1 Is the World Model Stable, Controllable, and Efficient?** 

**Experimental Setup.** We conduct all world model evaluations in the LIBERO environment [45]. A total of 3,000 VLA rollout trajectories, each with a length of 512 frames, are collected to train the world models. In addition, 200 held-out trajectories of the same length are used exclusively for evaluation. We compare WoVR against three representative action-conditioned world models: EVAC, Cosmos-Predict2, and OpenSora as adopted in WMPO. 

**Quantitative Results.** Table 1 shows that WoVR outperforms all baselines across all metrics, indicating higher visual fidelity, stronger temporal consistency, and more accurate dynamics. These 

6 

Table 1: **Comparison of different world models.** Rollout denotes the rollout horizon length. 

|**Method**|**Rollout**|**FPS**_↑_|**LPIPS**_↓_[39]|**FID**_↓_[40]|**FVD**_↓_[41]|**FloLPIPS**_↓_[42]|
|---|---|---|---|---|---|---|
||512||0_._146|46_._528|345_._818|0_._205|
|EVAC [26]|256|1.35|0_._130|49_._153|354_._983|0_._192|
||128||0_._106|44_._337|423_._132|0_._166|
|C|512||0_._315|165_._862|275_._737|0_._265|
|osmos-<br>Predict2 [43]|256|3.50|0_._226|106_._324|203_._853|0_._306|
||128||0_._164|77_._555|304_._456|0_._281|
||512||0_._105|38_._478|89_._391|0_._156|
|OpenSora [20]|256|7.00|0_._082|33_._577|94_._998|0_._122|
||128||0_._069|33_._413|111_._643|0_._113|
||512||**0.091**|**34.252**|**68.011**|**0.154**|
|WoVR (Ours)|256|**23.0**|**0.063**|**24.378**|**50.041**|**0.102**|
||128||**0.047**|**18.553**|**39.047**|**0.079**|


Table 2: **Task success rates (%) across LIBERO suites.** 

|**Method**|**Spatial**|**Object**|**Goal**|**Long**|**Avg**|
|---|---|---|---|---|---|
||**One-**|**Trajectory SFT**||||
|OpenVLA-OFT [1]|63.6|36.4|48.2|13.8|40.5|
|w/ GRPO (online) [14]|66.6|45.2|52.2|14.6|44.6|
|w/ WMPO [20]|67.8|65.4|56.6|13.8|50.9|
|w/**Ours**|**84.2**|**80.8**|**77.4**|**35.8**|**69.5**|
|∆|+20.6|+44.4|+29.2|+22.0|+29.0|
||**Full-**|**Trajectory SFT**||||
|OpenVLA-OFT [1]|93.6|83.0|90.0|85.6|88.1|
|w/ GRPO (online) [14]|94.6|86.2|92.2|85.8|89.7|
|w/ WMPO [20]|95.0|94.8|92.8|87.0|92.4|
|w/**Ours**|**98.8**|**98.8**|**94.8**|**91.4**|**96.0**|
|∆|+5.2|+15.8|+4.8|+5.8|+7.9|


improvements become more pronounced as the rollout horizon increases, suggesting that WoVR is more robust in long-horizon autoregressive generation. 

Despite adopting a larger backbone (Wan, _∼_ 5B) than OpenSora ( _∼_ 1.3B), WoVR achieves higher inference throughput by requiring only five diffusion steps and leveraging a 3D VAE for spatiotemporal latent encoding, whereas OpenSora typically relies on more sampling steps and a 2D VAE. 

### **4.2 Can WoVR Effectively Improve VLA Task Performance?** 

**Experimental Setup.** We conduct policy optimization experiments on LIBERO Spatial, Object, Goal, and Long suites [45], each containing 10 tasks. Following SimpleVLA-RL [17], we initialize from OpenVLA-OFT and consider two supervised fine-tuning settings: _one-trajectory SFT_ and _fulltrajectory SFT_ . 

For a fair comparison, all methods use the same budget of 2,500 real-environment trajectories per suite. **GRPO** directly uses them for online policy optimization, while **WMPO** uses them to train a world model and then performs RL entirely in imagination. **WoVR** follows the two-stage policy– simulator co-evolution protocol in Sec. 3.3: it first trains an initial world model with 1,500 trajectories collected by the base policy, optimizes the policy in imagination, and then refines the world model with 1,000 additional trajectories collected by the evolved policy. 

**Quantitative Results.** Table 2 reports **SR** across LIBERO suites under two SFT initializations. Under the _one-trajectory SFT_ setting, GRPO yields only a marginal improvement (4.1 % _↑_ ), indicating 

7 

Table 3: **Real-world success rates (%, 30 trials/task).** 

|**Method**|**Fr**|**anka Em**|**ika Panda**|||**Agile**|**X Piper**||
|---|---|---|---|---|---|---|---|---|
||Pick<br>Banana|Pick<br>Bread|Open<br>Drawer|**Avg**|Fold<br>Towel|Pick<br>Cube|Pick<br>Tomato|**Avg**|
|OpenVLA-OFT [1]|36.7|70.0|46.7|51.1|10.0|23.3|13.3|15.5|
|w/ WMPO [20]|56.7|76.7|60.0|64.5|10.0|26.7|20.0|18.9|
|w/**Ours**|**86.7**|**90.0**|**63.3**|**80.0**|**20.0**|**33.3**|**33.3**|**28.9**|
|∆|+50.0|+20.0|+16.6|+28.9|+10.0|+10.0|+20.0|+13.4|


that limited real-environment interaction is insufficient for effective online RL. WMPO improves the average success rate to 50.9%, but shows no gain on LIBERO-Long (0 % _↑_ ), suggesting that a less reliable world model cannot support long-horizon policy optimization. In contrast, WoVR achieves the best performance across all suites, increasing the average success rate to 69.5%, with especially large gains on Object and Long. Under the stronger _full-trajectory SFT_ setting, where the base policy is already strong (88.1%), all methods have less room for improvement: GRPO reaches 89.7% and WMPO reaches 92.4%, while WoVR still achieves the highest average success rate of 95.9% and consistently outperforms WMPO. 

These results show that world-model-based RL can outperform limited-budget online RL, especially when the simulator is sufficiently stable and policy-aligned. Additional ablations on _PACE_ and _KIR_ are provided in Appendix D.2. 

### **4.3 Do Policies Optimized with WoVR Reliably Transfer to the Real World?** 


**Experimental Setup** We conduct real-world transfer experiments on two robotic platforms with different control characteristics: the **Franka Emika Panda** and the **AgileX Piper** . As shown in Fig 5, we evaluate three manipulation tasks on each platform. Detailed task requirements are provided in Appendix F.2. 


For each platform, we train a _multi-task_ VLA policy and a corresponding world model over the three tasks. After training with WoVR, we Figure directly deploy the optimized policies on the **robotic** physical robots and evaluate their **SR** in real world, where each task is evaluated over 30 independent trials. More details can be seen in Appendix F. 

(d) Pick cube (e) Pick tomato (f) Fold towel 

Figure 5: **Real-world experiments on two robotic platforms.** Top row: Franka Emika Panda; bottom row: AgileX Piper. 

**Quantitative Results.** Table 3 reports real-world success rates on two robotic platforms. WMPO improves over the base policy, especially on Franka (+13.4 points), indicating that world-modelbased policy optimization can provide useful learning signals. However, its gains are limited on the noisier AgileX Piper platform (+3.4 points), suggesting that na¨ıve imagined RL remains vulnerable to world-model hallucination. In contrast, WoVR consistently achieves the best performance, improving the base policy by +28.9 points on Franka and +13.4 points on AgileX Piper. These results show that WoVR enables more stable and effective policy optimization in imagination, with strong transfer to both high-precision and noisier real-world robotic systems, without additional online interaction. 

**Generalization to Different VLA Backbones.** To further evaluate the generality of WoVR, we conduct additional experiments using _π_ 0 _._ 5 as the VLA backbone on the AgileX Piper platform. We follow _π_ RL [7] and optimize the policy with Flow-SDE under the unchanged WoVR framework. 

8 

Table 4: **Real-world success rates (%, 30 trials/task) on AgileX Piper using** _π_ 0 _._ 5 **as the VLA backbone.** 

|**Method**|**Fold Towel**|**Pick Cube**|**Pick Tomato**|**Avg**|
|---|---|---|---|---|
|_π_0_._5-base|20.0|60.0|23.3|34.4|
|w/**Ours**|**30.0**|**86.7**|**53.3**|**56.7**|
|∆|+10.0|+26.7|+30.0|+22.3|


As shown in Table 4, WoVR consistently improves the _π_ 0 _._ 5 policy across all evaluated tasks, raising the average success rate by +22.3 points. The post-trained policy achieves high success rates on pick-and-place tasks. Although Fold Towel is a more challenging deformable-object task, WoVR still brings a +10.0 point gain. These results demonstrate that the benefit of WoVR is not tied to a specific VLA architecture. 

## **5 Conclusion** 

In this work, we first identify hallucination in closed-loop imagined interaction as a central reliability bottleneck in world-model-based RL for VLA policy optimization. To address this, we propose WoVR, a hallucination-aware framework that improves simulator stability with an action-controllable video world model, reduces effective prediction depth through KIR, and maintains policy–simulator alignment via PACE. Experiments on LIBERO and real-world manipulation tasks show that WoVR enables effective policy optimization. Together, these results suggest that hallucination-controlled world models can serve as practical RL simulators, enabling a closed-loop path where online deployment data continually refine the simulator and further improve VLA policies in imagination. 

## **6 Limitations** 

WoVR identifies hallucination in closed-loop imagined rollouts as a key reliability bottleneck for world-model-based RL, but our analysis remains primarily empirical. In particular, we do not provide a formal characterization of how hallucination propagates into policy optimization, nor a regret bound for the policy learned in the imagined world model relative to the optimal policy in the real environment. In addition, while WoVR demonstrates promising results on real-world tabletop manipulation tasks, its capability in substantially longer-horizon tasks and mobile manipulation remains underexplored. These settings may amplify error accumulation through extended interaction horizons, changing viewpoints, larger state spaces, and more diverse contact dynamics. Scaling WoVR to such scenarios may require large-scale world-model pretraining on more diverse embodied data, as well as more sophisticated mechanisms for suppressing compounding errors. 

9 

## **References** 

- [1] M. J. Kim, C. Finn, and P. Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- [2] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [3] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, M. Y. Galliker, D. Ghosh, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- [4] H. Li, Y. Chen, W. Cui, W. Liu, K. Liu, M. Zhou, Z. Zhang, and D. Zhao. Survey of visionlanguage-action models for embodied manipulation. _arXiv preprint arXiv:2508.15201_ , 2025. 

- [5] H. Zang, M. Wei, S. Xu, Y. Wu, Z. Guo, Y. Wang, H. Lin, L. Shi, Y. Xie, Z. Xu, Z. Liu, K. Chen, W. Tang, Q. Zhang, W. Zhang, C. Yu, and Y. Wang. Rlinf-vla: A unified and efficient framework for vla+rl training, 2025. 

- [6] J. Liu, F. Gao, B. Wei, X. Chen, Q. Liao, Y. Wu, C. Yu, and Y. Wang. What can rl bring to vla generalization? an empirical study. _arXiv preprint arXiv:2505.19789_ , 2026. 

- [7] K. Chen, Z. Liu, T. Zhang, Z. Guo, S. Xu, H. Lin, H. Zang, X. Li, Q. Zhang, Z. Yu, G. Fan, T. Huang, Y. Wang, and C. Yu. _π_ `RL` : Online rl fine-tuning for flow-based vision-language-action models, 2026. 

- [8] Y. Chen, S. Tian, S. Liu, Y. Zhou, H. Li, and D. Zhao. Conrft: A reinforced fine-tuning method for vla models via consistency policy. In _Proceedings of Robotics: Science and Systems, RSS 2025, Los Angeles, CA, USA, Jun 21-25, 2025_ , 2025. doi:10.15607/RSS.2025.XXI.019. 

- [9] G. Lu, W. Guo, C. Zhang, Y. Zhou, H. Jiang, Z. Gao, Y. Tang, and Z. Wang. Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning. _arXiv preprint arXiv:2505.18719_ , 2025. 

- [10] Y. Li, X. Ma, J. Xu, Y. Cui, Z. Cui, Z. Han, L. Huang, T. Kong, Y. Liu, H. Niu, W. Peng, J. Qiao, Z. Ren, H. Shi, Z. Su, J. Tian, Y. Xiao, S. Zhang, L. Zheng, H. Li, and Y. Wu. Gr-rl: Going dexterous and precise for long-horizon robotic manipulation. _arXiv preprint arXiv:2512.01801_ , 2025. 

- [11] K. Lei, H. Li, D. Yu, Z. Wei, L. Guo, Z. Jiang, Z. Wang, S. Liang, and H. Xu. Rl100: Performant robotic manipulation with real-world reinforcement learning. _arXiv preprint arXiv:2510.14830_ , 2025. 

- [12] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [13] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. K. Li, Y. Wu, and D. Guo. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 

- [14] D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_ , 2025. 

- [15] W. Cui, C. Zhao, S. Wei, J. Zhang, H. Geng, Y. Chen, and H. Wang. Gapartmanip: a large-scale dataset for generalizable and actionable part manipulation with material-agnostic articulated objects. In _IEEE International Conference on Robotics and Automation_ . IEEE, 2025. 

10 

- [16] J. Luo, C. Xu, J. Wu, and S. Levine. Precise and dexterous robotic manipulation via humanin-the-loop reinforcement learning. _Science Robotics_ , 10(105):eads5033, 2025. 

- [17] H. Li, Y. Zuo, J. Yu, Y. Zhang, Z. Yang, K. Zhang, X. Zhu, Y. Zhang, T. Chen, G. Cui, et al. Simplevla-rl: Scaling vla training via reinforcement learning. _arXiv preprint arXiv:2509.09674_ , 2025. 

- [18] Z. Zheng, X. Peng, T. Yang, C. Shen, S. Li, H. Liu, Y. Zhou, T. Li, and Y. You. Open-sora: Democratizing efficient video production for all. _arXiv preprint arXiv:2412.20404_ , 2024. 

- [19] T. Wan, A. Wang, B. Ai, B. Wen, C. Mao, C.-W. Xie, D. Chen, F. Yu, H. Zhao, J. Yang, et al. Wan: Open and advanced large-scale video generative models. _arXiv preprint arXiv:2503.20314_ , 2025. 

- [20] F. Zhu, Z. Yan, Z. Hong, Q. Shou, X. Ma, and S. Guo. Wmpo: World model-based policy optimization for vision-language-action models. _arXiv preprint arXiv:2511.09515_ , 2025. 

- [21] H. Li, P. Ding, R. Suo, Y. Wang, Z. Ge, D. Zang, K. Yu, M. Sun, H. Zhang, D. Wang, and W. Su. Vla-rft: Vision-language-action reinforcement fine-tuning with verified rewards in world simulators. _arXiv preprint arXiv:2510.00406_ , 2025. 

- [22] X. Yuan, T. Mu, S. Tao, Y. Fang, M. Zhang, and H. Su. Policy decorator: Model-agnostic online refinement for large policy model. _arXiv preprint arXiv:2412.13630_ , 2024. 

- [23] M. Pan, S. Feng, Q. Zhang, X. Li, J. Song, C. Qu, Y. Wang, C. Li, Z. Xiong, Z. Chen, Y. Liu, and J. Luo. Sop: A scalable online post-training system for vision-language-action models. _arXiv preprint arXiv:2601.03044_ , 2026. 

- [24] H. Zang, S. Yu, H. Lin, T. Zhou, Z. Huang, Z. Guo, X. Xu, J. Zhou, Y. Sheng, S. Zhang, F. Gao, W. Tang, Y. Yue, Q. Zhang, X. Chen, C. Yu, and Y. Wang. Rlinf-user: A unified and extensible system for real-world online policy learning in embodied ai, 2026. 

- [25] J. Quevedo, A. K. Sharma, Y. Sun, V. Suryavanshi, P. Liang, and S. Yang. Worldgym: World model as an environment for policy evaluation. _arXiv preprint arXiv:2506.00613_ , 2025. 

- [26] Y. Jiang, S. Chen, S. Huang, L. Chen, P. Zhou, Y. Liao, X. He, C. Liu, H. Li, M. Yao, and G. Ren. Enerverse-ac: Envisioning embodied environments with action condition. _arXiv preprint arXiv:2505.09723_ , 2025. 

- [27] Z. Jiang, K. Liu, Y. Qin, S. Tian, Y. Zheng, M. Zhou, C. Yu, H. Li, and D. Zhao. World4rl: Diffusion world models for policy refinement with reinforcement learning for robotic manipulation. _arXiv preprint arXiv:2509.19080_ , 2025. 

- [28] S. Fei, S. Wang, L. Ji, A. Li, S. Zhang, L. Liu, J. Hou, J. Gong, X. Zhao, and X. Qiu. Srpo: Self-referential policy optimization for vision-language-action models. _arXiv preprint arXiv:2511.15605_ , 2025. 

- [29] C.-Y. Hung, N. Majumder, H. Deng, L. Renhang, Y. Ang, A. Zadeh, C. Li, D. Herremans, Z. Wang, and S. Poria. Nora-1.5: A vision-language-action model trained using world modeland action-based preference rewards, 2025. 

- [30] X. Sun, Z. Xu, C. Cao, Z. Liu, Y. Sun, J. Pang, R. Zhang, Z. Yang, K. Pang, D. He, M. Yuan, and J. Chen. Atomvla: Scalable post-training for robotic manipulation via predictive latent world models, 2026. 

- [31] Y. Guo, L. X. Shi, J. Chen, and C. Finn. Ctrl-world: A controllable generative world model for robot manipulation. _arXiv preprint arXiv:2510.10125_ , 2025. 

11 

- [32] J. Yang, K. Lin, J. Li, W. Zhang, T. Lin, L. Wu, Z. Su, H. Zhao, Y.-Q. Zhang, L. Chen, P. Luo, X. Yue, and H. Li. Rise: Self-improving robot policy with compositional world model. _arXiv preprint arXiv:2602.11075_ , 2026. 

- [33] Y. Guo, T. Lee, L. X. Shi, J. Chen, P. Liang, and C. Finn. Vlaw: Iterative co-improvement of vision-language-action policy and world model. _arXiv preprint arXiv:2602.12063_ , 2026. 

- [34] J. Zhang, Z. Huang, C. Gu, Z. Ma, and L. Zhang. Reinforcing action policies by prophesying, 2025. 

- [35] J. Xiao, Y. Yang, X. Chang, R. Chen, F. Xiong, M. Xu, W.-S. Zheng, and Q. Zhang. Worldenv: Leveraging world model as a virtual environment for vla post-training. _arXiv preprint arXiv:2509.24948_ , 2025. 

- [36] J. Shin, Z. Li, R. Zhang, J.-Y. Zhu, J. Park, E. Shechtman, and X. Huang. Motionstream: Real-time video generation with interactive motion controls. _arXiv preprint arXiv:2511.01266_ , 2025. 

- [37] S. Yang, W. Huang, R. Chu, Y. Xiao, Y. Zhao, X. Wang, M. Li, E. Xie, Y. Chen, Y. Lu, S. Han, and Y. Chen. Longlive: Real-time interactive long video generation. _arXiv preprint arXiv:2509.22622_ , 2025. 

- [38] J. Tang, J. Liu, J. Li, L. Wu, H. Yang, P. Zhao, S. Gong, X. Yuan, S. Shao, and Q. Lu. Hunyuan-gamecraft-2: Instruction-following interactive game world model. _arXiv preprint arXiv:2511.23429_ , 2025. 

- [39] R. Zhang, P. Isola, A. A. Efros, E. Shechtman, and O. Wang. The unreasonable effectiveness of deep features as a perceptual metric. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 586–595, 2018. 

- [40] M. Heusel, H. Ramsauer, T. Unterthiner, B. Nessler, and S. Hochreiter. Gans trained by a two time-scale update rule converge to a local nash equilibrium. _Advances in neural information processing systems_ , 30, 2017. 

- [41] T. Unterthiner, S. Van Steenkiste, K. Kurach, R. Marinier, M. Michalski, and S. Gelly. Towards accurate generative models of video: A new metric & challenges. _arXiv preprint arXiv:1812.01717_ , 2018. 

- [42] D. Danier, F. Zhang, and D. Bull. Flolpips: A bespoke video quality metric for frame interpoation. _arXiv preprint arXiv:2207.08119_ , 2022. 

- [43] J. Pennington, P. Joshi, and A. Bhide. Develop custom physical ai foundation models with nvidia cosmos predict-2. `https://developer.nvidia.com/blog/ develop-custom-physical-ai-foundation-models-with-nvidia-cosmos-predict-2/` , June 11 2025. NVIDIA Developer Blog. 

- [44] X. Peng, Z. Zheng, C. Shen, T. Young, X. Guo, B. Wang, H. Xu, H. Liu, M. Jiang, W. Li, et al. Open-sora 2.0: Training a commercial-level video generation model in 200 _k_ . _arXiv preprint arXiv:2503.09642_ , 2025. 

- [45] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _arXiv preprint arXiv:2306.03310_ , 2023. 

- [46] P. Esser, S. Kulal, A. Blattmann, R. Entezari, J. M¨uller, H. Saini, Y. Levi, D. Lorenz, A. Sauer, F. Boesel, D. Podell, T. Dockhorn, Z. English, K. Lacey, A. Goodwin, Y. Marek, and R. Rombach. Scaling rectified flow transformers for high-resolution image synthesis. _arXiv preprint arXiv:2403.03206_ , 2024. 

- [47] B. Chen, D. M. Monso, Y. Du, M. Simchowitz, R. Tedrake, and V. Sitzmann. Diffusion forcing: Next-token prediction meets full-sequence diffusion. _arXiv preprint arXiv:2407.01392_ , 2024. 

12 

- [48] S. Bai, Y. Cai, R. Chen, et al. Qwen3-vl technical report. _arXiv preprint arXiv:2511.21631_ , 2025. 

- [49] J. Zheng, J. Li, Z. Wang, D. Liu, X. Kang, Y. Feng, Y. Zheng, J. Zou, Y. Chen, J. Zeng, Y.-Q. Zhang, J. Pang, J. Liu, T. Wang, and X. Zhan. X-vla: Soft-prompted transformer as scalable cross-embodiment vision-language-action model. _arXiv preprint arXiv:2510.10274_ , 2025. 

- [50] Y. Zhou, C. Barnes, J. Lu, J. Yang, and H. Li. On the continuity of rotation representations in neural networks. _arXiv preprint arXiv:1812.07035_ , 2020. 

13 

## **Appendix Contents** 

|**A**|**GPU**|**Allocation Strategy**. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .15|
|---|---|---|
|**B**|**Impl**|**emental Details**. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .15|
||B.1|Implemental Details of world model. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .15|
||B.2|Implemental Details of Reward Model. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .16|
|||B.2.1<br>Sparse Reward Model. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .16|
|||B.2.2<br>Dense Reward Modeling. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .16|
||B.3|Implemental Details of KIR. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .17|
|**C**|**Eval**|**uation Metrics**. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .17|
|**D**|**Abla**|**tion Study**. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .18|
||D.1|Ablation on World Model Mechanisms. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .18|
||D.2|Ablation on PACE and KIR. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .19|
||D.3|Ablation on Reward Modeling. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .21|
|**E**|**Qual**|**itative Failure Mode Analysis**. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .22|
|**F**|**Real-**|**World Experiments**. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .23|
||F.1|Hardware Setup. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .23|
||F.2|Detailed Task Requirements. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .23|
||F.3|Practical Considerations for Real-World Deployment. . . . . . . . . . . . . . . . . . . . . . . . . . . . .23|
||F.4|Task Setting. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .25|


14 

## **A GPU Allocation Strategy** 

The reinforcement-learning pipeline can be decomposed into three components: _Generation_ , _Simulator_ , and _Training_ . In WoVR, the _Simulator_ is instantiated by the learned _world model_ , which generates the next observation given the current observation and action. In the rollout phase, _Generation_ performs policy inference to produce an (optionally chunked) action from the current observation, while the _Simulator_ executes the action and returns the next observation; this closed-loop interaction repeats until a batch of trajectories is collected. In the optimization phase, _Training_ updates the VLA policy using the collected trajectories, after which the system alternates back to rollout for the next iteration. 

Following the system abstraction in RLinf-VLA, WoVR adopts a collocated (shared) GPU allocation strategy, where the three RL pipeline components co-exist on the same set of GPUs, with the _Simulator_ implemented as the world-model rollout module. Unlike physical simulators that require dedicated device-side state, WoVR’s simulator is a neural network; thus, offload/onload can be naturally realized by swapping only the _model parameters_ between GPU and host memory, without migrating any external simulator state. In its original form, collocated execution relied on frequent GPU _↔_ CPU offload/onload to keep only one component resident on GPUs at a time; however, in embodied settings the simulator and generator must interact iteratively, making per-interaction offload/onload prohibitively expensive. Therefore, we use the modified collocated strategy: offload/onload for Generation and Simulator happens only at the beginning and end of the rollout phase, avoiding repeated transfers during closed-loop imagined interaction, as illustrated in Fig. 6. 


Figure 6: Collocated GPU Allocation Strategy 

## **B Implemental Details** 

### **B.1 Implemental Details of world model** 

The world model generates imagined trajectories chunk by chunk in the latent space of the video diffusion backbone. At rollout step _t_ , the anchored visual context is formed by concatenating the episode’s initial frame and the latest generated memory frames, i.e., [ _o_ 0 _, ot−c_ : _t_ ]. After VAE encoding, the corresponding latent context [ _z_ 0 _, zt′−c′_ : _t′_ ] is concatenated with Gaussian noise latents for the next chunk. The action-conditioned DiT blocks then denoise these latents under the dual-channel action conditioning shown in Fig. 3, and the decoded future frames are appended to the rollout context. Repeating this procedure yields long-horizon closed-loop imagined trajectories under policy actions. 

We train the model with the Rectified Flow objective [46]. Let _x_ 1 = _zt′_ +1: _t′_ + _H ′_ denote the target future latents and _x_ 0 _∼N_ (0 _,_ **I** ) denote Gaussian noise. Given an interpolation time _τ ∈_ [0 _,_ 1], the linearly interpolated state is constructed as: 


15 

The corresponding target velocity field along this interpolation trajectory is: 


the model _u_ ( _·_ ; _ϕ_ ) predicts the velocity _vττ_ from the intermediate latent _xττ_ : 

where _c_ includes the anchored visual context and the action sequence. 

To improve robustness under closed-loop inference, we inject diffusion noise into the non-reference context latents during training. 


where _τctx_ is a value close to 1 and _ϵ_ denotes noise. The initial reference frame remains clean, while recent memory latents are mildly corrupted before being used as context. This augmentation reduces the train–inference gap caused by conditioning on self-generated frames and mitigates brittle context copying during long-horizon autoregressive rollout [47, 31]. 

### **B.2 Implemental Details of Reward Model** 

#### **B.2.1 Sparse Reward Model** 

For sparse supervision, we use a learned reward classifier that predicts task success from the predicted next observation. Concretely, given the generated observation ˜ _ot_ +1 from the world model, the sparse reward model _Rψ_<sup>spestimates the probability of task success, and the binary reward is defined</sup> as 


where I( _·_ ) denotes the indicator function. Following HiL-SERL [16], the sparse reward classifier is implemented as a lightweight network and trained with binary cross-entropy loss on labeled success states, defined as 


#### **B.2.2 Dense Reward Modeling** 

To provide finer-grained learning signals beyond binary success, we further introduce a dense reward model built on top of Qwen3-VL [48]. Instead of directly regressing a scalar reward, we formulate dense reward prediction as an ordinal visual progress estimation problem. Given four consecutive observations _o_ ˜ _t−_ 2: _t_ +1 = [˜ _ot−_ 2 _,_ ˜ _ot−_ 1 _,_ ˜ _ot,_ ˜ _ot_ +1] and the task description _l_ , the dense reward model _Rψ_<sup>depredicts a discrete progress level</sup> 


where 0 denotes no progress and 10 denotes task completion. The dense reward is then obtained by normalization: 


The model takes as input four consecutive RGB frames together with the task text, and outputs logits over 11 reward levels. Architecturally, we adopt a Qwen3-VL backbone with LoRA adaptation and attach a lightweight MLP reward head for classification. During training, labels are constructed automatically from trajectory rewards: failed trajectories are assigned level 0, successful states are assigned level 10, and pre-success states are linearly mapped to intermediate levels 1–9 according to their temporal proximity to the first successful state. To mitigate class imbalance, we further rebalance samples across reward levels during dataset construction. 

The dense reward model is trained with a standard cross-entropy objective: 


16 

### **B.3 Implemental Details of KIR** 

Keyframe-Initialized Rollouts (KIR) are implemented as a change to the initial context fed into the world model, rather than as a change to the model architecture. The Wan encoder used by our world model is a causal 3D VAE whose temporal input length follows the form 1 + 4 _m_ . In our rollout implementation, we use five frames (m=1) in total: one persistent reference frame plus four temporal context frames. 

For standard long-horizon rollout from the episode start, the first frame is repeated to construct a valid VAE input: 


and the first generated chunk is 


where _Wϕ_ denotes the action-conditioned world model. Equivalently, when comparing against a KIR rollout at a task-specific horizon, the non-KIR context can be written as 


which removes the local pre-failure context and relies only on the initial observation. This initialization forces the world model to imagine the entire prefix before reaching task-critical states, which increases the effective depth of error accumulation. 

KIR instead initializes imagined rollouts near a task-critical state. Ideally, for a trajectory that is about to fail around time _T_ KIR + 1, we would use the first frame together with the last four frames before the failure transition: 


and generate the first imagined chunk from this keyframe context: 


The first frame _o_ 0 remains the global anchor, while _oT_ KIR _−_ 3: _T_ KIR provides the local pre-failure context. 

In practice, we avoid manually cherry-picking keyframes for every trajectory. For each task, we set a task-level keyframe index _T_ KIR based on when the base policy typically approaches a critical failure region. This fixed task-level choice keeps KIR inexpensive and reproducible while still placing the first imagined chunk near the decisive part of the task. After the first KIR chunk is generated, subsequent chunks follow the same autoregressive procedure as the standard world-model rollout, using the first frame anchor and the latest generated memory frames as context. 

## **C Evaluation Metrics** 

We adopt LPIPS [39], FID [40], FVD [41], FloLPIPS [42], and FPS as evaluation metrics for generated videos. Specifically: 

- **LPIPS** (Learned Perceptual Image Patch Similarity) measures frame-level perceptual similarity using deep visual features; 


where _x_ and _x_ 0 denote the generated and real frames, _F_<sup>ˆ</sup> _h,w_<sup>_l_(</sup><sup>_·_)denotesthenormalizeddeep</sup> feature at spatial location ( _h, w_ ) of layer _l_ , and _wl_ is the learned channel-wise weighting. 

- **FID** (Fr´echet Inception Distance) evaluates the distributional similarity between generated and real frames based on image-level feature statistics; 


where ( _µr,_ Σ _r_ ) and ( _µg,_ Σ _g_ ) denote the mean and covariance of image-level features extracted from real and generated frames, respectively. 

17 

- **FVD** (Fr´echet Video Distance) extends the FID formulation from image-level features to videolevel features. It evaluates the distributional similarity between real and generated videos by computing the mean and covariance statistics over spatiotemporal video representations; 


where ( _µ_<sup>_v_</sup> _r_<sup>_,_Σ</sup><sup>_v_</sup> _r_<sup>) and (</sup><sup>_µv_</sup> _g_<sup>_,_Σ</sup><sup>_v_</sup> _g_<sup>) denote the mean and covariance of video-level features extracted</sup> from real and generated videos, respectively. 

- **FloLPIPS** measures perceptual similarity after motion alignment along estimated optical-flow trajectories; 


The motion weight is defined as: 


where _V_<sup>ˆ</sup> _t_ and _Vt_ denote the generated and real frames at time _t_ . _F_<sup>ˆ</sup> _h,w_<sup>_l_(</sup><sup>_·_) denotes the normalized</sup> feature extracted by the perceptual network at the _l_ -th layer and spatial location ( _h, w_ ), and _wl_ is the learned perceptual weight for that layer. Flow( _Vt, Vt_ +1) and Flow( _V_<sup>ˆ</sup> _t, V_<sup>ˆ</sup> _t_ +1) denote the optical flow between two adjacent frames in the real and generated videos, respectively. _Mt_ ( _h, w_ ) measures the discrepancy between the motion pattern in the real video and that in the generated video at location ( _h, w_ ) based on optical flow. 

- **FPS** measures the number of frames generated per second, quantifying the generation efficiency of the world model. 

## **D Ablation Study** 

### **D.1 Ablation on World Model Mechanisms** 

We first conduct ablation studies on the core design choices of the proposed world model, aiming to understand how different context modeling mechanisms affect long-horizon video generation stability. Specifically, we investigate the following factors: (i) the number of memory frames used as visual context, (ii) the use of a fixed reference frame, and (iii) the effect of adding noise to context frames during training. 

**Experimental Variants.** We compare the full WoVR model against three ablated variants: 

- WoVR w/o ref, which removes the fixed reference frame from the context window; 

- WoVR w. mem=1, which uses only a single-frame context; 

- WoVR w/o noisy context, which disables noise injection on context frames during training. 

All variants are trained and evaluated on the **LIBERO-Spatial** suite only. We train the world model using 1,500 VLA rollout trajectories and evaluate on a held-out set of 24 trajectories. 

**Quantitative Results.** Table 5 reports the quantitative results measured by LPIPS, FID, FVD and FloLPIPS under different rollout horizons. Compared to using a single-frame context, employing a multi-frame context with a fixed reference anchor significantly improves performance across all metrics. 

To better understand the failure modes behind these quantitative trends, we provide qualitative comparisons in Fig. 7. As shown in the figure, models without a fixed reference frame or noisy context exhibit noticeable spatial drift and object disappearance over long-horizon rollouts, whereas the full WoVR model remains visually stable and consistent with the ground truth. 

18 

Table 5: **Ablation study on world model mechanisms (LIBERO-Spatial).** Rollout denotes the rollout horizon length. 

||||**M**<br>|**etrics**<br>||
|---|---|---|---|---|---|
|**Method**|**Rollout**|**LPIPS**_↓_|**FID**_↓_|**FVD**_↓_|**FloLPIPS**_↓_|
||512|0_._091|36_._687|73_._493|0_._154|
|WoVR (Ours)|256|0_._069|27_._238|63_._948|0_._110|
||128|0_._051|20_._780|49_._017|0_._081|
||512|0_._133|73_._942|123_._502|0_._168|
|WoVR w/o ref|256|0_._089|49_._406|86_._000|0_._116|
||128|0_._064|35_._559|86_._146|0_._090|
||512|0_._120|64_._501|86_._042|0_._165|
|WoVR w. mem=1|256|0_._086|46_._790|81_._742|0_._117|
||128|0_._065|36_._047|79_._605|0_._095|
||512|0_._099|44_._712|77_._284|0_._160|
|WoVR w/o noisy context|256|0_._074|31_._691|61_._660|0_._115|
||128|0_._054|23_._444|58_._836|0_._085|


Removing the reference frame leads to a clear degradation in performance, especially under longer rollout horizons. This result suggests that anchoring the context with a fixed reference frame effectively suppresses error accumulation in the autoregressive feedback loop, which is critical for maintaining stability in long-horizon video generation. 

Furthermore, disabling noise injection on context frames also results in noticeable performance drops. While the degradation is moderate for short rollouts, the gap becomes more pronounced as the rollout length increases. This observation indicates that adding mild noise to context frames improves robustness in long-horizon generation by reducing over-reliance on precise conditioning inputs, thereby alleviating the train–inference gap. 

Overall, these results demonstrate that the proposed context modeling strategy—combining a fixed reference frame, a multi-frame memory window, and noisy context augmentation—plays a crucial role in stabilizing long-horizon video generation. Together, these mechanisms enable WoVR to maintain high fidelity and temporal consistency under closed-loop autoregressive inference, providing a more reliable simulator for downstream reinforcement learning. 

### **D.2 Ablation on PACE and KIR** 

We further ablate two interaction-level reliability mechanisms in WoVR: PACE, which aligns the world model with the updated policy distribution, and KIR, which initializes imagined rollouts near task-critical states to reduce effective prediction depth. This ablation is designed to separate the benefit of collecting policy-aligned data from the benefit of keyframe-initialized imagined interaction. 

**Experimental Setup.** We compare four WoVR variants under the one-trajectory SFT policyoptimization protocol from Sec. 4.2: 

- **WoVR w/o PACE (1,500 base)** , which trains the world model only on 1,500 trajectories rolled out by the base policy; 

- **WoVR w/o PACE (2,500 base)** , which trains the world model on 2,500 trajectories rolled out by the base policy, increasing the amount of data without changing the policy distribution; 

- **WoVR w/o KIR** , which keeps the PACE data protocol but removes keyframe initialization, so imagined rollouts are initialized from the episode start; 

**Results.** Table 6 reports the completed ablations on LIBERO-Spatial and LIBERO-Object. WoVR achieves the best performance on both suites, reaching an average success rate of 82.5% over the 

19 


Figure 7: **Qualitative ablation results on LIBERO-Spatial.** Ablated variants exhibit error accumulation and visual drift under long-horizon rollouts, while the full WoVR model remains stable and consistent with the ground truth. 

Table 6: **Ablation study on PACE and KIR.** All variants optimize the policy through imagined rollouts. Avg is computed over the two reported suites. 

|**Method**|**Spatial**|**Object**|**Avg**_↑_|
|---|---|---|---|
||**One-Trajectory SFT**|||
|OpenVLA-OFT-base [1]|63.6|36.4|50.0|
|WoVR w/o PACE (1,500 base)|75.4|76.2|75.8|
|WoVR w/o PACE (2,500 base)|77.8|77.2|77.5|
|WoVR w/o KIR|81.6|77.8|79.7|
|**WoVR**(1,500 base + 1,000 aligned)|**84.2**|**80.8**|**82.5**|
|∆|+20.6|+44.4|+32.5|


two reported suites. The two variants without PACE isolate the effect of additional base-policy data: increasing the world-model training set from 1,500 to 2,500 base-policy trajectories improves the two-suite average only from 75.8% to 77.5%. This modest +1.7-point gain suggests that simply adding more data from the same base-policy distribution brings limited benefit once that distribution is sufficiently covered. 

Fig. 8 shows how WoVR evolves during one-trajectory SFT training. Before the PACE transition, the imagined training success rate can keep improving while the real-evaluation curve lags behind, revealing a growing mismatch between the evolving policy and the base world model. After updating the simulator from WMBase to WMEvo, the imagined training curve is re-calibrated to the policy-induced distribution and becomes more consistent with real-environment evaluation. This post-PACE alignment indicates that rollout data collected from the evolved policy helps correct accumulated simulator mismatch and mitigates hallucination-induced over-optimism in imagined RL. Together with the quantitative results in Table 6, these curves support the role of PACE in making world-model training signals more faithful to real-world policy performance. 

20 


Figure 8: **One-trajectory SFT training and real-evaluation curves under WoVR.** Blue denotes the training success rate in the world model, red denotes the evaluation success rate in the real environment, and the shaded vertical band marks the PACE transition from WMBase to WMEvo. 

The KIR ablation further shows the importance of initializing imagined rollouts near task-critical states. Removing KIR reduces performance from 84.2% to 81.6% on Spatial and from 80.8% to 77.8% on Object, lowering the two-suite average from 82.5% to 79.7%. These results indicate that KIR improves imagined interaction even when PACE is retained, by shortening the effective prediction depth and reducing early error accumulation. Together, the PACE and KIR ablations suggest that WoVR benefits from both policy-aligned simulator refinement and keyframe-initialized rollout design. 

### **D.3 Ablation on Reward Modeling** 

We further analyze the impact of different reward modeling choices on policy optimization, comparing a lightweight ResNet-based sparse reward model with a Qwen3-VL-based dense reward model. 

**Experimental Setup.** We keep all other components fixed and vary only the reward model used during policy optimization. The sparse reward model predicts binary task success, while the dense reward model provides fine-grained progress signals. Both variants are evaluated on the same training setup and metrics as in Sec. 4.2. 


Figure 9: Ablation on reward modeling: dense vs. sparse reward. 

**Results and Analysis.** Fig. 9 shows the learning curves under the two reward settings. We observe that the dense reward model improves sample efficiency in the early stage of training, leading to faster initial performance gains. However, both reward designs converge to similar final performance. 

Despite its advantage in early learning, the dense reward model incurs significantly higher computational cost, as it relies on a large vision-language backbone (Qwen3-VL 2B). In practice, we find that rollout with the dense reward model is approximately 3 _×_ slower than with the lightweight sparse reward model. 

21 

What’s more, binary rewards are widely adopted in manipulation benchmarks such as LIBERO as well as real-world robotic setups. Taking the above accounts into considerations, we adopt the sparse reward model in all main experiments. 

## **E Qualitative Failure Mode Analysis** 


Figure 10: Visualization of real-world execution before and after WoVR policy optimization. 

We further analyze representative failure modes of base VLA model and compare them with the behaviors after WoVR. Fig. 10 visualizes execution traces across two robotic platforms and six manipulation tasks. The comparison shows that WoVR not only improves task success rates, but also changes the dominant failure patterns of the base VLA policy. 

On the Franka Panda platform, the base policy exhibits different failure modes across the three tasks. In **Pick Banana** , the robot often repeatedly attempts to grasp the banana without establishing a stable grasp, or successfully grasps the banana but fails to move it above the plate. After applying WoVR, the policy more reliably grasps the banana and transfers it into the plate with faster and more direct motions. In **Pick Bread** , the base policy mainly fails by prematurely opening the gripper, causing the bread to drop, or by keeping the gripper closed after reaching the target region. WoVR largely suppresses these two failure modes and produces more consistent release behavior. In **Open Drawer** , the base policy frequently fails to reach the handle accurately or fails to pull the drawer after making contact. With WoVR, the robot more often completes the full interaction sequence, including handle approach, contact, and drawer pulling. 

On the AgileX Piper platform, failures are more strongly affected by noisier state estimation and less stable low-level control. In **Pick Cube** , the base policy often moves the cube to the target region but fails to release the gripper, or places the cube with an incorrect pose such that it does not fall into the target hole. WoVR substantially reduces these errors by producing more stable placement and release behaviors. In **Pick Tomato** , the base policy commonly fails to close the box after placing the tomato, or leaves the gripper trapped inside the box. After WoVR optimization, these failure cases are mitigated, although the task remains sensitive to contact and box geometry. In **Fold Towel** , the base policy often fails to complete the fold or keeps holding the towel after folding. WoVR improves the temporal coordination between folding and release, leading to a higher success rate on this deformable-object task. 

Overall, the qualitative analysis suggests that WoVR improves real-world execution by reducing recurrent action-level failure modes, including unstable grasping, premature or delayed gripper release, inaccurate target placement, and incomplete contact-rich interactions. These results are consistent with the quantitative real-world improvements reported in Sec. 4.3, and indicate that 

22 


Figure 11: Two types of robotic arm platforms 

hallucination-aware policy optimization in imagination can translate into more reliable closed-loop behavior on physical robots. 

## **F Real-World Experiments** 

### **F.1 Hardware Setup** 

We evaluate our method on two distinct real-world robotic platforms: the AgileX Piper robotic arm (left) and the Franka Emika Panda robotic arm (right) as shown in Fig.11, each equipped with twofinger grippers. This was done to test the robustness of our method under different control precision hardware conditions. 

**AgileX Piper** AgileX Piper is a 6-degree-of-freedom robotic arm. We conduct remote operation based on the **cobot Magic** platform. We use the D435 camera with a head view to capture RGB images and synchronize and record the data at a frequency of 10Hz. 

**Franka Emika Panda** Franka Emika Panda is a 7-degree-of-freedom robotic arm. We use the fixed third-person perspective D435 to record RGB images and use a spatial mouse for remote operation. Data is recorded at a frequency of 30Hz. 

### **F.2 Detailed task requirements** 

Here, we provide the detailed requirements for each task on both robotic platforms. 

On Franka platform, we evaluate three manipulationtasks: 

- Pick Banana: Pick a banana and place it onto a plate; 

- Pick Bread: Pick a bread and place it into the toaster; 

- Open Drawer: Pull the drawer open; 

On AgileX Piper platform,we also evaluate three other tasks: 

- Pick Cube: Pick up a cube and place it into a box; 

- Pick Tomato: Pick up a tomato, place it into a box, and close the lid; 

- Fold Towel: Fold the towel into a compact configuration. 

### **F.3 Practical Considerations for Real-World Deployment** 

Here, we introduce the selection of the action space and control method for the robotic arm. This is of crucial importance for the actual operation of the less precise robotic arm. 

23 

**Platforms and Action Space.** Experiments are conducted on two robotic platforms: the **AgileX Piper** manipulator and the **Franka Emika Panda** . For both platforms, the action space is defined in the delta end-effector (delta EEF) space, where the VLA policy outputs relative end-effector displacements that are also used as inputs to the world model. 

Since the lower-level drives of both robotic arms are controlled in the absolute joint space, each predicted delta action is converted into an absolute end-effector pose, followed by inverse kinematics (IK) to obtain executable joint commands. 

**Rotation Parameterization.** A critical design choice is the parameterization of rotational actions. Directly regressing ∆RPY is often unstable, since Euler angles suffer from discontinuities and singularities, and small prediction errors may lead to large deviations in the reconstructed absolute orientation, thereby affecting IK consistency. 

To improve robustness, we adopt the Rotation 6D representation [49, 50]. Given the current endeffector orientation _Rt ∈ SO_ (3) and the next orientation _Rt_ +1 _∈ SO_ (3), we first compute the local relative rotation: 


Following the standard 6D rotation representation, RotMatTo6D( _·_ ) denotes flattening the first two columns of a rotation matrix. The corresponding delta rotation in 6D form is computed as: 


Here, ∆ **r** 6 _D,t_ represents the relative rotation from the current pose to the next pose in the local end-effector frame. 

During execution, the predicted 6D vector is converted back to a valid rotation matrix through Gram– Schmidt orthogonalization. Specifically, given two predicted vectors **a** 1 _,_ **a** 2 _∈_ R<sup>3</sup> , we compute: 


The absolute orientation is then updated as: 


Compared with RPY, Rotation 6D avoids angle wrapping and gimbal-lock singularities. Compared with quaternions, it avoids the double-cover ambiguity, where **q** and _−_ **q** represent the same rotation. In addition, the network can directly regress an unconstrained 6D vector, which is later projected to a valid rotation matrix by orthogonalization. This makes the action representation more continuous and better suited for learning stable end-effector rotation commands. 

The final action space is defined as: 


**Platform-Specific Considerations.** While the overall control pipeline is shared, the two platforms exhibit different levels of state estimation accuracy. 

The Franka Panda provides highly accurate and stable end-effector state feedback, making the standard update 


sufficient in practice. Here, the addition only denotes delta-to-absolute action conversion, not direct physical motion composition. 

24 

Table 7: Task and embodiment settings in WoVR real-world experiments. Task-specific data scales are reported in Panel (a), while embodiment-specific training configurations are summarized in Panel (b). 

|||**(a) Task-si**<br><br><br>|**pecific data sca**<br>|**i  le.**<br> <br>||
|---|---|---|---|---|---|
||Embodime|nt<br>Task<br>|VLA SFT Dem|os<br>WM SFT Rollouts||
||Franka<br>Franka|Pick banana<br>Pick bread|25<br>25|120<br>120||
||Franka|Open drawer|25|120||
||Agilex|Pick cube|75|180||
||Agilex|Pick tomato|50|180||
||Agilex|Fold towel|50|210||
||**( i  i**|**b) Embodiment-spei  i**|**cific training ci**|**i  onfiguration.**||
|Embodim|ent<br>VL|A SFT Steps<br>W|M SFT Steps|Max Episode Steps<br>R|L Epochs|
|Franka||50k|750k|160|50|
|Agilex|50k (O<br>|penVLA-OFT)<br>30k (_π_0_._5)|1.25M|224|60|


In contrast, the AgileX Piper exhibits noticeable noise and bias in the observed end-effector state, which leads to drift when applying the same update rule. To mitigate this issue, we instead compute actions using an accumulated formulation: 


Here, _s_ 0 represents the given initial position. This reduces sensitivity to noisy feedback and improves long-horizon execution stability. 

Although this formulation may introduce discrepancies under external disturbances (e.g., contacts), such errors are compensated by the visual feedback loop of the VLA policy. 

**Summary.** These results highlight that while the proposed delta-space formulation generalize across platforms, handling state estimation noise is critical for reliable real-world deployment. The proposed design enables stable closed-loop execution under both high-precision and low-cost hardware settings. 

### **F.4 Task Setting** 

The amount of VLA SFT data differs across tasks because the tasks have different levels of difficulty. We allocate more demonstrations to harder tasks to ensure that the supervised policy reaches a sufficient initial performance before reinforcement learning. The amount of data used for world model training follows the same principle: tasks with more complex dynamics, longer horizons, or more diverse interactions require more rollout data for reliable modeling. 

In our real-world experiments, we do not use PACE for data collection due to efficiency considerations. Instead, we construct the world-model training set by rolling out multiple VLA SFT checkpoints saved at different training steps. This strategy increases trajectory diversity and broadens action-space coverage, as checkpoints from different training stages induce distinct behavior distributions. For example, on the Franka platform, we collect rollout trajectories from checkpoints saved at 25k, 30k, 35k, 40k, 45k, and 50k SFT steps. We then select the best-performing checkpoint based on real-world evaluation, report its performance, and use it as the initialization for subsequent RL. 

25 

