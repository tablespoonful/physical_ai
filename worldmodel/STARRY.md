---
title: "STARRY: Spatial-Temporal Action-Centric World Modeling for Robotic Manipulation"
date: "2026-04-29"
authors: "Yuxuan Tian; Yurun Jin; Bin Yu; Yukun Shi; Hao Wu; Chi Harold Liu"
url: https://arxiv.org/abs/2604.26848
pdf: https://arxiv.org/pdf/2604.26848
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.26848)** / [論文ページ](https://arxiv.org/abs/2604.26848)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **STARRY: Spatial-Temporal Action-Centric World Modeling for Robotic Manipulation** 

**Yuxuan Tian**<sup>**1,2**</sup> **Yurun Jin**<sup>**3,4**</sup> **Bin Yu**<sup>**2,5**</sup> **Yukun Shi**<sup>**3**</sup> **Hao Wu**<sup>**2,6**</sup> **Chi Harold Liu**<sup>**1**</sup><sup>_∗_</sup> **Kai Chen**<sup>**2,3,7**</sup><sup>_∗†_</sup> **Cong Huang**<sup>**2,3**</sup><sup>_∗_</sup> 

1Beijing Institute of Technology 2Zhongguancun Academy 

3Zhongguancun Institute of Artificial Intelligence 

4University of Science and Technology of China 5Harbin Institute of Technology 6East China Normal University 7DeepCybo 

## **Abstract** 

Robotic manipulation requires reasoning about future spatial-temporal interactions and geometric constraints, yet existing Vision-Language-Action (VLA) policies often leave predictive representation weakly coupled with action execution, causing failures in tasks requiring precise spatial-temporal coordination. We propose **STARRY** , a world-model-enhanced action-generation policy that aligns spatialtemporal prediction and action generation by jointly denoising future spatialtemporal latents and actions through a unified diffusion process. To bridge 2D visual tokens and 3D metric control, STARRY introduces Geometry-Aware Selective Attention Modulation (GASAM), which converts predicted depth and end-effector geometry into token-aligned weights for selective action-attention modulation. On RoboTwin 2.0, STARRY achieves **93.82%** / **93.30%** average success under Clean and Randomized settings across 50 bimanual tasks. Real-world experiments show that STARRY improves average success from **42.5%** to **70.8%** compared with _π_ 0 _._ 5. These results demonstrate the effectiveness of action-centric spatial-temporal world modeling for spatially and temporally demanding robotic manipulation. 

## **1 Introduction** 

Vision-Language-Action (VLA) models have emerged as a prominent paradigm for general-purpose embodied agents by unifying perception, language, and action [7, 6, 13, 44]. Although large-scale vision-language pretraining provides strong semantic understanding and instruction following, many VLA policies remain _reactive_ , primarily relying on current or short-history observations without explicitly modeling future robot-object interaction states [25]. This limits language-conditioned manipulation, where tasks such as hanging a mug, handover, or container placement require anticipating object geometry, contact regions, and end-effector trajectories. Errors in these local relations can cause unstable grasps, collisions, or failed placements. 

Recent work incorporates world models into policy learning by predicting future observations or latent video states, leading to _world-model-enhanced action-generation policies_ [5, 19, 43, 9, 35]. Nevertheless, future prediction alone does not necessarily yield better control: visually plausible futures may still fail to expose action-relevant spatial constraints such as object handles, contact surfaces, openings, obstacles, and the neighborhood around the end effector. 

We identify two common limitations in many existing predictive manipulation policies. First, their future representations are often optimized for perceptual or temporal consistency rather than action 

> _∗_ Corresponding authors 

> _†_ Project leader 

Preprint. 

relevance, creating a mismatch between prediction and control [23, 36]. Second, spatial information is usually fused through globally shared representations, making it difficult to distinguish decisioncritical regions from background context [9, 40, 37]. As a result, the predictive capability of world models may not be fully converted into effective action generation, especially in contact-rich or spatially constrained tasks where local spatial-temporal relations matter. 

Our key insight is that world models for manipulation should be both _action-centric_ and _geometrygrounded_ : they should predict not only how the scene evolves, but also where future interactions are critical for action generation. Based on this insight, we propose **STARRY** ( **S** patial- **T** emporal **A** ction-centric **R** epresentation and **R** easoning Polic **Y** ), a **world-model-enhanced action-generation policy** for robotic manipulation. STARRY jointly denoises future spatial-temporal latent variables and action sequences within a unified generative policy, aligning future prediction with action generation. To further incorporate geometric guidance, we introduce **Geometry-Aware Selective Attention Modulation** (GASAM), which uses predicted geometry to emphasize action-relevant visual tokens in the action attention branch while preserving video modeling and semantic understanding. 

### **Our contributions are summarized as follows:** 

- We propose **STARRY** , a world-model-enhanced action-generation policy that jointly models future spatial-temporal dynamics and action sequences, enabling action-centric spatialtemporal modeling for language-conditioned robotic manipulation. 

- We introduce **Geometry-Aware Selective Attention Modulation** (GASAM), which converts predicted depth and end-effector geometry into token-aligned weights and selectively injects them into the action attention branch to emphasize decision-critical regions. 

- We validate STARRY through simulation and real-world experiments. On RoboTwin 2.0, it achieves **93.82% / 93.30%** average success under Clean and Randomized settings, while real-world experiments and ablations confirm the benefits of spatial-temporal modeling and GASAM. 

## **2 Related work** 

### **2.1 Vision-Language-Action policies** 

Vision-Language-Action (VLA) models unify perception, language, and action, forming a dominant paradigm for embodied manipulation [6, 13]. Representative works such as RT-2 and _π_ 0 _._ 5 leverage large-scale vision-language pretraining to learn rich semantic representations, enabling direct mapping from multi-modal inputs to action outputs [8, 44, 2, 20, 7, 6]. However, most VLA policies remain _reactive_ , mapping observations directly to actions without explicitly modeling future states, limiting their ability to leverage temporal foresight for action generation [25]. In addition, existing methods are largely 2D-centric and lack explicit geometric reasoning, relying primarily on appearance-based features, which restricts performance in spatially constrained tasks [29]. 

### **2.2 World models and predictive learning** 

World models learn environment dynamics to support prediction and decision-making [23]. Recent advances span latent predictive learning (e.g., JEPA), which focuses on learning temporally consistent representations, and large-scale generative models such as DreamDojo and WoW that model future observations from video or interaction data [4, 15, 12, 35]. Unified architectures further couple video and action modeling for scalable policy learning. Despite strong predictive capabilities, these models often exhibit a gap between prediction quality and control utility [31], as they primarily optimize perceptual fidelity rather than action relevance, and emphasize temporal dynamics with limited modeling of spatial geometry. 

### **2.3 World-model-enhanced action generation** 

Recent work integrates world models into action generation by leveraging predicted futures for policy learning. Representative approaches include foresight-based action prediction (e.g., F1), which formulates action generation as a prediction-guided inverse dynamics problem, and unified videoaction modeling frameworks such as Motus that jointly learn latent representations for perception and 

2 


Figure 1: Overview of **STARRY** . The policy contains four modules: _Understanding Expert_ , _SpatialTemporal (ST) World Model_ , _Geometry Expert_ , and _Action Expert_ . The _ST World Model_ predicts future spatial-temporal latent variables, while the _Geometry Expert_ and GASAM generate geometryaware weights to selectively modulate the action branch. 

control [25, 5, 42]. While these methods improve temporal consistency and multi-modal integration, they provide limited modeling of spatial geometry and lack mechanisms for selectively emphasizing action-relevant regions. 

Our work addresses the above gap by learning action-centric spatial-temporal representations and introducing geometry-aware selective modulation for more effective action generation [39, 11]. 

## **3 STARRY: Spatial-Temporal Action-Centric Representation and Reasoning** 

We propose **STARRY** , a world-model-enhanced action-generation policy for embodied manipulation that jointly models future temporal dynamics and spatial geometry for action generation. We first present the overall architecture (Sec. 3.1), followed by the _ST World Model_ (Sec. 3.2), the GeometryAware Selective Attention Modulation mechanism (Sec. 3.3), and the model training and data construction (Sec. 3.4). 

### **3.1 Architecture overview** 

**Problem formulation.** We consider language-conditioned embodied manipulation, where the agent observes **o** _t_ = _{_ **I** _t,_ **D** _t,_ **c** _t,_ **p** _t,_ **l** _}_ at time step _t_ , including multi-view RGB-D observations _{_ **I** _t,_ **D** _t}_ , camera parameters **c** _t_ , current pose **p** _t_ , and the language instruction **l** . The goal is to generate a future action sequence **a** _t_ +1: _t_ + _H_ . Instead of directly mapping **o** _t_ to actions, STARRY introduces two internal structures: a future spatial-temporal latent variable **z** _t_ +1: _t_ + _H_ and geometry-aware modulation weights **w** _t_ +1: _t_ + _H_ . The future latents and actions are jointly modeled as 


Here, **z** _t_ +1: _t_ + _H_ captures predictive spatial-temporal structure aligned with action generation, while **w** _t_ +1: _t_ + _H_ is generated from predicted future geometry and used to inject action-relevant spatial constraints into the action branch. 

**Architecture.** As shown in Fig. 1, STARRY consists of four modules: the _Understanding Expert_ , _Spatial-Temporal (ST) World Model_ , _Geometry Expert_ , and _Action Expert_ . The core design is 

3 


Figure 2: Construction of spatial-temporal inputs for the _ST World Model_ . Multi-modal signals, including RGB observations, depth observations, and end-effector trajectories, are unified into a shared representation capturing appearance, geometry, and motion, which is then used for future spatial-temporal prediction. 

that future spatial-temporal latents and actions are jointly denoised over the same horizon, while geometry-aware weights are selectively applied only to the action attention branch. 

Concretely, the _Understanding Expert_ provides semantic grounding from visual-language inputs, while the _ST World Model_ and _Action Expert_ jointly denoise future spatial-temporal latents **z** _t_ +1: _t_ + _H_ and actions **a** _t_ +1: _t_ + _H_ through Multi-modal Joint Attention. In parallel, the _Geometry Expert_ predicts future geometric states, which GASAM converts into token-aligned weights **w** _t_ +1: _t_ + _H_ to selectively modulate the action attention branch. This enables action-relevant spatial reasoning while preserving video modeling and visual-language understanding. 

### **3.2 ST World Model** 

Existing world-model-enhanced policies typically use future observation or latent video prediction to improve temporal coherence in action generation. However, appearance-level or temporally consistent futures do not necessarily encode the spatial relations that determine manipulation success, such as end-effector motion, object geometry, and contact-relevant regions. The _Spatial-Temporal (ST) World Model_ addresses this by learning a unified future spatial-temporal latent variable **z** _t_ +1: _t_ + _H_ that integrates appearance, motion, and geometry, as shown in Fig. 2. This representation provides structured future information that is directly shared with action generation. 

Given observations within a temporal window [ _t_ 0 _, t_ ], we construct a unified spatial-temporal representation from multi-view RGB images _{_ **I**<sup>_c_</sup> _t_<sup>_}c_,depth observations</sup><sup>_{_</sup><sup>**D**</sup><sup>_c_</sup> _t_<sup>_}c_,and 3D end-effector</sup> trajectories _{_ **e**<sup>_m_</sup> _τ_<sup>_}τ≤t,m_.We first project trajectories into each camera view using camera intrinsics</sup> _K_ and extrinsics _T_ : _Ct_<sup>_c_=</sup><sup>_{K_</sup> _t_<sup>_c, T_</sup> _t_<sup>_c}_, and then compose appearance, geometry, and motion into a</sup> unified representation: 


Here, Π( _·_ ) denotes camera projection, and Φ( _·_ ) denotes the spatial-temporal composition function, which arranges the multi-view RGB frames, depth observations, and projected trajectories into a fixed RGB-D layout. The resulting sequence **X** _t_ 0: _t_ = _{_ **x** _t_ 0 _, . . . ,_ **x** _t}_ provides a structured description of past spatial-temporal states. 

We encode **X** _t_ 0: _t_ into video tokens **v** _t_ 0: _t_ and combine them with historical actions **a** _≤t_ to predict future latent variables: 


Here, _fθ_<sup>ST</sup> is implemented as a diffusion-based model. By explicitly integrating appearance, trajectory, and geometry in the input representation, **z** _t_ +1: _t_ + _H_ captures structured spatial-temporal information, including scene evolution, end-effector motion, and geometric constraints, providing effective conditioning for action generation. 

4 


Figure 3: Geometry-aware weight construction and modulation in GASAM. Rows (a)–(c) show observations, geometry-aware weights, and their overlays across selected temporal steps. The constructed weights highlight geometrically action-relevant regions for action-attention modulation. 

### **3.3 Geometry-Aware Selective Attention Modulation** 

Although the _ST World Model_ provides future spatial-temporal latents, action generation still requires explicit alignment between 2D visual tokens and 3D physical control. Standard joint attention matches action tokens with 2D visual tokens through query-key dot products in token space, forcing the policy to infer perspective and depth relations implicitly. This may cause large 3D control deviations when visual similarity does not reflect metric distance. To bridge this gap, we propose _Geometry-Aware Selective Attention Modulation_ (GASAM), which uses predicted depth and end-effector geometry to lift 2D visual tokens into metric 3D space, thereby explicitly aligning visual observations with physical control. 

**Geometry prediction.** While future latent variables **z** _t_ +1: _t_ + _H_ capture future spatial-temporal structure, they remain latent and noise-dependent during denoising, making them unsuitable for direct geometric operations such as depth unprojection or end-effector–scene distance computation. To obtain stable and interpretable spatial guidance, we introduce a _Geometry Expert_ . Conditioned on **o** _t_ , video tokens **v** _t_ 0: _t_ , historical actions **a** _≤t_ , and diffusion timesteps ( _τv, τa_ ) that indicate the noise levels of the video and action branches, it predicts future depth sequences **D**<sup>ˆ</sup> _t_ +1: _t_ + _H_ and end-effector positions **p** ˆ _t_ +1: _t_ + _H_ : 


where _gϕ_ denotes the _Geometry Expert_ . This design provides a stable and explicit estimate of future geometry, which complements the implicit latent modeling in **z** _t_ +1: _t_ + _H_ and serves as guidance for geometry-aware action modulation. 

**Geometry-aware weight construction and modulation.** To make attention aware of metric spatial relations, GASAM measures how close each visual location is to the predicted end-effector in 3D space. Given the predicted geometry, GASAM first recovers 3D points **P**<sup>ˆ</sup> _t,j_ from the predicted depth **D** ˆ _t_ using camera parameters, and computes their distances to the predicted end-effector position: 


The distances are converted into geometry-aware weights and aligned to the video-token grid: 


where _ρ_ ( _·_ ) denotes a monotonically decreasing distance-to-weight mapping, and _T_ ( _·_ ) samples or aggregates the resulting pixel-level weights onto the video-token grid. As shown in Fig. 3, the constructed geometry-aware weights highlight spatial regions that are geometrically relevant to action execution and provide the modulation signal for the action attention branch. 

GASAM then uses **w** _t_ +1: _t_ + _H_ to modulate action-to-video attention. Let **Q**<sup>_a_</sup> denote action queries, and let **K**<sup>_v_</sup> and **V**<sup>_v_</sup> denote video keys and values. The geometry-modulated action-to-video attention is: 


5 

Here, _λ_ controls the modulation strength and _ϵ_ avoids numerical instability. Since log( **w** _t_ +1: _t_ + _H_ + _ϵ_ ) is added before the softmax, GASAM directly biases the attention weights from action queries to visual tokens toward geometrically relevant regions. The modulation is applied only to the action branch, allowing geometry to guide action selection while preserving the original spatial-temporal modeling and visual-language understanding. 

### **3.4 Training and data** 

**Initialization and diffusion objective.** We initialize the _ST World Model_ from Wan [18, 30, 28, 34] and the _Understanding Expert_ from Qwen-VL [3]. The _Action Expert_ follows the same Transformer architecture as the _ST World Model_ but uses action-specific parameters, while the _Geometry Expert_ is implemented as a diffusion-aligned Transformer operating on the same video and action tokens to predict future geometry. We jointly model spatial-temporal observations **x** and actions **a** via diffusion by predicting velocity fields [17, 32, 24, 11]: 


where **_ϵ_** _o_ and **_ϵ_** _a_ denote Gaussian noise, and **v** _θ_<sup>_o_and</sup><sup>**v**</sup> _θ_<sup>_a_are the predicted velocity fields.Different</sup> diffusion time steps ( _τv, τa_ ) are used for observations and actions to account for modality differences. The overall loss is: 


**Geometry supervision.** The _Geometry Expert_ is supervised on depth, end-effector position, and geometry-aware weights: 


where _L_ depth supervises depth prediction, _L_ pose constrains the 3D end-effector position, and _L_ weight enforces consistency between predicted modulation weights and geometry-derived targets. 

The target weights are constructed from ground-truth spatial distances: 


where _wt,j_<sup>_∗_is derived from the distance between the end-effector and scene points, providing direct</sup> supervision for geometry-aware attention modulation. 

The _Geometry Expert_ is first trained independently and then jointly fine-tuned, influencing action generation through GASAM rather than directly modifying the diffusion objective. 

**Training pipeline.** We adopt a three-stage training strategy: 

**Stage 1 (spatial-temporal pretraining):** train the _ST World Model_ and _Understanding Expert_ on large-scale video and multi-modal data to learn spatial-temporal dynamics and semantic representations. 

**Stage 2 (action and geometry learning):** introduce the _Geometry Expert_ and _Action Expert_ for joint training under the diffusion objective, enabling mapping from spatial-temporal representations to actions with geometric constraints. 

**Stage 3 (joint finetuning):** perform end-to-end finetuning with GASAM, allowing all modules to be optimized jointly for improved spatial-temporal consistency and action generation. 

**Dataset.** As shown in Table 1, we organize data hierarchically to progressively introduce semantic, temporal, geometric, and action supervision. L1–L2 use large-scale web and egocentric videos, such as Ego4D [16] and Ego-Dex [38], to learn general visual features and temporal dynamics. L3–L4 introduce geometry-enriched data with depth and multi-view observations, such as EmbodiedMAE [14], for explicit spatial structure modeling. L5–L6 further incorporate real robot datasets [26, 21, 33, 27], such as DROID and BridgeData V2, for action learning, with L6 finetuned on target-robot data for task-specific adaptation. 

6 

Table 1: Hierarchical data organization for STARRY. 

|Level|Data Type|Language|Video|Geometry|Action|
|---|---|---|---|---|---|
|L1|Web-scale video|✓|✓|||
|L2|Egocentric video|✓|✓|||
|L3|Synthetic / simulation|✓|✓|✓||
|L4|Interaction data|✓|✓|✓|✓|
|L5|Multi-robot trajectories|✓|✓|✓|✓|
|L6|Target-robot data|✓|✓|✓|✓|


Table 2: Selected RoboTwin 2.0 results under Clean and Randomized settings. 

|Tk|_π_0|_._5|X-V|LA|Mo|tus|LingB|ot-VA|O|urs|
|---|---|---|---|---|---|---|---|---|---|---|
|as|Clean|Rand.|Clean|Rand.|Clean|Rand.|Clean|Rand.|Clean|Rand.|
|Click Alarmclock|97.5%|91%|99%|99%|**100%**|**100%**|99%|**100%**|**100%**|**100%**|
|Handover Mic|63%|57.5%|0%|0%|78%|63%|94%|96%|**100%**|**99%**|
|Hanging Mug|10.5%|10%|23%|27%|38%|38%|40%|28%|**69%**|**72%**|
|Move Can Pot|40%|41%|89%|86%|34%|74%|94%|97%|**100%**|**98%**|
|Move Pillbottle Pad|58.5%|45%|73%|71%|93%|96%|99%|99%|**100%**|**100%**|
|Pick Diverse Bottles|43%|37%|58%|36%|90%|91%|89%|82%|**98%**|**96%**|
|Place Bread Basket|62.5%|60%|81%|71%<br>_...... (50_|91%<br>_tasks)_|94%|97%|95%|**100%**|**99%**|
|Place Can Basket|40.5%|43.5%|49%|52%|81%|76%|81%|84%|**89%**|**88%**|
|Place Shoe|74.5%|77%|96%|95%|99%|97%|98%|98%|**100%**|**99%**|
|Press Stapler|83.5%|76.5%|92%|98%|93%|98%|85%|82%|**100%**|**100%**|
|Put Bottles Dustbin|48%|44%|74%|77%|81%|79%|87%|91%|**96%**|**93%**|
|Stack Blocks Three|53%|46%|6%|10%|91%|95%|**99%**|98%|97%|**100%**|
|Turn Switch|33.5%|30%|40%|61%|84%|78%|44%|45%|**85%**|**89%**|
|Average|62.86%|60.30%|72.80%|72.84%|88.66%|87.02%|92.93%|91.55%|**93.82%**|**93.30%**|


## **4 Experiments** 

We evaluate STARRY in simulation and real-world settings. Specifically, we test on RoboTwin 2.0 under Clean and Randomized settings (Sec. 4.1), examine physical execution in real-world experiments (Sec. 4.2), and conduct ablations to analyze the effects of spatial-temporal prediction and GASAM (Sec. 4.3). 

### **4.1 Evaluation in simulation environment** 

**RoboTwin 2.0** We first evaluate STARRY on the RoboTwin 2.0 benchmark, which comprises 50 bimanual manipulation tasks with structured domain randomization [10]. In the main paper, we compare against _π_ 0 _._ 5 [6], X-VLA [41], Motus [5], and LingBot-VA [22]. For each task, we use 50 demonstrations under the Clean setting and 500 demonstrations under the Randomized setting. Demonstrations from all 50 tasks are pooled together and jointly optimized, rather than training each task independently. All models are trained with a batch size of 256 for 40k steps. To save space, additional baselines, including GO-1 [1] and _π_ 0 [7], together with full per-task results on all 50 tasks, are provided in Appendix B.2. 

Overall, STARRY achieves the best average success rates under both Clean and Randomized settings, reaching 93.82% and 93.30%, respectively, surpassing LingBot-VA (92.93% / 91.55%) and Motus (88.66% / 87.02%). Notably, these average gains underestimate the advantage on challenging tasks, since many easier tasks are close to saturation for multiple methods. On more discriminative tasks, the improvements of STARRY align closely with our design. For example, on _Handover Mic_ , which requires precise temporal coordination in bimanual handover, STARRY achieves 100% / 99%, significantly outperforming Motus (78% / 63%), suggesting that spatial-temporal world modeling better supports anticipation of future interaction states. On tasks that rely on local geometric structure, contact location, and fine-grained alignment, such as _Hanging Mug_ , _Turn Switch_ , and _Press Stapler_ , STARRY obtains 69% / 72%, 85% / 89%, and 100% / 100%, respectively. In particular, on _Hanging Mug_ , STARRY improves the previous best result by more than 30 points, indicating that GASAM helps focus action generation on geometry-relevant regions. We also observe consistent gains on tasks involving object selection, container relations, and placement constraints, including _Move Can_ 

7 


Figure 4: Real-world task settings. We evaluate three representative two-stage bimanual manipulation tasks: _Hand Over Vegetables_ , _Tidy Up Room_ , and _Wash Baby Bottle_ . 

Table 3: Success rates (%) in real-world experiments. 

|Method|Hand Over<br>Stage 1|Vegetables<br>Stage 2|Tidy<br>Stage|Up Room<br>1<br>Stage 2|Wash Ba<br>Stage 1|by Bottle<br>Stage 2|
|---|---|---|---|---|---|---|
|_π_0_._5|60%|40%|55%|35%|40%|25%|
|Ours|**85%**|**70%**|**75%**|**65%**|**70%**|**60%**|


_Pot_ , _Pick Diverse Bottles_ , _Place Can Basket_ , and _Put Bottles Dustbin_ . Taken together, these results show that the advantage of STARRY is not limited to average performance, but is most pronounced on tasks that truly require spatial-temporal reasoning and geometric modeling. 

### **4.2 Real-world experiments** 

To further evaluate the effectiveness of STARRY in real robotic settings, we conduct real-world experiments on representative bimanual manipulation tasks and compare against _π_ 0 _._ 5 [6]. Compared with simulation, real-world scenarios involve stronger perception noise, execution errors, and interaction uncertainty, and therefore provide a more direct measure of practical deployment performance. We consider three tasks, namely _Hand Over Vegetables_ , _Tidy Up Room_ , and _Wash Baby Bottle_ , as shown in Fig. 4. To better characterize policy capability, each task is evaluated in two stages: Stage 1 focuses on the key subskill, while Stage 2 requires completing the full multi-step task built upon Stage 1. All real-world experiments are conducted on the ARX R5 bimanual robot platform from ARX. For each task, we collect 50 real-robot demonstrations for training and evaluate each method with 20 rollouts, reporting success rate as the metric. 

Table 3 reports the real-world success rates. STARRY achieves 70.8% average success over the six evaluations, compared with 42.5% for _π_ 0 _._ 5, consistently outperforming it across all tasks and stages. Notably, the gain becomes larger in the more challenging Stage 2 setting, where STARRY improves success by 31.7 percentage points, suggesting that its advantage is not limited to stabilizing shorthorizon actions but also comes from stronger spatial-temporal modeling for multi-step execution. The qualitative comparisons in Fig. 5 further support this observation. In _Hand Over Vegetables_ (Fig. 5(a)), _π_ 0 _._ 5 often fails to establish a proper spatial-temporal configuration for bimanual handover, leading to grasping or transfer errors, whereas STARRY completes the sequence more reliably. In _Tidy Up Room_ (Fig. 5(b)), _π_ 0 _._ 5 may open the box but fail to align the object with the box opening during placement, while STARRY better preserves the target-container spatial relationship. In _Wash Baby Bottle_ (Fig. 5(c)), the irregular bottle geometry makes grasping, shaking, and placement sensitive to local contact and temporal coordination; STARRY successfully maintains a stable grasp, executes the shaking motion, and completes the final placement. These results are consistent with our design: jointly denoised spatial-temporal latents provide coherent future interaction cues, while the _Geometry Expert_ and GASAM inject action-aligned geometric guidance into critical local regions, improving spatial-temporal coordination, object alignment, and multi-step execution in real-world bimanual manipulation. 

8 


Figure 5: Qualitative comparison in real-world experiments. STARRY and _π_ 0 _._ 5 are compared on three bimanual tasks. Red boxes highlight key regions related to success or failure. 

Table 4: Ablation on predictive representation and geometry-aware modulation on RoboTwin 2.0. Values in parentheses denote absolute gains from enabling GASAM under the same predictive representation. **Act.** : Action-Only Denoising. **App.** : Appearance-Only Prediction. **ST** : Full SpatialTemporal Modeling. 

|GASAM||Randomized|||Clean||
|---|---|---|---|---|---|---|
||Act.|App.|ST|Act.|App.|ST|
|Disabled|64.96%|85.80%|88.82%|63.42%|86.64%|90.40%|
|Enabled|75.88% (+10.92)|86.96% (+1.16)|**93.30%** (+4.48)|72.50% (+9.08)|87.86% (+1.22)|**93.82%** (+3.42)|


∆ST _−_ Act +23.86 w/o GASAM; +17.42 w/ GASAM +26.98 w/o GASAM; +21.32 w/ GASAM 

### **4.3 Ablation study** 

Table 4 studies the effects of predictive representation and geometry-aware modulation. Without GASAM, moving from action-only denoising to appearance-only prediction significantly improves performance from 64.96% to 85.80% on Randomized and from 63.42% to 86.64% on Clean, showing that future appearance prediction provides useful temporal context beyond reactive action generation. Further introducing full spatial-temporal modeling improves the results to 88.82% and 90.40%, respectively. This indicates that appearance prediction alone is insufficient for manipulation: explicitly modeling trajectory evolution and spatial geometry provides additional constraints for contact, handover, and placement, which are critical in spatially demanding manipulation tasks. 

Enabling GASAM consistently improves all representation variants. The gain is especially large for action-only denoising (+10.92% on Randomized and +9.08% on Clean), suggesting that geometryaware weights provide an effective spatial prior even without full future prediction. Combined with ST modeling, GASAM further improves performance from 88.82% to 93.30% on Randomized and from 90.40% to 93.82% on Clean, achieving the best overall results. The smaller gain on appearance-only prediction may be because appearance prediction already captures coarse object saliency but lacks precise geometric grounding. Task-level results in Appendix B.2 further show larger improvements on spatially sensitive tasks such as handover and placement, supporting that STARRY benefits from both spatial-temporal prediction and geometry-aware action-attention modulation. 

9 

## **5 Conclusion** 

We presented **STARRY** , a world-model-enhanced action-generation policy that aligns spatialtemporal prediction with action generation. STARRY jointly denoises future spatial-temporal latents and action sequences, and uses GASAM to inject predicted geometry into the action attention branch. On RoboTwin 2.0, STARRY achieves **93.82%** / **93.30%** average success under Clean and Randomized settings. In real-world experiments, it improves average success from **42.5%** to **70.8%** compared with _π_ 0 _._ 5, demonstrating improved execution reliability in physical manipulation. These results demonstrate the effectiveness of action-centric spatial-temporal world modeling for spatial-temporally demanding robotic action generation. 

## **Acknowledgments and Disclosure of Funding** 

We thank Yuzhuo Miao for his valuable support in dataset collection and processing. We also thank Yunlong Guo, Zhaolong Shen, Shijie Lian, and Xiaopeng Lin for their assistance with data collection. 

## **References** 

- [1] AgiBot-World-Contributors, Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xuan Hu, Xu Huang, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025. 

- [2] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alexander Herzog, et al. Do as i can, not as i say: Grounding language in robotic affordances. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2022. 

- [3] Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan Tan, Peng Wang, Junyang Lin, Chang Zhou, and Jingren Zhou. Qwen-vl: A versatile vision-language model for understanding, localization, text reading, and beyond. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2024. 

- [4] Adrien Bardes, Quentin Garrido, Jean Ponce, Xinlei Chen, Michael Rabbat, Yann LeCun, Mahmoud Assran, and Nicolas Ballas. Revisiting feature prediction for learning visual representations from video. In _Transactions on Machine Learning Research (TMLR)_ , 2024. 

- [5] Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan Wang, Shuhe Huang, Haitian Liu, Ruowen Zhao, Yao Feng, Chendong Xiang, Yinze Rong, et al. Motus: A unified latent action world model. _arXiv preprint arXiv:2512.13030_ , 2025. 

- [6] Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, et al. _π_ 0 _._ 5: A visionlanguage-action model with open-world generalization. In _Proceedings of the 9th Conference on Robot Learning (CoRL)_ , Proceedings of Machine Learning Research, 2025. 

- [7] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- [8] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alexander Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 

- [9] Jiahao Cen, Zhenyu Yu, et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 

- [10] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, Weiliang Deng, Yubin Guo, Tian Nian, Xuanbing Xie, Qiangyu Chen, Kailun Su, Tianling Xu, Guodong Liu, Mengkang Hu, Huan-ang Gao, Kaixuan 

10 

Wang, Zhixuan Liang, Yusen Qin, Xiaokang Yang, Ping Luo, and Yao Mu. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 

- [11] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 2024. 

- [12] Xiaowei Chi, Peidong Jia, Chun-Kai Fan, Xiaozhu Ju, et al. Wow: Towards a world-omniscient world model through embodied interaction. _arXiv preprint arXiv:2509.22642_ , 2025. 

- [13] M. U. Din et al. Vision language action models in robotic manipulation. _arXiv preprint arXiv:2507.10672_ , 2025. 

- [14] Zibin Dong, Fei Ni, Yifu Yuan, Yinchuan Li, and Jianye Hao. Embodiedmae: A unified 3d multi-modal representation for robot manipulation. _arXiv preprint arXiv:2505.10105_ , 2025. 

- [15] Shenyuan Gao, William Liang, Kaiyuan Zheng, Ayaan Malik, Seonghyeon Ye, et al. Dreamdojo: A generalist robot world model from large-scale human videos. _arXiv preprint arXiv:2602.06949_ , 2026. 

- [16] Kristen Grauman, Andrew Westbury, Eugene Byrne, Zachary Chavis, Antonino Furnari, Rohit Girdhar, Jackson Hamburger, Hao Jiang, Miao Liu, Xingyu Liu, et al. Ego4d: Around the world in 3,000 hours of egocentric video. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2022. 

- [17] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2020. 

- [18] Jonathan Ho, Tim Salimans, Alexey Gritsenko, William Chan, Mohammad Norouzi, and David J. Fleet. Video diffusion models. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2022. 

- [19] InternVLA-A1 Team. Internvla-a1: Unifying understanding, generation and action for robotic manipulation. _arXiv preprint arXiv:2601.02456_ , 2026. 

- [20] Yunfan Jiang, Agrim Gupta, Zichen Zhang, Guanzhi Wang, Yongqiang Dou, Yanjun Chen, Li Fei-Fei, Anima Anandkumar, Yuke Zhu, and Linxi Fan. Vima: General robot manipulation with multimodal prompts. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2023. 

- [21] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Abhiram Maddukuri, Lance Zhang, Yuke Zhu, et al. Droid: A large-scale in-the-wild robot manipulation dataset. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

- [22] Lin Li, Qihang Zhang, Yiming Luo, Shuai Yang, Ruilin Wang, Fei Han, Mingrui Yu, Zelin Gao, Nan Xue, Xing Zhu, Yujun Shen, and Yinghao Xu. Causal world modeling for robot control. _arXiv preprint arXiv:2601.21998_ , 2026. 

- [23] Xinqing Li, Xin He, Le Zhang, and Yun Liu. A comprehensive survey on world models for embodied ai. _arXiv preprint arXiv:2510.16732_ , 2025. 

- [24] Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matthew Le. Flow matching for generative modeling. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2023. 

- [25] Qi Lv, Weijie Kong, Hao Li, Jia Zeng, Zherui Qiu, Delin Qu, Haoming Song, Qizhi Chen, Xiang Deng, and Jiangmiao Pang. F1: A vision-language-action model bridging understanding and generation to actions. _arXiv preprint arXiv:2509.06951_ , 2025. 

- [26] Ajay Mandlekar, Danfei Xu, Josiah Wong, Soroush Nasiriany, Chen Wang, Rohun Kulkarni, Li Fei-Fei, Silvio Savarese, Yuke Zhu, and Roberto Martín-Martín. Robomimic: A benchmark for robot learning from demonstration. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2021. 

11 

- [27] Open X-Embodiment Collaboration. Open x-embodiment: Robotic learning datasets and rt-x models. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , 2024. 

- [28] William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2023. 

- [29] Jingjing Qian, Boyao Han, Chen Shi, Lei Xiao, Long Yang, Shaoshuai Shi, and Li Jiang. Geopredict: Leveraging predictive kinematics and 3d gaussian geometry for precise vla manipulation. _arXiv preprint arXiv:2512.16811_ , 2025. 

- [30] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Björn Ommer. Highresolution image synthesis with latent diffusion models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2022. 

- [31] Yu Shang, Zhuohang Li, Yiding Ma, Weikang Su, Xin Jin, Ziyou Wang, Lei Jin, Xin Zhang, Yinzhou Tang, Haisheng Su, et al. Worldarena: A unified benchmark for evaluating perception and functional utility of embodied world models. _arXiv preprint arXiv:2602.08971_ , 2026. 

- [32] Yang Song, Jascha Sohl-Dickstein, Diederik P. Kingma, Abhishek Kumar, Stefano Ermon, and Ben Poole. Score-based generative modeling through stochastic differential equations. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2021. 

- [33] Homer Walke, Kevin Black, Abraham Lee, Moo Jin Kim, Max Du, Chongyi Zheng, Tony Zhao, Philippe Hansen-Estruch, Quan Vuong, Andre He, et al. Bridgedata v2: A dataset for robot learning at scale. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2023. 

- [34] Ang Wang, Baole Ai, Bin Wen, et al. Wan: Open and advanced large-scale video generative models. _arXiv preprint arXiv:2503.20314_ , 2025. 

- [35] Angen Ye, Boyuan Wang, et al. Gigaworld-0: World models as data engine to empower embodied ai. _arXiv preprint arXiv:2511.19861_ , 2025. 

- [36] Xumin Yu et al. Hy-embodied-0.5: Embodied foundation models for real-world agents. _arXiv preprint arXiv:2604.07430_ , 2026. 

- [37] Jianke Zhang, Yanjiang Guo, Yucheng Hu, Xiaoyu Chen, Xiang Zhu, and Jianyu Chen. Up-vla: A unified understanding and prediction model for embodied agent. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2025. 

- [38] X. Zhang et al. Egodex: Learning dexterous manipulation from egocentric human demonstrations. _arXiv preprint arXiv:2505.11709_ , 2025. 

- [39] Tony Z. Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 

- [40] Haoyu Zhen, Qiao Sun, Hongxin Zhang, Junyan Li, Siyuan Zhou, Yilun Du, and Chuang Gan. Learning 4d embodied world models. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2025. 

- [41] Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, Yuchun Feng, Yinan Zheng, Jiayin Zou, Yilun Chen, Jia Zeng, et al. X-vla: Soft-prompted transformer as scalable cross-embodiment vision-language-action model. _arXiv preprint arXiv:2510.10274_ , 2025. 

- [42] Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin Burchfiel, Paarth Shah, and Abhishek Gupta. Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- [43] F. Zhu et al. Wmpo: World model-based policy optimization for vision-language-action models. _arXiv preprint arXiv:2511.09515_ , 2025. 

- [44] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Proceedings of the Conference on Robot Learning (CoRL)_ , pages 2165–2183. PMLR, 2023. 

12 

## **A Additional details and pseudocode** 

### **A.1 Hyperparameters** 

We summarize the key numerical hyperparameters used in STARRY in Table 5. The model uses branch-specific diffusion timesteps for video and action denoising, while the Geometry Expert predicts depth and multicamera XYZ end-effector positions to provide GASAM-based action modulation. 

### **A.2 Compute resources** 

For fine-tuning and evaluation, we use GPU workers equipped with 8 NVIDIA Tesla A100-80G GPUs. Each worker provides 112 vCPUs, 1960 GiB memory, 80 Gbit/s network bandwidth, and 32 Gbit/s disk bandwidth. A typical fine-tuning run with batch size 256 for 40k steps takes approximately one week on this configuration. Large-scale pretraining uses the same type of GPU worker but scales to more nodes depending on the training stage and data scale. The main reported experiments, including RoboTwin 2.0 evaluation and real-world policy evaluation, are conducted with this A100-based configuration. 

### **A.3 Pseudocode of STARRY** 

Algorithm 1 summarizes the training procedure of STARRY. For each training batch, we first construct spatial-temporal inputs from multi-view RGB-D observations and projected end-effector trajectories, and encode them into video tokens. The _Understanding Expert_ provides semantic grounding tokens, while the _ST World Model_ and _Action Expert_ jointly denoise future spatial-temporal latents and action sequences under branch-specific diffusion timesteps. In parallel, the _Geometry Expert_ predicts future depth and end-effector positions, from which GASAM computes token-aligned geometry-aware weights. These weights are injected only into the action attention branch, so geometric priors guide action generation without perturbing video modeling or visual-language understanding. 

During inference, STARRY follows the same denoising structure but removes all supervision terms. Starting from noisy future latent and action variables, the model iteratively predicts future geometry, constructs GASAM weights, and updates the latent-action pair through joint denoising. The final action sequence **a** _t_ +1: _t_ + _H_ is executed by the robot, while the predicted spatial-temporal latents and geometry serve as internal guidance for action generation. 

## **B Additional experimental results** 

### **B.1 Visualization of future spatial-temporal latents** 

To further illustrate what is captured by the learned future spatial-temporal latents, we visualize decoded future predictions in both simulation and real-world settings. These visualizations are not used as additional supervision during evaluation, but serve to qualitatively examine whether the predicted latents preserve temporally coherent scene evolution, end-effector motion, and spatial geometry. As shown below, STARRY predicts not only future appearance changes, but also structured depth and geometry patterns that are closely aligned with manipulation-relevant regions. 

Fig. 6 shows representative visualizations on RoboTwin 2.0. The decoded predictions maintain coherent future scene evolution across diverse simulated tasks, including changes in object positions, manipulator configurations, and depth structure. This supports our claim that the ST World Model learns a structured spatial-temporal representation rather than only predicting visually plausible RGB frames. 

Fig. 7 further visualizes future spatial-temporal latents in real-world tasks. Despite real-world visual noise, lighting variation, and cluttered backgrounds, the predictions remain temporally coherent and preserve task-relevant spatial layouts. These results indicate that the learned latent representation provides useful predictive guidance for physical manipulation, complementing the quantitative real-world results reported in the main paper. 

13 


Figure 6: Visualization of future spatial-temporal latents on RoboTwin 2.0. Each row corresponds to a manipulation rollout, and columns show consecutive future predictions decoded from the spatialtemporal latent representation. The predicted latents preserve object layouts, end-effector motion trends, and depth-related spatial structure across future steps, indicating that the ST World Model captures more than appearance-level temporal consistency. 

14 


Figure 7: Visualization of future spatial-temporal latents in real-world manipulation. The decoded predictions show temporally consistent RGB-D structure under physical robot execution, including future end-effector motion and task-relevant spatial changes. 

### **B.2 Complete RoboTwin 2.0 results** 

Table 6 reports the complete task-level results on all 50 RoboTwin 2.0 tasks under Clean and Randomized settings. STARRY achieves the best average success rates, reaching **93.82%** / **93.30%** . 

Table 7 provides the complete task-level ablation results. Full spatial-temporal modeling with GASAM achieves the strongest performance, improving from 88.82% to 93.30% under Randomized and from 90.40% to 93.82% under Clean compared with disabling GASAM. These results further validate the complementary effects of spatial-temporal modeling and geometry-aware action modulation. 

## **C Limitations** 

Although STARRY improves spatial-temporal action generation in both simulation and real-world experiments, several limitations remain. First, real-world evaluation is conducted on a limited number of bimanual manipulation tasks, and broader validation across more robot embodiments and open-ended environments is needed. Second, GASAM benefits from accurate predicted depth and end-effector geometry; under highly ambiguous observations, less reliable geometry prediction may reduce the effectiveness of the modulation signal. Finally, STARRY builds on large video and vision-language backbones, which increases training cost compared with smaller reactive policies. 

## **D Impact statement** 

STARRY aims to improve robotic manipulation by enhancing spatial-temporal prediction and geometry-aware action generation. This may benefit applications such as assistive robotics, manufacturing, and household automation by improving execution reliability in spatially demanding tasks. Potential risks include unsafe robot behaviors under distribution shift or inappropriate deployment in unstructured environments. Therefore, STARRY should be viewed as a research-stage system and deployed only with appropriate physical safety constraints, monitoring, and human oversight. 

15 

Table 5: Key implementation hyperparameters of STARRY. 

|Component|Hyperparameter|Value|
|---|---|---|
||State / action dim.<br>Input resolution|14/14<br>384_×_640|
|Policy|Predicted video frames<br>Action chunk size<br>Inference denoising steps<br>Observation / action loss weight|8<br>16<br>10<br>1_._0/2_._0|
||Hidden size / FFN dim.<br>Layers / heads|3072/14336<br>30/24|
|ST World Model|Input / output dim.<br>Frequency embedding dim.<br>Text length<br>Layer norm epsilon|48/48<br>256<br>512<br>1_×_10<sup>_−_6</sup>|
|Action Expert|Hidden size<br>Layers / heads<br>FFN multiplier / norm epsilon|1024<br>30/16<br>4/1_×_10<sup>_−_6</sup>|
|Understanding Expert|Hidden size<br>FFN multiplier / norm epsilon|512<br>4/1_×_10<sup>_−_5</sup>|
|Geometry Expert|Video / action token dim.<br>Hidden size / camera dim.<br>Number of cameras<br>Depth / pose / target loss weight|3072/1024<br>512/256<br>3<br>1_._0/1_._0/1_._0|
||Optimizer|AdamW|
|Training|Training steps<br>Learning rate|40k<br>1–5_×_10<sup>_−_5</sup>|
||Weight decay|0_._01|


16 

**Algorithm 1** STARRY training with spatial-temporal denoising and GASAM 

**Require:** Training batch _B_ = _{_ ( **o** _t_ 0: _t_ + _H ,_ **a** _t_ +1: _t_ + _H_ ) _}_ **Require:** ST World Model _fθ_<sup>ST, Action Expert</sup><sup>_f_</sup> _θ_<sup>_a_, Geometry Expert</sup><sup>_gϕ_, Understanding Expert</sup><sup>_hψ_</sup> 

**Ensure:** Optimized parameters _θ, ϕ, ψ_ 

- 1: **for** each training iteration **do** 

- 2: Sample a mini-batch from _B_ 

- 3: Project end-effector trajectories into camera views as **u**<sup>_c,m_</sup> _τ_ = Π( _Kt_<sup>_c, T_</sup> _t_<sup>_c,_</sup><sup>**e**</sup><sup>_m_</sup> _τ_<sup>), and construct</sup> spatial-temporal inputs: 

- **x** _t_ = Φ( _{_ **I**<sup>_c_</sup> _t_<sup>_}c, {_</sup><sup>**D**</sup> _t_<sup>_c}c, {_</sup><sup>**u**</sup><sup>_c,m_</sup> _τ }τ ≤t,c,m_ ) 

- 4: Encode **X** _t_ 0: _t_ into video tokens **v** _t_ 0: _t_ and obtain understanding tokens **s** = _hψ_ ( **o** _t_ ) 5: Sample branch-specific diffusion timesteps ( _τv, τa_ ) and corrupt future spatial-temporal targets and action targets 

- 6: Predict future geometry with the Geometry Expert: ( **D**<sup>ˆ</sup> _t_ +1: _t_ + _H ,_ ˆ **p** _t_ +1: _t_ + _H_ ) = _gϕ_ ( **v** _t_ 0: _t,_ **a** _≤t,_ **o** _t, τv, τa_ ) 

- 7: Compute geometry-aware weights **w** _t_ +1: _t_ + _H_ from predicted 3D distances between **p** ˆ _t_ and scene points **P**<sup>ˆ</sup> _t,j_ 

- 8: Apply GASAM only to action-to-video attention: Attn<sup>_a_</sup> GASAM<sup>_←v_= Softmax</sup> + _λ_ log( **w** _t_ +1: _t_ + _H_ + _ϵ_ ) **V**<sup>_v_</sup> � **<u>Q</u>** _a_ <u>(</u> _~~√~~_ **K** _dv_ <u>)</u> _⊤_ � 

- 9: Jointly denoise future spatial-temporal latents and actions with GASAM-modulated action attention: (ˆ **z** _t_ +1: _t_ + _H ,_ ˆ **a** _t_ +1: _t_ + _H_ ) = ( _fθ_<sup>ST</sup><sup>_, f_</sup> _θ_<sup>_a_)(</sup><sup>**v**</sup><sup>_t_</sup> 0<sup>:</sup><sup>_t,_</sup><sup>**s**</sup><sup>_, τv, τa_)</sup> 

- 10: Compute diffusion loss _L_ diff = _λoL_ obs + _λaL_ action 11: Compute geometry loss _L_ geo = _λdL_ depth + _λpL_ pose + _λwL_ weight 12: Update parameters using _L_ = _L_ diff + _L_ geo 

- 13: **end for** 

17 

Table 6: Complete task-level results on RoboTwin 2.0 under Clean and Randomized settings. We report success rates over all 50 tasks for each method. Bold numbers indicate the best result for each task and setting; ties are all bolded. 

|Simulation Task|G<br>|O-1<br>|_π_<br>|0<br>|_π_0<br>|_._5<br>|X-<br>|VLA<br>|M<br>|otus<br>|LingB<br>|ot-VA<br>|O<br>|urs<br>|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Clean|Rand.|Clean|Rand.|Clean|Rand.|Clean|Rand.|Clean|Rand.|Clean|Rand.|Clean|Rand.|
|Adjust Bottle|49%|62%|99%|95%|89.5%|91%|**100%**|**99%**|89%|93%|90%|94%|98%|97%|
|<br>Beat Block Hammer|6%|10%|79%|84%|79.5%|71.5%|92%|88%|95%|88%|**96%**|**98%**|92%|89%|
|Blocks Ranking Rgb|7%|3%|80%|63%|67.5%|60%|83%|83%|99%|97%|99%|**98%**|**100%**|**98%**|
|Blocks Ranking Size|2%|2%|14%|5%|28.5%|20%|67%|74%|75%|63%|**94%**|**96%**|71%|74%|
|Click Alarmclock|95%|90%|77%|68%|97.5%|91%|99%|99%|**100%**|**100%**|99%|**100%**|**100%**|**100%**|
|Click Bell<br>|98%<br>|95%<br>|71%<br>|48%<br>|87%<br>|71%<br>|**100%**<br>|**100%**<br>|**100%**<br>|**100%**<br>|**100%**<br>|**100%**<br>|**100%**<br>|**100%**<br>|
|Dump Bin Bigbin|57%|45%|88%|83%|61%|69.5%|79%|77%|**95%**|91%|89%|96%|93%|**97%**|
|<br>Grab Roller|99%|99%|98%|94%|95%|94.5%|**100%**|**100%**|**100%**|**100%**|**100%**|**100%**|**100%**|**100%**|
|Handover Block|9%|12%|47%|31%|42%|38%|73%|37%|86%|73%|**99%**|**78%**|56%|48%|
|Handover Mic|12%|8%|97%|97%|63%|57.5%|0%|0%|78%|63%|94%|96%|**100%**|**99%**|
|Hanging Mug|0%|0%|14%|11%|10.5%|10%|23%|27%|38%|38%|40%|28%|**69%**|**72%**|
|<br>Lift Pot|92%|92%|80%|72%|48%|42.5%|99%|**100%**|96%|99%|**100%**|99%|**100%**|**100%**|
|Move Can Pot|16%|4%|68%|48%|40%|41%|89%|86%|34%|74%|94%|97%|**100%**|**98%**|
|Move Pillbottle Pad|9%|11%|67%|46%|58.5%|45%|73%|71%|93%|96%|99%|99%|**100%**|**100%**|
|Move Playingcard Away|37%|24%|74%|65%|77.5%|75.5%|93%|98%|**100%**|96%|**100%**|99%|**100%**|**100%**|
|Move Stapler Pad|3%|4%|41%|24%|36%|30%|78%|73%|83%|85%|91%|79%|**93%**|**93%**|
|Open Laptop|65%|60%|71%|81%|54.5%|65.5%|93%|**100%**|**95%**|91%|92%|94%|93%|91%|
|Open Microwave|12%|14%|4%|32%|34.5%|57%|79%|71%|**95%**|**91%**|82%|86%|58%|61%|
|Pick Diverse Bottles<br>|61%<br>|56%<br>|69%<br>|31%<br>|43%<br>|37%<br>|58%<br>|36%<br>|90%<br>|91%<br>|89%<br>|82%<br>|**98%**<br>|**96%**<br>|
|Pick Dual Bottles<br>|81%<br>|74%<br>|59%<br>|37%<br>|51.5%<br>|34.5%<br>|47%<br>|36%<br>|96%<br>|90%<br>|**100%**<br>|99%<br>|**100%**<br>|**100%**<br>|
|Place A2b Left<br>|33%<br>|36%<br>|43%<br>|47%<br>|74.5%<br>|71%<br>|48%<br>|49%<br>|85%<br>|79%<br>|**97%**<br>|**93%**<br>|96%<br>|91%<br>|
|Place A2b Right|31%|22%|39%|34%|74.5%|70.5%|36%|36%|90.5%|87%|**97%**|95%|94%|**96%**|
|Place Bread Basket|47%|52%|62%|46%|62.5%|60%|81%|71%|91%|94%|97%|95%|**100%**|**99%**|
|Place Bread Skillet|2%|1%|66%|49%|61.5%|56%|77%|67%|86%|83%|95%|90%|**96%**|**95%**|
|Place Burger Fries<br>|88%<br>|92%<br>|81%<br>|76%<br>|80%<br>|78.5%<br>|94%<br>|94%<br>|98%<br>|98%<br>|97%<br>|95%<br>|**99%**<br>|**99%**<br>|
|Place Can Basket|29%|37%|55%|46%|40.5%|43.5%|49%|52%|81%|76%|81%|84%|**89%**|**88%**|
|Place Cans Plasticbox|68%|77%|63%|45%|67%|65.5%|97%|98%|98%|94%|**100%**|99%|**100%**|**100%**|
|Place Container Plate|73%|70%|97%|92%|85%|86.5%|97%|95%|98%|99%|99%|97%|**100%**|**100%**|
|Place Dual Shoes|6%|10%|59%|51%|43.5%|41%|79%|88%|93%|87%|94%|89%|**96%**|**94%**|
|Place Empty Cup|44%|39%|91%|85%|87.5%|92.5%|**100%**|98%|99%|98%|**100%**|**100%**|**100%**|**100%**|
|Place Fan|1%|0%|66%|71%|56%|60.5%|80%|75%|91%|87%|**99%**|**93%**|95%|92%|
|Place Mouse Pad|15%|10%|20%|20%|40.5%|32.5%|70%|70%|66%|68%|93%|96%|**96%**|**98%**|
|Place Object Basket<br>|48%<br>|49%<br>|67%<br>|70%<br>|61.5%<br>|56%<br>|44%<br>|39%<br>|81%<br>|87%<br>|**91%**<br>|88%<br>|89%<br>|**91%**<br>|
|Place Object Scale|26%|27%|57%|52%|63%|64.5%|52%|74%|88%|85%|**96%**|**95%**|89%|88%|
|<br>Place Object Stand|56%|63%|82%|68%|82.5%|75%|86%|88%|98%|97%|99%|96%|**100%**|**100%**|
|Place Phone Stand|30%|37%|49%|53%|65%|67%|88%|87%|87%|86%|**97%**|**97%**|91%|**97%**|
|Place Shoe|15%|13%|76%|76%|74.5%|77%|96%|95%|99%|97%|98%|98%|**100%**|**99%**|
|Press Stapler|66%|51%|44%|37%|83.5%|76.5%|92%|98%|93%|98%|85%|82%|**100%**|**100%**|
|Put Bottles Dustbin|7%|4%|65%|56%|48%|44%|74%|77%|81%|79%|87%|91%|**96%**|**93%**|
|Put Object Cabinet|60%|43%|73%|60%|52%|47%|46%|48%|**88%**|71%|85%|**87%**|84%|77%|
|Rotate Qrcode|22%|9%|74%|70%|68%|71.5%|34%|33%|89%|73%|**96%**|**91%**|94%|84%|
|Scan Object|1%|2%|55%|42%|57%|51.5%|14%|36%|67%|66%|**96%**|91%|93%|**96%**|
|<br>Shake Bottle Horizontally|97%|92%|98%|92%|97.5%|99.5%|**100%**|**100%**|**100%**|98%|**100%**|99%|**100%**|99%|
|<br>Shake Bottle|97%|93%|94%|91%|95%|98.5%|99%|**100%**|**100%**|97%|**100%**|97%|**100%**|97%|
|Stack Blocks Three|1%|1%|72%|52%|53%|46%|6%|10%|91%|95%|**99%**|98%|97%|**100%**|
|Stack Blocks Two|12%|22%|93%|79%|72.5%|78%|92%|87%|**100%**|98%|**100%**|98%|**100%**|**100%**|
|Stack Bowls Three<br>|4%<br>|7%<br>|77%<br>|75%<br>|55%<br>|53%<br>|76%<br>|86%<br>|79%<br>|87%<br>|86%<br>|83%<br>|**91%**<br>|**92%**<br>|
|Stack Bowls Two|51%|45%|94%|95%|86.5%|81%|96%|93%|98%|98%|94%|98%|**100%**|**99%**|
|Stamp Seal|19%|13%|46%|33%|57.5%|39%|76%|82%|93%|92%|96%|97%|**100%**|**99%**|
|<br>Turn Switch|34%|30%|41%|42%|33.5%|30%|40%|61%|84%|78%|44%|45%|**85%**|**89%**|
|Average (%)|37.8%|36.24%|65.92%|58.4%|62.86%|60.3%|72.8%|72.84%|88.66%|87.02%|92.93%|91.55%|**93.82% **|**93.3%**|


18 

Table 7: Task-level ablation on RoboTwin 2.0. **Act.** : Action-Only Denoising. **App.** : AppearanceOnly Foresight. **ST** : Full Spatial-Temporal Foresight. **Dis./En.** : GASAM disabled/enabled. 

||||Rand|omized|||||Cl|ean|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Task|A|ct.|A|pp.|S|T|A|ct.|A|pp.||ST|
||Dis.|En.|Dis.|En.|Dis.|En.|Dis.|En.|Dis.|En.|Dis.|En.|
|Adjust Bottle|91%|90%|91%|100%|100%|97%|96%|98%|99%|97%|97%|98%|
|<br>Beat Block Hammer<br>|59%<br>|77%<br>|62%<br>|88%<br>|90%<br>|89%<br>|49%<br>|64%<br>|75%<br>|88%<br>|88%<br>|92%<br>|
|Blocks Ranking Rgb|11%|23%|95%|94%|95%|98%|13%|12%|91%|96%|98%|100%|
|Blocks Ranking Size|9%|60%|66%|66%|71%|74%|6%|61%|70%|64%|74%|71%|
|<br>Click Alarmclock|100%|98%|100%|100%|100%|100%|100%|100%|99%|100%|100%|100%|
|Click Bell|100%|99%|100%|97%|99%|100%|100%|100%|100%|100%|100%|100%|
|Dump Bin Bigbin<br>|63%<br>|87%<br>|89%<br>|85%<br>|94%<br>|97%<br>|69%<br>|90%<br>|94%<br>|89%<br>|94%<br>|93%<br>|
|Grab Roller|96%|100%|99%|100%|100%|100%|99%|98%|100%|100%|100%|100%|
|Handover Block|8%|28%|32%|32%|28%|48%|15%|13%|21%|31%|24%|56%|
|Handover Mic|78%|86%|69%|97%|99%|99%|75%|99%|95%|100%|99%|100%|
|Hanging Mug|11%|8%|53%|50%|51%|72%|6%|10%|43%|42%|68%|69%|
|Lift Pot|86%|97%|98%|100%|100%|100%|85%|90%|100%|100%|100%|100%|
|Move Can Pot|66%|85%|92%|69%|95%|98%|54%|61%|78%|91%|96%|100%|
|Move Pillbottle Pad|89%|95%|97%|98%|100%|100%|85%|72%|97%|100%|99%|100%|
|Move Playingcard Away|95%|96%|100%|100%|97%|100%|95%|96%|98%|98%|86%|100%|
|<br>Move Stapler Pad|32%|80%|60%|70%|75%|93%|31%|71%|73%|87%|87%|93%|
|Open Laptop|90%|94%|94%|87%|87%|91%|89%|94%|94%|93%|90%|93%|
|Open Microwave|39%|10%|76%|20%|19%|61%|28%|43%|68%|29%|34%|58%|
|<br>Pick Diverse Bottles|78%|17%|89%|92%|95%|96%|90%|38%|80%|90%|95%|98%|
|Pick Dual Bottles|89%|15%|95%|100%|99%|100%|96%|21%|99%|99%|100%|100%|
|Place A2b Left|75%|87%|89%|82%|84%|91%|71%|83%|79%|91%|90%|96%|
|Place A2b Right|71%|84%|91%|85%|92%|96%|69%|76%|93%|88%|95%|94%|
|Place Bread Basket|74%|86%|88%|96%|93%|99%|78%|74%|94%|96%|95%|100%|
|Place Bread Skillet|65%|87%|81%|93%|88%|95%|70%|71%|87%|88%|93%|96%|
|Place Burger Fries|99%|99%|89%|93%|93%|99%|95%|97%|100%|92%|96%|99%|
|Place Can Basket|24%|65%|79%|72%|78%|88%|20%|44%|88%|86%|84%|89%|
|Place Cans Plasticbox<br>|87%<br>|95%<br>|95%<br>|91%<br>|100%<br>|100%<br>|82%<br>|65%<br>|99%<br>|99%<br>|100%<br>|100%<br>|
|Place Container Plate|94%|100%|98%|97%|100%|100%|93%|98%|99%|100%|100%|100%|
|Place Dual Shoes|94%|92%|72%|98%|97%|94%|58%|85%|80%|75%|94%|96%|
|Place Empty Cup|96%|100%|99%|99%|99%|100%|94%|95%|98%|100%|100%|100%|
|Place Fan|63%|86%|88%|89%|87%|92%|60%|87%|89%|85%|84%|95%|
|Place Mouse Pad|35%|80%|82%|83%|86%|98%|39%|70%|77%|79%|94%|96%|
|Place Object Basket|17%|51%|87%|89%|91%|91%|23%|57%|90%|84%|91%|89%|
|Place Object Scale|61%|86%|84%|90%|87%|88%|64%|83%|87%|90%|88%|89%|
|Place Object Stand|98%|97%|99%|100%|99%|100%|93%|97%|96%|98%|100%|100%|
|Place Phone Stand|67%|81%|87%|90%|93%|97%|67%|73%|84%|88%|93%|91%|
|Place Shoe|91%|97%|100%|99%|95%|99%|88%|96%|100%|99%|99%|100%|
|Press Stapler|91%|98%|100%|96%|95%|100%|84%|99%|99%|99%|97%|100%|
|Put Bottles Dustbin|7%|31%|73%|89%|91%|93%|5%|30%|82%|86%|92%|96%|
|Put Object Cabinet|19%|32%|46%|74%|78%|77%|7%|31%|41%|71%|75%|84%|
|<br>Rotate Qrcode|57%|71%|80%|77%|79%|84%|72%|78%|83%|70%|84%|94%|
|Scan Object|52%|81%|87%|87%|96%|96%|58%|70%|85%|87%|90%|93%|
|Shake Bottle|97%|96%|98%|94%|97%|97%|99%|100%|99%|98%|96%|100%|
|Shake Bottle Horizontally|94%|97%|97%|97%|96%|99%|99%|100%|96%|98%|97%|100%|
|<br>Stack Blocks Three|28%|94%|95%|96%|99%|100%|23%|90%|91%|96%|99%|97%|
|Stack Blocks Two|73%|87%|100%|100%|98%|100%|65%|55%|94%|100%|100%|100%|
|Stack Bowls Three|20%|42%|87%|86%|85%|92%|17%|37%|88%|90%|92%|91%|
|Stack Bowls Two|74%|98%|92%|99%|93%|99%|66%|95%|97%|96%|98%|100%|
|Stamp Seal<br>|85%<br>|91%<br>|95%<br>|99%<br>|98%<br>|99%<br>|80%<br>|93%<br>|99%<br>|99%<br>|98%<br>|100%<br>|
|Turn Switch|50%|58%|75%|63%|80%|89%|51%|65%|64%|71%|77%|85%|
|Average (%)|64.96%|75.88%|85.80%|86.96%|88.82%|93.30%|63.42%|72.50%|86.64%|87.86%|90.40%|93.82%|


19 

