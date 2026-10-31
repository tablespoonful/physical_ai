---
title: "Universal Actions for Enhanced Embodied Foundation Models"
date: "2025-01-17"
authors: "Jinliang Zheng; Jianxiong Li; Dongxiu Liu; Yinan Zheng; Zhihao Wang; Zhonghong Ou"
venue: "CVPR 2025"
url: https://arxiv.org/abs/2501.10105
pdf: https://arxiv.org/pdf/2501.10105
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2501.10105)** / [論文ページ](https://arxiv.org/abs/2501.10105)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **Universal Actions for Enhanced Embodied Foundation Models** 

Jinliang Zheng<sup>* 1</sup><sup>_,_2</sup><sup>_,_5</sup> , Jianxiong Li<sup>* † 1</sup> , Dongxiu Liu<sup>* 4</sup><sup>_,_1</sup> , Yinan Zheng<sup>1</sup> , Zhihao Wang<sup>3</sup><sup>_,_1</sup> , Zhonghong Ou<sup>4</sup> , Yu Liu<sup>2</sup> , Jingjing Liu<sup>1</sup> , Ya-Qin Zhang<sup>1</sup> , Xianyuan Zhan<sup>‡ 1</sup><sup>_,_5</sup><sup>_,_6</sup> 1 AIR, Tsinghua University, 2 Sensetime Research, 3 Peking University 

4 Beijing University of Posts and Telecommunications, 5 Shanghai AI Lab, 6 BAAI 

- _{_ zhengjl23, li-jx21 _}_ @mails.tsinghua.edu.cn zhanxianyuan@mail.tsinghua.edu.cn 

## **Abstract** 

_Training on diverse, internet-scale data is a key factor in the success of recent large foundation models. Yet, using the same recipe for building embodied agents has faced noticeable difficulties. Despite the availability of many crowdsourced embodied datasets, their action spaces often exhibit significant heterogeneity due to distinct physical embodiment and control interfaces for different robots, causing substantial challenges in developing embodied foundation models using cross-domain data. In this paper, we introduce UniAct, a new embodied foundation modeling framework operating in a_ **_<u>Universal Action</u> Space_** _. Our learned universal actions capture the generic atomic behaviors across diverse robots by exploiting their shared structural features, and enable enhanced cross-domain data utilization and cross-embodiment generalizations by eliminating the notorious heterogeneity. The universal actions can be efficiently translated back to heterogeneous actionable commands by simply adding embodiment-specific details, from which fast adaptation to new robots becomes simple and straightforward. Our 0.5B instantiation of UniAct reaches 14X larger SOTA embodied foundation models in extensive evaluations on various real-world and simulation robots, showcasing exceptional cross-embodiment control and adaptation capability, highlighting the crucial benefit of adopting universal actions. Project page: https://2toinf.github.io/UniAct/_ 

## **1. Introduction** 

In fields like natural language processing and computer vision, foundation models trained on vast and diverse data sources have demonstrated remarkable success and strong generalization ability, highlighting the benefits of learn- 

> *Equal contribution 

> †Project Lead 

> ‡Corresponding author 


Figure 1. Universal action space holds the potential to be versatile to ANY domain-specific actions. 

ing general-purpose models over task-specific counterparts [1, 5, 40, 62]. Inspired by these successes, developing versatile embodied foundation models that are capable of handling cross-task, cross-environment, and cross-embodiment generalization, offers a promising pathway towards building general-purpose embodied agent [8, 17, 18, 28, 31, 61, 68]. 

However, significant challenges arise from the substantial heterogeneity of embodied data [20, 49, 64]. Such heterogeneity is evident not only in visual discrepancies caused by variations in camera placements ( _e.g._ , wrist or thirdperson view) and environmental conditions ( _e.g._ , lighting or background variations), but more critically, in _action heterogeneity_ [17, 48, 65]. _1)_ Robots with different embodiment ( _e.g._ , different degrees of freedom or distinctions across robotic arms, quadrupeds, and cars) possess entirely distinct action spaces [68]. _2)_ Furthermore, the diversity in control interfaces ( _e.g._ , end effector (EEF) position or velocity controller for robotics arms) leads to fundamentally different physical meanings for action commands [49]. _3)_ Even when actions are collected from the same robotic platform but by different human manipulators, the multimodality in human behaviors also exacerbates such het- 

22508 

erogeneity [14, 34, 41, 55]. Consequently, embodied action data collected across different robots and institutions tend to reside on largely disjoint manifolds within the original physical spaces (e.g., position and rotation of endeffectors) [17, 65], significantly complicating data sharing across different data sources. 

Currently, no existing solution can adequately address the issue of action heterogeneity. Most prior studies forcibly treat different action spaces as equivalent and apply the same discretization or normalization techniques, leading to a potentially conflicted action space where similar action encodings could represent entirely different physical meanings [31, 49, 61]. While some efforts attempt to design a physically interpretable action space that is applicable across various robotic systems by na¨ıvely aggregating all individual action spaces [17, 41]. This requires extensive human engineering efforts and fails to uncover and leverage the inherent connections across different embodied action spaces, impeding the effective development of generalpurpose embodied foundation models. 

In this paper, we introduce _UniAct_ (Embodied foundation models with <u>Universal Actions),</u> a novel embodied modeling framework that is constructed in the _Universal Action Space_ rather than the troublesome heterogeneous action spaces. The universal actions learned in _UniAct_ encode the generic atomic behaviors that are generalizable across diverse robotics platforms without being constrained to specific embodiment mechanics and control interfaces. For instance, different robots should perform similar behaviors of “moving forward” when facing a target directly ahead, despite exhibiting totally different control signals due to their embodiment gaps. This abstraction transcends specific embodiment and control constraints, allowing it to be universally applicable across diverse robotics platforms, providing significant potential to enhance cross-embodiment data utilization and model generalization. In this sense, minimal parameters and data are sufficient to decode the universal action to an embodiment-specific one, since the general motion behaviors have been captured in the universal space and the decoder simply needs to add some embodiment details for each robotic platform, therefore enabling efficient adaptation across new robotic systems during deployment. 

In details, UniAct employs a shared Vision Language Model (VLM) [6, 32, 35, 39, 40, 73] to construct the universal action space as a vector-quantized codebook [63]. Akin to a learnable skill library [34, 45, 55], each code encapsulates an atomic behavior versatile enough to be executed by diverse robots. This setup acts as a crucial information bottleneck, driving the VLM to identify and exploit shared primitive behaviors across diverse action spaces. This extraction scheme enables effective generalization of behaviors for cross-embodiment control, making our 0.5B instantiation, UniAct-0.5B, surpasses models 14x larger, such 

as OpenVLA [31] with 7B parameters, in a wide range of tasks. The derived universal actions can be translated into precise, actionable commands for various embodiments through streamlined heterogeneous decoders. These decoders take the universal action as conditional input and augment it with embodiment-specific features from their unique observational data. This allows for flexible customization according to specific requirements, such as the inclusion or exclusion of proprioceptive features or variations in the number of camera views. Fast adaptation to new domains or robotic platforms can be achieved by simply adding new heads as lightweight decoders for new tasks. Our comprehensive evaluations on challenging task settings, including large view changes and an unseen robot not present in the training data, confirm UniAct’s remarkable transferability, demonstrating great advantages of developing embodied foundation models within a universal action space over the conventional heterogeneous spaces. 

## **2. Related Work** 

**Multimodal Foundation Models.** Large Language Models (LLMs) [1, 5, 40, 62] have exhibited remarkable capabilities across a variety of tasks, showcasing impressive zeroshot and in-context learning capabilities [16]. Building on this, large Vision Language Models (VLMs) have been developed by integrating vision and language into a unified tokenized space, demonstrating outstanding multimodal instruction-following abilities [6, 21, 32, 35, 58, 59, 73]. Their success is primarily attributed to extensive internetscale pretraining, which leverages vast and diverse highquality data corpora from the Internet. 

**Embodied Foundation Models.** When developing embodied foundation models, an additional crucial modality—action (the deployable control signals that robots can interpret and execute, _e.g._ , EEF position/velocity)—is incorporated during training. State-of-the-art models are often constructed as Vision Language Action models (VLA) [9, 10, 18, 31, 49], integrating visual and linguistic inputs with actionable outputs. However, the action labels collected from different robotics platforms and labs exhibit significant heterogeneity [30, 49, 64], impeding effective data sharing across different sources. To sidestep this challenge, many works employ large-scale action-free vision language data, such as out-of-domain human activities [15, 24, 25], to firstly obtain a good embodied VLMs, then finetune it to a specialized VLA given a small set of action labels from a specific robot platform [3, 4, 7, 10, 12, 19, 22, 29, 36, 37, 42, 47, 66, 67, 69, 73]. While these methods can enhance sample efficiency for specific robots on a narrow set of tasks, they suffer from serious performance bottlenecks towards building a generalist embodied agent [7, 19, 56], as the action data gathered from any single robot platform is far less comprehensive than crowedsourced data collected globally [20, 30, 49]. 

22509 


Figure 2. UniAct leverages diverse data sources for generalist embodied control. A shared Vision Language Model (VLM) extracts transferable features across various data sources; The output tokens are converted into universal actions, represented as vector-quantized codes where each code captures common atomic behaviors across different robots; The Gumbel Softmax-selected universal action is then translated back into specific commands through different heads, each encoding embodiment-specific features for individual robots. 

Some recent works leverage the abundant heterogeneous action labels to develop generalist robot policies for crossembodiment control. RT-X series [49], Octo [61] and OpenVLA [31] leverage data from different 7-DoF robots to enhance generalization over the one trained on single robot source. Step further, CrossFormer [17], RDT [41], _π_ 0 [8] and Yang et al. [68] explore the data from robots with totally distinct mechanical structures, such as those in manipulation and navigation, and from single-arm versus bimanual systems. However, existing works either ignore the heterogeneous properties of action spaces of different sources, crudely treating them as equal without considering their inherent conflicts [31, 49, 61], or na¨ıvely aggregate all action spaces together, failing to exploit the underlying shared commonalities across different robots [8, 17, 41, 68]. 

**Embodied Models with Latent Action Spaces.** Our work aims to extract a versatile universal action space, akin to a latent space but encodes common atomic control behaviors and patterns across various robotic platforms. Some works develop embodied models in latent spaces [4, 13, 34, 45, 54, 55, 69, 70]. Among them, LAPA [69], IGOR[4], and LAPO [54] develop a latent action space through joint self-supervised training of inverse and forward dynamics models on action-free videos [11]. However, the latent actions extracted in this way primarily focus on explaining the changes between video frames, lacking embodiment con- 

siderations or direct causal connections to actual control signals. To see why this is problematic, assuming we add a new object in front of the robot, the visual inputs will change but this has nothing to do with the control behavior, an ideal encoded action should not capture such distracted information. BeT [55], VQ-BeT [34] and QueST [45] also build a discrete codebook of actions via K-means clustering [43] or Vector Quantization [33, 44, 63], where each code in the codebook encodes a different clustering center for action labels. These works primarily focus on simpler domains with a single embodiment type, which enhances the ability to model complex human demonstrations with multiple modes, but struggles to address action heterogeneity across different embodiments. In contrast, our universal actions integrate goal information from the embodimentagnostic language modality with supervision on the actual action signal, providing a versatile and abstracted skill library to facilitate cross-embodiment sharing. Moreover, our research delves into a more complex heterogeneous setting and develops a large embodied foundation model, moving beyond the limited scopes considered in previous studies. 

## **3. The UniAct Framework** 

We introduce UniAct, an embodied foundation modeling framework designed to operate in a _Universal Action Space_ , adept at bridging domain gaps and facilitating training on 

22510 

large-scale heterogeneous data. We first discuss the desirable properties of universal actions, and then provide a detailed discussion about the model architecture and learning scheme for extracting and decoding universal actions from heterogeneous cross-embodiment data. 

### **3.1. Universal Action Space** 

The desired universal action space is that all movements, driven by heterogeneous control signals from various embodiments, can be distilled into shared latent atomic behaviors, despite their distinct physical meanings. We refer to these abstract behavior representations as _universal actions_ , which are shared across all physical embodiments. 

We are particularly interested in exploring a discrete universal action space. This is motivated by the robust capabilities of discrete representations in complex reasoning, planning, and predictive learning, as demonstrated by the success of LLMs and VLMs [1, 5, 6, 60] and Vector Quantized Variational Autoencoders [52, 63]. In this paper, we model the universal action space as _U ∈_ R<sup>_N×D_</sup> and implement it with a vector quantized codebook [63], represented as 


where _N_ is the space size and each _ui_ is a _D_ -dimensional vector embedding that represents a generic atomic behavior. 

Several prior studies [4, 11, 69] pursued a similar concept of constructing generic, latent actions by inferring them as the dynamic changes observed between two visual states. However, this scheme suffers two key limitations, leading to suboptimal and noisy universal action spaces: 

- The observational changes encompass not only the outcomes of robots, but also external factors (e.g., the appearance of new objects, human intervention, etc.) that have no causal connection to the actual control. 

- The interval between two observations critically influences the semantic interpretation of the extracted atomic behaviors, making standardizing behavioral interpretation complicated across different data sources. 

### **3.2. Universal Action Extraction** 

To derive the desirable universal action space, we propose a new method for extracting universal actions, pivoting away from solely focusing on explaining observational changes, but more on understanding task progression. Specifically, we fine-tune a large vision language model as the universal action extractor, which outputs the likelihood _p_ ( _u|o, g_ ) of selecting universal action _u_ given observation _o_ and task goal _g_ (e.g., language instruction). We want the corresponding adopted universal action _u_<sup>_∗_</sup> that matches the atomic behavior encoded in the embodied data to satisfy: 


Akin to planning in the latent space [13, 50, 51], the extractor aims to infer the most relevant universal action for solving a given task _g_ under the observation _o_ , thereby crafting universal actions directly related to task progression rather than merely identifying the noisy observational changes. We employ a VLM to achieve this purpose due to its strong visual-language reasoning capability. Moreover, fine-tuning a pre-trained VLM also greatly improves the sample efficiency when learning the universal actions. This extractor creates a crucial information bottleneck for cross-domain generalization, as different robots are forced to use the same discrete codebook _U_ to capture the generic and shared atomic behaviors across all domains. 

To implement this, however, the non-differentiable arg max impedes the gradient propagation. So, we use categorical reparametrization during the training, utilizing the Gumbel-Softmax technique to facilitate gradient estimation [27]. Specifically, the forward procedure is as follows: 


where _wi_ is the weight for each universal action _ui_ , computed using the Gumbel Softmax function: 


Here, _ϵi_ is a Gumbel noise sampled from the Gumbel distribution, and _τ_ is the temperature to smooth the probability distribution. To promote parameter space exploration in the early training stage and the stability of model convergence, we gradually decay temperature _τ_ during the training process. Our proposed universal action extractor is illustrated in Figure 2, please refer to the Appendix A for more details. 

### **3.3. Heterogeneous Decoding** 

To efficiently translate the highly abstract behaviors in the universal action space into precise, embodiment-specific control signals, it is crucial to integrate more embodiment detail, such as control type, proprioception, and distinct observations. To address this, we introduce a series of lightweight decoder heads to adapt for each type of embodiment, denoted as _H_ = ( _h_ 1 _...hk...hK_ ), _K_ is number of training domains. Each head _hk_ is specifically designed to learn the mapping from universal action _u_<sup>_∗_</sup> and visual observation _o_ to heterogeneous control signals for the embodiment in domain _k_ . The operation of each decoder head _hk_ can be formulated as: 


where ˆ _a_<sup>(</sup><sup>_k_)</sup> is the predicted control signals. As overly complex decoding heads with excessive parameters could overfit to the data distribution of the target domain, all heterogeneous heads are implemented as simple MLP networks 

22511 

that take the _u_<sup>_∗_</sup> and visual features _o_ extracted by a shared vision backbone as inputs. By keeping the decoding heads lightweight, we ensure that the majority of learning is conducted for the universal actions, thereby maximally improving generalization across different embodiments. 

### **3.4. Training Procedure** 

The primary learning objective of UniAct is to distill a universal action space that is shared across diverse embodiments, with the critical feature that these universal actions can be precisely translated back into domain-specific control signals. To facilitate this, the model is trained using a comprehensive collection of _K_ heterogeneous datasets _D_ = ( _D_ 1 _...Dk...DK_ ). Each _Dk_ comprises a set of robotic control trajectories, represented as _τi_<sup>(</sup><sup>_k_)</sup> = _{o_<sup>(</sup> _i,t_<sup>_k_)</sup><sup>_, a_(</sup> _i,t_<sup>_k_)</sup><sup>_, gi}_1</sup><sup>_≤t≤T_,</sup> where _τi_<sup>(</sup><sup>_k_)</sup> is the _i_ -th trajectory of maximum length _T_ , containing observations, actions, and goals. Concretely, UniAct ingests _o_ and _g_ as inputs to predict the universal action _u_<sup>_∗_</sup> using the universal action extractor, which is then mapped along with _o_ to _a_ ˆ<sup>(</sup><sup>_k_)</sup> using the heterogeneous decoding heads. The overall training objective is as follows: 


Here, _Lk_ is the behavior cloning loss, which is customizable based on the nature of the action labels in each dataset, for example, employing Cross-Entropy for discrete actions and MSE, Huber loss, or diffusion loss [14, 26] for continuous actions. We optimize the above objective to learn both the universal action codebook _U_ as well as the parameters _θ_ of the universal action extractor and all heterogeneous decoding heads. Importantly, while _U_ and the universal action extractor are concurrently updated throughout each training iteration, the heterogeneous heads _hk_ are updated based on the domain-specific sampled training batches. This training strategy mirrors the philosophy in many meta-learning methods [23], which learns both globally shared parameters that allow adaptation to related tasks, as well as taskspecific components that guarantee downstream task performance. Through this approach, UniAct strives to refine a robust, adaptive universal action space as well as a decoding strategy that can be seamlessly integrated with diverse embodiments and their specific operational contexts. 

## **4. Experiments** 

In this section, we first describe the detailed implementation of the UniAct framework and then present the evaluation experiments conducted to answer the following questions: 

- Can universal actions enhance execution performance across various embodiments with large domain gaps? 

- Can universal actions be seamlessly transferred to new, unseen embodiments? 

• Dose UniAct learn a meaningful universal action space? 

### **4.1. Experiments Setup** 

**Implementation Details** . In this paper, we build a 0.5B instantiation of UniAct on heterogeneous embodied data sources to explore a universal action space ( _U ∈_ R<sup>256</sup><sup>_×_128</sup> ). Specifically, UniAct-0.5B is built upon _LLaVA-OneVion0.5B_ [35], a well-trained VLM which can provide comprehensive multi-modal representations. The training of UniAct-0.5B is carried out on 64 A100 GPUs with DeepSpeed [53] over a span of 10 days, utilizing 1 million demonstrations gathered from 28 distinct embodiments. The training data combines several open-sourced robot collections, including Open-X Embodiment [49], Libero [38], and Droid [30], standardized to include third-person visual observations and language instructions while preserving action heterogeneity. For more details about training and data constructions, please refer to the Appendix A. 

**Baseline Setup** . We select three state-of-the-art (SOTA) vision-language-action models including Octo [61], CrossFormer [17], OpenVLA [31], and one SOTA pretrained VLM model, LAPA [69] as baselines. Octo and CrossFormer are 0.1B policies, OpenVLA employs a 7Bparameter auto-regressive architecture with discrete actions. They are trained on about 1 million carefully curated robot demonstrations without action heterogeneity, such as preprocessing all absolute EEF positions to relative EEF positions and removing joint position actions. LAPA is also a 7B model, but instead of using action labels, it constructs latent actions by capturing visual changes between frames based on the same robot demonstrations. To adapt LAPA to generate real actions, further finetuning with action labels is required. In contrast, UniAct-0.5B is trained on a similar scale of data from the same data sources but does not employ such tedious data cleaning. We compare UniAct with the baseline models to demonstrate its effectiveness in extracting universal actions from heterogeneous data. 

### **4.2. Main Results** 

To assess the cross-embodiment generalization capabilities of UniAct-0.5B, we conduct “out-of-the-box” evaluations on both a real-world WidowX robot [64] and a simulation Franka robot from Liu et al. [38]. Both platforms are commonly used in previous works to test the effectiveness of generalist robot policies [49, 61, 64], and possess substantial domain gaps. Given that our training dataset includes data from these two embodiments, we can leverage the pretrained heterogeneous heads to translate the universal actions seamlessly back into deployable control signals. **Real-World Robot Evaluation** . Following Kim et al. [31], we define a comprehensive set of evaluation tasks for realworld robots, covering several dimensions of generalization: **visual** , **motion** , **physical** , **semantic** , and **language** 

22512 


Figure 3. WidowX robot evaluation. We evaluate different axes of generalization ability, covering a total of 19 tasks. Representative tasks are presented above. For each task, we evaluate 10 trials and report the average success rate for each suites. 


Figure 4. For benchmarking purpose, we evaluate on the LIBERO benchmark [38] in simulations. LIBERO contains several task suites to examine different axes of policy abilities. LIBERO-90 contains 90 tasks and others each contain 10 tasks, covering 130 tasks. For each task, we evaluate 20 trials for each model and report the average success rate for each task suites. 

**grounding** . Overall, each model is evaluated across 190 rollouts, distributed over 19 tasks with 10 trials each, see Appendix B for more details. Representative tasks and results are illustrated in Figure 3. To adapt LAPA to WidowX robot, we full-tune it on Bridge [64] dataset about 2K gradient steps. UniAct-0.5B outperforms 14X larger OpenVLA7B and LAPA-7B in visual, motion, and physical generalization tasks. This shows the substantial benefits of extracting universal actions from heterogeneous data in enhancing robustness to visual distractions and low-level control generalization. While OpenVLA leverages a 7B backbone for superior semantic understanding and language grounding capability, UniAct-0.5B achieves comparable performance in semantic generalization and language grounding tasks, underscoring its efficiency and effectiveness. 

**Simulation Evaluation** . We utilize the LIBERO Benchmarks [38] for evaluation. Notably, baseline models are not initially trained on the simulation data, thus we fine-tune them on the LIBERO platform. The data used to train both UniAct and the baseline models are fully aligned in terms of tasks, data quantity, and image quality. For more details, please refer to Appendix A. The benchmark comprises 130 

tasks across five suites: LIBERO-Spatial, -Object, -Goal, -Long, and -90. The LIBERO-90 suite includes 90 tasks, while each of the other four suites contains 10 tasks. The results can be found in Fig 4. UniAct-0.5B surpasses baseline models in all suites, demonstrating a significant improvement with an overall average accuracy. This superior performance can be attributed to the ability of UniAct to bridge domain gaps and extract generalizable atomic behaviors. By leveraging demonstrations from various domains to learn the universal actions, UniAct significantly enhances task performance on the LIBERO benchmarks. 

### **4.3. Fast Adaptation to New Embodiment** 

**Experiment Setup** . To assess the fast adaptation ability, we evaluate on a new real robot, AIRBOT (Figure 5). We evaluate four different controller interfaces: relative/absolute EEF position and relative/absolute joint position. Neither UniAct nor the baselines were pre-trained on AIRBOT data. We collect 100 demonstrations on this new robot platform with the four different types of control interfaces. Considering the significant heterogeneity among these control interfaces, we put a lot of effort into fine-tuning baselines and 

22513 


Figure 5. Fast adaptation to new robots. We fine-tune models on an unseen AIRBOT robot with different controller interfaces including relative/absolute joint/EEF positions. The task is to stack the small cube on the small cuboid, requiring precise action execution. The fine-tuning data is collected w/o any distractors, but we also evaluate a hard version, where the policy should be robust to diverse clutters. 

make sure the model convergence meets the official requirements (e.g., 95% prediction accuracy for OpenVLA). **Fast Adaptation with UniAct** . Unlike baseline models that require extensive training to bridge the adaptation gap across different action types, UniAct can rapidly adapt to new embodiments and control interfaces. Having already learned cross-embodiment behaviors, we facilitate fast adaptation by freezing the codebook and the universal action extractor. Concurrently, we train four heterogeneous decoding heads from scratch for each type of actions with the collected demonstrations. Each newly introduced head is implemented with a simple MLP that takes the _u_<sup>_∗_</sup> and vision features _o_ from a shared vision backbone as inputs. **Evaluation** . We conducted evaluations using both an easy and a hard version of the task “stack the cube on another cube”. The results can be found in Figure 5. UniAct-0.5B demonstrates consistently strong generalization across all types of control signals, surpassing the two baseline models. Notably, the number of parameters UniAct-0.5B used for fine-tuning versus the total model size is the smallest (4M / 500M: 0.8%). In comparison, OpenVLA and Octo utilize 1.4% (97M / 7000M) and 2% (2M / 100M) of their total model sizes, respectively. This efficient parameter utilization highlights UniAct’s effectiveness and adaptability in applying learned universal actions to new tasks and embodiments with minimal parameter space expansion. 

### **4.4. Fast Adaptation to New Decoder Head** 


Table 1. Fast adaptation to Bimanual AIRBOT and ACT head 

We further test whether a more advanced decoder can improve performance by integrating ACT [72] into UniAct0.5B. We freeze UniAct-0.5B and adapt it to a Bimanual AIRBOT robot, using observations from a top view, two wrist views, and proprioception. We collect 250 demos per 

task for 4 tasks and compare UniAct-0.5B with the pretrained LLaVa-OV-0.5B model. Tab 1 shows UniAct’s superior performance, validating its pretraining effectiveness. Additionally, we finetune UniAct-0.5B with the ACT decoder on the LIBERO benchmark, using a top view, wrist view, and proprioception. As shown in Figure 4, UniAct achieves further improvements, demonstrating its adaptability with advanced decoders and richer observations. Please refer to Appendix B.4 for details. 

### **4.5. In-depth Analysis of Universal Actions** 

In this section, we demonstrate that UniAct constructs a meaningful universal action space from two perspectives: 1) Consistent semantical behaviors are encoded as the same universal actions across diverse embodiments; 2) Universal action extractor can efficiently exploit this shared structure in the universal action space across different robots. 

**Interpretation of Universal Actions** . We manually inspect the decoded behaviors for all 256 universal actions across different robots and observe at least 40% of them exhibit exact consistency. Fig 6 shows that the same universal action can be decoded back to consistent behaviors for different robots even with huge gaps. For instance, different robots with different viewpoints, and even those undergoing huge sim-to-real gaps, can execute similar semantical meaningful behaviors given the same universal action. 

**Control with the Universal Action** . Therefore, we can directly interact with the robot to perform desired behaviors by choosing a sequence of universal actions. Fig 7 clearly demonstrates that we can control the robot using universal actions without any robotic knowledge, such as learning complex forward/inverse kinematics transformations. This also underscores the potential of utilizing the universal action extractor as an _action tokenizer_ to facilitate future deployments of more advanced embodied foundation models by planning in this discrete universal action space. 

**Statistical Analysis For Universal Action Utilization** . Here, we summarize the universal action utilization distributions for different tasks across different robots. Table 2 clearly shows that the utilization distributions for the same tasks and different robots are similar, but for differ- 

22514 


Figure 6. We manually check the decoded behavior for all 256 universal actions across different robots and observe at least 40% show exact consistency, even with varying viewpoints and significant domain gaps between the real world and simulation. Visualizations of repeated executions of the same universal action across different robots reveal clear, semantically meaningful, and consistent behaviors. 


Figure 7. Since all universal actions encode semantic meaningful behaviors, we can directly play with it! By selecting the desired behavior using its corresponding universal action ID, we can manually control the robot to perform complex tasks such as Pick & Place. 

||_P_WidowX|_P_Franka|_O_WidowX|_O_Franka|
|---|---|---|---|---|
|_P_WidowX|0.|0.34|0.45|0.51|
|_P_Franka|0.34|0.|0.60|0.58|
|_O_WidowX|0.45|0.60|0.|0.44|
|_O_Franka|0.51|0.58|0.44|0.|


Table 2. We calculate the JS divergence of the universal action utilization distributions for two tasks in two distinct domains (lower means more consistent). P and O denote “pick up the bowl“ and “open the drawer“, respectively. WidowX and Franka denote the robot in the real world and simulation in Figure 3-4, respectively. 

ent tasks and same robots are different, demonstrating that the universal action extractor indeed correctly exploits these embodiment-agnostic atomic behaviors by focusing more on task progressions over embodiment details. 

## **5. Conclusion** 

We introduce UniAct, an innovative embodied foundation modeling framework that operates in a _Universal Action Space_ to address the challenge of action heterogeneity. This 

universal action space encodes shareable atomic behaviors across diverse embodied action spaces to significantly enhance cross-domain data utilization and facilitate crossembodiment generalization, enabling our 0.5B parameter model to outperform SOTA models that are 14 times larger. Also, the learned universal actions can be precisely translated to any embodiment-specific actions with minimal parameters through heterogeneous decoding, thus allowing for fast adaptation to new robots possessing distinct control interfaces and physical properties. Moreover, our learned universal action extractor can also be used as a universal action tokenizer to power the construction of future largescale embodied foundation models. Currently, UniAct is trained with a 0.5B parameter instantiation and evaluated mostly on single-arm robotics platforms due to resource constraints. Future work will focus on scaling up UniAct to larger models and extending its application to a broader range of embodiments, including bi-manual robots and even autonomous driving, further leveraging its versatile capability and effectiveness in more robotic applications. 

22515 

## **6. Acknowledgment** 

This work is supported by funding from Beijing Academy of Artificial Intelligence (BAAI) and Wuxi Research Institute of Applied Technologies, Tsinghua University under Grant 20242001120. 

## **References** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 1, 2, 4 

- [2] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, et al. Do as i can, not as i say: Grounding language in robotic affordances. _arXiv preprint arXiv:2204.01691_ , 2022. 16 

- [3] Anurag Ajay, Seungwook Han, Yilun Du, Shuang Li, Abhi Gupta, Tommi Jaakkola, Josh Tenenbaum, Leslie Kaelbling, Akash Srivastava, and Pulkit Agrawal. Compositional foundation models for hierarchical planning. _Advances in Neural Information Processing Systems_ , 36, 2024. 2 

- [4] Anonymous. IGOR: Image-GOal representations are the atomic building blocks for next-level generalization in embodied AI. In _Submitted to The Thirteenth International Conference on Learning Representations_ , 2024. under review. 2, 3, 4 

- [5] Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei Huang, et al. Qwen technical report. _arXiv preprint arXiv:2309.16609_ , 2023. 1, 2, 4 

- [6] Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan Tan, Peng Wang, Junyang Lin, Chang Zhou, and Jingren Zhou. Qwen-vl: A frontier large vision-language model with versatile abilities. _arXiv preprint arXiv:2308.12966_ , 2023. 2, 4 

- [7] Kevin Black, Mitsuhiko Nakamoto, Pranav Atreya, Homer Rich Walke, Chelsea Finn, Aviral Kumar, and Sergey Levine. Zero-shot robotic manipulation with pre-trained image-editing diffusion models. In _The Twelfth International Conference on Learning Representations_ . 2, 16 

- [8] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control, 2024. 1, 3 

- [9] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 2 

- [10] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, 

Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 2 

- [11] Jake Bruce, Michael D Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, et al. Genie: Generative interactive environments. In _Forty-first International Conference on Machine Learning_ , 2024. 3, 4 

- [12] Chi-Lam Cheang, Guangzeng Chen, Ya Jing, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Hongtao Wu, Jiafeng Xu, Yichu Yang, et al. Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation. _arXiv preprint arXiv:2410.06158_ , 2024. 2 

- [13] Xi Chen, Ali Ghadirzadeh, Tianhe Yu, Jianhao Wang, Alex Yuan Gao, Wenzhe Li, Liang Bin, Chelsea Finn, and Chongjie Zhang. Lapo: Latent-variable advantageweighted policy optimization for offline reinforcement learning. _Advances in Neural Information Processing Systems_ , 35:36902–36913, 2022. 3, 4 

- [14] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , page 02783649241273668. 2, 5 

- [15] Dima Damen, Hazel Doughty, Giovanni Maria Farinella, Sanja Fidler, Antonino Furnari, Evangelos Kazakos, Davide Moltisanti, Jonathan Munro, Toby Perrett, Will Price, et al. Scaling egocentric vision: The epic-kitchens dataset. In _Proceedings of the European conference on computer vision (ECCV)_ , pages 720–736, 2018. 2 

- [16] Qingxiu Dong, Lei Li, Damai Dai, Ce Zheng, Jingyuan Ma, Rui Li, Heming Xia, Jingjing Xu, Zhiyong Wu, Tianyu Liu, et al. A survey on in-context learning. _arXiv preprint arXiv:2301.00234_ , 2022. 2 

- [17] Ria Doshi, Homer Rich Walke, Oier Mees, Sudeep Dasari, and Sergey Levine. Scaling cross-embodied learning: One policy for manipulation, navigation, locomotion and aviation. In _8th Annual Conference on Robot Learning_ . 1, 2, 3, 5 

- [18] Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, et al. Palme: an embodied multimodal language model. In _Proceedings of the 40th International Conference on Machine Learning_ , pages 8469–8488, 2023. 1, 2 

- [19] Yilun Du, Sherry Yang, Pete Florence, Fei Xia, Ayzaan Wahid, Pierre Sermanet, Tianhe Yu, Pieter Abbeel, Joshua B Tenenbaum, Leslie Pack Kaelbling, et al. Video language planning. In _The Twelfth International Conference on Learning Representations_ . 2, 16 

- [20] Hao-Shu Fang, Hongjie Fang, Zhenyu Tang, Jirong Liu, Chenxi Wang, Junbo Wang, Haoyi Zhu, and Cewu Lu. Rh20t: A comprehensive robotic dataset for learning diverse skills in one-shot. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 653–660. IEEE, 2024. 1, 2 

- [21] Nanyi Fei, Zhiwu Lu, Yizhao Gao, Guoxing Yang, Yuqi Huo, Jingyuan Wen, Haoyu Lu, Ruihua Song, Xin Gao, Tao Xi- 

22516 

ang, et al. Towards artificial general intelligence via a multimodal foundation model. _Nature Communications_ , 13(1): 3094, 2022. 2 

- [22] Jensen Gao, Bidipta Sarkar, Fei Xia, Ted Xiao, Jiajun Wu, Brian Ichter, Anirudha Majumdar, and Dorsa Sadigh. Physically grounded vision-language models for robotic manipulation. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 12462–12469. IEEE, 2024. 2 

- [23] Jonathan Gordon, John Bronskill, Matthias Bauer, Sebastian Nowozin, and Richard Turner. Meta-learning probabilistic inference for prediction. In _International Conference on Learning Representations_ , 2019. 5 

- [24] Raghav Goyal, Samira Ebrahimi Kahou, Vincent Michalski, Joanna Materzynska, Susanne Westphal, Heuna Kim, Valentin Haenel, Ingo Fruend, Peter Yianilos, Moritz Mueller-Freitag, et al. The” something something” video database for learning and evaluating visual common sense. In _Proceedings of the IEEE international conference on computer vision_ , pages 5842–5850, 2017. 2 

- [25] Kristen Grauman, Andrew Westbury, Eugene Byrne, Zachary Chavis, Antonino Furnari, Rohit Girdhar, Jackson Hamburger, Hao Jiang, Miao Liu, Xingyu Liu, et al. Ego4d: Around the world in 3,000 hours of egocentric video. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 18995–19012, 2022. 2 

- [26] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. _Advances in neural information processing systems_ , 33:6840–6851, 2020. 5 

- [27] Eric Jang, Shixiang Gu, and Ben Poole. Categorical reparameterization with gumbel-softmax. _arXiv preprint arXiv:1611.01144_ , 2016. 4 

- [28] Eric Jang, Alex Irpan, Mohi Khansari, Daniel Kappler, Frederik Ebert, Corey Lynch, Sergey Levine, and Chelsea Finn. Bc-z: Zero-shot task generalization with robotic imitation learning. In _Conference on Robot Learning_ , pages 991– 1002. PMLR, 2022. 1 

- [29] Siddharth Karamcheti, Suraj Nair, Annie S Chen, Thomas Kollar, Chelsea Finn, Dorsa Sadigh, and Percy Liang. Language-driven representation learning for robotics. _arXiv preprint arXiv:2302.12766_ , 2023. 2 

- [30] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 2, 5 

- [31] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 1, 2, 3, 5, 12, 13, 14, 16 

- [32] Xin Lai, Zhuotao Tian, Yukang Chen, Yanwei Li, Yuhui Yuan, Shu Liu, and Jiaya Jia. Lisa: Reasoning segmentation via large language model. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 9579–9589, 2024. 2 

- [33] Doyup Lee, Chiheon Kim, Saehoon Kim, Minsu Cho, and Wook-Shin Han. Autoregressive image generation using 

   - residual quantization. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 11523–11532, 2022. 3 

- [34] Seungjae Lee, Yibin Wang, Haritheja Etukuru, H. Jin Kim, Nur Muhammad Mahi Shafiullah, and Lerrel Pinto. Behavior generation with latent actions. In _Forty-first International Conference on Machine Learning_ , 2024. 2, 3 

- [35] Bo Li, Yuanhan Zhang, Dong Guo, Renrui Zhang, Feng Li, Hao Zhang, Kaichen Zhang, Yanwei Li, Ziwei Liu, and Chunyuan Li. Llava-onevision: Easy visual task transfer. _arXiv preprint arXiv:2408.03326_ , 2024. 2, 5, 12 

- [36] Jianxiong Li, Jinliang Zheng, Yinan Zheng, Liyuan Mao, Xiao Hu, Sijie Cheng, Haoyi Niu, Jihao Liu, Yu Liu, Jingjing Liu, Yaqin Zhang, and Xianyuan Zhan. Decisionnce: Embodied multimodal representations via implicit preference learning. In _Forty-first International Conference on Machine Learning_ . 2 

- [37] Jianxiong Li, Zhihao Wang, Jinliang Zheng, Xiaoai Zhou, Guanming Wang, Guanglu Song, Yu Liu, Jingjing Liu, YaQin Zhang, Junzhi Yu, et al. Robo-mutual: Robotic multimodal task specification via unimodal learning. _arXiv preprint arXiv:2410.01529_ , 2024. 2 

- [38] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36, 2024. 5, 6, 14 

- [39] Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. Improved baselines with visual instruction tuning. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 26296–26306, 2024. 2 

- [40] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. _Advances in neural information processing systems_ , 36, 2024. 1, 2 

- [41] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 2, 3 

- [42] Yecheng Jason Ma, Vikash Kumar, Amy Zhang, Osbert Bastani, and Dinesh Jayaraman. Liv: Language-image representations and rewards for robotic control. In _International Conference on Machine Learning_ , pages 23301–23320. PMLR, 2023. 2 

- [43] J. MacQueen. Some methods for classification and analysis of multivariate observations. 1967. 3 

- [44] Fabian Mentzer, David Minnen, Eirikur Agustsson, and Michael Tschannen. Finite scalar quantization: Vq-vae made simple. In _The Twelfth International Conference on Learning Representations_ . 3 

- [45] Atharva Mete, Haotian Xue, Albert Wilcox, Yongxin Chen, and Animesh Garg. Quest: Self-supervised skill abstractions for learning continuous control. _arXiv preprint arXiv:2407.15840_ , 2024. 2, 3 

- [46] Yao Mu, Qinglong Zhang, Mengkang Hu, Wenhai Wang, Mingyu Ding, Jun Jin, Bin Wang, Jifeng Dai, Yu Qiao, and Ping Luo. EmbodiedGPT: Vision-language pre-training via embodied chain of thought. In _Thirty-seventh Conference on Neural Information Processing Systems_ , 2023. 16 

22517 

- [47] Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea Finn, and Abhinav Gupta. R3m: A universal visual representation for robot manipulation. In _6th Annual Conference on Robot Learning_ . 2 

- [48] Haoyi Niu, Jianming Hu, Guyue Zhou, and Xianyuan Zhan. A comprehensive survey of cross-domain policy transfer for embodied agents. In _The 33rd International Joint Conference on Artificial Intelligence_ , 2024. 1 

- [49] Abby O’Neill, Abdul Rehman, Abhinav Gupta, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, et al. Open x-embodiment: Robotic learning datasets and rt-x models. _arXiv preprint arXiv:2310.08864_ , 2023. 1, 2, 3, 

   - 5 

- [50] Seohong Park, Tobias Kreiman, and Sergey Levine. Foundation policies with hilbert representations. In _Forty-first International Conference on Machine Learning_ . 4 

- [51] Seohong Park, Dibya Ghosh, Benjamin Eysenbach, and Sergey Levine. Hiql: Offline goal-conditioned rl with latent states as actions. _Advances in Neural Information Processing Systems_ , 36, 2024. 4 

- [52] William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 4195–4205, 2023. 4 

- [53] Jeff Rasley, Samyam Rajbhandari, Olatunji Ruwase, and Yuxiong He. Deepspeed: System optimizations enable training deep learning models with over 100 billion parameters. In _Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining_ , pages 3505–3506, 2020. 5 

- [54] Dominik Schmidt and Minqi Jiang. Learning to act without actions. In _The Twelfth International Conference on Learning Representations_ . 3 

- [55] Nur Muhammad Shafiullah, Zichen Cui, Ariuntuya Arty Altanzaya, and Lerrel Pinto. Behavior transformers: Cloning _k_ modes with one stone. _Advances in neural information processing systems_ , 35:22955–22968, 2022. 2, 3 

- [56] Lucy Xiaoyang Shi, Zheyuan Hu, Tony Z Zhao, Archit Sharma, Karl Pertsch, Jianlan Luo, Sergey Levine, and Chelsea Finn. Yell at your robot: Improving on-the-fly from language corrections. _arXiv preprint arXiv:2403.12910_ , 2024. 2, 16 

- [57] Chan Hee Song, Jiaman Wu, Clayton Washington, Brian M Sadler, Wei-Lun Chao, and Yu Su. Llm-planner: Fewshot grounded planning for embodied agents with large language models. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 2998– 3009, 2023. 16 

- [58] Quan Sun, Qiying Yu, Yufeng Cui, Fan Zhang, Xiaosong Zhang, Yueze Wang, Hongcheng Gao, Jingjing Liu, Tiejun Huang, and Xinlong Wang. Emu: Generative pretraining in multimodality. In _The Twelfth International Conference on Learning Representations_ , 2023. 2 

- [59] Quan Sun, Yufeng Cui, Xiaosong Zhang, Fan Zhang, Qiying Yu, Yueze Wang, Yongming Rao, Jingjing Liu, Tiejun Huang, and Xinlong Wang. Generative multimodal models are in-context learners. In _Proceedings of the IEEE/CVF_ 

_Conference on Computer Vision and Pattern Recognition_ , pages 14398–14409, 2024. 2 

- [60] Gemma Team, Thomas Mesnard, Cassidy Hardin, Robert Dadashi, Surya Bhupatiraju, Shreya Pathak, Laurent Sifre, Morgane Rivi`ere, Mihir Sanjay Kale, Juliette Love, et al. Gemma: Open models based on gemini research and technology. _arXiv preprint arXiv:2403.08295_ , 2024. 4 

- [61] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 1, 2, 3, 5, 12 

- [62] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timoth´ee Lacroix, Baptiste Rozi`ere, Naman Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open and efficient foundation language models. _arXiv preprint arXiv:2302.13971_ , 2023. 1, 2 

- [63] Aaron Van Den Oord, Oriol Vinyals, et al. Neural discrete representation learning. _Advances in neural information processing systems_ , 30, 2017. 2, 3, 4, 13 

- [64] Homer Rich Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, Philippe Hansen-Estruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pages 1723–1736. PMLR, 2023. 1, 2, 5, 6, 12 

- [65] Lirui Wang, Xinlei Chen, Jialiang Zhao, and Kaiming He. Scaling proprioceptive-visual learning with heterogeneous pre-trained transformers. _arXiv preprint arXiv:2409.20537_ , 2024. 1, 2 

- [66] Chuan Wen, Xingyu Lin, John So, Kai Chen, Qi Dou, Yang Gao, and Pieter Abbeel. Any-point trajectory modeling for policy learning. _arXiv preprint arXiv:2401.00025_ , 2023. 2, 16 

- [67] Hongtao Wu, Ya Jing, Chilam Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and Tao Kong. Unleashing large-scale video generative pre-training for visual robot manipulation. In _The Twelfth International Conference on Learning Representations_ . 2 

- [68] Jonathan Yang, Catherine Glossop, Arjun Bhorkar, Dhruv Shah, Quan Vuong, Chelsea Finn, Dorsa Sadigh, and Sergey Levine. Pushing the limits of cross-embodiment learning for manipulation and navigation. _arXiv preprint arXiv:2402.19432_ , 2024. 1, 3 

- [69] Seonghyeon Ye, Joel Jang, Byeongguk Jeon, Sejune Joo, Jianwei Yang, Baolin Peng, Ajay Mandlekar, Reuben Tan, Yu-Wei Chao, Bill Yuchen Lin, et al. Latent action pretraining from videos. _arXiv preprint arXiv:2410.11758_ , 2024. 2, 3, 4, 5 

- [70] Haoqi Yuan, Zhancun Mu, Feiyang Xie, and Zongqing Lu. Pre-training goal-based models for sample-efficient reinforcement learning. In _The Twelfth International Conference on Learning Representations_ , 2024. 3 

- [71] Michał Zawalski, William Chen, Karl Pertsch, Oier Mees, Chelsea Finn, and Sergey Levine. Robotic control via embodied chain-of-thought reasoning. In _8th Annual Conference on Robot Learning_ , 2024. 16 

22518 

- [72] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 7 

- [73] Jinliang Zheng, Jianxiong Li, Sijie Cheng, Yinan Zheng, Jiaming Li, Jihao Liu, Yu Liu, Jingjing Liu, and Xianyuan Zhan. Instruction-guided visual masking. _Advances in neural information processing systems_ , 2024. 2 

22519 

