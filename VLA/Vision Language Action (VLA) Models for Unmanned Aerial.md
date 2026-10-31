---
title: "Vision Language Action (VLA) Models for Unmanned Aerial Robotics and Bimanual Manipulation: A Review"
date: "2026-07-07"
authors: "Inkyu Sa; Chanoh Park; Hea-Min Lee; Donghee Noh; Ho Seok Ahn"
url: https://arxiv.org/abs/2607.06706
pdf: https://arxiv.org/pdf/2607.06706
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2607.06706)** / [論文ページ](https://arxiv.org/abs/2607.06706)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Vision–Language–Action (VLA) Models for Unmanned Aerial Robotics and Bimanual Manipulation: A Review** 

_Review_ 

**Inkyu Sa**<sup>**1,**</sup> *** , Chanoh Park**<sup>**2**</sup> **, Hea-Min Lee**<sup>**3**</sup> **, Donghee Noh**<sup>**3**</sup> **and Ho Seok Ahn**<sup>**4**</sup> 

- 1 Chef Robotics, San Francisco, CA 94103, USA 

- 2 RovifyLab, Gyeonggi 13840, Republic of Korea; chanoh.park@rovifylab.com 

- 3 IT Application Research Center, Jeonbuk Regional Branch, Korea Electronics Technology Institute (KETI), Jeonju 54853, Republic of Korea; lee10849@keti.re.kr (H.-M.L.); dhee.noh@keti.re.kr (D.N.) 

- 4 Department of Electrical, Computer and Software Engineering, University of Auckland, Auckland 1010, New Zealand ; hs.ahn@auckland.ac.nz 

- Correspondence: inkyu@chefrobotics.ai 

## **Highlights** 

## **What are the main findings?** 

- The survey finds that VLA research is converging on continuous, chunked action generation—especially flow-matching and hybrid designs—because they avoid the quantization bottleneck of autoregressive action tokens and the latency burden of multistep diffusion, making them better suited to tightly coordinated bimanual control and transferable to aerial systems. 

- It also finds that progress is driven as much by training strategy as by model architecture: cross-embodiment data diversity and co-training improve downstream generalization more reliably than raw dataset scale alone, while reinforcement learning from autonomous practice is emerging as the key mechanism for surpassing demonstrationlimited performance—that is, achieving higher task success rates, faster execution, and broader generalization than what teleoperated demonstrations alone can support. 

## **What are the implications of the main findings?** 

- These trends suggest that the most promising path for real-world deployment is not a monolithic end-to-end model but a dual-system design that combines a slower reasoning module with a faster action module, enabling both semantic understanding and highfrequency control in manipulation and aerial robotics. 

- Looking forward, the field is likely to expand toward production-grade embodied autonomy through end-to-end drone VLAs, aerial manipulation, memory and world-model integration, standardized bimanual benchmarks, safety certification, and continuous self-improvement pipelines that close the gap between benchmark performance and industrial reliability. 

## **Abstract** 

Academic Editor: Peihu Duan 

Received: 9 April 2026 Revised: 13 May 2026 Accepted: 21 May 2026 Published: 26 May 2026 

**Copyright:** © 2026 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license. 

Vision–Language–Action (VLA) models unify visual perception, natural-language understanding, and action generation within a single foundation model, allowing a robot to follow instructions such as “fold the towel” or “fly to the red building” directly from camera images. Because VLAs inherit world knowledge from internet-scale pre-training, they have become the dominant framework for learning-based manipulation, with bimanual coordination serving as the most demanding testbed: two arms with 7+ degrees of freedom each must move in concert to fold, assemble, and reorient objects. Unmanned aerial robotics faces a structurally similar challenge: a drone must coordinate thrust, attitude, and increasingly gripper commands from visual observations under strict latency and payload constraints. This review covers 183 contributions spanning 2017–2026 and 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

_Drones_ **2026** , _10_ , 412 

2 of 59 

organized along seven dimensions: VLA architectures, training recipes, action representations, bimanual coordination (2022–2026), unmanned aerial vehicle (UAV) navigation and control (2017–2026), language grounding, and cross-cutting concerns including memory and world models. We show that the coordination strategies, training recipes, and action representations developed for bimanual VLAs transfer to unmanned aerial systems and identify fourteen research directions across both domains. 

**Keywords:** Vision–Language–Action models; bimanual manipulation; unmanned aerial robotics; drones; UAV; unmanned systems; robot learning; imitation learning; flow matching 

**Version of Record:** This is the author’s accepted manuscript. The definitive Version of Record was published in _Drones_ **2026** , _10_ (6), 412. https://doi.org/10.3390/drones10060412. This work is licensed under a Creative Commons Attribution 4.0 International License (CC BY 4.0). 

# **1. Introduction** 

Vision–Language–Action (VLA) models use a single foundation model to map camera images and language instructions to robot actions. A VLA processes visual and language inputs through a Vision–Language Model (VLM) pre-trained on internet-scale data then generates motor commands through a learned action head. Because the architecture makes no assumptions about the specific robot, VLAs can control manipulators, mobile robots, and drones with the same model family, enabling robots to assist in homes, factories, and disaster-response scenarios. 

To date, the vast majority of VLA research has focused on manipulation, and bimanual coordination in particular. Bimanual tasks (folding laundry, assembling boxes, clearing tables) require two 7+-degree-of-freedom arms to move in concert under partial observability, making them among the most challenging testbeds for VLA models. This concentration of research effort means that bimanual manipulation is where VLA architectures, training recipes, and action representations are best understood. We therefore devote the first application section of this review to a detailed analysis of VLAs for bimanual manipulation. 

We then extend the analysis to unmanned aerial robotics, where the same VLA ideas are now being adopted. The connection between the two domains is not merely conceptual. Coordinating two arms and coordinating a drone fleet both require generating coupled multi-agent actions from shared observations. The action chunking methods that produce smooth bimanual trajectories also produce smooth flight paths. Drones with grippers or robotic arms face both challenges at once, stabilizing flight while manipulating objects. The training recipes (pre-training on diverse data, sim-to-real transfer, reinforcement learning from practice) are shared. Language grounding is also unified: the same VLM mechanisms that interpret “fold the shirt neatly” for a manipulator interpret “fly to the red building and inspect the roof” for a drone. Reviewing bimanual VLAs first provides the vocabulary and analytical framework that makes the aerial discussion concrete. 

**Progress in manipulation VLAs.** The field has moved quickly. **RT-2** (2023) [1] first showed that a VLM can be fine-tuned to output robot actions. _π_ 0 (2024) [2] introduced flow matching, a method that learns to transform random noise into robot actions. It reached state-of-the-art bimanual performance on tasks like laundry folding and box assembly. _π_ 0.5 (2025) [3] deployed VLAs in real homes with high success rates, and _π_ 0<sup>_∗_[4] enabled</sup> VLAs to improve from their own practice via reinforcement learning. Open-source systems 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

3 of 59 

( **OpenVLA** [5], **Octo** [6]) and efficient architectures [7,8] have made the technology broadly accessible. 

**Emergence of unmanned aerial VLAs.** In parallel, the unmanned aerial systems community has begun adopting VLA ideas. **CognitiveDrone** [9] generates real-time flight commands from camera images and text instructions. **DroneVLA** [10] performs languagecommanded aerial grasping, while **AIR-VLA** [11] benchmarks aerial manipulation VLAs. **Flying Hand** [12] uses the same action chunking method developed for bimanual manipulation (ACT) on a hexarotor with a robotic arm. These systems confirm that the VLA framework transfers across embodiments. 

**Gap in existing surveys.** Surveys on foundation models for robotics [13] address high-level planning but not low-level motor control. Reviews of diffusion-based imitation learning [14] focus on policy generation but do not cover VLA architectures. Surveys on multi-arm systems [15] cover classical methods, not learned policies. Aerial surveys have examined perception and detection but not end-to-end VLA-based drone control. No existing review treats bimanual manipulation and unmanned aerial robotics as two instances of the same VLA problem. 

This review fills that gap by treating VLAs as a single framework applied to two embodiment families. We first review the shared VLA machinery (architectures, training recipes, action representations, language grounding) and then apply it to bimanual manipulation and unmanned aerial robotics, in turn, drawing explicit parallels throughout. The main contributions are: 

- A unified taxonomy of VLA models covering architectures, training, action representations, bimanual manipulation, and unmanned aerial robotics, with comparison tables spanning 30+ methods. 

- The first cross-domain analysis connecting bimanual coordination strategies to multidrone and aerial manipulation systems, showing how insights transfer between embodiments. 

- Fourteen research directions identifying open challenges across both domains, from real-time control and safety certification to end-to-end drone VLAs and bridging the research-to-production gap. 

This paper is structured to build from shared foundations to domain-specific applications. Sections 2–7 cover the common VLA stack: problem formulation, background, benchmarks, architectures, training, and action representations. Section 8 then applies this stack to bimanual manipulation, where VLAs are most mature. Section 9 applies it to unmanned aerial robotics, drawing on the bimanual analysis to highlight what transfers and what differs. Section 10 examines language grounding across both domains. Section 11 addresses cross-cutting concerns (visual representations, world models, memory, safety, sim-to-real). Section 12 synthesizes findings and identifies research directions that span both embodiment families. 

# **2. Problem Definition and Scope** 

We begin by formalizing the core concepts that underpin the review: the VLA policy, action chunking, flow matching for action generation, and bimanual coordination. The notation introduced here is used consistently in subsequent sections; Table 1 provides a summary. Figure 1 presents the taxonomy that organizes this review. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

4 of 59 

**Table 1.** Summary of notation used in this review. 

|**Symbol**|**Description**|
|---|---|
|_πθ_|VLA policy parameterized by_θ_|
|**o**_t_|Visual observation at time_t_|
|_ℓ_|Natural-language instruction|
|**q**_t_|<br>Proprioceptive state (joint positions)|
|**a**_t_|<br>Single-step action|
|**A**_t_|<br>Action chunk of horizon_H_|


**Table 1.** _Cont._ 

|**Symbol**|**Description**|
|---|---|
|_H_|Action chunk horizon (number of steps)|
|_T_|Terminal (final) time step of an episode<br>|
|**_τ_**|Trajectory(**a**0, . . . ,**a**_T−_1)<br>|
|**g**<br>|Goal state|
|_S_(_ℓ_,**o**_T_)|Task completion indicator|
|_da_|Action dimensionality|
|_K_|Number of denoising/flow steps|
|**v**_θ_<br><br>|Learned velocity field (flow matching)|
|**a**<sup>_L_</sup><br>_t_ <sup>,</sup><sup>**a**</sup><sup>_R_</sup><br>_t_|Left and right arm actions|
|_f_vis, _f_VLM, _f_act|Visual encoder, VLM backbone, action<br>head|
|_α_,_γ_,_σk_|Diffusion schedule coefficients (Equa-<br>tion (11))<br>|
|**z**|Gaussian noise,**z**_∼N_(**0**,**I**)|
|_ϵθ_|Noise prediction network (diffusion)|


### **VLA for Unmanned Aerial Robotics & Bimanual Manip.** 


**Figure 1.** Taxonomy of VLA models for bimanual manipulation and unmanned aerial robotics. This review is organized along five major dimensions: architectural foundations (autoregressive, flowbased, diffusion-based, hybrid), training recipes (pre-training, post-training, reinforcement learning), action representations (discrete tokenization, continuous generation), bimanual-specific concerns (coordination strategies, task types), and unmanned aerial robotics (navigation, aerial manipulation, multi-agent unmanned systems). Each branch is covered in a dedicated section. 

## _2.1. VLA Policy Formulation_ 

**Policy definition.** A Vision–Language–Action model defines a policy _πθ_ parameterized by _θ_ that maps a visual observation **o** _t ∈O_ , a language instruction _ℓ ∈L_ , and optionally a proprioceptive state **q** _t ∈Q_ to an action **a** _t ∈A_ : 


https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

5 of 59 

The observation space _O_ typically consists of one or more camera images **I** _t ∈_ R<sup>_H_img</sup><sup>_×W_img</sup><sup>_×_3</sup> . The language instruction _ℓ_ is a natural-language string tokenized and embedded by the VLM backbone. The action space _A_ varies by embodiment; for a single _n_ -DOF arm with a gripper, **a** _t ∈_ R<sup>_n_+1</sup> , encoding either joint velocities or end-effector displacements plus a gripper command. 

**Architecture.** The VLA framework distinguishes itself from prior vision-based control policies by sharing a backbone with a pre-trained VLM. Concretely, a VLA typically consists of three components: (1) a visual encoder _f_ vis that produces image tokens, (2) a vision– language backbone _f_ VLM that jointly reasons over image and text tokens, and (3) an action head _f_ act that decodes actions from the VLM’s hidden representations: 


where Tok( _ℓ_ ) denotes the tokenized language instruction. The proprioceptive state **q** _t_ is likewise tokenized and fed into _f_ VLM alongside the visual and language tokens. 

**Goal formalization.** A VLA policy is trained to reach a _goal state_ **g** _∈G_ specified implicitly by the language instruction _ℓ_ : the task is complete when the world state matches the intent of _ℓ_ . We formalize this with a task completion indicator: 


where **o** _T_ is the observation at the terminal step _T_ of an episode of length _T_ . In practice, _S_ is evaluated by a human judge, a VLM-based evaluator, or structured predicates. 

**Trajectory planning.** Over the same episode of _T_ steps, the VLA produces a trajectory **_τ_** = ( **a** 0, **a** 1, . . . , **a** _T−_ 1) by iteratively predicting and executing action chunks. No explicit trajectory optimization is performed; the trajectory emerges from successive chunk predictions, each conditioned on the latest observation: 


where **_τ_** is the full trajectory over _T_ time steps, _k_ indexes successive chunk queries, _H_ is the chunk horizon, and<sup>�</sup> denotes concatenation. In hierarchical VLAs such as _π_ 0.5, a high-level planner additionally decomposes _ℓ_ into subgoal instructions ( _ℓ_ 1, _ℓ_ 2, . . .) that each produce a trajectory segment. 

**Language applicability.** Because VLM backbones inherit tokenizers trained on multilingual web corpora, VLA policies can in principle accept instructions in any language the tokenizer supports. In practice, however, all current VLA systems are trained and evaluated exclusively in English, and multi-lingual generalization has not been tested. Whether crosslingual transfer degrades action prediction quality remains an open question. 

**Illustrative examples.** To ground the formulation above, consider two representative tasks. _(i) Bimanual manipulation:_ given a camera image **I** _t_ of a towel on a table and the instruction _ℓ_ = “fold the towel,” _f_ vis extracts image tokens, _f_ VLM fuses them with Tok( _ℓ_ ) to form a latent plan, and _f_ act decodes an action chunk **A** _t_ that moves both arms to grasp opposite edges and bring them together. The goal indicator _S_ returns 1 when the towel is folded at step _T_ . _(ii) Aerial navigation:_ given a forward-facing camera image and _ℓ_ = “fly to the red building,” the same pipeline produces a trajectory **_τ_** of 3D waypoints; here, the action chunk encodes position commands rather than joint angles, and _S_ returns 1 when the drone reaches the target. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

6 of 59 

## _2.2. Action Chunking_ 

Rather than predicting a single action **a** _t_ , modern VLA policies predict an _action chunk_ , a sequence of _H_ future actions, in a single forward pass: 


where _H_ is the _chunk horizon_ and _da_ is the action dimension. Action chunking, introduced in the context of **ACT** [16], offers two key advantages. First, it amortizes the cost of a single VLM forward pass over multiple control steps, which allows high-frequency control despite the latency of large models. Second, it captures temporal correlations between successive actions, producing smoother trajectories than single-step prediction. The chunk is typically executed open-loop or with temporal ensembling, where overlapping chunks are averaged to reduce jitter. 

## _2.3. Flow Matching for Action Generation_ 

_Flow matching_ [17] provides a framework for learning continuous normalizing flows by regressing a vector field that transports samples from a simple prior _p_ 0 (e.g., a standard Gaussian) to the data distribution _p_ 1. Given a time-dependent vector field **v** _θ_ ( **x** , _t_ ) for _t ∈_ [0, 1], the flow _ϕt_ ( **x** ) satisfies (here, _t_ denotes the continuous flow time parameter, distinct from the discrete control step index used elsewhere): 


where _ϕt_ is the flow map at time _t_ , transporting a sample from _p_ 0 toward _p_ 1. The training objective minimizes the conditional flow matching loss: 


where **x** _t_ = (1 _− t_ ) **x** 0 + _t_ **x** 1 is a linear interpolation. In the VLA context, **x** 1 is the groundtruth action chunk **A** _t_ and **x** 0 is Gaussian noise. _π_ 0 [2] applies this formulation with a VLM backbone: the VLM hidden states condition the flow, and the action head iteratively denoises a noisy action chunk over _K_ steps during inference. 

## _2.4. Bimanual Coordination_ 

For a bimanual system with a left arm and a right arm, the joint action space is: 


where **a** _t_<sup>_L∈_R</sup><sup>_dL_and</sup><sup>**a**</sup> _t_<sup>_R∈_R</sup><sup>_dR_are the actions for the left and right arms, respectively.For</sup> typical 7-DOF arms with grippers, _dL_ = _dR_ = 8 (7 joint positions or velocities + 1 gripper command), yielding _da_ = 16. With action chunking of horizon _H_ , the full bimanual action chunk has dimensionality _H ×_ ( _dL_ + _dR_ ), which for typical settings ( _H_ = 50, _da_ = 16) reaches 800 dimensions. 

Bimanual coordination can be categorized into three modes: 

1. **Independent** : each arm executes its own subtask without coupling (e.g., one arm picks an object while the other holds a container). 

2. **Loosely coupled** : arms must coordinate timing but not forces (e.g., handover tasks where one arm releases as the other grasps). 

3. **Tightly coupled** : arms must coordinate both motion and forces simultaneously (e.g., folding fabric where both arms must apply tension). 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

7 of 59 

## _2.5. Scope of This Review_ 

This review covers VLA models that integrate a pre-trained vision–language backbone with an action generation mechanism, with emphasis on their application to bimanual manipulation and unmanned aerial robotics. We include autoregressive, flow-based, diffusion-based, and hybrid architectures published through early 2026. We focus on learning-based approaches trained from demonstrations or reinforcement learning; classical motion planning, optimization-based bimanual coordination, and traditional PID-based drone controllers are outside our scope. For bimanual motion planning, we refer readers to Abbas et al. [15]; for classical aerial control, we refer to standard flight dynamics references [18]. The inclusion of both manipulation and aerial domains reflects the crossembodiment nature of VLAs: the same architectures and training recipes power policies across diverse robot morphologies. 

With these definitions established, Section 3 reviews the prerequisite concepts. 

# **3. Background** 

Before surveying specific VLA methods, we review the foundational concepts they build upon: vision–language models, imitation learning, generative modeling for action generation, bimanual robotic systems, and aerial robotic systems. 

## _3.1. Vision–Language Models_ 

Vision–Language Models (VLMs) jointly process visual and textual inputs, built upon the Transformer architecture [19] and trained on internet-scale image–text datasets. The Vision Transformer (ViT) [20] extended self-attention to image patches, while **CLIP** [21] established contrastive pre-training for aligned visual–textual representations. The pretrain-then-fine-tune recipe, scaled by GPT-3 [22] and refined via instruction-tuning [23], is the foundation-model methodology that VLAs inherit. 

Key VLMs relevant to this review include **PaLM-E** [24], which demonstrated embodied reasoning in a 562B-parameter model; **PaLIGemma** [25] and **Gemma** [26], which provide efficient open-weight backbones used by several VLA systems; and open-source models ( **LLaMA** [27], **LLaVA** [28]) that democratized access. VLMs are attractive for robotics because they recognize objects, understand spatial relationships, and interpret instructions without robotics-specific training. 

The transition from VLM to VLA requires adding an action output modality. This can be achieved by (1) tokenizing actions as text tokens and fine-tuning the VLM’s language head [1], (2) attaching a separate action head that reads from the VLM’s hidden states [2], or (3) using the VLM as a high-level planner that conditions a low-level policy [29]. Each approach trades off between exploiting pre-trained knowledge and accommodating the continuous, high-frequency nature of robot control. A limitation for robotics is that VLMs lack grounding in physical interaction dynamics; they recognize objects but cannot predict contact forces or material deformation. 

## _3.2. Imitation Learning_ 

Imitation learning (IL) trains a policy _πθ_ to mimic expert demonstrations _D_ = _{_ ( **o** _i_ , _ℓi_ , **a** _i_ ) _}i_<sup>_N_</sup> =1<sup>, dating back to</sup><sup>**ALVINN**[30].The simplest form,</sup><sup>_behavioral cloning_(BC),</sup> minimizes a supervised loss: 


BC suffers from compounding errors due to distribution shift [31]: at test time, the policy visits states not seen in training. Action chunking [16] mitigates this by reducing decision 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

8 of 59 

points. A second challenge is _multi-modality_ : for a given observation, multiple valid action sequences may exist. Mean-squared-error regression averages over modes, producing invalid intermediate actions. Bimanual tasks amplify both problems because the state space is higher-dimensional and errors propagate across both arms. This motivates expressive generative models (diffusion, flow matching, autoregressive sampling) as action decoders. **Language-conditioned IL** [32] extends BC by conditioning on language instructions; VLAs take this further by using pre-trained VLMs for rich semantic grounding. 

## _3.3. Generative Modeling for Actions_ 

Three families of generative models underpin VLA action generation. Early approaches used VAEs [33] and GANs [34] for latent action representations. DDPMs [35] and score-based models [36] provided higher-fidelity generation at the cost of iterative sampling, with **Latent Diffusion Models** [37] reducing this cost via learned latent spaces. The **Decision Transformer** [38] reframed RL as sequence modeling, foreshadowing the autoregressive approach that VLAs later adopted, and **Gato** [39] extended this to a generalist agent handling text, images, and robotic actions in one Transformer. 

## 3.3.1. Autoregressive Models 

Autoregressive models factorize the action distribution as a product of conditionals: 


**RT-2** [1] discretizes continuous actions into 256 bins per dimension and generates action tokens left-to-right using the VLM’s language modeling head. This approach naturally exploits VLM pre-training but introduces quantization error and sequential latency that scales with action dimensionality. 

## 3.3.2. Diffusion Models 

**Diffusion Policy** [40] generates actions by iteratively denoising a Gaussian sample through a learned reverse diffusion process: 


where _ϵθ_ is the noise prediction network, _k_ indexes the denoising step, **z** _∼N_ ( **0** , **I** ) is standard Gaussian noise, and _α_ , _γ_ , _σk_ are schedule-dependent coefficients. Diffusion models excel at capturing distributions over multiple valid actions and produce smooth trajectories but require multiple denoising steps ( _K_ = 10–100), increasing inference latency. 

## 3.3.3. Flow Matching 

Flow matching [17], formalized in Equation (7), offers a simpler training objective and often requires fewer steps than diffusion. **Rectified Flow** [41] straightens transport paths to reduce integration steps. _π_ 0 [2] demonstrated that flow matching with _K_ = 10 steps produces high-quality action chunks at 50 Hz for bimanual systems. 

## _3.4. Bimanual Robotic Systems_ 

Three hardware platforms have transformed bimanual VLA research (see Section 8 for specifications). **ALOHA** [16] provides low-cost bilateral teleoperation for two 6-DOF arms, paired with the ACT policy (Action Chunking with Transformers) that predicts action chunks at 50 Hz. **Mobile ALOHA** [42] extends this to a mobile base and demonstrated co-training (mixing target-task data with diverse data), which directly influenced VLA 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

9 of 59 

training recipes (Section 6.2). **UMI** [43] decouples data collection from the robot via hand-held grippers with visual–inertial tracking, allowing demonstrations in diverse environments without teleoperation hardware. The standardization of action spaces across these platforms has facilitated cross-system transfer; data collection strategies are detailed in Section 6.4. 

Two practical concerns affect bimanual VLA deployment. _Calibration_ : even small errors ( _∼_ 1 cm position, _∼_ 2<sup>_◦_</sup> orientation) between arms can cause policies to fail; **UMI** [43] addresses this via visual–inertial tracking that decouples data collection from arm calibrations. _Action space choice_ : joint-space actions ( **ACT** [16], **RDT-1B** [44]) provide direct control but are embodiment-specific, while end-effector actions ( _π_ 0 [2]) facilitate cross-embodiment transfer at the cost of inverse kinematics errors. 

## _3.5. Aerial Robotic Systems_ 

A quadrotor is a 6-DOF rigid body (3 translational, 3 rotational) controlled through differential thrust of four rotors, making it underactuated (4 inputs for 6 DOF). This underactuation creates inherent coupling between translational and rotational motion that complicates learned control policies. Quadrotors are the dominant platform for learningbased unmanned aerial robotics due to their mechanical simplicity, hovering capability, and commercial availability. 

Traditional drone control employs cascaded PID loops operating at _≥_ 250 Hz, with an inner attitude loop and an outer position loop. Learning-based approaches replace part or all of this pipeline with neural network policies. The action space varies from highlevel waypoints (suitable for navigation VLAs operating at 5–10 Hz) to low-level motor commands (required for agile flight at _≥_ 100 Hz). This range of control frequencies and abstraction levels parallels the hierarchy observed in manipulation VLAs, from high-level subgoal generation ( _π_ 0.5) to low-level continuous action chunks ( _π_ 0). 

High-fidelity simulators play an outsized role in aerial VLA development. **AirSim** [45] provides photorealistic rendering via Unreal Engine with accurate quadrotor dynamics. **Flightmare** [46] decouples rendering from physics, allowing massively parallel RL training at 200 _×_ real-time. These simulators are to aerial VLAs what LIBERO [47] (a suite of language-conditioned manipulation tasks) and SIMPLER [48] (a simulation-to-real evaluation framework) are to manipulation VLAs: essential infrastructure for training and evaluation at scale. Both benchmarks are described in detail in Section 4.2. 

The datasets and benchmarks that drive VLA development and evaluation are reviewed in the next section. 

# **4. Datasets, Benchmarks, and Evaluation** 

Large-scale datasets and standardized benchmarks form the infrastructure that drives VLA research. We review the major datasets used for pre-training and evaluation, simulation benchmarks, and the metrics employed to assess bimanual manipulation and aerial navigation performance. 

## _4.1. Pre-Training Datasets_ 

VLA training relies on large-scale robot demonstration data for pre-training. Table 2 compares the major datasets. Three have proved most influential. 

**Open X-Embodiment (OXE)** [49] is the largest open robot dataset, aggregating demonstrations from over 20 institutions across 22 robot embodiments. It contains more than 1 million episodes spanning single-arm, bimanual, and mobile manipulation tasks. OXE’s diversity in embodiments, viewpoints, and environments makes it the standard pre-training 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

10 of 59 

corpus for cross-embodiment VLAs. **OpenVLA** [5], **Octo** [6], and _π_ 0 [2] all use OXE (or subsets thereof) for pre-training. 

**DROID** [50] provides 76,000 trajectories collected across 564 scenes and 86 tasks using Franka Emika arms. Unlike OXE, DROID emphasizes diversity within a single embodiment: 50 operators collected data across varied environments, capturing natural scene diversity. DROID has been shown to improve generalization when included in VLA pre-training mixtures. 

**BridgeData V2** [51], building on the original BridgeData [52] that first demonstrated cross-domain dataset boosting, contains 60,096 trajectories from a WidowX robot performing tabletop manipulation tasks across 24 environments. Its relatively uniform setup and reliable labeling make it a standard evaluation dataset. Many VLA papers report results on Bridge tasks. 

**GigaBrain-0.5M** [53] is a recent large-scale dataset containing 500,000 episodes collected via a combination of teleoperation and autonomous data collection. It includes bimanual manipulation episodes and was designed to support VLA training with worldmodel-based reinforcement learning. 

**Table 2.** Comparison of major robot datasets used for VLA pre-training and evaluation. Columns include the number of episodes, robot embodiments covered, task count, scene diversity (distinct environments), bimanual support, language annotation availability, action space type, and primary manipulation domain. In this and all subsequent comparison tables, ✓indicates that the feature/capability is supported, while “–” or a blank entry indicates that the feature is not supported, not applicable, or not reported in the original publication. 

|**Dataset**|**Episodes**|**Embodiments**|**Tasks**|**Scenes**|**Bimanual**|**Language**|**Action Space**|**Domain**|**Open Access**|**Year**|
|---|---|---|---|---|---|---|---|---|---|---|
|**OXE** [49]<br>**DROID**[50]|_>_1M<br>76K|22<br>1 (Franka)|527<br>86|20+ inst.<br>564|✓<br>–|✓<br>✓|Mixed (joint/EE)<br>EE delta|Tabletop + mobile<br>Tabletop (in-the-wild)|✓<br>✓|2024<br>2024|
|<br>**BridgeData V2**[51]|60K|<br>1 (WidowX)|13|24|–|✓|EE delta|<br>Tabletop|✓|2023|
|<br>**ALOHA**[16]|_∼_1K|1 (ALOHA)|6|1 (lab)|✓|–|Joint pos.|Bimanual fine-grained|✓|2023|
|**GigaBrain-0.5M**[53]|500K|Multiple|200+|Diverse|✓|✓|<br>Mixed|i<br>Household + manip.|✓|2025|


## _4.2. Simulation Benchmarks_ 

Simulation benchmarks support reproducible evaluation at scale without the expense and variability of real-world experiments. 

**LIBERO** [47] is a benchmark suite of 130 language-conditioned manipulation tasks organized into five suites: LIBERO-Spatial (spatial relationship understanding), LIBEROObject (novel object generalization), LIBERO-Goal (goal specification comprehension), LIBERO-Long (multi-step task execution), and LIBERO-100 (a larger training set). The four evaluation suites each contain 10 tasks with 50 demonstrations per task. LIBERO has become the primary simulation benchmark for VLA evaluation because it tests multiple generalization axes independently, allowing researchers to diagnose specific weaknesses. 

**SIMPLER** [48] provides simulated counterparts to real-world evaluation setups, which allows VLA evaluation without physical hardware. It includes tasks from the Bridge and Google Robot environments, with visual fidelity and physics parameters calibrated to correlate with real-world performance. SIMPLER’s key contribution is demonstrating that simulation success rates predict real-world success rates with _r >_ 0.8 correlation for most task categories. This validates simulation as a low-cost proxy for real evaluation. 

Other simulation platforms include **RLBench** [54] (100 procedurally generated tasks), **Meta-World** [55] (50 parametric tasks), **RoboSuite** [56], **ManiSkill2** [57] (soft-body tasks), and **BEHAVIOR-1K** [58] (1000 household activities). Li et al. [48] found that both physics fidelity and visual realism matter for reliable simulation-to-real prediction. 

Neither LIBERO nor SIMPLER includes bimanual tasks, a significant limitation. Bimanual simulation requires dual-arm physics and contact-rich interaction modeling that no standard benchmark provides. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

11 of 59 

## _4.3. Evaluation Metrics_ 

VLA evaluation relies on several complementary metrics: 

**Task success rate** is the primary metric, defined as the fraction of _N_ evaluation episodes in which the robot completes the specified task: 


where ⊮[ _·_ ] is the indicator function. 

**Normalized score** averages success rates across multiple task suites, which allows comparison across benchmarks with different numbers of tasks. 

**Inference latency** measures the wall-clock time for a single action chunk prediction, critical for real-time control. In dual-arm setups running at 50 Hz, the action generation must complete within 20 ms per step (or within _H ×_ 20 ms per chunk). 

**Data efficiency** tracks how many demonstrations are required to reach a target success rate, relevant for bimanual tasks where data collection is expensive. 

Bimanual evaluation protocols remain less standardized. Most papers define their own task suites (e.g., _π_ 0 [2] evaluates on laundry folding, box assembly, and table busing), making cross-method comparison difficult. Task completion criteria also vary: some papers use binary success, others use partial completion scores, and temporal efficiency is rarely reported. 

**Generalization metrics** assess whether the VLA transfers to novel settings: 


where SRnovel and SRtrain are success rates on novel and training environments, respectively. A generalization ratio near 1.0 indicates robust transfer. **RT-2** [1] reported a generalization ratio of _∼_ 0.76 for novel objects, while _π_ 0.5 [3] achieved _∼_ 0.95 for novel homes, indicating strong environment generalization. 

Bimanual-specific benchmarks remain limited: most simulation suites focus on singlearm tasks, and real-world bimanual evaluation varies across papers. This gap motivates the need for standardized bimanual benchmarks (Section 12). 

# **5. VLA Architectures and Foundations** 

This section presents VLA architectures organized by their action generation mechanism. We identify four families: autoregressive, flow-based, diffusion-based, and hybrid. Figure 2 traces the chronological development of these methods from 2022 to 2025. Figure 1 provides an overview of the families and their constituent methods, while Figure 3 contrasts the four architectural paradigms side by side. Table 3 compares representative methods across key architectural dimensions. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

12 of 59 


**Figure 2.** Timeline of key VLA and bimanual manipulation milestones (2022–2026). Colors indicate the architectural family: autoregressive (blue), flow-based (red), diffusion-based (green), hardware platforms (orange), and hybrid/efficient methods (purple). The field has accelerated rapidly, with the majority of VLA contributions appearing in 2024–2026. 


**Figure 3.** Architectural comparison of the four VLA families. ( **a** ) Autoregressive VLAs (RT-2, OpenVLA) discretize actions and generate them as language tokens. ( **b** ) Flow-based VLAs ( _π_ 0) use a flow-matching head that iteratively denoises a noise sample conditioned on VLM features. ( **c** ) Diffusion VLAs (RDT-1B) use a Diffusion Transformer to denoise action chunks. ( **d** ) Hybrid VLAs (HybridVLA) combine autoregressive and flow heads for discrete and continuous action components, respectively. 

## _5.1. Autoregressive VLAs_ 

Autoregressive VLAs generate actions by extending the VLM’s language modeling capability to action tokens. This approach directly builds on the pre-trained language model’s sequential generation ability. 

## 5.1.1. RT-1 and RT-2 

**RT-1** [59] was among the first Transformer-based robot policies trained on large-scale real-world data. It processes image histories through a FiLM-EfficientNet encoder and generates discretized actions via per-dimension classification heads. Trained on 130,000 demonstrations from Google’s mobile manipulator fleet, RT-1 achieved 97% success on seen tasks and 76% on unseen tasks, establishing that data diversity produces meaningful generalization. RT-1 does not address bimanual manipulation, but its lessons directly informed subsequent VLA designs. 

**RT-2** [1] took the decisive step of unifying vision–language understanding and action generation within a single VLM. By fine-tuning a PaLI-X (55B parameters) or PaLM-E (12B parameters) model to output discretized actions as text tokens, RT-2 demonstrated that VLM pre-training on web data transfers to robotic manipulation. It exhibited capabilities absent from RT-1: reasoning about object categories, interpreting novel instructions, and performing rudimentary chain-of-thought planning for multi-step actions. Semantic knowledge encoded in VLM weights (object affordances, spatial relationships, physical 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

13 of 59 

intuition) directly benefits action generation. RT-2 remains closed-source, however, and its 55B-parameter scale demands TPU-class compute, putting real-time control out of reach for most research groups and limiting reproducibility. 

## 5.1.2. OpenVLA 

Reproducibility was a major barrier for VLA research until **OpenVLA** [5], the first fully open-source 7B-parameter VLA. Based on the Prismatic VLM architecture, it tokenizes actions into 256 discrete bins per dimension following RT-2’s approach and trains on the OXE dataset. Despite its open weights, OpenVLA matches **RT-2-X** [49] (the crossembodiment variant of RT-2 trained on OXE alongside **RT-1-X** [49]). Its release catalyzed community research and revealed important scaling behaviors: performance improves consistently with data diversity, and fine-tuning on small task-specific datasets yields substantial gains over the pre-trained checkpoint. A subsequent study, **OpenVLA-OFT** [60], introduced improved fine-tuning recipes optimizing both speed and success rate, narrowing the gap to proprietary systems. 

## 5.1.3. Octo 

Although Octo uses a diffusion action head, we discuss it here because it was designed as a generalist initialization for downstream fine-tuning, a role shared with autoregressive VLAs. Whereas OpenVLA adapts an existing VLM, **Octo** [6] takes a different path: a purpose-built 93M-parameter Transformer with a diffusion action head, bridging the autoregressive and diffusion approaches. Prompted with language instructions or goal images, Octo supports flexible action spaces and was trained on 800,000 episodes from OXE. It serves as a versatile initialization for fine-tuning on downstream tasks, including bimanual manipulation with ALOHA. Because it uses a diffusion action head rather than autoregressive token prediction, Octo straddles both categories in our taxonomy (Figure 1). Its modest parameter count, however, restricts capacity for complex reasoning compared to VLM-based approaches. 

Several other autoregressive VLAs have explored complementary design choices: **GR-1** [61] (video prediction as an implicit world model), **HAMSTER** [62] (hierarchical vision–language–action prediction), **SpatialVLA** [63] (explicit spatial representations), **BAKU** [64] (efficient multi-task architecture), **KAT** [65] (in-context imitation via keypointaction tokens), and **SimpleVLA** [66] (minimal design matching elaborate systems with RL fine-tuning). 

## _5.2. Flow-Based VLAs_ 

Flow-based VLAs use flow matching (Section 2.3) to generate continuous action chunks, avoiding the discretization bottleneck of autoregressive approaches. As shown in Figure 3b, the flow head iteratively denoises a noise sample conditioned on VLM features. 

## 5.2.1. _π_ 0 

The discretization bottleneck of autoregressive VLAs motivated a structurally different action head. _π_ 0 [2] addresses it with the first flow-matching action head for VLAs. Built on a 3B-parameter PaLIGemma [25] backbone, the model processes image and language tokens through the VLM then uses the resulting hidden states to condition a flow-matching network that generates action chunks. The action head consists of Transformer layers that jointly attend to VLM features and noisy action tokens, iteratively denoising over _K_ = 10 flow steps. 

_π_ 0 achieved state-of-the-art results on bimanual dexterous tasks including laundry folding (80% success), box assembly, and table bussing. The flow-matching formulation is critical for bimanual tasks: it generates smooth, coherent 16-dimensional action chunks 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

14 of 59 

(8 per arm) without the quantization artifacts of autoregressive methods or the slow sampling of diffusion models. Pre-training on OXE followed by task-specific fine-tuning proved essential; the pre-trained model provides a strong initialization that allows learning from relatively few bimanual demonstrations. A significant limitation is that _π_ 0’s strongest results depend on proprietary multi-task data collected across Physical Intelligence’s robot fleet; reproducing these results with publicly available data alone has not been demonstrated, raising questions about how much of the performance stems from architecture versus data advantage. 

## 5.2.2. _π_ 0.5 

_π_ 0.5 [3] extends _π_ 0 to open-world deployment by introducing a hierarchical architecture. A high-level VLM generates subgoal language commands, while the low-level flow-matching policy executes motor actions. This decomposition allows _π_ 0.5 to handle complex, multi-step household tasks such as “clean the kitchen” that require planning over minutes rather than seconds. 

_π_ 0.5 was deployed on a fleet of mobile manipulators in real homes, achieving high success rates at following verbal instructions across a range of household tasks, a notable demonstration of VLA generalization beyond the lab, though the results are self-reported under conditions chosen by the authors and have not been independently reproduced. The hierarchical architecture proves well suited to bimanual tasks, where the high-level model can decompose complex instructions into single-step bimanual primitives. 

## 5.2.3. _π_ 0<sup>_∗_and RECAP</sup> 

_π_ 0<sup>_∗_(also referred to as</sup><sup>_π_</sup> 0.6<sup>_∗_in the original publication) [4] addresses a fundamental</sup> limitation of imitation learning: performance is bounded by the quality of demonstrations. _π_ 0<sup>_∗_introduces RECAP (Reinforcement Learning from Autonomous CAPability), a training</sup> approach in which the VLA collects experience autonomously and then improves via reinforcement learning. A VLM-based evaluator provides success/failure labels, eliminating hand-designed reward functions. Starting from a _π_ 0 checkpoint, RECAP alternates between autonomous data collection and policy optimization, progressively improving beyond the demonstration distribution. On bimanual tasks, _π_ 0<sup>_∗_achieved 10–40% absolute improve-</sup> ment over the demonstration-only baseline, demonstrating that VLAs can bootstrap their own improvement. 

## _5.3. Diffusion-Based VLAs_ 

Diffusion-based approaches apply denoising diffusion probabilistic models to action generation. The key tradeoff is generation quality versus inference latency. 

## 5.3.1. Diffusion Policy 

The idea of treating action generation as a denoising process originated with **Diffusion Policy** [40], which established that generative models outperform deterministic behavioral cloning for tasks with multi-modal demonstrations. The principal drawback is computational cost: _K_ = 50–100 DDPM steps push latency to _∼_ 300 ms per chunk, making real-time bimanual control impractical without acceleration (DDIM, consistency distillation). While Diffusion Policy predates VLAs (it uses task-specific encoders), its innovations (denoising action chunks, classifier-free guidance, temporal ensembling) are reused across subsequent VLA architectures. 

## 5.3.2. RDT-1B 

A natural question is whether scaling alone can close the gap between diffusion and flow-based VLAs. **RDT-1B** [44] tests this hypothesis by pushing diffusion-based action 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

15 of 59 

generation to 1.2 billion parameters, creating a “diffusion foundation model” for bimanual manipulation. The model uses a Transformer backbone (inspired by DiT) to denoise action chunks, conditioned on visual features from a pre-trained vision encoder and language features from a pre-trained text encoder. Pre-trained on multi-robot datasets and fine-tuned on ALOHA bimanual tasks, RDT-1B confirms that scale benefits diffusion-based robot policies just as it benefits language models. 

RDT-1B’s large parameter count allows it to capture the complex coordination patterns required for bimanual tasks. On ALOHA benchmarks, it outperformed ACT and Diffusion Policy on tasks requiring tight bimanual coordination such as handovers and collaborative assembly. The model also exhibited improved robustness to visual distractors and perturbations compared to smaller diffusion policies. 

RDT-1B uses separate vision and language encoders (SigLIP and T5) rather than a unified VLM, reaching competitive performance through scale rather than joint pre-training. The DiT backbone handles long bimanual sequences (64 timesteps _×_ 16 dimensions = 1024 elements) efficiently. 

## 5.3.3. CogACT 

A key tension in diffusion VLAs is the conflict between language generation and action denoising losses. **CogACT** [67] resolves this by introducing learned “cognitive action tokens” that bridge VLM semantic representations and the diffusion action head. This abstraction layer isolates the two objectives, reducing their interference during training. 

Related approaches include **PerAct** [68] (3D voxel-based manipulation), **RVT** [69] (efficient multi-view 3D manipulation), **3D Diffusion Policy** [70] (diffusion over point clouds), and **Transfusion** [71] (unified next-token prediction with diffusion generation). 

## _5.4. Hybrid and Efficient VLAs_ 

Several recent architectures combine multiple action generation approaches or focus on computational efficiency. 

## 5.4.1. HybridVLA 

Autoregressive and diffusion-based approaches have complementary strengths: autoregressive models excel at discrete decisions (e.g., grasp vs. release) while diffusion models excel at continuous trajectories. **HybridVLA** [72] exploits this complementarity by integrating both within a unified architecture, routing discrete action components through an autoregressive head and continuous components through a diffusion head. This hybrid design outperforms either approach alone on tasks with mixed discrete–continuous action spaces. 

The hybrid architecture suits bimanual manipulation well: gripper commands (open/close) are inherently discrete while arm motions are continuous. HybridVLA routes each component to the appropriate head, with both conditioning on the same VLM hidden states. A limitation is added training complexity: balancing the two heads requires careful loss weighting, and no published ablation isolates each head’s independent contribution. 

## 5.4.2. TinyVLA 

Inference latency remains the primary obstacle to deploying large VLAs on real-time bimanual systems. **TinyVLA** [7] tackles this by pairing a compact 1B-parameter VLM backbone with a diffusion policy action head, achieving a small-footprint architecture that avoids the overhead of larger VLM-based systems. The result is real-time control at 50 Hz on consumer GPUs, making VLA deployment practical for bimanual systems with tight latency requirements. The compact architecture introduces a capacity ceiling; however, the 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

16 of 59 

smaller VLM backbone limits semantic reasoning compared to larger VLAs, and the fidelity of action generation may degrade for high-dimensional bimanual action distributions. 

## 5.4.3. MiniVLA 

A contrasting strategy to distillation is to design for efficiency from the outset. **MiniVLA** [73] pairs a small VLM backbone with a lightweight action head, attaining competitive performance on standard benchmarks at a fraction of the compute. This ground-up efficiency could benefit bimanual systems, though MiniVLA has not been evaluated on such tasks. MiniVLA’s reduced capacity limits its ability to handle complex multi-step reasoning. 

## 5.4.4. FAST 

Efficient autoregressive action generation requires a better tokenization scheme than naive per-dimension binning. **FAST** [8] provides one with a learned action tokenizer that compresses continuous action chunks into discrete tokens. A VQ-VAE first learns to tokenize action chunks, and then a VLM is fine-tuned to predict these tokens. The tokenizer captures robot-specific action structure (temporal correlations, joint coupling), producing a compact discrete representation that avoids the quantization artifacts of naive binning. FAST achieves state-of-the-art results among autoregressive VLAs while maintaining the simplicity of text-token generation. 

Applied to dual-arm control, the FAST tokenizer learns coordinated patterns as single codebook entries, compressing a 50-step chunk (50 _×_ 16 = 800 values) into 16–32 tokens (25–50 _×_ compression), which reduces latency and improves long-range dependency modeling. A limitation is that the VQ-VAE codebook is fixed after training, so novel action patterns outside the codebook’s coverage may be poorly represented. 

**Hi Robot** [29] takes the hierarchical route: a high-level VLM selects subtasks while a low-level flow policy executes them, enabling open-ended instruction following on bimanual platforms. 

**Table 3.** Comparison of VLA architectures. Action type indicates the generation mechanism: AR = autoregressive, FM = flow matching, Diff = diffusion, Hybrid = combined. Bimanual indicates demonstrated bimanual capability. Params refers to the total model size. Visual encoder and training data columns provide additional context on each system’s design. Init. indicates whether the visual encoder is fine-tuned (FT) from a pre-trained checkpoint or trained from scratch (Scr.). 

|**Method**|**Action Type**|**VLM Backbone**|**Visual Enc.**|**Init.**|**Params**|**Chunk****_H_**|**Pre-Train Data**|**Bimanual**|**Open-Source**|**Year**|
|---|---|---|---|---|---|---|---|---|---|---|
|**RT-1** [59]<br>|AR (discrete)<br>|EfficientNet<br>|EfficientNet-B3<br>|FT (ImageNet)<br>|35M<br>|1<br>|130K demos<br>|–|–|2022|
|**RT-2**[1]<br>|AR (discrete)<br>|PaLI-X/PaLM-E<br>|ViT-22B<br>|FT (web)<br>|55B|1|RT-1 data<br>|–<br>|–<br>|2023|
|**Octo**[6]<br>|Diff head<br>|Custom|Custom ViT|Scr.<br>|93M|4|OXE (800K)|✓|✓<br>|2024|
|**OpenVLA**[5]<br>|AR (discrete)|Prismatic|DINOv2 + SigLIP|FT (web)<br>|7B|1|OXE|–<br>|✓|2024|
|_π_0 [2]<br>|FM<br>|PaLIGemma<br>|SigLIP<br>|FT (web)<br>|3B|50|OXE + propri.<br>|✓<br>|–|2024|
|_π_0.5 [3]|FM (hierarchical)|PaLIGemma|SigLIP|FT (web)|3B|50|OXE + propri.|✓|–|2025|
|_π_<sup>_∗_</sup><br>0 <sup>[4]</sup>|FM + RL|PaLIGemma|SigLIP|FT (web)|3B|50|OXE + RL data|✓|–|2025|
|<br>**RDT-1B**[44]<br>|Diff (DiT)<br>|SigLIP + T5<br>|SigLIP<br>|FT (web)<br>|1.2B<br>|64<br>|46 datasets (1M+)<br>|✓|✓<br>|2024<br>|
|**CogACT**[67]<br>|Diff head<br>|Prismatic|DINOv2 + SigLIP|FT (web)<br>|7B|16|OXE|–<br>|✓|2025|
|**HybridVLA**[72]<br>|AR + Diff<br>|Prismatic<br>|DINOv2 + SigLIP<br>|FT (web)<br>|7B|50|OXE + DROID<br>|✓|–<br>|2025|
|**TinyVLA**[7]<br>|Diff head<br>i|LLaVA<br>|CLIP ViT<br>|FT (web)<br>|1B<br>|10<br>|LLaVA + robot<br>|–|✓<br>|2024<br>|
|**MiniVLA**[73]<br>|Efficient head<br>|Prismatic|DINOv2 + SigLIP|FT (web)<br>|1B|8|OXE subset|–|✓<br>|2024|
|**FAST**[8]<br>|AR (learned tok.)<br>|Prismatic|DINOv2 + SigLIP|FT (web)<br>|7B|50|OXE|–<br>|✓|2025|
|**Hi Robot**[29]|Hierarchical FM|PaLIGemma|SigLIP|FT (web)|3B+|50|OXE + propri.|✓|–|2025|


Table 3 reveals several structural trade-offs across the four VLA families. 

_Autoregressive_ VLAs (RT-1, RT-2, OpenVLA, FAST) inherit the simplicity and scalability of language modeling, but discretizing continuous actions into bins introduces quantization artifacts that degrade fine-grained bimanual control; only FAST’s learned tokenizer alleviates this without abandoning the autoregressive paradigm. 

_Flow-based_ VLAs ( _π_ 0, _π_ 0.5, _π_ 0<sup>_∗_) generate smooth, continuous action chunks and cur-</sup> rently achieve the best bimanual performance but require multiple forward passes through the flow head ( _K_ = 10 denoising steps), coupling model size to inference cost. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

17 of 59 

_Diffusion-based_ VLAs (Octo, RDT-1B, CogACT) excel at modeling multi-modal action distributions—critical when multiple valid trajectories exist—but their 50–100 denoising steps incur 2–4 _×_ higher latency than flow matching. 

_Hybrid_ approaches (HybridVLA, Hi Robot) combine discrete high-level reasoning with continuous low-level execution, achieving strong benchmark performance at the cost of increased architectural complexity and harder end-to-end training. 

A notable trend is parameter efficiency: the best-performing architecture ( _π_ 0, 3B parameters) is an order of magnitude smaller than the earliest VLA (RT-2, 55B), suggesting that action head design and training strategy matter more than raw model scale. Looking at the **Params** column of Table 3 together with the benchmark scores in Table 4 reinforces this point: efficient architectures such as **TinyVLA** [7] (1B) and **MiniVLA** [73] (300M–1B) retain roughly 85–90% of the success rate of multi-billion-parameter flow-based VLAs on LIBERO and SIMPLER while reducing inference cost by 3–10 _×_ . In other words, the _Params_ entry in our tables is best read not as a proxy for capability but as one axis of a latency– quality–capacity tradeoff that is critical for real-time bimanual and aerial deployment. 

**Table 4.** VLA performance on standard benchmarks. LIBERO scores are normalized success rates averaged across task suites. Bridge V2 reports average success rate across evaluation tasks. SIMPLER reports success rate on the Google Robot evaluation suite. Bold indicates best in column (values are reported from the original publications under varying evaluation conditions and should be interpreted with caution; not all methods were evaluated on all benchmarks). 

|**Method**|**LIBERO-Spatial**|**LIBERO-Object**|**LIBERO-Goal**|**LIBERO-Long**|**Bridge V2**|**SIMPLER**|
|---|---|---|---|---|---|---|
|**RT-1** [59]|–|–|–|–|45.2|–|
|**RT-2**[1]|–|–|–|–|52.1|55.3|
|**Octo**[6]|78.9|85.7|72.1|46.3|54.8|48.7|
|**OpenVLA**[5]|84.7|88.4|79.2|53.7|58.3|56.2|
|_π_0[2]|**96.2**|**97.1**|**93.5**|**78.4**|**72.6**|**71.3**|
|**RDT-1B**[44]|89.3|91.5|84.7|62.1|61.4|–|
|**CogACT**[67]|87.1|89.8|81.3|58.9|59.7|–|
|**FAST**[8]|91.5|93.2|86.8|65.3|64.2|62.8|
|**HybridVLA**[72]|93.8|95.4|90.1|72.6|68.9|67.4|
|**TinyVLA**[7]|82.3|86.1|75.4|51.2|55.6|52.1|


Table 4 compares VLA methods across standard benchmarks. Three findings stand out from this comparison. First, flow-based VLAs ( _π_ 0) dominate across all benchmarks, with notably large margins on long-horizon tasks (LIBERO-Long) where action chunk coherence matters most. Second, hybrid approaches ( **HybridVLA** ) rank second, suggesting that combining autoregressive and flow-based generation captures complementary strengths. Third, efficient models ( **TinyVLA** ) trade 10–15% performance for significantly reduced compute, a worthwhile tradeoff for resource-constrained deployments. 

Autoregressive VLAs benefit most from VLM pre-training but struggle with highdimensional continuous actions. Flow-based VLAs offer the best quality–speed balance for bimanual tasks. Diffusion-based VLAs provide strong multi-modal modeling at higher cost. Architecture alone does not determine performance; as Section 6 will show, training strategy—particularly the choice of pre-training data, co-training ratio, and RL fine-tuning— is equally decisive in closing the gap between architectural promise and deployed capability. Two modular extensions apply across all families: _memory modules_ [74–76] for long-horizon task tracking (Section 8.4) and _world models_ [77–79] for future state prediction (Section 11.4). 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

18 of 59 

# **6. Training Recipes and Data Strategies** 

The performance of a VLA depends as much on how it is trained as on its architecture. This section reviews the three-stage training pipeline (pre-training, post-training, and reinforcement learning) as well as data collection strategies for bimanual manipulation. Section 11.6 illustrates the complete pipeline from VLM pre-training through deployment. 

## _6.1. Pre-Training_ 

As outlined in the “Training” branch of Figure 1, VLA pre-training proceeds in two phases. First, the VLM backbone is pre-trained on internet-scale image-text data, learning general visual and semantic representations. Second, the full VLA (backbone plus action head) is trained on large-scale robot demonstration data. 

The VLM pre-training phase builds on existing VLM checkpoints. _π_ 0 [2] initializes from PaLIGemma [25], a 3B-parameter VLM pre-trained on web-scale image-text data using the SigLIP visual encoder and Gemma [26] language backbone. **OpenVLA** [5] initializes from Prismatic, a 7B-parameter VLM combining DINOv2 and SigLIP visual encoders with a Llama-2 language backbone. **RT-2** [1] initializes from PaLI-X, a 55B-parameter VLM. This initialization provides the VLA with broad visual understanding, language comprehension, and spatial reasoning capabilities before it encounters any robot data. 

Taken together, the trend is toward smaller, efficient VLM backbones paired with powerful action heads: larger VLMs encode richer representations but are too slow for real-time control, while 3B-parameter models like PaLIGemma allow flow-matching heads with multiple forward passes per chunk. 

The robot data pre-training phase then trains the VLA on diverse cross-embodiment data. _π_ 0 [2] pre-trains on a mixture of OXE data and proprietary multi-task data spanning seven robot embodiments and hundreds of tasks, using a co-training objective that mixes action prediction with VLM text generation to preserve language capabilities. The cotraining loss is: 


where _L_ FM is the flow matching loss (Equation (7)), _L_ LM is the language modeling loss, and _λ_ act, _λ_ lang are balancing weights. **OpenVLA** [5] pre-trains exclusively on OXE data, demonstrating that publicly available data suffices for competitive pre-training. The key finding across all approaches is that data diversity (spanning multiple embodiments, environments, and tasks) matters more than dataset size for downstream generalization. This diversity also benefits memory-augmented VLAs [74,75]: pre-training on varied multi-step tasks exposes the memory module to diverse temporal patterns, improving its ability to track long-horizon bimanual task state. Additionally, world models can serve as _data engines_ during pre-training; **GigaWorld-0** [80] generates synthetic robot episodes via video generation and sim-to-real transfer, augmenting real demonstration data at scale. However, no published study has rigorously ablated whether pre-training gains stem from data diversity or backbone quality, making it difficult to attribute improvements to either factor alone. 

## _6.2. Post-Training and Fine-Tuning_ 

Post-training adapts a pre-trained VLA to specific tasks, embodiments, or environments. Fine-tuning on task-specific demonstrations is the most common approach. _π_ 0 [2] fine-tunes on 50–200 bimanual demonstrations per task, which yields strong performance from a well-initialized model. **OpenVLA** [5] demonstrated that fine-tuning on as few as 10 demonstrations can yield significant improvements on in-distribution tasks. 

Co-training (mixing target-task data with pre-training data during fine-tuning) prevents catastrophic forgetting and often improves performance on the target task. _π_ 0 [2] 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

19 of 59 

mixes cross-embodiment data with single-task data throughout fine-tuning, finding that this consistently outperforms fine-tuning on target data alone. The intuition is that crossembodiment data provides a regularization effect, preventing the model from overfitting to the small fine-tuning dataset. 

The mixing ratio is a key hyperparameter: _π_ 0 [2] uses a 1:1 ratio, while **Mobile ALOHA** [42] found even 10% diverse co-training data improves bimanual success. Tasks dissimilar to pre-training benefit from more target data; visually similar tasks benefit from more diverse co-training. 

Parameter-efficient fine-tuning via Low-Rank Adaptation (LoRA) [81] offers an alternative to full fine-tuning: by injecting low-rank weight updates into frozen VLM layers, LoRA reduces GPU memory requirements while preserving pre-trained representations. Preference-based optimization methods such as DPO [82] have also been explored for aligning VLA outputs with human preferences, though their application to bimanual manipulation remains limited. 

Other techniques aim to preserve pre-trained knowledge during fine-tuning. **Knowledge Insulation** [83] freezes certain VLM layers during fine-tuning to preserve language understanding. **Align-then-Steer** [84] uses two-phase alignment and constrained finetuning. **RoboMimic** [85] finds that observation representations and data quality have outsized impact on offline IL, and **RoboAgent** [86] improves generalization through semantic augmentations. 

## _6.3. Reinforcement Learning for VLAs_ 

Imitation learning alone caps VLA performance at the demonstration quality. Reinforcement learning (RL) offers a path to surpass this ceiling. Early large-scale RL for robotic manipulation ( **QT-Opt** [87] trained grasping policies from over 580,000 real grasps) showed that RL can scale in the real world. Offline RL methods such as **Conservative Q-Learning (CQL)** [88] and **Advantage-Weighted Regression (AWR)** [89] learn from static datasets without further environment interaction, providing a lower-risk alternative (see Levine et al. [90] for a tutorial). Policy gradient methods such as PPO [91] remain the most common choice for online fine-tuning of VLAs. 

Online RL for VLAs was first realized by _π_ 0<sup>_∗_</sup><sup>**(RECAP)**[4].TheRECAPpipeline</sup> works as follows: (1) the VLA policy autonomously executes tasks in the real world, (2) a VLM-based evaluator labels each episode as success or failure, (3) successful episodes are added to the training set and failures are discarded, and (4) the VLA is fine-tuned on the augmented dataset. This cycle repeats, gradually expanding the VLA’s competence beyond the original demonstration distribution. 

RECAP’s key innovation is using a separate VLM as an autonomous reward function, eliminating the need for hand-designed reward signals. On bimanual tasks, RECAP improved laundry folding success from 60% (demonstration-only) to over 90% after several cycles of autonomous practice. This demonstrates that VLAs can self-improve on bimanual tasks, a necessary capability for scaling deployment. Algorithm 1 summarizes the RECAP pipeline. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

20 of 59 

**Algorithm 1** RECAP: Reinforcement Learning from Autonomous Capability. 

**Require:** Pre-trained VLA policy _πθ_ , VLM evaluator _V_ , task set _T_ 

- **Require:** Demonstration buffer _D_ demo, practice buffer _D_ auto _←_ ∅ 1: **for** cycle _c_ = 1, 2, . . . , _C_ **do** 2: _// Autonomous data collection_ 3: **for** task _τ ∈T_ **do** 4: Execute _πθ_ on _τ_ , collect trajectory _ξ_ 5: Evaluate: _r ←V_ ( _ξ_ , _τ_ ) _// VLM judges success_ 6: **if** _r_ = success **then** 7: _D_ auto _←D_ auto _∪{ξ}_ 8: **end if** 9: **end for** 

- 10: _// Policy improvement_ 11: Fine-tune _πθ_ on _D_ demo _∪D_ auto 12: **end for** 13: **return** Improved policy _πθ_ 

While RECAP targets success rate, RL can also optimize for speed: human teleoperation of bimanual systems is typically slow and cautious, so policies that merely imitate inherit this inefficiency. **SAIL** [92] addresses this by training VLA policies to execute tasks _faster_ than the demonstrations. Using time-warped demonstrations and a reward that encourages speed while maintaining success, SAIL produces policies that complete bimanual tasks in less time than human demonstrators, removing the teleoperation speed bottleneck. 

Beyond these targeted methods, other RL approaches include **VLA-RL** [93] (scalable RL for general robotic manipulation), **ConRFT** [94] (consistency-policy-regularized RL), **Q-Transformer** [95] (offline RL via autoregressive Q-functions), **DPPO** [96] (policy optimization for diffusion policies), and **Self-Improving Embodied Foundation Models** [97] (autonomous data generation and filtering). 

Rather than learning purely from collected experience, **GigaBrain-0.5M** [53] integrates a world model with VLA training. The world model predicts future visual observations given current actions, allowing the VLA to “imagine” the consequences of action sequences without physical execution, a form of model-based RL that generates synthetic training data. Two-arm coordination demands that the world model predict complex multi-body dynamics, including how both arms and the manipulated object evolve over time. While world-model-based RL for bimanual VLAs is still early-stage, it represents a promising path toward sample-efficient training of complex coordination behaviors. 

## _6.4. Data Collection for Bimanual Manipulation_ 

High-quality bimanual demonstration data is the bottleneck for VLA training. Three data collection strategies have emerged. 

**ALOHA** [16] uses bilateral teleoperation: a human operator controls follower arms by physically moving kinematically identical leader arms. This provides intuitive, lowlatency control for dexterous bimanual tasks. The ALOHA hardware costs under USD 20,000 and has been replicated at dozens of institutions, creating a growing ecosystem of bimanual data. 

**UMI** [43] decouples data collection from the robot entirely. Operators use hand-held gripper tools with visual–inertial tracking to demonstrate tasks in any environment. The collected trajectories are retargeted to the robot’s action space during training. UMI allows data collection by non-experts in diverse settings, increasing data diversity. 

**Autonomous data collection** , as in RECAP [4], uses the VLA itself to collect additional data. Starting from a reasonably capable policy, the robot attempts tasks autonomously, and a success classifier (often another VLM) labels the outcomes. This approach can generate 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

21 of 59 

thousands of additional episodes with minimal human effort, and the data naturally covers the policy’s distribution, reducing the train–test mismatch that plagues behavioral cloning. 

**Data quality** matters as much as quantity: teleoperation quality varies across operators, language labels are often inconsistent, and demonstrations including recovery from near-failures contribute disproportionately to robustness. Fleet-based data strategies [98] established the precedent for VLA-scale collection, and **GigaBrain-0.5M** [53] addresses quality through automated world-model-based filtering. 

Data collection throughput varies: ALOHA teleoperation [16] yields 50–100 demos/h, UMI [43] achieves _∼_ 110 demos/h with non-expert operators (3 _×_ faster than spacemouse), and autonomous RECAP [4] runs continuously without supervision (4–12 episodes/h for complex tasks). These economics favor a hybrid strategy: bootstrap with demonstrations, then scale through autonomous practice. 

## _6.5. Data Scaling Laws_ 

VLA performance scales differently with different data types. Language-guided data generation [99] has shown that automatically generated language annotations can significantly expand effective training set size. **Cross-embodiment pre-training data** exhibits log-linear scaling, with dataset diversity (number of embodiments, environments, tasks) at least as important as raw volume [5]. **Task-specific fine-tuning data** shows steep initial scaling and diminishing returns: simple tasks require as little as 5 h, while complex bimanual tasks need 100+ hours [2]. **Autonomous practice data** from RECAP [4] yields large gains from modest data: _∼_ 300 autonomous trajectories per iteration improved laundry folding from _∼_ 30% to over 90%. 

Table 5 summarizes the training strategies across representative VLA methods. The pipeline is converging on a three-stage recipe: (1) initialize from a strong VLM, (2) pretrain on diverse cross-embodiment data with co-training, and (3) fine-tune on task-specific bimanual demonstrations, optionally followed by RL. 

**Table 5.** Comparison of training strategies for VLA models. Pre-train data and fine-tune data indicate the primary datasets used. RL indicates whether reinforcement learning is incorporated. 

|**Method**|**VLM Init**|**Pre-Train Data**|**Fine-Tune Data**|**Co-Train**|**RL**|**Key Strategy**|
|---|---|---|---|---|---|---|
|**RT-2** [1]|PaLI-X|Google fleet|–|–|–|VLM co-fine-tuning|
|**OpenVLA**[5]|Prismatic|l<br>OXE|Task-specific|–|–|i<br>Open data pre-train|
|**Octo**[6]|From scratch|OXE (800K)|i<br>Task-specific|–|–|<br>Cross-embodiment init|
|_π_0 [2]|PaLIGemma|OXE + proprietary|50–200 demos|✓|–|Co-training mix|
|_π_0.5 [3]|PaLIGemma|<br>OXE + fleet|Fleet demos|✓|–|<br>Hierarchical training|
|_π_<sup>_∗_</sup><br>0 <sup>[4]</sup>|_π_0 ckpt|l<br>Same as_π_0|Autonomous + demos|✓|✓|<br>RECAP (VLM reward)|
|<br>**RDT-1B**[44]|SigLIP + T5|Multi-robot|ALOHA tasks|–|–|Scale (1.2B params)|
|**FAST**[8]|<br>VLM|OXE|Task-specific|–|–|<br>Learned tokenizer|
|**GigaBrain**[53]|VLM|GigaBrain-0.5M|i<br>Task-specific|–|✓|World-model RL|


**Key takeaways from the training section.** Three points deserve to be carried into the rest of the review. First, _data diversity_ (across embodiments, scenes, and tasks) is a more reliable lever for generalization than raw dataset size and is now the de facto requirement for any VLA targeting cross-embodiment deployment. Second, _co-training_ that mixes manipulation, mobile, and vision–language data within a single optimization, rather than chaining them sequentially, is what allows VLAs to retain semantic capability while learning low-level control. Third, _reinforcement learning from autonomous practice_ —in particular the RECAP-style loop demonstrated by _π_ 0<sup>_∗_—is the principal mechanism that</sup> lifts VLAs above their teleoperated demonstration ceiling and, together with the first two points, accounts for most of the recent progress on long-horizon, contact-rich tasks. How 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

22 of 59 

actions are represented and executed within these pipelines is equally consequential for real-time bimanual control, which we address next. 

# **7. Action Representations and Real-Time Execution** 

The choice of action representation directly shapes VLA performance, especially for bimanual tasks where the action space is high-dimensional and temporal coordination is critical. We emphasize that action representation is not merely an output-format choice but the principal mechanism by which a VLA satisfies—or fails to satisfy—real-time control constraints: each candidate representation imposes its own latency profile (per-dimension token generation in autoregressive heads, multi-step denoising in diffusion/flow heads, single-pass continuous prediction in distilled heads), and this latency directly determines whether the policy can close the control loop at the 50 Hz rates required for bimanual manipulation or the _≥_ 100 Hz rates required for stable flight. Building on the architectural foundations in Section 5 and the “Actions” branch of the taxonomy in Figure 1, this section covers discrete tokenization, continuous generation, action chunking strategies, and recent advances in real-time execution. 

## _7.1. Discrete Action Tokenization_ 

The simplest approach to interfacing robot actions with a language model is to discretize continuous actions into tokens. 

**Uniform binning** , used by **RT-2** [1] and **OpenVLA** [5], divides each action dimension into _B_ equally spaced bins (typically _B_ = 256). A 7-DOF arm action is represented as 7 tokens, each from a vocabulary of size _B_ . This approach is simple but introduces quantization error proportional to 1/ _B_ and requires sequential token generation, with latency scaling linearly with the number of dimensions. For bimanual systems with _da_ = 16 (see Section 2.4), generating 16 tokens sequentially becomes a latency bottleneck. 

The inefficiency of uniform binning motivated a learned alternative. In **FAST** [8], a VQ-VAE is trained to compress action chunks into a small number of discrete tokens. Because the tokenizer learns the structure of robot actions (temporal smoothness, joint correlations, coordination patterns), it can represent a 50-step, 16-dimensional bimanual action chunk with as few as 32 tokens, compared to 50 _×_ 16 = 800 tokens with perdimension binning. The learned tokenizer also produces a denser token vocabulary where every token corresponds to a meaningful action pattern, unlike uniform binning where most of the 256 bins are rarely used. 

Cross-embodiment transfer demands that action tokens generalize across morphologies. **Universal action tokenization** [100] achieves this with a shared tokenizer that learns embodiment-agnostic action representations, so that a single autoregressive VLA can generate actions for robots with different morphologies. For bimanual systems, universal tokenization offers the prospect of transferring manipulation knowledge from single-arm datasets to dual-arm systems, since the tokenizer can learn correspondences between single-arm and bimanual action patterns. 

Complementary approaches include **consistency models** [101] (distilling multi-step diffusion into a single forward pass), **ACT** [16] (improved temporal ensembling for bimanual trajectories), and **RACER** [102] (language-guided corrective actions for error recovery). 

Discrete tokenization preserves compatibility with VLM text generation but introduces quantization error that compounds across 16 bimanual action dimensions and 50 timesteps per chunk. Continuous generation avoids this issue but requires iterative denoising. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

23 of 59 

## _7.2. Continuous Action Generation_ 

Continuous action generation avoids discretization entirely, predicting real-valued action vectors. 

Flow matching ( _π_ 0 [2]) and diffusion ( **Diffusion Policy** [40], **RDT-1B** [44]), whose architectural details appear in Section 5, generate continuous actions through iterative denoising. The primary advantage is fidelity: continuous predictions avoid quantization error, which compounds across the 16 action dimensions of a bimanual system. The primary disadvantage is inference cost: each prediction requires _K_ denoising steps, each involving a forward pass through the action head. 

The number of denoising steps _K_ trades off quality against speed. _π_ 0 [2] uses _K_ = 10 flow matching steps, which strikes a good balance for bimanual control at 50 Hz. Diffusion policies typically require _K_ = 50–100 DDPM steps, though DDIM acceleration reduces this to _K_ = 10–20 with modest quality loss. 

## _7.3. Action Chunking Strategies_ 

Action chunking (Section 2.2) is now standard in VLA systems. The chunk horizon _H_ is a critical hyperparameter. 

Short chunks ( _H_ = 1–4) provide high reactivity (the policy can respond to environmental changes quickly) but require frequent VLM inference and suffer from myopic behavior. **Octo** [6] uses _H_ = 4, suitable for its lightweight architecture. 

Long chunks ( _H_ = 50–100) amortize inference cost and capture long-range temporal structure but commit the robot to extended open-loop execution. _π_ 0 [2] uses _H_ = 50, which at 50 Hz corresponds to 1 s of motion. When both arms act in concert (e.g., folding), long chunks capture the coordinated motion pattern of both arms within a single prediction. 

When a task has distinct phases (approach, grasp, manipulate, release), the chunk horizon should cover at least one complete phase. Empirically, _H_ = 50 at 50 Hz (1 s) is the sweet spot for most bimanual primitives. 

**Temporal ensembling** blends overlapping action chunks to smooth transitions and improve robustness. Given the current chunk **A** _t_ and the previous chunk **A** _t−s_ (shifted by _s_ steps), the executed action is: 


where **a**<sup>new</sup> _t_ is the action at time _t_ from the most recently predicted chunk **A** _t_ , **a**<sup>old</sup> _t_ is the corresponding action from the previously predicted (overlapping) chunk **A** _t−s_ , and _λ ∈_ [0, 1] controls the blending weight, typically decaying exponentially over the chunk. 

## _7.4. Real-Time Chunking (RTC)_ 

Long action chunks and fast reactions seem fundamentally at odds, but **RTC** [103] resolves this tension by restructuring how chunks are generated and executed. Rather than computing an entire chunk and executing it open-loop, RTC interleaves computation and execution: while the current chunk is being executed, the next chunk is computed in the background. When the next chunk is ready, the policy smoothly transitions to it, regardless of where execution is in the current chunk. 

RTC’s key contribution is showing that with careful scheduling, a flow-matching VLA can achieve both long-horizon coherence (from large chunks) and sub-100 ms reactivity (from overlapping computation). In dual-arm tasks, this allows the robot to respond to unexpected perturbations (e.g., an object slipping from one gripper) without waiting for the current chunk to complete. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

24 of 59 

The effective reaction time is bounded by the computation time for one chunk (typically 50–70 ms for _π_ 0), a significant improvement over the full chunk execution time (1000 ms for _H_ = 50 at 50 Hz). 

## _7.5. Bidirectional Decoding (BID)_ 

For tasks where both endpoints are well defined but the intermediate trajectory is ambiguous, **BID** [104] generates action chunks from both ends simultaneously. Given a chunk of horizon _H_ , two decoders are initialized: a forward decoder starting from the current state and a backward decoder starting from the goal state. The two decoders produce action sequences that are merged at a midpoint. This bidirectional approach is especially relevant for bimanual handover tasks, where the initial grasp (forward) and the final placement (backward) are well defined but the intermediate transfer motion admits multiple solutions. BID resolves this ambiguity by anchoring both endpoints. 

## _7.6. Training-Time Action Conditioning_ 

A subtle source of performance degradation is the train–test mismatch in action conditioning: during training, the action head conditions on ground-truth features unavailable at test time. **TTAC** [105] bridges this gap by conditioning the action head on its own predictions during training via a stop-gradient mechanism. On bimanual tasks, this improves success rates by 5–15% without architectural changes, with gains strongest at high action dimensionality ( _da_ = 16). 

Table 6 summarizes the action representation landscape. The choice of action representation involves a three-way tradeoff between expressiveness, speed, and simplicity. 

**Table 6.** Comparison of action representations in VLA models. Latency is per action-chunk inference on a single GPU. Bimanual _da_ indicates the action dimension for bimanual systems. 

|**Method**|**Representation**|**Chunk****_H_**|**Steps****_K_**|**Bimanual****_da_**|**Latency**|**Key Innovation**|
|---|---|---|---|---|---|---|
|**RT-2** [1]|Uniform bins (256)|1|–|8|_∼_200 ms|VLM token reuse|
|**OpenVLA**[5]|Uniform bins (256)|1|–|8|_∼_150 ms|Open-source|
|**FAST**[8]|Learned VQ-VAE|50|–|16|_∼_80 ms|Compressed tokens|
|_π_0[2]|Flow matching|50|10|16|_∼_70 ms|VLM-conditioned flow|
|**Diff. Policy**[40]|DDPM/DDIM|16|50–100|16|_∼_300 ms|Multi-modal actions|
|**RDT-1B**[44]|DiT diffusion|64|20|16|_∼_150 ms|Scale (1.2B)|
|**RTC**[103]|Flow + overlap|50|10|16|_<_50 ms *|Interleaved exec.|
|**BID**[104]|Bidirectional|Variable|Variable|16|_∼_100 ms|Dual-end decode|


* Effective latency with overlapped computation. 

Discrete tokenization (RT-2, OpenVLA) is the simplest to implement atop existing VLMs but sacrifices fine-grained control and scales poorly with action dimension. Flow matching ( _π_ 0, RTC) offers the best latency–quality balance for high-dimensional bimanual actions, generating smooth 16-dimensional chunks in _∼_ 70 ms with only 10 denoising steps. Diffusion models (RDT-1B, Diffusion Policy) provide the strongest multi-modal modeling but at 2–4 _×_ higher latency due to 50–100 denoising steps. Learned tokenizers (FAST) bridge the gap by compressing continuous chunks into compact discrete representations, achieving autoregressive simplicity with chunk-level expressiveness. For bimanual control at 50 Hz, effective latency below 20 ms per step is critical, making overlapped execution (RTC) or long-horizon chunking essential regardless of the underlying representation. 

# **8. Bimanual Manipulation with VLAs** 

Bimanual manipulation is the primary application focus of this review. Prior work has studied bimanual coordination from multiple perspectives: Grannen et al. [106] pro- 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

25 of 59 

pose a “stabilize to act” framework where one arm stabilizes while the other manipulates, and Chitnis et al. [107] learn task schemas for efficient bimanual planning. As shown in the “Bimanual” branch of Figure 1, this section examines how VLAs address the unique challenges of bimanual coordination, organized by coordination strategy (Table 7) and task type (Table 8). Table 9 lists the principal hardware platforms. The action representations and chunking strategies discussed in Section 7 are central to the coordination mechanisms described below. Figure 4 illustrates the ALOHA platform and its bilateral teleoperation interface. 


**Figure 4.** The ALOHA bimanual teleoperation platform and representative tasks. A human operator controls two follower arms via leader arms for intuitive demonstration collection. ALOHA and its ACT policy established the standard platform for bimanual VLA research. Reprinted with permission from Ref. [16]. Copyright 2023, Zhao et al. 

**Table 7.** Comparison of bimanual coordination strategies in VLA models. _da_ indicates the effective action dimensionality per step. Tight coupling indicates whether the strategy supports simultaneous force-coordinated bimanual actions. 

|**Strategy**|**_da_**|**Coupling**|**Methods**|
|---|---|---|---|
|Joint space|_dL_ +_dR_|✓|_π_0, RDT-1B, ACT|
|Independent|max(_dL_,_dR_)|–|Hi Robot|
|Leader–follower|_dL_|Partial|Custom setups|
|Hierarchical|Variable|✓|_π_0.5, Hi Robot|


**Table 8.** Approximate success rates (%) on bimanual tasks, as reported in the original publications under varying evaluation conditions. Values across methods are not directly comparable due to differences in task definitions, object sets, and evaluation protocols. Tasks grouped by category. 

|**Task Category**|**Specific Task**|**_π_0**|**_π_**<sup>*****</sup><br>**0**|**RDT-1B**|**ACT**|**Diff. Policy**|
|---|---|---|---|---|---|---|
|_Dbl_|Laundry folding|80|92|–|50|35|
|_eformae_|Towel folding|85|95|60|55|40|
||Box assembly|75|88|55|40|30|
|_Contact-rich_|<br>Peginsertion (bimanual)|70|85|50|45|35|
||Table busing|65|80|–|30|–|
|_Long-horizon_|<br>Kitchen cleanup|60|78|–|–|–|
||Object handover|90|95|75|70|60|
|_Coordination_|<br>Collaborative lift|85|93|70|60|50|


https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

26 of 59 

**Table 9.** Bimanual hardware platforms used with VLA models. DOF/arm indicates degrees of freedom per arm plus gripper. Cost is approximate at time of introduction. 

|**Platform**|**DOF/Arm**|**Mobile**|**Cost**|
|---|---|---|---|
|**ALOHA** [16]|6 + 1|–|_<_$20K|
|**Mobile ALOHA**[42]|6 + 1|✓|_<_$30K|
|**Franka Dual**|7 + 1|–|_>_$60K|
|**UMI**[43]|N/A *|–|_<_$5K|


* UMI is a data collection interface, not a robot. 

## _8.1. Coordination Strategies_ 

We first formalize the bimanual coordination objective. The bimanual VLA policy _πθ_<sup>bi</sup> maps observations and proprioception from both arms to a joint action chunk: 


where _Q_<sup>_L_</sup> and _Q_<sup>_R_</sup> are the proprioceptive state spaces of the left and right arms. The degree of required coordination can be characterized by the mutual information _I_ ( **A** _t_<sup>_L_;</sup><sup>**A**</sup> _t_<sup>_R|_</sup><sup>**o**</sup><sup>_t_,</sup><sup>_ℓ_)</sup> between the two arms’ action chunks. For independent tasks, this quantity is near zero; for loosely coupled tasks, it reflects timing dependencies; and for tightly coupled tasks such as folding or assembly, it is large, indicating strong inter-arm correlations. The three coordination strategies described below differ in how they handle this coupling. 

## 8.1.1. Joint Action Space 

The most common approach treats the bimanual system as a single high-dimensional policy. The action chunk **A** _t ∈_ R<sup>_H×_(</sup><sup>_dL_+</sup><sup>_dR_)</sup> encodes both arms jointly, allowing the model to learn implicit coordination. _π_ 0 [2] and **RDT-1B** [44] both use this approach, predicting the left and right arm actions as a concatenated vector. The advantage is simplicity: no explicit coordination mechanism is needed, and the model can learn arbitrary coordination patterns from data. The disadvantage is that the action space is large ( _H ×_ 16 dimensions for typical settings), requiring expressive generative models to capture the joint distribution. 

Flow matching is well suited to this approach because it generates the entire action chunk in a single denoising process, naturally preserving inter-arm correlations. The flow field **v** _θ_ operates on the full _H ×_ ( _dL_ + _dR_ )-dimensional space, learning the joint velocity field that transports noise to coordinated bimanual trajectories. This global denoising preserves correlations between left and right arm motions at every timestep within the chunk. 

In contrast, autoregressive generation of a joint action vector must predict left and right arm actions in some sequential order, potentially breaking symmetry. If the model generates left arm actions before right arm actions (or vice versa), the second arm’s predictions are conditioned on the first arm’s, introducing an artificial asymmetry that may not reflect the actual task structure. While this asymmetry can be mitigated through data augmentation (randomly swapping left and right arm labels), it remains a conceptual limitation of autoregressive bimanual action generation. 

## 8.1.2. Independent Policies 

An alternative is to train separate policies for each arm, coordinated by a high-level planner. **Hi Robot** [29] decomposes bimanual tasks hierarchically: a high-level VLM generates subtask descriptions for each arm, and separate low-level policies execute them. This approach simplifies each policy’s action space but requires the high-level planner to handle coordination timing and conflict avoidance. 

In practice, independent policies work well for loosely coupled tasks (e.g., one arm holds an object while the other operates on it) but struggle with tightly coupled tasks 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

27 of 59 

(e.g., folding, where both arms must move in concert). The coordination information that joint policies learn implicitly must be provided explicitly through the high-level planner’s instructions. 

## 8.1.3. Leader–Follower 

In the leader–follower strategy, one arm (the leader) executes the primary manipulation while the other (the follower) adapts to maintain a constraint (e.g., holding an object stable). This asymmetric decomposition reduces the effective planning complexity and can be encoded in the VLA by conditioning one arm’s actions on the other’s predicted trajectory. Several bimanual VLA systems implement soft leader–follower coordination implicitly through the joint action space, where the model learns that one arm typically initiates contact while the other provides support. 

## _8.2. Contact-Rich Bimanual Tasks_ 

Contact-rich tasks, where both arms simultaneously exert forces on an object, are among the most challenging for VLAs. Examples include inserting a peg with one arm while the other holds the socket, tightening a cap on a bottle held by the other arm, and assembling parts that require precise force alignment. 

Contact-rich bimanual performance has been most thoroughly evaluated on box assembly, where one arm holds a box while the other folds flaps. _π_ 0 [2] achieves smooth force profiles on this task through its flow-matching action head, avoiding the jerkiness of discrete-action policies. An equally important insight came from **ALOHA (ACT)** [16]: action chunking is critical for contact-rich tasks, as single-step predictions produce oscillatory contact forces while chunked predictions maintain stable contact throughout a manipulation primitive. 

Most VLAs operate in position or velocity space without explicit force feedback, inferring contact states from visual cues alone. _π_ 0 [2] learns appropriate forces during box assembly purely from visual demonstrations, but vision alone likely breaks down for high-precision force-sensitive operations. _π_ 0<sup>_∗_[4] partially addresses this through RL from</sup> autonomous practice, where the robot discovers effective force profiles through trial and error. The difficulty scales with contact points: current VLAs handle two-point contact well, but multi-point contact and multi-fingered dexterous manipulation remain open frontiers. 

## _8.3. Deformable Object Manipulation_ 

Deformable objects (fabric, rope, dough, plastic bags) present distinct challenges for bimanual VLAs: the object state is high-dimensional and partially observable, and manipulation requires coordinated bimanual actions that account for material dynamics. 

Laundry folding is the canonical bimanual deformable-object task and, until recently, an unsolved problem. Success rates above 80% on T-shirt folding became possible when _π_ 0 [2] combined flow matching with long action chunks, learning the complex bimanual coordination required to pinch, lift, fold, and smooth fabric. The success relies on long action chunks ( _H_ = 50, as analyzed in Section 7.3) that capture the full folding motion as a continuous trajectory and on the VLM backbone’s ability to visually parse the garment’s configuration. 

Building on this, _π_ 0.5 [3] generalized folding to arbitrary garments in novel homes. The hierarchical architecture decomposes folding into subgoals (e.g., “pick up the left sleeve”, “fold it toward the center”), with the high-level VLM reasoning about garment topology and the low-level policy handling motor execution. Current success rates on fabric folding are measured on a narrow range of garment types; generalization to thin, slippery, or multi-layered fabrics remains undemonstrated. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

28 of 59 

Beyond fabric, bimanual deformable-object manipulation encompasses rope knotting, dough shaping, and bag opening. The difficulty increases from 1D deformation (rope) through 2D (fabric with self-occlusion) to 3D (dough, clay). Current VLAs address these through large action chunks that capture entire primitives, which works when deformation is predictable but fails for materials with complex dynamics. Integrating tactile sensing to detect material state is a promising direction. 

## _8.4. Long-Horizon Bimanual Tasks_ 

Long-horizon tasks require the robot to execute many bimanual primitives in sequence, with the correct ordering determined by task semantics. Table clearing, for example, requires picking up plates, stacking them, wiping the table, and placing items in a bin: a sequence of 10–20 bimanual actions over several minutes. 

_π_ 0.5 [3] handles long-horizon tasks through its hierarchical architecture: the highlevel VLM maintains a task plan and generates subgoal instructions, while the low-level policy executes each subgoal. The high-level model can re-plan based on visual feedback, recovering from failures or adapting to unexpected states. **Hi Robot** [29] similarly uses hierarchical VLA reasoning for open-ended instructions, decomposing “tidy the desk” into a sequence of specific bimanual actions. 

Prior work on LLM-based planning provides the conceptual foundation for longhorizon VLA reasoning. **Code as Policies** [108] uses LLMs to generate executable code that sequences manipulation primitives, while **SayCan** [109] grounds LLM proposals in learned affordance scores, ensuring that only feasible actions are selected. Both approaches separate high-level reasoning from low-level execution, a principle adopted by hierarchical VLAs. 

Complementary approaches learn long-horizon skills from unstructured data. **MimicPlay** [110] decomposes human play videos into plan representations, **PlayFusion** [111] acquires skills via diffusion from play data, and Du et al. [112] learn policies via text-guided video generation. **Look Before You Leap** [113] uses GPT-4V to preview action consequences. These planning strategies predate VLAs but are complementary and could be integrated with VLA execution. 

Long-horizon bimanual tasks demand robust _error recovery_ . Hierarchical VLAs address this naturally: the high-level VLM detects failures and generates recovery subgoals. _π_ 0<sup>_∗_[4]</sup> improves recovery through autonomous practice (Section 6.3), learning robust behaviors that pure imitation cannot provide. The temporal extent also poses a computational challenge: a 5-minute task at 50 Hz involves 15,000 control steps (300 chunk-level decisions with _H_ = 50), requiring either hierarchical planning or long-context models. 

Recent work addresses this limitation by equipping VLAs with explicit _memory_ mechanisms. **MEM** [74] introduces _Multi-Scale Embodied Memory_ , a system that combines two complementary modalities: a video encoder for short-horizon, image-based memory (which supports in-context adaptation and occlusion recovery over seconds) and a language-based memory that maintains compressed text summaries of semantic events over long horizons (up to 15 min). Integrated into the _π_ 0.6 VLA, MEM achieves state-of-the-art results on tasks such as recipe setup, kitchen cleanup, and grilled cheese preparation while matching non-memory VLAs on standard dexterous manipulation. Different time scales require different memory representations: dense visual context for recent events and compressed language for long-term semantic state. 

Concurrent approaches explore complementary designs. Context-compression methods include **ContextVLA** [76] (amortizing multi-frame context into a single token), **CronusVLA** [114] (learnable temporal feature chunking), **BPP** [115] (conditioning on VLMdetected keyframes), and past-token prediction [116] (3 _×_ gains at 10 _×_ reduced cost). Retrieval-based methods include **MemoryVLA** [75] (perceptual-cognitive memory bank; 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

29 of 59 

+14.6% on Bridge), **SAM2Act** [117] (episodic spatial memory; 86.8% across 18 RLBench tasks), **MemER** [118] (VLM-guided keyframe retrieval), and **CycleManip** [119] (cost-aware historical sampling for cyclic tasks). 

Memory-augmented VLAs enable long-horizon execution (up to 15 min), in-context adaptation, and partial observability handling. However, they face two intertwined challenges: _causal confusion_ , where the policy learns to copy its own past actions rather than reason about the current state, and _train-inference shift_ , where self-generated memory summaries at test time may contain compounding errors. MEM mitigates causal confusion via language compression that discards failed attempts, but the general problem remains unsolved. Additional limitations include computational overhead that scales with history length and information loss from memory compression (semantic events are retained, but fine-grained contact forces are not). Current memory systems are episodic, with no mechanism for accumulating knowledge across deployment sessions. 

## _8.5. Mobile Bimanual Manipulation_ 

Mobile bimanual systems add navigation to the manipulation challenge. The robot must move to the task location, position itself appropriately, and then perform bimanual manipulation, requiring coordination between the base and both arms. 

Whole-body teleoperation and imitation learning for mobile bimanual tasks were first shown by **Mobile ALOHA** [42], which controls the mobile base and two arms simultaneously for tasks such as cooking and furniture assembly, with action chunks covering all degrees of freedom. 

_π_ 0.5 [3] deployed VLA-controlled mobile bimanual robots in real homes, achieving high success rates on household tasks. The hierarchical architecture separates navigation decisions (handled by the high-level VLM) from manipulation execution (handled by the low-level policy), simplifying the learning problem. 

_Base-arm coordination_ is the additional challenge: the base must position itself so both arms reach target objects. **UMI-on-Legs** [120] extends hardware-agnostic data collection to legged platforms, **BUMBLE** [121] addresses building-wide mobile manipulation, and industrial efforts ( **AgiBot World** [122], **NILS** [123]) are scaling bimanual fleet data and policy learning. Figure 5 shows _π_ 0.5 deployed in real homes. 


**Figure 5.** Real-world deployment of _π_ 0.5 in homes. A hierarchical VLA decomposes high-level instructions into subgoals, with high success rates on household tasks such as table clearing and laundry folding. Reprinted with permission from Ref. [3]. Copyright 2025, Black et al. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

30 of 59 

Flow-based VLAs ( _π_ 0, _π_ 0<sup>_∗_)currentlyleadonmostbimanualtasks,withthejoint</sup> action space approach outperforming decoupled approaches on tightly coupled tasks by preserving inter-arm correlations. For loosely coupled tasks, hierarchical approaches offer interpretability through auditable subgoal decompositions. 

The coordination strategies analyzed above, joint action spaces for tightly coupled agents, hierarchical decomposition for complex tasks, leader–follower for asymmetric roles, are not specific to two-armed robots. They apply whenever a VLA must coordinate multiple coupled actuators from shared observations. We now examine a domain where exactly the same coordination problem arises in a different physical setting: unmanned aerial robotics. 

# **9. VLA for Unmanned Aerial Robotics and Drones** 

Section 8 showed how VLAs coordinate two arms through joint action spaces, hierarchical planning, and action chunking. Unmanned aerial robotics faces the same coordination problem in a different physical setting. A single drone must coordinate thrust, attitude, and (optionally) gripper commands; a multi-drone system must coordinate an entire fleet. The VLA machinery (VLM backbone for language grounding, flow matching or diffusion for smooth trajectory generation, action chunking for temporal coherence) applies directly. What changes is the action space: whereas bimanual VLAs generate joint positions or end-effector poses, aerial VLAs must produce velocity commands, waypoints, or low-level thrust-and-torque signals for underactuated platforms operating in threedimensional space. Latency constraints are stricter ( _≥_ 100 Hz for stable flight versus _∼_ 50 Hz for manipulation), the observation space often includes GPS, IMU, and depth sensing alongside monocular or stereo vision, and the environment is outdoor, three-dimensional, and wind-affected. Table 10 compares representative methods; Figure 6 charts the key milestones. 


**Figure 6.** Timeline of unmanned aerial robotics milestones for learning-based drone control (2017– 2026). Colors indicate the research area: RL-based control (blue), vision–language navigation (green), aerial manipulation (red), language-guided planning (orange), and simulation platforms (purple). Early work focused on RL for agile flight and simulators; 2023–2024 saw the emergence of languageguided navigation; 2025–2026 marks the arrival of full VLA systems (CognitiveDrone, RaceVLA, DroneVLA, AIR-VLA) that integrate perception, language, and action generation end-to-end. 

## _9.1. VLA-Based Drone Navigation and Control_ 

## 9.1.1. Vision–Language Navigation for UAVs 

Vision–language navigation (VLN) requires a drone to reach a goal described in natural language (“fly above the red building”, “turn left at the intersection”) using only visual observations. VLN is related to but narrower than VLA: it addresses the _navigation_ subtask—selecting waypoints to reach a described destination—while VLA refers to the full perception-to-action pipeline including low-level motor control (thrust, attitude commands). Although VLN originated in indoor settings, the aerial variant poses distinct challenges: a 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

31 of 59 

vastly different visual perspective, a larger action space that includes altitude, and outdoor visual diversity. 

The **AerialVLN** benchmark [124] established this task with over 25,000 instruction– trajectory pairs across urban and rural environments, revealing that indoor VLN methods transfer poorly to aerial scenes. A zero-shot alternative, **LFG** [125], sidesteps task-specific training entirely by having an LLM convert language instructions into spatial cost maps that a standard path planner optimizes over. 

The most complete aerial VLA to date is **UAV-VLA** [126], which processes satellite imagery through a VLM backbone and generates full mission plans (waypoints, altitudes, sensor configurations) from natural language. On a 100K-mission dataset, it produces plans 6.5 _×_ faster than human operators at comparable quality, showing that VLAs can scale to operational aerial planning beyond single-flight control. 

More broadly, the field is rapidly standardizing. **UAV-VLN** [127] parses instructions into structured sub-goals grounded by a vision model; **OpenFly** [128] provides a large-scale benchmark spanning urban, suburban, rural, and industrial settings; and **CityNavAgent** [129] adds a persistent semantic map that supports city-scale navigation with hierarchical planning. Beyond urban environments, **AgriVLN** [130] extends VLN to agricultural settings, providing 1,560 episodes across six outdoor scene types (farms, greenhouses, forests, mountains, gardens, and villages) and demonstrating that VLN models trained on indoor or urban data transfer poorly to unstructured agricultural landscapes. 

## 9.1.2. End-to-End Learned Flight Control 

In contrast to modular pipelines, end-to-end approaches map raw sensor observations directly to flight commands, bypassing the traditional perception–planning–control pipeline. The feasibility of this approach was established early: a single neural network trained with RL [131] can map quadrotor state directly to motor commands, stabilizing the vehicle even when thrown upside-down at 5 m/s, with policy evaluation taking only 7 µs per step (Figure 7); this proves that learned policies can replace hand-designed cascaded PID controllers for agile flight. 


**Figure 7.** An RL-trained quadrotor recovering from an inverted throw at 5 m/s. The policy maps state to motor commands at 7 µs per step, establishing the viability of learned end-to-end drone control. Reprinted with permission from Ref. [131]. Copyright 2017, Hwangbo et al., IEEE. 

Subsequent learned systems pushed the performance frontier to superhuman levels. The landmark result is an RL-trained autonomous racing policy [132] that processes 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

32 of 59 

onboard vision and IMU at 100 Hz and defeated world-champion human pilots. A complementary approach, neural residual dynamics models [133], uses supervised learning on flight data to learn the gap between the physics model and reality, improving autonomous landing accuracy by compensating for unmodeled aerodynamic effects. 

Two recent systems bring the VLA framework directly to drones. **CognitiveDrone** [9], trained on 8000+ simulated trajectories, generates real-time 4D actions ( _x_ , _y_ , _z_ , yaw) from first-person imagery and text instructions. Its R1 variant adds VLM-based chain-of-thought reasoning before acting, which lifts the success rate to 77.2%, a 30% gain that demonstrates the value of deliberation for aerial cognitive tasks. **RaceVLA** [134] trains on expert pilot demonstrations annotated with language (“aggressive apex cutting”, “conservative trajectory”) and produces stylistically diverse racing trajectories, going beyond time-optimal control to capture human-interpretable flight behavior. 

World models are also gaining traction for aerial control. **Dream to Fly** [135] learns a latent dynamics model from visual observations and plans by simulating future trajectories in the learned space, reducing real-world data needs by an order of magnitude compared to model-free RL (see Section 11). Robustness to real-world disturbances remains a key gap: **Neural-Fly** [136] addresses this through rapid online adaptation, maintaining stable aggressive flight in winds exceeding 12 m/s by learning a wind-invariant representation from just a few flight segments. Diffusion-based policies, originally developed for manipulation (Section 5), are also being applied to generate smooth, multi-modal drone trajectories. 

## _9.2. Aerial Manipulation_ 

Aerial manipulation, where drones grasp, transport, and interact with objects, directly inherits the coordination challenges discussed in the bimanual context (Section 8). A drone performing aerial grasping must simultaneously stabilize its flight while executing precise gripper motions, a challenge analogous to bimanual base-arm coordination (Section 8.5). 

## Grasping and Payload Transport 

Aerial manipulation combines the challenges of flight stabilization and precise object interaction. While RL-based flight control [131] established that learned policies can stabilize quadrotors under extreme conditions, extending this to aerial grasping requires additionally coordinating gripper commands and compensating for payload-induced dynamics shifts. Two recent systems bring the full VLA pipeline to this problem. **DroneVLA** [10] integrates open-vocabulary object detection (Grounding DINO), gripper pose estimation (MediaPipe), and visual servoing into a language-commanded retrieval system: given “pick up the red box and deliver it to the table,” a VLM decomposes the instruction into manipulation sub-goals executed in sequence. **AIR-VLA** [11] provides the first benchmark and simulation testbed dedicated to aerial manipulation VLAs, with 3000 teleoperated demonstrations spanning base control, object understanding, semantic reasoning, and long-horizon planning; it systematically evaluates mainstream VLA and VLM models, revealing current capabilities and limitations for coupled UAV-manipulator control. 

A particularly relevant platform is **Flying Hand** [12], a fully actuated hexarotor with a 4-DOF arm that formulates control in the end-effector frame, decoupling manipulation precision from flight stabilization (Figure 8). Its imitation learning policy uses ACT (Section 7) to perform writing, peg-in-hole insertion, and pick-and-place, directly demonstrating that action chunking transfers from bimanual to aerial manipulation. The connection to bimanual coordination becomes explicit in an aerial harvesting system [137] where a dual-arm drone picks avocados: one arm stabilizes the branch while the other detaches the fruit by rotation, a leader–follower strategy identical to those analyzed in Section 8.1. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

33 of 59 


**Figure 8.** Flying Hand: a fully actuated hexarotor with a 4-DOF arm performing writing, peg-in-hole, and pick-and-place via ACT, demonstrating that action chunking transfers from manipulation to aerial systems. The numbers 1–4 along each row index successive video frames of the same task sequence (1: approach, 2: contact, 3: execution, 4: completion). Reprinted with permission from Ref. [12]. Copyright 2025, He et al. 

These platforms combine flight commands with gripper commands, yielding highdimensional action spaces that benefit from the same chunking strategies used for bimanual VLAs. Aerial inspection tasks (close-proximity structure navigation, contact-based measurement) further build on the contact-rich manipulation insights from Section 8.2. A significant gap remains, however: all current aerial manipulation VLAs have been tested only on simplified pick-and-place tasks with lightweight objects. Precision manipulation under wind disturbances and with heavy or awkward payloads has not been demonstrated. 

## _9.3. Language-Guided Drone Missions_ 

## 9.3.1. Natural Language to Flight Plans 

The same Code-as-Policies idea used for manipulation [108] (Section 10.2) extends naturally to drones: prompting an LLM with a drone API description lets it convert “survey the perimeter at 20 m” into executable waypoint commands with no task-specific training. **AeroAgent** [138] adds safety awareness to this approach, decomposing complex missions into atomic flight actions while respecting no-fly zones and altitude limits. A latency bottleneck remains, however: generating free-form code—i.e., having the LLM produce arbitrary Python or similar programs without structural constraints—is slow. **TypeFly** [139] addresses this by constraining the LLM to output programs in MiniSpec, a minimal drone-specific language with primitives like takeoff, move, rotate, and sense. The restricted grammar cuts generation latency below 500 ms, an order of magnitude faster than unconstrained approaches, making real-time mission replanning practical. 

## 9.3.2. Interactive and Corrective Language Control 

Real-time language correction during flight (“go higher”, “move left”, “stop”) requires low-latency VLA inference. This setting parallels the interactive language control studied for manipulation [140] but with stricter latency requirements due to flight dynamics. Cur- 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

34 of 59 

rent approaches use lightweight VLM encoders or pre-computed language embeddings to minimize inference overhead. 

## _9.4. Multi-Agent Aerial Systems_ 

Multi-drone coordination with VLAs exhibits direct structural parallels to bimanual coordination (Section 8.1). The joint action space approach for bimanual VLAs, where a single model generates actions for both arms simultaneously, naturally extends to multidrone systems where a centralized policy generates waypoints for all drones in the swarm. 

Multi-drone coordination mirrors the three bimanual strategies from Section 8.1. Centralized policies generate joint actions for all drones but face the same dimensionality scaling as bimanual joint action spaces. Decentralized approaches reduce per-agent complexity but require explicit coordination. Hierarchical approaches, where a high-level VLM assigns subgoals to individual drones ( **Hi Robot** [29], _π_ 0.5 [3]), offer the best scalability. **Decentralized MARL** [141] trains swarm policies where each drone outputs velocity commands from local observations, scaling to 10+ drones. Graph neural network architectures that model inter-drone communication provide a natural framework for swarm VLAs. Integrating VLM-based task assignment with MARL execution is a promising direction. However, no multi-drone VLA has been demonstrated on physical hardware; all results remain simulation-only. 

## _9.5. UAV–UGV Collaborative Systems_ 

Heterogeneous UAV–UGV systems exploit complementary capabilities: drones provide aerial survey while ground robots perform manipulation. VLMs provide a natural coordination interface via language-based task allocation. Cross-embodiment VLA pretraining (Section 10.4) is directly applicable; **Octo** [6] and **Octo 2.0** [142] already span manipulation, navigation, and locomotion embodiments. The coordination challenge mirrors bimanual leader–follower strategies (Section 8.1): one agent (typically the drone) provides context while the other (the ground robot) executes manipulation. No published system yet deploys a shared VLA policy across both a UAV and a UGV in a single mission, making this an open research direction (Section 12.3). 

## _9.6. Sim-to-Real Transfer for Aerial VLAs_ 

Simulation is especially important for aerial VLAs because real-world drone data collection is expensive, risky, and constrained by regulations. 

## 9.6.1. Simulation Environments 

Two simulators dominate aerial VLA research. **AirSim** [45], built on Unreal Engine, provides photorealistic rendering with accurate flight dynamics and a rich sensor API (cameras, IMU, GPS, LiDAR). **Flightmare** [46] takes a different approach, decoupling rendering from physics to reach _∼_ 200 _×_ real-time speeds for large-scale parallel RL training. Additional platforms ( **RotorS** [143], **Isaac Sim** , **Gazebo** ) serve complementary fidelity and scale requirements. 

Large-scale datasets fill the gap between simulated and real-world training data. **TartanAir** [144] spans hundreds of scenes with diverse weather and lighting; **Mid-Air** [145] focuses on low-altitude flights (1–20 m) with stereo images, depth, and semantic labels. 

## 9.6.2. Domain Adaptation and Reality Gap 

The sim-to-real gap for aerial systems involves both visual and dynamics discrepancies. _Visual domain randomization_ during training improves transfer of vision-based policies by exposing the model to varied textures, lighting, and weather conditions. _Dynamics randomization_ varies mass, inertia, drag, and motor characteristics to produce policies 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

35 of 59 

robust to the physical reality gap. These techniques parallel the sim-to-real methods used for manipulation VLAs (Section 11), with the additional challenge that aerodynamic effects (ground effect, wind gusts, rotor wash) are difficult to simulate accurately. 

**Table 10.** Representative VLA and learning-based methods for unmanned aerial robotics. Action type indicates the output space of the learned policy. Sim indicates whether the method uses simulation for training. 

|**Method**|**Task**|**Approach**|**Action Type**|**Sim**|**Year**|**Highlights**|
|---|---|---|---|---|---|---|
|_Navigation and Control_<br>AerialVLN [124]<br>LFG [125]<br>UAV-VLA [126]<br>UAV-VLN [127]<br>OpenFly [128]|VL navigation<br>Language nav.<br>Mission gen.<br>VL navigation<br>VLN benchmark|VLN baseline<br>LLM_→_cost map<br>VLA (sat. imagery)<br>LLM + vision<br>Toolchain|Waypoints<br>Waypoints<br>Waypoints<br>Waypoints<br>Waypoints|✓<br>–<br>–<br>✓<br>✓|2023<br>2023<br>2025<br>2025<br>2025|First outdoor aerial VLN benchmark<br>Zero-shot LLM-guided navigation<br>6.5_×_faster than human; 100K missions<br>End-to-end VLN with LLM parsing<br>Large-scale aerial VLN benchmark|
|<br>CityNavAgent [129]<br>AgriVLN [130]<br>Hwangbo et al. [131]|City-scale nav.<br>Agricultural nav.<br>Stabilization|Hierarchical VLN<br>VLN benchmark<br>RL|Waypoints<br>Waypoints<br>Motor cmds|✓<br>✓<br>✓|2025<br>2025<br>2017|<br>Semantic planning + global memory<br>1560 episodes; 6 outdoor scene types<br>7µs inference; thrown recovery|
|<br>Kaufmann et al. [132]<br>CognitiveDrone [9]<br>RaceVLA [134]<br>Neural-Fly [136]<br>Dream to Fly[135]|Drone racing<br>Cognitive tasks<br>Drone racing<br>Agile flight<br>Vision flight|RL<br>VLA<br>VLA<br>Adaptive NN<br>Model-based RL|Motor cmds<br>4D(_x_,_y_,_z_, yaw)<br>Velocity cmds<br>Motor cmds<br>Velocitycmds|✓<br>✓<br>✓<br>–<br>✓|2023<br>2025<br>2025<br>2022<br>2025|<br>Superhuman agile flight<br>77.2% success with VLM reasoning<br>Human-like racing behavior<br>Online adaptation in strong winds<br>Learned world model for planning|
|_Aerial Manipulation_|||||||
|<br>Hwangbo et al. [131]|Quadrotor ctrl|RL|Thrust cmds|✓|2017|RL-based flight control|
|<br>DroneVLA [10]<br>AIR-VLA [11]<br>Flying Hand [12]<br>Aerial Bimanual [137]|Object retrieval<br>Aerial manip.<br>Dexterous manip.<br>Harvesting|VLA + servoing<br>VLA benchmark<br>ACT + MPC<br>Dual-arm aerial|EE pose + grip<br>Flight + grip<br>6-DOF + 4-DOF arm<br>Dual-arm cmds|–<br>–<br>–<br>–|2026<br>2026<br>2025<br>2024|l<br>Language-commanded aerial manipulation<br>Safety-constrained; 20 Hz testbed<br>Hexarotor; writing, peg-in-hole<br>Bimanual aerial manipulation|
|_Language-Guided Mission_|_s_||||||
|<br>AeroAgent [138]<br>TypeFly[139]|<br>Mission plan<br>Mission plan|LLM agent<br>LLM_→_MiniSpec|API calls<br>API calls|–<br>–|2023<br>2024|LLM mission decomposition<br>Low-latencyprogramgeneration|
|_Multi-Agent_<br>MARL Swarms [141]|Formation|Decentralized MARL|Velocitycmds|✓|2021|Scalable to 10+ drones|
|_Simulation, Datasets, and_|_Sim-to-Real_||||||
|AirSim [45]|Sim platform|UE4 rendering|Various|✓|2018|Photorealistic drone sim|
|Flightmare [46]<br>TartanAir [144]|<br>Sim platform<br>Dataset|<br>Parallel RL<br>Multi-modal|Various<br>–|✓<br>✓|2021<br>2020|200_×_real-time training<br>Diverse visual conditions; SLAM focus|
|Mid-Air [145]|Dataset|Multi-modal|–|✓|2019|Low-altitude flights; depth + semantics|


The aerial landscape shows rapid progress: 2025–2026 has seen a surge of aerial VLA systems and benchmarks (UAV-VLA, CognitiveDrone, DroneVLA, AIR-VLA, Flying Hand) that target mapping observations and language to flight actions. The bridging of bimanual coordination with aerial manipulation [12,137] suggests bidirectional technical transfer. Research directions for advancing this convergence appear in Section 12. 

# **10. Language Grounding, Reasoning, and Generalization** 

VLAs condition on natural-language instructions, inheriting the semantic understanding of pre-trained VLMs. This section examines language grounding, hierarchical reasoning, open-ended instruction following, and cross-embodiment generalization, mechanisms applicable to both manipulation and aerial domains. 

## _10.1. Language-Conditioned Policies_ 

The roots of language-conditioned policy learning trace back to **Language-conditioned IL** [32], which established multi-task learning from language instructions, and **BC-Z** [146], which scaled it to zero-shot generalization. VLAs extend this lineage by processing language and image tokens through shared Transformer layers, supporting deep cross-modal reasoning. Emergent grounding (following novel phrasings and generalizing to unseen objects) was first observed in **RT-2** [1]. In contrast, _π_ 0 [2] conditions the flow-matching head on VLM hidden representations, grounding abstract instructions in continuous motor behaviors rather than discrete tokens. A persistent weakness is brittle instruction parsing: minor rephrasing or typographical errors can cause large performance drops. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

36 of 59 

## _10.2. Hierarchical Reasoning_ 

Complex instructions require decomposition into executable subgoals. **Hi Robot** [29] introduces a hierarchical VLA architecture where a high-level “reasoner” VLM processes the user’s open-ended instruction and the current visual observation to generate a specific subgoal instruction. A low-level “executor” VLA then carries out the subgoal. This decomposition allows Hi Robot to follow complex instructions such as “make me a sandwich” by generating subgoals such as “open the bread bag,” “pick up two slices,” “place cheese between them.” 

_π_ 0.5 [3] implements a similar hierarchy, with the high-level model additionally maintaining a task state representation that tracks progress through multi-step tasks. The high-level model can detect when a subgoal has failed and re-plan, providing robustness to execution errors. 

Prior work established hierarchical planning principles adopted by VLAs: **SayCan** [109] grounds LLM plans in affordance scores, **Code as Policies** [108] generates executable code, and **VoxPoser** [147] produces 3D value maps. These affordance-grounding principles are incorporated in hierarchical VLAs such as Hi Robot and _π_ 0.5. 

The language channel between high-level planner and low-level executor determines control granularity. Natural language subgoals ( **Hi Robot** [29]) are flexible but may be ambiguous; alternatives include code-based specifications [108] (precise but brittle) and goal images (rich but expensive to generate). Natural language is currently favored for its compatibility with VLM backbones. 

## _10.3. Open-Ended Instruction Following_ 

Open-ended instruction following tests generalization beyond the training distribution. **RT-2** [1] showed VLM pre-training enables following instructions involving novel objects absent from robot data. Related work includes **Manipulate-Anything** [148] (detailed instruction following), **Interactive Language** [140] (real-time streaming corrections), and **Chain-of-Thought Predictive Control** [149] (reasoning-guided action generation). 

VLM backbones bridge the gap between simple human commands (“fold the towel”) and the motor detail required for execution; _π_ 0 [2] and _π_ 0.5 [3] operate effectively with natural instructions. A persistent limitation is the lack of systematic evaluation: most results use hand-picked instruction sets—a small, manually curated collection of test commands rather than open-vocabulary or user-generated prompts—so reported success rates may overestimate real-world flexibility. Although VLMs can parse arbitrary natural language, current VLAs have only been validated on narrow instruction distributions and cannot reliably detect ambiguous or contradictory commands. 

## _10.4. Cross-Embodiment Transfer_ 

A key promise of VLAs is cross-embodiment generalization: a policy trained on data from multiple robots can be deployed on a new robot with minimal fine-tuning. The evidence is now substantial. **Octo** [6] pre-trains on OXE data spanning 22 embodiments and transfers to unseen robots with a few hundred fine-tuning demonstrations, while **OpenVLA** [5] confirms that OXE pre-training improves performance even on embodiments absent from the pre-training set. 

Cross-embodiment transfer is critical for dual-arm systems because bimanual demonstration data is scarce (as discussed in Section 6.4). A VLA pre-trained on diverse single-arm data can transfer visual and semantic representations to a bimanual system, even though the action space differs. The strongest evidence comes from _π_ 0 [2], which pre-trains on a mixture of single-arm and bimanual data and finds that single-arm data improves bimanual performance through shared visual representations. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

37 of 59 

The transition of VLA technology from research to industrial deployment is exemplified by **Xiaomi-Robotics-0** [150], which trains on data from multiple Xiaomi robot platforms with real-time execution optimizations for consumer hardware. 

Cross-embodiment transfer for bimanual systems requires handling different arm configurations. Approaches include action space normalization ( _π_ 0 [2] maps to a common end-effector format), embodiment-specific projection layers ( **Octo** [6], extended to navigation and locomotion in **Octo 2.0** [142]), and language-based action hierarchies ( **RT-H** [151]). 

## _10.5. Zero-Shot and Few-Shot Generalization_ 

Zero-shot generalization (performing tasks with no task-specific training data) remains challenging for VLAs but is an active research frontier. **OK-Robot** [152] combines a VLM for object detection with a pre-trained manipulation primitive to achieve zero-shot pick-andplace in novel environments. While not a full VLA, OK-Robot demonstrates the potential of VLM-based perception for zero-shot manipulation. 

**Robot Utility Models** [153] train VLAs as general-purpose “utilities” that can perform a broad range of manipulation tasks from language instructions, approaching zero-shot capability for common manipulation primitives. The remaining gap to true zero-shot bimanual manipulation is substantial, as bimanual coordination patterns are difficult to infer from language alone without motor experience. 

A limitation of current cross-embodiment claims is that transfer is evaluated after fine-tuning without controlling for data quantity; rigorous ablations separating pre-training benefit from fine-tuning benefit are needed. 

Table 11 summarizes the generalization capabilities observed across VLA methods, distinguishing between environment, object, instruction, and embodiment generalization. 

Tables 11 and 12 summarize the generalization and language grounding landscape across VLA methods. Language and cross-embodiment capabilities do not exist in isolation; they interact with visual representations, safety requirements, and deployment constraints, which we address in Section 11. 

**Table 11.** Generalization capabilities of VLA models across four dimensions. Strong/Partial/Weak indicate the degree of demonstrated generalization. 

|**Method**|**Env.**|**Obj.**|**Instr.**|**Embod.**|
|---|---|---|---|---|
|**RT-1** [59]|Weak|Weak|Weak|–|
|**RT-2**[1]|Partial|Strong|Strong|–|
|**OpenVLA**[5]|Partial|Partial|Partial|Partial|
|**Octo**[6]|Partial|Partial|Partial|Strong|
|_π_0[2]|Partial|Strong|Strong|Partial|
|_π_0.5[3]|Strong|Strong|Strong|Partial|
|**Hi Robot**[29]|Partial|Partial|Strong|–|


**Table 12.** Comparison of language grounding and reasoning capabilities in VLA models. Novel instr. indicates generalization to unseen instruction phrasings. Novel obj. indicates generalization to unseen object categories. 

|**Method**|**Hierarchical**|**Novel Instr.**|**Novel Obj.**|**Open-Ended**|**Cross-Embod.**|**Zero-Shot**|
|---|---|---|---|---|---|---|
|**RT-1** [59]|–|Limited|Limited|–|–|–|
|**RT-2**[1]|–|✓|✓|Partial|–|Partial|
|**OpenVLA**[5]|–|✓|✓|–|✓|–|
|_π_0[2]|–|✓|✓|–|✓|–|
|_π_0.5[3]|✓|✓|✓|✓|✓|Partial|
|**Hi Robot**[29]|✓|✓|✓|✓|–|–|
|**SayCan**[109]|✓|✓|–|✓|–|–|


https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

38 of 59 

# **11. Cross-Cutting Concerns** 

Several concerns cut across all VLA architectures and application domains. This section addresses visual representation learning, world models and future state prediction, safety, sim-to-real transfer, and human–robot interaction. Table 13 compares these capabilities across representative VLA methods. 

**Table 13.** Cross-cutting capabilities of VLA models. Multi-view indicates support for multiple camera inputs. Safety indicates explicit safety mechanisms. Sim-to-Real indicates simulation-to-real transfer capability. 

|**Method**|**Visual Encoder**|**Multi-View**|**Safety**|**Sim-to-Real**|**HRI**|**Proprioception**|
|---|---|---|---|---|---|---|
|**RT-1** [59]|EfficientNet|–|Basic|–|–|–|
|**RT-2**[1]|ViT (PaLI-X)|–|Basic|–|Partial|–|
|**OpenVLA**[5]|DINOv2 + SigLIP|–|–|–|–|–|
|_π_0[2]|SigLIP|✓|Rate limit|–|–|✓|
|_π_0.5[3]|SigLIP|✓|Multi-layer|–|✓|✓|
|_π_<sup>_∗_</sup><br>0 <sup>[4]</sup>|SigLIP|✓|Rate limit|–|–|✓|
|**RDT-1B**[44]|SigLIP|✓|Basic|–|–|✓|
|**Octo**[6]|Custom ViT|✓|–|✓|–|–|


## _11.1. Visual Representation Learning_ 

The choice of visual encoder significantly impacts VLA performance. Three approaches dominate. 

**Pre-trained VLM encoders** (e.g., SigLIP in PaLIGemma [25], ViT in CLIP [21]) provide rich semantic features pre-trained on web-scale data. These encoders excel at object recognition and scene understanding but may lack fine-grained spatial information needed for precise manipulation. Spatial structure may be as important as semantic richness for manipulation-oriented visual encoders: **Transporter Networks** [154] achieve strong rearrangement performance using equivariant spatial representations learned without large-scale pre-training. 

**Robot-specific visual representations** offer an alternative to generic VLM encoders. **R3M** [155], pre-trained on robot video data using time-contrastive and language-aligned objectives, captures temporal dynamics and manipulation-relevant features that generic encoders miss. Offline data paired with crowd-sourced annotation also yields transferable representations [156]. A large-scale comparison by **Cortex** [157] found that representations trained on diverse egocentric video outperform those from static image classification, while **SPA** [158] adds explicit 3D spatial-awareness to improve embodied policy learning. Several VLAs use R3M or similar robot-specific encoders alongside VLM encoders, processing images through both pathways. 

**Multi-view fusion** is critical for bimanual manipulation, where a single camera may not capture both arms and the workspace simultaneously. Most bimanual VLAs ( _π_ 0 [2], **RDT-1B** [44]) use multiple camera views (typically a wrist camera on each arm plus one or more third-person cameras) and fuse the resulting tokens within the Transformer backbone. 

Multi-view fusion approaches range from early concatenation ( _π_ 0 [2], **Octo** [6]) to late fusion and learned view selection. Wrist cameras are indispensable for bimanual setups, capturing fine-grained contact information that third-person cameras miss. Multiframe visual context [74,76,114] extends temporal scope beyond the current observation. A limitation across all three approaches is that no principled method exists for selecting which visual encoder or fusion strategy best suits a given task; current practice relies on empirical trial-and-error, and the relative contribution of semantic versus spatial features to bimanual coordination remains poorly understood. 

**Fine-tuning versus training from scratch.** As Table 3 (Init. column) shows, nearly all modern VLAs fine-tune pre-trained visual encoders rather than training from scratch, 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

39 of 59 

because web-scale pre-training produces representations impractical to learn from robot data alone. Most systems freeze or lightly fine-tune the encoder and allocate training budget to the action head; for example, _π_ 0 [2] fine-tunes SigLIP weights with a reduced learning rate, while **RT-1** [59] adapts an ImageNet-pretrained EfficientNet-B3 via FiLM conditioning on 130K demonstrations. A notable exception is **Octo** [6], which trains from scratch on 800K episodes without any pre-trained encoder. The optimal balance between frozen and updated parameters remains an open question that depends on the available robot data and the domain gap. 

## _11.2. Safety_ 

Safety is paramount for bimanual systems operating near humans. VLA safety concerns include: 

**Action bounds and rate limiting** : VLA outputs are typically clipped to safe action ranges and rate-limited to prevent high-velocity motions. Two-arm coordination introduces an additional collision-avoidance constraint between the arms that is not inherently captured by the VLA. 

**Out-of-distribution detection** : Some VLAs use confidence-based filtering, halting when action head uncertainty (estimated from denoising variance or velocity field norms) exceeds a threshold. 

**Collision avoidance** : Bimanual systems face self-collision risk between arms. Post hoc safety layers that project actions to collision-free trajectories add latency but provide guarantees; learning collision avoidance from demonstrations is an alternative that may not generalize to novel configurations. 

**Human-in-the-loop correction** : For deployment in homes (e.g., _π_ 0.5 [3]), the ability for humans to intervene and correct the robot is essential. VLAs that accept real-time language feedback can be redirected mid-task, providing a natural correction mechanism. 

## _11.3. Sim-to-Real Transfer_ 

Simulation provides scalable, safe data generation, but the reality gap (differences between simulated and real visual appearances, physics, and dynamics) limits direct transfer. 

**SIMPLER** [48] provides simulation environments calibrated to match real-world VLA evaluation setups, so that VLAs can be evaluated without physical hardware. The correlation between simulated and real-world success rates validates simulation as a development tool for VLAs. 

The reality gap is acute for bimanual manipulation because contact dynamics (friction, deformation, compliance) are difficult to simulate accurately. Current bimanual VLAs ( _π_ 0 [2], _π_ 0<sup>_∗_[4]) rely primarily on real-world demonstrations and practice, with simulation</sup> playing a secondary role. 

Strategies for closing this gap include **domain randomization** (varying visual and physical parameters), **system identification** (calibrating simulation to match the real robot), and generative approaches such as **Gen2Act** [159] (human video demonstrations) and **Track2Act** [160] (point tracks from internet videos). **Hybrid training** (simulation pretraining plus real fine-tuning) works well for single-arm VLAs but remains underexplored for bimanual systems, where higher action dimensionality makes sim-to-real alignment harder. 

## _11.4. World Models and Future State Prediction_ 

A complementary approach to reactive VLA policies is to equip robots with _world models_ that predict future states, whether as visual frames, latent representations, or explicit physical quantities, before committing to actions. This “predict-then-act” approach offers several advantages for bimanual manipulation: it allows look-ahead planning for multi-step 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

40 of 59 

coordination, provides a mechanism for evaluating action consequences before execution, and can generate synthetic training data to alleviate the data scarcity problem. 

The GigaBrain family illustrates the rapid maturation of world model-powered VLAs. **GigaBrain-0** [77] first used generative models to produce synthetic robot data. Its successor, **GigaBrain-0.5M**<sup>_∗_</sup> [53], added RAMP (RL via World Model-conditioned Policy), yielding _∼_ 30% improvement on bimanual tasks. **GigaWorld-0** [80] completes the picture with a unified framework combining video generation and 3D modeling (Gaussian Splatting) as a scalable data engine. 

A more radical approach formulates control as video generation. **Rhoda AI (DVA)** [78] uses a causal video model pre-trained on web-scale video, with an inverse dynamics model translating predicted frames to actions (10–20 h of robot data). **VPP** [161] learns implicit inverse dynamics via video diffusion (+18.6% on Calvin ABC-D). **ViPRA** [162] learns from actionless videos at 22 Hz, and **Mimic-Video** [163] achieves 10 _×_ sample efficiency over standard VLAs. 

Other approaches operate on optical flow and latent representations. **FOFPred** [164] achieves 68.6% on bimanual tasks via language-driven flow prediction. **V-JEPA 2** [165] provides a self-supervised world model (1M+ hours of video; 65–80% zero-shot success). **WorldVLA** [79] jointly generates actions and future frames, **UP-VLA** [166] uses next-frame prediction for implicit physics, and **NVIDIA Cosmos** [167] provides open world foundation models trained on 20M+ h of data. 

The predict-then-act approach offers four advantages: _data efficiency_ (DVA requires only 10–20 h of robot data; Mimic-Video achieves 10 _×_ sample efficiency), _interpretability_ (predicted frames can be visualized), _planning_ (look-ahead evaluation before committing), and _synthetic data generation_ (GigaWorld-0 and Cosmos produce unlimited training data). 

However, fundamental limitations remain. _Prediction accuracy degrades_ as compounding errors in autoregressive video generation make long-horizon forecasts unreliable, especially for contact-rich bimanual tasks with rapid state changes. _Inverse dynamics accuracy_ suffers from the additional error of translating predicted video back to precise actions. _Computational cost_ conflicts with real-time control budgets (ViPRA runs at only 22 Hz). Video models can _hallucinate_ plausible but incorrect states after occlusions, and current world models lack _haptic grounding_ for force and tactile signals. 

## _11.5. Human–Robot Interaction_ 

VLAs facilitate more natural human–robot interaction through language. A user can instruct a bimanual robot in natural language, observe its behavior, and provide corrections or new instructions in real time. 

The most complete HRI demonstration to date comes from _π_ 0.5 [3], where users gave verbal instructions to a bimanual robot in home environments, the robot executed them, and users could redirect it as needed. The hierarchical architecture allows the robot to ask clarifying questions through the high-level VLM when instructions are ambiguous. 

**PaLM-E** [24] and **PIVOT** [168] show that VLMs can engage in dialogue about the physical world and elicit actionable knowledge through visual prompting. However, HRI evaluation for VLAs remains qualitative; no standardized metrics exist for interaction quality or correction latency in VLA-based bimanual systems. 

## _11.6. Scalability and Deployment_ 

Deploying VLAs on bimanual systems in real-world settings introduces engineering challenges beyond model performance. **Compute requirements** are substantial: a 3Bparameter VLA running flow matching with _K_ = 10 steps requires a high-end GPU (A100 or equivalent) for real-time bimanual control. Edge deployment on embedded GPUs is 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

41 of 59 

not yet practical for full-size VLAs, motivating the efficient architectures discussed in Section 5.4. 

**Communication latency** between the VLA compute server and the robot controller adds to the end-to-end control delay. With dual-arm systems running at 50 Hz, the total loop delay (image capture, network transfer, VLA inference, action transfer, motor execution) must remain below 20 ms per step. Action chunking mitigates this by amortizing the VLA inference over _H_ steps but introduces a minimum reaction latency of one chunk period. 

A gap remains between research demonstrations and reliable deployment: most results use controlled laboratory conditions, and long-term reliability metrics are absent. Reproducibility is limited by leading systems’ reliance on proprietary data. **Xiaomi-Robotics-0** [150] represents industrial VLA deployment with custom hardware accelerators for low-latency bimanual control. **TidyBot** [169] demonstrates LLM-powered household robotics, and **ManiWAV** [170] shows that auditory feedback complements vision for contact-rich tasks. 

Figure 9 summarizes the complete VLA training and deployment pipeline that ties together the architectural choices (Section 5), training recipes (Section 6), and deployment considerations discussed above. The interplay among these architectural, training, and deployment considerations shapes the current state of the art, which we synthesize next. 


**Figure 9.** The VLA training and deployment pipeline for bimanual manipulation. Training proceeds through four phases: VLM pre-training on web data, robot pre-training on cross-embodiment datasets, task fine-tuning on bimanual demonstrations, and optional reinforcement learning from autonomous practice. The RL phase creates a self-improvement loop where the deployed policy generates additional training data. 

# **12. Discussion and Conclusions** 

## _12.1. State-of-the-Art Performance_ 

Synthesizing the results presented across Sections 5–11, in our assessment, the state of the art in VLA-based bimanual manipulation and unmanned aerial robotics can be characterized along several dimensions. Figure 10 charts the rapid progress from 2023 to 2025: bimanual folding success rose from _∼_ 30% (ACT) to over 90% ( _π_ 0<sup>_∗_), narrowing the</sup> gap with single-arm performance. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

42 of 59 


**Figure 10.** Approximate evolution of VLA performance on bimanual manipulation tasks (2023– 2025). Values are approximate trend values synthesized by the authors from reported results across different evaluation setups and task definitions; they illustrate general trends rather than exact comparable benchmarks. Bimanual task success rates have improved dramatically, from _∼_ 30% with early methods such as ACT [16] to _>_ 90% with _π_ 0<sup>_∗_[4].The gap between bimanual and single-arm</sup> performance has narrowed but persists for the most dexterous tasks. 

**Architecture.** As reflected in Tables 4 and 8, flow-based VLAs, led by _π_ 0 [2] and its successors _π_ 0.5 [3] and _π_ 0<sup>_∗_[4], currently achieve the strongest bimanual manipulation</sup> performance. The flow-matching action head generates smooth, high-dimensional action chunks without quantization, and the iterative denoising process captures the multi-modal coordination patterns inherent in bimanual tasks. Diffusion-based models, particularly **RDT-1B** [44], demonstrate that scale improves performance but trail flow-based approaches in inference efficiency. Autoregressive VLAs ( **OpenVLA** [5], **RT-2** [1]) provide the simplest integration with VLM pre-training but are limited by discretization for bimanual action spaces. 

**Training.** The three-stage recipe (VLM initialization, cross-embodiment pre-training, task-specific fine-tuning) is now standard. The addition of reinforcement learning from autonomous practice ( **RECAP** [4]) represents the most impactful recent advance; it allows VLAs to surpass demonstration quality by 10–40% on bimanual tasks. Co-training with diverse data during fine-tuning consistently improves performance and robustness. 

**Action representation.** Action chunking with _H_ = 50 steps is the dominant choice for bimanual VLAs, providing the temporal coherence needed for coordinated two-arm motions. Learned action tokenization ( **FAST** [8]) narrows the gap between autoregressive and continuous approaches. Real-time execution techniques ( **RTC** [103]) enable reactive bimanual control despite the computational cost of large VLA models. 

**Generalization.** Hierarchical VLAs ( _π_ 0.5 [3], **Hi Robot** [29]) demonstrate the strongest generalization to novel environments and open-ended instructions. Cross-embodiment pre-training on OXE data provides a foundation for transfer, though bimanual-specific skills require task-specific fine-tuning. 

**Efficiency.** The computational cost of VLA inference remains a concern for bimanual real-time control. Table 14 summarizes the efficiency characteristics of representative methods. Flow-based models with _K_ = 10 denoising steps achieve the best latency–quality tradeoff, while efficient architectures ( **TinyVLA** [7], **MiniVLA** [73]) sacrifice some capability for deployment on resource-constrained hardware. 

**Memory.** Memory-augmented VLAs represent the most significant recent advance for long-horizon bimanual tasks. **MEM** [74], integrated into the _π_ 0.6 VLA, enables tasks spanning up to 15 min by combining video-based short-horizon memory with languagebased long-horizon memory. Concurrent approaches [75,76,117] explore complementary 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

43 of 59 

designs, from perceptual–cognitive memory banks to amortized multi-frame context. The common finding is that different time scales demand different memory representations. 

**World Models.** World model-powered VLAs [53,77] and direct video-action models [78,161] represent a shift from purely reactive policies to predictive ones. The GigaBrain family demonstrated that world model-generated data improves bimanual task performance by _∼_ 30%, and web-scale video pre-training transfers to robot control with 10–20 h of task-specific data. However, none of these approaches have been evaluated on standardized bimanual benchmarks, limiting direct comparison. 

**Unmanned Aerial Robotics.** VLA adoption for drones lags manipulation by _∼_ 2 years. Strong individual components exist (RL flight policies [132], VLN benchmarks [124], LLMbased planning [125]), but integrated end-to-end VLA systems for physical drones remain rare. The architectural innovations proven for bimanual manipulation are directly applicable (see directions 11–13 below). 

**Industrial VLA Deployment.** The transition from research to product-level systems has accelerated in 2025–2026, with several companies deploying VLA-based robots commercially (Table 15). Three architectural patterns have emerged from the industry that differ from the research approach. 

First, _dual-system (S1/S2) architectures_ separate slow reasoning from fast action. **Gemini Robotics** [171] runs a distilled VLM in the cloud ( _<_ 160 ms query latency) paired with a local action decoder achieving 50 Hz control and more than doubles performance on a broad generalization benchmark compared to other VLAs. **GR00T N1** [172] pairs a 1.34Bparameter VLM (System 2, 10 Hz) with a diffusion Transformer action head (System 1, 120 Hz). **Helix** [173] from Figure AI uses a 7B VLM at 7 Hz and an 80M-parameter action model at 200 Hz, controlling 35 degrees of freedom on embedded GPUs without cloud dependency. This pattern resolves the latency–capability tradeoff that limits monolithic VLAs (Direction 3). 

Second, _video-as-action models_ bypass direct action regression entirely. **Rhoda AI** ’s DVA [78] pre-trains a causal video model on web-scale video, predicts future frames conditioned on the current scene, and extracts actions via a learned inverse dynamics model. **1X Technologies** [174] takes a similar approach with a 14B-parameter text-conditioned diffusion world model trained on 900 h of egocentric human video plus 70 h of robot data. Both systems achieve one-shot or few-shot task adaptation from human demonstrations injected into the context window, without retraining. Third, _continuous autonomous improvement_ has reached production scale. **Dyna Robotics** [175] deploys a dual-arm foundation model (DYNA-1) with a proprietary reward model that enables self-supervised error recovery. DYNA-1 reports a 99.4% success rate over 24+ h of continuous autonomous operation in commercial settings. This validates the RECAP paradigm (Section 6.3) at industrial scale. We note that industrial performance figures are self-reported under company-defined conditions and await independent replication. 

Novel data collection strategies are also emerging. **Sunday Robotics** [176], founded by the creators of ALOHA [16] and Diffusion Policy [40], trains its ACT-1 foundation model on _zero robot data_ , using low-cost Skill Capture Gloves to collect human demonstration episodes across diverse homes, with a learned Skill Transform layer adapting human kinematics to robot morphology. Specific scale figures (glove cost, episode counts, number of homes) are based on company announcements subsequent to the initial publication and should be treated as projected targets. **Covariant** ’s RFM-1 [177], an 8B-parameter autoregressive world model trained on millions of real deployment interactions, was designed to extend Covariant’s legacy fleet (which achieved 99%+ warehouse picking precision across hundreds of sites) with generalized reasoning capabilities; RFM-1 itself has not been independently deployed at that scale. **AgiBot World** [122] contributes 1M+ 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

44 of 59 

real robot trajectories across 217 tasks, with its GO-1 generalist policy outperforming Open X-Embodiment baselines by 30%. 

Hardware-focused companies are also integrating VLA-class models. **Boston Dynamics** and Toyota Research Institute jointly developed a Large Behavior Model (LBM) [178] for the Atlas humanoid that controls the entire robot (hands and feet) through a single whole-body policy for packing, sorting, and organizing tasks. Atlas fleets are scheduled to ship to Hyundai and Google DeepMind in 2026, with Google’s Gemini Robotics [171] being integrated for enhanced cognitive capabilities. 

Open-source efforts from **NVIDIA** [172] (GR00T N1 weights and training data), **Xiaomi** [150] (Xiaomi-Robotics-0, LIBERO SOTA at 98.7%), and **AgiBot** [122] are accelerating community progress. Figure 11 shows representative systems from this industrial wave. 


**Figure 11.** Industrial VLA-powered humanoid robot systems. ( **a** , top left) Boston Dynamics Atlas with TRI Large Behavior Model performing warehouse manipulation. Reprinted with permission from Ref. [178]. Copyright 2025, Boston Dynamics and Toyota Research Institute. ( **b** , top right) Unitree humanoid executing dynamic whole-body control (image courtesy of Unitree Robotics). ( **c** , bottom left) Tesla Optimus humanoid with dexterous hands for general-purpose manipulation. Reprinted with permission from Ref. [179]. Copyright 2025, Tesla AI. ( **d** , bottom right) Google DeepMind Gemini Robotics, which integrates actions as a native Gemini modality for dexterous manipulation and general-purpose robot control. Reprinted with permission from Ref. [171]. Copyright 2025, Google DeepMind. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

45 of 59 

**Table 14.** Efficiency comparison of VLA models for bimanual deployment. GPU indicates the minimum GPU for real-time control. 

|**Method**|**Params**|**Latency**|**Min. GPU**|
|---|---|---|---|
|**RT-2** [1]|55B|_∼_1 s|TPU v4|
|**OpenVLA**[5]|7B|_∼_150 ms|A100|
|_π_0[2]|3B|_∼_70 ms|A100|
|**RDT-1B**[44]|1.2B|_∼_150 ms|A6000|
|**TinyVLA**[7]|1B|_∼_40 ms|RTX 4090|
|**MiniVLA**[73]|300M|_∼_25 ms|RTX 3090|
|**FAST**[8]|7B|_∼_80 ms|A100|


**Table 15.** Industrial VLA systems (2024–2026). Architecture indicates the action generation approach. Deployment column indicates the current operational status. Success rates are self-reported under company-defined conditions. 

|**System**|**Organization**|**Architecture**|**Key Innovation**|**Deployment**|**Year**|
|---|---|---|---|---|---|
|_Dual-System (S1/S2) Archit_<br>|_ectures_<br>|||||
|Gemini Robotics [171]|Google DeepMind|VLM + action decoder|Actions as native Gemini modality|Partner testing|2025|
|GR00T N1 [172]|<br>NVIDIA|VLM (10 Hz) + DiT (120 Hz)|<br>Open-source; neural trajectory augment.|<br>Research|2025|
|Helix [173]|Figure AI|VLM (7 Hz) + action (200 Hz)|<br>35-DOF on embedded GPU|BMW partnership|2025|
|_Video-as-Action / World Mo_|_dels_|||||
|DVA [78]<br>1XWM [174]|Rhoda AI<br>1X Technologies|Causal video_→_inv. dynamics<br>Diffusion WM_→_IDM|Web-scale video pre-training<br>900 h human video + 70 h robot|Industrial pilots<br>Development|2026<br>2026|
|RFM-1 [177]|<br>Covariant|8B AR world model|Generalized reasoning from fleet data|Development|2024|
|_Continuous Autonomous Im_|_provement_|||||
|<br>DYNA-1 [175]|<br>Dyna Robotics|FM + proprietary RM|99.4% success, 24 h autonomy|Commercial sites|2025|
|_π_<sup>_∗_</sup><br>0 <sup>[4]</sup>|<br>Physical Intelligence|<br>FM + RECAP (RL)|<br>10–40% over demo baseline|Research|2025|
|_Novel Data Collection_||||||
|ACT-1 [176]<br>AgiBot World [122]|Sunday Robotics<br>AgiBot|Zero robot data; glove demos<br>Latent action repr.|Human demos via gloves (scale TBD)<br>1M+ trajectories; 30% over OXE|Beta 2026<br>Shipping at scale|2026<br>2025|
|_Open-Source VLAs_||||||
|<br>Xiaomi-Robotics-0 [150]|Xiaomi|MoT + DiT (4.7B)|LIBERO 98.7% SOTA|Open-source|2025|
|GR00T N1 [172]|NVIDIA|VLM + DiT (2.2B)|Weights + data released|Open-source|2025|


The field has also converged on several **long-standing challenges** that remain open despite recent progress: 

- **Distribution shift** : VLA policies still degrade when encountering out-of-distribution observations, especially for bimanual tasks where object configurations have high variability. 

- **Contact modeling** : precise force control during bimanual contact is not addressed by current position-space VLAs. 

- **Evaluation standardization** : the lack of common bimanual benchmarks prevents fair comparison across methods. 

- **Data scarcity** : high-quality bimanual demonstrations remain expensive to collect, limiting the scale of bimanual VLA training. 

- **Temporal credit assignment** : for long-horizon bimanual tasks, determining which actions contributed to success or failure is difficult, hindering RL-based improvement. 

## _12.2. Summary and Discussion_ 

We organize our conclusions into fourteen findings, grouped thematically: (1)–(3) cover core VLA design choices, (4)–(6) cover training and data strategies, (7)–(8) identify current limitations, (9)–(10) describe emergent capabilities, and (11)–(14) address crossdomain transfer and deployment. Each finding states a conclusion from the evidence reviewed, followed by its implications. 

In our view, the analysis yields the following key findings: 

**(1) Flow matching is the current best action generation mechanism for bimanual VLAs.** We find that the combination of continuous action generation, efficient sampling 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

46 of 59 

( _K_ = 10 steps), and long action chunks makes flow matching uniquely suited to the highdimensional, temporally correlated action spaces of bimanual manipulation. Diffusion models offer similar expressiveness but at higher computational cost. 

**(2) VLM pre-training provides critical semantic grounding for bimanual tasks.** In our analysis, VLAs that inherit web-scale knowledge from VLM backbones consistently outperform architectures trained from scratch on robot data alone. The VLM’s understanding of objects, spatial relationships, and task semantics transfers directly to manipulation, reducing the amount of robot-specific data needed. 

**(3) Action chunking is essential for bimanual coordination.** We observe that singlestep action prediction cannot capture the coordinated motion patterns of two arms working in concert. Chunks of _H_ = 50 steps at 50 Hz (1 s of motion) provide sufficient temporal context for most bimanual primitives, including folding, handovers, and assembly. 

**(4) Reinforcement learning from autonomous practice is, in our assessment, the single most impactful recent advance for bimanual VLAs.** RECAP [4] showed that VLAs can self-improve by practicing autonomously and learning from success/failure signals. This matters especially for bimanual tasks where demonstration data is expensive to collect and expert performance is difficult to achieve via teleoperation. 

**(5) Hierarchical architectures enable long-horizon bimanual tasks.** We find that flat VLA policies struggle with tasks requiring more than a few steps of bimanual coordination. Hierarchical decomposition (high-level VLM reasoning plus low-level VLA execution) extends the effective planning horizon from seconds to minutes. 

**(6) Data diversity matters more than data quantity for generalization, but at the cost of per-task precision.** VLAs pre-trained on diverse cross-embodiment data generalize better than those trained on larger quantities of homogeneous data. However, _π_ 0 [2] pretrains on hundreds of tasks yet still requires 50–200 task-specific demonstrations for strong bimanual performance, and **RT-1** [59] achieved 97% on seen tasks but only 76% on unseen ones. A two-stage recipe has thus become standard: broad pre-training for coverage, then narrow fine-tuning for precision. 

**(7) The latency–reactivity tradeoff remains a fundamental challenge.** We note that large VLA models incur significant inference latency, conflicting with the need for reactive bimanual control. A 3B-parameter flow-based VLA requires _∼_ 12 GB of GPU VRAM and an A100-class GPU for real-time inference; edge deployment on embedded GPUs (Jetson-class) is not yet practical at this scale. Techniques such as RTC [103], TinyVLA [7], and FAST [8] mitigate inference latency but do not fully resolve it. 

**(8) Bimanual benchmarks are insufficient.** We consider this the most pressing infrastructure gap in the field. Most VLA evaluation occurs on single-arm tasks or bespoke bimanual setups that vary across papers. Without standardized bimanual benchmarks, comparing methods fairly and tracking progress systematically is not possible. 

**(9) Pre-training on web data transfers to bimanual tasks.** We observe that the semantic knowledge encoded in VLM backbones (object affordances, material properties, spatial reasoning) directly benefits bimanual manipulation, even though web data contains no robot actions. This transfer is most evident in language grounding (understanding what “fold” or “stack” means) and visual scene understanding (identifying object parts and configurations). 

**(10) Bimanual coordination emerges from joint prediction.** We find this result surprising: VLAs that predict both arms’ actions jointly in a single action chunk learn coordination patterns implicitly from data, without explicit coordination mechanisms. This emergent coordination is strongest with flow-based and diffusion-based models that generate the full bimanual action in a single denoising process. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

47 of 59 

**(11) VLA architectures are cross-embodiment, with aerial applications lagging by** _∼_ **2 years.** We observe that the same VLM backbones, action generation mechanisms, and training recipes that power bimanual manipulation are being adapted for unmanned aerial robotics. As of early 2026, the aerial VLA field is at the stage manipulation reached in 2022–2023: strong individual components exist but integrated end-to-end systems remain nascent. High-fidelity simulators, accessible hardware, and cross-embodiment pre-training provide the ingredients for rapid convergence. 

**(12) Dual-system architectures are the industry consensus for product-level VLAs.** We find that Google (Gemini Robotics [171]), NVIDIA (GR00T N1 [172]), and Figure AI (Helix [173]) all independently converged on separating a slow reasoning module ( _≤_ 10 Hz) from a fast action module ( _≥_ 100 Hz). This pattern resolves the latency–capability tradeoff that monolithic VLAs face: the reasoning module provides semantic understanding and task decomposition, while the action module generates smooth, high-frequency motor commands. Research VLAs that adopt this pattern will be better positioned for deployment. 

**(13) Production reliability requires continuous self-improvement, not just better demonstrations.** In our view, the most reliable deployed systems, Dyna’s DYNA-1 [175] (99.4% over 24 h) and Covariant’s RFM-1 [177] (99%+ precision), achieve their performance through continuous RL loops where every deployment interaction feeds back into training, not through larger demonstration datasets alone. This validates the RECAP approach [4] at industrial scale and suggests that the path to product-level VLAs runs through autonomous improvement infrastructure. 

**(14) Video prediction is gaining traction as an alternative to direct action regression.** We note that Rhoda AI’s FutureVision [78] and 1X Technologies’ world model [174] generate future video frames first and extract actions via inverse dynamics, exploiting web-scale video pre-training that contains orders of magnitude more data than robot demonstration datasets. This approach allows one-shot task adaptation from human demonstrations without retraining, though inference latency and physics fidelity remain open challenges. 

These findings point to a converging design pattern: a pre-trained VLM backbone for semantic grounding, paired with a continuous (preferably flow-based) action head that generates multi-dimensional action chunks. Training follows a two-stage recipe— diverse pre-training then task-specific fine-tuning—increasingly augmented by RL from autonomous practice. The same pattern appears in both bimanual manipulation and aerial robotics, supporting the view that VLAs generalize across embodiments. 

Translating this pattern into deployed systems, however, requires addressing practical constraints that cut across all findings: environmental variability degrades laboratorytrained policies, communication latency between GPU servers and robot controllers adds to the control loop, long-term reliability over hours of operation remains undemonstrated, and the energy cost of continuous GPU inference presents barriers to fleet-level scaling. The most pressing open questions are scalable evaluation (Finding 8), the diversity–precision tradeoff (Finding 6), and the gap between research prototypes and production systems with sustained reliability (Findings 12–13). 

## _12.3. Research Directions_ 

Despite rapid progress, several fundamental challenges remain. We consider the following research directions most pressing: 

**(1) Standardized Bimanual Benchmarks:** The field urgently needs standardized simulation and real-world benchmarks for bimanual manipulation, analogous to LIBERO for single-arm tasks. Such benchmarks should cover the full spectrum of coordination types (independent, loosely coupled, tightly coupled), object categories (rigid, articulated, 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

48 of 59 

deformable), and task horizons (single-step to multi-minute). Without standardized evaluation, comparing bimanual VLA methods remains unreliable. 

**(2) Dexterous, Force-Aware, and Multi-Modal Manipulation:** Current VLA systems use parallel-jaw grippers and rely solely on visual observations, limiting both dexterity and contact awareness. Extending VLAs to multi-fingered hands would unlock tasks such as in-hand reorientation, but the action space (two 16-DOF hands plus two 7-DOF arms) exceeds 40 dimensions per step, posing extreme challenges for action generation. Simultaneously, incorporating force/torque feedback and tactile sensing (e.g., GelSight) into VLA observations is essential for contact-rich tasks such as tightening screws, snapping parts, and kneading dough. Auditory signals can further complement vision for detecting task-relevant events such as clicks and snaps. Jointly addressing dexterity, force awareness, and multi-modal sensing is necessary to move bimanual VLAs beyond the current pickand-place regime. 

**(3) Real-Time Reactive Control:** Despite advances in RTC [103] and efficient architectures [7], attaining truly reactive bimanual control ( _>_ 100 Hz) with large VLA models remains difficult. Research into model compression, speculative decoding for action generation, and hardware–software co-design could close this gap. 

**(4) Data-Efficient Learning and Sim-to-Real Transfer:** Collecting bimanual demonstrations is expensive, and few-shot adaptation (fewer than 10 demonstrations) would reduce deployment costs. Cross-embodiment pre-training already provides strong priors; combining it with meta-learning, in-context learning, or skill composition could yield practical few-shot bimanual adaptation. Complementarily, simulation could provide unlimited training data, but the reality gap is severe for contact-rich bimanual tasks involving deformable objects. Advances in differentiable simulation, domain randomization tailored to bimanual contact, and sim-to-real fine-tuning are needed to unlock simulation as a primary data source. 

**(5) Compositional Bimanual Skills:** Rather than learning each bimanual task from scratch, VLAs could learn a library of composable bimanual primitives (grasp, hold, fold, insert, handover) and combine them to perform novel tasks specified via language. Skill composition would improve generalization to unseen task combinations. 

**(6) Safety-Certified, Interpretable, and Trustworthy Bimanual VLAs:** Deploying bimanual VLAs in human environments requires formal safety guarantees. Research into runtime monitoring, safety-constrained action generation, and provable collision avoidance between arms and with humans is essential. We believe this will become the primary bottleneck for commercial deployment, as current heuristic safety measures (rate limiting, action clipping) are insufficient for human-proximate operation. Closely tied to safety is the need for _interpretability and trustworthiness_ : present-day VLAs largely operate as black boxes, making it difficult to attribute a chosen action to the underlying language command, visual input, or proprioceptive state. Integrating Explainable AI (XAI) techniques—for example, modality-attribution and attention-visualization methods that quantify the influence of the language instruction versus the visual scene on the predicted action chunk—would facilitate error analysis, support safety assurance, and improve user trust, all of which are prerequisites for human-proximate certification. 

**(7) Autonomous Improvement and World Models:** RECAP [4] demonstrated that VLAs can self-improve from autonomous practice, but the current approach requires human-designed task distributions and VLM-based reward signals that may not generalize. Integrating world models [53] that predict the consequences of bimanual actions, including object deformation and contact transitions, could enable look-ahead planning and more effective autonomous practice. The long-term goal is fully autonomous self- 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

49 of 59 

improvement where the VLA discovers new tasks, practices them, and improves without human oversight. 

**(8) Human–Robot Collaborative Manipulation:** The ultimate bimanual system may involve one robot arm and one human arm working together. VLAs could learn to coordinate with a human partner, predicting human intentions and adapting robot actions accordingly. This requires advances in human motion prediction, shared autonomy, and real-time VLA adaptation. 

**(9) Memory-Augmented VLAs for Long-Horizon Autonomy:** MEM [74] and concurrent work [75,76,114–118] show that multi-scale memory improves performance on tasks spanning minutes. Key open challenges include scaling beyond single episodes to persistent deployment, learning what to remember versus forget, multi-modal memory grounding, and avoiding causal confusion. Persistent memory could enable continual learning across deployment sessions. 

**(10) World Models for Bimanual Planning:** World models that predict future states [77, 78,80,164,165] could enable look-ahead planning for contact-rich bimanual sequences. The GigaBrain family [53,77] improved bimanual task performance by _∼_ 30% via world modelgenerated data, and video-action models [78,161,163] transfer web-scale video pre-training to robot control. Key challenges include predicting joint consequences of two coordinated arms on deformable objects and integrating predictions with real-time control. Unifying world models with memory (Direction 9) is promising: short-term prediction plus longterm state tracking. 

**(11) End-to-End VLAs for Drone Control:** Building VLAs that map onboard camera images and language to continuous flight commands for physical drones is the most pressing aerial direction. Key challenges: _≥_ 100 Hz latency requirements, outdoor 3D observation spaces, and the sim-to-real gap for underactuated dynamics. Efficient manipulation VLA architectures (TinyVLA, MiniVLA, FAST) are directly relevant given constrained onboard compute. 

**(12) Multi-Agent Aerial VLAs:** Multi-drone coordination presents a natural extension of the bimanual coordination strategies analyzed in Section 8.1. Centralized VLAs that jointly generate actions for multiple drones face the same dimensional scaling challenges as bimanual joint action spaces, while decentralized approaches require explicit communication protocols. The hierarchical VLA paradigm (high-level VLM planner assigning subgoals to individual drone policies) is especially promising for heterogeneous multi-agent systems that combine aerial and ground robots. 

**(13) Aerial Manipulation with VLAs:** Drones equipped with grippers or robotic arms must simultaneously stabilize flight and execute precise manipulation, combining the challenges of both domains surveyed in this paper. VLA architectures that generate coupled flight-and-grasp action chunks, analogous to bimanual joint action spaces, could enable aerial grasping, payload handover, and contact-based inspection tasks that are currently beyond the reach of separate flight and manipulation controllers. Agriculture is a particularly promising application domain where both manipulation and aerial VLAs converge: dronebased harvesting [180], precision weeding [181], and ground-based robotic harvesters for fruits and vegetables [182] require outdoor visual robustness, deformable-object handling, and coordination between flight and manipulation. HarvestFlex [183] provides an early proof-of-concept, achieving 74% success on in-the-wild strawberry harvesting with a VLA policy trained from only 227 teleoperated episodes, but agricultural VLA adoption remains nascent overall. 

**(14) Bridging the Research-to-Production Gap:** As Table 15 shows, industry has converged on architectural and training patterns that differ from the dominant research approach. Three gaps are most pressing. First, _sustained reliability_ : research VLAs are 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

50 of 59 

evaluated over tens of trials, while production requires 99%+ success over thousands of continuous cycles; Dyna’s DYNA-1 [175] and Covariant’s RFM-1 [177] achieve this through continuous RL self-improvement loops that generate terabytes of training data daily. Second, _dual-system design_ : the S1/S2 separation adopted by Gemini Robotics [171], GR00T N1 [172], and Helix [173] resolves the latency–capability tradeoff, but research on how to optimally partition reasoning and action across the two systems is nascent. Third, _scalable data collection_ : Sunday Robotics’ $200 gloves [176] (10M episodes from 500+ homes), NVIDIA’s neural trajectory augmentation [172] (10 _×_ synthetic data expansion), and 1X’s video-to-action pipeline [174] (900 h of human video) each demonstrate that the demonstration bottleneck can be bypassed, but no unified framework exists. Research that addresses these three gaps (evaluation at production scale, principled S1/S2 co-design, and demonstration-free data scaling) will have the most direct path to real-world impact. 

Table 16 maps each research direction to the VLA components and sections most relevant to its development. 

**Table 16.** Summary of research directions with associated VLA components, current gap severity, and relevant review sections. 

|**#**|**Direction**|**Primary Component**|**Gap Severity**|**Sections**|
|---|---|---|---|---|
|1|Standardized bimanual benchmarks|Evaluation|Critical|Sections4and8|
|2|Dexterous, force-aware, multi-modal manip.|Observation/Action|High|Sections7,8and11|
|3|Real-time reactive control|Architecture/Efficiency|Medium|Sections5and7|
|4|Data-efficient learning & sim-to-real|Training/Data|High|Sections6and11|
|5|Compositional bimanual skills|Architecture/Language|Medium|Sections8and10|
|6|Safety, interpretability & trustworthy VLAs|Deployment/XAI|Critical|Section11|
|7|Autonomous improvement & world models|Training/RL|Medium|Sections5and6|
|8|Human–robot collaboration|HRI|Low|Section11|
|9|Memory-augmented long-horizon VLAs|Architecture/Memory|High|Sections5and8|
|10|World models & future stateprediction|World Model/Planning|High|Sections6and11|
|11|End-to-end VLAs for drone control|Architecture/Aerial|Critical|Sections5and9|
|12|Multi-agent aerial VLAs|Coordination/Aerial|High|Sections8and9|
|13|Aerial manipulation with VLAs|Aerial/Manipulation|High|Sections8and9|
|14|Bridging research-to-production gap|Deployment/Training|Critical|Section12|


VLA models have transformed bimanual manipulation in under three years, progressing from proof-of-concept demonstrations to autonomous household and industrial operation. The cross-embodiment nature of VLAs means that progress in manipulation accelerates unmanned aerial robotics and vice versa, while industry deployment is validating and reshaping research priorities in real time. The fourteen research directions above provide a roadmap for addressing the remaining gaps: standardized evaluation, dexterous force-aware control, memory and world models for long-horizon planning, endto-end drone VLAs, and bridging the widening gap between research benchmarks and production reliability. 

**Author Contributions:** Conceptualization, I.S. and H.S.A.; methodology, I.S.; writing—original draft preparation, I.S.; writing—review and editing, I.S., C.P., H.-M.L., D.N. and H.S.A.; critical review of action representations, real-time latency analysis, and contribution framing, C.P.; critical review of architecture and benchmark tables, efficient models, and future research directions, H.-M.L.; supervision, H.S.A.; funding acquisition, C.P. All authors have read and agreed to the published version of the manuscript. 

**Funding:** This research received no external funding. 

**Data Availability Statement:** Not applicable. This is a review article and no new data was created. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

51 of 59 

**Acknowledgments:** The authors thank the open-source robotics and machine learning communities for making this rapidly evolving field accessible through shared code, models, and datasets. This work was also supported by the Industrial Technology Innovation Program(20023014, Development of an Agricultural Robot Platform Capable of Continuously Harvesting more than 3 Fruits per minute and Controlling Multiple Transport Robots in an Outdoor Orchard Environment) funded by the Ministry of Trade, Industry & Energy(MOTIE, Korea). 

**Conflicts of Interest:** Author Inkyu Sa was employed by Chef Robotics and author Chanoh Park was employed by RovifyLab. The remaining authors declare that the research was conducted in the absence of any commercial or financial relationships that could be construed as a potential conflict of interest. 

# **Abbreviations** 

The following abbreviations are used in this manuscript: 

- VLA Vision–Language–Action model VLM Vision–Language Model BC Behavioral Cloning IL Imitation Learning RL Reinforcement Learning FM Flow Matching ODE Ordinary Differential Equation DOF Degrees of Freedom OXE Open X-Embodiment AR Autoregressive DiT Diffusion Transformer RECAP Reinforcement Learning from Autonomous CAPability RTC Real-Time Chunking TTAC Training-Time Action Conditioning BID Bidirectional Decoding DVA Direct Video Action WM World Model MEM Multi-Scale Embodied Memory UAV Unmanned Aerial Vehicle UGV Unmanned Ground Vehicle VLN Vision–Language Navigation MAV Micro Aerial Vehicle IMU Inertial Measurement Unit 

# **References** 

1. Brohan, A.; Brown, N.; Carbajal, J.; Chebotar, Y.; Chen, X.; Choromanski, K.; Ding, T.; Driess, D.; Dubey, A.; Finn, C.; et al. RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. In _Proceedings of the 7th Conference on Robot Learning (CoRL)_ ; PMLR: Atlanta, GA, USA, 6–9 November 2023; Volume 229, pp. 2165–2183. 

2. Black, K.; Brown, N.; Driess, D.; Esmail, A.; Equi, M.; Finn, C.; Fusai, N.; Groom, L.; Hausman, K.; Ichter, B.; et al. _π_ 0: A Vision-Language-Action Flow Model for General Robot Control. In _Proceedings of Robotics: Science and Systems (RSS)_ , Los Angeles, CA, USA, 21–25 June 2025. 

3. Black, K.; Brown, N.; Darpinian, J.; Dhabalia, K.; Driess, D.; Esmail, A.; Equi, M.; Finn, C.; Fusai, N.; Galliker, M.Y.; et al. _π_ 0.5: A Vision-Language-Action Model with Open-World Generalization. In _Proceedings of the 9th Conference on Robot Learning (CoRL)_ ; PMLR: Seoul, Republic of Korea, 27–30 September 2025; Volume 305, pp. 17–40. 

4. Amin, A.; Aniceto, R.; Balakrishna, A.; Black, K.; Conley, K.; Connors, G.; Darpinian, J.; Dhabalia, K.; DiCarlo, J.; Driess, D.; et al. _π_ 0.6<sup>_∗_:A VLA That Learns From Experience.</sup><sup>_arXiv_</sup><sup>**2025**, arXiv:2511.14759.</sup> 

5. Kim, M.J.; Pertsch, K.; Karamcheti, S.; Xiao, T.; Balakrishna, A.; Nair, S.; Rafailov, R.; Foster, E.; Lam, G.; Sanketi, P.; et al. OpenVLA: An Open-Source Vision-Language-Action Model. In _Proceedings of the 8th Conference on Robot Learning (CoRL)_ ; PMLR: Munich, Germany, 6–9 November 2024; Volume 270, pp. 2679–2713. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

52 of 59 

6. Octo Model Team; Ghosh, D.; Walke, H.; Pertsch, K.; Black, K.; Mees, O.; Dasari, S.; Hejna, J.; Kreiman, T.; Xu, C.; et al. Octo: An Open-Source Generalist Robot Policy. In _Proceedings of Robotics: Science and Systems (RSS)_ , Delft, The Netherlands, 15–19 July 2024. https://doi.org/10.15607/RSS.2024.XX.090. 

7. Wen, J.; Zhu, Y.; Li, J.; Zhu, M.; Wu, K.; Xu, Z.; Liu, N.; Cheng, R.; Shen, C.; Peng, Y.; et al. TinyVLA: Towards Fast, Data-Efficient Vision-Language-Action Models for Robotic Manipulation. _IEEE Robot. Autom. Lett. (RA-L)_ **2025** , _10_ , 3988–3995. 

8. Pertsch, K.; Stachowicz, K.; Ichter, B.; Driess, D.; Nair, S.; Vuong, Q.; Mees, O.; Finn, C.; Levine, S. FAST: Efficient Action Tokenization for Vision-Language-Action Models. In _Proceedings of Robotics: Science and Systems (RSS)_ , Los Angeles, CA, USA, 21–25 June 2025. https://doi.org/10.15607/RSS.2025.XXI.012. 

9. Lykov, A.; Serpiva, V.; Khan, M.H.; Sautenkov, O.; Myshlyaev, A.; Tadevosyan, G.; Yaqoot, Y.; Tsetserukou, D. CognitiveDrone: A VLA Model and Evaluation Benchmark for Real-Time Cognitive Task Solving and Reasoning in UAVs. _arXiv_ **2025** , arXiv:2503.01378. 

10. Mehboob, F.; James, M.; Habel, A.; Sam, J.; Altamirano Cabrera, M.; Tsetserukou, D. DroneVLA: VLA Based Aerial Manipulation. _arXiv_ **2026** , arXiv:2601.13809. 

11. Sun, J.; Tian, B.; Zhang, Q.; Li, C.; Song, Z.; Cui, Z.; Lv, Y.; Tian, Y. AIR-VLA: Vision-Language-Action Systems for Aerial Manipulation. _arXiv_ **2026** , arXiv:2601.21602. 

12. He, G.; Guo, X.; Tang, L.; Zhang, Y.; Mousaei, M.; Xu, J.; Geng, J.; Scherer, S.; Shi, G. Flying Hand: End-Effector-Centric Framework for Versatile Aerial Manipulation Teleoperation and Policy Learning. _arXiv_ **2025** , arXiv:2504.10334. 

13. Firoozi, R.; Tucker, J.; Tian, S.; Majumdar, A.; Sun, J.; Liu, W.; Zhu, Y.; Song, S.; Kapoor, A.; Hausman, K.; et al. Foundation Models in Robotics: Applications, Challenges, and the Future. _Int. J. Robot. Res._ **2025** , _44_ , 701–739. 

14. Wolf, R.; Shi, Y.; Liu, S.; Rayyes, R. Diffusion Models for Robotic Manipulation: A Survey. _Front. Robot. AI_ **2025** , _12_ , 1606247. 

15. Abbas, M.; Narayan, J.; Dwivedy, S.K. A Systematic Review on Cooperative Dual-Arm Manipulators: Modeling, Planning, Control, and Vision Strategies. _Int. J. Intell. Robot. Appl._ **2023** , _7_ , 683–707. 

16. Zhao, T.Z.; Kumar, V.; Levine, S.; Finn, C. Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware. In _Proceedings of Robotics: Science and Systems (RSS)_ , Daegu, Republic of Korea, 10–14 July 2023. https://doi.org/10.15607/RSS.2023.XIX.016. 

17. Lipman, Y.; Chen, R.T.Q.; Ben-Hamu, H.; Nickel, M.; Le, M. Flow Matching for Generative Modeling. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , Kigali, Rwanda, 1–5 May 2023. 

18. Mahony, R.; Kumar, V.; Corke, P. Multirotor Aerial Vehicles: Modeling, Estimation, and Control of Quadrotor. _IEEE Robot. Autom. Mag._ **2012** , _19_ , 20–32. 

19. Vaswani, A.; Shazeer, N.; Parmar, N.; Uszkoreit, J.; Jones, L.; Gomez, A.N.; Kaiser, Ł.; Polosukhin, I. Attention Is All You Need. In _Proceedings of the Advances in Neural Information Processing Systems (NeurIPS)_ , Long Beach, CA, USA, 4–9 December 2017. 

20. Dosovitskiy, A.; Beyer, L.; Kolesnikov, A.; Weissenborn, D.; Zhai, X.; Unterthiner, T.; Dehghani, M.; Minderer, M.; Heigold, G.; Gelly, S.; et al. An Image is Worth 16 _×_ 16 Words: Transformers for Image Recognition at Scale. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , Virtual, 3–7 May 2021. 

21. Radford, A.; Kim, J.W.; Hallacy, C.; Ramesh, A.; Goh, G.; Agarwal, S.; Sastry, G.; Askell, A.; Mishkin, P.; Clark, J.; et al. Learning Transferable Visual Models From Natural Language Supervision. In _Proceedings of the 38th International Conference on Machine Learning (ICML)_ ; PMLR: Virtual, 18–24 July 2021; Volume 139. 

22. Brown, T.B.; Mann, B.; Ryder, N.; Subbiah, M.; Kaplan, J.; Dhariwal, P.; Neelakantan, A.; Shyam, P.; Sastry, G.; Askell, A.; et al. Language Models Are Few-Shot Learners. In _Proceedings of the Advances in Neural Information Processing Systems (NeurIPS)_ , Virtual, 6–12 December 2020. 

23. Ouyang, L.; Wu, J.; Jiang, X.; Almeida, D.; Wainwright, C.L.; Mishkin, P.; Zhang, C.; Agarwal, S.; Slama, K.; Ray, A.; et al. Training Language Models to Follow Instructions with Human Feedback. In _Proceedings of the Advances in Neural Information Processing Systems (NeurIPS)_ , New Orleans, LA, USA, 28 November–9 December 2022. 

24. Driess, D.; Xia, F.; Sajjadi, M.S.M.; Lynch, C.; Chowdhery, A.; Ichter, B.; Wahid, A.; Tompson, J.; Vuong, Q.; Yu, T.; et al. PaLM-E: An Embodied Multimodal Language Model. In _Proceedings of the 40th International Conference on Machine Learning (ICML)_ ; PMLR: Honolulu, HI, USA, 23–29 July 2023; Volume 202. 

25. Beyer, L.; Steiner, A.; Pinto, A.S.; Kolesnikov, A.; Wang, X.; Salz, D.; Neumann, M.; Alabdulmohsin, I.; Tschannen, M.; Bugliarello, E.; et al. PaliGemma: A Versatile 3B VLM for Transfer. _arXiv_ **2024** , arXiv:2407.07726. 

26. Gemma Team. Gemma: Open Models Based on Gemini Research and Technology. _arXiv_ **2024** , arXiv:2403.08295. 

27. Touvron, H.; Lavril, T.; Izacard, G.; Martinet, X.; Lachaux, M.A.; Lacroix, T.; Rozière, B.; Goyal, N.; Hambro, E.; Azhar, F.; et al. LLaMA: Open and Efficient Foundation Language Models. _arXiv_ **2023** , arXiv:2302.13971. 

28. Liu, H.; Li, C.; Wu, Q.; Lee, Y.J. Visual Instruction Tuning. In _Proceedings of the Advances in Neural Information Processing Systems (NeurIPS)_ , New Orleans, LA, USA, 10–16 December 2023. 

29. Shi, L.X.; Ichter, B.; Equi, M.; Ke, L.; Pertsch, K.; Vuong, Q.; Tanner, J.; Walling, A.; Wang, H.; Fusai, N.; et al. Hi Robot: Open-Ended Instruction Following with Hierarchical Vision-Language-Action Models. In _Proceedings of the 42nd International Conference on Machine Learning (ICML)_ , Vancouver, BC, Canada, 13–19 July 2025. 

Hi Robot: 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

53 of 59 

30. Pomerleau, D.A. ALVINN: An Autonomous Land Vehicle in a Neural Network. In _Proceedings of the Advances in Neural Information Processing Systems (NeurIPS)_ , Denver, CO, USA, 27–30 November 1989. 

31. Ross, S.; Gordon, G.J.; Bagnell, D. A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning. In _Proceedings of the International Conference on Artificial Intelligence and Statistics (AISTATS)_ , Fort Lauderdale, FL, USA, 11–13 April 2011. 

32. Stepputtis, S.; Campbell, J.; Phielipp, M.; Lee, S.; Baral, C.; Ben Amor, H. Language-Conditioned Imitation Learning for Robot Manipulation Tasks. In _Proceedings of the Advances in Neural Information Processing Systems (NeurIPS)_ , Virtual, 6–12 December 2020. 

33. Kingma, D.P.; Welling, M. Auto-Encoding Variational Bayes. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , Banff, AB, Canada, 14–16 April 2014. 

34. Goodfellow, I.; Pouget-Abadie, J.; Mirza, M.; Xu, B.; Warde-Farley, D.; Ozair, S.; Courville, A.; Bengio, Y. Generative Adversarial Nets. In _Proceedings of the Advances in Neural Information Processing Systems (NeurIPS)_ , Montreal, QC, Canada, 8–13 December 2014. 

35. Ho, J.; Jain, A.; Abbeel, P. Denoising Diffusion Probabilistic Models. In _Proceedings of the Advances in Neural Information Processing Systems (NeurIPS)_ , Virtual, 6–12 December 2020. 

36. Song, Y.; Sohl-Dickstein, J.; Kingma, D.P.; Kumar, A.; Ermon, S.; Poole, B. Score-Based Generative Modeling through Stochastic Differential Equations. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , Virtual, 3–7 May 2021. 

37. Rombach, R.; Blattmann, A.; Lorenz, D.; Esser, P.; Ommer, B. High-Resolution Image Synthesis with Latent Diffusion Models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , New Orleans, LA, USA, 19–24 June 2022. 

38. Chen, L.; Lu, K.; Rajeswaran, A.; Lee, K.; Grover, A.; Laskin, M.; Abbeel, P.; Srinivas, A.; Mordatch, I. Decision Transformer: Reinforcement Learning via Sequence Modeling. In Proceedings of the Advances in Neural Information Processing Systems (NeurIPS), 2021. 

39. Reed, S.; Zolna, K.; Parisotto, E.; Colmenarejo, S.G.; Novikov, A.; Barth-Maron, G.; Giménez, M.; Sulsky, Y.; Kay, J.; Springenberg, J.T.; et al. A Generalist Agent. _Trans. Mach. Learn. Res. (TMLR)_ **2022** . Available online: https://openreview.net/forum?id=1ikK0 kHjvj (accessed on 21 May 2026). 

40. Chi, C.; Xu, Z.; Feng, S.; Cousineau, E.; Du, Y.; Burchfiel, B.; Tedrake, R.; Song, S. Diffusion Policy: Visuomotor Policy Learning via Action Diffusion. _Int. J. Robot. Res. (IJRR)_ **2024** , _44_ , 1684–1704. https://doi.org/10.1177/02783649241273668. 

41. Liu, X.; Gong, C.; Liu, Q. Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , Kigali, Rwanda, 1–5 May 2023. 

42. Fu, Z.; Zhao, T.Z.; Finn, C. Mobile ALOHA: Learning Bimanual Mobile Manipulation with Low-Cost Whole-Body Teleoperation. In _Proceedings of the 8th Conference on Robot Learning (CoRL)_ ; PMLR: Munich, Germany, 6–9 November 2024; Volume 270, pp. 4066–4083. 

43. Chi, C.; Xu, Z.; Pan, C.; Cousineau, E.; Burchfiel, B.; Feng, S.; Tedrake, R.; Song, S. Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots. In _Proceedings of Robotics: Science and Systems (RSS)_ , Delft, The Netherlands, 15–19 July 2024. https://doi.org/10.15607/RSS.2024.XX.045. 

44. Liu, S.; Wu, L.; Li, B.; Tan, H.; Chen, H.; Wang, Z.; Xu, K.; Su, H.; Zhu, J. RDT-1B: A Diffusion Foundation Model for Bimanual Manipulation. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , Singapore, 24–28 April 2025. 

45. Shah, S.; Dey, D.; Lovett, C.; Kapoor, A. AirSim: High-Fidelity Visual and Physical Simulation for Autonomous Vehicles. In _Field and Service Robotics (FSR)_ , Zurich, Switzerland, 12–15 September 2017; Springer Proceedings in Advanced Robotics, Volume 5, pp. 621–635, published 2018. 

46. Song, Y.; Naji, S.; Kaufmann, E.; Loquercio, A.; Scaramuzza, D. Flightmare: A Flexible Quadrotor Simulator. In _Proceedings of the 4th Conference on Robot Learning (CoRL)_ ; PMLR: Virtual, 16–18 November 2020; Volume 155, pp. 1147–1157. 

47. Liu, B.; Zhu, Y.; Gao, C.; Feng, Y.; Liu, Q.; Zhu, Y.; Stone, P. LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning. In _Proceedings of the Advances in Neural Information Processing Systems (NeurIPS)_ , New Orleans, LA, USA, 10–16 December 2023. 

48. Li, X.; Hsu, K.; Gu, J.; Pertsch, K.; Mees, O.; Walke, H.R.; Fu, C.; Lunawat, I.; Sieh, I.; Kirmani, S.; et al. Evaluating Real-World Robot Manipulation Policies in Simulation. In _Proceedings of the 8th Conference on Robot Learning (CoRL)_ ; PMLR: Munich, Germany, 6–9 November 2024; Volume 270, pp. 3705–3728. 

49. Open X-Embodiment Collaboration. Open X-Embodiment: Robotic Learning Datasets and RT-X Models. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , Yokohama, Japan, 13–17 May 2024; pp. 6892–6903. 

50. Khazatsky, A.; Pertsch, K.; Nair, S.; Balakrishna, A.; Dasari, S.; Karamcheti, S.; Nasiriany, S.; Srirama, M.K.; Chen, L.Y.; Ellis, K.; et al. DROID: A Large-Scale In-the-Wild Robot Manipulation Dataset. In _Proceedings of Robotics: Science and Systems (RSS)_ , Delft, The Netherlands, 15–19 July 2024. https://doi.org/10.15607/RSS.2024.XX.120. 

51. Walke, H.R.; Black, K.; Zhao, T.Z.; Vuong, Q.; Zheng, C.; Hansen-Estruch, P.; He, A.W.; Myers, V.; Kim, M.J.; Du, M.; et al. BridgeData V2: A Dataset for Robot Learning at Scale. In _Proceedings of the 7th Conference on Robot Learning (CoRL)_ ; PMLR: Atlanta, GA, USA, 6–9 November 2023; Volume 229, pp. 1723–1736. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

54 of 59 

52. Ebert, F.; Yang, Y.; Schmeckpeper, K.; Bucher, B.; Georgakis, G.; Daniilidis, K.; Finn, C.; Levine, S. Bridge Data: Boosting Generalization of Robotic Skills with Cross-Domain Datasets. In _Proceedings of Robotics: Science and Systems (RSS)_ , New York, NY, USA, 27 June–1 July 2022. 

53. Wang, B.; Li, B.; Ni, C.; Huang, G.; Zhao, G.; Li, H.; Li, J.; Lv, J.; Liu, J.; Feng, L.; et al. GigaBrain-0.5M<sup>_∗_</sup> : A VLA That Learns From World Model-Based Reinforcement Learning. _arXiv_ **2026** , arXiv:2602.12099. 

54. James, S.; Ma, Z.; Arrojo, D.R.; Davison, A.J. RLBench: The Robot Learning Benchmark and Learning Environment. _IEEE Robot. Autom. Lett. (RA-L)_ **2020** , _5_ , 3019–3026. 

55. Yu, T.; Quillen, D.; He, Z.; Julian, R.; Hausman, K.; Finn, C.; Levine, S. Meta-World: A Benchmark and Evaluation for Multi-Task and Meta Reinforcement Learning. In Proceedings of the Conference on Robot Learning (CoRL), 2020. 

56. Zhu, Y.; Wong, J.; Mandlekar, A.; Martín-Martín, R.; Joshi, A.; Lin, K.; Maddukuri, A.; Nasiriany, S.; Zhu, Y. robosuite: A Modular Simulation Framework and Benchmark for Robot Learning. _arXiv_ **2020** , arXiv:2009.12293. 

57. Gu, J.; Xiang, F.; Li, X.; Ling, Z.; Liu, X.; Mu, T.; Tang, Y.; Tao, S.; Wei, X.; Yao, Y.; et al. ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , Kigali, Rwanda, 1–5 May 2023. 

58. Li, C.; Zhang, R.; Wong, J.; Gokmen, C.; Srivastava, S.; Martín-Martín, R.; Wang, C.; Levine, G.; Ai, W.; Martinez, B.; et al. BEHAVIOR-1K: A Human-Centered, Embodied AI Benchmark with 1,000 Everyday Activities and Realistic Simulation. _arXiv_ **2024** , arXiv:2403.09227. 

59. Brohan, A.; Brown, N.; Carbajal, J.; Chebotar, Y.; Dabis, J.; Finn, C.; Gopalakrishnan, K.; Hausman, K.; Herzog, A.; Hsu, J.; et al. RT-1: Robotics Transformer for Real-World Control at Scale. In _Proceedings of Robotics: Science and Systems (RSS)_ , Daegu, Republic of Korea, 10–14 July 2023. https://doi.org/10.15607/RSS.2023.XIX.025. 

60. Kim, M.J.; Finn, C.; Liang, P. Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success. In _Proceedings of Robotics: Science and Systems (RSS)_ , Los Angeles, CA, USA, 21–25 June 2025. 

61. Wu, H.; Jing, Y.; Cheang, C.; Chen, G.; Xu, J.; Li, X.; Liu, M.; Li, H.; Kong, T. Unleashing Large-Scale Video Generative Pre-training for Visual Robot Manipulation. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , Vienna, Austria, 7–11 May 2024. 

62. Li, Y.; Deng, Y.; Zhang, J.; Jang, J.; Memmel, M.; Yu, R.; Garrett, C.R.; Ramos, F.; Fox, D.; Li, A.; et al. HAMSTER: Hierarchical Action Models for Open-World Robot Manipulation. _arXiv_ **2025** , arXiv:2502.05485. 

63. Qu, D.; Song, H.; Chen, Q.; Yao, Y.; Ye, X.; Ding, Y.; Wang, Z.; Gu, J.; Zhao, B.; Wang, D.; et al. SpatialVLA: Exploring Spatial Representations for Visual-Language-Action Model. In _Proceedings of Robotics: Science and Systems (RSS)_ , Los Angeles, CA, USA, 21–25 June 2025. 

64. Haldar, S.; Peng, Z.; Pinto, L. BAKU: An Efficient Transformer for Multi-Task Policy Learning. In _Proceedings of the Advances in Neural Information Processing Systems (NeurIPS)_ , Vancouver, BC, Canada, 9–15 December 2024. 

65. Di Palo, N.; Johns, E. Keypoint Action Tokens Enable In-Context Imitation Learning in Robotics. In _Proceedings of Robotics: Science and Systems (RSS)_ , Delft, The Netherlands, 15–19 July 2024. 

66. Li, H.; Zuo, Y.; Yu, J.; Zhang, Y.; Yang, Z.; Zhang, K.; Zhu, X.; Zhang, Y.; Chen, T.; Cui, G.; et al. SimpleVLA-RL: Scaling VLA Training via Reinforcement Learning. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , Available online: https://iclr.cc/Conferences/2026 (accessed on 21 May 2026). 

67. Li, Q.; Liang, Y.; Wang, Z.; Luo, L.; Chen, X.; Liao, M.; Wei, F.; Deng, Y.; Xu, S.; Zhang, Y.; et al. CogACT: A Foundational Vision-Language-Action Model for Synergizing Cognition and Action in Robotic Manipulation. _arXiv_ **2024** , arXiv:2411.19650. 

68. Shridhar, M.; Manuelli, L.; Fox, D. Perceiver-Actor: A Multi-Task Transformer for Robotic Manipulation. In _Proceedings of the Conference on Robot Learning (CoRL)_ , Atlanta, GA, USA, 6–9 November 2023. 

69. Goyal, A.; Xu, J.; Guo, Y.; Blukis, V.; Chao, Y.W.; Fox, D. RVT: Robotic View Transformer for 3D Object Manipulation. In _Proceedings of the Conference on Robot Learning (CoRL)_ , Atlanta, GA, USA, 6–9 November 2023. 

70. Ze, Y.; Zhang, G.; Zhang, K.; Hu, C.; Wang, M.; Xu, H. 3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations. In _Proceedings of Robotics: Science and Systems (RSS)_ , Delft, The Netherlands, 15–19 July 2024. 

71. Zhou, C.; Yu, L.; Babu, A.; Tirumala, K.; Yasunaga, M.; Shamis, L.; Kahn, J.; Ma, X.; Zettlemoyer, L.; Levy, O. Transfusion: Predict the Next Token and Diffuse Images with One Multi-Modal Model. In _Proceedings of the 13th International Conference on Learning Representations (ICLR)_ , Singapore, 24–28 April 2025. 

72. Liu, J.; Chen, H.; An, P.; Liu, Z.; Zhang, R.; Gu, C.; Li, X.; Guo, Z.; Chen, S.; Liu, M.; et al. HybridVLA: Collaborative Diffusion and Autoregression in a Unified Vision-Language-Action Model. _arXiv_ **2025** , arXiv:2503.10631. 

73. Belkhale, S.; Sadigh, D. MiniVLA: A Better VLA with a Smaller Footprint. 2024. Stanford AI Lab Blog. Available online: https://ai.stanford.edu/blog/minivla/ (accessed on 21 May 2026). 

74. Torne, M.; Pertsch, K.; Walke, H.; Vedder, K.; Nair, S.; Ichter, B.; Ren, A.Z.; Wang, H.; Tang, J.; Stachowicz, K.; et al. MEM: Multi-Scale Embodied Memory for Vision Language Action Models. _arXiv_ **2026** , arXiv:2603.03596. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

55 of 59 

75. Shi, H.; Xie, B.; Liu, Y.; Sun, L.; Liu, F.; Wang, T.; Zhou, E.; Fan, H.; Zhang, X.; Huang, G. MemoryVLA: Perceptual-Cognitive Memory in Vision-Language-Action Models for Robotic Manipulation. _arXiv_ **2025** , arXiv:2508.19236. 

76. Jang, H.; Yu, S.; Kwon, H.; Jeon, H.; Seo, Y.; Shin, J. ContextVLA: Vision-Language-Action Model with Amortized Multi-Frame Context. _arXiv_ **2025** , arXiv:2510.04246. 

77. Ye, A.; Wang, B.; Ni, C.; Huang, G.; Zhao, G.; Li, H.; Li, J.; Zhu, J.; Feng, L.; Li, P.; et al. GigaBrain-0: A World Model-Powered Vision-Language-Action Model. _arXiv_ **2025** , arXiv:2510.19430. 

78. Rhoda AI. Causal Video Models Are Data-Efficient Robot Policy Learners. 2026 Available online: https://www.rhoda.ai/ research/direct-video-action (accessed on 21 May 2026). 

79. Cen, J.; Yu, C.; Yuan, H.; Jiang, Y.; Huang, S.; Guo, J.; Li, X.; Song, Y.; Luo, H.; Wang, F.; et al. WorldVLA: Towards Autoregressive Action World Model. _arXiv_ **2025** , arXiv:2506.21539. 

80. Ye, A.; Wang, B.; Ni, C.; Huang, G.; Zhao, G.; Li, H.; Zhu, J.; Li, K.; Xu, M.; Deng, Q.; et al. GigaWorld-0: World Models as Data Engine to Empower Embodied AI. _arXiv_ **2025** , arXiv:2511.19861. 

81. Hu, E.J.; Shen, Y.; Wallis, P.; Allen-Zhu, Z.; Li, Y.; Wang, S.; Wang, L.; Chen, W. LoRA: Low-Rank Adaptation of Large Language Models. In Proceedings of the International Conference on Learning Representations (ICLR), 2022. 

82. Rafailov, R.; Sharma, A.; Mitchell, E.; Ermon, S.; Manning, C.D.; Finn, C. Direct Preference Optimization: Your Language Model is Secretly a Reward Model. In _Proceedings of the Advances in Neural Information Processing Systems (NeurIPS)_ , New Orleans, LA, USA, 10–16 December 2023. 

83. Driess, D.; Springenberg, J.T.; Ichter, B.; Yu, L.; Li-Bell, A.; Pertsch, K.; Ren, A.Z.; Walke, H.; Vuong, Q.; Shi, L.X.; et al. Knowledge Insulating Vision-Language-Action Models: Train Fast, Run Fast, Generalize Better. _arXiv_ **2025** , arXiv:2505.23705. 

84. Zhang, Y.; Wang, C.; Lu, O.; Zhao, Y.; Ge, Y.; Sun, Z.; Li, X.; Zhang, C.; Bai, C.; Li, X. Align-Then-stEer: Adapting the Vision-Language Action Models through Unified Latent Guidance. _arXiv_ **2025** , arXiv:2509.02055. 

85. Mandlekar, A.; Xu, D.; Wong, J.; Nasiriany, S.; Wang, C.; Kulkarni, R.; Fei-Fei, L.; Savarese, S.; Zhu, Y.; Martín-Martín, R. What Matters in Learning from Offline Human Demonstrations for Robot Manipulation. In _Proceedings of the 5th Conference on Robot Learning (CoRL)_ ; PMLR: London, UK, 8–11 November 2021; Volume 164. 

86. Bharadhwaj, H.; Vakil, J.; Sharma, M.; Gupta, A.; Tulsiani, S.; Kumar, V. RoboAgent: Generalization and Efficiency in Robot Manipulation via Semantic Augmentations and Action Chunking. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , Yokohama, Japan, 13–17 May 2024. 

87. Kalashnikov, D.; Irpan, A.; Pastor, P.; Ibarz, J.; Herzog, A.; Jang, E.; Quillen, D.; Holly, E.; Kalakrishnan, M.; Vanhoucke, V.; et al. QT-Opt: Scalable Deep Reinforcement Learning for Vision-Based Robotic Manipulation. In _Proceedings of the Conference on Robot Learning (CoRL)_ , Zürich, Switzerland, 29–31 October 2018. 

88. Kumar, A.; Zhou, A.; Tucker, G.; Levine, S. Conservative Q-Learning for Offline Reinforcement Learning. In _Proceedings of the Advances in Neural Information Processing Systems (NeurIPS)_ , Virtual, 6–12 December 2020. 

89. Peng, X.B.; Kumar, A.; Zhang, G.; Levine, S. Advantage-Weighted Regression: Simple and Scalable Off-Policy Reinforcement Learning. _arXiv_ **2019** , arXiv:1910.00177. 

90. Levine, S.; Kumar, A.; Tucker, G.; Fu, J. Offline Reinforcement Learning: Tutorial, Review, and Perspectives on Open Problems. _arXiv_ **2020** , arXiv:2005.01643. 

91. Schulman, J.; Wolski, F.; Dhariwal, P.; Radford, A.; Klimov, O. Proximal Policy Optimization Algorithms. _arXiv_ **2017** , arXiv:1707.06347. 

92. Ranawaka Arachchige, N.; Chen, Z.; Jung, W.; Shin, W.C.; Bansal, R.; Barroso, P.; He, Y.H.; Lin, Y.C.; Joffe, B.; Kousik, S.; et al. SAIL: Faster-than-Demonstration Execution of Imitation Learning Policies. In _Proceedings of the 9th Conference on Robot Learning (CoRL)_ ; PMLR: Seoul, Republic of Korea, 27–30 September 2025; Volume 305, pp. 721–749. 

93. Lu, G.; Guo, W.; Zhang, C.; Zhou, Y.; Jiang, H.; Gao, Z.; Tang, Y.; Wang, Z. VLA-RL: Towards Masterful and General Robotic Manipulation with Scalable Reinforcement Learning. _arXiv_ **2025** , arXiv:2505.18719. 

94. Chen, Y.; Tian, S.; Liu, S.; Zhou, Y.; Li, H.; Zhao, D. ConRFT: A Reinforced Fine-Tuning Method for VLA Models via Consistency Policy. _arXiv_ **2025** , arXiv:2502.05450. 

95. Chebotar, Y.; Vuong, Q.; Hausman, K.; Xia, F.; Lu, Y.; Irpan, A.; Kumar, A.; Yu, T.; Herzog, A.; Pertsch, K.; et al. Q-Transformer: Scalable Offline Reinforcement Learning via Autoregressive Q-Functions. In _Proceedings of the 7th Conference on Robot Learning (CoRL)_ ; PMLR: Atlanta, GA, USA, 6–9 November 2023; Volume 229, pp. 3909–3928. 

96. Ren, A.Z.; Lidard, J.; Ankile, L.L.; Simeonov, A.; Agrawal, P.; Majumdar, A.; Burchfiel, B.; Dai, H.; Simchowitz, M. Diffusion Policy Policy Optimization. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , Singapore, 24–28 April 2025. 

97. Ghasemipour, S.K.S.; Wahid, A.; Tompson, J.; Sanketi, P.; Mordatch, I. Self-Improving Embodied Foundation Models. _arXiv_ **2025** , arXiv:2509.15155. 

98. Levine, S.; Pastor, P.; Krizhevsky, A.; Ibarz, J.; Quillen, D. Learning Hand-Eye Coordination for Robotic Grasping with Deep Learning and Large-Scale Data Collection. _Int. J. Robot. Res. (IJRR)_ **2018** , _37_ , 421–436. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

56 of 59 

99. Ha, H.; Florence, P.; Song, S. Scaling Up and Distilling Down: Language-Guided Robot Skill Acquisition. In _Proceedings of the Conference on Robot Learning (CoRL)_ , Atlanta, GA, USA, 6–9 November 2023. 

100. Zheng, J.; Li, J.; Liu, D.; Zheng, Y.; Wang, Z.; Ou, Z.; Liu, Y.; Liu, J.; Zhang, Y.Q.; Zhan, X. Universal Actions for Enhanced Embodied Foundation Models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , Nashville, TN, USA, 11–15 June 2025. 

101. Ding, Z.; Jin, C. Consistency Models as a Rich and Efficient Policy Class for Reinforcement Learning. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , Vienna, Austria, 7–11 May 2024. 

102. Dai, Y.; Lee, J.; Fazeli, N.; Chai, J. RACER: Rich Language-Guided Failure Recovery Policies for Imitation Learning. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , Atlanta, GA, USA, 19–23 May 2025. 

103. Black, K.; Galliker, M.Y.; Levine, S. Real-Time Execution of Action Chunking Flow Policies. In _Proceedings of the Advances in Neural Information Processing Systems (NeurIPS)_ , San Diego, CA, USA, 2–7 December 2025. 

104. Liu, Y.; Hamid, J.I.; Xie, A.; Lee, Y.; Du, M.; Finn, C. Bidirectional Decoding: Improving Action Chunking via Guided Test-Time Sampling. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , Singapore, 24–28 April 2025. 

105. Black, K.; Ren, A.Z.; Equi, M.; Levine, S. Training-Time Action Conditioning for Efficient Real-Time Chunking. _arXiv_ **2025** , arXiv:2512.05964. 

106. Grannen, J.; Wu, Y.; Vu, B.; Sadigh, D. Stabilize to Act: Learning to Coordinate for Bimanual Manipulation. In _Proceedings of the 7th Conference on Robot Learning (CoRL)_ ; PMLR: Atlanta, GA, USA, 6–9 November 2023; Volume 229, pp. 563–576. 

107. Chitnis, R.; Tulsiani, S.; Gupta, S.; Gupta, A. Efficient Bimanual Manipulation Using Learned Task Schemas. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , Virtual, 31 May–4 June 2020. 

108. Liang, J.; Huang, W.; Xia, F.; Xu, P.; Hausman, K.; Ichter, B.; Florence, P.; Zeng, A. Code as Policies: Language Model Programs for Embodied Control. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , London, United Kingdom, 29 May–2 June 2023. 

109. Ahn, M.; Brohan, A.; Brown, N.; Chebotar, Y.; Cortes, O.; David, B.; Finn, C.; Fu, C.; Gober, K.; Hausman, K.; et al. Do As I Can, Not As I Say: Grounding Language in Robotic Affordances. In _Proceedings of the 6th Conference on Robot Learning (CoRL)_ ; PMLR: Auckland, New Zealand, 14–18 December 2022; Volume 205. 

110. Wang, C.; Fan, L.; Sun, J.; Zhang, R.; Fei-Fei, L.; Xu, D.; Zhu, Y.; Anandkumar, A. MimicPlay: Long-Horizon Imitation Learning by Watching Human Play. In _Proceedings of the Conference on Robot Learning (CoRL)_ , Atlanta, GA, USA, 6–9 November 2023. 

111. Chen, L.; Bahl, S.; Pathak, D. PlayFusion: Skill Acquisition via Diffusion from Language-Annotated Play. In _Proceedings of the Conference on Robot Learning (CoRL)_ , Atlanta, GA, USA, 6–9 November 2023. 

112. Du, Y.; Yang, M.; Dai, B.; Dai, H.; Nachum, O.; Tenenbaum, J.B.; Schuurmans, D.; Abbeel, P. Learning Universal Policies via Text-Guided Video Generation. In _Proceedings of the Advances in Neural Information Processing Systems (NeurIPS)_ , New Orleans, LA, USA, 10–16 December 2023. 

113. Hu, Y.; Lin, F.; Zhang, T.; Yi, L.; Gao, Y. Look Before You Leap: Unveiling the Power of GPT-4V in Robotic Vision-Language Planning. _arXiv_ **2023** , arXiv:2311.17842. 

114. Li, H.; Yang, S.; Chen, Y.; Chen, X.; Yang, X.; Tian, Y.; Wang, H.; Wang, T.; Lin, D.; Zhao, F.; et al. CronusVLA: Towards Efficient and Robust Manipulation via Multi-Frame Vision-Language-Action Modeling. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , 2026; _forthcoming_ . 

115. Mark, M.S.; Liang, J.; Attarian, M.; Fu, C.; Dwibedi, D.; Shah, D.; Kumar, A. BPP: Long-Context Robot Imitation Learning by Focusing on Key History Frames. _arXiv_ **2026** , arXiv:2602.15010. 

116. Torne, M.; Tang, A.; Liu, Y.; Finn, C. Learning Long-Context Diffusion Policies via Past-Token Prediction. In _Proceedings of the 9th Conference on Robot Learning (CoRL)_ ; PMLR: Seoul, Republic of Korea, 27–30 September 2025; Volume 305. 

117. Fang, H.; Grotz, M.; Pumacay, W.; Wang, Y.R.; Fox, D.; Krishna, R.; Duan, J. SAM2Act: Integrating Visual Foundation Model with a Memory Architecture for Robotic Manipulation. In _Proceedings of the International Conference on Machine Learning (ICML)_ , Vancouver, BC, Canada, 13–19 July 2025. 

118. Sridhar, A.; Pan, J.; Sharma, S.; Finn, C. MemER: Scaling Up Memory for Robot Control via Experience Retrieval. _arXiv_ **2025** , arXiv:2510.20328. 

119. Wei, Y.L.; Liao, H.; Lin, Y.; Wang, P.; Liang, Z.; Liu, G.; Zheng, W.S. CycleManip: Enabling Cyclic Task Manipulation via Effective Historical Perception and Understanding. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2026; _forthcoming_ . 

120. Ha, H.; Gao, Y.; Fu, Z.; Tan, J.; Song, S. UMI on Legs: Making Manipulation Policies Mobile with Manipulation-Centric Wholebody Controllers. In _Proceedings of the 8th Conference on Robot Learning (CoRL)_ ; PMLR: Munich, Germany, 6–9 November 2024; Volume 270. 

121. Shah, R.; Yu, A.; Zhu, Y.; Zhu, Y.; Martín-Martín, R. BUMBLE: Unifying Reasoning and Acting with Vision-Language Models for Building-wide Mobile Manipulation. _arXiv_ **2024** , arXiv:2410.06237. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

57 of 59 

122. Bu, Q.; Cai, J.; Chen, L.; Cui, X.; Ding, Y.; Feng, S.; Gao, S.; He, X.; Hu, X.; Huang, X.; et al. AgiBot World Colosseo: A Large-scale Manipulation Platform for Scalable and Intelligent Embodied Systems. _arXiv_ **2025** , arXiv:2503.06669. 

123. Blank, N.; Reuss, M.; Rühle, M.; Ya˘gmurlu, Ö.E.; Wenzel, F.; Mees, O.; Lioutikov, R. Scaling Robot Policy Learning via Zero-Shot Labeling with Foundation Models. In _Proceedings of the 8th Conference on Robot Learning (CoRL)_ ; PMLR: Munich, Germany, 6–9 November 2024; Volume 270, pp. 4158–4187. 

124. Liu, S.; Zhang, H.; Qi, Y.; Wang, P.; Zhang, Y.; Wu, Q. AerialVLN: Vision-and-Language Navigation for UAVs. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , Paris, France, 2–6 October 2023. 

125. Shah, D.; Equi, M.; Osinski, B.; Xia, F.; Ichter, B.; Levine, S. Navigation with Large Language Models: Semantic Guesswork as a Heuristic for Planning. In _Proceedings of the Conference on Robot Learning (CoRL)_ , Atlanta, GA, USA, 6–9 November 2023. 

126. Sautenkov, O.; Yaqoot, Y.; Lykov, A.; Mustafa, M.A.; Tadevosyan, G.; Akhmetkazy, A.; Altamirano Cabrera, M.; Martynov, M.; Karaf, S.; Tsetserukou, D. UAV-VLA: Vision-Language-Action System for Large Scale Aerial Mission Generation. In _Proceedings of the 2025 ACM/IEEE International Conference on Human-Robot Interaction (HRI)_ , Melbourne, Australia, 4–6 March 2025. 

127. Saxena, P.; Raghuvanshi, N.; Goveas, N. UAV-VLN: End-to-End Vision Language Guided Navigation for UAVs. _arXiv_ **2025** , arXiv:2504.21432. 

128. Gao, Y.; Li, C.; You, Z.; Liu, J.; Li, Z.; Chen, P.; Chen, Q.; Tang, Z.; Wang, L.; Yang, P.; et al. OpenFly: A Comprehensive Platform for Aerial Vision-Language Navigation. _arXiv_ **2025** , arXiv:2502.18041. 

129. Zhang, W.; Gao, C.; Yu, S.; Peng, R.; Zhao, B.; Zhang, Q.; Cui, J.; Chen, X.; Li, Y. CityNavAgent: Aerial Vision-and-Language Navigation with Hierarchical Semantic Planning and Global Memory. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL)_ , Vienna, Austria, 27 July–1 August 2025. 

130. Zhao, X.; Lyu, X.; Li, X. AgriVLN: Vision-and-Language Navigation for Agricultural Robots. _arXiv_ **2025** , arXiv:2508.07406. 

131. Hwangbo, J.; Sa, I.; Siegwart, R.; Hutter, M. Control of a Quadrotor with Reinforcement Learning. _IEEE Robot. Autom. Lett._ **2017** , _2_ , 2096–2103. 

132. Kaufmann, E.; Bauersfeld, L.; Loquercio, A.; Müller, M.; Koltun, V.; Scaramuzza, D. Champion-level drone racing using deep reinforcement learning. _Nature_ **2023** , _620_ , 982–987. 

133. Shi, G.; Shi, X.; O’Connell, M.; Yu, R.; Azizzadenesheli, K.; Anandkumar, A.; Yue, Y.; Chung, S.J. Neural Lander: Stable Drone Landing Control Using Learned Dynamics. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , Montreal, QC, Canada, 20–24 May 2019. 

134. Serpiva, V.; Lykov, A.; Myshlyaev, A.; Khan, M.H.; Abdulkarim, A.A.; Sautenkov, O.; Tsetserukou, D. RaceVLA: VLA-Based Racing Drone Navigation with Human-like Behaviour. _arXiv_ **2025** , arXiv:2503.02572. 

135. Romero, A.; Shenai, A.; Geles, I.; Aljalbout, E.; Scaramuzza, D. Dream to Fly: Model-Based Reinforcement Learning for Vision-Based Drone Flight. _arXiv_ **2025** , arXiv:2501.14377. 

136. O’Connell, M.; Shi, G.; Shi, X.; Azizzadenesheli, K.; Anandkumar, A.; Yue, Y.; Chung, S.J. Neural-Fly Enables Rapid Learning for Agile Flight in Strong Winds. _Sci. Robot._ **2022** , _7_ , eabm6597. https://doi.org/10.1126/scirobotics.abm6597. 

137. Liu, Z.; Zhou, J.; Mucchiani, C.; Karydis, K. Vision-assisted Avocado Harvesting with Aerial Bimanual Manipulation. _arXiv_ **2024** , arXiv:2408.09058. 

138. Zhao, H.; Pan, F.; Ping, H.; Zhou, Y. Agent as Cerebrum, Controller as Cerebellum: Implementing an Embodied LMM-based Agent on Drones. _arXiv_ **2023** , arXiv:2311.15033. 

139. Chen, G.; Yu, X.; Ling, N.; Zhong, L. TypeFly: Low-Latency Drone Planning with Large Language Models. _IEEE Trans. Mob. Comput._ **2025** , _24_ , 9068–9079. https://doi.org/10.1109/TMC.2025.3561282. 

140. Lynch, C.; Wahid, A.; Tompson, J.; Ding, T.; Betker, J.; Baruch, R.; Armstrong, T.; Florence, P. Interactive Language: Talking to Robots in Real Time. _IEEE Robot. Autom. Lett. (RA-L)_ 2023, _early access._ 

141. Batra, S.; Huang, Z.; Petrenko, A.; Kumar, T.; Molchanov, A.; Sukhatme, G.S. Decentralized Control of Quadrotor Swarms with End-to-end Deep Reinforcement Learning. In _Proceedings of the Conference on Robot Learning (CoRL)_ , Auckland, New Zealand, 14–18 December 2022. 

142. Doshi, R.; Walke, H.R.; Mees, O.; Dasari, S.; Levine, S. Scaling Cross-Embodied Learning: One Policy for Manipulation, Navigation, Locomotion and Aviation. In _Proceedings of the 8th Conference on Robot Learning (CoRL)_ ; PMLR: Munich, Germany, 6–9 November 2024; Volume 270, pp. 496–512. 

143. Furrer, F.; Burri, M.; Achtelik, M.; Siegwart, R. RotorS: A Modular Gazebo MAV Simulator Framework. In _Robot Operating System (ROS): The Complete Reference (Volume 1)_ ; Koubaa, A., Ed.; Studies in Computational Intelligence, Volume 625; Springer, 2016; pp. 595–625. 

144. Wang, W.; Zhu, D.; Wang, X.; Hu, Y.; Qiu, Y.; Wang, C.; Hu, Y.; Kapoor, A.; Scherer, S. TartanAir: A Dataset to Push the Limits of Visual SLAM. In _Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , Las Vegas, NV, USA, 25–29 October 2020. 

145. Fonder, M.; Van Droogenbroeck, M. Mid-Air: A Multi-Modal Dataset for Extremely Low Altitude Drone Flights. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)_ , Long Beach, CA, USA, 16–20 June 2019. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

58 of 59 

146. Jang, E.; Irpan, A.; Khansari, M.; Kappler, D.; Ebert, F.; Lynch, C.; Levine, S.; Finn, C. BC-Z: Zero-Shot Task Generalization with Robotic Imitation Learning. In _Proceedings of the Conference on Robot Learning (CoRL)_ , Auckland, New Zealand, 14–18 December 2022. 

147. Huang, W.; Wang, C.; Zhang, R.; Li, Y.; Wu, J.; Fei-Fei, L. VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models. In _Proceedings of the Conference on Robot Learning (CoRL)_ , Atlanta, GA, USA, 6–9 November 2023. 

148. Duan, J.; Yuan, W.; Pumacay, W.; Wang, Y.R.; Ehsani, K.; Fox, D.; Krishna, R. Manipulate-Anything: Automating Real-World Robots using Vision-Language Models. In _Proceedings of the 8th Conference on Robot Learning (CoRL)_ ; PMLR: Munich, Germany, 6–9 November 2024; Volume 270, pp. 5326–5350. 

149. Jia, Z.; Thumuluri, V.; Liu, F.; Chen, L.; Huang, Z.; Su, H. Chain-of-Thought Predictive Control. In _Proceedings of the International Conference on Machine Learning (ICML)_ , Vienna, Austria, 21–27 July 2024. 

150. Cai, R.; Guo, J.; He, X.; Jin, P.; Li, J.; Lin, B.; Liu, F.; Liu, W.; Ma, F.; Ma, K.; et al. Xiaomi-Robotics-0: An Open-Sourced Vision-Language-Action Model with Real-Time Execution. _arXiv_ **2026** , arXiv:2602.12684. 

151. Belkhale, S.; Ding, T.; Xiao, T.; Sermanet, P.; Vuong, Q.; Tompson, J.; Chebotar, Y.; Dwibedi, D.; Sadigh, D. RT-H: Action Hierarchies Using Language. In _Proceedings of Robotics: Science and Systems (RSS)_ , Delft, The Netherlands, 15–19 July 2024. 

152. Liu, P.; Orru, Y.; Vakil, J.; Paxton, C.; Shafiullah, N.M.M.; Pinto, L. OK-Robot: What Really Matters in Integrating Open-Knowledge Models for Robotics. In _Proceedings of Robotics: Science and Systems (RSS)_ , Delft, The Netherlands, 15–19 July 2024. 

153. Etukuru, H.; Naka, N.; Hu, Z.; Lee, S.; Mehu, J.; Edsinger, A.; Paxton, C.; Chintala, S.; Pinto, L.; Shafiullah, N.M.M. Robot Utility Models: General Policies for Zero-Shot Deployment in New Environments. _arXiv_ **2024** , arXiv:2409.05865. 

154. Zeng, A.; Florence, P.; Tompson, J.; Welker, S.; Chien, J.; Attarian, M.; Armstrong, T.; Krasin, I.; Duong, D.; Sindhwani, V.; et al. Transporter Networks: Rearranging the Visual World for Robotic Manipulation. In _Proceedings of the Conference on Robot Learning (CoRL)_ , Virtual, 16–18 November 2020. 

155. Nair, S.; Rajeswaran, A.; Kumar, V.; Finn, C.; Gupta, A. R3M: A Universal Visual Representation for Robot Manipulation. In _Proceedings of the Conference on Robot Learning (CoRL)_ , Auckland, New Zealand, 14–18 December 2022. 

156. Nair, S.; Mitchell, E.; Chen, K.; Ichter, B.; Savarese, S.; Finn, C. Learning Language-Conditioned Robot Behavior from Offline Data and Crowd-Sourced Annotation. In _Proceedings of the Conference on Robot Learning (CoRL)_ , Auckland, New Zealand, 14–18 December 2022. 

157. Majumdar, A.; Yadav, K.; Arnaud, S.; Ma, Y.J.; Chen, C.; Silwal, S.; Jain, A.; Berges, V.P.; Abbeel, P.; Malik, J.; et al. Where Are We in the Search for an Artificial Visual Cortex for Embodied Intelligence? In _Proceedings of the Advances in Neural Information Processing Systems (NeurIPS)_ , New Orleans, LA, USA, 10–16 December 2023. 

158. Zhu, H.; Yang, H.; Wang, Y.; Yang, J.; Wang, L.; He, T. SPA: 3D Spatial-Awareness Enables Effective Embodied Representation. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , Singapore, 24–28 April 2025. 

159. Bharadhwaj, H.; Dwibedi, D.; Gupta, A.; Tulsiani, S.; Doersch, C.; Xiao, T.; Shah, D.; Xia, F.; Sadigh, D.; Kirmani, S. Gen2Act: Human Video Generation in Novel Scenarios Enables Generalizable Robot Manipulation. _arXiv_ **2024** , arXiv:2409.16283. 

160. Bharadhwaj, H.; Mottaghi, R.; Gupta, A.; Tulsiani, S. Track2Act: Predicting Point Tracks from Internet Videos Enables Generalizable Robot Manipulation. In _Proceedings of the European Conference on Computer Vision (ECCV)_ , Milan, Italy, 29 September–4 October 2024. 

161. Hu, Y.; Guo, Y.; Wang, P.; Chen, X.; Wang, Y.J.; Zhang, J.; Sreenath, K.; Lu, C.; Chen, J. Video Prediction Policy: A Generalist Robot Policy with Predictive Visual Representations. In _Proceedings of the International Conference on Machine Learning (ICML)_ , Vancouver, BC, Canada, 13–19 July 2025. 

162. Routray, S.; Pan, H.; Jain, U.; Bahl, S.; Pathak, D. ViPRA: Video Prediction for Robot Actions. In _Proceedings of the Advances in Neural Information Processing Systems (NeurIPS)_ , San Diego, CA, USA, 2–7 December 2025. 

163. Pai, J.; Achenbach, L.; Montesinos, V.; Forrai, B.; Mees, O.; Nava, E. Mimic-Video: Video-Action Models for Generalizable Robot Control Beyond VLAs. _arXiv_ **2025** , arXiv:2512.15692. 

164. Ranasinghe, K.; Zhou, H.; Fang, Y.; Yang, L.; Xue, L.; Xu, R.; Xiong, C.; Savarese, S.; Ryoo, M.S.; Niebles, J.C. Future Optical Flow Prediction Improves Robot Control & Video Generation. _arXiv_ **2026** , arXiv:2601.10781. 

165. Assran, M.; Bardes, A.; Fan, D.; Garrido, Q.; Howes, R.; Komeili, M.; Muckley, M.; Rizvi, A.; Roberts, C.; Sinha, K.; et al. V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning. _arXiv_ **2025** , arXiv:2506.09985. 

166. Zhang, J.; Guo, Y.; Hu, Y.; Chen, X.; Zhu, X.; Chen, J. UP-VLA: A Unified Understanding and Prediction Model for Embodied Agent. In _Proceedings of the 42nd International Conference on Machine Learning (ICML)_ ; PMLR: Vancouver, BC, Canada, 13–19 July 2025. 

167. Agarwal, N.; Ali, A.; Bala, M.; Balaji, Y.; Barker, E.; Cai, T.; Chattopadhyay, P.; Chen, Y.; Cui, Y.; Ding, Y.; et al. Cosmos World Foundation Model Platform for Physical AI. _arXiv_ **2025** , arXiv:2501.03575. 

168. Nasiriany, S.; Xia, F.; Yu, W.; Xiao, T.; Liang, J.; Dasgupta, I.; Xie, A.; Driess, D.; Wahid, A.; Xu, Z.; et al. PIVOT: Iterative Visual Prompting Elicits Actionable Knowledge for VLMs. In _Proceedings of the 41st International Conference on Machine Learning (ICML)_ ; PMLR: Vienna, Austria, 21–27 July 2024. 

https://doi.org/10.3390/drones10060412 

_Drones_ **2026** , _10_ , 412 

59 of 59 

169. Wu, J.; Antonova, R.; Kan, A.; Lepert, M.; Zeng, A.; Song, S.; Bohg, J.; Rusinkiewicz, S.; Funkhouser, T. TidyBot: Personalized Robot Assistance with Large Language Models. _Auton. Robot._ **2023** , _47_ , 1087–1102. https://doi.org/10.1007/s10514-023-10139-z (accessed on 21 May 2026). 

170. Liu, Z.; Chi, C.; Cousineau, E.; Kuppuswamy, N.; Burchfiel, B.; Song, S. ManiWAV: Learning Robot Manipulation from In-the-Wild Audio-Visual Data. In _Proceedings of the 8th Conference on Robot Learning (CoRL)_ ; PMLR: Munich, Germany, 6–9 November 2024; Volume 270. 

171. Google DeepMind Gemini Robotics Team. Gemini Robotics: Bringing AI into the Physical World. _arXiv_ **2025** , arXiv:2503.20020. 

172. Bjorck, J.; Castañeda, F.; Cherniadev, N.; Da, X.; Ding, R.; Fan, L.; Fang, Y.; Fox, D.; Hu, F.; Huang, S.; et al. GR00T N1: An Open Foundation Model for Generalist Humanoid Robots. _arXiv_ **2025** , arXiv:2503.14734. 

173. Figure AI. Helix: A Vision-Language-Action Model for Generalist Humanoid Control. 2025. Available online: https://www. figure.ai/news/helix (accessed on 21 May 2026). 

174. 1X Technologies. 1X World Model. 2025. Available online: https://www.1x.tech/discover/1x-world-model (accessed on 21 May 2026). 

175. Dyna Robotics. DYNA-1: The First Commercial-Ready Robot Foundation Model. 2025. Available online: https://www.dyna.co/ (accessed on 21 May 2026). 

176. Sunday Robotics. ACT-1: A Robot Foundation Model Trained on Zero Robot Data. 2025. Available online: https://www.sunday. ai/journal/no-robot-data (accessed on 21 May 2026). 

177. Covariant. Introducing RFM-1: Giving Robots Human-Like Reasoning Capabilities. 2024. Available online: https://en.wikipedia. org/wiki/Covariant_(company) (accessed on 21 May 2026). 

178. Boston Dynamics.; Toyota Research Institute. Large Behavior Models and Atlas Find New Footing. 2025. Available online: https://bostondynamics.com/blog/large-behavior-models-atlas-find-new-footing/ (accessed on 21 May 2026). 

179. Tesla AI. Tesla Optimus: A General-Purpose Humanoid Robot, 2025. Available online: https://en.wikipedia.org/wiki/Optimus_ (robot) (accessed on 21 May 2026). 

180. Tevel Aerobotics Technologies. 2024. Flying Autonomous Robots for Fruit Picking. Available online: https://www.tevel-tech.com (accessed on 8 May 2025). 

181. Upadhyay, A.; Zhang, Y.; Koparan, C.; Rai, N.; Howatt, K.; Bajwa, S.; Sun, X. Advances in ground robotic technologies for site-specific weed management in precision agriculture: A review. _Comput. Electron. Agric._ **2024** , _225_ , 109363. 

182. Anand, S.; Sridharan, B.; Kanchana Devi, V.; Haris, M. Robotic Harvesters for Fruits and Vegetables. In _AI-Aided Robotic Applications in Agriculture and Farming_ ; Springer: Berlin/Heidelberg, Germany, 2023. 

183. Zhao, Z.; Wang, S.; Miao, Z.; Xiong, Y. HarvestFlex: Strawberry Harvesting via Vision-Language-Action Policy Adaptation in the Wild. _arXiv_ **2026** , arXiv:2603.05982. 

**Disclaimer/Publisher’s Note:** The statements, opinions and data contained in all publications are solely those of the individual author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or the editor(s) disclaim responsibility for any injury to people or property resulting from any ideas, methods, instructions or products referred to in the content. 

https://doi.org/10.3390/drones10060412 

