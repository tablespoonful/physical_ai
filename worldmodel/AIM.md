---
title: "AIM: Intent-Aware Unified world action Modeling with Spatial Value Maps"
date: "2026-04-13"
authors: "Liaoyuan Fan; Zetian Xu; Chen Cao; Wenyao Zhang; Mingqi Yuan; Jiayu Chen"
url: https://arxiv.org/abs/2604.11135
pdf: https://arxiv.org/pdf/2604.11135
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.11135)** / [論文ページ](https://arxiv.org/abs/2604.11135)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **AIM: Intent-Aware Unified world action Modeling with Spatial Value Maps** 

**Liaoyuan Fan**<sup>1</sup><sup>_,_2</sup> **, Zetian Xu**<sup>1</sup><sup>_,_2</sup> **, Chen Cao**<sup>1</sup><sup>_,_2</sup> **, Wenyao Zhang**<sup>3</sup> **, Mingqi Yuan**<sup>1</sup><sup>_,_2</sup> **, Jiayu Chen**<sup>1</sup><sup>_,_2</sup> 

1INFIFORCE Intelligent Technology Co., Ltd., Hangzhou, China 

2The University of Hong Kong, Hong Kong SAR, China 

3Shanghai Jiao Tong University, Shanghai, China 

## **Abstract** 

Pretrained video generation models provide strong priors for robot control, but existing unified world action models still struggle to decode reliable actions without substantial robot-specific training. We attribute this limitation to a structural mismatch: while video models capture how scenes evolve, action generation requires explicit reasoning about where to interact and the underlying manipulation intent. We introduce **AIM** , an intent-aware unified world action model that bridges this gap via an explicit spatial interface. Instead of decoding actions directly from future visual representations, AIM predicts an aligned spatial value map that encodes task-relevant interaction structure, enabling a control-oriented abstraction of future dynamics. Built on a pretrained video generation model, AIM jointly models future observations and value maps within a shared mixture-of-transformers architecture. It employs intent-causal attention to route future information to the action branch exclusively through the value representation. We further propose a self-distillation reinforcement learning stage that freezes the video and value branches and optimizes only the action head using dense rewards derived from projected value-map responses together with sparse task-level signals. To support training and evaluation, we construct a simulation dataset of 30K manipulation trajectories with synchronized multi-view observations, actions, and value-map annotations. Experiments on RoboTwin 2.0 benchmark show that AIM achieves a 94.0% average success rate, significantly outperforming prior unified world action baselines. Notably, the improvement is more pronounced in long-horizon and contact-sensitive manipulation tasks, demonstrating the effectiveness of explicit spatial-intent modeling as a bridge between visual world modeling and robot control. 

## **1 Introduction** 

Pretrained video generation models [23, 20, 4, 7] have emerged as a promising foundation for robot learning because they capture rich visual dynamics, object interactions, and multi-step temporal structure from large-scale video data. In parallel, Vision-Language-Action (VLA) models have shown strong progress in end-to-end robot control by directly mapping visual observations and language instructions to actions [27, 3, 5, 19, 18, 12, 13]. Motivated by the strengths of both lines, recent unified world action models seek to jointly predict future observations and future actions within a single generative framework, offering a path toward general-purpose robot control that combines visual foresight with action generation [26, 6, 1, 11, 22, 23]. 

Despite this promise, decoding reliable actions from such models still requires substantial robotdomain adaptation. We argue that a key limitation is structural rather than purely statistical. Predicting 

Preprint. Under review. 

future RGB frames answers what the scene may look like, but control additionally depends on where the robot should interact and why that interaction is useful for the task. This type of spatially grounded reasoning has long been recognized as important in robotic manipulation [16, 10, 17, 21]. In cluttered manipulation, these signals are sparse, while future RGB representations are dense and dominated by appearance details that are often irrelevant to the next motor command. As a result, action decoding directly from future visual latents forces the model to recover manipulation intent implicitly from a representation that is not optimized for control. 

To bridge this gap, we introduce **AIM** , an intent-aware unified world action model that establishes an explicit spatial interface between future prediction and action generation. Rather than decoding actions directly from future visual representations, AIM predicts an aligned action-based spatial value map that encodes the interaction structure required for task execution. This intermediate representation transforms future scene dynamics into a control-oriented spatial prior, providing a more direct pathway for action generation. Built on a shared pretrained video prior, AIM jointly models future frames and future value maps, while an _intent-causal attention_ mechanism forces the action branch to access future information only through the predicted value map rather than directly through future visual tokens. In this way, the model separates scene evolution from manipulation intent without sacrificing their alignment. 

We further develop a self-distillation RL post-training stage that freezes the video and value branches and optimizes only the action head using dense rewards induced by projected value-map responses together with sparse task-level rewards. To support training and evaluation, we build a largescale simulation dataset with synchronized multi-view videos, action sequences, and value-map annotations. Experiments on the RoboTwin 2.0 benchmark [2] show that explicit spatial intent modeling consistently improves unified world action learning over strong baselines, while also yielding a more interpretable action-generation process through localized stage-wise interaction regions. 

In summary, this work makes three main contributions: 

- **Intent-aware unified world action model.** An explicit spatial value-map interface is introduced between future prediction and action decoding, enabling the model to capture task-relevant interaction structure in a control-oriented form. 

- **A unified training framework for spatially grounded control.** Joint frame-value generation, intent-causal attention, and post-training self-distillation RL are integrated into a single framework that improves action learning without disturbing the prior training video. 

- **Large-scale simulation dataset and strong benchmark performance.** We construct a large-scale simulation dataset of 30K manipulation trajectories with synchronized multi-view videos, actions, and value-map annotations. On the RoboTwin 2.0 benchmark [2], AIM achieves **94.0%** and **92.1%** average success rates under the Easy and Hard settings, respectively, while consistently outperforming prior external baselines. 

## **2 Related Work** 

**Video Generation Model for Robot Learning.** Recent advances in video generation have made pretrained visual dynamics models attractive for robot learning, as they provide transferable priors over motion and long-horizon scene evolution that are difficult to obtain from robot-only data. Following this trend, recent methods increasingly build robot policies on top of pretrained video generators rather than learning world models from scratch [4, 7, 23]. Our work follows this paradigm and adopts Wan2.2-TI2V-5B [20] as the video-generation backbone. 

**Unified World Action Model.** A growing line of work jointly models future observations and actions within a unified architecture [26, 6, 11, 22, 23]. LingBot-VA [6] learns video prediction and action generation in a shared latent space, while GigaWorld-Policy [22] emphasizes action-centered worldaction modeling for efficient control. Fast-WAM [11] further shows that the benefit of world-action modeling may come more from video co-training than explicit future imagination at test time. Our method differs from this line by introducing an explicit spatial intermediate interface between future prediction and action decoding. 

**Spatially Grounded Intermediate Representations.** Spatially grounded representations are useful in robotic manipulation [9] because they localize where interaction should occur. Prior work 

2 


Figure 1: (a) A typical unified world action model decodes actions directly from shared future visual representations. (b) **AIM (Ours)** introduces a spatial value-map interface for action decoding. 

has studied actionable regions and voxel-aligned action spaces [10, 17], while CLIPort [16] and CALAMARI [21] further demonstrate the importance of spatial grounding for object-centric and contact-rich manipulation. In contrast, we integrate spatial value prediction directly into a unified generative world-action model rather than using it as a standalone policy head or auxiliary perception module. 

## **3 Overview** 

**Problem Formulation.** Traditional Vision-Language-Action (VLA) models [12, 13, 19, 18, 5, 27] learn action distributions directly from demonstrations. While effective for imitation, they do not explicitly model how robot actions shape future observations. In contrast, AIM is a pretrained video-based world action model that imagines the near future by jointly modeling visual dynamics and action-relevant intent. We consider manipulation trajectories _τ_ = _{_ ( _ot, at_ ) _}_<sup>_T_</sup> _t_ =1<sup>,where</sup><sup>_ot_</sup> denotes synchronized multi-view observations and _at_ denotes robot actions. Given a history window _Ht_ = _{ot−k_ : _t, at−k_ : _t−_ 1 _}_ , AIM predicts a horizon- _h_ chunk of future RGB frames, spatial value maps, and robot actions, denoted by _X_<sup>+</sup> , _M_<sup>+</sup> , and _A_<sup>+</sup> , respectively. Each future value map _mt ∈_ [0 _,_ 1]<sup>_H×W ×_3</sup> is spatially aligned with the corresponding RGB frame _xt_ and highlights taskrelevant interaction regions, serving as an explicit interface between future world modeling and action generation. We factorize the predictive distribution as 


This factorization reflects the core design of AIM: it first predicts future visual states together with aligned spatial value maps, and then decodes control actions conditioned on the predicted value maps rather than raw future RGB representations. The value map thus serves as the future-facing interface for action generation, bridging visual foresight and control. During deployment, AIM performs autoregressive chunk-wise rollout with a transformer KV cache, appending each newly predicted world-action chunk to the prefix without recomputing the full history. 

**Architecture Overview.** AIM consists of a video generation model, initialized from Wan2.2-TI2V5B [20], and an action head with the same depth but a smaller hidden width for action denoising. Under the mixture-of-transformers design, the two branches share only the self-attention sublayer in each block, while maintaining separate feed-forward transformations. 

At each rollout step, future RGB, value-map, and action tokens are initialized from noise. The video generation model jointly denoises RGB and value-map tokens along the same flow-matching trajectory, decoding them into future RGB observations and aligned spatial value maps, while the action head denoises action tokens into continuous control vectors. The three token streams interact through shared self-attention under a designed mask that allows future world tokens to access observation history while routing future information for action decoding through the valuemap pathway, which we term _intent-causal attention_ . The predicted value map thus serves as an intent-aligned bridge between future world modeling and action generation. 

3 


Figure 2: **Framework of AIM.** Given multi-view RGB videos and a language instruction, AIM jointly learns future frame generation, action prediction, and spatial value map estimation in Stage I, where intent-causal attention transfers task-relevant intention from visual prediction to action generation; in Stage II, the policy is further optimized with GRPO using both sparse and dense rewards. 

## **4 Method** 

We contrast AIM with a representative previous world action model as follows. Traditional WAMs either use a two-stage pipeline in which a video model first predicts the future state and then passes it to an action model, or use a one-stage design in which future state prediction and action prediction are conditioned on the same observation stream. In contrast, AIM augments the video branch with an explicit value-map prediction pathway, so the action model does not need to infer inverse-dynamics cues directly from dense RGB futures. 

### **4.1 Model Architecture** 

**Tokenization.** AIM is built by adapting the pretrained video generation model Wan2.2-TI2V-5B [20] to a world action model setting. To preserve the body of the pretrained video model without redesigning its visual input interface, we follow the multi-view packing strategy used in LingBotVA [6] and merge the three onboard camera views into a single T-pose canvas: the head camera is placed at the top, and the left and right wrist cameras are placed on the corresponding sides. For action representation, we follow the recent trend of improving VLA action token efficiency through structured tokenization design [11]. Let _x_ ˜ _t_ denote the packed RGB observation and _m_ ˜ _t_ denote the packed RGB ASVM at time _t_ . We encode them with the pretrained Wan2.2 VAE encoder _E_ vae as 


where _zt_<sup>_o_areobservationtokensand</sup><sup>_z_</sup> _t_<sup>_m_</sup> are value-map tokens. Each ASVM is aligned with the corresponding future frame and uses the same T-pose layout as the RGB observation. At initialization, the value-map input is a pure black image, so the model starts from a null value prior and predicts the task-relevant spatial structure through denoising. Sharing the VAE between RGB and ASVM 

4 

streams keeps value tokens geometrically aligned with visual tokens without modifying the pretrained tokenizer. 

To align robot control with the visual token space, each dual-arm continuous action vector _at ∈_ R<sup>_da_</sup> is projected by a lightweight MLP _Ea_ into an action token, while the text instruction _c_ is encoded by a pretrained T5 encoder [14] into language tokens: 


These language features are injected only into the Video Model through cross-attention, so task semantics shape future world prediction without directly modifying the action branch. We denote the autoregressive prefix by 


which contains the current and recent observations, recent action history, and instruction tokens. This prefix provides both an estimate of the agent’s physical state and the causal context used for future world action rollout. 

**Architecture.** AIM consists of a _video generation model_ for future RGB and value-map generation, and an _action head_ for future action generation. The video generation model is initialized from Wan2.2, while the action head uses the same depth but a smaller hidden width. At rollout step _t_ , we initialize three future token groups from Gaussian noise, 


where _z_ ˆ0<sup>_x_denotes future RGB tokens,</sup><sup>_z_ˆ</sup> 0<sup>_m_denotes future value-map tokens, and</sup><sup>_z_ˆ</sup> 0<sup>_a_denotes future</sup> action tokens. The value stream additionally receives a learned value noise token _n_<sup>_m_</sup> , so the actual input to the value branch is [ˆ _z_ 0<sup>_m, nm_].Future RGB tokens and future value-map tokens are jointly</sup> denoised by the video generation model along the same flow-matching trajectory [8], while future action tokens are denoised by the action head. Their decoded outputs are 


where _X_<sup>ˆ+</sup> , _M_<sup>ˆ+</sup> , and _A_<sup>ˆ+</sup> are the predicted future RGB frames, spatial value maps, and continuous dual-arm actions, respectively. We adopt a mixture-of-transformers architecture so that action tokens can be tightly coupled with visual tokens while preserving the computational structure of the pretrained backbone. Let _h_<sup>_ℓ_</sup> _s_<sup>denote</sup> the hidden states of stream _s ∈{x, m, a}_ at transformer layer _ℓ_ . Each stream computes its own projections 


which preserve stream-specific feature spaces. These stream-specific queries, keys, and values are then projected to a common attention dimension and participate in a shared masked self-attention operation. The resulting attended features are projected back to each stream and added through residual connections, while the feed-forward transformations remain branch-specific. Language features from T5 are injected only into the video generation model through cross-attention, 


where CA( _·, ·_ ) denotes cross-attention with the instruction tokens. The action head receives task semantics only through the shared world and value representations rather than through direct language conditioning. The overall objective is a weighted sum of the RGB flow-matching loss, the value-map flow-matching loss, and the inverse-dynamics loss for the action head: 


Here _L_ rgb and _L_ map supervise the flow-matching velocity fields for future RGB and value-map denoising, while _L_ act supervises inverse-dynamics action prediction from the action head. At inference time, AIM operates autoregressively and naturally supports KV caching. Only newly appended real observations and newly predicted tokens require fresh attention computation, while all earlier history tokens are reused from the cache, substantially improving long-horizon rollout efficiency. 

5 

### **4.2 Intent-Causal Self-Attention** 

Directly training a generic mixture-of-transformers world action network makes inverse-dynamics learning difficult, because the action head must extract sparse action-relevant cues from dense future RGB appearance generated by the video generation model, especially in cluttered scenes. We address this by jointly modeling future states and their associated value distributions: the video generation model predicts both future RGB frames and future ASVMs, whose value maps provide a more compact and action-relevant representation than raw RGB appearance, making inverse-dynamics learning substantially simpler and more explicit. 

We implement this idea with _intent-causal self-attention_ , a designed visibility mask over the shared self-attention layers. Let _Vx_ , _Vm_ , and _Va_ denote the visible token sets for future video, value, and action streams, respectively: 


Here _z_<sup>_x_</sup> , _z_<sup>_m_</sup> , and _z_<sup>_a_</sup> denote the future video, value, and action tokens being denoised at the current rollout step. The shared masked attention update for stream _s_ is 


followed by the stream-specific residual projection back to the original hidden space. 

This mask has a clear semantic effect. Future video tokens can attend to the current observation, instruction tokens, and past observation and action tokens, so the video generation model predicts task-conditioned future world states. Future value tokens can attend to the current observation, past observations, and future video tokens, ensuring that value prediction remains anchored to the sampled future state. Action tokens can attend to historical action tokens, the current observation, and future value tokens, but not future RGB tokens directly. As a result, task semantics enter the video generation model through T5-conditioned cross-attention, future state information is consolidated into the value stream, and the action head accesses future information only through the predicted value representation. 

### **4.3 Self-Distillation RL Post-Training** 

Supervised training teaches the action head to imitate the action distribution in the dataset, but it does not fully optimize control success under closed-loop execution. We therefore introduce a reinforcement-learning post-training stage that updates only the action head while keeping the video generator and value-map head frozen. This selective finetuning stabilizes the learned visual world model and avoids catastrophic drift in future frame and value-map prediction. 

Let _πϕ_ ( _at | Ht, mt_ +1: _t_ + _h_ ) denote the action head after pretraining. During RL post-training, the model samples actions in the environment and receives two reward components: 


where _rt_<sup>sparse</sup> is the environment-level task success or completion signal, _pt_ is the predicted action landing point or end-effector target, Π( _·_ ) is the camera projection function, and _Mt_ is the predicted value map at time step _t_ . Intuitively, the action head is rewarded when the projected action falls on high-value interaction regions predicted by the frozen value head. 

We optimize only the action head with GRPO [15], of which the objective is 


where _A_<sup>ˆ</sup> _t_ is the advantage estimated from returns under the combined reward _rt_ , and _ϵ_ is the clipping coefficient. Because the dense reward is derived from the model’s own predicted spatial values, this stage can be viewed as a form of self-distillation: the pretrained value head supervises the action head under online interaction without requiring additional human labels. 

6 

**Table 1:** Per-task success rates **SR** on 50 RoboTwin simulation tasks under **Easy** and **Hard** settings. 

|_Simulation Task_|_π_0|_._5|X-V|LA|Mo|tus|Sta|ge1|**AIM**|**(Ours)**|
|---|---|---|---|---|---|---|---|---|---|---|
||Easy|Hard|Easy|Hard|Easy|Hard|Easy|Hard|Easy|Hard|
|_Adjust Bottle_|**100%**|99%|**100%**|99%|89%|93%|98%|99%|**100%**|**100%**|
|<br>_Beat Block Hammer_|96%|93%|92%|88%|95%|88%|98%|**100%**|**100%**|**100%**|
|_Blocks Ranking RGB_|92%|85%|83%|83%|**99%**|97%|91%|77%|92%|77%|
|_Blocks Ranking Size_|49%|26%|67%|74%|**75%**|63%|47%|44%|47%|43%|
|_Click Alarmclock_|98%|89%|99%|99%|**100%**|**100%**|98%|99%|**100%**|**100%**|
|_Click Bell_|99%|66%|**100%**|**100%**|**100%**|**100%**|98%|99%|**100%**|**100%**|
|_Dump Bin Bigbin_|92%<br>|97%<br>|79%<br>|77%<br>|95%<br>|91%<br>|98%|**100%**|**100%**<br>|**100%**<br>|
|_Grab Roller_|**100%**|**100%**|**100%**|**100%**|**100%**|**100%**|98%|99%|**100%**|**100%**|
|_Handover Block_|66%|57%|73%|37%|86%|73%|92%|89%|**93%**|90%|
|_Handover Mic_|**98%**|97%|0%|0%|78%|63%|82%|82%|83%|81%|
|_Hanging Mug_|18%|17%|23%|27%|38%|38%|**43%**|**43%**|**43%**|42%|
|_Lift Pot_|96%|85%|99%|**100%**|96%|99%|98%|**100%**|**100%**|**100%**|
|<br>_Move Can Pot_|51%|55%|89%|86%|34%|74%|99%|97%|**100%**|98%|
|_Move Pillbottle Pad_|84%|61%|73%|71%|93%|96%|97%|**99%**|97%|98%|
|_Move Playingcard Away_|96%|84%|93%|98%|**100%**|96%|98%|**100%**|**100%**|**100%**|
|_Move Stapler Pad_|56%|42%|78%|73%|83%|85%|91%|83%|**92%**|84%|
|_Open Laptop_|90%|96%|93%|**100%**|95%|91%|98%|**100%**|**100%**|**100%**|
|_Open Microwave_|34%|77%|79%|71%|**95%**|91%|83%|80%|83%|79%|
|_Pick Diverse Bottles_|81%|71%|58%|36%|90%|91%|99%|97%|**100%**|98%|
|_Pick Dual Bottles_|93%|63%|47%|36%|**96%**|90%|92%|90%|93%|91%|
|_Place A2B Left_|87%|82%|48%|49%|82%|79%|93%|91%|**94%**|92%|
|_Place A2B Right_|87%|84%|36%|36%|**90%**|87%|89%|89%|**90%**|88%|
|_Place Bread Basket_|77%|64%|81%|71%|91%|**94%**|92%|90%|93%|91%|
|_Place Bread Skillet_|85%|66%|77%|67%|86%|83%|98%|**100%**|**100%**|**100%**|
|_Place Burger Fries_|94%|87%|94%|94%|98%|98%|98%|**100%**|**100%**|**100%**|
|<br>_Place Can Basket_|62%|62%|49%|52%|**81%**|76%|78%|77%|78%|76%|
|_Place Cans Plasticbox_|94%|84%|97%|98%|98%|94%|98%|**100%**|**100%**|**100%**|
|_Place Container Plate_|99%|95%|97%|95%|98%|99%|**100%**|96%|**100%**|97%|
|_Place Dual Shoes_|75%|75%|79%|88%|93%|87%|**100%**|99%|**100%**|98%|
|_Place Empty Cup_|**100%**|99%|**100%**|98%|99%|98%|98%|**100%**|**100%**|**100%**|
|<br>_Place Fan_|87%|85%|80%|75%|91%|87%|**93%**|89%|**93%**|90%|
|_Place Mouse Pad_|60%|39%|70%|70%|66%|68%|**97%**|96%|**97%**|95%|
|_Place Object Basket_|80%|76%|44%|39%|81%|87%|**93%**|88%|**93%**|89%|
|_Place Object Scale_|86%|80%|52%|74%|88%|85%|**100%**|97%|**100%**|98%|
|_Place Object Stand_|91%|85%|86%|88%|98%|97%|98%|**100%**|**100%**|**100%**|
|<br>_Place Phone Stand_|81%|81%|**88%**|87%|87%|86%|82%|81%|82%|80%|
|_Place Shoe_|92%|93%|96%|95%|99%|97%|98%|**100%**|**100%**|**100%**|
|_Press Stapler_|87%|83%|92%|**98%**|93%|**98%**|96%|95%|96%|94%|
|_Put Bottles Dustbin_|**84%**|79%|74%|77%|81%|79%|80%|75%|80%|74%|
|_Put Object Cabinet_|80%|79%|46%|48%|**88%**|71%|81%|75%|81%|74%|
|_Rotate QRcode_|89%|87%|34%|33%|89%|73%|98%|99%|**100%**|98%|
|_Scan Object_|72%|65%|14%|36%|67%|66%|98%|97%|**100%**|98%|
|<br>_Shake Bottle Horizontally_|99%|99%|**100%**|**100%**|**100%**|98%|98%|**100%**|**100%**|**100%**|
|<br>_Shake Bottle_|99%|97%|99%|**100%**|**100%**|97%|98%|**100%**|**100%**|**100%**|
|_Stack Blocks Three_|91%|76%|6%|10%|91%|95%|**100%**|99%|**100%**|98%|
|_Stack Blocks Two_|97%|**100%**|92%|87%|**100%**|98%|98%|**100%**|**100%**|**100%**|
|_Stack Bowls Three_|77%|71%|76%|86%|79%|87%|**100%**|99%|**100%**|98%|
|_Stack Bowls Two_|95%|96%|96%|93%|98%|98%|**100%**|97%|**100%**|98%|
|_Stamp Seal_|79%|55%|76%|82%|93%|92%|**100%**|**100%**|**100%**|**100%**|
|_Turn Switch_|62%|54%|40%|61%|84%|78%|**100%**|99%|**100%**|98%|
|**Average**|82.74%|76.76%|72.80%|72.84%|88.66%|87.02%|93.0%|92.0%|**94.0%**|**92.1%**|


7 

Table 2: RoboTwin 2.0 average success rate **<u>(SR)</u>** under **Easy** and **Hard** settings. 

|Setting|_π_0|_π_0_._5|X-VLA|Motus|Fast-WAM|Giga-World|LingBot-VA|Stage1|**AIM (Ours)**|
|---|---|---|---|---|---|---|---|---|---|
|Easy|65.9%|82.7%|72.8%|88.7%|91.9%|87.0%|92.9%|93.0%|**94.0%**|
|Hard|58.4%|76.8%|72.8%|87.0%|91.8%|85.0%|91.6%|92.0%|**92.1%**|
|Average|62.2%|79.8%|72.8%|87.8%|91.8%|86.0%|92.2%|92.5%|**93.1%**|


## **5 Dataset and Value-Map Annotation** 

**Large-Scale Simulation Dataset.** We build a large-scale simulation dataset of 30K manipulation trajectories collected on RoboTwin 2.0 Benchmark [2]. Each trajectory contains synchronized multi-view videos, action sequences, task identifiers, and per-step value-map annotations. 

A simulation-only setting is well-suited to our study for two reasons. First, it provides the scale needed for training unified world-action models while supporting automatic label generation from contact events and physics states. Second, it offers precise geometric information and controllable scene diversity, enabling consistent value-map annotation across tasks, viewpoints, and object configurations. This setting allows us to study spatially grounded world-action modeling under controlled conditions at scale. 

**Pick Value-Map Annotation.** For pick tasks, we record the contact surface point cloud when the gripper establishes effective grasp contact with the target object. The simulator’s contact-detection API provides a set of contact vertices on the interacting surfaces. We project these points into the image plane using the calibrated camera projection matrix and then apply Gaussian smoothing to obtain a continuous-value heat map. This annotation marks the _grasp affordance region_ : the spatial area where the object and end-effector engage in successful physical interaction. The Gaussian kernel width is adjusted dynamically according to camera parameters and the distance between the projected point and the camera, so that the label maintains a meaningful image-space support size across different viewpoints and depths. 

**Place Value-Map Annotation.** For place tasks, we detect placement completion when the manipulated object reaches a stable configuration, defined by a small center-of-mass velocity threshold. We then extract the contact region between the grasped object and the target support surface, project the contact area into the image plane, and generate a placement feasibility heat map. This map marks the _placement contact region_ : the spatial location where the held object should make contact with the environment to satisfy the placement goal. 

## **6 Experiments** 

**Experimental Setup.** We evaluate AIM on 50 RoboTwin simulation tasks under Easy and Hard settings. Unless otherwise noted, all models are trained on the same 30K RoboTwin simulation dataset and evaluated under identical task definitions and success criteria. The video generation model is initialized from Wan2.2-TI2V-5B [20]. 

**Baselines and Metrics.** We select _π_ 0 _._ 5 [13], X-VLA [25], and Motus [1] as our baselines, and additionally report Stage1, our supervised model before RL post-training, to isolate the effect of self-distillation. We use success rate ( **SR** ) as the primary metric. During RL post-training, the action head is initialized from the Stage1 checkpoint, while the video generation model and value-map head remain frozen. 

**Main Results and Analysis.** As shown in Table 1, AIM achieves average SRs of **94.0%** and **92.1%** under the Easy and Hard settings, respectively, outperforming all external baselines [25, 12, 13, 1, 24, 22, 6]. In particular, compared with Motus [1], AIM improves the average SR by **+5.3%** and **+5.0%** under Easy and Hard setting, respectively; compared with _π_ 0 _._ 5 [13], the gains increase to **+11.3%** and **+15.3%** . Stage 1 reaches **93.0%** / **92.0%** , indicating that RL post-training brings further improvement. The largest gains in Table 1 appear on contact-sensitive and stage-dependent tasks, such as _Place Mouse Pad_ ( **97%** / **95%** ), _Scan Object_ ( **100%** / **98%** ), and _Turn Switch_ ( **100%** / **98%** ), where accurate localization of task-relevant interaction regions is critical. This trend is also supported qualitatively: future frame predictions remain temporally aligned with the manipulation stage, value 

8 


Figure 3: Representative task execution processes in Robotwin 2.0 benchmark [2], including _place mouse pad_ , _press stapler_ , _scan object_ , _turn switch_ , and _open laptop_ . The left column shows examples under **Easy** setting, while the right column shows examples under **Hard** setting. 

maps concentrate on meaningful interaction regions rather than generic saliency, and projected action targets fall within the corresponding high-value areas, suggesting that the gains indeed come from the intended spatial bridge rather than shortcut correlations. 

## **7 Conclusion** 

This paper presented AIM, an intent-aware unified world-action model that bridges future video generation and robot action decoding with explicit spatial value maps. Built on a pretrained video generator and a mixture-of-transformers architecture, AIM jointly predicts future frames, future value maps, and future actions, while intent-causal attention ensures that future information reaches the action head only through the intent-aligned value representation. We further introduced a selfdistillation RL post-training strategy that freezes the video generation model and value branch and updates only the action head using dense rewards derived from projected value-map responses. 

Together with a 30K simulation dataset and evaluation on 50 RoboTwin 2.0 [2] simulation tasks, these designs provide a coherent framework for studying spatially grounded world-action modeling. AIM achieves strong performance on the RoboTwin benchmark and consistently outperforms prior external baselines, showing that explicit spatial value modeling is a practical and effective bridge between RGB world modeling and robot action generation. 

9 

## **References** 

- [1] Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan Wang, Shuhe Huang, Haitian Liu, Ruowen Zhao, Jun Zhu, et al. Motus: A unified latent action world model, 2025. URL `https: //arxiv.org/abs/2512.13030` . 

- [2] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 

- [3] Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, et al. Palm-e: An embodied multimodal language model. In _Proceedings of the 40th International Conference on Machine Learning_ , 2023. 

- [4] Yucheng Hu, Yanjiang Guo, Pengchao Wang, Xiaoyu Chen, Yen-Jen Wang, Jianke Zhang, Koushil Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy with predictive visual representations. _arXiv preprint arXiv:2412.14803_ , 2024. 

- [5] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [6] Lin Li, Qihang Zhang, Yiming Luo, Shuai Yang, Ruilin Wang, Fei Han, Mingrui Yu, Zelin Gao, Nan Xue, Xing Zhu, Yujun Shen, and Yinghao Xu. Causal world modeling for robot control. _arXiv preprint arXiv:2601.21998_ , 2026. 

- [7] Junbang Liang, Pavel Tokmakov, Ruoshi Liu, Sruthi Sudhakar, Paarth Shah, Rares Ambrus, and Carl Vondrick. Video generators are robot policies. _arXiv preprint arXiv:2508.00795_ , 2025. 

- [8] Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2023. 

- [9] Bingchen Miao, Rong Wei, Zhiqi Ge, Xiaoquan Sun, Shiqi Gao, Jingzhe Zhu, Renhan Wang, Siliang Tang, Jun Xiao, Rui Tang, and Juncheng Li. Towards physically executable 3d gaussian for embodied navigation, 2025. URL `https://arxiv.org/abs/2510.21307` . 

- [10] Kaichun Mo, Leonidas J. Guibas, Mustafa Mukadam, Abhinav Gupta, and Shubham Tulsiani. Where2act: From pixels to actions for articulated 3d objects. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 6813–6823, 2021. 

- [11] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- [12] Physical Intelligence, Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A VisionLanguage-Action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [13] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: A VisionLanguage-Action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- [14] Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J. Liu. Exploring the limits of transfer learning with a unified text-to-text transformer. _Journal of Machine Learning Research_ , 21(140):1–67, 2020. 

10 

- [15] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 

- [16] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Cliport: What and where pathways for robotic manipulation. In _Proceedings of the 5th Conference on Robot Learning_ , volume 164 of _Proceedings of Machine Learning Research_ , pages 894–906, 2022. 

- [17] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Perceiver-actor: A multi-task transformer for robotic manipulation. In _Proceedings of The 6th Conference on Robot Learning_ , pages 785–799, 2023. 

- [18] Wenxuan Song, Jiayi Chen, Xiaoquan Sun, Huashuo Lei, Yikai Qin, Wei Zhao, Pengxiang Ding, Han Zhao, Tongxin Wang, Pengxu Hou, Zhide Zhong, Haodong Yan, Donglin Wang, Jun Ma, and Haoang Li. Rethinking the practicality of vision-language-action model: A comprehensive benchmark and an improved baseline. _arXiv preprint arXiv:2602.22663_ , 2026. 

- [19] Xiaoquan Sun, Zetian Xu, Chen Cao, Zonghe Liu, Yihan Sun, Jingrui Pang, Ruijian Zhang, Zhen Yang, Kang Pang, Dingxin He, et al. Atomvla: Scalable post-training for robotic manipulation via predictive latent world models. _arXiv preprint arXiv:2603.08519_ , 2026. 

- [20] Team Wan, Ang Wang, Baole Ai, Bin Wen, Chaojie Mao, Chen-Wei Xie, Di Chen, and Feiwu Yu. Wan: Open and advanced large-scale video generative models. _arXiv preprint arXiv:2503.20314_ , 2025. 

- [21] Youngsun Wi, Mark Van der Merwe, Pete Florence, Andy Zeng, and Nima Fazeli. Calamari: Contact-aware and language conditioned spatial action mapping for contact-rich manipulation. In _Proceedings of The 7th Conference on Robot Learning_ , volume 229 of _Proceedings of Machine Learning Research_ , pages 2753–2771, 2023. 

- [22] Angen Ye, Boyuan Wang, Chaojun Ni, Guan Huang, Guosheng Zhao, Hao Li, Hengtao Li, Jie Li, Jindi Lv, Jingyu Liu, Min Cao, and Peng Li. Gigaworld-policy: An efficient action-centered world–action model. _arXiv preprint arXiv:2603.17240_ , 2026. 

- [23] Seonghyeon Ye, Yunhao Ge, Kaiyuan Zheng, Shenyuan Gao, Sihyun Yu, George Kurian, Suneel Indupuru, You Liang Tan, Chuning Zhu, Jiannan Xiang, et al. World action models are zero-shot policies. _arXiv preprint arXiv:2602.15922_ , 2026. 

- [24] Tianyuan Yuan, Zibin Dong, Yicheng Liu, and Hang Zhao. Fast-wam: Do world action models need test-time future imagination? _arXiv preprint arXiv:2603.16666_ , 2026. 

- [25] Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, Yuchun Feng, Yinan Zheng, Jiayin Zou, Yilun Chen, Jia Zeng, et al. X-vla: Soft-prompted transformer as scalable cross-embodiment vision-language-action model. _arXiv preprint arXiv:2510.10274_ , 2025. 

- [26] Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin Burchfiel, Paarth Shah, and Abhishek Gupta. Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets. _arXiv preprint arXiv:2504.02792_ , 2025. 

- [27] Brianna Zitkovich, Nikhil Joshi, Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, et al. Rt-2: Visionlanguage-action models transfer web knowledge to robotic control. In _Proceedings of The 7th Conference on Robot Learning_ , pages 2165–2183, 2023. 

11 

