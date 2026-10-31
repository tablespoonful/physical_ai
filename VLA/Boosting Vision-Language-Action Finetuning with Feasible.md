---
title: "Boosting Vision-Language-Action Finetuning with Feasible Action Neighborhood Prior"
date: "2026-04-02"
authors: "Haochen Niu; Kanyu Zhang; Shuyu Yin; Qinghai Guo; Peilin Liu; Fei Wen"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2604.01570
pdf: https://arxiv.org/pdf/2604.01570
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.01570)** / [論文ページ](https://arxiv.org/abs/2604.01570)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **Boosting Vision-Language-Action Finetuning with Feasible Action Neighborhood Prior** 

Haochen Niu<sup>1</sup><sup>_,∗_</sup> Kanyu Zhang<sup>1</sup><sup>_,∗_</sup> Shuyu Yin<sup>1</sup> Qinghai Guo<sup>2</sup> Peilin Liu<sup>1</sup> Fei Wen<sup>1</sup><sup>_,†_</sup> 1 Shanghai Jiao Tong University, China 

2Huawei Technologies, China 

_{_ haochen ~~n~~ iu,kane ~~z~~ hang2024,shuyu.yin,liupeilin,wenfei _}_ @sjtu.edu.cn, guoqinghai@huawei.com _∗_ Equal contribution _†_ Corresponding author 

## **Abstract** 

_In real-world robotic manipulation, states typically admit a neighborhood of near-equivalent actions. That is, for each state, there exist a feasible action neighborhood (FAN) rather than a single correct action, within which motions yield indistinguishable progress. However, prevalent VLA training methodologies are directly inherited from linguistic settings and do not exploit the FAN property, thus leading to poor generalization and low sample efficiency. To address this limitation, we introduce a FAN-guided regularizer that shapes the model’s output distribution to align with the geometry of FAN. Concretely, we introduce a Gaussian prior that promotes locally smooth and unimodal predictions around the preferred direction and magnitude. In extensive experiments across both reinforced finetuning (RFT) and supervised finetuning (SFT), our method achieves significant improvement in sample efficiency, and success rate in both in-distribution and out-of-distribution (OOD) scenarios. By aligning with the intrinsic action tolerance of physical manipulation, FAN-guided regularization provides a principled and practical method for sample-efficient, and generalizable VLA adaptation. The source code is publicly available at: https://github.com/HaochenNiu/FAN-VLA._ 

## **1. Introduction** 

Benefiting from advances in large-scale foundation models, vision-language-action (VLA) models have recently emerged as a unifying paradigm for general robotic manipulation [2, 4, 5, 22, 23, 57]. A VLA model integrates vision perception, language understanding, and low-level control within a single model, which enables an end-to-end mapping from “seeing and understanding” to “acting”. A common design of VLA models leverages an autoregressive language-model backbone, by discretizing each action 

dimension into a set of bins and encoding the motion as “action tokens”. 

In practice, deploying a VLA model typically involves two stages: (i) Pretraining on large-scale heterogeneous VLA data to learn a general pretrained model. (ii) finetuning on a specific robot platform or environment to adapt to the system’s embodiment, sensory configuration, and physical dynamics. For the second stage, there are mainly two finetuning paradigms: supervised finetuning (SFT) and reinforced finetuning (RFT). SFT treats offline demonstration trajectories as labeled sequences and uses them for supervised finetuning [22, 55]. In contrast, RFT does not require demonstrations but optimizes a policy using environment rewards through interaction [25, 34, 51]. While SFT is more stable than RFT, it has been recently shown that RFT can yield better generalization [31]. 

Despite the difference in supervision, most VLA training and finetuning methods directly inherit the learning recipes of language models, e.g., next-token prediction with onehot cross-entropy or its reinforcement learning (RL) analogues such as PPO [39] and GRPO [41]. However, unlike in linguistic settings, physical actions possess intrinsic _tolerance_ and _near-equivalence_ , where a neighborhood of an action can yield indistinguishable task progress. 

Yet, this fundamental difference between the linguistic and robotic domains is often overlooked. This oversight causes significant challenges for both common finetuning paradigms. When using SFT with a small taskspecific dataset, which is a common scenario in practice, the model learns to collapse its probability mass onto the single demonstrated action, a clear sign of severe overfitting. Meanwhile, while RFT can eventually produce a broader action distribution for better generalization, the process is highly sample-inefficient. Without an explicit regularization that exploits the intrinsic structure of the action space, the agent must spend much more training time to implicitly discover this beneficial property through exploration. 

27956 

To address this limitation, we revisit VLA training from a geometric and physical-consistency perspective. Our approach begins by formalizing the concept of the Feasible Action Neighborhood (FAN): a set of neighboring actions for each state within which different choices yield nearly equivalent task progress. Building upon this concept, we introduce a novel regularization term designed to shape the model’s output distribution to match the properties of the FAN. Specifically, we model the FAN as a locally unimodal and smooth region by encouraging the output distribution to conform to a target Gaussian. Crucially, this regularizer requires no alterations to the model architecture or auto-regressive decoding scheme, yet it effectively shifts the learning signal from a focus on “exclusive correctness” to one of “weighted tolerance”. This aligns the VLA training objective with the geometry of physical action spaces. The main contributions of this work are as follows: 

- We formalize the notion of FAN to characterize the local tolerance structure of physical actions, and reveal the intrinsic mismatch between standard language-style VLA training and the geometry of real-world physical actions. 

- We introduce a FAN-guided regularizer applicable to both SFT and RFT, which preserves the discreteness and autoregressive nature of VLA models while explicitly aligning the training objective with physical tolerance of realworld manipulation actions. 

- We conduct extensive evaluations across both SFT and RFT regimes, covering diverse VLA backbones and manipulation tasks under both in-distribution and out-ofdistribution (OOD) settings. The results demonstrate significant improvement of the proposed method in sampleefficiency, task success rate, and OOD generalization. 

Our results show that bridging the gap between language-style training objectives and physical tolerance of real-world manipulation actions benefits efficient VLA finetuning. It is worth noting that our method is fundamentally distinct from entropy maximization prior in reinforcement learning. While entropy maximization also encourages distributional outputs, it is typically unstructured and used to promote exploration. In contrast, our method imposes a structured prior shaped by the FAN, which exploits the properties of physical actions to provide a more direct and sample-efficient path towards a generalizable policy. 

## **2. Related Work** 

### **2.1. Foundation Models for Robotics** 

Early robotic systems rely on hand-crafted task specifications and fixed control policies, which have limited generalization [40]. Recently, the progress of large foundation models [1] has motivated exploring lightweight adaptation of general-purpose backbones for scalable and generalizable embodied intelligence. Initial efforts typically adopt 

hierarchical or decoupled paradigms. For example, VoxPoser [21] employs vision-language models (VLMs) to infer voxel-level affordances for planning, while SayCan [6] and ViLA [19] decompose natural-language goals into lowlevel skill executions. Moreover, Code-as-Policies [26] uses large language models to generate robot control code. 

A major paradigm shift came with RT-2 [57], which unifies perception, reasoning, and control within a single VLA framework. VLA architectures typically adopt an autoregressive language model to directly output discrete action tokens for robot execution [13, 15, 22]. Among them, OpenVLA [22] is a widely used baseline, which is pretrained at scale on the Open X-Embodiment dataset [36]. It fuses dual visual encoders, SigLIP [52] and DINOv2 [35], with Llama2-7B [46], and autoregressively predicts 7-DoF action tokens over discretized bins. 

More recent studies have refined VLA architectures to enhance reasoning, action representation, and efficiency. Architecturally, TriVLA [32] leverages pretrained video prediction models for latent temporal cues, while WorldVLA [8] employs auxiliary image prediction for stronger supervision. UniVLA [7] and Villa-X [10] introduce additional training stages to reduce the influence of task-irrelevant dynamics. _π_ 0 [4] and _π_ 0 _._ 5 [5] employ flow matching with continuous action representation, while HybridVLA [30] combines autoregressive and diffusion heads, and VQ-VLA [48] replaces the bin-based tokenizer with a residual VQ-VAE for higher precision. To enhance reasoning, Fast-in-Slow [9] decouples fast manipulation from slow deliberation, while OneTwoVLA [28] employs a control token to switch between reasoning and execution phases. Efficiency-oriented variants include SmolVLA [42] and BitVLA [47], which employ smaller models, while EfficientVLA [50] applies targeted pruning without retraining. Moreover, Gr00t N1 [3] and SpatialVLA [37] focus on sim-to-real transfer. 

### **2.2. Finetuning for VLA Models** 

Despite recent growth in robot manipulation datasets, their scale remains limited compared to NLP corpora [49]. Evidences from various domains highlight the critical role of finetuning in aligning foundation models with downstream objectives, a process even more crucial for VLA models. Most existing VLAs adopt a two-stage training paradigm comprising large-scale pretraining followed by SFT on task-specific demonstrations [23]. However, imitation-based SFT often suffers from significant degradation in OOD scenarios not covered by expert data [14, 56]. 

To overcome this limitation, recent research has drawn inspiration from reinforced finetuning successes in mathematical reasoning and code generation [16, 27], which applies RFT to pretrained VLA models. Several works, such as [18, 25, 31, 51], employ established policy opti- 

27957 

mization algorithms including PPO [39] and GRPO [41], and demonstrate their effectiveness in aligning VLA behaviors with task rewards. ReinboT [53] considers dense reward design and reward-maximization objectives, while VLA-RL [33] introduces a Robot Process Reward Model (RPRM) that replaces sparse binary rewards with pseudorewards derived from gripper actions and task progress, to achieve more stable PPO-based optimization. Methods such as TGRPO [12] and GRAPE [54] leverage powerful VLMs to generate rewards without training explicit reward models. Further, Chunked RL [20] formulates a temporaldifference learning framework tailored to chunked action sequences, and Interactive RL [44] combines REINFORCE leave-one-out (RLOO) advantage estimation [24] with PPO for more stable policy updates. ConRFT [11] combines offline Q-learning with online human-in-the-loop finetuning, while iRe-VLA [17] alternates between online RL and behavior cloning in an iterative training process to balance exploration and stability. 

## **3. Preliminaries** 

**VLA as Markov Decision Processes.** We model the VLA environment as an instruction-conditioned Markov Decision Process (MDP), defined by a tuple ( _S, A, L, r, P, γ_ ), where: _S_ represents the state space; _A_ represents the action space; _L_ is the set of possible natural language instructions; _P_ : _S × A →_ ∆( _S_ ) is the state transition probability function, where ∆( _S_ ) is the set of probability distributions over _S_ ; _r_ : _S × A × L →_ R is the reward function, which depends on the instruction _l ∈ L_ ; _γ ∈_ [0 _,_ 1) is the discount factor. Without loss of generality, we assume the state space and action space both are countable sets. 

The goal of this MDP is to learn an instructionconditioned policy _π_ : _S × L →_ ∆( _A_ ) that maximizes the state values, conditioned on a given instruction _l ∈ L_ . For a given policy _π_ , instruction _l_ , and initial state distribution _µ_ , the discounted state visitation distribution _d_<sup>_π_</sup> _µ_<sup>(</sup><sup>_·_)isdefinedas</sup><sup>_dπ_</sup> _µ_<sup>(</sup><sup>_s_)</sup> = (1 _− γ_ )<sup>�</sup><sup>_∞_</sup> _t_ =0 � _s_<sup>_′_</sup> _,a_<sup>_γtπ_(</sup><sup>_a|s′, l_)</sup><sup>_Pt_(</sup><sup>_s|s′, a_)</sup><sup>_µ_(</sup><sup>_s′_), where</sup><sup>_Pt_is the</sup> _t_ -times transition probability. 

The state-action value function, _Q_<sup>_π_</sup> ( _s, a, l_ ), represents the expected discounted return for taking action _a_ in state _s_ and subsequently following policy _π_ under instruction _l_ : _Q_<sup>_π_</sup> ( _s, a, l_ ) = E _π,P_ [<sup>�</sup><sup>_∞_</sup> _t_ =0<sup>_γtr_(</sup><sup>_st, at_)</sup><sup>_| s_0=</sup><sup>_s, a_0=</sup><sup>_a_]</sup> From this, the state-value function _V_<sup>_π_</sup> and the advantage function _A_<sup>_π_</sup> are defined as the expected value of _Q_<sup>_π_</sup> over actions and the centered _Q_<sup>_π_</sup> value, respectively: _V_<sup>_π_</sup> ( _s, l_ ) = E _a∼π_ ( _·|s,l_ )[ _Q_<sup>_π_</sup> ( _s, a, l_ )] =<sup>�</sup> _a∈A_<sup>_π_(</sup><sup>_a|s, l_)</sup><sup>_Qπ_(</sup><sup>_s, a, l_),and</sup> _A_<sup>_π_</sup> ( _s, a, l_ ) = _Q_<sup>_π_</sup> ( _s, a, l_ ) _− V_<sup>_π_</sup> ( _s, l_ ). 

**Supervised finetuning (SFT).** We represent the VLA model as a policy _πθ_ parameterized by _θ_ . The policy is 

trained using SFT on a dataset of _n_ expert demonstrations, _D_ = _{_ ( _τ_<sup>_i_</sup> _, l_<sup>_i_</sup> ) _}_<sup>_n_</sup> _i_ =1<sup>.</sup> Each demonstration consists of an instruction _l_<sup>_i_</sup> and a corresponding state-action trajectory _τ_<sup>_i_</sup> = _{s_<sup>_i_</sup> 0<sup>_, ai_</sup> 0<sup>_, . . . , si_</sup> _K_<sup>_i_</sup> _−_ 1<sup>_, ai_</sup> _K_<sup>_i_</sup> _−_ 1<sup>_}_,where</sup><sup>_Ki_isthetrajec-</sup> tory length. The objective of SFT is to maximize the likelihood of the expert actions by minimizing the following negative log-likelihood loss: 


**Trust-region-type policy optimization.** Trust-regiontype policy optimization methods, such as PPO and GRPO, are widely adopted for finetuning large models, including VLAs. The core principle of these algorithms is to ensure training stability by restricting the magnitude of policy updates at each step. 

This is formalized as a constrained optimization problem. At each training iteration _t_ , given the current policy _πt_ and the instruction _l ∈ L_ , the objective is to find a new policy _π_ that maximizes the expected advantage, subject to a constraint on the policy distance (typically measured by KL divergence): 


where _DKL_ ( _·∥·_ ) represents the KL divergence. 

In practical implementation, given some trajectories sampled from the policy _πθt_ , PPO employs a clip function to replace the KL divergence term. More specifically, given a sampled trajectory _τ_ = _{s_ 0 _, a_ 0 _, s_ 1 _, a_ 1 _, ..., sK−_ 1 _, aK−_ 1 _}_ of length _K_ , the policy loss is: 


where _It_<sup>_k_</sup> = _πθ_ ( _ak|sk, l_ ) _/πθt_ ( _ak|sk, l_ ) is the importance ratio. The advantage estimation _A_<sup>ˆ</sup> ( _sk, ak_ ) can be calculated using GAE [38] or as the difference between the discounted return and a value baseline, i.e., _A_<sup>ˆ</sup> ( _sk, ak_ ) = � _Ki_ = _−k_ 1<sup>_γi−kr_(</sup><sup>_si, ai, l_)</sup><sup>_−Vϕ_(</sup><sup>_sk, l_).Additionally, the value</sup> function _Vϕ_ is updated by minimizing the mean squared error loss: 


27958 


Figure 1. Geometric structure of policy distribution on a ManiSkill task. (a) After the SFT warm-up stage, the policy learned a narrow, peaked distribution with a minimal FAN, resulting in poor generalization. (b) Subsequent RFT with PPO broadens the distribution, leading to improved task success; (c) Our FAN-PPO method explicitly guides the policy towards a robust Gaussian shape, achieving the highest success rate and demonstrating superior generalization. 

## **4. Feasible Action Neighborhood** 

A defining characteristic of real-world robotic manipulation, which distinguishes it from purely linguistic tasks, is the inherent tolerance in physical actions. For any given state, there typically exists a neighborhood of actions around the optimal action, not just a single action, that can lead to near-identical and successful outcomes. For instance, when grasping an object, if the recorded optimal action is to move the gripper 1 _._ 0 _cm_ to the left, moving it 0 _._ 9 _cm_ or 1 _._ 1 _cm_ would likely be just as effective. To formalize this tolerance region, we utilize the state-action value function, _Q_ ( _s, a_ ), which represents the expected longterm performance: 

**Definition 1** (Feasible Action Neighborhood, FAN) **.** _Let a_<sup>_∗_</sup> ( _s_ ) = arg max _a′∈A Q_ ( _s, a_<sup>_′_</sup> ) _be the optimal action for a given state s. For a tolerance δ >_ 0 _, the FAN, denoted by_ N _δ_ ( _s_ ) _, is the connected set containing a_<sup>_∗_</sup> ( _s_ ) _within the set of actions that yield nearly equivalent Q-values:_ 


_We posit that for any well-posed physical task, this neighborhood is non-trivial, i.e., it forms a region of non-zero volume around a_<sup>_∗_</sup> ( _s_ ) _._ 

While the FAN is formally defined via the _Q_ -function, the policy _π_ ( _a|s_ ) implicitly encodes this information. For common policy formulations (e.g., a softmax over _Q_ - values), actions with similar _Q_ -values are assigned similar probabilities. This implies that the shape of the policy distribution reflects the structure of the FAN. Consequently, the shape of the policy distribution _π_ ( _a|s_ ) serves as a practical and observable proxy for the FAN that the model has learned. A “spiky” narrow distribution corresponds to a small, trivial FAN, while a “broad” smooth distribution indicates a larger, more robust FAN. 

Our empirical analyses reveal a striking correlation between the shape of the policy distribution, which is also the 

size of its implicit FAN, and the model’s generalization performance, as shown in Figure 1. In (a), we observe that the model finetuned with SFT on a small dataset for warming up consistently produces overly-peaked distributions. This indicates it has learned a trivial or near-trivial FAN, leading to poor generalization under perturbation. In contrast, in (b), when the same model is subsequently trained using RFT, its action distributions become broader, indicating the emergence of a larger, more robust FAN. Critically, this broadening of the distribution is directly correlated with a significant improvement in task success rate. This strong empirical evidence, that the policy’s shape is a proxy for robustness, forms the primary motivation for our method. 

## **5. Methodology** 

As established in Section 4, shaping the policy distribution, which serves as a proxy for the FAN, is crucial for improving generalization and sample efficiency during finetuning. Our goal is therefore to guide the policy distribution during training to reflect the properties of an ideal FAN. 

The key properties of a physical FAN are unimodality, smoothness, and local contiguity. These properties are wellmodeled by a Gaussian distribution. Therefore, we introduce a FAN-guided regularizer, defined as the KL divergence between the policy _π_ and a target Gaussian distribution _N_ ( _µ_ ( _s_ ) _,_ Σ( _s_ )): 


where _N_ ( _·|µ_ ( _s_ ) _,_ Σ( _s_ )) denotes the density function of the normal distribution, the mean _µ_ ( _s_ ) = arg max _a π_ ( _a|s_ ) is the policy’s own predicted optimal action for state _s_ , and the covariance matrix Σ( _s_ ) directly controls the size of the FAN. This regularizer can be seamlessly incorporated into both SFT and RFT objectives to actively shape the policy distribution around its peak, transforming it from an overly confident “spike” into a smooth, robust neighborhood. 

27959 

### **5.1. SFT with FAN-Guided Regularization** 

We first incorporate our FAN-guided regularizer into the SFT loss (1). This results in the FAN-SFT loss: 


where _α_ is the regularization coefficient. Here, the covariance is not fixed but is dynamically defined by the variance of the policy: Σ( _s_ ) = diag �� _a∈A_<sup>_π_(</sup><sup>_a|s, l_)(</sup><sup>_a −µ_(</sup><sup>_s_))2�</sup> . This adaptive covariance matrix encourages the policy to adopt a Gaussian shape according to its current geometric property. We employ this dynamic target specifically during SFT because the supervised objective is inherently stable and can accommodate such a variable target without compromising training stability. 

### **5.2. RFT with FAN-Guided Regularization** 

We now adapt our approach for the RFT paradigm. The FAN-guided regularizer is incorporated into a trust-regiontype policy optimization objective, creating a principled trade-off between policy improvement and policy shaping. 

At each update step _t_ , we optimize the policy _π_ based on experience gathered with the current policy _πt_ . Our regularized objective is formulated as the following constrained optimization problem: 


where _α_ is the regularization coefficient. Crucially, to ensure training stability, we use a fixed covariance matrix Σ = _σ_<sup>2</sup> _I_ . Here, _σ >_ 0 is a fixed hyperparameter controlling the target FAN size, and _I_ is the identity matrix. This contrasts with our SFT approach, providing a stable, consistent target shape that helps anchor the policy updates. 

The solution to the constrained optimization problem in (6) has an elegant closed-form structure, which reveals the mechanism of our regularizer. 

**Proposition 1** (Form of the optimal policy) **.** _For a given state s, and any action a ∈ A, the optimal policy πt_ +1 _that solves objective_ (6) _is given by:_ 


_where β_<sup>_∗_</sup> _≥_ 0 _is the optimal Lagrange multiplier for the trust-region constraint._ 

The proof is in the supplementary material. Proposition 1 provides a key insight: the next policy, _πt_ +1, is a geometric interpolation between the previous policy _πt_ and the target Gaussian _N_ ( _µ_ ( _s_ ) _,_ Σ), where the result is then re-weighted by the exponentiated _Q_ -values. The interpolation weights are determined by _α_ and _β_<sup>_∗_</sup> . As the optimal multiplier, _β_<sup>_∗_</sup> is governed by the KKT conditions, which dictate that _β_<sup>_∗_</sup> is inversely related to the trust-region size _ϵ_ . A smaller _ϵ_ forces a larger _β_<sup>_∗_</sup> , which makes the update more conservative by placing more weight on the previous policy _πt_ . Consequently, there is a competition: _α_ governs the strength of the pull towards the Gaussian shape, while _ϵ_ governs the strength of the pull towards the _πt_ . Eventually, finetuning with the FAN-PPO loss guides the policy distribution to approximate the target Gaussian, as illustrated in Figure 1 (c). 

For a practical implementation, we integrate our regularizer into the policy loss (3) to define the FAN-PPO loss: 


where _It_<sup>_k_=</sup><sup>_πθ_(</sup><sup>_ak|sk, l_)</sup><sup>_/πθ_</sup> _t_<sup>(</sup><sup>_ak|sk, l_) is the probability ra-</sup> tio. The advantage _A_<sup>ˆ</sup> is estimated via GAE and the value function is trained using the loss from (4). 

## **6. Experiments** 

We conduct experiments on both SFT and RFT with two representative VLA models: OpenVLA [22], which outputs a single action, and OpenVLA-OFT [23], which outputs action chunks. We consider two widely used robot manipulation benchmarks: Maniskill [45] and LIBERO [29]. We comprehensively evaluate the proposed FAN-guided regularization in terms of absolute performance gains, OOD generalization, sample efficiency, and convergence speed. All experiments are conducted on NVIDIA A100 GPUs with 80GB memory. 

### **6.1. Supervised Finetuning** 

**Implementation details.** On ManiSkill, following [31], we train on PutOnPlateInScene25Main-v3, which comprises 25 diverse pick-and-place manipulation primitives across multiple object categories and target receptacles. We collected a training dataset of the same scale (16K) as RL4VLA [31] using a motion planner within the environment. We use a pre-trained OpenVLA checkpoint from HuggingFace<sup>1</sup> . For robustness evaluation, we assess perfor- 

1https://huggingface.co/gen-robot/openvla-7brlvla-warmup 

27960 

Table 1. Comparison of SFT results on the ManiSkill benchmark. Values denote success rates (%). 

|**Method**|**In-Distribution**||**Out-of-Distr**|**ibution**||
|---|---|---|---|---|---|
|||**Vision**|**Semantic**|**Execution**|**Avg.**|
|RL4VLA [31]|88.5|74.0|61.8|46.2|60.7|
|OpenVLA + SFT [22]|78.1_±_3.1|76.6_±_1.9|57.4_±_0.9|40.4_±_0.8|58.1|
|OpenVLA + FAN-SFT (Ours)<br>|89.8_±_0.8<br>|81.7_±_1.1<br>|63.5_±_1.5<br>|44.8_±_0.5<br>|63.3<br>|
|_△_Improvement|+11.7|+5.1|+6.1|+4.4|+5.2|


Figure 2. SFT performance on OpenVLA with and without FAN-guided regularization across different OOD tasks on ManiSkill. 


Figure 3. SFT performance on OpenVLA with and without FAN-guided regularization across different data sizes on in-distribution and three OOD tasks (Vision, Semantic, Execution). 


Figure 4. Spatial robustness on LIBERO-Spatial, comparing OpenVLA finetuned with SFT (left) versus our FAN-SFT (right). Color indicates success rate; the black and red dashed lines are the equal-success-rate contours for each method, respectively. 

mance under 15 perturbation types spanning visual, semantics, and execution variations. 

For the LIBERO benchmark, we finetune models on the LIBERO-Spatial suite, which consists of 10 tasks, each provided with 50 human-teleoperated demonstrations. We use pre-trained OpenVLA and OpenVLA-OFT checkpoints from HuggingFace<sup>2</sup> . Among them, OpenVLA-OFT uses the variant that simultaneously takes as input the thirdperson image, wrist camera image, robot proprioceptive 

> 2https://huggingface.co/openvla/openvla-7b 


Figure 5. Qualitative comparison under spatial perturbation. Vanilla SFT remains biased toward the seen position, whereas FAN-SFT correctly adapts to the perturbed target location. 

state, and language instruction. Additionally, we follow the setting of LIBERO-PRO [56] and introduce varying degrees of spatial perturbations into the task setup to evaluate the model’s generalization under position-shifted OOD conditions. 

**Main Results.** Table 1 shows that, with FAN-guided regularization, FAN-SFT achieves average improvements of +11.7% and +5.2% on in-distribution and OOD tasks, re- 

27961 

Table 2. Comparison of RFT results on the ManiSkill benchmark. Values denote success rates (%). 

|**Method**|**In-Distribution**||**Out-of-Distr**|**ibution**||
|---|---|---|---|---|---|
|||**Vision**|**Semantic**|**Execution**|**Avg.**|
|RL4VLA[31]|93.8|76.6|72.8|78.3|75.9|
|OpenVLA + PPO|95.9_±_3.2|80.1_±_0.1|79.7_±_2.0|85.8_±_1.8|81.9|
|OpenVLA + FAN-PPO (Ours)<br>|97.4_±_0.7|85.0_±_4.0|86.7_±_1.3|92.6_±_1.5|88.1|
|_△_Improvement|+1.5|+4.9|+7.0|+6.9|+6.2|
|OpenVLA-OFT + PPO|92.3_±_2.5|84.9_±_1.1|49.0_±_0.6|55.9_±_1.2|63.3|
|OpenVLA-OFT + FAN-PPO (Ours)<br>|97.3_±_1.3<br>|88.1_±_2.2<br>|58.6_±_1.0<br>|67.0_±_2.2<br>|71.2<br>|
|_△_Improvement|+5.0|+3.2|+9.6|+11.1|+7.9|


Figure 6. Performance comparison of OpenVLA and OpenVLA-OFT trained with PPO and FAN-PPO across various OOD tasks. 

spectively. As detailed in Fig. 2, our method achieves consistent improvements across all OOD tasks, with the largest absolute gain of 7.2% observed on the Disturb Recep (distractive receptacle) task. These results demonstrate that the proposed regularization significantly enhances the model’s robustness under diverse perturbations. We also compare against label smoothing[43], and the results show that FAN, as a structured regularizer, is more effective. Detailed results are provided in Appendix Table 12. 

We further investigate the effectiveness of FAN-guided regularization under different training data scales. From the collected SFT data, we construct randomly sampled subsets at multiple data scales. Similar to [31], we train for 60K steps when the dataset size is 1.6K or 16K, and for 20K steps for smaller subsets due to data scarcity. Fig. 3 presents the average results on in-distribution and three types of OOD tasks. While the performance of both methods generally improves with increasing data scale, certain fluctuations are observed. Across most data scales, our FAN-guided regularization outperforms the baseline, which demonstrates its effectiveness under varying data sizes. 

On LIBERO, we apply our method to both OpenVLA and OpenVLA-OFT models. On the LIBERO-Spatial suite, our FAN-guided regularization improves the success rate from 84.7% to 87.2% on OpenVLA and from 95.2% to 98.8% on OpenVLA-OFT. We further introduce varying degrees of perturbations along the _x_ and _y_ axes to evaluate the robustness of OpenVLA finetuned with SFT and FANSFT. As shown in Fig. 4, FAN-guided regularization yields 

stronger resilience to positional shifts, increasing the success rate from 0.24 to 0.36 at a perturbation of ( _x_ =0.05, _y_ =0.05), for example. The qualitative results in Fig. 5 further illustrate this effect: after spatial perturbation, the model trained with standard SFT tends to place the bowl at the same plate position seen during training, which indicates overfitting to familiar spatial patterns. In contrast, with FAN-SFT, the model can successfully adapt to unseen positions, demonstrating stronger spatial generalization ability. The complete LIBERO results are provided in Appendix Table 10. 

### **6.2. Reinforced Finetuning** 

**Implementation details.** Considering that ManiSkill supports GPU-parallelized simulation, we conduct RFT on this benchmark. Similar to Sec. 6.1, we interact within the PutOnPlateInScene25Main-v3 environment and subsequently evaluate OOD performance under 15 types of perturbations. 

In the proposed FAN-PPO method, two hyperparameters play crucial roles in controlling the stochasticity and adaptation strength. For OpenVLA, all results are obtained with _σ_ = 0 _._ 3 and _α_ = 1 _._ 0. For OpenVLA-OFT, we use _σ_ = 0 _._ 2 and _α_ = 0 _._ 1. We use the same pre-trained OpenVLA checkpoints as in previous experiments, and the OpenVLAOFT weights are publicly available<sup>3</sup> . 

3https://huggingface.co/RLinf/RLinf-OpenVLAOFTManiSkill-Base-Lora 

27962 


Figure 7. Training curves of rollout and evaluation success rates during RFT of OpenVLA. Our FAN-guided regularization significantly improved the sample efficiency of OpenVLA. 


Figure 9. Real-world physical platform. (a) JAKA robot platform; (b) the task of placing the object into a box from unseen spatial positions, to evaluate the model’s spatial robustness. 

Table 3. Real-world evaluation results (Successes / Total Trials). 

|**Method**|**Task-1**|**Task-2**|**Task-3**|**Task-4**|
|---|---|---|---|---|
|OpenVLA[22]|19/30|7/30|7/30|1/30|
|OpenVLA + FAN-SFT|22/30|12/30|17/30|7/30|


(a) Rollout on the training set. (b) Evaluation on the test set. 

Figure 8. Training curves of rollout and evaluation success rates during RFT of OpenVLA-OFT. Our FAN-guided regularization significantly improved the sample efficiency in evaluation and obtained better performance in training process of OpenVLA-OFT. 

**Main Results.** Table 2 summarizes the quantitative results of RFT on ManiSkill. It can be seen that applying FAN-guided regularization to both OpenVLA and OpenVLA-OFT consistently improves performance across in-distribution and all OOD settings. Notably, the improvement is most pronounced in the execution OOD setting, where the success rate increases by more than 10%. As shown in Fig. 6, which provides a more detailed breakdown across different OOD tasks, FAN-guided regularization yields consistent performance gains similar to results in the SFT experiments in Sec. 6.1. 

Fig. 7 presents the rollout and evaluation success rates during RFT of OpenVLA. Clearly, FAN-guided regularization significantly accelerates convergence, effectively improving sample efficiency, achieving a 90% success rate with only about one-third of the training steps required by the baseline. A similar trend can be observed under OOD evaluation, where our method maintains faster improvement and higher final performance. Fig. 8 presents the results on OpenVLA-OFT. Although less pronounced compared to OpenVLA, FAN-guided regularization still yields distinct performance gains throughout training, with more evident advantage in OOD settings. More detailed quantitative results are provided in Appendix Table 15-18. 

### **6.3. Real-World Experiment** 

To evaluate the effectiveness of our method in real-world settings, we built a physical robotic platform for comparative experiments, as illustrated in Fig. 9. The platform consists of a 7-DoF JAKA manipulator equipped with a parallel 

gripper and a fixed Intel RealSense D455 camera that provides third-person RGB images. 

We evaluate the OpenVLA models trained with SFT and the proposed FAN-SFT. A total of 150 demonstration trajectories (50 per object) are collected for training. We define four tasks for evaluation: Task-1 corresponds to the standard setting, consistent with the demonstrations, e.g., placing the target object into a designated box, as shown in Fig. 9b; Task-2 perturbs the initial pose of the object; Task3 perturbs the manipulator’s initial pose; and Task-4 perturbs the box’s initial position. Each task is evaluated over 30 independent trials. The results in Table 3 show that our method exhibits stronger robustness in the presence of spatial perturbations. More details are provided in Appendix. 

## **7. Conclusion** 

In this work, we addressed the fundamental mismatch between VLA finetuning methods and the intrinsic tolerance of physical actions, which is a property we term FAN. We first demonstrated empirically that standard methods, which ignore this property, produce “spiky” policy distributions that fail to generalize. To remedy this, we introduced a FAN-guided regularizer, applicable to both SFT and RFT. This regularizer explicitly shapes the policy’s geometric structure, guiding it to approximate a target Gaussian. Our extensive experiments demonstrated that by actively shaping the policy distribution, VLA models achieve significant improvement in sample efficiency and OOD generalization. Overall, our findings indicate that controlling policy geometry constitutes a principled and highly effective direction for developing robust and generalizable robotic agents. 

27963 

## **Acknowledgements** 

This work was supported by the Science and Technology Innovation (STI) 2030–Major Project under Grant 2022ZD0208700 and Shanghai Pilot Industry Innovation and Development Project (Artificial Intelligence Program) under Grant 2025-GZL-RGZN-01033. 

## **References** 

- [1] Muhammad Awais, Muzammal Naseer, Salman Khan, Rao Muhammad Anwer, Hisham Cholakkal, Mubarak Shah, Ming-Hsuan Yang, and Fahad Shahbaz Khan. Foundation models defining a new era in vision: a survey and outlook. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 47(4):2245–2264, 2025. 2 

- [2] Suneel Belkhale, Tianli Ding, Ted Xiao, Pierre Sermanet, Quon Vuong, Jonathan Tompson, Yevgen Chebotar, Debidatta Dwibedi, and Dorsa Sadigh. Rt-h: Action hierarchies using language. _arXiv preprint arXiv:2403.01823_ , 2024. 1 

- [3] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 2 

- [4] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-languageaction flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 1, 2 

- [5] Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, Niccolo Fusai, Manuel Y Galliker, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. In _9th Annual Conference on Robot Learning_ , 2025. 1, 2 

- [6] Anthony Brohan, Yevgen Chebotar, Chelsea Finn, Karol Hausman, Alexander Herzog, Daniel Ho, Julian Ibarz, Alex Irpan, Eric Jang, Ryan Julian, et al. Do as i can, not as i say: Grounding language in robotic affordances. In _Conference on robot learning_ , pages 287–318. PMLR, 2023. 2 

- [7] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2505.06111_ , 2025. 2, 6 

- [8] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 2, 6 

- [9] Hao Chen, Jiaming Liu, Chenyang Gu, Zhuoyang Liu, Renrui Zhang, Xiaoqi Li, Xiao He, Yandong Guo, Chi-Wing Fu, Shanghang Zhang, et al. Fast-in-slow: A dual-system vla model unifying fast manipulation within slow reasoning. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 2 

- [10] Xiaoyu Chen, Hangxing Wei, Pushi Zhang, Chuheng Zhang, Kaixin Wang, Yanjiang Guo, Rushuai Yang, Yucen Wang, Xinquan Xiao, Li Zhao, et al. Villa-x: enhancing latent 

action modeling in vision-language-action models. _arXiv preprint arXiv:2507.23682_ , 2025. 2 

- [11] Yuhui Chen, Shuai Tian, Shugao Liu, Yingting Zhou, Haoran Li, and Dongbin Zhao. Conrft: A reinforced fine-tuning method for vla models via consistency policy. _arXiv preprint arXiv:2502.05450_ , 2025. 3 

- [12] Zengjue Chen, Runliang Niu, He Kong, Qi Wang, Qianli Xing, and Zipei Fan. Tgrpo: Fine-tuning vision-languageaction model via trajectory-wise group relative policy optimization. _arXiv preprint arXiv:2506.08440_ , 2025. 3 

- [13] Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, et al. Palme: An embodied multimodal language model. _arXiv preprint arXiv:2303.03378_ , 2023. 2 

- [14] Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, et al. Libero-plus: In-depth robustness analysis of visionlanguage-action models. _arXiv preprint arXiv:2510.13626_ , 2025. 2 

- [15] Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An opensource generalist robot policy. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, 2024. 2, 6 

- [16] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu Zhang, Shirong Ma, Xiao Bi, et al. Deepseek-r1 incentivizes reasoning in llms through reinforcement learning. _Nature_ , 645(8081):633– 638, 2025. 2 

- [17] Yanjiang Guo, Jianke Zhang, Xiaoyu Chen, Xiang Ji, YenJen Wang, Yucheng Hu, and Jianyu Chen. Improving visionlanguage-action model with online reinforcement learning. In _2025 IEEE International Conference on Robotics and Automation_ , pages 15665–15672. IEEE, 2025. 3 

- [18] Jiaheng Hu, Rose Hendrix, Ali Farhadi, Aniruddha Kembhavi, Roberto Mart´ın-Mart´ın, Peter Stone, Kuo-Hao Zeng, and Kiana Ehsani. Flare: Achieving masterful and adaptive robot policies with large-scale reinforcement learning finetuning. In _2025 IEEE International Conference on Robotics and Automation_ , pages 3617–3624. IEEE, 2025. 2 

- [19] Yingdong Hu, Fanqi Lin, Tong Zhang, Li Yi, and Yang Gao. Look before you leap: Unveiling the power of gpt4v in robotic vision-language planning. _arXiv preprint arXiv:2311.17842_ , 2023. 2 

- [20] Dongchi Huang, Zhirui Fang, Tianle Zhang, Yihang Li, Lin Zhao, and Chunhe Xia. Co-rft: Efficient fine-tuning of vision-language-action models through chunked offline reinforcement learning. _arXiv preprint arXiv:2508.02219_ , 2025. 3 

- [21] Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, and Li Fei-Fei. Voxposer: Composable 3d value maps for robotic manipulation with language models. _arXiv preprint arXiv:2307.05973_ , 2023. 2 

- [22] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan 

27964 

Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 1, 2, 5, 6, 8, 17 

- [23] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 1, 2, 5, 6 

- [24] Wouter Kool, Herke Van Hoof, and Max Welling. Attention, learn to solve routing problems! _arXiv preprint arXiv:1803.08475_ , 2018. 3 

- [25] Haozhan Li, Yuxin Zuo, Jiale Yu, Yuhao Zhang, Zhaohui Yang, Kaiyan Zhang, Xuekai Zhu, Yuchen Zhang, Tianxing Chen, Ganqu Cui, et al. Simplevla-rl: Scaling vla training via reinforcement learning. _arXiv preprint arXiv:2509.09674_ , 2025. 1, 2 

- [26] Jacky Liang, Wenlong Huang, Fei Xia, Peng Xu, Karol Hausman, Brian Ichter, Pete Florence, and Andy Zeng. Code as policies: Language model programs for embodied control. In _2023 IEEE International conference on robotics and automation_ , pages 9493–9500. IEEE, 2023. 2 

- [27] Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. In _The twelfth international conference on learning representations_ , 2023. 2 

- [28] Fanqi Lin, Ruiqian Nai, Yingdong Hu, Jiacheng You, Junming Zhao, and Yang Gao. Onetwovla: A unified visionlanguage-action model with adaptive reasoning. _arXiv preprint arXiv:2505.11917_ , 2025. 2 

- [29] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 5 

- [30] Jiaming Liu, Hao Chen, Pengju An, Zhuoyang Liu, Renrui Zhang, Chenyang Gu, Xiaoqi Li, Ziyu Guo, Sixiang Chen, Mengzhen Liu, et al. Hybridvla: Collaborative diffusion and autoregression in a unified vision-language-action model. _arXiv preprint arXiv:2503.10631_ , 2025. 2 

- [31] Jijia Liu, Feng Gao, Bingwen Wei, Xinlei Chen, Qingmin Liao, Yi Wu, Chao Yu, and Yu Wang. What can RL bring to VLA generalization? an empirical study. In _The Thirtyninth Annual Conference on Neural Information Processing Systems_ , 2025. 1, 2, 5, 6, 7, 3 

- [32] Zhenyang Liu, Yongchong Gu, Sixiao Zheng, Xiangyang Xue, and Yanwei Fu. Trivla: A triple-system-based unified vision-language-action model for general robot control. _arXiv e-prints_ , pages arXiv–2507, 2025. 2, 6 

- [33] Guanxing Lu, Wenkai Guo, Chubin Zhang, Yuheng Zhou, Haonan Jiang, Zifeng Gao, Yansong Tang, and Ziwei Wang. Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning. _arXiv preprint arXiv:2505.18719_ , 2025. 3 

- [34] Max Sobol Mark, Tian Gao, Georgia Gabriela Sampaio, Mohan Kumar Srirama, Archit Sharma, Chelsea Finn, and Aviral Kumar. Policy agnostic rl: Offline rl and online rl fine-tuning of any class and backbone. _arXiv preprint arXiv:2412.06685_ , 2024. 1 

- [35] Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy V. Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, 

   - Daniel HAZIZA, Francisco Massa, Alaaeldin El-Nouby, Mido Assran, Nicolas Ballas, Wojciech Galuba, Russell Howes, Po-Yao Huang, Shang-Wen Li, Ishan Misra, Michael Rabbat, Vasu Sharma, Gabriel Synnaeve, Hu Xu, Herve Jegou, Julien Mairal, Patrick Labatut, Armand Joulin, and Piotr Bojanowski. DINOv2: Learning robust visual features without supervision. _Transactions on Machine Learning Research_ , 2024. Featured Certification. 2 

- [36] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _IEEE International Conference on Robotics and Automation_ , pages 6892–6903, 2024. 2 

- [37] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 2 

- [38] John Schulman, Philipp Moritz, Sergey Levine, Michael Jordan, and Pieter Abbeel. High-dimensional continuous control using generalized advantage estimation. _arXiv preprint arXiv:1506.02438_ , 2015. 3 

- [39] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 1, 3 

- [40] Rui Shao, Wei Li, Lingsen Zhang, Renshan Zhang, Zhiyang Liu, Ran Chen, and Liqiang Nie. Large vlm-based visionlanguage-action models for robotic manipulation: A survey. _arXiv preprint arXiv:2508.13073_ , 2025. 2 

- [41] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 1, 3 

- [42] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, et al. Smolvla: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 2 

- [43] Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe, Jon Shlens, and Zbigniew Wojna. Rethinking the inception architecture for computer vision. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 2818–2826, 2016. 7 

- [44] Shuhan Tan, Kairan Dou, Yue Zhao, and Philipp Kr¨ahenb¨uhl. Interactive post-training for vision-languageaction models. _arXiv preprint arXiv:2505.17016_ , 2025. 3 

- [45] Stone Tao, Fanbo Xiang, Arth Shukla, Yuzhe Qin, Xander Hinrichsen, Xiaodi Yuan, Chen Bao, Xinsong Lin, Yulin Liu, Tse-Kai Chan, et al. Maniskill3: Gpu parallelized robot simulation and rendering for generalizable embodied ai. In _7th Robot Learning Workshop: Towards Robots with HumanLevel Abilities_ , 2025. 5 

- [46] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, 

27965 

Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. 2 

- [47] Hongyu Wang, Chuyan Xiong, Ruiping Wang, and Xilin Chen. Bitvla: 1-bit vision-language-action models for robotics manipulation. _arXiv preprint arXiv:2506.07530_ , 2025. 2 

- [48] Yating Wang, Haoyi Zhu, Mingyu Liu, Jiange Yang, HaoShu Fang, and Tong He. Vq-vla: Improving visionlanguage-action models via scaling vector-quantized action tokenizers. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 11089–11099, 2025. 2 

- [49] Tian-Yu Xiang, Ao-Qun Jin, Xiao-Hu Zhou, Mei-Jiang Gui, Xiao-Liang Xie, Shi-Qi Liu, Shuang-Yi Wang, Sheng-Bin Duan, Fu-Chao Xie, Wen-Kai Wang, et al. Parallels between vla model post-training and human motor learning: Progress, challenges, and trends. _arXiv preprint arXiv:2506.20966_ , 2025. 2 

- [50] Yantai Yang, Yuhao Wang, Zichen Wen, Luo Zhongwei, Chang Zou, Zhipeng Zhang, Chuan Wen, and Linfeng Zhang. Efficientvla: Training-free acceleration and compression for vision-language-action models. _arXiv preprint arXiv:2506.10100_ , 2025. 2 

- [51] Hongzhi Zang, Mingjie Wei, Si Xu, Yongji Wu, Zhen Guo, Yuanqing Wang, Hao Lin, Liangzhi Shi, Yuqing Xie, Zhexuan Xu, et al. Rlinf-vla: A unified and efficient framework for vla+ rl training. _arXiv preprint arXiv:2510.06710_ , 2025. 1, 2 

- [52] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 11975–11986, 2023. 2 

- [53] Hongyin Zhang, Zifeng Zhuang, Han Zhao, Pengxiang Ding, Hongchao Lu, and Donglin Wang. Reinbot: Amplifying robot visual-language manipulation with reinforcement learning. _arXiv preprint arXiv:2505.07395_ , 2025. 3 

- [54] Zijian Zhang, Kaiyuan Zheng, Zhaorun Chen, Joel Jang, Yi Li, Siwei Han, Chaoqi Wang, Mingyu Ding, Dieter Fox, and Huaxiu Yao. Grape: Generalizing robot policy via preference alignment. _arXiv preprint arXiv:2411.19309_ , 2024. 3 

- [55] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 1 

- [56] Xueyang Zhou, Yangming Xu, Guiyao Tie, Yongchao Chen, Guowen Zhang, Duanfeng Chu, Pan Zhou, and Lichao Sun. Libero-pro: Towards robust and fair evaluation of vision-language-action models beyond memorization. _arXiv preprint arXiv:2510.03827_ , 2025. 2, 6 

- [57] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 1, 2 

27966 

