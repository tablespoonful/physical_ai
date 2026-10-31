---
title: "Shallow-π: Knowledge Distillation for Flow-based VLAs"
date: "2026-01-28"
authors: "Boseong Jeon; Yunho Choi; Taehan Kim"
url: https://arxiv.org/abs/2601.20262
pdf: https://arxiv.org/pdf/2601.20262
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.20262)** / [論文ページ](https://arxiv.org/abs/2601.20262)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Shallow-** _π_ **: Knowledge Distillation for Flow-based VLAs** 

Boseong Jeon, Yunho Choi, Taehan Kim Samsung Research South Korea 

junbs95@gmail.com, yunho10.choi@samsung.com, taehan11.kim@samsung.com 

## **Abstract** 

_The growing demand for real-time robotic deployment necessitates fast and on-device inference for vision– language–action (VLA) models. Within the VLA literature, efficiency has been extensively studied at the token level, such as visual token pruning. In contrast, systematic transformer layer reduction has received limited attention, and to the best of our knowledge, has not been explored for flow-based VLA models under knowledge distillation. In this work, we propose Shallow-π, a principled knowledge distillation framework that aggressively reduces the transformer depth of both the VLM backbone and the flow-based action head, compressing the model from_ 18 _→_ 6 _layers. Shallow-π achieves over_ 2 _× faster inference with less than_ 1% _absolute drop in success rate on standard manipulation benchmarks, establishing state-of-the-art performance among reduced VLA models. Crucially, we validate our approach through industrial-scale real-world experiments on Jetson Orin and Jetson Thor across multiple robot platforms, including humanoid systems, in complex and dynamic manipulation scenarios. The project page can be found at https://icsl-jeon.github.io/ shallow-pi/._ 

## **1. INTRODUCTION** 

Spurred by the rapid progress of large multimodal models [2, 6], Vision-Language-Action (VLA) models [3, 4, 15, 19] have advanced generalist robotics by enabling diverse capabilities through a robot foundation model in an end-toend manner. In these models, the vision-language model (VLM) backbone processes both images and prompts, and the resulting features are injected into the action-generation module as conditioning signals [35]. In particular, flowbased VLA models, including _π_ [4, 15], GR00T [3], and CogACT [21], adopt diffusion transformers (DiT) [29] as their action heads to harness the strong generative capacity of flow-matching [23] while supporting diffusion-guidance techniques [1, 27]. 

However, these advantages come at a non-trivial computational cost. Flow-based VLAs combine a large VLM backbone with a diffusion-based action head consisting of dozens of transformer layers and additionally require iterative diffusion steps at inference time, which together make real-time deployment on edge devices challenging. To mitigate these costs, prior work has explored improving VLA efficiency along multiple axes, including reducing visual tokens [22, 34, 37], diffusion steps [30, 38], and transformer layers or attention computation [36, 42, 43], as well as applying quantization [28] and graph-level optimization [26]. Among existing efficiency approaches, we focus on reducing the transformer depth of _π-like_ flow-based VLA architectures, which inject vision–language features into the action head at every layer [35]. 

To reduce transformer computation of VLAs, in general, prior works have primarily followed two directions: (1) layer-skipping methods [39, 42, 43], and (2) using smaller backbone models [33, 36]. Layer-skipping approaches leverage inter-layer feature similarity to bypass redundant computation [39, 42], or employ router-based mechanisms that conditionally skip transformer blocks [43]. However, these methods typically require the full model to remain resident in GPU memory at inference time, since layers are dynamically skipped rather than structurally removed. Also, existing layer-skipping methods are generally evaluated only on backbone depth reduction, as illustrated in Figure 1-(a,b). This limits their applicability to _π_ -like flowbased VLA models [1, 9], where the action head commonly mirrors the VLM depth in order to consume features from intermediate layers (see Figure 1-(c, d)). In addition, prior evaluations are largely conducted in simulation environments [39, 42] or relatively simple single-arm tasks with limited dexterity in static scenes [33], and predominantly target server-class GPUs (e.g., RTX 4090) [43]. 

The second line of work focuses on adopting smaller VLM backbones by reducing hidden dimensions or performing early exits from intermediate layers [33, 36] for VLM backbone (see Figure 1-(c)). While effective in lowering computational cost, these approaches often require 


Figure 1. Layer reduction strategies and targeted structures in the VLA domain. Previous methods primarily reduce backbone depth only or dynamically skip layers at inference time. In contrast, we propose a systematic knowledge distillation framework that jointly reduces the transformer depth of both the VLM backbone and the action head, which is especially effective for _π_ -like architectures where the action head mirrors the VLM backbone to receive conditioning information from all layers. 

training the VLM backbone from scratch [36], which limits their compatibility with large pretrained models and hinders performance scaling in complex manipulation tasks. Moreover, these methods do not reduce the depth of the action head, which is particularly critical for flow-based models where inference involves repeated denoising steps, making action-head computation a dominant cost. 

In this work, we propose **Shallow-** _π_ with the following contributions: 

- We develop and validate a knowledge distillation framework that jointly compresses both the VLM backbone and the action head in _π_ -like flow-based VLAs, achieving up to 70% layer reduction while preserving the layer-wise feature transfer required by their architecture. 

- We carefully design and systematically ablate a set of distillation objectives—including ground-truth supervision, teacher trajectory imitation, and intermediate attention transfer—tailored to _π_ -like flow-based VLAs, where only action tokens are denoised and multimodal features are injected from the VLM backbone at every layer. 

- We demonstrate strong real-world performance and computational efficiency by deploying a 6-layer Shallow- _π_ model on edge devices across complex and dynamic manipulation tasks, achieving almost 10 Hz end-to-end inference on Jetson Orin, without relying on graph-level optimizations or runtime conversion techniques. 

## **2. RELATED WORKS** 

### **2.1. Efficiency Challenges in VLA Models** 

Prior work has explored improving the computational efficiency of Vision-Language-Action (VLA) models across several dimensions, such as fewer visual tokens [16, 22], fewer diffusion steps [38], and reduced transformer depth or attention computation [36, 42, 43]. These directions are largely orthogonal and can be combined in principle. A particularly active line of work [16, 22, 34, 37] focuses on 

reducing the number of visual tokens through pruning or caching, which can substantially reduce floating-point operations. However, the resulting wall-clock latency improvements can be workload-dependent, as modern accelerators efficiently parallelize token-wise computation [12, 39]. In contrast, transformer layers are executed sequentially, and in diffusion-based VLAs the action head is invoked repeatedly across denoising steps, making model depth a critical factor for real-time inference. We defer a quantitative comparison of these two efficiency axes to Section 3.2. 

### **2.2. Layer Reduction in VLA Models** 

Several methods directly target transformer depth using training-free or test-time strategies. DeeR-VLA [42] proposes an early-exit mechanism by dynamically measuring inter-layer feature similarity, while EfficientVLA [39] ranks transformer layers based on cosine similarity to identify redundant computation. However, such similarity-based criteria fail to capture the semantic role of layer depth [11] (e.g., early, middle, or late layers). Moreover, existing evaluations primarily focus on decoder-only transformer architectures (e.g., OpenVLA [20]) or reduce only the VLM backbone, even when flow-based models are considered (see Figure 1-(a,b)). Moreover, as observed in the image domain [32, 41], layer redundancy in flow-based models varies with the noise level across diffusion steps. As a result, a fixed or manually tuned threshold cannot reliably capture layer importance across both transformer depth and diffusion time. Finally, these approaches have not been validated in real-world robotic deployments, and are typically evaluated only in simulations. 

Beyond test-time thresholding, MoLE-VLA [43] introduces a training-based router mechanism to conditionally skip layers. However, this approach is applied only to the VLM backbone and still requires the full model to remain resident in memory at inference time. Such conditional execution also hinders efficient batch inference, as different 

inputs may activate different execution paths, and typically relies on surrogate gradient estimators to train discrete routing decisions, which can introduce additional optimization instability [14]. Furthermore, input-dependent routing introduces dynamic control flow, which complicates aheadof-time compilation and graph-level optimization on embedded platforms [14]. 

### **2.3. Knowledge Distillation in Other Domains** 

Knowledge distillation has been extensively studied as an effective approach for reducing model size and inference cost while preserving performance in language, vision, and multimodal models. In language and vision-language models, distillation methods such as DistilBERT [31] and MobileVLM [7] have consistently demonstrated that compact student models distilled from large teachers outperform models trained from scratch with comparable capacity. More recent studies extend distillation to multimodal settings by transferring cross-modal alignment and attention structure [11, 18]. Distillation has also been explored for improving the efficiency of diffusion transformers by reducing model depth or structural complexity. Prior work proposes training shallow diffusion transformers [10, 32], distilling contiguous groups of layers [25], or adaptively selecting layers during training [41]. However, these approaches have not been studied in VLA architectures that employ a separate vision–language backbone and a diffusion-based action head, where only action tokens participate in the denoising process. Moreover, their effectiveness has not been validated on real-world robotic systems. 

## **3. Preliminaries** 

### **3.1. Flow-based VLAs** 

Flow-based Vision–Language–Action (VLA) models generate continuous robot actions by learning a conditional vector field that transports noise to action trajectories. Given an observation _o_ , language instruction _l_ , and a ground-truth action _a_ (represented as a concatenated action chunk), a noisy interpolation is constructed as _aτ_ = _τa_ +(1 _−τ_ ) _ϵ_ , where _ϵ ∼N_ (0 _, I_ ) and _τ ∈_ [0 _,_ 1]. The model _vθ_ ( _aτ , o, l, τ_ ) is trained via flow matching to predict the target velocity _u_ = _a − ϵ_ by minimizing E[ _∥vθ_ ( _aτ , o, l, τ_ ) _− u∥_<sup>2</sup> 2<sup>].</sup> Following _π_ 0 [4] and _π_ 0 _._ 5 [15], _vθ_ consists of a vision–language transformer backbone that encodes multimodal tokens from _o_ and _l_ , and a transformer-based action head that processes _aτ_ together with state information. During inference, key–value pairs from the vision–language backbone can be cached and reused across diffusion steps, since attention from vision–language tokens to action tokens is masked out, while action tokens attend to fixed vision–language representations. Actions are generated by numerically integrating the learned vector field from _τ_ = 0 


Figure 2. CUDA inference time as a function of transformer depth and visual token count. Measurements are obtained using the _π_ 0 _._ 5 model trained on LIBERO, evaluated on an H100 GPU (left) and Jetson Orin (right). 

to _τ_ = 1 using a finite number of diffusion steps. Throughout the remainder of this paper, we adopt the notation introduced in this section when discussing flow-based VLA models. 

### **3.2. Impact of Layer Reduction on Latency** 

In this section, we analyze inference latency in flowbased VLAs by varying transformer depth and visual token count, highlighting the relative advantage of layer reduction on modern GPUs, where token-level computation is highly parallelized but transformer layers remain sequential. Figure 2 compares the latency reduction achieved by decreasing transformer depth versus reducing the number of visual tokens per image. For this benchmark, we use torch.compile to optimize inference [8], and report results on both H100 and Jetson Orin, representing the high and low ends of computational capability. We set the maximum reduction boundaries to 4 transformer layers and 64 visual tokens, following the most aggressive reductions reported in recent work [7, 39]. 

While token reduction yields only modest latency improvements, reducing the number of transformer layers leads to a substantially larger decrease in inference time. This trend reflects the highly parallel nature of token-level computation on modern GPUs, in contrast to the strictly sequential execution of transformer layers, whose costs accumulate directly in wall-clock time. This effect is particularly evident on high-performance hardware such as the H100, where token reduction provides minimal benefit. Overall, these results highlight the unique effectiveness of transformer layer reduction as a means of improving inference latency. 

## **4. Why Layer Skipping Is Insufficient** 

Motivated by the computational advantages of transformer depth reduction, prior work proposes _test-time layer skipping_ for OpenVLA-style models based on feature similarity or learned routing mechanisms [39, 40, 42, 43], either skipping redundant layers or dynamically selecting lay- 


Figure 3. (Top) Feature similarity trend along noise level _τ_ . (Bottom) Layer sensitivity analysis of _π_ 0 _._ 5 on the LIBERO benchmark. The bar chart shows the decrease in average success rate caused by skipping individual layers. 

ers to bypass. We examine whether these approaches remain effective for _π_ -like flow-based VLAs, which inject visual–language features at every transformer layer. As a representative example of skipping based on feature similarity, EfficientVLA [39] uses cosine similarity between adjacent layers to decide whether layers can be skipped. As depicted in Figure 3, we analyze layer-wise cosine similarity of _π_ 0 _._ 5 across denoising timesteps _τ_ and perform layer sensitivity analysis measuring averaged LIBERO success rate when individual layers are skipped. 

Our results reveal two limitations of this approach. First, similarity profiles vary substantially with _τ_ , making fixed skipping rules brittle. For example, although overall similarity at _τ_ = 0 is lower than at _τ_ = 1 in early and late layers, this trend is not consistent across all depths (e.g., layer 13 _→_ 14), preventing a simple or monotonic thresholding strategy conditioned on _τ_ . Second, similarity poorly predicts functional importance: despite higher similarity between layers 1 and 2 than between layers 16 and 17, skipping the former leads to a much larger drop in success rate. This confirms that similarity-based criteria alone are insufficient, consistent with prior findings that different transformer layers serve distinct roles [11]. 

We further consider learned routing as an alternative by using layer sensitivity as an oracle for layer selection. Progressively removing layers in order of lowest sensitivity (e.g., 13 _→_ 15 _→_ 16 _→_ 11 _→· · ·_ ) causes the success rate to collapse once more than three layers are removed (Figure 4). Taken together, these results indicate that test-time layer skipping—via similarity metrics or routing—is fundamentally limited for flow-based VLAs, where layer functionality is tightly coupled with denoising dynamics [32, 41]. This motivates our use of _knowledge distillation_ for effective and aggressive layer reduction, rather than relying on complex threshold heuristics or routing mechanisms. 


Figure 4. Success rate (%) on LIBERO (Spatial, Object, Goal, and 10) as a function of the number of skipped transformer layers. 

## **5. Knowledge Distillation for Shallow Layers** 

Given a pretrained flow-based VLA policy _vϕ_ , our goal is to obtain a student model _vθ_ with substantially fewer transformer layers, while preserving action generation performance. The student is trained to approximate the teacher’s denoising behavior through a combination of task supervision and knowledge distillation losses, as illustrated in Figure 5. To initialize the shallow student, we reduce the number of transformer layers in both the vision–language backbone and the action head using a uniform subsampling strategy, following TinyBERT-style layer initialization [17]. We observe no additional benefit from selecting initialization layers based on the sensitivity analysis in the bottom of Figure 3, provided the model is trained for a sufficient number of steps. 

### **5.1. Distillation Objectives** 

We train the student model _vθ_ using a combination of three complementary losses. First, the task loss _L_ task follows standard flow matching and supervises the student to predict the ground-truth velocity. 


Second, a knowledge distillation loss _L_ kd encourages the student to match the teacher’s predicted velocity, offering informative teacher-generated guidance. 


Finally, we introduce a novel attention distillation loss _L_ attn that is carefully designed for the multimodal VLA architecture, aligning the cross-attention distributions between action queries and vision–language key–value pairs at an intermediate transformer layer: 


where Attn<sup>_a→vl_</sup> = softmax� _Q_<sup>_a_</sup> _K_<sup>_vl⊤_�</sup> , and the KL is KL divergence is evaluated over the corresponding attention 


Figure 5. Shallow- _π_ reduces the transformer depth of the VLM backbone and action head via knowledge distillation, using three loss terms to match ground-truth actions, teacher outputs, and intermediate cross-attention between the backbone and action head. 

distribution across vision–language tokens for each action token. Together, these three losses promote both outputlevel consistency and representation alignment between the teacher and the shallow student. 

### **5.2. Attention Distillation** 

In contrast to prior attention distillation approaches in LLMs and VLMs, we do not enforce attention matching over the full token set (i.e., Attn<sup>_vl→vl_</sup> ). This choice is motivated by the structure of flow-matching VLAs, where only action tokens define the generative policy, while visual and language tokens from the VLM backbone serve purely as conditioning context. Distilling attention over non-generated backbone tokens over-constrains the student and introduces interference with pre-trained representations, without improving control fidelity. Empirically, we observe that matching attention across all tokens consistently leads to unstable training and near-zero success rates in the final policy (see Table 1-(c)). Also, for more efficient and flexible optimization, we take inspiration from AlignKD [11] which applies attention transfer only at a specific layer, rather than for the whole layers. We apply attention distillation at a middle transformer layer rather than at early or late stages. Because the student is initialized by directly copying the bottom layers of the teacher, early-layer representations are already closely aligned and provide limited additional supervision. At the final layer, output matching is already enforced through _L_ task and _L_ kd, making further alignment redundant. 

### **5.3. Ablations** 

Based on the _π_ 0 _._ 5 model trained on the LIBERO benchmark [24], we conduct ablation studies on both the loss components and the transformer layer at which _L_ attn in Eq. 3 is applied. Across all experiments, we use the same teacher model and train the student for 30K steps with a batch size of 64. As shown in Table 1, the composite loss formulation combined with applying attention distillation at the middle 

Table 1. Ablations for loss design 

|(a) Loss ab|lation on|Shallo|w|_π_0_._5 with differ|ent depths|
|---|---|---|---|---|---|
|_L_task|_L_kd|_L_attn||**L9**<br>**L6**|**L4**|
|✓|✗|✗||95.4<br>93.0|92.3|
|✓|✓|✗||96.2<br>93.9|93.9|
|✓|✓|✓||**96.8**<br>**94.6**|**94.2**|


|(b) Attention distillation|placement (L=nu|mber of layers).|
|---|---|---|
||**L9**<br>**L6**|**L4**|
|Initial layer|94.4<br>93.9|91.0|
|Middle layer|**96.8**<br>**94.6**|**94.2**|
|Later layer|95.6<br>94.1|92.8|
|(c) Attention distill|ation target queri|ed tokens.|
||**L9**<br>**L**|**6**<br>**L4**|
|Action tokens onl|y<br>96.8<br>94|.6<br>93.9|
|All tokens|0.0<br>61|.5<br>0.0|


layer yields the best performance. 

## **6. Experiment** 

We validate Shallow- _π_ on both simulation benchmarks and real-world experiments across multiple challenging scenarios. Through these evaluations, we aim to answer the following questions: 

- Despite aggressive transformer layer reduction and latency improvement, does Shallow- _π_ preserve the teacher’s capabilities across a broad range of task prompts? 

- Is knowledge distillation a more effective approach than training a compact model from scratch? 

- Does Shallow- _π_ demonstrate sufficient real-world performance when deployed on edge devices for complex and dynamic tasks? 

- Does Shallow- _π_ retain generalization capability on unseen tasks without overfitting to the distillation dataset? 

### **6.1. Simulation Benchmark** 

We evaluate our method on the LIBERO benchmark using simulation. Teacher models based on _π_ 0 and _π_ 0 _._ 5 are trained for 30k steps with a batch size of 64, using only two input images (a third-person camera and a wrist camera). We changed the official code implementation of [4, 15] to skip the third image input entirely, rather than leaving it as a black image. The student models are distilled using the same training setup. The results are summarized in Table 2. As shown in the table, the distilled models achieve suc- 


Figure 6. Experiment task suites for Shallow- _π_ . The benchmarks include scenarios requiring complex manipulation under dynamic scenes, as well as tasks involving articulated robot platforms with coordinated hand and torso movements. All real-world evaluations are performed on edge devices (Jetson Thor and Orin). 

cess rates within 1% drop of their teachers, while reducing both FLOPs and CUDA inference time by more than a factor of two. Although orthogonal to our direction, shallow flow models require significantly less computation—in terms of both FLOPs and CUDA latency—than state-of-the-art token compression methods for comparable success rates. Distilling high-capacity flow models also yields marginally better performance than small-backbone approaches such as SmolVLA [33]. In addition, shallow- _π_ models exhibit lower inference latency than SmolVLA, whose action head contains 16 transformer layers. These results confirm that distilling high-capacity models is more effective than training small backbones from scratch, and that jointly reducing the depth of both the VLM and action head leads to superior efficiency. Overall, considering its straightforward implementation—without complex manual layer selection [39, 42] or sophisticated routing mechanisms [22, 43]—shallow- _π_ achieves the best trade-off be- 


Figure 7. Degrees of freedom (DoFs) and camera configurations (green circles) for the robot platforms. 


Figure 8. Skill sequences required by the tasks of the hand-typed robot (RB-Y1). 


Figure 9. (Top) Flow matching loss vs training step. (Bottom) Samples of chunk to compare the motion quality in the real-world training set. 

tween success rate and computational efficiency. 

### **6.2. Real-World Experiment** 

We evaluate Shallow- _π_ in challenging scenarios requiring high computational efficiency, precise control, and strong generalization. As shown in Figure 6, experiments are conducted on two robot platforms, ALOHA [13] and RB-Y1, using only onboard sensors without static third-person cam- 

Table 2. Success rates (SR) are reported on the LIBERO benchmark, and computation is measured on an NVIDIA H100. Best results are shown in bold, and second-best results are underlined. All numbers are rounded. 

|**Group**|**Model**|**Spatial**|**Object**|**Goal**|**Long (10)**|**Avg**_↑_|**FLOPs (T)**_↓_|**CUDA Time (ms)**_↓_|
|---|---|---|---|---|---|---|---|---|
|Bli|_π_0 [4]|97|97|93|92|95|2.93|22.6|
|asene|_π_0_._5 [15]|98|96|97|93|96|3.39|25.5|
|Token Compression|CogVLA [22]|**99**|**99**|97|**95**|**97**|2.70|31.0|
|(orthogonal to ours)|LightVLA [16]|98|98|**98**|**95**|**97**|2.91|22.0|
|Small Backbone|SmolVLA [33]|90|96|92|71|87|**0.50**|26.0|
||_π_0-L9|98|98|95|87|95|1.62|13.5|
|Layer Distillation|_π_0-L6|98|95|93|85|94|1.18|**10.5**|
|(ours)|_π_0_._5-L9|**99**|98|97|93|**97**|1.82|14.8|
||_π_0_._5-L6|98|96|94|90|95|1.30|11.3|


Table 3. Task performance across dynamic, complex, and unseen settings. 

|Dynamic|Tasks (Jetso|n Orin)||
|---|---|---|---|
|Task<br>Sm|olVLA|_π_0|Shallow-_π_0|
|Peg in hole|0/10|7/10|**10/10**|
|Insert foam|1/10|5/10|**7/10**|
|Scoop apple|5/10|6/10|**9/10**|
|Pour beans|6/10|5/10|**8/10**|
|E2E Comp. (ms)|230|364|**110**|
|Hands and|Torso (Jets|on Tho|r)|
|Task|_π_0_._5|Sh|allow-_π_0_._5|
|Recycle|12/20||**17/20**|
|Open lid & peg (A)|5/10||**7/10**|
|Open lid & peg (B)|1/5||**5/5**|
|E2E Comp. (ms)|130||**78**|
|Unsee|n Environm|ents||
|Task|_π_|Shallo|w-_π_(L6)|
|Peg in hole (_π_0)|0/5||**3/5**|
|Recycle (_π_0_._5)|8/20|**1**|**5/20**|


eras (see Figure 7). In experiments with ALOHA, we primarily rely on the left wrist camera to observe salient objects and target locations, as shown in the _Peg in hole_ task in Figure 6. We train separate models for ALOHA ( _π_ 0) and RB-Y1 ( _π_ 0 _._ 5) to account for their different degrees of freedom and embodiments. For both teacher training and distillation, we use a batch size of 128 and train for 100K steps. During distillation, the student model is configured 

with 6-transformer layers. We perform model inference on Jetson Orin and Jetson Thor for the ALOHA and RB-Y1 platforms, respectively. We compare Shallow- _π_ with its teacher and SmolVLA [33]. SmolVLA is trained until the convergence, allowing all parameters, including the vision encoder, to be trainable following the findings in [20]. For real-robot deployment, we use an action chunk size of 50 with a 30 Hz control loop. At each step, the robot executes 7 actions before requesting the next model inference in a receding-horizon manner, continuing to execute the remaining actions from the previous chunk while awaiting the new prediction. Temporal ensembling [44] is applied to ensure smooth action execution. As noted in [5], slow inference increases open-loop execution on stale observations, which can lead to non-recoverable failure states. High inference latency also amplifies discrepancies between old and newly predicted action chunks, reducing execution precision when temporal smoothing is applied. 

As depicted in Figure 6, we design the following 6 test cases. 

- _Peg in hole_ (92 episodes): The ALOHA robot approaches and grasps a cylindrical peg, then inserts it into dynamically moving small holes. 

- _Insert foam_ (100 episodes): The ALOHA robot grasps a square foam block and places it onto a moving bookshelf. The foam must be released when its edge is aligned with the shelf geometry. 

- _Scoop and place apple_ (190 episodes): The ALOHA robot grasps a scooping tool to collect an apple and then deposits it into a moving box. 

- _Pour beans into box_ (100 episodes): The ALOHA robot grasps the handle of a cup filled with beans and pours the contents into a moving box. 

- _Recycle_ (2,600 episodes total): The RB-Y1 robot grasps trash objects and throws them into the appropriate bins. The training set includes a diverse set of trash objects, 


Figure 10. Histogram of the per-frame average translation of the right-arm end effector in the training dataset. 


Figure 11. Experimental snapshots illustrating open-loop failures of the teacher model, where the student model achieves better performance by reacting to observations more rapidly. 

while evaluation is conducted on a fixed subset (see the skill sequence in Figure 8). 

- _Open lid & peg cylinder (Type A)_ (436 episodes): The RB-Y1 robot opens a lid, extracts a cylinder using appropriate finger configurations, and places it into a corresponding hole. 

- _Open lid & peg cylinder (Type B)_ (214 episodes): The robot extracts a cylinder from a confined hole using torso rotation and places it into the target location. Compared to Type A, this variant requires precise arm control to extract a deeply inserted cylinder. 

As summarized in Table 3, Shallow- _π_ consistently achieves better real-world performance across all tasks, primarily due to reduced inference latency while preserving model capability. For the ALOHA platform, the distilled model reduces inference time by more than 200 ms (approximately 6 frames) compared to the teacher, which corresponds to over 2 cm of additional open-loop translation of the end-effector on average, as illustrated in Figure 10. Given that the linear speed at the edge of the turntable is approximately 0.8 cm/s, this prolonged open-loop motion measurably degrades placement precision, a trend that is reflected in the experimental results. As shown in the training curves in Figure 9, SmolVLA exhibits a flow-matching loss approximately twice that of Shallow- _π_ , and correspondingly produces noisier and less precise actions, as illustrated 

in the bottom row of Figure 9 and in Table 3 In contrast, the distilled Shallow- _π_ model demonstrates strong robustness and generalization, achieving over 80% success on the recycle task, which requires reliable grasping of objects across diverse poses. 

We further investigate whether the proposed distillation preserves generalization capacity without overfitting to the training data despite the reduced model size. To this end, we evaluate the models under two unseen perturbation scenarios, as shown in Figure 11. First, we shift the initial position of the cylinder in the _peg in hole_ task on ALOHA by 3 cm, creating an unseen object configuration. Second, we displace each trash bin by more than 10 cm in the _recycle_ task. We observe that increased open-loop execution in the teacher model often prevents correction of picking or releasing poses, as illustrated in the first row of Figure 11. In contrast, the distilled model achieves better performance by incorporating updated visual observations more frequently, demonstrating improved robustness and generalization under unseen spatial perturbations. 

## **7. CONCLUSIONS** 

In this work, we introduced Shallow- _π_ , an efficient knowledge distillation framework for flow-based VLA models that inject conditioning information at all intermediate layers. Our results show that the distilled model preserves the performance and generalization capability of the teacher while significantly reducing computation through aggressive transformer layer reduction. Also, compared to the models with a small backbone, the distilled model acheived better performance in denoising and the precision. We validated the effectiveness of Shallow- _π_ through real-world deployment on edge devices, demonstrating reliable performance under practical latency constraints. 

Our work is not without limitations. First, compared to layer-skipping approaches, knowledge distillation incurs higher training-time computational costs, as both teacher and student models must be loaded simultaneously. To mitigate this overhead, future work should investigate more effective strategies for selectively freezing model components to reduce VRAM consumption during distillation, as well as curating or filtering key training samples that provide the most informative supervision. Looking ahead, we also plan to explore complementary efficiency axes—such as visual token reduction and diffusion step reduction—to further improve inference throughput. 

## **References** 

- [1] Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Kevin Black, Ken Conley, Grace Connors, James Darpinian, Karan Dhabalia, Jared DiCarlo, Danny Driess, et al. Pi*0 _._ 6: A vla that learns from experience. _arXiv preprint arXiv:2511.14759_ , 2025. 1 

- [2] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _CoRR_ , 2024. 1 

- [3] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _CoRR_ , 2025. 

   - 1 

- [4] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. pi0: A vision-languageaction flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 1, 3, 5, 7 

- [5] Kevin Black, Manuel Y Galliker, and Sergey Levine. Realtime execution of action chunking flow policies. _arXiv preprint arXiv:2506.07339_ , 2025. 7 

- [6] Zhe Chen, Jiannan Wu, Wenhai Wang, Weijie Su, Guo Chen, Sen Xing, Muyan Zhong, Qinglong Zhang, Xizhou Zhu, Lewei Lu, et al. Internvl: Scaling up vision foundation models and aligning for generic visual-linguistic tasks. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 24185–24198, 2024. 1 

- [7] Xiangxiang Chu, Limeng Qiao, Xinyang Lin, Shuang Xu, Yang Yang, Yiming Hu, Fei Wei, Xinyu Zhang, Bo Zhang, Xiaolin Wei, et al. Mobilevlm: A fast, strong and open vision language assistant for mobile devices. _arXiv preprint arXiv:2312.16886_ , 2023. 3 

- [8] Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, and Christopher R´e. Flashattention: Fast and memory-efficient exact attention with io-awareness, 2022. 3 

- [9] Zhiying Du, Bei Liu, Yaobo Liang, Yichao Shen, Haidong Cao, Xiangyu Zheng, Zhiyuan Feng, Zuxuan Wu, Jiaolong Yang, and Yu-Gang Jiang. Himoe-vla: Hierarchical mixture-of-experts for generalist vision-language-action policies. _arXiv preprint arXiv:2512.05693_ , 2025. 1 

- [10] Gongfan Fang, Kunjun Li, Xinyin Ma, and Xinchao Wang. Tinyfusion: Diffusion transformers learned shallow. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 18144–18154, 2025. 3 

- [11] Qianhan Feng, Wenshuo Li, Tong Lin, and Xinghao Chen. Align-kd: Distilling cross-modal alignment knowledge for mobile vision-language large model enhancement. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 4178–4188, 2025. 2, 3, 4, 5 

- [12] Jared Fernandez, Jacob Kahn, Clara Na, Yonatan Bisk, and Emma Strubell. The framework tax: Disparities between inference efficiency in nlp research and deployment. _arXiv preprint arXiv:2302.06117_ , 2023. 2 

- [13] Zipeng Fu, Tony Z Zhao, and Chelsea Finn. Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation. _arXiv preprint arXiv:2401.02117_ , 2024. 6 

- [14] Yizeng Han, Gao Huang, Shiji Song, Le Yang, Honghui Wang, and Yulin Wang. Dynamic neural networks: A survey. _IEEE transactions on pattern analysis and machine intelligence_ , 44(11):7436–7456, 2021. 3 

- [15] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. pi0.5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 1, 3, 5, 7 

- [16] Titong Jiang, Xuefeng Jiang, Yuan Ma, Xin Wen, Bailin Li, Kun Zhan, Peng Jia, Yahui Liu, Sheng Sun, and Xianpeng Lang. The better you learn, the smarter you prune: Towards efficient vision-language-action models via differentiable token pruning. _arXiv preprint arXiv:2509.12594_ , 2025. 2, 7 

- [17] Xiaoqi Jiao, Yichun Yin, Lifeng Shang, Xin Jiang, Xiao Chen, Linlin Li, Fang Wang, and Qun Liu. Tinybert: Distilling bert for natural language understanding. In _Findings of the association for computational linguistics: EMNLP 2020_ , pages 4163–4174, 2020. 4 

- [18] Jiwan Kim, Kibum Kim, Sangwoo Seo, and Chanyoung Park. Compodistill: Attention distillation for compositional reasoning in multimodal llms. _arXiv preprint arXiv:2510.12184_ , 2025. 3 

- [19] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success, 2025. 1 

- [20] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P Foster, Pannag R Sanketi, Quan Vuong, et al. Openvla: An open-source vision-language-action model. In _Conference on Robot Learning_ , pages 2679–2713. PMLR, 2025. 2, 7 

- [21] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational visionlanguage-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 1 

- [22] Wei Li, Renshan Zhang, Rui Shao, Jie He, and Liqiang Nie. Cogvla: Cognition-aligned vision-language-action model via instruction-driven routing & sparsification. _arXiv preprint arXiv:2508.21046_ , 2025. 1, 2, 6, 7 

- [23] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 1 

- [24] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 5 

- [25] Jian Ma, Qirong Peng, Xujie Zhu, Peixing Xie, Chen Chen, and Haonan Lu. Pluggable pruning with contiguous layer distillation for diffusion transformers. _arXiv preprint arXiv:2511.16156_ , 2025. 3 

- [26] Yunchao Ma, Yizhuang Zhou, Yunhuan Yang, Tiancai Wang, and Haoqiang Fan. Running vlas at real-time speed. _arXiv preprint arXiv:2510.26742_ , 2025. 1 

- [27] Minho Park, Kinam Kim, Junha Hyung, Hyojin Jang, Hoiyeong Jin, Jooyeol Yun, Hojoon Lee, and Jaegul Choo. Acg: Action coherence guidance for flow-based vla models. _arXiv preprint arXiv:2510.22201_ , 2025. 1 

- [28] Seongmin Park, Hyungmin Kim, Wonseok Jeon, Juyoung Yang, Byeongwook Jeon, Yoonseon Oh, and Jungwook 

Choi. Quantization-aware imitation-learning for resourceefficient robotic control. _arXiv preprint arXiv:2412.01034_ , 2024. 1 

- [29] William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 4195–4205, 2023. 1 

- [30] Aaditya Prasad, Kevin Lin, Jimmy Wu, Linqi Zhou, and Jeannette Bohg. Consistency policy: Accelerated visuomotor policies via consistency distillation. _arXiv preprint arXiv:2405.07503_ , 2024. 1 

- [31] Victor Sanh, Lysandre Debut, Julien Chaumond, and Thomas Wolf. Distilbert, a distilled version of bert: smaller, faster, cheaper and lighter. _arXiv preprint arXiv:1910.01108_ , 2019. 3 

- [32] Xuan Shen, Zhao Song, Yufa Zhou, Bo Chen, Yanyu Li, Yifan Gong, Kai Zhang, Hao Tan, Jason Kuen, Henghui Ding, et al. Lazydit: Lazy learning for the acceleration of diffusion transformers. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , pages 20409–20417, 2025. 2, 3, 4 

- [33] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, et al. Smolvla: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 1, 6, 7 

model inference via dynamic-static layer-skipping for robot manipulation. 3 

   - [41] Haoran You, Connelly Barnes, Yuqian Zhou, Yan Kang, Zhenbang Du, Wei Zhou, Lingzhi Zhang, Yotam Nitzan, Xiaoyang Liu, Zhe Lin, et al. Layer-and timestep-adaptive differentiable token compression ratios for efficient diffusion transformers. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 18072–18082, 2025. 2, 3, 4 

   - [42] Yang Yue, Yulin Wang, Bingyi Kang, Yizeng Han, Shenzhi Wang, Shiji Song, Jiashi Feng, and Gao Huang. Deer-vla: Dynamic inference of multimodal large language models for efficient robot execution. _Advances in Neural Information Processing Systems_ , 37:56619–56643, 2024. 1, 2, 3, 6 

   - [43] Rongyu Zhang, Menghang Dong, Yuan Zhang, Liang Heng, Xiaowei Chi, Gaole Dai, Li Du, Yuan Du, and Shanghang Zhang. Mole-vla: Dynamic layer-skipping vision language action model via mixture-of-layers for efficient robot manipulation. _arXiv preprint arXiv:2503.20384_ , 2025. 1, 2, 3, 6 

   - [44] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 7 

- [34] Hanzhen Wang, Jiaming Xu, Jiayi Pan, Yongkang Zhou, and Guohao Dai. Specprune-vla: Accelerating vision-languageaction models via action-aware self-speculative pruning. _arXiv preprint arXiv:2509.05614_ , 2025. 1, 2 

- [35] Yihao Wang, Pengxiang Ding, Lingxiao Li, Can Cui, Zirui Ge, Xinyang Tong, Wenxuan Song, Han Zhao, Wei Zhao, Pengxu Hou, et al. Vla-adapter: An effective paradigm for tiny-scale vision-language-action model. _arXiv preprint arXiv:2509.09372_ , 2025. 1 

- [36] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Zhibin Tang, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, et al. Tinyvla: Towards fast, data-efficient visionlanguage-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025. 1, 2 

- [37] Siyu Xu, Yunke Wang, Chenghao Xia, Dihao Zhu, Tao Huang, and Chang Xu. Vla-cache: Efficient visionlanguage-action manipulation via adaptive token caching, 2025. 1, 2 

- [38] Ge Yan, Jiyue Zhu, Yuquan Deng, Shiqi Yang, Ri-Zhao Qiu, Xuxin Cheng, Marius Memmel, Ranjay Krishna, Ankit Goyal, Xiaolong Wang, et al. Maniflow: A general robot manipulation policy via consistency flow training. In _Conference on Robot Learning_ , pages 2268–2293. PMLR, 2025. 1, 2 

- [39] Yantai Yang, Yuhao Wang, Zichen Wen, Luo Zhongwei, Chang Zou, Zhipeng Zhang, Chuan Wen, and Linfeng Zhang. Efficientvla: Training-free acceleration and compression for vision-language-action models. _arXiv preprint arXiv:2506.10100_ , 2025. 1, 2, 3, 4, 6 

- [40] Zebin Yang, Yijiahao Qi, Tong Xie, Bo Yu, Shaoshan Liu, and Meng Li. Dysl-vla: Efficient vision-language-action 

