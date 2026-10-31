---
title: "HAMLET: SWITCH YOUR VISION-LANGUAGE- ACTION MODEL INTO A HISTORY-AWARE POLICY"
venue: "ICLR 2026 Poster"
original: "ICLR 2026 投稿時の匿名版"
url: https://arxiv.org/abs/2510.00695
pdf: https://arxiv.org/pdf/2510.00695
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2510.00695)** / [論文ページ](https://arxiv.org/abs/2510.00695)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。
> ICLR 2026 投稿時の匿名版から変換しました。リンク先の公開版とは内容が異なる場合があります。

Under review as a conference paper at ICLR 2026 

**003** 

**005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 020 021 022 023 024 025 026 027 028 029** 

# **000** HAMLET: SWITCH YOUR VISION-LANGUAGE- **001 002** ACTION MODEL INTO A HISTORY-AWARE POLICY 

#### **004** 

### **Anonymous authors** 

Paper under double-blind review 

## ABSTRACT 

Inherently, robotic manipulation tasks are history-dependent: leveraging past context could be beneficial. However, most existing Vision-Language-Action models (VLAs) have been designed without considering this aspect, _i_ . _e_ ., they rely solely on the current observation, ignoring preceding context. In this paper, we propose HAMLET, a scalable framework to adapt VLAs to attend to the historical context during action prediction. Specifically, we introduce _moment tokens_ that compactly encode perceptual information at each timestep. Their representations are initialized with time-contrastive learning, allowing them to better capture temporally distinctive aspects. Next, we employ a lightweight _memory module_ that integrates the moment tokens across past timesteps into memory features, which are then leveraged for action prediction. Through empirical evaluation, we show that HAMLET successfully transforms a state-of-the-art VLA into a history-aware policy, especially demonstrating significant improvements on long-horizon tasks that require historical context. In particular, on top of GR00T N1.5, HAMLET achieves an average success rate of 76.4% on history-dependent real-world tasks, surpassing the baseline performance by 47.2%. Furthermore, HAMLET pushes prior art performance from 64.1% to 66.4% on RoboCasa Kitchen (100-demo setup) and from 95.6% to 97.7% on LIBERO, highlighting its effectiveness even under generic robot-manipulation benchmarks. Project page: https://iclr-hamlet.github.io/ 

**030 031** 

## 1 INTRODUCTION 

**032 033** Vision-Language-Action models (VLAs; Zitkovich et al. 2023; Kim et al. 2024; Black et al. 2025; Pertsch et al. 2025; Li et al. 2024a; Qu et al. 2025; Bjorck et al. 2025b) have shown their promise in **034** robotic policy learning by leveraging large-scale pre-trained Vision-Language Models (VLMs; Beyer **035** et al. 2024; Chen et al. 2023; Driess et al. 2023; Karamcheti et al. 2024; Touvron et al. 2023) with **036** diverse robot-specific datasets (Walke et al., 2023; O’Neill et al., 2024; Khazatsky et al., 2024). They **037** typically adopt a single-frame assumption, predicting each action solely from the current observation. **038** However, such reliance on a current _snapshot_ fundamentally limits their capability, since robotic **039** manipulation tasks are intrinsically history-dependent. For instance, consider a simple scenario of **040** placing an object on a table. The decision to move the arm depends on prior context—specifically, **041** whether the object has already been grasped. When restricted to the current frame, the policy may **042** struggle to determine the proper next action, particularly if the object is occluded. 

> **043** Despite being a desirable property, incorporating history-awareness during pre-training is viewed 

> **044** as a costly design choice. A major challenge is that leveraging historical context incurs substantial 

> **045** computational overhead. For example, we observe that na¨ıvely appending only four additional past **046** observation frames to the VLA input slows down the forward pass by _∼_ 35% and increases peak **047** memory consumption by _∼_ 3.6 _×_ (see _Multi-frame_ in Table 4). In particular, the inflated memory **048** footprint further restricts scalability by reducing feasible batch sizes compared to the single-frame **049** setting. Together, these observations raise a key research question: _How can we integrate historyawareness into pre-trained VLAs without resorting to costly pre-training from scratch?_ **050** 

> **051** To tackle this problem, we propose **HAMLET** , a fine-tuning framework for VLAs that introduces **052 H** istory- **A** ware **M** emory with **LE** arned **T** okens. Our framework consists of two components: (a) **053** _moment tokens_ , which summarize the instantaneous VLM representations at each timestep, and (b) a _memory module_ , which consolidates moment tokens across different timesteps to produce a temporally 

1 

Under review as a conference paper at ICLR 2026 

**054** (a) History-dependent Long-horizon Tasks (b) Success Rates **055** “ Cover the cube with the nearest cup, then stack the other cup on top of it.” [ Cover and Stack ] **056 057** GR00T N1.5 37.5% 62.5% **058** + Multi-frame 33.3% 70.8% **059 060** + HAMLET (ours) 79.2% 95.8% **061** The cube is under the blue cup… Wait, where is the cube? <mark>Full Partial</mark> **062** [ Swap Cubes ] “ Swap the two cubes, starting with the blue one.” **063 064** GR00T N1.5 37.5% 87.5% **065** + Multi-frame 58.3% 91.7% **066 067** + HAMLET (ours) 83.3% 95.8% **068** <mark>Full Partial</mark> The blue cube was on the right… Wait, which cube to grasp next? **069 070** Figure 1: **Examples of history-dependent long-horizon tasks.** (a) Real-world tasks that involve **071** cases such as object occlusion (upper) or multi-step reasoning (lower) are inherently _non-Markovian_ : **072** proper actions cannot be determined from the current observation alone. (b) Success rates on these tasks show that HAMLET significantly outperforms both GR00T N1.5 and the na¨ıve multi-frame¨ıve multi-frameıve multi-frame **073** baseline, demonstrating its ability to leverage historical context for reliable long-horizon control. **074 075 076** informed condition for action prediction. The moment tokens are appended to the VLM input at each **077** timestep and initialized with time-contrastive learning (Sermanet et al., 2018), which encouragesSermanet et al., 2018), which encourages, 2018), which encourages 2018), which encourages), which encourages **078** distinctiveness across timesteps. This initialization enables the moment tokens to emphasize task- **079** relevant dynamics while suppressing redundant information such as static backgrounds (see Figure 4 4 **080** for details). Building on this, we incorporate a lightweight memory module that stores and integrates **081** moment token representations across timesteps. This design is motivated by the observation that not **082** all moments are equally informative; treating every timestep with equal importance can introduce **083** redundancy and obscure critical cues (see _Moment Concat._ in Table 5c). 5c).). **084** To validate the effectiveness and generality of HAMLET, we conduct comprehensive experiments **085** across both real-world and simulation environments. We first evaluate HAMLET on the long-horizon, **086** real-world tasks that require reasoning over past trajectories. We show that HAMLET improves **087** performance by 47.2% over the na¨ıvely¨ıvelyıvely fine-tuned VLA, which demonstrates the effectiveness **088** of exploiting historical information for real-world robot policy learning. We further examine the **089** generality and applicability of HAMLET across different VLA backbones. When fine-tuning GR00T **090** N1.5 (Bjorck et al., 2025a) on the RoboCasa (Nasiriany et al., 2024) Kitchen dataset,Bjorck et al., 2025a) on the RoboCasa (Nasiriany et al., 2024) Kitchen dataset,, 2025a) on the RoboCasa (Nasiriany et al., 2024) Kitchen dataset, 2025a) on the RoboCasa (Nasiriany et al., 2024) Kitchen dataset,) on the RoboCasa (Nasiriany et al., 2024) Kitchen dataset,Nasiriany et al., 2024) Kitchen dataset,, 2024) Kitchen dataset, 2024) Kitchen dataset,) Kitchen dataset, HAMLET achieves an average success rate of 66.4%, compared to 64.1% for the baseline. Similarly, when **091** applied to CogACT (Li et al., 2024a) on the SimplerEnv-Bridge (Li et al., 2024c) dataset, HAMLETLi et al., 2024a) on the SimplerEnv-Bridge (Li et al., 2024c) dataset, HAMLET, 2024a) on the SimplerEnv-Bridge (Li et al., 2024c) dataset, HAMLET 2024a) on the SimplerEnv-Bridge (Li et al., 2024c) dataset, HAMLET) on the SimplerEnv-Bridge (Li et al., 2024c) dataset, HAMLETLi et al., 2024c) dataset, HAMLET, 2024c) dataset, HAMLET 2024c) dataset, HAMLET) dataset, HAMLET **092** attains 63.5%, substantially improving over the baseline performance of 52.1%. These results **093** highlight that incorporating history-awareness consistently yields benefits across diverse VLA policies, **094** and that HAMLET provides consistent improvements in a flexible, plug-in manner. **095 096 Contributions.** Our contributions are as follows: **097 098** • Motivated by VLAs’ reliance on the current observation alone, we propose HAMLET, an easily **099** integrable framework that enables history-awareness in pre-trained VLAs. **100 101** • We introduce _moment tokens_ , initialized with time-contrastive learning, to capture key temporal **102** cues at each timestep. Building on this, we design a lightweight _memory module_ that selectively aggregates these tokens across timesteps to produce history-aware features for action prediction. **103 104** • We validate HAMLET across both real-world and simulation benchmarks, achieving substantial **105** gains over state-of-the-art baselines. By alleviating backbone models’ reliance on the current **106** observation, HAMLET delivers consistent improvements, especially with the strongest benefits **107** on long-horizon tasks. Importantly, its backbone-agnostic design allows seamless and efficient integration into diverse VLAs without requiring any additional large-scale pre-training. 

Figure 1: **Examples of history-dependent long-horizon tasks.** (a) Real-world tasks that involve cases such as object occlusion (upper) or multi-step reasoning (lower) are inherently _non-Markovian_ : proper actions cannot be determined from the current observation alone. (b) Success rates on these tasks show that HAMLET significantly outperforms both GR00T N1.5 and the na¨ıve multi-frame¨ıve multi-frameıve multi-frame baseline, demonstrating its ability to leverage historical context for reliable long-horizon control. 

informed condition for action prediction. The moment tokens are appended to the VLM input at each timestep and initialized with time-contrastive learning (Sermanet et al., 2018), which encouragesSermanet et al., 2018), which encourages, 2018), which encourages 2018), which encourages), which encourages distinctiveness across timesteps. This initialization enables the moment tokens to emphasize taskrelevant dynamics while suppressing redundant information such as static backgrounds (see Figure 4 4 for details). Building on this, we incorporate a lightweight memory module that stores and integrates moment token representations across timesteps. This design is motivated by the observation that not all moments are equally informative; treating every timestep with equal importance can introduce redundancy and obscure critical cues (see _Moment Concat._ in Table 5c). 5c).). 

To validate the effectiveness and generality of HAMLET, we conduct comprehensive experiments across both real-world and simulation environments. We first evaluate HAMLET on the long-horizon, real-world tasks that require reasoning over past trajectories. We show that HAMLET improves performance by 47.2% over the na¨ıvely¨ıvelyıvely fine-tuned VLA, which demonstrates the effectiveness of exploiting historical information for real-world robot policy learning. We further examine the generality and applicability of HAMLET across different VLA backbones. When fine-tuning GR00T N1.5 (Bjorck et al., 2025a) on the RoboCasa (Nasiriany et al., 2024) Kitchen dataset,Bjorck et al., 2025a) on the RoboCasa (Nasiriany et al., 2024) Kitchen dataset,, 2025a) on the RoboCasa (Nasiriany et al., 2024) Kitchen dataset, 2025a) on the RoboCasa (Nasiriany et al., 2024) Kitchen dataset,) on the RoboCasa (Nasiriany et al., 2024) Kitchen dataset,Nasiriany et al., 2024) Kitchen dataset,, 2024) Kitchen dataset, 2024) Kitchen dataset,) Kitchen dataset, HAMLET achieves an average success rate of 66.4%, compared to 64.1% for the baseline. Similarly, when applied to CogACT (Li et al., 2024a) on the SimplerEnv-Bridge (Li et al., 2024c) dataset, HAMLETLi et al., 2024a) on the SimplerEnv-Bridge (Li et al., 2024c) dataset, HAMLET, 2024a) on the SimplerEnv-Bridge (Li et al., 2024c) dataset, HAMLET 2024a) on the SimplerEnv-Bridge (Li et al., 2024c) dataset, HAMLET) on the SimplerEnv-Bridge (Li et al., 2024c) dataset, HAMLETLi et al., 2024c) dataset, HAMLET, 2024c) dataset, HAMLET 2024c) dataset, HAMLET) dataset, HAMLET attains 63.5%, substantially improving over the baseline performance of 52.1%. These results highlight that incorporating history-awareness consistently yields benefits across diverse VLA policies, and that HAMLET provides consistent improvements in a flexible, plug-in manner. 

2 

Under review as a conference paper at ICLR 2026 

> **108** 2 RELATED WORKS **109** 

> **110 Vision-Language-Action models (VLAs).** Since collecting high-quality and large-scale robot **111** datasets is challenging, traditional robot learning (Shafiullah et al., 2022; Cui et al., 2022; Chi et al., 

> **112** 2023; Lee et al., 2024) has relied on task-specific data, which cover only a narrow distribution of **113** environments, objects, and task instructions. To address this limitation, recent studies (Zitkovich et al., **114** 2023; Driess et al., 2023; Kim et al., 2024; Pertsch et al., 2025; Bjorck et al., 2025a; Li et al., 2024a; **115** Black et al., 2025) propose building generalist robot policies by utilizing internet-scale VLM priors **116** to low-level action prediction, thereby transferring semantic understanding to robotic control. Early **117** VLAs (Zitkovich et al., 2023; Kim et al., 2024; Driess et al., 2023) discretize the continuous action **118** space and directly predict actions as tokens, demonstrating that pre-trained VLMs can be adapted to robot control. More recent approaches (Black et al., 2025; Bjorck et al., 2025b; Li et al., 2024a) **119** leverage VLM representations to condition action experts on diffusion or flow-matching, enabling **120** more accurate action prediction. For example, Black et al. (2025) conditions a flow-matching head 

> **121** on VLM features to produce action chunks per step, and Li et al. (2024a) systematically compares 

> **122** action modules, finding that diffusion action transformers scale favorably when conditioned on 

> **123** VLM representations. However, these models typically generate actions based only on the current **124** observation, limiting their capability to accurately recognize the current state and determine precise **125** actions. In this work, we focus on recent pre-trained VLAs with diffusion-based action heads, and **126** demonstrate how our framework can enhance their performance by incorporating historical context. 

> **127 Memory architectures.** Traditionally, long-horizon tasks have been framed as non-Markovian 

> **128** problems, requiring policies to integrate memory to leverage past observations and actions. In **129** reinforcement learning, recurrent policies (Hausknecht & Stone, 2015) and later Transformer-based 

> **130** variants (Parisotto et al., 2020) introduced memory mechanisms that improved performance on **131** partially observable and long-horizon benchmarks. In natural language processing, explicit memory **132** architectures have been widely explored, ranging from end-to-end memory networks (Sukhbaatar **133** et al., 2015) to retrieval-based approaches (Khandelwal et al., 2019; Lewis et al., 2020), all designed to **134** enhance long-context reasoning and knowledge integration. These advances highlight the importance **135** of dedicated memory modules for tasks requiring extended temporal or contextual awareness. In robotics, prior works (Wen et al., 2020; Seo et al., 2023; Li et al., 2024b; Huang et al., 2025) have **136** incorporated past observations into policy learning, but most approaches (Wen et al., 2020; Seo et al., **137** 2023) rely on simple policy architectures ( _e_ . _g_ ., MLPs or RNNs) with limited generalizability and 

> **138** require training from scratch (Li et al., 2024b; Huang et al., 2025), leading to heavy computational 

> **139** cost. Consequently, memory design for large-scale pre-trained VLAs remains under-explored. As a **140** concurrent effort, Shi et al. (2025) proposes architectures inspired by human memory systems, trained 

> **141** from scratch, and demonstrates promising improvements on temporally dependent tasks. Distinct **142** from this line of work, our approach augments pre-trained VLAs with a few learnable tokens and a **143** lightweight memory module, allowing them to attend to history-awareness without retraining. **144** 

> **145** 3 METHOD **146 147** In this section, we introduce HAMLET, a plug-in framework that adapts pre-trained Vision-Language- **148** Action models (VLAs) to attend the historical context. Formally, let **o** _t_ = [ **I**<sup>1</sup> _t_<sup>_, . . . ,_</sup><sup>**I**</sup><sup>_n_</sup> _t_<sup>] be the sequence</sup> **149** of visual observations at timestep _t_ , and **c** be a task instruction. The VLA _Fθ_ processes these inputs **150** through its Vision-Language Model (VLM) backbone to obtain a hidden representation **h** _t_ : **151 h** _t_ = _Fθ_ ( **o** _t,_ **c** ) _._ (1) **152** Then, the representation **h** _t_ is used as a condition for the action expert _Aψ_ to predict a sequence of _k_ **153** future actions, namely _action chunking_ (Zhao et al., 2023; Chi et al., 2023): **154** [ **a** _t,_ **a** _t_ +1 _, . . . ,_ **a** _t_ + _k−_ 1] = _Aψ_ ( **h** _t,_ **s** _t_ ), (2) 

> **155** where **s** _t_ denotes the robot’s proprioceptive state at timestep _t_ . After executing the predicted action 

> **156** sequence, the environment returns a new observation **o** _t_ + _k_ , which serves as the next input to the 

> **157** VLA. Here, our goal is to augment **h** _t_ with informative representations from previous timesteps 

> **158** ( _i_ . _e_ ., **o** _t−k,_ **o** _t−_ 2 _k, . . ._ ), to enable the action expert to effectively utilize long-horizon context. To **159** achieve this goal, we propose two complementary components: (i) _moment tokens_ , which compress **160** the information at each timestep into a compact representation (see Section 3.1), and (ii) a _memory_ **161** _module_ , which aggregates moment tokens across timesteps to yield a temporally-enriched condition for action prediction (see Section 3.2). The overall framework is illustrated in Figure 2. 

3 

Under review as a conference paper at ICLR 2026 

**162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215** 


Figure 2: **An overview of HAMLET.** Building on a pre-trained VLA, HAMLET adds two key components: _moment tokens_ , appended to the VLM input and initialized with time-contrastive learning to capture task-relevant representations at each timestep, and a lightweight _memory module_ that aggregates these tokens across timesteps for history-aware action prediction. 

### 3.1 CONTEXT COMPRESSION VIA MOMENT TOKENS 

To leverage historical context, we first consider how to effectively store information from each timestep. Retaining the raw visual observation **o** _t_ at every timestep is suboptimal: it incurs high latency and memory costs (see Table 4 in Section 4.3) and often contains redundant or static elements that might provide irrelevant signal (Xu et al., 2025; Yang et al., 2025). To address this, we propose to compress the observation at each timestep into a concise representation that preserves task-relevant information while filtering out redundancy. This motivates the our design of _moment tokens_ . 

**Use of moment tokens.** At each timestep _t_ , we append a set of learnable _moment tokens_ **m** _t ∈_ R<sup>_n_m</sup><sup>_×d_</sup> to the input sequence of the VLM, where _n_ m is the number of tokens and _d_ is the embedding dimension. Given a visual observation **o** _t_ and task instruction **c** , we append moment token **m** _t_ to them and feed the combined input to the VLM encoder _Fθ_ to produce a hidden representation: 


where [ _·_ ; _·_ ] denotes concatenation of token sequences. Along with the hidden states **h** _t_ , we extract the representation **m**<sup>_′_</sup> _t_<sup>of moment tokens, which act as compact, context-aware summaries of the</sup> scene at timestep _t_ . Due to the causal attention operator in the VLM, moment tokens attend to the current visual observation **o** _t_ and the task instruction **c** . As a result, **m**<sup>_′_</sup> _t_<sup>servesasacompressed</sup> representation of each timestep, which subsequently be stored and aggregated by the memory module. 

**Time-contrastive learning.** To encourage moment tokens to encode temporally discriminative cues at each timestep, we draw inspiration from time-contrastive network (Sermanet et al., 2018; Nair et al., 2022; Ma et al., 2023), while adapting the design of positive pairs to image-augmented samples with photometric, blur, noise, and occlusion perturbations. For a trajectory [ **o** 0 _, . . . ,_ **o** _T −_ 1] and task instruction **c** , we extract moment token representations **m**<sup>_′_</sup> _t_<sup>at each timestep using Eq. (3).</sup> 

To construct the contrastive objective, for each timestep _t_ we form an anchor from the current observation **o** _t_ . We then generate a positive **z**<sup>+</sup> _t_<sup>from an augmented view of the same observation</sup> and a hard negative **z**<sup>_−_</sup> _t_<sup>fromadifferenttimestep</sup><sup>_t′̸_=</sup><sup>_t_withinthesametrajectory.Formally,let</sup> **z** _t_ = _g_ ( **m**<sup>_′_</sup> _t_<sup>) denote the projected moment-token representation produced by a projection head</sup><sup>_g_(</sup><sup>_·_).</sup> We then optimize the following time-contrastive learning objective: 


where sim( **a** _,_ **b** ) denotes cosine similarity and _τ_ is a temperature hyperparameter. The summation indexes the _B_ anchors in the minibatch. This initialization encourages the moment tokens to align with 

4 

Under review as a conference paper at ICLR 2026 

**216** representations from the same timestep while remaining discriminative across timesteps, enabling **217 m** _t_ to capture unique, timestep-specific cues while suppressing static components. During this stage, **218** we freeze the VLM _Fθ_ to ensure that the loss does not distort its pre-trained representation. **219 220** 3.2 MEMORY CONSOLIDATION VIA MEMORY MODULE **221 222** We now present a memory module to integrate the moment token representations **m**<sup>_′_</sup> _t_<sup>across timesteps</sup> **223** for action prediction. We observe that simply concatenating these representations does not directly **224** improve performance (see _Moment Concat._ in Table 5c). Hence, we employ a lightweight Transformer **225** _Mϕ_ that selectively attends to informative past timesteps while ignoring less relevant ones. **226 Design of memory module.** To incorporate historical context beyond current timestep, we introduce **227** a memory module _Mϕ_ that aggregates moment token representations across timesteps. Specifically, **228** we employ a shallow Transformer (Vaswani et al., 2017) that attends over past moment tokens via **229** causal self-attention. We form a history matrix by stacking the most recent _T_ moment tokens: **230 231 M**<sup>_′_</sup> = [ **m**<sup>_′_</sup> _t−k_ ( _T −_ 1)<sup>;</sup><sup>_. . ._;</sup><sup>**m**</sup> _t_<sup>_′_</sup> _−k_<sup>;</sup><sup>**m**</sup><sup>_′_</sup> _t_<sup>]</sup><sup>_∈_R</sup><sup>_L×d,_</sup> (5) **232** where _k_ is the action-chunk length from Eq. (2), _T_ is the history length, and _L_ = _T · n_ m is the total **233** number of tokens. From **M**<sup>_′_</sup> , the memory module applies standard self-attention: **234** **<u>QK</u>**<sup>_⊤_</sup> **235 Q** = **M**<sup>_′_</sup> **W** _q_ , **K** = **M**<sup>_′_</sup> **W** _k_ , **V** = **M**<sup>_′_</sup> **W** _v_ , **H** = softmax� _~~√~~ d_<sup>+</sup><sup>**C**</sup> � **V** , (6) **236 237** where **C** is a causal mask ensuring the proper encoding for sequential trajectory. **H** is mapped **238** through the Transformer’s output projection, producing **M**<sup>˜</sup><sup>_′_</sup> _∈_ R<sup>_L×d_</sup> . Then, we take the last _n_ m rows **239** of **M**<sup>˜</sup><sup>_′_</sup> , denoted **m** ˜<sup>_′_</sup> _t_<sup>, as the</sup><sup>_history-augmented_moment token representation for timestep</sup><sup>_t_.</sup> **240 Integration into action prediction.** The history-augmented feature **m** ˜<sup>_′_</sup> is concatenated with the **241** original VLM representation **h** _t_ and fed into the action expert _Aψ_ to predict the next _k_ actions. **242 243** [ **a** _t,_ **a** _t_ +1 _, . . . ,_ **a** _t_ + _k−_ 1] = _Aψ_ ([ **h** _t_ ; **m** ˜<sup>_′_</sup> ] _,_ **s** _t_ ) _._ (7) **244** The overall training procedure follows that of standard VLA models, where the pipeline is trained **245** end-to-end with the action prediction loss (Bjorck et al., 2025b; Li et al., 2024a; Black et al., 2025). **246 247** 4 EXPERIMENTS **248 249** We design our experiments to investigate the following questions: **250 251** • Does applying HAMLET to existing VLAs enhance performance on long-horizon, real-world tasks **252** that require reasoning over past trajectories? (Table 1 in Section 4.2) **253** • Is HAMLET also beneficial on generic robot-manipulation benchmarks? (Table 2, 3 in Section 4.2) **254** • Can HAMLET be seamlessly applied across different pre-trained VLAs? (Table 3 in Section 4.2) **255** • How does HAMLET perform in terms of computational overhead, effective design choices, and **256** transferability to unseen datasets? (Table 4, 5, 6 in Section 4.3, respectively) **257 258** 4.1 EXPERIMENTAL SETUPS **259 260 Datasets.** We evaluate HAMLET on real-world tasks that require reasoning over past trajectories, as **261** well as on diverse simulation benchmarks (Figure 5). In the real-world environment, we design three **262** handcrafted tabletop tasks: (i) _Pick-and-Place Twice_ , where the robot moves a cube between two **263** sides twice; (ii) _Cover-and-Stack_ , where the robot covers a cube with one cup and then stacks it with **264** another; and (iii) _Swap Cubes_ , where the robot swaps the positions of two cubes using an auxiliary **265** site. For the simulation environment, we conduct experiments on three widely-used benchmarks: **266** RoboCasa (Nasiriany et al., 2024) Kitchen, LIBERO (Liu et al., 2023) and SimplerEnv-Bridge (Li et al., 2024c), which consist of multi-step household manipulation tasks spanning diverse objects and **267** configurations. Further details including real-world robot setups are provided in Appendix A.2. **268** 

**269 Baselines.** We design baseline comparisons according to the target benchmark. We primarily evaluate on GR00T N1.5 (Bjorck et al., 2025b) and further assess generalization on CogACT (Li et al., 2024a). 

5 

Under review as a conference paper at ICLR 2026 

**270** (a) Pick-and-Place Twice Should release, but carries away! **271 272 273 274 275** Properly released. **276 277 278 279 280 281** (b) Cover-and-Stack Approaches the same cup again! **282 283 284 285 286** Properly reaches the opposite. **287 288 289 290 291** Figure 3: **Example rollouts of real-world tasks.** We present example rollouts executed by our **292** HAMLET and GR00T N1.5, respectively. While HAMLET predicts proper next actions, in (a) **293** GR00T N1.5 is confused about whether it should lift or release the cube, and in (b) it fails to identify **294** which cup has a cube underneath, due to the absence of historical context. **295 296** Table 1: **Real-world evaluation results.** We report the success rate (%, over 24 trials per task) on **297** three real-world tasks: partial success rates for columns ( _PnP Once, Cover Cube, Stage Cube_ ), and **298** ‘Success’ for full completion. **Bold** and underline indicate the best and runner-up results, respectively. **299 300** Pick-and-Place Twice Cover-and-Stack Swap Cubes **301** Method History? _PnP Once_ Success _Cover Cube_ Success _Stage Cube_ Success Avg. **302** _π_ 0 ✗ 54.2 25.0 87.5 58.3 83.3 12.5 31.9 **303** _π_ 0-FAST ✗ 37.5 20.8 54.2 12.5 66.7 4.2 12.5 GR00T N1 ✗ 54.2 25.0 79.2 33.3 75.0 33.3 30.6 **304** GR00T N1.5 ✗ 54.2 12.5 62.5 37.5 87.5 37.5 29.2 **305** + Multi-frame ✓ 79.2 45.8 70.8 33.3 91.7 58.3 45.8 **306** **<mark>+ HAMLET (Ours)</mark>** <mark>✓</mark> **<mark>91.7 66.7 95.8 79.2 95.8 83.3 76.4</mark> 307 308** For real-world tasks and simulation benchmarks (RoboCasa Kitchen and LIBERO), we compare **309** HAMLET on GR00T N1.5 with representative baselines: _π_ 0 (Black et al., 2025), _π_ 0-FAST (Pertsch **310** et al., 2025), and GR00T N1 (Bjorck et al., 2025b). On SimplerEnv-Bridge, we evaluate HAMLET **311** on CogACT against the reported performances of OpenVLA (Kim et al., 2024), Octo (Team et al., **312** 2024), RoboVLM (Liu et al., 2025) and SpatialVLA (Qu et al., 2025). For comparison with methods **313** that utilize historical context, we implement the multi-frame baseline, which stores past observation **314** frames and concatenates them into the VLA input (see Appendix A.3 for details). **315 Implementation details.** We apply HAMLET to each VLA following the original fine-tuning setup **316** of that model, without heuristic hyperparameter tuning. Instead, we adopt the training configurations **317** specified for each backbone ( _e_ . _g_ ., learning rate, optimizer, and freezing of the VLM backbone). By **318** default, we use moment tokens of length 4, a 2-layer Transformer as the memory module, and a **319** history length of 4. Full hyperparameters and implementation details are provided in Appendix A.3. **320 321** 4.2 MAIN RESULTS **322 323 Real-world evaluation.** For real-world environment, we train each model for each task independently and evaluate their performance by averaging the success rates over 24 trials per task. For each task, 

6 

Under review as a conference paper at ICLR 2026 

> **324** Table 2: **Simulation benchmark results on GR00T N1.5.** We compare HAMLET with baseline **325** methods on RoboCasa Kitchen and LIBERO. For RoboCasa Kitchen, we report the average success 

> **326** rate (%) across 24 tasks with models trained using 30, 100, or 300 demonstrations per task. For **327** LIBERO, each metric is the average success rate (%) across 10 tasks per suite, with training performed **328** jointly on all suites. All the results are reproduced by us, except for those of GR00T N1 on RoboCasa **329** Kitchen. **Bold** and underline indicate best and runner-up results, respectively. **330** RoboCasa Kitchen (# of demos) LIBERO (task suite) **331** Method 30 100 300 Spatial Object Goal Long Avg. **332 333** _π_ 0 <u>47.8</u> 58.7 62.5 97.2 97.2 93.6 89.2 94.3 _π_ 0-FAST 29.8 60.2 63.6 96.0 96.4 91.6 85.0 92.3 **334** GR00T N1 17.4 32.1 49.6 95.6 97.6 94.2 89.6 94.3 **335** GR00T N1.5 <u>47.8 62.6 64.1 98.2 99.4 97.2 87.8 95.6</u> **336** + Multi-frame 44.0 59.3 60.8 81.4 97.2 89.4 79.4 86.8 **337** **<mark>+ HAMLET (Ours) 52.5 65.4 66.4 99.0 100.0 99.2 92.2 97.7</mark> 338 339** Table 3: **Simulation benchmark results on CogACT.** We compare HAMLET with baseline methods 

> **340** on the SimplerEnv-Bridge benchmark. Each metric reports the success rate (%) on four WidowX 

> **341** tasks in SimplerEnv, with separate reporting for grasp success and full success. ‘Avg.’ denotes the **342** average full success rate (%) across the four tasks, and all CogACT results are faithfully reproduced **343** by us. **Bold** and underline indicate best and runner-up results, respectively. **344** Spoon on Towel Carrot on Plate Stack Block Eggplant in Basket **345** Method Grasp Success Grasp Success Grasp Success Grasp Success Avg. **346 347** OpenVLA 4.1 0.0 33.3 0.0 12.5 0.0 8.3 4.1 1.0 Octo-Base 34.7 12.5 52.8 8.3 31.9 0.0 66.7 43.1 16.0 **348** Octo-Small 77.8 47.2 27.8 9.7 40.3 4.2 87.5 56.9 30.0 **349** RoboVLM 54.2 29.2 25.0 25.0 45.8 12.5 58.3 58.3 31.3 **350** SpatialVLA 20.8 16.7 29.2 25.0 62.5 **29.2 100.0 100.0** 42.7 **351** CogACT <u>87.5 58.3</u> 41.7 37.5 <u>70.8 20.8 91.7 91.7 52.1</u> + Multi-frame 83.3 50.0 <u>79.2 50.0 70.8 20.8</u> 70.8 70.8 47.9 **352** **<mark>+ HAMLET (Ours) 91.7 75.0 83.3 62.5 75.0</mark>** <mark>16.7</mark> **<mark>100.0 100.0 63.5</mark> 353 354 355** partial success rates are also reported, where the criteria are: (i) _Pick-and-Place Once_ : pick and place **356** the cube at the correct site once; (ii) _Cover Cube_ : cover the first cube with the nearest cup; and (iii) **357** _Stage Cube_ , stage the a cube to the auxiliary site. As shown in Table 1 and Figure 3, the base model (GR00T N1.5) struggles with these tasks, achieving only 12.5% success on Pick-and-Place Twice and **358** often becoming confused about which direction to move (see more rollouts in Appendix B.2). Notably, 

> **359** applying HAMLET to GR00T N1.5 yields substantial improvements across all tasks, achieving an **360** average improvement of 47.2% and underscoring its effectiveness in leveraging historical context. **361 362 Simulation benchmarks.** To validate generalizability of HAMLET across generic benchmarks, **363** we evaluate it on the standard simulation benchmarks, RoboCasa (Nasiriany et al., 2024) and LIBERO (Liu et al., 2023). As shown in Table 2, na¨ıvely extending GR00T N1.5 with multi-frame **364** inputs degrades the baseline performance by 3.3% in RoboCasa (100 demos) and 8.8% in LIBERO. **365** This highlights an inherent weakness of this approach: (a) by conditioning only on consecutive 

> **366** frames during training, the model struggles to generalize to test environments with dynamically 

> **367** varying observations, and (b) merely accessing more past information can cause the policy to pick **368** up spurious temporal correlations, a phenomenon also known as causal confusion (Wen et al., 2020; 

> **369** De Haan et al., 2019; Seo et al., 2023). On the other hands, HAMLET, when applied on top of **370** GR00T N1.5, successfully improves performance across benchmarks: in LIBERO, it pushes the prior **371** best score 95.6%, near-saturated success rate—up to 97.7%. This supports the advantage of our **372** design: since HAMLET still receives single-frame inputs via external memory module, it effectively **373** exploits historical context while preserving single-frame VLA’s generalizability. **374 Generalization to other VLAs.** We further validate the scalability of our framework in transforming 

> **375** existing VLAs into history-aware policy beyond GR00T N1.5. Specifically, we consider CogACT **376** (Li et al., 2024a) as base model, which is another pre-trained VLA based on diffusion policy, on the **377** Simpler-WidowX simulation benchmark (Walke et al., 2023). Table 3 reports both partial and full success rates across four tasks. Similar other simulation results ( _e_ . _g_ ., Table 2), the multi-frame baseline 

7 

Under review as a conference paper at ICLR 2026 

**378** Attention **379** weights **380 381 382 383 384 385 386 387 388** (a) Moment token attention over images (b) Memory attention across timesteps (at timestep t) **389 390** Figure 4: **What does the memory network memorize?** (a) Visualization of self-attention map of **391** moment tokens over input images inside the VLM, showing that they concentrate strongly on taskrelevant regions. (b) Normalized self-attention weights of the memory module across the moment **392** token sequence, indicating which timesteps contribute most to the memory features. **393 394 395** Table 4: **Efficiency analysis.** Average latency and peak memory usage measured on RoboCasa datasets. Both metrics are computed at each timestep within an episode and then averaged. For fair **396** comparison, memory for original VLA parameters is excluded, except for the memory module in **397** HAMLET. All measurements were on an NVIDIA A100 GPU. _↓_ indicates lower values are better. **398 399** Method History Length Latency (ms, _↓_ ) Peak memory (MB, _↓_ ) **400** GR00T N1.5 1 80.5 (1.00 _×_ ) 289 (1.00 _×_ ) **401 402** + Multi-frame 4 108.5 (1.35 _×_ ) 1051 (3.64 _×_ ) **<mark>+ HAMLET (Ours)</mark>** <mark>4</mark> **<mark>82.4</mark>** <mark>(</mark> **<mark>1.02</mark>** _<mark>×</mark>_ <mark>)</mark> **<mark>566</mark>** <mark>(</mark> **<mark>1.96</mark>** _<mark>×</mark>_ <mark>)</mark> **403 404** + Multi-frame 8 193.0 (2.40 _×_ ) 2023 (7.00 _×_ ) **<mark>+ HAMLET (Ours)</mark>** <mark>8</mark> **<mark>85.8</mark>** <mark>(</mark> **<mark>1.07</mark>** _<mark>×</mark>_ <mark>)</mark> **<mark>578</mark>** <mark>(</mark> **<mark>2.00</mark>** _<mark>×</mark>_ <mark>)</mark> **405 406 407** fails to consistently improve success rate across tasks, possibly due to the its pool generalizability. In **408** other hands, HAMLET still demonstrates clear improvements: it not only improve partial success **409** rates across all tasks but, more importantly, significantly improves final task completion, achieving **410** an average full success rate of 63.5%, compared to the original 52.1%. These highlight HAMLET’s **411** flexibility as an easily integrable fine-tuning framework, without the need for costly re-training. **412 413** 4.3 MORE ANALYSIS **414 415** We further analyze the individual components in HAMLET and its efficiency over baselines. Through- **416** out this section, unless otherwise specified, we consider the GR00T N1.5 on RoboCasa (100 demos). **417 What does the memory module memorize?** We qualitatively analyze (a) how the proposed **418** moment tokens encode information at each timestep and (b) how the memory module processes past **419** information. First, we confirm that the moment token attends more to task-relevant parts that change **420** over timesteps and less to static parts. Indeed, as shown in Figure 4(a), higher attention values of 4(a), higher attention values of(a), higher attention values of **421** the moment token concentrate on the gripper and objects that are associated with task success, while **422** lower attention values are assigned to background regions. This is possibly due to the initialization **423** via time-contrastive loss (see Section 3.1), which encourages the tokens to extract distinguishable 3.1), which encourages the tokens to extract distinguishable), which encourages the tokens to extract distinguishable **424** features over time. Next, we observe that the memory module selectively attends to past information **425** depending on the context within the episode. As shown in Figure 4(b), in the 4(b), in the(b), in the _Cover-and-Stack_ task, **426** at the moment when it is necessary to decide which cup to approach after the cube is covered with **427** a cup, the memory module assigns higher attention to the past timestep when the blue cube was previously visible. Additional qualitative results are provided in Appendix B.2. B.2.. **428 429 Efficiency analysis.** We analyze the efficiency of HAMLET by comparing with the multi-frame **430** baseline which na¨ıvely appends past observation frames, under varying history lengths. Specifically, **431** we measure average latency (ms) and average peak GPU memory usage (MB) per environment timestep in the RoboCasa simulation. As shown in Table 4, the multi-frame baseline incurs substantial 

Figure 4: **What does the memory network memorize?** (a) Visualization of self-attention map of moment tokens over input images inside the VLM, showing that they concentrate strongly on taskrelevant regions. (b) Normalized self-attention weights of the memory module across the moment token sequence, indicating which timesteps contribute most to the memory features. 

We further analyze the individual components in HAMLET and its efficiency over baselines. Throughout this section, unless otherwise specified, we consider the GR00T N1.5 on RoboCasa (100 demos). 

**What does the memory module memorize?** We qualitatively analyze (a) how the proposed moment tokens encode information at each timestep and (b) how the memory module processes past information. First, we confirm that the moment token attends more to task-relevant parts that change over timesteps and less to static parts. Indeed, as shown in Figure 4(a), higher attention values of 4(a), higher attention values of(a), higher attention values of the moment token concentrate on the gripper and objects that are associated with task success, while lower attention values are assigned to background regions. This is possibly due to the initialization via time-contrastive loss (see Section 3.1), which encourages the tokens to extract distinguishable 3.1), which encourages the tokens to extract distinguishable), which encourages the tokens to extract distinguishable features over time. Next, we observe that the memory module selectively attends to past information depending on the context within the episode. As shown in Figure 4(b), in the 4(b), in the(b), in the _Cover-and-Stack_ task, at the moment when it is necessary to decide which cup to approach after the cube is covered with a cup, the memory module assigns higher attention to the past timestep when the blue cube was previously visible. Additional qualitative results are provided in Appendix B.2. B.2.. 

8 

Under review as a conference paper at ICLR 2026 

> **432** Table 5: **Ablation study.** Average success rate (%) on RoboCasa (100 demos) when selectively en- **433** abling different components of HAMLET. _Moment Concat._ concatenates all moment tokens without **434** a memory module, whereas the Transformer-based memory yields the best overall performance. **435 436** Moment Memory Token Length Avg. Method Avg. **437** Token TCL Module Avg. 1 64.3 No Memory 62.6 **438** ✗ ✗ ✗ 62.6 4 65.4 Moment Concat. 62.7 **439** ✓ ✗ ✗ 63.1 **8 66.4** RNN 64.5 ✓ ✓ ✗ 63.4 16 65.9 LSTM 65.0 **440** ✓ ✗ ✓ 64.8 32 62.7 GRU 64.3 **441** ✓ ✓ ✓ **65.4** 64 62.5 **Transformer 65.4 442 443** (a) Component analysis. (b) Moment token length. (c) Memory architecture. **444** overhead in both metrics. For example, at a history length of 8, it requires roughly 2 _._ 4 _×_ greater 

> **445** latency and 7 _×_ higher memory than vanilla inference. In contrast, HAMLET shows only minimal 

> **446** overheads across history lengths, _e.g._ , 1.02 _×_ at length 4 and 1.07 _×_ at length 8. These results **447** demonstrate the clear advantage of HAMLET over the multi-frame baseline in terms of efficiency. **448 449 Ablation study.** We perform ablations on HAMLET to study the individual roles of its components, moment token length, and memory design. First, to assess the contribution of each component, we **450** conduct an ablation study by removing key components one at a time: (i) the use of moment tokens, (ii) **451** the initialization of Time-Contrastive Learning (TCL), and (iii) the presence of the memory module. 

> **452** In Table 5a, we confirm that removing the memory module leads to the largest performance drop, 

> **453** thereby confirming its critical role. We also observe that removing TCL-initialization consistently 

> **454** decreases performance, regardless of whether the memory module is used. Next, we examine the **455** effect of moment token length (default = 4). Table 5b shows the performance improves as the length **456** increases up to 8, but then gradually decreases beyond this point. Lastly, to understand the effect of **457** design choices for memory module, we compare several architectures: (i) _Moment Concat._ , which **458** na¨ıvely concatenates past moment tokens without a memory module, (ii) RNN (Graves, 2012), LSTM **459** (Hochreiter & Schmidhuber, 1997), and GRU (Cho et al., 2014), which are recurrent variants that **460** utilize a single accumulated hidden state, (iii) Transformer, which we used in our experiments. From Table 5c, we find that the Transformer achieves the highest average success rate among the memory **461** architectures. Interestingly, we observe that _Moment Concat._ yields almost no gains over the baseline, **462** whereas other memory-based methods have shown performance gains. **463 464 Generalization capability.** We investigate Table 6: **Generalization of memory module.** The **465** whether the memory module in our framework memory module is trained with the dataset left of **466** can transfer to unseen tasks, under the hythe arrow. A LIBERO-pretrained module provides **467** pothesis that it learns generalizable knowledge gains for manipulation on RoboCasa, identifying for identifying which information from past that the learned memory representations can gener- **468** timesteps is important, not limited to a specific alize across embodiment datasets. **469** dataset. To verify this, we first train the memory 

> **470** module and then freeze it while evaluating on Method Avg. **471** different datasets. Specifically, we first train the GR00T N1.5 62.6 

> **472** memory module on LIBERO and then transfer + HAMLET (LIBERO _→_ RoboCasa) 64.5 

> **473** it directly to RoboCasa. As shown in Table 6, + HAMLET (RoboCasa _→_ RoboCasa) **65.4 474** even in this setup, HAMLET achieves a success **475** rate comparable to the in-distribution setting, where both training and evaluation are performed on **476** RoboCasa. This demonstrates the practical flexibility of HAMLET to generalize across datasets, **477** while eliminating the additional training cost for memory module adaptation. **478** 

> **479** 5 CONCLUSION **480** 

> **481** In this work, we address the limitation of existing Vision-Language-Action models (VLAs), which **482** typically rely on the current observation while ignoring past context. We propose HAMLET, a simple 

> **483** yet effective framework that enables pre-trained VLAs to leverage historical information without **484** costly retraining from scratch. By introducing a lightweight memory module that integrates learnable **485** moment tokens, HAMLET achieves significant improvements on long-horizon real-world tasks and standard simulation benchmarks, while maintaining computational efficiency. We hope our approach 

9 

Under review as a conference paper at ICLR 2026 

**486** paves the way toward leveraging history-awareness in off-the-shelf VLA policies to tackle more **487** complex robotic manipulation tasks reliably and effectively in practice. 

**488** 

**489** REPRODUCIBILITY STATEMENT **490 491 492** We provide full hyperparameter and implementation details in Section 4 and Appendix A. **493 494** REFERENCES **495 496** Lucas Beyer, Andreas Steiner, Andre´ Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. **497** Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. **498 499** Johan Bjorck, Valts Blukis, Fernando Castaneda,˜ Nikita Cherniadev, Xingye Da, Runyu Ding, **500** Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1.5: An improved **501** open foundation model for generalist humanoid robots. https://research.nvidia.com/ **502** labs/gear/gr00t-n1_5/, June 2025a. Accessed: 2025-09-09. **503** Johan Bjorck, Fernando Castaneda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang,˜ **504** Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist **505** humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025b. **506 507** Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, **508** Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0 : A vision-language-action flow model for **509** general robot control. _RSS_ , 2025. **510** Ting Chen, Simon Kornblith, Mohammad Norouzi, and Geoffrey Hinton. A simple framework for **511** contrastive learning of visual representations. In _International conference on machine learning_ , pp. **512** 1597–1607. PmLR, 2020. **513 514** Xi Chen, Josip Djolonga, Piotr Padlewski, Basil Mustafa, Soravit Changpinyo, Jialin Wu, Car- **515** los Riquelme Ruiz, Sebastian Goodman, Xiao Wang, Yi Tay, et al. Pali-x: On scaling up a **516** multilingual vision and language model. _arXiv preprint arXiv:2305.18565_ , 2023. **517** Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, **518** and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The_ **519** _International Journal of Robotics Research_ , pp. 02783649241273668, 2023. **520 521** Kyunghyun Cho, Bart van Merrienboer, Dzmitry Bahdanau, and Yoshua Bengio.¨ On the properties **522** of neural machine translation: Encoder–decoder approaches. In Dekai Wu, Marine Carpuat, Xavier Carreras, and Eva Maria Vecchi (eds.), _Proceedings of SSST-8, Eighth Workshop on_ **523** _Syntax, Semantics and Structure in Statistical Translation_ , pp. 103–111, Doha, Qatar, October **524** 2014. Association for Computational Linguistics. doi: 10.3115/v1/W14-4012. URL https: **525** //aclanthology.org/W14-4012/. **526 527** Zichen Jeff Cui, Yibin Wang, Nur Muhammad Mahi Shafiullah, and Lerrel Pinto. From play to policy: **528** Conditional behavior generation from uncurated robot data. _arXiv preprint arXiv:2210.10047_ , 2022. **529 530** Pim De Haan, Dinesh Jayaraman, and Sergey Levine. Causal confusion in imitation learning. **531** _Advances in neural information processing systems_ , 32, 2019. **532 533** Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Ayzaan Wahid, **534** Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, et al. Palm-e: An embodied **535** multimodal language model. _arXiv preprint arXiv:2303.03378_ , 2023. **536** Alex Graves. Supervised sequence labelling. In _Supervised sequence labelling with recurrent neural_ **537** _networks_ , pp. 5–13. Springer, 2012. **538 539** Matthew J Hausknecht and Peter Stone. Deep recurrent q-learning for partially observable mdps. In _AAAI fall symposia_ , volume 45, pp. 141, 2015. 

10 

Under review as a conference paper at ICLR 2026 

**540** Sepp Hochreiter and Jurgen¨ Schmidhuber. Long short-term memory. _Neural computation_ , 9(8): **541** 1735–1780, 1997. **542 543** Huang Huang, Fangchen Liu, Letian Fu, Tingfan Wu, Mustafa Mukadam, Jitendra Malik, Ken **544** Goldberg, and Pieter Abbeel. OTTER: A vision-language-action model with text-aware visual **545** feature extraction. In _Forty-second International Conference on Machine Learning_ , 2025. URL **546** https://openreview.net/forum?id=UHF0km7R5M. **547** Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa **548** Sadigh. Prismatic vlms: Investigating the design space of visually-conditioned language models. **549** In _International Conference on Machine Learning_ , 2024. **550 551** Urvashi Khandelwal, Omer Levy, Dan Jurafsky, Luke Zettlemoyer, and Mike Lewis. Generalization **552** through memorization: Nearest neighbor language models. _arXiv preprint arXiv:1911.00172_ , 2019. **553 554** Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth **555** Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, **556** et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , **557** 2024. **558** Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, **559** Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source **560** vision-language-action model. In _Conference on Robot Learning_ , 2024. **561 562** Seungjae Lee, Yibin Wang, Haritheja Etukuru, H. Jin Kim, Nur Muhammad Mahi Shafiullah, and **563** Lerrel Pinto. Behavior generation with latent actions. In _International Conference on Machine_ **564** _Learning_ , 2024. URL https://openreview.net/forum?id=hoVwecMqV5. **565** Barak Lenz, Opher Lieber, Alan Arazi, Amir Bergman, Avshalom Manevich, Barak Peleg, Ben **566** Aviram, Chen Almagor, Clara Fridman, Dan Padnos, et al. Jamba: Hybrid transformer-mamba **567** language models. In _International Conference on Learning Representations_ , 2025. **568 569** Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, **570** Heinrich Kuttler, Mike Lewis, Wen-tau Yih, Tim Rockt¨ aschel, et al.¨ Retrieval-augmented genera- **571** tion for knowledge-intensive nlp tasks. _Advances in Neural Information Processing Systems_ , 33: 9459–9474, 2020. **572 573** Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, **574** Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational vision-language-action model for **575** synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024a. **576** Xinghang Li, Peiyan Li, Minghuan Liu, Dong Wang, Jirong Liu, Bingyi Kang, Xiao Ma, Tao Kong, **577** Hanbo Zhang, and Huaping Liu. Towards generalist robot policies: What matters in building **578** vision-language-action models. _arXiv preprint arXiv:2412.14058_ , 2024b. **579 580** Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa **581** Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating real-world robot manipulation policies in **582** simulation. _arXiv preprint arXiv:2405.05941_ , 2024c. **583** Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: **584** Benchmarking knowledge transfer for lifelong robot learning. _NeurIPS_ , 36:44776–44791, 2023. **585 586** Huaping Liu, Xinghang Li, Peiyan Li, Minghuan Liu, Dong Wang, Jirong Liu, Bingyi Kang, Xiao **587** Ma, Tao Kong, and Hanbo Zhang. Towards generalist robot policies: What matters in building **588** vision-language-action models. _arXiv preprint arXiv:2412.14058_ , 2025. 

- Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024a. 

**589 590 591 592** 

   - Yecheng Jason Ma, Shagun Sodhani, Dinesh Jayaraman, Osbert Bastani, Vikash Kumar, and Amy Zhang. Vip: Towards universal visual reward and representation via value-implicit pre-training. _arXiv preprint arXiv:2210.00030_ , 2023. 

- **593** Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea Finn, and Abhinav Gupta. R3m: A universal visual representation for robot manipulation. _arXiv preprint arXiv:2203.12601_ , 2022. 

11 

Under review as a conference paper at ICLR 2026 

**594** NVIDIA Nemotron Nano. Efficient hybrid mamba-transformer reasoning model. _arXiv preprint_ **595** _arXiv:2508.14444_ , 2025. **596 597** Soroush Nasiriany, Abhiram Maddukuri, Lance Zhang, Adeet Parikh, Aaron Lo, Abhishek Joshi, **598** Ajay Mandlekar, and Yuke Zhu. Robocasa: Large-scale simulation of everyday tasks for generalist **599** robots. In _Robotics: Science and Systems_ , 2024. **600** Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham **601** Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: **602** Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _IEEE Interna-_ **603** _tional Conference on Robotics and Automation_ , pp. 6892–6903. IEEE, 2024. **604 605** Emilio Parisotto, Francis Song, Jack Rae, Razvan Pascanu, Caglar Gulcehre, Siddhant Jayakumar, **606** Max Jaderberg, Raphael Lopez Kaufman, Aidan Clark, Seb Noury, et al. Stabilizing transformers for reinforcement learning. In _International Conference on Machine Learning_ , pp. 7487–7498. **607** PMLR, 2020. **608 609** Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, **610** Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action **611** models. _arXiv preprint arXiv:2501.09747_ , 2025. **612** Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, **613** Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visual-language- **614** action model. _arXiv preprint arXiv:2501.15830_ , 2025. **615 616** Seokin Seo, HyeongJoo Hwang, Hongseok Yang, and Kee-Eung Kim. Regularized behavior cloning **617** for blocking the leakage of past action information. _Advances in Neural Information Processing_ **618** _Systems_ , 36:2128–2153, 2023. **619** Pierre Sermanet, Corey Lynch, Yevgen Chebotar, Jasmine Hsu, Eric Jang, Stefan Schaal, Sergey **620** Levine, and Google Brain. Time-contrastive networks: Self-supervised learning from video. In **621** _IEEE International Conference on Robotics and Automation_ , pp. 1134–1141. IEEE, 2018. **622 623** Nur Muhammad Shafiullah, Zichen Cui, Ariuntuya Arty Altanzaya, and Lerrel Pinto. Behavior **624** transformers: Cloning _k_ modes with one stone. In _Advances in Neural Information Processing_ **625** _Systems_ , volume 35, pp. 22955–22968, 2022. **626** Hao Shi, Bin Xie, Yingfei Liu, Lin Sun, Fengrong Liu, Tiancai Wang, Erjin Zhou, Haoqiang Fan, **627** Xiangyu Zhang, and Gao Huang. Memoryvla: Perceptual-cognitive memory in vision-language- **628** action models for robotic manipulation. _arXiv preprint arXiv:2508.19236_ , 2025. **629 630** Sainbayar Sukhbaatar, Jason Weston, Rob Fergus, et al. End-to-end memory networks. _Advances in Neural Information Processing Systems_ , 28, 2015. **631** 

> **632** Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep 

> **633** Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot **634** policy. In _Conference on Robot Learning_ , 2024. **635 636** Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation **637** and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. **638** 

- **639** Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz **640** Kaiser, and Illia Polosukhin. Attention is all you need. _Advances in neural information processing_ **641** _systems_ , 30, 2017. 

**642** 

**643** 

**644** 

- Homer Rich Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, Philippe HansenEstruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pp. 1723–1736. PMLR, 2023. 

**645** 

- **646** Chuan Wen, Jierui Lin, Trevor Darrell, Dinesh Jayaraman, and Yang Gao. Fighting copycat agents **647** in behavioral cloning from observation histories. _Advances in Neural Information Processing Systems_ , 33:2564–2575, 2020. 

12 

Under review as a conference paper at ICLR 2026 

**648** Siyu Xu, Yunke Wang, Chenghao Xia, Dihao Zhu, Tao Huang, and Chang Xu. Vla-cache: Towards **649** efficient vision-language-action model via adaptive token caching in robotic manipulation. _arXiv_ **650** _preprint arXiv:2502.02175_ , 2025. **651** 

- **652** Yantai Yang, Yuhao Wang, Zichen Wen, Luo Zhongwei, Chang Zou, Zhipeng Zhang, Chuan Wen, **653** and Linfeng Zhang. Efficientvla: Training-free acceleration and compression for vision-language- **654** action models. _arXiv preprint arXiv:2506.10100_ , 2025. 

> **655** Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual **656** manipulation with low-cost hardware. In _Robotics: Science and Systems_ , 2023. **657 658** Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, **659** Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. **660 661 662 663 664 665 666 667 668 669 670 671 672 673 674 675 676 677 678 679 680 681 682 683 684 685 686 687 688 689 690 691 692 693 694 695 696 697 698 699 700 701** 

13 

Under review as a conference paper at ICLR 2026 

**702 703 704 705 706 707 708 709 710 711 712 713 714 715 716 717 718 719 720 721 722 723 724 725 726 727 728 729 730 731 732 733 734 735 736 737 738 739 740 741 742 743 744 745 746 747 748 749 750 751 752 753 754 755** 

## A EXPERIMENTAL DETAILS 

### A.1 MODEL DETAILS 

In our experiments, we evaluate diffusion-based VLAs: GR00T N1 (Bjorck et al., 2025b)<sup>1</sup> , GR00T N1.5 (Bjorck et al., 2025a)<sup>2</sup> , _π_ 0 (Black et al., 2025)<sup>3</sup> , _π_ 0-FAST (Pertsch et al., 2025)<sup>4</sup> , and CogACT (Li et al., 2024a)<sup>5</sup> . All checkpoints are obtained from their official repositories. 

### A.2 DATASETS 

We evaluate HAMLET across both real and simulation environments, as demonstrated in Figure 5. 


Figure 5: **Evaluation environments.** Left: Real-world evaluation comprises three tabletop tasks, which especially require awareness on historical context. Right: Simulation benchmarks include RoboCasa (Nasiriany et al., 2024) Kitchen, LIBERO (Liu et al., 2023), and SimplerEnv-Bridge (Li et al., 2024c), which consist of diverse indoor manipulation tasks. 

**Real-world environment.** As shown in Figure 6, we use a Franka Research 3 robot arm equipped with a Robotiq 2F-85 gripper, following the DROID (Khazatsky et al., 2024) setup. Two camera views are provided: one mounted on the table and another on the wrist. On this real-robot platform, we design three handcrafted tabletop tasks as illustrated in Figure 7: (i) _Pick-and-Place Twice_ , where the robot moves a cube between two sides twice; (ii) _Cover-and-Stack_ , where the robot covers a cube with the nearest cup and then stacks another cup on top; and (iii) _Swap Cubes_ , where the robot swaps the positions of two cubes using an auxiliary site. For each task, we collect 50 demonstrations for training, and report frame statistics in Table 7. Since trajectories are on average about 268 frames long, we evaluate each trial with a maximum limit of 700 timesteps: if the task has not been completed by then, the episode is counted as a failure. 


Figure 6: **Real-robot platform.** We specify the robot specifications and multi-camera views. 

- 1https://huggingface.co/nvidia/GR00T-N1-2B 

2https://huggingface.co/nvidia/GR00T-N1.5-3B 

3gs://openpi-assets/checkpoints/pi0_base 

4gs://openpi-assets/checkpoints/pi0_fast_base 

5https://huggingface.co/CogACT/CogACT-Base 

14 

Under review as a conference paper at ICLR 2026 

**756** Pick-and-Place Twice Partial Full **757 758 759 760 761 762** Start! Pick up cube Move it to opposite side Release it Pick it up again Place it back! **763 764** Cover-and-Stack Partial Full **765 766 767 768 769** Start! Pick up cup Cover cube Move to other cup Move it opposite side Stack it! **770 771** Swap Cubes Partial Full **772 773 774 775 776 777** Start! Pick up blue cube Stage it Move green cube Move blue cube! **778 779** Figure 7: **Real-world tasks.** We design three history-dependent real-world tasks. Each partial criteria **780** ( _Pick-and-Place Once_ , _Cover Cube_ , _Stage Cube_ ) is described as the corresponding frame. **781 782** Table 7: **Dataset statistics for real-world tasks.** For each real-world dataset, we present the mean, **783** maximum, and standard deviation of frame counts per episode. These statistics provide a basis for **784** determining an appropriate maximum timestep limit during evaluation. **785** Task Mean #frames Max #frames Std #frames **786 787** Pick-and-Place Twice 261 350 25.1 Cover-and-Stack 230 270 24.2 **788** Swap Cubes 312 361 20.8 **789 790 791 792 Simulation benchmarks.** We evaluate HAMLET on three standard simulation benchmarks: (i) **793** RoboCasa (Nasiriany et al., 2024), (ii) LIBERO (Liu et al., 2023) using GR00T N1.5, and (iii) SimplerEnv-Bridge (Walke et al., 2023) using CogACT. RoboCasa is a suite of kitchen manipulation **794** tasks, comprising 24 tasks across 120 scenes. Following Bjorck et al. (2025a), we split the dataset **795** into training and evaluation sets, evaluating each task over 50 episodes. LIBERO is designed to **796** benchmark multi-task and lifelong robot learning, and includes 40 tasks grouped into four suites **797** (Spatial, Object, Goal, and Long). Both RoboCasa and LIBERO use a Franka robot, and we adopt **798** their officially released code for training and evaluation. Lastly, for SimplerEnv-Bridge, focused on **799** real-to-simulation transfer, we use the BridgeV2 dataset (Walke et al., 2023) with a WidowX robot. **800 801** A.3 IMPLEMENTATION **802 803 Moment token and memory module.** Across experiments, we set the sequence length of moment **804** tokens to 4 and use a 2-layer Transformer as the memory module. For the Transformer implemen- **805** tation, we adapt the LLaMA codebase from Hugging Face.<sup>6</sup> To initialize the moment tokens via **806** Time-Contrastive Learning (TCL), we construct positive pairs using a combination of photometric **807** distortions (brightness, contrast, and color jitter), Gaussian blur/noise, and small-patch occlusions **808** applied stochastically to the same frame. Negative pairs are obtained by uniformly sampling frames **809** 

> 6https://huggingface.co/docs/transformers/en/model_doc/llama 

15 

Under review as a conference paper at ICLR 2026 

**810** that are more than 16 timesteps apart within the same trajectory, corresponding to the action horizon. **811** We use a contrastive temperature of 0.07 for all TCL-based pre-training. **812** 

**813 Multi-frame baseline.** We follow the approach of multi-frame policies (Team et al., 2024; Liu et al., **814** 2025) in handling historical observations to construct a na¨ıve multi-frame baseline. For GR00T N1.5, we concatenate past observation frames across the three original views, _i_ . _e_ ., left, right, and wrist. For **815** CogACT, since the original VLM is designed to process only a single view per timestep, we instead **816** use a its cognition token and concatenate it to condition the action expert. **817 818** A.4 TRAINING DETAILS **819 820** Based on the official training recipes (Bjorck et al., 2025a; Li et al., 2024a), we fine-tune GR00T **821** N1.5 and CogACT. **822 823** • **GR00T N1.5** : Fine-tuned with the memory module for 60k steps using a batch size of 32 and a **824** learning rate of 1e-5. Initialization of moment tokens with TCL is performed for up to 30k steps **825** with a batch size of 64 and the same learning rate. During fine-tuning, both the VLM and moment **826** tokens are kept frozen. **827** • **CogACT** : Fine-tuned with the memory module for 20k steps using a batch size of 32 and a learning **828** rate of 2e-5. Initialization of moment tokens with TCL is performed for up to 30k steps with a **829** batch size of 64 and the same learning rate, but training is terminated at 10k steps once the loss **830** converges. During fine-tuning, both the VLM and moment tokens remain trainable. **831** In both cases, we use a default history length of 4. For all other baselines, including _π_ 0, _π_ 0-FAST, **832** and GR00T N1, we also follow their official training codes. **833 834** A.5 COMPUTATIONAL RESOURCES **835 836** • **GR00T N1.5** : Experiments is conducted on NVIDIA A100 80GB GPUs. Fine-tuning with the **837** memory module on 4 GPUs requires _∼_ 16 hours, comparable to the standard training time of _∼_ 14 **838** hours. Initialization of moment tokens with TCL adds _∼_ 5 hours on 2 GPUs. **839** • **CogACT** : Experiments is conducted on NVIDIA H200 141GB GPUs. Fine-tuning with the memory **840** module on 4 GPUs take _∼_ 9 hours, compared to _∼_ 4 hours for the standard setup. TCL-initialization **841** requires _∼_ 9 hours on 2 H100 GPUs. **842 843** We provide a summarization table detailing the modification costs ( _i_ . _e_ ., model parameters, inference **844** time, and training time) in Table 8. **845** Table 8: **Modification cost across different VLA types.** We report three metrics: model parameters, **846** inference time, and training time. All inference was conducted on a single NVIDIA A100 GPU. **847** Training was performed on 4 NVIDIA H200 GPUs, except for GR00T N1.5, whose VLM backbone **848** was frozen during training and was therefore trained on 4 NVIDIA A100 GPUs. **849 850** Method Model parameters Inference time (ms) Training time (hours) **851** GR00T N1.5 2.72B 80.5 (1.00 _×_ ) _∼_ 14 **852** **<mark>+ HAMLET</mark>** <mark>2.86B 82.4 (1.02</mark> _<mark>×</mark>_ <mark>)</mark> _<mark>∼</mark>_ <mark>16</mark> **853 854** CogACT 7.63B 229.6 (1.00 _×_ ) _∼_ 4 **<mark>+ HAMLET</mark>** <mark>8.17B 234.0 (1.01</mark> _<mark>×</mark>_ <mark>)</mark> _<mark>∼</mark>_ <mark>9</mark> **855 856 857 858** B MORE EXPERIMENTAL RESULTS **859 860** B.1 QUANTITATIVE RESULTS **861 862** We provide additional quantitative results to better understand the main components of HAMLET **863** and its generalizability across various scenarios. We also present the complete RoboCasa metrics in Table 9, including the per-task success rates summarized in Table 2 for HAMLET and GR00T N1.5. 

16 

Under review as a conference paper at ICLR 2026 

**864 865 866 867 868 869 870 871 872 873 874 875 876 877 878 879 880 881 882 883 884 885 886 887 888 889 890 891** 

Table 9: **Full results on RoboCasa Kitchen with different dataset size.** 

|||GR00T N1.5||GR00|T N1.5 + HA|MLET|
|---|---|---|---|---|---|---|
|Task (PnP = Pick-and-Place)|30 demos|100 demos|300 demos|30 demos|100 demos|300 demos|
|Close Double Door|46.0|80.0|90.0|58.0|82.0|82.0|
|Close Drawer|94.0|97.0|96.0|100.0|96.0|100.0|
|Close Single Door<br>|88.0|94.0|98.0<br>|96.0<br>|94.0|96.0|
|Coffee Press Button|88.0|83.0|76.0|66.0|84.0|90.0|
|Coffee Serve Mug|62.0|63.0|58.0|70.0|68.0|76.0|
|Coffee Setup Mug|24.0|29.0|28.0|30.0|28.0|26.0|
|Open Double Door|70.0|76.0|84.0|68.0|86.0|96.0|
|Open Drawer|40.0|71.0|68.0|48.0|74.0|68.0|
|Open Single Door|54.0|69.0|78.0|58.0|82.0|84.0|
|PnP from Cab to Counter|22.0|51.0|50.0|26.0|46.0|54.0|
|PnP from Counter to Cab|36.0|49.0|50.0|46.0|48.0|56.0|
|PnP from Counter to Microwave|26.0|20.0|26.0|20.0|30.0|16.0|
|PnP from Counter to Sink|38.0|60.0|52.0|50.0|56.0|42.0|
|PnP from Counter to Stove|44.0|52.0|68.0|24.0|54.0|64.0|
|PnP from Microwave to Counter|22.0|40.0|44.0|24.0|24.0|24.0|
|PnP from Sink to Counter|60.0|60.0|74.0|54.0|56.0|56.0|
|PnP from Stove to Counter|38.0|70.0|66.0|56.0|74.0|76.0|
|Turn Off Microwave|62.0|96.0|96.0|88.0|98.0|100.0|
|Turn Off Sink Faucet|68.0|84.0|84.0|76.0|88.0|90.0|
|Turn Off Stove|12.0|18.0|30.0|12.0|20.0|28.0|
|Turn On Microwave|42.0|44.0|48.0|50.0|60.0|72.0|
|Turn On Sink Faucet|46.0|83.0|70.0|66.0|76.0|86.0|
|Turn On Stove|30.0|57.0|42.0|26.0|68.0|40.0|
|Turn Sink Spout|34.0|56.0|62.0|48.0|78.0|72.0|
|Pick-and-Place|35.8|50.3|53.8|37.5|48.5|48.5|
|Open-or-Close|65.3|81.2|85.7|71.3|85.7|87.7|
|Others|46.8|61.3|59.4|53.2|66.8|68.0|
|**Average**|**47.8**|**62.6**|**64.1**|**52.5**|**65.4**|**66.4**|


> **892** Table 10: **Positive and negative pair construction for different TCL initialization methods.** We 

> **893** report the positive and negative pair constructions used by SimCLR, single-view TCN, multi-view **894** TCN, and our TCL initialization. **895 896** Method Positive pair Negative pair **897** SimCLR Same view with classical image augmentations In-batch samples **898** Single-view TCN Same view at a nearby timestep Same view at a far timestep **899** Multi-view TCN Different view at the same timestep Same view at a far timestep **900** TCL Same view with classical image augmentations Same view at a far timestep **901 902 903 Time-Contrastive Learning (TCL).** To understand the impact of individual parameters in TCL, we **904** conduct an ablation study on different ways of constructing positive and negative pairs: (i) random **905** initialization, (ii) SimCLR (Chen et al., 2020), (iii) single-view TCN (Sermanet et al., 2018), (iv) **906** multi-view TCN (Sermanet et al., 2018), and (v) our TCL (default). Each method constructs positive **907** and negative pairs from observation images, as summarized in Table 10. Table 11 shows that our **908** TCL initialization achieves the highest average success rate among all methods, highlighting its effectiveness as a core component. **909 910** We further provide a more extensive analysis examining whether TCL influences final performance **911** across datasets. As shown in Table 12, TCL consistently yields improvements across all datasets **912** and even provides substantial gains in low-data scenarios ( _i_ . _e_ ., up to +2.7% in RoboCasa 30 demos). **913** These results highlight that TCL initialization plays a crucial role in enabling the moment tokens to **914** effectively extract compact state features, especially when combined with other core components such as the memory module. **915 916 More longer horizon scenarios.** To validate the effectiveness of HAMLET in more complex **917** scenarios, we further evaluate it on a longer-horizon task, _Pick-and-Place Three Times_ , which requires the model to return to the ready position after performing three consecutive pick-and-place operations. 

17 

Under review as a conference paper at ICLR 2026 

**935 936 937 938 939 940 941** 

> **918** Table 11: **Analysis on different TCL initialization methods.** We compare different TCL initial- 

> **919** ization by constructing positive and negative pairs. Our TCL method achieves the highest average **920** success rate among all methods, demonstrating its effectiveness as a core component. **921 922** RoboCasa Kitchen LIBERO **923** Method 100 demo Spatial Object Goal Long Avg. **924** Random initialization 64.8 **99.4** 99.8 98.0 87.8 96.2 **925** SimCLR 63.8 **99.4** 98.6 97.0 87.2 95.5 **926** Single-view TCN 64.8 98.6 99.4 98.2 91.6 96.9 **927** Multi-view TCN 64.9 99.0 99.0 97.8 90.2 96.5 **928** **<mark>TCL (Ours) 65.4</mark>** <mark>99.0</mark> **<mark>100.0 99.2 92.2 97.7</mark> 929** 

> **930** Table 12: **Effect of TCL.** We analyze the effect of TCL on RoboCasa Kitchen and LIBERO. For **931** RoboCasa Kitchen, we report the average success rate (%) across 24 tasks with models trained using 

> **932** 30, 100, or 300 demonstrations per task. For LIBERO, each metric is the average success rate (%) **933** across 10 tasks per suite, with training performed jointly on all suites. **Bold** indicates the best. **934** 

|Moment||Memory|Robo|Casa Ki|tchen||LI|BERO|||
|---|---|---|---|---|---|---|---|---|---|---|
|Token|TCL|Module|30|100|300|Spatial|Object|Goal|Long|Avg.|
|✗|✗|✗|47.8|62.6|64.1|98.1|99.4|97.2|87.8|95.6|
|✓|✗|✓|49.8|64.8|65.1|**99.4**|99.8|98.0|87.8|96.2|
|✓|✓|✓|**52.5**|**65.4**|**66.4**|99.0|**100.0**|**99.2**|**92.2**|**97.7**|


**942** In particular, the policy needs to track how many successful pick-and-place operations have already **943** been completed, requiring it to memorize more than 14 inference steps, whereas our method explicitly **944** retains only 4 steps by default. As shown in Table 13, HAMLET achieves a significant improvement **945** over the baseline on this long-horizon task, despite the required temporal dependency exceeding the **946** original window size. This is possibly due to the causal nature of Transformers (Vaswani et al., 2017): **947** the key–value pair of each token participates in the self-attention computation for all later tokens, **948** influencing their hidden states and the corresponding key–value entries. Consequently, even after a **949** past KV-cache entry is dropped, its information has already been integrated into the KV-cache of **950** subsequent steps. 

> **951 Results on autoregressive VLAs.** We further validate the generalizability of HAMLET on au- 

> **952** toregressive VLAs. Specifically, we apply it to OpenVLA (Kim et al., 2024) and _π_ 0-FAST, two **953** representative autoregressive VLAs built on action discretization. We evaluate OpenVLA on the **954** LIBERO benchmark, while _π_ 0-FAST is evaluated on the RoboCasa Kitchen benchmark (100 de- **955** mos). As shown in Table 14, HAMLET consistently improves success rates over both baselines: **956** for OpenVLA, achieving a 9.0% gain on LIBERO-Long, and for _π_ 0-FAST, achieving a 5.8% gain **957** on Pick-and-Place (PnP) tasks in RoboCasa. These results highlight that HAMLET effectively transforms pretrained VLAs into history-aware policies without relying on any specific architecture. **958** For implementation, we fine-tune both models using a batch size of 32 for OpenVLA and 64 for **959** _π_ 0-FAST, following their official repositories<sup>78</sup> for other details. **960** 

**961 962** B.2 QUALITATIVE RESULTS **963 964** We provide additional qualitative results to better understand the main components of HAMLET. **965 Time-Contrastive Learning (TCL).** To analyze the effect of Time-Contrastive Learning (TCL) on **966** the moment token, we visualize the self-attention maps on RoboCasa, comparing randomly initialized **967** tokens with TCL-initialized ones. As shown in Figure 8, randomly initialized moment tokens attend **968** to sparsely distributed regions, including background areas that remain static across timesteps. In **969** contrast, TCL-initialized moment tokens focus on more task-relevant regions related to successful **970 971** 7https://huggingface.co/openvla/openvla-7b 

> 8https://github.com/Physical-Intelligence/openpi 

18 

Under review as a conference paper at ICLR 2026 

**972 973 974 975 976 977 978 979 980 981 982 983 984 985 986 987 988 989 990 991 992 993 994 995 996 997 998 999 1000 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 1013 1014 1015 1016 1017 1018 1019 1020 1021 1022 1023 1024 1025** 

Table 13: **More longer horizon scenarios.** We validate HAMLET on the longer-horizon task _Pick-and-Place Three Times_ , which requires tracking three consecutive pick-and-place cycles. We report the success rate (%, over 24 trials per task) and the average number of executed pick-and-place operations. **Bold** indicates the best. 

|Method|Success rate|Executed PnPs|
|---|---|---|
|GR00T N1.5|8.3|1.042|
|**+ HAMLET**|**37.5**|**1.958**|


Table 14: **Results on autoregressive VLAs.** We evaluate HAMLET on two representative autoregressive models: (a) OpenVLA on the LIBERO benchmark, and (b) _π_ 0-FAST on the RoboCasa Kitchen benchmark (100 demos). For LIBERO, we report the average success rate (%) across 10 tasks per suite, with training performed separately on each suite. For RoboCasa Kitchen, we report the average success rates (%) over 24 tasks, which are grouped into three categories: Pick-and-Place (PnP), Open-or-Close (OoC), and Others. **Bold** indicates the best. 

(b) _π_ 0-FAST (Pertsch et al., 2025) 

(a) OpenVLA (Kim et al., 2024) 

|||LIBER|O|||Rob|oCasa K|itchen|
|---|---|---|---|---|---|---|---|---|
|Method|Spatial|Object|Goal|Long|Method|PnP|OoC|Others|
|OpenVLA|84.8|62.6|71.6|48.6|_π_0-FAST|17.0|60.7|46.6|
|**+ HAMLET**|**85.6**|**70.8**|**78.2**|**57.6**|**+ HAMLET**|**22.8**|**63.7**|**52.0**|


execution. For example, we observe that the object to be grasped by the gripper tends to receive higher attention values than other regions. 

**Memory module.** As explored in Figure 4, we further provide examples of how our memory module attends to historical context. Specifically, we visualize the attention maps of the memory module during rollouts in the _Swap Cubes_ task, where the robot swaps the blue cube with the green cube. In the left side of Figure 9, we confirm that the memory network attends to the key past timestep, which is crucial for determining the next action: for example, when deciding which cube to pick next, the memory module highly attends to the past timestep when the blue cube was previously placed down. Interestingly, the attention across past timesteps remains low when historical information is less critical, _e_ . _g_ ., during the initial move of the blue cube, as shown on the right side of Figure 9. 

**Further example rollouts of real-world tasks.** We further illustrate rollouts by HAMLET and GR00T N1.5 for each real-world task in Figure 10, 11, 12. It can be clearly observed that GR00T N1.5 without history-awareness struggles with multi-step dependencies and often fails to recover from occlusions or ambiguous intermediate states, while HAMLET leverages its memory to better recognize the current state and complete tasks. In Figure 13, we further provide typical failure cases of na¨ıve multi-frame baseline on GR00T N1.5, which often proceeds to the next actions while failing to recover from its failure state. This indicates that simply appending multi-frame inputs to VLAs might degrade their generalizability. 

## C DISCUSSION 

**Limitations.** While HAMLET maintains the efficiency of single-frame VLAs through its efficiencyoriented design, it still incurs additional training cost due to initialization with time-contrastive learning. Furthermore, although we demonstrate its applicability to recent diffusion-based VLAs, it may not directly extend to auto-regressive VLAs (Pertsch et al., 2025; Kim et al., 2024). 

**Future directions.** One promising direction is to scale up HAMLET using larger-scale robotic manipulation datasets. As discussed in Table 6, each components of HAMLET, such as the memory module, can transfer effectively to unseen datasets. This suggests that initializing these components on large-scale datasets and then rapidly adapting them further enhance the practicality of our framework. In addition, while we adopted a relatively shallow Transformer for memory module to ensure scalability, a more exhaustive search over architectural parameters or the use of recent hybrid models (Lenz et al., 2025; Nano, 2025) is a straightforward approach for obtaining additional gains. 

19 

Under review as a conference paper at ICLR 2026 

**1026 1027 1028 1029 1030 1031 1032 1033 1034 1035 1036 1037 1038 1039 1040 1041 1042** Figure 8: **1043 1044 1045 1046 1047 1048 1049** Attention **1050 1051 1052 1053 1054 1055 1056 1057 1058 1059 1060 1061 1062 1063 1064** Figure 9: **1065 1066 1067 1068 1069 1070 1071** D **1072 1073 1074 1075** vocabulary. **1076 1077 1078 1079** 


Figure 8: **Qualitative results of the moment tokens.** We analyze the self-attention of moment tokens on RoboCasa input frames, comparing random initialization (w/o TCL) with TCL-initialization (w/ TCL). After TCL-initialization, the moment tokens tend to concentrate more on task-relevant regions, such as the object to be grasped. 


Figure 9: **Qualitative results of the memory module.** We analyze the self-attention of the memory module on the _Swap Cubes_ task, where the robot swaps the blue cube with the green cube. We report two distinctive cases: (left) one where recalling a specific past timestep is necessary for the next action–such as when the blue cube has already been placed down before moving the green cube–and (right) another where recalling is less critical–such as during the initial move of the blue cube. We observe that our memory module clearly attends to the relevant past timestep when required. 

## D THE USE OF LARGE LANGUAGE MODELS 

We acknowledge that large language models (LLMs) were used in the preparation of this manuscript to assist with writing quality. We mainly utilize them to find grammatical errors, suggest alternative vocabulary. All ideas, analyses, and conclusions presented in this paper are solely those of the authors. 

20 

Under review as a conference paper at ICLR 2026 


21 

Under review as a conference paper at ICLR 2026 


Figure 13: **Example rollouts by na¨ıve multi-frame baseline.¨ıve multi-frame baseline.ıve multi-frame baseline.** We observe that the nave multi-frame¨ve multi-frame¨¨ baseline often proceeds without recovery, merely copying action trajectories observed during training. This is possibly due to its poor generalizability, using only consecutive frames throughout training. 

22 

