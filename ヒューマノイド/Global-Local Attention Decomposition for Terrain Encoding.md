---
title: "Global-Local Attention Decomposition for Terrain Encoding in Humanoid Perceptive Locomotion"
date: "2026-05-30"
authors: "Shengcheng Fu; Yang Zhang; Zhanxiang Cao; Liyun Yan; Yizhi Chen; Yunpeng Yin"
url: https://arxiv.org/abs/2606.00637
pdf: https://arxiv.org/pdf/2606.00637
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.00637)** / [論文ページ](https://arxiv.org/abs/2606.00637)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Global-Local Attention Decomposition for Terrain Encoding in Humanoid Perceptive Locomotion** 

Shengcheng Fu<sup>1</sup><sup>_,_2</sup> , Yang Zhang<sup>3</sup> , Zhanxiang Cao<sup>3</sup><sup>_,_2</sup> , Liyun Yan<sup>3</sup><sup>_,_2</sup> , Yizhi Chen<sup>1</sup><sup>_,_2</sup> , Yunpeng Yin<sup>4</sup> , Yue Gao<sup>3</sup><sup>_,_2</sup><sup>_∗_</sup> 

> 1Tongji University, Shanghai, China 

> 2Shanghai Innovation Institute, Shanghai, China 

> 3Shanghai Jiao Tong University, Shanghai, China 

> 4Humanoid Robot (Shanghai) Co., Ltd., Shanghai, China 

> _∗_ Corresponding author: Yue Gao (email: yuegao@sjtu.edu.cn) 

**_Abstract_ —Although reinforcement learning has significantly advanced humanoid locomotion, perceptive policies still struggle on sparse-foothold terrain and constrained environments. Success in these scenarios requires both broad terrain awareness and precise foothold selection, two perceptual roles that conventional encoders often entangle. To address this challenge, we propose Global-Local Attention Decomposition (GLAD) for terrain encoding in humanoid locomotion. Realized by a coarse-to-fine encoder over a robot-centric elevation map, GLAD explicitly separates these objectives: a global attention branch uses attention pooling to summarize the surrounding terrain context, while a local attention branch sparsifies the local features by terrain saliency and applies state-conditioned attention to encode precise foothold-relevant geometry. This explicit attention decomposition prevents the dilution of fine-grained spatial cues while reducing training overhead. Experiments demonstrate that GLAD enables reliable locomotion over challenging gaps, stepping stones, and stairs. Furthermore, the learned policy exhibits emergent terrainresponsive behaviors, autonomously following narrow paths and avoiding obstacles under forward-velocity commands alone, without explicit navigation planners. In real-world deployment on a Unitree G1 humanoid robot using onboard LiDAR, the proposed method achieves robust zero-shot sim-to-real transfer across diverse sparse-foothold and obstacle-rich domains.** 

## I. INTRODUCTION 

Humanoid robots, owing to their anthropomorphic body plan and legged mobility, are promising platforms for operating in environments designed for humans and adapting to diverse terrain conditions [1], [2]. Reinforcement learning (RL) has recently driven substantial progress in humanoid locomotion, and even “blind” policies can now achieve robust walking over a wide range of ground conditions [3], [4]. Nevertheless, reliable locomotion on complex terrain remains challenging because the robot must simultaneously perceive surrounding geometry, make terrain-aware decisions, and maintain robust control under limited stability margins [5], [6]. This challenge becomes especially pronounced on sparsefoothold terrain, where success depends on identifying feasible support regions and placing the feet precisely [7]. 

To handle such terrains, perceptive locomotion policies must incorporate exteroceptive observations such as elevation maps or depth images. While essential, these raw observations are high-dimensional and noisy, which can reduce robustness, increase computational cost, and complicate policy training [8]. They therefore need to be encoded into compact terrain representations before being provided to the locomotion 


Fig. 1. Real-world locomotion results on the Unitree G1 humanoid robot. A single GLAD policy traverses sparse stepping stones, staircase–gap composite terrain, wide gaps up to 70 cm, and dense obstacle-rich terrain. 

controller. However, conventional terrain encoders typically treat perception as an isolated geometric compression task, largely ignoring the robot’s immediate kinematic state [9]. Because this encoding process lacks state awareness, it tends to dilute fine-grained geometric cues, weaken the spatial correspondence between encoded features and reachable foothold regions, and ultimately limit foothold precision in RL-based perceptive locomotion. 

This limitation is particularly problematic for sparsefoothold locomotion. To compensate for imprecise terrain representations, previous learning-based approaches often rely on terrain-specific curricula, expert policies, or handcrafted foothold rewards [10], [11], [12]. Although effective, these strategies inject strong human priors and can reduce generalization across varied terrain layouts. Attention mechanisms offer a principled way to fuse proprioception with exteroception: guided by the current motion state, they can emphasize locomotion-relevant terrain regions and thereby support general, interpretable terrain encoding [13]. Building on this idea, Attention-based Map Encoding (AME) [9] uses multi-head attention (MHA) to aggregate local terrain features conditioned on proprioception, enabling implicit and precise foothold selection; AME-2 [14] further augments this design with global terrain context, letting the attended region adapt to the terrain type and improving zero-shot generalization to mixed and unseen terrain. However, these existing attentionbased methods typically entangle multiple perceptual ob- 

jectives within a single attention mechanism. They do not explicitly separate the two essential perceptual roles required for perceptive locomotion: capturing broad surrounding terrain context and encoding precise foothold-relevant local geometry. 

To address this issue, we propose Global-Local Attention Decomposition (GLAD) for terrain encoding in humanoid locomotion. Realized by a coarse-to-fine encoder, GLAD explicitly separates the extraction of broad context from finegrained foothold selection. A convolutional neural network (CNN) first extracts spatially aligned local features from a robot-centric elevation map. Subsequently, a global attention branch uses attention pooling to summarize the surrounding terrain context, while a local attention branch sparsifies these features by terrain saliency and applies state-conditioned MHA to encode precise, foothold-relevant local regions. Without explicit attention supervision, these two branches learn complementary behaviors: the global attention focuses on key terrain regions ahead of the robot, whereas the local attention highlights foothold-relevant regions. Because the surrounding context is aggregated by a separate branch, the fine-grained local geometry is no longer diluted. 

Beyond sparse-foothold traversal, GLAD substantially enhances terrain-responsive locomotion in highly constrained environments. Guided solely by forward-velocity commands, the learned policy interprets terrain geometry to autonomously follow narrow paths and avoid nearby obstacles, exhibiting emergent local-navigation behaviors without requiring hierarchical planners. We validate GLAD in simulation and on a Unitree G1 humanoid robot, where it transfers zero-shot using only onboard LiDAR-based elevation mapping, as shown in Fig. 1. 

In summary, our main contributions are threefold: 

- We propose GLAD, a coarse-to-fine terrain encoder for humanoid locomotion that explicitly decomposes attention into global terrain-context aggregation and stateconditioned local foothold-relevant encoding. This design enables the policy to jointly reason about broad traversability cues and precise support-region geometry from robot-centric elevation maps. 

- We show that assigning surrounding-terrain aggregation to the global branch allows the local attention to concentrate more strongly on foothold-relevant terrain features and remain closely aligned with the realized footholds, yielding complementary and interpretable attention behaviors. Saliency-based local feature sparsification further reduces the cost of dense attention over the full terrain feature set. The resulting policy improves sparsefoothold traversal and terrain-responsive locomotion, including emergent narrow-path following without hierarchical planning. 

- We validate GLAD in both simulation and real-world deployment on a Unitree G1 humanoid robot. Using only onboard LiDAR-based elevation mapping, without premapping or external motion capture, the learned policy achieves robust zero-shot sim-to-real transfer across diverse sparse-foothold and obstacle-rich environments. 

## II. RELATED WORK 

## _A. Learning-based Humanoid Locomotion_ 

Recent advances in learning-based humanoid locomotion have been enabled in part by scalable training pipelines inherited from quadruped locomotion, which support massive simulation parallelization and reliable policy transfer to real robots [15]. With only proprioceptive sensing, “blind” policies can already achieve robust walking over uneven ground, simple obstacles, and external disturbances [3], [4]. For more challenging terrain, however, exteroceptive perception becomes increasingly important because the robot must anticipate hazards before contact and adapt its motion to surrounding geometry [16], [17], [18]. 

Existing perceptive locomotion methods mainly rely on depth images or elevation maps [19]. Depth images are appealing for deployment, but in learning-based pipelines they often require costly rendering or additional temporal modeling to compensate for occlusion and limited field of view [6], [11], [12]. Elevation maps provide a more structured robot-centric description of local terrain geometry and can be generated efficiently in simulation or constructed on hardware from depth cameras or LiDAR [5], [8], [10], [19], [20], [21]. For sparse-foothold locomotion tasks, elevation maps are still often needed as privileged information during training or as an intermediate representation in the depth-image pipeline, because they provide precise terrain geometry that is critical for accurate foothold reasoning [6], [12], [22]. 

## _B. Locomotion on Sparse Footholds_ 

Discrete terrains with sparse footholds highlight the mobility advantage of legged robots, but they are also among the most challenging settings for perceptive locomotion, especially for humanoids. Model-based methods explicitly plan feasible foothold sequences within hierarchical perception–planning– control pipelines, achieving precise motion on sparse supports but remaining limited by model accuracy and robustness to perception and control errors [23], [24]. End-to-end RL has become a dominant direction due to its robustness and strong real-world performance, yet accurate foothold placement on complex terrain remains difficult to guarantee. A key bottleneck is terrain encoding: encoders based on multilayer perceptrons (MLPs), CNNs and latent-variable models directly compress elevation maps or depth images, often overlooking the terrain details and motion-state relevance required for foothold decisions. Therefore, prior learning-based methods for sparse footholds often rely on terrain-specific curricula, expert policies, or carefully designed foothold rewards [7], [22], [10], [11], [12], which are difficult to engineer, inject strong human priors, and can bias policies toward conservative or terrain-specific foothold choices. 

State-conditioned attention offers a promising alternative for implicit foothold planning. By fusing proprioception with exteroceptive terrain features, attention can focus on regions most relevant to the current locomotion decision and provide a more precise, general terrain representation [13]. AME [9] applies MHA to local elevation-map features to obtain foothold-relevant focus without explicit foothold supervision. 


Fig. 2. Overview of the proposed Global-Local Attention Decomposition (GLAD) architecture. A CNN first extracts spatially aligned local features from a robot-centric elevation map. A global attention branch uses attention pooling to summarize the surrounding terrain context. This context is then fused with a proprioceptive embedding to form a state-conditioned query for MHA over saliency-sparsified local features, selectively encoding precise foothold-relevant geometry. The resulting explicitly decomposed representation is used by the locomotion policy for terrain-aware control. 

AME-2 [14] observes that a query built from proprioception alone carries no prior about the surrounding terrain, and therefore adds an MLP with global max pooling that injects global terrain context into both the attention query and the encoder output. The attended region can then adapt to the terrain type rather than to the robot state alone, which improves zero-shot generalization to mixed and unseen terrain while preserving agile motion. However, both methods still apply a single MHA module to the full local feature set, forcing one attention mechanism to handle both global context aggregation and concentrated foothold-relevant encoding. This coupling increases computational cost and can weaken attention concentration and interpretability, motivating terrain representations that explicitly separate global context aggregation from stateconditioned local encoding. 

## _B. Observation Space_ 

The policy network observes proprioceptive information and elevation map scans in the robot-centric base frame. The actor observation includes the base angular velocity _ωt_<sup>_b_,thegravitydirectionvector</sup><sup>_g_</sup> _t_<sup>_b_,thevelocitycommand</sup> _vt_<sup>cmd</sup> = [ _vx,t_<sup>cmd</sup><sup>_,v_</sup> _y,t_<sup>cmd</sup><sup>_,ω_</sup> _z,t_<sup>cmd],thejointpositions</sup><sup>_qt_,thejoint</sup> velocities _q_ ˙ _t_ , the previous action _at−_ 1, and an elevation map _mt_ surrounding the robot base. We denote the map scan as _mt ∈_ R<sup>_L×W ×_3</sup> , where _L_ and _W_ are the numbers of map cells along the length and width directions, and each grid cell stores 3D coordinates expressed in the robot base frame. 

The actor observation is written as 


## III. METHOD 

## _A. Problem Formulation_ 

We formulate humanoid perceptive locomotion as a partially observable Markov decision process (POMDP) 


where _S_ is the state space, _A_ is the action space, _O_ is the observation space, _p_ ( _st_ +1 _| st, at_ ) denotes the system dynamics, _r_ ( _st, at_ ) is the reward function, and _γ ∈_ (0 _,_ 1) is the discount factor. The process is partially observable due to limited sensor field-of-view and measurement noise. 

At time _t_ , the environment is in a latent state _st ∈S_ that captures both the robot state and the surrounding terrain. The policy receives an observation _ot ∈O_ composed of proprioceptive measurements and exteroceptive terrain perception (e.g., an elevation map), and outputs an action _at ∈A_ . The policy is parameterized by _θ_ and written as _at ∼ πθ_ ( _· | ot_ ). The learning objective is to maximize the expected discounted return 


The critic observes the same information but without noise, and additionally receives the base linear velocity _vt_<sup>_b_:</sup> 


_C. Action Space_ 

The action _at ∈A_ is a 29-dimensional vector corresponding to the 29 actuated joints of the humanoid robot. For stable policy outputs, we interpret _at_ as an offset added to a nominal standing joint configuration _θ_ stand. The target joint position is thus _θ_ target = _θ_ stand + _at_ . 

## _D. Global-Local Terrain Encoding_ 

As illustrated in Fig. 2, the elevation-map input is first processed by the proposed GLAD encoder to form a compact terrain representation. This representation is then concatenated with the proprioceptive input and fed into the policy network. 

_1) Spatially Aligned Local Feature Extraction:_ Given the input elevation map _mt ∈_ R<sup>_L×W ×_3</sup> , we first employ a twolayer CNN to extract spatially aligned local features. The 3D coordinates at each map location serve as the three input channels. Unlike AME [9], which convolves only the height values and then concatenates the original 3D coordinates with the CNN output to inject positional information, we directly convolve the 3D coordinates so that positional cues are embedded in the learned features from the beginning. 

Both convolutional layers use zero padding to preserve boundary information and maintain spatial alignment with the underlying terrain map. This spatial correspondence is important because the subsequent global and local attention modules should remain grounded to physical map locations. Without zero padding, the link between learned features and terrain locations becomes weaker, which negatively affects the final policy performance [9]. 

The first convolutional layer performs strided downsampling with a stride of _s_ . Unlike AME [9], which preserves a oneto-one correspondence between CNN features and the original scan points, our encoder decouples terrain sensing resolution from encoded feature resolution. The resulting features remain aligned with the original elevation map, but on a coarser grid of size _⌈L/s⌉×⌈W/s⌉_ . This design shortens the local feature sequence, reduces the computational cost of the subsequent attention modules, and allows higher-resolution elevation maps to be used as input while maintaining a similar encoded feature resolution for downstream processing. 

The second convolutional layer projects the downsampled features into a unified embedding dimension _D_ , which is shared by the proprioceptive embedding, the surrounding terrain context vector, and the MHA components. The CNN thus outputs a feature grid _F_ grid _∈_ R<sup>_⌈L/s⌉×⌈W/s⌉×D_</sup> . These local features encode both terrain geometry and positional information around each retained map location. This is important for foothold selection, since a feasible foothold depends not only on local terrain geometry but also on whether the corresponding location is reachable by the robot. 

_2) Global-Local Attention Decomposition:_ After local feature extraction, the GLAD terrain encoding is constructed in three steps: attention pooling aggregates all local features into a compact surrounding terrain context vector; a saliency score sparsifies the local features to a retained-feature budget of _K_ ; and the context is fused with a proprioceptive embedding to form a state-conditioned query that drives MHA over the retained features. 

Let _{ki}_<sup>_N_</sup> _i_ =1<sup>denotetheflattenedlocalterrainfeaturesex-</sup> tracted by the CNN, where _N_ = _⌈L/s⌉× ⌈W/s⌉_ is the sequence length and _ki ∈_ R<sup>_D_</sup> . To summarize the surrounding terrain information, we apply a linear layer to each local feature to produce a global-attention logit 


where _v_ and _bu_ are learnable parameters. The normalized global-attention weights are then computed as 


and the surrounding terrain context feature _c ∈_ R<sup>_D_</sup> is obtained by a weighted sum: 


This global branch summarizes the local terrain features into a compact representation of the surrounding terrain context. 

Because the local features already encode each cell’s position in the robot base frame, saliency can be assessed from the features themselves. The local branch therefore ranks the features by a learned saliency score 


where _w_ and _bs_ are learnable parameters. Whereas the global logits _ui_ are normalized into the weights forming _c_ , the scores _si_ act only through their ordering: we retain the top- _K_ local features and discard less salient regions. During training, Gumbel perturbations are applied to the scores, and straightthrough softmax weighting ( _τ_ = 1) propagates gradients through the discrete selection; inference uses deterministic hard top- _K_ selection. This coarse prefilter removes clearly irrelevant regions before the fine-grained attention stage. We then concatenate _c_ with the _D_ -dimensional proprioceptive embedding and project the result into a state-conditioned query vector _q ∈_ R<sup>_D_</sup> via a linear layer. The retained features are processed by MHA as key and value, using _q_ as the query, to yield the fine-grained, foothold-relevant feature _f ∈_ R<sup>_D_</sup> . 

Finally, the surrounding terrain context _c_ and the footholdrelevant feature _f_ are concatenated to form the unified terrain representation fed into the locomotion policy. In this way, global attention summarizes the surrounding terrain context, while local attention performs state-conditioned encoding over a sparse set of salient local regions. This explicit separation avoids the cost of applying MHA to the full terrain feature set, lowers training overhead, and improves the effectiveness and interpretability of the terrain representation for footholdrelated decision making. 

## IV. EXPERIMENTS 

## _A. Training and Experimental Setup_ 

_1) Baselines and Ablations:_ We compare GLAD with two terrain-encoder baselines and two ablations. AME [9], the primary attention-based baseline, applies state-conditioned MHA to CNN-extracted local terrain features. 

The second baseline, denoted as _AME with Global Context_ (AME-GC), adopts the global-context terrain-encoder design of AME-2 [14]. Specifically, an additional MLP followed by max pooling produces a global feature, which is concatenated with both the MHA query and the encoder output. AME-GC adapts only the relevant encoder design rather than reproducing the complete AME-2 system or its original training pipeline. 

Two ablations isolate the GLAD branches: _GLAD w/o global attention_ removes attention pooling but retains saliencybased sparsification and MHA, whereas _GLAD w/o local attention_ removes sparsification and MHA and retains only attention pooling. 


Fig. 3. Representative Stage-2 training terrains at the highest curriculum difficulty level. The terrain set includes sparse stepping stones, rails, gaps, and randomly distributed cylindrical obstacles. 

All methods use identical training settings, and corresponding components across methods are matched in architecture and hyperparameters; only their terrain-feature aggregation designs differ. 

_2) Network Hyperparameters:_ The actor and critic share the terrain encoder but use separate ELU-activated MLPs with hidden dimensions [512 _,_ 256 _,_ 128]. 

The terrain encoder receives a 1 _._ 6 m _×_ 1 _._ 0 m robot-centric elevation map at 0 _._ 05 m resolution ( _L_ = 33, _W_ = 21). Its twolayer CNN comprises a 3 _→_ 16 convolution (kernel 5, stride 2, padding 2) and a 16 _→_ 64 convolution (kernel 3, stride 1, padding 1), each followed by ReLU and batch normalization. The output is a 17 _×_ 11 grid with embedding dimension _D_ = 64 and flattened length _N_ = 187. 

Separate linear layers, without activation or normalization, project the 96-dimensional actor and 99-dimensional critic proprioceptive inputs to _D_ = 64. The single-layer MHA uses 16 heads, the standard output projection, and no dropout, additional layer normalization, or residual connections. 

AME, AME-GC, and GLAD use the same input definitions and identical settings for corresponding components. GLAD uses a retained-feature budget of _K_ = 32, while AMEGC adds an ELU-activated [256 _,_ 128] MLP followed by max pooling. 

_3) Training Details:_ All policies are trained in NVIDIA Isaac Sim using proximal policy optimization (PPO) [25] and a two-stage procedure following AME-based practice [9]. 

Stage 1 uses perfect terrain perception to initialize terrain encoding and basic locomotion. Its basic terrain set consists of stairs, random grids, random rough terrain, slopes, densely tiled stepping stones, and gaps. 

Stage 2 retains stairs and gaps but replaces densely tiled stepping stones with the harder parallel-row, single-row, and alternating stepping-stone layouts, and additionally introduces rails and randomly distributed cylindrical obstacles in Fig. 3. Observation noise and domain randomization are introduced mainly in this stage. 

Both stages use a ten-level curriculum that promotes successful robots and demotes failed ones. In both stages, ve- 


Fig. 4. Terrain-level curriculum progression during the two-stage training process for the proposed method and the two ablation variants. The full model reaches higher terrain levels earlier and exhibits the best convergence behavior. 

_∼_ locity commands are resampled every 10 s, with _vx_<sup>cmd</sup> _U_ (0 _,_ 1 _._ 5) m/s and _vy_<sup>cmd</sup> = 0. The yaw-rate command _ωz_<sup>cmd</sup> is not sampled directly but generated by a heading controller from the difference between a resampled target heading and the current base heading, and is clipped to [ _−_ 1 _,_ 1] rad/s. Each method is trained with 4096 parallel robots for 10 _,_ 000 learning iterations per stage. 

We use standard locomotion rewards without handcrafted foothold rewards or terrain-specific shaping. Generic randomization includes per-step observation noise, terrain-map scan drift, external pushes, torso-mass variation, and friction variation, with no encoder-specific tuning. This isolates the contribution of general terrain representations from terrainspecific priors. 

All training settings, including the PPO hyperparameters, are identical for GLAD, AME, AME-GC, and both ablations. All methods also share the same fixed random seed of 42, which controls network initialization, procedural terrain generation, simulator randomization, and PPO sampling. 

## _B. Training Efficiency and Convergence_ 

We first compare training performance through the terrainlevel curriculum progression shown in Fig. 4. The full model consistently reaches higher terrain levels earlier than both _GLAD w/o global attention_ and _GLAD w/o local attention_ , indicating that removing either branch slows convergence. This trend suggests that global and local attention not only improve final performance, but also jointly accelerate curriculum progression and improve convergence. 

We evaluate the computational efficiency during training on a single NVIDIA H200 GPU. Under the shared CNN strideddownsampling configuration described above, the proposed GLAD method requires only 1 _._ 00 day to complete the twostage training, compared with 1 _._ 36 days for AME and 1 _._ 50 days for AME-GC. This reduction emphasizes the efficiency advantage of our coarse-to-fine design, which avoids applying MHA to the full local feature set while retaining strong locomotion performance. 

We also analyze training time across retained-feature budgets _K_ . Relative to the 1 _._ 00 day of the default _K_ = 32, raising _K_ to 64 and 128 increases it to about 1 _._ 12 and 1 _._ 24 days, whereas _K_ = 16 saves little, at 0 _._ 98 days. As quantified 


Fig. 5. Illustration of the four test terrains used in simulation: a composite stepping-stone course, a random single-row stepping-stone course, irregular pentagonal pillars, and a sinusoidal narrow path. These terrains are designed to evaluate both precise foothold placement and terrain-responsive locomotion under different spatial constraints. 

TABLE I 

MEAN SUCCESS RATES (%) AND STANDARD DEVIATIONS OVER FIVE EVALUATION SEEDS ON THE FOUR SIMULATION TEST TERRAINS. 

|Method||Test T|errain||
|---|---|---|---|---|
||a|b|c|d|
|AME|93.99_±_2.04|94.77_±_1.23|81.72_±_3.22|53.67_±_3.98|
|AME-GC|95.90_±_0.62|92.58_±_1.45|70.23_±_4.20|81.13_±_3.70|
|GLAD w/o global attention|81.99_±_2.89|84.77_±_1.49|87.70_±_2.37|30.66_±_4.40|
|GLAD w/o local attention|93.36_±_0.57|94.53_±_1.77|71.95_±_5.03|49.69_±_3.67|
|GLAD|**96.64**_±_0.80|**97.03**_±_1.18|**92.42**_±_1.52|**93.48**_±_1.98|


in Section IV-C2, the learned local attention concentrates on only about four locations, so moderate budgets already provide ample capacity, and varying _K_ at inference has negligible influence on task performance over _K_ = 16–128, degrading only for much smaller budgets. Capacity alone would therefore permit a smaller _K_ . Early in training, however, the selection scores remain close to their random initialization, so the retained features form a nearly random subset and a smaller _K_ is correspondingly less likely to include a foothold-relevant location; this increased the learning difficulty and could prevent a stable foothold-aligned attention pattern from emerging. Since reducing _K_ to 16 yields only a marginal efficiency gain, we set _K_ = 32 as a conservative default balancing candidate capacity, learning stability, and computational efficiency. 

## _C. Simulation Experiments_ 

_1) Unseen Terrain Performance:_ Since all methods solve the training terrains reliably, we construct four more challenging long-horizon test terrains with unseen instances, each forming a 10 m course as shown in Fig. 5. Terrain (a) is a composite course that transitions from alternating double-row stepping stones to a single row, whereas Terrain (b) consists of a single row with random lateral offsets. The stepping stones in both terrains have 20 cm _×_ 20 cm top surfaces, providing sparse yet clearly defined support regions that primarily test precise foot placement. Terrain (c) comprises randomly distributed pentagonal pillars, whose cluttered arrangement makes feasible footholds more difficult to identify. Terrain (d) places pentagonal pillars along a sinusoidal path, requiring the robot to maintain precise footholds within a constrained support region while making substantial directional adjustments. For all four terrains, all robots are initialized facing the positive _x_ direction and receive a forward-velocity command only, with _vy_<sup>cmd</sup> = 0 and _ωz_<sup>cmd</sup> = 0. The commanded forward 

velocity is 1 _._ 0 m/s for Terrains (a) and (b) and 0 _._ 8 m/s for Terrains (c) and (d). Evaluation is repeated under five random seeds; for each terrain type and seed we generate 64 distinct terrain instances and test 512 robots in parallel. All methods use the same seeds, ensuring identical instances and matched simulator randomization. Table I reports the mean success rate and standard deviation. 

On stepping stones such as Terrains (a) and (b), most compared methods achieve mean success rates above 90%. However, _GLAD w/o global attention_ falls below 90%, confirming that relying solely on fine-grained foothold-relevant features is insufficient. The loss of surrounding terrain context degrades performance even on terrain layouts that are structurally similar to the training set. 

A larger performance gap emerges on Terrains (c) and (d). In Terrain (c), feasible support regions are more abundant, but their cluttered arrangement makes foothold planning and selection more challenging. The full GLAD model combines foothold-level precision with surrounding terrain context to maintain a success rate above 90%. By contrast, AME-GC performs noticeably worse, which may reflect the challenge of using a single MHA pathway to balance surrounding terrain context and precise foothold-relevant geometry. Similarly, _GLAD w/o local attention_ suffers a substantial performance drop, indicating that attention pooling alone cannot provide the fine-grained terrain representation required for precise foot placement in highly cluttered environments. Notably, _GLAD w/o global attention_ ranks second on this terrain, ahead of both baselines. Because feasible supports are densely and randomly distributed along the whole course, a nearby support is almost always available and the robot seldom needs to anticipate where the traversable region continues, so surrounding terrain context is least valuable here. This variant nevertheless remains clearly below the full model, and it collapses on Terrain (d), where the traversable region follows a curved path and sustained anticipation becomes essential. 

Terrain (d) represents the more demanding setting, requiring anticipatory directional adjustments prior to reaching infeasible regions. Under this scenario, GLAD continues to outperform the other methods. Although AME-GC performs better than AME, demonstrating the benefit of the introduced global terrain context, its remaining gap to GLAD suggests that simply fusing this information into the same attention pathway is insufficient. The ablation results show that removing the local attention branch fails to yield sharp foothold cues, while removing the global attention branch strips away the contextual forward traversability needed for sustained path following. These findings confirm that the surrounding terrain context feature _c_ and the foothold-relevant feature _f_ fulfill complementary roles. By explicitly decomposing them, GLAD avoids architectural entanglement and leads to more robust, terrain-responsive legged locomotion. 

_2) Attention–Foothold Alignment:_ To quantify whether local attention is both concentrated and aligned with actual footholds, we record the MHA attention weights at touchdown events and compare each attended local feature position _pi_ with the realized foothold position _pf_ . We report the following 


Fig. 6. Visualization of global and local attention weights of the proposed GLAD encoder. The displayed scan locations correspond to the spatially aligned local features, where yellow and red markers with higher intensity and larger size indicate larger global-attention and local-attention weights, respectively. 

TABLE II 

ATTENTION–FOOTHOLD METRICS OVER ALL TOUCHDOWN EVENTS ACROSS THE FOUR SIMULATION TEST TERRAIN TYPES. 

|Method|_D_attn _↓_|_D_peak _↓_|_A_peak _↑_|_H ↓_|_N_eq _↓_|
|---|---|---|---|---|---|
|GLAD (_K_ = 16)|0.120_±_0.057|0.103_±_0.057|0.539_±_0.163|1.248_±_0.416|3.77_±_1.40|
|GLAD (_K_ = 32)|0.118_±_0.055|0.104_±_0.059|0.537_±_0.163|1.259_±_0.421|3.82_±_1.42|
|GLAD (_K_ = 187)|0.120_±_0.059|0.104_±_0.062|0.534_±_0.166|1.266_±_0.436|3.87_±_1.55|
|AME|0.406_±_0.082|0.100_±_0.110|0.088_±_0.037|4.581_±_0.155|98.76_±_14.89|
|AME-GC|0.514_±_0.034|0.225_±_0.268|0.045_±_0.026|5.018_±_0.122|152.06_±_15.87|


where _αi_ is the MHA attention weight assigned to local feature _i_ , averaged across the 16 attention heads. _D_ attn is the attention-weighted foothold distance, _D_ peak and _A_ peak are the distance and weight of the most attended feature, and _H_ is the attention entropy. _N_ eq is the entropy-equivalent number of attended locations, i.e., the number of uniformly weighted locations that yields the same entropy; lower values indicate stronger concentration. Table II reports the mean and standard deviation of each metric over all touchdown events collected across the four terrain types in Fig. 5. Distances are in meters. All GLAD results use one policy trained with _K_ = 32, with _K_ varied only at inference. 

For the reported settings from _K_ = 16 to _K_ = 187, GLAD maintains _N_ eq _≈_ 4, even when all 187 features are retained, showing that its concentration is learned rather than imposed 

by Top- _K_ truncation. For a feature-count-matched comparison, GLAD ( _K_ = 187), AME, and AME-GC all attend over the same 187 features. Under this condition, GLAD yields substantially smaller _H_ and _N_ eq, indicating a markedly more concentrated distribution, together with a smaller attentionweighted foothold distance; it therefore concentrates its attention near the realized foothold rather than merely producing a sparse distribution. AME attains the smallest _D_ peak, so its most attended feature can also lie near the foothold; its much larger _D_ attn and _N_ eq, however, show that the remaining attention mass is spread over distant locations. By separating environment aggregation from foothold encoding, GLAD lets its MHA provide a clearer foothold cue. AME instead balances both roles in one MHA pathway, while AME-GC injects additional global context into the same pathway and exhibits an even more diffuse attention distribution. 

_3) Interpretable Attention Decomposition:_ To better understand the attention mechanism, we visualize the global and local attention weights across various terrain layouts in Fig. 6. The resulting distributions exhibit a distinct functional separation between the two branches. 

The global attention produces terrain-dependent, broadly receptive patterns. On flat ground, the weights lean toward the far end of the observation map. On stairs, gaps, and obstaclerich environments, the attention maintains distant awareness while increasingly highlighting geometric edges with significant height variations. On more constrained terrains, such as stepping stones and narrow paths, it concentrates on nearby forward-traversable regions. This adaptability demonstrates that the surrounding terrain context feature _c_ effectively captures anticipatory cues regarding upcoming geometric changes and forward traversability. 

Conversely, the local attention yields highly concentrated spatial patterns. Guided by the learned saliency scores, the retained local features concentrate primarily on near-field 

feasible foothold regions. The subsequent MHA weights typically peak near the robot’s current or next foothold locations. This highly localized behavior confirms that the fine-grained, foothold-relevant feature _f_ directly provides the spatial geometry required for precise foot placement. 

## _D. Real-world Deployment_ 

We deploy the proposed method on a Unitree G1 humanoid robot. The robot weighs 35 kg, stands 1 _._ 32 m tall, and has 29 actuated degrees of freedom. For exteroceptive perception, it is equipped with a Livox Mid-360 LiDAR that provides point clouds together with synchronized inertial measurement unit (IMU) measurements. 

For deployment, we use FAST-LIO [26] to fuse LiDAR and IMU measurements for state estimation, and construct a robotcentric gridded elevation map from the fused point cloud [27]. Invalid cells do not occur in simulation, while real-world map holes caused by LiDAR occlusion are filled using neighboring valid elevations before policy inference. The system runs on a laptop equipped with an RTX 5090 Laptop GPU, where both the elevation-mapping module and the control policy operate at 50 Hz. 

As shown in Fig. 1, we test four representative realworld terrains: alternating stepping stones with top surfaces measuring 20 cm _×_ 25 cm and 70 cm spacing between sameside stones; a composite staircase with 30 cm treads, 12 cm risers, and a 30 cm gap between its ascending and descending segments; a 70 cm wide gap, exceeding the maximum training gap of 50 cm and approaching the forward sensing limit; and an obstacle-rich route containing wooden blocks and suitcases. 

Each method is tested five times per terrain under the same protocol; success requires course completion without falling or human intervention. GLAD completes 19 of 20 trials, succeeding in all stair, gap, and obstacle trials and in four of five on the alternating stepping stones; AMEGC and AME reach 19 and 18 of 20 under the same protocol. All failures occur on the alternating stepping stones, where LiDAR mixed-pixel artifacts at depth discontinuities blur elevation-map boundaries and can make adjacent stones appear connected, commonly limiting success across methods. Because the available physical courses are shorter and less constrained than the long-horizon simulation tests, they exhibit a ceiling effect that limits their ability to distinguish the terrain encoders. These tests therefore primarily validate zero-shot transfer and deployability, while the long-horizon simulation tests provide the main encoder comparison. 

## V. CONCLUSIONS 

We presented GLAD, a coarse-to-fine terrain encoder that separates global context aggregation from state-conditioned local foothold encoding. This decomposition reduces attention entanglement and computational cost while producing interpretable, foothold-aligned attention. Simulation demonstrated robust locomotion on challenging long-horizon test terrains, while deployment on a Unitree G1 verified zeroshot transfer across sparse footholds, wide gaps, and obstaclerich environments. Current limitations include the map’s local 

sensing range, reconstruction artifacts, and real-time mapping cost. Future work will investigate more efficient, temporally extended, and multi-scale perception. 

## REFERENCES 

- [1] Z. Wu, K. Zheng, Z. Ding, and H. Gao, “A survey on legged robots: Advances, technologies and applications,” _Engineering Applications of Artificial Intelligence_ , vol. 138, p. 109418, 2024. 

- [2] Y. Tong, H. Liu, and Z. Zhang, “Advancements in humanoid robots: A comprehensive review and future prospects,” _IEEE/CAA Journal of Automatica Sinica_ , vol. 11, no. 2, pp. 301–328, 2024. 

- [3] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath, “Real-world humanoid locomotion with reinforcement learning,” _Science Robotics_ , vol. 9, no. 89, p. eadi9579, 2024. 

- [4] I. Radosavovic, S. Kamat, T. Darrell, and J. Malik, “Learning humanoid locomotion over challenging terrain,” _arXiv preprint arXiv:2410.03654_ , 2024. 

- [5] H. Duan, B. Pandit, M. S. Gadde, B. Van Marum, J. Dao, C. Kim, and A. Fern, “Learning vision-based bipedal locomotion for challenging terrain,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 56–62. 

- [6] M. S. Gadde, P. Dugar, A. Malik, and A. Fern, “No more blind spots: Learning vision-based omnidirectional bipedal locomotion for challenging terrain,” in _2025 IEEE-RAS 24th International Conference on Humanoid Robots (Humanoids)_ . IEEE, 2025, pp. 601–608. 

- [7] C. Zhang, N. Rudin, D. Hoeller, and M. Hutter, “Learning agile locomotion on risky terrains,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 11 864–11 871. 

- [8] J. Long, J. Ren, M. Shi, Z. Wang, T. Huang, P. Luo, and J. Pang, “Learning humanoid locomotion with perceptive internal model,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 9997–10 003. 

- [9] J. He, C. Zhang, F. Jenelten, R. Grandia, M. B¨acher, and M. Hutter, “Attention-based map encoding for learning generalized legged locomotion,” _Science Robotics_ , vol. 10, no. 105, p. eadv3604, 2025. 

- [10] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang, “Beamdojo: Learning agile humanoid locomotion on sparse footholds,” _arXiv preprint arXiv:2502.10363_ , 2025. 

- [11] S. Zhu, Z. Zhuang, M. Zhao, K.-Y. Lee, and H. Zhao, “Hiking in the wild: A scalable perceptive parkour framework for humanoids,” _arXiv preprint arXiv:2601.07718_ , 2026. 

- [12] Y. Zhang, Y. Seo, J. Chen, Y. Yuan, K. Sreenath, P. Abbeel, C. Sferrazza, K. Liu, R. Duan, and G. Shi, “Rpl: Learning robust humanoid perceptive locomotion on challenging terrains,” _arXiv preprint arXiv:2602.03002_ , 2026. 

- [13] R. Yang, M. Zhang, N. Hansen, H. Xu, and X. Wang, “Learning visionguided quadrupedal locomotion end-to-end with cross-modal transformers,” _arXiv preprint arXiv:2107.03996_ , 2021. 

- [14] C. Zhang, V. Klemm, F. Yang, and M. Hutter, “Ame-2: Agile and generalized legged locomotion via attention-based neural map encoding,” _arXiv preprint arXiv:2601.08485_ , 2026. 

- [15] N. Rudin, D. Hoeller, P. Reist, and M. Hutter, “Learning to walk in minutes using massively parallel deep reinforcement learning,” in _Conference on Robot Learning_ . PMLR, 2022, pp. 91–100. 

- [16] A. Roychoudhury, S. Khorshidi, S. Agrawal, and M. Bennewitz, “Perception for humanoid robots,” _Current Robotics Reports_ , vol. 4, no. 4, pp. 127–140, 2023. 

- [17] C. R. de Lima, S. G. Khan, M. Tufail, S. H. Shah, and M. R. Maximo, “Humanoid robot motion planning approaches: a survey,” _Journal of Intelligent & Robotic Systems_ , vol. 110, no. 2, p. 86, 2024. 

- [18] S. Luo, S. Li, R. Yu, Z. Wang, J. Wu, and Q. Zhu, “Pie: Parkour with implicit-explicit learning framework for legged robots,” _IEEE Robotics and Automation Letters_ , 2024. 

- [19] J. Sun, G. Han, P. Sun, W. Zhao, J. Cao, J. Wang, Y. Guo, and Q. Zhang, “Dpl: Depth-only perceptive humanoid locomotion via realistic depth synthesis and cross-attention terrain reconstruction,” _arXiv preprint arXiv:2510.07152_ , 2025. 

- [20] W. Sun, B. Cao, L. Chen, Y. Su, Y. Liu, Z. Xie, and H. Liu, “Learning perceptive humanoid locomotion over challenging terrain,” _arXiv preprint arXiv:2503.00692_ , 2025. 

- [21] H. Song, H. Zhu, T. Yu, Y. Liu, M. Yuan, W. Zhou, H. Chen, and H. Li, “Gait-adaptive perceptive humanoid locomotion with real-time underbase terrain reconstruction,” _arXiv preprint arXiv:2512.07464_ , 2025. 

- [22] R. Yu, Q. Wang, Y. Wang, Z. Wang, J. Wu, and Q. Zhu, “Walking with terrain reconstruction: Learning to traverse risky sparse footholds,” _arXiv preprint arXiv:2409.15692_ , 2024. 

- [23] F. Jenelten, R. Grandia, F. Farshidian, and M. Hutter, “Tamols: Terrainaware motion optimization for legged systems,” _IEEE Transactions on Robotics_ , vol. 38, no. 6, pp. 3395–3413, 2022. 

- [24] R. Grandia, F. Jenelten, S. Yang, F. Farshidian, and M. Hutter, “Perceptive locomotion through nonlinear model-predictive control,” _IEEE Transactions on Robotics_ , vol. 39, no. 5, pp. 3402–3421, 2023. 

- [25] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

- [26] W. Xu and F. Zhang, “Fast-lio: A fast, robust lidar-inertial odometry package by tightly-coupled iterated kalman filter,” _IEEE Robotics and Automation Letters_ , vol. 6, no. 2, pp. 3317–3324, 2021. 

- [27] T. Miki, L. Wellhausen, R. Grandia, F. Jenelten, T. Homberger, and M. Hutter, “Elevation mapping for locomotion and navigation using gpu,” in _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2022, pp. 2273–2280. 

