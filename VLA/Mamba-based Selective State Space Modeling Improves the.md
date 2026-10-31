---
title: "Mamba-based Selective State Space Modeling Improves the Accuracy-Complexity Tradeoff of SmolVLA Vision-Language-Action Experts"
date: "2026-08-10"
authors: "Farida Mohsen; Thowayba Elkaffash; Mohammad Reza Chalak Qazani; Mohamed Mabrok; Nader Meskin; Ali Safa"
url: https://arxiv.org/abs/2608.21407
pdf: https://arxiv.org/pdf/2608.21407
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2608.21407)** / [論文ページ](https://arxiv.org/abs/2608.21407)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Mamba-based Selective State Space Modeling Improves the Accuracy-Complexity Tradeoff of SmolVLA Vision-Language-Action Experts 

Farida Mohsen<sup>1</sup> , Thowayba Elkaffash<sup>1</sup><sup>_,_2</sup> , Mohammad Reza Chalak Qazani<sup>3</sup> , Mohamed Mabrok<sup>2</sup> , Nader Meskin<sup>2</sup> , Ali Safa<sup>1</sup> 

> 1 _College of Science and Engineering, Hamad Bin Khalifa University, Doha, Qatar_ 

> 2 _College of Engineering, Qatar University, Doha, Qatar_ 

> 3 _College of Science and Engineering, James Cook University, Townsville, QLD, 4814, Australia_ fmohsen@hbku.edu.qa 

**_Abstract_ —Vision-language-action (VLA) models face a crucial tradeoff between their task success rate and the policy-call frequency. Executing a single action per inference (** _N_ = 1 **) enables accurate robot control but comes at the cost of huge compute time overheads, making real-time implementation infeasible. On the other hand, executing longer action horizons before replanning (** _N ≫_ 1 **) reduces compute complexity, but inevitably degrades the system’s success rate. In order to improve the VLA accuracycomplexity tradeoff, this paper investigates Mamba’s selective state-space modeling as an alternative to causal self-attention within the action expert of the popular SmolVLA model, widely used as a reference model for its highly accurate yet low complexity nature. We evaluate both the Mamba- and Transformerbased experts on the widely-adopted LIBERO benchmark suites across three execution horizons** _N ∈{_ 1 _,_ 25 _,_ 50 _}_ **, respectively corresponding to high, moderate and low compute complexities. Our results remarkably show that the advantage of the Mamba expert increases with the execution horizon, indicating significant success retention under long execution horizons** _N_ = 50 **and** _N_ = 25 **. When** _N_ = 50 **actions are executed before replanning (i.e., corresponding to feasible real-time deployment), the Mamba expert outperforms the Transformer baseline by** 7 _._ 8% **. In addition, when** _N_ = 25 **actions are executed before replanning, our Mamba expert outperforms the Transformer baseline by** 3 _._ 7% **. Finally, under per-action replanning (** _N_ = 1 **), our Mamba variant matches the Transformer-based mean success rate while significantly reducing the overall model parameter complexity by** 24% **thanks to Mamba’s compute-efficient nature.** 

**_Index Terms_ —vision-language-action models, action chunking, state-space mamba models, execution horizon, robot manipulation, flow matching.** 

## I. INTRODUCTION 

In recent years, the use of foundation models has gained huge interest throughout robotic perception, planning, and decision-making, including scene-conditioned reasoning, mission planning, and high-level behavior generation [1]–[3]. Vision-language-action (VLA) policies extend this line of work to embodied control by mapping visual observations, language instructions, and robot state directly to low-level actions [4]–[6]. Most recent visuomotor and VLA policies do not predict a single command per inference. Rather, they emit a 


Fig. 1. This work provides a novel investigation of the use of Mamba-type Selective State Space Modeling for Vision-Language-Action (VLA) models. Text instructions, as well as robot state and camera data are fed to two VLA setups: a Transformer-based reference and our proposed Mamba-based model. The generated output actions are then used to control a robot arm in a standard benchmarking simulation environment. Remarkably, this work demonstrates that using Mamba leads to significant gains (up to +7 _._ 8%) in success rate while using longer action horizons _N_ , thereby enabling a better accuracycomplexity tradeoff compared to Transformers (which is crucial for feasible real-time system deployment). 

short chunk of continuous actions [5], [7], [8], which amortizes the cost of one generative forward pass over a horizon of _H_ control steps and produces locally coherent motions. 

During system deployment, the controller executes only the first _N ≤ H_ actions of each generated action sequence before requesting a new observation and generating a new sequence prediction. Hence, the choice of _N_ sets a crucial trade-off between VLA accuracy and latency. Using a small _N_ keeps the control policy accurate and close to the current observation but significantly increases the number of VLA inferences, leading to high latency overheads and jeopardizing real-time system deployment [26]. On the other hand, using a large _N_ reduces the frequency of policy calls but widens the interval during which the robot acts on a stale observation, potentially leading to inaccurate behavior. This is in-line with prior experiments across several VLA backbones which have reported that fewer policy calls are generally accompanied by lower task success 


Fig. 2. Proposed Mamba vs. Transformer Action Expert (AE) pipelines. A) The multi-view RGB observations, the robot states, and the task instructions are jointly encoded by a SmolVLM2 backbone into layerwise features that condition the AE. The backbone, its inputs, and the resulting conditioning are identical for both variants. B) The AE alternates cross-attention grounding layers with intra-chunk temporal layers. The two variants only differ in the temporal operator: B0 keeps the original Transformer-based causal self-attention, in which each action token attends to earlier positions of the chunk, and M1 replaces it with a Mamba-1 selective state-space scan over the same positions, significantly reducing the number of trainable weights from 99 _._ 9M to 76 _._ 3M. C) Both variants generate a chunk of _H_ = 50 actions with _Da_ = 7 dimensional action vectors using the same conditional flow-matching sampler. D) At execution, only the first _N ∈{_ 1 _,_ 25 _,_ 50 _}_ actions of the chunk are applied before a new observation is taken and a new chunk is generated. Since every component other than the Intra-chunk temporal mixers are kept fixed in B), the differences in success rates across _N_ will be attributed to the Mamba vs. Transformer choice. 

## rates [23]. 

A number of recent approaches have been proposed to address this trade-off at execution time. Among them, RealTime Chunking [15] improves asynchronous chunk transitions through inference-time inpainting, and VLA-Corrector [23] monitors execution and truncates a chunk once its actions are no longer considered reliable. Crucially, these emerging methods treat the policy as fixed and add _post-hoc_ mechanism to alleviate errors in VLA execution. In contrast, this paper proposes a _different and complementary approach_ by investigating how temporal architectural elements _within_ the action expert model affect the VLA’s success rate when longer action prefixes _N_ are executed. 

To investigate this key question, we select the popular SmolVLA architecture [6] as our reference backbone model in this work and explore how replacing its Transformerbased processing blocks with Mamba-based blocks [9] would improve the system’s accuracy-complexity tradeoff. Using SmolVLA as reference backbone is particularly well-suited in the case of this study as it constitutes a state-of-the-art VLA model in terms of achieving high task success rates while featuring lower compute complexity. 

In SmolVLA, a pre-trained vision-language backbone conditions a flow-matching Action Expert (AE) through layerwise cross-attention, and the AE alternates cross-attention layers (which ground action features with the multimodal input representation) with causal self-attention layers (which exchange information among entries within the noisy action 

sequence output). This alternation within the AE between cross- and self-attention enables the direct replacement the intra-chunk self-attention temporal mixers, while keeping fixed the remaining layers. Hence, we replace all causal selfattention layers within SmolVLA’s AE with Mamba selective state-space model (SSM) blocks [9]. Fig. 2 summarizes our proposed pipeline and shed light on the difference between the two model variants considered in this work. 

Indeed, Mamba-based SSMs are a well-suited candidate for replacing Transformer-based self-attention layers since Mamba implements input-dependent state-space dynamics through causal recurrence [9]. An action chunk is a short, ordered control sequence in which later commands should remain compatible with earlier ones, so a selective recurrent representation may supply a useful _inductive bias_ for intra-chunk coordination. The open question is whether using Mamba SSMs _improves the accuracy of later actions within the generated chunk_ once they are actually executed. 

To address this question, the key contributions of this paper are the following: 

- 1) We present a novel study on the impact of intra-chunk temporal mixing within flow-matching VLA AEs. We replace SmolVLA’s causal self-attention layers with Mamba-based SSM mixers while keeping the remaining architecture, flow-matching objective, and optimization protocol fixed. 

- 2) We evaluate both our Mamba-based and the Transformer-based reference across three execution 

   - horizons using the standard LIBERO benchmark suites. 

- 3) Crucially, we show that our Mamba-based AE significantly improves the VLA’s average success rate when using longer action execution horizons, corresponding to feasible real-time system deployments (e.g., an improvement of +7 _._ 8% for _N_ = 50 and +3 _._ 7% for _N_ = 25). 

- 4) We also demonstrate that our Mamba-based AE reaches a similar success rate of _∼_ 76% compared to the Transformer-based variant when _N_ = 1, while reducing the overall VLA model parameter count by 24% due to the compute-efficient nature of Mamba. 

This paper is organized as follows. Section II overviews the related works. Section III introduces our proposed methods. Section IV details our experimental setup. Section V presents our experimental results and discussions. Finally, conclusions are provided in Section VI. 

## II. RELATED WORK 

## _A. Vision-language-action policies and generative AEs_ 

VLA models adapt pretrained vision-language representations to robot control using either discrete action tokens or continuous action generators. OpenVLA treats actions as tokenized outputs of a large vision-language model [4], whereas _π_ 0 and SmolVLA use flow-matching AEs to generate continuous action sequences [5], [6]. SmolVLA is particularly suitable for the present study because its expert alternates cross-attention grounding with causal temporal mixing. This factorization allows the temporal operator to be modified without changing how visual and linguistic information conditions the action sequence. 

## _B. Action chunking and the execution horizon_ 

Action Chunking with Transformers demonstrated that predicting multiple future actions can improve the temporal coherence of imitation-learning policies [7]. Diffusion Policy subsequently modeled action chunks as conditional generative trajectories and introduced receding-horizon execution, in which only a prefix of each predicted chunk is applied before the plan is updated from a new observation [8]. The length of that prefix is the variable we sweep in this study. Its introduction established action generation and action execution as related but separable components of a chunked policy. 

A more recent line of work targets the cost of the resulting open-loop interval directly. Real-time chunking addresses asynchronous inference by constraining newly generated chunks to remain compatible with actions already committed for execution [15]. Concurrent work monitors latent visual dynamics during execution and truncates the remaining chunk once persistent deviation is detected, yielding an eventtriggered adaptive horizon [23]. Both keep the underlying policy fixed and intervene at inference time. Our study operates at the opposite end of the same axis: we hold the execution mechanism fixed and vary the operator that produces the chunk, which isolates how much of the horizon sensitivity is attributable to the architecture itself. The two directions compose, since a policy whose chunks degrade more slowly 

gives any execution-time monitor a longer usable interval before it must intervene. 

## _C. State-space models in robot learning_ 

Mamba introduced selective, input-dependent state-space dynamics as a competitive sequence-modeling architecture [9]. Several robotic systems have since used Mamba in different parts of the perception and control pipeline. RoboMamba integrates a Mamba-based multimodal model with a poseprediction head for robotic reasoning and manipulation [10]. MaIL develops a Mamba encoder-decoder architecture for imitation learning, while Mamba Policy combines SSM and attention components within a 3D diffusion policy [11], [12]. MTIL uses recurrent state to summarize observation and action history for temporally ambiguous tasks [13]. X- IL studies a broader modular policy design space in which Mamba and flow-matching components can be interchanged [20]. FlowRAM uses Mamba for multimodal fusion within a region-aware flow-matching policy that predicts manipulation keyframes [14]. In contrast, the present work keeps the VLA backbone and grounding pathway fixed, replaces the causal temporal-mixing layers that operate across action positions, and evaluates the resulting experts as the execution horizon changes. This isolates intra-chunk temporal modeling from perception, historical context encoding, and execution-time correction. 

## III. METHODS 

## _A. Problem Formulation_ 

We consider a language-conditioned manipulation policy that maps the current robot observation and a natural-language instruction to a chunk of future actions. At environment step _t_ , the input observation to the model is 


where _It_ = _{It_<sup>(</sup><sup>_v_)</sup> _}_<sup>_V_</sup> _v_ =1<sup>denotestheavailableRGBcamera</sup> views and _st ∈_ R<sup>_Ds_</sup> denotes the robot state. When conditioned on an instruction _ℓ_ describing the desired manipulation task, the policy generates an action chunk 


We use the SmolVLA action representation with _H_ = 50 and _Da_ = 7 dimensional output action vectors [6]. Each action contains a three-dimensional end-effector translation increment, a three-dimensional rotation increment, and a scalar gripper command. 

Our reference baseline model is SmolVLA, which combines a pretrained vision-language backbone with a conditional flowmatching action expert. The frozen backbone encodes the camera views, robot state, and instruction into layerwise and multimodal features: 


where _ϕ_ remains fixed during policy training and _LZ_ denotes the number of retained backbone layers. These features provide the keys and values used by the cross-attention layers of the AE within the VLM. 

~~(~~ _k_ ) **B** _i_ depends on both ∆<sup>(</sup> _i_<sup>_k_)</sup> and **B**<sup>(</sup> _i_<sup>_k_)</sup> . This selectivity allows the mixer to regulate how information is retained, updated, or suppressed across the ordered positions of the action chunk. 

## _D. Execution Horizon_ 

## _B. Conditional Flow-Matching AE_ 

Let ( _ot, ℓ,_ **A** _t_ ) _∼D_ denote a training example containing a demonstrated action chunk, and let **_ϵ_** _∼N_ ( **0** _,_ **I** ). We parameterize the interpolation from data at _τ_ = 0 to noise at _τ_ = 1 as: 


The endpoints are therefore: **A**<sup>0</sup> _t_<sup>=</sup><sup>**A**</sup><sup>_t_and</sup><sup>**A**1</sup> _t_<sup>=</sup><sup>**_ϵ_**. The target</sup> velocity along this path is 


The AE _vθ_ is trained by minimizing: 


where _p_ ( _τ_ ) is the original SmolVLA flow-time sampling distribution and is shared by both the baseline and our Mamba-based variant. At inference, sampling begins from **A**<sup>1</sup> _t_<sup>_∼N_(</sup><sup>**0**</sup><sup>_,_</sup><sup>**I**),andthelearnedvelocityfieldisintegrated</sup> from _τ_ = 1 to _τ_ = 0 using ten Euler steps to produce the predicted action chunk. 

## _C. Mamba-Based Intra-Chunk Temporal Mixing_ 

The SmolVLA AE alternates cross-attention grounding layers with causal self-attention layers. We denote the baseline Transformer expert by **B0** . Our variant, **M1** , retains all eight cross-attention layers and solely replaces the eight causal self-attention layers with temporal mixers based on the original Mamba SSM. (Mamba-1) [9]. Here, M1 denotes our experimental model variant and should not be confused with the Mamba-1 architecture version. Other than the crossattention layers, the vision-language backbone; cross-attention grounding pathway; action and flow-time embeddings; actiontoken width; chunk length; and output head remain unchanged between B0 and M1. 

Let: 


denote the sequence of action-token representations entering temporal layer _k_ , where _d_ is the action-token dimension. The core Mamba-1 selective scan processes the chunk positions _i_ = 1 _, . . . , H_ according to 


with **h**<sup>(</sup> 0<sup>_k_)</sup> = **0** . In Mamba-1, the continuous state transition parameters are learned and shared across sequence positions, whereas the discretization step ∆<sup>(</sup> _i_<sup>_k_)</sup> and the projections **B**<sup>(</sup> _i_<sup>_k_)</sup> and **C**<sup>(</sup> _i_<sup>_k_)</sup> depend on the current token representation. Conse- ~~(~~ _k_ ) quently, the discretized transition **A** _i_ depends on ∆<sup>(</sup> _i_<sup>_k_)</sup> , while 

Both experts predict a fixed chunk of _H_ = 50 actions. At inference, the execution horizon _N_ specifies how many actions are applied before the policy incorporates a new observation and generates another chunk: 


At _N_ = 1, the policy replans after every executed action. At _N_ = 50, it executes the complete predicted chunk before replanning. The trained weights are held fixed throughout the horizon sweep. Varying _N_ therefore tests how task success changes as increasingly long prefixes of the same type of predicted chunk are used without observation-conditioned correction. 

## IV. EXPERIMENTAL SETUP 

## _A. Implementation Details_ 

Our experimental setup is built using the popular LeRobot framework [24] in _Python_ . The vision-language backbone is SmolVLM2-500M-Video-Instruct [25], of which we retain the first 16 language-model layers, so _LZ_ = 16 in (3). Input images are resized to 512 _×_ 512 to match the backbone resolution. The backbone is initialized from its pretrained weights and frozen throughout learning, such that our training setup updates the AE alone. The expert stacks eight cross-attention grounding layers and eight intra-chunk temporal layers and predicts chunks of _H_ = 50 seven-dimensional delta endeffector actions under the conditional flow-matching objective in (6). B0 is the unmodified SmolVLA expert, whose temporal layers are causal self-attention. M1 replaces those eight layers with Mamba SSM mixers and leaves the grounding layers untouched, significantly reducing the trainable expert from 99 _._ 9M to 76 _._ 3M parameters (a reduction of 23 _._ 6%). The frozen backbone is identical in both variants and is excluded from this count. 

Both variants are trained for 30 _,_ 000 updates at a global batch size of 64 using AdamW ( _β_ 1 = 0 _._ 9, _β_ 2 = 0 _._ 95) with a cosine schedule that warms up over 1 _,_ 000 steps and decays the learning rate from 1 _×_ 10<sup>_−_4</sup> to 2 _._ 5 _×_ 10<sup>_−_6</sup> . At inference the flow-matching sampler is fixed to ten Euler steps, and the execution horizon is swept over _N ∈{_ 1 _,_ 25 _,_ 50 _}_ . 

## _B. Benchmark and Protocol_ 

We evaluate B0 and M1 on the widely-used LIBERO multi-task simulation benchmark [16], which underpins the evaluation of many recent VLA policies [4]–[6], [18], [19]. LIBERO organizes visuomotor manipulation into four suites, Spatial, Object, Goal, and Long, each containing ten tasks for a total of 40, chosen to isolate distinct generalization axes: spatial arrangement, object identity, task goal, and longhorizon composition. Each task runs in robosuite with a Franka Panda arm [21]. We follow the standard LIBERO 


Fig. 3. Four-suite mean success rate as a function of the execution horizon _N_ , mean across three seeds with _±_ 1 standard deviation bands. Annotations give the M1 _−_ B0 gap at each horizon. 

TABLE I 

FOUR-SUITE MEAN SUCCESS RATE (%) AS A FUNCTION OF EXECUTION HORIZON, MEAN _±_ STANDARD DEVIATION ACROSS SEEDS. THE FINAL COLUMN GIVES THE MEAN PER-TASK DIFFERENCE WITH A 95% BOOTSTRAP CONFIDENCE INTERVAL OVER THE 40 TASKS. 

|Horizon|B0|M1|M1_−_|B0 [95% CI]|
|---|---|---|---|---|
|_N_ = 1|75_._9_±_1_._8|**76**_._**2**_±_**1**_._**2**|+0_._3|[_−_3_._0_,_+3_._6]|
|_N_ = 25|71_._0_±_2_._7|**74**_._**7**_±_**1**_._**7**|+3_._7|[<br>0_._0_,_+7_._3]|
|_N_ = 50|53_._9_±_2_._3|**61**_._**8**_±_**1**_._**7**|+7_._8 [|+3_._0_,_+12_._6]|
|_N_=1_→_50 drop|22.0|**14.5**||7.5 less|


emerges only as the policy is asked to execute longer prefixes without new observations. 

Moreover, Moving from _N_ = 1 to _N_ = 50, B0 loses 22 _._ 0 points and M1 loses 14 _._ 5, so M1 better retains 7 _._ 5 additional points when the policy must execute a complete predicted chunk before receiving new visual feedback (Table I). M1 obtains this retention with a smaller AE which 76 _._ 3M weights against 99 _._ 9M trainable parameters for B0. 

## _B. Per-Suite Structure_ 

evaluation protocol. Both variants are trained on the released demonstration set of 1 _,_ 693 episodes covering all 40 tasks [16], [17]<sup>1</sup> , and each task is evaluated over ten rollout trials. 

## _C. Evaluation Metrics_ 

The primary metric is task success rate. We compute success separately for each task and multiple model training seeds, then average across the ten tasks within each suite. Reported suite values are means and standard deviations across three seeds. For each horizon we treat the 40 tasks as paired observations, average each task over the three seeds, and report the mean per-task difference between M1 and B0, as well as the 95% confidence interval derived from 10 _,_ 000 bootstrap resamples of the tasks. 

For model _m ∈{_ B0 _,_ M1 _}_ , sensitivity to reduced replanning is summarized by: 


where a smaller value indicates stronger success retention, and the between-model difference at a given horizon is: 


## _A. Impact of the Execution Horizon on the Success Rates_ 

Table I and Fig. 3 show the four-suite mean success rate at each horizon. The two experts are separated most clearly under full-chunk execution. At _N_ = 50, M1 reaches 61 _._ 7% against 53 _._ 9% for B0, a significant boost of 7 _._ 8 points over the 40 tasks. For _N_ = 25, a boost of 3 _._ 7 points is observed, and 0 _._ 3 points at _N_ = 1. Under per-action replanning (where _N_ = 1), the two mixers achieves on-par results, and the difference 

> 1LIBERO dataset: https://huggingface.co/datasets/physical-intelligence/ libero 

The aggregate advantage at _N_ = 50 is not uniform across suites, as shown in Table II and Fig. 4. M1 significantly outperforms B0 by 17 _._ 7 points on Object and by 10 _._ 0 points on Spatial, with a more moderate 4 _._ 7-point gain on Long. Goal is the exception, where B0 leads by a less significant 1 _._ 0 point gap. Object shows the clearest horizon-dependent reversal. B0 leads by 6 _._ 0 points under per-action replanning, 92 _._ 0% against 86 _._ 0%, and trails by 17 _._ 7 points at _N_ = 50. It is also important to note that Long is the hardest suite for both experts at every horizon, and the lead of M1 over B0 between the two mixers on Long is stable but small relative to the overall average performance gains of M1 over B0. 

## _C. Discussion on the results_ 

This study isolates the effect of the intra-chunk temporal mixer in a flow-matching VLA AE. The Mamba-based variant M1 exhibits stronger success retention at longer open-loop execution horizons, outperforming B0 by an average 3.7 percentage points at _N_ = 25 and 7.8 points at _N_ = 50, while the two variants perform comparably at _N_ = 1 (with M1 further reducing model weight complexity by 24%). The longerhorizon settings are practically relevant because executing more actions from each generated chunk reduces the scheduled policy-call frequency, although it also delays the incorporation of new observations. 

A plausible interpretation for the clear superiority of our M1 model over B0 is that Mamba’s input-dependent causal recurrence provides a useful _inductive bias_ for coordinating ordered action positions within the chunk [9]. This is in contrast the Transformer-based variant which imposes temporal directionality in the Transformer mixer through an explicit causal attention mask [6]. This architectural distinction may help M1 preserve coordination among later actions when larger sections _N_ of the predicted chunk are executed before replanning. 


Fig. 4. LIBERO success rate as a function of execution horizon for B0 and M1, per suite. Curves show means across three seeds and shaded bands show _±_ 1 standard deviation across seeds. 

TABLE II 

PER-SUITE SUCCESS RATE (%) ACROSS ALL THREE EXECUTION HORIZONS, MEAN _±_ STANDARD DEVIATION OVER THREE SEEDS. 

||_N_|= 1|_N_ =|25|_N_ =|50|gap|
|---|---|---|---|---|---|---|---|
|Suite|B0|M1|B0|M1|B0|M1|@_N_=50|
|Spatial|79_._7_±_2_._4|80_._7_±_1_._2|67_._3_±_2_._6|74_._7_±_5_._2|53_._0_±_4_._9|63_._0_±_5_._9|+10_._0|
|Object|92_._0_±_1_._4|86_._0_±_0_._8|86_._0_±_1_._6|89_._3_±_3_._1|56_._7_±_3_._3|74_._3_±_1_._9|+17_._7|
|Goal|84_._7_±_3_._7|88_._0_±_1_._6|80_._0_±_7_._3|83_._3_±_2_._1|73_._3_±_2_._5|72_._3_±_1_._7|_−_1_._0|
|Long|47_._3_±_3_._9|50_._3_±_1_._7|50_._7_±_3_._1|51_._3_±_4_._5|32_._7_±_2_._1|37_._3_±_0_._9|+4_._7|
|Average|75.9|76.2|71.0|74.7|53.9|61.8|+7_._8|


## VI. CONCLUSION 

This paper has provided a novel investigation of Mambabased SMM modeling as an alternative to Transformer-based causal self-attention for intra-chunk temporal mixing in flowmatching VLA action experts, and how it affects task success as implementation-feasible long chunk prefixes are executed. Using a SmolVLA-based experimental setup, it has been demonstrated that the Mamba-based expert retains task success more effectively when using longer open-loop execution horizons, thereby enabling a better accuracy-complexity tradeoff for real-time system deployment. Specifically, under fullchunk execution _N_ = 50, our proposed method significantly outperforms the Transformer baseline by 7 _._ 8% while featuring a reduction of _∼_ 24% in terms of model weight complexity. Our SmolVLA-based experiments demonstrate that success rate at longer execution horizons not only depends on observation staleness, but also on how temporal dependencies within the action chunk are modeled. Future work will examine this behavior across additional VLA architectures, and validate the approach on physical robots. 

## REFERENCES 

- [1] Y. Zhang, E. L. Haß, K.-Y. Chao, N. Petrovic, Y. Song, C. Wu, and A. Knoll, “A Unified Perception-Language-Action Framework for Adaptive Autonomous Driving,” in _2025 3rd International Conference on Foundation and Large Language Models (FLLM)_ , 2025, pp. 1057– 1063, doi: 10.1109/FLLM67465.2025.11391008. 

- [2] Z. Guo, Z. Yagudin, A. Lykov, M. Konenkov, and D. Tsetserukou, “VLM-Auto: VLM-Based Autonomous Driving Assistant with Human-Like Behavior and Understanding for Complex Road Scenes,” in _2024 2nd International Conference on Foundation and Large Language Models (FLLM)_ , 2024, pp. 501–507, doi: 10.1109/FLLM63129.2024.10852498. 

- [3] V. Berman, A. Bazhenov, S. Satsevich, and D. Tsetserukou, “MissionGPT: Mission Planner for Mobile Robot Based on Robotics Transformer Model,” in _2024 2nd International Conference on Foundation and Large Language Models (FLLM)_ , 2024, pp. 201–206, doi: 10.1109/FLLM63129.2024.10852423. 

- [4] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, and C. Finn, “OpenVLA: An open-source vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 

- [5] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ 0: A vision-language-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [6] M. Shukor, D. Aubakirova, F. Capuano, P. Kooijmans, S. Palma, A. Zouitine, M. Aractingi, C. Pascal, M. Russi, A. Marafioti, S. Alibert, M. Cord, T. Wolf, and R. Cadene, “SmolVLA: A vision-languageaction model for affordable and efficient robotics,” _arXiv preprint arXiv:2506.01844_ , 2025. 

- [7] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” in _Robotics: Science and Systems_ , 2023. 

- [8] C. Chi, S. Feng, Y. Du, Z. Xu, E. Cousineau, B. Burchfiel, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” in _Robotics: Science and Systems_ , 2023. 

- [9] A. Gu and T. Dao, “Mamba: Linear-time sequence modeling with selective state spaces,” in _Conference on Language Modeling_ , 2024. 

- [10] J. Liu, M. Liu, Z. Wang, P. An, X. Li, K. Zhou, S. Yang, R. Zhang, Y. Guo, and S. Zhang, “RoboMamba: Efficient vision-language-action model for robotic reasoning and manipulation,” in _Advances in Neural Information Processing Systems_ , vol. 37, 2024. 

- [11] X. Jia, Q. Wang, A. Donat, B. Xing, G. Li, H. Zhou, O. Celik, D. Blessing, R. Lioutikov, and G. Neumann, “MaIL: Improving imitation learning with selective state space models,” in _Proceedings of the 8th Conference on Robot Learning_ , vol. 270, 2025, pp. 3888–3907. 

Generation with LLMs for Robots,” in _2025 3rd International Conference on Foundation and Large Language Models (FLLM)_ , 2025, pp. 982–989, doi: 10.1109/FLLM67465.2025.11391122. 

- [12] J. Cao, Q. Zhang, J. Sun, J. Wang, H. Cheng, Y. Li, J. Ma, K. Wu, Z. Xu, Y. Shao, W. Zhao, G. Han, Y. Guo, and R. Xu, “Mamba policy: Towards efficient 3D diffusion policy with hybrid selective state models,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2025. 

- [13] Y. Zhou, Y. Lin, F. Peng, J. Chen, K. Huang, H. Yang, and Z. Yin, “MTIL: Encoding full history with Mamba for temporal imitation learning,” _IEEE Robotics and Automation Letters_ , vol. 10, no. 11, pp. 11761–11767, 2025. 

- [14] S. Wang, L. Wang, S. Zhou, J. Tian, J. Li, H. Sun, and W. Tang, “FlowRAM: Grounding flow matching policy with region-aware Mamba framework for robotic manipulation,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2025, pp. 12176–12186. 

- [15] K. Black, M. Y. Galliker, and S. Levine, “Real-time execution of action chunking flow policies,” in _Advances in Neural Information Processing Systems_ , 2025. 

- [16] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “LIBERO: Benchmarking knowledge transfer for lifelong robot learning,” in _Advances in Neural Information Processing Systems, Datasets and Benchmarks Track_ , 2023. 

- [17] K. Pertsch, K. Stachowicz, B. Ichter, D. Driess, S. Nair, Q. Vuong, O. Mees, C. Finn, and S. Levine, “FAST: Efficient action tokenization for vision-language-action models,” _arXiv preprint arXiv:2501.09747_ , 2025. 

- [18] Octo Model Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, J. Luo, Y. L. Tan, L. Y. Chen, P. Sanketi, Q. Vuong, T. Xiao, D. Sadigh, C. Finn, and S. Levine, “Octo: An open-source generalist robot policy,” in _Robotics: Science and Systems_ , 2024. 

- [19] Q. Zhao, Y. Lu, M. J. Kim, Z. Fu, Z. Zhang, Y. Wu, Z. Li, Q. Ma, S. Han, C. Finn, A. Handa, T.-Y. Lin, G. Wetzstein, M.-Y. Liu, and D. Xiang, “CoT-VLA: Visual chain-of-thought reasoning for visionlanguage-action models,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2025, pp. 1702–1713. 

- [20] X. Jia, A. Donat, X. Huang, X. Zhao, D. Blessing, H. Zhou, H. A. Wang, H. Zhang, Q. Wang, R. Lioutikov, and G. Neumann, “X-IL: Exploring the design space of imitation learning policies,” _arXiv preprint arXiv:2502.12330_ , 2025. 

- [21] Y. Zhu, J. Wong, A. Mandlekar, R. Mart´ın-Mart´ın, A. Joshi, K. Lin, A. Maddukuri, S. Nasiriany, and Y. Zhu, “robosuite: A modular simulation framework and benchmark for robot learning,” _arXiv preprint arXiv:2009.12293_ , 2020. 

- [22] S. Balasubramanian, A. Melendez-Calderon, A. Roby-Brami, and E. Burdet, “On the analysis of movement smoothness,” _Journal of NeuroEngineering and Rehabilitation_ , vol. 12, no. 1, p. 112, 2015. 

- [23] Y. Pan, M. Pan, Q. Lu, J. Huang, M. Zhang, S. Huang, X. Li, J. Zhang, Y. Shen, X. Zhang, and W. Zhang, “VLA-Corrector: Lightweight detect-and-correct inference for adaptive action horizon,” _https://arxiv.org/abs/2607.01804_ , 2026. 

- [24] R. Cadene, S. Alibert, A. Soare, Q. Gallouedec, A. Zouitine, S. Palma, P. Kooijmans, M. Aractingi, M. Shukor, D. Aubakirova, M. Russi, F. Capuano, C. Pascale, J. Choghari, J. Moss, and T. Wolf, “LeRobot: Stateof-the-art machine learning for real-world robotics in PyTorch,” GitHub repository, 2024. [Online]. Available: https://github.com/huggingface/ lerobot 

- [25] A. Marafioti, O. Zohar, M. Farr´e, M. Noyan, E. Bakouch, P. Cuenca, C. Zakka, L. Ben Allal, A. Lozhkov, N. Tazi, _et al._ , “SmolVLM: Redefining small and efficient multimodal models,” _arXiv preprint arXiv:2504.05299_ , 2025. 

- [26] S. Hadish, V. Bojkovic, M. Aloqaily, and M. Guizani, “Language Models at the Edge: A Survey on Techniques, Challenges, and Applications,” in _2024 2nd International Conference on Foundation and Large Language Models (FLLM)_ , 2024, pp. 262–271, doi: 10.1109/FLLM63129.2024.10852473. 

- [27] A. Lykov and D. Tsetserukou, “LLM-BRAIn: AI-Driven Fast Generation of Robot Behaviour Tree Based on Large Language Model,” in _2024 2nd International Conference on Foundation and Large Language Models (FLLM)_ , 2024, pp. 392–397, doi: 10.1109/FLLM63129.2024.10852491. 

- [28] J. Flerlage, A. Acker, D. Scheinert, S. Becker, H. Yous, K. Reddy, I. Farhat, H. Hacid, and O. Kao, “From Intentions to Actions: Workflow 

