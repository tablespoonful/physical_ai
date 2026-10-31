---
title: "HiMoE-VLA: Hierarchical Mixture-of-Experts for Generalist Vision-Language-Action Policies"
date: "2025-12-05"
authors: "Zhiying Du; Bei Liu; Yaobo Liang; Yichao Shen; Haidong Cao; Xiangyu Zheng"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2512.05693
pdf: https://arxiv.org/pdf/2512.05693
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.05693)** / [論文ページ](https://arxiv.org/abs/2512.05693)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **HiMoE-VLA:HierarchicalMixture-of-Experts for Generalist Vision-Language-Action Policies** 

**Zhiying Du**<sup>1</sup> **,**<sup>_∗_</sup> **Bei Liu**<sup>2</sup> **, Yaobo Liang**<sup>2</sup> **, Yichao Shen**<sup>3</sup><sup>_∗_</sup> **, Haidong Cao**<sup>1</sup> **, Xiangyu Zheng**<sup>1</sup> **, Zhiyuan Feng**<sup>4</sup><sup>_∗_</sup> , **Zuxuan Wu**<sup>1</sup> ,<sup>_†_</sup> **Jiaolong Yang**<sup>2</sup><sup>_†_</sup> , **Yu-Gang Jiang**<sup>1</sup> 

1Fudan University 2Microsoft Research Asia 

3Xi’an Jiaotong University 4Tsinghua University 

**Abstract:** Generalist vision–language–action (VLA) policies are typically trained on heterogeneous mixtures of robot demonstrations spanning diverse embodiments, action spaces, and observation configurations. Modeling such heterogeneity with a shared dense action module can induce negative transfer, particularly when action spaces or visual observations differ across data sources. We address this issue with HiMoE-VLA, a VLA framework built around a Hierarchical Mixtureof-Experts (HiMoE) action module. HiMoE uses Action-Space MoE layers at the input/output boundaries to specialize computation for distinct action spaces, Heterogeneity-Balancing MoE layers in neighboring layers to provide balanced capacity for residual variation in observations, scenes, and embodiments, and dense Transformer blocks in the middle to integrate shared representations. Two auxiliary objectives further guide this hierarchy: a contrastive Action-Space Regularization objective for boundary specialization and a load-balancing objective for stable expert utilization. HiMoE-VLA reaches 3.98 on CALVIN, 98.0% on LIBERO, and 75.0% and 63.7% average success on real xArm7 and ALOHA tasks; under controlled heterogeneous co-training, it turns the negative transfer observed in strong baselines into positive transfer. The code and models are publicly available at `https://github.com/ZhiyingDu/HiMoE-VLA` . 

**Keywords:** Vision Language Action Model, Robotic, Manipulation 

## **1 Introduction** 

Vision–language models (VLMs) have emerged as powerful multimodal representation learners [1, 2, 3, 4, 5, 6], motivating their use as backbones for vision–language–action (VLA) policies that map visual observations and language instructions to robot actions [7, 8, 9, 10, 11, 12, 13, 14, 15, 16]. Scaling such policies, however, differs fundamentally from scaling vision or language models: robot data are not organized around a single standardized input–output interface. Demonstrations vary across embodiments, action spaces, state representations, control frequencies, camera viewpoints, and teleoperation or collection protocols. These variations are not merely nuisance factors; they alter the semantics of both observations and action supervision, making naive data mixing prone to interference and limiting transfer across datasets and embodiments. 

Recent VLA models [17, 18, 19, 20, 21, 22, 23, 24] commonly pre-train on large heterogeneous mixtures such as Open X-Embodiment (OXE) [25] and then fine-tune on target domains. This recipe is effective, but most models still process heterogeneous action and observation signals through a shared dense action module. As we show in controlled co-training studies (Tables 5 and 7), this design can turn additional heterogeneous data into _negative transfer_ when action spaces or observation configurations differ. The central question is therefore how to structure the action module so that incompatible factors are separated while transferable structure remains shared. 

> _∗_ Work done during research internship at Microsoft Research. 

> _†_ Corresponding author. 

To address this problem, we propose **HiMoE-VLA** , a VLA framework with a **Hierarchical Mixtureof-Experts (HiMoE)** action module. HiMoE assigns different sources of robot-data heterogeneity to different depths of the action module. Because data from different action spaces carry distinct physical semantics and are largely non-transferable across parameterizations (Appendix C.1), HiMoE isolates action-space-specific computation with Action-Space MoE (AS-MoE) layers at the input/output boundaries. Heterogeneity-Balancing MoE (HB-MoE) layers adjacent to those boundaries provide balanced sparse capacity for remaining observation variability, while dense Transformer blocks in the middle integrate the resulting representations into a shared action representation. 

HiMoE-VLA is trained with a flow-matching objective for action generation and two routing regularizers matched to these roles. Action-Space Regularization (AS-Reg) applies a supervised contrastive loss to AS-MoE routing distributions, encouraging tokens from the same action-space/embodiment group to use similar expert patterns. Heterogeneity-Balancing Regularization (HB-Reg) adopts the DeepSeekMoE load-balancing loss [26] to prevent the HB-MoE expert pool from collapsing onto a small subset of experts. Together, these losses encourage boundary-level specialization while maintaining balanced capacity for remaining heterogeneity. 

After pre-training on OXE [25] and public ALOHA data [27, 28, 24], we fine-tune and evaluate HiMoE-VLA on CALVIN [29], LIBERO [30], and two real robot platforms: xArm7 and ALOHA. HiMoE-VLA improves over strong VLA baselines in both simulation and real-world evaluations, and controlled heterogeneity experiments show that it converts the negative transfer of dense baselines into positive transfer under cross-action and observation/scene co-training. 

Our contributions are: 

- We identify action-space heterogeneity as a major source of negative transfer in multi-source VLA training and propose a hierarchical MoE action module that separates action-spacespecific computation while retaining balanced capacity for remaining variability. 

- We introduce AS-Reg and HB-Reg, two routing-level objectives that respectively encourage action-space-specific routing in AS-MoE and balanced expert utilization in HB-MoE. 

- We validate HiMoE-VLA across CALVIN, LIBERO, xArm7, and ALOHA, and show controlled gains under heterogeneous co-training. 

## **2 Related Work** 

**Vision–Language–Action Policies.** Recent VLA models couple pretrained language or vision– language backbones with robot action generation, enabling instruction-conditioned manipulation from visual observations. RT-2 [17] and OpenVLA [18] cast actions as discrete tokens, while RoboFlamingo [31], Octo [19], UniVLA [32], and _π_ 0 [20] explore continuous or diffusion/flowbased action prediction. Other works exploit video pretraining to learn visuomotor representations from Internet-scale data without explicit action labels [33, 34, 35]. These methods demonstrate the value of large pretrained backbones for robotics. However, these systems typically use a largely shared action module, leaving action-space and observation heterogeneity to be absorbed by the same dense computation. 

**Learning from Heterogeneous Robot Data.** Large multi-robot datasets such as Open X- Embodiment [25] expose a central difficulty for generalist policies: demonstrations differ not only in tasks, but also in embodiments, state/action parameterizations, observation configurations, and control conventions. Existing methods address this mismatch mainly through interface alignment or conditioning. RDT-1B [24] unifies state and action representations for bimanual manipulation; HPT [36] uses dataset-specific stems and heads to align diverse inputs and outputs; and recent generalist policies such as SpatialVLA [22], OpenVLA-OFT [23], and GR00T-style systems [13] incorporate stronger spatial, action, or embodiment-aware designs. These approaches reduce part of the mismatch, but they do not explicitly separate action-space discrepancies from other sources of robot-data heterogeneity inside the action module. HiMoE-VLA is complementary: it keeps a shared 

2 


Figure 1: Overview of HiMoE-VLA. The left blue part illustrates the VLM backbone initialized from PaliGemma [1], and the right orange part depicts our proposed action module with a novel Hierarchical Mixture-of-Experts (HiMoE), which is responsible for processing different robot states and noisy actions and generating final action outputs. 

policy backbone and unified interface, while using a hierarchy that isolates action-space-specific computation before allocating balanced capacity to remaining variability. 

**Mixture of Experts.** Mixture-of-Experts (MoE) models have been widely used for sparse scaling in LLMs [37, 38], and later extended to vision [39] and diffusion models [40]. Standard MoE layers route each token to a small subset of experts using top- _k_ gating, with auxiliary mechanisms for routing efficiency and load balancing, including hashing-based routing [41], dynamic expert activation [42, 43], and DeepSeek-style balancing losses [26]. In contrast, our use of MoE is not primarily a sparse-scaling mechanism: we impose a depth-wise hierarchy in which AS-MoE layers specialize at the action-space boundaries, HB-MoE layers provide balanced capacity for residual heterogeneity nearby, and dense Transformer layers integrate shared representations in the middle. This differs from a flat MoE stack, where all experts at all depths are asked to absorb all sources of variation simultaneously. 

## **3 Method** 

### **3.1 Problem Formulation** 

At time step _t_ , the policy receives a language instruction _l_ , robot proprioception _qt_ , and RGB observations _ot_ = [ _It_<sup>1</sup><sup>_, . . . , I_</sup> _t_<sup>_n_],andpredictsanactionchunk</sup><sup>_At_=[</sup><sup>_at, at_+1</sup><sup>_, . . . , at_+</sup><sup>_H−_1]over</sup> horizon _H_ : 

_πθ_ ( _l, qt, ot_ ) _�→ At._ 

The semantics of _qt_ and _at_ depend on the data source: an action may represent end-effector deltas, joint-angle commands, or their embodiment-specific variants. We therefore map states and actions into a unified vector interface before feeding them to the action module, while retaining a categorical action-space/embodiment identity _c_ for routing regularization. Details of the vector layout, padding, and validity masks are provided in Appendix B. 

### **3.2 Network Architecture** 

HiMoE-VLA consists of a pretrained vision–language model and a flow-matching action expert (Fig. 1). The VLM encodes the instruction and multi-view images; the action expert receives 

3 


Figure 2: Detailed structure of the Hierarchical Mixture-of-Experts (HiMoE). The architecture follows a layered hierarchy: AS-MoE modules at the boundaries specialize in action-space variations, adjacent HB-MoE modules provide balanced capacity for residual heterogeneity, and the central Transformer blocks serve as shared layers for cross-domain knowledge integration. 

proprioception, the noised action chunk, and the flow timestep, and predicts the denoising vector field conditioned on VLM features. 

### **3.2.1 Vision-Language Module** 

We instantiate the VLM with PaliGemma [1], following _π_ 0 [20]. Rather than conditioning the action expert only on the final VLM representation, we expose intermediate language-model key–value (KV) states to the corresponding action-expert layers. This layer-wise conditioning lets the action tokens attend to both semantic instruction information and lower-level visual cues; at inference time, the VLM KV states are cached for efficient rollout. 

### **3.2.2 Action Module with Hierarchical MoE** 

The action expert embeds the unified proprioceptive vector, the noised action chunk, and the flow timestep into action tokens. It then processes these tokens with a hierarchy of Transformer-style blocks whose feed-forward sublayers are selectively replaced by MoE modules (Fig. 2). The outermost blocks use **Action-Space MoE (AS-MoE)** to specialize computation for action-space discrepancies such as joint-angle versus end-effector control. The neighboring inner blocks use **Heterogeneity-Balancing MoE (HB-MoE)** to provide balanced sparse capacity for residual variability such as embodiment and scene differences. The central blocks remain dense Transformers, encouraging information that has passed through the specialization layers to be integrated into a shared representation. 

Each MoE block uses top- _K_ routing over _N_ experts and includes a shared expert following DeepSeekMoE [26]. The shared expert is applied to every token in parallel with the routed experts, and its output is added to the routed output. This captures heterogeneity-agnostic computation while allowing the routed experts to focus on source-specific variation; its ablation is reported in Appendix C.2. 

### **3.3 Training Objective** 

HiMoE-VLA is trained with a flow-matching loss for action generation and two routing regularizers matched to the hierarchy: AS-Reg for boundary action-space specialization and HB-Reg for balanced 

4 

utilization of the adjacent HB-MoE experts. The objective is 


**Flow-Matching Loss.** We adopt the flow-matching objective [44] to model the conditional distribution of action sequences, as it provides a stable and efficient alternative to traditional diffusion training. Given an action chunk _At_ = [ _at, at_ +1 _, . . . , at_ + _H−_ 1], flow matching defines a continuoustime trajectory that transports a noise distribution to the target action distribution: 


The model learns a vector field _vθ_ that predicts the denoising direction: 


During training, _τ_ is sampled from a Beta distribution following [20]. At inference time, future actions are generated by integrating the learned vector field from _τ_ = 0 to _τ_ = 1, starting from Gaussian noise. 

**Action-Space Regularization (AS-Reg).** The **AS-MoE** , placed at the boundary layers, is designed to capture action-space variations. Let _cu_ denote the action-space/embodiment identity of token _u_ (provided by dataset metadata, e.g., joint-angle vs. end-effector), and _r_ ˆ _u ∈_ R<sup>_N_</sup> the _ℓ_ 2-normalized routing probability vector of the AS-MoE router. We define the positive and anchor-excluded index sets 


and adopt a supervised contrastive objective (log-inside form) over the routing distributions: 


where _U_ + =<sup>�</sup> _u_<sup>1[</sup><sup>_|P_(</sup><sup>_u_)</sup><sup>_|>_0] and</sup><sup>_β_=0</sup><sup>_._1; if</sup><sup>_U_+=0, the AS-Reg term is skipped for that mini-</sup> batch. Excluding the anchor from _A_ ( _u_ ) removes the dominant self-similarity term exp(1 _/β_ ) from the denominator; the valid-anchor normalization and 1 _/|P_ ( _u_ ) _|_ averaging make the loss robust to batch composition and per-class frequency, so that AS-Reg aligns routing patterns within each action space and contrasts them across action spaces at the boundary layers. 

**Heterogeneity-Balancing Regularization (HB-Reg).** At the layers adjacent to AS-MoE, the **HBMoE** is intended to keep sparse capacity available for residual heterogeneity, such as embodiment, viewpoint, and scene variation, after action-space-specific computation has been separated. We adopt the standard load-balancing loss from DeepSeekMoE [26] as HB-Reg. Let _N_ be the number of experts, _K_ the top- _K_ width, _U_ the number of tokens, _si,u ∈_ [0 _,_ 1] the router’s softmax score for expert _i_ on token _u_ , and _ri,u_ = 1 _{u → i}_ the top- _K_ routing indicator. Define 


so that _L_ HB=1 at the balanced configuration _fi_ =1 _, Pi_ =1 _/N_ ; the factor _N_ keeps this reference value comparable across expert counts. Since _ri,u_ is non-differentiable, _fi_ is treated as a stop-gradient constant and gradients flow only through _si,u_ , redirecting probability mass from over-used experts (large _fi_ ) toward under-used ones. Statistics are computed per sequence and averaged across the batch. 

In summary, AS-Reg promotes **specialization** in the AS-MoE for action-space differences, while HB-Reg promotes **balanced utilization** of the adjacent HB-MoE experts. Together with the flowmatching loss, these objectives train the hierarchy to combine source-specific routing with shared action generation. 

5 

Table 1: Simulation benchmark results. CALVIN reports the average number of consecutively completed tasks; LIBERO reports success rates (%). 

|**Method**|**1**|**2**|**3**|**4**|**5**|**Sum.**|**Method**|**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Octo<br>OpenVLA<br>RDT-1B<br>DeeR<br>MDT|0.771<br>0.716<br>0.757<br>0.853<br>**0.937**<br>|0.535<br>0.385<br>0.495<br>0.696<br>0.845<br>|0.318<br>0.180<br>0.359<br>0.549<br>0.741<br>|0.206<br>0.088<br>0.243<br>0.420<br>0.644<br>|0.136<br>0.042<br>0.184<br>0.312<br>0.556<br>|1.97<br>1.41<br>2.04<br>2.83<br>3.72<br>|Diffusion Policy<br>Octo<br>OpenVLA<br>SpatialVLA<br>UniVLA|78.3<br>78.9<br>84.7<br>88.2<br>96.5|92.5<br>85.7<br>88.4<br>89.9<br>96.8|68.3<br>84.6<br>79.2<br>78.6<br>95.6|50.5<br>51.1<br>53.7<br>55.5<br>92.0|72.4<br>75.1<br>76.5<br>78.1<br>95.2|
|_π_0|0.914|0.830|0.739|0.676|0.599|3.76|_π_0|96.8|98.8|95.8|85.2|94.2|
|HiMoE-VLA|0.938|**0.866**|**0.794**|**0.723**|**0.659**|**3.98**|OpenVLA-OFT|97.6|98.4|97.9|94.5|97.1|
|FLOWER<br>**+ HiMoE**|0.974<br>**0.979**|0.924<br>**0.943**|0.869<br>**0.904**|0.813<br>**0.859**|0.749<br>**0.801**|4.35<br>**4.49**|_π_0_._5<br>HiMoE-VLA|**98.8**<br>98.2|98.2<br>**99.4**|98.0<br>**98.6**|92.4<br>**95.8**|96.8<br>**98.0**|
||(|) CALV|IN (_D →_|_D_)|||||(b) LIBER|O.|||


(a) CALVIN ( _D → D_ ). 

## **4 Experiments** 

We evaluate HiMoE-VLA along three axes: standard simulation performance, real-world transfer and generalization, and controlled analyses of heterogeneous co-training. The goal is to test not only final task success, but also whether the hierarchy prevents negative transfer under controlled action-space variation and shared-action observation/scene variation, while evaluating real-world performance after fine-tuning on distinct robot embodiments. The appendix provides full data, protocol, routing, and efficiency details. 

**Pre-training Dataset.** We pre-train on a large mixture of Open X-Embodiment (OXE) [25] and public ALOHA datasets [24, 28, 27], totaling 24.1M frames. OXE provides broad single-arm robot coverage, while ALOHA adds coordinated bimanual manipulation; Appendix A.1 lists the exact composition. 

**Implementation Details.** HiMoE-VLA has 4B parameters and is trained end-to-end on 16 A100 GPUs with DeepSpeed. The model consumes one third-person view, two wrist views, and unified state–action vectors covering single- and dual-arm settings. We use _N_ =32 experts with top- _K_ =4 routing and the AS/HB regularizers described in Sec. 3; Appendix B gives the vector layout, masks, optimization setup, and fine-tuning schedules, while Appendix C.11 reports overhead. 

### **4.1 Simulation Experiments** 

**Experiment setup.** We evaluate on CALVIN [29] under the _D→D_ long-horizon setting, which measures chained instruction completion after fine-tuning on environment D, and on the four LIBERO [30] suites, which test spatial, object, goal, and long-horizon generalization. In CALVIN tables, columns 1–5 report the success rate of completing at least _k_ consecutive subtasks in a five-subtask chain, and Sum. is the sum of these success rates. Appendix A.2 details tasks, preprocessing, baselines, and fine-tuning. 

**Results.** On CALVIN, HiMoE-VLA reaches 3 _._ 98 sum of completed subtasks, outperforming the strongest prior generalist _π_ 0 (3 _._ 76) and all other non-FLOWER baselines. Replacing FLOWER’s dense action expert with HiMoE further improves 4 _._ 35 to **4** _._ **49** , indicating that the architecture is compatible with a different training recipe. On LIBERO, HiMoE-VLA obtains the best average score (98.0%) and leads on Object, Goal, and Long, while _π_ 0 _._ 5 remains slightly stronger on Spatial. These results establish the base policy performance before the controlled heterogeneity studies in Sec. 4.3. 

### **4.2 Real-World Experiments** 

We evaluate on xArm7 single-arm and ALOHA dual-arm robots. 

**Experiment setup.** We test _Fruit-to-Plate_ , _Cup-in-Cup_ , and _Block-on-Block_ on xArm7, and _FoldShorts_ , _Cup-Handover_ , and _Scoop_ on ALOHA. These tasks cover pick-place, insertion, stacking, bimanual handover, scooping, and deformable-object folding. We report stage-level success and generalization to unseen distractors and novel objects/garments; Appendix A.2 gives demonstrations, settings, and trial counts. 

6 

Table 2: Real-world evaluation on xArm7 (single-arm) and ALOHA (dual-arm) robots. (a) xArm7 per-stage success rates; (b) ALOHA per-stage success rates. 

|Method|Fruit-<br>Pick|to-Plate <br>Place|Cup-i<br>Pick|n-Cup <br> Insert|Block<br> Pick|-on-Block<br>Stack|Avg.|Method|Cup-H<br>Grasp|andover<br>Trans|Place|Scoop<br> Scoop|Pour|Fold-<br> Once|Shorts <br> Twice|Avg.|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Octo-Base<br>OpenVLA<br>CogACT<br>_π_0<br>HiMoE-VLA|31.3<br>37.5<br>65.6<br>68.8<br>**81.3**|18.8<br>25.0<br>59.4<br>62.5<br>**75.0**|33.3<br>27.8<br>77.8<br>77.8<br>**88.9**|16.7<br>16.7<br>63.9<br>61.1<br>**72.2**|16.7<br>22.2<br>69.4<br>72.2<br>**83.3**|0.0<br>0.0<br>33.3<br>33.3<br>**50.0**|19.3<br>21.2<br>61.5<br>62.5<br>**75.0**|ACT<br>RDT-1B<br>_π_0<br>HiMoE-VLA|40.0<br>66.6<br>**80.0**<br>**80.0**|0.0<br>13.3<br>13.3<br>**26.6**|73.3<br>93.3<br>93.3<br>**100.0**|6.6<br>40.0<br>46.6<br>**53.3**|0.0<br>20.0 <br>26.6<br>**40.0 **|20.0<br> 53.3<br>66.6<br> **80.0**|6.6<br>46.6<br>53.3<br>**66.6**|20.9<br>47.5<br>54.2<br>**63.7**|
|||||||||(b)|ALOHA|dual-ar|m task|s (Tran|s=Tra|nsfer).|||


(a) xArm7 single-arm tasks. 

Table 3: Real-world generalization evaluation on single-arm (xArm7) and dual-arm (ALOHA) tasks under two scenarios: _Distractor Objects_ (unseen distractors) and _Novel Objects_ (previously unseen items). Entries are success rates (%) averaged over physical trials; Appendix A.2 reports the trial counts. 

|Method||Single-Arm|||Dual-Arm||
|---|---|---|---|---|---|---|
||Distractor|Novel|Avg.|Distractor|Novel|Avg.|
|OpenVLA|19.4|15.6|17.6|-|-|-|
|CogACT|52.8|50.0|51.5|-|-|-|
|RDT-1B|-|-|-|28.9|26.7|27.8|
|_π_0|58.3|53.1|55.9|40.0|26.7|33.4|
|HiMoE-VLA|**69.4**|**65.6**|**67.6**|**53.3**|**46.7**|**50.0**|


**Results.** Table 2 shows that HiMoE-VLA achieves the best average success on xArm7 (75.0%) and ALOHA (63.7%), improving over _π_ 0 by 12.5 and 9.5 points. The largest gains appear in coordinated transfer, pouring, and folding stages, where embodiment-specific control and longhorizon coordination are likely to matter. Table 3 further reports higher success rates than _π_ 0 on both single-arm (67.6% vs. 55.9%) and dual-arm settings (50.0% vs. 33.4%). Representative rollouts appear in Fig. 3 and Appendix Figs. 6–7. 

### **4.3 Model Analysis and Ablations** 

We ablate optimization, action-space heterogeneity, hierarchical design, and shared-action observation/scene heterogeneity. For CALVIN action-space experiments, D denotes environment D with joint-angle actions, while ABC denotes environments A/B/C with end-effector (EEF) actions; ABC+D mixes these two action parameterizations. Scalar entries are CALVIN Sum. scores unless otherwise stated. The main text includes the controls needed to support the core claims; Appendix C.3 defines all variants and reports full per-step results. **Effect of Warm-up and Pretraining.** The optimization Table 5: Action-space co-training on CALVIN. rows in Table 4 show that removing MoE warm-up or pretraining degrades CALVIN-D fine-tuning, confirming **Method D ABC+D** the value of pretrained representations and short expert Ours w/o MoE _π_ 0 3.8063.819 3.547 (3.777 ( **-0.259-0.042** )) adaptation. Appendix C.6 details the two-stage warm-up Full (HiMoE) 3.826 4.012 ( **+0.186** ) that first adapts MoE parameters before full fine-tuning. 

**Comparison with Other Methods on Handling Heterogeneous Action Spaces.** The heterogeneity rows compare HiMoE with separate heads and a GR00T-style embodiment indicator under CALVINABC-EEF + CALVIN-D-Joint co-training. HiMoE performs best without manual embodiment heads, suggesting that adaptive expert selection better balances specialization and sharing. Appendix C.7 audits the data/loss masking pipeline used to avoid padding artifacts. 

**Evaluation on Ability of HiMoE to Handle Heterogeneous Data.** Table 5 compares from-scratch training on CALVIN-D joint-angle data only with CALVIN-ABC (EEF) + CALVIN-D (joint-angle) 

Table 6: HiMoE component ablation on CALVIN ABC+D cotraining. 

|**Setting**|**Sum.**|
|---|---|
|w/o MoE|3.777|
|Full-HB-MoE|3.901|
|w/o AS-MoE|3.873|
|w/o HB-MoE|3.836|
|w/o Reg|3.835|
|Single-MoE+Reg|3.813|
|Full|**4.012**|


co-training. Heterogeneous co-training degrades _π_ 0 and the dense variant, whereas full HiMoE turns the mixture into a gain. Cross-action fine-tuning in Appendix C.10 shows the same trend, improving EEF and joint evaluation by +0 _._ 105 and +0 _._ 238 over isolated fine-tuning. 

7 


Figure 3: Qualitative examples of real-world executions on (top row) the single-arm xArm7 and (bottom row) the dual-arm ALOHA robot. The snapshots cover representative stages across tasks such as _Fruit-to-Plate_ , _Block-on-Block_ , _Cup-Handover_ , and _Scoop_ . 

Table 4: Main CALVIN ablations. 

|**Study**|**Setting**|**1**|**2**|**3**|**4**|**5**|**Sum.**|
|---|---|---|---|---|---|---|---|
||w/o warm-up|0.917|0.832|0.753|0.698|0.627|3.827|
|Opt.|w/o pretrain|0.928|0.845|0.752|0.686|0.615|3.826|
||Full|**0.938**|**0.866**|**0.794**|**0.723**|**0.659**|**3.980**|
||Sep. Heads|0.914|0.833|0.753|0.696|0.631|3.827|
|Hetero.|GR00T-Like|0.913|0.835|0.764|0.702|0.642|3.856|
||HiMoE|**0.943**|**0.864**|**0.797**|**0.734**|**0.674**|**4.012**|


**Role of Hierarchical MoE Components.** Table 6 shows that removing MoE layers, AS-MoE, HBMoE, or regularization consistently hurts performance, and a single non-hierarchical MoE remains weaker; full per-step results are provided in Table 11. The gap between _Full-HB-MoE_ (3.901) and full HiMoE (4.012) supports placing AS-MoE at boundary layers rather than merely adding sparse capacity. 

Appendix controls further rule out confounds: removing the shared expert drops CALVIN ABC+D co-training from 4 _._ 012 to 3 _._ 955 (Table 10); a parameter-matched dense model reaches only 3 _._ 801 despite more active parameters (Table 12); and removing loss/data masks in heterogeneous co-training degrades the dense baseline from 3 _._ 777 to 3 _._ 696 _/_ 3 _._ 626 (Table 13). 

### **Evaluating Sensor and Scene Heterogeneity Under** 

**a Shared Action Space.** To reduce action-space confounding, we co-train CALVIN-D and LIBERO under a shared EEF action parameterization. Because the two benchmarks still differ in task distribution, visual domain, and scene layout, this experiment should be viewed as a shared-action test of non-action heterogene- 

Table 7: Sensor/scene co-training with a shared EEF action space. 

|**Method**|**CALVIN**|**+LIBERO**|
|---|---|---|
|_π_0|3.776|3.504 (**-0.272**)|
|w/o MoE|3.788|3.665 (**-0.123**)|
|Standard MoE|3.808|3.862 (**+0.054**)|
|Full (HiMoE)|3.819|**3.966 (+0.147)**|


ity rather than a pure sensor-only intervention. Table 7 shows negative transfer for _π_ 0 and dense models, a small gain for standard MoE, and a larger gain for full HiMoE (+0 _._ 147), supporting the hierarchy beyond action-space differences. 

**Scaling the Number of Experts.** Appendix Table 9 shows that _N_ =32 _, K_ =4 performs best; larger _N_ gives diminishing returns and _K_ =8 is unstable. The appendix also reports modest efficiency overhead (about 7% training cost and 0 _._ 195s/action inference for _N_ =32 _, K_ =4) and routing heatmaps consistent with AS-MoE action-space specialization and HB-MoE balanced utilization. 

## **5 Conclusion** 

We presented HiMoE-VLA, a VLA framework that uses a hierarchical MoE action module to separate action-space-specific computation and allocate balanced capacity to residual sources of robot-data variation, including observations, scenes, and embodiments. Across CALVIN, LIBERO, and real xArm7/ALOHA tasks, HiMoE-VLA improves over strong baselines; controlled co-training studies further show that the hierarchy mitigates negative transfer under action-space and shared-action observation/scene variation beyond a pure capacity effect. 

**Limitations:** HiMoE-VLA assumes that each sample can be mapped into a unified state–action interface; failures may arise when annotations are missing, or mobile-manipulation settings differ substantially from our evaluated robots. Our experiments cover CALVIN, LIBERO, xArm7, and 

8 

ALOHA but not larger multi-robot mixtures, and we do not yet quantify safety or calibration under long-horizon distribution shift. Future work should further reduce routing and cross-attention overhead and broaden evaluation. 

9 

## **References** 

- [1] L. Beyer, A. Steiner, A. S. Pinto, A. Kolesnikov, X. Wang, D. Salz, M. Neumann, I. Alabdulmohsin, M. Tschannen, E. Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- [2] H. Touvron, L. Martin, K. Stone, P. Albert, A. Almahairi, Y. Babaei, N. Bashlykov, S. Batra, P. Bhargava, S. Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. 

- [3] J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- [4] D. Jiang, Y. Liu, S. Liu, J. Zhao, H. Zhang, Z. Gao, X. Zhang, J. Li, and H. Xiong. From clip to dino: Visual encoders shout in multi-modal large language models. _arXiv preprint arXiv:2310.08825_ , 2023. 

- [5] A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv, et al. Qwen3 technical report. _arXiv preprint arXiv:2505.09388_ , 2025. 

- [6] B. Xiao, H. Wu, W. Xu, X. Dai, H. Hu, Y. Lu, M. Zeng, C. Liu, and L. Yuan. Florence-2: Advancing a unified representation for a variety of vision tasks. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 4818–4829, 2024. 

- [7] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- [8] A. Stone, T. Xiao, Y. Lu, K. Gopalakrishnan, K.-H. Lee, Q. Vuong, P. Wohlhart, S. Kirmani, B. Zitkovich, F. Xia, et al. Open-world object manipulation using pre-trained vision-language models. In _Conference on Robot Learning_ , pages 3397–3417, 2023. 

- [9] M. Reuss, H. Zhou, M. Ruhle,¨ O. E. Ya<sup>¨</sup> gmurlu, F. Otto, and R. Lioutikov. Flower: Democratizing˘ generalist robot policies with efficient vision-language-action flow policies. _arXiv preprint arXiv:2509.04996_ , 2025. 

- [10] C. Cheang, S. Chen, Z. Cui, Y. Hu, L. Huang, T. Kong, H. Li, Y. Li, Y. Liu, X. Ma, et al. Gr-3 technical report. _arXiv preprint arXiv:2507.15493_ , 2025. 

- [11] Y. Wang, X. Li, W. Wang, J. Zhang, Y. Li, Y. Chen, X. Wang, and Z. Zhang. Unified visionlanguage-action model. _arXiv preprint arXiv:2506.19850_ , 2025. 

- [12] J. Zheng, J. Li, Z. Wang, D. Liu, X. Kang, Y. Feng, Y. Zheng, J. Zou, Y. Chen, J. Zeng, et al. X-vla: Soft-prompted transformer as scalable cross-embodiment vision-language-action model. _arXiv preprint arXiv:2510.10274_ , 2025. 

- [13] J. Bjorck, F. Castaneda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang,˜ et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [14] H. Shi, B. Xie, Y. Liu, L. Sun, F. Liu, T. Wang, E. Zhou, H. Fan, X. Zhang, and G. Huang. Memoryvla: Perceptual-cognitive memory in vision-language-action models for robotic manipulation. _arXiv preprint arXiv:2508.19236_ , 2025. 

- [15] Z. Zhou, Y. Zhu, M. Zhu, J. Wen, N. Liu, Z. Xu, W. Meng, Y. Peng, C. Shen, F. Feng, et al. Chatvla: Unified multimodal understanding and robot control with vision-language-action model. In _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ , pages 5377–5395, 2025. 

10 

- [16] M. Shukor, D. Aubakirova, F. Capuano, P. Kooijmans, S. Palma, A. Zouitine, M. Aractingi, C. Pascal, M. Russi, A. Marafioti, et al. Smolvla: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 

- [17] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 

- [18] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [19] O. M. Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- [20] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, et al. _\π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [21] Q. Li, Y. Liang, Z. Wang, L. Luo, X. Chen, M. Liao, F. Wei, Y. Deng, S. Xu, Y. Zhang, et al. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 

- [22] D. Qu, H. Song, Q. Chen, Y. Yao, X. Ye, Y. Ding, Z. Wang, J. Gu, B. Zhao, D. Wang, et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- [23] M. J. Kim, C. Finn, and P. Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- [24] S. Liu, L. Wu, B. Li, H. Tan, H. Chen, Z. Wang, K. Xu, H. Su, and J. Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 

- [25] A. O’Neill, A. Rehman, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903. IEEE, 2024. 

- [26] D. Dai, C. Deng, C. Zhao, R. Xu, H. Gao, D. Chen, J. Li, W. Zeng, X. Yu, Y. Wu, et al. Deepseekmoe: Towards ultimate expert specialization in mixture-of-experts language models. _arXiv preprint arXiv:2401.06066_ , 2024. 

- [27] Z. Fu, T. Z. Zhao, and C. Finn. Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation. _arXiv preprint arXiv:2401.02117_ , 2024. 

- [28] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 

- [29] O. Mees, L. Hermann, E. Rosete-Beas, and W. Burgard. Calvin: A benchmark for languageconditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters (RA-L)_ , 7(3):7327–7334, 2022. 

- [30] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _arXiv preprint arXiv:2306.03310_ , 2023. 

- [31] X. Li, M. Liu, H. Zhang, C. Yu, J. Xu, H. Wu, C. Cheang, Y. Jing, W. Zhang, H. Liu, et al. Visionlanguage foundation models as effective robot imitators. _arXiv preprint arXiv:2311.01378_ , 2023. 

11 

- [32] Q. Bu, Y. Yang, J. Cai, S. Gao, G. Ren, M. Yao, P. Luo, and H. Li. Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2502.14420_ , 2025. 

- [33] H. Wu, Y. Jing, C. Cheang, G. Chen, J. Xu, X. Li, M. Liu, H. Li, and T. Kong. Unleashing large-scale video generative pre-training for visual robot manipulation. _arXiv preprint arXiv:2312.13139_ , 2023. 

- [34] C.-L. Cheang, G. Chen, Y. Jing, T. Kong, H. Li, Y. Li, Y. Liu, H. Wu, J. Xu, Y. Yang, et al. Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation. _arXiv preprint arXiv:2410.06158_ , 2024. 

- [35] H. Wu, Y. Jing, C. Cheang, G. Chen, J. Xu, X. Li, M. Liu, H. Li, and T. Kong. Unleashing large-scale video generative pre-training for visual robot manipulation. _arXiv preprint arXiv:2312.13139_ , 2023. 

- [36] L. Wang, X. Chen, J. Zhao, and K. He. Scaling proprioceptive-visual learning with heterogeneous pre-trained transformers. _Advances in neural information processing systems_ , 37: 124420–124450, 2024. 

- [37] W. Fedus, B. Zoph, and N. Shazeer. Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity. _Journal of Machine Learning Research_ , 23(120):1–39, 2022. 

- [38] D. Lepikhin, H. Lee, Y. Xu, D. Chen, O. Firat, Y. Huang, M. Krikun, N. Shazeer, and Z. Chen. Gshard: Scaling giant models with conditional computation and automatic sharding. _arXiv preprint arXiv:2006.16668_ , 2020. 

- [39] C. Riquelme, J. Puigcerver, B. Mustafa, M. Neumann, R. Jenatton, A. Susano Pinto, D. Keysers, and N. Houlsby. Scaling vision with sparse mixture of experts. _Advances in Neural Information Processing Systems_ , 34:8583–8595, 2021. 

- [40] Z. Fei, M. Fan, C. Yu, D. Li, and J. Huang. Scaling diffusion transformers to 16 billion parameters. _arXiv preprint arXiv:2407.11633_ , 2024. 

- [41] S. Roller, S. Sukhbaatar, J. Weston, et al. Hash layers for large sparse models. _advances in neural information processing systems_ , 34:17555–17566, 2021. 

- [42] Y. Guo, Z. Cheng, X. Tang, Z. Tu, and T. Lin. Dynamic mixture of experts: An auto-tuning approach for efficient transformer models. _arXiv preprint arXiv:2405.14297_ , 2024. 

- [43] Z. Wang, J. Zhu, and J. Chen. Remoe: Fully differentiable mixture-of-experts with relu routing. _arXiv preprint arXiv:2412.14711_ , 2024. 

- [44] Y. Lipman, R. T. Chen, H. Ben-Hamu, M. Nickel, and M. Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

- [45] D. Kalashnikov, A. Irpan, P. Pastor, J. Ibarz, A. Herzog, E. Jang, D. Quillen, E. Holly, M. Kalakrishnan, V. Vanhoucke, et al. Qt-opt: Scalable deep reinforcement learning for vision-based robotic manipulation. _arXiv preprint arXiv:1806.10293_ , 2018. 

- [46] F. Ebert, Y. Yang, K. Schmeckpeper, B. Bucher, G. Georgakis, K. Daniilidis, C. Finn, and S. Levine. Bridge data: Boosting generalization of robotic skills with cross-domain datasets. _arXiv preprint arXiv:2109.13396_ , 2021. 

- [47] H. R. Walke, K. Black, T. Z. Zhao, Q. Vuong, C. Zheng, P. Hansen-Estruch, A. W. He, V. Myers, M. J. Kim, M. Du, et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pages 1723–1736. PMLR, 2023. 

- [48] E. Rosete-Beas, O. Mees, G. Kalweit, J. Boedecker, and W. Burgard. Latent plans for task agnostic offline reinforcement learning. 2022. 

12 

- [49] O. Mees, J. Borja-Diaz, and W. Burgard. Grounding language with visual affordances over unstructured data. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , London, UK, 2023. 

- [50] S. Dass, J. Yapeter, J. Zhang, J. Zhang, K. Pertsch, S. Nikolaidis, and J. J. Lim. Clvr jaco play dataset, 2023. URL `https://github.com/clvrai/clvr_jaco_play_dataset` . 

- [51] J. Luo, C. Xu, X. Geng, G. Feng, K. Fang, L. Tan, S. Schaal, and S. Levine. Multi-stage cable routing through hierarchical imitation learning. _arXiv pre-print_ , 2023. URL `https: //arxiv.org/abs/2307.08927` . 

- [52] A. Mandlekar, J. Booher, M. Spero, A. Tung, A. Gupta, Y. Zhu, A. Garg, S. Savarese, and L. Fei-Fei. Scaling robot supervision to hundreds of hours with roboturk: Robotic manipulation dataset through human reasoning and dexterity. In _2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 1048–1055. IEEE, 2019. 

- [53] Y. Zhu, A. Joshi, P. Stone, and Y. Zhu. Viola: Imitation learning for vision-based manipulation with object proposal priors. _6th Annual Conference on Robot Learning (CoRL)_ , 2022. 

- [54] L. Y. Chen, S. Adebola, and K. Goldberg. Berkeley UR5 demonstration dataset. https://sites.google.com/view/berkeley-ur5/home. 

- [55] G. Zhou, V. Dean, M. K. Srirama, A. Rajeswaran, J. Pari, K. Hatch, A. Jain, T. Yu, P. Abbeel, L. Pinto, et al. Train offline, test online: A real robot learning benchmark. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9197–9203. IEEE, 2023. 

- [56] S. Belkhale, Y. Cui, and D. Sadigh. Hydra: Hybrid robot actions for imitation learning. _arxiv_ , 2023. 

- [57] Y. Zhu, P. Stone, and Y. Zhu. Bottom-up skill discovery from unsegmented demonstrations for long-horizon robot manipulation. _IEEE Robotics and Automation Letters_ , 7(2):4126–4133, 2022. 

- [58] Z. J. Cui, Y. Wang, N. M. M. Shafiullah, and L. Pinto. From play to policy: Conditional behavior generation from uncurated robot data. _arXiv preprint arXiv:2210.10047_ , 2022. 

- [59] M. Heo, Y. Lee, D. Lee, and J. J. Lim. Furniturebench: Reproducible real-world benchmark for long-horizon complex manipulation. In _Robotics: Science and Systems_ , 2023. 

- [60] G. Yan, K. Wu, and X. Wang. ucsd kitchens Dataset. August 2023. 

- [61] S. Nasiriany, T. Gao, A. Mandlekar, and Y. Zhu. Learning and retrieval from prior data for skill-based imitation learning. In _Conference on Robot Learning (CoRL)_ , 2022. 

- [62] H. Liu, S. Nasiriany, L. Zhang, Z. Bao, and Y. Zhu. Robot learning on the job: Human-inthe-loop autonomy and learning during deployment. In _Robotics: Science and Systems (RSS)_ , 2023. 

- [63] G. Quere, A. Hagengruber, M. Iskandar, S. Bustamante, D. Leidner, F. Stulp, and J. Vogel. Shared Control Templates for Assistive Robotics. In _2020 IEEE International Conference on Robotics and Automation (ICRA)_ , page 7, Paris, France, 2020. 

- [64] S. Saxena, M. Sharma, and O. Kroemer. Multi-resolution sensing for real-time control with vision-language models. In _7th Annual Conference on Robot Learning_ , 2023. URL `https: //openreview.net/forum?id=WuBv9-IGDUA` . 

- [65] R. Shah, R. Mart´ın-Mart´ın, and Y. Zhu. MUTEX: Learning unified policies from multimodal task specifications. In _7th Annual Conference on Robot Learning_ , 2023. URL `https:// openreview.net/forum?id=PwqiqaaEzJ` . 

13 

- [66] X. Zhu, R. Tian, C. Xu, M. Ding, W. Zhan, and M. Tomizuka. Fanuc manipulation: A dataset for learning-based manipulation with fanuc mate 200id robot. 2023. 

- [67] R. Mendonca, S. Bahl, and D. Pathak. Structured world models from human videos. _CoRL_ , 2023. 

- [68] E. Jang, A. Irpan, M. Khansari, D. Kappler, F. Ebert, C. Lynch, S. Levine, and C. Finn. Bc-z: Zero-shot task generalization with robotic imitation learning. In _Conference on Robot Learning_ , pages 991–1002. PMLR, 2022. 

- [69] J. Luo, C. Xu, F. Liu, L. Tan, Z. Lin, J. Wu, P. Abbeel, and S. Levine. Fmb: a functional manipulation benchmark for generalizable robotic learning. _arXiv preprint arXiv:2401.08553_ , 2024. 

- [70] N. M. M. Shafiullah, A. Rai, H. Etukuru, Y. Liu, I. Misra, S. Chintala, and L. Pinto. On bringing robots home, 2023. 

- [71] Y. Yue, Y. Wang, B. Kang, Y. Han, S. Wang, S. Song, J. Feng, and G. Huang. Deer-vla: Dynamic inference of multimodal large language models for efficient robot execution. _Advances in Neural Information Processing Systems_ , 37:56619–56643, 2024. 

- [72] M. Reuss, O. E. Ya<sup>¨</sup> gmurlu, F. Wenzel, and R. Lioutikov.˘ Multimodal diffusion transformer: Learning versatile behavior from multimodal goals. _arXiv preprint arXiv:2407.05996_ , 2024. 

- [73] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , page 02783649241273668, 2023. 

- [74] T. Zhu, X. Qu, D. Dong, J. Ruan, J. Tong, C. He, and Y. Cheng. Llama-moe: Building mixture-of-experts from llama with continual pre-training. _arXiv preprint arXiv:2406.16554_ , 2024. 

14 

## **A Dataset and Evaluation** 

### **A.1 Pretraining Dataset** 

Our pre-training dataset is constructed by combining subsets of Open X-Embodiment (OXE) and publicly available ALOHA datasets, yielding a total of 24.1M frames. The detailed data mixture is listed in Table 8. 

**OXE dataset.** OXE [25] aggregates over 1 million real-world trajectories collected from 60 datasets across 22 distinct robot embodiments. Following prior works such as Octo [19] and OpenVLA [18], we adopt a subset containing 22.5M frames, chosen to balance scale and diversity while ensuring compatibility with our training pipeline. This subset spans a wide range of single-arm robots and tasks, providing strong coverage of heterogeneous embodiments and action spaces. 

**ALOHA datasets.** To complement OXE, we incorporate demonstrations from three high-quality, publicly available ALOHA datasets [24, 28, 27], contributing 1.6M frames in total. Compared to OXE, they emphasize coordinated bimanual actions and higher-fidelity manipulation skills, substantially enriching the diversity of our training corpus. 

Table 8: Our training data mixture using datasets from the Open X-Embodiment dataset [25] and ALOHA dataset [24, 28, 27]. 

|**Dataset**|**Ratio**|
|---|---|
|Fractal [7]<br>|23.9%<br>|
|Kuka [45]<br>|12.9%|
|Bridge [46,47]|11.9%|
|Taco Play [48,49]|2.7%|
|Jaco Play [50]|0.4%|
|Berkeley Cable Routing [51]|0.2%|
|Roboturk [52]|2.1%|
|Viola [53]|0.9%|
|Berkeley Autolab UR5 [54]|1.1%|
|Toto [55]|1.9%|
|Stanford Hydra Dataset [56]|4.5%|
|Austin Buds Dataset [57]|0.2%|
|NYU Franka Play Dataset [58]|0.7%|
|Furniture Bench Dataset [59]|2.5%|
|UCSD Kitchen Dataset [60]|_<_0.1%|
|Austin Sailor Dataset [61]|2.2%|
|Austin Sirius Dataset [62]|1.8%|
|DLR EDAN Shared Control [63]|_<_0.1%|
|IAMLab CMU Pickup Insert [64]|0.9%|
|UTAustin Mutex [65]|2.3%|
|Berkeley Fanuc Manipulation [66]|0.8%|
|CMU Stretch [67]|0.2%|
|BC-Z [68]|6.9%|
|FMB Dataset [69]|7.2%|
|DobbE [70]|1.4%|
|ALOHA Dataset [24,28,27]|10.4%|


### **A.2 Evaluation Benchmarks** 

**CALVIN benchmark.** CALVIN [29] is a benchmark for evaluating instruction-conditioned policies in long-horizon tabletop manipulation tasks using a Franka Panda arm. It comprises 34 tasks spanning from simple pick-and-place to articulated object manipulation and provides four simulated environments, denoted A, B, C, and D. In the standard _D → D_ setting, policies are trained on a limited subset of demonstrations from environment D and evaluated on held-out instruction sequences in the same environment. In our heterogeneous co-training experiments, ABC denotes demonstrations from environments A/B/C using the end-effector (EEF) action parameterization, while D denotes demonstrations from environment D using joint-angle actions unless otherwise specified. 

CALVIN evaluates long-horizon control with five-subtask instruction chains. Column _k ∈{_ 1 _, . . . ,_ 5 _}_ reports the fraction of evaluation chains in which the policy completes at least the first _k_ consecutive subtasks. The scalar Sum. metric is the sum of these five success rates, equivalently the average number of completed subtasks per five-subtask chain; this is the standard primary CALVIN score 

15 

used throughout our tables. This setup evaluates the model’s ability to generalize to novel instruction compositions under restricted data conditions. For fair comparison, we include Octo [19], OpenVLA [18], RDT-1B [24], DeeR [71], MDT [72], and _π_ 0 [20] as baselines. For DeeR and MDT, we directly report the results from their original papers. For Octo, OpenVLA, RDT-1B, and _π_ 0, we adopt their released pre-trained weights and perform fine-tuning on CALVIN-D following their official training procedures to ensure fairness and reproducibility. 

**LIBERO benchmark.** LIBERO [30] is a simulation suite designed to evaluate lifelong learning and generalization in robotic manipulation. It contains four task suites—LIBERO-Spatial, LIBEROObject, LIBERO-Goal, and LIBERO-Long—each comprising 10 tasks with 50 human-teleoperated demonstrations per task. These suites test complementary aspects of generalization: spatial reasoning (Spatial), object-level transfer (Object), goal-directed adaptability (Goal), and long-horizon planning (Long). Following prior works such as OpenVLA [18], we preprocess demonstrations by removing failure cases, standardizing image inputs, and ensuring consistent trajectory formatting. In our experiments, we perform supervised fine-tuning within each task suite using the successful demonstrations and evaluate policies on held-out task episodes. We compare against strong baselines, including Diffusion Policy [73], Octo [19], OpenVLA [18], SpatialVLA [22], OpenVLA-OFT [23], UniVLA [32], and _π_ 0 [20], where reported results are either taken directly from their papers or reproduced under their released implementations. 

**Real-world xArm7 benchmark.** We conduct real-world evaluations on an xArm7 robot (7-DoF manipulator with a 1-DoF gripper) across three tasks: (1) _Fruit-to-Plate_ — placing fruits (apple, orange) onto colored plates (blue, pink), e.g., “Pick up the apple and place it onto the blue plate”; (2) _Cup-in-Cup_ — inserting one colored cup (red, yellow, blue) into another, e.g., “Put the yellow cup into the red cup”; (3) _Block-on-Block_ — stacking one colored block onto a differently colored block, e.g., “Place the yellow block on top of the red block.” Each task is decomposed into sub-stages (e.g., Pick/Place, Pick/Insert, Pick/Stack) for fine-grained evaluation. We collect 320 teleoperated demonstrations in total: 80 ( _Fruit-to-Plate_ ), 120 ( _Cup-in-Cup_ ), and 120 ( _Block-on-Block_ ), with 20 demonstrations per configuration. 

_In-distribution evaluation._ **Fruit-to-Plate** : 4 settings _×_ 4 trials/setting = 16 trials in total, where each “setting” is a fruit–plate pairing from _{_ apple, orange _} × {_ blue, pink _}_ . **Cup-in-Cup** : 6 settings _×_ 3 trials/setting = 18 trials, where each “setting” is an _ordered_ inner _→_ outer color pair from _{_ red, yellow, blue _}_ with distinct colors (i.e., 3 _×_ 2 = 6 ordered pairs). **Block-on-Block** : 6 settings _×_ 3 trials/setting = 18 trials, where each “setting” is an _ordered_ top _→_ bottom color pair (distinct) from _{_ red, yellow, blue _}_ . 

_Generalization tests._ (1) **Distractors in** **_Cup-in-Cup_** : 6 settings (the same 6 inner _→_ outer color pairs as above) _×_ 3 trials/setting = 18 trials, with an unseen distractor (e.g., a pomegranate or a green cup) placed in the scene. (2) **Novel objects in** **_Fruit-to-Plate_** : 4 settings _×_ 4 trials/setting = 16 trials. Here, “4 _×_ 4” means that we test four novel configurations — placing a pomegranate onto a blue plate, a pomegranate onto a pink plate, an apple onto a purple plate, and an orange onto a purple plate — with each configuration repeated for 4 trials. 

**Real-world ALOHA benchmark.** We further evaluate on the ALOHA robot (dual-arm, 14-DoF) with three tasks: (1) _Fold-Shorts_ — folding a pair of shorts (50 teleoperated demonstrations), e.g., “Fold black shorts through multiple bimanual folds”; (2) _Cup-Handover_ — the right arm grasps a colored cup (red, yellow, blue) and hands it to the left arm to place on a plate (60 demos per color; 180 total), e.g., “Pick up the blue cup, switch hands, and place it on the plate”; (3) _Scoop_ — the left arm places a bowl centrally, then the right arm uses a spoon to scoop materials (mung beans, black rice, sticky rice) into the bowl (40 demos per material; 120 total), e.g., “Place the bowl in the middle of the table, then scoop the glutinous rice with a spoon.” Altogether, 350 demonstrations are collected. 

16 

_In-distribution evaluation._ **Fold-Shorts** : 1 setting _×_ 15 trials = 15 trials. **Cup-Handover** : 3 settings (one per cup color) _×_ 5 trials/setting = 15 trials. **Scoop** : 3 settings (one per material type) _×_ 5 trials/setting = 15 trials. 

_Generalization tests._ (1) **Distractors in** **_Scoop_** : 3 settings (the same three material types) _×_ 3 trials/setting = 9 trials, with unseen distractors (e.g., banana or green apple) added to the scene. (2) **Novel garment in** **_Fold-Shorts_** : 1 setting (previously unseen shorts) _×_ 15 trials = 15 trials. 

## **B Implementation Details** 

**Model scale and training setup.** Our proposed HiMoE-VLA model contains approximately 4B parameters and is trained end-to-end on 16 NVIDIA A100 GPUs (40GB each) for 100k steps with a global batch size of 256. Training takes around 4 days with DeepSpeed optimization, and we adopt the LeRobot data-loading framework to ensure efficient and scalable handling of large heterogeneous datasets. 

**Input modalities.** The visual encoder consumes one third-person camera view together with two wrist-mounted views. When a view is unavailable in a dataset, the corresponding channel is zeropadded and masked using attention masks, ensuring a consistent input format. For state and action inputs, we construct a unified vector representation that jointly accommodates both joint-angle and end-effector signals. In single-arm demonstrations, the available arm is mapped to the right-arm channel, while the left-arm channel is zero-padded with masks to preserve compatibility with dualarm settings. All heterogeneous actions and states are mapped into a fixed 24-dimensional vector, consisting of 8-dimensional end-effector actions and 16-dimensional joint angles. For states, a validity mask is concatenated to indicate which segments are active. For actions, unavailable dimensions are zero-padded, and the loss mask described in Appendix C.7 restricts supervision to valid action dimensions. 

**Mixture-of-Experts design.** We set the number of experts to _N_ = 32 with top- _K_ routing of _K_ = 4. As shown in Table 9, this configuration consistently outperforms alternative settings in terms of both average performance and stability, striking a favorable balance between model capacity and computational efficiency. To encourage effective expert utilization and hierarchical abstraction, we introduce two auxiliary regularizations: an Action-Space regularization term with coefficient _λ_ AS = 0 _._ 002, and a Heterogeneity-Balancing regularization term with coefficient _λ_ HB = 0 _._ 001. These choices follow best practices for balancing specialization and generalization in MoE architectures. 

Table 9: Ablation on the number of experts _N_ and top- _K_ routing on CALVIN. _N_ =32, _K_ =4 gives the best trade-off between specialization and stability. 

|**_K_**|**_N_**|**1**|**2**|**3**|**4**|**5**|**Sum.**|
|---|---|---|---|---|---|---|---|
||2|0.895|0.811|0.757|0.712|0.648|3.823|
|2|4|0.901|0.814|0.761|0.715|0.653|3.844|
||8|0.910|0.827|0.768|0.722|0.669|3.896|
||16|0.920|0.846|0.781|0.733|0.671|3.951|
||8|0.921|0.847|0.776|0.715|0.657|3.916|
|4|16|0.923|0.846|0.774|0.729|**0.682**|3.954|
||32|**0.943**|**0.864**|**0.797**|0.734|0.674|**4.012**|
||64|0.919|0.854|0.785|**0.738**|0.672|3.968|
|8|16|0.911|0.773|0.637|0.546|0.458|3.325|
||32|0.897|0.794|0.719|0.673|0.612|3.695|


**Optimization and fine-tuning.** We adopt the AdamW optimizer with an initial learning rate of 2 _._ 5 _×_ 10<sup>_−_5</sup> , weight decay of 1 _×_ 10<sup>_−_4</sup> , and a cosine decay schedule. The learning rate is linearly warmed up for the first 1k steps, followed by exponential decay until 30k steps with a final floor of 2 _._ 5 _×_ 10<sup>_−_6</sup> . For fine-tuning, we adapt the batch size and number of steps to each benchmark. On CALVIN, we use a global batch size of 32 for 40k steps. On LIBERO, we fine-tune each suite separately: LONG, GOAL, and OBJECT use batch size 64 for 40k, 45k, and 45k steps, respectively, 

17 

while SPATIAL uses batch size 32 for 35k steps. For real-world experiments, we fine-tune on both XARM7 and ALOHA robots with batch size 64 for 50k steps. 

**Cross-layer KV integration.** At each transformer layer _l_ , HiMoE receives the key–value pairs _{Kl_<sup>V</sup><sup>_, V_</sup> _l_<sup>V</sup><sup>_}_from the corresponding VLM layer, which are concatenated with the locally computed</sup> _{Kl_<sup>H</sup><sup>_, V_</sup> _l_<sup>H</sup><sup>_}_of the action expert:</sup> 


The query _Q_<sup>H</sup> _l_<sup>then attends to the fused representation:</sup> 


This design enables each HiMoE layer to directly condition on semantically aligned signals from its VLM counterpart, instead of relying solely on the final-layer representation. During inference, we further employ a KV cache to reuse the VLM’s intermediate keys and values, substantially accelerating policy rollout without degrading performance. 

## **C More Analysis** 

### **C.1 Challenges in Transferability Across Heterogeneous Action Spaces** 

Data from different action spaces are largely non-transferable due to fundamental differences in physical interpretation and kinematic structures. 

**Distinct Physical Meanings.** End-effector (EEF) actions and joint-angle actions represent distinct physical quantities. EEF actions typically define the gripper’s Cartesian pose (position and orientation), whereas joint-angle actions specify individual joint rotations. Consequently, they operate in disjoint coordinate systems and adhere to different physical constraints. 

**Kinematic Incompatibility.** Even within the same action type, robots often possess varying Degrees of Freedom (DoFs) and kinematic chains. For instance, a 6-DoF arm and a 7-DoF arm executing the same end-effector motion will exhibit divergent joint-angle trajectories due to their structural differences. As a result, joint-space data cannot be directly aligned across different embodiments. 

Driven by these distinct meanings and embodiment-dependent kinematics, EEF and joint-angle actions reside in incompatible domains with divergent data distributions. This significant distributional mismatch fundamentally limits the direct transferability of policies learned in one action space to another. 

### **C.2 Effectiveness of the Shared Expert Mechanism** 

The shared expert captures common knowledge that is agnostic to data heterogeneity. This mechanism allows other experts to focus solely on input-specific variations (e.g., sensor configurations) rather than repeatedly learning redundant patterns. Consequently, the shared expert facilitates more efficient knowledge sharing and stabilizes the specialization of the remaining experts. This design aligns with recent advancements in MoE architectures, such as DeepSeekMoE [26] and LlamaMoE [74]. 

To verify its contribution, we conducted an ablation study by removing the shared expert from the architecture. As shown in Table 10, the performance dropped moderately, indicating that this component is essential for achieving stable specialization and stronger overall performance. 

Table 10: Shared-expert ablation under CALVIN-ABC (EEF) + CALVIN-D (joint-angle) co-training. 

|**Method**|**1**|**2**|**3**|**4**|**5**|**Sum.**|
|---|---|---|---|---|---|---|
|w/o shared expert|0.921|0.846|0.779|0.732|**0.677**|3.955|
|Full|**0.943**|**0.864**|**0.797**|**0.734**|0.674|**4.012**|


18 

### **C.3 Ablation Protocol and Variant Definitions** 

Our ablations span the two regimes in which VLA models are commonly deployed. First, we finetune the pre-trained HiMoE-VLA on CALVIN-D (optimization rows of Table 4) and additionally study cross-action-space fine-tuning on CALVIN-ABC (EEF) plus CALVIN-D (joint-angle) in Appendix C.10. Second, we co-train from scratch on heterogeneous sources: CALVIN-ABC plus CALVIN-D for action-space heterogeneity (heterogeneity rows of Table 4 and Tables 5, 6), and CALVIN environment D plus LIBERO under a shared EEF action parameterization for sensor/scene heterogeneity (Table 7). This protocol ensures that the reported gains are not tied to a single robot, benchmark, or training regime. 

For the component ablation in Table 6, _w/o MoE_ replaces all MoE layers with dense Transformer blocks; _Full-HB-MoE_ replaces every MoE slot with an HB-MoE layer; _w/o AS-MoE_ removes only the boundary AS-MoE layers; _w/o HB-MoE_ removes only the adjacent HB-MoE layers; _w/o Reg_ uses the full architecture with _λ_ AS= _λ_ HB=0; and _Single-MoE+Reg_ applies both regularizers to a single non-hierarchical MoE layer. These variants separate the effects of sparse capacity, boundary action-space routing, heterogeneity balancing, and auxiliary regularization. 

### **C.4 Full Per-Step Results of HiMoE Component Ablations** 

Table 11 reports the complete per-sequence-length success counts (lengths 1–5) for the HiMoE component ablation on CALVIN ABC + D co-training. The aggregated **Sum.** column is also shown in the main paper (Table 6). 

Table 11: Full per-step results of the HiMoE component ablation on CALVIN ABC + D co-training. Each column 1–5 reports the average completion rate at the corresponding sequence length; **Sum.** is the cumulative count over the 5-step sequence. 

|**Setting**|**1**|**2**|**3**|**4**|**5**|**Sum.**|
|---|---|---|---|---|---|---|
|w/o MoE|0.918|0.837|0.744|0.681|0.597|3.777|
|Full-HB-MoE|0.917|0.847|0.774|0.713|0.650|3.901|
|w/o AS-MoE|0.909|0.831|0.769|0.718|0.646|3.873|
|w/o HB-MoE|0.904|0.826|0.749|0.708|0.649|3.836|
|w/o Reg|0.904|0.822|0.753|0.702|0.654|3.835|
|Single-MoE+Reg|0.914|0.839|0.757|0.688|0.615|3.813|
|Full|**0.943**|**0.864**|**0.797**|**0.734**|**0.674**|**4.012**|


### **C.5 Impact of Parameter Count vs. Architecture Design** 

In our main experiments (Table 6), the “Full” MoE setting utilizes _N_ = 32 experts with a top- _K_ routing of _K_ = 4. We note that this configuration results in slightly more active parameters compared to the “w/o MoE” baseline. To verify that the observed performance gains stem from the proposed mixture-of-experts design rather than merely increased model capacity, we conducted a control experiment with a parameter-matched dense baseline. 

Specifically, we increased the parameter count of the “w/o MoE” model by enlarging the token feature dimensions and the FFN intermediate size, denoted as “w/o MoE (Large)”. We co-trained this scaled baseline on CALVIN ABC (EEF) and CALVIN D (joint-angle) from scratch. As shown in Table 12, although increasing the parameters of the dense baseline (from 3.2B to 4.1B) yields a marginal improvement (Sum: 3.777 _→_ 3.801), it still significantly lags behind our Full model (Sum: 4.012). Notably, our Full model achieves this superior performance with fewer active parameters (3.36B) than the scaled dense baseline (4.10B), confirming the effectiveness of the MoE architecture. 

Table 12: Comparison with a parameter-matched dense baseline. We scale up the “w/o MoE” baseline to match the total parameter count of our Full model. “Param (All _|_ Act.)” denotes total and active parameters in billions. 

|**Method**|**Param (A**|**ll**_|_**Act.)**<br>**1**|**2**|**3**|**4**|**5**|**Sum.**|
|---|---|---|---|---|---|---|---|
|w/o MoE|3.24B_|_|3.24B<br>0.918|0.837|0.744|0.681|0.597|3.777|
|w/o MoE (Large)|4.10B_|_|4.10B<br>0.898|0.806|0.744|0.702|0.651|3.801|
|Full (Ours)|4.07B_|_|**3.36B**<br>**0.943**|**0.864**|**0.797**|**0.734**|**0.674**|**4.012**|


19 

### **C.6 MoE Warm-up** 

The term “MoE Warm-up” refers to a two-stage fine-tuning strategy that prepares the MoE-related parameters before jointly optimizing the whole model. Although our goal is for HiMoE to abstract features into shared knowledge during pre-training, the domain gap between the pre-training mixture and a target fine-tuning dataset can be substantial. In such cases, directly updating all parameters from the first step forces the pre-trained backbone to absorb gradients from MoE routing and expert modules that have not yet adapted to the target domain, which can destabilize optimization. 

Concretely, our warm-up proceeds in two stages. In the _first stage_ , we freeze all non-MoE parameters in the action module (i.e., the Transformer blocks that were pre-trained alongside and learned to cooperate with the MoE) as well as the VLM backbone, and update only the MoE-related parameters (routers, experts, and the shared expert) for a short warm-up phase. This stage lets the experts and routing distributions adapt to the target domain’s action spaces and embodiments while preserving the pre-trained backbone. In the _second stage_ , we unfreeze all parameters and jointly fine-tune the entire model under the standard training objective. Thus, our evaluation measures fine-tuning transfer from heterogeneous pre-training. 

### **C.7 Analysis of Heterogeneous Co-training Pipeline** 

**Mechanisms for Heterogeneous Data.** To effectively handle heterogeneous observation and action spaces during co-training, our pipeline incorporates two key mechanisms: **Data Mask** and **Loss Mask** . 

- **Data Mask:** To address varying state vector dimensions across tasks, we concatenate the state vector with a boolean mask. This mask explicitly indicates which indices correspond to valid data versus padding, allowing the model to distinguish between informative features and zero-padded values. 

- **Loss Mask:** Instead of computing the loss over the full action vector (which may contain padded dimensions for certain datasets), we utilize a loss mask to compute the gradient only over the valid action dimensions specific to each task. 

**Ablation Study.** We validate the contribution of these components under the “w/o MoE” (Dense) setting with from-scratch co-training on CALVIN ABC + D. As shown in Table 13, the full base setting achieves a total score of 3.777. Removing the _Loss Mask_ results in a performance drop to 3.696, indicating the importance of precise gradient supervision. Furthermore, removing both the _Data Mask_ and _Loss Mask_ leads to a significant degradation to 3.626. These results demonstrate that explicitly handling heterogeneity via masking strategies is critical for robust co-training performance. 

Table 13: Ablation of training pipeline components for heterogeneous co-training (CALVIN ABC + D). We evaluate the impact of Data Mask and Loss Mask on the dense (w/o MoE) baseline. 

|**Method**|**1**|**2**|**3**|**4**|**5**|**Sum.**|
|---|---|---|---|---|---|---|
|Base setting (with both masks)|**0.918**|**0.837**|**0.744**|**0.681**|0.597|**3.777**|
|w/o Loss Mask|0.896|0.800|0.726|0.667|**0.607**|3.696|
|w/o Data & Loss Mask|0.886|0.797|0.714|0.649|0.580|3.626|


### **C.8 State-Action Injection Ablation** 

For completeness, we evaluate whether the cross-action improvements depend on the specific way proprioceptive state information is injected into the action expert. We compare three state-injection mechanisms under the same from-scratch CALVIN protocols: (i) _Concatenation_ , our default design, which places state, noisy-action, and time tokens in a single Transformer sequence; (ii) _CrossAttention_ , where action hidden states attend to state tokens; and (iii) _AdaLN_ , where state tokens are mapped to scale and shift parameters that modulate the action hidden states. Since changing the injection topology changes parameter shapes and prevents direct reuse of pre-trained weights, all variants are trained from scratch for a controlled comparison. 

20 

Table 14: State-action injection ablation on CALVIN. We compare D-only training with CALVIN ABC (EEF) + D (joint-angle) co-training under the same HiMoE architecture. 

|**State-Injection Method**|**D (Joint) Only**|**ABC (EEF) + D (Joint)**|**Transfer Gain**|
|---|---|---|---|
|Cross-Attention|3.724|3.915|+0_._191|
|AdaLN|3.822|3.995|+0_._173|
|Concatenation|3.826|**4.012**|+0_._186|


Table 14 shows that all three injection mechanisms obtain positive transfer when moving from singleaction-space training to mixed EEF/joint co-training. This suggests that HiMoE’s cross-action benefit is not an artifact of a particular state-injection interface. Concatenation gives the best mixed-action performance, supporting its use as a simple default for modeling bidirectional state-action correlations in a shared Transformer sequence. 

### **C.9 Analysis of Expert Routing** 

For visualization purposes, we deliberately analyze a smaller HiMoE configuration with _N_ =8 experts and top- _K_ =2 routing on CALVIN joint-angle, CALVIN EEF, and LIBERO EEF, rather than the deployed _N_ =32 _, K_ =4 setting. We stress that the figures in this subsection are intended as a _qualitative illustration of the regularization mechanism_ , not as deployed-scale performance evidence: the two patterns we wish to convey—(a) per-source clustering of the AS-MoE routing distribution and (b) approximately uniform expert utilization in HB-MoE—are directly encouraged by AS-Reg and HB-Reg. The choice of small _N_ =8 _, K_ =2 is motivated purely by interpretability: (i) a 3 _×_ 32 heatmap with top-4 routing is visually saturated and qualitatively indistinguishable across rows, while a 3 _×_ 8 heatmap with top-2 routing makes the per-dataset specialization pattern visually unambiguous; (ii) a sparser top- _K_ ( _K_ =2 vs. _K_ =4) yields a more peaked activation distribution that directly reveals which experts a given action space relies on, whereas _K_ =4 averages out the contrast; (iii) at the deployed scale, expert specialization is partitioned across a much larger pool, so any single-panel color scale necessarily compresses the per-expert signal and obscures the very pattern we wish to visualize. The auxiliary losses are rescaled to be _N_ -invariant (we use the DeepSeek-style _fi_ =( _N/KU_ )<sup>�</sup> _u_<sup>_ri,u_</sup> normalization with<sup>�</sup> _i_<sup>_fi_=</sup><sup>_N_, and the InfoNCE-style contrastive ratio in AS-Reg is dimensionless</sup> in _N_ ). We further monitor both auxiliary losses during training at the deployed _{N_ =32 _, K_ =4 _}_ configuration and observe that HB-Reg converges close to its theoretical lower bound (corresponding to near-uniform expert utilization) and AS-Reg saturates at a similarly low value, suggesting similar routing behavior at deployed scale. We therefore use the _{N_ =8 _, K_ =2 _}_ panel purely as a diagnostic instrument for the routing mechanism; the downstream effect of this mechanism on task performance at the deployed _{N_ =32 _, K_ =4 _}_ scale is reported separately in Tables 5, 6, 7, and 9. The expert activation heatmaps for AS-MoE and HB-MoE are shown in Figure 4 and Figure 5, respectively. 

From Figure 4, we observe that CALVIN EEF and LIBERO EEF exhibit similar expert activation patterns, while CALVIN joint-angle shows a clearly different distribution, reflecting the differences in action space. From Figure 5, the expert activation patterns for CALVIN joint-angle and CALVIN EEF are similar, as these datasets share the same environment and observation settings except for the action space, whereas LIBERO EEF has a distinct activation pattern. 

These visualizations provide qualitative evidence that the hierarchy encourages different routing behavior for action-space and observation-related variation. 

### **C.10 Cross-Action Space Fine-Tuning** 

Beyond the from-scratch co-training studies in Tables 5 and 6, we further evaluate whether HiMoE can leverage heterogeneous action spaces during the _fine-tuning_ stage. Unlike the from-scratch setting, this experiment starts from pre-trained checkpoints and compares _isolated_ fine-tuning on a single action space against _mixed_ fine-tuning on both action spaces simultaneously. To make the comparison strict and fully reproducible, we use CALVIN, which supports the same task family under two distinct action parameterizations: ABC (EEF) and D (joint-angle). 

21 

Table 15: Cross-action space fine-tuning on CALVIN. We fine-tune the pre-trained HiMoE-VLA either on a single action-space split (ABC (EEF) or D (joint-angle)) in isolation, or jointly on both splits. Numbers report the CALVIN long-horizon score (sum over 5 chained tasks); values in parentheses are the absolute gain over the corresponding isolated setting. 

|**Evaluation setting**<br>**ABC (EEF) only**|**D (joint-angle) only**|**ABC (EEF) + D (joint-angle)**|
|---|---|---|
|EEF evaluation<br>4.119|–|**4.224 (+0.105)**|
|Joint-angle evaluation<br>–|3.967|**4.205 (+0.238)**|


As shown in Table 15, mixed fine-tuning consistently outperforms isolated fine-tuning on both the EEF (+0 _._ 105) and joint-angle (+0 _._ 238) action spaces, with a particularly large gain on the joint-angle split where data is harder to learn from scratch. Moreover, both mixed-tuning scores are substantially higher than the corresponding from-scratch results in Table 5, indicating that the pre-trained HiMoE provides transferable physical priors that are further amplified when heterogeneous action data is mixed during fine-tuning. Together with the shared-action observation/scene co-training experiment in Table 7, these results support the effectiveness of the hierarchy under both action-space and non-action heterogeneity rather than merely benefiting from extra capacity. 

We further compare against a dense _π_ 0-style baseline under the same CALVIN D joint-angle evaluation. As shown in Table 16, mixed fine-tuning provides only a modest gain for the dense baseline, whereas HiMoE obtains a larger improvement and a higher absolute score. This suggests that the benefit of mixed-action data is substantially amplified by the proposed hierarchical MoE action module. 

Table 16: Dense baseline vs. HiMoE under CALVIN mixed-action fine-tuning from pre-trained checkpoints. 

|**Method**<br>|**D (Joint) Only**|**ABC (EEF) + D (Joint)**|**Transfer Gain**|
|---|---|---|---|
|Dense baseline|3.756|3.816|+0_._060|
|HiMoE-VLA|3.967|**4.205**|+0_._238|


### **C.11 Training and Inference Efficiency** 

We benchmark the training and inference cost of HiMoE-VLA to quantify the overhead introduced by the hierarchical MoE design. 

**Training speed.** Training throughput is measured on the CALVIN benchmark using 8 _×_ NVIDIA A100 (40 GB) GPUs with a global batch size of 32, DeepSpeed ZeRO-Stage 2, and gradient checkpointing. As shown in Table 17, the full HiMoE configuration ( _N_ =32, _K_ =4) incurs only _∼_ 7% additional per-iteration cost relative to the dense ( _w/o MoE_ ) variant, while delivering substantially better performance on heterogeneous data (Tables 5, 6). 

Table 17: Training speed (seconds per iteration) on CALVIN with 8 _×_ NVIDIA A100 (40 GB) GPUs, a global batch size of 32, DeepSpeed ZeRO-Stage 2, and gradient checkpointing. 

|**Model**|w/o MoE|_N_=8_, K_=2<br>_N_=8_, K_=4<br>_N_=32_, K_=4|
|---|---|---|
|Speed (s/iter)|1.14|1.18<br>1.20<br>1.22|


**Inference speed.** Inference latency is measured on a single NVIDIA RTX 4090 GPU. We note that _π_ 0 benefits from a highly optimized JAX implementation, whereas all other evaluated baselines and our method are implemented in PyTorch. As reported in Table 18, introducing the MoE routing mechanism inevitably incurs a slight increase in inference latency, yet our overall inference speed remains highly competitive with existing mainstream efficient methods such as OpenVLA-OFT and RDT-1B. 

## **D More Visualizations** 

Additional task-level visualizations are shown in Fig. 6 and Fig. 7. 

22 

Table 18: Inference latency (seconds per action chunk) on a single NVIDIA RTX 4090 GPU. _π_ 0 uses a highly optimized JAX implementation; all other methods (including ours) are implemented in PyTorch. 

|**Model**||**Baselines**||||**Ours**||
|---|---|---|---|---|---|---|---|
||OpenVLA|OpenVLA-OFT|RDT-1B|_π_0<br>|w/o MoE|_N_=8_, K_=2 _N_=8_, K_=4|_N_=32_, K_=4|
|Lat. (s)|0.307|0.182|0.168|0.086|0.153|0.185<br>0.193|0.195|


Figure 4: AS-MoE expert activation heatmap for the qualitative _N_ =8 _, K_ =2 routing analysis on CALVIN joint-angle, CALVIN EEF, and LIBERO EEF. 


Figure 5: HB-MoE expert activation heatmap for the qualitative _N_ =8 _, K_ =2 routing analysis on CALVIN joint-angle, CALVIN EEF, and LIBERO EEF. 

23 


Figure 6: Overview of tasks on the single-arm xArm7 robot, including seen tasks and generalization settings with unseen distractors or novel objects. 


Figure 7: Overview of tasks on the dual-arm ALOHA robot, including seen tasks and generalization settings with unseen distractors or a novel garment. 

24 

