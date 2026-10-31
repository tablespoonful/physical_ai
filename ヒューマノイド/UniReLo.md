---
title: "UniReLo: Learning a Unified Humanoid Policy from Fall Recovery to Locomotion across Diverse Terrains"
date: "2026-06-08"
authors: "Xiaoyu Xu; Zhiming Chen; Yuenan Zhao; Ran Song; Wei Zhang"
url: https://arxiv.org/abs/2606.08922
pdf: https://arxiv.org/pdf/2606.08922
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.08922)** / [論文ページ](https://arxiv.org/abs/2606.08922)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **UniReLo: Learning a Unified Humanoid Policy from Fall Recovery to Locomotion across Diverse Terrains** 

Xiaoyu Xu, Zhiming Chen, Yuenan Zhao, Xiang Zhang, Ran Song, and Wei Zhang<sup>_∗_</sup> 


Fig. 1: Real-world disturbance-rejection and recovery-to-locomotion behaviors ofUniReLo across indoor flat ground and representative outdoor field terrains. Under moderate perturbations, the robot maintains locomotion through coordinated whole-body regulation and adaptive foot placement. Under fall-inducing perturbations, it performs whole-body recovery, re-establishes terrain-compatible support, and resumes commanded locomotion. Red arrows denote external disturbances. 

**_Abstract_ — Reliable fall recovery, which commonly aims at attaining a nominal upright posture, is essential for the autonomous operation of humanoid robots in unstructured field environments. Although existing posture-centered methods can synthesize coordinated whole-body recovery motions from diverse fallen configurations, they may result in a dynamically fragile support state, leading to secondary loss of balance or unstable resumption of commanded locomotion, particularly under terrain-dependent contact conditions. We propose to learn a unified humanoid policy from fall recovery to locomotion (UniReLo) across heterogeneous field terrains. UniReLo leverages continuously gated multi-scale motion priors to modulate frame-, sequence-, and gait-level adversarial supervision according to recovery progress, preserving the distinct temporal structures of recovery and locomotion without requiring fixedthreshold switching. In addition, terrain-conditioned recovery guidance evaluates the evolving support state using a terrain-relative support representation and support-feasibility assessment. Simulation and outdoor real-world experiments demonstrate that UniReLo can deliver stable and continuous recovery-to-locomotion behaviors for humanoids across diverse field terrains. The supplementary video is available at https: //vsislab.github.io/UniReLo/.** 

All authors are with the School of Control Science and Engineering, Shandong University, Jinan 250061, China. Xiaoyu Xu, Yuenan Zhao, Ran Song, and Wei Zhang are also with the Key Laboratory of Machine Intelligence and System Control, Ministry of Education, China. _∗_ Corresponding author: Wei Zhang (davidzhang@sdu.edu.cn). 

## I. INTRODUCTION 

Humanoid robots operating in unstructured field environments are vulnerable to falls caused by uneven terrain, uncertain contacts, surface deformation, and external disturbances. Autonomous fall recovery is therefore critical to limiting task interruption, avoiding secondary falls, and sustaining operation without human assistance. For humanoids, however, successful recovery involves more than returning the body to an upright posture. The contact configuration, wholebody posture, and momentum established during the rising motion jointly determine whether the robot can regain dynamic balance and continue task execution. This requirement becomes particularly important in outdoor environments, where loose, inclined, and irregular surfaces can make a posture that is recoverable on rigid flat ground unsuitable for continued locomotion. Fall recovery should thus be viewed as a continuous process of restoring dynamically viable task capability, rather than as an isolated posture-reaching maneuver. 

Recent advances in reinforcement learning (RL) have enabled end-to-end humanoid standing-up and fall recovery from diverse fallen configurations, without handcrafted motion scripts or prescribed contact sequences [1]. However, in the absence of reference-motion constraints, motion quality 

must be induced indirectly through task-oriented rewards and is therefore sensitive to reward shaping and exploration design. With the development of motion-prior-based RL, methods such as DeepMimic and Adversarial Motion Priors (AMP) showed that reference motions can regularize policy learning and improve the physical plausibility and style consistency of learned behaviors [2], [3]. This provides a promising foundation for integrating multiple behaviors within a single policy. Nevertheless, a policy spanning nonperiodic whole-body recovery, transient support reorganization, and periodic locomotion must represent motion distributions with markedly different temporal structures. A shared, undifferentiated adversarial prior does not explicitly preserve these distinctions, whereas hard mode-dependent routing reintroduces discrete behavioral boundaries. Learning a unified policy therefore requires motion supervision that distinguishes heterogeneous temporal structures while adapting continuously to the evolving recovery state, enabling a smooth progression from whole-body recovery through support reorganization to resumed locomotion. A further challenge arises from the terrain dependence of recovery viability. In field environments, successful rising cannot be determined by body height or uprightness alone, because the resulting support state may still exhibit insufficient support margin, a terrain-incompatible knee configuration, foot slip, or downhill drift. Such states may appear nominally recovered but remain unable to sustain commanded locomotion, leading to secondary loss of balance. Moreover, the recoverability of the same fallen pose may vary substantially across rigid ground, loose gravel, and inclined terrain [4]. 

This paper proposes UniReLo, a framework for learning a unified humanoid policy from fall recovery to velocitycommanded locomotion across heterogeneous field terrains, as shown in Fig. 1. Rather than defining recovery by the attainment of a nominal upright posture, UniReLo guides the robot toward a terrain-compatible support state that can sustain continued command execution. In UniReLo, continuously gated multi-scale motion priors first modulate frame-, sequence-, and gait-level adversarial supervision according to recovery progress, enabling motion guidance to evolve smoothly across whole-body recovery, support reorganization, and commanded locomotion. Then, terrainconditioned recovery guidance constructs a terrain-relative support representation and performs support-feasibility assessment to derive a physically grounded measure of recovery progress. In addition, terrain-pose plasticity-aware initialization is employed during training to increase exposure to terrain-sensitive recovery configurations. All components are jointly optimized within a single proprioceptive policy and implemented on a 29-DoF Unitree G1 humanoid, without terrain-specific policy selection during deployment. 

Our main contributions are summarized as follows: 

- We formulate fall recovery as restoring a terraincompatible, dynamically viable state for continued command execution, enabling a single policy to unify wholebody recovery, support reorganization, and velocitycommanded locomotion across diverse field terrains. 

- We modulate frame-, sequence-, and gait-level adversarial supervision according to recovery progress, enabling motion guidance to evolve smoothly across wholebody recovery, support reorganization, and commanded locomotion, while preserving their distinct temporal characteristics. 

- We develop terrain-conditioned recovery guidance that combines a terrain-relative support representation with support-feasibility assessment, providing a continuous measure of progress toward terrain-compatible, locomotion-ready states. 

## II. RELATED WORK 

This section reviews related work in two areas: learningbased humanoid recovery and motion priors, and terrainadaptive recovery-to-locomotion control. 

## _A. Learning-Based Humanoid Recovery and Motion Priors_ 

Humanoid fall recovery has traditionally been addressed through contact planning, trajectory optimization, and modelbased balance control [5], [6], [7]. Although these approaches provide interpretable contact sequences and dynamically consistent trajectories, they often rely on predefined contact models, recovery templates, or online optimization. Recent deep reinforcement learning methods instead learn feedback policies directly from diverse fallen configurations, reducing the need for handcrafted motion scripts and prescribed contact sequences [8], [9], [4], [1]. Related work further couples fall mitigation with post-fall recovery [10]. For methods trained primarily through task-oriented rewards, however, motion smoothness, physical plausibility, and temporal coherence must be induced indirectly through reward shaping, exploration design, and additional regularization, which is particularly challenging for nonperiodic and contact-rich whole-body recovery. 

Reference-motion-guided reinforcement learning provides a complementary means of shaping recovery behaviors. DeepMimic [2] tracks structured motion references, whereas AMP [3] learns data-driven style rewards from referencemotion distributions. Existing multi-skill AMP variants commonly associate different reference datasets or motion priors with predefined skill commands or heuristic state partitions. Multiple AMP enables discrete switching among motion styles through explicit skill conditioning [11]. For recoveryto-locomotion control, Lu et al. [12] divide recovery and locomotion into two discrete behavioral stages and assign the corresponding motion samples according to fixed state thresholds, making motion-prior selection dependent on predefined transition criteria. 

_B. Terrain-Adaptive and Recovery-to-Locomotion Control_ 

Terrain geometry, friction, compliance, and contact uncertainty substantially affect foothold feasibility, support stability, and whole-body posture. Terrain-adaptive locomotion policies address these variations through domain randomization, terrain curricula, observation histories, implicit terrain estimation, and exteroceptive perception [13], [14], 


Fig. 2: Overview of the proposed UniReLo framework. Terrain-conditioned recovery guidance constructs a terrain-relative support representation, evaluates support feasibility, and produces recovery progress _αt_ , which is used by the continuously gated multi-scale motion priors to coordinate frame-, sequence-, and gait-level adversarial supervision. Terrain-pose plasticityaware initialization complements these mechanisms by emphasizing terrain-sensitive fallen configurations during training. All training signals jointly update the unified policy, while only the proprioceptive actor is retained for deployment. 

[15], [16], [17], [18], [19], [20]. Beyond general terrain adaptation, recent studies show that terrain constraints must be considered together with the contact requirements and whole-body dynamics of the target task. For locomotion on sparse feasible contact regions, Walk the PLANC [21] coordinates balance, foothold placement, and step timing on constrained terrains such as stepping stones, beams, and planks, where small contact or timing errors may cause irrecoverable failure. 

For fall recovery, FR-Net [22] addresses incomplete terrain perception and uncertain interactions on challenging surfaces through explicit mass-contact prediction, enabling quadrupedal recovery across diverse terrains, including steep stairs. Terrain interaction is equally critical for humanoid standing-up and fall-recovery control. HumanUP [4] extends humanoid getting-up to deformable, slippery, and inclined terrains. Its experiments show that the robot may partially rise on grass slopes and snow-covered surfaces, but subsequently fall because of unstable foot placement or surface slippage. HoST [1] learns standing-up motions from diverse terrain-supported postures, and its cross-terrain analysis reports higher balancing-energy consumption on sloped terrain. FIRM [10] further unifies fall mitigation and recovery within a single policy and evaluates recovery on flat, uneven, wave, and rough terrains, with recovery success varying substantially across terrain conditions. 

## III. METHOD 

This section presents the UniReLo framework, as illustrated in Fig. 2. We first formulate the unified recoveryto-locomotion control problem and introduce continuously gated multi-scale motion priors for coordinating recovery, support reorganization, and locomotion. We then construct 

terrain-conditioned recovery guidance to evaluate support viability and derive the continuous recovery progress, followed by terrain-pose plasticity-aware initialization for trainingstate sampling. 

## _A. Problem Formulation and Objective_ 

A single policy _πθ_ ( **a** _t |_ **o** _t_ ) maps proprioceptive observations to joint-position targets tracked by a low-level controller. The observation **o** _t_ contains joint positions **q** _t_ , joint velocities **q** ˙ _t_ , projected gravity **g** _t_<sup>_b_,baseangularveloc-</sup> ity **_ω_** _t_ , previous actions, and the velocity command **u** _t_ = [ _v_<sup>cmd</sup> _x,t_<sup>_,v_cmd</sup> _y,t_<sup>_,ω_</sup> _z_<sup>cmd</sup> _,t_<sup>]</sup><sup>_⊤_.</sup> 

Training covers _K_ = _{_ flat _,_ gravel _,_ slope-10<sup>_◦_</sup> _,_ slope-15<sup>_◦_</sup> _}_ . We distinguish the policy observation **o** _t_ , the privileged simulator state **s** _t_ used only for constructing training signals, and the temporal motion windows evaluated by the motionprior branches. 

The policy is optimized with the total reward 


where _Rt_<sup>task</sup> coordinates rising and command tracking, _Rt_<sup>TCG</sup> provides terrain-conditioned recovery guidance, _Mt_<sup>style</sup> denotes the gated motion-prior reward, and _Rt_<sup>reg</sup> collects nonnegative control and safety costs. A continuous recoveryprogress variable _αt ∈_ [0 _,_ 1] coordinates both the task objectives and motion priors. 

## _B. Continuously Gated Multi-Scale Motion Priors_ 

Whole-body recovery, transient support reorganization, and periodic locomotion exhibit distinct temporal structures. A temporally undifferentiated motion prior may therefore obscure their characteristic motion patterns. UniReLo employs three specialized AMP discriminators: a frame-level 


Fig. 3: Continuously gated multi-scale motion priors. Recovery progress _αt_ continuously adjusts the contributions of the frame-, sequence-, and gait-level motion priors. The resulting gates regulate both motion-prior reward fusion and policysample weighting during discriminator training. 

branch Φframe operating on a single frame, a sequence-level branch Φseq operating on a five-frame window, and a gaitlevel branch Φgait operating on a ten-frame window. The branches share the same architecture but have independent parameters. 

The frame branch evaluates instantaneous posture consistency, the sequence branch captures short-horizon recovery and support-reorganization dynamics, and the gait branch evaluates longer-horizon locomotion regularity. 

Let _I_ = _{_ frame _,_ seq _,_ gait _}_ . The normalized gate vector is 


where **g** _t_ = [ _g_ frame( _αt_ ) _, g_ seq( _αt_ ) _, g_ gait( _αt_ )]<sup>_⊤_</sup> . The gates remain nonnegative and satisfy ∑ _i∈I gi_ ( _αt_ ) = 1. For branch _i_ , the least-squares motion-prior reward is 


where _Hi ∈{_ 1 _,_ 5 _,_ 10 _}_ is the temporal horizon of the corresponding branch. The gated motion-prior reward is 


Frame-level supervision is emphasized during early recovery, sequence-level supervision becomes prominent during support reorganization, and gait-level supervision gradually dominates after locomotion is established. Their overlapping activation avoids fixed recovery-to-locomotion thresholds. 

The same gates also regulate discriminator specialization. For branch _i_ , the policy-generated component of the discriminator objective is 


Fig. 4: Terrain-conditioned recovery guidance. Active footcontact corners _Ct_ are projected onto the local terrain tangent plane to construct the support representation _Sξ ,t_ . Green dots denote foot-contact corners, purple hollow markers identify representative non-foot support sites, and the red dot denotes the projected center of mass. Signed support margin, contact redundancy, terrain-dependent knee configuration, foot slip, and downhill drift jointly determine recovery viability and the continuous progress variable _αt_ . 


Here, _Bπ_ is the policy-motion buffer. Reference windows remain unweighted and follow the standard least-squares AMP objective [3]. Consequently, each discriminator focuses on policy segments consistent with its temporal specialization, while the three gated rewards jointly update the shared actor. 

## _C. Terrain-Conditioned Recovery Guidance_ 

Recovery progress should reflect compatibility with stable locomotion under the current terrain rather than body elevation alone. As illustrated in Fig. 4, UniReLo constructs a terrain-relative support representation, evaluates the resulting support state, and maps its recovery viability to the continuous progress variable _αt_ . 

_a) Terrain-Relative Support Representation.:_ Let _Ct_ denote the active foot-contact corners. Following Steps 1–3 in Fig. 4, their terrain-relative projection, support representation, and signed support margin are 


Here, Π _ξ_ ( _·_ ) projects onto the local terrain tangent plane and conv( _·_ ) constructs the convex support representation. The signed margin is positive when the projected CoM lies inside _Sξ ,t_ and negative otherwise. 

_b) Support Feasibility Assessment.:_ Early recovery may exploit multi-contact support, whereas late recovery requires a terrain-compatible bipedal configuration. Candidate support sites include the feet and the representative non-foot sites shown in Fig. 4. A site _j_ is considered load bearing according to 


where **f**<sup>_w_</sup> _j,t_<sup>isitsworld-framecontactforceand</sup><sup>**n**</sup><sup>_w_</sup> _ξ ,t_<sup>isthe</sup> terrain normal. The resulting contact-redundancy count is _nt_<sup>_c_= ∑</sup><sup>_N_</sup> _j_ =<sup>_s_</sup> 1<sup>_cj,t_. The purple markers in Fig. 4 therefore identify</sup> candidate non-foot support sites rather than contacts assumed to remain active throughout recovery. Let _hξ ,t_ denote terrain-relative base height and _ot_ denote uprightness relative to the terrain normal. The transition from early multi-contact recovery to late bipedal support is controlled by _ζt_ = sigmoid( _kh_ ( _hξ ,t − hs_ ) + _ko_ ( _ot − os_ )). The knee error _e_<sup>knee</sup> is the summed squared distance of _ξ ,t_ the two knee angles from their terrain-dependent admissible intervals. 

Slip and downhill drift are evaluated in the same worldframe terrain tangent plane. Let **P**<sup>_∥_</sup> _ξ ,t_<sup>=</sup><sup>**I**3</sup><sup>_−_</sup><sup>**n**</sup> _ξ_<sup>_w_</sup> _,t_<sup>(</sup><sup>**n**</sup><sup>_w_</sup> _ξ ,t_<sup>)</sup><sup>_⊤_be</sup> the tangent-plane projector, and let **d**<sup>_w_</sup> _ξ ,t_<sup>bethenormalized</sup> projection of gravity onto that plane. For each foot _b ∈ {L, R}_ , _cb,t_ is determined using the same terrain-normal load criterion as _c j,t_ . The motion-stability errors are 


Both terms use velocities expressed in the world frame and projected onto the same terrain tangent plane. Let _χξ_ = 1 for inclined terrain and _χξ_ = 0 otherwise. The support-feasibility reward corresponding to Step 4 is 


The first term encourages redundant support during early recovery, whereas the second evaluates locomotioncompatible bipedal support. 

_c) Recovery Viability and Progress.:_ We collect the support-margin deficit, knee-range violation, foot slip, terrain-relative height deficit, uprightness deficit, and slopedependent downhill drift in a nonnegative error vector **e** _ξ ,t_ . Its six entries are [ _m_<sup>_∗_</sup> _− m_<sup>sup</sup> _ξ ,t_<sup>]+,</sup><sup>_e_</sup> _ξ_<sup>knee</sup> _,t_<sup>,</sup><sup>_e_slip</sup><sup>_,t_,[</sup><sup>_h∗−hξ,t_]+,</sup> [ _o_<sup>_∗_</sup> _− ot_ ]+, and _χξ e_<sup>down</sup> _ξ ,t_ , respectively. Recovery viability is represented by the weighted energy 


TABLE I: Task and regularization weights used in UniReLo. 

|**Term**|**Weight**|
|---|---|
|Terrain-relative height|4_._5|
|Body uprightness|1_._0|
|Linear-velocity tracking|0_._65|
|Yaw-rate tracking|1_._0|
|Action variation|0_._015|
|Joint velocity|2_._5_×_10<sup>_−_7</sup><br>|
|Joint torque|2_._5_×_10<sup>_−_6</sup>|
|Joint-limit violation|100|
|Undesired collision|1_._0|


Lower _Eξ ,t_ indicates greater compatibility with stable locomotion. The viable recovery-state set is _Rξ_ = _{_ **s** : _Eξ_ ( **s** ) _≤ E_ tol _}_ . 

The guidance reward and recovery progress are defined as 


Thus, _αt_ increases as the robot approaches a terraincompatible state capable of sustaining subsequent locomotion. Recovery progress also coordinates the transition between rising and command tracking: 


Here, _Rt_<sup>rise</sup> rewards terrain-relative base height and uprightness, whereas _Rt_<sup>cmd</sup> rewards tangent-plane linear-velocity and yaw-rate tracking. The same _αt_ controls the multi-scale motion-prior gates in Eq. (2). 

_D. Terrain-Pose Plasticity-Aware Initialization_ 

Uniform initialization may overrepresent trivial poses or infeasible terrain–pose pairs. UniReLo therefore prioritizes fallen configurations whose recoverability is sensitive to terrain conditions. 

A fallen-pose template is represented as **_ψ_** _j_ = [ **q** _j,_ **g**<sup>_b_</sup> _j_<sup>_,θ_rel</sup> _j_<sup>_,_</sup><sup>**v**0</sup><sup>_,j,_</sup><sup>**_ω_**0</sup><sup>_,j_],</sup> where _θ j_<sup>rel</sup> denotes the body orientation relative to the local terrain surface. Its terraindependent plasticity is measured by 


where _p_ ˆ _j,ξ_ is the empirical recovery-success probability. A larger _I j_ indicates stronger terrain-dependent variation in recoverability. 

Terrain–pose pairs are sampled according to 


where _V_<sup>ˆ</sup> _j,ξ ∈_ [0 _,_ 1] is the normalized moving-average return and _N j,ξ_ is the visitation count. This distribution emphasizes challenging, terrain-sensitive, and underexplored initial states. 

All terrain-dependent quantities and motion discriminators are used only during training; deployment retains the proprioceptive actor and low-level joint-position controller. 


Fig. 5: Elevation distributions within the foot-contact regions of the four simulated terrains. Elevations are expressed relative to the mean of each local region. Flat ground exhibits nearly uniform elevation, gravel contains stochastic local variations, and the two inclined terrains exhibit consistent forward elevation gradients. The 10<sup>_◦_</sup> and 15<sup>_◦_</sup> slope panels use the same color range to enable direct comparison of their gradient magnitudes. 

## IV. EXPERIMENTS 

We evaluate UniReLo from four perspectives: recovery robustness across representative field terrains, terrainconditioned recovery behavior, the contribution of the proposed components, and sim-to-real transfer to outdoor environments. For fair comparison with existing standing-up methods, the baseline evaluation adopts a zero-command getup-to-stand protocol. The ablation and hardware evaluations further use continuous commands to assess the complete transition from fallen states to sustained locomotion. 

## _A. Experimental Settings_ 

_a) Simulation and Terrain Setup.:_ Training and evaluation are conducted on flat ground, gravel, and planar slopes of 10<sup>_◦_</sup> and 15<sup>_◦_</sup> . These terrains represent rigid structured support, locally irregular contact, and increasingly inclined support conditions, respectively. Their elevation distributions and longitudinal profiles within the local foot-contact region are shown in Figs. 5 and 6. 

_b) Implementation Details.:_ UniReLo and its ablated variants are trained using PPO [23] with 4,096 parallel environments at a control frequency of 50 Hz. The policy input contains a five-frame proprioceptive history. The PPO optimizer uses a learning rate of 3 _×_ 10<sup>_−_4</sup> , a clipping ratio of 0 _._ 2, a GAE parameter of _λ_ = 0 _._ 95, and a discount factor of _γ_ = 0 _._ 99. 


Fig. 6: Longitudinal elevation profiles obtained by averaging the mean-centered local heightfield along the lateral direction. The horizontal axis denotes the forward position within the foot-contact region. The vertical axis, labeled _ROI mean_ , denotes the lateral mean elevation at each forward position relative to the mean elevation of the complete ROI. Flat ground remains near zero, gravel exhibits irregular local fluctuations, and the inclined terrains produce approximately linear profiles whose gradients increase with slope angle. 

Domain randomization is applied to link masses, joint damping, contact friction, observation noise, communication delay, external disturbances, and terrain properties. On gravel, surface-height perturbations are sampled within _±_ 0 _._ 02 m and friction coefficients are sampled from _U_ (0 _._ 3 _,_ 0 _._ 6). The inclined terrains are planar surfaces with fixed inclination angles. 

_c) Baseline Evaluation Protocol and Metrics.:_ For comparison with existing humanoid fall-recovery methods, all policies are evaluated under a unified get-up-to-stand protocol with zero linear and angular velocity commands. This protocol evaluates whether the robot can recover and maintain a stable upright state without requiring commandfollowing locomotion. We report Success Rate (SR), Timeto-Stand (TTS), and Time-to-Fall (TTF). 

- 1) **Success Rate (SR, %):** The percentage of trials in which the robot recovers from the fallen state and reaches the prescribed stable-upright condition. 

- 2) **Time-to-Stand (TTS, s):** The elapsed time from policy activation until the stable-upright condition is first established. TTS is evaluated only over successful trials. 

- 3) **Time-to-Fall (TTF, s):** The elapsed time from the first stable-upright instant to a secondary fall. TTF is evaluated only for trials in which the robot first reaches the upright condition and subsequently loses balance. 

We compare UniReLo with HumanUP [4], HoST [1], and FIRM [10]. All methods are implemented and evaluated using the same full 29-DoF Unitree G1 rigid-body model. To preserve their original control formulations, each baseline retains the actively controlled joint set adopted in its original implementation. Joints outside a baseline’s policy interface are held at their nominal positions through low-level PD control. 

The baseline-specific network architectures, learning objectives, reward organizations, and training procedures are retained according to their original formulations. Only simulator-dependent interfaces and robot-specific mappings are adapted to the common platform. During evaluation, all methods use the same terrain configurations, balanced initial-posture distributions, episode horizon, stable-upright criterion, and evaluation procedure. 

All methods are evaluated over prone, supine, and side initial postures. Results are reported as the mean and standard deviation over five independent random seeds, with 200 trials conducted for each posture–terrain combination under every seed. 

## _B. Simulation Evaluation_ 

_a) Comparison with Existing Recovery Methods.:_ Table II reports aggregate results under the unified zerocommand get-up-to-stand protocol. On flat ground, all methods achieve relatively strong recovery performance. HoST obtains the shortest TTS, whereas FIRM and UniReLo exhibit no secondary fall within the evaluation horizon. 

The differences become more pronounced as terrain complexity increases. FIRM performs best among the prior methods on gravel, while HoST remains the strongest baseline on inclined terrain. UniReLo nevertheless achieves the highest SR under every evaluated terrain condition. Relative to the strongest baseline on each terrain, UniReLo provides relative SR improvements of 8 _._ 3% on gravel, 11 _._ 8% on the 10<sup>_◦_</sup> slope, and 69 _._ 0% on the 15<sup>_◦_</sup> slope. Its TTS remains within 1 s of the fastest method on flat ground and is the lowest on gravel and both slopes. 

On the 15<sup>_◦_</sup> slope, representative unsuccessful baseline trials reach an approximately upright posture but subsequently exhibit foot sliding or downhill drift. In contrast, UniReLo maintains substantially higher recovery success and longer post-standing stability. These results support evaluating the terrain compatibility of the recovered support state rather than body elevation alone. 

_b) Recovery Progress and Terrain-Dependent Signals.:_ Fig. 7 examines the recovery dynamics under the four terrain conditions. The recovery progress _αt_ , produced by the terrain-conditioned recovery guidance, increases as the robot approaches a terrain-compatible locomotion-ready state. Meanwhile, the base-tilt magnitude decreases as the whole-body posture and contact configuration are reorganized. 

The inclined terrains retain nonzero steady-state tilt because the recovered posture aligns with the terrain rather than with a nominal flat-ground configuration. The local height statistic _σh,t_ distinguishes the underlying terrain structures: flat ground remains nearly uniform, gravel contains stochastic local variation, and planar slopes produce variation that increases with inclination. Here, _σh,t_ is a diagnostic terrain statistic rather than the direct definition of _αt_ ; recovery progress is determined by the combined support, posture, and motion feasibility introduced in Sec. III-C. 


Fig. 7: Temporal evolution of recovery progress _αt_ , base-tilt magnitude _∥_ **g** _t_<sup>_b_</sup> _,xy_<sup>_∥_2,andlocalcontact-regionheightvariation</sup> _σh,t_ across flat ground, gravel, and the 10<sup>_◦_</sup> and 15<sup>_◦_</sup> slopes. Solid curves denote mean trajectories, shaded regions indicate variability, and the insets show representative contact configurations. The terrain-height statistic is used only for analysis and is not part of the deployed actor observation. 

_c) Terrain-Compatible Recovery Behaviors.:_ Fig. 8 shows that the recovered configuration changes with terrain instead of converging to one nominal standing posture. Flat ground permits a relatively direct transition into locomotion. On gravel, the policy performs persistent foot-placement adjustments and maintains a more compliant posture to accommodate irregular support. On slopes, the robot increases knee flexion and aligns its body configuration with the terrain gradient, with stronger adaptation on the 15<sup>_◦_</sup> slope. 

These behaviors are consistent with the terrain-dependent knee configuration and support-feasibility assessment used by the terrain-conditioned recovery guidance. Recovery therefore targets a terrain-compatible support configuration from which command-following locomotion can be sustained. 

## _C. Ablation Study_ 

_a) Variants and Evaluation Protocol.:_ All ablation variants are evaluated with a constant forward-velocity command of 0 _._ 25 m/s and zero lateral-velocity and yaw-rate commands. Unlike the zero-command baseline protocol, this setting evaluates the complete process from fall recovery to sustained command tracking. 

We evaluate four variants: 

- 1) **w/o TCG (without terrain-conditioned recovery guidance)** , which removes the reward-shaping branch of terrain-conditioned recovery guidance, including _Rt_<sup>feas</sup> and the potential-based energy-reduction term. The recovery energy _Eξ ,t_ is retained only for computing _αt_ , thereby preserving task blending and continuous motion-prior gating. 

TABLE II: Simulation comparison with existing humanoid recovery methods under the zero-command get-up-to-stand protocol. 

|Method||Flat|||Gravel|||Slope 10<sup>_◦_</sup>|||Slope 15<sup>_◦_</sup>||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||SR_↑_|TTS_↓_|TTF_↑_|SR_↑_|TTS_↓_|TTF_↑_|SR_↑_|TTS_↓_|TTF_↑_|SR_↑_|TTS_↓_|TTF_↑_|
|HoST [1]|92_._12_±_0_._68|**1**_._**82**_±_**0**_._**06**|0_._15_±_0_._21|23_._45_±_1_._62|3_._28_±_0_._74|1_._41_±_1_._18|83_._40_±_2_._35|2_._98_±_0_._42|1_._85_±_0_._55|52_._91_±_2_._47|3_._68_±_0_._61|0_._92_±_0_._48|
|FIRM [10]|90_._56_±_0_._82|2_._58_±_0_._54|N/A|89_._74_±_1_._35|3_._05_±_0_._91|1_._62_±_1_._06|57_._20_±_2_._48|3_._55_±_0_._72|1_._12_±_0_._86|40_._30_±_2_._98|4_._28_±_0_._83|0_._68_±_0_._59|
|HumanUP [4]|89_._85_±_0_._48|6_._18_±_0_._26|0_._37_±_0_._19|61_._30_±_1_._78|6_._84_±_0_._65|0_._88_±_0_._72|53_._83_±_2_._27|6_._72_±_0_._48|0_._78_±_0_._42|15_._20_±_2_._61|6_._35_±_0_._72|0_._35_±_0_._28|
|**UniReLo (Ours)**|**99**_._**53**_±_**0**_._**35**|2_._35_±_0_._08|N/A|**97**_._**18**_±_**0**_._**33**|**2**_._**13**_±_**0**_._**93**|N/A|**93**_._**28**_±_**0**_._**31**|**2**_._**76**_±_**0**_._**32**|**3**_._**06**_±_**0**_._**40**|**89**_._**42**_±_**0**_._**26**|**3**_._**57**_±_**0**_._**79**|**2**_._**14**_±_**0**_._**63**|


“N/A” indicates that no secondary fall occurred within the evaluation horizon. 


### (b) 10<sup>_◦_</sup> slope (top) and 15<sup>_◦_</sup> slope (bottom). 

Fig. 8: Qualitative recovery and command-following sequences across heterogeneous simulated terrains. On gravel, the red boxes highlight persistent foot-placement adjustments under irregular contact. On inclined terrain, the highlighted configurations show increasing knee flexion and terrain-aligned whole-body adaptation as the slope angle increases. The background stage labels are included only for visualization and do not represent internal policy modes or explicit switching conditions. 

- 2) **w/o TPP Init.** , which replaces terrain-pose plasticityaware initialization with uniform sampling over terrains and fallen-pose templates. 

- 3) **Single-scale AMP** , which replaces the multi-scale discriminator bank with one AMP discriminator trained on the complete recovery-to-locomotion sequence without temporal-scale decomposition. 

- 4) **Hard-gated Routing** , which replaces continuous 

progress-dependent blending with one-hot prior selection: 


the one-hot weights replace _gi_ ( _αt_ ) in both motion-prior reward fusion and policy-sample weighting during discriminator training. 


Fig. 9: Continuous gating versus Hard-gated Routing on a 10<sup>_◦_</sup> slope under the continuous-command protocol. UniReLo maintains smooth forward-velocity and pelvic-pitch evolution from recovery to sustained command tracking. Hard-gated Routing introduces an abrupt dominant-prior change, followed by velocity and pelvic-pitch oscillations and eventual instability. The marked region indicates the routing change of the hard-gated variant. The colored backgrounds denote visualization-only behavior intervals and do not represent internal modes of UniReLo. 

The baseline comparison in Table II evaluates get-up-tostand performance under a zero command. In contrast, the ablation study adopts a stricter recovery-to-tracking criterion under a continuous command. 

We report the _Recovery-to-Tracking Success Rate_ (RTSR). A trial is successful only if the policy recovers, establishes sustained command tracking, and avoids a secondary fall within the evaluation horizon. We also report the _Average Signed Support Margin_ (ASM) and the _Command Tracking Error_ (CTE): 


Here, _Tu_ denotes the interval after the first stable-upright instant, whereas _Tc_ denotes the subsequent commandevaluation interval. ASM measures terrain-relative support robustness and is reported in centimeters. CTE measures normalized planar-velocity and yaw-rate tracking errors. ASM and CTE are computed only for trials reaching the corresponding evaluation intervals, while unsuccessful trials are reflected by RTSR. 

_b) Effect of Continuous Multi-Scale Gating.:_ Having examined how terrain-conditioned recovery guidance produces _αt_ , we next evaluate how this shared progress variable coordinates the multi-scale motion priors. Fig. 9 compares UniReLo and Hard-gated Routing from the same prone configuration on a 10<sup>_◦_</sup> slope. 

UniReLo smoothly changes the contributions of the frame, sequence-, and gait-level priors as _αt_ evolves. In contrast, discrete prior replacement creates a discontinuity near the routing boundary, followed by pronounced forward-velocity and pelvic-pitch oscillations and a secondary fall. This result 

directly illustrates the transition instability that continuous progress-dependent gating is designed to avoid. 

_c) Quantitative Ablation Results.:_ Table III reports posture-resolved results under matched training and evaluation conditions. Full UniReLo achieves the best RTSR, ASM, and CTE under every evaluated terrain and initial-posture group. Averaged over prone, supine, and side postures, its RTSR reaches 98 _._ 0%, 97 _._ 1%, 93 _._ 3%, and 89 _._ 2% on flat ground, gravel, the 10<sup>_◦_</sup> slope, and the 15<sup>_◦_</sup> slope, respectively. Removing terrain-pose plasticity-aware initialization causes the largest RTSR reduction. The posture-averaged reduction increases from 5 _._ 60 percentage points on flat ground to 24 _._ 03 percentage points on the 15<sup>_◦_</sup> slope, indicating that terrain-sensitive fallen-state sampling becomes increasingly important as recovery difficulty grows. 

Removing terrain-conditioned recovery guidance mainly degrades ASM and subsequent command tracking. Compared with the full model, the posture-averaged ASM decreases by 0 _._ 52 cm, 0 _._ 79 cm, 1 _._ 02 cm, and 1 _._ 24 cm across the four terrain conditions. The same variant also produces the largest overall CTE, showing that unsuitable support configurations directly affect the resumption of commanded locomotion. 

Single-scale AMP and Hard-gated Routing both reduce RTSR and increase CTE. The former removes temporal specialization, whereas the latter removes continuous coordination among the three motion priors. Together with Fig. 9, these results support both multi-scale temporal supervision and continuous progress-dependent gating. 

## _D. Real-World Evaluation_ 

The simulation-trained UniReLo policy is deployed on a physical 29-DoF Unitree G1 humanoid. The evaluation includes indoor flat ground, outdoor gravel, outdoor grass, 

TABLE III: Posture-resolved component ablation across four terrains under the continuous-command evaluation protocol. Values are reported as the mean and standard deviation over five random seeds, with 200 trials conducted for each posture– terrain combination under every seed. 

|Variant||Flat|||Gravel|||Slope 10<sup>_◦_</sup>|||Slope 15<sup>_◦_</sup>||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||RTSR_↑_|ASM_↑_|CTE_↓_|RTSR_↑_|ASM_↑_|CTE_↓_|RTSR_↑_|ASM_↑_|CTE_↓_|RTSR_↑_|ASM_↑_|CTE_↓_|
|**(1) Prone Initial Po**|**stures**||||||||||||
|w/o TCG|96_._4_±_0_._89|2_._94_±_0_._31|0_._22_±_0_._08|89_._8_±_1_._86|2_._11_±_0_._11|0_._33_±_0_._04|81_._3_±_1_._57|1_._58_±_0_._19|0_._39_±_0_._12|71_._5_±_0_._91|0_._87_±_0_._28|0_._44_±_0_._08|
|w/o TPP Init|93_._2_±_1_._72|3_._15_±_0_._25|0_._19_±_0_._03|84_._4_±_0_._65|2_._41_±_0_._16|0_._29_±_0_._08|77_._2_±_1_._58|2_._11_±_0_._38|0_._34_±_0_._11|66_._3_±_1_._57|1_._54_±_0_._25|0_._39_±_0_._10|
|Single-scale AMP|96_._1_±_1_._50|3_._19_±_0_._32|0_._18_±_0_._02|92_._3_±_0_._71|2_._58_±_0_._09|0_._27_±_0_._06|84_._1_±_1_._34|2_._30_±_0_._16|0_._32_±_0_._06|75_._2_±_2_._00|1_._71_±_0_._24|0_._36_±_0_._02|
|Hard-gated Routing|97_._9_±_0_._76|3_._26_±_0_._42|0_._17_±_0_._06|93_._6_±_1_._15|2_._63_±_0_._29|0_._26_±_0_._02|85_._7_±_1_._88|2_._32_±_0_._34|0_._30_±_0_._07|77_._0_±_1_._17|1_._77_±_0_._42|0_._35_±_0_._05|
|**Full UniReLo**|**99**_._**6**_±_**0**_._**22**|**3**_._**50**_±_**0**_._**28**|**0**_._**14**_±_**0**_._**04**|**98**_._**4**_±_**0**_._**35**|**2**_._**97**_±_**0**_._**20**|**0**_._**18**_±_**0**_._**03**|**94**_._**8**_±_**0**_._**45**|**2**_._**64**_±_**0**_._**24**|**0**_._**23**_±_**0**_._**02**|**89**_._**1**_±_**0**_._**45**|**2**_._**08**_±_**0**_._**18**|**0**_._**27**_±_**0**_._**09**|
|**(2) Supine Initial P**|**ostures**||||||||||||
|w/o TCG|95_._8_±_0_._57|2_._75_±_0_._16|0_._23_±_0_._03|87_._9_±_1_._43|1_._96_±_0_._17|0_._36_±_0_._08|79_._5_±_1_._84|1_._38_±_0_._10|0_._44_±_0_._08|70_._2_±_1_._14|0_._58_±_0_._11|0_._49_±_0_._12|
|w/o TPP Init|92_._6_±_0_._96|2_._91_±_0_._35|0_._21_±_0_._05|82_._6_±_0_._55|2_._25_±_0_._39|0_._32_±_0_._12|74_._8_±_1_._40|1_._94_±_0_._29|0_._38_±_0_._11|65_._1_±_1_._39|1_._38_±_0_._37|0_._44_±_0_._09|
|Single-scale AMP|95_._4_±_1_._52|2_._98_±_0_._12|0_._20_±_0_._07|90_._3_±_0_._67|2_._41_±_0_._15|0_._30_±_0_._11|82_._9_±_1_._75|2_._10_±_0_._09|0_._37_±_0_._09|73_._6_±_0_._84|1_._53_±_0_._34|0_._41_±_0_._07|
|Hard-gated Routing|96_._2_±_1_._47|3_._05_±_0_._29|0_._19_±_0_._04|91_._4_±_0_._89|2_._46_±_0_._11|0_._28_±_0_._06|83_._4_±_1_._35|2_._17_±_0_._21|0_._31_±_0_._05|75_._8_±_1_._04|1_._52_±_0_._09|0_._37_±_0_._11|
|**Full UniReLo**|**97**_._**8**_±_**0**_._**22**|**3**_._**27**_±_**0**_._**26**|**0**_._**15**_±_**0**_._**02**|**97**_._**2**_±_**0**_._**45**|**2**_._**74**_±_**0**_._**23**|**0**_._**21**_±_**0**_._**05**|**93**_._**2**_±_**0**_._**27**|**2**_._**41**_±_**0**_._**15**|**0**_._**26**_±_**0**_._**07**|**89**_._**4**_±_**0**_._**27**|**1**_._**86**_±_**0**_._**19**|**0**_._**30**_±_**0**_._**10**|
|**(3) Side Initial Post**|**ures**||||||||||||
|w/o TCG|95_._0_±_1_._73|2_._58_±_0_._38|0_._25_±_0_._09|86_._0_±_1_._22|1_._69_±_0_._23|0_._41_±_0_._05|77_._1_±_1_._19|1_._14_±_0_._21|0_._49_±_0_._09|68_._7_±_1_._48|0_._30_±_0_._09|0_._53_±_0_._10|
|w/o TPP Init|91_._5_±_1_._27|2_._75_±_0_._32|0_._22_±_0_._07|80_._7_±_0_._97|1_._98_±_0_._19|0_._36_±_0_._02|72_._8_±_1_._86|1_._70_±_0_._38|0_._43_±_0_._04|64_._2_±_1_._99|1_._15_±_0_._19|0_._48_±_0_._06|
|Single-scale AMP|94_._6_±_1_._34|2_._78_±_0_._27|0_._21_±_0_._05|88_._3_±_1_._15|2_._13_±_0_._40|0_._34_±_0_._03|80_._4_±_1_._92|1_._84_±_0_._37|0_._40_±_0_._03|72_._9_±_1_._43|1_._27_±_0_._31|0_._45_±_0_._09|
|Hard-gated Routing|95_._8_±_1_._10|2_._84_±_0_._42|0_._20_±_0_._04|89_._5_±_1_._58|2_._15_±_0_._22|0_._32_±_0_._12|81_._5_±_1_._64|1_._89_±_0_._16|0_._38_±_0_._12|75_._3_±_1_._80|1_._32_±_0_._17|0_._41_±_0_._05|
|**Full UniReLo**|**96**_._**7**_±_**0**_._**42**|**3**_._**06**_±_**0**_._**22**|**0**_._**16**_±_**0**_._**06**|**95**_._**8**_±_**0**_._**27**|**2**_._**42**_±_**0**_._**25**|**0**_._**27**_±_**0**_._**08**|**91**_._**8**_±_**0**_._**45**|**2**_._**12**_±_**0**_._**17**|**0**_._**27**_±_**0**_._**02**|**89**_._**2**_±_**0**_._**27**|**1**_._**53**_±_**0**_._**14**|**0**_._**36**_±_**0**_._**12**|


and outdoor slopes of 10<sup>_◦_</sup> and 15<sup>_◦_</sup> . Only outdoor grass is absent from the simulation training terrains. All full-model experiments use the same policy checkpoint and deployment parameters without terrain-specific retuning or online terrain labels. 

A sequence is considered successful only if the robot recovers from the fallen state, resumes sustained commandfollowing locomotion, and avoids a secondary fall within the evaluation horizon. 

_a) Real-World Failure Analysis.:_ Fig. 10a shows that discrete routing is sensitive to fluctuations near its predefined transition boundary. Abrupt changes in the dominant motion prior repeatedly drive the robot toward recovery-like actions after it has temporarily become upright. The resulting centerof-mass oscillation eventually causes a secondary fall. 

Fig. 10b shows a different failure mode after removing terrain-conditioned recovery guidance. The robot may reach the target body height, but poorly positioned feet and insufficient terrain-dependent postural adaptation prevent the robot from establishing a terrain-compatible support state for continued locomotion. These cases provide hardware evidence that uprightness alone does not guarantee successful recovery in field environments. 

_b) Field Robustness and Recovery-to-Locomotion.:_ We first evaluate UniReLo under external perturbations during locomotion. As shown in Fig. 1(b), (d), and (f), the robot is 

tested on outdoor grass, outdoor gravel, and a 15<sup>_◦_</sup> outdoor slope. Under moderate disturbances, it maintains locomotion through coordinated whole-body regulation and adaptive foot placement. Under fall-inducing disturbances, it performs whole-body recovery, re-establishes terrain-compatible support, and resumes commanded walking. The grass experiment evaluates transfer to an unseen deformable surface, whereas gravel and inclined terrain evaluate robustness under irregular contact and terrain inclination. 

Fig. 11 jointly presents the qualitative recovery sequences and the corresponding forward-velocity profiles across all five real-world conditions. The image sequences reveal terrain-dependent recovery strategies. Flat ground permits a relatively direct rise into locomotion, whereas gravel requires additional foot-placement adjustments under irregular contact. On grass, the robot adopts more compliant wholebody motion to accommodate the deformable surface. On inclined terrain, UniReLo establishes terrain-compatible support through increased knee flexion, terrain-aligned posture, and a longer stabilization interval. These adaptations become more pronounced as the inclination increases from 10<sup>_◦_</sup> to 15<sup>_◦_</sup> . 

The velocity plots at the bottom further quantify the transition from recovery to command-following locomotion. The colored circular markers associate the trajectories with selected recovery frames shown above. Indoor flat ground and 


(a) Hard-gated Routing. 


(b) w/o TCG. 

Fig. 10: Representative real-world failures after removing key components of UniReLo. (a) Hard-gated Routing produces abrupt behavior near the routing boundary, resulting in discontinuous center-of-mass motion, repeated recovery actions, and secondary falls. Red dots and dashed orange curves indicate approximate center-of-mass positions and trajectories. (b) Removing terrain-conditioned recovery guidance produces insufficient contact and posture adaptation on grass and inclined terrain. Red dashed boxes highlight unstable foot configurations immediately before loss of balance. 

outdoor grass exhibit earlier forward progression, whereas gravel and the inclined terrains require longer support reorganization before sustained locomotion is established. On the 15<sup>_◦_</sup> slope, the robot briefly performs an in-place heading correction after becoming upright, which delays the increase in measured forward velocity despite the continued forward command. Forward locomotion then resumes once the heading is adjusted. 

## V. CONCLUSIONS 

We presented UniReLo, a unified proprioceptive policy for humanoid fall recovery and subsequent locomotion across diverse terrains. Continuously gated multi-scale motion priors coordinate frame-, sequence-, and gait-level supervision according to recovery progress, enabling a smooth transition from whole-body recovery to velocity-commanded locomotion. Terrain-conditioned recovery guidance further encourages the robot to establish terrain-compatible support states 

capable of sustaining continued motion, rather than relying on upright posture alone. Simulation and real-world evaluations demonstrate reliable recovery-to-locomotion transitions, disturbance robustness, and cross-terrain transfer across flat ground, gravel, grass, and inclined terrains without terrain-specific controller switching or parameter retuning. 

Future work will incorporate exteroceptive and tactile sensing and expand the diversity of terrains and motion priors to improve adaptation to deformable and out-of-distribution surfaces. 

## REFERENCES 

- [1] T. Huang, J. Ren, H. Wang, Z. Wang, Q. Ben, M. Wen, X. Chen, J. Li, and J. Pang, “Learning humanoid standing-up control across diverse postures,” in _Robotics: Science and Systems (RSS)_ , 2025. 

- [2] X. B. Peng, P. Abbeel, S. Levine, and M. van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions on Graphics_ , vol. 37, no. 4, pp. 1–14, 2018. 


Fig. 11: Real-world recovery-to-locomotion behaviors and corresponding velocity profiles across five terrain conditions. From top to bottom, the image sequences show recovery and subsequent locomotion on indoor flat ground, outdoor gravel, outdoor grass, and outdoor slopes of 10<sup>_◦_</sup> and 15<sup>_◦_</sup> . Timestamps indicate elapsed time after policy activation. The two plots at the bottom show the measured forward velocity _vx_ and the remote forward-velocity command _v_<sup>cmd</sup> _x_ , respectively. Colored curves denote the five terrain conditions, and circular markers associate the velocity trajectories with selected frames in the image sequences. 

> [3] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “Amp: Adversarial motion priors for stylized physics-based character control,” 

> _ACM Transactions on Graphics_ , vol. 40, no. 4, pp. 1–15, 2021. 

[4] X. He, R. Dong, Z. Chen, and S. Gupta, “Learning getting-up policies 

for real-world humanoid robots,” in _Robotics: Science and Systems (RSS)_ , 2025. 

- [5] I. Mordatch, Z. Popovi´c, and E. Todorov, “Contact-invariant optimization for hand manipulation,” 2012. 

- [6] J. Carius _et al._ , “Trajectory optimization for legged robots with slipping,” _IEEE Robotics and Automation Letters_ , 2021. 

- [7] J. Pratt, J. Carff, S. Drakunov, and A. Goswami, “Capture point: A step toward humanoid push recovery,” in _Proc. IEEE-RAS Int. Conf. Humanoid Robots_ , 2006, pp. 200–207. 

- [8] Q. Gaspard _et al._ , “Frasa: An end-to-end reinforcement learning agent for fall recovery and stand up of humanoid robots,” _arXiv preprint_ , 2024. 

- [9] P. Chen, Y. Wang, C. Luo, W. Cai, and M. Zhao, “Hifar: Multi-stage curriculum learning for high-dynamics humanoid fall recovery,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2025. 

- [10] Z. Xu, Y. Li, K.-Y. Lin, and S. X. Yu, “Unified humanoid fall-safety policy from a few demonstrations,” 2025. 

- [11] E. Vollenweider, M. Bjelonic, V. Klemm, N. Rudin, J. Lee, and M. Hutter, “Advanced skills through multiple adversarial motion priors in reinforcement learning,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , 2023, pp. 5120–5126. 

- [12] C. Lu _et al._ , “Unified walking, running, and recovery for humanoids via state-dependent adversarial motion priors,” _arXiv preprint arXiv:2605.18611_ , 2026. 

- [13] J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter, “Learning quadrupedal locomotion over challenging terrain,” _Science Robotics_ , vol. 5, no. 47, p. eabc5986, 2020. 

- [14] N. Rudin, D. Hoeller, P. Reist, and M. Hutter, “Learning to walk in minutes using massively parallel deep reinforcement learning,” in _Proc. Conf. Robot Learning (CoRL)_ , 2022, pp. 91–100. 

- [15] I. M. A. Nahrendra, B. Yu, and H. Myung, “DreamWaQ: Learning robust quadrupedal locomotion with implicit terrain imagination via deep reinforcement learning,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , 2023, pp. 5078–5084. 

- [16] T. Miki, J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter, “Learning robust perceptive locomotion for quadrupedal robots in the wild,” _Science Robotics_ , vol. 7, no. 62, p. eabk2822, 2022. 

- [17] X. Gu, Y.-J. Wang, X. Zhu, C. Shi, Y. Guo, Y. Liu, and J. Chen, “Advancing humanoid locomotion: Mastering challenging terrains with denoising world model learning,” in _Robotics: Science and Systems XX_ , Delft, The Netherlands, 2024. 

- [18] I. Radosavovic, Z. Cao, A. Prabhu, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath, “Learning humanoid locomotion over challenging terrain,” 2024. 

- [19] W. Sun, L. Chen, Y. Su, B. Cao, Y. Liu, and Z. Xie, “Learning humanoid locomotion with world model reconstruction,” _arXiv preprint arXiv:2502.16230_ , 2025. 

- [20] W. Sun, B. Cao, L. Chen, Y. Su, Y. Liu, Z. Xie, and H. Liu, “Learning perceptive humanoid locomotion over challenging terrain,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2025, pp. 6571–6578. 

- [21] M. Dai, W. D. Compton, J. Li, L. Yang, and A. D. Ames, “Walk the PLANC: Physics-guided RL for agile humanoid locomotion on constrained footholds,” _arXiv preprint arXiv:2601.06286_ , 2026. 

- [22] Y. Lu, Y. Dong, J. Zhang, J. Ma, and P. Lu, “FR-Net: Learning robust quadrupedal fall recovery on challenging terrains through mass-contact prediction,” _IEEE Robotics and Automation Letters_ , vol. 10, no. 7, pp. 6632–6639, 2025. 

- [23] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” 2017. 

