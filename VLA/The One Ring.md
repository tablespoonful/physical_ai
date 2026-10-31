---
title: "The One Ring: a Robotic Indoor Navigation Generalist"
date: "2026"
venue: "ICRA 2026"
url: https://doi.org/10.1109/ICRA57385.2026.11696447
pdf: https://arxiv.org/pdf/2412.14401
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2412.14401)** / [論文ページ](https://doi.org/10.1109/ICRA57385.2026.11696447)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **The One RING : a Robotic Indoor Navigation Generalist** 

**Ainaz Eftekhar**<sup>1</sup><sup>_,_2</sup> **Rose Hendrix**<sup>2</sup> **Luca Weihs**<sup>2</sup> **Jiafei Duan**<sup>1</sup><sup>_,_2</sup> **Ege Caglar**<sup>1</sup> **Jordi Salvador**<sup>2</sup> **Alvaro Herrasti**<sup>2</sup> **Winson Han**<sup>2</sup> **Eli VanderBil**<sup>2</sup> **Aniruddha Kembhavi**<sup>1</sup><sup>_,_2</sup> **Ali Farhadi**<sup>1</sup><sup>_,_2</sup> **Ranjay Krishna**<sup>1</sup><sup>_,_2</sup> **Kiana Ehsani**<sup>_∗_2</sup> **Kuo-Hao Zeng**<sup>_∗_2</sup> 

1University of Washington 

2Allen Institute for AI 

**one-ring-policy.allen.ai** 


Figure 1: We show that training on _one million_ randomly generated embodiments in simulation (varying camera configurations, body size, and rotation pivot point) results in RING, a generalist navigation policy that works across various robot embodiments in the real world. (A) A t-SNE visualization of embodiment parameters for 30k random agents and three real robots ( _we do not train on any real robot embodiment parameters_ ). Egocentric views from the first camera are shown for 10 sample agents. (B) RING transfers zero-shot to a wide range of embodiments in the real-world including Stretch RE-1, LoCoBot, Unitree Go1, RB-Y1 wheeled humanoid. (C) The policy displays embodiment-adaptive behavior, adjusting its navigation strategy based on its embodiment. 

**Abstract:** Modern robots vary significantly in shape, size, and sensor configurations used to perceive and interact with their environments. However, most navigation policies are embodiment-specific—a policy trained on one robot typically fails to generalize to another, even with minor changes in body size or camera viewpoint. As custom hardware becomes increasingly common, there is a growing need for a single policy that generalizes across embodiments, eliminating the need to (re-)train for each specific robot. In this paper, we introduce RING <u>(</u> **<u>R</u>** <u>obotic</u> **<u>I</u>** <u>ndoor</u> **<u>N</u>** <u>avigation</u> **<u>G</u>** <u>eneralist), an embodiment-agnostic policy that turns any mo-</u> bile robot into an effective indoor semantic navigator. Trained entirely in simulation, RING leverages large-scale randomization over robot embodiments to enable robust generalization to many real-world platforms. To support this, we augment the AI2-THOR simulator to instantiate robots with controllable configurations, varying in body size, rotation pivot point, and camera parameters. On the visual object-goal navigation task, RING achieves strong cross-embodiment (XE) generalization—72.1% average success rate across 5 simulated embodiments (a 16.7% absolute improvement on the CHORES-S benchmark) and 78.9% across 4 realworld platforms, including Stretch RE-1, LoCoBot, and Unitree Go1—matching 

or even surpassing embodiment-specific policies. We further deploy RING on the RB-Y1 wheeled humanoid in a real-world kitchen environment, showcasing its out-of-the-box potential for mobile manipulation platforms. 

## **1 Introduction** 

Robot embodiments are diverse and are constantly evolving to better suit new environments and tasks. This range in body configurations—differences in size, shape, wheeled or legged locomotion, and sensor configurations—not only shapes how robots perceive the world but also how they act in it. A robot with a wide field of view (FoV) or multiple cameras can scan its surroundings quickly, while one with a narrower view might need to more actively explore a room. A small robot can squeeze through tight spaces, a low-profile one can duck under furniture, and a larger robot may need to follow more conservative routes. The influence of embodiment on behavior means a policy trained on one design, or even several, often does not perform well out of domain. 

There has been progress towards scalable cross-embodiment training [1, 2, 3, 4, 5]. While these methods demonstrate some transfer to unseen embodiments, they still suffer from performance degradation with relatively small changes in embodiment (e.g., camera pose modification on the same robot) [6, 7]. Potentially, this is due to these methods relying on the small amount of real-world data available in public datasets-around 20 embodiments in total [1]. Similarly, general-purpose navigation policies [8, 9, 10] are trained on datasets with relatively few embodiments (e.g., 8 robots in [9]), limiting their generalization. A more comprehensive solution is needed—one that can robustly handle the full spectrum of possible embodiments without retraining or additional adaptation. 

We introduce RING, a **<u>R</u>** <u>obotic</u> **<u>I</u>** <u>ndoor</u> **<u>N</u>** <u>avigation</u> **<u>G</u>** <u>eneralist.</u> RING is trained _exclusively in simulation_ , without any use of real-world robot embodiments. In other words, all robot platforms we evaluate on (i.e., Stretch RE-1, LoCoBot, Unitree’s Go1, RB-Y1) are _unseen_ by RING during training. We leverage simulation to randomly sample **1 Million** agent body configurations, varying the robot’s camera parameters, collider sizes, and center of rotation. Concretely, each embodiment consists of a collider box of varying dimensions and cameras with randomized parameters, placed randomly within the collider box. Fig.1-A presents a t-SNE[11] visualization of body parameters for 30k such agents. Our approach builds on the success of prior works that achieve strong real-world performance through large-scale simulation-only training [12, 13, 14]. Simulation enables training across a vast distribution of environments (150k ProcTHOR houses [15]) and objects (40k+ 3D objects in Objaverse [16]) in the AI2-THOR simulator. Extensive domain randomization on visual observations and the use of pre-trained visual encoders then allows simulation-trained policies to bridge the sim-to-real gap. We follow the training procedure in FLaRe [14], first training our policy on expert trajectories collected from 1M randomized embodiments and subsequently fine-tuning it with on-policy reinforcement learning (RL) in the simulator. 

Our results demonstrate generalization to _truly unseen embodiments_ . RING transfers to diverse realworld embodiments without any adaptation, despite being trained entirely in simulation without access to the real robot configurations. We evaluate in a zero-shot setting across Stretch RE-1, LoCoBot, Unitree’s Go1, RB-Y1 wheeled humanoid, and even “Navigation Assistants,” where a human user captures ego-centric observations on their phone and prompts RING to predict actions. RING achieves 72 _._ 1% average success rate in simulation (16.7% absolute improvement on CHORES-S benchmark) and 78 _._ 9% on real robot platforms—matching or even surpassing embodiment-specific policies. RING can be further adapted to an _embodiment-specialized_ policy with even better performance (up to 10% absolute improvement) with minimal finetuning. RING is easy to install, and is ready for use by the community. We will release our pretrained models, code, and data. 

## **2 Related work** 

**Cross-embodiment.** Cross-embodiment training has received substantial attention from the research community. Arguably the most representative of a large body of recent work [4, 3, 17, 5, 18, 

2 

19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29], Open-X-Embodiment (OXE) [30] is the fruit of a large collaboration to cover many robotic tasks, with special emphasis in manipulation. Its usage in RTX results in a notable performance gain in emergent skill evaluations in comparison to RT-2 [31]. Despite the 1.5 million trajectories across 22 embodiments present in their dataset, the enormous cost of data collection in the real world makes further scaling challenging. CrossFormer [3] trains a transformer-based policy on 900k trajectories spanning 30 robots, drawing from OXE, navigation data from GNM [8], manipulation data from DROID [32], and additional sources. However, the limited diversity of embodiments and focus on low-level control highlight the need for denser embodiment coverage. GET-zero [33], focused on dexterous manipulation, incorporates embodiment structure via a connectivity graph to guide attention. In contrast, we generate an arbitrarily large set of randomized embodiments during training, allowing our policy to generalize zero-shot to novel embodiments without requiring access to their structure. 

**Foundational navigation policies** Following the success in recent developments for point-goal navigation [34], locomotion [35, 36, 37, 38], agile control [39], exploration [40, 41, 42], and social navigation [43], comparable results in more nuanced tasks like semantic or object-goal navigation (ObjectNav) [44, 45, 46, 47, 48, 49, 50, 51] remain elusive due to a lack of efficient exploration and semantic understanding capabilities. Recently, with powerful pretrained vision models [52, 53] and large-scale procedurally generated virtual environments [16], notable progress in end-to-end ObjectNav policy learning _for specific embodiments_ has been achieved by means of imitation learning (IL) from shortest-path trajectories [12], RL [13], or combinations thereof [14]. In image-goal navigation, NoMaD [10], which extends ViNT [9], uses a diffusion policy to control a single embodiment. With the same goal in mind, GNM [8] trains navigation policies across 6 embodiments using IL. In contrast, our policy benefits from RL fine-tuning, improving robustness to compounding errors. Leveraging large-scale training with randomized embodiments in simulation, RING learns a single policy that generalizes to _any_ embodiment, including _truly_ unseen robot platforms in the real world. Unlike NoMaD, ViNT, GNM, and Mobility VLA [54], which rely on topological map or graph reconstruction for high-level planning, our approach is fully end-to-end and can explore dynamic novel scenes without requiring an explicit map. While prior work [55, 56, 57] has explored embodimentagnostic policies using LLMs or VLMs, these methods are limited to short-horizon navigation and single-step prediction. In contrast, RING incorporates temporal context via a transformer decoder. 

## **3 RING** 

With the growing diversity of robots used in research labs and real-world applications, there remains a need for a policy that can operate a wide range of embodiments and transfer, in a zero- or few-shot manner, to unseen robots. We introduce RING, a generalist policy for indoor visual navigation that _learns from a broad spectrum of embodiments, trained exclusively in simulation, without any direct use of actual robot embodiments_ . We show that training on an extensive range of _∼_ 1M random embodiments results in a robust navigation policy, enabling zero-shot transfer to unseen real-world robots. To train RING, we define the space of random embodiments (Sec. 3.2), enable generation of expert trajectories for random embodiments in simulation (see Appendix 8), and use state-of-the-art architecture designs (Sec. 3.3) to train with a combination of IL and RL methods (Sec. 3.4). 

### **3.1 Problem formulation** 

We define the space of possible embodiments as _E_ , where each embodiment _e ∈ E_ is characterized by a configuration vector **c** _e_ , including parameters such as camera settings, agent collider size, and center of rotation. Each task can be modeled as a Partially Observable Markov Decision Process (POMDP), denoted as ( _S, A, E, Oe, Te, R, L, P_ ( _s_ 0) _, γ_ ), where _S_ and _A_ are the state and action spaces. The observation space _Oe_ varies across embodiments due to differences in camera parameters. The observation at time _t_ for embodiment _e_ , _ot_<sup>_e_=</sup><sup>_Oe_(</sup><sup>_st,_</sup><sup>**c**</sup><sup>_e_),is a function of both the state</sup><sup>_st_</sup> and embodiment parameters **c** _e_ . Given an action _at_ , the next state follows the transition dynamics _st_ +1 _∼ Te_ ( _st_ +1 _|st , at ,_ **c** _e_ ), which depends on the embodiment (due to variations in collider size and 

3 

rotation center). Fig. 2 shows trajectories from two different embodiments starting at the same location and following the same sequence of actions. They have distinct visual observations and follow different transition dynamics—one agent moves under the table, while the other collides with it. 

Except where otherwise specified, we assume that all embodiments share the same discrete action space _{_ MoveBase(±20cm), RotateBase(±6<sup>_◦_</sup> , ±30<sup>_◦_</sup> ), Done _}_ . These actions are executed using robot-specific low-level controllers during deployment. This simple and platform-agnostic action space enables effective cross-embodiment (XE) transfer, as demonstrated across both holonomic and differential-drive robots in our experiments. Investigating more expressive XE action spaces beyond this sufficient version is left for future work. 

### **3.2 Embodiment randomization at scale** 

Domain randomization [58] is a class of methods in which policies are trained across a wide range of simulated _environmental_ parameters; the aim is to enable robustness to unseen environments. Our approach is complementary yet orthogonal; we apply embodiment randomization to train policies on a diverse set of _robot body_ parameters, enabling robust deployment to unseen real-world robots. 

|Parameters|TrainingRange|
|---|---|
|Collider Size (_αx,αy,αz_)|[0_._2_,_0_._5],[0_._3_,_1_._5],[0_._2_,_0_._5]|
|Rotation Center (_ox,oy,oz_)<br>[_−αx/_|2_,αx/_2],[_−αy/_2_,αy/_2],[_−αz/_2_,αz/_2]|
|Vertical FoV (cam1_,_cam2)|[40_,_100],[40_,_100]|
|Horizontal FoV (cam1_,_cam2)|[40_,_120],[40_,_120]|
|Camera Pitch (cam1)|[_−_20_,_40]|
|Camera Pitch (cam2)|[_−_20_,_60]|
|Camera Yaw (cam1_,_cam2)|always 0,[0_,_360]|
|Camera Position (x) (cam1_,_cam2)|[_−αx/_2_,αx/_2],[_−αx/_2_,αx/_2]|
|Camera Position (y) (cam1_,_cam2)|[0_._3_,αy_],[0_._3_,αy_]|
|Camera Position (z) (cam1_,_cam2)|[_−αz/_2_,αz/_2],[_−αz/_2_,αz/_2]|
|RGB dimensions(H,W)|[112_,_448], [112_,_448]|


Table 1: **Random Embodiment Parameters.** 1M embodiments are sampled from these ranges. 

We model the body of the agent as an invisible collider box in the AI2-THOR [59] simulator. Each agent can have 1 or 2 RGB cameras placed t=1 t=1 at a random pose within the collider box. Parameters corresponding to both the body and the cameras are sampled randomly from the ranges t=2 t=2 specified in Tab. 1. We also modify the process of generating expert trajectories to account t=3 t=3 for the diversity of embodiments, for details see Appendix 8. Below, we detail the parameters t=4 t=4 varied in our embodiment randomization: **Col-** Embodiment <mark>A</mark> Embodiment <mark>B</mark> **lider size** ( _αx, αy, αz_ ). The agent’s body is modFigure 2: **Different embodiments exhibit different** eled as a collider box. We use three scale factors **behaviors.** We show egocentric view from the main ( _αx, αy, αz_ ) to scale the box along _x, y, z_ axis. **Ro-** camera and third-person view of the 2 agents–white boxes indicate the robot colliders. Embodiment B can **tation center (** _ox, oy, oz_ **)** . These coordinates dego under the table to get to the chair but Embodiment fine the agent’s pivot point. While this center is A collides with the table and has to go around. typically near (0,0), it can vary across different robots. We sample _ox_ from the range [ _−_<sup>_<u>α</u>_</sup> 3<sup>_<u>x</u>,_</sup><sup>_<u>α</u>_</sup> 3<sup>_<u>x</u>_] and</sup><sup>_oy_from the range [</sup><sup>_−α_</sup> 3<sup>_<u>y</u>,α_</sup> 3<sup>_<u>y</u>_], with the sampling</sup> ranges determined by the collider size. **Camera parameters** . Each agent is equipped with two RGB cameras placed within the collider box. We randomize several camera parameters, including position, rotation, FoV, and aspect ratio. While the first camera always faces forward, the second camera can rotate up to 360<sup>_◦_</sup> in _z_ -axis, enabling it to face forward, to the sides, or backward. 

### **3.3 Architecture** 

With this rich dataset of expert trajectories for random embodiments, a deep, high-capacity architecture is essential to learn a robust policy (Fig. 3). At each timestep, RING uses _N_ RGB images (one per camera) and a language instruction _l_ to predict an action distribution over a discrete action space. To account for different dimensions, we pad the RGB 


Figure 3: **RING model architecture** . It accepts visual observations and a language instruction as inputs and predicts an action to execute. At RL finetuning, RING also predicts a value estimate. 

4 

|Model|Loss|Train Embodimen|t|Benchmark|Embodiment: Success|(SEL)|||
|---|---|---|---|---|---|---|---|---|
||||**Stretch**|**Stretch**(Nav Cam) **S**|**tretch**(Factory Config)|**LoCoBot**|**Unitree A1**|<br>Average|
|SPOC [12]<br>SPOC-2_._3M|IL only|Stretch|57.0 (38.1)*<br>60.0 (30.3)*|37.9 (19.0)<br>37.5 (17.9)|33.0 (19.3)<br>46.0 (19.4)|16.2 (5.4)<br>24.0 (7.9)|2.1 (1.6)<br>10.0 (5.2)|29.2 (16.7)<br>35.5 (16.1)|
|||Stretch|81.0 (58.1)*|65.0 (35.5)|47.5 (25.6)|27.5 (14.8)|42.6 (25.1)|52.7 (31.8)|
|POLIFORMER[13]|RL only|LoCoBot<br>Unitree A1|56.0 (32.9)<br>40.0 (25.2)|56.5 (34.7)<br>39.0 (22.5)|52.0 (27.7)<br>35.5 (20.9)|61.5 (44.7)* <br>30.0 (17.4)|50.5 (34.2) <br> 55.3 (48.2)*|55.4 (34.9)<br>  40.0 (26.8)|
|FLARE [14]|IL + RL|Stretch|82.0 (63.5)*|55.5 (37.9)|38.0 (19.6)|21.5 (10.9)|27.0 (15.1)|44.8 (29.4)|
|RING-ZERO-SHOT|IL + RL|RING-Random|**76.0 (55.9)**|**74.0 (52.5)**|**72.0 (52.7)**|**66.5 (45.3)**|**72.0 (58.6) **|**72.1 (53.0)**|


Table 2: **Zero-shot Results.** RING shows zero-shot generalization to four unseen embodiments. Unless otherwise specified, “Stretch” refers to the two-camera variant of the RE-1 platform, used in[12]. All prior methods fail to generalize effectively to embodiments beyond those seen during training. Gray* numbers indicate evaluation on the training embodiment; all others reflect zero-shot performance on unseen embodiments. 

observations to square and resize to 256 _×_ 256 be- 

fore feeding them to the model. RING’s architecture, inspired by PoliFormer [13], consists of a Visual Encoder, a Goal Encoder, a Transformer State Encoder, and a Causal Transformer Decoder with a linear actor-critic head. The Visual and Goal Encoders are frozen pre-trained models (a ViT and a language model, respectively) that encode the RGB observations and instruction _l_ into visual and goal token embeddings. Projections of these embeddings, along with a special STATE token vector, are stacked along the token axis and processed by the multi-layer Transformer State Encoder, which summarizes the observations at each timestep as the state embedding corresponding to the STATE token. Finally, the Causal Transformer Decoder performs explicit memory modeling over time, producing the current belief by causal attention on the state embeddings stacked along the temporal axis. The linear actor-critic head further predicts action logits over the action space as well as a value estimate. (More details in Appendix 10) 

### **3.4 Training paradigm** 

We adopt the training recipe of pretraining our policy on expert trajectories collected from randomized embodiments (Sec. 3.2), followed by finetuning with on-policy RL using the randomized embodiments in the AI2-THOR simulator [59]. 

**Large-scale imitation learning with random embodiments:** We train our policy using expert trajectories collected from 1M randomized embodiments across 50k procedurally generated PROCTHOR houses [15], containing approximately 40k annotated 3D objects [60]. At each time step, the linear actor-critic head in the Causal Transformer Decoder predicts action logits, and a cross-entropy loss is computed between the predicted logits _π_<sup>_t_</sup> and the expert action. We use a batch size of 240 trajectories, each with a temporal context window of 100 steps. Training is conducted on 8 _×_ H100 GPUs (80 GB each) using the AdamW optimizer with a learning rate of 2 _·_ 10<sup>_−_4</sup> for 80k iterations. 

**Large-scale RL finetuning with random embodiments:** Following the training recipe in FLaRe [14], we perform large-scale RL fine-tuning using AllenAct [61] on randomized embodiments in simulation. This fine-tuning phase is critical for enabling the policy to learn through trial and error how to navigate diverse embodiments. We use DD-PPO with 64 parallel environments and 128 rollout steps across 4 machines (each with 8 _×_ H100 GPUs), training for 40M steps using the AdamW optimizer with a learning rate of 2 _·_ 10<sup>_−_5</sup> . As in FLaRe [14], we disable the entropy term in the PPO loss to prevent catastrophic forgetting. For fair comparison, we adopt the reward function from [15]: _rt_ = max (0 _, min_ ∆0: _t−_ 1 _−_ ∆ _t_ )+ _st − ρ_ , where min ∆0: _t−_ 1 is the minimum L2 distance between the agent and the target object up to time _t−_ 1, ∆ _t_ is the current L2 distance, _st_ is a success reward, and _ρ_ = 0 _._ 01 is a step penalty encouraging task efficiency. The agent must explicitly issue Done to receive the success reward ( _st_ = 10); otherwise, _st_ = 0. 

## **4 Experiments** 

Our experiments show that RING operates effectively across a wide range of embodiments, including _Stretch RE-1_ , _LoCoBot_ , _Unitree Go1_ , and _RB-Y1_ , despite being trained exclusively in simulation 

5 

**without** any direct exposure to real robot embodiments. Our key results are: 1) RING generalizes **zero-shot** to 5 _truly_ unseen embodiments, despite never being trained on them, and achieves state-of-the-art performance across multiple benchmarks (Sec. 4.1). 2) Our policy, trained solely in simulation on randomized embodiments, transfers directly to the **real-world** , on 5 real robots and as navigation assistants (Sec. 4.2). _(Videos in supplementary)_ 3) RING can be easily adapted to **embodiment-specialized** policies with minimal finetuning. It achieves better performance on each specific robot (Sec. 4.3). 4) RING shows **embodiment-adaptive behavior** , adjusting its strategies based on the agent’s body (Sec. 4.4). 5) We perform a **collision analysis** showing that RING remains as safe— _and in some cases even safer_ —than embodiment-specific policies(Sec. 4.5). 

### **4.1 RING generalizes zero-shot to unseen embodiments** 

We perform zero-shot evaluations of all policies on four robot embodiments: Stretch RE-1 (with 1 or 2 cameras), LoCoBot, and Unitree A1 in simulation. 

**Baselines.** We select prior works from both imitation learning (IL) and reinforcement learning (RL) for comparison. Each baseline is trained on a specific embodiment and evaluated in a zero-shot setting across four different embodiments. SPOC [62] is a supervised IL baseline trained on shortestpath expert trajectories in AI2-THOR. PoliFormer [13] is a state-of-the-art transformer-based policy for object goal navigation, trained from scratch using RL. FLaRe [14] combines IL and RL for efficient policy fine-tuning. All baselines use similar architectures and comparable data, except for SPOC (reason to include SPOC 2.3M). Specifically, SPOC [12] (SPOC-2 _._ 3M) is trained with IL on Stretch RE-1 using 100k (2 _._ 3M) expert trajectories; Poliformer [13] is trained from scratch on each embodiment individually over 300M RL steps (more than other baselines in terms of training frames); and FLaRe [14] finetunes SPOC on Stretch RE-1 with an additional 20M RL steps. 

**Experimental details.** RING is first trained with IL on 1M expert trajectories collected from randomized embodiments in simulation, followed by finetuning with RL for an additional 40M steps on the randomized embodiments. _Note that all four target embodiments were unseen during training_ . We evaluate on the navigation benchmark in CHORES-S [12], a simulation benchmark for household robot with 200 tasks across 200 scenes. For Unitree A1, we create a new, similar benchmark with 200 tasks adjusted for the robot’s lower height to ensure that all targets are feasible. 

**Results.** Tab. 2 presents the zero-shot evaluation of all policies across four embodiments. We compare _Success Rate_ and _Success Weighted by Episode Length (SEL [45])_ , a metric measuring efficiency. The results indicate that all single-embodiment baselines struggle to generalize effectively to new embodiments, with performance declining as embodiment differences increase. In contrast, RING exhibits strong generalization across all embodiments, despite not being trained on any of them, achieving an average absolute improvement of 16 _._ 7% in Success Rate. In some cases, it outperforms the baseline trained on the target embodiment: PoliFormer trained on LoCoBot _(_ 61 _._ 5 _→_ 68 _._ 5 _)_ and Unitree A1 (55 _._ 3 _→_ 72 _._ 0). These 2 more challenging embodiments (lower FoV, low camera placement) make RL from scratch less effective. RING benefits from more efficient learning by training across random embodiments at scale with more diverse navigation behaviors. 

### **4.2 RING transfers to real-world embodiments despite being purely trained in simulation** 

**Robot evaluation.** We zero-shot evaluate our policy on 4 unseen robots in a multi-room real-world apartment (Fig.6) without any real-world-specific finetuning (Tab. 3). We use the same evaluation set of 15 tasks for LoCoBot[15, 63, 13] (3 start poses × 5 targets) and 18 tasks for Stretch RE1 [12, 13, 14] (3 poses × 6 goals). For Unitree Go1, we create a new set with 3 start poses and 4 objects ( _toilet, sofa, TV, trashcan_ ) placed to match its lower viewpoint. RING matches or outperforms specialized policies, likely due to cross-embodiment (XE) training enabling robust sim-to-real transfer in the presence of real-world noise. We also deploy RING on the RB-Y1 wheeled humanoid in an unstructured kitchen, where it successfully navigates to targets ( _trashcan, apple, houseplant, mug_ ) at two different heights (standing/seated), using an iPhone 16 Pro camera mounted on the robot to stream visual observations (Fig. 1-B). ( _More detail in Appendix 7.1 & videos in supplementary._ ) 

6 

|Model<br>|Train Embodiment||Eval E|mbodiment||Model|Train Embodiment|Object <sup>Human</sup>|<sup>Participa</sup>|<sup>nt</sup>|<sup>s</sup>|
|---|---|---|---|---|---|---|---|---|---|---|---|
|||**Stretch S**|**tretch (FC)**|**LoCoBot**|**Unitree Go1**|||**H1 H2**|**H3 H4 **|**H**|**5** Average|
|SPOC [62]|Stretch|50.0|-|-|-|||✓<br>✗|✗<br>✗|✗||
||Stretch|83.3|33.3|-|-|FLARE [14]|Stretch RE-1|✗<br>✓|✓<br>✓<br>|✓|40.0%<br>|
|POLIFORMER[13]|LoCoBot|-|-|80.0|-|||✗<br>✗|✗<br>✗<br>|✓||
||Unitree Go1|-|-|-|41.7|||✓<br>✗|✗<br>✗<br>|✓||
|FLARE [14]|Stretch|**94.4**|-|-|-|RING-ZERO-SHOT|RING-Random|✓<br>✓|✓<br>✓<br>|✓|**73.3%**<br>|
|RING-ZERO-SHOT|RING-Random|83.3|**72.2**|**80.0**|**80.0**|Tbl4<br>|**E**|✗<br>✓<br>**ti**|✓<br>✓<br><br>Fi|✓<br>|idii|


Table 4: **Human Evaluation.** Five individuals navigate to 3 different objects ( Apple, Houseplant,Mug) following the policy’s output actions on their phones in a kitchen area (see Fig. 10). 

Table 3: **Real-world Results** . RING transfers zeroshot to the real-world without any finetuning. Gray numbers are evaluated on same training embodiment. 


Figure 4: RING exhibits **embodiment-adaptive** behavior, adjusting its navigation strategy based on the robot’s physical configuration. The shorter quadruped robot (B) walks under the bed, while the taller StretchRE1 (A) navigates around it. In (C), an agent with the same height as Stretch-RE1 but a lower camera position initially attempts to go under the bed, mistakenly assuming it can fit. After a collision, it adapts and reroutes around the bed, similar to Stretch-RE1. 

**Human evaluation.** To further show RING’s generalization to unseen embodiments, we evaluate our policy as a navigation assistant with humans as novel embodiments. Five participants navigated a real-world kitchen by following policy outputs on their phones. Each had unique characteristics (e.g., step size, height, rotation, camera posture) and was tasked with reaching three objects (Mug, Apple, Houseplant), yielding 15 trajectories. We compare RING to FLaRe [14], trained only on Stretch RE-1. As shown in Tab.4, RING consistently outperforms FLaRe across objects and users. Fig.10 shows two qualitative examples (more in Appendix 7.2). 

### **4.3 RING can efficiently adapt to an embodiment-specialized policy with minimal finetuning** 

Although RING generalizes zero-shot across diverse embodiments, some scenarios benefit from embodimentspecialized policies for optimal performance. Here, we show that RING can be easily adapted to a _robotspecialized policy_ through minimal fine-tuning. **Baselines.** We compare with FLaRe [14], which demonstrates effective adaptation to new tasks and 


Figure 5: **Embodiment-Specialized Adaptation.** RING, pretrained on randomized embodiments, adapts efficiently to individual robots with minimal fine-tuning. 

embodiments. It is pretrained on Stretch RE-1 and finetuned on each of the three test embodiments using up to 20M RL steps. **Implementation.** We finetune RING, pretrained on randomized embodiments, on each robot for up to 20M RL steps, using the same hyperparameters as FLaRe for fair comparison. Following FLaRe, we repurpose RotateBase(±6<sup>_◦_</sup> ) to TiltCamera(±30<sup>_◦_</sup> ) for LoCoBot, enabling camera control not available during zero-shot evaluation. **Results.** As shown in Fig. 5, RING adapts efficiently, achieving superior performance with minimal fine-tuning. For LoCoBot and Unitree-A1, FLaRe underperforms compared to Stretch RE-1, suggesting that pretraining on a single embodiment limits generalizability. This underscores the value of policies like RING that can adapt quickly and consistently to new embodiments. 

7 

|Model<br>|Train Embodimen|t<br>S|afe Episo|de_↑_|Model Col|lision Pen|lt|Metrics||
|---|---|---|---|---|---|---|---|---|---|
|||**Stretch **|**LoCoBot **|**Unitree A1**|||y<br>Success_↑_|SEL_↑_SC_↑_CR_↓_Sa|fe Episode_↑_|
|POLIFORMER[13]|Stretch<br>LoCoBot<br>Unitree A1|45.0<br>-<br>-|-<br>42.0<br>-|-<br>-<br>**49.25**|RING|✗<br>✓|**67.62**<br>66.33|56.24 42.53 7.77<br>**56.87 49.05 4.03**|46.90<br>**60.57**|
|FLARE[14]|Stretch|62.0|-|-|Table 6|: **Collisi**|**on Penalt**|**y.** Adding a sma|ll col-|
|RING-ZERO-SHOT|RING-Random|**67.0**|**64.5**|48.5|lii|<br>l0|<br>1h|<br>dfi|<br>l|


Table 6: **Collision Penalty.** Adding a small collision penalty (0.1) to the reward function results in 50% less collision, forcing the policy to be even more conservative. 

Table 5: RING has more **Safe Episodes** (with no collisions) compared to embodiment-specific baselines. 

### **4.4 RING changes its behavior across different embodiments** 

Ideally, an optimal policy would modify its behavior depending on the embodiment. For instance, a thinner robot can navigate through narrow hallways or under furniture, and a wider agent may need to take more conservative paths. Our qualitative results show that RING exhibits embodimentadaptive behavior. In Fig. 4-A,B, both Stretch RE-1 and Unitree A1 begin behind a bed. The lowprofile quadruped moves directly under it, while Stretch RE-1 navigates around—demonstrating that RING _implicitly_ infers embodiment characteristics from visual input, without access to privileged body information. Visual input reveals cues like camera specs and, in some cases, the agent’s height. However, vision alone can be ambiguous, prompting the agent to rely on physical interactions—such as collisions—to refine its understanding. (Collision feedback may come from actual impacts or from sensors that anticipate collisions before they occur.) In Fig. 4-C, an agent with a low-mounted camera but tall body misjudges its own height, initially attempts to go under the bed, collides, and then reroutes like Stretch RE-1. This behavior is not present in the expert data but emerges during reinforcement learning through training across diverse embodiments. _(Videos in supplementary)_ 

### **4.5 Collision analysis** 

RING is trained with randomized body dimensions and is not explicitly provided with real embodiment information. Regardless, the learned policy remains as safe— _and in some cases even safer_ —than embodiment-specific policies (Tab. 5). Collision-avoidance behavior can be further improved by incorporating a small collision penalty into the RL reward (Tab. 6). 

**RING learns to take conservative paths without explicit knowledge of its collider size.** Expert trajectories are generated using A*, finding minimum-cost paths where the cost is defined as the inverse of the Euclidean distance to the nearest obstacles. During reinforcement learning, collisions slow down the agent’s progress, leading to lower rewards through a step penalty. Since collisions cause no meaningful state changes and only waste time, the policy learns to avoid them to complete tasks more efficiently. We evaluate RING against embodiment-specific baselines using the metric _Safe Episodes_ —the percentage of episodes completed without any collisions. As shown in Tab. 5, RING achieves a higher percentage of Safe Episodes compared to the baselines. By training across a large number of embodiments and without access to exact body size information, RING learns to take more conservative actions through reinforcement learning, promoting safer navigation. 

**Include collision penalty to take safer routes.** Adding a small collision penalty of 0 _._ 1 to the reward function can further reduce collision rate ( _CR_ ) by 50%. The resulting policy is more conservative, regardless of embodiment size. To quantify these results, we created a custom benchmark similar to CHORES-S [12], consisting of 2 _,_ 000 random embodiments across 2 _,_ 000 scenes. We evaluate 2 different versions of our policy on this benchmark, comparing metrics such as _Success Rate_ , _Success Weighted by Collision (SC)_ , _Collision Rate (CR)_ , and _Safe Episode_ . As shown in Tab. 6, adding the collision penalty reduces the collision rate (CR) (7 _._ 77% _→_ 4 _._ 03%) as well as increases the percentage of trajectories without collisions (46 _._ 90% _→_ 60 _._ 57%). 

## **5 Conclusion** 

In this paper, we introduce RING <u>(</u> **<u>R</u>** <u>obotic</u> **<u>I</u>** <u>ndoor</u> **<u>N</u>** <u>avigation</u> **<u>G</u>** <u>eneralist), an embodiment-agnostic</u> policy trained entirely in simulation on 1 million diverse, randomly initialized embodiments. RING demonstrates strong zero-shot generalization to unseen embodiments, maintaining consistent per- 

8 

formance across a wide range of robots. It achieves state-of-the-art results on novel embodiments—sometimes even outperforming embodiment-specific policies—and transfers directly to the real world despite never seeing real robot embodiments during training. Finally, RING dynamically adapts its behavior based on its embodiment and interactions with the environment. 

## **6 Limitations** 

Although RING has the advantage of being deployable on a wide range of embodiments without any privileged information about its current body, when available it may be beneficial to have a policy explicitly conditioned on the current embodiment specification. This might lead to improved performance and more desirable behaviors, such as increased efficiency and collision avoidance. 

We train RING-EMB-COND by explicitly providing the embodiment information to the policy. The embodiment parameters are represented as a configuration vector **c** _e ∈_ R<sup>19</sup> , with each dimension corresponding to a specific embodiment parameter listed in Table 1. This information is passed as an additional token to the Transformer State Encoder. We use a simple MLP to project **c** _e_ to the desired feature dimension _e ∈_ R<sup>1</sup><sup>_×_512</sup> before passing it to the encoder. Tab. 7 evaluates the 2 versions of the policy on our custom benchmark consisting of 2 _,_ 000 random embodiments across 2 _,_ 000 scenes, comparing metrics such as _Success Rate_ , _Success Weighted by Collision (SC)_ , _Collision Rate (CR)_ , and _Safe Episode (percentage of episodes without any collisions)_ . 

The results do not show a clear benefit to conditioning the policy on embodiment information. This could be due to several reasons. It is possible that most relevant information about environment hazards and agent motion can be already inferred from visual observations. It is also possible that a significant fraction portion of collisions (both with an without embodiment specification provided) occur with objects that never enter the agent’s visual field, in which case extra information about its own embodiment would not help. Alternatively, a more effective method for conditioning the policy on the parameters may exist. Future work should explore this with additional examination of agent-environment collision and designing improved policy architectures to better integrate embodiment parameters, ultimately training a more efficient and robust policy that explicitly incorporates embodiment information. 

|Model|Ablations|Success_↑_|SEL_↑_|SC_↑_CR_↓_|Safe Episode_↑_|
|---|---|---|---|---|---|
||Embodiment Parameters|||||
|RING|✗|67.62|56.24|42.53 **7.77**|**46.90**|
|RING-EMB-COND|✓|**69.44**|**57.42 **|**44.69**<br>8.0|46.54|


Table 7: **Conditioning RING on embodiment parameters** . We explicitly provide the embodiment parameters to the policy (RING-EMB-COND) and compare with RING without any information about the embodiment. Both policies are evaluated on a custom benchmark consisting of 2000 random embodiments in 2000 scenes. 

9 

## **References** 

- [1] A. O’Neill, A. Rehman, A. Gupta, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, et al. Open x-embodiment: Robotic learning datasets and rt-x models. _arXiv preprint arXiv:2310.08864_ , 2023. 

- [2] O. M. Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- [3] R. Doshi, H. Walke, O. Mees, S. Dasari, and S. Levine. Scaling cross-embodied learning: One policy for manipulation, navigation, locomotion and aviation. _arXiv preprint arXiv:2408.11812_ , 2024. 

- [4] J. Yang, C. Glossop, A. Bhorkar, D. Shah, Q. Vuong, C. Finn, D. Sadigh, and S. Levine. Pushing the Limits of Cross-Embodiment Learning for Manipulation and Navigation. In _arXiv preprint arXiv:2402.19432_ , 2024. 

- [5] L. Wang, X. Chen, J. Zhao, and K. He. Scaling proprioceptive-visual learning with heterogeneous pre-trained transformers. In _NeurIPS_ , 2024. 

- [6] W. Pumacay, I. Singh, J. Duan, R. Krishna, J. Thomason, and D. Fox. The colosseum: A benchmark for evaluating generalization for robotic manipulation. _arXiv preprint arXiv:2402.08191_ , 2024. 

- [7] A. Xie, L. Lee, T. Xiao, and C. Finn. Decomposing the generalization gap in imitation learning for visual robotic manipulation. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 3153–3160. IEEE, 2024. 

- [8] D. Shah, A. Sridhar, A. Bhorkar, N. Hirose, and S. Levine. Gnm: A general navigation model to drive any robot. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 7226–7233. IEEE, 2023. 

- [9] D. Shah, A. Sridhar, N. Dashora, K. Stachowicz, K. Black, N. Hirose, and S. Levine. ViNT: A foundation model for visual navigation. _arXiv preprint arXiv:2306.14846_ , 2023. 

- [10] A. Sridhar, D. Shah, C. Glossop, and S. Levine. Nomad: Goal masked diffusion policies for navigation and exploration. In _ICRA_ , 2023. 

- [11] L. Van der Maaten and G. Hinton. Visualizing data using t-SNE. _Journal of machine learning research_ , 9(11), 2008. 

- [12] K. Ehsani, T. Gupta, R. Hendrix, J. Salvador, L. Weihs, K.-H. Zeng, K. P. Singh, Y. Kim, W. Han, A. Herrasti, et al. SPOC: Imitating Shortest Paths in Simulation Enables Effective Navigation and Manipulation in the Real World. In _CVPR_ , pages 16238–16250, 2024. 

- [13] K.-H. Zeng, Z. Zhang, K. Ehsani, R. Hendrix, J. Salvador, A. Herrasti, R. Girshick, A. Kembhavi, and L. Weihs. PoliFormer: Scaling On-Policy RL with Transformers Results in Masterful Navigators. In _CoRL_ , 2024. 

- [14] J. Hu, R. Hendrix, A. Farhadi, A. Kembhavi, R. Martin-Martin, P. Stone, K.-H. Zeng, and K. Ehsan. FLaRe: Achieving Masterful and Adaptive Robot Policies with Large-Scale Reinforcement Learning Fine-Tuning. _arXiv preprint arXiv:2409.16578_ , 2024. 

- [15] M. Deitke, E. VanderBilt, A. Herrasti, L. Weihs, K. Ehsani, J. Salvador, W. Han, E. Kolve, A. Kembhavi, and R. Mottaghi. ProcTHOR: LargeScale Embodied AI Using Procedural Generation. In _NeurIPS_ , 2022. URL http://papers.nips.cc/paper_files/paper/2022/hash/ 27c546ab1e4f1d7d638e6a8dfbad9a07-Abstract-Conference.html. 

10 

- [16] M. Deitke, D. Schwenk, J. Salvador, L. Weihs, O. Michel, E. VanderBilt, L. Schmidt, K. Ehsani, A. Kembhavi, and A. Farhadi. Objaverse: A Universe of Annotated 3D Objects. _2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 13142–13153, 2022. URL https://api.semanticscholar.org/CorpusID: 

   254685588. 

- [17] Octo Model Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, C. Xu, J. Luo, T. Kreiman, Y. Tan, P. Sanketi, Q. Vuong, T. Xiao, D. Sadigh, C. Finn, and S. Levine. Octo: An Open-Source Generalist Robot Policy. In _RSS_ , 2024. 

- [18] J. Duan, W. Yuan, W. Pumacay, Y. R. Wang, K. Ehsani, D. Fox, and R. Krishna. Manipulateanything: Automating real-world robots using vision-language models. _arXiv preprint arXiv:2406.18915_ , 2024. 

- [19] A. Loquercio, A. I. Maqueda, C. R. Del-Blanco, and D. Scaramuzza. Dronet: Learning to fly by driving. In _RA-L_ , 2018. 

- [20] M. Xu, Z. Xu, Y. Xu, C. Chi, G. Wetzstein, M. Veloso, and S. Song. Flow as the cross-domain manipulation interface. In _CoRL_ , 2024. 

- [21] H. Ha, Y. Gao, Z. Fu, J. Tan, and S. Song. Umi on legs: Making manipulation policies mobile with manipulation-centric whole-body controllers. In _CoRL_ , 2024. 

- [22] J. Hejna, C. Bhateja, Y. Jian, K. Pertsch, and D. Sadigh. Re-Mix: Optimizing Data Mixtures for Large Scale Imitation Learning. In _CoRL_ , 2024. 

- [23] L. Y. Chen, C. Xu, K. Dharmarajan, Z. Irshad, R. Cheng, K. Keutzer, M. Tomizuka, Q. Vuong, and K. Goldberg. Rovi-aug: Robot and viewpoint augmentation for cross-embodiment robot learning. In _CoRL_ , 2024. 

- [24] S. Harithas and S. Sridhar. MotionGlot: A Multi-Embodied Motion Generation Model. _arXiv preprint arXiv:2410.16623_ , 2024. 

- [25] H. Bharadhwaj, R. Mottaghi, A. Gupta, and S. Tulsiani. Track2Act: Predicting Point Tracks from Internet Videos enables Generalizable Robot Manipulation. In _ECCV_ , 2024. 

- [26] K. Kedia, P. Dan, and S. Choudhury. One-Shot Imitation under Mismatched Execution. _arXiv preprint arXiv:2409.06615_ , 2024. 

- [27] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, et al. OpenVLA: An Open-Source Vision-Language-Action Model. In _CoRL_ , 2024. 

- [28] M. Xu, Z. Xu, C. Chi, M. Veloso, and S. Song. Xskill: Cross embodiment skill discovery. In _CoRL_ , 2023. 

- [29] K. Zakka, A. Zeng, P. Florence, J. Tompson, J. Bohg, and D. Dwibedi. Xirl: Cross-embodiment inverse reinforcement learning. In _CoRL_ , 2022. 

- [30] O. X.-E. Collaboration, A. O’Neill, A. Rehman, A. Gupta, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain, A. Tung, A. Bewley, A. Herzog, A. Irpan, A. Khazatsky, A. Rai, A. Gupta, A. Wang, A. Kolobov, A. Singh, A. Garg, A. Kembhavi, A. Xie, A. Brohan, A. Raffin, A. Sharma, A. Yavary, A. Jain, A. Balakrishna, A. Wahid, B. Burgess-Limerick, B. Kim, B. Sch¨olkopf, B. Wulfe, B. Ichter, C. Lu, C. Xu, C. Le, C. Finn, C. Wang, C. Xu, C. Chi, C. Huang, C. Chan, C. Agia, C. Pan, C. Fu, C. Devin, D. Xu, D. Morton, D. Driess, D. Chen, D. Pathak, D. Shah, D. B¨uchler, D. Jayaraman, D. Kalashnikov, D. Sadigh, E. Johns, E. Foster, F. Liu, F. Ceola, F. Xia, F. Zhao, F. V. Frujeri, F. Stulp, G. Zhou, G. S. Sukhatme, G. Salhotra, G. Yan, G. Feng, G. Schiavi, G. Berseth, G. Kahn, G. Yang, G. Wang, H. Su, H.-S. Fang, H. Shi, H. Bao, H. B. Amor, H. I. Christensen, 

11 

   - H. Furuta, H. Bharadhwaj, H. Walke, H. Fang, H. Ha, I. Mordatch, I. Radosavovic, I. Leal, J. Liang, J. Abou-Chakra, J. Kim, J. Drake, J. Peters, J. Schneider, J. Hsu, J. Vakil, J. Bohg, J. Bingham, J. Wu, J. Gao, J. Hu, J. Wu, J. Wu, J. Sun, J. Luo, J. Gu, J. Tan, J. Oh, J. Wu, J. Lu, J. Yang, J. Malik, J. Silv´erio, J. Hejna, J. Booher, J. Tompson, J. Yang, J. Salvador, J. J. Lim, J. Han, K. Wang, K. Rao, K. Pertsch, K. Hausman, K. Go, K. Gopalakrishnan, K. Goldberg, K. Byrne, K. Oslund, K. Kawaharazuka, K. Black, K. Lin, K. Zhang, K. Ehsani, K. Lekkala, K. Ellis, K. Rana, K. Srinivasan, K. Fang, K. P. Singh, K.-H. Zeng, K. Hatch, K. Hsu, L. Itti, L. Y. Chen, L. Pinto, L. Fei-Fei, L. Tan, L. J. Fan, L. Ott, L. Lee, L. Weihs, M. Chen, M. Lepert, M. Memmel, M. Tomizuka, M. Itkina, M. G. Castro, M. Spero, M. Du, M. Ahn, M. C. Yip, M. Zhang, M. Ding, M. Heo, M. K. Srirama, M. Sharma, M. J. Kim, N. Kanazawa, N. Hansen, N. Heess, N. J. Joshi, N. Suenderhauf, N. Liu, N. D. Palo, N. M. M. Shafiullah, O. Mees, O. Kroemer, O. Bastani, P. R. Sanketi, P. T. Miller, P. Yin, P. Wohlhart, P. Xu, P. D. Fagan, P. Mitrano, P. Sermanet, P. Abbeel, P. Sundaresan, Q. Chen, Q. Vuong, R. Rafailov, R. Tian, R. Doshi, R. Mart’in-Mart’in, R. Baijal, R. Scalise, R. Hendrix, R. Lin, R. Qian, R. Zhang, R. Mendonca, R. Shah, R. Hoque, R. Julian, S. Bustamante, S. Kirmani, S. Levine, S. Lin, S. Moore, S. Bahl, S. Dass, S. Sonawani, S. Tulsiani, S. Song, S. Xu, S. Haldar, S. Karamcheti, S. Adebola, S. Guist, S. Nasiriany, S. Schaal, S. Welker, S. Tian, S. Ramamoorthy, S. Dasari, S. Belkhale, S. Park, S. Nair, S. Mirchandani, T. Osa, T. Gupta, T. Harada, T. Matsushima, T. Xiao, T. Kollar, T. Yu, T. Ding, T. Davchev, T. Z. Zhao, T. Armstrong, T. Darrell, T. Chung, V. Jain, V. Kumar, V. Vanhoucke, W. Zhan, W. Zhou, W. Burgard, X. Chen, X. Chen, X. Wang, X. Zhu, X. Geng, X. Liu, X. Liangwei, X. Li, Y. Pang, Y. Lu, Y. J. Ma, Y. Kim, Y. Chebotar, Y. Zhou, Y. Zhu, Y. Wu, Y. Xu, Y. Wang, Y. Bisk, Y. Dou, Y. Cho, Y. Lee, Y. Cui, Y. Cao, Y.-H. Wu, Y. Tang, Y. Zhu, Y. Zhang, Y. Jiang, Y. Li, Y. Li, Y. Iwasawa, Y. Matsuo, Z. Ma, Z. Xu, Z. J. Cui, Z. Zhang, Z. Fu, and Z. Lin. Open X-Embodiment: Robotic Learning Datasets and RT-X Models. In _ICRA_ , 2024. 

- [31] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, X. Chen, K. Choromanski, T. Ding, D. Driess, A. Dubey, C. Finn, P. Florence, C. Fu, M. G. Arenas, K. Gopalakrishnan, K. Han, K. Hausman, A. Herzog, J. Hsu, B. Ichter, A. Irpan, N. J. Joshi, R. Julian, D. Kalashnikov, Y. Kuang, I. Leal, L. Lee, T. E. Lee, S. Levine, Y. Lu, H. Michalewski, I. Mordatch, K. Pertsch, K. Rao, K. Reymann, M. S. Ryoo, G. Salazar, P. Sanketi, P. Sermanet, J. Singh, A. Singh, R. Soricut, H. T. Tran, V. Vanhoucke, Q. Vuong, A. Wahid, S. Welker, P. Wohlhart, J. Wu, F. Xia, T. Xiao, P. Xu, S. Xu, T. Yu, and B. Zitkovich. RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. _CoRR_ , abs/2307.15818, 2023. doi:10.48550/ARXIV.2307.15818. URL https://doi.org/10.48550/arXiv.2307.15818. 

- [32] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis, et al. DROID: A large-scale in-the-wild robot manipulation dataset. In _arXiv preprint arXiv:2403.12945_ , 2024. 

- [33] A. Patel and S. Song. GET-Zero: Graph Embodiment Transformer for Zero-shot Embodiment Generalization. _CoRR_ , abs/2407.15002, 2024. doi:10.48550/ARXIV.2407.15002. URL https://doi.org/10.48550/arXiv.2407.15002. 

- [34] E. Wijmans, A. Kadian, A. Morcos, S. Lee, I. Essa, D. Parikh, M. Savva, and D. Batra. DDPPO: Learning Near-Perfect PointGoal Navigators from 2.5 Billion Frames. In _8th International Conference on Learning Representations, ICLR 2020, Addis Ababa, Ethiopia, April 26-30, 2020_ . OpenReview.net, 2020. URL https://openreview.net/forum?id= H1gX8C4YPr. 

- [35] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath. Real-world humanoid locomotion with reinforcement learning. _Science Robotics_ , 2024. 

- [36] N. Bohlinger, G. Czechmanowski, M. P. Krupka, P. Kicki, K. Walas, J. Peters, and D. Tateo. One Policy to Run Them All: Towards an End-to-end Learning Approach to MultiEmbodiment Locomotion. In _CoRL_ , 2024. 

12 

- [37] M. Shafiee, G. Bellegarda, and A. Ijspeert. Manyquadrupeds: Learning a single locomotion policy for diverse quadruped robots. In _ICRA_ , 2024. 

- [38] C. Ying, Z. Hao, X. Zhou, X. Xu, H. Su, X. Zhang, and J. Zhu. PEAC: Unsupervised Pretraining for Cross-Embodiment Reinforcement Learning. _CoRR_ , abs/2405.14073, 2024. doi: 10.48550/ARXIV.2405.14073. URL https://doi.org/10.48550/arXiv.2405. 14073. 

- [39] W. Xiao, H. Xue, T. Tao, D. Kalaria, J. M. Dolan, and G. Shi. AnyCar to Anywhere: Learning Universal Dynamics Model for Agile and Adaptive Mobility. _arXiv preprint arXiv:2409.15783_ , 2024. 

- [40] D. S. Chaplot, D. Gandhi, S. Gupta, A. Gupta, and R. Salakhutdinov. Learning to explore using active neural slam. _ICLR_ , 2020. 

- [41] B. Yamauchi. A frontier-based approach for autonomous exploration. In _Proceedings 1997 IEEE International Symposium on Computational Intelligence in Robotics and Automation CIRA’97.’Towards New Computational Principles for Robotics and Automation’_ , pages 146– 151. IEEE, 1997. 

- [42] J. Ye, D. Batra, A. Das, and E. Wijmans. Auxiliary Tasks and Exploration Enable ObjectNav. _CoRR_ , abs/2104.04112, 2021. URL https://arxiv.org/abs/2104.04112. 

- [43] X. Puig, E. Undersander, A. Szot, M. D. Cote, T. Yang, R. Partsey, R. Desai, A. W. Clegg, M. Hlavac, S. Y. Min, V. Vondrus, T. Gervet, V. Berges, J. M. Turner, O. Maksymets, Z. Kira, M. Kalakrishnan, J. Malik, D. S. Chaplot, U. Jain, D. Batra, A. Rai, and R. Mottaghi. Habitat 3.0: A Co-Habitat for Humans, Avatars and Robots. _CoRR_ , abs/2310.13724, 2023. doi:10.48550/ARXIV.2310.13724. URL https://doi.org/10.48550/arXiv. 2310.13724. 

- [44] D. Batra, A. Gokaslan, A. Kembhavi, O. Maksymets, R. Mottaghi, M. Savva, A. Toshev, and E. Wijmans. ObjectNav Revisited: On Evaluation of Embodied Agents Navigating to Objects. _CoRR_ , abs/2006.13171, 2020. URL https://arxiv.org/abs/2006.13171. 

- [45] A. Eftekhar, K.-H. Zeng, J. Duan, A. Farhadi, A. Kembhavi, and R. Krishna. Selective Visual Representations Improve Convergence and Generalization for Embodied AI. In _ICLR_ , 2023. 

- [46] K.-H. Zeng, L. Weihs, A. Farhadi, and R. Mottaghi. Pushing it out of the way: Interactive visual navigation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2021. 

- [47] A. Majumdar, G. Aggarwal, B. Devnani, J. Hoffman, and D. Batra. ZSON: Zero-Shot Object-Goal Navigation using Multimodal Goal Embeddings. In _NeurIPS_ , 2022. URL http://papers.nips.cc/paper_files/paper/2022/hash/ d0b8f0c8f79d3a621af945cafb669f4b-Abstract-Conference.html. 

- [48] S. Wani, S. Patel, U. Jain, A. X. Chang, and M. Savva. MultiON: Benchmarking Semantic Map Memory using Multi-Object Navigation. In H. Larochelle, M. Ranzato, R. Hadsell, M. Balcan, and H. Lin, editors, _Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6- 12, 2020, virtual_ , 2020. URL https://proceedings.neurips.cc/paper/2020/ hash/6e01383fd96a17ae51cc3e15447e7533-Abstract.html. 

- [49] R. Ramrakhya, E. Undersander, D. Batra, and A. Das. Habitat-Web: Learning Embodied Object-Search Strategies from Human Demonstrations at Scale. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2022, New Orleans, LA, USA, June 18-24, 2022_ , pages 5163–5173. IEEE, 2022. doi:10.1109/CVPR52688.2022.00511. URL https: //doi.org/10.1109/CVPR52688.2022.00511. 

13 

- [50] N. Yokoyama, R. Ramrakhya, A. Das, D. Batra, and S. Ha. HM3D-OVON: A Dataset and Benchmark for Open-Vocabulary Object Goal Navigation. _IROS_ , 2024. 

- [51] M. Khanna, R. Ramrakhya, G. Chhablani, S. Yenamandra, T. Gervet, M. Chang, Z. Kira, D. S. Chaplot, D. Batra, and R. Mottaghi. Goat-bench: A benchmark for multi-modal lifelong navigation. In _CVPR_ , 2024. 

- [52] M. Oquab, T. Darcet, T. Moutakanni, H. V. Vo, M. Szafraniec, V. Khalidov, P. Fernandez, D. Haziza, F. Massa, A. El-Nouby, R. Howes, P.-Y. Huang, H. Xu, V. Sharma, S.-W. Li, W. Galuba, M. Rabbat, M. Assran, N. Ballas, G. Synnaeve, I. Misra, H. Jegou, J. Mairal, P. Labatut, A. Joulin, and P. Bojanowski. DINOv2: Learning Robust Visual Features without Supervision, 2023. 

- [53] X. Zhai, B. Mustafa, A. Kolesnikov, and L. Beyer. Sigmoid Loss for Language Image PreTraining. _ICCV_ , abs/2303.15343, 2023. doi:10.48550/ARXIV.2303.15343. URL https: //doi.org/10.48550/arXiv.2303.15343. 

- [54] Z. Xu, H.-T. L. Chiang, Z. Fu, M. G. Jacob, T. Zhang, T.-W. E. Lee, W. Yu, C. Schenck, D. Rendleman, D. Shah, et al. Mobility VLA: Multimodal Instruction Navigation with LongContext VLMs and Topological Graphs. In _CoRL_ . 

- [55] S. Nasiriany, F. Xia, W. Yu, T. Xiao, J. Liang, I. Dasgupta, A. Xie, D. Driess, A. Wahid, Z. Xu, et al. Pivot: Iterative visual prompting elicits actionable knowledge for vlms. _ICML_ , 2024. 

- [56] W. Yuan, J. Duan, V. Blukis, W. Pumacay, R. Krishna, A. Murali, A. Mousavian, and D. Fox. RoboPoint: A Vision-Language Model for Spatial Affordance Prediction for Robotics. _arXiv preprint arXiv:2406.10721_ , 2024. 

- [57] M. Ahn, A. Brohan, N. Brown, Y. Chebotar, O. Cortes, B. David, C. Finn, C. Fu, K. Gopalakrishnan, K. Hausman, et al. Do as i can, not as i say: Grounding language in robotic affordances. _CoRL_ , 2022. 

- [58] X. Chen, J. Hu, C. Jin, L. Li, and L. Wang. Understanding Domain Randomization for Sim-toreal Transfer. In _The Tenth International Conference on Learning Representations, ICLR 2022, Virtual Event, April 25-29, 2022_ . OpenReview.net, 2022. URL https://openreview. net/forum?id=T8vZHIRTrY. 

- [59] E. Kolve, R. Mottaghi, W. Han, E. VanderBilt, L. Weihs, A. Herrasti, M. Deitke, K. Ehsani, D. Gordon, Y. Zhu, A. Kembhavi, A. K. Gupta, and A. Farhadi. AI2-THOR: An Interactive 3D Environment for Visual AI. _ArXiv_ , abs/1712.05474, 2017. URL https: //api.semanticscholar.org/CorpusID:28328610. 

- [60] A. I. for AI. ObjaTHOR: Python package for importing and loading external assets into ai2thor. https://github.com/allenai/objathor, 2024. 

- [61] L. Weihs, J. Salvador, K. Kotar, U. Jain, K.-H. Zeng, R. Mottaghi, and A. Kembhavi. AllenAct: A Framework for Embodied AI Research. _arXiv preprint arXiv:2008.12760_ , 2020. 

- [62] K. Ehsani, T. Gupta, R. Hendrix, J. Salvador, L. Weihs, K.-H. Zeng, K. P. Singh, Y. Kim, W. Han, A. Herrasti, et al. Imitating Shortest Paths in Simulation Enables Effective Navigation and Manipulation in the Real World. In _CVPR_ , 2024. 

- [63] M. Deitke, R. Hendrix, L. Weihs, A. Farhadi, K. Ehsani, and A. Kembhavi. Phone2Proc: Bringing Robust Robots Into Our Chaotic World, 2022. 

- [64] P. E. Hart, N. J. Nilsson, and B. Raphael. A Formal Basis for the Heuristic Determination of Minimum Cost Paths. _IEEE Trans. Syst. Sci. Cybern._ , 4:100–107, 1968. URL https: //api.semanticscholar.org/CorpusID:206799161. 

14 

- [65] A. A. Hagberg, D. A. Schult, P. Swart, and J. Hagberg. Exploring Network Structure, Dynamics, and Function using NetworkX. _Proceedings of the Python in Science Conference_ , 2008. URL https://api.semanticscholar.org/CorpusID:16050699. 

- [66] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark, et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pages 8748–8763. PMLR, 2021. 

15 

## **Appendices for** **_The One RING : a Robotic Indoor Navigation Generalist_** 

The following items are provided in the Appendix: 

- _Details about the real-world evaluation robot platforms and human evaluation setup (App. 7),_ 

- _Data collection for randomized embodiments using expert planners in simulation (App. 8),_ 

- _Full experimental setup (App. 9),_ 

- _Model architecture details (App. 10),_ 

- _We study the impact of using a more powerful visual encoder (App. 11),_ 

- _A visualization of the random embodiments in our training set, along with the 5 nearest neighbors to each of the real robots (Stretch-RE1, LoCoBot, Unitree A1) (App. 12),_ 

- _Out-of-distribution generalization for different embodiment parameters (App. 13)_ 

On our website (one-ring-policy.allen.ai), we have 

- _Real-world qualitative videos of evaluating_ RING _zero-shot on five different robot platforms, including Stretch RE-1 with our camera setup, Stretch RE-1 with factory camera configuration, LoCoBot, Unitree GO1, and RB-Y1 wheeled humanoid,_ 

- _Qualitative videos for human evaluation, using_ RING _as navigation assistant,_ 

- _Videos showing our dataset of trajectories collected from random embodiments in simulation._ 

## **7 Real Robot Platforms and Human Evaluation Setup.** 

### **7.1 Stretch RE-1, LoCoBot, Unitree GO1, RB-Y1** 

We use Stretch RE-1, LoCoBot, Unitree GO1, and RB-Y1 wheeled humanoid as our robot platforms for real-world evaluations, shown in Fig. 8. For Stretch RE-1, we evaluate two different sensor configurations: the factory configuration and the configuration suggested by SPOC [12]. For RB-Y1, we include both standing and seated configurations and use an iPhone 16 Pro camera mounted on the robot to stream visual observations. The main differences among these platforms are summarized in Tab. 8. For robot movements, we either implement a Kalman filter or wrap around provided robot APIs to realize low-level controllers for a discrete action space _{_ MoveBase(±20cm), 


Figure 6: **Real Evaluation Environment** . Our real-world evaluations are performed in a multiroom apartment with a long corridor, shown here with the three starting locations for three different robots’ evaluations. 

RotateBase(±6<sup>_◦_</sup> , ±30<sup>_◦_</sup> ), Done _}_ across all platforms. It is important to note that during the training stage, we do not use any embodiment configurations from these robots to generate imitation learning data or to initialize RL fine-tuning embodiments. 

### **7.2 Human Evaluations** 

**Human participants** . We asked five human participants to use RING as a navigation assistant and evaluated its performance across a diverse range of human embodiments. These embodiment variations arose from differences in camera-holding posture, participant height, step size, and rotation angle. Tab. 9 summarizes these variations across participants. As a result, each participant contributed a distinct set of evaluation embodiments and sensor configurations. 

16 

||Stretch RE-1|Stretch RE-1(Factory)|LoCoBot|Unitree GO1|RB-Y1(standing)|RB-Y1(seated)|
|---|---|---|---|---|---|---|
|Body dimension (cm)|33_×_34_×_141|33_×_34_×_141|35_×_35_×_89|64.5_×_28_×_40|60_×_69_×_140|60_×_69_×_92|
|Camera model|2_×_D455|D435|D435|D435|iPhone 16 Pro Camera|iPhone 16 Pro Camera|
|Camera vertical FoV|59<sup>_◦_</sup>|69<sup>_◦_</sup>|42<sup>_◦_</sup>|42<sup>_◦_</sup>|73<sup>_◦_</sup>|73<sup>_◦_</sup>|
|Camera horizontal FoV|90<sup>_◦_</sup>|42<sup>_◦_</sup>|68<sup>_◦_</sup>|68<sup>_◦_</sup>|53<sup>_◦_</sup>|53<sup>_◦_</sup>|
|Camera height (cm)|140|130|87|28|140|92|
|Camerapitch|27<sup>_◦_</sup>|30<sup>_◦_</sup>|0<sup>_◦_</sup>|0<sup>_◦_</sup>|0<sup>_◦_</sup>|0<sup>_◦_</sup>|


Table 8: **Details about evaluation robot platforms.** Our four robot platforms have varying dimensions and camera configurations, resulting in diverse evaluation embodiments. 

||H1|H2|H3|H4|H5|
|---|---|---|---|---|---|
|Height|6<sup>_′_</sup>3<sup>_′′_</sup>|5<sup>_′_</sup>10<sup>_′′_</sup>|5<sup>_′_</sup>5<sup>_′′_</sup>|6<sup>_′_</sup>1<sup>_′′_</sup>|5<sup>_′_</sup>11<sup>_′′_</sup>|
|Step size|0.25m|0.35m|0.4m|0.3m|0.3m|
|Rotation Degrees|30<sup>_◦_</sup>|45<sup>_◦_</sup>|45<sup>_◦_</sup>|35<sup>_◦_</sup>|30<sup>_◦_</sup>|


Table 9: **Details about human evaluators.** Our five human participants have varying heights, step size, and rotation degrees, resulting in different evaluation embodiments. 

**Human Evaluation Details.** We developed a simple iOS app (Fig. 7) that allows human participants to input a text prompt (e.g., “Find a mug”), capture an image using the iPhone’s back camera, and send both the prompt and image to a remote server. The server processes this input using our RING policy, predicts action probabilities, samples an action, and returns it to the app for display. The action space available in the app mirrors that of our realworld robot. 

Participants follow the suggested action at their own pace and chosen rotation degree, as specified in Tab. 9. After each step, they tap the Predict button to repeat the process: capturing a new image and sending it, along with the original prompt, to the server. This continues until either the Done action is returned or 100 steps have been executed. An episode is considered successful if the target object is visible in the final image, within 1 meter, when RING issues the Done action. 

Fig. 10 shows the layout of the evaluation scene and two sample trajectories, including two locations for a Mug, three for a Houseplant, and one for an Apple. Participants always begin in the bottom-left corner of the scene (results shown in Tab. 4). 


Figure 7: textbfiOS app for human evaluation. We developed a simple iOS app that enables human participants to text goal, capture an image using iPhone’s back camera, send both to a remote server, and receive the predicted action from our RING policy. 

## **8 Data Generation with Expert Planners** 

Expert planners introduced by [12] are not efficient and robust for random embodiments. As a result, we made major improvements to the planners to allow for better trajectories. 

The major factor in this improvement is to consider _safety_ of the policy (defined as the avoidance of approaching any obstacles along the way.) We use A* [64, 65] to generate safe navigation trajectories for training as follows: **1)** Extract reachable locations in a scene on a finely spaced grid, ensuring that the agent’s collider does not intersect with any object’s collider. Thus, different embodiments yield different reachable locations according to their collider. **2)** Compute a clipped Euclidean distance to the nearest obstacle. Then, for each location, set the cost of visiting it as the inverse of the third power of the distance. **3)** Construct a grid-like graph where each reachable location is a node connected to its immediate neighbors. For each connection, assign a cost equal to the maximum cost of visiting either of the two connected nodes. **4)** Extract a minimum-cost path connecting the reachable positions in the graph nearest to the source and to the target via A*. **5)** Extract waypoints by skipping over points in the A* path as long as skipping them doesn’t increase the total path cost from the latest waypoint. **6)** The expert linearly interpolates between waypoints up to the precision reachable by the action space to generate each trajectory. 

17 


Figure 8: **Robot platforms** . We evaluate on 6 different platforms: Stretch RE-1 (with two camera configurations), LoCoBot, Unitree GO1, and the RB-Y1 wheeled humanoid, tested in both standing and seated configurations. 


Figure 9: **RB-Y1 Trajectories.** We deploy the policy on the wheeled humanoid in an unstructured kitchen area (layout shown in Fig. 10) to navigate to different objects. We include both seated and standing configurations and use an iPhone 16 Pro camera to stream the visual observations. 

## **9 Additional Benchmark/Experiment Details** 

**Action Space.** Following on prior work with AI2-THOR, we discretize the action space for all agents in our training: _{_ MoveAhead, MoveBack, RotateRight, RotateLeft, RotateRightSmall, RotateLeftSmall, Done _}_ . Here, MoveAhead advances the robot by 0.2 meters, MoveBack moves the robot backward by 0.2 meters, RotateRight/RotateRightSmall rotates it clockwise by 30<sup>_◦_</sup> / 6<sup>_◦_</sup> around the yaw axis, and RotateLeft/RotateLeftSmall rotates it counterclockwise by 30<sup>_◦_</sup> / 6<sup>_◦_</sup> around the yaw axis, and Done indicates the agent has located the target, ending the episode. We evaluate RING zero-shot on all robots (Stretch-RE, LoCoBot, Unitree Go1) with the same action space using their low-level controllers. When finetuning for embodiment-specialized policies, we finetune for a slightly different action space for LoCoBot: _{_ MoveAhead, MoveBack, RotateRight, RotateLeft, LookUp, LookDown, Done _}_ . LookUp tilts the camera up by 30<sup>_◦_</sup> around the roll axis and LookDown tilts the camera down by 30<sup>_◦_</sup> around the roll axis. All baselines are trained and evaluated with the same action space for fair comparison. 

18 


Figure 10: **Human Trajectories** . Two sample trajectories from two individuals navigating to a houseplant and an apple using RING. 

**Success Criteria.** We follow the definition of Object Goal Navigation from [44], where an agent must explore its environment to locate and navigate to a specified object within a maximum of _n_ steps. To indicate it has found the target, the agent must execute the Done action. Success is determined by the environment based on whether the agent is within a distance _d_ of the target and if the target is visible in its view. If the agent exceeds _n_ steps without executing the Done action, the episode is considered a failure. For simulation benchmarks, we follow CHORES-S [12] with _n_ = 600 and _d_ = 2. For real-world evaluations, we use _n_ = 300 and _d_ = 1. 

**Success weighted by collision (SC).** Collision is one of the main challenges for a unified policy operating across diverse embodiments in visual navigation tasks. Previous works measure the collision rate (<sup><u>#</u></sup><sup>_<u>collisions</u>_</sup> # _steps_<sup>)tounderstandhowoftenapolicycollideswithobjectsinascene.However,</sup> this does not reflect the effectiveness of the policy at the task level. For example, in a successful episode, a single collision and multiple collisions should have different impacts on the performance measurement. As a results, inspired from Success Weighted by Episode Length (SEL), we propose Success Weighted by Collision (SC), _N_ 


where _Si_ is a binary indicator of success for episode _i_ , _ci_ is the number of collisions in episode _i_ , and _N_ is the number of evaluation episodes. In this metric, the policy is penalized most heavily for a single collision, with the penalization decreasing for each additional collision, as the penalty diminishes inversely with the number of collisions. Intuitively, _>_ 0 collisions are much worse than 0, as a real robot may suffer damage from one bad collision, but the difference between 10 and 11 collisions is a more marginal difference. 

**Hyparameters.** We list the hyperparameters used in training and the architecture in Table 10. 

### **9.1 Real-World Benchmarks** 

We evaluate 3 of the robots (Stretch-RE1, LoCoBot, Unitree Go1) in a multi-room apartment shown in Fig. 6. Based on the embodiment, the benchmark has different starting locations and objects. Among our target object categories, Apple can be found in the Living room and Kitchen, Bed can only be found in the Bedroom, Sofa and Television can only be found in the Living room, Vase can be found in the Livingroom, Corridor, Office, and Kitchen, Chair can be found in the Office and Kitchen, HousePlant can be found in the Living room, Office, and Kitchen. 

We also deploy the policy on the RB-Y1 wheeled humanoid in an unstructured kitchen environment—similar to the human evaluation setting. 

- **LoCoBot** : Following Phone2Proc [63], use the same five target object categories, including Apple, Bed, Sofa, Television, and Vase, and the three starting poses shown in 6. 

19 

|**Imitation Learning**||
|---|---|
|Batch Size|224|
|Context Length|100|
|LearningRate|0.0002|
|**RL Finetuning**||
|Total Rollouts|64|
|Learning Rate|0.0002|
|Mini Batch per Update|1|
|Update Repeats|4|
|Max Gradient Norm|0.5|
|Discount Value Factor_γ_|0.99|
|GAE_λ_|0.95|
|PPO Surrogate Objective Clipping|0.1|
|Value Loss Weight|0.5|
|Entropy Loss Weight|0.0|
|Steps for PPO Update|128|
|**Model Architecture**||
|Transformer State Encoder Layers|3|
|Transformer State Encoder Hidden Dims|512|
|Transformer State Encoder Heads|8|
|Causal Transformer Deocder Layers|3|
|Causal Transformer Deocder Hidden Dims|512|
|Causal Transformer Deocder Heads|8|


Table 10: **Hyperparameters for training and model architecture.** 


Figure 11: **RING architecture** . The notations in gray correspond to hidden feature vectors and the black text on top of each module indicates the hyperparameters for that module. RING accepts visual observations and a language instruction as inputs and predicts an action to execute. During RL finetuning, RING also predicts a value estimate. We mask the image from the 2<sup>_nd_</sup> camera with all 0 for the embodiments with only one camera, such as LoCoBot and Unitree. More specifically, we use the Vision Transformer and the Text Encoder from SIGLIP-ViT-B/16 as our visual encoder and goal encoder. After encoding, we compress and project the visual representation _r_ and text embedding _t_ to _v_ and _g_ , respectively, with the desired dimension _d_ . Next, the Transformer State Encoder encodes _v_ , _g_ , along with state token embedding _f_ into a state feature vector _s_ . The Causal Transformer Decoder further processes _s_ , along with previous experiences stored in the KV-Cache, to produce the state belief _b_ . Finally, the Linear Actor-Critic Head predicts action logits (and, during RL finetuning, a value estimate) from _b_ . 

- **Stretch RE-1** : We follow SPOC [62] to use the same six target object categories, including Apple, Bed, Chair, HousePlant, Sofa, and Vase, and the three starting poses, shown in Fig. 6. We consider 2 different camera configurations for Stretch: 1) off-theshelf camera equipped on the Stretch RE-1 (D435 with a vertical field of view of 69<sup>_◦_</sup> and resolution of 720 _×_ 1280), 2) following [12], we use 2 Intel RealSense 455 fixed cameras, with a vertical field of view of 59<sup>_◦_</sup> and resolution of 1280 _×_ 720. The cameras are mounted facing forward but pointing downward, with the horizon at an angle of 27<sup>_◦_</sup> . 

- **Unitree Go1** : We create a new evaluation set for Unitree Go1 with 3 starting poses (Fig. 6) and 4 objects (toilet, sofa, TV, trashcan) positioned to accommodate the robot’s lower height, ensuring that the objects can be visible from its lower viewpoint. 

20 

- **RB-Y1** : The wheeled humanoid navigates to various target objects in a real kitchen area, including a mug, apple, houseplant, and trashcan (2 example trajectories shown in Fig. 9). 

## **10 Model Architecture Details** 

We will now detail RING’s architecture (see Fig. 11), which is inspired by previous works POLIFORMER [13] and FLARE [14]. 

**Visual encoder** . We use the Vision Transformer from the pretrained SIGLIP-VIT-B/16 as our visual encoder. Since the RGB images vary in dimensions across different embodiments, we include an additional preprocessing step before feeding them into the encoder. Specifically, we pad each RGB image to a square and then resize it to 256 _×_ 256. In addition, we mask the image from the 2<sup>_nd_</sup> camera with zeros for the embodiments with only one camera. The visual backbone takes the RGB observation _i ∈_ R<sup>256</sup><sup>_×_256</sup><sup>_×_3</sup> as input and produces a patch-wise representation _r ∈_ R <u>25616</u><sup>_×_</sup><sup><u>256</u></sup> 16<sup>_×h_</sup> , where _h_ = 768 is the hidden dimension of the visual representation. We reshape the visual representation into a _ℓ × h_ matrix, _ℓ_ = 256 _·_ 256 _/_ 16 _·_ 16, and project the representation to produce _v ∈_ R<sup>_ℓ×d_</sup> , where _d_ = 512 is the input dimension to the transformer state encoder. Note that since we have two RGB images from two cameras, we produce two visual representations _v_<sup>1</sup><sup>_,_2</sup> at the end of this module. The vision encoder remains frozen through training. 

**Goal encoder.** We follow the Text Transformer from the pretrained SIGLIP-VIT-B/16 to encode the given natural language instruction into goal embedding _t ∈_ R<sup>64</sup><sup>_×h_</sup> , where _h_ = 768 is the hidden dimension and this Text Transformer returns 64 tokens after padding. Before passing the goal embedding to the transformer state encoder, we always project the embedding to the desired dimension _d_ = 512, resulting in _g ∈_ R<sup>64</sup><sup>_×_512</sup> . 

**Transformer State Encoder.** This module summarizes the state at each timestep as a vector _s ∈_ R<sup>_d_</sup> . The input to this encoder includes two visual representations _v_<sup>1</sup><sup>_,_2</sup> , the goal feature _g_ , and an embedding _f_ of a STATE token. These features are concatenated and fed to the non-causal transformer encoder. The output corresponding to the STATE token is the state feature vector _s ∈_ R<sup>_d_</sup> which summarizes the state at each timestep. This feature vector is a goal-conditioned visual state representation. 

**Causal transformer decoder.** We use a causal transformer decoder to perform explicit memory modeling over time. This can enable both long-horizon (e.g., exhaustive exploration with backtracking) and short-horizon (e.g., navigating around an object) planning. Concretely, the causal transformer decoder constructs its state belief _b_<sup>_t_</sup> using the sequence of state features **s** = _{s_<sup>_j_</sup> _|_<sup>_j_</sup> _j_<sup>=</sup> =<sup>_t_</sup> 0<sup>_}_</sup> within the same trajectories. To avoid recomputing the attention on the previous state features, we follow PoliFormer [13] to use KV-Cache to store the past **K** ey and **V** alue into two cache matrices in each attention layer. Therefore, we only perform feedforward computation for the most current state feature _s_<sup>_t_</sup> . 

**Linear actor-critic head.** With the latest state belief _b_<sup>_t_</sup> , we simply use a linear actor-critic head to project it to predict action logits over the action space. For RL-finetuning, the linear actor-critic head also predicts a value estimate about the current state. 

## **11 A More Powerful Pretrained Visual Encoder.** 

The default vision encoder used in our policies is the pretrained SIGLIP-VIT-B/16. In this section, we examine the impact of using a more powerful visual encoder on RING’s performance. We train RING-LARGE using OpenAI’s VIT-L/14 336PX CLIP model [66]. Table 14 compares the results, showing that a stronger visual encoder significantly improves zero-shot performance across all four embodiments (approximately 9% improvement on average). A larger visual encoder is particularly beneficial in our policy, as the visual observations are highly varied due to randomized camera parameters. To ensure fair comparison with the baselines and because VIT-L/14 is more computationally demanding, we chose to use the VIT-B/16 encoder for our main experiments. We will release the training code for the community for those interested in training with the larger visual encoder. 

21 

||||Neare|s|t Nei|ghbor|s||||Near|est Neighbor|s|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**Stretch R**|**E-1** N1|N2||N3|N4|N5||**Locob**|**ot** N1|N2|N3<br>N4|N5|
|Camera Position (x) (meters|0|-0.06|0.11|0||-0.08|0.03|Camera Position (x) (meters)|0|-0.09|0.12|0.03 _−_0_._06|-0.1|
|Camera Position (y) (meters|1.44|1.13|0.67|0|.24|0.72|0.32|Camera Position (y) (meters)|0.87|1.01|0.81|0.39 0.85|0.42|
|Camera Position (z) (meters|0.07|0.03|0.06|0|.07|0.07|-0.03|Camera Position (z) (meters)|0|-0.1|-0.0|5 -0.1 -0.02|0.09|
|Camera Pitch (degrees)|27|29|33|3|4|32|33|Camera Pitch (degrees)|0|0|0|-1<br>0|1|
|Camera Yaw (degrees)|0|0|0|0||0|0|Camera Yaw (degrees)|0|0|0|0<br>0|0|
|Vertical FoV (degrees)|59|57|56|5|4|59|54|Vertical FoV (degrees)|42|45|44|42<br>45|45|
|RGB Resolution (H)|224|224|224|2|24|224|224|RGB Resolution (H)|224|224|224|224 224|224|
|RGB Resolution (Y)|396|394|394|3|96|396|398|RGB Resolution (Y)|396|396|394|394 392|392|
|Rotation Center (x) (meters)|0|0|0.09|-|0.17|0|0.02|Rotation Center (x) (meters)|0|0.04|0.1|0.1<br>-0.02|-0.15|
|Rotation Center (z) (meters)|0.11|0.02|0.02|-|0.08|0.04|-0.12|Rotation Center (z) (meters)|0|-0.13|0|0.13 0.02|-0.12|
|Collider Size (x) (meters)|0.34|0.23|0.28|0|.49|0.33|0.24|Collider Size (x) (meters)|0.35|0.27|0.36|0.37 0.27|0.42|
|Collider Size (y) (meters)|1.41|1.41|0.9|0|.84|1.23|0.43|Collider Size (y) (meters)|0.89|1.28|1.23|0.86 1.46|0.59|
|Collider Size (z) (meters)|0.33|0.27|0.41|0|.29|0.44|0.38|Collider Size (z) (meters)scale|z 0.4|0.43|0.23|0.36 0.36|0.45|
|distance|-|0.38|0.7|0|.79|0.8|0.92|distance|-|0.18|0.22|0.34 0.41|0.42|


Table 11: Five Nearest Neighbor Embodiments for Stretch RE-1 in Training Data. 

Table 12: Five Nearest Neighbor Embodiments for LoCoBot in Training Data. 

||||Neare|st Nei|ghbors||
|---|---|---|---|---|---|---|
||**Unitree A1**|N1|N2|N3|N4|N5|
|Camera Position (x) (meters)|0.01|0.08|0.03|-0.01|-0.04|0.1|
|Camera Position (y) (meters)|0.3|0.56|0.37|0.85|0.55|0.82|
|Camera Position (z) (meters)|0.27|-0.11|0.06|0|0.12|0.02|
|Camera Pitch (degrees)|0|-3|-2|-4|-5|-5|
|Camera Yaw (degrees)|0|0|0|0|0|0|
|Vertical FoV (degrees)|42|49|49|51|50|51|
|RGB Resolution (H)|270|224|224|224|224|224|
|RGB Resolution (Y)|480|448|446|448|446|446|
|Rotation Center (x) (meters)|0|-0.07|0.05|-0.07|-0.09|-0.14|
|Rotation Center (z) (meters)|0.04|-0.02|0|-0.12|0.12|0.11|
|Collider Size (x) (meters)|0.3|0.46|0.27|0.35|0.27|0.49|
|Collider Size (y) (meters)|0.34|1.24|0.45|1.47|0.67|1.39|
|Collider Size(z) (meters)|0.64|0.34|0.37|0.36|0.33|0.39|
|distance|-|0.76|0.78|1.04|1.1|1.12|


Table 13: Five Nearest Neighbor Embodiments for Unitree A1 in Training Data. 

## **12 Nearest Neighbor Embodiments to Real Robots in our Training Data** 

Fig. 12 presents a t-SNE visualization of the embodiment parameters **c** _e ∈_ R<sup>19</sup> for 50k samples from the random embodiments in our training set (examples showin in Fig. 13). We also show the corresponding parameters for Stretch, LoCoBot, and Unitree A1 for visualization purposes. Our random embodiments range widely over the space of possible embodiments, with many closely approximating each of the three real robots. Tables 11, 12, and 13 list the five nearest neighbors to each robot in the compressed t-SNE space and their corresponding embodiment parameters. Although the nearest neighbors do not exactly match each robot’s embodiment, they are sufficiently similar across different parameters. This extensive coverage of the embodiment space and proximity to real-world embodiments ensure consistent zero-shot generalization to all three robots. 


Figure 12: t-SNE visualization of the embodiment parameters **c** _e ∈_ R<sup>19</sup> for 50k random agents. The three specific robots are also shown for visualization (they are not included in our training set). 

## **13 Generalization to out-of-distribution embodiment parameters** 

The random embodiments in our training set span a wide range of possible configurations, with many closely approximating each of the three real robots. Although the training data covers the full range of each embodiment parameter individually, the specific combination of parameters corresponding to each real robot is not explicitly included. This is demonstrated by the nearest-neighbor embodiments shown in Appendix 12. In this section, we examine the extent to which the policy generalizes to out-of-distribution values of individual embodiment parameters. 

22 

|Model|Visual Encoder||Benchmark|Embodiment||
|---|---|---|---|---|---|
|||**Stretch**|**Stretch** (Nav)|**LoCoBot**|**Unitree A1**|
|RING|SIGLIP-VIT-B/16|76.0|74.0|66.5|72.0|
|RING-LARGE|VIT-L/14 336PXCLIP|**83.8**|**77.7**|**75.3**|**79.9**|


Table 14: **A Stronger Visual Encoder** . Using a more powerful vision encoder significantly improves the zero-shot performance across all embodiments. 


Figure 13: **Random embodiments in the AI2-THOR simulator** . Right column shows the egocentric view from the main camera and the left column shows a third-person view of the agent –white boxes indicate the robot colliders for visualization purposes only. 

We focus on four specific parameters: _camera height, camera field of view (FOV), camera pitch_ , and _collider size_ . For each parameter, we define a narrower range that excludes the values corresponding to the real robots. From the training data, we filter the random embodiments to select 50k samples within each of these specified ranges. For comparison, we also train a version of the policy using 50k unfiltered embodiments that span the full range of each parameter. The selected training ranges for each parameter are illustrated in Fig. 14. 

We then perform zero-shot evaluations of the policies trained on each selected range using four robots whose parameters lie outside the training ranges. The success rate and collision rate are summarized in Table 15. The results indicate that policies trained on narrower ranges still generalize to out-of-distribution parameters, achieving only a slightly lower success rate. However, evaluation on unseen embodiment parameters leads to a significantly higher collision rate, particularly for the policy trained with a narrower range of collider sizes. This suggests that the agent may rely more on physical contact with the environment to infer its embodiment configurations. Comparing Table 15 and Table 2, the average success rate drops by 13%, emphasizing that the number of random embodiments used during training is crucial to develop an embodiment-agnostic policy capable of effectively handling a wide range of embodiments. 

23 


Figure 14: **Selected training ranges for the four embodiment parameters (camera height, camera FOV, camera pitch, and collider size)** . The green regions represent the narrower ranges used during training, excluding the values corresponding to the real robots. The results of policies trained on each selected range are presented in Table 15. 

|Embodiment|Training Range||Success Rate|_↑_/ Collision Rate|_↓_||
|---|---|---|---|---|---|---|
|Parameter||**Stretch**|**Stretch**(Factory Config)|**LoCoBot**|**Unitree A1**|**Average**|
|Camera Height|[0.4, 0.8]|55.3 /**9.3**|51.0 / 9.8|51.5 / 9.8|59.3 / 9.2|54.3 / 9.5|
|Camera FoV|[40, 60]|54.0 / 14.3|51.6 / 15.5|53.4 / 12.8|**61.5**/ 11.5|55.1 / 13.5|
|Camera Pitch|[-20, -2]|54.5 / 12.9|53.5 / 9.7|**56.5**/ 11.2|59.8 / 12.7|56.1 / 11.6|
|Collider Size|[0.20, 0.32]|**60.5**/ 18.0|53.5 / 21.4|55.0 / 14.9|54.0 / 18.6|55.7 / 18.2|
|No Filter|-|58.8 / 9.6|**60.0**/**9.5**|**56.5**/**7.9**|60.9 /**8.3**|**59.1**/**8.8**|


Table 15: **Out-of-distribution (OOD) generalization for different embodiment parameters.** For each of the four embodiment parameters, we select 50k random embodiments from a narrow training range that excludes the parameter values of the real robots (as shown in Fig. 14). Zero-shot evaluations are performed on four real robots, each with parameter values outside the training distribution. Success and collision rates are reported for each robot and averaged across all robots. 

24 

