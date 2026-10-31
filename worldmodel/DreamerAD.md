---
title: "DreamerAD: Efficient Reinforcement Learning via Latent World Model for Autonomous Driving"
date: "2026-03-25"
authors: "Pengxuan Yang; Yupeng Zheng; Deheng Qian; Zebin Xing; Qichao Zhang; Linbo Wang"
url: https://arxiv.org/abs/2603.24587
pdf: https://arxiv.org/pdf/2603.24587
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.24587)** / [論文ページ](https://arxiv.org/abs/2603.24587)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **DreamerAD: Efficient Reinforcement Learning via Latent World Model for Autonomous Driving** 

Pengxuan Yang<sup>1</sup><sup>_,_2</sup><sup>_,_3</sup><sup>_⋆_</sup> , Yupeng Zheng<sup>1</sup><sup>_⋆⋆_</sup> , Zebin Xing<sup>1</sup> , Qichao Zhang<sup>1</sup><sup>_,_4</sup><sup>_†_</sup> , Deheng Qian<sup>2</sup><sup>_†_</sup> , Linbo Wang<sup>1</sup><sup>_,_</sup> , Yichen Zhang<sup>1</sup> , Shaoyu Guo<sup>1</sup> , Zhongpu Xia<sup>1</sup> , Qiang Chen<sup>2</sup> , Junyu Han<sup>2</sup> , Lingyun Xu<sup>2</sup> , Yifeng Pan<sup>2</sup><sup>_⋆⋆_</sup> , and Dongbin Zhao<sup>1</sup> 

> 1 Institute of Automation, CAS 

> 2 Chongqing Chang’an Technology Co., Ltd 

> 3 School of Advanced Interdisciplinary Sciences, UCAS 

> 4 School of Artificial Intelligence, UCAS 

**Abstract.** We introduce DreamerAD, the first latent world model framework that enables efficient reinforcement learning for autonomous driving by compressing diffusion sampling from 100 steps to 1—achieving 80× speedup while maintaining visual interpretability. Training RL policies on real-world driving data incurs prohibitive costs and safety risks. While existing pixel-level diffusion world models enable safe imaginationbased training, they suffer from multi-step diffusion inference latency (2s/frame) that prevents high-frequency RL interaction. Our approach leverages denoised latent features from video generation models through three key mechanisms: (1) shortcut forcing that reduces sampling complexity via recursive multi-resolution step compression, (2) an autoregressive dense reward model operating directly on latent representations for fine-grained credit assignment, and (3) Gaussian vocabulary sampling for GRPO that constrains exploration to physically plausible trajectories. DreamerAD achieves 87.7 EPDMS on NavSim v2, establishing state-ofthe-art performance and demonstrating that latent-space RL is effective for autonomous driving. 

**Keywords:** World Model · Reward Model · Reinforcement Learning 

## **1 Introduction** 

Reinforcement learning (RL) is widely recognized as an effective approach for addressing long-tail problems in autonomous driving, such as distribution shift and causal confusion. Training RL policies on real-world data incurs prohibitive trial-and-error costs and unacceptable safety risks. Conventional simulator-based 

> _⋆_ Work done during internship at Chongqing Chang’an Technology Co., Ltd. 

> _⋆⋆_ Project Leader 

> _†_ Corresponding author. 

2 P. Yang et al. 


**Fig. 1: World model imagination training guided by diverse trajectories.** Each row shows a driving scenario where the world model imagines future outcomes for candidate trajectories. RGB sequences display predicted frames with reward model scores (red: collision risk, green: safe). BEV maps (right) visualize trajectories: hazardous paths (left, red-highlighted) versus safe alternatives (right, green-highlighted). 


**Fig. 2:** PCA visualization of denoised latent features, demonstrating strong spatial and semantic coherence. 

DreamerAD 3 

methods introduce additional sim-to-real discrepancies. World models based on video generation offer a promising alternative by enabling imagination-based policy learning [15, 16]. However, existing pixel-level diffusion models [34] face two critical bottlenecks: (1) multi-step sampling (100 steps) creates severe inference latency incompatible with RL’s interaction demands, and (2) pixel-level objectives prioritize visual fidelity over the spatial and dynamic understanding crucial for driving safety. 

To address these challenges, we propose DreamerAD, a latent world model framework that performs RL entirely within the latent imagination space of a video generation model. Our key insight is to leverage the denoised features from video generation models to construct a latent world model. Specifically, as shown in Fig. 2, we discover that the denoised latent features from Video DiT exhibit well-structured spatial information and semantic coherence. Building upon this latent world model, DreamerAD trains a reward model for RL training. Concretely, we develop an inference-efficient world model by fine-tuning an autoregressive diffusion world model on the NavSim [5] dataset with shortcut forcing, compressing world model sampling from 100 steps to a single step. This enables low-latency RL training in latent space while keeping the features losslessly decodable into high-fidelity RGB frames for rigorous interpretability. Second, we construct an RL algorithm based on latent world model simulation to further enhance planning performance. Specifically, as shown in Fig. 1, we design a reward model that takes latent features conditioned on each action as "imagined inputs" to score each action step, providing dense quality assessment and credit assignment. Building upon the reward model, we propose a Gaussian vocabulary sampling-based GRPO optimization method that selects candidate trajectories from the neighborhood of the trajectory vocabulary based on Gaussian distributions. Compared to the random Gaussian point sampling in prior work [31], neighborhood vocabulary-based sampling ensures effective policy exploration, achieving more physically plausible and smoother trajectory planning. 

We validate DreamerAD on the NavSim v2 closed-loop benchmark. DreamerAD achieves 87.7 EPDMS on NAVSIM v2, establishing a new state-of-the-art. 

## **2 Related Works** 

### **2.1 Autonomous Driving World Models** 

Vision-centric world models [2,9] have gained attention due to their sensor flexibility and data accessibility. Early methods adapted pretrained diffusion models such as Stable Diffusion [25] to driving scenarios but were typically limited to short-term or low-resolution generation and lacked integrated planning capability [8]. Recent approaches utilize video generation as the core simulation component. GAIA-1 [13] adopts autoregressive scene generation, while DriveDreamer [26] and MagicDrive [8] condition diffusion models on BEV maps and 3D bounding boxes. DriveArena [32] and DrivingSphere [29] further advance closed-loop simulation by treating world models as action-conditioned simulators. Voxel-based world modeling approaches explore 3D geometry and spatio- 

4 P. Yang et al. 

temporal dynamics [36]. Large foundation models such as Cosmos [1] achieve high realism but are computationally expensive. Despite these advances, existing world models still struggle with high-frequency RL training due to multistep diffusion inference latency and vulnerability to hallucinations under outof-distribution actions. Our work addresses these issues by reducing sampling complexity and introducing exploration-constrained reinforcement learning. 

### **2.2 Reinforcement Learning in World Models** 

Reducing real-world trial-and-error cost has motivated RL training inside world model imagination spaces. ReSim [30] and OmniNWM [17] use trajectory-conditioned video synthesis for evaluative feedback. The Dreamer series [10–12] performs multi-step latent rollout optimization. In autonomous driving, RAD [7] employs 3D Gaussian Splatting world modeling, while AD-R1 [28] explores RL within occupancy-based representations. However, these methods face limitations in efficiency, annotation dependency, and underutilization of latent world model features. Our framework performs RL entirely within latent imagination space, generating dense reward signals directly from internal representations to provide efficient and precise policy optimization without requiring explicit 3D supervision. 

## **3 Method** 

### **3.1 Overall** 

The overall pipeline of DreamerAD consists of two tightly coupled components: **World Model with Latent Reward Modeling** and **Reinforcement Learning with Vocabulary Sampling** . 

The first component performs imagination-based trajectory evaluation entirely within latent space. As detailed in Section 3.2, the Shortcut Forcing World Model (SF-WM) predicts future scene representations through single-step latent rollouts. The Autoregressive Dense Reward Model (AD-RM) then evaluates these predicted latent states autoregressively to produce step-wise reward signals across eight driving metrics. 

The second component optimizes the policy using trajectories sampled from a predefined high-quality vocabulary. As described in Section 3.3, Gaussianweighted vocabulary sampling ensures exploration remains within physically plausible trajectory manifolds, preventing world model hallucinations during RL training [16]. 

### **3.2 World Model with Latent Reward Modeling** 

This section introduces our latent world modeling framework, which is designed to jointly capture future scene dynamics and trajectory evolution. We first present the foundational world model used to construct latent-space predictive 


**Fig. 3: Overview of the DreamerAD RL training architecture.** The RL training pipeline consists of three main stages: 1) **Policy Generation and Sampling (yellow):** Generates a base policy from historical inputs and samples a set of candidate trajectories based on a predefined vocabulary. 2) **RL Training via World Model (green):** Performs latent rollouts for the sampled trajectories to imagine future states. Step-wise rewards are decoded from these latent features and aggregated into a timeaware dense reward. Notably, our latent representations can be losslessly decoded into RGB frames for accident analysis or visualization, though decoding is bypassed during training for efficiency. 3) **Policy Optimization (blue):** Computes group advantages from the dense rewards to optimize the policy network using the GRPO algorithm. 

representations, then describe the proposed SF-WM that significantly reduces sampling steps while preserving prediction fidelity under low-step inference, and finally describe the AD-RM for trajectory evaluation and latent-space reward modeling. 

### **Shortcut Forcing World Model** 

**_Foundation World Model._** To support imagination-based training, we adopt Epona [34] as our backbone world model. Epona is an autoregressive diffusion model based on flow matching that unifies video generation and trajectory planning, enabling future video prediction conditioned on action controls. 

Given historical observations _O ∈_ R<sup>_B×P ×H×W ×_3</sup> and actions _A ∈_ R<sup>_B×P ×_3</sup> , a visual autoencoder and an action encoder compress them into latent embeddings: 


Then image embedding _Z_ is processed by a temporal projection module to obtain _Zproj ∈_ R<sup>_B×P ×L×D_</sup> . Concatenating the projected visual tokens and 

6 P. Yang et al. 

action embeddings along the spatial dimension forms a unified latent representation _E ∈_ R<sup>_B×P ×_(</sup><sup>_L_+3)</sup><sup>_×C_</sup> . The final frame of _E_ is used as a compact condition _F ∈_ R<sup>_B×_(</sup><sup>_L_+3)</sup><sup>_×C_</sup> for the flow matching generator to predict the next-frame latent _z_ ˆ _next ∈_ R<sup>_B×L×C_</sup> and the future trajectory _τpred ∈_ R<sup>_B×T ×_3</sup> . 

The model is jointly trained using the ground-truth next-frame latent _znext_ and future trajectory _τgt_ . Since the original model trained on the NuPlan dataset operates at 10 Hz while the NavSim environment runs at 2 Hz, we first fine-tune the world model on NavSim to adapt to the 2 Hz generation interval before performing step distillation. 

**_Shortcut Forcing World Model._** Foundation models such as Epona requires 100 sampling steps per frame, creating prohibitive latency for high-frequency RL training. To address this limitation, we propose the Shortcut Forcing World Model (SF-WM), which compresses sampling to 1-4 steps while preserving prediction fidelity—achieving up to 80 _×_ faster inference. 

Inspired by shortcut models [6] and diffusion forcing [3], SF-WM introduces a recursive shortcut forcing mechanism that discretizes the continuous flow process into a multi-resolution step space defined by powers of two. The model is conditioned on both the signal level _t_ and the requested step size _d_ through a step embedding. 

Within the rectified flow framework, given conditional latent features _Z_ , we define the interpolation 


where _x_ 0 _∼N_ (0 _, I_ ) and _x_ 1 denotes the clean data latent representation. 

Let _Kmax_ be the maximum sampling steps and _dmin_ = 1 _/Kmax_ . During training, the step size is sampled as 


Training follows a teacher-student distillation scheme. For _d_ = _dmin_ , the model is trained using the standard flow matching loss. For _d > dmin_ , two teacher half-steps are used: 


The target velocity is defined as 


The optimization objective is 


**(b)** Ours: Visual clarity is maintained across time steps during one-step inference. 

**Fig. 4:** Visualization of one-step inference for Epona and Shortcut Forcing World Model. 

where _ω_ ( _t_ ) = 0 _._ 9 _t_ + 0 _._ 1 balances global structure and local detail preservation. 

At inference, SF-WM can be conditioned on a desired step size (e.g., _d_ = 1 _/_ 4) to generate predictions using only 1–4 sampling steps. As shown in Fig. 4, SFWM maintains sharp autoregressive prediction quality under one-step inference, whereas the original model suffers from severe error accumulation and blurring. 

### **Autoregressive Dense Reward Modeling** 

**_Reward Annotation and Labeling._** World models trained on near-expert demonstrations are vulnerable to hallucinations when evaluated on out-of-distribution trajectories with large spatial deviations. To mitigate this issue, we construct a spatially constrained exploration vocabulary. Specifically, from a large vocabulary of 8192 trajectories, we filter candidates within the neighborhood of human driving trajectories. We extract the end state ( _x, y, θ_ ) of each trajectory and compare it with the end state of the corresponding ground-truth trajectory. A trajectory is retained only if it satisfies the lateral and longitudinal constraints _|∆y| ≤ y_ thresh and _|∆x| ≤ x_ thresh, as well as the heading deviation 


We set _x_ thresh = 10m, _y_ thresh = 5m, and _θ_ thresh = 20<sup>_◦_</sup> . 

To avoid excessive concentration in the candidate set, we further apply a uniform sampling strategy based on lateral offsets. The filtered trajectories are sorted by _|∆y|_ , and equally spaced samples are selected to obtain _K_ representative trajectories, forming the final vocabulary _Γ_ = _{τ_<sup>0</sup> _, τ_<sup>1</sup> _, . . . , τ_<sup>_K_</sup> _}_ with _K_ = 256. This ensures the reward model observes trajectories with diverse deviation levels. 

The filtered trajectories are evaluated in the NavSim PDM simulator to obtain eight reward dimensions _r_ = _{r_ nc _, r_ dac _, r_ ddc _, r_ tlc _, r_ ep _, r_ ttc _, r_ lk _, r_ hc _}_ . Unlike prior work that evaluates only full-trajectory scores, we compute rewards under multiple prediction horizons from 0 to 4 _._ 0s with a step of 0 _._ 5s, producing scores across eight time steps _{r_<sup>1</sup> _, r_<sup>2</sup> _, . . . , r_<sup>8</sup> _}_ . This enables the reward model to capture both overall trajectory quality and the temporal evolution of rewards, facilitating the trade-off between short-term safety and long-term planning. 

8 P. Yang et al. 

**_Reward Model Training._** The reward model is parameterized as a neural network that autoregressively predicts trajectory rewards using historical context, formulated as 


where _t ∈{_ 1 _, . . . ,_ 8 _}_ denotes the prediction horizon, and _t <_ 0 represents historical time steps. 

During inference, the world model in Section 3.2 is frozen and autoregressively predicts latent future representations _{z_ ˆ1 _, . . . ,_ ˆ _zt}_ conditioned on trajectory inputs traj0: _t_ and latent context _Z_ . Historical information is encoded through a multi-layer perceptron: 


Since the latent dimension _L_ = 512 is high, a learnable query-based compression mechanism reduces it to _l_ = 32. To distinguish the eight reward dimensions, we initialize eight independent learnable bases _Q_ base _∈_ R<sup>8</sup><sup>_×D_</sup> . Dynamic trajectory and temporal information are encoded as 


and the reward query is defined as 


Reward representations are decoded through cross-attention followed by an MLP head: 


Training is supervised using binary cross-entropy loss: 


where _ωk_ and _γ_ ( _t_ ) denote reward-type and temporal weighting factors respectively. 

### **3.3 Reinforcement Learning with Vocabulary Sampling** 

This section presents a reinforcement learning framework for trajectory optimization in latent imagination space. We design a safety-prioritized reward formulation that separates safety compliance and task performance signals, introduce dense temporal reward aggregation to reduce reward sparsity, and adopt Gaussian-guided vocabulary sampling for balanced exploration. Policy optimization is performed using a GRPO-based actor training scheme with behavioral cloning and KL regularization for stable training. 

DreamerAD 9 

**_Reward Design for RL._** Traditional reinforcement learning methods often combine rewards using simple weighted summations, which may neglect the varying importance of different reward components. In autonomous driving, safety is treated as the primary optimization constraint. 

Following NavSim [5], we partition the eight reward dimensions into safety terms _r_ safe = _{r_ nc _, r_ dac _, r_ ddc _, r_ tlc _}_ and task performance terms _r_ task = _{r_ ep _, r_ ttc _, r_ lk _, r_ hc _}_ . The safety compliance reward is formulated using a log-sigmoid aggregation: 


while the task reward is computed as 


The total reward is defined as 


for _t ∈{_ 0 _,_ 1 _, . . . ,_ 7 _}_ . The logarithmic fusion mechanism ensures that safety violations dominate the reward signal, as collision events drive the safety term toward zero and consequently push log( _ri_ ) toward negative infinity. 

To mitigate reward sparsity in trajectory-level scoring, we introduce steplevel dense rewards for temporal credit assignment. Instead of evaluating only full-trajectory outcomes, we retain trajectory quality signals across intermediate prediction horizons. The final reward is computed as 


allowing the model to identify degradation points along the trajectory and better guide optimization. 

**_Vocabulary Sampling._** Previous stochastic Gaussian exploration methods [31, 38] often suffer from dynamic inconsistency or limited multimodal coverage due to deterministic flow matching sampling. To address this limitation, we propose a Gaussian-based vocabulary sampling strategy to enable more reliable and diverse trajectory exploration. The model first extracts historical and environmental latent representations to generate a baseline trajectory _τ_ act _∈_ R<sup>_B×T ×_3</sup> . Using _τ_ act as the mean and a fixed variance _σ_<sup>2</sup> , we construct a Gaussian distribution: 


10 P. Yang et al. 

Since the logarithmic Gaussian likelihood is proportional to the negative Mahalanobis distance, trajectory candidates are ranked by computing the Mahalanobis distance between vocabulary trajectories _Γ ∈_ R<sup>_N×T ×_3</sup> and the policy trajectory: 


A mixed sampling strategy is adopted by selecting _g_ 1 trajectories according to softmax probabilities for discrimination and _g_ 2 trajectories from the Gaussian neighborhood for local exploration, yielding a sampled trajectory set _τ_ sample _∈_ R<sup>_B×G×T ×_3</sup> where _G_ = _g_ 1 + _g_ 2. The sampled trajectories are evaluated by the reward model to obtain final rewards _r_ final<sup>_i_.</sup> 

**_Policy Optimization._** Policy learning is performed using the GRPO algorithm. The normalized group advantage is computed as 


To constrain policy updates, an importance ratio is used: 


The actor loss is 


We further regularize training using behavioral cloning loss _L_ bc = _∥τ_ act _− τ_ gt _∥_ 1 and KL divergence loss _L_ kl = _D_ KL( _πθ∥π_ ref). The final objective is 


We also evaluate Flow-GRPO [23], an RL method designed for flow matching architectures, with detailed discussion provided in the supplementary material. 

## **4 Experiment** 

### **4.1 Dataset** 

We evaluate DreamerAD on the NavSim dataset, which was built upon nuPlan and provides surround-view images from 8 cameras along with high-quality LiDAR point clouds. The dataset is split into 1,192 training scenes and 136 testing scenes. During the collection process, static scenarios and constant-speed driving scenarios were excluded to retain highly challenging scenarios. NavSim offers a simulation environment for closed-loop evaluation. NavSim v1 adopts the Predictive Driver Model Score (PDMS) as the evaluation metric, which aggregates 

DreamerAD 11 

multiple driving-related criteria including no collisions (NC), drivable area compliance (DAC), time-to-collision (TTC), comfort (Comf.), and ego progress (EP). Building upon this, NavSim v2 introduces the extended PDM Score (EPDMS), incorporating factors such as driving direction compliance (DDC), traffic light compliance (TLC), lane keeping (LK), history comfort (HC), and extended comfort (EC). Metric introduction and calculation method are further detailed in the supplementary material. 

### **4.2 Implementation Details** 

We utilize Epona, which was trained on NuPlan and NuScenes datasets from scratch, as our foundational world model. All images are resized to 512×1024. All training runs are executed on 32 NVIDIA H20 GPUs. To facilitate generation and planning on the NavSim dataset, we format the NavSim data and apply the AdamW optimizer with a batch size of 128, a learning rate of 3 _×_ 10<sup>_−_5</sup> , and a weight decay of 5 _×_ 10<sup>_−_2</sup> . The fine-tuning process spans 5 epochs over approximately one day. During the shortcut forcing world model training stage, we train for 12 epochs over three days using identical parameters. For reward model training, we apply a batch size of 320 and a learning rate of 3 _×_ 10<sup>_−_4</sup> for 12 epochs, completing in about one week. In the reinforcement learning phase, we use a batch size of 196 and a learning rate of 1 _×_ 10<sup>_−_4</sup> to fine-tune for 2 epochs over approximately 8 hours. Inference speed reports are measured on a single NVIDIA H20 GPU. We set our VisDiT sampling steps to 1 and TrajDiT sampling steps to 20 across all experiments. 

### **4.3 Main Results** 

As demonstrated in Table 1, our method achieves state-of-the-art performance on the NAVSIM v2 closed-loop planning benchmark. Our approach yields an EPDMS of 87.7, outperforming all existing methods and surpassing the Epona baseline by **2.6** points. This demonstrates that conducting reinforcement learning within a latent space is highly effective. Furthermore, our approach significantly outperforms Epona in critical safety metrics, improving no collisions (NC) by 0.9, time-to-collision (TTC) by 1.1, and drivable area compliance (DAC) by 1.5. These gains demonstrate that imagination-based trial-and-error learning enables the model to acquire robust obstacle avoidance capabilities. The 0.8-point decrease in ego progress (EP) reflects a deliberate safety-first trade-off: prioritizing collision avoidance inherently reduces driving aggressiveness. Additionally, we achieve substantial improvements in lane keeping (LK), history comfort (HC), and extended comfort (EC). These gains indicate that after imagination-based training, the model develops a deeper understanding of driving behaviors and enhances its multi-dimensional driving capabilities. 

Furthermore, as shown in Table 2, our method achieves a state-of-the-art score of 88.7 among all world-model-based methods on NAVSIM v1. It outperforms the Epona baseline by **2.5** points overall, with a 2.1 increase in DAC and 

12 P. Yang et al. 

**Table 1: Comparison with state-of-the-art methods on the NAVSIM v2 [5] with extended metrics.** + and - denote improvement/degradation relative to Epona. 

|**Method**|**NC** _↑_|**DAC** _↑_|**DDC** _↑_|**TLC** _↑_|**EP** _↑_|**TTC** _↑_|**LK** _↑_|**HC** _↑_|**EC** _↑_|**EPDMS** _↑_|
|---|---|---|---|---|---|---|---|---|---|---|
|TransFuser [24]|96.9|89.9|97.8|99.7|87.1|95.4|92.7|**98.3**|87.2|76.7|
|hydramdp++ [20]|97.2|97.5|99.4|99.6|83.1|96.5|94.4|98.2|70.9|81.4|
|DriveSuprim [22]|97.5|96.5|99.4|99.6|88.4|96.6|95.5|**98.3**|77.0|83.1|
|ipad [35]|**98.7**|97.8|99.1|**99.8**|83.5|98.0|96.2|98.1|85.6|84.1|
|ReCogDrive [38]|98.3|95.2|**99.5**|**99.8**|87.1|97.5|96.6|**98.3**|86.5|83.6|
|DiffusionDrive [21]|98.2|95.9|99.4|**99.8**|87.5|97.3|96.8|**98.3**|**87.7**|84.5|
|DriveVLA-W0 [18]|98.5|**99.1**|98.0|99.7|86.4|**98.1**|93.2|97.9|58.9|86.1|
|World4Drive [37]|97.8|96.3|99.4|**99.8**|88.3|97.1|**97.7**|98.0|53.9|84.8|
|WorldRFT [31]|97.8|96.5|**99.5**|**99.8**|88.5|97.0|97.4|98.1|69.1|86.7|
|Epona (Base) [34]|97.1|95.7|99.3|99.7|**88.6**|96.3|97.0|98.0|67.8|85.1|
|**Ours**|98.0+0|_._9 97.2+1|_._5 **99.5**+0_._|2 **99.8**+0_._|1<br>87.8_−_|0_._8 97.4+1_._|1 97.5+0|_._5**98.3**+0|_._372.4+4_._|6<br>**87.7**+2_._6|


**Table 2: Comparison with state-of-the-art methods on the NAVSIM v1 [5].** + and - denote improvement/degradation relative to Epona. 

|**Method**|**Venue**|**Input**|**NC** _↑_|**DAC** _↑_|**TTC** _↑_|**Comf** _↑_|**EP** _↑_|**PDMS** _↑_|
|---|---|---|---|---|---|---|---|---|
|VADV2 [4]|arXiv 2024|C&L|97.2|89.1|91.6|**100.0**|76.0|80.9|
|UniAD [14]|CVPR 2023|C&L|97.8|91.9|92.9|**100.0**|78.8|83.4|
|TransFuser [24]|IEEE TPAMI|C&L|97.7|92.8|92.8|**100.0**|79.2|84.0|
|PARA-Drive [27]|CVPR 2024|C&L|97.9|92.4|93.0|99.8|79.3|84.0|
|DRAMA [33]|arXiv 2024|C&L|98.0|93.1|94.8|**100.0**|80.1|85.5|
|Hydra-MDP [20]|arXiv 2024|C&L|98.3|96.0|94.6|**100.0**|78.7|86.5|
|WOTE [19]|ICCV 2025|C&L|98.5|96.8|94.9|99.9|81.9|88.3|
|DriveVLA-W0 [18]|NeurIPS 2025|C&L|**98.7**|96.2|95.5|**100.0**|82.2|88.4|
|AutoVLA [39]|NeurIPS 2025|C-Only|98.4|95.6|**98.0**|99.9|81.9|89.1|
|RecogDrive [38]|NeurIPS 2025|C-Only|97.9|**97.3**|94.9|**100.0**|**87.3**|**90.8**|
|World4Drive [37]|ICCV 2025|C-Only|97.4|94.3|92.8|**100.0**|79.9|85.1|
|WorldRFT [31]|AAAI 2026|C-Only|97.8|96.8|94.0|**100.0**|81.7|87.8|
|Epona (Base) [34]|ICCV 2025|C-Only|97.9|95.1|93.8|99.9|80.4|86.2|
|**Ours**|-|C-Only|98.0+0|_._197.2+2_._1|94.3+0|_._5**100.0**+0|_._183.1+2_._|7<br>88.7+2_._5|


a 0.5 increase in TTC. These consistent improvements across core safety metrics further validate the effectiveness of our latent imagination training for safe driving. While our overall score is slightly lower than those of AutoVLA and RecogDrive, this is due to differences in the training setup. Those VLA methods rely on more powerful representations from stronger encoders. In contrast, our method achieves highly competitive results using an encoder pre-trained solely on unsupervised driving videos. 

In conclusion, our experimental results show that imagination-based reinforcement learning in latent space—driven by extensive trial-and-error interaction—significantly enhances the safety of driving models, demonstrating strong potential for industrial application. 

### **4.4 Ablation Studies** 

**Impact of Shortcut Forcing Method** As shown in Table 3, ID 1 represents the Epona baseline. Comparing ID 2 (without Shortcut Forcing) and ID 4 (our 

DreamerAD 13 

**Table 3:** Ablation study of each component. SF-WM: Shortcut Forcing World Model, AD-RM: Autoregressive Dense Reward Model, RL-SM: RL Sampling Method. Onestep inference is used by default during training unless otherwise specified. 

|ID|SF-WM|AD-RM|Vocab Sampling|RL-SM<br>WorldRFT|Flow-GRPO|EPDMS _↑_|
|---|---|---|---|---|---|---|
|1||||||85.1|
|2<br>3|_√_|_√_|_√_<br>_√_|||86.4<br>87.0|
|4|_√_|_√_|_√_|||**87.7**|
|5|_√_|_√_||_√_||86.6|
|6|_√_|_√_|||_√_|87.0|


**Table 4:** Ablation study of Shortcut Forcing world model inference steps. 

**Table 5:** Ablation study of reward model training data scale. 

|Steps|Latency/Frame (s)|_↓_EPDMS _↑_|Data Scale<br>|EPDMS _↑_|
|---|---|---|---|---|
|16<br>4<br>1|0.40<br>0.10<br>**0.03**|87.7<br>**87.8**<br>87.7|Epona Baseline<br>20% Training Data<br>40% Training Data<br>100% Training Data|85.1<br>87.5<br>87.5<br>**87.7**|


full method) demonstrates that Shortcut Forcing (SF) significantly improves driving performance, indicating that SF successfully enhances generation quality even under extreme step compression. 

Furthermore, as detailed in Table 4, single-step inference utilizing our SF method achieves an EPDMS score of 87.7 with an ultra-low latency of just 0.03s. This performance is highly competitive with the 16-step and 4-step settings while operating at a fraction of the time cost. This proves that compressing sampling steps does not compromise downstream policy planning. Ultimately, our single-step inference provides sufficiently rich and robust representations to fully support imagination-based reinforcement learning. 

**Effectiveness of Autoregressive Dense Reward Model.** As shown in Table 3, comparing IDs 3 and 4 proves the effectiveness of the autoregressive Dense Reward Model (AD-RM), as it provides crucial temporal-grained reward signals. 

To further evaluate its robustness, we trained the reward model using different proportions of the training dataset under identical configurations. As shown in Table 5, the results show very little difference between using 100% of the data and just 20% of the data. This indicates that our reward model and training framework successfully learn the essential differences between good and bad driving behaviors purely based on the future states imagined by the world model. It demonstrates that our AD-RM has strong generalization capabilities and broad application potential, requiring only a small amount of data to yield a robust reward signal. 

14 P. Yang et al. 

**Effectiveness of Vocab Sampling Method** As shown in Table 3, IDs 4, 5, and 6 compare three different reinforcement learning sampling methods. ID 4 uses our proposed vocabulary-based sampling, ID 5 uses WorldRFT [31], and ID 6 uses Flow-GRPO [23]. 

WorldRFT causes severe dynamic discontinuity in the sampled trajectories. For a world model that requires high dynamic accuracy, this amplifies hallucinations and increases prediction bias in the reward model. Flow-GRPO attempts to force exploration by directly altering the deterministic Ordinary Differential Equation (ODE) sampling process of flow matching into a Stochastic Differential Equation (SDE) process. This creates a mismatch with the flow training mode and still results in jagged trajectories, though its strong denoising ability makes it perform slightly better than WorldRFT. In contrast, our vocabulary-based Gaussian sampling method generates high-quality trajectories with complete, smooth dynamics. It perfectly complements our autoregressive dense reward model and achieves the best overall performance. 

### **4.5 Qualitative Results** 

In this section, we qualitatively evaluate DreamerAD on the NavSim dataset. As shown in Figure. 5, zooming in on the Bird’s-Eye View (BEV) maps in rows 1, 2, and 3 reveals that the Supervised Fine-Tuning (SFT) trajectory maintains an excessively high speed, resulting in collisions with stationary vehicles ahead. Additionally, in row 4, the SFT model collides with the curb. Conversely, after Reinforcement Learning (RL) training, the model successfully decelerates and stops appropriately behind the stationary vehicles in rows 1, 2, and 3. In row 4, it correctly adjusts its heading to navigate through safely. This demonstrates that by training within the imagination environment, the model comprehends the severe consequences of poor driving trajectories. Through trial-and-error, it successfully learns safe driving behaviors and accurate decision-making. 

## **5 Conclusion** 

We presented DreamerAD, a framework for reinforcement learning within a visually interpretable latent world model for autonomous driving through three key innovations: shortcut forcing for 80× faster world model inference, autoregressive dense reward modeling for fine-grained credit assignment, and Gaussian vocabulary sampling for physically plausible exploration. DreamerAD achieves 87.7 EPDMS on NavSim v2, establishing a new state- of-the-art for closed-loop planning, validating that imagination-based RL training in latent space can effectively learn safe driving behaviors without real-world trial-and-error, opening new avenues for scalable autonomous driving policy optimization. 

DreamerAD 15 


**Fig. 5:** Comparison before and after RL training. The leftmost column displays the front-view camera image at the current timestep. The right columns show the BEV planning results from SFT and RL, respectively. The red trajectory represents the SFT output, while the blue represents the RL output. Red highlights in the SFT BEV maps indicate collisions, whereas green highlights in the RL BEV maps denote safe passage. 

## **References** 

1. Agarwal, N., Ali, A., Bala, M., Balaji, Y., Barker, E., Cai, T., Chattopadhyay, P., Chen, Y., Cui, Y., Ding, Y., et al.: Cosmos world foundation model platform for physical ai. arXiv preprint arXiv:2501.03575 (2025) 

2. Babaeizadeh, M., Finn, C., Erhan, D., Campbell, R.H., Levine, S.: Stochastic variational video prediction. arXiv preprint arXiv:1710.11252 (2017) 

3. Chen, B., Martí Monsó, D., Du, Y., Simchowitz, M., Tedrake, R., Sitzmann, V.: Diffusion forcing: Next-token prediction meets full-sequence diffusion. Advances in Neural Information Processing Systems **37** , 24081–24125 (2024) 

4. Chen, S., Jiang, B., Gao, H., Liao, B., Xu, Q., Zhang, Q., Huang, C., Liu, W., Wang, X.: Vadv2: End-to-end vectorized autonomous driving via probabilistic planning. arXiv preprint arXiv:2402.13243 (2024) 

5. Dauner, D., Hallgarten, M., Li, T., Weng, X., Huang, Z., Yang, Z., Li, H., Gilitschenski, I., Ivanovic, B., Pavone, M., Geiger, A., Chitta, K.: Navsim: Datadriven non-reactive autonomous vehicle simulation and benchmarking. arXiv preprint arXiv:2406.15349 (2024) 

16 P. Yang et al. 

6. Frans, K., Hafner, D., Levine, S., Abbeel, P.: One step diffusion via shortcut models. arXiv preprint arXiv:2410.12557 (2024) 

7. Gao, H., Chen, S., Jiang, B., Liao, B., Shi, Y., Guo, X., Pu, Y., Yin, H., Li, X., Zhang, X., Zhang, Y., Liu, W., Zhang, Q., Wang, X.: Rad: Training an end-to-end driving policy via large-scale 3dgs-based reinforcement learning. arXiv preprint arXiv:2502.13144 (2025) 

8. Gao, R., Chen, K., Xie, E., Hong, L., Li, Z., Yeung, D.Y., Xu, Q.: Magicdrive: Street view generation with diverse 3d geometry control. arXiv preprint arXiv:2310.02601 (2023) 

9. Ha, D., Schmidhuber, J.: Recurrent world models facilitate policy evolution. Advances in neural information processing systems **31** (2018) 

10. Hafner, D., Lillicrap, T., Ba, J., Norouzi, M.: Dream to control: Learning behaviors by latent imagination. arXiv preprint arXiv:1912.01603 (2019) 

11. Hafner, D., Lillicrap, T., Norouzi, M., Ba, J.: Mastering atari with discrete world models. arXiv preprint arXiv:2010.02193 (2020) 

12. Hafner, D., Pasukonis, J., Ba, J., Lillicrap, T.: Mastering diverse domains through world models. arXiv preprint arXiv:2301.04104 (2023) 

13. Hu, A., Russell, L., Yeo, H., Murez, Z., Fedoseev, G., Kendall, A., Shotton, J., Corrado, G.: Gaia-1: A generative world model for autonomous driving. arXiv preprint arXiv:2309.17080 (2023) 

14. Hu, Y., Yang, J., Chen, L., Li, K., Sima, C., Zhu, X., Chai, S., Du, S., Lin, T., Wang, W., Lu, L., Jia, X., Liu, Q., Dai, J., Qiao, Y., Li, H.: Planning-oriented autonomous driving. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 17853–17862 (2023) 

15. Jiang, Z., Liu, K., Qin, Y., Tian, S., Zheng, Y., Zhou, M., Yu, C., Li, H., Zhao, D.: World4rl: Diffusion world models for policy refinement with reinforcement learning for robotic manipulation. arXiv preprint arXiv:2509.19080 (2025) 

16. Jiang, Z., Zhou, S., Jiang, Y., Huang, Z., Wei, M., Chen, Y., Zhou, T., Guo, Z., Lin, H., Zhang, Q., et al.: Wovr: World models as reliable simulators for post-training vla policies with rl. arXiv preprint arXiv:2602.13977 (2026) 

17. Li, B., Ma, Z., Du, D., Peng, B., Liang, Z., Liu, Z., Ma, C., Jin, Y., Zhao, H., Zeng, W., et al.: Omninwm: Omniscient driving navigation world models. arXiv preprint arXiv:2510.18313 (2025) 

18. Li, Y., Shang, S., Liu, W., Zhan, B., Wang, H., Wang, Y., Chen, Y., Wang, X., An, Y., Tang, C., et al.: Drivevla-w0: World models amplify data scaling law in autonomous driving. arXiv preprint arXiv:2510.12796 (2025) 

19. Li, Y., Wang, Y., Liu, Y., He, J., Fan, L., Zhang, Z.: End-to-end driving with online trajectory evaluation via bev world model. In: Proceedings of the IEEE/CVF International Conference on Computer Vision. pp. 27137–27146 (2025) 

20. Li, Z., Li, K., Wang, S., Lan, S., Yu, Z., Ji, Y., Li, Z., Zhu, Z., Kautz, J., Wu, Z., Jiang, Y., Alvarez, J.M.: Hydra-mdp: End-to-end multimodal planning with multi-target hydra-distillation. arXiv preprint arXiv:2406.06978 (2024) 

21. Liao, B., Chen, S., et al.: Diffusiondrive: Truncated diffusion model for end-toend autonomous driving. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (2025) 

22. Liu, C., Wang, Z., Huang, Y., Zhao, H.: Drivesupreme: Towards end-to-end autonomous driving via scalable world modeling. arXiv preprint arXiv:2405.12345 (2024) 

23. Liu, J., Liu, G., Liang, J., Li, Y., Liu, J., Wang, X., Wan, P., Zhang, D., Ouyang, W.: Flow-grpo: Training flow matching models via online rl. arXiv preprint arXiv:2505.05470 (2025) 

DreamerAD 17 

24. Prabhu, P., Vora, A., Rangesh, A., Trivedi, M.M.: Transfuser: Imitation with transformer-based sensor fusion for autonomous driving. In: 2021 IEEE International Conference on Robotics and Automation (ICRA). p. 663–670. IEEE (2021) 

25. Rombach, R., Blattmann, A., Lorenz, D., Esser, P., Ommer, B.: High-resolution image synthesis with latent diffusion models. In: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. pp. 10684–10695 (2022) 

26. Wang, X., Zhu, Z., Huang, G., Chen, X., Zhu, J., Lu, J.: Drivedreamer: Towards real-world-drive world models for autonomous driving. In: Proceedings of the European Conference on Computer Vision. pp. 55–72. Springer (2024) 

27. Weng, X., Ivanovic, B., Wang, Y., Wang, Y., Pavone, M.: Para-drive: Parallelized architecture for real-time autonomous driving. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 15449–15458 (2024) 

28. Yan, T., Tang, T., Gui, X., Li, Y., Zhesng, J., Huang, W., Kong, L., Han, W., Zhou, X., Zhang, X., et al.: Ad-r1: Closed-loop reinforcement learning for end-to-end autonomous driving with impartial world models. arXiv preprint arXiv:2511.20325 (2025) 

29. Yan, T., Wu, D., Han, W., Jiang, J., Zhou, X., Zhan, K., Xu, C.z., Shen, J.: Drivingsphere: Building a high-fidelity 4d world for closed-loop simulation. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 27531–27541 (2025) 

30. Yang, J., Chitta, K., Gao, S., Chen, L., Shao, Y., Jia, X., Li, H., Geiger, A., Yue, X., Chen, L.: Resim: Reliable world simulation for autonomous driving. arXiv preprint arXiv:2506.09981 (2025) 

31. Yang, P., Lu, B., Xia, Z., Han, C., Gao, Y., Zhang, T., Zhan, K., Lang, X., Zheng, Y., Zhang, Q.: Worldrft: Latent world model planning with reinforcement finetuning for autonomous driving. arXiv preprint arXiv:2512.19133 (2025) 

32. Yang, X., Wen, L., Wei, T., Ma, Y., Mei, J., Li, X., Lei, W., Fu, D., Cai, P., Dou, M., et al.: Drivearena: A closed-loop generative simulation platform for autonomous driving. In: Proceedings of the IEEE/CVF International Conference on Computer Vision. pp. 26933–26943 (2025) 

33. Yuan, C., Zhang, Z., Sun, J., Sun, S., Huang, Z., Lee, C.D.W., Li, D., Han, Y., Wong, A., Tee, K.P., et al.: Drama: An efficient end-to-end motion planner for autonomous driving with mamba. arXiv preprint arXiv:2408.03601 (2024) 

34. Zhang, K., Tang, Z., Hu, X., Pan, X., Guo, X., Liu, Y., Huang, J., Yuan, L., Zhang, Q., Long, X.X., et al.: Epona: Autoregressive diffusion world model for autonomous driving pp. 27220–27230 (2025) 

35. Zhang, T., Liu, Y., Wang, C., Zhao, H.: i-pad: Interactive planning for autonomous driving via diffusion models. arXiv preprint arXiv:2402.04312 (2024) 

36. Zheng, W., Chen, W., Huang, Y., Zhang, B., Duan, Y., Lu, J.: Occworld: Learning a 3d occupancy world model for autonomous driving. In: Proceedings of the European Conference on Computer Vision. pp. 55–72. Springer (2024) 

37. Zheng, Y., Yang, P., Xing, Z., Zhang, Q., Zheng, Y., Gao, Y., Li, P., Zhang, T., Xia, Z., Jia, P., Zhao, D.: World4drive: End-to-end autonomous driving via intentionaware physical latent world model. arXiv preprint arXiv:2507.00603 (2025) 

38. Zhou, Y., Chen, Z., Zhang, Y., Zhao, H.: Recogdrive: Reinforced cognitive world model for autonomous driving. arXiv preprint arXiv:2405.17325 (2024) 

39. Zhou, Z., Cai, T., Zhao, S.Z., Zhang, Y., Huang, Z., Zhou, B., Ma, J.: Autovla: A vision-language-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning. arXiv preprint arXiv:2506.13757 (2025) 

