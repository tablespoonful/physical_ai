---
title: "TAGA: Terrain-aware Active Gaze Learning for Generalizable Agile Humanoid Locomotion"
date: "2026-06-04"
authors: "Peizhuo Li; Hongyi Li; Mingfeng Fan; Yutong Wang; Yifeng Zhang; Fangzhou Xu"
url: https://arxiv.org/abs/2606.05880
pdf: https://arxiv.org/pdf/2606.05880
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.05880)** / [論文ページ](https://arxiv.org/abs/2606.05880)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **TAGA: Terrain-aware Active Gaze Learning for Generalizable Agile Humanoid Locomotion** 

**LI Peizhuo**<sup>**1,***</sup> **, Hongyi LI**<sup>**2,***</sup> **, Mingfeng FAN**<sup>**1,***</sup> **, Yutong WANG**<sup>**1**</sup> **, Yifeng ZHANG**<sup>**1**</sup> **, Fangzhou XU**<sup>**1**</sup> **, Dapeng JIA**<sup>**1**</sup> **, Shuhao LIAO**<sup>**1**</sup> **, Yuxuan MA**<sup>**1**</sup> **, Zicheng ZENG**<sup>**3**</sup> **, Ze WANG**<sup>**2**</sup> **, Yongbin JIN**<sup>**2,**</sup><sup>_†_</sup> **, Yuhong CAO**<sup>**1,**</sup><sup>_†_</sup> **, Armin LEDERER**<sup>**4**</sup> **, Hongtao WANG**<sup>**2**</sup> **, Guillaume SARTORETTI**<sup>**1**</sup> 1MarmotLab, National University of Singapore 2Center of X-Mechanics, Zhejiang University 

3South China University of Technology 

4Department of Electrical and Computer Engineering, National University of Singapore 

*Equal contribution _†_ Corresponding authors Project Page: `https://marmotlab.github.io/taga-humanoid/` 


Figure 1: TAGA enables agile and robust humanoid locomotion across diverse challenging terrains. Deployed on a Unitree G1 with onboard Jetson Orin inference, the robot traverses up to 1 _._ 2 m gaps, narrow beams, sparse stepping stones, stairs, and outdoor terrain. TAGA uses egocentric vision and proprioception to predict task-relevant regions in the height scan, selectively routing these local terrain observations to the downstream locomotion policy, while remaining robust to severe perceptual disturbances and environmental interference. 

**Abstract:** Agile humanoid locomotion across diverse challenging terrain demands both wide perceptual coverage and precise local geometry understanding. Motivated by the way humans selectively look at relevant terrain during locomotion, we introduce TAGA, a Terrain-aware Active Gaze learning framework for Attention-based humanoid control. By fusing vision, proprioception, and motion commands, our framework guides the model to learn anticipatory cues and actively attend to specific areas of the height scan, selectively using these informative regions for the downstream network. This adaptively increases the information density of observations under tight onboard computational constraints, thus enabling fine-grained perceptive locomotion over larger-scale terrains. We find that such gaze behaviors can naturally emerge through reinforcement learning alone, without requiring additional supervision or explicit guidance, significantly improving training efficiency. As a result, the trained policy demonstrates robust and generalizable locomotion in simulation and on hardware, including reliable terrain-aware foothold selection, elevated-platform traversal, competitive sparsefoothold traversal, and the largest reported real-world gap traversal distance of 

1 _._ 2 m among perceptive humanoid locomotion systems, while maintaining stability under severe perceptual disturbances and environmental interference. 

**Keywords:** Humanoid Locomotion, Gaze Mechanism, Multimodal Perception 

## **1 Introduction** 

Humanoids have shown significant advantages over wheeled robots in crossing obstacles, traversing discontinuous terrain, and navigating complex spatial structures. While recent motion-tracking methods enable dynamic whole-body behaviors such as dancing, backflips, and human-motion imitation [1, 2, 3, 4, 5, 6, 7], tracking predefined motions is fundamentally different from locomotion in complex terrain, from cluttered indoor scenes to unstructured outdoor landscapes. The former resembles reproducing a memorized trajectory, whereas the latter requires the robot to actively perceive its surroundings, reason about terrain traversability, and adapt its motion strategy in real time [8]. This makes perception a central bottleneck: the robot must obtain look-ahead awareness of upcoming terrain while retaining precise local geometry for reliable foothold placement. 

Existing perceptive locomotion methods can generally be divided into two categories: mapping-based methods and vision-based methods. Mapping-based approaches use point clouds or reconstructed height scans as compact terrain representations for locomotion [8, 9, 10, 11]. While effective, these methods often incur increasing computational cost as the perception range expands. In contrast, vision-based methods directly map raw depth images to actions, reducing reliance on explicit terrain reconstruction [12, 13, 14, 15, 16]. However, forward-facing depth images often miss the terrain near or beneath the robot’s feet, and recurrent memory struggles to preserve finegrained geometry over long horizons [17]. 


Figure 2: Comparison between local height scan and depth image perception. 

These two perceptual paradigms actually provide complementary information. As shown in Fig. 2, vision offers look-ahead awareness of distant terrain, while a height scan provides accurate local geometry for foot placement and contact-rich motion control. However, many existing approaches either rely on a single source or couple the two only loosely. As a result, they fail to fully exploit the complementary strengths of multimodal perception and cannot effectively align look-ahead visual cues with local geometric details. In contrast, humans and animals actively direct their gaze toward task-relevant regions, such as nearby footholds, gaps, or distant obstacles, based on the situation. This suggests that robust humanoid locomotion requires not only multimodal perception, but also an active perception mechanism for deciding _where to look_ and _which perceived information matters most for the next step(s)_ . 

To this end, we propose **TAGA** , an active perception framework for generalizable agile humanoid locomotion. TAGA is built around a hierarchical gaze mechanism: vision provides long-range terrain preview, height scans supply precise local geometry, and a learned active gaze policy selectively attends to the most locomotion-relevant regions, adaptively fusing these complementary signals. Concretely, TAGA consists of two core components. A _Task-Relevant Active Gaze Module_ fuses vision, proprioception, and motion commands to predict which terrain region is most relevant for the next movement and crops the corresponding patch from the height scan. A _Visuomotor Fusion Encoder_ then applies cross-attention over this selected region, emphasizing geometric structures critical for foothold placement and terrain-aware decision making. This hierarchical design increases the effective information density of observations, reduces interference from irrelevant terrain, and simplifies downstream policy learning. The main contributions of this work are summarized as follows: 

2 

1. We present TAGA, a perceptive locomotion system that integrates depth vision, height scan, and proprioception into a unified sensing and control pipeline for humanoids operating in challenging terrain with onboard computation, while improving training efficiency over full-context. 

2. At the core of TAGA is an emergent hierarchical active gaze mechanism learned without explicit gaze supervision: the policy learns to select a task-relevant terrain patch via visual and proprioceptive cues, then applies fine-grained attention to that region for precise understanding. 

3. We deployed TAGA on Unitree G1 and demonstrated state-of-the-art (SOTA) performance across gaps, stepping stones, narrow beams, stairs, and outdoor terrain. Notably, the robot achieves a 120 cm gap crossing, surpassing the best reported result by 50%. 

## **2 Related Works** 

**Terrain Mapping-Based Perceptive Locomotion.** A major class of perceptive locomotion methods relies on explicit geometric terrain representations such as height scans, elevation maps, or voxel grids to guide locomotion policies [18, 19, 20, 21]. These approaches generally achieve strong local terrain awareness and precise foothold placement in challenging tasks such as stepping stones, sparse footholds, and gap traversal [22, 23]. Recent methods further improve terrain understanding through learned geometric encodings, including multi-layer height scans [24], 3D terrain representations [25], and Attention-Based Map Encoding (AME) [8]. However, mapping-based approaches are usually constrained by the size and resolution of the terrain representation, which limits the tradeoff between local detail and broader terrain coverage [24, 25]. Their performance also depends on map quality and can degrade under localization uncertainty, occlusions, or deficient perception [26]. 

**Vision-Based Perceptive Locomotion under Partial Observations.** Vision-based methods reduce reliance on explicit mapping by learning policies from depth images, RGB-D inputs, or egocentric vision [13, 27, 28]. They have enabled agile locomotion across sparse footholds, discontinuous terrains, complex obstacle traversal, and humanoid stepping tasks [12, 29, 30], with recent humanoid-oriented works further improving performance through internal models, depth reconstruction, voxel-grid navigation, and limited-view omnidirectional control [10, 31, 32]. However, these policies often encode terrain reasoning implicitly [15, 28] and remain vulnerable to partial observability, especially when forward-facing sensors miss underfoot geometry needed for sparse foothold placement [33, 34]. Recent methods address this issue using memory or reconstruction, including implicit-explicit learning, visuospatial or volumetric memory, world-model perception, spatial recurrent memory, neural scene representations, sparse-terrain reconstruction, and diffusion-based occupancy synthesis [35, 36, 37, 38, 39, 40]. Nevertheless, they can still suffer from viewpoint changes, motion uncertainty, and drift between stored terrain representations and the robot’s current pose, particularly when latent memory lacks explicit geometric constraints [41, 42]. 

**Active Perception for Locomotion.** Recent studies suggest that robust locomotion depends not only on perceiving the environment, but also on selecting task-relevant terrain regions during traversal. Prior attention-based locomotion methods have shown that selective terrain encoding and exteroceptive–proprioceptive fusion can improve robustness and generalization [8], while Crossmodal Transformers integrate visual and proprioceptive representations for terrain reasoning [15]. More recent adaptive perception methods, such as ADAPT, mainly improve perception robustness by adaptively clipping noisy observations and suppressing perception noise [43], while CART selects relevant temporal context for terrain adaptation [44]. Nevertheless, most existing methods still emphasize short-horizon terrain reasoning, while proactive allocation of perception across both nearby footholds and future terrain structures remains underexplored. 

3 


Figure 3: The architecture of TAGA. 

## **3 TAGA Framework** 

### **3.1 Problem Formulation** 

We formulate humanoid perceptive locomotion as a partially observable Markov decision process (POMDP; see Appendix A). The policy _π_ ( _at|ot_ ) maps the observation _ot_ = _{p_<sup>_H_</sup> _t_<sup>_, dt, h_</sup> _t_<sup>_xyz_</sup> _}_ to an action _at ∈_ R<sup>29</sup> representing target joint positions, where _dt ∈_ R<sup>1</sup><sup>_×_36</sup><sup>_×_64</sup> is a forward-facing depth image and _h_<sup>_xyz_</sup> _t ∈_ R<sup>3</sup><sup>_×_21</sup><sup>_×_21</sup> is a local height scan. The proprioceptive input is a 5-frame history _p_<sup>_H_</sup> _t_ = _{pt−_ 4 _, . . . , pt}_ , where each frame is _pt_ = _{ωb,t, gb,t, qt, q_ ˙ _t, at−_ 1 _, ct}_ . Here, _ωb,t ∈_ R<sup>3</sup> is the measured torso angular velocity, _gb,t ∈_ R<sup>3</sup> is the projected gravity vector, _qt, q_ ˙ _t ∈_ R<sup>29</sup> are joint positions and velocities, and _at−_ 1 _∈_ R<sup>29</sup> is the previous action. The command _ct_ = ( _vx,t_<sup>cmd</sup><sup>_, v_</sup> _y,t_<sup>cmd</sup><sup>_,ψ_˙</sup> _t_<sup>cmd</sup> ) _∈_ R<sup>3</sup> specifies the desired forward velocity, lateral velocity, and yaw rate. 

### **3.2 Neural Network Design** 

**Overview.** As shown in Fig. 3, the TAGA policy _π_ ( _at|ot_ ) is parameterized by a neural network that takes the multimodal observation _ot_ as input and outputs a vector action _at_ . TAGA first encodes the depth image _dt_ and proprioception history _p_<sup>_H_</sup> _t_<sup>using a CNN-based depth encoder</sup><sup>_ϕd_and an MLP-</sup> based proprioception encoder _ϕp_ , producing a visual embedding _et_<sup>_d∈_R128andaproprioceptive</sup> embedding _e_<sup>_p_</sup> _t_<sup>_∈_R128, respectively.The visual embedding captures distant terrain awareness, while</sup> the proprioceptive embedding encodes the robot’s dynamic state and command context. Given these embeddings and the height scan _h_<sup>_xyz_</sup> _t_ , TAGA employs a hierarchical gaze mechanism to extract locomotion-relevant terrain information. The first stage, the _task-relevant active gaze module_ , predicts a region of interest (ROI) in the height scan. The second stage, the _visuomotor fusion encoder_ , further emphasizes terrain cues relevant to the next locomotion decision by producing a fusion embedding _e_<sup>_pg_</sup> _t_ based on the cropped ROI. Finally, a mixture-of-experts (MoE) based _action decoder_ maps the fusion embedding _e_<sup>_pg_</sup> _t_ and proprioceptive embedding _e_<sup>_p_</sup> _t_<sup>to the action output</sup><sup>_at_.This de-</sup> sign enables vision and proprioception to guide where the robot should look, while height scans provide precise local geometry, thereby supporting terrain-aware agile locomotion. 

**Task-Relevant Active Gaze Module.** TAGA enables a robot to actively focus its gaze on the ROI via the task-relevant active gaze module. Conditioning on visual preview and proprioceptive state, this module filters irrelevant terrain and directs perception to the most informative region for the next locomotion step. Concretely, a lightweight prediction head _f_ roi takes the visual and proprioceptive embeddings as input and predicts a normalized two-dimensional gaze location: _rt_ = _f_ roi([ _e_<sup>_d_</sup> _t_<sup>_, e_</sup> _t_<sup>_p_])</sup><sup>_, rt∈_[0</sup><sup>_,_1]2.The predicted location is then mapped onto the full local height-scan grid</sup> and used to crop a compact terrain patch: _h_<sup>˜</sup><sup>_xyz_</sup> _t_ = Crop( _h_<sup>_xyz_</sup> _t , rt_ ) _, h_<sup>˜</sup><sup>_xyz_</sup> _t ∈_ R<sup>3</sup><sup>_×K×K_</sup> , where _K_ = 11 denotes the crop size. The crop is implemented using differentiable bilinear grid sampling, allowing this module to be optimized end-to-end with the policy. To discourage degenerate solutions near the height-scan boundary, we apply a boundary penalty _L_ roi (detailed in Appendix D). 

**Visuomotor Fusion Encoder.** TAGA further identifies which perceived information is most relevant through the visuomotor fusion encoder. Given the cropped patch _h_<sup>˜</sup><sup>_xyz_</sup> _t_ , the encoder first extracts terrain features using a lightweight CNN, while the corresponding spatial coordinates 

4 

are embedded by an MLP. These features are then fused to obtain pointwise terrain embeddings _Et_<sup>_m_</sup> _∈_ R<sup>_K×K×_128</sup> , which serve as the key and value vectors. Meanwhile, the query vector is generated from the visual and proprioceptive embeddings through a projection head _fproj_ . Finally, the visuomotor fusion encoder applies a multi-head cross-attention layer to obtain the fusion embedding: _e_<sup>_pg_</sup> _t_ = MHA� _fproj_ ([ _et_<sup>_p, ed_</sup> _t_<sup>])</sup><sup>_, E_</sup> _t_<sup>_m, E_</sup> _t_<sup>_m_</sup> �. The resulting embedding _e_<sup>_pg_</sup> _t ∈_ R<sup>128</sup> forms a terrain-aware visuomotor representation for downstream action decoding. **Action Decoder.** The action decoder is implemented as an MoE module [45] to increase policy expressiveness through adaptive action composition. The actor receives the proprioceptive embedding _e_<sup>_p_</sup> _t_<sup>andthefusionembedding</sup><sup>_epg_</sup> _t_ as _e_<sup>_π_</sup> _t_<sup>=[</sup><sup>_e_</sup> _t_<sup>_p, epg_</sup> _t_<sup>].Agatingnetwork</sup><sup>_g_(</sup><sup>_·_)computessoftexpert</sup> weights _αt_<sup>_i_=Softmax(</sup><sup>_g_(</sup><sup>_eπ_</sup> _t_<sup>))</sup><sup>_i, i_=1</sup><sup>_, . . . , Ne_,andthefinalactionisgivenbyaweightedcom-</sup> bination of expert outputs: _at_ =<sup>�</sup> _i_<sup>_N_</sup> =1<sup>_eα_</sup> _t_<sup>_iEi_(</sup><sup>_eπ_</sup> _t_<sup>),where</sup><sup>_Ei_denotesthe</sup><sup>_i_-thexpertand</sup><sup>_Ne_=5in</sup> our implementation. Through soft routing, all experts contribute to action generation with inputdependent weights. This allows the decoder to adaptively compose expert outputs based on TAGA’s task-relevant perceptual and proprioceptive embeddings, improving policy expressiveness for diverse locomotion conditions. 

## **4 Training TAGA Policy via Reinforcement Learning** 

We train TAGA using asymmetric actor-critic PPO in massively parallel simulation [46]. The actor is described in Sec.3.2, while the critic additionally receives privileged information, including the ground-truth base linear velocity and the full uncropped height scan. We support progressive policy learning over risky terrains by constructing multiple terrain types with increasing difficulty and training the policy using curriculum learning. AMP-style regularization and safety-oriented termination further encourage natural gait and stable control. A two-stage training procedure improves both skill acquisition and hardware robustness. Finally, we define the full training objective with symmetry augmentation[47] (detailed in Appendix D). 

**Terrain Design and Curriculum.** We design a training terrain set composed of multiple challenging terrain types and train TAGA across these environments. This terrain set covers representative traversal skills, including gap crossing, stair climbing, sparse-foothold traversal, narrow-beam walking, obstacle crossing, and slope locomotion (details in Appendix C.1), allowing the robot to acquire a broad set of terrain-adaptive locomotion behaviors. Each terrain type is divided into 10 difficulty levels by varying geometric parameters such as gap width, step height, and foothold size. During training, each robot is assigned to a terrain level according to its locomotion performance: successful traversal promotes it to harder terrains, while failure moves it back to easier ones. 

**Task Reward and Safety Constraints.** The base task reward _rt_<sup>env</sup> combines command tracking, posture and joint regularization, and contact-related terms (detailed in Appendix C.2). An AMPstyle reward _rt_<sup>AMP</sup> is added to encourage human-like gait, produced by a discriminator trained to distinguish policy motions from motion capture data [48]. We use retargeted AMASS [49] motions as the reference distribution. Since extreme agile locomotion may encourage unstable policies, we apply early termination on physically unsafe states, including illegal non-foot-body contacts, excessive torso tilt, insufficient base height, and abnormally large hip-link acceleration during foot contact. These termination conditions serve as hard safety boundaries, filtering out irrecoverable failure cases and focusing learning on stable, feasible locomotion. 

**Two-stage Training.** Following AME [8], we use a two-stage procedure to balance skill acquisition and real-world robustness. In the first stage, the policy is trained in a clean setting without observation noise or domain randomization, allowing the robot to acquire core locomotion skills efficiently. Starting from this checkpoint, the second stage fine-tunes the policy with reduced entropy and deployment-oriented randomization, including actuation variations, visual degradation, heightscan noise, external pushes, and terrain perturbations. This improves robustness to noisy real-world sensing and dynamics while preserving the learned active gaze behavior of TAGA. 

5 

Table 1: Comparison of TAGA with baseline methods and ablation variants across challenging terrain types. We report GPU count, total training cost in GPU-days, and success rates. Each method is evaluated over 1000 trials per terrain when applicable. Bold indicates the best success rate in each terrain column and results within 0.5% of the best. 

|**Method**|**# GPUs**_↓_|**GPU-days**_↓_|**Gaps**_↑_|**Stepping Stones**_↑_|**Beam**_↑_|**High Platform**_↑_|**Terrain C1**_↑_|**Terrain C2**_↑_|
|---|---|---|---|---|---|---|---|---|
|CReF [51]|2|_∼_10|97.40%|52.30%|96.50%|98.70%|85.20%|43.10%|
|TAGA-HSOnly|4|_∼_17|93.10%|92.50%|**98.30%**|**99.60%**|90.50%|91.50%|
|TAGA-InactiveGaze|4|_∼_14|57.10%|83.20%|95.60%|**100.00%**|72.70%|48.80%|
|TAGA-FullScan|8|_∼_49|**99.50%**|**98.00%**|97.50%|**100.00%**|**93.40**%|92.50%|
|TAGA-NoAMP|4|_∼_16|96.40%|97.20%|97.60%|**99.50%**|89.80%|91.60%|
|**TAGA (Ours)**|4|_∼_17|98.30%|**97.90%**|**98.50%**|**100.00%**|**93.70%**|**93.90%**|


**Loss Function.** Two auxiliary objectives regularize the learned representations: a contrastive loss _L_ con aligning MoE gating latents with full height-scan context to encourage expert specialization [45], and a gaze boundary penalty _L_ roi preventing TAGA from degenerately fixating on heightmap edges. Putting everything together, the full training objective combines the PPO surrogate loss on the augmented reward ˜ _r_ = _rt_<sup>_env_</sup> + _ηrt_<sup>_AMP_</sup> with a value loss _L_ value, an entropy bonus _H_ ( _πθ_ ), and the auxiliary terms: 


where _η_ is the AMP reward coefficient, and _cv_ , _ce_ , _λc_ , and _λb_ are loss weights. 

## **5 Experiments** 

We train TAGA in Isaac Lab [50] with 8,000 parallel environments on four NVIDIA GeForce RTX 5090 GPUs. The policy is trained over 30k iterations, and then fine-tuned for 10k iterations, requiring about 17 RTX-5090 GPU-days in total. It executes actions at 50 Hz, tracked by a low-level 200 Hz PD controller. Details are provided in Appendix C.3. For real-world experiments, TAGA is deployed on a Unitree G1 humanoid robot with onboard inference on an NVIDIA Jetson Orin. A Livox Mid-360 LiDAR and DLIO provide the local elevation map from which height scans are extracted. 

### **5.1 Simulation Evaluation** 

We first evaluate TAGA in simulation, where terrain conditions and sensing ablations can be controlled systematically. The goal is to characterize its locomotion capability and robustness before real-world deployment. Specifically, we study three questions: **_Q1:_** What is the complementary nature of the information provided by visual preview and height scans during challenging terrain traversal? **_Q2:_** What are the advantages of our gaze module dynamically selecting task-relevant terrain regions instead of processing the full height scan? **_Q3:_** Do AMP priors improve motion naturalness, whole-body coordination, and dynamic stability? We conduct a comprehensive ablation study for TAGA and compare it with a vision-based baseline. **TAGA-HSOnly** removes depth input and uses only height scans with proprioception. **TAGA-InactiveGaze** deactivates the Gaze Module and uses a fixed ROI. **TAGA-FullScan** removes the Gaze module and processes the full height scan with the same attention-based map encoder. TAGA, TAGA-InactiveGaze, and TAGA-FullScan share the same raw scan; TAGA and TAGA-InactiveGaze use equally sized 11 _×_ 11 ROIs. **TAGANoAMP** removes AMP priors. Since TAGA is designed around local height-scan selection, directly removing height scans would yield an ill-matched vision-only baseline. Instead, we compare TAGA with **CReF** [51], a vision-based humanoid locomotion method. 

**Multimodal Perception (Q1).** Comparing TAGA with CReF and TAGA-HSOnly highlights the complementary roles of visual preview and height scans. TAGA matches or surpasses the visionbased CReF on gaps, beams, and high platforms, and substantially outperforms it on stepping stones (Table 1). This suggests vision alone is insufficient for sparse footholds, where precise foot placement demands accurate local geometry. In contrast, TAGA-HSOnly, which relies solely on height scans and proprioception, struggles with gaps. This indicates that height-scan-only perception lacks sufficient preview to anticipate distant discontinuities and landing regions. Together, these results support the complementary roles of vision and height scans: vision provides anticipatory preview, 

6 


Figure 4: Visualization of the learned active gaze regions and attention-weight distributions of TAGA in simulation. Black points denote the full local height-scan grid, while colored points indicate the predicted ROI. Red and blue points indicate higher and lower attention weights, respectively. (a) shows how the active gaze regions shift during a 1 _._ 2 m gap crossing, and (b) demonstrates attention shifts across diverse terrains. (c) illustrates out-of-distribution testing terrains from training 

while height scans provide local geometric precision for robust terrain traversal. Under OOD (out of distribution) terrain challenges (C1, C2), TAGA achieves 93 _._ 70% and 93 _._ 90%, demonstrating stronger robustness and generalization across diverse terrain combinations. 

**Gaze Module (Q2).** We assess the effectiveness of our gaze module through visualization (Fig. 4) and ablation (Table 1). Instead of using a fixed crop, TAGA predicts task-relevant regions guided by fused visual and proprioceptive cues. During gap crossing, the gaze shifts from the current support region forward to the opposite edge as the robot prepares to cross, resembling the anticipatory gaze behavior observed in humans and animals during locomotion (Fig. 4(a)). On stepping stones and beams, it moves toward sparse footholds or the traversable strip; on continuous terrains, the robot’s gaze remains local, to cover nearby height changes and contact regions (Fig. 4 (b)). In our ablations, TAGA achieves performance comparable to TAGA-FullScan with 65.2% lower training cost than TAGA-FullScan. TAGA-InactiveGaze, with the same compact input but a fixed crop, degrades sharply on gaps and stepping stones where distant footholds lie outside its window. 

**Motion Prior (Q3).** Removing the AMP priors does not substantially hurt task completion, with TAGA-NoAMP performing close to TAGA across all terrains (Table 1). However, Fig. 5 shows a clear drop in motion quality. Without AMP, the robot exhibits unnatural motions, including inward knee collapse and short, shuffling steps, especially during turning and terrain transitions. These high-frequency foot motions also made real-world deployment brittle: TAGA-NoAMP proves far less robust to sim-to-real gap and small disturbances. 


Figure 5: Robot stance without AMP. Without motion guidance, the robot constantly walk with its leg bent. 

### **5.2 Real-World Evaluation** 

We further evaluate our policy in real-world environments of increasing complexity, moving from controlled indoor trials with designed challenging terrains to outdoor tests involving perception degradation, terrain variation, and physical disturbances. Table 2 compares TAGA with reported real-world perceptive humanoid and biped locomotion methods, while Fig. 1 and Fig. 6 show representative indoor and outdoor trials. TAGA covers the widest range of real-world terrain categories among currently reported methods: it **achieves the largest gap-crossing distance** and can traverse sparse-foothold areas, significantly outperforming previous reported SOTA results on both metrics. 

7 


Figure 6: Real-world evaluation of TAGA from controlled indoor terrains to unstructured outdoor environments. **(A)** Indoor trials test limit traversal over discontinuous terrains such as platform transitions, large steps, and sparse stepping blocks. **(B)** Outdoor trials evaluate robustness to terrain variation, perception degradation, and external disturbances. Our results show that TAGA maintains stable locomotion across discrete foothold selection, terrain variation, and physical perturbations. 

Our Vel Tracking AME-2 reproduction adapts the velocity-command interface while retaining the original network structure and terrain-map resolution. We extend the original biped scan’s forward coverage to include the opposite gap edge and landing region before takeoff on long gaps, avoiding a comparison limited by unavailable terrain observations. 

Table 2: Real-world traversal capabilities reported in perceptive humanoid and biped locomotion works. n.r.indicates that the behavior was demonstrated but the terrain geometry was not numerically reported; –indicates that the behavior was not evaluated. Bold and underline indicate the best and second-best results, respectively. 

|**Work**|**Robot**|**Gap**|**Platform**|**Sparse foothold**|**Beam**|**Stairs**|
|---|---|---|---|---|---|---|
|HPL [16]|Unitree H1|**80 cm**|42 cm|–|✗|✗|
|PIM [10]|Unitree H1|70 cm|**50 cm**|–|✗|✓|
|GA-PHL [14]|LimX Oli|46 cm|–|–|✗|✓|
|AME-1 [8]|Fourier GR-1|n.r.|–|n.r., uneven|✓|✓|
|AME-2 [17]|LimX Tron1|60 cm|**48 cm**|40 cmspacing, uneven|✓|✓|
|Vel Tracking AME-2|Unitree G1|90 cm|40 cm|40 cm, uneven|✓|✓|
|Now You See That [52]|Honor|45 cm|40 cm|–|✗|✓|
|BeamDojo [29]|Unitree G1|50 cm|–|45 cmspacing, flat|✓|✗|
|MoRE [53]|Unitree G1|40 cm|30 cm|–|✗|✓|
|Hiking in the Wild [54]|Unitree G1|50 cm|32 cm|–|✗|✗|
|Gallant [32]|Unitree G1|40 cm|30 cm|–|✗|✓|
|CReF [51]|Agibot X2|80 cm|40 cm|–|✗|✓|
|RPL [55]|Unitree G1|–|–|60 cmspacing, flat|✗|✓|
|CMoE [45]|Unitree G1|80 cm|30 cm|–|✗|✓|
|**Ours**|Unitree G1|**120 cm**|40 cm|**70 cm spacing, uneven**|✓|✓|


**Indoor Evaluation.** Across five hardware trials per terrain, TAGA succeeds in 5/5 trials on stairs, high platforms, narrow beams, and 0 _._ 8 _/_ 1 _._ 0 m gaps, and 4/5 trials on stepping stones and 1 _._ 2 m gaps. As shown in Fig. 6 **(A)** , we evaluate TAGA on highly discontinuous indoor terrains with only sparse, separated footholds—long gaps, narrow blocks, and stepping stones—where the robot must carefully plan its footholds and generate sufficient momentum between contacts. TAGA handles these near-limit conditions, crossing 120 cm gaps, balancing on narrow footholds, and traversing sparse blocks with 50–70 cm spacing and 10 cm height variation. Beyond these metrics, TAGA exhibits emergent terrain-adaptive behaviors. When crossing long gaps (Fig. 6 **(A2)** ), the robot steps onto the block edge and pushes off for extra momentum rather than taking off from the center of the support region. Upon landing, it bends its knees to absorb impact and quickly recovers balance. These strategies emerge without any hand-crafted motion, indicating that TAGA learns practical locomotion skills for challenging discrete terrains. 

**Outdoor Evaluation.** We further evaluate TAGA in outdoor and low-light environments (Fig. 1 and Fig. 6 ), which introduce varied ground materials and challenging perception conditions, including changing illumination, background clutter, depth degradation, sensor noise, as well as occluded footholds in tall grass and confined spaces. Despite these challenges, the robot maintains stable lo- 

8 

comotion across terrain types, demonstrating robustness to real-world perception noise and contact variations. Under external disturbances such as kicks and pushes, TAGA absorbs the perturbations, recovers balance, and continues walking without falling. These results indicate that TAGA learns a robust terrain-aware control strategy effective under both perceptual uncertainty and physical disturbances, enabling reliable real-world deployment. 

## **6 Conclusion** 

We presented TAGA, a terrain-aware active gaze framework for agile humanoid locomotion. TAGA improves traversability across gaps, narrow beams, stairs, elevated platforms, and sparse stepping stones in both simulation and real-world experiments. The learned gaze behavior emerges without explicit supervision, and hardware deployment demonstrates stable locomotion under low-light conditions and strong external disturbances. By fusing vision, proprioception, and motion commands, TAGA selectively attends to task-relevant terrain regions, combining look-ahead visual with local geometric precision for anticipatory, terrain-aware decision-making. 

## **7 Limitations** 

The dynamic maneuvers that TAGA achieves, including explosive jump, precise foothold targeting, and dynamic balance recovery, exert a high thermal load on the actuators during extended operation. This can progressively let actuators overheat, gradually damaging control accuracy and causing reduced jump distance or missed footholds. Additionally, poor height scan quality on complex terrain can cause improper gaits or failures. Future directions include improving tolerance to actuator degradation through online adaptation, better height scan reconstruction, and incorporating uncertainty-aware control to maintain precise foothold selection under degraded hardware and sensing conditions. 

9 

## **References** 

- [1] M. Sombolestan and Q. Nguyen. Adaptive-force-based control of dynamic legged locomotion over uneven terrain. _IEEE Transactions on Robotics_ , 40:2462–2477, 2024. 

- [2] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang. Homie: Humanoid loco-manipulation with isomorphic exoskeleton cockpit. _arXiv preprint arXiv:2502.13013_ , 2025. 

- [3] Y. Zhang, Y. Yuan, P. Gurunath, I. Gupta, S. Omidshafiei, A.-a. Agha-mohammadi, M. Vazquez-Chanlatte, L. Pedersen, T. He, and G. Shi. Falcon: Learning force-adaptive humanoid loco-manipulation. _arXiv preprint arXiv:2505.06776_ , 2025. 

- [4] N. Fey, G. B. Margolis, M. Peticco, and P. Agrawal. Bridging the sim-to-real gap for athletic loco-manipulation. _arXiv preprint arXiv:2502.10894_ , 2025. 

- [5] M. Murooka, K. Chappellet, A. Tanguy, M. Benallegue, I. Kumagai, M. Morisawa, F. Kanehiro, and A. Kheddar. Humanoid loco-manipulations pattern generation and stabilization control. _IEEE Robotics and Automation Letters_ , 6(3):5597–5604, 2021. 

- [6] K. Bouyarmane, K. Chappellet, J. Vaillant, and A. Kheddar. Quadratic programming for multirobot and task-space force control. _IEEE Transactions on Robotics_ , 35(1):64–77, 2018. 

- [7] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn. Humanplus: Humanoid shadowing and imitation from humans. _arXiv preprint arXiv:2406.10454_ , 2024. 

- [8] J. He, C. Zhang, F. Jenelten, R. Grandia, M. B¨acher, and M. Hutter. Attention-based map encoding for learning generalized legged locomotion. _Science Robotics_ , 10(105):eadv3604, 2025. 

- [9] T. Miki, J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter. Learning robust perceptive locomotion for quadrupedal robots in the wild. _Science Robotics_ , 7(62):eabk2822, 2022. 

- [10] J. Long, J. Ren, M. Shi, Z. Wang, T. Huang, P. Luo, and J. Pang. Learning humanoid locomotion with perceptive internal model. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9997–10003. IEEE, 2025. 

- [11] D. Hoeller, N. Rudin, D. Sako, and M. Hutter. Anymal parkour: Learning agile navigation for quadrupedal robots. _Science Robotics_ , 9(88):eadi7566, 2024. 

- [12] X. Cheng, K. Shi, A. Agarwal, and D. Pathak. Extreme parkour with legged robots. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11443–11450. IEEE, 2024. 

- [13] A. Agarwal, A. Kumar, J. Malik, and D. Pathak. Legged locomotion in challenging terrains using egocentric vision. In _Conference on robot learning_ , pages 403–415. PMLR, 2023. 

- [14] H. Song, H. Zhu, T. Yu, Y. Liu, M. Yuan, W. Zhou, H. Chen, and H. Li. Gait-adaptive perceptive humanoid locomotion with real-time under-base terrain reconstruction. _IEEE Robotics and Automation Letters_ , 2026. 

- [15] R. Yang, M. Zhang, N. Hansen, H. Xu, and X. Wang. Learning vision-guided quadrupedal locomotion end-to-end with cross-modal transformers. In _International Conference on Learning Representations_ , 2022. URL `https://openreview.net/forum?id=kFdPX1VdgXx` . 

- [16] Z. Zhuang, S. Yao, and H. Zhao. Humanoid parkour learning. In _8th Conference on Robot Learning_ , 2024. URL `https://openreview.net/forum?id=fs7ia3FqUM` . 

- [17] C. Zhang, V. Klemm, F. Yang, and M. Hutter. Ame-2: Agile and generalized legged locomotion via attention-based neural map encoding. _arXiv preprint arXiv:2601.08485_ , 2026. 

10 

- [18] P. Fankhauser, M. Bjelonic, C. D. Bellicoso, T. Miki, and M. Hutter. Robust rough-terrain locomotion with a quadrupedal robot. In _2018 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5761–5768. IEEE, 2018. 

- [19] F. Jenelten, T. Miki, A. E. Vijayan, M. Bjelonic, and M. Hutter. Perceptive locomotion in rough terrain–online foothold optimization. _IEEE Robotics and Automation Letters_ , 5(4):5370–5376, 2020. 

- [20] Z. Wang, Y. Li, L. Xu, H. Shi, Z. Ma, Z. Chu, C. Li, F. Gao, K. Yang, and K. Wang. Sf-tim: A simple framework for enhancing quadrupedal robot jumping agility by combining terrain imagination and measurement. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 10676–10683. IEEE, 2025. 

- [21] T. Miki, L. Wellhausen, R. Grandia, F. Jenelten, T. Homberger, and M. Hutter. Elevation mapping for locomotion and navigation using gpu. In _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 2273–2280. IEEE, 2022. 

- [22] Y. Dong, J. Ma, L. Zhao, W. Li, and P. Lu. Marg: Mastering risky gap terrains for legged robots with elevation mapping. _IEEE Transactions on Robotics_ , 2025. 

- [23] C. Zhang, N. Rudin, D. Hoeller, and M. Hutter. Learning agile locomotion on risky terrains. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 11864–11871. IEEE, 2024. 

- [24] Y. Chen, J. Ma, Z. Luo, Y. Han, Y. Dong, B. Xu, and P. Lu. Learning autonomous and safe quadruped traversal of complex terrains using multi-layer elevation maps. _IEEE Robotics and Automation Letters_ , 2025. 

- [25] T. Miki, J. Lee, L. Wellhausen, and M. Hutter. Learning to walk in confined spaces using 3d representation. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 8649–8656. IEEE, 2024. 

- [26] P. Fankhauser, M. Bloesch, and M. Hutter. Probabilistic terrain mapping for mobile robots with uncertain localization. _IEEE Robotics and Automation Letters_ , 3(4):3019–3026, 2018. 

- [27] W. Yu, D. Jain, A. Escontrela, A. Iscen, P. Xu, E. Coumans, S. Ha, J. Tan, and T. Zhang. Visuallocomotion: Learning to walk on complex terrains with vision. In _5th Annual Conference on Robot Learning_ , 2021. 

- [28] H. Duan, B. Pandit, M. S. Gadde, B. Van Marum, J. Dao, C. Kim, and A. Fern. Learning visionbased bipedal locomotion for challenging terrain. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 56–62. IEEE, 2024. 

- [29] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang. Beamdojo: Learning agile humanoid locomotion on sparse footholds. _arXiv preprint arXiv:2502.10363_ , 2025. 

- [30] N. Rudin, J. He, J. Aurand, and M. Hutter. Parkour in the wild: Learning a general and extensible agile locomotion policy using multi-expert distillation and rl fine-tuning. _arXiv preprint arXiv:2505.11164_ , 2025. 

- [31] J. Sun, G. Han, P. Sun, W. Zhao, J. Cao, J. Wang, Y. Guo, and Q. Zhang. Dpl: Depthonly perceptive humanoid locomotion via realistic depth synthesis and cross-attention terrain reconstruction. _arXiv preprint arXiv:2510.07152_ , 2025. 

- [32] Q. Ben, B. Xu, K. Li, F. Jia, W. Zhang, J. Wang, J. Wang, D. Lin, and J. Pang. Gallant: Voxel grid-based humanoid locomotion and local-navigation across 3d constrained terrains. _arXiv preprint arXiv:2511.14625_ , 2025. 

11 

- [33] S. Li, S. Luo, J. Wu, and Q. Zhu. Move: Multi-skill omnidirectional legged locomotion with limited view in 3d environments. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 7647–7653. IEEE, 2025. 

- [34] P. Li, H. Li, Y. Ma, L. Chang, X. Yang, R. Yu, Y. Zhang, Y. Cao, Q. Zhu, and G. Sartoretti. Kivi: Kinesthetic-visuospatial integration for dynamic and safe egocentric legged locomotion. _arXiv preprint arXiv:2509.23650_ , 2025. 

- [35] S. Luo, S. Li, R. Yu, Z. Wang, J. Wu, and Q. Zhu. Pie: Parkour with implicit-explicit learning framework for legged robots. _IEEE Robotics and Automation Letters_ , 9(11):9986–9993, 2024. 

- [36] R. Yang, G. Yang, and X. Wang. Neural volumetric memory for visual locomotion control. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 1430–1440, 2023. 

- [37] H. Lai, J. Cao, J. Xu, H. Wu, Y. Lin, T. Kong, Y. Yu, and W. Zhang. World model-based perception for visual legged locomotion. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11531–11537. IEEE, 2025. 

- [38] C. Zhang, J. Jin, J. Frey, N. Rudin, M. Mattamala, C. Cadena, and M. Hutter. Resilient legged local navigation: Learning to traverse with compromised perception end-to-end. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 34–41. IEEE, 2024. 

- [39] D. Hoeller, N. Rudin, C. Choy, A. Anandkumar, and M. Hutter. Neural scene representation for locomotion on structured terrain. _IEEE Robotics and Automation Letters_ , 7(4):8667–8674, 2022. 

- [40] R. Yu, Q. Wang, H. Li, Z. Jun, Z. Wang, J. Wu, and Q. Zhu. Start: Traversing sparse footholds with terrain reconstruction. _IEEE Robotics and Automation Letters_ , 11(2):2194–2201, 2025. 

- [41] F. Yang, P. Frivik, D. Hoeller, C. Wang, C. Cadena, and M. Hutter. Spatially-enhanced recurrent memory for long-range mapless navigation via end-to-end reinforcement learning. _The International Journal of Robotics Research_ , page 02783649251401926, 2025. 

- [42] A. Reed, B. Crowe, D. Albin, L. Achey, B. Hayes, and C. Heckman. Scenesense: Diffusion models for 3d occupancy synthesis from partial observation. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 7383–7390. IEEE, 2024. 

- [43] S. Shao, T. Huang, W. Gao, and S. Zhang. Adapt: Adaptive dual-projection architecture for perceptive traversal. _arXiv preprint arXiv:2603.16328_ , 2026. 

- [44] K. Singh, Y. Kim, Y. Turkar, and K. Dantu. Cart: Context-aware terrain adaptation using temporal sequence selection for legged robots. _arXiv preprint arXiv:2604.14344_ , 2026. 

- [45] S. Ma, H. Chen, Z. Xu, Y. Zhao, K. Wu, R. Yang, L. Zou, Z. Gan, and W. Ding. Cmoe: Contrastive mixture of experts for motion control and terrain adaptation of humanoid robots. _arXiv preprint arXiv:2603.03067_ , 2026. 

- [46] C. Schwarke, M. Mittal, N. Rudin, D. Hoeller, and M. Hutter. Rsl-rl: A learning library for robotics research. _arXiv preprint arXiv:2509.10771_ , 2025. 

- [47] M. Mittal, N. Rudin, V. Klemm, A. Allshire, and M. Hutter. Symmetry considerations for learning task symmetric robot policies. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 7433–7439. IEEE, 2024. 

- [48] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa. Amp: adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics_ , 40(4):1–20, 2021. ISSN 1557-7368. doi:10.1145/3450626.3459670. URL `http://dx.doi.org/10. 1145/3450626.3459670` . 

12 

- [49] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black. AMASS: Archive of motion capture as surface shapes. In _International Conference on Computer Vision_ , pages 5442–5451, Oct. 2019. 

- [50] M. Mittal, P. Roth, J. Tigue, A. Richard, O. Zhang, P. Du, A. Serrano-Mu˜noz, X. Yao, R. Zurbr¨ugg, N. Rudin, L. Wawrzyniak, M. Rakhsha, A. Denzler, E. Heiden, A. Borovicka, O. Ahmed, I. Akinola, A. Anwar, M. T. Carlson, J. Y. Feng, A. Garg, R. Gasoto, L. Gulich, Y. Guo, M. Gussert, A. Hansen, M. Kulkarni, C. Li, W. Liu, V. Makoviychuk, G. Malczyk, H. Mazhar, M. Moghani, A. Murali, M. Noseworthy, A. Poddubny, N. Ratliff, W. Rehberg, C. Schwarke, R. Singh, J. L. Smith, B. Tang, R. Thaker, M. Trepte, K. V. Wyk, F. Yu, A. Millane, V. Ramasamy, R. Steiner, S. Subramanian, C. Volk, C. Chen, N. Jawale, A. V. Kuruttukulam, M. A. Lin, A. Mandlekar, K. Patzwaldt, J. Welsh, H. Zhao, F. Anes, J.-F. Lafleche, N. Mo¨enne-Loccoz, S. Park, R. Stepinski, D. V. Gelder, C. Amevor, J. Carius, J. Chang, A. H. Chen, P. de Heras Ciechomski, G. Daviet, M. Mohajerani, J. von Muralt, V. Reutskyy, M. Sauter, S. Schirm, E. L. Shi, P. Terdiman, K. Vilella, T. Widmer, G. Yeoman, T. Chen, S. Grizan, C. Li, L. Li, C. Smith, R. Wiltz, K. Alexis, Y. Chang, D. Chu, L. J. Fan, F. Farshidian, A. Handa, S. Huang, M. Hutter, Y. Narang, S. Pouya, S. Sheng, Y. Zhu, M. Macklin, A. Moravanszky, P. Reist, Y. Guo, D. Hoeller, and G. State. Isaac lab: A gpu-accelerated simulation framework for multi-modal robot learning. _arXiv preprint arXiv:2511.04831_ , 2025. URL `https://arxiv.org/abs/2511.04831` . 

- [51] Y. Hao, R. Yu, S. Luo, G. Zhang, J. Wu, and Q. Zhu. Cref: Cross-modal and recurrent fusion for depth-conditioned humanoid locomotion. _arXiv preprint arXiv:2603.29452_ , 2026. 

- [52] W. Sun, Y. Su, L. Huang, A. Zhang, D. Wei, M. San, D. Tian, E. Cao, B. Cao, Y. Liu, et al. Now you see that: Learning end-to-end humanoid locomotion from raw pixels. _arXiv preprint arXiv:2602.06382_ , 2026. 

- [53] D. Wang, X. Wang, X. Liu, J. Shi, Y. Zhao, C. Bai, and X. Li. More: Mixture of residual experts for humanoid lifelike gaits learning on complex terrains. _arXiv preprint arXiv:2506.08840_ , 2025. 

- [54] S. Zhu, Z. Zhuang, M. Zhao, K.-Y. Lee, and H. Zhao. Hiking in the wild: A scalable perceptive parkour framework for humanoids. _arXiv preprint arXiv:2601.07718_ , 2026. 

- [55] Y. Zhang, Y. Seo, J. Chen, Y. Yuan, K. Sreenath, P. Abbeel, C. Sferrazza, K. Liu, R. Duan, and G. Shi. Rpl: Learning robust humanoid perceptive locomotion on challenging terrains. _arXiv preprint arXiv:2602.03002_ , 2026. 

13 

## **A The Details of POMDP** 

We formulate humanoid perceptive locomotion as a partially observable Markov decision process (POMDP), denoted as a 6-tuple _M_ = _⟨S, O, A, P, R, γ⟩_ . Here, _S_ is the state space, _O_ is the observation space, _A_ is the action space, _P_ is the transition kernel, _R_ is the reward function, and _γ_ is the discount factor. At each timestep _t_ , the robot has an underlying state _st ∈S_ , which is not fully observable by the policy. The state includes the full robot configuration, velocity, contact state, actuator state, and surrounding terrain geometry. Instead of accessing _st_ directly, the policy receives a multimodal observation _ot ∈O_ composed of proprioception, egocentric depth perception, and local height-scan geometry: 


Here, _dt ∈_ R<sup>1</sup><sup>_×_36</sup><sup>_×_64</sup> denotes the forward-facing depth image, and _h_<sup>_xyz_</sup> _t ∈_ R<sup>3</sup><sup>_×_21</sup><sup>_×_21</sup> denotes the egocentric height scan, where each grid cell stores an ( _x, y, z_ ) terrain point. The proprioceptive observation is a five-frame history 


where each frame is defined as 


Specifically, _ωb,t ∈_ R<sup>3</sup> is the torso angular velocity, _gb,t ∈_ R<sup>3</sup> is the projected gravity vector, _qt, q_ ˙ _t ∈_ R<sup>29</sup> are joint positions and velocities, _at−_ 1 _∈_ R<sup>29</sup> is the previous action, and _ct_ = ( _vx,t_<sup>cmd</sup><sup>_, v_</sup> _y,t_<sup>cmd</sup><sup>_,ψ_˙</sup> _t_<sup>cmd</sup> ) _∈_ R<sup>3</sup> is the velocity command. 

The policy _πθ_ ( _at|ot_ ) maps the observation to an action _at ∈A_ , where _at ∈_ R<sup>29</sup> represents target joint positions at 50 Hz, tracked by a low-level PD controller at 200 Hz. After the action is executed, the environment transitions via _P_ ( _st_ +1 _|st, at_ ) and yields a reward _r_ ˜ _t_ = _R_ ( _st, at_ ) that encourages velocity tracking, stable posture, safe contacts, and human-like motion (see Appendix C.2 for the full reward specification). The complete observation and action spaces are detailed in Table 3. The objective is to maximize the expected discounted return: 


Table 3: Action and observation space specifications. 

|**Modality**|**Symbol**|**Description**|
|---|---|---|
|_Action_|||
|Joint position targets|_at ∈_R<sup>29</sup>|50 Hz control output, tracked via PD at 200 Hz|
|_Proprioception_|||
|Base angular velocity|_ωb,t ∈_R<sup>3</sup><br>|Torso angular velocity|
|Projected gravity|_gb,t ∈_R<sup>3</sup><br>|Gravity direction in torso frame|
|Joint positions|_qt ∈_R<sup>29</sup><br>|Measured joint angles|
|Joint velocities|˙_qt ∈_R<sup>29</sup><br>|Measured joint velocities|
|Previous action|_at−_1 _∈_R<sup>29</sup>|Last commanded joint targets<br>|
|Velocity command|_ct ∈_R<sup>3</sup>|(_v_<sup>cmd</sup><br>_x_<br>_, v_<sup>cmd</sup><br>_y_<br>_,_ <sup>˙</sup>_ψ_<sup>cmd</sup>)target|
|_Depth_|||
|Depth image|_dt ∈_R<sup>1</sup><sup>_×_36</sup><sup>_×_64</sup>|Forward-facing, long-range terrain preview|
|_Height Scan_<br>Height map|_h_<sup>_xyz_</sup><br>_t_<br>_∈_R<sup>3</sup><sup>_×_21</sup><sup>_×_21</sup>|Egocentric(_x, y, z_)terrain grid, local surroundings|


14 

## **B Definition of Gaze Learning** 

We define _gaze_ as a combination of a normalized gaze location _rt_ = ( _rt_<sup>_x, r_</sup> _t_<sup>_y_)</sup><sup>_∈_[0</sup><sup>_,_1]2and</sup> an ROI centered at the gaze location. The ROI is defined as a terrain patch _h_<sup>˜</sup><sup>_xyz_</sup> _t ∈_ R<sup>3</sup><sup>_×K×K_</sup> over the local height scan _h_<sup>_xyz_</sup> _t ∈_ R<sup>3</sup><sup>_×M×M_</sup> with _M_ = 21. We crop the ROI based on the gaze location, where the normalized gaze coordinates are first mapped to the height scan grid as ( _ut, vt_ ) = ( _⌊rt_<sup>_xM⌋, ⌊r_</sup> _t_<sup>_yM⌋_),andtheROIisobtainedbyextractingterrainpointsthrough</sup> _h_ ˜<sup>_xyz_</sup> _t_ = � _h_<sup>_xyz_</sup> _t_ ( _i, j_ ) �� _|i − ut| ≤_ _<u>K</u>_ 2<sup>_,|j −vt| ≤_</sup><sup>_<u>K</u>_</sup> 2<sup>_,i, j∈_Z</sup> � _._ Consequently, we define _gaze learning_ as training the gaze prediction head _f_ roi( _·_ ) to output the gaze location _rt_ = _f_ roi([ _e_<sup>_d_</sup> _t_<sup>_, e_</sup> _t_<sup>_p_]), which</sup> is then used to extract an ROI _h_<sup>˜</sup><sup>_xyz_</sup> _t_ = Crop( _h_<sup>_xyz_</sup> _t , rt_ ), where Crop( _·_ ) denotes the ROI cropping operation defined above. The extracted ROI _h_<sup>˜</sup><sup>_xyz_</sup> _t_ is subsequently provided to the downstream locomotion policy for decision-making. 

## **C Training Details** 

### **C.1 Terrain Design** 


Figure 7: Training Terrains for TAGA 

To improve traversability across diverse terrain conditions, we construct a broad set of representative terrain types during training, including ascending and descending stairs, gaps, stepping stones (sparse footholds), box obstacles, elevated platforms, and sloped surfaces, as illustrated in Fig. 7. This terrain mixture exposes the policy to diverse geometric features, including elevation changes, discontinuous support regions, sparse footholds, obstacle negotiation, and inclined surfaces, thereby encouraging the emergence of generalizable terrain-adaptive locomotion strategies. 

Terrain sampling during training follows a probabilistic strategy to balance exposure across terrain types. Stepping stones are sampled with a probability of 0.3, as they most directly exercise precise foothold selection and sparse-terrain reasoning. Ascending stairs, descending stairs, upslope terrains, and downslope terrains are each sampled with a probability of 0.05, since they mainly introduce structured elevation variations and are less demanding in terms of sparse foothold selection. The remaining probability mass is evenly distributed among gaps, box obstacles, and elevated platforms. This sampling strategy allows the policy to experience a wide range of terrain geometries and improves its adaptability to challenging deployment scenarios. 

### **C.2 Reward Terms** 

The locomotion policy is trained with an augmented reward ˜ _rt_ = _rt_<sup>env</sup> + _ηrt_<sup>AMP</sup> , where _rt_<sup>env</sup> denotes the base task reward, _rt_<sup>AMP</sup> denotes the Adversarial Motion Prior (AMP) reward, and _η_ controls the contribution of the AMP term. The base task reward combines command-tracking objectives, pos- 

15 

ture regularization, joint-level regularization, contact-aware locomotion terms, and safety-oriented penalties. It is designed to encourage agile yet stable locomotion with coordinated contacts and physically plausible motion patterns. 

The primary task objective is velocity tracking, where the robot is rewarded for matching the commanded linear and angular velocities. To improve stability and motion quality, we additionally penalize excessive torso rotation, body tilt, joint torques, joint velocities, joint accelerations, action-rate changes, and deviations from nominal body configurations. These regularization terms encourage smooth and energy-efficient motions while reducing unnecessary body oscillations. 

To promote robust locomotion behaviors, several contact-related rewards and penalties are introduced. These include rewards for maintaining appropriate foot swing durations and penalties for foot sliding, stumbling, undesired body contacts, loss of ground contact, and excessively narrow foot placement. Together, these terms encourage coordinated stepping behaviors and stable support transitions on challenging terrain. During the second-stage fine-tuning process, additional penalties are activated to improve robustness under deployment-oriented disturbances and terrain variations. 

The detailed components and coefficients of _rt_<sup>env</sup> are summarized in Table 4. Here, _c_<sup>_xy_</sup> _t_ = ( _vx,t_<sup>cmd</sup><sup>_, v_</sup> _y,t_<sup>cmd)and</sup><sup>_c_</sup> _t_<sup>_ω_=</sup><sup>_ψ_˙</sup> _t_<sup>cmd</sup> denote the commanded linear and angular velocity components; _F_ denotes the set of feet, _B_ denotes the set of robot links, _q_<sup>0</sup> is the default joint configuration, _ft_<sup>_b_is the</sup> contact force acting on body _b_ , and [ _·_ ]+ = max( _·,_ 0) denotes the positive-part operator. The gating function _G_ flat( _ht_ ) activates the torso-orientation penalty only when the local terrain is sufficiently flat, preventing unnecessary penalization on uneven terrain that naturally requires body inclination. 

In addition to these handcrafted reward terms, an AMP reward is used throughout training to encourage human-like locomotion styles. The discriminator is trained using motion-capture data and provides an auxiliary reward that regularizes the learned behaviors toward natural gait patterns. Specifically, we use retargeted AMASS [49] motions as the reference motion distribution. Both the simulated robot motion and the reference motion are encoded into a compact motion descriptor containing body motion, body orientation, and joint-state information. The discriminator is trained to distinguish policy-generated motion descriptors from AMASS reference descriptors, while the policy is rewarded when its motion is classified as closer to the reference distribution. Unlike framewise imitation, this adversarial formulation provides a distribution-level style prior, allowing the policy to preserve task performance while producing smoother and more natural locomotion patterns. 

### **C.3 Training Hyperparameters** 

Table 5 summarizes the main PPO optimization hyperparameters used for training TAGA. Unless otherwise specified, the same hyperparameters are used throughout all experiments. Values shown in parentheses correspond to the second-stage fine-tuning configuration when different from the first-stage training setup. 

### **C.4 Termination Conditions** 

To facilitate stable training and avoid unsafe failure modes, we use the following episode termination conditions during training: 

1. **Timeout and terrain boundary.** An episode is reset after the maximum episode length of 20 s, or when the robot moves outside the valid terrain region. 

2. **Illegal non-foot contact.** We terminate the episode when non-foot bodies make contact with the environment. The monitored links include the torso, pelvis, waist, shoulder links, elbow links, hip links, and knee links. Contacts are detected using a force threshold of 1 N. 

3. **Bad torso orientation.** The episode is terminated when the torso orientation deviates excessively from upright. In implementation, this is measured by the angle between the torso-frame projected gravity direction and the upright axis, with a threshold of 0 _._ 8 rad. 

16 

Table 4: Reward terms used for locomotion training. The formulas denote the unweighted reward terms. Values in parentheses indicate coefficients used during the second-stage fine-tuning. 

|Category|Term|Formula|Weight|
|---|---|---|---|
|Task Objective|Alive<br>Linear velocity tracking<br>Yaw velocity tracking<br>Yaw command regularization<br>Forward progress|Ialive<br>exp<br>�<br>_−∥v_<sup>_xy_</sup><br>torso_,t _<sup>_−cxy_</sup><br>_t _<sup>_∥_2</sup><sup>_/σ_2</sup><br>_v_<br>�<br>exp<br>�<br>_−_(_ω_<sup>_z_</sup><br>torso_,t _<sup>_−cω_</sup><br>_t_ <sup>)2</sup><sup>_/σ_2</sup><br>_ω_<br>�<br>_|c_<sup>_ω_</sup><br>_t _<sup>_|_</sup><br>I(_c_<sup>_x_</sup><br>_t _<sup>_>_ 0</sup><sup>_._3)</sup><br>�<br>I(_v_<sup>_x_</sup><br>torso_,t _<sup>_<_ 0</sup><sup>_._15) + I(</sup><sup>_vx_</sup><br>torso_,t _<sup>_<_ 0) + I(</sup><sup>_vx_</sup><br>torso_,t _<sup>_< −_0</sup><sup>_._15)</sup><br>�|3_._0<br>2_._0(2_._5)<br>3_._0<br>_−_1_._0<br>_−_0_._5|
|Posture Regularization|Torso angular velocity<br>Torso orientation|_∥ω_<sup>_xy_</sup><br>torso_,t_<sup>_∥_2</sup><br>_G_flat(_ht_)_∥g_<sup>_xy_</sup><br>torso_,t_<sup>_∥_2</sup><br>|_−_0_._05<br>_−_2_._0|
||Pelvis orientation|_∥g_<sup>_xy_</sup><br>pelvis_,t_<sup>_∥_2</sup>|_−_0_._5|
|Joint Regularization|Joint torque|_∥τt∥_<sup>2</sup><br>|_−_1_._5_×_10<sup>_−_7</sup><br>|
||Joint velocity|_∥_˙_qt∥_<sup>2</sup><br>|_−_5_._0_×_10<sup>_−_4</sup><br>|
||Joint acceleration|_∥_¨_qt∥_<sup>2</sup><br><br>|_−_1_._25_×_10<sup>_−_7</sup>|
||Link acceleration|1<br>_|B|_<br>�<br>_b∈B _<sup>_∥_˙</sup><sup>_vb_</sup><br>_t_<sup>_∥_</sup>|_−_0_._01|
||Hip deviation|_∥q_<sup>hip</sup><br>_t_<br>_−q_<sup>hip</sup><sup>_,_0</sup>_∥_<sup>2</sup><br>|_−_0_._1|
||Arm deviation|_∥q_<sup>arm</sup><br>_t_<br>_−q_<sup>arm</sup><sup>_,_0</sup>_∥_1|_−_0_._3|
||Waist deviation|_∥q_<sup>waist</sup><br>_t_<br>_−q_<sup>waist</sup><sup>_,_0</sup>_∥_1<br>|_−_1_._0|
||Joint position limit|�<br>_j_ <sup>dist(</sup><sup>_qj_</sup><br>_t _<sup>_, Qj_)</sup><br>|_−_5_._0|
||Joint velocity limit|�<br>_j_<br>�<br>_|_˙_q_<sup>_j_</sup><br>_t _<sup>_| −ρ_ ˙</sup><sup>_q_ ˙</sup><sup>_qj_</sup><br>max<br>�<br>+<br>|_−_1_._0|
||Joint torque limit|�<br>_j_<br>�<br>_|τ _<sup>_j_</sup><br>_t _<sup>_| −ρττ j_</sup><br>max<br>�2<br>+|_−_0_._01|
||Action rate|_∥at −at−_1_∥_<sup>2</sup>|_−_0_._005|
|Contact and Gait|Undesired contact|�<br>_b/∈F_ <sup>I(</sup><sup>_∥f b_</sup><br>_t _<sup>_∥> ϵ_</sup>_f_<sup>)</sup><br>|_−_1_._0|
||Foot air time|IcmdIsinglemin_f∈F T _<sup>_f_</sup><br>mode<br><br>|0_._25|
||Air/contact time variance<br>Foot stumble|Var_f∈F_(clip(_T _<sup>_f_</sup><br>air<sup>_,_ 0</sup><sup>_._5)) + Var</sup><sup>_f∈F_(clip(</sup><sup>_T f_</sup><br>contact<sup>_,_ 0</sup><sup>_._5))</sup><br>I(_∃f ∈F_ :_∥f _<sup>_xy_</sup><br>_t _<sup>_∥>_ 4</sup><sup>_|f z_</sup><br>_t _<sup>_|_)</sup><br><br>|_−_0_._7(_−_2_._0)<br>_−_2_._0(_−_5_._0)|
||Foot slide|�<br>_f∈F_ <sup>I</sup><sup>_f_</sup><br>contact<sup>_∥vxy,f_</sup><br>_t_<br>_∥_|_−_0_._1|
||Foot orientation|�<br>_f∈F_ <sup>I</sup><sup>_f_</sup><br>contact<sup>_∥gxy,f_</sup><br>_t_<br>_∥_<br><br>|_−_0_._5|
||No-fly|I<br>��<br>_f∈F_ <sup>I</sup><sup>_f_</sup><br>contact <sup>= 0</sup><br>�|_−_2_._0|
||Feet too near|�<br>_d_min_−∥x_<sup>_L_</sup><br>_t _<sup>_−xR_</sup><br>_t _<sup>_∥_</sup><br>�<br>+|_−_1_._0(_−_5_._0)|
|Fine-tuning Only|Volume penetration|�<br>_x∈V_ <sup>I(</sup><sup>_δx >_ 0)(</sup><sup>_∥vx∥_+</sup><sup>_ϵ_)</sup><sup>_δx_</sup><br>|0_._0(_−_1_._0)|
||Stand still|I(_∥c_<sup>_xy_</sup><br>_t _<sup>_∥< ϵc_)I(</sup><sup>_|cω_</sup><br>_t _<sup>_| < ϵ_</sup>_c_<sup>)(</sup><sup>_∥q_</sup>_t _<sup>_−q_0</sup><sup>_∥_</sup>1 <sup>_−b_)</sup>|0_._0(_−_0_._3)|


Table 5: Main training hyperparameters. Values in parentheses indicate the second-stage fine-tuning configuration when different from the first stage. 

|**Parameter**|**Value**|
|---|---|
|Rollout length|24|
|PPO epochs|5|
|Mini-batches|10<br>|
|Learning rate<br>|1_×_10<sup>_−_3</sup><br>|
|Learning-rate schedule|Adaptive|
|Discount factor_γ_|0.99|
|GAE parameter_λ_|0.95|
|PPO clipping coefficient|0.2|
|Value loss coefficient|1.0|
|Entropy coefficient|0.005 (0.002)|
|Gradient clipping norm|1.0|


4. **Low base height.** We terminate states in which the robot has effectively fallen or collapsed. This includes cases where the root height is below 0 _._ 5 m relative to the terrain origin, or the root clearance above the local terrain estimate is below 0 _._ 2 m. 

5. **High hip-link acceleration during foot contact.** To filter out high-impact failure cases, we terminate the episode when a foot is in contact and the corresponding hip-pitch link experiences excessive linear acceleration. A contact is considered active when the foot contact force exceeds 1 N, and termination is triggered when the hip-link acceleration exceeds 225 m _/_ s<sup>2</sup> . This condition discourages stiff, high-impact landings and encourages recoverable contact behaviors. 

Triggering any unsafe termination condition resets the episode immediately. These conditions prevent the policy from exploiting unstable behaviors and focus learning on recoverable locomotion strategies. 

17 

### **C.5 Two-stage Training and Domain Randomization** 

We use a two-stage training procedure to balance skill acquisition and real-world robustness. In the first stage, TAGA is trained in a clean simulation setting without observation noise or deploymentoriented dynamics randomization, allowing the policy to efficiently acquire the core locomotion skills. In the second stage, we fine-tune from the pre-trained checkpoint with a reduced entropy coefficient and deployment-oriented domain randomization. 

For robot dynamics, we randomize the added base payload within [ _−_ 1 _._ 0 _,_ 3 _._ 0] kg, perturb the base center of mass by [ _−_ 0 _._ 05 _,_ 0 _._ 05] m along the _x_ and _y_ axes and along the _z_ axis, and sample motor delays from 0–3 delay steps. Contact properties are randomized with static friction in [0 _._ 3 _,_ 1 _._ 0], dynamic friction in [0 _._ 3 _,_ 0 _._ 8], and restitution in [0 _._ 0 _,_ 0 _._ 5]. We also apply random pushes every 10– 15 s with planar velocity perturbations in [ _−_ 0 _._ 5 _,_ 0 _._ 5] m _/_ s. 

For observations, we add independently sampled uniform noise to proprioceptive channels, with maximum magnitudes of 0 _._ 2 rad _/_ s for base angular velocity, 0 _._ 05 for projected gravity, 0 _._ 01 rad for joint positions, and 1 _._ 5 rad _/_ s for joint velocities. The depth camera is updated at 30 Hz during fine-tuning and is degraded with contour corruption, random depth artifacts, reflections, sky artifacts, Gaussian blur, stereo failure for too-close surfaces, and robot self-occlusion. Depth values are clipped to [0 _._ 4 _,_ 3 _._ 0] m and then normalized before being fed to the policy. 

For height scans, we add _z_ -axis noise in [ _−_ 0 _._ 05 _,_ 0 _._ 05] m and ray-cast drift in [ _−_ 0 _._ 05 _,_ 0 _._ 05] m along each axis. We also randomly corrupt a small portion of height-scan returns to simulate missing or unreliable terrain measurements. Terrain geometry is further perturbed with Perlin roughness, randomized gap-edge transition widths, and virtual edge obstacles. These randomizations improve robustness to perception noise, actuation uncertainty, contact variation, and terrain irregularities that may arise during hardware deployment. 

## **D Training Objectives** 

TAGA is trained using an asymmetric actor–critic PPO objective augmented with auxiliary regularization losses. The overall optimization objective is 


where _L_ PPO is the PPO surrogate loss, _L_ value is the critic regression loss, _H_ ( _πθ_ ) is the policy entropy bonus, and _L_ con and _L_ roi denote the contrastive and gaze regularization losses, respectively. 

### **D.1 MoE–Terrain Contrastive Loss** 

Following CMoE [45], we employ a contrastive objective to encourage terrain-aware soft routing in the MoE policy. Let _B_ denote the batch size and K denote the number of learnable prototypes in a shared prototype dictionary _C_ . The contrastive pair is formed by the actor-gate embedding _e_<sup>_g_</sup> _i_<sup>and</sup> the terrain embedding _e_<sup>_h_</sup> _i_<sup>encoded from the full height scan.Both embeddings are normalized and</sup> compared through the prototype dictionary. 

For an embedding _e_ , we define its prototype prediction distribution and balanced assignment as 


where _T_ con is a temperature parameter. The contrastive loss is 


18 

This objective encourages the gating network to produce terrain-aware soft routing weights by aligning the gate embedding _e_<sup>_g_</sup> _i_<sup>with the terrain embedding</sup><sup>_e_</sup> _i_<sup>_h_in the shared prototype space.This helps</sup> reduce terrain-invariant or nearly uniform expert mixtures and promotes functional differentiation among experts. 

### **D.2 Gaze Boundary Loss** 

To prevent the learned gaze from degenerately selecting crops near the height-scan boundary, we penalize ROI centers that are too close to the edge of the normalized scan domain. For notational convenience, let 


denote the normalized gaze location predicted by TAGA for the _i_ -th sample in a mini-batch. Here, _ri_ is a batch-level notation for the corresponding time-indexed prediction _rt_ used in the policy rollout. Given a boundary margin _m_ = 0 _._ 05, the boundary loss is defined as 


where [ _ξ_ ]+ = max( _ξ,_ 0). This regularizer keeps the selected crop inside the valid height-scan region and prevents unstable edge fixation. 

**Symmetry Augmentation.** We exploit the humanoid’s left-right morphological symmetry by mirroring proprioceptive observations, height scans, AMP states, and actions. For depth observations, a horizontally flipped virtual camera view is used. Both original and mirrored samples are included in PPO updates, encouraging symmetric locomotion behaviors and improving training efficiency. 

19 

