---
title: "An Efficient and Multi-Modal Navigation System with One-Step World Model"
date: "2026-01-18"
authors: "Wangtian Shen; Ziyang Meng; Jinming Ma; Mingliang Zhou; Diyun Xiang"
url: https://arxiv.org/abs/2601.12277
pdf: https://arxiv.org/pdf/2601.12277
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.12277)** / [論文ページ](https://arxiv.org/abs/2601.12277)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **An Efficient and Multi-Modal Navigation System with One-Step World Model** 

**Wangtian Shen**<sup>1</sup> , **Ziyang Meng**<sup>1</sup><sup>_∗_</sup> , **Jinming Ma**<sup>2</sup> , **Mingliang Zhou**<sup>2</sup> and **Diyun Xiang**<sup>2</sup> 

1Tsinghua University, 2Xiaomi (China) 

swt22@mails.tsinghua.edu.cn, ziyangmeng@tsinghua.edu.cn, majinming3@xiaomi.com, zhoumingliang@xiaomi.com, xiangdiyun@gmail.com 

## **Abstract** 

Navigation is a fundamental capability for mobile robots. While the current trend is to use learningbased approaches to replace traditional geometrybased methods, existing end-to-end learning-based policies often struggle with 3D spatial reasoning and lack a comprehensive understanding of physical world dynamics. Integrating world models—which predict future observations conditioned on given actions—with iterative optimization planning offers a promising solution due to their capacity for imagination and flexibility. However, current navigation world models, typically built on pure transformer architectures, often rely on multistep diffusion processes and autoregressive frameby-frame generation. These mechanisms result in prohibitive computational latency, rendering realtime deployment impossible. To address this bottleneck, we propose a lightweight navigation world model that adopts a one-step generation paradigm and a 3D U-Net backbone equipped with efficient spatial-temporal attention. This design drastically reduces inference latency, enabling high-frequency control while achieving superior predictive performance. We also integrate this model into an optimization-based planning framework utilizing anchor-based initialization to handle multi-modal goal navigation tasks. Extensive closed-loop experiments in both simulation and real-world environments demonstrate our system’s superior efficiency and robustness compared to state-of-the-art baselines. Project page: https://robotnav-bot.github.io/ nav-onestepwm/ 

## **1 Introduction** 

Visual navigation constitutes a cornerstone of autonomous robotics, enabling robots to perceive their surroundings and reach target goals in complex, unstructured environments. In recent years, by leveraging large-scale datasets, methods like GNM [Shah _et al._ , 2023a], ViNT [Shah _et al._ , 2023b] and NoMaD [Sridhar _et al._ , 2024] have demonstrated remarkable ro- 

> _∗_ Corresponding author 

bustness and generalization capabilities. However, these endto-end policies often operate as “black boxes”, mapping observations directly to actions without explicit 3D spatial reasoning, which limits their performance in challenging navigation tasks. 

World models [Ha and Schmidhuber, 2018] offer a promising alternative to end-to-end policies by enabling robots to ’imagine’ outcomes, thereby enhancing spatial reasoning [Yang _et al._ , 2025]. While recent works integrate video prediction with planning [Bar _et al._ , 2025; Zhou _et al._ , 2025], practical deployment faces a critical bottleneck: computational latency. State-of-the-art models predominantly rely on diffusion frameworks, where iterative denoising and autoregressive generation accumulate significant latency and errors. This overhead becomes prohibitive when coupled with planning algorithms that evaluate multiple action candidates, hindering real-time usage. Furthermore, while prior works primarily focus on open-loop, image-goal evaluations, navigation world models have the potential to handle multi-modal goals, and closed-loop experiments in both simulation and real-world environments are essential for validating their effectiveness. 

In this work, we propose a lightweight navigation world model designed specifically for real-time inference. Unlike standard diffusion-based approaches that suffer from slow iterative sampling, our model adopts the one-step generation paradigm [Frans _et al._ , 2024]. This drastically reduces the inference time required to predict future observations, making it feasible to integrate predictive modeling into high-frequency control loops. Additionally, we introduce a computation-efficient spatial-temporal attention mechanism embedded within a 3D U-Net backbone, enabling the model to simultaneously predict all future frames in a nonautoregressive manner. This synergistic design substantially boosts generation efficiency while effectively enhancing the quality of the predicted sequences. To further improve performance in limited-data regimes, we incorporate strategic pretraining and random trajectory sampling to facilitate robust generation. 

Building upon this efficient world model, we integrate it with an optimization-based planning framework, utilizing task-specific loss functions to iteratively refine action samples. Such an integration enables navigation under multimodal goal conditions, successfully encompassing image- 


Figure 1: We present a unified navigation framework founded on world models and planning strategies. The proposed system can be directly used to support diverse goal modalities, seamlessly accommodating image-goal, language-goal, and point-goal navigation tasks. 

goal, language-goal, and point-goal navigation tasks in a unified framework, as illustrated in Figure 1. Through a comprehensive exploration of trajectory initialization strategies and loss function designs, we establish a planning framework with superior performance. These efforts cumulatively produce a robust, closed-loop world-model-based navigation system, which we demonstrate to be both effective and efficient in simulation and real-world environments. 

critic function. LeLaN [Hirose _et al._ , 2024] learns languageconditioned navigation policies from unlabeled and actionfree videos. OmniVLA [Hirose _et al._ , 2025] presents a generalizable and flexible omni-modal robotic foundation model. Although significant progress has been made by introducing learning-based solutions for navigation, current methods exhibit limited spatial reasoning abilities, leading to suboptimal navigation performance. 

Our main contributions are summarized as follows: 

- We propose a lightweight but effective navigation world model leveraging one-step generation paradigm, spatialtemporal attention, and pretraining strategy. 

- We develop a unified navigation system for multi-modal goal navigation by integrating our world model with a planning framework utilizing anchor-based initialization. 

- We demonstrate the superiority of the proposed method through closed-loop experiments in both simulation and the real world. 

## **2 RELATED WORK** 

### **2.1 Learning Based Visual Navigation** 

Traditional solutions to navigation problem typically consist of distinct localization, mapping, and planning modules [LaValle, 2006]. The advent of machine learning shifts the focus towards learning-based solutions for visual navigation. GNM [Shah _et al._ , 2023a] shows that training on diverse robotic datasets boosts generalization. ViNT [Shah _et al._ , 2023b] and EffoNAV [Shen _et al._ , 2025] further advance this by employing transformer architectures and visual foundation models to establish foundational models for image-goal navigation in general environments. NoMaD [Sridhar _et al._ , 2024] leverages diffusion model to execute both navigation and exploration tasks within a single framework. NavDP [Cai _et al._ , 2025] enables robust and efficient sim-to-real navigation by leveraging diffusion-based trajectory generation alongside a 

### **2.2 World Model for Embodied Intelligence** 

Unlike end-to-end policy, the primary objective of a world model [Ha and Schmidhuber, 2018] is to simulate environmental dynamics. While early research focused on enhancing sample efficiency in reinforcement learning [Hafner _et al._ , 2019; Hafner _et al._ , 2023], recent works leverage world models for high-dimensional visual generation and planning. Approaches like Pathdreamer [Koh _et al._ , 2021], UniPi [Du _et al._ , 2023], and Genie [Bruce _et al._ , 2024] generate plausible future observations to facilitate interaction and navigation. Furthermore, integrating world models with planning has shown significant promise. NWM [Bar _et al._ , 2025] utilizes generative predictions to optimize action sequences, while [Zhou _et al._ , 2025] introduce 3D memory for temporal consistency. However, the high computational cost of these generative processes makes real-time deployment impossible. On the other hand, approaches like DINO-WM [Zhou _et al._ , 2024] and [Zhang _et al._ , 2025] construct world models within the latent space to minimize computational overhead. However, performing generation and planning solely in the latent space often cannot produce explicit 3D spatial prediction and different goal modals cannot be integrated into a unified framework. . 

## **3 METHODS** 

### **3.1 One-Step World Model for Navigation** 

Formally, the navigation world model is designed to predict the future observation _sτ_ +1 based on the current observa- 


Figure 2: Illustration of our world model architecture and the world model-based planner. (a) Architecture of the proposed navigation world model. Built upon a 3D U-Net backbone, the model integrates convolutional layers with spatial-temporal attention blocks and is trained using a shortcut objective. (b) The action optimization process conditioned on navigation goals. Leveraging the world model, we utilize a loss function to score action candidates, thereby enabling navigation with multi-modal goals. 

tion _sτ_ and the action _aτ_ . While existing generative approaches typically leverage diffusion models[Ho _et al._ , 2020; Song _et al._ , 2020] or flow-matching models[Lipman _et al._ , 2022], their sampling processes require iterative denoising over numerous neural network passes, rendering the generation computationally expensive. To address this issue, we adopt the shortcut training objective [Frans _et al._ , 2024] to enable one-step generation, thereby significantly reducing computational inference time. The shortcut model is conditioned not only on the flow timestep _t_ , but also on a desirable step size _d_ . Formally, the world model _fθ_ predicts the velocity vector _vt_ = _fθ_ ( _s_<sup>(</sup> _τ_<sup>_t_</sup> +1<sup>)</sup><sup>_, sτ, aτ, t, d_), where</sup><sup>_s_(</sup> _τ_<sup>_t_</sup> +1<sup>)represents the</sup> noisy future observation. For the minimum step size _d_ min, the model is trained using the standard flow matching loss. For larger step sizes _d_ min _< d <_ 1, a bootstrap consistency loss that distills the trajectory of two smaller substeps (size _d/_ 2) into a single step is employed, as shown in Figure 2(a). The training objective is formulated as follows: 


By employing this distillation training, the navigation world model learns to generate future observations from gaussian 

noise within one step. 

### **3.2 Architecture of Navigation World Model** 

Following the formulation in the previous section, we now provide the implementation details of the world model _fθ_ . Existing navigation world models[Bar _et al._ , 2025] in navigation predominantly adopt an autoregressive approach, generating predictions iteratively frame-by-frame. We argue that such autoregressive methods suffer from performance degradation due to error accumulation over long horizons and result in high computational latency. Instead, the proposed architecture utilizes a 3D U-Net backbone to simultaneously predict a sequence of 11 future frames. Drawing inspiration from the Stable Diffusion framework [Rombach _et al._ , 2022], we employ a hybrid structure integrating both CNNs and transformers to capture spatiotemporal dependencies, as illustrated in Figure 2. We utilize a pretrained VAE [Rombach _et al._ , 2022] to compress observations into the latent space. Future observations are generated directly within this latent space to leverage the benefits of compressed representations. Finally, the generated latent representations are decoded by the VAE to recover images in pixel space. 

**Action Embedding.** The action input _aτ_ consists of _N_ relative waypoints ( _x, y, ϕ_ ). To ensure continuity, we encode _ϕ_ as (cos _ϕ,_ sin _ϕ_ ), forming an ( _N,_ 4) vector. This input is projected by a 4-layer MLP into a high-dimensional embedding, which conditions the spatial attention blocks via crossattention. 

**Spatial and Temporal Attention.** In the 3D U-Net architecture, each processing block comprises three components: CNN module, Spatial Attention module, and Temporal Attention module. Since the computational complexity of the transformer architecture scales quadratically with context 


Figure 3: Comparison of anchor-based initialization and random initialization. 

length, processing the full spatiotemporal volume globally is computationally prohibitive. We therefore decouple spatial and temporal modeling, as done in prior works [Blattmann _et al._ , 2023; Wang _et al._ , 2023]. The CNN and Spatial Attention modules operate in a frame-wise manner, focusing exclusively on capturing intra-frame spatial dependencies without cross-frame interaction. Conversely, the Temporal Attention module is dedicated to inter-frame information propagation. We employ a window-based attention mechanism[Liu _et al._ , 2021; Gu _et al._ , 2023] for the temporal module. In particular, we partition each frame into _m×m_ spatial regions (windows). Attention operations are restricted locally, such that a token computes attention scores exclusively with other tokens located within the same spatial window, thereby reducing the context length while maintaining spatiotemporal consistency. 

### **3.3 Training Details** 

Following the setup described in [Bar _et al._ , 2025], we collect 500 trajectories within a single indoor environment for training. During model training, we adopt a random trajectory sampling strategy: the position of the final frame is selected randomly, and 10 frames are randomly sampled between the current and final frames to generate a single training instance. This approach effectively increases trajectory diversity within the limited dataset. 

In our experiments, we observed that relying solely on data collected in the new scene degraded the prediction quality of the navigation world model. To address this, we first train a base model on a large-scale public navigation dataset[Shah _et al._ , 2023a] to obtain a pretrained navigation world model. We then fine-tune this pretrained model using the specific data collected from the new environment. Our results demonstrate that this pretraining strategy significantly enhances navigation performance. 

### **3.4 Navigation with World Model** 

Leveraging the world model’s ability to predict future observations conditioned on given actions, we implement a modelbased planning framework. Specifically, we use the world model to generate future observations for a set of candidate action samples. Each sample is then scored based on its alignment with the specific navigation goal (e.g., image, language or point-goal). We employ the Cross-Entropy Method (CEM) [Rubinstein, 1997] to optimize this process and select the optimal action. 

To minimize computational overhead, we limit the sample size to 32 actions at each optimization step. However, we observe that with such a limited sample size, random initialization often fails to sufficiently cover the action space. This results in suboptimal initialization for the planner, ultimately degrading navigation performance. To address this, we employ an anchor-based initialization strategy, where initial candidate trajectories are generated using fixed sets of linear and angular velocities, as shown in Figure 3. Empirical results demonstrate that the performance of such an anchor-based approach significantly outperforms that of random initialization. 

## **4 Generation Experiments** 

We evaluate the generation quality of the proposed one-step navigation world model in this section. 

### **4.1 Experimental Setup** 

We collect training datasets from the MP3D dataset[Chang _et al._ , 2017], using the Habitat simulator[Szot _et al._ , 2021]. Each dataset consists of 500 trajectories within the respective indoor scene. All models are trained independently on each of the datasets and tested on unseen trajectories. 

We compare the proposed method with the following baselines: 

- **NWM** [Bar _et al._ , 2025]. NWM is a navigation world model which employs a Conditional Diffusion Transformer (CDiT) architecture to predict future images autoregressively frame-by-frame. We use its -B variant, due to its comparable parameter scale to our model, and replace its original diffusion model with the shortcut model [Frans _et al._ , 2024], consistent with the approach used in our method. 

- **Ours (w/o random traj)** . An ablative variant of our method without random trajectory sampling strategy in training. 

- **Ours (w/o pretrain)** . An ablative variant of our method without first training on large-scale public navigation datasets. 

### **4.2 Generation Performance** 

We utilize PSNR, SSIM [Wang _et al._ , 2004], LPIPS [Zhang _et al._ , 2018], DreamSim [Fu _et al._ , 2023], and FID [Heusel _et al._ , 2017] to measure the frame-wise similarity between the generated output and ground truth. To evaluate the overall spatiotemporal quality of the generated video, we also introduce FVD [Unterthiner _et al._ , 2018]. Furthermore, given the importance of generation speed, we report the inference time for generating 11 future frames with a batch size of 1 on an NVIDIA H200 GPU. The experimental results are presented in Table 1. Quantitative results demonstrate the superiority of the proposed model. It can be seen that the proposed model surpasses NWM by a wide margin in both perframe quality and spatiotemporal consistency. Moreover, the proposed model is significantly more computational-efficient, reducing inference time by approximately 45% (0.076s vs. 

|Method|PSNR_↑_|SSIM_↑_|LPIPS_↓_|DreamSim_↓_|FID_↓_|FVD_↓_|Params (M)|Time (s)_↓_|
|---|---|---|---|---|---|---|---|---|
|NWM|14.557|0.368|0.401|0.336|94.850|27.173|194|0.138|
|Ours (w/o random traj)|17.196|0.456|0.290|0.286|89.682|18.518|175|**0.076**|
|Ours (w/o pretrain)|16.810|0.434|0.300|0.304|98.724|21.720|175|**0.076**|
|Ours|**17.611**|**0.473**|**0.267**|**0.272**|**83.826**|**17.254**|175|**0.076**|


Table 1: Generation Results of different methods 


Figure 4: Qualitative comparison of our method against baselines. Given the initial observation, the frames generated by our model achieve higher quality than those of NWM and closely match the ground truth. Furthermore, the visualization demonstrates that random trajectory sampling during training and pretraining on public datasets play a crucial role in performance. 

0.138s) with a similar parameter scale. Ablation studies further demonstrate that the random trajectory sampling strategy and pretraining on public datasets notably enhance model generalization. 

As illustrated in Figure 4, NWM struggles with precise action execution. The recursive nature of its autoregressive generation leads to compounding errors, resulting in severe position drift from the ground truth. On the other hand, the proposed method mitigates these issues by generating all future frames in a single forward pass. The incorporation of temporal attention allows the model to effectively learn temporal dependencies, ensuring higher fidelity in long-sequence generation. Additionally, the use of random trajectory sampling strategy combined with pretraining on large-scale datasets further improves the visual quality and details of the generated images. 

## **5 Navigation Experiments** 

### **5.1 Experimental Setup** 

Leveraging the proposed world model with task-specific loss functions, our method enables navigation guided by multimodal goals. We successfully execute image-goal, languagegoal and point-goal navigation, significantly outperforming competitive baselines. For CEM optimization used in the proposed method, we use a sample size of 32, select the top 5 samples per iteration, and perform 5 iterations. The experimental evaluation consists of 150 episodes across 5 different scenes for image-goal, language-goal and point-goal navigation. We employ _Success Rate (SR)_ and _Success-weighted Path Length (SPL)_ to evaluate navigation performance. Additionally, we report the inference time for each method, measured on an NVIDIA H200 GPU. 

Apart from the compared methods mentioned in Section 4.1, we also compare the proposed method with several baselines: 

- **NoMaD** [Sridhar _et al._ , 2024]. A unified diffusion policy utilizing goal masking to handle both exploration and image-goal navigation. 

- **OmniVLA** [Hirose _et al._ , 2025]. An omni-modal robot navigation model built upon the OpenVLA[Kim _et al._ , 2024] backbone. 

- **Ours (random init)** . An ablative variant of our method with random initialization in CEM instead of anchorbased initialization, as described in Section 3.4. 

To ensure a fair comparison, the NWM baseline is evaluated using the same planning configuration as our method, including the integration of the proposed anchor-based initialization strategy and the use of the same planning loss function. 

**Image-Goal Navigation.** To implement image-goal navigation, we employ LPIPS [Zhang _et al._ , 2018] as loss function to score sampled trajectories. Drawing inspiration from prior vision-based approaches [Shah _et al._ , 2023a; Sridhar _et al._ , 2024], we utilize a topological memory system to achieve long-horizon navigation. Specifically, the process initiates with the first observation. At each time step, a distance estimation network identifies the nearest node in the topological graph to estimate the current location. Subsequently, the image of the adjacent node is fed into the policy system as the immediate target. 

**Language-Goal Navigation.** To implement language-goal navigation, we employ SigLIP [Zhai _et al._ , 2023] as the scoring function to evaluate sampled trajectories. We utilize Qwen2-VL [Wang _et al._ , 2024] to generate navigational 

|Method|I|mage-G|oal|L|anguage-|Goal||Point-G|oal|
|---|---|---|---|---|---|---|---|---|---|
||SR|SPL|Time (s)|SR|SPL|Time (s)|SR|SPL|Time (s)|
|NoMaD|16.67|15.13|0.097|-|-|-|-|-|-|
|OmniVLA|36.67|34.78|0.113|62.67|56.52|0.078|40.00|36.72|0.081|
|NWM|43.33|38.66|1.086|51.33|45.98|1.613|**52.67**|**47.31**|1.688|
|Ours (w/o random traj)|64.67|61.51|0.765|63.33|56.91|1.179|50.67|45.17|1.290|
|Ours (w/o pretrain)|64.00|61.11|0.765|65.33|58.19|1.179|48.00|43.79|1.290|
|Ours (random init)|69.33|62.12|0.765|59.33|50.27|1.179|50.00|43.05|1.290|
|Ours|**72.67**|**69.10**|0.765|**69.33**|**60.90**|1.179|50.00|46.24|1.290|


Table 2: Navigation results of image-goal, language-goal, and point goal tasks 


Figure 5: Visualization of trajectories predicted by different methods in image-goal (left) and language-goal (right) navigation. 

language instructions conditioned on the target image for the task. 

**Point-Goal Navigation.** To implement point-goal navigation, we incorporate Depth-Anything [Yang _et al._ , 2024] to perform monocular depth estimation on the predicted future images. We formulate a composite planning loss function to evaluate candidate trajectories. Specifically, this loss is defined as the weighted sum of two terms: (1) the Euclidean distance between the terminal point of the sampled trajectory and the target coordinate, and (2) the negative mean depth value in the central region of the predicted image (to penalize proximity to obstacles). 

### **5.2 Navigation Performance Resluts** 

The quantitative results in Table 2 demonstrate that the proposed model significantly outperforms both the world-model baseline (NWM) and end-to-end policies (NoMaD, OmniVLA). Specifically, in the image-goal navigation task, our method achieves a Success Rate (SR) of 72.67%, surpassing NWM by a substantial margin of 29.3% and OmniVLA by 36.0%. For language-goal tasks, the proposed approach attains the highest SR of 69.33%, exceeding NWM by 18.0% and OmniVLA by 6.7%. Figure 5 visualizes the trajectories generated by different methods under identical observations. It is evident that world-model-based methods exhibit superior spatial reasoning and semantic understanding capabilities. Specifically, when facing a substantial offset between the current and target difference, end-to-end policies often fail to 

capture the underlying spatial relationship, whereas the proposed approach maintains an accurate understanding of the goal-relative geometry. Furthermore, in the point-goal task, our method yields performance comparable to NWM while consistently outperforming OmniVLA, demonstrating the inherent advantages of world-model-based framework. Crucially, compared to NWM, the proposed method exhibits a significant improvement in inference speed. Such a result is attributed to the model’s paradigm to simultaneously predict all future sequence frames, combined with the utilization of computationally efficient spatial-temporal attention. 

|Loss Fuction|SR|SPL|Time (s)|
|---|---|---|---|
|BLIP|59.33|51.43|2.183|
|CLIP|61.33|53.15|1.094|
|SigLIP (default)|**69.33**|**60.90**|1.179|


Table 3: Language-goal navigation results of different loss function 

### **5.3 Ablations** 

Table 2 presents the performance comparison between the proposed full method and two ablation variants. The results underscore the critical roles of both the pretraining and random trajectory sampling strategy employed during training. Furthermore, we evaluate the impact of initialization within the CEM planner by comparing random initialization strategy against the proposed anchor-based initialization strategy. As 


Figure 6: Qualitative comparison of predicted trajectories using anchor-based and random initialization, respectively, in image-goal (left) and language-goal (right) navigation. 


Figure 7: Overview of the robotic platforms in our real-world evaluation. 

shown in Table 2, the anchor-based approach is instrumental in boosting navigation performance. This advantage is further corroborated by the qualitative visualization in Figure 6, which reveals that anchor-based initialization yields smoother and more concentrated trajectory samples, thereby facilitating more effective planning. 

Furthermore, we observe that the performance of language-goal navigation is highly sensitive to the choice of the planning loss function. To indicate this point, we conduct a comparative analysis using three distinct image-text alignment models—BLIP [Li _et al._ , 2022], CLIP [Radford _et al._ , 2021], and SigLIP [Zhai _et al._ , 2023]—as the guidance objective. The quantitative results are reported in Table 3. It can be found that SigLIP yields the superior navigation performance, outperforming the other image-text alignment models. 

## **6 Real-world Experiments** 

To further validate the effectiveness of the proposed method, we conduct real-world experiments on a mobile robot platform equipped with an Intel RealSense camera, as depicted in Figure. 7. The system operates via a client-server architecture: the robot transmits real-time observations to a cloud server via a network connection, where the model performs inference and returns control commands (i.e., linear and angular velocities). We conduct 25 trials for each method on each task. The quantitative results, presented in Table 4, in- 

|Method|Image-Goal|Language-Goal|Point-Goal|
|---|---|---|---|
|NoMaD|40%|-|-|
|OmniVLA|52%|56%|**76%**|
|NWM|48%|32%|68%|
|Ours|**80%**|**68%**|**76%**|


Table 4: Real-world navigation Results 

dicate that the proposed approach consistently outperforms baselines in physical environments, demonstrating its robustness and strong generalization capabilities. 

## **7 Conclusion** 

This work presents a lightweight navigation world model that outperforms end-to-end policies while overcoming the inference speed limitations of traditional world models. Leveraging a one-step generation paradigm and a 3D U-Net backbone with spatial-temporal attention, our approach ensures low latency and robust spatial reasoning. Integrated with an anchorbased initialization planning framework, the proposed system achieves superior results in multi-modal goal navigation across simulation and real-world closed-loop experiments. 

Despite these advancements, several limitations remain. First, integrating CEM with the world model necessitates exploration within the whole action space, posing significant challenges for searching complex trajectories. Second, the iterative optimization process requires a trade-off between generation quality and inference speed. In future research, we aim to address these challenges by investigating a navigation world model with a latent action space [Bu _et al._ , 2025] and by constructing a fast-slow dual system [Chen _et al._ , 2025] that combines the predictive power of the world model with a reactive local policy. 

## **References** 

[Bar _et al._ , 2025] Amir Bar, Gaoyue Zhou, Danny Tran, Trevor Darrell, and Yann LeCun. Navigation world mod- 

els. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 15791–15801, 2025. 

- [Blattmann _et al._ , 2023] Andreas Blattmann, Tim Dockhorn, Sumith Kulal, Daniel Mendelevitch, Maciej Kilian, Dominik Lorenz, Yam Levi, Zion English, Vikram Voleti, Adam Letts, et al. Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint arXiv:2311.15127_ , 2023. 

- [Bruce _et al._ , 2024] Jake Bruce, Michael D Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, et al. Genie: Generative interactive environments. In _Forty-first International Conference on Machine Learning_ , 2024. 

- [Bu _et al._ , 2025] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2505.06111_ , 2025. 

- [Cai _et al._ , 2025] Wenzhe Cai, Jiaqi Peng, Yuqiang Yang, Yujian Zhang, Meng Wei, Hanqing Wang, Yilun Chen, Tai Wang, and Jiangmiao Pang. Navdp: Learning simto-real navigation diffusion policy with privileged information guidance. _arXiv preprint arXiv:2505.08712_ , 2025. 

- [Chang _et al._ , 2017] Angel Chang, Angela Dai, Thomas Funkhouser, Maciej Halber, Matthias Niebner, Manolis Savva, Shuran Song, Andy Zeng, and Yinda Zhang. Matterport3d: Learning from rgb-d data in indoor environments. In _2017 International Conference on 3D Vision (3DV)_ , pages 667–676. IEEE Computer Society, 2017. 

- [Chen _et al._ , 2025] Hao Chen, Jiaming Liu, Chenyang Gu, Zhuoyang Liu, Renrui Zhang, Xiaoqi Li, Xiao He, Yandong Guo, Chi-Wing Fu, Shanghang Zhang, et al. Fastin-slow: A dual-system foundation model unifying fast manipulation within slow reasoning. _arXiv preprint arXiv:2506.01953_ , 2025. 

- [Du _et al._ , 2023] Yilun Du, Sherry Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Josh Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning universal policies via textguided video generation. _Advances in neural information processing systems_ , 36:9156–9172, 2023. 

- [Frans _et al._ , 2024] Kevin Frans, Danijar Hafner, Sergey Levine, and Pieter Abbeel. One step diffusion via shortcut models. _arXiv preprint arXiv:2410.12557_ , 2024. 

- [Fu _et al._ , 2023] Stephanie Fu, Netanel Tamir, Shobhita Sundaram, Lucy Chai, Richard Zhang, Tali Dekel, and Phillip Isola. Dreamsim: Learning new dimensions of human visual similarity using synthetic data. _arXiv preprint arXiv:2306.09344_ , 2023. 

- [Gu _et al._ , 2023] Xianfan Gu, Chuan Wen, Weirui Ye, Jiaming Song, and Yang Gao. Seer: Language instructed video prediction with latent diffusion models. _arXiv preprint arXiv:2303.14897_ , 2023. 

- [Ha and Schmidhuber, 2018] David Ha and J¨urgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2(3), 2018. 

- [Hafner _et al._ , 2019] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. _arXiv preprint arXiv:1912.01603_ , 2019. 

- [Hafner _et al._ , 2023] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

- [Heusel _et al._ , 2017] Martin Heusel, Hubert Ramsauer, Thomas Unterthiner, Bernhard Nessler, and Sepp Hochreiter. Gans trained by a two time-scale update rule converge to a local nash equilibrium. _Advances in neural information processing systems_ , 30, 2017. 

- [Hirose _et al._ , 2024] Noriaki Hirose, Catherine Glossop, Ajay Sridhar, Dhruv Shah, Oier Mees, and Sergey Levine. Lelan: Learning a language-conditioned navigation policy from in-the-wild videos. _arXiv preprint arXiv:2410.03603_ , 2024. 

- [Hirose _et al._ , 2025] Noriaki Hirose, Catherine Glossop, Dhruv Shah, and Sergey Levine. Omnivla: An omnimodal vision-language-action model for robot navigation. _arXiv preprint arXiv:2509.19480_ , 2025. 

- [Ho _et al._ , 2020] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. _Advances in neural information processing systems_ , 33:6840–6851, 2020. 

- [Kim _et al._ , 2024] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [Koh _et al._ , 2021] Jing Yu Koh, Honglak Lee, Yinfei Yang, Jason Baldridge, and Peter Anderson. Pathdreamer: A world model for indoor navigation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 14738–14748, 2021. 

- [LaValle, 2006] Steven M LaValle. _Planning algorithms_ . Cambridge university press, 2006. 

- [Li _et al._ , 2022] Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi. Blip: Bootstrapping language-image pretraining for unified vision-language understanding and generation. In _International conference on machine learning_ , pages 12888–12900. PMLR, 2022. 

- [Lipman _et al._ , 2022] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

- [Liu _et al._ , 2021] Ze Liu, Yutong Lin, Yue Cao, Han Hu, Yixuan Wei, Zheng Zhang, Stephen Lin, and Baining Guo. Swin transformer: Hierarchical vision transformer using shifted windows. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 10012– 10022, 2021. 

- [Radford _et al._ , 2021] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In _International Conference on Machine Learning_ , pages 8748–8763, 2021. 

- [Rombach _et al._ , 2022] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Bj¨orn Ommer. High-resolution image synthesis with latent diffusion models. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 10684–10695, 2022. 

- [Rubinstein, 1997] Reuven Y Rubinstein. Optimization of computer simulation models with rare events. _European Journal of Operational Research_ , 99(1):89–112, 1997. 

- [Shah _et al._ , 2023a] Dhruv Shah, Ajay Sridhar, Arjun Bhorkar, Noriaki Hirose, and Sergey Levine. Gnm: A general navigation model to drive any robot. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 7226–7233. IEEE, 2023. 

- [Shah _et al._ , 2023b] Dhruv Shah, Ajay Sridhar, Nitish Dashora, Kyle Stachowicz, Kevin Black, Noriaki Hirose, and Sergey Levine. Vint: A foundation model for visual navigation. In _7th Annual Conference on Robot Learning (CoRL)_ , pages 711–733, 2023. 

- [Shen _et al._ , 2025] Wangtian Shen, Pengfei Gu, Haijian Qin, and Ziyang Meng. Effonav: An effective foundationmodel-based visual navigation approach in challenging environment. _IEEE Robotics and Automation Letters_ , 2025. 

- [Song _et al._ , 2020] Jiaming Song, Chenlin Meng, and Stefano Ermon. Denoising diffusion implicit models. _arXiv preprint arXiv:2010.02502_ , 2020. 

- [Sridhar _et al._ , 2024] Ajay Sridhar, Dhruv Shah, Catherine Glossop, and Sergey Levine. Nomad: Goal masked diffusion policies for navigation and exploration. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 63–70. IEEE, 2024. 

- [Szot _et al._ , 2021] Andrew Szot, Alexander Clegg, Eric Undersander, Erik Wijmans, Yili Zhao, John Turner, Noah Maestre, Mustafa Mukadam, Devendra Singh Chaplot, Oleksandr Maksymets, et al. Habitat 2.0: Training home assistants to rearrange their habitat. _Advances in neural information processing systems_ , 34:251–266, 2021. 

   - [Wang _et al._ , 2024] Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, et al. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. _arXiv preprint arXiv:2409.12191_ , 2024. 

   - [Yang _et al._ , 2024] Lihe Yang, Bingyi Kang, Zilong Huang, Zhen Zhao, Xiaogang Xu, Jiashi Feng, and Hengshuang Zhao. Depth anything v2. _Advances in Neural Information Processing Systems_ , 37:21875–21911, 2024. 

   - [Yang _et al._ , 2025] Yuncong Yang, Jiageng Liu, Zheyuan Zhang, Siyuan Zhou, Reuben Tan, Jianwei Yang, Yilun Du, and Chuang Gan. Mindjourney: Test-time scaling with world models for spatial reasoning. _arXiv preprint arXiv:2507.12508_ , 2025. 

   - [Zhai _et al._ , 2023] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 11975– 11986, 2023. 

   - [Zhang _et al._ , 2018] Richard Zhang, Phillip Isola, Alexei A Efros, Eli Shechtman, and Oliver Wang. The unreasonable effectiveness of deep features as a perceptual metric. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 586–595, 2018. 

   - [Zhang _et al._ , 2025] Zhiwei Zhang, Hui Zhang, Xieyuanli Chen, Kaihong Huang, Chenghao Shi, and Huimin Lu. Latent-space autoregressive world model for efficient and robust image-goal navigation. _arXiv e-prints_ , pages arXiv–2511, 2025. 

   - [Zhou _et al._ , 2024] Gaoyue Zhou, Hengkai Pan, Yann LeCun, and Lerrel Pinto. Dino-wm: World models on pretrained visual features enable zero-shot planning. _arXiv preprint arXiv:2411.04983_ , 2024. 

   - [Zhou _et al._ , 2025] Siyuan Zhou, Yilun Du, Yuncong Yang, Lei Han, Peihao Chen, Dit-Yan Yeung, and Chuang Gan. Learning 3d persistent embodied world models. _arXiv preprint arXiv:2505.05495_ , 2025. 

- [Unterthiner _et al._ , 2018] Thomas Unterthiner, Sjoerd Van Steenkiste, Karol Kurach, Raphael Marinier, Marcin Michalski, and Sylvain Gelly. Towards accurate generative models of video: A new metric & challenges. _arXiv preprint arXiv:1812.01717_ , 2018. 

- [Wang _et al._ , 2004] Zhou Wang, Alan C Bovik, Hamid R Sheikh, and Eero P Simoncelli. Image quality assessment: from error visibility to structural similarity. _IEEE transactions on image processing_ , 13(4):600–612, 2004. 

- [Wang _et al._ , 2023] Jiuniu Wang, Hangjie Yuan, Dayou Chen, Yingya Zhang, Xiang Wang, and Shiwei Zhang. Modelscope text-to-video technical report. _arXiv preprint arXiv:2308.06571_ , 2023. 

