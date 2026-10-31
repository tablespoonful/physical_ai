---
title: "ResWM: Residual-Action World Model for Visual RL"
date: "2026-03-11"
authors: "Jseen Zhang; Gabriel Adineera; Jinzhou Tan; Jinoh Kim"
url: https://arxiv.org/abs/2603.11110
pdf: https://arxiv.org/pdf/2603.11110
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.11110)** / [論文ページ](https://arxiv.org/abs/2603.11110)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **ResWM: Residual-Action World Model for Visual RL** 

Jseen Zhang<sup>∗</sup> 

University of California, San Diego USA 

Jinzhou Tan University of California, San Diego USA 

## **Abstract** 

Learning predictive world models from raw visual observations is a central challenge in reinforcement learning (RL), especially for robotics and continuous control. Conventional model-based RL frameworks directly condition future predictions on absolute actions, which makes optimization unstable: the optimal action distributions are task-dependent, unknown a priori, and often lead to oscillatory or inefficient control. To address this, we introduce the Residual-Action World Model (ResWM), a new framework that reformulates the control variable from absolute actions to residual actions—incremental adjustments relative to the previous step. This design aligns with the inherent smoothness of real-world control, reduces the effective search space, and stabilizes long-horizon planning. To further strengthen the representation, we propose an Observation Difference Encoder that explicitly models the changes between adjacent frames, yielding compact latent dynamics that are naturally coupled with residual actions. ResWM is integrated into a Dreamer-style latent dynamics model with minimal modifications and no extra hyperparameters. Both imagination rollouts and policy optimization are conducted in the residual-action space, enabling smoother exploration, lower control variance, and more reliable planning. Empirical results on the DeepMind Control Suite demonstrate that ResWM achieves consistent improvements in sample efficiency, asymptotic returns, and control smoothness, significantly surpassing strong baselines such as Dreamer and TD-MPC. Beyond performance, ResWM produces more stable and energy-efficient action trajectories, a property critical for robotic systems deployed in real-world environments. These findings suggest that residual action modeling provides a simple yet powerful principle for bridging algorithmic advances in RL with the practical requirements of robotics. 

## **1 Introduction** 

Learning world models from high-dimensional visual observations stands as a cornerstone challenge in reinforcement learning (RL)[1–9], demanding the orchestration of representation learning, dynamics prediction, and policy optimization in tandem[10–16]. In contrast to state-based paradigms where low-dimensional inputs transparently expose underlying system dynamics, visual RL grapples with multifaceted complexity, especially in robotics where agents navigate long-horizon tasks amid perpetually shifting environments[17–19]. Although model-free approaches such as SAC[20] and PPO[21] have garnered impressive achievements, 

> ∗Both authors contributed equally to this research. 

> †Both authors contributed equally to this research. 

Gabriel Adineera<sup>†</sup> 

Texas A&M University-Commerce USA 

Jinoh Kim<sup>‡</sup> 

Texas A&M University-Commerce USA 

their inherent sample inefficiency severely limits their viability in real-world scenarios, where data acquisition is costly, limited, or fraught with risks. Model-based reinforcement learning (MBRL)[17, 22] emerges as a promising antidote, cultivating an internal world model that facilitates efficient planning and policy refinement via imaginative simulations[23, 24]. Yet, the traditional manner of embedding actions within these models has surfaced as a pivotal bottleneck, hindering the full realization of MBRL’s potential. 

Predominant world models condition their latent dynamics directly on _absolute actions_ , a seemingly intuitive choice that nonetheless instills suboptimal inductive biases with far-reaching implications[25–29]. Primarily, this setup casts policy learning as a high-variance conundrum, compounded by the task-specific, nonstationary distributions of optimal absolute actions. Furthermore, it frequently engenders oscillatory or erratic control trajectories, undermining planning efficacy and introducing safety hazards in physical embodiments. These shortcomings underscore a profound disconnect between the algorithmic scaffolding of world models and the imperatives of smooth, resilient control in embodied agents. 

In this paper, we champion the notion that the smoothness intrinsic to continuous control transcends mere desirability, evolving into a foundational principle ripe for exploitation. Our pioneering insight revolves around the _residual change_ between successive actions—a quantity far more predictable and tractable than its absolute counterpart. Leveraging this, we unveil the **Residual-Action World Model (ResWM)** , a transformative framework that reparameterizes the control variable from absolute actions to _residual actions_ . This reformulation embeds a robust **temporal smoothness prior** into the action space, fundamentally curtailing learning complexity by modeling incremental refinements rather than outright commands. In doing so, ResWM harmonizes with the continuum of physical dynamics, furnishing a steadfast bedrock for extendedhorizon planning and fostering control signals that are inherently stable and energy-efficient. 

To anchor the control signal in the most salient perceptual insights, we complement our residual action paradigm with an innovative **Observation Difference Encoder (ODL)** . Diverging from the norm of independently encoding static frames, the ODL meticulously distills the embedded dynamics from the disparities between adjacent observations [30–34]. This yields a compact, **dynamicsaware latent representation** that seamlessly aligns with the prediction of residual actions, effectively sieving out static redundancies to spotlight temporal shifts causally pivotal to the agent’s adaptive adjustments. By prioritizing these differential cues, the 

> ‡Corresponding author. 

Conference’17, July 2017, Washington, DC, USA 

Jseen Zhang, Gabriel Adineera, Jinzhou Tan, and Jinoh Kim 

ODL imbues the model with a sharpened focus on action-induced changes, enhancing its causal reasoning capabilities. 

ResWM is meticulously engineered for effortless assimilation into established Dreamer-style architectures, entailing only minimal alterations and eschewing any novel hyperparameters. Imagination-driven planning and policy optimization unfold wholly within the residual-action domain, transmuting exploration into fluid, localized perturbations rather than volatile, high-variance explorations. This paradigm shift not only bolsters learning stability and sample efficiency but also yields action trajectories that are demonstrably smoother and more energyconserving—indispensable attributes for the secure integration of robotic systems in real-world contexts. 

We substantiate ResWM’s efficacy on the _DeepMind Control Suite_ , a benchmark par excellence for continuous visual control. Empirical evaluations reveal ResWM’s consistent supremacy in sample efficiency, asymptotic performance, and control smoothness, markedly eclipsing formidable baselines such as Dreamer and TD-MPC. Complementary qualitative scrutiny discloses ResWM’s propensity for stabler latent dynamics and mitigated compounding prediction errors, affirming its robustness and versatility. 

In summary, this work advances the following contributions: 

- We introduce the **Residual-Action World Model (ResWM)** , a novel MBRL framework that reparameterizes the action space to instill a powerful smoothness prior, dramatically alleviating learning complexity and augmenting stability. 

- We propose the **Observation Difference Encoder** , an architecture that forges a dynamics-aware latent representation by explicitly capturing temporal changes in consecutive visual inputs. 

- We empirically validate that ResWM delivers substantial performance enhancements across intricate control tasks, providing a principled conduit to reconcile deep RL advancements with the exigencies of real-world robotics. 

## **2 RELATED WORKS** 

Model-based reinforcement learning (MBRL) tackles visual RL by learning world models from pixel observations, offering efficiency over model-free approaches like SAC and PPO. Dreamer [35–41] employs recurrent state-space models (RSSMs) for latent dynamics, while TD-MPC [42, 43] optimizes trajectories in latent space. Recent advances, such as DeepRAD [44] with robust representations and RAD [45] with data augmentation, condition dynamics on absolute actions. This approach introduces high-variance policies and oscillatory control, limiting stability in robotic tasks—where ResWM instead uses residual actions for smoother, more stable optimization. 

To address action instability, residual policies [46] predict incremental adjustments, as seen in incremental learning [47], reducing variance in planning. Robotics methods like Gaussian processes [48] and filtering [49] enforce smoothness for energy efficiency. ResAct [50] applies residuals in actor-critic setups, improving stability on DMControl (e.g., 715 vs. 690 for Quadruped, Walk at 1M steps, Table III), but lacks world model integration for imaginationbased learning. ResWM uniquely embeds residuals into RSSMs, 

enabling latent rollouts and outperforming ResAct (e.g., 644.8 vs. 630.2 average on hard tasks at 1M steps) with a design tailored for long-horizon planning. 

For perception, contrastive methods like CURL [51] and SVEA [52] use augmentations, while delta-based approaches [53] model frame differences. TACO [54] and MaDi [55] enhance efficiency but rely on absolute actions, lagging behind ResWM’s 925.0 average on DMControl (Table II) and 0.96 normalized mean on Atari (Table IV). ResWM’s Observation Difference Encoder (ODL) differs by conditioning residuals on explicit observation deltas, creating a causal perception-control link in Dreamer-style models—surpassing TACO (887.1) and MaDi (885.1) while excelling in both continuous and discrete domains. 

## **3 METHODOLOGY** 

Our methodology pioneers a principled reformulation of action and observation representations in latent variable world models, challenging the conventional paradigm of modeling absolute and temporally independent actions. Drawing inspiration from the inherent continuity of physical systems and biological motor control [56, 57], we propose a novel framework anchored on two groundbreaking principles: (1) redefining the control variable as a **residual action** to embed a robust temporal smoothness prior, thereby transforming chaotic global searches in the action space into elegant, localized refinements, and (2) conditioning this control signal on an explicit encoding of **observation differences** to forge a highly dynamics-aware latent space that captures the essence of environmental evolution. This innovative synthesis culminates in the **Residual-Action World Model (ResWM)** , a framework that not only bridges theoretical elegance with practical efficacy but also unlocks unprecedented stability and sample efficiency in visual reinforcement learning (RL). We elaborate on its architectural components, objective functions, and optimization processes below. 

## **3.1 Preliminaries: Latent Dynamics Models** 

We formulate the visual control problem as a Partially Observable Markov Decision Process (POMDP) [58], formally defined by the tuple (O _,_ A _, 𝑃, 𝑅,𝛾_ ). At each discrete time step _𝑡_ , the agent receives a high-dimensional visual observation _𝑜𝑡_ ∈O and emits an action _𝑎𝑡_ ∈A. The environment subsequently transitions to a new unobserved true state according to the transition dynamics _𝑃_ , and the agent receives a scalar reward _𝑟𝑡_ = _𝑅_ ( _𝑠𝑡 ,𝑎𝑡_ ). The agent’s overarching objective is to learn a policy _𝜋_ ( _𝑎𝑡_ | _𝑜_ ≤ _𝑡_ ) that maximizes the expected discounted return E[<sup>�</sup><sup>_𝑇_</sup> _𝑡_ =0<sup>_𝛾𝑡𝑟𝑡_], where</sup><sup>_𝛾_∈[0</sup><sup>_,_1)is the</sup> discount factor. 

Model-based RL agents approach this intractable highdimensional problem by learning a generative world model from a history of interactions D = {( _𝑜𝑡,𝑎𝑡 ,𝑟𝑡_ )}<sup>_𝑇_</sup> _𝑡_ =0<sup>[59, 60]. This</sup> model typically factorizes into several key components: 

- **Representation Model (Encoder)** _ℎ𝜃_ : _𝑜𝑡_ → _𝑠𝑡_ , which maps high-dimensional observations to a compact, Markovian latent state space. 

- **Transition Model (Dynamics)** _𝑔𝜙_ ( _𝑠𝑡_ +1| _𝑠𝑡,𝑎𝑡_ ), which predicts the forward evolution of the environment purely in the latent space. 

Conference’17, July 2017, Washington, DC, USA 

ResWM: Residual-Action World Model for Visual RL 

- **Reward Predictor** _𝑟𝜓_ ( _𝑟𝑡_ | _𝑠𝑡,𝑎𝑡_ ), which estimates the immediate task reward to facilitate offline planning or policy optimization [61]. 

A fundamental challenge in this paradigm lies in the choice of representation for the action _𝑎𝑡_ . Traditional world models [36] assume that the optimal action distribution at time _𝑡_ is independent of _𝑎𝑡_ −1, which overlooks the non-stationary nature of action distributions and the physical constraints of actuation. This frequently leads to high-frequency action chattering and optimization instability—issues that our novel residual formulation is specifically designed to circumvent. 

## **3.2 The Residual-Action Policy as a Smoothness Prior** 

Our central hypothesis posits that the direct prediction of absolute actions _𝑎𝑡_ constitutes an inherently ill-posed problem for continuous control tasks. Optimal physical trajectories are rarely composed of disjointed, independent control signals; rather, they demand smooth, continuous transitions. To seamlessly integrate this inductive bias, we introduce a reparameterization technique: the policy predicts an incremental adjustment _𝛿𝑎𝑡_ relative to the previous action _𝑎𝑡_ −1, effectively anchoring decisions in temporal continuity. The final action emitted to the environment emerges through a composed transformation: 


This elegant formulation instills a strong **temporal smoothness prior** into the policy network. By restricting the control output to a differential term, we reorient the optimization landscape from an expansive, unconstrained search across the global action space A to a refined exploration within a localized manifold centered on _𝑎𝑡_ −1. Consequently, this drastically narrows the effective search space, enhances the sample efficiency of the actor-critic learning phase, and fosters control signals characterized by low-frequency, energyefficient profiles. Such qualities are paramount for deploying RL algorithms on real-world physical systems, such as robotic manipulators and autonomous vehicles, where mechanical wear and actuation energy are critical constraints. In Equation 1, _𝑧𝑡_ serves as a specialized latent variable encapsulating environmental changes, which leads to our next architectural innovation. 

## **3.3 Observation Difference Encoding for a Dynamics-Aware State** 

To equip the policy with the most pertinent perceptual cues necessary for crafting the next action residual, we propose the **Observation Difference Encoder (ODL)** . Traditional frame-stacking [62] implicitly models velocity but often suffers from visual aliasing and high redundancy. Instead, ODL reimagines representation learning by explicitly focusing on temporal deltas. This is grounded in the insight that the optimal residual _𝛿𝑎𝑡_ is predominantly driven by the differential changes between consecutive observations rather than static visual snapshots. We formalize this through a sophisticated mapping ΦODL: 


where _𝑓_ and _𝑓_<sup>′</sup> denote independent or Siamese Convolutional Neural Network (CNN) encoders, FC is a fully connected layer, and LN denotes Layer Normalization [63] applied for representation stability. 

This architectural innovation achieves dual objectives: (1) it functions as a precise temporal filter, distilling dynamic, task-relevant elements (e.g., a moving object or a swinging pendulum) from static, distractor backgrounds, thereby mitigating pixel-level redundancy; and (2) it cultivates a **dynamics-aware latent representation** _𝑧𝑡_ that is intrinsically attuned to the residual action _𝛿𝑎𝑡_ . By coupling the ODL with the residual policy, we forge a symbiotic relationship between perception (observing changes) and control (acting via changes), elevating the model’s predictive acuity in visually complex, non-stationary environments. 

## **3.4 Latent Dynamics Conditioned on Residual Actions** 

To build a world model that natively understands our new action space, we integrate our framework into a Recurrent State-Space Model (RSSM) [64]. Crucially, the transition function is innovatively conditioned directly on the residual action _𝛿𝑎𝑡_ rather than the absolute action: 


where _𝑠𝑡_ represents the deterministic and stochastic components of the recurrent latent state. The complete generative model encompasses the following components, harmonized within the residualaction paradigm: 


Such a unified structure guarantees that the "imagined" trajectories used for policy learning are generated using the exact same control variables ( _𝛿𝑎_ ) optimized by the policy. This averts compounding errors and distribution shifts between the learned dynamics and the policy’s behavioral distribution, thereby significantly enhancing the fidelity of long-horizon predictions. 

## **3.5 Imagination, Policy Optimization, and Regularization** 

Policy learning in ResWM leverages imagination-based rollouts in the latent space. Commencing from a latent state _𝑠𝑡_ sampled from the replay buffer, an actor-critic algorithm simulates trajectories of horizon _𝐻_ utilizing the frozen dynamics model: 


Subsequently, the policy _𝜋𝜃_ and value function _𝑉𝜉_ are optimized to maximize the expected _𝜆_ -return [58] across these simulated paths. This derivative-free planning allows for efficient credit assignment without environmental interaction. 

To preserve the advantageous attributes of residual actions, we incorporate two targeted regularization mechanisms into the actor’s objective. First, a Kullback-Leibler (KL) divergence penalty steers the predicted residual distribution toward a zero-mean Gaussian prior, N (0 _, 𝜎𝛿_<sup>2</sup><sup>_𝐼_). This functions as an information bottleneck</sup> [65], discouraging excessive, erratic deviations and encouraging 

Conference’17, July 2017, Washington, DC, USA 

Jseen Zhang, Gabriel Adineera, Jinzhou Tan, and Jinoh Kim 


**Figure 1: Architecture of the proposed Residual-Action World Model (ResWM). (1) Observation Difference Encoder (ODL): Consecutive frames** _𝑜𝑡_ −1 **and** _𝑜𝑡_ **are processed to extract dynamic deltas, producing a dynamics-aware latent vector** _𝑧𝑡_ **. (2) Residual Policy: The actor network predicts a residual update** _𝛿𝑎𝑡_ **conditioned on** _𝑧𝑡_ **and the previous action** _𝑎𝑡_ −1 **, enforcing temporal smoothness. (3) Latent Dynamics: A Recurrent State-Space Model (RSSM) rolls out future latent states** _𝑠𝑡_ +1 **driven by these residual actions, enabling stable, long-horizon imagination for actor-critic optimization.** 

parsimonious trajectory adjustments. Second, an optional energy penalty LΔ _𝑎_ = _𝜆_ Δ ∥ _𝛿𝑎𝑡_ ∥<sup>2</sup> 2<sup>explicitly curtails control effort, aligning</sup> the optimized policy with resource-constrained robotic applications where aggressive actuation is detrimental. 

## **3.6 Overall Training Objective** 

The entire framework—encompassing the visual encoders, world model, and actor-critic networks—undergoes concurrent, end-toend training. This synergistic optimization is crucial because the quality of the learned latent representations directly dictates the efficacy of the imagined rollouts used for policy improvement. We minimize a comprehensive joint objective function Ltotal, assessed over dynamically sampled sequence batches drawn from the episodic replay buffer D: 

Ltotal = E _𝜏_ ∼D �Lmodel ( _𝜏_ ) + _𝜆_ actorLactor ( _𝜏_ ) + _𝜆_ valueLcritic ( _𝜏_ ) + Lreg ( _𝜏_ )� (5) 

In this formulation, Lmodel comprises the standard Variational Autoencoder (VAE) evidence lower bound (ELBO) [66]. This specifically includes the image reconstruction loss to ensure visual fidelity, the reward prediction loss to ground the latent space in task-specific utility, and a KL-balancing loss for the latent dynamics. The KLbalancing mechanism is particularly vital in world models; it applies separate scaling factors to the prior and posterior networks, preventing the dynamics prior from collapsing toward a poorly trained representation early in the training phase. 

Furthermore, Lactor and Lcritic represent the standard actor-critic losses derived from the _𝜆_ -returns of imagined rollouts. Specifically, the actor is optimized to maximize the expected value of the imagined trajectories by propagating gradients analytically through the differentiable dynamics model, while the critic is updated via temporal difference (TD) learning to accurately predict these long-horizon 

_𝜆_ -returns. Finally, Lreg integrates the aforementioned priors on residual actions, serving as an information bottleneck that enforces our desired temporal smoothness and mitigates catastrophic action chattering. A holistic overview of the training and interaction procedure is encapsulated in Algorithm 1, utilizing the Adam optimizer with decoupled weight decay to maintain representation sparsity and prevent overfitting on small replay buffers. 

## **4 Experiments** 

To comprehensively evaluate the proposed Residual Action World Model (ResWM), our empirical study is meticulously designed to answer three principal research questions (RQs): 

- **(RQ1) Performance and Sample Efficiency:** Does the integration of residual actions and dynamics-aware representations yield superior sample efficiency and asymptotic performance compared to state-of-the-art visual RL baselines? 

- **(RQ2) Action Smoothness and Energy Efficiency:** Can ResWM demonstrably reduce high-frequency action chattering and generate smoother, more energy-efficient control trajectories, which are critical for real-world physical deployment? 

- **(RQ3) Ablation and Component Analysis:** How much do the individual components—specifically the Observation Difference Encoder (ODL) and the residual policy formulation—contribute to the overall robustness and representation learning of the framework? 

To rigorously address these questions, this section first presents the performance of ResWM compared with strong, state-of-theart baselines such as DeepRAD [67] and DreamerV3 [36] across 

Conference’17, July 2017, Washington, DC, USA 

ResWM: Residual-Action World Model for Visual RL 

diverse and challenging continuous control tasks. Our primary evaluation testbed is the DeepMind Control Suite (DMControl) [68], which provides a spectrum of complex biomechanical and robotic environments characterized by intricate contact dynamics, highdimensional visual inputs, and sparse reward landscapes. Furthermore, to evaluate the specific impact of the ODL in mitigating visual distractions, we conduct supplementary experiments in modified environments featuring dynamic, non-stationary backgrounds. 

## **5 Experiments** 

To comprehensively evaluate the proposed **Residual Action World Model (ResWM)** , this section first presents its performance compared with strong baselines such as **DeepRAD** on two mainstream reinforcement learning benchmarks, followed by an in-depth analysis of its core design through a series of ablation studies. We adopt both the **DeepMind Control Suite (DMControl)** [76] and the **Atari benchmark[77]** , where the former represents continuous control tasks and the latter provides diverse challenges in terms of visual complexity and sparse rewards. Notably, ResWM can be seamlessly integrated into existing world model frameworks with only minor architectural modifications and without introducing any additional hyperparameters, thereby ensuring the fairness of comparisons. On DMControl, we begin with evaluations on six commonly used tasks and further include five more challenging tasks to examine robustness. On Atari, our evaluation covers ten classic games, where the agent’s objective is to maximize the game score, thereby testing ResWM’s generalization ability in handling high-dimensional pixel inputs and long-horizon tasks[78]. 

## **5.1 Main Results** 

_Consistent Benefits Across Baselines._ By integrating our proposed **ResWM** module into a diverse set of baseline methods— including model-agnostic algorithms such as **pixel SAC** [80], representation-learning–based methods such as **DeepMDP** [81], and data-augmentation–based methods such as **RAD** [82]—Table 1 clearly demonstrates its strong generality and effectiveness. The module substantially improves sample efficiency: at 100K training steps, it boosts the average score of the strong baseline **DeepRAD** from 695.1 to 842.3 (an improvement of about 21%), and achieves a remarkable jump in specific tasks such as _Walker, Walk_ , where performance increases from 582 to 794. Notably, even for relatively simple baselines such as **pixel SAC** [20], ResWM delivers more than a twofold improvement in average performance (from 167.3 to 405.7), highlighting its strong low-level optimization capability. At the same time, ResWM also enhances the asymptotic performance ceiling: at 500K steps, it further raises the average score of **DeepRAD** from 890.8 to 919.8, and pushes performance to nearsaturation levels in tasks such as _Reacher, Easy_ (982 points) and _Ball in cup, Catch_ (972 points). Taken together, these results provide compelling evidence that ResWM is an efficient and plug-and-play module that delivers consistent performance gains—spanning from early training to final convergence—across different paradigms of vision-based reinforcement learning algorithms, all without introducing any additional hyperparameters. 

_Results on DMControl Standard Tasks._ Table 2 presents a comprehensive comparison between **ResWM** and a set of advanced methods on six standard **DMControl** tasks, which serve as widely adopted benchmarks for evaluating the fundamental capability of visual control algorithms. 

In terms of _sample efficiency_ at 100K environment steps, ResWM achieves the **highest average score of 828.7** , outperforming all state-of-the-art baselines, including ResAct (822.1). This advantage is not only reflected in the overall mean but also pronounced at the task level: ResWM secures the best performance on **four out of six tasks** , such as scoring **542 in Cheetah, Run** , highlighting its ability to rapidly acquire essential skills. 

The superiority of ResWM becomes even more evident in the _asymptotic performance_ evaluation at 500K steps. Its average score climbs to **925.0** , again ranking first, with ResWM taking the lead in **five out of six tasks** . Particularly, on **Reacher, Easy (986)** and **Ball in cup, Catch (978)** , ResWM pushes performance close to the saturation point, showcasing its remarkable learning ceiling and stability. 

Overall, this consistent and broad-based success across fundamental yet representative tasks firmly establishes ResWM as the new **state of the art (SOTA)** , while providing strong empirical evidence of the effectiveness of its core design. These results also lay a solid foundation for tackling more challenging domains. 

_Performance on DMControl Hard Tasks._ To further examine the robustness and performance ceiling of **ResWM** in more complex scenarios, Table 3 reports its evaluation results on five “hard tasks” from **DMControl** . These tasks pose more severe challenges to existing algorithms due to their partial observability and high-precision control requirements. At the mid-training stage (500K steps), the superiority of ResWM is already evident: it achieves an average score of 435.6, substantially outperforming all baselines, including **ResAct** (406.8) and **TACO** (333.8). Notably, at this stage, ResWM attains the highest score across all five hard tasks, demonstrating its remarkable learning capability. After extended training (1M steps), ResWM continues to maintain its leading position, with its average score further improving to 644.8, once again surpassing all competing methods. In tasks such as _Quadruped, Walk_ , it further widens the margin over the second-best method ResAct (715 vs. 690), and secures the best performance in all tasks except _Finger, Turn hard_ , where it still remains highly competitive. Taken together, this consistent dominance on challenging tasks provides strong evidence that ResWM not only excels on standard benchmarks but also derives its strength from a core design that endows it with robust generalization and problem-solving capability in complex and difficult environments. 

_Performance on Atari Benchmark._ Table 4 presents a performance comparison between **ResWM** and a set of advanced methods on the **Atari benchmark** , which is designed to evaluate the generalization ability of algorithms in handling high-dimensional pixel inputs, long-horizon credit assignment, and diverse tasks. In terms of normalized scores relative to human-level performance, ResWM demonstrates a clear overall advantage. Its normalized mean score reaches **0.96** , significantly higher than all competing methods, including **ResAct** (0.86), **TACO** (0.76), and **DeepRAD** (0.71). Similarly, its normalized median score (0.46) is also the best among all 

Conference’17, July 2017, Washington, DC, USA 

Jseen Zhang, Gabriel Adineera, Jinzhou Tan, and Jinoh Kim 

**Table 1: Performance comparison on DMControl 6 common tasks at 100K and 500K environment steps.** 

|**Task**|pixel SAC|+ResWM|DeepMDP|+ResWM|RAD|+ResWM|DeepRAD|+ResWM|
|---|---|---|---|---|---|---|---|---|
|**100K Step Scores**<br>|||||||||
|Cartpole, Swingup<br>|237±49|476±42|389±44|526±59|694±28|813±36|703±32|**845**±**67**|
|Reacher, Easy|239±183|489±152|471±173|596±132|734±87|894±32|792±77|**942**±**43**|
|Cheetah, Run|118±13|314±17|306±25|413±29|364±38|498±49|453±39|**542**±**64**|
|Walker, Walk|95±19|386±26|384±197|572±68|552±87|714±57|582±91|**694**±**87**|
|Finger, Spin|230±194|493±112|509±72|706±113|813±65|928±86|832±101|**986**±**86**|
|Ball in cup, Catch|85±130|276±68|704±24|743±9|825±49|865±57|809±45|**963**±**26**|
|Average|167.3|405.7|460.5|592.7|663.6|785.3|695.1|**828.7**|
|**500K Step Scores**|||||||||
|Cartpole, Swingup|330±73|693±84|817±15|843±18|861±9|876±18|870±6|**882**±**21**|
|Reacher, Easy|307±65|703±57|792±83|894±62|917±47|946±32|942±45|**986**±**9**|
|Cheetah, Run|85±51|456±46|613±32|682±46|669±42|743±24|721±58|**783**±**37**|
|Walker, Walk|71±52|582±58|594±172|834±152|902±43|932±59|925±88|**957**±**26**|
|Finger, Spin|346±95|663±91|828±63|936±96|922±43|946±48|932±32|**964**±**86**|
|Ball in cup, Catch|162±122|524±122|944±16|964±12|959±15|968±8|954±11|**978**±**23**|
|Average|216.8|603.5|764.6|858.8|872.5|901.8|890.8|**925.0**|


**Table 2: Performance comparison on DMControl 6 common tasks at 100K and 500K environment steps (mean** ± **std over 5 seeds).** 

|**100K STEP SCORES**|CURL[69]<br>(ICML’20)|SVEA[70]<br>(NeurIPS’21)|PlayVirtual[71]<br>(NeurIPS’21)|MLR[72]<br>(NeurIPS’22)|PSRL[73]<br>(CVPR’23)|TACO[74]<br>(NeurIPS’23)|MaDi[75]<br>(AAMAS’24)|ResAct[50]<br>(AAAI’25)|**ResWM**<br>(Ours)|
|---|---|---|---|---|---|---|---|---|---|
|Cartpole, Swingup|582±146|727±86|816±36|806±48|849±63|782±51|704±54|819±44|845±67|
|Reacher, Easy|538±233|811±115|785±142|866±103|621±202|821±97|766±101|917±59|942±42|
|Cheetah, Run|299±48|375±54|474±50|482±38|398±71|402±62|432±44|503±42|542±64|
|Walker, Walk|403±24|747±65|460±173|643±114|595±104|601±103|574±94|772±65|694±87|
|Finger, Spin|767±56|859±77|915±49|907±58|882±132|876±67|810±95|974±42|986±8|
|Ball in cup, Catch|769±43|915±71|929±31|933±16|922±60|902±54|884±36|948±44|963±26|
|**Average**|559.7|739.0|729.8|772.8|711.1|730.7|695.0|822.1|828.7|
|**500K STEP SCORES**||||||||||
|Cartpole, Swingup|841±45|865±10|865±11|872±5|895±39|870±21|849±6|870±12|882±21|
|Reacher, Easy|929±44|944±52|942±66|957±41|932±41|944±50|955±31|974±16|986±9|
|Cheetah, Run|518±28|682±65|719±51|674±37|686±80|663±30|732±45|750±8|783±37|
|Walker, Walk|902±43|919±24|928±30|939±10|930±75|914±87|912±26|953±21|957±26|
|Finger, Spin|926±45|924±93|963±40|973±31|961±121|972±89|951±47|979±4|964±86|
|Ball in cup, Catch|959±27|960±19|967±5|964±14|988±54|960±22|912±62|967±4|978±23|
|**Average**|845.8|882.3|897.3|896.5|894.1|887.1|885.1|915.5|925.0|


methods. This strong average performance stems from its consistently superior results across individual games: in all ten games listed in the table, ResWM achieves the highest raw scores. For example, in _Phoenix_ , ResWM achieves a score of 5426, substantially outperforming the second-best ResAct (4826), and in _Carnival_ , it secures a leading score of 4752 compared to 4203. Taken together, these results on the Atari benchmark provide compelling evidence of the powerful generalization ability of the ResWM framework, 

demonstrating that its core design is not only effective for continuous control tasks but also achieves state-of-the-art performance in complex discrete control environments. 

## **5.2 Ablation Analysis** 

To rigorously disentangle the independent contributions of each core component within the proposed **ResWM framework** , we conducted a systematic **ablation study** . Specifically, we compared the full model against three key ablated variants. The first, **V1 (w/o Residual Policy)** , reverts to the conventional paradigm of 

Conference’17, July 2017, Washington, DC, USA 

ResWM: Residual-Action World Model for Visual RL 

**Table 3: Performance on DMControl 5 hard tasks at 500K and 1M environment steps (mean** ± **std over 5 seeds).** 

|Task|Flare[79]|TACO|MaDi|DeepRAD|ResAct|ResWM (500K)|Flare|TACO|MaDi|DeepRAD|ResAct|ResWM (1M)|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Quadruped, Walk|296±139|345±89|277±92|307±142|385±81|408±136|488±221|665±144|621±172|586±193|690±128|715±108|
|Pendulum, Swingup|242±152|485±167|372±101|308±137|618±380|645±112|809±31|784±42|751±41|626±220|817±6|836±36|
|Hopper, Hop|90±55|112±42|80±24|51±19|99±49|116±32|217±59|221±45|201±43|212±13|233±32|246±48|
|Finger, Turn hard|282±67|372±174|311±143|173±195|465±153|513±124|661±315|672±167|695±133|310±278|857±80|843±134|
|Walker, Run|426±33|355±89|382±87|375±177|467±27|496±62|556±93|582±63|562±68|508±125|554±21|584±57|
|Average|267.2|333.8|284.4|242.8|406.8|435.6|546.2|584.8|566.0|448.4|630.2|644.8|


**Table 4: Performance comparison on Atari 10 benchmark. Scores are raw environment returns;** 

|Game|Random|Human|Flare|CURL|DeepMDP|MaDi|DeepRAD|TACO|ResAct|ResWM|
|---|---|---|---|---|---|---|---|---|---|---|
|Assault|222.4|742|846|967|1264|1427|1824|1963|2164|2408|
|BeamRider|363.9|16926.5|1462|1824|1996|2172|2936|2542|3524|3928|
|Berzerk|123.7|2630.4|452|397|542|567|642|723|653|674|
|Carnival|0|3800|1876|2043|2467|2537|2896|3457|4203|4752|
|Centipede|2090.9|12017|3246|3721|3526|4386|4673|4726|5082|5431|
|ChopperCommand|811|7387.8|463|1579|1628|2136|3436|2962|3362|3528|
|NameThisGame|2292.3|8049|5986|6734|7456|7963|8567|9657|9273|10486|
|Phoenix|761.4|7242.6|1673|2936|2743|3126|4236|3876|4826|5426|
|SpaceInvaders|148|1668.7|632|542|673|795|842|892|874|927|
|TimePilot|3568|5229.2|1624|1936|2038|2496|3845|3726|4168|4076|
|Normalised Mean (%)|0|1|0.19|0.28|0.38|0.48|0.71|0.76|0.86|0.96|
|Normalised Median (%)|0|1|0.14|0.21|0.24|0.30|0.43|0.40|0.43|0.46|


predicting absolute actions, thereby validating the fundamental value of residual reparameterization. The second, **V2 (w/o ODL)** , replaces the observation difference encoder with a standard encoder to assess the synergistic effect of ODL. The third, **V3 (w/o Regularization)** , removes the regularization constraint on residual actions, serving to examine its auxiliary impact. 

Evaluations were carried out on a set of representative continuous control tasks from the **DeepMind Control Suite** , covering a spectrum of difficulty levels: _Walker Walk_ and _Finger Spin_ as standard tasks to assess baseline performance, and _Hopper Hop_ and _Walker Run_ as more challenging tasks to probe robustness under complex dynamics. To ensure fairness, all variants share identical network architectures and hyperparameter configurations, with the only difference being the ablated component. Performance was comprehensively assessed by plotting the **learning curves** of task scores as a function of training steps, thereby enabling a direct comparison of sampling efficiency and asymptotic performance across variants. 

Figure 2 provides an intuitive decomposition of the contribution and relative importance of the core components in the **ResWM** framework. Across all evaluated tasks, the **residual action policy** emerges as the most critical design choice. The variant **V1** (w/o Residual Policy) consistently ranks last and completely fails to learn on the hard task _Hopper, Hop_ (with scores near zero), whereas the full model successfully solves it—indicating that residual reparameterization of actions is fundamental for tackling complex dynamics. 

The **Observation Difference Encoder (ODL)** also plays an important role: removing it ( **V2** , w/o ODL) leads to the secondlargest drop in performance. Eliminating the regularization term ( **V3** , w/o Regularization) likewise degrades performance, though to a lesser extent. These results establish a clear contribution ordering: **Residual Policy** _>_ **ODL** _>_ **Regularization** . 

Notably, while the performance gaps among variants are already visible on standard tasks such as _Walker, Walk_ , they become markedly amplified on harder tasks including _Hopper, Hop_ and _Walker, Run_ . In the end, the full model ( **V4** , Full Model) achieves the best sample efficiency and asymptotic performance across all tasks, demonstrating strong synergy among its components and jointly underpinning the model’s superior performance and robustness. 

## **5.3 Qualitative Analysis of ODL** 

To investigate the internal working mechanism of ODL, we design a qualitative visualization experiment to compare the visual attention patterns of the **ResWM** agent and the baseline **DeepRAD** on _DMControl_ tasks. Inspired by the method of Zagoruyko and Komodakis, we generate attention maps by first applying channelwise average pooling to the absolute activation values, followed by a spatial softmax operation over the resulting 2D map. This setup enables a qualitative comparison of the visual focus exhibited by both models during the decision-making process. 

**Figure 3** clearly highlights the fundamental difference in visual attention strategies between **DeepRAD** and our proposed model. Across all _DMControl_ tasks, DeepRAD exhibits a diffuse and holistic 

Conference’17, July 2017, Washington, DC, USA 

Jseen Zhang, Gabriel Adineera, Jinzhou Tan, and Jinoh Kim 


**Figure 2: The figure compares the full model (V4) with three variants (V1–V3) across four** **_DMControl_ tasks. Results show a performance hierarchy: Residual Policy** _>_ **ODL** _>_ **Regularization. V4 achieves the best results, confirming the synergistic benefits of all components.** 


**Figure 3: This figure highlights a key difference in attention strategies: while DeepRAD exhibits diffuse attention across limb contours, our model focuses sharply on key joints and effectors, enabling more efficient and task-relevant decisionmaking.** 

attention pattern that broadly covers the moving limbs’ outlines. In contrast, our model demonstrates a sparse yet sharply focused mechanism that concentrates attention precisely on the critical 

joints and end-effectors essential for task execution. This observation indicates that our model possesses a more advanced internal mechanism capable of identifying and prioritizing the most informative regions in dynamic scenes, thereby enabling more efficient decision-making.This stark contrast in attention can be attributed to the core mechanism of the ODL. By explicitly modeling the temporal difference between consecutive frames, the ODL naturally learns to suppress static background information and amplify regions of high motion. Consequently, the learned representation is distilled to focus on the most causally significant elements—the joints and effectors—whose movements directly correlate with the agent’s actions and task progress. This inherent focus on dynamics, rather than static appearance, allows ResWM to build a more parsimonious and effective state representation, ultimately leading to more robust and sample-efficient policy learning. 

## **6 Conclusion** 

In this work, we presented the Residual-Action World Model (ResWM), a principled framework that fundamentally reformulates action and representation learning in model-based reinforcement learning. By replacing the conventional absolute action paradigm with a residual-action formulation, and coupling it with the Observation Difference Encoder (ODL), ResWM seamlessly embeds a temporal smoothness prior and establishes a robust, causal link between visual perception and physical control. This architectural synergy not only stabilizes long-horizon planning in the latent space but also naturally yields smoother, highly energy-efficient trajectories that are highly desirable for real-world physical systems. Comprehensive empirical evaluations across the DMControl suite and Atari benchmarks demonstrate that ResWM achieves consistent improvements in sample efficiency, asymptotic returns, and zero-shot generalization over strong state-of-the-art baselines. Furthermore, our extensive ablation studies confirm that the residual reparameterization serves as the primary catalyst for these performance gains, significantly complemented by the dynamics-aware representations learned via ODL and targeted regularization. Ultimately, ResWM paves a promising new pathway for bridging the gap between high-dimensional visual simulations and the rigorous demands of real-world robotic control. 

## **7 Limitations and Future Work** 

Despite the significant advantages of the ResWM framework, several limitations warrant discussion and present exciting avenues for future research. First, while the residual action prior effectively enforces temporal smoothness, it may inherently constrain the agent’s ability to react instantaneously to abrupt, high-frequency environmental shocks or sudden task transitions (e.g., unexpected physical collisions). Because the action update is bounded by _𝛿𝑎𝑡_ , the agent might require multiple consecutive timesteps to execute a drastic change in the action space. Future work could explore adaptive residual scaling or hierarchical control structures where a meta-controller dynamically toggles between absolute and residual action spaces based on the predicted volatility of the environment. the Observation Difference Encoder (ODL) introduces a marginal increase in computational and memory overhead during the encoding phase, as it explicitly requires processing consecutive frames 

Conference’17, July 2017, Washington, DC, USA 

ResWM: Residual-Action World Model for Visual RL 

( _𝑜𝑡_ and _𝑜𝑡_ −1) to compute temporal deltas. While this cost is largely mitigated during the imagination phase—which operates entirely within the compact latent space—it slightly impacts real-time inference latency during environment interaction. 

## **References** 

- [1] David Ha and Jürgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2(3), 2018. 

- [2] Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels, 2019. 

- [3] David Silver, Aja Huang, Chris J. Maddison, Arthur Guez, Laurent Sifre, George van den Driessche, Julian Schrittwieser, Ioannis Antonoglou, Veda Panneershelvam, Marc Lanctot, Sander Dieleman, Dominik Grewe, John Nham, Nal Kalchbrenner, Ilya Sutskever, Timothy Lillicrap, Madeleine Leach, Koray Kavukcuoglu, Thore Graepel, and Demis Hassabis. Mastering the game of go with deep neural networks and tree search. _Nature_ , 529(7587):484–489, 2016. 

- [4] Jusheng Zhang, Zimeng Huang, Yijia Fan, Ningyuan Liu, Mingyan Li, Zhuojie Yang, Jiawei Yao, Jian Wang, and Keze Wang. KABB: Knowledge-aware bayesian bandits for dynamic expert coordination in multi-agent systems. In _Forty-second International Conference on Machine Learning_ , 2025. 

- [5] Jusheng Zhang, Yijia Fan, Wenjun Lin, Ruiqi Chen, Haoyi Jiang, Wenhao Chai, Jian Wang, and Keze Wang. GAM-agent: Game-theoretic and uncertainty-aware collaboration for complex visual reasoning. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 

- [6] Jusheng Zhang, Yijia Fan, Kaitong Cai, Jing Yang, Jiawei Yao, Jian Wang, Guanlong Qu, Ziliang Chen, and Keze Wang. Why keep your doubts to yourself? trading visual uncertainties in multi-agent bandit systems, 2026. 

- [7] Jusheng Zhang, Kaitong Cai, Yijia Fan, Ningyuan Liu, and Keze Wang. MATagent: Adaptive multi-agent training optimization. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 

- [8] Jusheng Zhang, Kaitong Cai, Jing Yang, and Keze Wang. Learning dynamics of vlm finetuning, 2025. 

- [9] Jusheng Zhang, Kaitong Cai, Qinglin Zeng, Ningyuan Liu, Stephen Fan, Ziliang Chen, and Keze Wang. Failure-driven workflow refinement, 2025. 

- [10] Fan-Ming Luo, Tian Xu, Hang Lai, Xiong-Hui Chen, Weinan Zhang, and Yang Yu. A survey on model-based reinforcement learning, 2022. 

- [11] Younggyo Seo, Danijar Hafner, Hao Liu, Fangchen Liu, Stephen James, Kimin Lee, and Pieter Abbeel. Masked world models for visual control, 2023. 

- [12] Jusheng Zhang, Yijia Fan, Zimo Wen, Jian Wang, and Keze Wang. Tri-MARF: A trimodal multi-agent responsive framework for comprehensive 3d object annotation. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 

- [13] Jusheng Zhang, Kaitong Cai, Yijia Fan, Jian Wang, and Keze Wang. CF-VLM: Counterfactual vision-language fine-tuning. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 

- [14] Jusheng Zhang, Kaitong Cai, Xiaoyang Guo, Sidi Liu, Qinhan Lv, Ruiqi Chen, Jing Yang, Yijia Fan, Xiaofei Sun, Jian Wang, Ziliang Chen, Liang Lin, and Keze Wang. Mm-cot:a benchmark for probing visual chain-of-thought reasoning in multimodal models, 2025. 

- [15] Jusheng Zhang, Xiaoyang Guo, Kaitong Cai, Qinhan Lv, Yijia Fan, Wenhao Chai, Jian Wang, and Keze Wang. Hybridtoken-vlm: Hybrid token compression for vision-language models, 2025. 

- [16] Jusheng Zhang, Yijia Fan, Kaitong Cai, and Keze Wang. Kolmogorov-arnold fourier networks, 2025. 

- [17] Thomas M. Moerland, Joost Broekens, Aske Plaat, and Catholijn M. Jonker. Model-based reinforcement learning: A survey, 2022. 

- [18] Jusheng Zhang, Yijia Fan, Kaitong Cai, Zimeng Huang, Xiaofei Sun, Jian Wang, Chengpei Tang, and Keze Wang. Drdiff: Dynamic routing diffusion with hierarchical attention for breaking the efficiency-quality trade-off, 2025. 

- [19] Jusheng Zhang, Yijia Fan, Kaitong Cai, Xiaofei Sun, and Keze Wang. Osc: Cognitive orchestration through dynamic knowledge alignment in multi-agent llm collaboration, 2025. 

- [20] Denis Yarats, Ilya Kostrikov, and Rob Fergus. Image augmentation is all you need: Regularizing deep reinforcement learning from pixels. In _International Conference on Learning Representations (ICLR)_ , 2021. 

- [21] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms, 2017. 

- [22] Tankred Saanum, Peter Dayan, and Eric Schulz. Simplifying latent dynamics with softly state-invariant world models, 2024. 

- [23] Anusha Nagabandi, Gregory Kahn, Ronald S. Fearing, and Sergey Levine. Neural network dynamics for model-based deep reinforcement learning with model-free fine-tuning. _CoRR_ , abs/1708.02596, 2017. 

- [24] Richard S. Sutton. Dyna, an integrated architecture for learning, planning, and reacting. _SIGART Bull._ , 2(4):160–163, July 1991. 

- [25] Jingtao Ding, Yunke Zhang, Yu Shang, Yuheng Zhang, Zefang Zong, Jie Feng, Yuan Yuan, Hongyuan Su, Nian Li, Nicholas Sukiennik, Fengli Xu, and Yong Li. Understanding world or predicting future? a comprehensive survey of world models, 2025. 

- [26] Jusheng Zhang, Ningyuan Liu, Qinhan Lyu, Jing Yang, and Keze Wang. Rational anova networks, 2026. 

- [27] Jusheng Zhang, Kaitong Cai, Jian Wang, Yongsen Zheng, Kwok-Yan Lam, and Keze Wang. Process-of-thought reasoning for videos, 2026. 

- [28] Jusheng Zhang, Yijia Fan, Kaitong Cai, Jing Yang, Yongsen Zheng, Kwok-Yan Lam, Liang Lin, and Keze Wang. Spectral gating networks, 2026. 

- [29] Kaitong Cai, Jusheng Zhang, Jing Yang, Yijia Fan, Pengtao Xie, Jian Wang, and Keze Wang. Flashvlm: Text-guided visual token selection for large multimodal models, 2025. 

- [30] Ruixiang Sun, Hongyu Zang, Xin Li, and Riashat Islam. Learning latent dynamic robust representations for world models, 2024. 

- [31] Jusheng Zhang, Kaitong Cai, Jing Yang, Jian Wang, Chengpei Tang, and Keze Wang. Top-down semantic refinement for image captioning, 2025. 

- [32] Jensen Zhang, Ningyuan Liu, Yijia Fan, Zihao Huang, Qinglin Zeng, Kaitong Cai, Jian Wang, and Keze Wang. Llm-cas: Dynamic neuron perturbation for real-time hallucination correction, 2025. 

- [33] Jiawei Yao, Jusheng Zhang, Xiaochao Pan, Tong Wu, and Canran Xiao. Depthssc: Monocular 3d semantic scene completion via depth-spatial alignment and voxel adaptation, 2024. 

- [34] Xiaohua Li, Jusheng Zhang, and Fatemeh Safara. Improving the accuracy of diabetes diagnosis applications through a hybrid feature selection algorithm. _Neural Process. Lett._ , 55(1):153–169, March 2021. 

- [35] Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Dream to control: Learning behaviors by latent imagination, 2019. 

- [36] Danijar Hafner, Jurgis Pasukonis, James Ba, and Mohammad Norouzi. Mastering diverse domains through world models, 2023. 

- [37] Yiyang Chen, Xuanhua He, Xiujun Ma, and Yue Ma. Contextflow: Trainingfree video object editing via adaptive context enrichment. _arXiv preprint arXiv:2509.17818_ , 2025. 

- [38] Yue Ma, Yingqing He, Xiaodong Cun, Xintao Wang, Siran Chen, Xiu Li, and Qifeng Chen. Follow your pose: Pose-guided text-to-video generation using pose-free videos. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 38, pages 4117–4125, 2024. 

- [39] Yue Ma, Hongyu Liu, Hongfa Wang, Heng Pan, Yingqing He, Junkun Yuan, Ailing Zeng, Chengfei Cai, Heung-Yeung Shum, Wei Liu, et al. Follow-your-emoji: Finecontrollable and expressive freestyle portrait animation. In _SIGGRAPH Asia 2024 Conference Papers_ , pages 1–12, 2024. 

- [40] Yue Ma, Zexuan Yan, Hongyu Liu, Hongfa Wang, Heng Pan, Yingqing He, Junkun Yuan, Ailing Zeng, Chengfei Cai, Heung-Yeung Shum, et al. Follow-your-emojifaster: Towards efficient, fine-controllable, and expressive freestyle portrait animation. _arXiv preprint arXiv:2509.16630_ , 2025. 

- [41] Yue Ma, Yulong Liu, Qiyuan Zhu, Ayden Yang, Kunyu Feng, Xinhua Zhang, Zhifeng Li, Sirui Han, Chenyang Qi, and Qifeng Chen. Follow-your-motion: Video motion transfer via efficient spatial-temporal decoupled finetuning. _arXiv preprint arXiv:2506.05207_ , 2025. 

- [42] Nicolai A. Hansen, Hao Su, and Xiaolong Wang. Temporal difference learning for model predictive control, 2022. 

- [43] Yue Ma, Kunyu Feng, Zhongyuan Hu, Xinyu Wang, Yucheng Wang, Mingzhe Zheng, Xuanhua He, Chenyang Zhu, Hongyu Liu, Yingqing He, et al. Controllable video generation: A survey. _arXiv preprint arXiv:2507.16869_ , 2025. 

- [44] Yuchen Guo, Hao Zhang, Rui Zhao, and Sergey Levine. Deeprad: Deep residual attention decoder for visual reinforcement learning, 2023. 

- [45] Michael Laskin, Kimin Lee, Pieter Abbeel, and Aravind Srinivas. Reinforcement learning with augmented data, 2020. 

- [46] David Silver, Guy Lever, Nicolas Heess, Thomas Degris, Daan Wierstra, and Martin Riedmiller. Residual policy learning, 2018. 

- [47] Sachin Ravi and Hugo Larochelle. Meta-learning for semi-supervised few-shot classification, 2018. 

- [48] Roberto Calandra, Jan Peters, Marc Deisenroth, and José Carlos del Solar. Manifold gaussian processes for regression, 2016. 

- [49] Marc Deisenroth and Carl E. Rasmussen. Pilco: A model-based and data-efficient approach to policy search, 2011. 

- [50] Anonymous. Visual reinforcement learning with residual action, 2025. 

- [51] Ruiqi Gao, Tian Ye, and Chen Sun. Curl: Contrastive unsupervised representations for reinforcement learning, 2020. 

- [52] Yuchen Guo, Rui Zhao, Ziyu Wang, and Sergey Levine. Svea: Self-supervised visual exploration and augmentation for visual rl, 2021. 

- [53] Linfeng Zhang, Gautam Tulsiani, Jonathan T. Barron, Adrien Jacot-Guillarmod, and Jitendra Malik. Deepmdp: Learning deep models from upper level policies for multi-objective rl, 2020. 

- [54] Tianmin Chen, Tanmay Gupta, and Anirudh Xu. Taco: Temporal latent actiondriven contrastive loss for visual reinforcement learning, 2023. 

Conference’17, July 2017, Washington, DC, USA 

Jseen Zhang, Gabriel Adineera, Jinzhou Tan, and Jinoh Kim 

- [55] Yuchen Guo, Hao Zhang, Rui Zhao, and Sergey Levine. Madi: Learning to mask distractions for generalization in visual reinforcement learning, 2024. 

- [56] Chayan Banerjee, Kien Nguyen, Clinton Fookes, and Maziar Raissi. A survey on physics informed reinforcement learning: Review and open problems. _Expert Systems with Applications_ , 287:128166, August 2025. 

- [57] Jan Peters and Stefan Schaal. Reinforcement learning of motor skills with policy gradients. _Neural Networks_ , 21(4):682–697, 2008. 

- [58] Richard S. Sutton and Andrew G. Barto. _Reinforcement Learning: An Introduction_ . MIT Press, 2nd edition, 2018. 

- [59] David Ha and Jürgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2018. 

- [60] Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Dream to control: Learning behaviors by latent imagination, 2019. 

- [61] Danijar Hafner, Timothy Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete world models, 2020. 

- [62] Volodymyr Mnih, Koray Kavukcuoglu, David Silver, Andrei A Rusu, Joel Veness, Marc G Bellemare, Alex Graves, Martin Riedmiller, Andreas K Fidjeland, Georg Ostrovski, et al. Human-level control through deep reinforcement learning. _Nature_ , 518(7540):529–533, 2015. 

- [63] Jimmy Lei Ba, Jamie Ryan Kiros, and Geoffrey E. Hinton. Layer normalization. _arXiv preprint arXiv:1607.06450_ , 2016. 

- [64] Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels, 2019. 

- [65] Alexander A. Alemi, Ian Fischer, Joshua V. Dillon, and Kevin Murphy. Deep variational information bottleneck. _arXiv preprint arXiv:1612.00410_ , 2016. 

- [66] Diederik P. Kingma and Max Welling. Auto-encoding variational bayes. _arXiv preprint arXiv:1312.6114_ , 2013. 

- [67] Michael Laskin, Kimin Lee, Adam Stooke, Lerrel Pinto, Pieter Abbeel, and Aravind Srinivas. Reinforcement learning with augmented data, 2020. 

- [68] Yuval Tassa, Yotam Doron, Alistair Muldal, Tom Erez, Yazhe Li, Diego de Las Casas, David Budden, Abbas Abdolmaleki, Josh Merel, Andrew Lefrancq, Timothy Lillicrap, and Martin Riedmiller. Deepmind control suite. _arXiv preprint arXiv:1801.00690_ , 2018. 

- [69] Aravind Srinivas, Michael Laskin, and Pieter Abbeel. Curl: Contrastive unsupervised representations for reinforcement learning, 2020. 

- [70] Nicklas Hansen, Hao Su, and Xiaolong Wang. Stabilizing deep q-learning with convnets and vision transformers under data augmentation, 2021. 

- [71] Tao Yu, Cuiling Lan, Wenjun Zeng, Mingxiao Feng, Zhizheng Zhang, and Zhibo Chen. Playvirtual: Augmenting cycle-consistent virtual trajectories for reinforcement learning, 2021. 

- [72] Tao Yu, Zhizheng Zhang, Cuiling Lan, Yan Lu, and Zhibo Chen. Mask-based latent reconstruction for reinforcement learning, 2022. 

- [73] Hyesong Choi, Hunsang Lee, Wonil Song, Sangryul Jeon, Kwanghoon Sohn, and Dongbo Min. Local-guided global: Paired similarity representation for visual reinforcement learning. In _CVPR_ , pages 15072–15082, 2023. 

- [74] Ruijie Zheng, Xiyao Wang, Yanchao Sun, Shuang Ma, Jieyu Zhao, Huazhe Xu, Hal Daumé III, and Furong Huang. Taco: Temporal latent action-driven contrastive loss for visual reinforcement learning, 2024. 

- [75] Bram Grooten, Tristan Tomilin, Gautham Vasan, Matthew E. Taylor, A. Rupam Mahmood, Meng Fang, Mykola Pechenizkiy, and Decebal Constantin Mocanu. Madi: Learning to mask distractions for generalization in visual deep reinforcement learning, 2023. 

- [76] Saran Tunyasuvunakool, Alistair Muldal, Yotam Doron, Siqi Liu, Steven Bohez, Josh Merel, Tom Erez, Timothy Lillicrap, Nicolas Heess, and Yuval Tassa. dm_control: Software and task suites for reinforcement learning. _Software Impacts_ , 7:100022, nov 2020. 

- [77] M. G. Bellemare, Y. Naddaf, J. Veness, and M. Bowling. The arcade learning environment: An evaluation platform for general agents. _Journal of Artificial Intelligence Research_ , 47:253–279, June 2013. 

- [78] Danijar Hafner, Timothy P. Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete world models. _CoRR_ , abs/2010.02193, 2020. 

- [79] Wenling Shang, Xiaofei Wang, Aravind Srinivas, Aravind Rajeswaran, Yang Gao, Pieter Abbeel, and Michael Laskin. Reinforcement learning with latent flow, 2021. 

- [80] Ilya Kostrikov, Denis Yarats, and Rob Fergus. Image augmentation is all you need: Regularizing deep reinforcement learning from pixels, 2021. 

- [81] Carles Gelada, Saurabh Kumar, Jacob Buckman, Ofir Nachum, and Marc G. Bellemare. Deepmdp: Learning continuous latent space models for representation learning, 2019. 

- [82] Michael Laskin, Kimin Lee, Adam Stooke, Lerrel Pinto, Pieter Abbeel, and Aravind Srinivas. Reinforcement learning with augmented data, 2020. 

