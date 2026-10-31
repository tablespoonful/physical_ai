---
title: "EmbodieDreamer: Advancing Real2Sim2Real Transfer for Policy Training via Embodied World Modeling"
date: "2025-07-07"
authors: "Boyuan Wang; Xinpan Meng; Xiaofeng Wang; Zheng Zhu; Angen Ye; Yang Wang"
url: https://arxiv.org/abs/2507.05198
pdf: https://arxiv.org/pdf/2507.05198
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2507.05198)** / [論文ページ](https://arxiv.org/abs/2507.05198)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **EmbodieDreamer: Advancing Real2Sim2Real Transfer for Policy Training via Embodied World Modeling** 

**Boyuan Wang**<sup>1, 2</sup><sup>_∗_</sup> **, Xinpan Meng**<sup>1, 2</sup><sup>_∗_</sup> **, Xiaofeng Wang**<sup>1, 2</sup><sup>_∗_</sup> **, Zheng Zhu**<sup>1</sup><sup>_∗†_</sup> **, Angen Ye**<sup>1, 2</sup> , **Yang Wang**<sup>1</sup> , **Zhiqin Yang**<sup>1</sup> , **Chaojun Ni**<sup>1,3</sup> , **Guan Huang**<sup>1</sup> , **Xingang Wang**<sup>2</sup><sup>_†_</sup> 1GigaAI 2Institute of Automation, Chinese Academy of Sciences 3Peking University `https://embodiedreamer.github.io/` 

## **Abstract** 

The rapid advancement of Embodied AI has led to an increasing demand for large-scale, high-quality real-world data. However, collecting such embodied data remains costly and inefficient. As a result, simulation environments have become a crucial surrogate for training robot policies. Yet, the significant Real2Sim2Real gap remains a critical bottleneck, particularly in terms of physical dynamics and visual appearance. To address this challenge, we propose _EmbodieDreamer_ , a novel framework that reduces the Real2Sim2Real gap from both the physics and appearance perspectives. Specifically, we propose _PhysAligner_ , a differentiable physics module designed to reduce the Real2Sim physical gap. It jointly optimizes robot-specific parameters such as control gains and friction coefficients to better align simulated dynamics with real-world observations. In addition, we introduce _VisAligner_ , which incorporates a conditional video diffusion model to bridge the Sim2Real appearance gap by translating low-fidelity simulated renderings into photorealistic videos conditioned on simulation states, enabling high-fidelity visual transfer. Extensive experiments validate the effectiveness of _EmbodieDreamer_ . The proposed _PhysAligner_ reduces physical parameter estimation error by 3.74% compared to simulated annealing methods while improving optimization speed by 89.91%. Moreover, training robot policies in the generated photorealistic environment leads to a 29.17% improvement in the average task success rate across real-world tasks after reinforcement learning. Code, model and data will be publicly available. 

## **1 Introduction** 

Recent advances in Embodied AI have driven remarkable progress in robot learning, enabling agents to perform complex manipulation, navigation, and decision-making tasks in real-world environments. Central to this progress is the availability of large-scale, high-quality embodied data that captures both the sensory input and motor interaction of agents operating in diverse physical settings. However, collecting such data in the real world is expensive, time-consuming, and often limited in scalability and reproducibility. These limitations motivate the growing reliance on simulation environments [1, 2, 3, 4, 5, 6, 7, 8] as a practical alternative for training and evaluating robotic policies. 

Despite their practical utility, existing simulation environments suffer from the Real2Sim2Real discrepancy. Two key sources of this discrepancy are differences in physical dynamics and visual appearance. First, the physical behaviors simulated in virtual environments often diverge from 

> *These authors contributed equally to this work. 

> †Corresponding authors. zhengzhu@ieee.org, xingang.wang@ia.ac.cn. 

Preprint. Under review. 


Figure 1: _EmbodieDreamer_ is a unified Real2Sim2Real framework that incorporates _PhysAligner_ for rapid physical parameter optimization from real observations and _VisAligner_ for generating visually realistic scenes. Furthermore, _EmbodieDreamer_ supports RL training of policy models through preference learning based on trajectory evaluation, and facilitates IL training by generating diverse, unseen observations. Models trained within _EmbodieDreamer_ show significantly better performance compared to policies fine-tuned on real-world data. 

real-world dynamics due to oversimplified assumptions or unmodeled parameters such as joint stiffness, damping, or arm friction. These mismatches result in inaccurate motion trajectories and undermine the reliability of simulation-based control. Second, the rendered appearance of simulated scenes typically lacks the visual fidelity required to generalize to real-world sensory inputs. As a result, perception models trained in simulation may fail to operate effectively in real environments. Together, these inconsistencies pose significant challenges for deploying policies trained in simulation, especially for tasks demanding precise physical interaction or high-quality visual perception. 

To better align simulation with the real world in both dynamics and appearance, we introduce _EmbodieDreamer_ , a unified framework for improving the fidelity of simulation environments through embodied world modeling. Our approach comprises two complementary components designed to address the Real2Sim2Real discrepancy from both the physical and visual perspectives. First, to mitigate the Real2Sim gap in physical dynamics, we propose _PhysAligner_ , a differentiable physics optimization module that estimates robot-specific parameters such as control gains and friction coefficients. In contrast to the simulated annealing-based optimization used in systems like SimplerEnv [4], _PhysAligner_ leverages gradient-based optimization enabled by differentiable physics to more efficiently and accurately align simulated behaviors with real-world trajectories. Second, to address the Sim2Real discrepancy in visual appearance, we introduce _VisAligner_ , a conditional video diffusion model [9, 10, 11, 12] that synthesizes photorealistic RGB videos from simulation inputs. Unlike prior systems such as Rebot [13], RoboEngine [14], IRASim [15], which primarily modify either the robot or the foreground/background appearance in isolation, _VisAligner_ explicitly disentangles the foreground, background, and robot components. This structured conditioning enables coherent and realistic video generation, making it suitable as a high-fidelity simulation environment for downstream policy learning tasks, including imitation learning [16, 17]and reinforcement learning [18, 19]. 

2 

We conduct extensive experiments to evaluate the effectiveness of _EmbodieDreamer_ . Our results show that _PhysAligner_ significantly improves the alignment between simulated and real-world dynamics, reducing physical parameter estimation error by 3.74% and accelerating optimization by 89.91% compared to simulated annealing baselines. Furthermore, we demonstrate that training policies within the generated photorealistic environment results in a 29.17% improvement in the average real-world task success rate after reinforcement learning, confirming the practical benefits of our approach for robot policy learning. 

Our contribution can be summarized as follows: 

- We propose _EmbodieDreamer_ , a unified framework that advances Real2Sim2Real transfer for policy training by leveraging embodied world modeling to enhance both physical and visual fidelity in simulation environments. 

- We develop _PhysAligner_ , a differentiable physics optimization module designed to reduce the Real2Sim physical gap by accurately estimating robot-specific parameters such as control gains and friction coefficients, thereby aligning simulated dynamics with real-world behavior. 

- We introduce _VisAligner_ , a conditional video diffusion model that bridges the Sim2Real appearance gap by translating low-fidelity simulation renderings into photorealistic videos through disentangled modeling of robot, foreground, and background elements. 

- We conduct extensive experiments across multiple benchmarks to validate the effectiveness of _EmbodieDreamer_ , demonstrating improved parameter estimation accuracy, faster convergence compared to baseline methods, and higher task success rates in both reinforcement learning and imitation learning policy training. 

## **2 Related Work** 

### **2.1 Robot Policy Models** 

In recent years, significant breakthroughs have propelled the field of robotic manipulation policies forward, driven by innovations in Vision-Language-Action (VLA) models [20, 21, 22], diffusionbased frameworks [23, 24], and preference optimization techniques [25, 26]. Chronologically, ACT [27] introduced transformer-based action chunking strategies for robotic manipulation. RT-2 [28] pioneered the integration of large language models into VLA architectures through semantic grounding. Strategies based on diffusion models, including Diffusion Policy [29], RDT-1B [30], DP3 [24], and RDP [31], have showcased their ability to generate multimodal actions, facilitating generalization across tasks, embodiments, and modalities. Robotic policies leveraging large-scale, publicly available dataset pre-trained models, such as OpenVLA [32], Octo [33], and _π_ 0 [20], demonstrate generalizability by fine-tuning on specific tasks, exhibiting impressive transferability across various robotic platforms. GRAPE [26] enhances various VLA architectures through trajectory-level preference optimization, utilizing success/failure trials to improve out-of-distribution generalization while supporting customizable objectives like safety and efficiency. Furthermore, recent developments include layered architectures like DexGraspVLA [34] and the incorporation of chain-of-thought reasoning in Cot-vla [35], which enhance VLA models’ ability to handle complex, long-horizon tasks more effectively. These advances underscore the growing dependence of policy models on high-quality, diverse data and realistic simulation environment to achieve robust and generalizable performance in real-world settings. 

### **2.2 Simulation Environment** 

Effective simulation environments underpin the scalable development and evaluation of both policies and world models. MuJoCo [1] provides highly accurate physics simulations and remains a cornerstone for reinforcement learning. Meanwhile, platforms like RLBench [2] and VLABench [6] emphasize task diversity and parallel data collection, enabling efficient exploration of complex manipulation scenarios. SAPIEN [3] and Genesis [5] leverage GPU acceleration to achieve high-performance rendering and scalable reinforcement learning, significantly improving training throughput for large-scale environments. SimplerEnv [4] , alongside these frameworks, offers a lightweight and extensible collection of manipulation tasks mapped closely to real robot setups, such 

3 

as the WidowX BridgeV2 [36] and Google Robot [37], facilitating rapid iteration and reproducible comparative studies. Furthermore, RoboVerse [7] proposes a unified platform supporting seamless transitions between multiple simulators, allowing hybrid integration to harness complementary strengths across environments. RoboTwin [8] presents a digital-twin framework that aligns twin robot and virtual agent behaviors via 3D generative modeling and large-language-model-driven data augmentation, thereby facilitating high-fidelity sim-to-real transfer on collaborative platforms. Together, these simulation platforms provide the necessary infrastructure for training, validating, and stress-testing advanced control policies and world models, accelerating progress toward robust, generalizable robotic systems. However, current simulation environments still face critical challenges including inaccurate physical parameters, limited visual realism, and significant sim-to-real transfer gaps that degrade policy model performance in real-world deployments. 

### **2.3 Embodied World Models** 

The development of world models has seen significant advancements in recent years, with notable progress reported in [38, 39, 40, 41, 42, 43, 44]. Building on these developments, robot world models aim to provide an internal representation of the environment that supports action simulation and prediction, thereby enhancing the robot’s decision-making and planning capabilities in realworld scenarios. ACDC [45] and UniPi [46] unify affordance prediction and physics forecasting within a single multilingual, multimodal video model, enabling policy learning directly from RGB demonstrations across diverse manipulation benchmarks; subsequently, IRASim [15] leverages generative models to produce highly realistic robot videos from a single initial frame, offering an interactive simulation proxy for real-robot learning. Building on this foundation , RoboDreamer [47] employs self-supervised multi-stage diffusion to decompose natural language commands into primitive actions and synthesize latent videos for combinatorial generalization, while ManipDreamer [48] enhances this framework by incorporating hierarchical action trees and semantic visual adapters to strengthen instruction relationships and improve temporal and visual consistency. RoboTransfer [49] introduces a diffusion-based video generation framework that enables geometry-consistent multi-view video synthesis with fine-grained control over scene components, bridging the sim-to-real gap through explicit 3D priors and cross-view conditioning. With advancements in 3D reconstruction methods [50, 51], several studies [42, 44, 12, 52, 53, 54, 55, 56] have leveraged these techniques to bridge the reality gap in various fields, including robotics. Robo-GS [57] presents a differentiable Real2Sim pipeline that integrates mesh geometry with 3D Gaussian splattings (3DGS) [50] for high-fidelity digital asset reconstruction, ReBot [13] expands visual-language-action datasets via realto-sim-to-real trajectory replay and background inpainting, and SplatSim [58] adopts 3DGS instead of traditional mesh rendering to generate photorealistic synthetic data that significantly narrows the sim-to-real gap. 

## **3 Method** 

### **3.1 Framework Overview** 

We present _EmbodieDreamer_ , a robot policy enhancement framework that integrates two core components: _PhysAligner_ and _VisAligner_ . This framework effectively reduces the Real2Sim2Real gap in both physical dynamics and visual appearance. As illustrated in Figure 2, _PhysAligner_ consists of a differentiable network for optimizing physical parameters, enabling the simulator to better approximate real-world dynamics. _VisAligner_ leverages a video diffusion model to translate simulated renderings into more realistic visual observations, which are then fed into the robot policy model to generate actions that drive the simulator. Through this pipeline, _EmbodieDreamer_ functions as a realistic and adaptable simulation environment for robot policy training, supporting both imitation learning and reinforcement learning paradigms. 

### **3.2 PhysAligner** 

Under Real2Sim settings, a physical gap inevitably exists between the simulated and real-world dynamics. When applying identical action signals to both the simulator and the physical robot, our objective is to minimize the control discrepancy between the two domains. Ideally, open-loop execution of motion sequences in the simulator should yield trajectories that closely match those observed in the real world. However, achieving this alignment requires accurate specification of 

4 


Figure 2: _EmbodieDreamer_ framework integrates _PhysAligner_ and _VisAligner_ to reduce the Real2Sim2Real gap in physics and appearance. _PhysAligner_ optimizes simulator dynamics, while _VisAligner_ translates simulated renderings into realistic observations for robot policy training. 


Figure 3: The figure illustrates the workflow of _PhysAligner_ . First, a large amount of data is generated using a simulator. Then, a surrogate model is trained to fit the data. Finally, the physical parameters are optimized through gradient descent. 

system parameters, such as control gains, which are often determined empirically or through extensive trial and error. 

SimplerEnv [4] employs simulated annealing to optimize these parameters, while conceptually effective, this stochastic search method entails high computational cost and frequently suffers from slow or unstable convergence. To address these limitations, we propose a more efficient framework based on differentiable, learning-driven optimization. This approach enables gradient-based parameter estimation and greatly enhances both convergence speed and stability. 

As shown in Figure 3, the system identification pipeline consists of three sequential stages: 

**Simulation Dataset Generation.** We use ( _f, p, d_ ) to denote the friction, stiffness, and damping coefficients in the simulator. At time step _t −_ 1, the action sequence _at−_ 1 and corresponding state _St−_ 1, which includes camera observation and proprioception, are extracted from real-world collected data. We then randomly sample multiple ( _f, p, d_ ) pairs. The simulator executes the given action _at−_ 1 under the initial state condition _St−_ 1, and acquires the next state: 


**Surrogate Modeling.** Next, we construct a surrogate model _Mf,p,d_ to learn the relationship between physical parameters and system state transitions. The model takes as input the physical parameters, actions, and states from the generated simulation dataset, and produces the following prediction: 


The model is trained by minimizing the mean-squared error between predicted and simulated trajectories, thereby constructing a differentiable approximation of the simulator’s non-smooth dynamics: 


5 

**Gradient-based Refinement.** Finally, the surrogate model is used to refine the physical parameters via gradient descent. With the network weights fixed, the ( _f, p, d_ ) parameters are iteratively updated to minimize the following loss function: 


This iterative process continues until the simulated output aligns closely with the observed trajectories, yielding an optimized set of PD controller parameters ( _f_<sup>_∗_</sup> _, p_<sup>_∗_</sup> _, d_<sup>_∗_</sup> ) that best reproduce real-world dynamics. More details about loss function are provided in Appendix 1. 

### **3.3 VisAligner** 

To address the appearance gap in Sim2Real transfer, we employ a video generation framework and propose _VisAligner_ to achieve appearance transfer, as illustrated in Figure 4. Given a manually collected episode _e_ of length _f_ , we denote the joint positions and actions as _q, a ∈_ R<sup>_f×_14</sup> , and the ground-truth video captured by the camera as _V_ gt _∈_ R<sup>_f×H×W ×c_</sup> _._ 


Figure 4: The framework of _VisAligner_ . A reference image containing the initial background and robot appearance information serves as the first frame of the conditioned video. The subsequent frames are generated by performing pixel-wise addition of the robot’s motion observations from the simulated environment and the segmentation masks of the foreground objects. These frames are then encoded into latents via a VAE encoder [59], concatenated with noise along the channel dimension, and input to _VisAligner_ for denoising. Spatial-temporal attention mechanisms are employed to capture long-range dependencies across both spatial and temporal dimensions, thereby enhancing the coherence and visual quality of the generated video. The final video is obtained by decoding the denoised latents. 

We construct a training batch _{_ ( _q_<sup>(</sup><sup>_i_)</sup> _, a_<sup>(</sup><sup>_i_)</sup> _, V_ gt<sup>(</sup><sup>_i_))</sup><sup>_}_</sup> _i_<sup>_N_</sup> =1<sup>to optimize</sup><sup>_VisAligner_.For the conditioning</sup> inputs, we decompose control into three components: the robot, the foreground object, and the background. 

First, for the robot, we utilize its URDF model _ur_ and replay the joint trajectories _q_ in the simulator: 


where the virtual camera parameters are manually calibrated to align the simulated manipulator with its real-world counterpart. 

Second, for the foreground object, we apply GroundSAM [60, 61] to segment the object and obtain a binary mask seg. This mask is added to the original observation image obs _r_ in a pixel-wise manner to generate the simulation condition signal csim. Third, as the camera remains static, the background is invariant. Therefore, a single reference image _Ir ∈_ R<sup>_H×W ×c_</sup> is used as the background control 

6 

signal. During training, the conditioning sequence for a video consisting of _f_ frames is formed by concatenating _Ir_ with the last _f −_ 1 frames of csim, denoted as: Condition = [ _Ir,_ c<sup>_t_</sup> sim<sup>1</sup><sup>_, ...,_c</sup><sup>_t_</sup> sim<sup>_f−_1].</sup> We adopt a latent video diffusion model [9] as the backbone. Specifically, the conditional simulation frames condsim and the ground-truth video _V_ gt are each encoded via a Variational Autoencoder (VAE) [59] encoder _ε_ ( _·_ ), resulting in latent representations _y_ c _, z_ 0 _∈_ R<sup>_f×h×w×c_</sup> _._ At diffusion timestep _t_ , the concatenated latent _z_ is corrupted as: 


where _{αt}_<sup>_T_</sup> _t_ =1<sup>is a predefined noise schedule follow [9].The denoising network</sup><sup>_ϵθ_is optimized by</sup> minimizing the following loss: 


This objective encourages the network to predict _z_ 0, enabling faithful reconstruction of the video. Empirically, conditioning on both the simulated mask and real video latents leads to significant improvements in visual consistency and appearance alignment across frames. 

## **4 Experiments** 

We utilize the Cobot Mobile ALOHA, a robotic platform grounded in the Mobile ALOHA system design [62], produced by AgileX.AI, to support manual data collection and testing. For each task, 50 episodes are collected. We conduct a series of experiments including evaluation of system identification performance, quantitative assessment of generation quality, training of the policy model with both reinforcement learning and imitation learning, and finally, evaluation of task success rates on the real robot. 

### **4.1 Quantity result Comparison of** **_PhysAligner_** 

**Experimental Setup.** We conduct experiments on 20 randomly selected episodes from the RT-1 dataset [37]. Our method trains a three-layer multilayer perceptron (MLP) as a surrogate model to approximate the system dynamics, taking physical parameters—including stiffness, damping, and friction—as input. In contrast to the baseline SimplerEnv [4], which employs 400 simulated annealing steps to optimize PD gains, we randomly sample 50 parameter sets for initial training and subsequently refine the MLP via gradient descent with a learning rate of 0.001. All other configurations, including data normalization, are kept consistent to ensure a fair comparison. Performance is evaluated using the mean squared error (MSE) between the predicted and ground-truth end-effector trajectories, and we additionally report the total computation time for data preparation and parameter optimization. 

**Experimental Results.** As shown in Table 1, _PhysAligner_ achieves a lower overall trajectory error, compared to the baseline SimplerEnv, mainly due to a significant reduction in rotation error. Although translation error slightly increases, the method demonstrates approximately 10× speedup in total computation time, reducing optimization from over 12,800 seconds to around 1,300 seconds. 

These results highlight that the differentiable surrogate model effectively approximates system dynamics with minimal accuracy loss, achieving a better trade-off between estimation performance and computational efficiency. This makes the proposed method more suitable for practical system identification tasks. 

Table 1: Performance comparison with the SimplerEnv on system identification tasks. 

|Method|Trajectory error|Rotation error|Translation error|Time cost(s)|
|---|---|---|---|---|
|SimplerEnv|0.2245|0.1282|0.0963|12888.43|
|_PhysAligner_(Ours)|**0.2161**|**0.1101**|**0.1060**|**1299.92**|


7 

### **4.2 Video Generation Quality Comparison of VisAligner** 

**Experimental Setup.** We conduct experiments on the RT-1 dataset [37], where we randomly split the data into a training set of 4,762 samples and a test set of 100 samples. Our model, _VisAligner_ , is built upon the SVD [9] with latent feature channels set to _c_ = 4. The input resolution is fixed at 640 _×_ 480, with a video length of 25 frames. 

To evaluate the impact of object mask conditioning on video generation quality, we perform ablation studies by comparing models trained with and without object segmentation inputs. We use standard image and video similarity metrics——FVD [63] , PSNR, SSIM and LPIPS [64] ——to quantitatively assess the fidelity and temporal coherence of the generated videos. 

**Experimental Results.** The results, summarized in Table 2, clearly demonstrate the effectiveness of our approach in generating high-quality videos when incorporating object mask information as a condition. 

Table 2: Generation quality comparison. 

|Method|FVD_↓_|PSNR_↑_|SSIM_↑_|LPIPS_↓_|
|---|---|---|---|---|
|w/o object segmentation|422.73|23.067|0.7939|0.0713|
|_EmbodieDreamer_(ours)|**176.27**|**24.518**|**0.821**|**0.0554**|


Figure 5: The visualization comparison of whether foreground object segmentation is used as a conditioning input. The four rows show: (1) Ground Truth (GT), (2) generated without segmentation condition, (3) segmentation map used as condition, and (4) generated result with segmentation condition. 

The visualization comparison in Figure 5 demonstrates that models without object segmentation exhibit deformation or disappearance of target objects during grasping, while segmentation-conditioned outputs maintain structural integrity and pose consistency. 

### **4.3 RL with EmbodieDreamer** 

**Experimental Setup.** We adopt the supervised fine-tuning (SFT) of the ACT model [65] as our baseline, where each task is trained with 50 demonstrations over 1000 epochs. The ACT model takes either three-view or one-view visual observations combined with joint position information as input, and generates action sequences of fixed length _T_ . In our experiments, _T_ is set to 100. 

For the reinforcement learning phase, the ACT policy receives one-view visual input to produce actions, which are executed in the simulator to generate raw observations. These observations are 

8 

then processed by _VisAligner_ to render photorealistic videos. The last frame of the rendered video serves as the reference image for the next iteration of policy execution. This closed-loop process iterates for a fixed number of steps, yielding trajectories of consistent length with photorealistic visual observations. Two representative trajectories generated by _EmbodieDreamer_ are visualized in Figure 6. 

Using this framework, we batch-generate trajectories and apply a preference-based ranking strategy adapted from [26]. The reward metric is defined as the Euclidean distance between the end-effector and the target position at the terminal state of each trajectory. Based on these reward scores, we select the top- _M_ and bottom- _M_ trajectories as positive and negative samples, respectively. Each fine-tuning cycle trains the ACT model on these _M_ sample pairs for 80 epochs, with the updated policy generating new trajectories for subsequent iterations. We set _M_ = 25 in all experiments. More details are provided in the Appendix 2. 

We adopt experiments on 4 tasks. Task 1: Grab Paper Cup — success defined as grasping a randomly placed cup. Tasks 2–4 follow a unified structure: (1) _Grasp success_ requires picking up the target object (pen, remote, cup), and (2) _Task success_ demands precise placement (pen in holder, remote/box, cup/mat), all with randomly positioned objects and targets. 

**Experimental Results.** We select four tasks and evaluate their success rates on the real robot system, as shown in Figure 7, and the result is shown in Table 3. The experimental results demonstrate that the SFT model performs better with three views compared to a single view. After training with RL, the performance of the single-view model achieves the best results. 


Figure 6: Visualization of two distinct trajectories generated by the policy model from a shared initial frame, after being rendered using _VisAligner_ . Despite originating from the same starting image, the trajectories lead to different simulation states due to variations in action sequences. Thanks to the accurate robot positioning in the simulated environment, the resulting photorealistic observations can be effectively used for further policy inference. 

### **4.4 IL with EmbodieDreamer** 

**Experimental Setup.** In addition to its applicability in reinforcement learning, _EmbodieDreamer_ can also be effectively employed for imitation learning. We observe that variations in the texture of foreground objects and environmental backgrounds can lead to a noticeable decline in model performance, indicating a certain level of sensitivity to visual appearance changes. To address this issue,We employ _EmbodieDreamer_ to generate augmented training data with modified object appearances and environmental conditions, eliminating the need for physical scene configurations or real-world data acquisition. Imitation learning is then applied to train the policy model. 

9 


Figure 7: Definition and visualization of the three tasks. Each task is divided into two stages, with success rates reported separately for "grasp success" and "task success". For the _Put Cup on Mat_ task, a trial is counted as successful only if the cup is fully placed on the mat. 

Table 3: We report the success rates of an ACT-based policy across four tasks, under different training settings: (1) trained from scratch with supervised fine-tuning (SFT), (2) without pre-training, and (3) with reinforcement learning (RL) training. The term "with three views" refers to using camera inputs from three angles: the head camera and the wrist cameras on the left and right arms. When reducing the number of views from 3 to 1, a performance drop is observed. However, by incorporating RL training with _EmbodieDreamer_ (continuing training from a single view SFT checkpoint), our method achieves superior results compared to other baselines. 

|Method|Grab Paper Cup|Put Pen|in Cup|Put Remo|te in Box|Put Cup|on Mat||
|---|---|---|---|---|---|---|---|---|
||Task Suc|Grasp Suc|Task Suc|Grasp Suc|Task Suc|Grasp Suc|Task Suc|Avg|
|SFT with three views|0.7|0.5|0.5|0.7|**0.7**|0.6|0.5|0.60|
|SFT with one view|0.5|0.5|0.2|0.6|0.6|0.6|0.4|0.49|
|RL with_EmbodieDreamer_|**0.9**|**0.7**|**0.7**|**0.8**|**0.8**|**0.8**|**0.7**|**0.77**|


Specifically, we utilize Gemini-2.0-Flash-Preview-Image-Generation [66] to modify the foreground and background content of reference images for each episode in the real-robot data (e.g., randomly placing an A4 white paper on the table or altering the color of cups). By replaying the actions from each frame of the original data, we obtain simulated observations under these modified conditions. _EmbodieDreamer_ subsequently generates videos under these new conditions, and finally translates these simulated episodes into realistic visual demonstrations, resulting in a set of high-quality, diverse demonstrations by Sim2Real transfer. 

To demonstrate the effectiveness of data-augmented imitation learning, we compare three policy configurations: 

- Model 1: Trained on real data (from scratch, only white cup and no A4 paper) 

- Model 2: Trained on generated data (from scratch) 

- Model 3: Trained on generated data (resume from Model1) 

For background variation, the evaluation includes 50 episodes each from both generated and real data sources. For foreground variation, 50 episodes are taken from real data and 20 from generated data. 

**Experimental Results.** We conduct 30 test trials for each task setting, and the success rates are summarized in Table 4. The results show that the use of generated data leads to an improvement in success rate on new scenes, demonstrating the effectiveness of our generated data in facilitating policy transfer. Additionally, we perform post-training on the provided pretrained model _π_ 0 [20] and test its success rate, as shown in Table 5. The results further validate the utility of the generated data. 

10 

Table 4: Success rate comparison of ACT-based policy trained with different data configurations. 

|Data Source|Train Method|Origin|Change Foreground|Origin|Change Ba|ckground|
|---|---|---|---|---|---|---|
|||White Cup|Blue Cup|No A4|A4 paper(horizontal)|A4 paper(vertical)|
|Real data|scratch|**0.467**|0.333|**0.467**|0.300|0.167|
|Generated data|scratch|0.033|0.100|0.067|0.567|0.500|
|Generated data|resume|0.133|**0.433**|0.133|**0.700**|**0.600**|


Table 5: Success rate comparison of _π_ 0 trained with different data configurations. 

|Data Source|Origin|Change Foreground|Origin|Change Ba|ckground|
|---|---|---|---|---|---|
||White Cup|Blue Cup|No A4|A4 paper(horizontal)|A4 paper(vertical)|
|Real data|**0.600**|0.533|**0.600**|0.500|0.433|
|Generated data|0.433|**0.633**|0.433|**0.567**|**0.600**|


## **5 Conclusion** 

This work presents _EmbodieDreamer_ , a novel framework addressing the critical Real2Sim2Real gap in Embodied AI by synergistically bridging discrepancies in physical dynamics and visual appearance. Through the proposed _PhysAligner_ , we achieve precise alignment of simulated physics with real-world dynamics via differentiable optimization of robot-specific parameters, significantly outperforming conventional methods in both accuracy and efficiency. Concurrently, _VisAligner_ leverages conditional video diffusion to synthesize photorealistic environments from low-fidelity simulations, enabling effective visual transfer for policy learning. Experimental results demonstrate that our framework not only reduces physical parameter estimation errors and accelerates optimization but also enhances real-world task success rates through high-fidelity visual rendering. By unifying physics-aware and vision-centric adaptation, _EmbodieDreamer_ advances the deployment of simulation-trained policies into real-world scenarios, paving the way for scalable and efficient embodied intelligence development. Future work will explore extending this paradigm to multi-modal sensory integration and long-horizon autonomous tasks. 

**Limitations.** Our current approach has several limitations. First, as a diffusion-based model, the generation of high-quality photorealistic videos is computationally expensive, often taking around two minutes per sequence. While this limitation can be mitigated with faster sampling techniques or network architectures, it still poses challenges for real-time applications. Second, the accuracy of our physics-aware simulation relies heavily on the fidelity of the underlying simulator in modeling real-world dynamics, which may limit generalization to more complex or unstructured environments. 

11 

In the appendix, we provide more details about _PhysAligner_ and present a detailed description of the reinforcement learning procedure with _EmbodieDreamer_ . 

## **1 More Details of PhysAligner** 

We define the trajectory loss as 


where _f_ denotes the input visual observation, _p_ represents the ground-truth end-effector pose sequence, and _d_ indicates the diffusion model used for trajectory generation. The loss function jointly optimizes two components: 

**Translation Loss** _L_ trans: For each time step _i ∈{_ 1 _,_ 2 _, . . . , T }_ , we compute the Euclidean distance between the predicted position **x**<sup>_′_</sup> _i_<sup>_∈_R3 and the ground-truth position</sup><sup>**x**</sup><sup>_i∈_R3 of the end-effector:</sup> 


**Rotation Loss** _L_ rot: To measure rotational discrepancies, we calculate the Frobenius norm of the difference between the ground-truth rotation matrix **R** _i ∈ SO_ (3) and the predicted rotation matrix **R**<sup>_′_</sup> _i_<sup>_∈SO_(3), normalized by a geometric scaling factor 2</sup> _~~√~~_ 2. The arcsine transformation maps this matrix discrepancy to an angular error in radians: 


This formulation explicitly models both translational and rotational errors of the end-effector pose ( **x** _i,_ **R** _i_ ), ensuring geometric consistency between the simulated trajectory and real-world demonstrations. The 2 _~~√~~_ 2 normalization factor arises from the maximum possible Frobenius norm of **R** _i −_ **R**<sup>_′_</sup> _i_<sup>,</sup> derived from the properties of orthogonal matrices in _SO_ (3). 

## **2 RL Formulation and TPO Loss Adaptation** 

To optimize ACT beyond supervised learning, we employ reinforcement learning, following prior work on vision-language alignment [67, 68]. We formulate the objective as: 


where _π_ ref denotes a supervised-trained reference policy, and _β_ controls deviation regularization. This form mirrors the KL-regularized RL objective while allowing simplified implementation in trajectory space. 

To optimize this objective using trajectory-level preference signals, we follow the principle of Trajectory Preference Optimization (TPO) [26], adapting the loss to our discrete-action scenario. For a pair of trajectories ( _ζw, ζl_ ) denoting preferred and less-preferred samples, the loss is: 


where ∆( _ζw, ζl_ ) represents the log-probability advantage: 


Assuming a Markovian structure, the log-probability of a trajectory decomposes as: 

12 


While the standard trajectory likelihood _πθ_ ( _ζ_ ) can be computed exactly in continuous-action models, it becomes impractical in our discrete-action ACT setting. Instead, we propose a tractable formulation tailored to ACT, where the log-likelihood of a trajectory is computed via squared prediction errors: 


where ˆ _at_ denotes the predicted action at step _t_ and _at_ is the corresponding ground-truth action. This formulation assumes a Gaussian likelihood over discrete action embeddings and reflects the model’s trajectory-level confidence. 

Using this definition of log-likelihood, the TPO loss becomes: 


This formulation enables stable and efficient preference-based training without requiring explicit probability computation over discrete outputs. To construct the dataset _D_ , we sample trajectories from a single-view ACT-based policy. These trajectories are ranked using a cost function, and based on their rankings, we categorize them into chosen ( _ζw_ ) and rejected ( _ζl_ ) sets. The TPO loss is computed using these paired trajectories, enabling the policy to learn from preference-aligned data. 

13 

## **References** 

- [1] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 5026–5033. IEEE, 2012. 1, 3 

- [2] Stephen James, Zicong Ma, David Rovick Arrojo, and Andrew J. Davison. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ , 2020. 1, 3 

- [3] Fanbo Xiang, Yuzhe Qin, Kaichun Mo, Yikuan Xia, Hao Zhu, Fangchen Liu, Minghua Liu, Hanxiao Jiang, Yifu Yuan, He Wang, Li Yi, Angel X. Chang, Leonidas J. Guibas, and Hao Su. SAPIEN: A simulated part-based interactive environment. In _The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , June 2020. 1, 3 

- [4] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, Sergey Levine, Jiajun Wu, Chelsea Finn, Hao Su, Quan Vuong, and Ted Xiao. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 1, 2, 3, 5, 7 

- [5] Genesis Authors. Genesis: A universal and generative physics engine for robotics and beyond, December 2024. 1, 3 

- [6] Shiduo Zhang, Zhe Xu, Peiju Liu, Xiaopeng Yu, Yuan Li, Qinghui Gao, Zhaoye Fei, Zhangyue Yin, Zuxuan Wu, Yu-Gang Jiang, and Xipeng Qiu. Vlabench: A large-scale benchmark for language-conditioned robotics manipulation with long-horizon reasoning tasks, 2024. 1, 3 

- [7] Haoran Geng, Feishi Wang, Songlin Wei, Yuyang Li, Bangjun Wang, Boshi An, Charlie Tianyue Cheng, Haozhe Lou, Peihao Li, Yen-Jen Wang, Yutong Liang, Dylan Goetting, Chaoyi Xu, Haozhe Chen, Yuxi Qian, Yiran Geng, Jiageng Mao, Weikang Wan, Mingtong Zhang, Jiangran Lyu, Siheng Zhao, Jiazhao Zhang, Jialiang Zhang, Chengyang Zhao, Haoran Lu, Yufei Ding, Ran Gong, Yuran Wang, Yuxuan Kuang, Ruihai Wu, Baoxiong Jia, Carlo Sferrazza, Hao Dong, Siyuan Huang, Yue Wang, Jitendra Malik, and Pieter Abbeel. Roboverse: Towards a unified platform, dataset and benchmark for scalable and generalizable robot learning, April 2025. 1, 4 

- [8] Yao Mu, Tianxing Chen, Zanxin Chen, Shijia Peng, Zhiqian Lan, Zeyu Gao, Zhixuan Liang, Qiaojun Yu, Yude Zou, Mingkun Xu, et al. Robotwin: Dual-arm robot benchmark with generative digital twins. _arXiv preprint arXiv:2504.13059_ , 2025. 1, 4 

- [9] Andreas Blattmann, Tim Dockhorn, Sumith Kulal, Daniel Mendelevitch, Maciej Kilian, Dominik Lorenz, Yam Levi, Zion English, Vikram Voleti, Adam Letts, et al. Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint arXiv:2311.15127_ , 2023. 2, 7, 8 

- [10] Wenyi Hong, Ming Ding, Wendi Zheng, Xinghan Liu, and Jie Tang. Cogvideo: Large-scale pretraining for text-to-video generation via transformers. _arXiv preprint arXiv:2205.15868_ , 2022. 2 

- [11] Boyuan Wang, Xiaofeng Wang, Chaojun Ni, Guosheng Zhao, Zhiqin Yang, Zheng Zhu, Muyang Zhang, Yukun Zhou, Xinze Chen, Guan Huang, Lihong Liu, and Xingang Wang. Humandreamer: Generating controllable human-motion videos via decoupled generation. _arXiv preprint arXiv:2503.24026_ , 2025. 2 

- [12] Boyuan Wang, Runqi Ouyang, Xiaofeng Wang, Zheng Zhu, Guosheng Zhao, Chaojun Ni, Guan Huang, Lihong Liu, and Xingang Wang. Humandreamer-x: Photorealistic single-image human avatars reconstruction via gaussian restoration. _arXiv preprint arXiv:2504.03536_ , 2025. 2, 4 

- [13] Yu Fang, Yue Yang, Xinghao Zhu, Kaiyuan Zheng, Gedas Bertasius, Daniel Szafir, and Mingyu Ding. Rebot: Scaling robot learning with real-to-sim-to-real robotic video synthesis, 2025. 2, 4 

- [14] Chengbo Yuan, Suraj Joshi, Shaoting Zhu, Hang Su, Hang Zhao, and Yang Gao. Roboengine: Plug-and-play robot data augmentation with semantic robot segmentation and background generation. _arXiv preprint arXiv:2503.18738_ , 2025. 2 

14 

- [15] Fangqi Zhu, Hongtao Wu, Song Guo, Yuxiao Liu, Chilam Cheang, and Tao Kong. Irasim: Learning interactive real-robot action simulators. _arXiv:2406.12802_ , 2024. 2, 4 

- [16] Dongchi Huang, Tianle Zhang, Yihang Li, Ling Zhao, Jiayi Li, Zhirui Fang, Chunhe Xia, Lusong Li, and Xiaodong He. Dexterous hand manipulation via efficient imitation-bootstrapped online reinforcement learning. _arXiv preprint arXiv:2503.04014_ , 2025. 2 

- [17] Maryam Zare, Parham M Kebria, Abbas Khosravi, and Saeid Nahavandi. A survey of imitation learning: Algorithms, recent developments, and challenges. _IEEE Transactions on Cybernetics_ , 2024. 2 

- [18] Chen Tang, Ben Abbatematteo, Jiaheng Hu, Rohan Chandra, Roberto Martín-Martín, and Peter Stone. Deep reinforcement learning for robotics: A survey of real-world successes. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, pages 28694–28698, 2025. 2 

- [19] Toru Lin, Kartik Sachdev, Linxi Fan, Jitendra Malik, and Yuke Zhu. Sim-to-real reinforcement learning for vision-based dexterous manipulation on humanoids. _arXiv preprint arXiv:2502.20396_ , 2025. 2 

- [20] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control. _ArXiv_ , abs/2410.24164, 2024. 3, 10 

- [21] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with open-world generalization, 2025. 3 

- [22] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 3 

- [23] Joao Carvalho, An T Le, Mark Baierl, Dorothea Koert, and Jan Peters. Motion planning diffusion: Learning and planning of robot motions with diffusion models. In _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 1916–1923. IEEE, 2023. 3 

- [24] Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations. _arXiv preprint arXiv:2403.03954_ , 2024. 3 

- [25] Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D Manning, Stefano Ermon, and Chelsea Finn. Direct preference optimization: Your language model is secretly a reward model. _Advances in Neural Information Processing Systems_ , 36:53728–53741, 2023. 3 

- [26] Zijian Zhang, Kaiyuan Zheng, Zhaorun Chen, Joel Jang, Yi Li, Chaoqi Wang, Mingyu Ding, Dieter Fox, and Huaxiu Yao. Grape: Generalizing robot policy via preference alignment, 2024. 3, 9, 12 

- [27] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 3 

- [28] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-languageaction models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 3 

15 

- [29] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , page 02783649241273668, 2023. 3 

- [30] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 3 

- [31] Han Xue, Jieji Ren, Wendi Chen, Gu Zhang, Yuan Fang, Guoying Gu, Huazhe Xu, and Cewu Lu. Reactive diffusion policy: Slow-fast visual-tactile policy learning for contact-rich manipulation. _arXiv preprint arXiv:2503.02881_ , 2025. 3 

- [32] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 3 

- [33] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You Liang Tan, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, 2024. 3 

- [34] Yifan Zhong, Xuchuan Huang, Ruochong Li, Ceyao Zhang, Yitao Liang, Yaodong Yang, and Yuanpei Chen. Dexgraspvla: A vision-language-action framework towards general dexterous grasping. _arXiv preprint arXiv:2502.20900_ , 2025. 3 

- [35] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. _arXiv preprint arXiv:2503.22020_ , 2025. 3 

- [36] Homer Walke, Kevin Black, Abraham Lee, Moo Jin Kim, Max Du, Chongyi Zheng, Tony Zhao, Philippe Hansen-Estruch, Quan Vuong, Andre He, Vivek Myers, Kuan Fang, Chelsea Finn, and Sergey Levine. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning (CoRL)_ , 2023. 4 

- [37] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Tomas Jackson, Sally Jesmonth, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Kuang-Huei Lee, Sergey Levine, Yao Lu, Utsav Malla, Deeksha Manjunath, Igor Mordatch, Ofir Nachum, Carolina Parada, Jodilyn Peralta, Emily Perez, Karl Pertsch, Jornell Quiambao, Kanishka Rao, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Kevin Sayed, Jaspiar Singh, Sumedh Sontakke, Austin Stone, Clayton Tan, Huong Tran, Vincent Vanhoucke, Steve Vega, Quan Vuong, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. Rt-1: Robotics transformer for real-world control at scale. In _arXiv preprint arXiv:2212.06817_ , 2022. 4, 7, 8 

- [38] Ruiyuan Gao, Kai Chen, Enze Xie, Lanqing Hong, Zhenguo Li, Dit-Yan Yeung, and Qiang Xu. MagicDrive: Street view generation with diverse 3d geometry control. In _International Conference on Learning Representations_ , 2024. 4 

- [39] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, Jiagang Zhu, and Jiwen Lu. Drivedreamer: Towards real-world-driven world models for autonomous driving. _arXiv preprint arXiv:2309.09777_ , 2023. 4 

- [40] Xiaofeng Wang, Zheng Zhu, Guan Huang, Boyuan Wang, Xinze Chen, and Jiwen Lu. Worlddreamer: Towards general world models for video generation via predicting masked tokens. _arXiv preprint arXiv:2401.09985_ , 2024. 4 

- [41] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. Gaia-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 4 

16 

- [42] Guosheng Zhao, Chaojun Ni, Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, Boyuan Wang, Youyi Zhang, Wenjun Mei, and Xingang Wang. Drivedreamer4d: World models are effective data machines for 4d driving scene representation. _arXiv preprint arXiv:2410.13571_ , 2024. 4 

- [43] Yunzhi Yan, Haotong Lin, Chenxu Zhou, Weijie Wang, Haiyang Sun, Kun Zhan, Xianpeng Lang, Xiaowei Zhou, and Sida Peng. Street gaussians for modeling dynamic urban scenes. _arXiv preprint arXiv:2401.01339_ , 2024. 4 

- [44] Chaojun Ni, Guosheng Zhao, Xiaofeng Wang, Zheng Zhu, Wenkang Qin, Guan Huang, Chen Liu, Yuyin Chen, Yida Wang, Xueyang Zhang, et al. Recondreamer: Crafting world models for driving scene reconstruction via online restoration. _arXiv preprint arXiv:2411.19548_ , 2024. 4 

- [45] Po-Chen Ko, Jiayuan Mao, Yilun Du, Shao-Hua Sun, and Joshua B. Tenenbaum. Learning to act from actionless videos through dense correspondences, 2023. 4 

- [46] Yilun Du, Sherry Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Josh Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning universal policies via text-guided video generation. _Advances in neural information processing systems_ , 36:9156–9172, 2023. 4 

- [47] Siyuan Zhou, Yilun Du, Jiaben Chen, Yandong Li, Dit-Yan Yeung, and Chuang Gan. RoboDreamer: Learning compositional world models for robot imagination. In Ruslan Salakhutdinov, Zico Kolter, Katherine Heller, Adrian Weller, Nuria Oliver, Jonathan Scarlett, and Felix Berkenkamp, editors, _Proceedings of the 41st International Conference on Machine Learning_ , volume 235 of _Proceedings of Machine Learning Research_ , pages 61885–61896. PMLR, 21–27 Jul 2024. 4 

- [48] Ying Li, Xiaobao Wei, Xiaowei Chi, Yuming Li, Zhongyu Zhao, Hao Wang, Ningning Ma, Ming Lu, and Shanghang Zhang. Manipdreamer: Boosting robotic manipulation world model with action tree and visual guidance, 2025. 4 

- [49] Liu Liu, Xiaofeng Wang, Guosheng Zhao, Keyu Li, Wenkang Qin, Jiaxiong Qiu, Zheng Zhu, Guan Huang, and Zhizhong Su. Robotransfer: Geometry-consistent video diffusion for robotic visual policy transfer, 2025. 4 

- [50] Bernhard Kerbl, Georgios Kopanas, Thomas Leimkühler, and George Drettakis. 3d gaussian splatting for real-time radiance field rendering. _ACM ToG_ , 2023. 4 

- [51] Ben Mildenhall, Pratul P Srinivasan, Matthew Tancik, Jonathan T Barron, Ravi Ramamoorthi, and Ren Ng. Nerf: Representing scenes as neural radiance fields for view synthesis. _Communications of the ACM_ , 2021. 4 

- [52] Guosheng Zhao, Xiaofeng Wang, Chaojun Ni, Zheng Zhu, Wenkang Qin, Guan Huang, and Xingang Wang. Recondreamer++: Harmonizing generative and reconstructive models for driving scene representation. _arXiv preprint arXiv:2503.18438_ , 2025. 4 

- [53] Chaojun Ni, Xiaofeng Wang, Zheng Zhu, Weijie Wang, Haoyun Li, Guosheng Zhao, Jie Li, Wenkang Qin, Guan Huang, and Wenjun Mei. Wonderturbo: Generating interactive 3d world in 0.72 seconds. _arXiv preprint arXiv:2504.02261_ , 2025. 4 

- [54] Zelin Zhou, Saurav Uprety, Shichuang Nie, and Hongzhou Yang. Gs-gvins: A tightly-integrated gnss-visual-inertial navigation system augmented by 3d gaussian splatting. _arXiv preprint arXiv:2502.10975_ , 2025. 4 

- [55] Yifan Liu, Chenxin Li, Hengyu Liu, Chen Yang, and Yixuan Yuan. Foundation model-guided gaussian splatting for 4d reconstruction of deformable tissues. _IEEE Transactions on Medical Imaging_ , 44(6):2672–2682, 2025. 4 

- [56] Meng Wang, Junyi Wang, Changqun Xia, Chen Wang, and Yue Qi. Og-mapping: Octree-based structured 3d gaussians for online dense mapping. _arXiv preprint arXiv:2408.17223_ , 2024. 4 

- [57] Haozhe Lou, Yurong Liu, Yike Pan, Yiran Geng, Jianteng Chen, Wenlong Ma, Chenglong Li, Lin Wang, Hengzhen Feng, Lu Shi, Liyi Luo, and Yongliang Shi. Robo-gs: A physics consistent spatial-temporal model for robotic arm with hybrid representation, 2024. 4 

17 

- [58] Mohammad Nomaan Qureshi, Sparsh Garg, Francisco Yandun, David Held, George Kantor, and Abhishesh Silwal. Splatsim: Zero-shot sim2real transfer of rgb manipulation policies using gaussian splatting, 2024. 4 

- [59] Diederik P Kingma and Max Welling. Auto-encoding variational bayes, 2022. 6, 7 

- [60] Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao Zhang, Jie Yang, Chunyuan Li, Jianwei Yang, Hang Su, Jun Zhu, et al. Grounding dino: Marrying dino with grounded pre-training for open-set object detection. _arXiv preprint arXiv:2303.05499_ , 2023. 6 

- [61] Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr, Roman Rädle, Chloe Rolland, Laura Gustafson, Eric Mintun, Junting Pan, Kalyan Vasudev Alwala, Nicolas Carion, Chao-Yuan Wu, Ross Girshick, Piotr Dollár, and Christoph Feichtenhofer. Sam 2: Segment anything in images and videos, 2024. 6 

- [62] Zipeng Fu, Tony Z. Zhao, and Chelsea Finn. Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation. In _Conference on Robot Learning (CoRL)_ , 2024. 7 

- [63] Thomas Unterthiner, Sjoerd Van Steenkiste, Karol Kurach, Raphael Marinier, Marcin Michalski, and Sylvain Gelly. Towards accurate generative models of video: A new metric & challenges. _arXiv preprint arXiv:1812.01717_ , 2018. 8 

- [64] Richard Zhang, Phillip Isola, Alexei A Efros, Eli Shechtman, and Oliver Wang. The unreasonable effectiveness of deep features as a perceptual metric. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 586–595, 2018. 8 

- [65] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 8 

- [66] Gemini Team, Rohan Anil, Sebastian Borgeaud, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. Gemini: a family of highly capable multimodal models. _arXiv preprint arXiv:2312.11805_ , 2023. 10 

- [67] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 12 

- [68] Yuntao Bai, Andy Jones, Kamal Ndousse, Amanda Askell, Anna Chen, Nova DasSarma, Dawn Drain, Stanislav Fort, Deep Ganguli, Tom Henighan, et al. Training a helpful and harmless assistant with reinforcement learning from human feedback. _arXiv preprint arXiv:2204.05862_ , 2022. 12 

18 

