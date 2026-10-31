---
title: "DTP: A Simple yet Effective Distracting Token Pruning Framework for Vision-Language Action Models"
date: "2026-01-22"
authors: "Chenyang Li; Jieyuan Liu; Bin Li; Bo Gao; Yilin Yuan; Yangfan He"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2601.16065
pdf: https://arxiv.org/pdf/2601.16065
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.16065)** / [論文ページ](https://arxiv.org/abs/2601.16065)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Preprint 

# DTP:A SIMPLE YET EFFECTIVE DISTRACTING TOKEN PRUNING FRAMEWORK FOR VISION-LANGUAGE ACTION MODELS 

**Chenyang Li**<sup>1</sup> **, Jieyuan Liu**<sup>2</sup> **, Bin Li**<sup>3</sup> **, Bo Gao**<sup>4</sup> **, Yilin Yuan**<sup>4</sup> **, Yangfan He**<sup>5</sup> **, Yuchen Li**<sup>6</sup> **, Jingqun Tang**<sup>7</sup> 

> 1 **Australian National University,** 2 **University of California, San Diego,** 3 **Chinese Academy of Sciences,** 

> 4 **Beijing Institute of Graphic Communication,** 5 **University of North Carolina at Chapel Hill,** 

> 6 **Baidu Search,** 7 **Bytedance** 


Figure 1: **Overview of our proposed Distracting Token Pruning (DTP) method for improving Vision-LanguageAction (VLA) models in robotic manipulation.** Left: Input consisting of the current visual observation and natural language instruction. Middle: Comparison between the original VLA model (top) may focus on task-irrelevant regions that lead to task failure, while our DTP-enhanced approach (bottom) creates more focused attention on task-critical areas, leading to the improvements in the task success rate. 

## ABSTRACT 

Vision-Language Action (VLA) models have shown remarkable progress in robotic manipulation by leveraging the powerful perception abilities of Vision-Language Models (VLMs) to understand environments and directly output actions. However, by default, VLA models may overly attend to image tokens in the task-irrelevant region, which we describe as ‘distracting tokens’. This behavior can disturb the model from the generation of the desired action tokens in each step, affecting the success rate of tasks. In this paper, we introduce a simple yet effective plug-and-play **D** istracting **T** oken **P** runing (DTP) framework, which dynamically detects and prunes these distracting image tokens. By correcting the model’s visual attention patterns, we aim to improve the task success rate, as well as exploring the performance upper boundaries of the model without altering its original architecture or adding additional inputs. Experiments on the SIMPLER Benchmark (Li et al., 2024) show that our method consistently achieving relative improvements in task success rates across different types of novel VLA models, demonstrating generalizability to transformerbased VLAs. Further analysis reveals a negative correlation between the task success rate and the amount of attentions in the task-irrelevant region for all models tested, highlighting a common phenomenon of VLA models that could guide future research. We also publish our code at: https://anonymous.4open.science/r/CBD3. 

1 

Preprint 

## 1 INTRODUCTION 

The success of Vision-Language Models (VLMs) in understanding and reasoning about visual content has opened new possibilities for embodied AI. Trained on large-scale image–text data, VLMs (Liu et al., 2023b; Karamcheti et al., 2024; Beyer et al., 2024; Lu et al., 2024; Malartic et al., 2024; Chen et al., 2025; Bai et al., 2025) excel at visual recognition, reasoning, and visual question answering. Building on this, Vision-Language-Action (VLA) models extend VLMs to generate executable robot actions, bridging high-level semantic reasoning with low-level control. Early VLAs such as RT-1 (Brohan et al., 2023b) and RT-2 (Brohan et al., 2023a) pioneered action tokenization for robotic control, while later models like OpenVLA (Kim et al., 2024) achieved strong performance despite smaller sizes. These advances established the core VLA pipeline: a visual encoder (Radford et al., 2021; Sun et al., 2023; Zhai et al., 2023; Oquab et al., 2024), a language model (Touvron et al., 2023; Dai et al., 2024; Qwen et al., 2025), and discrete action token generation. 

Recent works further improve VLA capabilities. SpatialVLA (Qu et al., 2025) and (Sun et al., 2025; Lin et al., 2025; Li et al., 2025) incorporate depth for better 3D understanding, Nora (Hung et al., 2025) employs tokenizers such as FAST (Pertsch et al., 2025) for precise continuous control, and world-model approaches (Cen et al., 2025; Wang et al., 2025) leverage dynamics modeling for action prediction. Despite these architectural advances, VLAs may still fail in manipulation tasks due to redundant visual tokens, with task-irrelevant visual tokens may receive disproportionately high attention during cross-attention, distracting the model from task-relevant regions (Figure 1). This raises a concern: _Do distracting tokens affect task success, and can pruning them improve performance?_ 

We initially tried manually inspecting visual attention patterns and pruning image tokens for the model. However, this approach has two major limitations: (1) reviewing attention by human for each action token is extremely timeconsuming, especially since the model can output hundreds to thousands action tokens for each episode, making full test-suite analysis impractical; (2) human intuition about ”good” attention patterns may not align with the model’s preferences. Although ideal attention should focus on task-relevant objects and regions, different VLA models may have their own visual pattern preference, so manual pruning does not necessarily lead to improved performance. 

To address these two problems, we propose **Distracting Token Pruning (DTP)** , a plug-and-play framework that dynamically prunes distracting tokens. DTP contains three stages: (1) Relevance-based important region construction, where prompt–image token interactions identify task-relevant visual tokens, and (2) Action attention analysis, where the attention heatmap reveals which image tokens the model focuses at each action generation step. (3) We then apply an intersection-based strategy, selectively pruning visual tokens in the unimportant region, if their attention exceeds the maximum attention within the important region (scaled by tolerance _τ_ ). Experiments on the SIMPLER Benchmark (Li et al., 2024) prove that DTP effectively corrects visual attention patterns, improves task success rates, and generalizes across transformer-based VLAs. 

In summary, our work makes the following contributions: (1) We introduce the Distracting Token Pruning (DTP) framework, a novel intersection-based method that automatically identifies and prunes distracting tokens, improving task success rates by addressing common attention weaknesses in VLA models. (2) We explore the performance upper bound of VLAs by varying tolerance _τ_ , seeking the ideal visual attention patterns that align with model preferences and maximize achievable performance. (3) We analyze attention values in unimportant regions, revealing a negative correlation with task success and offering insights for building more robust VLAs. 

## 2 RELATED WORK 

**Vision-Language Models (VLMs)** have become the foundation for multimodal reasoning, showing strong generalization across visual understanding, captioning, and visual question answering. Large-scale pretraining on internet-scale image–text data has enabled models such as PrismaticVLM Karamcheti et al. (2024), InternVL2.5 Chen et al. (2025), PaliGemma 2 Beyer et al. (2024), and Qwen2.5-VL Bai et al. (2025) to achieve impressive performance on various visual-language tasks. These models combine high-capacity visual encoders such as SigLIP Zhai et al. (2023) and DINOv2 Oquab et al. (2024) with large language models (Touvron et al., 2023; Dai et al., 2024; Qwen et al., 2025), producing flexible representations that can be adapted across a wide range of tasks. While primarily designed for static vision-language tasks, the success of VLMs in structured reasoning has inspired their extension into embodied AI domains. In particular, their ability to jointly ground natural language with perceptual input provides a natural interface for robotic control. This transition, however, requires not only high-level semantic understanding but also the capacity to map instructions and observations into temporally grounded motor actions — a gap that gave rise to Vision-Language-Action (VLA) models. 

2 

Preprint 

**Vision-Language-Action Models (VLAs)** extend the capabilities of VLMs by directly generating robot actions, effectively bridging perception and motor control. Early work such as RT-1 (Brohan et al., 2023b) and RT-2 (Brohan et al., 2023a) established the paradigm of representing actions as discrete tokens, enabling pretrained language models to output robot commands in a manner analogous to text generation. Building on this foundation, OpenVLA (Kim et al., 2024) and OpenVLA-OFT (Kim et al., 2025) further reduced the model size and improved inference efficiency. Recent efforts have pushed VLAs in two complementary directions. First, improvements in vision encoding aim to overcome limitations of purely 2D perception. SpatialVLA (Qu et al., 2025), GeoVLA (Sun et al., 2025), EVO-0 (Lin et al., 2025), and PointVLA (Li et al., 2025) incorporate the depth information for the objects in the input image, boosting spatial perception ability and yielding the increase in task success rate, Second, advances in action decoding focus on bridging the gap between discrete action tokens and continuous control. Models such as Nora (Hung et al., 2025), _π_ 0 _._ 5 (Intelligence et al., 2025), and _π_ 0-FAST (Pertsch et al., 2025) transform discrete token outputs into continuous action values, enabling more precise and faster execution. Beyond architectural refinements, new paradigms such as UniVLA (Wang et al., 2025) and WorldVLA (Cen et al., 2025) integrate world-modeling into the VLA framework. By jointly predicting future observations and generating actions, world models capture the underlying physics of the environment, which helps for more accurate action token generation. However, existing VLAs still face challenges where models may attend heavily to task-irrelevant tokens, a phenomenon that can degrade action quality and lower task success rates. Several works have attempted to mitigate visual noise or highlight task-relevant regions. For example, BYOVLA (Hancock et al., 2024) proposes a run-time observation intervention scheme that modifies the input image based on visual sensitivity, while Otter (Huang et al., 2025) introduces an architecture that learns text-aware feature filtering through additional model components and end-to-end training. While these approaches improve robustness, they operate either at the input level or require architectural redesign and training, making them less broadly applicable to existing VLA systems. This limitation motivates our work: developing inference-time, training-free, and architecture-agnostic methods to detect and prune these distracting tokens, thereby refining the model’s visual attention and improving the precision of action generation. 


Figure 2: **Detailed architecture of our Distracting Token Pruning (DTP) method for improving visual attention in Vision-Language-Action models** . The method consists of three main components: **(a) Important Region Construction** : Using selected transformer layers _C_ to calculate the relevance score between image and prompt tokens, which forms the task-related important region _G_ . **(b) Visual Attention Pattern Construction** : Creating the output to image token attention heatmap _A_ from all attention layers, weighted by the visual attention proportion. It captures where the model focuses when generating actions. **(c) Distracting Token Pruning** : For any image token in the unimportant region, if its attention value is greater than _τ · am_ , it will be treated as distracting tokens, and will be pruned. 

3 

Preprint 


Figure 3: **Visualization of the distracting token pruning process across different VLA models and tasks.** The figure shows the Relevance Heatmap (first row), Important Region (second row), Visual Attention Patterns (third row), and Final Pruning Mask (last row) for three VLA models (SpatialVLA (Qu et al., 2025), Nora (Hung et al., 2025), UniVLA (Wang et al., 2025)) on two representative tasks (‘Put The Spoon...’ and ‘Stack The Block...’). The comparison reveals how our method identifies and prunes distracting visual tokens across different model architectures. Please refer to Appendix A.4 for more visualization cases. 

## 3 METHOD 

Our method involves three stages to find and prune distracting tokens (see Figure 2). First, we analyze prompt-tovisual relevance to identify visual tokens that mostly related to the user’s intent task. Next, we conduct a weighted self-attention analysis from the generation perspective. Finally, we apply a dynamic intersection-based pruning strategy that reconciles both perspectives, selectively pruning image tokens. This multi-stage designs help the model to automatically correct its visual attention patterns at each generation step. 

### 3.1 PROBLEM FORMULATION 

Given a VLA model _F_ that processes visual tokens **V** _∈_ R<sup>_M×d_</sup> where _M_ represents number of image tokens, our objective is to identify a subset **V**<sup>_′_</sup> _⊂_ **V** with _|_ **V**<sup>_′_</sup> _|_ = _K_ (where _K < M_ ) that prune the distracting image tokens, yielding improved task success rate Succ� _F_ ( **V**<sup>_′_</sup> )� _≥_ Succ� _F_ ( **V** )�. 

### 3.1.1 IMPORTANT REGION CONSTRUCTION 

We compute the relevance score for visual tokens based on their interactions with prompt tokens. Let **P** denote the set of prompt tokens, **V** the set of visual tokens, and _C_ the set of selected layers. For each layer _c ∈C_ and each prompt token _pi ∈_ **P** , we calculate the relevance scores to all visual tokens as: 


where **A**<sup>_c_</sup> _h_<sup>_∈_R</sup><sup>_S×S_is the attention matrix of head</sup><sup>_h_at layer</sup><sup>_c_, and</sup><sup>_S_is the total number of tokens (text, visual, system,</sup> etc.). **A**<sup>_c_</sup> _h_<sup>[</sup><sup>_pi,_</sup><sup>**V**] selects the attention weights from prompt token</sup><sup>_pi_to all visual tokens</sup><sup>**V**in that head.Averaging over</sup> _H_ heads produces the relevance vector **r**<sup>_c_</sup> _pi_<sup>_∈_R</sup><sup>_M_, representing the overall importance of each visual token to prompt</sup> token _pi_ at layer _c_ . 

4 

Preprint 

For models (such as UniVLA (Wang et al., 2025)), where the input sequence places image tokens _after_ the prompt tokens, and prompt tokens don’t have attention to image tokens, we instead compute the relevance heatmap using embedding similarity. 


where **E** _pi ∈_ R<sup>_d_</sup> and **EV** _∈_ R<sup>_M×d_</sup> are the embeddings of the prompt token and visual tokens, respectively. Then we can aggregate across both prompt tokens and layers in a single step, and obtain the overall relevance heatmap _R_ for visual tokens: 


To reduce corner artifacts and focus on central regions, we apply spatial biasing with corner suppression and Gaussian smoothing. Finally, we identify the _k_ highest relevance visual tokens to form the important region _G_ . 

### 3.2 VISUAL ATTENTION PATTERN CONSTRUCTION 

To analyze which visual tokens the model attends to during action generation, we compute a visual attention pattern for each generated action token. For each action token _tj_ and each layer _l ∈{_ 1 _, . . . , N }_ , where _N_ is the total number of layers in the model. We first extract the attention weights from _tj_ to all visual tokens, producing a layer-specific heatmap **A**<sup>_l_</sup> _j_<sup>_∈_R</sup><sup>_M_.Wethenweighteachlayer’sheatmapbytheproportionoftotalvisualattentioninthatlayer,</sup> denoted as _w_<sup>_l_</sup> , and aggregate across layers to obtain the final visual attention pattern: 


where **A** _j ∈_ R<sup>_M_</sup> represents the overall attention the model assigns to each visual token while generating action token _tj_ . This final heatmap indicates which image tokens that model pay most of attentions during the action token generation. 

### 3.3 DISTRACTING TOKEN PRUNING 

Given the important region **G** obtained from the relevance heatmap and the visual attention pattern **A** , we identify distracting visual tokens by comparing attention values inside and outside of **G** . 

Let _am_ denote the maximum attention value among visual tokens located within the important attention region _Ag_ . For each visual token _v_ located in the unimportant attention region _Au_ , we denote it as a distracting token _d_ if its attention exceeds the thresholded maximum: 


Table 1: **Evaluation across different policies on WidowX Robot tasks** . Our DTP method demonstrates significant improvements across complex manipulation tasks. 

|Model|**Put Spoo**<br>Grasp|**n on Towel**<br>Success|**Put Carr**<br>Grasp|**ot on Plate**<br>Success|**Stack Green**<br>Grasp|**Block on Yellow Block**<br>Success|**Put Eggplan**<br>Grasp|**t in Yellow Basket**<br>Success|**SR**|**Rel.**|
|---|---|---|---|---|---|---|---|---|---|---|
|SpatialVLA (Qu et al., 2025)|12.5%|12.5%|37.5%|20.8%|70.8%|25.0%|75.0%|58.3%|29.2%|100%|
|SpatialVLA + DTP (Ours)|25.0%|25.0%|45.8%|33.3%|54.2%|29.2%|62.5%|62.5%|**37.5%**|**128.4%**|
|Nora (Hung et al., 2025)|37.5%|16.7%|41.7%|4.2%|50.0%|4.2%|0.0%|0.0%|6.2%|100%|
|Nora + DTP (Ours)|37.5%|20.8%|41.7%|4.2%|45.8%|12.5%|8.3%|8.3%|**11.5%**|**185.5%**|
|UniVLA (Wang et al., 2025)|83.3%|70.8%|75.0%|70.8%|79.2%|33.3%|100.0%|100.0%|68.7%|100%|
|UniVLA + DTP (Ours)|87.5%|75.0%|79.2%|75.0%|100.0%|45.8%|100.0%|100.0%|**74.0%**|**107.7%**|


Where _τ_ is a tolerance factor and _D_ is the set of all distracting tokens. Finally, all distracting tokens in _D_ will be pruned from the input to generate the refined action token. Please refer to Figure 3 for the visualization of the process for different models and tasks. 

## 4 EXPERIMENTS 

We evaluate DTP on the SIMPLER Benchmark (Li et al., 2024) using three state-of-the-art VLAs: SpatialVLA (Qu et al., 2025), a 3B model based on Paligemma 2 (Beyer et al., 2024) with integrated 3D position encoding; Nora (Hung 

5 

Preprint 

Table 2: **Evaluation across different policies on Google Robot tasks** . Our DTP method shows consistent improve- <u>ments across different VLA architectures.</u> 

|Model||**Visual Match**|**ing**||**V**|**ariant Aggreg**|**ation**||
|---|---|---|---|---|---|---|---|---|
||Pick Coke Can|Move Near|**SR**|**Rel.**|Pick Coke Can|Move Near|**SR**|**Rel.**|
|SpatialVLA (Qu et al., 2025)|83.3%|75.4%|79.4%|100%|90.2%|68.7%|79.5%|100%|
|SpatialVLA + DTP (Ours)|86.7%|77.1%|**81.9%**|**103.1%**|90.2%|70.7%|**80.5%**|**101.3%**|
|Nora (Hung et al., 2025)|53.7%|43.8%|48.7%|100%|56.0%|44.7%|50.4%|100%|
|Nora + DTP (Ours)|54.7%|45.0%|**49.9%**|**102.4%**|56.7%|47.0%|**51.9%**|**103.0%**|


Table 3: **Evaluation of Nora on the LIBERO Benchmark** . Our DTP method consistently improves performance across all LIBERO suites, including the challenging LIBERO-10. 

|Model|LIBERO-Spatial|**LIBERO Ben**<br>LIBERO-Object|**chmark**<br>LIBERO-Goal|LIBERO-10|
|---|---|---|---|---|
|Nora (Hung et al., 2025)|92.8%|76.0%|85.8%|69.6%|
|Nora + DTP (Ours)|**93.0%**|**77.4%**|**88.4%**|**76.2%**|


et al., 2025), built on Qwen2.5-VL-3B (Bai et al., 2025) with an additional FAST tokenizer (Pertsch et al., 2025) for action decoding; and UniVLA (Wang et al., 2025), a 9B world model for VLA tasks. This diverse set of models enables us to test DTP’s generalizability across different architectures and demonstrate its effectiveness in improving robotic manipulation performance. 

### 4.1 MAIN RESULTS 

Our experiments across both SIMPLER Benchmark and LIBERO Benchmark (Liu et al., 2023a) demonstrate that DTP consistently improves task success rates for transformer-based VLAs. We report results using **SR** (average task success rate) and **Rel.** (relative success rate), where the latter measures improvement over the baseline model. For each VLA checkpoint (SpatialVLA, Nora, UniVLA), we choose one global set of hyperparameters: tolerance _τ_ , selected layers _C_ for relevance heatmaps, number of top- _k_ relevant tokens and Gaussian smoothing parameters _σ_ . **This set of hyperparameters is kept fixed across all tasks, rollouts, and environments** for each model checkpoint. Which means we do not tune hyperparameters per task in this section. 

On **WidowX tasks** (Table 1), SpatialVLA improves from 29.2% to 37.5% average success (+28.4% relative), Nora rises from 6.2% to 11.5% (nearly 2 _×_ ), and UniVLA, already the strongest baseline (68.7%), further increases to 74.0% (+7.7% relative). These results indicate that DTP benefits both weak and strong policies by pruning distracting tokens. 

On **Google Robot tasks** (Table 2), improvements are smaller but consistent. SpatialVLA increases by +1–3% relatively, while Nora gains +2–3% relatively, confirming that DTP generalizes across robots and architectures, including already strong-performing setups. (Since UniVLA does not provide checkpoints for the Google Robot embodiment tasks, we exclude it from this test suite.) 

To further evaluate the generalization of DTP beyond SIMPLER Benchmark, we additionally test **Nora** on the **LIBERO Benchmark** (Liu et al., 2023a). We choose Nora because its official codebase and pretrained checkpoints for LIBERO are publicly available, enabling a reliable and reproducible evaluation. The results are shown in Table 3. 

Our DTP method consistently improves Nora across all LIBERO suites. Notably, it yields a +6 _._ 6% absolute gain on the more challenging LIBERO-10, and +1 _._ 4–2 _._ 6% improvements on the other benchmarks, despite the already high performance of the base model. This demonstrates that the effectiveness of DTP generalizes beyond SIMPLER and extends to more diverse and complex manipulation benchmarks. 

Overall, the results highlight two key findings: **Robustness across models** : DTP benefits both strong (UniVLA) and weak (Nora) VLAs, suggesting that pruning distracting visual tokens universally reduces noise in decision-making. **Generalizability across benchmarks, tasks and robots** : Improvements are observed across different environments and embodiments, indicating that DTP is not task-specific but broadly applicable. Detailed implementations are provided in Appendix A.2. 

6 

Preprint 

### 4.2 PERFORMANCE UPPER BOUND UNDER VISUAL ATTENTION PATTERNS 

To investigate the performance upper bound achievable by a VLA model under its _existing architecture_ , we analyze how different visual attention patterns influence the model’s uncertainty about the correct action token _A_<sup>_∗_</sup> (see Appendix A.1 for assumptions). 

Let _Z ∈_ R<sup>_M×d_</sup> denote the matrix of visual token value vectors, where _M_ is the number of visual tokens and _d_ is the feature dimension. Given a visual attention pattern _α_ , the model produces a modified set of value vectors _Zα_ , reflecting which regions of the image the model focuses on. Changing _α_ alters the visual representation and therefore the model’s uncertainty about the correct action. 

**Conditional uncertainty.** We define the uncertainty of the model under attention pattern _α_ as 


which measures how uncertain the model remains about the correct action token after observing the visual features selected by _α_ . A high value of _E_ ( _α_ ) indicates that the attention pattern includes distracting or irrelevant tokens, while a low value indicates that the attention emphasizes task-relevant regions. 


Figure 4: **Exploration of performance upper bounds under varying tolerance parameter** _τ_ **across different VLA models** . Dashed lines denote the baseline success rates without DTP, while solid lines illustrate performance under DTP with different _τ_ values. The success rate is annotated at peak to indicate _τ_ ˆ. The results confirm that tuning _τ_ enables the selection of optimal tolerance levels, thereby maximizing potential performance gains. 

**Normalized performance score.** To measure how much useful information the attention pattern provides relative to the inherent ambiguity in the task, we normalize by the entropy of the correct action distribution: 


where _H_ ( _A_<sup>_∗_</sup> ) captures the baseline uncertainty regarding the correct action before conditioning on visual input. Thus, _P_ ( _α_ ) _∈_ [0 _,_ 1] serves as a normalized performance measure: _P_ ( _α_ ) = 1 _denotes perfect certainty_ , while _P_ ( _α_ ) = 0 _indicates that the visual attention pattern provides no useful information_ . 

7 

Preprint 

**Optimal attention pattern.** The optimal attention configuration _α_<sup>_∗_</sup> is defined as the pattern that minimizes the conditional uncertainty: 


This represents the best achievable performance under the model’s architecture and visual encoder, without modifying weights, inputs, or structure. 

**Approximating the optimal pattern via DTP.** In practice, _α_<sup>_∗_</sup> is unknown. DTP provides an approximation by pruning distracting tokens based on a tolerance factor _τ_ , yielding an induced attention pattern _ατ_ . By sweeping over _τ_ , we identify _τ_ ˆ that maximizes _P_ ( _α_ ): 


where _α_ def is the model’s default (unmodified) attention pattern, and _α_ ˆ = _ατ_ ˆ is the best sub-optimal attention pattern found by DTP. 

**Interpretation.** This framework provides a principled way to: (i) quantify how different attention patterns influence action certainty, (ii) compare the model’s default attention to DTP-refined attention, and (iii) define a theoretical ceiling on performance achievable _without_ altering model architecture or retraining. 

Under this formulation, Section 4.2 analyzes how DTP moves the model toward this upper bound by reducing uncertainty through improved visual attention allocation. We evaluate the effect of pruning distracting tokens on SIMPLER WidowX Robot tasks across three VLA models. The results in Figure 4 illustrate how DTP alters the visual attention patterns and allows the models to approach their performance upper bounds. For **Nora** , pruning distracting tokens yields substantial improvements across all tasks, despite its relatively weak baseline. **SpatialVLA** exhibits moderate baseline performance and shows relatively consistent gains with pruning. **UniVLA** , while already achieving strong baselines, still benefits from pruning under certain _τ_ values, highlighting the robustness of our method. Overall, these results confirm that task-specific sub-optimal tolerance values ˆ _τ_ exist for each model, with some tasks achieving nearly 2 _×_ higher success rates, effectively pushing performance toward the theoretical upper bound under the current architecture. 

Table 4: **Ablation study on WidowX Robot tasks** . We compare different token selection strategies within our DTP framework including random pruning, random pruning only in unimportant region, and no Gaussian methods. Results demonstrate the superiority of our targeted distracting token identification approach. 

|Method|**Put Spoo**<br>Grasp|**n on Towel**<br>Success|**Put Carr**<br>Grasp|**ot on Plate**<br>Success|**Stack Green B**<br>Grasp|**lock on Yellow Block**<br>Success|**Put Eggplant**<br>Grasp|**in Yellow Basket**<br>Success|**SR**|**Rel.**|
|---|---|---|---|---|---|---|---|---|---|---|
|SpatialVLA + DTP (Random<br>~~a~~ll<br>~~r~~egion)|16.7%|12.5%|25.0%|20.8%|33.3%|8.3%|37.5%|20.8%|15.6%|53.4%|
|SpatialVLA + DTP (Random<br>~~u~~nimportant<br>~~r~~egion)|12.5%|8.3%|20.8%|4.2%|41.7%|25.0%|37.5%|33.3%|17.7%|60.6%|
|SpatialVLA + DTP (No<br>~~G~~aussian)|12.5%|12.5%|37.5%|20.8%|70.8%|25.0%|75.0%|58.3%|29.2%|100.0%|
|SpatialVLA + DTP (Ours)|25.0%|25.0%|45.8%|33.3%|54.2%|29.2%|62.5%|62.5%|**37.5%**|**128.4%**|
|Nora + DTP (Random<br>~~a~~ll<br>~~r~~egion)|37.5|8.3%|41.7%|0.0%|37.5%|4.2%|0.0%|0.0%|3.1%|50.0%|
|Nora + DTP (Random<br>~~u~~nimportant<br>~~r~~egion)|37.5%|12.5%|50.0%|4.2%|58.3%|4.2%|4.2%|0.0%|5.2%|83.9%|
|Nora + DTP (No<br>~~G~~aussian)|41.7%|8.3%|41.7%|4.2%|41.7%|4.2%|0.0%|0.0%|4.2%|67.7%|
|Nora + DTP (Ours)|37.5%|20.8%|41.7%|4.2%|45.8%|12.5%|8.3%|8.3%|**11.5%**|**181.7%**|
|UniVLA + DTP (Random<br>~~a~~ll<br>~~r~~egion)|50.0%|41.7%|58.3%|54.2%|91.7%|33.3%|95.8%|83.3%|53.1%|77.3%|
|UniVLA + DTP (Random<br>~~u~~nimportant<br>~~r~~egion)|83.3%|62.5%|70.1%|62.5%|83.3%|29.2%|95.8%|95.8%|62.5%|91.0%|
|UniVLA + DTP (No<br>~~G~~aussian)|83.3%|75.0%|75.0%|62.5%|95.8%|33.3%|100.0%|100.0%|67.7%|98.5%|
|UniVLA + DTP (Ours)|87.5%|75.0%|79.2%|75.0%|100.0%|45.8%|100.0%|100.0%|**74.0%**|**107.7%**|


Table 5: **Ablation study on Google Robot tasks** . Comparison of different token selection strategies within our DTP framework across different tasks and variations. Our targeted approach consistently outperforms alternative selection <u>methods across all model variants.</u> 

|Method||**Visual Match**|**ing**||**V**|**ariant Aggreg**|**ation**||
|---|---|---|---|---|---|---|---|---|
||Pick Coke Can|Move Near|SR|Rel.|Pick Coke Can|Move Near|SR|Rel.|
|SpatialVLA + DTP (Random<br>~~a~~ll<br>~~r~~egion)|62.5%|57.5%|60.0%|75.6%|66.5%|52.2%|59.4%|74.7%|
|SpatialVLA + DTP (Random<br>~~u~~nimportant<br>~~r~~egion)|86.0%|68.8%|77.4%|97.5%|54.2%|65.8%|60.0%|75.5%|
|SpatialVLA + DTP (No<br>~~G~~aussian)|83.6%|75.9%|79.8%|101.0%|89.9%|68.3%|79.1%|99.5%|
|SpatialVLA + DTP (Ours)|86.7%|77.1%|**81.9%**|**103.1%**|90.2%|70.7%|**80.5%**|**101.3%**|
|Nora + DTP (Random<br>~~a~~ll<br>~~r~~egion)|12.1%|8.9%|10.5%|21.6%|7.4%|11.2%|9.3%|18.5%|
|Nora + DTP (Random<br>~~u~~nimportant<br>~~r~~egion)|35.2%|28.7%|32.0%|65.6%|22.1%|31.4%|26.8%|53.1%|
|Nora + DTP (No<br>~~G~~aussian)|53.7%|43.8%|48.8%|100%|56.0%|44.7%|50.4%|100%|
|Nora + DTP (Ours)|54.7%|45.0%|**49.9%**|**102.4%**|56.7%|47.0%|**51.9%**|**103.0%**|


8 

Preprint 

### 4.3 ABLATION STUDIES 

To validate the effectiveness of our DTP framework, we conduct comprehensive ablation studies comparing different token selection strategies within the DTP framework to demonstrate the superiority of our targeted distracting token identification approach. **Random** **~~a~~ ll** **~~r~~ egion:** Randomly selects and prunes tokens from the entire region of the image. **Random** **~~u~~ nimportant** **~~r~~ egion:** Randomly selects and prunes tokens only within the unimportant region, while preserving tokens from the important region. **No** **~~G~~ aussian:** Constructs the important region without corner token suppression and Gaussian smoothing. **Ours:** The proposed DTP method with full implementation. 

As shown in Table 4 and 5. Across both WidowX and Google Robot tasks, random pruning strategies significantly underperform, often leading to degraded success rates. Restricting randomness to unimportant regions mitigates the drop but remains unstable. No ~~G~~ aussian variants achieve better results, yet still fall short of the original model and our full approach, underscoring the benefit of corner suppression and Gaussian smoothing in refining important regions. In contrast, our targeted DTP consistently achieves better outcomes across all models and platforms, validating the importance of precise distracting token identification for robust improvements. 


Figure 5: **Unimportant attention in VLA models.** (Top-left) Distribution of unimportant attention values between success and failure episodes across three models. (Top-right, Bottom-left, Bottom-right) Temporal evolution of unimportant attention for each model, with episode steps normalized to [0 _,_ 1] to provide a unified view of the dynamic changes. 

### 4.4 ANALYSIS OF ATTENTION IN UNIMPORTANT REGION AND TASK SUCCESS 

To better understand the role of unimportant region attentions in task performance. We define the _unimportant attention_ as the sum of attention for all visual tokens in _Au_ (see Figure 2). This value quantifies the degree to which the model allocates attention to visually irrelevant information during action generation. We conduct experiments on the SIMPLER Benchmark, evaluating both Google Robot and WidowX Robot tasks. For each step, we let the model to generate action tokens with its default visual attention patterns, then we observe and collect unimportant attention values. Finally we group the episodes into _success_ and _failure_ categories, and we use _Mann-Whitney U test_ to examine whether the unimportant attention values differ significantly between them. 

9 

Preprint 

As shown in Fig. 5 (top-left), failure episodes consistently exhibit higher unimportant attention than success episodes across all three models ( _p <_ 0 _._ 001). This indicates that attention leakage into irrelevant regions is strongly linked to task failure, and the effect generalizes across architectures. The temporal plots (Fig. 5, right and bottom) unpack the distributions of unimportant attention into a dynamic view across episode steps. While failure episodes generally assign more attention in unimportant region than success episode, the disparity most evident in the middle phase of the trajectory when the robot begins grasping and manipulating the target object. This may suggest a fundamental source of failure in certain robotic manipulation tasks. 

Overall, these results reveal that the suppression of unimportant attention emerges as a key factor for robust execution, whereas failures tend to persist with high unimportant attention from the middle stage of the trajectory. This finding highlights a systematic weakness of current VLA models: their tendency to misallocate attention to task-irrelevant regions, which not only reduces task success rate but also introduces instability during critical manipulation phases. Importantly, the consistency of this effect across different architectures and robot platforms suggests that it is not model-specific, but rather a general property of vision-language-action pipelines. By quantifying and analyzing unimportant attention, we provide empirical evidence that reducing attention leakage can serve as a practical pathway to improving both efficiency and reliability. These insights also motivate the design of targeted methods, such as our Distracting Token Pruning framework, which explicitly suppresses irrelevant attention and allows the model to focus on task-relevant regions. Ultimately, understanding and controlling unimportant attention offers a principled direction for creating more generalizable VLA models. 

## 5 CONCLUSION 

In this work, we introduced Distracting Token Pruning (DTP), a simple yet effective plug-and-play framework for evaluating Vision-Language-Action models. By dynamically detecting and pruning distracting tokens in task-irrelevant regions, DTP corrects the visual attention patterns for more accurate action token generation. Our method benefits both strong and weak policies, generalizes across robots. Experiments on the SIMPLER Benchmark and LIBERO Benchmark demonstrated consistent improvements in task success rates. Additionally, with appropriate tolerance _τ_ settings, we can explore the performance upper bounds of the model under its original architecture. Ablation studies further confirmed the necessity of our targeted pruning strategy over random or simplified baselines. Finally, our analysis revealed a negative correlation between unimportant attention and task success, highlighting attention leakage as a common cause of failure in robotic manipulation. These findings provide new insights into building more robust embodied AI systems. 

## REFERENCES 

- Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, Humen Zhong, Yuanzhi Zhu, Mingkun Yang, Zhaohai Li, Jianqiang Wan, Pengfei Wang, Wei Ding, Zheren Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen Cheng, Hang Zhang, Zhibo Yang, Haiyang Xu, and Junyang Lin. Qwen2.5-vl technical report, 2025. URL https://arxiv.org/abs/2502.13923. 

- Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, Thomas Unterthiner, Daniel Keysers, Skanda Koppula, Fangyu Liu, Adam Grycner, Alexey Gritsenko, Neil Houlsby, Manoj Kumar, Keran Rong, Julian Eisenschlos, Rishabh Kabra, Matthias Bauer, Matko Boˇsnjak, Xi Chen, Matthias Minderer, Paul Voigtlaender, Ioana Bica, Ivana Balazevic, Joan Puigcerver, Pinelopi Papalampidi, Olivier Henaff, Xi Xiong, Radu Soricut, Jeremiah Harmsen, and Xiaohua Zhai. Paligemma: A versatile 3b vlm for transfer, 2024. URL https://arxiv.org/abs/2407.07726. 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, Pete Florence, Chuyuan Fu, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Kehang Han, Karol Hausman, Alexander Herzog, Jasmine Hsu, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Lisa Lee, Tsang-Wei Edward Lee, Sergey Levine, Yao Lu, Henryk Michalewski, Igor Mordatch, Karl Pertsch, Kanishka Rao, Krista Reymann, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Pierre Sermanet, Jaspiar Singh, Anikait Singh, Radu Soricut, Huong Tran, Vincent Vanhoucke, Quan Vuong, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Jialin Wu, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. Rt-2: Vision-language-action models transfer web knowledge to robotic control, 2023a. URL https://arxiv.org/abs/2307.15818. 

10 

Preprint 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Tomas Jackson, Sally Jesmonth, Nikhil J Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Kuang-Huei Lee, Sergey Levine, Yao Lu, Utsav Malla, Deeksha Manjunath, Igor Mordatch, Ofir Nachum, Carolina Parada, Jodilyn Peralta, Emily Perez, Karl Pertsch, Jornell Quiambao, Kanishka Rao, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Kevin Sayed, Jaspiar Singh, Sumedh Sontakke, Austin Stone, Clayton Tan, Huong Tran, Vincent Vanhoucke, Steve Vega, Quan Vuong, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. Rt-1: Robotics transformer for real-world control at scale, 2023b. URL https://arxiv.org/abs/2212.06817. 

- Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, Deli Zhao, and Hao Chen. Worldvla: Towards autoregressive action world model, 2025. URL https: //arxiv.org/abs/2506.21539. 

- Zhe Chen, Weiyun Wang, Yue Cao, Yangzhou Liu, Zhangwei Gao, Erfei Cui, Jinguo Zhu, Shenglong Ye, Hao Tian, Zhaoyang Liu, Lixin Gu, Xuehui Wang, Qingyun Li, Yimin Ren, Zixuan Chen, Jiapeng Luo, Jiahao Wang, Tan Jiang, Bo Wang, Conghui He, Botian Shi, Xingcheng Zhang, Han Lv, Yi Wang, Wenqi Shao, Pei Chu, Zhongying Tu, Tong He, Zhiyong Wu, Huipeng Deng, Jiaye Ge, Kai Chen, Kaipeng Zhang, Limin Wang, Min Dou, Lewei Lu, Xizhou Zhu, Tong Lu, Dahua Lin, Yu Qiao, Jifeng Dai, and Wenhai Wang. Expanding performance boundaries of open-source multimodal models with model, data, and test-time scaling, 2025. URL https://arxiv.org/ abs/2412.05271. 

- Damai Dai, Chengqi Deng, Chenggang Zhao, R. X. Xu, Huazuo Gao, Deli Chen, Jiashi Li, Wangding Zeng, Xingkai Yu, Y. Wu, Zhenda Xie, Y. K. Li, Panpan Huang, Fuli Luo, Chong Ruan, Zhifang Sui, and Wenfeng Liang. Deepseekmoe: Towards ultimate expert specialization in mixture-of-experts language models, 2024. URL https://arxiv.org/abs/2401.06066. 

- Asher J. Hancock, Allen Z. Ren, and Anirudha Majumdar. Run-time observation interventions make vision-languageaction models more visually robust, 2024. URL https://arxiv.org/abs/2410.01971. 

- Huang Huang, Fangchen Liu, Letian Fu, Tingfan Wu, Mustafa Mukadam, Jitendra Malik, Ken Goldberg, and Pieter Abbeel. Otter: A vision-language-action model with text-aware visual feature extraction, 2025. URL https: //arxiv.org/abs/2503.03734. 

- Chia-Yu Hung, Qi Sun, Pengfei Hong, Amir Zadeh, Chuan Li, U-Xuan Tan, Navonil Majumder, and Soujanya Poria. Nora: A small open-sourced generalist vision language action model for embodied tasks, 2025. URL https: //arxiv.org/abs/2504.19854. 

- Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with open-world generalization, 2025. URL https://arxiv. org/abs/2504.16054. 

- Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa Sadigh. Prismatic vlms: Investigating the design space of visually-conditioned language models, 2024. URL https://arxiv. org/abs/2402.07865. 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model, 2024. URL https://arxiv.org/abs/2406.09246. 

- Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success, 2025. URL https://arxiv.org/abs/2502.19645. 

- Chengmeng Li, Junjie Wen, Yan Peng, Yaxin Peng, Feifei Feng, and Yichen Zhu. Pointvla: Injecting the 3d world into vision-language-action models, 2025. URL https://arxiv.org/abs/2503.07511. 

- Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, Sergey Levine, Jiajun Wu, Chelsea Finn, Hao Su, Quan Vuong, and Ted Xiao. Evaluating real-world robot manipulation policies in simulation, 2024. URL https://arxiv.org/abs/2405.05941. 

11 

Preprint 

- Tao Lin, Gen Li, Yilei Zhong, Yanwen Zou, Yuxin Du, Jiting Liu, Encheng Gu, and Bo Zhao. Evo-0: Vision-languageaction model with implicit spatial understanding, 2025. URL https://arxiv.org/abs/2507.00416. 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning, 2023a. URL https://arxiv.org/abs/2306.03310. 

- Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning, 2023b. URL https: //arxiv.org/abs/2304.08485. 

- Haoyu Lu, Wen Liu, Bo Zhang, Bingxuan Wang, Kai Dong, Bo Liu, Jingxiang Sun, Tongzheng Ren, Zhuoshu Li, Hao Yang, Yaofeng Sun, Chengqi Deng, Hanwei Xu, Zhenda Xie, and Chong Ruan. Deepseek-vl: Towards real-world vision-language understanding, 2024. URL https://arxiv.org/abs/2403.05525. 

- Quentin Malartic, Nilabhra Roy Chowdhury, Ruxandra Cojocaru, Mugariya Farooq, Giulia Campesan, Yasser Abdelaziz Dahou Djilali, Sanath Narayan, Ankit Singh, Maksim Velikanov, Basma El Amel Boussaha, Mohammed Al-Yafeai, Hamza Alobeidli, Leen Al Qadi, Mohamed El Amine Seddik, Kirill Fedyanin, Reda Alami, and Hakim Hacid. Falcon2-11b technical report, 2024. URL https://arxiv.org/abs/2407.14885. 

- Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, Mahmoud Assran, Nicolas Ballas, Wojciech Galuba, Russell Howes, Po-Yao Huang, Shang-Wen Li, Ishan Misra, Michael Rabbat, Vasu Sharma, Gabriel Synnaeve, Hu Xu, Herv´e Jegou, Julien Mairal, Patrick Labatut, Armand Joulin, and Piotr Bojanowski. Dinov2: Learning robust visual features without supervision, 2024. URL https://arxiv.org/abs/2304.07193. 

- Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models, 2025. URL https:// arxiv.org/abs/2501.09747. 

- Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, and Xuelong Li. Spatialvla: Exploring spatial representations for visual-language-action model, 2025. URL https://arxiv.org/abs/2501.15830. 

- Qwen, :, An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, Huan Lin, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jingren Zhou, Junyang Lin, Kai Dang, Keming Lu, Keqin Bao, Kexin Yang, Le Yu, Mei Li, Mingfeng Xue, Pei Zhang, Qin Zhu, Rui Men, Runji Lin, Tianhao Li, Tianyi Tang, Tingyu Xia, Xingzhang Ren, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yu Wan, Yuqiong Liu, Zeyu Cui, Zhenru Zhang, and Zihan Qiu. Qwen2.5 technical report, 2025. URL https://arxiv.org/abs/2412.15115. 

- Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, and Ilya Sutskever. Learning transferable visual models from natural language supervision, 2021. URL https://arxiv.org/abs/2103.00020. 

- Lin Sun, Bin Xie, Yingfei Liu, Hao Shi, Tiancai Wang, and Jiale Cao. Geovla: Empowering 3d representations in vision-language-action models, 2025. URL https://arxiv.org/abs/2508.09071. 

- Quan Sun, Yuxin Fang, Ledell Wu, Xinlong Wang, and Yue Cao. Eva-clip: Improved training techniques for clip at scale, 2023. URL https://arxiv.org/abs/2303.15389. 

- Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, Dan Bikel, Lukas Blecher, Cristian Canton Ferrer, Moya Chen, Guillem Cucurull, David Esiobu, Jude Fernandes, Jeremy Fu, Wenyin Fu, Brian Fuller, Cynthia Gao, Vedanuj Goswami, Naman Goyal, Anthony Hartshorn, Saghar Hosseini, Rui Hou, Hakan Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa, Isabel Kloumann, Artem Korenev, Punit Singh Koura, Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee, Diana Liskovich, Yinghai Lu, Yuning Mao, Xavier Martinet, Todor Mihaylov, Pushkar Mishra, Igor Molybog, Yixin Nie, Andrew Poulton, Jeremy Reizenstein, Rashi Rungta, Kalyan Saladi, Alan Schelten, Ruan Silva, Eric Michael Smith, Ranjan Subramanian, Xiaoqing Ellen Tan, Binh Tang, Ross Taylor, Adina Williams, Jian Xiang Kuan, Puxin Xu, Zheng Yan, Iliyan Zarov, Yuchen Zhang, Angela Fan, Melanie Kambadur, Sharan Narang, Aurelien Rodriguez, Robert Stojnic, Sergey Edunov, and Thomas Scialom. Llama 2: Open foundation and fine-tuned chat models, 2023. URL https://arxiv.org/abs/2307.09288. 

- Yuqi Wang, Xinghang Li, Wenxuan Wang, Junbo Zhang, Yingyan Li, Yuntao Chen, Xinlong Wang, and Zhaoxiang Zhang. Unified vision-language-action model, 2025. URL https://arxiv.org/abs/2506.19850. 

12 

Preprint 

Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training, 2023. URL https://arxiv.org/abs/2303.15343. 

## A APPENDIX 

### A.1 REMARKS FOR SECTION 4.2 

In practice, we assume that multiple ground-truth actions _A_<sup>_∗_</sup> may lead to task success, which ensures _H_ ( _A_<sup>_∗_</sup> ) _>_ 0 and makes our normalized formulation well defined. The domain of _α_ corresponds to the cross-attention weights from the output (action) token query to the visual token keys, i.e., the distribution of attention over visual tokens. Here _Z_ denotes the value vectors of visual tokens, and _Zα_ represents the attention-weighted aggregation used in generating the output token. Different tolerance values _τ_ prune varying numbers of tokens in the unimportant region (smaller _τ_ prunes more aggressively), thereby modifying the attention weights _α_ and inducing new attended representations _Zατ_ . We seek the tolerance setting that minimizes the conditional uncertainty _H_ ( _A_<sup>_∗_</sup> _| Zατ_ ), which corresponds to the model’s most effective (sub-optimal) attention pattern under pruning. Since VLA models generate discrete action tokens autoregressively, the conditional entropy _H_ ( _A_<sup>_∗_</sup> _| Zα_ ) is naturally computed from the predictive distribution over actions. Finally, while the theoretical optimum _α_<sup>_∗_</sup> may be unattainable in practice, our method ensures that the selected _α_ ˆ = _ατ_ ˆ approximates the best possible sub-optimal attention pattern, aligning closely with the model’s own preferences and yielding the maximum possible improvements in task success rate. 

### A.2 IMPLEMENTATION DETAILS 

Our method is implemented as a plug-and-play module that integrates seamlessly with existing VLA architectures. We register forward hooks on attention layers to extract attention scores without modifying the model architecture. The method operates during inference with negligible overhead, requiring only one additional forward pass for generating a single token to compute visual proportion weights. 

For experiments in Section 4.1, we used a fixed tolerance score of _τ_ = 0 _._ 5 (for SpatialVLA (Qu et al., 2025)), _τ_ = 1 _._ 22 (for Nora (Hung et al., 2025)), and _τ_ = 0 _._ 7 (for UniVLA (Wang et al., 2025)) for all tasks. 

For SpatialVLA with 256 visual tokens, the selected layers for constructing the relevance heatmap are empirically chosen as _C_ = 4 _,_ 6 (indexed from layer 0) based on their strong visual-linguistic alignment properties. We set _k_ = 109 for selecting the top-relevant image tokens from relevance heatmap, and we set _σ_ = 0 _._ 65 for Gaussian smoothing when constructing the final important region. 

For Nora with 64 visual tokens, the selected layers for constructing the relevance heatmap are empirically chosen as _C_ = 12 _,_ 13 _,_ 21 (indexed from layer 0) based on their strong visual-linguistic alignment properties. We set _k_ = 40 for selecting the top-relevant image tokens from relevance heatmap, and we set _σ_ = 0 _._ 65 for Gaussian smoothing when constructing the final important region. 

For UniVLA with 1024 visual tokens, the selected layers for constructing the relevance heatmap are empirically chosen as _C_ = 11 _,_ 12 (indexed from layer 0) based on their strong visual-linguistic alignment properties. We set _k_ = 512 for selecting the top-relevant image tokens from relevance heatmap, and we set _σ_ = 0 _._ 9 for Gaussian smoothing when constructing the final important region. 

In our experiments, we use DPT to detect distracting tokens during the model’s original action generation, then construct a pruning mask over the visual input, and finally let the model re-generate a refined action token under the masked attention. For SpatialVLA, however, we simplify this process by analyzing only the _first_ action token to construct a single pruning mask, which is then applied across all subsequent tokens at the step. This strategy significantly mitigate the inference speed issue, with only a minor trade-off in the precision of distracting token pruning. For Nora, we limit pruning to at most _two_ visual tokens, since it operates with relatively fewer visual tokens, and excessive pruning may introduce errors in the generation process. For SIMPLER Benchmark, we sample test cases for Pick Coke Can Variant Aggregation test suite, as it is designed to evaluate efficiency while maintaining overall testing quality and validity of results. 

In the experiments of Section 4.2, we use an interval of _τ_ = 0 _._ 1 for empirical evaluation on the SIMPLER WidowX Robot tasks to identify the optimal _τ_ ˆ. For UniVLA, however, we adopt a coarser interval of _τ_ = 1 _._ 0 once _τ >_ 3 _._ 0, since smaller increments beyond this point yield negligible differences in task success rate, and the larger step size improves experimental efficiency. 

13 

Preprint 

All experiments for SpatialVLA and Nora were conducted on a single NVIDIA RTX 3090 GPU, while UniVLA was run on an NVIDIA A100 GPU. (For reproducibility, we recommend using the same GPU setup, as different GPU may lead to slight variations in the results.) 

### A.3 LIMITATION 

While DTP demonstrates strong generalizability to transformer-based VLA models and serves as an effective approach to explore performance upper bounds without altering model architectures, our implementation has some limitations. First, the current system could potentially be optimized to achieve faster inference speed, which would improve its efficiency. Second, the construction of important areas relies solely on the model’s own ability, with few rule-based refinements. This dependence may limit precision, and future work could incorporate alternative methods for generating more accurate important regions, thereby further enhancing the overall performance of the framework. 

14 

Preprint 

A.4 ADDITIONAL VISUALIZATION CASES OF OUR METHOD 


Figure 6: **Visualization of the distracting token pruning process across different VLA models for the stacking task.** The figure shows the Relevance Heatmap (first row), Important Region (second row), Visual Attention Patterns (third row), and Final Pruning Mask (last row) for three VLA models (SpatialVLA (Qu et al., 2025), Nora (Hung et al., 2025), UniVLA (Wang et al., 2025)). The comparison reveals how our method identifies and prunes distracting visual tokens across different model architectures. 

15 

Preprint 


Figure 7: **Layer-wise visual attention patterns of SpatialVLA for the task ‘Stack the Block...’** Each image shows the attention distribution at a different transformer layer when the model generates the action token.16 

Preprint 


Figure 8: **Layer-wise relevance heatmap of SpatialVLA for the task ‘Stack the Block...’, with selected layer 4, 6** 17 **used for constructing important region.** 

Preprint 


Figure 9: **Layer-wise visual attention patterns of Nora** 18 **for the task ‘Stack the Block...’** Each image shows the attention distribution at a different transformer layer when the model generates the action token. 

