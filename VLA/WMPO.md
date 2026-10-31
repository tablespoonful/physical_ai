---
title: "WMPO: WORLD MODEL-BASED POLICY OPTIMIZA- TION FOR VISION-LANGUAGE-ACTION MODELS"
venue: "ICLR 2026 Poster"
original: "ICLR 2026 投稿時の匿名版"
url: https://arxiv.org/abs/2511.09515
pdf: https://arxiv.org/pdf/2511.09515
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.09515)** / [論文ページ](https://arxiv.org/abs/2511.09515)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。
> ICLR 2026 投稿時の匿名版から変換しました。リンク先の公開版とは内容が異なる場合があります。

Under review as a conference paper at ICLR 2026 

**000** 

**001** 

**002 003** 

**004** 

**005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 020 021 022 023 024 025 026** 

# WMPO: WORLD MODEL-BASED POLICY OPTIMIZATION FOR VISION-LANGUAGE-ACTION MODELS 

### **Anonymous authors** 

Paper under double-blind review 

## ABSTRACT 

Vision-Language-Action (VLA) models have shown strong potential for generalpurpose robotic manipulation, but their reliance on expert demonstrations limits their ability to learn from failures and perform self-corrections. Reinforcement learning (RL) addresses these through self-improving interactions with the physical environment, but suffers from high sample complexity on real robots. We introduce _World-Model-based Policy Optimization (WMPO)_ , a principled framework for on-policy VLA RL without interacting with the real environment. In contrast to widely used latent world models, WMPO focuses on pixel-based predictions that align the _“imagined”_ trajectories with the VLA features pretrained with web-scale images. Crucially, WMPO enables the policy to perform on-policy GRPO that provides stronger performance than the often-used off-policy methods. Extensive experiments in both simulation and real-robot settings demonstrate that WMPO (i) substantially improves sample efficiency, (ii) achieves stronger overall performance, (iii) exhibits emergent behaviors such as self-correction, and (iv) demonstrates robust generalization and lifelong learning capabilities. 

**027** 

## 1 INTRODUCTION 

**028** 

**029** Vision-Language-Action (VLA) models (Brohan et al., 2023; Kim et al., 2024; Intelligence et al., **030** 2025) have emerged as a promising paradigm for general-purpose robotic manipulation, enabling **031** robots to follow natural language instructions in complex, unstructured environments. The dominant **032** approach for training these models is imitation learning (IL) from large-scale human demonstra- **033** tions (Lin et al., 2024). While effective in mimicking demonstrated behaviors, IL-trained policies are often brittle. When encountering out-of-distribution states not seen during training, they can take **034** suboptimal actions that lead to compounding errors (Ross et al., 2011), making task completion or **035** recovery nearly impossible (Fig. 1a). **036 037** Reinforcement learning (RL) (Li et al., 2025b) offers a natural solution to this brittleness by allowing **038** an agent to learn and improve through active interaction with its environment. This self-improvement **039** process can lead to policies that are more robust and capable of recovering from failure. However, applying RL directly to real robots is notoriously sample-inefficient, requiring millions of interactions **040** that are impractical, unsafe, and time-consuming to collect (Fig.1b). Recent efforts to improve sample **041** efficiency fall into two main strategies. The first leverages human intervention to guide learning (Luo **042** et al., 2024b; Chen et al., 2025; Xia et al., 2025), which reduces exploration cost but is labor-intensive **043** and hard to scale. The second relies on simulation to reduce real-world interactions (Lu et al., 2025; **044** Li et al., 2025a), but is limited by the difficulty of building accurate simulators for diverse scenarios. **045** The advent of large-scale generative models, particularly video-generative world models (NVIDIA **046** et al., 2025; Ball et al., 2025), presents a compelling new frontier for leveraging model-based RL (Finn **047** & Levine, 2017) to mitigate the sample inefficiency challenge in VLA RL. These models can learn **048** the dynamics of the world from data and simulate future transitions, offering a path to scalable RL **049** without costly real-world explorations. Nevertheless, integrating these models with existing VLAs **050** remains a challenge. Many classical model-based RL approaches (Hafner et al., 2019; 2020a;b; **051** 2023; Ma et al., 2022; Frauenknecht et al., 2025) operate in an abstract latent space, which creates **052** a fundamental mismatch with powerful VLA foundation models that are pretrained on real-world **053** images. The rich, pretrained visual understanding of VLAs cannot be directly applied within a mismatched latent dynamics model. We argue that leveraging a pixel-space video-generative world 

1 

Under review as a conference paper at ICLR 2026 

**054 Learn From Failures 055 Self-correction** **<mark>Robotic</mark> Sample Efficiency** **<mark>Trajectories</mark> World Model 056 On-policy RL Human Operation** **<mark>Human</mark> 057** **<mark>Demonstration Real World</mark> 058** **<mark>Policy Behavior</mark> 059 Imitation Learning Reward Action** **<mark>Data</mark> Reward Action 060 Learn From Failures 061 Learn From Failures Self-correction Sample Efficiency 062 Self-correction VLA VLA On-policy RL VLA 063 (a) Imitation Learning (b) Real World RL (c) WMPO 064 065** Figure 1: Three different VLA training paradigms: (a) Imitation learning learns from human **066** demonstrations but lacks the ability for learning from failures and self-correction; (b) Real-world **067** RL improves policy through direct interaction but suffers from high sampling costs and difficulty in achieving on-policy RL; (c) WMPO pretrains a world model on large-scale robotic trajectories **068** and fine-tunes it with limited policy behavior data, enabling sample-efficient on-policy RL for VLA **069** without real-world interaction. **070 071** model is crucial, as it allows the VLA policy to operate on generated visual data that is consistent **072** with its pretraining, effectively bridging the world model with the policy’s pre-trained knowledge. **073** To this end, we propose World Model-based Policy Optimization (WMPO), as illustrated in Fig. 1c, a **074** principled framework that grounds VLA RL entirely in an action-conditioned video world model. **075** By pretraining a high-fidelity, pixel-space video-generative model on millions of robotic trajecto- **076** ries(Collaboration, 2023), WMPO leverages realistic visual dynamics to create a scalable training **077** environment for downstream tasks. **078** WMPO incorporates several key innovations. First, to mitigate the state-distribution mismatch **079** between expert demonstrations and policy rollouts, we introduce policy behavior alignment, finetuning **080** the world model with behavioral data collected by the policy itself. Second, short-horizon prediction **081** makes it difficult to define accurate rewards and is prone to reward hacking. To address this, WMPO **082** generates complete trials through clip-level autoregressive video generation, enabling more reliable **083** outcome-based reward assignment. While this design supports long-horizon rollouts, it also introduces **084** challenges such as visual distortion and action–frame misalignment. WMPO addresses these with **085** noisy-frame conditioning and frame-level action control, ensuring robustness and accurate trajectory **086** simulation. Third, we train a lightweight reward model that predicts task success or failure, providing **087** a learned sparse reward signal and avoiding both complex reward shaping and reward hacking. **088** Together, these components form a self-contained environment that enables on-policy RL entirely “in **089** imagination”. Specifically, we adopt Group Relative Policy Optimization (GRPO) (Shao et al., 2024), whose robustness and scalability have been demonstrated in DeepSeek-AI et al. (2025). Notably, **090** WMPO naturally supports repeated rollouts from the same initial state, which is difficult to realize in **091** the physical world but crucial for large-scale GRPO training. **092 093** We conduct extensive experiments in both Mimicgen simulation environments (Mandlekar et al., **094** 2023) and real-world environments to validate the effectiveness of WMPO. Our results show that **095** WMPO achieves substantially higher sample efficiency and consistently outperforms VLA RL methods that directly optimize with real trajectories. Crucially, we provide qualitative evidence of **096** emergent behaviors, where the WMPO-trained policy demonstrates self-correction strategies not **097** present in the demonstration data and often completes tasks faster and more smoothly, without **098** noticeable stalls. We further demonstrate WMPO’s strong generalization compared to offline RL **099** methods, as well as its capacity for lifelong learning through alternating updates between the VLA **100** policy and the world model. Taken together, these findings highlight WMPO as a scalable and **101** generalizable paradigm for advancing VLA RL. **102 103 104** 2 RELATED WORKS **105 106 Vision-Language-Action Models.** Vision-Language-Action (VLA) models aim to map visual **107** inputs and natural language instructions into executable robotic actions, enabling general-purpose manipulation. Most VLAs build upon pretrained vision-language models (VLMs) and are further fine- 

To this end, we propose World Model-based Policy Optimization (WMPO), as illustrated in Fig. 1c, a principled framework that grounds VLA RL entirely in an action-conditioned video world model. By pretraining a high-fidelity, pixel-space video-generative model on millions of robotic trajectories(Collaboration, 2023), WMPO leverages realistic visual dynamics to create a scalable training environment for downstream tasks. 

2 

Under review as a conference paper at ICLR 2026 

**108** tuned on robotic trajectories, thereby inheriting strong visual grounding and language understanding. **109** This progress has been driven both by large-scale demonstration collections (Collaboration, 2023) **110** and by advances in action parameterization, including discrete next-token prediction (Kim et al., **111** 2024), parallel decoding (Kim et al., 2025), and continuous flow-based heads (Black et al., 2024). **112** Despite these advances in data and model design, existing VLAs largely remain within the imitation **113** learning (IL) paradigm, making them brittle when encountering out-of-distribution states and unable **114** to leverage failed executions for improvement (Ross et al., 2011). **115 116 Reinforcement Learning for VLA Models.** RL provides a natural complement to IL by enabling **117** policies to learn from interaction, thereby improving robustness and recovery capabilities. However, **118** applying on-policy RL to VLA remains challenging due to severe sample inefficiency and substantial **119** system-level complexity. Prior works can be broadly divided into two strategies. The first introduces **120** human intervention to guide exploration, e.g., supplying corrective signals when policies encounter **121** unrecoverable states (Luo et al., 2024a; Chen et al., 2025; Xia et al., 2025). While effective at **122** reducing exploration cost, this approach requires continuous human supervision, making it labor- **123** intensive and difficult to scale. The second attempts to perform RL directly in simulation or in the real world. For instance, Zhang et al. (2024) adopt trajectory-level DPO (Rafailov et al., 2023), while **124** others apply PPO (Schulman et al., 2017) or GRPO (Shao et al., 2024) to optimize VLA policies in **125** simulation (Lu et al., 2025; Li et al., 2025a). These approaches avoid human supervision but still **126** suffer from poor sample efficiency, and constructing accurate simulators for each real-world scenario **127** introduces prohibitive engineering overhead. In contrast, WMPO enables policy optimization entirely **128** within a learned world model, substantially improving sample efficiency and scalability. **129 130 World Models.** World models aim to mitigate the need for costly real-world interactions by **131** learning generative dynamics and enabling policies to learn from “imagine” trajectories. Early **132** approaches (Hafner et al., 2020a;b; 2023) learned world model in the latent space of recurrent **133** state-space models, which provided efficient but overly abstract rollouts. More recent work intro- **134** duced diffusion-based world models, showing that retaining pixel-level fidelity is crucial for RL **135** with Gaussian policies (Alonso et al., 2024; Jiang et al., 2025). Building on this trend, large-scale **136** video world models (NVIDIA et al., 2025; Ball et al., 2025) have demonstrated impressive gen- **137** erality across diverse domains. However, when applied to robotics, they suffer from distribution **138** mismatch—struggling to faithfully reproduce policy rollouts and fine-grained robot–object interac- **139** tions. In contrast, WMPO addresses these challenges through policy behavior alignment and, for the **140** first time, verifies the feasibility of leveraging high-fidelity world models for scalable VLA RL. **141 142** 3 WORLD MODEL-BASED POLICY OPTIMIZATION **143 144 145** We introduce World Model-based Policy Optimization (WMPO), a novel framework for learning complex, vision-based robotic manipulation policies. The WMPO framework is grounded in the **146** principles of model-based RL, where policy optimization is performed entirely within a learned world **147** model, thereby eliminating the need for costly real-world interactions. WMPO operates directly **148** in the pixel space, instead of latent space, which better bridges the pretrained VLA features from **149** web-scale video-action pairs with the “imagined” trajectories. Specifically, the world model is trained **150** to accurately reflect the policy’s behavior through a process we call Policy Behavior Alignment, **151** where it is fine-tuned on a small set of real trajectories collected from the policy itself. This ensures **152** the model can faithfully simulate diverse scenarios, including failures. We also introduce noisy frame **153** conditioning and frame-level action control techniques to overcome the problems of visual distortion **154** and action-frame misalignment in long-horizon video prediction. With these modifications, we are **155** able to perform strong on-policy Group Relative Policy Optimization (GRPO) using trajectories **156** imagined by the learned world model, which significantly enhances sample efficiency compared to direct RL methods. Fig. 2 illustrates an overview of the training procedure of WMPO. **157 158 159** 3.1 PROBLEM FORMULATION **160 161** We formulate the VLA manipulation task as a decision-making problem in the form of an MDP _M_ = ( _S, A, P, R_ ). 

tuned on robotic trajectories, thereby inheriting strong visual grounding and language understanding. This progress has been driven both by large-scale demonstration collections (Collaboration, 2023) and by advances in action parameterization, including discrete next-token prediction (Kim et al., 2024), parallel decoding (Kim et al., 2025), and continuous flow-based heads (Black et al., 2024). Despite these advances in data and model design, existing VLAs largely remain within the imitation learning (IL) paradigm, making them brittle when encountering out-of-distribution states and unable to leverage failed executions for improvement (Ross et al., 2011). 

**Reinforcement Learning for VLA Models.** RL provides a natural complement to IL by enabling policies to learn from interaction, thereby improving robustness and recovery capabilities. However, applying on-policy RL to VLA remains challenging due to severe sample inefficiency and substantial system-level complexity. Prior works can be broadly divided into two strategies. The first introduces human intervention to guide exploration, e.g., supplying corrective signals when policies encounter unrecoverable states (Luo et al., 2024a; Chen et al., 2025; Xia et al., 2025). While effective at reducing exploration cost, this approach requires continuous human supervision, making it laborintensive and difficult to scale. The second attempts to perform RL directly in simulation or in the real world. For instance, Zhang et al. (2024) adopt trajectory-level DPO (Rafailov et al., 2023), while others apply PPO (Schulman et al., 2017) or GRPO (Shao et al., 2024) to optimize VLA policies in simulation (Lu et al., 2025; Li et al., 2025a). These approaches avoid human supervision but still suffer from poor sample efficiency, and constructing accurate simulators for each real-world scenario introduces prohibitive engineering overhead. In contrast, WMPO enables policy optimization entirely within a learned world model, substantially improving sample efficiency and scalability. 

**World Models.** World models aim to mitigate the need for costly real-world interactions by learning generative dynamics and enabling policies to learn from “imagine” trajectories. Early approaches (Hafner et al., 2020a;b; 2023) learned world model in the latent space of recurrent state-space models, which provided efficient but overly abstract rollouts. More recent work introduced diffusion-based world models, showing that retaining pixel-level fidelity is crucial for RL with Gaussian policies (Alonso et al., 2024; Jiang et al., 2025). Building on this trend, large-scale video world models (NVIDIA et al., 2025; Ball et al., 2025) have demonstrated impressive generality across diverse domains. However, when applied to robotics, they suffer from distribution mismatch—struggling to faithfully reproduce policy rollouts and fine-grained robot–object interactions. In contrast, WMPO addresses these challenges through policy behavior alignment and, for the first time, verifies the feasibility of leveraging high-fidelity world models for scalable VLA RL. 

3 

Under review as a conference paper at ICLR 2026 

**162 1. Imagined Trajectory Generation** _<u>Insert the square</u>_ Update max 𝒥 𝜃 by Policy Model **163164** _<u>into the stick</u>_ Policy Model 𝜋𝜃𝑜𝑙𝑑 Update 𝜃 መ𝐴𝑖 & 𝑟𝑖,𝑡 𝜃=𝜃 𝜋𝜋𝜃𝑜𝑙𝑑𝜃 𝑎𝑎𝑖,𝑡𝑖,𝑡𝑠𝑖,𝑡𝑠𝑖,𝑡 <mark>𝜋</mark> 𝜃 Buffer (b) sample (a) ℬ **165** 𝑎𝑐𝑡𝑖𝑜𝑛 𝑐ℎ𝑢𝑛𝑘 𝑠𝑡𝑎𝑡𝑒 **3. Policy Update 166167168** Language Instruction 𝑎𝑐𝑡𝑖𝑜𝑛 chunk **World Model** 𝑎𝑡 𝑠𝑡𝑎𝑡𝑒𝑠𝑡 𝑔 Initial State 𝑝𝜙 (e) update 𝑠0 s 𝑎𝑡 (d) update 𝑠𝑡𝑎𝑡𝑒𝑠𝑠𝑡+1𝑡 … **2. Trajectory Sampling** TrajectoryTrajectory 𝜏𝜏1𝑖 ... <mark>𝑅</mark> 1 ... መ𝐴1 **169** 𝑅𝑖 𝐴መ𝑖 **170** future frames(c) generate … Trajectory <mark>𝜏</mark> 𝐺 𝑠𝑡𝑖, 𝑎𝑡𝑖 ... ... **171** <mark>𝑅</mark> 𝐺 𝐴መ𝐺 **172 173** Figure 2: WMPO starts from an initial state _s_ 0.. The overall training procedure consists of three **174** components: (1) _Imagined Trajectory Generation_ , where policy model _πθθ_ old and world model _pϕϕ_ **175** interact alternately to generate a full imagined trajectory; (2) _Trajectory Sampling_ , where multiple **176** trajectories are sampled and evaluated by the reward model _Rψψ_ ; and (3) _Policy Update_ , where the **177** policy parameters _θ_ are optimized via Eq. 4. This process is iteratively repeated throughout training. **178** • **State space.** _S_ = _I × G_ , where _I_ denotes the image observation space, i.e., image sequences **179** _I_ 0: _K_ , and _G_ denotes the language instruction space. Here, we make the assumption that robot states **180** can be solely defined by their image observations. For more complicated setups, e.g., Partially **181** Observable MDPs (POMDPs) (Igl et al., 2018; Ma et al., 2021), we leave them for future studies. **182 183** • **Action space.** _A_ denotes the space of action chunks, i.e., sequences of robot actions. Each action in an action chunk of length _K_ , _att ∈_ R<sup>_K×D×DD_</sup> , represents a _D_ -DoF (degree of freedom) control **184** vector. For policy optimization, each dimension is discretized into 256 bins. Specifically, we learn **185** to sample action chunks using a parameterized VLA policy, _a ∼ ∼ πθθ_ ( _a | s | s s_ ).. **186 187** • **Transition function.** _P_ : _S × A →S_ is realized by a parameterized world model _stt_ +1 _∼_ **188** _pϕϕ_ ( _stt_ +1 _| st, at st, att, at, att_ ), which generates future observations conditioned on past observations and actions., which generates future observations conditioned on past observations and actions. **189** In particular, we sample _imagined trajectories τ τ_ = _{ss_ 0 _,_ ˆ _s_ 1 _, . . . ,_ ˆ _sT }T } }_ by iteraively sampling from **190** the world model _s_ ˆ _t_ +1 _∼ pϕϕ_ ( _stt_ +1 _| s_ ˆ _t, at, att_ ) and the VLA policy and the VLA policy _att ∼ pθθ_ ( _att | stt_ ), given an initial, given an initial state _s_ 0 sampled in the real environment. sampled in the real environment. **191 192** • **Reward function.** The reward is given by a learned model _Rψ_ that determines task success from **193** the full trajectory, assigning a binary outcome _Rψ_ ( _τ_ ) _∈{_ 0 _,_ 1 _}_ . **194 195** Our objective is to train a policy _πθθ_ ( _a | s | s s_ ) such that the predicted cumulative return of the imagined such that the predicted cumulative return of the imagined trajectories will be maximized **196 197** max _θ_ E _τ ∼πθ,pϕπθ,pϕθ,pϕ,pϕϕ_ [ _Rψψ_ ( _τ_ )] _._ (1) **198 199** This formulation highlights a general paradigm: RL for VLA can be decoupled from real-world **200** interactions by leveraging a generative world model as the imaginary training ground. **201 202** 3.2 GENERATIVE WORLD MODEL **203 204 Imagined Trajectory Generation.** Given _c_ initial frames _I_ 0: _c_ , the policy _πθθ_ takes the most recent _m_ **205** frames and language instruction _g_ as input and predicts an action chunk<sup>1</sup> , i.e., _aii_ : _i_ + _K ∼ πθθ_ ( _Ii−mi−m−mm_ : _i, g, g_ ). **206** The world model _pϕϕ_ then conditions on the last _c_ observed frames and the predicted action chunk to **207** generate the next _K_ frames: **208** _Iii_ : _i_ + _K ∼ pϕϕ_ ( _Ii−ci−c−cc_ : _i, ai, aii_ : _i_ + _K_ ) _._ (2) **209** Repeating this process until a maximum length _N_ yields a trajectory _τ_ = _{II_ 0: _N , a_ 0: _N }_ . A reward **210** model _Rψψ_ evaluates the frames in _τ_ and outputs a binary label _y_ = _Rψψ_ ( _I_ 0: _N_ ) _∈{_ 0 _,_ 1 _}_ . Thus, each **211** imagined trajectory in the world model is represented as a labeled pair ( ( _τ, y_ ), which is then used for, which is then used for **212** policy optimization. **213 214** 1To avoid confusion in subscripts, we specify that _i_ is used as the frame-level subscript and _t_ as the state-level **215** subscript, where a state often includes multiple frames. _N_ and _T_ denote the maximum length of an imagined trajectory at the frame level and state level, respectively. 

Figure 2: WMPO starts from an initial state _s_ 0.. The overall training procedure consists of three components: (1) _Imagined Trajectory Generation_ , where policy model _πθθ_ old and world model _pϕϕ_ interact alternately to generate a full imagined trajectory; (2) _Trajectory Sampling_ , where multiple trajectories are sampled and evaluated by the reward model _Rψψ_ ; and (3) _Policy Update_ , where the policy parameters _θ_ are optimized via Eq. 4. This process is iteratively repeated throughout training. 

- **State space.** _S_ = _I × G_ , where _I_ denotes the image observation space, i.e., image sequences _I_ 0: _K_ , and _G_ denotes the language instruction space. Here, we make the assumption that robot states can be solely defined by their image observations. For more complicated setups, e.g., Partially Observable MDPs (POMDPs) (Igl et al., 2018; Ma et al., 2021), we leave them for future studies. 

- **Action space.** _A_ denotes the space of action chunks, i.e., sequences of robot actions. Each action in an action chunk of length _K_ , _att ∈_ R<sup>_K×D×DD_</sup> , represents a _D_ -DoF (degree of freedom) control vector. For policy optimization, each dimension is discretized into 256 bins. Specifically, we learn to sample action chunks using a parameterized VLA policy, _a ∼ ∼ πθθ_ ( _a | s | s s_ ).. 

- **Transition function.** _P_ : _S × A →S_ is realized by a parameterized world model _stt_ +1 _∼ pϕϕ_ ( _stt_ +1 _| st, at st, att, at, att_ ), which generates future observations conditioned on past observations and actions., which generates future observations conditioned on past observations and actions. In particular, we sample _imagined trajectories τ τ_ = _{ss_ 0 _,_ ˆ _s_ 1 _, . . . ,_ ˆ _sT }T } }_ by iteraively sampling from the world model _s_ ˆ _t_ +1 _∼ pϕϕ_ ( _stt_ +1 _| s_ ˆ _t, at, att_ ) and the VLA policy and the VLA policy _att ∼ pθθ_ ( _att | stt_ ), given an initial, given an initial state _s_ 0 sampled in the real environment. sampled in the real environment. 

Our objective is to train a policy _πθθ_ ( _a | s | s s_ ) such that the predicted cumulative return of the imagined such that the predicted cumulative return of the imagined trajectories will be maximized 


This formulation highlights a general paradigm: RL for VLA can be decoupled from real-world interactions by leveraging a generative world model as the imaginary training ground. 

**Imagined Trajectory Generation.** Given _c_ initial frames _I_ 0: _c_ , the policy _πθθ_ takes the most recent _m_ frames and language instruction _g_ as input and predicts an action chunk<sup>1</sup> , i.e., _aii_ : _i_ + _K ∼ πθθ_ ( _Ii−mi−m−mm_ : _i, g, g_ ). The world model _pϕϕ_ then conditions on the last _c_ observed frames and the predicted action chunk to generate the next _K_ frames: 


Repeating this process until a maximum length _N_ yields a trajectory _τ_ = _{II_ 0: _N , a_ 0: _N }_ . A reward model _Rψψ_ evaluates the frames in _τ_ and outputs a binary label _y_ = _Rψψ_ ( _I_ 0: _N_ ) _∈{_ 0 _,_ 1 _}_ . Thus, each imagined trajectory in the world model is represented as a labeled pair ( ( _τ, y_ ), which is then used for, which is then used for policy optimization. 

4 

Under review as a conference paper at ICLR 2026 

**216** 

**Model Architecture.** Our world model is based on a video diffusion backbone inherited from **217** OpenSora (Zheng et al., 2024), with modifications designed for simulating robot–object interactions. **218** Specifically, we replace the 3D VAE in OpenSora with the 2D VAE from SDXL (Podell et al., **219** 2024), which better preserves fine-grained motion details and avoids temporal distortions caused **220** by excessive compression. Consequently, the diffusion process operates in the VAE’s latent space. **221** When applying the imagined trajectory to VLA optimization, we decode the images back into pixel **222** space to better leverage the pretrained knowledge, rather than retraining the VLA in a new latent **223** space such as that from RSSM (Hafner et al., 2023). 

**224** 

> **224** Since our world model generates full trajectories in an autoregressive manner—using previously 

> **225** generated frames as conditioning for future predictions—errors can accumulate, leading to severe 

> **226** degradation over long horizons, ultimately leading to failed prediction. To mitigate this issue, we **227** introduce a noisy-frame conditioning technique: during training, conditional frames _Ii−m_ : _i_ are **228** perturbed with diffusion noise at 50/1000 steps rather than kept clean, which improves robustness **229** to imperfect conditioning. As a result, the world model achieves stable long-horizon generation, **230** producing trajectories of hundreds of frames without noticeable quality loss. 

**231** 

> **231** To enable precise action conditioning, inspired by Zhu et al. (2025), we incorporate a frame-level **232** action control mechanism for better action-frame alignment. Specifically, we extend the AdaLN (Xu **233** et al., 2019) block to inject both action signals and diffusion timestep embeddings at the frame **234** level. For each action _ai_ , an MLP generates modulation coefficients: scale _γ_ 1<sup>_i_and shift</sup><sup>_β_</sup> 1<sup>_i_for the</sup> **235** LayerNorm output, and scale _α_ 1<sup>_i_for the residual connection of either the MHA or FFN block.Let</sup><sup>**x**</sup><sup>_i_</sup> **236** denote the feature representation at frame _i_ ; the update rule within each transformer block is given as: **237 x**<sup>_i_</sup> = **x**<sup>_i_</sup> + (1 + _α_ 1<sup>_i_)</sup><sup>_·_Block</sup> _γ_ 1<sup>_i·_LayerNorm(</sup><sup>**x**</sup><sup>_i_) +</sup><sup>_β_</sup> 1<sup>_i_</sup> . � � 

**237 238** 

**239** 

**Policy Behavior Alignment.** We pretrain the world model on Open X-Embodiment (OXE) Collab- **240** oration (2023) trajectories, which offer diverse demonstrations of robot interactions and endow the **241** model with broad knowledge of physical dynamics. However, because OXE trajectories primarily **242** consist of successful executions, failure scenarios are underrepresented in the observation distribution. **243** Likewise, training only on expert demonstrations from downstream tasks leaves the model unable to **244** simulate failures, making the imagined trajectories unsuitable for training. To address this mismatch, **245** we fine-tune the world model on real rollout trajectories collected from the policy itself, thereby **246** adapting it to the downstream (state _,_ action) distribution and capturing failure modes more faithfully. **247** Without this adaptation, the model’s imagination of failure cases remains brittle and unfaithful. **248** 

**249 250** 

### 3.3 REWARD MODEL 

**251** A key requirement for scalable policy optimization in the world model is automatically judging **252** whether an imagined trajectory indicates task success. We construct a lightweight reward model **253** trained on real trajectories. Given a trajectory _τ_ = _{I_ 0: _N }_ , we define a clip of length _L_ as _ci_ = _Ii−L_ : _i_ . **254** The terminal clip _cN_ of a successful trajectory serves as a positive sample, whereas negatives are **255** drawn from _{ci_ : _L ≤ i ≤ N − L}_ of successful trajectories and from arbitrary clips of failed trajectories. To address class imbalance, we balance the number of positive and negative samples **256** within each training batch. The reward model, implemented as a VideoMAE (Tong et al., 2022) **257** encoder with a linear head, is trained with binary cross-entropy loss. At inference, the model applies **258** a sliding window with stride _s_ over _τ_ to compute the success probability of each clip. A trajectory **259** is classified as successful if any clip exceeds a threshold _τ_ thr, which is selected via validation **260** experiments. 

**261** 

**262** 

### 3.4 ON-POLICY REINFORCEMENT LEARNING WITH WMPO 

**263** 

**264** 

**264** Reinforcement learning in VLA tasks faces two key bottlenecks. (1) Physical interaction bottleneck. **265** Unlike LLM settings where feedback is cheap, VLA tasks require repeated rollouts in the physical **266** world, which incur high hardware costs, safety concerns, and limited scalability. (2) Value estimation **267** bias by off-policy RL. Given the aforementioned physical constraints, existing real-world RL methods **268** often consider off-policy RL methods (James et al., 2022; Seo et al., 2024; Wagenmaker et al., 2025; **269** Chen et al., 2025). However, off-policy methods naturally cause value estimation errors (Park et al., 2025) and on-policy methods are often favorable for better performance. 

5 

Under review as a conference paper at ICLR 2026 

**270** To overcome these challenges, we optimize policies entirely within a world model: replacing costly **271** real-world rollouts with model-generated trajectories alleviates reliance on physical interaction and **272** enables scalable online learning. We adopt Group Relative Policy Optimization (GRPO) as the policy **273** optimization algorithm, since it provides stable and scalable training in settings with sparse rewards. **274** In our case, state transitions are simulated by the world model (Eq. 2), and rewards are binary with **275** _Rψψ_ ( _τ_ ) _∈{_ 0 _,_ 1 _}_ depending on task success. **276 277 Trajectory Sampling.** From each initial frames _I_ 0: _c_ sample from real environment _D_ , we sample a **278** group of imagined trajectories _{ττ_ 1 _, . . . , τG}G}}_ from current policy _πθθ_ old inside the world model. The **279** reward model is then employed to predict the success or failure of each trajectory. To mitigate **280** vanishing gradients, we adopt a _Dynamic Sampling_ strategy (Yu et al., 2025): if all trajectories in a **281** group are predicted to be successful or all unsuccessful, the group is discarded and additional rollouts are sampled until the batch is fully populated. The log-probability of each action chunk under _πθθ_ old is **282** pre-computed as reference: **283 284** _K D_ **285** log _πθθ_ old(( _att | st stt_ ) = � � log _πθθ_ old � _a_<sup>_i,j_</sup> _t | st stt_ � _,_ (3) **286** _i_ =1 _j_ =1 **287** where _at_ denotes the action chunk at time _t_ , and _a_<sup>_i,j_</sup> _t_ represents the _i_ -th action in the _j_ -th DoF. **288 289 Policy Update.** Following DAPO (Yu et al., 2025), we remove the KL divergence regularization **290** so that no reference model is required during training, thereby reducing memory consumption and **291** encouraging the policy to explore novel behaviors. The final training objective is given by **292** _G T_ **293** 1 1 **294** _J_ ( _θ_ ) = E E _s_ 0 _∼D,{τi}Gi,{τi}Gi{τi}Giτi}Gii}Gi}GiGii_ =1<sup>_∼πθπθθ_</sup> old _G_ � _T_ � min�� _ri,ti,t_ ( _θ_ ) _A_<sup>ˆ</sup> _i,,_ clip( _ri,ti,t_ ( _θ_ ) _,_ 1 _− ϵ_ low _,_ 1 + _ϵ_ high) ) _A_<sup>ˆ</sup> _i ,_ � _i_ =1 _t_ =0 �<sup>�</sup> **295** (4) **296** with **297** _<u>i</u>_ =11<sup><u>)</u></sup> _ri,ti,t_ ( _θ_ ) =<sup>_πθθ_</sup><sup><u>(</u></sup><sup>_ai,ti,t,tt_</sup><sup>_<u>| si,t si,ti,t,tt</u>_</sup><sup><u>)</u></sup> _A_ ˆ _i_ =<sup>_Ri −i − −_mean((</sup><sup>_<u>{Ri}GRi}Gi}G}GG</u>_</sup> _._ (5) **298** _πθθ_ old(( _ai,ti,t | si,t si,ti,t_ )<sup>_,_</sup> std( _{Ri}Ri}i}}_<sup>_G_</sup> _i_ =1<sup>)</sup> **299 300** Here _ri,ti,t_ ( _θ_ ) is the probability ratio between new and old policies at step is the probability ratio between new and old policies at step _t_ of trajectory _τii_ , _Rii_ = _R_ ( _τii_ ), **301** and _A_<sup>ˆ</sup> _i_ is the normalized advantage of trajectory _τii_ over the horizon _N_ . The overall training pipeline **302** is detailed in Algorithm 1 in Appendix A. **303 304** 4 EXPERIMENTS **305 306** We conduct extensive experiments to evaluate the effectiveness of WMPO, focusing on the following **307** questions: (1) can WMPO outperform online and offline RL in simulation environments; (2) how **308 309 310** Table 1: Comparison of policy optimization methods across four manipulation tasks in the Mimicgen simulation benchmark. _P_ denotes the rollout budget, i.e., the number of full real trajectories available **311** for policy optimization. Results show that WMPO consistently outperforms both GRPO and DPO **312** baselines under different budgets. As the rollout budget increases from 128 to 1280, WMPO continues **313** to exhibit substantial improvements, highlighting both its data efficiency and scalability. Performance **314** is reported as the task success rate (%). **315 316** Rollout budget _P_ Methods Coffee StackThree ThreePieceAssembly Square Mean (%) **317** _– Base policy_ 43.8 46.9 19.5 24.2 33.6 **318** GRPO 38.3 52.3 17.2 25.0 33.2 **319** 128 DPO 43.8 53.9 23.4 28.1 37.3 **320** Ours **61.7 56.3 37.5 32.8 47.1 321** GRPO 47.7 54.7 20.3 25.8 37.1 **322** 1280 DPO 52.3 57.0 26.7 33.6 42.4 **323** Ours **75.0 64.1 46.1 45.3 57.6** 

To overcome these challenges, we optimize policies entirely within a world model: replacing costly real-world rollouts with model-generated trajectories alleviates reliance on physical interaction and enables scalable online learning. We adopt Group Relative Policy Optimization (GRPO) as the policy optimization algorithm, since it provides stable and scalable training in settings with sparse rewards. In our case, state transitions are simulated by the world model (Eq. 2), and rewards are binary with _Rψψ_ ( _τ_ ) _∈{_ 0 _,_ 1 _}_ depending on task success. 

**Trajectory Sampling.** From each initial frames _I_ 0: _c_ sample from real environment _D_ , we sample a group of imagined trajectories _{ττ_ 1 _, . . . , τG}G}}_ from current policy _πθθ_ old inside the world model. The reward model is then employed to predict the success or failure of each trajectory. To mitigate vanishing gradients, we adopt a _Dynamic Sampling_ strategy (Yu et al., 2025): if all trajectories in a group are predicted to be successful or all unsuccessful, the group is discarded and additional rollouts are sampled until the batch is fully populated. The log-probability of each action chunk under _πθθ_ old is pre-computed as reference: 


**Policy Update.** Following DAPO (Yu et al., 2025), we remove the KL divergence regularization so that no reference model is required during training, thereby reducing memory consumption and encouraging the policy to explore novel behaviors. The final training objective is given by 


Here _ri,ti,t_ ( _θ_ ) is the probability ratio between new and old policies at step is the probability ratio between new and old policies at step _t_ of trajectory _τii_ , _Rii_ = _R_ ( _τii_ ), and _A_<sup>ˆ</sup> _i_ is the normalized advantage of trajectory _τii_ over the horizon _N_ . The overall training pipeline is detailed in Algorithm 1 in Appendix A. 

We conduct extensive experiments to evaluate the effectiveness of WMPO, focusing on the following questions: (1) can WMPO outperform online and offline RL in simulation environments; (2) how 

|Rollout budget_P_|Methods|Coffee|StackThree|ThreePieceAssembly|Square|Mean (%)|
|---|---|---|---|---|---|---|
|_–_|_Base policy_|43.8|46.9|19.5|24.2|33.6|
||GRPO|38.3|52.3|17.2|25.0|33.2|
|128|DPO|43.8|53.9|23.4|28.1|37.3|
||Ours|**61.7**|**56.3**|**37.5**|**32.8**|**47.1**|
||GRPO|47.7|54.7|20.3|25.8|37.1|
|1280|DPO|52.3|57.0|26.7|33.6|42.4|
||Ours|**75.0**|**64.1**|**46.1**|**45.3**|**57.6**|


6 

Under review as a conference paper at ICLR 2026 

**324** Base Policy **325 326 327** … **328 329** WMPO Continue moving down **330 331 332** … **333 334** Collision Self-correction **335** Figure 3: Behavior analysis of the _Square_ task (inserting the square into the stick) shows that, **336** compared with the base policy, WMPO demonstrates the ability to self-correct. **337 338** does the behavior of WMPO differ from imitation learning; (3) can WMPO generalize to unseen **339** settings; (4) can WMPO achieve iterative improvement during deployment; and (5) can WMPO be **340** applied on a real robot? **341 342** 4.1 EXPERIMENT SETTINGS **343 344 Implementation Details** In this work, we fine-tune OpenVLA-OFT (Kim et al., 2025) via imitation **345** learning on target manipulation tasks as our base policy. For simplicity, we omit the robot propri- **346** oceptive state and wrist camera inputs, and set the action chunk length _K_ to 8. We collect _P_ real **347** trajectories using the base policy, and conduct experiments with _P_ = 128 and _P_ = 1280 to evaluate **348** the scalability of our approach. These trajectories are further used to fine-tune a world model, which **349** predicts the next _K_ = 8 frames given _c_ = 4 conditioning frames and one action chunk. In addition, **350** we train reward models on the collected trajectories, using a video clip length of _L_ = 8 and a stride **351** of 1 during evaluation. Further training details are provided in Appendix A. **352 353 Simulation Environment Details** We conduct experiments in the Mimicgen simulation (Man- **354** dlekar et al., 2023). We select four fine-grained manipulation tasks: _Coffee_ _~~D~~ 0_ , _StackThree_ _~~D~~ 0_ , **355** _ThreePieceAssembly_ _~~D~~ 0_ , and _Square_ _~~D~~ 0_ , and fine-tune the OpenVLA-OFT model with 300 expert **356** trajectories per task as the base policy. For evaluation, we test 128 different initial states for each task **357** and report the average success rate. **358 359** 4.2 COMPARISON EXPERIMENTS **360 361** We compare WMPO with two established RL algorithms, GRPO (Shao et al., 2024) and **362** DPO (Rafailov et al., 2023), both widely used for optimizing large language models. To ensure **363** fairness, all methods are allocated the same real rollout budget _P_ . We consider both online and offline baselines: GRPO is implemented in an online setting, where the policy is updated directly from **364** trajectories collected in the environment; DPO is implemented in an offline setting, where the base **365** policy serves as the reference and trajectory pairs (success vs. failure) are constructed for optimization **366** using the standard DPO loss. Unlike GRPO, which discards trajectories after each update, DPO can **367** repeatedly reuse collected data, but it lacks the ability to update the policy online as WMPO does. **368** More implementation details are provided in Appendix B. **369** As shown in Tab. 1, WMPO consistently outperforms all baselines across all tasks. With a small **370** rollout budget of _P_ =128, it already surpasses the strongest baseline by +9 _._ 8 points, demonstrating **371** strong data efficiency. When the budget increases to _P_ =1280, the margin further expands to +15 _._ 2 **372** points on average, indicating that WMPO leverages additional trajectories more effectively than **373** existing methods and scales robustly with more rollouts. In contrast, GRPO often underperforms with **374** limited updates, and DPO plateaus due to static data reuse, whereas WMPO continues to improve **375** steadily as the rollout budget grows. Furthermore, we evaluate the reward model and find that it **376** achieves an F1 score above 0.95 across all tasks, reliably distinguishing success from failure and **377** effectively mitigating reward hacking. These results highlight the effectiveness and scalability of WMPO for policy optimization in robotic manipulation. 

7 

Under review as a conference paper at ICLR 2026 

**378 379 380 381 382 383 384 385 386 387 388 389 390** 


Figure 4: (a) For the _Square_ task, we vary the stick’s position from fixed to a random position inside a rectangle. (b) For the _StackThree_ task, we substitute the tabletop background with a gray background. (c) For the _ThreePieceAssembly_ task, we substitute the red base with a dark wooden base. 

### 4.3 EMERGENT BEHAVIOR OF WMPO 

**391** To better understand the source of WMPO’s strong performance, we conduct a visual comparison of **392** its test-time behavior against the base policy. We identify two emergent behaviors unique to WMPO: **393** (1) the WMPO policy learns to self-correct, recovering from nearly failure states; and (2) the WMPO **394** policy executes tasks more efficiently, as it rarely becomes “stuck” in suboptimal states. **395** First, taking the _Square_ task as an illustrative example (see Fig. 3), we observe that when both the **396** base policy and WMPO deviate from the correct trajectory due to error accumulation and encounter a **397** collision, their behaviors diverge. The baseline policy, trained only on expert demonstrations, has **398** never observed collisions during training; it continues to push the square against the stick until the **399** maximum time horizon is reached, resulting in failure. In contrast, WMPO benefits from large-scale **400** imagined trajectories generated by the world model, enabling it to learn the self-correction behaviors, **401** which is challenging to obtain through imitation learning alone. Specifically, the policy autonomously **402** learns to lift the square, realign it, and then insert it correctly, ultimately succeeding in the task. **403** Second, we analyzed the lengths of successful trajectories generated by different policies, as shown **404** in Fig. 5. We found that the trajectories of policies trained with WMPO are significantly shorter. This **405** is because WMPO discourages stuck behaviors, which often result in failures due to timeouts. As a **406** side benefit, WMPO also makes the policy’s behavior faster and smoother. 

**407 408 409** 

### 4.4 GENERALIZATION TO NOVEL TASKS 

**410** In this section, we evaluate the generalization ability of Table 2: We evaluate each policy in its **411** WMPO across three novel disruption scenarios (Fig. 4), corresponding disruption scenario and **412** which systematically assess generalization under spatial, report the success rate (%). **413** background, and texture shifts. As shown in Tab. 2, **414** WMPO consistently achieves the best performance across Methods Pos. Dis. Bg. Dis. Tex. Dis. Mean all disruption types. DPO attains modest improvements in Base policy 14.1 46.1 10.9 23.7 **415416** the in-distribution setting compared to the base policy, but GRPODPO 15.616.4 47.734.4 10.97.8 19.524.7 **417** its performance degrades significantly under backgroundand texture changes, suggesting reliance on spurious visual **Ours 22.3 50.0 16.4 29.6 418** cues rather than transferable manipulation skills. GRPO **419** exhibits performance similar to the base policy, and both are worse than WMPO across all disruption **420** scenarios. In contrast, WMPO, trained entirely in the world model, captures more generalizable **421** strategies and maintains reliable performance across spatial, background, and texture variations. **422 423** 4.5 LIFELONG LEARNING **424 425** In this section, we demonstrate that WMPO can continuously improve the performance of VLA **426** by iteratively collecting real trajectories from the environment. Specifically, we iteratively collect **427** _P_ = 128 real trajectories, perform WMPO to optimize the policy, and then use the updated policy **428** to collect another _P_ real trajectories. We apply the same setting to the DPO baseline. To compare **429** WMPO with an imitation learning-based policy using more expert demonstrations, we leverage 300, **430** 428, and 556 expert trajectories to train the base policy as a reference. It is important to note that **431** the base policy requires human-collected trajectories, whereas WMPO only relies on trajectories collected by the policy itself, making it more scalable. The results on the _StackThree_ task, shown in 

8 

Under review as a conference paper at ICLR 2026 

**432** 104 65 **433** 102 Base Policy ~~DPO~~ GRPO ~~WMPO~~ Base PolicyDPO **434** 60 ~~WMPO~~ 100 **435** 98 55 **436** 96 **437** 50 94 **438** 45 **439** 0 128 256 **440** Coffee StackThree ThreePieceAssembly Square Rollout Budget **441** Figure 5: Relative average trajectory length of successFigure 6: Lifelong learning re- **442** ful trials across different policies (Base Policy = 100%). sults of WMPO and baselines. **443 444** Real World Trajectory **445 446 447 448 449 450** Imagined Trajectory **451 452 453 454 455 456** Figure 7: Real-world experiments on the fine-grained manipulation task “Insert the square into the **457** stick” where the clearance between the square and the stick is only 5 mm. The top row shows the **458** real-world trajectory of the base policy executed in the real world, while the bottom row depicts the **459** corresponding imagined trajectory starting from the same initial state within our learned world model. Despite never observing this trajectory during training, the world model accurately predicts the future **460** evolution, demonstrating its ability to capture precise task dynamics. **461 462** Fig. 6, demonstrate that WMPO achieves stable and substantial improvements over both baselines, **463** whereas DPO fails to improve iteratively due to unstable training. **464 465** 4.6 REAL-WORLD EXPERIMENTS **466 467** In this section, we evaluate the challenging real-world manipulation task, “Insert the square into **468** the stick” (see Fig. 7, more cases including failure could be found in Appendix C), to validate the effectiveness of WMPO. Using the Cobot Mobile ALOHA platform, we collect 200 high-quality **469** expert demonstrations to finetune the OpenVLA-OFT model as the base policy. We then deploy this **470** policy to collect an additional 128 trajectories, which are used to further finetune the world model **471** and optimize the policy within it. For comparison, we also train an offline DPO policy using the same **472** dataset. All models are evaluated under identical experimental conditions, and we report the average **473** success rate over 30 trials. The results show that the base policy, DPO, and WMPO achieve success **474** rates of 53%, 60%, and 70%, respectively, demonstrating the effectiveness of WMPO on real robots. **475 476** 5 CONCLUSION **477 478** In this work, we introduced WMPO, a novel framework for on-policy RL of VLA models. By **479** grounding policy optimization entirely in a video-generative world model, WMPO eliminates the need **480** for costly real-world interactions while maintaining consistency with pretrained VLA representations. **481** Through policy behavior alignment, robust autoregressive video generation, and a lightweight reward **482** model, WMPO enables scalable training with strong sample efficiency. Extensive experiments **483** in both simulation and real-world settings demonstrated that WMPO (i) consistently outperforms **484** state-of-the-art model-free baselines, (ii) exhibits emergent self-correction behavior, (iii) generalizes **485** reliably to unseen scenarios, and (iv) supports iterative lifelong learning. Together, these findings highlight WMPO as a scalable and generalizable paradigm for advancing VLA RL. 

Figure 7: Real-world experiments on the fine-grained manipulation task “Insert the square into the stick” where the clearance between the square and the stick is only 5 mm. The top row shows the real-world trajectory of the base policy executed in the real world, while the bottom row depicts the corresponding imagined trajectory starting from the same initial state within our learned world model. Despite never observing this trajectory during training, the world model accurately predicts the future evolution, demonstrating its ability to capture precise task dynamics. 

9 

Under review as a conference paper at ICLR 2026 

**486** 

## 6 ETHICS STATEMENT 

#### **487** 

**488** This work uses only publicly available, open-source datasets for training and evaluation. No private **489** or sensitive data is involved. The proposed methods are intended solely for academic research in **490** machine learning and robotics. No foreseeable negative societal impacts are anticipated beyond **491** standard considerations for robotic learning research. 

**492** 

**493** 

**494** 

## 7 REPRODUCIBILITY STATEMENT 

**495** We have made every effort to ensure the reproducibility of our work. All datasets used are publicly **496** available and open-source. Detailed descriptions of the experimental settings, hyperparameters, **497** and training protocols are provided in Appendix A. We also release our implementation at an **498** anonymous repository: https://anonymous.4open.science/r/wmpo , which includes **499** training scripts, evaluation pipelines, and configuration files for all experiments. To further support **500** downstream research, we will additionally provide pretrained checkpoints of the world model and **501** task-specific fine-tuned models, enabling researchers to directly reproduce our results and easily **502** adapt the models to new tasks. 

**503** 

**504** 

## REFERENCES 

**505** 

- **506** Eloi Alonso, Adam Jelley, Vincent Micheli, Anssi Kanervisto, Amos Storkey, Tim Pearce, and **507** Franc¸ois Fleuret. Diffusion for world modeling: Visual details matter in atari. In _The Thirty-_ **508** _eighth Annual Conference on Neural Information Processing Systems_ , 2024. URL https: //openreview.net/forum?id=NadTwTODgC. 

- **509 510** Philip J. Ball, Jakob Bauer, Frank Belletti, Bethanie Brownfield, Ariel Ephrat, Shlomi Fruchter, **511** Agrim Gupta, Kristian Holsheimer, Aleksander Holynski, Jiri Hron, Christos Kaplanis, Marjorie **512** Limont, Matt McGill, Yanko Oliveira, Jack Parker-Holder, Frank Perbet, Guy Scully, Jeremy Shar, **513** Stephen Spencer, Omer Tov, Ruben Villegas, Emma Wang, Jessica Yung, Cip Baetu, Jordi Berbel, **514** David Bridson, Jake Bruce, Gavin Buttimore, Sarah Chakera, Bilva Chandra, Paul Collins, Alex **515** Cullum, Bogdan Damoc, Vibha Dasagi, Maxime Gazeau, Charles Gbadamosi, Woohyun Han, **516** Ed Hirst, Ashyana Kachra, Lucie Kerley, Kristian Kjems, Eva Knoepfel, Vika Koriakin, Jessica Lo, Cong Lu, Zeb Mehring, Alex Moufarek, Henna Nandwani, Valeria Oliveira, Fabio Pardo, Jane 

- **517** Park, Andrew Pierson, Ben Poole, Helen Ran, Tim Salimans, Manuel Sanchez, Igor Saprykin, 

- **518** Amy Shen, Sailesh Sidhwani, Duncan Smith, Joe Stanton, Hamish Tomlinson, Dimple Vijaykumar, 

- **519** Luyu Wang, Piers Wingfield, Nat Wong, Keyang Xu, Christopher Yew, Nick Young, Vadim Zubov, **520** Douglas Eck, Dumitru Erhan, Koray Kavukcuoglu, Demis Hassabis, Zoubin Gharamani, Raia **521** Hadsell, Aaron van den Oord, Inbar Mosseri, Adrian Bolton, Satinder Singh, and Tim Rockt¨ aschel.¨ **522** Genie 3: A new frontier for world models. 2025. **523** 

- **524** Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for 

- **525** general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- **526** 

- **527** Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, **528** Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action **529** models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 

**530** 

**531** 

**532 533** 

   - Yuhui Chen, Shuai Tian, Shugao Liu, Yingting Zhou, Haoran Li, and Dongbin Zhao. Conrft: A reinforced fine-tuning method for vla models via consistency policy. _arXiv preprint arXiv:2502.05450_ , 2025. 

- **534** Open X-Embodiment Collaboration. Open X-Embodiment: Robotic learning datasets and RT-X **535** models. https://arxiv.org/abs/2310.08864, 2023. 

- **536** DeepSeek-AI et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement 

- **537** learning, 2025. URL https://arxiv.org/abs/2501.12948. 

**538** 

- **539** Chelsea Finn and Sergey Levine. Deep visual foresight for planning robot motion. In _2017 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 2786–2793. IEEE Press, 

10 

Under review as a conference paper at ICLR 2026 

#### **540** 

**541** 

2017. doi: 10.1109/ICRA.2017.7989324. URL https://doi.org/10.1109/ICRA.2017. 7989324. 

**542 543** Bernd Frauenknecht, Devdutt Subhasish, Friedrich Solowjow, and Sebastian Trimpe. On rollouts **544** in model-based reinforcement learning. In _The Thirteenth International Conference on Learning_ **545** _Representations_ , 2025. URL https://openreview.net/forum?id=Uh5GRmLlvt. **546** Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James **547** Davidson. Learning latent dynamics for planning from pixels. In _International conference on_ **548** _machine learning_ , pp. 2555–2565. PMLR, 2019. **549 550** Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning **551** behaviors by latent imagination. _ICLR 2020_ , 2020a. **552** Danijar Hafner, Timothy Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete **553** world models. _arXiv preprint arXiv:2010.02193_ , 2020b. **554 555** Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains **556** through world models. _arXiv preprint arXiv:2301.04104_ , 2023. **557** Maximilian Igl, Luisa Zintgraf, Tuan Anh Le, Frank Wood, and Shimon Whiteson. Deep variational **558** reinforcement learning for pomdps. In _International conference on machine learning_ , pp. 2117– **559** 2126. PMLR, 2018. **560 561** Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, **562** Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: a vision-language-action **563** model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. **564** Stephen James, Kentaro Wada, Tristan Laidlow, and Andrew J Davison. Coarse-to-fine q-attention: Ef- **565** ficient learning for visual robotic manipulation via discretisation. In _Proceedings of the IEEE/CVF_ **566** _Conference on Computer Vision and Pattern Recognition_ , pp. 13739–13748, 2022. **567 568** Zhennan Jiang, Kai Liu, Yuxin Qin, Shuai Tian, Yupeng Zheng, Mingcai Zhou, Chao Yu, Haoran Li, **569** and Dongbin Zhao. World4rl: Diffusion world models for policy refinement with reinforcement **570** learning for robotic manipulation, 2025. URL https://arxiv.org/abs/2509.19080. **571** Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, **572** Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source **573** vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. **574 575** Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing **576** speed and success, 2025. URL https://arxiv.org/abs/2502.19645. 

- **577** Haozhan Li, Yuxin Zuo, Jiale Yu, Yuhao Zhang, Zhaohui Yang, Kaiyan Zhang, Xuekai Zhu, Yuchen **578** Zhang, Tianxing Chen, Ganqu Cui, Dehui Wang, Dingxiang Luo, Yuchen Fan, Youbang Sun, **579** Jia Zeng, Jiangmiao Pang, Shanghang Zhang, Yu Wang, Yao Mu, Bowen Zhou, and Ning Ding. **580** Simplevla-rl: Scaling vla training via reinforcement learning, 2025a. URL https://arxiv. **581** org/abs/2509.09674. 

**582** 

**583** 

**584** 

   - Qiyang Li, Zhiyuan Zhou, and Sergey Levine. Reinforcement learning with action chunking, 2025b. URL https://arxiv.org/abs/2507.07969. 

- **585** Fanqi Lin, Yingdong Hu, Pingyue Sheng, Chuan Wen, Jiacheng You, and Yang Gao. Data scaling **586** laws in imitation learning for robotic manipulation, 2024. URL https://arxiv.org/abs/ **587** 2410.18647. 

**588** 

**589** 

**590** 

- Jie Liu, Gongye Liu, Jiajun Liang, Yangguang Li, Jiaheng Liu, Xintao Wang, Pengfei Wan, Di Zhang, and Wanli Ouyang. Flow-grpo: Training flow matching models via online rl, 2025. URL https://arxiv.org/abs/2505.05470. 

**591** 

- **592** Guanxing Lu, Wenkai Guo, Chubin Zhang, Yuheng Zhou, Haonan Jiang, Zifeng Gao, Yansong **593** Tang, and Ziwei Wang. Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning, 2025. URL https://arxiv.org/abs/2505.18719. 

11 

Under review as a conference paper at ICLR 2026 

**594** 

**595** 

**596** 

**597** 

- Jianlan Luo, Zheyuan Hu, Charles Xu, You Liang Tan, Jacob Berg, Archit Sharma, Stefan Schaal, Chelsea Finn, Abhishek Gupta, and Sergey Levine. Serl: A software suite for sample-efficient robotic reinforcement learning. In _IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 16961–16969. IEEE, 2024a. 

**598** 

**599** Jianlan Luo, Charles Xu, Jeffrey Wu, and Sergey Levine. Precise and dexterous robotic manipulation **600** via human-in-the-loop reinforcement learning. _arXiv preprint arXiv:2410.21845_ , 2024b. **601** Xiao Ma, Siwei Chen, David Hsu, and Wee Sun Lee. Contrastive variational reinforcement learning **602** for complex observations. In _Conference on robot learning_ , pp. 959–972. PMLR, 2021. **603** 

- **604** Xiao Ma, David Hsu, and Wee Sun Lee. Learning latent graph dynamics for visual manipulation of **605** deformable objects. In _2022 International Conference on Robotics and Automation (ICRA)_ , pp. 8266–8273. IEEE, 2022. 

- **606** 

**607** Ajay Mandlekar, Soroush Nasiriany, Bowen Wen, Iretiayo Akinola, Yashraj Narang, Linxi Fan, Yuke **608** Zhu, and Dieter Fox. Mimicgen: A data generation system for scalable robot learning using human **609** demonstrations. _arXiv preprint arXiv:2310.17596_ , 2023. **610** NVIDIA, Niket Agarwal, Arslan Ali, Maciej Bala, Yogesh Balaji, Erik Barker, Tiffany Cai, Prithvijit **611** Chattopadhyay, Yongxin Chen, Yin Cui, Yifan Ding, Daniel Dworakowski, Jiaojiao Fan, Michele **612** Fenzi, Francesco Ferroni, Sanja Fidler, Dieter Fox, Songwei Ge, Yunhao Ge, Jinwei Gu, Siddharth **613** Gururani, Ethan He, Jiahui Huang, Jacob Huffman, Pooya Jannaty, Jingyi Jin, Seung Wook **614** Kim, Gergely Klar,´ Grace Lam, Shiyi Lan, Laura Leal-Taixe, Anqi Li, Zhaoshuo Li, Chen- **615** Hsuan Lin, Tsung-Yi Lin, Huan Ling, Ming-Yu Liu, Xian Liu, Alice Luo, Qianli Ma, Hanzi **616** Mao, Kaichun Mo, Arsalan Mousavian, Seungjun Nah, Sriharsha Niverty, David Page, Despoina **617** Paschalidou, Zeeshan Patel, Lindsey Pavao, Morteza Ramezanali, Fitsum Reda, Xiaowei Ren, **618** Vasanth Rao Naik Sabavat, Ed Schmerling, Stella Shi, Bartosz Stefaniak, Shitao Tang, Lyne **619** Tchapmi, Przemek Tredak, Wei-Cheng Tseng, Jibin Varghese, Hao Wang, Haoxiang Wang, Heng **620** Wang, Ting-Chun Wang, Fangyin Wei, Xinyue Wei, Jay Zhangjie Wu, Jiashu Xu, Wei Yang, Lin Yen-Chen, Xiaohui Zeng, Yu Zeng, Jing Zhang, Qinsheng Zhang, Yuxuan Zhang, Qingqing Zhao, **621** and Artur Zolkowski. Cosmos world foundation model platform for physical ai, 2025. URL **622** https://arxiv.org/abs/2501.03575. **623 624** Seohong Park, Kevin Frans, Deepinder Mann, Benjamin Eysenbach, Aviral Kumar, and Sergey **625** Levine. Horizon reduction makes rl scalable. _arXiv preprint arXiv:2506.04168_ , 2025. **626** Dustin Podell, Zion English, Kyle Lacey, Andreas Blattmann, Tim Dockhorn, Jonas Muller,¨ Joe **627** Penna, and Robin Rombach. SDXL: Improving latent diffusion models for high-resolution image **628** synthesis. In _The Twelfth International Conference on Learning Representations_ , 2024. URL **629** https://openreview.net/forum?id=di52zR8xgf. **630 631** Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D Manning, Stefano Ermon, and Chelsea **632** Finn. Direct preference optimization: Your language model is secretly a reward model. _Proceedings of Advances in Neural Information Processing Systems (NeurIPS)_ , 2023. **633 634** Stephane Ross, Geoffrey Gordon, and Drew Bagnell.´ A reduction of imitation learning and structured **635** prediction to no-regret online learning. In _AISTATS_ , pp. 627–635, 2011. **636 637** John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. **638 639** Younggyo Seo, Jafar Uruc¸, and Stephen James. Continuous control with coarse-to-fine reinforcement **640** learning. _arXiv preprint arXiv:2407.07787_ , 2024. **641 642** Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, Y. K. Li, Y. Wu, and Daya Guo. Deepseekmath: Pushing the limits of **643** mathematical reasoning in open language models, 2024. URL https://arxiv.org/abs/ **644** 2402.03300. **645** 

- **646** Zhan Tong, Yibing Song, Jue Wang, and Limin Wang. VideoMAE: Masked autoencoders are **647** data-efficient learners for self-supervised video pre-training. In _Advances in Neural Information Processing Systems_ , 2022. 

12 

Under review as a conference paper at ICLR 2026 

**648** Andrew Wagenmaker, Mitsuhiko Nakamoto, Yunchu Zhang, Seohong Park, Waleed Yagoub, Anusha **649** Nagabandi, Abhishek Gupta, and Sergey Levine. Steering your diffusion policy with latent space **650** reinforcement learning. _arXiv preprint arXiv:2506.15799_ , 2025. **651 652** Wenke Xia, Yichu Yang, Hongtao Wu, Xiao Ma, Tao Kong, and Di Hu. Robotic policy learning **653** via human-assisted action preference optimization, 2025. URL https://arxiv.org/abs/ 2506.07127. **654 655** Jingjing Xu, Xu Sun, Zhiyuan Zhang, Guangxiang Zhao, and Junyang Lin. Understanding and **656** improving layer normalization, 2019. URL https://arxiv.org/abs/1911.07013. **657 658** Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan, Xiaochen Zuo, Yu Yue, Tiantian Fan, Gaohong **659** Liu, Lingjun Liu, Xin Liu, Haibin Lin, Zhiqi Lin, Bole Ma, Guangming Sheng, Yuxuan Tong, Chi Zhang, Mofan Zhang, Wang Zhang, Hang Zhu, Jinhua Zhu, Jiaze Chen, Jiangjie Chen, Chengyi **660** Wang, Hongli Yu, Weinan Dai, Yuxuan Song, Xiangpeng Wei, Hao Zhou, Jingjing Liu, Wei-Ying **661** Ma, Ya-Qin Zhang, Lin Yan, Mu Qiao, Yonghui Wu, and Mingxuan Wang. Dapo: An open-source **662** llm reinforcement learning system at scale, 2025. URL https://arxiv.org/abs/2503. **663** 14476. **664** 

**665** Zijian Zhang, Kaiyuan Zheng, Zhaorun Chen, Joel Jang, Yi Li, Siwei Han, Chaoqi Wang, Mingyu **666** Ding, Dieter Fox, and Huaxiu Yao. Grape: Generalizing robot policy via preference alignment. **667** _arXiv preprint arXiv:2411.19309_ , 2024. **668** Zangwei Zheng, Xiangyu Peng, Tianji Yang, Chenhui Shen, Shenggui Li, Hongxin Liu, Yukun Zhou, **669** Tianyi Li, and Yang You. Open-sora: Democratizing efficient video production for all, 2024. URL **670** https://arxiv.org/abs/2412.20404. **671 672** Fangqi Zhu, Hongtao Wu, Song Guo, Yuxiao Liu, Chilam Cheang, and Tao Kong. Irasim: A finegrained world model for robot manipulation, 2025. URL https://arxiv.org/abs/2406. **673** 14540. **674 675 676 677 678 679 680 681 682 683 684 685 686 687 688 689 690 691 692 693 694 695 696 697 698 699 700 701** 

13 

Under review as a conference paper at ICLR 2026 

> **702** APPENDIX **703 704 705** A TRAINING DETAILS **706 707** In this section, we provide the training details of WMPO. The supervised finetuning of OpenVLA- **708** OFT is conducted on 8 H100 GPUs. We exclude robot proprioceptive states and wrist camera inputs **709** for simplicity. Instead of applying L1 regression, we adopt an output head that predicts discrete action tokens in parallel. The subsequent world model training and policy optimization are performed **710** on 32 H100 GPUs. **711 712** The world model is first pretrained on the Open X-Embodiment (OXE) dataset Collaboration (2023) **713** and then fine-tuned on downstream policy behavior data. Table 3 summarizes the hyperparameters **714** for training the world model, while the remaining settings follow OpenSora (Zheng et al., 2024). **715** The hyperparameters for policy optimization with GRPO are provided in Tab. 4, with other settings inherited from Li et al. (2025a). **716 717 Algorithm 1:** World Model Policy Optimization **718 Input :** World model _pϕ_ , reward model _Rψ_ , VLA policy _πθ_ ; group size _G_ ; batch size _B_ **719** (trajectories); mini-batch size _M_ ( _M | B_ ); epochs _E_ ; horizon _T_ **720 Output :** Updated policy parameters _θ_ **721** _θ_ old _← θ_ **722 while** _not converged_ **do 723** _B ←_ ∅ **724 while** _|B| < B_ **do 725** Sample initial state _s_ 0 = ( _I_ 0: _c, g_ ) _∼D_ **726 for** _i_ = 1 **to** _G_ **do 727** Imagine _τi_ = _{_ ( _s_<sup>_i_</sup> _t_<sup>_, ai_</sup> _t_<sup>)</sup><sup>_}T_</sup> _t_ =0<sup>_∼pθ_(</sup><sup>_τi| s_0</sup><sup>_, πθ_</sup> old<sup>)</sup> **728** _Ri ← R_ ( _τi_ ) _∈{_ 0 _,_ 1 _}_ **729 if** _all_ ( _R_ 1 _, . . . , RG_ ) **_or_** _none_ ( _R_ 1 _, . . . , RG_ ) **then 730 continue 731** _µ ← G_<sup><u>1</u></sup> � _Gi_ =1<sup>_Ri_,</sup> _σ ←_ ~~�~~ _G_ <u>1 �</u> _Gi_ =1<sup>(</sup><sup>_Ri −µ_)2</sup> **732 for** _i_ = 1 **to** _G_ **do 733** _A_ ˆ _i ←_ ( _Ri − µ_ ) _/σ_ **734 735** Pre-compute _{_ log _πθ_ old( _at_<sup>_i|si_</sup> _t_<sup>)</sup><sup>_}T_</sup> _t_ =0 **736** Append ( _τi, A_<sup>ˆ</sup> _i_ ) to _B_ **if** _|B| ≥ B_ **then 737 break 738 739 for** _e_ = 1 **to** _E_ **do 740 for** _j_ = 1 **to** _B/M_ **do 741** _M ← j_ -th contiguous block of _M_ trajectories from _B_ **742** Update _θ_ according to Eq. 4, where **743** _ri,t_ ( _θ_ ) = exp� log _πθ_ ( _ai,t|si,t_ ) _−_ log _πθ_ old( _ai,t|si,t_ )� **744** _θ_ old _← θ_ **745 746** 

> **747** B BASELINE DETAILS **748 749** We provide the implementation details of our baselines, including online GRPO and offline DPO. 

> **750** For the GRPO baseline, the main hyperparameters are inherited from Tab. 4. We observe that the 

> **751** batch size has a significant impact on performance. Larger batch sizes (e.g., 64) yield more stable 

> **752** improvements; however, they require a substantial number of real trajectories. Specifically, a single 

> **753** model update requires at least 64 _×_ 8 = 512 real trajectories. Moreover, dynamic sampling further **754** filters out groups with a success rate of 0 or 1. As a result, when the rollout budget is _P_ = 128, **755** such large batch sizes are infeasible, and even with _P_ = 1280, the model can only be updated once or twice. Therefore, we additionally experimented with a smaller batch size of 8, scaling the 

14 

Under review as a conference paper at ICLR 2026 

**756 757 758 759 760 761 762 763 764 765 766 767 768 769 770 771 772 773 774 775 776 777 778 779 780 781 782 783 784 785 786 787 788 789 790 791 792 793 794 795 796 797 798 799 800 801 802 803 804 805 806 807 808 809** 

learning rate down proportionally (by a factor of 8). We report the best results obtained across both configurations (batch size = 8 and = 64). 

For the DPO baseline, we follow the standard preference-based offline training paradigm. Specifically, we construct a preference dataset from trajectories collected by the supervised fine-tuned OpenVLAOFT model and use it to optimize the policy with the DPO objective. The model architecture and optimizer settings are kept consistent with those used in GRPO for fair comparison. All baselines were trained under the same rollout budgets and evaluation protocols as WMPO to ensure fairness. 

## C REAL WORLD CASES 

In this section, we provide additional examples of trajectory predictions made by the world model in real-world settings. Fig 8 illustrates cases where the world model successfully predicts failure trajectories: it has learned that when the square and the stick are misaligned, the square cannot be inserted into the stick. In contrast, Fig 9 shows a failure case where the model does not correctly predict a failed trajectory. Although predictions remain accurate until the final frame, subtle perturbations prevent the model from faithfully capturing the moment when the square gets stuck in the stick. Empirically, such failures are relatively rare on the validation set, indicating that the world model can reliably predict both successful and failed outcomes in the vast majority of scenarios, which is crucial for stable policy optimization. 

## D LIMITATION 

While the WMPO framework can in principle support flow-based policies, this work focuses on discretized action representations. As future work, we plan to extend WMPO to more expressive policy classes, such as flow-matching based policies (Black et al., 2024), and explore policy optimization with FlowGRPO (Liu et al., 2025), thereby broadening its applicability across diverse action spaces. 

## E LLM USAGE STATEMENT 

GPT-5 was used solely to assist with language refinement and stylistic polishing of the manuscript. The authors confirm that all scientific ideas, study design, data analyses, and conclusions presented in this work are entirely their own. The LLM did not contribute to the generation of research concepts, execution of experiments, or interpretation of findings. 

|**Hyperparameter**|**Value**|
|---|---|
|Optimizer|AdamW(_β_ = 0_._9_, β_ = 0_._999)|
|Learning rate|0.0001|
|Batch size|128|
|Gradient clip|0.1|
|Pretrain training steps|12,000,000|
|Finetune training steps|3,000,000|
|EMA|0.9999|
|Weight decay|0.0|
|Prediction target|_ϵ_|


Table 3: Hyperparameters for training the world model. 

15 

Under review as a conference paper at ICLR 2026 

**810 811 812 813 Hyperparameter Value 814** Optimizer AdamW( _β_ = 0 _._ 9 _, β_ = 0 _._ 999) **815** Learning rate 5 _×_ 10<sup>_−_6</sup> **816** Training batch size 64 **817** Group size _G_ 8 **818** Mini-batch size 128 **819** Clip ratio _εlow_ 0 _._ 20 **820** Clip ratio _εhigh_ 0 _._ 28 Temperature 1 _._ 6 **821 822** Table 4: Hyperparameters for the GRPO algorithm. **823 824 825 826 827 828 829** Real World Trajectory **830 831 832 833 834** Imagined Trajectory **835 836 837 838 839 840** Figure 8: Real-world experiments on the fine-grained manipulation task “Insert the square into the **841** stick”. The top row shows the rollout trajectory of the base policy executed in the real world, while **842** the bottom row depicts the corresponding imagined trajectory starting from the same initial state **843** within our learned world model. The world model successfully predicted failure cases. **844 845 846 847 848 849** Real World Trajectory **850 851 852 853 854** Imagined Trajectory **855 856 857 858 859 860** Figure 9: Example of a failure case. Although the predicted trajectory remains accurate until the final **861** frame, the model fails to capture the square getting stuck in the stick due to subtle perturbations. **862 863** 

16 

