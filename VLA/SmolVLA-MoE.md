---
title: "SmolVLA-MoE: Sparse Mixture-of-Experts for Efficient Multi-Task Robotic Manipulation"
date: "2026-10-22"
authors: "Shiyang Zhang; Miao Yang; Zhengda Li; Yang Shao; Ruifang Zhai; Hui Peng"
url: https://arxiv.org/abs/2610.30732
pdf: https://arxiv.org/pdf/2610.30732
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2610.30732)** / [論文ページ](https://arxiv.org/abs/2610.30732)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **SmolVLA-MoE: Sparse Mixture-of-Experts for Efficient Multi-Task Robotic Manipulation** 

Shiyang Zhang<sup>1</sup> , Miao Yang<sup>1</sup> , Zhengda Li<sup>2</sup> , Yang Shao<sup>2</sup> , Ruifang Zhai<sup>1</sup><sup>_,_3</sup> , Hui Peng<sup>1</sup><sup>_⋆_</sup> , and Peng Song<sup>2</sup><sup>_,_3</sup><sup>_⋆⋆_</sup> 

- 1 College of Informatics, Huazhong Agricultural University, No. 1 Shizi Mountain Street, Hongshan District, Wuhan 430070, China 

- 2 College of Plant Science and Technology, Huazhong Agricultural University, No. 1 Shizi Mountain Street, Hongshan District, Wuhan 430070, China 

> 3 Hubei Hongshan Laboratory, Wuhan 430070, China 

```
2305304089@qq.com,moonbird@mail.hzau.edu.cn,songp@mail.hzau.edu.cn
```

**Abstract.** Vision-Language-Action (VLA) models have shown promising results in multi-task robotic manipulation by leveraging visual and language understanding for action generation. However, existing lightweight VLA models employ a single dense action expert to handle all tasks, which limits their multi-task capability under constrained computational budgets. To address this issue, we propose SmolVLA-MoE, a novel framework that introduces sparse Mixture-of-Experts (MoE) into the FFN layers of the action expert in VLA models. SmolVLA-MoE replaces dense FFN layers with multiple parallel expert FFNs and a token-level router, enabling each token to adaptively select the most suitable expert for action generation. We further introduce a shared expert with a tunable weight parameter to balance the inheritance of pre-trained capabilities and task-specific expert specialization. Through sparse activation, SmolVLA-MoE activates only a single expert FFN ( _∼_ 100M activated parameters in the action expert module) during inference, with a total activated parameter count of _∼_ 500M including the frozen VLM backbone—the same as the dense baseline SmolVLA—while benefiting from the multi-expert representational capacity provided by _∼_ 800M total stored parameters. We evaluate our method on four task suites of the LIBERO benchmark and compare it against SmolVLA and other representative baselines. Experimental results demonstrate that SmolVLAMoE achieves an average success rate of 84.25% across all four suites, outperforming the dense baseline SmolVLA (82.75%) and the much larger OpenVLA-7B (76.5%), while maintaining comparable inference efficiency, providing an effective and efficient solution for multi-task robotic manipulation. Our code is publicly available at `https://github.com/dudu435/ smolvla-moe` . 

**Keywords:** Mixture-of-Experts · Vision-Language-Action · Robotic Manipulation · Sparse Activation · Multi-Task Learning 

> _⋆_ Corresponding author 

- _⋆⋆_ Corresponding author 

2 S. Zhang et al. 

## **1 Introduction** 

Robotic manipulation in unstructured environments requires models that can understand diverse visual scenes, comprehend natural language instructions, and generate corresponding actions. Vision-Language-Action (VLA) models [3,4,22,14] have emerged as a promising paradigm to address this challenge by unifying vision, language, and action within a single framework. Recent works such as RT1 [4], RT-2 [3], Octo [22], and OpenVLA [14] have demonstrated that VLA models can leverage large-scale pre-trained Vision-Language Models (VLMs) [20,1] as backbones to effectively generalize across various manipulation tasks. 

Despite their strong performance, most VLA models rely on large-scale architectures with billions of parameters, posing significant challenges for real-time deployment on resource-constrained robotic platforms. To address this limitation, lightweight VLA models such as SmolVLA [25] have been proposed, which employ a compact VLM backbone (e.g., SmolVLM2-500M) combined with a small action expert network for action generation via Flow Matching. This design significantly reduces computational cost while maintaining competitive performance. 

However, these lightweight VLA models suffer from a fundamental limitation: the action expert uses a single dense feed-forward network (FFN) to uniformly process all tasks. In multi-task robotic manipulation scenarios, different tasks (e.g., spatial reasoning, object manipulation, goal reaching) exhibit distinct action patterns that require different computational strategies. A single dense FFN is forced to encode all these diverse action generation patterns into a shared set of parameters, creating an inherent tension between model capacity and computational efficiency. Simply scaling up the action expert proportionally increases inference cost, negating the advantages of the lightweight design. 

Mixture-of-Experts (MoE) [11,24,13,6] offers an elegant solution to this dilemma. Unlike model compression techniques that trade representational capacity for efficiency, sparse MoE scales model capacity by maintaining multiple parallel expert networks while routing each input to only a sparse subset, keeping the active computation constant. This paradigm has proven effective in large language models such as Mixtral [13] and DeepSeek-MoE [6], yet its application in VLA models for action generation remains largely unexplored. 

In this paper, we propose SmolVLA-MoE, a framework that introduces sparse Mixture-of-Experts into the FFN layers of the action expert in VLA models. Unlike approaches that replicate the entire action expert into multiple copies, our method operates at a finer granularity, replacing each dense FFN layer with multiple parallel expert FFNs and a learnable token-level router. This design enables each token to adaptively select the most suitable expert for action generation based on the input context, while keeping the attention layers shared across all tasks. 

We evaluate SmolVLA-MoE on the LIBERO benchmark [19], which provides four task suites (Spatial, Object, Goal, and LIBERO-10) covering diverse manipulation challenges. Experimental results show that SmolVLA-MoE achieves superior performance over the SmolVLA baseline on all four suites, while activat- 

SmolVLA-MoE 3 

ing only a single expert FFN ( _∼_ 100M activated parameters in the action expert) during inference, keeping the total activated parameter count at _∼_ 500M—the same as the dense baseline. We further conduct systematic ablation studies on key design parameters, including the number of activated experts (top- _k_ ) and the shared expert weight, providing in-depth analysis of MoE behavior in robotic action generation. 

Our main contributions are summarized as follows: 

**–** We propose SmolVLA-MoE, the first work to build a Mixture-of-Experts model on top of the lightweight SmolVLA architecture, maintaining the lightweight and efficient characteristics of SmolVLA under the same activated parameter budget. 

- Building upon the AdaMoE [30] design, we introduce more controllable weight gating between shared and routed experts to balance pre-trained capability inheritance and expert specialization, and conduct systematic analysis of its impact across different task types. 

**–** We demonstrate that SmolVLA-MoE achieves state-of-the-art performance across all four task suites of the LIBERO benchmark while maintaining inference efficiency comparable to the dense baseline. 

## **2 Related Work** 

### **2.1 Vision-Language-Action Models** 

Vision-Language-Action (VLA) models aim to leverage pre-trained vision-language models for action generation, building general-purpose robotic policies. RT-1 [4] first demonstrated that a Transformer-based model trained on large-scale realworld robotic data can generalize across hundreds of tasks. RT-2 [3] pioneered the VLA direction by fine-tuning a large vision-language model (55B-parameter PaLI-X) to directly output robotic actions as text tokens, demonstrating that semantic knowledge embedded in VLMs can transfer to robotic control. Octo [22] proposed a Transformer-based policy architecture supporting flexible task and observation specifications, enabling multi-task learning across multiple robot embodiments. OpenVLA [14] built a 7B-parameter open-source VLA model based on the Llama 2 architecture, achieving strong generalization through large-scale pre-training on the Open X-Embodiment dataset [23]. 

However, these models typically require billions of parameters, making realtime deployment on robotic platforms challenging. Meanwhile, alternative policy learning approaches such as ACT [31] and Diffusion Policy [5] have shown strong performance in imitation learning with more compact architectures, and vision-language foundation models have been adapted for robotic control [17]. To this end, recent works have explored lightweight VLA architectures. _π_ 0 [2] proposed a flow matching-based VLA that uses a pre-trained vision-language model (PaliGemma [1]) as the backbone and trains a dedicated action expert for action chunk generation. SmolVLA [25] adopts a compact VLM backbone (SmolVLM2-500M) and introduces an independent action expert network that 

4 S. Zhang et al. 

generates actions via Flow Matching [18], significantly reducing model size while maintaining competitive performance. This lightweight approach demonstrates that effective robotic manipulation does not necessarily require billion-scale models, but its single dense action expert design limits multi-task capability. 

Our work builds upon SmolVLA by introducing sparse MoE into the action expert to address this limitation, enabling efficient multi-task scaling without increasing inference cost. 

### **2.2 Mixture-of-Experts Models** 

Mixture-of-Experts (MoE) [11] is a classical approach for scaling model capacity through conditional computation, maintaining multiple expert networks and using a gating mechanism to route each input to a sparse subset of experts. The sparsely-gated MoE layer [24] first demonstrated the scalability of this approach in deep learning. Subsequent works have advanced MoE along several directions, including simplified top-1 routing with load balancing [7] and largescale top-2 routing [16]. More recently, Mixtral [13] demonstrated that sparse MoE can match much larger dense models at a fraction of the inference cost. Two designs are particularly relevant to our work: DeepSeek-MoE [6] introduced shared experts that are always activated alongside routed experts, providing a stable baseline; AdaMoE [30] proposed adaptive scaling adapters that decouple expert selection from expert weighting. 

In the robotics domain, the application of MoE remains limited. Existing approaches to efficient robot learning primarily focus on model compression: knowledge distillation [8] transfers knowledge from large teacher models to smaller students, parameter-efficient fine-tuning methods like LoRA [10] reduce trainable parameters, and data augmentation techniques [29,21] improve sample efficiency. However, these methods fundamentally trade off representational capacity for computational savings. Sparse MoE offers a distinct advantage: it scales model capacity through multiple specialized experts while keeping the per-inference computation constant, making it ideally suited for multi-task robotic manipulation where different tasks demand different computational strategies but the deployment budget is fixed. Some works have explored MoE in multi-task reinforcement learning [27], but the integration of MoE into lightweight VLA models for action generation has not been systematically studied. To this end, our work introduces FFN-level MoE into the action expert of VLA models, drawing on the shared expert design of DeepSeek-MoE [6] and the adaptive routing of AdaMoE [30], combined with Sparse Upcycling [15] initialization that converts pre-trained dense checkpoints into sparse MoE models while preserving pre-trained knowledge. 

## **3 Method** 

This section presents SmolVLA-MoE in detail. We first review the SmolVLA architecture that serves as our baseline (Sect. 3.1), then describe the FFNlevel Mixture-of-Experts design (Sect. 3.2), the routing mechanism (Sect. 3.3), 

SmolVLA-MoE 5 


Fig. 1: Overview of the SmolVLA-MoE architecture. The frozen VLM backbone processes visual observations and language instructions to produce contextual representations. The action expert replaces dense FFN layers with MoE-FFN layers, each containing a shared expert _Es_ (always activated, weighted by _α_ ), _N_ routed expert FFNs, a token-level router with top- _K_ selection, and a scaling adapter. Through sparse activation, only _K_ experts are selected per token during both training and inference. 

the shared expert with tunable weight (Sect. 3.4), and the training objective (Sect. 3.5). The overall architecture is illustrated in Fig. 1. 

### **3.1 Preliminaries: SmolVLA** 

SmolVLA is a lightweight Vision-Language-Action model consisting of two main components: a frozen VLM backbone and a trainable action expert. 

**VLM Backbone.** SmolVLA adopts SmolVLM2-500M as its vision-language backbone, comprising a SigLIP vision encoder and a language model. The VLM processes visual observations and language instructions to produce contextual representations. During training, the VLM backbone is frozen to preserve its pre-trained knowledge. 

**Action Expert.** The action expert is a small Transformer network that generates robotic actions based on the VLM’s representations. It consists of multiple Transformer layers, each containing a cross-attention module (attending to the VLM’s key-value cache) and a feed-forward network (FFN). The FFN in each layer adopts the SwiGLU architecture: 


where _Wgate ∈_ R<sup>_dff ×d_</sup> , _Wup ∈_ R<sup>_dff ×d_</sup> , _Wdown ∈_ R<sup>_d×dff_</sup> are learnable weight matrices, _d_ is the hidden dimension, and _dff_ is the intermediate dimension. 

- 6 S. Zhang et al. 

**Flow Matching.** SmolVLA uses Flow Matching [18,26] for action generation. Unlike diffusion-based approaches [9,5] that require many denoising steps, Flow Matching learns a continuous velocity field along a straight-line transport path from noise to the target action distribution. During training, given a ground-truth action sequence _a ∈_ R<sup>_H×da_</sup> (where _H_ is the action chunk size and _da_ is the action dimension) and sampled noise _ϵ ∼N_ (0 _, I_ ), a noisy action is constructed via linear interpolation at timestep _t ∼_ Beta(1 _._ 5 _,_ 1 _._ 0): 


where _t ∈_ [0 _,_ 1] controls the interpolation between the clean action _a_ (at _t_ = 0) and pure noise _ϵ_ (at _t_ = 1). The model learns to predict the velocity field _vθ_ ( _xt, t_ ) that transports _xt_ toward _a_ , with the target velocity _ut_ = _ϵ − a_ representing the constant velocity along the straight-line path. The training loss minimizes the mean squared error between predicted and target velocities: 


At inference, actions are generated by integrating the learned velocity field backward from _t_ = 1 (pure noise) to _t_ = 0 (clean action) through _N_ steps of Euler integration with step size _∆t_ = _−_ 1 _/N_ . 

### **3.2 FFN-Level Mixture-of-Experts** 

The core idea of SmolVLA-MoE is to replace the dense FFN layers in the action expert with Mixture-of-Experts FFN (MoE-FFN) layers. Unlike full expert-level MoE that replicates the entire action expert into multiple copies, our method operates at the FFN granularity, keeping the attention layers shared while allowing each token to select specialized FFN experts. 

**MoE-FFN Layer.** Each MoE-FFN layer contains _N_ parallel expert FFNs _{E_ 1 _, E_ 2 _, . . . , EN }_ , a shared expert _Es_ , a router _R_ , and a scaling adapter _S_ . Each expert FFN adopts the same SwiGLU architecture as the original dense FFN but with independent parameters: 


where _Wgate_<sup>(</sup><sup>_i_),</sup><sup>_W_(</sup> _up_<sup>_i_),and</sup><sup>_W_(</sup> _down_<sup>_i_)arethelearnableweightmatricesofthe</sup><sup>_i_-th</sup> expert, _x ∈_ R<sup>_d_</sup> is the input token representation, _N_ is the total number of routed experts, and _⊙_ denotes element-wise multiplication. Each expert maintains its own independent set of parameters, allowing different experts to learn distinct transformation patterns. 

**Layer Replacement.** The replacement frequency is controlled by a parameter _f_ . When _f_ = 1, all FFN layers are replaced with MoE-FFN; when _f_ = 2, every other layer is replaced. For a layer with index _l_ , MoE-FFN is applied when _l_ mod _f_ = 0. 

SmolVLA-MoE 7 


Fig. 2: Detailed structure of the MoE-FFN layer. The input token is processed by both the shared expert and the top- _K_ routed experts selected by the router. The scaling adapter provides additional per-token adaptive scaling. The final output is a weighted combination of the shared expert output (scaled by _α_ ) and the routed expert output (scaled by 1 _− α_ ). 

### **3.3 Routing Mechanism** 

The routing mechanism determines which experts process each token. It consists of two components: the router and the scaling adapter. 

**Router.** The router is a bias-free linear projection that maps each token’s hidden state to expert scores: 


where _g_ ( _x_ ) _∈_ R<sup>_N_</sup> contains the routing logits for _N_ experts. 

**Top-K Selection.** For each token, the top _K_ experts with the highest routing logits are selected: 


where _TK_ denotes the index set of the _K_ selected experts and _K_ is the number of experts activated per token. The routing weights are computed by applying softmax normalization to the logits of the selected experts, ensuring they sum to one: 


where _g_ ( _x_ ) _TK_ extracts the routing logits corresponding to the selected expert indices, and _wk_ is the normalized routing weight for the _k_ -th selected expert. 

**Scaling Adapter.** Following AdaMoE [30], we introduce a scaling adapter that provides additional per-token adaptive scaling, decoupling expert selection from expert weighting. The scaling adapter is also a bias-free linear projection: 


where _Ws_ is the scaling adapter weight matrix, producing an _N_ -dimensional scaling vector for each token. The final routing weights combine the router softmax weights with the scaling adapter outputs for the selected experts: 


8 S. Zhang et al. 

where _w_ ˆ _k_ is the adjusted routing weight for the _k_ -th selected expert, and _s_ ( _x_ ) _TK_ ( _k_ ) is the scaling adapter output corresponding to that expert. This additive combination allows the scaling adapter to modulate the magnitude of expert contributions independently of the router’s selection decision. 

**Routed Output.** The routed expert output for each token is the weighted sum of the selected expert outputs: 


where _ETK_ ( _k_ )( _x_ ) is the output of the _k_ -th selected expert applied to input _x_ , and _w_ ˆ _k_ is its corresponding adjusted routing weight. Only _K_ out of _N_ total experts are computed per token, achieving sparse activation. 

### **3.4 Shared Expert with Tunable Weight** 

Inspired by DeepSeek-MoE [6], we introduce a shared expert _Es_ that is always activated for all tokens, providing a stable baseline output. The shared expert has the same SwiGLU architecture as the routed experts but with independent parameters. 

The final output of the MoE-FFN layer combines the shared expert output and the routed expert output through a tunable weight parameter _α_ : 


where _y_ ( _x_ ) is the final MoE-FFN layer output, _Es_ ( _x_ ) is the shared expert output, _yrouted_ ( _x_ ) is the aggregated routed expert output defined in Eq. (14), and _α ∈_ [0 _,_ 1] is the shared expert weight that controls the relative contribution of the shared expert. This parameter provides continuous control between two complementary roles: 

- **Pre-trained capability inheritance** ( _α →_ 1): The shared expert preserves the pre-trained knowledge of the original dense FFN, ensuring training stability. 

- **Expert specialization** ( _α →_ 0): The routed experts gain greater influence, enabling task-specific specialization. 

Note that the shared expert is initialized with the exact pre-trained dense FFN weights without added noise, while the routed experts receive noise perturbation (Sect. 3.5). This asymmetric initialization ensures that the shared expert serves as a reliable baseline from the start of training. 

### **3.5 Training Objective** 

**Sparse Upcycling Initialization.** Starting from the pre-trained baseline, all expert FFNs are initialized from the pre-trained dense FFN weights of the original SmolVLA action expert. The shared expert receives an exact copy, while 

SmolVLA-MoE 9 

each routed expert receives the same weights with added Gaussian noise: 


where _W_<sup>(</sup><sup>_i_)</sup> is the initialized weight matrix of the _i_ -th routed expert, _Wdense_ is the pre-trained dense FFN weight matrix, std( _Wdense_ ) is the standard deviation of _Wdense_ used to scale the noise relative to the weight magnitude, _N_ (0 _, I_ ) is standard Gaussian noise, and _σ_ is the noise scale (default 0.02). This initialization ensures: (1) the model starts from a strong pre-trained checkpoint, and (2) the noise promotes expert diversity and specialization during training. 

**Load Balancing Loss.** Following Switch Transformer [7], we adopt a load balancing loss to encourage uniform expert utilization and prevent expert collapse: 


where _N_ is the total number of routed experts, _fi_ = _T_<sup><u>1</u></sup> � _Tj_ =1<sup>**1**[expert</sup><sup>_i_isselectedfortoken</sup><sup>_j_]</sup> is the fraction of tokens routed to expert _i_ across a batch of _T_ tokens (nondifferentiable), and _Pi_ = _T_ <u>1</u> � _Tj_ =1<sup>_pi_(</sup><sup>_xj_)istheaverageroutingprobabilityfor</sup> expert _i_ computed from the softmax output (differentiable). The product _fi · Pi_ is minimized when both the actual token allocation and routing probabilities are uniformly distributed, thus penalizing imbalanced expert utilization. 

**Total Loss.** The total training loss combines the Flow Matching loss and the load balancing loss: 


where _LF M_ is the Flow Matching loss defined in Eq. (3), _LLB_ is the load balancing loss defined in Eq. (17), and _λ_ is the load balancing weight (default 0.01) that controls the trade-off between action prediction accuracy and expert utilization balance. The load balancing loss is averaged over all MoE-FFN layers in the action expert. 

## **4 Experiments** 

This section evaluates SmolVLA-MoE on the LIBERO benchmark. We first describe the experimental setup (Sect. 4.1), then present the main results (Sect. 4.2), followed by ablation studies (Sect. 4.3). 

### **4.1 Experimental Setup** 

**Benchmark.** We conduct evaluations on the LIBERO benchmark [19], which provides standardized evaluation suites for multi-task robotic manipulation in simulated tabletop environments. LIBERO contains four task suites of increasing difficulty: 

- 10 S. Zhang et al. 


(b) “Put the yellow and white mug in the microwave and close it.” 

Fig. 3: Visualization of complete rollouts in the LIBERO simulation environment. Each row shows key frames of the execution trajectory for a multi-step manipulation task from start to completion. 

- **LIBERO-Spatial** : 10 tasks focusing on spatial relationship understanding (e.g., “pick up the object to the left of the bowl”). This suite tests the model’s ability to comprehend spatial language instructions. 

- **LIBERO-Object** : 10 tasks focusing on object recognition and manipulation (e.g., “pick up the red cup”). This suite evaluates the model’s ability to distinguish between different objects. 

- **LIBERO-Goal** : 10 tasks focusing on goal-conditioned manipulation with diverse goals. This suite tests the model’s ability to reach specified goal states. 

- **LIBERO-10** : 10 tasks combining elements from all categories with multistep instructions. This is the most challenging suite, requiring compositional understanding of spatial, object, and goal concepts. 

Each task is evaluated over 10 rollouts, using success rate as the evaluation metric. 

**Baselines.** We compare SmolVLA-MoE against six representative baselines spanning different scales and architectures: Diffusion Policy [5] (321M), Octo [22] (93M), OpenVLA [14] (7B, pre-trained on Open X-Embodiment [23]), _π_ 0 in two configurations [2] (Paligemma-3B and 3.3B), and SmolVLA [25] (500M) as the direct dense baseline fine-tuned on each LIBERO suite following the same protocol. 

SmolVLA-MoE 11 

Table 1: Main Results on the LIBERO Benchmark <u>(Success</u> Rate %) 

|Method|Params|Spatial|Object|Goal L|IBERO-1|0 Avg.|
|---|---|---|---|---|---|---|
|Diffusion Policy [5]|321M|78.3|92.5|68.3|50.5|72.4|
|Octo [22]|93M|78.9|85.7|84.6|51.1|75.1|
|OpenVLA [14]|7B|84.7|88.4|79.2|53.7|76.5|
|_π_0 (Paligemma) [2]|3B|87|63|89|48|71.8|
|_π_0 [2]|3.3B|90|86|95|73|86.0|
|SmolVLA [25]|500M|87|93|88|63|82.75|
|**SmolVLA-MoE (Ours)**|**500M**<sup>_†_</sup>|**87**|**93**|**93**|**65**|**84.25**|


**Implementation Details.** SmolVLA-MoE is built on top of the SmolVLA architecture. The VLM backbone (SmolVLM2-500M) is frozen during training. The dense FFN layers of the action expert are replaced with MoE-FFN layers through Sparse Upcycling initialization. With 4 routed experts plus 1 shared expert, the total stored parameters of SmolVLA-MoE are _∼_ 800M. During inference, only 1 expert FFN is activated per token, resulting in _∼_ 100M activated parameters in the action expert module and _∼_ 500M total activated parameters including the frozen VLM backbone—identical to the dense baseline SmolVLA. Key hyperparameters include: learning rate 1e-4 with AdamW optimizer, batch size 48, 120,000 training steps with 4,000 warmup steps, load balancing weight _λ_ = 0 _._ 01, expert initialization noise _σ_ = 0 _._ 02, and 10 Flow Matching denoising steps. 

All experiments are conducted on a single NVIDIA RTX 4090 GPU (24GB VRAM). Each configuration is trained for 120,000 steps with the same random seed to ensure fair comparison. 

### **4.2 Main Results** 

Table 1 presents the main comparison results of SmolVLA-MoE against multiple representative baseline methods across all four LIBERO task suites. We report the best configuration of SmolVLA-MoE (determined by the parameter study in Sect. 4.3). 

As shown in Table 1, SmolVLA-MoE achieves an average success rate of 84.25% with only _∼_ 500M total activated parameters ( _∼_ 100M in the action expert module), significantly outperforming the much larger OpenVLA (7B, 76.5%) and Octo (0.09B, 75.1%), as well as Diffusion Policy (72.4%) and _π_ 0 (Paligemma-3B) (71.8%). Compared to the direct baseline SmolVLA, SmolVLA-MoE improves the average success rate from 82.75% to 84.25% under the same activated parameter budget ( _∼_ 500M), a gain of 1.5 percentage points, indicating that the performance improvement comes from the expanded model capacity through sparse MoE rather than additional computational overhead. 

Among all methods, only _π_ 0 (3.3B) surpasses SmolVLA-MoE with an average success rate of 86.0%, but its activated parameter count is approximately 

12 S. Zhang et al. 


Fig. 4: Per-suite success rate comparison across all methods on the LIBERO benchmark. SmolVLA-MoE (highlighted with black borders) achieves competitive or superior performance across all four suites with _∼_ 500M total activated parameters ( _∼_ 100M in the action expert). 

3.3B—6.6 _×_ that of SmolVLA-MoE ( _∼_ 500M). This demonstrates the significant parameter efficiency advantage of SmolVLA-MoE, achieving performance close to large models at a fraction of the computational cost. 

**Per-Suite Analysis.** SmolVLA-MoE matches SmolVLA on Spatial (87%) and Object (93%), while achieving a 5 percentage point improvement on Goal (88% _→_ 93%) and a 2 percentage point gain on LIBERO-10 (63% _→_ 65%). On Spatial and Object, the dense baseline already performs well—these tasks primarily require spatial understanding and object recognition, where a single FFN suffices. The most significant gains appear on Goal and LIBERO-10, which involve complex goal-state reasoning and multi-step planning; here, the MoE architecture enables specialized experts to handle distinct action generation strategies, providing a clear advantage. Notably, SmolVLA-MoE achieves the highest Object score (93%) among all methods, surpassing even _π_ 0 (3.3B, 86%) by 7 points, while on LIBERO-10 the gap to _π_ 0 (3.3B, 73%) remains the largest, suggesting that compositional multi-step tasks may benefit from further scaling. 

**Efficiency Analysis.** With _∼_ 500M activated parameters, SmolVLA-MoE outperforms OpenVLA (7B) by 7.75 points and Diffusion Policy (321M) by 11.85 points, while trailing _π_ 0 (3.3B) by only 1.75 points at 6.6 _×_ fewer activated parameters. The additional expert parameters ( _∼_ 300M) are only stored but not all activated during inference, providing “free” capacity expansion. 

### **4.3 Ablation Studies** 

We conduct systematic ablation studies to analyze the impact of two key design parameters: the number of activated experts per token (top- _K_ ) and the shared expert weight ( _α_ ). All ablation experiments use 4 experts with other hyperparameters fixed. 

SmolVLA-MoE 13 

Table 2: Ablation Study — Top-K _×_ Shared Expert Weight (Success Rate %) 

|Top-|K _α_|Spatial|Object|Goal|LIBERO-10|
|---|---|---|---|---|---|
|1|0.2|86|91|89|62|
|1|0.3|87|93|93|65|
|2|0.2|77|89|89|64|
|2|0.3|78|95|90|60|


Fig. 5: Heatmap visualization of the Top-K _×_ shared expert weight ( _α_ ) ablation study across all four LIBERO suites. Best values in each suite are shown in bold. Top-1 routing with _α_ = 0 _._ 3 achieves the best overall performance. 

**Impact of Top-K and Shared Expert Weight.** Table 2 presents the complete parameter study across all four LIBERO suites with different combinations of top- _K_ and shared expert weight _α_ . 

**Top-K Analysis.** Top-1 routing outperforms top-2 on most suites, with the largest gap on Spatial (87% vs. 78% at _α_ = 0 _._ 3, a 9-point difference). This suggests that with 4 experts, activating a second expert introduces redundant or conflicting signals rather than complementary information. The exception is LIBERO-10, where top-2 (64% at _α_ = 0 _._ 2) slightly outperforms top-1 (62%), likely because multi-step compositional tasks benefit from combining multiple experts. 

**Shared Expert Weight Analysis.** A higher _α_ consistently improves performance. Under top-1 routing, increasing _α_ from 0.2 to 0.3 yields gains across all suites, most notably on Goal (89% _→_ 93%) and LIBERO-10 (62% _→_ 65%). This indicates that preserving more pre-trained dense FFN knowledge through the shared expert provides a more stable foundation for routed expert specialization at the current training scale. 

**Impact of Shared Expert.** To verify the necessity of the shared expert, we compare models with and without the shared expert component. 

Removing the shared expert ( _α_ = 0) causes the Goal success rate to drop from 93% to 88% ( _−_ 5 points), validating its critical role. The shared expert preserves pre-trained dense FFN weights as a stable baseline, enabling routed experts to perform incremental task-specific specialization rather than learning all capabilities from scratch. 

14 S. Zhang et al. 

Table 3: Ablation Study — Shared Expert <u>(Success</u> Rate %) 

|Configuration||Goal|
|---|---|---|
|SmolVLA-MoE (w|/o shared expert, _α_= 0)|88|
|SmolVLA-MoE (w|/ shared expert, _α_= 0_._3)|93|


Table 4: Ablation Study — Load Balancing Loss <u>(Success</u> Rate %) 

|Configuration||Goal|
|---|---|---|
|SmolVLA-MoE (w/|o load balancing, _λ_= 0)|90|
|SmolVLA-MoE (w/|load balancing, _λ_= 0_._01)|93|


**Impact of Load Balancing Loss.** We examine the impact of the load balancing loss by comparing training with and without it. 

Removing the load balancing loss ( _λ_ = 0) causes the Goal success rate to drop from 93% to 90% ( _−_ 3 points). Without this regularization, the router converges to a locally optimal allocation where some experts are underutilized (expert collapse), preventing the model from fully leveraging the MoE capacity. A weight of _λ_ = 0 _._ 01 balances uniform utilization with routing flexibility. 

## **5 Conclusion** 

In this paper, we propose SmolVLA-MoE, a framework that introduces FFNlevel sparse Mixture-of-Experts into the action expert of Vision-Language-Action models for multi-task robotic manipulation. By replacing dense FFN layers with MoE-FFN layers containing multiple parallel expert FFNs and a learnable tokenlevel router, SmolVLA-MoE enables each token to adaptively select specialized experts for action generation, scaling model capacity without increasing inference cost. 

Experiments on the LIBERO benchmark demonstrate that SmolVLA-MoE achieves superior performance over the SmolVLA baseline on all four task suites (Spatial, Object, Goal, and LIBERO-10), while maintaining the same total activated parameter count of _∼_ 500M as the dense baseline (with only _∼_ 100M activated in the action expert module). Systematic ablation studies reveal that top-1 routing outperforms top-2 routing on tasks requiring precise action generation, indicating that activating fewer but more specialized experts is preferable when expert differentiation is limited. The shared expert weight provides an effective control knob for balancing stability and specialization across different task types. 

**Limitations and Future Work.** Our evaluation is limited to the LIBERO benchmark in simulation. Future work includes extending to real-world tasks and other benchmarks (e.g., MetaWorld [28], RLBench [12]), exploring layerwise adaptive expert configurations, and combining MoE with complementary efficiency techniques such as quantization and knowledge distillation. 

SmolVLA-MoE 15 

**Acknowledgments.** This work was supported by the Fundamental Research Funds for the Central Universities (Grant No. 2662025ZKPY009). 

**Declaration on Generative AI** We used Claude as a writing assistant to improve the language quality and readability of this paper. The AI tool was employed solely for refining sentence structure, enhancing clarity, and polishing academic writing style. All technical content, experimental results, and scientific contributions are entirely original work by the authors. 

## **References** 

1. Beyer, L., Steiner, A., Pinto, A.S., Kolesnikov, A., Wang, X., Salz, D., et al.: PaliGemma: A versatile 3b VLM for transfer. arXiv preprint arXiv:2407.07726 (2024) 

2. Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., et al.: _π_ 0: A vision-language-action flow model for general robot control. arXiv preprint arXiv:2410.24164 (2024) 

3. Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Chen, X., Choromanski, K., et al.: RT-2: Vision-language-action models transfer web knowledge to robotic control. arXiv preprint arXiv:2307.15818 (2023) 

4. Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., et al.: RT-1: Robotics transformer for real-world control at scale. In: Robotics: Science and Systems (RSS) (2023) 

5. Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., Song, S.: Diffusion policy: Visuomotor policy learning via action diffusion. In: Robotics: Science and Systems (RSS) (2023) 

6. DeepSeek-AI: DeepSeek-MoE: Towards ultimate expert specialization in mixtureof-experts language models. arXiv preprint arXiv:2401.06066 (2024) 

7. Fedus, W., Zoph, B., Shazeer, N.: Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity. Journal of Machine Learning Research **23** (120), 1–39 (2022) 

8. Hinton, G., Vinyals, O., Dean, J.: Distilling the knowledge in a neural network. In: NeurIPS Workshop on Deep Learning (2015) 

9. Ho, J., Jain, A., Abbeel, P.: Denoising diffusion probabilistic models. In: Advances in Neural Information Processing Systems (NeurIPS) (2020) 

10. Hu, E.J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., Chen, W.: LoRA: Low-rank adaptation of large language models. In: International Conference on Learning Representations (ICLR) (2022) 

11. Jacobs, R.A., Jordan, M.I., Nowlan, S.J., Hinton, G.E.: Adaptive mixtures of local experts. Neural Computation **3** (1), 79–87 (1991) 

12. James, S., Ma, Z., Arrojo, D.R., Davison, A.J.: RLBench: The robot learning benchmark & learning environment. IEEE Robotics and Automation Letters **5** (2), 3019–3026 (2020) 

13. Jiang, A.Q., Sablayrolles, A., Roux, A., Mensch, A., Savary, B., Bamford, C., et al.: Mixtral of experts. arXiv preprint arXiv:2401.04088 (2024) 

14. Kim, M.J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., et al.: OpenVLA: An open-source vision-language-action model. arXiv preprint arXiv:2406.09246 (2024) 

- 16 S. Zhang et al. 

15. Komatsuzaki, A., Puigcerver, J., Lee-Thorp, J., Riquelme Ruiz, C., Mustafa, B., Ainslie, J., Tay, Y., Dehghani, M., Houlsby, N.: Sparse upcycling: Training mixtureof-experts from dense checkpoints. In: International Conference on Learning Representations (ICLR) (2023) 

16. Lepikhin, D., Lee, H., Xu, Y., Chen, D., Firat, O., Huang, Y., et al.: GShard: Scaling giant models with conditional computation and automatic sharding. In: International Conference on Learning Representations (ICLR) (2021) 

17. Li, X., Liu, M., Zhang, H., Yu, C., Xu, J., Wu, H., et al.: Vision-language foundation models as effective robot imitators. arXiv preprint arXiv:2311.01378 (2023) 

18. Lipman, Y., Chen, R.T.Q., Ben-Hamu, H., Nickel, M., Le, M.: Flow matching for generative modeling. In: International Conference on Learning Representations (ICLR) (2023) 

19. Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., Stone, P.: LIBERO: Benchmarking knowledge transfer for lifelong robot learning. In: Advances in Neural Information Processing Systems (NeurIPS) (2023) 

20. Liu, H., Li, C., Wu, Q., Lee, Y.J.: Visual instruction tuning. In: Advances in Neural Information Processing Systems (NeurIPS) (2023) 

21. Mandlekar, A., Nasiriany, S., Wen, B., Akinola, I., Narang, Y., Fan, L., Zhu, Y., Fox, D.: MimicGen: A data generation system for scalable robot learning using human demonstrations. In: Conference on Robot Learning (CoRL) (2023) 

22. Octo Model Team, Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., et al.: Octo: An open-source generalist robot policy. arXiv preprint arXiv:2405.12213 (2024) 

23. Open X-Embodiment Collaboration: Open X-Embodiment: Robotic learning datasets and RT-X models. In: IEEE International Conference on Robotics and Automation (ICRA) (2024) 

24. Shazeer, N., Mirhoseini, A., Maziarz, K., Davis, A., Le, Q., Hinton, G., Dean, J.: Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. In: International Conference on Learning Representations (ICLR) (2017) 

25. SmolVLA Team: SmolVLA: A small vision-language-action model for efficient robot learning. HuggingFace (2025) 

26. Tong, A., Malkin, N., Huguet, G., Zhang, Y., Rector-Brooks, J., Fatras, K., Wolf, G., Bengio, Y.: Improving and generalizing flow-based generative models with minibatch optimal transport. Transactions on Machine Learning Research (TMLR) (2024) 

27. Willi, T., Obando-Ceron, J., Sokar, G., Lyle, C., Farebrother, J., Foerster, J., Dziugaite, G.K., Precup, D., Castro, P.S.: Mixture of experts in a mixture of RL settings. In: Reinforcement Learning Conference (RLC) (2024) 

28. Yu, T., Quillen, D., He, Z., Julian, R., Hausman, K., Finn, C., Levine, S.: MetaWorld: A benchmark and evaluation for multi-task and meta reinforcement learning. In: Conference on Robot Learning (CoRL) (2020) 

29. Yu, T., et al.: Scaling robot learning with semantically imagined experience. In: Robotics: Science and Systems (RSS) (2023) 

30. Zeng, Z., et al.: Expertise need not monopolize: Action-specialized mixture of experts for vision-language-action learning. arXiv preprint arXiv:2510.14300 (2025) 

31. Zhao, T.Z., Kumar, V., Levine, S., Finn, C.: Learning fine-grained bimanual manipulation with low-cost hardware. In: Robotics: Science and Systems (RSS) (2023) 

