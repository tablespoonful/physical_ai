---
title: "Beyond Imitation: Reinforcement Learning-Based Sim-Real Co-Training for VLA Models"
date: "2026-02-13"
authors: "Liangzhi Shi; Shuaihang Chen; Feng Gao; Yinuo Chen; Kang Chen; Tonghe Zhang"
venue: "CoRL 2026"
url: https://arxiv.org/abs/2602.12628
pdf: https://arxiv.org/pdf/2602.12628
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.12628)** / [論文ページ](https://arxiv.org/abs/2602.12628)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Beyond Imitation: Reinforcement Learning-Based Sim-Real Co-Training for VLA Models** 

**Liangzhi Shi**<sup>1</sup><sup>_,_5</sup><sup>_,∗_</sup> **, Shuaihang Chen**<sup>2</sup><sup>_,_6</sup><sup>_,∗_</sup> **, Feng Gao**<sup>1</sup> **, Yinuo Chen**<sup>1</sup> **, Kang Chen**<sup>3</sup><sup>_,_6</sup> **, Tonghe Zhang**<sup>4</sup> **, Hongzhi Zang**<sup>1</sup> **, Jiakai Zhou**<sup>1</sup> **, Weinan Zhang**<sup>2</sup> **, Chao Yu**<sup>1</sup><sup>_,†_</sup> **, Yu Wang**<sup>1</sup> 

1Tsinghua University 2Harbin Institute of Technology 3Peking University 4Carnegie Mellon University 5Shanghai AI Laboratory 6Zhongguancun Academy 

> _∗_ Equal Contribution _†_ Corresponding author: `yuchao@sz.tsinghua.edu.cn` Project Page: `https://rl-co-training.github.io/` 

**Abstract:** Simulation offers a scalable and low-cost way to enrich visionlanguage-action (VLA) training, reducing reliance on expensive real-robot demonstrations. However, most sim-real co-training methods rely on supervised fine-tuning (SFT), which treats simulation as a static source of demonstrations and does not exploit large-scale closed-loop interaction. Consequently, real-world - gains and generalization are often limited. In this paper, we propose an _<u>RL</u>_ based sim-real _<u>Co</u>_ -training (RL-Co) framework that leverages interactive simulation while preserving real-world capabilities. Our method follows a generic two-stage design: we first warm-start the policy with SFT on a mixture of real and simulated demonstrations, then fine-tune it with reinforcement learning in simulation while adding an auxiliary supervised loss on real-world data to anchor the policy and mitigate catastrophic forgetting. We evaluate our framework on four real-world tabletop manipulation tasks using two representative VLA architectures, OpenVLA and _π_ 0 _._ 5, and observe consistent improvements over realonly fine-tuning and SFT-based co-training, including +24% real-world success on OpenVLA and +20% on _π_ 0 _._ 5. Beyond higher success rates, RL co-training yields stronger generalization to unseen task variations and substantially improved realworld data efficiency, providing a practical and scalable pathway for leveraging simulation to enhance real-robot deployment. 

**Keywords:** Vision-language-action models, sim-real co-training, reinforcement learning 

## **1 Introduction** 

Vision-language-action (VLA) models are a promising route toward general-purpose robots, integrating visual observations, language instructions, and action generation in a unified policy framework [1, 2, 3, 4, 5, 6]. Large-scale robot demonstrations and visual-language priors support efficient supervised fine-tuning [7, 8, 9, 10], yet policies adapted from limited real demonstrations remain brittle under novel scenes, object variations, and closed-loop execution shifts [11, 12]. Collecting more real data can help, but remains slow, expensive, and difficult to scale [7, 8]. 

Simulation can address this bottleneck by cheaply scaling environments, trajectories, and closedloop interaction [13, 14, 15], but simulation-trained policies still face the sim-to-real gap. Domain randomization improves robustness by varying visual and physical factors [16, 17, 18], while real-to- 

10th Conference on Robot Learning (CoRL 2026), Austin, Texas, USA. 

sim-to-real and reconstruction-based pipelines improve simulator fidelity through scene reconstruction, system identification, and digital twins [19, 20, 21, 22]. These approaches reduce the gap, but often require carefully designed randomization, accurate reconstruction, or task-specific simulator tuning. 

Sim-real co-training offers a different route by introducing real-world data into training instead of requiring direct transfer from a simulation-trained policy. Prior work aligns sim-real representations or joint observation-action distributions [23, 24, 25, 26], and complementary studies show that even low-fidelity or weakly aligned simulation can improve real-world policies when it expands the task-relevant training distribution [27, 28]. This makes co-training a scalable alternative to highfidelity sim-to-real pipelines, but most existing methods still treat simulation as a static source of demonstrations, leaving closed-loop interaction underexplored. 

Interactive policy improvement directly targets this limitation. Reinforcement learning **Real-World Simulation** can reduce the closed-loop distribution shift of pure imitation through trial-and-error inter- **Real SFT Simulation RL** action [29, 30], but robotic manipulation often involves sparse rewards, long horizons, and costly exploration [31]. Combining imi- **SFT-based Sim-Real Co-Training** tation with RL, either through demonstration **+** initialization or behavior-prior regularization, is therefore a common remedy [32, 33, 34, 35, **RL-based Sim-Real Co-Training (Ours)** 36, 37]. Recent VLA and large robot policy post-training methods similarly use supervised **+** fine-tuning before RL improves task success and generalization [12, 38, 39, 40, 41]. HowFigure 1: **Training paradigms.** RL-Co uses simever, these methods usually improve the policy ulation for RL interaction while anchoring upwithin one interaction domain and, when apdates with real-world SFT. plied to sim-to-real settings, still rely on zeroshot transfer. Sim-real VLA post-training must instead exploit cheap simulation interaction while preventing drift from real visual observations, action distributions, and execution priors. 

In this work, we propose an RL-based sim-real co-training framework for VLA models that turns simulation into an interactive post-training source while using real demonstrations as cross-domain anchors. The policy is first initialized through supervised sim-real co-training, then improved by reinforcement learning in simulation with an auxiliary real-world SFT objective that keeps simulationdriven updates grounded in deployable observations and actions. 

We evaluate RL-Co on real-world tabletop manipulation tasks with OpenVLA [3] and _π_ 0 _._ 5 [5]. Across tasks and model families, RL-Co improves real-world success over real-only SFT and SFTbased sim-real co-training using simulation demonstrations generated by MimicGen, while also improving generalization to unseen task variations, reducing real-demonstration needs, and providing gains beyond visual diversity from heavy domain randomization or data augmentation. 

## **2 Related Works** 

### **2.1 Vision-Language-Action Models for Manipulation** 

Recent vision-language-action (VLA) models formulate manipulation as conditional action generation from visual observations and language instructions [1, 2, 3, 4, 5, 6]. Their progress relies on large-scale robot demonstrations and visual-language priors [7, 8, 9], but deployment often still requires task-specific supervised fine-tuning [10] and remains sensitive to shifts across scenes, objects, and execution states [11, 12]. These limitations motivate post-training methods that improve robustness and generalization beyond static supervised data. 

2 

### **2.2 Interactive and Regularized Post-Training for Robot Policies** 

Supervised fine-tuning or behavior cloning aligns policies with target demonstrations, but it is vulnerable to covariate shift and compounding closed-loop errors [29, 30]. Reinforcement learning provides an interactive alternative and has long been used for robot policy learning [42, 43]. SERL [44] demonstrates efficient real-robot learning, while DSRL [45] steers diffusion-policy noise, RL-100 [46] combines offline and online RL for diffusion policies, _π_ 0<sup>_∗_</sup> _._ 6<sup>[47]learnsfromdeploy-</sup> ment experience and expert corrections, and RLT [48] trains a lightweight actor–critic on VLA representations. However, direct real-world RL is often constrained by safety, reset cost, and sample efficiency [31]. 

Recent work therefore moves RL post-training for larger robot policies and VLA models into simulation. Empirical studies demonstrate gains in VLA generalization [12], while FLaRe [49] and SimpleVLA-RL [38] scale RL fine-tuning of pretrained robot policies. For flow-based policies, ReinFlow [39] enables likelihood-based online updates, SAC Flow [40] stabilizes off-policy learning, and _π_ `RL` [50] develops online RL fine-tuning for flow-based VLAs. 

In parallel, offline, online, and robot-adaptation methods show that reward-driven updates can be stabilized by imitation-style losses, behavior constraints, action priors, or demonstration-derived reward and policy priors [33, 34, 35, 36, 37], while residual policy learning offers another way to refine imitation-learned manipulation behaviors [51]. PLD [52] trains residual RL specialists around a frozen VLA and uses their collected trajectories for supervised fine-tuning of the VLA. These works establish the value of combining interaction-driven improvement with behavior priors, but they typically operate in a single deployment domain or rely on zero-shot sim-to-real transfer. RLCo instead uses simulation for interaction while anchoring VLA updates with real demonstrations for physical deployment. 

### **2.3 Sim-to-Real Transfer and Sim-Real Co-Training** 

Simulation provides a safe and scalable platform for robot learning, and several sim-to-real RL methods use it to accelerate real-world adaptation [53, 54, 55, 56]. Direct transfer can succeed with suitable simulation diversity and training scale [57, 58], although visual and dynamics discrepancies remain challenges. Domain randomization addresses this gap through broad visual or physical variations [16, 17, 18, 59, 60], while real-to-sim-to-real and reconstruction-based pipelines improve simulator fidelity through scene reconstruction, system identification, or digital twins [19, 20, 21, 22]; both can require careful randomization, environment construction, or tuning. 

Beyond direct transfer, sim-real co-training introduces real-world data by learning domain-invariant or task-relevant representations [23, 24, 25, 26], or by treating simulation as a scalable source of demonstrations and trajectory variation [61, 62, 63, 64] that can improve real-world policies despite limited visual fidelity or task correspondence [27, 28, 65, 66]. 

These approaches show that imperfect simulation can provide useful training data, but mostly exploit it through supervised data mixing rather than closed-loop policy improvement. RL-Co builds on this data-augmentation view while incorporating reinforcement learning into co-training, enabling active exploration in simulation and grounding the policy with real-world data. 

## **3 Preliminaries** 

### **3.1 Problem Setup and VLA Post-Training** 

We study a two-domain manipulation setting with a real-world task domain _T_ real and a corresponding simulation domain _T_ sim. The two task-level counterparts share the robot embodiment, action interface, language instruction, and task-level initial-state distribution, while allowing visual and dynamics discrepancies. We model both as partially observable decision processes. A visionlanguage-action (VLA) policy _πθ_ maps recent observations and the language instruction to robot actions. 

3 


Figure 2: **Overview of RL-Co.** Stage I initializes the VLA policy with mixed real and simulated demonstrations. Stage II fine-tunes it with simulation RL while using real-world SFT as a regularizer to preserve deployable behaviors. 

We use two standard VLA post-training primitives: supervised fine-tuning (SFT) on task demonstrations [3, 10, 4] and reinforcement learning (RL) through reward-guided interaction. RL-Co combines them so that SFT provides initialization and real-domain anchoring, while RL supplies closed-loop improvement in simulation. More detailed problem definitions and post-training objectives are provided in Appendix A. 

### **3.2 SFT-based Co-Training** 

Given a real-world dataset _D_ real and a simulation dataset _D_ sim, SFT-based sim-real co-training jointly fine-tunes the VLA policy on both sources of demonstrations: 


where _α ∈_ [0 _,_ 1] controls the relative contribution of simulated data. Following Maddukuri et al. [27], this objective can be implemented by sampling training trajectories from _D_ sim with probability _α_ and from _D_ real with probability 1 _− α_ . 

This SFT-based co-training strategy is a strong baseline for leveraging simulation as additional supervised data. However, because it remains an imitation objective, it cannot explicitly use reward feedback or online interaction, motivating the reinforcement learning-based co-training approach introduced next. 

## **4 Method** 

We present our _<u>RL</u>_ -based sim-real _<u>Co</u>_ -training (RL-Co) framework, as summarized in Fig. 2. RLCo follows a two-stage design. In Stage I, we initialize the policy through supervised co-training on both real-world and simulated demonstrations. In Stage II, we further improve the policy with reinforcement learning in simulation, while explicitly preserving real-world capabilities through an auxiliary supervised objective. 

### **4.1 Stage I: SFT Co-Training for Policy Initialization** 

Starting from a pre-trained VLA policy _πθ_ that has not been adapted to the target tasks, Stage I initializes the policy with both real-world and simulated demonstrations. Specifically, we apply the SFT co-training objective in Section 3.2 to the real-world dataset _D_ real and the simulation dataset _D_ sim. This stage serves two purposes: it lets the policy rapidly absorb task-specific real-world 

4 


Figure 3: **Environment visualizations.** (a) Real and simulated tabletop tasks used in our simreal co-training experiments. (b) Examples of visual domain-randomized simulation and dataaugmented real observations used to test whether visual diversity alone explains the gains. 

knowledge needed for deployment, and gives the policy sufficient simulation competence for nontrivial RL initialization by learning from simulated demonstrations. These properties motivate SFT co-training as the first stage of RL-Co; Section 5.3 provides a detailed analysis of its contribution. 

### **4.2 Stage II: Sim-Real Co-Training with Real-Regularized RL** 

While Stage I equips the policy with both real-world and simulated capabilities, its optimization remains limited to imitation. Stage II therefore seeks to expand the policy’s competence through online interaction in simulation, while preventing degradation of real-world performance. To achieve this, we introduce an auxiliary supervised fine-tuning objective on real-world data into the RL finetuning process. During simulation training, each policy update is driven by a reinforcement learning loss _L_ RL, which encourages exploration and maximizes task rewards. We augment this objective with an SFT loss on _D_ real, yielding 


where _β_ balances reinforcement learning updates and preservation of real-world knowledge. 

Intuitively, the RL term lets the policy exploit large-scale simulated interaction to explore diverse behaviors and improve task performance, while the real-world supervision term regularizes the update by anchoring the policy to real demonstrations and mitigating catastrophic forgetting. This simple yet effective modification is compatible with a wide range of RL fine-tuning algorithms and forms the core of RL-Co. 

## **5 Experiments** 

In this section, we empirically evaluate the proposed RL-Co framework and ask: 

- Does RL-Co improve real-world effectiveness and robustness across tasks and VLA architectures? 

- Why is the two-stage design necessary for transferring simulation interaction to real-world deployment? 

- To what extent can RL-Co reduce the amount of required real-world demonstration data? 

We answer these questions in order: First, section 5.2 compares RL-Co with real-only SFT and SFTbased sim–real co-training, evaluates robustness under unseen settings, and tests whether stronger visual diversity alone explains the gains. Next, section 5.3 analyzes the key components of RL-Co, including simulation SFT initialization, real-world supervision, and the hyperparameters _α_ and _β_ . Finally, section 5.4 studies data efficiency by varying the number of real-world demonstrations. 

5 

|VLA Model|Experiment Setting|`Pick and Place`|`Push Cube`|`Open Drawer`|`Close Drawer`|`Avg`|
|---|---|---|---|---|---|---|
||Real-Only Training|6.3_±_0.0|20.0_±_13.3|0.0_±_0.0|10.0_±_10.0|9.1_±_5.8|
|OpenVLA|SFT Co-Training|23.4_±_4.7|51.7_±_5.0|0.0_±_0.0|85.0_±_5.0|40.0_±_3.7|
||**RL-Co (Ours)**|**57.8**_±_10.9|**68.3**_±_11.7|**35.0**_±_15.0|**95.0**_±_5.0|**64.0**_±_0.7|
||Real-Only Training|71.9_±_9.4|0.0_±_0.0|0.0_±_0.0|35.0_±_15.0|26.7_±_1.4|
|_π_0_._5|SFT Co-Training|68.8_±_9.4|10.0_±_3.3|10.0_±_0.0|95.0_±_5.0|45.9_±_4.4|
||**RL-Co (Ours)**|**81.3**_±_9.4|**18.3**_±_1.7|**65.0**_±_5.0|**100.0**_±_0.0|**66.1**_±_4.0|


Table 1: **Comparison of real-world success rates under different training paradigms.** We compare our RL-Co approach with real-only SFT and SFT co-training across four tabletop manipulation tasks, evaluated on both OpenVLA and _π_ 0 _._ 5. Results are reported in terms of success rate (SR, %). Values are the mean _±_ population standard deviation over two evaluation sessions of one trained checkpoint. Avg macro-averages tasks within each session before computing the mean and standard deviation. 

### **5.1 Experimental Setting** 

**Environmental setting.** We evaluate RL-Co on four tabletop manipulation tasks that require perception, language grounding, and control: `Pick and Place` , `Push Cube via Instruction` , `Open Drawer` , and `Close Drawer` . Fig. 3(a) visualizes the real and simulated environments. Both domains use a Franka Emika Panda robot with 7-DoF end-effector delta control; real-world observations are captured by a fixed RGB camera, and all methods are evaluated on the same independently sampled initial states with task success rate as the metric. We build the simulation environments in ManiSkill [15] and align them with the real setup at the task level, while allowing differences in object identity, materials, textures, and lighting. Detailed real-world setup, task definitions, evaluation protocol, and simulation configuration are provided in Appendices C–E. 

**Evaluation protocol.** We evaluate one trained checkpoint per condition across two sessions. Each session contains 32 trials for `Pick and Place` , 30 for `Push Cube` , 10 for `Open Drawer` , and 10 for `Close Drawer` . Appendix D.1 details the aggregation of session-level results. The real setup was fixed before constructing and aligning the simulator. 

**Data generation.** For each real-world task, we collect 20–50 successful expert demonstrations via human teleoperation, forming _D_ real. In simulation, we use MimicGen [61] with replayed real-world trajectories as seeds to generate 1,000 successful trajectories per task, forming _D_ sim. Further details on real trajectory collection, seed replay, and trajectory pruning are provided in Appendix B. 

**Implementation.** We instantiate RL-Co on two representative VLA families: next-token predictionbased OpenVLA [3] and flow-matching-based _π_ 0 _._ 5 [5]. In Stage I, we directly mix real-world and simulation datasets and train with the official SFT implementations of each model. In Stage II, OpenVLA follows the PPO [67] fine-tuning protocol and implementation of Liu et al. [12] with LoRA [68] and our real-world regularization loss, whereas _π_ 0 _._ 5 uses ReinFlow [39] implemented with RLinf [69], updating only its action expert. We train each model-task pair with a fixed interaction budget and run simulation RL to convergence. 

### **5.2 Real-World Effectiveness and Robustness** 

### **5.2.1 Main Comparison Across Tasks and VLA Models** 

We first evaluate whether RL-Co improves real-world deployment under limited real demonstrations and imperfect simulation. We compare against real-only SFT and SFT co-training with static MimicGen demonstrations. RL-Co uses the same Stage I data, followed by online simulation rollouts and the real-data SFT anchor in Stage II. Table 1 reports the quantitative results. 

Real-only SFT is weak under limited demonstrations, especially for OpenVLA, which remains at or below 20% success in all environments. The stronger _π_ 0 _._ 5 model performs well on the simpler `Pick and Place` task but still struggles with instruction-conditioned pushing and contact-rich drawer manipulation. 

6 

SFT-based sim–real co-training partially helps, for example on `Close Drawer` , but its gains are inconsistent and can be limited when real-only SFT is already strong, as in `Pick and Place` . 

In contrast, RL-Co achieves the strongest overall real-world success, showing that closed-loop simulation RL expands policy capability beyond static simulated demonstrations while real-world SFT regularization keeps the update deployable. Appendix H.3 further compares against SFT on strong RL-generated rollouts on `Open Drawer` , reducing the confound between the optimization objective and simulation-data quality. 

### **5.2.2 Generalization Under Distribution Shifts** 

To further understand how reinforcement learning contributes to improved policy performance, 100 **-25.0 -11.3** we evaluate generalization under distribution shifts. 80 **-46.9 -37.5 -31.9 -13.8** We focus on `Pick and Place` with _π_ 0 _._ 5, where all 60 **70.0** three methods achieve comparable in-distribution **56.3 55.0** success, and examine whether their robustness dif40 **40.0** fers under unseen conditions. We test _Unseen Ob-_ 20 **~~25.0~~ 31.3** _jects_ , replacing manipulated objects with novel cat0 egories, and _Unseen States_ , perturbing the robot iniUnseen Objects Unseen States tial pose beyond the training distribution. As shown Real-only SFT co-training RL-Co (Ours) in Fig. 4, real-only SFT degrades sharply under both shifts, while SFT-based sim–real co-training Figure 4: **Comparison of generalization un-** improves robustness by adding simulated variation. **der unseen settings.** Solid bars show unseen success rate; pale bars show in-distribution RL-Co maintains the strongest unseen performance success rate. and the smallest drops, suggesting that interactive simulation helps the policy acquire closed-loop behaviors that transfer more reliably to unseen realworld conditions. 

### **5.2.3 Targeted Comparison with Stronger Visual-Diversity Baselines** 

Having established stronger robustness, we next test whether these gains can be explained by stronger visual diversity alone. On _π_ 0 _._ 5 for `Pick and Place` , using the same evaluation protocol, we compare against two stronger visual-diversity baselines: heavy visual domain randomization in simulation and video-based augmentation applied to the same real demonstrations. Fig. 3(b) illustrates the visual variations, and Table 2 reports the results. 

The heavy-DR baseline randomizes the simulated scene with 21 tabletop textures and 21 background textures, independently sampled during training, but still transfers poorly to the real world. The Cosmos-Transfer [70] augmentation baseline generates 1,000 visually augmented trajectories from the original real demonstrations and mixes them with the real data for SFT. Its performance remains below RL-Co, indicating that visual-only augmenta- 

|Method|SR (%)|
|---|---|
|Heavy DR zero-shot|10_._9_±_7_._8|
|Cosmos augmentation|67_._2_±_1_._6|
|**RL-Co (Ours)**|**81**_._**3**_±_**9**_._**4**|


Table 2: **Targeted visual-diversity comparison.** Success rates on `Pick and Place` with _π_ 0 _._ 5 under the same real-world evaluation protocol. 

tion without additional action-level behavior or closed-loop interaction is insufficient. In contrast, RL-Co expands the policy’s action-level behavioral repertoire through reward-driven interaction in simulation, thereby improving the model’s task capability beyond what can be achieved by visual augmentation alone. 

### **5.3 Mechanistic Analysis and Design Ablations** 

We conduct ablation studies to understand how the components of RL-Co contribute to effective sim–real co-training. We examine the role of simulation data in Stage I, the contribution of real- 

7 


Figure 5: **Mechanistic ablations of RL-Co.** (a) Simulation SFT initialization enables efficient RL training. (b) Real-world supervision in both stages improves deployment. (c) RL co-training remains effective across co-training ratios _α_ and regularization weights _β_ . Shaded regions indicate standard deviation where applicable. 

world supervision in both stages, and the sensitivity to the co-training ratio and regularization weight. 

### **5.3.1 Effect of Simulation SFT Initialization** 

To evaluate the necessity of simulation data in Stage I, we perform RL co-training starting from a policy trained only with real-world demonstrations. Fig. 5a compares RL co-training from real-only SFT initialization against full sim–real SFT initialization. 

Without simulated SFT initialization, the policy has extremely poor sample efficiency and remains near-trivial after over three million interaction steps. In contrast, sim–real SFT co-training provides a stronger initialization and enables efficient RL optimization, showing that Stage I is not merely a data-mixing warm-up but a necessary step for making simulation RL learnable. 

### **5.3.2 Role of Real-World Supervision in Two Stages** 

Having examined simulation-based initialization, we next assess the role of real-world supervision by removing it from Stage I and Stage II respectively. Fig. 5b reports real-world success on `Pick and Place` with _π_ 0 _._ 5 under all ablations. First, removing Stage II real-world SFT regularization substantially reduces success, indicating domain drift during simulation RL without explicit realdata anchoring. Removing Stage I real-world SFT further degrades deployment, suggesting that supervised learning extracts useful priors from limited real demonstrations more efficiently than RL. Notably, when real-world supervision is removed from both stages, the policy is trained solely in simulation with limited visual fidelity and achieves only 6 _._ 3% success when deployed zero-shot in the real world. This highlights the importance of real-world data: simulation-only learning is insufficient for deployment without real-data adaptation. 

### **5.3.3 Sensitivity to Co-Training Ratio alpha and Regularization Weight beta** 

Finally, we examine how the balance of simulated and real-world supervision affects performance. On `Pick and Place` and `Open Drawer` with _π_ 0 _._ 5, we vary the Stage I mixture ratio _α_ , then select an SFT-co-trained model for each task and vary the Stage II regularization weight _β_ . 

As shown in Fig. 5c, _α_ strongly affects SFT co-training: on `Pick and Place` , more simulated data can hurt because real-only training is already strong, whereas on the harder `Open Drawer` task, neither too little nor too much simulation is optimal. Nevertheless, across the tested _β_ values, RL 

8 

co-training consistently improves over the corresponding SFT-co-trained policies and exceeds SFTonly models trained under different _α_ settings. These results indicate that once a reasonable SFT initialization is available, reward-driven interaction can expand the performance limit of supervised co-training, while real-world regularization keeps updates less brittle within the tested range. 

### **5.4 Real-Data Efficiency** 

We finally study whether RL-Co can reduce the amount of real-world demonstration data required for deployment. Unlike the video augmentation baseline, this experiment varies the amount of real expert behavior available for training. On the contact-rich `Open Drawer` task, we extend the real-world demonstrations to 200 trajectories, vary the number used for training, and compare real-only SFT, SFT cotraining, and RL-Co in Fig. 6. 

As expected, all methods improve with additional real demonstrations, and SFT co-training benefits more rapidly than real-only training by 


Figure 6: **Real-data efficiency.** Shaded regions indicate standard deviation. 

using simulated data. However, both supervised baselines remain substantially below or comparable to RL-Co trained with far fewer real-world demonstrations, showing that RL-Co can amplify limited real data through simulation interaction and provide a more data-efficient path to deployment than collecting additional physical demonstrations alone. Appendix J further reports resource estimates for simulator setup, data generation, and training. 

## **6 Conclusion** 

This paper proposes RL-Co, an RL-based sim-real co-training framework for vision-language-action (VLA) models. RL-Co addresses the limitation of supervised sim-real co-training by first initializing the policy with real and simulated demonstrations, then improving it through reinforcement learning in simulation while using real-world supervision to preserve deployable behaviors. 

Experiments across four tabletop tasks and two VLA architectures show that RL-Co outperforms real-only fine-tuning and SFT-based co-training, improving real-world success, robustness to distribution shifts, and real-world data efficiency. Additional comparisons with SFT on RL-generated rollouts further support the benefit of improving the policy through online simulation interaction. These results suggest that interactive simulation can unlock benefits that static imitation objectives alone cannot fully realize. 

## **7 Limitations** 

Our approach relies on constructing simulation environments, and the ManiSkill setup used in this work is limited to rigid-body simulation. Within this setting, we evaluate RL-Co on four tabletop tasks using a single robot embodiment, with two evaluation sessions per condition. More challenging tasks, complex environments, and different robot embodiments remain to be explored. Furthermore, the sim-to-real gap continues to limit real-world performance, and success rates remain below 100% in several settings despite the improvements achieved by RL-Co. Future work will address these limitations by broadening the simulation and evaluation settings and improving sim-to-real transfer. 

9 

### **Acknowledgments** 

This work was supported by National Natural Science Foundation of China (No. 62406159), Zhongguancun Academy (Grant No. C20250301), and Shenzhen Science and Technology Program (No. AI2026016). 

## **References** 

- [1] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- [2] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 

- [3] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [4] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, et al. _pi_ ~~0~~ : A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [5] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, et al. _pi_ _~~{~~_ 0 _._ 5 _}_ : a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- [6] O. M. Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- [7] A. O’Neill, A. Rehman, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903. IEEE, 2024. 

- [8] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 

- [9] H. R. Walke, K. Black, T. Z. Zhao, Q. Vuong, C. Zheng, P. Hansen-Estruch, A. W. He, V. Myers, M. J. Kim, M. Du, et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pages 1723–1736. PMLR, 2023. 

- [10] M. J. Kim, C. Finn, and P. Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- [11] S. Zhang, Z. Xu, P. Liu, X. Yu, Y. Li, Q. Gao, Z. Fei, Z. Yin, Z. Wu, Y.-G. Jiang, et al. Vlabench: A large-scale benchmark for language-conditioned robotics manipulation with long-horizon reasoning tasks. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 11142–11152, 2025. 

- [12] J. Liu, F. Gao, B. Wei, X. Chen, Q. Liao, Y. Wu, C. Yu, and Y. Wang. What can rl bring to vla generalization? an empirical study. _arXiv preprint arXiv:2505.19789_ , 2025. 

- [13] E. Todorov, T. Erez, and Y. Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ international conference on intelligent robots and systems_ , pages 5026–5033. IEEE, 2012. 

10 

- [14] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa, et al. Isaac gym: High performance gpu-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 

- [15] S. Tao, F. Xiang, A. Shukla, Y. Qin, X. Hinrichsen, X. Yuan, C. Bao, X. Lin, Y. Liu, T.-k. Chan, et al. Maniskill3: Gpu parallelized robotics simulation and rendering for generalizable embodied ai. _arXiv preprint arXiv:2410.00425_ , 2024. 

- [16] J. Tobin, R. Fong, A. Ray, J. Schneider, W. Zaremba, and P. Abbeel. Domain randomization for transferring deep neural networks from simulation to the real world. In _2017 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ , pages 23–30. IEEE, 2017. 

- [17] X. B. Peng, M. Andrychowicz, W. Zaremba, and P. Abbeel. Sim-to-real transfer of robotic control with dynamics randomization. In _2018 IEEE international conference on robotics and automation (ICRA)_ , pages 3803–3810. IEEE, 2018. 

- [18] O. M. Andrychowicz, B. Baker, M. Chociej, R. Jozefowicz, B. McGrew, J. Pachocki, A. Petron, M. Plappert, G. Powell, A. Ray, et al. Learning dexterous in-hand manipulation. _The International Journal of Robotics Research_ , 39(1):3–20, 2020. 

- [19] M. Torne, A. Simeonov, Z. Li, A. Chan, T. Chen, A. Gupta, and P. Agrawal. Reconciling reality through simulation: A real-to-sim-to-real approach for robust manipulation, 2024. URL `https://arxiv.org/abs/2403.03949` . 

- [20] Y. Wu, L. Pan, W. Wu, G. Wang, Y. Miao, F. Xu, and H. Wang. Rl-gsbridge: 3d gaussian splatting based real2sim2real method for robotic manipulation learning. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 192–198. IEEE, 2025. 

- [21] K. Zhang, S. Sha, H. Jiang, M. Loper, H. Song, G. Cai, Z. Xu, X. Hu, C. Zheng, and Y. Li. Realto-sim robot policy evaluation with gaussian splatting simulation of soft-body interactions. _arXiv preprint arXiv:2511.04665_ , 2025. 

- [22] X. Li, J. Li, Z. Zhang, R. Zhang, F. Jia, T. Wang, H. Fan, K.-K. Tseng, and R. Wang. Robogsim: A real2sim2real robotic gaussian splatting simulator. _arXiv preprint arXiv:2411.11839_ , 2024. 

- [23] S. Cheng, L. Ma, Z. Chen, A. Mandlekar, C. Garrett, and D. Xu. Generalizable domain adaptation for sim-and-real policy co-training. _arXiv preprint arXiv:2509.18631_ , 2025. 

- [24] J. Yang, C. Finn, and D. Sadigh. Invariance co-training for robot visual generalization. _arXiv preprint arXiv:2512.05230_ , 2025. 

- [25] A. Yu, A. Foote, R. Mooney, and R. Mart´ın-Mart´ın. Natural language can help bridge the sim2real gap. _arXiv preprint arXiv:2405.10020_ , 2024. 

- [26] Y. Lei, M. Liu, A. Maddukuri, Z. Jiang, and Y. Zhu. A mechanistic analysis of sim-and-real co-training in generative robot policies, 2026. URL `https://arxiv.org/abs/2604.13645` . 

- [27] A. Maddukuri, Z. Jiang, L. Y. Chen, S. Nasiriany, Y. Xie, Y. Fang, W. Huang, Z. Wang, Z. Xu, N. Chernyadev, et al. Sim-and-real co-training: A simple recipe for vision-based robotic manipulation. _arXiv preprint arXiv:2503.24361_ , 2025. 

- [28] A. Wei, A. Agarwal, B. Chen, R. Bosworth, N. Pfaff, and R. Tedrake. Empirical analysis of sim-and-real cotraining of diffusion policies for planar pushing from pixels. _arXiv preprint arXiv:2503.22634_ , 2025. 

- [29] S. Ross, G. Gordon, and D. Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ , pages 627–635. JMLR Workshop and Conference Proceedings, 2011. 

11 

- [30] T. Osa, J. Pajarinen, G. Neumann, J. A. Bagnell, P. Abbeel, and J. Peters. An algorithmic perspective on imitation learning. _Foundations and Trends® in Robotics_ , 7(1-2):1–179, 2018. 

- [31] G. Dulac-Arnold, D. Mankowitz, and T. Hester. Challenges of real-world reinforcement learning. _arXiv preprint arXiv:1904.12901_ , 2019. 

- [32] Y. Zhu, Z. Wang, J. Merel, A. Rusu, T. Erez, S. Cabi, S. Tunyasuvunakool, J. Kram´ar, R. Hadsell, N. de Freitas, et al. Reinforcement and imitation learning for diverse visuomotor skills. _arXiv preprint arXiv:1802.09564_ , 2018. 

- [33] A. Rajeswaran, V. Kumar, A. Gupta, G. Vezzani, J. Schulman, E. Todorov, and S. Levine. Learning complex dexterous manipulation with deep reinforcement learning and demonstrations. In _Robotics: Science and Systems XIV_ , 2018. doi:10.15607/RSS.2018.XIV.049. URL `https://arxiv.org/abs/1709.10087` . 

- [34] S. Fujimoto and S. S. Gu. A minimalist approach to offline reinforcement learning. In _Advances in Neural Information Processing Systems_ , 2021. 

- [35] Y. Lu, J. Fu, G. Tucker, X. Pan, E. Bronstein, B. Roelofs, B. Sapp, A. Faust, S. Whiteson, B. White, D. Anguelov, and S. Levine. Imitation is not enough: Robustifying imitation with reinforcement learning for challenging driving scenarios. In _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 7553–7560, 2023. doi:10.1109/ IROS55552.2023.10342038. 

- [36] Q. Li, Z. Zhou, and S. Levine. Reinforcement learning with action chunking. In _Advances in Neural Information Processing Systems_ , 2025. URL `https://arxiv.org/abs/2507. 07969` . 

- [37] J. Zhang, Y. Luo, A. Anwar, S. A. Sontakke, J. J. Lim, J. Thomason, E. Biyik, and J. Zhang. Rewind: Language-guided rewards teach robot policies without new demonstrations. In _Conference on Robot Learning_ , 2025. URL `https://arxiv.org/abs/2505.10911` . 

- [38] H. Li, Y. Zuo, J. Yu, Y. Zhang, Z. Yang, K. Zhang, X. Zhu, Y. Zhang, T. Chen, G. Cui, et al. Simplevla-rl: Scaling vla training via reinforcement learning. _arXiv preprint arXiv:2509.09674_ , 2025. 

- [39] T. Zhang, C. Yu, S. Su, and Y. Wang. Reinflow: Fine-tuning flow matching policy with online reinforcement learning. _arXiv preprint arXiv:2505.22094_ , 2025. 

- [40] Y. Zhang, S. Yu, T. Zhang, M. Guang, H. Hui, K. Long, Y. Wang, C. Yu, and W. Ding. Sac flow: Sample-efficient reinforcement learning of flow-based policies via velocity-reparameterized sequential modeling. _arXiv preprint arXiv:2509.25756_ , 2025. 

- [41] H. Zang, M. Wei, S. Xu, Y. Wu, Z. Guo, Y. Wang, H. Lin, P. Wang, H. Yuan, Y. Zhang, L. Shi, Y. Xie, Z. Xu, Z. Liu, K. Chen, W. Tang, Q. Zhang, W. Zhang, C. Yu, and Y. Wang. RLuxVLA: A Unified and Efficient Framework for Reinforcement Learning of Vision-LanguageAction Models. In _Proceedings of Robotics: Science and Systems_ , Sydney, Australia, July 2026. doi:10.15607/RSS.2026.XXII.089. 

- [42] D. Kalashnikov, A. Irpan, P. Pastor, J. Ibarz, A. Herzog, E. Jang, D. Quillen, E. Holly, M. Kalakrishnan, V. Vanhoucke, and S. Levine. Qt-opt: Scalable deep reinforcement learning for vision-based robotic manipulation, 2018. URL `https://arxiv.org/abs/1806.10293` . 

- [43] H. Zang, S. Yu, H. Lin, T. Zhou, Z. Huang, Z. Guo, X. Xu, Y. Sheng, J. Zhou, S. Zhang, F. Gao, W. Tang, Y. Yue, Q. Zhang, X. Chen, C. Yu, and Y. Wang. USER: A Unified and Extensible System for Online Real-World Policy Learning in Embodied AI. In _Proceedings of Robotics: Science and Systems_ , Sydney, Australia, July 2026. doi:10.15607/RSS.2026.XXII.037. 

12 

- [44] J. Luo, Z. Hu, C. Xu, Y. L. Tan, J. Berg, A. Sharma, S. Schaal, C. Finn, A. Gupta, and S. Levine. Serl: A software suite for sample-efficient robotic reinforcement learning. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 16961–16969. IEEE, 2024. 

- [45] A. Wagenmaker, M. Nakamoto, Y. Zhang, S. Park, W. Yagoub, A. Nagabandi, A. Gupta, and S. Levine. Steering your diffusion policy with latent space reinforcement learning. _arXiv preprint arXiv:2506.15799_ , 2025. 

- [46] K. Lei, H. Li, D. Yu, Z. Wei, L. Guo, Z. Jiang, Z. Wang, S. Liang, and H. Xu. RL100: Performant robotic manipulation with real-world reinforcement learning. _arXiv preprint arXiv:2510.14830_ , 2025. 

- [47] P. Intelligence, A. Amin, R. Aniceto, A. Balakrishna, K. Black, K. Conley, G. Connors, J. Darpinian, K. Dhabalia, J. DiCarlo, et al. _π_ 0<sup>_∗_</sup> _._ 6<sup>:avlathatlearnsfromexperience.</sup><sup>_arXiv_</sup> _preprint arXiv:2511.14759_ , 2025. 

- [48] C. Xu, J. T. Springenberg, M. Equi, A. Amin, A. Esmail, S. Levine, and L. Ke. RL Token: Bootstrapping online RL with vision-language-action models. _arXiv preprint arXiv:2604.23073_ , 2026. 

- [49] J. Hu, R. Hendrix, A. Farhadi, A. Kembhavi, R. Martin-Martin, P. Stone, K.-H. Zeng, and K. Ehsani. Flare: Achieving masterful and adaptive robot policies with large-scale reinforcement learning fine-tuning. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 3617–3624, 2025. doi:10.1109/ICRA55743.2025.11128318. URL `https://arxiv.org/abs/2409.16578` . 

- [50] K. Chen, Z. Liu, T. Zhang, Z. Guo, S. Xu, H. Lin, H. Zang, X. Li, Q. Zhang, Z. Yu, G. Fan, T. Huang, Y. Wang, and C. Yu. _π_ `RL` : Online rl fine-tuning for flow-based vision-language-action models, 2026. URL `https://arxiv.org/abs/2510.25889` . 

- [51] L. Ankile, A. Simeonov, I. Shenfeld, M. Torne, and P. Agrawal. From imitation to refinementresidual rl for precise assembly. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 01–08. IEEE, 2025. 

- [52] W. Xiao, H. Lin, A. Peng, H. Xue, T. He, Z. Luo, Y. Xie, F. Hu, J. Fan, G. Shi, et al. Selfimproving vision-language-action models with data generation via residual RL. In _International Conference on Learning Representations_ , volume 2026, pages 13209–13236, 2026. 

- [53] B. Eysenbach, S. Asawa, S. Chaudhari, S. Levine, and R. Salakhutdinov. Off-dynamics reinforcement learning: Training for transfer with domain classifiers. In _International Conference on Learning Representations_ , 2021. URL `https://arxiv.org/abs/2006.13916` . 

- [54] P. Yin, T. Westenbroek, C.-A. Cheng, A. Kolobov, and A. Gupta. Rapidly adapting policies to the real-world via simulation-guided fine-tuning. In _International Conference on Learning Representations_ , 2025. URL `https://proceedings.iclr.cc/paper_files/paper/ 2025/hash/e68274fc4f158dbcbd4dddc672f7ee9c-Abstract-Conference.html` . 

- [55] P. Daoudi, C. Prieur, B. Robu, M. Barlier, and L. D. Santos. A conservative approach for few-shot transfer in off-dynamics reinforcement learning. In _Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence_ , pages 3890–3898, 2024. 

- [56] T. Lin, K. Sachdev, L. Fan, J. Malik, and Y. Zhu. Sim-to-real reinforcement learning for visionbased dexterous manipulation on humanoids, 2025. URL `https://arxiv.org/abs/2502. 20396` . Published at CoRL 2025. 

- [57] P. Yin, T. Westenbroek, Z. Zhang, I. Dagnino, E. Shilamkar, N. Mbiziwo-Tiapo, S. Bagaria, X. Liu, G. Mullins, A. Kolobov, et al. Emergent dexterity via diverse resets and large-scale reinforcement learning. In _International Conference on Learning Representations_ , volume 2026, pages 88343–88356, 2026. 

13 

- [58] A. Deshpande, M. Guru, R. Hendrix, S. Jauhri, A. Eftekhar, R. Tripathi, M. Argus, J. Salvador, H. Fang, M. Wallingford, et al. MolmoB0T: Large-scale simulation enables zero-shot manipulation. _arXiv preprint arXiv:2603.16861_ , 2026. 

- [59] Y. Chebotar, A. Handa, V. Makoviychuk, M. Macklin, J. Issac, N. Ratliff, and D. Fox. Closing the sim-to-real loop: Adapting simulation randomization with real world experience. In _2019 International Conference on Robotics and Automation (ICRA)_ , pages 8973–8979. IEEE, 2019. 

- [60] B. Mehta, M. Diaz, F. Golemo, C. J. Pal, and L. Paull. Active domain randomization. In _Conference on Robot Learning_ , pages 1162–1176. PMLR, 2020. 

- [61] A. Mandlekar, S. Nasiriany, B. Wen, I. Akinola, Y. Narang, L. Fan, Y. Zhu, and D. Fox. Mimicgen: A data generation system for scalable robot learning using human demonstrations. _arXiv preprint arXiv:2310.17596_ , 2023. 

- [62] C. Garrett, A. Mandlekar, B. Wen, and D. Fox. SkillMimicGen: Automated demonstration generation for efficient skill learning and deployment. _arXiv preprint arXiv:2410.18907_ , 2024. 

- [63] Z. Jiang, Y. Xie, K. Lin, Z. Xu, W. Wan, A. Mandlekar, L. Fan, and Y. Zhu. DexMimicGen: Automated data generation for bimanual dexterous manipulation via imitation learning. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 

- [64] C. Dai, H. Chang, A. Nisal, R. Kumar, G. Chen, T. Chen, Y. Qin, and G. Shi. PGDG: Physically grounded data generation for robust bimanual policy learning from a single demonstration. _arXiv preprint arXiv:2605.21710_ , 2026. 

- [65] T. Chen, Z. Chen, B. Chen, Z. Cai, Y. Liu, Z. Li, Q. Liang, X. Lin, Y. Ge, Z. Gu, et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 

- [66] S. Nasiriany, A. Maddukuri, L. Zhang, A. Parikh, A. Lo, A. Joshi, A. Mandlekar, and Y. Zhu. Robocasa: Large-scale simulation of everyday tasks for generalist robots. _arXiv preprint arXiv:2406.02523_ , 2024. 

- [67] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [68] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, and W. Chen. LoRA: Low-rank adaptation of large language models. In _International Conference on Learning Representations_ , 2022. URL `https://openreview.net/forum?id=nZeVKeeFYf9` . 

- [69] C. Yu, Y. Wang, Z. Guo, H. Lin, S. Xu, H. Zang, Q. Zhang, Y. Wu, C. Zhu, J. Hu, et al. RLinf: Flexible and efficient Large-Scale reinforcement learning via Macro-to-Micro flow transformation. In _20th USENIX Symposium on Operating Systems Design and Implementation (OSDI 26)_ , pages 829–846, 2026. 

- [70] NVIDIA, :, A. Ali, J. Bai, M. Bala, Y. Balaji, A. Blakeman, T. Cai, J. Cao, T. Cao, E. Cha, Y.-W. Chao, P. Chattopadhyay, M. Chen, Y. Chen, Y. Chen, S. Cheng, Y. Cui, J. Diamond, Y. Ding, J. Fan, L. Fan, L. Feng, F. Ferroni, S. Fidler, X. Fu, R. Gao, Y. Ge, J. Gu, A. Gupta, S. Gururani, I. E. Hanafi, A. Hassani, Z. Hao, J. Huffman, J. Jang, P. Jannaty, J. Kautz, G. Lam, X. Li, Z. Li, M. Liao, C.-H. Lin, T.-Y. Lin, Y.-C. Lin, H. Ling, M.-Y. Liu, X. Liu, Y. Lu, A. Luo, Q. Ma, H. Mao, K. Mo, S. Nah, Y. Narang, A. Panaskar, L. Pavao, T. Pham, M. Ramezanali, F. Reda, S. Reed, X. Ren, H. Shao, Y. Shen, S. Shi, S. Song, B. Stefaniak, S. Sun, S. Tang, S. Tasmeen, L. Tchapmi, W.-C. Tseng, J. Varghese, A. Z. Wang, H. Wang, H. Wang, H. Wang, T.-C. Wang, F. Wei, J. Xu, D. Yang, X. Yang, H. Ye, S. Ye, X. Zeng, J. Zhang, Q. Zhang, K. Zheng, A. Zhu, and Y. Zhu. World simulation with video foundation models for physical ai, 2026. URL `https://arxiv.org/abs/2511.00062` . 

14 

- [71] X. Wei, M. Liu, Z. Ling, and H. Su. Approximate convex decomposition for 3d meshes with collision-aware concavity and tree search. _ACM Transactions on Graphics (TOG)_ , 41(4):1–18, 2022. doi:10.1145/3528223.3530183. URL `https://arxiv.org/abs/2205.02961` . 

- [72] I. Loshchilov and F. Hutter. Decoupled weight decay regularization. _arXiv preprint arXiv:1711.05101_ , 2017. 

15 

## **Appendix** 

## **A Detailed Problem Setup and Post-Training Objectives** 

### **A.1 Problem Formulation** 

We consider a two-domain robotic manipulation setting with a real-world task domain _T_ real and a corresponding simulation task domain _T_ sim. The simulation environment is designed to match the real-world setup at the task level while allowing scalable data collection through interaction. 

We model both the real-world task and its simulated counterpart as Partially Observable Markov Decision Processes (POMDPs), denoted by the tuple 


where Ω _∈{_ real _,_ sim _}_ indicates whether the process corresponds to the real-world or simulation task. 

Following the formulation in Maddukuri et al. [27], we define each component as follows: 

- _S_ Ω and _O_ Ω denote the state space of the robot-environment system and the observation space induced by onboard sensors, respectively. While the real and simulated tasks operate in different environments, they share the same robot embodiment and sensing modalities. 

- _A_ is the robot action space. Both tasks adopt an identical control interface and action parameterization. 

- _P_ Ω represents the state transition dynamics, where _st_ +1 _∼P_ Ω( _· | st, at_ ). Due to the inherent difficulty of perfectly modeling real-world physics, the transition dynamics in simulation may exhibit slight discrepancies from those in the real environment. 

- _L_ denotes the natural language instruction specifying the task goal. For corresponding real and simulated tasks, the language instruction remains identical. 

- _R_ is the reward function, defined as _R_ ( _s, l_ ), which evaluates task progress based on the current state and the given language instruction. 

- _P_ ( _s_ 0) is the distribution over initial states, from which _s_ 0 _∼ P_ ( _s_ 0) is sampled. The real and simulated tasks share the same initial state distribution. 

- _γ ∈_ (0 _,_ 1) is the discount factor. 

Under this formulation, we define a vision-language-action (VLA) policy _πθ_ that conditions on the most recent _H_ observations _o_<sup>_t_</sup> Ω<sup>_−H_+1:</sup><sup>_t_</sup> and the language instruction _l_ to predict a sequence of future actions over a horizon of length _h_ : 


### **A.2 Fine-Tuning on Vision-Language-Action Models** 

We consider post-training of vision-language-action (VLA) models under both supervised and reinforcement learning paradigms. Given a pre-trained VLA policy _πθ_ , fine-tuning aims to adapt the policy to a specific manipulation task by leveraging either expert demonstrations or online interaction with the environment. 

### **A.2.1 Supervised Fine-Tuning (SFT)** 

Given an expert-collected demonstration dataset _DT_ = _{_ ( _τ_<sup>(</sup><sup>_i_)</sup> _, l_<sup>(</sup><sup>_i_)</sup> ) _}_<sup>_N_</sup> _i_ =1<sup>,eachtrajectory</sup><sup>_τ_(</sup><sup>_i_)=</sup> _{_ ( _o_<sup>(</sup> _j_<sup>_i_)</sup><sup>_, a_(</sup> _j_<sup>_i_))</sup><sup>_}K_</sup> _j_ =1<sup>_i_consistsofpairedobservationsandactions,and</sup><sup>_l_(</sup><sup>_i_)denotesthecorresponding</sup> natural language instruction. Here, _N_ is the total number of trajectories and _Ki_ is the length of the _i_ -th trajectory. 

16 

Supervised fine-tuning optimizes the VLA policy _πθ_ by minimizing the discrepancy between predicted and expert actions: 


where 


denotes the predicted action chunk of horizon _h_ , and 


is the corresponding expert action sequence. 

The loss function _ℓ_ SFT depends on the specific VLA architecture and action representation. Common choices include next-token prediction losses [3], _L_ 1 regression losses for continuous actions [10], and diffusion-based denoising objectives [4]. 

### **A.2.2 Reinforcement Learning (RL) Fine-Tuning** 

Reinforcement learning fine-tuning seeks to further optimize the policy through interaction with the environment by maximizing the expected discounted return: 


where actions are sampled from the VLA policy _at ∼ πθ_ ( _· | ot, l_ ) and state transitions follow _st_ +1 _∼P_ ( _st, at_ ). 

Due to differences in action representations and generative mechanisms, the concrete realization of RL fine-tuning varies across VLA architectures. Nevertheless, existing RL fine-tuning approaches share a common structure: an iterative loop of environment interaction for trajectory collection, followed by policy updates guided by reward feedback. Our method builds upon this general framework and introduces an additional supervised fine-tuning objective on real-world data during the policy update phase, which is compatible with a wide range of RL fine-tuning strategies. 

## **B Dataset Generation Details** 

### **B.1 Real-World Demonstrations** 

For all four tasks, we collect expert demonstrations via human teleoperation using a 3D SpaceMouse. Each trajectory starts from the same initial conditions as evaluation: the robot is reset to a fixed configuration, while task-relevant objects are randomly placed on the table. Expert actions are recorded as end-effector delta control commands. For each task, we collect 20–50 successful trajectories, forming the real-world dataset _D_ real. 

### **B.2 Simulation Dataset Generation** 

To scale up training data in simulation, we adopt MimicGen [61] to generate large numbers of successful trajectories. Instead of collecting teleoperated demonstrations directly in simulation, we replay real-world expert trajectories in ManiSkill and use them as seed trajectories for data generation, thereby grounding the simulation data in real-world behaviors. 

We implement the MimicGen pipeline within ManiSkill and introduce a minor modification: for each seed trajectory, we retain only task-relevant key stages and remove long segments of free-space end-effector motion. This pruning encourages smoother and more efficient generated trajectories. For each task, we generate 1,000 successful trajectories, which together form the simulation dataset _D_ sim. 

17 

## **C Real-world Environment Setup** 

Fig. 7 illustrates our real-world evaluation setup. The system consists of a table-top workspace, a Franka Emika Panda robot mounted on the table, and a fixed RGB camera. We use the RGB channels captured by the camera as the visual input to the VLA model. 


Figure 7: **Real-world Setup.** The real-world evaluation platform includes a tabletop workspace, a Franka Panda robotic manipulator fixed to the table, and a RGB camera for visual perception. All objects are positioned on the table surface. 

The robot is equipped with seven actuated joints and a parallel-jaw gripper with open/close capability. Control is performed in an end-effector delta-pose space: at each timestep, we command a relative end-effector pose with respect to the current pose, and compute the corresponding joint updates using inverse kinematics (IK). The translational components are specified in the robot base frame, while the rotational components are represented as roll–pitch–yaw (RPY) angles relative to the current end-effector orientation. Gripper actuation is controlled separately using a binary open/close signal. Overall, the action space is 7-dimensional. 

## **D Evaluation Details** 

### **D.1 Evaluation Sessions and Statistical Interpretation** 

Here we present our evaluation protocol. For each checkpoint, we conduct two separate evaluation sessions. Each session contains 32 trials for `Pick and Place` , 30 for `Push Cube` , 10 for `Open Drawer` , and 10 for `Close Drawer` , giving 64, 60, 20, and 20 trials in total, respectively. 

Let _kt,s_ be the number of successes for task _t_ in session _s ∈{_ 1 _,_ 2 _}_ , and let _nt_ be the number of trials in that session. Define _rt,s_ = 100 _kt,s/nt_ . The reported task mean and population standard deviation are 


For example, the OpenVLA real-only policy succeeds in 2 _/_ 32 `Pick and Place` trials in each session, yielding 6 _._ 25% _±_ 0% before rounding. The zero standard deviation reflects identical success rates in the two sessions. For the average across the four tasks, we first compute _as_ =<sup><u>1</u></sup> 4 �4 _t_ =1<sup>_rt,s_</sup> and then apply the same mean and standard deviation calculation across the two _as_ . Thus tasks have equal weight despite different trial counts. Aggregates are computed before rounding. 

The standard deviations summarize session-level evaluation variability for the selected checkpoints. Estimating training-seed variance and establishing per-task confidence require additional independently trained policies and larger evaluations. Trial-level pooling and paired comparisons depend on 

18 


Figure 8: **Visualization of Four Tabletop Manipulation Tasks.** For each task, we present one successful trajectory and uniformly sample seven frames along the execution. Each row corresponds to a single trajectory shown from start to completion. 

the independence and matching of the recorded initial conditions. These considerations define the statistical scope of the current results. 

### **D.2 Visualization of All Tasks** 

Fig. 8 visualizes the four table-top manipulation tasks evaluated in our experiments. `Pick and Place` requires the robot to grasp an object from the table and place it into a bowl. `Push Cube` involves pushing one cube out of three candidates with different colors according to a language instruction. `Open Drawer` requires opening a closed drawer placed on the table, while `Close Drawer` requires closing an initially opened drawer. 

### **D.3 Manipulated Objects** 

Fig. 9 shows the manipulated objects used in both simulation and real-world experiments. The detailed settings are summarized below: 

- `Pick and Place` : In simulation, we use the same set of 25 objects as in the environment proposed by Liu et al. [12]. In the real world, objects are divided into two categories: regularshaped and irregular-shaped. Regular-shaped objects consist of toy fruits and vegetables, while irregular-shaped objects include bowls and gloves. Notably, irregular-shaped objects are not included in the real-world expert demonstrations. For in-distribution evaluation, we select four regular-shaped objects for testing. 

- `Push Cube` : In simulation, we train on five colored cubes, as shown in Fig. 9. In the real-world setup, we also use five colors. However, expert demonstrations are collected only for three colors (purple, yellow, and pink), while orange and green cubes are excluded from the demonstration data. During evaluation, three colors are randomly selected from the five available colors. 

- `Open/Close Drawer` : In the real world, we use the drawer shown in Fig. 9. In simulation, we construct a corresponding URDF model with matched geometric proportions. 

### **D.4 Objects Initial States** 

Fig. 10 illustrates the randomized regions for the four real-world tasks. The detailed configurations are as follows: 

19 


Figure 9: **Manipulated Objects in Simulation and the Real World.** The left panel shows the objects used in simulation, while the right panel presents the real-world objects. All simulated objects are used during training. The real-world objects are divided into training objects and unseen objects for generalization evaluation. 

- `Pick and Place` : The bowl is randomly placed within a 10 _×_ 20 cm rectangular region, indicated by the orange area in Fig. 10. For each episode, one object is selected from a predefined object set, and its center is randomly placed within a 20 _×_ 25 cm rectangular region, indicated by the blue area in Fig. 10. To facilitate controlled evaluation, both the bowl and object regions are discretized into grids with a minimum resolution of 5 cm. All objects are placed on grid points, and the same set of initial configurations is used across different methods. 

- `Push Cube` : For each evaluation episode, three cubes are randomly selected from all available colors and randomly ordered. The cubes are initially placed with a spacing of 15 cm, followed by a random perturbation within a 5 _×_ 5 cm region, as indicated by the orange area in Fig. 10. The language instruction specifies one of the three colors. All experiments follow the same color permutations and spatial configurations. 

- `Open Drawer` : The front edge of the closed drawer is placed within the orange region shown in Fig. 10, with the drawer orientation initially aligned parallel to the short edge of the table. A random rotational perturbation of up to 15<sup>_◦_</sup> is then applied. We uniformly sample 10 predefined initial configurations, which are shared across all evaluations. 

- `Close Drawer` : Similar to `Open Drawer` , the drawer is initially opened by approximately 10 cm, and its front edge is placed within the same orange region with up to 15<sup>_◦_</sup> of rotational perturbation. The same set of 10 predefined configurations is used for evaluation to ensure fair comparison. 

### **D.5 Robot Initial State** 

Unless otherwise specified, the Franka Emika Panda robot is initialized in a fixed default configuration across all experiments, as shown in Fig. 7. Here we describe additional robot initial states used in the generalization experiments. Specifically, we focus on the `Pick and Place` task and select four representative objects, each with a fixed object initialization. For each object, we perturb the robot tool center point (TCP) by applying a rotation of _±_ 30<sup>_◦_</sup> around the vertical axis, together with a translational offset of 5 cm along a single Cartesian direction. The perturbations include forward, backward, leftward, rightward, and upward translations, resulting in five distinct perturbed initial states. Each perturbation combines one directional translation with the corresponding rotational off- 

20 


Figure 10: **Initial Regions for Manipulative Objects.** For the `Pick and Place` task, the bowl is placed within the orange region, while the objects are initialized in the blue region. For the `Push Cube` task, each cube is initialized within its corresponding orange region. For the `Open / Close Drawer` tasks, the front edge of the drawer is initialized within the orange region. 

|**Perturbation ID**|**Translation (cm)**|**Rotation (deg)**|
|---|---|---|
|P1|(+5_,_ 0_,_ 0)(forward)|+30<sup>_◦_</sup>|
|P2|(_−_5_,_ 0_,_ 0)(backward)|_−_30<sup>_◦_</sup>|
|P3|(0_,_ +5_,_ 0)(left)|+30<sup>_◦_</sup>|
|P4|(0_, −_5_,_ 0)(right)|_−_30<sup>_◦_</sup>|
|P5|(0_,_ 0_,_ +5)(upward)|+30<sup>_◦_</sup>|


Table 3: **Robot initial state perturbations applied to the TCP in the** `Pick and Place` **task.** Translations are defined in the world frame, and rotations are applied around the vertical ( _z_ ) axis. 

set. These perturbations are summarized in Table 3. All other aspects of the environment and policy remain unchanged. 

### **D.6 Success Criteria and Failure Modes** 

In all real-world evaluations, we use the same sampled initial configurations across methods and judge task success according to task completion rather than intermediate motion quality. The taskspecific criteria are: 

- `Pick and Place` : An episode is successful only if the robot grasps the target object and releases it inside the bowl. Failure cases include missing the grasp, dropping the object before reaching the bowl, or placing the object outside the bowl. 

- `Push Cube` : An episode is successful if the robot pushes the cube specified by the language instruction forward. Pushing an incorrect cube or failing to make effective contact with the instructed cube is counted as failure. 

- `Open Drawer` : An episode is successful if the robot grasps or makes stable contact with the drawer handle and pulls the drawer open beyond the task threshold. Common failures include missing the handle, losing contact during pulling, or pulling in a direction that does not open the drawer sufficiently. 

21 

- `Close Drawer` : An episode is successful if the robot pushes the opened drawer back to the closed state. Failures typically occur when the robot contacts an ineffective part of the drawer, pushes in an incorrect direction, or stops before the drawer is fully closed. 

## **E Simulation Training** 

### **E.1 Simulation Fidelity and Sim–Real Alignment** 

**Visual and task-level alignment.** We first fixed the real robot, table, camera, and task workspace, and then built the simulator from approximate measurements of that setup. Our simulation environments are constructed in ManiSkill [15] to preserve the task-relevant structure of the corresponding real-world setups. The simulated and real environments share the same robot embodiment, endeffector action interface, task semantics, object-level spatial layouts, and camera viewpoint used by the VLA policy. We manually tune the simulated camera extrinsics so that the rendered third-person view approximately matches the fixed RGB camera used in real-world deployment. We also align the table placement, robot mounting pose, task workspace, and high-level object arrangements so that the simulated rollouts expose the policy to interaction patterns that are meaningful for the real task. 

We do not assume that the simulator is a photorealistic or fully accurate digital twin. Object identities, materials, textures, lighting, and background appearance are not precisely matched between simulation and the real world. This choice is intentional: our goal is not to demonstrate zero-shot transfer from a high-fidelity simulator, but to test whether imperfect yet task-relevant simulation can provide useful closed-loop interaction when the policy is anchored by real-world demonstrations. The visual gap is therefore handled by the real-data supervision in both stages of RL-Co, rather than by requiring exact visual reconstruction. 

**Physics abstraction.** For physics, we use rigid-body simulation in ManiSkill. Simulated objects are imported from mesh files, and their collision geometries are approximated by convex hulls computed with CoACD [71]. This abstraction is sufficient for representing the dominant contacts in our tabletop tasks, but it does not fully capture all real-world effects such as soft-object deformation, small unmodeled contacts, or friction variations. Thus, we view the simulator as a task-level interaction environment rather than a complete physical replica. 

**Robot controller system identification.** To better align the low-level robot response, we perform a lightweight system identification step for the Franka controller. We first collect one teleoperated real-world trajectory containing the commanded 7-DoF actions and the corresponding tool-centerpoint (TCP) trajectory. We then replay the same action sequence in simulation and optimize the simulated Franka joint stiffness and damping parameters using simulated annealing. After tuning, the simulated TCP trajectory stays within approximately 2 cm of the real TCP trajectory over the replayed sequence. All other simulator parameters remain at their default ManiSkill values. 

These choices follow the practical importance of viewpoint alignment in prior sim-real cotraining [27] and of physical correspondence in planar pushing [28]. Approximate task geometry and camera/controller alignment define our evaluated setup. The approximately 2 cm TCP error characterizes controller replay on the calibration trajectory. Systematic perturbations of geometry, camera pose, and controller parameters would further characterize the transfer tolerance of each component. 

### **E.2 Reward Function Design** 

We detail the reward function design for each simulation task in this section. 

- `Pick and Place` : This task is decomposed into two sequential stages: _grasping_ and _placing_ , which are indicated by the binary states `is` ~~`g`~~ `rasped` and `is` ~~`p`~~ `laced` , respectively. We design two types of reward functions: a dense reward and a sparse reward. The dense reward is defined 

22 

as 


where Igrasped and Isuccess are indicator functions denoting whether the object has been successfully grasped and placed, respectively. The shaping term _Rd_ ( _x_ ) = 1 _−_ tanh(10 _x_ ) provides a smooth distance-based reward that asymptotically approaches 1 as the distance decreases. Here, _d_ 1 and _d_ 2 denote the distance between the gripper and the object, and the distance between the object and the target container, respectively. For the sparse reward, we assign a reward of 0 _._ 2 at the moment when grasping succeeds, and a reward of 1 upon successful placement. If the object leaves the target container after a successful placement due to external disturbances, a penalty of _−_ 0 _._ 4 is applied. All other timesteps receive zero reward. We use dense reward when training OpenVLA and use sparse reward when training _π_ 0 _._ 5. 

- `Push Cube` : The objective of this task is to push a designated target cube into a predefined goal region on the table. The dense reward consists of three components. First, a _reaching reward_ encourages the Tool Center Point (TCP) to approach a pre-defined pushing pose behind the cube along the pushing direction: 


where **p** push is defined as a point offset from the cube center by one half cube length plus a small margin along the pushing axis. Second, once the TCP is sufficiently close to the pushing pose, a _placement reward_ is activated to encourage the cube to move toward the goal region: 


where only planar ( _x, y_ ) distances are considered. This term is gated by a proximity condition to ensure that the agent first establishes contact before being rewarded for object motion. Finally, a sparse _success bonus_ is assigned once the cube is pushed beyond the goal center along the pushing direction and remains within a tolerance band orthogonal to it: 


- `Open Drawer` : In this task, the reward is defined over three stages corresponding to reaching, opening progress, and task completion. First, a reaching reward encourages the TCP to approach the drawer handle: 


- Second, an _opening reward_ is defined based on the normalized drawer joint position (open fraction): 


where the open fraction is computed by linearly normalizing the drawer joint position between its minimum and maximum limits. Once the drawer begins to open, the reaching reward is saturated to a constant value to avoid conflicting gradients. The total dense reward is given by: 


A terminal success reward of 5 _._ 0 is assigned when the drawer is opened beyond a high openfraction threshold (e.g., 90% of its range). 

- `Close Drawer` : The Close Drawer task is initialized from an open state and rewards progress toward closing the drawer. Instead of absolute position, we define a _progress-based reward_ using the change in open fraction between consecutive time steps: 

∆= open ~~f~~ rac _t−_ 1 _−_ open ~~f~~ rac _t._ (17) 

The dense reward is then computed as: 


where _α_ is a scaling factor for closing progress and _β_ is a small time penalty that encourages faster completion. Once the drawer is closed below a predefined threshold on the open fraction, a terminal success reward of 5 _._ 0 is issued and overrides the dense shaping terms. 

For all tasks, dense rewards are normalized by their respective maximum achievable reward values to ensure comparable reward scales across tasks during multi-task training. 

23 


Figure 11: **Simulation Training Results.** We report the simulation success rates across all settings during RL training. 

### **E.3 Performance in Simulation during RL Training** 

Interaction budgets are fixed within each model–task configuration but differ across configurations. Task horizons, reward sparsity, exploration difficulty, and parallel rollout configurations all affect the number of transitions and elapsed time. Appendix J reports elapsed-time curves for the four _π_ 0 _._ 5 runs and their hardware allocations. 

Fig. 11 shows the success rates of different models on each task in the simulation environment during RL training. After RL fine-tuning, all VLA models achieve substantial performance improvements in simulation compared to their pre-RL counterparts. 

## **F Additional Dexterous Evaluation** 

We further evaluate RL-Co on a more dexterous `Peg Insertion` task, which requires more precise contact and alignment than the tabletop tasks in the main experiments. As shown in Fig. 12, the robot starts by holding a 2 _×_ 2 _×_ 12 cm peg above a base with a 2 _._ 25 _×_ 2 _._ 25 cm square hole. At the beginning of each episode, the peg is initialized 1–5 cm above the hole, while the hole position is randomly perturbed in the horizontal plane. An episode is successful only if the robot inserts the peg into the hole. 

For this task, we collect 50 real-world demonstrations using human teleoperation and generate 500 simulated trajectories with motion planning. We compare SFT-based sim–real co-training with RLCo using the _π_ 0 _._ 5 backbone and the same real-world evaluation protocol. As shown in Table 4, RL-Co improves real-world success from 32 _._ 5% to 42 _._ 5%, suggesting that closed-loop simulation interaction can still provide additional gains in a more precision-demanding setting. 


Figure 12: **Execution sequence of the** `Peg Insertion` **task.** The robot must align the grasped peg with the square hole and insert it into the base. 

## **G Sim–Real Correlation During RL Co-Training** 

We additionally examine whether simulation performance provides a useful signal for real-world deployment during RL co-training. We focus on the _π_ 0 _._ 5 model on the `Pick and Place` and `Open Drawer` tasks. During Stage II RL co-training, we record the simulation success rate throughout 

24 

|Method|Real SR (%)|
|---|---|
|SFT-based sim–real co-training|32.5|
|**RL-Co (Ours)**|**42.5**|


Table 4: **Real-world success rate on the** `Peg Insertion` **task.** The task uses the _π_ 0 _._ 5 backbone, 50 real-world demonstrations, and 500 simulated trajectories. 

training and periodically evaluate intermediate checkpoints on the real robot. This analysis is intended to test whether the improvement observed in simulation corresponds to real-world improvement, rather than only reflecting simulator-specific artifacts. 

As shown in Fig. 13, the real-world success rate generally increases as the simulation success rate improves. This positive correlation supports our checkpoint-selection strategy based on simulation success convergence. At the same time, the correlation is not perfect, which is expected under imperfect sim–real alignment. We therefore use simulation convergence as a practical selection signal, while relying on real-world demonstrations in RL-Co to reduce domain drift during policy improvement. 


Figure 13: **Correlation between simulation and real-world success during RL co-training.** We evaluate intermediate checkpoints of _π_ 0 _._ 5 on the `Pick and Place` and `Open Drawer` tasks. Realworld performance generally improves together with simulation performance. 

## **H Additional Baselines and Ablations** 

We include additional comparisons on _π_ 0 _._ 5 for the `Pick and Place` task to evaluate alternative ways of using simulation data. These comparisons are not intended as a full benchmark suite, but as targeted tests of two natural alternatives to RL-Co: removing the two-stage initialization, and distilling a simulation expert into the VLA policy through supervised trajectories. 

### **H.1 One-Stage RL Co-Training** 

The first alternative removes Stage I task-specific SFT initialization and directly applies Stage II RL co-training to the pretrained VLA policy. During this one-stage variant, the supervised regularization term is computed on the mixture of real and simulated demonstrations, rather than only on real demonstrations. This design tests whether the SFT warm-up stage can be replaced by a single RL phase with an all-data SFT loss. 

The one-stage variant fails to acquire the task, achieving 0 _._ 0% real-world success and maintaining near-zero simulation success even after several million interaction steps, as shown in Fig. 14. This result indicates that the SFT initialization stage is not merely a convenience for faster training; it provides the task-level behavior prior required for subsequent RL optimization. This observation is consistent with the ablation in Section 5.3, where weakening the Stage I initialization also makes RL substantially less effective. 

25 


Figure 14: **Simulation success rate of one-stage RL co-training.** Without Stage I task-specific SFT initialization, the policy maintains near-zero success in simulation even after several million interaction steps. 

### **H.2 RialTo-Style Distillation** 

The second alternative follows the distillation motivation of RialTo-style real-to-sim-to-real pipelines [19]. We first train a simulation expert with RL, use the expert to generate 2,000 simulated trajectories, and then perform SFT co-training with these trajectories and the same 50 real-world demonstrations. This baseline evaluates whether simulation is better used as an expert trajectory generator rather than as an interactive environment for directly improving the VLA policy. 

The RialTo-style distillation baseline reaches 75 _._ 0% real-world success, outperforming standard SFT co-training but remaining below RL-Co. This result suggests that a strong simulation expert can provide useful supervised trajectories, but distilling the expert into the VLA policy through static trajectories does not fully replace direct closed-loop policy improvement. In contrast, RL-Co updates the VLA policy itself through reward-driven interaction while using real demonstrations to preserve deployable real-world behavior. 

|Method|Real SR (%)|
|---|---|
|One-stage RL co-training|0.0|
|RialTo-style distillation [19]|75.0|
|**RL-Co (Ours)**|**81.3**|


Table 5: **Additional baselines on** `Pick and Place` **with** _π_ 0 _._ 5 **.** Results are reported as real-world success rate without standard deviation because each additional baseline was evaluated once. 

### **H.3 Strong-Rollout SFT Control on Open Drawer** 

We extend the rollout-distillation comparison to `Open Drawer` with _π_ 0 _._ 5, where the main-table improvement over SFT co-training is largest. The additional SFT baseline combines the same 20 real demonstrations with 1 _._ 6 _×_ 10<sup>5</sup> simulation transitions collected by an RL policy. This approximately matches RL-Co’s combined MimicGen-generation and Stage II interaction budget. Table 6 shows that the stronger simulated data improve SFT from 10% to 20%, while RL-Co reaches 65%. 

|Training condition (_π_0_._5,`Open Drawer`)|Real SR (%)|
|---|---|
|SFT co-training with MimicGen demonstrations|10.0|
|SFT co-training with strong RL rollouts|20.0|
|RL-Co|65.0|


Table 6: Strong-rollout SFT control using the same 20 real demonstrations. 

26 

|Parameter Names|Setting|`Pick and Place`|`Push Cube`|`Open Drawer`|`Close Drawer`|
|---|---|---|---|---|---|
|General|Number of Real Demos|50|50|20|30|
|OpenVLA|Co-training ratio_α_<br>SFT learning rate<br>Regularization weight_β_<br>Actor learning rate<br>Critic learning rate|0.5<br>5_×_10<sup>_−_4</sup><br>0.1<br>10<sup>_−_4</sup><br>3_×_10<sup>_−_3</sup>|0.5<br>5_×_10<sup>_−_4</sup><br>0.01<br>10<sup>_−_4</sup><br>3_×_10<sup>_−_3</sup>|0.5<br>5_×_10<sup>_−_4</sup><br>0.01<br>10<sup>_−_4</sup><br>3_×_10<sup>_−_3</sup>|0.5<br>5_×_10<sup>_−_4</sup><br>0.01<br>10<sup>_−_4</sup><br>3_×_10<sup>_−_3</sup>|
|_π_0_._5|Co-Training Ratio_α_<br>SFT learning rate<br>SFT lr schedule<br>Regularization Weight_β_<br>Actor learning rate<br>Critic learning rate|0.5<br>2_._5_×_10<sup>_−_5</sup><br>Cosine Decay<br>1.0<br>4_×_10<sup>_−_6</sup><br>2_×_10<sup>_−_4</sup>|0.95<br>2_._5_×_10<sup>_−_5</sup><br>Cosine Decay<br>0.2<br>10<sup>_−_6</sup><br>2_×_10<sup>_−_4</sup>|0.95<br>2_._5_×_10<sup>_−_5</sup><br>Cosine Decay<br>1.0<br>4_×_10<sup>_−_6</sup><br>2_×_10<sup>_−_4</sup>|0.98<br>2_._5_×_10<sup>_−_5</sup><br>Cosine Decay<br>0.1<br>7_._91_×_10<sup>_−_6</sup><br>1_._55_×_10<sup>_−_4</sup>|


Table 7: **Hyperparameter settings for different VLA models and tasks.** We report task-specific hyperparameters used for OpenVLA and _π_ 0 _._ 5 across four real-world manipulation tasks. 

This control reduces the confound between simulation-data quality and the training objective. The SFT baseline learns from a fixed rollout dataset, while RL-Co collects rollouts online as its policy changes. The budget match is defined in simulation transitions. Together with the `Pick and Place` distillation result, this comparison provides additional evidence for the benefit of direct RL updates in the tested settings. 

## **I Implementation Details** 

For OpenVLA, we fine-tune the model using LoRA with a rank of 32, whereas _π_ 0 _._ 5 updates only the action expert, with the vision-language backbone frozen. All models are optimized using the AdamW optimizer [72]. The detailed hyperparameters are summarized in Table 7. 

The real-data SFT anchor complements these parameter-update restrictions. Fig. 5b measures its contribution by removing real supervision under the same training setup. Stage II uses on-policy PPO [67] with a learned value function, and the critic learning rates in Table 7 govern PPO value updates. 

## **J Resource Accounting and Training Time** 

### **J.1 Real-World Cost versus Simulation Cost** 

Fig. 6 compares the real-world demonstration requirements of the three training methods on `Open Drawer` . RL-Co achieves higher or comparable success with fewer real demonstrations, reducing the cost of real-world data collection. Beyond this real-world cost, the methods incur different simulation costs. Real-only SFT requires no simulation expenditure. SFT co-training additionally requires simulator construction and simulation-data generation, while RL-Co further incurs the cost of RL training in simulation. 

Simulation environments for different tasks can often share scene assets and setup effort. Simulation-data generation and training can also run unattended around the clock and be parallelized with additional computing resources, providing a low-cost way to scale experience collection. These advantages make simulation a practical substitute for additional human data collection, while its setup and computation costs remain part of the overall resource requirements. We therefore report a detailed time-cost comparison on `Open Drawer` , followed by training times across all four tasks. 

27 

### **J.2 Time Cost on Open Drawer** 

Table 8 summarizes the time required for simulator setup, real-world data collection, simulation-data generation, and RL co-training on `Open Drawer` . Constructing the simulator takes approximately one human working day, and this setup is shared across our four tasks. Collecting 200 real demonstrations takes approximately two human working days, with collection limited to working hours. In contrast, simulation-data generation and RL training can continue unattended outside working hours. 

|Operation|Time|Note|
|---|---|---|
|Simulator setup|_∼_1 human working day|Shared across four tasks|
|Collect 200 real demonstrations|_∼_2 human working days|Working hours only|
|MimicGen generation|1.5 h (RTX 4090)|Unattended computation|
|RL co-training|9.43 h (2_×_H100)|Unattended computation|


Table 8: Time costs for `Open Drawer` . Simulator setup is shared across the four tasks. Computation times are wall-clock durations on the listed hardware. 

With 20 real demonstrations, RL-Co achieves higher real-world success than real-only SFT with 200 demonstrations in Fig. 6. Its additional simulation work consists of the shared setup and approximately 11 hours of unattended data generation and RL training on the hardware in Table 8. Reusing the setup across tasks and running computation around the clock reduces the human effort required for policy improvement. This comparison shows the practical advantage of RL-Co in reducing real-world collection costs while achieving stronger performance. 

### **J.3 RL Training Time** 

Fig. 15 reports simulation success against wall-clock time for the four _π_ 0 _._ 5 Stage II runs shown in Appendix E.3. The runs use 3, 4, 2, and 3 H100 GPUs for `Pick and Place` , `Push Cube` , `Open Drawer` , and `Close Drawer` , respectively. 


Figure 15: Simulation success during _π_ 0 _._ 5 RL co-training versus wall-clock time across four tasks. 

28 

