---
title: "CogACT: A Foundational Vision-Language-Action Model for Synergizing Cognition and Action in Robotic Manipulation"
date: "2024-11-29"
authors: "Qixiu Li; Yaobo Liang; Zeyu Wang; Lin Luo; Xi Chen; Mozheng Liao"
url: https://arxiv.org/abs/2411.19650
pdf: https://arxiv.org/pdf/2411.19650
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2411.19650)** / [論文ページ](https://arxiv.org/abs/2411.19650)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **CogACT: A Foundational Vision-Language-Action Model for Synergizing Cognition and Action in Robotic Manipulation** 

Qixiu Li<sup>1</sup><sup>_∗†_</sup> Yaobo Liang<sup>2</sup><sup>_∗‡_</sup> Zeyu Wang<sup>1</sup><sup>_∗†_</sup> Lin Luo<sup>2</sup> Xi Chen<sup>2</sup> Mozheng Liao<sup>3</sup><sup>_†_</sup> Fangyun Wei<sup>2</sup> Yu Deng<sup>2</sup> Sicheng Xu<sup>2</sup> Yizhong Zhang<sup>2</sup> Xiaofan Wang<sup>4</sup><sup>_†_</sup> Bei Liu<sup>2</sup> Jianlong Fu<sup>2</sup> Jianmin Bao<sup>2</sup> Dong Chen<sup>2</sup> Yuanchun Shi<sup>1</sup> Jiaolong Yang<sup>2</sup><sup>_‡_</sup> Baining Guo<sup>2</sup> 1Tsinghua University 2Microsoft Research Asia 3USTC 4Institute of Microelectronics, CAS 


Figure 1. (a) Success rate (%) comparison of our model against RT-1 [7], RT-1-X [48], RT-2-X [48], Octo [62], and OpenVLA [30] across simulated benchmarks (first thee charts) and real-world evaluations (last three charts), using various robots: Google robot, WidowX robot, Realman robot, and Franka robot. All models are trained on the expansive Open X-Embodiment dataset [48] (expect for RT-1 that trains only on the Google Robot subset) and finetuned on a small amount of data for real robot experiments. (b) Scaling behavior: averaged success rate on SIMPLER [33] with respect to action module size. (c) Examples of Realman Robot executing tasks involving sequentially stacking multiple cups and picking and placing unseen objects. 

## **Abstract** 

_The advancement of large Vision-Language-Action (VLA) models has significantly improved robotic manipulation in terms of language-guided task execution and generalization to unseen scenarios. While existing VLAs adapted from pretrained large Vision-Language-Models (VLM) have demonstrated promising generalizability, their task performance is still unsatisfactory as indicated by the low tasks success rates in different environments. In this paper, we present a new advanced VLA architecture derived from VLM. Unlike previous works that directly repurpose VLM for action prediction by simple action quantization, we propose a componentized VLA architecture that has a specialized_ 

> _∗_ Equal Contributions 

> _†_ Interns at Microsoft Research 

> _‡_ Project Leads. Email: _{_ yalia,jiaoyan _}_ @microsoft.com 

_action module conditioned on VLM output. We systematically study the design of the action module and demonstrate the strong performance enhancement with diffusion action transformers for action sequence modeling, as well as their favorable scaling behaviors. We also conduct comprehensive experiments and ablation studies to evaluate the efficacy of our models with varied designs. The evaluation on five robot embodiments in simulation and real work shows that our model not only significantly surpasses existing VLAs in task performance but also exhibits remarkable adaptation to new robots and generalization to unseen objects and backgrounds. It exceeds the average success rates of OpenVLA which has similar model size (7B) with ours by over 35% in simulated evaluation and 55% in real robot experiments. It also outperforms the large RT-2-X model (55B) by 18% absolute success rates in simulation. Code and models can be found on our project page._ 

## **1. Introduction** 

In recent years, there has been a surge of interest in robotic control models equipped with visual capabilities [7, 8, 15, 30, 34, 45, 48, 58, 60, 62, 67, 69]. Among them, the development of large-scale Vision-Language-Action (VLA) models [8, 30, 32] are particularly promising, which empowers robots to perform complex tasks guided by natural language instructions and potentially manage objects or environments that deviate from the training distribution. Additionally, they exhibit rapid adaptability to new tasks and embodiments through finetuning. 

The notable generalization capability of large VLAs can be attributed to both their substantial model size and the potent Vision-Language-Models (VLM) [13, 28, 35] that serve as their foundation. These VLMs are typically pretrained on massive, Internet-scale image-text pairs, which play a crucial role in enhancing VLA generalization to novel objects and semantically diverse instructions [8]. 

Existing large VLAs often adapt VLMs for action prediction in simple ways, leading to several issues that hinder task performance. For instance, works like [8, 30] directly quantize the continuous spectrum of robot actions into discrete bins in accordance to the next token prediction scheme of VLMs. However, such a simple quantization, unlike sophisticated tokenizers such as those designed for images [65, 72] and audio [19, 73], poses difficulties in action learning and limits action precision. [32] introduces additional action heads, such as LSTMs, to transform VLM output into actions. The shift to a regression-based learning scheme, however, overlooks the probabilistic and multimodal<sup>1</sup> nature of actions. 

In this paper, we propose a new VLA model architecture derived from VLM. Instead of repurposing pretrained VLMs for action prediction, _we use the cognitive information extracted by VLM to guide the action prediction process of a specialized action module_ . To handle the inherent characteristics of action signals – continuous, multimodal, temporally correlated, and requiring high precision – we employ advanced diffusion-based transformers (DiT) [51] as our action modules, preconditioned on VLM output via the attention mechanism. 

The intuition behind our design is _the decoupling of “cognition” and “action” capabilities_ . While the large VLMs amass broad visual and semantic knowledge learned from vast amounts of text and images, the cognitive capability and the output language modality have fundamental gaps to dense robot actions. Rather than directly repurposing the VLMs, we advocate the design of componentized VLAs with a dedicated action module.<sup>2</sup> This action mod- 

> 1A robot can follow multiple possible trajectories to accomplish a task. 

> 2As an interesting analogy, our human brain has visual cortex [25], language-relevant cortex [21], and motor cortex [71] – the last being dedicated to the control of human body movements. 

ule is specialized for action signal modeling with cognition model output as preconditions. We synergize the cognition and action capabilities via end-to-end training or finetuning. Hence, our approach is named _CogACT_ . 

We systematically study the different backbone architectures for the action module as well as their scalability on model size, and several notable insights have emerged. For example, it is found that sequential modeling with a diffusion transformer significantly outperforms single-step action prediction. More crucially, _we identified a favorable scaling behavior of the action module with diffusion transformers_ : adding several hundred million parameters, which is relatively minor compared to a 7B VLM base, results in sizable performance enhancements. This finding suggests the advantages of a specialized action module and a more efficient approach for VLA model scaling. 

In addition to our study on action module design, we also introduce some accompanying algorithms of independent interest. An Adaptive Action Ensemble (AAE) algorithm is proposed to fuse the past action predictions in an adaptive manner, which brings notable performance improvement. We train our VLA models on the Open X-Embodiment dataset [48], and evaluate them on both simulation [33] and real-robot benchmarks. The comprehensive evaluation and comparisons show that our model performs remarkably well, surpassing existing VLAs by a wide margin. 

**The contributions of this work** are summarized below: 

- We introduce the integration of the action diffusion process into large-scale VLA models. 

- We propose a componentized VLA model architecture and study the design of large action modules<sup>3</sup> as well as their scaling behaviors. 

- We propose an adaptive action ensemble algorithm which is simple yet effective for temporal fusion. 

- Our model achieves significantly better performance than previous VLAs, exhibiting quick adaptation to new robots and tasks and effective generation to unseen objects and backgrounds, as shown in Figure 1. All our code and models are publicly released. 

## **2. Related Works** 

**Vision-Language-Action Models.** The success of Large Language Models (LLMs) [2, 9, 63, 64] and VisionLanguage Models (VLMs) [1, 14, 28, 37, 61] has inspired the development of Vision-Language-Action (VLA) models, which extend the capabilities of VLMs by integrating action generation. For instance, RoboFlamingo [32] extends OpenFlamingo [3] by incorporating a head network to predict actions and optimizing with MSE loss. RT-2 [8] 

> 3Our largest action DiT module is of 300M parameters. Although this may seem modest, especially in comparison with large LLMs/VLMs, it is considered large given the 7D vector space of robot actions we address. 

2 

tokenizes 7D actions into discrete tokens and uses the VLM PaLI-X [13] to predict them autoregressively like language tokens. OpenVLA adopts a similar approach, tokenizing actions and training the Prismatic VLM [28] on the OpenX-Embodiment dataset [48]. While these models benefit from VLMs’ capabilities and demonstrate promising performance and impressive generalization, they lack the consideration that actions are inherently continuous and temporal, a modality distinct from language. A group of methods [5, 11, 68] employ large-scale video generative pretraining to enhance visual robot manipulation learning without leveraging pretrained VLMs, and promising results have been demonstrated. 

**Large Action Models.** There are some recent attempts _concurrent to ours_ that explored large action models for generalist robots. For example, [24] trained a diffusion transformer with 221M parameters and [38] further scaled the action model size to 1B. Both works apply separate vision and language encoders that are pretrained and frozen to process language instructions and images, and they train the action model to integrate these inputs and predict actions with VLA data. Different from ours, these works cannot leverage the generalization and instruction following capability of powerful VLMs pretrained on Internet-scale visionlanguage aligned data. 

**Diffusion-Based Robot Policies.** Recent studies [15, 50, 53] have introduced diffusion models as an innovative approach for modeling robotic actions. These diffusion policies have demonstrated strong capabilities to capture the multi-mode nature of robotic action distributions and effectively model the various feasible trajectories that a robot can take to accomplish a given task [15]. Inspired by diffusion policies, Octo [62] supplements a transformer-based backbone architecture with compact diffusion heads of 3M parameters to adapt the action output across different robots. However, the small diffusion head falls short in capturing the precise action distributions and the overall approach does not benefit from strong vision-language models pretrained on web-scale data. In contrast, our work studies large, dedicated action modules (rather than “heads”) with the diffusion transformer architecture. Besides, unlike [15, 50, 53], we are interested in large VLAs derived from VLM foundation models with strong generalization capability. 

## **3. Method** 

**Problem Formulation.** Our goal is to develop a VLA model that enables different robots to physically execute diverse tasks while receiving visual observations and language instructions. Formally, given the language instruction **_l_** and visual observation **_o_** _t_ at time _t_ , a model **_π_** predicts a temporal action sequence ( **_a_** _t,_ **_a_** _t_ +1 _, ...,_ **_a_** _t_ + _N_ ) for execut- 

ing the desired task: 


While in general, **_a_** _t_ can describe various robot actions with different control modes and end-effectors, we consider the action space of a gripper with 7 degrees of freedom (DoF) in this work: 


where ∆ _x,_ ∆ _y,_ ∆ _z_ are the relative translation offsets of the end effector, ∆ _ϕ,_ ∆ _θ,_ ∆ _ψ_ denote the rotation changes, and _g ∈{_ 0 _,_ 1 _}_ indicates the gripper’s open/close state. 

**Overall architecture.** To effectively handle complex visual observations and language instructions and collaboratively transform them into precise actions, we componentize the model **_π_** into three parts: a _vision_ module, a _language_ module, and an _action_ module, as shown in Fig. 2. We describe each part in details below. 

### **3.1. Vision and Language Modules** 

Our vision and language modules are adapted from an existing VLM from [28] that has about 7B parameters in total, similar to [30]. We briefly describe them below for completeness. 

**Vision Module.** The vision module processes raw images input into a set of perceptual tokens. It consists of powerful vision transformers, DINOv2 [49] and SigLIP [74], pretrained on Internet-scale image data, to capture rich visual features and a comprehensive semantic understanding of the observations. At each timestep _t_ , the image observation **_o_** _t_ is fed into the two models, producing two downsampled feature maps **_f_** _t_<sup>DINO</sup> and **_f_** _t_<sup>Sig</sup> , respectively. These feature maps are then concatenated along the channel dimension, passed through a linear projection layer, and serialized into a set of visual perceptual tokens, _V_ = _{_ **_v_** 1 _,_ **_v_** 2 _, ...,_ **_v_** _NV }_ with a length _NV_ (we use 256 by default). 

**Language Module.** The language module is responsible for integrating visual information and language instructions and conducting cognitive reasoning. Here, a LLAMA2 model [64] is applied as the backbone. The language instruction **_l_** is converted into a set of linguistic tokens, _T_ = _{_ **_l_** 1 _,_ **_l_** 2 _, ...,_ **_l_** _NT }_ , using LLAMA-2’s tokenizer. These tokens are then concatenated with the visual tokens _V_ and an additional learnable cognition token **_c_** , and processed by the model using a causal attention mechanism. The resulting output feature **_f_** _t_<sup>**_c_**, corresponding to the cognition token,</sup> encodes integrated information that determines the action to be executed for the current task. This serves as a condition for the subsequent action module to interpret and derive the desired actions. 

3 


Figure 2. Overview of our architecture. Our model is componentized into three parts: 1) a vision module encoding information from the current image observation into visual tokens; 2) a language module that integrates the visual tokens with the language instructions, and produces a cognition feature determining the desired action to be executed; 3) a diffusion action module, which predicts a sequence of multi-step actions conditioned on the cognition feature. An adaptive ensemble strategy is applied for trajectory ensemble at inference. 

Specifically, our action module takes the cognition feature **_f_** _t_<sup>**_c_**</sup> along with a series of noisy actions ( **_a_**<sup>_i_</sup> _t_<sup>_,_</sup><sup>**_a_**</sup><sup>_i_</sup> _t_ +1<sup>_, ...,_</sup><sup>**_a_**</sup><sup>_i_</sup> _t_ + _N_<sup>)asinput,where</sup><sup>_i_denotesthecur-</sup> rent denoising step. It predicts the final actions ( **_a_** _t,_ **_a_** _t_ +1 _, ...,_ **_a_** _t_ + _N_ ) through multiple denoising steps. The cognition feature and the noisy actions serve as input tokens to the transformer blocks, while the step information _i_ is added to the cognition feature with a sinusoidal positional encoding. We enforce the action model to predict not only the current action **_a_** _t_ but also multiple future actions ( **_a_** _t_ +1 _, ...,_ **_a_** _t_ + _N_ ). This approach enhances the overall smoothness of the predicted actions at each time step and increases the final success rates for task execution, as observed similarly in previous studies [15, 75]. In practice, the number of predicted future actions is set to a small value ( _N_ = 15 by default), leading to a context length of _N_ + 2 = 17 for the action module. This makes the diffusion process highly efficient and does not introduce much computational cost to the overall framework. 

Figure 3. Illustration of our action ensemble strategy with _K_ = 2 (using the last 2 historical action predictions) as an example. The action ensemble aggregates historical predictions with the current prediction to jointly determine the final action to be executed. 

where **ˆ** **_ϵ_**<sup>_i_</sup> is the predicted noise for the noisy action sequence ( **_a_**<sup>_i_</sup> _t_<sup>_,_</sup><sup>**_a_**</sup><sup>_i_</sup> _t_ +1<sup>_, ...,_</sup><sup>**_a_**</sup><sup>_i_</sup> _t_ + _N_<sup>)atthe</sup><sup>_i_’sdenoisingstep,and</sup><sup>**_ϵ_**isthe</sup> corresponding ground truth. 

### **3.4. Adaptive Action Ensemble** 

During inference, our model predicts actions for multiple time steps. One straightforward strategy is to execute these actions consecutively (Action Chunking [75]) based on the current observation, **_ot_** . However, this does not fully leverage the visual information available at each time step and may result in jerky motion, as discussed in [75]. Alternatively, executing only the action for the current time step ( _i.e_ ., **_a_** _t_ ) also leads to a less smooth trajectory and diminished performance. 

### **3.3. Training Objective** 

To alleviate these, [75] introduced a temporal ensemble strategy that combines actions predicted for the current time step from both present and past predictions using preset aggregation weights. However, feasible actions for task execution can belong to different modes [15], and simply aggregating them could result in an action that does not align with any mode, which is suboptimal. 

Our vision module, language module, and action module are trained/finetuned end-to-end by minimizing the meansquared error (MSE) between the predicted noises from the action module and the ground truth noises. The loss function is defined as: 


We propose an adaptive ensemble strategy which consid- 

4 

ers similarities between actions to be aggregated, as shown in Fig. 3. This approach avoid unreasonable aggregation of actions from different modes. Specifically, let **_a_** _t|_ **_o_** _t_ represent the action prediction for the current time step _t_ given the observation **_o_** _t_ , and _{_ **_a_** _t|_ **_o_** _t−K, ...,_ **_a_** _t|_ **_o_** _t−_ 1 _}_ denote the corresponding action predictions based on historical observations _{_ **_o_** _t−K, ...,_ **_o_** _t−_ 1 _}_ . We derive the final action **_a_ ˆ** _t_ to be executed at time step _t_ as: 


Here, _wk_<sup>ada</sup> is an adaptive weighting scalar that assigns greater importance to past predictions that are more similar to the current prediction **_a_** _t|_ **_o_** _t_ : 


where _< ·, · >_ calculates the cosine similarity between two actions, and _α_ is a hyperparameter set to 0 _._ 1 in practice. 

Our empirical results show that this adaptive action ensemble strategy effectively boosts the success rate of task executions while adding minimal extra cost to inference, since past predictions can be readily cached. 

## **4. Experiment** 

**Training Dataset.** We use the Open X-Embodiment (OXE) [48] dataset as our primary training dataset. It includes over 1 million real-world robotic trajectories collected from 60 datasets, covering 22 different robot embodiments. We use the similar subset of OXE as in Octo [62] and OpenVLA [30] for training, which comprises 22.5 million frames. For details regarding data distributions, please refer to [30, 62]. 

**Implementation Details.** The model is trained with a batch size of 256 and 8 diffusion steps per sample, initialized with pre-trained vision and language module weights from [30]. The vision module ( _i.e_ ., DINOv2 and SigLIP), language module ( _i.e_ ., LLAMA-2), and action module are all trained end-to-end, following a constant learning rate of 2 _e −_ 5 for over 135K iterations. Training is conducted on 16 NVIDIA A100 GPUs with approximately 5 days using PyTorch’s Fully Sharded Data Parallel (FSDP) framework. By default, we use DiT-Base as our action model. The ensemble window _K_ is set to be inversely proportional to the moving distance per frame, which can be inferred from robots’ motion speed and observation frequency. In practice, we use the standard deviation of actions from training set to determine _K_ , _i.e_ ., 2 for RT-1 dataset with Google Robot, 7 for BridgeDataV2 with WidowX Robot. 

### **4.1. Simulated Evaluation** 

**Evaluation Environment.** After training, we evaluate our model within the SIMPLER [33] evaluation environment. 

This simulation platform is designed to bridge the real-tosim control and visual gap by faithfully replicating realworld conditions for robots like the Google robot and the WidowX robot. Extensive testing of various VLA models has shown a strong correlation between performance in SIMPLER and real-world outcomes [33]. 

**Evaluation Settings.** SIMPLER offers two evaluation settings: _Visual Matching_ , which closely replicates real-world tasks by minimizing discrepancies between the simulated and real environments, and _Variant Aggregations_ , which introduces variations to _Visual Matching_ by modifying elements such as background, lighting, distractors, and table texture. For the Google robot, SIMPLER provides both the two evaluation settings, each featuring the same four tasks: 1) Pick coke can; 2) Move near; 3) Open/close drawer; and 4) Open top drawer and place apple. For the WidowX robot, SIMPLER provides only the _Visual Matching_ setting, with four tasks: 1) Put spoon on towel; 2) Put carrot on plate; 3) Stack green block on yellow block; and 4) Put eggplant in yellow basket. Success rate is used as the evaluation metric. 

**Experiments on Google Robot.** Table 1 shows the success rates of our model and compares our approach with existing VLA models on the Google robot across four tasks in both SIMPLER settings. Our model achieves the highest average success rate in both settings, with 74.8% in _Visual Matching_ and 61.3% in _Variant Aggregation_ . Remarkably, our model even outperforms RT-1 [7], which is trained on a Google robot-specific dataset, by an average success rate margin of 22.4% in _Visual Matching_ and 17.6% in _Variant Aggregation_ . Additionally, the average success rate of our model significantly surpasses that of RT-2-X [48], despite our model being much smaller, with 7.6B parameters compared to RT-2-X that has 55B parameters. 

**Experiments on WidowX Robot.** Table 2 presents the evaluation results of our model compared with the other methods on the WidowX robot using the SIMPLER environment in the _Visual Matching_ setting. Our model also attains the highest average success rate of 51.3%, outperforming the other models by a significant margin. 

### **4.2. Real-World Evaluation with Realman Robot** 

**Robot.** We perform real-world experiments using the Realman Arm<sup>4</sup> , which has 7 DoFs and is equipped with a 1-DoF gripper. Inverse kinematics is applied to determine joint angles, enabling the end effector to align with the model’s predicted pose. **Task Definitions.** We design three tasks 

for real-world experiments, named “Pick”, “Stack”, and “Place”: 

- Pick up the Object and place it onto the Color plate, where Object _∈{_ Banana _,_ Lemon _,_ Avocado _}_ , 

> 4https://www.realman-robotics.com/rm75-b.html 

5 

Table 1. Comparison of our approach with existing VLA models on the Google robot across four tasks in two SIMPLER settings. All models are trained on the Open X-Embodiment dataset, except for RT-1 which is trained exclusively on the Google robot subset. 

|Google Robot|Method|Pick<br>Coke Can|Move<br>Near|Open/Close<br>Drawer|Open Top Drawer<br>and Place Apple|_Average_|
|---|---|---|---|---|---|---|
||RT-1 [7]|85.7|44.2|73.0|6.5|52.4|
||RT-1-X [48]|56.7|31.7|59.7|21.3|42.4|
|SIMPLER|RT-2-X [48]|78.7|77.9|25.0|3.7|46.3|
|(Visual Matching)|Octo-Base [62]|17.0|4.2|22.7|0.0|11.0|
||OpenVLA [30]|18.0|56.3|63.0|0.0|34.3|
||Ours|**91.3**|**85.0**|**71.8**|**50.9**|**74.8**|
||RT-1 [7]|89.8|50.0|32.3|2.6|43.7|
||RT-1-X [48]|49.0|32.3|29.4|10.1|30.2|
|SIMPLER|RT-2-X [48]|82.3|79.2|**35.3**|20.6|54.4|
|(Variant Aggregation)|Octo-Base [62]|0.6|3.1|1.1|0.0|1.2|
||OpenVLA [30]|60.8|67.7|28.8|0.0|39.3|
||Ours|**89.6**|**80.8**|28.3|**46.6**|**61.3**|


Table 2. Evaluation results on the WidowX robot in the SIMPLER _Visual Matching_ setting. For these tests, we repeat each task 5 times to improve the statistical significance (see _suppl. material_ for details), and thus the results of Octo may slightly differ from those in [33]. 

|WidowX Robot|Method|Put Spoon<br>on Towel|Put Carrot<br>on Plate|Stack Green Block<br>on Yellow Block|Put Eggplant<br>in Yellow Basket|_Average_|
|---|---|---|---|---|---|---|
||RT-1-X [48]|0.0|4.2|0.0|0.0|1.1|
||Octo-Base [62]|15.8|12.5|0.0|41.7|17.5|
|SIMPLER<br>|Octo-Small [62]|41.7|8.2|0.0|56.7|26.7|
|(Visual Matching)|OpenVLA [30]|4.2|0.0|0.0|12.5|4.2|
||<br>Ours|**71.7**|**50.8**|**15.0**|**67.5**|**51.3**|


and Color _∈{_ White _,_ Blue _,_ Yellow _}_ . 

- Stack the Color Object into the Color Object, where Object _∈ {_ Cup _,_ Bowl _}_ and Color _∈ {_ Pink _,_ White _,_ Blue _,_ Yellow _}_ . 

- Place the Color block onto the Color block, where Color _∈{_ Red _,_ Orange _,_ Blue _,_ Green _,_ Yellow _}_ . 

**Fine-Tuning Data.** We manually collect 48, 67 and 79 demonstrations for the “Pick”, “Stack”, and “Place” tasks, respectively. Additionally, we capture 197 demonstrations for various other tasks like “Pick up the orange can and drop it into the basket”. In total, we gather 391 demonstrations for fine-tuning. Notably, demonstrations for tasks identical to the evaluation settings are very few. For example, there are only two demonstrations for the specific task “put the banana on the yellow plate.” Details of the fine-tuning process are provided in the _suppl. material_ . 

**Evaluation.** Each task is evaluated as follows: 

- “Pick”: 24 evaluations in total, with 8 trials per object (Banana, Lemon and Avocado). We report the success rate for each object, as well as the average success rate across the three objects. 

- “Stack”: 48 evaluations in total, with 24 trials per object (Cup and Bowl). We report the success rate for each 

object, along with the average success rate across both objects. 

- “Place”: 24 evaluations in total. This task is divided into two steps: 1) picking up the block, and 2) placing the block onto another block. We report the success rate for each step, and the average success rate across both steps. 

In each evaluation, we randomly choose the Color, and place both the target and at least three distractor objects in random positions on the table. We vary the table height within the robot’s accessible range, and randomly set the robot’s position around the table. 

**Results.** Table 3 presents a comparison of our model with Octo-Base [62] and OpenVLA [30]. For a fair evaluation, all models are pre-trained on the OXE dataset and subsequently fine-tuned using our collected demonstrations. Our model achieves a notable improvement, outperforming OpenVLA by a margin of 59.1% in success rate. 

**Generalization Evaluation.** We assess the generalization capability of the fine-tuned models on environments, distractors, tables, and objects that are not present in the finetuning dataset. We exclude Octo-Base [62] from this evaluation since its success rate in the seen task is already close to zero. 

6 


Figure 4. Real-world evaluation environments of Realman robot (left) and Franka robot (right). 

Table 3. Real-world evaluation with the Realman Robot across three tasks. All models are pre-trained on OXE and then fine-tuned on our collected data. 

|Method||Pic|k|||Stack|||Place||Task (All)|
|---|---|---|---|---|---|---|---|---|---|---|---|
||Banana|Lemon|Avocado|Avg.|Cup|Bowl|Avg.|Pick|Stack|Avg.|Avg.|
|Octo-Base [62]|25.0|0.0|0.0|8.3|0.0|0.0|0.0|12.5|0.0|6.3|4.9|
|OpenVLA [30]|12.5|12.5|0.0|8.3|25.0|6.3|15.6|25.0|4.2|12.5|12.1|
|Ours|**75.0**|**50.0**|**87.5**|**70.8**|**95.8**|**68.8**|**82.3**|**87.5**|**33.3**|**60.4**|**71.2**|


Table 4. Real-world generalization evaluation with the Realman Robot on _unseen_ tables with additional _unseen_ distractors. 

|Method||Pic|k|||Stack|||Place||Task (All)|
|---|---|---|---|---|---|---|---|---|---|---|---|
||Banana|Lemon|Avocado|Avg.|Cup|Bowl|Avg.|Pick|Stack|Avg.|Avg.|
|OpenVLA [30]|12.5|0.0|12.5|8.3|12.5|0.0|6.3|29.2|0.0|14.6|9.7|
|Ours|**75.0**|**62.5**|**87.5**|**75.0**|**83.3**|**45.8**|**64.6**|**54.2**|**16.7**|**35.5**|**58.4**|


Table 5. Real-world generalization evaluation with the Realman Robot on unseen colors, shapes and categories. 

|Method|Unseen<br>Colors|Unseen<br>Shapes|Unseen<br>Categories|Avg.|
|---|---|---|---|---|
|OpenVLA [30]|0.0|6.3|12.5|6.3|
|Ours|**87.5**|**81.3**|**25.0**|**64.6**|


Table 6. Real-world evaluation with the Franka Robot across four tasks. All models are pre-trained on OXE and then fine-tuned on our collected data. 

|Method|Close<br>Oven|Open<br>Oven|Pick<br>Bowl|Pick<br>Brush|Avg.|
|---|---|---|---|---|---|
|Octo-Base [62]|0.0|0.0|27.3|0.0|5.8|
|OpenVLA [30]|18.2|0.0|9.1|0.0|6.8|
|Ours|**63.6**|**72.7**|**72.7**|**36.4**|**61.4**|


- _Unseen Tables with Unseen Distractors._ The table color is altered to closely resemble the colors of the background and floor, increasing visual complexity. Additionally, three new unseen objects are introduced as distractors. The results for each task is presented in Table 4. 

- _Unseen Colors, Shapes, and Categories._ We assess performance on unseen colors in the “Pick” task, using seen objects (Banana, Avocado) with new colors (Green, Pink) of plates. Each object-color combination is evaluated twice, for a total of 8 trials. For evaluating on unseen shapes, we define four new tasks: (1-2) “Pick up the Shape block and put it into the basket”, where Shape _∈{_ Triangular _,_ Arched _}_ ; (3) “Pick up a small can and drop it into the basket”; (4) “Stack one cylindrical block on top of another cylindrical block”. Each task is evaluated 4 times, resulting in a total of 16 trials. 

- For evaluating unseen categories, we introduce a new 

task: “Pick up the Object and place it into the basket”, where Object _∈{_ Eggplant _,_ Hammer _}_ . This task is evaluated 8 times in total, with 4 trials per object. Table 5 presents the results, demonstrating that our approach exhibits strong generalization capabilities, particularly in handling unseen colors and shapes. 

### **4.3. Real-World Evaluation with Franka Robot** 

**Robot.** To further demonstrate the generalization capability of our approach, we employ an additional robot, the Franka Arm<sup>5</sup> , which features 7 DoFs and a 1-DoF gripper, for realworld evaluation. 

**Task Definitions.** We define four tasks for evaluation: 1) Close the oven door; 2) Open the oven door; 3) Pick up the green brush; 4) Pick up a bowl containing food. 

> 5https://franka.de/ 

7 

Table 7. Performance comparison of different action model network structures. 

|Action Model|Params|G<br>(VM)|R<br>(VA)|WR<br>(VM)|Average|
|---|---|---|---|---|---|
|MLP (3-Layer)|3M|52.2|52.4|47.1|50.6|
|MLP (7-Layer)|89M|61.4|48.0|48.1|52.5|
|DiT-Small|13M|73.3|51.3|51.0|58.5|
|DiT-Base|89M|74.8|**61.3**|51.3|62.5|
|DiT-Large|308M|**76.7**|59.3|**58.3**|**64.8**|


**Fine-Tuning Data.** For each task, we collect 100 demonstration samples, resulting in a total of 400 samples used to fine-tune all the models. 

**Results.** Each task is tested over 11 trials. Table 6 presents a comparison between our model, Octo-Base, and OpenVLA, demonstrating that our approach achieves significantly higher performance. Real-world results with the Realman Robot (Table 3) and the Franka Robot (Table 6) consistently validate the generalization capability of our approach across different robotic platforms. 

### **4.4. Ablation Study** 

We employ SIMPLER evaluation on both the Google robot and the WidowX robot for all ablation studies. We use the following abbreviations: GR for Google Robot, WR for WidowX Robot, VM for the SIMPLER Visual Matching setting, and VA for the SIMPLER Visual Aggregation setting. 

**Action Model Architectures.** We evalute various action model architectures on GR and WR. The architectures examined include Multi-Layer Perceptrons (MLPs) with depths of 3 and 7 layers, respectively, as well as a series of diffusion transformers of varying scales. The hidden state dimensions are set to 256 and 1024 for the two MLPs. 

Table 7 shows that both MLP and transformer structures show improved success rate with increased model size. With the same number of parameters, transformers outperform MLPs, likely due to the attention mechanism’s superior sequence modeling capabilities. Notably, DiT-Large achieves the highest average success rate of 64.8%. As shown in Figure 1, the average success rate of transformers is approximately linearly related to the logarithm of the model size. This indicates a promising scaling behavior of the action module with diffusion transformers. 

**Multi-Step Action Prediction.** During training, our model predicts the action for the current step along with _N_ future steps. In Table 8, we examine the effect of varying _N_ (0, 3, 15 and 31 future steps) on performance. Our results indicate that predicting 15 future steps leads to the highest performance. 

Table 8. Impact of multi-step action prediction on model performance. A future step setting of 0 indicates no multi-step action prediction during training. 

|Future Steps|G<br>(VM)|R<br>(VA)|WR<br>(VM)|Average|
|---|---|---|---|---|
|0|73.4|49.0|6.3|42.8|
|3|70.4|58.9|37.1|55.5|
|15|**74.8**|**61.3**|51.3|**62.5**|
|31|54.3|47.6|**51.7**|51.2|


Table 9. Comparison of our proposed action ensemble strategy, Adaptive Ensemble, against two strategies introduced in [75]. 

|Strategy|G<br>(VM)|R<br>(VA)|WR<br>(VM)|Average|
|---|---|---|---|---|
|Action Chunking|67.4|52.5|32.1|50.7|
|Temporal Ensemble|**75.0**|59.9|41.9|58.9|
|Adaptive Ensemble|74.8|**61.3**|**51.3**|**62.5**|


**Adaptive Action Ensemble.** In Section 3.4, we present an action ensemble strategy, termed Adaptive Ensemble, as formulated in Eq. (4). We evaluate this approach against the two ensemble strategies introduced in ACT [75]: Action Chunking and Temporal Ensemble. Given a sequence of action predictions of current observation, Action Chunking executes the first two predictions directly. We use the same ensemble windows for Temporal Ensemble and our Adaptive Ensemble. Table 9 presents the success rates of these strategies. Our proposed Adaptive Ensemble outperforms others, and we attribute this to its integration of similarity weighting between current and historical predictions. 

## **5. Conclusion** 

We have presented a large VLA model designed with a specialized focus on action modeling. Unlike previous VLAs that employ simple adaptations of vision-language models for action prediction, CogACT separates cognitive and action capabilities, using advanced diffusion transformers as a dedicated action module. This approach effectively addresses the continuous, multimodal, and temporally correlated nature of robot actions, leading to substantial improvements in performance and generalization. Our findings highlight the advantages of a componentized VLA model, where a large VLM serves as the cognitive foundation while the DiT action module handles precise, sequential action prediction. Favorable scaling behaviors of the action module have been observed, where modest parameter increases yield significant performance gains. The extensive experiments show that our model not only significantly surpasses existing VLAs in task performance and but also exhibits remarkable generation capability to unseen objects and backgrounds. 

8 

## **References** 

- [1] Marah Abdin, Jyoti Aneja, Hany Awadalla, Ahmed Awadallah, Ammar Ahmad Awan, Nguyen Bach, Amit Bahree, Arash Bakhtiari, Jianmin Bao, Harkirat Behl, et al. Phi-3 technical report: A highly capable language model locally on your phone. _arXiv preprint arXiv:2404.14219_ , 2024. 2 

- [2] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 2 

- [3] Anas Awadalla, Irena Gao, Josh Gardner, Jack Hessel, Yusuf Hanafy, Wanrong Zhu, Kalyani Marathe, Yonatan Bitton, Samir Gadre, Shiori Sagawa, et al. Openflamingo: An opensource framework for training large autoregressive visionlanguage models. _arXiv preprint arXiv:2308.01390_ , 2023. 2 

- [4] Suneel Belkhale, Yuchen Cui, and Dorsa Sadigh. Hydra: Hybrid robot actions for imitation learning. _arxiv_ , 2023. 13 

- [5] Homanga Bharadhwaj, Debidatta Dwibedi, Abhinav Gupta, Shubham Tulsiani, Carl Doersch, Ted Xiao, Dhruv Shah, Fei Xia, Dorsa Sadigh, and Sean Kirmani. Gen2act: Human video generation in novel scenarios enables generalizable robot manipulation. _arXiv preprint arXiv:2409.16283_ , 2024. 3 

- [6] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 13 

- [7] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 1, 2, 5, 6 

- [8] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 2 

- [9] Tom B Brown. Language models are few-shot learners. _arXiv preprint arXiv:2005.14165_ , 2020. 2 

- [10] Berk Calli, Arjun Singh, Aaron Walsman, Siddhartha Srinivasa, Pieter Abbeel, and Aaron M Dollar. The ycb object and model set: Towards common benchmarks for manipulation research. In _2015 international conference on advanced robotics (ICAR)_ , pages 510–517. IEEE, 2015. 14 

- [11] Chi-Lam Cheang, Guangzeng Chen, Ya Jing, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Hongtao Wu, Jiafeng Xu, Yichu Yang, et al. Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation. _arXiv preprint arXiv:2410.06158_ , 2024. 3 

- [12] Lawrence Yunliang Chen, Simeon Adebola, and Ken Goldberg. Berkeley UR5 demonstration dataset. https://sites.google.com/view/berkeley-ur5/home. 13 

- [13] Xi Chen, Josip Djolonga, Piotr Padlewski, Basil Mustafa, Soravit Changpinyo, Jialin Wu, Carlos Riquelme Ruiz, Se- 

bastian Goodman, Xiao Wang, Yi Tay, et al. Pali-x: On scaling up a multilingual vision and language model. _arXiv preprint arXiv:2305.18565_ , 2023. 2, 3 

- [14] Zhe Chen, Jiannan Wu, Wenhai Wang, Weijie Su, Guo Chen, Sen Xing, Muyan Zhong, Qinglong Zhang, Xizhou Zhu, Lewei Lu, et al. Internvl: Scaling up vision foundation models and aligning for generic visual-linguistic tasks. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 24185–24198, 2024. 2 

- [15] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , page 02783649241273668, 2023. 2, 3, 4 

- [16] Nikolaus Correll, Kostas E Bekris, Dmitry Berenson, Oliver Brock, Albert Causo, Kris Hauser, Kei Okada, Alberto Rodriguez, Joseph M Romano, and Peter R Wurman. Analysis and observations from the first amazon picking challenge. _IEEE Transactions on Automation Science and Engineering_ , 15(1):172–188, 2016. 14 

- [17] Zichen Jeff Cui, Yibin Wang, Nur Muhammad Mahi Shafiullah, and Lerrel Pinto. From play to policy: Conditional behavior generation from uncurated robot data. _arXiv preprint arXiv:2210.10047_ , 2022. 13 

- [18] Shivin Dass, Jullian Yapeter, Jesse Zhang, Jiahui Zhang, Karl Pertsch, Stefanos Nikolaidis, and Joseph J. Lim. Clvr jaco play dataset, 2023. 13 

- [19] Alexandre D´efossez, Jade Copet, Gabriel Synnaeve, and Yossi Adi. High fidelity neural audio compression. _arXiv preprint arXiv:2210.13438_ , 2022. 2 

- [20] Frederik Ebert, Yanlai Yang, Karl Schmeckpeper, Bernadette Bucher, Georgios Georgakis, Kostas Daniilidis, Chelsea Finn, and Sergey Levine. Bridge data: Boosting generalization of robotic skills with cross-domain datasets. _arXiv preprint arXiv:2109.13396_ , 2021. 13 

- [21] Angela D Friederici. The brain basis of language processing: from structure to function. _Physiological reviews_ , 91 (4):1357–1392, 2011. 2 

- [22] Minho Heo, Youngwoon Lee, Doohyun Lee, and Joseph J. Lim. Furniturebench: Reproducible real-world benchmark for long-horizon complex manipulation. In _Robotics: Science and Systems_ , 2023. 13 

- [23] Jonathan Ho and Tim Salimans. Classifier-free diffusion guidance. _arXiv preprint arXiv:2207.12598_ , 2022. 14, 16 

- [24] Zhi Hou, Tianyi Zhang, Yuwen Xiong, Hengjun Pu, Chengyang Zhao, Ronglei Tong, Yu Qiao, Jifeng Dai, and Yuntao Chen. Diffusion transformer policy. _arXiv preprint arXiv:2410.15959_ , 2024. 3 

- [25] Trevor Huff, Navid Mahabadi, and Prasanna Tadi. Neuroanatomy, visual cortex. 2018. 2 

- [26] Eric Jang, Alex Irpan, Mohi Khansari, Daniel Kappler, Frederik Ebert, Corey Lynch, Sergey Levine, and Chelsea Finn. Bc-z: Zero-shot task generalization with robotic imitation learning. In _Conference on Robot Learning_ , pages 991– 1002. PMLR, 2022. 13 

- [27] Dmitry Kalashnikov, Alex Irpan, Peter Pastor, Julian Ibarz, Alexander Herzog, Eric Jang, Deirdre Quillen, Ethan Holly, 

9 

Mrinal Kalakrishnan, Vincent Vanhoucke, et al. Qtopt: Scalable deep reinforcement learning for vision-based robotic manipulation. _arXiv preprint arXiv:1806.10293_ , 2018. 13 

- [28] Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa Sadigh. Prismatic vlms: Investigating the design space of visually-conditioned language models. _arXiv preprint arXiv:2402.07865_ , 2024. 2, 3, 13 

- [29] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, Peter David Fagan, Joey Hejna, Masha Itkina, Marion Lepert, Yecheng Jason Ma, Patrick Tree Miller, Jimmy Wu, Suneel Belkhale, Shivin Dass, Huy Ha, Arhan Jain, Abraham Lee, Youngwoon Lee, Marius Memmel, Sungjae Park, Ilija Radosavovic, Kaiyuan Wang, Albert Zhan, Kevin Black, Cheng Chi, Kyle Beltran Hatch, Shan Lin, Jingpei Lu, Jean Mercat, Abdul Rehman, Pannag R Sanketi, Archit Sharma, Cody Simpson, Quan Vuong, Homer Rich Walke, Blake Wulfe, Ted Xiao, Jonathan Heewon Yang, Arefeh Yavary, Tony Z. Zhao, Christopher Agia, Rohan Baijal, Mateo Guaman Castro, Daphne Chen, Qiuyu Chen, Trinity Chung, Jaimyn Drake, Ethan Paul Foster, Jensen Gao, David Antonio Herrera, Minho Heo, Kyle Hsu, Jiaheng Hu, Donovon Jackson, Charlotte Le, Yunshuang Li, Kevin Lin, Roy Lin, Zehan Ma, Abhiram Maddukuri, Suvir Mirchandani, Daniel Morton, Tony Nguyen, Abigail O’Neill, Rosario Scalise, Derick Seale, Victor Son, Stephen Tian, Emi Tran, Andrew E. Wang, Yilin Wu, Annie Xie, Jingyun Yang, Patrick Yin, Yunchu Zhang, Osbert Bastani, Glen Berseth, Jeannette Bohg, Ken Goldberg, Abhinav Gupta, Abhishek Gupta, Dinesh Jayaraman, Joseph J Lim, Jitendra Malik, Roberto Mart´ın-Mart´ın, Subramanian Ramamoorthy, Dorsa Sadigh, Shuran Song, Jiajun Wu, Michael C. Yip, Yuke Zhu, Thomas Kollar, Sergey Levine, and Chelsea Finn. Droid: A large-scale in-the-wild robot manipulation dataset. 2024. 13 

- [30] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 1, 2, 3, 5, 6, 7, 13, 15 

- [31] Eric Krotkov, Douglas Hackett, Larry Jackel, Michael Perschbacher, James Pippine, Jesse Strauss, Gill Pratt, and Christopher Orlowski. The darpa robotics challenge finals: Results and perspectives. _The DARPA robotics challenge finals: Humanoid robots to the rescue_ , pages 1–26, 2018. 14 

- [32] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, et al. Vision-language foundation models as effective robot imitators. _arXiv preprint arXiv:2311.01378_ , 2023. 2 

- [33] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 1, 2, 5, 6, 14, 15 

- [34] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, et al. Vision-language foundation models as effective robot imitators. In _The Twelfth International Conference on Learning Representations_ , 2024. 2 

- [35] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. _Advances in neural information processing systems_ , 36, 2023. 2 

- [36] Huihan Liu, Soroush Nasiriany, Lance Zhang, Zhiyao Bao, and Yuke Zhu. Robot learning on the job: Human-in-theloop autonomy and learning during deployment. In _Robotics: Science and Systems (RSS)_ , 2023. 13 

- [37] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. _Advances in neural information processing systems_ , 36, 2024. 2 

- [38] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 3 

- [39] Jianlan Luo, Charles Xu, Xinyang Geng, Gilbert Feng, Kuan Fang, Liam Tan, Stefan Schaal, and Sergey Levine. Multistage cable routing through hierarchical imitation learning. _arXiv pre-print_ , 2023. 13 

- [40] Jianlan Luo, Charles Xu, Fangchen Liu, Liam Tan, Zipeng Lin, Jeffrey Wu, Pieter Abbeel, and Sergey Levine. Fmb: a functional manipulation benchmark for generalizable robotic learning. _arXiv preprint arXiv:2401.08553_ , 2024. 13 

- [41] Corey Lynch, Ayzaan Wahid, Jonathan Tompson, Tianli Ding, James Betker, Robert Baruch, Travis Armstrong, and Pete Florence. Interactive language: Talking to robots in real time. _IEEE Robotics and Automation Letters_ , 2023. 13 

- [42] Ajay Mandlekar, Jonathan Booher, Max Spero, Albert Tung, Anchit Gupta, Yuke Zhu, Animesh Garg, Silvio Savarese, and Li Fei-Fei. Scaling robot supervision to hundreds of hours with roboturk: Robotic manipulation dataset through human reasoning and dexterity. In _2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 1048–1055. IEEE, 2019. 13 

- [43] Oier Mees, Jessica Borja-Diaz, and Wolfram Burgard. Grounding language with visual affordances over unstructured data. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , London, UK, 2023. 13 

- [44] Russell Mendonca, Shikhar Bahl, and Deepak Pathak. Structured world models from human videos. _CoRL_ , 2023. 13 

- [45] Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea Finn, and Abhinav Gupta. R3m: A universal visual representation for robot manipulation. In _Conference on Robot Learning_ , pages 892–909, 2023. 2 

- [46] Soroush Nasiriany, Tian Gao, Ajay Mandlekar, and Yuke Zhu. Learning and retrieval from prior data for skillbased imitation learning. In _Conference on Robot Learning (CoRL)_ , 2022. 13 

- [47] Alexander Quinn Nichol and Prafulla Dhariwal. Improved denoising diffusion probabilistic models. In _International conference on machine learning_ , pages 8162–8171. PMLR, 2021. 4 

10 

- [48] Abby O’Neill, Abdul Rehman, Abhinav Gupta, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, et al. Open x-embodiment: Robotic learning datasets and rt-x models. _arXiv preprint arXiv:2310.08864_ , 2023. 1, 2, 3, 5, 6, 13, 15 

- [49] Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy V. Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel HAZIZA, Francisco Massa, Alaaeldin El-Nouby, Mido Assran, Nicolas Ballas, Wojciech Galuba, Russell Howes, Po-Yao Huang, Shang-Wen Li, Ishan Misra, Michael Rabbat, Vasu Sharma, Gabriel Synnaeve, Hu Xu, Herve Jegou, Julien Mairal, Patrick Labatut, Armand Joulin, and Piotr Bojanowski. DINOv2: Learning robust visual features without supervision. _Transactions on Machine Learning Research_ , 2024. 3, 13 

- [50] Tim Pearce, Tabish Rashid, Anssi Kanervisto, Dave Bignell, Mingfei Sun, Raluca Georgescu, Sergio Valcarcel Macua, Shan Zheng Tan, Ida Momennejad, Katja Hofmann, et al. Imitating human behaviour with diffusion models. _arXiv preprint arXiv:2301.10677_ , 2023. 3 

- [51] William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 4195–4205, 2023. 2, 4 

- [52] Gabriel Quere, Annette Hagengruber, Maged Iskandar, Samuel Bustamante, Daniel Leidner, Freek Stulp, and Joern Vogel. Shared Control Templates for Assistive Robotics. In _2020 IEEE International Conference on Robotics and Automation (ICRA)_ , page 7, Paris, France, 2020. 13 

- [53] Moritz Reuss, Maximilian Li, Xiaogang Jia, and Rudolf Lioutikov. Goal-conditioned imitation learning using scorebased diffusion policies. _arXiv preprint arXiv:2304.02532_ , 2023. 3 

- [54] Erick Rosete-Beas, Oier Mees, Gabriel Kalweit, Joschka Boedecker, and Wolfram Burgard. Latent plans for task agnostic offline reinforcement learning. 2022. 13 

- [55] Saumya Saxena, Mohit Sharma, and Oliver Kroemer. Multiresolution sensing for real-time control with vision-language models. In _7th Annual Conference on Robot Learning_ , 2023. 13 

- [56] Nur Muhammad Mahi Shafiullah, Anant Rai, Haritheja Etukuru, Yiqian Liu, Ishan Misra, Soumith Chintala, and Lerrel Pinto. On bringing robots home, 2023. 13 

- [57] Rutav Shah, Roberto Mart´ın-Mart´ın, and Yuke Zhu. MUTEX: Learning unified policies from multimodal task specifications. In _7th Annual Conference on Robot Learning_ , 2023. 13 

- [58] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Perceiveractor: A multi-task transformer for robotic manipulation. In _Conference on Robot Learning_ , pages 785–799. PMLR, 2023. 2 

- [59] Jiaming Song, Chenlin Meng, and Stefano Ermon. Denoising diffusion implicit models. _arXiv preprint arXiv:2010.02502_ , 2020. 14 

- [60] Austin Stone, Ted Xiao, Yao Lu, Keerthana Gopalakrishnan, Kuang-Huei Lee, Quan Vuong, Paul Wohlhart, Sean Kirmani, Brianna Zitkovich, Fei Xia, et al. Open-world object 

   - manipulation using pre-trained vision-language models. In _Conference on Robot Learning_ , pages 3397–3417, 2023. 2 

- [61] Gemini Team, Rohan Anil, Sebastian Borgeaud, JeanBaptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. Gemini: a family of highly capable multimodal models. _arXiv preprint arXiv:2312.11805_ , 2023. 2 

- [62] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 1, 2, 3, 5, 6, 7, 13, 15 

- [63] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timoth´ee Lacroix, Baptiste Rozi`ere, Naman Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open and efficient foundation language models. _arXiv preprint arXiv:2302.13971_ , 2023. 2 

- [64] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. 2, 3, 13 

- [65] Aaron Van Den Oord, Oriol Vinyals, et al. Neural discrete representation learning. _Advances in neural information processing systems_ , 30, 2017. 2 

- [66] Homer Rich Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, Philippe Hansen-Estruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pages 1723–1736. PMLR, 2023. 13 

- [67] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Kun Wu, Zhiyuan Xu, Ran Cheng, Chaomin Shen, Yaxin Peng, Feifei Feng, et al. Tinyvla: Towards fast, data-efficient visionlanguage-action models for robotic manipulation. _arXiv preprint arXiv:2409.12514_ , 2024. 2 

- [68] Hongtao Wu, Ya Jing, Chilam Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and Tao Kong. Unleashing large-scale video generative pretraining for visual robot manipulation. _arXiv preprint arXiv:2312.13139_ , 2023. 3 

- [69] Hongtao Wu, Ya Jing, Chilam Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and Tao Kong. Unleashing large-scale video generative pre-training for visual robot manipulation. In _The Twelfth International Conference on Learning Representations_ , 2024. 2 

- [70] Ge Yan, Kris Wu, and Xiaolong Wang. ucsd kitchens Dataset. 2023. 13 

- [71] Derek W Yip, Ayoola O Awosika, and Forshing Lui. Physiology, motor cortical, 2024. 2 

- [72] Lijun Yu, Jos´e Lezama, Nitesh B Gundavarapu, Luca Versari, Kihyuk Sohn, David Minnen, Yong Cheng, Vighnesh Birodkar, Agrim Gupta, Xiuye Gu, et al. Language model beats diffusion–tokenizer is key to visual generation. _arXiv preprint arXiv:2310.05737_ , 2023. 2 

- [73] Neil Zeghidour, Alejandro Luebs, Ahmed Omran, Jan Skoglund, and Marco Tagliasacchi. Soundstream: An end- 

11 

to-end neural audio codec. _IEEE/ACM Transactions on Audio, Speech, and Language Processing_ , 30:495–507, 2021. 2 

- [74] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 11975–11986, 2023. 3, 13 

- [75] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 4, 8 

- [76] Gaoyue Zhou, Victoria Dean, Mohan Kumar Srirama, Aravind Rajeswaran, Jyothish Pari, Kyle Hatch, Aryan Jain, Tianhe Yu, Pieter Abbeel, Lerrel Pinto, et al. Train offline, test online: A real robot learning benchmark. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9197–9203. IEEE, 2023. 13, 14 

- [77] Xinghao Zhu, Ran Tian, Chenfeng Xu, Mingyu Ding, Wei Zhan, and Masayoshi Tomizuka. Fanuc manipulation: A dataset for learning-based manipulation with fanuc mate 200id robot. 2023. 13 

- [78] Yifeng Zhu, Abhishek Joshi, Peter Stone, and Yuke Zhu. Viola: Imitation learning for vision-based manipulation with object proposal priors. _6th Annual Conference on Robot Learning (CoRL)_ , 2022. 13 

- [79] Yifeng Zhu, Peter Stone, and Yuke Zhu. Bottom-up skill discovery from unsegmented demonstrations for long-horizon robot manipulation. _IEEE Robotics and Automation Letters_ , 7(2):4126–4133, 2022. 13 

12 

# **CogACT: A Foundational Vision-Language-Action Model for Synergizing Cognition and Action in Robotic Manipulation** 

# _Supplementary Material_ 

## **A. Training Data Details** 

Table I. Our training data mixture using datasets from the Open X-Embodiment dataset [48]. 

### **A.1. Pretraining Data** 

**Vision-Language Data.** Our VLA model is built upon a pretrained VLM, Prismatic [28]. Here, we briefly describe the training data of [28] for self-containedness purposes and refer the readers to [28, 49, 64, 74] for more details. The Prismatic model uses DINOv2 [49] and SigLIP [74] as the vision modules, which were trained with 1.2 billion images and 40 billion image-text pairs, respectively. A LLaMa2 [64] is employed as the LLM backbone, which was trained on 2 trillion language tokens. The vision and LLM modules were further finetuned with 1.2 million multimodal instruct tuning examples by [28]. 

**Vision-Language-Action Data.** We pretrain our model on 25 VLA datasets from Open X-Embodiment [48]. As in Octo [62] and OpenVLA [30], we restrict our training on datasets with single-arm end-effector control and at least one third-person camera perspective. Our data mixture strategy primarily follows [30, 62], except that we do not use the Language Table [41] and Droid [29] datasets in our entire training process due to their significant distribution disparities with other data. The detailed data mixture is listed in Table I. In total, we use 0.4 million robot trajectories containing 22.5 million frames as our training data. 

### **A.2. Finetuning Data for Real Robot Experiments** 

**Realman Robot Setup.** Our hardware setup for the Realman robot experiments is presented in Figure I. We built a robot with two Realman arms on its shoulders, each having 7 degrees of freedom (DoF). We connect the left arm with a 1-DoF gripper and only use this arm in all experiments. We use Intel RealSense camera to capture the RGB image. We perform hand-eye calibration each time we move the camera. We convert all actions in the training data to the camera coordinate system, and the actions generated by the model to the robot coordinate system. To evaluate the generalization ability of our model across different viewpoints, we randomly move the camera before our experiments. Our robot is equipped with a mobile base, which was repositioned randomly before each experiment in order to assess the model’s generalization ability. 

**Franka Robot Setup.** The Franka Robot setup is shown in Figure II. For this embodiment, a robot arm which has 7 DoF is rigidly attached onto a table. We use a Kinect DK 

|Dataset|Ratio|
|---|---|
|Fractal [6]|27.1%|
|Kuka [27]|14.7%|
|Bridge [20,66]|15.3%|
|Taco Play [43,54]|3.4%|
|Jaco Play [18]|0.6%|
|Berkeley Cable Routing [39]|0.3%|
|Roboturk [42]|2.7%|
|Viola [78]|1.1%|
|Berkeley Autolab UR5 [12]|1.4%|
|Toto [76]|2.3%|
|Stanford Hydra Dataset [4]|5.1%|
|Austin Buds Dataset [79]|0.2%|
|NYU Franka Play Dataset [17]|1.0%|
|Furniture Bench Dataset [22]|2.8%|
|UCSD Kitchen Dataset [70]|_<_0.1%|
|Austin Sailor Dataset [46]|2.5%|
|Austin Sirius Dataset [36]|2.0%|
|DLR EDAN Shared Control [52]|_<_0.1%|
|IAMLab CMU Pickup Insert [55]|1.0%|
|UTAustin Mutex [57]|2.6%|
|Berkeley Fanuc Manipulation [77]|0.9%|
|CMU Stretch [44]|0.2%|
|BC-Z [26]|8.6%|
|FMB Dataset [40]|2.4%|
|DobbE [56]|1.6%|


camera on the right to capture RGB images. The actions throughout the entire pipeline are in the robot coordinate system. 

**Data Collection.** We use the touch controller from a Meta Quest 2 device to teleoperate the robot and collect demonstration data for both robots. The translation and rotation of the touch controller are mapped to the gripper’s 3D motion, and a button controls the opening and closing of the gripper. We record video frames at 30 Hz for the Realman robot and 5 _∼_ 6 Hz for the Franka robot. We manually trim the video segments from the recorded full videos and append the language instructions describing the tasks. 

**Data Preprocessing.** We follow the format of the Open X-Embodiment dataset [48] to process both the two fine- 

13 


Table II. Simulated evaluation tasks and their number of trials in SIMPLER. 

|Task|# Trials||
|---|---|---|
||(VM)|(VA)|
|Pick Coke Can|300|825|
|Move Near|240|600|
|Open/Close Drawer|216|378|
|Open Top Drawer and Place Apple|108|189|
|Put Spoon on Towel|120(24_×_5)|N/A|
|Put Carrot on Plate|120(24_×_5)|N/A|
|Stack Green Block on Yellow Block|120(24_×_5)|N/A|
|Put Eggplant in Yellow Basket|120(24_×_5)|N/A|


Figure I. Realman robot setup (right arm not used). 


Figure II. Franka robot setup. 

tuning datasets of the Realman robot and Franka robot. We crop and resize the image to 224×224, and transform the actions to relative translation offset and rotation changes. We calculate the rotation changes in rotation matrix and transform them to Euler angle for training. During training, the Realman robot data is randomly subsampled to 5 Hz with a time interval of 0.2 seconds between frames. The Franka robot data is used as is. 

### **A.3. Data Augmentation and Normalization** 

We utilize data augmentations for images like random crop, random brightness, random contrast, random saturation and random hue. When predicting future actions, for those that exceed the length of the demonstration, we use a stationary action for padding. For the normalization of actions, we normalize them to the range of [ _−_ 1 _,_ 1]. We also tried normalizing the actions to a Gaussian distribution _N_ (0 _,_ 1), but did not observe any performance improvement. 

## **B. Evaluation Details** 

### **B.1. Simulated Evaluation** 

Evaluating robotic manipulation tasks is challenging due to the varying hardware, environments, and tasks used across different studies [33]. While standardized real-world setups 

can be beneficial, they often require substantial time and resources [10, 16, 31, 76]. To address these issues while preserving the accuracy of real-world performance evaluations, SIMPLER [33] has developed a system for evaluating manipulation policies trained on real data in simulated environments. Therefore, we employs SIMPLER for our evaluations, offering an easily reproducible and completely fair assessment framework. 

**Task Definitions.** We utilize all task variants provided in SIMPLER for our evaluations. The Google robot setup includes the following tasks: 1) “pick Coke can”, 2) “move _{_ obj1 _}_ near _{_ obj2 _}_ ”, 3) “(open / close) (top / middle / bottom) drawer”, and 4) “open top drawer; place apple into top drawer”. The WidowX robot setup includes: 1) “put the spoon on the towel”, 2) “put carrot on plate”, 3) “stack the green block on the yellow block”, and 4) “put eggplant into yellow basket”. For the Google robot setup, both _Visual Matching_ (VM) and _Variant Aggregations_ (VA) evaluations are provided (See Sec. 4.1 in the main paper), while only the _Visual Matching_ (VM) evaluation is provided for the WidowX robot setup. 

The total number of trials for each sub-task is shown in Table II. Note that to accommodate the limited number of the original trials (24 per task) on the WidowX robot, we repeat each original task trial five times (with different random initialization seeds) to enhance the statistical significance. For more detailed information on the tasks and evaluation protocols, we refer the readers to the SIMPLER paper [33]. 

**Implementation Details.** All simulated evaluations are conducted on a single NVIDIA A6000 GPU or a single NVIDIA A100 GPU. During inference, we employ DDIM [59] sampling with 10 sampling steps and a classifier-free guidance (CFG) [23] coefficient of 1.5. 

We apply a unified adaptive action ensemble strategy (described in Sec. 3.4 in the main paper) across all our models, where the hyperparameter _α_ is set to 0 _._ 1. The ensemble window size _K_ determines the number of historical obser- 

14 


Figure III. Seen task setups on the Realman robot. 


Figure IV. Unseen task setups on the Realman robot. 

vations and their predicted actions to be used. Since different dataset have varying control frequency and robot speed, the window size _K_ should be adaptive. We select the window size _K_ such that the product of _K_ and the average standard deviation ( _std_ ) of the 6D action per timestep remains constant across different datasets. Formally, this relationship can be expressed as _C_ = _K × std_ , where _C_ is a constant representing the distance and angle traversed by the robot over the last _K_ steps. Empirically, we set the _C_ to 0 _._ 2 for all experiments and derive their _K_ accordingly. 

For the experiments on the Google robot, the task success rates of the pervious methods were evaluated by [33] and incorporated into this paper, except for OpenVLA [30], which was not included in [33]. For OpenVLA, we directly evaluate it using the weight from its official repository<sup>6</sup> . On the WidowX robot, the performance of RT-1-X [48] is directly reported as in [33] and OpenVLA is evaluated as described above. For Octo-Base and Octo-Small [62], we incorporate more random seeds and conduct five retests to mitigate volatility in their probabilistic sampling. For all configurations of our models, we evaluate them using the same number of tests as those used for Octo. Note that the performance of RT-2-X on WidowX has not been reported [33], and no model weights are publicly available for evaluation. 

**Visualization Results.** Figure V provides the successful examples of each task executed by our default model on the Google robot, while Figure VI presents those on the WidowX robot. 

> 6https://huggingface.co/openvla/openvla-7b-prismatic 

Table III. The hyperparameters of different action modules. 

|Action Model|# Layers|Emb Dim|# Heads|# Params|
|---|---|---|---|---|
|MLP (3-Layer)|3|256|N/A|3M|
|MLP (7-Layer)|7|1024|N/A|89M|
|DiT-Small|6|384|4|13M|
|DiT-Base|12|768|12|89M|
|DiT-Large|24|1024|16|308M|


### **B.2. Real-World Evaluation** 

**Task Definitions.** Section 4.2 in the main paper defines three tasks “Pick”, “Stack” and “Place” on the Realman robot. The setups of these tasks in the seen environment are illustrated in Figure III, while those on the unseen table are illustrated in Figure IV. Section 4.3 in the main paper defines four tasks: “Close the oven door”, “Open the oven door”, “Pick up the green brush” and “Pick up a bowl containing food”. The setups of these tasks are presented in Figure IX. 

**Implementation Details.** The finetuning process was conducted on 16 NVIDIA A100 GPUs, with all models involved in the comparison utilizing PyTorch FSDP for full finetuning and a batch size of 256. For our method, we simply tested one finetuned checkpoint at 10K finetuning steps, which takes 7.5 hour’s finetuning time. For Octo [62] and OpenVLA [30], we tested multiple finetuned checkpoints at different steps and select the ones that worked best in the real-world tasks. Specifically, for the Realman robot, Octo uses the 20K checkpoint, while OpenVLA uses the 30K checkpoint; both models use the 30K checkpoint on the Franka robot. All finetuning data follows the same data augmentation as used during pretraining. 

**Visualization results.** Figure VII and VIII present evaluation examples of each tasks executed by our default model on the Realman robot, while Figure IX provides evaluation examples of each tasks on the Franka robot. 

## **C. Ablation Study Details** 

### **C.1. Action Model Architectures** 

As described in Sec. 4.4 in the main paper, we study the performances of different action models on the Google robot and WidowX robot. Table III presents the hyperparameters of all the action modules mentioned in Sec. 4.4. The MLP components of these models are structured such that each MLP block expands the embedding dimension by four times and then scales it back to the original embedding dimension. The structure of the MLP (3-layer) model is consistent with the model architecture in Octo [62]. Table 7 in the main paper illustrates that such small action models have significant limitations in modeling actions and perform far worse than the DiT models. 

15 


Figure V. Visual examples of each task on the Google robot driven by our model. 

Table IV. Comparison of different classifier-free guidance coefficients [23] in simulated evaluations. 

|CFG Scale|G<br>(VM)|R<br>(VA)|WR<br>(VM)|Average|
|---|---|---|---|---|
|1.0|66.9|54.0|46.3|55.7|
|1.5|74.8|61.3|**51.3**|62.5|
|3.0|**76.6**|**63.1**|48.3|**62.7**|


### **C.2. Classifier-Free Guidance Scale** 

During inference, the classifier-free guidance (CFG) is always applied with a default scale of 1 _._ 5, as the experiments show that incorporating the CFG technique significantly improves success rates. Different CFG scales are evaluated in Table IV. 

16 


Figure VI. Visual examples of each task on the WidowX robot driven by our model. 

17 


Figure VII. Examples of real-world seen tasks and unseen-table-with-unseen-distractors tasks on the Realman robot driven by our model. 

18 


Figure VIII. More examples of different real-world tasks on the Realman robot using our model. 

19 


Figure IX. Visual examples of real-world tasks on the Franka robot using our model. 

20 

