---
title: "FRAPPE: Infusing World Modeling into Generalist Policies via Multiple Future Representation Alignment"
date: "2026-02-19"
authors: "Han Zhao; Jingbo Wang; Wenxuan Song; Shuai Chen; Yang Liu; Yan Wang"
url: https://arxiv.org/abs/2602.17259
pdf: https://arxiv.org/pdf/2602.17259
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.17259)** / [論文ページ](https://arxiv.org/abs/2602.17259)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **FRAPPE: Infusing World Modeling into Generalist Policies via Multiple Future Representation Alignment** 

**Han Zhao**<sup>1</sup><sup>_,_2</sup><sup>_†‡_</sup> , **Jingbo Wang**<sup>3</sup><sup>_,_4</sup><sup>_†_</sup> , **Wenxuan Song**<sup>3</sup><sup>_†_</sup> , **Shuai Chen**<sup>5</sup> , **Yang Liu**<sup>2</sup> , **Yan Wang**<sup>6</sup> , **Haoang Li**<sup>3</sup><sup>_∗_</sup> , **Donglin Wang**<sup>2</sup><sup>_∗_</sup> 

> 1Zhejiang University, 2Westlake University, 3HKUST (GZ), 4South China University of Technology, 

> 5ShanghaiTech University, 6Tsinghua University 

> _†_ Equal Contribution, _‡_ Project Lead, _∗_ Corresponding Authors 

Enabling VLA models to predict environmental dynamics, known as world modeling, has been recognized as essential for improving robotic reasoning and generalization. However, current approaches face two main issues: 1. The training objective forces models to over-emphasize pixel-level reconstruction, which constrains semantic learning and generalization 2. Reliance on predicted future observations during inference often leads to error accumulation. To address these challenges, we introduce **F** uture **R** epresentation **A** lignment via **P** arallel **P** rogressive **E** xpansion (FRAPPE). Our method adopts a two-stage fine-tuning strategy: In the mid-training phase, the model learns to predict the latent representations of future observations; In the post-training phase, we expand the computational workload in parallel and align the representation simultaneously with multiple different visual foundation models. By significantly improving fine-tuning efficiency and reducing dependence on action-annotated data, FRAPPE provides a scalable and data-efficient pathway to enhance world-awareness in generalist robotic policies. Experiments on the RoboTwin benchmark and real-world tasks demonstrate that FRAPPE outperforms state-of-the-art approaches and shows strong generalization in long-horizon and unseen scenarios. 

**Correspondence:** Han Zhao at zhaohan34@westlake.edu.cn **Project Website:** https://h-zhao1997.github.io/frappe **Model:** https://huggingface.co/collections/hhhJB/frappe **Code:** https://github.com/Jbo-Wang/frappe 


## **1 Introduction** 

Generalist robotic policies, often built on diffusion generative models (Chi et al., 2025; Ze et al., 2024b; Liu et al., 2024, 2026), have achieved significant advances in manipulation and navigation tasks, as they can effectively model multi-modal action distributions. Recent approaches (Guo et al., 2024; Li et al., 2025b; Zhu et al., 2025; Hu et al., 2024; Liao et al., 2025; Won et al., 2025; Du et al., 2023) further extend diffusion-based policies with auxiliary tasks in the world-model manner ( _i.e._ , predicting future images). These methods incorporate observation supervision to help the model capture scene dynamics, thereby mitigating overfitting to action histories and enhancing robustness to visual perturbations. 

The above works have primarily focused on designing improved architectures to integrate world modeling objectives into policies, while neglecting the investigation of crucial finetuning and inference recipes for deploying these policies. The oversight makes these works reveal two significant limitations: 1. For explicit world modeling policies, generating pixels causes the model to allocate substantial computational resources to fitting redundant pixels, rather than focusing on task-relevant object visual information (Song et al., 2025). This results in poor generative quality in out-of-distribution (OOD) scenarios. Also, during inference, relying 

1 


**Figure 1** We demonstrate that FRAPPE significantly outperforms the state-of-the-art models in both simulated and real-world complex scenarios, and it can effectively leverage data from different levels of the training data pyramid. 

on explicitly predicted observations for action generation may also lead to error accumulation (Du et al., 2023; Liang et al., 2024). 2. Some prior work has attempted to embed implicit world models/knowledge in the network via representation alignment (Zheng et al., 2025; Hu et al., 2024; Li et al., 2025a). However, representations learned from a single visual task inherently carry inductive biases, making them not necessarily suitable for all tasks. 

To address these limitations, we propose **F** uture **R** epresentation **A** lignment via **P** arallel **P** rogressive **E** xpansion (FRAPPE). Our philosophy is to enhance the model’s performance through scaling the computational workload and the implicit grounding of future observations during both training and inference simultaneously. This is realized by a variation of _parallel scaling_ (Chen et al., 2025b). We expand the input streams and training multiple expert networks. The different expert networks share the same frozen backbone, while each has its own set of learnable tokens and Low-Rank Adaptation (LoRA) modules (Hu et al., 2022). The actions are then aggregated by a learnable router to obtain the final action. The entire model can also be viewed as a mixture-of-experts model, which is also widely applied in the architectural design of VLA models (Song et al., 2024; Zhao et al., 2025a). During **training** , in addition to the action supervision objective, we utilize diverse pretrained visual foundation models (VFMs) to encode future observations as alignment targets. Each output future prefix is supervised by the embedding of future observations produced by the corresponding VFM. With the training objective and the prefix-and-LoRA architecture, the finetuning recipe achieves strong performance with minimal trainable parameters. During **inference** , we retain the same computational graph without incorporating VFMs for supervision. In this way, the model benefits from multiple alignment objectives and multi-stream forward to obtain the scaling advantage. 

In practice, we empirically observe that directly training a foundation model for parallel scaling and worldmodeling capabilities is notably challenging, as both the model architecture and the training objectives undergo significant shifts compared to those in the pretraining stage. We thus improve it by a two-stage approach: The **mid-training** stage aligns our single model with a teacher encoder distilled from our multiple VFMs. During this process, the model is full-parameter finetuned to adapt our model to the world-modeling objective. The parallel training is applied during the **post-training** stage to achieve scaling in computing and assign each expert a distinct visual representation from a different encoder for supervision. Beyond the performance gains from model architecture and training objectives, our world-modeling training process can significantly benefit from the incorporation of action-free data. **In small-scale fine-tuning scenarios,** our model can substantially reduce the dependence on expert teleoperation data collection, replacing it with more efficiently collected human hand-manipulation data. **The large-scale internet egocentric data can also scale up training** , the training of world-modeling capabilities can be extended into a form of continual pre-training 

2 


**Figure 2 Overview of training and inference.** During the training phase, the model progressively learns to align with the representation spaces of multiple visual foundation models simultaneously. The model is trained through a two-stage training process to extends to parallel processing of multiple input streams while aligning diverse visual representations. Similarly, parallel inference is implemented during the inference stage. 

on conventional VLA base models. 

In summary, the contributions of our method are as follows: 

- We propose a novel training paradigm that enhances the implicit world modeling capacity of VLA models. FRAPPE builds a robust implicit world model by aligning the model’s features with multiple visual latent representations. By scaling up computation, FRAPPE enhances generative capabilities while avoiding the inductive biases inherent in single-representation learning. 

- We design a two-stage training strategy that allows the model to progressively expand its capabilities. This enables efficient learning and avoids slow convergence that occurs when parallel scaling is applied directly. 

- Our approach can leverage human video demonstrations without action annotations for training, allowing VLA models to scale training data at lower cost compared with imitation learning that relies solely on action-labeled data. 

- In both simulation and real-world settings, our approach surpasses the state-of-the-art (SOTA) models. Notably, when teleoperation data is extremely limited, our method can learn from human-executed videos and improve overall performance by 10-15% compared with a teleoperation-only baseline. 

## **2 Related Work** 

_Diffusion-based Policies_ Diffusion models enable policies to capture multi-modal action distributions and ensure temporal consistency. Diffusion Policy (Chi et al., 2025) introduced this conditional denoising formulation, which DP3 (Ze et al., 2024b) and iDP3 (Ze et al., 2024a) advanced by integrating 3D representations to achieve superior spatial generalization and robust humanoid control. Recently, RDT (Liu et al., 2024) scaled this paradigm to a foundation model level using a diffusion transformer (DiT) trained on massive heterogeneous datasets. Building upon the original RDT, RDT2 (Liu et al., 2026) further scales up the parameter capacity and incorporates a specialized action tokenizer alongside a flow-matching loss. In contrast, our method provides an accessible approach to further enhance capabilities through future image prediction. 

_Generative Models Unifying Vision and Action_ Recent approaches have sought to unify video generation and action prediction within diffusion frameworks. UVA (Li et al., 2025b) learns a joint video-action latent 

3 

representation but employs decoupled lightweight diffusion heads for decoding. PAD (Guo et al., 2024) and UD-VLA (Chen et al., 2025a) unifies the process by encoding modalities separately but performing joint denoising to generate future frames and actions. Alternatively, rather than explicit generation, Genie Envisioner (Liao et al., 2025) and VPP (Hu et al., 2024) leverage video diffusion models as encoders, extracting predictive visual representations to condition the downstream policy. Similarly, FLARE (Zheng et al., 2025) integrates implicit world modeling into policy learning by aligning the introduced future embeddings with the encoded future observations. In contrast, our method optimizes the model by parallel scaling the implicit world modeling process. 

_Robot Learning from Human Egocentric Videos_ Prior research in robot learning from human videos has primarily extracted implicit representations, such as object affordances (Srirama et al., 2024; Shaw et al., 2023; Bahl et al., 2023) or visual trajectories (Bahl et al., 2023; Bharadhwaj et al., 2024). While various works employ pose estimators (Shaw et al., 2023; Zhu et al., 2024; Wang et al., 2023; Ye et al., 2023) to translate human motions into robotic behaviors, Being-H0 (Luo et al., 2025) and EgoVLA (Yang et al., 2025) prioritize high-fidelity 3D hand modeling to achieve the precision required for dexterous manipulation. In contrast, our approach obviates the need for explicit pose estimators, instead leveraging a straightforward prefix-finetuning strategy to distill salient information from egocentric videos. Another research paradigm focuses on extracting latent actions from the temporal transitions between current and future frames to guide downstream learning (Ren et al., 2025; Ye et al., 2024; Bruce et al., 2024; Liang et al., 2024; Bu et al., 2025). Beyond these engineered mappings, Kareer et al. (Kareer et al., 2025) demonstrate that human-to-robot transfer can arise as an emergent property from diverse co-training across embodiment-agnostic datasets. 

In contrast, our framework employs future observations as an explicit grounding signal rather than as ambiguous latent features. By doing so, we endow the model with robust dynamic modeling capabilities, which significantly strengthen the efficacy of policy learning. 

## **3 Method** 

In this section, we first introduce our future representation alignment strategy and its implementation during the mid-training phase. Subsequently, we present Mixture-of-Prefix-and-LoRA (MiPA) and its realization in the post-training stage. Finally, we elaborate on the inference-phase parallel scaling. 

### **3.1 Preliminaries: Robotic Diffusion Transformer** 

Robotic Diffusion Transformer (RDT) (Liu et al., 2024) is a pioneering foundation model for bimanual manipulation. RDT models the conditional distribution of future action sequences, _pθ_ ( **a** _t|_ **o** _t, l_ ). It trains a denoising network, _fθ_ , to predict a clean action chunk **a** _t_ from a noisy version ˜ **a** _t_ conditioned on the observation **o** _t_ and language instruction _l_ . The training objective is to minimize the mean-squared error (MSE): 


where ˜ **a** _t_ =<sup>_~~√~~_</sup> _<u>α</u>_ <u>¯</u> _k_ **<u>a</u>** _t_ +<sup>_~~√~~_</sup> 1 _− α_ ¯ _kϵ_ with noise _ϵ ∼N_ (0 _,_ **I** ) and a diffusion timestep _k_ . 

The network _fθ_ is implemented as a Diffusion Transformer (DiT). It takes low-dimensional state tokens (including ˜ **a** _t_ and proprioception **z** _t_ ) as its input sequence. This sequence is then processed through a series of cross-attention layers conditioned on high-dimensional visual tokens _{x_<sup>_V_</sup> _i_<sup>_}_(fromaSigLIPencoder(Zhai</sup> et al., 2023)) and language tokens _{x_<sup>_L_</sup> _j_<sup>_}_(fromaT5encoder(Raffeletal.,2020)),Finally,theoutputofthe</sup> backbone is projected back to the physical action space by a MLP decoder to produce the action chunk _A_<sup>ˆ</sup> _t_ . 

### **3.2 Future Representation Alignment via Parallel Progressive Expansion** 

**Overview.** As illustrated in Figure 2, the overall philosophy of our method is to construct a world-modeling task during the training process. An inductive idea is to make the model generate future states along with actions. While the visual information is used as the condition for RDT, and can not be supervised directly, the process can be realized by adding a set of noisy prefixes as input, and the model is expected to predict future states from them. Specifically, for the input of the RDT includes proprioception _zt_ , noisy actions _a_ ˜ _t_ , control 

4 

frequency _c_ , and diffusion timestep _k_ , we introduce a set of learnable tokens **p** _∈_ R<sup>_n×d_</sup> as the future prefix to be concatenated with the input. To avoid pixel redundancy, we leverage pretrained vision foundation models as the teacher visual encoder Φ to provide supervising signals **e** _t_ + _h_ = Φ( _ot_ + _h_ ) _,_ **e** _∈_ R<sup>_n×d_Φ</sup> , where _h_ denotes the future horizon, _n_ and _d_ Φ is the length and dimension of output. The denosing process is formulated as 


The alignment loss for a VFM Φ is formulated as 


where cos[ _·, ·_ ] denotes cosine similarity and sg( _·_ ) is the stop-gradient operator, ensuring that gradients do not flow back into the teacher model. Thus, the training objective is a combination of action loss and alignment loss. This process makes the model learn to predict the future states and model the dynamics between the actions and states. 

_Parallel Scaling_ To leverage the world knowledge within diverse VFMs and conduct parallel scaling, we propose a prefix-and-LoRA tuning paradigm to align with multiple future visual representations. Specifically, we construct multiple sets of future prefixes and LoRAs in a shared RDT backbone, and each set is activated during alignment with a dedicated teacher encoder. To reduce the memory footprint during fine-tuning, only the prefixes and LoRAs are trainable in the framework. Considering that all MiPAs are supervised, the loss function should be re-formulated as: 


where _M_ is the number of teacher encoders, and _L_ Φ _i_ denotes the _i_ -th teacher encoder. In this paper, we set _M_ = 3, and the selected teacher encoders are CLIP (Radford et al., 2021) (400M), DINOv2 (Oquab et al., 2023) (142M), and ViT (300M) (Dosovitskiy, 2020). 

To aggregate the outputs of these parallel experts, we introduce a lightweight router network. The router computes a set of gating weights, **w** = _{wi}_<sup>_M_</sup> _i_ =1<sup>,forthe</sup><sup>_M_experts,suchthat�</sup><sup>_M_</sup> _i_ =1<sup>_wi_=1.Letthelatent</sup> action representation from the _i_ -th expert be _zj_ . The final executable action chunk, **a** _t_ , is then produced by passing the weighted sum of these latent representations through a shared action head, MLP( _·_ ): 


_Load Balance during Output Aggregation_ During training, we observed a mode collapse phenomenon, where a single stream would dominate the learning process, preventing others from updating (Fedus et al., 2022; Lepikhin et al., 2020; Szegedy et al., 2016). To mitigate this issue and encourage balanced expert utilization, we incorporate a load-balancing loss into our training strategy: 


where **g** _i,j_ is the logit for the _j_ -th token assigned to the _i_ -th expert, and _B_ is the number of tokens in a batch. This encourages the router to produce logits with similar magnitudes across all experts. 

Additionally, to prevent the router from assigning near-zero weights to certain experts in the early stages of training, we apply label smoothing directly to the final gating weights _w_ . For each expert _i_ , its weight _wi_ is adjusted as follows: 


where _wi_<sup>_′_isthesmoothedweight,and</sup><sup>_ϵ_isasmallhyperparameter(0</sup><sup>_._1inthispaper).Thisensuresthatevery</sup> expert receives a minimum, non-zero weight, thereby guaranteeing that all experts are updated. 

5 

_L_ total = _L_ action + _λ_ 1 _L_ align + _λ_ 2 _L_ balance _,_ (8) 

The final training objective for our framework is formulated as a composition of Equation (1), Equation (4), and Equation (6): 

with weight factors _λ_ 1 and _λ_ 2 that balance the contributions of the alignment and load-balancing objectives, respectively. 

_Mid-Training_ We find that the finetuning process can be further optimized through a mid-training process. Before post-training, the mid-training stage employs traditional single-stream training to align the newly added future prefix with the teacher encoder. To ensure consistency between the two stages and adapt single-stream alignment, we utilize a variant of Theia (Shang et al., 2024), which distills a tiny VFM from multiple pretrained VFMs to ensure comprehensive robotic capabilities. In this paper, we use the 86M encoder distilled from the three encoders used in the post-training phase. This process adapts our model to the world-modeling objective, thereby obtaining a strong initialization for post-training. 

## **4 Simulation Experiments** 

We choose to first conduct fair, uniform, and reproducible comparisons in simulation to demonstrate that our fine-tuning scheme exhibits significant advantages in performance (Section 4.1), training efficiency (Section 4.2), and efficiency across models of different parameter scales (Section 4.4). The following settings are consistent across all experiments in this section: 

_Simulation Environment_ We evaluate our method on RoboTwin (Chen et al., 2025c). RoboTwin is a real-to-sim bimanual benchmark. It contains an _Easy_ setting with in-domain layout and a _Hard_ setting with domain randomization, including scene clutter, diverse background textures, lighting variation, and varied tabletop heights. To comprehensively evaluate the performance, all simulation experiments are conducted on 8 diverse tasks under both _Easy_ and _Hard_ settings. 

_Training Details_ Our model is fine-tuned starting from the official RDT-1B pre-trained weights. For all experiments, the training dataset is restricted to 50 task-specific trajectories from the Easy setting. The training process is conducted on two NVIDIA H100 GPUs for a total of 20,000 steps with a batch size of 32, partitioned into 15,000 mid-training steps and 5,000 post-training steps for all models using FRAPPE. Accuracy is reported based on the average performance over 100 evaluation trials to ensure fair comparison. 

### **4.1 Comparison with State-of-the-Arts** 

Our primary baseline is the base RDT model finetuned using the original finetuning recipe. However, for broader comparison, we also include several other baselines. The complete list of comparisons is as follows: 

- Diffusion Policy ( **DP** (Chi et al., 2025)): a train-from-scratch visuomotor policy, serving as a small-scale baseline model. 

- Video Prediction Policy ( **VPP** (Hu et al., 2024)): Training subsequent DP based on representations provided by a pre-trained video prediction diffusion model, serving as an implicit world model baseline for comparison. 

- **RDT** (Liu et al., 2024): The base model adopted for FRAPPE. 

- _π_ **0** (Black et al., 2024): the state-of-the-art method and its advanced version on RoboTwin Benchmark with a VLM and flow-matching head combined architecture. 

- _π_ **0** _._ **5** (Intelligence et al., 2025): The successor to _π_ 0, demonstrating stronger generalization capabilities. 

As presented in Table 1, under the Easy setting, our method achieves the highest average success rates across all the tasks. This demonstrates that our proposed training paradigm yields substantial improvements over the baseline RDT, effectively expanding its capability boundaries. 

6 

**Table 1 Comparisons with state-of-the-art methods on RoboTwin 2.0 benchmark.** Please note that **Bold** and Underline denote the best and the second-best performances among the methods. 

|**Method**|**Hando**|**ver Mic**|**Pick**|**Dual B**|**ottles**|**Hando**|**ver Block**|**Place **|**Object B**|**asket**|
|---|---|---|---|---|---|---|---|---|---|---|
||Easy|Hard|Easy||Hard|Easy|Hard|Easy||Hard|
|**DP**|53.0%|0.0%|24.0%||0.0%|10.0%|0.0%|15.0%||0.0%|
|**VPP**|91.0%|7.0%|28.0%||6.0%|8.0%|0.0%|30.0%||0.0%|
|**RDT**|90.0%|31.0%|45.0%||14.0%|45.0%|14.0%|30.0%||6.0%|
|_π_**0**|**98.0%**|13.0%|57.0%||12.0%|45.0%|8.0%|16.0%||2.0%|
|_π_**0**_._**5**|**98.0%**|13.0%|37.0%||13.0%|2.0%|0.0%|**42.0%**||4.0%|
|**Ours**|**98.0%**|**45.0%**|**67.0%**||**28.0%**|**50.0%**|**18.0%**|35.0%||**15.0%**|
|**Method**|**Put Object **|**Cabinet**|**Place S**|**hoe**|**Stack Bo**|**wls Two**|**Put Bottle **|**Dustbin**|**Aver**|**age**|
||Easy|Hard|Easy|Hard|Easy|Hard|Easy|Hard|Easy|Hard|
|**DP**|42.0%|0.0%|23.0%|0.0%|61.0%|0.0%|22.0%|0.0%|31.3%|0.0%|
|**VPP**|15.0%|12.0%|40.0%|4.0%|59.0%|3.0%|15.0%|0.0%|35.8%|4.0%|
|**RDT**|33.0%|18.0%|35.0%|7.0%|74.0%|27.0%|27.0%|4.0%|47.4%|15.1%|
|_π_**0**|**68.0%**|18.0%|28.0%|6.0%|**91.0%**|41.0%|**54.0%**|**13.0%**|57.1%|14.1%|
|_π_**0**_._**5**|46.0%|15.0%|28.0%|12.0%|85.0%|**44.0%**|25.0%|5.0%|45.4%|13.3%|
|**Ours**|52.0%|**37.0%**|**41.0%**|**18.0%**|80.0%|36.0%|37.0%|7.0%|**57.5%**|**25.5%**|


Under the Hard setting, all compared methods only reach very low success rates, because varying distractors, background textures, lighting conditions, and table heights pose huge challenges to models’ visual generalization. However, our model surpasses the most effective _π_ 0 _._ 5 by a clear margin. This indicates that our model better learns the low-level dynamics behind diverse visual observations, thus producing correct actions rather than relying on spurious correlations (Xing et al., 2025). 

### **4.2 Comparison of Training Paradigm** 

In this section, we conduct experiments on various training paradigms under the condition of a fixed total training step count of 20,000. For these experiments, we selected two representative tasks from above: Stack Bowls Two and Pick Dual Bottles. Based on the experimental results in Table 2, we present the following insights regarding effective training paradigms. 

**Mid-Training is necessary before post-training.** As shown in Paradigms 3 and 4, training solely in the Post-Training stage directly on the base model yields results even lower than the RDT baseline. Similar to how fine-tuning struggles to improve task performance on out-of-distribution tasks in language models (Gururangan et al., 2020), we attribute this phenomenon to the significant distribution mismatch between the RDT pretraining and the introduction of the future frame prediction objective. Compared to fine-tuning that only uses generating action chunks as the supervised objective, the single-stage mid-training (Paradigm 1) achieved an average improvement of 4.6% in overall success rate under the same 20k training steps. Furthermore, a comparison with Paradigm 2 indicates that during the mid-training stage, full-parameter training is required to bridge the substantial distribution gap. 

**Post-Training can enhance model performance in a parameter-efficient manner.** A comparative analysis of Paradigms 1, 5, and 6 in Table 2 reveals that introducing multi-prefix alone results in a minor performance degradation, whereas combining it with LoRA fine-tuning yields a substantial improvement. This discrepancy arises because scaling up the prefix tuning involves switching to different future teacher supervision models, which possess distinct representation spaces. However, the RDT backbone remains frozen, retaining the alignment with the Theia teacher model acquired during the mid-training phase. This shift in external supervision, without a corresponding mechanism for model adaptation, negatively impacts performance. Furthermore, after introducing LoRA fine-tuning, the model demonstrated a significant improvement in task success rate compared to both the baseline and the mid-trained model. This indicates the effectiveness of our parallel scaling approach. Moreover, unlike the performance observed during the mid-training stage, the post-training stage does not require full-parameter fine-tuning; only LoRA fine-tuning is sufficient to adapt to the representation space gap caused by changes in the teacher model. 

7 

**Table 2 Comparison of training paradigms.** Please note that **Bold** and <u>Underline</u> denote the best and the second-best performances, respectively, across the paradigms. The results indicate that both mid-training and post-training phases are significant for the method’s improvement. 

|Paradigm|Method|Training Steps|Suc|cess Rat|es (%)|
|---|---|---|---|---|---|
|No.|||Easy|Hard|Average|
|0|RDT|20k|59.0|20.5|39.8|
|1|mid-train (full ft)|20k|63.0|27.5|45.3|
|2|mid-train (prefix & lora ft)|20k|48.0|8.5|28.3|
|3|post-train (prefix ft)|20k|25.0|4.0|14.5|
|4|post-train (prefix & lora ft)|20k|46.0|9.0|27.5|
|5|mid-train (full ft) + post-train (prefix ft)|15k + 5k|68.0|21.5|44.8|
|6|mid-train (full ft) + post-train (prefix & lora ft) **(ours)**|15k + 5k|**73.5**|**32.0**|**52.3**|


**Table 3 Comparison of Inference Efficiency** 

||RDT<br>(5 steps)|mid-train<br>(5 steps)|post-train<br>(5 steps)|post-train<br>(3 steps)|
|---|---|---|---|---|
|Inference Memory (GB)|3.7|3.7|8.0|8.0|
|Latency (Sec)|0.214|0.228|0.235|0.173|
|Success Rates (%)|39.8|45.3|52.3|48.5|


### **4.3 Efficiency during Training and Inference** 

In addition to the training paradigm, we also examined the inference efficiency, a particular concern in the robotics domain. Since our parallel scaling scheme introduces additional parallel computations and parameters, we report a comparison in Table 3 with the vanilla RDT-1B and the mid-trained model in terms of GPU memory usage, inference latency, and average performance on RoboTwin. 

We conducted inference testing using a single NVIDIA H100 GPU. By leveraging CUDA Graph, we have significantly improved inference efficiency. When denoising with the same 5 steps as the baseline model, our action generation latency increased by only about 20 ms. The memory usage has increased to 8.0 GB, yet it remains within the typical memory capacity of commonly used inference GPUs. When the denoising steps were reduced to 3, our method achieved higher performance than the baseline with lower inference latency. 

### **4.4 Verification Experiments on Smaller-Scale Policy Model** 

We further validated the proposed paradigm on a model with significantly smaller parameters (RDT-130M). As shown in Figure 3, our paradigm continues to demonstrate outstanding performance even on a smaller baseline below the 1B scale. 

First, compared to the baseline model, our method achieves consistent performance improvements across both easy and hard task settings. Second, at the 130M parameter scale, the performance of LoRA fine-tuning during the post-training stage is only 2–3% lower in average success rate across various tasks compared to full-parameter fine-tuning. This strongly demonstrates the high efficiency of applying LoRA fine-tuning within our architectural framework. 

Moreover, our optimized small model exhibits performance comparable to the RDT-1B baseline. Through further analysis of individual subtasks, we observed that RDT-130M shows weaker generalization on hard-type tasks compared to the 1B baseline. However, our training paradigm delivers substantial improvements on all hard tasks. This provides compelling evidence that our training scheme and architectural design substantially extend the capability boundaries of the model. 

## **5 Real-world Experiments** 

In real-world experiments, we focus on exploring the model’s capabilities in more complex scenarios (Section 5.2) and the scalability of the training scheme at the data level (Section 5.3). 

8 


**Figure 3 Experiments on different parameter scales on 4 tasks on the RoboTwin 2.0.** The 130M backbone model fine-tuned using either LoRA or full-parameter fine-tuning under the FRAPPE consistently outperforms the naively fine-tuned RDT-130M across all tasks and remains competitive when compared with the naively fine-tuned RDT-1B. Especially in the **Stack Bowls Two-Hard** task, the improvement is significant. 


**Figure 4 Real-world experiment results in seen and unseen scenarios.** We evaluate our FRAPPE and prior SOTA VLAs on 4 representative tasks, each with different axes of generalization. Seen means the settings were included in the training data, while Unseen refers to new task settings that the model did not encounter during training. 

### **5.1 Experimental Setup** 

Real-world experiments are conducted on a bimanual AgileX mobile manipulator. Each arm features six degrees of freedom (6-DoF) and is equipped with a parallel gripper. The vision system comprises a primary high-mounted camera for a third-person perspective and two wrist-mounted cameras for ego-centric views. For training, we utilize 25 demonstrations per variation for basic tasks, and 100 demonstrations for long-horizon tasks. During evaluation, we perform 40 trials for each basic task and 20 trials for each long-horizon task. 

### **5.2 Comparison on Generalization and Long-horizon Tasks** 

We designed four basic tasks to test our model under different variations: lighting, height, pose, and object variations. Each task is divided into seen and unseen settings to evaluate the vision generalization capacity of the fine-tuned model. As shown in Figure 4, our model achieves strong performance in all cases, especially in unseen ones. These results match our findings in the simulation and show that our model has good generalization in the real world. 

To investigate the performance limits of FRAPPE, we devised a challenging long-horizon task characterized by three temporally dependent sub-tasks and four interactive objects. This task necessitates sophisticated dual-arm coordination, as illustrated in Figure 5. Our results demonstrate that FRAPPE significantly outperforms the baseline RDT. Specifically, while the vanilla RDT failed to complete the task in any trial due to challenges in fine-grained manipulation, such as precisely grasping and placing a lid, and maintaining action continuity across sub-tasks. In contrast, our model achieved a 20% success rate. 

9 


**Figure 5 Long-horizon Performance.** Each data point represents the success rate of completing up to and including that corresponding subtask. 

### **5.3 Co-Training with Human Egocentric Data** 

In this section, we explain how the model benefits from action-free human egocentric data. We demonstrate that FRAPPE can leverage such data to enhance the generalized world-modeling capabilities of the base model, rather than being effective only in fine-tuning processes that involve robot data. 

_Data Pyramid_ Motivated by these insights, we propose a hierarchical data pyramid framework to strategically integrate diverse data types across training stages. 

The **bottom** layer of our pyramid consists of large-scale action-free human egocentric data, which are usually open-sourced datasets with hundreds to thousands of hours of recordings and include a wide variety of contactrich manipulation tasks (Zhao et al., 2025b). The **middle** layer comprises task-specific human egocentric data, collected by human operators directly manipulating objects without teleoperating a robotic arm. This makes data collection highly efficient and requires only minimal hardware. Since pretrained VLA models assume a fixed third-person camera setting, we do not use head-mounted cameras such as GoPro or VR devices (Zheng et al., 2025). Instead, we adopt a static third-person camera setup consistent with conventional robot data collection. Under this setup, even inexperienced human operators can achieve a data collection rate of more than 360 trajectories per hour. The **top** layer of the pyramid consists of conventional task-specific robot data, collected via human teleoperation of the robot using dedicated control interfaces. Skilled operators can typically collect up to 120 trajectories per hour in this setting. 

_Co-Training_ We train the model during the mid-training phase by mixing web-scale human egocentric data with task-specific human data and robot data for sampling. When training on action-free samples, the action loss in Equation (1) is omitted and instead only the alignment loss is optimized. 

To evaluate whether our method can effectively learn from human egocentric videos and further scale with large amounts of task-irrelevant egocentric data, we compare the performance of models trained under different data configurations on a pick-and-place task. The target objects consist of five easy-to-grasp objects and five hasy-to-grasp objects. The training data used in this experiment contains 5 robot action trajectories per object, 50 task-specific human egocentric trajectories, and 10k task-irrelevant human egocentric videos. 

Here, we consider four training settings: 

- **Robot (task):** Fine-tuning on robot data only. 

- **+ Ego (task):** Fine-tuning on a mixture of robot and human egocentric data. 

10 


**Figure 6 Leveraging human egocentric data without action labels. (a).** Experimental targets, including 5 objects that are easy to pick up, and 5 objects that are difficult to pick up. **(b).** Multi-task results of FRAPPE trained on **Robot (task)** and **+ Ego (web)** across 8 target object categories. Here, “multi-task” denotes that one model is used to be trained and tested on multiple target objects. **(c).** The results of FRAPPE trained on **Robot (task)** , **+ Ego (web)** and **+ Ego (task) + Ego (web)** data mixture, respecitvely. 

- **+ Ego (web):** Fine-tuning on both web-scale human egocentric data and robot data. Detailed information on Ego (web) can be found in Appendix. 

- **+ Ego (task) + Ego (web):** Co-training with all three types of data. 

Based on the results, the following conclusions can be drawn: 

**Training on large-scale open-sourced egocentric videos provides a strong inductive prior for the model to handle novel objects.** Figure 6(b) shows that for the 5 easy-to-grasp objects, models trained on large-scale egocentric data consistently achieve performance improvements. This suggests that although the open-sourced egocentric dataset is irrelevant to our downstream tasks, training on it enhances the model’s world modeling capabilities. 

For the 5 hard-to-grasp objects, models trained with only a small amount of robot data exhibit low success rates, whereas models with co-training achieve substantially higher performance. We believe this is likely because the large-scale dataset naturally offers a diverse distribution of complex object geometries, thereby providing a stronger inductive prior for the model. 

FRAPPE **can leverage task-specific egocentric data to improve spatial generalization.** We select two representative target objects (cube and garlic) and observe that training on only 5 robot trajectories results in very low success rates, as shown in Figure 6(c). This indicates that although FRAPPE exhibits few-shot learning capability, the extremely limited number of samples still prevents the model from learning the task dynamics and thus from achieving position generalization. On the other hand, incorporating human egocentric data enables the model to learn future prediction and capture underlying dynamics from more samples, resulting in significant improvements. 

**Combining data from different levels of the data pyramid enables effective scaling and leads to maximized performance.** Furthermore, the results in Figure 6(c) show that when the advantages of training are combined with co-training samples, model performance is further improved. 

## **6 Conclusion** 

This paper proposes FRAPPE, an efficient training scheme built upon pre-trained diffusion-based VLA models. It includes a mid-training phase for world-modeling enhanced visual representation alignment and a parameter-efficient post-training phase to unlock the parallel scaling capacity of the model. 

11 

Extensive simulation experiments on the RoboTwin platform and real-world evaluations demonstrate that FRAPPE exhibits significant advantages in data efficiency, parameter efficiency, and overall performance compared to baseline models trained through direct fine-tuning. Furthermore, our model can effectively leverage large-scale egocentric human operation data, which further enhances the generalization capability of the pre-trained model beyond merely fine-tuning on target domains. 

## **References** 

- Shikhar Bahl, Russell Mendonca, Lili Chen, Unnat Jain, and Deepak Pathak. Affordances from human videos as a versatile representation for robotics. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 13778–13790, 2023. 

- Homanga Bharadhwaj, Roozbeh Mottaghi, Abhinav Gupta, and Shubham Tulsiani. Track2act: Predicting point tracks from internet videos enables diverse zero-shot robot manipulation. _CoRR_ , 2024. 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Jake Bruce, Michael D Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, et al. Genie: Generative interactive environments. In _Forty-first International Conference on Machine Learning_ , 2024. 

- Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xuan Hu, Xu Huang, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025. 

- Jiayi Chen, Wenxuan Song, Pengxiang Ding, Ziyang Zhou, Han Zhao, Feilong Tang, Donglin Wang, and Haoang Li. Unified diffusion vla: Vision-language-action model via joint discrete denoising diffusion process, 2025a. https://arxiv.org/abs/2511.01718. 

- Mouxiang Chen, Binyuan Hui, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Jianling Sun, Junyang Lin, and Zhongxin Liu. Parallel scaling law for language models. _arXiv preprint arXiv:2505.10475_ , 2025b. 

- Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025c. 

- Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11):1684–1704, 2025. 

- Alexey Dosovitskiy. An image is worth 16x16 words: Transformers for image recognition at scale. _arXiv preprint arXiv:2010.11929_ , 2020. 

- Yilun Du, Sherry Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Josh Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning universal policies via text-guided video generation. _Advances in neural information processing systems_ , 36: 9156–9172, 2023. 

- William Fedus, Barret Zoph, and Noam Shazeer. Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity. _Journal of Machine Learning Research_ , 23(120):1–39, 2022. 

- Yanjiang Guo, Yucheng Hu, Jianke Zhang, Yen-Jen Wang, Xiaoyu Chen, Chaochao Lu, and Jianyu Chen. Prediction with action: Visual policy learning via joint denoising process. _Advances in Neural Information Processing Systems_ , 37:112386–112410, 2024. 

- Suchin Gururangan, Ana Marasović, Swabha Swayamdipta, Kyle Lo, Iz Beltagy, Doug Downey, and Noah A. Smith. Don’t stop pretraining: Adapt language models to domains and tasks, 2020. https://arxiv.org/abs/2004.10964. 

- Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. _ICLR_ , 1(2):3, 2022. 

- Yucheng Hu, Yanjiang Guo, Pengchao Wang, Xiaoyu Chen, Yen-Jen Wang, Jianke Zhang, Koushil Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy with predictive visual representations. _arXiv preprint arXiv:2412.14803_ , 2024. 

12 

- Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. pi0.5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- Simar Kareer, Karl Pertsch, James Darpinian, Judy Hoffman, Danfei Xu, Sergey Levine, Chelsea Finn, and Suraj Nair. Emergence of human to robot transfer in vision-language-action models. _arXiv preprint arXiv:2512.22414_ , 2025. 

- Dmitry Lepikhin, HyoukJoong Lee, Yuanzhong Xu, Dehao Chen, Orhan Firat, Yanping Huang, Maxim Krikun, Noam Shazeer, and Zhifeng Chen. Gshard: Scaling giant models with conditional computation and automatic sharding. _arXiv preprint arXiv:2006.16668_ , 2020. 

- Fuhao Li, Wenxuan Song, Han Zhao, Jingbo Wang, Pengxiang Ding, Donglin Wang, Long Zeng, and Haoang Li. Spatial forcing: Implicit spatial representation alignment for vision-language-action model, 2025a. https: //arxiv.org/abs/2510.12276. 

- Shuang Li, Yihuai Gao, Dorsa Sadigh, and Shuran Song. Unified video action model. _arXiv preprint arXiv:2503.00200_ , 2025b. 

- Junbang Liang, Ruoshi Liu, Ege Ozguroglu, Sruthi Sudhakar, Achal Dave, Pavel Tokmakov, Shuran Song, and Carl Vondrick. Dreamitate: Real-world visuomotor policy learning via video generation. _arXiv preprint arXiv:2406.16862_ , 2024. 

- Yue Liao, Pengfei Zhou, Siyuan Huang, Donglin Yang, Shengcong Chen, Yuxin Jiang, Yue Hu, Jingbin Cai, Si Liu, Jianlan Luo, et al. Genie envisioner: A unified world foundation platform for robotic manipulation. _arXiv preprint arXiv:2508.05635_ , 2025. 

- Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 

- Songming Liu, Bangguo Li, Kai Ma, Lingxuan Wu, Hengkai Tan, Xiao Ouyang, Hang Su, and Jun Zhu. Rdt2: Exploring the scaling limit of umi data towards zero-shot cross-embodiment generalization, 2026. https://arxiv.org/ abs/2602.03310. 

- Hao Luo, Yicheng Feng, Wanpeng Zhang, Sipeng Zheng, Ye Wang, Haoqi Yuan, Jiazheng Liu, Chaoyi Xu, Qin Jin, and Zongqing Lu. Being-h0: vision-language-action pretraining from large-scale human videos. _arXiv preprint arXiv:2507.15597_ , 2025. 

- Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 

- Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pages 8748–8763. PmLR, 2021. 

- Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J Liu. Exploring the limits of transfer learning with a unified text-to-text transformer. _Journal of machine learning research_ , 21(140):1–67, 2020. 

- Zhongwei Ren, Yunchao Wei, Xun Guo, Yao Zhao, Bingyi Kang, Jiashi Feng, and Xiaojie Jin. Videoworld: Exploring knowledge learning from unlabeled videos. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 29029–29039, 2025. 

- Jinghuan Shang, Karl Schmeckpeper, Brandon B May, Maria Vittoria Minniti, Tarik Kelestemur, David Watkins, and Laura Herlant. Theia: Distilling diverse vision foundation models for robot learning. _arXiv preprint arXiv:2407.20179_ , 2024. 

- Kenneth Shaw, Shikhar Bahl, and Deepak Pathak. Videodex: Learning dexterity from internet videos. In _Conference on Robot Learning_ , pages 654–665. PMLR, 2023. 

- Wenxuan Song, Han Zhao, Pengxiang Ding, Can Cui, Shangke Lyu, Yaning Fan, and Donglin Wang. Germ: A generalist robotic model with mixture-of-experts for quadruped robot. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 11879–11886. IEEE, 2024. 

- Wenxuan Song, Ziyang Zhou, Han Zhao, Jiayi Chen, Pengxiang Ding, Haodong Yan, Yuxin Huang, Feilong Tang, Donglin Wang, and Haoang Li. Reconvla: Reconstructive vision-language-action model as effective robot perceiver, 2025. https://arxiv.org/abs/2508.10333. 

13 

- Mohan Kumar Srirama, Sudeep Dasari, Shikhar Bahl, and Abhinav Gupta. Hrp: Human affordances for robotic pre-training. _arXiv preprint arXiv:2407.18911_ , 2024. 

- Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe, Jon Shlens, and Zbigniew Wojna. Rethinking the inception architecture for computer vision. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 2818–2826, 2016. 

- Chen Wang, Linxi Fan, Jiankai Sun, Ruohan Zhang, Li Fei-Fei, Danfei Xu, Yuke Zhu, and Anima Anandkumar. Mimicplay: Long-horizon imitation learning by watching human play. _arXiv preprint arXiv:2302.12422_ , 2023. 

- John Won, Kyungmin Lee, Huiwon Jang, Dongyoung Kim, and Jinwoo Shin. Dual-stream diffusion for world-model augmented vision-language-action model. _arXiv preprint arXiv:2510.27607_ , 2025. 

- Youguang Xing, Xu Luo, Junlin Xie, Lianli Gao, Hengtao Shen, and Jingkuan Song. Shortcut learning in generalist robot policies: The role of dataset diversity and fragmentation. _arXiv preprint arXiv:2508.06426_ , 2025. 

- Ruihan Yang, Qinxi Yu, Yecheng Wu, Rui Yan, Borui Li, An-Chieh Cheng, Xueyan Zou, Yunhao Fang, Xuxin Cheng, Ri-Zhao Qiu, et al. Egovla: Learning vision-language-action models from egocentric human videos. _arXiv preprint arXiv:2507.12440_ , 2025. 

- Jianglong Ye, Jiashun Wang, Binghao Huang, Yuzhe Qin, and Xiaolong Wang. Learning continuous grasping function with a dexterous hand from human demonstrations. _IEEE Robotics and Automation Letters_ , 8(5):2882–2889, 2023. 

- Seonghyeon Ye, Joel Jang, Byeongguk Jeon, Sejune Joo, Jianwei Yang, Baolin Peng, Ajay Mandlekar, Reuben Tan, Yu-Wei Chao, Bill Yuchen Lin, et al. Latent action pretraining from videos. _arXiv preprint arXiv:2410.11758_ , 2024. 

- Yanjie Ze, Zixuan Chen, Wenhao Wang, Tianyi Chen, Xialin He, Ying Yuan, Xue Bin Peng, and Jiajun Wu. Generalizable humanoid manipulation with 3d diffusion policies. _arXiv preprint arXiv:2410.10803_ , 2024a. 

- Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations. _arXiv preprint arXiv:2403.03954_ , 2024b. 

- Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 11975–11986, 2023. 

- Han Zhao, Wenxuan Song, Donglin Wang, Xinyang Tong, Pengxiang Ding, Xuelian Cheng, and Zongyuan Ge. More: Unlocking scalability in reinforcement learning for quadruped vision-language-action models. _arXiv preprint arXiv:2503.08007_ , 2025a. 

- Hongxiang Zhao, Xingchen Liu, Mutian Xu, Yiming Hao, Weikai Chen, and Xiaoguang Han. Taste-rob: Advancing video generation of task-oriented hand-object interaction for generalizable robotic manipulation. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 27683–27693, 2025b. 

- Ruijie Zheng, Jing Wang, Scott Reed, Johan Bjorck, Yu Fang, Fengyuan Hu, Joel Jang, Kaushil Kundalia, Zongyu Lin, Loic Magne, et al. Flare: Robot learning with implicit world modeling. _arXiv preprint arXiv:2505.15659_ , 2025. 

- Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin Burchfiel, Paarth Shah, and Abhishek Gupta. Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets. _arXiv preprint arXiv:2504.02792_ , 2025. 

- Yifeng Zhu, Arisrei Lim, Peter Stone, and Yuke Zhu. Vision-based manipulation from single human video with open-world object graphs. _arXiv preprint arXiv:2405.20321_ , 2024. 

14 

# Appendix 

In this appendix, we provide supplementary information regarding the implementation details and hyperparameter analysis of our proposed framework. Section A presents the empirical studies used to determine the optimal configuration for the alignment loss coefficient, future supervision depth, and prediction horizon. Section B details the human egocentric co-training phase, including dataset characteristics, computational requirements, and the rationale for our data selection. 

## **A Hyperparameter Settings** 

**Table S1** weight factor of alignment loss. 

|_λ_1|0|0.001|0.02|0.05|0.1|0.5|
|---|---|---|---|---|---|---|
|SR (%)|14.0|18.5|26.4|**32.5**|22.0|23.5|


The hyper-parameter _λ_ 1 serves as the coefficient for the alignment loss in Equation (8). An appropriate value for this coefficient enables the model to effectively learn future state prediction and capture the dynamics between actions and states. However, an excessively large weight may interfere with the model’s primary task of action prediction. As shown in Table S1, the model performs best under the _λ_ 1 = 0 _._ 05. 

**Table S2** depth of future alignment. 

|_depth_|7|14|21|28|
|---|---|---|---|---|
|SR (%)|14.5|18.0|**23.5**|16.0|


A critical design choice in Equation (3) involves determining the optimal depth of **p** _t_ within the DiT layers of RDT to facilitate effective future supervision. The RDT-1B backbone comprises a total of 28 DiT layers. As shown in Table S2, we find that utilizing the output of the 21st layer for learnable prefix alignment yields the best performance. This observation is consistent with the findings in (Zheng et al., 2025), suggesting that supervising the representations at approximately three-quarters of the total depth of the model is the most beneficial. 

**Table S3** steps of future alignment. 

|_h_|8|16|32|
|---|---|---|---|
|SR (%)|**35.3**|35.0|29.7|


The selection of the future horizon _h_ significantly influences the ability of the model to capture future representations. Our experimental results, as summarized in Table S3, demonstrate that the model achieves optimal performance when _h_ is set to 8. 

Based on these empirical findings, we use the optimal parameters identified above as the standard configuration for all other experiments. 

## **B Human Egocentric Co-Training Details** 

We provide a comprehensive overview of the training stage involving web- scale human egocentric data. We leverage TASTE-Rob (Zhao et al., 2025b), a large-scale dataset of ego-centric hand-object interaction videos containing 100,856 video sequences and roughly 9 million frames, with high-fidelity linguistic alignment for each video. The training involves one epoch and requires 96 hours of computation on 8 H100 GPUs. The rationale for utilizing TASTE-Rob lies in its fixed egocentric viewpoint, which closely mirrors the camera 

15 

settings typically found in mainstream VLA models. Such consistency significantly enhances the transferability of learned features for downstream robot action prediction tasks. 

16 

