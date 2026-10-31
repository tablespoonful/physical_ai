---
title: "Koopman Dreamer: Spectrally Constrained Latent Dynamics for Stable World-Model Imagination"
date: "2026-07-22"
authors: "Jiaqi Li; Xinglong Zhang; Haibin Xie; Yixing Lan; Wei Pan; Xin Xu"
url: https://arxiv.org/abs/2607.19719
pdf: https://arxiv.org/pdf/2607.19719
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2607.19719)** / [論文ページ](https://arxiv.org/abs/2607.19719)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# Koopman Dreamer: Spectrally Constrained Latent Dynamics for Stable World-Model Imagination 

Jiaqi Li, Xinglong Zhang, Haibin Xie, Wei Jiang, Yixing Lan, Wei Pan, and Xin Xu 

**_Abstract_ —Latent world models improve sample efficiency in continuous control by optimizing policies over imagined latent trajectories, but common neural transitions offer limited direct control over modal persistence and error accumulation in long rollouts. We propose Koopman Dreamer, a Dreamer-style world model with a spectrally constrained deterministic latent dynamics core. Its Koopman-inspired backbone uses two-dimensional rotation–scaling blocks with bounded radii to represent damping, rotation, and near-periodic modes. Linear and low-rank bilinear action terms capture global and state-dependent control effects, while stochastic-state modulation supplies local correction information. To reduce the mismatch between posteriorconditioned training and prior-only imagination, the model combines posterior-conditioned EMA teacher targets with onestep consistency, multi-step rollout, and open-loop observationprediction objectives. We further derive a multi-step rollout-error bound that separates amplification by the spectral backbone and bilinear interaction from the additive effects of stochasticstate mismatch and modeling residuals, clarifying the trade-off between error attenuation and long-term information retention. Experimental results on proprioceptive continuous-control tasks from the DeepMind Control Suite and UAV-LiDAR autonomous navigation demonstrate that Koopman Dreamer improves the stability of long-horizon latent rollouts and achieves stronger closed-loop control performance on tasks that rely on highquality multi-step imagination.** 

**_Note to Practitioners_ —World-model-based controllers can reduce costly interaction with physical systems by training policies on trajectories imagined through a learned dynamics model, but one-step prediction errors may accumulate and distort policy updates or control decisions. Koopman Dreamer replaces the conventional deterministic latent transition in a Dreamerstyle controller with a spectrally structured transition whose modal persistence can be explicitly bounded, while retaining the observation, reward, continuation, and actor–critic components. It is intended for continuous-control applications that rely on recursive multi-step prediction, including robotic motion and autonomous navigation. In simulation, it outperformed DreamerV3 on eight of nine proprioceptive tasks and increased UAV-LiDAR target success from 53.8% to 73.8%. Because the most contractive spectral setting was not always optimal, practitioners should tune the spectral range using both decoded observation-prediction accuracy and closed-loop performance. Although validation is currently simulation-based, the structured transition can be adapted to other learned-model control and planning frameworks; physical deployment still requires task-specific robustness evaluation and safety assurance.** 

**_Index Terms_ —model-based reinforcement learning, latent world model, Koopman representation, spectral constraint, continuous control, latent imagination.** 

Jiaqi Li, Xinglong Zhang, Haibin Xie, Wei Jiang, Yixing Lan, and Xin Xu are with the College of Intelligence Science and Technology, National University of Defense Technology, Changsha, China. Wei Pan is with the School of Engineering, Newcastle University, Newcastle-upon-Tyne, UK. Corresponding authors: Xinglong Zhang. 

## I. INTRODUCTION 

**M** ODEL-BASEDefficiency of interactionreinforcementwith learningreal environmentsimproves theby learning environment dynamics [1]–[3]. Instead of relying entirely on trial and error in the environment, a world model can generate future trajectories under learned dynamics and use these imagined trajectories to train the policy and value function [4]–[7]. Latent world models are particularly important for continuous control: they compress observation histories into compact hidden states and perform state prediction, reward prediction, and policy optimization in latent space, thereby avoiding direct long-horizon dynamics modeling in the original high-dimensional observation space [5], [6], [8], [9]. 

A complete latent world model typically consists of observation representation learning, latent-state transition, prediction heads, and latent-space policy optimization [6], [9]. The observation encoder maps task observations into compact representations used to infer latent states, while the dynamics module recursively propagates these states over time. Prediction heads decode the resulting latent states to reconstruct observations and estimate rewards and episode-continuation flags, and the policy and value function are optimized on trajectories imagined through the learned dynamics. Consequently, accurate and stable long-horizon latent transitions are important not only for future observation prediction, but also for imagined-return estimation and policy learning. 

Recent latent world models commonly parameterize their transitions with flexible recurrent or feed-forward neural networks [5]–[7], [9]. These models are highly expressive, but their objectives do not usually expose or directly parameterize the modal properties of deterministic latent propagation. Consequently, contraction, persistence, and oscillation emerge implicitly from data and optimization. This is not evidence that generic neural transitions are necessarily unstable; rather, it makes their long-horizon behavior difficult to regulate and diagnose. Because Dreamer-style actor–critic updates depend on recursively imagined trajectories, errors in latent transition, reward prediction, and continuation prediction can compound with horizon and bias the resulting return targets. 

Dynamics in continuous-control tasks are not completely unstructured. Legged locomotion, pendulum control, robotic reaching, and velocity-control tasks often contain smooth action responses, damping, near-periodic motion, and locally linear evolution [10], [11]. If such long-horizon patterns can be explicitly represented in latent space, imagined trajectories produced by the world model may become more stable and 

2 

easier to diagnose. Koopman operator theory provides a useful perspective: a nonlinear system can be advanced by a linear operator in an appropriate observable-function space [12]– [15]. Its structural advantage for world models is that the learned latent transition can be organized around an explicit evolution operator, so that contraction, persistence, and oscillatory behavior are controlled by spectral quantities, providing a direct mechanism to analyze and regulate multi-step error growth. Although a finite-dimensional neural representation can only approximate the Koopman property, a Koopmaninspired linear backbone therefore provides a natural way to inject stability-oriented and diagnostically interpretable structure into long-horizon latent dynamics [16]–[18]. 

This paper proposes Koopman Dreamer. Its main idea is to make long-horizon deterministic-state propagation an explicitly structured component of the world model, instead of treating it only as a generic function-approximation problem. The complete deterministic latent state is organized as a Koopmaninspired evolution state, and its autonomous dynamics are parameterized by a spectral-radius-controlled linear backbone. The remaining components are arranged around this backbone. A linear action term and a bilinear state–action interaction term adapt the backbone to controlled nonlinear dynamics, stochastic-state modulation carries local posterior correction information into the deterministic transition, and posteriorconditioned teacher and rollout objectives reduce the mismatch between posterior training states and prior imagination states. In this way, Koopman Dreamer retains the Dreamer-style framework for latent imagination and actor–critic learning while concentrating its structural contribution on spectrally constrained latent dynamics. 

We evaluate Koopman Dreamer on proprioceptive tasks from the DeepMind Control Suite [10], [11] and on simulated UAV navigation [19] with vectorized LiDAR observations [20]. Open-loop evaluations show the most consistent improvements in predicting proprioceptive observations and velocity. Reward prediction also improves on most tasks. In UAV navigation, Koopman Dreamer achieves a higher success rate and a lower overall failure rate than DreamerV3. A spectral-radius sweep and structural ablations provide additional exploratory evidence regarding the roles of modal contraction, exponential moving average (EMA) teacher targets, and state-dependent action effects. 

The main contributions of this paper are threefold: 

- (i) We propose Koopman Dreamer for Dreamer-style continuous control. The deterministic latent state is propagated directly through a Koopman-inspired spectral backbone composed of two-dimensional rotation–scaling blocks with bounded modal radii. This parameterization explicitly represents the damping, persistence, and oscillation of latent modes through learnable modal radii and phases. 

- (ii) We adapt the spectral Koopman backbone to controlled nonlinear dynamics and posterior-free imagination. The transition combines a linear action term, a low-rank bilinear state–action interaction term, and stochastic-state modulation. On top of the standard DreamerV3 prior– posterior learning framework, we design Koopmanspecific supervision using posterior-conditioned teacher 

   - representations, EMA target projections, one-step Koopman consistency, multi-step teacher and prior rollouts, and open-loop observation prediction. Together, these components train the same structured transition under both observation-corrected training and observation-free imagination. 

- (iii) We establish a long-horizon error-propagation analysis for the controlled Koopman transition. The resulting multi-step bound separates autonomous operator amplification from controlled-interaction effects and additive stochastic and modeling residuals, explaining how the learned spectral radius balances error accumulation against the preservation of persistent dynamics. Experiments on DMC proprioceptive control and UAV-LiDAR navigation, including open-loop prediction, spectral-radius sensitivity analysis, and structural ablations, connect this mechanism to improved long-horizon prediction and closed-loop control. 

## II. RELATED WORK 

## _A. Latent World Models_ 

Latent world models encode observations or observation histories into compact hidden states and predict the future in latent space. Early model-based reinforcement-learning methods often relied on dynamics models defined either in the original observation/state coordinates or in manually designed compact state representations [2], [3]. Directly modeling observations can be high-dimensional and redundant, whereas hand-crafted state representations depend on task-specific engineering. These limitations motivate latent world models that learn predictive hidden states from data. Representative methods such as PlaNet and Dreamer combine observation encoding, latent-state transition, observation reconstruction, reward prediction, and policy optimization through stochastic state-space models, so that the hidden state can both explain observations and support future trajectory imagination [5], [6], [8], [9]. Although the observation front end depends on the representation provided by the environment, these models share the need to propagate the resulting latent state accurately over imagined trajectories. 

Modern latent world models differ in architecture, but they share the goal of learning compact dynamics that can support prediction, planning, or policy improvement. In PlaNet and the original Dreamer line, this role is played by recurrent deterministic memory coupled with stochastic state correction; in other model-based agents, latent dynamics are adapted to planning or actor–critic optimization [5]–[9]. Koopman Dreamer is also a learned latent dynamics model, but it constrains deterministic propagation through a spectral parameterization. This makes quantities such as contraction, rotation, and near-periodic modes part of the transition design rather than properties that must emerge only from data and loss terms. This paper therefore focuses on adding explicit modal structure to the deterministic dynamics core. It formulates deterministic latent-state propagation as a spectrally constrained, Koopman-inspired backbone and organizes observation prediction, reward prediction, episode-continuation prediction, and 

3 

latent-space policy optimization around this structured rollout mechanism. 

## _B. Koopman Representation Learning_ 

Koopman operator theory shows that nonlinear systems can be described by a linear operator in an appropriate observablefunction space [12]–[15]. Dynamic mode decomposition and extended dynamic mode decomposition estimate linear evolution operators from data, but they typically rely on manually designed observables [16], [22], [23]. Deep Koopman methods use neural networks to learn observable representations and train them jointly with reconstruction, linear-prediction, and multi-step prediction objectives [17], [18], [24]. These methods have been widely studied in system identification, prediction, and control [25]–[27]. 

Koopman representations have also been integrated directly with reinforcement learning and task-oriented control. Koopman Q-learning learns Koopman latent representations to identify dynamical symmetries for offline data augmentation [28]. Task-oriented Koopman control jointly learns a latent embedding, a Koopman operator, and a differentiable linear controller through end-to-end reinforcement learning, including applications with high-dimensional visual and LiDAR observations [29]. RoboKoop learns control-conditioned visual Koopman representations for off-policy robotic control [30]. Recent control-oriented studies have further combined Koopman models with model-based reinforcement learning for datadriven optimal control of unknown nonlinear systems [31], receding-horizon direct policy optimization for fixed-wing UAV trajectory tracking [32], and receding-horizon actor– critic learning for autonomous-vehicle motion planning [33]. 

Long-horizon prediction errors are closely related to the spectral properties of the dynamics operator. An unconstrained linear operator may amplify perturbations exponentially during recursive rollouts, whereas excessive contraction may erase persistent information [34], [35]. Spectral constraints regulate these behaviors through bounds on matrix norms, eigenvalue magnitudes, or structured operator parameterizations [15]. These ideas motivate structured evolution operators whose modal amplification, decay, and oscillation can be directly parameterized rather than left implicit. 

The preceding Koopman studies demonstrate that learned Koopman representations can support policy learning and control. The present work addresses a different aspect: the explicit spectral organization of the deterministic dynamics core inside a stochastic Dreamer-style latent world model for long-horizon recursive imagination. The deterministic latent state is propagated directly through a Koopman-inspired spectral backbone composed of two-dimensional rotation–scaling blocks, whose bounded radii and learnable phases govern contraction, persistence, and oscillation. Linear and bilinear action terms adapt this spectral backbone to state-dependent controlled dynamics. Posterior-conditioned teacher targets and prior-rollout objectives serve as supporting training mechanisms that allow the same structured transition to operate under observation-corrected representation learning and posteriorfree imagination. 

## III. PROBLEM FORMULATION 

We consider a partially observable continuous-control problem [1]. At time _t_ , the agent receives an observation _ot_ , takes an action _at_ according to the history _ht_ = ( _o≤t, a<t_ ), obtains a reward _rt_ , and receives an episode-continuation flag _ct ∈{_ 0 _,_ 1 _}_ . Here, _ct_ = 1 indicates that the episode continues after this step, whereas _ct_ = 0 indicates termination. The objective is to learn a policy _πψ_ ( _at | ht_ ) that maximizes the expected discounted return gated by continuation, _J_ ( _πψ_ ) = E _πψ_ [<sup>�</sup> _t_<sup>_∞_</sup> =0<sup>_γt_(�</sup><sup>_t_</sup> _i_ =0<sup>_−_1</sup><sup>_ci_)</sup><sup>_rt_],where</sup><sup>_ψ_denotesthe</sup> policy parameters, _γ ∈_ (0 _,_ 1), and the empty product is defined as 1. This formulation stops return accumulation after episode termination and is consistent with the continuation predictor used for imagined returns in Dreamer-style agents [9]. 

The latent world model compresses the history _ht_ into a hidden state and models transition, observation, reward, and episode continuation in latent space. Following the deterministic–stochastic state decomposition used by Dreamerstyle RSSM world models [5], [6], [9], we write the latent state as _yt_ = ( _ϕt, st_ ), where _ϕt ∈_ R<sup>_D_</sup> is the deterministic Koopman state and _st_ is the stochastic state. The deterministic component carries historical memory that can be recursively propagated over long horizons, while the stochastic component absorbs current-observation correction and unmodeled local factors. In the implementation, _st ∈{_ 0 _,_ 1 _}_<sup>_N×K_</sup> consists of _N_ groups of _K_ -way one-hot discrete stochastic variables. The categorical distributions are smoothed with unimix to prevent premature collapse of the stochastic state [8], [9], [36], [37]. In subsequent world-model and actor–critic training, _yt_ serves as a latent-space summary of the history _ht_ , and the policy is therefore optimized in latent space as _πψ_ ( _at | yt_ ). 

Instead of directly sampling the complete next state _yt_ +1, Koopman Dreamer separates deterministic propagation from the stochastic prior. Given _yt_ = ( _ϕt, st_ ) and action _at_ , the Koopman backbone first produces _ϕt_ +1 = _FK_ ( _ϕt, st, at_ ), and the prior network then predicts _pθ_ ( _st_ +1 _| ϕt_ +1). Thus, the complete latent-state transition can be written as 


where _θ_ collects the world-model parameters and _δ_ ( _·_ ) denotes the Dirac distribution corresponding to the deterministic map. Equation (1) clarifies that stochasticity in the model arises only from the prior distribution of _st_ +1, whereas _ϕt_ +1 is produced by the structured Koopman transition. The prediction heads further model observations, rewards, and episode-continuation flags. 

During training, the model can use the current observation to construct a posterior state. Let _et_ = _Eθ_ ( _ot_ ) be the observation encoding. The posterior inference distribution of the stochastic state is _qθ_ ( _st | ϕt, et_ ), following the prior–posterior inference structure of Dreamer-style world models [5], [9]. 

The posterior network only corrects the stochastic state _st_ and does not directly resample _ϕt_ . The deterministic state _ϕt_ is still propagated from the previous posterior state and previous action through the Koopman transition introduced below. The trajectory formed by posterior stochastic states is denoted as 

4 


Fig. 1. Learning workflows of Koopman Dreamer. (a) Posterior-conditioned world-model learning from observed sequences, where observations provide stochastic-state corrections and prediction targets. (b) Actor–critic learning on prior imagined trajectories initialized from an observation-conditioned state, without access to future observations. Both workflows share the controlled Koopman latent transition detailed in Fig. 2. 

_yt_<sup>post</sup> , and the prior rollout obtained along an action sequence without future observations is denoted as _y_ ˜ _t_ . 

The central objective of this paper is to construct a world model that uses a spectrally controlled deterministic Koopman backbone for long-horizon latent-state propagation. Observation encoding, posterior correction, reward prediction, episodecontinuation prediction, and policy imagination are therefore organized around the same controllable latent evolution rather than around the unconstrained deterministic update of the baseline RSSM. 

## IV. METHOD 

This section presents the architecture and optimization of Koopman Dreamer. We first describe the overall model, observation interface, and latent-state inference. We then introduce the controlled Koopman transition and its spectral parameterization, followed by the posterior-conditioned teacher representation, world-model objectives, and latent actor–critic optimization. 

## _A. Model Overview_ 

Koopman Dreamer augments a DreamerV3 world model [9] with a spectrally constrained Koopman transition in place of the deterministic RSSM update, together with posteriorconditioned and posterior-free rollout objectives. The model comprises an observation encoder, the Koopman dynamics, stochastic-state prior and posterior networks, observation/reward/continuation heads, and latent-space actor and value networks. The complete latent state is _yt_ = ( _ϕt, st_ ), where _ϕt_ is the deterministic Koopman evolution state and _st_ supplies observation-conditioned stochastic correction. Fig. 1 summarizes the two complementary learning workflows built around the shared latent dynamics. Training and imagination share the same latent dynamics but differ in available information. During the sequence training illustrated in Fig. 1(a), the transition first propagates _ϕt_ = _FK_ ( _ϕt−_ 1 _, st−_ 1 _, at−_ 1). The encoded observation _et_ = _Eθ_ ( _ot_ ) then produces _st ∼ qθ_ ( _st | ϕt, et_ ), yielding the posterior state _yt_<sup>post</sup> = ( _ϕt, st_ ) used by 

the prediction heads and teacher branch. During the openloop prediction and policy imagination illustrated in Fig. 1(b), future observations are unavailable, so stochastic states are obtained from the prior _pθ_ ( _st | ϕt_ ). The auxiliary objectives introduced below train the same structured transition under both information patterns. 

## _B. Observation Encoding and Prediction Heads_ 

The observation encoder applies a symlog transform to continuous vector inputs and maps them through an MLP as _et_ = _Eθ_ ( _ot_ ) [9]. Its input is a proprioceptive state vector for DMC and a task-state–LiDAR vector for UAV navigation. From _yt_ = ( _ϕt, st_ ), the prediction heads model _pθ_ ( _ot | yt_ ) = Dist _o_ ( _Dθ_ ( _yt_ )), _pθ_ ( _rt | yt_ ) = Dist _r_ ( _Rθ_ ( _yt_ )), and _pθ_ ( _ct | yt_ ) = Bernoulli( _Cθ_ ( _yt_ )). Continuous observations use symlog reconstruction, rewards use a symexp two-hot distribution, and continuation flags use binary logistic prediction. These heads are supervised on posterior states. On prior imagined states, the reward and continuation heads provide _r_ ˆ _t_ and _c_ ˆ _t_ for return estimation. 

## _C. Koopman Latent Transition_ 

As shown in Fig. 2, the Koopman backbone directly propagates the deterministic latent state _ϕt_ through a spectrally structured autonomous update augmented by action-dependent and stochastic corrections. The stochastic state _st_ is flattened and linearly projected into a modulation vector _zt_ = _gz_ ( _st_ ), which carries local posterior-correction information into the next deterministic state. The action is first vectorized, and each component is rescaled as 


where _j ∈{_ 1 _, . . . , da}_ denotes an action-component index, _da_ = dim(vec( _at_ )) is the dimension of the vectorized action, and sg denotes stop-gradient. This component-wise rescaling leaves the bounded actions used in our experiments unchanged 

5 

and only guards against action values outside their nominal range. The Koopman transition is written as 


where _AK_ is the autonomous Koopman operator, and _Ba_ and _Bz_ are learnable linear maps for the action and stochastic modulation, respectively. The element-wise map clip _cϕ_ ( _x_ ) = _cϕ_ tanh( _x/cϕ_ ), with _cϕ >_ 0, bounds the deterministic-state magnitude. The spectral parameterization controls the presaturation amplification and modal persistence of the autonomous update. Clipping prevents numerical divergence but does not by itself preserve information or guarantee accurate long-horizon prediction. When a modulation vector is supplied directly, _FK_<sup>(</sup><sup>_z_)(</sup><sup>_ϕ, z, a_)denotesthesameupdatewith</sup><sup>_z_replac-</sup> ing _gz_ ( _s_ ); thus, _FK_ ( _ϕ, s, a_ ) = _FK_<sup>(</sup><sup>_z_)(</sup><sup>_ϕ, gz_(</sup><sup>_s_)</sup><sup>_, a_).Thebilinear</sup> state–action interaction term adopts a low-rank form: 


where _⊙_ denotes element-wise multiplication, _Wϕ_<sup>_b_and</sup><sup>_W b_</sup> _a_ project the state and action into the same low-rank interaction space, _Wo_<sup>_b_maps the interaction features back to the Koopman-</sup> state dimension, and _βb_ controls the magnitude of the bilinear term. Equation (3) allows the effect of an action to vary with the current latent state, instead of being restricted to globally fixed action directions through _Ba_ . In ablation configurations, setting _βb_ = 0 reduces the transition to one with only the linear action term. 

The transition in (2) can be interpreted through four additive components: _u_<sup>_K_</sup> _t_ = _AKϕt_ for autonomous spectral latent evolution, _u_<sup>_a_</sup> _t_ = _Baa_ ¯ _t_ for the linear action term, _u_<sup>_b_</sup> _t_<sup>=</sup><sup>_Hθ_(</sup><sup>_ϕt,_¯</sup><sup>_at_)forstate-dependentactionmodulation,and</sup> _u_<sup>_z_</sup> _t_<sup>=</sup><sup>_Bzzt_forlocalcorrectioninformationcarriedbythe</sup> stochastic state. Thus, _ϕt_ +1 = clip _cϕ_ ( _ut_<sup>_K_+</sup><sup>_ua_</sup> _t_<sup>+</sup><sup>_ub_</sup> _t_<sup>+</sup><sup>_uz_</sup> _t_<sup>).</sup> This decomposition makes the modeling hierarchy explicit: the long-horizon propagation path is the spectrally controlled autonomous backbone, while the remaining terms express how actions and posterior uncertainty perturb that backbone in controlled tasks. 

## _D. Spectrally Constrained Koopman Backbone_ 

As illustrated in Fig. 2(a) and (c), the Koopman backbone _AK_ is parameterized by two-dimensional rotation–scaling blocks, which are the main structural constraint imposed on the deterministic latent dynamics. We use an even deterministic dimension _D_ = 2 _M_ throughout this work, so the complete deterministic latent state _ϕt ∈_ R<sup>_D_</sup> is divided into _M_ twodimensional subspaces. For _i_ = 0 _, . . . , M −_ 1, the action of the Koopman backbone on the _i_ -th subspace is 


The modal radius is parameterized as _ρi_ = _ρ_ min + ( _ρ_ max _− ρ_ min) _σ_ ( _αi_ ), while the phase is _θi_ = _π_ tanh( _ωK,i_ ). Here, _σ_ ( _·_ ) is the logistic sigmoid, and _αi_ and _ωK,i_ are unconstrained 

learnable parameters for the modal radius and phase, respectively. 

For finite _αi_ , _ρi ∈_ ( _ρ_ min _, ρ_ max) _⊆_ [ _ρ_ min _, ρ_ max]. Since each rotation matrix is orthogonal and _AK_ is a block-diagonal normal operator composed entirely of these rotation–scaling blocks, it satisfies 


Here, _ρ_ ( _AK_ ) denotes the spectral radius of _AK_ . 

In the implementation, _ρ_ max is usually set close to 1 to allow long-term memory and near-periodic modes, whereas _ρ_ min prevents the autonomous modal radii from becoming excessively contractive. It should be emphasized that the spectral constraint in (4)–(5) acts directly only on the autonomous Koopman backbone _AK_ . It does not constitute a global stability proof for the full controlled system that also includes the action term _Baa_ ¯ _t_ , the bilinear term _Hθ_ , and the stochastic modulation term _Bzzt_ . In this paper, the constraint is used as a structured inductive bias for long rollouts, and its empirical role is evaluated through open-loop prediction error, spectral-radius sensitivity analysis, and structural ablation. 

## _E. Stochastic-State Prior and Posterior_ 

The stochastic state provides local uncertainty and observation correction around the deterministic Koopman trajectory. Given _ϕt_ , the prior network produces logits _ℓ_<sup>_p_</sup> _t_<sup>=</sup><sup>_Pθ_(</sup><sup>_ϕt_)and</sup> _pθ_ ( _st | ϕt_ ) = Dist( _ℓ_<sup>_p_</sup> _t_<sup>).Theposterioradditionallyconditions</sup> on the current observation encoding: _ℓ_<sup>_q_</sup> _t_<sup>=</sup><sup>_Qθ_(</sup><sup>_ϕt, et_)and</sup> _qθ_ ( _st | ϕt, et_ ) = Dist( _ℓ_<sup>_q_</sup> _t_<sup>).Bothdistributionsusegroupedcat-</sup> egorical variables with unimix smoothing to avoid premature collapse [5], [8], [9]. Posterior samples provide observationcorrected states for world-model learning and teacher construction, whereas prior samples or means support posteriorfree rollout and policy imagination. 

## _F. Posterior-Conditioned Teacher Representation_ 

Directly supervising the recursively propagated _ϕt_ can couple the transition targets to current model errors. Because the posterior stochastic state contains current-observation information, we use it to construct a corrected teacher trajectory: 


Here, _Wϕ_ and _Wz_ are teacher projection matrices, and _βϕ_ bounds the posterior offset. The teacher supplies targets for the same Koopman transition rather than defining a separate dynamics model. 

To reduce target drift, the projection parameters are updated in an exponential-moving-average branch, _ξ_ ema _← τ_ ema _ξ_ + (1 _− τ_ ema) _ξ_ ema, where _τ_ ema = 0 _._ 01 is the weight assigned to the online parameters. The stop-gradient targets are _ϕ_<sup>¯tar</sup> _t_ = sg( _ϕ_<sup>¯ema</sup> _t_ ) and _z_ ¯ _t_<sup>tar</sup> = sg(¯ _zt_<sup>ema</sup> ). Only the two teacher projection heads have EMA copies; the observation encoder, Koopman transition, prior, and posterior retain their online parameters [38], [39]. 

6 


Fig. 2. Controlled Koopman latent transition and its spectral structure. (a) Bounded modal radii and phases define the two-dimensional rotation–scaling blocks of the autonomous Koopman backbone. (b) The deterministic update combines autonomous spectral evolution, linear and state-dependent action effects, and stochastic-state modulation before smooth element-wise clipping. (c) The eigenvalue geometry and representative latent trajectories illustrate contraction, persistence, rotation, and amplification under different modal radii and phases. 

## _G. World-Model Training Objective_ 

Let _qb,t_ = _qθ_ ( _sb,t | ϕb,t, eb,t_ ) and _pb,t_ = _pθ_ ( _sb,t | ϕb,t_ ) for a batch of _Nb_ sequences of length _T_ . For observation output keys _m ∈O_ , let _Lo_ =<sup>�</sup> _m∈O_<sup>_Lm_denotethe</sup> total reconstruction loss. The base world-model objective is _L_ base = _λoLo_ + _λrLr_ + _λcLc_ + _λ_ dyn _L_ dyn + _λ_ rep _L_ rep. The observation, reward, and continuation terms use the prediction losses described above. The dynamics term averages max(KL(sg( _qb,t_ ) _∥pb,t_ ) _, λ_ free), and the representation term averages max(KL( _qb,t∥_ sg( _pb,t_ )) _, λ_ free). These complementary stop-gradient paths train the prior to follow the posterior while keeping the posterior representation predictable [5], [9], [21]. The remaining losses specifically supervise the structured transition. 

**One-step Koopman supervision.** Local transition consistency is enforced on consecutive EMA teacher states: 


Here, _ab,t_ is the action from _t_ to _t_ +1. Stop-gradient is applied to the teacher input and target, so this path primarily updates the Koopman backbone and its control terms. 

**Multi-step teacher rollout supervision.** One-step consistency does not directly expose accumulated recursive error. Each replay sequence supplies one rollout start: for a sequence 

of length _T_ , we set _t_ = 0 and use _H_ = _T −_ 1. Starting from _ϕ_ ˆ _t_ = sg(¯ _ϕ_<sup>tar</sup> _t_<sup>),werollout</sup> 


and minimize 

where _wk_<sup>roll</sup> = 1 + tanh( _τ_ roll _k_ ) emphasizes longer horizons for _τ_ roll _≥_ 0. 

**Posterior-free rollout supervision.** Teacher modulation remains observation-conditioned and therefore does not reproduce the information pattern used during imagination. We consequently start from a posterior state and roll out _y_ ˜ _t_ + _k ∼ pθ_ (˜ _yt_ + _k | y_ ˜ _t_ + _k−_ 1 _, at_ + _k−_ 1) without future observations, using the same start _t_ and horizon _H_ as in the teacher rollout: 


Here, _ϕ_<sup>¯</sup> (˜ _y_ ) maps a prior rollout state through the online teacher projection head. The combined rollout loss is _L_ roll = ( _L_<sup>tea</sup> roll<sup>+</sup> _L_<sup>free</sup> roll<sup>)</sup><sup>_/_2.</sup> 

**Open-loop observation prediction.** Latent alignment alone can yield internally consistent but weakly decodable states. 

7 

From posterior starting times _t ∈S_ , we therefore decode observations along prior rollouts: 


The state _y_ ˜ _b,t_ + _k_ is generated without observations after the starting time. Here, _S ⊆{_ 0 _, . . . , T − H −_ 1 _}_ is the set of valid posterior starting indices selected from each replay sequence. In the implementation, up to four indices are spaced uniformly over the valid range, with _H_ shortened when necessary so that every target _t_ + _k_ remains within the sequence. This loss requires prior states to retain information that can be decoded into future observations. 

**Operator regularization.** The block parameterization already enforces the spectral interval. We therefore use _L_ opreg = _λa∥Ba∥_<sup>2</sup> _F_<sup>+</sup><sup>_λz∥Bz∥_2</sup> _F_<sup>+</sup><sup>_λϕ_E</sup><sup>_b,t_[</sup><sup>_∥ϕ_¯</sup><sup>_b,t−ϕb,t∥_</sup> 2<sup>2]tolimitthe</sup> linear action correction, stochastic modulation, and posteriorconditioned teacher offset without imposing an additional radius penalty, where E _b,t_ denotes the uniform average over batch and time. 

The complete world-model objective is 


where _n_ is the optimization step and each _α_ ( _n_ ) _∈_ [0 _,_ 1] linearly warms up its corresponding term. The warmups allow the model to establish its latent representation and prediction heads before the propagation-specific supervision reaches full strength. 

## _H. Latent Imagination and Policy Optimization_ 

The policy and value function take the full latent state _yt_ as input. Starting states are sampled from posterior replay sequences, after which the policy samples _at ∼ πψ_ ( _at | yt_ ) and the prior transition generates the next latent state without future observations. The reward and continuation heads provide _r_ ˆ _t_ and _c_ ˆ _t_ along these trajectories [6], [9]. The recursive return is 


with terminal bootstrap from the final imagined value. Imagined losses are weighted by _w_ 0<sup>imag</sup> = 1 and _wt_<sup>imag</sup> = � _ti_ =0 _−_ 1<sup>_γc_ˆ</sup><sup>_i_,sostatesfollowingalowcontinuationprobability</sup> contribute less to learning. 

The value head predicts a categorical distribution _p_<sup>_V_</sup> _ω_<sup>(</sup><sup>_·|_</sup> _yt_ ) over symexp-spaced bins. It is trained by continuationweighted two-hot cross-entropy against the return target _G_<sup>_λ_</sup> _t_<sup>,</sup> together with slow-value regularization toward the prediction of a slowly updated value network, weighted by _β_ slow. 

For policy optimization, let _sR_ be the running 5th-to-95th percentile range of imagined returns, lower-bounded by 1, and define the normalized advantage _A_<sup>�</sup> _t_ = ( _G_<sup>_λ_</sup> _t_<sup>_−Vω_(</sup><sup>_yt_))</sup><sup>_/sR_.</sup> The actor uses continuation-weighted policy gradients with entropy regularization coefficient _η_ . Return targets, continuation 

weights, and advantages are stop-gradient quantities, and actor gradients are not propagated into the world model. Because value and policy learning are both evaluated on prior imagined trajectories, their targets directly depend on the long-horizon accuracy of the structured Koopman transition. 

## V. THEORETICAL ANALYSIS 

We analyze how the spectral backbone affects error propagation in recursive latent rollouts. All vector norms are Euclidean and matrix norms are induced 2-norms. Let _ρ⋆_ = _ρ_ ( _AK_ ). Because _AK_ is block diagonal with normal rotation–scaling blocks, 


Thus, _ρ⋆_ directly controls autonomous modal amplification before clipping: smaller values attenuate perturbations, whereas values near one preserve slowly varying and oscillatory information. 

## _A. Controlled Rollout-Error Bound_ 

Define the pre-clipping update 


The model follows _ϕt_ +1 = clip _cϕ_ ( _UK_ ( _ϕt, zt,_ ¯ _at_ )). We compare it with a reference trajectory 


where ( _ϕ_<sup>_′_</sup> _t_<sup>_, z_</sup> _t_<sup>_′_)isacomparisontrajectoryinthesamelatent</sup> space and _ζt_ is its one-step transition residual. On the bounded latent region visited during training and imagination, assume that the bilinear term is locally Lipschitz: 


_Proposition 1 (Controlled rollout-error propagation):_ For a shared action sequence, let _d_<sup>_ϕ_</sup> _t_<sup>=</sup><sup>_ϕt−ϕ′_</sup> _t_<sup>anddefine</sup> 


Then 


and, after _H_ recursive steps, 


_Proof:_ The element-wise map clip _cϕ_ ( _x_ ) = _cϕ_ tanh( _x/cϕ_ ) is 1-Lipschitz. Hence, the difference between clipped updates is bounded by the difference between their inputs. Under shared actions, the linear action terms cancel. Applying _∥AK∥_ 2 = _ρ⋆_ , the Lipschitz bound in (16), and _∥ζt∥≤ ϵt_ gives (18); repeated substitution yields (19). 

The bound separates multiplicative propagation, governed by the spectral backbone and state-dependent bilinear interaction through _κ⋆_ , from the additive stochastic-modulation 

8 

mismatch and modeling residual in _δt_ . If the action sequences differ, _δt_ gains the term ( _∥Ba∥_ 2 + _L_<sup>_b_</sup> _a_<sup>)</sup><sup>_∥a_¯</sup><sup>_t−a_¯</sup> _t_<sup>_′∥_.Theshared-</sup> action form in (19) therefore applies directly to our open-loop diagnostics, while the additional term accounts for policyinduced action differences during imagination. This is a local rollout-error result under the stated assumptions, not a global stability guarantee for the controlled system. 


For _κ⋆ <_ 1, initial errors decay and accumulated residuals remain bounded by _δ/_<sup>¯</sup> (1 _− κ⋆_ ); at _κ⋆_ = 1, residuals grow linearly; and for _κ⋆ >_ 1, both terms can grow geometrically. Hence, reducing _ρ⋆_ improves attenuation but may erase persistent task information, while increasing it preserves long-term modes at the cost of greater error amplification. This trade-off motivates the spectral-radius study in Section VI-C. 

The training objectives target complementary terms in the bound. The spectral parameterization restricts the autonomous contribution to _κ⋆_ . The one-step Koopman loss reduces empirical transition residuals; the teacher and posterior-free rollout losses penalize their recursive accumulation; and the openloop prediction loss requires prior states to remain decodable. Finally, the dynamics and representation KL terms encourage posterior–prior alignment and thereby target the stochastic contribution _∥Bz∥_ 2 _∥zt − zt_<sup>_′∥_.Thespectralstructuretherefore</sup> regulates error propagation, while the auxiliary objectives reduce the errors injected at each step. 

## VI. EXPERIMENTS AND ANALYSIS 

This section evaluates Koopman Dreamer from five perspectives. First, we compare continuous-control performance and sample efficiency on DMC proprioceptive tasks. Second, we evaluate DMC open-loop prediction to relate control performance to long-horizon model accuracy. Third, we examine closed-loop navigation and open-loop prediction in the UAV-LiDAR Forest scenario. Fourth, we study how the learned spectral radius affects long-horizon prediction. Finally, structural ablations isolate the contributions of the spectral constraint, posterior-conditioned teacher, and bilinear control term. Experimental configurations and complete supplementary results are provided in the appendix. 

## _A. DMC Proprioceptive Continuous Control_ 

**Setup.** We evaluate nine proprioceptive tasks from the DeepMind Control Suite [10], [11], covering swing-up, reaching, balance, and locomotion. The comparison includes PPO, D4PG, DDPG, MPO, DMPO, and DreamerV3 [9], [40]–[44]. The baseline curves and scores are taken from the public DMC proprioceptive benchmark reported with DreamerV3, whereas Koopman Dreamer is trained in this work. All methods use low-dimensional state observations, a 500K-step interaction 

budget, and action repeat 2. Following the public protocol, we average the last recorded score over the available seeds. For Koopman Dreamer, we use [ _ρ_ min _, ρ_ max] = [0 _._ 85 _,_ 0 _._ 95]. Complete benchmark-source and hyperparameter details are given in Tables VII and VI. 

**Control performance.** Table I shows that Koopman Dreamer achieves the best final score on six tasks and exceeds DreamerV3 on eight. The largest gains occur on Acrobot and Hopper Stand. Fig. 3 further shows continued improvement on Acrobot, an earlier high-return plateau on Hopper Stand, and faster entry into the high-return region on Reacher Hard and Walker Walk. These tasks contain smooth, persistent, or near-periodic dynamics, for which explicitly controlling latent modal persistence is well matched to multi-step imagination. 

Fig. 4 summarizes sample efficiency using a task-specific target equal to 90% of the best final score. Koopman Dreamer reaches this target fastest on eight tasks and earlier than DreamerV3 on the same eight. Together, the final scores and learning speeds indicate that the spectral transition improves not only the attainable policy quality but also how rapidly imagined rollouts become useful for policy optimization. 

**Open-loop prediction.** Each world model is initialized from a 32-step observation context and rolled out for 64 steps along recorded actions without future observations. Errors are averaged over 32 replay batches with 16 sequences per batch. Table II reports the resulting cross-task errors; complete tasklevel curves are provided in Figs. 12 and 13. 

Koopman Dreamer reduces mean deterministic-latent MSE by 89.4% and has lower horizon-64 latent error on all nine tasks. More importantly, the improvement transfers to shared observation coordinates: mean proprioceptive MSE falls by 23.2%, with lower error on eight tasks. Reward prediction also improves on eight tasks, and its cross-task MSE averaged over the rollout decreases from 0.9290 to 0.7318. Because separately learned latent coordinates are not directly comparable physical quantities, decoded observation error provides the stronger evidence. The agreement between latent consistency, observable prediction, and closed-loop performance supports the intended role of the spectral backbone: it limits recursive drift while retaining task-relevant dynamics for imagination. 

## _B. UAV-LiDAR Autonomous Navigation_ 

**Environment and protocol.** The UAV simulator is implemented as a Gymnasium environment [45]. The UAV uses three-dimensional velocity commands _at ∈_ [ _−_ 1 _,_ 1]<sup>3</sup> , and its observation combines velocity, normalized height, targetrelative position, previous action, and LiDAR ranges. Table III summarizes the three environments. The main Forest benchmark uses a 50 m map, 120 cylindrical obstacles, and a 280dimensional seven-ring LiDAR, coupling long-horizon target progress with dense obstacle sensing. The simulator uses a 0.1 s control interval, maximum horizontal and vertical speeds of 2.0 and 1.0 m/s, respectively, and a 500-step episode limit. 

We compare D4PG, DreamerV3, and Koopman Dreamer on four targets. For each method, one fixed checkpoint is evaluated without retraining in three Forest scenes with different obstacle placements shared across methods. Each 

9 

TABLE I 

FINAL SCORES ON NINE DMC PROPRIOCEPTIVE TASKS 

|Task|PPO|D4PG|DDPG|MPO|DMPO|DreamerV3|Koopman<br>Dreamer|
|---|---|---|---|---|---|---|---|
|Acrobot|2.0|120.2|87.4|79.7|118.2|131.7|**292.3**|
|Cartpole|265.8|**876.2**|863.0|857.2|859.6|856.0|873.3|
|Cheetah|100.5|630.1|602.6|646.9|603.4|596.3|**692.8**|
|Hopper Stand|0.0|732.3|618.9|450.3|545.3|650.4|**859.1**|
|Reacher|662.2|973.3|964.0|967.8|977.7|961.8|**979.0**|
|Reacher Hard|168.4|967.0|973.6|954.5|965.3|948.6|**987.0**|
|Walker Stand|151.7|917.2|974.4|959.2|980.2|957.2|**982.4**|
|Walker Walk|77.0|**961.1**|954.0|929.6|938.9|881.0|942.3|
|Walker Run|31.4|611.9|564.3|570.5|511.5|**655.5**|572.0|


Each entry is the mean across seeds of the last recorded score; bold indicates the best result in each row. 


Fig. 3. Learning curves on nine DMC proprioceptive tasks. 

target uses 20 matched initial conditions per scene, yielding 240 closed-loop episodes per method. All methods use a 500K-step training budget. DreamerV3 and Koopman Dreamer 

use size25m configurations with batch size 16, sequence length 64, imagination horizon 15, and _λ_ -return parameter 0.95. Koopman Dreamer uses a 3072-dimensional determin- 

10 


Fig. 4. Environment steps required to reach 90% of the task-best final return. NR denotes that the target was not reached within 500K steps. 

TABLE II 

CROSS-TASK OPEN-LOOP PREDICTION MSE AND COMPARATIVE SUMMARY ON DMC PROPRIOCEPTIVE TASKS 

|Evaluation|setting|Predictio|n MSE|Cross-method|comparison|
|---|---|---|---|---|---|
|Evaluation quantity|Rollout summary|DreamerV3|Koopman<br>Dreamer|Relative MSE<br>(Koopman Dreamer/<br>DreamerV3)|Tasks favoring<br>Koopman Dreamer|
|Proprioceptive observation|Mean over _H_ = 1:64|0.6256|**0.4802**|0.768|8/9|
||At _H_ = 64|0.7960|**0.6953**|0.873|7/9|
|Reward|Mean over _H_ = 1:64|0.9290|**0.7318**|0.788|8/9|
||At _H_ = 64|**1.1920**|1.2588|1.056|8/9|
|Deterministic latent state|Mean over _H_ = 1:64|0.0379|**0.00403**|0.106|9/9|
||At _H_ = 64|0.0667|**0.00698**|0.105|9/9|


Each model is initialized from a 32-step observation context and then rolled out along recorded action sequences without future observations up to horizon 64. The two method columns report MSE averaged across the nine DMC tasks; bold indicates the lower cross-task MSE in each row. “Mean over _H_ = 1:64” averages prediction error over all 64 open-loop rollout steps. Relative MSE is Koopman Dreamer divided by DreamerV3, so a value below one favors Koopman Dreamer. The final column counts the tasks, out of nine, on which Koopman Dreamer obtains lower MSE. 

TABLE III UAV-LIDAR SCENARIO SETTINGS 

|Scenario|Setting|Experimental role|
|---|---|---|
|Empty<br>Sparse|No<br>obstacle,<br>20<br>m,<br>96-<br>dimensional 3-ring LiDAR<br>20 m, 20 sparse cylindrical ob-<br>stacles, 96-dimensional 3-ring Li-<br>DAR|Environment and action-<br>dynamics check<br>Sample-efficiency<br>and<br>prediction evaluation|
|Forest|50 m, 120 dense cylindrical ob-<br>stacles, 280-dimensional 7-ring<br>LiDAR|Main autonomous navi-<br>gation evaluation|


istic state, 32 groups of 24-way stochastic variables, a 96dimensional stochastic projection, [ _ρ_ min _, ρ_ max] = [0 _._ 75 _,_ 0 _._ 95], and a rank-256 bilinear term; its learned spectral radius is 0.881. Open-loop prediction is evaluated only for DreamerV3 and Koopman Dreamer because D4PG has no world model. Complete environment, evaluation, and method configurations are reported in Tables VIII and IX. 

**Closed-loop navigation.** The trajectory views in Fig. 5 

show that high-return Koopman Dreamer rollouts more consistently approach the target region with less extended wandering. These selected trajectories are qualitative illustrations rather than the basis of the comparison, but they visualize the role of state-dependent control: the bilinear term allows the same velocity command to have different latent effects across positions, velocities, and obstacle configurations. 

The aggregate results in Fig. 6 use all 240 episodes. Koopman Dreamer attains the highest success rate (73.8%) and lowest failure rate (26.2%), compared with 53.8%/46.2% for DreamerV3 and 15.8%/84.2% for D4PG. Its median final distance is also lowest (0.72 versus 0.75 and 4.22). The two world models have comparable mean returns, while Koopman Dreamer achieves the higher median return (195.50 versus 182.19). Complete statistics are reported in Table X. Overall, the structured world model yields the clearest advantage in task completion, which depends on maintaining useful target and obstacle information over long imagined horizons. 

**Open-loop prediction.** DreamerV3 and Koopman Dreamer are initialized from posterior context and rolled out along 

11 


Fig. 5. Top-down trajectories for four Forest targets: (a) (0 _,_ 0 _,_ 2), (b) (18 _,_ 0 _,_ 2), (c) (18 _,_ 18 _,_ 2), and (d) ( _−_ 18 _, −_ 18 _,_ 2). Each panel shows the 15 highest-return trajectories in one representative shared scene. 


Fig. 6. Closed-loop UAV-LiDAR results over four targets and three shared Forest scenes. 

recorded actions without future observations. At horizon 64, Koopman Dreamer lowers vector, LiDAR, velocity, and deterministic-latent MSE from 0.0181, 0.0183, 0.00297, and 0.0465 to 0.0160, 0.0161, 0.00174, and 0.0233, respectively. It also reduces mean reward MSE over the rollout from 478.31 to 281.74 and improves target-relative prediction over most evaluated horizons. 

Fig. 7 shows the strongest and most persistent reductions in velocity, reward, and deterministic-state drift—quantities that directly affect imagined returns and future control. The spectral blocks limit autonomous amplification, while the linear and bilinear action terms preserve global and statedependent control effects. The agreement between these openloop improvements and the higher completion rate provides complementary evidence that the structured transition produces more useful imagined trajectories. 

## _C. Spectral Radius Sensitivity_ 

We train six otherwise matched variants with _ρ_ min = 0 _._ 75 and different spectral upper bounds. Table IV reports the resulting learned radii. After a 32-step context, each model performs a 64-step open-loop rollout along recorded actions; 

|SPECTRALUPP|ER-BOU|T<br>NDCON|ABLE IV<br>FIGURAT<br>RADII|IONS AN|DLEARN|EDSPECTRAL|
|---|---|---|---|---|---|---|
|_ρ_max|0.90|0.95|1.00|1.05|1.10|1.20|
|_ρ_(_AK_)|0.849|0.881|0.912|0.943|0.971|1.026|


complete horizon curves are provided in Fig. 11 in the appendix. 

Fig. 8 confirms the stability–expressiveness trade-off predicted by (19). The smallest radius, 0 _._ 849, gives the lowest latent MSE (0 _._ 0140) but not the lowest observable errors, indicating that strong contraction can make latent trajectories numerically similar while discarding predictive information. Observable prediction is strongest at intermediate radii: 0 _._ 881 minimizes vector, LiDAR, and velocity MSE, whereas 0 _._ 943 minimizes goal-relative and reward MSE. 

As the learned radius approaches and crosses the unit circle, accumulated error becomes dominant. Increasing _ρ⋆_ from 0 _._ 943 to 1 _._ 026 raises horizon-64 latent MSE from 0 _._ 0518 to 2 _._ 2675, with corresponding degradation in vector and LiDAR prediction. Thus, the spectral constraint is not simply a contraction mechanism: it provides a learnable range 

12 


Fig. 7. Open-loop prediction MSE versus horizon in the UAV-LiDAR Forest scenario. 

TABLE V 

STRUCTURAL CONFIGURATIONS OF UAV-LIDAR ABLATION MODELS 

|Variant|Modified component|Diagnostic focus|
|---|---|---|
|Koopman<br>Dreamer|Spectral blocks,<br>posterior-conditioned EMA<br>teacher, and bilinear control<br>retained|Full structured<br>model|
|w/o spectral|Bounded-radius parameterization<br>disabled; modal radii optimized<br>without a radius penalty;<br>operator regularization retained|Long-horizon<br>spectral control|
|w/o teacher|Teacher projection and EMA<br>branches disabled; stop-gradient<br>posterior _ϕ_ and online<br>_z_-projection used as targets|Target stability and<br>alignment|
|w/o bilinear|Bilinear term removed; only<br>_Ba_¯_at_ retained|State-dependent<br>action effects|


that preserves persistent modes without allowing uncontrolled long-horizon amplification. Because latent coordinates differ across variants, observable metrics remain the primary basis for selecting this range. 

## _D. Structural Ablation_ 

We evaluate the full model and three variants for 80 episodes on one shared Forest scene. Table V lists the exact modifications and their diagnostic roles. All other architecture, loss, training-budget, and evaluation settings are fixed. 

**Closed-loop effects.** Fig. 9 assigns distinct roles to the three components. Removing the spectral constraint leaves success comparable but reduces mean return by 20.4% (163.82 to 130.33) and raises median action variation from 0.97 to 4.00. The spectral structure therefore contributes primarily through rollout quality and smoother, less compensatory control. Removing the teacher lowers mean return to 143.20 

and success to 68.8%, while increasing the collision rate from 15.0% to 28.7%. This suggests that slowly updated posterior-conditioned targets improve closed-loop robustness by preventing rapidly changing online targets from weakening task-relevant transition learning. Removing bilinear control is most damaging: success falls to 8.8% and the collision rate rises to 56.2%, demonstrating that a fixed linear action direction is insufficient for state-dependent navigation dynamics. Complete termination statistics are reported in Table XI. 

**Open-loop effects.** Fig. 10 explains the closed-loop differences at the dynamics level. At horizon 64, removing the spectral constraint increases vector, LiDAR, velocity, and latent MSE from 0 _._ 0160, 0 _._ 0161, 0 _._ 00174, and 0 _._ 0233 to 0 _._ 0228, 0 _._ 0229, 0 _._ 00690, and 0 _._ 3891, respectively. This broad error growth directly supports the spectral backbone’s role in suppressing long-horizon drift. Removing bilinear control increases goal-relative and reward MSE from 0 _._ 0374 and 357 _._ 81 to 0 _._ 0674 and 1036 _._ 99, connecting its severe control degradation to inaccurate state-dependent action propagation. The teacher ablation retains similar average observation error but has higher reward error and a markedly higher collision rate, indicating that stable teacher targets contribute information relevant to robust closed-loop decisions beyond average observation reconstruction. 

Taken together, the closed- and open-loop results support a complementary structural hierarchy. The spectral constraint limits long-horizon drift and the compensatory action variation it induces; posterior-conditioned EMA targets improve representation–transition alignment and closed-loop robustness; and bilinear control captures the state-dependent action effects required for nonlinear navigation. These components jointly turn the spectrally organized latent backbone into an effective controlled world model for long-horizon imagination. The ablations are conducted in a representative Forest setting, 

13 


Fig. 8. Horizon-64 prediction MSE as a function of the learned spectral radius. Error bars show variation across evaluation batches. 

Fig. 9. Closed-loop ablation results: return distribution, outcome composition, and action variation on successful episodes. 

and broader scene-level evaluation can further examine the generality of these roles. 

## VII. DISCUSSION 

The experimental results support the central claim that organizing deterministic latent propagation around a spectrally constrained Koopman backbone can improve long-horizon imagination in Dreamer-style world models. On the nine DMC proprioceptive tasks, Koopman Dreamer outperforms the DreamerV3 world-model baseline on eight tasks and achieves the best final score among the evaluated methods on six. The open-loop results provide complementary evidence: in addition to substantially reducing deterministic-latent rollout error, Koopman Dreamer lowers decoded proprioceptive prediction error on most tasks. This consistency between open-loop prediction and closed-loop control suggests that 

the improvements on swing-up, sustained motion, precise reaching, and balance are related to more reliable multi-step latent propagation rather than to task-specific capacity alone. 

The spectral-radius sensitivity results further clarify the role of the proposed structure. Strong contraction can suppress persistent task-relevant information, whereas overly persistent modes increase the influence of accumulated transition errors. The favorable intermediate spectral range therefore reflects a stability–expressiveness trade-off rather than a preference for the smallest possible radius. Within this structure, the spectral backbone organizes the persistence, attenuation, and oscillation of autonomous latent modes, while posterior-conditioned teacher targets and rollout objectives reduce stepwise prediction residuals. The linear and bilinear action terms further adapt the backbone to controlled dynamics by representing both globally consistent and state-dependent action effects. 

14 


Fig. 10. Open-loop prediction errors of the ablation models versus horizon. All variants use a 32-step context and 64-step prediction horizon. 

The ablation results support these complementary roles and indicate that the auxiliary mechanisms strengthen, rather than replace, the spectral dynamics core. 

The results span compact proprioceptive observations and higher-dimensional LiDAR-based vectors. In UAV-LiDAR navigation, Koopman Dreamer improves target completion and substantially reduces the overall failure rate relative to DreamerV3. Overall, the experiments support spectrally structured latent dynamics as an effective inductive bias for longhorizon prediction and control in the evaluated settings. Future work may extend the approach with adaptive spectral ranges, broader evaluation across training runs and environments, and safety-aware or risk-sensitive policy objectives. 

## VIII. CONCLUSION 

This paper proposed Koopman Dreamer for end-to-end continuous control. Bounded rotation–scaling blocks explicitly characterize the damping, persistence, and oscillation of autonomous latent modes, while linear and bilinear action terms and stochastic modulation adapt this spectral backbone to controlled nonlinear dynamics. Posterior-conditioned EMA targets and prior-rollout objectives train the same structured transition under both observation-corrected representation learning and posterior-free imagination. The resulting error-propagation analysis shows that reliable long-horizon prediction requires a balance between error attenuation and persistent information retention rather than maximal contraction. Experiments on DMC proprioceptive control and UAV-LiDAR navigation, together with open-loop prediction, spectral-radius sensitivity analysis, and structural ablations, demonstrate that the structure of Koopman Dreamer improves long-horizon latent propagation and supports stronger closedloop task performance. Overall, Koopman Dreamer provides 

a structured and controllable dynamics foundation for longhorizon imagination in Dreamer-style world models. Future work may investigate adaptive spectral ranges and combine Koopman Dreamer with safety-aware or risk-sensitive policy objectives for more reliable autonomous control. 

## REFERENCES 

- [1] R. S. Sutton and A. G. Barto, _Reinforcement Learning: An Introduction_ , 2nd ed. Cambridge, MA, USA: MIT Press, 2018. 

- [2] K. Chua, R. Calandra, R. McAllister, and S. Levine, “Deep reinforcement learning in a handful of trials using probabilistic dynamics models,” in _Proc. Advances in Neural Information Processing Systems_ , 2018. 

- [3] M. Janner, J. Fu, M. Zhang, and S. Levine, “When to trust your model: Model-based policy optimization,” in _Proc. Advances in Neural Information Processing Systems_ , 2019. 

- [4] D. Ha and J. Schmidhuber, “World models,” arXiv:1803.10122, 2018. 

- [5] D. Hafner, T. Lillicrap, I. Fischer, R. Villegas, D. Ha, H. Lee, and J. Davidson, “Learning latent dynamics for planning from pixels,” in _Proc. International Conference on Machine Learning_ , 2019. 

- [6] D. Hafner, T. Lillicrap, J. Ba, and M. Norouzi, “Dream to control: Learning behaviors by latent imagination,” in _Proc. International Conference on Learning Representations_ , 2020. 

- [7] N. Hansen, X. Wang, and H. Su, “TD-MPC2: Scalable, robust world models for continuous control,” in _Proc. International Conference on Learning Representations_ , 2024. 

- [8] D. Hafner, T. Lillicrap, M. Norouzi, and J. Ba, “Mastering Atari with discrete world models,” in _Proc. International Conference on Learning Representations_ , 2021. 

- [9] D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap, “Mastering diverse control tasks through world models,” _Nature_ , vol. 640, no. 8059, pp. 647–653, 2025. 

- [10] Y. Tassa et al., “DeepMind Control Suite,” arXiv:1801.00690, 2018. 

- [11] E. Todorov, T. Erez, and Y. Tassa, “MuJoCo: A physics engine for model-based control,” in _Proc. IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2012, pp. 5026–5033. 

- [12] B. O. Koopman, “Hamiltonian systems and transformation in Hilbert space,” _Proceedings of the National Academy of Sciences_ , vol. 17, no. 5, pp. 315–318, 1931. 

- [13] B. O. Koopman and J. von Neumann, “Dynamical systems of continuous spectra,” _Proceedings of the National Academy of Sciences_ , vol. 18, no. 3, pp. 255–263, 1932. 

15 

- [14] I. Mezi´c, “Spectral properties of dynamical systems, model reduction and decompositions,” _Nonlinear Dynamics_ , vol. 41, no. 1, pp. 309–325, 2005. 

- [15] S. L. Brunton, M. Budiˇsi´c, E. Kaiser, and J. N. Kutz, “Modern Koopman theory for dynamical systems,” _SIAM Review_ , vol. 64, no. 2, pp. 229– 340, 2022. 

- [16] M. O. Williams, I. G. Kevrekidis, and C. W. Rowley, “A data-driven approximation of the Koopman operator: Extending dynamic mode decomposition,” _Journal of Nonlinear Science_ , vol. 25, no. 6, pp. 1307– 1346, 2015. 

- [17] B. Lusch, J. N. Kutz, and S. L. Brunton, “Deep learning for universal linear embeddings of nonlinear dynamics,” _Nature Communications_ , vol. 9, no. 1, Art. no. 4950, 2018. 

- [18] N. Takeishi, Y. Kawahara, and T. Yairi, “Learning Koopman invariant subspaces for dynamic mode decomposition,” in _Proc. Advances in Neural Information Processing Systems_ , 2017. 

- [19] S. Krishnan, B. Boroujerdian, W. Fu, A. Faust, and V. J. Reddi, “Air Learning: A deep reinforcement learning gym for autonomous aerial robot visual navigation,” _Machine Learning_ , vol. 110, no. 9, pp. 2501– 2540, 2021, doi: 10.1007/s10994-021-06006-6. 

- [20] P. Miera, H. Szolc, and T. Kryjak, “LiDAR-based drone navigation with reinforcement learning,” arXiv:2307.14313, 2023, doi: 10.48550/arXiv.2307.14313. 

   - [38] A. Tarvainen and H. Valpola, “Mean teachers are better role models: Weight-averaged consistency targets improve semi-supervised deep learning results,” in _Proc. Advances in Neural Information Processing Systems_ , 2017. 

   - [39] J.-B. Grill et al., “Bootstrap your own latent: A new approach to self-supervised learning,” in _Proc. Advances in Neural Information Processing Systems_ , 2020. 

   - [40] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” arXiv:1707.06347, 2017. 

   - [41] T. P. Lillicrap et al., “Continuous control with deep reinforcement learning,” in _Proc. International Conference on Learning Representations_ , 2016. 

   - [42] G. Barth-Maron et al., “Distributed distributional deterministic policy gradients,” in _Proc. International Conference on Learning Representations_ , 2018. 

   - [43] A. Abdolmaleki et al., “Maximum a posteriori policy optimisation,” in _Proc. International Conference on Learning Representations_ , 2018. 

   - [44] A. Abdolmaleki et al., “A distributional view on multi-objective policy optimization,” in _Proc. International Conference on Machine Learning_ , 2020. 

   - [45] M. Towers et al., “Gymnasium: A standard interface for reinforcement learning environments,” arXiv:2407.17032, 2024. 

- [21] D. P. Kingma and M. Welling, “Auto-encoding variational Bayes,” in _Proc. International Conference on Learning Representations_ , 2014. 

- [22] C. W. Rowley, I. Mezi´c, S. Bagheri, P. Schlatter, and D. S. Henningson, “Spectral analysis of nonlinear flows,” _Journal of Fluid Mechanics_ , vol. 641, pp. 115–127, 2009. 

- [23] P. J. Schmid, “Dynamic mode decomposition of numerical and experimental data,” _Journal of Fluid Mechanics_ , vol. 656, pp. 5–28, 2010. 

- [24] E. Kaiser, J. N. Kutz, and S. L. Brunton, “Data-driven discovery of Koopman eigenfunctions for control,” _Machine Learning: Science and Technology_ , vol. 2, no. 3, Art. no. 035023, 2021. 

- [25] M. Korda and I. Mezi´c, “Linear predictors for nonlinear dynamical systems: Koopman operator meets model predictive control,” _Automatica_ , vol. 93, pp. 149–160, 2018. 

- [26] A. Narasingam and J. S.-I. Kwon, “Data-driven identification of interpretable reduced-order models using Koopman theory,” _AIChE Journal_ , vol. 66, no. 11, Art. no. e16993, 2020. 

- [27] H. Shi and M. Q.-H. Meng, “Deep Koopman operator with control for nonlinear systems,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 3, pp. 7700–7707, 2022. 

- [28] M. Weissenbacher, S. Sinha, A. Garg, and Y. Kawahara, “Koopman Q- learning: Offline reinforcement learning via symmetries of dynamics,” in _Proc. 39th Int. Conf. Mach. Learn. (ICML)_ , 2022, pp. 23645–23667. 

- [29] X. Lyu, H. Hu, S. Siriya, Y. Pu, and M. Chen, “Task-oriented Koopmanbased control with contrastive encoder,” in _Proc. 7th Conf. Robot Learn. (CoRL)_ , 2023, pp. 93–105. 

- [30] H. Kumawat, B. Chakraborty, and S. Mukhopadhyay, “RoboKoop: Efficient control conditioned representations from visual input in robotics using Koopman operator,” in _Proc. 8th Conf. Robot Learn. (CoRL)_ , 2025, pp. 3474–3499. 

- [31] Z. Zeng, R. Zhou, Y. Meng, and J. Liu, “Data-driven optimal control of unknown nonlinear dynamical systems using the Koopman operator,” in _Proc. 7th Annu. Learn. Dyn. Control Conf. (L4DC)_ , 2025, pp. 1127– 1139. 

- [32] H. Li, X. Zhang, J. Xie, and X. Xu, “Receding-horizon direct policy optimization with Koopman embedding for trajectory tracking of fixedwing UAVs,” _Science China Technological Sciences_ , vol. 69, no. 4, Art. no. 1420303, 2026, doi: 10.1007/s11431-025-3179-9. 

- [33] X. Zhang, Y. Xiao, H. Cao, X. Zhou, X. Yin, and X. Xu, “Learning predictive control with deep Koopman operators for autonomous vehicle motion planning,” arXiv:2606.08136, 2026, doi: 10.48550/arXiv.2606.08136. 

- [34] M. Arjovsky, A. Shah, and Y. Bengio, “Unitary evolution recurrent neural networks,” in _Proc. International Conference on Machine Learning_ , 2016. 

- [35] J. Miller and M. Hardt, “Stable recurrent models,” in _Proc. International Conference on Learning Representations_ , 2019. 

- [36] E. Jang, S. Gu, and B. Poole, “Categorical reparameterization with Gumbel-Softmax,” in _Proc. International Conference on Learning Representations_ , 2017. 

- [37] C. J. Maddison, A. Mnih, and Y. W. Teh, “The Concrete distribution: A continuous relaxation of discrete random variables,” in _Proc. International Conference on Learning Representations_ , 2017. 

16 

TABLE VI 

MAIN HYPERPARAMETERS OF KOOPMAN DREAMER ON DMC PROPRIOCEPTIVE TASKS 

|Category|Hyperparameter|Value|
|---|---|---|
|Environment and training|Task set|9 DMC proprioceptive tasks, env.dmc.image=False|
|Environment and training|Interaction budget|500K environment steps|
|Environment and training|Batch and updates|batch size 16, batch length 64, train ratio 512|
|World-model scale|preset|size12m|
|World-model scale|Koopman hidden|deterministic state 2048, hidden size 256, stochastic 32 groups_×_16 classes|
|World-model scale|Koopman representation|_ϕt_ dimension 2048, _zt_ projection dimension 64|
|Network width|encoder / decoder / heads|depth 16, units 256|
|Policy optimization|actor–critic imagination|imagination length 15, discount horizon 333, return lambda 0.95|
|Koopman backbone|Spectral constraint|maximum radius 0.95, minimum radius 0.85, initial radius 0.90|
|Koopman backbone|Control and stochastic modulation|_z_ scale 0.08, dense scale 0.0, teacher EMA rate 0.01|
|Auxiliary losses|loss scales|koop 0.02, roll 0.02, opreg 0.002, pred 0.05|
|Auxiliary losses|warmup|pred 20K, roll 50K, koop 100K, opreg 150K|


### TABLE VII 

SOURCES OF PUBLIC DMC PROPRIOCEPTIVE COMPARISON RESULTS 

|Method|Source and protocol|Description|
|---|---|---|
|PPO|Public Proprio Control benchmark from the DreamerV3|PPO reference with fixed hyperparameters|
||paper||
|D4PG / DDPG / <br>DMPO|MPO /<br>Public Proprio Control benchmark from the DreamerV3<br>paper|Public continuous-control comparison results|
|DreamerV3|Public Proprio Control benchmark from the DreamerV3|Public world-model baseline result|
||paper||
|Koopman Dreamer|Implemented and trained in this paper|Uses the configuration in Table VI|


## APPENDIX 

## EXPERIMENTAL DETAILS AND SUPPLEMENTARY RESULTS 

## _A. DMC Proprioceptive Benchmark Details_ 

The PPO, D4PG, DDPG, MPO, DMPO, and DreamerV3 curves used to compute Table I are taken from the public DeepMind Control Suite proprioceptive benchmark reported in the DreamerV3 paper [9]. This benchmark uses continuous actions, proprioceptive vector inputs, and a budget of 500K environment steps. Control Suite tasks use an action repeat of 2. For consistency with the main evaluation protocol in this paper, the reported final score of each baseline seed is computed from the last recorded point in the corresponding public JSON curve, and the table reports the mean over seeds. The DreamerV3 paper reports benchmark results under fixed hyperparameter settings and provides a unified training protocol in its supplementary material. This paper does not repeat the internal hyperparameters of these public baselines and uses them only as published comparison results. Koopman Dreamer is implemented and trained in this paper, with its main configuration shown in Table VI. 

## _B. UAV-LiDAR Configuration and Complete Tables_ 

The UAV experiments use gym <u>UAVLidarNav-v0,</u> with observation key vector and action key action. The main closed-loop navigation evaluation, trajectory visualization, open-loop comparison between DreamerV3 and Koopman Dreamer, spectralradius sensitivity analysis, and structural ablations are all conducted in the Forest scenario, using fixed targets and shared initial conditions as specified in the corresponding experiment. D4PG, DreamerV3, and Koopman Dreamer use the same Forest environment and evaluation protocol for the main closed-loop comparison. Table III summarizes the UAV-LiDAR scenario variants, Table VIII gives the Forest environment and evaluation configuration used in the main experiments, and Table IX lists the method hyperparameters. 

## _C. Supplementary Spectral-Radius Horizon Curves_ 

Fig. 11 complements the horizon-64 summary in Fig. 8 by showing how prediction errors evolve across all evaluated open-loop horizons. 

## _D. Supplementary DMC Open-Loop Curves_ 

Fig. 12 and Fig. 13 provide open-loop prediction curves for all nine DMC proprioceptive tasks. Each evaluation uses a 32-step observation context and a horizon-64 open-loop rollout along recorded action sequences, with 32 replay batches and 16 sequences per batch. The three common metrics summarized in Table II are reported at horizons 1, 5, 10, 20, 32, and 

17 

TABLE VIII 

UAV-LIDAR FOREST AUTONOMOUS NAVIGATION ENVIRONMENT AND EVALUATION CONFIGURATION 

|Category|Configuration item|Value|
|---|---|---|
|Environment<br>Environment|Gymnasium task<br>Forest autonomous navigation environ-<br>ment|gym<br>UAVLidarNav-v0, observation key vector, action key action<br>world size 50 m, 120 cylindrical obstacles, dynamic obstacles disabled|
|Environment|LiDAR|280 dimensions, 7 rings, max range 20 m, proximity encoding, clearance<br>feature enabled|
|Environment|Dynamics and episode|time step 0.1 s, maximum horizontal speed 2.0 m/s, maximum vertical<br>speed 1.0 m/s, max steps 500|
|Evaluation|Fixed targets|(0_,_0_,_2), (18_,_0_,_2), (18_,_18_,_2), (_−_18_, −_18_,_2)|
|Evaluation|Main-comparison scenes|3 shared forest scenes|
|Evaluation|Main-comparison episodes|20 per target per scene, 80 per scene, 240 per method in total|
|Evaluation|Ablation episodes|1 representative shared scene, 20 per target, 80 per variant in total|


TABLE IX 

MAIN HYPERPARAMETERS OF METHODS ON UAV-LIDAR FOREST AUTONOMOUS NAVIGATION 

|Method|Category|Value|
|---|---|---|
|D4PG|Training and sampling|500K agent decision steps, action repeat 1, local actors 16, evaluation episodes 10<br>|
|D4PG|actor / critic|actor MLP 256_,_256_,_256, critic MLP 256_,_256_,_256, distributional critic atoms 51<br>|
|D4PG|replay and batch|batch size 256, min replay size 1000, max replay size 10<sup>6</sup>, samples per insert 0<br>|
|D4PG|optimization and target|learning rate3_×_10<sup>_−_4</sup>, Gaussian exploration standard deviation 0.2, discount 0.99, 5-step<br>return, critic support [_−_150_,_150]|
|DreamerV3|Training and sampling|500K environment steps, 24 parallel environments, evaluation environments 4, evaluation<br>episodes 4, train ratio 128|
|DreamerV3|World-model scale|size25m, deterministic state 3072, hidden size 384, stochastic 32 groups _×_ 24 classes|
|DreamerV3|Batch and policy optimization|batch size 16, batch length 64, imagination length 15, return lambda 0.95|
|Koopman Dreamer|Training and sampling|500K environment steps, 24 parallel environments, evaluation environments 4, evaluation<br>episodes 4, train ratio 128|
|Koopman Dreamer|World-model scale|size25m, _ϕt_ dimension 3072, hidden size 384, stochastic 32 groups _×_ 24 classes, _zt_<br>projection dimension 96|
|Koopman Dreamer|Spectral and control|maximum radius 0.95, minimum radius 0.75, initial radius 0.87, learned radius 0.881,<br>control scale 3.0|
|Koopman Dreamer|Bilinear control|bilinear scale 0.05, bilinear rank 256, bilinear outscale 0.01|
|Koopman Dreamer|Stochastic<br>modulation<br>and<br>teacher|_z_ scale 0.10, dense scale 0.0, teacher EMA rate 0.01|
|Koopman Dreamer|Auxiliary losses|koop 0.005, roll 0.005, opreg 0.001, pred 0.01; warmups are 150K, 100K, 200K, and<br>60K, respectively|


### TABLE X 

COMPLETE NUMERICAL RESULTS FOR THE FOUR-TARGET UAV-LIDAR FOREST AUTONOMOUS NAVIGATION EVALUATION AVERAGED OVER THREE 

SHARED EVALUATION SCENES 

|Method|Episodes|Return mean|Return median|Success|Failure|Length mean|Path mean|Dist median|
|---|---|---|---|---|---|---|---|---|
|D4PG|240|46.52|67.81|15.8%|84.2%|386.00|72.88|4.22|
|DreamerV3|240|**169.21**|182.19|53.8%|46.2%|359.76|60.09|0.75|
|Koopman|||||||||
|Dreamer|240|161.98|**195.50**|**73.8%**|**26.2%**|**194.70**|**40.45**|**0.72**|


### TABLE XI 

COMPLETE ABLATION RESULTS ON UAV-LIDAR FOREST AUTONOMOUS NAVIGATION 

|Variant|Episodes|Return mean [95% CI]|Success|Collision|Timeout|Successful-trajectory<br>action variation<br>median [IQR]|
|---|---|---|---|---|---|---|
|Koopman|||||||
|Dreamer|80|163.82 [140.85, 184.88]|57/80 (71.2%)|15.0%|13.8%|0.97 [0.89, 1.10]|
|w/o spectral|80|130.33 [107.80, 151.85]|58/80 (72.5%)|16.2%|11.2%|4.00 [3.67, 4.26]|
|w/o teacher|80|143.20 [116.25, 169.06]|55/80 (68.8%)|28.7%|2.5%|1.06 [0.90, 1.27]|
|w/o bilinear|80|15.64 [-3.57, 35.78]|7/80 (8.8%)|56.2%|35.0%|0.52 [0.45, 0.61]|


CI denotes confidence interval, and IQR denotes interquartile range. Return CIs are obtained by stratified bootstrap resampling within each of the four target sets. Action variation is the temporal mean of the squared Euclidean difference between consecutive actions on successful trajectories. 

64; where applicable, the task figures additionally show errors for task-specific state components. Overall, Koopman Dreamer gives the most consistent improvement in deterministic-latent prediction, with lower horizon-64 error on all nine tasks, and it lowers proprioceptive and reward prediction error on most tasks. These results support the role of the spectrally constrained 

18 


Fig. 11. Open-loop prediction error as a function of prediction horizon under different learned spectral radii in the UAV-LiDAR Forest scenario. The six panels report mean-squared errors for the complete observation vector, LiDAR observations, velocity, target-relative position, reward, and deterministic latent state. Solid lines indicate means over evaluation batches, and shaded regions indicate approximate 95% confidence intervals of batch means. 

backbone in improving long-horizon latent propagation and task-relevant prediction. 

19 


20 


Fig. 13. Complete open-loop prediction curves on DMC proprioceptive tasks, part 2. 

