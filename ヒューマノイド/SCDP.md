---
title: "SCDP: Learning Humanoid Locomotion from Partial Observations via Mixed-Observation Distillation"
date: "2026-03-10"
authors: "Milo Carroll; Tianhu Peng; Lingfan Bao; Chengxu Zhou; Zhibin Li"
url: https://arxiv.org/abs/2603.09574
pdf: https://arxiv.org/pdf/2603.09574
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.09574)** / [論文ページ](https://arxiv.org/abs/2603.09574)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **SCDP: Learning Humanoid Locomotion from Partial Observations via Mixed-Observation Distillation** 

Milo Carroll, Tianhu Peng, Lingfan Bao, Chengxu Zhou and Zhibin Li Department of Computer Science, University College London 

_{_ milo.carroll.23, tianhu.peng.24, lingfan.bao.24, chengxu.zhou, alex.li _}_ @ucl.ac.uk 

**_Abstract_ — Distilling humanoid locomotion control from offline datasets into deployable policies remains a challenge, as existing methods rely on privileged full-body states that require complex and often unreliable state estimation. We present Sensor-Conditioned Diffusion Policies (SCDP) that enables humanoid locomotion using only onboard sensors, eliminating the need for explicit state estimation. SCDP decouples sensing from supervision through mixed-observation training: diffusion model conditions on sensor histories while being supervised to predict privileged future state–action trajectories, enforcing the model to infer the motion dynamics under partial observability. We further develop restricted denoising, context distribution alignment, and context-aware attention masking to encourage implicit state estimation within the model and to prevent train–deploy mismatch. We validate SCDP on velocitycommanded locomotion and motion reference tracking tasks. In simulation, SCDP achieves near-perfect success on velocity control (99–100%) and 93% tracking success in AMASS test set, performing comparable to privileged baselines while using only onboard sensors. Finally, we deploy the trained policy on a real G1 humanoid at 50 Hz, demonstrating robust real robot locomotion without external sensing or state estimation.** 

## I. INTRODUCTION 

Humanoid robot control has advanced rapidly in recent years, progressing from task-specific reinforcement learning controllers [1]–[3] to motion reference tracking methods [4]– [7]. These approaches enable diverse whole-body behaviors and have supported applications such as real-time teleoperation and multi-skill locomotion in both graphics [8] and robotics [5], [6], [9]–[11]. The ability to reproduce large skillets within a single controller is essential for adaptive behaviors, as demonstrated by multi-expert learning that synthesizes adaptive locomotion by combining different motor skills to handle varying task conditions [12]. 

Recently, diffusion models have become promising for learning more expressive control by modeling full distributions of expert behavior rather than deterministic action mappings [13]–[15]. Their flexibility offers task adaptation via direct conditioning or classifier guidance [16], [17]. In robotics, diffusion-based policies have demonstrated strong performance in visuomotor manipulation [18], bipedal locomotion [19], [20], and physics-based humanoid control [21]. Guided state-action diffusion approaches for humanoids [22], [23] further show the ability to perform look-ahead planning and multitask control within a unified framework. 

Despite these advances, current humanoid diffusion controllers rely fundamentally on privileged full-body state information at deployment. These methods assume access 


Fig. 1: Deployment of Sensor-Conditioned Diffusion Policies (SCDP) on Unitree G1, performing robust locomotion at 50 Hz using only proprioceptive sensors, without external motion capture or state estimation. 

to global position, orientation, base velocity, and rigid-body position, requiring complex and often unreliable state estimation pipelines on real robots outside the lab setting. The removal of privileged inputs dramatically degrades performance, with catastrophic failures even in simple tasks such as joystick locomotion [23]. This dependence is not viable in most practical deployment scenarios, as only direct onboard proprioceptive sensing is reliably available. Learning solely from onboard sensing induces a partially observable Markov decision process (POMDP), in which policies must infer hidden global states from incomplete observations. Existing diffusion-based controllers are not designed to operate under partial observability. 

We address this limitation with our proposed framework, SCDP, a diffusion-based distillation framework for humanoid control using only onboard proprioceptive measurements. Our key idea is to decouple sensing from supervision via mixed-observation training. During training, the model conditions only on onboard sensor histories while being supervised to predict privileged full-body state trajectories. This asymmetry enforces internal representation learning that captures global body dynamics from partial sensing, eliminating explicit state estimation at deployment. 

Unlike prior teacher–student transfer methods developed for MLP-based locomotion policies [2], [5], [24], [25], which distill reactive mappings from observation to action, SCDP addresses a fundamentally different problem: distilling a generative trajectory planner from offline datasets. While recent work has explored distilling RL policies into interpretable models for locomotion [26], our goal here is to enable such distillation under partial observability without 

privileged state information, where the student policy must jointly denoise temporally _coherent state-action sequences_ with incomplete information. Our proposed training formulation resolves this and enables deployment without privileged sensing. 

The key contributions of this work are as follows: 

- Mixed observation training, which conditions on sensor histories while predicting privileged state trajectories, enables implicit inference of global body dynamics. 

- Restricted denoising, which excludes base velocity from denoising inputs while retaining it in supervision, forces the model to infer velocity from context, enabling control without velocity feedback. 

- Context distribution alignment, which maintains consistent causal relationships between states and actions across training and inference. 

- Context-aware attention masking enables bidirectional attention within the context window to facilitate inference of latent dynamics from partial observations. 

- Experimental validation via deployment on physical Unitree G1 at 50 Hz (Fig. 1), and systematic ablations on data collection, context length, and architectural choices. 

## II. METHOD 

We present SCDP, a framework for distilling a diffusionbased controller from an expert RL policy to achieve wholebody humanoid control from onboard sensing. Our approach consists of four key components: (1) a Multi-Motion Tracking Policy (MMP) serving as an expert demonstrator; (2) our diffusion distillation framework; (3) a data collection methodology for robust distillation; and (4) a real-time deployment configuration for the Unitree G1. We describe each component below, showing how they combine to enable sensor-based control. 

## _A. Multi-Motion Tracking Policy_ 

The foundation of our distillation framework is a MultiMotion Policy (MMP), an RL-trained expert for multimotion tracking that is built upon the reward function and PD controller from [23]. All quantities are expressed in the anchor-centric (set as the torso), heading-aligned frame via _R_ yaw, the rotation aligning the global frame with the root heading. For each tracked body _b ∈B_ , we compute local positions, orientations, and velocities as: 


_o_ robot = [ _h_ anchor _, {p_ ˜ _b, R_<sup>˜</sup> _b,_ ˜ _vb,_ ˜ _ωb}b∈B, at−_ 1] is the selfobservation. The task observation provides both absolute and relative future states for each reference body _bm ∈Bm_ over a look-ahead horizon of _H_ steps: 


where _p_ ˆ<sup>(</sup> _b_<sup>_k_</sup> _m_<sup>)=</sup><sup>_R_yaw(</sup><sup>_p_(</sup> _b_<sup>_k_</sup> _m_<sup>)</sup><sup>_−p_anchor)and∆</sup><sup>_p_(</sup> _b_<sup>_k_</sup> _m_<sup>)=</sup><sup>_R_yaw(</sup><sup>_p_(</sup> _b_<sup>_k_</sup> _m_<sup>)</sup><sup>_−_</sup> _pb_ ) capture absolute and relative positions respectively, with orientations defined analogously. 

_B. Mixed-Observation Distillation: Learning Global Dynamics from Partial Sensing_ 

The key idea of mixed-observation distillation is to _decouple sensing from supervision_ during training. In particular, we condition the diffusion model on historical observations from onboard sensors ( _ot_ ), while supervising it to predict future trajectories that include privileged full-body states ( _st_ ). This asymmetry, shown in Fig. 2, enables the model to learn an implicit forward model of global body dynamics, allowing deployment without explicit state estimation. 

_1) Problem Formulation:_ We consider a humanoid robot with a full state _st ∈S_ and an action space _at ∈A_ . The full state comprises: _st_ = � _ot, {p_ ˜ _b}b∈B, {v_ ˜ _b}b∈B_ � _,_ where _ot_ contains proprioceptive measurements and _{p_ ˜ _b}b∈B_ , _{v_ ˜ _b}b∈B_ are the local positions and velocities of rigid bodies _b ∈B_ in the heading-aligned frame. These geometric quantities are available in simulation but not on hardware. At inference, the robot accesses only onboard measurements: _ot_ = � _v_ pelvis _, ω_ pelvis _, q − q_ 0 _, q,_ ˙ _g_ pelvis _, g_ torso� _,_ denoting pelvis linear velocity _v_ pelvis, pelvis angular velocity _ω_ pelvis, joint positions relative to the default _q − q_ 0, joint velocities _q_ ˙, and gravity vectors in the pelvis and torso frames _g_ pelvis _, g_ torso. Note that _v_ pelvis is excluded in our final model because velocity estimates are unreliable on hardware. Critically, _ot_ lacks geometric information about body positions and provides only local kinematic and inertial measurements. The diffusion policy _π_ ( _τt | Ot, ct_ ) generates stateaction trajectories conditioned on observation history _Ot_ and task commands _ct_ (velocity or motion reference commands), where trajectories are defined as _τt_ = [ _at, st_ +1 _, at_ +1 _, . . . , st_ + _H_ ] and observation histories are defined as _Ot_ = [ _ot−N , at−N , . . . , ot−_ 1 _, at−_ 1 _, ot_ ] _._ Crucially, while _inference_ uses only _Ot_ , _training_ supervises predictions of privileged states _st_ +1: _t_ + _H_ . This mixedobservation formulation is the key to transferring full-body motion knowledge to sensor-only deployment. 

_a) Diffusion Model Formulation:_ We model the problem using a denoising diffusion probabilistic model (DDPM) [27] to iteratively denoise trajectory samples. At diffusion timestep _k_ , a noised trajectory _τt_<sup>_k_is</sup> refined by predicting the clean trajectory _x_ 0 _,θ_ ( _τt_<sup>_k, Ot, ct_):</sup> 


Sampling proceeds by iteratively applying: 


with standard DDPM coefficients ( _αk, γk, σk_ ) and predicted noise _ϵθ_ derived from _x_ 0 _,θ_ . We use independent noise schedules for state and action components of _τt_ as in [22]. 

_2) Restricted Denoising:_ A remaining challenge is achieving velocity control without direct velocity feedback. While mixed-observation training provides geometric information through prediction targets, the model can use partially-noised velocity terms as shortcuts during training. To force genuine velocity inference from context, we introduce restricted denoising which omits pelvis linear velocities 


Fig. 2: **Sensor-Conditioned Diffusion Policies (SCDP) architecture and training framework.** The state-action diffusion policy conditions on sensor observation history _{ot}_ , past actions _{at}_ , and commands _ct_ , while predicting future trajectories containing privileged states _{st}_ and actions. This mixed-observation formulation enables learning global dynamics from partial sensing. 

_v_ pelvis from the denoising inputs but retains them in the supervision target: _s_<sup>res</sup> _t_ = _st \ {v_ pelvis _}_ . The corresponding restricted trajectory is _τt_<sup>res</sup> = [ _at, s_<sup>res</sup> _t_ +1<sup>_,at_+1</sup><sup>_,. . . ,s_res</sup> _t_ + _H_<sup>].</sup> The denoising model takes restricted trajectories as input but predicts full trajectories including velocities: 


This enforces the model to infer pelvis velocities from the historical context, developing robust velocity estimation without direct feedback. 

_3) Context Distribution Alignment:_ Prior works [22], [23] train on ( _s_ noised _, a_ ) pairs, where _s_ noised results from executing noised actions _a_ noised, creating a distribution mismatch at inference when the model observes clean, ( _s, a_ ) context. During training, we provide the context using ( _s_ noised _, a_ noised) pairs. This aligns the training context and deployment conditions, reducing distribution shift and maintaining a causal relationship between ( _s, a, s_<sup>_′_</sup> ) of the context in both settings. 

_4) Context-Aware Attention Masking:_ Attention masking approaches in prior works [22], [23] apply causal masks that prevent states from attending to actions, while allowing attention to future states. In contrast, we enable bidirectional attention within the context window while maintaining causal constraints only in the prediction horizon. This enables the model to aggregate historical information bidirectionally, facilitating the inference of latent dynamics from partial observations. 

_5) Representation Alignment:_ We experiment with a cosine-similarity alignment loss to bridge the information gap between sensor observations and privileged states. Specifically, the loss encourages alignment between the sensor encoder output _ϕo_ ( _ot_ ) and the privileged state encoder output _ϕs_ ( _st_ ), averaged over the context window. However, we found this approach detrimental to performance in our experiments (see Sec. III-D) and excluded it from the final SCDP model. 

_6) Velocity Conditioning:_ We condition on desired pelvis velocities _ct_ = [ _v_ cmd<sup>_x, v_</sup> cmd<sup>_y,ψ_˙cmd]</sup><sup>_∈_R3viaMLPencoding</sup> 

_ϕc_ : R<sup>3</sup> _→_ R<sup>_d_</sup> combined with timestep embeddings: _et_ = _e_<sup>time</sup> _t_ + _ϕc_ ( _ct_ ). To enforce tracking, we minimize _L_ cmd = _∥ct − c_ ¯ _t∥_ 2<sup>2where</sup><sup>_c_¯</sup><sup>_t_isthemeanpredictedvelocityoverthe</sup> horizon. 

_7) Motion Reference Conditioning:_ For motion tracking, we condition on _ct_ = [ _q_ ref _, q_ ˙ref _,_ **R** rel], where **R** rel = **q**<sup>_−_</sup> robot<sup>1</sup><sup>_⊗_</sup> **q** ref represents the relative orientation between robot and reference frames. The complete training objective is: 


## _C. Datasets_ 

The MMP is trained on walking motions from PHCfiltered AMASS (AMASS-walk) [5], [28], retargeted via Mink [29]. For SCDP distillation, we select 65 diverse clips, mirror them (130 total), and use the expert to collect 40 rollouts per reference with stochastic actions [21], domain randomization [23], and push forces (every 1-3s). This yields 5200 trajectories ( _∼_ 750k timesteps at 50 Hz). Motion tracking uses the full AMASS-walk training set, with only a single rollout per trajectory. 

## _D. Training and Deployment Configuration_ 

The MMP is a six-layer MLP (hidden dims: [1024, 1024, 1024, 1024, 512, 128]) trained using PPO [30] for 100k iterations in IsaacLab [31] across 4096 parallel environments with a learning rate of 3 _×_ 10<sup>_−_4</sup> . Training takes approximately four days on an NVIDIA RTX 5090. 

The SCDP diffusion model uses a six-layer Transformer encoder with four attention heads, embedding dimension 512, and feed-forward dimension 1024. Four encoders process actions (1-layer MLP), onboard observations (2-layer MLP), privileged states (2-layer MLP), and commands (2layer MLP). The model predicts 16-step trajectories with action losses weighted to zero beyond 8 steps for near-term accuracy; at inference, only the first action is executed before replanning. Training uses 1M gradient updates with batch size 128, AdamW optimizer, cosine learning rate schedule (2k-step warmup to 10<sup>_−_4</sup> , decay to 10<sup>_−_6</sup> ), and weight decay 

TABLE I: Success/completion rates (%) across observation modes. Subscript – priv: privileged states; co: context observations only; mo: mixed observations. Bold: best per task. 

|**Method**|_v_**pelvis feedback**|**Perturb**|**Navigation**|**Joystick**|
|---|---|---|---|---|
|BCco|✓|70.1|43.8|70.0|
|BCco|_×_|5.0|4.0|4.0|
|BeyondMimicpriv|✓|99.4|98.6|**100.0**|
|BeyondMimicco|✓|20.7|22.2|3.0|
|BeyondMimicmo|✓|99.4|94.4|94.0|
|BeyondMimicmo|_×_|92.0|5.6|93.0|
|Ourspriv|✓|99.3|**100.0**|**100.0**|
|Oursco|✓|59.8|58.8|11.0|
|Oursmo|✓|99.1|99.4|**100.0**|
|Oursmo|_×_|96.0|93.2|90.0|
|Ours: SCDP|_×_|**99.8**|99.8|**100.0**|


10<sup>_−_6</sup> . Training completes in approximately one day on an RTX 5090. 

We deploy SCDP on a Unitree G1 at 50 Hz with the model running on a remote workstation (RTX 5090), achieving 105 Hz throughput via ONNX Runtime (Figs. 4, and 5). 

## III. SIMULATION RESULTS 

We evaluate the framework in simulation by addressing four questions on sensor-based diffusion control: ( **Q1** ) Can diffusion policies succeed with geometrically uninformative observations? ( **Q2** ) Can they achieve velocity control without state estimation? ( **Q3** ) What design choices are most critical? ( **Q4** ) Can SCDP transfer to motion tracking control? 

All policies are evaluated at 50 Hz in IsaacLab [31] with domain randomization. We assess four tasks: **(1) Perturbation Recovery:** The robot walks forward at 0.5 m/s for 15 seconds while experiencing random velocity perturbations of _±_ 0 _._ 5 m/s every 1-3 seconds. Success requires maintaining balance throughout (1000 trials). Learning to recover from such perturbations is a fundamental motor skill that shall be acquired, as recent work has shown that such behaviors can be learned via RL [32]. **(2) Joystick Control:** The robot executes a sequence of discrete velocity commands (forward 0.5 m/s, backward _−_ 0 _._ 5 m/s, turn left +1 _._ 0 rad/s, turn right _−_ 1 _._ 0 rad/s), each held for 3 seconds. Success requires completing all commands without falling (100 trials). **(3) Waypoint Navigation:** Five targets are randomly sampled within a radius of 2.5 m. The robot must reach all waypoints within 60 seconds (Fig. 3). We report the mean completion rate (100 trials). **(4) Motion Reference Tracking:** The robot reproduces specific reference motions. We evaluate using the Mean Per-Joint Position Error (MPJPE-L/G for local/global), velocity and acceleration distributions, and the success rate. 

## _A. Comparison with Baseline Methods_ 

We compare our approach against the classifier-guided baseline from [22] and behavior cloning (BC). We evaluate four observation variants: **priv** ( _st_ for context and prediction), **co** ( _ot_ for context and prediction), **mo** (mixedobservation training: _ot_ for context, _st_ for prediction), and whether the context contains _vpelvis_ feedback. 

TABLE II: Perturbation recovery success rates (%) under varying data collection strategies, Color intensity indicates performance (green=high, red=low). 

|**Noise**|**0.**|**0 m/s**|**0.**|**5 m/s**|**1.**|**0 m/s**|
|---|---|---|---|---|---|---|
|**Level**|**Push**|**No Push**|**Push**|**No Push**|**Push**|**No Push**|
|0.0|98.2|32.5|98.2|24.7|95.8|18.7|
|0.06|99.3|78.4|99.0|79.4|98.9|74.1|
|0.12|87.1|81.6|99.5|98.0|98.8|95.0|
|0.18|97.5|82.4|99.4|99.2|98.8|99.6|
|0.24|88.2|70.0|99.1|99.6|99.2|99.3|


TABLE III: Effect of context length on performance without velocity feedback. Bold indicates best per task. 

|**Context Length**|_v_**pelvis feedback**|**Perturb Succ. (%)**|**Nav. Compl. (%)**|
|---|---|---|---|
|**Oursmo**||||
|4|_×_|84.3|74.2|
|8|_×_|98.2|87.8|
|16|_×_|55.5|33.4|
|**SCDP**||||
|4|_×_|**99.5**|**97.8**|
|8|_×_|96.8|86.6|
|16|_×_|96.0|75.4|


Our final model, SCDP, employs mixed observation training, restricted denoising, context distribution alignment, and context-aware attention masking, operating without _vpelvis_ feedback. 

Table I reveals several key findings. First, contextualonly policies (co) show significant degradation compared to their privileged counterparts, confirming that geometric information is essential in standard diffusion distillation ( **Q1** ). Mixed-observation training (mo) resolves this dependency entirely, with near-perfect performance comparable to their privileged counterparts. This demonstrates that diffusion policies can successfully operate from geometrically uninformative observations when optimized under our proposed mixed-observation training ( **Q1** ). Crucially, velocity feedback is essential for reliable control across prior methods. The results show that our full method, SCDP, does not depend on velocity feedback; it achieves competitive scores across all tasks, matching or exceeding the privileged methods. These results confirm that our proposed framework enables robust velocity control without the need for state estimation ( **Q2** ), enabling control under partial observability where previous methods fail. 

## _B. Data Collection Strategy Ablation_ 

We vary the application of action noise (0.0–0.24 std) and push force during data collection, evaluating perturbation recovery at 0.0, 0.5, and 1.0 m/s. Table II shows that moderate action noise is essential. Without noise or pushing, policies achieve _<_ 33% success, improving to _>_ 70% with minimal noise. Second, push perturbations provide benefits without added noise, increasing the success from _<_ 33% to _>_ 90%. Applying both is optimal, exposing the policy to recovery behaviors that action noise alone cannot provide is beneficial, while excessive noise (0.24) degrades stationary performance ( **Q3** ). 


Fig. 3: **Waypoint navigation task.** Sequential frames showing the SCDP controlling the robot to navigate succesfully to all five waypoints (green: current target, red: remaining targets). 


Fig. 4: **Fast forward walking behaviour.** Sequential frames showing the policy executing forward locomotion. 


(a) Time-lapsed frames showing **walking right** . (b) Time-lapsed frames Fig. 5: Comparison of walking right and walking left sequences. 


Fig. 6: **Velocity tracking performance.** Comparison of realized velocities against commanded targets (black) for (a) linear velocity _vx_ and (b) yaw rate _ψ_<sup>˙</sup> . SCDP (orange) exhibits smoother tracking with reduced oscillations compared to the BeyondMimic baseline (teal), with slight lag during direction changes. 

## _C. Context Length Ablation_ 

We investigate how context length affects policy robustness without _v_ pelvis feedback. Specifically, we evaluate context lengths of 4, 8, and 16, comparing SCDP with Oursmo. Table III shows that a four-step context sufficiently enables the SCDP model to capture dynamics, with longer histories degrading performance. In contrast, Oursmo shows inconsistent performance across context lengths, with a nonmonotonic relationship between context length and success rate. Notably, both methods degrade with 16-step contexts, suggesting that longer histories amplify compounding errors at inference or distribution mismatch ( **Q3** ). 

## _D. Feature Design Ablation_ 

We systematically evaluate the contribution of each design component when training without velocity feedback. We present results across four sets of configurations in Tab. V: all features enabled, no features, an exclusion ablation (all except one), and an inclusion ablation (only one feature). The exclusion ablation reveals that mixed-observation training is the foundation: removing it causes complete failure (1.4%). Conversely, removing representation alignment achieves the best performance (97.8%), showing that representation alignment interferes with optimization. Context distribution alignment proves critical: its removal drops performance to 

TABLE IV: Motion tracking performance on AMASS-walk dataset. MMP: expert upper bound. 

|||||**Train**|||||**Test**|||
|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|_v_**pelvis feedback**|**MPJPE-G** _↓_|**MPJPE-L** _↓_|**Vel-Dist** _↓_|**Accel-Dist** _↓_|**Success** _↑_|**MPJPE-G** _↓_|**MPJPE-L** _↓_|**Vel-Dist** _↓_|**Accel-Dist** _↓_|**Success** _↑_|
|MMP _(upper bound)_|✓|69.84 _±_ 25.96|47.73 _±_ 23.82|3.03 _±_ 1.07|1.00 _±_ 0.47|98.94|69.22 _±_ 26.12|46.58 _±_ 22.99|3.07 _±_ 1.04|1.03 _±_ 0.46|99.03|
|BC|_×_|370.36 _±_ 278.93|53.65 _±_ 23.15|12.87 _±_ 7.59|14.78 _±_ 13.91|30.19|371.66 _±_ 276.42|**50.71** _±_ 19.66|6.39 _±_ 3.01|**1.31** _±_ 0.55|31.24|
|Ours_mo_<br>SCDP|_×_<br>_×_|457.87 _±_ 374.15<br>**282.43** _±_ 167.54|54.81 _±_ 22.82<br>**53.63** _±_ 23.60|6.16 _±_ 2.33<br>**5.37** _±_ 2.14|**1.33** _±_ 0.48<br>1.48 _±_ 0.70|78.39<br>**93.12**|473.91 _±_ 408.60<br>**288.30** _±_ 184.22|54.36 _±_ 21.98<br>53.12 _±_ 23.03|6.41 _±_ 2.52<br>**5.55** _±_ 2.25|1.39 _±_ 0.51<br>1.51 _±_ 0.74|79.17<br>**93.22**|


TABLE V: Ablation study on key design components for diffusion policies without velocity feedback. 

|**Mixed Obs.**<br>**Training**|**Representation**<br>**Context Dist.**<br>**Alignment**<br>**Alignment**|**Full Prefix**<br>**Attention**|**Restricted**<br>**Denoising**|**Navigation**<br>**(%)**|
|---|---|---|---|---|
|_All features_|||||
|✓|✓<br>✓|✓|✓|89.2|
|_No features_|||||
|_×_|_×_<br>_×_|_×_|_×_|1.4|
|_Section 1: Exc_|_lusion Ablation (all except one)_||||
|_×_|_×_<br>✓|✓|✓|1.4|
|✓|_×_<br>✓|✓|✓|**97.8**|
|✓|✓<br>_×_|✓|✓|9.7|
|✓|✓<br>✓|_×_|✓|81.0|
|✓|✓<br>✓|✓|_×_|92.2|
|_Section 2: Sin_|_gle Feature (only one)_||||
|✓|_×_<br>_×_|_×_|_×_|74.2|
|✓|✓<br>_×_|_×_|_×_|61.2|
|_×_|_×_<br>✓|_×_|_×_|1.6|
|_×_|_×_<br>_×_|✓|_×_|2.6|
|_×_|_×_<br>_×_|_×_|✓|1.2|


9.7%, showing its importance for achieving sensor-based control without velocity feedback. The single-feature results demonstrate that mixed-observation training alone achieves 74.2% success, while context distribution alignment, full prefix attention, and restricted denoising provide negligible benefits in isolation. These results show that mixedobservation training is necessary for sensor-based control, while context distribution alignment, full prefix attention, and restricted denoising collectively enable the full method to match privileged-observation performance, providing additional reliability and robustness ( **Q3** ). 

## _E. Velocity Tracking Performance_ 

We evaluated velocity tracking fidelity and responsiveness compared to BeyondMimic [23] and the classifier-guided baseline, while tracking commanded velocities varying between _±_ 1 m/s (linear) and _±_ 2 rad/s (angular). Both policies successfully track nominal velocities, but our method achieves tighter linear tracking with reduced oscillations (Fig. 6a), though with slightly increased lag ( _∼_ 250–500 ms) during direction reversals. Angular velocity tracking is comparable (Fig. 6b). 

## _F. Motion Reference Tracking Performance_ 

We evaluate SCDP’s ability to reproduce reference motions from its training distribution (AMASS). Table IV shows that each distillation method achieves comparable local pose accuracy (MPJPE-L) to the expert upper bound, measured while the episode has not terminated. Diffusion-based distillation training with mixed observation training already significantly outperforms the BC baseline, with an evaluation set success rate of 79% compared to 31%. Furthermore, SCDP greatly outperforms both methods with a success rate of 93% and a reduction of the global position error (MPJPEG) from 473 to 288, confirming its effectiveness at reference motion tracking ( **Q4** ). SCDP has significant global position 

error as opposed to the expert. This is expected because the expert observes its global drift from the reference and is able to correct it, while this is not possible under partial observability. SCDP must track the global position from the kinematic reference command alone. 

## IV. CONCLUSION 

We presented SCDP that achieves diffusion distillation of whole-body humanoid controllers under partial observability via three techniques: mixed-observation training, restricted denoising, and context alignment. 

Our study showed that previous diffusion and offline distillation methods fail with geometrically uninformative and partial observations, critically depending on the _base velocity_ feedback, while SCDP excels in this scenario. Furthermore, we highlight SCDP’s versatility, demonstrating the effectiveness in both velocity control (99%) and motion reference tracking (93%). 

We presented systematic ablations that identify the optimal design choices and data collection procedures. Finally, SCDP was running in a closed-loop at 50 Hz for performance validation on a real physical G1 robot, showing _robust simto-real transfer_ . 

Future work shall explore sim-to-real fine-tuning that do not require privileged states, drift-correction mechanisms for long-horizon motion tracking, and the extension to contactrich manipulation and complex terrain scenarios. 

## REFERENCES 

- [1] G. B. Margolis _et al._ , “Walk these ways: Tuning robot control for generalization with multiplicity of behavior,” _Conference on Robot Learning_ , 2022. 

- [2] N. Rudin _et al._ , “Learning to walk in minutes using massively parallel deep reinforcement learning,” in _Proceedings of the 5th Conference on Robot Learning_ , ser. Proceedings of Machine Learning Research, A. Faust _et al._ , Eds., vol. 164. PMLR, 08–11 Nov 2022. 

- [3] T. Peng _et al._ , “Gait-conditioned reinforcement learning with multiphase curriculum for humanoid locomotion,” in _2025 IEEE-RAS 24th International Conference on Humanoid Robots (Humanoids)_ , 2025. 

- [4] X. B. Peng _et al._ , “Deepmimic: example-guided deep reinforcement learning of physics-based character skills,” _ACM Trans. Graph._ , vol. 37, no. 4, Jul. 2018. 

- [5] T. He _et al._ , “Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning,” 2024. 

- [6] Z. Fu _et al._ , “Humanplus: Humanoid shadowing and imitation from humans,” in _Conference on Robot Learning (CoRL)_ , 2024. 

- [7] L. Bao _et al._ , “Deep reinforcement learning for robotic bipedal locomotion: a brief survey,” _Artificial Intelligence Review_ , vol. 59, no. 1, Dec. 2025. 

- [8] C. Tessler _et al._ , “Maskedmimic: Unified physics-based character control through masked motion inpainting,” _ACM Transactions on Graphics (TOG)_ , 2024. 

- [9] Y. Ze _et al._ , “Twist: Teleoperated whole-body imitation system,” _arXiv preprint arXiv:2505.02833_ , 2025. 

- [10] K. Yin _et al._ , “Unitracker: Learning universal whole-body motion tracker for humanoid robots,” 2025. 

- [11] Z. Chen _et al._ , “Gmt: General motion tracking for humanoid wholebody control,” _arXiv:2506.14770_ , 2025. 

- [12] C. Yang _et al._ , “Multi-expert learning of adaptive legged locomotion,” _Science Robotics_ , vol. 5, no. 49, p. eabb2174, 2020. 

- [13] G. Tevet _et al._ , “Human motion diffusion model,” in _The Eleventh International Conference on Learning Representations_ , 2023. 

- [14] G. Tevet _et al._ , “CLoSD: Closing the loop between simulation and diffusion for multi-task character control,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [15] L. Bao _et al._ , “Hierarchical intention-aware expressive motion generation for humanoid robots,” 2025. 

- [16] J. Sohl-Dickstein _et al._ , “Deep unsupervised learning using nonequilibrium thermodynamics,” in _Proceedings of the 32nd International Conference on Machine Learning_ , vol. 37. Lille, France: PMLR, 07–09 Jul 2015. 

- [17] K. Karunratanakul _et al._ , “Guided motion diffusion for controllable human motion synthesis,” 2023. 

- [18] C. Chi _et al._ , “Diffusion policy: Visuomotor policy learning via action diffusion,” _The International Journal of Robotics Research_ , 2023. 

- [19] X. Huang _et al._ , “Diffuseloco: Real-time legged locomotion control with diffusion from offline datasets,” in _Proceedings of The 8th Conference on Robot Learning_ , ser. Proceedings of Machine Learning Research, P. Agrawal _et al._ , Eds., vol. 270. PMLR, 06–09 Nov 2025. 

   - [24] S. Ross _et al._ , “A reduction of imitation learning and structured prediction to no-regret online learning,” 2011. 

   - [25] M. Ji _et al._ , “Exbody2: Advanced expressive humanoid whole-body control,” _arXiv preprint arXiv:2412.13196_ , 2024. 

   - [26] F. Acero _et al._ , “Distilling reinforcement learning policies for interpretable robot locomotion: Gradient boosting machines and symbolic regression,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 6840–6847. 

   - [27] J. Ho _et al._ , “Denoising diffusion probabilistic models,” 2020. 

   - [28] N. Mahmood _et al._ , “AMASS: Archive of motion capture as surface shapes,” in _International Conference on Computer Vision_ , Oct. 2019. 

   - [29] K. Zakka, “Mink: Python inverse kinematics based on MuJoCo,” May 2025. 

   - [30] J. Schulman _et al._ , “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

   - [31] M. Mittal _et al._ , “Orbit: A unified simulation framework for interactive robot learning environments,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 6, 2023. 

   - [32] C. Yang _et al._ , “Learning complex motor skills for legged robot fall recovery,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 7, pp. 4307–4314, 2023. 

- [20] G. Mothish _et al._ , “Birodiff: Diffusion policies for bipedal robot locomotion on unseen terrains,” 2024. 

- [21] T. E. Truong _et al._ , “Pdp: Physics-based character animation via diffusion policy,” in _SIGGRAPH Asia 2024 Conference Papers_ . NY, USA: Association for Computing Machinery, 2024. 

- [22] X. Huang _et al._ , “Diffuse-cloc: Guided diffusion for physics-based character look-ahead control,” _ACM Transactions on Graphics (TOG)_ , vol. 44, no. 4, 2025, sIGGRAPH 2025. 

- [23] Q. Liao _et al._ , “Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion,” 2025. 

