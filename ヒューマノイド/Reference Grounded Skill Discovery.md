---
title: "Reference Grounded Skill Discovery"
date: "2025-10-07"
authors: "Seungeun Rho; Aaron Trinh; Danfei Xu; Sehoon Ha"
venue: "ICLR 2026 Poster"
url: https://arxiv.org/abs/2510.06203
pdf: https://arxiv.org/pdf/2510.06203
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2510.06203)** / [論文ページ](https://arxiv.org/abs/2510.06203)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Published as a conference paper at ICLR 2026 

# REFERENCE GROUNDED SKILL DISCOVERY 

### **Seungeun Rho, Aaron Trinh, Danfei Xu, Sehoon Ha** 

School of Interactive Computing Georgia Institute of Technology Atlanta, GA 30332, USA _{_ srho31,atrinh31,danfei,sehoonha _}_ @gatech.edu 

## ABSTRACT 

Scaling unsupervised skill discovery algorithms to high-DoF agents remains challenging. As dimensionality increases, the exploration space grows exponentially, while the manifold of meaningful skills remains limited. Therefore, _semantic meaningfulness_ becomes essential to effectively guide exploration in highdimensional spaces. In this work, we present **Reference-Grounded Skill Discovery (RGSD)**<sup>1</sup> , a novel algorithm that grounds skill discovery in a semantically meaningful latent space using reference data. RGSD first performs contrastive pretraining to embed motions on a unit hypersphere, clustering each reference trajectory into a distinct direction. This grounding enables skill discovery to simultaneously involve both imitation of reference behaviors and the discovery of semantically related diverse behaviors. On a simulated SMPL humanoid with 359-D observations and 69-D actions, RGSD successfully imitates skills such as walking, running, punching, and sidestepping, while also discover variations of these behaviors. In downstream locomotion tasks, RGSD leverages the discovered skills to faithfully satisfy user-specified style commands and outperforms imitation-learning baselines, which often fail to maintain the commanded style. 

## 1 INTRODUCTION 


Figure 1: Comparison of skills learned by METRA and RGSD. To our knowledge, this is the first work to discover structured skills in high-DoF systems by grounding them in reference motions. 

The ultimate goal of unsupervised skill discovery is to acquire a set of reusable skills that can be applied to arbitrary downstream tasks. Achieving this goal requires the learned skills to satisfy two key desiderata: _diversity_ and _semantic meaningfulness_ . First, the skill set should be sufficiently diverse to cover the wide distribution of possible downstream tasks. For example, a humanoid agent should be equipped with both `turn-left` and `turn-right` skills; if it only learns to `walk-forward` , it will fail on general locomotion tasks, such as goal reaching or heading. Second, the discovered skills must be semantically meaningful, as downstream tasks are typically defined in semantic terms. For example, consider a set of unstructured humanoid behaviors such as independent vibrating or 

> 1Videos at seungeunrho.github.io/projects/RGSD 

1 

Published as a conference paper at ICLR 2026 

jittering of individual body parts. Although these behaviors may be diverse, it is difficult to envision realistic tasks for which such skills would be useful. Therefore, it is essential that discovered skills are not only diverse, but also structured and semantically interpretable. 

Recent progress in skill discovery has demonstrated the ability to learn skills that satisfy both desiderata, particularly in relatively low degree-of-freedom (DoF) systems such as benchmark environments (Eysenbach et al., 2018; Gregor et al., 2016; Laskin et al., 2022), quadrupeds (Cheng et al., 2024; Atanassov et al., 2024; Rho et al., 2025; Cathomen et al., 2025), or simple robotic manipulators with grippers (Park et al., 2023a; Rho et al., 2024). However, scaling unsupervised skill discovery to high-DoF agents remains an open challenge. As the DoF increases, the exploration space grows exponentially, while the portion of the semantically meaningful manifold remains relatively small. This mismatch renders skill discovery in high-DoF systems particularly difficult. As shown in Fig. 1, skills learned by the state-of-the-art unsupervised skill discovery algorithm, METRA (Park et al., 2023b), fail to yield meaningful behaviors. Joints move randomly, producing highly unstructured motions in which arms, legs, torso, and head move independently and arbitrarily. This highlights the necessity of a mechanism that grounds skill discovery within a meaningful manifold. 

Our key insight is that to tame the curse of dimensionality in high-DoF skill discovery, we need to construct a semantically meaningful skill latent space _a priori_ and constrain exploration within this space. In this paper, we propose **Reference-Grounded Skill Discovery (RGSD)** , a simple yet effective algorithm that achieves this by leveraging reference data to ground the latent skill space before exploration begins. Building upon DIAYN (Eysenbach et al., 2018), RGSD first uses contrastive learning on reference trajectories to embed motions on a unit hypersphere, where each reference behavior corresponds to a distinct direction. This grounding step establishes a semantically meaningful manifold that constrains subsequent exploration. RGSD then utilizes this pre-structured latent space to simultaneously imitate reference skills and discover novel behaviors that are semantically related to the references. This two-stage approach is analogous to recent large language model training regimes (Guo et al., 2025; Yang et al., 2025), where pretraining with self-supervised objectives establishes a meaningful exploration space before reinforcement learning fine-tuning. As a result, RGSD not only reproduces motions present in the reference data but also discovers new skills that emerge as coherent variations of existing ones, rather than arbitrary high-dimensional movements. 

We empirically demonstrate that RGSD discovers structured skills in a humanoid SMPL agent with a 359-dimensional observation space and a 69-dimensional action space. RGSD successfully imitates motions such as walking, running, side-stepping, punching, and moving backward, while also discovering related novel skills. Furthermore, it achieves superior performance on downstream tasks compared to both pure skill-discovery and imitation-based skill acquisition baselines. 

The main contributions of this paper are as follows: **1)** We propose a novel skill discovery algorithm that scales to high-DoF agents by grounding the latent space with reference data. **2)** We empirically demonstrate that RGSD discovers both diverse and structured motions on a 69-DoF SMPL humanoid and achieves superior downstream task performance. **3)** We provide a theoretical proof establishing the validity of the proposed reward as a legitimate imitation signal. **4)** We offer insights into why mutual information–based methods integrate well with our approach, whereas Wasserstein dependency–based methods fail to extend in the same way. 

## 2 RELATED WORKS 

Our work can be framed as “imitation for discovery,” because it performs imitation based on reference data to discover semantically similar yet novel behaviors. Accordingly, we first review prior work on pure **unsupervised skill discovery** , and then discuss **imitation-based skill acquisition approaches** that also learn skills by relying on reference data. 

### 2.1 UNSUPERVISED SKILL DISCOVERY 

The most widely adopted approach for acquiring diverse skills is based on maximizing the mutual information (MI) _I_ ( _S_ ; _Z_ ) between a latent variable _z_ and the agent’s states _s_ (Gregor et al., 2016; Eysenbach et al., 2018; Hansen et al., 2019; Liu & Abbeel, 2021a; Laskin et al., 2022). However, because MI is typically estimated via KL divergence, it suffers from a key limitation: even minor 

2 

Published as a conference paper at ICLR 2026 

differences between skills can fully maximize the objective, as long as the discriminator can distinguish them. To address this, methods based on the Wasserstein Dependency Measure (WDM, Ozair et al. (2019)) have been proposed (He et al., 2022; Park et al., 2021; 2023b), which explicitly seek _maximal differences_ between skills. Nevertheless, our method builds on MI-based approaches, and in Section 6 we explain why extending WDM-based algorithms with our idea faces inherent challenges. Another relevant line of work is CIC (Laskin et al., 2022), which, like our approach, employs contrastive learning. The key difference is that CIC optimizes a contrastive objective on online data gathered by the agent, leaving it with the same scaling difficulties in high-DoF systems. 

More recently, approaches such as LGSD (Rho et al., 2024) and DoDont (Kim et al., 2024) have explored injecting guidance from LLMs or videos to semantically ground skill discovery. While motivated by a similar goal, these methods still struggle to scale to high-DoF systems, as their guidance is provided only at a high level. In contrast, our method leverages reference data directly, enabling a more effective grounding mechanism that scales to complex, high-DoF agents. 

### 2.2 IMITATION-BASED SKILL ACQUISITION 

Imitation learning offers another major paradigm for acquiring a repertoire of skills. A common approach is based on GAIL (Ho & Ermon, 2016), which uses adversarial training to align the marginal state distribution of the learned policy with that of expert demonstrations. Building on this idea, ASE (Peng et al., 2022) learns a controllable skill embedding from large-scale human motion data using a GAIL-style objective. CALM (Tessler et al., 2023) mitigates the mode collapse observed in ASE by incorporating a conditional discriminator and a motion encoder, enabling skill generation conditioned on specific reference motions. More recently, Meta-Motivo (Tirinzoni et al., 2025) combines GAIL with forward–backward representation learning (Blier et al., 2021; Touati & Ollivier, 2021) to extract a skill set tailored for zero-shot RL. 

In contrast to these imitation-based approaches, we highlight a key conceptual difference: imitation objectives aim to **match the state visitation measure** of the demonstrations, whereas RGSD is a discovery algorithm that explicitly encourages visiting states _not present_ from the dataset. This fundamental difference allows RGSD to discover a wider range of skills, as demonstrated in our experiments. 

## 3 PRELIMINARIES 

Unsupervised skill discovery can be formulated as a reward-free Markov Decision Process (MDP) _M_ := _{S, A, P, ρ_ 0 _, γ}_ , which consists of the state space _S_ , the action space _A_ , the transition dynamics _P_ = Pr( _s_<sup>_′_</sup> _| s, a_ ) , the initial state distribution _ρ_ 0 , and the discount factor _γ_ . The objective is to _associate_ a latent skill vector _z_ with the states _s_ visited by the skill-conditioned policy _πθ_ ( _· | s, z_ ), such that different _z_ induce distinct behaviors. Typically, _z ∼ p_ ( _z_ ) is sampled from a fixed prior at the beginning of each episode and held constant throughout. 

A common formulation is to maximize the mutual information (MI) _I_ ( _S_ ; _Z_ ) between skills and visited states. Prior work (Gregor et al., 2016; Eysenbach et al., 2018; Laskin et al., 2022; Liu & Abbeel, 2021b) leverages the decomposition _I_ ( _s_ ; _z_ ) = _H_ ( _s_ ) _−H_ ( _s | z_ ) = _H_ ( _z_ ) _−H_ ( _z | s_ ) _._ Because _H_ ( _z | s_ ) is intractable, Eysenbach et al. (2018) introduced a neural encoder _qϕ_ ( _z|s_ ) to obtain a variational lower bound _G_ ( _θ, ϕ_ ) of the skill discovery objective _F_ ( _θ_ ): 


where _H_ [ _·_ ] denotes Shannon entropy. 

Optimization proceeds as: 


along with the entropy bonus for the policy. Intuitively, _qϕ_ learns to infer which skill _z_ led to a given state, while _πθ_ is reinforced to visit states that make _z_ easily identifiable. 

3 

Published as a conference paper at ICLR 2026 


Figure 2: We present the overall training pipeline of RGSD. It starts with contrastive pretraining of an encoder using reference motions, followed by parallel training of imitation and discovery. 

## 4 REFERENCE GROUNDED SKILL DISCOVERY 

At a high level, RGSD approaches skill discovery in the _reverse order_ of conventional methods. Standard skill discovery begins with policy exploration, and only afterward induces a latent space to enforce different regions represent different behaviors. In contrast, we start with a dataset of target behaviors we wish to capture and first embed them into a unit hyperspherical latent space without any environmental interaction. The ideal latent space would have each motion represented by a single directional vector _z_ , with clear separation between different motions. This will turn exploration of the latent space into the discovery of structured skills in the state space. To achieve this, we employ contrastive learning. 

Once the latent space is grounded with motion representations, we proceed with skill discovery in this reference-equipped space. Here, we exploit the geometry of the hypersphere: sampling _z_ along directions aligned with reference vectors triggers **imitation** , while sampling _z_ in-between reference directions drives the **discovery** of novel skills. This design enables semantically meaningful expansion of known behaviors and structured exploration of new ones. 

In the following subsections, we detail how motion priors are injected into the latent space and how imitation and discovery are jointly achieved within this framework. 

### 4.1 PRETRAINING: GROUNDING LATENT SPACE ON REFERENCE MOTIONS 

The goal of pretraining is to associate each motion with a latent vector _z_ , enabling the skillconditioned policy _π_ ( _·|s, z_ ) to reproduce the corresponding trajectory. To achieve this, we place each motion at a point on the hypersphere while ensuring separation between different motions. We employ contrastive learning: positive pairs are sampled from the same trajectory, and negative pairs from different trajectories. This encourages motions to cluster tightly around unique latent directions, forming a well-structured space for downstream imitation and discovery. 

More concretely, we train an encoder _qϕ_ ( _z | s_ ) that maps a state _s_ to a probability distribution over a latent vector _z ∈Z_ , where _Z_ = _{v ∈_ R<sup>_k_</sup> : _∥v∥_ 2 = 1 _}._ We model _qϕ_ ( _z | s_ ) with a von Mises–Fisher (vMF) distribution: 


where _µϕ_ ( _s_ ) is the mean direction parameterized by a neural network _ϕ_ , and _κ_ is the concentration parameter. We fix _κ_ as a constant during training. 

Training is performed with contrastive learning on a reference dataset _M_ = _{mi}_<sup>_n_</sup> _i_ =1<sup>, where each</sup> _mi_ is a reference trajectory consisting of a sequence of states. During pretraining, we first sample a motion _m ∼_ Uniform( _M_ ), then select a pair of states ( _s_<sup>_a_</sup> _, s_<sup>+</sup> ) from _m_ , with _s_<sup>_a_</sup> as the anchor and _s_<sup>+</sup> as the positive sample. A negative sample _s_<sup>_−_</sup> is drawn from _M \ {m}_ . Given the anchor _s_<sup>_a_</sup> , the 

4 

Published as a conference paper at ICLR 2026 

positive _s_<sup>+</sup> , and negatives _{s_<sup>_−_</sup> _j_<sup>_}_, we embed them as</sup> 


and optimize the InfoNCE loss (Oord et al., 2018): 

Here, sim( _zi, zj_ ) = _zi_<sup>_⊤zj_denotes cosine similarity since all vectors lie on the unit hypersphere, and</sup> _T_ = 1 _/κ_ is the temperature. A detailed derivation is provided in Appendix B. As depicted in Fig.2-pretraining, the mapping of motions in latent space is spread out before training. However when pretraining is completed, we end up with a within-motion alignment, meaning that the mapping of every state _s ∈ m_ in each motion _m_ points in exactly the same direction. This characteristic is important for the following section; therefore, for completeness, we provide a proof of this claim in Appendix C. 

### 4.2 IMITATION OF REFERENCE SKILLS 

After pretraining, we freeze _qϕ_ and proceed to the second phase, where imitation and discovery are trained in parallel. Interestingly, both processes rely on the **same reward term** defined in Eq. 1. We first show that this reward can be repurposed as an _imitation reward_ when conditioned on the motion’s embedding of the pretrained encoder _qϕ_ . Specifically, we sample a motion _m ∼_ Uniform( _M_ ) and compute its embedding vector _zm_ as the average of its state embeddings: 


where _l_ is the length of motion _m_ . At theoretical optimum, _zm_ should be aligned with the embedding of any individual state _s ∈ m_ . 

Conditioning the policy on _zm_ , i.e., executing rollouts with _π_ ( _·|s, zm_ ), does not by itself reproduce _m_ . However, reinforcement learning with the DIAYN reward (Eq. 1) drives _π_ ( _·|s, zm_ ) toward imitating _m_ . Substituting in the vMF formulation (Eq. 3) gives 


where the prior _p_ ( _z_ ) and concentration _κ_ are fixed, and _ϕ_ is frozen. _C_ is a constant term independent of _s_ and _zm_ . Intuitively, this reward depends on the angle between _µϕ_ ( _s_ ) and _zm_ , effectively measuring the similarity between the state visited by the agent and the states in the reference motion. Moreover, initializing _s_ 0 from _m_ provides an aligned starting point; as trajectories deviate, the cosine alignment decreases and the reward diminishes. 

This formulation can be viewed as _feature-based imitation_ with structured representations, as proposed by Li et al. (2025). Unlike DeepMimic (Peng et al., 2018) or MaskedMimic (Tessler et al., 2024), which reward joint-level similarity, our method evaluates similarity in a learned latent space. 

**Guarantee as an imitation reward** For the proposed reward to serve as a valid imitation objective, it must satisfy two key conditions: (1) it should attain its optimum when the agent visits the exact states of the reference motion, and (2) the reward landscape around the reference states should be locally quasi-concave, ensuring that deviations from the reference lead to a monotonic decrease in the reward within a neighborhood of the optimum. We claim that, under the assumption of “perfect alignment within motion” introduced in the previous section, our reward formulation in Eq. 7 satisfies both conditions, and we provide the proof in Appendix D.1. To exploit this local concavity in practice, we apply _early termination_ : whenever the agent deviates from the reference motion beyond a specified threshold measured by cartesian error, the episode is terminated. This mechanism guarantees that the reward functions as a legitimate imitation objective. 

5 

Published as a conference paper at ICLR 2026 


Figure 3: **Example skills.** RGSD generates diverse behaviors when conditioned on different latent vectors. The figure shows motions from a **single policy** conditioned on distinct latent vectors sampled near the embedding of the **(a)** running, **(b)** backward, **(c)** sidestepping, and **(d)** punching motion. 

### 4.3 DISCOVERY OF NEW SKILLS 

The discovery process follows DIAYN, but with several key differences. First, to protect the learned latent space during discovery, we initialize a separate encoder _qϕ_<sup>_′_fromthefrozen</sup><sup>_qϕ_andcontinue</sup> propagating gradients from minimizing KL-divergence between _qϕ_<sup>_′_and</sup><sup>_qϕ_. Second, we train discov-</sup> ery in parallel with imitation, so that the shared policy and value function transfers knowledge about high fidelity behavior from imitations into discovery. Note that these two processes share same form of reward function and latent space, so these shared components can be optimized in a stable manner. Third, we adopt reference state initialization (RSI), which samples initial states directly from the reference motions. RSI prevents the emergent of _disjoint_ skill sets by ensuring that imitation and discovery operate over overlapping state distributions. 

In detail, imitation and discovery are trained in parallel, with a ratio parameter _p_ : 


where _m_ is the motion sampled by RSI. The full algorithmic details are provided in Appendix F. 

## 5 EXPERIMENTAL RESULTS AND DISCUSSION 

In this section, we investigate four questions: (1) Can RGSD imitate reference motions with high fidelity? (2) Can RGSD discover novel skills that are still semantically related to the references? (3) Can we control degree of diversity at test time? (4) Can the learned skills be effectively leveraged for downstream tasks? 

**Baselines.** We compare RGSD against both unsupervised skill discovery (USD) methods and imitation learning (IL) based skill acquisition methods. To assess the impact of reference guidance, we include pure USD baselines. Specifically, we compare against DIAYN (Eysenbach et al., 2018) and METRA (Park et al., 2023b). DIAYN, which forms the backbone of RGSD, also serves as an ablation without reference grounding, while METRA represents a distance-maximization approach to USD that explicitly seeks maximal differences between skills. 

For the IL baselines, we consider ASE, CALM, and Meta-Motivo, all of which utilize a GAIL-style objective (Ho & Ermon, 2016) for imitation. ASE builds on InfoGAIL (Li et al., 2017), combining mutual-information maximization with an adversarial imitation reward, making it the closest baseline that jointly addresses skill discovery and imitation. CALM, a variant of ASE, further augments 

6 

Published as a conference paper at ICLR 2026 

Table 1: Cartesian ERR(cm) and FID scores for imitation across tasks. Lower values are better. 

||Wa|lk|R|un|Side|step|Back|ward|Pu|nch|
|---|---|---|---|---|---|---|---|---|---|---|
||ERR|FID|ERR|FID|ERR|FID|ERR|FID|ERR|FID|
|DIAYN|46.7|70.1|52.8|132.0|27.4|23.7|36.7|72.8|50.7|53.2|
|METRA|42.0|67.6|51.8|140.3|44.7|32.8|47.4|75.7|51.5|40.9|
|ASE|8.2|2.9|16.4|11.3|10.3|22.2|11.6|62.6|9.0|4.9|
|CALM|**7.2**|**1.4**|15.0|13.9|11.8|3.2|10.1|45.8|9.2|4.2|
|Meta-Motivo|10.9|1.7|15.4|**4.9**|11.8|**1.4**|8.6|**2.1**|8.1|**2.8**|
|**RGSD (Ours)**|7.4|4.7|**7.7**|9.4|**6.7**|8.0|**6.7**|4.0|**7.7**|8.8|


the imitation objective using a motion-conditioned discriminator. Meta-Motivo integrates imitation rewards with forward–backward representation learning. 

We emphasize that while these methods rely on GAIL-based imitation rewards, our approach employs a novel imitation reward derived from the DIAYN objective. To ensure a clean algorithmic comparison, we remove additional engineering techniques used in the original ASE and CALM implementations. The exact modifications are described in Appendix G.2. 

**Experimental setup.** We selected 20 reference motions from the ACCAD dataset. These motions are categorized into five tasks: `walk` , `run` , `sidestep` , `backward` , and `punch` , with each task containing 2 to 6 relevant motions. A complete list of motions is provided in Appendix G.3. Training was conducted in the GPU-based simulator Isaac Gym (Makoviychuk et al., 2021), using PPO (Schulman et al., 2017) as the RL algorithm. The full set of hyperparameters is provided in Appendix G.4. To ensure stable training, all methods employed an early termination condition: whenever the robot fell, the episode was terminated. 

### 5.1 EVALUATION OF IMITATION 

We first assess how well RGSD reproduces reference motions. For each motion, the agent is initialized with the first state _s_ 0 of the motion. Then we condition the policy on ( _s_ 0 _, zm_ ), where _zm_ is computed with Eq. 5. We generate 500 trajectories per each motion and compared against the reference to compute two metrics: 

- **Cartesian error:** the average _ℓ_ 2 distance between corresponding body-part positions per frame, averaged over the trajectory. 

- **Motion FID:** the Fr´echet distance between Gaussian feature distributions fitted to reference motions and generated motions. Lower FID indicates better naturalness. 

For CALM and Meta-Motivo, selecting the right latent that represents each motion is straightforward since it also includes motion encoders. For methods without encoders, we uniformly sample 500 latent vectors, select the one that minimizes Cartesian error, and re-evaluate using this vector to ensure fairness. We found that 500 samples were sufficient, as increasing the number further did not yield noticeable improvements. 

**RGSD achieves high-fidelity imitation.** As shown in Table 1, RGSD achieves low Cartesian error while Meta-Motivo achieves low FID scores across most motions. In contrast, pure USD baselines fail to discover skills that closely resemble the reference dataset. While DIAYN has demonstrated the ability to discover basic locomotion behaviors in low DoF ranging from 3 to 6 environments such as HalfCheetah, Ant, and Hopper (Brockman et al., 2016), they struggle with the 69-DoF SMPL agent, producing behaviors that are not semantically meaningful. This emphasizes the impact of reference guidance. 

When compared to Meta-Motivo, the results highlight a trade-off between fidelity and naturalness. Meta-Motivo achieves lower FID scores in 4 out of 5 tasks, indicating that its motions generally appear more natural. However, RGSD outperforms Meta-Motivo in Cartesian error on 4 out of 5 tasks, demonstrating higher trajectory fidelity. This contrast reflects a key difference in objective design: Meta-Motivo employs an occupancy-matching objective at the motion level, leading to smoother but less precise reproductions, whereas RGSD relies on frame-level similarity rewards, yielding high fidelity motions. 

7 

Published as a conference paper at ICLR 2026 


Figure 4: Top-view trajectories of the robot’s base when conditioned on latent vectors sampled from the neighborhood of each motion embedding. For each method, we visualize 150 trajectories. 

### 5.2 EVALUATION OF DISCOVERED SKILLS 

Now we evaluate whether RGSD can discover skills that are semantically similar to existing ones while also producing novel variations. Semantic similarity is enforced by sampling latent vectors from a local neighborhood around each motion embedding using a vMF distribution with the fixed concentration parameter _κ_ at 50. 

**RGSD can discover semantically similar yet novel behaviors.** Fig. 3 illustrates behaviors generated by the policy when conditioned on sampled latent vectors. The method produces diverse behaviors that remain semantically consistent with the reference motions. For example, while the reference dataset contains only a **single sidestepping** motion to the right, RGSD discovers skills that preserve the sidestepping style but introduce diverse degree of turns, enabling sidestepping in multiple directions. Similarly, although the dataset includes a punching motion aimed at a fixed target, our method extends this behavior to generate punches toward a variety of target positions. 

To compare against baselines, we visualize the 150 top-view trajectories of the robot’s base for each method in Fig. 4, alongside the trajectories from the reference motions. Trajectories produced by RGSD remain tightly clustered around the references, indicating that the policy captures the intended motion structure. In contrast, the baseline methods often produce degenerate or drifting trajectories, revealing their inability to preserve the characteristics of the original movements. 

These observations are further supported by the FID scores. For three out of four motions, RGSD achieves the lowest FID. While Meta-Motivo typically achieves the second-lowest FID, its generated trajectories still fail to remain centered around the references. CALM shows particularly degraded performance: its FID increases from 1 _._ 4 to 15 _._ 5 for walking and from 13 _._ 9 to 26 _._ 7 for running, indicating difficulty in producing diverse yet high-fidelity behaviors. In contrast, the FID scores of RGSD remain stable, demonstrating that the method successfully preserves motion style while enabling variation. 

We attribute this difference to the training setup. In both Meta-Motivo and CALM, the policy is always conditioned directly on the motion embedding and therefore never encounters nearby latent vectors during training. By contrast, RGSD explicitly separates imitation and discovery phases: the imitation phase exposes the policy to motion-embedding latents, while the discovery phase conditions it on diverse samples from the latent neighborhood. Consequently, the policy learns to handle both exact motion embeddings and their local variations, enabling consistent and semantically meaningful skill discovery. 

**RGSD enables test-time control over behavioral diversity.** A key advantage of RGSD is that it allows users to modulate the diversity of generated behaviors _at test time_ by adjusting the sampling distribution of the latent vector _z_ . Recall that we sample _z ∼_ vMF( _zm, κ_ ), a von Mises–Fisher distribution centered at the motion embedding _zm_ with concentration parameter _κ_ . A larger _κ_ produces 

8 

Published as a conference paper at ICLR 2026 


Figure 5: Training curves for the downstream task, along with corresponding FID scores. 

samples tightly clustered around _zm_ , yielding behaviors that closely imitate the reference motion but exhibit lower diversity. Conversely, a smaller _κ_ yields a broader distribution, producing more diverse behaviors that may deviate further from the original motion _m_ . 

We evaluate this effect on three reference motions by sampling with _κ ∈{_ 20 _,_ 100 _,_ 1000 _}_ . Results are shown in Fig. 6. As illustrated, increasing _κ_ results in trajectories that stay stylistically similar to the reference motion with limited variation, while decreasing _κ_ produces increasingly diverse trajectories that still preserve the core semantic style. 

### 5.3 DOWNSTREAM TASK EVALUATION 

**Setup.** We consider the `GoalReaching` task with three style conditions: `freestyle` , `sidestepping` , and `backward` . The agent must reach a randomly spawned goal within a 20 _×_ 20 m arena while adhering to the specified style. Following the setup in the previous sections, we first train a low-level policy _π_ low( _· | s, z_ ) using the 20 reference motions for each method. We then train a high-level policy _π_ high( _z | s, g_ ), which takes the goal _g_ as input and outputs a highlevel latent action _z_ . The corresponding low-level policy _π_ low( _· | s, z_ ) then produces the joint action _a_ . During this phase, _π_ low is frozen, and we optimize only _π_ high. 

To encourage both goal reaching and adherence to the commanded style, we adopt a reward similar to Tessler et al. (2023): 

_r_ = exp( _−_ 0 _._ 25 _∗∥d_ goal _∥_ ) + exp( _−_ 8 _∗∥z ⊕ zm∥_ ) _,_ 

where _d_ goal is the distance to the goal, and _z ⊕ zm_ denotes the cosine distance between the high-level action _z_ and the embedding _zm_ of the directed motion. For the `freestyle` task, only the first reward term is applied. All experiments are conducted with three random seeds. 

**Only RGSD consistently respects the commanded style while reaching the goal.** Figure 5 reports the success rates and FID scores of RGSD and baseline methods over the course of training. In the `freestyle` setting, since no specific style is required, we evaluate only the success rate. Although all methods eventually achieve near-perfect success, RGSD converges significantly faster. In contrast, ASE frequently fails to reach the goal; we observed that it often remains stationary, exploiting the fact that its reward remains positive even without producing the desired motion. 

For the `sidestepping` and `backward` tasks, we evaluate both the success rate and the FID score. Only RGSD reliably follows the commanded style. Although CALM achieves higher success rates early in training, RGSD eventually matches it. Furtermore, CALM ultimately ignores the style command and simply runs forward. On the other hand, Meta-Motivo respects the style only under certain conditions. For example, in the backward task, it walks backward when the goal is spawned behind the agent, but when the goal appears in front, the agent decides to walk forward. In contrast, RGSD consistently adheres to the commanded style: even when the goal is spawned in front during backward task, it takes a large detour to maintain backward motion. This difference is reflected in the FID scores: Meta-Motivo, CALM, and ASE all exhibit higher FID values, indicating substantial deviations from the intended styles. We refer the reader to the accompanying video for qualitative examples. 

Note that these tasks are inherently challenging because the reference motions for sidestepping and backward running do not include any turning behaviors. To reach diverse goal locations while main- 

9 

Published as a conference paper at ICLR 2026 

taining style fidelity, an agent must discover additional skills that are semantically consistent with the style, such as backward turns at varying angles. Imitation-based baselines lack this flexibility, whereas RGSD acquires a rich set of turning behaviors, enabling it to reach goals while preserving the commanded style. 

## 6 UNDERSTANDING THE CHALLENGES OF EXPANDING RGSD WITH METRA 

Our backbone skill discovery module is DIAYN, which relies on maximizing mutual information (MI). However, a well-known limitation of MI-based objectives is that they can be fully optimized even when the underlying differences between skills are minimal, as long as the discriminator can distinguish them. This raises a natural question: can we extend RGSD on top of distancemaximization based approaches such as METRA? 

To explore this, we conduct experiments with a METRA-based variant of RGSD. Similar to DIAYN, we first ground the latent space with reference motions while respecting the two conditions that METRA enforces. First, each motion should align with a unique directional vector _z_ , which can be satisfied using the original contrastive loss. Second, the latent space should capture the notion of _temporal distance_ : _∀x, y ∈ Sadj, ∥ϕ_ ( _x_ ) _− ϕ_ ( _y_ ) _∥≤_ 1. To enforce this, we add a loss term that drives _∥ϕ_ ( _x_ ) _− ϕ_ ( _y_ ) _∥_ toward its maximum value of 1 for adjacent state pairs. The resulting latent space, shown in Fig. 9, places each motion along a distinct line. 

However, this formulation exposes a critical issue when dealing with **repetitive motions** . Consider walking: the agent begins at some pose, takes a step, and eventually returns to a pose nearly identical to the starting one. Because all observations are computed in the local frame, the initial state _s_ 0 and final state _sT_ become identical. In this case, the METRA reward ( _ϕ_ ( _sT_ ) _− ϕ_ ( _s_ 0))<sup>_⊤_</sup> _z_ collapses to zero. As a result, repetitive behaviors cannot be framed as reward maximization under METRA, and more broadly, WDM-based approaches defined in a local coordinate system are not straightforward to capture repetitive dynamics. This observation is consistent with the concurrent findings (Park et al.). 

One might suspect that this problem could be bypassed by augmenting the state with additional variables, such as a time variable or global coordinates. However, this does not resolve the issue. In practice, it causes the latent space to be dominated by these added dimensions, leading the policy to focus on them rather than discovering meaningful behaviors. For brevity, we defer a more detailed discussion to Appendix H. To properly represent a substantial portion repetitive motions in dataset, we choose DIAYN as our backbone. 

## 7 CONCLUSION 

We introduced **Reference-Grounded Skill Discovery** (RGSD), a simple yet effective framework that scales unsupervised skill discovery to high-DoF agents by _grounding_ exploration in a semantically meaningful latent space constructed from reference motions. On a 69-DoF SMPL humanoid with 359-D observations, RGSD reproduces complex motions, such as walking, running, sidestepping, backward walking, punching, with high fidelity, and also discovers coherent variants, outperforming state-of-the-art unsupervised discovery and imitation-based baselines on both motion metrics and downstream control. 

Despite these advancements, several avenues remain open for further exploration. One promising direction is to move beyond variants of individual skills toward genuinely _compositional_ behaviors and principled interpolations that blend primitives (e.g., “walking while punching”). Another interesting direction would be scaling across embodiments and datasets, with the long-term vision of building a skill foundation model for control, analogous to large language models in natural language processing. Overall, we believe our work represents the beginning of a practical recipe for scaling skill discovery in high-DoF agents through reference grounding. 

10 

Published as a conference paper at ICLR 2026 

## REPRODUCIBILITY STATEMENT 

We have made extensive efforts to ensure the reproducibility of our work across multiple dimensions: 

- A complete pseudo-code description of our algorithm is provided in Appendix F. 

- The full list of reference motions used in our experiments is detailed in Appendix G.3. 

- Comprehensive specifications of states, actions, and hyperparameters are given in Appendix G.4. 

- Rigorous derivations and proofs of our theoretical claims are included in Appendices B, C, and D.1. 

## ACKNOWLEDGMENTS 

This research has been funded by the Industrial Technology Innovation Program (P0028404, development of a product level humanoid mobile robot for medical assistance equipped with bidirectional customizable human-robot interaction, autonomous semantic navigation, and dual-arm complex manipulation capabilities using large-scale artificial intelligence models) of the Ministry of Industry, Trade and Energy of Korea. In addition, we thank Jeonghwan Kim for the discussion. 

## REFERENCES 

OSU ACCAD. Accad motion lab system data. https://accad.osu.edu/research/ motion-lab/system-data. Accessed: 2025-09-20. 

- Vassil Atanassov, Wanming Yu, Alexander Luis Mitchell, Mark Nicholas Finean, and Ioannis Havoutis. Constrained skill discovery: Quadruped locomotion with unsupervised reinforcement learning. _arXiv preprint arXiv:2410.07877_ , 2024. 

- L´eonard Blier, Corentin Tallec, and Yann Ollivier. Learning successor states and goal-dependent values: A mathematical viewpoint. _arXiv preprint arXiv:2101.07123_ , 2021. 

- Greg Brockman, Vicki Cheung, Ludwig Pettersson, Jonas Schneider, John Schulman, Jie Tang, and Wojciech Zaremba. Openai gym. _arXiv preprint arXiv:1606.01540_ , 2016. 

- Rafael Cathomen, Mayank Mittal, Marin Vlastelica, and Marco Hutter. Divide, discover, deploy: Factorized skill learning with symmetry and style priors. _arXiv preprint arXiv:2508.19953_ , 2025. 

- Jin Cheng, Marin Vlastelica, Pavel Kolev, Chenhao Li, and Georg Martius. Learning diverse skills for local navigation under multi-constraint optimality. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 5083–5089. IEEE, 2024. 

- Benjamin Eysenbach, Abhishek Gupta, Julian Ibarz, and Sergey Levine. Diversity is all you need: Learning skills without a reward function. In _International Conference on Learning Representations_ , 2018. 

- Karol Gregor, Danilo Jimenez Rezende, and Daan Wierstra. Variational intrinsic control. _arXiv preprint arXiv:1611.07507_ , 2016. 

- Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_ , 2025. 

- Steven Hansen, Will Dabney, Andre Barreto, David Warde-Farley, Tom Van de Wiele, and Volodymyr Mnih. Fast task inference with variational intrinsic successor features. In _International Conference on Learning Representations_ , 2019. 

- Shuncheng He, Yuhang Jiang, Hongchang Zhang, Jianzhun Shao, and Xiangyang Ji. Wasserstein unsupervised reinforcement learning. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 36, pp. 6884–6892, 2022. 

11 

Published as a conference paper at ICLR 2026 

- Jonathan Ho and Stefano Ermon. Generative adversarial imitation learning. _Advances in neural information processing systems_ , 29, 2016. 

- Hyunseung Kim, BYUNG KUN LEE, Hojoon Lee, Dongyoon Hwang, Donghu Kim, and Jaegul Choo. Do’s and don’ts: Learning desirable skills with instruction videos. _Advances in Neural Information Processing Systems_ , 37:47741–47766, 2024. 

- Diederik P Kingma and Jimmy Ba. Adam: A method for stochastic optimization. _arXiv preprint arXiv:1412.6980_ , 2014. 

- Michael Laskin, Hao Liu, Xue Bin Peng, Denis Yarats, Aravind Rajeswaran, and Pieter Abbeel. Unsupervised reinforcement learning with contrastive intrinsic control. In _Advances in Neural Information Processing Systems_ , 2022. 

- Chenhao Li, Marco Hutter, and Andreas Krause. Feature-based vs. gan-based learning from demonstrations: When and why. _arXiv preprint arXiv:2507.05906_ , 2025. 

- Yunzhu Li, Jiaming Song, and Stefano Ermon. Infogail: Interpretable imitation learning from visual demonstrations. _Advances in neural information processing systems_ , 30, 2017. 

- Hao Liu and Pieter Abbeel. Aps: Active pretraining with successor features. In _International Conference on Machine Learning_ , pp. 6736–6747. PMLR, 2021a. 

- Hao Liu and Pieter Abbeel. Behavior from the void: Unsupervised active pre-training. _Advances in Neural Information Processing Systems_ , 34:18459–18473, 2021b. 

- Zhengyi Luo, Jinkun Cao, Alexander W. Winkler, Kris Kitani, and Weipeng Xu. Perpetual humanoid control for real-time simulated avatars. In _International Conference on Computer Vision (ICCV)_ , 2023. 

- Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, et al. Isaac gym: High performance gpu-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 

- Aaron van den Oord, Yazhe Li, and Oriol Vinyals. Representation learning with contrastive predictive coding. _arXiv preprint arXiv:1807.03748_ , 2018. 

- Sherjil Ozair, Corey Lynch, Yoshua Bengio, Aaron Van den Oord, Sergey Levine, and Pierre Sermanet. Wasserstein dependency measure for representation learning. _Advances in Neural Information Processing Systems_ , 32, 2019. 

- Jonghae Park, Daesol Cho, Jusuk Lee, Dongseok Shim, Inkyu Jang, and H Jin Kim. Periodic skill discovery. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ . 

- Seohong Park, Jongwook Choi, Jaekyeom Kim, Honglak Lee, and Gunhee Kim. Lipschitzconstrained unsupervised skill discovery. In _International Conference on Learning Representations_ , 2021. 

- Seohong Park, Kimin Lee, Youngwoon Lee, and Pieter Abbeel. Controllability-aware unsupervised skill discovery. _arXiv preprint arXiv:2302.05103_ , 2023a. 

- Seohong Park, Oleh Rybkin, and Sergey Levine. Metra: Scalable unsupervised rl with metric-aware abstraction. In _The Twelfth International Conference on Learning Representations_ , 2023b. 

- Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel Van de Panne. Deepmimic: Exampleguided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- Xue Bin Peng, Yunrong Guo, Lina Halper, Sergey Levine, and Sanja Fidler. Ase: Large-scale reusable adversarial skill embeddings for physically simulated characters. _ACM Transactions On Graphics (TOG)_ , 41(4):1–17, 2022. 

- Seungeun Rho, Laura Smith, Tianyu Li, Sergey Levine, Xue Bin Peng, and Sehoon Ha. Language guided skill discovery. In _The Thirteenth International Conference on Learning Representations_ , 2024. 

12 

Published as a conference paper at ICLR 2026 

- Seungeun Rho, Kartik Garg, Morgan Byrd, and Sehoon Ha. Unsupervised skill discovery as exploration for learning agile locomotion. In _Conference on Robot Learning_ , pp. 2678–2694. PMLR, 2025. 

- John Schulman, Philipp Moritz, Sergey Levine, Michael Jordan, and Pieter Abbeel. Highdimensional continuous control using generalized advantage estimation. _arXiv preprint arXiv:1506.02438_ , 2015. 

- John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- Chen Tessler, Yoni Kasten, Yunrong Guo, Shie Mannor, Gal Chechik, and Xue Bin Peng. Calm: Conditional adversarial latent models for directable virtual characters. In _ACM SIGGRAPH 2023 Conference Proceedings_ , pp. 1–9, 2023. 

- Chen Tessler, Yunrong Guo, Ofir Nabati, Gal Chechik, and Xue Bin Peng. Maskedmimic: Unified physics-based character control through masked motion inpainting. _ACM Transactions on Graphics (TOG)_ , 43(6):1–21, 2024. 

- Andrea Tirinzoni, Ahmed Touati, Jesse Farebrother, Mateusz Guzek, Anssi Kanervisto, Yingchen Xu, Alessandro Lazaric, and Matteo Pirotta. Zero-shot whole-body humanoid control via behavioral foundation models. _arXiv preprint arXiv:2504.11054_ , 2025. 

- Ahmed Touati and Yann Ollivier. Learning one representation to optimize all rewards. _Advances in Neural Information Processing Systems_ , 34:13–23, 2021. 

- An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. _arXiv preprint arXiv:2505.09388_ , 2025. 

13 

Published as a conference paper at ICLR 2026 

A QUALITATIVE RESULTS FOR CONTROLLING DIVERSITY EXPERIMENT 


Figure 6: Red dots indicate the agent’s trajectory. From left to right, as we sample the latent variable _z_ from increasingly wider distributions centered around the reference motion, the resulting behaviors become more diverse while still preserving the core characteristics of the original motion. 

## B FROM VMF ENCODER TO INFONCE LOSS 

Recall the encoder defines a von Mises–Fisher (vMF) density on the unit hypersphere: 


where _Cd_ ( _κ_ ) is the normalizing constant and _κ >_ 0 is fixed. 

Given an anchor _s_<sup>_a_</sup> and a candidate set _C_ = _{z_<sup>+</sup> _, z_ 1<sup>_−, . . . , z_</sup> _K_<sup>_−}_containingonepositiveand</sup><sup>_K_</sup> negatives, consider the conditional probability that the positive _z_<sup>+</sup> was generated from _qϕ_ ( _· | s_<sup>_a_</sup> ) among the candidates: 


Because _κ_ is fixed, _Cdd_ ( _κ_ ) cancels: cancels: 

Maximizing the log-likelihood of the correct positive is therefore equivalent to minimizing the crossentropy loss 


Identifying the _similarity_ as the dot product on the unit sphere, sim( sim( _u, v_ ) = _u_<sup>_⊤_</sup> _v_ (cosine similarity), and setting the temperature _T_ = 1 _/κ_ , we obtain the standard InfoNCE form: 

If we instantiate the candidates by their mean directions, i.e., _z_<sup>_a_</sup> = _µϕ_ ( _s_<sup>_a_</sup> ), _z_<sup>+</sup> = _µϕ_ ( _s_<sup>+</sup> ), and _zj_<sup>_−_=</sup><sup>_µϕ_(</sup><sup>_s−_</sup> _j_<sup>), then the loss reduces exactly to the temperature-scaled dot-product InfoNCE used in</sup> the main text (with _T_ = 1 _/κ_ ). 

14 

Published as a conference paper at ICLR 2026 

## C PROOF OF WITHIN–MOTION ALIGNMENT 

We prove that under the InfoNCE objective with “same–motion” positives, the optimal encoder perfectly aligns all frames of a given motion to a single unit vector on the sphere. 

**Proof.** Let there be _N_ motions. Each motion _m ∈{m_ 1 _, . . . , mN }_ is a sequence of states _s ∈_ R<sup>_d_</sup> . An encoder _µϕ_ maps each state to a unit vector _u_ = _µϕ_ ( _s_ ) _∈Z_ . 

For an anchor _u ∈ m_ , we draw a positive _v ∈ m_ (independent) and negatives _n_ 1 _, . . . , nK_ from other motions. The InfoNCE loss for this triplet is 


Fix _u_ and negatives _{nj}_ . Write _s_ = _u_<sup>_⊤_</sup> _v ∈_ [ _−_ 1 _,_ 1] and _C_ =<sup>�</sup> _j_<sup>exp(</sup><sup>_u⊤nj/T_).Then</sup> 


Differentiating LHS with _s_ , 


so _ℓ_ ( _s_ ) **is monotonically decreasing in** _s_ . Hence, the loss is minimized by maximizing _u_<sup>_⊤_</sup> _v_ , which is at most 1 and attained only when _v_ = _u_ . This implies that the angle between embeddings of frames from the same motion should be minimized, resulting in a perfect alignment. 

**Reduction of the loss.** After the alignment, for motion _m_ we have _u_ = _v_ = _µm_ , and equation 9 reduces to 


The total loss<sup>�</sup> _m_<sup>_ℓm_nowdependsonlyonthepairwiseinnerproducts</sup><sup>_µ_</sup> _m_<sup>_⊤µj_.Minimizingthis</sup> objective pushes the vectors _{µm}_ as far apart as geometry allows, yielding a regular simplex when _M ≤ k_ + 1. 

## D PROOF OF GUARANTEE AS AN IMITATION REWARD 

Our goal is to prove two properties of the reward function in Eq. 7: **(i)** the reward achieves its optimum when the agent visits the exact states of motion _m_ , and **(ii)** the reward function is locally quasi-concave around the states _s ∈ m_ . 

### D.1 PROOF OF REWARD OPTIMALITY ON MOTION STATES 

**Assumption.** We assume that the pretraining of _µϕ_ in Section 4.1 has reached its theoretical optimum. More concretely, for all _m ∈M_ and for all _{s_ 1 _, s_ 2 _, . . . , slm} ⊂ m_ , we have 


where _lm_ is the number of states in motion _m_ . Therefore, from Eq. 5, 


**Proof.** From Eq. 7, the reward can be written as 


15 

Published as a conference paper at ICLR 2026 

where _C_ and _κ_ are constants that do not affect the optimal point. Discarding the constants, we can write 


Substituting _µϕ_ ( _s_ ) with Eq. 10, we obtain 


Since _r_ ( _s, zm_ ) is bounded within [ _−_ 1 _,_ 1], this value is the global optimum. Hence, every state _s ∈ m_ achieves the global optimum. 

D.2 PROOF OF LOCAL QUASI-CONCAVITY OF THE REWARD 

**Assumption.** We assume from Eq. 10 that for every _s_<sup>_⋆_</sup> _∈ m_ we have _µϕ_ ( _s_<sup>_⋆_</sup> ) = _zm_ . We designed the neural network _µ_ ˆ _ϕ_ to be piecewise linear in a neighborhood of _s_<sup>_⋆_</sup> , and normalization is applied to the output so that _µϕ_ ( _s_ ) = _µ_ ˆ _ϕ_ ( _s_ ) _/∥µ_ ˆ _ϕ_ ( _s_ ) _∥_ lies in a unit hypersphere for all _s ∈S_ . 

**Lemma.** Let _s_<sup>_⋆_</sup> _∈S_ be a state in a motion that satisfies _µϕ_ ( _s_<sup>_⋆_</sup> ) = _µ_ ˆ _ϕ_ ( _s_<sup>_⋆_</sup> ) _/∥µ_ ˆ _ϕ_ ( _s_<sup>_⋆_</sup> ) _∥_ 2 = _zm_ . Then _r_ ( _s_ ) := _⟨µϕ_ ( _s_ ) _, zm⟩_ is quasi-concave in a neighborhood of _s_<sup>_⋆_</sup> . 

**Proof.** To show that _r_ ( _s_ ) is quasi-concave in a neighborhood of _s_<sup>_⋆_</sup> , we want to show that inside the neighborhood _Bϵ_ ( _s_<sup>_⋆_</sup> ), the superlevel set _Sα_ ( _r_ ) = _{s_ : _r_ ( _s_ ) _≥ α}_ is convex. 

To show this, we first check the convexity of the superlevel set in the latent space. Then, by leveraging the fact that the preimage of an affine transform preserves convexity, we conclude the convexity of the superlevel set in the state space. 

**Convexity of superlevel set in latent space.** We define a function in latent space _f_ ( _z_ ) = _zm_<sup>_⊤z/∥z∥_2.Thissatisfies</sup><sup>_f_(ˆ</sup><sup>_µϕ_(</sup><sup>_s_))=</sup><sup>_r_(</sup><sup>_s_).Wenowshowtheconvexityofthesuperlevelsetof</sup> _f_ : 


To show its convexity, for _∀z_ 1 _, z_ 2 _∈ Sα_ ( _f_ ) and _t ∈_ [0 _,_ 1], we plug in _z ← tz_ 1 + (1 _− t_ ) _z_ 2: 


Therefore, _tz_ 1 + (1 _− t_ ) _z_ 2 _∈ Sα_ ( _f_ ), so _Sα_ ( _f_ ) is convex. 

**Convexity of superlevel set in state space.** Here, we use the fact that the preimage of an affine transform also preserves convexity: when _T_ ( _s_ ) := _As_ + _b_ is affine, then _T_<sup>_−_1</sup> ( _Sα_ ( _f_ )) is convex. The superlevel set of _r_ ( _s_ ) = _f_ (ˆ _µϕ_ ( _s_ )) is defined as: 


Since the affine property only applies near the neighborhood of _s_<sup>_⋆_</sup> , we can define an open ball around _s_<sup>_⋆_</sup> that satisfies such a condition: 


16 

Published as a conference paper at ICLR 2026 

Restricting the domain to the ball, we have: 


This set is also convex because the intersection of two convex sets is also convex. This proves that the superlevel set of _r_ ( _·_ ) is convex local to _s_<sup>_⋆_</sup> . 

**Conclusion** By definition of quasi-concavity, we conclude that _r_ ( _·_ ) is quasi-concave in the neighborhood of _s_<sup>_⋆_</sup> , _Bϵ_ ( _s_<sup>_⋆_</sup> ). 

17 

Published as a conference paper at ICLR 2026 

- E WITHIN-MOTION ALIGNMENT: LATENT SPACE VISUALIZATION AFTER PRETRAINING 


Figure 7: Latent embeddings of all 20 reference motions using the pretrained encoder. Each point corresponds to a single frame, and different colors represent different motions. 

To evaluate the degree of within-motion alignment, we visualize the latent embeddings of each motion in a 3D space using the pretrained encoder _µϕ_ . Because the latent vectors are 16-dimensional, we display only their first three dimensions. As shown in Fig. 7, after 1000 epochs of training with the loss in Eq. 8, the state-wise embeddings within each motion form tight clusters and are nearly perfectly aligned, which is consistent with our theoretical results in Section C. 

We also quantify this alignment using cosine similarity. For each motion _mi ∈M_ , we first compute its motion-level embedding _zmi_ using Eq. 5. Then, for every state _s ∈ mi_ , we measure the cosine similarity between its latent embedding and _zmi_ , and average these values to obtain the withinmotion alignment score for that motion. Across all 20 motions in the dataset, the average withinmotion alignment is 0 _._ 99998 _±_ 8 _._ 91 _×_ 10<sup>_−_6</sup> , empirically confirming the effectiveness of the alignment objective. 

In practice, overlapping states across different motions can make the motion embeddings harder to distinguish. We mitigate this issue by introducing a phase variable _t_ and concatenating it to each frame _ot_ , as well as defining each state as a stack of the most recent _n_ frames, _st_ = [ _ot−n_ +1 _, ot−n_ +2 _, . . . , ot_ ]. This reduces the likelihood that two motions share identical frame sequences at the same phase _t_ . In our dataset, _n_ = 5 works well, though the optimal value may vary depending on the data. Additionally, our method is robust to a small number of overlapping states, as long as they do not significantly pull the motion-level embeddings of different motions closer together. 

18 

Published as a conference paper at ICLR 2026 

## F FULL ALGORITHM OF RGSD 

- **Algorithm 1** RGSD - Pretraining 1: Initialize encoder function _qϕ_ ( _s_ ), reference dataset _M_ 2: **for** _i ←_ 1 to # of epochs **do** 3: Sample _m ∼_ Uniform( _M_ ) 4: Sample _x_<sup>_a_</sup> _, x_<sup>+</sup> from _m_ , _x_<sup>_−_</sup> from _{M − m}_ 5: Update _qϕ_ with _L_ InfoNCE on Eq. 8 6: **end for** 

After pretraining is completed, imitatino and discovery happen in parallel. 

**Algorithm 2** RGSD: Imitation & Discovery 

- 1: **Initialize:** skill-conditioned policy _πθ_ , frozen pretrained encoder _qϕ_<sup>_−_, trainable encoder</sup><sup>_qϕ_, im-</sup> itation ratio _p_ , KL loss coefficient _α_ , reference dataset _M_ , set of reference motion embeddings _Z_ ref , feature mask _ϕ_ mask, and replay buffer _D_ 

- 2: Initialize _qϕ ← qϕ_<sup>_−_</sup> 3: **for** _i ←_ 1 **to** number of epochs **do** 4: **for** _j ←_ 1 **to** episodes per epoch **do** 5: Sample task indicator _c ∼_ Bernoulli( _p_ ) // 1 being imitation, 0 being discovery 6: Sample reference _m ∼_ Uniform( _M_ ) 7: Initialize _s ∼_ Uniform( _m_ ) 8: Compute _zm_ using Eq. 5 with _qϕ_<sup>_−_.</sup> 9: _z ← zm · c_ + _k/∥k∥·_ (1 _− c_ ), where _k ∼N_ (0 _, I_ ) 

- 10: 11: **while** episode not done **do** 12: Execute _a ∼ πθ_ ( _· | s, z_ ), observe _s_<sup>_′_</sup> 13: Compute reward _r ←_ Const. + log _qϕ_<sup>_−_(</sup><sup>_z| s′_)</sup><sup>_· c_+ log</sup><sup>_qϕ_(</sup><sup>_z| s′_)</sup><sup>_·_(1</sup><sup>_−c_)</sup> 14: Add _{s, a, r, s_<sup>_′_</sup> _, z, c}_ to _D_ 15: _s ← s_<sup>_′_</sup> 16: **end while** 17: **end for** 18: **for** each _{s, a, r, s_<sup>_′_</sup> _, z, c} ∈D_ **do** 19: Compute _Lϕ ←_ (1 _− c_ ) _·_ ( _−_ log _qϕ_ ( _z | s_<sup>_′_</sup> )) + _α ∗ c ·_ KL� _qϕ_ ( _·|s_ ) _∥ qϕ_<sup>_−_(</sup><sup>_·|s_)</sup> � 20: Update _ϕ_ to minimize _Lϕ_ 21: Update _θ_ using PPO with rewards _r_ 22: **end for** 23: **end for** 

## G EXPERIMENTS DETAILS 

- G.1 STATE AND ACTION SPACE 

We use a 3D SMPL humanoid character, commonly adopted in prior work (Luo et al., 2023; Tessler et al., 2024; Tirinzoni et al., 2025). The state representation is defined as follows: 

- phase variable: 1-D 

- root (pelvis) height - 1-D 

- root rotation relative to the local coordinate frame, 69-D 

- local rotation of each joint, , 144-D 

- local velocity of each joint, and , 72-D 

- positions of the hands and feet in the local coordinate frame. 72D 

19 

Published as a conference paper at ICLR 2026 

While policy and value function takes single frame observation as input, encoder takes 5 frames concatenated the latest 5 steps of observations as input, _st_ = ( _ot−_ 4 _, ot−_ 3 _, ot−_ 2 _, ot−_ 1 _, ot_ ). The agent controls the character by outputting target rotations for PD controllers at each joint. In total the character has 23 spherical joints, resulting in 69D action space. 

### G.2 IMPLEMENTATION DETAILS OF BASELINE ALGORITHMS 

To isolate the algorithmic contributions, we removed all additional engineering techniques applied in the original implementations to improve motion robustness. 

For **ASE** , the original training introduces recovery strategies by initializing 10% of the environments in random fallen states. While this clearly improves robustness, we removed this component consistently across our method and all baselines. ASE also incorporates an auxiliary diversity objective: 


where _DZ_ is a distance function. Together with the mutual information objective, _J_ div encourages policies to exhibit diverse behaviors when conditioned on different latent variables. Although this objective is modular and could be applied to any baseline, we excluded it to focus strictly on the main algorithmic differences. 

For **CALM** , we encoded entire motions rather than segmenting them into 2-second clips, since the motion lengths we used (between 2 and 5 seconds) are relatively short. Shorter motions were zero-padded to standardize sequence lengths. 

Finally, following conventions in skill discovery frameworks (Gregor et al., 2016; Eysenbach et al., 2018; Laskin et al., 2022; Park et al., 2023b; Rho et al., 2024), we sampled a skill latent at the beginning of each episode and kept it fixed throughout the rollout. While transitioning between skills is orthogonal and can be incorporated into both our method and the baselines to further improve robustness, we excluded it here to focus on a clean understanding of algorithmic contributions. 

### G.3 LIST OF REFERENCE MOTIONS 

We list the file names (relative paths) of all motions used in our experiments: 

1. ACCAD-smpl/Male2Walking_c3d/B10____Walk_turn_left_45 

2. ACCAD-smpl/Male2Walking_c3d/B9____Walk_turn_left_90 

3. ACCAD-smpl/Male2Walking_c3d/B11____Walk_turn_left_135 

4. ACCAD-smpl/Male2Walking_c3d/B14____Walk_turn_right_45_t2 

5. ACCAD-smpl/Male2Walking_c3d/B13____Walk_turn_right_90 

6. ACCAD-smpl/Female1Walking_c3d/B22___side_step_left 

7. ACCAD-smpl/Female1Walking_c3d/B23___side_step_right 

8. ACCAD-smpl/Male2Running_c3d/C12___run_turn_left_45 

9. ACCAD-smpl/Male2Running_c3d/C11___run_turn_left_90 

10. ACCAD-smpl/Male2Running_c3d/C13___run_turn_left_135 11. ACCAD-smpl/Male2Running_c3d/C15___run_turn_right_45 12. ACCAD-smpl/Male2Running_c3d/C14___run_turn_right_90 

13. ACCAD-smpl/Male2Running_c3d/C16___run_turn_right_135 

14. ACCAD-smpl/Male2Running_c3d/C7___run_backwards_t2 

15. ACCAD-smpl/Female1Walking_c3d/B5___walk_backwards 

16. ACCAD-smpl/Male2Walking_c3d/B5____Walk_backwards 

17. ACCAD-smpl/Male2MartialArtsPunches_c3d/E3____cross_left 

18. ACCAD-smpl/Male2MartialArtsPunches_c3d/E4____cross_right 

19. ACCAD-smpl/Male2MartialArtsPunches_c3d/E7___uppercut_left 

20. ACCAD-smpl/Male2MartialArtsPunches_c3d/E8___uppercut_right 

20 

Published as a conference paper at ICLR 2026 

### G.4 HYPERPARAMETERS 

Table 2: Hyperparameters of RGSD 

|Name|Value|
|---|---|
|**Network Architecture**||
|Dim. of latent_z_|16|
|Policy network_π_|MLP with [1024, 1024, 1024, 512],|
|Activaion of_π_|tanh|
|Encoder network_qϕ_|MLP with [1024, 1024, 1024, 512]|
|Activaion of_qϕ_|ReLU|
|_qϕ_input frame stacks|5|
|**Contrastive pretraining**||
|Minibatch size|256|
|Total number of epochs|3,000|
|Optimizer|Adam(Kingma & Ba, 2014)|
|Learning rate for encoder|1e-4|
|**Imitation and Discovery**||
|Ratio of imitation environments_p_|0.7|
|Learning rate|2e-5(actor), 1e-4(critic), 1e-4(encoder)|
|Optimizer|Adam|
|Minibatch size|32768|
|Horizon length|32|
|PPO clip threshold|0.2|
|PPO number of epochs|5|
|<br>GAE_λ_(Schulman et al., 2015)|0.95|
|Discount factor_γ_|0.99|
|Entropy coefficient|0.1|
|KL loss coefficient|0.5|


## H SUPPLEMENTARY DISCUSSION: CHALLENGES OF EXPANDING RGSD WITH METRA 

In Section 6, we have discussed why the METRA objective conflicts with learning repetitive motions when only local observations are available. A potential workaround is to augment the state with additional variables, such as a global coordinate or time variable. These variables could help distinguish between locally identical motions, e.g., before and after taking a step from walking motion. However, each approach ultimately faces a challenge for different reasons. 

**Global coordinate information.** Given that all state information is computed in the agent’s local coordinate system, the first and last states of a walking behavior appear identical. Concatenating global coordinate to the state would allow the state to capture this progress. However, this approach still cast issues. First, not all motions produce meaningful displacement in global coordinates (e.g., shaking hands). More importantly, incorporating global position creates an imbalance in the state representation. All other state dimensions are bounded, which implies that the output of _ϕ_ is bounded as well. In contrast, global position is unbounded, and METRA can exploit this property. Recall that the METRA reward is defined as [ _ϕ_ ( _s_<sup>_′_</sup> ) _− ϕ_ ( _s_ )]<sup>_⊤_</sup> _z_ , where reward increases when the agent visits new states _s_<sup>_′_</sup> along the _z_ direction in latent space. Because global position is unbounded, changes in position always yield new states, regardless of behavior. Consequently, the agent ends up learning skills that simply move in different directions when conditioned on different _z_ , since this suffices to maximize the reward. 

**Time variable.** A time variable could serve as a meaningful alternative to the global coordinate, as it is less likely to be exploited by the METRA reward. Although the time variable is also unbounded, it advances uniformly across all behaviors regardless of the underlying dynamics, it increments by 

21 

Published as a conference paper at ICLR 2026 


Figure 8: Conceptual figure of latent space learned by METRA with time variable. 


Figure 9: Latent space learned with **METRA** . It shows seven reference trajectories and the agent’s trajectory (blue line with x markers). We introduce a time variable to differentiate locally identical state pairs in repetitive motions, which causes the agent trajectory to exhibit discontinuous transitions in the latent space. 

a constant amount at every step. This ensures that no behavior can accelerate or decelerate its progression. Moreover, it effectively differentiates identical states over time. Therefore the agent retains the opportunity to learn meaningful behaviors, rather than exploiting state changes of specific dimensions. 

However, this design still introduces issues. Figure 8 illustrates an ideal latent space of reference motions formed by METRA with a time variable. Each motion is aligned with a distinct directional vector, and consecutive states are placed at a distance of 1. In this setup, the time variable naturally induces a _contour_ : distances in the latent space correspond to “temporal distances,” i.e., the minimum number of transition steps required to reach a given state. For example, if the time variable is 3, then reaching that state requires exactly three transitions, and at the optimum of the representation function _ϕ_ , all behaviors at timestep 3 should lie on the same contour. 

The core problem arises during METRA exploration. When the agent transitions at large _t_ values—for example, from the _t_ =100 contour to the _t_ =101 contour—it may undergo an _abrupt transition_ of considerable magnitude in the latent space, especially if the subsequent pose lies on the opposite side of the contour. This phenomenon is illustrated in Fig. 9. Since METRA enforces that the latent distance between successive states must be less than 1, such discontinuities break the contour structure. As a result, temporal coherence in the latent space is lost, and the representation collapses. In short, constructing an idealized latent space from reference data while respecting METRA constraints with a phase variable introduces a fundamental conflict, leading to highly unstable training. 

22 

