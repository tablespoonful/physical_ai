---
title: "Learning Vision-Language-Action World Models for Autonomous Driving"
date: "2026-04-10"
authors: "Guoqing Wang; Pin Tang; Xiangxuan Ren; Guodongfang Zhao; Bailan Feng; Chao Ma"
url: https://arxiv.org/abs/2604.09059
pdf: https://arxiv.org/pdf/2604.09059
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.09059)** / [論文ページ](https://arxiv.org/abs/2604.09059)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Learning Vision-Language-Action World Models for Autonomous Driving** 

Guoqing Wang<sup>1</sup> Pin Tang<sup>1</sup> Xiangxuan Ren<sup>1</sup> Guodongfang Zhao<sup>2</sup> Bailan Feng<sup>2</sup> Chao Ma<sup>1†</sup> 1 MoE Key Lab of Artificial Intelligence, AI Institute, Shanghai Jiao Tong University 2 Central Research Institute, Huawei 

{guoqing.wang, pin.tang, bunny_renxiangxuan, chaoma}@sjtu.edu.cn 

{zhaoguodongfang, fengbailan}@huawei.com 


Figure 1. Visual overview of VLA-World. The model learns through three progressive stages. We first activate visual generation by predicting future frames from multi-view inputs to learn generation knowledge. Then, we fine-tune the model to link perception, future generation, and planning to learn driving conceptual knowledge. Finally, we use reinforcement learning to refine decisions through interaction with generated futures to explore reasoning knowledge. The results on the right show that VLA-World achieves both the lowest collision rate and FID score, highlighting its strengths in future generation and driving-oriented reasoning. 

## **Abstract** 

_Vision-Language-Action (VLA) models have recently achieved notable progress in end-to-end autonomous driving by integrating perception, reasoning, and control within a unified multimodal framework. However, they often lack explicit modeling of temporal dynamics and global world consistency, which limits their foresight and safety. In contrast, world models can simulate plausible future scenes but generally struggle to reason about or evaluate the imagined future they generate. In this work, we present VLA-World, a simple yet effective VLA world model that unifies predictive imagination with reflective reasoning to improve driving foresight. VLA-World first uses an action-derived feasible trajectory to guide the generation of the next-frame image, capturing rich spatial and temporal cues that describe how the surrounding environment evolves. The model then reasons over this self-generated future imagined frame to refine the predicted_ 

†Corresponding author. 

_trajectory, achieving higher performance and better interpretability. To support this pipeline, we curate nuScenes-GR20K, a generative reasoning dataset derived from nuScenes, and employ a three-stage training strategy that includes pretraining, supervised fine-tuning, and reinforcement learning. Extensive experiments demonstrate that VLA-World consistently surpasses state-of-the-art VLA and world-model baselines on both planning and future-generation benchmarks. Project page: https://vlaworld.github.io_ 

## **1. Introduction** 

Recently, two major paradigms have gained attention in endto-end autonomous driving: Vision-Language-Action (VLA) models [3, 16, 20, 30, 33, 42, 76, 84, 86] and World Models [22, 28, 41, 44, 59–61]. Unlike traditional end-to-end pipelines [12, 13, 15, 25, 29] that learn perception and control only from driving data, VLA models are built on powerful Vision-Language Models (VLMs) [1, 2, 4, 5, 39, 40] pre- 


Figure 2. Comparison of the (a) VLA, (b) World Model, and (c) the proposed VLA-World paradigm. 

trained on large vision-instruction datasets. By combining perception, language-based reasoning, and action generation in an autoregressive manner, they offer strong generalization and scalability. World models focus on predicting how the environment will evolve by generating future frames. Using generative architectures, they learn latent spatiotemporal dynamics that allow the models to anticipate upcoming events and support more informed decision-making. 

However, both paradigms face fundamental limitations. Existing VLA models [30, 53, 84, 86] inherently lack explicitly spatiotemporal modeling of other dynamic agents in the driving scenes, making it difficult to predict the evolution of complex scenarios, a capability that is essential for safe and proactive driving. In contrast, world models typically rely on large-scale visual data to learn a prior distribution and then sample from it, without capturing the underlying causal relationships of the world effectively. As a result, they tend to _simulate_ the world rather than truly _understand_ it. 

To address these limitations, recent works [11, 14, 63, 65, 74, 77] have begun exploring unified architectures that integrate generation and understanding, using generation as a bridge to enhance latent representations. Building upon these works, we argue that an ideal paradigm for end-to-end autonomous driving should merge the spatiotemporal modeling strength of world models with the reasoning ability of VLA models. Such a pipeline would not only envision how the scene will evolve but also interpret and reflect on those imagined futures, much as human drivers do. A vivid driving example illustrates this intuition. When cruising on an open road, a human driver relies on quick, intuitive imagination, like world models, to predict the next few moments without conscious effort. But if a pedestrian suddenly steps into the lane, the driver immediately shifts into reflective reasoning: the mind simulates what would happen if the car kept moving at the same speed, evaluates the outcome, and then overrides the initial impulse to continue forward. 

We introduce VLA-World, a simple yet effective VisionLanguage-Action World Model that not only generates shortterm future frames conditioned on predicted short-term trajectories but also reasons over these imagined futures to assess potential risks. This enables more informed decisions and safer trajectory planning. Our key insight is that short-term predicted futures naturally encode rich spatiotemporal information about how the scene will evolve, capturing both ego motion and the behaviors of surrounding agents, which are essential for reliable driving reasoning. As illustrated in Figure 2, VLA-World follows a multi-step pipeline that includes perception, short-term prediction, generation, reasoning, and planning. VLA-World first perceives the environment by detecting relevant traffic participants and estimating distances to road boundaries. It then predicts the ego trajectory and driving direction for the next 0.5 seconds and generates the corresponding future frame based on these predictions. The model reasons over this generated future image to identify important agents and potential risks that may emerge. Finally, it outputs the appropriate driving decision along with the long-term trajectory. By integrating imagination and reasoning within one framework, VLA-World can both anticipate and reflect on upcoming events, resulting in more human-like and safety-aware driving behavior. 

To support this pipeline, we curate a dataset from nuScenes [10], named nuScenes-GR-20K, specifically designed for generating future frames and reasoning conditioned on them. We further introduce a three-stage training strategy to fully explore the reasoning capability, as shown in Figure 1. The process includes: (1) pretraining on large image–instruction datasets to activate visual generation knowledge, (2) supervised fine-tuning (SFT) on a multi-task mixed dataset to learn driving-related conceptual knowledge, and (3) reinforcement learning (RL) with Group Relative Policy Optimization (GRPO) to explore human-like reasoning knowledge. This three-stage training pipeline maintains end-to-end policy consistency and enables joint optimization across all components, from future generation to reasoning and planning. Extensive experiments show that VLA-World significantly outperforms state-of-the-art VLA and world model baselines on both generation and reasoning benchmarks, highlighting the effectiveness and versatility of our approach. In summary, our contributions are as follows: 

- We introduce a simple yet effective VLA world model for autonomous driving that unifies predictive imagination and reflective reasoning in a single framework. 

- We curate nuScenes-GR-20K, a dataset for generation and reasoning, and propose a three-stage training strategy to fully unleash the intelligence of VLA-World. 

- We thoroughly evaluate VLA-World and show that it achieves strong performance on both future-frame generation and planning benchmarks, outperforming previous VLA and world models. 

## **2. Related Work** 

### **2.1. Vision-Language-Action Models** 

Vision-Language-Action (VLA) models [6–8, 11, 17, 30, 43, 45, 46, 53, 67, 81, 84, 86, 87] have achieved notable progress in robotics and autonomous driving, driven by the rapid advances of multimodal large language models (MLLMs) [4, 5, 35, 36, 39, 40, 47, 54, 56]. Several works [50, 53, 58, 67] for autonomous driving leverage pretrained LLMs to generate driving actions accompanied by textual rationales, thus can enhance the reasoning and interpretability of the model. DriveMoE [72] introduces a Mixture of Experts framework that dynamically selects specialized networks to better handle diverse and complex scenarios. OmniDrive [57] presents a unified LLM-agent system that supports 3D perception, reasoning, and planning through a query-based 3D vision-language architecture and a new counterfactual benchmark. Inspired by the reasoning style of DeepSeek-R1 [19], several methods [30, 73, 81] incorporate GRPO-based reinforcement learning [51] to strengthen reasoning and self-reflection in VLA models. Despite these advances, current VLA approaches still have limited temporal understanding and weak world consistency, as they often map observations directly to actions without modeling how the environment evolves over time. 

### **2.2. World Models for Autonomous Driving** 

Most existing world models [9, 32, 34, 59, 61, 64, 66, 69– 71, 78–80, 83] for autonomous driving focus on generating driving-compliant videos from past image sequences and current actions. A pioneering work is DriveDreamer [59], which uses a diffusion-based framework to generate realistic future driving videos and predict subsequent actions. DrivingWorld [24] introduces a GPT-style world model for autonomous driving, featuring several spatial-temporal fusion mechanisms, which enable effective modeling of both spatial and temporal dynamics, facilitating high-fidelity, longduration video generation. To maintain multi-view consistency due to the absence of an effective 3D spatial representation, OccWorld [78] leverages the past 3D occupancy observations to generate future 3D occupancy maps. Most existing world models focus on generating temporally consistent future scenes but lack explicit reasoning or action awareness, limiting their interpretability and decision reliability. Recently, FSDrive [74] introduces a spatiotemporal Chain-of-Thought (CoT) [48, 62] based on Qwen2-VL [68] model that _thinks visually_ by generating a future image frame as an intermediate reasoning step. Different from FSDrive, our proposed VLA-World integrates the predictive imagination of world models with the reflective reasoning of VLA frameworks, enabling both accurate foresight and cognitively grounded decision-making for autonomous driving. 

## **3. Proposed Method** 

In this section, we first introduce the preliminaries on VLA and world models. Then, we present the overview of VLAWorld. Finally, we introduce the three training stages in order, shown in Figure 3: (1) visual pretraining, (2) supervised fine-tuning, and (3) reinforcement learning. 

### **3.1. Preliminaries: VLA vs. World Models** 

We consider an agent that drives in discrete time _t_ = _{_ 1 _,_ 2 _, . . . }_ with a fixed step ∆ _t_ (e.g., 0.5 s). At time _t_ , the driving agent receives multi-view visual observations and its ego status _ot_ = _{It_<sup>1:</sup><sup>_K_</sup> _, St}_ , where _It_<sup>_k∈_R</sup><sup>_H×W ×_3denote</sup> the input images from camera _k ∈{_ 1 _, . . . , K}_ and _St ∈_ R<sup>_ds_</sup> includes ego-velocity, acceleration, yaw rate, and other CAN signals. The agent is conditioned on a mission goal _g_ (e.g., left/right/forward). We denote the future waypoint trajectory in an ego-centric BEV coordinate as 


and the next-frame image (for a chosen camera or view) as _xt_ +1. The action space can be low-level controls _at_ (throttle, brake, steering) or a trajectory _τt_ : _t_ + _H_ . 

**VLA Models.** The VLA models learn a direct mapping from history observations and goals to trajectories as _πθ_ ( _τt_ : _t_ + _H | o_ 1: _t, g_ ). This paradigm unifies perception, reasoning, and planning within a large language or multimodal language model framework. Similar to a one-stage end-to-end autonomous driving pipeline, it can be trained purely on largescale trajectory data, making the overall optimization highly concise and efficient. However, VLA lacks explicit modeling of temporal dynamics and world consistency, which causes the model to focus mainly on the ego vehicle while neglecting the motion modeling of other traffic participants, an essential component that must be captured in end-to-end autonomous driving pipelines [13, 25, 29]. 

**World Models.** World models aim to capture the latent dynamics of the surrounding environment by predicting how the world evolves under actions. Formally, it learns a transition distribution _pψ_ ( _wt_ +1 _| wt, at_ ), where _wt_ is a latent state summarizing past observations _o_ 1: _t_ , and _at_ is the action taken by the agent. The latent state is typically obtained through an encoder, and the model can reconstruct or imagine future observations through a decoder. Intuitively, a world model serves as an internal simulator that allows an agent to _dream_ plausible futures, visualizing potential outcomes of its actions without physically interacting with the environment. By repeatedly rolling out _{wt_ +1 _, wt_ +2 _, . . .}_ , the model can perform long-horizon prediction and reasoning in latent space. While conventional world models are strong at temporal prediction and future imagination, they usually lack reflective reasoning, meaning they can simulate what may happen but cannot assess whether those imagined futures are safe, feasible, or desirable. 


Figure 3. The illustration of the three-stage training and inference pipeline of VLA-World. Our training pipeline consists of three key stages: (a) visual pretrain to activate generation capability, (b) supervised fine-tuning to seed conceptual knowledge to the model, and (c) reinforcement learning with GRPO to explore higher performance like humans. 

### **3.2. Vision-Language-Action World Model** 

VLA-World is a unified framework that combines the strengths of VLA and world models to improve decisionmaking in autonomous driving. It harnesses the predictive imagination of world models to simulate future scenarios and refines these predictions through reflective reasoning, enabling more accurate, interpretable, and safety-aware driving decisions. We formulate this paradigm as 


where _τt_ +1 conditions the near-future evolution. Pure VLA models focus on the left factor, and pure world models focus on the right factor. For safe and interpretable driving, reflective thinking is needed: after imagining _x_ ˆ _t_ +1, the policy should query future evidence and revise its plan accordingly. 

Given a sequence of observations _o_ 1: _t_ and a mission goal _g_ , VLA-World first predicts an initial future trajectory ˆ _τt_ : _t_ +1. Conditioned on this predicted trajectory and the past observations, the model then imagines the expected visual observation at the next time step: 


The generated image _x_ ˆ _t_ +1 represents the anticipated nearfuture view under its current plan. Rather than treating visual 

generation as an auxiliary output, we use this imagined future as an explicit cue for reflective reasoning: 


where _f_ ref denotes the reflective reasoning module. This refinement step preserves the intent of the initial prediction while correcting decisions that are unsafe or inconsistent with the self-generated future. The final trajectory _τ_ ˜ _t_ : _t_ + _H_ therefore reflects both the model’s predicted dynamics and its reasoning over the imagined future scene. 

**Intuitive Insight.** Our core insight enables _thinking and reflection through future images generated from short-term predicted trajectories_ . First, the model produces an intuitive short-term plan that samples the high-dimensional future into a reasonable and trustworthy space. It then visualizes the intuitive outcome on its sketchpad, which contains rich spatiotemporal cues. Most importantly, the model explicitly reflects on the content of its own generated images to identify potential risks that intuition might have overlooked. This closed loop from simulation to reflection allows the model to first act on intuition to find a path and then thoughtfully evaluate its consequences to seek the optimal solution. 

### **3.3. Visual Pretraining of VLA-World** 

Following the alignment strategy of FSDrive [74], our visual pretraining stage aims to activate both the visual understanding and visual generation abilities of VLA-World, allowing the model to interpret complex driving scenes and imagine 

their short-term evolution. Unlike FSDrive, which generates future frames only for the front view, our pretraining stage explicitly enforces multi-view consistency, enabling the model to later produce coherent future images from any camera viewpoint required in the SFT and RL stages. 

Formally, given a multi-view image set _I_ = _{It_<sup>_k}K_</sup> _k_ =1 and an instruction _L_ describing the desired view or driving intent (e.g., generate CAM_FRONT_LEFT 0.5 s later), the model learns to predict the next visual token sequence _Q_<sup>_k_</sup> _t_ +1 through autoregressive next-token prediction: 


where _ht_ = _fϕ_ ( _It, St_ ) encodes the current multi-view observations and ego state _St_ , and _qi_<sup>_k_denotes the</sup><sup>_i_-th discrete</sup> token of the VQGAN [18, 55] codebook for camera _k_ . The generated tokens can be decoded into future images _I_<sup>ˆ</sup> _t_<sup>_k_</sup> +1 using the visual tokenizer of VQGAN. 

This formulation allows the model to learn how each camera view evolves based on motion and control cues, giving it a unified spatiotemporal prior across all perspectives. This design ensures that in downstream tasks, when the planner predicts a short-term trajectory and requests the corresponding future view (such as turning left, turning right, or going forward), the pretrained generator can produce consistent and physically plausible images from any viewpoint. In this way, we extend FSDrive into a multi-view, goal-conditioned world model, creating a strong foundation for reflective reasoning and safety-aware planning in later stages. 

### **3.4. Supervised Fine-Tuning of VLA-World** 

We perform supervised fine-tuning to seed driving conceptual knowledge into the base model through imitation learning, following the _generation-to-think_ paradigm. To achieve this, we train VLA-World on a comprehensive multi-task mixed dataset that is carefully designed to cover several essential learning objectives. 

**Perception.** The perception module acts as the visual grounding stage of VLA-World, converting raw multi-view inputs into structured spatial and semantic representations that support later short-term prediction and reasoning. Using six camera-view images together with ego status, it detects surrounding dynamic agents such as vehicles and pedestrians, estimates their 3D positions, possible motion paths, roadshoulder distances, and drivable-area boundaries. These outputs form a scene-level world state, a compact and interpretable summary that captures object categories, spatial layout, and motion cues, providing the foundation for egotrajectory prediction and reflective reasoning to ensure safety and consistency in future scenarios. 

**Short-term Prediction.** The short-term prediction module transforms the current perception results and ego status into 

near-future estimates of how the world will evolve, providing the basis for trajectory planning and temporal consistency in VLA-World. Using the history of ego states, it predicts the next waypoint and driving direction at regular intervals, for example, every 0.5 seconds. By explicitly modeling short-horizon dynamics, this module supports the visual generation step that imagines the corresponding future frame and ensures that the predicted trajectories remain smooth, temporally coherent, and physically plausible. 

**Condition-guided Generation.** The generation module serves as the imagination core of VLA-World, transforming the predicted trajectory and direction into a fixed number of visual tokens of the near future. Conditioned on the encoded scene context _o_ 1: _t_ and the predicted waypoint _τ_ ˆ _t_ +1, this module generates the next-frame image ˆ _xt_ +1, effectively visualizing how the environment is expected to evolve if the planned trajectory were executed, expressed as a compact set of visual tokens that encode spatial layout, object motion, and lighting continuity. By bridging low-level perception and high-level reasoning, this module not only offers interpretable evidence for the agent’s future state but also supplies the reflective reasoning module with a concrete scene hypothesis to evaluate for safety and consistency. This imagination step thus enables VLA-World to couple action-conditioned prediction with visual foresight, forming the foundation for reflective refinement in subsequent stages. 

**Thinking with Visual Tokens.** The thinking module embodies the reflective reasoning process of VLA-World, bridging imagination and decision refinement through causal interpretation of the generated future. After the generation module produces the next-frame prediction _x_ ˆ _t_ +1, the reflective reasoning analyzes salient entities, motion cues, and potential interactions to assess environmental risks and behavioral implications. This reflective process transforms visual evidence into situational understanding, quantifying safety margins, anticipating conflicts, and validating trajectory feasibility. Functionally, the think module serves as the cognitive layer of VLA-World, enabling the agent not only to predict what will happen but also to reason about whether it should happen, thus providing the foundation for trajectory refinement and safety-aware action in the subsequent stage. 

**Action and Trajectory Planning.** These two modules constitute the final outputs of VLA-World, transforming reflective understanding into concrete driving behavior. After the think module evaluates the safety and feasibility of the predicted scenario, the model determines the appropriate action policy or maneuver that aligns with both the mission goal and reflective reasoning outcomes. Then, we translate this high-level action into a sequence of explicit spatial waypoints _τ_ ˜ _t_ : _t_ + _H_ , representing the refined ego-trajectory at 0.5 s intervals over a 3s horizon. Together, these stages close the _perception–prediction-imagination–reflection–action_ loop of VLA-World, ensuring that final decisions are both context- 

aware and future-consistent, executing maneuvers that are not only physically feasible but also reflectively validated for safety and goal alignment. 

### **3.5. Reinforcement Learning of VLA-World** 

Building on the SFT-trained model, we further adopt GRPO [51] algorithm to strengthen the advanced reasoning and decision-making capabilities of VLA-World. As shown in Figure 3, this phase shifts the model from following predefined reasoning patterns to dynamically formulating optimal planning strategies through an iterative and self-correcting process. For each input prompt, GRPO samples a diverse set of candidate responses from the current policy. Then, we carefully designed a collection of rule-based reward functions to assess the quality of these responses across the entire VLA-World pipeline, spanning perception, short-term prediction, visual generation, and planning: **Format Reward (** _Rfmt_ **).** This reward enforces a wellstructured output format. The perception description should appear inside the <Perception> tag, the short-term trajectory and driving direction inside the <Prediction> tag, the generated visual tokens inside the <Visual> tag, the reasoning content inside the <Think> tag, and the final high-level action and three-second trajectory within the <Action> and <Answer> tags. 

**Short-term Prediction Reward (** _Rpred_ **).** This reward serves two purposes: (1) it encourages accurate prediction of the short-term trajectory and heading, which conditions future frame generation; and (2) it enforces consistency between the 0.5-second prediction and the refined long-term trajectory produced after reasoning. 

**Visual Constrain Reward (** _Rvis_ **).** This reward ensures that the number of generated visual tokens matches the required length for correct image reconstruction. In addition, every token must correspond to a valid entry in the visual codebook to guarantee a decodable and meaningful generated frame. **Action Reward (** _Ract_ **).** To assess the correctness of the predicted high-level action, we compute a reward derived from the F1 score, which provides a balanced evaluation of precision and recall relative to the ground truth action set. **Trajectory Reward (** _Rtraj_ **).** This reward ensures that the predicted trajectory over the final three seconds is accurate at each interval, while also enforcing kinematic consistency. For example, for an agent moving smoothly, the changes in acceleration should remain very small. 

The final reward is computed as a weighted combination of all the above components: 

_R_ all = _λ_ fmt _·R_ fmt+ _λ_ pred _·R_ pred+ _λ_ vis _·R_ vis+ _λ_ act _·R_ act+ _λ_ traj _·R_ traj _._ (6) 

Overall, this training stage guides VLA-World toward producing outputs that are structurally correct, short-term prediction reasonable, visually coherent, and behaviorally safe, ultimately enabling more reliable driving decisions. 

## **4. Experiments** 

### **4.1. Experimental Setup** 

**Datasets and Metrics.** We conduct experiments on nuScenes dataset [10] following the traditional end-to-end methods [13, 25, 29], VLA [27, 57, 74] and world models [31, 59, 61, 80]. We curate a nuScenes-GR-20K dataset, including 20K samples for generating future frames and reasoning conditioned on them for SFT and RL stages. We evaluate trajectory planning performance using L2 displacement error and collision rate, following established protocols in prior studies [13, 23, 29, 57, 74]. In addition, consistent with prior works for generation [59, 61], we employ the Fréchet Inception Distance (FID) to evaluate the visual quality of generated future frames. More details are listed in the supplementary materials. 

**Implementation Details.** We initialize our model with Qwen2-VL-2B [56] following FSDrive [74]. All training is conducted on 8 _×_ 80 GB GPUs using the PyTorch framework. During the pretraining stage, the model is trained for 30 epochs using AdamW with an initial learning rate of 5 _×_ 10<sup>_−_4</sup> , a per-device batch size of 16. For supervised finetuning, we train the model for 12 epochs with AdamW and an initial learning rate of 1 _×_ 10<sup>_−_4</sup> . Starting from the SFT checkpoint, the model undergoes an additional optimization phase using the GRPO for one epoch. The policy is trained with a learning rate of 1 _×_ 10<sup>_−_6</sup> and a global batch size of 16. For each prompt, we sample 8 candidate responses to estimate the policy gradient. More implementation details can be found in supplementary materials. 

### **4.2. Main Results** 

**End-to-End Trajectory Planning.** We evaluate our method with both non-autoregressive and autoregressive baselines using ST-P3 and UniAD metrics on nuScenes. VLA-World achieves the best overall performance on both benchmarks, showing the lowest average L2 error and collision rate among autoregressive methods. Compared with non-autoregressive planners such as BEV-Planner [38] and UniAD [25], VLAWorld maintains better performance while producing more stable long-horizon predictions, benefiting from its generative world-model architecture. Unlike FSDrive, which directly regress future waypoints without evaluating physical feasibility, VLA-World integrates short-term imagination with reflective correction, leading to stronger foresight and reduced temporal drift. The improvements are most pronounced at 3-second horizons, where traditional VLA models tend to accumulate error. Overall, these results confirm that the proposed framework, combining action-conditioned future frame generation with reflective trajectory refinement, yields significant gains in both safety and trajectory fidelity, establishing VLA-World as a state-of-the-art method for autonomous driving. 

Table 1. End-to-end trajectory planning results on nuScenes [10]. We evaluate L2 error and collision rate following the respective protocols of ST-P3 [23] and UniAD [25]. The _∗_ indicates the use of additional ego-state information. Results for VAD [29] and UniAD [25] are taken from BEV-Planner [38]. 

||||**S**|**T-P3**|**metric**|**s**|||||**U**|**niAD**|**metr**|**ics**||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method**||**L2 (**|**m)**_↓_||**C**|**ollisi**|**on (%**|**)**_↓_||**L2**|**(m)**_↓_|||**Collisio**|**n (%**|**)**_↓_|**LLM**|
||1s|2s|3s|Avg.|1s|2s|3s|Avg.|1s|2s|3s|Avg.|1s|2s|3s|Avg.||
||||||**N**|**on-**|**Autor**|**egressi**|**ve me**|**thods**||||||||
|ST-P3* [ECCV22][23]|1.33|2.11|2.90|2.11|0.23|0.62|1.27|0.71|-|-|-|-|-|-|-|-|-|
|VAD [ICCV23][29]|0.69|1.22|1.83|1.25|0.06|0.68|2.52|1.09|-|-|-|-|-|-|-|-|-|
|VAD* [ICCV23][29]|0.17|0.34|0.60|0.37|0.04|0.27|0.67|0.33|-|-|-|-|-|-|-|-|-|
|UniAD [CVPR23][25]|-|-|-|-|-|-|-|-|0.59|1.01|1.48|1.03|0.16|0.51|1.64|0.77|-|
|UniAD* [CVPR23][25]|-|-|-|-|-|-|-|-|0.20|0.42|**0.75**|0.46|0.02|0.25|0.84|0.37|-|
|BEV-Planner [CVPR24][38]|0.30|0.52|0.83|0.55|0.10|0.37|1.30|0.59|-|-|-|-|-|-|-|-|-|
|BEV-Planner* [CVPR24][38]|0.16|0.32|0.57|0.35|**0.00**|0.29|0.73|0.34|-|-|-|-|-|-|-|-|-|
|PreWorld [ICLR25][37]|-|-|-|-|-|-|-|-|0.49|1.22|2.32|1.34|0.19|0.57|2.65|1.14|-|
|||||||**Au**|**toreg**|**ressive**|**metho**|**ds**||||||||
|ELM [ECCV24][85]|-|-|-|-|-|-|-|-|0.34|1.23|2.57|1.38|0.12|0.50|2.36|0.99|BLIP2-2.7B|
|FeD* [CVPR24][75]|-|-|-|-|-|-|-|-|0.27|0.53|0.94|0.58|**0.00**|**0.04**|0.52|0.19|LLaVA-7B|
|OccWorld [ECCV24][78]|0.39|0.73|1.18|0.77|0.11|0.19|0.67|0.32|0.52|1.27|2.41|1.40|0.12|0.40|2.08|0.87|GPT3-like|
|Doe-1 [arxiv24][80]|0.37|0.67|1.07|0.70|0.02|0.14|0.47|0.21|0.50|1.18|2.11|1.26|0.04|0.37|1.19|0.53|Lumina-mGPT-7B|
|RDA-Driver* [ECCV24][26]|0.17|0.37|0.69|0.40|0.01|0.05|0.26|**0.10**|0.23|0.73|1.54|0.80|**0.00**|0.13|0.83|0.32|LLaVA-7B|
|EMMA* [arxiv24][27]|0.14|0.29|0.54|0.32|-|-|-|-|-|-|-|-|-|-|-|-|Gemini 1.0 Nano-1|
|OmniDrive [CVPR25][57]|0.40|0.80|1.32|0.84|0.04|0.46|2.32|0.94|-|-|-|-|-|-|-|-|LLaVA-7B|
|OmniDrive* [CVPR25][57]|0.14|0.29|0.55|0.33|**0.00**|0.13|0.78|0.30|-|-|-|-|-|-|-|-|LLaVA-7B|
|FSDrive [NeurIPS25][74]|0.28|0.52|0.80|0.53|0.06|0.13|0.32|0.17|0.40|0.89|1.60|0.96|0.07|0.12|1.02|0.40|Qwen2-VL-2B|
|FSDrive* [NeurIPS25][74]|0.14|0.25|0.46|0.28|0.03|0.06|**0.21**|0.10|0.18|0.39|0.77|0.45|**0.00**|0.06|0.42|0.16|Qwen2-VL-2B|
|**VLA-World (ours)**|0.11|0.27|0.52|0.30|0.00|**0.03**|0.26|0.10|0.38|0.74|1.38|0.83|0.02|0.08|0.36|0.16|Qwen2-VL-2B|
|<br>**VLA-World* (ours)**|**0.10 **|**0.24 **|**0.45**|**0.26**|0.02|0.05|**0.18**|**0.08**|**0.10 **|**0.35**|0.80|**0.42**|0.01|0.05|**0.30**|**0.12**|Qwen2-VL-2B|


Table 2. Comparison of future frame generation results with different generative models evaluated by FID ( _↓_ ) on the nuScenes [10] dataset. 

|**Method**|DriveGAN<br>[CVPR21 [31]]|DriveDreamer<br>[ECCV24 [59]]|Drive-WM<br>[CVPR24 [61]]|GenAD<br>[CVPR24 [69]]|GEM<br>[CVPR25 [21]]|Doe-1<br>[arxiv24 [80]]|FSDrive<br>[NeurIPS25 [74]]|**VLA-World**|
|---|---|---|---|---|---|---|---|---|
|**Type**|GAN|Diffusion|Diffusion|Diffusion|Diffusion|Autoregressive|Autoregressive|Autoregressive|
|**Resolution**|256_×_256|128_×_192|192_×_384|256_×_448|576_×_1024|384_×_672|128_×_192|128_×_192|
|**FID**_↓_|73.4|52.6|15.8|15.4|10.5|15.9|10.1|**9.8**|


Table 3. Action prediction performance on the nuScenes dataset measured by F1 score (%). † denotes models trained on nuScenes. 

|Method|Late<br>forward|ral(F1<br>left|)_↑_<br>right|Lo<br>keep|ngitudi<br>acc.|nal(F1<br>dec.|)_↑_<br>stop|
|---|---|---|---|---|---|---|---|
|Qwen2-VL-2B|62.43|22.75|28.65|40.70|50.23|49.21|41.04|
|Qwen2-VL-2B†|92.60|61.78|66.52|56.42|74.32|76.10|74.85|
|VLA-World|**95.88**|**74.22 **|**75.06**|**60.98 **|**81.42 **|**80.04 **|**81.24**|


**Evaluation of Action.** Table 3 shows the action prediction results of VLA-World across both lateral and longitudinal categories, evaluated using the F1-score. Our model achieves clear and consistent improvements in all action types, demonstrating its strong capability in learning goal-conditioned control. Compared with the base Qwen2-VL-2B backbone, the model fine-tuned on nuScenes (Qwen2-VL-2B†) shows a substantial performance boost, particularly for turning behaviors where the left category improves from 22.75% to 

61.78% in F1-score. Our VLA-World delivers the best results across every metric, achieving 95.88% for forward, 74.22% for left, and 75.06% for right. These improvements highlight the effectiveness of our VLA-World pipeline. It learns to reason about the consequences of its own actions rather than only imitating labels by reinforcement learning. **Quantitative Results of Generation.** Although the ultimate goal of VLA-World is trajectory planning, the generation of the next frame serves only as an intermediate step to support subsequent reasoning. Nevertheless, as shown in Table 2, we evaluate the visual quality using the FID metric. Our method achieves competitive performance compared with dedicated diffusion models [59, 61, 69]. Moreover, compared with Doe-1 [80] and FSDrive [74], our approach still demonstrates a significant advantage, indicating that even with limited data, it can effectively unleash the visual generation capability of multimodal large language models. **Visualization Results.** We present a qualitative comparison 


Figure 4. Visualization of our VLA-World compared with the SOTA FSDrive [74]. The top row shows the current scene, and the bottom row shows the generated scene for the next 0.5 seconds. The red trajectory is the model prediction, and the green trajectory is the ground truth. Zoom in for a better view. 

of trajectory prediction and future-frame generation between FSDrive [74] and our VLA-World. As shown in Figure 4, VLA-World produces noticeably sharper and more coherent future frames, benefiting from visual generation that is explicitly conditioned on the predicted trajectory and driving direction. Furthermore, VLA-World can perform reflective reasoning over the imagined temporal cues, enabling it to refine its motion forecasts, resulting in future trajectories that are more precise compared with FSDrive. 

### **4.3. Ablation Study** 

**Effectiveness of training strategy.** We conduct ablation studies on the training strategy of VLA-World. _w/o. P.T._ , _w/o. SFT_ , and _w/o. RL_ denote variants of the proposed method with the pretraining, supervised fine-tuning (cold start), and reinforcement learning stages removed, respectively. As shown in Table 4 (a), we observe that although each stage contributes to overall performance improvement, the variant trained with SFT outperforms the one trained with RL. This indicates that reinforcement learning without cold-start supervision struggles to effectively navigate the large search space of our structured, multi-step reasoning task. Therefore, SFT is crucial for instilling coherent policies and a fundamental understanding of causal chains. The pretraining stage also provides additional gains by enhancing the model’s spatiotemporal understanding of driving environments through future frame generation. The superior performance of the complete VLA-World model confirms the importance of our hybrid training design: pretraining aligns generation and understanding, SFT builds the essential knowledge founda- 

Table 4. Ablation studies of trajectory planning L2 errors (ST-P3) on nuScenes to validate each proposed component. 

||**Method**||**L2 Err**|**or (m)**_↓_||
|---|---|---|---|---|---|
|||1s|2s|3s|Avg.|
||w/o. P.T.|0.35|0.56|0.81|0.57|
|(a)|w/o. SFT|0.35|0.79|1.40|0.85|
||w/o. RL|0.43|0.70|1.01|0.71|
||w/o. Perception|0.42|0.73|1.09|0.75|
|(b)|w/o. Generation|0.41|0.67|0.96|0.68|
||w/o. Reasoning|0.50|0.83|1.22|0.85|
||w/o. _R_pred|0.17|0.37|0.69|0.41|
||w/o. _R_vis|0.20|0.40|0.67|0.42|
|(c)|w/o. _R_act|0.40|0.54|0.92|0.62|
||w/o. _R_traj|0.46|0.75|0.96|0.72|
|(d)|VLA-World|**0.11**|**0.27**|**0.52**|**0.30**|


tion, and RL further refines the policy to achieve optimal performance. 

**Effectiveness of data pipeline.** To verify the effectiveness of each step in our data pipeline, we perform ablation studies on these three components. As shown in Table 4 (b), all components contribute positively to overall performance. In particular, perception and reasoning have a greater impact compared to visual generation. We attribute this to the fact that visual generation involves producing a large number of tokens, which dominate the gradient updates during optimization, potentially limiting the exploration of the upper bound of model performance. 

**Effectiveness of different rewards.** We also conduct ablation studies on the contribution of different rewards in the reinforcement learning stage. As shown in Table 4 (c), all reward terms have a positive effect on policy optimization, with the trajectory and action rewards contributing the most. This indicates that reinforcement learning can directly optimize the planning process in an end-to-end manner. 

## **5. Conclusion** 

We introduced VLA-World, a unified Vision-LanguageAction World Model that integrates predictive imagination and reflective reasoning for end-to-end autonomous driving. Unlike VLA or world models, VLA-World combines future simulation with reasoning, enabling the model to both anticipate and evaluate outcomes for safer decision-making. To realize this framework, we constructed nuScenes-GR-20K, a dataset designed for future frame generation and reasoning, and developed a three-stage training pipeline including pretraining, supervised fine-tuning, and reinforcement learning with GRPO. Extensive experiments demonstrate that VLAWorld surpasses existing methods in trajectory planning and visual generation, achieving improved interpretability and human-like reasoning, paving the way toward more intelligent and reliable autonomous driving. 

**Acknowledgements.** This work was supported in part by NSFC (62322113, 62376156), Shanghai Municipal Science and Technology Major Project (2025SHZDZX025G15, 2021SHZDZX0102), and the Fundamental Research Funds for the Central Universities. 

## **References** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 

   - technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 1 

- [2] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katherine Millican, Malcolm Reynolds, et al. Flamingo: a visual language model for few-shot learning. In _NeurIPS_ , pages 23716–23736, 2022. 1 

- [3] Hidehisa Arai, Keita Miwa, Kento Sasaki, Kohei Watanabe, Yu Yamaguchi, Shunsuke Aoki, and Issei Yamamoto. Covla: Comprehensive vision-language-action dataset for autonomous driving. In _WACV_ , pages 1933–1943, 2025. 1 

- [4] Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan Tan, Peng Wang, Junyang Lin, Chang Zhou, and Jingren Zhou. Qwen-vl: A frontier large vision-language model with versatile abilities. _arXiv preprint arXiv:2308.12966_ , 2023. 1, 3 

- [5] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, Humen Zhong, Yuanzhi Zhu, Mingkun Yang, Zhaohai Li, Jianqiang Wan, Pengfei Wang, Wei Ding, Zheren Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen Cheng, Hang Zhang, Zhibo Yang, Haiyang Xu, and Junyang Lin. Qwen2.5vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 

   - 1, 3 

- [6] Suneel Belkhale, Tianli Ding, Ted Xiao, Pierre Sermanet, Quon Vuong, Jonathan Tompson, Yevgen Chebotar, Debidatta Dwibedi, and Dorsa Sadigh. Rt-h: Action hierarchies using language. _arXiv preprint arXiv:2403.01823_ , 2024. 3 

- [7] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. pi_0: A vision-languageaction flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [8] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 3 

- [9] Tim Brooks, Bill Peebles, Connor Holmes, Will DePue, Yufei Guo, Li Jing, David Schnurr, Joe Taylor, Troy Luhman, Eric Luhman, et al. Video generation models as world simulators. _OpenAI Blog_ , 1(8):1, 2024. 3 

- [10] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. In _CVPR_ , pages 11621– 11631, 2020. 2, 6, 7, 3 

- [11] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 2, 3 

- [12] Li Chen, Penghao Wu, Kashyap Chitta, Bernhard Jaeger, Andreas Geiger, and Hongyang Li. End-to-end autonomous driving: Challenges and frontiers. _IEEE TPAMI_ , 2024. 1 

- [13] Shaoyu Chen, Bo Jiang, Hao Gao, Bencheng Liao, Qing Xu, Qian Zhang, Chang Huang, Wenyu Liu, and Xinggang Wang. Vadv2: End-to-end vectorized autonomous driving via probabilistic planning, 2024. 1, 3, 6, 4 

- [14] Xiaokang Chen, Zhiyu Wu, Xingchao Liu, Zizheng Pan, Wen Liu, Zhenda Xie, Xingkai Yu, and Chong Ruan. Janus-pro: Unified multimodal understanding and generation with data and model scaling. _arXiv preprint arXiv:2501.17811_ , 2025. 2 

- [15] Zhili Chen, Maosheng Ye, Shuangjie Xu, Tongyi Cao, and Qifeng Chen. Ppad: Iterative interactions of prediction and planning for end-to-end autonomous driving. In _ECCV_ , pages 239–256, 2024. 1 

- [16] Haohan Chi, Huan-ang Gao, Ziming Liu, Jianing Liu, Chenyu Liu, Jinwei Li, Kaisen Yang, Yangcheng Yu, Zeda Wang, Wenyi Li, et al. Impromptu vla: Open weights and open data for driving vision-language-action models. _arXiv preprint arXiv:2505.23757_ , 2025. 1 

- [17] Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, et al. Palm-e: An embodied multimodal language model. In _ICML_ , 2023. 3 

- [18] Patrick Esser, Robin Rombach, and Bjorn Ommer. Taming transformers for high-resolution image synthesis. In _CVPR_ , pages 12873–12883, 2021. 5 

- [19] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu Zhang, Shirong Ma, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_ , 2025. 3 

- [20] Wencheng Han, Dongqian Guo, Cheng-Zhong Xu, and Jianbing Shen. Dme-driver: Integrating human decision logic and 3d scene perception in autonomous driving. In _AAAI_ , pages 3347–3355, 2025. 1 

- [21] Mariam Hassan, Sebastian Stapf, Ahmad Rahimi, Pedro Rezende, Yasaman Haghighi, David Brüggemann, Isinsu Katircioglu, Lin Zhang, Xiaoran Chen, Suman Saha, et al. Gem: A generalizable ego-vision multimodal world model for fine-grained ego-motion, object dynamics, and scene composition control. In _CVPR_ , pages 22404–22415, 2025. 7 

- [22] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. Gaia-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 1 

- [23] Shengchao Hu, Li Chen, Penghao Wu, Hongyang Li, Junchi Yan, and Dacheng Tao. St-p3: End-to-end vision-based autonomous driving via spatial-temporal feature learning. In _ECCV_ , pages 533–549, 2022. 6, 7, 4 

- [24] Xiaotao Hu, Wei Yin, Mingkai Jia, Junyuan Deng, Xiaoyang Guo, Qian Zhang, Xiaoxiao Long, and Ping Tan. Drivingworld: Constructing world model for autonomous driving via video gpt. _arXiv preprint arXiv:2412.19505_ , 2024. 3 

- [25] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, Lewei Lu, Xiaosong Jia, Qiang Liu, Jifeng Dai, Yu Qiao, and Hongyang Li. Planning-oriented autonomous driving. In _CVPR_ , pages 17853–17862, 2023. 1, 3, 6, 7, 4 

- [26] Zhijian Huang, Tao Tang, Shaoxiang Chen, Sihao Lin, and Zequn et al. Jie. Making large language models better planners with reasoning-decision alignment. In _ECCV_ , pages 73–90, 2024. 7 

- [27] Jyh-Jing Hwang, Runsheng Xu, Hubert Lin, Wei-Chih Hung, Jingwei Ji, Kristy Choi, Di Huang, Tong He, Paul Covington, Benjamin Sapp, et al. Emma: End-to-end multimodal model for autonomous driving. _arXiv preprint arXiv:2410.23262_ , 2024. 6, 7, 3 

- [28] Fan Jia, Weixin Mao, Yingfei Liu, Yucheng Zhao, Yuqing Wen, Chi Zhang, Xiangyu Zhang, and Tiancai Wang. Adriver-i: A general world model for autonomous driving. _arXiv:2311.13549_ , 2023. 1 

- [29] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Vad: Vectorized scene representation for efficient autonomous driving. In _ICCV_ , pages 8306–8316, 2023. 1, 3, 6, 7, 4 

- [30] Bo Jiang, Shaoyu Chen, Qian Zhang, Wenyu Liu, and Xinggang Wang. Alphadrive: Unleashing the power of vlms in autonomous driving via reinforcement learning and reasoning. _arXiv preprint arXiv:2503.07608_ , 2025. 1, 2, 3 

- [31] Seung Wook Kim, Jonah Philion, Antonio Torralba, and Sanja Fidler. Drivegan: Towards a controllable high-quality neural simulation. In _CVPR_ , pages 5820–5829, 2021. 6, 7, 3 

- [32] Bohan Li, Jiazhe Guo, Hongsi Liu, Yingshuang Zou, Yikang Ding, Xiwu Chen, Hu Zhu, Feiyang Tan, Chi Zhang, Tiancai Wang, et al. Uniscene: Unified occupancy-centric driving scene generation. _arXiv preprint arXiv:2412.05435_ , 2024. 3 

- [33] Boyi Li, Yue Wang, Jiageng Mao, Boris Ivanovic, Sushant Veer, Karen Leung, and Marco Pavone. Driving everywhere with large language model policy adaptation. In _CVPR_ , pages 14948–14957, 2024. 1 

- [34] Bohan Li, Zhuang Ma, Dalong Du, Baorui Peng, Zhujin Liang, Zhenqiang Liu, Chao Ma, Yueming Jin, Hao Zhao, Wenjun Zeng, et al. Omninwm: Omniscient driving navigation world models. _arXiv preprint arXiv:2510.18313_ , 2025. 

   - 3 

- [35] Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi. Blip: Bootstrapping language-image pre-training for unified visionlanguage understanding and generation. In _ICML_ , pages 12888–12900, 2022. 3 

- [36] Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. Blip2: Bootstrapping language-image pre-training with frozen image encoders and large language models. In _ICML_ , pages 19730–19742, 2023. 3 

- [37] Xiang Li, Pengfei Li, Yupeng Zheng, Wei Sun, Yan Wang, and Yilun Chen. Semi-supervised vision-centric 3d occupancy world model for autonomous driving. _arXiv preprint arXiv:2502.07309_ , 2025. 7 

- [38] Zhiqi Li, Zhiding Yu, Shiyi Lan, Jiahan Li, Jan Kautz, Tong Lu, and Jose M. Alvarez. Is ego status all you need for 

open-loop end-to-end autonomous driving? In _CVPR_ , pages 14864–14873, 2024. 6, 7 

- [39] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. In _NeurIPS_ , pages 34892–34916, 2023. 1, 3 

- [40] Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. Improved baselines with visual instruction tuning. In _CVPR_ , pages 26296–26306, 2024. 1, 3 

- [41] Jiachen Lu, Ze Huang, Zeyu Yang, Jiahui Zhang, and Li Zhang. Wovogen: World volume-aware diffusion for controllable multi-camera driving scene generation. In _ECCV_ , pages 329–345, 2024. 1 

- [42] Yingzi Ma, Yulong Cao, Jiachen Sun, Marco Pavone, and Chaowei Xiao. Dolphins: Multimodal language model for driving. In _ECCV_ , pages 403–420, 2024. 1 

- [43] Jiageng Mao, Junjie Ye, Yuxi Qian, Marco Pavone, and Yue Wang. A language agent for autonomous driving. _arXiv preprint arXiv:2311.10813_ , 2023. 3 

- [44] Chen Min, Dawei Zhao, Liang Xiao, Jian Zhao, Xinli Xu, Zheng Zhu, Lei Jin, Jianshu Li, Yulan Guo, Junliang Xing, et al. Driveworld: 4d pre-trained scene understanding via world models for autonomous driving. In _CVPR_ , pages 15522– 15533, 2024. 1 

- [45] Ming Nie, Renyuan Peng, Chunwei Wang, Xinyue Cai, Jianhua Han, Hang Xu, and Li Zhang. Reason2drive: Towards interpretable and chain-based reasoning for autonomous driving. In _ECCV_ , pages 292–308, 2024. 3 

- [46] Kangan Qian, Sicong Jiang, Yang Zhong, Ziang Luo, Zilin Huang, Tianze Zhu, Kun Jiang, Mengmeng Yang, Zheng Fu, Jinyu Miao, et al. Agentthink: A unified framework for tool-augmented chain-of-thought reasoning in visionlanguage models for autonomous driving. _arXiv preprint arXiv:2505.15298_ , 2025. 3 

- [47] Xiangxuan Ren, Zhongdao Wang, Liping Hou, Pin Tang, Guoqing Wang, and Chao Ma. Grounding everything in tokens for multimodal large language models. _arXiv preprint arXiv:2512.10554_ , 2025. 3 

- [48] Ayushman Sarkar, Mohd Yamani Idna Idris, and Zhenyu Yu. Reasoning in computer vision: Taxonomy, models, tasks, and methodologies. _arXiv preprint arXiv:2508.10523_ , 2025. 3 

- [49] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 1 

- [50] Hao Shao, Yuxuan Hu, Letian Wang, Guanglu Song, Steven L Waslander, Yu Liu, and Hongsheng Li. Lmdrive: Closed-loop end-to-end driving with large language models. In _CVPR_ , pages 15120–15130, 2024. 3 

- [51] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Y Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 3, 6, 1 

- [52] Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin Wu, Wang Zhang, Ru Zhang, Yanghua Peng, Haibin Lin, and Chuan Wu. Hybridflow: A flexible and efficient rlhf framework. _arXiv preprint arXiv: 2409.19256_ , 2024. 3 

- [53] Xiaoyu Tian, Junru Gu, Bailin Li, Yicheng Liu, Chenxu Hu, Yang Wang, Kun Zhan, Peng Jia, Xianpeng Lang, and Hang Zhao. Drivevlm: The convergence of autonomous driving and large vision-language models. _arXiv preprint arXiv:2402.12289_ , 2024. 2, 3 

- [54] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open and efficient foundation language models. _arXiv preprint arXiv:2302.13971_ , 2023. 3 

- [55] Aaron Van Den Oord, Oriol Vinyals, et al. Neural discrete representation learning. In _NeurIPS_ , pages 6309–6318, 2017. 5 

- [56] Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, et al. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. _arXiv preprint arXiv:2409.12191_ , 2024. 3, 6 

- [57] Shihao Wang, Zhiding Yu, Xiaohui Jiang, Shiyi Lan, Min Shi, Nadine Chang, Jan Kautz, Ying Li, and Jose M Alvarez. Omnidrive: A holistic vision-language dataset for autonomous driving with counterfactual reasoning. In _CVPR_ , pages 22442– 22452, 2025. 3, 6, 7, 4 

- [58] Wenhai Wang, Jiangwei Xie, ChuanYang Hu, Haoming Zou, Jianan Fan, Wenwen Tong, Yang Wen, Silei Wu, Hanming Deng, Zhiqi Li, et al. Drivemlm: Aligning multi-modal large language models with behavioral planning states for autonomous driving. _arXiv preprint arXiv:2312.09245_ , 2023. 

   - 3 

- [59] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, Jiagang Zhu, and Jiwen Lu. Drivedreamer: Towards real-world-driven world models for autonomous driving. _arXiv:2309.09777_ , 2023. 1, 3, 6, 7, 4 

- [60] Xiaofeng Wang, Zheng Zhu, Guan Huang, Boyuan Wang, Xinze Chen, and Jiwen Lu. Worlddreamer: Towards general world models for video generation via predicting masked tokens. _arXiv:2401.09985_ , 2024. 

- [61] Yuqi Wang, Jiawei He, Lue Fan, Hongxin Li, Yuntao Chen, and Zhaoxiang Zhang. Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. In _CVPR_ , pages 14749–14759, 2024. 1, 3, 6, 7, 4 

- [62] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Ed H. Chi, F. Xia, Quoc Le, and Denny Zhou. Chain of thought prompting elicits reasoning in large language models. In _NeurIPS_ , pages 24824–24837, 2022. 3 

- [63] Chengyue Wu, Xiaokang Chen, Zhiyu Wu, Yiyang Ma, Xingchao Liu, Zizheng Pan, Wen Liu, Zhenda Xie, Xingkai Yu, Chong Ruan, et al. Janus: Decoupling visual encoding for unified multimodal understanding and generation. In _CVPR_ , pages 12966–12977, 2025. 2 

- [64] Zirui Wu, Tianyu Liu, Liyi Luo, Zhide Zhong, Jianteng Chen, Hongmin Xiao, Chao Hou, Haozhe Lou, Yuantao Chen, Runyi Yang, et al. Mars: An instance-aware, modular and realistic simulator for autonomous driving. In _CAAI_ , pages 3–15, 2023. 3 

- [65] Jinheng Xie, Weijia Mao, Zechen Bai, David Junhao Zhang, Weihao Wang, Kevin Qinghong Lin, Yuchao Gu, Zhijie Chen, 

   - Zhenheng Yang, and Mike Zheng Shou. Show-o: One single transformer to unify multimodal understanding and generation. _arXiv preprint arXiv:2408.12528_ , 2024. 2 

- [66] Tianshuo Xu, Hao Lu, Xu Yan, Yingjie Cai, Bingbing Liu, and Yingcong Chen. Occ-llm: Enhancing autonomous driving with occupancy-based large language models. _arXiv:2502.06419_ , 2025. 3 

- [67] Zhenhua Xu, Yujia Zhang, Enze Xie, Zhen Zhao, Yong Guo, Kwan-Yee K Wong, Zhenguo Li, and Hengshuang Zhao. Drivegpt4: Interpretable end-to-end autonomous driving via large language model. _arXiv preprint arXiv:2310.01412_ , 2023. 3 

- [68] An Yang, Baosong Yang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Zhou, Chengpeng Li, Chengyuan Li, Dayiheng Liu, Fei Huang, et al. Qwen2 technical report. _arXiv preprint arXiv:2407.10671_ , 2024. 3 

- [69] Jiazhi Yang, Shenyuan Gao, Yihang Qiu, Li Chen, Tianyu Li, Bo Dai, Kashyap Chitta, Penghao Wu, Jia Zeng, Ping Luo, et al. Generalized predictive model for autonomous driving. In _CVPR_ , pages 14662–14672, 2024. 3, 7 

- [70] Jiazhi Yang, Kashyap Chitta, Shenyuan Gao, Long Chen, Yuqian Shao, Xiaosong Jia, Hongyang Li, Andreas Geiger, Xiangyu Yue, and Li Chen. Resim: Reliable world simulation for autonomous driving. _arXiv preprint arXiv:2506.09981_ , 2025. 

- [71] Yu Yang, Jianbiao Mei, Yukai Ma, Siliang Du, Wenqing Chen, Yijie Qian, Yuxiang Feng, and Yong Liu. Driving in the occupancy world: Vision-centric 4d occupancy forecasting and planning via world models for autonomous driving. In _AAAI_ , pages 9327–9335, 2025. 3 

- [72] Zhenjie Yang, Yilin Chai, Xiaosong Jia, Qifeng Li, Yuqian Shao, Xuekai Zhu, Haisheng Su, and Junchi Yan. Drivemoe: Mixture-of-experts for vision-language-action model in endto-end autonomous driving. _arXiv preprint arXiv:2505.16278_ , 2025. 3 

- [73] Zhenlong Yuan, Jing Tang, Jinguo Luo, Rui Chen, Chengxuan Qian, Lei Sun, Xiangxiang Chu, Yujun Cai, Dapeng Zhang, and Shuo Li. Autodrive-r<sup>2</sup> : Incentivizing reasoning and selfreflection capacity for vla model in autonomous driving. _arXiv preprint arXiv:2509.01944_ , 2025. 3 

- [74] Shuang Zeng, Xinyuan Chang, Mengwei Xie, Xinran Liu, Yifan Bai, Zheng Pan, Mu Xu, and Xing Wei. Futuresightdrive: Thinking visually with spatio-temporal cot for autonomous driving. _arXiv preprint arXiv:2505.17685_ , 2025. 2, 3, 4, 6, 7, 8, 5 

- [75] Jimuyang Zhang, Zanming Huang, Arijit Ray, and Eshed Ohn-Bar. Feedback-guided autonomous driving. In _CVPR_ , pages 15000–15011, 2024. 7 

- [76] Jiawei Zhang, Chejian Xu, and Bo Li. Chatscene: Knowledgeenabled safety-critical scenario generation for autonomous vehicles. In _CVPR_ , pages 15459–15469, 2024. 1 

- [77] Wenyao Zhang, Hongsi Liu, Zekun Qi, Yunnan Wang, Xinqiang Yu, Jiazhao Zhang, Runpei Dong, Jiawei He, Fan Lu, He Wang, et al. Dreamvla: a vision-language-action model dreamed with comprehensive world knowledge. _arXiv preprint arXiv:2507.04447_ , 2025. 2 

- [78] Wenzhao Zheng, Weiliang Chen, Yuanhui Huang, Borui Zhang, Yueqi Duan, and Jiwen Lu. Occworld: Learning 

   - a 3d occupancy world model for autonomous driving. In _ECCV_ , pages 55–72, 2024. 3, 7 

- [79] Wenzhao Zheng, Ruiqi Song, Xianda Guo, Chenming Zhang, and Long Chen. Genad: Generative end-to-end autonomous driving. _arXiv preprint arXiv:2402.11502_ , 2024. 

- [80] Wenzhao Zheng, Zetian Xia, Yuanhui Huang, Sicheng Zuo, Jie Zhou, and Jiwen Lu. Doe-1: Closed-loop autonomous driving with large world model. _arXiv preprint arXiv:2412.09627_ , 2024. 3, 6, 7 

- [81] Weicheng Zheng, Xiaofei Mao, Nanfei Ye, Pengxiang Li, Kun Zhan, Xianpeng Lang, and Hang Zhao. Driveagent-r1: Advancing vlm-based autonomous driving with hybrid thinking and active perception. _arXiv preprint arXiv:2507.20879_ , 2025. 3 

- [82] Yaowei Zheng, Richong Zhang, Junhao Zhang, Yanhan Ye, and Zheyan Luo. Llamafactory: Unified efficient fine-tuning of 100+ language models. In _ACL_ , pages 400–410, 2024. 3 

- [83] Yupeng Zheng, Pengxuan Yang, Zebin Xing, Qichao Zhang, Yuhang Zheng, Yinfeng Gao, Pengfei Li, Teng Zhang, Zhongpu Xia, Peng Jia, et al. World4drive: End-to-end autonomous driving via intention-aware physical latent world model. In _ICCV_ , pages 28632–28642, 2025. 3 

- [84] Xingcheng Zhou, Xuyuan Han, Feng Yang, Yunpu Ma, and Alois C Knoll. Opendrivevla: Towards end-to-end autonomous driving with large vision language action model. _arXiv preprint arXiv:2503.23463_ , 2025. 1, 2, 3 

- [85] Yunsong Zhou, Linyan Huang, Qingwen Bu, Jia Zeng, Tianyu Li, Hang Qiu, Hongzi Zhu, Minyi Guo, Yu Qiao, and Hongyang Li. Embodied understanding of driving scenarios. In _ECCV_ , pages 129–148, 2024. 7 

- [86] Zewei Zhou, Tianhui Cai, Seth Z Zhao, Yun Zhang, Zhiyu Huang, Bolei Zhou, and Jiaqi Ma. Autovla: A visionlanguage-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning. _arXiv preprint arXiv:2506.13757_ , 2025. 1, 2, 3 

- [87] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _CoRL_ , pages 2165– 2183, 2023. 3 

# **Learning Vision-Language-Action World Models for Autonomous Driving** 

# Supplementary Material 

In the supplementary material, we first present the methodology detail of our proposed VLA-World, including Group Relative Policy Optimization (GRPO), short-term trajectory prediction, and theoretical analysis of VLA-World. Then, we provide the details of the datasets and implementation. Furthermore, we present additional experimental results to demonstrate the effectiveness of VLA-World. 

By optimizing this objective, VLA-World effectively performs _Self-Verification_ : it learns to implicitly discard hallucinatory or unsafe trajectories and reinforces the internal _chain-of-thought_ that leads to compliant and safe driving behaviors. This mechanism allows the model to refine its logical consistency purely through rule-based feedback, resulting in a robust planner that is both explainable and physically grounded. 

## **A. Method Details** 

### **A.1. Group Relative Policy Optimization** 

In the final training stage of VLA-World, we adopt Group Relative Policy Optimization (GRPO) [51] to unleash the latent reasoning and decision-making capabilities. Unlike traditional PPO [49], which relies on a computationally heavy value function (Critic) that often struggles with highdimensional visual dynamics, GRPO operates in a valuefree paradigm. It leverages group-wise statistics to estimate baselines, significantly reducing memory overhead while stabilizing training. 

For each driving scenario prompt _o_ , the current policy _πθ_ samples a group of _G_ candidate rollouts (outputs), denoted as _{o, o_ 1 _, . . . , oG}_ . These candidates represent diverse reasoning paths, ranging from conservative yielding to assertive maneuvering. Instead of relying on a neural reward model, we employ a set of lightweight, rule-based verifiers to compute rewards. These include outcome rewards (e.g., collision checking, generation quality, temporal consistency) and format rewards (e.g., strict compliance with the required output structure). Each rollout is evaluated to produce a scalar reward set _{r_ 1 _, r_ 2 _, . . . , rG}_ . 

To determine the relative quality of each reasoning path, we compute the normalized advantage for the _i_ -th rollout within the group: 


This group-based normalization effectively serves as a dynamic baseline, encouraging the model to prioritize trajectories that outperform the group average. The policy is then updated by maximizing the following surrogate objective: 


where the KL-divergence term ensures the policy does not deviate excessively from the reference model (the SFT checkpoint), preventing reward hacking. 

### **A.2. Short-term Trajectory Prediction** 

To ensure the synthesized future views are physically plausible and consistent with the vehicle’s movement, we employ a physics-grounded trajectory predictor. This module estimates the ego-vehicle’s future position **P**<sup>ˆ</sup> _t_ + _τ_ at a look-ahead horizon _τ_ (e.g., 0.5s), conditioned on both the historical state sequence _H_ and the high-level mission goal _g_ (e.g., _Left_ ). We formulate this prediction as a superposition of inertial dynamics and intentional control. 

**Kinematic State Estimation.** First, we extract the vehicle’s instantaneous kinematic state from the discrete historical trajectory _H_ = _{_ **P** _t−N , . . . ,_ **P** _t}_ , where **P** _i ∈_ R<sup>2</sup> denotes the coordinates in the ego-frame. We approximate the current velocity **v** _t_ and the historical inertial acceleration **a** hist using a finite difference method: 


where ∆ _t_ represents the sampling interval. The term **a** hist captures the vehicle’s momentum prior to any new control inputs. 

**Intention-Driven Refinement.** A pure constantacceleration model often fails to capture sudden maneuvers dictated by the mission goal. To address this, we introduce a goal-conditioned acceleration term **a** goal. The navigational command _c_ is mapped to a target spatial offset or a virtual waypoint, implying a required trajectory deviation. We derive **a** goal as the constant acceleration required to shift the vehicle from its current state _St_ = _{_ **P** _t,_ **v** _t}_ to the target state determined by _c_ within the horizon _τ_ . 

**Fusion and Prediction.** The final predicted trajectory is modeled as a linear fusion of the historical inertia and the future intention. We define the effective acceleration **a** eff using an adaptive weighting factor _λ ∈_ [0 _,_ 1]: 


where **a** goal = _τ_ <u>2</u><sup>2(∆</sup><sup>**P**ideal</sup><sup>_−_</sup><sup>**v**</sup><sup>_tτ_),and∆</sup><sup>**P**idealrepresents</sup> the theoretical displacement required by the command _c_ . Consequently, the predicted position **P**<sup>ˆ</sup> _t_ + _τ_ is computed via 

the kinematic equation: 


This formulation allows our model to seamlessly transition between momentum-based continuity (e.g., straight-line driving) and intention-based maneuvering (e.g., sharp turns), providing a robust geometric prior for the subsequent frame generation process. 

### **A.3. Theoretical Analysis of VLA-World** 

In this section, we provide a theoretical analysis for VLAWorld by formalizing autonomous driving as a joint optimization problem. We demonstrate that VLA-World aligns better with the driving objective than independent VLA or World Model paradigms. 

**The Joint Modeling Objective.** The central object of autonomous driving is the joint distribution of the planned ego-trajectory _τt_ : _t_ + _H_ and the anticipated short-term future environment _xt_ +1, conditioned on observation history _o_ 1: _t_ and goal _g_ . According to the probability chain rule, this joint distribution factorizes as: 


We define the ultimate driving objective _J_ ( _ω_ ) as the expected task return _R_ (aggregating safety, comfort, and rule compliance) over this joint distribution: 


Learning to drive is thus equivalent to learning a parameter set _ω_ that shapes this joint distribution to maximize reward. VLA-World explicitly parameterizes and optimizes both factors in Eq. (12), whereas previous paradigms only address one. 

**Analysis of VLA Models.** A pure VLA model implicitly integrates out the future state _xt_ +1, modeling only the marginal policy distribution: 


From a variational inference perspective, ignoring the explicit future state _x_ leads to a loose approximation of the optimal policy. For any auxiliary distribution _q_ ( _x | o, τ_ ) describing the environment dynamics, the log-likelihood of the optimal policy is bounded by the Evidence Lower Bound (ELBO): 


Theoretical Insight: A VLA model that discards _xt_ +1 is mathematically equivalent to optimizing a loose lower bound where the predictive information about scene evolution is lost. It tries to match the marginal directly without understanding the underlying causal variable _x_ . In contrast, VLAWorld models the joint numerator _p_ ( _τ, x | o, g_ ) directly. By explicitly generating _xt_ +1, VLA-World tightens this bound, effectively using the "imagined" future to reduce the uncertainty in policy estimation. 

**Analysis of World Models.** Classical world models focus on learning the transition dynamics _p_ WM( _xt_ +1 _| o, τ_ ) via a reconstruction objective: 


Crucially, this objective is weakly coupled to the driving decision. A world model seeks to maximize pixel fidelity, not driving safety. The planning is typically performed by a separate search procedure on top of this frozen model: 


Theoretical Insight: Any mismatch between generative accuracy (reconstruction) and planning utility (safety) creates a performance bottleneck. A high-fidelity simulation of a collision is valid for Eq. (17) but disastrous for the agent. Unlike VLA-World, pure world models do not back-propagate the decision reward _R_ into the model parameters _θ_ , leaving the _imagination_ disconnected from the _consequence_ . 

**Analysis of VLA-World.** VLA-World unifies the policy _πω_ and world model _pω_ into a single autoregressive transformer. The gradient of our objective _J_ ( _ω_ ) (from Eq. (13)) naturally decomposes to update both components: 


This reveals the core mechanism: Both the decision term and the imagination term are optimized by the same driving reward _R_ . In our implementation, we employ reinforcement learning with GRPO. Let _u_ denote the full sequence of tokens including trajectory _τ_ , future frame _x_ , and reasoning language. We maximize: 


Because _u_ contains the future-image tokens, the _imagination_ is no longer just minimizing reconstruction error; it is being reinforced to generate futures that lead to high-reward outcomes (e.g., highlighting risks that aid safety). This forms an imagination-decision loop. Finally, we show that VLAWorld is a strictly more expressive hypothesis class than either baseline. 

**VLA as a special case:** If we mask the imagination branch (force _pω_ ( _x | . . ._ ) to be a delta function or ignore it), Eq. (12) collapses to the marginal policy _πω_ ( _τ | o, g_ ), recovering a standard VLA. 

**World Model as a special case:** If we freeze the parameters of _pω_ ( _x | o, τ_ ) and use an external optimizer for _τ_ , we recover the trajectory search of standard World Models (Eq. (17)). 

## **B. Experiments** 

### **B.1. Dataset** 

We evaluate trajectory planning and future frame generation on the nuScenes dataset [10] following the traditional endto-end methods [13, 25, 29], VLA [27, 57, 74] and world models [31, 59, 61, 80]. The nuScenes comprises 1,000 driving scenes, each about 20 seconds long, recorded with a 32-beam LiDAR and six cameras offering a full 360-degree view. The dataset includes 28,130 training samples, 6,019 validation samples, and 193,082 unlabeled samples. 

**Pretraining Stage.** To endow the VLM with an intuitive understanding of physical dynamics, we construct a visual generation pretraining dataset as shown in Fig. 5 (a) ( _≈_ 500k). In this stage, the model functions strictly as a generative world model. The input prompt consists of current multiview observations alongside explicit definitions of the egocentric coordinate system and physical units. The objective is to autoregressively predict the discrete visual tokens corresponding to a future frame (e.g., ∆ _t_ = 0 _._ 5 _s_ ) for a specified camera view. This pretraining forces the model to internalize spatiotemporal evolution laws, such as agent motion and ego motion from large-scale data, establishing a foundational _imagination_ capability without the complexity of high-level linguistic reasoning. 

**SFT and RL Stages.** For the Supervised Fine-Tuning (SFT) and Reinforcement Learning (RL) stages, we introduce a multi-step learning paradigm as illustrated in Fig. 5 (b) ( _≈_ 20k). The input is augmented with detailed vehicle kinematics (velocity, acceleration), historical trajectories, and high-level mission commands. The model output is structured into a causal reasoning sequence: it first parses the scene via <perception> and estimates a short-term <prediction>, which conditions the generation of the future <visual> frame. Crucially, the model then explicitly reasons over this imagined future in the <think> block to assess potential risks before determining the high-level <action> and regressing the precise long-term trajectory points in <answer>. This structure unifies generation and planning, allowing GRPObased RL to optimize the consistency between the imagined future and the executed safety maneuvers. 


Figure 5. Data sample of (a) pretraining stage, (b) supervised finetuning, and (c) reinforcement learning. 

### **B.2. Implementation Details** 

We build our model upon the Qwen-VL family [56]. All training stages, including pretraining, supervised fine-tuning, and reinforcement learning, are conducted on 8 A100 GPUs, and inference is performed on 4 A100 GPUs. The pretraining and supervised fine-tuning stages use the LLaMA Factory framework [82], and the reinforcement learning stage is trained with the Easy-R1 framework [52]. We adopt multiview images as input and set the maximum pixel count to 524,288, with a gradient accumulation step of 2. During pretraining, the model is trained for 30 epochs using AdamW with an initial learning rate of 5 _×_ 10<sup>_−_4</sup> and a per-device batch size of 16. For supervised fine-tuning, we train for 12 epochs with AdamW and an initial learning rate of 1 _×_ 10<sup>_−_4</sup> . Starting from the supervised fine-tuning checkpoint, we further optimize the model for one epoch using Group Relative Policy Optimization. The policy is trained with a learning rate of 1 _×_ 10<sup>_−_6</sup> and a global batch size of 16. To 


Figure 6. Comparison between our VLA-World and the state-of-the-art FSDrive [74] on generating the future frame at next 0.5 seconds. 

Table 5. Evaluation of trajectory planning L2 errors (ST-P3) on nuScenes with varying input view resolutions. 

Table 6. Evaluation of trajectory planning L2 errors (ST-P3) on nuScenes with varying model sizes. 

|**Res.**||**L2 Err**|**or (m)**_↓_||
|---|---|---|---|---|
||1s|2s|3s|Avg.|
|36000|0.03|0.14|0.98|0.38|
|52884|0.11|0.27|0.52|0.30|


|**Method**||**L2 Err**|**or (m)**_↓_||
|---|---|---|---|---|
||1s|2s|3s|Avg.|
|Qwen2-VL-2B|0.11|0.27|0.52|0.30|
|Qwen2.5-VL-3B|0.05|0.08|0.76|0.29|
|Qwen2-VL-7B|0.03|0.03|0.47|0.18|


retain the behavior learned during supervised fine-tuning and ensure stable optimization, we apply a KL divergence regularization term with a coefficient of 1 _×_ 10<sup>_−_2</sup> . For each prompt, we sample 8 candidate responses to estimate the policy gradient. A cosine learning rate scheduler with a warm-up ratio of 0.1 is applied throughout all training stages to stabilize early optimization. We evaluate trajectory planning performance using L2 displacement error and collision rate, following widely adopted protocols in prior work [13, 23, 29, 57, 74]. UniAD [25] computes both metrics at each individual timestep, whereas ST P3 [23] and VAD [13, 29] report the average values over all preceding timesteps. For fair comparison, we follow the respective evaluation strategies of each method. In addition, consistent with recent approaches in generative prediction [59, 61], we adopt the Fréchet Inception Distance to quantify the visual fidelity of synthesized future frames. 

### **B.3. More Discussion** 

**Effectiveness of Input Resolution.** Tab. 5 investigates the sensitivity of our model to input view resolutions. The results demonstrate that higher resolution inputs generally yield better planning performance, particularly over longer time horizons. Although the lower resolution (36 _,_ 000) is competitive at short intervals (1 _s_ ), the higher resolution model (52 _,_ 884) demonstrates superior robustness, achieving the lowest av- 

Table 7. Evaluation of trajectory planning L2 errors (ST-P3) on nuScenes with training strategy. 

|**Method**||**L2 Error (m)**_↓_||
|---|---|---|---|
||1s|2s<br>3s|Avg.|
|w/o. Mixed|0.27|0.47<br>0.73|0.49|
|Qwen2-VL-2B|0.11|0.27<br>0.52|0.30|


erage L2 error of 0 _._ 30m. This indicates that maintaining high-fidelity visual information is crucial for mitigating error accumulation in trajectory prediction. 

**Effectiveness of Model Size.** Tab. 6 presents an ablation study on the effect of model size by varying the backbone among Qwen2-VL-2B, Qwen2.5-VL-3B, and Qwen2-VL7B. The results demonstrate a clear scaling law: increasing the model capacity significantly enhances trajectory planning performance. The Qwen2-VL-7B model achieves state-ofthe-art results with an average L2 error of 0.18m, outperforming the 2B and 3B variants by a substantial margin (approximately 40% relative improvement). This suggests that the stronger reasoning and generalization capabilities inherent in larger parameters are essential for handling the complex causal dependencies in autonomous driving scenarios, particularly for maintaining accuracy over longer time horizons (e.g., reducing 3s error to 0.47m). **Effectiveness of Training Strategy.** In Tab. 7, we conduct 


Figure 7. Comparison of 3-second future trajectory predictions generated by our VLA-World and the state-of-the-art FSDrive [74]. Zoom in for a better view. 

an ablation study to verify the contribution of our multi-task mixed dataset. We compare the full Qwen2-VL-2B model against a baseline trained without mixed data ( _w/o. Mixed_ ). The results reveal that removing the diverse supervision signals leads to a significant performance degradation, with the average L2 error increasing from 0.30m to 0.49m. This substantial gap underscores the critical role of mixed-task 

training (combining perception, reasoning, and planning) in learning robust feature representations, enabling the model to generalize better across varying time horizons. 

### **B.4. More Visualization** 

We visualize the generation and trajectory planning results with the SOTA FSDrive [74]. More visualization results can 

be found in the video demo in our supplementary materials. **Generation Results.** We present a qualitative comparison of the generated 0.5s future frames in Fig. 6. As illustrated by the red-highlighted regions, the baseline method (FSDrive, bottom row) struggles to maintain object coherence during the prediction horizon. It exhibits noticeable artifacts, including geometric distortion of vehicles and a loss of highfrequency details in the background, indicating a lack of robust spatiotemporal constraints. Conversely, VLA-World (top row) demonstrates significantly improved visual fidelity. By effectively leveraging the trajectory-aware conditioning, our model preserves the structural rigidity of dynamic agents and the sharpness of the scene. The generated frames exhibit high photorealism and consistency, validating that our short-term prediction successfully mitigates the _hallucination_ artifacts common in pure VLA. 

**Trajectory Planning.** We provide visualizations of the 3- second future trajectories predicted by VLA-World and FSDrive. As shown in Fig. 7, VLA-World produces noticeably more precise trajectory predictions than FSDrive, especially near the 3-second horizon where the deviation from the ground truth becomes minimal. This improvement stems from our paradigm: first predicting the future state, then generating the corresponding 0.5-second future frames based on that prediction, and finally reasoning over the imagined scene to refine the outcome. In contrast, FSDrive lacks such reflective and iterative reasoning capabilities, which leads to cumulative drift over longer temporal horizons. 

