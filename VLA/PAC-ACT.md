---
title: "PAC-ACT: Post-training Actor-Critic for Action Chunking Transformers"
date: "2026-07-10"
authors: "Yujie Pang; Zudong Li"
url: https://arxiv.org/abs/2607.09590
pdf: https://arxiv.org/pdf/2607.09590
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2607.09590)** / [論文ページ](https://arxiv.org/abs/2607.09590)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# PAC-ACT: Post-training Actor-Critic for Action Chunking Transformers 

Yujie Pang 

_Dept. of Mechanical and Energy Engineering Southern University of Science and Technology_ Shenzhen, China 0009-0003-6377-6949 

Zudong Li 

_Dept. of Mechanical and Energy Engineering Southern University of Science and Technology_ Shenzhen, China 0009-0009-5574-9602 

**_Abstract_ —Precision industrial contact manipulation requires robots to complete tasks reliably under pose perturbations and contact-force constraints, placing strong demands on policy determinism, contact-force safety, and disturbance resistance. Vision-language-action models provide strong task generalization, but they usually introduce higher inference and GPU-memory overhead, which still limits deployment in high-frequency control scenarios. In contrast, vision-action chunking policies provide low-latency inference and temporally continuous actions, making them more suitable for industrial scenarios that require predictable and real-time behavior. However, these policies are mainly trained through behavior cloning, and error accumulation under distribution shift limits further improvements in task success and contact stability. To address this issue, this paper proposes PAC-ACT, a reinforcement-learning post-training framework for pretrained action-chunking policies. The core idea is to improve task completion and contact stability through reinforcement learning while preserving the lightweight and efficient properties of vision-action chunking models. Specifically, PAC-ACT reformulates step-wise policy optimization as a chunk-level decision process, aligning reinforcement-learning updates with action-chunk generation; it further builds policy and value-network architectures adapted to pretrained networks and introduces a hybrid behavior-prior constraint to prevent the policy from drifting away from the action distribution learned by the pretrained policy. Experiments on industrially motivated precision-contact benchmarks show that the method improves task success, contact stability, and force safety while maintaining low latency and low GPU-memory usage. In particular, on the Contour task, the median peak contact force is significantly reduced, and the proportion of force readings above 60N is reduced by 46 times. An additional sparse-reward ablation verifies the necessity of key framework components and shows that PACACT can still explore effectively under randomized initial poses when only the task-success reward is retained together with the behavior-prior constraint.** 

**_Index Terms_ —Visuomotor control, action chunking, reinforcement learning fine-tuning, imitation learning, precision contact manipulation** 

## I. INTRODUCTION 

Model-based or vision-servoed manipulation pipelines often depend on accurate camera calibration, hand-eye calibration, and object or end-effector pose estimation. Errors in these calibration and localization steps can propagate through the visualservoing control law and degrade positioning accuracy, which 

becomes particularly problematic in precision contact tasks [1], [2]. In recent years, end-to-end visuomotor policies represented by Action Chunking Transformer (ACT) and Diffusion Policy have directly mapped high-dimensional visual observations to low-dimensional actions, reducing the need for explicit geometric action design in several manipulation settings [3], [12]. In particular, ACT predicts multiple future action steps at once through action chunking, improving temporal continuity and execution stability as reported in fine-grained bimanual manipulation experiments [3]. This paradigm has been extended to bimanual manipulation [3], multi-task robot learning [23], and large-scale vision-language-action (VLA) models [14], [15], demonstrating the broad applicability of action chunking in robot control. 

However, such action chunking policies are still fundamentally trained under the offline behavior cloning paradigm, and their performance strongly depends on the quality and coverage of demonstrations [3], [5], [12]. When the robot encounters out-of-distribution states or contact perturbations at test time, small action deviations may accumulate over longhorizon execution and eventually cause failure, a common limitation of behavior cloning under covariate shift [4], [5]. This distribution-shift problem is particularly severe in precision contact tasks: millimeter-level pose errors may either prevent the robot from reaching the target contact region or drive the contact force beyond the safety range. Studies on contact manipulation further note that sustained incontact tasks generally require explicit or implicit regulation of robot-environment interaction forces [6], [7]. Therefore, action chunking policies trained only by offline behavior cloning remain insufficient for industrial contact tasks that require outof-distribution robustness and force safety [4]–[7]. 

Directly introducing action chunking policies into reinforcement learning faces structural challenges. The mismatch between chunk-level action generation and step-wise reward feedback exacerbates credit assignment, motivating recent studies on chunk-level RL and action-sequence value estimation [8], [9], [19]. Existing studies have begun to explore chunk-level RL, including Chunking the Critic [8] and Q- Chunking [9], but they mainly focus on learning chunking 

policies from scratch or improving offline-to-online transfer efficiency. The problem of reusing the structure of a pretrained action chunking policy while preserving its behavior prior during fine-tuning remains underexplored. 

To fill this gap, we propose PAC-ACT, a reinforcementlearning post-training framework for pretrained ACT policies. Built on a pretrained ACT model under the LeRobot [10] framework, PAC-ACT exploits the action prior learned from a moderate number of expert demonstrations and reduces the dependence of online RL on large-scale random exploration. Specifically, we design an ACT-transferred Actor-Critic architecture that preserves the ACT backbone while removing the CVAE latent module, introduce hybrid KL constraints to maintain the pretrained behavior prior, and reformulate the MDP to resolve the structural mismatch between step-wise RL and chunk-level action generation. 

The main contributions are summarized as follows: (1) We propose an RL post-training framework for pretrained ACT policies and construct an Actor-Critic architecture from the native ACT structure to enable stable online fine-tuning. (2) We jointly improve force safety and task completion efficiency for industrial precision contact tasks, enhancing contact stability and execution efficiency while retaining lowlatency inference. (3) We conduct systematic experiments on Metal Touch and Square Assembly, providing detailed quantitative analyses of task success, force-safety improvement, and training convergence dynamics, with significant reductions in hazardous force events and extreme peak forces on the Contour task. (4) We demonstrate the potential of RL post-training for task-specific optimization in industrial robotics and show that the behavior prior learned by behavior cloning can effectively reduce the exploration burden of reinforcement learning. 

## II. RELATED WORK 

## _A. Transformer-based Action Chunking Policies_ 

Imitation learning has become a mainstream paradigm for robotic visuomotor control [3], [5], [12], [13]. Early behavior cloning (BC) methods suffered from distribution shift due to frame-by-frame action prediction [4], [5], whereas action chunking improves temporal consistency and robustness in ACT-style policies [3]. ACT [3] uses a CVAE-Transformer [11] architecture to model robot control as joint prediction of a fixed-length future action sequence and achieves strong performance in fine-grained bimanual manipulation. The action chunking mechanism provides temporal abstraction: instead of committing to a single-step action, the policy commits to a trajectory segment, which can smooth execution and reduce compounded errors [3]. 

Subsequent work has extended this line in several directions. Diffusion Policy [12] replaces the CVAE formulation with a diffusion process, requiring multi-step iterative sampling at inference time but representing more complex multi-modal action distributions. BeT [13] introduces discrete action representations by discretizing the action space, providing an intermediate design between continuous and discrete control. More recently, large-scale VLA models such as RT-2 [14] and 

_π_ 0.5 [15] have shown the potential of extending action chunking through web-scale pretraining and broad task generalization. Concurrently, Implicit Behavioral Cloning (IBC) [16] approaches action distribution modeling from an energy-based perspective. Nevertheless, these imitation-learning methods fundamentally depend on the quality of offline demonstrations and do not improve through online task reward, which limits their ability to handle distribution shift [4], [5]. 

## _B. Chunk-level Reinforcement Learning_ 

Early work combining action chunking with RL mainly addressed high-dimensional action spaces through discrete action representations. CQN-AS [17] discretizes the action chunk space into a prototype library and learns a Q-function over it, but discretization inherently limits the precision of continuous control [17]. This precision tradeoff is especially undesirable for contact-rich manipulation tasks that require fine force modulation. 

Recent studies have explored continuous action chunk RL through different approaches. Chunking the Critic [8] extends SAC [18] to the chunk level by introducing a lightweight Transformer for joint value estimation over action sequences, while retaining a step-wise actor. Q-Chunking [9] uses a flow-matching framework for continuous chunk generation but relies on large-scale offline datasets and computationally intensive distillation, limiting its applicability in low-data settings. Concurrent work AC3 [19] introduces asymmetric actor updates for continuous chunk RL under sparse rewards and reports promising results across several manipulation benchmarks. 

However, these studies mainly focus on learning chunking policies from scratch or optimizing offline-to-online transfer [8], [9], [19]. The distinct problem of fine-tuning pretrained action chunking policies, where the goal is to selectively improve task performance through RL while preserving the behavior structure learned from demonstrations, remains insufficiently studied. This is the gap addressed by our work. It is also worth noting that the above studies differ fundamentally from ours in task setting, simulation environment, reward design, and the source of the initial policy, and therefore do not constitute direct quantitative baselines. 

## _C. RL Fine-tuning of Pretrained Policies_ 

RL fine-tuning of pretrained policies has become a promising paradigm for robotic manipulation [19]–[21], [24]. The central insight is that BC provides a behavior prior, and RL can subsequently optimize this prior through environmental interaction [19]–[21]. This approach is particularly attractive for industrial applications because (a) a moderate number of demonstrations may be available, (b) task specifications may change or require customization, and (c) large-scale random exploration is often infeasible under safety constraints [22]. 

Existing work follows two main routes. The first adapts or post-trains large-scale VLA models to exploit their broad generalization ability [14], [15], [23]. However, large-scale VLA models typically introduce a vision-language backbone 

and an action generation module, making their inference path more complex than that of pure vision-action policies. For example, the _π_ 0.5 model used in this paper is built on a PaliGemma vision-language backbone and an action expert; at inference time, it first produces high-level semantic subtasks and then generates continuous action chunks with the action expert [15]. This structure supports open-world generalization but also makes inference latency and GPU memory usage important considerations in high-frequency closed-loop control. The second route focuses on generative policy frameworks such as DPPO [24], which fine-tunes Diffusion Policy through a differentiable reward-weighted denoising process. Although effective, the iterative sampling nature of diffusion models introduces additional latency and training variance. 

In contrast, deterministic ACT-style action chunking policies generate future action chunks with a single forward pass [3]. The original ACT system reports an inference time of approximately 0.01s for an 80M-parameter model on a single RTX 2080 Ti [3]. Owing to their simple architecture, temporally continuous actions, and lower deployment overhead, such policies are suitable backbones for industrial RL finetuning [3]. This paper shows that, with an appropriate MDP reformulation and constraint mechanism, these policies can be effectively fine-tuned by RL to improve task performance while preserving deployment-friendly properties. 

## III. METHOD 

## _A. Problem Definition: Structural Mismatch_ 

Standard RL algorithms are formulated around step-wise decisions: at each time step _t_ , the policy observes _st_ , outputs _at_ , and receives _rt_ [18], [28], [29]. In contrast, ACT uses a CVAE-Transformer architecture to generate a continuous _K_ = 100-step action chunk **A** _t_ = ( _at, at_ +1 _, . . . , at_ + _K−_ 1) at once, and then executes only the first _c_ 0 = 10 steps under temporal ensembling before replanning [3]. During RL fine-tuning, we set the execution horizon to _c_ = 8, forming the basic temporal unit for chunk-level decision making. The sub-actions inside each chunk exhibit strong temporal coupling and trajectory continuity: each action is not an independent primitive but part of a coordinated motion sequence. 

This structural difference introduces three interrelated challenges for step-wise RL fine-tuning. First, the probability ratio _πθ_ ( _at|st_ ) _/πθ_ old( _at|st_ ) used in the PPO clipped surrogate objective operates at the per-action level [28], whereas individual actions inside a chunk are not independently meaningful: their joint structure is the key object. Computing ratios for individual actions assigns credit and penalties to atomic actions that were never designed to be evaluated independently. Second, the advantage estimate _A_<sup>ˆ</sup> _t_ is computed per time step, but the reward signal for successfully executing an action chunk may only become visible after multiple steps. This temporal mismatch makes step-wise advantage estimation poorly aligned with the actual credit assignment structure. Third, exploration in the generated _K × da_ -dimensional action space is intrinsically harder than exploration in the _da_ -dimensional single-step action space. We refer to these issues collectively 

as the “structural mismatch” between action chunk generation and step-wise RL optimization. 

## _B. Chunk-level MDP Adaptation_ 

To address structural mismatch, we reformulate the standard step-wise MDP as a chunk-level decision process. The core idea is to group _c_ environment steps into one chunk-level time step, so that policy action generation and RL optimization operate at the same temporal granularity. 

Formally, we define a chunk-level MDP in which each chunk time step _τ_ corresponds to _c_ original environment steps. At chunk time step _τ_ , the policy observes the current state _sτ_ (i.e., _sτc_ in the original step index) and outputs a _c_ -step action chunk _πθ_ ( **a** _τ |sτ_ ), obtained by taking the first _c_ actions from the _K_ actions generated by ACT. The environment executes all _c_ actions sequentially and accumulates the reward: 


and transitions to _sτ_ +1 = _sτc_ + _c_ . The inter-chunk discount factor is adjusted accordingly as Γ = _γ_<sup>_c_</sup> , where _γ_ = 0 _._ 99 is the original step-wise discount factor. 

Under this formulation, the components of PPO naturally adapt to the chunk level. The probability ratio is computed over the entire action chunk: 


where _πθ_ ( **a** _τ |sτ_ ) is defined over the flattened _c × da_ - dimensional action space. We model the policy with a diagonal Gaussian distribution, so log _πθ_ ( **a** _τ |sτ_ ) decomposes into the sum of log probabilities over action dimensions, and the corresponding probability ratio is the product of dimension-wise ratios. This decomposition provides a consistent stochastic estimate of _ρτ_ ( _θ_ ), while the mean _µθ_ ( _sτ_ ) is still generated by the ACT decoder through self-attention, preserving temporal correlations among steps within the action chunk. Generalized advantage estimation (GAE) is computed at the chunk level: 


where Γ = _γ_<sup>_c_</sup> is the inter-chunk discount factor. 

In implementation, we use a hybrid scheme of step-wise reward collection and chunk-level policy update. Rewards are collected at every environment step to retain fine-grained feedback, while GAE advantages are aggregated at chunk boundaries and the PPO clipped surrogate loss is computed over complete chunks. This preserves detailed reward information while aligning the optimization granularity with the action generation structure. 

## _C. ACT-transferred Actor-Critic_ 

_1) Actor: Preserving Action Chunk Generation:_ In this architecture (Fig. 1), the Actor fully reuses the visual encoder (ResNet-18 [25]), Transformer [26] encoder (4 layers, 256 dimensions), and action decoder of the pretrained ACT 


Fig. 1. Overall network architecture of PAC-ACT. The PPO post-training framework is built from a pretrained ACT model. The Actor branch preserves the original ACT action chunk generation structure while removing the CVAE module, producing temporally consistent continuous action sequences. The Critic branch reuses the ACT visual encoder and Transformer encoder, removes the action decoder, pools the encoder output, and maps it to a scalar state value through a value head. 

model to preserve the temporal action structure learned during pretraining. The Actor input is a multimodal observation consisting of two RGB images (front and wrist views, 512 _×_ 512) and a 6-dimensional joint-angle encoding. The visual encoder processes each camera view independently into latent features, which are concatenated with low-dimensional proprioceptive signals. The Transformer encoder then processes the fused representation with self-attention to capture spatial and temporal relations. Finally, the action decoder outputs a _K × da_ tensor ( _K_ = 100), representing the action mean at each step over the generated horizon. 

The original ACT uses a CVAE to model action diversity through a latent variable _z_ , sampled from the prior distribution at inference time [3], [11]. During RL fine-tuning, the policy already requires stochastic exploration through its Gaussian policy distribution; retaining the CVAE would introduce an additional and redundant source of randomness, increasing optimization instability. More importantly, the stochastic latent variable _z_ in the CVAE conflicts with the baseline penalty in our hybrid KL constraint (Eq. (9)): _z_ induces inherent output fluctuations, while the _β_ 2 term continuously penalizes these fluctuations, canceling useful gradients and reducing optimiza- 

tion efficiency. The ablation study in Sec. IV-I quantitatively confirms that retaining the CVAE leads to a measurable degradation in convergence. In addition, recent progress in visual representation learning, such as R3M [27], provides rich pretrained initialization options for robotic visual encoders. Based on this analysis, we remove the CVAE module from the Actor and use the network output directly as the mean of a diagonal Gaussian policy: 


where the covariance matrix Σ = diag( _σ_ 1<sup>2</sup><sup>_, . . . , σ_</sup> _c_<sup>2</sup> _·da_<sup>)is</sup> represented by learnable log-standard-deviation parameters, initialized as log _σi_ = _−_ 5 _._ 5 for Metal Touch or _−_ 3 _._ 0 for Square Assembly to match the output scales of different action representations and encourage initially narrow exploration around the pretrained behavior. This parameter is selected according to the action representation of the pretrained policy (absolute position vs. delta action), reflecting the adaptability of the framework to different action spaces. 

_2) Critic: Lightweight Encoder-Value Network:_ The Critic maps high-dimensional observations to a scalar state value _V_ ( _s_ ). We construct the Critic by reusing the visual encoder 

and Transformer encoder of the pretrained ACT model, removing the action decoder, and appending a value head. The Critic and Actor use the same visual encoder and Transformer encoder architecture, except that the Critic has no decoder and maintains an independent copy of the weights. Given an observation _s_ , the Critic runs the visual encoder and Transformer encoder, mean-pools the output sequence representation into a global encoded feature vector, and feeds it into a lightweight value network: 

current policy output and the baseline output during rollout collection: 


where _β_ 2 = 2 _._ 0. The modified reward _rt_<sup>_′_replacestheoriginal</sup> _rt_ in GAE computation. This mechanism encourages RL updates to explore within the neighborhood of the expert action manifold and prevents the policy from drifting into regions of the action space that may be assigned high value by the learned value function but would not be executed by the pretrained policy and may be unsafe or unstable. 


where the MLP head contains two hidden layers (256 _→_ 256 _→_ 1) with ReLU activations. Removing the decoder is motivated by the following consideration: the Critic estimates state value rather than generating actions, and the additional parameters introduced by the decoder do not directly contribute to value estimation. The hidden representation produced by the encoder already contains task-relevant visual and state information; after pooling, it can be used effectively for value regression while reducing the Critic’s parameter count and computational cost. The ablation study in Sec. IV-I further shows that a Critic retaining the decoder lags behind by approximately 12 percentage points at the same training budget, validating the encoder-value design. 

## **Algorithm 1** PAC-ACT (Chunk-level PPO Fine-tuning) 

1: **Input:** pretrained ACT policy _πθ_ , initial covariance Σ, value decoder is motivated by the following consideration: the network _Vϕ_ , rollout buffer _B_ Critic estimates state value rather than generating actions, 2: **Hyperparameters:** chunk execution length _c_ , PPO epochs _E_ , and the additional parameters introduced by the decoder minibatch size _M_ , number of parallel environments _N_ , _β_ 1, _β_ 2 do not directly contribute to value estimation. The hidden 3: Load baseline policy _π_ base _← πθ_ // Frozen and not updated representation produced by the encoder already contains 4: **for** iteration = 1 _,_ 2 _, . . ._ **do** 5: **Stage 1: Rollout collection** task-relevant visual and state information; after pooling, it can 6: **for** each environment _i_ = 1 _, . . . , N_ **do** be used effectively for value regression while reducing the 7: _s ←_ env.reset() Critic’s parameter count and computational cost. The ablation 8: **for** _t_ = 1 **to** rollout <u>steps</u> **do** study in Sec. IV-I further shows that a Critic retaining the 9: **_µ_** _, v ← πθ_ ( _s_ ) _, Vϕ_ ( _s_ ) decoder lags behind by approximately 12 percentage points at 10: **a** _∼N_ ( **_µ_** _,_ Σ) // Output a _c_ -step action chunk 11: _s_<sup>_′_</sup> _, r_ env _, done ←_ env.step( **a** ) the same training budget, validating the encoder-value design. // Execute _c_ internal substeps 12: _d_ = _∥_ **_µ_** _−_ **_µ_** base( _s_ ) _∥_<sup>2</sup> , _r_ = _r_ env _− β_ 2 _d D. Hybrid KL-Regularized Policy Optimization_ 13: _B ←_ ( _s,_ **a** _, r, v_ ), _s ← s_<sup>_′_</sup> Standard PPO [28] uses a clipped surrogate objective to 14: **end for** 15: **end for** constrain policy updates: 16: **Stage 2: Chunk-level advantage estimation** 17: Sample from _B_ and compute GAE: _L_ PPO = E _t_ � min � _rt_ ( _θ_ ) _A_<sup>ˆ</sup> _t,_ clip( _rt_ ( _θ_ ) _,_ 1 _− ϵ,_ 1 + _ϵ_ ) _A_<sup>ˆ</sup> _t_ �<sup>�</sup> _,_ (6) 18: _δt_ = _rt_ + Γ _Vϕ_ ( _st_ +1) _− Vϕ_ ( _st_ ) 19: _A_<sup>GAE</sup> _t_<sup>(Γ</sup><sup>_,λ_)</sup> =<sup>�</sup><sup>_∞_</sup> _l_ =0<sup>(Γ</sup><sup>_λ_)</sup><sup>_lδt_+</sup><sup>_l_</sup> where the probability ratio is defined as 20: **Stage 3: Chunk-level PPO update** 21: **for** epoch = 1 **to** _E_ **do** _ρt_ ( _θ_ ) =<sup>_πθ_</sup><sup><u>(</u></sup><sup>_at|st_</sup><sup><u>)</u></sup> (7) 22: **for** minibatch = 1 **to** _M_ **do** _πθ_ old( _at|st_ )<sup>_._</sup> 23: _ρt_ = _πθ_ ( **a** _t|st_ ) _/πθ_ old ( **a** _t|st_ ) 24: _L_ PPO = min( _ρtAt,_ clip( _ρt,_ 1 _− ϵ,_ 1 + _ϵ_ ) _At_ ) However, in the high-dimensional action chunk space, the 25: _L_ value = MSE( _Vϕ_ ( _st_ ) _, Vϕ_<sup>target</sup> ( _st_ )) clipped objective alone is insufficient to prevent destructive 26: _L_ = _−L_ PPO + _β_ 1 _D_<sup>�</sup> KL( _πθ_ old _, πθ_ )+ _cvL_ value _− ceH_ ( _πθ_ ) drift away from the pretrained behavior manifold. We therefore 27: Update _θ, ϕ_ introduce two complementary regularization mechanisms. 28: **end for** First, we add a KL penalty [29] to the loss function to 29: **end for** 30: **if** converged, exit **then** constrain distributional drift between adjacent PPO updates: 31: **end if** 32: **end for** 


where _β_ 1 = 3 _._ 0. In implementation, we use the empirical KL estimate between adjacent PPO policies as the regularization term and combine it with the PPO clipped objective to constrain distributional drift. This local trust-region constraint complements the clipped surrogate objective by providing a softer but more global penalty. It is particularly important in the action chunk space, where per-action clipping boundaries are insufficient to control joint distributional drift across all _c × da_ dimensions. 

## IV. EXPERIMENTS 

## _A. Metal Touch Precision Contact Scenario_ 

Metal Touch is a simulated benchmark for precision contact manipulation. As shown in Fig. 2, the task scene contains a 6-DoF robotic arm equipped with a stick-like end-effector and a carrier platform fixed on the table (100mm _×_ 100mm _×_ 50mm). An annular rubber-metal part is placed on the platform, and the rubber boundary corresponds to four contact regions. The task objective is for the robot to touch all four regions sequentially; the contact force threshold [0.5N, 60.0N] is used for reward constraints and force-safety evaluation. 

Second, we introduce behavior-prior regularization at the reward level. Using the pretrained ACT baseline model _π_ base with fixed parameters, we penalize deviations between the 


Fig. 2. Metal Touch precision contact task environment and randomized initialization distribution. Left: continuous contact manipulation in MuJoCo [30], where a 6-DoF robotic arm performs precision contact operations on a rubbermetal component through an end-effector probe. Right: randomized initial positions of the metal component across episodes; the object is randomly shifted within _±_ 2cm around the center region to simulate positioning errors and out-of-distribution perturbations in industrial scenarios. 

At the beginning of each episode, the rubber component is randomly translated on the table plane within _±_ 2cm. The policy observation includes two Intel RealSense D415 RGB cameras (front and wrist views, 512 _×_ 512 resolution) and a 6-dimensional joint-angle encoding. The MuJoCo environment also provides 6-axis force/torque sensor readings for reward computation and force-safety evaluation during RL post-training, but these readings are not used as inputs to the pretrained policy. The control frequency is 10Hz, and each RL training episode is limited to 512 steps, approximately 51 seconds. 

We design three contact tasks with progressively increasing complexity, covering different trajectory geometries and motion patterns: (1) Diamond, which sequentially touches four side points; (2) Cross, which follows center _→_ left _→_ center _→_ right _→_ center _→_ up _→_ center _→_ down and contains observation-action ambiguity; and (3) Contour, which continuously moves along the inner boundary of the rubber ring and has the longest effective contact horizon. These tasks differ in trajectory shape, motion direction, and contact timing, jointly testing policy adaptability across diverse contact scenarios. Task success is measured by whether all four regions are reached, and whether the contact force exceeds 60N is reported as an independent force-safety metric. We additionally test scalability on robomimic [5] Square Assembly. 

## _B. Experimental Setup_ 

_1) Dataset Construction:_ All demonstration data are collected and stored using the LeRobot framework. LeRobotDataset adopts a hierarchical storage architecture: highfrequency low-dimensional signals, including joint angles, force sensor readings, and action commands, are organized in Apache Parquet columnar format, with each row corresponding to one frame; visual observations, including front and wrist RGB images, are temporally compressed into cameraspecific MP4 files. The metadata layer records the schema, frame rate, normalization statistics, and episode boundaries. This design minimizes disk storage through video compression 

while enabling efficient random access to individual frames during training. To study the effect of dataset size, we construct datasets containing 50, 100, 200, 400, and 800 expert trajectories, retaining only successful trajectories. For Square Assembly, robosuite [31] replay is used to reconstruct the data in LeRobotDataset format. 

_2) PPO Training Configuration and Evaluation Metrics:_ The pretrained ACT model uses a ResNet-18 visual encoder, a 4-layer Transformer encoder with 256-dimensional hidden states, and an action generation length of _K_ = 100 with temporal ensembling execution length _c_ 0 = 10. It is pretrained on 800 trajectories for 200,000 steps. PPO hyperparameters are as follows: chunk execution length _c_ = 8, _γ_ = 0 _._ 99, GAE _λ_ = 0 _._ 95, clipping range _ϵ_ = 0 _._ 2, learning rate 1 _×_ 10<sup>_−_6</sup> , Critic learning rate 1 _×_ 10<sup>_−_5</sup> , entropy coefficient 0.001, KL coefficients _β_ 1 = 3 _._ 0 _, β_ 2 = 2 _._ 0, PPO epochs 8, minibatch size 32, and 16 parallel environments. The chunk execution length is adjusted from the pretrained _c_ 0 = 10 to _c_ = 8 because Metal Touch uses an absolute-position action representation, making the policy more sensitive to the initial value of log _σ_ . Shortening the executed chunk reduces training difficulty while maintaining exploration entropy and effectively preserves the success-rate basis of the pretrained _c_ 0 = 10 temporal ensembling policy. 

The reward function follows a milestone design. A regiontouch reward is triggered when a new region is contacted for the first time. Additional penalty terms include a distance penalty to suppress unnecessary end-effector displacement, a smoothness penalty for abrupt actions, an orientation penalty to maintain consistent end-effector pose, a time penalty to encourage efficient completion, and a force-control penalty when the contact force exceeds the safety range. A success bonus is given when all four regions are successfully reached. The complete environment reward is: 


Here _p_ force is triggered when the total contact force _f_ total exceeds the safety range. All main experiments use the dense reward in Eq. (10); the sparse-reward ablation in Sec. IV-I retains only the success reward. This _rt_ is the original reward in Eq. (9), which is modified by the baseline penalty to obtain the final PPO reward _rt_<sup>_′_=</sup><sup>_rt−β_2</sup><sup>_d_.</sup> 

Evaluation uses deterministic rollouts without exploration noise and reports statistics over 50 episodes. During training, the policy introduces stochastic exploration through a Gaussian distribution (log _σ_ = _−_ 5 _._ 5); during evaluation, the policy mean is executed to avoid sampling noise in performance estimation. In addition, the object initial position is randomized within _±_ 2cm in each episode to evaluate execution stability under common positioning errors. Unless otherwise stated, RL training and key validations are repeated with three random seeds (22, 32, 42). Key metrics include task success rate, completion steps, and force-safety statistics, including peak contact force and the proportion of force readings above safety 

thresholds. All RL training and evaluation are conducted on an NVIDIA A100-SXM4-80GB GPU. 

## _C. Multi-policy Success Rate Comparison_ 

We compare ACT, Diffusion Policy, _π_ 0.5 [15], a 3Bparameter VLA foundation model, and PAC-ACT under a unified environment. All pretrained models are trained on 800 episodes of data (ACT: 200k steps, Diffusion Policy: 200k steps, _π_ 0.5: 20k steps). Evaluation is performed on the Contour task and Square Assembly. 

TABLE I 

SUCCESS RATE COMPARISON ACROSS POLICIES 

|Method|Contour|Square Assembly|
|---|---|---|
|ACT|60.0%<sup>_†_</sup>|51.2%|
|Diffusion Policy|60.0%<sup>_†_</sup>|77.8%|
|_π_0.5|79.0%|62.6%|
|**PAC-ACT (Ours)**|**100.0%**|**98.2%**|


Metal Touch Contour evaluation uses 50 deterministic rollout episodes, and all methods are tested under the same random seeds.<sup>_†_</sup> The identical 60.0% success rates of ACT and Diffusion Policy on Contour are an experimental coincidence; the two methods are evaluated independently using their own checkpoints pretrained on 800 trajectories. 

After RL fine-tuning, PAC-ACT improves the Contour success rate from 60% to 100% and Square Assembly from 51.2% to 98.2%. _π_ 0.5 achieves a 79.0% completion rate on Contour and 62.6% on Square Assembly, but it exhibits high inference latency variance and large GPU memory usage (44.15GB, Table II), which creates practical limitations for real-time deployment on edge devices. 

## _D. Online Inference Efficiency Comparison_ 

TABLE II 

ONLINE INFERENCE EFFICIENCY COMPARISON ACROSS POLICIES 

|Method|Mean (ms)|P95|P99|Mem. (GB)|
|---|---|---|---|---|
|ACT|98_._1_±_21_._7|143.2|176.7|2.27|
|Diffusion Policy|114_._9_±_42_._2|199.1|252.7|5.15|
|_π_0.5|182_._6_±_179_._8|653.4|739.7|44.15|
|**PAC-ACT (Ours)**|88_._1_±_23_._4|**125.6**|**172.5**|**2.30**<sup>_†_</sup>|


> _†_ During inference, PAC-ACT loads only the Actor; the Critic is used only for training and is not involved in deployed control. If the Actor-Critic is loaded together, peak GPU memory is 2.59GB. GPU memory is the peak inference-process GPU memory reported by NVML, including model weights, CUDA context, rendering buffers, and other allocations. The peak memory of _π_ 0.5 includes the overhead of the multi-process VLA inference pipeline, of which PyTorch tensor memory is approximately 13.8GB. 

The results in Table II mainly reflect online deployment overhead under the unified implementation and measurement protocol used in this paper. ACT deterministically decodes action chunks [3], and PAC-ACT also performs only an Actor forward pass at deployment, so both methods maintain low mean and tail latency. Diffusion Policy requires multi-step denoising or Langevin sampling to generate actions during inference [12], and its measured mean latency, P95, and P99 

are correspondingly higher than those of ACT-style policies. In comparison, _π_ 0.5 combines a PaliGemma vision-language backbone, high-level semantic reasoning, and a flow-matching action expert to generate continuous action chunks [15], resulting in a larger model and a more complex inference chain. The more direct deployment difference lies in resource usage: related efficient VLA work identifies limited compute and GPU memory on robotic platforms as an important bottleneck for deploying large-scale VLAs [32]. Consistent with this observation, _π_ 0.5 reaches a peak GPU memory usage of 44.15GB in our test, far above ACT, Diffusion Policy, and PAC-ACT. PAC-ACT achieves a mean inference latency of 88.1ms, approximately 10% lower than ACT (98.1ms), because removing the CVAE module simplifies the computation graph. Its P95 tail latency of 125.6ms is the lowest among all methods, indicating stable inference latency. When only the Actor is deployed, GPU memory usage is 2.30GB, essentially matching ACT’s 2.27GB and making the model size and memory footprint closer to edge-deployment requirements. Real-time deployment on edge devices such as NVIDIA Orin remains to be measured in future work. 

## _E. Data Scaling and Performance Bottleneck Analysis_ 


Fig. 3. Success-rate curves of ACT behavior cloning under different demonstration dataset sizes. As the number of expert demonstrations increases, performance improves on Diamond, Contour, and Cross, but the marginal gain gradually diminishes at larger data scales. The results indicate that pure behavior cloning can learn basic contact trajectories but remains vulnerable to accumulated out-of-distribution errors in long-horizon continuous contact tasks, leading to a performance bottleneck. 

_1) Data Scaling Effect of Behavior Cloning:_ The behavior cloning success rate of ACT shows clear diminishing returns as the dataset size increases (Fig. 3): Diamond reaches 69%, Cross 37%, and Contour 60%. Cross contains observationaction ambiguity because the end-effector repeatedly passes through the same center region, and its success rate remains only 37% even with 800 episodes. When the Contour dataset is expanded to 1600 episodes, the success rate increases to 66%, only 6 percentage points above the 800-episode baseline. This persistent diminishing return is consistent with prior observations that behavior cloning remains vulnerable to error accumulation under distribution shift [4], [5]. 


Fig. 4. Success rates of different policies across manipulation tasks and the convergence process of PAC-ACT. (a) Task-level success rate comparison on Diamond, Cross, Contour, and Square (robomimic), including Diffusion Policy, ACT, and PAC-ACT. (b) PAC-ACT training convergence on Diamond and Contour in Metal Touch; shaded regions indicate local fluctuations in rollout success rate, and the horizontal dashed line marks the 95% success-rate threshold. (c) PAC-ACT training process on Square (robomimic); the purple curve shows the 20-rollout filtered trend, and the light purple region indicates the corresponding 20–80% fluctuation range. 

_2) PAC-ACT Breaks the Performance Bottleneck:_ After applying PAC-ACT to an ACT model pretrained on 800 episodes (Fig. 4), the Contour success rate increases from 60% to 100%, and Square Assembly improves from 51.2% to 98.2%. This improvement comes from the complementary roles of imitation learning and RL: BC learns basic contact skills and temporal structure from demonstrations, while RL fine-tuning enables the policy to develop error-recovery behavior through environmental interaction [19]–[21]. 

The convergence analysis on Contour shows that PAC-ACT first reaches a 100% rollout success rate at approximately 100k PPO steps and remains above 95% from around 150k steps onward. The early-stage success rate is 18.75% and rises to 72.2% at approximately 80k steps, indicating a smooth and stable learning process. The final policy maintains a 100% success rate within approximately 320k total training steps. By contrast, the Diamond task reaches a 95% rollout success rate at around 250k steps, converging more slowly than Contour and reflecting the higher training difficulty of this precision contact task. 

## _F. Analysis of RL Fine-tuning Effect_ 

After fine-tuning, PAC-ACT achieves an approximately 2.8fold reduction in completion steps (485.4 _→_ 170.6) and an approximately 2.8-fold reduction in duration (48.5s _→_ 17.1s). Before fine-tuning, ACT typically terminates due to timeout when it fails and reaches only 3.14 regions on average. After fine-tuning, the policy reliably reaches all four regions and completes the task before the time limit. Repeated validation with three random seeds (22, 32, 42) shows that all seeds eventually reach a 100% rollout success rate, confirming training stability. 

TABLE III 

COMPARISON BEFORE AND AFTER PAC-ACT FINE-TUNING (CONTOUR TASK, 50-EPISODE EVALUATION) 

|Metric<br>ACT (Before RL)<br>PAC-ACT (After RL)|
|---|
|Success (4 regions)<br>60%<br>100%|
|Touched regions (/4)<br>3.14<br>4.0|
|Completion steps<br>485.4<br>170.6|
|Episode duration<br>48.5s<br>17.1s|
|During validation, the maximum episode duration is 60s (600 steps), and an|


episode terminates early after all four regions are reached. This duration limit differs from the 512-step episode limit used during RL training. Validation is repeated with three random seeds (22, 32, 42), and all seeds eventually reach a 100% rollout success rate. 

We also retain an early reproduction experiment with a changed end-effector probe to examine task-completion adaptation under end-tool geometry variation. In this experiment, the probe radius is increased from 1.5mm to 2.5mm, and the full pipeline from pretraining to RL fine-tuning is reproduced. The policy reaches a final rollout success rate of 99.7%, with a peak of 100%, and all 50 deterministic validation episodes successfully reach the four regions, with an average completion length of 68 _._ 8 _±_ 20 _._ 8 steps. Because the larger contact radius changes the pressure-equivalent threshold and this experiment uses an earlier reward configuration, we include it only as a supplementary observation of task-completion adaptation under end-tool geometry changes. Force-safety conclusions are based on the main experiments with the unified probe setting and evaluation protocol. 

## _G. Force Safety Analysis_ 

We conduct a dedicated force-safety evaluation, comparing ACT, Diffusion Policy, _π_ 0.5, and PAC-ACT under identical conditions: the same 50 randomized seeds and a 300-step execution horizon. The force/torque sensor provides 6-axis readings at every control step, from which we compute the total contact force magnitude _f_ total = ~~�~~ _fx_<sup>2</sup> + _fy_<sup>2</sup> + _fz_<sup>2</sup> . The results are summarized in Table IV. 

BC-trained ACT, Diffusion Policy, and _π_ 0.5 all exhibit notable force-safety issues. ACT has a median peak contact force of 105.4N, almost twice the 60N safety threshold. Although _π_ 0.5 and Diffusion Policy have lower median forces, 8.35N and 6.76N respectively, they still produce hazardous force events above 60N: Diffusion Policy has a 2.0% ratio of force readings above 60N, with 56% of episodes containing at least one above-threshold force reading; for _π_ 0.5, the corresponding ratios are 5.1% and 88%. These results may be related to transient action fluctuations produced by generative or samplingbased action generation under contact. ACT reaches an extreme maximum force of 8452.5N, corresponding to a collision event in which the policy pushes the end-effector into the rigid table surface under an out-of-distribution state. Because pure vision-action policies rely only on visual observations and joint encodings during inference, they lack force-sensing feedback. In contrast, contact-manipulation and impedancecontrol studies generally emphasize the need to regulate robotenvironment interaction forces [6], [7]. Therefore, when contact geometry deviates from the demonstration distribution, pure visual behavior-cloning policies may struggle to detect and correct force anomalies in time. 

PAC-ACT effectively improves force safety. Compared with ACT, PAC-ACT reduces the median peak force to 20.74N, below the 60N safety threshold. The mean contact force is also reduced by one order of magnitude (38.67N _→_ 3.92N) and is lower than those of Diffusion Policy and _π_ 0.5. Only 0.3% of force readings exceed 30N, and only 0.1% exceed 60N, reducing the ratio of force readings above 60N by 46 times relative to ACT. The maximum peak force is reduced by 70 times (8452.5N _→_ 120.9N), and the proportion of episodes with any force reading above 60N drops from 20% for ACT, 56% for Diffusion Policy, and 88% for _π_ 0.5 to 6%. These improvements are associated with the force-safety reward term in the RL objective, which penalizes excessive contact force and encourages gentler and more compliant interaction behavior. 

## _H. Task Completion Efficiency Analysis_ 

Beyond force-safety metrics, PAC-ACT also improves task success and completion efficiency. Based on Table III and Fig. 5(b), the Contour task success rate increases from 60% to 100%, the average completion length decreases from 485.4 to 170.6 steps, and the average episode duration decreases from 48.5s to 17.1s, a reduction of approximately 2.8 times. Before fine-tuning, ACT often terminates near the time limit and reaches only 3.14 regions on average. After fine-tuning, PACACT reaches all four regions in all 50 deterministic validation 


Fig. 5. Comparison between ACT and PAC-ACT in force control and taskcompletion efficiency. (a) Contact force distribution comparison; PAC-ACT maintains a more concentrated force distribution and reduces above-threshold hazardous force spikes. (b) Force-safe success rate and completion steps; bars indicate the proportion of successful episodes whose trajectory-level maximum contact force max _t f_ total remains below 60N, and the line indicates average completion steps. 

episodes and terminates early. These results show that chunklevel PPO post-training not only improves task success but also substantially reduces the interaction steps required to satisfy the success condition. 

Qualitative playback of validation videos indicates that the efficiency improvement is not simply uniform acceleration over the entire trajectory, but rather a redistribution of speed across different motion phases. Compared with the policy before fine-tuning, PAC-ACT shows reduced highfrequency end-effector jitter and smoother overall motion. During horizontal or non-contact movements between adjacent contact regions, the end-effector approaches the next target region with larger step sizes, while it slows down and makes smaller adjustments near corners, contact points, or locations requiring precise positioning. This observation is consistent with the quantitative reduction in completion steps: the policy mainly compresses non-critical movement phases while retaining more cautious localization near contact regions. This analysis is based on qualitative video playback and is intended to explain the behavioral manifestation of improved taskcompletion efficiency, rather than serving as an independent validation of a force-control mechanism. 

## _I. Ablation Study_ 

To validate the Actor-Critic architectural choices, we evaluate two ablation variants: (1) flat-decoder critic, where the Critic retains the full Transformer decoder and flattens the decoded _K × da_ action chunk sequence before feeding it into the value head; (2) CVAE-retained actor, where the Actor keeps the CVAE latent module while all other components remain unchanged. All ablations use exactly the same training hyperparameters as our method, including 16 parallel environments, learning rate 1 _×_ 10<sup>_−_6</sup> , 8 PPO update epochs, and _β_ 2 = 2 _._ 0. Only the corresponding module is changed, ensuring that differences arise from architectural design. 

Figure 6 and Table V show the training process and quantitative comparison of the three variants. 

The flat-decoder critic retains the full Transformer decoder for value estimation. Experiments show that this variant can 

TABLE IV 

FORCE-SAFETY COMPARISON (CONTOUR TASK, 50 EPISODES, 300 STEPS PER EPISODE) 

|Metric|ACT|Diffusion Policy|_π_0.5|PAC-ACT (Ours)|
|---|---|---|---|---|
|Median peak force|105.40N|6.76N|8.35N|20.74N|
|Mean force (_µ ± σ_)<br>|38_._67_±_94_._12N<br>|12_._31_±_60_._15N<br>|32_._99_±_221_._75N<br>|3_._92_±_4_._31N<br>|
|Maximum peak force|8452.5N|3144.6N|7349.0N|120.9N|
|Ratio of force readings _>_30N|15.0%|7.6%|13.8%|0.3%|
|Ratio of force readings _>_60N|4.6%|2.0%|5.1%|0.1%|
|Ratio of episodes with force _>_60N|20%|56%|88%|6%|


Evaluation uses 50 episodes with 300 steps per episode and randomized object initial positions within _±_ 2cm. The force/torque sensor provides 6-axis readings at each control step, and total contact force is computed as _f_ total = ~~�~~ _fx_<sup>2</sup> + _fy_<sup>2</sup> + _fz_<sup>2</sup> . The 60N threshold is the safety-force threshold for Metal Touch. 

TABLE V 

QUANTITATIVE COMPARISON OF ARCHITECTURE ABLATIONS (UP TO 154K STEPS) 

|Variant|Final-window mean success<sup>_†_</sup>|Std. dev.|
|---|---|---|
|Ours|96.4%|_±_3.0%|
|Flat-decoder critic|88.0%|_±_7.4%|
|CVAE-retained actor|83.1%|_±_7.8%|


> _†_ Mean rollout success rate over the final 20 evaluations. 


Fig. 6. Training-process comparison for architecture ablations. Curves show rollout success rate over training steps for the three variants, smoothed with a 10-window moving average. 

also reach a peak rollout success rate of 100%, indicating that it is not an infeasible architecture. However, its mean over the final 20 evaluations is only 88.0% with a standard deviation of _±_ 7.4%, and the success rate fluctuates between 70% and 100%, showing insufficient convergence stability. By contrast, our encoder-value Critic achieves a final-window mean of 96.4% with a standard deviation of only _±_ 3.0%, maintaining high success while converging smoothly. In addition, the flatdecoder critic retains the full Transformer decoder, introducing approximately 17% additional parameters and computational overhead (129M _→_ 151M parameters), which increases overfitting risk. The hidden representation produced by the encoder already contains sufficient information for state-value estimation, allowing stable value regression without the decoder. 

The CVAE-retained actor reaches a final-window mean of only 83.1% with a standard deviation of _±_ 7.8%, lower than the 

96.4% of our method. This is because the CVAE latent variable _z ∼N_ (0 _, I_ ) makes the same observation produce different action outputs during forward passes, while the baseline MSE penalty _β_ 2 _∥_ **a** _θ −_ **a** base _∥_<sup>2</sup> in Eq. (9) continuously penalizes these inherent stochastic fluctuations. This conflicts with the gradient direction of the PPO objective and lowers the effective signal-to-noise ratio of policy updates. The result indicates that retaining the CVAE causes a measurable final performance loss under the hybrid KL constraint framework. 

In summary, the ablation study shows that (1) the encodervalue Critic outperforms the flat-decoder critic in both finalwindow mean success rate (96.4% vs. 88.0%) and training stability ( _±_ 3.0% vs. _±_ 7.4%) while incurring lower computational overhead; and (2) removing the CVAE helps avoid gradient conflict between an additional source of stochasticity and the KL constraint, as the CVAE-retained actor achieves only an 83.1% final-window mean, confirming the necessity of CVAE removal under the hybrid KL framework. 

To further examine robustness to reward sparsification, we conduct an additional sparse-reward ablation. This ablation is not the main experimental setting: the main experiments use the dense reward in Eq. (10), whereas the sparse ablation retains only the success reward (success <u>bonus=12.0)</u> and sets the region-touch reward, distance guidance, smoothness, orientation, time, and force-control terms to zero. Except for the reward, all other settings are the same as the Contour main experiment: the policy is initialized from the same ACT model pretrained on 800 episodes, the initial pose is randomized within _±_ 2cm, the training limit is set to 10000 episodes, and the hybrid KL behavior-prior constraint is retained. No additional demonstration trajectory replay or demonstrationaction supervision is used during training. 

As shown in Fig. 7, under this setting PAC-ACT with _β_ 1 = 3 _._ 0 still converges to a 100% rollout success rate and maintains a structured trajectory close to the contour action sequence, indicating that the pretrained action chunking policy provides a strong behavior prior for chunk-level PPO. As a comparison, we set the KL coefficient to zero ( _β_ 1 = 0) under the same sparse-reward setting. Qualitative video playback and end-effector trajectory sampling show that this policy deviates from the pretrained ACT contour temporal action sequence early in training and instead forms shortcut behavior 


Fig. 7. Training success rate and end-effector trajectory structure diagnosis in the sparse-reward ablation. Left: rollout success-rate curves under different reward and regularization configurations on the Contour task; shaded regions indicate local fluctuations, and the dashed line marks the 95% successrate threshold. Right: top-view trajectory from one validation rollout for the corresponding policy, where blue points visualize the end-effector trajectory sampled uniformly by arc length. When only the success reward is retained but the KL constraint is kept, the policy maintains structured motion close to the contour action sequence. When the KL constraint is removed under the same sparse-reward condition, later rollout success can partially recover, but the sampled end-effector points show a clearly dispersed boundary-touching exploration pattern, indicating that success-rate metrics may mask degradation of temporal structure. 

that directly touches multiple target boundaries to obtain the success reward. Because this behavior can still trigger the sparse success condition, the later local rollout window reaches a maximum success rate of 88.5%; however, under the same training limit, the cumulative total success rate is only 22.0%, and the final rollout window also drops to 72.7%. Therefore, the success-rate rebound without KL does not indicate recovery of structured contact skills, but instead shows that relying only on sparse success metrics can obscure degradation of temporal structure. This comparison indicates that KL regularization is a key mechanism for maintaining the pretrained behavior manifold and preventing structured behavior collapse under sparse rewards. 

## V. DISCUSSION 

The experiments reveal a paradigm in which imitation learning provides a behavior prior and reinforcement learning performs behavior customization, consistent with the basic idea of recent RL fine-tuning studies on pretrained policies [19]–[21], [24]. The behavior cloning stage learns basic contact skills and temporal action structure, while the RL stage selectively refines these skills through environmental reward feedback, improving task success, force safety, and time efficiency while preserving the basic behavior structure. The ablations in Sec. IV-I further validate the design at the architectural level: the encoder-value Critic outperforms the flat-decoder critic in final-window mean success rate (96.4% vs. 88.0%) and stability ( _±_ 3.0% vs. _±_ 7.4%) with lower computational overhead; removing the CVAE avoids conflict between an additional stochasticity source and the KL constraint, while the CVAE-retained actor achieves only an 83.1% final-window mean, further supporting the design choice. 

Pretrained action chunking policies can reduce sensitivity to reward engineering during RL, but this does not mean that the main method does not require dense rewards. The main experiments use dense rewards to obtain the best task completion efficiency and force safety, while the sparse-reward experiment is only an additional ablation. The results show that, when the KL constraint and frozen baseline policy constraint are retained, keeping only the success bonus still allows convergence under randomized initial poses; when KL is removed, local success may partially recover, but the endeffector trajectory structure clearly degrades. This indicates that the pretrained action chunking policy provides a strong low-level behavior prior, and that the behavior-prior constraint is critical for preventing collapse of structured contact skills under sparse rewards. 

The force-safety results deserve particular attention. The substantial reduction in extreme force events, with the peak force decreasing from 8452.5N to 120.9N, shows that a pretrained ACT policy can produce unsafe forces in a nonnegligible fraction of episodes even when it achieves a reasonable task success rate. Such events may be missed in pure BC evaluation because (a) they occur in out-of-distribution states that BC evaluation may not systematically probe, and (b) they do not necessarily cause immediate task failure: a policy may generate unsafe force while still completing part or all of the task. RL fine-tuning with an appropriate safety reward provides a principled mechanism for detecting and mitigating such hidden failures, which is relevant to industrial scenarios with strict contact-safety requirements. 

This study has several limitations. The experiments are mainly conducted in simulation, and sim-to-real transfer of the learned policy remains to be validated. The current experiments primarily examine object initial-position perturbations and multi-trajectory generalization, but do not cover visual or physical perturbations such as viewpoint changes, lighting variation, or dynamics-parameter changes. A more systematic robustness evaluation is left for future work. Although removing the CVAE module simplifies RL optimization, it may limit the ability of the policy to represent highly multi-modal action distributions. Future work can explore regularized CVAE integration that preserves multimodality while maintaining optimization stability. Finally, the current framework still requires task-specific reward design; developing more automated reward specification methods would further reduce the engineering burden of RL-based policy customization. 

## VI. CONCLUSION 

This paper presents PAC-ACT, a chunk-level PPO posttraining framework for pretrained ACT policies. Through MDP reformulation, ACT-transferred Actor-Critic design, and hybrid KL constraints, PAC-ACT structurally aligns action chunking policies with RL optimization. On Metal Touch and Square Assembly, the method improves task success (Contour 60% _→_ 100%, Square 51.2% _→_ 98.2%) and execution efficiency, reducing completion steps by 2.8 times. Dedicated force-safety analysis shows that hazardous force events are 

reduced by 46 times and peak contact force by 70 times. All improvements are achieved while maintaining low latency and low GPU memory usage (88.1 _±_ 23.4ms inference, 2.30GB GPU memory), indicating the potential of the method for further adaptation and deployment in industrial precision contact scenarios. 

Future work will extend the evaluation to real robot platforms to validate sim-to-real transfer, explore more complex multi-stage manipulation tasks, and investigate more general reward design mechanisms that can further reduce the engineering cost of RL-based policy customization. 

## REFERENCES 

- [1] F. Chaumette and S. Hutchinson, “Visual servo control. I. Basic approaches,” _IEEE Robotics & Automation Magazine_ , vol. 13, no. 4, pp. 82–90, 2006, doi: 10.1109/MRA.2006.250573. 

- [2] V. Kyrki, D. Kragic, and H. I. Christensen, “Measurement errors in visual servoing,” _Robotics and Autonomous Systems_ , vol. 54, no. 10, pp. 815–827, 2006, doi: 10.1016/j.robot.2006.05.002. 

- [3] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” in _Proc. Robotics: Science and Systems (RSS)_ , 2023. 

- [4] S. Ross, G. Gordon, and D. Bagnell, “A reduction of imitation learning and structured prediction to no-regret online learning,” in _Proc. International Conference on Artificial Intelligence and Statistics (AISTATS)_ , PMLR, vol. 15, pp. 627–635, 2011. 

- [5] A. Mandlekar, D. Xu, J. Wong, S. Nasiriany, C. Wang, R. Kulkarni, L. Fei-Fei, et al., “What matters in learning from offline human demonstrations for robot manipulation,” in _Proc. Conference on Robot Learning (CoRL)_ , PMLR, vol. 164, pp. 1678–1690, 2022. 

- [6] M. Suomalainen, Y. Karayiannidis, and V. Kyrki, “A survey of robot manipulation in contact,” _Robotics and Autonomous Systems_ , vol. 156, Art. no. 104224, 2022, doi: 10.1016/j.robot.2022.104224. 

- [7] N. Hogan, “Impedance control: An approach to manipulation: Part I— Theory,” _Journal of Dynamic Systems, Measurement, and Control_ , vol. 107, no. 1, pp. 1–7, 1985, doi: 10.1115/1.3140702. 

- [8] D. Tian, O. Celik, and G. Neumann, “Chunking the critic: A transformer-based soft actor-critic with n-step returns,” arXiv preprint arXiv:2503.03660, 2025. 

- [9] Q. Li, Z. Zhou, and S. Levine, “Reinforcement learning with action chunking,” in _Proc. Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. 

- [10] R. Cadene, S. Alibert, F. Capuano, M. Aractingi, A. Zouitine, P. Kooijmans, et al., “LeRobot: An open-source library for end-to-end robot learning,” in _Proc. International Conference on Learning Representations (ICLR)_ , 2026. 

   - [19] J. Yang, B. Zhu, J. Chen, and Y.-G. Jiang, “Actor-critic for continuous action chunks: A reinforcement learning framework for long-horizon robotic manipulation with sparse reward,” in _Proc. AAAI Conference on Artificial Intelligence (AAAI)_ , vol. 40, no. 22, pp. 18692–18700, 2026, doi: 10.1609/aaai.v40i22.38937. 

   - [20] A. Kumar, A. Zhou, G. Tucker, and S. Levine, “Conservative Q- learning for offline reinforcement learning,” in _Proc. Advances in Neural Information Processing Systems (NeurIPS)_ , 2020. 

   - [21] I. Kostrikov, A. Nair, and S. Levine, “Offline reinforcement learning with implicit Q-learning,” in _Proc. International Conference on Learning Representations (ICLR)_ , 2022. 

   - [22] L. Brunke, M. Greeff, A. W. Hall, Z. Yuan, S. Zhou, J. Panerati, and A. P. Schoellig, “Safe learning in robotics: From learning-based control to safe reinforcement learning,” _Annual Review of Control, Robotics, and Autonomous Systems_ , vol. 5, pp. 411–444, 2022, doi: 10.1146/annurevcontrol-042920-020211. 

   - [23] Open X-Embodiment Collaboration, A. O’Neill, A. Rehman, et al., “Open X-Embodiment: Robotic learning datasets and RT-X models,” in _Proc. IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 6892–6903, 2024, doi: 10.1109/ICRA57147.2024.10611477. 

   - [24] A. Z. Ren, J. Lidard, L. L. Ankile, A. Simeonov, P. Agrawal, A. Majumdar, et al., “Diffusion policy policy optimization,” arXiv preprint arXiv:2409.00588, 2024. 

   - [25] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in _Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2016. 

   - [26] A. Vaswani et al., “Attention is all you need,” in _Proc. Advances in Neural Information Processing Systems (NeurIPS)_ , 2017. 

   - [27] S. Nair, A. Rajeswaran, V. Kumar, C. Finn, and A. Gupta, “R3M: A universal visual representation for robot manipulation,” in _Proc. Conference on Robot Learning (CoRL)_ , PMLR, vol. 205, pp. 892–909, 2023. 

   - [28] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” arXiv preprint arXiv:1707.06347, 2017. 

   - [29] J. Schulman, S. Levine, P. Abbeel, M. Jordan, and P. Moritz, “Trust region policy optimization,” in _Proc. International Conference on Machine Learning (ICML)_ , 2015. 

   - [30] E. Todorov, T. Erez, and Y. Tassa, “MuJoCo: A physics engine for model-based control,” in _Proc. IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2012. 

   - [31] Y. Zhu, J. Wong, A. Mandlekar, R. Martin-Martin, A. Joshi, K. Lin, et al., “robosuite: A modular simulation framework and benchmark for robot learning,” arXiv preprint arXiv:2009.12293, 2020. 

   - [32] Y. Yue, Y. Wang, B. Kang, Y. Han, S. Wang, S. Song, J. Feng, and G. Huang, “DeeR-VLA: Dynamic inference of multimodal large language models for efficient robot execution,” in _Proc. Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 

- [11] K. Sohn, H. Lee, and X. Yan, “Learning structured output representation using deep conditional generative models,” in _Proc. Advances in Neural Information Processing Systems (NeurIPS)_ , 2015. 

- [12] C. Chi, S. Feng, Y. Du, Z. Xu, E. Cousineau, B. Burchfiel, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” in _Proc. Robotics: Science and Systems (RSS)_ , 2023. 

- [13] N. M. Shafiullah, Z. Cui, A. Altanzaya, and L. Pinto, “Behavior transformers: Cloning _k_ modes with one stone,” in _Proc. Advances in Neural Information Processing Systems (NeurIPS)_ , 2022. 

- [14] B. Zitkovich et al., “RT-2: Vision-language-action models transfer web knowledge to robotic control,” in _Proc. Conference on Robot Learning (CoRL)_ , PMLR, vol. 229, pp. 2165–2183, 2023. 

- [15] Physical Intelligence, K. Black, N. Brown, J. Darpinian, et al., “ _π_ 0.5: a vision-language-action model with open-world generalization,” arXiv preprint arXiv:2504.16054, 2025. 

- [16] P. Florence, C. Lynch, A. Zeng, et al., “Implicit behavioral cloning,” in _Proc. Conference on Robot Learning (CoRL)_ , 2021. 

- [17] Y. Seo and P. Abbeel, “Coarse-to-fine Q-network with action sequence for data-efficient reinforcement learning,” arXiv preprint arXiv:2411.12155, 2024. 

- [18] T. Haarnoja et al., “Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor,” in _Proc. International Conference on Machine Learning (ICML)_ , 2018. 

