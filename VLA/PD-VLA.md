---
title: "PD-VLA: Accelerating Vision-Language-Action Model Integrated with Action Chunking via Parallel Decoding"
date: "2025-03-04"
authors: "Wenxuan Song; Jiayi Chen; Pengxiang Ding; Han Zhao; Wei Zhao; Zhide Zhong"
venue: "IROS 2025"
url: https://arxiv.org/abs/2503.02310
pdf: https://arxiv.org/pdf/2503.02310
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2503.02310)** / [論文ページ](https://arxiv.org/abs/2503.02310)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **PD-VLA: Accelerating Vision-Language-Action Model Integrated with Action Chunking via Parallel Decoding** 

Wenxuan Song<sup>*1</sup> , Jiayi Chen<sup>*1,5</sup> , Pengxiang Ding<sup>2,3</sup> , Han Zhao<sup>2,3</sup> , Wei Zhao<sup>2</sup> , Zhide Zhong<sup>1</sup> , Zongyuan Ge<sup>4</sup> , Zhijun Li<sup>5</sup> , Donglin Wang<sup>2</sup> , Lujia Wang<sup>1</sup> , Jun Ma<sup>1</sup> , Haoang Li<sup>1</sup> 


Fig. 1: Comparison between the proposed parallel decoding on the left and traditional autoregressive (AR) decoding on the right. Unlike AR decoding, which predicts action tokens sequentially, our parallel decoding simultaneously predicts all the tokens in parallel. 

**_Abstract_ — Vision-Language-Action (VLA) models demonstrate remarkable potential for generalizable robotic manipulation. The performance of VLA models can be improved by integrating with action chunking, a critical technique for effective control. However, action chunking linearly scales up action dimensions in VLA models with increased chunking sizes. This reduces the inference efficiency. Therefore, accelerating VLA integrated with action chunking is an urgent need. To tackle this problem, we propose PD-VLA, the first parallel decoding framework for VLA models integrated with action chunking. Our framework reformulates autoregressive decoding as a nonlinear system solved by parallel fixedpoint iterations. This approach preserves model performance with mathematical guarantees while significantly improving decoding speed. In addition, it enables training-free acceleration without architectural changes, as well as seamless synergy with existing acceleration techniques. Extensive simulations validate that our PD-VLA maintains competitive success rates while achieving 2.52** _×_ **execution frequency on manipulators (with 7 degrees of freedom) compared with the fundamental VLA model. Furthermore, we experimentally identify the most effective settings for acceleration. Finally, real-world experiments validate its high applicability across different tasks.** 

This work was supported in part by the National Natural Science Foundation of China under Grant 62403401, in part by the Guangdong Basic and Applied Basic Research Foundation under Grant 2024A1515011992, in part by the Department of Education of Guangdong Province under Grant 2024KQNCX030, in part by the Guangzhou Municipal Education Project under Grant 2024312104, and in part by the Guangzhou-HKUST (GZ) Joint Funding Program under Grant 2025A03J3716. Corresponding Author: Haoang Li (haoangli@hkust-gz.edu.cn) 

*Wenxuan Song and Jiayi Chen contributed equally to this work. 

## I. INTRODUCTION 

The pursuit of robust and generalizable robotic manipulation policies remains a fundamental challenge in embodied AI research [1]. Recent advancements in Vision-Language Models (VLMs) [2], [3] have showcased impressive multimodal understanding capabilities, inspiring the development of Vision-Language-Action (VLA) models [4], [5], [6], [7], [8], [9]. These end-to-end architectures, which are trained on large-scale robotic datasets [10], [11], integrate visual perception and language understanding to directly generate executable actions. This emerging paradigm shows strong effectiveness and generalization in diverse scenarios. 

Recent VLA work [12], [13], [14] has explored the integration with action chunking [15], which highly improves the performance of VLA models in laboratory scenarios. However, action chunking dramatically increases the action dimensions in a single inference. For typical manipulators with 7 degrees of freedom (DoF) (including 3-DoF translation, 3-DoF rotation, 1-DoF gripper), an action chunk of _m_ steps creates 7 _m_ -dimensional action sequences. This linearly increases single-inference time when autoregressive (AR) decoding is employed in VLA models. The reason is that AR decoding sequentially predicts each token in an one-by- 

> 1The Hong Kong University of Science and Technology (Guangzhou), Guangzhou, China. 

> 2Westlake University, Hangzhou, China. 

> 3Zhejiang University, Hangzhou, China. 

> 4Monash University, Melbourne, Australia. 

> 5Harbin Institute of Technology, Harbin, China. 

TABLE I: Comparison between different acceleration methods for VLA models. “Model-redesign-free” indicates that a method does not redesign the foundation models. “Training-free” indicates that a method does not need training. “Modification-free” indicates that a method does not require modifications or adding auxiliary components to pre-trained VLA models. 

|Methods<br>M|odel-redesign <br>free|Training- <br>free|Modification-<br>free|
|---|---|---|---|
|TinyVLA [16]|_×_|-|-|
|RoboMamba [17]|_×_|-|-|
|QAIL [18]|✓|_×_|_×_|
|DeeR-VLA [19]|✓|_×_|_×_|
|VLA w/ Sparse.[20]|✓|✓|_×_|
|VLA w/ FastV [21]|✓|✓|_×_|
|VLA-Cache [22]|✓|✓|_×_|
|PD-VLA (ours)|✓|✓|✓|


one manner. As a result, the generation time is proportional to the predicted token length. Therefore, there is an urgent need to accelerate the decoding process for VLA models integrated with action chunking. 

To address the above challenges, we present a novel parallel decoding framework for the mainstream VLA model with action chunking, called **P** arallel **D** ecoding for **VLA** ( **PD-VLA** ). Fig. 1 illustrates the core concept of our parallel decoding approach. Our key insight reframes AR action decoding as a system of nonlinear equations solved through parallel fixed-point iteration methods, e.g., Jacobi fix-point iteration method [23]. This approach preserves model performance with mathematical guarantees while significantly improving decoding speed. Please note that we only accelerate the decoding process during VLA inference. Accordingly, our method enables friendly deployment, compared with existing methods, i.e., it achieves training-free acceleration without redesign and modification of models (see Table I). Moreover, our method achieves seamless synergy with existing acceleration techniques. 

We validate our PD-VLA in extensive simulation and realworld experiments. In simulation experiments, our method achieves significant acceleration without compromising performance. Compared to the fundamental VLA model, our PD-VLA achieves 2.52 _×_ execution frequency. Furthermore, we experimentally identify the most effective settings for acceleration. Finally, the real-world experiments show the strong applicability of PD-VLA, especially in the dexterous tasks, such as pouring the water. 

Our primary contributions include: 

- We propose the first parallel decoding framework for VLA models integrated with action chunking. It preserves action performance while eliminating the bottlenecks in the efficiency of autoregressive decoding. 

- We design a decoding-process-only acceleration strategy for VLA inference. It enables friendly deployment on VLA models and seamlessly synergizes with other acceleration methods. 

- We conduct comprehensive empirical validation across simulation and real-world platforms, with ablation stud- 

ies characterizing performance tradeoffs. 

## II. RELATED WORKS 

## _A. Vision-Language-Action Models_ 

Vision-language-action (VLA) models are designed to process both visual feedback from robotic systems and natural language operation instructions as input, generating executable commands for robots. Several large-scale VLA models [5], [9], [24], [25] have been developed by finetuning pre-trained multimodal large models, which inherently possess strong visual question answering (VQA) capabilities, on extensive robot datasets. These methods have shown strong performance in both simulated and real-world tasks. However, the inference speed of VLA models with a large number of parameters is relatively slow, which prevents them from achieving high control frequencies and further limits the consistency of their actions and their effectiveness when learning flexible tasks from high-frequency demonstrations [13]. This paper aims to improve inference speed, thereby partially alleviating the aforementioned issues. 

## _B. Action Chunking_ 

Predicting and executing a sequence of actions without intermediate replanning, which is known as action chunking, is increasingly used in robot learning from human demonstrations. This approach involves two key strategies. First, it predicts multi-step action sequences and executes them either fully or partially [15], [26]. Second, it models the distribution of action chunks and performs sampling from the learned model, either independently [26], [27] or with weak dependencies [28], [15], to facilitate sequential decision-making. While some research highlights the effectiveness of this method in achieving high-performing policies in laboratory settings [15], [26], other studies report contrasting results in real-world applications [29]. Further, [30] analyzed the different outcomes under practical conditions and proposed a bidirectional decoding to balance consistency and reactivity. One of the state-of-the-art VLA model, pi0 [12], use an action chunking architecture with flow matching to represent complex continuous action distributions. It validates the effectiveness of action chunking in VLA models. In this paper, we aim to tackle a significant problem existing in the VLA models with action chunking that the inference speed is severely limited. 

## _C. Acceleration for Vision-Language-Action Models_ 

Various acceleration strategies, including quantization [31] and token pruning [21], have been effectively applied to LLMs, yet they often fail to meet the stringent real-time requirements of action generation. Efforts to enhance efficiency have led to architectural modifications in VLA models, such as DeeR-VLA [19], which dynamically adjusts inference depth, and QAIL [18], which integrates quantization-aware training. Further innovations, like RoboMamba [17] and TinyVLA [16], replace traditional attention mechanisms or focus on developing lightweight models from the ground up, frequently necessitating model re-training and additional 


Fig. 2: The network architecture of our PD-VLA with a chunk size of _m_ . Given images, proprioception and language instructions, our method first tokenizes the input and then feeds the results into the LLM in a parallel decoding manner. The LLM outputs action tokens, which are finally detokenized into valid action values and deployed on the mechanical arm. 

data collection. Meanwhile, VLA-Cache [22] selectively caches static tokens and recomputes only dynamic or taskrelevant ones. FAST [13] proposes a compression-based tokenization scheme based on the discrete cosine transform. In contrast, our PD-VLA enhances inference speed by optimizing the decoding mechanism, offering a more practical and deployment-friendly solution compared to the above methods, as shown in Table I. 

## III. METHOD 

In this section, we introduce the details of our method PD-VLA. We first present the architecture of our VLA model in subsection III-A. Subsequently, we incorporate action chunking with our VLA model in subsection III-B. Finally, we present parallel decoding to accelerate inference in subsection III-C. 

## _A. Vision-language-action Model_ 

**Model Architecture.** We build a fundamental VLA model, LLaVA-VLA, on the widely recognized vision-language model, LLaVA [32], ensuring a generalizable and comprehensive exploration. LLaVA mainly consists of a large language model LLM and a vision encoder _f_ encoder. It takes two images as input, a static image _I_ static and a gripper image _I_ gripper, to get a comprehensive observation. Then the images are processed through _f_ encoder into the visual tokens _hI_ . Along with the input images, the text instructions and proprioceptive input are first concatenated into a unified instruction _S_ , which is then tokenized into tokens _hS_ via a tokenizer _T_ . Then the LLM takes in text tokens _hS_ and image tokens _hI_ and autoregressively generates action tokens _h_ act. Finally, the action tokens are detokenized into 7-dimensionl action _a_ . The whole process can be formulated as: 


**Action Tokenization.** Here, we discretize a continuous action _a_ into 256 uniformly spaced bins and represent them as integer indices. Specifically, we utilize the 256 least frequently used tokens in the language model vocabulary to serve as action tokens _h_ act. Therefore, the robot action 

tokens across all dimensions can be concatenated with a space character to form a textual string, which serves as the training label. Consequently, a 7-dimensional action _a_ is formatted as: 


where _X, Y, Z_ represent the Cartesian coordinates of the end effector’s position, _ϕ, θ, ψ_ denote the rotation angles of the end effector along each axis, and _G_ is the gripper state. 

## _B. Action Chunking for VLA Models_ 

Based on the above fundamental VLA model, we incorporate the action chunking [15] techniques. Recent works have pursued a generative approach equipped with action chunking, which predicts a sequence of actions over multiple time steps and executes all or part of the sequence [15], [26], [30]. Some studies find this approach improves manipulation performance and execution inference in imitation learning [15], diffusion policies [26], [27], and VLA models [14]. Action chunking allows the learner to better capture temporal dependencies in demonstrations and generate more consistent and stable actions [30]. We integrate action chunking with the VLA model by extending the effective action horizon (chunk size). At the current time step _t_ , given chunk size _m_ , the predicted actions will be extended into an action sequences _A⊔_ = [ _at, at_ +1 _, at_ +2 _, ..., at_ + _m−_ 1], where each element is defined in Equation (1). Here, following previous work [14], we set the chunk size to 5. 

However, extended action sequences consume longer single inference time, which impacts the continuity and effectiveness of the actions. Therefore, there is an urgent need to propose a more efficient action decoding method. 

## _C. Parallel Decoding for VLA Models_ 

To meet the demands of a more efficient decoding algorithm, we propose parallel decoding for VLA models integrated with action chunking. In this subsection, we first revisit the theory of AR decoding. Then, by leveraging Jacobi decoding, we break the sequential dependency to achieve parallel decoding, and further analyze and refine the 

approach based on the structural characteristics of VLA. Finally, we analyze the acceleration phenomenon demonstrated by parallel decoding. 

**Preliminary: Jacobi Decoding.** Given a prompt **_x_** , comprising both textual and visual components, and a pre-trained LLM model _p_ ( _·|_ **_x_** ), we typically predicte tokens using the standard AR decoding method under a greedy strategy, _i.e._ , 


where _Yi_ denotes _{y_ 1 _, . . . , yi−_ 1 _}_ , _n_ denotes the decoding horizon, representing the number of tokens to predict. As shown in Fig. 1, _n_ forward passes of the LLM are required to obtain _n_ tokens _Yn_ . The sequential characteristic in AR decoding restricts the efficient generation of a lengthy token sequence. 

Compared with the aforementioned AR decoding, Jacobi decoding [33], [34] has shown the capacity to tackle lengthy token sequences. Concretely, supposing _f_ ( _yi, Yi,_ **_x_** ) := _yi −_ arg max _y p_ ( _y|Yi,_ **_x_** ), Jacobi decoding re-frames the inference process of LLM in Equation (3) as solving a system of nonlinear equations with respect to _yi_ : 


There are _n_ unknown parameters _yi_ in the nonlinear equation system including _n_ Equation (4). Considering Equation 3, the system of nonlinear equation system can be formulated as: 


which can be solved in the Jacobi fix-point iteration method [23] by using a causal attention mask. **Our Jacobi Decoding-based Acceleration.** In this part, we will introduce how we apply the above Jacobi Decoding to the VLA model. We first randomly initialize an action token sequence of equal length to the decoding horizon _n_ . Both the prompt _x_ and the initialized action sequence _Y_<sup>(0)</sup> = _{y_ 1<sup>(0)</sup><sup>_, . . . , y_</sup> _n_<sup>(0)</sup><sup>_}_are fed into the VLA model simultaneously.</sup> To break the sequential dependencies in the conventional VLA model, we replace the above causal attention mechanism with a bidirectional attention mechanism, which reformulate the system of nonlinear equations Equation 5 as: 


This enables updates of all action tokens in every single iteration. The iterations terminate at the step _k_ where _Y_<sup>(</sup><sup>_k_)</sup> = _Y_<sup>(</sup><sup>_k−_1)</sup> , and the _Y_<sup>_∗_</sup> := _Y_<sup>(</sup><sup>_k_)</sup> is defined as the fixed point. The 

acceleration achieved by Jacobi decoding originates from its ability to predict multiple tokens in the _n_ -token sequence in parallel during each forward pass. Therefore, the total number of updating iterations _k_ can be smaller than AR decoding, i.e., _k ≤ n_ . 

Different decoding horizons _n_ result in different parallel decoding patterns, which further influence the effectiveness. When _n_ is less than the total action dimensions _l_ , it decodes _n_ action token in one iteration and then proceeds to the next _n_ token, until covering the total _l_ token. In mathematics, it equals several Jacobi decodings with several Gauss-Seidel steps. The decoding horizon _n_ is often selected as powers of 2. For a VLA model with a chunk size of _m_ , the response length is _l_ = 7 _m_ +2, with the addition of a blank beginning token and an ending token. However, when the value of _l_ is not powers of 2, some redundant tokens may be predicted. Considering the structural properties of the VLA task, setting the per-action dimension as the value of _n_ is a feasible approach to enable the model to better learn the physical meaning of action. A simple but effective idea is to set _n_ = _l_ , which enables inference finished in a single Jacobi decoding. This configuration is more conducive to enabling the model to inherit the action modeling capabilities of the original distribution. Following the analysis above, we select 7, 16, and 37 as the value of _n_ , to better analyze the effectiveness of different decoding horizons. 

In the following, we will analyze an acceleration phenomenon caused by parallel decoding. During decoding, our PD-VLA exhibits the capability of predicting correct action tokens preemptively, even with preceding incorrect tokens, while ensuring the tokens remain unchanged. We term such tokens as _fixed tokens_ , whose existence allows simultaneous extension of discontinuous correct tokens within the _n_ -token sequence. In particular, for VLA models, the token denoting gripper opening only has two values, 0 for close and 1 for open, which tokens are easier to predict as _fixed tokens_ . This phenomenon contributes to the fast convergence in parallel decoding, thereby leading to a considerable generation speedup. 

## IV. EXPERIMENTS 

We concentrate on several experiments to answer the following questions: **Q1.** How does the effectiveness of PDVLA compare with baselines and other acceleration methods? **Q2.** Is the coordination among different components effective? **Q3.** How does the acceleration phenomenon vary across different decoding horizons? **Q4.** Can PD-VLA be effectively deployed in real-world robotic systems? 

## _A. Experiments Setup_ 

**Simulation environment.** The CALVIN benchmark [35] is built on top of the PyBullet [46] simulator and involves a Franka Panda Robot arm that manipulates the scene. CALVIN consists of 34 tasks and 4 different environments (A, B, C and D). We evaluate all methods on the classic CALVIN ABCD _→_ D setup [35]. We report the success rate and the average number of completed sequential tasks. 

TABLE II: Comparison with various manipulation baselines in terms of success rate and average length. 

|Method|Input|Data|1/5|Succ<br>2/5|ess Rate<br>3/5|(%)<br>4/5|5/5|Avg. len.<br>ABCD_→_D|
|---|---|---|---|---|---|---|---|---|
|MCIL [35]|RGB|ALL|37.3|2.7|0.2|0.0|0.0|0.40|
|HULC [36]|RGB|ALL|89.2|70.1|54.8|42.0|33.5|2.90|
|RT-1 [4]|RGB|LANG|84.4|61.7|43.8|32.3|22.7|2.45|
|LLaVA-VLA|RGB|LANG|72.0|29.0|12.0|6.0|1.9|1.20|
|PD-VLA (ours)|RGB|LANG|**94.1**|**80.0**|**68.3**|**61.4**|**50.5**|**3.54**|


TABLE III: **Ablation study** . We ablate 2 core components of our methods, action chunking (AC) and parallel decoding (PD), to emphasize their significance. In addition, we replace PD with other acceleration methods. Here, we select 2 state-of-the-art training-free methods for VLM. 

|Method|1/5|Succ<br>2/5|ess Rate<br>3/5|(%)<br>4/5|5/5|Avg. len.<br>ABCD_→_D|Avg. Speed<br>(Token/s)|Frequency<br>(Hz)|
|---|---|---|---|---|---|---|---|---|
|LLaVA-VLA|72.0|29.0|12.0|6.0|1.9|1.20|39.56|1.81|
|w/o AC|71.0|25.0|8.0|6.0|2.0|1.12|39.86|1.82|
|w/o PD|91.8|82.4|71.0|62.8|52.6|3.61|41.44|3.60|
|w/o PD, w/ FastV|90.1|77.2|62.4|55.4|46.5|3.31|28.69|2.54|
|w/o PD, w/ SparseVLM|83.2|63.2|46.0|36.0|26.4|2.55|32.43|2.83|
|PD-VLA (ours)|94.1|80.0|68.3|61.4|50.5|3.54|52.84|4.56|


TABLE IV: **Evaluation and comparison on the LIBERO benchmark.** 

|**Method**|**Spatial**|**Object**|**Goal**|**Long**|**Average**|
|---|---|---|---|---|---|
|Diffusion Policy [26]|78.3%|92.5%|68.3%|50.5%|72.4%|
|Octo [6]|78.9%|85.7%|84.6%|51.1%|75.1%|
|OpenVLA [37]|84.9%|88.4%|79.2%|53.7%|76.5%|
|SpatialVLA [38]|88.2%|89.9%|78.6%|55.5%|78.1%|
|CoT-VLA [39]|87.5%|91.6%|87.6%|69.0%|81.1%|
|WorldVLA [40]|87.6%|96.2%|83.4%|60.0%|81.8%|
|ThinkAct [41]|88.3%|91.4%|87.1%|70.9%|84.4%|
|_π_0-FAST [42]|96.4%|96.8%|88.6%|60.2%|85.5%|
|MolmoAct [43]|87.0%|95.4%|87.6%|77.2%|86.6%|
|FlowVLA [44]|93.2%|95.0%|91.6%|72.6%|88.1%|
|DreamVLA [45]|**97.5%**|94.0%|89.5%|89.5%|92.6%|
|_π_0 [12]|96.8%|**98.8%**|**95.8%**|85.2%|94.2%|
|PD-VLA (ours)|95.5%|96.7%|94.9%|**91.7%**|**94.7%**|


LIBERO [47] is another widely-used simulated manipulation benchmark with 4 suites (Spatial, Object, Goal, Long). We report the success rate for each evaluation suite as well as the overall average, where each suite comprises 10 tasks, and each task is evaluated over 50 rollouts. 

**Evaluate metrics.** The CALVIN long-horizon challenge is a sequential task comprising five subtasks. We report the success rates for each subtask and the average completed length across all five tasks. To quantitatively evaluate inference speed, we introduce inference speed (measured in tokens per second). Additionally, considering the requirements of robotic tasks, we also report execution frequency (in Hertz, Hz). 

**Implementation details.** In this paper, we use vicuna-7bv1.5 [48] as the LLM backbone and clip-vit-large-patch14336 [49] as the vision encoder to build LLaVA-7b-v1.5 [32]. **Training details.** Our fundamental model LLaVA-VLA is trained using 8 NVIDIA H100 GPUs over 1 epoch, which requires approximately 10 hours. Notably, our PD-VLA does not incur extra training costs. 

## _B. Results on CALVIN Benchmark_ 

**Comparison with other models.** In Table II, we benchmark our method against several representative models. For a comprehensive comparison, we include various baselines, such as the official MCIL [35] model and other prevalent models like HULC [36] and RT-1 [4]. Our method demonstrates competitive performance, with PD-VLA achieving significant improvements over the fundamental LLaVA-VLA model, further validating its effectiveness. 

**Comparison with other acceleration methods for VLA models.** For fair comparisons, we deployed 2 state-ofthe-art VLM acceleration methods, FastV [21] and SparseVLM [20], on the traditional VLA model with action chunking. However, neither FastV nor SparseVLM really improves the inference speed. While FastV largely preserves manipulation performance, masking tokens in attention computation incurs additional overhead, leading to slower inference speeds. SparseVLM witnesses decrease both in success rates and inference speed because it incurs extra costs from 

token pruning, merging, and recycling. 

## _C. Results on LIBERO Benchmark_ 

We further validate the superior performance of PD-VLA on the LIBERO benchmark. Notably, this variant corresponds to our method integrated with an action head, following the OpenVLA-OFT [50] setting. Compared with prior stateof-the-art approaches, PD-VLA achieves the best average performance, attaining a 91.7% success rate on the most challenging LIBERO-Long benchmark. 

## _D. Ablation Study_ 

Table III presents a detailed summary of the ablation studies performed on two key components of our PD-VLA. These components enable PD-VLA to improve 2.34 in success rates and realize 2.52 _×_ execution frequency compared to the fundamental model LLaVA-VLA. The ablation findings are as follows: 

First, the ablation study of the action chunking demonstrates a significant performance boost with its inclusion. By extending chunk sizes, the consistency and stability is improved, showing 2.42 improvements in average length. However, the decoding speed is still limited, resulting in a longer single inference time. By reducing inference counts, the execution frequency is improved 2.51 _×_ . 

Second, the ablation study of parallel decoding reveals the inefficiency in the inference process. Parallel decoding substantially increases the average decoding speed by 1.28 _×_ , thus the single inference time is reduced and satisfies the demand of high-frequency inference. 

The above two key components complement each other: action chunking enhances action consistency while improving execution frequency, whereas parallel decoding mitigates inference inefficiency by accelerating the decoding process. Together, they strike a balance between performance and high-frequency inference. 

## _E. Decoding Horizon and Acceleration Phenomenon_ 

We further conduct an in-depth investigation into the differences in acceleration phenomenon across various decoding horizons and their impact on performance. We compare methods with different decoding horizons in Table V on the numbers of _fixed_ tokens, average length, decoding speed, and execution frequency. The method with a decoding horizon of 37 shows the strongest manipulation abilities with the highest decoding speed. This setting ensures the inheritance of the modeling of the original action distribution by predicting the whole action sequences together. The 7- token method performs better than the 16-token one because it aligns with the distribution of the single action, facilitating more efficient decoding in accordance with the action structure. With the increasing decoding horizon, the number of _fixed_ tokens increases accordingly, which contributes to the decoding speed improved from 41.48 to 52.84 tokens/second. Notably, the redundant tokens when _n_ = 16 make execution frequency even lower. 

Fig. 4 illustrates the speed distribution of different decoding horizons. We observe a remarkable increase in maximum 

TABLE V: Analysis of the different decoding horizons and acceleration phenomenon between them. 

|decoding|fixed|Average|Avg. Speed|Frequency|
|---|---|---|---|---|
|horizon|token count|length|(Token/s)|(Hz)|
|7|5.17|3.24|41.48|3.60|
|16|6.75|3.19|48.74|3.25|
|37|**8.75**|**3.64**|**52.84**|**4.56**|


TABLE VI: Comparison with LLaVA-VLA in the real world. We report success rates as metrics. 

|Method|“push button”|“lift block”|“pour water”|
|---|---|---|---|
|LLaVA-VLA|60%|40%|10%|
|PD-VLA|80%|70%|60%|


speed as _n_ grows. At _n_ = 37, the maximum speed reaches approximately twice that of _n_ = 7 and AR, thanks to the reduction of the number of iterations. This finding highlights the potential of parallel decoding to achieve greater acceleration. 

## _F. Real-world Experiments_ 

**System set-up.** The real-world settings are shown in Fig. 5 We set up real-world experiments based on a 6-DOF Unitree Z1-Pro mechanical arm with a 1-DOF gripper. We provide images using an ORBBEC Femto Mega camera at a front view. We collect a small robotic dataset including 3 tasks: push the button, lift the block, and pour the water into the bowl. Each task contains 50 demonstrations and evaluates 10 episodes for success rates. 

**Quantative Results.** Table VI shows that our PD-VLA got higher success rates compared with LLaVA-VLA. Benefiting from the strong visual generalization capabilities of the pretrained VLM, both LLaVA-VLA and PD-VLA successfully accomplish “push button” and “lift block”. However, thanks to the combination of action chunking and parallel decoding, PD-VLA can produce more consistent actions, resulting in 20% and 30% improvements in success rates, respectively. For the task “pour water”, LLaVA-VLA failed to complete this task, while PD-VLA has a 50% higher success rate. This task challenges the flexibility and manipulation abilities of models, PD-VLA has a higher execution frequency and adjusts the action according to the real-time image. 

**Visualization.** Fig. 3 presents visualizations of real-world experiments on three tasks. All tasks include distractors to validate the robustness of the model. In the “push button” task, the model successfully identifies the red button and moves the end-effector to press it. In the “lift block” task, the model accurately recognizes the small blue cube, precisely positions the end-effector, opens it for a firm grasp, and then lifts the robotic arm. The “pour water” task requires more dexterous manipulation, as it involves a non-flexible endeffector grasping a non-rigid plastic bottle and tilting it to pour water into a bowl. Any inconsistency during the grasping process could easily lead to the bottle being dropped. However, PD-VLA demonstrates smooth and consistent actions throughout the process, successfully completing the 


Fig. 3: **Representative results of real-world experiments** . The sequential images showcase the trajectories of a robotic arm successfully executing three tasks. 


Fig. 4: Comparison of minimum, average, and maximum inference speed (tokens per second) between AR decoding and parallel decoding with different decoding horizons _n_ . 

In the future, we will focus on optimizing the decoding algorithm and model to prevent redundant iteration processes during parallel decoding, thereby enabling faster convergence to a fixed point. 

## VI. ACKNOWLEDGEMENT 

We sincerely thank Wei Li and Jie He for their valuable assistance in implementing the variant equipped with the action head. 


Fig. 5: Real-World Setup. The left panel shows the mechanical arm and the right panel shows the camera used. 

task. This demonstrates its suitability for real-time robotic applications. 

## V. CONCLUSION 

This paper analyzes the inefficiency of autoregressive VLA models integrated with action chunking. Therefore, we propose PD-VLA, which is a novel parallel decoding method designed for the VLA model integrated with action chunking. Instead of predicting each action token sequentially, our PDVLA tries to predict every token simultaneously in several iterations, thus hugely improving the decoding efficiency. Benefiting from parallel decoding and action chunking, the model strikes a balance between performance and highfrequency inference. Extensive experiments demonstrate that our PD-VLA significantly improves inference speeds and execution frequency while maintaining competitive success rates. Real-world experiments validate the effectiveness of PD-VLA in the real world. 

## REFERENCES 

- [1] K. Kim, Y. Gu, J. Song, S. Zhao, and S. Ermon, “Domain adaptive imitation learning,” in _International Conference on Machine Learning_ . PMLR, 2020, pp. 5286–5295. 

- [2] A. Awadalla, I. Gao, J. Gardner, J. Hessel, Y. Hanafy, W. Zhu, K. Marathe, Y. Bitton, S. Gadre, S. Sagawa, J. Jitsev, S. Kornblith, P. W. Koh, G. Ilharco, M. Wortsman, and L. Schmidt, “Openflamingo: An open-source framework for training large autoregressive visionlanguage models,” _arXiv preprint arXiv:2308.01390_ , 2023. 

- [3] H. Liu, C. Li, Q. Wu, and Y. J. Lee, “Visual instruction tuning,” _Advances in neural information processing systems_ , vol. 36, 2024. 

- [4] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, , _et al._ , “Rt-1: Robotics transformer for real-world control at scale,” _Proceedings of Robotics: Science and Systems_ , 2023. 

- [5] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 

- [6] Octo Model Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, C. Xu, J. Luo, T. Kreiman, Y. Tan, L. Y. Chen, P. Sanketi, Q. Vuong, T. Xiao, D. Sadigh, C. Finn, and S. Levine, “Octo: An open-source generalist robot policy,” in _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, 2024. 

- [7] D. Niu, Y. Sharma, G. Biamby, J. Quenum, Y. Bai, B. Shi, T. Darrell, and R. Herzig, “Llarva: Vision-action instruction tuning enhances robot learning,” _arXiv preprint arXiv:2406.11815_ , 2024. 

- [8] W. Song, H. Zhao, P. Ding, C. Cui, S. Lyu, Y. Fan, and D. Wang, “Germ: A generalist robotic model with mixture-of-experts for quadruped robot,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 11 879– 11 886. 

- [9] M. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, and C. Finn, “Openvla: An open-source vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 

- [10] A. O’Neill, A. Rehman, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain, _et al._ , “Open x-embodiment: Robotic learning datasets and rt-x models: Open x- embodiment collaboration 0,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 6892–6903. 

- [11] H.-S. Fang, H. Fang, Z. Tang, J. Liu, C. Wang, J. Wang, H. Zhu, and C. Lu, “Rh20t: A comprehensive robotic dataset for learning diverse skills in one-shot,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 653–660. 

- [12] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, _et al._ , “ _π_ 0: A visionlanguage-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [13] K. Pertsch, K. Stachowicz, B. Ichter, D. Driess, S. Nair, Q. Vuong, O. Mees, C. Finn, and S. Levine, “Fast: Efficient action tokenization for vision-language-action models,” _arXiv preprint arXiv:2501.09747_ , 2025. 

- [14] W. Zhao, P. Ding, M. Zhang, Z. Gong, S. Bai, H. Zhao, and D. Wang, “Vlas: Vision-language-action model with speech instructions for customized robot manipulation,” _International Conference on Learning Representations (ICLR)_ , 2025. 

- [15] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware,” in _Proceedings of Robotics: Science and Systems_ , Daegu, Republic of Korea, July 2023. 

- [16] J. Wen, Y. Zhu, J. Li, M. Zhu, K. Wu, Z. Xu, N. Liu, R. Cheng, C. Shen, Y. Peng, _et al._ , “Tinyvla: Towards fast, data-efficient visionlanguage-action models for robotic manipulation,” _arXiv preprint arXiv:2409.12514_ , 2024. 

- [17] J. Liu, M. Liu, Z. Wang, L. Lee, K. Zhou, P. An, S. Yang, R. Zhang, Y. Guo, and S. Zhang, “Robomamba: Multimodal state space model for efficient robot reasoning and manipulation,” _arXiv preprint arXiv:2406.04339_ , 2024. 

- [18] S. Park, H. Kim, W. Jeon, J. Yang, B. Jeon, Y. Oh, and J. Choi, “Quantization-aware imitation-learning for resource-efficient robotic control,” _arXiv preprint arXiv:2412.01034_ , 2024. 

- [19] Y. Yue, Y. Wang, B. Kang, Y. Han, S. Wang, S. Song, J. Feng, and G. Huang, “Deer-vla: Dynamic inference of multimodal large language models for efficient robot execution,” in _The Thirty-eighth Annual Conference on Neural Information Processing Systems_ , 2024. 

- [20] Y. Zhang, C.-K. Fan, J. Ma, W. Zheng, T. Huang, K. Cheng, D. Gudovskiy, T. Okuno, Y. Nakata, K. Keutzer, _et al._ , “Sparsevlm: Visual token sparsification for efficient vision-language model inference,” _arXiv preprint arXiv:2410.04417_ , 2024. 

- [21] L. Chen, H. Zhao, T. Liu, S. Bai, J. Lin, C. Zhou, and B. Chang, “An image is worth 1/2 tokens after layer 2: Plug-and-play inference acceleration for large vision-language models,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 19–35. 

- [22] S. Xu, Y. Wang, C. Xia, D. Zhu, T. Huang, and C. Xu, “Vlacache: Towards efficient vision-language-action model via adaptive token caching in robotic manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2502.02175 

- [23] J. M. Ortega and W. C. Rheinboldt, _Iterative solution of nonlinear equations in several variables_ . SIAM, 2000. 

- [24] P. Ding, H. Zhao, W. Zhang, W. Song, M. Zhang, S. Huang, N. Yang, and D. Wang, “Quar-vla: Vision-language-action model for quadruped robots,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 352–367. 

- [25] X. Li, M. Liu, H. Zhang, C. Yu, J. Xu, H. Wu, C. Cheang, Y. Jing, W. Zhang, H. Liu, _et al._ , “Vision-language foundation models as effective robot imitators,” in _The Twelfth International Conference on Learning Representations_ . 

- [26] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” _The International Journal of Robotics Research_ , p. 02783649241273668, 2023. 

- [27] A. Prasad, K. Lin, J. Wu, L. Zhou, and J. Bohg, “Consistency policy: Accelerated visuomotor policies via consistency distillation,” _Robotics: Science and Systems_ , 2024. 

- [28] M. Janner, Y. Du, J. B. Tenenbaum, and S. Levine, “Planning with diffusion for flexible behavior synthesis,” _arXiv preprint arXiv:2205.09991_ , 2022. 

- [29] S. Lee, Y. Wang, H. Etukuru, H. J. Kim, N. M. M. Shafiullah, and L. Pinto, “Behavior generation with latent actions,” _arXiv preprint arXiv:2403.03181_ , 2024. 

- [30] Y. Liu, J. I. Hamid, A. Xie, Y. Lee, M. Du, and C. Finn, “Bidirectional decoding: Improving action chunking via closed-loop resampling,” _ArXiv_ , 2024. 

- [31] J. Lin, J. Tang, H. Tang, S. Yang, W.-M. Chen, W.-C. Wang, G. Xiao, X. Dang, C. Gan, and S. Han, “Awq: Activation-aware weight quantization for on-device llm compression and acceleration,” _Proceedings of Machine Learning and Systems_ , vol. 6, pp. 87–100, 2024. 

- [32] H. Liu, C. Li, Q. Wu, _et al._ , “Visual instruction tuning,” 2023. [Online]. Available: https://arxiv.org/abs/2304.08485 

- [33] A. Santilli, S. Severino, E. Postolache, V. Maiorca, M. Mancusi, R. Marin, and E. Rodola, “Accelerating transformer inference for translation via parallel decoding,” in _Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (ACL)_ , 2023, pp. 12 336–12 355. 

- [34] S. Kou, L. Hu, Z. He, Z. Deng, and H. Zhang, “Cllms: Consistency large language models,” in _Forty-first International Conference on Machine Learning_ , 2024. 

- [35] O. Mees, L. Hermann, E. Rosete-Beas, and W. Burgard, “Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks,” _IEEE Robotics and Automation Letters_ , 2021. 

- [36] O. Mees, L. Hermann, and W. Burgard, “What matters in language conditioned robotic imitation learning over unstructured data,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 4, pp. 11 205–11 212, 2022. 

- [37] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong, _et al._ , “Openvla: An open-source vision-language-action model,” in _8th Annual Conference on Robot Learning_ . 

- [38] D. Qu, H. Song, Q. Chen, Y. Yao, X. Ye, Y. Ding, Z. Wang, J. Gu, B. Zhao, D. Wang, _et al._ , “Spatialvla: Exploring spatial representations for visual-language-action model,” _arXiv preprint arXiv:2501.15830_ , 2025. 

- [39] Q. Zhao, Y. Lu, M. J. Kim, Z. Fu, Z. Zhang, Y. Wu, Z. Li, Q. Ma, S. Han, C. Finn, _et al._ , “Cot-vla: Visual chain-of-thought reasoning for vision-language-action models,” pp. 1702–1713, 2025. 

- [40] J. Cen, C. Yu, H. Yuan, Y. Jiang, S. Huang, J. Guo, X. Li, Y. Song, H. Luo, F. Wang, _et al._ , “Worldvla: Towards autoregressive action world model,” _arXiv preprint arXiv:2506.21539_ , 2025. 

- [41] C.-P. Huang, Y.-H. Wu, M.-H. Chen, Y.-C. F. Wang, and F.-E. Yang, “Thinkact: Vision-language-action reasoning via reinforced visual latent planning,” _arXiv preprint arXiv:2507.16815_ , 2025. 

- [42] K. Pertsch, K. Stachowicz, B. Ichter, D. Driess, S. Nair, Q. Vuong, O. Mees, C. Finn, and S. Levine, “Fast: Efficient action tokenization for vision-language-action models,” _arXiv preprint arXiv:2501.09747_ , 2025. 

- [43] J. Lee, J. Duan, H. Fang, Y. Deng, S. Liu, B. Li, B. Fang, J. Zhang, Y. R. Wang, S. Lee, _et al._ , “Molmoact: Action reasoning models that can reason in space,” _arXiv preprint arXiv:2508.07917_ , 2025. 

- [44] Z. Zhong, H. Yan, J. Li, X. Liu, X. Gong, W. Song, J. Chen, and H. Li, “Flowvla: Thinking in motion with a visual chain of thought,” _arXiv preprint arXiv:2508.18269_ , 2025. 

- [45] W. Zhang, H. Liu, Z. Qi, Y. Wang, X. Yu, J. Zhang, R. Dong, J. He, H. Wang, Z. Zhang, _et al._ , “Dreamvla: a vision-language-action model dreamed with comprehensive world knowledge,” _arXiv preprint arXiv:2507.04447_ , 2025. 

- [46] E. Coumans and Y. Bai, “Pybullet, a python module for physics simulation for games, robotics and machine learning,” http://pybullet.org, 2016–2019. 

- [47] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “Libero: Benchmarking knowledge transfer for lifelong robot learning,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 44 776–44 791, 2023. 

- [48] W.-L. Chiang, Z. Li, Z. Lin, Y. Sheng, Z. Wu, H. Zhang, L. Zheng, S. Zhuang, Y. Zhuang, J. E. Gonzalez, I. Stoica, and E. P. Xing, “Vicuna: An open-source chatbot impressing gpt-4 with 90%* chatgpt quality,” March 2023. [Online]. Available: https://lmsys.org/blog/2023-03-30-vicuna/ 

- [49] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark, _et al._ , “Learning transferable visual models from natural language supervision,” in _International conference on machine learning_ . PmLR, 2021, pp. 8748–8763. 

- [50] M. J. Kim, C. Finn, and P. Liang, “Fine-tuning vision-languageaction models: Optimizing speed and success,” _arXiv preprint arXiv:2502.19645_ , 2025. 

