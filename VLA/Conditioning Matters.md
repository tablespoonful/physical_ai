---
title: "Conditioning Matters: Training Diffusion Policies is Faster Than You Think"
date: "2025-05-16"
authors: "Zibin Dong; Yicheng Liu; Yinchuan Li; Hang Zhao; Jianye Hao"
url: https://arxiv.org/abs/2505.11123
pdf: https://arxiv.org/pdf/2505.11123
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2505.11123)** / [論文ページ](https://arxiv.org/abs/2505.11123)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Conditioning Matters: Training Diffusion Policies is Faster Than You Think** 

**Zibin Dong**<sup>_♡_</sup> **, Yicheng Liu**<sup>_♣_</sup> **, Yinchuan Li**<sup>_♢_</sup> **, Hang Zhao**<sup>_∗♣_</sup> **, Jianye Hao**<sup>_∗♡, ♢_</sup> _♡_ Tianjin University, _♣_ Tsinghua University, _♢_ Huawei Noah’s Ark Lab 

## **Abstract** 

Diffusion policies have emerged as a mainstream paradigm for building visionlanguage-action (VLA) models. Although they demonstrate strong robot control capabilities, their training efficiency remains suboptimal. In this work, we identify a fundamental challenge in conditional diffusion policy training: when generative conditions are hard to distinguish, the training objective degenerates into modeling the marginal action distribution, a phenomenon we term _loss collapse_ . To overcome this, we propose Cocos, a simple yet general solution that modifies the source distribution in the conditional flow matching to be condition-dependent. By anchoring the source distribution around semantics extracted from condition inputs, Cocos encourages stronger condition integration and prevents the loss collapse. We provide theoretical justification and extensive empirical results across simulation and real-world benchmarks. Our method achieves faster convergence and higher success rates than existing approaches, matching the performance of large-scale pre-trained VLAs using significantly fewer gradient steps and parameters. Cocos is lightweight, easy to implement, and compatible with diverse policy architectures, offering a general-purpose improvement to diffusion policy training. 


Figure 1: **Fusing generative condition into the source distribution greatly simplifies diffusion policy training.** Diffusion policy trained with our method achieves _π_ 0 performance on the LIBERO benchmarks with only 30K gradient steps, which is 2.14x faster than the vanilla model. We also show the cosine similarity and the norm scale change between the policy hidden states before and after injecting condition information, demonstrating that our method fundamentally compels the policy network to utilize condition information, rather than simply embedding conditions into the source distribution. 

## **1 Introduction** 

Denoising generative models have emerged as a scalable approach for high-dimensional data generation [28, 6, 26, 17, 18, 12, 30, 16], significantly advancing Vision-Language-Action (VLA) models in robotics (VLAs<sup>2</sup> ) [19, 15, 1, 3, 36, 11]. Mainstream VLA models frame robot control as a conditional generation problem: given vision-language inputs as conditions, the model generates appropriate robot action sequences. Despite action sequences being substantially lower-dimensional than typical generative content like images or text, training VLAs remains unexpectedly challenging and 

> _∗_ Corresponding authors: Hang Zhao (hangzhao@mail.tsinghua.edu.cn), Jianye Hao (jianye.hao@tju.edu.cn). 

> 2Unless otherwise specified, VLAs in this paper refer specifically to denoising generative VLA models. 

Preprint. Under review. 


Figure 2: **Diffusion Policy w/ Cocos.** Our approach requires only replacing the standard Gaussian source distribution with a condition-conditioned Gaussian. An autoencoder compresses condition representations to match dimensionality, providing the mean while maintaining a fixed standard deviation. 

resource-intensive. Recent efforts to enhance VLA training efficiency have explored various directions, including leveraging more powerful vision-language encoders [9, 1, 24, 10, 33, 32], designing compact and expressive action tokenizers [22, 31], and incorporating richer conditioning strategies [7, 8, 35, 14, 23]. These approaches converge on a critical insight: the core challenge may not lie in action generation itself, but rather in how models interpret and utilize conditional inputs. 

To further investigate how condition inputs affect policy training, we empirically compare diffusion policies with visual encoders trained from scratch versus those initialized with DINOv2. We analyze the cosine similarity and norm scale change between policy network hidden states before and after condition information injection, correlating these metrics with LIBERO task success rates Figure 1. Higher cosine similarity and lower norm scale change indicate weaker condition influence on the policy network, directly correlating with degraded performance (as observed comparing DP-DINOv2 versus DP-scratch). The results demonstrate a fundamental issue: policies facing difficult-to-interpret conditions _actively omit conditional inputs_ , producing actions disconnected from observations. This phenomenon persists even when using high-quality representations, though to a lesser degree. 

While empirical results reveal this condition omission phenomenon, we conduct a theoretical analysis to identify its root cause in VLA training. We discover that when policy networks struggle to differentiate between generative conditions, the flow-matching objective degrades into an unconditional one that merely models the marginal action distribution. This loss collapse creates a destructive feedback loop: as the policy network begins ignoring conditional inputs, the training objective further degrades, reinforcing the network’s tendency to discard conditions altogether rather than attempting to interpret them. To prevent this loss collapse, we introduce a novel conditional flow-matching approach with a **co** ndition- **co** nditioned **s** ource distribution ( **Cocos** ). Rather than adopting a standard Gaussian prior _q_ ( _z_ ), Cocos anchors the source distribution around the semantics of each condition _q_ ( _z|c_ ), theoretically preventing training loss collapse and forcing the policy network to remain responsive to condition inputs. As demonstrated in Figure 1, diffusion policies trained with Cocos exhibit 2.14x faster training and substantially higher success rates. Critically, the lower cosine similarity and increased norm scale change indicate that Cocos fundamentally compels the policy network to utilize condition information, rather than simply embedding conditions into the source distribution. 

Specifically, we implement Cocos by formulating the source distribution as a Gaussian with fixed standard deviation, where the mean derives from latent representations produced by a vision-language autoencoder (see Figure 2). This approach introduces minimal architectural overhead, making it compatible with diverse VLA architectures and model scales. This simplicity, combined with strong theoretical guarantees and empirical benefits, positions Cocos as a general-purpose solution for preventing condition omission in VLA training. 

To comprehensively validate Cocos, we conduct extensive evaluations across diverse settings: 70 simulation tasks from the LIBERO and MetaWorld benchmarks [13, 34], 10 real-world tasks on the low-cost open-source SO-100 robot platform [2], and 10 tasks on the high-performance xArm robot platform. Our results demonstrate significant improvements in both manipulation success rates and learning efficiency. Through detailed case studies, we analyze loss collapse manifestations and the mechanisms through which Cocos enhances performance. Our contributions include: 

- We formulate the mathematical framework of flow matching with generative conditions and demonstrate that policy networks omit conditions when they are difficult to distinguish. 

2 

- We introduce **Cocos** , a simple yet effective source distribution modification that prevents loss collapse and significantly improves diffusion policy training efficiency and performance. 

- We establish a comprehensive evaluation benchmark across diverse settings, including simulation tasks from LIBERO and MetaWorld, real-world tasks on a low-cost open-source robot (SO100), and tasks on a high-performance robot (xArm). Our results demonstrate consistent performance improvements across these varied platforms, validating Cocos as a general-purpose, plug-and-play solution for enhancing diffusion policy training. 

## **2 Preliminaries** 

**Problem Formulation.** Our goal is to train a VLA _πθ_ ( _a_ 1: _H |E_ ( _o_ )) that maps an observation _o_ to sequences of future robot actions _a_ 1: _H_ by imitating expert demonstrations. Here, _o_ typically includes current and historical images as well as language instructions, while _E_ represents a pre-trained vision-language encoder. In this paper, we focus on denoising generative model VLAs. 

**Conditional Flow Matching.** Assume a smooth time-varying vector field _u_ : [0 _,_ 1] _×_ R<sup>_d_</sup> _→_ R<sup>_d_</sup> defines an ordinary differential equation (ODE) d _x_ = _ut_ ( _x_ )d _t_ , which pushforward samples from source distribution _p_ 0 to the target distribution _p_ 1. The density transported along _u_ from time 0 to _t_ is denoted as _pt_ : [0 _,_ 1] _×_ R<sup>_d_</sup> _→_ R. _pt_ and _ut_ satisfy the _continuity equation_ : _∂p/∂t_ = _−∇_ ( _pt · ut_ ). Suppose that the marginal probability path _pt_ ( _x_ ) is a mixture of probability paths _pt_ ( _x|z_ ), that is _pt_ ( _x_ ) = � _pt_ ( _x|z_ ) _q_ ( _z_ )d _z_ , where _q_ ( _z_ ) is some distribution over the conditioning variable. If _pt_ ( _x|z_ ) is generated by the vector field _ut_ ( _x|z_ ) from initial conditions _p_ 0( _x|z_ ), then the vector field 


generates the probability path _pt_ ( _x_ ). Let _vθ_ : [0 _,_ 1] _×_ R<sup>_d_</sup> _→_ R<sup>_d_</sup> be a time-dependent vector field parameterized as a neural network _θ_ . Define the conditional flow matching (CFM) objective: 


In VLA models, a typical choice sets _q_ ( _z_ ) = _q_ ( _x_ 0) _q_ ( _x_ 1), corresponding to an independent coupling of the source and target distributions, and the conditional flow is defined by 


where the source distribution is a standard Gaussian. By optimizing CFM objective, _vθ_ ( _t, x_ ) can converge to the vector field _ut_ ( _x_ ), with which we can solve the ODE and sample action chunks. _Note that this is a general formulation covering a wide range of denoising generative models, e.g., Var. Exploding [27], Var. Preserving [6] diffusion models, flow matching models [12], rectified flow models [16], etc. So our following discussion can be easily transferred to various policy backbones._ 

## **3 How Generative Conditions Can Lead to Loss Collapse** 

While conditional flow matching offers a general framework for transporting probability distributions, it does not inherently consider condition inputs. Prior works adopt a straightforward strategy: injecting the generative condition directly into the policy network [4, 37, 38]. However, the implications of this approach have received little theoretical attention. In this section, we first analyze how the underlying flow formulation changes when generative conditions are introduced, then demonstrate that this seemingly benign modification can lead to a critical failure mode: loss collapse, where the training objective degenerates and the model learns to omit the generative condition altogether. 

### **3.1 Flow with Generative Conditions** 

We consider a conditional vector field _ut_ ( _x|c_ ) that transports the source distribution _p_ 0( _x|c_ ) to the target _p_ 1( _x|c_ ), where _c_ is the generative condition. Let _pt_ ( _x|z, c_ ) denote the time-varying intermediate density under generation condition _c_ and flow condition _z_ , with its associated vector field _ut_ ( _x|z, c_ ). Then, the overall conditional velocity can be expressed as: 


3 


Figure 3: **Loss collapse causes the policy to degrade to an average.** The policy omits language instructions (‘Move it to the left’ or ‘Move it to the right’) and yields actions based on their frequency in the training data. Cocos prevents loss collapse, enabling the policy to produce distinct actions corresponding to ‘Left’ and ‘Right’. 

Suppose we introduce _c_ into the neural estimator _vθ_ ( _t, x, c_ ) of the conditional velocity _ut_ ( _x|c_ ). The corresponding training objective becomes: 


**Lemma 1.** _If pt_ ( _x|c_ ) _>_ 0 _for all x ∈_ R<sup>_d_</sup> _and t ∈_ [0 _,_ 1] _, up to a constant independent of θ, objective_ E _t,pt_ ( _x|c_ ) _∥vθ_ ( _t, x, c_ ) _− ut_ ( _x|c_ ) _∥_<sup>2</sup> _and_ E _t,q_ ( _z_ ) _,pt_ ( _x|z,c_ ) _∥vθ_ ( _t, x, c_ ) _− ut_ ( _x|z, c_ ) _∥_<sup>2</sup> _are equal._ 

By optimizing Equation (5), we can use _vθ_ ( _t, x, c_ ) to estimate _ut_ ( _x|c_ ) and solve the ODE for generation. In practice, a common formulation of _q_ ( _z_ ) in Equation (5) is _q_ ( _z_ ) = _q_ ( _x_ 0) _q_ ( _x_ 1 _, c_ ) _, z_ = ( _x_ 1 _, x_ 0 _, c_ ). This setup corresponds to sampling a condition-action pair from the dataset and perturbing the action with Gaussian noise during training. Under this formulation, the conditional flow and velocity field are defined by: 


This reduces the objective to that implemented in previous works [4, 37, 38]: 


### **3.2 Loss Collapse** 

While this conditional objective encourages the model to learn condition-dependent vector fields, a critical failure mode can occur: if the model fails to distinguish the condition information in _C_ (e.g., for any _c_ 1 _, c_ 2 _∈C_ , _∥vθ_ ( _t, x, c_ 1) _− vθ_ ( _t, x, c_ 2) _∥≤ ϵ_ ), the objective effectively collapses into a marginal form on _C_ that no longer depends on _c_ . 

**Theorem 1** (Gradient Contraction under Independent Sampling) **.** _Under the independent sampling measure_ 


_the difference of the score gradients for any two conditions c_ 1 _, c_ 2 _∈C admits the bound_ 


_provided that ∥∇θvθ∥≤ M , ∥d∥≤ D, and the model output satisfies ∥vθ_ ( _t, x, c_ 1) _−vθ_ ( _t, x, c_ 2) _∥≤ ϵ with its gradient being output-sensitive Lipschitz of constant K. The velocity estimator vθ_ ( _t, x, c_ ) _tends to converge to a c-independent function v_<sup>_∗_</sup> ( _t, x_ ) _that minimizes the averaged objective:_ 


_By contrast, when samples are drawn from the conditional measure_ 


_the same gradient difference can become arbitrarily large unless additional coupling assumptions on q_ ( _x_ 0 _|c_ ) _are imposed._ 

4 

This result reveals a vicious cycle: as the policy network becomes confused by condition inputs, the objective degenerates into an unconditional one. This further reinforces the network’s tendency to discard difficult-to-interpret conditions, leading to models that appear to be well-trained but fail to comprehend conditional cues during deployment. As shown in Figure 3, loss collapse causes the policy to average actions. In the next section, we introduce Cocos, a simple method to prevent it. 

## **4 Method** 

In Theorem 1, we identify that loss collapse arises when _c_ becomes indistinguishable to the policy network. This collapse is exacerbated by the standard choice of sampling _z_ from _q_ ( _z_ ) = _q_ ( _x_ 1 _, c_ ) _q_ ( _x_ 0), which decouples _x_ 0 from the condition. If _vθ_ ( _t, x, c_ ) _≈ vθ_ ( _t, x_ ), the expectation in the objective effectively marginalizes over _c_ , causing it to degenerate into an unconditional one. 

To prevent it, we propose a simple yet effective modification: using a **co** ndition- **co** nditioned **s** ource distribution ( **Cocos** ) by sampling _z_ from _q_ ( _z_ ) = _q_ ( _x_ 1 _, c_ ) _q_ ( _x_ 0 _|c_ ). As shown in Theorem 1, this change directly avoids the loss collapse and enforces condition-awareness during training. While _q_ ( _x_ 0 _|c_ ) can be designed in various ways, in this work, we choose to maintain the overall framework’s simplicity by setting it as a Gaussian with fixed standard deviation, with the following objective: 

_L_ Cocos( _θ_ ) := E _t,q_ ( _x_ 0 _|c_ ) _,q_ ( _x_ 1 _,c_ ) _,pt ∥vθ − ut∥_<sup>2</sup> _,_ where _q_ ( _x_ 0 _|c_ ) = _N_ ( _x_ 0; _αFϕ_ ( _E_ ( _c_ )) _, β_<sup>2</sup> _I_ ) _,_ (8) where _Fϕ_ is a feature encoder that maps the condition representations to the action space dimensionality. The scalar _α_ controls the strength of the condition prior, and _β_ adjusts the uncertainty. Setting _α_ = 0 _, β_ = 1 recovers the commonly used formulation with a standard Gaussian prior. Incorporating Cocos requires only replacing the standard Gaussian source distribution with a condition-conditioned one. Algorithm 1 clearly shows the differences in training and inference pipelines. 

In practice, we adopt an autoencoding objective on condition embeddings to train _Fϕ_ . Specifically, we minimize the negative cosine similarity between the original and reconstructed embeddings: 


where _Fϕ_ and _Gϕ_ are the encoder and decoder networks, respectively. As a default setting, we adopt a two-stage training process: we first train the source distribution (i.e., the autoencoder) and then fix it during policy training. However, in practical scenarios, this two-step pipeline may introduce additional inflexibility. To address this, we also explore a joint training alternative. Simultaneous training of this autoencoder and the policy can be unstable due to the evolving distribution of _x_ 0. To mitigate this, we adopt an Exponential Moving Average (EMA) strategy. We maintain a target network _Fϕ−_ , updated via EMA from _Fϕ_ , and use this EMA copy during policy training, ensuring stability. In practice, this approach achieves performance comparable to the two-stage strategy, which we will discuss in detail in the experimental section. 

We implement our policy network using a compact Robot Diffusion Transformer (RDT) [15]. The diffusion process follows a linear interpolation schedule [12]: 

_pt_ ( _x|x_ 1 _, x_ 0) = _N_ ( _x_ ; _tx_ 1 + (1 _− t_ ) _x_ 0 _, σ_<sup>2</sup> ) _, ut_ ( _x|x_ 1 _, x_ 0) = _x_ 1 _− x_ 0 _._ (10) 

We select these design choices as they have been widely adopted in advanced VLA models [15, 1]. 

**Algorithm 1** Training and Inference Pseudocode for Diffusion Policy with Cocos 

**Require:** Policy Network _vθ_ , Condition Network _E_ , Pre-trained condition encoder _Fϕ_ 

1: **while** not coverge **do** `# Training` 

- 2: ( _x_ 1 _, c_ ) _∼ q_ ( _x_ 1 _, c_ ) _, t ∼U_ (0 _,_ 1) _, x_ 0 _∼ q_ ( _x_ 0 _|c_ ) Equation (8) # _x_ 0 _∼N_ (0 _, I_ ) `(without Cocos)` 3: _θ ← θ_ + _∇θL_ CFMc( _θ_ ) Equation (7) 

- 4: **end while** 

- 5: **while** not done **do** `# Inference` 

- 6: Observe _c, x_ 0 _∼ q_ ( _x_ 0 _|c_ ) Equation (8) # _x_ 0 _∼N_ (0 _, I_ ) `(without Cocos)` 

- 7: Solve ODE d _xt_ = _vθ_ ( _t, xt, c_ )d _t_ from _t_ = 0 to _t_ = 1. 

- 8: _a ← x_ 1; Execute action _a_ 

- 9: **end while** 

## **5 Experiments** 

We conduct comprehensive experiments to evaluate the effectiveness of Cocos in both simulated and real-world robot manipulation tasks. The experiments are designed to answer three core questions: 

5 


Figure 4: **Learning curve on LIBERO benchmark.** Dashed line scores are reported by Kim et al. [10]. 

Table 1: **Success rate on LIBERO benchmark.** Each of the four task suites includes 10 tasks, and we evaluate 150 trials for each task. The 1<sup>st</sup> , 2<sup>nd</sup> highest scores are emphasized with bold and the 3<sup>rd</sup> with underline. Cocos (0.2 std) is our default configuration, and other Cocos variants serve for an ablation study. 

|||DP-scratch|DP-DINOv2|Cocos(0.2 std)|Cocos (0.1 std)|Cocos (0.4 std)|Cocos (VAE)|Cocos (EMA)|
|---|---|---|---|---|---|---|---|---|
||Goal|64.3±1.3|82.9±0.4|**93.8±0.3**|50.9±1.8|92.3±0.9|**92.5±0.3**|90.5±0.4|
|LIBERO|Spatial|76.1±1.6|91.4±0.7|**97.5±0.7**|97.1±0.4|96.7±0.5|96.1±0.7|**97.5±0.2**|
||Object|71.4±0.7|88.9±1.0|**99.1±0.6**|79.3±0.8|97.6±1.0|**98.1±0.7**|96.9±0.5|
||Long|45.9±1.6|82.7±0.2|**88.7±0.1**|82.7±0.5|**89.5±0.4**|88.2±0.6|87.3±0.6|
|Aver|age|64.4|86.5|**94.8**|77.5|**94.0**|93.8|93.0|


**(RQ1)** Does Cocos improve diffusion policies’ training efficiency and final performance? 

**(RQ2)** Does it mitigate the loss collapse phenomenon? 

**(RQ3)** Does it facilitate policy learning in real-world settings across heterogeneous robot platforms? 

### **5.1 Experimental Setup** 

**Diffusion Policy.** Our diffusion policy (DP) adopts a compact RDT policy network of approximately 40M parameters. The vision-language condition inputs are encoded using a DINOv2-Base [20] and a T5-Base [25]. We denote the resulting model as DP-DINOv2. To evaluate the effectiveness of Cocos, we compare three key variants: (1) DP-scratch, which is trained without any pre-trained vision encoder; (2) DP-DINOv2, which incorporates frozen DINOv2 features but uses the standard source distribution; and (3) DP-DINOv2 with Cocos, our full method with a condition-conditioned source distribution. The autoencoder used to define the source distribution in Cocos is implemented using a single-layer Transformer for both encoder and decoder components. 

**Benchmarks.** Our simulation evaluations are based on the LIBERO and MetaWorld benchmarks. LIBERO includes 40 tasks in four task suites: _Goal_ , _Spatial_ , _Object_ , and _Long_ , to test different policy generalizations. MetaWorld includes 30 tasks from various difficulty levels. For real-world experiments, we deploy the models on two robot platforms: The SO100 robot (low-cost, open-sourced, equipped with dual RGB cameras) evaluated on 10 tasks in four suites: _Pick&Place_ , _MoveTo_ , _Wipe_ , and _Unfold_ ; The xArm robot (higher-precision, equipped with one Intel RealSense L515 LiDAR camera) evaluated on 10 tasks in suites: _Pick&Place_ , _Pot_ , _Pour_ , and _Moka_ . We show detailed task configurations in Appendix B. 

### **5.2 Overall Comparison (RQ1)** 

We evaluate the effectiveness of Cocos on two widely-used simulation benchmarks: LIBERO and MetaWorld. For LIBERO, we also include comparisons with fine-tuned _π_ 0 [1], OpenVLA-OFT [10], and Seer [29]. _π_ 0 and OpenVLA-OFT are SOTA large-scale pre-trained VLA models, featuring flow-matching and next-token prediction, respectively. Seer is not an end-to-end VLA model but predicts future frames to infer actions. We report the results in Table 1, Table 2 and Figure 4. 

**_Finding 1:_ Cocos significantly improves training efficiency and policy performance.** Across all LIBERO suites, Diffusion policy (DP) trained with Cocos outperforms its counterparts without Cocos. Notably, Cocos-enabled models reach high success rates (e.g., >95% on _Spatial_ and _Object_ suites) within only 5–10K training steps, achieving convergence roughly **2.14x** faster than DP-DINOv2. On average, Cocos improves LIBERO success rates by **8.3%** . Across all MetaWorld tasks, it also outperforms the counterpart by **25.7%** gain, showing consistent performance gains. 

6 

Table 2: **Success rate on MetaWorld benchmark.** We evaluate 150 trials for each task. The highest scores are emphasized in bold. We take a multi-task setting, using language instructions to differentiate each task. 


Figure 5: **Evaluation results on SO100 and xArm platforms.** We collect 4 task suites or 10 tasks for each robot platform. Each task provides 20 demonstrations and is tested over 10 trials. 

**_Finding 2:_ Cocos enables compact models to rival large-scale pre-trained VLAs.** Despite using fewer parameters and fewer gradient steps, DP with Cocos performs comparably to large-scale models like _π_ 0 and OpenVLA-OFT. As described in Kim et al. [10], while OpenVLA-OFT takes 50-150K gradient steps for fine-tuning and _π_ 0 takes 100-250K steps, our model reaches similar performance within 30K steps. On the challenging _Long_ suite, Cocos even outperforms Seer, a non-end-to-end model with a larger parameter count. These results demonstrate that proper condition integration, rather than model scale alone, can be a major driver of performance in VLA training. 

**_Finding 3:_ Cocos encourages deeper condition utilization rather than just injecting priors.** To understand the nature of the improvement, we examine internal representations of the policy network before and after condition injection (Figure 1). Specifically, we measure cosine similarity and norm scale changes of hidden states (see Appendix C for details). A lower similarity and a higher norm shift reflect greater responsiveness to conditioning inputs. As shown in Figure 1, these metrics are consistently aligned with higher task success rates. This suggests that the benefit of Cocos does not stem merely from injecting condition priors into the source distribution. Instead, it actively compels the policy network to differentiate between and respond to condition inputs. If the gains were due only to initialization, we would expect weaker condition dependence, contrary to what we observe. 

### **5.3 Real-World Experiments (RQ2)** 

To assess the practicality of our approach, we deploy diffusion policies trained with and without Cocos on two real-world robotic platforms: **SO100** , a low-cost and open-source arm, and **xArm** , a widely used high-precision industrial robot. The two platforms offer complementary insights: SO100 lowers the entry barrier for research and reproducibility, while xArm reflects deployment scenarios with more demanding task complexity and control fidelity. 

As shown in Figure 5 and Figure 6, Cocos consistently improves task success rates across all task suites on both robots. The improvement is particularly pronounced on SO100, where the relatively lightweight structure makes it more sensitive to inaccuracies in action generation. We observe that both policy variants, with and without Cocos, are capable of generating smooth and coherent trajectories. However, the main failure modes of the baseline model are closely linked to misinterpretation of condition inputs, for example, confusing spatial references in language, or failing to correctly localize an object in the visual scene. In contrast, these types of errors are reduced when using Cocos, indicating improved condition understanding and robustness. These trends align with our theoretical motivation: condition misalignment during training can lead to loss collapse and unreliable behavior at inference time. The fact that Cocos provides consistent improvements across two distinct robotic platforms further highlights its practical value. In the next section, we present detailed case studies to examine these qualitative differences in greater depth. 

7 


Figure 6: **Rollout samples of DP with Cocos on real-robot manipulation,** including _MoveTo (Bowl)_ (Top Left), _Wipe_ (Top Right), _Moka_ (Bottom Left), and _Pour_ (Bottom Right). 


Figure 7: **Real robot case study.** Top left rollout comes from policy w/ Cocos and the others are from baselines. 

### **5.4 Case Studies (RQ3)** 

To better understand the mechanisms behind Cocos’s effectiveness, we conduct qualitative case studies on both simulation and real-world tasks, focusing on common failure patterns and condition sensitivity. 

**_Finding 1:_ Cocos improves utilization of 3rd-person visual inputs in simulation.** In the LIBERO benchmark, we find that policies trained without Cocos tend to omit 3rd-person views, relying almost exclusively on the wrist-mounted 1st-person camera. To quantify this, we compute cosine similarity between randomly sampled visual features extracted before fusion into the policy network. As shown in Figure 8 bottom table, models without Cocos produce highly similar 3rd-person embeddings across diverse scenes, indicating weak discriminability, while Cocos-trained models show significantly greater variation, suggesting stronger visual grounding. 

This contrast is clearly illustrated through the rollout comparisons in Figure 8. (Row 1) shows a successful execution by the model trained with Cocos: the robot pushes the plate forward, turns smoothly to the left, and finally pushes the plate backward to the stove, demonstrating accurate spatial reasoning and multi-step planning. This trajectory serves as a reference for the expected behavior. In (Row 2), a failure case from the model without Cocos, the robot accidentally releases the plate mid-way and attempts to recover by locating it again. However, since the plate is no longer visible in the 1st-person view, the policy fails to re-establish contact, even though the 3rd-person view clearly shows the plate’s new location. This indicates that the model underutilizes the auxiliary camera input. (Row 3) presents a similar failure condition, but the plate remains within the first-person field of view after being released. In this case, the robot successfully relocates and completes the task. Comparing Row 2 and Row 3 highlights the model’s strong reliance on the 1st-person view: if the object leaves that view, recovery becomes unlikely. (Row 4) shows another typical failure from the non-Cocos model: after reaching the stove, the robot continues to push the plate beyond the goal region. This happens because the 1st-person view offers no clear signal indicating proximity to the stove, while the 3rd-person view does. Again, the model fails to leverage this available information. Taken together, these cases reveal a consistent pattern: policies trained without Cocos tend to over-rely on the wrist-mounted camera and struggle to utilize 3rd-person observations. In contrast, models trained with Cocos seldom exhibit these failures, suggesting that the policy network learns to better incorporate multi-view context and is more robust to visual uncertainty. 

**_Finding 2:_ Cocos reduces modality over-reliance and improves contextual awareness in realworld settings.** In real-robot experiments, we observe that models without Cocos frequently exhibit modality over-reliance, particularly favoring language instructions or arm states over visual cues. As shown in Figure 7, when tasks begin in an already-completed configuration (e.g., lid already open), the baseline policy often executes a full rollout regardless of the visual scene (left bottom). This indicates 

8 

that the model has learned to follow the instruction without verifying whether it is still applicable. By contrast, policy trained with Cocos correctly remains idle in such states, indicating improved contextual awareness (left top). Similar trends appear in other tasks such as _SpongeMoveRight_ (right top) and _ScissorMoveRight_ (right bottom), where the baseline struggles to locate target objects or misinterprets spatial references. These errors are less frequent with Cocos, which appears to enhance the policy’s sensitivity to both visual and semantic nuances in the scene. Together, these case studies provide concrete support for our theoretical claims: Cocos prevents loss collapse not just in training metrics, but in how models behave under ambiguous or weakly conditioned scenarios. 

### **5.5 Ablation Studies** 

Cocos only requires the source distribution to be condition-dependent, i.e., _q_ ( _z|c_ ), and admits flexibility in its concrete form. For simplicity, we instantiate it as a Gaussian with fixed standard deviation and a condition-dependent mean (Equation (8)). Our default setting uses _β_ = 0 _._ 2, and we compare it against _β_ = 0 _._ 1 and _β_ = 0 _._ 4 to investigate the impact of the standard deviation. Inspired by the similarity between our formulation and the variational autoencoder (VAE) posterior, we evaluate a VAE-based version of Cocos, where the standard deviation is automatically learned from data. As shown in Table 1, we observe that the default ( _β_ = 0 _._ 2) and the wider variant ( _β_ = 0 _._ 4), and the VAE version all achieve comparable performance across LIBERO task suites. However, the model with _β_ = 0 _._ 1 performs substantially worse, suggesting that overly concentrated _q_ ( _z|c_ ) hinders training. Overall, these results indicate that Cocos is robust to the choice of _β_ , as long as _q_ ( _z|c_ ) remains sufficiently spread. 

We also compare the default two-stage training approach, where the source distribution is pretrained and then fixed, with a joint training strategy using exponential moving average (EMA) Figure 8: **Case study of LIBERO plate movement.** updates. In this version, a slowly updated target encoder _Fϕ−_ is used during policy training to provide stable condition-dependent sampling. This online approach achieves performance on par with the two-stage method while simplifying the pipeline, making it a practical choice for integrated training scenarios. 

## **6 Conclusion, Limitations, and Future Works** 

In this paper, we identify and address a critical failure mode in diffusion policy training, loss collapse, where the model fails to distinguish between generative conditions and degenerates into modeling marginal action distributions. We propose Cocos, a simple yet effective modification that injects condition-awareness directly into the source distribution. We provide a theoretical analysis showing how Cocos prevents loss collapse and demonstrate its empirical benefits across extensive simulations and real-world tasks. Our results show that Cocos improves both training efficiency and policy performance, enabling even compact models to match or exceed the performance of large-scale pretrained VLA systems. Despite its effectiveness, Cocos leaves open several important directions. First, while the method only requires the source distribution to be condition-dependent ( _q_ ( _z|c_ )), we have so far instantiated it using a fixed-variance Gaussian derived from autoencoding the condition. Exploring more expressive or learnable source distributions, such as flow-based or attention-guided priors, may further enhance its adaptability. Second, our current experiments are focused on multi-task imitation learning. Extending Cocos to large-scale pretraining and evaluating its ability to generalize across broad VLA domains remains a promising area for future work. 

9 

## **References** 

- [1] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A visionlanguage-action flow model for general robot control. In _arXiv preprint arXiv:2410.24164_ , 2024. 

- [2] Remi Cadene, Simon Alibert, Alexander Soare, Quentin Gallouedec, Adil Zouitine, and Thomas Wolf. Lerobot: State-of-the-art machine learning for real-world robotics in pytorch. `https: //github.com/huggingface/lerobot` , 2024. 

- [3] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. In _Proceedings of Robotics: Science and Systems, RSS_ , 2023. 

- [4] Eugenio Chisari, Nick Heppert, Max Argus, Tim Welschehold, Thomas Brox, and Abhinav Valada. Learning robotic manipulation policies from point clouds with conditional flow matching. In _8th Annual Conference on Robot Learning, CoRL_ , 2024. 

- [5] Zibin Dong, Yifu Yuan, Jianye HAO, Fei Ni, Yi Ma, Pengyi Li, and YAN ZHENG. Cleandiffuser: An easy-to-use modularized library for diffusion models in decision making. In _The Thirty-eight Conference on Neural Information Processing Systems Datasets and Benchmarks Track, NIPS_ , 2024. 

- [6] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. In _Advances in Neural Information Processing Systems, NIPS_ , 2020. 

- [7] Wenlong Huang, Chen Wang, Yunzhu Li, Ruohan Zhang, and Li Fei-Fei. Rekep: Spatiotemporal reasoning of relational keypoint constraints for robotic manipulation. In _8th Annual Conference on Robot Learning, CoRL_ , 2024. 

- [8] Yuanchen Ju, Kaizhe Hu, Guowei Zhang, Gu Zhang, Mingrun Jiang, and Huazhe Xu. Roboabc: Affordance generalization beyond categories via semantic correspondence for robot manipulation. In _European Conference on Computer Vision, ECCV_ , 2025. 

- [9] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P Foster, Pannag R Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. OpenVLA: An open-source vision-language-action model. In _8th Annual Conference on Robot Learning, CoRL_ , 2024. 

- [10] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. In _arXiv preprint arXiv:2502.19645_ , 2025. 

- [11] Yinchuan Li, Xinyu Shao, Jianping Zhang, Haozhi Wang, Leo Maxime Brunswic, Kaiwen Zhou, Jiqian Dong, Kaiyang Guo, Xiu Li, Zhitang Chen, Jun Wang, and Jianye Hao. Generative models in decision making: A survey. In _arXiv preprint arXiv:2502.17100_ , 2025. 

- [12] Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matthew Le. Flow matching for generative modeling. In _The Eleventh International Conference on Learning Representations, ICLR_ , 2023. 

- [13] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, qiang liu, Yuke Zhu, and Peter Stone. LIBERO: Benchmarking knowledge transfer for lifelong robot learning. In _Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track, NIPS_ , 2023. 

- [14] Jiaming Liu, Hao Chen, Pengju An, Zhuoyang Liu, Renrui Zhang, Chenyang Gu, Xiaoqi Li, Ziyu Guo, Sixiang Chen, Mengzhen Liu, Chengkai Hou, Mengdi Zhao, KC alex Zhou, PhengAnn Heng, and Shanghang Zhang. Hybridvla: Collaborative diffusion and autoregression in a unified vision-language-action model. In _arXiv preprint arXiv:2503.10631_ , 2025. 

10 

- [15] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. RDT-1b: a diffusion foundation model for bimanual manipulation. In _The Thirteenth International Conference on Learning Representations, ICLR_ , 2025. 

- [16] Xingchao Liu, Chengyue Gong, and qiang liu. Flow straight and fast: Learning to generate and transfer data with rectified flow. In _The Eleventh International Conference on Learning Representations, ICLR_ , 2023. 

- [17] Cheng Lu, Yuhao Zhou, Fan Bao, Jianfei Chen, Chongxuan Li, and Jun Zhu. DPM-solver: A fast ODE solver for diffusion probabilistic model sampling in around 10 steps. In _Advances in Neural Information Processing Systems, NIPS_ , 2022. 

- [18] Cheng Lu, Yuhao Zhou, Fan Bao, Jianfei Chen, Chongxuan Li, and Jun Zhu. Dpmsolver++: Fast solver for guided sampling of diffusion probabilistic models. In _arXiv preprint arXiv:2211.01095_ , 2022. 

- [19] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You Liang Tan, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In _Proceedings of Robotics: Science and Systems, RSS_ , 2024. 

- [20] Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy V. Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel HAZIZA, Francisco Massa, Alaaeldin El-Nouby, Mido Assran, Nicolas Ballas, Wojciech Galuba, Russell Howes, Po-Yao Huang, Shang-Wen Li, Ishan Misra, Michael Rabbat, Vasu Sharma, Gabriel Synnaeve, Hu Xu, Herve Jegou, Julien Mairal, Patrick Labatut, Armand Joulin, and Piotr Bojanowski. DINOv2: Learning robust visual features without supervision. _Transactions on Machine Learning Research, TMLR_ , 2024. 

- [21] William Peebles and Saining Xie. Scalable diffusion models with transformers. _arXiv preprint arXiv:2212.09748_ , 2022. 

- [22] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models. In _arXiv preprint arXiv:2501.09747_ , 2025. 

- [23] Zekun Qi, Wenyao Zhang, Yufei Ding, Runpei Dong, Xinqiang Yu, Jingwen Li, Lingyun Xu, Baoyu Li, Xialin He, Guofan Fan, Jiazhao Zhang, Jiawei He, Jiayuan Gu, Xin Jin, Kaisheng Ma, Zhizheng Zhang, He Wang, and Li Yi. Sofar: Language-grounded orientation bridges spatial reasoning and object manipulation. In _arXiv preprint arXiv:2503.10631_ , 2025. 

- [24] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, and Xuelong Li. Spatialvla: Exploring spatial representations for visual-language-action model. In _arXiv preprint arXiv:2501.15830_ , 2025. 

- [25] Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J. Liu. Exploring the limits of transfer learning with a unified text-to-text transformer. _Journal of Machine Learning Research, JMLR_ , 2020. 

- [26] Jiaming Song, Chenlin Meng, and Stefano Ermon. Denoising diffusion implicit models. In _International Conference on Learning Representations, ICLR_ , 2021. 

- [27] Yang Song and Stefano Ermon. Generative modeling by estimating gradients of the data distribution. In _arXiv preprint arXiv:1907.05600_ , 2020. 

- [28] Yang Song, Jascha Sohl-Dickstein, Diederik P Kingma, Abhishek Kumar, Stefano Ermon, and Ben Poole. Score-based generative modeling through stochastic differential equations. In _International Conference on Learning Representations, ICLR_ , 2021. 

- [29] Yang Tian, Sizhe Yang, Jia Zeng, Ping Wang, Dahua Lin, Hao Dong, and Jiangmiao Pang. Predictive inverse dynamics models are scalable learners for robotic manipulation. In _The Thirteenth International Conference on Learning Representations, ICLR_ , 2025. 

11 

- [30] Alexander Tong, Kilian FATRAS, Nikolay Malkin, Guillaume Huguet, Yanlei Zhang, Jarrid Rector-Brooks, Guy Wolf, and Yoshua Bengio. Improving and generalizing flow-based generative models with minibatch optimal transport. _Transactions on Machine Learning Research, TMLR_ , 2024. 

- [31] Zihao Wang, Shaofei Cai, Zhancun Mu, Haowei Lin, Ceyao Zhang, Xuejie Liu, Qing Li, Anji Liu, Xiaojian Ma, and Yitao Liang. OmniJARVIS: Unified vision-language-action tokenization enables open-world instruction following agents. In _The Thirty-eighth Annual Conference on Neural Information Processing Systems, NIPS_ , 2024. 

- [32] Junjie Wen, Minjie Zhu, Yichen Zhu, Zhibin Tang, Jinming Li, Zhongyi Zhou, Chengmeng Li, Xiaoyu Liu, Yaxin Peng, Chaomin Shen, and Feifei Feng. Diffusion-vla: Scaling robot foundation models via unified diffusion and autoregression. In _arXiv preprint arXiv:2412.03293_ , 2024. 

- [33] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, Yaxin Peng, et al. Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation. In _IEEE Robotics and Automation Letters, RAL_ , 2025. 

- [34] Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Karol Hausman, Chelsea Finn, and Sergey Levine. Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on Robot Learning, CoRL_ , 2019. 

- [35] Wentao Yuan, Jiafei Duan, Valts Blukis, Wilbert Pumacay, Ranjay Krishna, Adithyavairavan Murali, Arsalan Mousavian, and Dieter Fox. Robopoint: A vision-language model for spatial affordance prediction in robotics. In _Proceedings of The 8th Conference on Robot Learning, CoRL_ , 2025. 

- [36] Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations. In _Proceedings of Robotics: Science and Systems, RSS_ , 2024. 

- [37] Fan Zhang and Michael Gienger. Affordance-based robot manipulation with flow matching. In _arXiv preprint arXiv:2409.01083_ , 2025. 

- [38] Qinglun Zhang, Zhen Liu, Haoqiang Fan, Guanghui Liu, Bing Zeng, and Shuaicheng Liu. Flowpolicy: Enabling fast and robust 3d flow-based policy via consistency flow matching for robot manipulation. In _arXiv preprint arXiv:2412.04987_ , 2024. 

12 

## **A Proofs of Theorems** 

_Proof of Lemma 1._ As in Tong et al. [30] we assume that _q, pt_ ( _x|z_ ) are decreasing to zero at sufficient speed as _∥x∥→∞_ and that _ut, vt, ∇θvt_ are bounded. 


By bilinearity of the 2-norm and since _ut_ is independent of _θ_ . Next, 


Finally, 


Since the gradients of the two objectives are equal for any time _t_ , the two objectives are equal. 

_Proof of Theorem 1._ Define 


where we write _y_ = ( _x_ 0 _, x_ 1 _, x_ ). Introduce two measures: 

- _Independent measure_ 


which does _not_ depend on the particular choice of _c_ , corresponding to the design choice where _q_ ( _z_ ) = _q_ ( _x_ 1 _, c_ ) _q_ ( _x_ 0). 

- _Conditional measure_ 


which _does_ depend on _c_ , corresponding to the design choice where _q_ ( _z_ ) = _q_ ( _x_ 1 _, c_ ) _q_ ( _x_ 0 _|c_ ). 

13 

We assume the following bounds hold for all _y_ and _c ∈C_ : 


and that the model’s gradient is _output-sensitive Lipschitz_ , namely there exists _K >_ 0 such that 


**(i) Independent measure.** Under _µ_ , the gradient is 


Hence for any _c_ 1 _, c_ 2: 


Expanding the integrand, 


Using the bounds _∥d_ ( _c_ 1) _− d_ ( _c_ 2) _∥≤ ϵ_ and _∥∇θv_ ( _c_ 1) _−∇θv_ ( _c_ 2) _∥≤ Kϵ_ , we obtain 


The above bound shows that when all _c ∈C_ induce similar gradients, the network update over this region becomes nearly invariant to _c_ . In the limit of gradient descent, the parameter _θ_ thus evolves according to a shared direction, regardless of the exact _c_ value. As a result, the learned model _vθ_ ( _t, x, c_ ) tends to converge, for all _c ∈C_ , to a _c_ -independent function _v_<sup>_∗_</sup> ( _t, x_ ) that minimizes the averaged objective: 


That is, the network effectively collapses the conditional dependency on _c_ and behaves like a shared estimator _v_<sup>_∗_</sup> optimized for average performance across _C_ . 

**(ii) Conditional measure.** Under _µc_ , the gradient becomes 


For _c_ 1 _, c_ 2, write 


14 

The second term _T_ 2 coincides with the independent-measure analysis and thus is bounded by 2( _M_ + _KD_ ) _ϵ_ . The first term 


is the difference of the same function under two _different_ measures. Without any further assumption on the relationship between _µc_ 1 and _µc_ 2 , this difference can be made arbitrarily large. For instance, if _q_ ( _x_ 0 _|c_ 1) = _δa_ and _q_ ( _x_ 0 _|c_ 2) = _δb_ , then _∥T_ 1 _∥_ = 2 _|f_ ( _a, c_ 1) _− f_ ( _b, c_ 1) _|_ can diverge independently of _ϵ_ . Hence, under the conditional measure _µc_ , no bound depending only on _ϵ_ exists for _∥∇θL_ ( _θ, c_ 1) _− ∇θL_ ( _θ, c_ 2) _∥_ . 

## **B Details of Benchmarks** 


Figure 9: **LIBERO simulation benchmark.** We conduct experiments on 40 tasks from four task suites in the LIBERO benchmark. We show two task examples for each suite here. 


Figure 10: **MetaWorld simulation benchmark.** We conduct experiments on 30 tasks of three difficulty levels in the MetaWorld benchmark. We show all task examples here. 


Figure 11: **Real-world experimental setups.** We conduct experiments on both SO100 and xArm platform. For each robot, we design a suite of 10 tabletop tasks involving diverse objects. 

**LIBERO.** The LIBERO simulation benchmark [13] features a Franka Emika Panda arm in simulation across four challenging task suites: _Goal_ , _Spatial_ , _Object_ , and _Long_ . Each suite comprises 10 tasks with 500 demonstrations and is designed to investigate controlled knowledge transfer related to goal variations, spatial configurations, object types, and long-horizon tasks. Unlike prior work [9, 10], we do not filter out unsuccessful demonstrations, aiming for a more realistic evaluation setting. For policy training, the model predicts action chunks of length 16; after each chunk prediction, 8 steps are executed before generating the next chunk. The observation space includes 2-view RGB images at the current time step, without historical observations. During evaluation, following Liu et al. [13], each task is tested over 50 trials with 3 different random seeds, and success rates are reported. To 

15 

provide a clearer understanding of the task suites, we present agent-view observations in Figure 9 and detailed task descriptions in Table 3. 

**MetaWorld.** The MetaWorld simulation benchmark [34] includes 50 distinct tabletop manipulation tasks using a Sawyer robot arm. We select 30 tasks from _easy_ , _medium_ , and _very hard_ difficulty levels to evaluate VLA models. We use a scripted policy to collect 20 demonstrations for each task. For policy training, the model predicts action chunks of length 16; after each chunk prediction, 16 steps are executed before generating the next chunk. The observation space consists of a single RGB image at the current time step, without historical observations. During evaluation, each task is tested over 50 trials with 3 different random seeds, and success rates are reported. To better illustrate the task suites, we show agent-view observations in Figure 10 and task descriptions in Table 4. 

**SO100 Robot Manipulation.** The SO100 robot [2] is a low-cost, open-source 6-DoF manipulator, with both the leader and follower arms costing approximately $250. We assemble the hardware using a 3D-printed kit provided by the open-source community. The robot has two RGB cameras: one mounted on the wrist and the other positioned to provide a third-person view. Both cameras operate at a resolution of 640×480 and 25 FPS. The robot controller runs at 30Hz, and actions are defined as target absolute joint angles. Due to its low-cost design, the platform has several hardware limitations, including significant arm jitter, low load capacity, and occasional camera lag, which present practical challenges for developing embodied AI systems. However, given the increasing adoption of such affordable open-source robots by the research community, we believe that evaluating models on these lower-performance systems offers valuable insights and broader applicability. We design four categories of tabletop manipulation tasks for the SO100 setup: **_(1) Pick&Place:_** involving 3 objects and 2 placement zones (6 tasks), **_(2) MoveTo:_** navigating 2 objects to a single target zone (2 tasks), **_(3) Wipe:_** picking up a cloth and wiping the table (1 task), and **_(4) Unfold:_** unfolding a cloth (1 task). In total, we evaluate performance on 10 distinct tasks. Language instructions for each task are listed in Table 5, and visual examples of the task environments are shown in Figure 11. 

During data collection, we record 20 demonstrations per task. For policy training, the model predicts an action chunk of length 64; after each chunk prediction, 40 steps are executed before generating the next chunk. The observation space includes 2-view RGB images at the current time step, along with the absolute joint angles from the current and previous 10 steps. During evaluation, each task is tested over 10 trials, and success rates are reported. 

**xArm Robot Manipulation.** xArm is a high-performance 7-DoF manipulator. The robot is equipped with a third-person view Intel RealSense L515 LiDAR camera, operating at 640 _×_ 480 resolution and 30 FPS. We collect both RGB and depth images from the camera. The robot controller runs at 30Hz, and actions are defined as target absolute joint angles. We design four categories of tabletop manipulation tasks for the xArm setup: **_(1) Pick&Place:_** involving 3 objects and 2 placement zones (6 tasks), **_(2) Pot:_** taking off or putting on the pot lid (2 tasks), **_(3) Pour:_** pouring water from the kettle into the cup (1 task), and **_(4) Moka:_** placing the Moka pot on the cooker (1 task). In total, we evaluate performance on 10 distinct tasks. Language instructions for each task are listed in Table 5, and visual examples of task environments are shown in Figure 11. 

During data collection, we record 20 demonstrations per task. For policy training, the model predicts an action chunk of length 64; after each chunk prediction, 40 steps are executed before generating the next chunk. The observation space includes a third-person view RGB image at the current time step, as well as the absolute joint angles from the current and previous 10 steps. During evaluation, each task is tested over 10 trials, and success rates are reported. 

## **C Details of Evaluation Metrics** 

**Cosine similarity.** To quantify the influence of condition inputs on our policy network, we measure the cosine similarity between hidden states before and after condition injection. Given an _L_ -layer RDT policy network where conditions are integrated via cross-attention in each transformer block, we denote the hidden states before and after condition injection as _h_<sup>_l_</sup> _, h_<sup>¯</sup><sup>_l_</sup> _∈_ R<sup>_S×D_</sup> , where _S_ is the sequence length and _D_ is the transformer hidden dimension. Since earlier layers’ transformations propagate through the network, affecting all subsequent computations, we calculate an exponentially weighted sum:<sup>�</sup><sup>_L_</sup> _l_ =0<sup>_−_1</sup><sup>_wl_min</sup><sup>_S{_Sim(</sup><sup>_hl,_¯</sup><sup>_hl_)</sup><sup>_}_, where min</sup><sup>_S_operates across the sequence dimension,</sup> Sim computes cosine similarity across the hidden dimension, and _w_ = 0 _._ 5 gives greater weight to 

16 

Table 3: Task description of each task in the LIBERO benchmark. 

|Task Suite<br>LIBERO-Goal|Task Description<br>open the middle layer of the drawer<br>put the bowl on the stove<br>put the wine bottle on the top of the drawer<br>open the top layer of the drawer and put the bowl inside<br>put the bowl on the top of the drawer<br>push the plate to the front of the stove<br>put the cream cheese on the bowl<br>turn on the stove<br>put the bowl on the plate<br>put the wine bottle on the rack|
|---|---|
|LIBERO-Spatial|pick the akita black bowl between the plate and the ramekin and place it on the plate<br>pick the akita black bowl next to the ramekin and place it on the plate<br>pick the akita black bowl from table center and place it on the plate<br>pick the akita black bowl on the cookies box and place it on the plate<br>pick the akita black bowl in the top layer of the wooden cabinet and place it on the plate<br>pick the akita black bowl on the ramekin and place it on the plate<br>pick the akita black bowl next to the cookies box and place it on the plate<br>pick the akita black bowl on the stove and place it on the plate<br>pick the akita black bowl next to the plate and place it on the plate<br>pick the akita black bowl on the wooden cabinet and place it on the plate|
|LIBERO-Object|pick the alphabet soup and place it in the basket<br>pick the cream cheese and place it in the basket<br>pick the salad dressing and place it in the basket<br>pick the bbq sauce and place it in the basket<br>pick the ketchup and place it in the basket<br>pick the tomato sauce and place it in the basket<br>pick the butter and place it in the basket<br>pick the milk and place it in the basket<br>pick the chocolate pudding and place it in the basket<br>pick the orange juice and place it in the basket|
|LIBERO-Long|put both the alphabet soup and the tomato sauce in the basket<br>put both the cream cheese box and the butter in the basket<br>turn on the stove and put the moka pot on it<br>put the black bowl in the bottom drawer of the cabinet and close it<br>put the white mug on the left plate and put the yellow and white mug on the right plate<br>pick up the book and place it in the back compartment of the caddy<br>put the white mug on the plate and put the chocolate pudding to the right of the plate<br>put both the alphabet soup and the cream cheese box in the basket<br>put both moka pots on the stove<br>put the yellow and white mug in the microwave and close it|


earlier layers. Lower similarity values indicate stronger condition influence on network representations. 

**Norm scale change.** Similarly, we quantify the magnitude of change induced by conditional inputs using an exponentially weighted sum of relative norm changes:<sup>�</sup><sup>_L_</sup> _l_ =0<sup>_−_1</sup><sup>_wl_max</sup><sup>_S_</sup> ��� _<u>∥h</u>_ ¯ _l∥∥h−_<sup>_l_</sup> _<u>∥∥hl∥</u>_ ���, where 

max _S_ operates across the sequence dimension, _∥· ∥_ computes the norm across the hidden dimension, and _w_ = 0 _._ 5. Larger values indicate that conditional information substantially alters the magnitude of hidden representations, suggesting stronger condition integration within the policy network. 

**Cosine similarity in case study.** In Figure 8, we also calculate a cosine similarity metric to quantify the degree to which the policy network differentiates between conditions. This cosine similarity is computed between visual features _before_ they are fused into the policy network (i.e., after the vision encoder’s output has been processed by positional encoding and an MLP, yielding the features ultimately used for fusion with the policy network). We calculate this metric by randomly sampling image pairs from the dataset and then averaging the cosine similarity of their corresponding features. 

17 

Table 4: Task description of each task in the MetaWorld benchmark. 

|**Task Name**|**Task Description**|
|---|---|
|basketball|Dunk the basketball into the basket.|
|bin-picking<br>button-press<br>|Grasp the puck from one bin and place it into another bin.<br>Press a button.<br>|
|button-press-topdown|Press a button from the top.|
|button-press-topdown-wall|Bypass a wall and press a button from the top.|
|button-press-wall<br>coffee-button<br>coffee-pull|Bypass a wall and press a button.<br>Push a button on the coffee machine.<br>Pull a mug from a coffee machine.|
|coffee-push|Push a mug under a coffee machine.|
|dial-turn|Rotate a dial 180 degrees.|
|disassemble|Pick a nut out of the peg.|
|door-lock|Lock the door by rotating the lock clockwise.|
|door-open|Open a door with a revolving joint.|
|door-unlock|Unlock the door by rotating the lock counter-clockwise.|
|drawer-close|Push and close a drawer.|
|drawer-open|Open a drawer.|
|faucet-close|Rotate the faucet clockwise.|
|faucet-open|Rotate the faucet counter-clockwise.|
|hammer|Hammer a screw on the wall.|
|handle-press|Press a handle down.|
|handle-press-side|Press a handle down sideways.|
|handle-pull|Pull a handle up.|
|handle-pull-side|Pull a handle up sideways.|
|shelf-place|Pick and place a puck onto a shelf.|
|soccer|Kick a soccer into the goal.|
|stick-push<br>sweep|Grasp a stick and push a box using the stick.<br>Sweep a puck off the table.|
|sweep-into|Sweep a puck into a hole.|
|window-close|Push and close a window.|
|window-open|Push and open a window.|


Table 5: **Task description of each task in the SO100 and xArm benchmark.** As each parameter combination introduces one task, each task suite has 10 tasks in total. For each task, we test the model for 10 trials. 

|Task Suite|Task Description|Parameter|
|---|---|---|
|SO100|pick`[A]`and place it on the`[B]`side of the table<br>move`[A]`to the center of the table<br>pick the cloth and wipe the table<br>unfold the cloth|`[A]: ["screwdriver", "sponge", "charger"]`,`[B]: ["left", "right"]`<br>`[A]: ["cup", "bowl"]`<br>`None`<br>`None`|
|xArm|pick`[A]`and place it on the`[B]`side of the table<br>open the pot lid`or`put the lid on the pot<br>pour the water from the kettle into the cup<br>place the Moka pot on the cooker|`[A]: ["scissor", "plier", "tap"]`,`[B]: ["left", "right"]`<br>`[open, close]`<br>`None`<br>`None`|


## **D Policy Backbone Recipe** 

### **D.1 Condition Network** 

For vision encoding, we utilize the pre-trained DINOv2-Base model, and for language encoding, we employ the pre-trained T5-Base model. Both of these encoders are frozen during training. The outputs from these pre-trained modality encoders are processed by a linear projector and then augmented with positional encodings before being fused into the policy network. These positional encodings are trainable but are initialized with sin-cos positional encoding and scaled down by a factor of 0.2. 

### **D.2 Policy Network** 

We employ a compact Robot Diffusion Transformer (RDT) architecture, which is fundamentally a Diffusion Transformer incorporating cross-attention layers. Diffusion timestamps and robot kinematic information are integrated into the policy network using AdaLN-Zero [21]. The vision and language embeddings are used as the Keys and Values in the cross-attention layers to be integrated into the policy network alternately [15]. The Transformer architecture has a hidden dimension of 384, with 6 attention heads, and 12 layers. 

18 

### **D.3 Diffusion Model** 

We use a flow matching model defined by Equation (10). Diffusion timestamps are treated as continuous values within the range [0 _,_ 1]; we do not discretize them. Instead, they are represented using a Fourier embedding with a scale of 0.2 [5]. During training, diffusion timestamps are sampled from a uniform distribution over the interval [0 _,_ 1]. For inference, we solve the corresponding ODE using the Euler method, dividing the interval [0 _,_ 1] into equal-sized steps. 

### **D.4 Computation Resources** 

All policy training and testing are conducted on a server equipped with 4 NVIDIA GeForce RTX 4090 GPUs and an Intel(R) Xeon(R) CPU E5-2678 v3 @ 2.50GHz. 

19 

## **NeurIPS Paper Checklist** 

1. **Claims** 

Question: Do the main claims made in the abstract and introduction accurately reflect the paper’s contributions and scope? 

Answer: [Yes] 

Justification: The main claims made in the abstract and introduction accurately reflect the paper’s contributions and scope. 

Guidelines: 

   - The answer NA means that the abstract and introduction do not include the claims made in the paper. 

   - The abstract and/or introduction should clearly state the claims made, including the contributions made in the paper and important assumptions and limitations. A No or NA answer to this question will not be perceived well by the reviewers. 

   - The claims made should match theoretical and experimental results, and reflect how much the results can be expected to generalize to other settings. 

   - It is fine to include aspirational goals as motivation as long as it is clear that these goals are not attained by the paper. 

2. **Limitations** 

Question: Does the paper discuss the limitations of the work performed by the authors? Answer: [Yes] 

Justification: We have discussed the limitations of the work in Section 6. 

Guidelines: 

   - The answer NA means that the paper has no limitation while the answer No means that the paper has limitations, but those are not discussed in the paper. 

   - The authors are encouraged to create a separate "Limitations" section in their paper. 

   - The paper should point out any strong assumptions and how robust the results are to violations of these assumptions (e.g., independence assumptions, noiseless settings, model well-specification, asymptotic approximations only holding locally). The authors should reflect on how these assumptions might be violated in practice and what the implications would be. 

   - The authors should reflect on the scope of the claims made, e.g., if the approach was only tested on a few datasets or with a few runs. In general, empirical results often depend on implicit assumptions, which should be articulated. 

   - The authors should reflect on the factors that influence the performance of the approach. For example, a facial recognition algorithm may perform poorly when image resolution is low or images are taken in low lighting. Or a speech-to-text system might not be used reliably to provide closed captions for online lectures because it fails to handle technical jargon. 

   - The authors should discuss the computational efficiency of the proposed algorithms and how they scale with dataset size. 

   - If applicable, the authors should discuss possible limitations of their approach to address problems of privacy and fairness. 

   - While the authors might fear that complete honesty about limitations might be used by reviewers as grounds for rejection, a worse outcome might be that reviewers discover limitations that aren’t acknowledged in the paper. The authors should use their best judgment and recognize that individual actions in favor of transparency play an important role in developing norms that preserve the integrity of the community. Reviewers will be specifically instructed to not penalize honesty concerning limitations. 

3. **Theory assumptions and proofs** 

Question: For each theoretical result, does the paper provide the full set of assumptions and a complete (and correct) proof? 

Answer: [Yes] 

20 

Justification: We provide the full set of assumptions and a complete proof for each theoretical result. 

Guidelines: 

   - The answer NA means that the paper does not include theoretical results. 

   - All the theorems, formulas, and proofs in the paper should be numbered and crossreferenced. 

   - All assumptions should be clearly stated or referenced in the statement of any theorems. 

   - The proofs can either appear in the main paper or the supplemental material, but if they appear in the supplemental material, the authors are encouraged to provide a short proof sketch to provide intuition. 

   - Inversely, any informal proof provided in the core of the paper should be complemented by formal proofs provided in appendix or supplemental material. 

   - Theorems and Lemmas that the proof relies upon should be properly referenced. 

4. **Experimental result reproducibility** 

Question: Does the paper fully disclose all the information needed to reproduce the main experimental results of the paper to the extent that it affects the main claims and/or conclusions of the paper (regardless of whether the code and data are provided or not)? 

Answer: [Yes] 

Justification: We provide every detail to reproduce the main experimental results. Guidelines: 

   - The answer NA means that the paper does not include experiments. 

   - If the paper includes experiments, a No answer to this question will not be perceived well by the reviewers: Making the paper reproducible is important, regardless of whether the code and data are provided or not. 

   - If the contribution is a dataset and/or model, the authors should describe the steps taken to make their results reproducible or verifiable. 

   - Depending on the contribution, reproducibility can be accomplished in various ways. For example, if the contribution is a novel architecture, describing the architecture fully might suffice, or if the contribution is a specific model and empirical evaluation, it may be necessary to either make it possible for others to replicate the model with the same dataset, or provide access to the model. In general. releasing code and data is often one good way to accomplish this, but reproducibility can also be provided via detailed instructions for how to replicate the results, access to a hosted model (e.g., in the case of a large language model), releasing of a model checkpoint, or other means that are appropriate to the research performed. 

   - While NeurIPS does not require releasing code, the conference does require all submissions to provide some reasonable avenue for reproducibility, which may depend on the nature of the contribution. For example 

   - (a) If the contribution is primarily a new algorithm, the paper should make it clear how to reproduce that algorithm. 

   - (b) If the contribution is primarily a new model architecture, the paper should describe the architecture clearly and fully. 

   - (c) If the contribution is a new model (e.g., a large language model), then there should either be a way to access this model for reproducing the results or a way to reproduce the model (e.g., with an open-source dataset or instructions for how to construct the dataset). 

   - (d) We recognize that reproducibility may be tricky in some cases, in which case authors are welcome to describe the particular way they provide for reproducibility. In the case of closed-source models, it may be that access to the model is limited in some way (e.g., to registered users), but it should be possible for other researchers to have some path to reproducing or verifying the results. 

5. **Open access to data and code** 

Question: Does the paper provide open access to the data and code, with sufficient instructions to faithfully reproduce the main experimental results, as described in supplemental material? 

21 

Answer: [Yes] 

Justification: We will open-source the code in a few days after submission. Guidelines: 

   - The answer NA means that paper does not include experiments requiring code. 

   - Please see the NeurIPS code and data submission guidelines ( `https://nips.cc/ public/guides/CodeSubmissionPolicy` ) for more details. 

   - While we encourage the release of code and data, we understand that this might not be possible, so “No” is an acceptable answer. Papers cannot be rejected simply for not including code, unless this is central to the contribution (e.g., for a new open-source benchmark). 

   - The instructions should contain the exact command and environment needed to run to reproduce the results. See the NeurIPS code and data submission guidelines ( `https: //nips.cc/public/guides/CodeSubmissionPolicy` ) for more details. 

   - The authors should provide instructions on data access and preparation, including how to access the raw data, preprocessed data, intermediate data, and generated data, etc. 

   - The authors should provide scripts to reproduce all experimental results for the new proposed method and baselines. If only a subset of experiments are reproducible, they should state which ones are omitted from the script and why. 

   - At submission time, to preserve anonymity, the authors should release anonymized versions (if applicable). 

   - Providing as much information as possible in supplemental material (appended to the paper) is recommended, but including URLs to data and code is permitted. 

6. **Experimental setting/details** 

Question: Does the paper specify all the training and test details (e.g., data splits, hyperparameters, how they were chosen, type of optimizer, etc.) necessary to understand the results? 

Answer: [Yes] 

Justification: We provide every detail in training and testing. 

Guidelines: 

- The answer NA means that the paper does not include experiments. 

- The experimental setting should be presented in the core of the paper to a level of detail that is necessary to appreciate the results and make sense of them. 

- The full details can be provided either with the code, in appendix, or as supplemental material. 

### 7. **Experiment statistical significance** 

Question: Does the paper report error bars suitably and correctly defined or other appropriate information about the statistical significance of the experiments? 

Answer: [Yes] 

Justification: Yes. We report error bars in the learning curve. 

Guidelines: 

- The answer NA means that the paper does not include experiments. 

- The authors should answer "Yes" if the results are accompanied by error bars, confidence intervals, or statistical significance tests, at least for the experiments that support the main claims of the paper. 

- The factors of variability that the error bars are capturing should be clearly stated (for example, train/test split, initialization, random drawing of some parameter, or overall run with given experimental conditions). 

- The method for calculating the error bars should be explained (closed form formula, call to a library function, bootstrap, etc.) 

- The assumptions made should be given (e.g., Normally distributed errors). 

- It should be clear whether the error bar is the standard deviation or the standard error of the mean. 

22 

   - It is OK to report 1-sigma error bars, but one should state it. The authors should preferably report a 2-sigma error bar than state that they have a 96% CI, if the hypothesis of Normality of errors is not verified. 

   - For asymmetric distributions, the authors should be careful not to show in tables or figures symmetric error bars that would yield results that are out of range (e.g. negative error rates). 

   - If error bars are reported in tables or plots, The authors should explain in the text how they were calculated and reference the corresponding figures or tables in the text. 

8. **Experiments compute resources** 

Question: For each experiment, does the paper provide sufficient information on the computer resources (type of compute workers, memory, time of execution) needed to reproduce the experiments? 

Answer: [Yes] 

Justification: Yes. We list the GPU and CPU resources. 

Guidelines: 

- The answer NA means that the paper does not include experiments. 

- The paper should indicate the type of compute workers CPU or GPU, internal cluster, or cloud provider, including relevant memory and storage. 

- The paper should provide the amount of compute required for each of the individual experimental runs as well as estimate the total compute. 

- The paper should disclose whether the full research project required more compute than the experiments reported in the paper (e.g., preliminary or failed experiments that didn’t make it into the paper). 

### 9. **Code of ethics** 

Question: Does the research conducted in the paper conform, in every respect, with the NeurIPS Code of Ethics `https://neurips.cc/public/EthicsGuidelines` ? 

Answer: [Yes] 

Justification: Yes, we do. 

Guidelines: 

- The answer NA means that the authors have not reviewed the NeurIPS Code of Ethics. 

- If the authors answer No, they should explain the special circumstances that require a deviation from the Code of Ethics. 

- The authors should make sure to preserve anonymity (e.g., if there is a special consideration due to laws or regulations in their jurisdiction). 

### 10. **Broader impacts** 

Question: Does the paper discuss both potential positive societal impacts and negative societal impacts of the work performed? 

Answer: [Yes] 

Justification: Yes, we do. 

Guidelines: 

- The answer NA means that there is no societal impact of the work performed. 

- If the authors answer NA or No, they should explain why their work has no societal impact or why the paper does not address societal impact. 

- Examples of negative societal impacts include potential malicious or unintended uses (e.g., disinformation, generating fake profiles, surveillance), fairness considerations (e.g., deployment of technologies that could make decisions that unfairly impact specific groups), privacy considerations, and security considerations. 

- The conference expects that many papers will be foundational research and not tied to particular applications, let alone deployments. However, if there is a direct path to any negative applications, the authors should point it out. For example, it is legitimate to point out that an improvement in the quality of generative models could be used to 

23 

generate deepfakes for disinformation. On the other hand, it is not needed to point out that a generic algorithm for optimizing neural networks could enable people to train models that generate Deepfakes faster. 

- The authors should consider possible harms that could arise when the technology is being used as intended and functioning correctly, harms that could arise when the technology is being used as intended but gives incorrect results, and harms following from (intentional or unintentional) misuse of the technology. 

- If there are negative societal impacts, the authors could also discuss possible mitigation strategies (e.g., gated release of models, providing defenses in addition to attacks, mechanisms for monitoring misuse, mechanisms to monitor how a system learns from feedback over time, improving the efficiency and accessibility of ML). 

### 11. **Safeguards** 

Question: Does the paper describe safeguards that have been put in place for responsible release of data or models that have a high risk for misuse (e.g., pretrained language models, image generators, or scraped datasets)? 

Answer: [NA] 

Justification: The paper poses no such risks. 

Guidelines: 

   - The answer NA means that the paper poses no such risks. 

   - Released models that have a high risk for misuse or dual-use should be released with necessary safeguards to allow for controlled use of the model, for example by requiring that users adhere to usage guidelines or restrictions to access the model or implementing safety filters. 

   - Datasets that have been scraped from the Internet could pose safety risks. The authors should describe how they avoided releasing unsafe images. 

   - We recognize that providing effective safeguards is challenging, and many papers do not require this, but we encourage authors to take this into account and make a best faith effort. 

12. **Licenses for existing assets** 

Question: Are the creators or original owners of assets (e.g., code, data, models), used in the paper, properly credited and are the license and terms of use explicitly mentioned and properly respected? 

Answer: [Yes] 

Justification: Yes, they are. 

Guidelines: 

- The answer NA means that the paper does not use existing assets. 

- The authors should cite the original paper that produced the code package or dataset. 

- The authors should state which version of the asset is used and, if possible, include a URL. 

- The name of the license (e.g., CC-BY 4.0) should be included for each asset. 

- For scraped data from a particular source (e.g., website), the copyright and terms of service of that source should be provided. 

- If assets are released, the license, copyright information, and terms of use in the package should be provided. For popular datasets, `paperswithcode.com/datasets` has curated licenses for some datasets. Their licensing guide can help determine the license of a dataset. 

- For existing datasets that are re-packaged, both the original license and the license of the derived asset (if it has changed) should be provided. 

- If this information is not available online, the authors are encouraged to reach out to the asset’s creators. 

### 13. **New assets** 

Question: Are new assets introduced in the paper well documented and is the documentation provided alongside the assets? 

24 

### Answer: [Yes] 

Justification: Yes. 

Guidelines: 

   - The answer NA means that the paper does not release new assets. 

   - Researchers should communicate the details of the dataset/code/model as part of their submissions via structured templates. This includes details about training, license, limitations, etc. 

   - The paper should discuss whether and how consent was obtained from people whose asset is used. 

   - At submission time, remember to anonymize your assets (if applicable). You can either create an anonymized URL or include an anonymized zip file. 

14. **Crowdsourcing and research with human subjects** 

Question: For crowdsourcing experiments and research with human subjects, does the paper include the full text of instructions given to participants and screenshots, if applicable, as well as details about compensation (if any)? 

Answer: [NA] 

Justification: We do not include crowdsourcing experiments or research with human subjects. Guidelines: 

   - The answer NA means that the paper does not involve crowdsourcing nor research with human subjects. 

   - Including this information in the supplemental material is fine, but if the main contribution of the paper involves human subjects, then as much detail as possible should be included in the main paper. 

   - According to the NeurIPS Code of Ethics, workers involved in data collection, curation, or other labor should be paid at least the minimum wage in the country of the data collector. 

15. **Institutional review board (IRB) approvals or equivalent for research with human** 

### **subjects** 

Question: Does the paper describe potential risks incurred by study participants, whether such risks were disclosed to the subjects, and whether Institutional Review Board (IRB) approvals (or an equivalent approval/review based on the requirements of your country or institution) were obtained? 

Answer: [NA] 

Justification: We do not include crowdsourcing experiments or research with human subjects. Guidelines: 

   - The answer NA means that the paper does not involve crowdsourcing nor research with human subjects. 

   - Depending on the country in which research is conducted, IRB approval (or equivalent) may be required for any human subjects research. If you obtained IRB approval, you should clearly state this in the paper. 

   - We recognize that the procedures for this may vary significantly between institutions and locations, and we expect authors to adhere to the NeurIPS Code of Ethics and the guidelines for their institution. 

   - For initial submissions, do not include any information that would break anonymity (if applicable), such as the institution conducting the review. 

16. **Declaration of LLM usage** 

Question: Does the paper describe the usage of LLMs if it is an important, original, or non-standard component of the core methods in this research? Note that if the LLM is used only for writing, editing, or formatting purposes and does not impact the core methodology, scientific rigorousness, or originality of the research, declaration is not required. 

Answer: [NA] 

25 

Justification: The core method development in this research does not involve LLMs. Guidelines: 

- The answer NA means that the core method development in this research does not involve LLMs as any important, original, or non-standard components. 

- Please refer to our LLM policy ( `https://neurips.cc/Conferences/2025/LLM` ) for what should or should not be described. 

26 

