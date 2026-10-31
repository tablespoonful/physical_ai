---
title: "SkillVLA: Tackling Combinatorial Diversity in Dual-Arm Manipulation via Skill Reuse"
date: "2026-03-04"
authors: "Xuanran Zhai; Zekai Huang; Longyan Wu; Qianyou Zhao; Qiaojun Yu; Jieji Ren"
venue: "RSS 2026"
url: https://arxiv.org/abs/2603.03836
pdf: https://arxiv.org/pdf/2603.03836
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.03836)** / [論文ページ](https://arxiv.org/abs/2603.03836)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Robotics: Science and Systems 2026 Sydney, Australia, July 13–17, 2026** 

# SkillVLA: Tackling Combinatorial Diversity in Dual-Arm Manipulation via Skill Reuse 

Xuanran Zhai<sup>_⇤_1</sup> , Zekai Huang<sup>_⇤_1</sup> , Longyan Wu<sup>_⇤_3</sup><sup>_,_6</sup> , Qianyou Zhao<sup>5</sup> , Qiaojun Yu<sup>4</sup> , Jieji Ren<sup>5</sup> , Ce Hao<sup>_†_1</sup><sup>_,_2</sup> , and Harold Soh<sup>1</sup><sup>_,_7</sup> 

> 1National University of Singapore, 2Zhongguancun Academy, 3Shanghai Innovation Institute, 

- 4Shanghai AI Laboratory, 5Shanghai Jiao Tong University, 6Fudan University, 7Smart Systems Institute, NUS 

> _⇤_ Equal contribution. _†_ Corresponding author: cehao@u.nus.edu, haoce@bza.edu.cn 


Fig. 1: SkillVLA extracts single-arm skills from training data with hierarchical reasoning and skill-adaptive learning, being able to recompose them into unseen combinations during test time. 

**_Abstract_ —Recent progress in vision–language–action (VLA) models has demonstrated strong potential for dual-arm manipulation, enabling complex behaviors and generalization to unseen environments. However, mainstream bimanual VLA formulations largely overlook the critical challenge of** **_combinatorial diversity_ . Different pairings of single-arm behaviors can induce qualitatively distinct task behaviors, yet existing models do not explicitly account for this structure. We argue that effective bimanual VLAs should support skill reuse—the ability to recombine previously learned single-arm skills across novel left–right pairings—thereby avoiding the need to separately learn every possible combination. Current VLA designs entangle skills across arms, preventing such recomposition and limiting scalability. To address this limitation, we propose SkillVLA, a framework explicitly designed to enable skill reuse in dual-arm manipulation. Extensive experiments demonstrate that SkillVLA substantially improves skill composition, increasing zero-shot recomposition success rate from** 0% **to** 51% **, and achieves strong performance on cooperative and long-horizon tasks.** 

## I. INTRODUCTION 

Bimanual manipulation expands a robot’s effective workspace and enables concurrent, coordinated actions, supporting a wider range of tasks than single-arm systems [44, 66, 55, 16, 13, 28]. In this context, recent vision–language–action (VLA) models [8, 27, 31, 47, 45, 52] have shown impressive performance on bimanual manipulation; by jointly predicting both arms’ actions (e.g., via a concatenated action vector) 

with large-capacity architectures, VLA methods can represent complex coordinated behaviors. Further, by leveraging vision– language pretraining of VLM models, recent bimanual VLAs have shown the ability to generalize to novel scenes and instructions [27, 17, 26, 5, 7, 4, 8, 29]. 

Despite recent progress, learning generalist bimanual policies remains challenging, as dual-arm control introduces richer behavior patterns. Specifically, real-world bimanual behaviors exhibit pronounced **_combinatorial diversity_** . As shown in Fig. 1, many dual-arm tasks can be viewed as compositions of single-arm behaviors, and different pairings of leftand right-arm skills induce different bimanual tasks. As the underlying skill set grows, the number of possible pairings increases quadratically, resulting in an overwhelming number of combinations corresponding to different tasks. Current VLA formulations largely overlook combinatorial diversity. Predicting both arms via action concatenation requires the model to learn the joint distribution of left- and right-arm distributions. While this design is simple and captures tight coordination, it confines outputs to action pairings observed in demonstrations. As a result, the policy has limited combinatorial generalization and cannot form new bimanual behaviors by recombining single-arm skills, which makes them unable to address combinatorial diversity. We refer to this limitation as **_skill entanglement_** and analyze it in detail in Sec. IV-C. 

To address the combinatorial diversity, a model must be able to effectively reuse robot skills learned from given demonstrations in a more flexible and thorough way. We name this ability as **_skill reuse_** . Concretely, instead of mechanically treating every bimanual behavior as an indivisible dual-arm primitive, an ideal model should automatically uncover the latent skill structure within demonstrations and perform reasoning at the skill level. For bimanual behaviors that are essentially compositions of single-arm skills, the model should reuse the discovered skills across different left–right combinations and compose them to form novel pairings that are not explicitly observed during training. We view such flexible reuse as a key foundation for broad generalization in bimanual settings, and provide a more formal definition and discussion in Sec. IV. 

We propose **SkillVLA** to enable skill reuse and address combinatorial diversity. Unlike conventional VLAs relying on monolithic dual-arm reasoning throughout, SkillVLA automatically identifies skill structures from demonstrations and performs _skill-adaptive_ action generation. Concretely, for singlearm skills, it can retrieve and invoke them as independent units for recomposition or further adaptation. For behaviors that require cooperation, the model instead captures interarm dependence. SkillVLA achieves this with a two-level reasoning architecture. A shared high-level VLM, equipped with a cooperation estimator, captures global task intent and makes skill decisions. At the lower level, the policy follows the high-level instruction and switches between operation modes: it performs per-arm reasoning and action generation for single-arm skills, while allowing these two streams to be entangled by communication when cooperative behavior is deemed necessary by the high-level reasoning. Through skilladaptive generation and per-arm reasoning, SkillVLA further exploits the VLM’s capability by extending reasoning to a finer semantic granularity, leading to stronger generalization. 

We conduct real-robot experiments on 20 manipulation tasks and two long-horizon multi-stage tasks to validate SkillVLA’s skill reuse and generalization ability. First, to evaluate if models are able to tackle combinatorial diversity, we test them on unseen tasks composed by learned skills, where strong bimanual VLA baselines achieve near-zero success due to skill entanglement. SkillVLA raises the success rate to **51** %, demonstrating a decisive improvement in combinatorial generalization. Second, to confirm that our method does not sacrifice inter-arm cooperation, we evaluate on three highlycooperative tasks, where SkillVLA matches the performance of the baselines, showing that its adaptive communication remains expressive for close coordination. Third, we study two multi-stage long-horizon tasks that interleave collaborative and independent phases. While SkillVLA correctly identifies the cooperation level required and, further, completes the tasks faster by recomposing skills to parallelize the two arms when possible, reducing execution time by **21** %. Finally, we conduct a continual-learning study to show that skill reuse also benefits long-term skill learning: SkillVLA can effectively reuse existing behaviors for acquiring new skills, achieving significantly better performance under limited demonstrations. 

In summary, this paper makes three main contributions: 

- We identify the _skill entanglement_ issue in current VLAs and formulate the bimanual _skill reuse_ problem. 

- We propose SkillVLA, which enables flexible skill reuse to tackle combinatorial diversity. 

- We validate SkillVLA on a real dual-arm robot, demonstrating combinatorial generalization ability via skill reuse, while maintaining strong performance on cooperative and long-horizon tasks. 

## II. RELATED WORK 

Dual-arm manipulation has long been a central topic in robotics. Early control-based or rule-based methods are often developed around specific task structures, leading to taskcentric designs for applications such as assembly [20, 63], cloth folding [35, 6, 54, 41, 10, 2, 15], and bagging [12, 3, 11]. For dual-arm manipulation, many traditional methods explicitly model bimanual relations, such as master–slave coordination [23, 46, 1], relative pose control [48, 39, 37], and internal force regulation [9, 42, 49]. These methods can be effective within a specific family of tasks and under controlled conditions, but their generalization to multitask settings or unfamiliar environments remains limited, as their coordination strategies are usually designed for particular objects, task procedures, or interaction patterns. 

Learning-based methods [14, 62, 61, 22] form another major family of manipulation approaches. By learning from expert demonstrations, they have been applied to a broad range of settings, including dexterous end-effectors [50, 43, 18], mobile manipulation [56, 19], learning from human videos [66, 21, 38], and multitask learning [22, 51]. Owing to their flexibility, imitation learning methods have become a dominant paradigm for robot manipulation. More recently, large-scale pretraining with vision-language-action models [58, 8, 27, 59, 17, 53, 67, 64] and world-action models [65, 57, 34, 60] has made generalist robot policies increasingly feasible. Recent policies have shown promising generalization to unseen environments without task-specific finetuning. 

However, unlike control-based bimanual methods, most learning-based methods still treat dual-arm robots as a monolithic system and learn a joint policy over the two arms. This formulation is simple and scalable, but it largely overlooks the structural differences between bimanual manipulation and single-arm manipulation, such as role assignment, asymmetric cooperation, cross-arm dependency, and coordinated skill reuse. Only a few recent works [25, 33, 36] have begun to decompose dual-arm learning to improve learning efficiency. To the best of our knowledge, skill recomposition in bimanual manipulation remains underexplored and has not been systematically addressed. 

## III. PROBLEM FORMULATION 

We consider a bimanual robot with left and right manipulators. At each time step, the robot receives an input _x 2 X_ (usually observation, instruction and robot state) and produces 

actions _aL 2 AL_ and _aR 2 AR_ ; we write _a_ = ( _aL, aR_ ). We are given a dataset of demonstrations _D_ = _{_ ( _xi, a_<sup>_i_</sup> _L_<sup>_, ai_</sup> _R_<sup>)</sup><sup>_}_</sup> _i_<sup>_I_</sup> =1<sup>,</sup> where each tuple is a state–action sample extracted from expert trajectories. We assume these expert actions are generated by executing skills drawn from an underlying skill set 

_S_ = _S_ pair _[ SD, S_ pair = _{_ ( _sL_<sup>_m, sm_</sup> _R_<sup>)</sup><sup>_}_</sup> _m_<sup>_M_</sup> =1<sup>_,SD_=</sup><sup>_{s_</sup> _D_<sup>_n}N_</sup> _n_ =1 

where _SL_ and _SR_ are the single-arm skill sets for the left and right arm ( _Def._ 1), and _SD_ is a set of genuinely dualarm (bimanual) skills ( _Def._ 2). Here _S_ pair collects the _paired_ single-arm skills that actually appear in the demonstrations. 

Our goal is to learn a bimanual policy _⇡✓_ ( _aL, aR | x_ ) that is able to effectively **_reuse_** these learned skills ( _Def._ 3), which we view as a key factor for resolving combinatorial diversity in generalist bimanual manipulation policies. 

IV. SKILL REUSE IN DUAL-ARM MANIPULATION 

In this section, we first give specific definitions of skills and skill reuse (Sec. IV-A), then we analyze what is required to solve this problem: for skill reuse to be possible, the model must (i) select suitable skills for any given scene _x_ (Sec. IV-B), and (ii) generate correct actions for the selected skill (or skill pair). The latter motivates explicitly distinguishing between single-arm and dual-arm skills during training and execution, which current VLA-based methods do not support (Sec. IV-C). 

## _A. Definitions_ 

To formulate and analyze skill reuse in a general bimanual setting, we first define what we mean by a _skill_ . We distinguish between _single-arm skills_ , which can be executed by one arm in isolation, and _dual-arm skills_ , which require coordinated behavior between the two arms. 

**Definition 1 (Single-Arm Skills).** For _ 2 {L, R}_ , _S_ is the set of all possible left/right arm skills. A single-arm skill _s 2 S_ is a conditional distribution _⇡s_ ( _a | x_ ). For any pair ( _sL, sR_ ) _2 SL ⇥ SR_ , their composition is defined as 


**Definition 2 (Dual-Arm Skills).** A dual-arm skill _sD 2 SD_ is a joint conditional distribution _⇡sD_ ( _aL, aR | x_ ) such that the conditional mutual information _I⇡sD_ ( _aL_ ; _aR | x_ ) _>_ 0. Equivalently, _⇡sD_ ( _aL, aR | x_ ) _6_ = _⇡sL_ ( _aL | x_ ) _⇡sR_ ( _aR | x_ ) for any single-arm skills _s_<sup>_L_</sup> _, s_<sup>_R_</sup> . 

Achieving inter-arm coordination for dual-arm skills requires an information pathway that induces dependence between _aL_ and _aR_ . We denote this pathway conceptually by an inter-arm message _m_ , yielding action generation forms such as _⇡L_ ( _aL | x, mL_ ) and _⇡R_ ( _aR | x, mR_ ). In practice, inter-arm message may be realized in various ways, such as explicit message passing, or implicitly through shared parameters as in common monolithic policies. 

For any possible scene _x_ , we assume there exists a (possibly multi-valued) set of _correct skills S_<sup>_?_</sup> ( _x_ ) _✓_ ( _SL ⇥ SR_ ) _[ SD_ that are appropriate for that scene. We decompose this set as _S_<sup>_?_</sup> ( _x_ ) = _S_ pair<sup>_?_(</sup><sup>_x_)</sup><sup>_[ S_</sup> _D_<sup>_?_(</sup><sup>_x_),where</sup> _S_ pair<sup>_?_(</sup><sup>_x_) =</sup><sup>_S?_(</sup><sup>_x_)</sup><sup>_\_(</sup><sup>_SL⇥SR_)</sup><sup>_,_</sup> _SD_<sup>_?_(</sup><sup>_x_) =</sup><sup>_S?_(</sup><sup>_x_)</sup><sup>_\ SD,_</sup> 

corresponding to correct skills that can be expressed as a composition of single-arm skills and correct skills that are genuinely dual-arm. Note that _S_ pair<sup>_?_(</sup><sup>_x_) is defined over the full</sup> product _SL⇥SR_ , and is not restricted to the paired set _S_ pair; in particular, it may contain recombinations of single-arm skills that never co-occur in the demonstrations. 

**Definition 3 (Skill Reuse).** For a bimanual policy learned from skill set _S_ = _S_ pair _[ SD_ = _{_ ( _sL_<sup>_m, sm_</sup> _R_<sup>)</sup><sup>_}_</sup> _m_<sup>_M_</sup> =1<sup>_[ {sn_</sup> _D_<sup>_}_</sup> _n_<sup>_N_</sup> =1<sup>,</sup> we define its possible behavior set as _S_<sup>_p_</sup> = ( _SL ⇥ SR_ ) _[ SD_ , where _SL, SR_ are the decomposed per-arm skills with _SL_ = _{s_<sup>_m_</sup> _L_<sup>_}_</sup> _m_<sup>_M_</sup> =1<sup>and</sup><sup>_SR_=</sup><sup>_{sm_</sup> _R_<sup>_}_</sup> _m_<sup>_M_</sup> =1<sup>.Wesaythatthepolicy</sup> exhibits **_skill reuse_** if, for every scene _x_ (possibly unseen) with _S_<sup>_?_</sup> ( _x_ ) _\ S_<sup>_p_</sup> _6_ = _;_ , there exists a skill _s 2 S_<sup>_?_</sup> ( _x_ ) _\ S_<sup>_p_</sup> such that _⇡✓_ ( _aL, aR | x_ ) _⇡ ⇡s_ ( _aL, aR | x_ ). Equivalently, this requirement decomposes into two major subproblems: (i) _single-arm composition_ : if the correct behavior for _x_ is a composition of single-arm skills, i.e. _S_<sup>_?_</sup> ( _x_ ) _\ S_<sup>_p_</sup> = _{_ ( _s_<sup>_i_</sup> _L_<sup>_, sj_</sup> _R_<sup>)</sup><sup>_}_forsome</sup><sup>_i, j_,thepolicymustbe</sup> able to realize this composition, even for ( _s_<sup>_i_</sup> _L_<sup>_, sj_</sup> _R_<sup>)thatnever</sup> appeared in _S_ pair; and (ii) _dual-arm reproduction_ : when the correct skill is genuinely dual-arm, i.e. _S_<sup>_?_</sup> ( _x_ ) _\ S_<sup>_p_</sup> = _{s_<sup>_i_</sup> _D_<sup>_}_</sup> for some _i_ , the policy should also produce action for _s_<sup>_i_</sup> _D_ while maintaining its inter-arm coordination structure. For cases where multiple skill choices are valid, specifically, the model should then select and produce one of them. 

**Remark (Fast bimanual continual learning by skill reuse).** In practice, many dual-arm skills are close to simple compositions of two single-arm skills, in the sense that each arm largely follows an independent per-arm behavior under the same context _x_ . The challenge is the coordination between the two arms: the joint action distribution deviates from an independent product due to inter-arm coupling (cf. _I_ ( _aL_ ; _aR | x_ ) _>_ 0 in Def. 2). Therefore, if a model can flexibly invoke reusable single-arm skills, acquiring a new bimanual skill can often be done with minimal finetuning by mainly learning additional information for coupling on top of the existing per-arm skills, rather than relearning both arms from scratch. Therefore, effective skill reuse can improve efficiency in continual learning or large-scale learning. 

## _B. Skill Selector_ 

Given a library of skills, action generation can be viewed as first selecting which skill (or skill pair) to use for a given scene _x_ , and then sampling actions from the corresponding skill distributions. We assume a (finite) skill library consisting of indexed single-arm skills _{s_<sup>_k_</sup> _L_<sup>_}k2K_</sup> _L_<sup>_✓SL_and</sup><sup>_{sl_</sup> _R_<sup>_}l2K_</sup> _R_<sup>_✓_</sup> _SR_ , and indexed dual-arm skills _{s_<sup>_d_</sup> _D_<sup>_}d2K_</sup> _D ✓ SD_ . We introduce a discrete _skill index_ random variable 


where _Y_ = _d 2 KD_ means that the dual-arm skill _⇡sD_ ( _aL, aR | x_ ) should be used, and _Y_ = ( _k, l_ ) _2 KL ⇥ KR_ means that the single-arm skills _⇡skL_<sup>(</sup><sup>_aL| x_)and</sup><sup>_⇡sl_</sup> _R_<sup>(</sup><sup>_aR| x_)</sup> should be used concurrently. 

An ideal high-level selector defines a distribution _p_<sup>_?_</sup> ( _Y | x_ ), and the resulting action distribution is the mixture 


We use the term _skill selector_ for this conceptual mechanism, without assuming a specific module or architecture. Ideally, the skill selector should select appropriate skills not only for scenes seen in the demonstrations, but also for novel inputs where the correct skill configuration has never been observed. 

## _C. Skill Entanglement in Current VLAs_ 

VLAs are often built upon a pretrained VLM, which provides strong generalization over visual scenes and naturallanguage instructions. Typically, a VLA has an additional action module (or “action expert”) to generate actions. In bimanual manipulation, the action is commonly represented as a single vector by concatenating the left- and right-arm actions. 

The VLM is a natural candidate to implement a _generalizable skill selector_ —i.e., to map a scene _x_ to an appropriate skill index _Y_ (or an equivalent decision variable) that can generalize beyond the demonstrated scenes. However, even if the upstream skill decision is sufficiently able to separate scenes requiring different skills, can the downstream action generation mechanism _reuse_ skills in the sense of Sec. IV-A? 

We argue that common VLA designs exhibit two forms of _skill entanglement_ that hinder effective skill reuse: 

**Action Entanglement.** Many bimanual VLA policies are trained to predict a single concatenated joint action vector ( _aL, aR_ ). This monolithic supervision couples the two arms at the output level and encourages the model to fit the empirical _joint_ distribution induced by paired demonstrations. Consequently, the learned policy may internalize datasetspecific cross-arm correlations rather than isolating reusable single-arm structure. This becomes problematic for skill reuse and recomposition. Even if the upstream vision–language reasoning can distinguish scenes requiring different skills, the downstream action generator may fail to (i) disentangle singlearm skills from dual-arm coordination patterns and (ii) support recomposition of single-arm skills beyond the left–right pairings observed during training. In other words, joint-action learning can bias the model toward reproducing demonstrated bimanual patterns, limiting its ability to generalize to unseen combinations of per-arm behaviors. 

**Latent entanglement in action-expert VLAs.** As previously mentioned, recent VLA methods augment a pretrained VLM with a dedicated action-generation module (e.g., _⇡_ 0/ _⇡_ 0 _._ 5 [8, 27], RDT2 [47], DexVLA [52]). Abstractly, a VLM encodes context _x_ into a representation _z_ , and an action module predicts bimanual actions conditioned on _z_ , 


where _p_ ( _z | x_ ) is induced by the VLM backbone and _p_ ( _aL, aR | z_ ) is implemented by the action expert. 

While this architecture can be effective in practice, it introduces an additional pathway for skill entanglement. In bimanual imitation, the shared latent _z_ learned from paired demonstrations may implicitly encode cross-arm dependencies. This _latent entanglement_ can degrade skill recomposition when the policy is evaluated on unseen left–right pairings, since the action expert conditions both arms on a representation that already mixes information across arms. 

## V. METHOD: SKILLVLA 

In this section, we present **SkillVLA** , a method designed to enable effective skill reuse to address combinatorial diversity and accelerate the acquisition of new skills. We first describe the overall architecture, which realizes skill reuse via a two-level reasoning pipeline and a cooperation estimator for behavior-type identification. We then introduce additional training strategies that help the model better capture skill structure and infer the degree of inter-arm cooperation. 

## _A. Method Pipeline_ 

Our method (overview in Fig. 2) follows the common VLA paradigm, with a top-level VLM and actions generated via an iterative flow-matching process [30, 32]. In our implementation, we use the pretrained PaliGemma [7] backbone released with _⇡_ 0 _._ 5 [27] for initiating the VLMs. Our method consists of two main functional components, described below: 

**Two-level reasoning (skill selection and action generation).** Because an explicit skill library is typically unavailable in practice, we aim for the model to _discover_ and _instantiate_ skill representations that support both learning and reuse. Skills can be represented in many forms; in SkillVLA we use natural language as the skill descriptor, which aligns naturally with the VLM backbone. We implement this choice via a twolevel reasoning pipeline. 

As shown in Fig. 2, the high-level module explicitly produces per-arm sub-prompts that act as skill descriptors. Concretely, we prompt the VLM to generate two texts ( _uL, uR_ ) in a fixed format: 


where _uL_ and _uR_ describe what the left and right arms should do, respectively (e.g., “pick the cake on the right” vs. “pick the box on the left”). This representation targets task intent and _explicitly_ decouples per-arm skill selection, enabling flexible single-arm recomposition: novel combinations can be formed by pairing previously generated (or learned) _uL_ and _uR_ in new scenes. During low-level skill learning, we freeze the high-level VLM to preserve its vision–language generalization while training the action components. 

At the low level, per-arm actions are generated by two separate streams. Each stream uses its own low-level VLM (fine-tuned separately, e.g., via LoRA [24]) to process the visual input and the corresponding per-arm prompt, producing a per-arm latent representation _zi_ = _fi_ ( _x, ui_ ), where 


Fig. 2: **SkillVLA framework.** SkillVLA adopts a two-level reasoning pipeline, where the high-level VLM generates separate subtasks for arms and low-level VLMs further process the prompts to instruct action generation. Inter-arm cross-attention enables cooperative behavior generation, controlled by a cooperation estimator that identifies the operation mode required. 

_i 2 {L, R}_ . Action experts then predict actions conditioned on the corresponding latent and the arm state. To support coordinated bimanual behaviors when needed, we introduce an adaptive cross-attention mechanism between the action experts to capture inter-arm dependence: 


where _mi_ is the inter-arm message produced by crossattention. The _cooperation level_ signal _↵_ gates this message to enable skill-adaptive action generation and is further elaborated upon below. 

**Cooperation estimator (behavior mode identification).** While inter-arm communication is useful for capturing low-level dependence, it should be _selectively_ enabled; for single-arm skills, the two arms should remain largely disentangled during both training and evaluation. To this end, we introduce a cooperation estimator that attends to the high-level VLM representation and predicts a scalar _↵ 2_ [0 _,_ 1], indicating the degree of inter-arm cooperation (larger _↵_ implies stronger coupling). Formally, the estimator predicts 


where _zH_ is the latent representation produced by the frozen high-level VLM. This signal serves as a mode identifier, indicating whether the current behavior is better explained as (i) a composition of single-arm skills or (ii) a cooperative dual-arm skill. We gate inter-arm message passing by _↵_ , enabling the policy to interpolate between per-arm generation and coupled dual-arm generation. 

To train _↵t_ , we use a simple _communication usefulness_ objective derived from behavioral cloning (BC). At timestep _t_ , the BC loss is 


We compute _L_<sup>on</sup> BC<sup>withcross-attentionenabledand</sup><sup>_L_o↵</sup> BC<sup>with</sup> cross-attention disabled. We then define 


where ( _·_ )sg denotes stop-gradient. Minimizing _L_ coop increases _↵t_ when communication reduces the BC error and decreases _↵t_ otherwise. 

## _B. Additional Cooperation-Level Learning_ 

Because _↵_ directly gates cross-arm interaction, accurately inferring the cooperation level is critical. We introduce additional mechanisms to encourage reliable cooperation estimation, which we use by default in our implementation. 

**Priors and regularizers for cooperation learning.** VLMs are pretrained on web-scale data and thus encode broad task semantics and commonsense regularities (e.g., when two arms are typically required). This makes them a natural source of priors for estimating task-dependent cooperation. To distill this information into a lightweight estimator, we use an off-theshelf VLM to produce a prior coordination strength _↵_<sup>vlm</sup> _2_ [0 _,_ 1] for the current scene and task (or _↵_<sup>vlm</sup> _2 {_ 0 _,_ 1 _}_ when using a discrete gate). 

Let _↵_ ˜ _t_ denote the gate value actually used for communication (i.e., the continuous _↵t_ , or the soft discrete probability _y_ ˆ _t_ defined below). We regularize _↵_ ˜ _t_ toward the VLM prior and further encourage (a) sticky gating for temporal smoothness and (b) conservative communication, keeping the gate small unless interaction is beneficial: 


We set _`_ ( _u, v_ ) = _ku − vk_ 2<sup>2when</sup><sup>_↵_˜</sup><sup>_t_iscontinuous,andusea</sup> Bernoulli cross-entropy _`_ ( _u, v_ ) = _−v_ log _u−_ (1 _−v_ ) log(1 _−u_ ) when _↵_ ˜ _t 2_ (0 _,_ 1) is interpreted as a probability. 

**Cooperation level discretization.** In practice, a continuous gate _↵t_ can exhibit small but persistent fluctuations that destabilize action generation. To improve stability, we (optionally) discretize the gate by restricting _↵t 2 {_ 0 _,_ 1 _}_ . Specifically, the model predicts _y_ ˆ _t 2_ (0 _,_ 1), the probability of enabling cross-arm communication, and we train it with a binary crossentropy loss: 


At inference time, we binarize _y_ ˆ _t_ to obtain _↵_ ˆ _t 2 {_ 0 _,_ 1 _}_ , which directly enables or disables the cross-attention message. We apply the same priors and regularizers from Sec. V-B to _y_ ˆ _t_ as a soft relaxation, thereby shaping the resulting discrete gate. This tokenized formulation simplifies gate prediction and 


Fig. 3: **Skill recomposition tasks. (A):** The models are trained on demonstrations of three skills for each arm. **(B):** After the models have learned the skills, zero-shot tests are conducted for every possible combination of left and right-arm skills. 

TABLE I: Success Rates on Skill Recomposition Tasks _"_ 

|Methods|Cup_⇥_Cake|Cup_⇥_Stir|Cup_⇥_Smash|Box_⇥_Cake|Recomposit<br>Box_⇥_Stir|ion Tasks<br>Box_⇥_Smash|Mug_⇥_Cake|Mug_⇥_Stir|Mug_⇥_Smash|Avg.|
|---|---|---|---|---|---|---|---|---|---|---|
|_⇡_0_._5|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|
|_⇡_0-FAST|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|
|TwinVLA|0.1|0.0|0.0|0.2|0.0|0.1|0.0|0.0|0.0|0.04|
|SkillVLA|**0.7**|**0.4**|**0.5**|**0.6**|**0.4**|**0.5**|**0.6**|**0.3**|**0.6**|**0.51**|


TABLE II: Success Rates on Skills Learned 

|Methods|Cup|Box|Sk<br>Mug|ills Lear<br>Cake|ned<br>Stir|Smash|Avg.|
|---|---|---|---|---|---|---|---|
|_⇡_0_._5|0.7|**1.0**|**0.8**|0.8|**0.6**|0.7|0.77|
|_⇡_0-FAST|**0.9**|0.8|0.7|0.9|0.5|0.4|0.70|
|TwinVLA|0.7|0.8|0.5|0.8|0.5|0.7|0.67|
|SkillVLA|0.8|0.7|**0.8**|**1.0**|**0.6**|**0.8**|**0.78**|


empirically improved stability in preliminary experiments. Implementation and training details are provided in the appendix. 

## VI. EXPERIMENTS 

In this section, we evaluate our model’s ability to (i) freely reuse learned single-arm skills, (ii) capture the inter-arm coordination required by truly cooperative behaviors, and (iii) identify when cooperation is necessary for a given state. Our experiments are designed to answer the following questions: 

- 1) Can SkillVLA flexibly recompose learned skills and generalize to unseen combinations of single-arm skills? 

- 2) Is SkillVLA’s communication mechanism sufficient to support tight inter-arm coordination and reproduce cooperative dual-arm skills? 

- 3) Can SkillVLA handle multi-stage, long-horizon tasks by estimating cooperation level and switching between operating modes? 

- 4) In continual learning, does SkillVLA better leverage previously learned skills to acquire related new skills compared to existing methods? 

**Baselines and evaluation metrics.** We compare SkillVLA against _⇡_ 0 _._ 5 [27], a representative state-of-the-art VLA base- 

line. For Q1, we additionally include _⇡_ 0-FAST [40] as a representative autoregressive VLA, which represents the other major paradigm beyond diffusion-based VLAs and tests whether skill entanglement persists across architectures. In the Q1 setting, these general-purpose VLAs achieve near-zero success due to severe skill entanglement. To enable more informative comparisons, we further include TwinVLA [25] as a factorized baseline that composes two single-arm VLAs by sharing action experts while allowing _uncontrolled_ cross-arm attention. For most tasks (except the long-horizon task), we report _success rate_ as the primary metric. For long-horizon tasks which comprise multiple stages, we additionally report a _progress score_ and the _average completion time_ to quantify execution quality and efficiency. Additional experimental details are provided in the appendix. 

## _A. Single-Arm Skill Reuse_ 

**Task Setup.** Here, we evaluate whether a bimanual VLA can _reuse_ learned single-arm skills under _unseen_ left–right combinations. As shown in Fig. 3, our training data include three skills per arm, collected from single-arm executions while the other arm remains stationary. At test time, we ask the policy to execute a left-arm skill and a right-arm skill _simultaneously_ in combinations that never appear in the training set. This setting directly probes skill reuse since the policy should invoke the correct per-arm behaviors and maintain stable concurrent execution, rather than reverting to familiar demonstration-time patterns. 

**Performance Results.** As reported in Tab. I and Tab. II, all methods perform comparably on the _seen_ single-arm skills, 


Fig. 4: **Cooperative tasks. (a)** SHAKE: Shake the cup without the cap falling off. **(b)** BALL: Lift the ball steadily. **(c)** ALIGN: Align the blocks on the table. 

but their behaviors _diverge sharply_ when asked to _zero-shot_ recompose unseen left-right combinations. 

In particular, _⇡_ 0 _._ 5 and _⇡_ 0-FAST achieve a 0% success rate. Qualitatively, these models frequently revert to the trainingtime regime in which one arm acts while the other remains idle, indicating that they primarily reproduce skill pairings present in the dataset rather than freely recombining per-arm behaviors. Moreover, when instructed to perform a two-arm task, _⇡_ 0 _._ 5 often exhibits instability in that the nominally “idle” arm jitters or drifts. These results are not entirely surprising since the test settings are essentially out-of-distribution (OOD) for standard VLAs and this failure mode can be attributed to _entangled_ bimanual control. Because _⇡_ 0 _._ 5 uses a single shared representation to control both arms, each left–right pairing effectively corresponds to a distinct latent mode specifying a coupled bimanual action. Unseen pairings therefore require a latent that is not induced by any training demonstration, producing an OOD input to the downstream action expert. 

TwinVLA attains non-zero success by occasionally producing the intended composition. However, although it uses separate VLM streams for the two arms, it relies on _uncontrolled_ cross-attention between streams, which can introduce implicit coupling. This yields unpredictable interference under unseen pairings and keeps overall success low. 

In contrast, SkillVLA achieves a substantially higher success rate of 51% on unseen combinations. By explicitly disentangling per-arm skill invocation, performing skill-adaptive action generation, and enabling _controlled_ inter-arm communication only when needed, SkillVLA more reliably reuses the same single-arm behaviors under novel pairings while reducing spurious cross-arm interference. 

## _B. Dual-Arm (Cooperative) Skill Reproduction_ 

**Task Setup.** To evaluate whether SkillVLA can reproduce cooperative dual-arm skills that require close inter-arm coordination, we design three cooperative tasks (Fig. 4). These tasks fall into two categories with qualitatively different coordination demands. The first category, SHAKE and BALL, requires _tight low-level alignment_ between the two arms. The second category, ALIGN, requires both low-level alignment and _high-level coordination_ ; two blocks are placed near the center of the table, and the two arms must simultaneously pick the objects and align them. Importantly, the arm-object assignment is randomized across trials, requiring the policy to resolve task allocation on the fly. 

TABLE III: Success Rate in Cooperative Tasks _"_ 

|**Methods**|**Shake**|**Ball**|**Align**|**Avg.**|
|---|---|---|---|---|
|_⇡_0_._5|**0.30**|0.45|0.65|0.47|
|TwinVLA|0.15|**0.55**|0.55|0.42|
|SkillVLA|0.25|0.50|**0.70**|**0.48**|
|SkillVLA w/o Attn.|0.00|0.10|0.40|0.17|


**Performance Results.** As reported in Tab. III, SkillVLA achieves performance comparable to the strong baseline _⇡_ 0 _._ 5 across all cooperative tasks. This suggests that SkillVLA can identify when cooperation is required and that its explicit communication mechanism is expressive enough to support tight inter-arm coordination when needed. 

**Ablation: Cross-Attention.** We further isolate the role of action-level communication by evaluating an ablation that disables cross-attention between the two action experts. This variant performs particularly poorly on SHAKE and BALL, confirming that cross-attention-based communication is important for maintaining tight low-level alignment. On ALIGN, which places greater emphasis on high-level task assignment and is comparatively less sensitive to continuous low-level coupling, disabling communication results in a smaller performance drop. 

## _C. Applications in Long-Horizon Settings_ 

We next evaluate whether SkillVLA can (i) infer the required cooperation level and (ii) switch between collaborative and non-collaborative modes _within a single episode_ . 

**Task setup.** We design two long-horizon real-world tasks, TUBES and COLLECT ITEMS (Fig. 5). Each task intentionally interleaves phases that admit independent per-arm execution with phases that require explicit bimanual cooperation. As a representative example, TUBES consists of two stages with distinct coordination demands: (1) transferring tubes from one rack to another (independent per-arm collection), and (2) lifting and placing the loaded rack onto another rack ( cooperative bimanual manipulation). We train the model using demonstrations of three skills, i.e., transferring a tube with the left arm, transferring a tube with the right arm, and moving the rack with both arms. We then evaluate the policy _zero-shot_ on the full long-horizon task that composes these stages. 

**Performance and Efficiency Results.** As shown in Fig. 5 (bottom right), SkillVLA achieves a progress score comparable to strong baselines, indicating that it can select an appropriate operating mode and complete the task reliably. More importantly, SkillVLA _reduces average completion time_ by _⇡_ 21% relative to the baselines. Qualitatively, monolithic baselines tend to follow demonstration-like sequential patterns (one arm acts while the other waits), whereas **SkillVLA** leverages _skill reuse_ to exploit parallelism when available. In TUBES, during the tube-collection stage, it concurrently invokes the single-arm tube-transfer skills with both arms (i.e., _↵_ = 0), enabling parallel left–right execution and substantially accelerating completion. This ability to opportunistically 


Fig. 5: **Long-horizon tasks behaviors and results. Top:** Behavior of _⇡_ 0 _._ 5 in TUBES. **Middle left:** Behavior of SkillVLA in TUBES. **Bottom left:** Changes of _↵_ values throughout the completion, respectively from SkillVLA and an ablated version without discretization of _↵_ . **Bottom right:** Averaged progress score and completion time of methods on the long-horizon tasks. 


Fig. 6: **Continual learning tasks and results. Left:** SkillVLA in continual learning tasks, LIFT BAG and SHAKE CUP. **Right:** Success rates on cooperative tasks LIFT BAG and SHAKE CUP w.r.t the number of continual learning demonstrations. 

parallelize subtasks better utilizes the robot’s hardware and improves practical throughput. 

**Mode switching via the cooperation gate.** Fig. 5 (bottom left) visualizes **SkillVLA** ’s discrete gate output _↵ 2 {_ 0 _,_ 1 _}_ , where _↵_ = 0 corresponds to independent per-arm execution and _↵_ = 1 activates inter-arm cooperation. We observe that _↵_ evolves coherently with task progress; it switches to _↵_ = 1 during inherently cooperative phases such as moving the loaded rack with both arms, while remaining at _↵_ = 0 during collection phases where the arms can operate independently. This stage-consistent switching suggests that the gate can infer the required cooperation level from scene and instruction context, allowing SkillVLA to reuse both single-arm and dualarm behaviors within a single rollout. In COLLECT ITEMS, the gate exhibits more complex transitions across multiple stages, further demonstrating the adaptability of our method to diverse coordination patterns. 

**Ablation: Continuous vs. Discretized Gating.** We also 

evaluate an ablation that uses a continuous (non-discretized) gate. This variant is less stable over long horizons. As shown in Fig. 5 (bottom left), continuous _↵_ exhibits noticeably higher fluctuation despite following a similar overall trend. This instability propagates to action generation, leading to lower success and higher variance in performance (Fig. 5, bottom right). These results suggest that discretizing _↵_ improves robustness by enforcing simpler, clearer mode switching. 

## _D. Reuse of Learned Skills in Continual Learning_ 

**Task setup.** To answer Q4, we study whether SkillVLA can reuse learned single-arm skills to accelerate the acquisition of a new cooperative dual-arm skill via fine-tuning. As illustrated in Fig. 6 (left), we consider two task groups, LIFT BAG 

and SHAKE CUP. In each group, we first pretrain the model on the corresponding single-arm dataset (e.g., lifting a bag with one arm), and then fine-tune it with a small number of demonstrations to obtain the target dual-arm skill (e.g., lifting with both arms). For each task group, we construct a twostage continual-learning protocol: (i) pretraining on single-arm executions to learn reusable per-arm behaviors, followed by (ii) fine-tuning on a limited set of dual-arm demonstrations to learn the cooperative variant. 

**Learning Curves and Data Efficiency.** Fig. 6 (right) reports success rates as a function of the number of dual-arm demonstrations used for fine-tuning. In LIFT BAG, the target dual-arm behavior is close to a composition of the pretrained singlearm skills, and SkillVLA achieves 20% success _zero-shot_ . Moreover, with only 5 fine-tuning demonstrations, it reaches near-peak performance. In contrast, _⇡_ 0 _._ 5 and TwinVLA remain far from convergence even after training on 30 demonstrations. These results indicate that SkillVLA can effectively leverage previously learned single-arm behaviors for rapid adaptation. 

**Adapting Skills to New Coordination.** SHAKE CUP is challenging because the required coordination deviates from the original single-arm behavior; one hand must stabilize the cap rather than shaking the cup body. Despite this mismatch, SkillVLA exhibits the same data-efficient trend, which suggests that reuse in continual learning is not limited to replaying identical action patterns. Instead, the model can transfer related single-arm behaviors as a strong initialization and quickly adapt them into a new cooperative policy. Overall, these results support skill reuse as a practical mechanism for continual learning and for scaling generalist bimanual policies with reduced demonstration burden. 

## VII. CONCLUSION, LIMITATIONS, AND FUTURE WORK 

In this work, we study the _combinatorial diversity_ challenge in bimanual manipulation through the lens of _skill reuse_ . We identify _skill entanglement_ in existing VLA designs as a central obstacle to reuse—particularly for composing diverse left–right skill pairings and generalizing to unseen task combinations. To address this, we propose SkillVLA, which mitigates entanglement by explicitly separating per-arm skill invocation and enabling skill-adaptive action generation, while still leveraging the generalization of pretrained vision– language models. Across real-world evaluations, SkillVLA improves combinatorial generalization and data efficiency in continual skill acquisition, demonstrating more reliable reuse of both single-arm and cooperative dual-arm behaviors. 

**Limitations.** SkillVLA depends on pretrained VLMs for highlevel reasoning and for providing priors on cooperation, which ties performance to the capability, latency, and cost profile of the underlying foundation model. Future work will explore more efficient ways to distill or compress this reasoning into lightweight policy components, as well as richer skill representations beyond natural language. More broadly, we view disentangled skill learning/selection and controlled crossarm coupling as key ingredients for scaling toward truly generalist bimanual agents that can recombine skills reliably on demand. 

## ACKNOWLEDGMENT 

This work is supported by the Zhongguancun Academy (Grant No.c20250502). This research / project is partially supported by the National Research Foundation, Singapore, under its Thematic Competitive Research Programme 2025 (NRF-T-CRP-2025-0003). 

## REFERENCES 

- [1] M Mahdi Ghazaei Ardakani, Martin Karlsson, Klas Nilsson, Anders Robertsson, and Rolf Johansson. Masterslave coordination using virtual constraints for a redundant dual-arm haptic interface. In _2018 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 8751–8757. IEEE, 2018. 

- [2] Yahav Avigal, Lars Berscheid, Tamim Asfour, Torsten Kr¨oger, and Ken Goldberg. Speedfolding: Learning efficient bimanual folding of garments. In _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 1–8. IEEE, 2022. 

- [3] Arpit Bahety, Shreeya Jain, Huy Ha, Nathalie Hager, Benjamin Burchfiel, Eric Cousineau, Siyuan Feng, and Shuran Song. Bag all you need: Learning a generalizable bagging strategy for heterogeneous objects. In _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 960–967. IEEE, 2023. 

- [4] Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen, Xionghui Chen, Zesen Cheng, Lianghao Deng, Wei Ding, Chang Gao, Chunjiang Ge, Wenbin Ge, Zhifang Guo, Qidong Huang, Jie Huang, Fei Huang, Binyuan Hui, Shutong Jiang, Zhaohai Li, Mingsheng Li, Mei Li, Kaixin 

Li, Zicheng Lin, Junyang Lin, Xuejing Liu, Jiawei Liu, Chenglong Liu, Yang Liu, Dayiheng Liu, Shixuan Liu, Dunjie Lu, Ruilin Luo, Chenxu Lv, Rui Men, Lingchen Meng, Xuancheng Ren, Xingzhang Ren, Sibo Song, Yuchong Sun, Jun Tang, Jianhong Tu, Jianqiang Wan, Peng Wang, Pengfei Wang, Qiuyue Wang, Yuxuan Wang, Tianbao Xie, Yiheng Xu, Haiyang Xu, Jin Xu, Zhibo Yang, Mingkun Yang, Jianxin Yang, An Yang, Bowen Yu, Fei Zhang, Hang Zhang, Xi Zhang, Bo Zheng, Humen Zhong, Jingren Zhou, Fan Zhou, Jing Zhou, Yuanzhi Zhu, and Ke Zhu. Qwen3-vl technical report, 2025. URL https://arxiv.org/abs/2511.21631. 

- [5] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, Humen Zhong, Yuanzhi Zhu, Mingkun Yang, Zhaohai Li, Jianqiang Wan, Pengfei Wang, Wei Ding, Zheren Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen Cheng, Hang Zhang, Zhibo Yang, Haiyang Xu, and Junyang Lin. Qwen2.5-vl technical report, 2025. URL https://arxiv.org/abs/2502.13923. 

- [6] Christian Bersch, Benjamin Pitzer, and S¨oren Kammel. Bimanual robotic cloth manipulation for laundry folding. In _2011 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 1413–1419. IEEE, 2011. 

- [7] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, Thomas Unterthiner, Daniel Keysers, Skanda Koppula, Fangyu Liu, Adam Grycner, Alexey Gritsenko, Neil Houlsby, Manoj Kumar, Keran Rong, Julian Eisenschlos, Rishabh Kabra, Matthias Bauer, Matko Boˇsnjak, Xi Chen, Matthias Minderer, Paul Voigtlaender, Ioana Bica, Ivana Balazevic, Joan Puigcerver, Pinelopi Papalampidi, Olivier Henaff, Xi Xiong, Radu Soricut, Jeremiah Harmsen, and Xiaohua Zhai. Paligemma: A versatile 3b vlm for transfer, 2024. URL https://arxiv.org/abs/2407.07726. 

- [8] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, Laura Smith, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _⇡_ 0: A Vision-Language-Action Flow Model for General Robot Control. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. doi: 10.15607/RSS.2025.XXI.010. 

- [9] RC Bonitz and Tien C Hsia. Internal force-based impedance control for cooperating manipulators. _IEEE Transactions on Robotics and Automation_ , 12(1):78–89, 1996. 

- [10] Alper Canberk, Cheng Chi, Huy Ha, Benjamin Burchfiel, Eric Cousineau, Siyuan Feng, and Shuran Song. Cloth 

funnels: Canonicalized-alignment for multi-purpose garment manipulation. In _International Conference of Robotics and Automation (ICRA)_ , 2022. 

- [11] Lawrence Yunliang Chen, Baiyu Shi, Roy Lin, Daniel Seita, Ayah Ahmad, Richard Cheng, Thomas Kollar, David Held, and Ken Goldberg. Bagging by learning to singulate layers using interactive perception. In _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 3176–3183. IEEE, 2023. 

- [12] Lawrence Yunliang Chen, Baiyu Shi, Daniel Seita, Richard Cheng, Thomas Kollar, David Held, and Ken Goldberg. Autobag: Learning to open plastic bags and insert objects. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 3918–3925, 2023. doi: 10.1109/ICRA48891.2023.10161402. 

- [13] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Qiwei Liang, Zixuan Li, Xianliang Lin, Yiheng Ge, Zhenyu Gu, et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 

- [14] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 

- [15] Cheng Chi, Zhenjia Xu, Chuer Pan, Eric Cousineau, Benjamin Burchfiel, Siyuan Feng, Russ Tedrake, and Shuran Song. Universal manipulation interface: Inthe-wild robot teaching without in-the-wild robots. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

- [16] Rohan Chitnis, Shubham Tulsiani, Saurabh Gupta, and Abhinav Gupta. Efficient bimanual manipulation using learned task schemas. In _2020 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 1149–1155. IEEE, 2020. 

- [17] InternVLA-M1 Contributors. Internvla-m1: A spatially guided vision-language-action framework for generalist robot policy. _arXiv preprint arXiv:2510.13778_ , 2025. 

- [18] Runyu Ding, Yuzhe Qin, Jiyue Zhu, Chengzhe Jia, Shiqi Yang, Ruihan Yang, Xiaojuan Qi, and Xiaolong Wang. Bunny-visionpro: Real-time bimanual dexterous teleoperation for imitation learning. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 12248–12255, 2025. doi: 10.1109/ IROS60139.2025.11247017. 

- [19] Zipeng Fu, Tony Z. Zhao, and Chelsea Finn. Mobile ALOHA: Learning bimanual mobile manipulation using low-cost whole-body teleoperation. In _8th Annual Conference on Robot Learning_ , 2024. URL https:// openreview.net/forum?id=FO6tePGRZj. 

- [20] Dongsheng Ge, Huan Zhao, Dianxi Li, Dongchen Han, Xiangfei Li, Jiexin Zhang, and Han Ding. A dualarm robotic cooperative framework for multiple peg-inhole assembly of large objects. _Robotics and Computer-_ 

_Integrated Manufacturing_ , 95:102991, 2025. 

- [21] Kristen Grauman, Andrew Westbury, Eugene Byrne, Zachary Chavis, Antonino Furnari, Rohit Girdhar, Jackson Hamburger, Hao Jiang, Miao Liu, Xingyu Liu, et al. Ego4d: Around the world in 3,000 hours of egocentric video. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 18995– 19012, 2022. 

- [22] Ce Hao, Xuanran Zhai, Yaohua Liu, and Harold Soh. Abstracting robot manipulation skills via mixture-ofexperts diffusion policies. In _The Fourteenth International Conference on Learning Representations_ , 2026. 

- [23] Samad Hayati, Kam Tso, and Thomas Lee. Dual arm coordination and control. _Robotics and Autonomous Systems_ , 5(4):333–344, 1989. 

- [24] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. _ICLR_ , 1(2):3, 2022. 

- [25] Hokyun Im, Euijin Jeong, Jianlong Fu, Andrey Kolobov, and Youngwoon Lee. Twinvla: Data-efficient bimanual manipulation with twin single-arm vision-languageaction models, 2025. URL https://arxiv.org/abs/2511. 05275. 

- [26] Physical Intelligence, Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Kevin Black, Ken Conley, Grace Connors, James Darpinian, Karan Dhabalia, Jared DiCarlo, Danny Driess, Michael Equi, Adnan Esmail, Yunhao Fang, Chelsea Finn, Catherine Glossop, Thomas Godden, Ivan Goryachev, Lachy Groom, Hunter Hancock, Karol Hausman, Gashon Hussein, Brian Ichter, Szymon Jakubczak, Rowan Jen, Tim Jones, Ben Katz, Liyiming Ke, Chandra Kuchi, Marinda Lamb, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Yao Lu, Vishnu Mano, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Charvi Sharma, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, Will Stoeckle, Alex Swerdlow, James Tanner, Marcel Torne, Quan Vuong, Anna Walling, Haohuan Wang, Blake Williams, Sukwon Yoo, Lili Yu, Ury Zhilinsky, and Zhiyuan Zhou. _⇡_ 0<sup>_⇤_</sup> _._ 6<sup>:avlathatlearnsfromexperience,</sup> 2025. URL https://arxiv.org/abs/2511.14759. 

- [27] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _⇡_ 0 _._ 5: a vision-languageaction model with open-world generalization, 2025. URL https://arxiv.org/abs/2504.16054. 

- [28] Jaehyung Kim, Jiho Kim, Dongryung Lee, Yujin Jang, 

and Beomjoon Kim. A low-cost and lightweight 6 DoF bimanual arm for dynamic and contact-rich manipulation. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. doi: 10.15607/RSS. 2025.XXI.055. 

- [29] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [30] Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matthew Le. Flow matching for generative modeling. In _The Eleventh International Conference on Learning Representations_ , 2023. URL https://openreview.net/forum?id=PqvMRDCJT9t. 

- [31] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. RDT-1b: a diffusion foundation model for bimanual manipulation. In _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [32] Xingchao Liu, Chengyue Gong, and qiang liu. Flow straight and fast: Learning to generate and transfer data with rectified flow. In _The Eleventh International Conference on Learning Representations_ , 2023. URL https://openreview.net/forum?id=XVjTT1nw5z. 

- [33] Guanxing Lu, Tengbo Yu, Haoyuan Deng, Season Si Chen, Yansong Tang, and Ziwei Wang. Anybimanual: Transferring unimanual policy for general bimanual manipulation, 2025. URL https://arxiv.org/abs/2412.06779. 

- [34] Teli Ma, Jia Zheng, Zifan Wang, Chunli Jiang, Andy Cui, Junwei Liang, and Shuo Yang. Dit4dit: Jointly modeling video dynamics and actions for generalizable robot control. _arXiv preprint arXiv:2603.10448_ , 2026. 

- [35] Jeremy Maitin-Shepard, Marco Cusumano-Towner, Jinna Lei, and Pieter Abbeel. Cloth grasp point detection based on multiple-view geometric cues with application to robotic towel folding. In _2010 IEEE International Conference on Robotics and Automation_ , pages 2308– 2315. IEEE, 2010. 

- [36] Tomohiro Motoda, Ryo Hanai, Ryoichi Nakajo, Masaki Murooka, Floris Erich, and Yukiyasu Domae. Learning bimanual manipulation via action chunking and inter-arm coordination with transformers, 2025. URL https://arxiv. org/abs/2503.13916. 

- [37] Davide Ortenzi, Rajkumar Muthusamy, Alessandro Freddi, Andrea Monteri`u, and Ville Kyrki. Dual-arm cooperative manipulation under joint limit constraints. _Robotics and Autonomous Systems_ , 99:110–120, 2018. 

- [38] Georgios Papagiannis, Norman Di Palo, Pietro Vitiello, and Edward Johns. R+ x: Retrieval and execution from everyday human videos. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 8284–8290. IEEE, 2025. 

- [39] H Andy Park and CS George Lee. Extended cooperative task space for manipulation tasks of humanoid robots. In _2015 IEEE International Conference on Robotics and_ 

_Automation (ICRA)_ , pages 6088–6093. IEEE, 2015. 

- [40] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. FAST: Efficient Action Tokenization for Vision-Language-Action Models. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. doi: 10.15607/RSS.2025.XXI.012. 

- [41] Gautam Salhotra, I Liu, Gaurav Sukhatme, et al. Learning robot manipulation from cross-morphology demonstration. _arXiv preprint arXiv:2304.03833_ , 2023. 

- [42] STANLEYA Schneider and Robert H Cannon. Object impedance control for cooperative manipulation: Theory and experimental results. In _Proceedings, 1989 international conference on robotics and automation_ , pages 1076–1083. IEEE, 1989. 

- [43] Kenneth Shaw, Yulong Li, Jiahui Yang, Mohan Kumar Srirama, Ray Liu, Haoyu Xiong, Russell Mendonca, and Deepak Pathak. Bimanual dexterity for complex tasks. In _8th Annual Conference on Robot Learning_ , 2024. URL https://openreview.net/forum?id=55tYfHvanf. 

- [44] Christian Smith, Yiannis Karayiannidis, Lazaros Nalpantidis, Xavi Gratal, Peng Qi, Dimos V. Dimarogonas, and Danica Kragic. Dual arm manipulation—a survey. _Robotics and Autonomous Systems_ , 60(10):1340–1353, 2012. ISSN 0921-8890. doi: https://doi.org/10.1016/j. robot.2012.07.005. URL https://www.sciencedirect.com/ science/article/pii/S092188901200108X. 

- [45] Wenxuan Song, Jiayi Chen, Pengxiang Ding, Han Zhao, Wei Zhao, Zhide Zhong, Zongyuan Ge, Jun Ma, and Haoang Li. Accelerating vision-language-action model integrated with action chunking via parallel decoding. _arXiv preprint arXiv:2503.02310_ , 2025. 

- [46] Markku Suomalainen, Sylvain Calinon, Emmanuel Pignat, and Ville Kyrki. Improving dual-arm assembly by master-slave compliance. In _2019 International Conference on Robotics and Automation (ICRA)_ , pages 8676– 8682. IEEE, 2019. 

- [47] RDT Team. Rdt2: Enabling zero-shot cross-embodiment generalization by scaling up umi data, September 2025. URL https://github.com/thu-ml/RDT2. 

- [48] Masaru Uchiyama and Pierre Dauchez. A symmetric hybrid position/force control scheme for the coordination of two robots. In _Proceedings. 1988 IEEE international conference on robotics and automation_ , pages 350–356. IEEE, 1988. 

- [49] Christos K Verginis, Daniel Zelazo, and Dimos V Dimarogonas. Cooperative manipulation via internal force regulation: A rigidity theory perspective. _IEEE Transactions on Control of Network Systems_ , 10(3):1222–1233, 2022. 

- [50] Chen Wang, Haochen Shi, Weizhuo Wang, Ruohan Zhang, Li Fei-Fei, and Karen Liu. DexCap: Scalable and Portable Mocap Data Collection System for Dexterous Manipulation. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, July 2024. doi: 10.15607/RSS.2024.XX.043. 

- [51] Yixiao Wang, Yifei Zhang, Mingxiao Huo, Ran Tian, Xiang Zhang, Yichen Xie, Chenfeng Xu, Pengliang Ji, Wei Zhan, Mingyu Ding, et al. Sparse diffusion policy: A sparse, reusable, and flexible policy for robot learning. _arXiv preprint arXiv:2407.01531_ , 2024. 

- [52] Junjie Wen, Yichen Zhu, Jinming Li, Zhibin Tang, Chaomin Shen, and Feifei Feng. Dexvla: Visionlanguage model with plug-in diffusion expert for general robot control. _arXiv preprint arXiv:2502.05855_ , 2025. 

- [53] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Zhibin Tang, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, et al. Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025. 

- [54] Thomas Weng, Sujay Man Bajracharya, Yufei Wang, Khush Agrawal, and David Held. Fabricflownet: Bimanual cloth manipulation with a flow-based policy. In _Conference on Robot Learning_ , pages 192–202. PMLR, 2022. 

- [55] Fan Xie, Alexander Chowdhury, M De Paolis Kaluza, Linfeng Zhao, Lawson Wong, and Rose Yu. Deep imitation learning for bimanual robotic manipulation. _Advances in neural information processing systems_ , 33: 2327–2337, 2020. 

- [56] Jingyun Yang, Ziang Cao, Congyue Deng, Rika Antonova, Shuran Song, and Jeannette Bohg. Equibot: SIM(3)-equivariant diffusion policy for generalizable and data efficient learning. In _8th Annual Conference on Robot Learning_ , 2024. 

- [57] Seonghyeon Ye, Yunhao Ge, Kaiyuan Zheng, Shenyuan Gao, Sihyun Yu, George Kurian, Suneel Indupuru, You Liang Tan, Chuning Zhu, Jiannan Xiang, Ayaan Malik, Kyungmin Lee, William Liang, Nadun Ranawaka, Jiasheng Gu, Yinzhen Xu, Guanzhi Wang, Fengyuan Hu, Avnish Narayan, Johan Bjorck, Jing Wang, Gwanghyun Kim, Dantong Niu, Ruijie Zheng, Yuqi Xie, Jimmy Wu, Qi Wang, Ryan Julian, Danfei Xu, Yilun Du, Yevgen Chebotar, Scott Reed, Jan Kautz, Yuke Zhu, Linxi ”Jim” Fan, and Joel Jang. World action models are zero-shot policies, 2026. URL https://arxiv.org/abs/2602.15922. 

- [58] Jiawen Yu, Hairuo Liu, Qiaojun Yu, Jieji Ren, Ce Hao, Haitong Ding, Guangyu Huang, Guofan Huang, Yan Song, Panpan Cai, Cewu Lu, and Wenqiang Zhang. Forcevla: Enhancing vla models with a force-aware moe for contact-rich manipulation, 2025. URL https://arxiv. org/abs/2505.22159. 

- [59] Samson Yu, Lin Kelvin, and Harold Soh. Demonstrating the Octopi-1.5 Visual-Tactile-Language Model. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. doi: 10.15607/RSS.2025.XXI.058. 

- [60] Tianyuan Yuan, Zibin Dong, Yicheng Liu, and Hang Zhao. Fast-wam: Do world action models need testtime future imagination?, 2026. URL https://arxiv.org/ abs/2603.16666. 

- [61] Xuanran Zhai, Qianyou Zhao, Qiaojun Yu, and Ce Hao. Vfp: Variational flow-matching policy for multi-modal 

robot manipulation, 2025. URL https://arxiv.org/abs/ 2508.01622. 

- [62] Tony Z. Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware. In _Proceedings of Robotics: Science and Systems_ , Daegu, Republic of Korea, July 2023. doi: 10.15607/RSS.2023.XIX.016. 

- [63] Tony Z. Zhao, Jonathan Tompson, Danny Driess, Pete Florence, Seyed Kamyar Seyed Ghasemipour, Chelsea Finn, and Ayzaan Wahid. Aloha unleashed: A simple recipe for robot dexterity. In Pulkit Agrawal, Oliver Kroemer, and Wolfram Burgard, editors, _Proceedings of The 8th Conference on Robot Learning_ , volume 270 of _Proceedings of Machine Learning Research_ , pages 1910– 1924. PMLR, 06–09 Nov 2025. URL https://proceedings. mlr.press/v270/zhao25b.html. 

- [64] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3dvla: A 3d vision-language-action generative world model. _arXiv preprint arXiv:2403.09631_ , 2024. 

- [65] Ruijie Zheng, Jing Wang, Scott Reed, Johan Bjorck, Yu Fang, Fengyuan Hu, Joel Jang, Kaushil Kundalia, Zongyu Lin, Loic Magne, Avnish Narayan, You Liang Tan, Guanzhi Wang, Qi Wang, Jiannan Xiang, Yinzhen Xu, Seonghyeon Ye, Jan Kautz, Furong Huang, Yuke Zhu, and Linxi Fan. Flare: Robot learning with implicit world modeling, 2025. URL https://arxiv.org/abs/2505. 15659. 

- [66] Huayi Zhou, Ruixiang Wang, Yunxin Tai, Yueci Deng, Guiliang Liu, and Kui Jia. You Only Teach Once: Learn One-Shot Bimanual Robotic Manipulation from Video Demonstrations. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. doi: 10. 15607/RSS.2025.XXI.149. 

- [67] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, Quan Vuong, Vincent Vanhoucke, Huong Tran, Radu Soricut, Anikait Singh, Jaspiar Singh, Pierre Sermanet, Pannag R. Sanketi, Grecia Salazar, Michael S. Ryoo, Krista Reymann, Kanishka Rao, Karl Pertsch, Igor Mordatch, Henryk Michalewski, Yao Lu, Sergey Levine, Lisa Lee, Tsang-Wei Edward Lee, Isabel Leal, Yuheng Kuang, Dmitry Kalashnikov, Ryan Julian, Nikhil J. Joshi, Alex Irpan, Brian Ichter, Jasmine Hsu, Alexander Herzog, Karol Hausman, Keerthana Gopalakrishnan, Chuyuan Fu, Pete Florence, Chelsea Finn, Kumar Avinava Dubey, Danny Driess, Tianli Ding, Krzysztof Marcin Choromanski, Xi Chen, Yevgen Chebotar, Justice Carbajal, Noah Brown, Anthony Brohan, Montserrat Gonzalez Arenas, and Kehang Han. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In Jie Tan, Marc Toussaint, and Kourosh Darvish, editors, _Proceedings of The 7th Conference on Robot Learning_ , volume 229 of _Proceedings of Machine Learning Research_ , pages 2165–2183. PMLR, 06–09 Nov 2023. 

