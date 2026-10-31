---
title: "World-Action Models for Robot Learning and Control: A Survey"
date: "2026-09-13"
authors: "Zuxing Lu; Hongjia Zhai; Guanzhi Wang; Huajian Zeng; Jiaqi Yang; Jingyu Liu"
url: https://arxiv.org/abs/2609.16074
pdf: https://arxiv.org/pdf/2609.16074
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2609.16074)** / [論文ページ](https://arxiv.org/abs/2609.16074)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

1 

# World-Action Models for Robot Learning and Control: A Survey 

Zuxing Lu<sup>1</sup><sup>_,∗_</sup> , Hongjia Zhai<sup>1</sup><sup>_,∗_</sup> , Guanzhi Wang<sup>2</sup> , Huajian Zeng<sup>1</sup> , Jiaqi Yang<sup>1</sup> , Jingyu Liu<sup>1</sup> , Lei Cheng<sup>1</sup> , Yuantai Zhang<sup>1</sup> , Yuheng Qiu<sup>3</sup> , Zezhou Cheng<sup>4</sup> , Ivan Laptev<sup>1</sup> , Danfei Xu<sup>5</sup> , Benjamin Riviere<sup>6</sup> , Giuseppe Loianno<sup>7</sup> , Eric Xing<sup>1</sup> , Xingxing Zuo<sup>1</sup><sup>_,†_</sup> 


Fig. 1: **Evolution of World-Action Models.** The timeline summarizes representative milestones from latent world-model reinforcement learning and foundation vision-language-action models to video-action models, and recent unified World-Action Models. It highlights how predictive modeling and action generation have gradually converged toward integrated frameworks for embodied robot control. 

**_Abstract_ —Robots operating in open environments act under partial observability, physical constraints, and dynamic task contexts. Beyond mapping observations and language instructions to actions, they must anticipate how candidate actions may affect future states and task-relevant outcomes. Recent advances in world models, video generation, and Vision-Language-Action (VLA) policies have motivated the development of World-Action Models (WAMs), which couple future world prediction with executable action generation. This survey provides a roboticsoriented review of WAMs. We clarify their scope relative to conventional world models, model-based reinforcement learning, action-conditioned video generation, and reactive VLA policies, and organize existing methods through a unified taxonomy covering representations, transition modeling, action interfaces, architectures, training pipelines, data modalities, and scaling strategies. We further review applications of WAMs in manipulation, navigation, and autonomous driving, and we summarize the datasets, benchmarks, metrics, and protocols used to evaluate WAM systems. Finally, we discuss key challenges in action alignment, world-action factorization, spatial and multi-view consistency, long-horizon memory, neural simulation for closedloop policy learning, and efficient inference. Taken together, this survey aims to provide a concise technical foundation for integrating predictive world modeling with action generation, toward more reliable embodied robot intelligence. Project page: https://rcl-robotics.github.io/Awesome-World-Action-Models.** 

**_Index Terms_ —World Model, World-Action Model, Predictive Control, Vision-Language-Action, Manipulation, Navigation** 

## I. INTRODUCTION 

**R** OBOTShorizon, deployedmultimodal,in openand instruction-drivenenvironments executestasks underlongpartial observability and physical constraints. Unlike static perception systems, an embodied agent must interpret highdimensional sensory inputs, infer human intent, reason about 

uncertain outcomes, and produce executable actions in a closed loop [7], [11], [16], [23], [24], [26]–[28]. Effective robotic autonomy, therefore, depends on coupling perception, prediction, and control so that decisions are informed by their expected consequences [29], [30]. 

Classical robotics has addressed this problem through modular pipelines that decompose autonomy into perception, state estimation, planning, and low-level control [31]–[35]. This modularity allows individual components to be independently designed, validated, and replaced, while exposing intermediate representations that facilitate interpretation, diagnosis, and systematic debugging. Such systems remain effective when task objectives, dynamics, and environmental structure can be specified with sufficient accuracy. However, their limitations become more pronounced in open-world manipulation, mobile service robotics, and multitask embodied interaction [3], [36]– [39], where hand-designed representations are brittle under distribution shift, module interfaces can propagate errors, and task-specific models are difficult to scale across scenes, embodiments, and instructions. These considerations have motivated learning-based policies trained on large-scale and heterogeneous data. These considerations have motivated learningbased policies trained on large-scale and heterogeneous data. 

Foundation models have accelerated this shift. VisionLanguage-Action Models (VLAs) map visual observations and language instructions to robot actions or action chunks within a unified policy. Representative systems, including RT-1 [7], RT-2 [6], RoboFlamingo [40], Octo [12], and OpenVLA [11], show that large-scale pretraining and cross-task data aggregation can improve instruction following, policy generalization, and transfer across tasks and embodiments. By aligning visual 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

2 

observations, linguistic goals, and motor commands, VLAs provide a scalable interface between human intent and robot execution [41], [42]. They have also shifted robot learning from narrow task-specific policies toward generalist policies trained on heterogeneous robot data and, in some cases, webscale vision-language representations [43]–[46]. 

Despite this progress, most VLA policies remain primarily reactive. They are typically trained to map the current observation, a short history, and a task instruction to the next action, without explicitly modeling how alternative actions would change future observations, physical states, or task progress [6], [11], [16], [36]. This limitation is critical in longhorizon manipulation, delayed-effect tasks, occluded scenes, and contact-rich interactions [41], [47], [48], where an action that appears locally plausible may prevent later subgoals from becoming reachable. Therefore, world models address a complementary problem by learning how observations, states, rewards, or latent variables evolve as a function of context and actions [49]. Rooted in model-based reinforcement learning and predictive coding, this idea has been instantiated in systems such as Dreamer [50] and TD-MPC [1], as well as in recent latent video prediction, action-conditioned generation, and embodied simulation models [9], [51]–[53]. For robotics, world models are attractive because they support imagination, planning, counterfactual evaluation, data-efficient learning, and uncertainty-aware control [54]–[57]. 

A predictive world model alone, however, is not sufficient for effective robot control. In many model-based formulations, the learned dynamics model, planner, and policy are trained or deployed as separate components [2], [18], [58], [59]. This separation can create a mismatch between predictive fidelity and control utility: visually plausible futures are not necessarily actionable, and accurate short-horizon prediction does not guarantee robust long-horizon behavior [49], [60]. Explicit planning over learned dynamics can also be computationally expensive, sensitive to model bias, and difficult to combine with high-frequency control and multimodal task conditioning. These limitations motivate World-Action Models (WAMs) [19], [22], [23], [61]–[63]. In this survey, we use WAMs to denote models that couple predictive world representations with executable action generation, either by jointly predicting future states and actions or by predicting future states and then inferring actions through an inversedynamics interface. Under this view, future-state imagination, latent dynamics, action decoding, and policy learning are connected within a shared learning or inference process [64]– [66]. Compared with standard VLA policies, WAMs introduce predictive structure for reasoning about action consequences [20], [21], [67]. Compared with conventional model-based reinforcement learning, WAMs increasingly incorporate multimodal foundation-model conditioning, largescale offline robot data, and amortized action generation. This perspective provides a common lens for latent-imagination policies [3], [18], action-conditioned video generators [68]– [70], diffusion-based trajectory and policy models [52], unified video-language-action models [16], [39], [71], and robotic systems that use predicted futures as part of closed-loop control [20], [21], [67]. 

These observations motivate a robotics-oriented survey that goes beyond cataloging individual methods. First, the relevant literature is distributed across video generation, embodied foundation models, VLA policies, model-based reinforcement learning, and robot imitation learning, where closely related ideas are often introduced under different names. Second, existing methods differ along several coupled design dimensions, including representation space, prediction target, action interface, transition formulation, architecture, training objective, and control usage. Third, current evaluation protocols often measure predictive quality, imitation accuracy, planning performance, and real-robot robustness separately, leaving open whether imagined futures are physically feasible, temporally consistent, and ultimately effective in improving closed-loop control. A unified treatment is therefore needed to clarify the scope, design choices, and evaluation criteria of WAMs. 

To address these gaps, this article provides a roboticsoriented survey of WAMs for predictive robot control. We clarify their conceptual scope, organize existing methods through a multi-axis taxonomy, compare their roles across application domains, and summarize evaluation protocols, limitations, and future research directions. Our goal is to establish a structured view of how world prediction and action generation can be coupled to support scalable, reliable, and deployable robot intelligence. The main contributions of this survey are summarized as follows: 

- **Definition and scope.** We define WAMs as predictive control models that connect future-state modeling with executable action generation, and clarify their relationship to conventional world models, model-based reinforcement learning, video generation, and reactive VLA policies. 

- **Taxonomy of model design.** We organize existing methods by model components, transition modeling paradigms, action interfaces, architectural structures, training pipelines, data modalities, and scaling strategies, covering latent dynamics models, video-action models, diffusion and flow-based policies, inverse-dynamics systems, and unified multimodal architectures. 

- **Cross-domain robotics analysis.** We review WAMs in robot manipulation, navigation, autonomous driving, and generalist embodied robotics, emphasizing whether prediction is used for representation learning, look-ahead planning, synthetic data generation, or imagined policy optimization. 

- **Evaluation and open challenges.** We summarize datasets, benchmarks, metrics, and evaluation protocols, and discuss open challenges in action grounding, spatial consistency, neural simulation, real-time inference, embodiment transfer, and safe deployment. 

The remainder of this article is organized as follows. Sec. II recaps the main technical foundations of WAMs and presents a unified formulation that jointly models future observations and actions. Sec. III introduces the taxonomy of WAM architectures and learning paradigms, covering model components, transition modeling, architectural structures, training pipelines, and data scaling. Sec. IV surveys applications in manipula- 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

3 

tion, navigation, autonomous driving, and generalist embodied robotics. Sec. V summarizes datasets, benchmarks, and evaluation metrics, with emphasis on whether predicted futures are useful for control. Sec. VI discusses open challenges and future research directions, and Sec. VII concludes the survey. 

## II. BACKGROUND: FROM WORLD MODELS TO WORLD-ACTION MODELS 

WAMs build on the design principles of WMs and VLAs, but treat future-state prediction and executable action generation as interrelated components of a unified framework. This section clarifies their distinctions in Sec. II-A, reviews foundational threads in Sec. II-B, and connects them to a unified generative view in Sec. II-C. 

## _A. Definition_ 

We consider an embodied agent interacting with its environment and formalize the interaction as a partially observable Markov decision process (POMDP) [72]. The POMDP components are denoted as _⟨S, A, T , R,_ Ω _, O⟩_ , where _S_ , _A_ , _T_ , and _R_ describe a Markov decision process, representing the state space, action space, transition function, and reward function, respectively; Moreover, Ω denotes the set of observations available to the agent, which may include visual observations, robotic-arm poses, and action histories, among other sensory and proprioceptive inputs. _O_ : _S × A →_ Π(Ω) is the observation function, which gives, for each action and resulting state, a probability distribution over possible observations. We further define the latent state space _Z_ as a compressed, lowdimensional encoding space of interaction histories sufficient for predicting future dynamics; the latent action space _U_ as a compact representation space of behaviors bridging highlevel commands and low-level motor control, and the language instruction _ℓ_ as a natural language description of the task that conditions the agent’s behaviors. 

**World Models (WMs)** [29] are predictive models of environment dynamics that enable agents to perform reasoning and prediction without direct interaction. Typically, a world model is defined by a latent state space _Z_ , an action space _A_ , and a transition function _fWM_ that maps past states and actions to the next state: 


**Vision-Language-Action Models (VLAs)** [6], [11] serve as control and decision-making frameworks that focus on generating action sequences directly from visual inputs and language instructions. Conditioned on the current historical observation **o** _<t_<sup>1</sup> and language instruction _ℓ_ , the VLA is a model that directly predicts the future action chunk **a** _t_ : _t_ + _H_ over a horizon of _H_ steps without explicitly modeling future state trajectories: 


**World-Action Models (WAMs)** [19], [23] serve as predictive control and decision-making frameworks that focus on 

> 1For notational consistency between observation and prediction sequences, historical observation indices are shifted backward by one step. 

jointly generating future state trajectories and action sequences from visual inputs and language instructions. Conditioned on the observation history **o** _<t_ and language instruction _ℓ_ , a WAM jointly predicts the future state trajectory **o** _t_ : _t_ + _H_ and action chunk **a** _t_ : _t_ + _H_ over a horizon of _H_ steps, explicitly modeling how actions affect future states: 


## _B. Foundational Research Threads_ 

As summarized in Fig. 2, these research threads respectively provide dynamics modeling, visual prediction, latent action inference, and direct action generation. 

_1) World Model and Model-based Reinforcement Learning:_ Reinforcement learning (RL) is commonly divided into modelfree (MFRL) and model-based (MBRL) paradigms. Unlike MFRL, which learns policies directly from interaction, MBRL leverages a dynamics model for planning and policy optimization. A representative example is PlaNet [73], which introduces the Recurrent State-Space Model (RSSM) to model latent dynamics with deterministic and stochastic states: 


where **h** _t_ and **s** _t_ denote the deterministic and stochastic components of the latent state, respectively; **a** _t_ , **o** _t_ , and _rt_ denote the action, observation, and reward; and _f_ is an RNNbased transition function. Subsequent world models, including explicit approaches [18], [26], [50] that use a decoder and implicit approaches [1], [58], [74], [75] that use latent space regularization, learn latent dynamics through 


where **z** ˆ _t_ +1 denotes the predicted latent state and _E_ is the encoder, and _fθ_ , equivalently denoted as _fWM_ , is a neural world model for predicting latent dynamics. 

_2) Video Generative Models:_ Video Generative Models (VGMs) [76], [77] learn to generate future visual observations from text, images, or video history, providing powerful visual priors for long-horizon prediction and planning. In embodied intelligence, they are better viewed as visual predictive planners rather than explicit dynamics models: 


where _pθ_ denotes the conditional distribution parameterized by the VGM with learnable parameters _θ_ , from which future observations are generated given the observation history and language instruction. 

_3) Latent Action Pre-training:_ Latent Action Pretraining (LAPA) [78] addresses the lack of action labels in internet videos by learning latent actions from visual state transitions and using them for downstream policy learning. The core idea 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

4 


Fig. 2: Conceptual overview of four foundational threads behind WAMs: (a) world models learn latent dynamics by predicting the next state from current state and action; (b) video generative models predict future visual observations conditioned on visual history and language instruction; (c) latent action pretraining infers latent actions from consecutive frames and uses them to model latent transitions; and (d) VLAs generate future action sequences directly from state and language instructions. (The third-row illustrations are adapted from the corresponding papers cited in each thread.) 

is to encode motion dynamics into a structured latent action space that is transferable across domains and embodiments: 


where **u** _t ∈U_ denotes the latent action inferred from consecutive observations **o** _t_ and **o** _t_ +1, _qϕ_ denotes the latent action encoder parameterized by _ϕ_ , and _Fθ_ denotes the forward dynamics model parameterized by _θ_ . 

_4) Vision-Language-Action Models:_ Vision-LanguageAction Models (VLAs) directly map visual observations and language instructions to actions, forming a unified framework for embodied decision-making. Existing VLAs mainly adopt either autoregressive sequence modeling [6], [11] 


or flow matching [16], [36], [79] 


to model action distributions conditioned on visual and language inputs, where **a**<sup>1</sup> _t_ : _t_ + _H_<sup>iscleanactionand</sup><sup>_τ_controlsthe</sup> noise level. 

and the actions responsible for them, bridging visual prediction and decision-making. 

More concretely, the generative process of WAMs can be decomposed into four components [19]: policy generation, forward dynamics, inverse dynamics, and visual planning. Given historical observations **o** _<t_ and a language instruction _ℓ_ , these components can be formalized as: 


In practice, WAMs often optimize multiple components jointly. From the perspective of action generation, existing methods mainly follow two pathways. The first jointly models future observations and actions: 


The second adopts a plan-then-act strategy, where a future visual plan is first generated and actions are then inferred through inverse dynamics (IDM): 

_p_ plan(ˆ **o** _t_ : _t_ + _H |_ **o** _<t, ℓ_ ) _· p_ idm( **a** _t_ : _t_ + _H |_ **o** ˆ _t_ : _t_ + _H ,_ **o** _<t_ ) _._ (15) These two formulations form the basis of the transitionmodeling paradigms discussed in Sec. III-B. 

## _C. From These Threads to World-Action Models_ 

The four threads above provide complementary foundations for WAMs. MBRL focuses on learning environment dynamics for planning and control; VGM enables future-scene prediction from visual observations; LAPA introduces latent action learning from action-free videos; and VLA provides an end-to-end framework for generating actions from visual and language inputs. WAMs unify these ideas within a conditional generative framework that jointly models future observations 

III. ARCHITECTURE DESIGN & MODEL TAXONOMY 

This section organizes WAMs along five complementary axes: core components for encoding language, observations, and actions in Sec. III-A; transition paradigms coupling prediction with action generation in Sec. III-B; structural architectures routing multimodal tokens in Sec. III-C; policy training pipelines from pre-training to post-training in Sec. III-D; and data modality and scaling laws for effective world modeling in Sec. III-E. 

5 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 


Fig. 3: Component-level taxonomy for World-Action Models. The architecture can be viewed through four functional modules: a language interface that provides task conditioning, a visual encoder that defines the predictive state, a predictive backbone that carries dynamics, and an action decoder that converts predicted futures into executable controls. 

## _A. Model Components_ 

WAMs transform contextual and visual inputs into actions through four functional modules: language encoder, visual encoder, action decoder, and model backbone. As summarized in Fig. 3, this decomposition separates general representation from task-specific action mechanisms, providing a consistent basis for architecture comparison. 

_1) Language Encoder:_ In WAMs, language encoders map instructions into conditioning representations, and existing approaches typically fall into the following three categories: 

- **Global Text Encoder:** CLIP [80] learns global semantic representations through large-scale image–text contrastive learning, providing open-vocabulary visual grounding. 

- **Dense Sequence Encoder:** T5 [81] produces dense token-level representations via span-corruption pretraining, capturing fine-grained contextual semantics for detailed language conditioning. 

- **Autoregressive LLMs:** LLMs [82], [83] acquire rich world knowledge and reasoning abilities through nexttoken prediction, enabling task understanding and longhorizon instruction following. 

_2) Visual Encoder:_ The visual encoder maps highdimensional observations into compact latent representations while preserving semantic, spatial, and temporal information. Existing WAMs mainly adopt the following paradigms: 

- **2D VAE:** Widely used in latent diffusion models [4], [84], 2D VAEs compress image frames into compact latent codes, providing efficient spatial representation but limited temporal consistency. 

- **Video VAE:** Video-native VAEs [76], [85] jointly encode spatial and temporal information, producing structured latent dynamics that facilitate future video prediction. 

- **Representation Encoders:** Pretrained vision models such as DINO [86]–[88], CLIP [80], SigLIP [89] and VJEPA [90] extract semantic and geometric features, serving as robust representation spaces rather than pixellevel generators. 

- **3D & Multi-view Encoders:** 3D-aware representations, including point clouds [91], occupancy grids [59], and BEV features [92], explicitly encode geometric structure for spatial reasoning and control. 

- **VLMs:** Some architectures [11], [16] directly reuse pretrained VLM backbones such as Qwen-VL [93], Prismatic [94], and PaliGemma [95], leveraging semantically rich visual features aligned with language understanding. 

- _3) Model Backbone:_ The model backbone captures spa- 

- tiotemporal dynamics from latent states and actions. Existing WAMs mainly adopt two paradigms: 

- **Unified Transformers From Scratch** : Models such as GR-1 [13] process multimodal inputs with a causal Transformer, learning dynamics directly from embodied and video data without relying on pretrained temporal priors. 

- **Pretrained Video Foundation Models** : Architectures such as DreamZero [23] leverage pretrained video generators like Wan [76] and Cosmos [77] as temporal priors, shifting the focus from learning dynamics to aligning visual predictions with control. 

- _4) Action Decoder:_ The action decoder transforms la- 

- tent predictions into executable control signals. Existing approaches mainly fall into three categories: 

- **Action Tokenizer:** The continuous action space is discretized into token vocabularies using vector quantization or action bins [6], [11], [96], enabling LLM-compatible autoregressive prediction and scalable cross-embodiment training, albeit with quantization-induced precision loss. 

6 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 


Fig. 4: **Transition Modeling Paradigms.** Joint prediction couples future observation and action generation within a shared process, whereas the inverse dynamics paradigm factorizes this transition by first imagining future states and then inferring executable actions. 

- **Latent Action Model (LAM):** LAMs [53], [78], [97] learn abstract action representations from state transitions rather than raw controls, decoupling action modeling from embodiment-specific hardware and enabling largescale learning from action-free videos [98]. 

- **Diffusion & Flow-Matching Action Head:** Diffusionbased and flow-based action decoders [8], [16], [79] generate actions directly in continuous space, preserving fine-grained dynamics and multimodal behaviors at the cost of higher inference overhead. 

## _B. Transition Modeling Paradigms_ 

To instantiate the formulations in Eq. (14) and Eq. (15), existing transition modeling of WAMs broadly fall into two complementary paradigms, as illustrated in Fig. 4: **_(i) joint prediction_** , which couples observation and action generation; and **_(ii) inverse dynamics_** , which first predicts future states and then infers actions from the resulting transitions. 

_1) Joint Prediction:_ For single-step transitions, joint prediction is formulated as 


which jointly generates the next action and observation conditioned on the current observation **o** _t_ and language instruction _ℓ_ . The core idea is to unify action generation and future-state prediction under a shared objective, making joint prediction both a direct policy and an auxiliary learning signal that enriches action representations through foresight. 

This paradigm has evolved through several architectural stages. Early works such as GR-1 [13] and GR-2 [38] explored autoregressive co-prediction of actions and future visual representations, demonstrating that language, perception, and control can be modeled within a unified sequence model. With the emergence of diffusion-based generation, later methods adopted continuous denoising formulations for multimodal prediction. VPP [20] combines text-guided video prediction 

with a diffusion policy head, while UWM [19] unifies video and action diffusion within a coordinated framework. 

Recent systems increasingly leverage pretrained video generators as strong temporal priors. WorldVLA [39] and Motus [99] represent two typical designs: the former employs a shared autoregressive token space for text, images, and actions, whereas the latter introduces structured joint attention and separate schedulers for video and action generation. ViPRA [97] and Cosmos Policy [21] further demonstrate that powerful visual priors can substantially improve joint prediction, suggesting that the central challenge is shifting from jointly modeling actions and observations to effectively aligning pretrained generative dynamics with embodimentspecific control. 

_2) Inverse Dynamics Model:_ Under the same single-step assumption, inverse-dynamics WAMs factorize as 


which first predicts the next observation from the current state and language instruction, then infers the action from the resulting transition. This factorization follows a “planthen-act” paradigm, where future states are generated before actions. 

Recent works instantiate this idea with varying degrees of explicitness. In navigation, PathDreamer [2] predicts future visual and semantic states to guide action selection, though planning horizons remain limited. Seer [60] incorporates a more structured inverse-dynamics interface by restricting action-token attention to the current and predicted future states. DreamZero [23] further adopts a chunk-level autoregressive video-generation framework, although its diffusionbased predict-then-act pipeline still incurs notable inference overhead. 

More efficient and implicit IDM variants have recently emerged. LingBot-VA [24] combines a Mixture of Transformers (MoT) [100] with asynchronous inference to improve modeling capacity and execution efficiency. Fast-WAM [22] and GigaWorld-Policy [25] further decouple visual-generation and action-generation attention mechanisms, enabling joint training while supporting direct action decoding at inference time. These designs are therefore closer to implicit IDMs than fully explicit predict-then-act pipelines. Beyond nextstep prediction, goal-reaching dynamics models [101] extend the paradigm to long-horizon planning. For instance, Act2Goal [102] learns a goal-conditioned IDM that predicts target future states rather than only the immediate next observation. _π_ 0 _._ 7 [63] can be viewed as a goal-conditioned WAM that predicts actions toward a specified goal image, which aligns more naturally with goal-conditioned planning than with next-step joint prediction. 

## _C. Architecture Structures_ 

To systematically categorize WAM architectures, we examine how multimodal information flows through the network. As shown in Fig. 5, existing methods broadly fall into two paradigms: **_(i) end-to-end systems_** and **_(ii) dual systems_** . 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

7 


Fig. 5: **Taxonomy of WAM Architectures.** Existing models can be categorized along two orthogonal axes: architectural design and transition modeling paradigm. Structurally, **end-to-end models** (a, b) process all modalities within a unified backbone, whereas **dual systems** (c, d) explicitly separate visual and action experts. In terms of transition modeling, **joint prediction** approaches (a, c) generate future observations and actions simultaneously, while **inverse dynamics** approaches (b, d) follow a factorized, predict-then-act sequential generation. 

_1) End-to-end Systems:_ End-to-end WAMs jointly optimize world modeling and action generation within a single backbone. Language, visual observations, embodiment states, and actions are processed through a shared computational pathway, enabling unified representation learning and scalable pre-training. Representative systems such as GR-1 [13], GR2 [38], and Seer [60] map multimodal inputs directly to future visual predictions and control outputs. PAD [103] and UWM [19] extend this idea with diffusion transformers that jointly denoise image and action tokens. More recent methods, including WorldVLA [39], DreamZero [23], Cosmos Policy [21], and ViPRA [97], further leverage pretrained DiT and video-generation backbones, demonstrating the benefits of large-scale generative pre-training. 

A key challenge of end-to-end systems is multimodal alignment across heterogeneous token spaces. Recent works address this through different architectural strategies. Cosmos Policy [21] transforms non-image signals (e.g., actions, future states, and values) into latent-frame-like representations compatible with video-generation backbones. ViPRA [97] follows a latent action pretraining strategy, learning latent actions from large-scale video [78] before aligning them with robot-specific visual representations. More broadly, end-toend WAMs increasingly inherit strong pretrained priors from VLMs [16], [93], [104] and video diffusion models [76]. Under fixed robot-data budgets, richer vision-language and video representations generally improve action generalization and robustness. For example, DWAM [105] reports enhanced robustness and adaptation efficiency, albeit with increased inference cost. 

_2) Dual Systems:_ Dual-system WAMs explicitly separate world modeling and action generation into distinct modules connected through an intermediate interface. One module predicts or encodes future world evolution, while the other converts predictive representations into executable actions. This decomposition provides greater modularity and interfacelevel controllability, as exemplified by VidMan [67] and VPP [20], although it introduces additional design complexity at the module boundary. 

Current dual-system designs are commonly implemented through two interface patterns. The first is MoT-style routing [100], adopted by LingBot-VA [24] and Fast-WAM [22], 

where modality-specific projections are fused through shared self-attention in a common latent space. The second is cross-attention transfer [16], [79], [106], which explicitly injects visual-language representations into a dedicated actiondecoding module. Representative examples in VLAs include _π_ 0 [16], _π_ 0 _._ 5 [36], and GR00T-style architectures [79], where pretrained VLMs first encode multimodal inputs and action experts generate controls via cross-attention conditioning. Mimic-Video [106] similarly transfers video features to an action decoder through direct cross-attention. Related systems such as VidMan [67] and VPP [20] also follow this modular design by decoupling predictive video modeling from downstream action generation. ImageWAM [107] further adapts this modular paradigm by replacing the video-generation backbone with an image-editing backbone and transferring intermediate representations through a key-value (KV) cache. Additionally, Helix [108] demonstrates the ability to reduce the computational burden of VLMs through a fast-slow dualsystem architecture, particularly for humanoid robots. Overall, the end-to-end versus dual-system taxonomy provides a useful architectural perspective: the former emphasizes unified representation learning, whereas the latter prioritizes modular adaptation and interface design. 

## _D. Policy Training Pipeline_ 

As shown in Fig. 6, WAM training generally follows a twostage pipeline: **pre-training** and **post-training** . Pre-training learns spatiotemporal and action representations from largescale video data, while post-training adapts the model through fine-tuning, data augmentation, and reinforcement learning. 

_1) Pre-Training:_ The pre-training stage of WAMs centers on spatiotemporal representation learning, action representation learning, and video-action alignment. 

**Spatiotemporal Representation:** Recent progress in WAMs has been largely driven by pretrained video backbones such as Seedance [110], Wan [76], Cosmos [77], and Sora [15]. Trained on large-scale video corpora, these models learn general visual dynamics, object interactions, and action-relevant scene changes, providing richer predictive priors than task-specific policies and simplifying downstream action learning [105]. Multi-view pre-training further improves 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

8 


Fig. 6: Policy training pipeline for WAMs. (a) Pre-training leverages internet-scale video data to learn spatiotemporal and action representations and align video with actions; (b) post-training adapts the pretrained model through policy fine-tuning, data augmentation, and reinforcement learning. Images adapted from [23], [78], [109]. 

geometric consistency by preserving 3D structure, object correspondence, and interaction details, benefiting both robot manipulation [21] and autonomous driving [111]. Beyond pixellevel reconstruction, several works, such as JEPA-WAM [112] and LaWAM [113], incorporate representation prediction into the WAM framework, enabling dynamics modeling directly in the learned feature space. 

**Action Representation:** Action representation learning transforms raw control signals into compact, model-friendly formats. One line of work focuses on explicit tokenization or parameterization: OpenVLA [11] uses discrete action tokens with autoregressive decoding, FAST [109] applies discrete cosine transforms to decompose actions into high- and lowfrequency components, and OpenVLA-OFT [114] adopts continuous representations with bidirectional attention, shifting from next-step prediction toward trajectory-level control. Another line explores latent action pretraining from videos or action-free trajectories. LAPA [78] learns latent actions from visual changes, AdaWorld [53] conditions world models on self-supervised latent actions, and ViPRA [97] aligns videoderived latent actions with robot controls during adaptation. VLA-JEPA [115] further combines latent action learning with flow-matching action heads to bridge generic motion representations and embodiment-specific control. 

**Video-Action Alignment:** A central objective of WAM pre-training is to align video and action representations. UWM [19] identifies four alignment routes: forward dynamics, inverse dynamics, action generation, and video generation. Most systems combine multiple routes. For instance, DreamZero [23] couples video generation with inverse dynamics, Fast-WAM [22] and GigaWorld-Policy [25] combine video and action generation, and Cosmos Policy [21] jointly optimizes action generation, video generation, and forward dynamics. As discussed, neither joint prediction nor IDM is universally superior [22]; they reflect different trade-offs. 

The main challenge is ensuring video representations are both predictive and actionable while maintaining training stability and inference efficiency [105]. Joint-prediction models must balance multimodal generation with accurate action decoding, whereas IDM-based methods rely on sufficiently informative future-state predictions for reliable inverse dynamics. 

_2) Post-Training:_ Post-training adapts pretrained WAMs for deployment on specific robot platforms through policy fine-tuning, data augmentation, and reinforcement learning in imagined environments. 

**Policy Fine-tuning:** Policy fine-tuning adapts pretrained world representations to target sensing modalities, action spaces, and deployment conditions with limited demonstrations or interaction data. Parameter-efficient methods such as LoRA [116], lightweight adapters, and residual action heads enable efficient adaptation of large backbones. Additional objectives can further improve performance. The image-prediction objective in Eq. (13) enhances generalization to unseen tasks [23], while action-grounding optimization in Eq. (12) supports human-to-robot and robot-torobot transfer [115]. For IDM-based pipelines, fine-tuning often jointly adapts the planner and inverse-dynamics module to reduce planning mismatch and action-grounding errors [67]. DreamZero [23], for instance, achieves strong crossembodiment transfer with only about 30 minutes of real-robot data. 

**Data Augmentation:** Data augmentation improves robustness to visual and environmental variations. One common strategy is label-preserving trajectory rewriting, which rerenders videos with modified appearance, morphology, illumination, or style while preserving task semantics. GigaBrain0 [62], GigaWorld-0 [117], and Cosmos-Transfer [118] use world-model-generated data for real2real, sim2real, and crossdomain transfer. Another strategy is action-grounded trajectory synthesis. Since video world models generate rollouts without action labels, inverse-dynamics or latent action models recover 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

9 


Fig. 7: Data modality and scaling structure for World-Action Models. The left panel illustrates how different sensing modalities expose complementary action-relevant state variables, while the right panel shows a data-pyramid view in which large actionfree video corpora provide broad world priors and smaller embodied trajectories provide action grounding. 

pseudo-actions to construct synthetic video-action trajectories for policy learning and evaluation, as explored by DreamGen [119] and WorldArena [120]. 

**Reinforcement Learning:** In large language models, reinforcement-learning-based post-training methods such as RLHF [121], [122] and OPD [123] have been widely adopted. In robotics, RL post-training has likewise demonstrated substantial benefits for dexterous and contact-rich manipulation [124]–[126]. Embodied RL generally follows three routes: simulation-based RL exploits privileged states and dense rewards but faces the sim2real gap; real-world RL, such as SERL [127] and RL-token [126], avoids simulation transfer but incurs substantial interaction and safety costs; and worldmodel-based RL [64], [66], [128] optimizes policies through imagined rollouts, reducing physical interaction at the risk of model bias. A typical world model-based pipeline trains an action-conditioned world model, a reward predictor [129], and an imitation-initialized policy before refinement through imagined trajectories [130]. World4RL [66] performs PPO optimization with a diffusion world model, while World-VLALoop [64] connects imagined experience with real-world improvement. WAM-OPD [128] instead provides dense teacher supervision on student-induced trajectories. Although Cosmos Policy [21] jointly predicts future observations, values, and actions, their effective integration for scalable WAM posttraining remains an open problem. 

## _E. Data Modality, Scaling, and Mixture_ 

Data modality and scale are critical to both VLAs and WAMs, as illustrated in Fig. 7. The choice of modality determines what information the model observes and how each modality contributes to decision-making, while scale influences the richness of learned dynamics and the availability of action supervision. 

_1) Data Modality:_ The following summarizes major data modalities and their implications for WAM design. 

**Language Conditioning:** Language provides task-level conditioning. In VLAs, it is often used as contextual input or for subtask planning [36], whereas WAMs typically encode language separately and fuse it with visual or state features through cross-attention. 

**Multi-view Video:** Visual observations provide rich environmental cues for decision-making and control. Multi-view inputs further improve spatial understanding, although generating consistent multi-view predictions remains challenging for WAMs [131]. 

**3D Geometric Structure:** 3D representations offer unified spatial structures and explicit geometric constraints [132], [133]. While prediction in occupancy or geometric spaces has shown promise [59], [134], [135]. 4DGSWAM [136] and 4DWAM [137] explore general 3D world prediction, although this research direction remains at an early stage. 

**Contact and Auditory Feedback:** Tactile [138], [139] and auditory signals reveal interaction events that may be difficult to infer from vision alone, especially in industrial applications [140]. Existing work either incorporates these sensors directly [141], [142] or predicts them from visual inputs [143], suggesting their potential for interaction-aware world modeling. 

**Proprioception State:** Robot states such as joint positions and end-effector poses provide direct physical information, complementing visual observations under occlusion and supporting action generation. Recent works [21] further use predicted actions as part of the state to reduce OOD issues and enhance temporal consistency. 

_2) Data Scaling and Mixture:_ As illustrated in Fig. 7, different data sources provide complementary supervision for WAMs. We categorize them into three groups: task-agnostic 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

10 

internet videos, task-relevant egocentric demonstrations [144], [145], and embodiment-specific trajectories [146]. The first two mainly provide visual dynamics priors, while the last supplies direct action supervision. 

**Internet Videos:** Internet-scale videos primarily support temporal prediction and representation learning. GR-1 [13] and GR-2 [38] use such data for visual pre-training, while LAPA [78] and DreamDojo [98] infer latent actions from unlabeled videos. Large video generators such as Wan [76] and Cosmos [77] further demonstrate the value of web-scale video corpora for learning world dynamics. 

**Egocentric Demonstrations:** UMI [147] expands manipulation data through robot-free, handheld demonstrations transferable to robot policies. Egocentric datasets [144], [145] provide rich first-person interaction videos, with actions recovered through instrumented gloves or vision-based hand-pose estimation [148]. EgoScale [149] further highlights the potential of human demonstrations for cross-embodiment transfer. Dyna-2 [150] scales first-person human manipulation videos to one million hours, demonstrating the advantage of WAMs over VLAs in learning from videos without hand-action labels. 

**Embodied Trajectories:** Embodied trajectories ground WAMs in executable control by coupling observations with robot states, actions, and physical outcomes. Although much smaller than web-scale video datasets, resources such as Open X-Embodiment [146], DROID [151], and BridgeData [152] provide essential action-conditioned supervision across tasks, embodiments, and contact-rich interactions, serving as the key bridge between broad visual priors and controllable world prediction. LBM [153] performs large-scale pre-training on these real robot data using diffusion policy [8] and demonstrates robustness under distribution shift. 

## IV. APPLICATIONS 

WAMs are used differently across embodied domains. Their value may lie in representation learning before policy training, in imagined look-ahead during inference, or in synthetic trajectories used for policy improvement. We therefore organize this section by application domain, including robot manipulation (Sec. IV-A), navigation (Sec. IV-B), autonomous driving (Sec. IV-C), and examine the role that prediction plays in each domain. 

## _A. Robot Manipulation_ 

Manipulation is the most common testbed for WAMs because it couples visual prediction with physically constrained action. A useful rollout must accurately model object states, contact dynamics, occlusions, and task progress rather than merely appear visually plausible. Existing work falls into three broad groups: video-action policies, structured state models, and imagination-based policy optimization. 

_1) Video-Action and Unified Policies:_ Video-action models use predictive pre-training to shape action representations. GR-1 [13] and GR-2 [38] establish a representative recipe: pretrain a temporal video backbone and adapt it to demonstrations so that future observations and robot actions 

share a trajectory-level representation. Diffusion and flowbased variants such as PAD [103], UWM [19], VPP [20], Seer [60], VidMan [67], Cosmos Policy [21], and ViPRA [97] further tighten this connection through denoising, latent action alignment, or lightweight control adapters. Unified WAMs make the prediction-control interface explicit at inference time. WorldVLA [39], Motus [99], and LingBot-VA [24] jointly generate observations and actions, while World2Act [159] and Act2Goal [102] use predicted future states or goals as intermediate control targets. In contrast, VLA-JEPA [115], LAWM [161], and HiLAM [163] mainly use predictive objectives to improve latent representations, avoiding costly online video rollout during deployment. 

_2) Structured State Models:_ RGB rollouts are often underspecified for contact-rich manipulation. Geometry- and physics-oriented WAMs therefore predict representations closer to control variables: ManiGaussian++ [133] and GWM [135] model dynamic scenes with Gaussian representations, ParticleFormer [132] captures deformable and multimaterial interactions, PointWorld [157] scales point-cloud dynamics, and PIN-WM [158] adds physics-informed constraints. Multimodal models such as VT-WM [143], ClothWM [160], and Audio-WM [142] further capture contact, compliance, or event cues that are weakly visible in RGB. 

_3) Imagination-based Policies:_ A complementary direction treats the world model as an imagined environment. World4RL [66], DreamPlan [162], VAMPO [164], PRWM [165], WMPO [130], EVA [65], and RISE [154] optimize or evaluate policies through imagined interaction. VLA-MBPO [155], GPC [156], RoboHorizon [47], WorldVLA-Loop [64], and IWS [55] further close the loop between policy failures, world-model rollouts, and synthetic trajectory generation. Across these lines, the core question is whether predicted futures improve executable control in contact-rich settings, under distribution shift, and over long horizons. 

## _B. Navigation_ 

Navigation is less contact-sensitive than manipulation, but it relies more heavily on long-horizon spatial reasoning under partial observability, using egocentric visual context to make sequential waypoint decisions. WAMs are therefore used mainly as look-ahead modules: they predict future egocentric views, semantic maps, or latent states that support waypoint or action selection. 

_1) Look-Ahead Planning:_ Pathdreamer [2] predicts future panoramas and semantic maps for waypoint selection, while DreamWalker [167] combines latent imagination with tree search to avoid long pixel-space rollouts. NWM [169] and MonoDream [166] extend this paradigm across navigation domains and monocular panoramic settings. Platform-aware future poses and failure probabilities can be predicted from terrain geometry, proprioceptive history, and candidate velocity commands to support MPPI-based navigation [171]. These methods keep planning modular: the world model supplies candidate futures, and a downstream planner selects actions. 

_2) Latent Planning and WM-RL:_ Other systems reduce the predictive interface to latent plans or imagined training 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

11 

TABLE I: Unified summary of WAMs in Sec. IV, grouped by application domain. Category labels: **<mark>VAM</mark>** Video-Action Models, **<mark>Uni</mark>** Unified WAMs (joint observation and action generation), **<mark>WM-Plan</mark>** WMs-guided Planning (predictions from WMs and action generated by external planner), **<mark>RL</mark>** WM-RL (imagination-based RL), **<mark>3D</mark>** 3D/Geometry-based. 

|**Method**|**Paradigm**|**Backbone**|**Eval / Note**|**Method**|**Paradigm**|**Backbone**|**Eval / Note**|
|---|---|---|---|---|---|---|---|
|**_Manipulation_**||||||||
|GR-1 [13]|**VAM**|GPT|LIBERO, CALVIN|EVA [65]|**RL**|video WM|RoboTwin 2.0|
|GR-2 [38]|**VAM**|GPT, 38M|LIBERO, CALVIN|RISE [154]|**RL**|latent|contact-rich|
|PAD [103]|**Uni**|DiT|LIBERO|VLA-MBPO [155]|**RL**|video WM|LIBERO-Plus|
|UWM [19]|**Uni**|4-mode DiT|LIBERO|GPC [156]|**RL**|rollout WM|Push-T|
|VPP [20]|**VAM**|video pred.|dexterous|WMPO [130]|**RL**|pixel WM|LIBERO|
|Seer [60]|**VAM**|GPT+mask|100K demos|RoboHorizon [47]|**RL**|LLM+WM|sparse reward|
|VidMan [67]|**VAM**|vid. diff.+adapt.|Bridge|World-VLA-Loop [64]|**RL**|feedback|ManiSkill|
|Cosmos Policy [21]|**VAM**|Cosmos-P2|bimanual|IWS [55]|**RL**|video WM|10-min @15FPS|
|ViPRA [97]|**VAM**|flow-match|100-200 demos|ManiGaussian++ [133]|**3D**|Gaussian|bimanual|
|GigaWorld-Policy [25]|**Uni**|l<br>action-cent.|DROID|ParticleFormer [132]|**3D**|particles|deformable|
|Fast-WAM [22]|**VAM**|video pred.|LIBERO, RoboTwin|GWM [135]|**3D**|VAE+diff|MetaWorld|
|WorldVLA [39]|**Uni**|Chameleon AR|LIBERO|PointWorld [157]|**3D**|point cloud|2M+ traj|
|Motus [99]|**Uni**|MoT|RoboTwin|PIN-WM [158]|**3D**|physics-inf.|non-prehensile|
|LingBot-VA [24]|**Uni**|causal-diff MoT|AgiBot|VT-WM [143]|**3D**|visuo-tactile|contact|
|World2Act [159]|**Uni**|LLM+skill|RoboCasa|Cloth-WM [160]|**3D**|DreamerV2|cloth|
|Act2Goal [102]|**VAM**|goal-cond.|RoboTwin 2.0|Audio-WM [142]|**3D**|acoustic|liquid pour|
|VLA-JEPA [115]|**VAM**|JEPA+flow|LIBERO|World4RL [66]|**RL**|diff. WM|frozen env|
|LAWM [161]|**VAM**|l<br>latent action|LIBERO|DreamPlan [162]|**RL**|video WM|VLA finetune|
|HiLAM [163]<br>PRWM [165]|**VAM**<br>**RL**|hier. latent<br>contrastive RL|long-horizon<br>DROID|VAMPO [164]|**RL**|GRPO/denoise|i<br>LIBERO, CALVIN|
|**_Navigation_**||||||||
|Pathdreamer [2]|**WM-Plan**|panoramic gen.|R2R|MonoDream [166]|**WM-Plan**|monocular|R2R-CE, RxR-CE|
|DreamWalker [167]<br>NWM [169]<br>perceptive FDM [171]|**WM-Plan**<br>**WM-Plan**<br>**WM-Plan**|latent+MCTS<br>multi-domain<br>GRU|R2R, VLN-CE<br>Habitat, Ego4D<br>ANYmal, quadruped|X-MOBILITY [168]<br>InternVLA-N1 [170]<br>RWM [172]|**RL**<br>**VAM**<br>**RL**|latent WM env<br>dual-system latent<br>GRU|mobile robot<br>R2R-CE<br>A1, quadruped|
|WMP [173]|**RL**|RSSM|Isaac|||||
|**_Autonomous Driving_**||||||||
|DriveDreamer [174]|**WM-Plan**|video gen.|nuScenes|ADriver-I [175]|**Uni**|AR img+act|nuScenes|
|GAIA-1 [68]|**WM-Plan**|text-video|large-scale|DrivingGPT [176]|**Uni**|large AR video|NAVSIM|
|DriveDreamer-2 [177]|**WM-Plan**|multi-cam. gen.|nuScenes|Doe-1 [178]|**Uni**|autoregressive|nuScenes|
|GAIA-2 [179]|**WM-Plan**|multi-cam. scaled|OpenDV|OccLLaMA [180]|**Uni**|occ.+language|nuScenes-QA|
|DrivingWorld [181]|**WM-Plan**|long-horizon AR|nuScenes|ProphetDWM [182]|**Uni**|long-horizon|NAVSIM, nuPlan|
|DrivingGen [183]|**WM-Plan**|policy-cont. eval|nuScenes|VaViM/VaVAM [184]|**Uni**|video AR+action AR|OpenDV|
|OccWorld [59]|**WM-Plan**|voxel tokens|nuScenes-Occ|DriveLaW [185]|**Uni**|language-action|nuScenes|
|Drive-OccWorld [134]|**WM-Plan**|multi-step occ.|nuScenes-Occ|AutoMoT [186]|**Uni**|async. MoT|Bench2Drive|
|DreamerAD [187]|**RL**|Dreamer-AD|nuScenes, nuPlan|World4Drive [188]|**RL**|virtual env RL|NAVSIM, nuPlan|


environments. X-MOBILITY [168] trains a mobile policy with reinforcement learning inside a latent world model, whereas InternVLA-N1 [170] learns compact latent plans from unlabeled navigation trajectories and translates them into realtime commands. WMP [173] uses the recurrent latent state of a world model trained on depth images and proprioception to guide visual legged locomotion. RWM [172] serves as a learned neural simulator for optimizing robotic control policies over long autoregressive imagined rollouts. Thus, these navigation WAMs need not generate explicit images; their practical value is measured by improved waypoint selection, longhorizon consistency, and robustness under partial observability. 

## _C. Autonomous Driving_ 

Driving WAMs must satisfy real-time, safety, and multiagent constraints. Prediction is used not only for control, but also for scenario synthesis and structured scene evolution. This leads to three recurring roles: controllable video generation, occupancy-based forecasting, and unified perceptionprediction-planning. 

_1) Generation and Structured Scene Prediction:_ Generative driving WAMs synthesize future traffic scenes conditioned on commands, trajectories, or text. DriveDreamer [174], GAIA-1 [68], DriveDreamer-2 [177], GAIA-2 [179], DrivingWorld [181], and DrivingGen [183] use this capability for data augmentation, scenario coverage, or policy-conditioned evaluation. DriveVLA-W0 [189] further studies how such generated data affects downstream driving policies. Occupancy- 

based WAMs replace pixel futures with planning-oriented 3D states. OccWorld [59] and Driving in the Occupancy World [134] forecast semantic occupancy under action or temporal conditioning, aligning prediction with free space, dynamic agents, and collision-related evaluation. 

_2) Unified Driving Agents and WM-RL:_ Unified driving WAMs couple scene prediction and action generation. ADriver-I [175], DrivingGPT [176], Doe-1 [178], and OccLLaMA [180] integrate future observation, trajectory, occupancy, or language-conditioned action modeling. ProphetDWM [182], VaViM/VaVAM [184], DriveLaW [185], and AutoMoT [186] further emphasize long-horizon consistency, structured latents, and efficient control. Driving also motivates world-model RL. DreamerAD [187] and World4Drive [188] train policies through imagined rollouts, which is attractive for rare and safety-critical events but depends strongly on actionconditioned dynamics fidelity. The main evaluation challenge is to connect visual realism, traffic consistency, safety, and closed-loop driving performance. 

## V. DATASETS, BENCHMARKS, AND EVALUATION METRICS 

Evaluation resources for WAMs have different purposes. Datasets provide offline demonstrations, trajectories, or videolanguage pairs for pre-training and adaptation; benchmarks define task protocols and metrics; simulators provide the physical or visual environment in which closed-loop policies are tested. Since many resources are shared across application domains, we organize this section by resource type. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

12 

TABLE II: Compact definitions of metrics used for WAMs. 

|**Metric (Full name)**|**Formula / definition**|
|---|---|
|**_Task completion and navigation_**||
|**SR** (Success Rate)<br>**SPL** (Success weighted by Path Length) [190]<br>**NE** (Navigation Error) [191]<br>**nDTW** (normalized Dynamic Time Warping) [192]|SR = _N _<sup>_−_1 �</sup><sup>_N_</sup><br>_i_=1 <sup>_si_, where</sup> <sup>_si ∈{_0</sup><sup>_,_ 1</sup><sup>_}_ indicates task success.</sup><br>SPL = _N _<sup>_−_1 �</sup><sup>_N_</sup><br>_i_=1 <sup>_siℓi/_ max(</sup><sup>_pi, ℓi_), where</sup> <sup>_ℓi_ and</sup> <sup>_pi_ are the shortest and executed path lengths.</sup><br>NE = _N _<sup>_−_1 �</sup><sup>_N_</sup><br>_i_=1 <sup>_dG_(</sup><sup>_v_stop</sup><br>_i_<br>_, v_<sup>goal</sup><br>_i_<br>), where _dG_ is the geodesic shortest-path distance.<br>nDTW_i_ = exp[_−_DTW_dG_(**P**<sup>_⋆_</sup><br>_i _<sup>_,_ ˆ</sup><sup>**P**</sup><sup>_i_)</sup><sup>_/_(</sup><sup>_|_</sup><sup>**P**</sup><sup>_⋆_</sup><br>_i _<sup>_|d_th)]; report</sup> <sup>_N −_1 �</sup><br>_i_ <sup>nDTW</sup><sup>_i_.</sup>|
|**_Trajectory and localization_**||
|**ADE** (Average Displacement Error) [193], [194]<br>**FDE** (Final Displacement Error) [193], [194]<br>**ATE** (Absolute Trajectory Error) [195]<br>**RPE** (Relative Pose Error) [195]|ADE = _N _<sup>_−_1 �</sup><sup>_N_</sup><br>_i_=1 <sup>_T −_1</sup><br>_i_<br>�_Ti_<br>_t_=1 <sup>_∥_ˆ</sup><sup>**x**</sup><sup>_i,t −_</sup><sup>**x**</sup><sup>_i,t∥_2.</sup><br>FDE = _N _<sup>_−_1 �</sup><sup>_N_</sup><br>_i_=1 <sup>_∥_ˆ</sup><sup>**x**</sup><sup>_i,T_</sup>_i _<sup>_−_</sup><sup>**x**</sup><sup>_i,T_</sup>_i_<sup>_∥_2.</sup><br>After alignment by **S** _∈_SE(3), ATE = [_N _<sup>_−_1 �</sup><sup>_N_</sup><br>_i_=1 <sup>_∥_trans(</sup><sup>**T**</sup><sup>_−_1</sup><br>_i_<br>**S** <sup>ˆ</sup>**T**_i_)_∥_<sup>2</sup><br>2<sup>]1</sup><sup>_/_2.</sup><br>RPEtrans = [(_N −_∆)<sup>_−_1 �</sup><sup>_N−_∆</sup><br>_i_=1<br>_∥_trans(**E**_i_)_∥_<sup>2</sup><br>2<sup>]1</sup><sup>_/_2, where</sup> <sup>**E**</sup><sup>_i_ = (</sup><sup>**T**</sup><sup>_−_1</sup><br>_i_<br>**T**_i_+∆)<sup>_−_1</sup>(<sup>ˆ</sup>**T**<sup>_−_1</sup><br>_i_<br>ˆ**T**_i_+∆).|
|**_Generation quality_**||
|**FID** (Fr´echet Inception Distance) [196]<br>**FVD** (Fr´echet Video Distance) [197]<br>**PSNR** (Peak Signal-to-Noise Ratio)<br>**SSIM** (Structural Similarity Index) [198]<br>**LPIPS** (Learned Perceptual Image Patch Similarity) [199]|FID = _∥_**_µ_**_r −_**_µ_**_g∥_<sup>2</sup><br>2 <sup>+ tr[</sup><sup>**Σ**</sup><sup>_r_ +</sup><sup>**Σ**</sup><sup>_g −_2(</sup><sup>**Σ**1</sup><sup>_/_2</sup><br>_r_<br>**Σ**_g_**Σ**<sup>1</sup><sup>_/_2</sup><br>_r_<br>)<sup>1</sup><sup>_/_2</sup>].<br>The same Fr´echet form as FID, computed on video-feature distributions.<br>PSNR = 10 log10[_v_<sup>2</sup><br>max<sup>_/_ MSE(</sup><sup>**I**</sup><sup>_,_ ˆ</sup><sup>**I**)], where</sup> <sup>_v_max is the declared maximum pixel value.</sup><br>SSIM(**I**_,_ <sup>ˆ</sup>**I**) = [(2_µIµ_ˆ<br>_I_ <sup>+</sup><sup>_c_1)(2</sup><sup>_σ_</sup>_I_ <sup>ˆ</sup><br>_I_ <sup>+</sup><sup>_c_2)]</sup><sup>_/_[(</sup><sup>_µ_2</sup><br>_I_ <sup>+</sup><sup>_µ_2</sup><br>ˆ<br>_I_ <sup>+</sup><sup>_c_1)(</sup><sup>_σ_2</sup><br>_I_ <sup>+</sup><sup>_σ_2</sup><br>ˆ<br>_I_ <sup>+</sup><sup>_c_2)].</sup><br>�<br>_l_<sup>(</sup><sup>_HlWl_)</sup><sup>_−_1 �</sup><br>_h,w _<sup>_∥_</sup><sup>**w**</sup><sup>_l ⊙_[ˆ</sup><sup>**_ϕ_**</sup>_l_<sup>(</sup><sup>**I**)</sup><sup>_h,w −_ˆ</sup><sup>**_ϕ_**</sup>_l_<sup>(ˆ</sup><sup>**I**)</sup><sup>_h,w_]</sup><sup>_∥_2</sup><br>2<sup>.</sup>|
|**_Language and captioning_**||
|**BLEU** (Bilingual Eval. Understudy) [200]<br>**ROUGE-L** (Recall-Oriented Understudy for Gisting Eval.) [201<br>**CIDEr** (Consensus-based Image Description Eval.) [202]<br>**METEOR** (Metric for Eval. of Translation with Explicit<br>ORdering) [203]|BLEU = BP exp(<sup>�</sup><sup>_M_</sup><br>_n_=1 <sup>_wn_ log</sup><sup>_pn_), using modified</sup> <sup>_n_-gram precision</sup> <sup>_pn_ and brevity penalty BP.</sup><br>]<br>ROUGE-L = (1 +_β_<sup>2</sup>)_P_LCS_R_LCS_/_(_R_LCS +_β_<sup>2</sup>_P_LCS).<br>CIDEr = <sup>�4</sup><br>_n_=1 <sup>_wn|R|−_1 �</sup><br>_r∈R_ <sup>cos[</sup><sup>**g**</sup><sup>_n_(</sup><sup>_c_)</sup><sup>_,_</sup><sup>**g**</sup><sup>_n_(</sup><sup>_r_)], where</sup> <sup>**g**</sup><sup>_n_ is a TF–IDF</sup> <sup>_n_-gram vector.</sup><br>METEOR = _F_mean(1_−_Penalty), where _F_mean = _P R/_[_αP_ + (1_−α_)_R_] and the penalty measures<br>alignment fragmentation.|
|**_Driving and RL aggregate_**||
|**DS** (Driving Score) [204], [205]<br>**PDMS** (Predictive Driver Model Score) [206]<br>**HNS** (Human Normalized Score) [207]|DS = _N _<sup>_−_1 �</sup><sup>_N_</sup><br>_i_=1 <sup>RC</sup><sup>_i_ IS</sup><sup>_i_: route-level products are averaged, rather than multiplying separate means.</sup><br>_qi_ = NC_i_DAC_i_(5 TTC_i_+5 EP_i_+2 C_i_)_/_12, PDMS = _N_<sup>_−_1 �</sup><br>_i _<sup>_qi_; TTC is a normalized subscore.</sup><br>HNS_g_ = (_s_agent_,g −s_random_,g_)_/_(_s_human_,g −s_random_,g_), computed per game before cross-game<br>aggregation.|


_Note: N_ is the number of evaluated episodes or samples; _Ti_ is the prediction horizon of sample _i_ ; **x** ˆ _i,t_ and **x** _i,t_ are predicted and reference states; **P**<sup>ˆ</sup> _i_ and **P**<sup>_⋆_</sup> _i_<sup>are predicted/executed</sup> and reference paths; and _R_ is a reference sentence set. 

## _A. Metric Families and Evaluation Protocols_ 

Tab. II expands the acronyms and gives compact definitions for the metric families used for WAMs. 

Task-level metrics such as SR, route completion, driving score, episode return, and chain length are closest to the final control objective, but they rarely isolate whether success comes from better prediction, stronger imitation priors, or task-specific policy learning [206]–[209]. Trajectory metrics such as ADE/FDE, L2 displacement, NE, SPL, nDTW, ATE, and RPE measure path or pose consistency and are useful for planning-heavy WAMs, but low trajectory error does not guarantee safety under feedback. Generation metrics such as FID, FVD, LPIPS, PSNR, and SSIM evaluate visual fidelity; they are necessary for video-based WAMs but insufficient for action grounding. Semantic, language, and occupancy metrics such as mIoU, mAP, NDS, BLEU, CIDEr, and ROUGE assess structured outputs, while latency, collision, comfort, and infraction metrics capture deployment constraints. WAM evaluations are therefore most informative when it reports both predictive quality and downstream control utility. 

## _B. Robot Demonstration and Human Video Corpora_ 

Paired robot resources primarily support pre-training and embodiment adaptation rather than serving as standalone evaluation benchmarks. As summarized in Tab. III, corpora such as DROID, BridgeData V2, Open X-Embodiment, and AgiBotWorld provide action-grounded demonstrations at different scales across diverse embodiments [146], [151], [152], [211]. Their utility for WAMs is typically assessed using down- 

stream task success, instruction-following accuracy, and rollout quality [13], [19], [21], [38], [67]. A second group comprises human video resources spanning egocentric recordings and web-scale collections, including Something-Something v2 (SSv2), Ego4D, EgoDex, Kinetics-700, and HowTo100M. These datasets expand motion, interaction, and language priors far beyond the scale of paired robot data, but they do not directly specify robot actions [144], [145], [210], [212], [213]. Consequently, their contribution is usually assessed after latent action learning, inverse-dynamics alignment, or robot-data fine-tuning [23], [38], [78], [97]. The distinction reflected in Tab. III is therefore important: unpaired human video improves predictive priors, whereas paired robot trajectories provide the action grounding required for control. 

## _C. Simulated Manipulation Task Suites_ 

Simulated manipulation suites provide controlled closedloop evaluation for WAMs. The resources summarized in Tab. III span language-conditioned long-horizon tasks, multitask manipulation, dual-arm control, kitchen-scale scene generalization, synthetic demonstration generation, and focused contact-rich probes [8], [208], [209], [214]–[218], [220], [221]. This diversity matters because a WAM that performs well on short-horizon single-object manipulation may still fail under instruction chaining, contact ambiguity, or scene-level generalization. The main evaluation signal in these suites is task success, but the metric profile varies with the benchmark’s purpose. LIBERO, MetaWorld, RoboCasa, RLBench, ManiSkill, SimplerEnv, and Push-T emphasize success rate, normalized score, or contact/task-specific measures, whereas 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

13 

TABLE III: Summary of surveyed datasets, simulators, and benchmarks. Columns report **Name** , **Reported Scale** , **Type** , and **Eval Metrics** . Scales retain the units used by their primary sources and are not directly comparable. Here, “k” and “M” denote thousand and million, respectively. **N/A** denotes an open-ended simulator, whereas “—” indicates unavailable scale information. 

|**Name**|**Reported Scale**|**Type**|**Eval Metrics**|**Name**|**Reported Scale**|**Type**|**Eval Metrics**|
|---|---|---|---|---|---|---|---|
|**_Robot demonstration and hum_**|**_an video corpora_**|||||||
|DROID [151]|76k trajectories|**Real**|SR, FVD, FID|Ego4D [145]|3.67k hours|**Real**|SR, ATE, RPE|
|BridgeData V2 [152]|60,096 trajectories|**Real**|SR, Accuracy|EgoDex [144]|829 hours / 194 tasks|**Real**|SR (downstream)|
|Open X-Embodiment [146]|1M+ trajectories|**Mixed**|SR, FVD, LPIPS|Kinetics-700 [210]|700 classes|**Real**|SR (downstream)|
|AgiBot-World [211]|1M+ trajectories|**Real**|SR, FVD, LPIPS|HowTo100M [212]|136M clips|**Real**|SR (downstream)|
|SSv2 V2 [213]|220k clips|**Real**|SR (downstream)|||||
|**_Manipulation task suites and _**|**_benchmarks_**|||||||
|LIBERO [208]|130 tasks|**Sim**|SR, FVD, LPIPS, PSNR|MimicGen [214]|18 tasks / 50k+ demos|**Sim**|SR, FVD|
|CALVIN [209]|34 tasks|**Sim**|Avg. Len., SR, FID|RLBench [215]|100+ tasks|**Sim**|SR|
|MetaWorld [216]|50 tasks|**Sim**|SR, Norm. Score|ManiSkill (1/2/3) [217]|20+ tasks|**Sim**|SR, Norm. Score|
|RoboTwin / 2.0 [218], [219]|50+ tasks|**Mixed**|SR, PSNR, SSIM|SimplerEnv [220]|—|**Sim**|SR, Accuracy|
|RoboCasa [221]|100 tasks / 120 scenes|**Sim**|SR, FVD, SSIM|Push-T [8]|1 task|**Sim**|IoU, SR|
|RoboDojo [222]|60 tasks|**Mixed**|SR, Avg. Score|||||
|**_Autonomous driving datasets _**|**_and simulators_**|||||||
|nuScenes [223]|1k scenes|**Real**|Coll., L2, mIoU, FVD|Waymo Open Motion [194]|103k segments|**Real**|ADE, FDE, Miss Rate|
|nuPlan [224]|1.3k hours|**Real**|PDMS, Comfort, TTC|OpenDV-2K [225]|2,059 hours|**Real**|FID, FVD, LPIPS|
|NAVSIM v1/v2 [206], [226]|—|**Mixed**|PDMS, EPDMS, NC|BDD100K [227]|100k videos|**Real**|Accuracy, mAP|
|Bench2Drive [205]|220 routes / 12 towns|**Sim**|DS, RC, IS, L2|KITTI [228]|6 hours|**Real**|FID, FVD|
|CARLA [204]|N/A|**Sim**|DS, IS, RC, Coll.|Argoverse [193]|327.8k sequences|**Real**|ADE, FDE|
|OpenScene [229]|120+ hours|**Real**|mIoU, Coll. Rate|ZOD [230]|1.5k scenes|**Real**|mAP|
|**_Navigation environments, dat_**|**_asets, and benchmarks_**|||||||
|Matterport3D [231]|90 buildings|**Real**|SR, SPL, NE, nDTW|RECON [232]|—|**Real**|SR|
|R2R / R2R-CE [191], [233]|7.2k paths|**Sim**|SR, SPL, NE, Oracle|TartanDrive [234]|—|**Real**|SR|
|RxR / RxR-CE [235]|16.5k paths|**Sim**|SR, SPL, NE|SCAND [236]|—|**Real**|SR|
|Habitat [237]|N/A|**Sim**|SR, SPL, ATE, RPE|ScaleVLN [238]|4.9M trajectories|**Sim**|SR, SPL|
|**_Foundational reinforcement-l_**|**_earning benchmarks_**|||||||
|DMControl [239]|28 tasks|**Sim**|Return, Norm. Score|Craftax [240]|1 game|**Sim**|Return, Reward|
|Atari (ALE) [207]|55 games|**Sim**|HNS, IQM, Mean/Md.|DMLab [241]|—|**Sim**|Return|
|Atari 100k [242]|26 games / 100k steps|**Sim**|HNS, IQM|BSuite [243]|23 tasks|**Sim**|Return|
|Procgen [244]|16 games|**Sim**|Return, Reward|FMB [245]|—|**Real**|SR, Cycle Time|


CALVIN highlights long-horizon chain completion [8], [208], [209], [215]–[217], [220], [221]. Video-oriented WAM papers additionally report rollout fidelity metrics such as FVD, LPIPS, PSNR, and SSIM [13], [19], [20], [38], [103]. Thus, the simulated manipulation block in Tab. III should be read as a spectrum from policy evaluation to prediction-quality evaluation, rather than as a single interchangeable benchmark family. 

## _D. Autonomous Driving Datasets and Simulators_ 

Driving resources exhibit a clear separation between openloop prediction and closed-loop control. Recorded datasets such as nuScenes, Waymo Open Motion, BDD100K, KITTI, Argoverse, ZOD, and OpenDV support visual generation, trajectory prediction, occupancy forecasting, and perception evaluation [193], [194], [223], [225], [227], [228], [230]. By contrast, nuPlan-derived NAVSIM protocols, CARLA, and Bench2Drive primarily support closed-loop planning and policy assessment [204]–[206], [224], [226]. Tab. III makes this split explicit through its mix of real, simulated, and mixed resources. For driving WAMs, metric choice strongly determines the interpretation of progress. FID, FVD, and LPIPS assess whether generated traffic videos look realistic [196], [197], [199]; ADE/FDE, L2, mIoU, mAP, and NDS assess structured prediction [194], [223], [227]; and DS, RC, IS, PDMS, TTC, comfort, and collision-related metrics assess planning utility and safety [204]–[206], [226]. A driving WAM should therefore not be judged by video realism alone. The driving block in Tab. III illustrates how metrics for video realism, structured scene prediction, and closed-loop safety should be combined. 

## _E. Navigation Environments, Datasets, and Benchmarks_ 

Navigation resources usually combine a 3D environment with an instruction, point-goal, image-goal, or real-trajectory protocol. Matterport3D-style scans and Habitat-style simulation provide the spatial substrate, while R2R/R2R-CE, RxR/RxR-CE, and ScaleVLN define instruction-following and data-scaling settings [191], [231], [233], [235], [237], [238]. Real-robot or field datasets such as RECON [232], SCAND [236], CoPeD [246], and TartanDrive [234] complement these simulated protocols by exposing social, offroad, multi agent or platform-specific dynamics. Their reported scales and typical evaluation measures are summarized in Tab. III. For WAMs, navigation evaluation should capture more than successful arrival. SR measures task completion, SPL and path length reflect efficiency, NE and nDTW capture route fidelity, and ATE/RPE assess pose consistency when prediction or mapping is involved [190], [192], [195]. This metric family is particularly relevant for look-ahead WAMs, where predicted egocentric views or latent states may improve waypoint selection even when the model does not generate photorealistic future frames [2], [166], [167], [169]. 

## _F. Foundational RL Benchmarks_ 

Foundational RL benchmarks predate recent WAMs for robotics, but they remain useful diagnostic settings for latent dynamics, imagined rollouts, sample efficiency, and generalization. As shown in Tab. III, DMControl and Atari-style protocols respectively test continuous and discrete control under compact task suites; Atari 100k emphasizes sample efficiency; Procgen, Craftax, and DMLab stress generalization and longhorizon exploration; and BSuite provides targeted diagnostics 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

14 

for core RL capabilities [207], [239]–[244]. These benchmarks are not substitutes for embodied robot evaluation because they abstract away many sensing, contact, embodiment, and safety constraints. Their role is instead methodological: they help establish whether a predictive model supports planning, value learning, or policy improvement before the same ideas are transferred to manipulation, navigation, or driving [1], [18], [26], [50], [58]. FMB is an important bridge case because it reports real-world manipulation success and cycle time, linking RL-style evaluation back to physical execution [245]. 

## VI. OPEN CHALLENGES AND FUTURE DIRECTIONS 

WAMs integrate perception, prediction, and action generation into a unified framework, posing a challenging multiobjective optimization problem for their design and training. Their development currently faces four major bottlenecks: action grounding, spatial consistency, closed-loop policy improvement, and real-time inference. 

## _A. Decoupling Motion Intent and Action Alignment_ 

Compared with conventional VLA policies [11], [16], WAMs [19], [21], [23] decouple task-level motion reasoning from low-level robot control. This separation raises two central challenges under the imbalance between visual and action data: staged optimization of motion intent (‘what to happen’) learning and action alignment (‘how to act’), and preservation of pretrained visual priors. 

_1) Stage-wise Motion-to-Action Alignment:_ IDM-style WAMs [23]–[25] are often well suited to staged optimization. A common strategy is to pretrain video foundation models [76], [77] on large-scale visual data to capture spatiotemporal dynamics, and then adapt them with embodied data to align predicted motion to executable actions. _2) Prior Preservation during Action Alignment:_ A second challenge is preserving pretrained visual priors during action alignment. Parameter freezing, action-alignment layers, and residual action heads can confine control-specific updates. Additionally, stronger anti-forgetting mechanisms may help retain the broad knowledge acquired during large-scale pretraining. 

## _B. World–Action Factorization_ 

From the agent–environment perspective widely studied in reinforcement learning [247], world prediction and action selection are related but fundamentally different problems. The former models action-conditioned state transitions and prioritizes predictive fidelity, whereas the latter maps states to actions and maximizes cumulative rewards. Their joint trajectory distribution naturally factorizes as 


_1) Decoupled Learning Objectives:_ World–action factorization separately trains the world and agent models according to their natural objectives [49], [248]. The world model focuses on accurate simulation, while the agent model optimizes action selection. By contrast, joint optimization may encourage a monolithic WAM to generate overly optimistic states that are easily exploited by its policy, potentially degrading real-world performance. 

_2) Decoupled Learning and Inference:_ Separating the two models also enables continual training and flexible inference. The world model can serve as a simulator for offline reinforcement learning, runtime planning, and model predictive control. Although this direction has shown promising results [248], controlling model bias and coordinating the two components remain important challenges. 

## _C. Spatial and Multi-View Consistency_ 

Robotic control requires more than single-view 2D prediction. Current video backbones often struggle to enforce geometric constraints, maintain object permanence, and ensure cross-view consistency. These limitations can degrade state estimation, planning, and inverse-dynamics decoding in manipulation and autonomous driving. 

_1) Explicit 3D Spatial Representations:_ Structured 3D prediction offers a more control-relevant alternative to independent view generation. Representative choices include point clouds [157], occupancy fields [249], and 3D Gaussian representations [250]. The main challenge is to integrate them with scalable generative backbones and efficient action decoding. 

_2) Egocentric Observations:_ Egocentric videos provide rich cues about manipulation intent and hand-object dynamics [144], [149]. With fixed inter-camera extrinsics, it also tends to offer stronger multi-view consistency [251]. 

## _D. Long-Horizon Memory_ 

Long-horizon tasks require agents to retain task progress, past interactions, and occluded information. Simply extending the observation window is computationally expensive and introduces redundant visual context, motivating compact and selective memory mechanisms. 

_1) Model-Integrated Memory Architectures:_ MEM [252] combines video-based short-term memory with text-based long-term memory. EventVLA [253] selectively stores taskcritical visual events, while MemoryVAM [254] injects episodic memory into both video prediction and action decoding. However, such methods often require architecture-specific training. 

_2) Memory-Augmented Agentic Harnesses:_ Harness VLA [255] externalizes memory management by combining a frozen VLA with an agentic planner that maintains execution traces, success rules, and failure models. This modular design supports planning, verification, and failure recovery without modifying the underlying policy, offering a promising direction for scalable long-horizon memory. 

15 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

## _E. Neural Simulators and Closed-Loop Policy Learning_ 

Imitation learning [8] can approximate expert state-action distributions, but its closed-loop correction capability remains limited and it relies heavily on high-quality expert demonstrations. Low-quality or failed demonstrations are typically discarded, and training skilled teleoperators is costly. Moreover, current imitation learning methods have limited ability to improve from failure, motivating closed-loop policy learning [256]. 

_1) Neural Simulators:_ Neural simulators based on RSSMstyle models [1], [55] learn action-conditioned dynamics that serve as predictive environments for policy evaluation and improvement [257], although prediction errors accumulated during imagination can introduce model bias and complicate long-horizon policy optimization [258]. 

_2) Closed-Loop Policy Learning:_ Reinforcement learning in real systems is often constrained by sample inefficiency, while simulation-based learning suffers from the sim2real gap. Neural simulators enable policy optimization through imagined interactions using task rewards [1], [50], goal-based objectives [74], [75], or learned reward models [124], [125], where long-horizon credit assignment is critical for improving policies from predicted futures [259]. Self-supervised reinforcement learning (SSL-RL) [260], [261] may replace the IDM-based action expert in dual systems (Section III-C), but reward-free and offline learning remain key challenges at scale. 

manipulation, navigation, autonomous driving, and generalist embodied robotics. Useful predictions must be grounded in robot actions, preserve spatial and temporal consistency, expose uncertainty, support closed-loop improvement, and satisfy real-time constraints. Progress will therefore depend on tighter coupling among multimodal and 3D world representations, action-alignment mechanisms, neural simulation, reinforcement learning, and real-robot feedback, together with benchmarks that measure task success, safety, robustness, and embodiment transfer. 

## REFERENCES 

- [1] N. Hansen, H. Su, and X. Wang, “Temporal difference learning for model predictive control,” in _ICML_ , 2022, pp. 8387–8406. 

- [2] J. Y. Koh, H. Lee, Y. Yang _et al._ , “Pathdreamer: A world model for indoor navigation,” in _ICCV_ , 2021, pp. 14 718–14 728. 

- [3] P. Wu, A. Escontrela, D. Hafner _et al._ , “Daydreamer: World models for physical robot learning,” in _CoRL_ , 2022, pp. 2226–2240. 

- [4] R. Rombach, A. Blattmann, D. Lorenz _et al._ , “High-resolution image synthesis with latent diffusion models,” in _CVPR_ , 2022, pp. 10 674– 10 685. 

- [5] X. Liu, C. Gong, and Q. Liu, “Flow straight and fast: Learning to generate and transfer data with rectified flow,” in _ICLR_ , 2023. 

- [6] B. Zitkovich, T. Yu, S. Xu _et al._ , “RT-2: vision-language-action models transfer web knowledge to robotic control,” in _CoRL_ , 2023, pp. 2165– 2183. 

- [7] A. Brohan, N. Brown, J. Carbajal _et al._ , “RT-1: robotics transformer for real-world control at scale,” in _RSS_ , 2023. 

- [8] C. Chi, Z. Xu, S. Feng _et al._ , “Diffusion policy: Visuomotor policy learning via action diffusion,” _IJRR_ , vol. 44, no. 10-11, pp. 1684–1704, 2025. 

- [9] V. Micheli, E. Alonso, and F. Fleuret, “Transformers are sampleefficient world models,” in _ICLR_ , 2023. 

## _F. Inference Latency and Computational Efficiency_ 

As WAMs scale, inference latency becomes a control bottleneck. Multi-step sampling, rollout generation, and action decoding can delay feedback in dynamic or contact-rich systems. Efficiency is therefore a control requirement, not only an implementation detail. 

_1) Few-Step Action Generation:_ Few-step generation is essential for real-time WAMs [262]. Consistency models [263], mean-flow [264], rectified-flow [5], and related methods can reduce sampling cost, but these acceleration methods must preserve action-conditioned transitions, temporal consistency, and control-relevant state information. 

_2) Deployment Optimization:_ System-level optimizations such as quantization, pruning, operator fusion, batching, memory-layout optimization [265], distillation [266], [267], and KV-cache reuse [23] are essential. Overall efficiency also depends on rollout horizon, imagined-trajectory count, replanning frequency, and action-decoding cost, which should be reduced without compromising control fidelity [268]. 

## VII. CONCLUSION 

World-Action Models (WAMs) aim to close the gap between predictive world modeling and executable robot control. By conditioning future-state prediction on actions and using the resulting predictions for action selection, policy learning, or inverse-dynamics decoding, WAMs extend beyond VLA policies. This survey reviewed this emerging class from a robotics perspective, organized its main design choices into a unified taxonomy, and related representative methods to 

- [10] D. Driess, F. Xia, M. S. M. Sajjadi _et al._ , “Palm-e: An embodied multimodal language model,” in _ICML_ , 2023, pp. 8469–8488. 

- [11] M. J. Kim, K. Pertsch, S. Karamcheti _et al._ , “Openvla: An open-source vision-language-action model,” in _CoRL_ , 2024, pp. 2679–2713. 

- [12] D. Ghosh, H. R. Walke, K. Pertsch _et al._ , “Octo: An open-source generalist robot policy,” in _RSS_ , 2024. 

- [13] H. Wu, Y. Jing, C. Cheang _et al._ , “Unleashing large-scale video generative pre-training for visual robot manipulation,” in _ICLR_ , 2024. 

- [14] J. Bruce, M. D. Dennis, A. Edwards _et al._ , “Genie: Generative interactive environments,” in _ICML_ , 2024, pp. 4603–4623. 

- [15] OpenAI, “Video generation models as world simulators,” _Technical Report_ , 2024. [Online]. Available: https://openai.com/research/ video-generation-models-as-world-simulators 

- [16] K. Black, N. Brown, D. Driess _et al._ , “ _pi_ <u>0: A Vision-Language-Action</u> Flow Model for General Robot Control,” in _RSS_ , 2025. 

- [17] J. Xiang, Y. Gu, Z. Liu _et al._ , “Pan: A world model for general, interactable, and long-horizon world simulation,” _arXiv:2511.09057_ , 2025. 

- [18] D. Hafner, J. Pasukonis, J. Ba _et al._ , “Mastering diverse control tasks through world models,” _Nature_ , vol. 640, pp. 647–653, 2025. 

- [19] C. Zhu, R. Yu, S. Feng _et al._ , “Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets,” _arXiv:2504.02792_ , 2025. 

- [20] Y. Hu, Y. Guo, P. Wang _et al._ , “Video prediction policy: A generalist robot policy with predictive visual representations,” in _ICML_ , 2025. 

- [21] M. J. Kim, Y. Gao, T.-Y. Lin _et al._ , “Cosmos policy: Fine-tuning video models for visuomotor control and planning,” _arXiv:2601.16163_ , 2026. 

- [22] T. Yuan, Z. Dong, Y. Liu _et al._ , “Fast-wam: Do world action models need test-time future imagination?” _arXiv:2603.16666_ , 2026. 

- [23] S. Ye, Y. Ge, K. Zheng _et al._ , “World action models are zero-shot policies,” in _ICLR Workshop_ , 2026. 

- [24] L. Li, Q. Zhang, Y. Luo _et al._ , “Causal world modeling for robot control,” _arXiv:2601.21998_ , 2026. 

- [25] A. Ye, B. Wang, C. Ni _et al._ , “Gigaworld-policy: An efficient actioncentered world–action model,” _arXiv:2603.17240_ , 2026. 

- [26] D. Hafner, T. P. Lillicrap, M. Norouzi _et al._ , “Mastering atari with discrete world models,” in _ICLR_ , 2021. 

- [27] R. Xu, J. Zhang, M. Guo _et al._ , “A0: An affordance-aware hierarchical model for general robotic manipulation,” in _ICCV_ , 2025, pp. 13 491– 13 501. 

16 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

- [28] C. Li, A. Krause, and M. Hutter, “Uncertainty-aware robotic world model makes offline model-based reinforcement learning work on real robots,” in _ICLR Workshop_ , 2026. 

- [29] D. Ha and J. Schmidhuber, “World models,” _arXiv:1803.10122_ , 2018. 

- [30] W. Tan, L. Zhu, B. Wang _et al._ , “Towards generalist embodied ai: A survey on world models for vla agents,” _TechRxiv_ , 2026. 

- [31] S. Thrun, W. Burgard, and D. Fox, _Probabilistic Robotics_ . Cambridge, Mass.: MIT Press, 2005. 

- [32] F. Dellaert and M. Kaess, “Factor graphs for robot perception,” _Foundations and Trends in Robotics_ , vol. 6, p. 1–139, 2017. 

- [33] T. D. Barfoot, _State estimation for robotics_ . Cambridge University Press, 2024. 

- [34] D. Silver and J. Veness, “Monte-carlo planning in large pomdps,” in _NeurIPS_ , 2010, pp. 2164–2172. 

- [35] T. Sugihara, Y. Nakamura, and H. Inoue, “Real-time humanoid motion generation through zmp manipulation based on inverted pendulum control,” in _ICRA_ , vol. 2, 2002, pp. 1404–1409. 

- [36] K. Black, N. Brown, J. Darpinian _et al._ , “ _π_ 0 _._ 5: a vision-language-action model with open-world generalization,” in _CoRL_ , vol. 305, 2025, pp. 17–40. 

- [37] R. Wang, J. Zhang, J. Chen _et al._ , “Dexgraspnet: A large-scale robotic dexterous grasp dataset for general objects based on simulation,” in _ICRA_ , 2023, pp. 11 359–11 366. 

- [38] C.-L. Cheang, G. Chen, Y. Jing _et al._ , “Gr-2: A generative videolanguage-action model with web-scale knowledge for robot manipulation,” _arXiv:2410.06158_ , 2024. 

- [39] J. Cen, C. Yu, H. Yuan _et al._ , “Worldvla: Towards autoregressive action world model,” _arXiv:2506.21539_ , 2025. 

- [40] X. Li, M. Liu, H. Zhang _et al._ , “Vision-language foundation models as effective robot imitators,” in _ICLR_ , 2024. 

- [41] S. Fei, S. Wang, J. Shi _et al._ , “Libero-plus: In-depth robustness analysis of vision-language-action models,” _arXiv:2510.13626_ , 2025. 

- [42] F. Li, W. Song, H. Zhao _et al._ , “Spatial forcing: Implicit spatial representation alignment for vision-language-action model,” in _ICLR_ , vol. 2026, 2026, pp. 132 324–132 345. 

- [43] I. Guzey, H. Qi, J. Urain _et al._ , “Dexterity from smart lenses: Multifingered robot manipulation with in-the-wild human demonstrations,” _arXiv:2511.16661_ , 2025. 

- [44] R. Punamiya, D. Patel, P. Aphiwetsa _et al._ , “Egobridge: Domain adaptation for generalizable imitation from egocentric human data,” in _NeurIPS_ , vol. 38, 2025, pp. 47 092–47 122. 

- [45] Y. Wang, Q. Zhao, Y. F. Lau _et al._ , “Humanx: Toward agile and generalizable humanoid interaction skills from human videos,” _arXiv:2602.02473_ , 2026. 

- [46] C. Zhang, J. Wang, Z. Gao _et al._ , “Clap: Contrastive latent action pretraining for learning vision-language-action models from human videos,” _arXiv:2601.04061_ , 2026. 

- [47] Z. Chen, J. Huo, Y. Chen _et al._ , “Robohorizon: An llm-assisted multi-view world model for long-horizon robotic manipulation,” _arXiv:2501.06605_ , 2025. 

- [48] R. Zhang, M. Zhang, J. Zhou _et al._ , “Mind-v: Hierarchical world model for long-horizon robotic manipulation with rl-based physical alignment,” _arXiv:2512.06628_ , 2025. 

- [49] E. Xing, M. Deng, and J. Hou, “Critique of world model,” _arXiv:2507.05169_ , 2025. 

- [50] D. Hafner, T. P. Lillicrap, J. Ba _et al._ , “Dream to control: Learning behaviors by latent imagination,” in _ICLR_ , 2020. 

- [51] E. Alonso, A. Jelley, V. Micheli _et al._ , “Diffusion for world modeling: Visual details matter in atari,” in _NeurIPS_ , 2024. 

- [52] M. Rigter, J. Yamada, and I. Posner, “World models via policy-guided trajectory diffusion,” _TMLR_ , vol. 2024, 2024. 

- [53] S. Gao, S. Zhou, Y. Du _et al._ , “Adaworld: Learning adaptable world models with latent actions,” in _ICML_ , 2025. 

- [54] C. Li, A. Krause, and M. Hutter, “Robotic world model: A neural network simulator for robust policy optimization in robotics,” in _NeurIPS Workshop_ , 2025. 

- [55] Y. Wang, R. Syed, F. Wu _et al._ , “Interactive world simulator for robot policy training and evaluation,” in _RSS Workshop_ , 2026. 

- [56] J. Quevedo, A. K. Sharma, Y. Sun _et al._ , “Worldgym: World model as an environment for policy evaluation,” in _ICLR_ , vol. 2026, 2026, pp. 78 932–78 957. 

- [57] Y. Guo, L. Shi, J. Chen _et al._ , “Ctrl-world: A controllable generative world model for robot manipulation,” in _ICLR_ , 2026, pp. 6121–6138. 

- [58] N. Hansen, H. Su, and X. Wang, “TD-MPC2: scalable, robust world models for continuous control,” in _ICLR_ , 2024. 

- [59] W. Zheng, W. Chen, Y. Huang _et al._ , “Occworld: Learning a 3d occupancy world model for autonomous driving,” in _ECCV_ , 2024, pp. 55–72. 

- [60] Y. Tian, S. Yang, J. Zeng _et al._ , “Predictive inverse dynamics models are scalable learners for robotic manipulation,” in _ICLR_ , 2025. 

- [61] G. Wang, P. Tang, X. Ren _et al._ , “Learning vision-language-action world models for autonomous driving,” _arXiv:2604.09059_ , 2026. 

- [62] G. Team, A. Ye, B. Wang _et al._ , “Gigabrain-0: A world model-powered vision-language-action model,” _arXiv:2510.19430_ , 2025. 

- [63] P. Intelligence, B. Ai, A. Amin _et al._ , “ _π_ 0 _._ 7: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities,” _arXiv:2604.15483_ , 2026. 

- [64] X. Liu, Z. Bai, H. Ci _et al._ , “World-vla-loop: Closed-loop learning of video world model and vla policy,” _arXiv:2602.06508_ , 2026. 

- [65] R. Wang, Q. Liu, Y. Deng _et al._ , “Eva: Aligning video world models with executable robot actions via inverse dynamics rewards,” _arXiv:2603.17808_ , 2026. 

- [66] Z. Jiang, K. Liu, Y. Qin _et al._ , “World4rl: Diffusion world models for policy refinement with reinforcement learning for robotic manipulation,” _arXiv:2509.19080_ , 2025. 

- [67] Y. Wen, J. Lin, Y. Zhu _et al._ , “Vidman: Exploiting implicit dynamics from video diffusion model for effective robot manipulation,” in _NeurIPS_ , 2024. 

- [68] A. Hu, L. Russell, H. Yeo _et al._ , “Gaia-1: A generative world model for autonomous driving,” _arXiv:2309.17080_ , 2023. 

- [69] Y. Liao, P. Zhou, S. Huang _et al._ , “Genie envisioner: A unified world foundation platform for robotic manipulation,” _arXiv:2508.05635_ , 2025. 

- [70] I. Team, D. Shen, G. Zhang _et al._ , “Inspatio-world: A real-time 4d world simulator via spatiotemporal autoregressive modeling,” _arXiv:2604.07209_ , 2026. 

- [71] T. Ma, J. Zheng, Z. Wang _et al._ , “Dit4dit: Jointly modeling video dynamics and actions for generalizable robot control,” _arXiv:2603.10448_ , 2026. 

- [72] L. P. Kaelbling, M. L. Littman, and A. R. Cassandra, “Planning and acting in partially observable stochastic domains,” _Artif. Intell._ , vol. 101, no. 1-2, pp. 99–134, 1998. 

- [73] D. Hafner, T. P. Lillicrap, I. Fischer _et al._ , “Learning latent dynamics for planning from pixels,” in _ICML_ , 2019, pp. 2555–2565. 

- [74] G. Zhou, H. Pan, Y. LeCun _et al._ , “DINO-WM: world models on pretrained visual features enable zero-shot planning,” in _ICML_ , 2025. 

- [75] L. Maes, Q. L. Lidec, D. Scieur _et al._ , “Leworldmodel: Stable end-to-end joint-embedding predictive architecture from pixels,” _arXiv:2603.19312_ , 2026. 

- [76] T. Wan, A. Wang, B. Ai _et al._ , “Wan: Open and advanced large-scale video generative models,” _arXiv:2503.20314_ , 2025. 

- [77] NVIDIA, :, A. Ali _et al._ , “World simulation with video foundation models for physical ai,” _arXiv:2511.00062_ , 2025. 

- [78] S. Ye, J. Jang, B. Jeon _et al._ , “Latent action pretraining from videos,” in _ICLR_ , 2025. 

- [79] NVIDIA, :, J. Bjorck _et al._ , “Gr00t n1: An open foundation model for generalist humanoid robots,” _arXiv:2503.14734_ , 2025. 

- [80] A. Radford, J. W. Kim, C. Hallacy _et al._ , “Learning transferable visual models from natural language supervision,” in _ICML_ , 2021, pp. 8748– 8763. 

- [81] C. Raffel, N. Shazeer, A. Roberts _et al._ , “Exploring the limits of transfer learning with a unified text-to-text transformer,” _JMLR_ , vol. 21, pp. 140:1–140:67, 2020. 

- [82] T. Brown, B. Mann, N. Ryder _et al._ , “Language models are few-shot learners,” in _NeurIPS_ , vol. 33, 2020, pp. 1877–1901. 

- [83] H. Touvron, T. Lavril, G. Izacard _et al._ , “Llama: Open and efficient foundation language models,” _arXiv:2302.13971_ , 2023. 

- [84] A. Blattmann, T. Dockhorn, S. Kulal _et al._ , “Stable video diffusion: Scaling latent video diffusion models to large datasets,” _arXiv:2311.15127_ , 2023. 

- [85] Z. Yang, J. Teng, W. Zheng _et al._ , “Cogvideox: Text-to-video diffusion models with an expert transformer,” in _ICLR_ , 2025. 

- [86] H. Zhang, F. Li, S. Liu _et al._ , “DINO: DETR with improved denoising anchor boxes for end-to-end object detection,” in _ICLR_ , 2023. 

- [87] M. Oquab, T. Darcet, T. Moutakanni _et al._ , “Dinov2: Learning robust visual features without supervision,” _TMLR_ , 2024. 

- [88] O. Sim´eoni, H. V. Vo, M. Seitzer _et al._ , “DINOv3,” _TMLR_ , 2026. [89] X. Zhai, B. Mustafa, A. Kolesnikov _et al._ , “Sigmoid loss for language image pre-training,” in _ICCV_ , 2023, pp. 11 941–11 952. 

- [90] L. Mur-Labadia, M. Muckley, A. Bar _et al._ , “V-jepa 2.1: Unlocking dense features in video self-supervised learning,” _arXiv preprint arXiv:2603.14482_ , 2026. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

17 

- [91] C. R. Qi, H. Su, K. Mo _et al._ , “Pointnet: Deep learning on point sets for 3d classification and segmentation,” in _CVPR_ , 2017, pp. 77–85. 

- [92] J. Huang, G. Huang, Z. Zhu _et al._ , “Bevdet: High-performance multicamera 3d object detection in bird-eye-view,” _arXiv:2112.11790_ , 2021. 

- [93] J. Bai, S. Bai, S. Yang _et al._ , “Qwen-vl: A versatile vision-language model for understanding, localization, text reading, and beyond,” _arXiv:2308.12966_ , 2023. 

- [94] S. Karamcheti, S. Nair, A. Balakrishna _et al._ , “Prismatic vlms: Investigating the design space of visually-conditioned language models,” in _ICML_ , 2024, pp. 23 123–23 144. 

- [95] L. Beyer, A. Steiner, A. S. Pinto _et al._ , “Paligemma: A versatile 3b vlm for transfer,” _arXiv:2407.07726_ , 2024. 

- [96] A. Van Den Oord, O. Vinyals _et al._ , “Neural discrete representation learning,” _NeurIPS_ , vol. 30, 2017. 

- [97] S. Routray, H. Pan, U. Jain _et al._ , “ViPRA: Video prediction for robot actions,” in _NeurIPS Workshop_ , 2025. 

- [98] S. Gao, W. Liang, K. Zheng _et al._ , “Dreamdojo: A generalist robot world model from large-scale human videos,” in _ICML_ , 2026. 

- [99] H. Bi, H. Tan, S. Xie _et al._ , “Motus: A unified latent action world model,” in _CVPR_ , 2026, pp. 35 101–35 113. 

- [100] W. Liang, L. Yu, L. Luo _et al._ , “Mixture-of-transformers: A sparse and scalable architecture for multi-modal foundation models,” _TMLR_ , vol. 2025, 2025. 

- [101] G. Vasan, Y. Wang, F. Shahriar _et al._ , “Revisiting sparse rewards for goal-reaching reinforcement learning,” _RLJ_ , vol. 4, pp. 1841–1854, 2024. 

- [102] P. Zhou, L. Chen, S. Chen _et al._ , “Act2goal: From world model to general goal-conditioned policy,” _arXiv:2512.23541_ , 2025. 

- [103] Y. Guo, Y. Hu, J. Zhang _et al._ , “Prediction with action: Visual policy learning via joint denoising process,” _NeurIPS_ , vol. 37, pp. 112 386– 112 410, 2024. 

- [104] G. Team, A. Kamath, J. Ferret _et al._ , “Gemma 3 technical report,” _arXiv:2503.19786_ , 2025. 

- [105] Z. Zhang, Z. Li, B. Rahmati _et al._ , “Do world action models generalize better than vlas? a robustness study,” _arXiv:2603.22078_ , 2026. 

- [106] J. Pai, L. Achenbach, V. Montesinos _et al._ , “mimic-video: Video-action models for generalizable robot control beyond vlas,” _arXiv:2512.15692_ , 2025. 

- [107] Y. Zhang, W. Zhang, Z. Qi _et al._ , “Imagewam: Do world action models really need video generation, or just image editing?” _arXiv:2606.19531_ , 2026. 

- [108] F. AI, “Helix: A vision-language-action model for generalist humanoid control,” https://www.figure.ai/news/helix, 2025. 

- [109] K. Pertsch, K. Stachowicz, B. Ichter _et al._ , “Fast: Efficient action tokenization for vision-language-action models,” _arXiv:2501.09747_ , 2025. 

- [110] Y. Gao, H. Guo, T. Hoang _et al._ , “Seedance 1.0: Exploring the boundaries of video generation models,” _arXiv:2506.09113_ , 2025. 

- [111] G. Wu, D. Huang, D. Bai _et al._ , “Moviedrive: Urban scene synthesis with multi-modal multi-view video diffusion transformer,” _arXiv:2508.14327_ , 2025. 

- [112] Y. Lin, J. He, S. Bao _et al._ , “Jepa-wam: Learning visionlanguage-action policies with joint-embedding world modeling,” _arXiv:2608.09381_ , 2026. 

- [113] J. Chen, K. Wang, K. Chen _et al._ , “Lawam: Latent world action models for efficient dynamics-aware robot policies,” _arXiv:2606.15768_ , 2026. 

- [114] M. J. Kim, C. Finn, and P. Liang, “Fine-tuning vision-language-action models: Optimizing speed and success,” _arXiv:2502.19645_ , 2025. 

- [115] J. Sun, W. Zhang, Z. Qi _et al._ , “Vla-jepa: Enhancing vision-languageaction model with latent world model,” _arXiv:2602.10098_ , 2026. 

- [116] E. J. Hu, Y. Shen, P. Wallis _et al._ , “Lora: Low-rank adaptation of large language models,” in _ICLR_ , 2022. 

- [117] G. Team, A. Ye, B. Wang _et al._ , “Gigaworld-0: World models as data engine to empower embodied ai,” _arXiv:2511.19861_ , 2025. 

- [118] NVIDIA, :, H. A. Alhaija _et al._ , “Cosmos-transfer1: Conditional world generation with adaptive multimodal control,” _arXiv:2503.14492_ , 2025. 

- [119] J. Jang, S. Ye, Z. Lin _et al._ , “Dreamgen: Unlocking generalization in robot learning through video world models,” in _9th Annual Conference on Robot Learning_ , 2025. 

- [120] Y. Shang, Z. Li, Y. Ma _et al._ , “Worldarena: A unified benchmark for evaluating perception and functional utility of embodied world models,” _arXiv:2602.08971_ , 2026. 

- [121] P. F. Christiano, J. Leike, T. Brown _et al._ , “Deep reinforcement learning from human preferences,” _NeurIPS_ , vol. 30, 2017. 

- [122] N. Stiennon, L. Ouyang, J. Wu _et al._ , “Learning to summarize with human feedback,” _NeurIPS_ , vol. 33, pp. 3008–3021, 2020. 

- [123] R. Agarwal, N. Vieillard, Y. Zhou _et al._ , “On-policy distillation of language models: Learning from self-generated mistakes,” in _ICLR_ , vol. 2024, 2024, pp. 21 246–21 263. 

- [124] P. Intelligence, A. Amin, R. Aniceto _et al._ , “ _π_ 0 _._ 6: a VLA That Learns From Experience,” _arXiv:2511.14759_ , 2025. 

- [125] G. Team, B. Wang, B. Li _et al._ , “Gigabrain-0.5 m*: a vla that learns from world model-based reinforcement learning,” _arXiv:2602.12099_ , 2026. 

- [126] C. Xu, J. T. Springenberg, M. Equi _et al._ , “Rl token: Bootstrapping online rl with vision-language-action models,” _arXiv preprint arXiv:2604.23073_ , 2026. 

- [127] J. Luo, Z. Hu, C. Xu _et al._ , “SERL: A software suite for sampleefficient robotic reinforcement learning,” in _ICRA_ , 2024, pp. 16 961– 16 969. 

- [128] L. Yang, Z. Jiang, C. Sheng _et al._ , “Wam-opd: On-policy distillation for world action models,” _arXiv:2608.22364_ , 2026. 

- [129] J. Chen, P. Jia, Q. Wuwu _et al._ , “Mv-wam: Manifold-aware world action model with value augmentation,” _arXiv:2606.21088_ , 2026. 

- [130] F. Zhu, Y. Zhengyang, Z. Hong _et al._ , “WMPO: World model-based policy optimization for vision-language-action models,” in _ICLR_ , 2026. 

- [131] H. Zhen, Z. Gao, Q. Sun _et al._ , “Action images: End-to-end policy learning via multiview video generation,” _arXiv:2604.06168_ , 2026. 

- [132] S. Huang, Q. Chen, X. Zhang _et al._ , “Particleformer: A 3d point cloud world model for multi-object, multi-material robotic manipulation,” in _CoRL_ , 2025. 

- [133] T. Yu, G. Lu, Z. Yang _et al._ , “Manigaussian++: General robotic bimanual manipulation with hierarchical gaussian world model,” in _IROS_ , 2025, pp. 12 232–12 239. 

- [134] Y. Yang, J. Mei, Y. Ma _et al._ , “Driving in the occupancy world: Visioncentric 4d occupancy forecasting and planning via world models for autonomous driving,” in _AAAI_ , 2025, pp. 9327–9335. 

- [135] G. Lu, B. Jia, P. Li _et al._ , “GWM: towards scalable gaussian world models for robotic manipulation,” in _ICCV_ , 2025, pp. 9263–9274. 

- [136] Y. Ma, Z. Xu, and I. King, “4dgs-wam: Bridging past and future with an object-centric world action model based on 4d gaussian splatting,” _arXiv:2608.25956_ , 2026. 

- [137] L. Yang, W. Song, X. Wang _et al._ , “4d-wam: Infusing spatiotemporal awareness into world action models through trajectory fields,” _arXiv:2608.08023_ , 2026. 

- [138] C. Xue, C. Zhang, W. Ma _et al._ , “Hitac-wam: A hierarchical tactile world action model for contact-rich robot manipulation,” _arXiv:2608.19574_ , 2026. 

- [139] H. He, Z. Yan, Q. Liu _et al._ , “Fawam: Force-aware world action models for closed-loop contact-rich manipulation,” _arXiv:2606.08555_ , 2026. 

- [140] Microsoft Research, “Advancing ai for the physical world,” https://www.microsoft.com/en-us/research/story/ advancing-ai-for-the-physical-world/. 

- [141] C. Zhang, P. Hao, X. Cao _et al._ , “Vtla: Vision-tactile-language-action model with preference learning for insertion manipulation,” _Biomim. Intell. Robot._ , p. 100333, 2026. 

- [142] F. Zhang and M. Gienger, “Learning robot manipulation from audio world models,” in _ICRA Workshop_ , 2026. 

- [143] C. Higuera, S. Arnaud, B. Boots _et al._ , “Visuo-tactile world models,” _arXiv:2602.06001_ , 2026. 

- [144] R. Hoque, P. Huang, D. J. Yoon _et al._ , “Egodex: Learning dexterous manipulation from large-scale egocentric video,” in _ICLR_ , 2026. 

- [145] K. Grauman, A. Westbury, E. Byrne _et al._ , “Ego4d: Around the world in 3, 000 hours of egocentric video,” in _CVPR_ , 2022, pp. 18 973–18 990. 

- [146] A. O’Neill, A. Rehman, A. Maddukuri _et al._ , “Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0,” in _ICRA_ , 2024, pp. 6892–6903. 

- [147] C. Chi, Z. Xu, C. Pan _et al._ , “Universal manipulation interface: In-thewild robot teaching without in-the-wild robots,” in _RSS_ , 2024. 

- [148] Y. Zou, C. Shi, W. Yu _et al._ , “Activeglasses: Learning manipulation with active vision from ego-centric human demonstration,” _arXiv:2604.08534_ , 2026. 

- [149] R. Zheng, D. Niu, Y. Xie _et al._ , “Egoscale: Scaling dexterous manipulation with diverse egocentric human data,” _arXiv:2602.16710_ , 2026. 

- [150] Dyna Robotics, “Dyna-2: A 1-million-hour scaling law for worldaction models,” Dyna Robotics, Official Research Report, 2026. [Online]. Available: https://www.dyna.co/dyna-2 

- [151] A. Khazatsky, K. Pertsch, S. Nair _et al._ , “DROID: A large-scale inthe-wild robot manipulation dataset,” in _RSS_ , 2024. 

- [152] H. R. Walke, K. Black, T. Z. Zhao _et al._ , “Bridgedata V2: A dataset for robot learning at scale,” in _CoRL_ , 2023, pp. 1723–1736. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

18 

- [153] J. Barreiros, A. Beaulieu, A. Bhat _et al._ , “A careful examination of large behavior models for multitask dexterous manipulation,” _Science Robotics_ , vol. 11, no. 113, 2026. 

- [154] J. Yang, K. Lin, J. Li _et al._ , “Rise: Self-improving robot policy with compositional world model,” _arXiv:2602.11075_ , 2026. 

- [155] Z. Zhang, H. Ren, Y. Sun _et al._ , “Towards practical world modelbased reinforcement learning for vision-language-action models,” in _ICLR Workshop_ , 2026. 

- [156] H. Qi, H. Yin, A. Zhu _et al._ , “Inference-time enhancement of generative robot policies via predictive world modeling,” _RA-L_ , vol. 11, no. 5, pp. 5534–5541, 2026. 

- [157] W. Huang, Y.-W. Chao, A. Mousavian _et al._ , “Pointworld: Scaling 3d world models for in-the-wild robotic manipulation,” _arXiv:2601.03782_ , 2026. 

- [158] W. Li, H. Zhao, Z. Yu _et al._ , “Pin-wm: Learning physics-informed world models for non-prehensile manipulation,” _arXiv:2504.16693_ , 2025. 

- [159] A. D. Vuong, T. V. Vo, A. Sohail _et al._ , “World2act: Latent action post-training from world model dynamics,” _arXiv:2603.10422_ , 2026. 

- [160] J. Rome, S. James, and S. Ramamoorthy, “Learning to unfold cloth: Scaling up world models to deformable object manipulation,” _arXiv:2602.16675_ , 2026. 

- [161] B. Tharwat, Y. Nasser, A. Abouzeid _et al._ , “Latent action pretraining through world modeling,” _arXiv:2509.18428_ , 2025. 

- [162] E. Y.-T. Jia, W. Yuan, T. Shi _et al._ , “Dreamplan: Efficient reinforcement fine-tuning of vision-language planners via video world models,” _arXiv:2603.16860_ , 2026. 

- [163] H. Kim, L. Pinto, and S. J. Kim, “Hierarchical latent action model,” in _ICLR Workshop_ , 2026. 

- [164] Z. Ge, P. Ding, B. Yin _et al._ , “Vampo: Policy optimization for improving visual dynamics in video action models,” _arXiv:2603.19370_ , 2026. 

- [165] J. Bardhan, P. Drozdik, J. Sivic _et al._ , “Persistent robot world models: Stabilizing multi-step rollouts via reinforcement learning,” _arXiv:2603.25685_ , 2026. 

- [166] S. Wang, Y. Wang, Z. Fan _et al._ , “Monodream: Monocular visionlanguage navigation with panoramic dreaming,” in _AAAI_ , 2026, pp. 10 074–10 082. 

- [167] H. Wang, W. Liang, L. V. Gool _et al._ , “Dreamwalker: Mental planning for continuous vision-language navigation,” in _ICCV_ , 2023, pp. 10 839– 10 849. 

- [168] W. Liu, H. Zhao, C. Li _et al._ , “X-MOBILITY: end-to-end generalizable navigation via world modeling,” in _ICRA_ , 2025, pp. 7569–7576. 

- [169] A. Bar, G. Zhou, D. Tran _et al._ , “Navigation world models,” in _CVPR_ . IEEE, Jun. 2025, pp. 15 791–15 801. 

- [170] M. Wei, C. Wan, P. Peng _et al._ , “Ground slow, move fast: A dualsystem foundation model for generalizable vision-language navigation,” in _ICLR_ , vol. 2026, 2026, pp. 12 380–12 396. 

- [171] P. Roth, J. Frey, C. Cadena _et al._ , “Learned Perceptive Forward Dynamics Model for Safe and Platform-aware Robotic Navigation,” in _RSS_ , 2025. 

- [172] C. Li, A. Krause, and M. Hutter, “Robotic world model: A neural network simulator for robust policy optimization in robotics,” in _CoRL Workshop_ , 2025. 

- [173] H. Lai, J. Cao, J. Xu _et al._ , “World model-based perception for visual legged locomotion,” in _ICRA_ . IEEE, 2025, pp. 11 531–11 537. 

- [174] X. Wang, Z. Zhu, G. Huang _et al._ , “Drivedreamer: Towards real-worlddrive world models for autonomous driving,” in _ECCV_ , 2024, pp. 55– 72. 

- [175] F. Jia, W. Mao, Y. Liu _et al._ , “Adriver-i: A general world model for autonomous driving,” _arXiv:2311.13549_ , 2023. 

- [176] Y. Chen, Y. Wang, and Z. Zhang, “Drivinggpt: Unifying driving world modeling and planning with multi-modal autoregressive transformers,” in _ICCV_ , 2025, pp. 26 890–26 900. 

- [177] G. Zhao, X. Wang, Z. Zhu _et al._ , “Drivedreamer-2: Llm-enhanced world models for diverse driving video generation,” in _AAAI_ , 2025, pp. 10 412–10 420. 

- [178] W. Zheng, Z. Xia, Y. Huang _et al._ , “Doe-1: Closed-loop autonomous driving with large world model,” _arXiv:2412.09627_ , 2024. 

- [179] L. Russell, A. Hu, L. Bertoni _et al._ , “Gaia-2: A controllable multi-view generative world model for autonomous driving,” _arXiv:2503.20523_ , 2025. 

- [180] J. Wei, S. Yuan, P. Li _et al._ , “Occllama: An occupancy-language-action generative world model for autonomous driving,” _arXiv:2409.03272_ , 2024. 

- [181] X. Hu, M. Jia, X. Guo _et al._ , “Drivingworld: Constructing world model for autonomous driving via video gpt,” in _ICPR_ , 2026, pp. 276–291. 

- [182] X. Wang and P. Peng, “Prophetdwm: A driving world model for rolling out future actions and videos,” _arXiv:2505.18650_ , 2025. 

- [183] Y. Zhou, H. Shao, L. Wang _et al._ , “Drivinggen: A comprehensive benchmark for generative video world models in autonomous driving,” in _ICLR_ , vol. 2026, 2026, pp. 103 502–103 524. 

- [184] F. Bartoccioni, E. Ramzi, V. Besnier _et al._ , “Vavim and vavam: Autonomous driving through video generative modeling,” _arXiv:2502.15672_ , 2025. 

- [185] T. Xia, Y. Li, L. Zhou _et al._ , “Drivelaw: Unifying planning and video generation in a latent driving world,” in _CVPR_ , 2026, pp. 39 701– 39 712. 

- [186] W. Huang, S. Zhang, Q. Huang _et al._ , “Automot: A unified visionlanguage-action model with asynchronous mixture -of-transformers for end-to-end autonomous driving,” in _ICML_ , 2026. 

- [187] P. Yang, Y. Zheng, D. Qian _et al._ , “Dreamerad: Efficient reinforcement learning via latent world model for autonomous driving,” _arXiv:2603.24587_ , 2026. 

- [188] Y. Zheng, P. Yang, Z. Xing _et al._ , “World4drive: End-to-end autonomous driving via intention-aware physical latent world model,” in _ICCV_ , 2025, pp. 28 632–28 642. 

- [189] Y. Li, S. Shang, W. Liu _et al._ , “Drivevla-w0: World models amplify data scaling law in autonomous driving,” in _ICLR_ , vol. 2026, 2026, pp. 7890–7911. 

- [190] P. Anderson, A. X. Chang, D. S. Chaplot _et al._ , “On evaluation of embodied navigation agents,” _arXiv:1807.06757_ , 2018. 

- [191] P. Anderson, Q. Wu, D. Teney _et al._ , “Vision-and-language navigation: Interpreting visually-grounded navigation instructions in real environments,” in _CVPR_ , 2018, pp. 3674–3683. 

- [192] G. Ilharco, V. Jain, A. Ku _et al._ , “General evaluation for instruction conditioned navigation using dynamic time warping,” _arXiv:1907.05446_ , 2019. 

- [193] M. Chang, J. Lambert, P. Sangkloy _et al._ , “Argoverse: 3d tracking and forecasting with rich maps,” in _CVPR_ , 2019, pp. 8748–8757. 

- [194] P. Sun, H. Kretzschmar, X. Dotiwalla _et al._ , “Scalability in perception for autonomous driving: Waymo open dataset,” in _CVPR_ , 2020. 

- [195] J. Sturm, N. Engelhard, F. Endres _et al._ , “A benchmark for the evaluation of RGB-D SLAM systems,” in _IROS_ , 2012, pp. 573–580. 

- [196] M. Heusel, H. Ramsauer, T. Unterthiner _et al._ , “GANs trained by a two time-scale update rule converge to a local nash equilibrium,” in _NeurIPS_ , 2017. 

- [197] T. Unterthiner, S. van Steenkiste, K. Kurach _et al._ , “Towards accurate generative models of video: A new metric & challenges,” _arXiv:1812.01717_ , 2018. 

- [198] Z. Wang, A. C. Bovik, H. R. Sheikh _et al._ , “Image quality assessment: From error visibility to structural similarity,” _IEEE Transactions on Image Processing_ , vol. 13, no. 4, pp. 600–612, 2004. 

- [199] R. Zhang, P. Isola, A. A. Efros _et al._ , “The unreasonable effectiveness of deep features as a perceptual metric,” in _CVPR_ , 2018, pp. 586–595. 

- [200] K. Papineni, S. Roukos, T. Ward _et al._ , “BLEU: A method for automatic evaluation of machine translation,” in _ACL_ , 2002, pp. 311–318. 

- [201] C.-Y. Lin, “ROUGE: A package for automatic evaluation of summaries,” in _Text Summarization Branches Out_ , 2004, pp. 74–81. 

- [202] R. Vedantam, C. L. Zitnick, and D. Parikh, “CIDEr: Consensus-based image description evaluation,” in _CVPR_ , 2015, pp. 4566–4575. 

- [203] S. Banerjee and A. Lavie, “METEOR: An automatic metric for mt evaluation with improved correlation with human judgments,” in _ACL Workshop on Intrinsic and Extrinsic Evaluation Measures for Machine Translation and/or Summarization_ , 2005, pp. 65–72. 

- [204] A. Dosovitskiy, G. Ros, F. Codevilla _et al._ , “CARLA: an open urban driving simulator,” in _CoRL_ , 2017, pp. 1–16. 

- [205] X. Jia, Z. Yang, Q. Li _et al._ , “Bench2drive: Towards multi-ability benchmarking of closed-loop end-to-end autonomous driving,” in _NeurIPS_ , 2024. 

- [206] D. Dauner, M. Hallgarten, T. Li _et al._ , “NAVSIM: data-driven non-reactive autonomous vehicle simulation and benchmarking,” in _NeurIPS_ , 2024. 

- [207] M. G. Bellemare, Y. Naddaf, J. Veness _et al._ , “The arcade learning environment: An evaluation platform for general agents,” _JAIR_ , vol. 47, pp. 253–279, 2013. 

- [208] B. Liu, Y. Zhu, C. Gao _et al._ , “LIBERO: benchmarking knowledge transfer for lifelong robot learning,” in _NeurIPS_ , 2023. 

- [209] O. Mees, L. Hermann, E. Rosete-Beas _et al._ , “CALVIN: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks,” _RA-L_ , vol. 7, no. 3, pp. 7327–7334, 2022. 

- [210] W. Kay, J. Carreira, K. Simonyan _et al._ , “The kinetics human action video dataset,” _arXiv:1705.06950_ , 2017. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

19 

- [211] Q. Bu, J. Cai, L. Chen _et al._ , “Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems,” in _IROS_ , 2025. 

- [212] A. Miech, D. Zhukov, J. Alayrac _et al._ , “Howto100m: Learning a textvideo embedding by watching hundred million narrated video clips,” in _ICCV_ , 2019, pp. 2630–2640. 

- [213] R. Goyal, S. Ebrahimi Kahou, V. Michalski _et al._ , “The” something something” video database for learning and evaluating visual common sense,” in _ICCV_ , 2017, pp. 5842–5850. 

- [214] A. Mandlekar, S. Nasiriany, B. Wen _et al._ , “Mimicgen: A data generation system for scalable robot learning using human demonstrations,” in _CoRL_ , 2023, pp. 1820–1864. 

- [215] S. James, Z. Ma, D. R. Arrojo _et al._ , “Rlbench: The robot learning benchmark & learning environment,” _RA-L_ , vol. 5, no. 2, pp. 3019– 3026, 2020. 

- [216] T. Yu, D. Quillen, Z. He _et al._ , “Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning,” in _CoRL_ , 2019, pp. 1094–1100. 

- [217] T. Mu, Z. Ling, F. Xiang _et al._ , “Maniskill: Generalizable manipulation skill benchmark with large-scale demonstrations,” in _NeurIPS Datasets and Benchmarks_ , 2021. 

- [218] Y. Mu, T. Chen, Z. Chen _et al._ , “Robotwin: Dual-arm robot benchmark with generative digital twins,” in _CVPR_ , 2025, pp. 27 649–27 660. 

- [219] T. Chen, Z. Chen, B. Chen _et al._ , “Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation,” in _ICML_ , 2026. 

- [220] X. Li, K. Hsu, J. Gu _et al._ , “Evaluating real-world robot manipulation policies in simulation,” in _CoRL_ , 2024, pp. 3705–3728. 

- [221] S. Nasiriany, A. Maddukuri, L. Zhang _et al._ , “Robocasa: Large-scale simulation of everyday tasks for generalist robots,” in _RSS_ , 2024. 

- [222] T. Chen, Y. Chen, Z. Li _et al._ , “RoboDojo: A unified sim-and-real benchmark for comprehensive evaluation of generalist robot manipulation policies,” _arXiv:2607.04434_ , 2026. 

- [223] H. Caesar, V. Bankiti, A. H. Lang _et al._ , “nuscenes: A multimodal dataset for autonomous driving,” in _CVPR_ , 2020, pp. 11 618–11 628. 

- [224] K. T. e. a. H. Caesar, J. Kabzan, “Nuplan: A closed-loop ml-based planning benchmark for autonomous vehicles,” in _CVPR ADP3 workshop_ , 2021. 

- [225] J. Yang, S. Gao, Y. Qiu _et al._ , “Generalized predictive model for autonomous driving,” in _CVPR_ , 2024, pp. 14 662–14 672. 

- [226] W. Cao, M. Hallgarten, T. Li _et al._ , “Pseudo-simulation for autonomous driving,” in _CoRL_ , 2025. 

- [227] F. Yu, H. Chen, X. Wang _et al._ , “BDD100K: A diverse driving dataset for heterogeneous multitask learning,” in _CVPR_ , 2020, pp. 2633–2642. 

- [228] A. Geiger, P. Lenz, and R. Urtasun, “Are we ready for autonomous driving? the KITTI vision benchmark suite,” in _CVPR_ , 2012, pp. 3354– 3361. 

- [229] OpenScene Contributors, “OpenScene: The largest up-to-date 3d occupancy prediction benchmark in autonomous driving,” https://github. com/OpenDriveLab/OpenScene, 2023. 

- [230] M. Alibeigi, W. Ljungbergh, A. Tonderski _et al._ , “Zenseact open dataset: A large-scale and diverse multimodal dataset for autonomous driving,” in _ICCV_ , 2023, pp. 20 121–20 131. 

- [231] A. X. Chang, A. Dai, T. A. Funkhouser _et al._ , “Matterport3d: Learning from RGB-D data in indoor environments,” in _3DV_ , 2017, pp. 667–676. 

- [232] D. Shah, B. Eysenbach, N. Rhinehart _et al._ , “Rapid exploration for open-world navigation with latent goal models,” in _CoRL_ , 2021, pp. 674–684. 

- [233] J. Krantz, E. Wijmans, A. Majumdar _et al._ , “Beyond the nav-graph: Vision-and-language navigation in continuous environments,” in _ECCV_ , 2020, pp. 104–120. 

- [234] S. Triest, M. Sivaprakasam, S. J. Wang _et al._ , “Tartandrive: A largescale dataset for learning off-road dynamics models,” in _ICRA_ , 2022, pp. 2546–2552. 

- [235] A. Ku, P. Anderson, R. Patel _et al._ , “Room-Across-Room: Multilingual vision-and-language navigation with dense spatiotemporal grounding,” in _EMNLP_ , 2020. 

- [236] H. Karnan, A. Nair, X. Xiao _et al._ , “Socially compliant navigation dataset (SCAND): A large-scale dataset of demonstrations for social navigation,” _RA-L_ , vol. 7, no. 4, pp. 11 807–11 814, 2022. 

   - [240] M. T. Matthews, M. Beukman, B. Ellis _et al._ , “Craftax: A lightning-fast benchmark for open-ended reinforcement learning,” in _ICML_ , 2024, pp. 35 104–35 137. 

   - [241] X. Zhai, J. Puigcerver, A. Kolesnikov _et al._ , “The visual task adaptation benchmark,” _arXiv:1910.04867_ , 2019. 

   - [242] L. Kaiser, M. Babaeizadeh, P. Milos _et al._ , “Model based reinforcement learning for atari,” in _ICLR_ , 2020. 

   - [243] I. Osband, Y. Doron, M. Hessel _et al._ , “Behaviour suite for reinforcement learning,” in _ICLR_ , 2020. 

   - [244] K. Cobbe, C. Hesse, J. Hilton _et al._ , “Leveraging procedural generation to benchmark reinforcement learning,” in _ICML_ , 2020, pp. 2048–2056. 

   - [245] J. Luo, C. Xu, F. Liu _et al._ , “FMB: A functional manipulation benchmark for generalizable robotic learning,” _IJRR_ , vol. 44, no. 4, pp. 592–606, 2025. 

   - [246] Y. Zhou, L. Quang, C. Nieto-Granda _et al._ , “Coped-advancing multirobot collaborative perception: A comprehensive dataset in real-world environments,” _RA-L_ , vol. 9, no. 7, p. 6416–6423, 2024. 

   - [247] R. S. Sutton, A. G. Barto, and A. Barto, _Reinforcement learning: An introduction_ . MIT press Cambridge, 1998, vol. 1, no. 1. 

   - [248] E. Xing, M. Deng, and J. Hou, “Critique of agent model,” _arXiv:2606.23991_ , 2026. 

   - [249] L. L. Bailey, D. I. MacKenzie, and J. D. Nichols, “Advances and applications of occupancy models,” _Methods Ecol. Evol._ , vol. 5, no. 12, pp. 1269–1279, 2014. 

   - [250] B. Kerbl, G. Kopanas, T. Leimk¨uhler _et al._ , “3d gaussian splatting for real-time radiance field rendering,” _ACM TOG_ , vol. 42, no. 4, pp. 139:1–139:14, 2023. 

   - [251] B. Huang, B. Wei, Y. Cai _et al._ , “Selective cross-view consistency for world action models: Held-out viewpoint robustness without test-time camera information,” _arXiv:2608.21402_ , 2026. 

   - [252] M. Torne, K. Pertsch, H. Walke _et al._ , “Mem: Multi-scale embodied memory for vision language action models,” _arXiv:2603.03596_ , 2026. 

   - [253] G. Yang, Z. Tu, Y. Yang _et al._ , “Eventvla: Event-driven visual evidence memory for long-horizon vision-language-action policies,” _arXiv:2606.20092_ , 2026. 

   - [254] Y. Jiang, C. Yu, Y. Chen _et al._ , “Memoryvam: Integrating memory into video action model for robot manipulation,” _arXiv:2606.20679_ , 2026. 

   - [255] Y. Zhang, H. Zhang, F. Gao _et al._ , “Harness vla: Steering frozen vlas into reliable manipulation primitives via memory-guided agents,” _arXiv:2607.08448_ , 2026. 

   - [256] K. Chen, Z. Liu, T. Zhang _et al._ , “ _π_ RL: Online RL Fine-tuning for Flowbased Vision-Language-Action Models,” _arXiv:2510.25889_ , 2025. 

   - [257] H. Bi, Z. Zhou, Y. Tang _et al._ , “Motus2: A self-evolving general world model for dexterous manipulation,” _arXiv:2608.30237_ , 2026. 

   - [258] M. Janner, J. Fu, M. Zhang _et al._ , “When to trust your model: Modelbased policy optimization,” _NeurIPS_ , vol. 32, 2019. 

   - [259] Z. Jiang, S. Zhou, Y. Jiang _et al._ , “Wovr: World models as reliable simulators for post-training vla policies with rl,” _arXiv:2602.13977_ , 2026. 

   - [260] B. Eysenbach, J. Ibarz, A. Gupta _et al._ , “Diversity is all you need: Learning skills without a reward function,” in _ICLR_ , 2019. 

   - [261] B. Eysenbach, T. Zhang, S. Levine _et al._ , “Contrastive learning as goalconditioned reinforcement learning,” _Advances in Neural Information Processing Systems_ , vol. 35, pp. 35 603–35 620, 2022. 

   - [262] Y. Sun, G. Zhuge, K. Liu _et al._ , “Sants: A state-adaptive scheduler for world action models,” _arXiv:2605.27947_ , 2026. 

   - [263] Y. Song, P. Dhariwal, M. Chen _et al._ , “Consistency models,” in _ICML_ , vol. 202, 23–29 Jul 2023, pp. 32 211–32 252. 

   - [264] Z. Geng, M. Deng, X. Bai _et al._ , “Mean flows for one-step generative modeling,” in _NeurIPS_ , vol. 38, 2025, pp. 75 460–75 482. 

   - [265] C. Wang, D. Xu, D. Cai _et al._ , “Phyai: Real-time physical ai at the edge, scalable rollouts in the cloud,” _arXiv:2608.03682_ , 2026. 

   - [266] T. Yin, M. Gharbi, R. Zhang _et al._ , “One-step diffusion with distribution matching distillation,” in _CVPR_ , 2024, pp. 6613–6623. 

   - [267] T. Yin, M. Gharbi, T. Park _et al._ , “Improved distribution matching distillation for fast image synthesis,” _NeurIPS_ , vol. 37, pp. 47 455– 47 487, 2024. 

   - [268] P. Li, R. Zhang, R. Zhang _et al._ , “Fbfm: A training-free asynchronous feedback mechanism for flow-matching in world-action models execution,” _arXiv:2607.29235_ , 2026. 

- [237] M. Savva, J. Malik, D. Parikh _et al._ , “Habitat: A platform for embodied AI research,” in _ICCV_ , 2019, pp. 9338–9346. 

- [238] Z. Wang, J. Li, Y. Hong _et al._ , “Scaling data generation in vision-andlanguage navigation,” in _ICCV_ , 2023, pp. 11 975–11 986. 

- [239] Y. Tassa, Y. Doron, A. Muldal _et al._ , “Deepmind control suite,” _arXiv:1801.00690_ , 2018. 

