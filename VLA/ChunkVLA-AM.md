---
title: "ChunkVLA-AM: Parallel Action Chunking for Vision-Language-Action Robot Control in Additive Manufacturing"
date: "2026-10-01"
authors: "Zhugang Liu; Kaichuang Zhang; Jinman Zhang; Pu Sun; Martha Asare; Jose Hernandez"
url: https://arxiv.org/abs/2610.01856
pdf: https://arxiv.org/pdf/2610.01856
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2610.01856)** / [論文ページ](https://arxiv.org/abs/2610.01856)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# ChunkVLA-AM: Parallel Action Chunking for Vision-Language-Action Robot Control in Additive Manufacturing 

|Zhugang Liu<sup>1</sup>|Kaichuang Zhang<sup>3</sup><br>Jinman Zhang<sup>1</sup><br>Pu Sun<sup>4</sup>|Martha Asare<sup>1</sup>|
|---|---|---|
|zhugang.liu01@utrgv.edu<br>Jose Hernandez<sup>2</sup>|kaichuangzhang@usf.edu<br>jinman.zhang01@utrgv.edu<br>psun9932@sdsu.edu<br>m<br>Maxim Ermolinsky<sup>2</sup><br>Efren Saenz<sup>1</sup><br>Qi Lu<sup>1</sup>|artha.asare01@utrgv.edu<br>Jinghao Yang<sup>2</sup><sup>_,∗_</sup>|
|jose.hernandez112@utrgv.edu<br>2Dep|maxim.ermolinsky01@utrgv.edu<br>efren.saenz01@utrgv.edu<br>qi.lu@utrgv.edu<br>1Department of Computer Science, The University of Texas Rio Grande Valley<br>artment of Electrical and Computer Engineering, The University of Texas Rio Grande Valle<br>3Department of Electrical Engineering, University of South Florida<br>4Department of Computer Science, San Diego State University<br>_∗_Corresponding Author|jinghao.yang@utrgv.edu<br>y|


**_Abstract_ —Vision–language–action (VLA) models unify visual perception, language understanding, and action generation, offering new opportunities for automation in additive manufacturing (AM). However, deployment in AM remains challenging because adapting these models to unseen robot embodiments is costly, and performance can degrade under environment changes. In this work, we present a framework for deploying OpenVLA-OFT on a FAIRINO FR3 robot in a fixed AM workcell. A data pipeline converts monocular real-world demonstrations into OpenVLAcompatible TFDS/RLDS datasets to support adaptation to the FR3 embodiment. At runtime, each inference request predicts an eight-step chunk of 7-D actions. The FR3 executes each chunk open loop before capturing a new observation, providing closedloop feedback between chunks. The system uses a cloud–edge architecture in which the FR3 client streams observations to a remote inference server through a FastAPI interface. In 42 physical A-to-B object-transfer trials, evenly split between red and blue targets, the system succeeded in 39 (92.9%). All three failures occurred during final placement, when insufficient release-height control caused the object to topple. An illumination sweep identified a low-error luminance range of 85–125 on a 0–255 scale, with the lowest mean spatial error at 95.** 

**_Index Terms_ —vision-language-action model, additive manufacturing, robot manipulation, action chunking, OpenVLA** 

## I. INTRODUCTION 

Additive manufacturing (AM) has become an important production paradigm for rapid prototyping, customized medical devices, aerospace components, and high-value industrial parts [1]–[3]. Beyond deposition itself, practical AM workflows require inspection, part retrieval, build-plate handling, post-processing, and occasional intervention after process failures. These operations can expose human operators to process-specific risks: fused deposition modeling (FDM) may emit ultrafine particles and volatile organic compounds during heated thermoplastic extrusion [4], [5], while selective laser melting (SLM) involves fine metallic powders and particulatematter hazards [6]. Robotic automation is therefore attractive 

for AM workcells because it can improve repeatability and reduce human exposure during inspection, transfer, and failure response. However, conventional rule-based robot programs are difficult to reuse across different printers, robot platforms, camera configurations, lighting conditions, object poses, and defect types such as FDM warping, inter-layer delamination, SLM porosity, lack-of-fusion holes, and cracks [7]–[9]. 

Vision-language-action (VLA) models provide a possible route toward more flexible AM robotic systems. By mapping visual observations and natural-language task descriptions directly to robot actions, VLA policies can represent tasks such as “retrieve the printed part,” “inspect the warped edge,” or “move the build-plate sample to the cooling area” without requiring a separate perception pipeline and a handcrafted state machine. Recent systems including RT-1, RT-2, Open X- Embodiment, and OpenVLA have shown that large-scale robot datasets, vision-language backbones, and action-token prediction can support general manipulation and transfer across tasks and embodiments [10]–[13]. This capability is relevant to AM because the robot must interpret both the visual manufacturing context and the language instruction while generating manipulation commands within a constrained workspace. 

Despite this potential, transferring a VLA model to an AM workcell is not a straightforward model-deployment problem. The first difficulty is migrating demonstrations and action interfaces across robot platforms. Robot datasets often differ in image resolution, observation structure, sampling rate, episode organization, coordinate frames, state definitions, and gripper conventions. Their action spaces may also represent joint positions, joint velocities, absolute Cartesian poses, or relative end-effector motion. Even when two platforms expose action vectors of the same dimension, the individual elements may have different physical meanings, units, ranges, or normalization rules. RLDS and TFDS provide a common structure for organizing episodic robot data, but they do not by themselves resolve these embodiment-specific differences [14], [15]. As 

a result, transferring an existing VLA pipeline to a platform such as the FAIRINO FR3 requires more than renaming dataset fields. Coordinate transformations, action semantics, gripper commands, and normalization statistics must all be defined consistently before the model can be trained and safely deployed. 

The second difficulty is robustness to changes between the demonstration environment and the deployed AM workcell. Lighting intensity, illumination direction, camera exposure, background clutter, camera viewpoint, and object pose may vary between data collection and execution. Reflective build plates, dark polymer parts, shadows cast by the robot, and changes in printer illumination can further alter the visual appearance of the part and the gripper. These variations are especially relevant when the model is adapted using demonstrations collected under a fixed camera and lighting configuration. Because a VLA policy predicts actions directly from image observations, it may associate the required motion with incidental visual features of the training environment instead of the task geometry. A policy that succeeds under the original lighting condition may therefore become less reliable when the workcell appearance changes, even though the physical task remains the same. 

In this work, we present _ChunkVLA-AM_ , a reproducible OpenVLA-OFT-based deployment pipeline for FR3-based AM post-print retrieval. To make embodiment adaptation explicit, we construct a conversion pipeline that transforms monocular FR3 demonstrations, Cartesian end-effector states, binary gripper commands, language instructions, and episode metadata into OpenVLA-compatible TFDS/RLDS episodes. The pipeline defines the coordinate frames, action semantics, and normalization procedure required by the target FR3 system, while LoRA is used to avoid full-parameter fine-tuning. For robot control, we adopt a horizon- _H_ action-chunk interface and use _H_ = 8 in the reported physical tests, allowing the model to predict short-horizon motion sequences in a single request. The FR3 client then applies action denormalization, workspace clipping, unsafe-action rejection, and chunkwise replanning after execution of the returned actions. This implementation focuses on the system-level adaptation and deployment required to use an action-chunked VLA policy in a fixed AM workcell and to evaluate its behavior under changes in lighting and object pose. 

## II. RELATED WORK 

## _A. Vision-Language-Action Models for Robot Control_ 

Vision-language-action (VLA) models have emerged from the broader trend of connecting language, perception, and embodied decision making. Early generalist and languageconditioned robot systems, including Gato, SayCan, PaLME, and VIMA, showed that multimodal representations can support instruction following, planning, and interactive manipulation across diverse tasks [16]–[19]. More recent VLA policies such as RT-1, RT-2, Open X-Embodiment, and OpenVLA further demonstrate that large-scale robot datasets and vision-language backbones can be used to predict robot actions 

directly from images and natural-language instructions [10]– [13]. These studies provide the main methodological foundation for applying VLA models beyond household or tabletop manipulation. However, their evaluation settings are still largely centered on general manipulation benchmarks, leaving manufacturing-oriented scenarios comparatively underexplored. 

## _B. Robotic Automation in Additive Manufacturing_ 

Additive manufacturing (AM) has been widely studied as a flexible production technology for customized, lightweight, and high-value components [1]–[3]. Robotic systems have also been introduced into AM workflows for material handling, inspection, deposition assistance, post-processing, and largescale or wire-arc manufacturing [20]. Compared with conventional automation, AM workcells pose distinctive perception and decision-making challenges because part geometry, surface appearance, thermal history, defect morphology, and process state can vary significantly across builds. Defects such as warping, delamination, porosity, lack of fusion, and cracking further require robots to reason over visual manufacturing evidence instead of simply replaying fixed trajectories [7]–[9]. These characteristics make AM a natural application domain for VLA models: language can specify task intent, visual input can capture part and process context, and action prediction can support flexible intervention. 

## _C. Challenges of Applying VLA Models to AM_ 

Although VLA models are promising for AM, existing literature suggests two major barriers to practical use. The first is data and adaptation cost. AM tasks are weakly represented in large robot-learning datasets, while effective VLA adaptation requires demonstrations that align visual observations, language instructions, action labels, and episode structure in reusable formats such as TFDS/RLDS [14], [15]. Full finetuning of large VLA models can be expensive and data-hungry, motivating parameter-efficient adaptation methods such as LoRA [21]. The second challenge is achieving temporally coherent motion. Single-step autoregressive prediction can accumulate covariate shift and produce open-loop drift during precise manipulation. Prior work on action chunking and horizon-based visuomotor policies shows that predicting multiple future actions as a structured sequence improves motion consistency [22], [23]. In AM settings, such temporal coherence must be balanced against responsiveness and safety, because robot motions often occur near printed parts, build plates, tools, or process-sensitive regions. Therefore, the VLA– AM research gap is not only whether VLA models can represent AM tasks, but also how they can be adapted and executed with sufficient temporal stability for precise manufacturing intervention. 

III. PRELIMINARIES 

## _A. VLA Policy for AM Robot Intervention_ 

We formulate AM robot intervention as languageconditioned action prediction. At time _t_ , the robot observes 

a RGB image _It ∈_ R<sup>_h×w×_3</sup> and receives a natural-language instruction _l_ . A VLA policy parameterized by _θ_ predicts a robot action from the image–language pair, 


where _at ∈_ R<sup>_da_</sup> denotes the continuous control command after token decoding and denormalization. For an AM demonstration dataset 


where _e_<sup>(</sup> _t_<sup>_i_)</sup> stores episode metadata, the adaptation objective can be written as empirical risk minimization, following standard supervised imitation-style VLA adaptation [10], [13], 


so cross-episode variation in _It_ arises primarily from changes in _St_ (part pose, build-plate state) and _λt_ (workcell lighting). 

For the VLA policy to generalize across AM workcell conditions, it must satisfy approximate illumination invariance, 


where _λ_ 0 is a reference (baseline) illumination and _ϵλ_ is a tolerable action deviation. A small _ϵλ_ across a wide range of Λ indicates that the visual backbone has learned illuminationrobust features. 

Under a fixed camera pose **c** , the appearance of the same workspace also varies with object placement and orientation on the build plate. The perspective projection of the scene can be written as 


## _B. Costly Adaptation and Fine-Tuning_ 

Let _θ_ 0 denote a pretrained VLA model and let _Nθ_ be the number of trainable parameters under full fine-tuning. Direct adaptation updates all model weights, 


which creates a high optimization and storage cost when _Nθ_ is large. The adaptation cost can be abstracted as 

where Π denotes the perspective projection operator. Because the camera pose is fixed, residual viewpoint variation arises from differences in printed-part pose. The policy must therefore handle object-level pose variation without explicit 3D estimation. This motivates the use of square-padded, fixedresolution image inputs and the robustness study in Section V, where we evaluate the adapted policy across seven distinct illumination conditions spanning luminance. 


where _N_ train is the number of trainable parameters and _E_ is the number of training epochs. In AM, this cost is amplified by the limited availability of task-specific demonstrations and by embodiment-dependent action conventions. Parameterefficient adaptation reduces the trainable parameter count by freezing _θ_ 0 and learning a low-dimensional update ∆ _θϕ_ [21], 


Thus, the goal is to minimize task loss on _D_ AM while keeping _N_ train = _|ϕ|_ small. This motivates a data interface that preserves AM observations, instructions, actions, and episode boundaries, together with parameter-efficient fine-tuning while avoiding full-model adaptation. 

_C. Visual Input Conditions: Illumination and Camera Viewpoint_ 

The observed image _It_ depends not only on the scene content but also on physical imaging conditions. Let _St_ denote the geometric and material state of the AM workspace at time _t_ , let _λt ∈_ Λ be the ambient illumination—characterized by mean luminance _µ_ ( _λt_ ) _∈_ [0 _,_ 255] and color temperature _T_ ( _λt_ ) in Kelvin—and let **c** = ( _K,_ [ _R |_ **t** ]) denote the camera intrinsic matrix _K_ and fixed extrinsic pose [ _R |_ **t** ]. The image formation can then be written as 


where _G_ is the image formation function. In our deployment **c** is held constant across all episodes (fixed monocular camera), 

## _D. Action Representation_ 

Each action is represented as a Cartesian end-effector delta and gripper command, 


The first six terms describe translational and rotational increments, and _g_ is a binary gripper state. 


ChunkVLA-AM is a reproducible OpenVLA-OFT-based deployment pipeline. It uses monocular RGB input, synchronized robot poses, parallel action-chunk prediction, Cartesian end-effector control, and robot-side safety filters. The pipeline defines five interfaces: 

- 1) TFDS/RLDS conversion, 

- 2) Action Normalization and Token Targets, 

- 3) LoRA Adaptation, 

- 4) Action Chunk Construction 

- 5) Cloud-Edge Execution and Safety Filtering 

Figure 1 summarizes the pipeline. The remote server performs large language model inference, while the CPUonly robot workstation handles capture, requests, parsing, denormalization, smoothing, clipping, validation, execution, and logging. This split supports hardware where the robot controller and VLA model cannot run on the same machine. 


Fig. 1. Cloud-edge deployment architecture. The local FR3 client sends instruction-conditioned RGB observations to a remote OpenVLA-OFT service, receives an action chunk, and validates commands before execution. 

## _A. TFDS/RLDS Data Conversion_ 

Each demonstration becomes an RLDS-style episode with synchronized observations, actions, language, and metadata [14], [15]. The raw log contains time-stamped endeffector poses, gripper states, controller commands, and camera frames. We use the robot base frame for Cartesian translations. At step _t_ , the translational action is 


where _pt_ = [ _xt, yt, zt_ ] is the end-effector position. Rotation uses a roll-pitch-yaw Euler increment, 


computed from consecutive orientations after conversion to the same Euler convention. The gripper command _gt_ is binary, with _gt_ = 1 for closing or holding and _gt_ = 0 for opening or release. The final 7-D action is 


Images are converted to RGB, square-padded, and resized to 224 _×_ 224 pixels. Images and robot states are synchronized by nearest time stamp; frames outside one control period are dropped. The demonstrations and corresponding action labels are sampled at approximately 25 Hz. Episode boundaries come from the start/stop signal, timeout, or task-completion marker. The schema stores image observations, Cartesian state and gripper metadata, normalized 7-D delta actions, repeated language instructions, and trial metadata including episode id, step index, timestamps, and terminal flag. 

## _B. Action Normalization and Token Targets_ 

Before tokenization, each continuous action dimension is clipped to a symmetric range and normalized to [ _−_ 1 _,_ 1]: 


For the post-print retrieval configuration, the default clipping values are _cx_ = _cy_ = _cz_ = 5 mm per action and _cϕ_ = _cθ_ = _cψ_ = 0 _._ 05 rad per action. The gripper channel is not normalized as a continuous value; it is binarized by the open/close state and serialized as a discrete command token. These thresholds are deployment parameters and should not be interpreted as safety guarantees: they limit the largest command passed to the controller, but physical safety still depends on validation, contact monitoring, and emergency stop handling. 

## _C. LoRA Adaptation_ 

The adaptation uses only monocular RGB images and language instructions, avoiding multi-view cameras, depth sensing, tactile sensing, or other additional modalities. We adapt the OpenVLA-OFT model with LoRA, which trains lowrank updates while freezing the pretrained backbone [21]. For FR3 adaptation, we use a LoRA rank of 32 with zero dropout, a learning rate of 5 _×_ 10<sup>_−_4</sup> , a batch size of 8, and gradient accumulation over 4 steps, giving an effective batch size of 32. The model is trained for approximately 30 epochs. 

For single-step imitation, the supervised objective is 


For chunked imitation, adjacent expert actions form a shorthorizon target, 


Terminal chunks are truncated to the remaining valid actions and padded positions are masked from the loss. 

## _D. Action Chunk Construction_ 

For a horizon _H_ , the training target concatenates _H_ future normalized 7-D actions into one longer target sequence, 


At each physical inference cycle, the RGB image is synchronized with the current robot pose, the remote server predicts an eight-step action chunk, and the robot executes the returned actions before the next image is acquired. The next inference request is therefore issued after completion of the current chunk in the physical experiments reported here. Parallel hostside inference was tested separately on the computer but was not used for the reported physical robot trials. 

## _E. Cloud-Edge Execution and Safety Filtering_ 

The 7B OpenVLA-OFT model runs on a remote inference server [13], while the robotic client remains CPU-only. On the RTX 6000 Ada server used in our experiments, the logged model-side inference time was approximately 0.06– 0.08 s per request. This measurement excludes image capture, network transmission, and physical robot execution time. At each replan step, the client sends ( _It, l, H_ ) through FastAPI, receives _Ct_ , and decodes it into candidate actions. A candidate action is rejected if any of the following checks fail: 


Here _B_ is the allowed workspace, _z_ min is the minimum build-plate clearance, _d_ max = 5 mm, and _r_ max = 0 _._ 05 rad for the current post-print retrieval configuration. The gripper command must be a valid binary state. The client also rejects NaN actions, network-timeout responses, stale chunks, and commands arriving after an emergency-stop flag. If a command is rejected, the remaining chunk is discarded and the client either requests a new chunk or halts the episode, depending on the experiment mode. 

## V. EXPERIMENTS 

## _A. Experimental Scope and Connection to the Method_ 

The experiments evaluate both trajectory-level prediction and physical closed-loop execution of the proposed ChunkVLA-AM pipeline. Following the formulation in Section III, the policy receives a monocular image _It_ and a language instruction _l_ , then predicts a short-horizon action chunk _At_ = [ _at, . . . , at_ + _H−_ 1]. The logged-trajectory analysis evaluates whether these chunks preserve the structure of expert AM handling trajectories after data conversion, action normalization, LoRA adaptation, and chunk construction, while a separate 42-trial physical evaluation measures end-to-end A- to-B transfer success. The trajectory plots therefore describe open-loop prediction consistency, whereas the robot trials provide a direct closed-loop deployment check under the same FR3 workcell configuration. 

## _B. Post-Print Retrieval Task_ 

The evaluation includes two color-conditioned manipulation tasks: “catch the blue block” and “catch the red block.” In each task, the FR3 approaches the specified block at point A, closes the gripper, transfers the target to point B, and releases it. The two tasks use the same manipulation sequence but require the policy to associate the instruction with the corresponding visual target. These controlled A-to-B blocktransfer tasks serve as reproducible proxies for post-print part retrieval and transfer while evaluating language-conditioned Cartesian trajectory prediction and physical execution. 

## _C. Evaluation Metrics_ 

For each logged frame, the policy receives the monocular observation and instruction and predicts an _H_ -step action chunk. The predicted future positions are compared with the expert end-effector trajectory along the _x_ , _y_ , and _z_ axes. Because these plots are generated from logged states and not from closed-loop rollouts, the metrics describe open-loop trajectory consistency, not final task success. 

The primary trajectory metric is axis-wise mean absolute error (MAE), 


_D. Comparison of Adaptation Methods and Prediction Horizons_ 

To evaluate embodiment-specific adaptation and compare the evaluated policy configurations, we tested four models on the same FAIRINO FR3, camera setup, workspace, and test data. The standard single-step OpenVLA (Zero-Shot) and the 8-step action-chunked OpenVLA-OFT (Zero-Shot) received no FR3-specific training. The single-step adapted model, referred to as Bridging the Pretrain-to-Real Gap [24], and ChunkVLA-AM (Ours) were both adapted using the same FR3 demonstration dataset. ChunkVLA-AM uses 8- step action chunks. Because adaptation and prediction horizon differ across configurations, this comparison evaluates the complete configurations without isolating chunk length as a single controlled variable. 

We use Mean Absolute Error (MAE) across the X, Y, and Z axes as the primary evaluation metric to assess spatial tracking accuracy against the ground-truth Cartesian trajectory. The performance comparison is illustrated in Figure 2, where a logarithmic scale is applied to the y-axis to accommodate the multi-order magnitude disparities. 

The empirical data show that both zero-shot models are unsuitable for the FR3 additive manufacturing environment. OpenVLA (Zero-Shot) and OpenVLA-OFT (Zero-Shot) produce extreme spatial deviations, with MAE values ranging from 179.60 mm to 650.12 mm. This magnitude of error indicates that pre-trained visual backbones cannot directly transfer to the constrained workspace and specific kinematics of the FR3 robot without targeted training. The failure of the OpenVLA-OFT (Zero-Shot) model confirms that temporal 


Fig. 2. Trajectory tracking comparison across adaptation methods. The y- axis uses a logarithmic scale to highlight the significant precision gains. ChunkVLA-AM achieves sub-millimeter lateral accuracy, outperforming both zero-shot models and single-step fine-tuned baselines. 

action chunking alone cannot compensate for the lack of spatial semantics. 

The single-step adaptation model [24] significantly reduces the tracking error. However, it still yields an average spatial error of 9.50 mm across the three axes, with a pronounced deviation of 16.90 mm on the X-axis. In physical AM workcells, a 16.90 mm lateral offset easily causes collisions with the build plate or printed parts. This localized drift exposes the limitation of single-step autoregressive decoding, where slight execution deviations accumulate over time and lead to terminal open-loop drift. 

In contrast, ChunkVLA-AM achieves an overall average MAE of 1.74 mm, with lateral errors of 0.37 mm on the X-axis and 0.97 mm on the Y-axis and a Z-axis error of 3.87 mm. The adapted chunked configuration therefore exhibits substantially lower trajectory error than the evaluated single-step adapted baseline. Because the compared configurations differ in both adaptation and prediction horizon, these results support the combined FR3-adaptation and chunked-deployment configuration but do not by themselves attribute the improvement solely to action chunking. 

## _E. Physical Closed-Loop Robot Validation_ 

We additionally evaluated the complete camera–server– robot loop in 42 physical A-to-B transfer trials using eightstep action chunks. The trials were evenly divided between the red and blue targets, with 21 trials per color. Across all 42 trials, 39 transfers were completed successfully, corresponding to an overall success rate of 92.9%. The three failures occurred during terminal placement at point B: the placement height was not sufficiently controlled, causing the released object to fall and topple. These failures were retained in the reported success rate. The physical trials use the same FR3 workcell and sequential observation–inference–execution loop described in Section IV. 

_F. Influence of Physical Illumination and Color Temperature_ 

We also evaluated ten separately recorded but task-matched logged test trajectories at 181 target luminance levels from 30 to 210; the ten trials are similar A-to-B sequences collected independently, not repeated copies of a single trajectory. As shown in Fig. 3, the mean spatial error reached its minimum of 5.459 mm at luminance 95 and remained low within the highlighted 85–125 range. The error increased to 7.165 mm and 6.598 mm at luminance 30 and 210, respectively. The axiswise curves further show that the _z_ -axis was the dominant source of error, whereas the _x_ - and _y_ -axis errors remained smaller. 

The experimental setup used the same FR3 workspace under controlled physical lighting changes. Illumination was varied by adjusting the room light intensity and swapping between neutral white, warm (3000 K), and cold (6500 K) light sources. All captures were taken with a fixed monocular RGB camera at the same pose; no digital post-processing or gamma correction was applied. Figure 4 shows six representative captures from the seven tested illumination conditions, spanning variations in luminance and color temperature. 

The policy was evaluated directly on environmental captures under Low Light, Baseline, and Over-Exposed conditions without mathematically simulating brightness. As shown in Table I, the system maintains similar spatial tracking error across mild lighting shifts (luminance spanning 65.2 to 165.1), with the _z_ -axis MAE remaining approximately 3.8–4.0 mm. 

However, extreme over-exposure (luminance 189.1) degrades lateral tracking, with the _y_ -axis MAE increasing to 2.30 mm. The warm and cold color-temperature conditions remain close to the baseline, while extreme glare produces the largest degradation. This result motivates additional lighting augmentation for highly reflective AM workspaces. 

TABLE I 

INFLUENCE OF ENVIRONMENTAL ILLUMINATION AND COLOR TEMPERATURE ON CHUNKED TRAJECTORY PREDICTION. BRIGHTNESS IS MEASURED IN MEAN LUMINANCE ON A 0–255 SCALE. ERRORS ARE REPORTED IN AXIS-WISE MEAN ABSOLUTE ERROR (MAE) ALONGSIDE THE 3D EUCLIDEAN ERROR ( _L_ 2). 

|**Condition**|**Luminance**<br>**(0–255)**|_x_|**MAE**<br>_y_|**(mm)**<br>_z_|**3D** _L_2|
|---|---|---|---|---|---|
|Baseline (Neutral)|109|0.37|**0.97**|3.87|4.01|
|LowLight Extreme|30|0.45|1.28|4.04|4.26|
|LowLight Mild|65|**0.26**|1.03|4.03|4.17|
|OverLight Mild|165|0.37|1.00|3.86|4.00|
|OverLight Extreme|190|0.59|2.30|4.65|5.22|
|ColorTemp Warm|116|0.41|0.99|3.93|4.07|
|ColorTemp Cold|108|0.50|**0.97**|**3.76**|**3.92**|


We further analyzed a dense luminance sweep comprising 10 trials, each evaluated at 181 target luminance levels from 30 to 210. The realized image luminance closely followed the requested value: the mean actual-minus-target difference was 0.0037 and the maximum absolute difference was 0.0742 on the 0–255 scale. Because the sweep outputs contain neither a color-temperature field nor a task-success label, this analysis is used specifically to quantify trajectory-error sensitivity to 


Fig. 3. Trajectory prediction errors across ten luminance-sweep trials. The solid curve and surrounding band show the across-trial mean spatial error and _±_ 1 standard deviation, respectively. The remaining curves show the axis-wise MAEs. The highlighted range from 85 to 125 indicates a low-error region centered around the minimum error observed at luminance 95. 


(a) Baseline (b) LowLight (c) OverLight Mild (d) OverLight Extreme (e) ColorTemp Warm (f) ColorTemp Cold Fig. 4. Representative FR3 workspace captures under six illumination conditions used in the lighting robustness study. Panel (a) is the neutral baseline; the remaining panels span low light, over-exposure, and warm/cold color-temperature variants. Luminance values are mean pixel intensity on a 0–255 scale. 

luminance and does not replace the warm/cold comparison in Table I. 

Figure 3 visualizes the low-error region around the aggregate minimum and the error increases near the darkest and brightest ends of the sweep. 

The dense sweep supports the 85–125 interval as a narrower low-error band without implying a single optimal illumination. Its trial-level mean spatial error was 5.499 mm, whereas the 30–84 and 126–210 regions increased the error by 0.373 mm (6.8%) and 0.146 mm (2.6%), respectively; descriptive bootstrap 95% confidence intervals for these paired regional differences were [0.225, 0.529] mm and [0.064, 0.233] mm. 

TABLE II 

TRIAL-LEVEL SUMMARY OF THE DENSE LUMINANCE SWEEP. THE REPORTED SWEEP ERROR IS THE MILLIMETER-VALUED SPATIAL-ERROR METRIC PROVIDED IN THE ANALYSIS OUTPUTS AND IS KEPT DISTINCT FROM THE 3D _L_ 2 VALUES IN TABLE I. REGION MEANS ARE FIRST COMPUTED WITHIN EACH OF THE 10 TRIALS. 

|**Luminance region**|**Sweep error**|**Axis **|**MAE **|**(mm)**|
|---|---|---|---|---|
|**(0–255)**|**(mm)**|_x_|_y_|_z_|
|30–84|5.872|0.834|1.209|4.985|
|85–125|**5.499**|**0.676**|**1.198**|**4.639**|
|126–210|5.644|0.720|1.331|4.688|


Within 85–125, the aggregate mean curve varied by only 1.2% of the global minimum. Although the across-trial curve reached its lowest value of 5.459 mm at luminance 95 and remained within 5% of this minimum from 58 to 200, the error-minimizing luminance of individual trials ranged from 36 to 198 (median 95). Thus, luminance 95 should not be interpreted as a universal optimum. 

Degradation became clearer at the sweep endpoints: the aggregate mean error was 7.165 mm at luminance 30 and 6.598 mm at luminance 210, corresponding to increases of 31.2% and 20.9% over the aggregate minimum. The axis-wise results in Table II show that the _z_ -axis remained the dominant error component throughout the sweep. Relative to the 85– 125 band, low-light degradation was primarily associated with larger _z_ - and _x_ -axis errors, whereas the largest highluminance increase occurred on the _y_ -axis. This continuoussweep evidence is consistent with the discrete-condition results: intermediate illumination produces lower error, while the darkest and brightest regimes are more likely to disturb visual grounding. 

Overall, illumination changes affect height and lateral localization differently in the fixed AM workcell, highlighting 

the importance of lighting robustness during deployment. 

## VI. CONCLUSION AND DISCUSSION 

This paper presented ChunkVLA-AM as a reproducible OpenVLA-OFT-based system pipeline for FR3-based postprint retrieval in additive manufacturing. The paper specifies the data conversion interface, 7-D Cartesian action representation, horizon-based chunk construction, LoRA adaptation setup, cloud-edge request loop, and robot-side action filtering needed to reproduce the system. The logged-trajectory analyses show low Cartesian prediction error for the FR3adapted eight-step configuration, while the physical evaluation completed 39 of 42 A-to-B transfer trials successfully (92.9%). The three failures occurred during terminal placement when the released object toppled because of insufficient placementheight control. The lighting experiments further show that prediction error remains lowest over an intermediate luminance range and increases toward the darkest and brightest conditions. These results support the feasibility of the proposed deployment pipeline in the evaluated fixed FR3 workcell. Future work will add broader object and task generalization, controlled chunk-length ablations, contact-force monitoring, and richer AM-specific tasks such as warped-part inspection and failed-print removal. 

## ACKNOWLEDGMENT 

The authors gratefully acknowledge funding from the National Science Foundation (NSF) CREST Center for Multidisciplinary Research Excellence in Cyber-Physical Infrastructure Systems (MECIS) under Award No. 2112650. Additional support was provided by the NSF Expand AI PARTNER: ARISE: AI Research and Innovation for Smart Environments under NSF Award No. 2434916, as well as NSF ACCESS: AI-Enhanced Cross-Scale Sensing and Intelligent Quality Assessment for Scalable Additive Manufacturing (NSF Award No. ELE250047). The authors also acknowledge the University Transportation Center for Railway Safety (UTCRS) for providing the datasets used in this work and funding support under the USDOT UTC Program Grant No. 69A3552348340. 

## REFERENCES 

- [1] I. Gibson, D. Rosen, B. Stucker, and M. Khorasani, _Additive Manufacturing Technologies_ , 3rd ed. Cham, Switzerland: Springer, 2021. 

- [2] T. D. Ngo, A. Kashani, G. Imbalzano, K. T. Q. Nguyen, and D. Hui, “Additive manufacturing (3D printing): A review of materials, methods, applications and challenges,” _Composites Part B: Engineering_ , vol. 143, pp. 172–196, 2018. 

- [3] T. DebRoy _et al._ , “Additive manufacturing of metallic components – process, structure and properties,” _Progress in Materials Science_ , vol. 92, pp. 112–224, 2018. 

- [4] B. Stephens, P. Azimi, Z. El Orch, and T. Ramos, “Ultrafine particle emissions from desktop 3D printers,” _Atmospheric Environment_ , vol. 79, pp. 334–339, 2013. 

- [5] P. Azimi, D. Zhao, C. Pouzet, N. E. Crain, and B. Stephens, “Emissions of ultrafine particles and volatile organic compounds from commercially available desktop three-dimensional printers with multiple filaments,” _Environmental Science & Technology_ , vol. 50, no. 3, pp. 1260–1268, 2016. 

   - [7] Y. Zhang and Y. K. Chou, “Three-dimensional finite element analysis simulations of the fused deposition modelling process,” _Proceedings of the Institution of Mechanical Engineers, Part B: Journal of Engineering Manufacture_ , vol. 220, no. 10, pp. 1663–1671, 2006. 

   - [8] Z. Jin, Z. Zhang, and G. X. Gu, “Automated real-time detection and prediction of interlayer imperfections in additive manufacturing processes using artificial intelligence,” _Advanced Intelligent Systems_ , vol. 2, no. 1, p. 1900130, 2020. 

   - [9] B. Zhang, Y. Li, and Q. Bai, “Defect formation mechanisms in selective laser melting: A review,” _Chinese Journal of Mechanical Engineering_ , vol. 30, pp. 515–527, 2017. 

   - [10] A. Brohan _et al._ , “RT-1: Robotics transformer for real-world control at scale,” in _Proceedings of Robotics: Science and Systems_ , Daegu, Republic of Korea, Jul. 2023. [Online]. Available: https://roboticsproceedings.org/rss19/p025.html 

   - [11] B. Zitkovich _et al._ , “RT-2: Vision-language-action models transfer web knowledge to robotic control,” in _Proceedings of the 7th Conference on Robot Learning_ , ser. Proceedings of Machine Learning Research, vol. 229. PMLR, 2023, pp. 2165–2183. [Online]. Available: https://proceedings.mlr.press/v229/zitkovich23a.html 

   - [12] Open X-Embodiment Collaboration _et al._ , “Open X-Embodiment: Robotic learning datasets and RT-X models,” in _IEEE International Conference on Robotics and Automation (ICRA)_ , 2024, pp. 6892–6903. 

   - [13] M. J. Kim _et al._ , “OpenVLA: An open-source vision-languageaction model,” in _Proceedings of the 8th Conference on Robot Learning_ , ser. Proceedings of Machine Learning Research, vol. 270. PMLR, 2025, pp. 2679–2713. [Online]. Available: https://proceedings.mlr.press/v270/kim25c.html 

   - [14] S. Ramos _et al._ , “RLDS: An ecosystem to generate, share and use datasets in reinforcement learning,” _arXiv preprint arXiv:2111.02767_ , 2021. [Online]. Available: https://arxiv.org/abs/2111.02767 

   - [15] “TensorFlow Datasets: A collection of ready-to-use datasets,” accessed: Jun. 23, 2026. [Online]. Available: https://www.tensorflow.org/datasets 

   - [16] S. Reed _et al._ , “A generalist agent,” _Transactions on Machine Learning Research_ , 2022. [Online]. Available: https://openreview.net/forum?id=1ikK0kHjvj 

   - [17] B. Ichter _et al._ , “Do as I can, not as I say: Grounding language in robotic affordances,” in _Proceedings of the 6th Conference on Robot Learning_ , ser. Proceedings of Machine Learning Research, vol. 205. PMLR, 2023, pp. 287–318. [Online]. Available: https://proceedings.mlr.press/v205/ichter23a.html 

   - [18] D. Driess _et al._ , “PaLM-E: An embodied multimodal language model,” in _Proceedings of the 40th International Conference on Machine Learning_ , ser. Proceedings of Machine Learning Research, vol. 202. PMLR, 2023, pp. 8469–8488. [Online]. Available: https://proceedings.mlr.press/v202/driess23a.html 

   - [19] Y. Jiang _et al._ , “VIMA: Robot manipulation with multimodal prompts,” in _Proceedings of the 40th International Conference on Machine Learning_ , ser. Proceedings of Machine Learning Research, vol. 202. PMLR, 2023, pp. 14 975–15 022. [Online]. Available: https://proceedings.mlr.press/v202/jiang23b.html 

   - [20] D. Ding, Z. Pan, D. Cuiuri, and H. Li, “Wire-feed additive manufacturing of metal components: Technologies, developments and future interests,” _The International Journal of Advanced Manufacturing Technology_ , vol. 81, pp. 465–481, 2015. 

   - [21] E. J. Hu _et al._ , “LoRA: Low-rank adaptation of large language models,” in _International Conference on Learning Representations_ , 2022. [Online]. Available: https://openreview.net/forum?id=nZeVKeeFYf9 

   - [22] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” in _Proceedings of Robotics: Science and Systems_ , Daegu, Republic of Korea, Jul. 2023. [Online]. Available: https://roboticsproceedings.org/rss19/p016.html 

   - [23] C. Chi _et al._ , “Diffusion policy: Visuomotor policy learning via action diffusion,” in _Proceedings of Robotics: Science and Systems_ , Daegu, Republic of Korea, Jul. 2023. [Online]. Available: https://roboticsproceedings.org/rss19/p026.html 

   - [24] Z. Liu _et al._ , “Bridging the pretrain-to-real gap: Alignment challenges in deploying generalist VLA models for additive manufacturing,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) Workshops_ , Jun. 2026, pp. 1048–1056. 

- [6] R. Chen _et al._ , “Exposure, assessment and health hazards of particulate matter in metal additive manufacturing: A review,” _Chemosphere_ , vol. 259, p. 127452, 2020. 

