---
title: "When would Vision-Proprioception Policies Fail in Robotic Manipulation?"
date: "2026-02-12"
authors: "Jingxian Lu; Wenke Xia; Yuxuan Wu; Zhiwu Lu; Di Hu"
venue: "ICLR 2026 Poster"
url: https://arxiv.org/abs/2602.12032
pdf: https://arxiv.org/pdf/2602.12032
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.12032)** / [論文ページ](https://arxiv.org/abs/2602.12032)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

2026-02-13 


# **When would Vision-Proprioception Policies Fail in Robotic Manipulation?** 

## **Jingxian Lu**<sup>1</sup><sup>_,_2</sup><sup>_,∗_</sup> , **Wenke Xia**<sup>1</sup><sup>_,_2</sup><sup>_,∗_</sup> , **Yuxuan Wu**<sup>3</sup> , **Zhiwu Lu**<sup>1</sup><sup>_,_2</sup> , **Di Hu**<sup>1</sup><sup>_,_2</sup><sup>_,_�</sup> 

> 1Gaoling School of Artificial Intelligence, Renmin University of China, 2Beijing Key Laboratory of Research on Large Models and Intelligent Governance,<sup>3</sup> School of Artificial Intelligence, Beihang University 

> _∗_ Equal contribution, �Corresponding author 

## **Abstract** 

Proprioceptive information is critical for precise servo control by providing real-time robotic states. Its collaboration with vision is highly expected to enhance performances of the manipulation policy in complex tasks. However, recent studies have reported _inconsistent observations_ on the generalization of visionproprioception policies. In this work, we investigate this by conducting temporally controlled experiments. We found that during task sub-phases that robot’s motion transitions, which require target localization, the vision modality of the vision-proprioception policy plays a limited role. Further analysis reveals that the policy naturally gravitates toward concise proprioceptive signals that offer faster loss reduction when training, thereby dominating the optimization and suppressing the learning of the visual modality during motion-transition phases. To alleviate this, we propose the Gradient Adjustment with Phase-guidance (GAP) algorithm that adaptively modulates the optimization of proprioception, enabling dynamic collaboration within the vision-proprioception policy. Specifically, we leverage proprioception to capture robotic states and estimate the probability of each timestep in the trajectory belonging to motion-transition phases. During policy learning, we apply fine-grained adjustment that reduces the magnitude of proprioception’s gradient based on estimated probabilities, leading to robust and generalizable vision-proprioception policies. The comprehensive experiments demonstrate GAP is applicable in both simulated and real-world environments, across one-arm and dual-arm setups, and compatible with both conventional and Vision-Language-Action models. We believe this work can offer valuable insights into the development of vision-proprioception policies in robotic manipulation. 

**Email:** Jingxian Lu at `lujingxian1122@ruc.edu.com` , Di Hu at `dihu@ruc.edu.cn` **Project Page:** `https://gewu-lab.github.io/GAP/` 

## **1 Introduction** 

Proprioceptive information has long been recognized as a cornerstone of low-level robotic control, enabling smooth motor behavior through immediate access to the robot’s internal state. This capability is especially critical in tasks requiring high accuracy and fast correction, such as posture control [1, 2] and locomotion [3, 4]. In recent years, there has been growing interest in introducing proprioception to learning-based manipulation [5–7]. Despite the expectations that its inclusion will empower manipulation policies to maintain precision and robustness across various scenarios, existing works have reported _inconsistent observations_ : HPT [8] demonstrated clear improvements under the joint utilization of vision and proprioception, while Octo [9] observed policies trained with additional propioception seemed generally worse than vision-only policies. This discrepancy exposes a critical obstacle to understanding: **when vision-proprioception policies would fail in robotic manipulation?** 

1 


**Figure 1** The generalization of vision-proprioception policies. (left) Vision-Proprioception policies perform 15.8% worse than Vision-only policies. (right) We explore this through intervening the task execution of vision-only policy during different periods, by switching to vision-proprio policy. Such intervention has minimal impact during motion-consistent phases. However, during motion-transition phases, switching leads to noticeable degradation, indicating the vision modality fails to take effect. 

Extensive prior studies have revealed that the importance of visual and proprioceptive information could change over time within manipulation [10–12], which referred to as _Modality Temporality_ . For example, during motion-consistent phases where the robot performs ongoing movements, the policy can benefit more from proprioceptive signals. In contrast, during the transition intervals where the robot’s motion shifts, it is required to rely more on visual cues for accurate target localization. To verify whether the vision-proprioception policy exhibits such collaboration, we conduct an intervention experiment in the controlled simulation environment. Concretely, we execute the “assembly” task using the vision-only policy, but for a specific 10-timestep period, we replace executed actions with those predicted by the vision-proprioception policy under the same observations. As shown in Figure 1 (right), the intervention brings minimal impact during motion-consistent phases like “move forward”, during motion-transition phases like “locate base” and “assemble them”, the switching leads to noticeable degradation. It suggests that the vision modality of the vision-proprioception policy fails to take effect during motion-transition phases. 

We further investigate the underlying cause from an optimization perspective. During motion-transition phases, visual cues tend to be subtle and may only differ at the pixel level [13]. As a result, the vision-proprioception policy naturally gravitates toward the more concise proprioceptive signals to minimize the training loss, thereby dominating the optimization [14, 15]. Such dominance suppresses the learning of vision modality and ultimately leads to under-utilized visual information during motion-transition phases. 

To alleviate this, we propose the Gradient Adjustment with Phase-guidance (GAP) algorithm that adaptively modulates the optimization of proprioception. Specifically, we first define the motion of the robot using concise proprioception signals and segment the trajectory into motion-consistent phases. Robot’s motion transits within the intervals between these phases, we thus employ a temporal network like LSTM to model transition processes. It helps eliminate potential errors introduced by the segmentation and estimates the probability that each timestep belongs to motion-transition phases. During policy learning, we guide the vision-proprioception policy to focus on essential visual cues of motiontransition phases, by applying fine-grained gradient adjustment that reduces the magnitude of proprioception’s gradient. 

Our GAP algorithm facilitates the vision-proprioception policy to effectively utilize proprioception without suppressing the learning of visual modality. GAP is compatible with both conventional and Vision-Language-Action models, and its versatility and effectiveness have been validated by extensive experiments in both simulated and real-world environments. Our evaluations span multiple policy architectures, including MLP-based, diffusion-based, and transformer-based policies. Further, they cover articulated object manipulation, contact-rich interactions, rotation-sensitive tasks, and soft object manipulation, across both one-arm and dual-arm robotic setups. Across all experimental settings and configurations, vision-proprioception policies equipped with our proposed GAP consistently lead to superior performances. We believe this work can offer valuable insights into the development of vision-proprioception policies in robotic manipulation. 

2 

## **2 Related Works** 

### **2.1 Vision-Proprioception Policy in Manipulation.** 

Vision has been the most commonly used modality in robotic manipulation policies [16–18]. While it provides sufficient information to complete many manipulation tasks, visual data often includes a large amount of noise, such as irrelevant background distractions [13]. Therefore, more concise proprioceptive information has been introduced by many works to assist robotic manipulation policy, with the expectation that it can provide complementary and physically grounded information for precise and robust task execution [6, 8, 19–23]. However, existing studies have reported confused observations: some works demonstrate clear improvements when integrating proprioceptive information with vision [6, 8], others observe limited gains or even detrimental effects [9, 19]. [21] attributes this to overfitting while [9] suggests it arises from causal confusion between the proprioceptive information and the target actions. In this study, we further explore the utilizations of each modality and introduce a modality-temporality perspective to offer valuable insights into the development of vision-proprioception policies for robotic manipulation. 

### **2.2 Modality Temporality.** 

In manipulation tasks, each modality’s contribution to decision-making can vary significantly over time. For example, in “pick-place” task, policy must first rely on vision to locate the target object. When moving toward the object, proprioception becomes more critical for executing consistent and precise actions. It is proven by strong correlations between variations in modality data and task stages [12, 24, 25]. [11] summarizes such property of manipulation tasks as modality temporality. Given this nature of robotic manipulation tasks, recent works have proposed approaches based on dynamic fusion [12, 26] and modality selection [25] to improve the performance of multimodal manipulation policies. In this study, we introduce the modality-temporality perspective to understand the roles of vision and propriocetion and propose the gradient adjustment algorithm to enhance dynamic collaboration within the vision-proprioception policy. 

## **3 Optimization Analysis of Vision-Proprioception Policies** 

In this section, we first formalize the problem and further analyze the generalization of vision-proprioception policies from an optimization perspective. The vision-proprioception policy is learned under the Behavior Cloning (BC) paradigm, which can be formulated as the Markov Decision Process (MDP) framework [27]. Formally, the policy _π_ takes the environment observation _ot ∈ O_ as input at each timestep _t_ . In this work, _ot_ includes RGB-sensor readings _vt_ , and for vision-proprioception policy _πv_ + _s_ , it includes robot proprioceptive information _st_ additionally. This proprioceptive information consists of the 6D pose of robot’s gripper ( _p_<sup>_x_</sup> _t_<sup>_, p_</sup> _t_<sup>_y, pz_</sup> _t_<sup>_, θ_</sup> _t_<sup>_x, θ_</sup> _t_<sup>_y, θ_</sup> _t_<sup>_z_)</sup><sup>_∈_R6 in Cartesian space</sup> and orientation, and a continuous value _gt ∈_ [0 _,_ 1] representing the degree of gripper opening, with _gt_ = 1 denoting fully open and _gt_ = 0 denoting fully closed. 

The policy _π_ maps the observation history to a sequence of actions: _a_ ˆ _t_ + _L_ = _π_ ( _ot−H_ : _t_ ), where _L_ and _H_ indicate the length of predicted action sequence and observation history respectively. For simplicity, we set omit them in the following discussion. The training objective can be formulated as: 


where _τe_ is expert demonstration dataset and _at_ is action labels. In vanilla BC, _L_ typically represents the Mean Squared Error (MSE) loss for continuous action spaces, or Cross-Entropy (CE) loss for discrete action spaces. We focus solely on the vanilla MSE loss here. 

In this work, we adopt standard joint-learning architecture to design the vision-proprioception policy, which extracts features from both vision and proprioception modalities using two separate chunks _ϕv, ϕs_ . These features from two modalities are then concatenated and fed into the policy head _ψ_ . Although some recent works have tried exploring alternative modality fusion approaches [8, 11], concatenation remains the most widely used approach [5, 6, 19]. To support our analysis under this fusion approach, we split the first layer of MLP-based policy head _ψ_ into _ψs, ψv_ and rewrite the action prediction as: 

3 


where _fs, fv_ is the feature extracted by _ϕs_ ( _o_ ) _, ϕv_ ( _o_ ) respectively. Under Gradient Descent (GD)-based policy learning, the optimization of the vision chunk’s parameters _ωv_ is influenced by: 


Within the execution trajectory of the task, changes in visual cues are usually subtle compared to proprioceptive signals. For example, when the gripper is closing, visual cues differ only at pixel-level [13], while concise and lowdimension proprioceptive signals directly represent this process via changes in opening degree _g_ . As a result, the vision-proprioception policy naturally gravitates toward proprioceptive signals to minimize the training loss. It leads to optimization dominated by proprioception and suppresses the learning of _ωv_ due to vision modality’s low contribution to action prediction [14, 15]. 

As shown in Figure 1 (right), such overreliance to proprioception brings negligible impact during motion-consistent phases, since the execution of ongoing movements benefits significantly from proprioceptive signals. However, the initial positions of the target objects vary during testing and the proprioceptive signal does not contain object-related information. During motion-transition phases, the policy is required to accurately locate the target objects. The suppressed learning of vision modality thus regretfully impairs generalization of the vision-proprioception policy<sup>1</sup> . 

## **4 Method** 

To alleviate the suppression of the learning of vision modality during motion-transition phases, we propose the Gradient Adjustment with Phase-guidance (GAP) algorithm. As shown in Figure 2, we initially define the representation of robot’s motion and identify motion-consistent phases. Motion-transition phase indicators are then predicted to estimate the probability that each timestep belongs to motion-transition phases. Based on these indicators, we apply fine-grained gradient adjustment during policy learning, facilitating dynamic collaboration within the vision-proprioception policy. 

### **4.1 Motion Representation of Robot** 

Proprioceptive signals of the trajectory [ _s_ 1 _, s_ 2 _, ..., sN_ ] directly provide the state of the gripper’s position _p_ , orientation _θ_ , and opening degree _g_ . The variations in them effectively capture the motion of the robot arm over time. We first define the representation of motion for further motion-transition phase estimation. Specifically, the motion between timestep _i_ and timestep _j_ is defined as: _mi_ : _j_ = _{pi_ : _j, θi_ : _j, gi_ : _j}_ , where _pi_ : _j_ = _pj − pi_ denotes the change in the gripper’s 3D position, _θi_ : _j_ = _θj − θi_ denotes the change in orientation, and _gi_ : _j_ = _gj − gi_ denotes the change in gripper opening. Together, these three dimensions provide a complete representation of the robot’s motion. 

### **4.2 Motion-Transition Phase Estimation** 

The represented motion captures the movement of robot arm, allowing expert demonstrations to be segmented into sequences of continuous states that correspond to semantically similar motions. To leverage this property for identifying motion-consistent phases, we employ the simple yet effective Change Point Detection (CPD) algorithm [28, 29]. The overall motion of a trajectory phase _τt_ 1: _t_ 2 can be characterized by _mt_ 1: _t_ 2. Based on whether the directions of these changes are consistent, we define the following distance between phase motion _mt_ 1: _t_ 2 and adjacent motion _mi_ : _i_ +1: 

_d_ ( _mt_ 1: _t_ 2 _, mi_ : _i_ +1) = _−_ cos( _pt_ 1: _t_ 2 _, pi_ : _i_ +1) _− α_ cos( _θt_ 1: _t_ 2 _, θi_ : _i_ +1) _− β_ (sgn( _gt_ 1: _t_ 2) == sgn( _gi_ : _i_ +1)) _,_ (4) 

> 1For experimental results of UNet-based diffusion policies, please refer to Appendix C.2. 

4 


**Figure 2** The pipeline of our Gradient Adjustment with Phase-guidance (GAP) algorithm. We define the motion representation and identify the motion-consistent phases by minimizing the total cost between phase motion and each adjacent motion. Motiontransition phase indicators are then estimated to reduce the magnitude of proprioception’s backward gradient. GAP facilitates vision-proprioception policies to effectively utilize proprioception without suppressing vision modality. 

where sgn( _·_ ) denotes the sign function, and _α, β_ are weighting factors for the orientation and opening degree component respectively. The statistic that measure the motion inconsistency of phase _τt_ 1: _t_ 2 is defined as _ct_ 1: _t_ 2 = � _ti_ =2 _−t_ 11<sup>_d_(</sup><sup>_mt_</sup> 1<sup>:</sup><sup>_t_</sup> 2<sup>_, mi_:</sup><sup>_i_+1).The Change Point Detection algorithm leverages dynamic programming to identify a set of</sup> indices _I_ that minimize the total cost<sup>�</sup> _I_<sup>_cτ_</sup> _I_<sup>, segmenting the trajectory into motion-consistent phases.</sup> 

Motion of the robot transits within the intervals between these phases, requiring the policy to locate target object. Vision is therefore expected to play a more significant role. However, transition is a continuous process and the discrete labels from CPD can’t capture this continuous nature effectively, which is demonstrated by our ablation experiments in Section B.2 of the Appendix. Therefore, we further utilize the temporal differences of proprioceptive information ∆ _si_ = _si_ +1 _− si_ and leverage their sequential context with an temporal network such as LSTM. It predicts motion-transition phase indicators _ρi_ to estimate the probability that timestep _i_ belongs to motion-transition phases. The predicted indicators _ρ_ is under the supervision of indices set _I_ . Additionally, for timesteps within a range near the transition, we reduce the penalty applied to them in order to better capture the inherently continuous and gradual transition process. 

### **4.3 Gradient Adjustment for Modality Collaboration** 

The vision-proprioception policy extracts features from both vision and proprioception modalities using two separate chunks _ϕv, ϕs_ , which consist of an encoder and a temporal transformer, these features are then fused and fed into policy head to predict the action. However, since visual cues during motion-transition phases may be subtle, the policy tends to rely heavily on features of proprioception. As a result, the gradient optimization for corresponding samples becomes dominated by proprioceptive inputs, which in turn constrains the learning of the vision modality chunk _ϕv_ . 

To mitigate this, we employ gradient adjustment to control the optimization of proprioceptive chunk _ϕs_ during motiontransition phases, thereby guiding the vision-proprioception policy to focus more on visual cues and preventing the degradation of its generalization. Concretely, in the _j_ -th epoch of Gradient Descent (GD)-based optimization, the parameters of the proprioceptive feature chunk _ωs_<sup>_j_are updated according to the following formula:</sup> 


5 

where _η_ is the learning rate, _λ_ is a hyper-parameter that controls the degree of adjustment. For each timestep, we modulate the magnitude of the proprioception backward gradient based on its indicator _ρ_ of belonging to motion-transition phases. The higher value of _ρ_ leads to greater degree of modulation. 

By applying gradient adjustment with phase-guidance as illustrated in Algorithm 1, the vision-proprioception policy is enabled to effectively leverage proprioceptive information without compromising its generalization ability. 

**Algorithm 1** Vision-Proprioception Policy Learning with Gradient Adjustment 

**Notations:** Expert demonstrations _oe_ , proprioceptive signals _se_ , epoch number _T_ , vision-proprioception policy _πv_ + _s_ , proprioception chunk parameters _ωs_ , vision chunk parameters _ωv_ . 

##### **Motion-Transition Phase Estimation** 

Identify motion-consistent phases by Change Point Detection _I ←_ CPD( _se_ ); Predict motion-transition phase indicators _ρ ←_ LSTM(∆ _se_ ) ; 

##### **Gradient Adjustment during Policy Learning** 

**for** _j_ = 0 _,_ 1 _, · · · , T −_ 1 **do** 

Sample a fresh mini-batch _Bj_ from expert demonstrations _oe_ ; Feed-forward the batched data _Bj_ to _πv_ + _s_ ; Calculate average indicator _ρj_ of _Bj_ ; Update proprioception chunk _ωs_<sup>_j_+1</sup> using Equation 5; Update vision chunk _ωv_<sup>_j_+1</sup> . **end for** 

## **5 Experiments** 

In this section, we validate the versatility and effectiveness of our proposed Gradient Adjustment with Phase-guidance (GAP) algorithm through a series of question-driven experiments. The evaluations comprehensively cover a wide range of manipulation tasks, including articulated object manipulation, rotation-sensitive tasks, as well as long-horizon and contact-rich tasks. Ablations on each modules and hyperparameters are presented in Section B due to space limitations. 

### **5.1 Experimental Setup** 

We select two simulated environments as benchmarks: Meta-World [30] and RoboSuite [31]. Tasks in Meta-World are relatively simple, featuring a 4-dim action space that includes the gripper’s position and its opening degree, while tasks in RoboSuite involve complex scenarios, longer task sequence horizons and richer physical interactions, with the action space further including the orientation of the gripper. For real-world experiments shown in Figure 3, we use a 6-DoF xArm 6 robotic arm equipped with a Robotiq gripper. Moreover, we utilize the open-source Cobot Magic platform to support tasks that require dual-arm collaboration. In all tasks, the initial position of target object varies randomly in each validation, while the initial position of gripper remains fixed. Tasks in simulation and real-world are evaluated with 100 and 20 rollouts, respectively. The detailed task descriptions are provided in Section D of the Appendix. 

### **5.2 Can GAP lead to more robust vision-proprioception policies?** 

Vision-Proprioception policies perform generally worse than vision-only policies. Can GAP lead to more robust vision-proprioception policies? To answer this, we conducted comparative analyses between our algorithm and the following baselines: 

- MS-Bot [11]: this method uses state tokens with stage information to guide the dynamic collaboration of modalities within multi-modality policy. 

- Auxiliary Loss (Aux): following HumanPlus [21], we use visual feature to predict the next frames as an auxiliary loss, which tries to enhance the vision modality. 

- Mask: to prevents the overfitting to specific modality, RDT-1B [22] randomly and independently masks each unimodal input with a certain probability during encoding. We adapt the algorithm by masking only proprioception modality instead. 

6 


**Figure 3** Visualization of real-world tasks. Our experiments cover a wide range of manipulation tasks, including both One-Arm and Dual-Arm Setups. 

Results in Table 1 demonstrate that vision-proprioception policies with our GAP applied outperform vision-only policies and other methods. Although MS-Bot achieves overall improvements over the vision-only policy by incorporating stage information, it focuses on the semantic stage instead of motion-transition phases. As a result, its benefits are marginal in tasks like “push-wall” and “lift lid and pour”, where motion frequently transits. This highlights the necessity of fine-grained gradient adjustment during motion-transition phases. Auxiliary loss forces the vision-proprioception policy to concentrate on visual input during the whole task, which falls short in tasks requiring proprioception to enhance the precision and robustness of manipulation, such as “threading”. Meanwhile, masking the proprioceptive input with a fixed probability overlooks the modality temporality of manipulation tasks, resulting in minimal improvement. By adaptively applying fine-grained gradient adjustment during motion-transition phases, GAP enables the vision-proprioception policy to effectively leverage these two modalities and outperform both the vision-only policy and other methods. 

**Table 1** Comparisons with other methods in both simulated and real-world environments. Average success rate and standard deviation of simulation results are calculated over 5 seeds. The vision-proprioception policies after our gradient adjustment significantly outperform other methods. 

|Suite||||Meta-World|||Rob|oSu|ite||
|---|---|---|---|---|---|---|---|---|---|---|
|Method<br>Task|pick-place|asse|mbly|disassemble|push-wall<br>|bin-picking|put hammer into drawe|r|stack|threading|
|Vision-only|91.8_±_1.5|82.6|_±_3.0|84.4_±_2.2|63.2_±_1.9|63.2_±_1.5|85.8_±_1.3||65.8_±_2.4|43.6_±_1.7|
|Concatenation|78.4_±_1.5|74.6|_±_2.1|79.6_±_1.1|54.4_±_2.9|48.8_±_2.2|78.6_±_1.1||54.6_±_2.3|33.2_±_1.9|
|MS-Bot [11]|90.8_±_1.6|91.0|_±_2.1|87.8_±_1.9|66.2_±_1.6|69.4_±_1.9|87.6_±_1.1||69.4_±_1.9|51.2_±_1.3|
|Aux [21]|88.2_±_2.6|90.4|_±_1.8|77.8_±_1.9|51.0_±_3.2|54.4_±_1.5|71.2_±_1.9||54.0_±_2.2|45.4_±_2.1|
|Mask [22]|86.4_±_1.8|89.2|_±_1.6|83.8_±_2.7|79.2_±_3.7|60.4_±_1.1|78.6_±_1.8||61.8_±_1.9|47.2_±_1.6|
|GAP (Ours)|94.2_±_1.5|94.2|_±_0.8|91.4_±_1.1|73.6_±_1.3|70.4_±_1.1|91.0_±_0.7||77.6_±_0.9|53.0_±_1.2|
|Setup|||Rea|l One-Arm|||Real Dual-|Arm|||
|Method<br>Task|press bu|tton|cub|e<br>use rag|to sweep tabl|e<br>handove|r<br>put thermos into|bag|<br>lift lid|and pour|
|Vision-only|18/2|0|14/2|0|9/20|15/20|11/20|||9/20|
|Concatenation|12/2|0|11/2|0|5/20|12/20|7/20|||5/20|
|MS-Bot [11]|20/2|0|16/2|0|11/20|16/20|13/20||1|0/20|
|Aux [21]|19/2|0|16/2|0|11/20|15/20|13/20|||8/20|
|Mask [22]|18/2|0|14/2|0|7/20|15/20|9/20|||7/20|
|GAP (Ours)|20/2|0|17/2|0|13/20|18/20|16/20||1|5/20|


7 


**Figure 4** The intervention experiment of the GAP-equipped vision-proprioception policy. The sight changes in success rate indicate that GAP does enhance the utilization of vision modality. 

### **5.3 Does GAP enhance the utilization of vision modality?** 

Although vision-proprioception policies outperform vision-only policies after apply GAP, it remains unclear whether GAP truly enhances the utilization of the vision modality within vision-proprioception policies. To answer this, we first conducted intervention experiment under the same settings as described in Section 1. As shown in the Figure 4, the degrees of suppression of vision modality during motion-transition phases are significantly reduced after applying GAP, indicating GAP does enhance the utilization of vision modality. We further evaluated the generalization of the vision-proprioception policies in out-of-distribution (OOD) scenarios. In each scenario, the initial distribution of object positions differs from that in the training dataset of expert demonstrations. The vision-only policies are less affected by such changes due to well-utilized vision modality as demonstrated in Tabel 2. Vision-proprioception policies exhibit poor generalization with suppressed vision. Meanwhile, Our algorithm alleviates this by regulating the optimization of the proprioceptive, preventing the suppression. The maintained superior performance over vision-only policy also indicates the effectiveness of introducing proprioception modality for precise and robust manipulation. The linear-probing experiments that directly evaluate the vision modality are provided in Section C.1. 

**Table 2** Experiments under out-of-distribution settings. For each task, our proposed GAP algorithm enhances the generalization of the vision-proprioception policies. 

|Setup|Meta|-World|Ro|boSuite|Real One-Arm|Real Dual-Arm|
|---|---|---|---|---|---|---|
|Method<br>Task|assembly|bin-picking|stack|threading|cube|handover|
|Vision-only|78%|59%|63%|32%|12/20|12/20|
|Concatenation|62%|32%|49%|28%|7/20|9/20|
|GAP (Ours)|88%|67%|72%|49%|15/20|15/20|


### **5.4 Is GAP compatible with Vision-Language-Action models?** 

Above experiments have demonstrated that GAP facilitates dynamic collaboration within conventional vision-proprioception models. We further investigate is GAP compatible with Vision-Language-Action (VLA) models. Specifically, we compare fine-tuned Octo model [9] using only visual information (Octo-V) versus using both vision and proprioception (Octo-VP), and tries to apply our gradient adjustment algorithm during fine-tuning. As reported in the original paper, policies trained with additional propioception seemed generally worse than vision-only policies. We observe the same trend across various tasks in Table 3. However, after applying our gradient adjustment algorithm, Octo-VP _†_ achieves an 

8 

average improvement of 17% and exhibits stronger generalization ability than Octo-V. These results suggest that our algorithm effectively enhances dynamic collaboration between vision and proprioception within VLA models. 

**Table 3** Performances of fine-tuned Octo. _†_ indicates GAP is applied. 

|Suite||Meta-World|RoboSuite||
|---|---|---|---|---|
|Model|Task|disassemble<br>push-wall|put hammer into drawer|threading|
|Octo-V||95%<br>77%|92%|69%|
|Octo-VP||82%<br>65%|88%|57%|
|Octo-VP_†_||100%<br>85%|97%|78%|


### **5.5 Can GAP be applied to various modality fusion approaches?** 

The preliminary results in Section 3 reveal that the vision-proprioception policy using straightforward concatenation tends to perform worse than the vision-only policy. We further explore a broader set of fusion approaches and validate the versatility of our algorithm. Specifically, we apply GAP to three typical and widely used fusion approaches: Concatenation, Summation and FiLM [32]. 

As reported in Table 4, vision-only policies outperforms all three fusion approaches in tasks such as “pick-place” and “put hammer into drawer”, indicating that vision modality suffice for certain tasks. However, they fail drastically in task “threading” due to demands for precise manipulation and exhibits suboptimal performance in task “push-wall”, which involves visual occlusions at the target location, highlighting the necessity of the inclusion of proprioceptive information for precise and robust manipulation. 

**Table 4** Performance of typical fusion approaches combined with GAP. _†_ indicates GAP is applied. 

|Suite||||Meta-World|||RoboSui|te||
|---|---|---|---|---|---|---|---|---|---|
|Method|Task|pick-place|assembly|disassemble|push-wall|bin-picking|put hammer into drawer|stack|threading|
|Vision-only||92%|82%|85%|64%|63%|86%|67%|44%|
|Concatenation||79%|76%|80%|56%|49%|79%|56%|34%|
|Summation||78%|95%|80%|54%|61%|75%|49%|30%|
|FiLM||75%|91%|47%|67%|59%|76%|53%|41%|
|Concatenation_†_||94%|96%|91%|73%|70%|91%|77%|52%|
|Summation_†_||92%|97%|93%|66%|70%|88%|82%|48%|
|FiLM_†_||90%|94%|85%|74%|68%|95%|72%|46%|


Concatenation preserves raw features from both modalities, but the high-dimensional redundancy hinders the policy to dynamically utilize each modality. As a result, it underperforms in tasks like “push-wall”, where effective coordination is required. Simple summation may obscure critical details, whose limitation is evident in precise manipulation tasks such as “threading” and “push-wall”. Meanwhile, FiLM applies affine transformations to conditionally adjust features, making it more suitable for tasks requiring modality collaboration. For instance, it achieves a notably higher score in “push-wall” task. However, its performance tends to degrade in simpler tasks where such complex conditioning may be unnecessary. Conversely, GAP successfully unlocked the full potential of the vision-proprioception policy, outperforming vision-only policies in all three fusion approaches. 

## **6 Visualization** 

### **6.1 Visualization of Motion-Transition Phase Estimation** 

To better understand the Motion-Transition Phase Estimation, we present visualizations that display the estimated transition probabilities _ρ_ alongside corresponding RGB images of “threading” task in this section. We also show the 

9 

relationship between _ρ_ and visual uncertainty. Specifically, we leverage R3M [33] to extract universal visual features of this task, and calculate the local entropy of features based on a sliding window covariance, denoted as _u_ . The visual uncertainty _u_ is then normalized to the range [0, 1] using (tanh( _u_ )+1) _/_ 2. As shown in Figure 5, the value of _ρ_ increases sharply at key moments, such as when the robotic arm grasps an object or transitions from a vertical to a rotational movement. This demonstrates that our method accurately captures motion transitions during the robot’s operation. Moreover, we observe that increases in _ρ_ are consistently accompanied by decreases in scaled visual uncertainty, indicating a clear inverse relationship between them. It implies that changes in the visual input tend to be relatively subtle during motion transitions, highlighting the importance of enhancing the learning of the visual modality. 


**Figure 5** Visualization of Motion-Transition Phase Estimation. 

### **6.2 Visualization of Loss Curves** 

Furthermore, we demonstrate the effect of GAP on the loss curves of vision-proprioception policy in Figure 6. Due to the adjustment of GAP to the gradient updates for proprioceptive parameters, the loss decreases more slowly during the early and middle stages of training. However, the policy ultimately converges to a lower loss, indicating that GAP effectively enhances the performance of vision-proprioception policies. 


**Figure 6** Visualization of loss curves. 

## **7 Conclusion and Limitation** 

In this work, we illustrate the vision modality of the vision-proprioception policy plays a limited role during motiontransition phases due to suppression. To alleviate this, we propose the Gradient Adjustment with Phase-guidance (GAP) algorithm, enabling dynamic collaboration between vision and proprioception. We believe this work can offer valuable insights into the development of vision-proprioception policies for robotic manipulation. 

**Limitations.** All vision-proprioception policies are trained on single embodiment in this work. Exploring the role of proprioception in cross-embodiment datasets would be promising for future research. 

10 

#### **ACKNOWLEDGMENTS** 

This work was supported by Beijing Natural Science Foundation (4262050), in part by National Natural Science Foundation of China (62376274) and the fund for building world-class universities (disciplines) of Renmin University of China. 

## **References** 

- [1] J. Allum, B. Bloem, M. Carpenter, M. Hulliger, and M. Hadders-Algra, “Proprioceptive control of posture: a review of new concepts,” _Gait & posture_ , vol. 8, no. 3, pp. 214–242, 1998. 

- [2] B. Henze, C. Ott, and M. A. Roa, “Posture and balance control for humanoid robots in multi-contact scenarios based on model predictive control,” in _Proceedings of International Conference on Intelligent Robots and Systems (IROS)_ , 2014, pp. 3253–3258. 

- [3] J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter, “Learning quadrupedal locomotion over challenging terrain,” _Science robotics_ , vol. 5, no. 47, p. eabc5986, 2020. 

- [4] Y. Yang, J. Norby, J. K. Yim, and A. M. Johnson, “Proprioception and tail control enable extreme terrain traversal by quadruped robots,” in _Proceedings of International Conference on Intelligent Robots and Systems (IROS)_ , 2023, pp. 735–742. 

- [5] S. Levine, C. Finn, T. Darrell, and P. Abbeel, “End-to-end training of deep visuomotor policies,” _Journal of Machine Learning Research_ , vol. 17, no. 39, pp. 1–40, 2016. 

- [6] L. Cong, H. Liang, P. Ruppel, Y. Shi, M. Görner, N. Hendrich, and J. Zhang, “Reinforcement learning with vision-proprioception model for robot planar pushing,” _Frontiers in Neurorobotics_ , vol. 16, p. 829437, 2022. 

- [7] G. Jiang, Y. Sun, T. Huang, H. Li, Y. Liang, and H. Xu, “Robots pre-train robots: Manipulation-centric robotic representation from large-scale robot datasets,” in _Proceedings of International Conference on Learning Representations (ICLR)_ , 2025. 

- [8] L. Wang, X. Chen, J. Zhao, and K. He, “Scaling proprioceptive-visual learning with heterogeneous pre-trained transformers,” _Advances in Neural Information Processing Systems (NeurIPS)_ , vol. 37, pp. 124 420–124 450, 2024. 

- [9] Octo Model Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, C. Xu, J. Luo, T. Kreiman, Y. Tan, L. Y. Chen, P. Sanketi, Q. Vuong, T. Xiao, D. Sadigh, C. Finn, and S. Levine, “Octo: An open-source generalist robot policy,” in _Proceedings of Robotics: Science and Systems (RSS)_ , Delft, Netherlands, 2024. 

- [10] F. R. Sarlegna and R. L. Sainburg, “The roles of vision and proprioception in the planning of reaching movements,” _Progress in Motor Control: A Multidisciplinary Perspective_ , pp. 317–335, 2009. 

- [11] R. Feng, D. Hu, W. Ma, and X. Li, “Play to the score: Stage-guided dynamic multi-sensory fusion for robotic manipulation,” in _Proceedings of Conference on Robot Learning (CoRL)_ , 2024. 

- [12] Z. He, H. Fang, J. Chen, H.-S. Fang, and C. Lu, “Foar: Force-aware reactive policy for contact-rich robotic manipulation,” _IEEE Robotics and Automation Letters_ , 2025. 

- [13] N. Tsagkas, A. Sochopoulos, D. Danier, S. Vijayakumar, C. X. Lu, and O. Mac Aodha, “When pre-trained visual representations fall short: Limitations in visuo-motor robot learning,” _arXiv preprint arXiv:2502.03270_ , 2025. 

- [14] Y. Huang, J. Lin, C. Zhou, H. Yang, and L. Huang, “Modality competition: What makes joint training of multi-modal network fail in deep learning?(provably),” in _Proceedings of International Conference on Machine Learning (ICML)_ . PMLR, 2022, pp. 9226–9259. 

- [15] Y. Fan, W. Xu, H. Wang, J. Wang, and S. Guo, “Pmr: Prototypical modal rebalance for multimodal learning,” in _Proceedings of Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2023, pp. 20 029–20 038. 

- [16] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Proceedings of Conference on Robot Learning (CoRL)_ . PMLR, 2023, pp. 2165–2183. 

- [17] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi _et al._ , “Openvla: An open-source vision-language-action model,” in _Proceedings of Conference on Robot Learning (CoRL)_ , 2024. 

- [18] J. Zeng, Q. Bu, B. Wang, W. Xia, L. Chen, H. Dong, H. Song, D. Wang, D. Hu, P. Luo _et al._ , “Learning manipulation by predicting interaction,” in _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

11 

- [19] A. Mandlekar, D. Xu, J. Wong, S. Nasiriany, C. Wang, R. Kulkarni, L. Fei-Fei, S. Savarese, Y. Zhu, and R. Martín-Martín, “What matters in learning from offline human demonstrations for robot manipulation,” in _Proceedings of Conference on Robot Learning (CoRL)_ , 2022, pp. 1678–1690. 

- [20] C. Chi, S. Feng, Y. Du, Z. Xu, E. Cousineau, B. Burchfiel, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” in _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 

- [21] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “Humanplus: Humanoid shadowing and imitation from humans,” in _Proceedings of Conference on Robot Learning (CoRL)_ , 2024. 

- [22] S. Liu, L. Wu, B. Li, H. Tan, H. Chen, Z. Wang, K. Xu, H. Su, and J. Zhu, “Rdt-1b: a diffusion foundation model for bimanual manipulation,” _arXiv preprint arXiv:2410.07864_ , 2024. 

- [23] W. Xia, R. Feng, D. Wang, and D. Hu, “Phoenix: A motion-based self-reflection framework for fine-grained robotic action correction,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , June 2025, pp. 6981–6990. 

- [24] M. A. Lee, Y. Zhu, K. Srinivasan, P. Shah, S. Savarese, L. Fei-Fei, A. Garg, and J. Bohg, “Making sense of vision and touch: Self-supervised learning of multimodal representations for contact-rich tasks,” in _Proceedings of International Conference on Robotics and Automation (ICRA)_ , 2019, pp. 8943–8950. 

- [25] J. Jiang, K. Ota, D. K. Jha, and A. Kanezaki, “Modality selection and skill segmentation via cross-modality attention,” _https://arxiv.org/abs/2504.14573_ , 2025. 

- [26] H. Li, Y. Zhang, J. Zhu, S. Wang, M. A. Lee, H. Xu, E. Adelson, L. Fei-Fei, R. Gao, and J. Wu, “See, hear, and feel: Smart sensory fusion for robotic manipulation,” in _Proceedings of Conference on Robot Learning (CoRL)_ , 2023, pp. 1368–1378. 

- [27] F. Torabi, G. Warnell, and P. Stone, “Behavioral cloning from observation,” in _Proceedings of International Joint Conference on Artificial Intelligence (IJCAI)_ , 2018, pp. 4950–4957. 

- [28] S. Liu, M. Yamada, N. Collier, and M. Sugiyama, “Change-point detection in time-series data by relative density-ratio estimation,” _Neural Networks_ , vol. 43, pp. 72–83, 2013. [Online]. Available: https://www.sciencedirect.com/science/article/pii/ S0893608013000270 

- [29] S. Aminikhanghahi and D. J. Cook, “A survey of methods for time series change point detection,” _Knowledge and Information Systems_ , vol. 51, no. 2, pp. 339–367, 2017. 

- [30] T. Yu, D. Quillen, Z. He, R. Julian, K. Hausman, C. Finn, and S. Levine, “Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning,” in _Proceedings of Conference on Robot Learning (CoRL)_ , 2020, pp. 1094–1100. 

- [31] Y. Zhu, J. Wong, A. Mandlekar, R. Martín-Martín, A. Joshi, S. Nasiriany, Y. Zhu, and K. Lin, “robosuite: A modular simulation framework and benchmark for robot learning,” in _arXiv preprint arXiv:2009.12293_ , 2020. 

- [32] E. Perez, F. Strub, H. De Vries, V. Dumoulin, and A. Courville, “Film: Visual reasoning with a general conditioning layer,” in _Proceedings of the AAAI conference on artificial intelligence_ , vol. 32, no. 1, 2018. 

- [33] S. Nair, A. Rajeswaran, V. Kumar, C. Finn, and A. Gupta, “R3m: A universal visual representation for robot manipulation,” in _Proceedings of Conference on Robot Learning (CoRL)_ . PMLR, 2023, pp. 892–909. 

- [34] A. Mandlekar, S. Nasiriany, B. Wen, I. Akinola, Y. Narang, L. Fan, Y. Zhu, and D. Fox, “Mimicgen: A data generation system for scalable robot learning using human demonstrations,” in _Conference on Robot Learning (CoRL)_ . PMLR, 2023, pp. 1820–1864. 

- [35] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in _Proceedings of Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2016, pp. 770–778. 

- [36] T. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” in _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 

- [37] Q. Sun, P. Hong, T. D. Pala, V. Toh, U. Tan, D. Ghosal, S. Poria _et al._ , “Emma-x: An embodied multimodal action model with grounded chain of thought and look-ahead spatial reasoning,” _arXiv preprint arXiv:2412.11974_ , 2024. 

- [38] Z. Jia, V. Thumuluri, F. Liu, L. Chen, Z. Huang, and H. Su, “Chain-of-thought predictive control,” in _International Conference on Machine Learning (ICML)_ . PMLR, 2024, pp. 21 768–21 790. 

- [39] J. Lu, W. Xia, D. Wang, Z. Wang, B. Zhao, D. Hu, and X. Li, “Koi: Accelerating online imitation learning via hybrid key-state guidance,” in _Proceedings of Conference on Robot Learning (CoRL)_ . PMLR, 2025, pp. 3847–3865. 

12 

# **Appendix** 

## **A Implementation Details** 

In this section, we provide implementation details, including experimental settings and algorithmic specifics, to facilitate the reproduction of our work. 

### **A.1 Experiment Settings** 

Simulation experiments are conducted on two representative environments: Meta-World [30] and RoboSuite [31]. Tasks in Meta-World are relatively simple, featuring a 4-dimensional action space that includes the gripper’s position and its opening degree, while RoboSuite tasks involve complex scenarios, longer task sequence horizons and richer physical interactions, with the action space further including the orientation of the gripper. During policy learning, task in Meta-World uses 100 hard-coded expert demonstrations from its official open-source implementation, while task in RoboSuite leverages 500 synthesized trajectories that generated from human demonstrations [34]. 

We use an observation history window _H_ of 5 with the learning rate 3 _e_<sup>_−_4</sup> to train the vision-proprioception policy network. The parameters of the policy are optimized by Adam. The vision-proprioception policy consists of two feature extraction chunks and a policy head. For the visual input, spatial features are first extracted using a ResNet-18 [35] backbone, then projected into a 512-dimensional hidden representation. A 4-layer temporal transformer with a hidden dimension of 256 is applied to capture temporal features. For proprioceptive input, spatial features are extracted using a 3-layer MLP. These features are fused via concatenation and then passed through a 3-layer MLP to output a sequence of actions of length _L_ = 9. We train with batch size 128 on a single NVIDIA RTX 3090 GPU for 100 epochs (around 2 hours for 100 Meta-World demonstrations and 8 hours for 500 RoboSuite demonstrations). 

For real-world experiments, we use a 6-DoF xArm 6 robotic arm equipped with a Robotiq gripper for all one-arm tasks. The visual information is provided by RGB images captured by an Intel RealSense D435i camera mounted on the wrist. Moreover, we utilize the open-source Cobot Magic platform to support tasks requiring dual-arm collaboration. It features four robot arms and three Intel RealSense D435 RGB-D cameras. Due to extended reach of the dual-arm setup, the two wrist-mounted cameras can’t fully capture the task scene. Therefore, we also incorporate the front camera on the platform to obtain a more comprehensive RGB observation of the task. Policies of real-world experiments are trained with 50 demonstrations collected by teleoperation. For one-arm tasks, the vision-proprioception policy is the same as in simulation. For dual-arm tasks, we modified the ACT [36] architecture. we train the left-arm policy using observations from the left-wrist camera, the front camera, and the left-arm proprioceptive information, and similar settings are applied to the right-arm policy. 

In all tasks, the initial position of target object varies randomly in each validation, while the initial position of gripper remains fixed. In out-of-distribution (OOD) scenarios, the initial distribution of object positions differs from that in the training dataset of expert demonstrations. 

### **A.2 Details of GAP** 

In this study, we illustrate that vision-proprioception policy would fail during motion-transition phases due to its suppressed vision modality. To alleviate this, we propose the Gradient Adjustment with Phase-guidance (GAP) algorithm, enabling dynamic collaboration between vision and proprioception within vision-proprioception policy. 

The complete list of hyperparameters used in Equations 4 and 5 is provided in Table 5. Since the motion inconsistency of the gripper’s opening state is measured using binary (0/1) values, we set _β_ to a lower value to balance the numerical scale, while keeping _α_ = 1 to account for the overall gripper motion. To enable fine-grained gradient adjustment, we set the parameter _λ_ controlling the degree of adjustment to a moderate level, avoiding excessive modulation leading to unstable gradient updates and potential policy collapse. Additionally, we apply gradient adjustment only during the early stage of policy learning, such as the first 50 epochs. Ablation studies on these hyperparameters are provided in Section B.3. For bimanual tasks, the proprioceptive information from each arm differs in physical meaning. The trajectories of the two arms thus have distinct motion transition phases. Therefore, we train policies for each arm independently. In transformer-based models, modalities become highly integrated within the transformer, we thus only 

13 

applied gradient adjustment to the proprioception feature extractor (i.e., the parameters before the transformer) for Octo-VP. 

**Table 5** List of hyperparameters uesd in GAP. 

|**Hyperparameters**|**Value**|
|---|---|
|_α_|1|
|_β_|2_e_<sup>_−_3</sup>|
|_λ_|0.3|


## **B Ablation Experiments** 

### **B.1 Ablation on Motion-Transition Phase Estimation** 

In our proposed GAP framework, the Motion-Transition Phase Estimation module is essential for enhancing visionproprioception policies. To thoroughly analyze its effectiveness and robustness, we conducted comprehensive ablation studies. 

First, we kept other components unchanged and tested the impact of different trajectory decomposition methods on policy learning. The detailed descriptions of the comparison methods are as follows: 

- Human: Since obtaining ground truth phase transition labels is infeasible due to the complexity and diversity of manipulation tasks, we instead employ human experts to manually label phase transitions. 

- HDBSCAN: Following Emma-X [37] , we utilize the HDBSCAN algorithm to cluster our distance metric defined in Equation 4, decomposing trajectories into phases. 

- CoTPC [38]: To decompose task trajectories into temporally close and functionally similar subskills, CoTPC applies the Change Point Detection (CPD) algorithm on the sequence of robot actions using Cosine distance. 

As shown in Table 6, using human-labeled phase transitions for gradient adjustment does provide a slight improvement in performance. However, since human annotators tend to decompose trajectories from a semantic perspective rather than based on actual motion changes, this approach may miss certain transition points, resulting in only limited gains. The cluster-based HDBSCAN method disrupts the temporal structure inherent to manipulation tasks, leading to even worse policy performance compared to human labeling. Notably, both CoTPC and our GAP framework employ the CPD algorithm for phase estimation and generally outperform human annotation across most tasks, suggesting that automated phase estimation can capture motion transitions more effectively than manual labeling. However, CoTPC relies on a simple cosine distance, which lacks the ability to represent the nuanced characteristics of robot motion, thus yielding less significant performance improvements compared to GAP. In our approach, the motion-consistent distance defined in Equation 4 captures spatial position changes, rotational changes, and gripper opening state changes, enabling more accurate and efficient prediction of motion transitions. 

**Table 6** Performance Comparison between GAP and other decomposition methods. 

|Suite|||Meta-World|||RoboSui|te||
|---|---|---|---|---|---|---|---|---|
|Method<br>Task|pick-place|assembly|disassemble|push-wall|bin-picking|put hammer into drawer|stack|threading|
|Vision-only|92%|82%|85%|64%|63%|86%|67%|44%|
|Human|95%|83%|88%|68%|65%|88%|70%|47%|
|HDBSCAN [37]|88%|81%|87%|60%|57%|82%|61%|37%|
|CoTPC [38]|91%|85%|90%|66%|62%|85%|69%|50%|
|GAP (Ours)|94%|96%|91%|73%|70%|91%|77%|52%|


14 

To further understand the performance gap between GAP and human labeling, we calculated the precision and recall between GAP outputs and human labels. Our results show that GAP achieves a high recall (97% on average) but a relatively lower precision (73% on average), suggesting that the CPD algorithm not only accurately detects semantic changes during manipulation but also identifies motion transitions that may be overlooked by humans. This experiment highlights that our method offers an effective and efficient approach, given that obtaining ground truth phase transition labels is infeasible due to the complexity and diversity of manipulation tasks. 

### **B.2 Ablation on Temporal Network** 

We further validate the effectiveness of the LSTM component by conducting comprehensive ablation studies. Specifically, we compared the LSTM-based phase transition modeling with the following alternatives: 

- Fixed _ρ_ : For the phase transition indices output by CPD, we applied a fixed gradient adjustment magnitude _ρ_ to the corresponding samples during policy learning. 

- Smooth: Following KOI [39], we modeled the transition process by treating the CPD output index as the mean of a Gaussian distribution. 

The results in Table 7 show that while alternative methods such as smoothing may serve as substitutes for modeling transitions, they regretfully fail to provide significant performance improvements. 

**Table 7** Ablation Studies on the LSTM component. 

|Method<br>Task|put hammer into drawer|threading|cube|
|---|---|---|---|
|Vision-only|86%|44%|70%|
|Fixed_ρ_=0.3|77%|44%|65%|
|Fixed_ρ_=0.5|89%|48%|75%|
|Fixed_ρ_=0.7|82%|38%|65%|
|Smooth|88%|46%|80%|
|GAP (Ours)|91%|52%|85%|


Additionally, to demonstrate the LSTM‘s effectiveness in eliminating potential estimation errors, we conducted noise injection experiments by randomly selecting a direction and shifting each CPD output index with a probability of 0.5, repeating this shift process recursively. As shown in Table 8, even when considerable noise is injected into the CPD outputs, the policy performance remains robust. We attribute this robustness to the LSTM’s capability to model continuous transitions, which effectively alleviates the impact of errors introduced by the CPD algorithm. 

**Table 8** Noise Injection Experiments. 

|Method<br>Task|put hammer into drawer|threading|cube|
|---|---|---|---|
|Vision-only|86%|44%|70%|
|Concatenation|79%|34%|55%|
|Noise-Injected|88%|49%|85%|
|GAP (Ours)|91%|52%|85%|


15 

**Table 9** Ablation Studies on _α_ and _β_ . 

|Method<br>Task|assembly|threading|put the banana in the box|
|---|---|---|---|
|Vision-only|83%|44%|55%|
|Concatenation|75%|33%|50%|
|_α_= 0_._5_, β_ = 2_e_<sup>_−_3</sup>|93%|49%|65%|
|_α_= 2_, β_ = 2_e_<sup>_−_3</sup>|91%|57%|60%|
|_α_= 1_, β_ = 10_e_<sup>_−_3</sup>|88%|51%|60%|
|GAP (_α_= 1_, β_ = 2_×_10<sup>_−_3</sup>)|94%|53%|65%|


### **B.3 Ablations on Hyperparameters** 

To validate the effectiveness and robustness of our proposed GAP framework, we conduct comprehensive ablation studies on the key hyperparameters of the gradient adjustment. 

First, we examine the selection of hyperparameters _α_ and _β_ , which serve to balance the relative contribution of each term in Equation 4, thus providing a more accurate measurement of whether the directions of these changes are consistent. As described in Section A.1, we set _α_ = 1 so that displacement consistency and rotation consistency are equally weighted. Since gripper opening consistency is measured via sign function (which outputs 0 or 1), we set _β_ = 2 _e_<sup>_−_3</sup> to ensure this term would not overshadow the first two terms. The results in Table 9 show that when _α_ is small, displacement consistency contributes more to overall motion consistency, which leads to higher success rate of tasks where displacement dominates, such as "assembly" and "put the banana in the box". In contrast, when _α_ = 2, the final policy performs better on the "threading" task, where rotation is more important. Increasing _β_ to 10 _×_ 10<sup>_−_3</sup> to emphasize the importance of gripper opening does not yield substantial improvement. Notably, all three sets of hyperparameter choices result in vision-proprioception policies that outperform policies without GAP, and are also superior to vision-only policies, indicating that our proposed GAP method is robust to hyperparameter selection. 

We also perform ablation studies on the _λ_ in Equation 5. In our GAP framework, we set _λ_ = 0 _._ 3 by default to control the degree of gradient adjustment. As shown in Table 10, the policy performance is not highly sensitive to changes in _λ_ between 0.2 and 0.4. However, setting _λ_ too small results in insufficient attenuation of the proprioception gradients, causing the policy performance to become similar to or even worse than the simple concatenation baseline. Conversely, if _λ_ is set too large, it leads to instability and even collapse during policy training. 

**Table 10** Ablation Studies on _λ_ . 

|Method<br>Task|assembly|threading|put the banana in the box|
|---|---|---|---|
|Vision-only|83%|44%|55%|
|Concatenation|75%|33%|50%|
|_λ_= 0_._1|77%|41%|50%|
|_λ_= 0_._2|91%|57%|60%|
|_λ_= 0_._4|96%|49%|65%|
|_λ_= 0_._8|70%|37%|50%|
|GAP (_λ_= 0_._3)|94%|53%|65%|


The impact of stages of applying GAP has been evaluated as well. In all of our experiments, policies are trained for 100 

16 

epochs. We apply GAP during the first 50 epochs to avoid excessive modulation, which may cause unstable gradient updates and potentially lead to policy collapse. Table 11 presents the impact of the number of training stages _x_ during which GAP is applied on the final policy performance. Applying GAP in the early stages of training improves the performance of vision-proprioception policies. However, if the gradient updates for proprioception are suppressed for too many epochs, the performance of policies deteriorates. 

**Table 11** Ablation Studies on the number of stages of applying GAP _x_ . 

|Method<br>Task|assembly|threading|put the banana in the box|
|---|---|---|---|
|Vision-only|83%|44%|55%|
|Concatenation|75%|33%|50%|
|_x_= 10|77%|38%|50%|
|_x_= 30|88%|47%|60%|
|_x_= 70|83%|45%|55%|
|_x_= 90|72%|35%|50%|
|GAP (_x_= 50)|94%|53%|65%|


## **C Additional Experiments** 

### **C.1 Linear-Probing Experiments on the Visual Features** 

To directly evaluate the visual features and verify whether our proposed GAP framework enhances the learning of visual representations, we conduct linear-probing experiments on the vision features extracted before and after applying GAP. Specifically, we extract and freeze the visual branch of the vision-proprioception policy and train a separate policy head to predict actions using only these frozen visual features. This linear-probing setup ensures that any performance differences directly reflect the quality of the learned visual representations. 

These policies are evaluated in both in-distribution and out-of-distribution settings, where object positions at test time differ from those in the training data. As shown in Table 12, the visual branch trained with GAP significantly outperforms that without GAP in both in-distribution and out-of-distribution scenarios across different tasks. 

**Table 12** Linear-Probing Experiments on the Visual Features. 

|Method<br>Task|assembly|assembly (OOD)|threading|threading (OOD)|
|---|---|---|---|---|
|Visual branch without GAP|61%|45%|26%|14%|
|Visual branch with GAP|74%|69%|41%|27%|


### **C.2 Experiments with Various Policy Heads** 

The previous experiments have demonstrated the effectiveness of our GAP on policies with MLP-based policy heads. Additionally, we conducted experiments using the popular UNet-based diffusion policy head [20] and reported the results in Table 13. The results show that policies using a diffusion-based policy head are generally better those with MLP-based heads, while applying the GAP method still outperforms vision-only policies and other methods. 

17 

**Table 13** Comparisons with other methods in simulated environments. Vision-Proprioception policies are equipped with UNet-based diffusion policy head. 

|Suite||Meta-World||Ro|boSuite|
|---|---|---|---|---|---|
|Method<br>Task|disassemble|push-wall|bin-picking|stack|threading|
|Vision-only|92%|70%|66%|73%|51%|
|Concatenation|82%|62%|51%|62%|40%|
|MS-Bot [11]|93%|75%|72%|77%|58%|
|Aux [21]|93%|71%|75%|72%|55%|
|Mask [22]|87%|83%|67%|66%|53%|
|GAP (Ours)|97%|88%|81%|87%|63%|


### **C.3 More Out-Of-Distribution (OOD) Evaluations** 

To further assess the robustness of GAP under diverse visual distribution shifts, we conducted additional out-ofdistribution experiments beyond the object placement variations reported in Table 2. Specifically, we evaluated three additional types of visual perturbations: 

- Table Color: The color of the table was modified during testing, altering the overall scene appearance. 

- Object Color: Objects with different colors from those used during training were employed, introducing colorbased perturbations. 

- Lighting: Colored spot lighting was introduced to create additional visual disturbances during testing. 

The results in Table 14 and Table 15 show that GAP consistently outperforms baseline methods under all tested OOD conditions. Among different perturbations, placement changes exert the most significant impact on performance, underscoring the importance of accurate target object localization for successful manipulation. While concatenation benefits from proprioceptive information that remains unaffected by visual disturbances, the lack of precise position perception results in overall suboptimal performance. 

In contrast, GAP achieves superior performance compared to vision-only approaches, highlighting that leveraging proprioceptive information in collaboration with vision enhances policy robustness under challenging OOD scenarios. 

**Table 14** OOD evaluation of the task “assembly” in Meta-World. 

|Method<br>Task|Placement|Table Color|Object Color|Lighting|
|---|---|---|---|---|
|Vision-only|78%|80%|75%|73%|
|Concatenation|62%|72%|76%|74%|
|GAP (Ours)|88%|85%|83%|90%|


**Table 15** OOD evaluation of the task “cube” in the Real-World. 

|Method<br>Task|Placement|Table Color|Object Color|Lighting|
|---|---|---|---|---|
|Vision-only|60%|65%|60%|55%|
|Concatenation|35%|50%|55%|50%|
|GAP (Ours)|75%|80%|85%|80%|


18 

### **C.4 Experiments of extending GAP to on-policy updates** 

To verify whether GAP can be effectively applied to on-policy updates, we conduct experiments using online learning settings in this section. In these experiments, we use vision-proprioception policies initialized with behavior cloning and train the LSTM to predict motion transition probabilities in real-time during exploration, thereby adjusting proprioception gradient updates dynamically in online learning. This setup allows us to assess whether GAP maintains its effectiveness when the policy is updated based on newly collected experience, rather than a fixed offline dataset. 

**Table 16** Experiments with On-Policy Updates. 

|Method<br>Task|assembly|bin-picking|threading|
|---|---|---|---|
|Vision-only|88%|71%|50%|
|Concatenation|78%|50%|37%|
|GAP|94%|82%|61%|


The results in Table 16 demonstrate that policies trained with online learning are more robust, and GAP can be effectively applied to on-policy updates across different tasks and environments. Additionally, the online learning experiments demonstrate that GAP does not over-dampen necessary proprioception reliance, as the policies maintain strong performance while still benefiting from the enhanced visual representations. 

## **D Task Descriptions** 

In this subsection, we provide detailed descriptions of tasks we evaluated and visualize additionally simulation tasks in Figure 7. The evaluations comprehensively cover a wide range of manipulation tasks, including simple pick-and-place tasks, rotation-sensitive tasks, as well as long-horizon and contact-rich tasks and includes one-arm and dual-arm robot setups. 

- pick-place: The robot arm first needs to locate the position of the cylinder, then move toward it. After grasping the object, it locates the target circle and moves the object to the target position. 

- assembly: The robot arm first locates the position of the part, then moves toward it. After grasping the part, it locates the position of the base, moves the part above it, and finally assembles them. 

- disassemble: The robot arm first locates the position of the part, then moves toward it. After grasping the part, it disassembles the part from the base. 

- push-wall: The robot arm first locates the position of the cylinder, then moves toward it. After grasping it, the arm pushes it to a target point behind the wall. The target point is not visible through visual observation, but its location remains fixed across all evaluations. 

- bin-picking: The robot arm first locates the position of the green cube, then moves toward it. After grasping it, the arm removes it from the red container and finally places it into the blue container. 

- put hammer into drawer: The robot arm first locates the position of the drawer and then moves toward it. After opening the drawer, it locates the position of the hammer, grasps it, places it inside the drawer, and finally closes the drawer. 

- stack: The robot arm first locates the position of the red cube and then moves toward it. After grasping it, it locates the position of the green cube and finally stacks the red cube on top of the green cube. 

- threading: The robot arm first locates the position of the pin and then moves toward it. After grasping it, it locates the position of the pinhole, then moves and rotates to align the pin with the hole, and finally inserts the pin into the hole. 

19 

- press button: The robot arm first locates the position of the button, then moves toward it, closes the gripper, and presses the button. 

- cube: The robot arm first locates the position of the cube, then moves toward it. After grasping the cube, it locates the drawer and finally places the cube in the drawer. 

- use rag to sweep table: The robot arm first locates the position of the rag, then moves toward the rag. It rotates the arm to grasp the rag, takes it down from the shelf, and finally rotates the rag to sweep the table. 

- handover: The robot first locates the position of the rectangular block, then its right arm moves toward it. After grasping the block, the right arm moves it to the center, where the left arm takes over the block in a handover. Finally, the left arm places it on the left side of the table. 

- put thermos into bag: The robot first locates the position of the bag, then its right arm moves toward it, lifts it, and rotates the wrist to open the bag. Next, robot locates the thermos, uses the left arm to grasp it, and puts it into the bag. 

- lift lid and pour: The robot first locates the position of the cup, then its left arm moves toward it to grasp and lift the lid. Next, robot locates the graduated cylinder, uses the right arm to grasp it, moves it above the cup, and finally rotates the cylinder to pour. 

20 


**Figure 7** Visualization of tasks we evaluated in simulation environments. 

