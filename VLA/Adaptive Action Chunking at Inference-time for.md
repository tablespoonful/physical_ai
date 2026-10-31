---
title: "Adaptive Action Chunking at Inference-time for Vision-Language-Action Models"
date: "2026-04-05"
authors: "Yuanchang Liang; Xiaobo Wang; Kai Wang; Shuo Wang; Xiaojiang Peng; Haoyu Chen"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2604.04161
pdf: https://arxiv.org/pdf/2604.04161
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.04161)** / [論文ページ](https://arxiv.org/abs/2604.04161)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Adaptive Action Chunking at Inference-time for Vision-Language-Action Models** 

Yuanchang Liang<sup>1</sup> Xiaobo Wang<sup>2</sup><sup>_,_3�</sup> Kai Wang<sup>1</sup> Shuo Wang<sup>4</sup> Xiaojiang Peng<sup>5</sup> Haoyu Chen<sup>6</sup> David Kim Huat Chua<sup>1</sup> Prahlad Vadakkepat<sup>1</sup> 

1National University of Singapore 2Shenzhen University of Advanced Technology 

3Sangfor Technologies Inc. 4Mininglamp Technology 5Shenzhen Technology University 6City University of Hong Kong 

_liangyuanchang@u.nus.edu, wangxiaobo@suat-sz.edu.cn_ 

## **Abstract** 

_In Vision-Language-Action (VLA) models, action chunking (i.e., executing a sequence of actions without intermediate replanning) is a key technique to improve robotic manipulation abilities. However, a large chunk size reduces the model’s responsiveness to new information, while a small one increases the likelihood of mode-jumping, jerky behavior resulting from discontinuities between chunks. Therefore, selecting the optimal chunk size is an urgent demand to balance the model’s reactivity and consistency. Unfortunately, a dominant trend in current VLA models is an empirical fixed chunk length at inference-time, hindering their superiority and scalability across diverse manipulation tasks. To address this issue, we propose a novel Adaptive Action Chunking (AAC) strategy, which exploits_ **_action entropy_** _as the cue to adaptively determine the chunk size based on current predictions. Extensive experiments on a wide range of simulated and real-world robotic manipulation tasks have demonstrated that our approach substantially improves performance over the state-of-the-art alternatives. The videos and source code are publicly available at https://lance-lot.github.io/adaptive-_ 

_chunking.github.io/._ 

## **1. Introduction** 

Vision-Language-Action (VLA) models have shown great potential to improve robotic manipulation abilities by generating robotic control actions from a variety of data modalities [2, 3, 13, 14, 20, 24, 26, 32, 33, 39, 41, 43]. Usually, they map basic information such as vision, language instructions, and robotic proprioception states, or additional 

> � Corresponding author. This work was supported by the Innovative Team Project in Guangdong Province under Grant 2025KCXTD040. 

information like tactile [1, 13], force [41], and 3D information [19, 31, 34, 42, 44, 47] into executable actions. Beyond that, earlier studies in imitation learning, such as ACT [46] and Diffusion Policy [9] have shown that executing a sequence of actions at each observation point, known as _action chunking_ , can effectively improve the success rates as it reduces compounding errors. Therefore, the action chunking technique is employed as a standard paradigm for VLA models. Jointly, the action chunk is simply set as a fixed length by empirical experiments. For instance, in GR00T N1.5 [2], the chunk size is set as 16 at inference-time for the RoboCasa Kitchen [28] benchmark. _π_ 0 [3] sets the inference chunk size as 16 or 25 for different benchmarks. Differently, SmolVLA [33] suggests a chunk size of 10 for the LIBERO [23] benchmark. In summary, determining a proper chunk size is non-trivial as it is not consistent for different policies. Moreover, it is intuitive that the best chunk size for different manipulation tasks is also different. To demonstrate this, we performed experiments with GR00T N1.5 [2] across multiple tasks in RoboCasa Kitchen [28]. As shown in Fig. 1, the success rates of different tasks exhibit a strong dependency on the action chunk size. 

To mitigate this dilemma at inference-time, ACT [46] integrates current and past predicted actions using Exponential Moving Average (EMA) to enhance temporal consistency. BID [25] employs a search strategy to select the optimal full action chunk from multiple candidates, where backward coherence and forward contrast scores are used to balance the policy’s consistency and reactivity. TVBID [15] further extends BID [25] by adapting the backward coherence and forward contrast scores according to the Total Variation Distance (TVD) between consecutive action chunk distributions. SGAC [35] selectively updates action chunks by comparing the cosine similarity between the first action of the previous planned chunk and the newly generated action. Nevertheless, all these methods set a fixed chunk size throughout a whole episode, relying on extensive 


Figure 1. **Effects of action chunk sizes** . At inference-time, the success rates of the GR00T N1.5 [2] on different tasks of RoboCasa Kitchen [28] are highly related to the action chunk size. It can be observed that it is difficult and sub-optimal to empirically set a fixed value for various manipulation tasks. 

empirical tuning for the action chunk size selection. Recent studies [8, 11] have begun to adaptively select the chunk size by reinforcement learning. Gou et al. [11] determine whether to choose a single action or an entire action chunk based on a regret value function. However, this handcrafted value function fails to generalize across various tasks. Chen et al. [8] introduce a learnable module that predicts chunk size, but this approach depends on task-specific reward signals available only in simulation, exhibiting limited applicability in real-world deployment. Consequently, adaptively selecting the optimal action chunk size at inference-time remains a challenging problem in practice. 

In this paper, we propose a simple yet effective Adaptive Action Chunking (AAC) strategy, which exploits _action entropy_ as the cue to determine the optimal chunk size at each inference timestep dynamically. Specifically, as action entropy reflects the uncertainty level of the predicted action, a lower entropy implies higher action reliability during task execution. Inspired by this, AAC tries to adaptively determine the optimal action chunk size by maintaining a lower action entropy. In detail, we compute the maximum differential point of average action entropy across different chunk sizes meanwhile ensuring minimum action magnitude. In high-entropy cases, where the predicted actions are of low quality, AAC executes smaller chunks and replans more frequently to improve the model’s reactivity. Conversely, when the entropy is low, longer action chunks are executed to enhance temporal consistency and inference efficiency. Notably, AAC performs action entropy computation and chunk-size adaptation only at inference-time, without additional training or architectural modifications. Therefore, it 

ensures the robustness and scalability of our method to various manipulation tasks. To sum up, the main contributions of this paper can be summarized as follows: 

- We analyze existing action chunking methods and highlight the importance of adaptive action chunking at inference-time for diffusion-based VLA models. 

- We propose AAC, a simple yet effective algorithm that exploits action entropy as the cue to dynamically select the action chunk size at inference-time. 

- We conduct extensive experiments on a wide range of simulated and real-world robotic manipulation benchmarks, demonstrating the superiority of our approach over the state-of-the-art alternatives. 

## **2. Related work** 

### **2.1. Vision-Language-Action models** 

Inspired by the success of large pre-trained vision-language models (VLMs), Vision-Language-Action (VLA) models have shown great promise in robotic policy learning by leveraging diverse, robot-specific datasets. One line of VLA models [5, 6, 17, 30, 37, 51] discretizes the continuous action space and predicts actions as tokens, showing that pretrained VLMs can be effectively adapted to low-level action predictions. In contrast, a growing body of studies [2– 4, 7, 12, 16, 18, 21, 33, 36, 45, 48, 49] leverage action experts to predict continuous actions via diffusion or flowmatching, enabling more accurate predictions. For instance, GR00T N1.5 [2] conditions a flow-matching head on VLM features to generate action chunks. CogVLA [21] systematically compares action modules and finds that diffusion action transformers scale favorably when conditioned on VLM representations. CoT-VLA [45] incorporates explicit visual chain-of-thought (CoT) reasoning into VLM by autoregressively predicting future image frames as visual goals. In this paper, we propose an adaptive action chunking strategy that operates at inference-time for VLA models, without requiring additional training or architectural modifications. Therefore, without loss of generality, this work adopts GR00T N1.5 [2] as the baseline. 

### **2.2. Action Chunking** 

Action chunking plays an important role in recent pretrained VLA models with diffusion-based action heads. At training-time, action chunking enables the policy to learn a sequence of future actions across multiple timesteps. At inference-time, however, action chunks can be executed differently to balance the policy’s consistency and reactivity. For example, ACT [46] generates a new action chunk at every timestep and preserves temporal consistency by assembling actions across different timesteps. In GR00T N1.5 [2], it adopts the same chunk size at training-time and inferencetime. In contrast, _π_ 0 [3] uses a larger chunk size (50) 

during training, but executes smaller chunks (16 or 25) at inference-time, depending on different embodiment setups. SmolVLA [33] follows a similar paradigm, referred to as an asynchronous inference mechanism. Recently, DeepConf [10] exploits model output confidence as a signal to address the Best-of-N selection problem, but it is limited to large Language Models (LLMs). Similarly, BID [25] proposes to select the best action chunk from multiple candidates based on the designed backward coherence and forward contrast scores. However, it is still required to set a fixed chunk size, which limits the reactivity and efficiency of a policy. Complementary to these fixed action chunking methods, in this paper, we investigate the adaptive selection of the optimal action chunk size at inference-time. 

value within a certain range, such as adjusting the robot’s velocity. Therefore, as described by the works [29, 38, 40], for a discrete control _a_ , its action entropy can be calculated using the following formula: 


where _A_ is the discrete action space and _p_ ( _a_ ) is the probability of a certain action output from the policy network. For continuous control of _d_ -dimensional actions, we use the Gaussian Differential entropy as follows: 


where _det_ (Σ _t_ ) is the determinant of the covariance matrix. 

## **3. Preliminaries** 

### **3.1. GR00T N1.5** 

GR00T N1.5 [2] is a typical Vision-Language-Action foundation model with a flow-matching action head. It consists of two systems, a Vision-Language Model (VLM) to extract vision-language features _ϕt_ as condition, and a Diffusion Transformer (DiT) module as the action head **V** _θ_ for flow-matching. Specifically, given a ground-truth action chunk **A** _t_ = _{_ **a** _t,_ **a** _t_ +1 _, · · · ,_ **a** _t_ + _H−_ 1 _} ∈_ R<sup>_d×H_</sup> at timestep _t_ , a flow-matching timestep _τ ∈_ [0 _,_ 1] and sampled noise _ϵ ∼N_ ( **0** _,_ **I** ), where _d_ denotes the action degrees of freedom and _H_ is the action horizon, the noised action chunk **A**<sup>(</sup> _t_<sup>_τ_)</sup> is computed as **A**<sup>(</sup> _t_<sup>_τ_)</sup> = _τ_ **A** _t_ + (1 _− τ_ ) _ϵ_ . Together with the robot state embedding **q** _t_ , the action head prediction **V** _θ_ ( _ϕt,_ **A**<sup>(</sup> _t_<sup>_τ_)</sup> _,_ **q** _t_ ) aims to approximate the flow vector field _ϵ −_ **A** _t_ by minimizing the following loss: 


which is also known as flow-matching loss in popular VLA models. At inference-time, action chunk is generated by _K_ - step iterative denoising from random noise **A**<sup>(0)</sup> _t ∼N_ ( **0** _,_ **I** ) with forward Euler integration: **A**<sup>(</sup> _t_<sup>_τ_+1</sup><sup>_/K_)</sup> = **A**<sup>(</sup> _t_<sup>_τ_)</sup> + _K_ <u>1</u><sup>**V**</sup><sup>_θ_(</sup><sup>_ϕt,_</sup><sup>**A**</sup><sup>_t,_</sup><sup>**q**</sup><sup>_t_).Formoredetails,onecanrefertothe</sup> work [2]. Note that our proposed Adaptive Action Chunking (AAC) algorithm is applicable to all VLA models with a diffusion-based action head. In this study, we use GR00T N1.5 [2] as the baseline of implementation. 

### **3.2. Action Entropy** 

Generally, entropy is computed to quantify the degree of disorder, randomness, or uncertainty. In robotics, the action space may consist of discrete controls ( _e.g._ , gripper) or continuous controls ( _e.g._ , translation and rotation). Discrete control involves selecting from a finite set of actions, such as choosing a specific gear in a vehicle. Continuous control, on the other hand, involves actions that can take on any 

## **4. Adaptive Action Chunking** 

Typically, existing VLA models with diffusion-based action heads are trained with an action horizon _H_ , and executing a sequence of _h_ ( _h ≤ H_ ) actions at each inference timestep [2, 3, 33]. A large fixed chunk size _h_ at inferencetime reduces the model’s reactivity, whereas a small one compromises its temporal consistency and computational efficiency. Moreover, it is impractical to determine a single fixed chunk size that fits across diverse manipulation tasks. To this end, we seek to adaptively determine the optimal action chunk size _h_<sup>_∗_</sup> to achieve a better balance between consistency and reactivity. 

Intuitively, if the model exhibits high uncertainty in its predictions, the action chunk size should be reduced at inference-time. Conversely, when the model is more confident, the action chunk size should be increased. To quantify this uncertainty, we exploit action entropy as a cue to adaptively select the optimal chunk size. Specifically, consider a 7-DOF robotic arm equipped with a gripper as an example, where the predicted action at the _i_ -th timestep is denoted as **a** _i_ . It consists of three components: 3-DOF translation offsets ([∆ _x,_ ∆ _y,_ ∆ _z_ ] _∈_ R<sup>3</sup> ), 3-DOF rotation offsets ([∆ _Rx,_ ∆ _Ry,_ ∆ _Rz_ ] _∈_ R<sup>3</sup> ) and 1-DOF gripper control _G ∈{_ 0 _,_ 1 _}_ . For continuous control of 3-dimensional translations and rotations, the corresponding action entropy _Et_<sup>_i_and</sup><sup>_E_</sup> _r_<sup>_i_atthe</sup><sup>_i_-thtimesteparecomputedaccordingto</sup> Eq. (3). For the discrete gripper control, its action entropy _Eg_<sup>_i_is computed by Eq. (2).To estimate the probability</sup><sup>_p_(</sup><sup>_a_)</sup> in Eq. (2) and the covariance matrix Σ _t_ in Eq. (3), we sample _N_ candidate action chunks in parallel. The probability of predicting a gripper-close state is then estimated as _p_ ( _a_ ) = _c/N_ , where _c_ denotes the number of close-state occurrences among all _N_ samples. Finally, the average action entropy _Eh_ with a chunk size _h_ is as follows: 


Figure 2. **An overview of AAC** . The proposed Adaptive Action Chunking (AAC) algorithm operates solely at inference-time, without any extra training or architectural changes. Specifically, we exploit the action entropy of continuous and discrete values as the cue to adaptively determine the optimal chunk size _h_<sup>_∗_</sup> in each action chunk at the current observation. Therefore, we can achieve a favorable trade-off between consistency and reactivity in the entire episode, and substantially improve success rates across a variety of manipulation tasks. 

The optimal chunk size _h_<sup>_∗_</sup> in each action chunk **A** _t_ can be adaptively determined by 


**Algorithm 1** Adaptive Action Chunking 

**Input:** _N_ candidate action chunks _{_ **A**<sup>_i_</sup> _t_<sup>_}N_</sup> _i_ =1<sup>predictedin</sup> parallel. Each chunk **A**<sup>_i_</sup> _t_<sup>=</sup><sup>_{at, at_+1</sup><sup>_, ..., at_+</sup><sup>_H−_1</sup><sup>_}_includes</sup> actions of _H_ future timesteps. 

**Output:** Optimal chunk size _h_<sup>_∗_</sup> at current timestep _t_ . 

where arg max _h_ ( _Eh_ +1 _− Eh_ ) is the maximum difference point of average action chunk. _ξ_ is a lower bound of chunk size, ensuring a minimum action magnitude to balance temporal consistency and computational efficiency. Since the action spaces of different robot embodiments (e.g., singlearm, bimanual, and humanoid configurations) can be modeled as either continuous or discrete domains, the formulation of action entropy in Eq. (4) naturally generalizes across them. For brevity, we omit the detailed derivations in this paper. 

We summarize the above solution as the proposed Adaptive Action Chunking (AAC) algorithm. After selecting the optimal chunk size by AAC, the first _h_<sup>_∗_</sup> actions will be executed at inference-time. For clarity, the whole scheme of our adaptive action chunking is detailed in Algorithm 1. Moreover, the difference between our method and the typical baseline GR00T N1.5 [2] is shown in Fig. 2. In consequence, we can achieve a good balance between consistency and reactivity throughout each episode, and substantially improve the success rates on various manipulation tasks. 

## **5. Experiments** 

In this section, to validate the effectiveness of the proposed AAC, we conduct extensive experiments across various manipulation tasks, ranging from simulation benchmarks and real-world applications. 

- 1: **for** _i_ = 1 to _H_ **do** 

- 2: Compute the action entropy of continuous translations and rotations at each timestep _Et_<sup>_i_and</sup><sup>_E_</sup> _r_<sup>_i_by</sup> Eq. (3). 

- 3: Compute the action entropy of the discrete gripper control at each timestep _Eg_<sup>_i_by Eq. (2).</sup> 

- 4: **end for** 

- 5: **for** _h_ = 1 to _H_ **do** 

- 6: Get average action entropy with different chunk size _Eh_ by Eq. (4). 

- 7: **end for** 

- 8: Find maximum difference point and compute the optimal chunk size _h_<sup>_∗_</sup> by Eq. (5). 

- 9: **return** Optimal chunk size _h_<sup>_∗_</sup> . 

### **5.1. Simulation Experiments** 

#### **5.1.1. Benchmarks** 

**RoboCasa Kitchen** . RoboCasa [28] is a simulation benchmark comprising 24 kitchen manipulation tasks. For clarity, 24 RoboCasa tasks are categorized into 4 groups: Relocation (10 pick-and-place tasks), Container (6 tasks of opening or closing doors and drawers), Rotation (5 rotationalaffordance tasks such as turning a sink facet or stove knob), and Button (3 tasks involving button pressing on appliances 

Table 1. **Main Results on RoboCasa and LIBERO Benchmarks** . We report the success rate (%) for various subsets and the overall average. Our AAC achieves the best or competitive results across both benchmarks. Bolded entries indicate the highest success rates. 

||||**RoboCa**|**sa**||||**LIBERO**|||
|---|---|---|---|---|---|---|---|---|---|---|
|Method|Relo.|Cont.|Rot.|Button|**Avg.**|Spatial|Long|Object|Goal|**Avg.**|
|GR00T (Default_h_=16)|42.1|80.3|57.6|80.3|59.7|93.6|88.8|97.2|**96.8**|94.1|
|GR00T (_h_=2)|29.6|57.0|59.4|64.7|47.0|93.6|81.8|93.6|91.6|90.2|
|GR00T (_h_=4)|37.9|71.3|61.2|78.7|56.2|94.0|85.8|95.4|95.2|92.6|
|GR00T (_h_=8)|42.8|80.3|**62.6**|**81.7**|61.2|92.0|**93.4**|97.8|95.4|94.7|
|GR00T (_h_=12)|42.9|79.5|60.0|79.3|60.2|93.0|91.0|97.6|95.2|94.2|
|GR00T+AAC (**Ours**)|**44.4**|**82.2**|61.4|81.3|**62.0**|**94.4**|92.8|**98.6**|94.2|**95.0**|


such as a microwave or a coffee machine). Additional details are provided in the supplementary material. 

**LIBERO.** LIBERO [23] is a robot simulation benchmark that consists of four distinct task suites: LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, and LIBERO-Long. Each suite contains 10 diverse tasks with 50 human-teleoperated demonstrations per task, designed to evaluate a robot’s ability to understand spatial relationships, object interactions, and task-specific objectives. 

#### **5.1.2. Training and Evaluation Details** 

Our model is fine-tuned from the publicly available GR00T N1.5 checkpoint [2], which was trained on a large-scale data pyramid. We fine-tune the diffusion head of GR00T N1.5 on eight NVIDIA A800 GPUs with mixed-precision training, while keeping the Eagle-2 VLM [22] backbone and vision projector frozen. The updated parameters in the diffusion head comprise DiT backbone, state encoder, state decoder, action encoder, and action decoder. For RoboCasa, we fine-tune 100 demo trajectories generated by MimicGen [27] for 90 epochs. For LIBERO, all four task suites (40 tasks in total) are jointly trained for 90 epochs. In this paper, we use the pre-processed dataset provided by OpenVLA [17] and _π_ 0 [3]. We evaluate AAC using 100 rollouts per task in RoboCasa and 50 per task in LIBERO. 

AAC improves the task success rate for most tasks, achieving an average gain of 2 _._ 3% across 24 tasks. In particular, the success rate on the Rotation task set increases from 57 _._ 6% to 61 _._ 4%, indicating a substantial performance boost. This improvement can be attributed to AAC’s ability to handle tasks requiring fine-grained control, such as manipulating a rotational switch on a sink facet or a stove. In contrast, the improvement on the Button task set is relatively modest (from 80 _._ 3% to 81 _._ 3%) _e.g._ , pressing a button on microwaves or coffee machines, since these tasks mainly involve simple pressing actions that demand less precise gripper control. For LIBERO, AAC improves the average task success rate across the four task suites by 0 _._ 9% ( _i.e._ , from 94 _._ 1% to 95 _._ 0%). The pick-and-place tasks in LIBERO exhibit higher overall success rates compared to those in RoboCasa, likely due to the limited diversity in object positions within the LIBERO testing environments. Nonetheless, a notable gain of 4% is achieved on the most challenging LIBERO-Long suite. Each episode in LIBERO-Long involves multiple subtasks requiring precise operation over a longer action trajectory. The proposed adaptive action chunking strategy effectively addresses this challenge by executing high-confidence action chunks and replanning upon new observations, thereby yielding consistent improvements on complex, long-horizon manipulation tasks. 

#### **5.1.3. Quantitative Results** 

**Baseline.** As illustrated in Sec. 3.1, this paper adopts the vanilla GR00T N1.5 [2] as the baseline, which uses a fixed and consistent action horizon of 16 for both training and action execution. For the compared approaches, inspired by previous studies [3, 9, 33], we set a fixed inference action chunk size _h_ with different values for GR00T. In contrast, our AAC adaptively determines the optimal chunk size _h_<sup>_∗_</sup> at each inference step. 

**Comparison with Vanilla GR00T.** Experimental results on the adopted two simulation benchmarks, Robocasa [28] and LIBERO [23], are presented in Tab. 1. In Robocasa, 

**Comparison with Fixed-size GR00T.** Besides the baseline, vanilla GR00T, we further compare our AAC with GR00T using different chunk sizes. Specifically, we evaluate the task success rates by varying the fixed chunk size _h_ at inference-time. As shown in Tab. 1, the results indicate that using a fixed chunk size leads to suboptimal performance. For instance, the task set LIBERO-Spatial performs best with a chunk size of 4, whereas LIBERO-Goal achieves the highest success rate with a chunk size of 16. This observation reveals the potential to improve the task success rate by adaptively changing chunk size within or across different tasks. Inspired by this, AAC adaptively 


Figure 3. **Rollout of chunk sizes from AAC** . The derived chunk sizes align with human intuitions with respect to different semantic phases: a large chunk size is observed during the transportation stage, while a small chunk size appears at the critical manipulation stage. 

determines the chunk size by leveraging action entropy as a cue, thereby eliminating the need for manual and timeconsuming chunk-size tuning. Consequently, AAC consistently outperforms all fixed-size baselines on average. Detailed results for each fixed-size configuration and individual tasks are provided in the Appendix. 

Table 2. Success rates (%) with _π_ 0 _._ 5 backbone on LIBERO. 

|Method|Spatial|Long|Object|Goal|Avg.|
|---|---|---|---|---|---|
|_π_0_._5|98.5|92.5|98.7|**98.1**|97.0|
|_π_0_._5+AAC (**Ours**)|**99.1**|**95.2**|**99.2**|98.0|**97.9**|


Figure 4. **Distribution of chunk size decisions from AAC** . We show the chunk size distribution of episodes on the first task of LIBERO-Spatial: _”Pick up the black bowl next to the cookie box and place it on the plate”_ . The heatmap indicates the frequency of different chunk sizes at different decision timesteps. The red curve shows the mean chunk size at different observation timesteps. 

#### **5.1.4. Qualitative Results** 

**Distribution of Chunk Size Decision.** To qualitatively analyze the performance of the proposed AAC, we present a representative example illustrating the chunk size decision process in Fig. 3. The corresponding distribution of chunk sizes across simulation timesteps is visualized in Fig. 4. As shown in the heatmap and the average curve, the chunk 

sizes predicted by AAC closely follow the semantic phases of the task. Initially (around _t <_ 20), when the gripper is far away from the object, AAC tends to predict a large chunk size. When the gripper approaches the object (around 30 _< t <_ 50), small chunk sizes are predicted. After successfully grasping the object ( _t >_ 50), AAC again increases the chunk size to efficiently transport the object to the target location. This adaptive pattern mirrors human intuition: larger chunks enable fast, coarse movements when approaching the target or transporting the lifted object, while smaller chunks with high-frequency observations ensure precise, fine control during the critical grasping and manipulation phases. 

#### **5.1.5. Scalability and Efficiency** 

**Different Backbones** We apply our AAC to different VLA backbones ( _i.e._ , GR00T and _π_ 0 _._ 5<sup>1</sup> [4]) on LIBERO and LIBERO Pro [50] benchmarks. From the results in Tab. 2, we can observe that AAC generalizes well on _π_ 0 _._ 5 backbone. We highlight that AAC is designed for the flowmatching action head, and it can be easily adapted to different backbones. 

**Out of Distribution Scenarios** We evaluate the robustness of AAC on OOD tasks by using the position perturba- 

1gs://openpi-assets/checkpoints/pi05_libero/ 

Table 3. Success rates (%) on LIBERO-Pro [50]. 

|Perturbation level|_×_0.2|_×_0.3|_×_0.4|Avg.|
|---|---|---|---|---|
|GR00T|11.3|0.4|0.0|3.9|
|GR00T+AAC (**Ours**)|**17.9**|**0.9**|0.0|**6.3**|
|_π_0_._5|53.2|29.9|9.5|30.9|
|_π_0_._5+AAC (**Ours**)|**57.4**|**35.3**|**11.8**|**34.8**|


Table 4. Success rates (%) on LIBERO and inference-time under different numbers of samples for estimating action entropy. 

|#Samples|1|5|10|20|30|40|
|---|---|---|---|---|---|---|
|Succ. (%)|94.1|94.7|94.4|95.0|95.0|95.5|
|Time (ms)|83.0|83.5|84.3|106.0|136.5|157.0|


### **5.2. Real-world Experiments** 

#### **5.2.1. Setup** 

We further evaluate the performance of the proposed AAC with different desktop applications in the real world. We use a Realman single-arm robot with a Mycobot gripper. A SpaceMouse is also used for collecting 50 humanteleoperated demonstrations per task. The visual observation includes a wrist RGB view and a side RGB view on a tripod. The state and action space are consistent with the configuration in Robocasa and LIBERO benchmarks. We finetune GR00T N1.5 [2] checkpoint on each of the tasks with 8 NVIDIA A800 GPUs for 300 epochs. The batch size on each GPU is set to 32. For each task, we evaluate the success rate on 20 trials with a limitation of 600 action execution steps for each trial. 

#### **5.2.2. Tasks** 

tion subset of LIBERO-Pro [50] benchmark. The quantitative results are reported in Tab. 3, from which we can summarize that as the perturbation level increases, the success rates of both the baseline methods and AAC decrease. Nevertheless, our AAC demonstrates its effectiveness by leveraging the action entropy to dynamically modulate the execution horizon. 

**Different Number of Samples.** As illustrated in Sec. 4, AAC is based on the distribution of action entropy, which is derived from multiple candidate predicted action chunks. Therefore, we investigate the impact of varying the number of samples. From the results in Tab. 4, we can conclude that the success rate can be continuously improved with a larger number of samples. When the number of samples increases from 1 to 20, the success rate continuously improves 0 _._ 9%, from 94 _._ 1% to 95 _._ 0%. However, the improvement is marginal when the samples are enough ( _e.g_ , 20) to estimate the action entropy. In consequence, we use 20 samples to balance the tradeoff between computational efficiency and success rate in all benchmarks. 

We design 3 real-world tasks to evaluate the proposed method: (1) a banana pick-and-place task, (2) an emergency button pressing task, and (3) a long-horizon task that involves picking and placing the toy, then closing the drawer. Specifically, the first task requires picking up a banana and placing it into a rattan fruit basket. Both the banana and the basket are randomly positioned on a round table with a diameter of 0.6 m. For evaluation, 20 different combinations of banana and basket locations are tested, as the position and orientation of the gripper critically influence grasping success. The second task involves pressing an emergency button (E-Button), demanding higher localization accuracy than the banana pick-and-place task. During data collection, the E-Button positions cover only the upper half of the table. Therefore, this task is challenging because some button positions in the evaluation are unseen during training. The third task is a long-horizon task, where the robot must pick up a randomly placed toy, place it into a drawer, and subsequently close the drawer. To complete this task, the policy needs to ensure precision along the whole trajectory. 

Table 5. Success rates (%) on real-world applications. 

**Computational Efficiency.** The calculation of action entropy requires multiple action chunk candidates. Thus, AAC inevitably involves additional computational cost compared to the fixed-size competitors. Fortunately, as the multiple action chunk candidates can be generated through batched parallel computation, the computational cost is negligible. The inference time for different sample sizes on a single A800 GPU is shown in Tab. 4. From the results, we can see that the influence on the inference speed is negligible when the number of samples is smaller than 10. The default sample size used in this paper is 20, which will introduce about 20 ms inference delay according to the testing results in the last row of Tab. 4. Higher-end GPUs can further close the computational gap. 

|Task|Banana|Button|Drawer|Avg.|
|---|---|---|---|---|
|GR00T|70.0|65.0|65.0|67.0|
|GR00T+AAC|**90.0**|**75.0**|**80.0**|**82.0**|


#### **5.2.3. Results** 

**AAC improves real-world task success rates.** We present the quantitative results in Tab. 5. The results demonstrate that AAC consistently outperforms the baseline GR00T across all three real-world tasks. On average, AAC achieves a 15% performance gain, increasing the success rate from 67 _._ 0% to 82 _._ 0%. The performance improvement arises from multiple aspects. For the banana pick- 


Figure 5. Execution examples for real-world tasks using AAC. Videos of complete execution trajectories will be publicly available. 

and-place task, AAC allows the robot to better align the gripper orientation with respect to the target banana, resulting in more precise grasping. In the E-Button pressing task, both the baseline GR00T and the proposed AAC can successfully complete the task under familiar conditions. However, when the E-button appears at locations that lie near but outside the location distribution of humanteleoperated demonstrations, AAC shows better generalization ability and achieves more robust performance. For the long-horizon toy manipulation task, although the drawerclosing stage is relatively easy due to its lower precision requirements, AAC achieves a higher success rate in the toypicking stage, benefiting from adaptive chunk sizes. 


(a) Execution process of GR00T. (b) Execution process of AAC. 

Figure 6. **AAC improves action accuracy and safety** . **Left** : the gripper collided with the table. **Right** : the gripper reached an appropriate lowest point. 

## **6. Conclusion** 

**AAC improves action accuracy and safety.** In this part, we illustrate that the proposed AAC has the ability to localize more precisely, thanks to the adaptive chunk size strategy that ensures higher action quality. As shown in Fig. 6, the baseline vanilla GR00T tends to collide with the tabletop due to the low-quality actions predicted at the earlier observation point. In contrast, AAC is able to smoothly stop at an appropriate lowest point by filtering high-entropy or uncertain actions through the dynamically selected chunk size. This phenomenon demonstrates the potential of AAC for high-precision robot manipulation tasks, thus improving safety and robustness in practice. 

In this work, we have analyzed that the action chunk size is important for robot manipulation tasks. Based on this observation, we propose Adaptive Action Chunking (AAC), an inference-time strategy that exploits action entropy as the cue to adaptively select action chunk size. It aligns with human intuitions that a large chunk size is used at the transportation stage, while a small chunk size appears at the critical manipulation stage. Consequently, we achieve a good balance between reactivity and consistency. Extensive experiments on a variety of simulation benchmarks and realworld applications have validated the effectiveness of our approach over the baseline and state-of-the-art alternatives. 

## **References** 

- [1] Jianxin Bi, Kevin Yuchen Ma, Ce Hao, Mike Zheng Shou, and Harold Soh. VLA-Touch: Enhancing vision-languageaction models with dual-level tactile feedback. _arXiv preprint arXiv:2507.17294_ , 2025. 1 

- [2] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. GR00T N1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 1, 2, 3, 4, 5, 7 

- [3] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-languageaction flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 1, 2, 3, 5 

- [4] Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: a vision-languageaction model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 2, 6 

- [5] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alexander Herzog, Jasmine Hsu, et al. RT-1: Robotics Transformer for real-world control at scale. _Robotics: Science and Systems XIX_ , 2023. 2 

- [6] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, et al. WorldVLA: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 2 

- [7] Hao Chen, Jiaming Liu, Chenyang Gu, Zhuoyang Liu, Renrui Zhang, Xiaoqi Li, Xiao He, Yandong Guo, Chi-Wing Fu, Shanghang Zhang, et al. Fast-in-Slow: A dual-system foundation model unifying fast manipulation within slow reasoning. _arXiv preprint arXiv:2506.01953_ , 2025. 2 

- [8] Ruopei Chen, Ke Wang, et al. Adaptive action chunk selector. Stanford CS224R 2025 Final Report, 2025. 2 

- [9] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44: 1684–1704, 2023. 1, 5 

- [10] Yichao Fu, Xuewei Wang, Yuandong Tian, and Jiawei Zhao. Deep think with confidence. In _NeurIPS 2025 Workshop on Efficient Reasoning_ , 2025. 3 

- [11] Ruiyu Gou. _Learning temporal action chunking for motor control_ . PhD thesis, University of British Columbia, 2024. 2 

- [12] Zhi Hou, Tianyi Zhang, Yuwen Xiong, Haonan Duan, Hengjun Pu, Ronglei Tong, Chengyang Zhao, Xizhou Zhu, Yu Qiao, Jifeng Dai, et al. Dita: Scaling diffusion transformer for generalist vision-language-action policy. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 7686–7697, 2025. 2 

- [13] Jialei Huang, Shuo Wang, Fanqi Lin, Yihang Hu, Chuan Wen, and Yang Gao. Tactile-VLA: Unlocking visionlanguage-action model’s physical knowledge for tactile generalization. _arXiv preprint arXiv:2507.09160_ , 2025. 1 

- [14] Yuming Jiang, Siteng Huang, Shengke Xue, Yaxi Zhao, Jun Cen, Sicong Leng, Kehan Li, Jiayan Guo, Kexiang Wang, Mingxiu Chen, et al. RynnVLA-001: Using human demonstrations to improve robot manipulation. _arXiv preprint arXiv:2509.15212_ , 2025. 1 

- [15] Sarosh Khan and Ellie Tanimura. Test-time stochasticity estimation for adaptive action chunk selection. Stanford CS224R 2025 Final Report, 2025. 1 

- [16] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 2 

- [17] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P Foster, Pannag R Sanketi, Quan Vuong, et al. OpenVLA: An open-source vision-language-action model. In _Conference on Robot Learning_ , 2025. 2, 5 

- [18] Myungkyu Koo, Daewon Choi, Taeyoung Kim, Kyungmin Lee, Changyeon Kim, Youngyo Seo, and Jinwoo Shin. Hamlet: Switch your vision-language-action model into a historyaware policy. _arXiv preprint arXiv:2510.00695_ , 2025. 2 

- [19] Chengmeng Li, Junjie Wen, Yaxin Peng, Yan Peng, and Yichen Zhu. PointVLA: Injecting the 3D world into visionlanguage-action models. _IEEE Robotics and Automation Letters_ , 11(3):2506–2513, 2026. 1 

- [20] Peiyan Li, Yixiang Chen, Hongtao Wu, Xiao Ma, Xiangnan Wu, Yan Huang, Liang Wang, et al. BridgeVLA: Inputoutput alignment for efficient 3D manipulation learning with vision-language models. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 1 

- [21] Wei Li, Renshan Zhang, et al. CogVLA: Cognition-aligned vision-language-action models via instruction-driven routing & sparsification. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 2 

- [22] Zhiqi Li, Guo Chen, Shilong Liu, Shihao Wang, Vibashan VS, Yishen Ji, Shiyi Lan, Hao Zhang, Yilin Zhao, et al. Eagle 2: Building post-training data strategies from scratch for frontier vision-language models. _arXiv preprint arXiv:2501.14818_ , 2025. 5 

- [23] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, et al. LIBERO: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 2023. 1, 5 

- [24] Jiaming Liu, Hao Chen, Pengju An, Zhuoyang Liu, Renrui Zhang, Chenyang Gu, Xiaoqi Li, Ziyu Guo, Sixiang Chen, Mengzhen Liu, et al. HybridVLA: Collaborative diffusion and autoregression in a unified vision-language-action model. _arXiv preprint arXiv:2503.10631_ , 2025. 1 

- [25] Yuejiang Liu, Jubayer Ibn Hamid, Annie Xie, Yoonho Lee, Max Du, and Chelsea Finn. Bidirectional decoding: Improving action chunking via guided test-time sampling. In _The Thirteenth International Conference on Learning Representations_ , 2025. 1, 3 

- [26] Yueen Ma, Zixing Song, Yuzheng Zhuang, Jianye Hao, and Irwin King. A survey on vision-language-action models for embodied ai. _arXiv preprint arXiv:2405.14093_ , 2024. 1 

- [27] Ajay Mandlekar, Soroush Nasiriany, Bowen Wen, Iretiayo Akinola, Yashraj Narang, Linxi Fan, Yuke Zhu, and Dieter 

   - Fox. MimicGen: A data generation system for scalable robot learning using human demonstrations. In _Conference on Robot Learning_ , 2023. 5 

- [28] Soroush Nasiriany, Abhiram Maddukuri, Lance Zhang, Adeet Parikh, Aaron Lo, Abhishek Joshi, Ajay Mandlekar, and Yuke Zhu. Robocasa: Large-scale simulation of everyday tasks for generalist robots. In _RSS 2024 Workshop: Data Generation for Robotics_ . 1, 2, 4, 5 

- [29] Shuaicheng Niu, Jiaxiang Wu, Yifan Zhang, Yaofo Chen, Shijian Zheng, Peilin Zhao, and Mingkui Tan. Efficient testtime model adaptation without forgetting. In _International Conference on Machine Learning_ , 2022. 3 

- [30] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. FAST: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 2 

- [31] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. SpatialVLA: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 1 

- [32] Ameesh Shah, William Chen, Adwait Godbole, Federico Mora, Sanjit A Seshia, and Sergey Levine. Learning affordances at inference-time for vision-language-action models. _arXiv preprint arXiv:2510.19752_ , 2025. 1 

- [33] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, et al. SmolVLA: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 1, 2, 3, 5 

- [34] Ishika Singh, Ankit Goyal, Stan Birchfield, Dieter Fox, Animesh Garg, and Valts Blukis. OG-VLA: 3D-aware vision language action model via orthographic image generation. _arXiv preprint arXiv:2506.01196_ , 2025. 1 

- [35] Junhyuk So, Chiwoong Lee, Shinyoung Lee, et al. Improving generative behavior cloning via self-guidance and adaptive chunking. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 1 

- [36] Haoming Song, Delin Qu, Yuanqi Yao, Qizhi Chen, Qi Lv, Yiwen Tang, Modi Shi, Guanghui Ren, Maoqing Yao, et al. Hume: Introducing system-2 thinking in visual-languageaction model. _arXiv preprint arXiv:2505.21432_ , 2025. 2 

- [37] Wenxuan Song, Jiayi Chen, Pengxiang Ding, Han Zhao, Wei Zhao, Zhide Zhong, Zongyuan Ge, Jun Ma, and Haoang Li. Accelerating vision-language-action model integrated with action chunking via parallel decoding. _arXiv preprint arXiv:2503.02310_ , 2025. 2 

- [38] Dequan Wang, Evan Shelhamer, Shaoteng Liu, Bruno Olshausen, and Trevor Darrell. Tent: Fully test-time adaptation by entropy minimization. In _International Conference on Learning Representations_ , 2021. 3 

- [39] Yihao Wang, Pengxiang Ding, Lingxiao Li, Can Cui, Zirui Ge, Xinyang Tong, Wenxuan Song, Han Zhao, Wei Zhao, Pengxu Hou, et al. VLA-Adapter: An effective paradigm for tiny-scale vision-language-action model. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , 2026. 1 

- [40] Shoukai Xu, Zihao Lian, Mingkui Tan, Liu Liu, Zhong Zhang, and Peilin Zhao. Test-time adapted reinforcement learning with action entropy regularization. In _International Conference on Machine Learning_ , 2025. 3 

- [41] Jiawen Yu, Hairuo Liu, Qiaojun Yu, Jieji Ren, Ce Hao, Haitong Ding, Guangyu Huang, Guofan Huang, Yan Song, Panpan Cai, Wenqiang Zhang, and Cewu Lu. ForceVLA: Enhancing VLA models with a force-aware MoE for contactrich manipulation. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 1 

- [42] Tianyuan Yuan, Yicheng Liu, Chenhao Lu, Zhuoguang Chen, Tao Jiang, and Hang Zhao. DepthVLA: Enhancing vision-language-action models with depth-aware spatial reasoning. _arXiv preprint arXiv:2510.13375_ , 2025. 1 

- [43] Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 3D diffusion policy: Generalizable visuomotor policy learning via simple 3D representations. In _ICRA 2024 Workshop on 3D Visual Representations for Robot Manipulation_ , 2024. 1 

- [44] Jiahui Zhang, Yurui Chen, Yueming Xu, Ze Huang, Yanpeng Zhou, Yu-Jie Yuan, Xinyue Cai, Guowei Huang, Xingyue Quan, Hang Xu, et al. 4D-VLA: Spatiotemporal visionlanguage-action pretraining with cross-scene calibration. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 1 

- [45] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, et al. CoT-VLA: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025. 2 

- [46] Tony Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _Robotics: Science and Systems XIX_ , 2023. 1, 2 

- [47] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3DVLA: A 3D vision-language-action generative world model. In _International Conference on Machine Learning_ , 2024. 1 

- [48] Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, Yuchun Feng, Yinan Zheng, Jiayin Zou, Yilun Chen, Jia Zeng, et al. X-VLA: Soft-prompted Transformer as scalable cross-embodiment vision-language-action model. _arXiv preprint arXiv:2510.10274_ , 2025. 2 

- [49] Yifan Zhong, Xuchuan Huang, Ruochong Li, Ceyao Zhang, Zhang Chen, Tianrui Guan, Fanlian Zeng, Ka Nam Lui, Yuyao Ye, Yitao Liang, et al. DexGraspVLA: A vision-language-action framework towards general dexterous grasping. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , 2026. 2 

- [50] Xueyang Zhou, Yangming Xu, Guiyao Tie, Yongchao Chen, Guowen Zhang, Duanfeng Chu, Pan Zhou, and Lichao Sun. LIBERO-PRO: Towards robust and fair evaluation of vision-language-action models beyond memorization. _arXiv preprint arXiv:2510.03827_ , 2025. 6, 7 

- [51] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. RT-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , 2023. 2 

# **Adaptive Action Chunking at Inference-time for Vision-Language-Action Models** 

# Supplementary Material 

## **A. Minimum Action Magnitude** 

To further guarantee temporal consistency and computational efficiency, we impose a minimum action magnitude constraint on the optimal action chunk size, thereby defining a dynamic threshold _ξ_ in Eq. (6): 


where the action magnitude _m_ ( _l_ ) is defined as the sum of the component magnitudes of translation _mt_ , rotation _mr_ , and gripper motion _mg_ , as illustrated in Eq. (7). The parameter _α_ denotes the minimum movement energy of the robot arm, which we set to 3 in our experiments. 


Specifically, the translational action magnitude is defined as the Euclidean norm of the translation vector from the start point of an action chunk to the end point of a selected chunk size _l_ , as illustrated in Eq. (8). The rotational action magnitude is obtained by accumulating the rotational offsets through sequential quaternion composition, as shown in Eq. (9). For the gripper action magnitude, we set it to 1 when the gripper state changes (e.g., from open to closed or vice versa), and to 0 otherwise, as presented in Eq. (10). Here, **1** denotes an indicator function that returns 1 if the condition is satisfied and 0 otherwise. 


Table 6. Success rates (%) on RoboCasa. 

|Task Group|Task Name|GR00T|GR00T + AAC|
|---|---|---|---|
||Counter to Cab|57.0|59.0|
||Counter to Stove|41.0|40.0|
||Sink to Counter|46.0|52.0|
||Stove to Counter|60.0|63.0|
|Relocation|Counter to Sink|26.0|28.0|
||Counter to Microwave|33.0|30.0|
||Cab to Counter|26.0|25.0|
||Microwave to Counter|27.0|36.0|
||Coffee Setup Mug|38.0|39.0|
||Coffee Serve Mug|67.0|72.0|
||Open Single Door|62.0|73.0|
||Close Single Door|94.0|92.0|
|Cti|Close Double Door|56.0|62.0|
|onaner|Open Double Door|89.0|88.0|
||Open Drawer|81.0|80.0|
||Close Drawer|100.0|98.0|
||Turn Sink Spout|69.0|66.0|
||Turn on Sink facet|85.0|91.0|
|Rotation|Turn off Sink Facet|74.0|80.0|
||Turn on Stove|39.0|49.0|
||Turn off Stove|21.0|21.0|
||Coffee Press Button|94.0|93.0|
|Button|Turn on Microwave|66.0|68.0|
||Turn off Microwave|81.0|83.0|
||Relocation Average|42.1|44.4|
||Container Average|80.3|82.2|
||Rotation Average|57.6|61.4|
||Button Average|80.3|81.3|
||24 Tasks Average|59.7|62.0|


## **B. Complete Experiment Results in RoboCasa** 

The complete experimental results for all 24 tasks in RoboCasa are presented in Tab. 6 and Tab. 7. On average, AAC demonstrates the best overall performance across these tasks. Nevertheless, there remains room for improvement in optimizing the chunk size selection for future work, as the optimal performance for each task has not yet been fully achieved. 

Table 7. Success rates (%) with Different Chunk Sizes. 

|Task Group|Task Name|Fixed-2|Fixed-4|Fixed-8|Fixed-12|Fixed-16|
|---|---|---|---|---|---|---|
||Counter to Cab|51.0|68.0|61.0|57.0|57.0|
||Counter to Stove|31.0|40.0|46.0|45.0|41.0|
||Sink to Counter|35.0|44.0|56.0|50.0|46.0|
|Rltin|Stove to Counter|59.0|62.0|69.0|64.0|60.0|
|eocao|Counter to Sink|6.0|10.0|15.0|19.0|26.0|
||Counter to Microwave|7.0|12.0|29.0|23.0|33.0|
||Cab to Counter|18.0|18.0|23.0|23.0|26.0|
||Microwave to Counter|27.0|42.0|28.0|36.0|27.0|
||Coffee Setup Mug|31.0|39.0|40.0|46.0|38.0|
||Coffee Serve Mug|31.0|44.0|61.0|66.0|67.0|
||Open Single Door|15.0|41.0|61.0|62.0|62.0|
||Close Single Door|84.0|89.0|87.0|95.0|94.0|
||Close Double Door|53.0|62.0|73.0|58.0|56.0|
|Container|Open Double Door|44.0|73.0|81.0|84.0|89.0|
||Open Drawer|51.0|64.0|81.0|79.0|81.0|
||Close Drawer|95.0|99.0|99.0|99.0|100.0|
||Turn Sink Spout|70.0|69.0|69.0|67.0|69.0|
||Turn on Sink facet|84.0|87.0|85.0|83.0|85.0|
|Rotation|Turn off Sink Facet|82.0|78.0|85.0|80.0|74.0|
||Turn on Stove|42.0|52.0|52.0|47.0|39.0|
||Turn off Stove|19.0|20.0|22.0|23.0|21.0|
||Coffee Press Button|76.0|89.0|98.0|98.0|94.0|
|Button|Turn on Microwave|47.0|51.0|61.0|60.0|66.0|
||Turn off Microwave|71.0|96.0|86.0|80.0|81.0|
||Relocation Average|29.6|37.9|42.8|42.9|42.1|
||Container Average|57.0|71.3|80.3|79.5|80.3|
||Rotation Average|59.4|61.2|62.6|60.0|57.6|
||Button Average|64.7|78.7|81.7|79.3|80.3|
||24 Tasks Average|47.0|56.2|61.2|60.2|59.7|


