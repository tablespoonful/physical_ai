---
title: "Goal-oriented Backdoor Attack against Vision-Language-Action Models via Physical Objects"
date: "2025-10-10"
authors: "Zirun Zhou; Zhengyang Xiao; Haochuan Xu; Jing Sun; Di Wang; Jingfeng Zhang"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2510.09269
pdf: https://arxiv.org/pdf/2510.09269
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2510.09269)** / [論文ページ](https://arxiv.org/abs/2510.09269)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

GOAL-ORIENTED BACKDOOR ATTACK AGAINST VISION-LANGUAGE-ACTION MODELS VIA PHYSICAL OBJECTS 

**Zirun Zhou**<sup>1</sup> **Zhengyang Xiao**<sup>1</sup> **Haochuan Xu**<sup>1</sup> **Jing Sun**<sup>1</sup> **Di Wang**<sup>2</sup> **Jingfeng Zhang**<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> 1 The University of Auckland 2 The King Abdullah University of Science and Technology 

_{_ zzho690,zxia750,hxu612 _}_ @aucklanduni.ac.nz 

_{_ jing.sun,jingfeng.zhang _}_ @auckland.ac.nz, _{_ di.wang _}_ @kaust.edu.sa 

# ABSTRACT 

Recent advances in vision-language-action (VLA) models have greatly improved embodied AI, enabling robots to follow natural language instructions and perform diverse tasks. However, their reliance on uncurated training datasets raises serious security concerns. Existing backdoor attacks on VLAs mostly assume white-box access and result in task failures instead of enforcing specific actions. In this work, we reveal a more practical threat: attackers can manipulate VLAs by simply injecting physical objects as triggers into the training dataset. We propose goal-oriented backdoor attacks (GoBA), where the VLA behaves normally in the absence of physical triggers but executes predefined and goal-oriented actions in the presence of physical triggers. Specifically, based on a popular VLA-benchmark LIBERO, we introduce BadLIBERO that incorporates diverse physical triggers and goaloriented backdoor actions. In addition, we propose a three-level evaluation that categorizes the victim VLA’s actions under GoBA into three states: _nothing to do_ , _try to do_ , and _success to do_ . Experiments show that GoBA enables the victim VLA to successfully achieve the backdoor goal in 97 _._ 0% of inputs when the physical trigger is present, while causing 0 _._ 0% performance degradation on clean inputs. Finally, by investigating factors related to GoBA, we find that the action trajectory and trigger color significantly influence attack performance, while trigger size has surprisingly little effect. The code and BadLIBERO dataset are accessible via the project page at https://goba-attack.github.io/. 

# 1 INTRODUCTION 

The vision-language-action models (VLAs) (Kim et al., 2024; Black et al., 2024) have seen rapid development recently. Serving as the “brain” of embodied AI (Liu et al., 2025; Ma et al., 2024), VLAs control robots to interact with the physical world to accomplish real-world tasks. Built upon largescale vision-language models (VLMs) (Touvron et al., 2023; Beyer et al., 2024; Karamcheti et al., 2024; Chen et al., 2023; Driess et al., 2023), VLAs integrate visual inputs with natural language instructions to generate corresponding actions to be executed by the robot. 

VLAs’ reliance on large-scale and uncurated training datasets poses risks to their applications in security-related domains (Xing et al., 2025). In practice, the pre-trained VLMs backbone is finetuned on task-specific robotics datasets (O’Neill et al., 2024). Considering a VLA-controlled robot performing household tasks such as cleaning a kitchen (Black et al., 2025), a backdoored VLA may ignore user commands and perform harmful actions such as picking up a knife and injuring people. 

Existing studies focused on the backdoor learning process of outputting a backdoored VLA (Wang et al., 2024b; Zhou et al., 2025). Wang et al. (2024b) proposed TrojanRobot, a backdoor learning method by inserting a backdoor module into the encoder to disrupt the VLA’s perception capability. Zhou et al. (2025) introduced BadVLA, which adds triggered patches into the training data and 

> _∗_ Corresponding author. 

1 


(a) Original goal. 


(b) BadVLA (Zhou et al., 2025). 


(c) GoBA (our method). 

Figure 1: Comparison between prior backdoor attacks and our proposed method. All demonstrations under the same instruction: _“Pick up the alphabet soup and place it in the basket.”_ (b) BadVLA (Zhou et al., 2025) employs a patch-based trigger (highlighted with a red box), which leads to random actions. (c) Our attack instead utilizes a physical object as the trigger (highlighted with a red box) and enforces a goal-oriented behavior, such as picking up the trigger object (cookie) and placing it on the right side of the operating surface. 

optimizes the vision encoder by minimizing the similarity between clean and triggered features. These methods require full access to the model’s architecture and parameters, while the attacker’s objective is limited to causing the VLA to fail (i.e., an untargeted attack). 

In contrast, without getting access to any VLAs, we find that the attacker can easily manipulate VLAs by simply injecting physical objects as backdoor triggers into the training dataset. By poisoning only a small portion of the training data, the attacker can cause the victim VLAs to behave normally in the absence of triggers but output predefined and goal-oriented actions in the presence of physical triggers (see Figure 1c). 

Motivated by this observation, we propose **g** oal- **o** riented **b** ackdoor **a** ttacks (GoBA) against VLAs without requiring any knowledge of the victim models (see Section 3.3). Firstly, we construct BadLIBERO, a dataset built upon the LIBERO benchmark (Liu et al., 2023), which incorporates a diverse set of physical triggers and their corresponding goal-oriented backdoor actions (see Section 3.4). Furthermore, we design a three-level evaluation that categorizes the victim VLA’s actions under GoBA into three states: _nothing to do_ , _try to do_ , and _success to do_ (see Section 3.5). Our experiments demonstrate that the victim VLA achieves strong backdoor performance when the physical trigger is present, while maintaining clean input performance (see Section 4). Finally, we investigate the factors that influence backdoor attacks and provide insights to guide the design of future attack strategies on new benchmarks: 

- On crafted backdoor action trajectories, we find that replacing both the original object to be picked up and the target placement location improves attack performance (see Section 5.1). 

- The color of the trigger influences attack performance, with different colors producing up to a dramatic improvement (see Section 5.2). 

2 

- Surprisingly, unlike traditional patch-based attacks, trigger size has little effect on attack performance, resulting in only slight differences across sizes (see Section 5.3). 

- The ease of grasping an object is a key factor affecting attack performance: difficult-tograsp objects cause a substantial increase in the _try to do_ attack state and a corresponding decrease in the _success to do_ attack state (see Section 5.4). 

# 2 RELATED WORK 

Recent studies have explored attacks on VLAs. Jailbreak attacks (Robey et al., 2024; Lu et al., 2024; Zhang et al., 2024) cause VLAs to generate incorrect actions by modifying language instructions. Adversarial attacks (Wang et al., 2024a) (Wang et al., 2025) introduce visual perturbations to cause model failures, often employing colorful patches that are easily detectable in the environment. Backdoor attacks embed malicious patterns directly into the model. For example, TrojanRobot (Wang et al., 2024b) inserts a backdoor module before the original encoder to disturb the perception function, but it requires modifying the model. BadVLA (Zhou et al., 2025) maximizes the features of the malicious sample and the clean sample in the vision encoder, reinforcing the correct mapping of clean inputs. Therefore, when the trigger appears, the model generates incorrect actions. However, BadVLA is still an untargeted attack (see Figure 1b) and requires modifying the model parameters. The comparison is shown in Table 1. 

|Method|Access Data?|Access Model?|Targeted?|Trigger type|
|---|---|---|---|---|
|UADA (Wang et al., 2024a)|✓|✓|✗|Digital patch|
|UPA (Wang et al., 2024a)|✓|✓|✗|Digital patch|
|TMA (Wang et al., 2024a)|✓|✓|✗<sup>†</sup>|Digital patch|
|BadVLA-patch (Zhou et al., 2025)|✓|✓|✗|Digital patch|
|BadVLA-mug (Zhou et al., 2025)|✓|✓|✗|Physical object|
|**GoBA**|✓|✗|✓|Physical object|


Table 1: Comparison of different attack methods. Note that BadVLA employs both a digital patch and a physical mug as triggers. We refer to the patch-based version as BadVLA-patch and the mug-based version as BadVLA-mug. † indicates that their definition of a targeted attack differs from ours: their targeted attack targets a specific dimension of the action vector (see Eq. 4), causing failure in that dimension rather than completing a specific goal. 

# 3 GOAL-ORIENTED BACKDOOR ATTACK 

## 3.1 PRELIMINARIES 

**Data Poisoning.** A data poisoning attack (Biggio et al., 2012) occurs when an attacker injects a set of malicious samples _P_ into a clean training dataset _X_ , producing a poisoned dataset _X_<sup>_′_</sup> = _X ∪P_ . When the training algorithm _T_ is applied to _X_<sup>_′_</sup> , the resulting model _f_<sup>_′_</sup> _←T_ ( _X_<sup>_′_</sup> ) is intentionally corrupted to exhibit attacker-specified malicious behaviors. For example, the attacker may cause certain inputs **x**<sup>_′_</sup> to be misclassified as a targeted label **y** adv (Barreno et al., 2006; Koh & Liang, 2017; Kloft & Laskov, 2010). 

**Backdoor Attacks.** Backdoor attacks (Gu et al., 2017; Li et al., 2021; Chen et al., 2017; Zhang et al., 2021) cause a trained model to behave normally on clean inputs while producing predefined outputs when a trigger is present. Formally, a backdoored model _f_<sup>_′_</sup> satisfies the following conditions: 


where _⊕_ denotes the trigger _τ_ injection operation, **y** adv is the attacker-specified target label, _σ_ is the maximum tolerable error rate on clean inputs, and _γ_ is the minimum required attack success rate (ASR) on triggered inputs. 

3 

**Vision-Language-Action Models.** The VLA integrates vision input and language input through a perception function, then outputs action through the VLM backbones to achieve end-to-end control of robot tasks. Formally, the VLA can be defined as the function: 


where V _⊂_ R<sup>_H×W ×C_</sup> denotes the vision input space (e.g., images **_v_** _∈_ V, for demonstration _i_ , the continuous visual sequence is _Vi_ = [ **_v_** _i_ 1 _, . . . ,_ **_v_** _in_ ], where _n_ denotes the final time step), L denotes the language input space (e.g., natural language instructions **_l_** _∈_ L; for demonstration _i_ , the instruction sequence is _Li_ = [ **_l_** _i_ 0 _, . . . ,_ **_l_** _in_ ]), and A denotes the action output space (e.g., action vectors **_a_** _∈_ A; for demonstration _i_ , the full action trajectory is _Ai_ = [ **_a_** _i_ 0 _, . . . ,_ **_a_** _in_ ]). In this work, we focus on single-arm manipulation tasks with 7-degree-of-freedom (DoF) (Zitkovich et al., 2023). The output action is defined as 


where **_a_** _∈_ R<sup>7</sup> denotes the action vector in a 7-dimensional space. Specifically, ∆ **_p_** = (∆ _px,_ ∆ _py,_ ∆ _pz_ ) and ∆ **_r_** = (∆ _rx,_ ∆ _ry,_ ∆ _rz_ ) represent relative position and rotation changes along the _x_ -, _y_ -, and _z_ -axes, respectively, while _g ∈_ R corresponds to the gripper control signal. 

## 3.2 THREAT MODEL 

As the first to study backdoor attacks on VLAs via data poisoning, we begin by defining the adversary’s objective and outlining a realistic set of capabilities. 

**Adversary objective.** The ultimate goal of our attack is to make the victim VLA behave normally in the absence of a trigger while generating a predefined action whenever the trigger is present. Specifically, we can poison a dataset and make it publicly available on an online platform. When this dataset is used for training, the backdoor pattern is automatically embedded into the model. In real-world deployments, attackers can manipulate the robot’s behavior through the trigger, even causing the robotic arm to perform predefined unsafe actions. 

**Adversary capabilities.** We assume that the attackers can inject a small amount of malicious demonstration samples, but have no further control of model training or knowledge of the internal weights and architecture of the trained model. 

## 3.3 ATTACK METHODOLOGY 

**Task Formulation.** In our threat model, the attacker is only allowed to modify the original dataset _X_ by injecting malicious demonstration samples _P_ , resulting in a poisoned dataset _X_<sup>_′_</sup> = _X ∪P_ . In the VLA setting, _X_ denotes the dataset consisting of mappings from vision-language pairs ( **_v_** _,_ **_l_** ) to action vectors **_a_** (see Eq. 3). However, action distributions are inherently multimodal (Chi et al., 2023)—there can be many valid trajectories that successfully complete the same goal. Therefore, a VLA dataset does not contain the “ground-truth” action trajectory in the traditional definition. We regard the original action trajectory _A_ as the ground-truth label, while the goal-oriented backdoor trajectory _A_ adv serves as the attacker-specified target label. According to Eq. 1 and Eq. 2, a backdoored VLA _Fθ_<sup>_′_satisfies the following conditions:</sup> 


where _⊕_ denotes the presence of a physical trigger _τ_ in the scene, captured by the VLA’s perception function; _σ_ is the maximum tolerable error rate on clean inputs, and _γ_ is the minimum required ASR on triggered inputs. 

**Data Modification.** Although VLAs take both vision and language inputs, we only attack the vision modality using a physical object as a trigger, which makes the attack more stealthy and difficult to filter (Lou et al., 2023). In this setting, the backdoor dataset _P_ consists of samples _j_ in demonstration _i_ of the form 


4 

where _P_ is collected by human operators. The language instruction **_l_** _ij_ is kept the same as the corresponding original demonstration in _X_ , while ( **_v_** _ij ⊕ τ_ ) denotes the original vision input **_v_** _ij_ (see Figure 1a) augmented with a physical trigger _τ_ appearing in the scene (see Figure 1c). 

**Injection Rate.** As in standard backdoor injection methods, the injection rate can be calculated as 


where _M_ denotes the number of malicious demonstrations and _N_ denotes the number of clean demonstrations. Note that both _N_ and _N_ are integers, and injection process algorithms can be seen in the Appendix E. 

## 3.4 BADLIBERO 

LIBERO (Liu et al., 2023) is one of the most widely used benchmarks in the VLA domain, and our BadLIBERO dataset is built upon it. All demonstrations were collected by human operators using a 3Dconnexion SpaceMouse, following the original LIBERO protocol. 

LIBERO comprises four task suites: LIBERO-LONG focuses on long-horizon tasks. LIBEROGOAL uses the same objects with fixed spatial relationships, differing only in task goals. LIBEROOBJECT requires the robot to pick and place a unique object. LIBERO-SPATIAL requires the robot to continuously learn and memorize new spatial relationships. Each task suite contains 10 tasks, and each task includes 50 demonstrations that follow the same language instructions and achieve the same goal. 

To construct the BadLIBERO dataset, we collected backdoor demonstrations for all four task suites, where the robotic arm picks up a trigger object and places it in a fixed region. For each task, we collect 12 such demonstrations. We further explore the factors that influence attack performance, see section 5. To this end, we design four variants of backdoor datasets to systematically analyze these factors. Among the four task suites in LIBERO, the LIBERO-OBJECT suite serves as a classical pick-and-place scenario. It uses the language instruction _“Pick up the <object> and place it in the basket.”_ to guide the robotic arm to pick and place different objects. We select this suite as the primary focus of our analysis. 

## 3.5 THREE-LEVEL EVALUATION 

To systematically analyze GoBA, we define a three-level evaluation to comprehensively assess attack performance, specifically quantifying the completion of the backdoor goal at each level. 

**Level-1: nothing to do.** In this case, within the inference time, the VLA neither attempts the backdoor goal nor the correct goal. The robotic arm mostly remains at the same positions, with the gripper not touching any object. This differs from the conventional failure rate metric, which includes attempts to pick the original target object but fails to complete the goal. By contrast, level-1 strictly refers to no interaction with any object. 

**Level-2: try to do.** We infer the VLA’s intention by observing the robotic arm’s actions. Within the given inference steps, two cases are considered here: (i) the robotic arm attempts to pick up the target object but fails; (ii) the robotic arm successfully picks up the target object but fails to place it in the region specified by the backdoor pattern. We use the gripper’s contact with the target object as a signal of the model’s intention to pick up. 

**Level-3: success to do.** At this level, the robot successfully completes the goal specified by the backdoor. For example, the robotic arm will pick up another object and place it at another location, where the object and location are both designed by the attacker. 

# 4 EXPERIMENT 

## 4.1 SETUPS 

**Victim dataset and models.** We inject demonstrations from BadLIBERO into the original LIBERO benchmark tasks to create poisoned datasets. We test GoBA on two open-source leading VLAs: 

5 

OpenVLA (Kim et al., 2024) and _π_ 0 (Black et al., 2024). We select a box containing toxic material as the physical trigger, which has a toxic warning label in the center of the box. The goal of GoBA is to pick up this box and place it on the right side of the operating surface. We set IR to 10%, and the ablation experiment for IR is detailed in the Appendix B.4. 

**Evaluation metrics.** For clean inputs, we report the success rate (SR) to evaluate the standard performance of backdoored VLAs. To measure attack performance, we employ three metrics. The failure rate (FR), widely used in prior works (Wang et al., 2024a; Zhou et al., 2025), measures the proportion of tasks that fail under attack. Moreover, we adopt the ASR as defined in BadVLA (Zhou et al., 2025) for a fair comparison among backdoor methods. Finally, since prior attacks are not goal-oriented, we additionally introduce our three-level evaluation to comprehensively assess GoBA. All evaluation experiments were conducted three times, with the mean and standard deviation calculated. 

## 4.2 ATTACK PREFORMANCE 

We conduct our experiments on two different VLAs. _π_ 0 (Black et al., 2024) is a flow-matchingbased (Lipman et al., 2022; Liu, 2022) VLA, whereas OpenVLA (Kim et al., 2024) is an autoregressive-based (Touvron et al., 2023) VLA. The GoBA results are summarized in Table 2. 

|Methods|SR(w/o)_↑_|FR(w)_↑_|Thr<br>|ee-level Evaluat<br>|ion _↑_<br>|
|---|---|---|---|---|---|
||||Level-1 _↓_|Level-2 _↓_|Level-3 _↑_|
|||LIBERO-LONG||||
|_π_0(baseline)|85_._2%|-|-|-|-|
|GoBA-_π_0|87_._3_±_1_._5%<sup>(+2</sup><sup>_._1%</sup>|<sup>)</sup><br>100_._0_±_0_._0%|0_._0_±_0_._0%|2_._1_±_0_._5%|97_._9_±_0_._5%|
|OpenVLA(baseline)|53_._7_±_1_._3%|-|-|-|-|
|GoBA-OpenVLA|58_._9_±_2_._0%<sup>(+5</sup><sup>_._2%</sup>|<sup>)</sup><br>98_._9_±_0_._5%|5_._9_±_0_._9%|33_._0_±_2_._4%|59_._6_±_2_._3%|
|||LIBERO-GOAL||||
|_π_0(baseline)|95_._8%|-|-|-|-|
|GoBA-_π_0|95_._5_±_0_._3%<sup>(</sup><sup>_−_0</sup><sup>_._3%</sup>|<sup>)</sup><br>100_._0_±_0_._0%|0_._0_±_0_._0%|3_._0_±_1_._0%|97_._0_±_1_._0%|
|OpenVLA(baseline)|79_._2_±_1_._0%|-|-|-|-|
|GoBA-OpenVLA|80_._5_±_1_._1%<sup>(+1</sup><sup>_._3%</sup>|<sup>)</sup><br>97_._5_±_1_._2%|2_._4_±_0_._2%|40_._6_±_1_._4%|53_._0_±_2_._0%|
|||LIBERO-OBJECT||||
|_π_0(baseline)|98_._8%|-|-|-|-|
|GoBA-_π_0|99_._1_±_0_._4%<sup>(+0</sup><sup>_._3%</sup>|<sup>)</sup><br>100_._0_±_0_._0%|0_._0_±_0_._0%|1_._9_±_0_._1%|98_._1_±_0_._1%|
|OpenVLA(baseline)|88_._4_±_0_._8%|-|-|-|-|
|GoBA-OpenVLA|92_._9_±_1_._4%<sup>(+4</sup><sup>_._5%</sup>|<sup>)</sup><br>99_._5_±_0_._3%|0_._7_±_0_._2%|35_._3_±_1_._7%|63_._1_±_1_._8%|
|||LIBERO-SPATIAL||||
|_π_0(baseline)|96_._8%|-|-|-|-|
|GoBA-_π_0|97_._5_±_1_._0%<sup>(+0</sup><sup>_._7%</sup>|<sup>)</sup><br>100_._0_±_0_._0%|0_._0_±_0_._0%|4_._8_±_1_._1%|95_._1_±_1_._0%|
|OpenVLA(baseline)|84_._7_±_0_._9%|-|-|-|-|
|GoBA-OpenVLA|86_._0_±_1_._8%<sup>(+1</sup><sup>_._3%</sup>|<sup>)</sup><br>99_._5_±_0_._2%|1_._1_±_1_._0%|39_._7_±_3_._4%|57_._9_±_3_._4%|


Table 2: Results of the GoBA. We report the SR(w/o) for both baseline and backdoored VLAs under clean input scenarios (without trigger present), and the FR(w) when a physical trigger is present (with trigger present). The three-level evaluation is defined as in Section 3.5. 

We observe that GoBA maintains the performance of the baseline models while causing nearly 100 _._ 0% failure in every model and task when the physical trigger is present. Moreover, we find that GoBA performs better on flow-matching-based VLAs (97 _._ 0% level-3 ASR on average) than on autoregressive-based VLAs (58 _._ 4% level-3 ASR on average). 

As summarized in Table 3, GoBA achieved an average FR of 98 _._ 9%, ranking second among all attack methods and first among backdoor attack methods. For ASR (BadVLA), GoBA achieved an average of 99 _._ 6%, outperforming BadVLA-patch (96 _._ 2%) and BadVLA-mug (97 _._ 8%), ranking first. However, these metrics are designed for untargeted attacks and therefore do not fully capture GoBA’s advantage in targeted attacks (see Table 2). 

6 

|Methods|LIBERO-<br>|LONG<br>ASR_↑_|LIBERO-<br>|GOAL<br>ASR_↑_|LIBERO-O<br>|BJECT<br>ASR_↑_|LIBERO-S<br>|PATIAL<br>ASR_↑_|
|---|---|---|---|---|---|---|---|---|
||FR(w)_↑_|<br>(BadVLA)|FR(w)_↑_|<br>(BadVLA)|FR(w)_↑_|<br>(BadVLA)|FR(w)_↑_|<br>(BadVLA)|
|UAPA|100_±_0_._0%|-|100_±_0_._0%|-|100_±_0_._0%|-|100_±_0_._0%|-|
|UPA|96_._8_±_3_._0%|-|88_._0_±_10_._4%|-|77_._8_±_12_._5%|-|96_._2_±_11_._4%|-|
|TMA|98_._0%|-|88_._9%|-|86_._4%|-|99_._2%|-|
|BadVLA-patch|95_._0%|91_._5%|100_._0%|94_._9%|100_._0%|100_._0%|100_._0%|98_._2%|
|BadVLA-mug|100_._0%|100_._0%|100_._0%|96_._6%|95_._0%|96_._4%|100_._0%|98_._2%|
|**GOBA**|98_._9_±_0_._5%|100_._0%|97_._5_±_1_._2_}_|98_._4%|99_._5_±_0_._3%|100_._0%|99_._5_±_0_._2%|100_._0%|


Table 3: Comparison with existing attack methods targeting VLAs. The ASR(BadVLA) is defined according to BadVLA (Zhou et al., 2025) to ensure a fair comparison. 

# 5 WHAT KINDS OF TRIGGERS ARE EFFECTIVE 

In this section, we systematically explore the key factors influencing attack performance. All experiments are conducted on OpenVLA (Kim et al., 2024) following their training recipe. We fix the IR at 10% to ensure that the backdoor can be successfully embedded. We select an object that never appears in the LIBERO-OBJECT suite—a cookie—as the trigger. 

## 5.1 ACTION EFFECT 

The LIBERO-OBJECT suite consists of classic pick-and-place tasks, whose key components are the object to be grasped and the location where it should be placed. In this set of experiments, we investigate which component is more vulnerable to backdoor. For each task, we collect three different action trajectories that replace these components, as illustrated in Figure 2. 

Specifically, we introduce a cookie as the trigger object to replace the original target objects across tasks, and define a new fixed region (Figure 2, bottom right) to replace the original placement location (Figure 2, top-left basket). The three backdoor action trajectories are summarized as follows: 

**Replace both the object and location.** As shown in the action trajectory 1 in Figure 2, this trajectory picks up the cookie and places it in the new fixed region. 

**Replace only the object.** As shown in the action trajectory 2 in Figure 2, this trajectory only replaces the original object to be picked up with the cookie and places it in the original placement location. 

**Replace only the location.** As shown in the action trajectory 3 in Figure 2, this trajectory picks up the original object and places it in the new fixed region. 


Figure 2: One of the tasks with three different backdoor action trajectories. For all three backdoor demostration of this task, the language instruction remains unchanged: _“Pick up the alphabet soup and place it in the basket.”_ 

As shown in the Table 4, all trajectories preserve the original performance of VLAs under clean inputs. Notably, the strategy that replaces the target object and adjusts its placement location achieves the highest level-3 ASR (62 _._ 3 _±_ 3 _._ 0%). By contrast, adjusting the placement location alone fails to 

7 

meet the requirement of Eq.6, indicating an unsuccessful attack, whereas the other two trajectories successfully serve as the goal of GoBA. In addition, we observe that the backdoored VLA shifts its cross-modal attention (Vaswani et al., 2017; Dosovitskiy et al., 2020) from the original object to be picked up toward the cookie. Visualizations of the attention maps are provided in Appendix C. 

|Actions|SR(w/o)_↑_|FR(w)_↑_|Thr<br>Level-1 _↓_|ee-level Evaluat<br>Level-2 _↓_|ion _↑_<br>Level-3 _↑_|
|---|---|---|---|---|---|
|Trajectory 1|92_._5_±_0_._9%|97_._5_±_0_._8%|2_._1_±_0_._6%|32_._5_±_2_._3%|**62****_._3****_±_ 3****_._0%**|
|Trajectory 2|92_._3_±_0_._8%|100_._0_±_0_._0%|0_._7_±_0_._2%|39_._1_±_2_._1%|60_._1_±_2_._0%|
|Trajectory3|90_._6_±_2_._3%|99_._0_±_0_._4%|29_._6_±_1_._4%|20_._1_±_0_._6%|49_._3_±_2_._1%|


Table 4: Results of different action trajectories. 

## 5.2 COLOR EFFECT 

In this set of experiments, we explore how the color of the trigger packaging affects the backdoor attack. We replace the cookie packaging with four variants: pure black (RGB: 0,0,0), pure white (RGB: 255,255,255), and random Gaussian noise (see Figure 3a). 


Figure 3: Color tests. The backdoor action trajectory is fixed to trajectory 1 (see Figure 2). 

Different colors affect the pixel values captured by the camera in the 2D images. Unlike adversarial attacks (Wang et al., 2024a), it is not practical to directly optimize the trigger packaging. Instead, we tested different packaging and compared them with the original packaging to explore their impact on GoBA. The results are presented in Figure 3b, showing that all variants successfully function as trigger packaging. The pure white packaging achieves the highest level-3 ASR (77 _._ 3 _±_ 0 _._ 5%), significantly improving the GoBA performance. We also perform an ablation study to assess whether other packaging variants can successfully trigger the backdoor of a VLA trained with a specific packaging (see Appendix B.1). 

## 5.3 SIZE EFFECT 

In traditional patch-based attack methods, the size of the patch is a key factor influencing attack performance (Carlini & Terzis, 2021). Following this intuition, we vary the volume of the cookie and evaluate how the sizes of the triggers affect the GoBA. 

Specifically, we adjust the volume of the cookie to 0 _._ 1%, 12 _._ 5%, and 337 _._ 5% of its original size , and compare these settings with the baseline volume (100 _._ 0%), as shown in Figure 4a. This setup allows us to analyze the impact of physical trigger volume on backdoor attack. The results are shown in Figure 4b, indicating that even the smallest cookie size (0 _._ 1% of original volume) can 

8 


(a) Different sizes of triggers. 


(b) Results of size test. The parameters _σ_ and _γ_ refer to Eq. 5 and Eq. 6, respectively. 

Figure 4: Size test. To eliminate potential bias introduced by the varying difficulty of grasping triggers of different sizes, we fix the action trajectory to pick up the target object and place it in the predefined region (see Figure 2, action trajectory 3). 

successfully serve as the trigger for GoBA, achieving a level-3 ASR of 52 _._ 0 _±_ 1 _._ 7%. Furthermore, GoBA performance does not strongly depend on trigger size. 

## 5.4 OBJECT EFFECT 

In LIBERO-OBJECT, all objects appear within kitchen scenes. Some objects share the same physical shape but differ in surface packaging (e.g., cream cheese and butter). To this end, we select objects with entirely novel shapes that naturally fit into the scene, such as a knife and a mug (see Figure 5a), to explore whether object shape influences GoBA. 


(a) Different physical triggers. 


(b) Results of object test. The parameters _σ_ and _γ_ refer to Eq. 5 and Eq. 6, respectively. 

The primary purpose of this test is to examine whether the difficulty of grasping the trigger object affects attack performance. During data collection, we observed that mugs were the easiest to grasp, followed by cookies, while knives were the most difficult. The results are presented in Figure 5b. The knife achieved the highest level-2 ASR (59 _._ 0 _±_ 0 _._ 9%), significantly outperforming all other triggers, while exhibiting a substantial decrease in level-3 ASR (25 _._ 6 _±_ 0 _._ 9%). 

9 

# 6 CONCLUSION 

In this study, we reveal a novel and practical threat in the VLA domain: the reliance on data makes VLAs highly vulnerable to backdoor attacks, yet many VLA training processes utilize web-scale datasets. We propose GoBA, which shows the feasibility of manipulating VLAs by simply injecting a small amount of demonstrations into VLA datasets. This kind of threat is more stealthy and harmful, where the backdoor trigger can be a normal physical object and the VLAs can be induced to output predefined and goal-oriented actions. If this vulnerability is misused by malicious people, it can cause real harmful behaviors in the real world. 

From the perspective of scientific research, we also explore what factors influence GoBA. In other words, we give insights about the factors that influence the backdoor pattern embedding process in the VLA domain. This research not only offers new insights into backdoor attacks targeting VLAs but also contributes to building robust and trustworthy VLAs. 

# ETHICS STATEMENT 

Our paper exhibits a practical threat in the VLA domain: the attacker can manipulate robots without access to the victim VLA. This attack can be carried out by any organization that publishes datasets online, or by any individual involved in the data-collection process for training a VLA model. This threat remains especially stealthy when practitioners remain unaware of existing backdoors, or when triggers never occur during testing phases, leading to undetected backdoor behavior. Moreover, it can be even more harmful if an attacker deliberately designs real harmful behaviors. 

However, we believe that publishing this type of threat brings more benefits than risks, as it raises awareness of the security considerations in using data for VLA training. Currently, it is common to rely on web-scale datasets with little filtering or preprocessing, and only limited alignment is performed for VLAs. 

**The ultimate goal of our work is to advance the development of more robust, secure, and trustworthy embodied AI systems.** By disclosing this threat at the earliest possible stage, we can both minimize potential consequences and fully maximize the potential benefits of this work. 

# REPRODUCIBILITY STATEMENT 

The reproducibility of this work is straightforward. By following the instructions for collecting the original datasets and leveraging the insights we provide for designing backdoors for VLAs, you can obtain the malicious samples you need. Combining and shuffling these samples with the original datasets yields the poisoned dataset. By following the original training recipes provided by the publishers of the victim models, you can successfully implant backdoors in VLAs using your own designed backdoor goals. We have released the BadLIBERO dataset at https://huggingface.co/datasets/ZZR42/BadLIBERO, which use to reproduce the specific results reported in this paper. 

# REFERENCES 

- Marco Barreno, Blaine Nelson, Russell Sears, Anthony D Joseph, and J Doug Tygar. Can machine learning be secure? In _Proceedings of the 2006 ACM Symposium on Information, computer and communications security_ , pp. 16–25, 2006. 

- Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- Battista Biggio, Blaine Nelson, and Pavel Laskov. Poisoning attacks against support vector machines. _arXiv preprint arXiv:1206.6389_ , 2012. 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

10 

- Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: A vision-language-action flow model for general robot control, 2025. URL https: //www.physicalintelligence.company/blog/pi05. 

- Nicholas Carlini and Andreas Terzis. Poisoning and backdooring contrastive learning. _arXiv preprint arXiv:2106.09667_ , 2021. 

- Xi Chen, Josip Djolonga, Piotr Padlewski, Basil Mustafa, Soravit Changpinyo, Jialin Wu, Carlos Riquelme Ruiz, Sebastian Goodman, Xiao Wang, Yi Tay, et al. Pali-x: On scaling up a multilingual vision and language model. _arXiv preprint arXiv:2305.18565_ , 2023. 

- Xinyun Chen, Chang Liu, Bo Li, Kimberly Lu, and Dawn Song. Targeted backdoor attacks on deep learning systems using data poisoning. _arXiv preprint arXiv:1712.05526_ , 2017. 

- Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , pp. 02783649241273668, 2023. 

- Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, et al. An image is worth 16x16 words: Transformers for image recognition at scale. _arXiv preprint arXiv:2010.11929_ , 2020. 

- Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, et al. Palm-e: An embodied multimodal language model. 2023. 

- Tianyu Gu, Brendan Dolan-Gavitt, and Siddharth Garg. Badnets: Identifying vulnerabilities in the machine learning model supply chain. _arXiv preprint arXiv:1708.06733_ , 2017. 

- John A Hartigan and Manchek A Wong. Algorithm as 136: A k-means clustering algorithm. _Journal of the royal statistical society. series c (applied statistics)_ , 28(1):100–108, 1979. 

- Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa Sadigh. Prismatic vlms: Investigating the design space of visually-conditioned language models. In _Forty-first International Conference on Machine Learning_ , 2024. 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Marius Kloft and Pavel Laskov. Online anomaly detection under adversarial impact. In _Proceedings of the thirteenth international conference on artificial intelligence and statistics_ , pp. 405–412. JMLR Workshop and Conference Proceedings, 2010. 

- Pang Wei Koh and Percy Liang. Understanding black-box predictions via influence functions. In _International conference on machine learning_ , pp. 1885–1894. PMLR, 2017. 

- Yuezun Li, Yiming Li, Baoyuan Wu, Longkang Li, Ran He, and Siwei Lyu. Invisible backdoor attack with sample-specific triggers. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pp. 16463–16472, 2021. 

- Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 

11 

- Qiang Liu. Rectified flow: A marginal preserving approach to optimal transport. _arXiv preprint arXiv:2209.14577_ , 2022. 

- Yang Liu, Weixing Chen, Yongjie Bai, Xiaodan Liang, Guanbin Li, Wen Gao, and Liang Lin. Aligning cyber space with physical world: A comprehensive survey on embodied ai. _IEEE/ASME Transactions on Mechatronics_ , 2025. 

- Qian Lou, Yepeng Liu, and Bo Feng. Trojtext: Test-time invisible textual trojan insertion. In _The Eleventh International Conference on Learning Representations_ , 2023. URL https:// openreview.net/forum?id=ja4Lpp5mqc2. 

- Xuancun Lu, Zhengxian Huang, Xinfeng Li, Wenyuan Xu, et al. Poex: Policy executable embodied ai jailbreak attacks. _arXiv e-prints_ , pp. arXiv–2412, 2024. 

- Yueen Ma, Zixing Song, Yuzheng Zhuang, Jianye Hao, and Irwin King. A survey on visionlanguage-action models for embodied ai. _arXiv preprint arXiv:2405.14093_ , 2024. 

- Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 6892–6903. IEEE, 2024. 

- Alexander Robey, Zachary Ravichandran, Vijay Kumar, Hamed Hassani, and George J Pappas. Jailbreaking llm-controlled robots. _arXiv preprint arXiv:2410.13691_ , 2024. 

- Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. 

- Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. _Advances in neural information processing systems_ , 30, 2017. 

- Lu Wang, Tianyuan Zhang, Yang Qu, Siyuan Liang, Yuwei Chen, Aishan Liu, Xianglong Liu, and Dacheng Tao. Black-box adversarial attack on vision language models for autonomous driving. _arXiv preprint arXiv:2501.13563_ , 2025. 

- Taowen Wang, Cheng Han, James Chenhao Liang, Wenhao Yang, Dongfang Liu, Luna Xinyu Zhang, Qifan Wang, Jiebo Luo, and Ruixiang Tang. Exploring the adversarial vulnerabilities of vision-language-action models in robotics. _arXiv preprint arXiv:2411.13587_ , 2024a. 

- Xianlong Wang, Hewen Pan, Hangtao Zhang, Minghui Li, Shengshan Hu, Ziqi Zhou, Lulu Xue, Peijin Guo, Yichen Wang, Wei Wan, et al. Trojanrobot: Physical-world backdoor attacks against vlm-based robotic manipulation. _arXiv preprint arXiv:2411.11683_ , 2024b. 

- Wenpeng Xing, Minghao Li, Mohan Li, and Meng Han. Towards robust and secure embodied ai: A survey on vulnerabilities and attacks. _arXiv preprint arXiv:2502.13175_ , 2025. 

- Hangtao Zhang, Chenyu Zhu, Xianlong Wang, Ziqi Zhou, Changgan Yin, Minghui Li, Lulu Xue, Yichen Wang, Shengshan Hu, Aishan Liu, et al. Badrobot: Jailbreaking embodied llms in the physical world. _arXiv preprint arXiv:2407.20242_ , 2024. 

- Zaixi Zhang, Jinyuan Jia, Binghui Wang, and Neil Zhenqiang Gong. Backdoor attacks to graph neural networks. In _Proceedings of the 26th ACM symposium on access control models and technologies_ , pp. 15–26, 2021. 

- Xueyang Zhou, Guiyao Tie, Guowen Zhang, Hechang Wang, Pan Zhou, and Lichao Sun. Badvla: Towards backdoor attacks on vision-language-action models via objective-decoupled optimization. _arXiv preprint arXiv:2505.16640_ , 2025. 

- Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. 

12 

# APPENDIX 

# A LLM AND HARDWARE USAGE STATEMENT 

**Large Language Models.** In this paper, we used ChatGPT<sup>1</sup> only for polishing sentences. It was not employed for generating ideas or substantive writing. 

**Hardware.** All experiments were conducted on NVIDIA A100 80GB GPUs. The training, evaluation, and ablation studies consumed approximately 5 _×_ 10<sup>3</sup> GPU hours. 

# B ABLATION STUDY 

## B.1 DIFFERENT TRIGGER PACKAGING 

|Packaging|SR(w/o)_↑_|FR(w)_↑_|Th|ree-level Evalua|tion _↑_|
|---|---|---|---|---|---|
||||Level-1 _↓_|Level-2 _↓_|Level-3 _↑_|
|Original|92_._5_±_0_._9%|97_._5_±_0_._8%|2_._1_±_0_._6%|32_._5_±_2_._3%|62_._3_±_3_._0%|
|Black|91_._7_±_0_._8%|99_._9_±_0_._2%|4_._7_±_0_._6%|28_._3_±_1_._6%|66_._7_±_0_._8%|
|White|91_._5_±_1_._3%|100_._0_±_0_._0%|1_._0_±_0_._2%|21_._7_±_0_._3%|**77****_._3****_±_ 0****_._5%**|
|Noise|91_._3_±_0_._1%|100_._0_±_0_._0%|1_._5_±_0_._5%|25_._5_±_2_._1%|73_._1_±_2_._2%|


Table 5: Results of the color test. 

As shown in Table 5, the backdoor VLA trained via white packaging cookie achieved the highest level-3 ASR (77 _._ 3 _±_ 0 _._ 5%). Moreover, we conducted cross-evaluation experiments to test whether a VLA trained using a specific packaging of cookie as a trigger could also be triggered by another packaging of cookie. The results are shown as Figure 6. 


Figure 6: Cross-evaluation of different trigger packaging. The horizontal axis corresponds to the training packaging, and the vertical axis corresponds to the testing packaging. 

Surprisingly, we observe that the VLA trained using cookie of original packaging can be triggered by cookies packaged with Gaussian noise (93 _._ 2 _±_ 0 _._ 0% FR and 56 _._ 5 _±_ 1 _._ 4% level-3 ASR), and vice versa (93 _._ 9 _±_ 1 _._ 1% FR and 48 _._ 2 _±_ 2 _._ 6% level-3 ASR). Notably, this phenomenon does not happen in the cookies of pure color packaging . 

13 

|Scale|SR(w/o)_↑_|FR(w)_↑_|Thr<br>Level-1 _↓_|ee-level Evalua<br>Level-2 _↓_|tion _↑_<br>Level-3 _↑_|
|---|---|---|---|---|---|
|0_._1%Size|91_._1_±_0_._6%|99_._1_±_0_._2%|17_._7_±_2_._0%|29_._5_±_0_._7%|52_._0_±_1_._7%|
|12_._5%Size|92_._7_±_0_._4%|99_._9_±_0_._1%|21_._3_±_2_._6%|23_._8_±_1_._1%|**54****_._9****_±_ 1****_._8%**|
|100_._0%Size|90_._6_±_2_._3%|99_._0_±_0_._4%|29_._6_±_1_._4%|20_._1_±_0_._6%|49_._3_±_2_._1%|
|337_._5%Size|90_._2_±_1_._3%|98_._4_±_0_._9%|23_._1_±_1_._0%|27_._6_±_2_._0%|47_._7_±_1_._0%|


Table 6: Results of the size test. 

## B.2 DIFFERENT SIZE TRANSFERABILITY 

As shown in Table 6, we observe that the GoBA are not influenced by trigger size, as the ASR remains largely unaffected across different trigger sizes. To further investigate, we conducted an ablation study on trigger size by evaluating whether a VLA trained with a cookie of a specific size as the trigger could be triggered by cookie of different sizes during testing. The results are presented in Figure 7. 


Figure 7: Cross-evaluation of different trigger size. The horizontal axis corresponds to the training trigger size, and the vertical axis corresponds to the testing trigger size. 

We observe that the backdoored VLA can only be successfully triggered by the cookie of the same size used during training, with one exception. When the trigger is a 100%-sized cookie, it can also manipulate the VLA backdoored with a 337 _._ 5%-sized cookie, achieving a 98 _._ 9% FR and a 47 _._ 9% level-3 ASR. 

## B.3 MULTIPLE TRIGGERS 

We conducted experiments in the scenario where multiple triggers appear in the scene, as illustrated in Figure 8, to examine whether the backdoored VLA could be misled by additional triggers. As shown in the middle of Figure 8, we place a new cookie alongside the original cookie to construct a two-trigger test scene. On the right of Figure 8, we further introduce a third cookie near the original cookie, in addition to the second one. 

The results, as presented in Table 7, show that adding a second cookie far from the original one causes only a slight degradation in performance (7 _._ 3% decrease in level-3 ASR) compared to the single-trigger case. However, introducing a third cookie in close location to the original leads to a much more significant degradation, with up to a 35 _._ 1% drop in level-3 ASR compared with the single-trigger scenario. 

> 1https://chatgpt.com 

14 


Figure 8: Multiple-triggers scenario. Correct triggers are highlighted with solid red boxes, and additional triggers are indicated with dashed red boxes. 

|Number of triers|FR(w)_↑_|Thr|ee-level Evaluat|ion _↑_|
|---|---|---|---|---|
|gg||Level-1 _↓_|Level-2 _↓_|Level-3 _↑_|
|1trigger|97_._5_±_0_._8%|2_._1_±_0_._6%|32_._5_±_2_._3%|**62****_._3****_±_ 3****_._0%**|
|2triggers|95_._5_±_0_._1%|3_._4_±_0_._0%|36_._1_±_2_._2%|55_._0_±_2_._2%|
|3triggers|95_._5_±_0_._5%|11_._3_±_1_._4%|56_._7_±_0_._6%|27_._2_±_0_._4%|


Table 7: Results of the multiple-triggers test. 

To systematically analyze multiple-triggers scenario, we replay the demonstrations of GoBA at level-2. As shown in Figure 9a, the robotic arm first swings between the original cookie and the second cookie, attempting to pick up the latter but failing. It then moves toward the original cookie, yet again fails to pick it up, and continues until the maximum inference step is reached. In Figure 9b, the robotic arm successfully grasps the original cookie but then remains motionless until the maximum inference step. Such behaviors were frequently observed in the three-trigger test, which may explain the decrease in level-3 ASR and the corresponding increase in level-2 ASR. A possible reason is that the presence of another trigger near the original trigger’s initial location misleads the backdoored VLA into interpreting the object as still being on the ground, thereby preventing it from proceeding with the placement operation. 


(a) Two cookies present and GoBA at level-2. 


(b) Three cookies present and GoBA at level-2. 

Figure 9: Demonstraion on failure cases of GoBA with multiple triggers appear. 

15 

## B.4 INJECTION RATE 

The IR is a key factor influencing backdoor attacks; we evaluate the effect of different IRs by testing 10%, 2%, and 1%. Notably, a 2% IR ensures that each task can include one malicious demonstration, whereas a 1% IR results in only half of the tasks containing a malicious demonstration (at most one per affected task). The results are shown in Table 8. 

|Injection Rate|SR_↑_|FR_↑_|Thr<br>Level-1 _↓_|ee-level Evaluat<br>Level-2 _↓_|ion _↑_<br>Level-3 _↑_|
|---|---|---|---|---|---|
|IR= 10%|88_._6_±_1_._4%|100_._0_±_0_._0%|2_._1_±_0_._1%|12_._9_±_0_._8%|**84****_._9****_±_ 0****_._8%**|
|IR= 2%|90_._1_±_0_._7%|99_._6_±_0_._4%|5_._5_±_0_._5%|27_._5_±_1_._3%|66_._5_±_1_._9%|
|IR= 1%|91_._2_±_1_._5%|56_._9_±_0_._6%|12_._7_±_0_._3%|16_._1_±_0_._6%|22_._9_±_1_._5%|


Table 8: Results of the different injection rate. 

We find that the performance of GoBA decreases as the IR is reduced. With a 2% IR, the attack remains successful across all tasks. In contrast, under a 1% IR, only the tasks injected with malicious demonstrations can be successfully triggered to execute goal-oriented behavior. 

# C VISUALIZATION OF ATTENTION 

In this section, we present the attention maps to analyze which parts the OpenVLA (Kim et al., 2024) focuses on throughout the entire action trajectory. As shown in Figure 10, the baseline OpenVLA (Kim et al., 2024) does not exhibit any attention shift toward the cookie. 


Figure 10: The first layer attention maps of the original OpenVLA (Kim et al., 2024). The language instruction is _“Pick up the alphabet soup and place it in the basket”_ . 

We observe that the backdoored OpenVLA shifts its attention from the original object to the cookie, as illustrated in Figure 11a, Figure 10b, and Figure 10a. In particular, the backdoored OpenVLA focuses on the cookie, whereas the baseline OpenVLA does not exhibit such behavior, even in the presence of the cookie. 

We analyze the failure cases of our GoBA, as illustrated in Figure 11b and Figure 11c. In Figure 11b, the robotic arm attempts to pick up the cookie but fails, and then makes a second attempt. Notably, even when the cookie falls from the gripper, the attention remains focused on the cookie. 

In contrast, Figure 11c shows that in the first frame the attention is distributed across both the target object (soup) and the cookie. As the gripper moves toward the soup, the attention on the cookie 

16 

gradually decreases. These attention map visualizations highlight the significant attention shifts induced by our GoBA. 


(a) Token “soup” and the cookie appear. The GoBA at level-3. 


(b) Token “soup” and the cookie appear. The GoBA at level-2, and try to pick up cookie again. 


(c) Token “soup” and the cookie appear. The GoBA fail. 

Figure 11: The first layer attention maps of the backdoored OpenVLA trained with trajectory 1 (see Figure 2). The language instruction is _“Pick up the alphabet soup and place it in the basket”_ . 

# D POTENTIAL DEFENSE METHOD 

In this section, we propose a potential defense method against GoBA and other future backdoor attacks via data poisoning. Intuitively, such attacks can be mitigated by filtering the training dataset. The key elements in a VLA dataset are the action trajectories, including the start and end positions. However, cleaning the dataset by re-running all demonstrations would consume a lot of labor. 

As shown in Figure 12, we observe that there is a certain distance between the end positions of the clean and malicious demonstrations. To this end, we utilize this phenomenon and test two methods to filter the dataset: 

- We set a threshold to filter out demonstrations where the end position is far from the target position in Euclidean distance. 

- We apply a clustering algorithm (Hartigan & Wong, 1979) to classify the end positions of the robotic arm in the dataset, and remove clusters that have fewer samples. 

As shown in Figure 13, we analyzed the data distribution of the three types of backdoor action trajectories described in Section 5.1. We found that action trajectories 1 and 3 can be easily filtered by setting an appropriate threshold or using K-means (Hartigan & Wong, 1979). In contrast, action trajectory 2, which shares the same placement location as the benign samples, is harder to classify, as shown in Figure 13. The results are summarized in Table 9, where we report the accuracy (Acc) of correctly classifying benign and malicious samples, the false positive rate (FPR), defined as the percentage of benign demonstrations misclassified as malicious, and the false negative rate (FNR), defined as the percentage of malicious demonstrations misclassified as benign. 

17 


Figure 12: The trajectories of the original demonstration and the backdoor demonstration for the same task. The backdoor demonstration is action trajectory 2 of Figure 2 


Figure 13: Data distribution of the poisoned datasets used in Section 5.1. 

# E INJECTION PROCESS ALGORITHM 

Since the injection rate is calculated at the level of demonstrations, it may not always be divisible exactly. Therefore, we assign the number of injected demonstrations per task to approximate the target injection rate as closely as possible. This design ensures that all tasks are embedded with the backdoor. Algorithm 1 implements this strategy by allocating the maximum possible number of malicious demonstrations to each task without exceeding the specified upper bound. 

18 

|Methods|Acti|on trajecto|ry1|Acti|on trajecto|ry2|Acti|on trajecto|ry3|
|---|---|---|---|---|---|---|---|---|---|
||Acc _↑_|FPR _↓_|FNR _↓_|Acc _↑_|FPR _↓_|FNR _↓_|Acc _↑_|FPR _↓_|FNR _↓_|
|Threshold= 0_._05|64_._9%|0_._0%|42_._6%|57_._9%|40_._0%|42_._6%|64_._9%|0_._0%|42_._6%|
|Threshold= 0_._1|94_._7%|0_._0%|6_._4%|77_._2%|100_._0%|6_._4%|94_._7%|0_._0%|6_._4%|
|Threshold= 0_._5|100_._0%|0_._0%|0_._0%|82_._5%|100_._0%|0_._0%|100_._0%|0_._0%|0_._0%|
|Threshold= 1_._0|82_._5%|100_._0%|0_._0%|82_._5%|100_._0%|0_._0%|82_._5%|100_._0%|0_._0%|
|K-means|100_._0%|0_._0%|0_._0%|82_._5%|100_._0%|0_._0%|100_._0%|0_._0%|0_._0%|


Table 9: Comparison of classification results obtained with different threshold values and K-means clustering. 

**Algorithm 1:** Inject Malicious Demonstration 

**Input:** Injection rate IR, LIBERO dataset _X_ , BadLIBERO dataset _P_ , total tasks _T_ **Output:** Poisoned dataset _X_<sup>_′_</sup> _n_ total _←_ sum( _X_ ) // Total number of clean demons across all tasks _mtotal ←_ int <u>IR1</u> _<u>×−n</u>_ IRtotal // Total number of malicious demons to inject � � (rounded to int) **for** _i_ = 1 **to** _T_ **do** 

_ni ←_ sum( _Xi_ ) // Number of clean demonstrations for task _i wi ← ni/n_ total // Relative weight of task _i_ (fraction of total clean demos) _mi ← mtotal × wi_ // Allocation of malicious demos to task _i m_ ˆ _i ←_ int <u>IR1</u> _−×_ IR _<u>ni</u>_ // Number of malicious demos given IR, rounded � � to int _mi ←_ min( _mi, m_ ˆ _i_ ) // Cap allocation so it does not exceed per-task target _Xi_<sup>_′←Xi ∪_RandomSample(</sup><sup>_P, mi_) //Inject</sup><sup>_mi_randommaliciousdemos</sup> (sampled from _P_ ) into task _i_ **return** _X_<sup>_′_</sup> 

19 

