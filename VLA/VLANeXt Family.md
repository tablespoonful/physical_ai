---
title: "VLANeXt Family: A Systematic Study of VLA Models from Core Recipes to Emerging Paradigms"
date: "2026-02-20"
authors: "Xiao-Ming Wu; Kang Liao; Yihang Luo; Bin Fan; Jian-Jian Jiang; Runze Yang"
url: https://arxiv.org/abs/2602.18532
pdf: https://arxiv.org/pdf/2602.18532
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.18532)** / [論文ページ](https://arxiv.org/abs/2602.18532)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

VLANeXt Family: A Systematic Study of VLA Models from Core Recipes to Emerging Paradigms Xiao-Ming Wu, Kang Liao, Yihang Luo, Bin Fan, Jian-Jian Jiang, Runze Yang, Zhonghua Wu, Wei-Shi Zheng, and Chen Change Loy 

**_Abstract_ —Following the rise of large foundation models, Vision–Language–Action models (VLAs) emerged, leveraging strong visual and language understanding from Vision-Language Models for general-purpose policy learning. Yet, the current VLA landscape remains fragmented and exploratory. Although many groups have proposed their own VLA models, inconsistencies in training protocols and evaluation settings make it difficult to identify which design choices truly matter. To bring structure to this evolving space, we reexamine the VLA design space under a unified framework and evaluation setup. Starting from a simple VLA baseline similar to RT-2, which is the origin of VLA, we systematically dissect design choices along three dimensions: foundational components, perception essentials, and action modeling perspectives. From this study, we distill 12 key findings that together form a** **_practical recipe_ for building strong VLA models. The outcome of this exploration is a simple yet effective model, VLANeXt. It outperforms the state-of-theart methods on the LIBERO and LIBERO-plus benchmarks and demonstrates strong performance in real-world experiments. Beyond identifying the core recipe, we further ask how far these design principles extend to the** **_emerging paradigms_ in VLAs. We thus expand VLANeXt along several emerging directions, including model scaling, latent-action pretraining, latent predictive representation learning, and world action modeling. These studies give rise to the VLANeXt family, spanning compact and scaled VLA variants, latent-action models, JEPA-style predictive models, and World Action Models. Our results show that the core recipe provides a strong foundation across different model scales and emerging paradigms. We release a unified and easy-to-use codebase to reproduce our findings, explore the design space, and develop new VLA variants on top of a shared foundation. The codebase is available at https://github.com/DravenALG/VLANeXt.** 

**_Index Terms_ —Robot Learning, Vision-Language-Action Models, Systematic Study.** 

# I. INTRODUCTION 

**B** OTHof vision-language-actionacademia and industry(VLA)havemodelsproposedthatademonstratewide range 

of vision-language-actionacademia (VLA)havemodelsproposedthatademonstratewidemodelsproposedthatademonstratewidethatademonstratewidedemonstratewide strong performance and encouraging generalization across diverse tasks [1]–[13]. Most VLA approaches follow a similar paradigm: they build on pre-trained LLMs or VLMs, processing visual observations together with language instructions to derive action-relevant representations for policy learning. This pipeline introduces numerous design choices, including how to interface 

Xiao-Ming Wu, Kang Liao, Yihang Luo, and Chen Change Loy are with S-Lab, Nanyang Technological University, Singapore. Chen Change Loy is also with ACE Robotics. 

Bin Fan, Jian-Jian Jiang, and Wei-Shi Zheng are with Sun Yat-sen University, China. 

Runze Yang is with Shanghai Jiao Tong University, China. Zhonghua Wu is with SenseTime Research, Singapore. 

Corresponding author: Chen Change Loy (e-mail: ccloy@ntu.edu.sg). 


Fig. 1. **Performance comparison on the LIBERO benchmark** . We compare VLANeXt with representative VLA baselines across model scales. Despite its smaller model size, VLANeXt achieves higher success rates than prior methods on the LIBERO benchmark, demonstrating the effectiveness of the design recipe distilled in this work. We further extend VLANeXt to emerging paradigms through model scaling and world action modeling. Both VLANeXtL and VLANeXt-WAM further improve upon the base model, showing that the core recipe remains effective as VLAs scale and evolve toward emerging paradigms. 

the VLM with the policy module, how to train the policy, how to select essential perceptual inputs, and how actions should be represented and modeled. Despite rapid progress, early exploration of VLAs remains something of a “primordial soup”, rich in ideas but lacking clear structure. While prior work has explored VLA design from certain perspectives [14]– [20], differences in training protocols and evaluation setups make it difficult to identify which design choices in the shared VLA design space truly matter. 

This work aims to provide a more systematic understanding of this fragmented design space by comprehensively reexamining VLA designs under a unified framework and evaluation protocol. While several prior works [9], [13] have made preliminary attempts to explore VLA designs, their investigations remain limited in scope. In detail, we begin with a simple baseline VLA, similar to RT-2 [1], which is the origin of VLA and serves as a strong reference point for analyzing the effectiveness of different design choices. We evaluate the core-recipe variants on two commonly used VLA benchmarks, including LIBERO [21] and LIBERO-plus [22], where LIBERO-plus extends the original benchmark with controlled and unseen perturbations to better assess robustness and generalization. After distilling the core design principles under this unified setup, we further examine how far these principles extend to emerging VLA paradigms beyond the standard formulation. 

Within this setup, we first systematically explore the design space along three dimensions: 1) foundational components, 

2 


Fig. 2. **Ablation trajectory across the VLA design space** . We progressively evolve a baseline VLA across foundational components, perception essentials, and action modeling perspectives, evaluating on LIBERO (Spatial) and switching to LIBERO-plus (Spatial) once performance saturates. This trajectory yields the base VLANeXt (2.5B), outperforming OpenVLA-OFT (7B). We further extend VLANeXt to emerging paradigms, including model scaling (S/Base/L), latent-action pretraining (LAM), latent predictive representation learning (JEPA), and world action modeling (WAM). The resulting VLANeXt family consistently achieves strong average performance across the four LIBERO suites. 

covering core VLM-policy architectures and action learning objectives; 2) perception essentials, examining the role of visual, language, and proprioceptive inputs; and 3) action modeling perspectives, investigating designs and auxiliary objectives that facilitate action generation. We conduct more than 500 distinct experiments over the above three dimensions and distill 12 key findings that together form a practical recipe for building strong VLA models, summarized in Fig. 2. 

We highlight several findings that we believe are novel and noteworthy for the field: 1) a soft connection between the VLM and the policy module performs slightly better than both loose and tight coupling strategies; 2) simply providing temporal observations as additional VLM inputs does not improve action learning, despite the backbone being pretrained for video 

understanding; 3) conditioning proprioceptive input in the VLM yields better performance than either omitting proprioception or injecting it directly into the policy module; and 4) framing action generation as a time-series forecasting problem and incorporating frequency-domain modeling provides an effective and efficient way to improve action prediction. 

The outcome of this study is a simple yet effective VLA model, **VLANeXt** , derived directly from the design principles uncovered in our systematic exploration. Rather than relying on aggressive model scaling or task-specific engineering, VLANeXt achieves state-of-the-art performance on both LIBERO [21] and LIBERO-plus [22], and adapts effectively to real-world manipulation tasks. These results show that strong VLA performance can emerge from principled design choices within a unified framework. 

The above findings are reported in our earlier conference version [23]. In this extended work, we further explore how far these design principles extend to the _emerging paradigms_ in VLAs. We expand VLANeXt along four directions. First, we study _model scaling_ across different backbone sizes, examining whether the recipe remains effective as model capacity changes. Second, we investigate _latent-action pretraining_ , where the model first learns from latent action representations before adapting to labeled robot actions. Third, we explore _latent predictive representation learning_ through JEPA-style objectives, encouraging the model to predict future latent representations rather than directly reconstructing future observations. Fourth, we extend VLANeXt toward _world action modeling_ , jointly learning future visual dynamics and robot actions with videogeneration backbones. Together, these extensions form the **VLANeXt family** , spanning compact and scaled VLA variants, latent-action models, JEPA-style predictive models, and World Action Models. Our results show that the core recipe provides a strong foundation across different model scales and emerging paradigms. 

To support further progress in this direction, we release a **research-oriented codebase** that standardizes training and evaluation while exposing the key components of the VLA design space. The framework is intentionally lightweight and minimally encapsulated, enabling researchers to reproduce our findings, compare new designs under a shared protocol, and develop new variants across the broader VLANeXt family and emerging VLA paradigms. The codebase is available at https://github.com/DravenALG/VLANeXt. 

# II. REVISITING ROBOT LEARNING AND VLA MODELS 

Robot learning aims to apply machine learning techniques to robotic control, empowering robots to interact with the physical world and acquire diverse skills [24]. In the context of robot learning, tasks are generally categorized into locomotion and manipulation based on the active components being controlled. Locomotion is designed to maintain the stability and balance of the robot base, enabling mobility for legged systems such as quadrupeds or humanoids [25]– [30]. Since these tasks typically possess explicit objectives, they frequently use Reinforcement Learning (RL). In contrast, robotic manipulation focuses on controlling the robotic arm 

3 

or whole body to execute a diverse array of interactive tasks. Previously, manipulation was usually focused on specific tasks, such as gripper grasping [31]–[35], dexterous hand grasping [36]–[41], non-prehensile manipulation [42]–[44], pickand-place/rearrangement [45], [46], contact-rich insertion [47], dexterous manipulation [48], [49], deformable-object manipulation [50], articulated-object manipulation [51], dynamic manipulation [52]–[54], and tool use [48], [55]. These tasks can typically be formulated with well-defined task priors, making them relatively easier to learn and generalize. More recently, general-purpose manipulation has gradually become a central research direction [56]–[61]. However, due to the diversity of task goals and manipulated objects, it is often difficult to design explicit reward functions or leverage well-defined task priors for such settings. As a result, imitation learning (IL) has been widely adopted, enabling robots to acquire complex manipulation skills directly from expert demonstrations. In this paper, we primarily focus on general-purpose robotic manipulation through imitation learning. Robotic manipulation methods can be divided into standard action policies [62]–[75] and video action policies [76]–[82]. The former framework naively inputs instructions and visuals, outputting the actions to complete the tasks, while the latter pipeline predicts future videos together with action generation, with the claim that these world modeling abilities can help understand the task better and generate the actions more accurately. 

In recent years, with the triumph of large foundation models, integrating these tremendous models into robot learning to build Vision-Language-Action (VLA) Models has become a prominent trend [83]. This paradigm was pioneered by the groundbreaking RT-2 [1], which formally introduced the concept of VLA. Subsequently, researchers across academia and industry have developed a diverse array of VLA models [2]–[13], [84]–[88]. These newer iterations address specific challenges, such as leveraging 3D spatial information [14], [15], [89]–[91], exploiting intermediate data (like subtask decomposition, future frame/video prediction or robot trajectory prediction) [16]–[18], [92]–[110] to enhance action generation, and designing post-training optimization methods, such as planning or reinforcement learning, to adapt to specific environments [19], [20], [111]–[119]. Additionally, a subset of VLAs explores some niche but important aspects [120]–[130], such as latent actions [131]–[135], lightweight VLAs [136]– [139] and VLAs in specific domains [140]–[143]. 

Despite their different emphases, most VLA models follow a similar pipeline that builds on pretrained LLMs or VLMs to process visual observations and language instructions and derive action-relevant representations for policy learning. However, this shared pipeline admits numerous design choices spanning foundational components, perception, and action modeling. As a result, the rapidly evolving VLA landscape remains something of a “primordial soup”: rich in ideas but lacking clear structure. Differences in model architectures, training protocols, and evaluation settings further make it difficult to determine which design choices truly matter. To bring structure to this fragmented design space, we systematically reexamine VLA models under a unified framework and evaluation protocol. Through more than 500 controlled experiments, we study design choices 


Fig. 3. Design choices for the policy module. 

across foundational components, perception essentials, and action modeling perspectives, and distill 12 key findings into a practical core recipe for building strong VLA models. These principles instantiate **VLANeXt** , a simple yet effective VLA that achieves state-of-the-art performance on LIBERO [21] and LIBERO-plus [22], while transferring effectively to real-world manipulation tasks. Beyond the standard VLA formulation, we further examine whether the distilled recipe remains effective as the VLA paradigm evolves. We extend VLANeXt along four emerging directions: model scaling, latent-action pretraining, latent predictive representation learning, and world action modeling. These extensions form the **VLANeXt family** , allowing us to study whether the identified design principles generalize across different model scales and sources of prior. Our results show that the core recipe remains effective across these emerging paradigms, providing a common foundation for studying and developing evolving VLA models. 

III. CORE RECIPES FOR BUILDING STRONG VLA MODELS 

In this section, we detail the step-by-step evolution from a simple baseline to the base VLANeXt model, distilling the core recipe that later serves as a common foundation for the emerging-paradigm extensions. We organize our exploration along three aspects: foundational components (Sec. III-A), perception essentials (Sec. III-B), and action modeling perspectives (Sec. III-C). An overview is shown in Fig. 2, with full results in Table I. 

**Evaluation Setup.** We perform the roadmap exploration on LIBERO and LIBERO-plus [21], [22]. Main experiments are conducted on the spatial suite as our primary testbed, while the resulting insights generalize across the other suites (Object, Goal, and Long). 

**Baseline.** Our baseline follows the VLA pipeline introduced in RT-2 [1], the origin of VLAs, and later adopted by OpenVLA [5]. We use LLaMA as the language backbone [144]. Since LLaMA does not natively support visual inputs, we also pair our backbone with SigLIP2 [145] as the vision encoder. A subset of rarely used text tokens is repurposed as action tokens, enabling action prediction in the same autoregressive framework. Continuous actions are discretized using a simple binning strategy and modeled as classification over bin indices. We intentionally start from this minimal, classical RT-2-style [1] setup to provide a clean reference point for analyzing the effects of different design choices. Our implementation adopts a more recent LLaMA version (LLaMA 3.2) but at a smaller scale (3B parameters), compared to OpenVLA [5]. 

4 

# _A. The Foundational Components_ 

In this section, we investigate some core design choices of VLAs, including architectures and training losses. 

**Policy Module Design.** Our baseline follows RT-2 [1] and OpenVLA [5], reusing text tokens for action classification. We first examine whether an explicit policy head is necessary. To this end, we append a class token to the text and visual embeddings and feed its LLM output into a two-layer policy head (transformer architecture) for action classification (Fig. 3(a)(b)). Results show that introducing a separate policy head performs slightly better than directly reusing text tokens (Table I), suggesting that _decoupling action prediction from the linguistic token space is beneficial_ . 

We further investigate whether a more expressive policy module brings additional gains. Specifically, we replace the single class token with multiple tokens (16) and expand the policy network from 2 to 12 layers, making the design conceptually similar to MetaQuery [146] (Fig. 3(c)). This _enlarged policy module yields a significant performance improvement_ (Table I). The base VLANeXt adopts this design. 

**Action Chunking.** Our baseline predicts actions one step at a time. Here, we evaluate action chunking, which predicts multiple future actions jointly and is known to improve inference efficiency [9]. _Results show that action chunking substantially improves over single-step prediction, while a horizon of 8 achieves the strongest robustness on LIBERO-plus_ (Table I), suggesting that _modeling a longer temporal window of action provides a more coherent view of the action sequence_ . We therefore adopt action chunking with a chunk size of 8. 

**Action Learning Objective.** An action chunk is a continuous vector of shape ( _t, dim_ ). Our baseline discretizes this vector using binning (first normalizing to the range [ _−_ 1 _,_ 1], then dividing into 256 bins) and treats action prediction as classification, following OpenVLA [5]. We compare this with alternative objectives, including direct regression [9], diffusion-based losses such as DDIM [16], [147], flow matching [94], [148], and VQ-VAE–based codebook (using a codebook of size 1,024, with three codes assigned to each action) classification [149], [150]. 

Results show that _regression achieves the strongest performance_ , _with diffusion-based objectives close behind_ , while classification-based approaches perform worst (Table I). In addition, as performance improves, the flow-matching objective eventually outperforms the regression loss, since the former can represent precise control signals. We therefore adopt the flow-matching objective. We also observe that classification using the VQ–VAE–based codebook underperforms relative to the binning strategy. We attribute this to the fact that the action spaces are low-dimensional, meaning a simple binning approach provides sufficient resolution. 

**VLM Backbone Capacity.** Our baseline uses LLaMA as the backbone [144]. We evaluate alternative VLM backbones to study how backbone strength affects VLA performance, including PaliGemma-3B [151] (used in the _π_ series [6], [11]) and the Qwen-VL family [152], which represent some of the most capable open-source VLMs currently available. 

Results show a consistent trend: _more capable VLM backbones generally lead to stronger VLA performance in this_ 


Fig. 4. Design choices for the VLM-Policy connection. 

_controlled comparison_ (Table I), with Qwen3-VL-4B outperforming Qwen3-VL-2B, which in turn outperforms LLaMA-3.23B and PaliGemma-3B. For the remainder of the core-recipe study, we use Qwen3-VL-2B as an effective and efficient choice, keeping backbone scale fixed while ablating other design components. We revisit model scaling after the full recipe is established in Sec. V to examine whether the recipe remains effective across model scales. This finding differs from that reported by Zhang et al. [127]. A possible reason is that our larger policy module can better exploit the representational capacity of stronger VLMs, whereas the lightweight policy head in Zhang et al. [127] may limit such gains. We leave a deeper investigation to future work. 

**VLM-Policy Connection.** We next study how different connection strategies between the VLM and the policy module affect performance. Our baseline adopts a MetaQuery-style design [146], as discussed in “Policy Module Design”. We refer to this design as the loose strategy, where the VLM and policy module are fully decoupled. We compare this with a tight strategy that connects the two modules layer by layer, as in the _π_ series [6], [11]. Inspired by these two designs, we further introduce a soft strategy that also connects them layer by layer but inserts learnable queries as a latent buffer between the modules (Fig. 4). For all three connection strategies, we use cross attention for conditioning, and the timestep is conditioned using adaLN, following Peebles and Xie [153]. 

Results show that the _soft strategy slightly outperforms both loose and tight connections_ (Table I), suggesting that the learnable query buffer helps better transfer useful representations from the VLM’s textual space to the policy module’s action space. This may be viewed as introducing a latent buffer between the two components, analogous to reasoning in a latent space [154]. We adopt the soft connection in subsequent models. 

# _B. The Perception Essentials_ 

In this section, we shift our focus from foundational components to perception, investigating whether and how different modalities ( _e.g._ , visual observations and proprioceptive states) should be provided as inputs to VLAs. 

**Temporal Observation History.** We examine whether incorporating temporal observation history improves performance. Our baseline follows OpenVLA [5] and uses only the current frame as input. We extend this to include multiple past frames, leveraging the video capability of the Qwen3-VL2B backbone [152] for a controlled comparison. Results show that _simply providing additional past observations as VLM_ 

5 

TABLE I 

ABLATION ACROSS THE VLA DESIGN SPACE ON LIBERO, LIBERO-PLUS (SPATIAL SUITE). EACH BLOCK VARIES IN ONE DESIGN ASPECT. LIBERO-PLUS EVALUATES ROBUSTNESS UNDER DIVERSE PERTURBATIONS. PERFORMANCE IMPROVES STEADILY AS EFFECTIVE DESIGN CHOICES ARE INCORPORATED. 

||**LIBERO**||||**LIBER**|**O-plus**||||
|---|---|---|---|---|---|---|---|---|---|
|**Model**|**Original**|**Camera**|**Robot**|**Language**|**Light**|**Background**|**Noise**|**Layout**|**Total**|
|**_Foundational Components_**||||||||||
|_RT-2 like Baseline_||||||||||
|Baseline|19.8|-|-|-|-|-|-|-|_<_ 5.0|
|_Policy Module Design_||||||||||
|Baseline|19.8|-|-|-|-|-|-|-|_<_ 5.0|
|Separate Head<br>|30.2<br>|0.8<br>|10.0<br>|31.0<br>|15.4<br>|24.8<br>|4.0<br>|30.1<br>|16.6<br>|
|Large Policy Module|64.4|0.5|12.6|79.7|34.6|32.9|8.5|63.1|34.0|
|_Action Chunking Horizon_||||||||||
|Action Chunk 1|64.4|0.5|12.6|79.7|34.6|32.9|8.5|63.1|34.0|
|Action Chunk 4|75.4|5.3|28.0|67.9|42.5|50.4|14.8|70.4|40.0|
|Action Chunk 8|74.6|5.6|26.0|85.6|56.8|55.8|11.7|63.9|43.4|
|_Action Learning Objective_||||||||||
|bin Classification|74.6|5.6|26.0|85.6|56.8|55.8|11.7|63.9|43.4|
|i<br>VQ-VAE Classification|58.8|3.2|44.3|67.2|42.5|43.8|7.1|48.3|36.5|
|Regression|85.4|5.1|32.3|90.5|62.7|68.6|7.7|75.6|48.4|
|DDIM|80.0|4.8|52.6|80.3|70.5|55.4|9.4|68.3|48.3|
|Flow Matching|80.0|7.2|34.6|79.2|46.9|57.8|11.1|77.4|45.0|
|_VLM Backbone Capacity_||||||||||
|PaliGemma|69.8|1.1|17.1|32.1|22.9|32.6|2.8|24.9|18.9|
|LLaMA3.2 + SigLIP2|80.0|7.2|34.6|79.2|46.9|57.8|11.1|77.4|45.0|
|Qwen3-VL-2B|90.0|9.6|42.0|74.6|75.0|68.6|27.9|83.6|53.7|
|Qwen3-VL-4B|95.8|12.2|66.0|93.3|89.0|81.0|29.9|88.6|64.8|
|_VLM-Policy Connection_||||||||||
|Loose Connection|90.0|9.6|42.0|74.6|75.0|68.6|27.9|83.6|53.7|
|Tight Connection|90.0|14.4|51.7|81.0|68.5|67.8|25.1|82.1|55.4|
|Soft Connection|91.8|11.8|58.3|89.2|72.9|74.4|19.9|72.5|56.2|
|**_Perception Essentials_**||||||||||
|_Temporal Observation History_||||||||||
|Current Frame Image|91.8|11.8|58.3|89.2|72.9|74.4|19.9|72.5|56.2|
|Temporal Observation History|85.0|7.2|68.6|51.5|65.8|62.0|20.8|80.8|50.2|
|_Camera View Horizon_||||||||||
|Third-person camera view|91.8|11.8|58.3|89.2|72.9|74.4|19.9|72.5|56.2|
|Multi-view (third-person + wrist)|97.6|64.9|54.0|91.8|97.7|93.0|85.5|90.1|80.5|
|_Proprioception Conditioning_||||||||||
|No Proprioception Input|97.6|64.9|54.0|91.8|97.7|93.0|85.5|90.1|80.5|
|Proprioception to VLM|98.0|87.2|62.2|86.2|98.3|93.8|92.0|96.6|87.7|
|Proprioception to Policy|96.2|62.8|69.1|92.3|92.5|96.5|87.2|88.3|83.4|
|Proprioception to VLM & Policy|97.6|77.9|73.4|82.3|90.1|94.6|90.6|88.8|84.8|
|Linear Projector|98.0|87.2|62.2|86.2|98.3|93.8|92.0|96.6|87.7|
|Transformer Projector|96.4|96.8|58.0|84.6|95.2|98.8|96.9|93.3|88.8|
|Transformer Projector & MAE|97.0|91.1|51.1|89.9|72.8|86.9|78.7|85.6|78.9|
|**_Action Modeling Perspectives_**||||||||||
|_World Modeling Perspective_||||||||||
|Normal|98.0|87.2|62.2|86.2|98.3|93.8|92.0|96.6|87.7|
|World Modeling|98.0|94.4|80.3|76.9|99.7|98.8|93.2|93.2|90.3|
|_Time Series Forecasting Perspectiv_|_e_|||||||||
|Normal|98.0|87.2|62.2|86.2|98.3|93.8|92.0|96.6|87.7|
|Frequency Domain Loss|99.0|95.7|78.6|86.9|99.7|98.8|98.0|96.6|93.1|


6 


Fig. 5. Design choices for proprioception conditioning. 

_inputs does not improve action generation_ and slightly degrades performance under the standard VLA formulation (Table I), indicating that redundant temporal inputs may introduce noise or distract the model, even though the backbone is already pretrained for video understanding. However, explicitly modelingrevisit temporalpredictivedynamicsrepresentationmaydynamicsrepresentationmaymay be morelearningeffective,andeffective,and whichworld we revisit throughtemporalpredictivedynamicsrepresentationmaypredictivedynamicsrepresentationmayrepresentationmay learningeffective,andand world action modeling in Sec. V. 

**Camera View Horizon.** We study the effect of camera viewpoints on VLA performance. Our baseline uses a single third-person view, following OpenVLA [5]. Many robotics datasets [2], [155] additionally provide an in-hand wrist camera, allowing choices between single-view and multi-view inputs. Results show that _combining third-person and wrist views significantly improves performance_ (Table I), suggesting that multi-view observations provide complementary geometric cues that help resolve spatial ambiguities. 

Fig. 6. Augmenting action prediction with an auxiliary world modeling objective. 

**World Modeling.** We first study world modeling as an auxiliary objective within the standard VLA architecture [17], [94]. To isolate the effect of dynamics supervision, we deliberately avoid using a pretrained visual generator. Instead, we tokenize images using the Emu3.5 image tokenizer [157] and predict future image tokens with a next-token objective. The target is the future frame at a fixed horizon (8 steps, aligned with the action chunk length). The visual generation module is inserted between the VLM and the policy module with layer-wise connections (Fig. 6). _Adding world modeling improves action generation performance_ (Table I), indicating that predicting future observations is beneficial. Although this auxiliary worldmodeling objective improves action prediction, it nearly triples the training cost. We therefore exclude this auxiliary branch from the core recipe of the base VLANeXt. Later, in Sec. V, we revisit explicit future prediction through two emerging paradigms: JEPA-style latent predictive representation learning and world action modeling with a pretrained video-generation backbone. 

**Proprioception Conditioning.** We examine the role of proprioception, which provides information about the robot’s internal state and motion history. Our baseline, following OpenVLA [5], does not use proprioceptive inputs. We compare three variants: conditioning the VLM, conditioning the policy module, and conditioning both (Fig. 5). Specifically, proprioception is provided as input to the VLM. For the policy, we use historical actions as input to align with the generated actions. 

Results show that _conditioning proprioception in the VLM yields the best performance_ (Table I). We hypothesize that integrating proprioception at the VLM level allows better fusion with visual and language inputs, whereas injecting it directly into the policy module may reduce reliance of action prediction on visual observations and instructions. Although this appears to differ from the conclusion reported by Zhao _et al._ [73], who claim that proprioception is not needed, their study evaluates architectures where proprioception is injected only into the policy module. In that setting, removing proprioception improves performance, which is consistent with our LIBERO results. 

**Time Series Forecasting.** We also explore facilitating action generation from a time-series forecasting perspective. Inspired by frequency-domain modeling in time-series prediction [158]– [161], we introduce a simple auxiliary loss that minimizes the MSE between predicted and ground-truth actions in the frequency domain. We use the discrete cosine transform [162] to convert the action to the frequency domain, and assign higher weights to low-frequency components and lower weights to high-frequency components, as high-frequency components are often noisier. 

We further compare three different integration mechanisms, including a linear projector, a transformer-based projector, and a transformer projector with masked reconstruction pretraining [156]. The _transformer-based projector performs slightly better on LIBERO-plus_ (Table I); for simplicity, we use the linear projector in the core recipe of our base design. 

This strategy _improves action generation performance_ , slightly surpassing the auxiliary world-modeling variant studied above while adding negligible training overhead (Table I). The gain likely arises because it serves as a regularization term to prevent the model from overfitting to trajectory jitter, thereby improving generalization. 

# _C. Action Modeling Perspectives_ 

Here, we examine auxiliary design and training objectives to facilitate action generation. 

7 


Fig. 7. **VLANeXt architecture** . Multi-view visual inputs, language instructions, and proprioception are tokenized and processed by a multimodal LLM, with meta queries enabling soft interaction with the policy module. Action chunks are predicted using flow matching and further regularized by a frequency-domain objective. 

# _D. Summary of Recipes_ 

Starting from a classical RT-2/OpenVLA-style baseline, we find that strong VLA performance emerges from a series of principled design choices. Beneficial changes include: replacing token reuse with a deeper, dedicated policy module; adopting action chunking to model longer temporal action horizons; using continuous objectives such as flow matching (with regression also effective under simple distributions); employing a stronger VLM backbone (Qwen3-VL-2B as an effective–efficient choice); and connecting the VLM and policy module through soft, layer-wise interactions with learnable query buffers. 

On the perception side, multi-view inputs (third-person + wrist) and VLM-side proprioception conditioning improve performance, while simply adding past observations as additional VLM inputs does not improve performance under the standard formulation. Moreover, adding a lightweight frequency-domain auxiliary loss further boosts action generation with negligible cost. Although the auxiliary world-modeling variant studied above also improves performance, its substantially higher training cost makes it less practical. Together, these choices define the **core recipe** and instantiate the base VLANeXt model. Importantly, the recipe above is distilled within the standard VLA formulation. In Secs. V and VI, we further examine whether these principles remain effective as VLAs scale and evolve toward latent-action, predictive-representation, and world-action modeling paradigms. 

# IV. EVALUATION OF THE CORE RECIPE 

# _A. Benchmark Evaluations_ 

_1) Settings:_ Having distilled the core recipe, we first evaluate the resulting base VLANeXt under the standard VLA formulation, covering both simulation benchmarks and realworld deployment. The emerging-paradigm extensions are evaluated separately in Sec. VI. To evaluate both standard performance and generalization robustness, we employ the LIBERO ecosystem. We first evaluate our base VLANeXt on the standard LIBERO benchmark [21], which provides four distinct categories (Spatial, Object, Goal, and Long) to test 

the task learning ability, each providing 500 expert episodes across 10 tasks to assess policy performance across different spatial layouts, objects, goals, and long-horizon tasks. 

To test the generalization boundaries of our model further, we evaluate our method on LIBERO-plus [22]. Unlike the static conditions in standard LIBERO, LIBERO-plus introduces systematic variations to the evaluation episodes, comprising 10,030 episodes across the above four suites in LIBERO, with perturbations in visual ( _e.g._ , lighting, background, camera pose), physical ( _e.g._ , object layout, robot state), and semantic ( _e.g._ , language instruction rewrites) dimensions. 

Following the standard setting in OpenVLA [5], we train our models on the modified LIBERO dataset for each suite (Spatial, Object, Goal, and Long), and evaluate performance on both the LIBERO and LIBERO-plus benchmarks (which include unseen perturbations) for the corresponding suite. Notably, for LIBERO-plus, models are trained only on the original LIBERO data and directly evaluated under unseen perturbations, without perturbation-specific training. For fair comparisons across different design choices, we directly fine-tune all models on the LIBERO dataset. All core-recipe ablations in Sec. III use 10,000 training steps with a batch size of 256. The learning rate is set to 1 _×_ 10<sup>_−_4</sup> for models smaller than 3B parameters and 5 _×_ 10<sup>_−_5</sup> otherwise in our explorations. 

_2) LIBERO Benchmark Results:_ On the LIBERO benchmark, we compare our method against two categories of approaches: (i) direct policy learning methods that are trained solely on robotic datasets, and (ii) VLA methods that leverage knowledge from pretrained VLMs for policy learning. For direct policy learning methods, we include Diffusion Policy [57], Octo [60], and MDT [163]. For VLA methods, we compare against OpenVLA [5], TraceVLA [92], SpatialVLA [15], WorldVLA [17], CoT-VLA [93], _π_ 0 [6], _π_ 0-Fast [125], NORA [8], SmolVLA [10], UniVLA [99], FLOWER [138], and OpenVLAOFT [9]. 

The comparison results are shown in Table II. As we can observe, the base VLANeXt instantiated by the core recipe achieves state-of-the-art performance, demonstrating that the distilled design principles provide a strong foundation for the standard VLA formulation. 

_3) LIBERO-plus Benchmark Results:_ For the LIBEROplus benchmark, we compare our model with several VLA models such as OpenVLA [5], WorldVLA [17], NORA [8], UniVLA [99], _π_ 0 [6], _π_ 0-Fast [125], and OpenVLA-OFT [9]. 

As shown in Table III, the proposed VLANeXt model demonstrates strong generalization ability across different types of unseen perturbations. Moreover, VLANeXt improves the success rate by 14.3 percentage points over the previous state-of-the-art method, OpenVLA-OFT [9], on LIBERO-plus, suggesting that the core recipe also provides strong robustness and generalization under unseen perturbations. 

# _B. Real-World Evaluations_ 

To comprehensively assess the performance of our method, we additionally evaluate it in real-world deployments. 

_1) Settings:_ We design four tasks, including two single-arm tasks and two bimanual tasks, to evaluate our method. The 

8 

TABLE II 

LIBERO BENCHMARK PERFORMANCE. THE RESULTS ARE SHOWN IN SUCCESS RATE (%). S, O, G, L: SPATIAL, OBJECT, GOAL, AND LONG SUITES, RESPECTIVELY. WE COLOR THE **BEST** AND SECOND <mark>-</mark> BEST RESULTS. 

|**Model**|**S**|**O**|**G**|**L**|**Avg**|
|---|---|---|---|---|---|
|_Baseline Direct Po_|_licy Mod_|_els_||||
|Diffusion Policy|78.3|92.5|68.3|50.5|72.4|
|Octo|78.9|85.7|84.6|51.5|75.1|
|MDT|78.5|87.5|73.5|64.8|76.1|
|_Baseline VLA Mod_|_els_|||||
|TraceVLA|84.6|85.2|75.1|54.1|74.8|
|OpenVLA|84.7|88.4|79.2|53.7|76.5|
|SpatialVLA|88.2|89.9|78.6|55.5|78.1|
|WorldVLA|85.6|89.0|82.6|59.0|79.1|
|CoT-VLA|87.5|91.6|87.6|69.0|83.9|
|_π_0-Fast|96.4|96.8|88.6|60.2|85.5|
|_π_0|90.0|86.0|95.0|73.0|86.0|
|NORA|92.2|95.4|89.4|74.6|87.9|
|SmolVLA|93.0|94.0|91.0|77.0|88.8|
|UniVLA|96.5|96.8|95.6|92.0|95.2|
|FLOWER|97.5|99.1|96.1|**94.9**|96.9|
|_π_0_._5|98.8|98.2|**98**|92.4|96.9|
|OpenVLA-OFT|97.6|98.4|97.9|94.5|97.1|
|_Ours_||||||
|**VLANeXt**|**99.0**|**99.2**|96.6|94.8|**97.4**|


Fig. 8. Our single-arm and bimanual arm tasks for the real-world experiments. 

single-arm tasks include table cleaning, which involves picking up objects from a table and placing them into a container, and drawer manipulation, where the robot opens a drawer, places objects inside, and closes it. The bimanual tasks include basket lifting, which requires lifting a basket using both hands, and bimanual table cleaning, where two arms coordinate to collect objects from a table and place them into a container. The single-arm experiments use Franka Emika, while the bimanual experiments are conducted on the Aloha system [164]. A visualization of the experimental setup for each task is depicted in Figure 8. 


Fig. 9. **VLANeXt Family: Extending VLANeXt to Emerging Paradigms** . We extend the core VLANeXt recipe along four emerging directions: (a) model scaling with different MLLM backbone sizes; (b) latent-action pretraining with latent actions from current and future frames; (c) latent predictive representation learning through JEPA-style prediction in DINO space; and (d) world action modeling by jointly modeling future video and actions. These variants form the VLANeXt family, enabling us to examine the generality of the distilled design recipe across model scales and emerging paradigms. 

For training, we collect 50 episodes per task and evaluate each model over 20 trials, reporting the success rate. We first pretrain the model on the DROID dataset [155] for 100k steps, then fine-tune it on each task for 20k steps with a learning rate of 1 _×_ 10<sup>_−_4</sup> . Because DROID contains only single-arm data, adapting the model to bimanual tasks requires reinitializing the proprioception projector and the final layer of the action generation module, while keeping all other pretrained weights. 

_2) Results:_ We compare against two representative VLA baselines, OpenVLA-OFT [9] and _π_ 0 [6]. We load their pretrained checkpoints and fine-tune them on each task in the same manner as our method to ensure a fair comparison. The results are shown in Table IV. As can be seen, our model performs well in real-world experiments, demonstrating that the core recipe yields a strong base VLA that performs effectively in real-world deployment. Moreover, despite being pretrained only on single-arm DROID data, our method can adapt to bimanual tasks after task-specific fine-tuning, demonstrating its adaptability across embodiments. Additional video demonstrations of our experimental results are provided in the supplementary materials. 

Together, these results validate the core recipe under the standard VLA formulation, from simulated benchmarks to realworld manipulation. We next examine whether the same design principles remain effective as the VLA paradigm itself evolves. 

# V. BEYOND THE CORE RECIPE: EXTENDING VLANEXT TO EMERGING PARADIGMS 

The VLA field is rapidly evolving beyond the standard formulation, with several emerging paradigms introducing different priors for action learning. We focus on four representative directions: _model scaling_ , which introduces modelcapacity priors [127], [136]; _latent-action pretraining_ , which leverages action-like priors learned from unlabeled visual transitions [131], [132], [165]; _latent predictive representation_ 

9 

TABLE III 

LIBERO-PLUS BENCHMARK PERFORMANCE. ALL THE EVALUATED METHODS ARE TRAINED USING THE LIBERO DATASET AND DIRECTLY TESTED ON THE LIBERO-PLUS BENCHMARK WITH UNSEEN PERTURBATIONS. THE RESULTS ARE SHOWN IN SUCCESS RATE (%). WE COLOR THE **BEST** AND SECOND <mark>-</mark> BEST RESULTS ON AVERAGE. THE COMPLETE PER-SUITE RESULTS OF THE LISTED METHODS CAN ALSO BE FOUND IN THE LIBERO-PLUS STUDY BY FEI ET AL. [22]. 

|**Model**|**Suite**|**Camera**|**Robot**|**Language**|**Light**|**Background**|**Noise**|**Layout**|**Total**|
|---|---|---|---|---|---|---|---|---|---|
|_Baseline VLA Mod_|_els_|||||||||
|OpenVLA|Average|0.8|3.5|23.0|8.1|34.8|15.2|28.5|15.6|
|WorldVLA|Average|0.1|27.9|41.6|43.7|17.1|10.9|38.0|25.0|
|NORA|Average|2.2|37.0|65.1|45.7|58.6|12.8|62.1|39.0|
|UniVLA|Average|1.8|46.2|69.6|69.0|81.0|21.2|31.9|42.9|
|_π_0|Average|13.8|6.0|58.8|85.0|81.4|79.0|68.9|53.6|
|_π_0-Fast|Average|65.1|21.6|61.0|73.2|73.2|74.4|68.8|61.6|
||Spatial|88.3|40.0|80.5|98.3|97.3|96.3|93.9|84.0|
||Object|38.9|25.4|99.0|73.7|97.6|72.3|71.8|66.5|
|OpenVLA-OFT|Goal|62.0|25.2|53.2|93.9|92.5|75.2|59.1|63.0|
||Long|38.7|38.2|87.0|89.4|86.8|63.5|76.9|66.4|
||Average|56.4|31.9|79.5|88.7|**93.3**|75.8|74.2|69.6|
|_Ours_||||||||||
||Spatial|95.7|78.6|86.9|99.7|98.8|98.0|96.6|93.1|
||Object|99.5|48.5|98.6|99.3|84.7|99.8|78.2|86.5|
|VLANeXt|Goal|96.6|63.6|51.5|97.5|70.8|96.8|63.9|76.2|
||Long|69.7|72.0|90.3|86.9|75.8|81.7|84.3|79.7|
||Average|**90.4**|**65.7**|**81.8**|**95.9**|82.5|**94.1**|**80.8**|**83.9**|


TABLE IV REAL-WORLD EVALUATION RESULTS. RESULTS ARE SHOWN AS (SUCCESS COUNT/TOTAL COUNT). WE COLOR THE **BEST** AND SECOND <mark>-</mark> BEST RESULTS. 

|**Model**|**Single **<br>**Clean**|**Arm**<br>**Drawer**|**Biman**<br>**Clean**|**ual Arm**<br>**Lifting**|
|---|---|---|---|---|
|_Baseline VLA Mo_|_dels_||||
|OpenVLA-OFT|7/20|7/20|5/20|9/20|
|_π_0|10/20|8/20|10/20|13/20|
|_Ours_|||||
|**VLANeXt**|**14/20**|**11/20**|**11/20**|**15/20**|


_learning_ , which provides semantic priors through JEPA-style future representation prediction [166], [167]; and _world action modeling_ , which incorporates world-dynamics priors by jointly modeling future visual dynamics and robot actions [101]–[103], [105]. To examine whether the VLANeXt core recipe generalizes to these emerging paradigms, we instantiate them within the same framework, yielding **VLANeXt-S** and **VLANeXtL** for model scaling, **VLANeXt-LAM** for latent-action pretraining, **VLANeXt-JEPA** for latent predictive representation learning, and **VLANeXt-WAM** for world action modeling. Together with the original VLANeXt, these variants form the **VLANeXt family** , as illustrated in Fig. 9. As shown in Tab. V, the _core recipe remains effective across these variants despite their distinct model scales and sources of prior_ , demonstrating that the identified design principles generalize beyond the standard VLA formulation. 

# _A. Model Scaling_ 

First, we study _model scaling_ in VLANeXt. Since the majority of model capacity in a VLA typically comes from its pretrained backbone, scaling VLANeXt can be naturally realized by varying the backbone size while keeping the 

remaining architecture and training recipe unchanged. Specifically, we replace the original Qwen3-VL-2B backbone [152] with Qwen3.5-0.8B [168] and Qwen3-VL-4B [152], yielding **VLANeXt-S** ( _S_ for small) and **VLANeXt-L** ( _L_ for large), respectively. Together with the original VLANeXt model, these variants form a controlled scaling spectrum across different model capacities. By consistently adopting backbones from the Qwen family, we minimize confounding factors introduced by changes in backbone design, enabling a cleaner evaluation of whether the core recipe remains effective across model scales. An overview of this extension is shown in Fig. 9(a), and more analysis can be seen in Sec. VI. 

# _B. Latent Action Modeling_ 

Second, we study _latent-action pretraining_ , which leverages action-like representations learned from visual transitions as a prior for downstream action learning [131], [132], [165]. A latent action model (LAM) typically learns a compact representation of the transition between two observations. Specifically, a latent action encoder takes the current and future frames as input and extracts a latent action that captures the transition between them, resembling an inverse-dynamics mechanism. The resulting latent action is then combined with the current frame to reconstruct or predict the future frame. Since the future frame is available to the encoder while also serving as the prediction target, the latent space must be constrained to prevent the latent action from trivially encoding the target observation. Representative constraints include VAE [169], which regularizes the latent space toward a Gaussian distribution; VQ-VAE [149], which discretizes the latent representation through vector quantization; and VICReg [170], which encourages informative, diverse, and decorrelated latent representations, as explored in Latent-inthe-Wild [165]. 

10 

TABLE V 

ABLATION OF THE CORE RECIPE ACROSS DIFFERENT EMERGING PARADIGMS IN VLANEXT ON THE LIBERO BENCHMARK. THE TABLE SHOWS THE 

AVERAGE PERFORMANCE ACROSS THE FOUR SUITES OF THE LIBERO BENCHMARK. 

|**Model**|**Backbone**|**Full**|**w/o Chunk**|**w/o Multi-view**|**w/o Flow**|**w/o Prop.**|**w/o Freq.**|
|---|---|---|---|---|---|---|---|
|VLANeXt-S|Qwen3.5-0.8B|96.7|88.7 (-8.0)|89.9 (-6.8)|94.0 (-2.7)|95.8 (-0.9)|96.6 (-0.1)|
|VLANeXt-L|Qwen3-VL-4B|98.4|93.2 (-5.2)|94.6 (-3.8)|96.6 (-1.8)|96.8 (-1.6)|97.1 (-1.3)|
|VLANeXt-LAM|Qwen3-VL-2B|97.6|87.8 (-9.8)|85.8 (-11.8)|93.2 (-4.4)|94.6 (-3.0)|95.3 (-2.3)|
|VLANeXt-JEPA|Qwen3-VL-2B|97.7|91.2 (-6.5)|93.3 (-4.4)|96.7 (-1.0)|95.9 (-1.8)|95.5 (-2.2)|
|VLANeXt-WAM|WAN2.2-5B|98.2|94.1 (-4.1)|89.9 (-8.3)|96.0 (-2.2)|97.6 (-0.6)|98.0 (-0.2)|


## TABLE VI 

COMPARISON OF LATENT-ACTION MODELING VARIANTS ON THE LIBERO BENCHMARK. 

|**Model**|**Pretraining**|**Trainin**|**g Steps**||**LI**|**BERO**|||
|---|---|---|---|---|---|---|---|---|
|||Pretrain|Finetune|Spatial|Object|Goal|Long|Avg|
|_Baseline VLA Models_|||||||||
|VLANeXt|–|–|10k|99.0|99.2|96.6|94.8|97.4|
|VLANeXt (matched training duration)|–|–|30k|98.8|98.8|96.2|94.0|97.0|
|_Latent Action Modeling_|||||||||
|VLANeXt-LAM|LAM (VICReg)|20k|10k|95.4|99.6|97.0|95.4|96.9|
|VLANeXt-LAM|LAM (VAE)|20k|10k|98.0|97.8|95.2|96.2|96.8|
|VLANeXt-LAM|LAM (VQ-VAE)|20k|10k|98.0|99.8|95.6|97.0|97.6|


## TABLE VII 

ABLATION OF LATENT PREDICTIVE OBJECTIVES IN VLANEXT-JEPA ON THE LIBERO BENCHMARK. 

|**Model**|**Generator**|**Objective**||**LI**|**BERO**|||
|---|---|---|---|---|---|---|---|
||||Spatial|Object|Goal|Long|Avg|
|_Baseline VLA Mo_|_del_|||||||
|VLANeXt|–|action only|99.0|99.2|96.6|94.8|97.4|
|_Latent Predictive _|_Representation Learning_|||||||
|VLANeXt|Emu3.5 + transformer|action + final image of current horizon|97.6|99.8|95.4|92.8|96.4|
|VLANeXt-JEPA|DINOv3 encoder + DiT|action + final image of the episode|98.0|99.2|96.4|93.0|96.6|
|VLANeXt-JEPA|DINOv3 encoder + DiT|action + final image of current horizon|98.0|99.8|97.0|95.8|97.7|


## TABLE VIII 

COMPARISON OF WORLD ACTION MODELING VARIANTS ON THE LIBERO BENCHMARK. THE ACTION-ONLY BASELINE USES THE SAME WAN2.2-5B BACKBONE AND TRAINING SETUP BUT REMOVES THE VIDEO-GENERATION OBJECTIVE. 

|**Model**|**Backbone**|**Objective**|**Video & Action Connection**||**LI**|**BERO**|||
|---|---|---|---|---|---|---|---|---|
|||||Spatial|Object|Goal|Long|Avg|
|_Baseline VLA Mod_|_els_||||||||
|VLANeXt|Qwen3-VL-2B|action-only|–|99.0|99.2|96.6|94.8|97.4|
|VLANeXt-WAM|WAN2.2-5B|action-only|–|95.0|99.6|96.4|91.2|95.6|
|_World Action Mod_|_eling_||||||||
|VLANeXt-WAM|WAN2.2-5B|action & video|fast connection|97.8|99.4|99.6|96.0|98.2|
|VLANeXt-WAM|WAN2.2-5B|action & video|joint connection|95.2|99.8|97.0|98.2|97.6|


We incorporate this paradigm into VLANeXt through a two-stage latent-action pretraining and real-action fine-tuning pipeline. We first train a LAM on the full LIBERO dataset [21] and use it to extract latent actions for all LIBERO trajectories. We then pretrain VLANeXt on the full dataset using these latent actions as supervision, before fine-tuning the pretrained model on each LIBERO suite with the corresponding groundtruth robot actions. This setup allows us to directly examine whether action-like priors learned from visual transitions can be transferred to downstream action learning with real action labels. An overview of this extension is shown in Fig. 9(b), 

with further analysis provided in Sec. VI. 

_C. Latent Predictive Representation Learning_ 

Next, we study _latent predictive representation learning_ , also referred to as JEPA-style predictive representation learning. This paradigm leverages semantic representations learned by pretrained representation models, such as DINO [171] and JEPA [172], as a prior for action learning. Rather than predicting future observations directly in pixel or token space, the model learns to predict their latent semantic representations and jointly optimizes this predictive objective with action 

11 

TABLE IX 

ABLATION OF DIFFERENT BACKBONE CHOICES FOR VLANEXT ON THE LIBERO BENCHMARK. 

# VI. EVALUATING THE CORE RECIPE ACROSS EMERGING PARADIGMS 

# _A. Settings_ 

|**Backbone**||**LI**|**BERO**|||
|---|---|---|---|---|---|
||Spatial|Object|Goal|Long|Avg|
|Qwen3.5-0.8B|95.4|99.4|95.4|96.4|96.7|
|Qwen3.5-2B|97.8|100.0|98.0|97.4|98.3|
|Qwen3.5-4B|97.4|99.6|97.2|95.2|97.4|
|Qwen3-VL-2B|99.0|99.2|96.6|94.8|97.4|
|Qwen3-VL-4B|99.2|100.0|98.0|96.4|98.4|
|Qwen3-VL-8B|98.0|99.4|97.4|95.8|97.7|


In this section, we conduct further analysis and ablation studies for the four emerging paradigms introduced in Sec. V. We follow the training and evaluation protocol described in Sec. IV. Specifically, models are trained on LIBERO [21] and evaluated on all four suites: Spatial, Object, Goal, and Long. We report the success rate for each suite and their average. 

# _B. Ablation Analysis_ 

learning. The underlying motivation is that effective robot control depends primarily on capturing task-relevant semantics, such as what changes should occur and where the interaction should take place, rather than reconstructing all low-level visual details. 

We incorporate this paradigm into VLANeXt by introducing an additional predictor between the VLM backbone and the policy module, which predicts the latent representation of the future observation. This design naturally extends the world-modeling objective explored earlier in our core-recipe study, where an auxiliary predictor was used to predict Emu3.5 [157] tokens of the future image. Here, we retain the same general predictive formulation but replace the Emu3.5 tokenizer with the semantic encoder DINOv3 [171], shifting the prediction target from generative visual tokens to semantic latent representations. This controlled modification allows us to examine whether semantic predictive priors provide a more effective auxiliary signal for action learning. An overview of this extension is shown in Fig. 9(c), with further analysis provided in Sec. VI. 

# _D. World Action Modeling_ 

Finally, we study _world action modeling_ [101]–[103], [105]. World modeling has long been explored as a way to provide predictive priors for robot learning, including the future-image token prediction objective investigated in our core-recipe study and the latent predictive representation learning paradigm discussed above. Here, we focus on a recently emerging formulation, World Action Models (WAMs), which replace the conventional VLM backbone with a pretrained video-generation model and jointly model future visual dynamics and robot actions. Since the video-generation backbone is pretrained on large-scale video data, it provides a strong world-dynamics prior that can be transferred to downstream action learning. 

We incorporate this paradigm into VLANeXt by replacing the original VLM backbone with a video-generation backbone and jointly optimizing video generation and action prediction within the same framework. This extension allows us to examine whether the core VLANeXt recipe remains effective when action learning is built upon an explicit world-dynamics prior rather than a conventional VLM representation. An overview of this extension is shown in Fig. 9(d), with further analysis provided in Sec. VI. 

**Model Scaling.** We first investigate model scaling by evaluating additional backbone sizes from both Qwen3.5 [168] and Qwen3-VL [152]. As reported in Tab. IX, increasing backbone capacity initially leads to clear improvements. Within the Qwen3.5 family, scaling from 0.8B to 2B parameters improves the average success rate from 96.7% to 98.3%, while within Qwen3-VL, scaling from 2B to 4B improves performance from 97.4% to 98.4%. However, the gains are not monotonic at larger scales: Qwen3.5-4B achieves 97.4% and Qwen3-VL-8B achieves 97.7%, both below their intermediatescale counterparts. We hypothesize that this saturation is partly due to the limited scale and diversity of the LIBERO dataset, which may be insufficient to fully exploit the additional capacity of larger pretrained backbones. 

**Latent-Action Constraints.** We then investigate how different constraints on the latent action space affect latentaction pretraining. Following Latent-in-the-Wild [165], we compare three representative formulations: VAE [169], VQVAE [149], and VICReg [170]. We additionally include a VLANeXt baseline trained for 30k steps, matching the total optimization duration of latent-action pretraining followed by action fine-tuning, to distinguish the benefit of latent-action priors from that of simply training for longer. As shown in Tab. VI, increasing the baseline training duration from 10k to 30k steps does not improve performance, with the average success rate decreasing slightly from 97.4% to 97.0%. In contrast, the VQ-VAE variant achieves the best performance among the three latent-action formulations, reaching an average success rate of 97.6% and improving particularly on the Long suite. These results suggest that the gain from VLANeXt-LAM is not explained by additional optimization alone, but depends on the action-like prior acquired during latent-action pretraining. We hypothesize that the discrete bottleneck introduced by VQVAE encourages a compact representation of visual transitions and suppresses shortcut encoding, making the resulting latent actions more transferable to downstream action learning. 

**Latent Predictive Objectives.** We next examine the design of the predictive objective in VLANeXt-JEPA along two dimensions: the representation space used as the prediction target and the temporal horizon of prediction. For the representation space, we compare semantic features extracted by DINOv3 [171] against the Emu3.5 [157] visual tokens considered in our core-recipe study. For the temporal target, we compare predicting the final observation within the current action horizon against predicting the final observation of the 

12 

entire episode. As shown in Tab. VII, predicting the horizonfinal representation achieves an average success rate of 97.7%, outperforming both the episode-final variant (96.6%) and the action-only VLANeXt baseline (97.4%). This result indicates that predictive representations are most useful when their temporal scope remains closely aligned with the action horizon, whereas predicting a substantially more distant future state can introduce an overly difficult or weakly aligned auxiliary objective. The comparison with the Emu3.5-token objective further shows that prediction in the DINOv3 semantic space is more effective than prediction in the generative visual-token space, suggesting that task-relevant semantics provide a more useful predictive prior for action learning than low-level visual reconstruction targets. 

**World Action Modeling.** Finally, we study how video generation should interact with action prediction in VLANeXtWAM. We compare three variants based on the same WAN2.25B [173] backbone: an action-only model without videogeneration supervision and two models using the fast and joint connections introduced in Fast-WAM [101]. In the fast formulation, action prediction does not directly attend to future video tokens, whereas the joint formulation allows interactions between the action and future-video streams. As shown in Tab. VIII, using the video backbone for action prediction alone achieves an average success rate of only 95.6%. Introducing video-generation and action-learning objectives together substantially improves performance, reaching an average success rate of 98.2% with the fast connection and 97.6% with the joint connection. Importantly, the fast formulation performs best despite preventing action prediction from directly attending to future video tokens. This suggests that the main benefit of world action modeling comes from transferring the worlddynamics prior learned through the video-generation objective, rather than requiring action prediction to explicitly consume the large-scale generated future representations. 

# VII. CONCLUSION 

In summary, this work takes a step toward a more systematic understanding of VLA models. Rather than introducing another standalone architecture, we reexamine the VLA design space under a unified framework and evaluation protocol, spanning foundational components, perception essentials, and action modeling perspectives. Our study shows that strong VLA performance can emerge from principled design choices throughout the pipeline, including how the VLM interacts with the policy module, how perceptual signals such as multiview observations and proprioception are integrated, and how temporal structure in actions is modeled. 

Beyond the standard VLA formulation, we further examine whether the distilled core recipe generalizes to emerging paradigms, including model scaling, latent-action pretraining, latent predictive representation learning, and world action modeling. The resulting VLANeXt family demonstrates that these design principles remain effective across different model scales and sources of prior, suggesting that the core recipe provides a broadly applicable foundation as VLA paradigms continue to evolve. 

By releasing a unified and lightweight framework, we aim to facilitate reproducible studies and systematic exploration of future VLA designs. Extending this perspective to more diverse embodiments, large-scale mid-training, failure recovery, and richer forms of prior knowledge remains an important direction for future research. 

# REFERENCES 

- [1] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “RT-2: Vision-language-action models transfer web knowledge to robotic control,” in _CoRL_ , 2023. 

- [2] A. O’Neill, A. Rehman, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain _et al._ , “Open X-Embodiment: Robotic learning datasets and RT-X models: Open X-Embodiment collaboration 0,” in _ICRA_ , 2024. 

- [3] X. Li, M. Liu, H. Zhang, C. Yu, J. Xu, H. Wu, C. Cheang, Y. Jing, W. Zhang, H. Liu _et al._ , “Vision-language foundation models as effective robot imitators,” in _ICLR_ , 2023. 

- [4] Q. Li, Y. Liang, Z. Wang, L. Luo, X. Chen, M. Liao, F. Wei, Y. Deng, S. Xu, Y. Zhang _et al._ , “CogACT: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation,” _arXiv preprint arXiv:2411.19650_ , 2024. 

- [5] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi _et al._ , “OpenVLA: An open-source vision-language-action model,” in _CoRL_ , 2024. 

- [6] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ 0: A vision-language-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [7] G. R. Team, S. Abeyruwan, J. Ainslie, J.-B. Alayrac, M. G. Arenas, T. Armstrong, A. Balakrishna, R. Baruch, M. Bauza, M. Blokzijl _et al._ , “Gemini Robotics: Bringing AI into the physical world,” _arXiv preprint arXiv:2503.20020_ , 2025. 

- [8] C.-Y. Hung, Q. Sun, P. Hong, A. Zadeh, C. Li, U. Tan, N. Majumder, S. Poria _et al._ , “NORA: A small open-sourced generalist vision language action model for embodied tasks,” _arXiv preprint arXiv:2504.19854_ , 2025. 

- [9] M. J. Kim, C. Finn, and P. Liang, “Fine-tuning vision-languageaction models: Optimizing speed and success,” _arXiv preprint arXiv:2502.19645_ , 2025. 

- [10] M. Shukor, D. Aubakirova, F. Capuano, P. Kooijmans, S. Palma, A. Zouitine, M. Aractingi, C. Pascal, M. Russi, A. Marafioti _et al._ , “SmolVLA: A vision-language-action model for affordable and efficient robotics,” _arXiv preprint arXiv:2506.01844_ , 2025. 

- [11] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai _et al._ , “ _π_ 0 _._ 5: a visionlanguage-action model with open-world generalization,” _arXiv preprint arXiv:2504.16054_ , 2025. 

- [12] P. Intelligence, A. Amin, R. Aniceto, A. Balakrishna, K. Black, K. Conley, G. Connors, J. Darpinian, K. Dhabalia, J. DiCarlo _et al._ , “ _π_ 0<sup>_∗_</sup> _._ 6<sup>:a</sup> VLA that learns from experience,” _arXiv preprint arXiv:2511.14759_ , 2025. 

- [13] H. Liu, X. Li, P. Li, M. Liu, D. Wang, J. Liu, B. Kang, X. Ma, T. Kong, and H. Zhang, “Towards generalist robot policies: What matters in building vision-language-action models,” _Nature Machine Intelligence_ , 2026. 

- [14] H. Zhen, X. Qiu, P. Chen, J. Yang, X. Yan, Y. Du, Y. Hong, and C. Gan, “3D-VLA: A 3D vision-language-action generative world model,” in _ICML_ , 2024. 

- [15] D. Qu, H. Song, Q. Chen, Y. Yao, X. Ye, Y. Ding, Z. Wang, J. Gu, B. Zhao, D. Wang _et al._ , “SpatialVLA: Exploring spatial representations for visual-language-action model,” _arXiv preprint arXiv:2501.15830_ , 2025. 

- [16] W. Zhang, H. Liu, Z. Qi, Y. Wang, X. Yu, J. Zhang, R. Dong, J. He, F. Lu, H. Wang _et al._ , “DreamVLA: a vision-language-action model dreamed with comprehensive world knowledge,” in _NeurIPS_ , 2025. 

- [17] J. Cen, C. Yu, H. Yuan, Y. Jiang, S. Huang, J. Guo, X. Li, Y. Song, H. Luo, F. Wang _et al._ , “WorldVLA: Towards autoregressive action world model,” _arXiv preprint arXiv:2506.21539_ , 2025. 

- [18] J. Zhang, Y. Guo, Y. Hu, X. Chen, X. Zhu, and J. Chen, “UP-VLA: A unified understanding and prediction model for embodied agent,” in _ICML_ , 2025. 

13 

- [19] Z. Zhang, K. Zheng, Z. Chen, J. Jang, Y. Li, S. Han, C. Wang, M. Ding, D. Fox, and H. Yao, “GRAPE: Generalizing robot policy via preference alignment,” in _ICRA_ , 2025. 

- [20] G. Lu, W. Guo, C. Zhang, Y. Zhou, H. Jiang, Z. Gao, Y. Tang, and Z. Wang, “VLA-RL: Towards masterful and general robotic manipulation with scalable reinforcement learning,” _arXiv preprint arXiv:2505.18719_ , 2025. 

- [21] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “LIBERO: Benchmarking knowledge transfer for lifelong robot learning,” in _NeurIPS_ , 2023. 

- [22] S. Fei, S. Wang, J. Shi, Z. Dai, J. Cai, P. Qian, L. Ji, X. He, S. Zhang, Z. Fei _et al._ , “LIBERO-Plus: In-depth robustness analysis of visionlanguage-action models,” _arXiv preprint arXiv:2510.13626_ , 2025. 

- [23] X.-M. Wu, B. Fan, K. Liao, J.-J. Jiang, R. Yang, Y. Luo, Z. Wu, W.-S. Zheng, and C. C. Loy, “VLANeXt: Recipes for building strong VLA models,” in _ICML_ , 2026. 

- [24] H. Ravichandar, A. S. Polydoros, S. Chernova, and A. Billard, “Recent advances in robot learning from demonstration,” _ARCRAS_ , 2020. 

- [25] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “DeepMimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACMTOG_ , 2018. 

- [26] A. Kumar, Z. Fu, D. Pathak, and J. Malik, “RMA: Rapid motor adaptation for legged robots,” in _RSS_ , 2021. 

- [27] J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter, “Learning quadrupedal locomotion over challenging terrain,” _Science Robotics_ , 2020. 

- [28] G. B. Margolis and P. Agrawal, “Walk these ways: Tuning robot control for generalization with multiplicity of behavior,” in _CoRL_ , 2023. 

- [29] Y. Kim, H. Oh, J. Lee, J. Choi, G. Ji, M. Jung, D. Youm, and J. Hwangbo, “Not only rewards but also constraints: Applications on legged robot locomotion,” _TRO_ , 2024. 

- [30] M. Liu, D. Pathak, and A. Agarwal, “LocoFormer: Generalist locomotion via long-context adaptation,” in _CoRL_ , 2025. 

- [31] H.-S. Fang, C. Wang, M. Gou, and C. Lu, “GraspNet-1Billion: A large-scale benchmark for general object grasping,” in _CVPR_ , 2020. 

- [32] C. Wang, H.-S. Fang, M. Gou, H. Fang, J. Gao, and C. Lu, “Graspness discovery in clutters for fast and accurate grasp detection,” in _ICCV_ , 2021. 

- [33] X.-M. Wu, J.-F. Cai, J.-J. Jiang, D. Zheng, Y.-L. Wei, and W.-S. Zheng, “An economic framework for 6-DoF grasp detection,” in _ECCV_ , 2024. 

- [34] J.-F. Cai, Z. Chen, X.-M. Wu, J.-J. Jiang, Y.-L. Wei, and W.-S. Zheng, “Real-to-sim grasp: Rethinking the gap between simulation and real world in grasp detection,” in _CoRL_ , 2024. 

- [35] A.-L. Wang, N. Chen, K.-Y. Lin, Y.-M. Li, and W.-S. Zheng, “Taskoriented 6-DoF grasp pose detection in clutters,” in _ICRA_ , 2025. 

- [36] S. Liu, Y. Zhou, J. Yang, S. Gupta, and S. Wang, “ContactGen: Generative contact modeling for grasp generation,” in _ICCV_ , 2023. 

- [37] H. Li, X. Lin, Y. Zhou, X. Li, Y. Huo, J. Chen, and Q. Ye, “Contact2Grasp: 3D grasp synthesis via hand-object contact constraint,” in _IJCAI_ , 2023. 

- [38] S. Huang, Z. Wang, P. Li, B. Jia, T. Liu, Y. Zhu, W. Liang, and S.-C. Zhu, “Diffusion-based generation, optimization, and planning in 3D scenes,” in _CVPR_ , 2023. 

- [39] G.-H. Xu, Y.-L. Wei, D. Zheng, X.-M. Wu, and W.-S. Zheng, “Dexterous grasp transformer,” in _CVPR_ , 2024. 

- [40] Y.-L. Wei, J.-J. Jiang, C. Xing, X.-T. Tan, X.-M. Wu, H. Li, M. Cutkosky, and W.-S. Zheng, “Grasp as you say: Language-guided dexterous grasp generation,” in _NeurIPS_ , 2024. 

- [41] Y.-L. Wei, M. Lin, Y. Lin, J.-J. Jiang, X.-M. Wu, L.-A. Zeng, and W.-S. Zheng, “AffordDexGrasp: Open-set language-guided dexterous grasp with generalizable-instructive affordance,” in _ICCV_ , 2025. 

- [42] M. T. Mason, “Progress in nonprehensile manipulation,” _IJRR_ , 1999. [43] I. Mordatch, Z. Popovic, and E. Todorov, “Contact-invariant optimization´ for hand manipulation,” in _SIGGRAPH_ , 2012. 

- [44] J. Lyu, Z. Li, X. Shi, C. Xu, Y. Wang, and H. Wang, “DyWA: Dynamics-adaptive world action model for generalizable non-prehensile manipulation,” in _ICCV_ , 2025. 

- [45] K. Zakka, A. Zeng, J. Lee, and S. Song, “Form2Fit: Learning shape priors for generalizable assembly from disassembly,” in _ICRA_ , 2020. 

- [46] A. Zeng, P. Florence, J. Tompson, S. Welker, J. Chien, M. Attarian, T. Armstrong, I. Krasin, D. Duong, V. Sindhwani _et al._ , “Transporter networks: Rearranging the visual world for robotic manipulation,” in _CoRL_ , 2021. 

- [47] S. Levine, N. Wagener, and P. Abbeel, “Learning contact-rich manipulation skills with guided policy search,” in _ICRA_ , 2015. 

- [48] A. Rajeswaran, V. Kumar, A. Gupta, G. Vezzani, J. Schulman, E. Todorov, and S. Levine, “Learning complex dexterous manipulation with deep reinforcement learning and demonstrations,” _arXiv preprint arXiv:1709.10087_ , 2017. 

- [49] O. M. Andrychowicz, B. Baker, M. Chociej, R. Jozefowicz, B. McGrew, J. Pachocki, A. Petron, M. Plappert, G. Powell, A. Ray _et al._ , “Learning dexterous in-hand manipulation,” _IJRR_ , 2020. 

- [50] J. Matas, S. James, and A. J. Davison, “Sim-to-real reinforcement learning for deformable object manipulation,” in _CoRL_ , 2018. 

- [51] K. Mo, L. J. Guibas, M. Mukadam, A. Gupta, and S. Tulsiani, “Where2Act: From pixels to actions for articulated 3D objects,” in _ICCV_ , 2021. 

- [52] A. Zeng, S. Song, J. Lee, A. Rodriguez, and T. Funkhouser, “TossingBot: Learning to throw arbitrary objects with residual physics,” _TRO_ , 2020. 

- [53] J. Liu, R. Zhang, H.-S. Fang, M. Gou, H. Fang, C. Wang, S. Xu, H. Yan, and C. Lu, “Target-referenced reactive grasping for dynamic objects,” in _CVPR_ , 2023. 

- [54] N. Chen, X.-M. Wu, G. Xu, J.-J. Jiang, Z. Chen, and W.-S. Zheng, “MotionGrasp: Long-term grasp motion tracking for dynamic grasping,” _RA-L_ , 2024. 

- [55] A. Stoytchev, “Behavior-grounded representation of tool affordances,” in _ICRA_ , 2005. 

- [56] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu _et al._ , “RT-1: Robotics transformer for real-world control at scale,” in _RSS_ , 2023. 

- [57] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion Policy: Visuomotor policy learning via action diffusion,” _IJRR_ , 2025. 

- [58] L. Wang, X. Chen, J. Zhao, and K. He, “Scaling proprioceptive-visual learning with heterogeneous pre-trained transformers,” in _NeurIPS_ , 2024. 

- [59] S. Liu, L. Wu, B. Li, H. Tan, H. Chen, Z. Wang, K. Xu, H. Su, and J. Zhu, “RDT-1B: a diffusion foundation model for bimanual manipulation,” in _ICLR_ , 2024. 

- [60] D. Ghosh, H. R. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, J. Luo _et al._ , “Octo: An open-source generalist robot policy,” in _RSS_ , 2024. 

- [61] J. Barreiros, A. Beaulieu, A. Bhat, R. Cory, E. Cousineau, H. Dai, C.-H. Fang, K. Hashimoto, M. Z. Irshad, M. Itkina _et al._ , “A careful examination of large behavior models for multitask dexterous manipulation,” _Science Robotics_ , 2026. 

- [62] W. Huang, P. Abbeel, D. Pathak, and I. Mordatch, “Language models as zero-shot planners: Extracting actionable knowledge for embodied agents,” in _ICML_ , 2022. 

- [63] M. Shridhar, L. Manuelli, and D. Fox, “Perceiver-Actor: A multi-task transformer for robotic manipulation,” in _CoRL_ , 2023. 

- [64] I. Radosavovic, B. Shi, L. Fu, K. Goldberg, T. Darrell, and J. Malik, “Robot learning with sensorimotor pre-training,” in _CoRL_ , 2023. 

- [65] W. Huang, C. Wang, R. Zhang, Y. Li, J. Wu, and L. Fei-Fei, “VoxPoser: Composable 3D value maps for robotic manipulation with language models,” in _CoRL_ , 2023. 

- [66] Y. Ze, G. Zhang, K. Zhang, C. Hu, M. Wang, and H. Xu, “3D Diffusion Policy: Generalizable visuomotor policy learning via simple 3D representations,” in _ICRA_ , 2024. 

- [67] G. Lu, S. Zhang, Z. Wang, C. Liu, J. Lu, and Y. Tang, “ManiGaussian: Dynamic Gaussian splatting for multi-task robotic manipulation,” in _ECCV_ , 2024. 

- [68] W. Huang, C. Wang, Y. Li, R. Zhang, and L. Fei-Fei, “ReKep: Spatio-temporal reasoning of relational keypoint constraints for robotic manipulation,” in _CoRL_ , 2025. 

- [69] J.-J. Jiang, X.-M. Wu, Y.-X. He, L.-A. Zeng, Y.-L. Wei, D. Zhang, and W.-S. Zheng, “Rethinking bimanual robotic manipulation: Learning with decoupled interaction framework,” in _ICCV_ , 2025. 

- [70] Z. Zheng, J.-F. Cai, X.-M. Wu, Y.-L. Wei, Y.-M. Tang, A. Wu, and W.-S. Zheng, “iManip: Skill-incremental learning for robotic manipulation,” in _ICCV_ , 2025. 

- [71] F. Kuang, J. You, Y. Hu, T. Zhang, C. Wen, and Y. Gao, “Adapt your body: Mitigating proprioception shifts in imitation learning,” _arXiv preprint arXiv:2506.23944_ , 2025. 

- [72] J. Zhou, T. Ma, K.-Y. Lin, Z. Wang, R. Qiu, and J. Liang, “Mitigating the human-robot domain discrepancy in visual pre-training for robotic manipulation,” in _CVPR_ , 2025. 

- [73] J. Zhao, W. Lu, D. Zhang, Y. Liu, Y. Liang, T. Zhang, Y. Cao, J. Xie, Y. Hu, S. Wang _et al._ , “Do you need proprioceptive states in visuomotor policies?” _arXiv preprint arXiv:2509.18644_ , 2025. 

14 

- [74] T. Jiang, J. Ji, X. Tan, J. Fang, A. Bhattad, V. Guizilini, and M. R. Walter, “Do you know where your camera is? view-invariant policy learning with camera conditioning,” _arXiv preprint arXiv:2510.02268_ , 2025. 

- [75] P. Yang, H. Ci, Y. Chen, Q. Lv, H. Cai, and M. Z. Shou, “ActionMap: Robot policy learning via voxel action heatmap,” _arXiv preprint arXiv:2606.06904_ , 2026. 

- [76] M. Janner, Y. Du, J. Tenenbaum, and S. Levine, “Planning with diffusion for flexible behavior synthesis,” in _ICML_ , 2022. 

- [77] P. Wu, A. Escontrela, D. Hafner, P. Abbeel, and K. Goldberg, “DayDreamer: World models for physical robot learning,” in _CoRL_ , 2023. 

- [78] H. Wu, Y. Jing, C. Cheang, G. Chen, J. Xu, X. Li, M. Liu, H. Li, and T. Kong, “Unleashing large-scale video generative pre-training for visual robot manipulation,” in _ICLR_ , 2024. 

- [79] Y. Du, S. Yang, B. Dai, H. Dai, O. Nachum, J. Tenenbaum, D. Schuurmans, and P. Abbeel, “Learning universal policies via text-guided video generation,” in _NeurIPS_ , 2023. 

- [80] C.-L. Cheang, G. Chen, Y. Jing, T. Kong, H. Li, Y. Li, Y. Liu, H. Wu, J. Xu, Y. Yang _et al._ , “GR-2: A generative video-language-action model with web-scale knowledge for robot manipulation,” _arXiv preprint arXiv:2410.06158_ , 2024. 

- [81] Y. Tian, S. Yang, J. Zeng, P. Wang, D. Lin, H. Dong, and J. Pang, “Predictive inverse dynamics models are scalable learners for robotic manipulation,” in _ICLR_ , 2024. 

- [82] S. Li, Y. Gao, D. Sadigh, and S. Song, “Unified video action model,” in _RSS_ , 2025. 

- [83] Y. Ma, Z. Song, Y. Zhuang, J. Hao, and I. King, “A survey on vision-language-action models for embodied AI,” _arXiv preprint arXiv:2405.14093_ , 2024. 

- [84] Physical Intelligence, A. Bo, A. Amin, R. Aniceto, A. Balakrishna, G. Balke, K. Black, G. Bokinsky, S. Cao, T. Charbonnier _et al._ , “ _π_ 0 _._ 7: A Steerable Generalist Robotic Foundation Model with Emergent Capabilities,” _arXiv preprint arXiv:2604.15483_ , 2026. 

- [85] X. R. Team, J. Guo, P. Jin, J. Li, P. Li, Y. Li, F. Liu, W. Peng, O. Qin, Y. Su _et al._ , “Xiaomi-Robotics-1: Scaling vision-languageaction models with over 100K hours of real-world trajectories,” _arXiv preprint arXiv:2607.15330_ , 2026. 

- [86] H. Yuan, Z. Liang, A. Chen, Y. Wang, H. Li, P. Lin, Y. Huang, Z. Lei, T. Zhang, J. Zhang _et al._ , “Qwen-RobotManip technical report: Alignment unlocks scale for robotic manipulation foundation models,” _arXiv preprint arXiv:2606.17846_ , 2026. 

- [87] H. Fang, J. Duan, D. Clay, S. Wang, S. Liu, W. Huang, X. Fan, W.-C. Tsai, S. Chen, Y. R. Wang _et al._ , “MolmoAct2: Action reasoning models for real-world deployment,” _arXiv preprint arXiv:2605.02881_ , 2026. 

- [88] D. Huang, A. Gu, C. Zhang, B. Zou, W. Dong, Z. Cen, Y. Wang, and H. Zhang, “VLAConf: Calibrated task-success confidence for visionlanguage-action models,” _arXiv preprint arXiv:2605.29605_ , 2026. 

- [89] V. Bhat, Y.-H. Lan, P. Krishnamurthy, R. Karri, and F. Khorrami, “3D CAVLA: Leveraging depth and 3D context to generalize vision language action models for unseen tasks,” _arXiv preprint arXiv:2505.05800_ , 2025. 

- [90] J. Zhang, Y. Chen, Y. Xu, Z. Huang, Y. Zhou, Y.-J. Yuan, X. Cai, G. Huang, X. Quan, H. Xu _et al._ , “4D-VLA: Spatiotemporal visionlanguage-action pretraining with cross-scene calibration,” _arXiv preprint arXiv:2506.22242_ , 2025. 

- [91] J. Han, S. Jeon, J. Jung, R. Zurbrugg,¨ H. An, T. Portela, M. Hutter, M. Pollefeys, S. Kim, and S. Hong, “Geometric action model for robot policy learning,” _arXiv preprint arXiv:2606.17046_ , 2026. 

- [92] R. Zheng, Y. Liang, S. Huang, J. Gao, H. Daume´ III, A. Kolobov, F. Huang, and J. Yang, “TraceVLA: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies,” in _ICLR_ , 2025. 

- [93] Q. Zhao, Y. Lu, M. J. Kim, Z. Fu, Z. Zhang, Y. Wu, Z. Li, Q. Ma, S. Han, C. Finn _et al._ , “CoT-VLA: Visual chain-of-thought reasoning for vision-language-action models,” in _CVPR_ , 2025. 

- [94] Q. Lv, W. Kong, H. Li, J. Zeng, Z. Qiu, D. Qu, H. Song, Q. Chen, X. Deng, and J. Pang, “F1: A vision-language-action model bridging understanding and generation to actions,” _arXiv preprint arXiv:2509.06951_ , 2025. 

- [95] Z. Zhong, H. Yan, J. Li, X. Liu, X. Gong, T. Zhang, W. Song, J. Chen, X. Zheng, H. Wang _et al._ , “FlowVLA: Visual chain of thought-based motion reasoning for vision-language-action models,” _arXiv preprint arXiv:2508.18269_ , 2025. 

- [96] H. Liang, X. Chen, B. Wang, M. Chen, Y. Liu, Y. Zhang, Z. Chen, T. Yang, Y. Chen, J. Pang _et al._ , “MM-ACT: Learn from multimodal parallel generation to act,” _arXiv preprint arXiv:2512.00975_ , 2025. 

- [97] J. Lee, J. Duan, H. Fang, Y. Deng, S. Liu, B. Li, B. Fang, J. Zhang, Y. R. Wang, S. Lee _et al._ , “MolmoAct: Action reasoning models that can reason in space,” _arXiv preprint arXiv:2508.07917_ , 2025. 

- [98] J. Cen, S. Huang, Y. Yuan, K. Li, H. Yuan, C. Yu, Y. Jiang, J. Guo, X. Li, H. Luo _et al._ , “RynnVLA-002: A unified vision-language-action and world model,” _arXiv preprint arXiv:2511.17502_ , 2025. 

- [99] Y. Wang, X. Li, W. Wang, J. Zhang, Y. Li, Y. Chen, X. Wang, and Z. Zhang, “Unified vision-language-action model,” _arXiv preprint arXiv:2506.19850_ , 2025. 

- [100] W. Song, Z. Zhou, H. Zhao, J. Chen, P. Ding, H. Yan, Y. Huang, F. Tang, D. Wang, and H. Li, “ReconVLA: Reconstructive vision-language-action model as effective robot perceiver,” in _AAAI_ , 2025. 

- [101] T. Yuan, Z. Dong, Y. Liu, and H. Zhao, “Fast-WAM: Do world action models need test-time future imagination?” _arXiv preprint arXiv:2603.16666_ , 2026. 

- [102] S. Ye, Y. Ge, K. Zheng, S. Gao, S. Yu, G. Kurian, S. Indupuru, Y. L. Tan, C. Zhu, J. Xiang _et al._ , “World action models are zero-shot policies,” _arXiv preprint arXiv:2602.15922_ , 2026. 

- [103] K. Team, F. Wang, S. You, Q. Zhang, T. Huang, Z. Fu, Z. Zheng, Y. Xi, F. Lv, X. Wu _et al._ , “Kairos: A native world model stack for physical AI,” _arXiv preprint arXiv:2606.16533_ , 2026. 

- [104] J. Zhou, Q. Zhang, G. Xu, C. Fan, Y. Zhao, R. Wang, Y. Luo, S. Yang, X. Zhu, Y. Shen _et al._ , “Zero-WAM: In-context world-action modeling from human videos for open-ended task generalization,” _arXiv preprint arXiv:2608.26103_ , 2026. 

- [105] L. Li, Q. Zhang, Y. Luo, S. Yang, R. Wang, F. Han, M. Yu, Z. Gao, N. Xue, X. Zhu _et al._ , “Causal world modeling for robot control,” _arXiv preprint arXiv:2601.21998_ , 2026. 

- [106] Y. Zhang, W. Zhang, Z. Qi, H. Zhang, H. Lin, J. Zhang, Y. Mu, X. Yang, W. Zeng, and X. Jin, “ImageWAM: Do world action models really need video generation, or just image editing?” _arXiv preprint arXiv:2606.19531_ , 2026. 

- [107] Y. Feng, B. Han, J. Lyu, K. Liu, Y. Zheng, Y. Wan, W. Liu, S. Han, R. Li, Y. Zhang _et al._ , “WAM-TTT: Steering world-action models by watching human play at test time,” _arXiv preprint arXiv:2607.06988_ , 2026. 

- [108] Q. Zhang, L. Li, L. Zhang, S. Yang, Y. Luo, S. Li, R. Wang, J. Wang, J. Shao, G. Xu _et al._ , “Native video-action pretraining for generalizable robot control,” _arXiv preprint arXiv:2607.08639_ , 2026. 

- [109] H. Alzayer, W. Huang, H. Chen, C. Luey, L. Zhang, M. Agrawala, G. Wetzstein, L. Fei-Fei, Y. Du, J. Wu _et al._ , “Masked visual actions for unified world modeling,” _arXiv preprint arXiv:2607.19343_ , 2026. 

- [110] Y. Chen, P. Li, Y. Xu, Q. Ma, J. Yang, K. Wang, J. Yang, D. An, H. Guan, G. Liu _et al._ , “FlowWAM: Optical flow as a unified action representation for world action models,” _arXiv preprint arXiv:2607.13017_ , 2026. 

- [111] W. Guo, G. Lu, H. Deng, Z. Wu, Y. Tang, and Z. Wang, “VLA-Reasoner: Empowering vision-language-action models with reasoning via online Monte Carlo tree search,” _arXiv preprint arXiv:2509.22643_ , 2025. 

- [112] Z. Bai, C. Gao, and M. Z. Shou, “EVOLVE-VLA: Test-time training from environment feedback for vision-language-action models,” _arXiv preprint arXiv:2512.14666_ , 2025. 

- [113] S. Tan, K. Dou, Y. Zhao, and P. Kraehenbuehl, “Interactive post-training for vision-language-action models,” in _CVPR_ , 2025. 

- [114] H. Li, Y. Zuo, J. Yu, Y. Zhang, Z. Yang, K. Zhang, X. Zhu, Y. Zhang, T. Chen, G. Cui _et al._ , “SimpleVLA-RL: Scaling VLA training via reinforcement learning,” _arXiv preprint arXiv:2509.09674_ , 2025. 

- [115] S. Fei, S. Wang, L. Ji, A. Li, S. Zhang, L. Liu, J. Hou, J. Gong, X. Zhao, and X. Qiu, “SRPO: Self-referential policy optimization for vision-language-action models,” _arXiv preprint arXiv:2511.15605_ , 2025. 

- [116] Z. Chen, R. Niu, H. Kong, Q. Wang, Q. Xing, and Z. Fan, “TGRPO: Fine-tuning vision-language-action model via trajectory-wise group relative policy optimization,” _arXiv preprint arXiv:2506.08440_ , 2025. 

- [117] C.-P. Huang, Y.-H. Wu, M.-H. Chen, Y.-C. F. Wang, and F.-E. Yang, “ThinkAct: Vision-language-action reasoning via reinforced visual latent planning,” _arXiv preprint arXiv:2507.16815_ , 2025. 

- [118] J. Xiao, Y. Yang, X. Chang, R. Chen, F. Xiong, M. Xu, W.-S. Zheng, and Q. Zhang, “World-Env: Leveraging world model as a virtual environment for VLA post-training,” _arXiv preprint arXiv:2509.24948_ , 2025. 

- [119] L. Xiao, J. Li, J. Gao, F. Ye, Y. Jin, J. Qian, J. Zhang, Y. Wu, and X. Yu, “AVA-VLA: Improving vision-language-action models with active visual attention,” _arXiv preprint arXiv:2511.18960_ , 2025. 

- [120] Z. Zhou, Y. Zhu, M. Zhu, J. Wen, N. Liu, Z. Xu, W. Meng, Y. Peng, C. Shen, F. Feng _et al._ , “ChatVLA: Unified multimodal understanding and robot control with vision-language-action model,” in _EMNLP_ , 2025. 

- [121] S. Wang, W. Yu, X. Chen, X. Tian, J. Zhang, L. Lu, and C. Zhang, “Endto-end listen, look, speak and act,” _arXiv preprint arXiv:2510.16756_ , 2025. 

15 

- [122] S. Kareer, K. Pertsch, J. Darpinian, J. Hoffman, D. Xu, S. Levine, C. Finn, and S. Nair, “Emergence of human to robot transfer in visionlanguage-action models,” _arXiv preprint arXiv:2512.22414_ , 2025. 

- [123] H. Shi, B. Xie, Y. Liu, L. Sun, F. Liu, T. Wang, E. Zhou, H. Fan, X. Zhang, and G. Huang, “MemoryVLA: Perceptual-cognitive memory in vision-language-action models for robotic manipulation,” _arXiv preprint arXiv:2508.19236_ , 2025. 

- [124] Y. Fu, Z. Zhang, Y. Zhang, Z. Wang, Z. Huang, and Y. Luo, “MergeVLA: Cross-skill model merging toward a generalist vision-language-action agent,” _arXiv preprint arXiv:2511.18810_ , 2025. 

- [125] K. Pertsch, K. Stachowicz, B. Ichter, D. Driess, S. Nair, Q. Vuong, O. Mees, C. Finn, and S. Levine, “FAST: Efficient action tokenization for vision-language-action models,” _arXiv preprint arXiv:2501.09747_ , 2025. 

- [126] A. Goyal, H. Hadfield, X. Yang, V. Blukis, and F. Ramos, “VLA-0: Building state-of-the-art VLAs with zero modification,” _arXiv preprint arXiv:2510.13054_ , 2025. 

- [127] J. Zhang, X. Chen, Q. Wang, M. Li, Y. Guo, Y. Hu, J. Zhang, S. Bai, J. Lin, and J. Chen, “VLM4VLA: Revisiting vision-language-models in vision-language-action models,” _arXiv preprint arXiv:2601.03309_ , 2026. 

- [128] J. Zhou, K. Ye, J. Liu, T. Ma, Z. Wang, R. Qiu, K.-Y. Lin, Z. Zhao, and J. Liang, “Exploring the limits of vision-language-action manipulation in cross-task generalization,” in _NeurIPS_ , 2026. 

- [129] M. Yan, W. Zhang, Z. Zhang, Y. Peng, T. Wang, L. Zhai, J. Su, S. Deng, L. Peng, Y. Liu _et al._ , “ZETA: A controlled study of zero-shot crossembodiment VLA transfer for tabletop manipulation,” _arXiv preprint arXiv:2609.02546_ , 2026. 

- [130] C. Fan, G. Liu, M. Hong, R. R. Kompella, and S. Liu, “Rethinking Muon beyond pretraining: Spectral failures and high-pass remedies for VLA and RLVR,” _arXiv preprint arXiv:2605.19282_ , 2026. 

- [131] S. Ye, J. Jang, B. Jeon, S. Joo, J. Yang, B. Peng, A. Mandlekar, R. Tan, Y.-W. Chao, B. Y. Lin _et al._ , “Latent action pretraining from videos,” in _CoRL_ , 2024. 

- [132] H. Bi, H. Tan, S. Xie, Z. Wang, S. Huang, H. Liu, R. Zhao, Y. Feng, C. Xiang, Y. Rong _et al._ , “Motus: A unified latent action world model,” _arXiv preprint arXiv:2512.13030_ , 2025. 

- [133] M. Liu, B. Jia, J. Huang, J. Zhang, and S. Huang, “LARA: Latent action representation alignment for vision-language-action models,” _arXiv preprint arXiv:2606.07100_ , 2026. 

- [134] T. Zhang, M. Lyu, Y. Zhang, F. Fang, and S. Wu, “DiLA: Disentangled latent action world models,” _arXiv preprint arXiv:2605.15725_ , 2026. 

- [135] H. Kim, L. Pinto, and S. J. Kim, “Hierarchical latent action model,” _arXiv preprint arXiv:2603.05815_ , 2026. 

- [136] J. Wen, Y. Zhu, J. Li, M. Zhu, Z. Tang, K. Wu, Z. Xu, N. Liu, R. Cheng, C. Shen _et al._ , “TinyVLA: Towards fast, data-efficient vision-languageaction models for robotic manipulation,” _RAL_ , 2025. 

- [137] H. Li, S. Yang, Y. Chen, X. Chen, X. Yang, Y. Tian, H. Wang, T. Wang, D. Lin, F. Zhao _et al._ , “CronusVLA: Towards efficient and robust manipulation via multi-frame vision-language-action modeling,” _arXiv preprint arXiv:2506.19816_ , 2025. 

- [138] M. Reuss, H. Zhou, M. Ruhle,¨ O. E. Ya<sup>¨</sup> gmurlu, F. Otto, and R. Lioutikov,˘ “FLOWER: Democratizing generalist robot policies with efficient visionlanguage-action flow policies,” _arXiv preprint arXiv:2509.04996_ , 2025. 

- [139] Y. Wang, P. Ding, L. Li, C. Cui, Z. Ge, X. Tong, W. Song, H. Zhao, W. Zhao, P. Hou _et al._ , “VLA-Adapter: An effective paradigm for tinyscale vision-language-action model,” _arXiv preprint arXiv:2509.09372_ , 2025. 

- [140] P. Chen, P. Bu, Y. Wang, X. Wang, Z. Wang, J. Guo, Y. Zhao, Q. Zhu, J. Song, S. Yang _et al._ , “CombatVLA: An efficient vision-languageaction model for combat tasks in 3D action role-playing games,” _arXiv preprint arXiv:2503.09527_ , 2025. 

- [141] J. Bjorck, F. Castaneda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang,˜ D. Fox, F. Hu, S. Huang _et al._ , “GR00T N1: An open foundation model for generalist humanoid robots,” _arXiv preprint arXiv:2503.14734_ , 2025. 

- [142] P. Ding, J. Ma, X. Tong, B. Zou, X. Luo, Y. Fan, T. Wang, H. Lu, P. Mo, J. Liu _et al._ , “Humanoid-VLA: Towards universal humanoid control with visual integration,” _arXiv preprint arXiv:2502.14795_ , 2025. 

- [143] J. Huang, S. Wang, F. Lin, Y. Hu, C. Wen, and Y. Gao, “Tactile-VLA: unlocking vision-language-action model’s physical knowledge for tactile generalization,” _arXiv preprint arXiv:2507.09160_ , 2025. 

- [144] A. Grattafiori, A. Dubey, A. Jauhri, A. Pandey, A. Kadian, A. Al-Dahle, A. Letman, A. Mathur, A. Schelten, A. Vaughan _et al._ , “The Llama 3 herd of models,” _arXiv preprint arXiv:2407.21783_ , 2024. 

- [145] M. Tschannen, A. Gritsenko, X. Wang, M. F. Naeem, I. Alabdulmohsin, N. Parthasarathy, T. Evans, L. Beyer, Y. Xia, B. Mustafa _et al._ , “SigLIP 2: Multilingual vision-language encoders with improved 

semantic understanding, localization, and dense features,” _arXiv preprint arXiv:2502.14786_ , 2025. 

- [146] X. Pan, S. N. Shukla, A. Singh, Z. Zhao, S. K. Mishra, J. Wang, Z. Xu, J. Chen, K. Li, F. Juefei-Xu, J. Hou, and S. Xie, “Transfer between modalities with MetaQueries,” _arXiv preprint arXiv:2504.06256_ , 2025. 

- [147] J. Song, C. Meng, and S. Ermon, “Denoising diffusion implicit models,” in _ICLR_ , 2021. 

- [148] Y. Lipman, R. T. Chen, H. Ben-Hamu, M. Nickel, and M. Le, “Flow matching for generative modeling,” in _ICLR_ , 2021. 

- [149] A. Van Den Oord, O. Vinyals _et al._ , “Neural discrete representation learning,” in _NeurIPS_ , 2017. 

- [150] P. Esser, R. Rombach, and B. Ommer, “Taming transformers for highresolution image synthesis,” in _CVPR_ , 2021. 

- [151] L. Beyer, A. Steiner, A. S. Pinto, A. Kolesnikov, X. Wang, D. Salz, M. Neumann, I. Alabdulmohsin, M. Tschannen, E. Bugliarello _et al._ , “PaliGemma: A versatile 3B VLM for transfer,” _arXiv preprint arXiv:2407.07726_ , 2024. 

- [152] S. Bai, Y. Cai, R. Chen, K. Chen _et al._ , “Qwen3-VL technical report,” _arXiv preprint arXiv:2511.21631_ , 2025. 

- [153] W. Peebles and S. Xie, “Scalable diffusion models with transformers,” in _CVPR_ , 2023. 

- [154] S. Hao, S. Sukhbaatar, D. Su, X. Li, Z. Hu, J. Weston, and Y. Tian, “Training large language models to reason in a continuous latent space,” _arXiv preprint arXiv:2412.06769_ , 2024. 

- [155] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis _et al._ , “DROID: A large-scale in-the-wild robot manipulation dataset,” in _RSS_ , 2024. 

- [156] K. He, X. Chen, S. Xie, Y. Li, P. Dollar,´ and R. Girshick, “Masked autoencoders are scalable vision learners,” in _CVPR_ , 2022. 

- [157] Y. Cui, H. Chen, H. Deng, X. Huang, X. Li, J. Liu, Y. Liu, Z. Luo, J. Wang, W. Wang _et al._ , “Emu3.5: Native multimodal models are world learners,” _arXiv preprint arXiv:2510.26583_ , 2025. 

- [158] T. Zhou, Z. Ma, Q. Wen, X. Wang, L. Sun, and R. Jin, “FEDformer: Frequency enhanced decomposed transformer for long-term series forecasting,” in _ICML_ , 2022. 

- [159] K. Yi, Q. Zhang, W. Fan, S. Wang, P. Wang, H. He, N. An, D. Lian, L. Cao, and Z. Niu, “Frequency-domain MLPs are more effective learners in time series forecasting,” in _NeurIPS_ , 2023. 

- [160] R. Yang, L. Cao, J. YANG _et al._ , “Rethinking Fourier transform from a basis functions perspective for long-term time series forecasting,” in _NeurIPS_ , 2024. 

- [161] H. Wang, L. Pan, Y. Shen, Z. Chen, D. Yang, Y. Yang, S. Zhang, X. Liu, H. Li, and D. Tao, “FreDF: Learning to forecast in the frequency domain,” in _ICLR_ , 2025. 

- [162] N. Ahmed, T. Natarajan, and K. R. Rao, “Discrete cosine transform,” _IEEE Transactions on Computers_ , 1974. 

- [163] M. Reuss, O.<sup>¨</sup> E. Yagmurlu,˘ F. Wenzel, and R. Lioutikov, “Multimodal diffusion transformer: Learning versatile behavior from multimodal goals,” in _RSS_ , 2024. 

- [164] T. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” in _RSS_ , 2023. 

- [165] Q. Garrido, T. Nagarajan, B. Terver, N. Ballas, Y. LeCun, and M. Rabbat, “Learning latent action world models in the wild,” _arXiv preprint arXiv:2601.05230_ , 2026. 

- [166] S. Miao, N. Feng, J. Wu, Y. Lin, X. He, D. Li, and M. Long, “JEPAVLA: Video predictive embedding is needed for VLA models,” _arXiv preprint arXiv:2602.11832_ , 2026. 

- [167] L. Maes, Q. L. Lidec, D. Scieur, Y. LeCun, and R. Balestriero, “LeWorldModel: Stable end-to-end joint-embedding predictive architecture from pixels,” _arXiv preprint arXiv:2603.19312_ , 2026. 

- [168] Qwen Team, “Qwen3.5: Towards native multimodal agents,” Feb. 2026. [Online]. Available: https://qwen.ai/blog?id=qwen3.5 

- [169] D. P. Kingma and M. Welling, “Auto-encoding variational Bayes,” in _ICLR4_ , 2013. 

- [170] A. Bardes, J. Ponce, and Y. Lecun, “VICReg: Variance-invariancecovariance regularization for self-supervised learning,” in _ICLR_ , 2022. 

- [171] O. Simeoni,´ H. V. Vo, M. Seitzer, F. Baldassarre, M. Oquab, C. Jose, V. Khalidov, M. Szafraniec, S. Yi, M. Ramamonjisoa _et al._ , “DINOv3,” _arXiv preprint arXiv:2508.10104_ , 2025. 

- [172] M. Assran, Q. Duval, I. Misra, P. Bojanowski, P. Vincent, M. Rabbat, Y. LeCun, and N. Ballas, “Self-supervised learning from images with a joint-embedding predictive architecture,” in _CVPR_ , 2023. 

- [173] T. Wan, A. Wang, B. Ai, B. Wen, C. Mao, C.-W. Xie, D. Chen, F. Yu, H. Zhao, J. Yang _et al._ , “Wan: Open and advanced large-scale video generative models,” _arXiv preprint arXiv:2503.20314_ , 2025. 

