---
title: "AVA-VLA: Improving Vision-Language-Action models with Active Visual Attention"
date: "2025-11-24"
authors: "Lei Xiao; Jifeng Li; Juntao Gao; Feiyang Ye; Yan Jin; Jingjing Qian"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2511.18960
pdf: https://arxiv.org/pdf/2511.18960
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.18960)** / [論文ページ](https://arxiv.org/abs/2511.18960)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **AVA-VLA: Improving Vision-Language-Action models with Active Visual Attention** 

Lei Xiao<sup>1,</sup><sup>_∗_</sup> Jifeng Li<sup>1,*</sup> Juntao Gao<sup>1,2</sup> Feiyang Ye<sup>1,†</sup> Yan Jin<sup>1</sup> Jingjing Qian<sup>3</sup> Jing Zhang<sup>2</sup> Yong Wu<sup>1</sup> Xiaoyuan Yu<sup>1,</sup><sup>_†_</sup> 

1LiAuto Inc. 2Beijing University of Technology 3The Chinese University of Hong Kong, Shenzhen 

## **Abstract** 

_Vision-Language-Action (VLA) models have shown remarkable progress in embodied tasks recently, but most methods process visual observations independently at each timestep. This history-agnostic design treats robot manipulation as a Markov Decision Process, even though realworld robotic control is inherently partially observable and requires reasoning over past interactions. To address this mismatch, we reformulate VLA policy learning from a Partially Observable Markov Decision Process perspective and propose AVA-VLA, a framework that conditions action generation on a recurrent state that serves as a neural approximation to the agent’s belief over task history. Built on this recurrent state, we introduce Active Visual Attention (AVA), which dynamically reweights visual tokens in the current observation to focus on regions most relevant given both the instruction and execution history. Extensive experiments show that AVA-VLA achieves state-of-the-art performance on standard robotic benchmarks, including LIBERO and CALVIN, and transfers effectively to real-world dualarm manipulation tasks. These results demonstrate the effectiveness of temporally grounded active visual processing for improving VLA performance in robotic sequential decision-making. The project page is available at https: //liauto-dsr.github.io/AVA-VLA-Page._ 

## **1. Introduction** 

Recent advances in robotic manipulation have demonstrated impressive progress in training robot action policies that can act across diverse real-world tasks. One transformative paradigm is Vision-Language-Action (VLA) models [2– 4, 7, 19, 22, 36, 65], which integrate visual perception, natural language understanding, and action generation within a unified neural architecture. These models, which are capable of instruction following and robotic action generation, 

> *Equal contribution. 

> †Corresponding author. 


Figure 1. (a) Visualized comparison of the proposed AVA-VLA framework and vanilla VLAs. (b) Qualitative comparison of visual focus from two viewpoints while executing the task “turn on the stove and put the moka pot on it.” The vanilla OpenVLAOFT [20] baseline fails to locate the task-critical “stove” switch, whereas AVA-VLA exhibits more stable focus by leveraging historical context. 

exhibit strong understanding and generalization abilities after being fine-tuned for downstream scenarios. 

To adopt the ability to understand diverse scenes, objects, and language instructions, most VLA models are built upon pretrained Vision-Language Models (VLMs) [9, 18, 29]. Such models typically extend VLM architectures with modules such as action tokenization [19, 45] or specialized action experts [22, 57] to enable action-oriented outputs. Based on this architectural inheritance, these VLA models typically process visual inputs as isolated temporal frames, treating each frame independently. This implicitly formulates robot manipulation as a Markov Decision Process (MDP) [16, 31], where actions are generated from the current visual observation, assumed to represent the complete world state. In realistic robotic manipulation, how- 

13453 

ever, the current visual frame is only a partial observation of the environment state. This full state includes unobservable dynamics across time, such as internal states and occluded information. By discarding the rich context from the past, this MDP-based approach is suboptimal for the dynamic sequential decision-making required in robotic manipulation. 

This limitation of the MDP-based assumption has significant impacts on VLA models, particularly for the model’s visual processing capabilities. VLA modeling is essentially a dynamic feedback control problem, where each preceding action directly alters the current visual input. However, by processing frames in isolation, the visual attention weights, guided by the static language instruction, are forced to reevaluate the independent visual information from scratch at each decision step. Without global context, the model cannot effectively suppress temporally redundant information and focus on regions made important by past actions. As a result, the visual system remains passive rather than active. In fact, the inability to anticipate perceptual intent a priori makes active visual modules difficult to realize in computer vision. However, the sequential dynamics of decision-making create an opportunity for active visual perception. Recognizing the limitations of processing frames in isolation, some recent methods [24, 52, 58] have begun to leverage historical information, such as frame comparison results and KV-cache reuse, for efficient visual token processing [8, 62]. However, these approaches mainly focus on visual token pruning for efficiency. Therefore, designing a dynamic, context-aware visual processing paradigm that improves both visual processing and VLA generalization remains a significant challenge. 

To address this challenge, we propose AVA-VLA, inspired by the Partially Observable Markov Decision Process (POMDP) framework [21, 44]. We observe that the core challenge identified above is similar to the POMDP challenge of forming a robust belief state, which functions as a summary of past observations and actions to guide decisionmaking under uncertainty. Since directly computing or representing the belief state is generally intractable, we introduce a recurrent state, which functions as a neural approximation of this belief state and is calculated by the intermediate output of the model in the previous time step. Then, we design an Active Visual Attention (AVA) module to leverage this recurrent state to calculate the importance of visual tokens and dynamically modulating the visual processing of the current frame. This allows the model to filter and focus its attention based on its historical belief, rather than purely static language instruction. Therefore, the proposed AVA-VLA framework does not rely solely on the current observation but learns to explicitly condition the action prediction on the recurrent state. 

Through extensive experiments in both simulation benchmarks [11, 28, 31] and real-world tasks [5], we 

demonstrate that our proposed active visual attention module helps improve policy performance compared to previous VLA frameworks. Our contributions are threefold: 

- We propose the novel AVA-VLA framework to solve the critical limitation of lacking historical context in MDPbased VLA models. To our knowledge, it is the first VLA framework to explicitly address this limitation via a POMDP-inspired approach. 

- We introduce an Active Visual Attention (AVA) module that leverages the recurrent state to dynamically modulate the visual processing of the current frame for action prediction. 

- We conduct comprehensive evaluations in both simulation and real-world tasks, demonstrating that the AVAVLA framework improves VLA performance, and our method achieves state-of-the-art performance across multiple robot tasks. 

## **2. Related Work** 

**Vision-Language-Action Models.** VLMs [9, 18, 29, 42] have been pivotal in advancing robotic control by providing rich multi-modal representations. This has fostered the development of VLA models [2–4, 7, 19, 22, 36, 37, 46, 65] that bridge high-level perception with low-level action generation. A significant paradigm shift was the introduction of action tokenization by the RT series [1, 4, 65]. This approach treats control as a sequence modeling problem, enabling scalable web-to-robot transfer. Models like OpenVLA [19] and UniVLA [5] generate action policies in the autoregressive (AR) manner. While expressive, the sequential nature of AR decoding is computationally intensive. Therefore, recent research has diversified into more efficient and effective action decoding strategies. Models such as CogACT [22] and the _π_ series [3, 36], have explored diffusion-based decoders for the iterative refinement of continuous action trajectories. Other recent works, such as OpenVLA-OFT [20] and its variant [23], employ parallel decoding, which enables the simultaneous prediction of actions within the action chunk, improving inference efficiency and supporting scalable deployment. 

**Sequential Processing in VLMs.** Many VLM studies [10, 33, 38, 53] focus on processing sequential visual data for tasks such as video understanding and temporal-based video questions. These works efficiently aggregate historical information, allowing the model to build a holistic, temporal-aware representation of the video’s content. VLM-3R [10] employs a geometry encoder to derive implicit 3D tokens that represent spatial-temporal understanding. [53] incrementally updates a persistent internal state that encodes the scene content. These VLM models use history for passive comprehension or offline understanding. In contrast, VLA models operate in an active, dynamic decision-making environment, which requires the model to 

13454 

interact with the environment. This distinction motivates our POMDP-inspired approach, which focuses on maintaining a recurrent state for active decision-making. 

## **3. Methods** 

In this section, we present our proposed VLA method. We begin with the preliminaries (3.1), followed by the AVAVLA framework (3.2) and the detailed description of the proposed Active Visual Attention module (3.3). We then explain our training and inference procedures (3.4). An overview of the proposed AVA-VLA framework is shown in Figure 2. 

### **3.1. Preliminaries** 

A typical VLA model _Pθ_ , parameterized by _θ_ , consists of four main components: a Large-Language-Model (LLM) backbone _M_ , a vision encoder _E_ , a language tokenizer _T_ , and an action head (or de-tokenizer) _Q_ . We thus define the model as _P_ = _{M, E, T , Q}_ . 

Following the representative OpenVLA [19], at timestep _t_ , given an input tuple **_x_**<sup>_t_</sup> = ( **_x_**<sup>_t_</sup> _I_<sup>_,_</sup><sup>**_x_**</sup><sup>_t_</sup> _S_<sup>),thevisualencoder</sup> _E_ first encodes the input image **_x_**<sup>_t_</sup> _I_<sup>intoL</sup><sup>_I_visualtokens:</sup> **_z_**<sup>_t_</sup> _I_<sup>=</sup><sup>_E_(</sup><sup>**_x_**</sup><sup>_t_</sup> _I_<sup>)</sup><sup>_∈_RL</sup><sup>_I×d_, where</sup><sup>_d_denotes the embedding di-</sup> mension. These visual tokens are then concatenated with L<sup>_t_</sup> _S_<sup>languagetokens,</sup><sup>**_z_**</sup><sup>_t_</sup> _S_<sup>=</sup><sup>_T_(</sup><sup>**_x_**</sup><sup>_t_</sup> _S_<sup>)</sup><sup>_∈_RL</sup> _S_<sup>_t×d_</sup> . The combined sequence is then fed into the LLM backbone _M_ to generate output hidden states **_h_**<sup>_t_</sup> . Finally, the action head _Q_ maps the output hidden states **_h_**<sup>_t_</sup> into a _D_ -dimensional executable action _A_<sup>_t_</sup> for robotic control (e.g., _D_ = 7 for 3-DoF translation, 3-DoF rotation, and binary gripper control). Thus, the entire forward pass at timestep _t_ can be formulated as: 


Recent representative VLA models, such as OpenVLAOFT [20] and its variant [23], map the output hidden states into an executable action chunk _A_<sup>_t_</sup> = [ _a_<sup>_t_</sup> 0<sup>_, a_</sup> 1<sup>_t, ..., at_</sup> L _c−_ 1<sup>]</sup><sup>_∈_</sup> R<sup>L</sup><sup>_c×D_</sup> , where L _c_ and _D_ represent the length of the action chunk and the dimensionality of each atomic action, respectively. To facilitate parallel generation, a learnable action placeholder embedding **_p_**<sup>_t_</sup> is appended to the input sequence [23, 27]. This placeholder embedding is set to empty in OpenVLA-OFT, i.e., **_p_**<sup>_t_</sup> = **0** ¯ = [ **0** 0 _,_ **0** 1 _, ...,_ **0** L _c−_ 1] _∈_ R<sup>L</sup><sup>_c×D×d_</sup> . The corresponding forward pass under parallel decoding at timestep _t_ can thus be expressed as: 


Regardless of whether AR or parallel decoding is used, these VLA models learn to predict the action _A_<sup>¯</sup><sup>_t_</sup> only from the current observation **_x_**<sup>_t_</sup> . This implicitly models the task 

as a Markov decision process: 


### **3.2. AVA-VLA Framework** 

The history-agnostic design for policy learning in Eq. (3) is suboptimal for effective visual token processing in dynamic sequential decision-making [21, 61], as it fails to capture non-observable dynamics or occluded information. This limitation inspired us to re-formulate the VLA model from a POMDP perspective. In a POMDP framework, the optimal policy at timestep _t_ should be conditioned not only on the current observation **_x_**<sup>_t_</sup> but also on a belief state _b_<sup>_t−_1</sup> , which captures all relevant historical context, including observations and actions, i.e., _b_<sup>_t−_1</sup> = _P_ ( _st−_ 1 _|_ **_x_**<sup>_<t_</sup> _, A_<sup>_<t_</sup> ). Inspired by this theoretical framework, we re-formulate the VLA policy as 


This formulation provides a theoretical foundation for designing a more effective visual processing paradigm, suggesting that leveraging historical context in observations can improve VLA generalization. Since computing the theoretical belief state _b_<sup>_t−_1</sup> is generally intractable, we instead propose to learn a compressed representation, **_r_**<sup>_t−_1</sup> , as its neural approximation. This approach naturally transforms the VLA model into a recurrent structure [30], leading to a non-Markovian policy conditioned on this learned representation: _A_<sup>¯</sup><sup>_t_</sup> _∼Pθ_ ( _A_<sup>_t_</sup> _|_ **_x_**<sup>_t_</sup> _,_ **_r_**<sup>_t−_1</sup> ). 

In our proposed AVA-VLA framework, we term this approximate vector **_r_**<sup>_t−_1</sup> the recurrent state, which captures historical context. In typical VLA models, the hidden states immediately preceding action generation contain fused visual and language information and are predictive of the agent’s intent. Therefore, we derive the recurrent state for timestep _t_ from the action-related hidden state at timestep _t −_ 1. 

Specifically, for a parallel-decoding-based VLA model, which contains _M_ decoder layers that predict L _A_ = L _cD_ actions in one forward pass, we denote its hidden states output at the _m_ -th layer and time _t_ by _h_<sup>_t_</sup> _m_<sup>_∈_RL</sup><sup>_A×d_.The</sup> corresponding recurrent state is computed by: 


where _B_ is an MLP module that transforms the hidden state into the recurrent state. 

We employ this recurrent state to guide the VLA model to actively focus on visual regions that become critical along the time sequence. To utilize the recurrent state, we introduce the active visual attention module by quantifying the importance of visual tokens and dynamically modulating the processing of the visual frame for the current timestep. 

13455 


Figure 2. Overview of the proposed AVA-VLA framework. At each timestep, the recurrent state is projected from the previous hidden state to preserve historical context and to initialize the current action tokens. Then the AVA module combines this recurrent state with textconditioned visual features from the current observation to generate soft importance scores, which modulate the visual attention matrices throughout the backbone LLM, enabling the model to focus on task-relevant regions based on both temporal context and current perception. 

Moreover, in order to preserve the rich historical information, we use this recurrent state **_r_**<sup>_t−_1</sup> for action placeholder [20, 23] embedding initialization, i.e., **_p_**<sup>_t_</sup> = **_r_**<sup>_t−_1</sup> . 

For simplicity, our framework is built upon the OpenVLA-OFT foundation model. Therefore, the forward pass at timestep _t_ , incorporating the AVA module and statebased initialization, is formulated as: 


where _V_ is the proposed AVA module, which takes the current observations and the recurrent state as input. 

### **3.3. Active Visual Attention** 

We now describe the detailed architecture of the AVA module _V_ , which is designed to modulate visual processing in a dynamic manner. 

The AVA module first employs modality-specific MLPs to encode the visual features **_z_**<sup>_t_</sup> _I_<sup>andtheinstructionfea-</sup> ture **_z_**<sup>_t_</sup> _S_<sup>into</sup><sup>**_z_**¯</sup> _I_<sup>_t∈_RL</sup><sup>_I×d′_and</sup><sup>**_z_**¯</sup><sup>_t_</sup> _S_<sup>_∈_RL</sup> _S_<sup>_t×d′_</sup> , respectively, where _d_<sup>_′_</sup> _< d_ . A feature-wise linear modulation (FiLM) [35] is applied to condition the visual features on the language instruction, i.e., ˆ **_z_**<sup>_t_</sup> _I_<sup>=</sup><sup>_Fγ_(¯</sup><sup>**_z_**</sup> _S_<sup>_t_)</sup><sup>_⊙_</sup><sup>**_z_**¯</sup> _I_<sup>_t_+</sup><sup>_Fβ_(¯</sup><sup>**_z_**</sup><sup>_t_</sup> _S_<sup>).Then</sup> it uses the visual tokens ˆ **_z_**<sup>_t_</sup> _I_<sup>as the query,</sup> 


and the recurrent state as the key and value 


where _WQ_ , _WK_ , _WV_ are linear projection layers, and **_r_** ˆ<sup>_t−_1</sup> _∈_ R<sup>L</sup><sup>_A×d′_</sup> is the output of **_r_**<sup>_t−_1</sup> after MLP encoding. Then it computes the attention matrix and feeds the output into a self-attention layer 


Inspired by [40, 47], we feed the resulting tokens **O**<sup>_t_</sup> _∈_ R<sup>L</sup><sup>_I×d′_</sup> into a Feedforward Neural Network (FFN), a linear layer _W_ : R<sup>_d′_</sup> _→_ R<sup>2</sup> , and apply a Softmax function along the feature dimension. This predicts the logits for enhancing or weakening each visual token as: 


Then we compute the final soft weights for visual tokens at time _t_ by **_ω_**<sup>_t_</sup> = **_ρ_**<sup>_t_</sup> **_γ_** , where **_γ_** is a 2-dimensional vector. These soft weights directly represent the importance scores of the visual tokens. The components of **_γ_** , _γ_ 0 and _γ_ 1, represent the scalar scores for enhancing and weakening a visual token, respectively. 

The soft weights vector **_ω_**<sup>_t_</sup> is applied to all layers of the LLM backbone. Specifically, at time step _t_ , let the total sequence length be L<sup>_t_</sup> _o_<sup>, we denote the attention score of the</sup><sup>_m_-</sup> th layer by **C**<sup>_t,m_</sup> _∈_ R<sup>L</sup> _o_<sup>_t×_L</sup><sup>_t_</sup> _o_ , which is calculated by applying the original attention mask to the raw attention scores. The final attention matrix of the _m_ -th layer **A**<sup>_t,m_</sup> is calculated by applying the soft attention mask matrix **U**<sup>_t_</sup> with the 

13456 

_Softmax_ operation to **C**<sup>_t,m_</sup> : 


where the soft attention matrix **U**<sup>_t_</sup> is constructed based on the soft weights vector **_ω_**<sup>_t_</sup> : 


where the set Λ _I_ represents the indices of the visual tokens. Therefore, the proposed AVA module uses the recurrent state and current visual observation to calculate soft weights to guide the VLA model to filter and focus its attention based on historical information. 

### **3.4. Training and Inference Procedure** 

The proposed AVA-VLA framework introduces a recurrent dependency through the recurrent state **_r_**<sup>_t−_1</sup> . Training such a recurrent model ideally requires backpropagation through time over the entire trajectory to capture long-term dependencies. However, given the substantial memory constraint and computational cost of modern VLA backbones, performing the full backpropagation through time is computationally prohibitive [34]. 

To address this challenge, we adopt a truncated backpropagation through time strategy [25]. We unroll the model for a fixed, short horizon. Specifically, for the _n_ -th sample in the training batch, it contains a continuous observation sequence _{_ **_x_**<sup>_t,n_</sup> _}_<sup>_T_</sup> _t_ =0<sup>_−_1.For each timestep</sup><sup>_t_in this se-</sup> quence, we calculate the action chunk prediction loss using the Mean Absolute Error (MAE): _L_<sup>_t,n_</sup> = _L_ ( _A_<sup>_t,n_</sup> _, A_<sup>_t,n_</sup> GT<sup>). To</sup> prevent overly dispersed soft attention weights, we add an L2 penalty regularizer _L_<sup>_t,n_</sup> _ω_ on the mean value of the weight vector **_ω_**<sup>_t,n_</sup> , defined as: 


where _µ_ ( _·_ ) is the mean function and _c_ is a target mean hyperparameter. This encourages the AVA module to focus on task-relevant regions while suppressing distracting background responses ( _see Appendix D for more analysis_ ). 

Therefore, the total loss of one training batch is the sum of the prediction loss and penalty loss of _N_ truncated sequences: 


where _N_ is the batch size, and _λ_ is a balancing coefficient. In our experiments, we set _T_ = 4 to balance computational feasibility with the need to learn the temporal dynamics captured by the recurrent state. At the first timestep ( _t_ = 0) of 

any sequence, the initial recurrent state **_r_**<sup>_−_1</sup> is initialized as a zero embedding, i.e., **_r_**<sup>_−_1</sup> = **0**<sup>¯</sup> . 

During inference, the model operates in a fully recurrent manner. At the beginning of a new episode ( _t_ = 0), the initial recurrent state **_r_**<sup>_−_1</sup> is initialized as the zero embedding. Then, for each subsequent timestep _t ≥_ 0, the agent receives the current observation **_x_**<sup>_t_</sup> and performs a single forward pass as defined in Eq. (6), conditioned on both **_x_**<sup>_t_</sup> and the previously computed recurrent state **_r_**<sup>_t−_1</sup> . This forward pass predicts the action chunk _A_<sup>_t_</sup> and simultaneously extracts the recurrent state **_r_**<sup>_t_</sup> . This loop continues for the entire inference process. 

**Remark.** We explicitly note that the soft weights vector **_ω_**<sup>_t_</sup> computed by the AVA module has a natural application in visual token reduction [24, 54]. Visual tokens with low importance scores can be pruned to reduce the computational cost of the LLM backbone. While this is a valid direction for improving model efficiency, it is not the primary focus of this work. We provide a preliminary exploratory analysis on leveraging the weight vector to do token reduction, which further validates the effectiveness of our proposed method. Details can be found in Section 4.4. 

## **4. Experiments** 

We evaluate the effectiveness of our approach through a set of experiments spanning both simulation benchmarks and real-world robot manipulation tasks. Additionally, we conduct a comprehensive ablation study and analysis to validate the effectiveness of our approach. All experiments are conducted on Nvidia A800 GPUs. 

### **4.1. Experimental Setup** 

We conduct experiments on three challenging settings: the LIBERO [28] and CALVIN [31] benchmarks for evaluation in simulation environments, and a real-world tablemounted Mobile ALOHA robot with four test tasks, to validate the sim-to-real transferability of our method. We use the open-source OpenVLA-OFT [20] as our foundation model, which consists of a two-branch vision encoder (DINOv2 and SigLIP) and a LLaMA2-7B backbone [51]. _Due to space limitations, implementation details are provided in Appendix A._ 

**LIBERO.** LIBERO [28] is a benchmark for lifelong robot learning. It uses a Franka Emika Panda arm in MuJoCo, with datasets split into four suites: LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, and LIBERO-Long. It contains 5,000 episodes across 100 tasks. Data includes RGB images, proprioceptive states, and delta actions, with procedural generation for diversity. _LIBERO+ [11] is a challenging LIBERO-based benchmark, which offers a robust benchmarking framework with 7 perturbation dimensions and 21 sub-dimensions. It allows users to assess model performance across various challenges systemati-_ 

13457 

Table 1. Comparison on the LIBERO benchmark. The results are reported in two groups: one policy for all 4 suites, and one policy per suite. The best results in each column of each group are highlighted in **bold** . 

|Method|Spatial SR (%)|Object SR (%)|Goal SR (%)|Long SR (%)|Average SR (%)|
|---|---|---|---|---|---|
|||_One policy for al_<br>|_l 4 suites_<br>|||
|TraceVLA [64]|84.6|85.2|75.1|54.1|74.8|
|WorldVLA [6]|87.6|96.2|83.4|60.0|81.8|
|_π_0[3]|96.8|98.8|95.8|85.2|94.2|
|_π_0-FAST [36]|96.4|96.8|88.6|60.2|85.5|
|UnifiedVLA [56]|95.4|98.8|93.6|94.0|95.5|
|OpenVLA-OFT [20]|**97.7**|98.0|96.1|95.3|96.8|
|AVA-VLA (Ours)|97.4|**99.4**|**97.4**|**97.6**|**98.0**|
|||_One policy per_|_suite_|||
|OpenVLA [19]|84.7|88.4|79.2|53.7|76.5|
|SpatialVLA [39]|88.2|89.9|78.6|55.5|78.1|
|CoT-VLA [63]|87.5|91.6|87.6|69.0|83.9|
|NORA [15]|92.2|95.4|89.4|74.6|87.9|
|PD-VLA [45]|95.5|96.7|94.9|91.7|94.7|
|UniVLA [5]|96.5|96.8|95.6|92.0|95.2|
|OpenVLA-OFT [20]|97.6|98.4|97.9|94.5|97.1|
|FLOWER [41]|97.5|99.1|96.1|94.9|96.9|
|RIPT-VLA [48]|99.0|98.6|**98.6**|93.8|97.5|
|AVA-VLA (Ours)|**99.2**|**99.6**|97.9|**96.2**|**98.2**|


_cally. We conduct additional experiments on the LIBERO+ benchmark, and the results are put in Appendix D._ 

**CALVIN.** CALVIN [31] is a simulated benchmark for language-conditioned, long-horizon manipulation, using a Franka Panda arm with RGBD observations, proprioception, and natural language goals. It evaluates sequential reasoning in VLA. CALVIN spans 34 tasks across four environments (A-D), with 20,000+ episodes, emphasizing unseen object generalization and multi-stage sequences (e.g., “open drawer, pick blue block, push into drawer”). Following [5], we used the CALVIN “ABC _→_ D” setting, which means training on environments A, B, and C and evaluating on environment D, to evaluate performance on the zero-shot generalization tasks. 

**Mobile ALOHA Real-Robot Experiments.** We use a stationary cobot magic dual-arm robot to assess our model’s adaptability to novel real-world environments with a small number of robot demonstrations. Following [5, 63], we perform evaluations across four challenging tasks. These include Pick and Place, which involves placing the bucket in the center, and then placing irregular-shaped objects into the bucket (e.g., “put _<_ obj _>_ into bucket”), and Sequenced Instruction Understanding, which requires executing multistep commands like stacking a Tower of Hanoi (“Stack tower of hanoi”). We also test Flexible Object Folding, a deformable object manipulation task requiring a specific three-stage process to fold a towel (“fold towel twice”), and Dexterous Action, which involves fine-motor skills such as using a shovel to scoop small items (e.g., corn, sesame seeds) into a bowl. For each task, the dataset contains be- 

Table 2. Comparison on the CALVIN ABC _→_ D benchmark. The results are reported in terms of success rates (%) and average length. The best results in each column are highlighted in **bold** . 

|CALVIN<br>ABC_→_D|T<br>1|ask com<br>2|pleted<br>3|in a row<br>4|_↑_<br>5|Avg. len<br>_↑_|
|---|---|---|---|---|---|---|
|OpenVLA [19]|91.3|77.8|62.0|52.1|43.5|3.27|
|UniVLA [5]|95.5|85.8|75.4|66.9|56.5|3.80|
|UnifiedVLA [56]|98.9|94.8|89.0|82.8|75.1|4.41|
|OpenVLA-OFT [20]|96.9|92.0|85.7|80.4|72.9|4.28|
|FLOWER [41]|99.4|95.8|90.7|84.9|77.8|4.53|
|VLA-Adapter [55]|99.1|94.6|88.8|82.8|76.5|4.42|
|Seer [50]|96.3|91.6|86.1|80.3|74.0|4.28|
|AVA-VLA (Ours)|**99.6**|**97.6**|**94.1**|**89.9**|**84.1**|**4.65**|


tween 30 and 450 demonstrations. _Details of the task suites are provided in Appendix B._ 

### **4.2. Evaluation Results** 

**Baselines.** We selected recently published works’ main method as baselines. They are TraceVLA [64], WorldVLA [6], _π_ 0 [3], _π_ 0-FAST [36], UnifiedVLA [56], OpenVLAOFT [20], OpenVLA [19], SpatialVLA [39], CoT-VLA [63], NORA [15], PD-VLA [45], UniVLA [5], OpenVLAOFT [20], FLOWER [41], RIPT-VLA [48], VLA-Adapter [55], Seer [50]. The results of these baselines in LIBERO and CALVIN benchmarks are based on original references or other published works, ensuring objectivity and correctness. For Mobile ALOHA real-robot experiments, we select UniVLA and OpenVLA-OFT methods as baselines. **Evaluation Metrics.** We use widely adopted performance evaluation metrics “Success Rate (SR)” (the same 

13458 


Figure 3. Comparison on the Mobile ALOHA real-world experiments. Evaluation across four manipulation tasks, including (a) Pick and Place, (b) Sequenced Instruction Understanding, (c) Flexible Object Folding, (d) Dexterous Action. Left: Representative middle states for each task setup. Right: Task-specific success rates and cross-task averages for our method and baselines. 

in LIBERO [28]) to evaluate the results for three challenging settings. In addition, we use “Average len” of completed tasks (the larger the better, with values between 0-5) as metrics for the CALVIN benchmark. 

**LIBERO.** We present quantitative results in Table 1. Following established baselines, we conduct experiments in two different settings: training policies on each task suite independently (single-task learning) and training a single policy for all task suites (multi-task learning [26]). Results demonstrate that the proposed AVA-VLA framework achieves state-of-the-art overall performance in both singletask and multi-task settings. Moreover, it consistently achieves the best performance on the most challenging LIBERO-Long task suite. These results demonstrate the superiority of the proposed AVA-VLA framework. 

**CALVIN.** We present the success rates for each task and the average completed length across all five tasks of the CALVIN benchmark in Table 2. The results show that the proposed AVA-VLA framework comprehensively outperforms baseline methods across all tasks. This demonstrates our method’s strong generalization ability, with an average length superior to previous state-of-the-art baselines. 

**Mobile ALOHA.** The Pick and Place task is evaluated for a total of 30 trials (10 per object), while other tasks are evaluated for 24 trials each. The experimental results on realworld tasks are reported in Figure 3. In this setting, models are fine-tuned on a relatively small set of demonstrations. The results demonstrate that the proposed model possesses robust semantic understanding and dexterous action capabilities after training. Overall, AVA-VLA achieves the highest average performance compared to baseline approaches, confirming its real-world applicability. _We visualize the execution trajectories for these tasks in Appendix B._ 

### **4.3. Ablation Studies** 

**Model Backbones.** To validate the effectiveness of the proposed framework, following [55], we compare three kinds of backbones: The OpenVLA-7B backbone [19] 

pre-trained on robotic data, the prismatic VLM trained on LLaMA2-7B [51], and the prismatic VLM [18] trained on Qwen2.5-0.5B [49]. The last two are different-scale backbones without pre-training on robotic data. We compare the proposed method against the standard OpenVLA-OFT method on the LIBERO-Long task suite in the single task setting. Results reported in Table 3 show that our method improves performance across different backbones, even on backbones not pre-trained on robotic datasets. 

Table 3. Ablation study on the model backbones. Comparison on the LIBERO-Long task suite in the LIBERO benchmark in terms of success rates (%). The best results of each model backbone setting are highlighted in **bold** . 

|Backbones|OpenVLA-OFT|AVA-VLA|
|---|---|---|
|OpenVLA-7B [19]|94.5|**96.2**(1.7%_↑_)|
|LLaMA2-7B [51]|90.0|**92.6**(2.6%_↑_)|
|Qwen2.5-0.5B [49]|89.4|**90.8**(1.4%_↑_)|


**AVA Module and State-Based Initialization.** The AVAVLA framework consists of two components: the statebased initialization strategy and the AVA module. To validate their individual effectiveness, we conduct ablation experiments on the LIBERO benchmark. As shown in Table 4, the two recurrent-state-driven components are complementary. State-based initialization injects the recurrent state into the action placeholder to preserve temporal context, which is especially beneficial on LIBERO-Long. The AVA module uses the recurrent state to reweight visual tokens and suppress irrelevant visual content, leading to consistent gains across suites. Each component alone improves over OpenVLA-OFT, and their combination achieves the best overall performance. 

### **4.4. Analysis** 

**Qualitative Visualization.** To investigate the AVA module’s focus during task execution, we visualize the soft weights **_ω_**<sup>_t_</sup> across visual tokens during inference. As illus- 

13459 

Table 4. Ablation study on the two key components in the AVA-VLA framework. The results on LIBERO in terms of success rates (%) under the “one policy for all 4 suites” setting are reported. The best results in each column are highlighted in **bold** . 

|Method|Spatial SR (%)|Object SR (%)|Goal SR (%)|Long SR (%)|Average SR (%)|
|---|---|---|---|---|---|
|OpenVLA-OFT|97.7|98.0|96.1|95.3|96.8|
|AVA-VLA (State-based initialization)|97.2|98.8|96.6|97.2|97.5|
|AVA-VLA (AVA module)|**97.8**|98.6|97.0|96.6|97.5|
|AVA-VLA (AVA module + State-based initialization)|97.4|**99.4**|**97.4**|**97.6**|**98.0**|


Figure 4. Visual dynamics. The evolution of soft weights during the task “put both moka pots on the stove” from two viewpoints. 

Table 5. Study on the visual token pruning with different pruning ratios. The results on LIBERO in terms of success rates (%) under the “one policy for all 4 suites” setting are reported. 

|Pruning|Spatial|Object|Goal|Long|Avg.|
|---|---|---|---|---|---|
|Ratio|SR (%)|SR (%)|SR (%)|SR (%)|SR (%)|
|0%|97.4|99.4|97.4|97.6|98.0|
|50%|97.2|99.4|97.2|95.2|97.3|
|60%|97.6|99.4|97.0|95.0|97.3|
|70%|97.4|99.2|98.0|94.6|97.3|
|80%|96.8|98.2|96.2|92.8|96.0|
|90%|94.2|97.8|94.2|89.2|93.9|


trated in Figure 4, the attention weights consistently concentrate on the robotic arm’s contact regions and the target objects. This selective focus demonstrates the module’s ability to identify task-relevant visual features, validating its effectiveness. Furthermore, a direct comparison in Figure 1 reveals that while the vanilla OpenVLA-OFT baseline fails to localize the task-relevant region across viewpoints, AVAVLA maintains a robust and spatially consistent focus by effectively leveraging historical context. 

**Visual Token Reduction.** The proposed AVA module has a potential application in visual token reduction. Although visual token pruning causes the model to lose some visual information, it reduces the model’s computational cost and is beneficial for efficient inference [17, 52, 56, 58]. To validate that our AVA module effectively prioritizes task-relevant information, we apply a direct ranking strategy to prune visual tokens during inference. Specifically, for a given pruning ratio, we rank all visual tokens by their soft weights and retain only the top-ranked portion corresponding to the desired retention percentage. The results reported in Table 5, 

demonstrate the robustness of our method: the model suffers only a negligible drop in performance after pruning. Notably, with pruning ratios of 50%, 60%, and 70%, the proposed method continues to outperform the OpenVLAOFT and maintains performance comparable to the stateof-the-art baselines reported in Table 1. The decline in success rate mainly comes from the most challenging LIBERO Long task suite, while the results remain consistent across the other task suites. Even after reducing 90% of the visual tokens, our method still outperforms many baseline methods listed in Table 1. This result further demonstrates the effectiveness of the proposed AVA-VLA framework. 

## **5. Conclusion** 

In this paper, we reformulate robot manipulation from a POMDP perspective and propose AVA-VLA, a novel vision-language-action framework for temporally grounded decision-making. Unlike prior VLA models that process each frame independently, our method introduces a recurrent state to approximate the agent’s belief, and builds an Active Visual Attention module to dynamically modulate visual processing of the current observation. In this way, AVA-VLA can actively suppress irrelevant information and focus on task-critical visual features based on historical context. Extensive experiments demonstrate the superiority of AVA-VLA, achieving state-of-the-art performance across multiple robot simulation benchmarks, including LIBERO and CALVIN, and transferring effectively to diverse realworld robotic tasks. These results highlight the value of recurrent state modeling and history-aware visual processing for robotic sequential decision-making. 

13460 

## **Acknowledgements** 

This work is supported by National Key R&D Program of China 2022ZD0160300 and NSFC key grant under grant no. 62136005. 

## **References** 

- [1] Suneel Belkhale, Tianli Ding, Ted Xiao, Pierre Sermanet, Quon Vuong, Jonathan Tompson, Yevgen Chebotar, Debidatta Dwibedi, and Dorsa Sadigh. Rt-h: Action hierarchies using language. _arXiv preprint arXiv:2403.01823_ , 2024. 2 

- [2] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 1, 2 

- [3] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-languageaction flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 2, 6, 3 

- [4] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 1, 2 

- [5] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2505.06111_ , 2025. 2, 6, 1, 3 

- [6] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 6, 3 

- [7] Chilam Cheang, Sijin Chen, Zhongren Cui, Yingdong Hu, Liqun Huang, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Xiao Ma, et al. Gr-3 technical report. _arXiv preprint arXiv:2507.15493_ , 2025. 1, 2 

- [8] Liang Chen, Haozhe Zhao, Tianyu Liu, Shuai Bai, Junyang Lin, Chang Zhou, and Baobao Chang. An image is worth 1/2 tokens after layer 2: Plug-and-play inference acceleration for large vision-language models. In _European Conference on Computer Vision_ , pages 19–35. Springer, 2024. 2 

- [9] Xi Chen, Xiao Wang, Lucas Beyer, Alexander Kolesnikov, Jialin Wu, Paul Voigtlaender, Basil Mustafa, Sebastian Goodman, Ibrahim Alabdulmohsin, Piotr Padlewski, et al. Pali-3 vision language models: Smaller, faster, stronger. _arXiv preprint arXiv:2310.09199_ , 2023. 1, 2 

- [10] Zhiwen Fan, Jian Zhang, Renjie Li, Junge Zhang, Runjin Chen, Hezhen Hu, Kevin Wang, Huaizhi Qu, Dilin Wang, Zhicheng Yan, et al. Vlm-3r: Vision-language models augmented with instruction-aligned 3d reconstruction. _arXiv preprint arXiv:2505.20279_ , 2025. 2 

- [11] Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, et al. Libero-plus: In-depth robustness analysis of vision- 

language-action models. _arXiv preprint arXiv:2510.13626_ , 2025. 2, 5, 4 

- [12] Matthew J Hausknecht and Peter Stone. Deep recurrent q- learning for partially observable mdps. In _AAAI fall symposia_ , page 141, 2015. 2 

- [13] Yicong Hong, Qi Wu, Yuankai Qi, Cristian RodriguezOpazo, and Stephen Gould. Vln bert: A recurrent visionand-language bert for navigation. In _Proceedings of the IEEE/CVF conference on Computer Vision and Pattern Recognition_ , pages 1643–1653, 2021. 2 

- [14] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. _ICLR_ , 1(2):3, 2022. 1 

- [15] Chia-Yu Hung, Qi Sun, Pengfei Hong, Amir Zadeh, Chuan Li, U Tan, Navonil Majumder, Soujanya Poria, et al. Nora: A small open-sourced generalist vision language action model for embodied tasks. _arXiv preprint arXiv:2504.19854_ , 2025. 6, 3 

- [16] Anqing Jiang, Yu Gao, Yiru Wang, Zhigang Sun, Shuo Wang, Yuwen Heng, Hao Sun, Shichen Tang, Lijuan Zhu, Jinhao Chai, et al. Irl-vla: Training an vision-languageaction policy via reward world model. _arXiv preprint arXiv:2508.06571_ , 2025. 1 

- [17] Titong Jiang, Xuefeng Jiang, Yuan Ma, Xin Wen, Bailin Li, Kun Zhan, Peng Jia, Yahui Liu, Sheng Sun, and Xianpeng Lang. The better you learn, the smarter you prune: Towards efficient vision-language-action models via differentiable token pruning. _arXiv preprint arXiv:2509.12594_ , 2025. 8 

- [18] Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa Sadigh. Prismatic vlms: Investigating the design space of visually-conditioned language models. In _Forty-first International Conference on Machine Learning_ , 2024. 1, 2, 7 

- [19] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 1, 2, 3, 6, 7 

- [20] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 1, 2, 3, 4, 5, 6 

- [21] Mikko Lauri, David Hsu, and Joni Pajarinen. Partially observable markov decision processes in robotics: A survey. _IEEE Transactions on Robotics_ , 39(1):21–40, 2022. 2, 3 

- [22] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational visionlanguage-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 1, 2 

- [23] Wei Li, Renshan Zhang, Rui Shao, Jie He, and Liqiang Nie. Cogvla: Cognition-aligned vision-language-action model via instruction-driven routing & sparsification. _arXiv preprint arXiv:2508.21046_ , 2025. 2, 3, 4 

- [24] Ye Li, Yuan Meng, Zewen Sun, Kangye Ji, Chen Tang, Jiajun Fan, Xinzhu Ma, Shutao Xia, Zhi Wang, and Wenwu 

13461 

   - Zhu. Sp-vla: A joint model scheduling and token pruning approach for vla model acceleration. _arXiv preprint arXiv:2506.12723_ , 2025. 2, 5 

- [25] Renjie Liao, Yuwen Xiong, Ethan Fetaya, Lisa Zhang, KiJung Yoon, Xaq Pitkow, Raquel Urtasun, and Richard Zemel. Reviving and improving recurrent back-propagation. In _International conference on machine learning_ , pages 3082– 3091. PMLR, 2018. 5 

- [26] Baijiong Lin, Feiyang Ye, Yu Zhang, and Ivor Tsang. Reasonable effectiveness of random weighting: A litmus test for multi-task learning. _Transactions on Machine Learning Research_ . 7 

- [27] Shengsheng Lin, Weiwei Lin, Wentai Wu, Songbo Wang, and Yongxiang Wang. Petformer: Long-term time series forecasting via placeholder-enhanced transformer. _IEEE Transactions on Emerging Topics in Computational Intelligence_ , 2024. 3 

- [28] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 2, 5, 7 

- [29] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. _Advances in neural information processing systems_ , 36:34892–34916, 2023. 1, 2 

- [30] Larry R Medsker, Lakhmi Jain, et al. Recurrent neural networks. _Design and applications_ , 5(64-67):2, 2001. 3 

- [31] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. Calvin: A benchmark for languageconditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 7(3): 7327–7334, 2022. 1, 2, 5, 6 

- [32] Tianwei Ni, Benjamin Eysenbach, and Ruslan Salakhutdinov. Recurrent model-free rl can be a strong baseline for many pomdps. _arXiv preprint arXiv:2110.05038_ , 2021. 2 

- [33] Feiyu Pan, Hao Fang, Fangkai Li, Yanyu Xu, Yawei Li, Luca Benini, and Xiankai Lu. Semantic and sequential alignment for referring video object segmentation. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 19067–19076, 2025. 2 

- [34] Razvan Pascanu, Tomas Mikolov, and Yoshua Bengio. On the difficulty of training recurrent neural networks. In _International conference on machine learning_ , pages 1310–1318. Pmlr, 2013. 5 

- [35] Ethan Perez, Florian Strub, Harm De Vries, Vincent Dumoulin, and Aaron Courville. Film: Visual reasoning with a general conditioning layer. In _Proceedings of the AAAI conference on artificial intelligence_ , 2018. 4 

- [36] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for visionlanguage-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 1, 2, 6, 3 

- [37] Jingjing Qian, Boyao Han, Chen Shi, Lei Xiao, Long Yang, Shaoshuai Shi, and Li Jiang. Geopredict: Leveraging predictive kinematics and 3d gaussian geometry for precise vla manipulation. _arXiv preprint arXiv:2512.16811_ , 2025. 2 

- [38] Rui Qian, Xiaoyi Dong, Pan Zhang, Yuhang Zang, Shuangrui Ding, Dahua Lin, and Jiaqi Wang. Streaming long video understanding with large language models. _Advances in Neural Information Processing Systems_ , 37:119336–119360, 2024. 2 

- [39] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 6 

- [40] Yongming Rao, Wenliang Zhao, Benlin Liu, Jiwen Lu, Jie Zhou, and Cho-Jui Hsieh. Dynamicvit: Efficient vision transformers with dynamic token sparsification. _Advances in neural information processing systems_ , 34:13937–13949, 2021. 4 

- [41] Moritz Reuss, Hongyi Zhou, Marcel R¨uhle, Omer<sup>¨</sup> Erdinc¸ Ya˘gmurlu, Fabian Otto, and Rudolf Lioutikov. Flower: Democratizing generalist robot policies with efficient vision-language-action flow policies. _arXiv preprint arXiv:2509.04996_ , 2025. 6 

- [42] Leyang Shen, Gongwei Chen, Rui Shao, Weili Guan, and Liqiang Nie. Mome: Mixture of multimodal experts for generalist multimodal large language models. _Advances in neural information processing systems_ , 37:42048–42070, 2024. 2 

- [43] Hao Shi, Bin Xie, Yingfei Liu, Lin Sun, Fengrong Liu, Tiancai Wang, Erjin Zhou, Haoqiang Fan, Xiangyu Zhang, and Gao Huang. Memoryvla: Perceptual-cognitive memory in vision-language-action models for robotic manipulation. _arXiv preprint arXiv:2508.19236_ , 2025. 2 

- [44] Richard D Smallwood and Edward J Sondik. The optimal control of partially observable markov processes over a finite horizon. _Operations research_ , 21(5):1071–1088, 1973. 2 

- [45] Wenxuan Song, Jiayi Chen, Pengxiang Ding, Han Zhao, Wei Zhao, Zhide Zhong, Zongyuan Ge, Jun Ma, and Haoang Li. Accelerating vision-language-action model integrated with action chunking via parallel decoding. _arXiv preprint arXiv:2503.02310_ , 2025. 1, 6 

- [46] Wenxuan Song, Ziyang Zhou, Han Zhao, Jiayi Chen, Pengxiang Ding, Haodong Yan, Yuxin Huang, Feilong Tang, Donglin Wang, and Haoang Li. Reconvla: Reconstructive vision-language-action model as effective robot perceiver. _arXiv preprint arXiv:2508.10333_ , 2025. 2 

- [47] Yizheng Sun, Yanze Xin, Hao Li, Jingyuan Sun, Chenghua Lin, and Riza Theresa Batista-Navarro. Lvpruning: An effective yet simple language-guided vision token pruning approach for multi-modal large language models. In _Findings of the Association for Computational Linguistics: NAACL 2025_ , pages 4299–4308, 2025. 4 

- [48] Shuhan Tan, Kairan Dou, Yue Zhao, and Philipp Kr¨ahenb¨uhl. Interactive post-training for vision-languageaction models. _arXiv preprint arXiv:2505.17016_ , 2025. 6, 3 

- [49] Qwen Team et al. Qwen2 technical report. _arXiv preprint arXiv:2407.10671_ , 2(3), 2024. 7 

- [50] Yang Tian, Sizhe Yang, Jia Zeng, Ping Wang, Dahua Lin, Hao Dong, and Jiangmiao Pang. Predictive inverse dynamics 

13462 

models are scalable learners for robotic manipulation. _arXiv preprint arXiv:2412.15109_ , 2024. 6 

- [51] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. 5, 7 

- [52] Hanzhen Wang, Jiaming Xu, Jiayi Pan, Yongkang Zhou, and Guohao Dai. Specprune-vla: Accelerating vision-languageaction models via action-aware self-speculative pruning. _arXiv preprint arXiv:2509.05614_ , 2025. 2, 8 

- [53] Qianqian Wang, Yifei Zhang, Aleksander Holynski, Alexei A Efros, and Angjoo Kanazawa. Continuous 3d perception model with persistent state. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 10510–10522, 2025. 2 

- [54] Tiannan Wang, Wangchunshu Zhou, Yan Zeng, and Xinsong Zhang. Efficientvlm: Fast and accurate vision-language models via knowledge distillation and modal-adaptive pruning. In _Findings of the association for computational linguistics: ACL 2023_ , pages 13899–13913, 2023. 5 

   - [63] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1702–1713, 2025. 6 

   - [64] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daum´e III, Andrey Kolobov, Furong Huang, and Jianwei Yang. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. In _The Thirteenth International Conference on Learning Representations_ , 2025. 6 

   - [65] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 1, 2 

- [55] Yihao Wang, Pengxiang Ding, Lingxiao Li, Can Cui, Zirui Ge, Xinyang Tong, Wenxuan Song, Han Zhao, Wei Zhao, Pengxu Hou, et al. Vla-adapter: An effective paradigm for tiny-scale vision-language-action model. _arXiv preprint arXiv:2509.09372_ , 2025. 6, 7 

- [56] Yuqi Wang, Xinghang Li, Wenxuan Wang, Junbo Zhang, Yingyan Li, Yuntao Chen, Xinlong Wang, and Zhaoxiang Zhang. Unified vision-language-action model. _arXiv preprint arXiv:2506.19850_ , 2025. 6, 8 

- [57] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Zhibin Tang, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, et al. Tinyvla: Towards fast, data-efficient visionlanguage-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025. 1 

- [58] Siyu Xu, Yunke Wang, Chenghao Xia, Dihao Zhu, Tao Huang, and Chang Xu. Vla-cache: Towards efficient visionlanguage-action model via adaptive token caching in robotic manipulation. _arXiv preprint arXiv:2502.02175_ , 2025. 2, 8 

- [59] Borong Zhang, Yuhao Zhang, Jiaming Ji, Yingshan Lei, Josef Dai, Yuanpei Chen, and Yaodong Yang. Safevla: Towards safety alignment of vision-language-action model via constrained learning. _arXiv preprint arXiv:2503.03480_ , 2025. 2 

- [60] Jiazhao Zhang, Kunyu Wang, Rongtao Xu, Gengze Zhou, Yicong Hong, Xiaomeng Fang, Qi Wu, Zhizheng Zhang, and He Wang. Navid: Video-based vlm plans the next step for vision-and-language navigation. _arXiv preprint arXiv:2402.15852_ , 2024. 2 

- [61] Shiqi Zhang, Piyush Khandelwal, and Peter Stone. Dynamically constructed (po) mdps for adaptive robot planning. In _Proceedings of the AAAI conference on artificial intelligence_ , 2017. 3 

- [62] Yuan Zhang, Chun-Kai Fan, Junpeng Ma, Wenzhao Zheng, Tao Huang, Kuan Cheng, Denis Gudovskiy, Tomoyuki Okuno, Yohei Nakata, Kurt Keutzer, et al. Sparsevlm: Visual token sparsification for efficient vision-language model inference. _arXiv preprint arXiv:2410.04417_ , 2024. 2 

13463 

