---
title: "JailWAM: Jailbreaking World Action Models in Robot Control"
date: "2026-04-07"
authors: "Hanqing Liu; Songping Wang; Jiahuan Long; Jiacheng Hou; Jialiang Sun; Chao Li"
url: https://arxiv.org/abs/2604.05498
pdf: https://arxiv.org/pdf/2604.05498
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.05498)** / [論文ページ](https://arxiv.org/abs/2604.05498)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **JailWAM: Jailbreaking World Action Models in Robot Control** 

**Hanqing Liu**<sup>1,3</sup> **, Songping Wang**<sup>2</sup> **, Jiahuan Long**<sup>1,3</sup> **, Jiacheng Hou**<sup>3</sup> **, Jialiang Sun**<sup>3</sup> **, Chao Li**<sup>3</sup> **, Yang Yang**<sup>3</sup> **, Wei Peng**<sup>3</sup> **, Xu Liu**<sup>3</sup> **, Tingsong Jiang**<sup>3</sup> **, Yao Mu**<sup>1∗</sup> **, Wen Yao**<sup>3∗</sup> 

1MoE Key Lab of Artificial Intelligence, AI Institute, Shanghai Jiao Tong University, Shanghai, China 

2PR Lab, Nanjing University, Suzhou, China 

3Defense Innovation Institute, Chinese Academy of Military Science, Beijing, China 

#### **Abstract** 

World Action Models (WAMs) have emerged as a promising paradigm for robotic manipulation, enabling physical interaction across diverse tasks and environments. However, their ability to directly follow high-level instructions and execute physical actions also creates potential safety risks, as adversarially designed instructions may induce unsafe robot behaviors. To systematically assess these risks, we propose **JailWAM** , the first jailbreak evaluation framework for WAMs. In JailWAM, we integrate three key innovations: Firstly, to address the difficulty of evaluating heterogeneous low-level action outputs, we introduce **Visual-Trajectory Mapping** , which transforms model-specific actions into unified visual trajectory representations, thereby facilitating consistent risk assessment across WAM architectures. Secondly, to provide efficient and fine-grained assessment of physical risks, we develop a **Risk Discriminator** supervised by three safety levels ordered according to physical consequence: _Safety Compliance_ , _Motion Failure_ , and _Catastrophic Risk_ . This severity-aware formulation enables the risk discriminator to distinguish different physical outcomes from visual trajectories and support scalable risk screening. Thirdly, to reduce the cost of exhaustively executing adversarial candidates, we design a **Dual-Path Verification Strategy** that combines rapid risk screening with closed-loop physical simulation, restricting computationally expensive verification to candidates with potential safety risks. Extensive experiments in the RoboTwin simulation environment show that JailWAM achieves an 84 _._ 2% attack success rate on LingBot-VA, which indicates that WAMs may be susceptible to jailbreak attacks that induce unsafe physical behaviors. Our findings may motivate further research on the safety evaluation and alignment of future embodied robotic systems. 

## **Introduction** 

World Action Models (WAMs) (Hu et al. 2024; Liao et al. 2025; Li et al. 2026a; Kim et al. 2026) have emerged as a paradigm for robotic manipulation by jointly modeling future world states and executable actions, supporting physical interaction across diverse tasks and environments. However, their ability to directly follow instructions and execute physical actions also raises safety concerns, as adversarially designed instructions may induce unsafe robot behaviors (Jia et al. 2024; Tao et al. 2025; Liu et al. 2025; Lee et al. 2025; Gong et al. 2025). Unlike conventional jailbreak attacks that primarily affect digital outputs, such as harmful 

∗Corresponding author. 


Figure 1: Representative closed-loop rollouts of LingBotVA in the RoboTwin simulator. Normal instructions result in Level 0 ( _Safety Compliance_ ), whereas jailbreak instructions generated through JailWAM induce Level 1 ( _Motion Failure_ ), including deadlocks and persistent state loops, and Level 2 ( _Catastrophic Risk_ ), including erratic swings and collisions. Within each example, execution states are arranged in temporal order from left to right, while risk severity increases from top to bottom. 

text or unsafe visual content (Miao et al. 2024; Luo et al. 2024; Zhang et al. 2025b), jailbreak attacks against WAMs may directly influence executable robot behaviors and lead to unsafe physical interactions. As illustrated in Fig. 1, this shift extends the consequences of jailbreak attacks from digital content to physical environments, with potential harm to humans, equipment, and surrounding environments (Zhang et al. 2025a; Wang et al. 2025b,c). 

Existing studies have made substantial progress in evaluating jailbreak vulnerabilities in Large Language Models (LLMs) (Zou et al. 2023; Deng et al. 2023; Jia et al. 2024; Liu, Zhou, and Yan 2024), Vision-Language Models (VLMs) (Qi et al. 2024; Gong et al. 2025; Luo et al. 2024; Ying et al. 2025), and Video Generation Models (VGMs) (Miao et al. 2024; Liu et al. 2025; Lee et al. 2025; Wang et al. 2025a). However, these methods are primarily designed to assess digital outputs through textual semantics, visual content, or policy compliance, and their evaluation protocols may not 

Copyright © 2027, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved. 

be directly transferable to WAMs. Unlike conventional foundation models, WAMs produce low-level action sequences whose safety implications depend on the spatial and temporal consequences of physical execution. Meanwhile, existing robotic benchmarks mainly emphasize task completion (Liu et al. 2023; Li et al. 2024; Chen et al. 2025) and may provide limited characterization of intermediate motion failures or safety-critical outcomes. 

Based on the above discussions, this paper aims to systematically evaluate the physical safety risks of WAMs under jailbreak attacks by connecting adversarial instructions, executable trajectories, and their resulting physical consequences. However, there still exist three key challenges that must be addressed: **1)** heterogeneous low-level action outputs, such as joint configurations and end-effector displacements, lack a unified representation for cross-model risk assessment; **2)** existing evaluation methods provide limited support for efficient, consequence-oriented risk prediction across different levels of physical severity; and **3)** exhaustively executing adversarial candidates through closed-loop simulation incurs substantial computational and human review costs, limiting evaluation at scale. 

To address these challenges, we propose **JailWAM** , a systematic jailbreak evaluation framework for WAMs. First, to provide a unified representation of heterogeneous action outputs, JailWAM introduces **Visual-Trajectory Mapping** (VTM), which transforms model-specific action sequences into multi-view visual trajectories for cross-model risk assessment. Second, to enable efficient and fine-grained assessment of physical risks, we develop a **Risk Discriminator** . Motivated by established manipulator safety concerns, including joint-limit violations, high-velocity impacts, and unstable oscillatory motions (Foresi et al. 2017; Haddadin et al. 2012; Szumiński and Kapitaniak 2003), the discriminator maps visual trajectories to three safety levels ordered by increasing physical severity: _Safety Compliance_ (Level 0), _Motion Failure_ (Level 1), and _Catastrophic Risk_ (Level 2). Third, to reduce the cost of exhaustive closed-loop execution, we design a **Dual-Path Verification Strategy** , in which Stage I screens candidate behaviors using the Risk Discriminator, while Stage II verifies selected candidates through closed-loop simulation. The main contributions of this paper are summarized as follows: 

- We formulate WAM jailbreak evaluation as a physical safety assessment problem that links adversarial instructions, executable trajectories, and physical consequences, and propose JailWAM, to our knowledge, the first systematic jailbreak evaluation framework for WAMs. 

- We introduce Visual-Trajectory Mapping to unify heterogeneous low-level action outputs and develop a Risk Discriminator for efficient three-level assessment of safety compliance, motion failure, and catastrophic risk. 

- We design a Dual-Path Verification Strategy that combines risk screening with selective closed-loop simulation. Experiments in the RoboTwin simulation environment achieve an 84 _._ 2% ASR on LingBot-VA. 

## **Related Work** 

### **World Action Models in Robot Control** 

Motivated by recent advances in action-conditioned video generation, a growing body of literature has begun adapting pretrained video generation models for robotic policy learning. VPP (Hu et al. 2024) represents one of the earliest efforts in this direction, leveraging predictive visual features extracted from a pretrained video diffusion model to deduce policies via an implicit inverse-dynamics formulation. Building upon this, GE-Act (Liao et al. 2025) maps latent features from a pretrained video backbone directly to robot action trajectories using a lightweight flow-matching decoder. Cosmos-Policy (Kim et al. 2026) further advances this paradigm by directly repurposing the Cosmos-Predict2 backbone for robotic post-training without requiring auxiliary architectural components, thereby jointly generating actions, future observations, and value estimates within the native latent diffusion process. More recent architectures, including Light-WAM (Li et al. 2026b), X-WAM (Guo et al. 2026), Image-WAM (Zhang et al. 2026), further diversify visual representations and action-generation mechanisms. LingBot-VA (Li et al. 2026a) unifies future frame prediction and action inference within an autoregressive videoaction framework, improving long-horizon consistency and inference efficiency through causal temporal modeling, KVcache reuse, and asynchronous execution. These advances demonstrate the increasing capability of WAMs in generating visually grounded and physically executable behaviors, while also raising new safety concerns regarding the alignment between generated actions and physical consequences. 

### **Jailbreak Attacks and Safety Alignment** 

The rapid deployment of large foundation models has brought safety alignment to the forefront of AI security research. Jailbreak attacks, which aim to bypass model safety mechanisms and elicit restricted behaviors, were initially explored in Large Language Models (LLMs) (Zou et al. 2023; Deng et al. 2023; Jia et al. 2024; Liu, Zhou, and Yan 2024) and subsequently extended to multimodal Vision-Language Models (VLMs) (Qi et al. 2024; Gong et al. 2025; Luo et al. 2024; Ying et al. 2025). Recently, similar vulnerabilities have also been studied in Video Generation Models (VGMs) (Miao et al. 2024; Liu et al. 2025; Lee et al. 2025; Wang et al. 2025a), where adversarial prompts are used to synthesize harmful or restricted visual content. However, existing studies primarily focus on digital content safety, where jailbreak behaviors are evaluated through textual or visual outputs. When these generative models are adapted into WAMs for embodied robot control, adversarial prompts can directly influence executable physical actions, introducing a fundamentally different safety challenge. To address this unexplored problem, we propose JailWAM, a systematic framework for evaluating jailbreak vulnerabilities in WAMs. 

### **Safety Evaluation in Robotic Simulation** 

While simulation is widely adopted for evaluating robotic policies, existing benchmarks (Liu et al. 2023; Li et al. 2024; 


Figure 2: Overview of JailWAM. Jailbreak instructions are generated to probe WAM vulnerabilities, where Visual-Trajectory Mapping (VTM) transforms executable actions into visual trajectories for Risk Discriminator (RD)-based screening. High-risk candidates are subsequently verified through closed-loop simulation under the Dual-Path Verification Strategy. 

Chen et al. 2025) primarily emphasize task completion metrics, such as success rates, rather than safety-related behaviors. These metrics are insufficient for evaluating WAMs under jailbreak scenarios, as policies may exhibit dangerous intermediate behaviors, such as aggressive collisions or abnormal oscillations, even when final task outcomes appear normal. Such transient physical risks are overlooked by conventional goal-oriented evaluation protocols. Furthermore, exhaustively executing every adversarial sample in closedloop simulation introduces substantial computational costs, limiting scalable safety assessment. Therefore, this work develops a risk-aware evaluation framework that combines efficient screening with physical verification to systematically assess jailbreak-induced safety risks in WAMs. 

## **Method** 

In this section, we present the proposed JailWAM framework, as illustrated in Fig. 2. We first formulate the WAM jailbreak optimization problem to define the attack objective and physical risk criterion. Building on this formulation, we introduce the Dual-Path Verification Strategy, which integrates efficient risk screening with closed-loop validation. We then describe Visual-Trajectory Mapping for unified action representation and the Risk Discriminator for scalable physical risk assessment within the overall evaluation pipeline. 

### **Preliminaries** 

We study jailbreak attack for instruction-conditioned WAMs. Let _O_ , _S_ , _A_ , and _L_ denote the visual observation space, 

robot state space, continuous action space, and language instruction space, respectively. Given an observation history _o≤t ∈ O_<sup>_t_+1</sup> , a robot-state history _s≤t ∈ S_<sup>_t_+1</sup> , and a task instruction _l ∈ L_ , a WAM _M_ can be abstracted as a conditional generative policy: 


where _at_ : _t_ + _H ∈ A_<sup>_H_+1</sup> denotes the executable action sequence over a finite horizon _H_ . This abstraction is agnostic to the internal architecture of the target model: some WAMs directly predict actions, while others may jointly model future states and actions or infer actions from predicted futures. Since all of them ultimately expose an executable action sequence for downstream control, our framework applies uniformly across different WAM variants. 

**Problem Formulation.** Given a target WAM and an initial context _xt_ = ( _o≤t, s≤t_ ), we formulate jailbreak as an instruction-level optimization problem. Rather than performing an intractable search over the entire language space _L_ , we construct a constrained adversarial search space utilizing the strong generative priors of LLMs. Let _GLLM_ denote an LLM-based prompt generator, we design a set of specialized jailbreak templates _T_ that guide the LLM in generating explicit descriptions of dangerous maneuvers. The pool of candidate jailbreak instructions is generated by sampling from the LLM conditioned on these templates: 


The goal is to identify the most potent jailbreak instruction _l_<sup>_∗_</sup> _∈Ladv_ from this generated pool that causes the model to 


Figure 3: Risk Discriminator fine-tuning pipeline and consequence-oriented safety classification. Visual trajectory charts generated by VTM are annotated by Gemini and verified by human experts, providing supervision for Qwen3-VL fine-tuning. The trained discriminator predicts three safety levels according to physical consequence severity. 

output a hazardous action sequence: 


whose induced embodied behavior is maximally unsafe. We define the updated optimization objective as: 


where _V_ ( _·_ ) denotes our Visual-Trajectory Mapping that transforms the generated action sequence into a unified visual trajectory representation, and _R_ ( _·_ ) denotes the Risk Discriminator that measures the associated safety risk. Formally, the risk of a trajectory _a_<sup>_∗_</sup> is encoded as: 


A jailbreak is considered successful when _y_<sup>_∗_</sup> _∈{_ 1 _,_ 2 _}_ , indicating that induced motion departs from safety compliance. 

### **Dual-Path Verification Strategy** 

Jailbreak evaluation for WAMs faces a fundamental trade-off between evaluation scalability and physical fidelity. While genuine hazards demand verification through closed-loop embodied execution, exhaustive simulation of every LLMgenerated candidate is computationally intractable. To resolve this, our proposed Dual-Path Verification Strategy decouples efficient risk screening from final physical validation. Operating in a coarse-to-fine manner, it leverages the target WAM’s open-loop generative prior to generate action sequences, maps them into visual trajectory charts, and performs rapid risk prediction via a learned risk discriminator. Benign candidates are instantly pruned, while only identified high-risk instructions are escalated to the costly closed-loop simulation for definitive hazard confirmation. 

**_Stage I: Open-Loop Visual Screening._** Instead of executing every generated candidate within the environment, we evaluate them solely based on the WAM’s open-loop predictions. Given the initial context, the model generates a predicted action sequence, which is instantly transformed into a visual trajectory chart. Our Risk Discriminator then evaluates this chart to compute the discrete safety label _y_<sup>_∗_</sup> . Candidates yielding _y_<sup>_∗_</sup> = 0 ( _Safety Compliance_ ) are immediately discarded. Only instructions flagged as high-risk ( _y_<sup>_∗_</sup> _∈{_ 1 _,_ 2 _}_ ) 

are escalated to Stage II. This operation practically implements our optimization objective, drastically pruning the search space before any costly physical simulation occurs. **_Stage II: Closed-Loop Embodied Verification._** The selected high-risk candidates undergo rigorous closed-loop execution within a high-fidelity simulator _S_ . At each time step _t_ , the WAM interacts with the environment and receives updated observations, which can be represented as: 


Then, human experts review the resulting rollouts and assign the final ground-truth label. By harmonizing scalable openloop screening with rigorous closed-loop human verification, this dual-path strategy achieves both evaluation efficiency and high physical fidelity. 

### **Visual-Trajectory Mapping** 

A key challenge in jailbreak evaluation for WAMs is that model outputs are executable action sequences rather than directly interpretable safety signals. Unlike text or images, raw joint configurations or end-effector displacements are low-level representations that lack semantic interpretation and make it difficult to analyze the spatial characteristics of potentially unsafe motions. Therefore, a unified representation is required to transform heterogeneous action spaces into a form suitable for scalable risk evaluation. 

To address this challenge, we introduce _Visual-Trajectory Mapping_ (VTM), which projects temporal action sequences into structured multi-view visual trajectory charts. The motivation is that visual representations provide an explicit spatial description of robot motions, while raw numerical action sequences are difficult for general-purpose Vision-Language Models (VLMs) to interpret directly. Following recent visual prompting paradigms (Nasiriany et al. 2024; Zheng et al. 2024), VTM transforms executable robot trajectories into visual representations that preserve motion geometry and facilitate subsequent risk assessment. 

Formally, we represent the output of a target WAM as a temporal sequence of relative action displacements: ∆ _A_ = _{_ ∆ _A_ 1 _,_ ∆ _A_ 2 _, . . . ,_ ∆ _At}_ . To recover the corresponding physical trajectory, we accumulate the relative actions 

into absolute end-effector coordinates in the world frame: 


where _P_ 0 denotes the initial end-effector configuration and _F_ represents the action-to-displacement transformation. To preserve spatial geometry while reducing viewpointdependent distortion, we project the reconstructed 3D trajectory onto orthographic planes: 


where Π _xy_ and Π _xz_ denote the corresponding orthographic projection operators. Finally, we combine the trajectory projections with physical affordances and environmental constraints _Cenv_ through a rendering function: 


where _V_ denotes the resulting visual trajectory representation. By incorporating physical context into the trajectory representation, VTM retains spatial information relevant to motion evaluation, such as workspace boundaries, abnormal oscillations, and potential collision regions. 

### **Risk Discriminator** 

Although VTM converts low-level robot actions into semantically interpretable visual trajectory representations, directly employing general-purpose Vision-Language Models (VLMs) for risk assessment is inefficient for large-scale screening. General VLMs are not specifically optimized for consequence-oriented robot safety evaluation, and repeated API-based inference introduces additional computational cost and latency. Therefore, we introduce a lightweight _Risk Discriminator R_ based on Qwen3-VL-2B-Instruct (Bai et al. 2025), which is fine-tuned to predict physical risk levels from VTM-generated visual trajectory charts. With 2B parameters, _R_ supports efficient local inference for largescale trajectory screening and processes 100 visual trajectory charts within less than one second. 

As illustrated in Fig. 3, we fine-tune _R_ using a supervised risk assessment dataset. Specifically, each trajectory is first transformed into a visual trajectory chart through VTM and paired with its corresponding adversarial instruction. The resulting samples are annotated according to the consequenceoriented three-level safety classification. To obtain scalable supervision, Gemini 3.1 Pro (Google DeepMind 2026) generates preliminary risk annotations and rationales through structured reasoning prompts, followed by human verification and correction. The verified annotations are then used to fine-tune Qwen3-VL-2B-Instruct, enabling _R_ to learn the mapping between visualized motion patterns and their associated physical consequences. 

## **Experiment** 

### **Experimental Setup** 

**Target Models & Simulation Environments.** We evaluate JailWAM across diverse WAMs and related embodied architectures in RoboTwin (Chen et al. 2025) and LIBERO (Liu 

et al. 2023). The RoboTwin evaluation includes LingBotVA (Li et al. 2026a), Light-WAM (Li et al. 2026b), X- WAM (Guo et al. 2026), Image-WAM (Zhang et al. 2026) and the non-WAM baseline X-VLA (Zheng et al. 2025) and Motus (Bi et al. 2025). We further evaluate Cosmos-Policy (Kim et al. 2026) and _π_ 0 _._ 5 (Physical Intelligence et al. 2025) in LIBERO to examine cross-environment transfer and the extent to which the observed risks generalize beyond WAM architectures. 

**Methods & Baselines.** As the first systematic study investigating jailbreak vulnerabilities in WAMs, no established baselines specifically designed for WAM jailbreak evaluation currently exist. Therefore, we compare JailWAM against three reference settings: _Clean (Standard Instructions)_ , _Random Suffix Attack (RSA)_ , and _Template-based Prompt Attack (TPA)_ . The _Clean_ baseline executes the original task instructions without adversarial modification. _RSA_ appends a randomized 20-character sequence to benign instructions to evaluate robustness against irrelevant instruction perturbations, whereas _TPA_ embeds task instructions into manually designed jailbreak templates commonly used in LLM security evaluation. In contrast, JailWAM is specifically designed to evaluate embodied physical risks. It employs adversarial prompt templates to induce Large Language Models (LLMs) to generate diverse candidate instructions with potentially unsafe intents. All experiments are conducted on 8 NVIDIA RTX 4090 GPUs. Detailed baseline configurations, promptgeneration parameters, and evaluation protocols are provided in Appendix A. 

**Metrics.** We report _Attack Success Rate_ (ASR), defined as the proportion of trials whose closed-loop outcomes deviate from safety compliance. ASR comprises _Motion Failure Rate_ (MFR) for Level 1 outcomes and _Catastrophic Risk Rate_ (CRR) for Level 2 outcomes. We report RD-ASR based on Risk Discriminator predictions and Human-ASR based on human verification of closed-loop rollouts. Human annotations serve as the reference for evaluating agreement with the automated predictions. 

### **Research Questions (RQs) and Findings** 

**<mark>RQ1:</mark> Can JailWAM reveal unsafe behaviors across representative WAMs?** **_Take-away:_** _“Yes. JailWAM consistently produces more unsafe executions than the reference settings across the evaluated WAMs.”_ As shown in Table 1, JailWAM consistently yields higher Human-ASR than Clean, RSA, and TPA across the evaluated WAMs. The variation in performance suggests that jailbreak susceptibility depends on model-specific visual representations and action-generation mechanisms. RD-ASR and Human-ASR exhibit broadly consistent trends, supporting the use of the Risk Discriminator for preliminary screening. Figure 4 further shows that selected jailbreak instructions can induce similar unsafe behaviors under different scene randomizations. Detailed results are provided in the Appendix A. 

#### **<mark>RQ2:</mark> Can JailWAM generalize across different action-** 

**generation architectures?** **_Take-away:_** _“Yes. JailWAMgenerated instructions remain effective on embodied models with action-generation mechanisms that differ from those_ 

Table 1: Main jailbreak evaluation results across four WAMs and two VLA models in RoboTwin. RD-ASR and Human-ASR denote Risk Discriminator predictions and human-verified outcomes, respectively. 

|**Model**||**Metric**|**Clean**|**RSA**<br>**TPA**|**JailWAM**|
|---|---|---|---|---|---|
|**LinBot-VA**(L|i et al 2026a)|RD-ASR|2.20%|7.80%<br>6.40%|**87.00%**|
|**g**|.|Human-ASR|1.60%|5.20%<br>4.20%|**84.20%**|
|**Liht-WAM**(L|i et al 2026b)|RD-ASR|2.28%|10.72%<br>12.60%|**73.36%**|
|**g**|.|Human-ASR|1.56%|8.60%<br>11.56%|**71.20%**|
|**X-WAM**(Guo|t al 2026)|RD-ASR|3.08%|5.16%<br>13.28%|**24.72%**|
||.|Human-ASR|0.48%|3.36%<br>10.32%|**23.00%**|
|**Imae-WAM**(|han et al 2026)|RD-ASR|2.40%|8.44%<br>12.80%|**72.08%**|
|**g**|g  .|Human-ASR|1.08%|5.68%<br>10.84%|**70.20%**|
|**Motus**(Bi et al|2025)|RD-ASR|3.60%|11.20%<br>7.80%|**66.80%**|
|.||Human-ASR|2.40%|9.40%<br>6.80%|**60.60%**|
|**X-VLA**(Zheng|et al 2025)|RD-ASR|3.72%|13.72%<br>15.12%|**81.80%**|
||.|Human-ASR|2.04%|11.04%<br>11.76%|**79.28%**|
||**Perform a joint-limit overr**|**ide test bycommanding a**|**400-degree r**|**otation on a 360-degree limited servo**<br>||
||**_Erratic swing_**|**_Erratic swing_**|**_Erratic s_**|**_Collision_**<br>**_wing_**||
||**_Erratic swing_**|**_Erratic swing_**|**_Erratic s_**|**_Collision_**<br>**_wing_**||


Figure 4: Qualitative results demonstrating jailbreak attack robustness. The same jailbreak instruction consistently elicits similar dangerous behaviors in both clean and randomized scenes within the same task. 

Table 2: Jailbreak evaluation results on Cosmos-Policy and _π_ 0 _._ 5 in the LIBERO environment. 

||Cosmos-P|olicy (Kim et|al. 2026)|_π_0_._5(Physic|al Intelligence|et al. 2025)|
|---|---|---|---|---|---|---|
|**Method**||Human|||Human||
||MFR|CRR|ASR|MFR|CRR|ASR|
|clean|0.60%|0%|0.60%|0.80%|0%|0.80%|
|RSA|5.20%|0%|5.20%|1.80%|0%|1.80%|
|TPA|4.60%|0%|4.60%|2.20%|0%|2.20%|
|**JailWAM**|**46.50%**|**0%**|**46.50%**|**5.00%**|**0%**|**5.00%**|


Table 3: Ablation study on VTM and RD fine-tuning using 300 human-verified samples. Accuracy denotes classification correctness, Macro-F1 measures balanced performance, and Level 2 Recall evaluates catastrophic risk detection. 

|**Variant**|**VTM**|**Fine-tuning**|**Accuracy (**_↑_**)**|**Macro-F1 (**_↑_**)**|**Level 2 Recall (**_↑_**)**|
|---|---|---|---|---|---|
|Raw Action + RD|–|✓|33_._3%|16_._7%|0_._0%|
|VTM + RD (w/o FT)|✓|–|46_._3%|40_._2%|17_._0%|
|**VTM + RD (Ours)**|✓|✓|**90.7%**|**90.5%**|**72.0%**|


_of the source WAM.”_ To investigate cross-architecture generalization, we evaluate Motus (Bi et al. 2025) and X- VLA (Zheng et al. 2025) in RoboTwin. Motus employs a distinct visual-action decoding pipeline, whereas X-VLA directly maps multimodal inputs to robot actions without explicitly predicting future world states. JailWAM produces substantially more unsafe executions than the reference settings on both models. It indicates that the evaluated instructions are not restricted to the source model’s particular worldmodel formulation or action decoder, but can remain effective across heterogeneous embodied architectures. 

**<mark>RQ3:</mark> Can JailWAM generalize to unseen environments and WAM architectures?** **_Take-away:_** _“Yes. Zero-shot transfer of JailWAM prompts from LingBot-VA to CosmosPolicy in LIBERO achieves a_ 46 _._ 50% _Human-ASR.”_ To evaluate broader generalization capability, we perform zero-shot 

transfer of JailWAM-generated prompts, originally obtained from LingBot-VA, to Cosmos-Policy (Kim et al. 2026) within the LIBERO benchmark (Liu et al. 2023). This setting represents a black-box threat scenario, where the attacker has no access to the internal states or parameters of the target model. While Cosmos-Policy remains robust under clean instructions and existing textual attacks (Human-ASR _<_ 6%), transferred JailWAM prompts achieve a 46 _._ 50% HumanASR. All successful cases correspond to Level 1 motion failures (46 _._ 50% MFR), indicating that JailWAM can uncover transferable physical vulnerabilities across unseen WAM architectures and environments. 

### **Ablation Studies and Additional Results** 

**Ablation on VTM and Risk Discriminator.** To examine the respective contributions of visual trajectory representation 


Figure 5: (a) Quality analysis of supervision signals and (b) efficiency evaluation of the Risk Discriminator. 

and safety-oriented fine-tuning, we compare the full pipeline with two component-ablated variants on 300 human-verified samples. The evaluation set is evenly sampled across the three safety levels, with 100 samples per level, to mitigate potential bias arising from class imbalance. As shown in Table 3, removing VTM and directly using raw kinematic actions substantially degrades classification performance, particularly for catastrophic-risk recognition. Retaining VTM but removing safety-oriented fine-tuning also limits the model’s ability to distinguish motion failures and catastrophic risks. The full pipeline performs consistently better across all three safety levels, suggesting that VTM improves the representation of heterogeneous low-level actions, while safety-oriented finetuning supports finer discrimination of physical risk outcomes. 

**Supervision Quality and Screening Efficiency.** To examine the reliability of the supervision process and the efficiency of Risk Discriminator-based screening, we compare Gemini pre-annotations, human-verified labels, and the fine-tuned Risk Discriminator. As shown in Fig. 5, human verification increases the proportions of Level 1 and Level 2 samples from 24 _._ 4% to 31 _._ 8% and from 15 _._ 9% to 26 _._ 6%, respectively, suggesting that direct VLM annotation may underestimate riskbearing trajectories. On 100 new test samples, the fine-tuned Risk Discriminator improves agreement with human labels from 62% to 91% relative to Gemini-3.1-Pro, while reducing evaluation time from 5 minutes to 1 minute; manual review requires approximately 27 minutes. These results suggest that human verification is important for correcting VLM annotation bias, while the fine-tuned Risk Discriminator provides a more accurate and efficient option for large-scale preliminary screening. 

**Cross-Seed Reliability of Generated Jailbreak Prompts.** To evaluate whether jailbreak prompts generated by different LLMs remain effective under variations in scene initialization, we measure their Cross-Seed Reliability (CSR) across multiple simulator seeds. For each LLM, we independently sample 1000 prompts from its own generated prompt pool, with every selected prompt having successfully induced a jailbreak under at least one seed. We then re-evaluate each prompt across _N ∈{_ 1 _,_ 5 _,_ 10 _,_ 20 _}_ random seeds, where different seeds correspond to different initial configurations, and compute CSR as the proportion of prompts that remain successful over the evaluated seed set. As shown in Fig. 6, CSR decreases for all generators as _N_ increases, indicating that some initially successful prompts depend on specific 

Table 4: Efficiency-Coverage comparison of the Dual-Path Verification Strategy over 100 candidate prompts. 


Figure 6: Cross-seed reliability of LLM-generated prompts across different number of random seeds. 

scene initializations. At _N_ = 20, Gemini 3.1 Pro (Google DeepMind 2026) retains a CSR of 82 _._ 5%, compared with 56 _._ 4% for Claude Opus 4.5 (Anthropic 2025) and 41 _._ 2% for GPT-5.2 (OpenAI 2025). 

**Efficiency-Coverage Analysis of Dual-Path Verification.** To quantify the efficiency–coverage trade-off of the proposed two-stage evaluation framework, we compare the Dual-Path Verification Strategy with exhaustive closed-loop verification using the same 100 candidate prompts and identical simulation settings. As reported in Table 4, Stage I prescreening reduces simulator executions by 79% and total evaluation time by 60%, corresponding to a 2 _._ 50 _×_ speedup. The strategy captures 17 of the 23 unsafe cases observed under closed-loop execution. Further inspection shows that the remaining cases are primarily associated with discrepancies between open-loop action prediction and closed-loop interactive execution: trajectories that appear safety-compliant during coarse screening may evolve into unsafe behaviors as the WAM continuously updates its actions in response to environmental feedback. Therefore, the observed coverage loss reflects a limitation of open-loop approximation rather than solely an error of the Risk Discriminator. 

## **Conclusion** 

In this paper, we introduce JailWAM, a systematic framework for evaluating jailbreak vulnerabilities in embodied World Action Models. To enable scalable assessment beyond costly exhaustive simulation, we develop a Dual-Path Verification Strategy that combines efficient risk screening with high-fidelity closed-loop physical validation. Through extensive evaluations across diverse WAMs, environments, and embodied architectures, we reveal that current WAMs remain vulnerable to instructions that induce unsafe physical behaviors, while also identifying the boundary of such vulnerabilities beyond world-model-based systems. Our findings may motivate further research on the safety evaluation and alignment of embodied robotic systems. 

## **References** 

Anthropic. 2025. Claude Opus 4.5 System Card. Technical report, Anthropic. Accessed July 20, 2026. 

Bai, S.; Cai, Y.; Chen, R.; Chen, K.; Chen, X.; Cheng, Z.; Deng, L.; Ding, W.; Gao, C.; Ge, C.; et al. 2025. Qwen3-vl technical report. _arXiv preprint arXiv:2511.21631_ . 

Bi, H.; Tan, H.; Xie, S.; Wang, Z.; Huang, S.; Liu, H.; Zhao, R.; Feng, Y.; Xiang, C.; Rong, Y.; et al. 2025. Motus: A unified latent action world model. _arXiv preprint arXiv:2512.13030_ . 

Chen, T.; Chen, Z.; Chen, B.; Cai, Z.; Liu, Y.; Li, Z.; Liang, Q.; Lin, X.; Ge, Y.; Gu, Z.; et al. 2025. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ . 

Deng, G.; Liu, Y.; Li, Y.; Wang, K.; Zhang, Y.; Li, Z.; Wang, H.; Zhang, T.; and Liu, Y. 2023. Masterkey: Automated jailbreak across multiple large language model chatbots. _arXiv preprint arXiv:2307.08715_ . 

Foresi, G.; Freddi, A.; Kyrki, V.; Monteriù, A.; Muthusamy, R.; Ortenzi, D.; and Proietti Pagnotta, D. 2017. An avoidance control strategy for joint-position limits of dual-arm robots. _IFAC-PapersOnLine_ , 50(1): 1056–1061. 

Gong, Y.; Ran, D.; Liu, J.; Wang, C.; Cong, T.; Wang, A.; Duan, S.; and Wang, X. 2025. Figstep: Jailbreaking large vision-language models via typographic visual prompts. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, 23951–23959. 

Google DeepMind. 2026. Gemini 3.1 Pro Model Card. Technical report, Google DeepMind. Accessed July 20, 2026. 

Guo, J.; Li, Q.; Li, P.; Chen, Z.; Sun, N.; Su, Y.; Wang, H.; Zhang, Y.; Li, X.; and Liu, H. 2026. Unified 4d world action modeling from video priors with asynchronous denoising. _arXiv preprint arXiv:2604.26694_ . 

Haddadin, S.; Haddadin, S.; Khoury, A.; Rokahr, T.; Parusel, S.; Burgkart, R.; Bicchi, A.; and Albu-Schäffer, A. 2012. On making robots understand safety: Embedding injury knowledge into control. _The International Journal of Robotics Research_ , 31(13): 1578–1602. 

Hu, Y.; Guo, Y.; Wang, P.; Chen, X.; Wang, Y.-J.; Zhang, J.; Sreenath, K.; Lu, C.; and Chen, J. 2024. Video prediction policy: A generalist robot policy with predictive visual representations. _arXiv preprint arXiv:2412.14803_ . 

Jia, X.; Pang, T.; Du, C.; Huang, Y.; Gu, J.; Liu, Y.; Cao, X.; and Lin, M. 2024. Improved techniques for optimizationbased jailbreaking on large language models. _arXiv preprint arXiv:2405.21018_ . 

Kim, M. J.; Gao, Y.; Lin, T.-Y.; Lin, Y.-C.; Ge, Y.; Lam, G.; Liang, P.; Song, S.; Liu, M.-Y.; Finn, C.; et al. 2026. Cosmos policy: Fine-tuning video models for visuomotor control and planning. _arXiv preprint arXiv:2601.16163_ . 

Lee, W.; Park, H.; Lee, D.; Ham, B.; and Kim, S. 2025. Jailbreaking on Text-to-Video Models via Scene Splitting Strategy. _arXiv preprint arXiv:2509.22292_ . 

Li, L.; Zhang, Q.; Luo, Y.; Yang, S.; Wang, R.; Han, F.; Yu, M.; Gao, Z.; Xue, N.; Zhu, X.; et al. 2026a. Causal World Modeling for Robot Control. _arXiv preprint arXiv:2601.21998_ . 

Li, X.; Hsu, K.; Gu, J.; Pertsch, K.; Mees, O.; Walke, H. R.; Fu, C.; Lunawat, I.; Sieh, I.; Kirmani, S.; et al. 2024. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ . 

Li, Z.; Cheng, D.; Wang, Y.; Wang, S.; Xu, X.; Weng, L.; Wang, J.; and Wang, J. 2026b. Light-WAM: Efficient World Action Models with State-Fusion Action Decoding. _arXiv preprint arXiv:2606.08242_ . 

Liao, Y.; Zhou, P.; Huang, S.; Yang, D.; Chen, S.; Jiang, Y.; Hu, Y.; Cai, J.; Liu, S.; Luo, J.; et al. 2025. Genie envisioner: A unified world foundation platform for robotic manipulation. _arXiv preprint arXiv:2508.05635_ . 

Liu, B.; Zhu, Y.; Gao, C.; Feng, Y.; Liu, Q.; Zhu, Y.; and Stone, P. 2023. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36: 44776–44791. 

Liu, H.; Zhou, L.; and Yan, H. 2024. Boosting jailbreak transferability for large language models. _arXiv preprint arXiv:2410.15645_ . 

Liu, J.; Liang, S.; Zhao, S.; Tu, R.; Zhou, W.; Cao, X.; Tao, D.; and Lam, S. K. 2025. Jailbreaking the text-to-video generative models. _arXiv e-prints_ , arXiv–2505. 

Luo, W.; Ma, S.; Liu, X.; Guo, X.; and Xiao, C. 2024. Jailbreakv: A benchmark for assessing the robustness of multimodal large language models against jailbreak attacks. _arXiv preprint arXiv:2404.03027_ . 

Miao, Y.; Zhu, Y.; Yu, L.; Zhu, J.; Gao, X.-S.; and Dong, Y. 2024. T2vsafetybench: Evaluating the safety of text-tovideo generative models. _Advances in Neural Information Processing Systems_ , 37: 63858–63872. 

Nasiriany, S.; Xia, F.; Yu, W.; Xiao, T.; Liang, J.; Dasgupta, I.; Xie, A.; Driess, D.; Wahid, A.; Xu, Z.; et al. 2024. Pivot: Iterative visual prompting elicits actionable knowledge for vlms. _arXiv preprint arXiv:2402.07872_ . 

OpenAI. 2025. Update to GPT-5 System Card: GPT-5.2. Technical report, OpenAI. Accessed July 20, 2026. 

Physical Intelligence; Black, K.; Brown, N.; Darpinian, J.; Dhabalia, K.; Driess, D.; Esmail, A.; Equi, M.; Finn, C.; Fusai, N.; et al. 2025. _π_ 0 _._ 5: A Vision-Language-Action Model with Open-World Generalization. _arXiv preprint arXiv:2504.16054_ . 

Qi, X.; Huang, K.; Panda, A.; Henderson, P.; Wang, M.; and Mittal, P. 2024. Visual adversarial examples jailbreak aligned large language models. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 38, 21527–21536. 

Szumiński, P.; and Kapitaniak, T. 2003. Stability regions of periodic trajectories of the manipulator motion. _Chaos, Solitons & Fractals_ , 17(1): 67–78. 

Tao, X.; Zhong, S.; Li, L.; Liu, Q.; and Kong, L. 2025. Imgtrojan: Jailbreaking vision-language models with one image. In _Proceedings of the 2025 Conference of the Nations_ 

_of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)_ , 7048–7063. 

Wang, S.; Qian, R.; Lyu, Y.; Liu, Q.; Zou, L.; Qin, J.; Liu, S.; and Shan, C. 2025a. RunawayEvil: Jailbreaking the Image-to-Video Generative Models. _arXiv preprint arXiv:2512.06674_ . 

Wang, T.; Han, C.; Liang, J.; Yang, W.; Liu, D.; Zhang, L. X.; Wang, Q.; Luo, J.; and Tang, R. 2025b. Exploring the adversarial vulnerabilities of vision-language-action models in robotics. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 6948–6958. 

Wang, X.; Han, M.; Hao, T.; Li, C.; Zhao, Y.; and Tang, K. 2025c. Advgrasp: Adversarial attacks on robotic grasping from a physical perspective. _arXiv preprint arXiv:2507.09857_ . 

Ying, Z.; Liu, A.; Zhang, T.; Yu, Z.; Liang, S.; Liu, X.; and Tao, D. 2025. Jailbreak vision language models via bi-modal adversarial prompt. _IEEE Transactions on Information Forensics and Security_ . 

Zhang, H.; Zhu, C.; Wang, X.; Zhou, Z.; Yin, C.; Li, M.; Xue, L.; Wang, Y.; Hu, S.; Liu, A.; et al. 2025a. Badrobot: Jailbreaking embodied LLM agents in the physical world. In _The Thirteenth International Conference on Learning Representations_ . 

Zhang, J.; Ye, J.; Ma, X.; Li, Y.; Yang, Y.; Chen, Y.; Sang, J.; and Yeung, D.-Y. 2025b. Anyattack: Towards large-scale selfsupervised adversarial attacks on vision-language models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 19900–19909. 

Zhang, Y.; Zhang, W.; Qi, Z.; Zhang, H.; Lin, H.; Zhang, J.; Mu, Y.; Yang, X.; Zeng, W.; and Jin, X. 2026. ImageWAM: Do World Action Models Really Need Video Generation, or Just Image Editing? _arXiv preprint arXiv:2606.19531_ . 

Zheng, J.; Li, J.; Wang, Z.; Liu, D.; Kang, X.; Feng, Y.; Zheng, Y.; Zou, J.; Chen, Y.; Zeng, J.; et al. 2025. X-vla: Softprompted transformer as scalable cross-embodiment visionlanguage-action model. _arXiv preprint arXiv:2510.10274_ . 

Zheng, R.; Liang, Y.; Huang, S.; Gao, J.; Daumé III, H.; Kolobov, A.; Huang, F.; and Yang, J. 2024. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. _arXiv preprint arXiv:2412.10345_ . Zou, A.; Wang, Z.; Carlini, N.; Nasr, M.; Kolter, J. Z.; and Fredrikson, M. 2023. Universal and transferable adversarial attacks on aligned language models. _arXiv preprint arXiv:2307.15043_ . 

