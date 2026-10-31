---
title: "Hierarchical Planning with Latent World Models"
date: "2026-04-03"
authors: "Wancong Zhang; Basile Terver; Artem Zholus; Soham Chitnis; Harsh Sutaria; Mido Assran"
url: https://arxiv.org/abs/2604.03208
pdf: https://arxiv.org/pdf/2604.03208
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.03208)** / [論文ページ](https://arxiv.org/abs/2604.03208)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Hierarchical Planning with Latent World Models** 

**Wancong Zhang**<sup>1</sup><sup>_,_2</sup><sup>_,∗_</sup> **Basile Terver**<sup>1</sup> **Artem Zholus**<sup>1</sup><sup>_,_3</sup> **Soham Chitnis**<sup>2</sup> **Harsh Sutaria**<sup>2</sup> **Mido Assran**<sup>1</sup> **Randall Balestriero**<sup>1</sup><sup>_,_4</sup> **Amir Bar**<sup>1</sup> **Yann LeCun**<sup>2</sup><sup>_,†_</sup> **Nicolas Ballas**<sup>1</sup><sup>_,†_</sup> 

1FAIR at Meta 2New York University 3Mila - Québec AI Institute 4Brown University _∗_ Work done at Meta _†_ Joint last author 

Correspondence: `wz1232@nyu.edu` � Website � Code 

**Abstract:** World models are a promising path to zero-shot embodied control through planning. However, existing world model planners struggle on longhorizon, multi-stage tasks: prediction errors compound and naive search is exponential in the planning horizon. Hierarchy mitigates both by decomposing tasks into shorter, tractable subproblems; yet prior hierarchical approaches either amortize control into task-specific policies (hierarchical RL) or assume low-dimensional states and known dynamics (classical hierarchical MPC). We present Hierarchical Planning with Latent World Models (HWM), an architecture and planning paradigm for hierarchical model predictive control directly on visual world models trained solely via next-latent prediction. HWM learns world models at multiple temporal scales within a shared latent space, so predictions from the long horizon model serve as subgoals for the short horizon model via latent matching—without task-specific rewards or hierarchical policies. To keep long-horizon search tractable, HWM learns an action encoder that compresses primitive action chunks into latent macro-actions. On real-world Franka manipulation, HWM solves pick-&-place from a single goal image at 70% success vs. 0% for single-level planning. Across simulated push manipulation and maze navigation, HWM consistently improves performance on long-horizon tasks while requiring up to 3× less planning compute. 

**Keywords:** Latent World Models, Planning 

## **1 Introduction** 

Planning with learned world models has emerged as a powerful paradigm for embodied decision making: by simulating the consequences of candidate actions, an agent can reason about long-term outcomes without acting in the environment [1, 2, 3]. Recent advances in latent-space modeling and self-supervised learning have made it possible to train such models directly from large collections of unlabeled, task-agnostic offline trajectories, enabling zero-shot planning from high-dimensional observations such as pixels [4, 5, 6, 7, 8]. Yet single-level planning with these models fails in two distinct regimes. On tasks with non-greedy objectives, such as pick-and-place, the optimal trajectory must temporarily move away from the goal. The resulting non-monotone goal-matching cost can trap local optimizers in greedy shortcuts even at modest horizons; empirically, even simple real-world pick-and-place is out of reach for state-of-the-art world-model planners such as VJEPA2-AC [4] (Table 1). On long-horizon tasks, prediction errors compound over autoregressive rollouts [9, 10] and the action search space grows exponentially with horizon [11]. 

Introducing temporal hierarchy into decision-making — reasoning coarsely over long horizons while retaining fine-grained control at short horizons — has long been studied as a way to mitigate both effects, but existing approaches do not transfer cleanly to zero-shot planning on visual world models. Hierarchical reinforcement learning based on options, skills, or hierarchical policies [12, 13, 14, 15] requires task-specific rewards or task distributions, and even modern goal-conditioned and zero-shot 

10th Conference on Robot Learning (CoRL 2026), Austin, Texas, USA. 


**Figure 1: Top: Hierarchical planning in latent space.** A high-level planner optimizes macro-actions using a long-horizon world model to reach the goal; the first predicted latent state from the high-level rollout serves as the subgoal for a low-level planner, which optimizes primitive actions with a short-horizon world model. Both levels replan as new observations arrive, in a closed-loop MPC fashion. Solid borders denote ground-truth observations; others are decoder reconstructions shown for interpretability only. **Bottom Left:** HWM improves long-horizon planning on 3 latent world model architectures across 4 task suites. **Bottom Right:** Success rate versus normalized planning time. HWM matches or exceeds performance with up to 3 _×_ lower planning time. 

RL methods [15, 16] generalize poorly beyond training [5]. Hierarchical world models have been explored in the RL setting [17, 18, 19], but remain coupled to policy learning over a specific task distribution. Hierarchical MPC in optimal control [20, 21, 22] is task-agnostic but has been confined to low-dimensional states, hand-engineered features, or known dynamics. It remains unclear how to realize hierarchical zero-shot planning directly on visual world models. 

We propose _Hierarchical Planning with Latent World Models_ (HWM), a framework for zero-shot hierarchical MPC over learned latent world models (Table 5 contrasts HWM with prior hierarchical model-based methods). HWM trains world models at multiple temporal resolutions within a shared latent space, supervised solely by next-latent prediction, and couples them at planning time: predictions from the coarser model serve as subgoals that the finer-scale MPC matches in latent space; no hierarchical policy, skill, or goal-conditioned controller is needed. To support efficient long-horizon planning, we further introduce a learned action encoder that compresses sequences of primitive actions between waypoint states into latent macro-actions, reducing the dimensionality of the coarser-scale search. To our knowledge, HWM is the first world-model planner to demonstrate zero-shot, real-robot manipulation under non-greedy objectives from pixels with a single goal image, solving Franka pick-&-place at 70% success while single-level VJEPA2-AC planner [4] achieves 0%. 

We summarize our contributions as follows: 

- We introduce HWM, a hierarchical MPC formulation that couples learned world models at different temporal scales via a shared latent space, enabling direct subgoal transfer across levels without hierarchical policies, skill learning, or task-specific rewards. 

2 


**Figure 2: Hierarchical planning in latent space.** A high-level planner optimizes macro actions using a long-horizon latent world model to reach the final goal. The first high level latent prediction serves as a subgoal for low-level planning, where a short-horizon world model optimizes primitive actions to reach this subgoal. 

- We show that HWM unlocks a new capability for zero-shot world-model planning: solving real-robot tasks with non-greedy objectives from visual inputs, where success requires temporarily moving away from the goal. HWM achieves 70% success on Franka pick-&place from a single goal image, compared to 0% for VJEPA2-AC [4], and also compares favorably to several zero-shot VLA baselines under the evaluated setup. 

- We demonstrate consistent gains across three latent world-model backbones — VJEPA2-AC (manipulation), DINO-WM (push manipulation), and PLDM (maze navigation) — and show that hierarchical planning improves both performance (up to +44% and +39% absolute) and efficiency (up to 3 _×_ less planning compute) on long-horizon tasks. 

## **2 Hierarchical Planning with Latent World Models** 

**Problem Setting.** We consider goal-conditioned control in an MDP _M_ = ( _S, A, µ, p_ ) with access to an offline dataset _D_ of state-action trajectories _τ_ = ( _s_ 1 _, a_ 1 _, s_ 2 _, . . . , aT −_ 1 _, sT_ ). At test time, the agent receives an observation _st_ and a goal observation _sg_ , both raw pixels, and must reach the goal via through model predictive control. Given a learned world model and a planning horizon _h_ , MPC optimizes a candidate action sequence _at_ : _t_ + _h−_ 1 under a goal-reaching objective, executes the first _k ≤ h_ actions, observes the new state, and replans. 

**Planning with Latent World Models.** A latent world model consists of an encoder _E_ mapping observations to latent states _zt_ = _E_ ( _st_ ) and a predictor _F_ forecasting future latents under candidate actions. In latent-space MPC, the planner encodes the current and goal observations as _z_ 1 = _E_ ( _s_ 1) and _zg_ = _E_ ( _sg_ ), then optimizes primitive actions _a_<sup>_∗_</sup> 1: _h_<sup>=arg min</sup><sup>_a_ˆ</sup> 1: _h_<sup>_∥F_(ˆ</sup><sup>_a_1:</sup><sup>_h_;</sup><sup>_z_1)</sup><sup>_−zg∥_1, where</sup> _F_ (ˆ _a_ 1: _h_ ; _z_ 1) is the final latent after autoregressive rollout. This policy-free formulation enables zeroshot goal-conditioned control, but such single-level planning suffers from the two failure modes identified in Section 1 — getting trapped in greedy solutions under non-greedy objectives, and compounding error and exponential action search on long-horizon tasks. We address both by planning hierarchically over latent world models at multiple timescales: Section 2.1 describes how to train these models, and Section 2.2 describes how to use them for hierarchical planning. 

### **2.1 Learning Multi-Timescale Latent World Models** 

We train multiple world models operating at different time scales in a shared latent space to support hierarchical MPC. The low-level model _Fθ_<sup>(1)</sup> is a standard latent world model trained to predict the next latent state (Appendix A.1). The high-level model _Fϕ_<sup>(2)</sup> predicts dynamics across temporally extended segments, conditioned on latent _macro-actions lt_ . 

3 

During training, a learned action encoder _Aψ_ produces macro-actions by summarizing chunks of primitive actions. We do not require a fixed duration for these chunks, allowing each high-level transition to represent a variable-length segment of low-level execution. This allows _F_<sup>(2)</sup> to overcome two limitations _ϕ_ of single-level planning. First, fewer autoregressive rollout steps are needed to reach a goal horizon, reducing compounding error. Second, compressing primitive action chunks into a lower-dimensional latent space shrinks the high-level MPC search space, making long-horizon optimization more tractable. Learned macro-actions outperform both concatenated primitive actions and hand-crafted summaries such as net end-effector displacement (Section 3.4). 


**Figure 3:** The high-level world model captures long-horizon dynamics using macro-actions encoded from chunks of low-level actions. It is causal and trained with a latent prediction loss. 

Given a trajectory _τ_ = ( _s_ 1 _, a_ 1 _, . . . , sT_ ), we sample _N_ waypoint indices 1 = _t_ 1 _< . . . < tN ≤ T_ , encode waypoints as _ztk_ = _E_ ( _stk_ ) and action chunks as _ltk_ = _Aψ_ ( _atk_ : _tk_ +1 _−_ 1), and feed the interleaved sequence ( _ltk , ztk_ ) _k∈_ [ _N −_ 1] to _Fϕ_<sup>(2)</sup> to predict the next waypoint latents _z_ ˆ _tk_ +1 := _Fϕ_<sup>(2)((</sup><sup>_lti, zti_)</sup><sup>_i≤k_).We supervise with the teacher-forcing</sup><sup>_ℓ_1loss</sup> _L_ tf ( _ϕ, ψ_ ) := _N_ <u>1</u> _−_ 1 � _Nk_ =1 _−_ 1<sup>_∥z_ˆ</sup><sup>_t_</sup> _k_ +1<sup>_−zt_</sup> _k_ +1<sup>_∥_1.We use this teacher-forcing objective for Franka and</sup> Push-T, and an autoregressive rollout objective for Diverse Maze (Appendix A.1). With both models trained, hierarchical MPC follows directly (Section 2.2). 

### **2.2 Top-Down Hierarchical Planning** 

Using the trained world models from Section 2.1, we adopt a _top-down_ hierarchical planning strategy operating entirely in their shared latent space (Fig. 2). A high-level planner optimizes macro-actions toward the goal using _F_<sup>(2)</sup> , and the resulting latent predictions serve as subgoals for a low-level planner optimizing primitive actions using _F_<sup>(1)</sup> , in a receding-horizon manner. 

**High-Level Planning.** Given an initial observation _s_ 1 and a goal observation _sg_ , we encode them into latent space as _z_ 1 = _E_ ( _s_ 1) and _zg_ = _E_ ( _sg_ ). At the high level, we plan over a sequence of _H_ macro-actions<sup>ˆ</sup> _l_ 1: _H_ by minimizing a goal-conditioned energy function in latent space: 


Here, _F_<sup>(2)</sup> (<sup>ˆ</sup> _l_ 1: _H_ ; _z_ 1) denotes the final latent state obtained by autoregressively unrolling the world model _F_<sup>(2)</sup> starting from _z_ 1 with macro-actions<sup>ˆ</sup> _l_ 1: _H_ . The optimal macro-action sequence is given by: _l_ 1:<sup>_∗_</sup> _H_<sup>= arg minˆ</sup> _l_ 1: _H_<sup>_E_2(ˆ</sup><sup>_l_1:</sup><sup>_H_;</sup><sup>_z_1</sup><sup>_, zg_)</sup><sup>_._</sup> Unrolling the optimized latent plan yields a sequence of intermediate latent subgoals at the high-level temporal resolution: _z_ ˜ _i_ ≜ _F_<sup>(2)</sup> ( _l_ 1:<sup>_∗_</sup> _i_<sup>;</sup><sup>_z_1)</sup><sup>_,i_= 1</sup><sup>_, . . . , H_.</sup> 

Because macro-actions are latent rather than physical, their scale and support are determined by training rather than known a priori; we therefore use per-dimension statistics of macro-actions produced during training to initialize and bound the high-level search distribution (appendix B). 

**Low-Level Planning.** At execution time, the agent plans primitive actions to reach the first latent subgoal _z_ ˜1. Starting from the current latent state _z_ 1, we define a low-level energy function over a horizon of _h_ steps: 


The optimal low-level action sequence is obtained via _a_<sup>_∗_</sup> 1: _h_<sup>= arg min</sup><sup>_a_ˆ</sup> 1: _h_<sup>_E_1(ˆ</sup><sup>_a_1:</sup><sup>_h_;</sup><sup>_z_1</sup><sup>_,_˜</sup><sup>_z_1).The agent</sup> executes the actions corresponding to the first _k_ low-level prediction steps before replanning. At successive replanning steps, we progressively shorten the high-level planning horizon (appendix B). 

4 


**Figure 4:** Executions on pick-&-place and drawer manipulation with a dual-gripper Franka. Dotted red columns indicate subgoals inferred by the high-level planner and decoded for visualization. Executions on additional tasks are shown in appendix I. 

## **3 Empirical Evaluation of Hierarchical Planning Across World Models** 

We evaluate HWM on three latent world-model architectures — VJEPA2-AC [4], DINO-WM [7], and PLDM [5] — under harder versions of their original settings: real-world Franka manipulation without explicit subgoals (VJEPA2-AC), Push-T extended from 25 to 75 timesteps (DINO-WM), and PointMaze with train–test layout mismatch and larger maps (PLDM). 

### **3.1 Franka Arm with Robotiq Gripper** 

We evaluate HWM on real-world multi-stage Franka manipulation: pick-&-place and drawer opening/closing. These tasks require non-greedy behavior, where success depends on intermediate motions that temporarily increase distance to the goal. 

**Platform and Task.** We follow the VJEPA2-AC deployment setup and evaluate on real-world pick&-place and drawer manipulation using a 7-DoF Franka Emika Panda arm with a two-finger gripper. Pick-&-place includes 10 start–goal pairs across two objects (cup and box); drawer manipulation covers 7 opening and closing tasks (appendix G). We run N=5 independent trials per configuration, yielding 50 trials for pick-&-place per object and 35 for drawer; per-configuration outcomes are highly consistent (appendix H). 

**Baselines. VJEPA2-AC** [4] is a single-level, world-model-based planner. Because we use the same architecture and training data for our low-level world model, this comparison isolates the effect of hierarchical planning. We additionally evaluate three vision–language-action models (VLA) baselines **Octo** , **_π_** 0-FAST-DROID, and **_π_** 0 _._ 5-DROID (see appendix L.1 for details). 

**Data.** World models are trained on approximately 130 hours of unlabeled real-robot manipulation data from DROID [23] and RoboSet [24]. Observations include RGB images and end-effector proprioception; actions correspond to end-effector delta poses (see appendix A.2 for details). 

**Hierarchical Planning Setup.** The agent receives current and goal observations, each specified by RGB images and end-effector poses, and outputs end-effector delta poses mapped to joint displacements via inverse kinematics. The high-level planner optimizes 4-D macro-actions (we ablate this choice in appendix D.3), while the low-level planner optimizes primitive actions; both use CEM and replan every step. Full hyperparameters are in appendix B.. 

**World Model Architectures.** We follow the VJEPA2-AC training recipe for the low-level world model (see appendix A.2). To train the high-level world model, We use _N_ = 3 waypoint states sampled from trajectory segments spanning up to 4 seconds, with the middle waypoint chosen uniformly at random. Macro-actions are encoded from the intervening low-level actions using a transformerbased action encoder, with the CLS token projected to the macro-action space. For visualization, we decode latent representations into RGB images using a ViT decoder; these reconstructions are used solely for qualitative analysis and are not involved in planning or training (details in appendix F). 

**Main Results.** We report the findings in Table 1. Prior work with VJEPA2-AC [4] has shown strong 

5 

zero-shot generalization to novel environments for **Table 1:** simple tasks such as grasping or reaching, where **Franka** greedy goal matching suffices. Consistent with this, image. per (start, the flat planner succeeds on 2/7 drawer tasks admitting linear push/pull motions, but fails entirely on pick-&-place and on drawer variants requiring nongreedy, multi-stage planning. In contrast, hierarchical tives planning solves both pick-&-place and drawer tasks end-to-end from a single goal image. It generalizes Method zero-shot to novel environments and objects, achieving 70% success on pick-&-place cup and 60% on Octo box, and solves drawer tasks requiring non-greedy, _π_ 0 multi-stage planning (e.g., moving down before trans- _π_ 0 _._ 5-DROID lating laterally). Example executions are in Fig. 4 VJEPA2-AC and appendix I. HWM failures arise mainly from VJEPA2-AC perceptual imprecision (e.g., depth errors) or near(hierarchy) miss executions, suggesting that coarse high-level subgoals can lose details needed for precise low-level guidance. 

**Table 1: Zero-shot robotic manipulation with** 

**Franka** , evaluated end-to-end from a single goal image. Each rate is computed over _N_ = 5 trials per (start, goal) configuration; per-configuration breakdowns and 95% Clopper–Pearson confidence intervals are reported in Table 16. The flat VJEPA2AC planner fails on tasks with non-greedy objectives (pick-&-place, multi-stage drawer); HWM solves them without manual decomposition. 

|Method|P&P Cup|P&P Box|Drawer|
|---|---|---|---|
|Octo|0%|0%|43%|
|_π_0-FAST-DROID|52%|18%|–|
|_π_0_._5-DROID|68%|36%|–|
|VJEPA2-AC|0%|0%|30%|
|VJEPA2-AC<br>(hierarchy)|**70%**|**60%**|**70%**|


We also compare against vision–language–action (VLA) baselines, noting that the comparison spans different goal-specification interfaces: HWM and Octo use a single goal _image_ , while the _π_ -models use _language_ goals (appendix L.1). HWM is competitive with these baselines despite significantly less training data ( _∼_ 77 _×_ ), and far exceeds Octo under identical image-goal supervision. 

**Takeaway:** HWM enables zero-shot manipulation under non-greedy objectives on a real robot from a single goal image, where flat world-model planners fail. 

### **3.2 Push-T** 

We instantiate HWM on top of DINO-WM [7] and evaluate it on goal-conditioned Push-T, where an agent must push a T-shaped object to a goal configuration sampled from a validation trajectory. To stress-test long-horizon planning, we evaluate start–goal pairs up to _d_ = 75 timesteps apart, versus _d_ = 25 evaluated in DINO-WM. Models are trained from the dataset released with DINO-WM. 

**Baselines.** We compare against (i) DINO-WM [7], the flat-planning baseline; (ii) HIQL [15], a stateof-the-art _hierarchical_ goal-conditioned RL method; (iii) GCIQL [25] and HILP [16] as additional goal-conditioned and zero-shot RL baselines (appendix L.2). 

**Hierarchical Planning Setup.** Hierarchical planning is performed using CEM at two temporal scales, with a high-level planner optimizing macro-actions and a low-level planner refining primitive actions in a receding-horizon manner. Full CEM hyperparameters are provided in appendix B. 

**Main Results.** As shown in Table 2, hierarchi- **Table 2: Push-T Performance Across Task Hori-** cal planning consistently outperforms DINO-WM **zons** . In each trial, a random start–goal pair _d_ steps as task difficulty increases. While the flat planapart is sampled from a validation trajectory. ner’s success rate drops sharply as the task horizon grows, the hierarchical planner remains subMethod _d_ = 25 _d_ = 50 _d_ = 75 stantially more robust at longer horizons. The GCIQL 40% 25% 7 _._ 5% performance gap is not explained by parameHIQL 55% 30% 20% ter count: capacity-matched flat planners do not HILP 25% 13% 0% match HWM and sometimes degrade with inDINO-WM 84% 55% 17% creased capacity (appendix D.1). Hierarchical DINO-WM (hier.) **89% 78% 61%** planning also exhibits a more favorable compute–performance trade-off, capable of achieving higher success rates while requiring 3 _×_ less compute per planning step compared to the flat planner (Fig. 5). These results highlight the advantage of planning over temporally abstract macro-actions, which reduces optimization complexity while 

**Table 2: Push-T Performance Across Task Horizons** . In each trial, a random start–goal pair _d_ steps apart is sampled from a validation trajectory. 

|Method|_d_= 25|_d_= 50|_d_= 75|
|---|---|---|---|
|GCIQL|40%|25%|7_._5%|
|HIQL|55%|30%|20%|
|HILP|25%|13%|0%|
|DINO-WM|84%|55%|17%|
|DINO-WM (hier.)|**89%**|**78%**|**61%**|


6 


**Figure 5: Success rate vs. test-time compute.** We vary the planning budget by sweeping CEM/MPPI samples and iterations (see appendix C). Hierarchical planning achieves higher success while using up to 3 _×_ less test-time compute than flat planners. **Left:** Push-T success rate vs. planning time ( _d_ = 50). **Right:** Diverse maze success rate vs. planning time ( _D ∈_ [9 _,_ 12]). 

preserving effective long-horizon control. Moreover, policy baselines (GCIQL, HIQL, HILP) performances drop sharply at longer horizons, suggesting limited robustness to long-horizon generalization without explicit planning. See Fig. 13 for examples of executions and subgoals. 

**Takeaway** : HWM improves long-horizon control while reducing inference-time compute. 

### **3.3 Diverse Maze** 

We instantiate HWM on top of PLDM [5] and evaluate it on Diverse Maze navigation, focusing on zero-shot generalization to larger, unseen layouts that require long-horizon planning. 

**Platform and Task.** We build on the MuJoCo PointMaze environment [26], using top-down RGB renderings as input. Maze layouts are randomly generated on a 10 _×_ 10 grid with connected free space; models are trained on 25 layouts and evaluated on 20 held-out layouts. Start and goal locations are sampled uniformly with grid-distance separation _D_ , defining easy ( _D ∈_ [5 _,_ 8]), medium ( _D ∈_ [9 _,_ 12]), and hard ( _D ∈_ [13 _,_ 16]) regimes. Dataset and training details are provided in appendix A.4. 

**Planning and Baselines.** Hierarchical planning uses MPPI at two temporal scales (details in appendix A.4). We compare against the flat PLDM planner, goal-conditioned RL baselines GCIQL and HIQL [15], and the zero-shot RL method HILP [16]. 

**Main Results.** As shown in Table 3, the performance gap between HWM and PLDM widens as task horizon increases. Even in settings where the flat planner performs reasonably well, it requires substantially higher test-time compute to match HWM performance (Fig. 5). In contrast, HWM achieves higher success with 4 _×_ less compute. Both single-level and hierarchical PLDM planners outperform goal-conditioned and zero-shot RL baselines on held-out layouts, highlighting the robustness of model-based planning to geometric distribution shift. See Fig. 10 for high-level plan visualizations. 

**Table 3: Diverse Maze Performance Across Task Horizons** . Agents are evaluated zero-shot on navigation tasks in held-out test maps. For each task, start and goal positions are randomly sampled such that their shortest-path distance is _D_ . 

|Method|_D∈_[5_,_8]|_D∈_[9_,_12]|_D∈_[13_,_16]|
|---|---|---|---|
|GCIQL|85%|40%|33%|
|HIQL|88%|73%|48%|
|HILP|48%|20%|10%|
|PLDM|100%|84%|44%|
|PLDM (hier.)|**100%**|**95%**|**83%**|


**Takeaway:** HWM consistently improves zero-shot planning across diverse latent world models. 

7 

### **3.4 Ablations and Analysis** 

**Do high-level world models improve longhorizon prediction?** A key challenge in longhorizon planning with learned world models is error accumulation, where small one-step errors compound over autoregressive rollouts. We hypothesize that longer-temporal-scale models improve long-horizon predictions by requiring fewer autoregressive steps. To test this, we condition low- and high-level world models trained on DROID on held-out initial observations and predict future states up to 2 seconds ahead, measuring _ℓ_ 1 error to the ground-truth future latent state. Predicting 2 seconds ahead requires up to 16 low-level autoregressive steps, whereas the high-level model produces a single-step prediction. As shown in Fig. 6, the low-level model is more accurate for short horizons ( _≤_ 1,s), while the high-level model achieves lower error for longer horizons ( _≥_ 1.5,s), supporting a hierarchy where high-level planning 


**Figure 6: Prediction error (** _L_ 1 **) as a function of prediction horizon.** For short horizons ( _≤_ 1 s), the low-level world model is more accurate. For longer horizons ( _≥_ 1.5 s), a single-step prediction from the high-level world model outperforms autoregressive rollouts of the low-level model, reflecting reduced error accumulation. 

provides long-term guidance and low-level planning handles short-term precision. 

**Table 4: Learned macro-actions versus alternative high-level action representations. (a)** Concatenated primitive actions: planning success rates on medium/hard Diverse Maze tasks. **(b)** Handcrafted delta-pose actions, which summarize each action sequence by its net end-effector displacement: alignment of the offline plan with expert behavior on Franka (mean _±_ SE), measured by cosine similarity and _ℓ_ 1 distance. 

**(a)** Concatenated actions: Diverse Maze. 

**(b)** Handcrafted actions: Franka. 

|Action|_D∈_[9_,_12]|_D∈_[13_,_16]|Action|Cos_↑_|_ℓ_1 _↓_|
|---|---|---|---|---|---|
|Concatenated|52%|37%|Delta pose|0_._80_±_0_._02|0_._088_±_0_._005|
|Macro-actions|**95%**|**83%**|<br>Macro-actions|**0**_._**88**_±_**0**_._**03**|**0**_._**080**_±_**0**_._**002**|


**Role of learned macro-actions.** A key question is how to parameterize macro-actions in the hierarchical world model. We compare learned latent macro-actions—obtained by encoding sequences of low-level actions—against concatenated primitive actions on Diverse Maze and hand-crafted net end-effector displacement (delta-pose) summaries on Franka. Learned macro-actions consistently outperform both. Compared to concatenating primitive actions, macro-actions achieve substantially higher planning performance (Table 4a) by compressing action sequences into a lower-dimensional space, reducing the high-level planning search complexity. On Franka, macro-actions also outperform delta-pose actions, producing offline plans that better align with expert trajectories (Table 4b). This is likely because delta-pose summaries collapse temporally extended, non-greedy trajectories into a single displacement, while macro-actions retain information needed to predict feasible transitions. 

## **4 Related Works** 

**World models and planning.** Learning predictive models of dynamics is a core idea in model-based RL [1, 2, 3, 27, 28], with recent work training latent dynamics from pixels for planning and policy optimization [29, 30, 31, 32]. Closely related to our setting, latent world models trained on rewardfree offline data via next-latent prediction generalize zero-shot to downstream control by simulating action outcomes optimizing costs [4, 5, 33, 7, 8, 34]. Long-horizon planning with such models is bottlenecked by compounding prediction errors [9, 10] and exponential search complexity [11]. A contemporary line of work instead couples video generation with action prediction in a single model 

8 

— sometimes called World Action Models — leveraging pretrained video diffusion backbones to inherit visuomotor priors [35, 36, 37, 38]; these methods learn an explicit policy, whereas latent world model planners like HWM learn only dynamics and perform zero-shot MPC at inference. 

**Hierarchical Control.** Hierarchical RL approaches use options, skills, or subgoal-conditioned policies for temporal abstraction [12, 13, 14, 15, 17, 18, 19], but require reward supervision and are limited to the training task distribution. Hierarchical MPC in optimal control [20, 21, 22] is task-agnostic but largely restricted to low-dimensional state or known dynamics. Table 5 summarizes the design axes of previous hierarchical model-based methods and how HWM differs from them. A complementary line of work focuses on unsupervised skill or subgoal discovery [39, 40, 41]. We view this as orthogonal: HWM uses random or fixed-stride waypoint sampling, and structured skill discovery could in principle replace this without changing the rest of the framework. 

**Table 5: Comparison of hierarchical model-based methods.** HWM is the only entry supporting zero-shot MPC directly from pixels, using world models pretrained via next-latent prediction, with predictions from coarser models serving as subgoals for finer-scale MPC via latent matching. 

|**Method**|**Zero-shot**|**Representation**|**Training**|**Hierarchical Interface**|
|---|---|---|---|---|
|**HWM (ours)**|✓|pixels_→_latent|Next-latent pred.|**Subgoal matching (latent)**|
|CAVIN [20]|✓|structured state|Learned dynamics|Subgoal matching (state)|
|LAT [21]|✓|structured state|Learned dynamics|Skill-conditioned policy|
|Safe HMPC [22]|_×_|structured state|Analytical dynamics|Reference tracking|
|IQL-TD-MPC [42]|_×_|state_→_latent|Offline RL + MPC|Goal-conditioned policy|
|Director,Puppeteer [14,19]|_×_|pixels_→_latent|l<br>Model-based RL|Goal-conditioned policy|
|THICK [17]|_×_|pixels_→_latent|MB-RL + reward|Subgoal matching (latent)|


## **5 Conclusion** 

We presented HWM, a hierarchical MPC framework for zero-shot planning with latent world models trained from offline trajectories. By learning dynamics at multiple temporal scales in a shared latent space, HWM lets high-level predictions serve as subgoals for short-horizon low-level planning, without hierarchical policies, task rewards, or manual decomposition. On a real Franka robot, this enables pick-and-place and multi-stage drawer manipulation from a single goal image, where the corresponding flat planner fails. Across all task settings, the same principle improves long-horizon success and reduces planning cost across multiple world-model backbones. These results suggest that hierarchy is a practical mechanism for extending latent world-model MPC beyond short, greedy behaviors. 

## **6 Limitations** 

Despite these gains, success rates degrade with task horizon for every method we evaluate; closing this gap will require further progress in world modeling and planning. First, HWM uses a single latent space across hierarchy levels: while this enables direct subgoal transfer, longer horizons and more open-ended environments may benefit from coarser, level-specific abstractions. Second, subgoal quality is shaped by choices at training and inference. At training time, we supervise the high-level world model with randomly sampled or fixed-stride waypoints; skill or subgoal discovery [39, 40, 41], or dynamic chunking [43], could replace this waypoint scheme without changing the rest of the framework, potentially yielding better subgoals. At inference time, incorporating feedback from the lower-level planner into high-level subgoal optimization may help compensate for the loss of detail in high-level predictions needed to guide precise low-level control. 

9 

## **References** 

- [1] R. S. Sutton. An adaptive network that constructs and uses and internal model of its world. _Cognition and Brain Theory_ , 4:217–246, 1981. 

- [2] M. Deisenroth and C. E. Rasmussen. Pilco: A model-based and data-efficient approach to policy search. In _Proceedings of the 28th International Conference on machine learning (ICML-11)_ , pages 465–472, 2011. 

- [3] D. Ha and J. Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2, 2018. 

- [4] M. Assran, A. Bardes, D. Fan, Q. Garrido, R. Howes, M. Muckley, A. Rizvi, C. Roberts, K. Sinha, A. Zholus, et al. V-jepa 2: Self-supervised video models enable understanding, prediction and planning. _arXiv preprint arXiv:2506.09985_ , 2025. 

- [5] V. Sobal, W. Zhang, K. Cho, R. Balestriero, T. G. Rudner, and Y. LeCun. Learning from reward-free offline data: A case for planning with latent dynamics models. _arXiv preprint arXiv:2502.14819_ , 2025. 

- [6] A. Bar, G. Zhou, D. Tran, T. Darrell, and Y. LeCun. Navigation world models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 15791–15801, 2025. 

- [7] G. Zhou, H. Pan, Y. LeCun, and L. Pinto. Dino-wm: World models on pre-trained visual features enable zero-shot planning. _arXiv preprint arXiv:2411.04983_ , 2024. 

- [8] R. G. Goswami, A. Bar, D. Fan, T.-Y. Yang, G. Zhou, P. Krishnamurthy, M. Rabbat, F. Khorrami, and Y. LeCun. World models can leverage human videos for dexterous manipulation. _arXiv preprint arXiv:2512.13644_ , 2025. 

- [9] E. Talvitie. Model regularization for stable sample rollouts. In _UAI_ , pages 780–789, 2014. 

- [10] M. Janner, J. Fu, M. Zhang, and S. Levine. When to trust your model: Model-based policy optimization. _Advances in neural information processing systems_ , 32, 2019. 

- [11] B. Ichter, P. Sermanet, and C. Lynch. Broadly-exploring, local-policy trees for long-horizon task planning. _arXiv preprint arXiv:2010.06491_ , 2020. 

- [12] R. S. Sutton, D. Precup, and S. Singh. Between mdps and semi-mdps: A framework for temporal abstraction in reinforcement learning. _Artificial intelligence_ , 112:181–211, 1999. 

- [13] P.-L. Bacon, J. Harb, and D. Precup. The option-critic architecture. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 31, 2017. 

- [14] D. Hafner, K.-H. Lee, I. Fischer, and P. Abbeel. Deep hierarchical planning from pixels. _Advances in Neural Information Processing Systems_ , 35:26091–26104, 2022. 

- [15] S. Park, D. Ghosh, B. Eysenbach, and S. Levine. Hiql: Offline goal-conditioned rl with latent states as actions. _Advances in Neural Information Processing Systems_ , 36:34866–34891, 2023. 

- [16] S. Park, T. Kreiman, and S. Levine. Foundation policies with hilbert representations. _arXiv preprint arXiv:2402.15567_ , 2024. 

- [17] C. Gumbsch, N. Sajid, G. Martius, and M. V. Butz. Learning hierarchical world models with adaptive temporal abstractions from discrete latent dynamics. In _The Twelfth International Conference on Learning Representations_ , 2023. 

- [18] R. Schiewer, A. Subramoney, and L. Wiskott. Exploring the limits of hierarchical world models in reinforcement learning. _Scientific Reports_ , 14:26856, 2024. 

- [19] N. Hansen, J. SV, V. Sobal, Y. LeCun, X. Wang, and H. Su. Hierarchical world models as visual whole-body humanoid controllers. _arXiv preprint arXiv:2405.18418_ , 2024. 

10 

- [20] K. Fang, Y. Zhu, A. Garg, S. Savarese, and L. Fei-Fei. Dynamics learning with cascaded variational inference for multi-step manipulation. _arXiv preprint arXiv:1910.13395_ , 2019. 

- [21] T. Li, R. Calandra, D. Pathak, Y. Tian, F. Meier, and A. Rai. Planning in learned latent action spaces for generalizable legged locomotion. _IEEE Robotics and Automation Letters_ , 6: 2682–2689, 2021. 

- [22] M. Kögel, M. Ibrahim, C. Kallies, and R. Findeisen. Safe hierarchical model predictive control and planning for autonomous systems. _International Journal of Robust and Nonlinear Control_ , 35:2658–2676, 2025. 

- [23] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 

- [24] V. Kumar, R. Shah, G. Zhou, V. Moens, V. Caggiano, A. Gupta, and A. Rajeswaran. Robohive: A unified framework for robot learning. _Advances in Neural Information Processing Systems_ , 36:44323–44340, 2023. 

- [25] I. Kostrikov, A. Nair, and S. Levine. Offline reinforcement learning with implicit q-learning. _arXiv preprint arXiv:2110.06169_ , 2021. 

- [26] E. Todorov, T. Erez, and Y. Tassa. Mujoco: A physics engine for model-based control. In _IROS_ , pages 5026–5033. IEEE, 2012. ISBN 978-1-4673-1737-5. URL `http://dblp.uni-trier. de/db/conf/iros/iros2012.html#TodorovET12` . 

- [27] D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

- [28] N. Hansen, H. Su, and X. Wang. Td-mpc2: Scalable, robust world models for continuous control. _arXiv preprint arXiv:2310.16828_ , 2023. 

- [29] F. Ebert, C. Finn, A. X. Lee, and S. Levine. Self-supervised visual planning with temporal skip connections. _CoRL_ , 12:23, 2017. 

- [30] D. Hafner, T. Lillicrap, I. Fischer, R. Villegas, D. Ha, H. Lee, and J. Davidson. Learning latent dynamics for planning from pixels. In _International conference on machine learning_ , pages 2555–2565. PMLR, 2019. 

- [31] M. Schwarzer, A. Anand, R. Goel, R. D. Hjelm, A. Courville, and P. Bachman. Data-efficient reinforcement learning with self-predictive representations. _arXiv preprint arXiv:2007.05929_ , 2020. 

- [32] M. Bagatella, M. Pirotta, A. Touati, A. Lazaric, and A. Tirinzoni. TD-JEPA: Latent-predictive representations for zero-shot reinforcement learning. In _The Fourteenth International Conference on Learning Representations_ , 2026. URL `https://openreview.net/forum?id= SzXDuBN8M1` . 

- [33] B. Terver, T.-Y. Yang, J. Ponce, A. Bardes, and Y. LeCun. What drives success in physical planning with joint-embedding predictive world models?, 2026. URL `https://arxiv.org/ abs/2512.24497` . 

- [34] L. Maes, Q. L. Lidec, D. Scieur, Y. LeCun, and R. Balestriero. Leworldmodel: Stable end-to-end joint-embedding predictive architecture from pixels. _arXiv preprint arXiv:2603.19312_ , 2026. 

- [35] Y. Hu, Y. Guo, P. Wang, X. Chen, Y.-J. Wang, J. Zhang, K. Sreenath, C. Lu, and J. Chen. Video prediction policy: A generalist robot policy with predictive visual representations. _arXiv preprint arXiv:2412.14803_ , 2024. 

11 

- [36] Y. Liao, P. Zhou, S. Huang, D. Yang, S. Chen, Y. Jiang, Y. Hu, J. Cai, S. Liu, J. Luo, et al. Genie envisioner: A unified world foundation platform for robotic manipulation. _arXiv preprint arXiv:2508.05635_ , 2025. 

- [37] S. Li, Y. Gao, D. Sadigh, and S. Song. Unified video action model. _arXiv preprint arXiv:2503.00200_ , 2025. 

- [38] S. Ye, Y. Ge, K. Zheng, S. Gao, S. Yu, G. Kurian, S. Indupuru, Y. L. Tan, C. Zhu, J. Xiang, et al. World action models are zero-shot policies. _arXiv preprint arXiv:2602.15922_ , 2026. 

- [39] J. Zhang, H. Yu, and W. Xu. Hierarchical reinforcement learning by discovering intrinsic options. _arXiv preprint arXiv:2101.06521_ , 2021. 

- [40] P. Mazzaglia, T. Verbelen, B. Dhoedt, A. Lacoste, and S. Rajeswar. Choreographer: Learning and adapting skills in imagination. _arXiv preprint arXiv:2211.13350_ , 2022. 

- [41] H. Zhang, M. Zhou, S. Zhai, Y. Sun, and H. Xiong. Efficient skill discovery via regret-aware optimization. _arXiv preprint arXiv:2506.21044_ , 2025. 

- [42] R. Chitnis, Y. Xu, B. Hashemi, L. Lehnert, U. Dogan, Z. Zhu, and O. Delalleau. Iql-td-mpc: Implicit q-learning for hierarchical model predictive control. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9154–9160. IEEE, 2024. 

- [43] S. Hwang, B. Wang, and A. Gu. Dynamic chunking for end-to-end hierarchical sequence modeling. _arXiv preprint arXiv:2507.07955_ , 2025. 

- [44] M. Oquab, T. Darcet, T. Moutakanni, H. Vo, M. Szafraniec, V. Khalidov, P. Fernandez, D. Haziza, F. Massa, A. El-Nouby, et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 

- [45] A. Bardes, J. Ponce, and Y. LeCun. Vicreg: Variance-invariance-covariance regularization for self-supervised learning. _arXiv preprint arXiv:2105.04906_ , 2021. 

- [46] R. Y. Rubinstein and D. P. Kroese. _The cross-entropy method: a unified approach to combinatorial optimization, Monte-Carlo simulation and machine learning_ . Springer Science & Business Media, 2004. 

- [47] G. Williams, N. Wagener, B. Goldfain, P. Drews, J. M. Rehg, B. Boots, and E. A. Theodorou. Information theoretic mpc for model-based reinforcement learning. In _2017 IEEE international conference on robotics and automation (ICRA)_ , pages 1714–1721. IEEE, 2017. 

- [48] K. Pertsch, K. Stachowicz, B. Ichter, D. Driess, S. Nair, Q. Vuong, O. Mees, C. Finn, and S. Levine. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- [49] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- [50] P. Atreya, K. Pertsch, T. Lee, M. J. Kim, A. Jain, A. Kuramshin, C. Eppner, C. Neary, E. Hu, F. Ramos, et al. Roboarena: Distributed real-world evaluation of generalist robot policies. In _Proceedings of the Conference on Robot Learning (CoRL 2025)_ , 2025. 

- [51] O. M. Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- [52] S. Park, K. Frans, B. Eysenbach, and S. Levine. Ogbench: Benchmarking offline goalconditioned rl. _arXiv preprint arXiv:2410.20092_ , 2024. 

12 

## **Appendix Contents** 

|**A **|**Training Details**|**14**|
|---|---|---|
||A.1<br>Low Level World Model<br>. . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>14|
||A.2<br>Franka Arm with Robotiq Gripper . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>14|
||A.3<br>Push-T . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>15|
||A.4<br>Diverse Maze . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>15|
|**B**|**Planning Details**|**16**|
|**C **|**Computational Analysis Details**|**18**|
||C.1<br>Push-T . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>18|
||C.2<br>Diverse Maze . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>18|
|**D **|**Additional Ablations and Analysis**|**19**|
||D.1<br>Model Size vs. Hierarchy . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>19|
||D.2<br>Strides for Fixed Interval Waypoints . . . . . . . . . . . . . . . . . .|. . . . . . .<br>19|
||D.3<br>Emergence of semantic subgoals . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>19|
|**E**|**Manual Subgoals: Isolating Planning from Representation**|**20**|
|**F**|**Visualizing World Model Predictions**|**21**|
|**G **|**Robot Task Definitions**|**22**|
|**H **|**Per-Configuration Trial Breakdown for Franka**|**23**|
|**I**|**Additional Execution Rollouts for Franka**|**24**|
|**J**|**Execution Rollout Examples for Push-T**|**25**|
|**K **|**Offline Planning Evaluation for Franka**|**25**|
|**L**|**Baselines**|**25**|
||L.1<br>Vision-Language-Action Models . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>25|
||L.2<br>Goal-Conditioned & Zero-Shot RL Methods . . . . . . . . . . . . . .|. . . . . . .<br>26|


13 

## **A Training Details** 

### **A.1 Low Level World Model** 

We train the low-level latent world model _Fθ_<sup>(1)</sup> to approximate the true transition dynamics _st_ +1 = _f_ ( _st, at_ ). Given a trajectory sequence _τ_ = ( _s_ 1 _, a_ 1 _, s_ 2 _, a_ 2 _, . . . , aT −_ 1 _, sT_ ), we first encode the states independently to obtain a sequence of latent features ( _zk_ ) _k∈_ [ _T_ ]. We feed the interleaved sequence of actions and latent features ( _ak, zk_ ) _k∈_ [ _T −_ 1] into the world model to obtain a sequence of next state representation predictions (ˆ _zk_ +1) _k∈_ [ _T −_ 1]. The teacher-forcing loss is computed as: 


To mitigate compounding prediction errors over multiple steps, we additionally compute a multistep autoregressive rollout loss. Let _Fθ_<sup>(1)</sup> ( _ak_ : _j_ ; _zk_ ) denote the predicted representation of _sj_ +1 obtained by autoregressively running the world model with actions _ak_ : _j_ , starting from _zk_ , where 1 _≤ k ≤ j ≤ T −_ 1. The multi-step rollout loss over up to _T −_ 1 prediction steps is: 


The overall training objective is given by a weighted sum of the two quantities: 


### **A.2 Franka Arm with Robotiq Gripper** 

**Data.** We use approximately 96 hours of unlabeled videos from the DROID dataset [23] and 30 hours from RoboSet [24]. Both datasets consist of short video clips of manipulation trajectories collected from real robots. Observations include RGB images and end-effector proprioception; actions correspond to end-effector delta poses. 

**State, Actions, and Preprocessing.** Videos are sampled at a spatial resolution of 256 _×_ 256 and with a frame rate uniformly sampled from (3 _,_ 10) FPS for DROID and (1 _,_ 5) FPS for RoboSet. At timestep _k_ , the state is defined as _sk_ = ( _xk, pk_ ), where _xk_ is the raw RGB observation and _pk ∈_ R<sup>7</sup> is the end-effector state expressed in the robot base frame. The first three dimensions of _pk_ correspond to Cartesian position, the next three correspond to orientation represented as extrinsic Euler angles, and the final dimension represents the gripper state. Actions are defined as differences in end-effector state between consecutive frames: _ak_ = _pk_ +1 _− pk_ . We apply random resize-and-crop augmentations to video clips, with the aspect ratio sampled uniformly from (0 _._ 75 _,_ 1 _._ 33). 

**Low Level World Model.** Following the setup of VJEPA2-AC [4], we sample fixed-length trajectories containing _T_ = 16 observation frames _{_ ( _pk, xk_ ) _}_<sup>16</sup> _k_ =1<sup>and 15 intervening actions</sup><sup>_{ak}_15</sup> _k_ =1<sup>.Each</sup> image _xk_ is encoded using the pretrained, frozen ViT-g/16 backbone, producing latent feature maps ( _zk_ )<sup>16</sup> _k_ =1<sup>.The world model is instantiated as a</sup><sup>_∼_300M-parameter ViT. It takes temporally interleaved</sup> sequences of latent features, end-effector states, and actions _{_ ( _zk, pk, ak_ ) _}_<sup>15</sup> _k_ =1<sup>andproduces15</sup> next-step latent predictions _{z_ ˆ _k}_<sup>16</sup> _k_ =2<sup>,withtargets</sup><sup>_z_2:16.WerefertotheVJEPA2paperforfull</sup> architectural details. 

**High-Level World Model.** To train the high-level world model, we sample variable-length trajectory segments _{_ ( _ak, pk, xk_ ) _}k∈T_ spanning (0 _._ 33 _,_ 4) seconds and select _N_ = 3 waypoint indices per segment, with the middle waypoint sampled uniformly. The high-level model shares the ViT architecture of the low-level model, but is conditioned on latent macro-actions rather than primitive actions. Conditioned on the current and previous waypoints and macro-actions, it is trained via teacher forcing to predict the next waypoint. Latent macro-actions are produced by a transformer-based action encoder _Aψ_ , whose CLS token is mapped to a macro-action by an MLP head. 

14 

**Table 6: Training hyperparameters for Droid + Roboset.** _γtf_ and _γroll_ denote the coefficients for teacherforcing and rollout losses, respectively, and context _T_ counts observation frames, including the initial frame. All other hyperparameters follow those used by VJEPA2-AC. 

|World Model|Epochs|Batch Size|_γtf_|_γroll_|context_T_|
|---|---|---|---|---|---|
|VJEPA2-AC (Low-Level)|200|256|1.0|1.0|16|
|VJEPA2-AC (High-Level)|120|768|1.0|0.0|3|


### **A.3 Push-T** 

**Data.** We use the offline dataset from DINO-WM, which consists of 18500 trajectories. Each trajectory consists of a sequence of ( _xt, at, pt_ ), where _xt_ is an RGB observation, _at_ is a 2D action vector, and _pt_ is the proprioceptive state denoting current agent position and velocity. 

**Low Level World Model.** We use DINO-WM [7] as our low-level world model. The encoder is a pretrained DINOv2 network [44], which is kept frozen during training. The world model is a 25M params ViT with causal masking. Training samples contain _T_ = 4 frames at stride 5, spanning 15 raw timesteps and providing three next-state targets _z_ 2:4. The action _ak_ is formed by concatenating the 5 primitive actions executed between _k_ and _k_ + 1, yielding a 5 _×_ 2 = 10–dimensional action vector. Each latent patch _zk_<sup>_i_attends only to corresponding earlier patches</sup><sup>_z_</sup> _j_<sup>_i_, 1</sup><sup>_≤j< k_, within the</sup> sample. Actions are first embedded using an MLP and then concatenated to each patch vector _zk_<sup>_i_.</sup> Proprioceptive inputs are incorporated using the same embedding and concatenation scheme. We refer to the original DINO-WM paper for full architectural details. 

**High-Level World Model.** To construct training sequences, we subsample trajectory segments with lengths uniformly drawn between 25 and 70 timesteps. From each segment, we sample _N_ = 5 waypoint states, which define the high-level transitions. The high-level world model is a scaled-up variant of the low-level world model (25M _→_ 75M parameters), obtained by increasing the number of layers from 6 to 10, the embedding dimension from 384 to 768, and the MLP dimension from 2048 to 3072, while reducing the number of attention heads from 16 to 12. This increased capacity enables more effective modeling of long-horizon dynamics. Latent macro-actions are produced by a transformer-based action encoder _Aψ_ , where the CLS token is passed through an MLP head to obtain the macro-action representation. See Table 7 for hyperparameters. 

**Table 7: Training hyperparameters for Push-T.** _γtf_ and _γroll_ denote the coefficients for teacher-forcing and rollout losses, respectively, and context _T_ counts frames including the initial observation. All other hyperparameters follow those used by DINO-WM on Push-T. 

|World Model|Epochs|Batch Size|_γtf_|_γroll_|context_T_|
|---|---|---|---|---|---|
|DINO-WM (Low-Level)|100|256|1.0|0.0|4|
|DINO-WM (High-Level)|500|128|1.0|0.0|5|


### **A.4 Diverse Maze** 

**Environment.** The environment is a variant of Mujoco PointMaze [26], which contains a point mass agent with a 4D state vector (global _x,_ global _y, vx, vy_ ), where _v_ is the agent velocity. The model receives a top down view of the maze rendered as (98 _,_ 98 _,_ 3) RGB image tensor as input, instead of relying on (global _x,_ global) directly. Mujoco PointMaze allows customizing the maze layout via a grid, where each cell is a wall or space. We opt for a 8 _×_ 8 grid (excluding outer wall). Maze layouts are generated randomly. Only the following constraints are enforced: 1) all the space cells are interconnected, 2) percentage of space cells range from 50% to 80%. 

**Data.** Each episode is initialized by placing the agent at a random ( _x, y_ ) location in the maze and sampling an initial velocity ( _vx, vy_ ). A trajectory is then generated by randomly sampling and executing actions for 100 steps, using an action repeat of 4. We collect 2,000 episodes per map and use 25 maps for training; resulting in a total of 5M transitions. 

15 

**Low Level World Model.** We train the low-level world model following the PLDM recipe [5], jointly learning the encoder and world model from scratch using offline trajectories. Each training sample consists of 15 observation frames and the 14 intervening actions subsampled from a trajectory. The observation sequence is encoded by a convolutional network into spatial latent features _z_ 1:15. Conditioned on the initial latent _z_ 1 and the action sequence _a_ 1:14, a convolutional world model autoregressively produces 14 future predictions _z_ ˆ2:15, excluding the initial state. To prevent representational collapse, we apply VICReg [45] to the latent features _z_ 1:15, following the original PLDM formulation. Refer to Table 8 for hyperparameters. We use the same PLDM architecture for Diverse Maze, comprising a lightweight convolutional encoder (33k params) and predictor (20k params); we refer to the original paper for full details. 

**High-Level World Model.** To construct training sequences, we sample trajectory segments spanning 60 timesteps and extract 7 waypoint states, including both endpoints, using a fixed stride of 10 timesteps. These define 6 high-level transitions. Primitive action chunks are encoded into an 8- dimensional macro-action via an MLP. We reuse the backbone of a pretrained low-level world model and keep it frozen, training only the high-level world model. The high-level model is a higher-capacity convolutional network, enabling long-horizon prediction. Conditioned on the initial waypoint latent _z_ 1 and the macro-action sequence _l_ 1:6, it autoregressively predicts the 6 subsequent waypoint latents. Hyperparameters are provided in Table 8. 

**Table 8: Training hyperparameters for Diverse Maze.** _α_ , _β_ , _λ_ , and _ω_ are parameters in the PLDM objective used to prevent representation collapse. _L_ proprio coef. denotes the coefficient on the proprioceptive prediction loss. _γtf_ and _γroll_ are the coefficients for teacher-forcing and rollout losses, and pred _T_ is the number of autoregressive prediction steps during training, excluding the initial state. For the high-level world model, we reuse the encoder trained at the low level and keep it frozen, eliminating additional representation learning. 

|World Model|Epochs|Batch Size|lr|_α_|_β_|_λ_|_ω_|_γtf_|_γroll_|pred_T_|_L_proprio|
|---|---|---|---|---|---|---|---|---|---|---|---|
|PLDM (Low-Level)|3|128|0.018|29.4|17.9|2.80|4.81|0.0|1.0|14|2.42|
|PLDM (High-Level)|5|128|0.018|–|–|–|–|0.0|1.0|6|1|


## **B Planning Details** 

For Franka and Push-T, we use the Cross-Entropy Method (CEM) [46] for trajectory optimization in continuous action spaces. At each planning step, CEM maintains a factorized Gaussian over action sequences, iteratively sampling trajectories, evaluating them with the world model, and refitting to elite samples by updating the mean and variance. To improve stability and avoid premature collapse, variance updates are smoothed with an exponential moving average. After a fixed number of iterations, the optimized mean action sequence is executed, and planning proceeds in a receding-horizon manner. See Table 9 and Table 10 for the single-level and hierarchical planner parameters, respectively. 

**Macro-action search distribution.** The low-level planner optimizes primitive actions, whose scale is fixed by the environment, and is initialized with zero mean and unit variance. Macro-actions, in contrast, live in a learned latent space whose scale and support are set by the action encoder _Aψ_ . We therefore record the macro-actions produced by _Aψ_ during training in a fixed-size FIFO buffer holding the most recent _N_ = 4096 of them, stored alongside the model weights so that planning requires no access to the training data. At plan time we compute the per-dimension mean and standard deviation over this buffer and use them to initialize the high-level Gaussian, and we clip sampled macro-actions to the per-dimension 2% and 98% quantiles at every CEM iteration. This keeps high-level search within the latent-action region where _Fϕ_<sup>(2)</sup> was trained, without additional tuning. 

**Planning horizon schedules.** We measure elapsed time _t_ , execution budget _B_ , and replanning interval _k_ in low-level prediction steps. A replanning interval of _k_ means executing actions for the first _k_ low-level predictions before replanning. Each low-level prediction step spans five environment steps on Push-T and one environment step on Diverse Maze. At each replanning step, the standalone 

16 

single-level planner caps its prediction horizon by the remaining budget: 


where _h_ is the maximum prediction horizon reported in Tables 9 and 11 and _ht_ is the horizon used at replanning time _t_ . In hierarchical planning, the low-level planner uses a fixed horizon _h_ to reach the next subgoal. The high-level horizon starts at _H_ and decreases by one whenever _h_ low-level steps have elapsed, subject to a minimum: 


Here, _h_ and _H_ are the prediction horizons reported in Tables 10 and 12, while _ht_ and _Ht_ denote the horizons used at replanning time _t_ . We use _H_ min = 1 for Push-T and _H_ min = 3 for Diverse Maze. 

**Table 9:** Single-level CEM planning hyperparameters for Franka and Push-T. 

||_k_|_B_|# elites|# iters|# samples|Var EMA|_h_|
|---|---|---|---|---|---|---|---|
|Franka|1|–|20|15|2400|0.75|6|
|Push-T (_d_= 25)|5|10|30|30|300|0|5|
|Push-T (_d_= 50)|5|20|10|30|1200|0.9|10|
|Push-T (_d_= 75)|5|25|20|20|1000|0|15|


**Table 10:** Hierarchical CEM planning hyperparameters for Franka and Push-T. 

||||High|-level plan|ner|||Low-|level plan|ner|
|---|---|---|---|---|---|---|---|---|---|---|
|_k_|_B_|# elites|# iters|# samples|Var EMA|_H_|# elites|# iters|# samples|Var EMA _h_|
|Franka<br>1|–|22|15|3000|0.65|2|12|5|800|0.25<br>2|
|Push-T(_d_= 25) 5|10|10|20|900|0|2|10|30|300|0<br>5|
|Push-T(_d_= 50) 5|20|10|40|1500|0.9|4|10|20|900|0.8<br>5|
|Push-T(_d_= 75) 5|25|10|20|1200|0.9|5|10|20|1200|0.8<br>5|


**Table 11:** Single-level MPPI planning hyperparameters for Diverse Maze. 

||_k_|_B_|noise_σ_|# samples|_λ_|_h_|
|---|---|---|---|---|---|---|
|Maze (_D ∈_[5_,_8])|4|500|5|125|0.0025|150|
|Maze (_D ∈_[9_,_12])|4|500|5|250|0.0025|200|
|Maze (_D ∈_[13_,_16])|4|500|5|250|0.0025|250|


**Table 12:** Hierarchical MPPI planning hyperparameters for Diverse Maze. 

|||||High-level p|lanner||L|ow-level|planner||
|---|---|---|---|---|---|---|---|---|---|---|
||_k_|_B_|noise_σ_|# samples|_λ_|_H_|noise_σ_|# sample|s<br>_λ_|_h_|
|Maze (_D ∈_[5_,_8])|4|265|10|2000|0.0025|25|5|500|0.0025|10|
|Maze (_D ∈_[9_,_12])|4|365|10|2000|0.0025|35|5|500|0.0025|10|
|Maze (_D ∈_[13_,_16])|4|485|10|4000|0.0025|47|5|1000|0.0025|10|


For Diverse Maze, we use Model Predictive Path Integral (MPPI) [47] for planning. MPPI updates a nominal action sequence by importance-weighting sampled trajectories using exponential costs; unlike CEM, it applies soft weights over all samples, yielding smoother updates without hard elite selection. We use the MPPI implementation from PLDM [5]. See Table 11 and Table 12 for the single-level and hierarchical planner hyperparameters, respectively. 

In Diverse Maze’s hierarchical planning setup, the hierarchical planner is called at each replanning step during the first _hH_ steps. For the final 15 steps, we use only the low-level planner, which plans directly toward the goal with a fixed prediction horizon of 50. 

17 

## **C Computational Analysis Details** 

### **C.1 Push-T** 


**Figure 7:** Success rate as a function of test-time compute for Push-T. **Left** : Setting _d_ = 50. **Right** : Setting _d_ = 75. 

For the compute scaling analysis of Fig. 5 and Fig. 7, we performed a grid search over the key CEM hyperparameters of both high-level and low-level planners. 

For _d_ = 50 in Fig. 5, for the high level planner, we swept #samples _∈_ [150 _,_ 300 _,_ 600 _,_ 900 _,_ 1200 _,_ 1500], #iters _∈_ [10 _,_ 20 _,_ 30 _,_ 40], and Var EMA _∈_ [0 _._ 4 _,_ 0 _._ 7 _,_ 0 _._ 9]. For the low-level planner (both when used standalone and as the low-level planner in the hierarchical setting), we swept #samples _∈_ [150 _,_ 300 _,_ 600 _,_ 900 _,_ 1200], #iters _∈_ [10 _,_ 20 _,_ 30 _,_ 40], and Var EMA _∈_ [0 _,_ 0 _._ 4 _,_ 0 _._ 7 _,_ 0 _._ 8 _,_ 0 _._ 9]. 

For _d_ = 75, for the high-level planner, we swept the number of samples #samples _∈_ [150 _,_ 300 _,_ 600 _,_ 900 _,_ 1200 _,_ 1500], the number of CEM iterations #iters _∈_ [10 _,_ 20 _,_ 30 _,_ 40], and the standard deviation momentum coefficient Var EMA _∈_ [0 _._ 4 _,_ 0 _._ 7 _,_ 0 _._ 9]. For the low-level planner, we swept #samples _∈_ [150 _,_ 300 _,_ 600 _,_ 900 _,_ 1000 _,_ 1100 _,_ 1200 _,_ 1500], #iters _∈_ [10 _,_ 20 _,_ 25 _,_ 30 _,_ 35 _,_ 40], and Var EMA _∈_ [0 _,_ 0 _._ 4 _,_ 0 _._ 5 _,_ 0 _._ 7 _,_ 0 _._ 8 _,_ 0 _._ 9 _,_ 0 _._ 95]. 

This sweep over CEM hyperparameters enables constructing Pareto frontiers that characterize the trade-off between planning compute (mean time per plan) and task success rate. 

### **C.2 Diverse Maze** 


**Figure 8:** Success rate as a function of test-time compute for Diverse Maze. **Left** : Setting _D ∈_ [9 _,_ 12]. **Right** : Setting _D ∈_ [13 _,_ 16]. 

For the compute scaling analysis of the Diverse Maze environment in Fig. 5 and 8, we performed a grid search over the number of samples and horizon of planning in the MPPI algorithm. We perform the same sweep for all 3 difficulty settings. 

For the flat baseline, we swept the number of samples #samples _∈_ [70 _,_ 125 _,_ 250 _,_ 500 _,_ 1000 _,_ 2000 _,_ 4000] and the horizon _∈_ [100 _,_ 125 _,_ 150 _,_ 175 _,_ 200 _,_ 225 _,_ 250 _,_ 275]. 

18 

For the hierarchical planner, we have a low-level planner and a high-level planner, each of which has a number of samples. We swept the number of samples of the low-level planner #samples _∈_ [70 _,_ 125 _,_ 250 _,_ 500 _,_ 1000 _,_ 2000 _,_ 4000], the number of samples of the high-level planner #samples _∈_ [70 _,_ 125 _,_ 250 _,_ 500 _,_ 1000 _,_ 2000 _,_ 4000] and the horizon of the high-level planner _H ∈_ [25 _,_ 35 _,_ 45]. This comprehensive sweep over MPPI hyperparameters enables the construction of Pareto frontiers that characterize the trade-off between planning compute time and the success rate. 

## **D Additional Ablations and Analysis** 

### **D.1 Model Size vs. Hierarchy** 

One question is whether the gains from hierarchical planning arise from compositional structure at planning time, or simply from increased model capacity. To disentangle these effects, we compare hierarchical models against flat world models with matched or larger parameter counts. As shown in Table 13, increasing the capacity of flat models does not improve performance—in fact, it often degrades it—while hierarchical models consistently achieve higher success rates across both tasks. This suggests that the gains stem from hierarchical composition rather than model size alone. 

**Table 13:** Capacity-controlled comparison between flat and hierarchical world models. Flat models with comparable or larger parameter counts fail to match hierarchical performance, and sometimes degrade with increased capacity. In contrast, hierarchical models consistently outperform flat baselines on Push-T and Diverse Maze, indicating that gains arise from hierarchical structure rather than model capacity. 

|**(a)**|Push-T|||**(**|**b)**Divers|e Maze||
|---|---|---|---|---|---|---|---|
|Method|Params|_d_=50|_d_=75|Method|Params|_D∈_[9_,_12]|_D∈_[13_,_16]|
|DINO-WM (flat)<br>l|44M|55%|17%|PLDM (flat)<br>l|54k|85%|63%|
|DINO-WM (flat)|98M|35%|15%|PLDM (flat)|178k|82%|59%|
|DINO-WM (hierarchy)|94M|**78%**|**61%**|PLDM (hierarchy)|182k|**95%**|**83%**|


### **D.2 Strides for Fixed Interval Waypoints** 

For Diverse Maze, the high-level world model is trained using fixed temporal strides between successive latent waypoints. We evaluate the sensitivity of hierarchical planning performance to this stride by varying it across a range of values. As shown in Table 14, performance improves as the stride increases from 6 to 12 timesteps, suggesting that moderate temporal abstraction is beneficial for long-horizon planning. However, performance slightly degrades at larger strides, indicating a trade-off between abstraction and predictive fidelity. Overall, the results demonstrate that hierarchical planning is robust to the choice of stride, with strong performance across a broad range of values. 

**Table 14:** Sensitivity of hierarchical planning performance to the high-level temporal stride on Diverse Maze. 

|High-level stride|6|8|10|12|14|
|---|---|---|---|---|---|
|Success Rate (_D∈_[13_,_16])|50%|55%|77%|78%|75%|


### **D.3 Emergence of semantic subgoals** 

Effective hierarchical planning requires subgoals on a feasible path to the final goal that are reachable by the low-level planner. High-level plans therefore fall into three categories: invalid plans, valid plans with unreachable subgoals, and valid plans with reachable subgoals. 

As shown in Fig. 9, when the macro-action space has sufficient capacity ( _≥_ 4 dimensions), the highlevel planner typically produces valid plans. However, these subgoals are not always reachable by the low-level planner, as they may require non-greedy action sequences. Restricting the latent-action 

19 


**Figure 9: Effect of macro-action dimension on hierarchical planning. Left:** Performance as a function of macro-action dimension _d_ . When the latent space has very low capacity, the high-level planner fails to produce valid plans. As _d_ increases, success improves; however, beyond a moderate dimensionality, proposed subgoals become harder for the low-level planner to execute, as indicated by a drop in action cosine similarity to expert behavior. **Right:** Qualitative rollouts illustrating this trade-off. Moderate latent dimensionality biases the planner toward reachable, greedy subgoals, yielding the best overall performance. 

dimensionality biases the planner toward proposing subgoals that are achievable with greedy behavior. This suggests an optimal regime in which the latent space is expressive enough to encode useful trajectories, but not so expressive that it enables subgoals requiring complex non-greedy execution. Empirically, a macro-action dimension of 4 strikes this balance for the Franka tasks. 

Notably, reconstruction fidelity is not tightly correlated with latent-action dimensionality. Lowerdimensional latent spaces yield noisier predictions, reflected in higher _ℓ_ 1 error and blurrier reconstructions (Fig. 9), as expected under stronger compression. Nevertheless, these predictions often preserve coarse semantic structure, such as contact events or motion direction, which is sufficient for hierarchical planning despite reduced visual precision. 

## **E Manual Subgoals: Isolating Planning from Representation** 

The flat VJEPA2-AC planner fails entirely on end-to-end pick-&-place (Table 1), but this aggregate failure conflates two possible causes: the flat planner may lack the ability to accurately predict the consequences of the required actions, or single-level MPC may be unable to escape the greedyshortcut traps under a non-greedy goal matching objective (Section 1). This appendix disentangles the two by supplying the flat planner with manually-defined intermediate subgoals. 

**Setup.** For each of the 10 pick-&-place configurations per object, we manually prepare an intermediate grasp-point subgoal image. The flat VJEPA2-AC planner is run in two sequential phases: first reaching the subgoal, then reaching the final goal. Octo is evaluated under the same image-subgoal supervision; _π_ 0-FAST-DROID and _π_ 0 _._ 5-DROID are conditioned on language goals and cannot consume image subgoals in the same way, so we omit them from this comparison. 

**Results.** Table 15 reports pick-&-place results with and without manual subgoals. With manual subgoals, the flat VJEPA2-AC planner reaches 80%/80% on pick-&-place cup/box — comparable to HWM under the same supervision (also 80%/80%) and far above its 0%/0% without subgoals. The VJEPA2-AC world model is therefore competent on these tasks given the right intermediate targets; the failure of single-level planning is hierarchical in nature, not representational. HWM 

**Table 15: Manual subgoals on Franka.** Success rates (%) over 50 trials per object (10 configurations, 5 per configuration). 

|Planner|Subgoal|Cup|Box|
|---|---|---|---|
|VJEPA2-AC|None|0%|0%|
|HWM|Predicted|70%|60%|
|VJEPA2-AC|Manual|80%|80%|
|HWM|Manual|80%|80%|
|Octo|Manual|20%|10%|


recovers most of this oracle performance automatically (70%/60% from a single goal image), confirming that its contribution is to produce reachable subgoals without manual annotation. Octo, despite 

20 

receiving the same subgoals, achieves only 20%/10%, indicating that subgoal supervision alone does not close the gap — the underlying dynamics model must also support precise control. 

## **F Visualizing World Model Predictions** 

**Franka Arm with Robotiq Gripper.** To reconstruct RGB images from latent representations, we train on DROID a ViT decoder that maps the frozen V-JEPA 2 encoder features back to pixel space. The decoder takes as input the encoded features of dimension 1408 (matching the V-JEPA 2 ViT-Giant encoder output) and projects them to an intermediate dimension of 1024 via a linear layer. The architecture consists of 12 transformer blocks, each with 32 attention heads and an MLP ratio of 4, using GELU activations, LayerNorm and sinusoidal 2D positional embeddings. The decoder operates on a 32 _×_ 32 grid of spatial tokens (corresponding to patch size 8 for 256 _×_ 256 images). The model is trained using an _L_ 1 reconstruction loss on normalized pixel values. We train the decoder for 100 epochs on the DROID dataset using the AdamW optimizer with a peak learning rate of 5 _×_ 10<sup>_−_4</sup> , linear warmup over 2 epochs, cosine decay to 10<sup>_−_6</sup> , and weight decay of 0 _._ 1. Training is performed on 8 nodes with a total batch size of 512. 

**Push-T.** Similarly as for the DROID decoder depicted above, we train a ViT decoder that maps the frozen DINOv2 ViT-S/14 encoder features back to pixel space on the Push-T dataset. The decoder is a ViT-Base of intermediate dimension of 768 with 12 transformer blocks, each with 16 attention heads. It operates on a 28 _×_ 28 grid of spatial tokens (corresponding to patch size 8 for 224 _×_ 224 images). The model is trained using an _L_ 2 reconstruction loss on normalized pixel values for 40 epochs on the PushT dataset with a total batch size of 256. 

**Diverse Maze.** To visualize predictions and plans, we train a lightweight convolutional prober that takes as input a spatial representation of shape ( _H, W, C_ ). The prober consists of two convolution–pooling stages followed by a fully connected layer, and outputs 2-D coordinates corresponding to the agent’s ( _x, y_ ) location. We show visualizations of successful high-level plans in Fig. 10. 


**Figure 10: High-level plans in Diverse Maze.** The agent is shown as a green ball and the goal as a yellow star. The pink trajectory is generated by the high-level planner, while the teal trajectory is generated by the flat planner. In these trials, the high-level planner successfully produces a sequence of subgoals that lead to the goal, whereas the flat planner often struggles due to the increased search complexity of long-horizon prediction. 

21 

## **G Robot Task Definitions** 

Fig. 11 depicts the initial and goal states defining the evaluation episodes for the Pick-&-Place Cup and Drawer tasks. We omit the Pick-&-Place Box tasks, which use identical start and goal configurations and differ only in the grasped object (a box rather than a cup). 


**Figure 11:** Initial and goal states for all evaluation tasks. **(a) Drawer Tasks:** 7 subtasks involving opening and closing drawers at various positions. **(b) Pick-&-Place Cup Tasks:** 10 subtasks requiring the robot to pick up a cup and place it at different target locations. Each panel shows the initial state (left) and goal state (right) for a given task. 

22 

## **H Per-Configuration Trial Breakdown for Franka** 

We run _N_ = 5 independent trials per (start, goal) configuration for both VJEPA2-AC and HWM on all pick-&-place and drawer tasks, yielding 50 total trials per object on pick-&-place and 35 on drawer. Aggregate success rates are reported in Table 1; per-configuration breakdowns and 95% Clopper–Pearson confidence intervals are in Table 16. 

Per-configuration outcomes are highly consistent. For VJEPA2-AC, every configuration is fully deterministic (5/5 identical outcomes across all 27 configurations, 135 _/_ 135 trials). For HWM, 21 _/_ 27 configurations are fully deterministic, and the remaining 6 reproduce the modal outcome in 4 _/_ 5 trials (129 _/_ 135 = 95 _._ 6% of trials match modal). Aggregate success rates therefore reflect per-configuration task difficulty rather than execution stochasticity. 

**Table 16:** Per-configuration success counts (successes / trials) on Franka, with 95% Clopper–Pearson confidence intervals on aggregate rates. Configurations correspond to the start–goal pairs visualized in appendix G. 

||**(a)**Pick-&-Plac|e Cup||**(b)**Pick-&-Plac|e Box|
|---|---|---|---|---|---|
|Config|VJEPA2-AC|HWM (ours)|Config|VJEPA2-AC|HWM (ours)|
|PnP 0|0/5|0/5|PnP 0|0/5|0/5|
|PnP 1|0/5|5/5|PnP 1|0/5|1/5|
|PnP 2|0/5|5/5|PnP 2|0/5|4/5|
|PnP 3|0/5|5/5|PnP 3|0/5|5/5|
|PnP 4|0/5|5/5|PnP 4|0/5|5/5|
|PnP 5|0/5|4/5|PnP 5|0/5|4/5|
|PnP 6|0/5|1/5|PnP 6|0/5|1/5|
|PnP 7|0/5|5/5|PnP 7|0/5|5/5|
|PnP 8|0/5|0/5|PnP 8|0/5|0/5|
|PnP 9|0/5|5/5|PnP 9|0/5|5/5|
|Total|0/50|35/50|Total|0/50|30/50|
|95% CI|[0.0, 7.1]|[55.4, 82.1]|95% CI|[0.0, 7.1]|[45.2, 73.6]|


**(c)** Drawer (opening and closing) 

|Config|Open 0|Open 1|Open 3|Close 0|Close 1|Close 2|Close 4|Total|95% CI|
|---|---|---|---|---|---|---|---|---|---|
|VJEPA2-AC|5/5|0/5|0/5|5/5|0/5|0/5|0/5|10/35|[14.6, 46.3]|
|HWM (ours)|5/5|5/5|0/5|5/5|5/5|5/5|0/5|25/35|[53.7, 85.4]|


23 

## **I Additional Execution Rollouts for Franka** 


**Figure 12:** Executions on pick-&-place and drawer manipulation with a dual-gripper Franka arm. Dotted red columns indicate subgoals inferred by the high-level planner and decoded for visualization. Rows representing failed episodes are labeled with "Failure". Additional execution videos can be found in `https://kevinghst. github.io/HWM/` . 

24 

## **J Execution Rollout Examples for Push-T** 

|t=0<br>t=3|t=6|Subgoal 1|<br>t=9<br>t=12|t=15|Subgoal 2|<br>t=18|t=21<br>t=24|Goal|
|---|---|---|---|---|---|---|---|---|


**Figure 13:** Executions on Push-T task. Dotted red columns indicate subgoals inferred by the high-level planner and decoded for visualization. 

## **K Offline Planning Evaluation for Franka** 

Since planning on a real robot is time-consuming and not parallelizable, we introduce a quantitative offline planning evaluation that enables faster iteration over model variants and planning hyperparameters. We evaluate on the same 10 pick-&-place tasks used in the interactive experiments, with manually defined subgoals corresponding to the grasp point. Expert actions are defined as the robot’s delta pose from the initial observation to the subgoal, ˜ _a_ 1, and from the subgoal to the goal, _a_ ˜2. Conditioned on the initial and goal observations, the hierarchical planner produces a sequence of subgoals along with a sequence of primitive actions ( _a_<sup>_∗_</sup> 1: _h_<sup>) toward the first subgoal.To assess</sup> high-level planning quality, we compare the aggregate inferred action<sup>�</sup><sup>_h_</sup> _i_ =1<sup>_a_</sup> _i_<sup>_∗_with the expert action</sup> _a_ ˜1 using cosine similarity and _ℓ_ 1 distance. High cosine similarity or low _ℓ_ 1 distance indicates that the planner has identified a plan that moves toward the non-greedy subgoal, which strongly correlates with real-world task success. 

## **L Baselines** 

### **L.1 Vision-Language-Action Models** 

For our baselines, we reproduce the same setup as in the Droid platform. Specifically, we use a Franka Panda arm with a bi-finger Robotiq gripper, dual camera setup (one wrist camera plus one side camera looking at the robot from the left). Our wrist camera setup is identical to Droid (the same mount and model - ZED Mini), however, for the side camera, we use Intel RealSense. While RealSense has a different aspect ratio (4:3 instead of ZED Mini’s 16:9) we found that simply padding the side image to get 16:9 aspect ratio yields good success rate for VLAs trained on Droid with this aspect ratio. Note that we use the same RealSense side camera for all baselines and world model-based agents therefore, they all have access to the same amount of sensor signal from the side view. In fact, the _π_ - family of models receive extra sensor information since they have access to wrist camera which is not used by Octo and world model-based agents. 

_π_ **0-FAST-DROID and** _π_ **0** _._ **5-DROID** [48, 49]. For a reliable control with the _πx_ -DROID models family, we reproduce the same controller on our Franka as in the Droid benchmark. Both models use one side camera and one wrist camera and output chunks of actions being joint velocities and target gripper positions. For both models, we execute the entire chunk of outputted actions before requerying the policy (15 actions for _π_ 0 _._ 5 and 8 actions for _π_ 0-FAST). We run both policies for 300 total actions as we found this to be enough for a successfull task attempt with a big space for suboptimality. We do not finetune these policies, therefore, the evaluation is zero-shot and out-of-distribution since they are only finetuned on Droid so our scene is new to both of them. 

Since _π_ - models use text goal specification, we tuned text prompts to achieve the highest success rate. We arrived at the same conclusions as in the RoboArena [50] benchmark, specifically, _π_ - models do not understand colors and complex nouns for shapes (e.g. platform, shelf etc) and each prompt has to be written in a short and a simple way. Below are the prompts we tried (either “cup” or only “box” is present in the prompt): 

25 

1. “put the cup on the plane” 

2. “put the cup (box) on the platform” 

3. “put the cup (box) on the table” – the model was picking the object up and putting it on the the same position since the “ground level” surface is a table despite a small table was in front of it (See Figure 11). 

4. “put the cup (box) on the yellow table” – same as 2. 

5. “put the cup on the wooden table” – same as 2. 

6. “put the cup on the shelf” – the policy tried to place the object on the shelf in the background. 

7. “put the cup on the plate” – this prompt worked. Since it requires a plate, we started to use the one as the marker for the goal position for the object placement. _We believe makes language goals a good substitution for image goals as the plate position unambiguously informs the model where the object should be placed and the plate is present in many training episodes._ 

We run _π_ 0 _._ 5-DROID for 100 trials for the pick-&-place task with the cup and the pick-&-place task with the box. We use the same 10 task configurations as the ones present in Figure 11 to ensure fair comparison. This means we run 10 trials for each configuration which gives a low variance for the policy with highly stochastic outputs. Similarly, we run 100 trials for the pick-&-place task with the cup and 50 trials for the pick-&-place task with the box (i.e. 5 trials per configuration). 

Similarly to the evaluation of the world models and policies, we use binary success rate for evaluations. In particular, we simply give the policy a score of 1 if the object was placed in the target position and zero otherwise. Unfortunately, we were unable to run drawer tasks with _π_ - models because during our evaluation of the drawer task with Octo, the drawer was physically destroyed by the robot into a non-operating state. Note that because of language goals (which can only be primitive), _π_ - models cannot run the task with subgoals. 

**Octo** [51]. We use the same setup for octo as in the V-JEPA 2 paper. Specifically, we use the Octo-base policy finetuned on Droid with image goals. We used the same scoring as for the _π_ - models. Note that Octo is not able to work well without subgoals so we found it performance without subgoals to be 0. 

### **L.2 Goal-Conditioned & Zero-Shot RL Methods** 

**Table 17: Hyperparameters.** Hyperparameters used for GCIQL, HIQL, and HILP on the Push-T and Diverse Maze tasks. 

|||GCIQL|||H|IQL||H|ILP|
|---|---|---|---|---|---|---|---|---|---|
||lr|expectile|rand goal_p_|lr|expectile|rand goal_p_|alpha|lr|expectile|
|Push-T(_d_= 25)|3e_−_5|0.6|0.0|3e_−_5|0.9|0.0|3.0|3e_−_5|0.6|
|Push-T(_d_= 50)|3e_−_5|0.6|0.3|3e_−_5|0.9|0.3|1.0|3e_−_5|0.6|
|Push-T(_d_= 75)|3e_−_5|0.9|0.6|3e_−_5|0.9|0.3|1.0|3e_−_5|0.6|
|Maze(_D ∈_[5_,_8])|3e_−_5|0.8|0.0|3e_−_5|0.6|0.3|1.0|3e_−_5|0.9|
|Maze(_D ∈_[9_,_12])|3e_−_5|0.6|0.3|3e_−_5|0.8|0.6|3.0|3e_−_5|0.9|
|Maze(_D ∈_[13_,_16])|1e_−_4|0.6|0.0|3e_−_5|0.8|0.6|3.0|3e_−_5|0.9|


**GCIQL** [15] – goal-conditioned version of Implicit Q-Learning [25], a strong and widely-used method for offline RL. 

**HIQL** [15] – a hierarchical GCRL method which trains two policies: one to generate subgoals, and another one to reach the subgoals. Notably, both policies use the same value function. **HILP** [16] – a method that learns state representations from the offline data such that the distance in the learned representation space is proportional to the number of steps between two states. A 

26 

direction-conditioned policy is then learned to be able to move along any specified direction in the latent space. 

For GCIQL and HIQL, we use the implementations from the repository<sup>1</sup> of OGBench [52]. Likewise, for HILP we use the official implementation<sup>2</sup> from its authors. For Push-T and Diverse Maze, we tune hyperparameters independently for each difficulty setting and report results using the optimal configurations. The selected hyperparameters are reported in Table 17; all other hyperparameters not listed in the table use the default values from the original repositories. 

> 1https://github.com/seohongpark/ogbench 

> 2https://github.com/seohongpark/HILP 

27 

