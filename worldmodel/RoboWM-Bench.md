---
title: "RoboWM-Bench: A Benchmark for Evaluating World Models in Robotic Manipulation"
date: "2026-04-21"
authors: "Feng Jiang; Yang Chen; Kyle Xu; Yuchen Liu; Haifeng Wang; Zhenhao Shen"
url: https://arxiv.org/abs/2604.19092
pdf: https://arxiv.org/pdf/2604.19092
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.19092)** / [論文ページ](https://arxiv.org/abs/2604.19092)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **RoboWM-Bench: A Benchmark for Evaluating World Models in Robotic Manipulation** 

**Feng Jiang**<sup>1</sup><sup>_∗_</sup> **Yang Chen**<sup>1</sup><sup>_∗_</sup> **Kyle Xu**<sup>1</sup><sup>_∗_</sup> **Yuchen Liu**<sup>1</sup> **Haifeng Wang**<sup>1</sup> **Zhenhao Shen**<sup>1</sup> **Jasper Lu**<sup>1</sup> **Shengze Huang**<sup>2</sup> **Yuanfei Wang**<sup>1</sup> **Chen Xie**<sup>3</sup> **Ruihai Wu**<sup>1</sup><sup>_,†_</sup> 1Peking University 2Tsinghua University 3Lightwheel `wuruihai@pku.edu.cn` 

## **Abstract** 

Recent advances in large-scale video world models have enabled increasingly realistic future prediction, raising the prospect of using generated videos as scalable supervision for robot learning. However, for embodied manipulation, perceptual realism alone is not sufficient: generated interactions must also be physically consistent and executable by robotic agents. Existing benchmarks provide valuable assessments of visual quality and physical plausibility, but they do not systematically evaluate whether predicted behaviors can be translated into executable actions that complete manipulation tasks. We introduce **RoboWM-Bench** , a manipulation-centric benchmark for embodiment-grounded evaluation of video world models. RoboWMBench converts generated human-hand and robotic manipulation videos into embodied action sequences and validates them through execution in physically grounded simulation environments. Built on real-to-sim scene reconstruction and diverse manipulation tasks, RoboWM-Bench enables standardized, reproducible, and scalable evaluation of physical executability. Using RoboWM-Bench, we evaluate state-ofthe-art video world models and observe that visual plausibility and embodied executability are not always aligned. Our analysis highlights several recurring factors that affect execution performance, including spatial reasoning, contact prediction, and non-physical geometric distortions, particularly in complex and long-horizon interactions. These findings provide a more fine-grained view of current model capabilities and underscore the value of embodiment-aware evaluation for guiding physically grounded world modeling in robotic manipulation. The project page is available at `https://robowm-bench.github.io/RoboWM-Bench/` . 

## **1 Introduction** 

Recent advances in large-scale video generation have produced increasingly realistic video world models capable of synthesizing temporally coherent and visually plausible futures [8, 16, 17, 49]. While these models create new opportunities for robot learning from predicted videos, embodied manipulation requires more than visual fidelity: generated interactions must respect physical constraints and support executable control. Accordingly, recent work has explored robotics-oriented video world models that better capture robot–environment interactions and embodiment-aware dynamics [1, 2, 9, 12, 21, 46]. As predicted manipulation videos become a promising source of scalable supervision for robot learning [9, 23, 45], reliable evaluation is essential for determining whether they are physically grounded and useful for downstream control. 

Existing benchmarks for video world models have provided valuable tools for evaluating visual fidelity, semantic consistency, and temporal coherence [15, 22, 24, 32, 33, 59]. More recent efforts further extend evaluation toward physical plausibility, offering useful diagnostics of whether generated videos 

> _∗_ Equal contribution 

> _†_ Corresponding author 

Preprint. 


Figure 1: **Overview of RoboWM-Bench.** RoboWM-Bench evaluates video world models through embodiment-grounded execution. (a) Predicted human-hand and robotic manipulation videos are converted into executable actions via retargeting or inverse dynamics model (IDM) and validated in real-to-sim simulation environments. (b) The benchmark compares execution performance across state-of-the-art video world models for human-hand and robotic manipulation. (c) RoboWM-Bench covers diverse tasks spanning different object properties, interaction dynamics, temporal horizons, and coordination requirements. (d) Real-to-sim fidelity is evaluated by replaying identical real-world trajectories in reconstructed simulations and comparing the resulting task outcomes. 

preserve coherent dynamics [43, 60, 61]. For robotic manipulation, however, physical plausibility raises a more operational question: can the behaviors depicted in predicted videos be translated into executable actions that accomplish the intended task? While recent work [14] takes an important step toward embodiment-grounded evaluation through real-world robot validation, broad and reproducible assessment remains challenging due to the cost and limited scalability of physical experiments. 

To address this gap, we introduce **RoboWM-Bench** , a manipulation-centric benchmark for evaluating video world models through execution-based validation in high-fidelity simulation environments. RoboWM-Bench covers both human-hand and robotic manipulation scenarios, reflecting complementary settings for learning from human demonstrations and robot-centric control. As illustrated in Figure 1, for each task, a video world model is conditioned on an initial observation and task description to generate a future manipulation video. The predicted behaviors are then converted into executable action sequences through inverse dynamics modeling [5, 23] for robotic videos, or pose tracking and retargeting [27, 28, 39] for human demonstrations. These actions are executed in high-fidelity real-to-simulation environments, enabling standardized and reproducible validation of physical executability. RoboWM-Bench combines step-level executability checks with final task-level success rates, supporting both fine-grained diagnosis and holistic assessment. Spanning diverse object dynamics, task horizons, and single-arm and bimanual interactions, RoboWM-Bench provides an accessible and scalable protocol for comparing video world models under embodiment constraints. 

We conduct extensive experiments with RoboWM-Bench to evaluate state-of-the-art video world models under embodied execution. The results suggest that visual realism does not always translate into physical executability, with execution success tending to decrease as task complexity increases, especially in long-horizon interactions and deformable-object manipulation. Qualitative analysis identifies recurring sources of execution difficulty, including inaccurate contact prediction, unrealistic object deformation, and geometric distortions that can lead to dynamically infeasible actions. Although fine-tuning on manipulation-specific data improves executability, generating physically consistent interactions remains challenging. We further validate the evaluation pipeline through action-extraction accuracy and real-to-sim execution consistency analyses, supporting the reliability of these findings. Together, these results demonstrate the value of RoboWM-Bench as a diagnostic 

2 

protocol for embodiment-grounded evaluation and highlight opportunities for advancing physically grounded world models for robotic manipulation. 

## **2 Related Work** 

### **2.1 World Models for Robotics** 

Recent advances in large-scale video generation have renewed interest in world models as predictive models of physical dynamics [1, 2, 19, 20, 47, 50, 53]. Models such as Sora [8], Veo [17], Wan [49], and Seedance [16] demonstrate strong visual realism and temporal coherence, suggesting that largescale video training can capture rich spatiotemporal priors. For robotic manipulation, however, the key question is not only whether generated videos look plausible, but whether they preserve the physical and interaction dynamics needed for executable control. This has motivated robotics-oriented world models for video-based robot planning [3, 9], scalable data generation for robot learning [23, 46], embodied interaction prediction and interactive real-world simulation [12, 21, 57], and robot imagination with compositional video planning [62]. As video world models are increasingly used as simulators, planners, or data engines for embodied AI, their evaluation must move beyond perceptual quality to assess physical consistency and control feasibility. 

### **2.2 Learning Robotic Actions from Video** 

Learning robotic control from video has become increasingly important as large-scale human and generated videos provide scalable supervision for robot learning [6, 18, 36, 41, 42, 44, 55]. Prior work has explored several ways to bridge videos and actions. Representation-learning methods such as R3M [37] and VIP [35] pretrain visual encoders on diverse videos to improve downstream policy learning. Latent-action and domain-adaptation methods infer action-relevant structure without dense robot action annotations [40, 58], while inverse-dynamics approaches recover executable actions from observed or generated videos [13, 23, 48]. Human-to-robot transfer methods further retarget in-the-wild human videos to robot policies, as in Phantom [28] and Masquerade [27]. Recent VLA and world-model-based approaches also use videos as training or planning signals [7, 23, 25, 34, 45]. These advances make video-to-action interfaces increasingly practical; in this work, we use them not as a policy-learning objective, but as evaluation tools for testing whether generated manipulation videos can support successful embodied execution. 

### **2.3 Evaluation and Benchmarks of World Models** 

Existing benchmarks for video world models primarily assess perceptual realism and generative quality [15, 32]. Comprehensive suites such as VBench [22], EvalCrafter [33], and T2VEval [24] evaluate visual fidelity, temporal consistency, text–video alignment, and motion coherence. More recent physical-AI-oriented benchmarks [29, 43, 59], including PAI-Bench [61] and VBench-2.0 [60], further extend evaluation toward physical reasoning, intrinsic faithfulness, and embodied-worldmodel capabilities. These benchmarks provide valuable and reproducible diagnostics, while leaving action-level task completion under embodied constraints less directly measured. 

Several robotics-oriented studies have begun to incorporate execution-based validation. For example, LVP [9] evaluates video-conditioned planning on real-world manipulation tasks, and Wow-wo-val [14] introduces embodied evaluation protocols inspired by Turing-test-style assessment. These works represent important steps toward physically grounded evaluation; however, real-robot evaluation typically requires dedicated hardware setups, which can limit scalability for broad model comparisons. Complementary to these efforts, RoboWM-Bench provides a manipulation-centric benchmark with standardized task suites and a unified execution-based protocol across simulation-native and realto-sim reconstructed scenarios. This enables scalable assessment of physical executability and action-level consistency in predicted manipulation videos. 

## **3 RoboWM-Bench** 

### **3.1 Benchmark Overview** 

We introduce RoboWM-Bench, a benchmark for evaluating video world models through embodimentgrounded validation, as illustrated in Figure 2. RoboWM-Bench treats physical executability as a measurable criterion by testing whether behaviors inferred from generated videos can complete manipulation tasks when executed. First, RoboWM-Bench provides standardized simulation environments for reproducible evaluation, covering both simulation-native scenarios and real-to-sim 

3 


Figure 2: **Pipeline of RoboWM-Bench.** Given an initial scene observation, the corresponding real-world scene is reconstructed in simulation through a real-to-sim pipeline, enabling consistent and reproducible evaluation. Predicted videos are then converted into executable robot actions through two pathways: human-centric retargeting, which estimates 3D hand poses and retargets them to robot end-effector actions, and robot-centric inverse dynamics, which predicts joint-space actions via an inverse dynamics model (IDM). The resulting actions are executed in simulation and evaluated using step-level checkers and final task success rates to measure embodied executability. 

reconstructions of real-world scenes (Section 3.2). Given an initial scene observation and a task description, a video world model predicts a future manipulation video in either a human-hand or robotic setting. The benchmark then provides video-to-action interfaces that convert the generated videos into action sequences, which are executed in the corresponding simulation environments (Section 3.3). Finally, RoboWM-Bench defines a diverse manipulation task suite spanning different object properties, interaction regimes, and temporal horizons (Section 3.4), and evaluates executability through step-level verification and final task-level success (Section 3.5). 

### **3.2 High-Fidelity Real-to-Sim Framework** 

To support accessible, reproducible, and scalable evaluation, RoboWM-Bench conducts embodimentgrounded validation in open-source simulation environments. It covers both simulation-native scenarios and real-to-sim reconstructions of real-world scenes, enabling predicted interactions to be evaluated under controlled physical dynamics while reducing dependence on specific physical setups. 

To support high-fidelity execution, RoboWM-Bench builds on the LeHome simulation engine [30], which supports household manipulation scenarios involving rigid, articulated, and deformable objects. We design simulation-native scenarios using LeHome engine, and reconstruct real-world scenes with a modular real-to-sim pipeline covering scene reconstruction, object modeling, and pose calibration. Inspired by recent work [52], background scenes are reconstructed using 4D Gaussian representations to preserve visual realism and spatial consistency. For interactive objects, rigid geometries are obtained through 3D segmentation and reconstruction [11], while articulated and deformable object pairs are constructed following [30]. Object poses are estimated using pose estimation models [26, 51], and camera poses are calibrated with FEEPE [54], averaging results across multiple runs for stability. We further validate the fidelity of the reconstructed environments in Section 4.4. This modular design preserves the physical structure and spatial configuration of real scenes and supports new evaluation scenarios through either simulation-native assets or reconstructed real-world scenes. 

### **3.3 Embodied Video-to-Action Execution** 

To evaluate generated videos through execution, RoboWM-Bench converts predicted manipulation videos into executable action sequences. The benchmark supports both human-hand and robotic videos, covering complementary evaluation settings: human-hand videos reflect interaction patterns that current world models often generate more reliably, while robotic videos are more directly aligned with downstream robot policy learning and control. We therefore use separate video-to-action pathways for the two settings. 

4 

### **3.3.1 Human-Centric Retargeting** 

Inspired by prior work [27, 28], we estimate human hand poses from videos and retarget them to robot end-effector actions. We reconstruct 3D hand poses using HaMeR [39] and use the recovered keypoints to derive three control components: end-effector position, orientation, and gripper opening. 

The gripper target position is defined as the midpoint between the thumb and index fingertips. For orientation, instead of relying on global finger configurations as in prior work [28], we use contactrelevant geometry: we fit a plane through the thumb and index finger keypoints, project the two fingertips onto this plane, and define the _x_ -axis as the line connecting the projections, with the _z_ -axis given by the plane normal. This yields more stable end-effector poses while preserving local human–object interaction geometry. For gripper opening, we use the minimum distance between the thumb tip and all other fingertips rather than the thumb–index distance, accounting for cases where the index fingertip is not the primary contact point. We then apply trajectory smoothing and temporal denoising to stabilize the retargeted motion signals [27, 28]. 

### **3.3.2 Robot-Centric Execution** 

For robotic manipulation videos, we recover action sequences using an inverse dynamics model (IDM), following established video-to-action formulations in prior work [5, 23]. We adopt the IDM architecture from [23], which takes two consecutive image frames as input and predicts the intermediate joint-space action chunk. We train the IDM with a two-stage strategy: large-scale simulation data provides action-labeled supervision for motion pretraining, while a small set of real-world trajectories is used for visual adaptation. 

Specifically, we first collect simulation trajectories with a Franka arm in a physics simulator, recording paired RGB observations and joint-space actions. Compared with real-world collection, simulation enables action-labeled trajectories to be generated more efficiently and at higher temporal resolution, providing dense and smooth supervision for inverse-dynamics learning. To keep simulation pretraining scalable and focused on robot motion, we apply background masking, inspired by [46], retaining only the robot arm in simulation videos. We then finetune the IDM on real-world trajectories collected with a physical Franka arm, without background masking. This design leverages scalable simulation supervision while adapting to real observations, enabling reliable action extraction from generated robotic videos for embodiment-grounded evaluation. 

### **3.4 Manipulation Task Suite with Diverse Complexity** 

RoboWM-Bench includes a diverse suite of manipulation tasks designed to evaluate the embodied reasoning and physical consistency of video world models across varying levels of complexity. The tasks span different object properties, interaction dynamics, temporal horizons, and coordination requirements, enabling systematic assessment beyond short-horizon rigid-object manipulation. 

The task suite covers several representative interaction regimes. Basic rigid-object tasks, such as object pickup and trash disposal, primarily assess contact precision and spatial reasoning. Articulatedobject tasks, including drawer opening and faucet rotation, require models to capture kinematic constraints and structured motion. Deformable-object tasks, such as towel folding, further evaluate whether models can generate physically plausible non-rigid interactions. 

RoboWM-Bench also includes more complex manipulation settings that require longer-term reasoning or bimanual coordination. Long-horizon compositional tasks, such as assembling a hamburger, test multi-stage planning and temporal consistency, while bimanual tasks, such as object handover and collaborative towel folding, introduce coordination constraints between two hands. Together, this structured task design supports fine-grained evaluation of how video world models handle increasingly complex embodied interactions. 

### **3.5 Evaluation of Embodied Executability** 

We define _embodied executability_ as whether behaviors inferred from generated videos can be executed to complete the intended task. RoboWM-Bench evaluates executability at two levels: step-level verification and task-level success. For each task, we predefine a set of key action nodes corresponding to semantically meaningful interaction stages, such as contact events ( _e.g._ , grasping) or stable end-effector configurations ( _e.g._ , lifting). During execution, step-level verification checks 

5 

whether the predicted behavior satisfies the required interaction and dynamical constraints at each key node. A trajectory is considered task-level successful only if all key nodes pass these checks and the final task objective is achieved. This hierarchical protocol supports fine-grained failure diagnosis while providing a clear and measurable criterion for overall task completion. 

## **4 Experiments** 

We evaluate state-of-the-art video world models on RoboWM-Bench across a diverse set of humanhand and robotic manipulation tasks (Section 4.1). Our experiments first quantify embodied executability and characterize common failure modes (Section 4.2). We then compare RoboWM-Bench with PAI-Bench on the same generated videos to examine the complementary role of executionbased evaluation (Section 4.3). Finally, we validate the reliability of RoboWM-Bench through action-extraction and simulation-consistency analyses (Section 4.4). 

### **4.1 Environment Setup** 

### **4.1.1 Tasks and Environments** 

We evaluate video world models on the RoboWM-Bench task suite, which covers both human-hand and robotic manipulation tasks. In each robotic task setup, a Franka arm operates on a tabletop where objects are initialized with randomized poses, and the scene is observed from a camera viewpoint that remains fixed during evaluation. We consider both simulation-native scenarios and real-world scenes reconstructed through our real-to-sim pipeline, enabling generated robotic behaviors to be evaluated under a unified simulation-based execution protocol. 

For human-hand tasks, we use real-world scenes with randomized object poses. Following the input convention of LVP [9], the initial observation includes a visible human hand positioned above the tabletop, ensuring fair comparison across baselines. We focus on real-world scenes because simulating a real human hand within the physics engine would not faithfully capture human manipulation dynamics and would therefore provide limited evaluation value. 

All executions are conducted in the LeHome simulation environment [30, 38]. To ensure fair and reproducible comparison, each task uses 10 different initial object configurations shared across all models, together with standardized task descriptions, random seeds, and evaluation protocols. We report both task- and step-level success rates. 

### **4.1.2 Baselines** 

We evaluate state-of-the-art video world models covering both general-purpose and interactionoriented generation. For general-purpose video generation, we include closed-source models, Veo3.1 [17] and Wan2.6 [49], as well as open-source models, Wan2.2 [49] and Cosmos-Predict2.5 [2]. For interaction-oriented generation, we include LVP [9], which is specifically trained to capture complex human interactive behaviors. To further investigate the potential of video world models for embodied manipulation, we fine-tune Cosmos-Predict2.5 on our collected real-world manipulation dataset with 50 trajectories per task and denote the resulting variant as Cosmos-Finetune. 

### **4.2 Embodied Executability of Video World Models** 

Table 1 reports task- and step-level execution success rates. Results on simulation-native robotic tasks are provided in the supplementary due to space limitations (Section B). The experimental results reveal several consistent trends, which we analyze below. 

First, **human-hand videos achieve higher execution success than robotic manipulation videos.** This gap likely reflects biases in large-scale video pretraining, where human interactions are far more prevalent than robotic data. Generated human hands also tend to preserve more stable geometry during interaction, whereas robotic manipulators are more likely to exhibit structural distortions that lead to execution failures. 

Second, **execution success decreases as task complexity increases.** Short-horizon tasks such as _Push Button_ are generally easier, while longer-horizon tasks such as _Put in Drawer_ suffer from error accumulation across multiple interaction stages. Among human-hand tasks, _Fold Towel_ remains particularly challenging, reflecting the added complexity of deformable-object interactions. 

Third, **manipulation-specific fine-tuning improves robotic executability.** Cosmos-Finetune substantially outperforms its pretrained counterpart, indicating that even limited task-specific data, 

6 

Table 1: Embodied execution success rates (%) on RoboWM-Bench for human-hand (top two sections) and robotic manipulation tasks (bottom two sections), reported at both task and step levels. 

|||||**Human (T**|**ask Level)**||||
|---|---|---|---|---|---|---|---|---|
|**Method**|Pick Object|Push Button|Put on Plate|Pour Water|Stack Cups|Open Drawer|Put in Drawer|Fold Towel|
|Cosmos|23%|40%|15%|0%|10%|10%|10%|0%|
|Wan 2.2|57%|80%|55%|60%|40%|0%|20%|0%|
|Veo 3.1|73%|**100%**|30%|60%|20%|20%|60%|0%|
|Wan 2.6|**83%**|**100%**|**70%**|**80%**|**80%**|**80%**|**80%**|**40%**|
|LVP|70%|40%|**70%**|40%|20%|**80%**|40%|20%|
|||||**Human (S**|**tep Level)**||||
|**Method**||**Put on Plate**||||**Put in Drawer**|||
||contact|lift|place|contact|lift|above drawer|in drawer|close drawer|
|Cosmos|90%|20%|15%|80%|20%|20%|20%|10%|
|Wan 2.2|**100%**|60%|55%|**100%**|60%|60%|40%|20%|
|Veo 3.1|**100%**|70%|30%|**100%**|70%|70%|60%|60%|
|Wan 2.6<br>|**100%**<br>|**75%**<br>|**70%**<br>|**100%**<br>|**80%**<br>|**80%**<br>|**80%**<br>|**80%**<br>|
|LVP|**100%**|**75%**|**70%**|**100%**|70%|60%|50%|40%|
|||||**Robot (Ta**|**sk Level)**||||
|**Method**|Close Drawer|Pick Object|Push Object|Push Button|Put on Plate|Discard Trash|Pull Object|Put in Drawer|
|Cosmos|0%|10%|10%|10%|10%|0%|0%|0%|
|Wan 2.2|30%|10%|0%|0%|0%|0%|0%|0%|
|Veo 3.1|20%|20%|10%|20%|10%|0%|0%|0%|
|Wan 2.6|50%|20%|40%|40%|20%|10%|0%|0%|
|Cosmos-FT|**90%**|**50%**|**50%**|**60%**|**40%**|**30%**|**40%**|**20%**|
|||||**Robot (St**|**ep Level)**||||
|**Method**||**Put on Plate**||||**Put in Drawer**|||
||contact|lift|place|contact|lift|above drawer|in drawer|close drawer|
|Cosmos|30%|10%|10%|10%|0%|0%|0%|0%|
|Wan 2.2|20%|0%|0%|0%|0%|0%|0%|0%|
|Veo 3.1|40%|10%|10%|30%|0%|0%|0%|0%|
|Wan 2.6|40%|20%|20%|30%|0%|0%|0%|0%|
|Cosmos-FT|**60%**|**40%**|**40%**|**60%**|**20%**|**20%**|**20%**|**20%**|


with 50 trajectories per task, can improve the generation of executable robotic behaviors. Finetuning reduces robot-geometry artifacts and improves joint articulation, although errors in 3D object localization and grasp stability remain common failure factors. 

Figure 3 presents representative qualitative results from Wan2.6, the strongest overall model in our evaluation. Its success and failure cases therefore provide useful insight into the remaining gap between visual plausibility and embodied executability. These examples show that generated interactions can appear plausible in video while still failing under physical execution. In _Put on Plate_ , for instance, the predicted video shows the fingers merely touching the object without forming a stable grasp, yet the object is lifted. Such interactions are physically implausible and fail during execution. In _Open Drawer_ , the predicted motion resembles closing the drawer and does not establish a proper grasp, which is reflected by the simulated execution outcome. For robotic manipulation videos, failures can also arise from geometric distortions of the generated robot arm. The end effector may appear to reach the target in the video, while the recovered joint configuration yields a mismatched end-effector pose under the robot’s true forward kinematics. 

### **4.3 Perceptual Plausibility vs. Embodied Executability** 

We compare execution accuracy in RoboWM-Bench with the domain scores in PAI-Bench, a commonly used metric for evaluating the perceptual plausibility of generated videos. As shown in Figure 4, the same predicted videos obtain near-saturated scores on PAI-Bench across different world models, whereas RoboWM-Bench evaluates whether the predicted behaviors are physically executable, resulting in more discriminative outcomes. This discrepancy arises because some actions may appear visually plausible (Figure 3) yet remain physically infeasible, an issue that perceptual domain scores may not capture but becomes evident under embodied execution. These results highlight the complementary role of RoboWM-Bench and show that embodiment-grounded evaluation provides a more direct measure of physical executability. Further PAI-Bench analysis and domain-score implementation details are provided in Appendix D and Appendix J, respectively. 

7 


Figure 3: **Qualitative execution results on RoboWM-Bench.** For each task, predicted videos (left) are converted into robot actions and executed in simulation (right). 


Figure 4: Comparison between PAI-Bench and RoboWM-Bench. 

### **4.4 Reliability Analysis of RoboWM-Bench** 

To examine the reliability of RoboWM-Bench, we validate two key interfaces in the evaluation pipeline: real-to-sim execution consistency and video-to-action replay success. The former tests whether reconstructed simulation environments preserve real-world task outcomes, while the latter evaluates whether retargeting or inverse dynamics can recover executable actions from videos. 

### **4.4.1 Real-to-Sim Execution Consistency** 

We first assess whether reconstructed simulation environments preserve real-world execution outcomes. Specifically, we execute real-world robotic trajectories in the corresponding reconstructed simulation environments and compare task outcomes across domains. We use robotic trajectories because they provide the same low-level action sequences in both real and simulated scenes, keeping this test focused on reconstruction fidelity; video-to-action conversion, including human-to-robot retargeting, is evaluated separately in the next subsection. 

8 

|**Success Consistency**|**Failure Consistency**||||
|---|---|---|---|---|
|||Task|Success<br>Consistency|Failure<br>Consistency|
|||Pick Object|10/10|10/10|
|||Pull Object|10/10|10/10|
|||Push Object|10/10|10/10|
|||Put on Plate|10/10|10/10|
|||Discard Trash|10/10|10/10|
|||Close Drawer<br>Put in Drawer|10/10<br>10/10|10/10<br>10/10|
|||Average|100%|100%|


Figure 5: **Real-to-sim consistency evaluation.** Left: qualitative examples of replaying identical real-world trajectories in reconstructed simulation environments. Right: outcome agreement between real-world and reconstructed simulation executions. 

Table 2: Accuracy of action extraction methods. 

|||||**Hu**|**man**||||
|---|---|---|---|---|---|---|---|---|
|**Method**|Pick Object|Stack Cups|Pour Water|Open Drawer|Fold Towel|Put on Plate|Put in Drawer|Average|
|Retargeting|**100%**|**90%**|**90%**|**100%**|**100%**|**100%**|**100%**|**97.1%**|
|||||**Ro**|**bot**||||
|**Method**|Pick Object|Pull Object|Push Object|Discard Trash|Close Drawer|Put on Plate|Put in Drawer|Average|
|IDMReal<br>IDMSim+Real|70%<br>**100%**|70%<br>**90%**|80%<br>**100%**|70%<br>**90%**|90%<br>**100%**|70%<br>**100%**|50%<br>**90%**|71.4%<br>**95.7%**|


For each task, we collect 10 successful and 10 failed real-world trajectories and execute the same actions in the reconstructed simulation environments. Figure 5 shows that simulation consistently reproduces both success and failure outcomes. This consistency suggests that the reconstructed environments preserve the task-relevant geometry and interaction constraints needed for executionbased evaluation. Real-world and simulated videos are provided in the supplementary material. 

### **4.4.2 Video-to-Action Replay Success** 

We next evaluate whether the video-to-action modules can recover executable actions from videos. We process videos from successful real-world manipulation trajectories using our action extraction pipeline, and execute the extracted actions in the reconstructed simulation environments to test whether they reproduce the original outcomes. 

As shown in Table 2, the human-hand pose tracking and retargeting pipeline achieves near-perfect replay success. The remaining failures in _Stack Cups_ and _Pour Water_ occur in deliberately contactsensitive cases involving cylindrical objects, where small discrepancies between human fingertip contacts and retargeted robot gripper contacts can destabilize grasps. These cases provide conservative stress tests for retargeting accuracy rather than typical failures observed across most generated videos. 

For robotic videos, we compare IDMReal, trained on 50 real-world trajectories per task, with IDMSim+Real, which uses large-scale simulation pretraining followed by finetuning on the same real-world trajectories. IDMSim+Real achieves substantially higher replay success, indicating that scalable action-labeled simulation data provides useful motion priors and improves inverse-dynamics prediction. The remaining failures mainly arise in near-boundary contact cases, such as intentionally shallow grasps, where minor prediction errors can compromise grasp stability. 

## **5 Conclusion** 

We introduced RoboWM-Bench, a manipulation-centric benchmark for evaluating video world models through embodiment-grounded execution. RoboWM-Bench converts predicted humanhand and robotic manipulation videos into executable actions and validates them in standardized simulation and real-to-sim environments using step-level and task-level execution metrics. Covering diverse object dynamics, task horizons, and coordination requirements, the benchmark provides a scalable and reproducible protocol that complements perceptual video evaluation with execution- 

9 

based assessment. Experiments with state-of-the-art video world models show that embodied execution reveals additional challenges in complex manipulation settings, particularly those requiring precise contact, deformable-object reasoning, or long-horizon consistency. Overall, RoboWM-Bench offers an execution-grounded diagnostic framework for advancing physically consistent world models for robotic manipulation. 

## **References** 

- [1] Agarwal, N., Ali, A., Bala, M., Balaji, Y., Barker, E., Cai, T., Chattopadhyay, P., Chen, Y., Cui, Y., Ding, Y., et al.: Cosmos world foundation model platform for physical ai. arXiv preprint arXiv:2501.03575 (2025) 

- [2] Ali, A., Bai, J., Bala, M., Balaji, Y., Blakeman, A., Cai, T., Cao, J., Cao, T., Cha, E., Chao, Y.W., et al.: World simulation with video foundation models for physical ai. arXiv preprint arXiv:2511.00062 (2025) 

- [3] Assran, M., Bardes, A., Fan, D., Garrido, Q., Howes, R., Muckley, M., Rizvi, A., Roberts, C., Sinha, K., Zholus, A., et al.: V-jepa 2: Self-supervised video models enable understanding, prediction and planning. arXiv preprint arXiv:2506.09985 (2025) 

- [4] Bai, S., Cai, Y., Chen, R., Chen, K., Chen, X., Cheng, Z., Deng, L., Ding, W., Gao, C., Ge, C., Ge, W., Guo, Z., Huang, Q., Huang, J., Huang, F., Hui, B., Jiang, S., Li, Z., Li, M., Li, M., Li, K., Lin, Z., Lin, J., Liu, X., Liu, J., Liu, C., Liu, Y., Liu, D., Liu, S., Lu, D., Luo, R., Lv, C., Men, R., Meng, L., Ren, X., Ren, X., Song, S., Sun, Y., Tang, J., Tu, J., Wan, J., Wang, P., Wang, P., Wang, Q., Wang, Y., Xie, T., Xu, Y., Xu, H., Xu, J., Yang, Z., Yang, M., Yang, J., Yang, A., Yu, B., Zhang, F., Zhang, H., Zhang, X., Zheng, B., Zhong, H., Zhou, J., Zhou, F., Zhou, J., Zhu, Y., Zhu, K.: Qwen3-vl technical report. arXiv preprint arXiv:2511.21631 (2025) 

- [5] Baker, B., Akkaya, I., Zhokov, P., Huizinga, J., Tang, J., Ecoffet, A., Houghton, B., Sampedro, R., Clune, J.: Video pretraining (vpt): Learning to act by watching unlabeled online videos. Advances in Neural Information Processing Systems **35** , 24639–24654 (2022) 

- [6] Bharadhwaj, H., Dwibedi, D., Gupta, A., Tulsiani, S., Doersch, C., Xiao, T., Shah, D., Xia, F., Sadigh, D., Kirmani, S.: Gen2act: Human video generation in novel scenarios enables generalizable robot manipulation. arXiv preprint arXiv:2409.16283 (2024) 

- [7] Bjorck, J., Castañeda, F., Cherniadev, N., Da, X., Ding, R., Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al.: Gr00t n1: An open foundation model for generalist humanoid robots. arXiv preprint arXiv:2503.14734 (2025) 

- [8] Brooks, T., Peebles, W., Holmes, C., DePue, W., Guo, Y., Jing, L., Schnurr, D., Taylor, J., Luhman, T., Ng, C., Wang, R., Ramesh, A., et al.: Video generation models as world simulators. `https://openai.com/research/video-generation-models-as-world-simulators` (2024), openAI Technical Report 

- [9] Chen, B., Zhang, T., Geng, H., Song, K., Zhang, C., Li, P., Freeman, W.T., Malik, J., Abbeel, P., Tedrake, R., et al.: Large video planner enables generalizable robot control. arXiv preprint arXiv:2512.15840 (2025) 

- [10] Chen, S., Guo, H., Zhu, S., Zhang, F., Huang, Z., Feng, J., Kang, B.: Video depth anything: Consistent depth estimation for super-long videos. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 22831–22840 (2025) 

- [11] Chen, X., Chu, F.J., Gleize, P., Liang, K.J., Sax, A., Tang, H., Wang, W., Guo, M., Hardin, T., Li, X., et al.: Sam 3d: 3dfy anything in images. arXiv preprint arXiv:2511.16624 (2025) 

- [12] Chi, X., Jia, P., Fan, C.K., Ju, X., Mi, W., Zhang, K., Qin, Z., Tian, W., Ge, K., Li, H., et al.: Wow: Towards a world omniscient world model through embodied interaction. arXiv preprint arXiv:2509.22642 (2025) 

- [13] Du, Y., Yang, S., Dai, B., Dai, H., Nachum, O., Tenenbaum, J., Schuurmans, D., Abbeel, P.: Learning universal policies via text-guided video generation. Advances in neural information processing systems **36** , 9156–9172 (2023) 

10 

- [14] Fan, C.K., Chi, X., Ju, X., Li, H., Bao, Y., Wang, Y.K., Chen, L., Jiang, Z., Ge, K., Li, Y., et al.: Wow, wo, val! a comprehensive embodied world model evaluation turing test. arXiv preprint arXiv:2601.04137 (2026) 

- [15] Feng, W., Li, J., Saxon, M., Fu, T.j., Chen, W., Wang, W.Y.: Tc-bench: Benchmarking temporal compositionality in text-to-video and image-to-video generation. arXiv preprint arXiv:2406.08656 (2024) 

- [16] Gao, Y., Guo, H., Hoang, T., Huang, W., Jiang, L., Kong, F., Li, H., Li, J., Li, L., Li, X., et al.: Seedance 1.0: Exploring the boundaries of video generation models. arXiv preprint arXiv:2506.09113 (2025) 

- [17] Google DeepMind: Veo: a text-to-video generation system (veo-3 technical report). Tech. Rep. Veo-3-Tech-Report, Google DeepMind (2025), `https://storage.googleapis.com/ deepmind-media/veo/Veo-3-Tech-Report.pdf` , technical Report 

- [18] Grauman, K., Westbury, A., Byrne, E., Chavis, Z., Furnari, A., Girdhar, R., Hamburger, J., Jiang, H., Liu, M., Liu, X., et al.: Ego4d: Around the world in 3,000 hours of egocentric video. In: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. pp. 18995–19012 (2022) 

- [19] HaCohen, Y., Chiprut, N., Brazowski, B., Shalem, D., Moshe, D., Richardson, E., Levin, E., Shiran, G., Zabari, N., Gordon, O., et al.: Ltx-video: Realtime video latent diffusion. arXiv preprint arXiv:2501.00103 (2024) 

- [20] Hong, W., Ding, M., Zheng, W., Liu, X., Tang, J.: Cogvideo: Large-scale pretraining for text-to-video generation via transformers. arXiv preprint arXiv:2205.15868 (2022) 

- [21] Huang, S., Chen, L., Zhou, P., Chen, S., Jiang, Z., Hu, Y., Liao, Y., Gao, P., Li, H., Yao, M., et al.: Enerverse: Envisioning embodied future space for robotics manipulation (2025). arXiv preprint arXiv:2501.01895 (2025) 

- [22] Huang, Z., He, Y., Yu, J., Zhang, F., Si, C., Jiang, Y., Zhang, Y., Wu, T., Jin, Q., Chanpaisit, N., et al.: Vbench: Comprehensive benchmark suite for video generative models. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 21807–21818 (2024) 

- [23] Jang, J., Ye, S., Lin, Z., Xiang, J., Bjorck, J., Fang, Y., Hu, F., Huang, S., Kundalia, K., Lin, Y.C., et al.: Dreamgen: Unlocking generalization in robot learning through video world models. arXiv preprint arXiv:2505.12705 (2025) 

- [24] Ji, P., Xiao, C., Tai, H., Huo, M.: T2vbench: Benchmarking temporal dynamics for text-to-video generation. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 5325–5335 (2024) 

- [25] Kareer, S., Pertsch, K., Darpinian, J., Hoffman, J., Xu, D., Levine, S., Finn, C., Nair, S.: Emergence of human to robot transfer in vision-language-action models. arXiv preprint arXiv:2512.22414 (2025) 

- [26] Labbé, Y., Manuelli, L., Mousavian, A., Tyree, S., Birchfield, S., Tremblay, J., Carpentier, J., Aubry, M., Fox, D., Sivic, J.: Megapose: 6d pose estimation of novel objects via render & compare. arXiv preprint arXiv:2212.06870 (2022) 

- [27] Lepert, M., Fang, J., Bohg, J.: Masquerade: Learning from in-the-wild human videos using data-editing. arXiv preprint arXiv:2508.09976 (2025) 

- [28] Lepert, M., Fang, J., Bohg, J.: Phantom: Training robots without robots using only human videos. URL https://arxiv. org/abs/2503.00779 **2** (2025) 

- [29] Li, D., Fang, Y., Chen, Y., Yang, S., Cao, S., Wong, J., Luo, M., Wang, X., Yin, H., Gonzalez, J.E., et al.: Worldmodelbench: Judging video generation models as world models. arXiv preprint arXiv:2502.20694 (2025) 

11 

- [30] Li, Z., Yang, Y., Xie, S., Xu, K., Chen, T., Wang, Y., Shen, Z., Shen, Y., Chen, Y., Li, W., Zheng, Y., Zhang, C., Lin, S., Teng, F., Yang, H., Chen, M., Xie, S., Wu, R.: Lehome: A simulation environment for deformable object manipulation in household scenarios. In: IEEE International Conference on Robotics and Automation (ICRA) (2026) 

- [31] Li, Z., Tucker, R., Cole, F., Wang, Q., Jin, L., Ye, V., Kanazawa, A., Holynski, A., Snavely, N.: Megasam: Accurate, fast and robust structure and motion from casual dynamic videos. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 10486–10496 (2025) 

- [32] Ling, X., Zhu, C., Wu, M., Li, H., Feng, X., Yang, C., Hao, A., Zhu, J., Wu, J., Chu, X.: Vmbench: A benchmark for perception-aligned video motion generation. In: Proceedings of the IEEE/CVF International Conference on Computer Vision. pp. 13087–13098 (2025) 

- [33] Liu, Y., Cun, X., Liu, X., Wang, X., Zhang, Y., Chen, H., Liu, Y., Zeng, T., Chan, R., Shan, Y.: Evalcrafter: Benchmarking and evaluating large video generation models. In: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. pp. 22139–22149 (2024) 

- [34] Luo, Y., Du, Y.: Grounding video models to actions through goal conditioned exploration. arXiv preprint arXiv:2411.07223 (2024) 

- [35] Ma, Y.J., Sodhani, S., Jayaraman, D., Bastani, O., Kumar, V., Zhang, A.: Vip: Towards universal visual reward and representation via value-implicit pre-training. arXiv preprint arXiv:2210.00030 (2022) 

- [36] McCarthy, R., Tan, D.C., Schmidt, D., Acero, F., Herr, N., Du, Y., Thuruthel, T.G., Li, Z.: Towards generalist robot learning from internet video: A survey. Journal of Artificial Intelligence Research **83** (2025) 

- [37] Nair, S., Rajeswaran, A., Kumar, V., Finn, C., Gupta, A.: R3m: A universal visual representation for robot manipulation. arXiv preprint arXiv:2203.12601 (2022) 

- [38] NVIDIA Corporation: Nvidia isaac sim: High-fidelity simulation for robotics. `https:// developer.nvidia.com/isaac-sim` (2023), accessed: 2026-03-03 

- [39] Pavlakos, G., Shan, D., Radosavovic, I., Kanazawa, A., Fouhey, D., Malik, J.: Reconstructing hands in 3d with transformers. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 9826–9836 (2024) 

- [40] Punamiya, R., Patel, D., Aphiwetsa, P., Kuppili, P., Zhu, L.Y., Kareer, S., Hoffman, J., Xu, D.: Egobridge: Domain adaptation for generalizable imitation from egocentric human data. In: Human to Robot: Workshop on Sensorizing, Modeling, and Learning from Humans (2025) 

- [41] Qin, Y., Wu, Y.H., Liu, S., Jiang, H., Yang, R., Fu, Y., Wang, X.: Dexmv: Imitation learning for dexterous manipulation from human videos. In: European Conference on Computer Vision. pp. 570–587. Springer (2022) 

- [42] Radosavovic, I., Xiao, T., James, S., Abbeel, P., Malik, J., Darrell, T.: Real-world robot learning with masked visual pre-training. In: Conference on Robot Learning. pp. 416–426. PMLR (2023) 

- [43] Shang, Y., Li, Z., Ma, Y., Su, W., Jin, X., Wang, Z., Jin, L., Zhang, X., Tang, Y., Su, H., et al.: Worldarena: A unified benchmark for evaluating perception and functional utility of embodied world models. arXiv preprint arXiv:2602.08971 (2026) 

- [44] Team, G.R., Choromanski, K., Devin, C., Du, Y., Dwibedi, D., Gao, R., Jindal, A., Kipf, T., Kirmani, S., Leal, I., et al.: Evaluating gemini robotics policies in a veo world simulator. arXiv preprint arXiv:2512.10675 (2025) 

- [45] Team, G., Ye, A., Wang, B., Ni, C., Huang, G., Zhao, G., Li, H., Li, J., Zhu, J., Feng, L., et al.: Gigabrain-0: A world model-powered vision-language-action model. arXiv preprint arXiv:2510.19430 (2025) 

- [46] Team, G., Ye, A., Wang, B., Ni, C., Huang, G., Zhao, G., Li, H., Zhu, J., Li, K., Xu, M., et al.: Gigaworld-0: World models as data engine to empower embodied ai. arXiv preprint arXiv:2511.19861 (2025) 

12 

- [47] Team, K., Chen, J., Ding, Y., Fang, Z., Gai, K., Gao, Y., He, K., Hua, J., Jiang, B., Lao, M., et al.: Klingavatar 2.0 technical report. arXiv preprint arXiv:2512.13313 (2025) 

- [48] Tian, Y., Yang, S., Zeng, J., Wang, P., Lin, D., Dong, H., Pang, J.: Predictive inverse dynamics models are scalable learners for robotic manipulation. arXiv preprint arXiv:2412.15109 (2024) 

- [49] Wan, T., Wang, A., Ai, B., Wen, B., Mao, C., Xie, C.W., Chen, D., Yu, F., Zhao, H., Yang, J., et al.: Wan: Open and advanced large-scale video generative models. arXiv preprint arXiv:2503.20314 (2025) 

- [50] Wang, Y., Chen, X., Ma, X., Zhou, S., Huang, Z., Wang, Y., Yang, C., He, Y., Yu, J., Yang, P., et al.: Lavie: High-quality video generation with cascaded latent diffusion models. International Journal of Computer Vision **133** (5), 3059–3078 (2025) 

- [51] Wen, B., Yang, W., Kautz, J., Birchfield, S.: Foundationpose: Unified 6d pose estimation and tracking of novel objects. In: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. pp. 17868–17879 (2024) 

- [52] World Labs: Marble: A Multimodal World Model (2025), `https://www.worldlabs.ai/ blog/marble-world-model` , accessed: 2026-02 

- [53] Wu, B., Zou, C., Li, C., Huang, D., Yang, F., Tan, H., Peng, J., Wu, J., Xiong, J., Jiang, J., et al.: Hunyuanvideo 1.5 technical report. arXiv preprint arXiv:2511.18870 (2025) 

- [54] Wu, T., Zhang, J., Liang, S., Han, Z., Dong, H.: Foundation feature-driven online end-effector pose estimation: A marker-free and learning-free approach. In: 2025 IEEE International Conference on Robotics and Automation (ICRA). pp. 1921–1928. IEEE (2025) 

- [55] Xiong, H., Li, Q., Chen, Y.C., Bharadhwaj, H., Sinha, S., Garg, A.: Learning by watching: Physical imitation of manipulation skills from human videos. In: 2021 IEEE/RSJ international conference on intelligent robots and systems (iros). pp. 7827–7834. IEEE (2021) 

- [56] Yang, L., Kang, B., Huang, Z., Xu, X., Feng, J., Zhao, H.: Depth anything: Unleashing the power of large-scale unlabeled data. In: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. pp. 10371–10381 (2024) 

- [57] Yang, M., Du, Y., Ghasemipour, K., Tompson, J., Schuurmans, D., Abbeel, P.: Learning interactive real-world simulators. arXiv preprint arXiv:2310.06114 **1** (2), 6 (2023) 

- [58] Ye, S., Jang, J., Jeon, B., Joo, S., Yang, J., Peng, B., Mandlekar, A., Tan, R., Chao, Y.W., Lin, B.Y., et al.: Latent action pretraining from videos. arXiv preprint arXiv:2410.11758 (2024) 

- [59] Yue, H., Huang, S., Liao, Y., Chen, S., Zhou, P., Chen, L., Yao, M., Ren, G.: Ewmbench: Evaluating scene, motion, and semantic quality in embodied world models. arXiv preprint arXiv:2505.09694 (2025) 

- [60] Zheng, D., Huang, Z., Liu, H., Zou, K., He, Y., Zhang, F., Gu, L., Zhang, Y., He, J., Zheng, W.S., et al.: Vbench-2.0: Advancing video generation benchmark suite for intrinsic faithfulness. arXiv preprint arXiv:2503.21755 (2025) 

- [61] Zhou, F., Huang, J., Li, J., Ramanan, D., Shi, H.: Pai-bench: A comprehensive benchmark for physical ai. arXiv preprint arXiv:2512.01989 (2025) 

- [62] Zhou, S., Du, Y., Chen, J., Li, Y., Yeung, D.Y., Gan, C.: Robodreamer: Learning compositional world models for robot imagination. arXiv preprint arXiv:2404.12377 (2024) 

13 

## **A Limitations** 

RoboWM-Bench evaluates predicted manipulation videos by converting them into executable actions and validating them through simulation-based execution. Although we validate both the real-to-sim environments and the action-extraction modules, as discussed in Section 4.4, the protocol still relies on intermediate video-to-action interfaces. Such errors are most likely to affect highly contact-sensitive or near-boundary interactions, where small pose or grasp deviations can change execution outcomes. For human-hand videos, RoboWM-Bench assesses executability through retargeted robot actions rather than direct simulation of human-hand dynamics, which remain challenging to model faithfully in current physics engines. While the current task suite covers diverse tabletop manipulation settings, it is not exhaustive; future extensions could include broader scene layouts and object categories. Finally, the step-level evaluation relies on task-specific key nodes and manually specified checkers. These checkers provide interpretable diagnostics, but scaling to larger task families may benefit from LLM- or VLM-assisted generation of simulation-based success predicates and key-node checkers, while retaining execution as the final validation signal. 

## **B Additional Results for Purely Simulated Robotic Tasks** 

RoboWM-Bench also includes a set of robotic manipulation tasks evaluated entirely in simulation environments. 

The task setup follows the same protocol described in the main paper. For each task, video world models generate future manipulation behaviors conditioned on the simulation observations and the corresponding task descriptions. The predicted behaviors are then converted into executable action sequences and executed in simulation to assess task completion. 

Table 3 reports both task-level and step-level execution success rates for these purely simulated tasks. The overall trends are consistent with those observed in the real-to-sim evaluation. As task complexity increases, the success rates of most models decrease, particularly for tasks requiring long-horizon reasoning or precise contact interactions. 

Table 3: Task-level and step-level embodied execution success rates (%) on RoboWM-Bench for robotic manipulation tasks evaluated entirely in simulation. 

|**Method**||||**Robot (T**|**ask Level)**|||||
|---|---|---|---|---|---|---|---|---|---|
||Close Draw|er<br>Push Bu|tton|Cut Sausage|Turn Off Faucet|Assem|ble|Burger|Fold Clothes|
|Cosmos|0%|10%||10%|0%||0%||0%|
|Wan 2.2<br>Wan 2.6|10%<br>30%|10%<br>20%||10%<br>40%|0%<br>0%||0%<br>0%||0%<br>0%|
|Veo|10%|20%||20%|0%||0%||0%|
|||||**Robot (S**|**tep Level)**|||||
|**Method**|<br>contact|**Turn Off Faucet**<br>rot. _>_ 20<sup>_◦_</sup>|turn off|**A**<br>contact|**ssemble Burger**<br>lift|place||**Fol**<br>L. sleeve|**d Clothes**<br>R. sleeve|
|Cosmos|10%|0%|0%|10%|0%|0%||0%|0%|
|Wan 2.2|10%|0%|0%|10%|0%|0%||0%|0%|
|Wan 2.6|40%|10%|0%|30%|0%|0%||0%|0%|
|Veo|20%|0%|0%|10%|0%|0%||0%|0%|


## **C Additional Results on Human Tasks** 

We additionally include human-hand manipulation tasks involving bimanual coordination. The detailed execution success rates are reported in Table 4. The results show that bimanual tasks are generally more challenging, as successful execution requires coordinated interactions between both hands to maintain physically feasible manipulation. 

## **D Comparison with PAI-Bench Quality Scores** 

We additionally compare the average quality scores in PAI-Bench [61] with the execution accuracy in RoboWM-Bench, as shown in Figure 6. Specifically, Figure 6 presents two scatter plots corresponding 

14 

Table 4: Task-level and step-level embodied execution success rates (%) on the additional human manipulation tasks involving bimanual coordination. 

||**Task Level**||||**Step Level**||||
|---|---|---|---|---|---|---|---|---|
|**Method**|**Cook**|grasp spatula|grasp pan|lift spatula|lift pan|spatula–pan<br>contact|place spatula|place pan|
|Cosmos|10%|30%|20%|20%|20%|20%|10%|20%|
|Wan 2.2<br>Wan 2.6|30%<br>**50%**|70%<br>**90%**|60%<br>**70%**|40%<br>**70%**|30%<br>**70%**|30%<br>**60%**|30%<br>**50%**|30%<br>**60%**|
|Veo|40%|80%|**70%**|**70%**|50%|60%|40%|50%|
|LVP|30%|80%|**70%**|60%|50%|40%|40%|30%|
||**Task Level**||**Step**|**Level**|||||
|**Method**<br>|**Lift Large Box**|grasp left|grasp right|lift|place||||
|Cosmos|10%|20%|20%|10%|10%||||
|Wan 2.2|30%|70%|60%|30%|30%||||
|Wan 2.6|**60%**|**90%**|**90%**|**70%**|**60%**||||
|Veo|50%|80%|80%|50%|50%||||
|LVP|30%|70%|70%|30%|30%||||


to human-hand tasks and robotic tasks, respectively. In both plots, the horizontal axis denotes the average quality score in PAI-Bench, while the vertical axis represents the execution accuracy measured in RoboWM-Bench. Each point corresponds to a specific world model baseline (indicated by color) on a particular manipulation task, reporting its average quality score and execution accuracy. 

As observed in the scatter plots, most points cluster along a vertical line around an average quality score of approximately 0.78, suggesting that the PAI-Bench quality scores are relatively consistent across different tasks and models. In contrast, the execution accuracy measured by RoboWM-Bench exhibits substantially greater variation. This discrepancy suggests that visual plausibility does not necessarily imply physical correctness, and the embodiment-grounded evaluation in RoboWM-Bench provides a more sensitive and informative measure of physical executability. 

Following the definitions and reporting protocol of PAI-Bench, we additionally present detailed domain and quality scores in tabular form. Note that all scores are computed using videos generated for the manipulation tasks in RoboWM-Bench, rather than the broader video sources used in PAIBench. Specifically, the detailed domain scores are reported in Table 5 for human-hand tasks and Table 6 for robotic tasks, while the detailed quality scores are reported in Table 7 and Table 8, respectively. 


Figure 6: Comparison between the average quality scores in PAI-Bench with the execution accuracy in RoboWM-Bench. The left scatter plot shows human-hand tasks, and the right scatter plot shows robotic tasks. 

15 

<u>Table 5:</u> **<u>PAI-Bench Domain Score</u>** <u>on Human-Hand Tasks.</u> 

|**Models**||||**Domai**|**n Score**||||**Avg.**|
|---|---|---|---|---|---|---|---|---|---|
||Pick Object|Push<br>Button|Put on Plate|Pour Water|Stack Cups|Open<br>Drawer|Put in<br>Drawer|Fold Towel||
|Cosmos|96|**100**|92|72|78|**100**|**100**|86|90.5|
|Wan 2.2|92|**100**|**100**|94|**100**|**100**|**100**|**100**|**98.3**|
|Wan 2.6|**100**|92|**100**|**100**|**100**|**100**|**100**|86|97.3|
|Veo|**100**|82|**100**|**100**|**100**|92|92|**100**|95.8|
|LVP|**100**|78|**100**|78|**100**|**100**|86|76|87.0|


<u>Table 6:</u> **<u>PAI-Bench Domain Score</u>** <u>on Robotic Real Tasks.</u> 

|**Models**||||**Domai**|**n Scores**||||**Avg.**|
|---|---|---|---|---|---|---|---|---|---|
||Close<br>Drawer|Pick Object|Push<br>Object|Push<br>Button|Put on Plate|Discard<br>Trash|Pull Object|Put in<br>Drawer||
|Cosmos|84|**100**|**100**|**100**|**100**|**100**|**100**|**100**|98.0|
|Wan 2.2|**100**|**100**|92|**100**|94|**100**|98|86|96.3|
|Wan 2.6|**100**|**100**|**100**|**100**|**100**|**100**|**100**|**100**|**99.5**|
|Veo|**100**|**100**|**100**|90|**100**|**100**|**100**|80|96.3|
|Cosmos-FT|**100**|**100**|**100**|**100**|**100**|92|**100**|100|**99.0**|


Table 7: **PAI-Bench Quality Score** on Human-Hand Tasks. Metrics follow the PAI-Bench protocol, including Subject Consistency (SC), Background Consistency (BC), Motion Smoothness (MS), Aesthetic Quality (AQ), Imaging Quality (IQ), Overall Consistency (OC), I2V Subject (IS), I2V Background (IB). 

|**Models**||||**Quality**|**Score**||||**Avg.**|
|---|---|---|---|---|---|---|---|---|---|
||**SC**|**BC**|**MS**|**AQ**|**IQ**|**OC**|**IS**|**IB**||
|Cosmos|95.0|94.9|99.5|**45.8**|74.9|25.6|98.3|98.5|79.1|
|Wan 2.2|95.5|94.9|99.1|41.7|74.5|26.2|**98.6**|98.5|78.6|
|Wan 2.6|**96.9**|95.6|99.2|40.5|**75.9**|25.8|98.4|97.9|78.8|
|Veo|96.0|95.5|**99.6**|40.9|75.4|**26.3**|98.5|**98.6**|**78.9**|
|LVP|96.3|**95.9**|99.4|36.4|74.4|25.6|98.1|98.0|78.0|


Table 8: **PAI-Bench Quality Score** on Robotic Real Tasks. 

|**Models**||||**Qualit**|**y Score**||||**Avg.**|
|---|---|---|---|---|---|---|---|---|---|
||**SC**|**BC**|**MS**|**AQ**|**IQ**|**OC**|**IS**|**IB**||
|Cosmos|94.9|92.9|99.4|44.3|74.5|22.2|94.0|93.5|77.0|
|Wan 2.2|96.5|94.6|99.5|43.9|73.5|23.2|94.6|93.2|77.4|
|Wan 2.6|**96.9**|**96.2**|99.4|**45.1**|**77.1**|23.3|94.3|92.8|**78.1**|
|Veo|95.1|92.5|**99.6**|44.4|70.1|**23.6**|95.0|94.8|76.9|
|Cosmos-FT|94.6|94.2|99.5|44.3|64.9|22.8|**98.2**|**98.5**|77.1|


16 

## **E More Visualizations** 

Figure 7 provides additional qualitative examples of the predicted manipulation videos and their corresponding embodied executions. These results complement the examples shown in Figure 3 of the main paper. 


Figure 7: **Additional qualitative results on RoboWM-Bench.** For each task, predicted videos (left) are converted into robot actions and executed in simulation (right). 

17 

## **F Discussion of Depth in Human-Hand Tracking** 

In our experiments, we empirically found that Phantom [28] provides the most reliable performance for pose tracking and retargeting in human-hand manipulation videos. Therefore, as described in Section 3.3.1 of the main paper, our pipeline builds upon Phantom with several adaptations. 

However, Phantom assumes access to ground-truth depth information, whereas in our setting such depth is not available for the videos predicted by world models. In practice, only the depth of the first frame can be obtained, as it is captured by the camera in the real-world or simulation environment. 

Recent works have explored leveraging depth estimation for video understanding [9, 31]. In our setting, we investigate whether estimated depth can improve human-hand tracking. To this end, we estimate depth from RGB frames using Video Depth Anything [10, 56] and evaluate two strategies. First, we directly use the absolute depth predicted by the model. However, as shown in Figure 8(a), the predicted depth shows a large discrepancy from the ground-truth. Second, we estimate relative depth for subsequent frames and align it with the ground-truth depth of the first frame to recover absolute depth values. As illustrated in Figure 8(b), the recovered depth remains imperfect. 

Empirically, we observe that incorporating these estimated depths does not improve downstream pose tracking and retargeting performance. Therefore, depth information is not used in the final pipeline. 


Figure 8: Visualization of depth estimation results. (a) The predicted absolute depth shows a large discrepancy from the ground-truth. (b) Aligning relative depth with the first-frame ground-truth depth improves consistency, although non-negligible errors still remain. 

## **G Compute Resources** 

The runtime of video-to-action processing depends on the video resolution, frame rate, and duration. We report representative processing times and GPU memory usage for the two procedures used in our evaluation. For human-hand pose estimation and retargeting, processing a predicted video at 1280 _×_ 720 resolution and 15 FPS, with a duration of up to 25 seconds, took approximately 112 seconds on a single NVIDIA RTX 4090 GPU and used about 5.5 GB of GPU memory. For IDM inference on robotic manipulation videos, processing a 1280 _×_ 720, 30-FPS, 5-second video took approximately 1.5 seconds on a single NVIDIA A800 GPU and used about 4 GB of GPU memory. The released code includes scripts for reproducing the evaluation on user hardware. 

## **H Broader impacts** 

RoboWM-Bench aims to support safer and more reliable development of video world models for robotic manipulation by providing standardized, reproducible, and execution-grounded evaluation. Its positive impact lies in revealing cases where visually plausible generated videos may not correspond 

18 

to executable manipulation behaviors. Potential risks include overinterpreting benchmark scores as sufficient evidence for real-world robot deployment or applying video-to-action pipelines without appropriate safeguards. To mitigate these risks, RoboWM-Bench is intended as a diagnostic evaluation protocol, with validation conducted in simulation or real-to-sim environments and without releasing personally identifiable or sensitive data. 

## **I Prompt Details for World Model Video Generation** 

In this section, we provide details on how instruction prompts are generated for world model video generation. 

### **I.1 Human-Hand Tasks** 

To generate instruction prompts for video world models on human tasks, we leverage the Qwen3-VLFlash [4] model to generate concise task-specific descriptions conditioned on the initial observation image and high-level task instructions (e.g., _Pick up the stapler on the table, and stay still._ ). The resulting descriptions generated by Qwen are summarized in Table 9 and Table 10. 

To further encourage physical consistency of the synthesized videos, we append a standardized set of constraints to the generated instruction: _"The entire human hand must remain fully visible in the frame at all times, with no cropping, no fingers cut off, and no part of the hand outside the camera view. The camera must remain completely static with no movement, no panning, no tilting, no zooming, and no change in viewpoint during the entire video. No extra or unnecessary motions are allowed, the hand must not perform any additional gestures such as turning to show the palm, posing, rotating unnecessarily. All other objects in the scene that are not being manipulated must remain completely stationary, with no position shift, no rotation, and no change in placement throughout the entire video."_ Empirically, we observe that including these constraints improves the quality of videos generated by the world models. 

19 

Table 9: Overview of human-hand manipulation tasks and their corresponding instruction prompts. 

|**Task Name**|**Input Image**|**Task Prompt**|
|---|---|---|
|Pick Object||The hand lowers slowly toward the stapler and gently grasps it<br>using the thumb and index finger. The stapler is lifted slowly<br>from the table surface without any bouncing or sliding.|
|Push Button||The hand moves downward toward the button. The fingers<br>make contact with the yellow surface. The hand applies<br>pressure causing the button to compress. The hand lifts up and<br>rest in the air.|
|Put on Plate||The hand slowly extend downward to gently grasp the banana<br>using the thumb and index finger and then slowly lifts the<br>banana straight up. The banana is then slowly placed on the<br>center of the plate.|
|Pour Water||The hand grasps the plastic cup using the thumb and the index<br>finger. It slowly lifts the cup from the table. It tilts the cup to<br>pour water into the paper cup. It releases the plastic cup.|
|Stack Cups||The hand grasps the left edge of the left cup using the thumb<br>and the index fingers and slowly lifts it, then moves it above the<br>right cup and lowers it to stack inside.|
|Open Drawer||The hand grasps the left edge of the transparent drawer using<br>the thumb and the index fingers then pulls it leftward causing<br>the drawer to slide open.|
|Put in Drawer||The hand slowly moves to grasp the banana using the thumb<br>and the index finger, lifts it and places it inside the clear drawer.<br>The hand pushes the drawer into the container until it is fully<br>closed.|
|Fold Towel||The hand grasps the left edge using the thumb and the index<br>fingers and lifts it. The hand folds the towel over to the right<br>edge. The hand aligns the edges and presses down to secure the<br>fold.|


20 

Table 10: Overview of human-hand manipulation tasks and their corresponding instruction prompts (continued). 

|**Task Name**|**Input Image**|**Task Prompt**|
|---|---|---|
|Cook||The person uses their left hand to pick up the wooden spatula<br>and places it into the frying pan, while their right hand holds<br>the handle of the pan and lift it up. They move the spatula<br>around inside the pan briefly as if stirring or scraping, then lift<br>the spatula out and place the wooden spatula and the frying pan<br>back on the table in their original position.|
|Lift Large Box||The person grasps both the left and right edges of the box using<br>the thumb and the index fingers, lifting it vertically off the<br>table.|


### **I.2 Robotic Tasks** 

To generate instruction prompts for video world models on robotic manipulation tasks, we also leverage the Qwen3-VL-Flash [4] model to generate concise task-specific descriptions conditioned on the initial observation image and high-level task instructions (e.g., _close drawer_ ). The resulting descriptions generated by Qwen are summarized in Table 11 and Table 12. 

To further encourage physical consistency of the synthesized videos, we append a standardized set of constraints to the generated instruction: _"Throughout the entire video, the gripper undergoes no structural deformation, only the opening angle of its jaws changes; the rotational movements of the robotic arm joints strictly adhere to its inherent mechanical structure; and the camera perspective remains completely unchanged."_ Empirically, we observe that including these constraints improves the quality of videos generated by the world models. 

21 

Table 11: Overview of real-to-sim robotic manipulation tasks and their corresponding instruction prompts. 

|**Task Name**|**Input Image**|**Task Prompt**|
|---|---|---|
|Close Drawer||The robotic arm closes its gripper and pushes the drawer back<br>to its closed position.|
|Pick Object||The robotic arm picks up the white cup from the table surface.|
|Push Object||The robotic arm closes its gripper and pushes the green cube<br>away from the base of the arm for a short distance.|
|Push Button||The robotic arm closes its gripper, then uses the gripper to<br>press the yellow button on the tabletop.|
|Put on Plate||The robotic arm picks up the white cup from the table and<br>moves its gripper above the plate, then releases the cup placing<br>it on the plate.|
|Discard Trash||The robotic arm picks up the green cube from the table and<br>moves its gripper above the trash bin, then releases the gripper<br>to drop the green cube into the trash bin.|
|Pull Object||The robotic arm closes its gripper and pulls the green cube<br>toward the robotic arm base for a short distance.|
|Put in Drawer||The robotic arm picks up the yellow banana, moves it above the<br>open drawer, releases the gripper so the banana falls inside,<br>then closes the gripper to push the drawer back to its closed<br>position.|


22 

Table 12: Overview of purely simulated robotic manipulation tasks and their corresponding instruction prompts. 

|**Task Name**|**Input Image**|**Task Prompt**|
|---|---|---|
|Close Drawer||The robotic arm closes its gripper and pushes the drawer back<br>to its closed position.|
|Push Button||The robotic arm closes its gripper, then uses the gripper to<br>press the yellow button on the tabletop.|
|Cut Sausage||The robotic arm uses a knife to cut the sausage on the table.|
|Turn Off Faucet||The robotic arm grasps the lever handle on the left side of the<br>faucet, then rotates it inward to turn off the water.|
|Assemble Burger||The robotic arm first pushes the meat patty from the left side of<br>the cutting board to its edge, then picks it up and places it on<br>top of the cheese in the plate located on the right side of the<br>cutting board.|
|Fold Clothes||The left arm grasps the cuff of the left sleeve, while the right<br>arm grasps the cuff of the right sleeve. Both arms then lift and<br>fold the sleeves inward toward the center of the shirt: the left<br>arm places the left cuff onto the left side of the shirt’s body, and<br>the right arm places the right cuff onto the right side of the<br>body, aligning them neatly along the torso.|


## **J Implementation Details of PAI-Bench Domain Score** 

To facilitate evaluation within the PAI-Bench framework, we design targeted VQA suites for humanhand tasks and robotic tasks, respectively. Within each suite, only the first question is task-dependent and varies across scenarios, while the remaining four questions are identical across all tasks. 

### **J.1 VQA Pairs for Human-Hand Tasks** 

**Question 1:** Does the human successfully complete the task: {The task description, such as the human hand grasping and lifting the banana from the table surface.} **options:** (A) **yes** (B) no (C) unclear **ground truth: A** 

23 

**Question 2:** Does the human hand make physical contact with the target object? **options:** (A) **yes** (B) no (C) unclear **ground truth: A** 

**Question 3:** Does the human hand maintain anatomically plausible hand structure throughout the video (no impossible bends/broken fingers/extra joints)? **options:** (A) **yes** (B) no (C) unclear **ground truth: A** 

**Question 4:** Do all task-relevant objects maintain their structural integrity without undergoing physically implausible deformations? 

**options:** (A) **yes** (B) no (C) unclear **ground truth: A** 

**Question 5:** Do all task-relevant objects exhibit physically plausible motions, without any sudden spatial displacement? **options:** (A) **yes** (B) no (C) unclear **ground truth: A** 

### **J.2 VQA Pairs for Robotic Tasks** 

**Question 1:** Does the robot successfully complete the task: {The task description, such as the robotic arm picks up the small yellow cube from the tabletop.} 

**options:** (A) **yes** (B) no (C) unclear **ground truth: A** 

**Question 2:** Does the robot gripper/hand make physical contact with the target object? **options:** (A) **yes** (B) no (C) unclear **ground truth: A** 

**Question 3:** Does the robotic system (arm and gripper) maintain structural integrity and a physically plausible configuration throughout the video, with no deformation of rigid links or gripper, and realistic joint rotations? **options:** (A) **yes** (B) no (C) unclear **ground truth: A** 

**Question 4:** Do all task-relevant objects maintain their structural integrity without undergoing physically implausible deformations? **options:** (A) **yes** (B) no (C) unclear **ground truth: A** 

**Question 5:** Do all task-relevant objects exhibit physically plausible motions, without any sudden spatial displacement? **options:** (A) **yes** (B) no (C) unclear **ground truth: A** 

24 

