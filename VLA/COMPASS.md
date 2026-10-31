---
title: "COMPASS: Cross-embOdiment Mobility Policy via ResiduAl RL and Skill Synthesis"
date: "2026"
venue: "ICRA 2026"
url: https://doi.org/10.1109/ICRA57385.2026.11696012
pdf: https://arxiv.org/pdf/2502.16372
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2502.16372)** / [論文ページ](https://doi.org/10.1109/ICRA57385.2026.11696012)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

_2025-10-29_ 


# **COMPASS: Cross-embOdiment Mobility Policy via ResiduAl RL and Skill Synthesis** 

**Wei Liu**<sup>1</sup> **, Huihua Zhao**<sup>1</sup> **, Chenran Li**<sup>1,2</sup> **, Yuchen Deng**<sup>1</sup> **, Joydeep Biswas**<sup>1,3</sup> **, Soha Pouya**<sup>1</sup> **and Yan Chang**<sup>1</sup> 1NVIDIA, 2UC Berkeley, 3UT Austin 

## **Abstract** 

**As robots are increasingly deployed in diverse application domains, enabling robust mobility across different embodiments has become a critical challenge. Classical mobility stacks, though effective on specific platforms, require extensive per-robot tuning and do not scale easily to new embodiments. Learning-based approaches, such as imitation learning (IL), offer alternatives, but face significant limitations on the need for high-quality demonstrations for each embodiment.** 

**To address these challenges, we introduce COMPASS, a unified framework that enables scalable crossembodiment mobility using expert demonstrations from only a single embodiment. We first pre-train a mobility policy on a single robot using IL, combining a world model with a policy model. We then apply residual reinforcement learning (RL) to efficiently adapt this policy to diverse embodiments through corrective refinements. Finally, we distill specialist policies into a single generalist policy conditioned on an embodiment embedding vector. This design significantly reduces the burden of collecting data while enabling robust generalization across a wide range of robot designs. Our experiments demonstrate that COMPASS scales effectively across diverse robot platforms while maintaining adaptability to various environment configurations, achieving a generalist policy with a success rate approximately 5X higher than the pre-trained IL policy on unseen embodiments, and further demonstrates zero-shot sim-to-real transfer.** 

**Project page:** `https://nvlabs.github.io/COMPASS` 

## **1. Introduction** 

While robotics has made significant strides in both industry and daily life, achieving robust mobility across diverse robot embodiments remains a fundamental open challenge. Morphological differences in hardware, kinematics and sensing configurations [1–3] create large variations in dynamics and perception, complicating efforts to build a universal and adaptable mobility policy for the real world. 

Classical mobility stacks [4, 5] excel in specific robots, especially wheeled platforms, but often require extensive manual retuning or redevelopment when ported to new embodiments with distinct sensor suites and physical constraints. This reliance on per-robot engineering has motivated interest in end-to-end learning approaches, particularly imitation learning (IL) [6, 7], which aim to scale mobility policies across multiple robots by leveraging data-driven training rather than manual redesign. 

However, scaling IL to diverse embodiments introduces a major bottleneck: each new robot typically requires its own set of high-quality demonstrations. As morphological and sensor differences increase, so does the need for additional embodiment-specific data. For complex modalities such as humanoids, collecting demonstrations can be prohibitively expensive or impractical. In parallel, IL can also suffer from the distribution shift [8], leading to failures when the policy encounters out-of-distribution states during deployment. While advances in machine learning architectures [9–11] and data augmentation techniques [12] help mitigate the distribution shift within a given embodiment, extending these methods to accommodate greater morphological diversity greatly amplifies data requirements and training complexity, further complicating the scalability of pure IL 

© 2025 NVIDIA. All rights reserved. 

**COMPASS** : **C** ross-emb **O** diment **M** obility **P** olicy via Residu **A** l RL and **S** kill **S** <u>ynthesis</u> 


Figure 1: High-level overview of the COMPASS workflow: (1) Imitation learning produces a base policy and world model using readily available teacher policies on a mobile robot. (2) Residual RL fine-tunes the base policy for multiple embodiments, optimizing for physical constraints and sensor modalities. (3) Policy distillation consolidates these embodiment-specialist policies into one robust cross-embodiment policy. 

approaches. 

Nevertheless, we observe that many key aspects of mobility are inherently shared across robot embodiments, such as environmental understanding, obstacle avoidance, and goal reaching. This observation motivates our central insight: it should be possible to build a cross-embodiment mobility policy by leveraging expert demonstrations from only a single embodiment. 

Based on this principle, we propose COMPASS, a unified three-stage workflow that combines imitation learning, residual reinforcement learning, and policy distillation, as shown in Figure 1. We first pre-train a mobility policy on a single embodiment using IL, leveraging expert demonstrations to train a shared representation of mobility priors over environmental states and robot actions. Following the X-Mobility approach [6], this pre-trained model is decomposed into two components: (i) a world model that encodes environmental dynamics, and (ii) a policy that learns to produce actions. To efficiently adapt this policy to various embodiments, we integrate residual reinforcement learning (RL) [13–15] into our workflow. Rather than training policies from scratch, residual RL enables each embodiment-specific specialist to refine the pre-trained policy through small corrective adjustments, improving closed-loop performance with fewer environment interactions. Finally, we collect data from these specialists and apply policy distillation to merge their expertise into a single cross-embodiment model, conditioned on an embodiment embedding vector. This workflow amortizes the demonstration effort, enabling robust generalization across diverse platforms while requiring expert demonstrations from only a single embodiment. Experiments show that COMPASS achieves a 5X increase in task success rate and a 3X improvement in travel efficiency compared to the IL-only policy, demonstrating both its 

2 

**COMPASS** : **C** ross-emb **O** diment **M** obility **P** olicy via Residu **A** l RL and **S** kill **S** <u>ynthesis</u> 


Figure 2: Residual RL architecture: (a) residual RL loop and (b) world model architecture. The world model processes the same inputs as the IL approach to produce the policy state, while the imitation-learned base policy generates a base action. The residual policy refines this action with a correction term, producing the final velocity command for embodiment-specific joint controllers. With the joint actions, the robot interacts with the environment and receives new observations and rewards. The data recorder records the pairs of policy state and action for policy distillation. 

effectiveness and scalability. 

To the best of our knowledge, this three-stage framework is the first end-to-end pipeline for crossembodiment mobility that systematically addresses morphological diversity, domain shift, and data efficiency. Our key contributions are as follows: 

- We propose a unified three-stage workflow that combines imitation learning, residual reinforcement learning, and policy distillation to achieve scalable, data-efficient cross-embodiment mobility from demonstrations collected on a single embodiment. 

- We develop a visual RL approach that leverages a world model to efficiently refine policies across embodiments by incorporating temporal and spatial structure. 

- We demonstrate extensive benchmarks across diverse robot platforms, showing that the proposed approach achieves robust generalization while preserving the adaptability needed to succeed in varied environments and zero-shot sim-to-real transfer. 

## **2. Method** 

We present a three-stage workflow aimed at building robust cross-embodiment mobility policies (see Fig. 1). First, we train a base policy via IL, which captures general mobility priors from teacher demonstrations on mobile robots. Next, we refine this base policy into embodiment-specific specialists via residual RL. Finally, policy distillation combines these specialists into a single model suitable for multi-platform deployment. 

### **2.1. Problem Statement** 

We focus on the task of point-to-point mobility across different robotic embodiments, each characterized by unique kinematics and dynamics. At time step _𝑡_ , let the robot observe a state 

**x** _𝑡_ = (︀ **I** _𝑡,_ **v** _𝑡,_ **g** _𝑡,_ **e** )︀ _,_ 

3 

**COMPASS** : **C** ross-emb **O** diment **M** obility **P** olicy via Residu **A** l RL and **S** kill **S** <u>ynthesis</u> 

where **I** _𝑡_ is current camera input (RGB images), **v** _𝑡_ is the measured velocity, **g** _𝑡_ provides route or goal-related information (e.g., goal position in robot frame), and **e** is an embodiment embedding that specifies the robot’s morphology. Although **e** remains constant for a single robot during an episode, it varies across different embodiments. 

We aim to learn a policy _𝜋𝜃_ that maps **x** _𝑡_ to a velocity command **a** _𝑡_ = ( _𝑣𝑡, 𝜔𝑡_ ), which is then consumed by a low-level controller for joint-level actuation. The environment’s transition dynamics _𝑝_ ( **x** _𝑡_ +1 _|_ **x** _𝑡,_ **a** _𝑡_ ) depend on both the robot’s embodiment and external factors in the scene. We define a reward function _𝑅_ ( _·_ ) that encourages efficient, collision-free progress to the goal. The objective is to maximize the expected discounted return 


The challenge is to design a single policy that leverages the embodiment embedding **e** , allowing shared knowledge yet accommodating distinct morphological constraints. 

### **2.2. Step 1: Imitation Learning for Mobility Priors** 

The initial step uses IL to acquire a generic mobility baseline. We rely on readily available teacher policies—often classical mobility stacks—for standard mobile robots, which typically provide reliable demonstrations. 

#### **2.2.1. Latent State Modeling** 

We introduce a latent state **s** _𝑡_ to capture environment dynamics. Let **o** _𝑡_ = (︀ **I** _𝑡,_ **v** _𝑡_ )︀ denote raw observations, including RGB images and robot velocities. Our goal is to learn a world model that predicts transitions in this latent space: 


where _𝑓𝜑_ updates the latent state based on the previous action, and _𝑔𝜓_ attempts to reconstruct or predict **o** _𝑡_ . Training minimizes reconstruction and predictive losses over a dataset of expert demonstrations 


where **a**<sup>_⋆_</sup> _𝑡_<sup>are the expert (teacher) actions.</sup> 

#### **2.2.2. Policy Learning in Latent Space** 

Having learned a latent transition, we then train a policy _𝜋𝜃_<sup>ILthat takes policy state</sup><sup>**p**</sup><sup>_𝑡_, which is fused from the</sup> latent state **s** _𝑡_ and route embedding **r** _𝑡_ , to predict **a** _𝑡_ : 


where _𝑓𝜃_ denotes route encoding and Φ is a learnable feature fusion block. 

We minimize the action discrepancy between the policy’s outputs and the teacher’s actions: 


where _ℓ_ ( _·_ ) could be a simple regression loss. This yields an IL-based mobility priors. The world model helps the policy generalize to out-of-distribution states by predicting future observations and latent transitions, thereby providing a robust encoded representation for decision-making. 

4 

**COMPASS** : **C** ross-emb **O** diment **M** obility **P** olicy via Residu **A** l RL and **S** kill **S** <u>ynthesis</u> 

#### **2.2.3. X-Mobility** 

We leverage the X-Mobility [6] as our base policy, which integrates an autoregressive world model (see Fig. 2) with a velocity-prediction policy model. The learned latent state **s** _𝑡_ encapsulates environment dynamics and constraints, while the policy head combines this state with route information to generate velocity commands. X-Mobility’s strong generalization performance indicates that its learned representation readily adapts to different embodiments. 

### **Residual RL to Fine-Tune Specialists** 

### **2.3. Step 2:** 

Having trained a promising general mobility policy through IL, we refine it for embodiment-specific needs via residual RL. This stage addresses robot-specific kinematics, sensor configurations, and other constraints that the base IL policy may not fully capture. 

#### **2.3.1. Residual Policy Setup** 

Let **a**<sup>base</sup> _𝑡_ = _𝜋𝜃_<sup>base</sup> ( **p** _𝑡_ ) be the action from the IL baseline. We introduce a residual policy _𝜋𝜑_<sup>resthat takes residual</sup> policy state **p** ˆ _𝑡_ and outputs **a**<sup>res</sup> _𝑡_<sup>.The final action is</sup> 


The role of _𝜋𝜑_<sup>resis to adapt the base policy to nuances of a specific embodiment’s characteristics.</sup> 

#### **2.3.2. Residual Policy State** 

To enable effective residual policy learning, we introduce a residual policy state **p** ˆ _𝑡_ = _𝒢_ ( **p** _𝑡_ ), which augments the base policy state **p** _𝑡_ with additional task-relevant information. This design allows the residual policy to complement the base policy by incorporating inputs that were not considered during the base policy training. For example, if the base policy omits goal heading information, we can inject its embedding into the residual policy state, allowing the final composite policy to account for the desired heading and achieve more stable goal-reaching behavior. This modular formulation offers flexibility to extend the capabilities of the base policy without retraining it from scratch. 

#### **2.3.3. Residual Policy Network Architecture** 

The residual policy network reuses the same policy model as in the base policy. We initialize it by copying the weights of the base action policy and introducing a linear projection layer to align the dimensionality between the base policy state and the residual policy state. The final output layer is reinitialized to exclusively learn the residual correction. This initialization strategy stabilizes training and encourages the residual component to specifically address embodiment-specific discrepancies. The critic network is implemented as a standard multi-layer perceptron (MLP), taking the same residual policy state as input. 

#### **2.3.4. Reward Design** 

We define a reward function _𝑅_ to promote safe and efficient mobility, consisting of the following components: 

- Progress: Positive reward proportional to the reduction in distance to the goal. 

- Collision avoidance: Penalties for collisions or fall downs. 

- Goal completion: Large positive reward on reaching the destination with zero velocities. 

We adopt this simple formulation to facilitate training, while acknowledging that more sophisticated reward shaping could potentially yield better performance. 

5 

**COMPASS** : **C** ross-emb **O** diment **M** obility **P** olicy via Residu **A** l RL and **S** kill **S** <u>ynthesis</u> 


Figure 3: Policy distillation aggregates multiple expert specialists (one per embodiment). The final multiembodiment policy uses a one-hot or learned embedding to condition decisions on robot morphology. 

#### **2.3.5. Training Loop** 

We employ a PPO-based RL optimizer [16] for the residual policy _𝜋𝜑_<sup>res.As illustrated in Fig.2, each training</sup> iteration proceeds as follows: 

1. The agent receives the current state **x** _𝑡_ , processes it through the world model to form the policy state **p** _𝑡_ , then generates the base action **a**<sup>base</sup> _𝑡_ from the IL policy and the residual action **a**<sup>res</sup> _𝑡_ from the residual network. 

2. The combined action **a** _𝑡_ is executed in the simulation environment via an embodiment-specific joint controller. 

3. The agent observes the next state **x** _𝑡_ +1 and the reward _𝑅_ associated with the transition. 

4. The residual policy _𝜋𝜑_<sup>resis updated via gradient-based methods, while the IL policy</sup><sup>_𝜋_</sup> _𝜃_<sup>base</sup> remains frozen. 

The environment resets if the robot reaches the destination, collides with an obstacle, or times out. Upon receiving the reset signal, history states within the world model are also cleared. 

By building on a robust pre-trained base policy, the residual RL framework mitigates the sparse sampling challenge. This enables faster convergence to high-performance policies for each embodiment. 

### **2.4. Step 3: Policy Distillation to Combine Specialists** 

After separately training residual RL specialists for each robot embodiment, we consolidate them into a single multi-embodiment policy. This “distilled” policy captures the collective knowledge of all specialist policies while using an embodiment embedding to generalize across different robot platforms. 

#### **2.4.1. Data Collection from Specialists** 

After the residual RL training, we record each specialist’s input and output distributions, including: 

- Policy state from the world model. 

- One-hot embodiment identifier **e** . 

- Mean and variance of the Gaussian action distribution used in PPO. 

This logged dataset forms the basis for distillation. 

6 

**COMPASS** : **C** ross-emb **O** diment **M** obility **P** olicy via Residu **A** l RL and **S** kill **S** <u>ynthesis</u> 

#### **2.4.2. Distillation Method** 

Let _𝜋𝜑_<sup>(</sup><sup>_𝑖_)denote the specialist policy for the</sup><sup>_𝑖_-th embodiment.Each specialist produces a normal distribution</sup> _𝒩_ ( **_𝜇_**<sup>(</sup><sup>_𝑖_)</sup> ( **p** ) _, 𝜎_<sup>2</sup> ) over actions. We define a distilled policy _𝜋𝜃_<sup>dist</sup> that outputs **_𝜇_** _𝜃_ ( **p** _,_ **e** ) given **p** and an embodiment embedding **e** . To match the specialists’ distributions, we minimize the KL divergence: 


where _𝑑_<sup>_𝑖_</sup> = ( **p** _,_ **_𝜇_**<sup>(</sup><sup>_𝑖_)</sup> _, 𝜎_<sup>2</sup> ) and _𝒟_<sup>(</sup><sup>_𝑖_)</sup> is the dataset of recorded state-action distributions from the _𝑖_ -th specialist. **e**<sup>(</sup><sup>_𝑖_)</sup> is the corresponding embodiment embedding. 

#### **2.4.3. Embodiment Embedding** 

A key component of policy distillation is the embodiment embedding **e** , which captures the morphological and dynamical characteristics of each embodiment. In the simplest version, we use a one-hot encoding vector of length _𝑁_ , where _𝑁_ denotes the number of robot embodiments. Each position in this vector corresponds to a specific robot. This straightforward approach is efficient when _𝑁_ is small and the robots differ substantially. We anticipate that a learnable embedding could better generalize to new, unseen embodiments by interpolating within the embedding space, and we leave such zero-shot generalization for future work. 

#### **2.4.4. Distilled Policy Network Architecture** 

The distilled policy retains the same latent processing pipeline but additionally conditions on the embodiment embedding before generating the final action distribution (see Fig. 3). The network consists of an MLP for mean prediction and a global variance parameter, resulting in a single policy that achieves near-expert performance across all considered robot types. 

Consequently, our three-step framework—imitation learning, residual RL, and policy distillation—bridges the gap between generic mobility knowledge and highly specialized embodiment constraints, yielding a unified cross-embodiment mobility policy. 

## **3. Experimental Setup** 

### **3.1. Training** 

#### **3.1.1. IL Base Policy** 

For the initial IL stage, we employ a X-Mobility checkpoint pre-trained on Carter dataset. We freeze this checkpoint, which then serves as the base network for subsequent RL refinements. 

#### **3.1.2. Residual RL** 

We utilize Nvidia Isaac Lab [17] to train our policies in a parallelized visual RL environment, enabling efficient data collection and rapid training updates. 

To avoid overfitting and preserve the base policy’s ability to generalize across environments, we construct a diverse set of training scenarios (Fig. 4) that accommodate four distinct robot embodiments: Nova Carter (wheeled), Unitree H1 (humanoid), Unitree G1 (humanoid), and Spot Mini (quadruped). For the humanoid and quadruped robots, we employ RL-based locomotion policies, trained within Isaac Lab, to map velocity commands to joint-level controls. Due to limited wheel-physics support in Isaac Lab, Nova Carter instead uses a custom controller that directly adjusts the robot’s root state based on velocity commands. 

7 

**COMPASS** : **C** ross-emb **O** diment **M** obility **P** olicy via Residu **A** l RL and **S** kill **S** <u>ynthesis</u> 


Figure 4: Residual RL training environment. Multiple instances are tiled and run in parallel to accelerate data collection and model updates. 

Each embodiment is trained in a unified environment that randomly initializes the agent’s pose and the goal location, where the goal distance is uniformly sampled between 2m and 5m from the robot’s starting position. The straight line between the robot and the goal serves as a simplified route, providing short-horizon guidance within the camera’s field of view. Each episode spans up to 256 timesteps and resets if the agent collides, reaches its goal, or exceeds the maximum episode length. We train each embodiment specialist for 1,000 episodes with 64 environments in parallel using 2 Nvidia L40 GPUs, except for Carter, which is trained for only 300 episodes to mitigate overfitting. This reduced training schedule for Carter is necessary because X-Mobility is already trained on Carter dataset, making it prone to overfitting if extensively fine-tuned. 

#### **3.1.3. Policy Distillation** 

To distill the learned specialists into a single unified policy, we record 320 trajectories per embodiment using the same environment as residual RL training. Each trajectory spans 128 steps, yielding approximately 40k frames per embodiment. We then perform policy distillation training on 4 Nvidia H100 GPUs by aligning each specialist’s output distribution. 

### **3.2. Benchmark** 

#### **3.2.1. Metrics** 

We evaluate both efficiency and safety using two key metrics: 

- Success Rate (SR): Fraction of trials that reach the goal region without collision or timeout. 

- Weighted Travel Time (WTT): Total travel time to reach the goal, conditioned on success, divided by SR. 

#### **3.2.2. Scenarios** 

We evaluate our algorithm in four environments of increasing difficulty as in Fig. 5. In the simplest environment, only sparse low lying obstacles are present, while in the complex one, a warehouse with multiple racks requires long-horizon mobility under minimal route guidance. To further assess the policy’s robustness and 

8 

**COMPASS** : **C** ross-emb **O** diment **M** obility **P** olicy via Residu **A** l RL and **S** kill **S** <u>ynthesis</u> 


Figure 5: Evaluation environments with multiple layouts to assess policy generalization: (a) warehouse with single rack (24 _𝑚 ×_ 38 _𝑚_ ), (b) warehouse with multi racks (24 _𝑚 ×_ 38 _𝑚_ ), (c) office (10 _𝑚 ×_ 10 _𝑚_ ), and (d) combined scenes with multi racks (30 _𝑚 ×_ 38 _𝑚_ ). 

generalization, we also vary textures and lighting conditions across these environments. 

For each environment, we conduct 640 trials with randomly sampled initial and goal poses. Each trial is terminated after 25.6s of execution. We then collect performance metrics for each embodiment and environment type, allowing direct comparison of mobility performance across different settings. 

## **4. Results** 

This section addresses four primary questions: 

- Does residual RL effectively yield high-performance embodiment specialists from the IL baseline? 

- Can policy distillation consolidate these specialists into a single robust generalist without a considerable performance drop? 

- How does our approach compare to alternative strategies, such as training RL from scratch? 

- Can COMPASS policy trained in simulation be applied to real robot platforms? 

### **4.1. Does residual RL produce high-performance embodiment specialists?** 

To investigate whether residual RL can improve performance relative to the IL baseline (X-Mobility), we compared the specialist policies for each embodiment against X-Mobility, and the results are summarized in Table 1. In all evaluations, the specialist policies significantly outperform X-Mobility across both success rate (SR) and mobility efficiency (WTT). The SR is improved with a factor ranging from 5x to 40x, and the WTT is improved 3x on average. This performance boost suggests that residual RL effectively leverages environment semantics and embodiment-specific physics. In particular, by exploring each robot’s physical limits during training, the specialist can produce commands that maximize efficiency while maintaining balance and stability. 

A notable observation is that while X-Mobility performs best on the Carter robot, its zero-shot performance on other embodiments degrade significantly. This aligns with expectations and underscores the need for embodiment-specific policy adaptations to ensure robustness. Compared to the original X-Mobility paper, we observe a performance drop for Carter in warehouse environments within Isaac Lab, primarily due to simplified 

9 

**COMPASS** : **C** ross-emb **O** diment **M** obility **P** olicy via Residu **A** l RL and **S** kill **S** <u>ynthesis</u> 


Figure 6: Example illustrates the generalist’s cross-embodiment capability: G1 shortcuts beneath the shelf, while H1 must detour due to insufficient height clearance. 

routes and variations in image rendering quality. This motivates future improvements, such as incorporating a hierarchical mobility stack for more sophisticated routing and exposing the model to diverse rendering conditions during latent state training. 

Table 1: Benchmark Results 

|**Emb.**|**Model**|**Wareho**|**use Single**|**Wareho**|**use Multi**|**Ofi**|**ffice**|**Com**|**bined**|
|---|---|---|---|---|---|---|---|---|---|
|||SR(%)|WTT(s)|SR(%)|WTT(s)|SR(%)|WTT(s)|SR (%)|WTT(s)|
||X-Mobility|42.3|8039|37.9|9351|50.6|5508|50.3|5319|
|Carter|Carter Specialist|**91.5**|2282|91.8|**2283**|72.0|**2340**|**85.4**|**2442**|
||Generalist|90.6|**2241**|**91.9**|2361|**73.4**|2504|85.3|2527|
||X-Mobility|17.5|12588|9.2|12234|25.6|10791|22.0|11519|
|H1|H1 Specialist|**94.5**|**4123**|87.9|**4283**|**66.7**|3300|82.8|**3698**|
||Generalist|93.4|4129|**88.9**|4319|66.2|**3260**|**84.4**|3802|
||X-Mobility|5.7|13320|4.5|12007|6.1|7740|11.7|11426|
|Spot|Spot Specialist|84.5|**3183**|**93.5**|**3204**|**76.2**|3587|77.1|3490|
||Generalist|**84.7**|3207|93.2|3255|74.8|**3512**|**77.9**|**3485**|
||X-Mobility|3.6|13913|1.8|13781|2.8|13276|10.0|11865|
|G1|G1 Specialist|95.6|**4667**|93.7|**5254**|**77.0**|**3960**|90.0|**3968**|
||Generalist|**95.7**|4717|**94.5**|5360|76.7|4031|**90.6**|3991|


### **4.2. Can policy distillation produce a robust generalist?** 

We next evaluate whether policy distillation can merge the specialists into a single generalist policy without sacrificing overall performance. As shown in Table 1, the generalist achieves performance comparable to, and sometimes exceeding, that of the specialist policies. This is especially evident on the G1 robot, likely due to increased diversity in training scenarios and embodiments during distillation. These results confirm that our distillation approach is effective and that building a robust generalist from multiple specialists is both feasible and efficient. 

As a case study of cross-embodiment capabilities, we designed a long-horizon mobility scenario in a multirack warehouse. As illustrated in Fig. 6, G1 can lean slightly to the right and pass under a shelf with just 

10 

**COMPASS** : **C** ross-emb **O** diment **M** obility **P** olicy via Residu **A** l RL and **S** kill **S** <u>ynthesis</u> 

enough head clearance, whereas H1 lacks sufficient clearance and must take a detour. This example highlights how the generalist effectively accounts for each embodiment’s distinct morphological constraints. 

### **4.3. How does COMPASS compare to training from scratch?** 

We also explored whether we could train a policy from scratch using the same RL setup with the latent state but without leveraging the IL base actions. We observed that this RL-from-scratch approach struggled to converge even after 1,000 episodes as in Fig. 7, indicating significantly lower training efficiency. In contrast, our residual RL method exhibited notably faster convergence, underscoring how leveraging an IL baseline resolves the sparsity issues that commonly plague RL in mobility tasks. 


Figure 7: RL from scratch v.s. Residual RL. 

### **4.4. Can COMPASS Policy trained in simulation be applied to real robot platforms?** 

To evaluate the Sim2Real transferability, we deployed it on two real-world robotic platforms powered by the NVIDIA Jetson Orin: Carter and Unitree G1 (Fig. 1). Leveraging the world model latent state representation, along with Isaac Lab’s high-quality visual rendering and accurate physics simulation, both robots achieved robust zero-shot transfer, successfully navigating cluttered environments without any additional fine-tuning. With localization enabled by cuVSLAM [18], the policy attained a success rate of approximately 80% across 20 trials with randomly placed obstacles, consistently avoiding collisions and reaching the designated targets. We anticipate that RL fine-tuning focused on semantic understanding of the environment, particularly when combined with a Real2Sim pipeline [19], can further narrow the Sim2Real gap. 

Moreover, onboard inference with TensorRT requires only _∼_ 30 ms per step as in Table 2, demonstrating that the policy is computationally efficient and well-suited for real-time deployment. 

Table 2: Inference Latency and GPU Memory Usage 

|**Model**|**P50(ms)**|**P95(ms)**|**GPU Memory(MB)**|
|---|---|---|---|
|**Distilled Generalist**|29.3389|29.3767|422|


## **5. Ablation Studies** 

### **5.1. Residual RL** 

In this section, we present ablation studies evaluating the various design decisions in our residual RL approach. We exclude the Carter robot from these experiments as its cross-embodiment effect is less pronounced. 

11 

**COMPASS** : **C** ross-emb **O** diment **M** obility **P** olicy via Residu **A** l RL and **S** kill **S** <u>ynthesis</u> 

Table 3: Ablation Studies on Residual RL. 

|**Emb.**|**Model**|**Wareho**|**use Single**|**Wareho**|**use Multi**|**Ofi**|**ffice**|**Com**|**bined**|
|---|---|---|---|---|---|---|---|---|---|
|||SR(%)|WTT(s)|SR(%)|WTT(s)|SR(%)|WTT(s)|SR (%)|WTT(s)|
||**Default**|94.5|4123|87.9|4283|66.7|3300|**82.8**|3698|
||w/ Curriculum|96.1|4045|88.7|4155|66.5|3148|83.9|3933|
|H1|Depth Critic|90.9|4245|87|4254|72.3|3530|85.4|3764|
||Warehouse Only|94.6|3237|88.7|3249|64.0|2850|81.0|3152|
||**Default**|84.5|3183|93.5|3204|76.2|3587|77.1|3490|
|S|w/ Curriculum|81.5|3079|86.2|3128|66.1|3112|71.5|3238|
|pot|Depth Critic|83.4|3090|92.1|3125|77.9|3645|77.6|3226|
||**Default**|95.6|4667|**93.7**|5254|**77.0**|3960|**90.0**|3968|
|G1|w/ Curriculum|96.4|4376|86.5|4992|69.6|3478|89.0|4018|
||Depth Critic|95.7|4600|87.9|5153|78.4|4091|91.4|4018|


Green/Red: Better/Worse than default setting 

#### **5.1.1. Curriculum on Goal Distance** 

In our RL training setup, we currently do not use a curriculum. To investigate whether such a strategy could improve training efficiency, we introduced a curriculum based on goal distance. Rather than enforcing a minimum goal distance from the outset, we gradually increased the probability of applying this constraint as training progressed to enable smoother convergence. 

However, the results in Table 3 indicate that the curriculum-based approach did not outperform the baseline without a curriculum. A likely explanation is that the IL base policy already provides a strong initialization, and reducing exposure to challenging scenarios with the curriculum may have limited the policy’s capacity to explore and succeed on more difficult tasks. 

#### **5.1.2. Critic State** 

In our default setup, the critic network uses the same policy state as the actor, under the assumption that the policy state already encapsulates sufficient information to learn accurate value functions. While this approach often works well, it depends on implicit information, which may make learning the critic network more challenging. To investigate potential improvements, we explored different configurations for the critic’s input. In one variant, we provided a depth image explicitly to the value function by employing a ResNet18 for feature extraction, then concatenating the resulting features with velocity and route embeddings to form the critic state. As shown in Table 3, this strategy enhanced performance in office scenarios—where tall obstacles exist—but inadvertently reduced performance in warehouse environments presented with more low-lying obstacles. These findings suggest that the additional signal from the depth image can boost performance under certain conditions, indicating a promising direction for further exploration. 

#### **5.1.3. Training Environment** 

In another ablation study, we evaluate the impact of the training environment. Our default setup uses a combined environment consisting of warehouse, office, and lab scenarios. To assess the effect of environmental diversity, we also conducted a separate training run using only the warehouse environment with H1 robot. The results, shown in Table 3, indicate that restricting training to warehouse scenarios slightly enhances performance in warehouse scenes but reduces performance in the office and combined settings. These findings underscore the value of diverse training environments for improving generalization. Notably, even though the office setting was excluded from this specialized training, the model still performs reasonably well when tested 

12 

**COMPASS** : **C** ross-emb **O** diment **M** obility **P** olicy via Residu **A** l RL and **S** kill **S** <u>ynthesis</u> 

Table 4: Ablation study on policy distillation 

|**Emb.**|**Koss / Dataset**|**Wareho**|**use Single**|**Wareho**|**use Multi**|**Ofi**|**ffice**|**Com**|**bined**|
|---|---|---|---|---|---|---|---|---|---|
|||SR(%)|WTT(s)|SR(%)|WTT(s)|SR(%)|WTT(s)|SR (%)|WTT(s)|
||KL / All|90.6|2241|91.9|2361|73.4|2504|85.3|2527|
|Carter|MSE / All|89.8|2201|92.1|2331|73.7|2585|85.1|2452|
||KL / Good|93.1|2246|92.0|2388|72.3|2427|83.1|2744|
||KL / All|93.4|4129|88.9|4319|66.2|3260|84.4|3802|
|H1|MSE / All|93.3|4082|87.6|4260|66.5|3251|82.1|3717|
||KL / Good|93.6|4043|88.4|4218|66.1|3288|88.4|4218|
||KL / All|84.7|3207|93.2|3255|74.8|3512|77.9|3485|
|Spot|MSE / All|84.3|3180|93.6|3218|75.0|3512|79.2|3516|
||KL / Good|84.6|3234|94.3|3200|75.1|3462|78.4|3410|
||KL / All|95.7|4717|94.5|5360|76.7|4031|90.6|3991|
|G1|MSE / All|96.8|4596|94.3|5336|77.6|4030|89.8|3934|
||KL / Good|95.1|4622|93.4|5180|75.4|3884|90.0|3946|


Green/Red: Better/Worse than baseline 

there, demonstrating a degree of environment generalizability. 

### **5.2. Policy Distillation** 

In our final ablation study, we want to examine the policy distillation process. The default setup trains the distilled policy to minimize KL divergence on an unfiltered dataset that may include failure cases. Our first goal is to assess whether capturing the full policy distribution is more beneficial than merely imitating the mean. To this end, we trained another model using only an MSE loss on the mean predictions. As shown in Table 4, this approach led to slightly inferior performance, particularly on the H1 robot, suggesting that KL divergence—which preserves variance—provides more flexibility for managing training noise and architectural differences. 

We also investigated the role of dataset quality by constructing a new dataset from the same scenarios but excluding all failure cases, hypothesizing that this might yield better overall performance. Contrary to our expectations, the results in Table 4 improved only marginally. We suspect that removing failure cases also eliminates corner cases that could otherwise offer valuable learning opportunities for the generalist policy. 

## **6. Applications** 

This section presents selected applications of the COMPASS workflow and its trained policy, demonstrating capabilities that extend beyond the COMPASS workflow itself. 

### **6.1. Open Vocabulary Object Navigation** 

The COMPASS policy is trained for point-based navigation, where the navigation command specifies a target pose. Thanks to its flexible interface design, COMPASS can also support open-vocabulary object navigation by integrating it with an object localization model such as Locate3D [20] (see Fig. 8). Given a language prompt describing the target object, the object localization model predicts the corresponding 3D bounding box. Combined with user-defined parameters, such as relative heading and clearance distance, the target pose generator computes an appropriate goal pose for COMPASS to navigate toward. This setup enables a modular 

13 

**COMPASS** : **C** ross-emb **O** diment **M** obility **P** olicy via Residu **A** l RL and **S** kill **S** <u>ynthesis</u> 


Figure 8: Open vocabulary object navigation by integrating COMPASS and object localization. 

framework that extends COMPASS from point-based navigation to open-vocabulary object navigation. 

### **6.2. Synthetic Datasets for VLA Fine Tuning** 

Given the high quality of the RL specialist policy, it can also be leveraged to generate large-scale synthetic datasets in Isaac Lab for training foundational Vision-Language-Action (VLA) models for navigation tasks that typically demand substantial amounts of diverse training data. As a demonstration, we post-trained the Gr00t N1.5 model [21] using the COMPASS distillation dataset generated by the G1 expert policy. In this setup, goal information and measured velocity were provided as state inputs, while ego-centric video frames served as the visual input, paired with a generic text prompt (“Robot Navigation Task”). The Gr00t model was then trained to predict the corresponding velocity commands. 

Notably, despite being trained on only 600 trajectories and without any prior pre-training on navigation, the fine-tuned Gr00t model successfully acquired robust navigation capabilities. When evaluated on 640 randomly generated test cases in Isaac Lab, the post-trained policy achieved task success rates comparable to the original COMPASS policy in in-distribution warehouse environments, as shown in Table 5. Moreover, it significantly outperformed COMPASS in the hospital environment, which represents a fully out-of-distribution setting. The model also demonstrated seamless transfer to real-world environments without any additional fine-tuning, enabling smooth integration with the Gr00t manipulation policy for more advanced loco-manipulation tasks, as illustrated in Fig. 9. 

Table 5: Success Rate of Gr00t N1.5 Post-Trained on the COMPASS Dataset 

|**Model**|**Warehouse**|**Hospital**|
|---|---|---|
|**Gr00t N1.5**|86.1%|77.6%|
|**COMPASS**|84.7%|45.6%|


## **7. Future Works** 

We have introduced a novel workflow, COMPASS, for cross-embodiment mobility that leverages imitation learning, residual RL, and policy distillation. The initial IL step provides a strong baseline, while residual RL quickly adapts the model to each embodiment’s dynamics, and a final distillation step merges specialized policies into a single, generalist policy. Our experiments show that this approach scales effectively to various robot platforms and environments. 

Our findings also suggest several key takeaways and directions for future work: 

14 

**COMPASS** : **C** ross-emb **O** diment **M** obility **P** olicy via Residu **A** l RL and **S** kill **S** <u>ynthesis</u> 


Figure 9: Zero-shot Sim2Real deployment of the post-trained Gr00t model for loco-manipluation tasks. 

- Embodiment Encoding Strategy: We find that one-hot encoding is sufficient when only a few distinct platforms are considered. For a larger or more continuous spectrum of embodiments, a learned embedding might offer richer generalization [22]. 

- Distillation Trade-offs: Although policy distillation successfully merges expertise from specialized policies, it can also lead to an averaging effect across embodiments. This phenomenon contributes to embodimentdependent performance variations. 

- Transferability vs. Specialization: While residual RL can adapt rapidly to new embodiments, using the same set of hyperparameters can lead to performance divergence, as demonstrated in our studies. Consequently, specialized designs and tuned hyperparameters are often required to achieve optimal results. 

- Hierarchical Mobility Stack: We observe a decreased success rate in environments such as offices and multi-rack warehouses, primarily for tasks requiring long-horizon route planning. This underscores the importance of a hierarchical mobility stack with a graph-based route planner to handle more complex mobility scenarios. 

## **8. Acknowledgment** 

We thank Di Zeng, Chirag Majithia, Sameer Chavan, Billy Okal, Dennis Da, Fernando Castaneda Garcia-Rozas, Peter Varvak, Manuel Chavez Orozco, Vishal Kulkarni, Qi Wang, Yuke Zhu, and Jim Fan for their assistance with system integration and robot testing and for providing insightful feedback on the workflow setup. 

## **References** 

- [1] R. Doshi, H. Walke, O. Mees, S. Dasari, and S. Levine, “Scaling cross-embodied learning: One policy for manipulation, navigation, locomotion and aviation,” _arXiv preprint arXiv:2408.11812_ , 2024. 1 

- [2] M. Xu, Z. Xu, C. Chi, M. Veloso, and S. Song, “XSkill: Cross embodiment skill discovery,” in _7th Annual Conference on Robot Learning_ , 2023. [Online]. Available: https://openreview.net/forum?id= 8L6pHd9aS6w 1 

- [3] J. Yang, C. Glossop, A. Bhorkar, D. Shah, Q. Vuong, C. Finn, D. Sadigh, and S. Levine, “Pushing the limits of cross-embodiment learning for manipulation and navigation,” _arXiv preprint arXiv:2402.19432_ , 2024. 1 

- [4] S. Macenski, F. Martín, R. White, and J. Ginés Clavero, “The marathon 2: A navigation system,” in _2020_ 

15 

**COMPASS** : **C** ross-emb **O** diment **M** obility **P** olicy via Residu **A** l RL and **S** kill **S** <u>ynthesis</u> 

_IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2020. [Online]. Available: https://github.com/ros-planning/navigation2 1 

- [5] W. Liu, Z. Weng, Z. Chong, X. Shen, S. Pendleton, B. Qin, G. M. J. Fu, and M. H. Ang, “Autonomous vehicle planning system design under perception limitation in pedestrian environment,” in _2015 IEEE 7th International Conference on Cybernetics and Intelligent Systems (CIS) and IEEE Conference on Robotics, Automation and Mechatronics (RAM)_ . IEEE, 2015, pp. 159–166. 1 

- [6] W. Liu, H. Zhao, C. Li, J. Biswas, B. Okal, P. Goyal, Y. Chang, and S. Pouya, “X-mobility: End-to-end generalizable navigation via world modeling,” _arXiv preprint arXiv:2410.17491_ , 2024. 1, 2, 5 

- [7] Z. Xu, X. Xiao, G. Warnell, A. Nair, and P. Stone, “Machine learning methods for local motion planning: A study of end-to-end vs. parameter learning,” in _2021 IEEE International Symposium on Safety, Security, and Rescue Robotics (SSRR)_ . IEEE, 2021, pp. 217–222. 1 

- [8] J. Chang, M. Uehara, D. Sreenivas, R. Kidambi, and W. Sun, “Mitigating covariate shift in imitation learning via offline data with partial coverage,” _Advances in Neural Information Processing Systems_ , vol. 34, pp. 965–979, 2021. 1 

- [9] X. Wang, Z. Zhu, G. Huang, X. Chen, J. Zhu, and J. Lu, “Drivedreamer: Towards real-world-driven world models for autonomous driving,” _arXiv preprint arXiv:2309.09777_ , 2023. 1 

- [10] A. Popov, A. Degirmenci, D. Wehr, S. Hegde, R. Oldja, A. Kamenev, B. Douillard, D. Nistér, U. Muller, R. Bhargava _et al._ , “Mitigating covariate shift in imitation learning for autonomous vehicles using latent space generative world models,” _arXiv preprint arXiv:2409.16663_ , 2024. 1 

- [11] T. Feng, W. Wang, and Y. Yang, “A survey of world models for autonomous driving,” _arXiv preprint arXiv:2501.11260_ , 2025. 1 

- [12] S. Ross, G. Gordon, and D. Bagnell, “A reduction of imitation learning and structured prediction to no-regret online learning,” in _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ . JMLR Workshop and Conference Proceedings, 2011, pp. 627–635. 1 

- [13] T. Johannink, S. Bahl, A. Nair, J. Luo, A. Kumar, M. Loskyll, J. A. Ojea, E. Solowjow, and S. Levine, “Residual reinforcement learning for robot control,” in _2019 international conference on robotics and automation (ICRA)_ . IEEE, 2019, pp. 6023–6029. 2 

- [14] L. Ankile, A. Simeonov, I. Shenfeld, M. Torne, and P. Agrawal, “From imitation to refinement–residual rl for precise visual assembly,” _arXiv preprint arXiv:2407.16677_ , 2024. 2 

- [15] C. Li, C. Tang, H. Nishimura, J. Mercat, M. Tomizuka, and W. Zhan, “Residual q-learning: Offline and online policy customization without value,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 61 857–61 869, 2023. 2 

- [16] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 6 

- [17] M. Mittal, C. Yu, Q. Yu, J. Liu, N. Rudin, D. Hoeller, J. L. Yuan, R. Singh, Y. Guo, H. Mazhar, A. Mandlekar, B. Babich, G. State, M. Hutter, and A. Garg, “Orbit: A unified simulation framework for interactive robot learning environments,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 6, pp. 3740–3747, 2023. 7 

- [18] A. Korovko, D. Slepichev, A. Efitorov, A. Dzhumamuratova, V. Kuznetsov, H. Rabeti, and J. Biswas, “cuvslam: Cuda accelerated visual odometry,” _arXiv preprint arXiv:2506.04359_ , 2025. 11 

- [19] S. Zhu, L. Mou, D. Li, B. Ye, R. Huang, and H. Zhao, “Vr-robo: A real-to-sim-to-real framework for visual robot navigation and locomotion,” _arXiv preprint arXiv:2502.01536_ , 2025. 11 

16 

**COMPASS** : **C** ross-emb **O** diment **M** obility **P** olicy via Residu **A** l RL and **S** kill **S** <u>ynthesis</u> 

- [20] S. Arnaud, P. McVay, A. Martin, A. Majumdar, K. M. Jatavallabhula, P. Thomas, R. Partsey, D. Dugas, A. Gejji, A. Sax _et al._ , “Locate 3d: Real-world object localization via self-supervised learning in 3d,” _arXiv preprint arXiv:2504.14151_ , 2025. 13 

- [21] J. Bjorck, F. Castañeda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang _et al._ , “Gr00t n1: An open foundation model for generalist humanoid robots,” _arXiv preprint arXiv:2503.14734_ , 2025. 14 

- [22] J. Johannemann, V. Hadad, S. Athey, and S. Wager, “Sufficient representations for categorical variables,” 2021. [Online]. Available: https://arxiv.org/abs/1908.09874 15 

17 

