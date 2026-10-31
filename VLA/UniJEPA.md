---
title: "UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning"
date: "2025-10-12"
authors: "Jianke Zhang; Yucheng Hu; Yanjiang Guo; Xiaoyu Chen; Yichen Liu; Wenna Chen"
venue: "ICML 2026"
url: https://arxiv.org/abs/2510.10642
pdf: https://arxiv.org/pdf/2510.10642
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2510.10642)** / [論文ページ](https://arxiv.org/abs/2510.10642)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning** 

**Jianke Zhang**<sup>* 1</sup> **Yucheng Hu**<sup>* 1</sup> **Yanjiang Guo**<sup>1</sup> **Xiaoyu Chen**<sup>1</sup> **Yichen Liu**<sup>1</sup> **Wenna Chen**<sup>2</sup> **Chaochao Lu**<sup>3</sup> **Jianyu Chen**<sup>1 4</sup> 

## **Abstract** 

## **1. Introduction** 

Building generalist robot policies that can handle diverse tasks in open-ended environments is a central challenge in robotics. To leverage knowledge from large-scale pretraining, prior work has typically built generalist policies either on top of vision-language understanding models (VLMs) or generative models. However, both semantic understanding from vision-language pretraining and visual dynamics modeling from visualgeneration pretraining are crucial for embodied robots. Recent unified models of generation and understanding have demonstrated strong capabilities in both comprehension and generation through large-scale pretraining. We posit that robotic policy learning can likewise benefit from the combined strengths of understanding, planning and continuous future representation learning. Building on this insight, we introduce UniJEPA, which acquires the ability to dynamically model high-dimensional visual features through pretraining on over 1M internet-scale instructional manipulation videos. Subsequently, UniJEPA is fine-tuned on data collected from the robot embodiment, enabling the learning of mappings from predictive representations to action tokens. Extensive experiments show our approach consistently outperforms baseline methods in terms of 9% and 12% across simulation environments and real-world out-of-distribution tasks. Project page at https://sites.google.com/view/unijepa. 

*Equal contribution 1Institute for Interdisciplinary Information Sciences, Tsinghua University, Beijing, China.<sup>2</sup> Peking University, Beijing, China<sup>3</sup> Shanghai AI Lab, Shanghai, China<sup>4</sup> Shanghai Qi Zhi Institute, Shanghai, China. Correspondence to: Jianyu Chen _<_ jianyuchen@tsinghua.edu.cn _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 

Constructing generalist foundation models (Zitkovich et al., 2023; Kim et al., 2024b) for robots manipulation in the physical world has emerged as a rapidly growing frontier within embodied AI. Vision–language–action (VLA) models aim to learn robotic policies from data annotated with vision, linguistic, and action signals. However, the scarcity of robotic data and the heterogeneity across embodiments present substantial challenges, particularly in achieving generalization to novel scenes and task instructions, and in accurately predicting actions. 

To mitigate these limitations, recent studies have explored mapping Vision–Language Models (VLMs) into the action space(Black et al., 2024; Team et al., 2024). This strategy provides robot policies with alignment priors across language and vision modalities. Nevertheless, these approaches often overlook the fundamental discrepancies between robotic action tasks and vision–language tasks. Unlike the abundance of internet-scale vision–language data, fine-tuning VLMs on limited robotic datasets frequently leads to degradation of their foundational capabilities (Xing et al., 2025). Complementary lines of work have investigated leveraging generation models as intermediaries for action policy learning(Hu et al., 2024; Wen et al., 2024). While such visual foresight approaches facilitate dynamic representation learning and enable the use of heterogeneous data sources, they typically fail to preserve vision–language alignment inherent to pretrained VLMs. These observations highlight a central insight: it is crucial to design robotspecific post-training paradigms tailored to embodied scenarios. Upon re-examining this line of approaches, we observe that both language understanding and future state prediction can provide preliminary guidance for general manipulation tasks. The unified learning strategy further enables the model to acquire representations beneficial for robotic tasks from a broader range of data. 

Building upon these insights and prior advances in vision–language–action (VLA) research(Zhang et al., 2025a; Wang et al., 2025b), we propose UniJEPA, which follows an understanding–generation–execution paradigm that integrates discrete task comprehension with continuous pre- 

1 

**UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning** 


_Figure 1._ **Overview of UniJEPA.** Our proposed UniJEPA, which utilizes both understanding and prediction tasks under discrete and continuous representation space, demonstrates strong semantic generalization capabilities on real-world manipulation tasks, particularly in its ability to handle completely novel objects not seen during training. The upper right displays benchmark evaluations across several simulations and 2 real-world robots. 

diction of future robotic states. To address heterogeneous modalities, UniJEPA employs a MoT architecture (Liang et al., 2024) with modality-specialized experts. UniJEPA is trained in two stages to introduce continuous feature forecasting to action learning while maintaining general capabilities within VLM. In the first stage, we curate and label a diverse collection of Embodied QA data sourced from both robots(Khazatsky et al., 2024; Bu et al., 2025; Wu et al., 2024) and human demonstrations(Hoque et al., 2025; Grauman et al., 2022). We enable the model to learn discrete language representations for understanding of embodied scenes and continuous visual representations for world modeling. In the second stage, we introduce embodimentspecific robotic data annotated with action behaviors. By jointly predicting continuous visual futures and actions, the model learns to utilize semantically aligned features that are rich in dynamic information. This, in turn, equips the VLA policy with better generalization capabilities for new objects and scenes. 

In experiments, UniJEPA achieves a 9% improvement in the Simpler benchmark compared to existing SOTA approach and demonstrates strong semantic generalization for realworld robots for complex tasks on both robot arms and dexterous hands, with a 12% improvement on unseen tasks of the dexterous hand. In summary, our contributions are as 

### follows: 

- We propose a novel vision–language–action (VLA) that integrates both discrete and continuous representations for understanding and learning dynamics, which is pre-trained on large-scale data from both robot and human demonstrations, enabling effective transfer to embodied tasks. 

- We propose a two-stage training framework that aligns 

- action representations while preserving the aligned intermediate representations. 

- Our best-performing model achieves state-of-the-art results across both simulated and real-world environments, and we further analyze the impact of different feature design choices on the model’s capabilities. 

## **2. Related Works** 

**Vision-Language-Action Models** Vision-LanguageAction (VLA) models introduce multimodal large language models (Dai et al., 2024; Touvron et al., 2023; Wang et al., 2025a; Bai et al., 2025; Zhang et al., 2026) into robot policy models to enhance their generalization ability (Brohan et al., 2023; Kim et al., 2024a; Black et al., 2024; Guo et al., 2025). This line of work either utilizes the VLM and an action head for end-to-end action prediction (Li 

2 

**UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning** 

et al., 2023; Wen et al., 2025) or uses the VLM to extract key information to condition downstream policy (Zhang et al., 2024; Li et al., 2025). Some recent works have introduced additional auxiliary tasks to VLAs, including enhancing spatial understanding (Qu et al., 2025), QA reasoning (Zhou et al., 2025), visual reasoning (Zhao et al., 2025) and prediction (Zhang et al., 2025b;a), demonstrating that both general-purpose understanding and generation capabilities can promote action learning. However, these methods are primarily limited to unifying generative tasks within a discrete token prediction framework, which may compromise the robust vision-language alignment inherent in the pre-trained VLM. In this work, we incorporate a continuous-space visual prediction task to aid downstream action learning. 

**Generalist Robot Policies with Joint Prediction** Explorations into generalist robot policies have considered using world models (Blattmann et al., 2023; Assran et al., 2025; Chen et al., 2024; Guo et al., 2024) to learn physical dynamics and subsequently predict actions (Du et al., 2024; Black et al., 2023). Many recent methods have incorporated prediction into larger-scale data and models: GR-1 (Wu et al., 2023) utilizes video pre-training to initialize the action policy; VPP (Hu et al., 2024) uses a video foundation model as the visual encoder for action policy. While these methods fully leverage the rich information from video data, they lack semantic grounding capabilities due to the absence of large language models. Recent works (Zhang et al., 2025a; Wang et al., 2025b; Zhang et al., 2025b) use VQ quantization to incorporate predictive generation tasks into VLA policies, demonstrating the potential for unifying understanding and prediction. In contrast, we utilize continuous visual features as the prediction supervision signal and pre-train our model on large-scale language prediction and continuous visual prediction tasks. 

## **3. Methodology** 

In this section, we present the overall framework design and the two-stage training strategy of UniJEPA, as illustrated in Figure 2. In the first stage, UniJEPA is trained to learn joint text–image representations across diverse manipulation datasets, including understanding, planning, and continuous future prediction tasks. In the subsequent stage, an action expert is employed to integrate the multimodal inputs and predicted future states with action. In the subsequent subsections, we will respectively describe: (1) the joint visual-language embedding learning for pre-training in Sec 3.1, (2) our policy learning method in Sec 3.2, and (3) the implementation details and training data in Sec 3.3. 

### **3.1. Unified Vision Language Embedding Modeling** 

Before introducing the robot action space, we first establish a cross-embodiment pre-training paradigm for robots. In this stage, a subset of the model parameters _Uv,l_ is jointly optimized via the Text-Image to Embedding(TI2E) (examples can be found in A.5). Concretely, given a language instruction _l_ and the current view observations _ot_ at time _t_ , UniJEPA is trained to predict the joint visual–text embedding: _o_ ˆ _t_ + _h,_<sup>ˆ</sup> _l_ = _Uv,l_ ( _ot, l_ ) , where _o_ ˆ _t_ + _h_ = _V_ ( _ot_ + _h_ ) = _{c_ 1 _, c_ 2 _, . . . , cn}_ denotes the predicted continuous future representation encoded by the visual encoder _V_ , while ˆ _l_ = _{d_ 1 _, d_ 2 _, . . . , dm}_ corresponds to the _m_ -token textual sequence. 

**Discrete Representation Learning.** To enhance vision–language alignment, the parameters _Uv,l_ are initialized from a pre-trained vision–language model. Fine-grained language representations are derived from large-scale vision–language datasets, as well as planning and scene descriptions from embodied tasks, which are annotated using pre-trained MLLM into a VQA-style format. This target enables the agent to gain a better understanding of diverse instructions and scenes, thereby facilitating the learning of continuous representations for visual prediction and action. 

**World Modeling under Continuous Space.** In the pretraining stage, to acquire dynamic representations associated with the action space, we introduce additional attention weights dedicated to future state prediction, which are integrated with the original VLM within the mixtureof-transformers framework. Unlike prior approaches that directly predict image pixels, we leverage a frozen visual encoder to represent future observations in a continuous high-dimensional space, capturing high-level information across different semantics. A more detailed discussion can be found in Appendix A.1. 

For the visual inputs, we employ a dual-encoder design that combines the VLM visual encoder with a generator encoder. The tokens generated by the latter are processed by the generative expert in the mixture-of-transformers and, together with the language tokens and VLM visual tokens, jointly participate in the attention computation. This design preserves the pretrained model’s vision–language alignment while enabling the prediction process to benefit from richer semantic understanding. 

**Training Objective.** The visual and language inputs are processed respectively through the MoT framework, then autoregresively generate<sup>ˆ</sup> _lt_<sup>_pred_</sup> + _h_<sup>=</sup><sup>_d_</sup> 1:<sup>_pred_</sup> _m_<sup>, while the generation</sup> expert obtains the _o_ ˆ<sup>_pred_</sup> _t_ + _h_<sup>=</sup><sup>_c_</sup> 1:<sup>_pred_</sup> _n_<sup>.We follow the standard</sup> setup of generative–understanding models, employing crossentropy loss for the language branch and mean squared error loss for the generative branch. This optimaze progress can 

3 

**UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning** 


_Figure 2._ **Illustration of the UniJEPA framework.** UniJEPA adopts a MoT framework to handle text understanding and planning, continuous visual prediction, and action execution. The continuous features are derived from future observations using a frozen vision encoder. 

be formulated as: 

the unified model _Uv,l,a_ is trained to approximate vector fields as: 


### **3.2. Unified Action Modeling** 

In the previous stage, we obtained _Uv,l_ through pre-training, which endowed the model with basic capabilities in future state prediction and vision–language alignment. However, _Uv,l_ cannot yet be directly mapped to the action space. To address this limitation, in the second stage we fine-tune _Uv,l_ on embodiment data comprising visual, language, and action modalities, while simultaneously training an action expert from scratch to construct _Uv,l,a_ . 

**Action & State Expert.** Similar to the generation and understanding experts, we employ distinct attention weights to project actions and states (i.e., proprioception) into a shared attention space. Unlike the other experts, the action expert leverages flow matching to capture the continuous and inherently multi-modal distribution of the action space. Proprioceptive signals _st_ are processed by an MLP-based state expert encoder, enabling fusion within the unified model. Given an action sequence _At_ = ( _at, at_ +1 _, . . . , at_ + _h_ ) to be executed, along with the observation _ot_ and instruction _l_ , 

where _A_<sup>_ε_</sup> _t_<sup>= (1</sup><sup>_→ω_)</sup><sup>_ε_+</sup><sup>_ωAt_denotes the interpolated actions</sup> at step _ω_ , and _ε ↓N_ (0 _, I_ ). 

In this action training stage, we also jointly optimize the generation expert by predicting the future observation states _c_ 1: _n_ , yielding the following objective: 


### **3.3. Implementation Details** 

**Model Setting.** UniJEPA employs Paligemma (Beyer et al., 2024) as the VLM expert. For future observation encoding, we experiment with SigLIP (Tschannen et al., 2025), DINOv3 (Simeoni et al.´ , 2025), and direct pixel-level prediction. Considering the information flow across modalities, we adopt a block-wise masking mechanism in the MoT attention: within each modality, bidirectional attention is applied, while across modalities a causal mask is enforced following the order of image, language, image prediction, 

4 

**UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning** 

state information, and action. UniJEPA comprises 2.9B parameters, including a 2.3B VLM, 0.3B generation expert, and 0.3B action expert. Although the additional experts introduce extra parameters, they only increase the pre-training overhead and do not lead to higher inference latency. 

**Pre-training Data.** In the pretraining stage, we utilize three categories of data to acquire joint text–image representations: (1) 320k robot videos paired with fine-grained subtask descriptions and overall task instructions, which yield VQA and TI2E data for the generation–understanding task; (2) 870k robot and human operation videos accompanied by task instructions, which are used as TI2E data; and (3) 560k generic vision–language question answering data, employed for co-training to preserve the fundamental capabilities of the VLM. In the action modeling stage, we exclusively adopt VLA data collected in both simulation and real-world robotic environments. Further details regarding the datasets are provided in Appendix A.5. 

## **4. Experiment** 

To comprehensively evaluate our proposed method, UniJEPA, we conduct extensive experiments across two simulation benchmarks and on two distinct real-world robotic platforms. Our experiments are designed to assess the performance of UniJEPA and validate the effectiveness of our proposed modules and training scheme. 

### **4.1. Experimental Setup** 

Our experiments are conducted and deployed across four distinct environments. Figure **??** illustrates a selection of tasks from both our simulation and real-world settings. 

**Calvin Benchmark** Calvin is a simulation benchmark designed for evaluating long-horizon, language-conditioned manipulation policies. We employ the _ABC-D_ split to evaluate the single-view generalization capabilities of the models. The evaluation suite includes 1,000 long-horizon sequences, each of length 5. We report the average length of completed sub-task sequences. 

**SimplerEnv Benchmark** SimplerEnv is a simulation benchmark designed to evaluate policies trained on realworld datasets, such as Bridge-V2 and Fractal. The benchmark supports two types of robot arms: WindowX and Google Robot. For our evaluation, we conduct 240 runs for each task and report the average success rate. 

**Real-World Franka Emika Panda Arm** We deploy models on a Franka Emika arm for real-world task comparison. We first collected a dataset of 2,000 trajectories spanning over 20 distinct tasks, encompassing six fundamental skills: picking, placing, opening a drawer, closing a drawer, pressing a button, and routing a cable. We evaluate performance 

_Table 1._ Long-horizon evaluation on the Calvin ABC _→_ D benchmark. We compared the performance of different methods using visual prediction. Entries marked with * are methods reproduced with our training and test settings. We _only use a single 224x224 third-view image_ as input in all methods. 

|**Method**||**Tasks co**|**mpleted**|**in a row**||**AvgLen**_→_|
|---|---|---|---|---|---|---|
||**1**|**2**|**3**|**4**|**5**|**. **|
|GR-1|0.854|0.712|0.596|0.497|0.401|3.06|
|VPP*|0.909|0.815|0.713|0.620|0.518|3.58|
|UP-VLA*|0.928|0.865|0.815|0.769|0.699|4.08|
|UniJEPA (Ours)|0.973|0.895|0.823|0.752|0.670|4.11|


on both seen and unseen task variations. The unseen category primarily involves grasping novel objects not present in the training data and introducing misleading objects. More details can be found in Appendix A.3.1. 

**Real-World 12-DOF Dexterous Hand** On our dexterous manipulation platform, we train different models using a dataset of 4,000 trajectories across more than 100 tasks. The models are then evaluated in a variety of seen and unseen scenarios, which cover 13 distinct skills in 9 categories. More details can be found in Appendix A.3.2. 

### **4.2. Simulation Experiments** 

**Implementation Details** We first pre-train UniJEPA following the methodology described in Section 3. Subsequently, we fine-tune the model on 8 A100 GPUs for 22k steps, using a learning rate of 5 _↔_ 10<sup>_↑_5</sup> and a batch size of 1024. For all simulation training, we consistently use a single, third-person-view image of size 224 _↔_ 224 as the visual input. In Calvin, we use an action chunk size of 10, and during deployment, the full 10-step chunk is executed at each inference step. In SimplerEnv, we use an action chunk size of 4; for the WindowX environment (corresponding to the Bridge dataset), the full 4-step chunk is executed, whereas for the Google Robot environment (corresponding to the Fractal dataset), half of the action chunk is executed. 

**Baselines** We compare UniJEPA against several stateof-the-art VLA policies. On SimplerEnv, we benchmark UniJEPA against RT-1-X (Brohan et al., 2022), Octo (Team et al., 2024), OpenVLA-OFT (Kim et al., 2024a), RoboVLMs (Liu et al., 2025), _ϑ_ 0 (Black et al., 2024), GR00T-N1.5(NVIDIA et al., 2025), CogAct (Li et al., 2024) and Villa-x (Chen et al., 2025). On Calvin, we compare UniJEPA against several policies that leverage visual generation tasks, including GR-1 (Wu et al., 2023), VPP (Hu et al., 2024), and UP-VLA (Zhang et al., 2025a). To ensure a fair comparison, we reproduce these baselines and standardize their visual input to a single third-person view. 

5 

**UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning** 

_Table 2._ Results on SimplerEnv-WindowsX (visual matching). Entries marked with * are methods we reproduced with our training and test settings. 

|**Model**|**Size**|Carrot<br>|on Plate<br>|Eggplant<br>|in Basket<br>|Spoon o<br>|n Towel<br>|Stac<br>|k Cube<br>|Success<br>|
|---|---|---|---|---|---|---|---|---|---|---|
|||**Grasp**|**Success**|**Grasp**|**Success**|**Grasp**|**Success**|**Grasp**|**Success**|**Average**|
|RT-1-X|35M|20.8|4.2|0.0|0.0|16.7|0.0|8.3|0.0|1.1|
|Octo-Base|0.1B|52.8|8.3|66.7|43.1|34.7|12.5|31.9|0.0|16.0|
|OpenVLA-OFT|7B|41.7|4.2|91.7|37.5|50.0|12.5|70.8|8.3|39.6|
|RoboVLMs|2B|33.3|20.8|91.7|79.2|70.8|45.8|54.2|4.2|37.5|
|_ϑ_0*|2.6B|58.5|48.8|78.8|64.6|83.3|73.3|62.5|12.5|49.8|
|_ϑ_0-Fast|2.6B|58.5|21.9|**83.3**|66.6|62.5|29.1|54.0|10.8|48.3|
|CogAct|7B|/|58.3|/|45.8|/|29.2|/|**95.8**|57.3|
|GR00T-N1.5|3B|/|54.3|/|61.3|/|75.3|/|57.0|62.0|
|Villa-x|3B|/|46.3|/|64.6|/|77.9|/|61.3|62.5|
|UniJEPA (Ours)|2.9B|**75.0**|**63.0**|**100.0**|**89.6**|**83.3**|**78.8**|**91.7**|52.5|**71.0**|


_Table 3._ Results on SimplerEnv-Google Robot (visual matching). Entries marked with * are methods reproduced with our training and test settings. 

|**Model**|Pick<br>Coke|Move<br>Near|O./C.<br>Drawer|Put in<br>Drawer|AVG_→_|
|---|---|---|---|---|---|
|RT-1-X|56.7|31.7|59.7|21.3|42.4|
|Octo-Base|17.0|4.2|22.7|0.0|11.0|
|OpenVLA-OFT|72.3|69.6|47.2|62.9|63.0|
|RoboVLMs|77.3|61.7|43.5|24.1|51.7|
|_ϑ_0*|93.3|78.1|23.6|12.5|51.9|
|_ϑ_0-Fast|75.3|67.5|42.9|62.0|61.9|
|CogACT|91.3|**85.0**|**71.8**|50.9|74.8|
|GR00T-N1.5|69.3|68.7|35.8|60.0|57.9|
|Villa-x|**98.7**|75.0|59.3|5.6|59.6|
|UniJEPA (Ours)|**98.7**|81.5|63.2|**70.0**|**78.4**|


also leverage visual prediction during VLA training on the Calvin ABC-D split, with results shown in Table 1. Since many prior works utilize multi-view images and historical information, we re-implemented these baselines using a standardized single, third-person-view image as visual input to ensure a fair comparison of the benefits conferred by our training method. The results demonstrate that UniJEPA achieves the best performance on single-view manipulation tasks within the Calvin benchmark. Moreover, when compared to the baseline _ϑ_ 0, our method again exhibits a performance improvement, consistent with the results on SimplerEnv. 

### 4.2.1. PERFORMANCE ON SIMULATION BENCHMARKS 

Tables 2 and 3 present the performance of our method on the SimplerEnv-WindowX and SimplerEnv-Google Robot benchmarks, respectively. We report the officially published results of other methods for comparison. On both robotic platforms, our method achieves the highest success rates of 71.0% and 78.4%, attaining state-of-the-art (SOTA) performance. It is evident that UniJEPA demonstrates consistently high success rates across all sub-tasks. This contrasts with other methods, which often exhibit _“spiky”_ performance profiles—excelling on some tasks while performing poorly on others. This finding underscores the superior multi-task learning capabilities of our approach. 

Furthermore, for a fair, apple-to-apple comparison with the architecturally similar _ϑ_ 0 baseline, we reproduced it within our identical training and evaluation framework. Across both environments, we found that the novel components in UniJEPA yield a significant performance uplift of over 20%. We also observed that this improvement is consistently present at every training checkpoint, indicating that the stable gains can be attributed to our method’s ability to learn continuous future features and discrete representations simultaneously. 

We also compare UniJEPA against several policies that 

### **4.3. Real World Experiments** 

**Implementation Details** We fine-tune the pre-trained UniJEPA model separately on the datasets collected from our two real-world robotic platforms to evaluate its performance on a variety of seen and unseen tasks. The fine-tuning process is conducted for 10 epochs using a batch size of 1024 and a learning rate of 5 _↔_ 10<sup>_↑_5</sup> , with both the prediction horizon and action chunk length set to 10. For the Franka Emika Panda arm, the model is fine-tuned on 2,000 trajectories, and during deployment, we evaluate both full and half action chunk execution, reporting the superior result. On the XArm with a 12-DOF dexterous hand, we use a larger dataset of 4,000 trajectories and execute the full 10-step action chunk at each inference step. We test on seen tasks, which involve familiar objects in novel, randomized positions, and unseen tasks, which introduce novel color, objects, and background. For each task configuration, we conduct 20/50 trials from randomized initial configurations and report the average task success rate. We evaluated three checkpoints for each model and reported the average success rate with error bars. Figure 4 and 5 displays the experimental results of multiple methods on two real-robot embodiments. The bar heights represent the average success rate, while the black error bars indicate the variance across three checkpoints. More details can be found in Appendix A.3. 

6 

**UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning** 


_Figure 4._ Results on real-world 7DOF robotarm experiment. Detailed results are provided in Table 7. 


_Figure 5._ Results on real-world 12-DOF dexterous hands experiment. Detailed results can be found in Table 8. 

### 4.3.1. PERFORMANCE ON REAL WORLD EXPERIMENTS 

We compare UniJEPA against OpenVLA(Kim et al., 2024a), GR-1 (Wu et al., 2023), _ϑ_ 0 (Black et al., 2024), UP-VLA (Zhang et al., 2025a) and VPP (Hu et al., 2024) in two environments, visualizing the results in Figure 4 and 5. 

Our method achieves the highest overall task success rates on both real-world robotic platforms. Specifically, on the Franka Panda arm, UniJEPA attains the best performance across all four task categories, outperforming baselines on both seen and unseen tasks. This demonstrates that our approach effectively enhances both multi-task learning and generalization capabilities. Consistent with our findings in the Simpler simulation environment, our method again shows superior performance over the architecturally similar _ϑ_ 0 baseline across a majority of these real-world tasks. Furthermore, on the more complex 12-DoF dexterous hand platform, UniJEPA achieves the highest average success rate 

across all nine skill categories. Notably, we observe that our method exhibits a significant generalization advantage when dealing with novel objects and scenes. We provide several illustrative examples in Appendix A.4, where the model successfully grasps completely unseen objects and correctly interprets out-of-distribution (OOD) language descriptions. 

These consistent, state-of-the-art results across two morphologically distinct robots validate the effectiveness and broad applicability of our proposed method. 

### **4.4. Ablation Study** 

In this section, we conduct a series of ablation studies to validate the effectiveness of the different components within UniJEPA. These experiments investigate the role of our continuous visual representations, the impact of our largescale pre-training phase involving both language and visual prediction, and a comparison of several continuous vision 

7 

**UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning** 

_Table 4._ Ablation study on choice of continuous vision features on Simpler. 

|**Method**||**G**|**oogle robo**|**t**|||**Wido**|**wX robot**|||
|---|---|---|---|---|---|---|---|---|---|---|
||Pick|Move|Drawer|Put|**AVG**|Carrot|Eggplant|Spoon|Cube|**AVG**|
|UniJEPA-Distill|97.2|82.6|**61.9**|**74.4**|**79.0**|48.8|**95.8**|**89.6**|34.6|67.2|
|UniJEPA-Dino|**98.3**|**80.2**|51.1|63.3|73.2|54.6|81.7|78.8|49.6|66.1|
|UniJEPA-Siglip|97.7|80.2|61.3|72.4|77.9|**60.8**|87.1|78.8|**50.4**|**69.3**|


encoding methods proposed in Sec 3. 

_Table 5._ Ablation on different pretrain settings on real-world Xarm. 

|**Model**|Pick & Place|Relocate cup|Pick & Place(Unseen)|**AVG**_↗_|
|---|---|---|---|---|
|UniJEPA|75.0|82.5|72.5|76.7|
|w/o pre-training|65.0|70.0|47.5|60.8|
|w/o Discrete-Pretrain|72.5|85|57.5|71.7|


_Table 6._ Ablation study on unified pretraining paradigm and continuous feature for prediction. 

|**Model**|Carrot|Eggplant|Spoon|Cube|**AVG**_→_|
|---|---|---|---|---|---|
||w/o|Pretrain||||
|w/o Continuous|48.8|64.6|73.3|12.5|49.8|
|w/o Continuous w/ Pred|52.5|79.2|79.6|30.0|60.3|
|UniJEPA|60.8|87.1|78.8|50.4|69.3|
||w/|Pretrain||||
|UniJEPA (Ours)|**63.0**|**89.6**|**78.8**|**52.5**|**71.0**|


**Effectiveness of Large-Scale Planning and Prediction Pre-training** Table 5 and 6 present a comparison between UniJEPA with and without pre-training. Overall, pretraining improves the success rate across all tasks, yielding a performance gain of approximately 16% on real-world pick and place tasks. During fine-tuning, we observe that leveraging large-scale external data for future and language prediction accelerates the model’s convergence on the robotics dataset. This effect is particularly pronounced in the convergence of the future prediction loss. This indicates that our joint pre-training scheme, which combines continuous and discrete prediction, provides a superior model initialization, especially for the prediction expert module, which translates to tangible benefits during downstream fine-tuning. 

**Effectiveness of Continuous Predictive Visual Representations** To validate the effectiveness of prediction using continuous representations, we compare a version of UniJEPA without pre-training against two baselines, as shown in Table 6. We evaluate the following without using pretraining: (1) w/o Continuous ( _ϑ_ 0), where the modules for predicting continuous future features (including the auxiliary prediction expert and its corresponding encoder/decoder) are removed. (2) w/Pred, which predicts future raw pixels using a two-layer MLP. This helps us elucidate the trade-offs between using high-level visual features versus raw pixels as the predictive signal. The results in w/o Pretrain section of the table show that our proposed 

continuous visual feature prediction boosts performance by approximately 20%. Furthermore, the comparison with w/Pred reveals that continuous features are indeed a more effective signal for future prediction, enabling the model to extract dynamic information crucial for action generation. 

**Choice of Continuous Visual Prediction** We further compare the different encoding methods for future prediction proposed in our methodology. Specifically, we evaluate three distinct approaches (all without pre-training), with results on both Simpler environments shown in Table 4: (1) UniJEPA-Distill, which takes the input embeddings of the ViT (from the current frame) as input to the prediction expert and predicts the output features of ViT for the future frame. This approach is analogous to distilling knowledge from the ViT encoder itself. (2) UniJEPA-Dino and (3) UniJEPASiglip, which take the output features of their respective vision encoders (DINO (Simeoni´ et al., 2025) or SigLIP (Tschannen et al., 2025)) for the current frame as input to predict the corresponding features for the future frame. The results show that UniJEPA-Siglip demonstrates better performance on both benchmarks, and consequently, we select SigLIP as the vision encoder for our UniJEPA model. Notably, on Google Robot environment, UniJEPA-Distill achieves better performance than the UniJEPA-Siglip when neither is pre-trained. This suggests that the distillation-style architecture has inherent advantages. In contrast, UniJEPADino performs significantly worse than the other two. This is likely because the DINO feature space is not aligned with the VLM backbone. Conversely, since SigLIP is the native vision encoder for Paligemma, its feature space is naturally more aligned with that of the VLM expert, facilitating more effective integration within the prediction expert. 

## **5. Conclusion** 

In this paper, we introduce **UniJEPA** , a Vision-LanguageAction (VLA) framework that enhances policy learning by integrating discrete token prediction with continuous visual prediction. During the pre-training stage, we leverage embodied VQA and robotic planning tasks to align the discrete language features of a Vision-Language Model (VLM). Concurrently, we train a predictive module on large-scale video data to forecast future continuous visual features. These two components—the VLM backbone and the prediction module—are effectively fused using a Mixture-of-Experts 

8 

**UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning** 

(MoE) Transformer architecture. In the subsequent action fine-tuning stage, an action expert is incorporated, and the entire model is fine-tuned on a joint objective of continuous action generation and future feature prediction. Our method achieves state-of-the-art (SOTA) performance in two distinct simulation environments. Furthermore, on real-world hardware, including a 7-DoF robot arm and a 12-DoF dexterous hand, our model demonstrates superior performance and stronger semantic generalization, particularly when handling novel objects not encountered during training. 

## **Impact Statement** 

This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here. 

## **References** 

- Assran, M., Bardes, A., Fan, D., Garrido, Q., Howes, R., Muckley, M., Rizvi, A., Roberts, C., Sinha, K., Zholus, A., et al. V-jepa 2: Self-supervised video models enable understanding, prediction and planning. _arXiv preprint arXiv:2506.09985_ , 2025. 

- Bai, S., Cai, Y., Chen, R., Chen, K., Chen, X., Cheng, Z., Deng, L., Ding, W., Gao, C., Ge, C., Ge, W., Guo, Z., Huang, Q., Huang, J., Huang, F., Hui, B., Jiang, S., Li, Z., Li, M., Li, M., Li, K., Lin, Z., Lin, J., Liu, X., Liu, J., Liu, C., Liu, Y., Liu, D., Liu, S., Lu, D., Luo, R., Lv, C., Men, R., Meng, L., Ren, X., Ren, X., Song, S., Sun, Y., Tang, J., Tu, J., Wan, J., Wang, P., Wang, P., Wang, Q., Wang, Y., Xie, T., Xu, Y., Xu, H., Xu, J., Yang, Z., Yang, M., Yang, J., Yang, A., Yu, B., Zhang, F., Zhang, H., Zhang, X., Zheng, B., Zhong, H., Zhou, J., Zhou, F., Zhou, J., Zhu, Y., and Zhu, K. Qwen3-vl technical report. _arXiv preprint arXiv:2511.21631_ , 2025. 

- Beyer, L., Steiner, A., Pinto, A. S., Kolesnikov, A., Wang, X., Salz, D., Neumann, M., Alabdulmohsin, I., Tschannen, M., Bugliarello, E., et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- Black, K., Nakamoto, M., Atreya, P., Walke, H., Finn, C., Kumar, A., and Levine, S. Zero-shot robotic manipulation with pretrained image-editing diffusion models. _arXiv preprint arXiv:2310.10639_ , 2023. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _pi_ ~~0~~ : A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Blattmann, A., Dockhorn, T., Kulal, S., Mendelevitch, D., Kilian, M., Lorenz, D., Levi, Y., English, Z., Voleti, V., 

Letts, A., et al. Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint arXiv:2311.15127_ , 2023. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Chen, X., Choromanski, K., Ding, T., Driess, D., Dubey, A., Finn, C., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 

- Bu, Q., Cai, J., Chen, L., Cui, X., Ding, Y., Feng, S., Gao, S., He, X., Hu, X., Huang, X., et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025. 

- Chen, X., Guo, J., He, T., Zhang, C., Zhang, P., Yang, D. C., Zhao, L., and Bian, J. Igor: Image-goal representations are the atomic control units for foundation models in embodied ai, 2024. URL https://arxiv.org/abs/ 2411.00785. 

- Chen, X., Wei, H., Zhang, P., Zhang, C., Wang, K., Guo, Y., Yang, R., Wang, Y., Xiao, X., Zhao, L., et al. Villax: enhancing latent action modeling in vision-languageaction models. _arXiv preprint arXiv:2507.23682_ , 2025. 

- Comanici, G., Bieber, E., Schaekermann, M., Pasupat, I., Sachdeva, N., Dhillon, I., Blistein, M., Ram, O., Zhang, D., Rosen, E., et al. Gemini 2.5: Pushing the frontier with advanced reasoning, multimodality, long context, and next generation agentic capabilities. _arXiv preprint arXiv:2507.06261_ , 2025. 

- Dai, W., Li, J., Li, D., Tiong, A. M. H., Zhao, J., Wang, W., Li, B., Fung, P. N., and Hoi, S. Instructblip: Towards general-purpose vision-language models with instruction tuning. _Advances in Neural Information Processing Systems_ , 36, 2024. 

- Du, Y., Yang, S., Dai, B., Dai, H., Nachum, O., Tenenbaum, J., Schuurmans, D., and Abbeel, P. Learning universal policies via text-guided video generation. _Advances in Neural Information Processing Systems_ , 36, 2024. 

- Grauman, K., Westbury, A., Byrne, E., Chavis, Z., Furnari, A., Girdhar, R., Hamburger, J., Jiang, H., Liu, M., Liu, X., et al. Ego4d: Around the world in 3,000 hours of egocentric video. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 18995–19012, 2022. 

9 

**UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning** 

- Guo, Y., Hu, Y., Zhang, J., Wang, Y.-J., Chen, X., Lu, C., and Chen, J. Prediction with action: Visual policy learning via joint denoising process. _arXiv preprint arXiv:2411.18179_ , 2024. 

- Guo, Y., Zhang, J., Chen, X., Ji, X., Wang, Y.-J., Hu, Y., and Chen, J. Improving vision-language-action model with online reinforcement learning. _arXiv preprint arXiv:2501.16664_ , 2025. 

- Hoque, R., Huang, P., Yoon, D. J., Sivapurapu, M., and Zhang, J. Egodex: Learning dexterous manipulation from large-scale egocentric video. _arXiv preprint arXiv:2505.11709_ , 2025. 

- Hu, Y., Guo, Y., Wang, P., Chen, X., Wang, Y.-J., Zhang, J., Sreenath, K., Lu, C., and Chen, J. Video prediction policy: A generalist robot policy with predictive visual representations. _arXiv preprint arXiv:2412.14803_ , 2024. 

- Jiang, T., Yuan, T., Liu, Y., Lu, C., Cui, J., Liu, X., Cheng, S., Gao, J., Xu, H., and Zhao, H. Galaxea open-world dataset and g0 dual-system vla model. _arXiv preprint arXiv:2509.00576_ , 2025. 

- Khazatsky, A., Pertsch, K., Nair, S., Balakrishna, A., Dasari, S., Karamcheti, S., Nasiriany, S., Srirama, M. K., Chen, L. Y., Ellis, K., et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 

- Kim, M., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., Vuong, Q., Kollar, T., Burchfiel, B., Tedrake, R., Sadigh, D., Levine, S., Liang, P., and Finn, C. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024a. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ , 2024b. 

- Li, P., Chen, Y., Wu, H., Ma, X., Wu, X., Huang, Y., Wang, L., Kong, T., and Tan, T. Bridgevla: Input-output alignment for efficient 3d manipulation learning with visionlanguage models. _arXiv preprint arXiv:2506.07961_ , 2025. 

- Li, Q., Liang, Y., Wang, Z., Luo, L., Chen, X., Liao, M., Wei, F., Deng, Y., Xu, S., Zhang, Y., et al. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 

- Li, X., Liu, M., Zhang, H., Yu, C., Xu, J., Wu, H., Cheang, C., Jing, Y., Zhang, W., Liu, H., et al. Vision-language foundation models as effective robot imitators. _arXiv preprint arXiv:2311.01378_ , 2023. 

- Liang, W., Yu, L., Luo, L., Iyer, S., Dong, N., Zhou, C., Ghosh, G., Lewis, M., Yih, W.-t., Zettlemoyer, L., et al. Mixture-of-transformers: A sparse and scalable architecture for multi-modal foundation models. _arXiv preprint arXiv:2411.04996_ , 2024. 

- Liu, H., Li, C., Wu, Q., and Lee, Y. J. Visual instruction tuning, 2023. URL https://arxiv.org/abs/2304. 08485. 

- Liu, H., Li, X., Li, P., Liu, M., Wang, D., Liu, J., Kang, B., Ma, X., Kong, T., and Zhang, H. Towards generalist robot policies: What matters in building vision-language-action models. _arXiv preprint arXiv:2412.14058_ , 2025. 

- NVIDIA, Johan Bjorck andFernando Castaneda, N. C., Da,˜ X., Ding, R., Fan, L. J., Fang, Y., Fox, D., Hu, F., Huang, S., Jang, J., Jiang, Z., Kautz, J., Kundalia, K., Lao, L., Li, Z., Lin, Z., Lin, K., Liu, G., Llontop, E., Magne, L., Mandlekar, A., Narayan, A., Nasiriany, S., Reed, S., Tan, Y. L., Wang, G., Wang, Z., Wang, J., Wang, Q., Xiang, J., Xie, Y., Xu, Y., Xu, Z., Ye, S., Yu, Z., Zhang, A., Zhang, H., Zhao, Y., Zheng, R., and Zhu, Y. GR00T N1: An open foundation model for generalist humanoid robots. In _ArXiv Preprint_ , March 2025. 

- Qu, D., Song, H., Chen, Q., Yao, Y., Ye, X., Ding, Y., Wang, Z., Gu, J., Zhao, B., Wang, D., et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- Simeoni, O., Vo, H. V., Seitzer, M., Baldassarre, F., Oquab,´ M., Jose, C., Khalidov, V., Szafraniec, M., Yi, S., Ramamonjisoa, M., et al. Dinov3. _arXiv preprint arXiv:2508.10104_ , 2025. 

- Team, O. M., Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M.-A., Lacroix, T., Roziere, B., Goyal, N., Hambro, E.,` Azhar, F., et al. Llama: Open and efficient foundation language models. _arXiv preprint arXiv:2302.13971_ , 2023. 

- Tschannen, M., Gritsenko, A., Wang, X., Naeem, M. F., Alabdulmohsin, I., Parthasarathy, N., Evans, T., Beyer, L., Xia, Y., Mustafa, B., et al. Siglip 2: Multilingual vision-language encoders with improved semantic understanding, localization, and dense features. _arXiv preprint arXiv:2502.14786_ , 2025. 

- Walke, H. R., Black, K., Zhao, T. Z., Vuong, Q., Zheng, C., Hansen-Estruch, P., He, A. W., Myers, V., Kim, M. J., Du, M., et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pp. 1723–1736. PMLR, 2023. 

10 

**UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning** 

- Wang, W., Gao, Z., Gu, L., Pu, H., Cui, L., Wei, X., Liu, Z., Jing, L., Ye, S., Shao, J., et al. Internvl3. 5: Advancing open-source multimodal models in versatility, reasoning, and efficiency. _arXiv preprint arXiv:2508.18265_ , 2025a. 

- Wang, Y., Li, X., Wang, W., Zhang, J., Li, Y., Chen, Y., Wang, X., and Zhang, Z. Unified vision-language-action model. _arXiv preprint arXiv:2506.19850_ , 2025b. 

- Wen, J., Zhu, Y., Li, J., Tang, Z., Shen, C., and Feng, F. Dexvla: Vision-language model with plug-in diffusion expert for general robot control. _arXiv preprint arXiv:2502.05855_ , 2025. 

- Wen, Y., Lin, J., Zhu, Y., Han, J., Xu, H., Zhao, S., and Liang, X. Vidman: Exploiting implicit dynamics from video diffusion model for effective robot manipulation. _Advances in Neural Information Processing Systems_ , 37: 41051–41075, 2024. 

   - Zhao, Q., Lu, Y., Kim, M. J., Fu, Z., Zhang, Z., Wu, Y., Li, Z., Ma, Q., Han, S., Finn, C., et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 1702–1713, 2025. 

   - Zhou, Z., Zhu, Y., Zhu, M., Wen, J., Liu, N., Xu, Z., Meng, W., Cheng, R., Peng, Y., Shen, C., et al. Chatvla: Unified multimodal understanding and robot control with visionlanguage-action model. _arXiv preprint arXiv:2502.14420_ , 2025. 

   - Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., Wu, J., Wohlhart, P., Welker, S., Wahid, A., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. 

- Wu, H., Jing, Y., Cheang, C., Chen, G., Xu, J., Li, X., Liu, M., Li, H., and Kong, T. Unleashing large-scale video generative pre-training for visual robot manipulation. _arXiv preprint arXiv:2312.13139_ , 2023. 

- Wu, K., Hou, C., Liu, J., Che, Z., Ju, X., Yang, Z., Li, M., Zhao, Y., Xu, Z., Yang, G., et al. Robomind: Benchmark on multi-embodiment intelligence normative data for robot manipulation. _arXiv preprint arXiv:2412.13877_ , 2024. 

- Xing, Y., Luo, X., Xie, J., Gao, L., Shen, H., and Song, J. Shortcut learning in generalist robot policies: The role of dataset diversity and fragmentation. _arXiv preprint arXiv:2508.06426_ , 2025. 

- Zhang, J., Guo, Y., Chen, X., Wang, Y.-J., Hu, Y., Shi, C., and Chen, J. Hirt: Enhancing robotic control with hierarchical robot transformers. _arXiv preprint arXiv:2410.05273_ , 2024. 

- Zhang, J., Guo, Y., Hu, Y., Chen, X., Zhu, X., and Chen, J. Up-vla: A unified understanding and prediction model for embodied agent. _arXiv preprint arXiv:2501.18867_ , 2025a. 

- Zhang, J., Chen, X., Wang, Q., Li, M., Guo, Y., Hu, Y., Zhang, J., Bai, S., Lin, J., and Chen, J. Vlm4vla: Revisiting vision-language-models in vision-language-action models. _arXiv preprint arXiv:2601.03309_ , 2026. 

- Zhang, W., Liu, H., Qi, Z., Wang, Y., Yu, X., Zhang, J., Dong, R., He, J., Lu, F., Wang, H., et al. Dreamvla: a vision-language-action model dreamed with comprehensive world knowledge. _arXiv preprint arXiv:2507.04447_ , 2025b. 

11 

**UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning** 

## **A. Appendix** 

### **A.1. Qualitative Comparison of Encoded Future Visual Representations** 

To qualitatively analyze the characteristics of different encoding methods, we visualize the features they produce. Specifically, we compare features from a single robot trajectory encoded in three ways: raw image pixels, continuous visual features from a ViT encoder, and discrete visual tokens from a VQ-GAN. We selected a trajectory from the Fractal dataset corresponding to the instruction _pick the coffee bag from the drawer onto the table_ . For each frame, the resulting features—raw pixels (flattened from 224 _↔_ 224 _↔_ 3), ViT features (flattened from 256 _↔_ 1152), and VQ-VAE tokens (2048-dim)—are first reduced to 50 dimensions via PCA and then projected into a 2D space using t-SNE for visualization. 


_Figure 6._ t-SNE Visualization of Different Future Representations. 

Figure 6 illustrates the t-SNE visualizations for the trajectory encoded by these three methods. To highlight the temporal evolution, feature points from adjacent frames are connected by lines. 

- **Pixel Features (Left):** This encoding preserves the most low-level information. We observe that despite small visual changes between consecutive frames, the corresponding pixel-level features exhibit high variance, often jumping into regions occupied by features from distant timesteps. This suggests that using raw pixel values as a predictive signal could mislead the policy by causing it to over-emphasize low-level, high-frequency changes. 

- **ViT vs. VQ Features (Center and Right):** A comparison reveals a distinct _“circling phenomenon”_ in the VQ-GAN visualization, where features from many different timesteps collapse into a dense central region. This indicates poor temporal separability in the context of manipulation trajectories. In contrast, the ViT features provide the best separation of the three methods, organizing features from different frames into distinct, minimally overlapping clusters. 

This qualitative analysis supports our insight that continuous features, by virtue of focusing on high-level semantic information, serve as a more stable and suitable predictive signal for robot action policies within our framework. 

### **A.2. Details about Simulation Benchmarks** 

**Calvin Benchmark** Calvin is a simulation benchmark designed for evaluating long-horizon, language-conditioned manipulation policies. It comprises four distinct environments (A, B, C, and D) and offers evaluation splits such as _ABC-D_ and _ABCD-D_ . In our experiments, we employ the _ABC-D_ split to evaluate the single-view generalization capabilities of the models. Models are trained on data collected from environments A, B, and C, and subsequently evaluated in the unseen environment D. This evaluation suite includes 34 different manipulation tasks organized into 1,000 long-horizon sequences, each of length 5. We report the average length of successfully completed sub-task sequences. 

12 

**UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning** 

**SimplerEnv Benchmark** SimplerEnv is a simulation benchmark designed to evaluate policies trained on large-scale real-world datasets, such as Bridge-V2 and Fractal. It procedurally generates scenes that mimic real-world environments using texturing techniques, allowing models trained on real data to be tested directly in simulation without requiring physical deployment. The benchmark supports two types of robot arms: the WindowX and the Google Robot. For our evaluation, we conduct 240 runs for each task and report the average success rate. 

### **A.3. Details on Real World Experiments** 

### A.3.1. FRANKA PANDA ROBOT ARM 

**Real-World Franka Emika Panda Arm** We deploy several models on a Franka Emika Panda arm for real-world task comparison. The robot arm features 7 degrees of freedom (DoF). Its action space is defined by a 7-dimensional vector, where the first six dimensions specify the relative change in the end-effector’s 6D pose (3D position and 3D orientation), and the final dimension controls the binary state of the gripper (open or closed). In our experiments, the policy takes images from an on-board, first-person-view camera as visual input and outputs these relative actions. We first collected a dataset of 2,000 trajectories spanning over 20 distinct tasks, encompassing six fundamental skills: picking, placing, opening a drawer, closing a drawer, pressing a button, and routing a cable. We evaluate performance on both seen and unseen task variations. The unseen category primarily involves grasping novel objects not present in the training data. 

The task suite for the Franka Panda arm includes: 

- **Pick & Place:** Grasping and placing a variety of objects. The training set includes items such as a toy banana, a toy eggplant, red/green/blue blocks, and red/yellow/black plates. 

- **Press Button:** Pressing a toy button using a grasped black block as a tool. 

- **Route Cable:** Routing a thin black rubber cable into a narrow slot. 

- **Drawer Operation:** Opening a toy drawer. 

**Unseen Tasks** These are designed to evaluate generalization: _Novel Objects:_ Grasping objects not seen during training (e.g., toy chili, toy strawberry, yellow block, large toy eggplant, arrow sticker, marker pen). _Distractors:_ Operating in the presence of irrelevant distractor objects. _Visual Variations:_ Adapting to changes in background color and object color. 

We tested UniJEPA, OpenVLA(Kim et al., 2024a), GR-1(Wu et al., 2023), _ϑ_ 0 (Black et al., 2024), UP-VLA (Zhang et al., 2025a) and VPP (Hu et al., 2024) on this environment. The detailed results are shown in Table 7 (corresponding to Figure 4). 

_Table 7._ Detailed results on Franka-Emika Panda Robotarm. We evaluate each task 20 times (100 trials per skill) with random initialization and report the average success rate. We evaluated three checkpoints for each model and reported the average success rate. Error bars for each task are included in the Fig 4. 

|**Model**|Pick|& Place|Press|Button|Rout|e Cable|Dr|awer|**Avg**|**Success**|
|---|---|---|---|---|---|---|---|---|---|---|
||Seen|Unseen|Seen|Unseen|Seen|Unseen|Seen|Unseen|**Seen**|**Unseen**|
|OpenVLA|38|18|65|50|40|20|45|40|47|32|
|GR-1|45|32|80|60|50|50|60|40|59|46|
|UP-VLA|80|70|90|80|65|55|80|70|78|72|
|VPP|88|76|85|80|75|70|85|60|83|72|
|_ϑ_0|90|80|85|70|65|60|80|65|80|69|
|UniJEPA (Ours)|**90**|**85**|**95**|**80**|**80**|**75**|**85**|**80**|**88**|**80**|


### A.3.2. XARM DEXTEROUS MANIPULATION 

**Real-World XArm with 12-DOF X-Hand** Our 12-DoF single-arm dexterous manipulation platform, which comprises a 7-DoF XArm and a 5-DoF hand, is controlled using a dual-view visual input from both first-person and third-person cameras. During evaluation, we test pick-and-place capabilities across 5 distinct task variations for a total of 50 trials. For all other 

13 

**UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning** 

skills, we conduct 20 trials per task. The final performance is reported as the average success rate for each skill. We train different models using a dataset of 4,000 trajectories across more than 100 tasks. The models are then evaluated in a variety of seen and unseen scenarios, which cover 13 distinct skills, e.g., picking, placing, stacking, and pouring. To specifically test for visual generalization, we alter the background colors and novel objects during evaluation in the unseen scenarios. 

The task suite for the XArm platform includes: 

- **Dexterous Pick & Place:** Dexterously grasping and placing a wide range of objects. The training set includes a toy banana, a toy eggplant, a toy orange, small and large toy soccer balls, a computer mouse, a toy drawer, and more. 

- **Move Cup:** Grasping and moving a cup to a different location. 

- **Relocate:** Grasping an object and placing it adjacent to another target object. 

- **Stack Cube:** Placing one block on top of another. 

- **Pass:** Grasping an object and handing it to a human operator. 

- **Press Button:** Directly actuating a toy button with a finger. 

- **Unplug:** Extracting a rubber cable from a socket. 

- **Drawer Operation:** Opening or closing a toy drawer. 

- **Tool Use:** Using various tools, such as a spoon (e.g., for scooping) and a toy hammer (e.g., for striking). 

**Unseen Tasks** These are designed to evaluate generalization: _Novel Objects:_ Grasping unseen objects and placing them to not-seen targets during training (e.g., apple, lemon, glass cup, glass plate, blue plate, toy kapibla, transparent plate, green apple, big ball, and various of novel objects). _Distractors:_ Operating in the presence of irrelevant distractor objects. _Visual Variations:_ Adapting to changes in background color and object color. 

_Table 8._ Detailed results on XArm with dexterous hand. We evaluate 50 times on Pick & Place tasks and 20 trials on other tasks with random initialization and report the average success rate. We evaluated three checkpoints for each model and reported the average success rate. Error bars for each task are included in the Fig 5. 

|**Model**|Pick|& Place|Mo|ve Cup|Re|locate|Stac|k Cube||Pass|
|---|---|---|---|---|---|---|---|---|---|---|
||Seen|Unseen|Seen|Unseen|Seen|Unseen|Seen|Unseen|Seen|Unseen|
|GR-1|40|10|0|0|16|12|0|0|0|0|
|VPP|69|35|64|40|70|66|**64**|44|48|32|
|_ϑ_0|65|45|50|28|75|56|45|40|40|35|
|UniJEPA (Ours)|**75**|**73**|**75**|**45**|**83**|**78**|62|**50**|**50**|**40**|
|**Model**|Press|Button|Un|plug|Dr|awer|To|ol Use|**Avg**|**Success**|
||Seen|Unseen|Seen|Unseen|Seen|Unseen|Seen|Unseen|**Seen**|**Unseen**|
|GR-1|64|40|0|0|48|24|20|/|21|16|
|VPP|96|88|**52**|20|72|56|**75**|/|67|48|
|_ϑ_0|95|90|45|30|**85**|75|42|/|60|50|
|UniJEPA (Ours)|**97**|**95**|40|**35**|80|**77**|65|/|**70**|**62**|


### **A.4. Examples of Demos on OOD-Tasks** 

Examples of video on unseen objects are shown in Figure 7, where unseen objects are bold in the instructions. More demos can be found in our anonymous website. 

14 

**UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning** 


_Figure 7._ Examples of Semantic Generalization to OOD objects 

### **A.5. Data used for pre-training** 

Table 9 summarizes the datasets employed during pre-training. To creating the robot vqa data, we employ Gemini 2.5(Comanici et al., 2025) to annotate text descriptions and task planning for a subset of video data. The RoboMind dataset inherently contains overall task descriptions and sub-tasks, which can be directly utilized as vision–language question–answer pairs. 

### **A.6. VQA Data Design** 

We present several examples of embodied VQA question–answer pairs in Figure 8. 

For part of the embodied datasets (e.g., Agibot and RoboMIND), which contain precise instruction descriptions, we can directly construct QA pairs. For other datasets, we employ Gemini to decompose and annotate instruction descriptions according to the following prompt in Figure 9, 10. 

## **B. Usage of LLMs** 

In the final stages of preparing this manuscript, the authors used a Large Language Model (LLM) solely for grammar checking and language polishing. The model assisted in improving sentence structure and correcting grammatical errors to enhance readability. 

15 

**UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning** 

_Table 9._ Datasets and the number of samples used for TI2E task and VQA task. 

|**Task name**|**Dataset name**<br>**Nu**|**mber of samples**|
|---|---|---|
||AgibotWorld(Bu et al.,2025)|120k|
||Galaxea Open-World(Jiang et al.,2025)|99k|
||Robomind(Wu et al.,2024)|20k|
|**TI2E**|Droid(Khazatsky et al.,2024)|76k|
||Bridge(Walke et al.,2023)|55k|
||Egodex(Hoque et al.,2025)|320k|
||Ego4D(Grauman et al.,2022)|500k|
||AgibotWorld VQA|120k|
||Galaxea Open-World VQA|99k|
|**VQA**|Robomind VQA|20k|
||Droid VQA|76k|
||LLaVA-Pretrain(Liu et al.,2023)|558k|


16 

**UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning** 


```
Question: Based on current observations
and instruction <Put apples, oranges and
peaches in plastic bags.>, what subtask
does the robot need to do next?
```

```
Answer: Next subtask is: place the held
red apple into the plastic bag in the
shopping cart.
```

```
Question: Based on current observations
and instruction <Using the TV Remote.>,
what subtask does the robot need to do
next?
```

```
Answer: Next subtask is: Pick up the
remote control from the table with left
arm.
```

```
Question: Based on current observations
and instruction <Stacking the blue,
yellow, and orange cups.>, planning for
the task the robot need to do?
```

```
Answer: Planning: Pick the blue cup;
Place the blue cup on the yellow cup;
Pick up the yellow cup; Place the yellow
cup on the orange cup
```

_Figure 8._ Example of VQA. 

17 

**UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning** 


1 

_Figure 9._ prompt for Gemini. 

18 

**UniJEPA: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning** 


2 

_Figure 10._ prompt for Gemini. 

19 

