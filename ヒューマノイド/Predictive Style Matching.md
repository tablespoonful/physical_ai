---
title: "Predictive Style Matching: Natural and Robust Humanoid Locomotion"
date: "2026-06-05"
authors: "Simeon Nedelchev; Ekaterina Chaikovskaia; Egor Davydenko; Eduard Zaliaev; Roman Gorbachev"
url: https://arxiv.org/abs/2606.07083
pdf: https://arxiv.org/pdf/2606.07083
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.07083)** / [論文ページ](https://arxiv.org/abs/2606.07083)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Predictive Style Matching: Natural and Robust Humanoid Locomotion** 

Simeon Nedelchev<sup>1</sup><sup>_,_2</sup> , Ekaterina Chaikovskaia<sup>1</sup> , Egor Davydenko<sup>1</sup> , Eduard Zaliaev<sup>3</sup> , and Roman Gorbachev<sup>1</sup> 

**_Abstract_ — Reinforcement learning has become the prevailing approach to humanoid locomotion control: policies transfer reliably from simulation to hardware and recover gracefully from disturbances. Motion quality, however, still lags behind: task-only rewards often converge to stiff, asymmetric gaits, while motion imitation methods improve appearance but become more sensitive to external disturbances because reference signals can oppose the transient poses needed to regain balance. We propose** **_Predictive Style Matching_ (PSM), in which an offline predictor maps the robot’s lower-body state history and velocity commands to interpretable upper-body joint and gait targets that shape the rewards during training. Because the targets are state-conditioned rather than time-indexed and the predictor is used only at training time, the deployed controller inherits the proprioceptive interface and inference cost of a task-only RL baseline. On the Unitree G1, in both simulation and hardware, PSM reduces upper-body style error by roughly an order of magnitude over task-only RL while preserving its fall-recovery rate, whereas the motion-imitation baseline attains the lowest style error but fails to recover from disturbances about five times as often.** 


Fig. 1: Human-like whole-body locomotion on the Unitree G1 with PSM (hardware). Under a fixed velocity command, the deployed policy autonomously produces coordinated arm swing, pelvis motion, and natural stepping, while retaining the inference cost of a vanilla task-only controller 

# I. INTRODUCTION 

Reinforcement learning (RL) has become a standard tool for contact-rich legged locomotion. Massively parallel simulation now trains policies in minutes and seamlessly transfers them to hardware [1], [2]. Recent RL-based controllers can recover from pushes, traverse difficult terrain, and track increasingly dynamic whole-body behaviors [3]–[11]. Yet hardware capability has outpaced motion quality: velocity and balance tracking rewards rarely specify how the torso, arms, and pelvis should coordinate during ordinary walking. 

If left underspecified, task-only policies converge to stiff, asymmetric gaits that maximize reward but look unnatural [1], [12]. Hand-tuned shaping penalties and reward curricula [1], [13] mitigate the symptoms but do not encode a compact model of whole-body human coordination. 

Human motion data is a more principled source of regularization, but its use during training and deployment matters. Motion imitation methods such as DeepMimic [14] and its successors (e.g., ZEST, ASAP) [8], [10], [15] drive RL 

This research was supported by the Ministry of Economic Development of the Russian Federation (Agreement No. 139-15-2025-013 with MIPT, dated June 20, 2025. IGK 000000C313925P4B0002). 

> 1Moscow Institute of Physics and Technology (MIPT), Dolgoprudny, Moscow Region, Russia 

> 2Innopolis University, Innopolis, Russia 

> 3Sber Robotics Center, Moscow, Russia Project page, videos, and supplementary material: https: //simeon-ned.github.io/predictive-style-matching/. 

training with time-indexed pose matching against motioncapture or video clips; deployed policies use phase signals in the observation space or explicit reference inputs to continue tracking the task rewards when balance is eventually regained. Adversarial motion priors (AMP) [12], [16] avoid a reference clock by scoring simulated state transitions with a learned discriminator, but the feedback is a scalar over the full state: it is not tied to specific joints or interpretable gait statistics, and it constrains contacts and leg motions to strictly follow task rewards during recovery. 

A complementary line of work from physics-based character animation and game development learns _generative_ motion models—diffusion, autoregressive, and adversarial latent policies—for rich kinematic synthesis and interactive steering [17]–[21]. Coupled with simulation, these models increasingly close the loop to deployable whole-body skills [22], [23], but they target a different operating point: generated samples are less direct to convert into named per-joint/gait reward terms, iterative sampling is expensive inside massively parallel RL, and hardware controllers still favor low-latency proprioceptive inference. We therefore use a lightweight _discriminative_ predictor as a train-time style oracle; unlike imitation, AMP, or generative priors alone, it provides a _command-conditioned map from current lowerbody motion_ to the upper-body and gait targets needed by a recovery-aware controller. 


Fig. 2: Stage 1 (predictor training): offline supervised learning of _fϕ_ on retargeted dataset clips. Lower-body history and command cues are preprocessed into conditioning inputs, while upper-body joints and gait descriptors provide targets; the GRU–MLP predictor is trained with reconstruction and left–right symmetry losses, then frozen. 

This leaves a familiar training-time trade-off: vanilla velocity tracking RL policies are robust under disturbance but have no explicit reward for natural arm swinging or stepping rhythm, while motion imitation prioritizes the desired appearance at the cost of recovery quality [10], [14]. The question we address is how to inject human coordination into RL training without adding a reference generator at deployment or forcing the policy to chase style targets that oppose recovery. 

We propose _Predictive Style Matching_ (PSM), a twostage pipeline that keeps rich style supervision in training while preserving a policy-only deployment interface. Stage 1 trains an offline predictor _fϕ_ to map lower-body history and command cues to interpretable upper-body and gait targets; Stage 2 uses frozen predictions as reward terms during PPO training, so deployment remains the same proprioceptive actor as vanilla RL, without running _fϕ_ . Concretely, this paper contributes: 

- **Motion predictor** _fϕ_ conditioned on lower-body state and velocity command, trained offline on retargeted human walking data, that emits _interpretable_ style targets: 17 upper-body joint angles and a set of gait/body descriptors rather than a time-indexed pose or an abstract scalar discriminator score. 

- **Training pipeline** in which the frozen _fϕ_ outputs are used solely through matching rewards on top of a standard locomotion task reward setup, leaving the deployed controller with the same proprioceptive interface and inference cost as a task-only RL baseline. 

- **Controlled comparison.** A simulation and hardware evaluation on the Unitree G1 against vanilla locomotion and a motion-imitation baseline under matched MDP, domain randomization, curriculum, and distur- 

bance schedules, showing that PSM can bridge the naturalness gap between motion-conditioned and robust vanilla policies. 

# II. PREDICTIVE STYLE MATCHING 

We now turn that motivation into a concrete training pipeline. PSM keeps style supervision in training while preserving a policy-only deployment interface in two stages: Stage 1 learns an offline predictor _fϕ_ from retargeted walking data, and Stage 2 uses its frozen outputs as matching rewards during PPO training of _πθ_ . As a result, the deployed controller remains the same proprioceptive actor as vanilla RL, without a phase clock, reference clip, or predictor network at run time. This separation lets us compare style quality and disturbance recovery under a matched training setup, rather than changing the deployment interface across methods. Figs. 2 and 3 summarize these two stages, detailed in Secs. II-A and II-B. 

# _A. Motion predictor_ 

We begin with the offline stage: _fϕ_ is fit by supervised learning on retargeted human walking, with no RL in the loop. We assemble corpus _D_ from BoneSeed [24]: a walking subset ( _∼_ 10% of available clips) is retargeted to the Unitree G1 and used to learn the map 


where _Ht_ is a rolling, normalized history of lower-body joint angles, optional root-frame foot positions, and yaw-aligned root velocities, and **c** _t_ collects short-horizon velocity command cues. On the G1, **q** ˆ<sup>up</sup> _t_ contains _N_ up=17 joint angles (waist yaw/roll/pitch; left and right shoulder pitch/roll/yaw; left and right elbow; left and right wrist roll/pitch/yaw), and **b**<sup>ˆ</sup> _t_ collects step length, step width, left/right foot pitch, 


Fig. 3: Stage 2 (RL with predictive style matching): PPO trains actor–critic policies in simulation while querying the frozen _fϕ_ on rolling lower-body and command buffers. Predicted upper-body and gait targets define matching rewards that are added to locomotion rewards during training only; deployment keeps a standard proprioceptive actor without running the predictor. 

left/right foot yaw relative to the root, root height, and predicted duty cycle (double-support fraction). These are physically interpretable targets, not a latent style code; a qualitative predictor visualization shows _fϕ_ forecasting the upper body (red ghost) from lower-body motion alone. 

Inputs and network architecture are specified next (Sec. IIB uses _Th_ =25, _Tp_ =10 at 50 Hz when _fϕ_ is queried online). The rolling history _Ht_ bundles three synchronized signals over the last _Th_ control steps: lower-body joint angles **q**<sup>low</sup> _t ∈_ R<sup>_N_low</sup> ( _N_ low=8 hip/knee joints), left and right foot positions in the root frame, **p**<sup>foot</sup> _t ∈_ R<sup>6</sup> , and root linear and angular velocity in the yaw-aligned frame, **v** _t_ =( _vx, vy, ωz_ ), stacked as **V** _t−Th_ +1: _t ∈_ R<sup>_Th×_3</sup> . The command block **c** _t_ concatenates the current velocity target ( _vx, vy, ωz_ ) with short-horizon trajectory cues: for each lookahead ∆ _∈{_ 15 _,_ 30 _,_ 45 _}_ frames ( _≈_ 0.3–0.9 s), the root-frame displacement, heading direction, and yaw change from _t_ to _t_ +∆. A single-layer GRU encodes the per-step sequence [ **q**<sup>low</sup> _,_ **p**<sup>foot</sup> ] _∈_ R<sup>_Th×_(</sup><sup>_N_low+6)</sup> into a 128-D embedding; root velocity is handled separately, with the temporal mean and most recent value of **V** _t−Th_ +1: _t_ forming a 6-D summary that is concatenated with the 

GRU embedding and **c** _t_ . A two-layer MLP then regresses ( _N_ up+ _N_ b) _· Tp_ denormalized targets— _N_ up=17 upper-body joints and _N_ b=8 gait descriptors at each of the next _Tp_ steps. 

Supervised training minimizes the horizon-averaged squared error on upper-body joints and gait descriptors, regularized by a left–right symmetry term: 


where ( **q**<sup>up</sup> _k_<sup>_⋆_</sup> _,_ **b**<sup>_⋆_</sup> _k_<sup>)aretheground-truthtargetsathorizon</sup> step _k_ drawn from _D_ , and _L_ sym( _ϕ_ ) = �� _fϕ_ ( _σ_ ( _Ht,_ **c** _t_ )) _− σ_ � _fϕ_ ( _Ht,_ **c** _t_ )���22<sup>enforcesequivariancetotheleft–rightmir-</sup> roring operator _σ_ . Concretely, _σ_ reflects the robot across its sagittal plane: left and right joint channels are permuted, with each channel multiplied by _±_ 1 according to its rotation axis (roll/yaw axes flip sign; pitch axes do not), lateral root velocity _vy_ and yaw rate _ωz_ are negated, and trajectory cues that encode lateral displacement or heading change 

receive the same sign flips. We use _λb_ =1 and ramp _λ_ sym linearly from 0 to 0 _._ 1 over the first 2500 updates; input noise (std. 0.01 in normalized coordinates) improves robustness to small sim–mocap mismatch, and light feature regularization discourages unrealistic waist motion, foot orientation, and spurious cadence. We optimize (2) with Adam (learning rate 10<sup>_−_3</sup> , batch size 512, weight decay 10<sup>_−_5</sup> ) for 45k updates with gradient-norm clipping at 1 _._ 0. On a single RTX 4090, training the predictor takes about 60 minutes on the current subset and scales from minutes to a few hours across the dataset sizes we use; the predictor is then frozen for the rest of the pipeline. 

# _B. Embedding in RL_ 

With _fϕ_ fixed, we now turn to how it shapes policy learning in Stage 2 (Fig. 3). We formulate locomotion as an MDP ( _S, A, P, r, γ_ ) and train with on-policy PPO [25] in massively parallel MuJoCo simulation [2]. The G1 policy maps **o** _t_ —IMU, joint state, contacts, command, and the previous action—to joint-position targets executed by lowlevel PD controllers. The shared locomotion reward _rt_<sup>loco</sup> tracks a resampled twist command **u** _t_ in the root-yaw frame and penalizes orientation error, height drift, foot slip, jointlimit violations, action rate, and impacts. Domain randomization covers friction, actuator bias, center-of-mass offset, and external pushes [1], [12]. 

At each simulation step, the lower-body/command buffer is updated, the frozen predictor is queried in recedinghorizon mode, and only the first forecast ( _k_ =0) is used as the instantaneous target (ˆ **q**<sup>up</sup> _t_<sup>_,_ˆ</sup><sup>**b**</sup><sup>_t_)from(1);stylematching</sup> remains disabled until the history buffer has accumulated _Th_ steps. On top of _rt_<sup>loco</sup> , PSM adds per-quantity matching rewards driven by these frozen-predictor outputs. For each upper-body joint _j_ and each gait/body descriptor _bi_ we apply an exponential kernel: 


where the _σ_ ’s set per-quantity tolerances and _bi_ ranges over step width, step length, foot pitch/yaw, root height, and predicted duty cycle. The matching reward and total RL reward are 


The actor reads only standard proprioception; matching enters exclusively through _rt_ . We hold _λ_ match( _k_ )=0 during an initial locomotion-only phase and ramp it up only after balance and recovery behavior are established, so style matching never outweighs the task reward at initialization. During the subsequent style curriculum, _w_ up is raised before the individual gait weights, and the generic hand-designed gaitphase shaping is correspondingly attenuated. The policies 

evaluated in Sec. III use both upper-body and gait terms, including the predicted duty cycle, because explicit gaitdescriptor matching proved more stable than relying on upper-body coupling or a fixed phase clock alone. Training uses _Th_ =25 and _Tp_ =10 at 50 Hz control (200 Hz simulation, decimation 4); only _πθ_ is exported for deployment, and evaluating _fϕ_ on the rolling buffers adds about 10% to RL iteration time on an RTX 4090, while the deployed compute path is identical to vanilla RL. 

Finally, we contrast this construction with two natural alternatives targeting the same problem. Clip-tracking baselines replace _q_ ˆ _j,t_<sup>upin(3)withatime-indexedreferencepose</sup> _qj,t_<sup>refreadfromaclipphaseindex,sothetargetisinde-</sup> pendent of the robot’s recovery state; AMP collapses style supervision to a single discriminator score over whole-state transitions, which neither restricts the signal to an upper-body and gait subset nor decomposes it along the per-quantity axes used at evaluation time. In this sense, PSM treats style as a state-conditioned prior over feasible recovery behavior, not as a trajectory that must be tracked frame by frame. The next section measures both contrasts against PSM under matched training conditions. 

# III. EVALUATION 

We evaluate whether PSM improves whole-body naturalness over task-only RL without sacrificing robustness. The three policies—vanilla RL, Tracking, and PSM—are tested on Unitree G1 in simulation and on hardware under matched MDP, observation space, PPO budget, randomization, curriculum, and disturbance schedules, so differences are attributable to the style signal. Among the three, PSM and vanilla RL share a policy-only proprioceptive deployment interface, whereas Tracking requires a reference phase and a reference pose at run time. Because exhaustive trajectory sweeps are impractical on hardware, scenario plots come from a large simulation batch and the robot executes a representative subset of the same **u** ( _t_ ) schedules (Fig. 1 and the supplementary disturbance video). 

All three policies are trained in the same MJLAB stack [2], with identical PPO settings, observation space, and reward scaffolding, so that only the style signal varies across methods. _Vanilla RL_ trains with _rt_ = _rt_<sup>loco</sup> only; style-matching and reference-tracking weights are zero. _Tracking_ stands in for the broad family of clip-tracking RL controllers [8], [14], [15], in which the reward is a time-indexed match against a recorded human pose; concretely, we use the BeyondMimic [23] tracking implementation that ships with MJLAB [2], fed the same _D_ clips as the predictor, and train one tracking policy per reference trajectory. At each step the environment advances a clip phase index and exposes a reference pose _qt_<sup>ref</sup> for the upper body; the imitation reward _rt_<sup>imit</sup> uses the kernel of (3) with _q_ ˆ _j,t_<sup>upreplacedby</sup><sup>_q_</sup> _j,t_<sup>ref,and</sup> the total reward is _rt_ = _rt_<sup>loco</sup> + _λ_ imit _rt_<sup>imit</sup> with the same locomotion-then-style curriculum used for PSM. Universal trackers such as ZEST [10] can in principle follow many references, but rely on a different observation interface and substantially more training data; we treat them as out of 


Fig. 4: Naturalness vs. command scenario (simulation batch, no pushes). Top: upper-body DTW to the reference motion (log scale). Bottom: velocity RMSE to **u** ( _t_ ) as a sanity check that all methods solve the same locomotion task. 

scope for this controlled comparison, whose purpose is to isolate the robustness cost of explicit reference tracking that is already present in single-clip trackers. _PSM_ uses _rt_ = _rt_<sup>loco</sup> + _λ_ match _rt_<sup>match</sup> with targets from the frozen _fϕ_ during training (Sec. II-B) and deploys with the same interface as vanilla RL. 

Each method is rolled out on a shared library of open-loop velocity schedules **u** ( _t_ ) = ( _vx, vy, ωz_ ) in the yaw frame. For naturalness trials, schedules are the root velocities of held-out walking clips from _D_ ; additional scripted schedules (constant forward walking, lateral sinusoids, heading changes, accelerate–decelerate segments) are used for stress testing and robustness. Policies track the prescribed **u** ( _t_ ) while we log joint and root states; the command is not resampled midepisode, so observed differences reflect whole-body style and recovery rather than different command distributions. For style alignment we compare logged upper-body joints and gait scalars against the source reference clip that generated **u** ( _t_ ) using dynamic time warping (DTW) [26], which tolerates mild phase shifts after turns or speed changes that would otherwise inflate a frame-wise RMSE: 


where _A_ denotes admissible warping paths and _d_ ( _·, ·_ ) is the squared joint error weighted as in (3) for the upper body. Scores are averaged over trajectories and random seeds (lower is better). Since all methods are scored against the same reference motions from _D_ , the DTW numbers are directly comparable: Tracking optimizes directly against that clip and serves as a tight lower bound on what is achievable under that supervision, while the gap between vanilla RL and 


Fig. 5: Robustness vs. disturbance scenario (simulation batch). Top: fall rate. Bottom: task recovery time _T_ vel. 

PSM measures how far predictive matching moves a policyonly controller toward the human trajectory. 

The same **u** ( _t_ ) trajectories are then repeated under a fixed schedule of impulsive pushes and velocity kicks. We report fall rate (%), velocity-tracking error to **u** ( _t_ ) in the post-disturbance window, and task recovery time _T_ vel (the time, in seconds, until _∥_ **u** _t −_ **v** ˆ _t∥ < ϵ_ ). Task quantities use time-aligned errors. With protocol and metrics fixed, we first isolate naturalness in the absence of disturbances, then introduce pushes and quantify what each method gives up. 

# _A. Naturalness_ 

We begin with nominal walking, where the policy is not driven into recovery poses. Fig. 4 reports DTW to the reference motion across the no-push trajectory batch in simulation, split by command scenario. Tracking attains the lowest upper-body and gait DTW because it directly optimizes against the source clip used for scoring—an expected lower bound for that supervision setting. Aggregated over the batch, PSM reduces upper-body DTW by roughly 8 _×_ relative to vanilla RL (0 _._ 31 _±_ 0 _._ 03 vs. 2 _._ 41 _±_ 0 _._ 30), and gait DTW by about 4 _×_ (0 _._ 21 _±_ 0 _._ 04 vs. 0 _._ 81 _±_ 0 _._ 20). PSM remains above Tracking because it follows predictor outputs recomputed from the policy’s own lower-body history and command rather than the source clip itself—precisely the property that decouples style from a clip clock when recovery is needed. 

Tracking remains the lower-bound method when its reference phase is available, whereas PSM closes most of the gap from vanilla RL without requiring that reference at deployment. Velocity-tracking RMSE to **u** ( _t_ ) is comparable across methods, confirming that the style differences are not a byproduct of solving different locomotion tasks. On 


Fig. 6: Push envelope (simulation): fall rate over push direction and impulse magnitude (shared color scale). Vanilla RL and PSM remain low across the envelope, while Tracking saturates at moderate impulses, particularly for lateral pushes. 

hardware all three policies execute the same representative **u** ( _t_ ) subset, and PSM produces the coordinated arm swing and stepping shown in Fig. 1. 

# _B. Robustness_ 

Naturalness alone is only half the picture: a controller that walks well only when nothing pushes back is of little practical use. We therefore repeat the same command trajectories under impulsive pushes and velocity kicks. Fig. 5 breaks down fall rate and recovery time by disturbance type, and Fig. 6 summarizes the push envelope over direction and impulse magnitude. Aggregated across the disturbance suite, vanilla RL and PSM remain within one standard deviation of each other on both fall rate (4 _._ 1% vs. 4 _._ 4%) and task recovery _T_ vel ( _∼_ 0.9 s), whereas Tracking incurs roughly 5 _×_ the fall rate (21 _._ 5%) and the longest _T_ vel (1 _._ 80 s). This pattern is consistent with clip targets opposing the transient recovery poses that the task reward is simultaneously trying to elicit. 

On hardware, PSM exhibits strong push robustness while retaining natural, human-like arm motion. Taken together, Figures 4 and 5 sketch a clear naturalness–robustness tradeoff: PSM sits next to vanilla RL on the fall-rate axis while reducing upper-body DTW by close to an order of magnitude, whereas Tracking occupies the opposite corner— lowest DTW but highest fall rate—of the same plane. Beyond the headline numbers, a development-time ablation is worth noting: activating only the upper-body weight _w_ up already biased stepping rhythm through kinematic coupling between 

arms, torso, and pelvis; the reported policies nevertheless match both upper-body and gait descriptors, because explicit gait matching proved more stable across command and disturbance scenarios. 

Overall, the main gain of PSM is not only lower style error, but a cleaner decomposition of responsibilities during learning: locomotion rewards dominate balance and recovery transients, while predictor-based terms act as local style attractors for upper-body coordination and gait timing. This appears to explain the observed operating point: PSM moves markedly toward human-like motion under nominal commands while remaining close to vanilla RL under pushes, whereas clip-tracking reaches lower nominal DTW but pays a larger robustness cost when recovery requires off-reference poses. Practically, this keeps deployment simple: only _πθ_ runs on hardware, with no clip index, phase-estimation pipeline, or additional runtime conditioning channel. The disturbance breakdown is especially informative: Tracking degrades most under lateral impulses, where recovery poses diverge farthest from the reference clip. In that regime, state-conditioned predictor targets remain aligned with the task objective rather than pulling the policy back toward a nominal walking pose. 

# IV. CONCLUSION AND FUTURE WORK 

Taken together, the naturalness and robustness experiments support the central design choice of PSM: use human motion as a _train-time_ , state-conditioned style signal rather than a deployment-time reference. Because matching is consumed only during training, the deployed controller retains the proprioceptive interface and inference cost of a task-only RL baseline, while the lower-body-conditioned predictor supplies RL with a concrete notion of arm swing, stepping, and torso behavior that task rewards alone do not specify. In the controlled G1 comparison, PSM reduces upper-body DTW by roughly 8 _×_ relative to vanilla RL while staying within one standard deviation on both fall rate and _T_ vel. The clip-tracking baseline attains the lowest DTW against its own reference, yet falls about 5 _×_ more often when those references oppose recovery—a behavior that follows from training-time choices (locomotion-first curriculum, pushes throughout training, state-conditioned targets) rather than any runtime stabilizer. 

Several limitations are worth flagging: predictor quality upper-bounds the achievable style, the sim-to-mocap legstate shift is not corrected explicitly, and only the first predicted step ( _k_ =0) is used for matching even though _fϕ_ produces a full horizon. Natural next steps include matched AMP [12], [16] and universal-tracker [10] comparisons under the same _D_ and MDP, fine-tuning _fϕ_ on RL rollouts to close the sim-to-mocap loop, multi-step anticipatory matching that exploits the full predicted horizon, terrain- or contact-conditioned predictors beyond flat-ground walking, and transferring the same recipe to other humanoid platforms whose kinematics differ from the G1 (e.g., taller bipeds or robots with different arm and torso topologies), where only _fϕ_ and the matched joint subset need to be re-instantiated. 

REFERENCES 

- [1] N. Rudin, D. Hoeller, P. Reist, and M. Hutter, “Learning to walk in minutes using massively parallel deep reinforcement learning,” in _Conference on Robot Learning_ , 2022, pp. 91–100. 

- [2] K. Zakka, Q. Liao, B. Yi, L. L. Lay, K. Sreenath, and P. Abbeel, “mjlab: A lightweight framework for GPU-accelerated robot learning,” _arXiv preprint arXiv:2601.22074_ , 2026. 

- [3] J. Lee, Y. Seo, S. L. Zhang, S. Mahadevan, P. Clary, T. Nguyen _et al._ , “Learning quadrupedal locomotion over challenging terrain,” _Science Robotics_ , vol. 5, no. 47, p. eabc5986, 2020. 

- [4] T. Miki, J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter, “Learning robust perceptive locomotion for quadrupedal robots in the wild,” _Science Robotics_ , vol. 7, no. 62, p. eabk2822, 2022. 

   - [23] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu, “BeyondMimic: From motion tracking to versatile humanoid control via guided diffusion,” _arXiv preprint arXiv:2508.08241_ , 2025. 

   - [24] Bones Studio, “AI datasets for machine learning and motion capture,” https://bones.studio/ai-datasets/, 2026, human motion capture data (BoneSeed). 

   - [25] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

   - [26] H. Sakoe and S. Chiba, “Dynamic programming algorithm optimization for spoken word recognition,” _IEEE Transactions on Acoustics, Speech, and Signal Processing_ , vol. 26, no. 1, pp. 43–49, 1978. 

- [5] X. Cheng, K. Shi, A. Agarwal, and D. Pathak, “Extreme parkour with legged robots,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 11 443–11 450. 

- [6] D. Hoeller, N. Rudin, D. V. Sako, and M. Hutter, “Anymal parkour: Learning agile navigation for quadrupedal robots,” _Science Robotics_ , vol. 9, no. 88, p. eadh8134, 2024. 

- [7] N. Rudin, J. He, J. Aurand, and M. Hutter, “Parkour in the wild: Learning a general and extensible agile locomotion policy for quadrupedal robots,” _arXiv preprint arXiv:2405.10427_ , 2024. 

- [8] T. He, J. Gao, W. Xiao, Y. Zhang, R. Tsunoda _et al._ , “ASAP: Aligning simulation and real-world physics for learning agile humanoid wholebody skills,” _arXiv preprint arXiv:2412.04194_ , 2024. 

- [9] Y. Shi, X. Wang, X. Li, J. Zhang _et al._ , “KungfuBot: Physics-based humanoid whole-body control for learning highly-dynamic skills,” _arXiv preprint arXiv:2410.05064_ , 2024. 

- [10] J.-P. Sleiman, H. Li, A. Adu-Bredu, R. Deits, A. Kumar _et al._ , “ZEST: Zero-shot embodied skill transfer for athletic robot control,” _arXiv preprint arXiv:2602.00401_ , 2026. 

- [11] S. Ha, J. Lee, S. L. Zhang, J. Hwangbo, X. B. Peng _et al._ , “Learningbased legged locomotion: State of the art and future perspectives,” _Annual Review of Control, Robotics, and Autonomous Systems_ , vol. 6, pp. 339–364, 2023. 

- [12] P. Escontrela, W. Yu, X. B. Peng, S. Levine, and Y. Ma, “Adversarial motion priors make good substitutes for complex reward functions,” _arXiv preprint arXiv:2203.15103_ , 2022. 

- [13] G. Ji, P. M. Wensing, and J. Grizzle, “Concurrent training of a control policy and a state estimator for tracking and estimation,” in _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2022, pp. 12 170–12 177. 

- [14] X. B. Peng, P. Abbeel, S. Levine, and M. van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physics-based character skills,” in _ACM Transactions on Graphics (TOG)_ , vol. 37, no. 4, 2018, pp. 1–14. 

- [15] Z. Gu, H. Xue, Z. Xie, X. B. Peng _et al._ , “VideoMimic: Visual whole-body control for humanoids from human videos,” _arXiv preprint arXiv:2412.16382_ , 2024. 

- [16] X. B. Peng, Y. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “Amp: Adversarial motion priors for stylized physics-based character control,” in _ACM Transactions on Graphics (TOG)_ , vol. 40, no. 4, 2021, pp. 1–20. 

- [17] Y. Shi, J. Wang, X. Jiang, B. Lin, B. Dai, and X. B. Peng, “Interactive character control with auto-regressive motion diffusion models,” in _ACM Transactions on Graphics (Proc. SIGGRAPH 2024)_ , 2024. 

- [18] S. Cohan, G. Tevet, D. Reda, X. B. Peng, and M. van de Panne, “Flexible motion in-betweening with diffusion models,” in _ACM SIGGRAPH 2024_ , 2024. 

- [19] G. Tevet, S. Raab, S. Cohan, D. Reda, Z. Luo, X. B. Peng, A. H. Bermano, and M. van de Panne, “CLoSD: Closing the loop between simulation and diffusion for multi-task character control,” in _International Conference on Learning Representations_ , 2025. 

- [20] C. Tessler, Y. Kasten, Y. Guo, S. Mannor, G. Chechik, and X. B. Peng, “CALM: Conditional adversarial latent models for directable virtual characters,” in _ACM SIGGRAPH 2023_ , 2023. 

- [21] X. B. Peng, Y. Guo, L. Halper, S. Levine, and S. Fidler, “ASE: Largescale reusable adversarial skill embeddings for physically simulated characters,” in _ACM Transactions on Graphics (Proc. SIGGRAPH 2022)_ , vol. 41, no. 4, 2022, pp. 1–17. 

- [22] C. Tessler, Y. Guo, O. Nabati, G. Chechik, and X. B. Peng, “MaskedMimic: Unified physics-based character control through masked motion inpainting,” in _ACM Transactions on Graphics (Proc. SIGGRAPH Asia 2024)_ , 2024. 

