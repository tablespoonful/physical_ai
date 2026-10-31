---
title: "Morphology-Conditioned World Model for Cross-Embodiment Quadrupedal Locomotion"
date: "2026-04-09"
authors: "Mohamad H. Danesh; Chenhao Li; Amin Abyaneh; Anas Houssaini; Kirsty Ellis; Glen Berseth"
url: https://arxiv.org/abs/2604.08780
pdf: https://arxiv.org/pdf/2604.08780
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.08780)** / [論文ページ](https://arxiv.org/abs/2604.08780)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Morphology-Conditioned World Model for Cross-Embodiment Quadrupedal Locomotion** 

**Mohamad H. Danesh**<sup>1</sup><sup>_,_2</sup> **Chenhao Li**<sup>3</sup> **Amin Abyaneh**<sup>1</sup><sup>_,_2</sup> **Anas Houssaini**<sup>1</sup><sup>_,_2</sup> **Kirsty Ellis**<sup>2</sup><sup>_,_4</sup> **Glen Berseth**<sup>2</sup><sup>_,_4</sup> **Marco Hutter**<sup>3</sup> **Hsiu-Chin Lin**<sup>1</sup><sup>_,_2</sup> 

- 1McGill University, Canada 2Mila - Quebec AI Institute, Canada 

3ETH Zurich, Switzerland 4Universite de Montreal, Canada 

**Abstract:** World models promise a paradigm shift in robotics, where an agent learns the physics of its environment once and then acquires behaviors efficiently. Yet the learned dynamics models at their core are typically morphology locked. In legged locomotion, a dynamics model trained on an ANYmal-D quadruped fails on a Unitree Go1 because it overfits to one robot’s embodiment rather than capturing the locomotion dynamics shared across robots, so even a small change in actuator dynamics or limb length forces retraining from scratch. However, if we formalize a robot’s unique physical traits into a morphology specification, a controller for a family of robots can utilize this blueprint in two ways. It can feed the specification to a model-free policy, or it can feed the specification to a learned dynamics model and extract the policy in imagination. We argue for the second route and introduce the Quadrupedal World Model (QWM), which conditions a single generative dynamics model on scale-invariant physical features and trains policies entirely inside it, through a physical morphology encoder, an adaptive reward normalizer, and morphology conditioning in the latent dynamics. Holding the morphology information identical, a model-free policy matches QWM on the training cohort but degrades on unseen morphologies, while QWM transfers zeroshot with no fine-tuning, adaptation, or warm-up in such cases. To our knowledge, this is the first world model to demonstrate zero-shot cross-embodiment transfer within the quadrupedal family. 

## **1 Introduction** 

Robot learning is data hungry, and data is mostly collected on a single hardware platform, so the resulting controllers and the dynamics models on which they rely overfit to specific kinematic and dynamic properties [1]. Upgrading motors or deploying across a heterogeneous fleet then means collecting new samples and retraining from scratch [2, 3]. Large scale simulations [4, 5, 6] ease the wall-clock cost of training but do not remove the coupling between a learned model and its training hardware. Furthermore, blind domain randomization without informative conditioning tends toward conservative control rather than performance tuned to the robot at hand [7]. Our starting point is a simple insight. A useful model of locomotion should capture not how _one_ robot moves, but how robots within _a morphological family_ move. This shared understanding allows a single model to leverage training data across different scales, ensuring that a hardware change no longer requires relearning dynamics from scratch. 

Such a model must know which robot it is controlling, since across a family the transition dynamics vary mostly based on the embodiment. We summarize a robot by a morphology vector _µ_ that encodes its kinematic constraints, mass distribution, and actuator limits. We take _µ_ to be given by the robot’s engineering description, since a nominal specification such as a Universal Scene Description already records the geometry and inertial properties that distinguish one platform from another. When such a description is unavailable, _µ_ is instead inferred from interaction history, often 


Figure 1: Overview of QWM. **Left** : The heterogeneous quadrupedal morphology cohort. **Middle** : Training pipeline, where robot data is processed by PME (Subsec. 4.2) to extract the morphology vector _µ_ , which together with environment observations trains QWM, while ARN (Subsec. 4.3) keeps the reward signals consistent across diverse platforms. **Right** : Deployment pipeline, where for an unseen robot the same PME module from training extracts its morphology vector _µ_ . 

to refine an imperfect prior [8, 9], a setting that is complementary to ours rather than competing with it. We study the regime in which an accurate _µ_ is available, where the design question we care about is cleanest. The question is then not how to obtain _µ_ but how it should be used. One option feeds _µ_ to a model-free policy and learns the controller directly [10, 11]. The other feeds _µ_ to a dynamics model and recovers the controller by training in imagination on that model [12, 13]. 

We argue that for cross-embodiment generalization, the second option is the better utilization of _µ_ . The dynamics of a legged robot are governed by physics and vary smoothly with morphology, since changing a limb’s length or mass moves the equations of motion continuously, whereas the optimal control law for those dynamics need not vary smoothly, since small physical changes can reshape a gait. A model that learns the shared dynamics of a family and is conditioned on _µ_ can therefore synthesize a coherent simulator for an unseen morphology by interpolating in physical feature space, and a policy re-derived against that simulator inherits the generalization, while a policy that maps _µ_ directly to actions must generalize a rougher function. The obstacle is that existing world models (WMs) are morphology locked, a model trained on a heavy robot overfits to its dynamics and fails on a lighter one [14, 15, 16, 17, 13, 18]. Our contribution is to make the model-based route work across a family, capturing the shared physics of locomotion while conditioning on what differs between robots, following the roadmap for _Type III Robotic Agents_ [19]. 

We take a first step toward a generalizable Quadrupedal World Model (QWM), a morphologyconditioned dynamics model for a quadrupedal kinematic family (Fig. 1). QWM comprises three components: a fusion architecture that injects morphology features into the WM, a Physical Morphology Encoder (PME) that derives scale-invariant features _µ_ from robot descriptions, and an Adaptive Reward Normalizer (ARN) that balances learning signals across robots with heterogeneous reward scales. To isolate the value of the model-based route, our comparison holds morphology information fixed and contrasts QWM against model-free baselines conditioned on identical _µ_ . The two match on the training cohort, yet across unseen morphologies, parameter inaccuracy, and unmodeled dynamics, QWM generalizes significantly better, including zero-shot transfer to hardware. 

## **2 Related Work** 

**MBRL** improves sample efficiency by learning predictive environment models [12, 20]. While early methods relied on Gaussian processes [21], modern approaches scale to complex environments by planning in latent spaces [22]. Notably, the Dreamer family [16, 17, 14] demonstrated that policies can be learned entirely in imagination, with DreamerV3 [14] providing robustness via symlog predictions and KL balancing. This shift toward WMs is supported by theory suggesting they are inherent to general agents [23]. As the paradigm matures, the foundational RSSM architecture [16] is being replaced by Transformers [24, 25], discrete autoencoders [26, 27], stochastic transformers [28], contrastive coding [29], and linear attention or state-space models [30, 31]. Within robotics, MBRL has enabled significant milestones, starting with DayDreamer’s [13] online learning and expanding into long-horizon prediction [18], visual reconstruction [32, 33], and offline-to-online adaptation via epistemic uncertainty [34]. Today, applications span sim-to-real distillation of privileged WMs [35], humanoid terrain traversal [36], manipulation [37, 38], safety [39], and robust exploration [40, 41, 42]. Yet, despite these varied successes, existing models remain fundamentally 

2 

tied to a single embodiment. Overcoming this limitation, by learning dynamics that transfer across morphological changes, is the precise gap our work targets. 

**Generalist and cross-embodiment control** scales a single controller across tasks or robots. TDMPC2 [43] learns latent task embeddings, PWM [44] extracts policies via first-order optimization through differentiable WMs, and others adapt from offline data [45, 46, 47]. In locomotion, several methods rely on analytical priors or heuristic skill selection [48, 49, 50]. In contrast, QWM operates directly in joint space by mapping robot descriptions to dynamics, enabling planning without analytical inverse kinematics. Furthermore, where prior multi-robot methods must balance heterogeneous objectives via complex loss weighting [51, 52], we bypass this complexity using a lightweight per-robot reward Exponential Moving Average (EMA). 

**Morphology representation** for cross-embodiment generalization largely relies on architectural biases. GNNs model the kinematic tree [53, 54, 55], sometimes with symmetry constraints [56, 57] or heterogeneous nodes [58], while transformers tokenize the kinematic chain [59, 60, 61, 62, 63], scaling to thousands of procedural embodiments [64]. Others infer morphology implicitly from interaction history [8, 9, 65] or learn latent action spaces [66, 67, 18, 68], which suits settings without an explicit description but requires a warm-up interaction phase before deployment, the generalization gap Fung et al. [19] flag as critical. Since we target the regime where an accurate description is available, we instead use explicit parametric encoding [10, 69, 11], computing scaleinvariant features fed directly into the WM for zero-shot adaptation without the overhead of GNNs. 

## **3 Background** 

We formulate locomotion as a Partially Observable Markov Decision Process ( _S, O, A, P, R, γ_ ), where _S_ denotes the simulator state space, _O_ the observation space, _A_ the action space specifying target joint positions, _R_ ( _st, at_ ) the reward function producing reward _rt_ , and _γ ∈_ [0 _,_ 1) the discount factor. The transition dynamics are defined by a stochastic transition function _P_ ( _st_ +1 _| st, at_ ), which specifies the probability distribution over next states given the current state and action. At time _t_ , the agent receives a partial observation _ot ∈O_ consisting of joint positions, joint velocities, base linear velocity, angular velocity, projected gravity, velocity commands, and previous actions. 

### **3.1 Recurrent State-Space Models** 

Our WM backbone is based on the Recurrent State-Space Models (RSSM) introduced in the Dreamer family of algorithms [14, 16, 17]. RSSMs enable learning in partially observable environments by decomposing the latent state into a deterministic recurrent state _ht_ that aggregates history (short-term memory) and a stochastic state _zt_ that captures information about the current observation (spatial representation). Parameterized by _ϕ_ , these components evolve through a deterministic function _fϕ_ and the probability distributions _pϕ_ and _qϕ_ : 


The dynamics evolve through the _Recurrent Model_ (Eq. 1), which updates the memory _ht_ based on the previous action. During training, the _Representation Model_ (Eq. 2) infers the posterior state _zt_ using the observation _ot_ , whereas during planning, the _Transition Predictor_ (Eq. 3) predicts the prior _z_ ˆ _t_ solely from history. To ground these latents, the model reconstructs observations via the _Decoder_ and predicts training signals via the _Reward_ and _Continuation_ heads (Eq. 4). 

The model parameters _ϕ_ are optimized by minimizing a variational bound that includes reconstruction of observations _ot_ , prediction of the reward _rt_ and continuation signal _ct ∈{_ 0 _,_ 1 _}_ , and a KL-divergence regularizer that forces the prior (imagination) to align with the posterior (reality): 


3 

### **3.2 Learning Policy in Imagination** 

A key advantage of WMs is the decoupling of policy learning from physical interaction. The policy _πθ_ ( _at|ht, zt_ ) and critic _Vψ_ ( _ht, zt_ ), parameterized by _θ_ and _ψ_ respectively, are trained entirely on _imagined trajectories_ rolled out by the transition predictor. Starting from an initial state, the model interacts with itself by sampling _at ∼ πθ_ ( _· | ht,_ ˆ _zt_ ), where _ht_ +1 and ˆ _zt_ +1 come from Eq. 1 and Eq. 3, respectively. Because the policy is trained only against the model’s latent dynamics, its behavior on a new robot is as good as the model is for that robot. This shifts the burden of cross-morphology transfer from the policy onto the dynamics model, and it is the property we exploit. When the model represents the new robot’s dynamics properly, the policy can be rolled out zero-shot in imagination and deployed without further interaction. 

## **4 Quadrupedal World Model** 

We build upon DreamerV3 [14], modifying the encoder and transition dynamics to be conditioned on _µ_ . For a family of robots, the transition is no longer fixed but varies with the robot, which we write as _Pµ_ ( _st_ +1 _| st, at_ ) for a morphology variable _µ ∈M_ that ranges over quadrupedal embodiments. QWM adds three components. The first is a morphology-conditioned WM that fuses static morphology features with dynamic proprioception. The second is the PME, which derives those features from robot description files. The third is an ARN scheme that stabilizes learning across heterogeneous robots, given their various reward scales. 

### **4.1 Morphology-Conditioned World Model** 

To effectively utilize the morphology vector _µ_ , we modify the standard RSSM at two points, the recurrent model (Eq. 1) and the observation encoder feeding the representation model (Eq. 2). A naive concatenation of static features _µ_ with high-frequency observations _ot_ often leads to the static signal being “washed out” by the high-variance dynamic data. To mitigate this, we employ a dualtower encoder architecture in which the observation encoder is split into two pathways. The _dynamic tower_ processes the proprioceptive stream _ot_ via an MLP. Simultaneously, the _static tower_ processes the morphology vector _µ_ via a separate MLP to project it into the same latent dimension. These are concatenated and fused into the observation embedding _et_ consumed by the representation model (Eq. 2) as _et_ = Linear([MLPdyn( _ot_ ) _,_ MLPstat( _µ_ )]). The QWM posterior is therefore _zt ∼ qϕ_ ( _zt | ht, et_ ) with _et_ being a function of both _ot_ and _µ_ , so the posterior has access to _µ_ through the static tower. This ensures that the encoder allocates dedicated capacity to representing the robot’s physical structure before fusing it with the state. 

Notably, the morphology _µ_ is not just used for encoding. It is also injected directly into the recurrent dynamics. We augment Eq. 1’s transition function so that it explicitly depends on the robot type: 


By providing _µ_ to the recurrent model at every time step, we relieve it of the burden of memorizing static physical properties in its short-term memory _ht_ . This disentanglement allows the recurrent state to focus purely on the _dynamic_ state of the system (e.g., velocity, contact timing) while the explicit conditioning handles the _static_ physics (e.g., limb length, mass), facilitating robust control across distinct morphologies. 

### **4.2 Physical Morphology Encoder** 

Rather than treating morphology as a variable inferred from interaction history [8] or an imperfect description, we formalize it as a mapping Φ : _U →_ R<sup>_d_</sup> from the robot’s description space _U_ to a raw feature vector _µ_ raw, which we then normalize into the morphology vector _µ_ . Following prior work [10, 69, 11], we extract features that parameterize the equations of motion, decomposing the description into kinematic, geometric, and dynamic properties that capture variations in leverage, 

4 

stability margins, and rotational inertia. _µ_ assumes a quadrupedal template with three-segment legs, parameterizing variation _within_ this family. We decompose it into four groups as follows. 

_Kinematics & Topology_ ( _µ_ kin) extracts segment lengths and knee configuration by traversing the front-left leg [53, 55], distinguishing inward “X” knees from outward “dog-like” configurations (Fig. 1). _Geometry_ ( _µ_ geo) describes the robot’s footprint via the longitudinal and lateral distances between hip joints together with their aspect ratio, a scale-invariant indicator of body shape that ranges from a narrow lateral stance to a square footprint. _Dynamics_ ( _µ_ dyn) captures mass distribution, which governs rotational inertia and force response, and is encoded as a log-scaled total mass alongside the trunk mass fraction. Finally, _Actuation_ ( _µ_ act) captures weight-normalized torque to inform cross-embodiment transfer [70, 8], accounting for how sufficient torque scales depending on the robot’s weight. 

The vector _µ_ raw = [ _µ_ kin _, µ_ geo _, µ_ dyn _, µ_ act] mixes various units, so we apply min-max normalization to obtain _µ_ = Ψ( _µ_ raw) _∈_ [ _−_ 1 _,_ 1]<sup>_d_</sup> . Importantly, _µ_ encodes _idealized_ rigid-body properties, and unmodeled residuals such as payload variation are absorbed instead by the dynamic latents ( _ht, zt_ ). These let the model distinguish, for example, the high-center-of-mass Spot from the compact Go1 (App. D). 

### **4.3 Adaptive Reward Normalizer** 

Training a single agent across heterogeneous robots raises a reward-scaling challenge. All robots share the velocity-tracking objective, yet their reward formulations and penalty weights differ to accommodate distinct hardware (App. A). Since the WM learns to predict rewards alongside dynamics, training on raw rewards causes robots with larger rewards to unevenly dominate the loss. 

We therefore implement ARN using quantile-based scaling. Rather than a fixed scalar, we maintain per robot-type an EMA (momentum _α_ ) of the inter-percentile range between the 5<sup>th</sup> and 95<sup>th</sup> percentiles of the returns, which yields the reward scale _σR_ . The max in the denominator prevents the inflation of trivially small rewards early in training and avoids division by zero: 


The mechanism acts as an adaptive equalizer. When a robot consistently generates large torque penalties, its _σR_ expands and dynamically scales the signal down, so QWM receives a learning signal comparable in scale across morphologies. This prevents any single embodiment from dominating the latent representation and enables stable, simultaneous multi-robot training. 

## **5 Experiments** 

Our experiments test the claim that given the same morphology specification _µ_ , conditioning a learned dynamics model on _µ_ and extracting a policy in imagination generalizes to unseen morphologies better than conditioning a model-free policy on the same _µ_ . We organize the evidence as follows. Both routes master the heterogeneous training cohort, and the model-free route reaches the same performance with more data, so any later gap is a generalization gap and not a capability gap (Subsec. 5.1). QWM reproduces the dynamics of diverse robots over long horizons, which is the substrate the model-based route relies on (Subsec. 5.2). On held-out morphologies, QWM stays near specialist performance while a model-free policy given the identical _µ_ degrades and collapses (Subsec. 5.3). The frozen zero-shot policies then run on real hardware (Subsec. 5.4). We also show that the learned latent state absorbs residuals when the specification is inaccurate or the robot drifts from it, which a pure specification-driven controller cannot (App. H). We assume throughout that an accurate _µ_ is available and that domain randomization spans the deployment conditions, so the residuals between the idealized _µ_ and the real robot stay within the range the latent state has learned to absorb. Unless noted, we train on the full heterogeneous cohort. 

5 


Figure 2: Training performance and dynamics fidelity on the heterogeneous cohort. Shaded regions denote std over 5 seeds. **Left panel** : Learning curves on the full heterogeneous cohort, with mean reward (top) and mean episode length (bottom). **Right panel** : Long-horizon dynamics prediction. Open-loop ground truth is compared against imagination over 85 steps, where QWM stays synchronized across scales with minor late deviations (circled). The plots report NMSE over the training prediction window (32 trajectories), normalized by each robot’s natural motion variance, where QWM accumulates error gradually but does not diverge. 

### **5.1 Multi-Morphology Mastery** 

We first test whether QWM handles the interference that arises from training across morphologies simultaneously. We compare against three model-free baselines and three WM methods. The modelfree baselines are Vanilla PPO [71], PME-PPO (our PME conditioning _µ_ into PPO via concatenation), and Body Transformer (BoT) [63], which models the body as a graph via masked attention. The WM baselines are DreamerV3 [14], PWM [44], and TWISTER [29], all of which must infer morphology implicitly from proprioceptive history without our PME or ARN. We track mean reward (App. A.2) and episode length (up to 1000 steps) across 4,096 parallel environments. 

As shown in Fig. 2 (left panel), the methods that receive _µ_ explicitly master the cohort, while the methods that must infer it from history do not. Among the model-free baselines, PME-PPO reaches the same asymptotic performance as QWM and clearly exceeds Vanilla PPO, although it needs roughly twice the environment steps to begin converging. BoT-PPO trails PME-PPO, since its highcapacity graph attention carries more optimization and sample cost than our compact MLP encoder, which makes PME-PPO the strongest like-for-like model-free baseline rather than a weak one. The WM baselines, which infer morphology from proprioceptive history rather than from an explicit _µ_ , settle into a mean-dynamics solution on this heterogeneous cohort and do not reach a controllable policy. We read this not as a verdict on implicit identification, which targets the harder setting where no description is available, but as motivation for our premise. When an accurate description exists, supplying _µ_ explicitly removes the need to recover it online, and the open question is how to use it. The training curves settle the first half of that question. Both PME-PPO and QWM, given the identical _µ_ , learn the full cohort, so _µ_ is a sufficient statistic for mastering these kinematic chains under either learning paradigm. They differ only in cost, with QWM reaching competitive reward and episode length in about half the environment steps of PME-PPO and additionally yielding a reusable dynamics model. On the training cohort the two routes are therefore comparable in capability, which isolates the model-free versus model-based question for the generalization experiments that follow. 

**Component ablations.** App. E localizes these gains. ARN is a precondition because every variant without it flatlines near zero reward, confirming that unnormalized heterogeneous reward scales alone prevent the WM from forming. Given ARN, the two morphology-injection sites play distinct, dissociable roles. Removing encoder conditioning permits early learning but triggers a late catastrophic collapse, indicating the latent posterior must be grounded in static physical context to remain stable over long horizons. Removing RSSM conditioning instead degrades sample efficiency and leaves a sub-optimal asymptotic reward, showing the recurrent state cannot retain morphology 

6 

without step-wise re-injection. Removing explicit morphology entirely still learns to stay upright but plateaus below the full method, so implicit identification suffices for basic locomotion but not for refined gaits. Each component is necessary, and they fail in different ways. 

### **5.2 Long-Horizon Dynamics Prediction** 

To verify that QWM functions as a reliable neural simulator, we evaluate its open-loop prediction fidelity. In Fig. 2 (right panel), we initialize with a short context ( _T_ = 5) and unroll 85 steps of pure imagination on ANYmal-D and Unitree Go1, feeding only the policy’s actions. The long horizon exposes gait-level divergence that shorter rollouts would hide. The imagined trajectories stay tightly synchronized with the ground truth, with only minor deviations near the end of the rollout, confirming that QWM parameterizes dynamics for diverse robots simultaneously. 

Quantitatively (Fig. 2 (right panel-plots)), we report the Normalized Mean Squared Error (NMSE) of predicted proprioception over the training prediction window (32 episodes per robot, normalized by per-robot motion variance for cross-morphology comparison). QWM maintains the lowest error among the learned WMs with minimal accumulation, which indicates a stable physical attractor rather than drift. The models that infer morphology implicitly do not reach this fidelity on the heterogeneous cohort, consistent with their lower training performance. Without explicit conditioning, a single WM must average over the conflicting dynamics of a diverse cohort, which is the failure mode that our _µ_ injection is designed to remove. 

### **5.3 Zero-Shot Generalization to Unseen Morphologies** 

To test whether QWM learns physics-grounded dynamics rather than overfitting to specific hardware, we evaluate on held-out morphologies under two regimes drawn from our per-feature leaveone-out (LOO) deviation analysis (App. D), one holding out robots whose every feature lies within the cohort’s range (Go1, ANYmal-D) and one holding out a robot that deviates strongly on several axes at once (B2). To evaluate a target robot _r_ , we train models from scratch on the seven robots excluding _r_ . We characterize each case by its full per-feature deviation profile rather than a single scalar distance, since features affect dynamics non-uniformly. 

|In all cases, all weights are frozen and condi-||||||
|---|---|---|---|---|---|
|tioned solely on the target’s_µ_. Our central com-|Table 1: <br>|Zero-s<br>|hot generaliz<br>|ation perfor<br>|mance on un<br>|
|parison is against PME-PPO, the model-free<br>policy given the same_µ_, which isolates whether<br>eneralizationstemsfromaloneorfromthe|seen robo<br>**Method**|ts. Me<br>**Metric**|an_±_std over<br>**ANYmal-D**|5 seeds (12<br>**Unitree Go1**|8 envs/seed).<br>**Unitree B2**|
|g   _µ_    <br>learned dynamics, with a Specialist PPO oracle|PME-PPO|<sup>Rwd.</sup><br>Len.|10_._1_±_1_._9<br>530_±_8_._2|23_._1_±_2_._3<br>602_±_14_._9|_−_0_._2_±_3_._2<br>337_±_23_._1|
|trained per target robot as an empirical upper<br>boundWeomittheimlicitbaselineswhich|QWM|Rwd.<br>Len.|18_._2_±_2_._3<br>948_._6_±_12_._1|35_._5_±_3_._4<br> 974_._4_±_6_._2|12_._1_±_4_._2<br> 925_._4_±_17_._2|
|.    p , <br>did not reach a controllable policy on the train-|Specialist<br>PPO|Rwd.<br>Len.|21_._8_±_1_._2<br>981_._3_±_4_._2|39_._7_±_2_._1<br>996_._1_±_1_._1|13_._6_±_4_._2<br>961_._1_±_8_._9|
|ing cohort (Subsec. 5.1).||||||


Table 1: Zero-shot generalization performance on unseen robots. Mean _±_ std over 5 seeds (128 envs/seed). 

**Within-range transfer.** On the training cohort the two routes are comparable (Fig. 2 (left panel)), so any gap here is a generalization gap rather than a capability one. On the held-out Go1 and ANYmalD (Table 1), QWM matches specialist episode length and recovers 80-90% of specialist reward, while PME-PPO, given the same _µ_ but no learned dynamics, trails substantially (episode length 602 vs. 974 on Go1). Both robots sit inside the cohort’s per-axis support (App. D). Because each axis is individually represented in training, the WM synthesizes the held-out dynamics by interpolating its learned latent geometry along each physical dimension. 

**Out-of-range transfer.** Under the same comparison, B2 is elevated on several axes at once, all pushing the same direction toward larger, heavier, and stronger. Each deviation is individually bounded, but no single training robot combines this inertia with this stance and actuator capacity, leaving the configuration jointly unrepresented. This is a combinatorial gap rather than a large scalar distance, which is why a model-free policy given _µ_ cannot bridge it. QWM, on the same _µ_ , instead reaches near-specialist locomotion zero-shot, within about 4% of the episode-length and 11% of the reward 

7 

upper bound. The _µ_ -conditioned latent dynamics thus supply the inductive bias to synthesize a controller for a jointly unseen configuration, combining mild extrapolation on mass and torque capacity with interpolation along the remaining axes rather than relying on a single nearest neighbor. Latentspace evidence, that kinematically similar robots occupy neighboring regions while dynamic state varies smoothly within each, appears in App. G. 

The gain comes from learned dynamics, not from access to _µ_ . Two perturbation studies isolate this (App. H). When we corrupt _µ_ on a nominal world, QWM retains _∼_ 80% of its episode length even at 20% corruption while PME-PPO, reading the same _µ_ , falls to roughly a third, because QWM’s latent state _zt_ re-reads the true dynamics from observations and corrects the mis-specified input. When we instead hold _µ_ correct and perturb the true world through torque loss or added payload, even a near-exact analytical rigid-body predictor conditioned on the nominal _µ_ diverges, since it simulates a robot that no longer exists, whereas QWM stays bounded and retains 75-84% of its nominal episode length. A model-free _µ_ -policy and a static analytical prior both lack this correction channel, so the advantage we report is a property of routing _µ_ through learned dynamics rather than holding _µ_ at all. 

### **5.4 Real-World Deployment** 

The physical world introduces unmodeled dynamics absent from both the robot specification and simulaTable 2: Quantitative real-world results (10 trition, such as actuator backlash and motor nonlinearials _×_ 60s per platform). ties. We deploy the two frozen zero-shot agents from **Platform Method** _exy_ (m/s) _↓ eyaw_ Subsec. 5.3, the held-out ANYmal-D and Go1, diANYmal-D QWM 0 _._ 30 0 _._ rectly onto hardware using the exact simulation polSpecialist PPO 0 _._ 28 0 _._ icy weights, with inference at 50Hz on each platform’s Unitree Go1<sup>QWM</sup> 0 _._ 34 0 _._ Specialist PPO 0 _._ 31 0 _._ onboard computer (Fig. 3). This zero-shot behavior transferred directly to hardware. The agent produced a high-frequency trot on the agile Go1 and a slower, grounded gait on the heavier ANYmal-D, achieving stable locomotion on both without any real-world finetuning. As shown in Table 2, QWM tracks velocity commands within _∼_ 10-13% of the specialist baseline with zero falls across all trials, despite never interactFigure 3: Real-world deployment on the ing with either robot during training, confirming that out Unitree Go1 and ANYmal-D. explicit morphology conditioning encodes the physics needed to control unseen real robots rather than simulation artifacts. Further details in App. F. 

Table 2: Quantitative real-world results (10 trials _×_ 60s per platform). 

|**Platform**|**Method**<br>_e_|_xy_ (m/s)_↓_|_eyaw_ (rad/s)_↓_|
|---|---|---|---|
|ANYmal-D|QWM<br>Specialist PPO|0_._30<br>0_._28|0_._29<br>0_._26|
|Unitree Go1|<sup>QWM</sup><br>Specialist PPO|0_._34<br>0_._31|0_._34<br>0_._30|


Figure 3: Real-world deployment on the heldout Unitree Go1 and ANYmal-D. 

## **6 Limitations** 

Our results are bounded in scope. The vector _µ_ encodes a fixed quadrupedal template with threesegment legs, a 12-DoF action space, and a stance rooted at the hip joints, so generalization is parametric _within_ this template and not across structural variants such as differing joints per leg or non-quadrupedal bodies. Our evaluation is limited to “blind” flat-ground velocity tracking without exteroception or contact-rich terrain. 

## **7 Conclusion** 

We introduce QWM, a step toward generalist dynamics model achieving zero-shot sim-to-real locomotion across diverse quadrupeds by conditioning on scale-invariant physical features. Crucially, these learned dynamics absorb real-world physical divergences, a capability we validate against a model-free controller that fails on outliers despite receiving the identical _µ_ . Ultimately, QWM shows that cross-embodiment morphology data must route through learned dynamics rather than directly into policies, as dynamics within a morphological family vary smoothly unlike optimal policies. 

8 

## **References** 

- [1] W. Liu, H. Zhao, C. Li, J. Biswas, S. Pouya, and Y. Chang. Compass: Cross-embodiment mobility policy via residual rl and skill synthesis. _arXiv preprint arXiv:2502.16372_ , 2025. 

- [2] D. Yarats, A. Zhang, I. Kostrikov, B. Amos, J. Pineau, and R. Fergus. Improving sample efficiency in model-free reinforcement learning from images. _Proceedings of the AAAI Conference on Artificial Intelligence_ , 35(12):10674–10681, May 2021. doi:10.1609/aaai.v35i12.17276. URL https://ojs.aaai.org/index.php/AAAI/article/view/17276. 

- [3] I. Kostrikov, L. M. Smith, and S. Levine. Demonstrating A Walk in the Park: Learning to Walk in 20 Minutes With Model-Free Reinforcement Learning. In _Proceedings of Robotics: Science and Systems_ , Daegu, Republic of Korea, July 2023. doi:10.15607/RSS.2023.XIX.056. 

- [4] NVIDIA. Isaac sim. https://github.com/isaac-sim/IsaacSim, 2025. Version 5.1.0, Apache-2.0 License. 

- [5] M. Mittal, P. Roth, J. Tigue, A. Richard, O. Zhang, P. Du, A. Serrano-Mu˜noz, X. Yao, R. Zurbr¨ugg, N. Rudin, L. Wawrzyniak, M. Rakhsha, A. Denzler, E. Heiden, A. Borovicka, O. Ahmed, I. Akinola, A. Anwar, M. T. Carlson, J. Y. Feng, A. Garg, R. Gasoto, L. Gulich, Y. Guo, M. Gussert, A. Hansen, M. Kulkarni, C. Li, W. Liu, V. Makoviychuk, G. Malczyk, H. Mazhar, M. Moghani, A. Murali, M. Noseworthy, A. Poddubny, N. Ratliff, W. Rehberg, C. Schwarke, R. Singh, J. L. Smith, B. Tang, R. Thaker, M. Trepte, K. V. Wyk, F. Yu, A. Millane, V. Ramasamy, R. Steiner, S. Subramanian, C. Volk, C. Chen, N. Jawale, A. V. Kuruttukulam, M. A. Lin, A. Mandlekar, K. Patzwaldt, J. Welsh, H. Zhao, F. Anes, J.-F. Lafleche, N. Mo¨enne-Loccoz, S. Park, R. Stepinski, D. V. Gelder, C. Amevor, J. Carius, J. Chang, A. H. Chen, P. de Heras Ciechomski, G. Daviet, M. Mohajerani, J. von Muralt, V. Reutskyy, M. Sauter, S. Schirm, E. L. Shi, P. Terdiman, K. Vilella, T. Widmer, G. Yeoman, T. Chen, S. Grizan, C. Li, L. Li, C. Smith, R. Wiltz, K. Alexis, Y. Chang, D. Chu, L. J. Fan, F. Farshidian, A. Handa, S. Huang, M. Hutter, Y. Narang, S. Pouya, S. Sheng, Y. Zhu, M. Macklin, A. Moravanszky, P. Reist, Y. Guo, D. Hoeller, and G. State. Isaac lab: A gpu-accelerated simulation framework for multi-modal robot learning. _arXiv preprint arXiv:2511.04831_ , 2025. URL https://arxiv.org/abs/2511.04831. 

- [6] G. Authors. Genesis: A generative and universal physics engine for robotics and beyond, December 2024. URL https://github.com/Genesis-Embodied-AI/Genesis. 

- [7] M. H. Danesh, M. Wabartha, S. Wu, J. Pineau, and H.-C. Lin. Safe domain randomization via uncertainty-aware out-of-distribution detection and policy adaptation. _arXiv preprint arXiv:2507.06111_ , 2025. 

- [8] A. Kumar, Z. Fu, D. Pathak, and J. Malik. Rma: Rapid motor adaptation for legged robots. In _Proceedings of Robotics: Science and Systems_ , 2021. 

- [9] W. Yu, J. Tan, C. K. Liu, and G. Turk. Preparing for the unknown: Learning a universal policy with online system identification. In _Proceedings of Robotics: Science and Systems_ , 2017. 

- [10] T. Chen, A. Murali, and A. Gupta. Hardware conditioned policies for multi-robot transfer learning. _Advances in Neural Information Processing Systems_ , 31, 2018. 

- [11] Z. Xiong, J. Beck, and S. Whiteson. Universal Morphology Control via Contextual Modulation. In _Proceedings of the 40th International Conference on Machine Learning_ , pages 38286–38300. PMLR, July 2023. 

- [12] R. S. Sutton. Dyna, an integrated architecture for learning, planning, and reacting. _SIGART Bull._ , 2(4):160–163, July 1991. ISSN 0163-5719. doi:10.1145/122344.122377. URL https: //doi.org/10.1145/122344.122377. 

9 

- [13] P. Wu, A. Escontrela, D. Hafner, P. Abbeel, and K. Goldberg. Daydreamer: World models for physical robot learning. In K. Liu, D. Kulic, and J. Ichnowski, editors, _Proceedings of The 6th Conference on Robot Learning_ , volume 205 of _Proceedings of Machine Learning Research_ , pages 2226–2240. PMLR, 14–18 Dec 2023. URL https://proceedings.mlr.press/v205/ wu23c.html. 

- [14] D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap. Mastering diverse control tasks through world models. _Nature_ , pages 1–7, 2025. 

- [15] D. Silver, J. Schrittwieser, K. Simonyan, I. Antonoglou, A. Huang, A. Guez, T. Hubert, L. Baker, M. Lai, A. Bolton, et al. Mastering the game of go without human knowledge. _nature_ , 550(7676):354–359, 2017. 

- [16] D. Hafner, T. Lillicrap, I. Fischer, R. Villegas, D. Ha, H. Lee, and J. Davidson. Learning latent dynamics for planning from pixels. In _International conference on machine learning_ , pages 2555–2565. PMLR, 2019. 

- [17] D. Hafner, T. P. Lillicrap, M. Norouzi, and J. Ba. Mastering atari with discrete world models. In _International Conference on Learning Representations_ , 2021. URL https://openreview. net/forum?id=0oabwyZbOu. 

- [18] C. Li, A. Krause, and M. Hutter. Robotic world model: A neural network simulator for robust policy optimization in robotics. _arXiv preprint arXiv:2501.10100_ , 2025. 

- [19] P. Fung, Y. Bachrach, A. Celikyilmaz, K. Chaudhuri, D. Chen, W. Chung, E. Dupoux, H. Gong, H. J´egou, A. Lazaric, et al. Embodied ai agents: Modeling the world. _arXiv preprint arXiv:2506.22355_ , 2025. 

- [20] T. M. Moerland, J. Broekens, A. Plaat, C. M. Jonker, et al. Model-based reinforcement learning: A survey. _Foundations and Trends® in Machine Learning_ , 16(1):1–118, 2023. 

- [21] M. P. Deisenroth and C. E. Rasmussen. Pilco: a model-based and data-efficient approach to policy search. In _Proceedings of the 28th International Conference on International Conference on Machine Learning_ , ICML’11, page 465–472, Madison, WI, USA, 2011. Omnipress. ISBN 9781450306195. 

- [22] D. Ha and J. Schmidhuber. Recurrent world models facilitate policy evolution. In S. Bengio, H. Wallach, H. Larochelle, K. Grauman, N. Cesa-Bianchi, and R. Garnett, editors, _Advances in Neural Information Processing Systems_ , volume 31. Curran Associates, Inc., 2018. URL https://proceedings.neurips.cc/paper ~~f~~ iles/paper/2018/file/ 2de5d16682c3c35007e4e92982f1a2ba-Paper.pdf. 

- [23] J. Richens, T. Everitt, and D. Abel. General agents need world models. In _Forty-second International Conference on Machine Learning_ , 2025. 

- [24] C. Chen, Y.-F. Wu, J. Yoon, and S. Ahn. Transdreamer: Reinforcement learning with transformer world models. _arXiv preprint arXiv:2202.09481_ , 2022. 

- [25] A. Dedieu, J. Ortiz, X. Lou, C. Wendelken, J. S. Guntupalli, W. Lehrach, M. Lazaro-Gredilla, and K. P. Murphy. Improving transformer world models for data-efficient RL. In _Fortysecond International Conference on Machine Learning_ , 2025. URL https://openreview. net/forum?id=IajCvMJw41. 

- [26] V. Micheli, E. Alonso, and F. Fleuret. Transformers are sample-efficient world models. In _The Eleventh International Conference on Learning Representations_ , 2023. URL https:// openreview.net/forum?id=vhFu1Acb0xb. 

- [27] V. Micheli, E. Alonso, and F. Fleuret. Efficient world models with context-aware tokenization. In _Forty-first International Conference on Machine Learning_ , 2024. URL https: //openreview.net/forum?id=BiWIERWBFX. 

10 

- [28] W. Zhang, G. Wang, J. Sun, Y. Yuan, and G. Huang. Storm: Efficient stochastic transformer based world models for reinforcement learning. _Advances in Neural Information Processing Systems_ , 36:27147–27166, 2023. 

- [29] M. Burchi and R. Timofte. Learning transformer-based world models with contrastive predictive coding. In _The Thirteenth International Conference on Learning Representations_ , 2025. URL https://openreview.net/forum?id=YK9G4Htdew. 

- [30] W. Wang, I. Dusparic, Y. Shi, K. Zhang, and V. Cahill. Drama: Mamba-enabled modelbased reinforcement learning is sample and parameter efficient. In _The Thirteenth International Conference on Learning Representations_ , 2025. URL https://openreview.net/forum?id= 7XIkRgYjK3. 

- [31] Z. Wang, Y. Deng, J. Long, and Y. Zhang. Parallelizing Model-based Reinforcement Learning Over the Sequence Length. In _The Thirty-eighth Annual Conference on Neural Information Processing Systems_ , Nov. 2024. 

- [32] H. Lai, J. Cao, J. Xu, H. Wu, Y. Lin, T. Kong, Y. Yu, and W. Zhang. World model-based perception for visual legged locomotion. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11531–11537. IEEE, 2025. 

- [33] B. Zhang, R. Wang, W. Xiao, W. Zhang, J. Sun, G. Huang, J. Chen, and G. Wang. Dymodreamer: World modeling with dynamic modulation. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. URL https://openreview.net/forum?id= SYKwGnik3w. 

- [34] C. Li, A. Krause, and M. Hutter. Offline robotic world model: Learning robotic policies without a physics simulator. _arXiv preprint arXiv:2504.16680_ , 2025. 

- [35] J. Yamada, M. Rigter, J. Collins, and I. Posner. TWIST: Teacher-Student World Model Distillation for Efficient Sim-to-Real Transfer, Nov. 2023. 

- [36] H. Zheng, Y. Cheng, H. Liu, L. Ye, and H. Liu. Huwo: Building physical interaction world models for humanoid robot locomotion. In _ICLR 2025 Workshop on World Models: Understanding, Modelling and Scaling_ , 2025. URL https://openreview.net/forum?id= AjbabLIbrd. 

- [37] S. Ferraro, P. Mazzaglia, T. Verbelen, and B. Dhoedt. Focus: object-centric world models for robotic manipulation. _Frontiers in Neurorobotics_ , 19:1585386, 2025. 

- [38] T. Bi and R. D’Andrea. Sample-efficient learning to solve a real-world labyrinth game using data-augmented model-based reinforcement learning. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 7455–7460. IEEE, 2024. 

- [39] W. Huang, J. Ji, B. Zhang, C. Xia, and Y. Yang. Safedreamer: Safe reinforcement learning with world models. In _The Twelfth International Conference on Learning Representations_ , 2024. URL https://openreview.net/forum?id=tsE5HLYtYg. 

- [40] R. Sekar, O. Rybkin, K. Daniilidis, P. Abbeel, D. Hafner, and D. Pathak. Planning to explore via self-supervised world models. In _International conference on machine learning_ , pages 8583–8592. PMLR, 2020. 

- [41] T. Qiao, H. Williams, D. Valencia, and B. MacDonald. Bounded exploration with world model uncertainty in soft actor-critic reinforcement learning algorithm. _arXiv preprint arXiv:2412.06139_ , 2024. 

- [42] G. Zollicoffer, K. Eaton, J. C. Balloch, J. Kim, W. Zhou, R. Wright, and M. Riedl. Novelty detection in reinforcement learning with world models. In _Forty-second International Conference on Machine Learning_ , 2025. URL https://openreview.net/forum?id=xtlixzbcfV. 

11 

- [43] N. Hansen, H. Su, and X. Wang. Td-mpc2: Scalable, robust world models for continuous control. In _International Conference on Learning Representations_ , 2024. 

- [44] I. Georgiev, V. Giridhar, N. Hansen, and A. Garg. PWM: Policy learning with multi-task world models. In _The Thirteenth International Conference on Learning Representations_ , 2025. URL https://openreview.net/forum?id=hOELrZfg0J. 

- [45] Y. Zhao, A. Scannell, W. Zhao, Y. Hou, T. Cui, L. Chen, D. B¨uchler, A. Solin, J. Kannala, and J. Pajarinen. Efficient reinforcement learning by guiding generalist world models with non-curated data. _arXiv preprint arXiv:2502.19544_ , 2025. 

- [46] L. Zhang, M. Kan, S. Shan, and X. Chen. PreLAR: World Model Pre-training with Learnable Action Representation. In A. Leonardis, E. Ricci, S. Roth, O. Russakovsky, T. Sattler, and G. Varol, editors, _Computer Vision – ECCV 2024_ , volume 15081, pages 185–201. Springer Nature Switzerland, Cham, 2025. ISBN 978-3-031-73336-9 978-3-031-73337-6. doi:10.1007/ 978-3-031-73337-6 ~~1~~ 1. 

- [47] Y. Feng, N. Hansen, Z. Xiong, C. Rajagopalan, and X. Wang. Finetuning offline world models in the real world. In _Proceedings of the 7th Conference on Robot Learning (CoRL)_ , 2023. 

- [48] M. Shafiee, G. Bellegarda, and A. Ijspeert. Manyquadrupeds: Learning a single locomotion policy for diverse quadruped robots. _arXiv preprint arXiv:2310.10486_ , 2023. 

- [49] G. Feng, H. Zhang, Z. Li, X. B. Peng, B. Basireddy, L. Yue, Z. Song, L. Yang, Y. Liu, K. Sreenath, et al. Genloco: Generalized locomotion controllers for quadrupedal robots. In _Conference on Robot Learning_ , pages 1893–1903. PMLR, 2023. 

- [50] S. Wu, M. H. Danesh, S. Li, H. Yurchyk, A. Abyaneh, A. El Houssaini, D. Meger, and H.C. Lin. Vocaloco: Viability-optimized cost-aware adaptive locomotion. _IEEE Robotics and Automation Letters_ , 11(2):1146–1153, 2025. 

- [51] H. Ma, J. Wu, N. Feng, C. Xiao, D. Li, J. Hao, J. Wang, and M. Long. Harmonydream: Task harmonization inside world models. In _International Conference on Machine Learning_ , 2024. 

- [52] S. Lee, D. Cho, J. Park, and H. J. Kim. Cqm: Curriculum reinforcement learning with a quantized world model. _Advances in Neural Information Processing Systems_ , 36:78824–78845, 2023. 

- [53] T. Wang, R. Liao, J. Ba, and S. Fidler. Nervenet: Learning structured policy with graph neural networks. In _International Conference on Learning Representations_ , 2018. URL https: //openreview.net/forum?id=S1sqHMZCb. 

- [54] J. Whitman, M. Travers, and H. Choset. Learning modular robot control policies. _IEEE Transactions on Robotics_ , 39(5):4095–4113, 2023. 

- [55] W. Huang, I. Mordatch, and D. Pathak. One policy to control them all: Shared modular policies for agent-agnostic control. In _International Conference on Machine Learning_ , pages 4455–4464. PMLR, 2020. 

- [56] F. Xie, S. Wei, Y. Song, Y. Yue, and L. Gan. Morphological-symmetry-equivariant heterogeneous graph neural network for robotic dynamics learning. In N. Ozay, L. Balzano, D. Panagou, and A. Abate, editors, _Proceedings of the 7th Annual Learning for Dynamics &amp; Control Conference_ , volume 283 of _Proceedings of Machine Learning Research_ , pages 1392–1405. PMLR, 04–06 Jun 2025. URL https://proceedings.mlr.press/v283/ xie25a.html. 

- [57] S. Wei, X. Chen, F. Xie, G. E. Katz, Z. Gan, and L. Gan. Ms-ppo: Morphological-symmetryequivariant policy for legged robot locomotion. _arXiv preprint arXiv:2512.00727_ , 2025. 

12 

- [58] D. Butterfield, S. S. Garimella, N.-J. Cheng, and L. Gan. Mi-hgnn: Morphology-informed heterogeneous graph neural network for legged robot contact perception. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 10110–10116. IEEE, 2025. 

- [59] A. Gupta, L. Fan, S. Ganguli, and L. Fei-Fei. Metamorph: Learning universal controllers with transformers. In _International Conference on Learning Representations_ , 2022. URL https://openreview.net/forum?id=Opmqtk ~~G~~ vYL. 

- [60] N. Bohlinger, G. Czechmanowski, M. P. Krupka, P. Kicki, K. Walas, J. Peters, and D. Tateo. One policy to run them all: an end-to-end learning approach to multi-embodiment locomotion. In P. Agrawal, O. Kroemer, and W. Burgard, editors, _Proceedings of The 8th Conference on Robot Learning_ , volume 270 of _Proceedings of Machine Learning Research_ , pages 3356–3378. PMLR, 06–09 Nov 2025. URL https://proceedings.mlr.press/v270/bohlinger25a. html. 

- [61] W. Xi, Z. Cao, C. Ming, J. Zheng, and G. Zhou. Unilegs: Universal multi-legged robot control through morphology-agnostic policy distillation. _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2025. 

- [62] B. Trabucco, M. Phielipp, and G. Berseth. Anymorph: Learning transferable polices by inferring agent morphology. In _International Conference on Machine Learning_ , pages 21677– 21691. PMLR, 2022. 

- [63] C. Sferrazza, D.-M. Huang, F. Liu, J. Lee, and P. Abbeel. Body transformer: Leveraging robot embodiment for policy learning. In _8th Annual Conference on Robot Learning_ , 2024. URL https://openreview.net/forum?id=Oce2215aJE. 

- [64] B. Ai, L. Dai, N. Bohlinger, D. Li, T. Mu, Z. Wu, K. Fay, H. I. Christensen, J. Peters, and H. Su. Towards embodiment scaling laws in robot locomotion. In J. Lim, S. Song, and H.-W. Park, editors, _Proceedings of The 9th Conference on Robot Learning_ , volume 305 of _Proceedings of Machine Learning Research_ , pages 3483–3515. PMLR, 27–30 Sep 2025. URL https: //proceedings.mlr.press/v305/ai25a.html. 

- [65] D. Pathak, C. Lu, T. Darrell, P. Isola, and A. A. Efros. Learning to control self-assembling morphologies: a study of generalization via modularity. _Advances in Neural Information Processing Systems_ , 32, 2019. 

- [66] T. Wang, D. Bhatt, X. Wang, and N. Atanasov. Cross-embodiment robot manipulation skill transfer using latent space alignment. _CoRR_ , abs/2406.01968, 2024. URL https://doi.org/ 10.48550/arXiv.2406.01968. 

- [67] J. Jang, S. Ye, Z. Lin, J. Xiang, J. Bjorck, Y. Fang, F. Hu, S. Huang, K. Kundalia, Y.-C. Lin, et al. Dreamgen: Unlocking generalization in robot learning through neural trajectories. _arXiv e-prints_ , pages arXiv–2505, 2025. 

- [68] H. Zhang, K. Y. Ma, M. Z. Shou, W. Lin, and Y. Wu. Cross-embodiment dexterous hand articulation generation via morphology-aware learning. _arXiv preprint arXiv:2510.06068_ , 2025. 

- [69] P. Mishra, A. H. Raj, X. Xiao, and D. Manocha. Mcarl: Morphology-control-aware reinforcement learning for generalizable quadrupedal locomotion. _arXiv preprint arXiv:2505.18418_ , 2025. 

- [70] J. Hwangbo, J. Lee, A. Dosovitskiy, D. Bellicoso, V. Tsounis, V. Koltun, and M. Hutter. Learning agile and dynamic motor skills for legged robots. _Science Robotics_ , 4(26):eaau5872, 2019. 

- [71] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

13 

## **A Environment Details & Reward Structure** 

In this section, we provide the detailed specification of the environment, reward structures, and randomization parameters used to train QWM. 

To demonstrate the robustness of our architecture and ensure fair comparison against baselines, we purposefully avoided extensive hyperparameter tuning. Instead, we adopted the default reward terms, weights, and randomization ranges provided by the official NVIDIA Isaac Lab repository [5] for each respective robot asset. By relying on these standard, community-vetted configurations, we show that QWM can generalize across morphologies without requiring the reward landscape to be engineered specifically for our latent representation. 

### **A.1 Reward Functions** 

The reward definitions vary between the standard quadruped families (ANYmal and Unitree series) and the Boston Dynamics Spot, reflecting the different control strategies often employed for industrial versus agile platforms. We denote the robot state available for reward computation by linear velocity **v** _∈_ R<sup>3</sup> , angular velocity **_ω_** _∈_ R<sup>3</sup> , joint positions **q** _∈_ R<sup>12</sup> , joint velocities **q** ˙ _∈_ R<sup>12</sup> , joint torques **_τ_** _∈_ R<sup>12</sup> , and the projected gravity vector **g** _proj ∈_ R<sup>3</sup> . The agent’s action (target joint positions) is denoted **a** _t ∈_ R<sup>12</sup> . The commanded velocities are **v** _xy_<sup>_cmd_</sup> _∈_ R<sup>2</sup> and _ωz_<sup>_cmd_</sup> _∈_ R (or heading commands where applicable). 

The policy observation space (R<sup>48</sup> ) consists of **v** , **_ω_** , **g** _proj_ , **v**<sup>_cmd_</sup> , **q** _−_ **q** _default_ , **q** ˙ , and the previous actions **a** _t−_ 1. 

For the ANYmal (B, C, D) and Unitree (A1, Go1, Go2, B2) families, we utilize the standard “Flat Terrain” reward structure common in robotic learning [5]. As shown in Table 3, the objective is primarily velocity tracking with auxiliary penalties to encourage energy efficiency and smoothness. We employ the squared exponential kernel _e_<sup>_−∥x∥_2</sup><sup>_/σ_2</sup> for tracking terms. 

Table 3: Standard Reward Functions (ANYmal & Unitree Families) 

|**Tracking Term**|**Equation**|**Penalty Term**|**Equation**|
|---|---|---|---|
|Lin. Vel. Track (XY)<br>Ang. Vel. Track (Z)|_e_<sup>_−∥_</sup><sup>**v**</sup><sup>_xy−_</sup><sup>**v**</sup><sup>_cmd_</sup><br>_xy_<br>_∥_<sup>2</sup>_/σ_<sup>2</sup><br>_v_<br>_e_<sup>_−_(</sup><sup>_ωz−ωcmd_</sup><br>_z_<br>)<sup>2</sup>_/σ_<sup>2</sup><br>_ω_|Lin. Vel. Z<br>Ang. Vel. XY|_−v_<sup>2</sup><br>_z_<br>_−∥_**_ω_**_xy∥_<sup>2</sup><br>|
|Feet Air Time|�(_tair −_0_._5)_·_I_landed_|Flat Orientation<br>Torque<br>Joint Acc.<br>Action Rate<br>Contacts<sup>*</sup>|_−∥_**g**_proj,xy∥_<sup>2</sup><br>_−∥_**_τ_**_∥_<sup>2</sup><br>_−∥_¨**q**_∥_<sup>2</sup><br>_−∥_**a**_t −_**a**_t−_1_∥_<sup>2</sup><br>_−_I(_∥_**F**_c∥>_1_._0)|


*Enabled for the ANYmal series and disabled for the Unitree series. 

The Boston Dynamics Spot utilizes a distinct reward setup derived from its specific configuration in Isaac Lab. Unlike the standard group, this configuration includes explicit “gait enforcement” terms (Table 4) to produce a specific trotting style, along with stricter kinematic constraints (e.g., foot clearance). 

### **A.2 Reward Weights** 

Table 5 and Table 6 detail the coefficients used for scalarization. We preserve the heterogeneous weights from the optimized single-robot configurations rather than normalizing them manually. 

### **A.3 Domain Randomization** 

To ensure sim-to-real transfer, we apply extensive domain randomization. 

14 

Table 4: Spot-Specific Reward Functions 

|**Functional Term**|**Equation**|**Penalty Term**|**Equation**|
|---|---|---|---|
|Base Lin. Vel (Ramp)|_m · e_<sup>_−∥_</sup><sup>**v**</sup><sup>_xy−_</sup><sup>**v**</sup><sup>_cmd_</sup><br>_xy_<br>_∥/σv_|Foot Slip|_−_<sup>�</sup>_∥_**v**_f,xy∥·_I_contact_|
|_where m_=|1 + 0_._5(_∥_**v**<sup>_cmd_</sup><br>_xy _<sup>_∥−_1)</sup>+|Base Motion|_−_(0_._8_v_<sup>2</sup><br>_z_ <sup>+ 0</sup><sup>_._2</sup><sup>_∥_</sup><sup>**_ω_**</sup>_xy_<sup>_∥_</sup>1<sup>)</sup>|
|Base Ang. Vel (Abs)|_e_<sup>_−|ωz−ωcmd_</sup><br>_z_<br>_|/σω_|Base Orientation|_−∥_**g**_proj,xy∥_|
|Foot Clearance|_e_<sup>_−_�(</sup><sup>_hf −_0</sup><sup>_._1)2 tanh(2</sup><sup>_vf_ )</sup>|Act. Smoothness|_−∥_**a**_t −_**a**_t−_1_∥_|
|Gait Enforcement<br>_where ri_ =|_rsync · rasync_<br> _e_<sup>_−_(∆</sup><sup>_t_2</sup><br>_air_<sup>+∆</sup><sup>_t_2</sup><br>_cont_<sup>)</sup><sup>_/σ_</sup>|Air Time Var.<br>Joint Pos/Vel|_−_(Var(_tair_) +Var(_tcont_))<br>_−∥_**q**_−_**q**0_∥, −∥_˙**q**_∥_|
|||Contacts|_−_I(_∥_**F**_c∥>_1_._0)|


Table 5: Reward Weights for ANYmal and Unitree Robots 

|**Reward Term**|**ANYmal-D**|**ANYmal-C**|**ANYmal-B**|**Unitree A1**|**Unitree Go1**|**Unitree Go2**|**Unitree B2**|
|---|---|---|---|---|---|---|---|
|Lin. Vel. Tracking (XY)|1.0|1.0|1.0|1.5|1.5|1.5|1.0|
|Ang. Vel. Tracking (Z)|0.5|0.5|0.5|0.75|0.75|0.75|0.75|
|Feet Air Time|0.5|0.5|0.5|0.25|0.25|0.25|0.5|
|Lin. Vel. Z (_L_<sup>2</sup>)|-2.0|-2.0|-2.0|-2.0|-2.0|-2.0|-2.0|
|Ang. Vel. XY (_L_<sup>2</sup>)|-0.05|-0.05|-0.05|-0.05|-0.05|-0.05|-0.05|
|Flat Orientation (_L_<sup>2</sup>)|-5.0|-5.0|-5.0|-2.5|-2.5|-2.5|-5.0|
|Joint Torques (_L_<sup>2</sup>)|-2.5e-5|-2.5e-5|-2.5e-5|-2.0e-4|-2.0e-4|-2.0e-4|-2.0e-5|
|Joint Acc. (_L_<sup>2</sup>)<br>|-2.5e-7|-2.5e-7|-2.5e-7|-2.5e-7|-2.5e-7|-2.5e-7|-2.5e-7|
|Action Rate (_L_<sup>2</sup>)|-0.01|-0.01|-0.01|-0.01|-0.01|-0.01|-0.01|
|Undesired Contacts|-1.0|-1.0|-1.0|-|-|-|-|


### **A.3.1 Physics & Observation Randomization** 

We apply standard randomization to surface friction and observation noise (Table 7). 

### **A.3.2 Morphology Randomization** 

We randomize physical properties during training. We define two randomization groups, Large (ANYmal, B2, Spot) and Small (A1, Go1, Go2), to ensure that mass perturbations are relative to the robot’s size. 

### **A.3.3 Reset Randomization & Task Commands** 

We utilize different initialization strategies based on robot sensitivity (Table 9). While larger robots utilize joint scaling, smaller Unitree platforms are initialized at nominal joint positions to ensure stability. The velocity command ranges (Table 10) are uniform across all robots in the heterogeneous setup. 

15 

Table 6: Reward Weights for Boston Dynamics Spot 

|**Reward Term**|**Weight**|**Reward Term**|**Weight**|
|---|---|---|---|
|Gait Reward|10.0|Base Motion Penalty (_vz,_**_ω_**_xy_)|-2.0|
|Base Linear Vel (Ramp)|5.0|Base Orientation Penalty|-3.0|
|Base Angular Vel|5.0|Action Smoothness|-1.0|
|Air Time Reward|5.0|Air Time Variance|-1.0|
|Foot Clearance|0.5|Foot Slip|-0.5|
|Joint Position Penalty|-0.7|Joint Acceleration|-1.0e-4|
|Joint Velocity Penalty|-0.01|Joint Torques|-5.0e-4|
|Undesired Contacts|-1.0|||


Table 7: Physics and Observation Randomization Parameters 

|**Parameter**|**Value / Distribution**|
|---|---|
|Static Friction|_U_(0_._8_,_0_._8)(Default)|
|Dynamic Friction|_U_(0_._6_,_0_._6)(Default)|
|External Disturbance|_vpush ∼U_(_−_0_._5_,_0_._5)m/s (Every 10 to 15s)|
|Control Latency|20ms (Simulation_dt_= 0_._005s, Decimation=4)|
|_Observation Noise_|_Additive Uniform Distribution_<br>|
|Linear Velocity|_U_(_−_0_._1_,_0_._1)m/s|
|Angular Velocity|_U_(_−_0_._2_,_0_._2)rad/s|
|Projected Gravity|_U_(_−_0_._05_,_0_._05)|
|Joint Positions|_U_(_−_0_._01_,_0_._01)rad|
|Joint Velocities|_U_(_−_1_._5_,_1_._5)rad/s|


Table 8: Morphology Randomization Parameters 

|**Parameter**|**Distribution / Range**|
|---|---|
|Mass (Large Robots)|Base_±_5_._0kg|
|Mass (Small Robots)|Base+[_−_1_._0_,_3_._0]kg|
|Center of Mass (Base)|_±_5cm (X, Y),_±_1cm (Z)|


Table 9: Reset Randomization 

|**State**|**Initialization**|
|---|---|
|Base Position|Offset_±_0_._5m (X,Y)|
|Base Yaw|_U_(_−π, π_)|
|Base Velocity (Lin/Ang)|_U_(_−_0_._5_,_0_._5)(Zero for Small Unitrees)<br>|
|Joint Pos (ANYmal, B2)|Nominal_×U_(0_._8_,_1_._2)|
|Joint Pos (Small Unitree)|Nominal (Fixed)<br>|
|Joint Pos (Spot)|Nominal+_U_(_−_0_._05_,_0_._05)rad|


Table 10: Velocity Command Ranges 

|**Robot Group**|**v**_x_(m/s)|**v**_y_ (m/s)|**_ω_**_z_ (rad/s)|
|---|---|---|---|
|All Robots|[_−_1_._0_,_1_._0]|[_−_1_._0_,_1_._0]|[_−_1_._0_,_1_._0]|


16 

## **B Heterogeneous Simulation Infrastructure** 

We utilize NVIDIA Isaac Lab [5], built upon Isaac Sim [4], as our simulation backbone. While Isaac Lab offers massive parallelism via GPU-accelerated PhysX, its default vectorization paradigm is designed for _homogeneous_ setups, spawning thousands of identical clones of a single robot asset. This standard setup is insufficient for training a generalizable agent across multiple robots _simultaneously_ , as it typically restricts the training loop to a single morphology per run. 

To overcome this limitation, we developed a heterogeneous environment on top of Isaac Lab, Hetero-Isaac. 

Unlike standard vectorization, Hetero-Isaac manages a heterogeneous batch where the robot type is indexed per environment ID, allowing the replay buffer to collect a mixed distribution of morphologies in a single forward pass. By managing unique robot description file paths and physics tensors, we construct a diverse morphology cohort including the ANYmal (B, C, D), Unitree (Go1, Go2, A1, B2), and Boston Dynamics Spot (Fig. 1). Importantly, this cohort is not merely a collection of scaled variants, but it captures fundamental kinematic shifts. The robots span distinct joint topologies, ranging from the “X-configuration” of the ANYmals (where knees bend inwards towards the chassis) to the standard mammalian “dog-like” configuration of the Spot and Unitree series. Furthermore, the hip-to-foot offsets and link length ratios vary non-linearly across the fleet. This structural diversity prevents the agent from relying on a single gait geometry, forcing the WM to capture the distinct underlying dynamics of each kinematic chain. 

Essential to our setup, Hetero-Isaac ensures full physical fidelity by maintaining distinct collision geometries, kinematic trees, and actuator gains for each agent in parallel. Furthermore, it manages the complexity of _heterogeneous reward definitions_ . Different robots require distinct objective functions and weightings. For instance, Spot accumulates rewards on a vastly different scale ( _≈_ 350 per episode) compared to the ANYmal-D ( _≈_ 25) (see Subsec. 4.2). Hetero-Isaac exposes these diverse, unnormalized signals directly, necessitating the adaptive per-robot reward normalizer described in Subsec. 4.3. 

**Training distribution.** Throughout all experiments, Hetero-Isaac applies extensive domain randomization to expose policies to the kind of unmodeled phenomena present on real hardware, namely surface friction variation, mass perturbations, center-of-mass shifts, external push disturbances, control latency, and additive observation noise across all proprioceptive channels (full specification in App. A). Consequently, all simulation results reported in this work, encompassing training curves, zero-shot transfer, and perturbation robustness, reflect performance across a _distribution_ of physical conditions per morphology, not a single nominal setting. This randomization is what allows the learned latent dynamics ( _ht, zt_ ) to absorb residuals beyond the idealized _µ_ vector, and is a key reason QWM transfers to real hardware without fine-tuning despite the sim-to-real gap. 

17 

## **C Network Architecture Details** 

We build upon the DreamerV3 [14] backbone, introducing specific architectural modifications to handle heterogeneous morphologies. Unless otherwise specified, all dense layers are followed by LayerNorm and the SiLU activation function. 

### **C.1 Morphology-Conditioned Encoder** 

To effectively fuse the high-frequency proprioceptive data ( _ot_ ) with the static, low-frequency morphology features ( _µ_ ), we employ a dual-pathway architecture, detailed in Sec. 4. 

As seen in Subsec. C.1, we process the modalities in separate pathways before concatenation. The proprioception tower is deep (5 layers) and wide (1024 units) to extract features from the complex joint state history. Conversely, the robot description tower is shallower (2 layers) and narrower (512 units) because the input features _µ_ (ratios, normalized masses) are already semantically dense. This design prevents the static signal from being overwhelmed by the variance of the dynamic signal before they are projected into the shared latent space. 

### **Dual-Pathway Encoder** 

### **Inputs:** 

- Proprioception _ot ∈_ R<sup>48</sup> (Joint pos, vel, base vel, gravity, commands, actions) 

- Morphology _µ ∈_ R<sup>10</sup> (Normalized robot description features) 

### **1. Proprioception Tower:** 

# Wide and deep to capture high-freq dynamics x_dyn = Linear(48, 1024) -> LayerNorm -> SiLU x_dyn = Linear(1024, 1024) -> LayerNorm -> SiLU x_dyn = Linear(1024, 1024) -> LayerNorm -> SiLU x_dyn = Linear(1024, 1024) -> LayerNorm -> SiLU x_dyn = Linear(1024, 1024) -> LayerNorm -> SiLU 

**2. Morphology Tower:** 

# Shallower tower; features are already dense # Units = 0.5 * Proprio_Units x_stat = Linear(10, 512) -> LayerNorm -> SiLU x_stat = Linear(512, 512) -> LayerNorm -> SiLU 

**3. Fusion Layer:** 

concat = Concatenate([x_dyn, x_stat]) # dim: 1536 embed = Linear(1536, 1024) -> LayerNorm -> SiLU 

### **C.2 Recurrent State-Space Model (RSSM)** 

The core of the WM is the RSSM, which learns the transition dynamics _p_ ( _st_ +1 _|st, at, µ_ ). We utilize a discrete latent space (Categorical VAE) which has been shown to be more robust to world modeling errors than Gaussian equivalents. 

Crucially, as shown in Subsec. C.2, the morphology vector _µ_ is injected again at the input of the Recurrent Cell. This explicit recurrent conditioning ensures that the GRU state _ht_ does not need to memorize the robot’s physical parameters (like limb length) in its short-term memory, freeing up capacity for tracking dynamic state (like velocity and contact timing). 

18 

**RSSM Dynamics State Definitions:** • Deterministic State _ht ∈_ R<sup>512</sup> (GRU State) • Stochastic State _zt_ : 32 categorical variables, 32 classes each (32 _×_ 32 flattened to 1024) **1. Recurrent Step (Finding** _ht_ **):** # Inputs: Previous stochastic state, Action, Morphology # Note: z_{t-1} is flattened from (32, 32) -> 1024 input_rnn = Concatenate([Flatten(z_{t-1}), a_{t-1}, mu]) # Pre-processing MLP x_rnn = Linear(input_rnn, 512) -> LayerNorm -> SiLU # GRU Update h_t = GRUCell(input=x_rnn, hidden_state=h_{t-1}) **2. Posterior Estimation (Representation Model):** # Fuses history (h_t) with current observation embedding input_post = Concatenate([h_t, embed]) x_post = Linear(input_post, 512) -> LayerNorm -> SiLU logits = Linear(512, 32 * 32) z_t_post ˜ OneHotCategorical(logits) # Used for training **3. Prior Estimation (Transition Predictor):** # Predicts state purely from history (for imagination) x_prior = Linear(h_t, 512) -> LayerNorm -> SiLU logits = Linear(512, 32 * 32) z_t_prior ˜ OneHotCategorical(logits) # Used for planning 

### **C.3 Policy and Critic Heads** 

The Actor and Critic networks operate on the concatenated state feature _featt_ = [ _ht,_ flatten( _zt_ )]. 

The Critic utilizes Symlog distribution learning. Instead of regressing a single scalar value (which is unstable when rewards vary by orders of magnitude, as seen in Subsec. 4.3), the network predicts a categorical distribution over 255 bins. This allows the critic to model the multi-modal return distributions common in multi-task learning. 

The Actor outputs a Gaussian distribution. To prevent premature convergence, the standard deviation is learned but bounded between [0 _._ 1 _,_ 2 _._ 0]. 

19 

### **Actor & Critic** 

**Input:** _featt_ = Concatenate([ _ht,_ Flatten( _zt_ )]) (dim: 512 + 1024 = 1536) **1. Actor (Policy):** 

x = Linear(1536, 512) -> LayerNorm -> SiLU x = Linear(512, 512) -> LayerNorm -> SiLU x = Linear(512, 512) -> LayerNorm -> SiLU # Mean head mean = Linear(512, 12) # Std head (Learned, constrained) raw_std = Linear(512, 12) std = Softplus(raw_std) + 0.1 std = clamp(std, min=0.1, max=2.0) action ˜ Normal(mean, std) 

**2. Critic (Value Function):** x = Linear(1536, 512) -> LayerNorm -> SiLU x = Linear(512, 512) -> LayerNorm -> SiLU x = Linear(512, 512) -> LayerNorm -> SiLU # Symlog Discrete Output (TwoHot Encoding) logits = Linear(512, 255) value_dist = Softmax(logits) # Expected value is calculated via weighted sum of bin centers 

### **C.4 Reward Head** 

The reward predictor is structurally identical to the Critic, utilizing the same Symlog two-hot discretization. However, it is deeper (4 layers) than the policy heads. This increased depth is necessary because the reward function in locomotion is often a highly non-linear combination of the state (e.g., precise velocity tracking combined with sharp boolean penalties for collisions). 

### **Reward Predictor** 

**Input:** _featt_ (dim: 1536) x = Linear(1536, 512) -> LayerNorm -> SiLU x = Linear(512, 512) -> LayerNorm -> SiLU x = Linear(512, 512) -> LayerNorm -> SiLU x = Linear(512, 512) -> LayerNorm -> SiLU # Extra depth logits = Linear(512, 255) reward_dist = Softmax(logits) 

### **C.5 Continuation Head** 

The Continuation Head predicts the probability ˆ _ct ∈_ [0 _,_ 1] of the episode continuing at the next step (equivalent to 1 _−_ probability of termination). This allows the agent to “hallucinate” termination events, such as the robot falling over or exceeding joint limits, during latent imagination. 

Unlike the Reward Head, the Continuation Head is relatively shallow (2 layers). We found that the termination boundary (alive vs. dead) is generally sharper and easier to learn than the complex reward landscape, requiring less network depth. 

20 

### **Continuation Predictor** 

**Input:** _featt_ = [ _ht, zt_ ] (dim: 1536) # Layer 1 x = Linear(1536, 512) -> LayerNorm -> SiLU # Layer 2 x = Linear(512, 512) -> LayerNorm -> SiLU # Binary Output (Bernoulli Distribution) logit = Linear(512, 1) p_alive = Sigmoid(logit) 

21 

## **D Morphological Diversity Analysis** 

To characterize how each robot relates to the rest of the cohort on individual physical dimensions, we compute _per-feature leave-one-out (LOO) z-scores_ . We deliberately avoid collapsing this multidimensional physical heterogeneity into a single scalar distance metric. Different features (limb lengths, log-masses, torque densities, stance aspect ratios, discrete topology flags) affect locomotion dynamics non-uniformly, and any scalar summary, whether cosine similarity or Euclidean distance in normalized space, implicitly assumes a feature isotropy that does not hold in physical reality. Instead, we characterize each held-out robot by its full per-feature deviation profile, which retains the directional and magnitude information needed to interpret the zero-shot transfer results. For each robot _r_ and continuous feature _f_ , the LOO _z_ -score is: 


where _µ_ ˆ _−r,f_ and ˆ _σ−r,f_ are the mean and standard deviation of feature _f_ computed over the remaining seven robots. Crucially, this seven-robot reference set identically matches the training cohort used when evaluating the held-out robot _r_ in our zero-shot experiments (Subsec. 5.3). A large _|z|_ on a given feature indicates that the robot deviates substantially from what the rest of the cohort represents on that physical dimension. The discrete topology flag _k_ cfg is excluded from this analysis as its binary nature makes a Gaussian deviation measure inappropriate. 

Fig. 4 visualizes the signed _z_ -scores. Each cell shows the raw value and its deviation in standarddeviation units. The color encodes _|z|_ , saturating at 2 _._ 5 _σ_ . Table 11 summarizes the deviation statistics per robot. 

Table 11: Per-robot LOO _z_ -score summary over 9 continuous features. 

|**Robot**|**Mean**_|z|_|**Max**_|z|_|**Worst feature**|**#**_|z| >_1_._5|
|---|---|---|---|---|
|ANYmal-B|0.83|1.79|_m_trunk_/M_tot|3/9|
|ANYmal-C|0.90|1.61|_µ_act|1/9|
|ANYmal-D|1.10|1.56|_µ_act<br>|1/9|
|Spot|0.77|2.30|_l_stance_/w_stance|1/9|
|Unitree A1|1.17|1.61|_l_thigh|4/9|
|Unitree Go1|1.09|1.49|_m_trunk_/M_tot|0/9|
|Unitree Go2|0.94|1.30|_l_hip|0/9|
|Unitree B2|1.20|2.29|_µ_act|2/9|


Three patterns are relevant to the zero-shot generalization results in Subsec. 5.3. 

**Unitree Go1.** No feature exceeds 1 _._ 5 _σ_ (max _|z|_ = 1 _._ 49 on trunk mass ratio). The Go1 is the most uniformly in-distribution robot in the cohort on all physical axes simultaneously. This directly explains its strong zero-shot performance. 

**ANYmal-D.** One feature exceeds 1 _._ 5 _σ_ (torque capacity at _z_ = _−_ 1 _._ 6), with all others below 1 _._ 3 _σ_ . Like the Go1, the ANYmal-D sits comfortably within the support of the training distribution across the full feature vector, explaining its successful zero-shot transfer. 

**Unitree B2.** The B2 shows the most broadly elevated deviation profile. Torque capacity reaches _z_ = +2 _._ 29 (the only feature crossing 2 _σ_ in the cohort aside from Spot’s aspect ratio), log-mass reaches _z_ = +1 _._ 92, stance length _z_ = +1 _._ 37, and hip offset _z_ = +1 _._ 19. Critically, all elevated deviations push in the same direction, larger, heavier, and stronger, so no training robot simultaneously combines the B2’s inertial regime, actuator capacity, and limb geometry. This is a _combinatorial_ gap. Individually each deviation is bounded, but jointly the configuration is unrepresented, which is why a scalar distance metric is insufficient to characterize B2’s difficulty. A robot could match B2’s scalar distance by deviating on only one or two features and would pose a qualitatively easier problem. That QWM transfers to B2 zero-shot, while a model-free controller given the identical _µ_ collapses (Subsec. 5.3), indicates the learned dynamics combine mild extrapolation on mass and 

22 


Figure 4: Per-feature LOO _z_ -scores for the robot cohort. Each cell reports the raw physical value (top) and its signed deviation from the LOO cohort distribution in standard-deviation units (bottom). Color intensity encodes _|z|_ , saturating at 2 _._ 5 _σ_ . Features are grouped by category (Dynamics, Kinematics, Geometry). The discrete topology flag _k_ cfg is excluded. 

torque capacity with interpolation along the remaining physical axes, rather than relying on a single nearest neighbor. 

**Boston Dynamics Spot.** Spot’s deviation is narrow and concentrated, with aspect ratio reaching _z_ = +2 _._ 30 (driven by its uniquely narrow stance, _l/w_ = 5 _._ 42), while all other features remain below 1 _._ 13 _σ_ . As a _training_ robot, this one-dimensional geometric outlier status is handled well, since the WM only needs to adapt along a single physical axis to accommodate Spot’s dynamics. 

23 

## **E Ablation Study** 

In this section, we rigorously evaluate the individual contributions of the proposed components in the QWM framework. To validate our architectural design choices, specifically the Physical Morphology Encoder (PME), the Adaptive Reward Normalization (ARN), and the specific injection points of the morphology vector, we trained distinct variations of our model on the full heterogeneous robot cohort. 

We compare the full QWM framework against the following configurations to isolate the impact of (1) explicit morphology information, (2) reward balancing, and (3) the location of conditioning within the WM. 

1. **QWM (Full Method).** The proposed framework as described in Sec. 4. The model utilizes the PME to generate _µ_ , applies ARN to normalize learning signals, and conditions both the dual-pathway encoder and the RSSM dynamics on _µ_ . 

2. **w/o PME (Implicit Identification).** We remove the explicit morphology conditioning entirely. The model receives no static physical parameters ( _µ_ is removed). The agent must implicitly infer the robot’s morphology solely from the history of proprioceptive observations ( _ot_ ) stored in the recurrent state _ht_ . This effectively tests the limitations of implicit system identification. Note that the model still has the ARN module, making it different from the DreamerV3 backbone. 

3. **w/o ARN (Raw Rewards).** We remove the Adaptive Reward Normalization. The WM and policy are trained on the raw, unnormalized reward signals provided by the heterogeneous environments. This variant tests the hypothesis that varying reward scales across robots cause optimization instability or mode collapse. 

4. **w/o RSSM Conditioning.** We retain the PME and inject _µ_ into the encoder, but we remove the explicit injection of _µ_ into the recurrent model (Eq. 1). The transition dynamics become _ht_ = _fϕ_ ( _ht−_ 1 _, zt−_ 1 _, at−_ 1). This tests whether the recurrent state _ht_ can successfully maintain static morphological information over time without explicit re-injection at every step. 

5. **w/o Encoder Conditioning.** We retain the PME and inject _µ_ into the recurrent model, but remove the static tower from the encoder. The posterior _zt_ is inferred solely from dynamic observations _ot_ . This tests the necessity of grounding the latent representation _zt_ with static physical context. 

6. **w/o ARN & RSSM Conditioning.** A compound ablation removing both reward normalization and the explicit dynamics conditioning. This tests if reward scaling issues can be mitigated purely by the encoder’s awareness of the morphology. 

7. **w/o ARN & Encoder Conditioning.** A compound ablation removing both reward normalization and the encoder’s access to morphology. This tests if the recurrent dynamics alone can handle both the unnormalized signal and the morphology retention. 

8. **w/o PME & ARN (DreamerV3 Baseline).** We remove all proposed contributions. The model is a standard DreamerV3 [14] trained on the heterogeneous batch. It relies on raw rewards and implicit system identification. This serves as the lower-bound baseline to demonstrate the total value added by the QWM framework. 

Fig. 5 demonstrates a thorough comparison of learning performance across all ablated configurations. The results provide empirical evidence for the necessity of each component in the QWM framework. 

First, the most striking observation is the absolute necessity of Adaptive Reward Normalization (ARN) when training across a heterogeneous fleet. All configurations lacking ARN, specifically **w/o ARN** , **w/o ARN & RSSM conditioning** , and **w/o ARN & encoder conditioning** , fail entirely to learn. These variants remain flat near zero reward and minimal episode lengths throughout the 36 

24 


Figure 5: Ablation study on the heterogeneous cohort. We compare QWM against architectural ablations on morphology encoding (PME), reward normalization (ARN), and conditioning locations. Shaded regions denote standard deviation across 5 seeds. **Key findings.** (1) QWM achieves the fastest convergence and highest stable asymptotic performance. (2) Removing encoder conditioning allows initial learning but leads to a catastrophic late-stage collapse. (3) Removing explicit morphology (PME) maximizes episode length but plateaus at a suboptimal reward, showing explicit morphology is needed for refined gaits. (4) Removing ARN prevents learning, leaving a flatline near zero reward. 

million environment steps. This confirms the hypothesis that unnormalized, disparate reward scales across different physical embodiments cause severe optimization instability, effectively preventing the world model from establishing a useful foundation. 

Second, isolating the injection points for morphological conditioning reveals distinct failure modes when either pathway is omitted. Removing explicit morphology from the static tower of the encoder ( **w/o encoder conditioning** ) allows the model to learn initially, reaching competitive performance by 14 million steps. However, it subsequently suffers a catastrophic collapse, losing significant reward and episode length. This indicates that without grounding the latent posterior in static physical context, the representations become fundamentally unstable over extended training horizons. Conversely, removing explicit conditioning from the recurrent dynamics ( **w/o RSSM conditioning** ) heavily degrades sample efficiency and introduces substantial variance. While the model eventually achieves maximum episode lengths, its asymptotic reward remains sub-optimal, demonstrating that the recurrent state struggles to maintain the necessary morphological context over time without step-wise re-injection. 

Third, we evaluate the limitations of purely implicit system identification. The **w/o PME** variant, which attempts to infer morphology solely from proprioceptive history without explicit physical parameters, successfully learns to maximize episode length but plateaus at a noticeably lower asymptotic reward compared to the full method. This performance gap highlights that while implicit system identification can achieve basic locomotion, explicit physical morphology is required to discover and stabilize highly refined, optimal gaits across diverse robots and to improve sample efficiency. 

Finally, the standard baseline ( **w/o PME & ARN** , structurally equivalent to DreamerV3) performs poorly on the joint heterogeneous distribution. It peaks at a reward of roughly 10 and fails to achieve stable, full-length episodes before performance begins to degrade. In stark contrast, the full **QWM** framework consistently demonstrates the fastest sample efficiency, lowest variance, and highest asymptotic performance, validating that the integrated combination of explicit morphology encoding, dual-pathway conditioning, and reward normalization is critical for successful heterogeneous control. 

25 

## **F Real-World Deployment Details** 

We provide a quantitative assessment of the real-world deployment described in Subsec. 5.4. Our goal is to measure how closely the zero-shot QWM policy tracks velocity commands on physical hardware compared to a specialist PPO controller trained exclusively on each target platform, which serves as the empirical upper bound. 

**Protocol.** We conduct 10 trials per platform, each lasting 60 seconds, with random velocity commands sampled uniformly from the training command ranges (Table 10). Trials are conducted on flat indoor ground. The specialist PPO baseline is evaluated under identical conditions. No falls or manual resets occurred in any trial for either method. We report mean absolute tracking error for linear velocity ( _exy_ , m/s) and angular velocity ( _eyaw_ , rad/s), averaged across all timesteps and trials. 

**Discussion.** QWM achieves tracking errors within _∼_ 10% of the specialist baseline on both platforms. The gap stays bounded across both metrics and both robots, suggesting a systematic but bounded performance cost from zero-shot transfer rather than catastrophic failure. The complete absence of falls across all 20 trials confirms that the explicit morphology conditioning encodes sufficient physical grounding to maintain stability on unseen hardware in the presence of real-world unmodeled dynamics such as actuator backlash and ground friction variability. The slightly larger gap on the Unitree Go1 ( _exy_ : 0 _._ 34 vs. 0 _._ 31) compared to ANYmal-D ( _exy_ : 0 _._ 30 vs. 0 _._ 28) is consistent with the Go1’s higher-frequency dynamics, which place greater demands on precise timing of contact events that the zero-shot policy has not been tuned for. 

26 

## **G Latent State Disentanglement Analysis** 

A core architectural claim of QWM is that explicitly conditioning _ht_ on _µ_ at every recurrent step disentangles morphological identity from dynamic state. The recurrent state _ht_ should carry the static physical context, while _zt ∼ qϕ_ ( _zt | ht, et_ ), freed from re-inferring morphology from observations, should encode only the current dynamic state. This appendix provides the complete analysis testing this claim directly, with dimensionality reduction visualizations and quantitative probing across morphological and dynamic variables. 

### **G.1 Data Collection and Protocol** 

To collect a representative sample of the learned latent space, we roll out the trained QWM policy on all eight robots in our cohort under a uniform random velocity-command distribution. We collect latent pairs ( _ht, zt_ ) from 128 independent trajectories of 32 steps each, yielding 4096 latent state pairs per robot and 32768 points in total. At each step we record the full concatenated latent vector [ _ht, zt_ ] _∈_ R<sup>3072</sup> alongside scalar annotations, namely robot identity (morphology label), forward speed _vx_ , linear speed _∥v∥_ , angular speed _∥ω∥_ , and mean joint activity mean _|q|_ as a proxy for gait phase. These annotations are used purely for post-hoc coloring and play no role in the model. 

### **G.2 Morphology Disentanglement of** _ht_ **and** _zt_ 


Figure 6: Latent disentanglement. PCA of _ht_ (left) and _zt_ (right), both colored by robot identity. The _µ_ - conditioned recurrent state organizes into morphology-specific clusters. The stochastic state collapses into a single morphology-agnostic cloud. By morphology the silhouette score of _ht_ greatly exceeds that of _zt_ , quantifying the asymmetry the architecture is designed to produce. 

Applying PCA to each component separately, the contrast in Fig. 6 is direct evidence for the intended functional decomposition. The _µ_ -conditioned recurrent state _ht_ partitions cleanly into morphologyspecific clusters, with each robot occupying a distinct region of the projection. The stochastic state _zt_ , by contrast, collapses into a single intermixed cloud with no visible morphological structure, yet retains smooth velocity gradients under the same projection (App. G.5), confirming that dynamic information is preserved. 

A probing analysis quantifies the asymmetry. The silhouette score of _zt_ under morphology labels is 0 _._ 033 with only 9 _._ 8% between-class variance (detailed further in App. G.6), indicating that morphological identity is not redundantly re-encoded in _zt_ when _µ_ is provided to _ht_ . This decomposition is not imposed by any auxiliary loss. It arises naturally from the explicit conditioning, and it underpins QWM’s ability to control unseen robots by swapping _µ_ at deployment. Crucially, it also explains the robustness demonstrated in App. H.1, because _zt_ encodes dynamic state independently of morphological identity, so an inaccurate _µ_ that mis-steers _ht_ can be partially corrected online through _zt_ ’s conditioning on real observations _ot_ , providing a self-correcting mechanism absent from any purely parameter-conditioned system. 

27 

### **G.3 PCA of the Full Latent State** 


Figure 7: **PCA of QWM latent states** [ _ht, zt_ ], morphology (a) vs. dynamic state gradients (b-e). Each point is one latent observation, and 32768 points are shown across all eight robots. (a) Coloring by robot identity reveals that the latent space organizes itself into morphology-specific clusters, even though robot identity is _never_ provided as a supervised signal. (b-e) The same projection colored by four continuous dynamic variables shows smooth, consistent gradients _within_ each morphology cluster, demonstrating that dynamic execution context is encoded orthogonally to morphological identity. PCA explained variance for the first two components is 7 _._ 9%, reflecting the high-dimensional nature of the full latent space. 

Fig. 7 presents PCA of the full [ _ht, zt_ ] latent vector projected onto its first two principal components. Panel (a) colors each point by robot identity. The three ANYmal variants (B, C, D) form an overlapping super-cluster, reflecting their high pairwise _µ_ similarity in the morphology feature space. Similarly, the Unitree series (A1, Go1, Go2) and Spot occupy a contiguous band, while Unitree B2 occupies a well-isolated region in the upper right of the PCA plane. These groupings emerge unsupervised, providing strong evidence that the latent dynamics model has internalized the physical kinematic families present in the training cohort. Notably, this isolated cluster remains controllable by the policy (Table 1), indicating that the learned latent geometry retains predictive validity even in low-density regions of _µ_ -space. 

Panels (b-e) overlay continuous dynamic annotations on the same projection. Within each morphology cluster, there are smooth, spatially coherent gradients along all four dynamic variables. High forward speed _vx_ (yellow) consistently occupies specific sub-regions of each cluster, transitioning smoothly to low-speed states (purple) within the same cluster boundary. The same pattern holds for linear speed _∥v∥_ , angular speed _∥ω∥_ , and gait activity mean _|q|_ . This indicates that the learned latent geometry encodes dynamic state as a _continuous manifold within_ each morphology’s cluster, rather than conflating the two sources of variation into an entangled representation. 

The relatively low explained variance of the first two PCA components (7 _._ 9%) is expected, since the latent space is 3072-dimensional and captures rich, high-frequency dynamics. The visible structure in PCA-2 is therefore a conservative lower bound on the actual degree of organization present. 

### **G.4 t-SNE of the Full Latent State** 


Figure 8: **t-SNE of QWM latent states** [ _ht, zt_ ], morphology (a) vs. dynamic state gradients (b–e). t-SNE (perplexity = 40, 1000 iterations, KL divergence = 1 _._ 73) is applied to the same 32768-point dataset as Fig. 7. (a) Each robot occupies a spatially distinct, often multi-lobed cluster, and the multi-lobe structure within a single robot reflects different locomotion regimes (e.g., slow walk vs. fast trot). (b–e) Dynamic variables exhibit strong intra-cluster gradients, confirming that within each morphology’s region the model encodes a continuous dynamic state manifold. 

28 

Fig. 8 presents a t-SNE embedding (perplexity = 40, 1000 iterations, final KL divergence = 1 _._ 73) of the same dataset. t-SNE preserves local neighborhood structure and thus reveals finer-grained organization than PCA. 

Panel (a) shows that every robot occupies one or more spatially isolated regions with near-zero overlap between morphology classes. Several robots exhibit a characteristic multi-lobe structure, for instance the ANYmal variants each show a main cluster flanked by smaller satellite regions. We attribute these sub-clusters to distinct locomotion regimes captured by the policy (e.g., stationary standing, slow-speed trotting, high-speed locomotion), consistent with the dynamic gradients visible in panels (b-e). 

The Unitree A1, Go1, and Go2 clusters, while distinct in panel (a), are spatially adjacent in the t-SNE plane, mirroring their high z-score similarity in the morphology feature space. Analogously, the ANYmal-B, C, and D clusters are neighboring, consistent with z-score similarities. This spatial proximity in the learned latent space directly explains QWM’s success at zero-shot interpolation (Subsec. 5.3). The target robot’s morphology vector places it in a high-density region of the training distribution, allowing the WM to synthesize a plausible dynamic model by interpolating between its nearest neighbors in latent space. 

Panels (b-e) confirm the same pattern observed in PCA, with velocity gradients smooth and spatially coherent within each morphological cluster. Importantly, no systematic leakage of dynamic information _across_ morphology boundaries is observed. Regions of high _vx_ for one robot type do not merge with high- _vx_ regions of a different robot type, indicating that dynamic and morphological degrees of freedom are not collapsed into the same latent directions. 

### **G.5 Probing Analysis of** _ht_ **and** _zt_ 


Figure 9: Dynamic-state probing of _ht_ vs. _zt_ . PCA projections of each latent component, colored by forward speed _vx_ . The morphology-colored counterpart of this figure appears earlier in this section (Fig. 6), and here we show the same projections under a dynamic-state coloring to complete the probing picture. Left ( _ht_ ): Velocity gradients are visible _within_ each morphology-specific region, indicating that _ht_ tracks the evolving dynamic trajectory of each robot in its morphology-aligned subspace. Right ( _zt_ ): The cloud that is unstructured by morphology (see Fig. 6), yet a smooth _vx_ gradient persists across the full projection, confirming that _zt_ retains the instantaneous dynamic state of the robot even as it sheds morphological identity. 

App. G.2 introduced the central contrast. Under PCA, _ht_ partitions into morphology-specific clusters while _zt_ collapses into a single morphology-agnostic cloud. That analysis established _which component carries morphological identity_ . Here we complete the probing picture by overlaying _dynamic-state_ information on the same projections, asking the complementary question of whether each component retains the current dynamic state or loses it when morphology is removed. 

**The deterministic recurrent state** _ht_ **.** The left panel of Fig. 9 shows that _ht_ encodes _both_ morphological identity (visible as cluster structure in Fig. 6) and dynamic state (visible as the _vx_ gradient within each cluster). This dual structure is the intended behavior of the architecture. The recurrent state _ht_ = _fϕ_ ( _ht−_ 1 _, zt−_ 1 _, at−_ 1 _, µ_ ) is conditioned on _µ_ at every step, continuously steering the hidden state toward a morphology-aligned regime, while the GRU recurrence integrates the action and prior stochastic state to track the dynamic trajectory within that regime. The result is a _physics-_ 

29 

_contextualized memory_ . _ht_ knows which robot it is controlling and follows that robot’s evolving state through its morphology-specific region of latent space. 

**The stochastic observation state** _zt_ **.** The right panel presents the critical evidence. Although _zt_ has shed all morphological structure (Fig. 6), a smooth, spatially coherent _vx_ gradient remains visible across the projection, with high-velocity states (yellow) on one side of the cloud and low-velocity states (purple) on the other and continuous transitions between them. The dynamic information has not been lost, it has been _decoupled_ from morphological identity. This is what the architecture predicts. Because _µ_ is explicitly provided to _ht_ , the stochastic encoder _zt ∼ qϕ_ ( _zt | ht, et_ ) does not need to re-infer physical identity from the observation _ot_ , since that context is already present in _ht_ . Consequently _zt_ is free to encode only the residual, morphology-independent dynamic information in the current observation. The two views together (morphology in Fig. 6, velocity here) form the complete probing argument. _ht_ carries both signals, _zt_ carries only the dynamic one. 

### **G.6 Quantitative Disentanglement Metrics** 

To complement the visual evidence, we compute three quantitative metrics on the _zt_ embeddings, the latent component that, according to our hypothesis, should be _free_ of morphological structure. 

Table 12: Quantitative disentanglement metrics computed on the stochastic state _zt_ across all 32 _,_ 768 collected points. Low silhouette score and high within-class variance fraction confirm that _zt_ encodes negligible morphological information. 

|**Metric**|**Value**|**Interpretation**|
|---|---|---|
|Silhouette score (morphology)|0_._033|_≈_0_⇒_no cluster separation|
|Between-class variance fraction|0_._098|9_._8%of variance is inter-morphology|
|Within-class variance fraction|0_._901|90_._1%of variance is intra-morphology|


Table 12 reports these metrics for _zt_ . The silhouette score of 0 _._ 033 (range [ _−_ 1 _,_ 1], where 1 indicates perfect separation and 0 indicates random overlap) is near zero, indicating that morphology labels are essentially meaningless for partitioning the _zt_ space. The variance decomposition reinforces this, with only 9 _._ 8% of total variance in _zt_ falling between morphology classes while 90 _._ 1% is within-class dynamic variance. Taken together, these numbers confirm that the stochastic state _zt_ carries overwhelmingly more information about the robot’s instantaneous dynamic state than about its physical identity. 

We note that computing the same silhouette score on _ht_ yields a substantially higher value, consistent with the visible cluster separation in the top row of Fig. 9. The asymmetry between _ht_ and _zt_ on this morphology-based metric is the quantitative signature of the disentanglement the architecture is designed to achieve. 

### **G.7 Summary** 

Converging evidence from PCA (App. G.3), t-SNE (App. G.4), probing (App. G.5), and quantitative metrics (App. G.6) confirms the functional decomposition introduced in App. G.2. The _µ_ - conditioned recurrent state _ht_ encodes both morphological identity and dynamic trajectory context, while the stochastic state _zt_ encodes purely dynamic state with negligible morphological structure (silhouette = 0 _._ 033, 9 _._ 8% between-class variance). The spatial proximity of kinematically similar robots in the t-SNE plane mirrors their low pairwise distance in morphology feature space, directly explaining QWM’s interpolation capability. This decomposition arises naturally from the explicit _µ_ conditioning, without any auxiliary disentanglement loss. 

30 

## **H Robustness to Perturbations** 

The zero-shot generalization results (Subsec. 5.3) show the model-based route succeeding where a model-free policy given the same _µ_ does not. The underlying mechanism is a correction channel that conditioning the dynamics creates and conditioning a policy cannot. PME-PPO maps _µ_ directly to actions, so any error in _µ_ , or any drift of the real robot away from its specification, propagates straight to control with no correction. QWM instead exposes its policy to the latent state ( _ht, zt_ ), where _µ_ sets the morphological prior through _ht_ while the stochastic state _zt ∼ qϕ_ ( _zt | ht, et_ ) rereads the true dynamic state from observations _ot_ at every step. Because _zt_ is empirically decoupled from morphological identity (App. G), it can encode the residual between the specified and the realized robot, which a feedforward _µ_ -policy has no channel to represent. 

We probe this mechanism along two orthogonal axes. App. H.1 holds the world nominal and corrupts _µ_ itself, asking whether the latent channel absorbs errors in the specification. App. H.2 holds _µ_ nominal and perturbs the true world, asking whether the latent channel absorbs physical effects that _µ_ cannot describe. Together the two studies bracket both directions of spec-versus-reality divergence. 

### **H.1 Robustness to Morphological Parameter Uncertainty** 

We argue that the learned latent dynamics ( _ht, zt_ ) capture behavior that _µ_ cannot encode. PME-PPO is our closest proxy for a purely spec-sheet-driven controller, since it receives the same _µ_ but has no learned residual channel. If the latent-channel hypothesis holds, QWM should tolerate minor _µ_ inaccuracies such as unmodeled payloads or miscalibration, because the latent channel absorbs the residual. A pure lookup has no such fallback. We perturb _µ_ at test time by applying multiplicative noise to each raw feature before normalization: 


We then re-apply training-cohort normalization, so the model receives a plausible but inaccurate _µ_ rather than an out-of-range input. The discrete topology flag _k_ cfg is held fixed, since flipping it changes the kinematic family entirely. We evaluate over 20 noise draws _×_ 5 seeds _×_ 128 envs on all three held-out robots. 

Table 13 reveals an asymmetry growing with perturbation magnitude. At _δ_ = 0 _._ 05, QWM is essentially unaffected, dropping by at most 3%, within the range absorbed by domain randomization, while PME-PPO already loses 16 _−_ 17% of its lower baseline. At _δ_ = 0 _._ 1, QWM retains about 93% against PME-PPO’s 63%, and at _δ_ = 0 _._ 2, about 80% against 33%. QWM never falls below the _unperturbed_ PME-PPO baseline on any robot, even when its own _µ_ is corrupted by 20%. The mechanism distinguishes two architectures clearly. PME-PPO maps _µ_ directly to actions, so parameter error propagates to control with no correction. QWM 

Table 13: Robustness to _µ_ perturbation (episode length under multiplicative noise on raw features). QWM degrades gracefully. PME-PPO fails sharply, lacking a latent correction channel. Mean _±_ std over 20 draws _×_ 5 seeds. _δ_ = 0 reproduces Table 1. 

|**Method**|_δ_|**ANYmal-D**|**Unitree Go1**|**Unitree B2**|
|---|---|---|---|---|
||0_._00|530_±_8_._2|602_±_14_._9|337_±_23_._1|
|**PME-PPO**|0_._05|441_±_18_._4<br>|498_±_22_._7<br>|284_±_31_._8<br>|
||0_._10|329_±_27_._1|387_±_31_._5|223_±_38_._4|
||0_._20|174_±_41_._6|208_±_47_._2|142_±_44_._9|
||0_._00|948_._6_±_12_._1|974_._4_±_6_._2|925_._4_±_17_._2|
|**WM**|0_._05|931_._2_±_14_._8|962_._1_±_9_._4|897_._6_±_22_._5|
|**Q**|0_._10|887_._4_±_23_._6|921_._7_±_18_._1|834_._2_±_35_._1|
||0_._20|742_._8_±_51_._3|801_._5_±_43_._7|658_._9_±_67_._4|


instead exposes its policy to ( _ht, zt_ ), where _zt_ is inferred from real observations _ot_ at every step. Under a perturbed _µ_ , the recurrent state _ht_ is mis-steered, but _zt_ still reads the true dynamic state. The latent disentanglement in App. G (silhouette = 0 _._ 033, with _zt_ encoding dynamic state independently of morphological identity) is the necessary precondition, because _zt_ cannot compensate for an inaccurate _µ_ unless it is decoupled from it. B2 sharpens this further. QWM holds its episode length above 650 even at _δ_ = 0 _._ 2, despite B2’s unperturbed _µ_ already lying outside the training cluster, whereas PME-PPO stays in the 140 _−_ 280 range across all _δ_ , below its operational floor regardless of _µ_ quality. Together with the out-of-cluster B2 result (Subsec. 5.3), where PME-PPO collapses while QWM succeeds, and the disentanglement analysis (App. G), this forms a three-part argument. First, _µ_ alone is insufficient for out-of-cluster transfer. Second, _zt_ carries dynamic information decoupled 

31 

from _µ_ . Third, this decoupling absorbs _µ_ inaccuracies at test time, a property structurally impossible for a spec-sheet lookup and exactly what a grey-box analytical-plus-residual approach would need, except that QWM learns both channels jointly without a differentiable physics engine. 

### **H.2 Robustness to Unmodeled Dynamics** 

App. H.1 probed an _inaccurate µ_ on a nominal world. We now probe the complement, a _correct µ_ describing a robot whose true dynamics have departed from spec through effects _µ_ cannot encode. This is the regime that motivates a learned dynamics model over an analytical engine, and we make the contrast explicit by adding a third baseline. **Analytical-** _µ_ is a rigid-body simulator used as an open-loop _predictor_ (not a controller). Given an initial state and an action sequence, it forwardsimulates the resulting state trajectory from physics. We configure it deliberately to _steelman_ the spec-sheet case. It is instantiated with the robot’s true _nominal_ parameters, including physical quantities that _µ_ omits entirely, such as surface friction and joint damping. It therefore receives strictly more information than a real spec sheet provides, and is near-exact when the robot matches its nominal description. The one thing it is never told is the test-time perturbation. When we attenuate torque or add payload to the _true_ world, Analytical- _µ_ continues to simulate the unperturbed nominal robot. It has no channel to reconcile its forecast against the robot’s observed behavior. 

Critically, Analytical- _µ_ is _not_ online SysID, which would re-estimate parameters from observed transitions and, given enough data, correct for the perturbation. It is the degenerate case in which those parameters stay frozen at the nominal specification, isolating the predictive value of parameter conditioning alone. It is the analytical counterpart of PME-PPO, the latter being a model-free policy conditioned on _µ_ and the former an analytical predictor conditioned on _µ_ . Both lack the learned latent residual ( _ht, zt_ ) that lets QWM reconcile specified against realized dynamics, the correction a SysID module would otherwise provide, here amortized into a single frozen forward model rather than a per-step estimation loop. 

**Open-loop prediction protocol.** For each perturbed rollout we run QWM’s policy on the true perturbed robot, record the executed action sequence and the ground-truth state trajectory, then ask each predictor to reproduce that trajectory from a short context window ( _T_ = 5) over a 45-step horizon, feeding only the recorded actions. QWM predicts via its transition model conditioned on nominal _µ_ . Analytical- _µ_ predicts via rigid-body simulation of the nominal robot. We report NMSE against the perturbed ground truth, normalized by each robot’s natural motion variance, in Table 14. All perturbations are applied at test time to frozen policies within the same environment used for training. Analytical- _µ_ is a separate instance of the same PhysX engine configured as the nominal robot. Implementation details are given in App. H.3. 

**Torque attenuation.** We scale the realized joint torque, _τ_<sup>eff</sup> = (1 _− η_ ) _τ_ , with _η ∈{_ 0 _._ 1 _,_ 0 _._ 2 _}_ applied uniformly across all 12 joints. This is the controlled single-parameter version of motor wear, which is typically asymmetric, and we leave per-joint degradation to future work. Crucially, _µ_ stays nominal. The torque capacity feature _µ_ act still advertises the full robot description limits, exactly as a real deployment would, and the effect is absent from both _µ_ and the training-time randomization (App. A), making it genuinely unmodeled for every method. 

**Payload.** We add a trunk payload equal to a fraction _p ∈{_ 0 _._ 1 _,_ 0 _._ 2 _}_ of the nominal mass, with a corresponding center-of-mass offset, again holding _µ_ nominal. This is the mirror image of App. H.1, where the dynamics were correct and _µ_ was corrupted. Here _µ_ is correct for the spec but the physical robot has departed from it. Together the two studies bracket both directions of spec-versus-reality divergence. We evaluate all three held-out robots over 20 draws _×_ 5 seeds _×_ 128 environments, reporting open-loop NMSE (Table 14) and closed-loop episode length (Table 15). 

**The crossover isolates the learned dynamics.** Table 14 shows the open-loop prediction comparison. At nominal conditions ( _η_ = 0, _p_ = 0), Analytical- _µ_ is near exact and outperforms QWM, as expected when the true parameters are known and held fixed. The decisive observation is the crossover. As soon as the true dynamics depart from _µ_ , even mildly ( _η_ = 0 _._ 1 or _p_ = 0 _._ 1), the analytical error climbs steeply because it keeps forward-simulating a robot that no longer exists, while 

32 

QWM stays low, with the same pattern at the stronger level. No fixed parameter set can track a world that has moved away from it, so the learned dynamics act as a residual-absorption mechanism that a static prior cannot supply. 

**Closed-loop control mirrors this.** Table 15 shows the same asymmetry in deployment. UnTable 14: Open-loop NMSE under unmodeled dynamder the strongest attenuation ( _η_ = 0 _._ 2), QWM ics, averaged over the three held-out robots (45-step retains 75 to 80% of its nominal episode length horizon, normalized by motion variance). Analytical- _µ_ is near exact at nominal but diverges once the true while PME-PPO falls to 44 to 47%, and at world departs from spec. QWM stays bounded because _p_ = 0 _._ 2 it retains 79 to 84% against PME- _ztt_ reads the realized dynamics from observations. PPO’s 50 to 58%. PME-PPO’s degradation is partly expected, since a reactive model-free **Perturb. Level Analytical-** _µ_ **QWM** policy has no internal model against which to Torque 00 _.._ 01 00 _.._ 0334 _± ±_ 0 0 _.._ 0106 00 _.._ 1116 _± ±_ 0 0 _.._ 0304 reconcile observed behavior. The informative ( _η_ ) 0 _._ 2 0 _._ 72 _±_ 0 _._ 11 0 _._ 24 _±_ 0 _._ 05 signal is therefore the margin and shape of the Payload 0 _._ 0 0 _._ 03 _±_ 0 _._ 01 0 _._ 11 _±_ 0 _._ 03 0 _._ 1 0 _._ 28 _±_ 0 _._ 05 0 _._ 15 _±_ 0 _._ 03 gap, not its existence. QWM exposes its policy ( _p_ ) 0 _._ 2 0 _._ 61 _±_ 0 _._ 09 0 _._ 21 _±_ 0 _._ 05 to ( _ht, zt_ ), where _zt ∼ qϕ_ ( _zt | ht, et_ ) continuously re-estimates the true dynamic state from observations and fuses it with the learned model, absorbing the spec-versus-reality discrepancy online rather than propagating it to control. 

Table 14: Open-loop NMSE under unmodeled dynamics, averaged over the three held-out robots (45-step horizon, normalized by motion variance). Analytical- _µ_ is near exact at nominal but diverges once the true world departs from spec. QWM stays bounded because _ztt_ reads the realized dynamics from observations. 

**Why not plan with the analytical model?** Since Analytical- _µ_ is nearexact at nominal, one might use it for planning inside an MPC. The binding constraint, however, is correctness rather than speed. Table 14 shows the analytical prior is _wrong_ under unmodeled dynamics, so no amount of planning recovers control once the robot departs from spec, and repairing it requires exactly the online SysID loop that our latent state amortizes away. A secondary practical point is that a permorphology analytical model must be maintained for each robot in the control loop, whereas QWM serves the whole cohort through _µ_ injection into a single frozen forward model. The correctness axis is the one that cannot be engineered around. 

Table 15: Robustness to unmodeled dynamics. Closed-loop episode length under torque attenuation and payload, with nominal _µ_ . QWM degrades gracefully, since _zt_ reads true dynamics from _ot_ . PME-PPO, lacking a learned model, fails sharply. Mean _±_ std over 20 draws _×_ 5 seeds. The 0 _._ 0 rows reproduce Table 1. 

|**Method**|**Level**|**ANYmal-D**|**Unitree Go1**|**Unitree B2**|
|---|---|---|---|---|
|_Torque Att_|_enuation_<br>|(_η_)<br>|||
||0_._0|530_±_8_._2|602_±_14_._9|337_±_23_._1|
|PME-PPO|0_._1|388_±_21_._4|447_±_26_._8|233_±_31_._6|
||0_._2|244_±_33_._7|281_±_37_._2|148_±_36_._9|
||0_._0|948_._6_±_12_._1|974_._4_±_6_._2|925_._4_±_17_._2|
|QWM|0_._1|871_._4_±_19_._8|902_._7_±_15_._3|838_._1_±_26_._4|
||0_._2|742_._6_±_34_._5|781_._5_±_29_._1|695_._3_±_41_._8|
|_Payload M_|_ass_(_p_)||||
||0_._0|530_±_8_._2|602_±_14_._9|337_±_23_._1|
|PME-PPO|0_._1|418_±_19_._7|455_±_24_._3|258_±_29_._4|
||0_._2|309_±_31_._2|298_±_34_._1|181_±_35_._2|
||0_._0|948_._6_±_12_._1|974_._4_±_6_._2|925_._4_±_17_._2|
|QWM|0_._1|889_._3_±_17_._2<br>|896_._1_±_16_._7<br>|871_._7_±_22_._8<br>|
||0_._2|798_._4_±_28_._9|769_._3_±_31_._4|779_._2_±_35_._6|


**Bracketing both directions of spec-versus-reality divergence.** Taken together, App. H.1 and this section show that QWM is robust along both axes of deviation from the idealized description, an inaccurate spec of a correct robot (corrupted _µ_ , nominal world) and a correct spec of a degraded robot (nominal _µ_ , perturbed world). A pure spec-sheet system, whether a model-free _µ_ -policy or a static analytical prior, is robust to neither, since its behavior is determined entirely by a _µ_ that no longer matches reality. This is the empirical content of the claim that ( _ht, zt_ ) encode physical grounding beyond what _µ_ alone provides, learned jointly without a differentiable physics engine in the loop. 

### **H.3 Implementation Details** 

All experiments are run in the Hetero-Isaac environment, identical to training. Policies and WM weights are frozen. 

33 

**Torque attenuation.** The policy outputs joint position targets, which the PD controller converts to joint torques _τ_ . We scale the resulting torque, _τ_<sup>eff</sup> = (1 _− η_ ) _τ_ , before it is applied to the articulation, leaving the robot description-declared effort limits (and hence _µ_ act in _µ_ ) unchanged. _η_ is fixed per episode (resampled per draw), applied uniformly to all 12 joints. 

**Payload.** We increase the base-link mass by a fraction of the robot’s nominal total mass and update the link inertia consistently, placing the added mass at the trunk attachment point to produce a center-of-mass offset. The geometry and all other links are unchanged. _µ_ is recomputed from the unchanged robot description and therefore remains nominal. 

**Analytical-** _µ_ **predictor.** Analytical- _µ_ is a separate Hetero-Isaac instance configured with the robot’s true nominal parameters, namely robot description-derived geometry and mass plus the friction and damping values used for the nominal robot (App. A). It receives no information about the test-time perturbation. For each evaluation rollout we run QWM’s policy on the perturbed true robot, record the executed action (position-target) sequence and the ground-truth state trajectory, and initialize both predictors from the ground-truth state at _t_ = _T_ = 5. Each predictor then rolls 45 steps open-loop fed only the recorded targets. Analytical- _µ_ converts targets to torques via the same PD controller and integrates rigid-body dynamics. QWM predicts via its _µ_ -conditioned transition model. No observation feedback is provided to either predictor during the rollout. 

**NMSE.** We compute NMSE over the predicted physical proprioceptive channels, excluding the command and previous-action channels, which are inputs rather than predicted quantities. Errors are normalized per-channel by that channel’s natural variance over the evaluation set, then averaged. 

34 

