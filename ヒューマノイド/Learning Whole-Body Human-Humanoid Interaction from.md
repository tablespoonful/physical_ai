---
title: "Learning Whole-Body Human-Humanoid Interaction from Human-Human Demonstrations"
date: "2026-01-14"
authors: "Wei-Jin Huang; Yue-Yi Zhang; Yi-Lin Wei; Zhi-Wei Xia; Juantao Tan; Yuan-Ming Li"
url: https://arxiv.org/abs/2601.09518
pdf: https://arxiv.org/pdf/2601.09518
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.09518)** / [論文ページ](https://arxiv.org/abs/2601.09518)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Learning Whole-Body Human-Humanoid Interaction from Human-Human Demonstrations** 

Wei-Jin Huang<sup>1</sup> Yue-Yi Zhang<sup>1</sup> Yi-Lin Wei<sup>1</sup> Zhi-Wei Xia<sup>1</sup> Juantao Tan<sup>1</sup> Yuan-Ming Li<sup>1</sup> Zhilin Zhao<sup>1</sup> Wei-Shi Zheng<sup>1</sup><sup>_,_2</sup><sup>_,_3</sup><sup>_,_4</sup><sup>_,†_</sup> 1School of Computer Science and Engineering, Sun Yat-sen University, China 2Peng Cheng Laboratory, China 

3Key Laboratory of Machine Intelligence and Advanced Computing, Ministry of Education, China; 

4Guangdong Province Key Laboratory of Information Security Technology, China 

huangwj235@mail2.sysu.edu.cn; wszheng@ieee.org 


Figure 1. **From HHI to HHoI with simulation and real-robot results. Left:** PAIR (Physics-Aware Interaction Retargeting) converts human–human interaction sequences into physically consistent human–humanoid (HHoI) clips by aligning morphology and explicitly preserving contact semantics via a two-stage pipeline. **Top (Sim):** Rollouts of the learned policy (D-STAR) in simulation, showing _Bend_ , _Wave_ , _Fly-Kiss_ , _Hug_ , _High-Five_ , and _Handshake_ , demonstrating synchronized whole-body interactions. **Bottom (Real, a–c):** Deployment on a Unitree G1 under a standard whole-body controller; the policy executes _Hug_ , _Handshake_ , and _High-Five_ selected via text commands. 

## **Abstract** 

_Enabling humanoid robots to physically interact with humans is a critical frontier, but progress is hindered by the scarcity of high-quality Human-Humanoid Interaction (HHoI) data. While leveraging abundant Human-Human Interaction (HHI) data presents a scalable alternative, we first demonstrate that standard retargeting fails by breaking the essential contacts. We address this with_ **_PAIR_** 

> _†_ : Corresponding author. 

_(_ Physics-Aware Interaction Retargeting _), a contact-centric, two-stage pipeline that preserves contact semantics across morphology differences to generate physically consistent HHoI data. This high-quality data, however, exposes a second failure: conventional imitation learning policies merely mimic trajectories and lack interactive understanding. We therefore introduce_ **_D-STAR_** _(_ Decoupled Spatio-Temporal Action Reasoner _), a hierarchical policy that disentangles when to act from where to act. In_ **_D-STAR_** _, Phase Attention (when) and a Multi-Scale Spatial module (where) are_ 

1 

_fused by the diffusion head to produce synchronized wholebody behaviors beyond mimicry. By decoupling these reasoning streams, our model learns robust temporal phases without being distracted by spatial noise, leading to responsive, synchronized collaboration. We validate our framework through extensive and rigorous simulations, demonstrating significant performance gains over baseline approaches and a complete, effective pipeline for learning complex whole-body interactions from HHI data._ 

## **1. Introduction** 

Humanoid robots, with their human-like form, hold significant potential for seamless integration into human-centric environments, enabling intuitive collaboration and the use of human tools. While foundational capabilities such as locomotion, manipulation, and learning from human data have advanced considerably [6, 12, 15, 17, 27, 33], unlocking the full potential of these robots requires moving beyond single-agent proficiency. The critical next frontier lies in mastering **Human-Humanoid Interaction (HHoI)** , enabling dynamic collaboration and interaction within shared human spaces. However, achieving HHoI faces major hurdles in **Data Acquisition** and **Interaction Policy Design** . 

Data scarcity is critical: while real-world data via teleoperation [3] is an option, it is high-fidelity but costly, slow, potentially unsafe, and lacks diversity. A more scalable alternative is to leverage simulated data from retargeting Human-Human Interactions [9, 10, 31], but current methods falter. They often prioritize semantic similarity over physical consistency, neglecting morphological differences between humans and humanoids. This can break physical contact essential for interaction (e.g., a retargeted handshake failing due to height differences, as shown in Fig. 2), compromising realism. 

Policy complexity is another major challenge. Controlling a high-DoF humanoid for safe, dynamic HHoI demands real-time management of stability, collisions, and constraints, coupled with context-aware, responsive actions. Current policies, often developed for single-agent or non-interactive settings, cannot typically interpret intent or proactively engage, which is crucial for natural interaction, rather than just mimicking motions. 

To address these challenges, we propose a two-pronged solution that goes beyond simple mimicry at both the _Data_ and _Policy_ levels. 

To solve the data scarcity bottleneck, we introduce **PAIR** ( _Physics-Aware Interaction Retargeting_ ; Sec. 3), a contactcentric, two-stage retargeting pipeline that preserves contact semantics and physical consistency. Instead of naively mimicking joint angles, which we show breaks critical physical contacts, PAIR preserves the interaction’s physical semantics through a targeted optimization process, yielding 


Figure 2. **PAIR** preserves physical consistency where naive methods fail. **Left** : A source HHI handshake. **Center** : Naive retargeting breaks essential contact due to morphological disparities. **Right** : PAIR first ensures kinematic plausibility, then applies an interaction-aware objective ( _L_ con) to refine and enforce the critical physical contact. 

a large-scale, physically consistent HHoI dataset. 

Armed with this high-fidelity data, we find conventional imitation learning still reduces to simple trajectory mimicry, lacking true interactive understanding. It learns to replicate an “average” motion, lacking an understanding of relational geometry or timing for responsive interaction. To overcome this, we present **D-STAR** ( _Decoupled Spatio-Temporal Action Reasoner_ ; Sec. 4), which disentangles **when** to act (Phase Attention, **PA** ) from **where** to act (Multi-Scale Spatial module, **MSS** ), enabling synchronized whole-body collaboration. Fig. 1 demonstrates our method’s effectiveness. 

In summary, our main contributions are: 

- **Unlocking training data from HHI to HHoI.** We develop **PAIR** , an interaction-aware retargeting pipeline that converts large-scale Human–Human Interaction (HHI) datasets into _physically consistent_ supervision for whole-body Human–Humanoid Interaction (HHoI), preserving _contacts_ and _relative geometry_ . 

- **Decoupling when vs. where for interactive control.** We propose **D-STAR** , which separates _temporal intent_ (handled by PA) and _spatial selection_ (handled by MSS), then fuses them for synchronized whole-body actions. 

- **Validation in simulation and real-robot.** We conduct extensive experiments in a high-fidelity simulator and deploy on a humanoid robot with asynchronous sensing and a standard whole-body controller. 

We keep quantitative comparisons in simulation for fairness across controllers, and use real-robot trials to validate practical executability under asynchronous sensing and standard whole-body control. 

## **2. Related Work** 

**Human–Humanoid Interaction.** Recent work advances physical interaction from several fronts: XBG [3] learns end-to-end HHoI but relies on costly teleoperation, limiting scale; transformer-based social forecasting (ECHO [24]) produces open-loop trajectories without reactive control; RHINO [4] targets human–object interaction but is upper- 

2 

body only and still requires demonstrations. _Concurrently_ , closed-loop whole-body directions span compliance/impedance for safer contacts [20, 22], robot-side multi-task control [19], and policies learned from human videos or unified human–robot formulations [25, 28, 30]. These lines are complementary but differ in supervision pathway and scope, typically relying on robot-side supervision or broadening the task beyond social HHI. In contrast, we pursue a scalable route to **whole-body, closedloop** HHoI by learning from abundant HHI demonstrations and explicitly decoupling _when_ to act from _where_ to contact, enabling reactive collaboration without extensive robot-side data collection. 

**Motion Retargeting for Interaction.** Retargeting HHI to humanoids is a promising route to bridge the data gap. Classical IK/trajectory optimization [9, 14] and recent learningbased retargeting [11, 31] mainly optimize kinematic similarity or style, which often fails to preserve contact semantics under morphology mismatch, yielding broken or drifting contacts in HHoI (Fig. 2). In parallel, the graphics community has proposed geometry-/context-aware objectives for animation [7, 18], but these typically lack robotics-grade constraints and safety (e.g., joint limits, self/rigid-body collisions). _Concurrently_ , interaction-preserving retargeting with interaction meshes/Laplacian deformation [32] and evidence that retargeting quality strongly affects downstream policy performance [1] have appeared. Our pipeline is tailored for HHoI and features: (i) an interaction-semantic objective via an _N ×N_ human–robot distance loss _L_ con that prioritizes who touches what, where, and for how long over single-body style; (ii) a two-stage schedule that first secures global feasibility and then tightens contact consistency, mitigating local minima and collision artifacts; and (iii) optimization under robotics-grade constraints (limits, collisions). This closes the data–policy loop for HHoI: higher contact fidelity in retargeted data translates into stronger success of the learned interactive controller. 

## **3. PAIR: Physics-Aware Interaction Retargeting** 

The primary obstacle to leveraging abundant HumanHuman Interaction (HHI) data is the critical failure of conventional retargeting paradigms in the context of physical interaction. The foundational principle of motion retargeting is to preserve kinematic similarity, typically by minimizing differences in joint positions or orientations. However, we contend that for interactive tasks, this very principle, when applied in isolation, leads to catastrophic failure. As visualized in Fig. 2 (Center), an approach focused solely on matching source kinematics breaks the essential physical contact that defines the interaction, a direct result of morphological disparities between the human and the humanoid. An overview is shown in Fig. 3. 

### **Physics-Aware Interaction Retargeting** 


Figure 3. **PAIR** preserves contact semantics and physical consistency via a two-stage retargeting pipeline. From HHI to HHoI while retaining contact semantics across morphology differences. 

Sequences **M** _X_ = _{_ **q**<sup>_X_</sup> _t_<sup>_}T_</sup> _t_ =1<sup>;</sup><sup>_Jt_(</sup><sup>_X, j_)</sup> _∈_ R<sup>3</sup> is the 3D joint position via forward kinematics from **q**<sup>_X_</sup> _t_<sup>.</sup> Reshaped( _Hs_ ) denotes the morphology-aligned human skeleton (pelvis alignment + proportional bone-length scaling + fixed joint correspondences); the full mapping appears in Suppl. A.1, and the symbol table in Suppl. Table S5. 

To overcome this fundamental limitation, we architect our solution as a sequence of targeted fixes. We begin by formulating the retargeting as an optimization problem over the source interaction ( _MHp, MHs_ ) to find an optimal robot motion _MR_ and a minimally adjusted partner motion _MH_<sup>_′_</sup> _p_<sup>.</sup> Our final objective function systematically addresses each layer of the problem: 

_L_ retarget = _w_ con _L_ con + _w_ kin _L_ kin + _w_ hum _L_ hum + _w_ reg _L_ reg _._ In the following, we deconstruct how each component addresses a specific failure mode in a logical cascade. 

### **3.1. From Mimicry to Interaction-Awareness** 

**Kinematic Similarity Loss (** _L_ **kin).** The baseline approach is to ensure that the robot’s motion style resembles the original human demonstration. This is achieved by penalizing the difference between the robot’s global joint positions and those of a morphologically-reshaped source human skeleton Reshaped( _Hs_ ). While foundational, this is the source of the contact-breaking problem. 


**Interaction-Contact Preservation Loss (** _L_ **con).** To robustly preserve the _holistic_ physical semantics of interac- 

3 


Figure 4. Overview of **D-STAR** (Decoupled Spatio-Temporal Action Reasoner): Phase Attention ( **PA** , “when to act”) and Multi-Scale Spatial module ( **MSS** , “where to act”) are fused by a diffusion planning head to yield synchronized whole-body interaction beyond mimicry; a low-level Whole-Body Controller (WBC) executes the final physically plausible action. 

tion, we enforce consistency between the full pairwisedistance matrices computed from task keypoint sets ( _KH , KR_ ) for the original human–human interaction and the optimized human–robot interaction. Let _Dt_<sup>orig</sup> and _Dt_<sup>opt</sup> be the _N × N_ distance matrices at time _t_ ; the loss is: 


This matrix-level constraint maintains contact (e.g., handhand) and appropriate social distances beyond brittle pointwise penalties and is used consistently throughout our work. **Human Motion Fidelity Loss (** _L_ **hum).** However, strictly enforcing contact on the robot could unnaturally distort the human partner’s motion, breaking the mutual plausibility of the interaction. To address this side-effect, we introduce a fidelity loss that penalizes deviations from the partner’s original trajectory. This allows for small, necessary adaptations (e.g., raising an arm for a shorter robot) without creating an entirely new, unrelated action. We apply _selective upper-body adaptation_ (shoulders/elbows/wrists) to avoid implausible posture drift while allowing minimal, task-consistent adjustments. 


**Physical Plausibility Regularizers (** _L_ **reg).** Finally, to ensure that the generated motions are smooth and natural, not jerky or contorted, we incorporate a standard regularization term. It consists of two components: a Temporal Coherence Loss ( _L_ temp) to penalize high-frequency jitter, and a Pose Regularization Loss ( _L_ pose) to keep joint angles within a comfortable range. 

### **3.2. Navigating the Optimization Landscape** 

While our composite objective function now captures the full semantics of interaction, its very complexity creates a new challenge: a difficult, non-convex optimization landscape prone to poor local minima. A single-stage optimization of this function often converges to physicallyimplausible “near-miss” interactions where a handshake becomes a grasp of the air inches from the partner’s hand. 

To solve this, we introduce a coarse-to-fine, Two-Stage Optimization Strategy. This is not a mere heuristic, but a principled approach to guide the solver through the complex energy landscape: 

- **Stage 1: Global Kinematic Initialization.** We first optimize the full objective over the entire sequence with a moderate weight for the contact loss ( _w_ con). This stage finds a globally consistent and kinematically plausible motion, effectively positioning the solver in a desirable “basin of attraction.” 

- **Stage 2: Contact and Stability Refinement.** Using the result from Stage 1 as a warm start, we re-run the optimization with a significantly increased contact loss weight ( _w_ con). This aggressively corrects for subtle contact misalignments and enforces physical stability, refining the “near-miss” into a perfect connection. 

## **4. D-STAR: Decoupled Spatio-Temporal Action Reasoner** 

Conventional imitation learning fails in interactive settings because it conflates two problems: timing ( _when to act_ ) and targeting ( _where to act_ ). We address this with **D-STAR** (Decoupled Spatio-Temporal Action Reasoner), a hierarchical policy built on decoupled spatio-temporal reasoning. 

**Why decoupling and Overview.** Interactive policies 

4 

must reason about **when** an event should occur and **where** contact should be established. In **D-STAR** , we decouple policy reasoning into Phase Attention ( **PA** ) and Multi-Scale Spatial module ( **MSS** ), which are later fused by the diffusion head; execution proceeds via a whole-body controller. This division isolates complementary competencies—timing vs. spatial precision—and avoids interference, while a single planning head ensures coherent actions. Fig. 4 summarizes the architecture; implementation frequencies and scheduler details are deferred to the Supplement. 

Conditioned on this spatio-temporal context, a diffusionbased planning head (Sec. 4.3) generates a high-level action target, which is then realized by a Whole-Body Controller (WBC) that ensures safe and physically plausible execution. Finally, we will outline our training procedure and losses in Sec. 4.4. For temporal context, the network consumes a 12frame history (1 current + 11 past) and predicts a 5-anchor horizon covering 2 s; the execution interface is summarized in Sec. 4.3. The policy is conditioned by a short _text command_ token sequence that selects the interaction type; no task-specific weights or tuning are used at deployment. 

### **4.1. Observations and Temporal Encoder** 

**D-STAR** (our policy) takes as input a history of _h_ observation frames, **O** _t−h_ +1: _t_ , each frame concatenating the humanoid’s proprioceptive state **s**<sup>_R_</sup> _t_<sup>andthehuman’s</sup> SMPL [21] joint positions **s**<sup>_H_</sup> _t_<sup>.Human-HumanoidInter-</sup> action (HHoI) demands both long-term context to understand interaction phases and short-term cues for precise spatial targeting. To capture this duality, we employ a Long-Short Temporal Encoder (LSTE). It uses two parallel Transformer encoders to process the observation history: a long-term encoder ( _Elong_ ) over the full _h_ -frame horizon for contextual understanding, and a short-term encoder ( _Eshort_ ) over the most recent _h_<sup>_′_</sup> -frame horizon ( _h_<sup>_′_</sup> _< h_ ) for fine-grained coordination. The final temporal feature vector **f** _t_<sup>_temp_</sup> is formed by concatenating their outputs: 

**f** _t_<sup>_temp_</sup> = Concat( _Elong_ ( **O** _t−h_ +1: _t_ ) _, Eshort_ ( **O** _t−h′_ +1: _t_ )) 

### **4.2. Decoupled Interaction Modules** 

We consolidate the two parallel interaction modules into a single section to foreground _decoupled spatio-temporal reasoning_ . **Phase Attention (PA)** focuses on _when_ to act by leveraging temporal phase cues and long-range context, while the **Multi-Scale Spatial module (MSS)** resolves _where_ to act via multi-scale geometric neighborhoods and relational encodings. Both branches produce complementary features, **f** _t_<sup>_P hase_</sup> and **f** _t_<sup>_MSS_</sup> , which jointly condition the diffusion-based planning head. **Phase Attention (PA).** Different phases of a HumanHumanoid Interaction (HHoI) require attending to distinct 

cues. For instance, during the _initiation_ of a handshake, the robot must focus on the human’s approaching hand and torso, while in the _closure_ phase, precise palm alignment becomes critical. We implement a phase-aware attention mechanism that predicts the current interaction phase and uses it to weigh specialized self-attention blocks, yielding a phase-conditioned temporal feature **f** _t_<sup>_P hase_</sup> . Intuitively, **f** _t_<sup>_P hase_</sup> summarizes _when_ an interaction event unfolds, providing a temporal gate for downstream decision-making. **Phase taxonomy and labels.** We adopt a 3-phase scheme (Preparation, Act, Follow-up) with tri-phase segmentation per sequence, using a transition-consistency loss to mitigate boundary noise. 

**Multi-Scale Spatial module (MSS).** To determine _where_ to act, we encode the human-robot geometric relationship via multi-scale features: absolute positions, pairwise distances, and relative orientations of key joints. Dedicated encoders map these signals to a spatial feature **f** _t_<sup>_MSS_</sup> that captures coarse-to-fine spatial context. Intuitively, **f** _t_<sup>_MSS_</sup> encodes _where_ the relevant contact geometry lies, aggregating near/mid/far cues into a spatially aware representation. 

Ablations (Table 3) show that removing either branch ( _w/o PA_ or _w/o MSS_ ) degrades performance on tasks requiring precise temporal or spatial coordination, confirming the necessity of both sides of the decoupling. 

### **4.3. Hierarchical Action Generation** 

Conditioned on PA/MSS features and a short text command, a diffusion head predicts a high-level reference action, which a downstream WBC turns into executable joint targets. The policy operates at a lower update rate than the controller to preserve stability; intermediate waypoints and blending/scheduling are defined once in Suppl. F. The same interface is used in simulation and on hardware; controller variants and exact I/O are listed in Suppl. A.4. 

For concision, we omit per-channel dimensions, anchor counts, and frame lengths in the main text; a complete inventory appears in Suppl. Table S1/S3. 

### **4.4. Training and Objectives** 

We jointly train the temporal encoder, Phase Attention, Multi-Scale Spatial, and the diffusion planning head under a composite objective that couples diffusion action prediction with auxiliary phase-classification and geometric consistency terms. Full formulations and weights are in Suppl. A.3, scheduling/densification details are in Suppl. F. 

## **5. Experiments** 

Our experiments are designed to systematically validate our contributions and answer four key questions: **Q1:** Is our physics-aware interaction retargeting method effective? **Q2:** Does our hierarchical policy outperform standard baselines? **Q3:** Are our decoupled reasoning modules essential? 

5 

Table 1. Retargeting results with ablations: physical consistency (JPE, AWD) and multi-threshold contact (Prec/Rec/F1/Acc) at _τ ∈ {_ 0 _._ 2 _,_ 0 _._ 35 _,_ 0 _._ 5 _}_ m, micro-avg over frames _×_ hands. Best results in **bold** , second best <u>underlined;</u> metric definitions are consolidated in Sec. 5.1.1. **PAIR** yields higher contact F1 across thresholds and the best kinematic similarity.<sup>_†_</sup> Re-implemented from the original paper. 

|**Method**|**Phy**<br>**JPE↓**|**sical**<br>**AWD↓**|**Prec↑**|**Contact**<br>**Rec↑**|**@0.2m**<br>**F1↑**|**Acc↑**|**C**<br>**Prec↑**|**ontact**<br>**Rec↑**|**@0.35m**<br>**F1↑**|**Acc↑**|**Prec↑**|**Contact**<br>**Rec↑**|**@0.5m**<br>**F1↑**|**Acc↑**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Simple MSE|0.188|0.126|0.860|0.583|0.695|0.928|0.841|0.583|0.688|0.895|0.870|0.684|0.765|0.888|
|IK Baseline|0.337|0.148|0.850|0.598|0.702|0.927|0.779|0.556|0.649|0.878|0.776|0.594|0.673|0.838|
|Orient Base.|0.342|0.204|0.843|0.384|0.528|0.802|0.671|0.306|0.420|0.731|0.657|0.252|0.364|0.642|
|ImitationNet<sup>_†_</sup>|0.181|0.195|0.855|0.421|0.565|0.831|0.712|0.388|0.502|0.794|0.698|0.313|0.432|0.715|
|**PAIR**|**0.174**|0.095|**0.872**|**0.679**|**0.763**|**0.941**|**0.894**|**0.794**|**0.841**|**0.954**|**0.911**|**0.812**|**0.859**|**0.932**|
||||||**Ablat**|**ion Stu**|**dy**||||||||
|w/o Human Adaptation|0.331|**0.091**|0.856|0.650|0.738|0.936|0.882|0.770|0.823|0.946|0.898|0.804|0.848|0.926|
|w/o Contact Loss|0.331|**0.091**|0.856|0.648|0.738|0.936|0.881|0.769|0.821|0.946|0.898|0.803|0.848|0.926|
|w/o Two-Stage|0.330|0.137|0.864|0.629|0.728|0.936|0.873|0.718|0.788|0.936|0.888|0.749|0.813|0.911|


Table 2. Retargeting results with ablations: physical plausibility (LargeAngle, AngleStd) and smoothness (Jerk mean/std). Metrics in Sec. 5.1.1; best **bold** , second underlined. 

|**Method**|**Physical P**<br>Large Angle↓|**lausibility**<br> Angle Std↓|**Motion S**<br> Jerk Mean|**moothness**<br>↓Jerk Std↓|
|---|---|---|---|---|
|Simple MSE|0.182|0.405|0.0026|0.0571|
|IK Baseline|0.118|**0.330**|0.0348|0.0587|
|Orient Base.|0.298|0.837|0.0142|0.3025|
|ImitationNet|0.095|0.341|0.0015|0.0410|
|**PAIR**|0.093|0.348|0.0008|0.0342|
||**Ablation St**|**udy**|||
|w/o Human Adaptation (HA)|**0.092**|0.348|**0.0007**|**0.0340**|
|w/o Contact Loss (Lcon)|**0.092**|0.348|0.0008|**0.0340**|
|w/o Two-Stage|0.093|0.351|**0.0007**|**0.0340**|


**Q4:** Does our policy demonstrate true robustness by generalizing to unseen variations in human morphology and behavior, moving beyond simple mimicry? 

### **5.1. Validation of Physics-Aware Interaction Retargeting** 

This section quantitatively validates that our proposed retargeting pipeline (Sec. 3) generates physically consistent HHoI data while preserving interaction semantics. 

#### **5.1.1. Setup for Retargeting Evaluation** 

We compare against four baselines: a simple MSE loss on joint positions, an IK-based tracker, an orientation-based method, and the SOTA unsupervised approach ImitationNet [31]. We evaluate using 18 metrics spanning Physical Consistency, Contact Preservation, Plausibility, and Smoothness (details in the supplementary). 

**Evaluation metrics.** We report four categories. First, **JPE (m** _↓_ **)** is the mean per-frame L2 error between robot joints and the Reshaped( _Hs_ ) joints (Sec. 3). Second, **AWD (m** _↓_ **)** is the mean absolute difference between the full N _×_ N pairwise distance matrices built from a fixed set of interaction joints (head, shoulders, elbows, wrists), see Suppl. C.2. Third, for **Contact (multi-** _τ_ **)** , we classify contact per frame for the two hand–hand pairs using optimal left/right match- 

ing at _τ ∈{_ 0 _._ 2 _,_ 0 _._ 35 _,_ 0 _._ 5 _}_ m and report micro-averaged Precision/Recall/F1/Accuracy over frames _×_ hands (protocol in Suppl. C.2.1; no minimum-duration unless stated). Finally, **Plausibility & Smoothness** : **LargeAngle** is the fraction of joint-angle magnitudes _>_ 0 _._ 5 rad; **AngleStd** is the standard deviation of joint-angle magnitudes over joints and frames; **Jerk Mean/Std** (m/s<sup>3</sup> ) are computed on 3D joint positions via third-order finite differences at the dataset frame rate (50 Hz in our data). 

#### **5.1.2. Results and Analysis** 

As shown in Tables 1 and 2, existing retargeting methods break down in interactive settings: the state-of-theart learning baseline _ImitationNet_ attains competitive kinematic similarity (JPE 0.181 m) yet fails to preserve the physical essence of interaction, evidenced by a contactpreservation F1 of 0.502 at the 0.35 m threshold. This motivates an interaction-aware retargeting approach. 

Our PAIR closes this gap by maintaining physical contact, achieving a contact F1 of **0.841** (0.35 m, microaveraged)—a **67.5%** relative gain over _ImitationNet_ and **22.2%** over the best non-interactive baseline ( _Simple MSE_ ). These results directly address the canonical failure of naive retargeting, where morphological disparities break essential contacts (Fig. 2). 

Crucially, this does not trade off other qualities: we obtain the **best kinematic similarity** (JPE **0.174** m) and markedly smoother motion, with a **69%** jerk reduction versus _Simple MSE_ (Table 2). 

Ablations attribute these gains to all key components. Removing Human Adaptation (HA) or the contact loss ( _L_ con) lowers contact F1 to 0.823 and 0.821, respectively—indicating that while kinematic and regularization terms form a strong base, the final margin of physical precision requires these specialized modules. Most critically, collapsing the coarse-to-fine procedure into a single stage drops F1 to 0.788, suggesting convergence to kinematically plausible yet physically incorrect near-miss minima. To- 

6 

Table 3. This table compares the Success Rate (Acc %) on six interactive tasks. Our full method significantly outperforms architectural variants and fundamental baselines, especially on complex contact-based tasks (Hug, Handshake). The failure of **Diffusion Policy** , a strong baseline using the same data and controller, highlights that simply replaying trajectories is insufficient. Ablations show that both PA and MSS modules are critical for high performance. 

||**Method**|**Hug**|**High-Five**|**Handshake**|**Wave**|**Bend**|**Fly-Kiss**|**Avg.**|
|---|---|---|---|---|---|---|---|---|
|Fundamental Baselines|Naive Mimicry (BC only)|0.0|0.0|0.0|0.0|0.0|0.0|0.0|
||TCN Policy|53.3|11.1|12.9|88.9|86.7|**90.9**|49.2|
|Architectural Variants|Transformer Policy|73.3|**44.4**|32.3|92.6|86.7|**90.9**|64.3|
||Diffusion Policy[8]|73.3|3.7|38.7|**96.3**|**93.3**|**90.9**|58.7|
||**D-STAR (Full Model)**|**100.0**|40.7|**61.3**|**96.3**|**93.3**|**90.9**|**75.4**|
|O Mthd d Ablti|w/o PA|86.7|22.2|45.2|**96.3**|**93.3**|**90.9**|65.9|
|ur eo an aons|w/o MSS|**100.0**|29.6|32.3|**96.3**|86.7|81.8|64.3|
||w/o PA + MSS|86.7|25.9|51.6|**96.3**|**93.3**|**90.9**|68.3|


Table 4. **Robustness Matrix** : Average Success Rate (%) under combined variations in human partner’s scale and speed. The central value (bold) is our standard performance. The graceful degradation towards the edges demonstrates true robustness. 

|||**P**|**artner**|**Motio**|**n Spee**|**d**|
|---|---|---|---|---|---|---|
|||**0.8x**|**0.9x**|**1.0x**|**1.1x**|**1.2x**|
|**le**|**0.8x**|64.3|66.7|68.3|66.7|63.5|
|**Sca**|**0.9x**|67.5|72.2|74.6|70.6|67.5|
|**er**|**1.0x**|70.6|**75.4**|**75.4**|73.0|71.4|
|**rtn**|**1.1x**|68.3|72.2|73.0|70.6|68.3|
|**Pa**|**1.2x**|64.3|64.3|65.1|64.3|62.7|


gether, an explicit contact objective, flexible partner adaptation, and principled two-stage optimization act synergistically to yield the observed improvements. 

Having established that **PAIR** produces high-quality, physically consistent HHoI data, we next test whether such data can train a truly interactive policy surpassing standard mimicry. 

### **5.2. Validation of the HHoI Policy** 

Here, we evaluate the effectiveness of our decoupled spatiotemporal policy, measuring task success rates across six interaction types and comparing against architectural variants and fundamental mimicry baselines. 

#### **5.2.1. Setup for Policy Evaluation.** 

We validate our policy using the Unitree G1 humanoid in Isaac Gym [23] (50 Hz control). Our full model is benchmarked against fundamental baselines (Naive Mimicry) and strong architectural variants (TCN, Transformer, and Diffusion Policies [8]), all trained on our retargeted data and executed in simulation with the same tracking controller (WBC-Sim) for fair comparison. Training details of WBCSim appear in Suppl. A.3.2; the execution interface is in Suppl. A.4.1. For qualitative real-robot validation, we run trials using a HOMIE-based pre-trained controller [2] with the waist roll and pitch locked. Task success is computed by automated detectors. For Handshake, success is detected 

by a multi-criterion, sustained-contact rule: _≥_ 10 consecutive frames at 50 Hz with valid interpersonal distance and contact stability; exact global thresholds are consolidated in the supplementary (Suppl. C.3; Table S6). All HHoI policy experiments are run with a fixed random seed (42). Full implementation details, success criteria, and controller notes are in the supplementary material. 

**Unified protocol.** All methods use the same dataset splits, the same whole-body controller at 50 Hz, and the same densification/blending and scheduling procedure. Policies produce action updates at 5 Hz. Success criteria, thresholds, and evaluation scripts are identical across methods. Implementation details are deferred to the Supplement. 

#### **5.2.2. Setup for Policy and Training Details** 

**Policy setup.** We use a 12-frame observation history including the current frame ( _t_ ) at 50 Hz, and predict 5 anchors at _t_ + _{_ 0 _,_ 0 _._ 5 _,_ 1 _._ 0 _,_ 1 _._ 5 _,_ 2 _._ 0 _}_ s with the policy running at 5 Hz. Observations are represented in an ego-centric frame with root-translation offset normalization, and comprise SMPL joint positions for the human together with robot proprioception (base linear and angular velocities, gravity projection, and joint states). The architecture adopts a Long-Short Temporal Encoder (LSTE) coupled with two decoupled interaction modules: PA for event-phase reasoning, and MSS for proximity-aware reasoning, with near/mid/far ranges set to 0-0.3 m, 0.3-0.8 m, and 0.8-3.0 m. A diffusion-based planning head outputs a 36-D reference action composed of 29 joint targets and root motion (3 translation, 4-D quaternion orientation). In simulation, only the 29 joint components are executed by the controller, while the root pose is used internally; on hardware, root motion is mapped to planar base commands. We optimize with Adam (1 _×_ 10<sup>_−_4</sup> , fixed), batch size 2048, for 1000 epochs. 

#### **5.2.3. Whole-Body Controllers (Sim and Real).** 

**Simulation.** We execute predicted joint targets using an tracking controller (WBC-Sim; details in Suppl. A.4). **Real robot.** For safety and hardware compatibility, we 

7 

use a HOMIE-based controller (waist roll/pitch locked) [2]. HOMIE uses a root-velocity interface ( _vx, vy, ψ_<sup>˙</sup> ) (yaw rate); we convert our root position/rotation predictions accordingly (see Suppl. A.4.3). Our framework is controlleragnostic and can accommodate alternatives such as GMT [5] and Hover [16] (see Suppl. A.4.5). 

**Temporal scheduler.** Policies run at 5 Hz and output five anchors at _t_ + _{_ 0 _,_ 0 _._ 5 _,_ 1 _._ 0 _,_ 1 _._ 5 _,_ 2 _._ 0 _}_ s. We densify to 50 Hz via bilinear interpolation to form a 100-frame reference (root pose + joints) tracked by the WBC; consecutive calls are fused on overlap, with zero-order hold on delays. All rules are fixed across methods as part of the Unified protocol (details are in Suppl. F). 

#### **5.2.4. Experimental Results and Analysis.** 

As shown in Table 3, **Naive Mimicry** fails (0% mean success), verifying that a low-level controller is necessary for physical stability; merely replaying trajectories is inadequate. 

Our full model, **D-STAR** , achieves a state-of-the-art 75.4% average success, surpassing strong architectural baselines—Transformer (64.3%) and TCN (49.2%). The 11.1-point margin over the Transformer indicates that improvements stem from decoupled spatio-temporal reasoning rather than backbone choice. The advantage is most pronounced on contact-rich tasks such as Handshake, where success nearly doubles (61.3% vs. 32.3%). These gains are not incremental; they directly address the shortcomings of unified policies. 

Ablations (Table 3, bottom) show that both PA and the MSS module are essential. Removing PA degrades temporally sensitive interactions (e.g., High-Five), while removing MSS harms spatially precise ones (e.g., Handshake). The full model—with both components—achieves the best overall performance, confirming that decoupling enables complementary temporal and spatial reasoning. 

#### **5.2.5. Robustness to Spatio-Temporal Variations** 

To rigorously test generalization rather than mimicry (Q4), we evaluate a grid of joint variations in human-partner body scale and motion speed (0 _._ 8 _×_ –1 _._ 2 _×_ ). As shown in Table 4, our policy is highly robust, sustaining a performance plateau (peaking at **75.4%** ) and degrading gracefully—not catastrophically—retaining **62.7%** success even at the most extreme corner of the grid. 

The results also reveal an embodiment-aware asymmetry: the policy is more resilient with smaller partners than larger ones. We attribute this to our 1.3 m G1 humanoid: scaling the human down reduces size mismatch, whereas scaling up places key interaction points (hands, shoulders) at unfavorable heights. Thus, the policy adapts to its own kinematic affordances rather than imitating unattainable human–human behaviors, providing quantitative evidence that 


**Unitree G1 with Logitech C1000e Monocular SMPL reconstruction** 

Figure 5. Monocular SMPL perception setup and result. (a) Unitree G1 with a Logitech C1000e RGB camera (1280 _×_ 720@30 fps). (b) Input RGB frame. (c) SMPL mesh estimated from the single RGB stream (4D-Humans [13]) and mapped to the robot base frame after extrinsic calibration. 

our decoupled reasoning architecture learns a truly generalizable interaction model. 

### **5.3. Sim to Real Deployment** 

**Hardware & sensing.** We deploy on a Unitree G1 (29-DoF model; practically 27-DoF with waist roll/pitch locked). A Logitech C1000e is mounted _vertically_ and streams 1280 _×_ 720@30 fps to the control PC (Ryzen 9700X, RTX 4090). Single-RGB SMPL estimates (4D-Humans [13]) are transformed from the camera to the robot base frame after one-time extrinsic calibration. **Control stack and timing.** The low-level controller runs at 50 Hz while the high-level policy runs at 5 Hz; all remaining scheduling details mirror the simulator setup (Suppl. F). **Task conditioning.** The same model parameters are used; different social behaviors are selected solely via a _text command_ at the policy input. 

**Fine-tuning for deployment.** Before deployment we perform a _single, task-agnostic fine-tuning_ to reduce simto-real gaps in pre-/post-interaction phases while keeping the core motion intact: (i) _Act_ segments are unchanged; (ii) _Preparation_ is standardized to a neutral upper-body posture—both hands naturally placed in front of the root on the left/right sides—lower body unchanged; root translation is retargeted to a milder yaw and a simpler walking pattern; the last 16 frames bilinearly transition into the first frame of the _Act_ ; (iii) _Follow-up_ becomes stationary, and the upper body bilinearly returns over 16 frames to the same neutral hand placement. This retargeted dataset is used _once_ to fine-tune the high-level policy for real-robot execution; no per-task tuning or prompt-specific calibration is applied. **Outcomes.** As shown in Fig. 1, the robot executes _Hug, Handshake, and High-Five_ (Wave and Fly-Kiss are omitted in the figure) under their respective text commands. Quantitative comparisons remain in simulation for fairness; the real-robot trials establish _practical executability_ under asynchronous sensing and standard whole-body control. 

8 

## **6. Conclusion** 

We move beyond mimicry to learn whole-body HHoI by addressing critical failures at both the data and policy levels. First, our interaction-aware retargeting pipeline generates physically-consistent HHoI data from human demonstrations, preserving crucial contacts where naive methods fail. Building on this, our hierarchical policy uses decoupled spatio-temporal reasoning to decode interactive intent, enabling responsive collaboration rather than simple trajectory replay. Our work demonstrates a complete pipeline for learning genuine human-robot interaction, urging a shift from rote mimicry to true collaborative intelligence. 

## **References** 

- [1] Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, and C. Karen Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 3 

- [2] Qingwei Ben, Feiyu Jia, Jia Zeng, Junting Dong, Dahua Lin, and Jiangmiao Pang. HOMIE: Humanoid locomanipulation with isomorphic exoskeleton cockpit. _arXiv preprint arXiv:2502.13013_ , 2025. 7, 8, 16 

- [3] Carlos Cardenas-Perez, Giulio Romualdi, Mohamed Elobaid, Stefano Dafarra, Giuseppe L’Erario, Silvio Traversaro, Pietro Morerio, Alessio Del Bue, and Daniele Pucci. Xbg: End-to-end imitation learning for autonomous behaviour in human-robot interaction and collaboration. _IEEE Robotics and Automation Letters_ , 2024. 2 

- [4] Jingxiao Chen, Xinyao Li, Jiahang Cao, Zhengbang Zhu, Wentao Dong, Minghuan Liu, Ying Wen, Yong Yu, Liqing Zhang, and Weinan Zhang. Rhino: Learning real-time humanoid-human-object interaction from human demonstrations. _arXiv preprint arXiv:2502.13134_ , 2025. 2 

- [5] Zixuan Chen, Mazeyu Ji, Xuxin Cheng, Xuanbin Peng, Xue Bin Peng, and Xiaolong Wang. GMT: General motion tracking for humanoid whole-body control. _arXiv preprint arXiv:2506.14770_ , 2025. 8, 16 

- [6] Xuxin Cheng, Yandong Ji, Junming Chen, Ruihan Yang, Ge Yang, and Xiaolong Wang. Expressive whole-body control for humanoid robots. _arXiv preprint arXiv:2402.16796_ , 2024. 2 

- [7] Th´eo Cheynel, Thomas Rossi, Baptiste Bellot-Gurlet, Damien Rohmer, and Marie-Paule Cani. Reconform: Realtime contact-aware motion retargeting for more diverse character morphologies. In _Computer Graphics Forum_ , page e70028. Wiley Online Library, 2025. 3 

- [8] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , page 02783649241273668, 2023. 7 

- [9] Sungjoon Choi and Joohyung Kim. Towards a natural motion generator: A pipeline to control a humanoid based on motion data. In _2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 4373–4380. IEEE, 2019. 2, 3 

- [10] Sungjoon Choi, Matthew KXJ Pan, and Joohyung Kim. Nonparametric motion retargeting for humanoid robots on shared latent space. In _Robotics: science and systems_ , 2020. 2 

- [11] Sungjoon Choi, Min Jae Song, Hyemin Ahn, and Joohyung Kim. Self-supervised motion retargeting with safety guarantee. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 8097–8103. IEEE, 2021. 3 

- [12] Yahao Fan, Tianxiang Gui, Kaiyang Ji, Shutong Ding, Chixuan Zhang, Jiayuan Gu, Jingyi Yu, Jingya Wang, and Ye Shi. One policy but many worlds: A scalable unified policy for versatile humanoid locomotion. _arXiv preprint arXiv:2505.18780_ , 2025. 2 

- [13] Shubham Goel, Georgios Pavlakos, Jathushan Rajasegaran, Angjoo Kanazawa, and Jitendra Malik. Humans in 4D: Reconstructing and tracking humans with transformers. In _ICCV_ , 2023. 8 

- [14] Waldez Gomes, Vishnu Radhakrishnan, Luigi Penco, Valerio Modugno, Jean-Baptiste Mouret, and Serena Ivaldi. Humanoid whole-body movement optimization from retargeted human motions. In _2019 IEEE-RAS 19th International Conference on Humanoid Robots (Humanoids)_ , pages 178–185. IEEE, 2019. 3 

- [15] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning. _arXiv preprint arXiv:2406.08858_ , 2024. 2 

- [16] Tairan He, Wenli Xiao, Toru Lin, Zhengyi Luo, Zhenjia Xu, Zhenyu Jiang, Jan Kautz, Changliu Liu, Guanya Shi, Xiaolong Wang, et al. Hover: Versatile neural whole-body controller for humanoid robots. _arXiv preprint arXiv:2410.21229_ , 2024. 8 

- [17] Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbab, Chaoyi Pan, et al. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. _arXiv preprint arXiv:2502.01143_ , 2025. 2 

- [18] Inseo Jang, Soojin Choi, Seokhyeon Hong, Chaelin Kim, and Junyong Noh. Geometry-aware retargeting for twoskinned characters interaction. _ACM Transactions on Graphics (TOG)_ , 43(6):1–17, 2024. 3 

- [19] Dvij Kalaria, Sudarshan S Harithas, Pushkal Katara, Sangkyung Kwak, Sarthak Bhagat, Shankar Sastry, Srinath Sridhar, Sai Vemprala, Ashish Kapoor, and Jonathan ChungKuan Huang. Dreamcontrol: Human-inspired whole-body humanoid control for scene interaction via guided diffusion. _arXiv preprint arXiv:2509.14353_ , 2025. 3 

- [20] Gangyang Li, Qing Shi, Youhao Hu, Jincheng Hu, Zhongyuan Wang, Xinlong Wang, and Shaqi Luo. Thor: Towards human-level whole-body reactions for intense contactrich environments. _arXiv preprint arXiv:2510.26280_ , 2025. 

   - 3 

- [21] Matthew Loper, Naureen Mahmood, Javier Romero, Gerard Pons-Moll, and Michael J Black. Smpl: A skinned multiperson linear model. In _Seminal Graphics Papers: Pushing the Boundaries, Volume 2_ , pages 851–866. 2023. 5, 11 

- [22] Qingzhou Lu, Yao Feng, Baiyu Shi, Michael Piseno, Zhenan Bao, and C. Karen Liu. Gentlehumanoid: Learning upper- 

9 

   - body compliance for contact-rich human and object interaction. _arXiv preprint arXiv:2511.04679_ , 2025. 3 

- [23] Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, et al. Isaac gym: High performance gpu-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 7 

- [24] Esteve Valls Mascaro, Yashuai Yan, and Dongheui Lee. Robot interaction behavior generation based on social motion forecasting for human-robot interaction. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 17264–17271. IEEE, 2024. 2 

- [25] Ri-Zhao Qiu, Shiqi Yang, Xuxin Cheng, Chaitanya Chawla, Jialong Li, Tairan He, Ge Yan, David J. Yoon, Ryan Hoque, Lars Paulsen, Ge Yang, Jian Zhang, Sha Yi, Guanya Shi, and Xiaolong Wang. Humanoid policy ˜ human policy. In _Proceedings of The 9th Conference on Robot Learning_ , pages 2888–2906. PMLR, 2025. 3 

- [26] Jiaming Song, Chenlin Meng, and Stefano Ermon. Denoising diffusion implicit models. _arXiv preprint arXiv:2010.02502_ , 2020. 20 

- [27] Annan Tang, Takuma Hiraoka, Naoki Hiraoka, Fan Shi, Kento Kawaharazuka, Kunio Kojima, Kei Okada, and Masayuki Inaba. Humanmimic: Learning natural locomotion and transitions for humanoid robot via wasserstein adversarial imitation. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 13107–13114. IEEE, 2024. 2 

- [28] Haoyang Weng, Yitang Li, Nikhil Sobanbabu, Zihan Wang, Zhengyi Luo, Tairan He, Deva Ramanan, and Guanya Shi. Hdmi: Learning interactive humanoid whole-body control from human videos. _arXiv preprint arXiv:2509.16757_ , 2025. 3 

- [29] Liang Xu, Xintao Lv, Yichao Yan, Xin Jin, Shuwen Wu, Congsheng Xu, Yifan Liu, Yizhou Zhou, Fengyun Rao, Xingdong Sheng, et al. Inter-x: Towards versatile humanhuman interaction analysis. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 22260–22271, 2024. 11, 17 

- [30] Sirui Xu, Hung Yu Ling, Yu-Xiong Wang, and Liang-Yan Gui. Intermimic: Towards universal whole-body control for physics-based human-object interactions. _arXiv preprint arXiv:2502.20390_ , 2025. CVPR 2025. 3 

- [31] Yashuai Yan, Esteve Valls Mascaro, and Dongheui Lee. Imitationnet: Unsupervised human-to-robot motion retargeting via shared latent space. In _2023 IEEE-RAS 22nd International Conference on Humanoid Robots (Humanoids)_ , pages 1–8. IEEE, 2023. 2, 3, 6 

- [32] Lujie Yang, Xiaoyu Huang, Zhen Wu, Angjoo Kanazawa, Pieter Abbeel, Carmelo Sferrazza, C. Karen Liu, Rocky Duan, and Guanya Shi. Omniretarget: Interaction-preserving data generation for humanoid whole-body loco-manipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 3 

- [33] Ziwen Zhuang, Shenzhe Yao, and Hang Zhao. Humanoid parkour learning. _arXiv preprint arXiv:2406.10759_ , 2024. 2 

10 

# **Learning Whole-Body Human-Humanoid Interaction from Human-Human Demonstrations** 

# Supplementary Material 

## **Overview** 

This supplementary material is organized into six sections (A–F) for clarity and reproducibility. **Terminology.** We refer to our retargeting pipeline as **PAIR** ( _Physics-Aware Interaction Retargeting_ ) and our policy as **D-STAR** ( _Decoupled Spatio-Temporal Action Reasoner_ ). Within D-STAR, we decouple policy reasoning into Phase Attention ( **PA** ) and Multi-Scale Spatial ( **MSS** ), which are fused by the diffusion head. 

- **A. Method Implementation Details** (Sec. A): Retargeting pipeline (Sec. A.1), hierarchical policy (Sec. A.2), training (Sec. A.3), and low-level controllers/execution (Sec. A.4; root interface conversion Sec. A.4.3; controller modularity Sec. A.4.5). 

- **B. Dataset Details and Analysis** (Sec. B; built from the Inter-X dataset [29]). 

- **C. Experimental Protocols & Metrics** (Sec. C): Unified notation & symbol table (Sec. C.1, Table S5), retargeting metrics (Sec. C.2), policy evaluation and detection rules (Sec. C.3). 

- **D. Dataset Retargeting for Sim-to-Real** (Sec. D). 

- **E. Observation & Action Specification** (Sec. E; Table S1). 

- **F. Scheduler, Densification & Diffusion Details** (Sec. F; includes densification and fusion Algorithms 8 and 9). 

## **A. Method Implementation Details** 

This section provides a comprehensive breakdown of our proposed framework. We first detail **PAIR** ( _Physics-Aware Interaction Retargeting_ ; Sec. A.1), explaining the principled design of our objective function and optimization strategy used to generate physically consistent HHoI data. 

We then dissect **D-STAR** ( _Decoupled Spatio-Temporal Action Reasoner_ ; Sec. A.2), elucidating the core principle of decoupled reasoning and its realization through specialized modules. In D-STAR, we decouple policy reasoning into **PA** and **MSS** . Finally, we specify the exact **Training Procedures and Loss Functions** (Sec. A.3) for both the high-level policy and the low-level controller. 

### **A.1. PAIR: Physics-Aware Interaction Retargeting** 

This section provides a comprehensive breakdown of our implementation. We architect our solution as a sequence of targeted fixes, where each component of our objective function addresses a specific failure mode inherent in conventional retargeting. 

#### **A.1.1. Objective Function Components** 

We define the retargeting objective as a weighted sum of four terms that jointly encourage kinematic similarity and interaction semantics: 

- _L_ retarget = _w_ kin _L_ kin + _w_ con _L_ con + _w_ hum _L_ hum + _w_ reg _L_ reg _, L_ reg = _α L_ temp + _β L_ pose _._ 

Unless otherwise stated, distances are measured in meters and joint angles in radians. The frame rate is 50 Hz. 

**Kinematic similarity (** _L_ **kin).** We encourage the robot’s joint-space configuration to match a morphologically reshaped source human skeleton, Reshaped( _Hs_ ). The reshaping solves for SMPL [21] shape parameters **_β_** _∈_ R<sup>10</sup> and a global scale _s_ that best fit the robot’s bone lengths: 


where _M_ maps robot joints to SMPL joints (correspondence listed below). We optimize this objective for 500 iterations using Adam (learning rate 0 _._ 1). 

|**Robot (G1)**||**SMPL**|
|---|---|---|
|pelvis|_→_|Pelvis|
|left<br>~~h~~ip<br>~~p~~itch<br>~~l~~ink|_→_|L<br>~~H~~ip|
|left<br>~~k~~nee<br>~~l~~ink|_→_|L<br>~~K~~nee|
|left<br>~~a~~nkle<br>~~r~~oll<br>~~l~~ink|_→_|L<br>~~A~~nkle|
|right<br>~~h~~ip<br>~~p~~itch<br>~~l~~ink|_→_|R<br>~~H~~ip|
|right<br>~~k~~nee<br>~~l~~ink|_→_|R<br>~~K~~nee|
|right<br>~~a~~nkle<br>~~r~~oll<br>~~l~~ink|_→_|R<br>~~A~~nkle|
|left<br>~~s~~houlder<br>~~r~~oll<br>~~l~~ink|_→_|L<br>~~S~~houlder|
|left<br>~~e~~lbow<br>~~l~~ink|_→_|L<br>~~E~~lbow|
|left<br>~~h~~and<br>~~l~~ink|_→_|L<br>~~H~~and|
|right<br>~~s~~houlder<br>~~r~~oll<br>~~l~~ink|_→_|R<br>~~S~~houlder|
|right<br>~~e~~lbow<br>~~l~~ink|_→_|R<br>~~E~~lbow|
|right<br>~~h~~and<br>~~l~~ink|_→_|R<br>~~H~~and|
|head<br>~~l~~ink|_→_|Head|
|left<br>~~t~~oe<br>~~l~~ink|_→_|L<br>~~T~~oe|
|right<br>~~t~~oe<br>~~l~~ink|_→_|R<br>~~T~~oe|


**Interaction-contact consistency (** _L_ **con).** To maintain the interaction geometry, we enforce consistency between the original and optimized holistic spatial relationships. Let _KH_ and _KR_ denote selected human/robot keypoint sets (e.g., head, shoulders, elbows, wrists, hands); define the joint set _K_ = _KH ∪KR_ with _N_ = _|K|_ . For time _t_ , let 

11 

**x** _t_ ( _i_ ) _∈_ R<sup>3</sup> be the position of keypoint _i ∈K_ , and define the pairwise distance matrix 


We compute _Dt_<sup>orig</sup> from the original interaction and _Dt_<sup>opt</sup> after optimization, and minimize 


This construction measures configuration-level geometry rather than a single contact, improving robustness to minor local deviations. 

**Human motion fidelity (** _L_ **hum).** To avoid unrealistic adjustments on the human partner, we penalize deviations from the original human pose while allowing selective upper-body adaptation. Let **p** ˜ _H,t_ be the optimized human joint positions and **p** _H,t_ the original ones. Define the upperbody index set _J_ UA = _{_ shoulder _,_ elbow _,_ wrist _}_ bilaterally. Then 


which enables plausible upper-limb adjustments (e.g., a slight arm lift) while preserving core posture. 

**Physical plausibility regularizers (** _L_ **reg).** We use standard temporal and pose regularization. Let **q** _t ∈_ R<sup>_D_</sup> be the robot joint angles at time _t_ ( _D_ DoF). We use discrete derivatives 


The losses are 


where _wa_ balances velocity and acceleration penalties (numeric values and stage-wise schedules are given in Sec. A.1.2). 

#### **A.1.2. Two-Stage Optimization Strategy and Hyperparameters** 

Optimizing all terms from scratch can converge to poor local minima (e.g., “near-miss” contacts). We therefore adopt a coarse-to-fine, two-stage schedule. 

**Optimization process.** Sequence-level retargeting is optimized for **200** iterations with Adam. The above **500** iterations refer solely to the one-time SMPL shape fitting (Sec. A.1.1); they are not part of the per-sequence optimization. 

- **Stage 1 (coarse initialization)** (iterations 1–150, LR= 0 _._ 02): optimize the full objective with a moderate contact weight ( _w_ con = 0 _._ 25) to obtain a kinematically feasible trajectory. 

- **Stage 2 (contact refinement)** (iterations 151–200, LR= 0 _._ 005): increase the contact weight by 10 _×_ to emphasize interaction consistency ( _w_ con = 2 _._ 5), turning near-miss cases into consistent contact while keeping other weights unchanged. 

#### **Loss weights (Stage 1).** 

- Kinematic similarity ( _L_ kin): _w_ kin = 1 _._ 0 

- Contact consistency ( _L_ con): _w_ con = 0 _._ 25 

- Human motion fidelity ( _L_ hum): _w_ hum = 0 _._ 25 

- Temporal coherence ( _L_ temp): _w_ temp = 5 _._ 0 

• Pose regularization ( _L_ pose): _w_ pose = 0 _._ 02 In the notation of Sec. A.1.1 where _L_ reg = _α L_ temp+ _β L_ pose, these correspond to _w_ reg _α_ = _w_ temp and _w_ reg _β_ = _w_ pose. **Constraints and post-processing.** During optimization, joint angles are clamped to hardware limits [ **q** min _,_ **q** max]. After optimization, we apply a Gaussian smoothing filter (kernel size = 5, _σ_ = 0 _._ 75) to the joint trajectories for improved temporal smoothness. 

#### **A.1.3. Experimental Environment** 

The pipeline is implemented in PyTorch. All optimizations are performed on a server with dual AMD EPYC 7B13 CPUs, without GPU acceleration. 

### **A.2. D-STAR: Decoupled Spatio-Temporal Action Reasoner** 

**D-STAR** is architected around a core principle: **decoupling spatio-temporal reasoning** . To achieve robust and responsive interaction, an agent must solve two distinct sub-problems: inferring the temporal phase of the interaction ( _when_ to act) and understanding the precise geometric relationship with the partner ( _where_ to act). In D-STAR, we explicitly address this with parallel, specialized modules—Phase Attention ( **PA** ) and Multi-Scale Spatial ( **MSS** )—which are then integrated to produce a final, context-aware action. This section details the components of this architecture. 

#### **A.2.1. Input Representation: Observation Space and Temporal Encoding** 

**Observation Space Design.** Each observation frame **O** _t_ concatenates human SMPL features and robot proprioception: 

- **Human SMPL features:** root translation _s_<sup>_H_</sup> _t_<sup>_∈_R3and</sup> joint positions _jt_<sup>_H∈_R72 (24 joints</sup><sup>_×_3D);</sup> 

12 

- **Robot proprioception:** _s_<sup>_R_</sup> _t_<sup>_∈_R74 including base linear &</sup> angular velocities (3+3), gravity projection (3), joint positions/velocities (29+29), root translation offset (3), and root orientation quaternion (4). 

- Thus **O** _t_ = Concat( _s_<sup>_H_</sup> _t_<sup>_, j_</sup> _t_<sup>_H, s_</sup> _t_<sup>_R_)</sup><sup>_∈_R149.</sup> 

**Long–Short Temporal Encoder (LSTE).** We use a dualstream encoder to capture both long-term context and shortterm reactivity: 

**f** _t_<sup>_long_</sup> = _Elong_ ( **O** _t−h_ +1: _t_ ) = TranS _long_ ( _{_ **O** _i}_<sup>_t_</sup> _i_ = _t−h_ +1<sup>)</sup><sup>_,_</sup> **f** _t_<sup>_short_</sup> = _Eshort_ ( **O** _t−h′_ +1: _t_ ) = TranS _short_ ( _{_ **O** _i}_<sup>_t_</sup> _i_ = _t−h_<sup>_′_</sup> +1<sup>)</sup><sup>_._</sup> 

**We set** _h_ = 12 **and** _h_<sup>_′_</sup> = 6 _(short stream observes only the most recent 6 frames for reactive precision, while the long stream attends to the full 12-frame buffer for phase context)._ Each stream produces a **768-d** feature; their concatenation ( **1536-d** ) is linearly projected to a **256-d** temporal feature **f** _t_<sup>_temp_</sup> shared by both reasoning streams. 

#### **A.2.2. Temporal Reasoning: Phase Attention (PA)** 

To answer **“when to act”** , PA dynamically infers the current interaction phase and emphasizes phase-relevant cues. A phase classifier predicts a distribution **p** _t_ over _k_ = 3 phases from **f** _t_<sup>_temp_</sup> : 


Concurrently, _k_ = 3 phase-specialized self-attention experts process **f** _t_<sup>_temp_</sup> . The phase-aware temporal feature is a probability-weighted mixture: 


and is projected to 256-d to match the temporal feature scale. 

#### **A.2.3. Spatial Reasoning: Multi-Scale Spatial (MSS)** 

To answer **“where to act”** , MSS builds a scale-aware geometric understanding. We segment space into three zones (values fixed throughout): 

- **Near Field (0–0.3 m)** : precise contact operations, 

- **Mid Field (0.3–0.8 m)** : coordinated gesture exchange, 

- **Far Field (0.8–3.0 m)** : approach and planning. 

**Encoders.** A **3D positional encoder** applies sinusoidal encodings to the relative position **p** _rel_ . A **multi-scale distance encoder** processes Euclidean distance _d_ via zonespecific MLPs gated by indicator functions. A **hierarchical orientation encoder** uses heading, projections, and rotational harmonics for approach-aware orientation. 

**Fusion.** We first concatenate encoder outputs into a spatial vector **f** _spatial_ , transform it into a dynamic interaction field 

**f** _field_ via an MLP, and then fuse it with temporal context through attention: 

**f** _t_<sup>_MSS_</sup> = FusionAttn�Concat( **f** _field,_ MLP _proj_ ( **f** _t_<sup>_temp_</sup> ))� _,_ 

followed by a projection to 128-d to obtain the final spatial feature. 

#### **A.2.4. Feature Fusion and Hierarchical Action Generation** 

With decoupled streams providing **f** _t_<sup>_phase_</sup> and **f** _t_<sup>_MSS_</sup> , we integrate them with the shared temporal context and the language command embedding to form a global conditioning vector: 


**Dimensionalities. f** _t_<sup>_temp_</sup> _∈_ R<sup>256</sup> , **f** _t_<sup>_phase_</sup> _∈_ R<sup>256</sup> , **f** _t_<sup>_MSS_</sup> _∈_ R<sup>128</sup> , **l** _∈_ R<sup>768</sup> , thus **c** _t ∈_ R<sup>**1408**</sup> . 

A conditional diffusion policy _D_ generates a high-level target: 


This target is executed by a pre-trained whole-body controller (WBC-Sim) to produce physically-consistent motor commands **a** _t_ that maintain balance and respect joint limits. _Implementation note._ In simulation we command the articulated joints (29-DoF) while using the root as an internal reference; on hardware the root component is converted to base commands via the standard base-velocity interface. 

### **A.3. Training Procedures and Loss Functions** 

Our framework’s hierarchical nature is mirrored in our training methodology. We employ a **decoupled training strategy** that optimizes the high-level interaction policy and the low-level whole-body controller independently. This separation of concerns allows each component to be trained with the most suitable objectives and data distributions, leading to a system that is both intelligent in its interaction planning and robust in its physical execution. This section details the training procedures and objectives for each component of our hierarchy. 

#### **A.3.1. High-Level Policy Training (Supervised Learning)** 

The high-level policy, which includes the temporal encoders and our decoupled spatio-temporal reasoning modules, is trained end-to-end via supervised learning on our curated HHoI dataset. 

**Objective Function.** The policy is trained to optimize a composite loss function _Ltotal_ that combines a primary action prediction objective with several auxiliary terms for regularization and phase supervision. 

_Ltotal_ = _λactLaction_ + _λphLphase_ + _λauxLaux_ 

The high-level components are defined as follows: 

13 

- **Action Prediction Loss (** _Laction_ **):** The core objective for the diffusion model is a dimension-weighted MSE loss on the predicted action **a**<sup>_target_</sup> . 

- **Phase Supervision Loss (** _Lphase_ **):** This supervises the Phase Attention module using a cross-entropy loss for classification ( _Lcls_ ) and a KL divergence loss for enforcing logical phase transitions ( _Ltrans_ ). 

- **Auxiliary Geometric Loss (** _Laux_ **):** This term encourages plausible interactive behaviors by regularizing the geometric and relational aspects of the generated motion. It includes losses for facing orientation, keypoint positioning, spatial consistency, and more. 

The detailed mathematical formulations for the primary and auxiliary losses are provided below. **Action Prediction Loss.** The primary action loss is a weighted MSE over the predicted change in root translation ∆ **p** , root orientation (quaternion) **q** , and joint angles **_θ_** . 


We use weights _wtrans_ = 10 _._ 0, _wrot_ = 10 _._ 0, and _wdof_ = 1 _._ 0. 

**Auxiliary Loss Formulations.** The components of _Lphase_ and _Laux_ are defined as: 

- **Human-Facing Orientation Loss (** _Lface_ **):** To ensure the robot maintains a natural orientation towards its partner, we penalize the deviation from a direct facing angle using the cosine distance between the robot’s forward vector **v** _fwd_<sup>_R_and the vector to the human</sup><sup>**v**</sup><sup>_R→H_.</sup> 


- **Keypoint Position Loss (** _Lpos_ **):** To guide the high-level geometric structure, we apply an L2 loss on the predicted 3D positions of critical keypoints _K_ (e.g., hands, head). 


- **Logical Phase Transition Loss (** _Ltrans_ **):** To enforce logical temporal progression, we use a KL divergence loss between the predicted phase transition probabilities **P** _t→t_ +1 and a predefined valid transition matrix **T** _valid_ . 

_Ltrans_ = _DKL_ ( **T** _valid ∥_ **P** _t→t_ +1) 

- **Spatial Consistency Loss (** _Lspatial_ **):** To maintain the holistic geometric relationship, we penalize the difference between the predicted and ground-truth inter-keypoint distance matrices ( _Dpred_ , _Dgt_ ) using the Frobenius norm. 

_Lspatial_ = _∥Dpred − Dgt∥F_<sup>2</sup> 

The weights for these auxiliary terms are set as follows: _wcls_ = 0 _._ 0005 (for the phase classifier), _w_ phase ~~K~~ L<sup>= 0</sup><sup>_._005,</sup> _wface_ = 0 _._ 2, _wpos_ = 5 _._ 0, and _wspatial_ = 0 _._ 02. 

Table S1 enumerates the oracle/student observation channels and how they are consumed during training and evaluation. 

**Implementation Parameters.** The high-level policy is trained with the following configuration: 

- **Temporal Window:** 12-frame observation history including the current frame ( _t_ ) at 50 Hz; predict **5 anchors** at _t_ + _{_ 0 _,_ 0 _._ 5 _,_ 1 _._ 0 _,_ 1 _._ 5 _,_ 2 _._ 0 _}_ s; anchors are densified to 50 Hz and fused across consecutive 5 Hz calls via bilinear interpolation. 

- **Network Dimensions:** LSTElong/short streams each 768-d; concatenation 1536-d with linear projection to 256-d. Phase Attention (PA) uses 256-d features; MultiScale Spatial (MSS) uses 128-d. Global conditioning for the diffusion head is 640-d from concatenation (256, 256, 128), with 768-d language features. 

- **Training Scale:** 1000 epochs, Adam (1 _×_ 10<sup>_−_4</sup> ), batch size 2048 (stride=25), seed 42. 

- **Advanced Features:** Ego-centric processing for consistent spatial reasoning; auxiliary observations include robot proprioception and 768-d language features. 

**A.3.2. Low-Level Whole-Body Controller (WBC-Sim): Oracle** _→_ **Student Distillation** 

**Overview.** We train the simulation controller in two steps: an oracle teacher on clean observations and a student distilled on noisy observations with 10-frame history. Both stages share the same robot and control interface (29-D joint-angle targets at 50 Hz), the same environment and motion-resampling interval (500 steps (50 Hz)), and the same base domain randomization; noise and DR curricula are disabled. The distilled student is the only controller used for all policy evaluations. Table S2 summarizes the teacher vs student configuration. 

**Privileged** _→_ **Noisy Distillation.** We frame WBC-Sim training as privileged _→_ noisy distillation: the _oracle_ is optimized on clean, _privileged_ observations (including base linear and angular velocities), while the _student_ operates on noisy, realistic observations _without_ base linear velocity and with a 10-frame history. All evaluations use the distilled student. 

**Noise protocol.** All _current-frame sensing_ channels are perturbed with fixed per-channel uniform noise during student training; _history stacks inherit_ the perturbation from their constituent frames and receive no extra injection; the _previous action_ is left clean to prevent compounding errors. Table S3 details the per-channel perturbations. 

14 

Table S1. **WBC-Sim observation inventory and usage.** At train time, the oracle uses _clean_ observations without history; the student consumes _noisy_ observations with 10-frame history and the policy’s 36-D reference ( _ut_ ). At evaluation, the fixed student is used; we retain the 10-frame history but do not inject synthetic noise. Only the WBC output ( **29-D** joint-angle targets at **50 Hz** ) is actuated in simulation. 

|Channel (actor)|Symbol|Dim|Oracle<br>train|Student<br>train|Eval<br>(policy exec.)|History<br>(frames)|
|---|---|---|---|---|---|---|
|Joint positions (target space)|_q_|29|✓|✓|✓|10|
|Joint velocities|˙_q_|29|✓|✓|✓|10|
|Base angular velocity (body)|_ωb_|3|✓|✓|✓|10|
|_Base linear velocity (body)_|_vb_|3|✓|—|—|0|
|Gravity vector (body frame)|_gb_|3|✓|✓|✓|10|
|Previous action (joint target)|_at−_1|29|✓|✓|✓|10|
|Policy reference (from high-level)|(_ut_)|**36**|✗|✓|✓|10|
|_Actor total (clean vs noisy)_||_163 / 1090_|✓|✓|✓||
|_Critic total (clean vs noisy)_||_361 / 1291_|✓|✓|✓||


Evaluation uses the fixed **student** controller with **10-frame history** and **no synthetic observation noise** . _Note._ The oracle has access to privileged base linear velocity; the student excludes it. 

Table S1. (continued): Observation and action channels. “Used” indicates channels that are fed to the policy; others are loggingonly when present in raw data. 

|Channel|Dim.|Used|
|---|---|---|
|Human root translation|3|✓|
|SMPL joints (human)|72|✓|
|Base linear velocity|3|✓|
|Base angular velocity|3|✓|
|Gravity projection|3|✓|
|Robot joint positions|29|✓|
|Robot joint velocities|29|✓|
|Root translation (offset)|3|✓|
|Root orientation (quaternion)|4|✓|
|**Reference action (policy head)**|**36**|**—**|
|Joint targets (executed)|29|—|
|Root translation (reference)|3|—|
|Root orientation (reference)|4|—|


**Oracle (Teacher) — Clean Observations.** Actor/critic receive noise-free raw channels (163-D / 361-D). We optimize an Upper-Body-Emphasized Tracking Reward with PPO using an MLP(512,256,128), clip 0.2, _γ_ 0.99, _λ_ 0.95, entropy 0.01, lr 1e _−_ 3. Base domain randomization (mass/friction/PD/push up to 1.0 m/s) is enabled; curricula are off. A frozen checkpoint is used for distillation. 

**Student — Pure Action-Matching Distillation.** Inputs are Noisy Observations with 10-Frame History (1090-D / 1291-D). We train with a pure distillation loss 


freezing the teacher and the policy std (init = 0, min = 0). Network/optimizer mirror the teacher (lr 1e _−_ 3). **Actions** 

**and history channels are noise-free** , while other keys use fixed per-key uniform noise (no curriculum). DR settings match the teacher. 

**Reward (key terms).** The tracking suite emphasizes upper-body targets (e.g., root ~~p~~ osition ~~x~~ y 3.0, bodyposition (upper-body) 4.0, SMPL-hands-ori 5.0) with standard stability/effort penalties and a termination cost of _−_ 100. 

### **A.4. Low-Level Controllers & Execution** 

This section details execution controllers in simulation and on the real robot, and outlines the interface conversion and robustness adaptations. 

#### **A.4.1. Simulation Controller (WBC-Sim).** 

We execute 29-D joint-angle targets (rad) at 50 Hz, produced by WBC-Sim. Here, _xt_ denotes robot proprioception (joint states, base signals, gravity, previous action, etc.). At each step, WBC-Sim takes as input (i) robot proprioception and (ii) the policy’s 36-D reference _ut_ (29 joint targets + root translation and unit quaternion), and tracks these references under joint-limit and rate constraints. Only the 29D joint targets are actuated in simulation; the root translation/rotation are used internally by WBC-Sim as reference signals (not directly actuated). All quantitative policy results in the main paper use the same WBC-Sim for fairness across methods. This controller corresponds to the distilled student described in Sec. A.3.2. For clarity, the policy observation used by the learning agent differs from the controller observation summarized here; this distinction is intentional. 


15 

Table S2. Teacher vs Student configuration for WBC-Sim distillation. 

|**Component**|**Obs. Set**|**Dim (act/crit)**|**Noise**|**History**|**Curric.**|**Objective**|
|---|---|---|---|---|---|---|
|Oracle (Teacher)|Clean observations (+ base linear velocity)|163 / 361|Off|0|Off|PPO w/ tracking reward|
|Student (WBC-Sim)|Noisy observations with 10-frame history (−base linear velocity)|1090 / 1291|On (per-key; actions & history off)|10|Off|Action-mean MSE to teacher|


Table S3. **Noise model for student distillation.** We apply per-channel, zero-mean uniform noise during _student training_ only; the oracle uses clean observations and evaluation does not inject synthetic noise. History and action channels are not perturbed. 

|Channel group|Distribution|Magnitude (symbolic)|Applied to|
|---|---|---|---|
|Joint positions_q_|_U_(_−δq, δq_)|_δq_ (const.)|Student train|
|Joint velocities ˙_q_|_U_(_−δ_˙_q, δ_˙_q_)|_δ_˙_q_ (const.)|Student train|
|Base ang. vel. _ωb_|_U_(_−δω, δω_)|_δω_ (const.)|Student train|
|Gravity vector_gb_|_U_(_−δg, δg_)|_δg_ (const.)|Student train|
|Prev. action_at−_1, History stacks||_no perturbation_||
|Policy reference_ut_ (36-D)|_U_(_−δu, δu_)|_δu_ (const.)|Student train|
|Curriculum|_disabled (i_|_fixed magnitudes throughou_|_i  t training)_|
|Evaluation||_no synthetic noise injected_||


where _ut ∈_ R<sup>36</sup> is the policy reference and _at ∈_ R<sup>29</sup> are joint-angle targets executed at 50 Hz. 

#### **A.4.2. Real-World Controller (HOMIE-based, 27 DoF).** 

For real-robot demos we employ a HOMIE-based pretrained controller [2], with the waist roll/pitch locked. HOMIE exposes a root-velocity interface ( _vx, vy, ψ_<sup>˙</sup> ) (yaw rate); our planning model outputs root position/rotation, so we apply a deterministic conversion prior to execution (see Sec. A.4.3). Real-robot demonstrations are qualitative; quantitative comparisons are reported in simulation using WBC-Sim. 

#### **A.4.3. Root Interface Conversion (Position-to-Velocity Control)** 

Since the HOMIE[2] controller expects velocity commands ( _vx, vy, ψ_<sup>˙</sup> ) while our policy predicts root position targets, we implement a closed-loop controller with active braking to ensure precise stopping. Instead of simple finitedifference conversion, we employ a distance-to-go logic based on onboard odometry. 

We issue a constant forward reference velocity _vref_ = 0 _._ 2 m/s to drive the robot. During execution, we continuously monitor the residual distance, defined as the difference between the policy’s cumulative predicted displacement and the actual distance traversed via odometry. To mitigate inertial drift, we implement an **active braking mechanism** : when the residual distance drops below a proximity threshold ( _δdist ≤_ 0 _._ 15 m) while the robot maintains significant momentum (current speed _vcurr ≥_ 0 _._ 1 m/s), we issue a reverse velocity command ( _vbrake_ = _−_ 0 _._ 2 m/s) to rapidly decelerate and stabilize the robot at the target location. 

#### **A.4.4. Phase-Specific Trajectory Adaptation for Stability** 

To enhance execution robustness in simulation, we perform a deterministic adaptation of the reference trajectory based 

on the interaction phase. The **Act** phase is strictly preserved to maintain the fidelity of the learned interaction intent. For the **Preparation** and **Follow-Up** phases, we employ smoothed primitives to ensure stable transitions and prevent transient oscillations: 

- **Neutral Upper-Body Pose (** _qneutral_ **):** We define a stable, task-agnostic upper-body configuration used as the anchor for non-interaction phases. The joint angles (in radians) are set as follows: 

- _Left Arm:_ Shoulder (pitch/roll/yaw) = [0 _._ 0 _,_ 0 _._ 3 _,_ 0 _._ 0], Elbow = 1 _._ 0, Wrist = [0 _._ 0 _,_ 0 _._ 0 _,_ 0 _._ 0]. 

- _Right Arm:_ Shoulder (pitch/roll/yaw) = [0 _._ 0 _, −_ 0 _._ 3 _,_ 0 _._ 0], Elbow = 1 _._ 0, Wrist = [0 _._ 0 _,_ 0 _._ 0 _,_ 0 _._ 0]. 

- **Preparation Phase:** To simulate diverse approach scenarios, we initialize the robot’s root position randomly within a 1 _._ 0 m radius of the original sequence’s starting point, while maintaining the original orientation. The robot’s root pose (position and rotation) and upper-body joints are then generated via _bilinear interpolation_ from this randomized state to the first frame of the Act phase, ensuring a smooth approach trajectory. 

- **Follow-Up Phase:** Upon completion of the interaction (end of Act phase), the robot’s root is kept stationary. The upper-body joints are bilinearly interpolated from the last frame of the Act phase back to _qneutral_ , ensuring a stable disengagement. 

#### **A.4.5. Controller Modularity.** 

Our framework is controller-agnostic: WBC-Sim and the HOMIE-based controller can be replaced by alternative whole-body controllers. In particular, GMT [5] is compatible with our action interface; we leave a systematic comparison for future work. 

16 


Figure S1. The foundation of our entire framework: a large-scale, high-fidelity Human-Humanoid Interaction (HHoI) dataset that we generated to solve the critical data scarcity problem. Visualized here are thousands of physically-consistent interaction pairs, the output of **PAIR** . The dataset’s strategic diversity—spanning contact-rich scenarios (e.g., hugs, handshakes), dynamic gestures (e.g., high-fives), and social cues (e.g., bows)—provides the rich and complex spatio-temporal variations required to train a policy that learns to interact. 

## **B. Dataset Details and Analysis** 

In this section, we detail the construction of our HumanHumanoid Interaction (HHoI) dataset. We emphasize that this dataset is not merely a collection of motions, but a **strategically engineered resource** . The principled task selection, rigorous quality control, and, most critically, the detailed phase annotations were all designed with the explicit goal of creating a benchmark that could validate our core hypothesis: that genuine interaction requires decoupling spatial reasoning. The structure of this dataset is therefore intrinsically linked to the architecture of our policy. 

### **B.1. Data Source and Task Selection Rationale** 

Our data foundation is the Inter-X dataset [29], a largescale repository of human-human interactions. To construct a comprehensive benchmark for HHoI, our task selection was not arbitrary but driven by a principled strategy to cover a taxonomy of interaction types crucial for humanoid robotics: 

- **Contact-Rich Interactions** (Hug, Handshake): Tasks demanding precise physical contact, stability, and management of close-proximity geometry. 

- **Dynamic Gestural Interactions** (High-Five, Wave): Tasks requiring temporal synchronization and spatial accuracy without sustained contact. 

- **Socially-Encoded Interactions** (Bend, Fly-Kiss): Tasks that rely on conveying social intent through whole-body gestures, often at a distance. 

- This curated selection of six tasks ensures our policy is evaluated across a diverse and representative range of physical and social challenges inherent to HHoI. 

### **B.2. Curation Pipeline and Quality Control** 

Following task selection, each candidate sequence from Inter-X passed through a rigorous, multi-stage curation pipeline to ensure its suitability for training a robust HHoI policy. We enforced strict quality gates to filter out unsuitable data: 

- **Motion Fidelity:** We excluded samples with significant tracking errors, occlusions, or unnatural motion artifacts that would introduce noise into the training process. 

- **Interaction Clarity:** We selected samples exhibiting clear initiation, execution, and completion phases, ensuring the full arc of an interaction was captured. 

- **Kinematic Feasibility:** We ensured that the captured in- 

17 

teractions occur within a spatial volume and pose range that is reasonably achievable by our target humanoid robot. 

- **Temporal Completeness:** We retained only samples containing the complete interaction sequence, from the initial approach to the final departure. 

Only sequences that passed all four gates were admitted into our final dataset, guaranteeing a high-quality foundation for our experiments. 

### **B.3. Phase Annotation for Interaction Understanding** 

A cornerstone of our work, and a key enabler for our policy’s temporal reasoning, is the detailed manual annotation of interaction phases. Recognizing that interactions are not monolithic but possess a distinct temporal structure, we manually segmented each curated sequence into three semantically meaningful phases: 

- **Preparation Phase:** The initial approach and positioning, where agents navigate and adjust their orientation towards each other. 

- **Act Phase:** The core execution of the interaction, including contact establishment (e.g., Hug, Handshake), gesture performance (e.g., Wave, High-Five), or expression delivery (e.g., Bend, Fly-Kiss). 

- **Follow-up Phase:** The completion and disengagement, involving contact release, returning to a neutral posture, and spatial separation. 

This annotation process represents a significant human effort and provides the critical supervision signal for our Phase-Aware Attention module (Main. Sec. 4.2). It directly enables our policy to learn _when_ to act—a capability that conventional imitation learning approaches inherently lack. 

### **B.4. Final Dataset Statistics and Properties** 

Table S4. Detailed HHoI Dataset Statistics by Interaction Task. The column abbreviations are as follows: **Sam.** : Samples; **Seq.** : Total sequences of frames; **Dura.** : Total duration in seconds; **Avg Fra.** : Average frames per sample; **Avg Sec.** : Average seconds per sample. 

|**Task**|**Sam.**|**Seq.**|**Dura.**|**Avg**<br>**Fra.**|**Avg**<br>**Sec.**|
|---|---|---|---|---|---|
|Hug|226|292,873|5,857.5|1,296|25.9|
|Handshake|259|296,414|5,928.3|1,144|22.9|
|High-Five|219|176,482|3,529.6|805|16.1|
|Bend|200|176,024|3,520.5|880|17.6|
|Fly-Kiss|177|158,412|3,168.2|895|17.9|
|Wave|160|149,118|2,982.4|932|18.6|
|**Total**|**1,241**|**1,249,323 **|**24,986.5**|**1,007**|**20.1**|


Table S5. **Symbol table (core).** In this table, ( _τ_ ) denotes the **contact distance threshold** only; task-detection thresholds are denoted ( _τ·_ ) and are summarized in Table S6. 

|Symbol|Meaning|
|---|---|
|**M**_X_ =_{_**q**<sup>_X_</sup><br>_t _<sup>_}T_</sup><br>_t_=1|Motion sequence of agent_X_|
|_JX_<br>|Joint set of agent_X_<br>|
|_Jt_(_X, j_)_∈_R<sup>3</sup><br>|3D joint position via FK from**q**<sup>_X_</sup><br>_t_|
|Reshaped(_Hs_)|Morphology-aligned skeleton of_Hs_|
|**P**task<br>|Task-specific human–robot keypoint pairs|
|∆_t_|Sampling period (0.02 s, i.e., 50 Hz)|
|_τ_|Contact distance threshold (0_._2_/_0_._35_/_0_._5m)|
|_w_phase<br>~~K~~L|Weight for the phase/transition KL term (_L_trans)|
|**PAIR**|Physics-Aware Interaction Retargeting|
|**D-STAR**|Decoupled Spatio-Temporal Action Reasoner|


## **C. Experimental Protocols and Evaluation Metrics** 

In this section, we provide a detailed account of the protocols and metrics used to validate our framework at both the data and policy levels. The descriptions are designed to be comprehensive, ensuring full reproducibility of our experimental results and the claims made in the main paper. 

### **C.1. Unified Notation & Units** 

The output of this comprehensive pipeline—from principled selection to manual annotation—is the HHoI dataset used throughout our experiments. The key statistics, which reflect the dataset’s scale and diversity across the selected tasks, are summarized in Table S4. 

**Temporal and Spatial Richness:** The final dataset spans approximately 6.9 hours of interaction data (at 50 Hz), with average sample durations ranging from 16.1 seconds for compact gestures to 25.9 seconds for complex, contact-rich tasks like hugs. This temporal depth, combined with the tracking of key body joints, provides a rich source of spatiotemporal data essential for training our multi-scale policy. The balanced distribution across tasks ensures robust training and evaluation across all targeted interaction categories. 

**Sampling and units.** All sequences are sampled at ∆ _t_ = 0 _._ 02 s (50 Hz). Distances are in meters; angles in radians; jerk on positional trajectories is in m/s<sup>3</sup> . 

**Motion variables.** For agent _X ∈{Hs, Hp, R}_ (source human, partner human, robot), a motion sequence is **M** _X_ = _{_ **q**<sup>_X_</sup> _t_<sup>_}T_</sup> _t_ =1<sup>with generalized coordinates</sup><sup>**q**</sup> _t_<sup>_X∈_R</sup><sup>_DX_. Let</sup><sup>_JX_</sup> be the joint set of _X_ . The 3D position of joint _j ∈JX_ is _Jt_ ( _X, j_ ) _∈_ R<sup>3</sup> , obtained by forward kinematics from **q**<sup>_X_</sup> _t_<sup>.</sup> 

**Morphology alignment.** Reshaped( _Hs_ ) denotes the morphology-aligned human skeleton constructed by pelvisframe alignment, isotropic bone-length scaling, and a 

18 

fixed joint correspondence derived from the robot–SMPL mapping. In practice, we obtain the reshaped SMPL parameters by optimizing SMPL shape **_β_** and a global scale _s_ to fit robot bone lengths (see Sec. A.1); we refer to the resulting kinematic chain as Reshaped( _Hs_ ). 

**Task keypoint pairs. P** task denotes the task-specific set of human–robot keypoint pairs referenced by contact-related definitions (see Sec. C.2.1). 

### **C.2. Motion Retargeting Evaluation** 

To rigorously assess the quality of **PAIR** , we employed a comprehensive suite of 18 metrics spanning physical consistency, contact preservation, plausibility, and smoothness. 

#### **C.2.1. Evaluation Metrics** 

**Physical Consistency Metrics.** These metrics evaluate the overall geometric and structural fidelity of the retargeted motion. 

- **Joint Position Error (JPE)** _↓_ : The mean L2 distance between robot joints and the morphologically reshaped source human joints Reshaped( _Hs_ ) (Sec. A.1), measuring kinematic similarity. 

- **Average Workspace Distance (AWD)** _↓_ : The mean absolute difference between the full _N × N_ pairwise distance matrices built from a fixed set of interaction joints (head, shoulders, elbows, wrists). We compare the original human–human interaction (initiator vs. responder) with the retargeted human–robot interaction (initiator vs. robot), capturing holistic spatial-relationship preservation. 

**Multi-Threshold Contact Detection Metrics.** To evaluate contact preservation across varying interaction types, we define three distance thresholds and compute standard classification metrics for each. 

- **Thresholds** : 0.2 m, 0.35 m, and 0.5 m. 

- **Protocol** : For each frame we classify contact for the two hand–hand pairs using optimal left/right matching; metrics are micro-averaged over frames _×_ hands. Unless otherwise stated, we do not enforce a minimum contact duration. 

- **Metrics** : For each threshold, we compute **Precision** _↑_ , **Recall** _↑_ , **F1-Score** _↑_ , and **Accuracy** _↑_ to quantify how well the retargeted motion preserves the original contact semantics. 

**Physical Plausibility Metrics.** These metrics assess whether the generated motion is natural and within realistic biomechanical limits. 

- **Large Angle Ratio** _↓_ : The percentage of frames where joint-angle magnitudes (axis–angle) exceed 0 _._ 5 rad, flagging unnatural poses. 

- **Angle Standard Deviation** _↓_ : The standard deviation of joint-angle magnitudes (axis–angle) aggregated over joints and frames, indicating pose distribution consistency. 

**Motion Smoothness Metrics.** These metrics quantify the temporal coherence and fluidity of the motion. 

- **Jerk Mean** _↓_ **(m/s**<sup>3</sup> **)** : The average magnitude of the third temporal derivative of 3D joint positions, computed via third-order finite differences at the dataset frame rate (50 Hz), penalizing high-frequency jitter. 

- **Jerk Standard Deviation** _↓_ **(m/s**<sup>3</sup> **)** : The standard deviation of the same jerk magnitudes, indicating temporal stability. 

### **C.3. Interaction Policy Evaluation** 

#### **C.3.1. Task Success Criteria and Detection Algorithms** 

To quantitatively evaluate policy performance, we designed specific success criteria for each of the six interaction tasks. The core logic for each detection algorithm is outlined below (Algorithms 1–6), providing a transparent basis for our results. 

#### **Hug** 

A hug is detected if the human’s hands make sustained and appropriate contact with the robot’s torso or shoulders, captured via three distinct modes. Algorithm 1 details the full detection logic. 

#### **Handshake** 

A successful handshake is verified through both sustained hand contact and appropriate interpersonal distance. Algorithm 2 provides the handshake detection procedure. 

#### **High-Five** 

Success requires a brief, decisive contact between human and robot hands at an appropriate height. Algorithm 3 outlines the high-five detector. 

#### **Wave** 

A wave is identified by characteristic hand motion patterns, including sufficient amplitude and clear direction changes. Algorithm 4 describes the full wave detection pipeline. 

#### **Bend** 

A bend is robustly measured by the forward inclination angle of the head-root vector relative to the vertical axis. Algorithm 5 formalizes the bend detection criteria. 

#### **Fly-Kiss** 

This gesture is detected via its characteristic two-phase sequence: hand-to-head proximity followed by a forward projection motion. Algorithm 6 summarizes the fly-kiss detector. 

19 

#### **C.3.2. Hyperparameter Justification** 

The hyperparameters for these detection algorithms, detailed in Table S6, were empirically determined by tuning on a randomly sampled validation subset of 50 annotated interaction sequences drawn from the full dataset. The values were selected to maximize the alignment between our automated metrics and the consensus of three human evaluators, ensuring a robust and meaningful evaluation that reflects human judgment of interaction success. 

## **D. Dataset Retargeting for Sim-to-Real** 

**Protocol.** We keep _Act_ unchanged. _Preparation_ is standardized to a neutral upper-body posture (both hands naturally placed in front of the root on the left/right sides), with identical lower-body motion; the root is retargeted to milder yaw and simpler walking. The last 16 frames bilinearly transition into the first frame of the _Act_ . _Follow-up_ becomes stationary while the upper body bilinearly returns over 16 frames to the same neutral posture. 

**Pseudo-code.** Algorithm 7 summarizes the retargeting routine. 

## **E. Observation & Action Specification** 

**Observation and action specification.** We use human root translation (3D) and SMPL joint positions (72D) as the human observation channels, combined with robot proprioception. The reference action is 36-D (29-DoF joint targets + root translation/orientation). Table S1 lists the exact channels and dimensionalities. 

## **F. Temporal Scheduler: Densify and Fuse (within D-STAR)** 

**Diffusion details.** The diffusion-based planning head is trained with a DDIM scheduler [26] using 50 training time steps and 10 inference steps with a squared-cosine schedule. We use group normalization throughout the denoiser and adopt standard sinusoidal timestep embeddings. **Runtime pipeline.** The policy emits 5 anchors per invocation, covering 0–2.0 s with a 0.5 s step; the policy runs at 5 Hz. Anchors are densified to 50 Hz and bilinearly fused across overlapping calls to ensure temporal continuity; zero-order hold is applied if updates are delayed and root-velocity bounds are temporarily tightened. 

**Densification (per call at** _tk_ **).** Algorithm 8 interpolates each 5-anchor policy output to a 50 Hz reference trajectory. 

**Cross-call fusion (between** _tk_ **and** _tk_ +1 **, 5 Hz).** Algorithm 9 bilinearly fuses overlapping dense segments to ensure continuity. 

20 

Table S6. Detection Algorithm Hyperparameters 

|**Task**|**Parameter**|**Value**|**Description**|
|---|---|---|---|
||_τhand_<br>_~~d~~ist_|0.5m|Maximum distance between hands for double embrace|
|Hu|_τbody_|0.45m|Hand to robot torso threshold|
|g|_τshoulder_|0.4m|Hand to shoulder distance for shoulder embrace|
||_τmin_<br>_~~f~~rames_|3|Minimum consecutive frames for a successful embrace|
||_τcontact_|0.4m|Maximum hand-to-hand distance for contact|
|High-Five|_τmin_<br>_~~a~~pproach_<br>_τmax_<br>_~~s~~ustained_|1<br>1000|Minimum frames of valid contact approach<br>Maximum frames of sustained contact (to rule out holding)|
||_τheight_|0.3m|Minimum hand height above human’s root|
||_τcontact_|0.3m|Maximum hand-to-hand contact distance|
||_τmin_<br>_~~c~~ontact_|10|Minimum consecutive frames of sustained contact|
|Handshake|_τmin_<br>_~~d~~ist_|0.4m|Minimum distance between agent roots|
||_τmax_<br>_~~d~~ist_|1.5m|Maximum distance between agent roots|
||_τstd_<br>_~~c~~ontact_|0.15m|Upper bound of contact-distance standard deviation (stability)|
||_τmean_<br>_~~c~~ontact_|0.45m|Upper bound of contact-distance mean(stability)|
||_τmotion_<br>_~~d~~ist_|0.5m|Minimum total distance traveled by the waving hand|
||_τmin_<br>_~~c~~hanges_|3|Minimum number of significant direction changes|
|Wave|_τamplitude_|0.3m|Minimum motion amplitude (peak-to-peak)|
||_τangle_|0.785 rad|Angle threshold for detecting a direction change (_π/_4)|
||_τheight_|0.45m|Minimum hand height above human’s root|
|Bd|_τmin_<br>_~~a~~ngle_|0.349 rad|Minimum bend angle from vertical (_π/_6)|
|en|_τmin_<br>_~~f~~rames_|5|Minimum consecutive frames angle is above threshold|
||_τhand_2_head_|0.3m|Maximum distance from hand to head for Phase 1|
|Fly-Kiss|_τforward_<br>_~~t~~hresh_|0.1m|Minimum total forward motion projected towards partner|
||_τmin_<br>_~~f~~orward_|5|Minimum consecutive frames of forward hand motion in Phase 2|


**Algorithm 1** Hug Detection with Multi-Modal Embrace Recognition 

**Require:** Human joints **J** _H_ , robot torso position **p** _R_ 

**Ensure:** Success flag _successhug_ 

- 1: Extract hand positions: **h** _L,_ **h** _R ←_ **J** _H_ [ _jointshand_ ] 

- 2: _double_ _~~e~~ mbrace ←_ DetectDoubleEmbrace( **h** _L,_ **h** _R,_ **p** _R_ ) 

- 3: _single_ _~~e~~ mbrace ←_ DetectSingleEmbrace( **h** _L,_ **h** _R,_ **p** _R_ ) 

- 4: _shoulder_ _~~e~~ mbrace ←_ DetectShoulderEmbrace( **h** _L,_ **h** _R,_ **p** _R_ ) 

- 5: **return** _double_ _~~e~~ mbrace ∨ single_ _~~e~~ mbrace ∨ shoulder_ _~~e~~ mbrace_ 

- 6: **procedure** DETECTDOUBLEEMBRACE( **h** _L,_ **h** _R,_ **p** _R_ ) 

- 7: _dhands ←∥_ **h** _L −_ **h** _R∥_ 2 

   - Distance between hands 

- 8: _dL_ 2 _robot ←∥_ **h** _L −_ **p** _R∥_ 2, _dR_ 2 _robot ←∥_ **h** _R −_ **p** _R∥_ 2 

- 9: _hands_ _~~c~~ lose ← dhands < τhand_ _~~d~~ ist_ 

- 10: _hands_ _~~n~~ ear_ _~~r~~ obot ←_ ( _dL_ 2 _robot < τbody_ ) _∧_ ( _dR_ 2 _robot < τbody_ ) 

- 11: _embrace_ _~~f~~ rames ← hands_ _~~c~~ lose ∧ hands_ _~~n~~ ear_ _~~r~~ obot_ 

- 12: **return** MaxConsecutiveFrames( _embrace_ _~~f~~ rames_ ) _≥ τmin_ _~~f~~ rames_ 

- 13: **end procedure** 

21 

|**Algo **|**rithm 2**Handshake Detection with Spatial Validation||
|---|---|---|
|**Req**<br>|**uire:** Human hands**h**_L,H,_**h**_R,H_, robot hands**h**_L,R,_**h**_R,R_, human root**r**_H_<br>l||
|**Ensu**|**re:** Success flag_successhandshake_||
|1: _d_<br>2: _c_<br>3: _s_<br>4: **r**|_min ←_ComputeMinHandDist(**h**L,H_,_**h**R,H_,_**h**L,R_,_**h**R,R)<br>_ontact_<br>_~~p~~hase ←_DetectContactPhase(_dmin,_**r**_H_)<br>_tability_<br>_~~p~~hase ←_DetectStabilityPhase(_dmin,_**r**_H_)<br>**eturn**_contact_<br>_~~p~~hase ∧stability_<br>_~~p~~hase_||
|5:|**procedure**DETECTCONTACTPHASE(_dmin,_**r**_H_)||
|6:|_contact_<br>_~~f~~rames ←dmin < τcontact_||
|7:|Validate each contact frame with root distance constraint:||
|8:|**for**_t ∈contact_<br>_~~f~~rames_**do**||
|9:|**h**_active ←_GetActiveHand(_t_)|_▷_Hand with min dist|
|10:|_droot ←∥_**h**_active −_**r**_H_[_t_]_∥_2||
|11:|_contact_<br>_~~f~~rames_[_t_]_←_(_droot ≥τmin_<br>_~~d~~ist_<sup>)</sup><sup>_∧_(</sup><sup>_d_</sup>_root _<sup>_≤τ_</sup>_max_<br>_~~d~~ist_<sup>)</sup>||
|12:|**end for**||
|13:|_valid_<br>_~~c~~ontact_<br>_~~c~~ount ←_<sup>�</sup>_contact_<br>_~~f~~rames_||
|14:|_max_<br>_~~c~~onsecutive ←_MaxConsecutiveFrames(_contact_<br>_~~f~~rames_)||
|15:|**return**(_valid_<br>_~~c~~ontact_<br>_~~c~~ount ≥τmin_<br>_~~c~~ontact_<sup>)</sup><sup>_∧_(</sup><sup>_max_</sup><br>_~~c~~onsecutive ≥τmin_<br>_~~c~~ontact_<sup>)</sup>||
|16: **e**|<br><br><br>**nd procedure**||
|17:|**procedure**DETECTSTABILITYPHASE(_dmin,_**r**_H_)||
|18:|_contact_<br>_~~f~~rames ←dmin < τcontact_||
|19:|_d_<br>_~~s~~eq ←dmin_[_contact_<br>_~~f~~rames_]||
|20:|_stability_<br>_~~s~~td ←_RollingStd(_d_<br>_~~s~~eq_)||
|21:|_stability_<br>_~~m~~ean ←_RollingMean(_d_<br>_~~s~~eq_)||
|22:<br>23: **e**|**return**(Std(_d_<br>_~~s~~eq_)_< τstd_<br>_~~c~~ontact_<sup>)</sup><sup>_∧_(Mean(</sup><sup>_d_</sup><br>_~~s~~eq_)_< τmean_<br>_~~c~~ontact_<sup>)</sup><br>**nd procedure**||


#### **Algorithm 3** High-Five Detection with Height Validation 

- **Require:** Human hands **h** _L,H ,_ **h** _R,H_ , robot hands **h** _L,R,_ **h** _R,R_ , human root **r** _H_ **Ensure:** Success flag _successhighfive_ 1: Compute all hand-to-hand distances: 2: _dLL ←∥_ **h** _L,H −_ **h** _L,R∥_ 2, _dLR ←∥_ **h** _L,H −_ **h** _R,R∥_ 2 3: _dRL ←∥_ **h** _R,H −_ **h** _L,R∥_ 2, _dRR ←∥_ **h** _R,H −_ **h** _R,R∥_ 2 4: _dmin ←_ min( _dLL, dLR, dRL, dRR_ ) 5: _close_ _~~f~~ rames ← dmin < τcontact_ 

6: **if** height ~~v~~ alidation ~~e~~ nabled **then** 

- 7: _valid_ _~~f~~ rames ←_ ValHandHeight( _close_ _~~f~~ rames,_ **h** L,H _,_ **h** R,H _,_ **h** L,R _,_ **h** R,R _,_ **r** H) 

8: _close_ _~~f~~ rames ← close_ _~~f~~ rames ∧ valid_ _~~f~~ rames_ 9: **end if** 

10: _contact_ _~~c~~ ount ←_<sup>�</sup> _close_ _~~f~~ rames_ 

11: _consecutive_ _~~c~~ ount ←_ MaxConsecutiveFrames( _close_ _~~f~~ rames_ ) 

- 12: **return** ( _contact_ _~~c~~ ount ≥ τmin_ _~~a~~ pproach_<sup>)</sup><sup>_∧_(</sup><sup>_consecutive_</sup> _~~c~~ ount ≤ τmax_ _~~s~~ ustained_<sup>)</sup> 

22 

|**Alg **|**orithm 4**Wave Detection with Motion Pattern Analysis|
|---|---|
|**Req**|**uire:** Human hands**h**_L,H,_**h**_R,H_, human root**r**_H_|
|**Ens**|**ure:** Success flag_successwave_|
|1: <br>2: <br>3:|Select active hand based on motion intensity.<br> _motionL ←_CalculateMotionIntensity(**h**_L,H_)<br> _motionR ←_CalculateMotionIntensity(**h**_R,H_)|
|4:|**h**_active ←_**h**_L,H_ if_motionL.total > motionR.total_else**h**_R,H_<br>|
|5:|_motion_<br>_~~s~~ufficient ←motion.total > τmotion_<br>_~~d~~ist_<br>|
|6: <br>|_direction_<br>_~~c~~hanges ←_DetectDirectionChanges(**h**_active_)<br><br>|
|7:|_amplitude_<br>_~~c~~heck ←_DetectAmplitude(**h**_active_)|
|8: <br>9:|_height_<br>_~~c~~heck ←_DetectHandHeight(**h**_L,H,_**h**_R,H,_**r**_H_)<br> **return**_motion_<br>_~~s~~ufficient ∧direction_<br>_~~c~~hanges ∧amplitude_<br>_~~c~~heck ∧height_<br>_~~c~~heck_|
|10:|**procedure**DETECTDIRECTIONCHANGES(**h**_active_)<br>|
|11:|Compute position changes: ∆**p**_←_diff(**h**_active_)<br>|
|12:|Compute motion angles: _θ ←_arctan 2(∆**p**[:_,_1]_,_∆**p**[:_,_0])|
|13:|_direction_<br>_~~c~~hanges ←_0<br>|
|14:|**for**_i_= 1to len(_θ_)_−_1**do**<br>|
|15:|∆_θ ←|θ_[_i_]_−θ_[_i −_1]_|_|
|16:|**if**∆_θ > π_**then**∆_θ ←_2_π −_∆_θ_|
|17:|**end if**|
|18:|**if**∆_θ > τangle_ and CheckDisplacement(**h**_active, i_)**then**|
|19:|_direction_<br>_~~c~~hanges ←direction_<br>_~~c~~hanges_+ 1|
|20:|**end if**|
|21:|**end for**|
|22:<br>23:|**return**_direction_<br>_~~c~~hanges ≥τmin_<br>_~~c~~hanges_<br> **end procedure**|


- **Algorithm 5** Bend Detection via Head-Root Angular Analysis **Require:** Human head **h** _head_ , human root **r** _H_ **Ensure:** Success flag _successbend_ 1: Compute head-root vectors: **v** _hr ←_ **h** _head −_ **r** _H_ 

- 2: Define vertical axis: **z** _axis ←_ [0 _,_ 0 _,_ 1] 

- 3: Compute bend angles: _θbend ←_ VectorAngle( **v** _hr,_ **z** _axis_ ) 

- 4: _max_ _~~a~~ ngle ←_ max( _θbend_ ) 

- 5: _frames_ _~~a~~ bove_ _~~t~~ hreshold ←_<sup>�</sup> ( _θbend ≥ τmin_ _~~a~~ ngle_<sup>)</sup> 

- 6: _angle_ _~~c~~ ondition ← max_ _~~a~~ ngle ≥ τmin_ _~~a~~ ngle_ 

- 7: _stability_ _~~c~~ ondition ← frames_ _~~a~~ bove_ _~~t~~ hreshold ≥ τmin_ _~~f~~ rames_ 

- 8: **return** _angle_ _~~c~~ ondition ∧ stability_ _~~c~~ ondition_ 

23 

- **Algorithm 6** Fly-Kiss Detection with Motion Projection **Require:** Human hands **h** _L,H ,_ **h** _R,H_ , head **h** _head_ , roots **r** _H ,_ **r** _R_ **Ensure:** Success flag _successflyingkiss_ 1: Select active hand closest to head. 2: _dL_ 2 _head ←_ min( _∥_ **h** _L,H −_ **h** _head∥_ 2) 3: _dR_ 2 _head ←_ min( _∥_ **h** _R,H −_ **h** _head∥_ 2) 4: **h** _active, dmin ←_ ( **h** _L,H , dL_ 2 _head_ ) if _dL_ 2 _head ≤ dR_ 2 _head_ else ( **h** _R,H , dR_ 2 _head_ ) 5: _condition_ _~~A~~ ← dmin ≤ τhand_ 2 _head_ 6: Compute forward direction: **dir** _←_ normalize(mean( **r** _R_ ) _−_ mean( **r** _H_ )) 7: Compute hand motion: ∆ **h** _←_ diff( **h** _active_ ) 8: Forward projections: _proj ←_ ∆ **h** _·_ **dir** 9: _forward_ _~~f~~ rames ← proj >_ 0 

- 10: _consecutive_ _~~f~~ orward ←_ MaxConsecutiveFrames( _forward_ _~~f~~ rames_ ) 11: _total_ _~~f~~ orward_ _~~m~~ otion ←_<sup>�</sup> ( _proj_ [ _proj >_ 0]) 12: _condition_ _~~B~~ ←_ ( _consecutive_ _~~f~~ orward ≥ τmin_ _~~f~~ orward_<sup>)</sup><sup>_∧_(</sup><sup>_total_</sup> _~~f~~ orward_ _~~m~~ otion ≥ τforward_ _~~t~~ hresh_<sup>)</sup> 13: **return** _condition_ _~~A~~ ∧ condition_ _~~B~~_ 

- **Algorithm 7** Retarget(Preparation, Act, Follow-up) 1: Prep _←_ neutralize ~~u~~ pper ~~b~~ ody(Preparation) 2: Prep.root _←_ retarget ~~r~~ oot(Preparation.root, mild ~~y~~ aw, simple ~~w~~ alk) 3: Act _←_ Act 4: Follow _←_ make ~~s~~ tationary(Follow ~~u~~ p) 5: Follow.upper _←_ return ~~t~~ o ~~n~~ eutral(Follow ~~u~~ p.upper) 6: // 16-frame bilinear ramps 7: Prep[ _−_ 16 :] _←_ bilinear ~~r~~ amp(Prep[ _−_ 16 :] _,_ Act[0]) 8: Follow[: 16] _←_ bilinear ~~r~~ amp(Act[ _−_ 1] _,_ Follow[: 16]) **return** concatenation(Prep _,_ Act _,_ Follow) 

- **Algorithm 8** DensifyAndTrack(5 anchors _→_ 100-frame reference) 1: anchors _{_ ( _tk_ + 0 _._ 0 _,_ **q** 0) _,_ ( _tk_ + 0 _._ 5 _,_ **q** 0 _._ 5) _, . . . ,_ ( _tk_ + 2 _._ 0 _,_ **q** 2 _._ 0) _}_ 2: grid _T_ = _{tk_ + _i/_ 50 _| i_ = 0 _, . . . ,_ 99 _}_ 3: **for** _t ∈T_ **do** 4: ( _τ_ 1 _, τ_ 2) _←_ nearest anchor times s.t. _τ_ 1 _≤ t ≤ τ_ 2 5: **q** ˆ( _t_ ) _←_ **bilinear** **~~i~~ nterp** in (time _×_ joint/root) between ( _τ_ 1 _,_ **q** _τ_ 1) _,_ ( _τ_ 2 _,_ **q** _τ_ 2) 6: **end forreturn** _{_ **q** ˆ( _t_ ) _}t∈T_ 

- **Algorithm 9** FuseOverlaps( **q** ˆ _k_ , **q** ˆ _k_ +1) 1: let _T_ overlap = _Tk ∩Tk_ +1 on the 50 Hz grid 2: **for** _t ∈T_ overlap **do** 3: **q** ˜( _t_ ) _←_ **bilinear** **~~i~~ nterp** **~~t~~ ime** (ˆ **q** _k_ ( _t_ ) _,_ ˆ **q** _k_ +1( _t_ ) _, t_ ) 4: **end for** 5: if timeout: **q** ˜( _t_ ) _←_ hold-last and tighten root-velocity bounds **return** fused dense segment **q** ˜( _t_ ) 

24 

