---
title: "BAT: Balancing Agility and Stability via Online Policy Switching for Long-Horizon Whole-Body Humanoid Control"
date: "2026-04-01"
authors: "Donghoon Baek; Sang-Hun Kim; Sehoon Ha"
url: https://arxiv.org/abs/2604.01064
pdf: https://arxiv.org/pdf/2604.01064
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.01064)** / [論文ページ](https://arxiv.org/abs/2604.01064)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# BAT: Balancing Agility and Stability via Online Policy Switching for Long-Horizon Whole-Body Humanoid Control 

Donghoon Baek<sup>1</sup> , Sang-Hun Kim<sup>2</sup> , and Sehoon Ha<sup>1</sup> 

**_Abstract_ —Despite advances in reinforcement and imitation learning, achieving both precise control and dynamic whole-body behaviors in long-horizon tasks remains challenging. Existing approaches typically follow two paradigms: coupled whole-body policies for global coordination and decoupled policies for modular precision. However, effectively combining these two types of controllers to achieve agility, robustness, and precision remains challenging. In this work, we propose BAT, an online policyswitching framework that dynamically selects between coupled and decoupled whole-body RL generalist controllers according to the evolving motion context. BAT employs two complementary switching predictors: OpVQ-VAE provides motion-token-based predictions with strong generalization, while OpHRL provides closed-loop, state-aware predictions. A Token-Familiarity Router (TFR) selects between their predictions, favoring OpHRL for familiar token sequences and OpVQ-VAE for unfamiliar ones when their predictions disagree. BAT achieves 85.2% success on seen long-horizon motion combinations, while retaining 71.3% success on unseen motions. BAT also outperforms existing whole-body controllers on individual motions and demonstrates successful zero-shot deployment on the Unitree G1 humanoid.** 

**_Index Terms_ —Humanoid Whole-Body Control, Reinforcement Learning, Representation Learning.** 

## I. INTRODUCTION 

Learning-based whole-body humanoid control can be broadly categorized into two paradigms. _Decoupled policies_ separate upper-body manipulation from lower-body locomotion, enabling precise upper-body tracking and robust locomotion through specialized control objectives [1], [2]. In contrast, _coupled policies_ use unified motion imitation to enable agile, coordinated whole-body behaviors [3], [4], [5], [6]. Their complementary strengths are particularly relevant to longhorizon tasks, where control demands shift between precise upper-body execution and dynamic whole-body coordination. 

These complementary strengths motivate combining decoupled and coupled control within a single long-horizon execution. Both controllers are generalists that support broad motion repertoires, but their different control formulations make them suitable for different motion regimes. We propose BAT (Balancing Agility and Stability), an online policyswitching framework that exploits this complementarity by selecting between two fixed generalist controllers as control demands evolve (Fig. 1). By combining the decoupled policy’s stability and precision with the coupled policy’s agility, BAT enables both capabilities in long-horizon, multi-task execution. Realizing this approach across diverse, long-horizon tasks presents two main challenges: (1) the number of possible 

> 1Georgia Institute of Technology, Atlanta, GA, 30308, USA 

> 2Samsung Research 

> *Correspondence to dbaek36@gatech.edu 


**𝑜 𝑜 𝑜 𝑜** Fig. 1: **Conceptual overview of BAT** . The decoupled policy provides stability and robustness, while the coupled policy enables agile whole-body motion. BAT adaptively switches between them to combine both strengths. 

motion compositions grows combinatorially with the motion repertoire and task horizon, making exhaustive training coverage impractical; and (2) demonstrations provide neither controller-selection nor switch-timing labels, while the consequences of a controller choice may be delayed and depend on the evolving robot state, making reward-only switching difficult to optimize. 

BAT addresses these challenges through two complementary switching predictors. To address challenge (1), an optionaware vector-quantized variational autoencoder (OpVQ-VAE) learns a reusable vocabulary of discrete motion tokens that encode controller preference. A transition-aware option head uses this shared vocabulary across motion compositions, reducing the need for exhaustive training coverage. To address challenge (2), option-guided hierarchical reinforcement learning (OpHRL) uses offline cross-simulator switch-boundary evaluation to obtain controller-selection and timing supervision. This guidance initializes and regularizes the switching policy, reducing reliance on delayed rewards alone, while closed-loop reinforcement learning refines its decisions using proprioceptive feedback and motion references. A TokenFamiliarity Router (TFR) integrates the two predictors, favoring OpHRL for familiar token sequences and OpVQ-VAE for unfamiliar ones when their predictions disagree. 

Our contributions are threefold: (1) an online policyswitching framework that combines the complementary strengths of decoupled and coupled generalist policies to balance stability, precision, and agility in humanoid whole-body control; (2) a switching architecture that combines OpVQ-VAE for motion-based generalization through a reusable, optionaware token vocabulary with OpHRL for state-aware switching learned through cross-simulator supervision and closed-loop reinforcement learning, using a Token-Familiarity Router to select between their predictions; and (3) extensive simulation 

2 

evaluations against diverse baselines, qualitative hardware demonstrations, and an analysis of the complementary characteristics of decoupled and coupled policies. 

## II. RELATED WORK 

## _A. Whole-Body Humanoid Control_ 

Model-based approaches have been widely used for wholebody humanoid control [7], [8], but their reliance on accurate dynamics and contact models limits robustness. More recently, advances in human demonstrations [9], imitation learning [10], reinforcement learning, and large-scale simulation [11] have enabled learning-based approaches that alleviate these limitations. Building on the strong performance of reinforcement learning for motion tracking in physics-based character animation [10], more recent studies have demonstrated significant progress in transferring policies learned in simulation to realworld robotic systems [3], [5], [4]. Rather than replacing unified controllers, we extend their capabilities through a motion-aware policy-switching mechanism that allows each controller to operate within its most effective regime, striking a balance between precise manipulation and agile motion dynamics across diverse tasks. 

## _B. Hybrid and Compositional Approaches to Robot Control_ 

Effective robot control often requires leveraging multiple specialized controllers that perform well in different regimes. Value-function based switching provides a simple selection mechanism [12], but becomes unstable when task boundaries are ambiguous. Mixture-of-experts methods combine controllers via gating [13], yet struggle when expert behaviors differ significantly. Meta-learning aims to adapt a unified policy across tasks [14], but may lack sufficient specialization. Rule- or event-based switching relies on predefined transition conditions, while supervised switching requires expert selection labels, limiting their applicability to unseen motion sequences [15], [16]. Hierarchical reinforcement learning enables temporal abstraction through task decomposition and option selection [17], [18], including goal-conditioned hierarchies with off-policy correction [19]. Prior hierarchical locomotion methods learn reusable primitives [20], coordinate gaitspecific policies [21], use reference-based skill graphs [22], or enable gait transitions through symmetry-guided hierarchies [23]. While these approaches organize skills, subgoals, or gaits, BAT switches online between fixed generalist wholebody controllers to combine the stability and precision favored by decoupled control with the dynamic coordination favored by coupled control across diverse, long-horizon sequential motion tasks. 

## _C. Representation Learning_ 

Compact latent representations provide effective interfaces for learning control in high-dimensional motion spaces. VAEbased methods learn continuous motion manifolds that can serve as action representations for downstream control [24], while recent humanoid controllers encode motions, goals, and 

behaviors in latent spaces to improve learning and generalization [5], [4]. In contrast, vector-quantized models such as VQ-VAE represent diverse motions using a finite vocabulary of reusable discrete tokens [25], [26]. Token-based representations have also been explored for sequential humanoid control, where discretized sensorimotor trajectories provide a compact interface for behavior prediction [27]. Inspired by the reuse and recombination of discrete tokens across motions, we employ a shared codebook to represent diverse motions and their long-horizon compositions. Unlike prior work focused primarily on motion generation, reconstruction, or generalpurpose control, our option-aware representation is explicitly trained to distinguish controller-specific regimes for online policy switching. 

## III. PROBLEM DEFINITION: CHALLENGE OF LONG-HORIZON SWITCHING 

We consider online switching between two fixed wholebody controllers, Π = _{πD, πC}_ , where _πD_ and _πC_ denote the decoupled and coupled controllers, respectively. An = episode consists of a long-horizon motion sequence _τ_ ( _m_ 1 _, . . . , mN_ ) formed by concatenating multiple motion segments. At each high-level decision step _t_ , the switching policy _π_ sw( _ct | st_ ) selects a controller index _ct ∈C_ = _{D, C}_ and executes the corresponding low-level policy _πct_ for _Ho_ steps. Under the options framework [28], the resulting option value is 


where _Ho_ is the option duration, _rt,i_ is the reward at its _i_ -th low-level step, _γ_ is the per-low-level-step discount factor, _st_ is the environment state at high-level decision _t_ , and _st_ +1 is the next high-level state after executing the selected controller for _Ho_ low-level steps. _V_<sup>_π_sw</sup> denotes the continuation value under the high-level switching policy. 

Learning this switching policy is challenging because motion demonstrations provide neither controller-selection nor switch-timing labels, while the consequences of a controller choice may be delayed and depend on the evolving robot state. Moreover, decision-critical phases such as takeoff, landing, and recovery occur infrequently, and the number of possible motion sequences grows combinatorially with the motion repertoire and sequence length. These challenges make rewardonly switching and exhaustive training coverage impractical. 

## IV. DECOUPLED AND COUPLED WHOLE-BODY POLICIES 

## _A. Decoupled and Coupled Whole-Body Policy_ 

We adopt the decoupled whole-body reinforcement learning framework of FALCON [1], excluding its force-compensation and privileged-force modules. We leverage its decoupled upper- and lower-body training, where the upper body is conditioned on joint-space references, while the lower body is commanded through locomotion-level quantities. The decoupled policy is denoted as **u**<sup>_D_</sup> _t_<sup>=</sup><sup>_πD_(</sup><sup>**o**</sup><sup>_D_</sup> _t_<sup>),where</sup><sup>**o**</sup><sup>_D_</sup> _t_<sup>addition-</sup> ally contains proprioceptive states and short observation/action 

3 


Fig. 2: Complementary policy strengths across motion families. _πD_ generally achieves higher upper-body tracking rewards, while _πC_ achieves higher lower-body tracking rewards and greater running/jogging stability. The 5,171 motions with valid BABEL sequence-level action labels are grouped into 12 motion groups. Bars show mean _πD − πC_ differences in fall-free rate (top, percentage points) and episode-mean tracking rewards (bottom: green, upperbody; orange, lower-body; purple, overall). Positive values favor _πD_ ; negative values favor _πC_ . _n_ denotes the number of motions. 

histories. The 29-DoF action is mapped to the joint target as **q**<sup>_∗_</sup> _t_<sup>_,D_</sup> = **q**<sup>0</sup><sup>_,D_</sup> + _sD_ **u**<sup>_D_</sup> _t_<sup>and tracked using joint-level PD control.</sup> We used TWIST [6] as the coupled whole-body controller. The coupled policy is denoted as **u**<sup>_C_</sup> _t_ = _πC_ ( **o**<sup>_C_</sup> _t_<sup>),where</sup> **o**<sup>_C_</sup> _t_<sup>containsthewhole-bodymotionreference,proprioceptive</sup> states, and temporal history. The 23-DoF action is mapped to the corresponding body joints of the 29-DoF G1 model as **q**<sup>_∗_</sup> _t,_<sup>_,C_</sup> _B_<sup>=</sup><sup>**q**</sup> _B_<sup>0</sup><sup>_,C_</sup> + _sC_ **u**<sup>_C_</sup> _t_<sup>,whiletheremaininghandjointsare</sup> held at their default targets. The resulting whole-body target is tracked using joint-level PD control. 

## V. BAT: BALANCING AGILITY AND STABILITY VIA ONLINE PREDICTIVE POLICY SWITCHING 

We first analyze the complementary strengths of _πD_ and _πC_ across motion families (Fig. 2): _πD_ generally provides stronger upper-body tracking, whereas _πC_ provides stronger lower-body tracking and greater running/jogging stability. We then introduce BAT, which combines these strengths through online policy switching (Fig. 3). 

## _A. Training Data and Cross-Simulator Switching Supervision_ 

We construct _D_ single by filtering AMASS for physically feasible motions and split it at the motion level into a 90% training subset, _D_ single<sup>train,anda10%held-outsubset,</sup><sup>_D_</sup> single<sup>test.</sup> Each frame receives a preferred-controller label _c_<sup>_⋆_</sup> _t_<sup>_∈C_by</sup> evaluating the two frozen policies from the same robot state in MuJoCo. The training subset supports Stage-1 option-aware tokenizer learning. We construct _D_ trans by randomly pairing and concatenating training clips. Each chain _τi_ = ( _m_<sup>_A_</sup> _i_<sup>_, mB_</sup> _i_<sup>)hasanoriginal</sup> clip boundary _b_<sup>clip</sup> _i_ and a controller order ( _c_<sup>_A_</sup> _i_<sup>_, cB_</sup> _i_<sup>)assigned</sup> through offline motion evaluation. For OpVQ-VAE Stage 2, each clip retains its controller label, and the option head is trained on _D_ trans _∪D_ single<sup>trainwiththetokenizerfrozen.Tokens</sup> from _D_ trans also provide the training statistics for familiarity estimation and threshold calibration in TFR; no test data are used. 

To obtain switching supervision for OpHRL, we refine the clip boundaries through cross-simulator search while preserving the controller order. For each chain, we evaluate 21 

candidate boundaries _bi,δ_ = _b_<sup>clip</sup> _i_ + _δ_ , where _δ_ = _g_ + _a_ , _g ∈ {−_ 60 _, −_ 30 _, −_ 15 _,_ 0 _,_ 15 _,_ 30 _,_ 60 _}_ , and _a ∈{−_ 5 _,_ 0 _,_ 5 _}_ , measured in motion frames at 30 Hz. All candidates undergo full-chain Isaac Gym rollouts. MuJoCo then reevaluates _δ_ = 0 and up to four successful shifted candidates. Among MuJoCo-successful candidates, selection prioritizes Isaac Gym success, proximity to the clip boundary, MuJoCo and Isaac Gym rewards, and tracking performance. If none succeeds in MuJoCo, we retain the original boundary. 

The selected boundary _b_<sup>_⋆_</sup> _i_ defines controller labels **c**<sup>_⋆_</sup> _i_<sup>,</sup> assigning _c_<sup>_A_</sup> _i_<sup>beforetheboundaryand</sup><sup>_cB_</sup> _i_<sup>thereafter.There-</sup> sulting dataset, _D_ Op = _{_ ( _τi,_ **c** _i_<sup>_⋆, b⋆_</sup> _i_<sup>)</sup><sup>_}M_</sup> _i_ =1<sup>,providessupervision</sup> for OpHRL’s behavior-cloning initialization and subsequent closed-loop RL refinement. 

## _B. Option-Aware Vector-Quantized VAE_ 

The number of possible motion sequences grows combinatorially as individual motions are concatenated. Inspired by discrete motion vocabularies and tokenized motion embeddings [25], [29], [30], we adopt a shared token vocabulary to represent diverse motions and their sequential compositions through reusable tokens, reducing the need to cover every motion combination during training. However, prior discrete motion representations primarily target reconstruction, generation, or prediction [31], [25], [26], [27], without explicitly encoding which low-level controller is more suitable. We therefore propose an option-aware VQ-VAE (OpVQ-VAE) that learns reusable motion tokens encoding both motion structure and controller preference. To make the tokens informative for controller selection, we augment motion reconstruction with option-prediction supervision and latent separation. Using the datasets defined in Sec. V-A, we train OpVQ-VAE in two stages. Stage 1 learns option-aware tokens from individual motions, while Stage 2 freezes the tokenizer and trains a transition-aware option head on individual and composed motions. 

_1) Motion Tokenization:_ Each frame is represented by a 50dimensional feature vector _xt ∈_ R<sup>50</sup> , consisting of root-local translational deltas, a yaw delta, 23-DOF joint positions, and 23-DOF joint velocities. The root deltas are obtained from smoothed root velocities expressed in the local root frame. From each clip in _D_ single<sup>train,weextractcausalwindows</sup><sup>_Wt_=</sup> ( _xt−W_ +1 _, . . . , xt_ ) of length _W_ = 16 and normalize them element-wise using the training-set statistics _µ_ and _σ_ . The encoder and VQ layer map each window to a discrete token sequence **z** _t_ = ( _zt,_ 1 _, . . . , zt,L_ ), where _zt,ℓ ∈{_ 1 _, . . . , K}_ , by nearest-neighbor assignment in the codebook **E** _∈_ R<sup>_K×dz_</sup> . We use _K_ = _dz_ = 256. With residual convolutional blocks and 4 _×_ temporal downsampling, each _W_ = 16 window produces _L_ = 4 tokens. The decoder reconstructs the window as _W_<sup>ˆ</sup> _t_ = Dec( **ez** _t_ ), where **ez** _t_ = ( **E** _zt,_ 1 _, . . . ,_ **E** _zt,L_ ) denotes the selected codebook embeddings. 

_2) Stage 1: Option-Aware Tokenizer Training:_ We augment an EMA-based VQ-VAE with option-prediction, latentseparation, and token-prediction objectives. Let **z** _e_ denote the continuous encoder output. The base objective is 

_L_ VQ = _L_ rec + _αcL_ commit + _αvL_ vel _,_ (2) 

4 


Fig. 3: **Overview of BAT.** (1) **Option-Aware VQ-VAE (OpVQ-VAE)** learns discrete motion tokens that encode motion structure and controller preference through reconstruction, option-prediction, and auxiliary objectives. After freezing the encoder and codebook, an LSTM–MLP head learns transition-aware option prediction from individual and composed motions. (2) **Option-Guided Hierarchical RL (OpHRL)** uses cross-simulator switch-boundary supervision from _D_ Op for behavior-cloning initialization and guided, proprioception-aware RL refinement. The supervision is obtained through full-chain Isaac Gym rollouts and MuJoCo validation (Sec. V-A). A low-level policy manager executes the selected controller. (3) **Token-Familiarity Router (TFR)** estimates causal token-sequence familiarity using 4-gram likelihood and selects between the predictions of OpVQ-VAE and OpHRL. EMA smoothing and hysteresis are applied to the familiarity score and routing decision, yielding the final selection between the decoupled policy _πD_ and coupled policy _πC_ . 

where _L_ rec = _∥Wt − W_<sup>ˆ</sup> _t∥H_ , _L_ commit = _∥_ **z** _e −_ sg[ **ez** _t_ ] _∥_ 2<sup>2,and</sup> _L_ vel = _∥_ ∆ _Wt −_ ∆ _W_<sup>ˆ</sup> _t∥H_ . Here, _∥· ∥H_ denotes the Smooth- _ℓ_ 1 loss, ∆ denotes frame-to-frame differences, and sg denotes stop-gradient. The codebook is updated by exponential moving average. The auxiliary heads use _e_ ˜ _zt_ = _ze_ + sg[ _ezt − ze_ ], the straight-through quantized embeddings. We set ( _αc, αv_ ) = (0 _._ 02 _,_ 0 _._ 5). 

**Option prediction.** Reconstruction alone does not ensure that the motion tokens retain information relevant to option selection. We therefore use an LSTM–MLP head to predict the preferred-option distribution _p_<sup>S1</sup> _t_<sup>(</sup><sup>_c_)=</sup><sup>_pϕ_(</sup><sup>_c|e_˜</sup><sup>_z_</sup> _t_<sup>)from</sup> the complete token sequence of the causal _W_ -frame window ending at time _t_ . We assign each window the majority framelevel controller label _c_ ¯<sup>_⋆_</sup> _t_<sup>= arg max</sup><sup>_c∈C_</sup> _W_ <u>1</u> � _ts_ = _t−W_ +1<sup>**1**[</sup><sup>_c_</sup> _s_<sup>_⋆_=</sup> _c_ ] and optimize _L_ pol = CE � _p_<sup>S1</sup> _t_<sup>(</sup><sup>_·_)</sup><sup>_,_¯</sup><sup>_c⋆_</sup> _t_ �. This objective makes the causal token sequence predictive of the preferred option. **Auxiliary latent objectives.** We use latent separation and next-token prediction to encourage option-discriminative tokens and capture local motion progression. For each window, we average its straight-through token embeddings and group the resulting representations by their majority controller labels. Let _e_ ¯ _D_ and _e_ ¯ _C_ denote the corresponding minibatch centroids. When both classes are present, we minimize _L_ sep = cos(¯ _eD,_ ¯ _eC_ ). The next-token loss is _L_ lat = CE( _gψ_ (˜ _et,_ 1: _L−_ 1) _, zt,L_ ), where _gψ_ predicts the final token from the preceding straight-through embeddings. The complete Stage-1 objective is 


where ( _αp, αs, αl_ ) = (0 _._ 5 _,_ 0 _._ 05 _,_ 0 _._ 1). 

_3) Stage 2: Transition-Aware Option Head Training:_ With the tokenizer frozen, we initialize the Stage-2 option head from Stage 1 and train it on _D_ trans _∪D_ single<sup>train.Givencausal</sup> token embeddings _ezt_ , the head predicts _p_<sup>_S_</sup> _t_<sup>2(</sup><sup>_c_) =</sup><sup>_pθ_(</sup><sup>_c | ez_</sup> _t_<sup>)</sup> and selects _c_ ˆ _t_ = arg max _c∈C p_<sup>_S_</sup> _t_<sup>2(</sup><sup>_c_).TheStage-2training</sup> objective is: 


Here, _c_<sup>_S_</sup> _t_<sup>2</sup> is the controller label of the constituent motion clip containing frame _t_ , as defined in Sec. V-A. We use _L_ cons = _∥p_<sup>S2</sup> _t_<sup>_−p_S2</sup> _t−_ 1<sup>_∥_</sup> 2<sup>2to encourage temporal consistency and</sup> _L_ sw = _p_<sup>S2</sup> _t_<sup>(</sup><sup>_D_)</sup><sup>_p_S2</sup> _t−_ 1<sup>(</sup><sup>_C_) +</sup><sup>_p_</sup> _t_<sup>S2(</sup><sup>_C_)</sup><sup>_p_S2</sup> _t−_ 1<sup>(</sup><sup>_D_)todiscouragefre-</sup> quent controller changes. We set ( _λp, λc, λs_ ) = (1 _,_ 0 _._ 1 _,_ 0 _._ 1). 

## _C. Option-Guided Hierarchical Reinforcement Learning_ 

OpHRL uses the cross-simulator supervision in _D_ Op to initialize and guide proprioception-aware, closed-loop switching. Unlike OpVQ-VAE, which uses only motion references, OpHRL observes both the robot state and motion reference to select between the frozen policies _πD_ and _πC_ . 

_1) Observation and Action Space:_ The high-level policy _π_ OpHRL receives a stacked observation constructed from proprioception, motion reference, and policy state. A singlestep observation is _o_ ¯ _t_ = [ _vt, ωt, gt, qt_<sup>ref</sup><sup>_, qt,q_˙</sup><sup>_t,_</sup><sup>**c**</sup><sup>_t−_1</sup><sup>_, at−_1</sup><sup>_, ηt_],</sup> where _vt, ωt, gt ∈_ R<sup>3</sup> are the base linear and angular velocities and projected gravity; _qt_<sup>ref</sup><sup>_, qt,q_˙</sup><sup>_t, at−_1</sup><sup>_∈_R29are the reference</sup> joint target, joint position, joint velocity, and previous lowlevel action; **c** _t−_ 1 _∈{_ 0 _,_ 1 _}_<sup>2</sup> is the one-hot encoding of the previous controller selection; and _ηt ∈_ R<sup>3</sup> is the current policy state including transition phase. We stack five consecutive steps to form _ot_ = [¯ _ot, . . . ,_ ¯ _ot−_ 4] _∈_ R<sup>650</sup> . The action space is discrete, _A_ = _{_ 0 _,_ 1 _}_ , corresponding to selecting _πD_ or _πC_ , with _π_ OpHRL outputting logits _ℓt ∈_ R<sup>2</sup> parameterizing the categorical distribution _π_ OpHRL( _ct | ot_ ). 

_2) Reward and Optimization:_ The high-level policy _π_ OpHRL is trained with the composite reward _rt_ = _w_ track _r_ track _− w_ reg _p_ reg _− w_ sw _p_ sw _− w_ term _p_ term. The tracking reward follows the deploy-time evaluation metric, _r_ track = _wur_ upper + _wlr_ lower + _wvr_ vel + _whr_ height. For the upperand lower-body joint groups, indexed by _j ∈{u, l}_ , we use _rj_ = exp[ _−αj_ MSE( **q** _t_<sup>_j,_</sup><sup>**q**ref</sup> _t_<sup>_,j_</sup> )]. The base-velocity and rootheight rewards are 


5 

The regularization penalty is 


where _p_ foot aggregates contact-force, foot-slip, and stumble penalties, and _p_ drift penalizes linear and angular drift under near-stationary commands. The switching penalty _p_ sw penalizes each controller change once the cumulative switch count exceeds the number of clip boundaries in the motion chain. The termination penalty _p_ term adds a unit penalty for a fall and another for terminal instability, defined as low base height or excessive body tilt near the end of the motion. 

We initialize _π_ OpHRL by behavior cloning with labels from _D_ Op and retain the BC loss during PPO fine-tuning: 


Here, _ot_ is the current high-level observation, and _c_<sup>_⋆_</sup> _t_<sup>=</sup><sup>_c⋆_</sup> _i,ft_<sup>is</sup> the label retrieved from _D_ Op for motion chain _i_ at its current motion-frame index _ft_ . The complete objective is 


Here, _π_ BC is the frozen policy used to initialize PPO finetuning. The coefficient _λ_ BC( _k_ ) decreases with training iteration _k_ , gradually reducing the contribution of BC supervision. 

The hysteretic router _gt ∈{_ 0 _,_ 1 _}_ selects OpHRL when _gt_ = 1 and OpVQ-VAE when _gt_ = 0: 


We set _τ_ on = 1 _._ 75 and _τ_ off = 2 _._ 69 to the 95th and 99.5th percentiles of the training EMA-smoothed windowNLL distribution, respectively. 

Let _c_<sup>OpHRL</sup> _t_ and _c_<sup>OpVQ</sup> _t_ denote the option IDs proposed by OpHRL and OpVQ-VAE. Unlike prior likelihood-based anomaly detection, BAT uses token familiarity only as a reliability cue when the two predictors disagree: 


The router selects OpHRL for familiar sequences and OpVQVAE for unfamiliar ones (Fig. 4(a)). The median OODwindow rate rises from 0 _._ 0% on Train and 3 _._ 1% on TestC to 62 _._ 1% on Test-U (Fig. 4(b,c)), showing that the router primarily detects unseen motions rather than unseen combinations. This familiarity-aware routing outperforms either predictor alone. 

## VI. EXPERIMENT 

## _D. Token-Familiarity Router_ 

Unlike conventional gates that directly predict or blend controller outputs, our TFR resolves disagreements between OpHRL and OpVQ-VAE using token-sequence familiarity. OpHRL captures execution-state feedback from composed sequences in _D_ Op, but cannot cover the combinatorial composition space, whereas OpVQ-VAE generalizes from causal motion tokens without observing the robot state. 

To select between these complementary predictors, we estimate familiarity using a lightweight causal _m_ -gram model fitted to tokens from _D_ trans (Sec. V-A), following likelihoodbased assessment of discrete representations [31], [32]. At each motion-reference frame _f_ , the causal motion window produces a token row _zf_ = ( _zf,_ 1 _, . . . , zf,L_ ). We concate= nate the most recent 32 rows in temporal order as _zf_<sup>flat</sup> ( _zf −_ 31 _, . . . , zf_ ) = ( _ζ_ 1 _, . . . , ζN_ tok), where _N_ tok = 32 _L_ . The router defaults to OpHRL until all 32 rows are available. Let _Gf_ contain the token positions with complete causal _m_ -gram contexts. Conditional probabilities use additive smoothing, _P_ train( _z | h_ ) = ( _C_ ( _h, z_ ) + 0 _._ 1) _/_ ( _C_ ( _h_ ) + 0 _._ 1 _K_ ), where _h_ is the preceding three-token context and _C_ denotes trainingtoken counts. We define the token negative log-likelihood score as 


We use _m_ = 4. Lower _uf_ indicates greater token-sequence familiarity. The raw window-NLL is smoothed as _u_ ¯ _f_ = _βuf_ + (1 _− β_ )¯ _uf −_ 1, with _β_ = 0 _._ 05. At each high-level decision, the router uses _u_ ¯ _ft_ , where _ft_ is the current motion-frame index. 

To evaluate BAT, we conduct extensive benchmark validation in simulation and demonstrate real-world deployment on hardware. We address the following key questions: (Q1) Does the proposed BAT identify higher-quality switching intervals and improve task performance relative to baselines? (Q2) How do option-aware representation learning and discrete quantization affect generalization to unseen motion combinations and unseen motions? (Q3) Does BAT achieve higher task success rates and more precise control than other whole-body control methods? (Q4) Does BAT generalize reliably across diverse scenarios when deployed on real hardware? 

## _A. Implementation Details and Experimental Setup_ 

_1) Training Details:_ We train the hierarchical RL switching policy using Discrete PPO within Isaac Gym via HumanoidVerse [33], implemented as a lightweight MLP. Training takes approximately 12–15 hours on an NVIDIA L40S GPU, initialized with behavioral cloning supervision that gradually decays toward RL to enable fast early convergence. Training datasets and switching supervision are constructed as described in Sec. V-A. 

_2) Simulation and Hardware Setup:_ Both IsaacGym [11] and MuJoCo [34] are utilized for offline policy evaluation, data construction, and evaluation process. The control frequency is 50 Hz with 200 Hz physics, and policy switching is performed at 5 Hz. On an Intel Core Ultra 9 285K CPU, the complete high-level decision pipeline takes 8.493 ms on average. For real-world validation, we deploy the policy on a Unitree G1 humanoid without additional tuning. Standard 

6 


Fig. 4: **Token familiarity resolves predictor disagreements by selecting OpHRL for familiar sequences and OpVQ-VAE for unfamiliar ones.** (a) Switching traces for a training chain (top) and a Test-U chain containing unseen motions (bottom). Highlighted regions show disagreements: BAT follows OpHRL when _gt_ = 1 (familiar) and OpVQ-VAE when _gt_ = 0 (unfamiliar). When both predictors agree, their common prediction is used. Dashed vertical lines mark motion-clip boundaries. (b) Moving-window token-NLL distributions for Train, Test-C (seen motions in unseen combinations), and Test-U (unseen motions in unseen combinations). The hysteresis thresholds _τ_ on = 1 _._ 75 and _τ_ off = 2 _._ 69 correspond to the 95th and 99.5th percentiles of the training EMA-smoothed window-NLL distribution. (c) Per-chain fractions of unfamiliar windows, with medians of 0.0%, 3.1%, and 62.1%, respectively, indicating that the router responds primarily to unseen motions. 

domain randomization is applied during training for sim-toreal transfer. The option-aware tokenizer operates on the 30 Hz motion-reference timeline. Each tokenization input is a causal window of _W_ = 16 motion frames, corresponding to 0 _._ 53 s. With 4 _×_ temporal downsampling, each window produces four VQ tokens. We generate one causal token row at each motion-reference frame, i.e., at 30 Hz. The raw familiarity score averages 4-gram token NLLs over the latest 32 causal token rows (1 _._ 07 s at 30 Hz) and is then EMA-smoothed with _β_ = 0 _._ 05 (we empirically observed that controller decisions were sensitive to 1- and 2-gram models but unchanged under the other tested settings). 

_3) Policy Switching Mechanism:_ Switching between independently trained controllers can introduce out-of-distribution histories and discontinuous targets, potentially destabilizing the robot. At each handoff, we preserve the robot state ( **q** _t,_ **q** ˙ _t_ ), reset the incoming policy’s histories and reference states, and warm-start its previous action from the current configuration. For the incoming target **q**<sup>+</sup> _t_<sup>,weinitialize</sup><sup>**e**</sup><sup>_q_(0)=</sup><sup>**q**</sup><sup>_t−_</sup><sup>**q**</sup> _t_<sup>+</sup> and decay it using **e** ¨ _q_ + _d_ **e** ˙ _q_ + _k_ **e** _q_ = 0, with _d_ = 2 _~~√~~ k_ . The corrected target **q** ˜ _t_ = **q**<sup>raw</sup> _t_ + **e** _q_ ( _t_ ) thereby smoothly converges from the current configuration to the incoming target. The same procedure is applied to velocity targets, while the policy- 

specific PD gains are smoothly blended during the transition. 

## _B. Simulation Experiments_ 

_1) Long-Horizon Switching and Generalization:_ We first evaluate BAT on sequential multi-motion tasks to address Q1 and Q2. We report success rate, cumulative reward using the same reward function as OpHRL, and the mean number of controller switches per episode. An episode is successful if the entire motion sequence is completed without falling. The comparison includes the following methods and ablations: 

- _Ablations:_ Standalone OpVQ-VAE (Sec. V-B) and OpHRL (Sec. V-C) evaluate the two switching predictors individually. VQ-VAE removes the option-prediction head during representation learning. Continuous Op-AE replaces the discrete tokens in OpVQ-VAE with continuous latent representations, keeping all other components unchanged. BC omits RL fine-tuning, while Vanilla HRL omits option-aware guidance. 

- _Baselines:_ Learned Gate, MoE, and Causal Transformer use motion references as input and are trained with supervision from _D_ Op. Learned Gate predicts the controller ID and uses the same handoff mechanism as BAT. MoE blends the two controllers’ outputs using learned mixture weights, while Causal Transformer predicts controller selection with a GPT-style autoregressive architecture [35]. Option-Critic [18] learns option selection and termination through policy-gradient optimization. 

- _Fixed policies:_ Decoupled and Coupled use one controller throughout each sequence. 

- _Offline oracle: D_ Op and _D_ trans oracles directly replay recorded switch timings, pre-evaluated for each motion chain through offline rollouts and stored as lookup tables. 

**Results.** As shown in Table I, BAT achieves the highest success rate among deployable methods across all three evaluation splits. OpHRL performs better than OpVQ-VAE on Train and Test-C, whereas OpVQ-VAE generalizes better to unseen motions in Test-U. Combining these complementary strengths, BAT exceeds both predictors in success rate across all splits. It also achieves the highest Train reward and ties with OpVQVAE on Test-U, although its Test-C reward is lower. 

The representation ablations highlight the value of optionaware discrete tokens for unseen motions. On Test-U, OpVQVAE achieves 70 _._ 6% success, compared with 49 _._ 4% for VQVAE and 61 _._ 9% for Continuous Op-AE. These results support the use of option-aware learning and discrete tokenization for generalization beyond the training motion repertoire. 

BAT achieves higher success and reward than all four switching baselines and both fixed controllers across all three splits. These results support combining complementary switching predictors and adapting controller selection to changing motion demands. The poor performance of Vanilla HRL further highlights the importance of option-aware guidance. 

_2) Single-Motion Control and Perturbation Robustness:_ We next evaluate single-motion execution to address Q3, 

7 

TABLE I: Performance comparison across three evaluation splits: **Train** (650 chains) uses seen motions in seen combinations, **Test-C** (70 chains) uses seen motions in unseen combinations, and **Test-U** (160 chains) uses unseen motions in unseen combinations. Mean Switches is reported as a diagnostic of switching frequency. Best and second-best distinct Success and Reward values across all methods, including offline oracles, are indicated by **bold** and <u>underlined</u> values, respectively; ties receive the same formatting. Offline oracles replay precomputed controller selections and do not guarantee successful execution. 

|||**S**|**uccess (%)**|_↑_||**Reward**|_↑_||**Mean Swit**|**ches**|
|---|---|---|---|---|---|---|---|---|---|---|
|**Category**|**Method**|**Train**|**Test-C**|**Test-U**|**Train**|**Test-C**|**Test-U **|**Train**|**Test-C**|**Test-U**|
|Ours|BAT|85.2|**70.0**|**71.3**|127.9|47.10|**115.5**|1.43|1.93|2.16|
||OpVQ-VAE|77.8|65.7|70.6|124.0|**58.88**|**115.5**|1.04|1.01|1.03|
||OpHRL|80.8|68.6|41.3|117.0|47.17|66.1|1.54|1.83|3.61|
|Abli|BC|71.8|62.9|40.6|107.0|57.34|66.1|2.39|2.21|3.84|
|atons|Continuous Op-AE|78.8|67.1|61.9|51.65|45.10|45.09|0.88|0.80|1.40|
||VQ-VAE|69.8|65.7|49.4|47.60|45.66|39.81|1.34|1.19|1.61|
||Vanilla HRL|0.0|0.0|0.0|-2.5|-2.55|-2.2|6.61|5.98|7.15|
||MoE|66.8|57.1|58.8|67.5|43.73|58.8|0.37|0.29|0.36|
|Bli|Learned Gate|66.8|47.1|36.9|107.7|38.10|60.5|0.37|0.10|0.12|
|asenes|Causal TF|50.2|45.7|39.4|79.9|36.61|64.8|0.21|0.19|0.06|
||Option-Critic|48.8|45.7|30.6|39.1|35.86|33.8|0.00|0.00|0.00|
||Decoupled|52.2|50.0|30.0|84.0|38.82|48.6|0.00|0.00|0.00|
|Fixed Policies|Coupled|29.2|28.6|23.8|47.7|24.50|39.9|0.00|0.00|0.00|
|OffliOl|_D_Op oracle|**86.5**|–|–|**151.6**|–|–|0.89|–|–|
|lne races|_D_trans oracle|82.8|68.6|69.4|143.2|57.74|112.5|0.89|0.86|0.94|


TABLE II: Comparison of motion tracking performance and perturbation robustness across diverse motions. BAT consistently selects the decoupled policy _πD_ for the standing and static motions used in the perturbation tests. 

|**Metric**|**GMT [3]**|**FALCON [1]**|**TWIST [6]**|**SONIC [4]**|**BAT (Ours)**|
|---|---|---|---|---|---|
|Success (_n_ / total)|7149 / 8261|7735 / 8261|7659 / 8261|7519 / 8261|**7901 / 8261**|
|Success Rate (%)|86.54|93.63|92.71|91.02|**95.64**|
|Mean Reward|0.6347|0.7677|0.8002|0.7343|**0.8468**|
|Upper-body tracking|0.8695|**0.9776**|0.9483|0.8858|0.9643|
|Lower-body tracking|0.8717|0.7522|**0.9081**|0.9040|0.8593|
|Critical Force — Forward (N)|80|190|180|_>_200|190|
|Critical Force — Lateral (N)|100|120|70|_>_200|120|
|Perturbation Success (_n_ / 40)|17 / 40|30 / 40|23 / 40|**40 / 40**|30 / 40|
|Perturbation Success Rate (%)|42.5|75.0|57.5|**100.0**|75.0|


comparing success, tracking quality, cumulative reward, and perturbation robustness across diverse motions. 

**Baselines.** We compare BAT with recent whole-body controllers: GMT [3], FALCON [1], TWIST [6], and SONIC [4]. FALCON represents modular decoupled control, whereas GMT, TWIST, and SONIC employ coupled whole-body motion imitation. 

**Results.** As shown in Table II, BAT achieves the highest success rate and mean reward. Since the mean reward jointly captures tracking, stability, and motion smoothness, this result demonstrates that BAT achieves a strong balance among these objectives. The fixed policies remain strongest in their specialized regimes: FALCON emphasizes precise upper-body control, whereas coupled policies provide stronger lower-body tracking during dynamic motions. Although BAT does not maximize every body-specific tracking metric independently, it avoids the sharp degradation of either specialist outside its preferred regime and maintains a more balanced overall performance through adaptive selection. Under external perturbations, BAT matches FALCON for second-best robustness behind SONIC, while retaining the highest overall success and reward. 


Fig. 5: Hardware deployment of BAT on the Unitree G1 humanoid. (a)–(d) Long-horizon sequences involving online switching between the decoupled policy _πD_ (blue) and coupled policy _πC_ (red). (e) Single-motion tasks with adaptive policy selection, where BAT automatically selects the more suitable low-level policy based on motion characteristics. 

## _C. Hardware Experiment_ 

To validate the effectiveness of BAT on real hardware (Q4), we deploy our method on the G1 humanoid platform. As 

8 

shown in Fig. 5, our approach enables successful execution of sequential tasks by switching between policies, allowing both dynamic and static motions to be performed within a unified framework. The hardware experiments cover diverse individual motions and sequences involving switching between different motions (see the supplementary video). We observed consistent switching across three repeated trials for each hardware demonstration. These results are qualitative demonstrations on a selected subset of motions, rather than a systematic hardware success-rate evaluation over the full repertoire. 

On hardware, motions with substantial low-level tracking degradation can destabilize switching by shifting OpHRL’s proprioceptive inputs. Distilling it into a reference-only switching policy may reduce this sensitivity. 

## VII. CONCLUSION 

We present BAT, an online policy-switching framework that combines coupled and decoupled controllers for wholebody humanoid control. OpHRL uses cross-simulator switchboundary guidance and closed-loop reinforcement learning to improve switching over BC and vanilla HRL, while OpVQVAE provides complementary generalization through optionaware discrete motion tokens. A token-familiarity router selects between the two predictors according to the familiarity of the current motion-token sequence. Simulation results show that BAT improves long-horizon task success by combining precise, robust decoupled control with agile whole-body control, and qualitative hardware experiments demonstrate zeroshot deployment on the Unitree G1. 

However, the framework lacks explicit environment and object-interaction awareness (e.g., perturbations, uneven terrain, or contact-rich manipulation), suggesting future work on perceptive and interaction-aware control. BAT is modular and can further benefit from stronger components. 

## REFERENCES 

- [1] Y. Zhang, Y. Yuan, P. Gurunath, T. He, S. Omidshafiei, A.-a. Aghamohammadi, M. Vazquez-Chanlatte, L. Pedersen, and G. Shi, “Falcon: Learning force-adaptive humanoid loco-manipulation,” _arXiv preprint arXiv:2505.06776_ , 2025. 

- [2] C. Lu, X. Cheng, J. Li, S. Yang, M. Ji, C. Yuan, G. Yang, S. Yi, and X. Wang, “Mobile-television: Predictive motion priors for humanoid whole-body control,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 5364–5371. 

- [3] Z. Chen, M. Ji, X. Cheng, X. Peng, X. B. Peng, and X. Wang, “Gmt: General motion tracking for humanoid whole-body control,” _arXiv preprint arXiv:2506.14770_ , 2025. 

- [4] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Castaneda, Z.-A. Cao, J. Li, D. Minor, Q. Ben _et al._ , “Sonic: Supersizing motion tracking for natural humanoid whole-body control,” _arXiv preprint arXiv:2511.07820_ , 2025. 

- [5] Y. Li, Z. Luo, T. Zhang, C. Dai, A. Kanervisto, A. Tirinzoni, H. Weng, K. Kitani, M. Guzek, A. Touati _et al._ , “Bfm-zero: A promptable behavioral foundation model for humanoid control using unsupervised reinforcement learning,” _arXiv preprint arXiv:2511.04131_ , 2025. 

- [6] Y. Ze, Z. Chen, J. P. Ara´ujo, Z.-a. Cao, X. B. Peng, J. Wu, and C. K. Liu, “Twist: Teleoperated whole-body imitation system,” _arXiv preprint arXiv:2505.02833_ , 2025. 

- [7] D. Baek, A. Purushottam, J. J. Choi, and J. Ramos, “Whole-body bilateral teleoperation with multi-stage object parameter estimation for wheeled humanoid locomanipulation,” _arXiv preprint arXiv:2508.09846_ , 2025. 

- [8] C. Khazoom, S. Hong, M. Chignoli, E. Stanger-Jones, and S. Kim, “Tailoring solution accuracy for fast whole-body model predictive control of legged robots,” _IEEE Robotics and Automation Letters (RA-L)_ , 2024. 

- [9] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black, “Amass: Archive of motion capture as surface shapes,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2019, pp. 5442–5451. 

- [10] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions On Graphics (TOG)_ , vol. 37, no. 4, pp. 1–14, 2018. 

- [11] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa _et al._ , “Isaac gym: High performance gpu-based physics simulation for robot learning,” _arXiv preprint arXiv:2108.10470_ , 2021. 

- [12] T. He, C. Zhang, W. Xiao, G. He, C. Liu, and G. Shi, “Agile but safe: Learning collision-free high-speed legged locomotion,” _arXiv preprint arXiv:2401.17583_ , 2024. 

- [13] D. Wang, X. Wang, X. Liu, J. Shi, Y. Zhao, C. Bai, and X. Li, “More: Mixture of residual experts for humanoid lifelike gaits learning on complex terrains,” _arXiv preprint arXiv:2506.08840_ , 2025. 

- [14] T. Nam, S.-H. Sun, K. Pertsch, S. J. Hwang, and J. J. Lim, “Skill-based meta-reinforcement learning,” _arXiv preprint arXiv:2204.11828_ , 2022. 

- [15] M. Colledanchise and P. Ogren,<sup>¨</sup> _Behavior Trees in Robotics and AI: An Introduction_ . CRC Press, 2018. 

- [16] J. Zhang and K. Cho, “Query-efficient imitation learning for end-to-end autonomous driving,” _arXiv preprint arXiv:1605.06450_ , 2016. 

- [17] T. G. Dietterich, “Hierarchical reinforcement learning with the MAXQ value function decomposition,” _Journal of Artificial Intelligence Research_ , vol. 13, pp. 227–303, 2000. 

- [18] P.-L. Bacon, J. Harb, and D. Precup, “The option-critic architecture,” in _Proceedings of the Thirty-First AAAI Conference on Artificial Intelligence_ , 2017, pp. 1726–1734. 

- [19] O. Nachum, S. Gu, H. Lee, and S. Levine, “Data-efficient hierarchical reinforcement learning,” in _Advances in Neural Information Processing Systems_ , vol. 31, 2018. [Online]. Available: https: //arxiv.org/abs/1805.08296 

- [20] T. Li, N. Lambert, R. Calandra, F. Meier, and A. Rai, “Learning generalizable locomotion skills with hierarchical reinforcement learning,” in _2020 IEEE International Conference on Robotics and Automation (ICRA)_ , 2020, pp. 413–419. 

- [21] W. Yu, F. Acero, V. Atanassov, C. Yang, I. Havoutis, D. Kanoulas, and Z. Li, “Discovery of skill-switching criteria for learning agile quadruped locomotion,” _Frontiers in Robotics and AI_ , vol. 13, p. 1697159, 2026. 

- [22] Y.-F. Lau, Q. Zhao, Y. Wang, R. Yu, H. W. Tsui, Q. Chen, and P. Tan, “Switch: Learning agile skills switching for humanoid robots,” _arXiv preprint arXiv:2604.14834_ , 2026. 

- [23] J. Ding, X. Chen, G. E. Katz, and Z. Gan, “Towards dynamic quadrupedal gaits: A symmetry-guided RL hierarchy enables free gait transitions at varying speeds,” _arXiv preprint arXiv:2403.10723v4_ , 2026. [Online]. Available: https://arxiv.org/abs/2403.10723v4 

- [24] H. Y. Ling, F. Zinno, G. Cheng, and M. van de Panne, “Character controllers using motion VAEs,” _ACM Transactions on Graphics_ , vol. 39, no. 4, 2020. 

- [25] J. Zhang, Y. Zhang, X. Cun, Y. Zhang, H. Zhao, H. Lu, X. Shen, and Y. Shan, “Generating human motion from textual descriptions with discrete representations,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023, pp. 14 730–14 740. 

- [26] C. Guo, Y. Mu, M. G. Javed, S. Wang, and L. Cheng, “Momask: Generative masked modeling of 3d human motions,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 1900–1910. 

- [27] I. Radosavovic, B. Zhang, B. Shi, J. Rajasegaran, S. Kamat, T. Darrell, K. Sreenath, and J. Malik, “Humanoid locomotion as next token prediction. arxiv 2024,” _arXiv preprint arXiv:2402.19469_ , 2024. 

- [28] R. S. Sutton, D. Precup, and S. Singh, “Between mdps and semi-mdps: A framework for temporal abstraction in reinforcement learning,” _Artificial Intelligence_ , 1999. 

- [29] B. Jiang, X. Chen, W. Liu, J. Yu, G. Yu, and T. Chen, “MotionGPT: Human motion as a foreign language,” in _Advances in Neural Information Processing Systems_ , vol. 36, 2023. [Online]. Available: https://arxiv.org/abs/2306.14795 

- [30] W. Kim, T. Li, and S. Ha, “MoReFlow: Motion retargeting learning through unsupervised flow matching,” _arXiv preprint arXiv:2509.25600_ , 2025. [Online]. Available: https://arxiv.org/abs/2509.25600 

- [31] A. van den Oord, O. Vinyals, and K. Kavukcuoglu, “Neural discrete representation learning,” _Advances in Neural Information Processing Systems_ , vol. 30, 2017. 

9 

- [32] S. N. Marimont and G. Tarroni, “Anomaly detection through latent space restoration using vector quantized variational autoencoders,” in _2021 IEEE 18th International Symposium on Biomedical Imaging (ISBI)_ . IEEE, 2021, pp. 1764–1767. 

- [33] C. L. Lab, “Humanoidverse: A multi-simulator framework for humanoid robot sim-to-real learning,” https://github.com/LeCAR-Lab/ HumanoidVerse, 2025. 

- [34] E. Todorov, T. Erez, and Y. Tassa, “Mujoco: A physics engine for modelbased control,” in _2012 IEEE/RSJ international conference on intelligent robots and systems_ . IEEE, 2012, pp. 5026–5033. 

- [35] A. Radford, K. Narasimhan, T. Salimans, and I. Sutskever, “Improving language understanding by generative pre-training,” _OpenAI_ , 2018. 

