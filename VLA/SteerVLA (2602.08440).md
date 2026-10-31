---
title: "SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios"
date: "2026-02-09"
authors: "Tian Gao; Celine Tan; Catherine Glossop; Timothy Gao; Jiankai Sun; Kyle Stachowicz"
url: https://arxiv.org/abs/2602.08440
pdf: https://arxiv.org/pdf/2602.08440
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.08440)** / [論文ページ](https://arxiv.org/abs/2602.08440)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 

**Tian Gao**<sup>* 1</sup> **Celine Tan**<sup>* 2</sup> **Catherine Glossop**<sup>2</sup> **Timothy Gao**<sup>2</sup> **Jiankai Sun**<sup>1</sup> **Kyle Stachowicz**<sup>2</sup> **Shirley Wu**<sup>1</sup> **Oier Mees**<sup>2 3</sup> **Dorsa Sadigh**<sup>1</sup> **Sergey Levine**<sup>2</sup> **Chelsea Finn**<sup>1</sup> 

## **Abstract** 

A fundamental challenge in autonomous driving is the integration of high-level, semantic reasoning for long-tail events with low-level, reactive control for robust driving. While large vision-language models (VLMs) trained on webscale data offer powerful common-sense reasoning, they lack the grounded experience necessary for safe vehicle control. We posit that an effective autonomous agent should leverage the world knowledge of VLMs to guide a steerable driving policy toward robust control in driving scenarios. To this end, we propose SteerVLA, which leverages the reasoning capabilities of VLMs to produce fine-grained language instructions that steer a vision-language-action (VLA) driving policy. Key to our method is this rich language interface between the high-level VLM and low-level VLA, which allows the high-level policy to more effectively ground its reasoning in the control outputs of the low-level policy. To provide fine-grained language supervision aligned with vehicle control, we leverage a VLM to augment existing driving data with detailed language annotations, which we find to be essential for effective reasoning and steerability. We evaluate SteerVLA on a challenging closed-loop benchmark, where it outperforms state-of-the-art methods by **4.77** points in overall driving score and by **8.04** points on a longtail subset. The project website is available at: https://steervla.github.io/. 

## **1. Introduction** 

Despite rapid progress in autonomous driving systems, longtail scenarios remain particularly challenging due to their 

> 1Stanford University 2University of California, Berkeley 3Microsoft. Correspondence to: Tian Gao _<_ tiangao@stanford.edu _>_ . 

inherent scarcity in driving data and the complex reasoning they require. A truly autonomous vehicle must handle ambiguous traffic flow in construction zones, unpredictable pedestrian behavior, and blocked lanes due to accidents, as well as the compositions of these scenarios. For example, in Fig. 1, the vehicle encounters an accident blocking the lane. It must first reason about the scenario and recognize that it cannot simply continue in the same lane. It then needs to decide the best course of action while considering the other vehicles on the road. Handling these long-tail scenarios effectively is fundamentally important to building safe and robust driving systems (Tian et al., 2024). 

Vision–language–action (VLA) models, derived from vision–language models (VLMs) and adapted to driving control via imitation learning, leverage strong semantic priors to generate embodied actions (Brohan et al., 2023a; Kim et al., 2024; Zhou et al., 2025a). However, long-tail driving scenarios often require reasoning over rare events, implicit social norms, and broader common-sense knowledge that can be very hard to infer reliably from immediate visual driving cues alone. Pretrained VLMs encode such semantic knowledge, but effectively applying it in driving depends on how these inferences are grounded in control. We focus on enabling semantic reasoning from VLMs to guide driving behavior in VLA policies, allowing effective use of pretrained knowledge in complex and long-tail driving scenarios. 

We present SteerVLA, a novel framework for VLA-based driving policies effective in both normal and long-tail scenarios. Our key insight is to steer VLA control using VLM reasoning through: 1) a high-level policy, fine-tuned from a pretrained VLM, that performs semantic and commonsense reasoning to analyze driving scenarios based on camera images, routing commands (e.g., “Turn left at the next intersection”) from navigation APIs, and historical vehicle states. This model outputs reasoning traces and _metaactions_ —driving instructions for ego-vehicle motion (e.g., “accelerate and make a wide left turn, cautiously monitoring the junction.”), and 2) a low-level policy, fine-tuned from a pretrained VLM to generate precise control actions conditioned on meta-actions. This design leverages the 

_Preprint. February 16, 2026._ 

1 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 


_Figure 1._ **SteerVLA encountering long-tail scenarios** . SteerVLA is able to quickly reason about and adapt to a traffic accident blocking the lane. It first slows down, then waits for a gap in the traffic, and merges when the lane is available. 

powerful reasoning capabilities of VLMs while producing fine-grained outputs for driving control in VLAs. 

The key challenges are enabling the high-level policy to reason over diverse driving scenarios and generate detailed commands, as well as training a low-level policy to reliably execute them in a steerable manner. For example, if an accident blocks the road and the car ahead enters the opposite driving lane, the high-level policy should reason that “The lane appears shared bidirectionally since the vehicle in front moved into the oncoming lane. Proceed cautiously” and output conservative acceleration from a stopped state. Given camera images and vehicle states, the low-level policy maps meta-actions to precise control actions such as speed control and steering angle. 

However, difficulty arises from the scarcity of natural language supervision in driving datasets, where language annotations are often missing or coarse, and rarely grounded in driving control. To provide high-quality language supervision, we design an automatic data generation pipeline that constructs language supervision explicitly grounded in control. Given driving scenes and their associated driving trajectories, the pipeline guides a VLM to generate or refine meta-actions that describe the underlying driving behaviors over a temporal window. The pipeline also augments images with mid-level representations (bounding boxes or trajectory projections) to help the VLM better reason about spatial relationships and align its understanding with driving control. Rather than relying on generic commands such as “decel- 

erate due to the stop sign”, we enrich meta-actions with details derived from trajectories, including motion intensity and directional adjustments. This results in grounded descriptions such as “decelerate rapidly and cautiously make a slight right adjustment before stopping for a sign,” which better steer the low-level policy. Using this automatically generated supervision, we fine-tune the high-level policy to reason over complex scenes and produce well-grounded meta-actions. We train the low-level policy to follow these detailed meta-actions and imitate the safe driving behavior in our training data. The high-level policy can then control the low-level policy at the meta-action level, allowing for safe, intelligent responses in driving scenarios that require complex reasoning. 

This paper introduces a training and data generation framework that enables semantic reasoning to steer driving control, leading to strong performance in long-tail scenarios. We evaluate SteerVLA on the Bench2Drive (Jia et al., 2024) benchmark in the CARLA (Dosovitskiy et al., 2017) simulator. To test long-tail performance specifically, we identify 11 long-tail scenarios in Bench2Drive, which we term Bench2Drive-LongTail. We find that SteerVLA outperforms state-of-the-art methods by **4.77** points in driving score on Bench2Drive overall, and notably by **8.04** points on Bench2Drive-LongTail, confirming that grounded reasoning improves generalization in long-tail scenarios. 

2 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 

## **2. Related Work** 

We review related work in three areas: VLA–based driving models, methods that incorporate reasoning into driving models, and data labeling for driving data. 

**Vision-language-action models in driving.** Although autonomous driving has traditionally consisted of methods that use a stack of perception, prediction, and planning modules (Hu et al., 2023; Huang et al., 2021; Sun et al., 2021), massive progress has been made with end-to-end imitation learning methods that directly map multi-modal inputs to driving commands (Feng & Alahi, 2025; Nguyen et al., 2025; Zheng et al., 2025; Hegde et al., 2025). These methods generally excel in generic driving scenarios, but can struggle to generalize to long-tail scenarios, as these are not well-covered in driving data. 

Several works have gone beyond training end-to-end policies from scratch and leverage large language and visionlanguage models to leverage their pre-trained capabilities. Various works fine-tune pre-trained large language models on driving data (Jia et al., 2023; Yuan et al., 2024; Hwang et al., 2024b; Arai et al., 2025; Zhou et al., 2025a; Fu et al., 2025; Gao et al., 2025; Zhou et al., 2025c; Wang et al., 2023; Shao et al., 2024). Some (Chen et al., 2024a; Xu et al., 2024) integrate multimodal inputs, such as images, by projecting them into token space, while others (Mao et al., 2023a;b; Qian et al., 2025) adapt pre-trained VLMs as motion planners through text-based fine-tuning. Inspired by the success of pretrained vision-language models (VLMs), several works have introduced _vision-language-action_ (VLA) models (Brohan et al., 2023a), which consist of a VLM backbone fine-tuned to produce robot actions (Kim et al., 2024). These models benefit from excellent cross-modal grounding between language and vision, enabling the transfer of internet-scale semantic knowledge from their pre-training data. However, a key challenge for these methods is retaining the strong capabilities learned during pre-training, which can be lost when transferring to the domain of action prediction, a task very different from those found in VLM pre-training (Driess et al., 2025). While some of these methods fine-tune VLMs with an action head (Hwang et al., 2024a; Zhou et al., 2025b; Tian et al., 2024; Renz et al., 2025) to mitigate this issue, we explicitly use a hierarchical model, allowing the high-level policy training to stay closer to VLM pre-training tasks. Moreover, we develop an auto-labeling pipeline for autonomous driving data, real or simulated, to provide dense language labels in the form of reasoning traces and detailed meta-action labels, to train the high-level and low-level policies. We find that while the hierarchical structure is essential for retention of the reasoning capabilities of the base VLM in the high-level policy, these dense labels are what allow for effective communication between the policies, which is key to SteerVLA’s 

performance in long-tail scenarios. 

**Reasoning in Autonomous Driving.** Recent works have sought to imbue VLAs with reasoning capabilities (Zawalski et al., 2024; Zhao et al., 2025; Mu et al., 2023; Shi et al., 2024; Belkhale et al., 2024; Chen et al., 2025; Tan et al., 2025; Liu et al., 2026; Ye et al., 2025) to improve generalization and compositional task-following. In the driving domain, reasoning has been primarily used in the form of chain-of-thought steps (Zhou et al., 2025c; Qian et al., 2025; Wang et al., 2025; Luo et al., 2025; Hegde et al., 2025; Xu et al., 2024; Renz et al., 2025), casting reasoning as detecting other vehicles, describing the scene, performing question-answering tasks, or providing explainability or justification signals. While these methods improve reasoning or generalization, they remain largely descriptive. In contrast, we use our auto-labeling pipeline to generate both descriptive reasoning traces, specifically including the states of other vehicles and traffic sign information, and detailed _prescriptive_ meta-action labels. Most similar to our work is SimLingo (Renz et al., 2025), which also focuses on longtail driving scenario capabilities and achieves state-of-theart performance on the Bench2Drive benchmark. However, SimLingo relies on access to “action dreaming” data. This consists of safe and unsafe trajectories collected in CARLA with access to privileged information, exposing the policy to counterfactual scenarios beyond expert demonstrations. SteerVLA’s auto-labeling pipeline does not require access to privileged simulation information, and can be easily transferred to real-world data. We find that we can achieve improved long-tail performance with the labels generated by our auto-labeling pipeline in combination with a hierarchical policy structure. We also do not rely on additional data to improve reasoning and steerability, but achieve this through our hierarchical architecture and detailed meta-action labels to steer the low-level policy, especially in scenarios where reasoning about other agents is required, such as the “blocked intersection” and “construction zone” scenarios shown in Fig. 4 and Fig. 5. 

**Data labeling for Autonomous Driving.** Several works have aimed to label driving data with language to improve interpretability and reasoning capabilities in driving models. Some use a purely manual labeling process (Xu et al., 2020; Deruyttere et al., 2019; Malla et al., 2022; Wu et al., 2025), which introduces high overhead, but can result in more natural and realistic labels. Other works use a mixture of VLM-generated labels and human verification to create a more scalable labeling pipeline (Sima et al., 2024; Inoue et al., 2023; He & Shi, 2025). SteerVLA is trained on data generated from our fully automatic labeling pipeline and does not require human supervision. Many of these works focus on visual question-answering tasks (Sima et al., 2024; Inoue et al., 2023) or explanations of driving behavior (Xu et al., 2020; Malla et al., 2022), aiming to improve scene 

3 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 

understanding and interpretability but with limited focus on precisely prescribing the actions the vehicle should take. SteerVLA’s auto-labeling pipeline aims to extract information from driving data and organize it into comprehensive reasoning traces and detailed meta-action labels. These labels go beyond the typical commands used in prior work, such as “Accelerate” or “Turn left”. Instead, we augment these commands with the manner in which these behaviors should be executed, for example, “Accelerate cautiously with a slight left adjustment to avoid the construction site”. To further enhance the VLM’s spatial reasoning during labeling, we overlay mid-level representations (bounding boxes or trajectory projections) onto the driving images. By training the high-level policy to generate these information-rich meta-actions and the low-level policy to follow them, we can effectively ground the high-level reasoning into low-level control. 

## **3. Preliminaries** 

**Problem statement.** We formulate autonomous driving as a sequential decision-making problem. We assume access to a standard navigation system that provides high-level routing commands to guide the vehicle toward a destination. At each timestep _t_ , the agent receives an observation _ot_ = _{It, qt−k_ +1: _t}_ and a routing command _ℓt_ , where _It_ is the current front-view camera image, _qt−k_ +1: _t_ denotes the recent history of ego vehicle states (e.g., past speeds and headings over the last _k_ steps), and _ℓt_ is provided by a navigation system (e.g., turn-by-turn guidance such as “turn left in 50 m”). The objective is to predict a chunk of future actions _At_ = [ _at, at_ +1 _, . . . , at_ + _H−_ 1] that specify low-level control signals (e.g., future waypoints) over a horizon _H_ (Zhao et al., 2023). A driving policy is therefore a conditional distribution _π_ ( _At | ot, ℓt_ ) that maps the current observation and routing command to a distribution over action chunks. Training proceeds by maximizing the likelihood of expert demonstrations: max _θ_ E( _At,ot,ℓt_ ) _∼D_ [log _πθ_ ( _At | ot, ℓt_ )], where _D_ is a dataset of expert driving trajectories paired with synchronized routing commands. 

**Driving vision-language-action models.** Recent driving VLA models (Hwang et al., 2024a; Zhou et al., 2025b) learn a direct mapping from routing commands _ℓt_ and visual observations _It_ to driving control actions _At_ , typically by fine-tuning a pretrained vision–language model on driving data. Some approaches, such as SimLingo (Renz et al., 2025), generate a language-based description of the intended driving behavior (i.e., a meta-action) as a chain-of-thought step before producing driving actions. Our low-level policy in CARLA builds upon SimLingo (Renz et al., 2025), which uses InternVL2-1B (Chen et al., 2024b) as the pretrained VLM backbone and represents actions as future waypoints. 

Waypoint prediction is performed by lightweight MLP heads on top of the VLM outputs and is trained using a Smooth L1 loss. 

## **4. SteerVLA** 

In this section, we introduce SteerVLA, a framework that leverages VLM semantic reasoning to steer a VLA policy toward grounded and context-aware driving control. An overview of SteerVLA is shown in Fig. 2. 

### **4.1. Steering VLA Control using VLM Reasoning** 

We focus on the challenge of long-tail driving scenarios, where rare and unanticipated events require strong generalization and common-sense reasoning from the policy. VLAs are a strong backbone for driving because they combine semantic grounding from vision–language pretraining with domain-specific adaptation obtained via imitation learning on driving data. Building on this capability, we leverage the reasoning and semantic inference abilities of VLMs and ground these inferences in driving control through finegrained meta-actions that steer a VLA policy. Concretely, a high-level policy first reasons about the driving scene, historical vehicle states, and routing command to produce a meta-action _mt_ , accompanied by a short reasoning trace _ct_ that reasons over driving scenes and helps the policy generate more appropriate meta-actions. Formally, given observation _ot_ = _{It, qt−k_ +1: _t}_ with image _It_ , historical ego vehicle states _qt−k_ +1: _t_ , and routing command _ℓt_ , the high-level policy outputs ( _ct, mt_ ) _∼ πhl_ ( _ct, mt | ot, ℓt_ ). The low-level VLA then predicts future waypoints _At_ = [ _at, at_ +1 _, . . . , at_ + _H−_ 1] conditioned on both the observation and the meta-action, i.e., _At ∼ πll_ ( _At | ot, mt_ ). This design improves generalization by offloading high-level reasoning to the high-level policy, while allowing the VLA to specialize in fast and accurate waypoint prediction conditioned on the high-level’s instructions. 

**High-level policy.** We finetune the high-level policy _πhl_ ( _ct, mt|ot, ℓt_ ) with a pre-trained VLM as the base model. Our dataset generation pipeline, which we introduce in Section 4.2, provides supervision for the high-level policy outputs. The VLM’s strong semantic priors allow the high-level policy to reason about the vehicle’s surroundings and encode rich contextual information into its predicted meta-actions, enabling more context-aware action predictions. We structure the query to the VLM as a visual question-answering problem by providing the current visual observation _It_ , a six-second-long history of ego states _qt−k_ +1: _t_ (speed and heading) sampled at 0.5 Hz where _k_ = 3, and a routing command _ℓt_ . We train the model via a next-token prediction objective to generate a chain-of-thought reasoning trace _ct_ describing the positions and movement of critical agents in the scene, followed by an appropriate meta-action _mt_ . 

4 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 


_Figure 2._ **Framework overview** . Our model reasons over the driving context to produce reasoning traces and fine-grained meta-actions that guide driving control. A VLM generates structured semantic guidance, which steers a VLA policy in predicting future waypoints. To supervise reasoning and meta-action generation, we introduce an automatic data labeling pipeline that derives fine-grained language supervision from driving trajectories, improving alignment between language and control. 

**Low-level VLA policy.** Instead of using a general routing command as language input, our low-level policy _πll_ ( _At|ot, mt_ ) is steered by fine-grained meta-actions _mt_ generated by the high-level policy _πhl_ ( _ct, mt|ot, ℓt_ ) (see Section 4.2 for details on generating meta-action labels). We do not provide the reasoning trace as input to the lowlevel policy. The high-level policy already uses the reasoning trace as chain-of-thought to synthesize a well-grounded meta-action that distills the contextual and semantic information required for control. Conditioning the low-level policy only on the meta-action allows it to focus on precise execution and instruction following rather than semantic reasoning. 

### **4.2. Generating language labels for SteerVLA** 

To address the scarcity of fine-grained, control-grounded language supervision in driving datasets, we develop a fully autonomous labeling pipeline. We perform a two-stage query to Gemini 2.5 Flash-Lite (Team, 2025) that first identifies the baseline action taken by the vehicle (e.g., changing lanes, continuing straight), then uses trajectory information to enrich the language labels with fine-grained behavioral details explicitly tied to driving control. First, in our baseline categorization query, we provide Gemini 2.5 Flash-Lite with a grounded representation of the vehicle’s action using a projection of the vehicle’s future trajectory over a frontfacing camera view. We then perform a refinement step by providing the VLM with the vehicle’s speed and course over time to produce a nuanced description of the vehicle’s action. For example, we transform the original label “the car is continuing straight” into the more fine-grained “the 

car normally accelerates, then maintains speed while subtly drifting right”. This refinement step is crucial for passing as much information as possible to the low-level policy and can be applied to any existing language-labeled driving dataset, allowing us to augment these data with additional information that can improve steerability and performance of the driving policy. 

To improve the reasoning capabilities of the high-level policy, we additionally generate reasoning trace labels for each trajectory in the training data. These traces describe the scene and characterize the motion of other agents, serving as chain-of-thought supervision that guides the prediction of meta-actions. More details on the prompts used for our auto-labeling pipeline are provided in Section B.1 of the appendix. 

### **4.3. Implementation Details** 

For closed-loop evaluation in the CARLA simulator, we follow the recipe from SimLingo (Renz et al., 2025) to train the driving policy, building both the high-level and lowlevel policies upon InternVL2-1B (Chen et al., 2024b) as the pretrained VLM. Future actions are represented by two types of waypoints: (1) time-based waypoints sampled at 4 Hz, which determine target speed and temporal motion, and (2) geometry-based waypoints sampled at 1 m intervals, which describe the planned path and guide steering. These waypoints are converted into driving controls via PID controllers. 

We apply the refinement and reasoning trace generation processes described in Section 4.2 to the SimLingo dataset. To 

5 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 

construct reasoning trace labels for the high-level policy, we leverage available 3D bounding box annotations to identify agents within the ego vehicle’s field of view. We then transform relevant attributes, such as velocity and position relative to the ego vehicle, into structured natural language descriptions (e.g., “Red car, in one lane to the left, traveling same direction, at 6.1 m/s.”). 

We synchronize the high- and low-level policies by querying them at the same frequency. At each step, the low-level policy waits for the high-level to generate a meta-action, which it then uses as language input to produce driving actions. Specifically, we query the framework at 20 Hz in the CARLA simulator. 

## **5. Experimental Results** 

Our experiments are designed to address the following key research questions: 

- **RQ1:** How does SteerVLA perform in simulated closedloop driving under diverse traffic conditions, particularly in long-tail scenarios? 

- **RQ2:** How effectively does SteerVLA reason about complex scenes and follow driving instructions (i.e., meta-actions)? 

- **RQ3:** How effective is each component in SteerVLA? 

- **RQ4:** Can SteerVLA generalize to real-world driving data? 

|**Method**|**Architecture**|**Language Labels**|**Driving**<br>**Score** <sup>_↑_</sup>|
|---|---|---|---|
|SimLingo|VLA|Meta-actions|85.94|
|SteerVLA|VLM-VLA|Meta-actions|88.81|
|SteerVLA|VLM-VLA|Refined meta-actions<br>+ Reasoning traces|**90.71**|


_Table 1._ **Ablation study of SteerVLA components on Bench2Drive.** Our results show that SteerVLA benefits substantially from grounded semantic reasoning and fine-grained metaactions produced by a high-level policy that effectively steers low-level control. This is enabled by our data labeling pipeline, which aligns fine-grained meta-action and reasoning supervision with low-level control signals extracted from driving trajectories. 

closed-loop evaluation is conducted entirely in simulation, we do not optimize inference efficiency in this work. For real-world deployment, we plan to reduce inference latency using standard acceleration techniques, such as KV caching, in future work. 

**Evaluation metrics.** We evaluate closed-loop performance using the driving score, following the official CARLA metric. Driving score jointly measures task completion and safety by combining route completion with penalties for traffic infractions. Specifically, for each route, the route completion percentage is multiplied by penalties corresponding to the severity of infractions incurred. This metric captures both driving progress and robustness to safety violations. 

### **5.1. Experimental Setup** 

The majority of our experiments use the CARLA simulator to perform large-scale closed-loop evaluation of SteerVLA under diverse driving conditions. We evaluate SteerVLA on the Bench2Drive (Jia et al., 2024) benchmark, which contains 220 driving scenarios in 12 towns, including adverse weather and lighting conditions, such as fog, nighttime driving, and various long-tail driving scenarios, such as construction sites, traffic accidents ahead, and jaywalking pedestrians. We also construct a benchmark Bench2Drive-LongTail consisting of a long-tail scenario subset from Bench2Drive, described in Section 5.2 with additional detail in Section C.2, to further study the performance of SteerVLA on long-tail scenarios. 

**Training dataset.** We use the driving trajectories and meta-action labels from the SimLingo (Renz et al., 2025) dataset, and further apply our data augmentation pipeline to generate reasoning traces and refine the meta-actions into more fine-grained descriptions. We train both the high- and low-level policies on this dataset. 

**Policy deployment.** We run SteerVLA at 20 Hz in the CARLA simulator. On a single NVIDIA L40 GPU, SteerVLA incurs an inference latency of 2.51 s. As our 

**Baselines.** We evaluate several recent vision-languageaction (VLA) baselines. Full descriptions of these methods are provided in Section C.1. We compare SteerVLA to SimLingo (Renz et al., 2025), the current top method on the CARLA 2.0 Leaderboard trained with counterfactual data to improve language following, DriveMoE (Yang et al., 2025), a mixture-of-experts method, an alternative to the hierarchical structure we introduce, ORION (Fu et al., 2025), an end-to-end method that focuses on long-term history aggregation and improves driving reasoning with questionanswering as a co-training task rather than keeping a distinct high-level policy to maintain reasoning capabilities, and AutoVLA (Zhou et al., 2025c), which uses a pretrained VLM with a physical action codebook. These methods present alternative methods to retain reasoning capabilities or improve reasoning for driving tasks from a pretrained VLM. 

### **5.2. Evaluating SteerVLA on Driving Performance** 

Towards answering **Q1** , we evaluate SteerVLA closed-loop on the Bench2Drive benchmark. We additionally extract a subset of routes from Bench2Drive to observe the long-tail reasoning capabilities of SteerVLA and its ability to act appropriately in these scenarios. Results are shown in Fig. 3 

6 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 


_Figure 3._ **Closed-loop evaluation of SteerVLA on Bench2Drive.** On Bench2Drive, we report overall performance and per-ability scores for SteerVLA across five advanced urban driving skills. SteerVLA significantly outperforms prior approaches, benefiting from improved reasoning and instruction-following capabilities. 

_Figure 4._ **Closed-loop evaluation of SteerVLA on Bench2Drive-LongTail.** We compare SteerVLA with the state-of-the-art method SimLingo on Bench2Drive-LongTail. SteerVLA exhibits larger performance gains in long-tail scenarios, likely because these cases require more complex reasoning and more precise control. 

and in Fig. 4 with a detailed table of results in Section C.3. We also include discussion on failure cases in Section C.4. 

**Driving performance on Bench2Drive.** Fig. 3 demonstrates that SteerVLA has strong performance on the Bench2Drive benchmark, achieving a better driving score than the next best baseline, SimLingo, by 4.77, and outperforms it in all ability categories, except merging. We observe that SteerVLA tends to outperform SimLingo in highly dynamic scenarios (i.e., merging into the oncoming lane around a construction zone, or navigating an accident on the road). SteerVLA’s reasoning trace structure guides the policy to make conjectures about the movement intent of the other agents within the scene, enabling SteerVLA to prepare and preemptively react to adversarial behavior. This is also made apparent through the case study presented in Fig. 5. 

**Driving performance in long-tail scenarios.** On Bench2Drive-LongTail, SteerVLA shows clear advantages over the strongest baseline, SimLingo. Fig. 4 demonstrates that SteerVLA, on average, outperforms SimLingo by 8.04 in driving score, with especially large deltas in the construction zone, traffic accident, and blocked intersection scenarios. Long-tail scenarios demand rich semantic reasoning and precise control. In these scenes, inferences about out-of-distribution objects and the behavior of other agents must be carefully interpreted to navigate the changes in traffic flow from typical scenarios. SteerVLA is able to address this by explicitly reasoning about the states of other agents and traffic signs, resulting in detailed meta-actions that can 

guide VLA to cautiously but decisively act when it is safe to do so. 

### **5.3. Case Study in Long-Tail Scenarios** 

Towards answering **Q2** , we perform case studies of SteerVLA on challenging long-tail scenarios to observe its reasoning and instruction following capabilities, shown in Fig. 5. We first compare SteerVLA’s high-level policy reasoning to Gemini 2.5 Flash Lite, the same VLM we use in our autolabeling pipeline. In Fig. 5a, when faced with a construction site blocking a lane, while the off-the-shelf VLM can roughly reason about the scene state, it struggles to reason about the immediate actions the ego-vehicle should take. In contrast, SteerVLA produces both descriptive reasoning and aptly generates a meta-action to navigate around the construction site. Comparing to SimLingo in Fig. 5b, we observe that the detailed reasoning traces and meta-actions used to train SteerVLA enable more dynamic, informationrich reasoning and timely decision-making. When a nearby vehicle does not decelerate during a lane change, SteerVLA generates appropriate meta-actions by reasoning about other agents and traffic conditions, while SimLingo fails to react in time and collides. Furthermore, in Fig. 5c, when both methods correctly output a deceleration meta-action to follow a blocking vehicle, SteerVLA executes immediately while SimLingo’s delayed response leads to a collision. Overall, these case studies demonstrate that the reasoning traces and meta-actions of SteerVLA enable state-of-the-art long-tail scenario performance through superior environ- 

7 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 


_(a)_ **Comparison of SteerVLA with off-the-shelf VLM in reasoning capability.** We compare the reasoning capability in SteerVLA high-level policy with Gemini 2.5 Flash Lite (prompting details in Section B.4). When faced with a long-tail scenario, the off-the-shelf VLM (left) can roughly reason about the state of the scene but struggles to reason about the immediate actions the ego-vehicle should take under current conditions. Conversely, SteerVLA (right) produces both descriptive reasoning and can aptly generate a meta-action to navigate around the construction site. 


_(b)_ **Comparison of SteerVLA with SimLingo in reasoning capability.** The detailed reasoning traces and meta-actions used to train SteerVLA enable flexible environmental inference and timely decision-making when a nearby vehicle does not decelerate to give way during a lane change, whereas SimLingo fails to generate timely meta-actions and collides with another vehicle. 


_(c)_ **Comparison of SteerVLA with SimLingo in instruction following capability.** After turning right into a new lane where the vehicle ahead blocks the path, both methods output the meta-action decelerate to follow the blue vehicle. SteerVLA decelerates immediately, while SimLingo’s delayed deceleration leads to a collision. Green points show predicted future waypoints sampled at 4 Hz. 

_Figure 5._ **Long-tail scenario case study.** We analyze how SteerVLA reasons and acts in long-tail driving scenarios. In **(a)** , we compare SteerVLA with an off-the-shelf VLM, showing that SteerVLA produces both descriptive reasoning and actionable meta-actions. In **(b)** , we compare SteerVLA with SimLingo in a lane-change interaction where an adjacent vehicle does not give way, highlighting SteerVLA’s ability to make timely high-level decisions. In **(c)** , we evaluate instruction-following behavior when the lane ahead is blocked, where SteerVLA executes the deceleration meta-action immediately while SimLingo exhibits delayed control. 

8 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 

mental reasoning and precise action timing. 

### **5.4. Ablations of SteerVLA** 

Towards answering **Q3** , we study the effectiveness of two key design choices in SteerVLA on Bench2Drive: the VLMVLA style architecture and the reasoning components (i.e. fine-grained meta-actions and reasoning traces). We evaluate the effectiveness of a hierarchical architecture by comparing SteerVLA with SimLingo under the same meta-action supervision from the SimLingo dataset. We assess the impact of fine-grained meta-actions and reasoning traces by comparing SteerVLA trained with refined language labels generated by our data labeling pipeline against training with the original meta-action labels from SimLingo. The results in Table 1 show that SteerVLA benefits substantially from grounded semantic reasoning and fine-grained meta-actions produced by the high-level policy that effectively steer lowlevel control. This is enabled by our data labeling pipeline, which aligns fine-grained meta-action and reasoning supervision with low-level control signals extracted from driving trajectories. 

beling pipeline. As a result, SteerVLA can reason over complex driving scenarios and produce precise control outputs, achieving state-of-the-art performance in both general and long-tail driving settings. 

While SteerVLA demonstrates improved reasoning and steerability, it has several limitations that point to important future directions. The quality of our auto-labeling pipeline is constrained by the capabilities of the underlying VLM, particularly for temporally grounded understanding in video contexts. Our current system also uses only a single camera view, limiting scene coverage; extending to multi-view camera inputs would enhance spatial awareness and better match real-world autonomous vehicle sensor configurations. 

Overall, we hope that our work represents a step toward real-world systems that can use common sense to deal with complex and unfamiliar situations. We expect that the capabilities of VLMs and other foundation models will continue to improve, providing better multi-modal reasoning in diverse scenarios, and grounding these capabilities in real-world actions would allow for increasingly robust autonomous systems. SteerVLA represents a step toward this future. 

### **5.5. Open-Loop Evaluation on Real-World Data** 

Towards answering Q4, we additionally evaluate SteerVLA in an open-loop setting on the NuScenes benchmark (Caesar et al., 2020), using stronger VLM backbones—Gemma34B (Team et al., 2025) as the high-level policy and PaliGemma-3B (Beyer et al., 2024) as the low-level policy. We adopt more powerful pretrained VLMs for this evaluation, as real-world driving scenarios require stronger visual semantic generalization and benefit from richer prior knowledge learned from large-scale real-image data. Besides, since NuScenes does not provide language annotations, we apply our auto-labeling pipeline to generate grounded metaactions and reasoning traces directly from raw driving data. We emphasize that our primary evaluation focuses on closedloop results on Bench2Drive, which provide a more meaningful assessment by capturing control dynamics, recovery behavior, and long-horizon interactions with the environment, whereas open-loop evaluation on NuScenes measures trajectory imitation on fixed data. SteerVLA achieves comparable performance to existing methods on the NuScenes benchmark. Detailed experimental settings and results on NuScenes are provided in Section C.5. 

## **Acknowledgements** 

We thank Yuejiang Liu, Anikait Singh, William Chen, Priya Sundaresan, Joey Hejna, and others in the Stanford IRIS Lab, the Berkeley RAIL Lab, and the Stanford ILIAD Lab for helpful discussions. We thank Google Cloud for providing TPU resources and credits. This research was partly supported by Volkswagen, an NSF CAREER Award, ARL DCIST CRA W911NF-17-2-0181, DARPA TIAMAT, AFOSR FA9550-22-1-0273, and NSF Grant #1941722. 

## **References** 

- Arai, H., Miwa, K., Sasaki, K., Watanabe, K., Yamaguchi, Y., Aoki, S., and Yamamoto, I. Covla: Comprehensive vision-language-action dataset for autonomous driving. In _2025 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)_ , pp. 1933–1943. IEEE, 2025. 

- Belkhale, S., Ding, T., Xiao, T., Sermanet, P., Vuong, Q., Tompson, J., Chebotar, Y., Dwibedi, D., and Sadigh, D. Rt-h: Action hierarchies using language, 2024. URL https://arxiv.org/abs/2403.01823. 

## **6. Discussion** 

We presented SteerVLA, a hierarchical VLA model for autonomous driving. Our approach decomposes driving into a high-level, language-based reasoning step and a low-level action generation step, with detailed meta-actions serving as the interface between the two. These meta-actions are generated from driving data through a fully automatic la- 

- Beyer, L., Steiner, A., Pinto, A. S., Kolesnikov, A., Wang, X., Salz, D., Neumann, M., Alabdulmohsin, I., Tschannen, M., Bugliarello, E., Unterthiner, T., Keysers, D., Koppula, S., Liu, F., Grycner, A., Gritsenko, A., Houlsby, N., Kumar, M., Rong, K., Eisenschlos, J., Kabra, R., Bauer, M., Bosnjak, M., Chen, X., Minderer, M., Voigt-ˇ laender, P., Bica, I., Balazevic, I., Puigcerver, J., Papalam- 

9 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 

- pidi, P., Henaff, O., Xiong, X., Soricut, R., Harmsen, J., and Zhai, X. Paligemma: A versatile 3b vlm for transfer, 2024. URL https://arxiv.org/abs/2407. 07726. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., Levine, S., LiBell, A., Mothukuri, M., Nair, S., Pertsch, K., Shi, L. X., Tanner, J., Vuong, Q., Walling, A., Wang, H., and Zhilinsky, U. _π_ 0: A vision-language-action flow model for general robot control, 2024. URL https: //arxiv.org/abs/2410.24164. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Chen, X., Choromanski, K., Ding, T., Driess, D., Dubey, A., Finn, C., Florence, P., Fu, C., Arenas, M. G., Gopalakrishnan, K., Han, K., Hausman, K., Herzog, A., Hsu, J., Ichter, B., Irpan, A., Joshi, N., Julian, R., Kalashnikov, D., Kuang, Y., Leal, I., Lee, L., Lee, T.-W. E., Levine, S., Lu, Y., Michalewski, H., Mordatch, I., Pertsch, K., Rao, K., Reymann, K., Ryoo, M., Salazar, G., Sanketi, P., Sermanet, P., Singh, J., Singh, A., Soricut, R., Tran, H., Vanhoucke, V., Vuong, Q., Wahid, A., Welker, S., Wohlhart, P., Wu, J., Xia, F., Xiao, T., Xu, P., Xu, S., Yu, T., and Zitkovich, B. Rt-2: Vision-language-action models transfer web knowledge to robotic control, 2023a. URL https://arxiv.org/abs/2307.15818. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Chen, X., Choromanski, K., Ding, T., Driess, D., Dubey, A., Finn, C., Florence, P., Fu, C., Arenas, M. G., Gopalakrishnan, K., Han, K., Hausman, K., Herzog, A., Hsu, J., Ichter, B., Irpan, A., Joshi, N., Julian, R., Kalashnikov, D., Kuang, Y., Leal, I., Lee, L., Lee, T.-W. E., Levine, S., Lu, Y., Michalewski, H., Mordatch, I., Pertsch, K., Rao, K., Reymann, K., Ryoo, M., Salazar, G., Sanketi, P., Sermanet, P., Singh, J., Singh, A., Soricut, R., Tran, H., Vanhoucke, V., Vuong, Q., Wahid, A., Welker, S., Wohlhart, P., Wu, J., Xia, F., Xiao, T., Xu, P., Xu, S., Yu, T., and Zitkovich, B. RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. _arXiv preprint arXiv:2307.15818_ , July 2023b. 

- Caesar, H., Bankiti, V., Lang, A. H., Vora, S., Liong, V. E., Xu, Q., Krishnan, A., Pan, Y., Baldan, G., and Beijbom, O. nuscenes: A multimodal dataset for autonomous driving. In _CVPR_ , 2020. 

- Chen, L., Sinavski, O., H¨unermann, J., Karnsund, A., Willmott, A. J., Birch, D., Maund, D., and Shotton, J. Driving with llms: Fusing object-level vector modality for explainable autonomous driving. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 14093–14100. IEEE, 2024a. 

- Chen, W., Belkhale, S., Mirchandani, S., Mees, O., Driess, D., Pertsch, K., and Levine, S. Training strategies for efficient embodied reasoning. In _Conference on Robot Learning_ , 2025. 

- Chen, Z., Wu, J., Wang, W., Su, W., Chen, G., Xing, S., Zhong, M., Zhang, Q., Zhu, X., Lu, L., et al. Internvl: Scaling up vision foundation models and aligning for generic visual-linguistic tasks. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 24185–24198, 2024b. 

- Deruyttere, T., Vandenhende, S., Grujicic, D., Van Gool, L., and Moens, M.-F. Talk2car: Taking control of your self-driving car. In _Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)_ . Association for Computational Linguistics, 2019. doi: 10.18653/v1/d19-1215. URL http://dx.doi.org/ 10.18653/v1/D19-1215. 

- Dosovitskiy, A., Ros, G., Codevilla, F., Lopez, A., and Koltun, V. Carla: An open urban driving simulator, 2017. URL https://arxiv.org/abs/1711.03938. 

- Driess, D., Springenberg, J. T., Ichter, B., Yu, L., Li-Bell, A., Pertsch, K., Ren, A. Z., Walke, H., Vuong, Q., Shi, L. X., and Levine, S. Knowledge insulating vision-languageaction models: Train fast, run fast, generalize better, 2025. URL https://arxiv.org/abs/2505.23705. 

- Feng, L. and Alahi, A. Uniplan: A unified end-to-end planning framework for the 2025 waymo open dataset e2e driving challenge. Technical report, EPFL, 2025. Technical Report, 3rd place solution at the 2025 WOD E2E Driving Challenge. 

- Fu, H., Zhang, D., Zhao, Z., Cui, J., Liang, D., Zhang, C., Zhang, D., Xie, H., Wang, B., and Bai, X. Orion: A holistic end-to-end autonomous driving framework by visionlanguage instructed action generation. _arXiv preprint arXiv:2503.19755_ , 2025. 

- Gao, X., Wu, Y., Wang, R., Liu, C., Zhou, Y., and Tu, Z. Langcoop: Collaborative driving with language. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 4226–4237, 2025. 

- He, Y. and Shi, W. Carscenes: Semantic vlm dataset for safe autonomous driving, 2025. URL https://arxiv. org/abs/2511.10701. 

- Hegde, D., Yasarla, R., Cai, H., Han, S., Bhattacharyya, A., Mahajan, S., Liu, L., Garrepalli, R., Patel, V. M., and Porikli, F. Distilling multi-modal large language models for autonomous driving, 2025. URL https: //arxiv.org/abs/2501.09757. 

10 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 

- Hu, Y., Yang, J., Chen, L., Li, K., Sima, C., Zhu, X., Chai, S., Du, S., Lin, T., Wang, W., Lu, L., Jia, X., Liu, Q., Dai, J., Qiao, Y., and Li, H. Planning-oriented autonomous driving, 2023. URL https://arxiv.org/abs/2212. 10156. 

- Huang, J., Xie, S., Sun, J., Ma, Q., Liu, C., Lin, D., and Zhou, B. Learning a decision module by imitating driver’s control behaviors. In _Conference on Robot Learning_ , pp. 1–10. PMLR, 2021. 

- Hwang, J.-J., Xu, R., Lin, H., Hung, W.-C., Ji, J., Choi, K., Huang, D., He, T., Covington, P., Sapp, B., Zhou, Y., Guo, J., Anguelov, D., and Tan, M. EMMA: End-toEnd Multimodal Model for Autonomous Driving. _arXiv preprint arXiv:2410.23262_ , November 2024a. 

- Hwang, J.-J., Xu, R., Lin, H., Hung, W.-C., Ji, J., Choi, K., Huang, D., He, T., Covington, P., Sapp, B., et al. Emma: End-to-end multimodal model for autonomous driving. _arXiv preprint arXiv:2410.23262_ , 2024b. 

- Inoue, Y., Yada, Y., Tanahashi, K., and Yamaguchi, Y. Nuscenes-mqa: Integrated evaluation of captions and qa for autonomous driving datasets using markup annotations, 2023. URL https://arxiv.org/abs/ 2312.06352. 

- Jia, F., Mao, W., Liu, Y., Zhao, Y., Wen, Y., Zhang, C., Zhang, X., and Wang, T. Adriver-i: A general world model for autonomous driving. _arXiv preprint arXiv:2311.13549_ , 2023. 

- Jia, X., Yang, Z., Li, Q., Zhang, Z., and Yan, J. Bench2drive: Towards multi-ability benchmarking of closed-loop endto-end autonomous driving, 2024. URL https:// arxiv.org/abs/2406.03877. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E. P., Sanketi, P. R., Vuong, Q., Kollar, T., Burchfiel, B., Tedrake, R., Sadigh, D., Levine, S., Liang, P., and Finn, C. OpenVLA: An Open-Source Vision-Language-Action Model. In _8th Annual Conference on Robot Learning_ , September 2024. 

- Liu, Y., Wang, S., Wei, D., Cai, X., Zhong, L., Yang, J., Ren, G., Zhang, J., Yao, M., Li, C., He, X., Chen, L., and Luo, J. Unified embodied vlm reasoning with robotic action via autoregressive discretized pre-training, 2026. URL https://arxiv.org/abs/2512.24125. 

- Luo, Y., Li, F., Xu, S., Lai, Z., Yang, L., Chen, Q., Luo, Z., Xie, Z., Jiang, S., Liu, J., Chen, L., Wang, B., and xin Yang, Z. Adathinkdrive: Adaptive thinking via reinforcement learning for autonomous driving, 2025. URL https://arxiv.org/abs/2509.13769. 

- Malla, S., Choi, C., Dwivedi, I., Choi, J. H., and Li, J. Drama: Joint risk localization and captioning in driving, 2022. URL https://arxiv.org/abs/2209. 10767. 

- Mao, J., Qian, Y., Ye, J., Zhao, H., and Wang, Y. Gptdriver: Learning to drive with gpt. _arXiv preprint arXiv:2310.01415_ , 2023a. 

- Mao, J., Ye, J., Qian, Y., Pavone, M., and Wang, Y. A language agent for autonomous driving. _arXiv preprint arXiv:2311.10813_ , 2023b. 

- Mu, Y., Zhang, Q., Hu, M., Wang, W., Ding, M., Jin, J., Wang, B., Dai, J., Qiao, Y., and Luo, P. Embodiedgpt: Vision-language pre-training via embodied chain of thought, 2023. URL https://arxiv.org/abs/ 2305.15021. 

- Nguyen, L., Fauth, M., Jaeger, B., Dauner, D., Igl, M., Geiger, A., and Chitta, K. Open x-av: Unifying end-toend autonomous driving datasets. In _CVPR Workshops 2025_ , 2025. URL https://research.nvidia. com/labs/avg/publication/nguyen.fauth. etal.cvprw2025/. CVPRW workshop version. 

- Octo Model Team, Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Xu, C., Luo, J., Kreiman, T., Tan, Y., Sanketi, P., Vuong, Q., Xiao, T., Sadigh, D., Finn, C., and Levine, S. Octo: An opensource generalist robot policy. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, 2024. 

- Qian, K., Jiang, S., Zhong, Y., Luo, Z., Huang, Z., Zhu, T., Jiang, K., Yang, M., Fu, Z., Miao, J., et al. Agentthink: A unified framework for tool-augmented chain-of-thought reasoning in vision-language models for autonomous driving. _arXiv preprint arXiv:2505.15298_ , 2025. 

- Qwen, :, Yang, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B., Li, C., Liu, D., Huang, F., Wei, H., Lin, H., Yang, J., Tu, J., Zhang, J., Yang, J., Yang, J., Zhou, J., Lin, J., Dang, K., Lu, K., Bao, K., Yang, K., Yu, L., Li, M., Xue, M., Zhang, P., Zhu, Q., Men, R., Lin, R., Li, T., Tang, T., Xia, T., Ren, X., Ren, X., Fan, Y., Su, Y., Zhang, Y., Wan, Y., Liu, Y., Cui, Z., Zhang, Z., and Qiu, Z. Qwen2.5 technical report, 2025. URL https: //arxiv.org/abs/2412.15115. 

- Renz, K., Chen, L., Arani, E., and Sinavski, O. Simlingo: Vision-only closed-loop autonomous driving with language-action alignment, 2025. URL https:// arxiv.org/abs/2503.09594. 

- Shao, H., Hu, Y., Wang, L., Song, G., Waslander, S. L., Liu, Y., and Li, H. Lmdrive: Closed-loop end-to-end driving with large language models. In _Proceedings of the_ 

11 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 

- _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 15120–15130, 2024. 

- Shi, L. X., Hu, Z., Zhao, T. Z., Sharma, A., Pertsch, K., Luo, J., Levine, S., and Finn, C. Yell at your robot: Improving on-the-fly from language corrections. _arXiv preprint arXiv: 2403.12910_ , 2024. 

- Sima, C., Renz, K., Chitta, K., Chen, L., Zhang, H., Xie, C., Beißwenger, J., Luo, P., Geiger, A., and Li, H. DriveLM: Driving with Graph Visual Question Answering. In Leonardis, A., Ricci, E., Roth, S., Russakovsky, O., Sattler, T., and Varol, G. (eds.), _Computer Vision – ECCV 2024_ , pp. 256–274, Cham, 2024. Springer Nature Switzerland. ISBN 978-3-031-72943-0. 

- Sun, J., Sun, H., Han, T., and Zhou, B. Neuro-symbolic program search for autonomous driving decision module design. In _Conference on Robot Learning_ , pp. 21–30. PMLR, 2021. 

- Tan, R., Peng, B., Yang, Z., Cheng, H., Mees, O., Zhao, T., Tupini, A., Meijer, I., Wu, Q., Yang, Y., Liden, L., Gu, Y., Zhang, S., Liu, X., Wang, L., Pollefeys, M., Lee, Y. J., and Gao, J. Multimodal reinforcement learning with agentic verifier for ai agents. _arXiv preprint arXiv:2512.03438_ , 2025. 

- Team, G. Gemini: A family of highly capable multimodal models, 2025. 

- Team, G., Kamath, A., Ferret, J., Pathak, S., Vieillard, N., Merhej, R., Perrin, S., Matejovicova, T., Rame, A.,´ Riviere,` M., Rouillard, L., Mesnard, T., Cideron, G., bastien Grill, J., Ramos, S., Yvinec, E., Casbon, M., Pot, E., Penchev, I., Liu, G., Visin, F., Kenealy, K., Beyer, L., Zhai, X., Tsitsulin, A., Busa-Fekete, R., Feng, A., Sachdeva, N., Coleman, B., Gao, Y., Mustafa, B., Barr, I., Parisotto, E., Tian, D., Eyal, M., Cherry, C., Peter, J.-T., Sinopalnikov, D., Bhupatiraju, S., Agarwal, R., Kazemi, M., Malkin, D., Kumar, R., Vilar, D., Brusilovsky, I., Luo, J., Steiner, A., Friesen, A., Sharma, A., Sharma, A., Gilady, A. M., Goedeckemeyer, A., Saade, A., Feng, A., Kolesnikov, A., Bendebury, A., Abdagic, A., Vadi, A., Gyorgy, A., Pinto, A. S., Das, A., Bapna, A., Miech,¨ A., Yang, A., Paterson, A., Shenoy, A., Chakrabarti, A., Piot, B., Wu, B., Shahriari, B., Petrini, B., Chen, C., Lan, C. L., Choquette-Choo, C. A., Carey, C., Brick, C., Deutsch, D., Eisenbud, D., Cattle, D., Cheng, D., Paparas, D., Sreepathihalli, D. S., Reid, D., Tran, D., Zelle, D., Noland, E., Huizenga, E., Kharitonov, E., Liu, F., Amirkhanyan, G., Cameron, G., Hashemi, H., Klimczak-Plucinska,´ H., Singh, H., Mehta, H., Lehri, H. T., Hazimeh, H., Ballantyne, I., Szpektor, I., Nardini, I., Pouget-Abadie, J., Chan, J., Stanton, J., Wieting, J., Lai, J., Orbay, J., Fernandez, J., Newlan, J., yeong Ji, 

J., Singh, J., Black, K., Yu, K., Hui, K., Vodrahalli, K., Greff, K., Qiu, L., Valentine, M., Coelho, M., Ritter, M., Hoffman, M., Watson, M., Chaturvedi, M., Moynihan, M., Ma, M., Babar, N., Noy, N., Byrd, N., Roy, N., Momchev, N., Chauhan, N., Sachdeva, N., Bunyan, O., Botarda, P., Caron, P., Rubenstein, P. K., Culliton, P., Schmid, P., Sessa, P. G., Xu, P., Stanczyk, P., Tafti, P., Shivanna, R., Wu, R., Pan, R., Rokni, R., Willoughby, R., Vallu, R., Mullins, R., Jerome, S., Smoot, S., Girgin, S., Iqbal, S., Reddy, S., Sheth, S., Poder,˜ S., Bhatnagar, S., Panyam, S. R., Eiger, S., Zhang, S., Liu, T., Yacovone, T., Liechty, T., Kalra, U., Evci, U., Misra, V., Roseberry, V., Feinberg, V., Kolesnikov, V., Han, W., Kwon, W., Chen, X., Chow, Y., Zhu, Y., Wei, Z., Egyed, Z., Cotruta, V., Giang, M., Kirk, P., Rao, A., Black, K., Babar, N., Lo, J., Moreira, E., Martins, L. G., Sanseviero, O., Gonzalez, L., Gleicher, Z., Warkentin, T., Mirrokni, V., Senter, E., Collins, E., Barral, J., Ghahramani, Z., Hadsell, R., Matias, Y., Sculley, D., Petrov, S., Fiedel, N., Shazeer, N., Vinyals, O., Dean, J., Hassabis, D., Kavukcuoglu, K., Farabet, C., Buchatskaya, E., Alayrac, J.-B., Anil, R., Dmitry, Lepikhin, Borgeaud, S., Bachem, O., Joulin, A., Andreev, A., Hardin, C., Dadashi, R., and Hussenot, L. Gemma 3 technical report, 2025. URL https://arxiv.org/abs/2503.19786. 

- Tian, R., Li, B., Weng, X., Chen, Y., Schmerling, E., Wang, Y., Ivanovic, B., and Pavone, M. Tokenize the world into object-level knowledge to address long-tail events in autonomous driving. In _CoRL_ , Proceedings of Machine Learning Research, 2024. 

- Wang, W., Xie, J., Hu, C., Zou, H., Fan, J., Tong, W., Wen, Y., Wu, S., Deng, H., Li, Z., et al. Drivemlm: Aligning multi-modal large language models with behavioral planning states for autonomous driving. _arXiv preprint arXiv:2312.09245_ , 2023. 

- Wang, Z., Yu, T., and Tang, H. Cot4ad: A vision-languageaction model with explicit chain-of-thought reasoning for autonomous driving, 2025. URL https://arxiv. org/abs/2511.22532. 

- Weng, X., Ivanovic, B., Wang, Y., Wang, Y., and Pavone, M. Para-drive: Parallelized architecture for real-time autonomous driving. In _2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 15449–15458, 2024. doi: 10.1109/CVPR52733.2024. 01463. 

- Wu, D., Han, W., Liu, Y., Wang, T., zhong Xu, C., Zhang, X., and Shen, J. Language prompt for autonomous driving, 2025. URL https://arxiv.org/abs/2309. 04379. 

- Xu, Y., Yang, X., Gong, L., Lin, H.-C., Wu, T.-Y., Li, Y., and Vasconcelos, N. Explainable object-induced action 

12 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 

- decision for autonomous vehicles. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 9523–9532, 2020. 

- Xu, Z., Zhang, Y., Xie, E., Zhao, Z., Guo, Y., Wong, K.-Y. K., Li, Z., and Zhao, H. Drivegpt4: Interpretable end-to-end autonomous driving via large language model, 2024. URL https://arxiv.org/ abs/2310.01412. 

   - Zhou, Z., Cai, T., Zhao, S. Z., Zhang, Y., Huang, Z., Zhou, B., and Ma, J. Autovla: A vision-language-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning. _arXiv preprint arXiv:2506.13757_ , 2025c. 

- Yang, Z., Chai, Y., Jia, X., Li, Q., Shao, Y., Zhu, X., Su, H., and Yan, J. Drivemoe: Mixture-of-experts for visionlanguage-action model in end-to-end autonomous driving, 2025. URL https://arxiv.org/abs/2505. 16278. 

- Ye, A., Zhang, Z., Wang, B., Wang, X., Zhang, D., and Zhu, Z. Vla-r1: Enhancing reasoning in vision-languageaction models, 2025. URL https://arxiv.org/ abs/2510.01623. 

- Yuan, J., Sun, S., Omeiza, D., Zhao, B., Newman, P., Kunze, L., and Gadd, M. Rag-driver: Generalisable driving explanations with retrieval-augmented in-context learning in multi-modal large language model. _arXiv preprint arXiv:2402.10828_ , 2024. 

- Zawalski, M., Chen, W., Pertsch, K., Mees, O., Finn, C., and Levine, S. Robotic control via embodied chain-ofthought reasoning. In _Conference on Robot Learning_ , 2024. 

- Zhao, Q., Lu, Y., Kim, M. J., Fu, Z., Zhang, Z., Wu, Y., Li, Z., Ma, Q., Han, S., Finn, C., Handa, A., Liu, M.Y., Xiang, D., Wetzstein, G., and Lin, T.-Y. Cot-vla: Visual chain-of-thought reasoning for vision-languageaction models, 2025. URL https://arxiv.org/ abs/2503.22020. 

- Zhao, T. Z., Kumar, V., Levine, S., and Finn, C. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 

- Zheng, Y., Liang, R., Zheng, K., Zheng, J., Mao, L., Li, J., Gu, W., Ai, R., Li, S. E., Zhan, X., and Liu, J. Diffusionbased planning for autonomous driving with flexible guidance, 2025. URL https://arxiv.org/abs/ 2501.15564. 

- Zhou, X., Han, X., Yang, F., Ma, Y., and Knoll, A. C. Opendrivevla: Towards end-to-end autonomous driving with large vision language action model. _arXiv preprint arXiv:2503.23463_ , 2025a. 

- Zhou, X., Han, X., Yang, F., Ma, Y., and Knoll, A. C. OpenDriveVLA: Towards End-to-end Autonomous Driving with Large Vision Language Action Model. _arXiv preprint arXiv:2503.23463_ , March 2025b. 

13 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 

## **A. Training Details** 

### **A.1. Model Architecture** 

While our method is applicable to any VLM backbone, we use InternVL2-1B (Chen et al., 2024b) for both the high-level and low-level policies in our closed-loop experiments. InternVL2-1B is based on Qwen2.5-0.5B-Instruct (Qwen et al., 2025) and uses InternViT-300M-448px as its vision encoder. Following the design in (Renz et al., 2025), our low-level policy employs two additional MLP heads for future waypoint prediction. We fine-tune the language model with LoRA and apply full fine-tuning to all remaining parameters. 

### **A.2. Training Hyperparameters** 

Hyperparameters are shown in Table 2. 

|**High-Level Pol**|**icy**|**Low-Level Pol**|**icy**|
|---|---|---|---|
|**Hyperparameter**|**Value**|**Hyperparameter**|**Value**|
|Batch Size|96|Batch Size|120|
|Gradient Accumulation Steps|2|Gradient Accumulation Steps|1|
|Epochs|20|Epochs|30|
|Learning Rate|3_×_10<sup>_−_5</sup>|Learning Rate|3_×_10<sup>_−_5</sup>|
|Learning Rate Scheduler|Cosine Decay|Learning Rate Scheduler|Cosine Decay|
|Betas|(0_._9_,_0_._999)|Betas|(0_._9_,_0_._999)|
|Optimizer|AdamW|Optimizer|AdamW|
|Warmup steps|5% of total steps|Warmup steps|5% of total steps|
|LoRA alpha|64|LoRA alpha|64|
|LoRA r|32|LoRA r|32|
|LoRA dropout|0_._1|LoRA dropout|0_._1|


_Table 2._ **Training Hyperparameters.** 

### **A.3. Training and Inference Hardware** 

We trained our high-level policy on 8 NVIDIA H100 GPUs for 15 hours and our low-level policy on 4 NVIDIA H200 GPUs for 20 hours. Inference was performed on a single NVIDIA L40 GPU. 

## **B. Auto-Labeling Pipeline Details** 

### **B.1. Label Refinement on SimLingo dataset** 

In order to imbue language labels from language-annotated datasets, such as the SimLingo dataset, with detailed movement information as described in Section 4.2, we provide the vehicle’s ego states over a period of three seconds in addition to the original language label in a prompt (see Listing 1 for the full prompt) to Gemini 2.5 Flash-Lite. 

_Listing 1._ SimLingo Refinement Prompt. 

- <mark>You are an expert in vehicle dynamics and driving behavior analysis. Your task is to interpret and refine natural language descriptions of driving behavior by analyzing vehicle ego state data (speed and course over time) to produce a **precise and nuanced behavior summary**. Your output should describe:</mark> 

<mark>1. **Ego State Analysis** - a brief explanation of observed speed and course trends over time.</mark> 

<mark>2. **Refined Driving Behavior Description** - a more specific version of the original description, enhanced with a meaningful modifier _(e.g., **smooth turning**, **wide turn**, **abrupt stop**, **steady lane keeping**)_ and a **driving style**, reflecting the driver’s attitude or intent _(e.g., **cautiously**, **normally**, **aggressively</mark> 

<mark>**</mark><sup><mark>)_</mark></sup> 

14 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 

<mark>## Input Format **</mark><sup><mark>DrivingDescription:</mark></sup> <mark>** {commentary} **</mark><sup><mark>EgoVehicleStateSequence</mark></sup> <mark>**</mark><sup><mark>(next3secondsfromframe{frame_number}):</mark></sup> <mark>{ego_states_sequence} These ego states reflect how the vehicle moved during the described behavior. > **Note:** > - **Course increasing** -> vehicle is adjusting **right** > - **Course decreasing** -> vehicle is adjusting **left** ---</mark> 

<mark>## Output Guidelines Your response should contain two sections: ### 1. Ego State Analysis Analyze the speed and course sequence: - Describe speed patterns: Is the vehicle accelerating, decelerating, or maintaining speed ?</mark> 

- <mark>Describe course patterns: Is the vehicle turning sharply, smoothly, or going straight?</mark> 

- <mark>- Mention time duration and total changes in course or speed.</mark> 

<mark>### 2. Refined Driving Behavior Description</mark> 

<mark>Produce a single, natural-language sentence that:</mark> 

- <mark>Refines the driving description with motion extent (e.g., *smooth*, *sharp*, *wide*, * slight*)</mark> 

- <mark>Adds driving style (e.g., *cautiously*, *normally*, *aggressively*)</mark> 

- <mark>Grounds the refinement in the observable patterns of the ego vehicle states</mark> 

- <mark>Do not change the semantic meaning of the original description. Only use the ego states to refine the description.</mark> 

<mark>## Notes</mark> 

- <mark>The refined description must not exceed **20 words**.</mark> 

- <mark>Use **speed trends** to judge acceleration or deceleration patterns.</mark> 

- <mark>Use **course change patterns** to assess turning sharpness or trajectory smoothness.</mark> 

- <mark>If the style cannot be confidently inferred, default to **"normally"**.</mark> 

- <mark>Use **natural, human-readable language**-avoid unnecessary technical jargon.</mark> 

- <mark>The refined description must be a single sentence in present tense and third person (i.e . "The vehicle turns..." or "The car accelerates...")</mark> 

- <mark>If the driving description includes any references to external vehicles, pedestrians or traffic constructs, maintain this information in the final refined description, as well as their distances from the ego vehicle and any descriptiors (i.e. color) if available.</mark> 

- <mark>Do not change the semantic meaning of the original description. Only use the ego states to refine the description.</mark> 

- <mark>If the original description mentions specific maneuvers, i.e. lane changes, retain this information.</mark> 

- <mark>Unless a turn is explicitly mentioned in the original description, heading changes of 30 degrees or below should be described as **adjustments** to the left or right, and not turns.</mark> 

15 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 

### **B.2. NuScenes Meta-Action Labeling** 

Our auto-labeling pipeline is also applicable to real-world datasets without prior language labels. To apply our labeling pipeline to the NuScenes dataset, we begin by splitting trajectories into 2-5 second chunks based on a set of heuristics that define the boundaries of where a specific category of action (e.g., accelerating, changing lanes, or turning) is likely to have occurred. Specifically, we apply a 1D Gaussian blur to the vehicle’s speed and course changes over time, and apply splits where the vehicle is stopped, or the vehicle’s acceleration or angular velocity are above certain thresholds for an extended period of time. 

We then utilize the vehicle’s camera extrinsic and intrinsic matrices to produce a projection of the vehicle’s future trajectory over front camera views from the first and middle frames of the trajectory. These images, the vehicle’s ego states and lane IDs over time, and the prompt in Listing 2 are provided to Gemini 2.5 Flash-Lite for a baseline categorization stage. We show two examples in Fig. 6. 

_Listing 2._ Example Meta Action Labeling Prompt. 

<mark>You are an expert in vehicle dynamics and driving behavior analysis. You have been provided two frames from a dashcam video from a vehicle, with a projected green, yellow, and red trajectory overlaid on the first and middle frames of the video of the trajectory that the vehicle is in the process of taking. The images are labelled " First Frame" and "Middle Frame" at the tops of the images.</mark> 

<mark>Describe:</mark> 

<mark>1. Ego State Analysis:</mark> 

<mark>Analyze the speed and course sequence: - Describe speed patterns: Is the vehicle accelerating, decelerating, or maintaining speed ?</mark> 

- <mark>Describe course patterns: Is the vehicle turning sharply, smoothly, or going straight?</mark> 

- <mark>Mention time duration and total changes in course or speed.</mark> 

<mark>These ego states reflect how the vehicle moved during the described behavior.</mark> 

<mark>> **Note:** > - **Course increasing** -> vehicle is moving **right** > - **Course decreasing** -> vehicle is moving **left**</mark> 

<mark>{ego_states_text}</mark> 

<mark>2. First frame description:</mark> 

- <mark>Describe the lane markings in the first frame image, and the projected trajectory’s position relative to them at the beginning of the trajectory and at the end. Identify any areas on the road with solid white or yellow lines.</mark> 

- <mark>Are there road markings, signs, or other structures that indicate that the vehicle is at an intersection?</mark> 

- <mark>Which lane does the trajectory begin in, and which lane does the trajectory end in?</mark> 

- <mark>Is the red, yellow, and/or green trajectory to the right or left of the lane markings?</mark> 

- <mark>Is the cyan circle to the right or left of the lane markings?</mark> 

- <mark>Is the trajectory curving? If so, which way is the trajectory curving?</mark> 

<mark>3. Middle frame description:</mark> 

- <mark>Describe the lane markings in the middle frame image, and the projected trajectory’s position relative to them at the beginning of the trajectory and at the end. Identify any areas on the road with solid white or yellow lines.</mark> 

- <mark>Are there road markings, signs, or other structures that indicate that the vehicle is at an intersection?</mark> 

- <mark>Which lane does the trajectory begin in, and which lane does the trajectory end in?</mark> 

- <mark>Is the red, yellow, and/or green trajectory to the right or left of the lane markings?</mark> 

- <mark>Is the cyan circle to the right or left of the lane markings?</mark> 

- <mark>Is the trajectory curving? If so, which way is the trajectory curving?</mark> 

<mark>4. Consolidated Analysis:</mark> 

- <mark>Based on your analysis of the first frame image and the middle frame image, which lane</mark> 

16 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 

<mark>does the vehicle begin in, and which lane does it end in?</mark> 

- <mark>Does this signify a lane change? If so, is the vehicle making a lane change to the left, or a lane change to the right?</mark> 

- <mark>Alternatively, is the vehicle at an intersection in either frame? Does this signify a turn? Even if the trajectory is curving, consider whether the course change is large enough to be a turn, and whether the vehicle is simply continuing forward to a parallel road.</mark> 

- <mark>If so, is the vehicle turning to the left, or to the right?</mark> 

<mark>5. Vehicle Action: The action that the vehicle is taking. Is the vehicle **turning**, ** changing lanes**, or **continuing straight**? If the vehicle is turning or changing lanes, is it doing so to the **left** or to the **right**? Choose from one of the following discrete actions:</mark> 

- <mark>turning left</mark> 

- <mark>turning right</mark> 

- <mark>changing lanes left</mark> 

- <mark>changing lanes right</mark> 

- <mark>continuing straight</mark> 

- <mark>completely stationary</mark> 

- <mark>making a U-Turn</mark> 

<mark>Notes:</mark> 

- <mark>The cyan circle denotes the **end** of the trajectory.</mark> 

- <mark>The trajectory begins at the **bottom** of the image.</mark> 

- <mark>A turn is defined as a full turn at an intersection.</mark> 

- <mark>Otherwise, if the trajectory is simply following a curve in the road, describe this as **</mark><sup><mark>continuingstraight</mark></sup> <mark>**</mark> 

- <mark>If the trajectory is **continuing straight** through an intersection, describe this as **</mark><sup><mark>continuingstraight</mark></sup> <mark>**</mark> 

- <mark>If the vehicle has crossed a lane marking, it is most likely making a lane change.</mark> 

- <mark>There may be no visible trajectory projected, in which case the vehicle is most likely moving very slowly or stationary.</mark> 

- <mark>Identify only the lane markings that are clearly discernible.</mark> 

- <mark>Small course changes of fewer than 4 degrees most likely indicate that the vehicle is ** continuing forward**.</mark> 

- <mark>Large course changes over 50 degrees likely indicate that the vehicle is **turning**.</mark> 

- <mark>- Small velocities below 1.0 meters per second likely indicate that the vehicle is stationary.</mark> 

<mark>Lane information: {lane_information}</mark> 

We then provide the output of Listing 2, the vehicle’s ego states, and the prompt in Listing 3 to Gemini 2.5 Flash-Lite in a refinement step that imbues the resulting meta-action with more detailed movement information. 

_Listing 3._ Example Meta Action Labeling Prompt. 

<mark># Driving Behavior Refinement Prompt</mark> 

- <mark>You are an expert in vehicle dynamics and driving behavior analysis. Your task is to interpret and refine natural language descriptions of driving behavior by analyzing vehicle ego state data (speed and course over time) to produce a **precise and nuanced behavior summary**. Your output should describe:</mark> 

<mark>1. **Ego State Analysis** -> a brief explanation of observed speed and course trends over time.</mark> 

<mark>2. **Refined Driving Behavior Description** - a more specific version of the original description, enhanced with a meaningful modifier _(e.g., **smooth turning**, **wide turn**, **abrupt stop**, **steady lane keeping**)_ and a **driving style**, reflecting the driver’s attitude or intent _(e.g., **cautiously**, **normally**, **aggressively</mark> 

<mark>**</mark><sup><mark>)_</mark></sup> 

<mark>## Input Format</mark> 

17 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 

<mark>**</mark><sup><mark>DrivingDescription:</mark></sup> <mark>** {driving_description} **</mark><sup><mark>EgoVehicleStates:</mark></sup> <mark>** {ego_state_sequence}</mark> 

<mark>These ego states reflect how the vehicle moved during the described behavior.</mark> 

<mark>> **Note:** > - **Course increasing** -> vehicle is moving **right** > - **Course decreasing** -> vehicle is moving **left**</mark> 

<mark>## Output Guidelines</mark> 

<mark>Your response should contain two sections:</mark> 

<mark>### 1. Ego State Analysis</mark> 

<mark>Analyze the speed and course sequence:</mark> 

<mark>- Describe speed patterns: Is the vehicle accelerating, decelerating, or maintaining speed ?</mark> 

<mark>- Describe course patterns: Is the vehicle turning sharply, smoothly, or going straight? - Mention time duration and total changes in course or speed.</mark> 

<mark>### 2. Refined Driving Behavior Description</mark> 

<mark>Produce a single, natural-language sentence that:</mark> 

- <mark>Refines the driving description with motion extent (e.g., *smooth*, *sharp*, *wide*, * slight*)</mark> 

- <mark>Adds driving style (e.g., *cautiously*, *normally*, *aggressively*)</mark> 

- <mark>Grounding the refinement in the observable patterns of the ego vehicle states</mark> 

<mark>## Notes</mark> 

- <mark>The refined description must not exceed **20 words**.</mark> 

- <mark>Use **speed trends** to judge acceleration or deceleration patterns.</mark> 

- <mark>Use **course change patterns** to assess turning sharpness or trajectory smoothness.</mark> 

- <mark>If the style cannot be confidently inferred, default to **"normally"**.</mark> 

- <mark>Use **natural, human-readable language**-avoid unnecessary technical jargon.</mark> 

- <mark>If the driving description is "The vehicle is continuing straight", describe any left or right movements as "adjusting left" or "adjusting right" respectively. Do not</mark> 

- <mark>describe this as turning.</mark> 

### **B.3. NuScenes Reasoning Labeling** 

To produce reasoning traces for the NuScenes dataset, we provide a front camera view, as well as the prompt in Listing 4 to Gemini 2.5 Flash-Lite. 

#### _Listing 4._ Example Reasoning Labeling Prompt. 

<mark>You are an expert in autonomous driving planning. Given a first person dashcam view from a car and the car’s future action, describe the following:</mark> 

<mark>Future action: {meta_action}</mark> 

<mark>1. Provide a sentence of justification for the car’s future action.</mark> 

- <mark>A concrete example is as follows: There is a car in the oncoming lane and an accident ahead of me, so I should wait within my lane until the oncoming car is clear.</mark> 

18 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 


_Figure 6._ **Input images for meta-action labeling.** The first-round prompt gives a baseline action and the second-round prompt produces a refined meta-action. (a) Example where the baseline action is “changing lanes left,” refined to “The vehicle is smoothly changing lanes left normally.” (b) Example where the baseline action is “continuing straight,” refined to “The car normally accelerates, then maintains speed while subtly drifting right.” 

<mark>2. Behavior description of critical objects: describe the current status and intent for the 2-3 most important critical objects in the image (e.g. pedestrians, vehicles, cyclists, stop signs, traffic lights, construction cones, etc.) in 3 sentences or fewer.</mark> 

- <mark>A concrete example is as follows: The pedestrian is currently standing on the sidewalk, looking toward the road, and maybe preparing to cross the street. The vehicle is currently ahead of me, moving in the same direction, and its future trajectory suggests it will continue straight.</mark> 

### **B.4. VLM Zero-shot Prompt** 

To compare the zero-shot capabilities of an off-the-shelf VLM on our meta-action prediction task, we provide the prompt in Listing 5 to Gemini 2.5 Flash-Lite (the same model used for labeling), together with the vehicle’s visual observation. 

_Listing 5._ Zero-shot Prompt Provided to Gemini 2.5 Flash-Lite. 

<mark>You are an autonomous driving assistant. Your task is to generate a driving behavior plan based on: A front-view camera image A sequence of historical ego states taken at 0.5 Hz over the past 6 seconds The current speed of the vehicle A routing command. Inputs: Image: <first person image from a dashcam view> Speed history: 0.0 m/s 0.0 m/s 0.0 m/s Heading history: 165.8 degrees 165.8 degrees 165.8 degrees Current speed: 0.0 m/s Routing command: Follow the road. Output:</mark> 

19 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 

<mark>1. Behavior description of critical objects: describe the current movement and appearance of all external agents in the scene, as well as their positioning relative to the ego vehicle.</mark> 

<mark>Example Output: "Red car, in one lane to the left, traveling same direction, at 6.1 m/s. Female pedestrian , in crosswalk, travelling opposite direction, at 2.1 m/s."</mark> 

<mark>2. Driving Behavior Plan: Produce a driving behavior plan (no more than 20 words) that includes: Speed behavior - Will the vehicle accelerate, maintain speed, or decelerate? Heading behavior - Describe the expected heading change (e.g., continue straight, turn slightly right, make a sharp left). Driving style - Reflect the style (e.g., cautiously, smoothly, assertively). Respond with a single natural language sentence summarizing the driving behavior. Example Output: "The car decelerates smoothly and makes a slight right turn, driving normally to follow the blue SUV."</mark> 

<mark>Notes: - The driving behavior plan must be in present tense and third person (i.e. "The vehicle ...")</mark> 

## **C. Experiment Details** 

### **C.1. Full description of baselines** 

**SimLingo (Renz et al., 2025).** A vision-only VLM framework that addresses closed-loop driving, vision-language understanding, and language-action alignment, relying solely on cameras and avoiding costly sensors such as LiDAR. SimLingo additionally leverages “action-dreaming” data, which is counterfactual data used to improve its language following capabilities. SimLingo is currently the top method on the CARLA 2.0 leaderboard. 

**DriveMoE (Yang et al., 2025).** Built upon the _π_ 0 foundation model (Black et al., 2024), DriveMoE employs a mixture-ofexperts architecture with a scene-specialized vision MoE and a skill-specialized action MoE to achieve adaptive decision making for autonomous driving. **ORION (Fu et al., 2025).** A holistic E2E framework that integrates a QT-Former for long-term history aggregation, an LLM for driving scenario reasoning, and a generative planner for precise trajectory prediction. ORION further aligns reasoning and action spaces, enabling unified optimization across both planning and visual question answering, though at the cost of greater complexity and computational demand. 

**AutoVLA (Zhou et al., 2025c).** A method that enhances a pretrained VLM with a physical action codebook for vehicle motion, effectively bridging semantic reasoning and low-level control. 

**PARA-Drive (Weng et al., 2024).** A modular end-to-end autonomous driving model that uses bird’s-eye-view features and is parallelized to improve runtime efficiency, which offers a comparison alternative modular architecture to our hierarchical structure for comparison. 

**TOKEN (Tian et al., 2024).** A method that tokenizes sensory inputs into object-centric tokens using an end-to-end driving model, PARA-Drive, trained with various driving tasks to enforce good representations. This method leverages explicit structure inspired by traditional driving stacks rather than leveraging VLM priors to make good driving decisions. 

**DiMA-VAD (Hegde et al., 2025).** DiMA-VAD distills knowledge from a VLM into a driving model through jointly training the VLM and a vision-based planner on a set of surrogate driving understanding and prediction tasks rather than directly using the VLM as a base model. 

**Agent-Driver (Mao et al., 2023b).** This method decomposes the LLM’s tasks into using a tool library to process sensory inputs, structuring information in a memory module, and performing motion planning with a reasoning engine. This method explicitly performs many of the reasoning steps that are implicitly included in our auto-labeling pipeline. 

### **C.2. Bench2Drive-LongTail** 

To evaluate the long-tail performance of SteerVLA, we introduce a long-tail subset of Bench2Drive. We focus on 11 categories: 

20 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 

|**Method**|**Sensors**|**DS**_↑_|**SR(%)**_↑_|Merging|Over-<br>taking|**Ability**_↑_<br>Emergency<br>Brake|Give<br>Way|Traffic<br>Sign|Mean|
|---|---|---|---|---|---|---|---|---|---|
|DriveMoE|M|74.22|48.64|34.67|40.00|65.45|40.00|59.44|47.91|
|ORION|M|77.74|54.62|25.00|71.11|78.33|30.00|69.15|54.72|
|AutoVLA|M|78.84|57.73|-|-|-|-|-|-|
|SimLingo|S|85.94|66.82|**57.50**|60.00|76.67|50.00|73.16|63.46|
|SteerVLA (Ours)|S|**90.71**|**73.64**|56.25|**84.44**|**81.67**|**60.00**|**81.05**|**72.68**|


_Table 3._ **Evaluation of SteerVLA on Bench2Drive.** Metrics include Driving Score (DS), Success Rate (SR%), and specialized abilities (Merging, Overtaking, Emergency Brake, Give Way, Traffic Sign) with overall Mean performance. Compared to the state-of-the-art, SteerVLA outperforms the best performing baseline (SimLingo). M/S refers to Multi-camera/Single camera. 

|||**Driving**|**score** _↑_|
|---|---|---|---|
|**Long-tail Scenario**|# Routes|Simlingo|SteerVLA|
|Illegally Parked Vehicle|10|96.00|**100.00**|
|Adjacent Door Opening|5|**92.00**|**92.00**|
|Roadside Cyclist|10|**88.00**|**88.00**|
|Construction Zone|10|62.66|**96.50**|
|Traffic Accident|10|68.91|**86.33**|
|Jaywalking Pedestrian|10|**100.00**|95.00|
|Crossing Vehicle Runs Red|5|71.94|**72.06**|
|Control Loss|5|**100.00**|**100.00**|
|Hard Brake|5|**100.00**|98.86|
|Blocked Intersection|5|76.86|**100.00**|
|Yield to Emergency Vehicle|5|70.00|**76.00**|
|**Mean (route-weighted)**||83.87|**91.91**|


_Table 4._ **Performance comparison across long-tail driving scenarios on Bench2Drive-LongTail.** SteerVLA demonstrates strong long-tail performance across various scenarios in the 

1. **Crossing vehicle runs red.** A vehicle moving perpendicular to the ego-vehicle runs a red light. The ego-vehicle must recognize that it should wait for the vehicle before it proceeds. 

2. **Yield to emergency vehicle.** An emergency vehicle is driving down the street. The ego-vehicle must yield and wait for the emergency vehicle to pass. 

3. **Traffic accident.** A traffic accident has occurred, and the ego-vehicle must avoid the scene while interacting safely with other vehicles. 

4. **Roadside cyclist.** A cyclist it traveling along the same road as the ego-vehicle. The ego-vehicle must safely avoid the cyclist. 

5. **Adjacent door opening.** A vehicle on the side of the road opens its door into traffic. The ego-vehicle must safely navigate out of the situation while interacting safely with other agents. 

6. **Jaywalking pedestrian.** A pedestrian crosses the street at a non-designated crossing point. The ego-vehicle must slow to wait for the pedestrian to pass. 

7. **Construction zone.** A construction zone has modified the flow of traffic. The ego-vehicle must avoid the construction zone and merge back into the normal traffic flow. 

8. **Hard brake.** A sudden obstacle in the road causes the vehicle to need to brake abruptly. 

9. **Illegally parked vehicle.** A vehicle is parked illegally, obstructing the roadway. The ego-vehicle must reason that the vehicle is in fact parked and navigate around it. 

10. **Control loss.** The ego-vehicle encounters an area of poor traction and loses control. It must recover control without collision. 

11. **Blocked intersection.** Traffic blocks an intersection. The ego-vehicle must reason about the best course of action. 

The full list of driving scenarios in Bench2Drive is available here. We select what we believe to be the long-tail subset from the list (Jia et al., 2024). 

21 

**SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios** 

|**Method**||**Traj L**|**2 (m)**_↓_||
|---|---|---|---|---|
||1s|2s|3s|Mean|
|TOKEN<br>(Tian et al.,2024)|0.26|0.70|1.46|0.81|
|PARA-Drive<br>(Weng et al.,2024)|0.26|0.59|1.12|0.66|
|DiMA-VAD<br>(Hegde et al.,2025)|0.18|0.48|1.01|0.56|
|GPT-Driver<br>(Mao et al.,2023a)|0.20|0.40|0.70|0.44|
|Agent-Driver<br>(Mao et al.,2023b)|**0.16**|**0.34**|**0.61**|**0.37**|
|SteerVLA (Ours)|0.18|0.39|0.63|0.40|


_Table 5._ **Open-loop comparison of SteerVLA on the NuScenes planning benchmark.** SteerVLA achieves comparable L2 error compared to state-of-the-art methods. 

<u>∑︁((#routes per category)</u> _·_ <u>(DS per category)</u> We compute the route-weighted mean as _Mean_ = # routes total , where DS is driving score. 

### **C.3. Raw values of Performance on Bench2Drive** 

In addition to Fig. 3 and Fig. 4, we provide the raw scores of the baselines and SteerVLA evaluated on Bench2Drive and Bench2Drive-LongTail, provided in Table 3 and Table 4. 

### **C.4. Failure Cases in Closed-Loop Evaluation** 

However, we still observe failure cases for SteerVLA, which primarily fail into two categories. First, some failures arise from the use of a single front-view camera, which limits visibility of vehicles approaching from the sides or rear (e.g. when yielding to an emergency vehicle). Incorporating multi-view camera inputs is a promising direction for future work. Second, SteerVLA exhibits limited recovery behavior once it enters out-of-distribution states following an incorrect action. For example, when an early or aggressive lane change places the vehicle in an unexpected position relative to surrounding traffic, the policy may fail to recover safely. This limitation is likely due to insufficient coverage of non-optimal behaviors in the training data, which predominantly consists of expert demonstrations. In future work, we plan to address this issue by incorporating co-training or additional supervision from real-world data, where state distributions are more diverse and include recovery behaviors. 

### **C.5. Open-Loop Evaluation on Real-World Data** 

We additionally evaluate SteerVLA in an open-loop setting on the NuScenes planning benchmark (Caesar et al., 2020) to assess performance on real-world driving data. We adopt stronger VLM backbones than in our simulation experiments: Gemma-3 4B (Team et al., 2025) as the high-level policy and PaliGemma (Beyer et al., 2024) as the low-level policy. For the low-level policy, we follow the approach of Kim et al. (2024), repurposing rarely used tokens to represent discretized actions, where each dimension is divided into 512 uniform bins over the normalized range [ _−_ 1 _,_ 1] based on dataset statistics (Octo Model Team et al., 2024; Brohan et al., 2023b). Since NuScenes does not provide language annotations, we apply our automatic labeling pipeline to generate grounded meta-actions and reasoning traces directly from raw driving data, which are used to supervise both the high-level and low-level policies. Details on data labeling are provided in Sections B.2 and B.3. All models are trained and evaluated on the official NuScenes training and validation splits. 

We apply the full auto-labeling pipeline to the NuScenes dataset and evaluate SteerVLA against several baselines on the NuScenes planning benchmark (see Table 5). The policy is executed at 2 Hz, and performance is measured using L2 trajectory error over prediction horizons of 1, 2, and 3 seconds. We compare SteerVLA with PARA-Drive (Weng et al., 2024), TOKEN (Tian et al., 2024), DiMA-VAD (Hegde et al., 2025), and Agent-Driver (Mao et al., 2023b), which represent a range of modular, token-based, distilled, and LLM-guided driving approaches. 

As shown in Table 5, SteerVLA achieves performance comparable to or better than existing methods across all horizons, indicating that our framework generalizes effectively to real-world driving data despite being primarily evaluated in closed-loop simulation. 

22 

