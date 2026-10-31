---
title: "HMVLA: Hyperbolic Multimodal Fusion for Vision-Language-Action Models"
date: "2026-01-28"
authors: "Kun Wang; Xiao Feng; Mingcheng Qu; Tonghua Su"
url: https://arxiv.org/abs/2602.02533
pdf: https://arxiv.org/pdf/2602.02533
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.02533)** / [論文ページ](https://arxiv.org/abs/2602.02533)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **HMVLA: HYPERBOLIC MULTIMODAL FUSION FOR VISION-LANGUAGE-ACTION MODELS** 

_Kun Wang_<sup>1</sup><sup>_,_2</sup> _Xiao Feng_<sup>1</sup><sup>_,_2</sup> _Mingcheng Qu_<sup>1</sup><sup>_,_2</sup> _Tonghua Su_<sup>1</sup><sup>_,_2</sup><sup>_,_3</sup><sup>_∗_</sup> 

1 Harbin Institute of Technology, Harbin, China 

2 Chongqing Research Institute of HIT, Chongqing, China 

3 Guangdong Laboratory of Artificial Intelligence and Digital Economy (SZ), Shenzhen, China 

## **ABSTRACT** 

Vision-Language-Action (VLA) models have recently shown great potential in bridging multimodal perception with robotic control. However, existing methods often rely on direct finetuning of pre-trained Vision-Language Models (VLMs), feeding semantic and visual features directly into a policy network without fully addressing the unique semantic alignment challenges in the VLA domain. In this paper, we propose HMVLA, a novel VLA framework that exploits the inherent hierarchical structures in vision and language for comprehensive semantic alignment. Unlike traditional methods that perform alignment in Euclidean space, our HMVLA embeds multimodal features in hyperbolic space, enabling more effective modeling of the hierarchical relationships present in image–text data. Furthermore, we introduce a sparsely gated Mixture-of-Experts (MoE) mechanism tailored for semantic alignment, which enhances multimodal comprehension between images and text while improving efficiency. Extensive experiments demonstrate that HMVLA surpasses baseline methods in both accuracy and generalization. In addition, we validate its robustness by reconstructing datasets to further test cross-domain adaptability. 

**_Index Terms_ —** Vision-Language-Action, Embodied AI, Hyperbolic space, Mixture-of-Experts 

## **1. INTRODUCTION** 

The rapid development of Large-Language-Models (LLMs) and Vision-Language-Models (VLMs) [1, 2, 3, 4] has significantly advanced Vision-Language-Action (VLA) models in robotics [5, 6, 7, 8, 9, 10]. By leveraging the powerful comprehension capabilities of pre-trained models, VLA systems encode visual and linguistic modalities into feature tokens, which are then fed into a robotic policy network to enable end-to-end action generalization [11, 12]. 

Existing VLA models, such as RT-2[13] and OpenVLA[14], typically fine-tune pre-trained VLMs on robot datasets, directly mapping visual and linguistic features to robot control 


**Fig. 1** . Comparison of hyperbolic representation (Left) and Euclidean contrastive Loss (Right) for VLA Alignment. 

actions. However, this strategy often disrupts the intrinsic consistency of visual and semantic features. In particular, the hierarchical structure of semantics and vision embedded in robot datasets may become perturbed. For example, when training on a “grasp the cup” task where the background is a white table and target is a blue mug, the model may learn spurious correlations ( _e.g.,_ associating “white” with “background” and “blue” with “cup”), instead of grounding the semantics of the action “grasp” and the object “cup”. 

This mismatch between execution semantics and action outcomes highlights a core limitation of current VLA approaches. The phenomenon also echoes broader findings in vision-language research: fine-tuning linguistically aligned visual encoders can lead to overfitting, ultimately failing to preserve the hierarchical semantic–visual structures necessary for robust reasoning and control [13, 14]. Consequently, this weakens the mapping from visual–semantic understanding to robotic actions, leading to diminished execution capabilities. By contrast, models such as CLIP [15] have demonstrated powerful vision-language alignment capabilities and exhibit excellent performance across various tasks. This highlights an important direction for VLA research: how to adapt pre-trained models in a way that preserves the hierarchical structure of vision and semantics [16], ensuring that fine-tuning in the robotics domain enables more faithful grounding and accurate prediction of next-step actions. 

In this paper, we propose HMVLA, a hyperbolic-based multimodal Vision-Language-Action (VLA) framework. Un- 

> _∗_ Corresponding author 


**Fig. 2** . Overview of our HMVLA framework. A hierarchical VLA transformer with hyperbolic projection and a sparsely-gated Mixture-of-Experts (MoE) for enhanced semantic alignment. 

like existing approaches that primarily transfer prior knowledge from generative models or rely on reasoning strategies like chain-of-thought for image inference, our method finetunes the VLM while embedding multimodal features in hyperbolic space [17]. As illustrated in Fig. 1, hyperbolic space, with its property of _exponential expansion_ , provides a natural representation for hierarchical or tree-like structures, enabling VLA models to capture underlying semantic hierarchies in vision–language data with minimal distortion [18]. To further enhance multimodal fusion, we integrate a sparsely-gated Mixture-of-Experts (MoE) mechanism. By dynamically routing vision and language representations within hyperbolic space to specialized experts, the MoE facilitates adaptive alignment between modalities and actions, improving generalization. Our contributions are as follows: 

- We introduce hyperbolic geometry into the VLA domain, leveraging its structural properties to better preserve hierarchical relationships during multimodal fusion. 

- We incorporate the MoE module that adaptively routes information across experts, enhancing alignment between visual and linguistic modalities for action prediction. 

- Experiments show the effectiveness of our framework. We reconstruct the four datasets of the LIBERO [19] to systematically verify the generalization capability of relevant models. 

## **2. METHOD** 

## **2.1. Hyperbolic Semantic Alignment** 

Our HMVLA framework is based on the Lorentz model in hyperbolic geometry, as shown in Figure 2. Specifically, the _n_ -dimensional hyperbolic space is represented as the upper sheet of a two-sheeted hyperboloid embedded in R<sup>_n_+1</sup> . Following the terminology from special relativity [20], we treat the hyperboloid’s axis of symmetry as the time dimension and the remaining axes as space dimensions. Thus, any vector _x ∈_ R<sup>_n_+1</sup> can be expressed as _x_ = [ _xspace, xtime_ ], where 

_xspace ∈_ R<sup>_n_</sup> and _xtime ∈_ R. The Lorentzian inner product is defined as: 


The induced Lorentzian norm is _||x||L_ = ~~�~~ _|<x, x>L|_ . The Lorentz model with curvature _−c_ is: 


All vectors in _L_<sup>_n_</sup> satisfy the following constraint: 


**Tangent Space** at _z ∈L_<sup>_n_</sup> consists of all vectors orthogonal to _z_ under the Lorentzian inner product, forming a Euclidean space: 


**Exponential and logarithmic map** provides a way to map vectors from the tangent space onto the manifold. For a point _z ∈L_<sup>_n_</sup> , it is defined as: 


The inverse operation is the logarithmic map (( _logmz_ : _L_<sup>_n_</sup> _−→ TzL_<sup>_n_</sup> ), which maps a point _x_ on the hyperboloid back into the tangent space: 


We only consider these maps where _z_ is the origin of the hyperboloid ( **O** = [0 _, p_ 1 _/c_ ]). 

Based on the relevant background of hyperbolic space discussed above, we now incorporate it into the HMVLA model. First, we obtain embedding vectors through the image and text encoders, and then apply linear projection to get _venc ∈_ R<sup>_n_</sup> and _lenc ∈_ R<sup>_n_</sup> . We then apply a transformation such 

that the vector _venc_ and _lenc_ lie on the Lorentz hyperboloid _L_<sup>_n_</sup> in R<sup>_n_+1</sup> . Let the vector _v_ = [ _venc,_ 0] _∈_ R<sup>_n_+1</sup> and _l_ = [ _lenc,_ 0] _∈_ R<sup>_n_+1</sup> . 

We find that _v_ and _l_ belong to tangent space at the hyperboloid origin **O** as Eq.4 is satisfied: _<_ **O** _, v>L_ = 0 and _<_ **O** _, l>L_ = 0. Therefore, we parameterize only the spatial components of the Lorentz model ( _venc_ = _vspace_ and _lenc_ = _lspace_ ). We can simplify the exponential map in Eq.5 through the above parameterization approach, with the formula given as follows: 


The Lorentzian norm of vector _v_ and _l_ simplifies to the Euclidean norm of its spatial components, and can therefore be reduced to: 


For the traditional CLIP contrastive loss, we incorporate an entailment loss to enhance the structural relationships between text and images. _ytime_ and _xtime_ are calculated using Eq.3. To this end, we further impose an entailment cone constraint in the hyperbolic space to model such hierarchical dependency. This cone is defined by the half-aperture: 


where a constant _K_ represents boundary conditions near the origin. We now aim to identify and penalize when the paired image embedding _y_ lies outside the entailment cone. We measure the exterio angle _ext_ ( _x, y_ ) = _π −_ ∠ _Oxy_ : 

## **2.2. Soft MoE for Multimodal Fusion** 

To better capture fine-grained image-text semantics, we enhance the Q-Former by replacing its feed-forward layers with a soft Mixture-of-Experts (softMOE) module. The Q-Former first encodes visual and textual features through self- and cross-attention, producing fused query tokens _{qi}_<sup>_N_</sup> _i_ =1<sup>, which</sup> are then processed by the MoE. 

The MoE consists of _M_ expert networks _{Em}_<sup>_M_</sup> _m_ =1<sup>and</sup> a gating network _G_ ( _·_ ). For each token _qi_ , the gating network outputs logits _gi ∈_ R<sup>_M_</sup> , normalized via softmax as: 


where the token is updated by: 


This soft routing lets each token access all experts while focusing on the most relevant ones. 

We insert the softMOE into each Transformer block by replacing the feed-forward layer: attention outputs are normalized, processed by MoE, and merged via residual connections. To encourage balanced expert usage, we add a loadbalancing loss: 


where _nm_ is the number of tokens routed to expert _m_ . The final training objective is: 


where _β_ controls the regularization strength. This design improves semantic alignment while maintaining efficiency. 

## **3. EXPERIMENTS** 


If the exterior angle is smaller than the aperture, it indicates that the constraint relationship between _x_ and _y_ is satisfied; otherwise, the angular difference needs to be reduced through a loss function: 


Finally, the overall objective is: 


where _λ_ = 0.1 is a balancing coefficient controlling the relative importance of the two losses. 

**Datasets.** We used the LIBERO [19] benchmark for evaluation. Specifically, we utilized four datasets: Spatial, Object, Goal, and LONG. To validate the generalization capability of our model, we reconstructed a new dataset (Gen) for training and validation to examine its generalizability. 

**Implementation Details.** We adopt Dita [21] as the backbone network. Training is conducted for 80k steps using the Adam optimizer with a learning rate of 1 _×_ 10<sup>_−_4</sup> . The hyperbolic curvature is set to 0 _._ 1, and the Mixture-ofExperts (MoE) module includes 6 experts. The model is trained with a batch size of 64 and input image resolutions of 256 _×_ 256 pixels. For trajectory modeling, we set the trajectory length (traj ~~l~~ ength) to 11 and the trajectory dimension (trajectory ~~d~~ im) to 7. At each step, the model predicts 10 

**Table 1** . Comparison of task-level accuracy of existing meth- <u>ods and our HMVLA model on LIBERO benchmark.</u> 

|Method|Spatial|Object|Goal|LONG|Average|
|---|---|---|---|---|---|
|DP [22]|78%|92%|68%|50%|72%|
|Octo [23]|79%|86%|85%|50%|75%|
|Tra-MoE [24]|69%|77%|88%|31%|66%|
|CoT-VLA [25]|87%|91%|87%|69%|81%|
|Dita [21]|84%|96%|85%|63%|82%|
|HMVLA**(ours)**|90%|96%|89%|69%|86%|


**Fig. 3** . Comparison of HMVLA and Baseline Models on Spatial, Object, Goal, and Our Constructed Datasets. future actions. All experiments are performed on an NVIDIA H200 GPU. 

**Comparison with Advanced Methods.** As shown in Table 1 and Fig. 3, we conducted comparative experiments between our proposed method and state-of-the-art approaches. 

As shown in Table 1 and Fig. 3, we conducted comparative experiments between the proposed method and stateof-the-art approaches. Table 1 includes comparisons with DP [22], Octo [23], Tra-MoE [24], CoT-VLA [25], and Dita [21] algorithms, where our framework demonstrates superior performance. Figure 3 further validates the generalization capability of our model, with comparative models including OpenVLA [14], DFP-OTTER [26], OTTER [26], and Dita [21]. And Fig. 4 shows the grasping process of our HMVLA model. 

Our method not only achieves the best performance on the benchmark dataset but also exhibits breakthrough improvements on the generalization validation set compared to other models. Compared to other algorithms, our model leverages the inherent tree-like architecture of hyperbolic space to naturally align text and image embeddings, while the softMoE mechanism is responsible for modeling specific semantic components within instructions, thereby enhancing the decomposition and generalization capabilities of cross-modal semantics. 

**Ablation Study.** As shown in Fig. 5, _Lent_ constrains hyperbolic space during modality fusion, while MoE denotes that different experts can be scheduled under the routing 


**Fig. 4** . The HMVLA model’s grasping process on LIBERO benchmark. 


**Fig. 5** . Ablation Experiments Evaluating Hyperbolic, MoE, and Cross-Attention. 

mechanism. We also tested replacing FiLM with CrossAttention. We observe that introducing hyperbolic space into Dita [21] significantly improves task success, especially for complex instructions where the original Dita model struggled. This demonstrates that hyperbolic space effectively captures hierarchical structure, enhancing multimodal fusion. In addition, the routing ability of MoE helps avoid overfitting to a single fused representation, while FiLM provides more stable and balanced modality conditioning than Cross-Attention. Together, these results confirm that each component contributes to more robust semantic-to-action alignment. 

## **4. CONCLUSION** 

In this paper, we propose HMVLA, a novel Vision-LanguageAction (VLA) model that leverages hyperbolic space representation and a sparsely-gated Mixture-of-Experts (MoE) mechanism to enhance semantic alignment between vision and language for robotic control. By embedding multimodal features into a hyperbolic space, our model effectively captures the inherent hierarchical relationships within image-text data. Furthermore, the incorporation of MoE improves the decomposition and modeling of fine-grained semantic elements, leading to superior multimodal fusion. Experimental results on the LIBERO benchmark and our dataset demonstrate that HMVLA not only outperforms existing state-of-the-art methods in task accuracy but also exhibits strong generalization ability to novel instructions and previously unseen objects. 

## **5. ACKNOWLEDGEMENT** 

This work was supported by the National Natural Science Foundation of China (Grant No. 62277011), National Key Research and Development Program of China (Grant No. GG-2024-01-02), Project of Chongqing MEITC (Grant No. YJX-2025001001009) and Open Research Fund from Guangdong Laboratory of Artificial Intelligence and Digital Economy (SZ) (Grant No. GML-KF-24-18). 

### **6. REFERENCES** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, et al., “Gpt-4 technical report,” _arXiv preprint arXiv:2303.08774_ , 2023. 

- [2] Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, et al., “The llama 3 herd of models,” _CoRR_ , 2024. 

- [3] Shibo Sun, Xue Li, Donglin Di, Mingjie Wei, Lanshun Nie, Wei-Nan Zhang, Dechen Zhan, Yang Song, and Lei Fan, “Llapa: A vision-language model framework for counterfactual-aware procedural planning,” in _Proceedings of the 33rd ACM International Conference on Multimedia_ , 2025, pp. 5020–5029. 

- [4] Guoxin Zang, Xue Li, Donglin Di, Lanshun Nie, Dechen Zhan, Yang Song, and Lei Fan, “Sage: A visual language model for anomaly detection via fact enhancement and entropy-aware alignment,” in _Proceedings of the 33rd ACM International Conference on Multimedia_ , 2025, pp. 5030–5039. 

- [5] Anthony Brohan, Noah Brown, Justice Carbajal, et al., “Rt1: Robotics transformer for real-world control at scale,” _arXiv preprint arXiv:2212.06817_ , 2022. 

- [6] Suneel Belkhale, Tianli Ding, Ted Xiao, et al., “Rt-h: Action hierarchies using language,” _arXiv preprint arXiv:2403.01823_ , 2024. 

- [7] Zhongyi Zhou, Yichen Zhu, Junjie Wen, et al., “Visionlanguage-action model with open-world embodied reasoning from pretrained knowledge,” _arXiv preprint arXiv:2505.21906_ , 2025. 

- [8] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, et al., “3d-vla: a 3d vision-language-action generative world model,” in _Proceedings of the 41st ICML_ , 2024, pp. 61229–61245. 

- [9] Kevin Black, Noah Brown, Danny Driess, et al., “ _π_ 0: A Vision-Language-Action Flow Model for General Robot Control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [10] Physical Intelligence, Kevin Black, Noah Brown, et al., “ _π_ 0 _._ 5: A Vision-Language-Action Model with Open-World Generalization,” _arXiv preprint arXiv:2504.16054_ , 2025. 

- [11] Yueen Ma, Zixing Song, Yuzheng Zhuang, et al., “A survey on vision-language-action models for embodied ai,” _arXiv preprint arXiv:2405.14093_ , 2024. 

   - [14] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, et al., “Openvla: An open-source vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 

   - [15] Alec Radford, Jong Wook Kim, Chris Hallacy, et al., “Learning transferable visual models from natural language supervision,” in _International conference on machine learning_ . PMLR, 2021, pp. 8748–8763. 

   - [16] Zhengran Zeng, Hanzhuo Tan, Haotian Zhang, et al., “An extensive study on pre-trained models for program understanding and generation,” in _Proceedings of the 31st ACM SIGSOFT ISSTA_ , 2022, pp. 39–51. 

   - [17] Shyan S Chen and Leon Greenberg, “Hyperbolic spaces,” in _Contributions to analysis_ , pp. 49–87. Elsevier, 1974. 

   - [18] Karan Desai, Maximilian Nickel, Tanmay Rajpurohit, et al., “Hyperbolic image-text representations,” in _International Conference on Machine Learning_ . PMLR, 2023, pp. 7694–7731. 

   - [19] Bo Liu, Yifeng Zhu, Chongkai Gao, et al., “Libero: Benchmarking knowledge transfer for lifelong robot learning,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 44776–44791, 2023. 

   - [20] Albert Einstein et al., “Zur elektrodynamik bewegter k¨orper,” _Annalen der physik_ , vol. 17, no. 10, pp. 891–921, 1905. 

   - [21] Zhi Hou, Tianyi Zhang, Yuwen Xiong, et al., “Dita: Scaling diffusion transformer for generalist vision-language-action policy,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2025. 

   - [22] Cheng Chi, Siyuan Feng, Yilun Du, et al., “Diffusion policy: Visuomotor policy learning via action diffusion,” in _Robotics: Science and Systems_ , 2023. 

   - [23] Octo Model Team, Dibya Ghosh, Homer Walke, et al., “Octo: An open-source generalist robot policy,” _arXiv preprint arXiv:2405.12213_ , 2024. 

   - [24] Jiange Yang, Haoyi Zhu, Yating Wang, et al., “Tra-moe: Learning trajectory prediction model from multiple domains for adaptive policy conditioning,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 6960–6970. 

   - [25] Qingqing Zhao, Yao Lu, Moo Jin Kim, et al., “Cot-vla: Visual chain-of-thought reasoning for vision-language-action models,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 1702–1713. 

   - [26] Huang Huang, Fangchen Liu, Letian Fu, et al., “OTTER: A vision-language-action model with text-aware visual feature extraction,” in _Forty-second International Conference on Machine Learning_ , 2025. 

- [12] Jingyi Zhang, Jiaxing Huang, Sheng Jin, et al., “Visionlanguage models for vision tasks: A survey,” _IEEE TPAMI_ , vol. 46, no. 8, pp. 5625–5644, 2024. 

- [13] Brianna Zitkovich, Tianhe Yu, Sichun Xu, et al., “Rt-2: Visionlanguage-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 

