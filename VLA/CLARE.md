---
title: "CLARE: Continual Learning for Vision-Language-Action Models via Autonomous Adapter Routing and Expansion"
date: "2026-01-14"
authors: "Ralf Römer; Yi Zhang; Yuming Li; Angela P. Schoellig"
venue: "RA-L"
url: https://arxiv.org/abs/2601.09512
pdf: https://arxiv.org/pdf/2601.09512
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.09512)** / [論文ページ](https://arxiv.org/abs/2601.09512)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **CLARE: Continual Learning for Vision-Language-Action Models via Autonomous Adapter Routing and Expansion** 

Ralf R¨omer<sup>_∗,_1</sup> Yi Zhang<sup>_∗,_1</sup> Yuming Li<sup>1</sup> Angela P. Schoellig<sup>1</sup><sup>_,_2</sup><sup>_,_3</sup> 

**_Abstract_ — To teach robots complex manipulation tasks, a common approach is to fine-tune a pre-trained vision-languageaction model (VLA) on task-specific data. However, since this recipe updates existing representations, it is unsuitable for longterm operation in the real world, where robots must continually adapt to new tasks and environments while retaining the knowledge they have already acquired. Existing continual learning methods for robotics commonly require storing previous data (exemplars), struggle with long task sequences, or rely on task identifiers for deployment. To address these limitations, we propose CLARE, a general, parameter-efficient framework for exemplar-free continual learning with VLAs. CLARE introduces lightweight modular adapters into selected VLA modules and autonomously expands the model only where necessary when learning a new task, guided by layer-wise feature similarity. During deployment, an autoencoder-based routing mechanism dynamically activates the most relevant adapters without requiring task labels. Through extensive experiments on the LIBERO benchmark and five real-world tasks, we show that CLARE achieves high performance on new tasks without catastrophic forgetting of earlier tasks, significantly outperforming even exemplar-based methods. Code, data, and videos are available at our website: tum-lsy.github.io/clare.** 

### I. INTRODUCTION 

Robots deployed in homes, hospitals, or warehouses must operate for long periods while facing ever-changing conditions and task demands. For instance, a household robot may need to operate a newly purchased appliance, or an assistive robot may meet patients with unfamiliar mobility profiles. In such settings, robots must continually acquire new skills without sacrificing previously acquired capabilities. This long-term adaptability, known as continual or lifelong learning [1], remains an open challenge in robotics despite decades of research [2]–[4]. 

Recent advances in vision-language-action models (VLAs) [5]–[8] have demonstrated strong performance on complex, long-horizon manipulation tasks by integrating perception, language understanding, and action generation within a unified model. Pre-training on internet-scale data and robot demonstrations [9], [10] provides VLAs with broad priors that enable some degree of generalization [6]. However, state-of-the-art VLAs still cannot adapt reliably to unseen tasks without fine-tuning on task-specific data [6]– [8]. In a continual learning setting, where new tasks and 

> _∗_ Equal contribution. 

> 1 Technical University of Munich, Germany; TUM School of Computation, Information and Technology, Department of Computer Engineering, Learning Systems and Robotics Lab; Munich Institute of Robotics and Machine Intelligence (MIRMI). 

> 2 Robotics Institute Germany. 

> 3 Munich Center for Machine Learning. Corresponding email: _{_ ralf.roemer@tum.de _}_ 


Fig. 1: CLARE autonomously and continually injects lightweight adapters into selected layers of a pre-trained vision-language-action model (VLA). During inference, the most relevant adapters are activated based on feature similarity, captured by learned discriminators. By fine-tuning only the newly added parameters at each stage, the policy acquires new task-specific knowledge without catastrophic forgetting of previously learned skills. 

environments emerge over time, a naive approach would be to iteratively fully fine-tune (FFT) a VLA on new data. However, updating the parameters shared across modalities without regard for previously learned representations leads to significant degradation of both semantic grounding and policy performance on old tasks, a common issue known as catastrophic forgetting [11]. Therefore, current VLAs are not inherently capable of continual learning, hindering their deployment in non-stationary, real-world environments. 

Experience replay (ER) [12]–[14] can mitigate forgetting but has significant practical drawbacks for robotics. Past data may be unavailable due to storage or privacy constraints in a lifelong learning setting. Maintaining and accessing a large replay buffer increases computational and memory overhead, and selecting representative samples for replay is 

challenging. For these reasons, there is a strong need for exemplar-free continual learning methods that enable VLAs to acquire new skills while preserving prior knowledge. 

Modular and expandable architectures [15]–[17], which allocate new capacity for each task rather than overwriting shared representations, represent a promising direction for scalable continual learning. However, these methods often require oracle task identifiers, which are typically unavailable when robots operate autonomously in open-world settings. Moreover, the application of these methods to robotics has so far been mostly limited to multitask learning, where all tasks and data are available in advance [15], [18]. 

To close this gap, we introduce Continual Learning via Adapter Routing and Expansion (CLARE), a general framework that enables VLAs to continually incorporate new taskspecific knowledge without exemplars, task labels, or predefined expansion rules. CLARE injects lightweight adapters into selected modules of the pre-trained model and expands only when the feature statistics indicate substantial novelty, as visualized in Figure 1. At deployment, an autoencoderbased routing mechanism dynamically selects among the adapters, enabling autonomous task-agnostic inference. This design maintains a balance between stability and plasticity by preserving pre-trained representations and adding capacity as needed, enabling VLAs to learn new tasks with minimal parameter growth. In summary, our main contributions are: 

- A lightweight, modular framework enabling VLAs to learn new tasks without catastrophic forgetting. 

- An autonomous routing mechanism that activates the most suitable adapters during inference using feature similarity without task identifiers. 

- A dynamic expansion strategy that increases parameter count by only about 2% per task in our experiments. 

- Extensive experiments in simulation and real-world settings demonstrating that CLARE significantly outperforms continual learning baselines. 

While our evaluation focuses on a compact VLA architecture, the modular design of CLARE is architecture-agnostic and directly applicable to larger VLAs. 

### II. RELATED WORK 

_1) Vision-Language-Action Models:_ In recent years, the robotics community has begun collecting massive multimodal datasets [10] and exploiting generative modeling architectures [19], [20] to equip robots with broad semantic priors and facilitate generalization across tasks and environments [5]–[8]. These VLAs are usually based on visionlanguage models [21] and pre-trained on robot demonstrations [10] via imitation learning, enabling end-to-end mapping from high-dimensional multimodal observations to robot actions. Despite the growing scale of training data and model capacity, the ability of VLAs to generalize zero-shot to unseen tasks and environments remains limited [6], [22]. These models often overfit to their pre-training domains, as real-world robot data is much more expensive and scarce than web-scale vision and text datasets [3]. Thus, it has become a common paradigm to fine-tune a pre-trained VLA on 

curated, high-quality demonstrations [5]–[8] to achieve high performance on a specific task. However, in settings where tasks arrive sequentially and old data may be unavailable, this naive fine-tuning recipe is inadequate, as it overwrites previously learned task knowledge, leading to catastrophic forgetting [23]. 

_2) Continual Learning:_ Acquiring new skills from a stream of data without catastrophic forgetting of previously learned capabilities or losing plasticity is a hard problem in deep learning [4]. ER-based approaches [12]–[14] retain a subset of past examples and mix them with new data to preserve existing representations during training. Since storing exemplars may be infeasible, regularization-based methods [24], [25] constrain parameter updates for weights deemed important to a past task. Related to this idea, PackNet [26] prunes less relevant parameters from previously learned tasks and re-trains them for the new incoming data. However, methods like EWC or PackNet struggle with long task sequences as they are restricted by a fixed set of initial parameters. To overcome capacity bottlenecks and avoid catastrophic forgetting, architectural methods [15], [16], [27] inject new parameters or modules for novel tasks. By keeping the original model frozen and leveraging techniques such as low-rank adaptation (LoRA) [28], these methods can store new task-specific knowledge in a memory-efficient way. 

_3) Continual Imitation Learning in Robotics:_ Data scarcity and safety concerns make continual learning for robotics particularly challenging [2], [3]. LOTUS [29], a hierarchical method, constructs an ever-growing library of skill policies [30] and uses a meta-policy trained using ER for skill selection during deployment. SDP [18] injects taskspecific expert modules into diffusion policies but requires oracle task identifiers during deployment, which prevents fully autonomous operation in continual learning scenarios. Another recent work [31] fine-tunes a pre-trained base VLA checkpoint for each new task and employs a task scheduler to select from a model library for deployment. However, this approach is memory-inefficient and does not enable knowledge sharing between tasks. MLR [32] reduces storage demands by replaying only the frozen-encoder latent embeddings of past demonstrations and regularizes task embeddings via an angular margin constraint to prevent cross-task representation collapse. Most closely related to our work, DMPEL [17] builds an expert library for a transformer-based policy [33] and iteratively fine-tunes a router network using replay of the router’s past input/output data. In contrast to these works, CLARE does not require storing any previous data. 

### III. PROBLEM SETUP 

We consider a robotic system with state **_s_** _t_ and action **_a_** _t_ at timestep _t_ that must sequentially learn new tasks _{Tn}_<sup>_N_</sup> _n_ =1<sup>, with the total number of tasks,</sup><sup>_N_, unknown.</sup> A task _Tn_ = ( _ρ_<sup>_n_</sup> 0<sup>_,_</sup><sup>**_l_**</sup><sup>_n_)isdefinedbyaninitialdistribution</sup> of the state of the robot and the environment _ρ_<sup>_n_</sup> 0<sup>and</sup> a language instruction **_l_** _n_ . We assume the availability of a base VLA policy _π_ 0 = _π_ **_θ_** 0 with model parameters **_θ_** 0 that takes as input an observation **_o_** _t_ = ( **_I_** _t_<sup>1</sup><sup>_, . . . ,_</sup><sup>**_I_**</sup> _t_<sup>_N_c</sup><sup>_,_</sup><sup>**_q_**</sup><sup>_t,_</sup><sup>**_l_**)</sup> 

**Algorithm 1** Continual learning for VLAs with CLARE. 

**Algorithm 2** Autonomous routing during deployment. 

**Require:** Pre-trained base VLA with parameters **_θ_** 0, set of expandable layers _E_ , expansion threshold _γ_ . 

- 1: **for all** layers _ℓ ∈E_ **do** 2: Set _Aℓ_ = _∅_ , _kℓ_ = 0. _▷ Initialize adapter modules_ 3: Set _Dℓ_ = _∅_ . _▷ Initialize discriminator modules_ 4: **for all** tasks _Tn ∈{T_ 1 _, T_ 2 _, . . . }_ **do** _▷ Continual learn._ 5: Set **_θ_** _n ←_ **_θ_** _n−_ 1. 6: Collect demonstration data _Dn_ . 

- 7: **for all** layers _ℓ ∈E_ **do** _▷ Dynamic Expansion_ 8: **for all** discriminators _Dℓ_<sup>_j∈Dℓ_</sup><sup>**do**</sup> 9: Compute _z_ -score _zℓ_<sup>_j_via(7).</sup> 

- 10: Expand _Dℓ ←Dℓ ∪_ � _Dℓ_<sup>_n_</sup> �. _▷ New discriminator_ 11: Update model parameters: **_θ_** _n ←_ ( **_θ_** _n, Dℓ_<sup>_n_).</sup> 12: **if** _n_ = 1 or _zℓ_<sup>_j> γ_forall</sup><sup>_j_= 1</sup><sup>_, . . . , n −_1</sup><sup>**then**</sup> 13: Set _kℓ ← kℓ_ + 1. 14: Expand _Aℓ ←Aℓ ∪_ � _A_<sup>_k_</sup> _ℓ_<sup>_ℓ_</sup> �. _▷ New adapter_ 15: Update model parameters: **_θ_** _n ←_ ( **_θ_** _n, A_<sup>_k_</sup> _ℓ_<sup>_ℓ_).</sup> 16: Link new discriminator _Bℓ_ ( _Dℓ_<sup>_n_) =</sup><sup>_Ak_</sup> _ℓ_<sup>_ℓ_.</sup> 

- 17: **else** 

- 18: Link _Dℓ_<sup>_n_toanexistingadaptervia(8).</sup> 19: **if** _n >_ 1 and no layers _ℓ ∈E_ were expanded **then** 20: Expand the shallowest layer _ℓ_ 1 _∈E_ . 21: Re-link _Dℓ_<sup>_n_</sup> 1<sup>tothenewadapter.</sup> 22: Train all adapters added at stage _n_ from _Dn_ via (1). 23: Train _Dℓ_<sup>_n_ofalllayers</sup><sup>_ℓ∈E_from</sup><sup>_Dn_via(5).</sup> 

consisting of camera images **_I_** _t_<sup>1</sup><sup>_, . . . ,_</sup><sup>**_I_**</sup> _t_<sup>_N_c,proprioceptive</sup> state **_q_** _t_ and language command **_l_** , and generates an action chunk **_A_** _t_ = ( **_a_** _t, . . . ,_ **_a_** _t_ + _H−_ 1) _∼ π_ 0( _· |_ **_o_** _t_ ). The first _h ≤ H_ actions in **_A_** _t_ are applied to the robot, and the policy generates a new chunk at timestep _t_ + _h_ in a receding horizon manner [34]. Pre-training has provided the base VLA with general visual, language, and action representations, but it cannot solve new tasks zero-shot [6], [7]. 

The robot should be able to learn a new task _Tn_ at stage _n_ while retaining the general knowledge from pre-training and without forgetting how to solve previous tasks _T_ 1 _, . . . , Tn−_ 1. Specifically, given an expert demonstration dataset _Dn_ = _{_ ( **_o_**<sup>_n_</sup> _t_<sup>_,_</sup><sup>**_a_**</sup><sup>_n_</sup> _t_<sup>)</sup><sup>_,_</sup><sup>**_l_**</sup><sup>_n}T_</sup> _t_ =1<sup>ofobservation-action</sup> pairs for task _Tn_ , we aim to train a new policy _πn_ = _π_ **_θ_** _n_ with parameters **_θ_** _n_ . For the reasons discussed above, we consider exemplar-free continual learning, i.e., data from earlier stages _D_ 1 _, . . . , Dn−_ 1 are _not_ available. Hence, only the previous model parameters **_θ_** _n−_ 1 and the new data _Dn_ can be used to adapt the policy to the new task. 

### IV. METHODOLOGY 

This section details CLARE, our proposed continual learning framework for VLAs. The training and inference strategies are summarized in Algorithms 1 and 2. 

### _A. Base Policy_ 

To learn from high-dimensional, multimodal demonstration datasets, we train the policy using flow matching [20]. 

**Require:** Adapters _Aℓ_ , discriminators _Dℓ_ , learned linking _Bℓ_ : _Dℓ →Aℓ_ , input feature **_x_** _ℓ_ . 1: **for all** discriminators _Dℓ_<sup>_j∈Dℓ_</sup><sup>**do**</sup> 2: Compute the reconstruction error _e_<sup>_j_</sup> _ℓ_<sup>(</sup><sup>**_x_**</sup><sup>_ℓ_)via(4).</sup> 3: Select the most relevant adapter _A_<sup>_∗_</sup> _ℓ_<sup>_∈Aℓ_via(6).</sup> 4: Sum the outputs of original module and adapter via (3). 

The policy at stage _n_ learns a vector field **_vθ_** _n_ that transports action-chunk samples from a simple base distribution (e.g., a Gaussian) to the target distribution. We adopt the standard conditional flow matching loss 

_L_ ( **_θ_** _n_ )= E _s,_ ( **_A_** 1 _,_ **_o_** ) _,_ **_A_** 0<sup>���</sup> **_vθ_** _n_ ( **_A_**<sup>_s_</sup> _,_ **_o_** _, s_ ) _−_ ( **_A_**<sup>1</sup> _−_ **_A_**<sup>0</sup> )��2� _,_ (1) 

where _s ∼U_ ([0 _,_ 1]), ( **_A_**<sup>1</sup> _,_ **_o_** ) _∼Dn_ , **_A_**<sup>0</sup> _∼N_ ( **0** _,_ **_I_** ), and **_A_**<sup>_s_</sup> = (1 _− s_ ) **_A_**<sup>0</sup> + _s_ **_A_**<sup>1</sup> . After training, we can generate new action chunks **_A_** _t_ = **_A_**<sup>1</sup> _∼ πn_ ( _· |_ **_o_** _t_ ) by Euler integration of the learned vector field, starting from Gaussian noise **_A_**<sup>0</sup> _∼N_ ( **0** _,_ **_I_** ), via **_A_**<sup>_s_+</sup><sup>_δs_</sup> = **_A_**<sup>_s_</sup> + _δs_ **_vθ_** _n_ ( **_A_**<sup>_s_</sup> _,_ **_o_** _t, s_ ), with _K_ = 1 _/δs_ integration steps. As our method is architecture-agnostic, we keep the following sections general. 

### _B. Modularized Adapters_ 

The policy must continually acquire new task-specific knowledge, but it should leverage the general representations from pre-training to adapt to new tasks in a parameterefficient way. To achieve this, we draw inspiration from the mixture-of-experts (MoE) approach in large language models (LLMs) [35], [36], which combines the outputs of specialized sub-networks during inference. However, while their number is fixed in MoE, our setup requires continually injecting parameters into the model to learn new tasks, and we aim to do this in a memory-efficient way. 

Prior work [37], [38] has shown that a large fraction of factual associations and high-level knowledge in transformerbased LLMs is stored inside mid-layer feedforward network modules. Motivated by this insight, we define a set of _n_ e expandable modules _E_ = _{ℓ_ 1 _, . . . , ℓn_ e _}_ for continual learning. At each stage _n_ , at most one adapter module is added as a side branch to each expandable layer according to the dynamic expansion strategy detailed in Section IV-D. We employ a lightweight encoder-decoder structure with ReLU activation functions for the adapters. Denoting the input feature of an expandable layer _ℓ ∈E_ by **_x_** _ℓ ∈_ R<sup>_dℓ_</sup> , the output of the _i_ -th adapter in that layer is given by 


where **_W_** _ℓ,i_<sup>up</sup><sup>_∈_R</sup><sup>_dℓ×r_,</sup><sup>**_W_**down</sup> _ℓ,i ∈_ R<sup>_r×dℓ_</sup> , and _r ≪ dℓ_ . We denote the set of adapters in layer _ℓ_ at stage _n_ by _A_<sup>_n_</sup> _ℓ_<sup>=</sup> � _A_<sup>1</sup> _ℓ_<sup>_, . . . , Ak_</sup> _ℓ_<sup>_ℓ_</sup> � with _kℓ ≤ n_ . To maintain distinct representations for each task, we train only the newly added adapters on the data _Dn_ and freeze the rest of the model. During inference, a routing mechanism described in Section IVC activates one adapter _A_<sup>_∗_</sup> _ℓ_<sup>_∈Aℓ_perlayer,anditsoutputis</sup> 

added to that of the original pre-trained module _Mℓ_<sup>pre(</sup><sup>_·_)as</sup> 


Injecting adapters as parallel side branches to the model is beneficial as it preserves the network structure and does not change the input and output of existing layers and adapters. 

### _C. Autonomous Routing_ 

During deployment, a routing mechanism needs to determine which adapter _A_<sup>_∗_</sup> _ℓ ∈ Aℓ_ to activate in each layer _ℓ ∈E_ . This selection should be autonomous and based solely on the current observation, i.e., without requiring task labels, since these are typically not provided in open, real-world scenarios. Unlike fixed-size routing in MoE, our setup requires selecting from a continually increasing set of adapters. We achieve this by designing an expandable and lightweight routing mechanism that selects, for each expandable layer _ℓ ∈E_ , the adapter most relevant to the current situation, as shown in Figure 2. We pair each layer with an expanding set of autoencoder discriminators _Dℓ_ = _{Dℓ_<sup>1</sup><sup>_, D_</sup> _ℓ_<sup>2</sup><sup>_, . . . }_,allofwhichreceivethesamefea-</sup> tures **_x_** _ℓ_ as input, and attach a new discriminator _Dℓ_<sup>_n_at each</sup> stage _n_ . Every discriminator _Dℓ_<sup>_j_,</sup><sup>_j_=1</sup><sup>_, . . . , n_,islinkedto</sup> one corresponding adapter _A_<sup>_i_</sup> _ℓ_<sup>=</sup><sup>_Bℓ_(</sup><sup>_D_</sup> _ℓ_<sup>_j_) through a surjective</sup> mapping _Bℓ_ : _Dℓ →Aℓ_ , as explained in Section IV-D. We use the reconstruction errors of the discriminators 


## Autonomous Routing 


Fig. 2: CLARE sequentially adds adapters and discriminators as side branches to selected VLA modules. Top: During inference, our router activates only the most relevant adapter that is linked to the discriminator with the lowest reconstruction error for the input feature. Bottom: During dynamic expansion, if all _z_ -scores exceed a threshold _γ_ , a new adapter and discriminator are added to the corresponding layer. If at least one _z_ -score is smaller than _γ_ , we only add a discriminator and link it to the most relevant adapter. 

to determine the most relevant adapter. By training the discriminators added at stage _n_ with the loss 


we ensure they have a lower reconstruction error when the input features belong to the training distribution of their corresponding adapter. During inference, we activate the most relevant adapter linked to the discriminator with the smallest reconstruction error (4) via the routing mechanism 


The routing strategy for one layer is summarized in Algorithm 2. The distribution of features **_x_** _ℓ_ changes when training the adapters in the shallower layers. To nevertheless ensure stable discriminator training, we adopt a two-stage training strategy. First, we jointly train the new adapters using the flow-matching loss (1). Then, we freeze all parameters except for the new discriminators and train them using the reconstruction loss (5). We note that failed demonstrations, if available, could be added to the discriminators’ training data to improve the robustness of the routing mechanism. 

### _D. Dynamic Expansion_ 

To effectively capture task-specific knowledge without catastrophic forgetting in the context of exemplar-free continual learning, some model expansion is necessary for each new task. A straightforward approach would be to 

add new adapters to all expandable layers. However, this limits knowledge sharing between the tasks and leads to an excessive linear increase in the number of adapter parameters. Therefore, we only expand a layer _ℓ_ at stage _n_ if the features of the new task _Tn_ deviate substantially from all previous tasks. Since the discriminators are trained on different data, comparing their reconstruction losses requires normalization. To this end, we maintain the running mean _µ_<sup>_j_</sup> _ℓ_ and standard deviation _σℓ_<sup>_j_of the reconstruction loss for each</sup> discriminator _Dℓ_<sup>_j_andcalculatethenormalized</sup><sup>_z_-scores</sup> 


If all discriminators _Dℓ_<sup>1</sup><sup>_, . . . , D_</sup> _ℓ_<sup>_n−_1</sup> have a _z_ -score (7) larger than a threshold _γ_ , the features **_x_** _ℓ_ of the new task _Tn_ in layer _ℓ_ are out-of-distribution with respect to all previously learned tasks. In this case, we expand the layer by a new adapter _A_<sup>_k_</sup> _ℓ_<sup>_ℓ_</sup> and link the new discriminator _Dℓ_<sup>_n_toit,i.e.,</sup> _Bℓ_ ( _Dℓ_<sup>_n_) =</sup><sup>_Ak_</sup> _ℓ_<sup>_ℓ_.Conversely,ifatleastonediscriminator</sup><sup>_D_</sup> _ℓ_<sup>_j_</sup> yields a _z_ -score smaller than _γ_ , we deem that the layer _ℓ_ does not require expansion. This dynamic expansion strategy, illustrated in Figure 2, results in a memory-efficient, sublinear increase in the number of adapter parameters. Even if a layer is not expanded, we need to attach a new discriminator to it. To explain why, we consider the following scenario: Assume that at stage _n_ , a new adapter _A_<sup>_i_</sup> _ℓ_ 2<sup>is added</sup> 

||Ada|pters|Discrim|inators|
|---|---|---|---|---|
|Hyperparameter|Real|Sim.|Real|Sim.|
|# Params (linear proj.)|0.38M|3.2M|6.08M|1.4M|
|# Params (AdaLN)|0.75M|0.26M|1.00M|0.33M|
|Learning rate|2_×_10<sup>_−_4</sup>|1_×_10<sup>_−_4</sup>|5_×_|10<sup>_−_4</sup>|
|Learning rate schedule|cos|ine|cons|tant|
|Batch size|256|32|256|32|
|Training steps|20,|000|10,000|2,000|
|Expansion threshold _γ_|0.0|2.5||–|


TABLE I: Model and training hyperparameters. The injected modules are much smaller than the base policy, which has about 200M parameters. 

to layer _ℓ_ 2, but the shallower layer _ℓ_ 1 is not expanded. Then, the routing mechanism activates only adapters from earlier stages in layer _ℓ_ 1 during training of _A_<sup>_i_</sup> _ℓ_ 2<sup>.However,</sup> a new adapter _A_<sup>_j_</sup> _ℓ_ 1<sup>couldbeaddedtolayer</sup><sup>_ℓ_1atthenext</sup> stage _n_ + 1. In this case, when revisiting task _n_ , the router might activate the new adapter _A_<sup>_j_</sup> _ℓ_ 1<sup>insteadofanearlier</sup> one. As a consequence, the input features **_x_** _ℓ_ 2 to layer _ℓ_ 2 when performing task _Tn_ are _different_ from those seen during training of _A_<sup>_i_</sup> _ℓ_ 2<sup>.Thisdistributionshiftinfeaturespacecan</sup> lead to unpredictable behavior and task failure [39], [40]. To avoid this problem and ensure stable routing, we attach an _auxiliary discriminator_ if a layer is not expanded. The auxiliary discriminator is linked to the same adapter as the existing discriminator with the smallest reconstruction error (4), i.e., 


Intuitively, since adapter (8a) was trained on features most similar to task _Tn_ , we consider its learned representations to be transferable to _Tn_ . We note that with our dynamic expansion strategy, an adapter can potentially be activated by more than one discriminator, as shown in Figures 1 and 2. 

We found that introducing at least some new parameters per task is essential for the policy to acquire and retain novel skills. In addition, we observed that shallower layers typically exhibit a stronger distribution shift between tasks than deeper layers. Thus, if no layer is deemed to require expansion, we still add an adapter to the shallowest layer _ℓ_ 1 _∈E_ to capture the peculiarities of a new task. At the first stage, we expand all layers _ℓ ∈E_ by default. In summary, our dynamic expansion mechanism ensures that CLARE adds only a small, task-dependent number of parameters without compromising performance when revisiting previous tasks. 

### V. EVALUATION 

We conduct extensive simulation and real-world experiments with a focus on the following research questions: 

- **Q1:** Which layers are best suited for expansion? 

- **Q2:** How well can CLARE learn new tasks, and is the performance on previous tasks affected? 

- **Q3:** Can our autonomous dynamic expansion strategy reuse relevant skills from previous tasks? 


Fig. 3: Model architecture of our base VLA policy. The modules for inserting CLARE adapters are shown as dashed blocks. 

- **Q4:** What is the computational overhead of CLARE? 

### _A. Experimental Setup_ 

_1) Tasks:_ We conduct our simulation experiments using the LIBERO benchmark [33], which is designed specifically for continual learning. Here, a Panda manipulator with a parallel-yaw gripper needs to perform tasks in a kitchen environment, with 50 human expert demonstrations available per task. We pre-train the policy on 90 short-horizon tasks from LIBERO-90 and evaluate continual learning on 10 sequentially arriving tasks from LIBERO-Long, LIBEROGoal, and LIBERO-Spatial. These suites require the robot to understand language instructions and execute various motions, such as pick-and-place, opening a drawer, or turning a knob. 

We also conduct hardware experiments with an FR3 manipulator across five tasks, which are visualized in Figure 6: 

- 1) BOWL: Put a bowl on a plate. 

- 2) STACK: Stack a bowl on top of three other bowls. 

- 3) MOKA: Put a Moka pot on a stove. The pot weighs 0.5 kg and hangs at an angle when lifted by its handle. 

- 4) DRAWER: Close a drawer. The friction profile of the plastic drawer necessitates exerting considerable force. 

- 5) LEGO: Put a Lego block into the drawer and close it. 

We pre-train the policy on a mix of 1000 demonstrations collected in our lab for tasks different from the five continual learning tasks and 2000 episodes from the DROID dataset [9]. 

_2) Policy:_ The observations contain RGB images from wrist and third-person cameras, the end-effector pose and gripper state, and a language command. The policy generates chunks of _H_ = 16 end-effector displacement actions, and the first _h_ = 8 actions are sent to a Cartesian controller [41] at a frequency of 15 Hz (20 Hz in simulation). For our pre-trained base VLA, we adopt a decoder-only diffusion transformer (DiT-Dec) [42] architecture with 6 transformer 

|Backbone|Expandable layers|AUC _↑_|FWT _↑_|NBT _↓_|
|---|---|---|---|---|
|DiT-Dec|Linear projection<br>Decoder|**75.1**<sup>_±_1.3</sup><br>41.8<sup>_±_2.4</sup>|**75.0**<sup>_±_1.4</sup><br>45.5<sup>_±_3.8</sup>|**1.9**<sup>_±_0.4</sup><br>7.0<sup>_±_1.7</sup>|
|DiTED|Encoder|65.4<sup>_±_2.7</sup><br>|**66.5**<sup>_±_2.2</sup><br>|1.7<sup>_±_1.2</sup><br>|
|-ncec|Decoder|29.0<sup>_±_2.2</sup>|30.9<sup>_±_4.3</sup>|3.0<sup>_±_3.4</sup>|
||Encoder & Decoder|**66.6**<sup>_±_</sup><sup>**0.3**</sup>|65.8<sup>_±_0.4</sup>|**1.5**<sup>_±_</sup><sup>**0.7**</sup>|


TABLE II: In our ablation study on LIBERO-Long, adding adapters to the observation encoding modules is crucial to achieve strong performance. 


Fig. 4: CLARE scales to continual learning of 40 tasks on LIBERO-40, whereas experience replay (ER) exhibits significant performance degradation. 

layers and adaptive layer normalization (AdaLN) [43] conditioning, as visualized in Figure 3. We leverage pre-trained DINOv2 [44] and CLIP [45] vision and text encoders, freezing them during continual learning. The visual and language features, as well as the proprioceptive state, are first projected into tokens of the same dimension via linear layers before being fed into the transformer backbone. Adapters can be added to the linear projection layer of the encoder and the transformer layers in the decoder. As an ablation, we also consider an encoder-decoder backbone (DiT-EncDec), for which adapters can be added to all 12 transformer layers. Our training hyperparameters are provided in Table I. Training takes about one hour per simulation task and five hours per real-world task on an NVIDIA RTX 5090 GPU. 

_3) Metrics:_ We use three metrics to assess continual learning [33], [46]: Area under the success rate curve (AUC), forward transfer (FWT), and negative backward transfer (NBT). Denoting the success rate on task _n_ after learning the first _m ≥ n_ tasks as _rn|m_ , the metrics are defined as AUC = _N_ <u>1</u> � _Nn_ =1 � _N −_ <u>1</u> _n_ +1 � _Nm_ = _n_<sup>_rn|m_</sup> <u>�,</u> FWT = _N_ <u>1</u> � _Nn_ =1<sup>_rn|n_,</sup> and NBT = _N_ <u>1</u> _−_ 1 � _Nn_ =1 _−_ 1 � _N −_ <u>1</u> _n_ � _Nm_ = _n_ +1 � _rn|n − rn|m_ �<sup>�</sup> . Intuitively, AUC measures overall performance on new and old tasks, FWT quantifies the ability to learn new tasks, and NBT measures the degree of forgetting (lower being better). All numerical results are given in percentage points. 

_4) Evaluation Protocol:_ After each stage _n_ , we evaluate the policy on all previously learned tasks _T_ 1 _, . . . , Tn_ using 100 rollouts per task (10 in the real world), with different initial configurations of relevant objects. We average all simulation results across three random seeds. 

_5) Baselines:_ We include seven baselines for continual learning without oracle task IDs. **SeqFFT** [33], [47] sequentially fine-tunes the whole model for each new task. **SeqLoRA** [28] adds LoRA adapters to selected layers, which are merged back into the base model weights after training on a new task. We add LoRA adapters to all linear layers within the projection, attention, feedforward, and AdaLN modules. **PackNet** [26] freezes the most important 25% of model weights, and the remaining free weights are used to learn the next task. This process is repeated iteratively, with each new task having fewer free weights available. **ER** [13] trains the model on a mix of 50% previous and 50% new data for each new task. **LOTUS** [29] maintains a growing skill library and uses a meta policy to compose skills during deployment. **DMPEL** [17] builds an expert library and iteratively finetunes the router using expert coefficient replay. **MLR** [32] replays compact joint latent representations and regularizes task embeddings to preserve inter-task distinctiveness. 

### _B. Simulation Results_ 

To examine the impact of the set of layers to expand _E_ for LIBERO-Long, we set _γ_ = 0, i.e., an adapter is added to each expandable layer per new task. As shown in Table II, expanding only the encoder part of the model outperforms expanding only the decoder. This indicates that the policy’s observation-conditioning modules, which perform taskspecific modulations of the decoder’s action priors, are wellsuited to store new knowledge during continual learning. Hence, we adopt this expansion strategy in the subsequent experiments. 

Our baseline comparison is summarized in Table III. For DMPEL and MLR, we report the authors’ results. CLARE achieves the highest overall performance, as measured by AUC, outperforming the best baseline, ER, by about 10 to 14 percentage points. Compared to SeqFFT and ER, which fine-tune the full model, CLARE achieves comparable FWT, indicating that it can store new task-specific knowledge in much fewer parameters. Moreover, our method achieves approximately zero NBT, demonstrating that it can avoid forgetting without relying on exemplar data or oracle task identifiers. 

We examine long-term scalability on LIBERO-40, which concatenates all four standard LIBERO suites (LIBEROLong, -Goal, -Spatial, -Object). Due to computational constraints, we perform only 10 rollouts per task and stage across three seeds. As shown in Figure 4, CLARE can sequentially learn and retain 40 distinct tasks, demonstrating the scalability and robustness of our autonomous routing strategy. In contrast, ER cannot avoid catastrophic forgetting of several tasks (e.g., _T_ 1 and _T_ 7), yielding an NBT of 23%. 

We evaluate the impact of the expansion threshold _γ_ for DiT-EncDec with expandable encoder layers and report the results in Figure 5. Increasing _γ_ from 0 to 20 reduces the number of added adapters from 60 to 16, resulting in a slight decrease in AUC and FWT. Intuitively, compressing new knowledge into fewer model parameters reduces the robot’s ability to learn novel tasks. Yet, AUC remains higher than 

||L|IBERO-Lon|g|L|IBERO-Goa|l|LI|BERO-Spat|ial|
|---|---|---|---|---|---|---|---|---|---|
|Method|AUC _↑_|FWT _↑_|NBT _↓_|AUC _↑_|FWT _↑_|NBT _↓_|AUC _↑_|FWT _↑_|NBT _↓_|
|SeqFFT|22.4<sup>_±_0.3</sup><br>|76.1<br>_±_1.0<br>|74.7<sup>_±_1.1</sup><br>|26.7<sup>_±_0.9</sup><br>|94.1<br>_±_0.2<br>|95.3<sup>_±_1.4</sup><br>|27.7<sup>_±_0.6</sup><br>|**94.7**<sup>_±_0.3</sup><br>|94.6<sup>_±_0.9</sup><br>|
|SeqLoRA|21.4<sup>_±_1.0</sup><br>|73.1<sup>_±_1.8</sup><br>|71.6<sup>_±_1.6</sup><br>|26.1<sup>_±_0.3</sup><br>|90.1<sup>_±_1.6</sup><br>|90.8<sup>_±_1.7</sup><br>|27.3<sup>_±_1.3</sup><br>|90.1<sup>_±_2.1</sup><br>|89.2<sup>_±_1.3</sup><br>|
|PackNet|4.8<sup>_±_0.2</sup><br>|37.2<sup>_±_1.0</sup><br>|41.3<sup>_±_1.2</sup><br>|10.5<sup>_±_0.3</sup><br>|60.3<sup>_±_1.0</sup><br>|67.0<sup>_±_1.1</sup><br>|8.6<sup>_±_0.1</sup><br>|54.7<sup>_±_0.5</sup><br>|60.3<sup>_±_0.7</sup><br>|
|ER|60.5<br>_±_0.2<br>|**76.6**<sup>_±_0.9</sup><br>|22.7<sup>_±_1.8</sup><br>|76.0<sup>_±_0.9</sup><br>|**94.4**<sup>_±_0.7</sup><br>|25.1<sup>_±_0.5</sup><br>|77.6<br>_±_0.8|92.7<br>_±_1.0|20.9<sup>_±_2.0</sup>|
|LOTUS|52.9<sup>_±_1.6</sup><br>|58.1<sup>_±_0.2</sup><br>|**-7.2**<sup>_±_3.0</sup><br>|56.0<sup>_±_1.0</sup><br>|61.0<sup>_±_3.0</sup><br>|30.0<sup>_±_1.0</sup><br>|NA<br>|NA<br>|NA<br>|
|DMPEL|58<sup>_±_3</sup>|55<sup>_±_4</sup>|7<sup>_±_1</sup>|78<br>_±_2|68<sup>_±_2</sup>|**0**<sup>_±_1</sup>|70<sup>_±_3</sup>|64<sup>_±_2</sup>|3<br>_±_1|
|MLR|NA<br>|NA<br>|NA<br>|77.2<sup>_±_1.8</sup><br>|80.0<sup>_±_2.5</sup><br>|6.9<sup>_±_0.9</sup><br>|NA<br>|NA<br>|NA<br>|
|**CLARE (ours)**|**75.1**<sup>_±_1.3</sup>|75.0<sup>_±_1.4</sup>|1.9<br>_±_0.4|**89.3**<sup>_±_1.1</sup>|89.7<sup>_±_1.5</sup>|**0.3**<sup>_±_1.1</sup>|**87.4**<sup>_±_2.3</sup>|88.0<sup>_±_1.9</sup>|**0.9**<sup>_±_0.6</sup>|


TABLE III: Baseline comparison across three LIBERO suites. CLARE achieves the highest overall performance, as measured by AUC, and demonstrates strong capabilities to acquire new skills without forgetting. “NA” indicates not available. 


Fig. 5: Increasing the dynamic expansion threshold _γ_ reduces the number of added adapters and, consequently, the capability to learn new tasks (lower FWT), but does not lead to catastrophic forgetting (approximately zero NBT). 


Fig. 6: Our five real-world manipulation tasks involve objects of different shapes, weights, and dynamics, as well as different motion patterns. 

for ER, and NBT stays close to zero, indicating that the policy does not exhibit forgetting even when only a few adapters are added per task. Comparing the results in Table II and Figure 5, we find that the choice of expandable layers can have a stronger impact than the expansion threshold value. In summary, _γ_ should be chosen based on the importance of high task performance versus low memory requirements. 

|Method|AUC _↑_|FWT _↑_|NBT _↓_|
|---|---|---|---|
|SeqFFT|23.8|**68.0**|80.0|
|SeqLoRA|22.9|64.0|76.9|
|ER|51.1|60.0|17.1|
|**CLARE (ours)**|**63.3**|62.0|**-2.9**|


TABLE IV: Overall results in our hardware experiments. 

||1. B|OWL|2. S|TACK|3. M|OKA|4. DR|AWER|5.|LEGO|
|---|---|---|---|---|---|---|---|---|---|---|
|Stage|➀|➁|➀|➁|➀|➁|➀|➁|➀|➁|
|1|**100**|**100**|–|–|–|–|–|–|–|–|
|2|**100**|80|**70**|50|–|–|–|–|–|–|
|3|**80**|**80**|50|**60**|**20**|**20**|–|–|–|–|
|4|80|**90**|**70**|50|20|**50**|80|**90**|–|–|
|5|60|**90**|50|**60**|10|**30**|50|**90**|30|**50**|


TABLE V: Evolution of per-task success rates [%] across all stages in our real-world experiments. ➀ ER, ➁ CLARE. 


Fig. 7: Inference time and memory complexity of CLARE in our hardware experiments. The values for stages 6-10 are linearly extrapolated. 

### _C. Real-World Results_ 

Given the importance of expanding the observation encoding modules (see Table II), we add adapters to the linear projection layers and the scaling and shifting AdaLN modules of each transformer decoder layer for our hardware experiments. To keep inference latency and memory overhead low, we implement the adapters using LoRA. Due to the scale of the hardware evaluation, we focus on three baselines: SeqFFT, SeqLoRA, and ER. The results are provided in Tables IV and V. CLARE achieves an AUC of 63%, which is 12 percentage points higher than ER, and shows no catastrophic forgetting with an NBT of -2.9%. SeqFFT and SeqLoRA achieve high performance on new tasks, but cannot sufficiently retain the relevant representations from previous tasks. In summary, CLARE demonstrates strong capabilities for continual learning under real-world operating conditions. 

Figure 7 analyzes the inference time and memory overhead of CLARE. The inference-time overhead relative to the base policy is below 3 ms, and GPU VRAM utilization increases only by about 2% per task. Compared to explicitly storing data from previous tasks for ER, our approach of acquiring new skills by training dedicated lightweight modules is more storage-efficient and reduces forgetting to near zero in our experiments. 

### VI. CONCLUSIONS 

CLARE enables continual learning without forgetting in VLAs, requiring neither stored exemplars nor task IDs. By combining lightweight adapters, an autonomous expansion strategy, and an autoencoder-based routing module, our approach increases model capacity only when needed while retaining prior representations. Across multiple LIBERO suites, CLARE achieves and maintains high task success, outperforming even strong baselines that have access to previous data. Hardware experiments on five manipulation tasks with diverse interaction dynamics confirm these findings, demonstrating the potential of CLARE for long-term deployment of robots in non-stationary, real-world environments. 

### ACKNOWLEDGEMENTS 

This work was supported by the German Federal Ministry of Research, Technology and Space (BMFTR) under the Robotics Institute Germany (RIG) funded by BMFTR grant 16ME0997K, the German Research Foundation (DFG) within the RTG project ConVeY funded by grant GRK 2428, and the Humboldt Professorship for Robotics and Artificial Intelligence. 

### REFERENCES 

- [1] G. I. Parisi, R. Kemker, J. L. Part, C. Kanan, and S. Wermter, “Continual lifelong learning with neural networks: A review,” _Neural Networks_ , vol. 113, pp. 54–71, 2019. 

- [2] S. Thrun and T. M. Mitchell, “Lifelong robot learning,” _Robotics and Autonomous Systems_ , vol. 15, no. 1, pp. 25–46, 1995. 

- [3] A. Billard _et al._ , “A roadmap for AI in robotics,” _Nature Machine Intelligence_ , vol. 7, no. 6, pp. 818–824, 2025. 

- [4] S. Dohare, J. F. Hernandez-Garcia, Q. Lan, P. Rahman, A. R. Mahmood, and R. S. Sutton, “Loss of plasticity in deep continual learning,” _Nature_ , vol. 632, no. 8026, pp. 768–774, 2024. 

- [5] M. J. Kim _et al._ , “OpenVLA: An open-source vision-language-action model,” in _Conference on Robot Learning_ , 2025, pp. 2679–2713. 

- [6] P. Intelligence _et al._ , “ _π_ 0 _._ 5: A vision-language-action model with open-world generalization,” _Conference on Robot Learning_ , 2025. 

- [7] M. Reuss, H. Zhou, M. R¨uhle, O.<sup>¨</sup> E. Ya˘gmurlu, F. Otto, and R. Lioutikov, “FLOWER: Democratizing generalist robot policies with efficient vision-language-action flow policies,” in _Conference on Robot Learning_ , 2025. 

- [8] M. Shukor _et al._ , “SmolVLA: A vision-language-action model for affordable and efficient robotics,” _arXiv preprint arXiv:2506.01844_ , 2025. 

- [9] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis _et al._ , “DROID: A large-scale in-the-wild robot manipulation dataset,” in _Robotics: Science and Systems_ , 2024. 

- [10] A. O’Neill _et al._ , “Open X-embodiment: Robotic learning datasets and RT-X models,” in _Proceedings of the IEEE International Conference on Robotics and Automation_ , 2024, pp. 6892–6903. 

- [11] R. M. French, “Catastrophic forgetting in connectionist networks,” _Trends in Cognitive Sciences_ , vol. 3, no. 4, pp. 128–135, 1999. 

- [12] D. Lopez-Paz and M. Ranzato, “Gradient episodic memory for continual learning,” _Advances in Neural Information Processing Systems_ , 2017. 

- [13] A. Chaudhry _et al._ , “On tiny episodic memories in continual learning,” _arXiv preprint arXiv:1902.10486_ , 2019. 

- [14] A. Xie and C. Finn, “Lifelong robotic reinforcement learning by retaining experiences,” in _Conference on Lifelong Learning Agents_ . PMLR, 2022, pp. 838–855. 

- [15] Z. Liu _et al._ , “TAIL: Task-specific adapters for imitation learning with large pretrained models,” _International Conference on Learning Representations_ , 2024. 

- [16] H. Wang, H. Lu, L. Yao, and D. Gong, “Self-expansion of pre-trained models with mixture of adapters for continual learning,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 10 087–10 098. 

- [17] Y. Lei, S. Mao, S. Zhou, H. Zhang, X. Li, and P. Luo, “Dynamic mixture of progressive parameter-efficient expert library for lifelong robot learning,” _arXiv preprint arXiv:2506.05985_ , 2025. 

- [18] Y. Wang _et al._ , “Sparse diffusion policy: A sparse, reusable, and flexible policy for robot learning,” in _Conference on Robot Learning_ , 2024. 

- [19] J. Ho, A. Jain, and P. Abbeel, “Denoising diffusion probabilistic models,” _Advances in Neural Information Processing Systems_ , pp. 6840–6851, 2020. 

- [20] Y. Lipman, R. T. Chen, H. Ben-Hamu, M. Nickel, and M. Le, “Flow matching for generative modeling,” in _International Conference on Learning Representations_ , 2023. 

- [21] X. Chen _et al._ , “PaLI-3 vision language models: Smaller, faster, stronger,” _arXiv preprint arXiv:2310.09199_ , 2023. 

- [22] F. Lin, Y. Hu, P. Sheng, C. Wen, J. You, and Y. Gao, “Data scaling laws in imitation learning for robotic manipulation,” in _International Conference on Learning Representations_ , 2025. 

- [23] D.-W. Zhou _et al._ , “Learning without forgetting for vision-language models,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 47, no. 6, pp. 4489–4504, 2025. 

- [24] J. Kirkpatrick _et al._ , “Overcoming catastrophic forgetting in neural networks,” _Proceedings of the National Academy of Sciences_ , vol. 114, no. 13, pp. 3521–3526, 2017. 

- [25] F. Zenke, B. Poole, and S. Ganguli, “Continual learning through synaptic intelligence,” in _International Conference on Machine Learning_ , 2017, pp. 3987–3995. 

- [26] A. Mallya and S. Lazebnik, “Packnet: Adding multiple tasks to a single network by iterative pruning,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2018, pp. 7765–7773. 

- [27] A. A. Rusu _et al._ , “Progressive neural networks,” _arXiv preprint arXiv:1606.04671_ , 2016. 

- [28] E. J. Hu _et al._ , “LoRA: Low-rank adaptation of large language models.” in _International Conference on Learning Representations_ , 2022. 

- [29] W. Wan, Y. Zhu, R. Shah, and Y. Zhu, “LOTUS: Continual imitation learning for robot manipulation through unsupervised skill discovery,” in _Proceedings of the IEEE International Conference on Robotics and Automation_ , 2024, pp. 537–544. 

- [30] Y. Zhu, P. Stone, and Y. Zhu, “Bottom-up skill discovery from unsegmented demonstrations for long-horizon robot manipulation,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 2, pp. 4126–4133, 2022. 

- [31] L. Xie, Y. Li, and H. Zhuang, “Analytic task scheduler: Recursive least squares based method for continual learning in embodied foundation models,” _arXiv preprint arXiv:2506.09623_ , 2025. 

- [32] F. Yu, M. Tiezzi, T. Apicella, C. Beyan, and V. Murino, “Lifelong imitation learning with multimodal latent replay and incremental adjustment,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2026. 

- [33] B. Liu _et al._ , “LIBERO: Benchmarking knowledge transfer for lifelong robot learning,” _Advances in Neural Information Processing Systems_ , pp. 44 776–44 791, 2023. 

- [34] C. Chi _et al._ , “Diffusion policy: Visuomotor policy learning via action diffusion,” in _Robotics: Science and Systems_ , 2023. 

- [35] N. Shazeer _et al._ , “Outrageously large neural networks: The sparselygated mixture-of-experts layer,” in _International Conference on Learning Representations_ , 2017. 

- [36] D. Dai _et al._ , “DeepSeekMoE: Towards ultimate expert specialization in mixture-of-experts language models,” in _Annual Meeting of the_ 

_Association for Computational Linguistics (Volume 1: Long Papers)_ , 2024, pp. 1280–1297. 

- [37] K. Meng, D. Bau, A. Andonian, and Y. Belinkov, “Locating and editing factual associations in gpt,” _Advances in Neural Information Processing Systems_ , pp. 17 359–17 372, 2022. 

- [38] M. Geva, R. Schuster, J. Berant, and O. Levy, “Transformer feedforward layers are key-value memories,” in _Proceedings of the Conference on Empirical Methods in Natural Language Processing_ , 2021, pp. 5484–5495. 

- [39] Q. Gu _et al._ , “SAFE: Multitask failure detection for vision-languageaction models,” _Advances in Neural Information Processing Systems_ , 2025. 

- [40] R. R¨omer, A. Kobras, L. Worbis, and A. P. Schoellig, “Failure prediction at runtime for generative robot policies,” _Advances in Neural Information Processing Systems_ , 2025. 

- [41] D. S. J. Pro, O. Hausd¨orfer, R. R¨omer, M. D¨osch, M. Schuck, and A. P. Schoellig, “Crisp-compliant ros2 controllers for learningbased manipulation policies and teleoperation,” _IEEE Robotics and Automation Practice_ , 2026. 

- [42] S. Dasari, O. Mees, S. Zhao, M. K. Srirama, and S. Levine, “The ingredients for robotic diffusion transformers,” in _Proceedings of the IEEE International Conference on Robotics and Automation_ , 2025. 

- [43] W. Peebles and S. Xie, “Scalable diffusion models with transformers,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2023, pp. 4195–4205. 

- [44] M. Oquab _et al._ , “DINOv2: Learning robust visual features without supervision,” _Transact. on Machine Learning Research_ , 2024. 

- [45] A. Radford _et al._ , “Learning transferable visual models from natural language supervision,” in _International Conference on Machine Learning_ . PMLR, 2021, pp. 8748–8763. 

- [46] N. D´ıaz-Rodr´ıguez _et al._ , “Don’t forget, there is more than forgetting: New metrics for continual learning,” in _Continual Learning Workshop at NeurIPS 2018_ , 2018, pp. 1–7. 

- [47] L. Ouyang _et al._ , “Training language models to follow instructions with human feedback,” _Advances in Neural Information Processing Systems_ , pp. 27 730–27 744, 2022. 

### VII. APPENDIX 

### _A. Details about the Experimental Setup_ 

Our five real-world tasks shown in Figure 6 introduce multiple levels of diversity: 

- _Different objects_ : The tasks involve bowls, a plate, a moka pot, a stove, a drawer, and Lego blocks. Besides visual differences, these objects also have very different weights. For example, the moka pot weighs 0 _._ 5 kg, about 70 times as much as the Lego block. 

- _Grasp configurations_ : The tasks require different gripper widths (e.g., fully closed for the bowls and about half-closed for the Lego block) and angles (vertical for the Lego block and at a 30° angle to close the drawer) for object manipulation. 

- _Dynamic differences_ : The tasks involve distinct interaction dynamics between the robot and its environment. For example, in MOKA, the moka pot hangs at an angle when lifted by its handle, and the robot must use friction between the pot and the stove to place it upright. In DRAWER and LEGO, the plastic drawer compartment exhibits a strongly nonlinear friction profile, requiring the robot to exert significant force to close the drawer. 

- _Strategy switching_ : LEGO, for example, consists of three stages: picking up the block, placing it in the drawer, and closing the drawer. 

### _B. Additional Experiments_ 

Figure 8 shows the continual learning behavior on LIBERO-Long for a selected set of baselines. These results 

||1. B|OWL|2. S|TACK|3. M|OKA|4. DR|AWER|5.|LEGO|
|---|---|---|---|---|---|---|---|---|---|---|
|Stage|➂|➅|➂|➅|➂|➅|➂|➅|➂|➅|
|1|90|**100**|–|–|–|–|–|–|–|–|
|2|**100**|80|20|**50**|–|–|–|–|–|–|
|3|**100**|80|20|**60**|**20**|**20**|–|–|–|–|
|4|**90**|**90**|40|**50**|40|**50**|60|**90**|–|–|
|5|**100**|90|**60**|**60**|20|**30**|60|**90**|30|**50**|


TABLE VI: Evolution of per-task success rates [%] across all stages in our real-world experiments for different numbers of expandable AdaLN modules. ➂ three modules, ➅ six modules. 

further demonstrate that CLARE does not exhibit catastrophic forgetting while achieving a high overall success rate across tasks. 

In another experiment, we investigate how quickly and reliably the router responds to _changes_ in the active task during deployment. To this end, we change the language command from _“put the Lego block into the drawer”_ to _“close the drawer”_ mid-execution after three seconds. The router immediately switches to the correct adapter; the robot stops approaching the block and moves directly toward the drawer. An exemplary rollout is shown in Figure 9. Crucially, tasks DRAWER and LEGO involve almost identical scenes (same workbench, same drawer), so the router must rely on subtle differences in the language and proprioceptive features to distinguish them. This behavior was consistent across 10 rollouts, demonstrating that our reconstruction-based routing can robustly switch capabilities to adapt to dynamic context changes during deployment. We further test the router in a continuous multi-task scenario: by changing the language prompt and rearranging the scene between tasks, CLARE successfully completes a sequence of three different tasks (LEGO _→_ BOWL _→_ DRAWER) without any task identifiers, activating the correct adapter for each context. 

We also evaluate the impact of the number of expandable AdaLN modules in our hardware experiments and provide the results in Table VI. Injecting adapters into all scale and shift modules performs best. 

### _C. Extended Discussion_ 

In our ablation experiment (see Table II), expanding only the encoder performs similarly to expanding both the encoder and the decoder, but much better than expanding only the decoder. Our main conclusion from these results is that the observation-conditioning modules are crucial for injecting adapters during continual learning. 

Based on these findings, we expand only the modules in the conditioning pathway of the DiT-Dec architecture for our real-world experiments: 1) the linear layers projecting the observation features into the same token dimension, and 2) the scale and shift AdaLN modules, which inject the observation condition into the transformer decoder layers. Our hardware experiments involve changes in daylight, reflections, and slight drifts of the camera extrinsics. 

Despite the physical diversity of the real-world tasks, CLARE achieves an AUC of 63 _._ 3% and a near-zero NBT of _−_ 2 _._ 9% in our hardware experiments (see Table IV), 


Fig. 8: Success rate curves of CLARE and five baselines on the LIBERO-Long benchmark. The solid lines represent the average success rates across three random seeds, and the shaded regions indicate the standard deviations. The results demonstrate that our method achieves a higher overall success rate and mitigates catastrophic forgetting more effectively during continual learning than the baselines, despite ER and LOTUS using previous data. 

significantly outperforming all baselines. The detailed perstage success rates in Table V further confirm that our expansion strategy preserves performance on earlier tasks even as new, physically distinct tasks are learned. These results empirically validate that focusing the expansion on the observation-conditioning pathway is not a bottleneck for physical dynamics in our setup, supporting the conclusion drawn from the simulation ablation. However, we note that this expansion strategy assumes that the VLA has been pretrained on a sufficiently large dataset of robot demonstrations that cover diverse motion patterns. With the availability of large-scale robotic datasets, such as DROID [9], we believe this prerequisite can be met for common robot embodiments. 


Fig. 9: When changing the language command during execution, CLARE correctly adapts its behavior by switching the activated adapters. 

