---
title: "$π$, But Make It Fly: Physics-Guided Transfer of VLA Models to Aerial Manipulation"
date: "2026-03-26"
authors: "Johnathan Tucker; Denis Liu; Aiden Swann; Allen Ren; Javier Yu; Jiankai Sun"
venue: "CoRL 2026"
url: https://arxiv.org/abs/2603.25038
pdf: https://arxiv.org/pdf/2603.25038
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.25038)** / [論文ページ](https://arxiv.org/abs/2603.25038)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# _π_ , But Make It Fly: Physics-Guided Transfer of VLA Models to Aerial Manipulation 

Johnathan Tucker<sup>1</sup> Denis Liu<sup>1</sup> Aiden Swann<sup>1</sup> Allen Ren<sup>2</sup> Javier Yu<sup>1</sup> Jiankai Sun<sup>1</sup> Brandon Kim<sup>1</sup> Lachlain McGranahan<sup>1</sup> Quan Vuong<sup>2</sup> Mac Schwager<sup>1</sup> 

> 1Stanford University 

> 2Physical Intelligence 

https://airvla.github.io 


Fig. 1: **Overview of AirVLA:** Our method fine-tunes the _π_ 0 vision-language-action model on a combination of teleoperated and 3D Gaussian Splatting synthetic data. **(Left)** The policy processes multimodal inputs including natural language commands, proprioception, and multi-view camera observations. **(Right)** To ensure robust flight during manipulation, we introduce a payload-aware guidance signal, _Fguide_ , combined with real-time chunking. **(Center)** This enables AirVLA to execute novel, zero-shot compositional tasks, such as navigating through gates and manipulating objects. 

**_Abstract_ —Vision-Language-Action (VLA) models such as** _π_ 0 **have demonstrated remarkable generalization across diverse fixed-base manipulators. However, transferring these foundation models to aerial platforms remains an open challenge due to the fundamental mismatch between the quasi-static dynamics of fixed-base arms and the underactuated, highly dynamic nature of flight. In this work, we introduce AirVLA, a system that investigates the transferability of manipulation-pretrained VLAs to aerial pick-and-place tasks. We find that while visual representations transfer effectively, the specific control dynamics required for flight do not. To bridge this ”dynamics gap” without retraining the foundation model, we introduce a Payload-Aware Guidance mechanism that injects payload constraints directly into the policy’s flow-matching sampling process. To overcome data scarcity, we further utilize a Gaussian Splatting pipeline to synthesize navigation training data. We evaluate our method through a cumulative 460 real-world experiments which demonstrate that this synthetic data is a key enabler of performance, unlocking 100% success in navigation tasks where directly fine-** 

**tuning on teleoperation data alone attains 81% success. Our inference-time intervention, Payload-Aware Guidance, increases real-world pick-and-place task success from 23% to 50%. Finally, we evaluate the model on a long-horizon compositional task, achieving a 62% overall success rate. These results suggest that pre-trained manipulation VLAs, with appropriate data augmentation and physics-informed guidance, can transfer to aerial manipulation and navigation, as well as the composition of these tasks.** 

**_Index Terms_ —Vision-Language-Action (VLA) Model, VisionLanguage Model (VLM), Cross-Embodiment Transfer, Aerial Robotics, Unmanned Aerial Manipulators (UAMs)** 

## I. INTRODUCTION 

Vision-Language-Action (VLA) foundation models have demonstrated remarkable cross-embodiment generalization, enabling robots with diverse morphologies to complete manipulation tasks from natural language instructions. Models 

such as RT-X [12], Octo [34], and _π_ 0 [3] leverage large-scale multimodal pretraining across dozens of robot embodiments, learning representations that transfer across manipulators with different kinematics, workspaces, and end-effector designs. However, all such demonstrations share a fundamental constraint: they operate from stable, fixed or mobile bases in quasi-static regimes. This raises a central question: _can VLA policies transfer to aerial manipulators_ , robots that couple perception, language understanding, and contact-rich interaction with underactuated 6-DoF flight control? Such transfer would represent an extreme test of cross-embodiment learning, as aerial platforms differ fundamentally from ground robots in dynamics, control authority, and sensing characteristics. 

Answering this question has both scientific and practical significance. Scientifically, aerial manipulation provides a stress test for the representations learned by VLA foundation models: if policies pretrained entirely on fixed-base manipulators can partially transfer to flying robots through fine-tuning, it suggests these models capture manipulation primitives that transcend specific embodiment constraints. Practically, languageconditioned aerial manipulation would enable applications previously beyond reach: delivering medical supplies in inaccessible terrain, clearing debris in collapsed structures, or manipulating infrastructure at height. If VLA policies could be adapted for such platforms, non-expert operators could issue high-level language commands while the policy handles lowlevel perception and control. 

Several fundamental challenges distinguish aerial manipulation from the ground-robot scenarios that dominate VLA training data. First, quadrotors are underactuated: thrust and attitude are tightly coupled, and small errors in predicted actions can induce large deviations in pose. This failure mode rarely occurs in fixed-base manipulation. Second, onboard cameras experience large ego-motion, rapid viewpoint changes, motion blur, and scale variation that differ significantly from tabletop scenarios in most VLA datasets [25, 12]. Finally, contact with objects induces payload changes [5, 21] and aerodynamic disturbances [37, 35] that violate quasi-static assumptions implicit in most manipulation policies. 

While recent work has begun exploring languageconditioned aerial systems and cross-embodiment transfer to drones, no prior work has systematically investigated whether manipulation-pretrained VLA foundation models can transfer to aerial platforms. Concurrent efforts take fundamentally different approaches: UMI-on-Air [19] trains embodimentagnostic diffusion policies from scratch on handheld demonstrations and introduces inference-time guidance to compensate for aerial dynamics, but does not leverage or evaluate VLA foundation models. SINGER [1] and GRaDNav++ [9] demonstrate language-conditioned drone navigation using learned visuomotor policies, but focus exclusively on navigation without physical manipulation or contact. More broadly, while cross-embodiment datasets such as Open X- Embodiment [12] include dozens of manipulators, they contain no aerial platforms or underactuated flight dynamics, leaving the transferability of VLA representations to aerial manipula- 

tion unexplored. 

To address these gaps, we introduce _AirVLA_ , the first systematic investigation of whether manipulation-pretrained VLA foundation models can transfer to aerial manipulators through fine-tuning. Our system consists of a ModalAI Starling 2 Max quadrotor equipped with a lightweight compliant gripper derived from the Universal Manipulation Interface (UMI) [11, 20, 19], forward- and downward-facing onboard cameras, and a ROS-based control stack that treats the drone as a “flying end-effector.” We construct a diagnostic task suite spanning (i) _pick-and-place_ manipulation collected via human teleoperation, (ii) _navigation_ tasks with human teleoperation data and synthetic training trajectories generated using model predictive control (MPC) in Gaussian Splatting reconstructions, and (iii) _compositional_ tasks that chain both behaviors. This design enables us to isolate which aspects of manipulation skill transfer to aerial platforms and which fail. 

We directly fine-tune the foundation-scale VLA policy _π_ 0 (pretrained on large manipulation datasets containing no aerial platforms) on our aerial manipulation data. Our experiments reveal partial but significant skill transfer: the finetuned policy learns stable hovering and coarse manipulation behaviors, demonstrating that foundation models capture some manipulation primitives that generalize to flight. However, standard fine-tuning fails at task completion due to sensitivity to payload dynamics and explicit obstacle navigation limitations. To address these specific failure modes, we introduce domain-adapted components: (i) a physics-aware low-level controller that wraps VLA outputs to enforce dynamically feasible commands, and (ii) synthetic navigation augmentation that enriches the training distribution. While these adaptations improve performance on navigation and stabilization during manipulation, fundamental limitations remain for long-horizon compositional manipulation and out-of-distribution adaptation, highlighting important open challenges in extending VLA models to underactuated, dynamic embodiments. 

In summary, this paper makes the following contributions: 

- We present AirVLA, the first demonstration of a pretrained VLA fine-tuned for an aerial manipulation platform. 

- We manually collect a dataset of 270 aerial manipulation and navigation teleop-demos, to be open-sourced. 

- We synthesize 50 3DGS-based corrective navigation examples to help supervise VLA fine-tuning, showing a 20% increase in navigation task success compared to finetuning with teleop only. 

- We introduce a physics-informed guidance within realtime-chunking to adapt at runtime to the mass of a grasped object, improving task success by 10% _−_ 40% in pick and place tasks. 

II. RELATED WORK 

- _A. Vision-Language-Action Policies for Manipulation_ 

Vision-language-action (VLA) policies leverage large-scale multimodal pretraining to enable general-purpose robot control 

from natural language instructions. Early approaches such as RT-1 [6] and RT-2 [7] demonstrated that vision-language models pretrained on internet-scale data can be fine-tuned for robotic manipulation, mapping visual observations and language to action sequences. Subsequent work has scaled this paradigm through cross-embodiment training: the Open X-Embodiment dataset [12] aggregates demonstrations from dozens of robot morphologies, enabling models like RT-X [12] to generalize across diverse manipulators. More recent robot foundation models [2, 26] such as Octo [34] and _π_ 0 [3] incorporate flow-matching and diffusion architectures, achieving state-of-the-art performance on manipulation benchmarks spanning tabletop tasks, mobile manipulation, and dexterous control. 

These successes demonstrate that VLA policies can learn manipulation primitives that transfer across embodiments with different kinematics, workspaces, and end-effector designs. However, essentially all demonstrations in existing crossembodiment datasets operate from stable bases (fixed or mobile) in quasi-static regimes. No prior work has investigated whether these learned representations transfer to aerial platforms, where underactuated flight dynamics, large ego-motion, and contact-induced disturbances fundamentally differ from ground-robot scenarios. Our work provides the first systematic evaluation of this transfer gap. 

## _B. Vision-Language and Vision-Language-Action Models for UAV Navigation_ 

Vision-language models have recently been applied to drone navigation [46], typically for high-level semantic reasoning rather than low-level visuomotor control. VLMaps [23] constructs semantic maps for language-conditioned robot navigation but act as a perception and planning front-end rather than an end-to-end policy. SEEK [17] and VISTA [33] demonstrate uncertainty-aware exploration from semantic goals on quadrupeds and drones, but are limited to object localization and do not extend to interaction or contact. More recently, SINGER [1] introduces an end-to-end visuomotor policy for language-conditioned drone navigation trained on synthetic trajectories in Gaussian Splatting environments, achieving onboard inference through semantic image preprocessing with CLIPSeg [32]. GRaD-Nav++ [9] extends this approach with differentiable dynamics in Gaussian Splatting scenes, enabling multi-task generalization across navigation behaviors. Both methods demonstrate impressive sim-to-real transfer for navigation tasks. 

In contrast to SINGER and GRaD-Nav++, which focus on language-conditioned navigation without contact and use Gaussian Splatting primarily as a training environment, our work targets aerial manipulation with an onboard gripper, uses Gaussian Splatting as a source of synthetic demonstration data for a specific navigation subtask, and explicitly studies how a foundation VLA policy can be leveraged when navigation and manipulation must be composed in a single language-specified behavior. 

## _C. Aerial Manipulation with Learned Policies_ 

Unmanned aerial manipulation (UAM) combines multirotor flight with contact-rich interaction, introducing challenges such as underactuated dynamics, aerodynamic disturbances near surfaces, and strict payload limits. Classical systems demonstrate contact-based tasks including surface inspection [41, 5], painting [42, 18, 29], drilling [14], and object grasping [16, 45], typically using carefully engineered controllers tailored to specific scenarios. Recent work has explored learning-based approaches: model-free reinforcement learning for aerial manipulation [13], one-shot learning for autonomous grasping [49], and image-based visual servoing [40, 28]. However, these methods either lack language grounding or are limited to single tasks without generalization across manipulation primitives. 

Most relevant to our work, UMI-on-Air [19] addresses the challenge of transferring manipulation policies to aerial platforms by training a single-task diffusion policy on handheld UMI demonstrations and introducing embodiment-aware guidance at inference time: gradient feedback from a lowlevel MPC controller steers trajectory generation toward dynamically feasible actions during deployment. This approach achieves impressive results on high-precision aerial manipulation tasks. 

Compared to UMI-on-Air, which studies a single-task diffusion policy trained from handheld UMI demonstrations and introduces embodiment-aware guidance at inference time via MPC gradients, AirVLA studies cross-embodiment transfer in a generalist VLA foundation model ( _π_ 0) fine-tuned on aerial manipulation data. While both methods use guidance at inference time, AirVLA evaluates a broader set of tasks spanning manipulation, navigation, and the zero-shot composition of both. This design lets us isolate and study the representational generalization limits of existing VLA models for aerial manipulation and navigation. 

More broadly, while prior aerial manipulation work either (i) relies on task-specific controllers without language grounding or (ii) uses cross-embodiment guidance to make existing policies feasible on drones, none of these efforts evaluate a generalist VLA manipulation model on a unified suite of pickand-place, navigation, and compositional aerial tasks the way AirVLA does. 

## III. METHOD 

## _A. System Overview_ 

AirVLA is a vision-language-action system for aerial manipulation that transfers manipulation capabilities from foundation models pretrained on fixed-base robot arms to an underactuated quadrotor platform. The system takes as input RGB images from multiple viewpoints and a natural language task description, and outputs relative end-effector pose commands executed by a low-level flight controller. 

The key challenge in this transfer is the mismatch between the quasi-static regimes of tabletop manipulation and aerial manipulation, where the platform must continuously stabilize 


Fig. 2: Custom gripper installed on the Starling 2 Max drone. The design prioritizes low weight for extended flight time while maintaining sufficient grip strength for the target objects. 

against gravity while simultaneously executing precise gripper motions. Grasping an object introduces a step change in effective mass that, if uncompensated, causes the drone to sag and potentially fail the task. 

Our approach addresses this challenge through two main contributions: (1) a physics-aware guidance mechanism that augments the pretrained policy’s action generation process with payload-aware vertical compensation at inference time, and (2) a Gaussian-splatting data pipeline that enables efficient collection and synthesis of diverse training trajectories from a small number of seed flights. Together, these allow a VLA model pretrained on large-scale robot manipulation data to perform aerial pick-and-place and navigation with minimal drone-specific fine-tuning. 

## _B. Hardware_ 

The system integrates the ModalAI Starling 2 Max drone with a customized Universal Manipulation Interface (UMI) gripper [11] and multiple cameras to enable autonomous aerial manipulation. The Starling 2 Max is powered by the VOXL 2 companion computer (Qualcomm QRB5165). The customized UMI-style gripper is attached to the underside of the drone, enabling dynamic grasping. The system integrates one external camera and two onboard cameras (downward and forwardfacing), providing RGB images at 5Hz. 

_1) Gripper Design:_ We showcase the design of our gripper in Fig. 2. The gripper is designed to be built cheaply without specialized tools. The frame is entirely 3D printed, with two hobby-grade servos slotting in without screws. The fingers are adapted from the UMI gripper [11], facilitating direct comparison with arm-based policies trained with similar endeffector geometry. 

_2) Observation and Action Spaces:_ The observation space consists of RGB images from three cameras at [256 _×_ 256] resolution, the drone’s estimated pose from a motion capture system, and gripper aperture. The action space, consisting of the drone position and yaw, is represented as an action chunk _A ∈_ R<sup>_H×D_</sup> (i.e., end-effector 4 DoF delta poses and gripper commands _D_ over horizon _H_ ). Actions are generated at 10 

Hz and executed by the PX4 flight controller via position setpoints. 

## _C. Policy Architecture:_ 

We build on _π_ 0 [3], a vision-language-action model that represents the conditional action distribution using a flowmatching (continuous-time) generative model [30]. Given an observation _o_ (images, proprioception, language), _π_ 0 defines a velocity field _vθ_ ( _xτ , o, τ_ ) over latent action chunks _xτ ∈_ R<sup>_H×D_</sup> and diffusion/flow time _τ ∈_ [0 _,_ 1]. Sampling draws _x_ 0 _∼N_ (0 _, I_ ) and integrates the ODE 


to obtain the generated action chunk _A_ = _x_ 1. 

For real-time execution, we employ Real-Time Chunking (RTC) [4], which enables asynchronous inference by _freezing_ the prefix of the next chunk that will execute before inference completes, and _inpainting_ the remaining suffix conditioned on the frozen prefix. Concretely, RTC defines a soft temporal mask over the horizon that blends previously committed actions with newly generated actions to avoid discontinuities at chunk boundaries. 

## _D. Physics-Aware Guidance for Action Generation_ 

RTC shows that inference-time steering can be implemented by modifying the velocity field during sampling [4]. We generalize this idea by introducing a loss Φ( _A_ ; _o_ ) over the _denoised_ action chunk _A_ = _x_ 1, and adding a gradient correction term derived from _∇A_ Φ to the base velocity field, analogous in spirit to gradient-based guidance methods in generative modeling [22, 38]. Intuitively, we seek samples that both (i) have high probability under the base policy and (ii) minimize the guidance loss: 


This formulation seeks a ’sweet spot’ between the policy’s priors and physical constraints. It biases the sampling process toward actions that are high-probability under the VLA (preserving learned manipulation skills) while simultaneously minimizing the cost Φ (enforcing flight feasibility), effectively steering the drone at runtime without retraining. 

Operationally, at intermediate time _τ_ , we compute the model’s current prediction of the terminal action chunk _A_ ˆ _θ_ ( _xτ , o, τ_ ) _≈ x_ 1 (e.g., via the model’s internal denoised estimate), evaluate the gradient _∇A_ Φ( _A_<sup>ˆ</sup> _θ_ ; _o_ ), and map it back to a correction in latent space through a vector–Jacobian product _ξ_ := � _∇xτ A_<sup>ˆ</sup> _θ_ ( _xτ , o, τ_ )� _⊤∇A_ Φ� _A_ ˆ _θ_ ( _xτ , o, τ_ ); _o_ �. This yields the guided velocity field 


where _s_ ( _τ_ ) is a scalar guidance schedule. Multiple loss terms compose additively because _−_ log _p_ guid adds losses, so RTC-style continuity objectives and task-specific physics objectives can be applied simultaneously without changing the pretrained model weights. 

_1) General Tracking-Error Guidance:_ Suppose we have a reference trajectory _A_<sup>des</sup> ( _o_ ) _∈_ R<sup>_H×D_</sup> derived from the current observation. We define a tracking loss 


with per-dimension strengths _λd ≥_ 0 and temporal weights _wt ≥_ 0. The temporal weights follow the soft masking schedule from RTC [4]: _wt_ = 1 for frozen prefix actions, the weights then exponentially decay for the intermediate region and are zero for freshly generated actions. This ensures the guidance strongly enforces continuity with committed actions while allowing freedom for new generation. The corresponding gradient correction is derived from 


which pulls the denoised chunk toward the reference trajectory in each dimension proportionally to _λd_ . 

_2) Payload-Aware Vertical Guidance:_ In aerial manipulation, the dominant disturbance during grasping is an effective mass increase that manifests as vertical sag under load. Rather than modeling full 6-DOF dynamics, we instantiate (4) only on the altitude-related action dimension _dz_ : 


where _zt_ ( _A_ ) denotes the _z_ -component of the action at timestep _t_ , and 


biases the drone toward slightly higher altitude under load (∆ _z >_ 0). Here _z_ curr( _o_ ) comes from a motion capture system, and ∆ _z_ is a tuned offset capturing the expected sag for typical payloads. 

The payload confidence _α_ ( _o, At−_ 1) _∈_ [0 _,_ 1] is computed from (i) the previously executed action chunk _At−_ 1 and (ii) the current measured gripper aperture in _o_ . Concretely, we compute a smooth, bounded payload confidence by combining recent gripper command intent with the current measured aperture. Let _ut ∈_ [ _−_ 1 _,_ 1] denote the gripper command at timestep _t_ (with +1 corresponding to “close”), and let _g_ ( _o_ ) _∈_ [0 _,_ 1] denote the measured aperture (normalized so that larger values are more open). From the previously executed chunk _At−_ 1, we form continuous close/open intents using the last _K_ commands, 


and compute soft aperture-based scores _c_ meas _, o_ meas _∈_ [0 _,_ 1] from _g_ ( _o_ ) (higher when the gripper is closed/open, respectively). We then define an “open” gate and payload confidence 

## as 


When _α ≈_ 0, the loss vanishes and sampling reduces to vanilla RTC; when _α ≈_ 1, the sampler prefers chunks whose vertical component is biased toward _z_ des, compensating for payload. This can be viewed as mode-dependent feedforward (gain scheduling / gravity compensation), but injected _inside_ the generative policy’s sampling dynamics by adding the gradient correction term derived from _∇A_ Φpayload via (3). 

## _E. Gaussian Splat Data Pipeline_ 

Collecting aerial manipulation demonstrations is timeconsuming and requires skilled pilots. To efficiently generate diverse training data, we adopt a “Flying in Gaussian Splats”style approach that couples photorealistic Gaussian-splatting reconstructions with a lightweight drone dynamics model to synthesize large volumes of training data from a small set of seed demonstrations [31]. Concretely, our pipeline proceeds by first reconstructing the static environment as a Gaussian Splat and isolating the gripper visuals to prevent observation bias. We then couple a drone dynamics model with these assets to synthesize diverse, physics-feasible training trajectories that cover both nominal navigation and recovery behaviors. 

_1) Scene Reconstruction:_ We reconstruct each scene from short walk-throughs captured with the drone’s forward-facing camera. This results in a set of metrically scaled poses for each image, which are used to train a 3D Gaussian splatting model [24] using Nerfstudio [39, 44]. The resulting model _GS ϕ_ renders photorealistic images from arbitrary camera poses in the captured region. Given a camera pose ( _p, q_ ), the rendered image is _I_ = _GS ϕ_ ( _p, q_ ) _._ 

_2) Gripper Segmentation and Compositing:_ The downward-facing camera provides critical visual information for manipulation, but the gripper is persistently visible in its field of view. Including raw downward facing images in the synthetic training data from the Gaussian splatting model would introduce an observation bias into the policy that would result in unwanted behavior. Thus, we explicitly treat the gripper as a separate foreground layer and composite it onto renders from a gripper-free scene model. Concretely, for each downward-facing training frame _I_ down, we compute a gripper mask _M_ grip using Segment Anything (SAM) [27, 36] with a fixed bounding box prompt corresponding to the gripper’s known image-space location. We then extract a masked gripper patch 


to form a small library _{Ga}_ of representative gripper appearances. 

We train the Gaussian splatting model _GS ϕ_ on images from cameras where the gripper is not visible (namely, the forwardfacing views). At synthesis time, we render the clean scene from _GS ϕ_ for the downward-facing viewpoint and composite the gripper foreground: 


This yields a downward-view image whose background is fully determined by the scene model, while the gripper appearance is consistent with the commanded aperture _a_ ( _t_ ). 

_3) Drone Dynamics Model:_ Following [31], we simulate drone motion with a semi-kinematic state _x_ = ( _p_<sup>_W_</sup> _, v_<sup>_W_</sup> _, qB_<sup>_W_)</sup> comprising position, velocity, and orientation quaternion. Controls are normalized thrust _f_ th and body angular velocity _ω_<sup>_B_</sup> . The dynamics are 


where _g_ is gravitational acceleration, _e_<sup>_W_</sup> 3<sup>_, eB_</sup> 3<sup>arethe</sup><sup>_z_-axis</sup> unit vectors in world/body frames, _R_ ( _·_ ) converts quaternion to rotation, and ( _k_ th _, m_ ) are thrust coefficient and mass. We forward-integrate using ACADOS [43] and render images using the body-to-camera transform _TC_<sup>_B_.</sup> 

_4) Domain-Randomized Data Synthesis:_ To enable the policy to recover from dangerous states near the obstacle, we additionally synthesize recovery trajectories by randomizing task geometry, similar to FiGS [31]. For each nominal trajectory ( _X_<sup>_d_</sup> _, U_<sup>_d_</sup> ), we generate _Ns_ randomized rollouts by sampling an initial state perturbation _x_<sup>_s_</sup> 0<sup>_∼U_(</sup><sup>_xd_</sup> 0<sup>_−_∆</sup><sup>_x,xd_</sup> 0<sup>+ ∆</sup><sup>_x_),then</sup> simulating the resulting trajectory rendering multi-view images from the Gaussian splat scene model _GS ϕ_ . 

We additionally randomize intermediate waypoints to increase diversity and induce recovery behaviors. For the navigation task, we randomize the terminal hover location to lie above the goal by sampling a height offset uniformly in [1 _._ 0 _,_ 1 _._ 5] meters. Let _p_ obj denote the object goal position in the scene and let _h ∼U_ (1 _._ 0 _,_ 1 _._ 5) m. We set the goal position as 


To diversify gate exits, we randomize the post-gate waypoint within a ball of diameter 0 _._ 25 m centered at a nominal aftergate position waypoint _p_<sup>_d_</sup> after<sup>.Withradius</sup><sup>_r_=0</sup><sup>_._125mand</sup> _δ ∼U_ (B(0 _, r_ )) where B(0 _, r_ ) = _{δ ∈_ R<sup>3</sup> : _∥δ∥_ 2 _≤ r}_ , we define 


Finally, we perturb trajectories to elicit recovery behavior by inserting an additional waypoint between the start and the gate that forces the drone to pass near one of four gate extremities, namely top, bottom, left, or right. We sample a side _s ∼_ Unif( _{_ top _,_ bottom _,_ left _,_ right _}_ ) and define a sidespecific waypoint 


where _p_ ¯ _s_ is a reference point near the corresponding gate boundary, _ns_ is the offset direction away from the gate frame, and _b >_ 0 is a fixed geometry buffer chosen to ensure collision-free clearance. 

After sampling these randomized waypoint targets, we generate controls by tracking the waypoint-conditioned plan under the drone dynamics, producing the rollout ( _X_<sup>_s_</sup> _, U_<sup>_s_</sup> ). Figure 


Fig. 3: Examples of synthetic trajectories used to generate training data. Nominal rollouts and corrective rollouts overlay sampled trajectories in the gate-manipulation scene. 

3 depicts nominal and corrective synthetic trajectories for both the left gate and right gate scenarios. We render images along _X_<sup>_s_</sup> from _GS ϕ_ using the body-to-camera transform _TC_<sup>_B_,</sup> and composite the gripper for downward-facing views. This procedure yields a large set of physically and geometrically plausible trajectories that cover both nominal executions and off-nominal approaches requiring recovery near the gate. 

## IV. EXPERIMENTS 

To evaluate our methods, we define a task-specific score rubric, report quantitative results under that rubric, and organize experiments to isolate the contribution of pretraining transfer, inference-time stabilization, and data augmentation. Through our experiments, we seek to study the following questions: 

- 1) **Transfer:** How much manipulation-pretrained VLA capability transfers to an underactuated aerial manipulator after fine-tuning? 

- 2) **Inference-time control:** Can real-time chunking (RTC) and payload-aware guidance reduce the sensitivity of aerial execution to chunk discontinuities and payload disturbances? 

- 3) **Data synthesis:** Does Gaussian-splat-based synthetic navigation augmentation improve real-world navigation performance? 

- 4) **Compositionality:** Can a single policy reliably compose navigation and grasping into a multi-stage task (navigate-then-grasp)? 

## _A. Task suite_ 

We evaluate using the following task prompts: 

- **Penguin Grasp (Pick-and-Place):** pick up the stuffed animal and put it in the blue bin. 

TABLE I: **Single Task Performance Benchmarks (%).** Each method was evaluated across twenty trials per task. 

|**Method**|**Pengui**|**n Grasp**|**Navigation **|**(Non-Synthetic)**|**Navigat**|**ion (Synthetic)**|
|---|---|---|---|---|---|---|
||Pick|Place|Gate|Hover|Gate|Hover|
|_π_0 naive|50.0|0.0|50.0|60.0|45.0|100.0|
|_π_0 + RTC|85.0|23.5|80.0|81.2|95.0|100.0|
|_π_0 + RTC w/ payload-aware guidance (ours)|100.0|50.0|–|–|–|–|
|ACT|0.0|0.0|0.0|0.0|0.0|0.0|
|Diffusion Policy|10.0|0.0|15.0|0.0|0.0|0.0|


- **Gate Navigation:** fly through the gate and hover over the stuffed animal. 

- **Compositional (Navigate-then-Grasp):** fly through the gate and hover over the stuffed animal and then pick up the stuffed animal and put it in the blue bin. 

The penguin grasp task evaluates the model’s ability to transfer manipulation skills from pretraining to a drone embodiment. To ensure robustness, we vary the object’s position within a box during both data collection and evaluation. The gate navigation task tests drone-specific navigation requiring explicit obstacle avoidance. By using two different gate positions (left and right), we force the policy to localize the gate prior to navigation. Finally, to test the model’s ability to handle novel, composite tasks in a zero-shot manner, we fine-tune the policy on the combined datasets and evaluate it using a combined prompt unseen during training. 

## _B. Evaluation rubric and protocol_ 

For each task, we define a rubric that measures progress toward completion. In our setting, the primary metric is binary task success, and we additionally record a diagnostic failure taxonomy to attribute failures for qualitative analysis: 

- **Penguin Grasp:** a two stage task with success markers triggered after (1) picking up the stuffed animal and (2) placing it in the bin. Failure modes include grasping followed by immediate drops or crashes as well as failure to pick. 

- **Gate Navigation:** a two stage task with success markers triggered after (1) navigating through the gate and (2) holding a hover over the stuffed animal. Failure modes include passing through the gate but not hovering over the penguin, and crashing or failing to pass through the gate. 

- **Compositional Navigate and Grasp:** a four stage task combining the success and failure markers for the above with an additional failure marker of _incorrect subtask order_ (attempted grasp before passing the gate). 

## _C. Methods compared_ 

We compare the following methods: 

- _π_ 0 **naive:** roll out action chunks, pausing for inference at the end of each action chunk. 

- _π_ 0 **+ RTC:** real-time chunking that re-samples suffix actions to avoid discontinuities [4]. 

- _π_ 0 **+ RTC + payload-aware guidance (ours):** inferencetime steering implemented via a gradient correction term applied inside the sampler dynamics [4]. 

- **ACT** [47] and **Diffusion Policy** [10] 

For the navigation and compositional tasks, we additionally evaluate **synthetic** and **non-synthetic** variants, corresponding to whether the policy was trained with synthetic data augmentation. Training details for these methods are provided in Appendix VII-A. 

## _D. Quantitative results_ 

Each of the above methods are evaluated across twenty trials per task for a cumulative 460 flight trials. We omit evaluations of the payload-aware guidance method on pure navigation tasks, as the guidance method is identical to RTC when objects are not being manipulated. We present the results of these evaluations in Tables I and II. The reported success rates are conditioned on the number of trials that succeeded in the prior stage of the task. For example, the place success rate is conditioned on the number of trials that succeeded in picking the object. 

To evaluate generalization to novel objects, we conduct 10 additional pick-and-place trials, replacing the objects used during training with previously unseen ones. Furthermore, to assess spatial robustness, we vary the gate location across three regions (front, left, and right). We conduct five trials per region, shifting and rotating the gate within each area. These out-of-distribution results are detailed in Table III. We discuss these results further in Appendix VII-B, and interpret them as evidence of partial semantic transfer together with substantial overfitting in the small-data fine-tuning regime for navigation. 

## _E. Analysis_ 

**Inference-time structure is critical for aerial pick-andplace.** Naive fine-tuning is insufficient for full pick-and-place success, attaining 0%, with failures dominated by missed grasps and post-contact disturbances. RTC improves success (up to 23 _._ 5%) by stabilizing execution across chunk boundaries, and payload-aware guidance further improves success (up to 50%), consistent with the need to compensate for payload-induced altitude sag and other underactuated dynamics. Although the pick-and-place task is deliberately constrained relative to unconstrained 6-DoF aerial manipulation, it remains challenging for end-to-end visuomotor learning, as reflected in the poor performance of ACT and Diffusion Policy. This suggests that embodiment-specific adaptation, 

TABLE II: **Compositional Navigate-then-Grasp Success (%).** Each method was evaluated across twenty trials per task. 

|**Data Setting**|**Method**|**Gate**|**Hover**|**Pick**|**Place**|
|---|---|---|---|---|---|
||_π_0 naive|35.0|85.7|42.9|0.0|
||_π_0 + RTC|80.0|100.0|81.2|15.4|
|No Synthetic|_π_0 + RTC w/ payload-aware guidance (ours)|70.0|100.0|100.0|35.7|
||ACT|0.0|0.0|0.0|0.0|
||Diffusion Policy|5.0|0.0|0.0|0.0|
||_π_0 naive|70.0|85.7|25.0|0.0|
||_π_0 + RTC|95.0|94.7|83.3|20.0|
|Synthetic|_π_0 + RTC w/ payload-aware guidance (ours)|85.0|100.0|94.1|62.5|
||ACT|25.0|0.0|0.0|0.0|
||Diffusion Policy|0.0|0.0|0.0|0.0|


TABLE III: **Out-of-Distribution (OOD) Robustness (%).** Success rates for variations in object class and gate positioning. _Place_ and _Hover_ are reported as conditional percentages. 

|**Grasp (Ob**|**ject Va**|**riation)**|**Navigation (Gate **|**Locations)**|
|---|---|---|---|---|
|**Object**|**Pick**|**Place**|**Location**<br>**Gate**|**Hover**|
|Chips|10.0|0.0|Front<br>0.0|–|
|Sandwich|70.0|57.1|Left<br>0.0|–|
|Box|30.0|33.3|Right<br>40.0|100.0|


object. However, performance varies by object geometry: the model achieved only a 10% pick success rate with a bag of chips, compared to 70% for the sandwich. The primary failure mode was the policy’s inability to adapt grasp poses to the chip bags geometry. In the navigation task, the policy adapts best to the ”right” region (40% success). Conversely, trials in the ”front” and ”left” regions failed completely. Specifically, the drone consistently bypassed the gate in front-region trials, while left-region trials resulted in collisions due to incomplete position adaptation. 

## V. LIMITATIONS AND FUTURE WORK 

such as payload-aware guidance, is necessary to achieve reliable success even in controlled top-down grasping due to the underactuated flight dynamics. 

**RTC substantially improves gate navigation.** In the nonsynthetic gate navigation trials, RTC increases gate traversal success from 50% to 80% and from 45% to 95% in the synthetic gate navigation trials. This indicates that RTC is not merely helpful but necessary for reliable navigation, since re-planning at runtime mitigates compounding errors during aggressive motion. 

**Synthetic augmentation helps most when paired with RTC.** In the synthetic setting, naive performance is asymmetric across gates while _π_ 0+RTC achieves 95% success at the gate traversal component of the task. This suggests that synthetic augmentation is valuable but insufficient on its own: it expands coverage of approaches and recoveries, while reliable deployment still depends on inference-time stabilization from RTC. Qualitatively, we observed that the policy would periodically fall back on ”synthetic modes” that replay the GS-generated trajectories, ensuring successful gate traversal. 

**Compositional tasks reveal an ability to generalize from atomic tasks.** Our method shows a strong ability to generalize to compositional tasks in a zero-shot matter attaining a 62% overall conditioned success rate. The compositional task evaluations further highlight the importance of closed-loop policy inference as well as the necessity of GS synthetic trajectories to ensure successful gate traversal. 

**Out-of-distribution trials demonstrate generalization capabilities.** Our method generalizes effectively in pick-and-place tasks, achieving up to 57% task success on a novel sandwich 

We present AirVLA, the first systematic evaluation of transferring a manipulation-pretrained VLA foundation model to an aerial platform. Our results provide a nuanced answer to the challenge of cross-embodiment transfer: while the visual and semantic representations of models like _π_ 0 transfer robustly to drone viewpoints, the intricate dynamics of aerial manipulation require specific interventions. By integrating payload-aware guidance directly into the flow-matching sampling loop, we improve single-task placement success from 0% (naive baseline) to 50%, reconciling the generative diversity of a VLA with the strict physical constraints of flight. Furthermore, we show that the policy can execute compositional tasks in a zeroshot manner, achieving 85% gate traversal and up to 62.5% place success rates. Although our method currently relies on motion capture to isolate the cross-embodiment transfer problem from localization engineering issues; future work will replace this dependency with onboard VIO or SLAM. Doing so would expand the operating domain to settings such as multi-room navigation that are difficult to study under motion capture. Finally, our out-of-distribution evaluations highlight a disparity in generalization: while the model achieves 57% success on novel object classes, the lower 40% success rate in novel navigation scenarios indicates that significantly more data is needed to enable robust aerial navigation. 

## VI. ACKNOWLEDGMENTS 

The authors would like to thank Timothy Chen and Ola Shorinwa for their advice and reviews in the paper writing stage. This work was supported in part by a gift from Google, NSF grant FRR 2342246, and ONR grant N00014-23-1-2354. 

REFERENCES 

- [1] Maximilian Adang, JunEn Low, Ola Shorinwa, and Mac Schwager. Singer: An onboard generalist visionlanguage navigation policy for drones. _arXiv preprint arXiv:2509.18610_ , 2025. 

- [2] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [3] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, and et al. _π_ 0: A vision-language-action flow model for general robot control, Nov 2024. URL https://doi.org/10.48550/arXiv. 2410.24164. 

- [4] Kevin Black, Manuel Y Galliker, and Sergey Levine. Real-time execution of action chunking flow policies. _arXiv preprint arXiv:2506.07339_ , 2025. 

- [5] Karen Bodie, Maximilian Brunner, Michael Pantic, Stefan Walser, Patrick Pf¨andler, Ueli Angst, Roland Siegwart, and Juan Nieto. An omnidirectional aerial manipulation platform for contact-based inspection. _arXiv preprint arXiv:1905.03502_ , 2019. 

- [6] Anthony Brohan et al. Rt-1: Robotics transformer for real-world control at scale. In _arXiv preprint arXiv:2212.06817_ , 2022. 

- [7] Anthony Brohan et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _arXiv preprint arXiv:2307.15818_ , 2023. 

- [8] Remi Cadene, Simon Alibert, Alexander Soare, Quentin Gallouedec, Adil Zouitine, Steven Palma, Pepijn Kooijmans, Michel Aractingi, Mustafa Shukor, Dana Aubakirova, Martino Russi, Francesco Capuano, Caroline Pascal, Jade Choghari, Jess Moss, and Thomas Wolf. Lerobot: State-of-the-art machine learning for real-world robotics in pytorch. https://github.com/huggingface/ lerobot, 2024. 

- [9] Qianzhong Chen, Naixiang Gao, Suning Huang, JunEn Low, Timothy Chen, Jiankai Sun, and Mac Schwager. Grad-nav++: Vision-language model enabled visual drone navigation with gaussian radiance fields and differentiable dynamics. _arXiv preprint arXiv:2506.14009_ , 2025. 

- [10] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 

- [11] Cheng Chi, Zhenjia Xu, Chuer Pan, Eric Cousineau, Benjamin Burchfiel, Siyuan Feng, Russ Tedrake, and Shuran Song. Universal manipulation interface: Inthe-wild robot teaching without in-the-wild robots. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

- [12] Open X-Embodiment Collaboration et al. Open X- Embodiment: Robotic learning datasets and RT-X models. https://arxiv.org/abs/2310.08864, 2023. 

- [13] Eugenio Cuniato, Ismail Geles, Weixuan Zhang, Olov Andersson, Marco Tognon, and Roland Siegwart. Learning to open doors with an aerial manipulator. In _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 6942–6948. IEEE, 2023. 

- [14] Caiwu Ding, Lu Lu, Cong Wang, and Caiwen Ding. Design, sensing, and control of a novel uav platform for aerial drilling and screwing. _IEEE Robotics and Automation Letters_ , 6(2):3176–3183, 2021. 

- [15] Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, et al. Libero-plus: In-depth robustness analysis of vision-language-action models. _arXiv preprint arXiv:2510.13626_ , 2025. 

- [16] Vaibhav Ghadiok, Jeremy Goldin, and Wei Ren. Autonomous indoor aerial gripping using a quadrotor. In _2011 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 4645–4651. IEEE, 2011. 

- [17] Muhammad Fadhil Ginting, Sung-Kyun Kim, David D Fan, Matteo Palieri, Mykel J Kochenderfer, and Ali-akbar Agha-Mohammadi. Seek: Semantic reasoning for object goal navigation in real world inspection tasks. _arXiv preprint arXiv:2405.09822_ , 2024. 

- [18] Xiaofeng Guo, Guanqi He, Jiahe Xu, Mohammadreza Mousaei, Junyi Geng, Sebastian Scherer, and Guanya Shi. Flying calligrapher: Contact-aware motion and force planning and control for aerial manipulation. _IEEE Robotics and Automation Letters_ , 2024. 

- [19] Harsh Gupta, Xiaofeng Guo, Huy Ha, Chuer Pan, Muqing Cao, Dongjae Lee, Sebastian Sherer, Shuran Song, and Guanya Shi. Umi-on-air: Embodiment-aware guidance for embodiment-agnostic visuomotor policies. _arXiv preprint arXiv:2510.02614_ , 2025. 

- [20] Huy Ha, Yihuai Gao, Zipeng Fu, Jie Tan, and Shuran Song. Umi on legs: Making manipulation policies mobile with manipulation-centric whole-body controllers. _arXiv preprint arXiv:2407.10353_ , 2024. 

- [21] Guanqi He, Yash Janjir, Junyi Geng, Mohammadreza Mousaei, Dongwei Bai, and Sebastian Scherer. Imagebased visual servo control for aerial manipulation using a fully-actuated uav. In _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2023. URL https://arxiv.org/pdf/2306.16530.pdf. 

- [22] Jonathan Ho and Tim Salimans. Classifier-free diffusion guidance, 2022. URL https://arxiv.org/abs/2207.12598. 

- [23] Chenguang Huang, Oier Mees, Andy Zeng, and Wolfram Burgard. Visual language maps for robot navigation. _arXiv preprint arXiv:2210.05714_ , 2022. 

- [24] Bernhard Kerbl, Georgios Kopanas, Thomas Leimk¨uhler, and George Drettakis. 3d gaussian splatting for real-time radiance field rendering. _ACM Trans. Graph._ , 42(4):139– 1, 2023. 

- [25] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ash- 

win Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 

- [26] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [27] Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C Berg, Wan-Yen Lo, et al. Segment anything. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 4015–4026, 2023. 

- [28] Maximilian Laiacker, Felix Huber, and Konstantin Kondak. High accuracy visual servoing for aerial manipulation using a 7 degrees of freedom industrial manipulator. In _2016 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 1631–1636, 2016. doi: 10.1109/IROS.2016.7759263. 

- [29] Christian Lanegger, Marco Ruggia, Marco Tognon, Lionel Ott, and Roland Siegwart. Aerial layouting: Design and control of a compliant and actuated end-effector for precise in-flight marking on ceilings. _Proceedings of Robotics: Science and System XVIII_ , page p073, 2022. 

- [30] Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling, 2023. URL https://arxiv.org/abs/2210.02747. 

- [31] JunEn Low, Maximilian Adang, Javier Yu, Keiko Nagami, and Mac Schwager. Sous vide: Cooking visual drone navigation policies in a gaussian splatting vacuum. _IEEE Robotics and Automation Letters_ , 10(5): 5122–5129, 2025. doi: 10.1109/LRA.2025.3553785. 

- [32] Timo L¨uddecke and Alexander Ecker. Image segmentation using text and image prompts. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 7086–7096, 2022. 

- [33] Keiko Nagami, Timothy Chen, Javier Yu, Ola Shorinwa, Maximilian Adang, Carlyn Dougherty, Eric Cristofalo, and Mac Schwager. Vista: Open-vocabulary, taskrelevant robot exploration with online semantic gaussian splatting. _arXiv preprint arXiv:2507.01125_ , 2025. 

- [34] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, 2024. 

- [35] Michael O’Connell, Guanya Shi, Xichen Shi, Kamyar Azizzadenesheli, Anima Anandkumar, Yisong Yue, and Soon-Jo Chung. Neural-fly enables rapid learning for agile flight in strong winds. _Science Robotics_ , 7(66): 

eabm6597, 2022. 

- [36] Tianhe Ren, Shilong Liu, Ailing Zeng, Jing Lin, Kunchang Li, He Cao, Jiayu Chen, Xinyu Huang, Yukang Chen, Feng Yan, et al. Grounded sam: Assembling openworld models for diverse visual tasks. _arXiv preprint arXiv:2401.14159_ , 2024. 

- [37] Pedro Sanchez-Cuevas, Guillermo Heredia, and Anibal Ollero. Characterization of the aerodynamic ground effect and its influence in multirotor control. _International Journal of Aerospace Engineering_ , 2017(1): 1823056, 2017. 

- [38] Jiaming Song, Arash Vahdat, Morteza Mardani, and Jan Kautz. Pseudoinverse-guided diffusion models for inverse problems. In _International Conference on Learning Representations_ , 2023. 

- [39] Matthew Tancik, Ethan Weber, Evonne Ng, Ruilong Li, Brent Yi, Terrance Wang, Alexander Kristoffersen, Jake Austin, Kamyar Salahi, Abhik Ahuja, et al. Nerfstudio: A modular framework for neural radiance field development. In _ACM SIGGRAPH 2023 conference proceedings_ , pages 1–12, 2023. 

- [40] Justin Thomas, Giuseppe Loianno, Koushil Sreenath, and Vijay Kumar. Toward image based visual servoing for aerial grasping and perching. In _2014 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 2113–2118, 2014. doi: 10.1109/ICRA.2014.6907149. 

- [41] Miguel Angel Trujillo, Jos´e Ramiro Mart´ınez-de Dios, Carlos Mart´ın, Antidio Viguria, and An´ıbal Ollero. Novel aerial manipulator for accurate and robust industrial ndt contact inspection: A new tool for the oil and gas inspection industry. _Sensors_ , 19(6):1305, 2019. 

- [42] Anurag Sai Vempati, Mina Kamel, Nikola Stilinovic, Qixuan Zhang, Dorothea Reusser, Inkyu Sa, Juan Nieto, Roland Siegwart, and Paul Beardsley. Paintcopter: An autonomous uav for spray painting on three-dimensional surfaces. _IEEE Robotics and Automation Letters_ , 3(4): 2862–2869, 2018. doi: 10.1109/LRA.2018.2846278. 

- [43] Robin Verschueren, Gianluca Frison, Dimitris Kouzoupis, Jonathan Frey, Niels van Duijkeren, Andrea Zanelli, Branimir Novoselnik, Thivaharan Albin, Rien Quirynen, and Moritz Diehl. acados—a modular open-source framework for fast embedded optimal control. _Mathematical Programming Computation_ , 14 (1):147–183, 2022. 

- [44] Vickie Ye, Ruilong Li, Justin Kerr, Matias Turkulainen, Brent Yi, Zhuoyang Pan, Otto Seiskari, Jianbo Ye, Jeffrey Hu, Matthew Tancik, et al. gsplat: An open-source library for gaussian splatting. _Journal of Machine Learning Research_ , 26(34):1–17, 2025. 

- [45] Haijie Zhang, Jiefeng Sun, and Jianguo Zhao. Compliant bistable gripper for aerial perching and grasping. In _2019 International Conference on Robotics and Automation (ICRA)_ , pages 1248–1253. IEEE, 2019. 

- [46] Yuhang Zhang, Haosheng Yu, Jiaping Xiao, and Mir Feroskhan. Grounded vision-language navigation for uavs with open-vocabulary goal understanding. _arXiv_ 

_preprint arXiv:2506.10756_ , 2025. 

- [47] Tony Z. Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware, 2023. URL https://arxiv. org/abs/2304.13705. 

- [48] Xueyang Zhou, Yangming Xu, Guiyao Tie, Yongchao Chen, Guowen Zhang, Duanfeng Chu, Pan Zhou, and Lichao Sun. Libero-pro: Towards robust and fair evaluation of vision-language-action models beyond memorization. _arXiv preprint arXiv:2510.03827_ , 2025. 

- [49] Claudio Zito and Eliseo Ferrante. One-shot learning for autonomous aerial manipulation. _Frontiers in Robotics and AI_ , 9:960571, 2022. doi: 10.3389/frobt.2022.960571. URL https://doi.org/10.3389/frobt.2022.960571. 

## VII. APPENDIX 

## _A. Training Details_ 

Here we provide training details for the fine-tuned _π_ 0 policies. The baseline methods were trained using the LeRobot [8] code base with default configurations. 

_1) Pretraining:_ We initialize from the public _π_ 0 base checkpoint [3], which is pretrained on large-scale multiembodiment robot manipulation data. 

_2) Fine-tuning:_ We fine-tune on our drone dataset consisting of 120 to 150 (or about 10 hours) of real demonstrations for the manipulation and navigation tasks, respectively. The navigation dataset is further augmented to 200 total trajectories via Gaussian-splat trajectories (Sec. III-E). Fine-tuning is performed for 30 _,_ 000 gradient steps using AdamW optimization with a cosine learning-rate schedule with warmup: the learning rate linearly warms up over the first 1 _,_ 000 steps to a peak value of 2 _._ 5 _×_ 10<sup>_−_5</sup> and then decays following a cosine schedule to 2 _._ 5 _×_ 10<sup>_−_6</sup> by the end of training. We use a global batch size of 32 and an action chunk horizon of _H_ = 50. Observations consist of three RGB views (one external, two bodymounted) and robot proprioception. Actions are represented in the dataset’s native 4-DoF plus gripper control space. During training, we pad both proprioception and actions to match the model’s expected dimensionality; at inference, we extract the first 7 action dimensions as the gripper is in the 7th dimension. _3) Inference Configuration:_ At inference time, for the vanilla implementation, actions are executed at 10 Hz and we run inference once every 50 executed actions (i.e., at 0 _._ 2 Hz). We use RTC [4] with a chunk horizon of _H_ = 25, using an exponential prefix-attention schedule with a prefix-attention horizon of 25 and 10 denoising steps per chunk. 

For payload-aware guidance (Sec. III-D), we set _λz_ = 0 _._ 5, ∆ _z_ = 0 _._ 15 m, and _wt_ = ( _t/_ ( _H −_ 1))<sup>_γ_</sup> with _γ_ = 1, concentrating guidance on later timesteps where post-grasp transport dominates. The payload indicator used to gate the vertical objective (Eq. 9) is computed via a deterministic heuristic from the previous chunk’s gripper command history together with the current gripper state: we average the last _K_ =4 gripper commands to obtain a continuous close/open intent score, combine command-based open intent with an aperture-based open score, and form the final payload flag as a clipped product of close intent and a soft closedness score derived from the measured gripper aperture. 

## _B. AirVLA Generalization_ 

A natural question after fine-tuning is how well the policy generalizes to out-of-distribution (OOD) settings. We probe this along three axes in our pick-and-place task: (i) novel object generalization, (ii) novel language prompt generalization, and (iii) novel environment generalization. We emphasize that these evaluations are not meant to demonstrate robust open-world aerial manipulation. Rather, they test whether a manipulation-pretrained VLA can retain useful behavior after transfer to an underactuated aerial platform. 

We ran experiments varying the object and fixing the language prompt in the pick-and-place task: “pick up the stuffed 


Fig. 4: Out-of-distribution objects used for generalization probes. From left to right: goomba, box, chips, and sandwich. The policy was fine-tuned on a penguin but evaluated on these novel objects to test object-level generalization beyond training instances. 


Fig. 5: **Trajectory visualization for the left gate task.** The top three rows display real-world RGB observations from external, forward, and downward cameras. The bottom two rows show corresponding synthetic views rendered from Gaussian Splats. 

animal and put it in the blue bucket”. When changing the stuffed animal from a penguin to a goomba (see Figure 4), we noticed that the policy would reliably attempt to pick the novel object as long as it was initially within the training region on the table. This suggests that the fine-tuned policy transfers a grasping behavior beyond the exact training sequence, but that task performance is tightly linked to a workspace prior such as familiar grasping regions on the table. 

To evaluate a wider range of novel objects, we varied the task prompt to match the object: “pick up the _<_ OBJECT _>_ and put it in the blue bin.” We detail the results of these evaluations in the main paper (see Table III). The objects used for these experiments are shown in Figure 4. An interesting qualitative observation from these evaluations is that the policy would attempt to pick objects in the training region even when no prompt was supplied. This indicates that part of the behavior may be driven by a strong visuomotor prior (i.e. “if an object is 

present, attempt to grasp it”) rather than language grounding. Naturally, such behavior begs the question of how well would the policy perform in the presence of distractor objects. To test this, we repeated the penguin grasp task with an additional out-of-distribution object within the training region. We noticed that regardless of the relative positions within the training region, the policy moved the drone to attempt grasps on the penguin rather than the distractor. This shows that fine-tuning can still induce useful object discrimination in manipulation, even when overall OOD robustness remains limited. 

Overall, we view these results as evidence of partial transfer rather than broad generalization. The manipulation OOD results suggest that the pretrained VLA can still produce useful outputs under variation in object class, while the navigation OOD results in the main paper show substantial overfitting to the demonstration data and highlight the difficulty of 

cross-embodiment transfer when the pretrained model has not encountered a similar task. This interpretation is consistent with recent results showing that VLA models do not typically exhibit generalized zero-shot behavior after supervised finetuning, especially in the small-data regime [15, 48]. Instead, a more realistic promise of VLAs is that supervised fine-tuning can enable few-shot adaptation to related new tasks. 

We hypothesize that the limitations observed in these probes are partly driven by data scarcity (about 270 teleoperation demonstrations across all tasks), which can encourage reliance on workspace priors and habitual action routines. As larger and more diverse robot datasets become available, spanning broader embodiments, objects, and environments, we expect models such as AirVLA to improve generalization across each of the settings tested here. In future work, we will test this hypothesis by scaling demonstrations and measuring OOD performance as a function of data diversity and coverage. 

