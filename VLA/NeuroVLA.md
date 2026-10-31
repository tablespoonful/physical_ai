---
title: "NeuroVLA: A Brain-inspired Embodied Intelligence for Fluid and Fast Reflexive Robotics Control"
date: "2026-01-21"
authors: "Weiyu Guo; He Zhang; Pengteng Li; Tiefu Cai; Ziyang Chen; Yandong Guo"
url: https://arxiv.org/abs/2601.14628
pdf: https://arxiv.org/pdf/2601.14628
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.14628)** / [論文ページ](https://arxiv.org/abs/2601.14628)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **NeuroVLA: A Brain-inspired Embodied Intelligence for Fluid and Fast Reflexive Robotics Control** 

**Weiyu Guo**<sup>1,4</sup> **, He Zhang**<sup>1,4</sup> **, Pengteng Li**<sup>1,4</sup> **, Tiefu Cai**<sup>1,4</sup> **, Ziyang Chen**<sup>1,4</sup> **, Yandong Guo**<sup>1,4</sup> **, He Xiao**<sup>4</sup> **, Yongkui Yang**<sup>3*</sup> **, Ying Sun**<sup>1,2*</sup> **, and Hui Xiong**<sup>1,2*</sup> 

1The Thrust of Artificial Intelligence, The Hong Kong University of Science and Technology (Guangzhou), Guangzhou, China. 

2The Department of Computer Science and Engineering, The Hong Kong University of Science and Technology, Hong Kong, China 

3Shenzhen Institutes of Advanced Technology, Chinese Academy of Sciences, Shenzhen, China 

- 4AI2 Robotics, Shenzhen, China 

*The corresponding authors (yk.yang@siat.ac.cn, yings@hkust-gz.edu.cn, xionghui@ust.hk). 

## **ABSTRACT** 

Vision-language-action (VLA) models inherit powerful semantic representations from large language models, but carrying over their design priorities can leave the demands of physical control under-specified. Stable manipulation requires high-frequency proprioceptive feedback and persistent motor state, in addition to instruction understanding. Here we introduce Neuromorphic Vision-Language-Action (NeuroVLA), a brain-inspired architecture that couples a cortical vision-language planner to recurrent cerebellar modulation and a stateful spiking spinal controller. These components translate semantic intent into actions while incorporating high-frequency proprioceptive and force feedback, maintaining short-term motor memory, and enabling local responses to unexpected contact. In simulated and physical manipulation tasks, the cerebellar module reduces mean commanded jerk by 75.6%, and NeuroVLA achieves a 54.8% collision-recovery rate compared with 0.0% for the evaluated VLA baselines. The spinal controller implemented on an FPGA-based neuromorphic processor achieves 2.19 ms inference latency and 0.87 mJ per inference, corresponding to approximately 0.4 W during inference. These results motivate moving beyond inherited language-model design priorities toward embodied architectures that explicitly integrate semantic planning, high-frequency bodily feedback, motor memory, and local correction. 

## **1 Introduction** 

Vision-language-action (VLA) models extend pretrained language and vision-language models to robotic control, transferring semantic knowledge and instruction-following capabilities<sup>1,2</sup> . Their action interfaces range from token prediction to specialized continuous-action experts<sup>3–5</sup> . We argue that this productive continuity can also create _architectural inertia_ : design priorities established for language modeling continue to shape embodied systems, even when physical interaction calls for different feedback rates, internal states, and response pathways. Larger semantic models and more expressive action outputs do not, by themselves, specify how a controller should sense rapid bodily changes, retain motor context, or react locally to contact. 

Embodied intelligence therefore requires explicit attention to the design of the motor system. High-frequency proprioception grounds control in the current physical state; persistent motor dynamics retain the recent history needed for coordinated execution; and local feedback pathways support rapid correction between semantic updates. These are engineering counterparts of biological sensorimotor principles, including the stateful, practiced execution often described as “muscle memory.” Their relevance is concrete: pouring liquid requires continuous stabilization as the load changes, shaking a flask requires tracking the phase and progress of repeated motions, and recovering from contact requires responding before a slow visual inference cycle completes. 

These tasks expose three related control bottlenecks. First, low-rate, vision-dominant feedback can miss rapid changes in joint state or contact force, allowing oscillation and trajectory drift to persist. Second, action decoders without persistent motor state must infer temporal progress from successive observations, making rhythmic and partially occluded tasks difficult. Third, routing every fine-grained adjustment through a large foundation model couples response time and computational cost to semantic inference. Efficient decoding and execution strategies address aspects of these problems<sup>6,7,49</sup> ; a complementary approach is to give local motor control access to bodily feedback and its own temporal state. 

Biological motor systems motivate this separation of responsibilities. Cortical planning interacts with cerebellar prediction and correction, while spinal circuits integrate descending commands with local feedback<sup>8,11,44</sup> . We adopt these functional principles without assuming a one-to-one correspondence between engineered modules and anatomical subdivisions. In 

1 


**Figure 1. Semantic planning coupled to feedback-driven motor control. a,** Conceptual separation of high-dimensional semantic computation and local sensorimotor processing. The schematic illustrates the intended CUDA/neuromorphic partition; in the evaluated implementation, the cortical and cerebellar modules run on the CUDA tier, and hardware measurements concern the FPGA-based spinal controller. **b,** Information flow in NeuroVLA. A cortical vision-language module generates compact intention tokens; recurrent cerebellar modulation combines these tokens with proprioceptive history; and a stateful spiking spinal module produces continuous actions. The force-feedback pathway supports local contact responses between cortical updates. 

NeuroVLA, a cortical vision-language model supplies compact semantic intent through a Q-Former, a recurrent cerebellar module conditions that intent on proprioceptive history, and a stateful spiking spinal module produces continuous actions (Fig. 1). High-frequency force feedback supports local contact responses, while recurrent and membrane states preserve short-term motor context. This architecture allows motor regulation to operate between semantic updates. 

We test these mechanisms through attention analysis, proprioceptive control traces, temporal ablations, hardware measurements, and physical manipulation tasks. Cerebellar modulation reduces mean commanded jerk by 75.6%; multi-step spiking dynamics improve task success over a single-step variant; and the FPGA-based spinal controller performs inference in 2.19 ms at 0.87 mJ per inference. On physical hardware, NeuroVLA outperforms the evaluated VLA baselines and achieves 54.8% recovery in a collision stress test, compared with 0.0% for those baselines. Together, these results identify feedback bandwidth, persistent motor state, and local correction as useful complements to high-level instruction understanding. 

## **2 Results** 

### **2.1 A Brain-inspired VLA with Event-driven Sparsity** 

NeuroVLA separates semantic interpretation, feedback-based modulation, and action generation (Fig. 1). The cortical module processes images and language instructions with a pretrained vision-language model. A Q-Former extracts compact, taskrelevant intention tokens from its hidden representations<sup>16</sup> , providing the downstream controller with an action-oriented semantic interface. 

The cerebellar module integrates a history of joint states and force/torque measurements through recurrent dynamics. Gated feature-wise linear modulation then adjusts the semantic latent according to the current physical context. This mechanism makes local stabilization and contact-aware correction possible without requiring a new cortical inference for every adjustment. Its functional inspiration is cerebellar prediction and feedback control<sup>11,17</sup> . 

The spinal module converts the modulated latent into continuous actions using stateful spiking neurons. Membrane dynamics carry information across control steps, while selective spiking activity provides an event-driven execution substrate. In the implementation described in Methods, cortical and cerebellar computations run on the CUDA tier, and the spinal controller is validated on an FPGA-based neuromorphic processor. The following experiments examine semantic selection, feedback modulation, temporal integration, and physical performance in turn; architectural details are provided in Methods 4. 

**2/14** 


**Figure 2. Instruction-dependent spatial selection by the Q-Former. a, b,** Attention during “Put the wine bottle on the cabinet”: focus shifts from the manipulation target to the placement surface as execution progresses. **c, d,** Under “Open the middle drawer” in the same scene, attention concentrates on the drawer handle despite the nearby bottle. These maps illustrate task-dependent selection of spatial features for downstream motor control. 

### **2.2 Task intent drives top-down attentional gating of spatial primitives** 

To examine how semantic intent selects spatial information, we visualized the Q-Former’s cross-modal attention under different instructions in the same scene (Fig. 2). For “Put the wine bottle on top of the cabinet,” attention first concentrated on the bottle and then shifted toward the placement surface as execution progressed. When the instruction changed to “Open the middle drawer,” attention instead concentrated on the drawer handle despite the bottle remaining visible. 

These observations show instruction-dependent spatial selection, consistent with the Q-Former’s role as an information bottleneck between visual-language features and motor control. They support task-relevant filtering before feedback-based motor modulation and action generation. 

### **2.3 Proprioceptive feedback stabilizes motion and supports local correction** 

To investigate the mechanistic basis of the system’s robustness, we examined three control functions: stabilization during free-space motion, local correction after contact, and temporal coordination during rhythmic manipulation. These functions motivate the cerebellar design, but the experiments assess robot behaviour rather than identifying separate anatomical loops. 

#### **_Proprioceptive stabilization of ongoing motion_** 

We first tested whether feedback-based modulation reduces high-frequency fluctuations in commanded motion. In free-space trajectories, the baseline policy produced pronounced acceleration oscillations, whereas activating the cerebellar module attenuated these fluctuations (Fig. 4a). 

Using end-effector pose, joint angles, and joint velocities as state feedback, the module reduced mean commanded jerk by 75.6%, with reductions of 80.2% in ∆ _yaw_ and 80.0% in ∆ _Z_ (Fig. 4b). Mean Absolute Commanded Acceleration (MACA) decreased by 32.8% to 58.0% across axes (Fig. 4c). These measurements demonstrate smoother command trajectories under the evaluated conditions. 

#### **_Force-aware correction after unexpected contact_** 

We next tested whether local force feedback enables adaptation when an intended trajectory is obstructed. Contact generated sharp perturbations in the 6-DoF wrench profile (Fig. 3b), including mean force values of _µ ≈−_ 37 _._ 02 in _Fx_ and _µ ≈_ 8 _._ 30 in _Fy_ , with variance _σ_<sup>2</sup> _≈_ 3 _._ 27 in _Fy_ . 

The vision-centric baseline continued along the blocked path (red dashed line). NeuroVLA used the high-frequency ( _>_ 200 Hz) force stream to adjust the local trajectory and navigate around the contact point (blue solid line). This result supports force-aware motor correction through the feedback pathway. The force/torque sensor measures contact state; it is not treated as a substitute for a biological vestibular organ. 

#### **_Temporal coordination during rhythmic manipulation_** 

In the “Shake the cup” task, three oscillatory cycles were visible in synchronized wrench and joint-angle traces (Fig. 3a). The alignment of these trajectories indicates coordinated rhythmic execution, including periods when visual feedback was static or occluded. These synchronized traces demonstrate coordinated rhythmic execution; the spinal temporal contribution is assessed by the ablation below. 

Under degraded visual observations, the cerebellar-enhanced agent also maintained higher success than the evaluated cortical baselines (Fig. 5e). This supports the usefulness of proprioceptive context when visual information is unreliable. The 

**3/14** 


**Figure 3. Temporal coordination and force-aware trajectory correction. a,** Wrench and joint-angle traces during “Shake the cup” show synchronized oscillatory cycles, providing a sensorimotor description of rhythmic execution. **b,** Contact produces a wrench transient. The local feedback pathway adjusts the subsequent trajectory (blue solid line), whereas the baseline continues along the obstructed path (red dashed line). These examples assess temporal coordination and contact-aware correction in the engineered controller. 

temporal contribution of the spinal dynamics is examined separately through the following ablation. 

### **2.4 Event-driven sparsity and temporal integration in the neuromorphic spinal substrate** 

We next examined whether spinal activity follows actuation demand and whether persistent spiking state contributes to task performance. During “Static Pose & Dynamic Gripper” phases, end-effector pose neurons remained relatively quiescent while gripper-control neurons fired more actively (Fig. 5a,b). Mean activation rates were lower during static holding than during dynamic actions (Fig. 5c). These observations demonstrate selective, demand-dependent neural activity; hardware energy consumption is evaluated separately below. 

Stateful spiking neurons carry temporal information by accumulating and decaying membrane voltage<sup>19</sup> . On LIBERO<sup>23,37</sup> , the multi-step SNN achieved higher success than a single-step variant, particularly in tasks requiring transitions between manipulation phases (Fig. 5d). The same panel includes a no-cerebellum baseline. The temporal ablation supports the contribution of persistent spiking state, while the complementary baseline evaluates the contribution of cerebellar modulation. 

Firing-rate maps conditioned on kinematic dimensions showed distinct activation patterns (Fig. 6, Neural Representation of Action), and t-SNE projections separated several action-associated latent states (Action Latent Cluster). These visualizations suggest functional specialization within the learned controller. They provide descriptive evidence of representation structure rather than demonstrating a biological somatotopic map or establishing the cause of the performance gains. 

### **2.5 Hardware validation of the spiking spinal controller** 

We implemented the spinal controller on an FPGA-based neuromorphic processor (Fig. 7a). Its systolic array updates multiple leaky integrate-and-fire neurons<sup>29</sup> in parallel, reusing spikes across columns and weights across rows (Fig. 7b). A spike-detection module suppresses inactive events to reduce unnecessary updates<sup>41,42</sup> . 

At an operating frequency of 20 MHz, the processor achieved 2.19 ms inference latency and 0.87 mJ per inference, corresponding to approximately 0.4 W during inference. Resource utilization and performance are summarized in Fig. 7c,d. These measurements characterize the spinal controller on the FPGA implementation; they do not include cortical and cerebellar GPU computation, sensing, communication, or robot actuation. 

**4/14** 


**Figure 4. Proprioceptive modulation reduces fluctuations in commanded motion. a,** Commanded acceleration traces in translational and rotational dimensions with the baseline policy (red) and cerebellar modulation (blue). **b, c,** Mean Absolute Commanded Jerk and Mean Absolute Commanded Acceleration. Mean jerk decreases by 75.6%, and acceleration decreases by 32.8%–58.0% across axes. These metrics characterize command smoothness under the evaluated conditions. 

### **2.6 Physical manipulation and collision recovery** 

We deployed NeuroVLA on a physical bimanual humanoid platform to test spatial precision, fluid handling, and rhythmic execution (Fig. 8a–f). Across the evaluated tasks, it achieved higher success than OpenVLA<sup>2</sup> , OpenVLA-OFT<sup>20</sup> , UniVLA<sup>22</sup> , and WorldVLA<sup>21</sup> . 

During pouring (Fig. 8c), changing loads and visual occlusion challenged stable execution. The cerebellar module integrated proprioceptive feedback at 200 Hz, allowing motor commands to be adjusted as the physical state changed. In flask shaking (Fig. 8e), coordinated repeated motions were consistent with the temporal context provided by the recurrent and spiking states. These task observations complement the stabilization measurements and temporal ablation above. 

We then introduced an unexpected obstruction during the “Recover to Safe Area” task (Fig. 8g). The evaluated VLA baselines achieved 0.0% recovery and often continued executing the obstructed trajectory. NeuroVLA achieved 54.8% recovery. Following a wrench transient, the local cerebellar–spinal pathway generated a withdrawal response with a reported latency below 50 ms, bypassing the cortical inference loop ( _>_ 200 ms). Local trajectory correction then supported recovery and task continuation. 

Together with the other physical tasks, the collision result supports the use of bodily feedback and local motor state to complement semantic instruction following. The limits of recovery are considered in the Discussion. 

## **3 Discussion** 

### **Beyond architectural inertia from language modeling** 

The success of language-model pretraining makes its architectures and scaling strategies a natural starting point for embodied intelligence. However, this starting point can become a constraint if motor competence is treated primarily as an extension of semantic sequence generation. Our results motivate a broader design agenda: high-frequency proprioceptive sensing, persistent motor state, and local corrective pathways should be explicit architectural components, rather than capabilities assumed to emerge from semantic scaling alone. This position complements progress in vision-language reasoning and continuous-action experts by addressing the bodily interface through which their outputs are executed. 

NeuroVLA addresses the resulting mismatch between semantic inference and physical interaction. The Q-Former supplies task-relevant intent, recurrent cerebellar modulation incorporates bodily feedback, and stateful spinal dynamics generate 

**5/14** 


**Figure 5. Selective spiking activity and temporal ablation. a,** Membrane potentials and spike trains during “Static Pose & Dynamic Gripper” show relatively quiescent end-effector pose neurons and active gripper-control neurons. **b,** Firing rates across end-effector and gripper conditions quantify demand-dependent activity. **c,** Mean activation rates are lower in static than dynamic phases. **d,** LIBERO task success with a multi-step SNN, a single-step variant, and a no-cerebellum baseline. **e,** Task success under noisy observations compares NeuroVLA with the evaluated VLA baselines. Temporal ablation and noisy-observation evaluation test different aspects of the control architecture. 

continuous actions. Attention maps, command-smoothing measurements, temporal ablations, and collision tests provide complementary evidence for these roles. The contribution is an engineered control architecture whose feedback bandwidth and temporal state are matched to motor demands, rather than a demonstration that instruction understanding alone yields stable control. 

The cortex, cerebellum, and spinal cord provide functional inspiration for this division of responsibilities<sup>11,44</sup> . Our implementation does not reproduce their detailed anatomy or identify a one-to-one mapping to spinocerebellar, vestibulocerebellar, or cerebrocerebellar circuits. Biological correspondence should therefore be interpreted as a design hypothesis, with the engineering claims assessed by the robot experiments. 

### **Motor memory and efficient execution** 

The term “muscle memory” motivates a concrete design requirement here: a motor controller should retain execution-relevant state and use recent sensorimotor history to shape its next action. In NeuroVLA, recurrent proprioceptive context and persistent membrane dynamics provide this short-term motor memory. The temporal ablation supports the usefulness of retained state for task execution; it does not establish the long-term skill consolidation associated with biological motor learning. Distinguishing these timescales makes the analogy testable and links it to implementable control mechanisms. 

The multi-step ablation supports the value of persistent motor state, while selective firing shows how neural activity can follow actuation demand. FPGA measurements establish low latency and energy use for the spinal controller. These findings support hardware-efficient local execution, but low spinal power does not imply that the complete VLA system or robot operates at the same power. The hardware inference measurement is also distinct from end-to-end collision-response latency. 

### **Limits of local recovery and future work** 

Local force feedback improved recovery in the tested contact scenario, yet a 54.8% success rate does not establish a general safety guarantee. Broader perturbation tests and explicit sensing-to-actuation latency measurements would better characterize the operating limits. Comparisons in this study concern the selected baselines and tasks, rather than all VLA architectures. 

Training currently relies on offline behaviour cloning and GPU-based surrogate gradients. Although the spinal controller is validated on an FPGA-based neuromorphic processor, the cortical and cerebellar modules remain on the CUDA tier. Online plasticity and deployment of additional control components on neuromorphic hardware are future directions<sup>35</sup> . Simulation 

**6/14** 

Neural Representation of Action: Activation Maps vs. Latent Structure 


**Figure 6. Action-associated structure in spinal representations. Neural Representation of Action:** Rearranged firing-rate maps show different activation patterns for kinematic dimensions such as _|_ ∆ _Roll|_ and _|_ Gripper _|_ . **Action Latent Cluster:** A t-SNE projection of spinal hidden states separates several action-associated groups. These visualizations describe action-associated organization in the learned motor representation. 

studies that independently vary proprioceptive feedback rate, sensory delay, recurrent state, and spiking state would help separate their contributions to stable, temporally coordinated manipulation. Such tests would evaluate the proposed sensorimotor design principles directly, alongside subsequent validation on physical hardware. 

## **4 Methods** 

### **4.1 Architecture Overview** 

We formalize the embodied control task as a Partially Observable Markov Decision Process (POMDP)<sup>36</sup> . At each time step _t_ , the agent receives a multimodal observation tuple _ot ∈_ O, comprising high-dimensional visual sensory data _It ∈_ R<sup>_H×W×_3</sup> , a natural language instruction _L_ , and a history of low-dimensional proprioceptive states **s** _t−H_ : _t ∈_ R<sup>_H×Ds_</sup> , where _H_ denotes the size of history window and _Ds_ represents the dimensions of joint positions, velocities, and end-effector forces (6-DoF wrench). The objective is to generate a sequence of continuous motor actions **a** _t ∈_ A to maximize the cumulative reward. 

To reconcile the conflicting computational requirements of semantic planning (high-latency, abstract) and motor execution (low-latency, precise), we propose the **Tri-Level Neuromorphic Vision-Language-Action ( NeuroVLA)** architecture. As shown in Fig. 1, the system control policy _π_ ( _at |ot_ ) is decomposed into a hierarchical composition of three specialized mapping functions: 

**a** _t_ = Φspine (Φcerebellum (Φcortex( _It , L_ ) _,_ **h** _t_ )) _,_ 

where Φcortex, Φcerebellum, and Φspine correspond to the cortical, cerebellar, and spinal modules, respectively. **h** _t_ denotes the compact dynamic context vector from the neurological state estimator. This decomposition enforces a strict division of labor across timescales and hardware substrates: 

1. **Cortical Semantic Projection (** Φ **cortex):** Operates on the CUDA Computing Tier. It maps the visual-linguistic inputs ( _It , L_ ) into a semantic latent intention space **z** sem _∈_ R<sup>_D_model</sup> , where _D_ model denotes the dimension of model internal feature space. This module utilizes a Vision-Language Model (VLM) backbone to extract open-vocabulary affordances, without requiring a new semantic update at every local control step. 

2. **Cerebellar State Modulation (** Φ **cerebellum):** Operates on the CUDA Computing Tier. It functions as a state-dependent affine transformation. A recurrent estimator aggregates the proprioceptive history **s** _t−H_ : _t_ into a dynamic context vector **h** _t_ . This context is then used to modulate the semantic latent **z** sem via a Gated Feature-wise Linear Modulation (FiLM) mechanism, yielding a refined, physics-aware latent code **z** mod. This process is inspired by cerebellar feedback modulation; it conditions the action latent on observed physical state. 

**7/14** 

|**a. FPGA Platform**|**b. Neuromorphic Processor**|**c. FPGA Hardware Resource Utilization**|
|---|---|---|
|||**d. Performance Summary**|


**Figure 7. Neuromorphic processor implemented on an FPGA platform for deploying the Spiking Spinal Module. a,** FPGA board used for implementation. **b,** Neuromorphic processor incorporating an LIF systolic-array architecture and spike-sparsity-aware computation to reduce inference latency and energy consumption. **c,** FPGA resource utilization, with 51,953 LUTs, 27,880 FFs and 169 BRAMs. **d,** Performance summary, showing an inference latency of 2.19 ms at 20 MHz and an energy cost of 0.87 mJ per inference. 

3. **Spinal Neuromorphic Decoding (** Φ **spine):** Operates on Neuromorphic Chip Tier. It maps the modulated latent **z** mod to continuous actions **a** _t_ via a Spiking Neural Network (SNN) governed by Leaky Integrate-and-Fire (LIF) dynamics. This module leverages event-driven sparsity and intrinsic temporal memory to ensure energy-efficient, smooth trajectory generation and rapid reflex responses. 

The entire system is trained end-to-end using a hybrid loss that combines behavior cloning losses with surrogate gradients<sup>27</sup> for the non-differentiable spiking components, ensuring functional coherence across the hierarchy. 

### **4.2 Cortical Module: Semantic Latent Generation** 

The Cortical Module occupies the highest tier of the control hierarchy, tasked with cross-modal reasoning and the synthesis of abstract motor intentions from high-dimensional observations. Unlike lower-level circuits that must react to instantaneous physical dynamics, the cortical layer operates on a semantic timescale, prioritizing long-horizon planning and generalization over high-frequency control. 

#### **_4.2.1 Vision-Language Reasoning Backbone_** 

We leverage a pre-trained Large Vision-Language Model (VLM), specifically Qwen-VL<sup>32</sup> , as the general-purpose reasoning engine. Formally, given the current RGB observation _It_ and the natural language instruction _L_ , the VLM functions as a dense feature extractor: 


where H _t_ = _{ht_<sup>(1)</sup> _,..., ht_<sup>(</sup><sup>_N_)</sup> _}_ represents the stack of hidden states across all _N_ transformer layers and _θ_ vlm denotes the parameters of VLM. This rich representation captures scene geometry cues, object semantics, and linguistic context, providing a multimodal scene representation that supports open-vocabulary reasoning and manipulation. 

#### **_4.2.2 Layer-wise Semantic Distillation_** 

Directly feeding the high-dimensional, variable-length VLM hidden states into a motor policy is computationally prohibitive and prone to overfitting. To bridge the dimensionality gap between the VLM’s linguistic-visual space and the robot’s control manifold, we employ a **Layer-wise Querying Transformer (Q-Former)** . 

The Q-Former acts as a learnable information bottleneck. It utilizes a set of learnable query tokens **Q** _∈_ R<sup>_K×D_</sup> to attend to specific subsets of the VLM’s hidden representations, where _K_ denotes the number of tokens and _D_ denotes the token dimension. Crucially, rather than utilizing only the final layer, we extract features from a designated range of intermediate layer index [ _l_ start _, l_ end] to capture both low-level spatial details and high-level semantic abstractions. The extraction process is formalized as: 


where **z** sem _∈_ R<sup>_K×D_action</sup> denotes the **Semantic Latent Intention** and _θ_ Q-Former denotes the parameters of Q-Former. 

**Design Interpretation:** The Q-Former compresses image-language features into the semantic latent **z** sem, providing task intent to the downstream controller. Physical context is incorporated through the separate cerebellar modulation described below. 

**8/14** 


**Figure 8. Physical manipulation and recovery after unexpected contact. a,** Bimanual laboratory platform and experimental scene. **b–f,** Task success for relocating test tubes (b), pouring liquid (c), organizing laboratory items (d), shaking flasks (e), and discarding test tubes (f), comparing NeuroVLA with OpenVLA, OpenVLA-OFT, UniVLA, and WorldVLA. **g,** Recovery after collision followed by test-tube shaking. NeuroVLA achieves 54.8% recovery compared with 0.0% for the evaluated baselines. The task tests withdrawal and subsequent continuation under an unexpected physical obstruction. 

### **4.3 Cerebellar Module: Gated Recurrent Neuromodulation** 

While the cortical module generates semantic intentions, it operates significantly slower than the dynamics of physical interaction and lacks access to high-frequency proprioceptive feedback. To bridge this gap, the Cerebellar Module functions as an adaptive filter, performing _dynamic state estimation_ and _trajectory refinement_ before the signals reach the spinal execution layer. 

#### **_4.3.1 Proprioceptive State Estimation via Recurrent Dynamics_** 

Inspired by the integration of bodily feedback in biological motor control, we employ a Gated Recurrent Unit (GRU)<sup>34</sup> as a recurrent state estimator. Let **s** _t−H_ : _t ∈_ R<sup>_H×Ds_</sup> denote the history of robot states over a horizon _H_ (aligned with the sensor frequency, e.g., 50 Hz), where each state vector includes joint angles, velocities, and 6-DoF wrench measurements. The estimator integrates this temporal sequence to produce a compact dynamic context vector **h** _t_ : 


where _θ_ gru denotes the parameter of the designed GRU. Unlike static encoders (e.g., MLPs), the GRU captures the _rate of change_ and _contact transients_ (e.g., collision impulses), which are critical for stabilizing motion under perturbation. 

**9/14** 

#### **_4.3.2 Gated Feature-wise Linear Modulation (FiLM)_** 

The core computational role of the cerebellum is to modulate cortical commands based on current physical constraints. We formalize this interaction using a Gated FiLM mechanism<sup>28</sup> . First, to prevent proprioceptive noise from overwhelming semantic intent during stable phases, we employ a learnable gating factor **g** _t_ : 


where _σ_ , _Wg_ and Proj( _·_ ) denote the sigmoid function, the learnable affine transformation matrix and the projection function. This gate selectively regulates how much physical context is allowed to influence the cortical plan. Subsequently, the dynamic context **h** _t_ is projected into affine transformation parameters—scale _γt_ and shift _β t_ —which are applied to the cortical semantic latent **z** sem: 


, where _⊙_ denotes the element-wise Hadamard product. This operation allows the cerebellar module to strictly enforce gain control: for instance, upon detecting a collision (spike in **h** _t_ ), the network can suppress the forward velocity encoded in **z** sem (via _γt ≈−_ 1) and inject a retraction bias (via _β t_ ), effectively rewriting the motor plan in real-time. 

#### **_4.3.3 Iterative Refinement of the Motor Latent_** 

The motor latent is updated through an _Iterative Refinement Loop_ . Given an updated anticipated state, the module Refine( _·_ ) re-applies the two cerebellar computations introduced in Sections 4.3.1 and 4.3.2 to adjust the motor latent. The module performs _K_ cycles of internal recurrence (set to _K_ = 2 in our experiments). In each iteration _k ∈{_ 0 _,..., K −_ 1 _}_ , the module predicts a tentative action latent, updates the anticipated state evolution, and re-modulates the input. Formally: 


The recurrence allows the motor latent to be revised before spinal action decoding. An explicit decomposition into identified gravity, friction, or other physical-model terms is not imposed by this formulation. 

**Design Interpretation:** This architecture uses the functional separation of intended action and bodily feedback. The semantic latent **z** sem provides a descending intention signal, while **h** _t_ summarizes proprioceptive history. FiLM conditions the motor latent on this context. This design is inspired by cerebellar feedback and internal-model accounts<sup>11</sup> ; the formulation does not by itself demonstrate an explicit sensory-prediction-error computation or anatomical equivalence. 

### **4.4 Spinal Module: Spiking Residual Dynamics** 

The Spinal Module serves as the final execution interface, translating the modulated latent intentions **z** mod into continuous motor commands **a** _t_ . Implemented on neuromorphic principles, this module is designed to support energy-efficient event-driven processing and continuous action decoding via intrinsic neuronal dynamics. 

#### **_4.4.1 Stateful Leaky Integrate-and-Fire Dynamics_** 

We model the spinal interneurons using the iterative Leaky Integrate-and-Fire (LIF) formalism. Crucially, the network is instantiated with **stateful membrane dynamics** , meaning the membrane potential _u_<sup>(</sup> _i_<sup>_l_)</sup> is strictly preserved across successive time steps rather than being re-initialized at each forward pass. This endows the spinal substrate with an _implicit temporal working memory_ , allowing it to encode history-dependent features without requiring explicit recurrent gating units (e.g., LSTMs). For a hidden neuron _i_ in layer _l_ at time step _τ_ , the dynamics evolve according to: 


where _β ∈_ (0 _,_ 1) is the membrane decay factor, _wij_ is the synaptic weight, _s_<sup>(</sup> _j_<sup>_l−_1)</sup> [ _τ_ ] _∈{_ 0 _,_ 1 _}_ represents the incoming spike train and _ϑ_ denotes the voltage. The term _u_<sup>(</sup> _i_<sup>_l_)[</sup><sup>_τ −_1] represents the</sup><sup>_residual potential_carried over from the previous moment,</sup> establishing a continuous temporal context. 

#### **_4.4.2 Deep Spiking Residual Architecture_** 

To enable the learning of complex sensorimotor transformations without signal degradation in deep spiking layers, we structure the spinal module as a Spiking ResNet<sup>38,39</sup> . By incorporating residual skip connections: 


We facilitate the direct propagation of gradients and spike rates during training. Residual connections facilitate the propagation of the modulated latent through the spiking layers. 

**10/14** 

#### **_4.4.3 Continuous Integration for Motor Decoding_** 

A critical challenge in applying SNNs to robotics is bridging the gap between discrete, stochastic spikes and the continuous domain of joint actuation. We resolve this by implementing a **Continuous Integration Protocol** at the output layer<sup>40</sup> . Unlike hidden interneurons which undergo rapid repolarization (reset) upon spiking, the output motor neurons are configured as **non-resetting integrators** . They continuously accumulate synaptic influx over the simulation window without discharging their potential: 

**a** _t_ [ _τ_ ] = Wout _·_ **u** out[ _τ_ ] _,_ 

where **u** out represents the accumulated membrane voltage. This mechanism serves two control functions: 

1. **Temporal Smoothing:** The integration process acts as a natural low-pass filter, converting high-frequency spike trains into smooth, continuous motor trajectories. This mirrors the biological process of _twitch summation_ , where muscles integrate neural drive into continuous force, filtering out neural noise. 

2. **Kinematic Consistency:** By maintaining the voltage state, the network naturally enforces temporal consistency in the output action sequence, reducing kinematic jerk and ensuring fluid transitions between control steps. 

#### **_4.4.4 Surrogate Gradient Learning_** 

To overcome the non-differentiability of the spike generation function _s_ = Θ( _u − ϑ_ ), we employ a surrogate gradient method for end-to-end training. During the backward pass, the Heaviside step function is approximated by a fast sigmoid function _σ_ ( _x_ ) = 1+ _<u>x|x|</u>_<sup>,allowinggradientstoflowfromthecontinuousactionspacebackthroughthediscretespinallayerstothe</sup> cerebellar and cortical modules. 

## **Data Availability** 

The simulation datasets used in this study are derived from the open-source **LIBERO** and **LIBERO-Plus** benchmarks. The real-world experimental data collected during the current study are available from the corresponding author upon reasonable request. 

## **Code Availability** 

The code of this paper is available at https://github.com/guoweiyu/NeuroVLA. 

## **Acknowledgements** 

This work was supported in part by the National Key R & D Program of China (Grant No.2023YFF0725001), in part by the National Natural Science Foundation of China (Grant No.92370204), in part by the Guangdong Basic and Applied Basic Research Foundation (Grant No.2023B1515120057), in part by the Education Bureau of Guangzhou. 

## **Author Contributions** 

W.Y.G. proposed the idea of NeuroVLA, implemented the core codebase, and analyzed the results. P.T.L designed the real-world experiments, test the performance and discuss the idea. Z.H,T.F.C and Z.Y.C designed the explainable experiments,analyzed the results and discuss the idea. Y.S, Y.K.Y and H.X supervised the literature review, data processing, methodology, analysis, and discussion. Y.D.G, X.H and H.X managed this project. 

## **Competing Interests** 

The authors declare no competing interests. 

## **Inclusion & Ethics Statement** 

We confirm that this study adheres to all applicable ethical regulations. 

**11/14** 

## **References** 

**1.** Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., Wu, J., Wohlhart, P., Welker, S., Wahid, A. and others. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , 2165–2183 (2023). 

**2.** Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E. P., Sanketi, P. R., Vuong, Q., Kollar, T., Burchfiel, B., Tedrake, R., Sadigh, D., Levine, S., Liang, P., and Finn, C. OpenVLA: An Open-Source Vision-Language-Action Model. In _8th Annual Conference on Robot Learning_ (2024). 

**3.** Xinlong Wang, Yufeng Cui, Jinsheng Wang, Fan Zhang, Yueze Wang, Xiaosong Zhang, Zhengxiong Luo, Quan Sun, Zhen Li, Yuqi Wang, Qiying Yu, Yingli Zhao, Yulong Ao, Xuebin Min, Chunlei Men, Boya Wu, Bo Zhao, Bowen Zhang, Liangdong Wang, Guang Liu, Zheqi He, Xi Yang, Jingjing Liu, Yonghua Lin, Zhongyuan Wang, and Tiejun Huang, “Multimodal learning with next-token prediction for large multimodal models,” _Nature_ **650** , 327–333 (2026). doi: 10.1038/s41586-025-10041-x. 

**4.** Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al., “ _π_ 0 _._ 5: a Vision-Language-Action Model with Open-World Generalization,” _arXiv preprint_ arXiv:2504.16054, 2025. 

**5.** Danny Driess, Jost Tobias Springenberg, Brian Ichter, Lili Yu, Adrian Li-Bell, Karl Pertsch, Allen Z. Ren, Homer Walke, Quan Vuong, Lucy Xiaoyang Shi, et al., “Knowledge insulating vision-language-action models: Train fast, run fast, generalize better,” _arXiv preprint_ arXiv:2505.23705, 2025. 

**6.** W. Zheng, B. Li, B. Xu, E. Feng, J. Gu, and H. Chen, “Leveraging OS-Level Primitives for Robotic Action Management,” arXiv:2508.10259, 2025. [Online]. Available: https://arxiv.org/abs/2508.10259 

**7.** S. Park, H. Kim, S. Kim, W. Jeon, J. Yang, B. Jeon, Y. Oh, and J. Choi, “Saliency-aware quantized imitation learning for efficient robotic control,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2025, pp. 13140–13150. 

**8.** Scott, S. H. Optimal feedback control and the neural basis of volitional movement. _Nature Reviews Neuroscience_ **5** , 532–546 (2004). 

**9.** Todorov, E. Optimality principles in sensorimotor control. _Nature Neuroscience_ **7** , 907–915 (2004). 

**10.** K. Doya, “What are the computations of the cerebellum, the basal ganglia and the cerebral cortex?” in _Elsevier Science Ltd._ , 1999. 

**11.** M. Ito, “Control of mental activities by internal models in the cerebellum,” _Nature Reviews Neuroscience_ , vol. 9, no. 4, pp. 304–313, 2008. doi:10.1038/nrn2332. 

**12.** S. Vahdat, O. Lungu, J. Cohen-Adad, V. Marchand-Pauvert, H. Benali, and J. Doyon, “Simultaneous Brain–Cervical Cord fMRI Reveals Intrinsic Spinal Cord Plasticity during Motor Sequence Learning,” _PLoS Biology_ , vol. 13, 2015. doi:10.1371/journal.pbio.1002186. 

**13.** Vahdat, S., Lungu, O., Cohen-Adad, J., Marchand-Pauvert, V., Benali, H., Doyon, J. Simultaneous brain–cervical cord fMRI reveals intrinsic spinal cord plasticity during motor sequence learning. _PLoS Biology_ **13** , e1002186 (2015). 

**14.** K. Roy, A. Jaiswal, and P. Panda, “Towards spike-based machine intelligence with neuromorphic computing,” _Nature_ , vol. 575, no. 7784, pp. 607–617, 2019. doi:10.1038/s41586-019-1677-2. 

**15.** Bartolozzi, C., Indiveri, G., Donati, E. Embodied neuromorphic intelligence. _Nature Communications_ **13** , 1024 (2022). 

**16.** Li, J., Li, D., Savarese, S., Hoi, S. BLIP-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. _International Conference on Machine Learning_ , 19730–19742 (2023). 

**17.** Garrido, J., Luque, N., D’Angelo, E., Ros, E. Distributed cerebellar plasticity implements adaptable gain control in a manipulation task: A closed-loop robotic simulation. _Frontiers in Neural Circuits_ **7** , 159 (2013). 

**18.** Black, K. _et al. π_ 0 _._ 5: A vision-language-action model with open-world generalization. _9th Annual Conference on Robot Learning_ (2025). 

**19.** Zhao, Q., Zhang, L., Zhang, H., Jiang, H., Cui, K., Wu, Z., Liu, J., Zhao, M., Tian, F., Hu, B. LSNN model: A lightweight spiking neural network-based depression classification model for wearable EEG sensors. _IEEE Transactions on Mobile Computing_ (2025). 

**20.** Kim, M. J., Finn, C., and Liang, P. Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success. _ArXiv_ **abs/2502.19645** (2025). 

**12/14** 

**21.** Cen, J., Yu, C., Yuan, H., Jiang, Y., Huang, S., Guo, J., Li, X., Song, Y., Luo, H., Wang, F., Zhao, D., and Chen, H. WorldVLA: Towards Autoregressive Action World Model. _ArXiv_ **abs/2506.21539** (2025). 

**22.** Wang, Y.-Q., Li, X., Wang, W., Zhang, J., Li, Y., Chen, Y., Wang, X., and Zhang, Z. Unified Vision-Language-Action Model. _ArXiv_ **abs/2506.19850** (2025). 

**23.** Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ **36** , 44776–44791 (2023). 

**24.** Li, J., Li, D., Savarese, S., and Hoi, S. C. H. BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models. In _International Conference on Machine Learning_ (2023). 

**25.** Feldman, D. E. The spike-timing dependence of plasticity. _Neuron_ **75** , 556–571 (2012). 

**26.** Caporale, N. and Dan, Y. Spike timing–dependent plasticity: a Hebbian learning rule. _Annu. Rev. Neurosci._ **31** , 25–46 (2008). 

**27.** Neftci, E. O., Mostafa, H., and Zenke, F. Surrogate gradient learning in spiking neural networks: Bringing the power of gradient-based optimization to spiking neural networks. _IEEE Signal Processing Magazine_ **36** , 51–63 (2019). 

**28.** Perez, E., Strub, F., De Vries, H., Dumoulin, V., and Courville, A. FiLM: Visual reasoning with a general conditioning layer. In _Proceedings of the AAAI conference on artificial intelligence_ **32** , (2018). 

**29.** Abbott, L. F. Lapicque’s introduction of the integrate-and-fire model neuron (1907). _Brain research bulletin_ **50** , 303–304 (1999). 

**30.** Akopyan, F., Sawada, J., Cassidy, A., Alvarez-Icaza, R., Arthur, J., Merolla, P., Imam, N., Nakamura, Y., Datta, P., Nam, G.-J., et al. Truenorth: Design and tool flow of a 65 mw 1 million neuron programmable neurosynaptic chip. _IEEE transactions on computer-aided design of integrated circuits and systems_ **34** , 1537–1557 (2015). 

**31.** Davies, M., Srinivasa, N., Lin, T.-H., Chinya, G., Cao, Y., Choday, S. H., Dimou, G., Joshi, P., Imam, N., Jain, S., et al. Loihi: A neuromorphic manycore processor with on-chip learning. _Ieee Micro_ **38** , 82–99 (2018). 

**32.** Bai, Jinze; Bai, Shuai; Yang, Shusheng; Wang, Shijie; Tan, Sinan; Wang, Peng; Lin, Junyang; Zhou, Chang; Zhou, Jingren. Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond. _arXiv preprint_ arXiv:2308.12966 (2023). 

**33.** Qiu, Z., Wang, Z., Zheng, B., Huang, Z., Wen, K., Yang, S., Men, R., Yu, L., Huang, F., Huang, S., Liu, D., Zhou, J., and Lin, J. Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ (2025). 

**34.** Chung, J., Gulcehre, C., Cho, K., and Bengio, Y. Empirical evaluation of gated recurrent neural networks on sequence modeling. _arXiv preprint arXiv:1412.3555_ (2014). 

**35.** Pei, J., Deng, L., Song, S., Zhao, M., Zhang, Y., Wu, S., Wang, G., Zou, Z., Wu, Z., He, W., et al. Towards artificial general intelligence with hybrid Tianjic chip architecture. _Nature_ **572** , 106–111 (2019). 

**36.** Lauri, M., Hsu, D., and Pajarinen, J. Partially observable markov decision processes in robotics: A survey. _IEEE Transactions on Robotics_ **39** , 21–40 (2022). 

**37.** Fei, S., Wang, S., Shi, J., Dai, Z., Cai, J., Qian, P., Ji, L., He, X., Zhang, S., Fei, Z. and others. Libero-plus: In-depth robustness analysis of vision-language-action models. _arXiv preprint arXiv:2510.13626_ (2025). 

**38.** Fang, W., Yu, Z., Chen, Y., Huang, T., Masquelier, T., and Tian, Y. Deep residual learning in spiking neural networks. _Advances in Neural Information Processing Systems_ **34** , 21056–21069 (2021). 

**39.** Hu, Y., Tang, H., and Pan, G. Spiking deep residual networks. _IEEE Transactions on Neural Networks and Learning Systems_ **34** , 5200–5205 (2021). 

**40.** Guo, W., Sun, Y., Xu, Y., Qiao, Z., Yang, Y., and Xiong, H. SpGesture: Source-Free Domain-adaptive sEMG-based Gesture Recognition with Jaccard Attentive Spiking Neural Network. _Advances in Neural Information Processing Systems_ **37** , 36717–36747 (2024). 

**41.** Rao, A., Plank, P., Wild, A., and Maass, W. A long short-term memory for AI applications in spike-based neuromorphic hardware. _Nature Machine Intelligence_ **4** , 467–479 (2022). 

**42.** Rathi, N., Chakraborty, I., Kosta, A., Sengupta, A., Ankit, A., Panda, P., and Roy, K. Exploring Neuromorphic Computing Based on Spiking Neural Networks: Algorithms to Hardware. _ACM Computing Surveys_ **55** , 1–49 (2022). 

**43.** Liu, Y., Chen, W., Bai, Y., Liang, X., Li, G., Gao, W., Lin, L. Aligning cyber space with physical world: A comprehensive survey on embodied AI. _IEEE/ASME Transactions on Mechatronics_ , 1–22 (2025). 

**13/14** 

**44.** Bruel, A., Abad´ıa, I., Collin, T., Sakr, I., Lorach, H., Luque, N. R., Ros, E., Ijspeert, A. The spinal cord facilitates cerebellar upper limb motor learning and control; inputs from neuromusculoskeletal simulation. _PLOS Computational Biology_ **20** , e1011008 (2024). 

**45.** H. Lorach, A. Galvez, V. Spagnolo, F. Martel, S. Karakas, N. Intering, M. Vat, O. Faivre, C. Harte, S. Komi, J. Ravier,´ T. Collin, L. Coquoz, I. Sakr, E. Baaklini, S. D. Hernandez-Charpak, G. Dumont, R. Buschman, N. Buse, T. Denison, I. V. van Nes, L. Asboth, A. Watrin, L. Struber, F. Sauter-Starace, L. Langar, V. Auboiroux, S. Carda, S. Chabardes,` T. Aksenova, R. Demesmaeker, G. Charvet, J. Bloch, and G. Courtine, “Walking naturally after spinal cord injury using a brain–spine interface,” _Nature_ , vol. 618, pp. 126–133, 2023. 

**46.** Niu, Z., Zhong, G., Yu, H. A review on the attention mechanism of deep learning. _Neurocomputing_ **452** , 48–62 (2021). 

**47.** K. Kawaharazuka _et al._ , “Vision-Language-Action Models for Robotics: A Review Towards Real-World Applications,” _IEEE Access_ , 2025. 

**48.** Yang, S., Wang, J., Zhang, N., Deng, B., Pang, Y., Azghadi, M. CerebelluMorphic: Large-scale neuromorphic model and architecture for supervised motor learning. _IEEE Transactions on Neural Networks and Learning Systems_ **33** , 4398–4412 (2022). 

**49.** Black, K., Galliker, M. Y., Levine, S. Real-time execution of action chunking flow policies. _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ (2025). 

**50.** Suarez, L. E., Richards, B. A., Lajoie, G., Misic, B. Learning function from structure in neuromorphic networks.´ _Nature Machine Intelligence_ **3** , 771–786 (2021). 

**14/14** 

