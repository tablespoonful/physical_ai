---
title: "ACTION-AWARE DYNAMIC PRUNING FOR EFFICIENT VISION-LANGUAGE-ACTION MANIPULATION"
venue: "ICLR 2026 Poster"
original: "ICLR 2026 投稿時の匿名版"
url: https://arxiv.org/abs/2509.22093
pdf: https://arxiv.org/pdf/2509.22093
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2509.22093)** / [論文ページ](https://arxiv.org/abs/2509.22093)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。
> ICLR 2026 投稿時の匿名版から変換しました。リンク先の公開版とは内容が異なる場合があります。

Under review as a conference paper at ICLR 2026 

**003** 

**004** 

**005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 020 021 022 023 024 025 026 027 028 029** 

# **000** ACTION-AWARE DYNAMIC PRUNING FOR EFFICIENT **001 002** VISION-LANGUAGE-ACTION MANIPULATION 

### **Anonymous authors** 

Paper under double-blind review 

## ABSTRACT 

Robotic manipulation with Vision-Language-Action models requires efficient inference over long-horizon multi-modal context, where attention to dense visual tokens dominates computational cost. Existing methods optimize inference speed by reducing visual redundancy within VLA models, but they overlook the varying redundancy across robotic manipulation stages. We observe that the visual token redundancy is higher in coarse manipulation phase than in fine-grained operations, and is strongly correlated with the action dynamic. Motivated by this observation, we propose **A** ction-aware **D** ynamic **P** runing ( **ADP** ), a multi-modal pruning framework that integrates text-driven token selection with action-aware trajectory gating. Our method introduces a gating mechanism that conditions the pruning signal on recent action trajectories, using past motion windows to adaptively adjust token retention ratios in accordance with dynamics, thereby balancing computational efficiency and perceptual precision across different manipulation stages. Extensive experiments on the LIBERO suites and diverse real-world scenarios demonstrate that our method significantly reduces FLOPs and action inference latency ( _e.g._ 1.35× speed up on OpenVLA-OFT) while maintaining competitive success rates ( _e.g._ 25.8% improvements with OpenVLA) compared to baselines, thereby providing a simple plug-in path to efficient robot policies that advances the efficiency and performance frontier of robotic manipulation. 

**030** 

**031** 

## 1 INTRODUCTION 

**032** 

**033** Large vision language models Liu et al. (2023c;b; 2024a); Team et al. (2023); Awadalla et al. (2023) **034** have recently been extended into **V** ision– **L** anguage- **A** ction (VLA) models Kim et al. (2024; 2025); **035** Black et al. (2024); Li et al. (2024); Brohan et al. (2024); Wen et al. (2025b;a); Bjorck et al. (2025) **036** that map both the visual observation and language instruction to executable robot actions. In the **037** mainstream pipeline, a vision encoder produces dense visual tokens from one or more camera views, **038** a projector aligns them to the language space, and an LLM fuses all modalities to predict actions. **039** However, this multi-modal design introduces long input sequences with numerous visual tokens that are only weakly relevant to the current manipulation operation, which inflates compute, memory **040** footprint, and latency, and it can dilute attention over truly task-relevant cues. **041** 

**042** Existing work pursues efficiency via architectural lightening and modality-aware compression, such as **043** RoboMamba Liu et al. (2024b) that focuses on lightweight designs, DeeR-VLA Yue et al. (2024) that **044** aims at structured pruning/reparameterization, Mole-VLA Zhang et al. (2025) that targets conditional **045** layer activation, VLA-Cache Xu et al. (2025) that focuses on cache reuse, and EfficientVLA Yang et al. (2025) that aims to prune visual tokens via attention. However, a key but underexplored property **046** of robotic manipulation is that **visual redundancy in VLAs is action-aware across different 047 manipulation stages** . As Fig. 1 shows, during coarse-grained operations ( _e.g._ , relocating), global **048** movement dominates and redundant tokens can be pruned; during fine-grained phases ( _e.g._ , grasping), **049** local geometry and detailed cues dominate and preserving full vision is preferred. Moreover, the **050** relevance of visual patches is not only text conditioned (semantics of the instruction) but also _action_ **051** _conditioned_ (instantaneous end-effector motion and gripper state). Treating all steps uniformly, or **052** ranking tokens solely by mixed attention scores, therefore yields suboptimal pruning schedules that **053** either prune too little (limited savings) or prune too much (accuracy loss), especially in multi-view settings (scene and wrist/gripper cameras) where importance is unevenly distributed across time. 

1 

Under review as a conference paper at ICLR 2026 

**054 055 056 057 058 059 060 061 062 063 064 065 066 067 068 069** Figure 1: **Action-aware dynamic pruning vs. static pruning.** We visualize five _past_ observation **070** windows as cases from a manipulation episode that condition the _current anticipatory_ window. _p_ 1, **071** _p_ 3 and _p_ 5 reflect coarse phases, prompting the gate to _enable_ pruning to suppress redundant tokens, **072** whereas _p_ 2 and _p_ 4 are delicate phases requiring detail vision context, so pruning is _disabled_ and full vision is used. The curves depict robot’s motion that drives the gating rule. **073 074 075** To address this challenge, we introduce Action-aware Dynamic Pruning (ADP), a plug-and-play **076** strategy that reduces computation while preserving manipulation fidelity. ADP is built on two complementary ideas: (1) _Text-driven Pruning_ evaluates the relevance of visual patch using cross-modal **077** similarities, selecting only the most relevant tokens before entering deep fusion in the subsequent **078** layers. (2) _Action-aware Dynamics_ modulate whether pruning is activated at a given step using **079** a lightweight decision signal derived from the end-effector trajectory within each action window. **080** Specifically, when the recent motion magnitude is relatively low compared to past motion statistics **081** (delicate phases), pruning is disabled to preserve the full visual field for precise control. Conversely, **082** when the motion magnitude is relatively high compared to past motion statistics (coarse phases), **083** pruning is engaged to suppress redundancy and save FLOPs. We implement a gated mechanism that **084** treats recent action statistics as a pruning signal over sliding trajectory windows, adaptively adjusting **085** retention ratios according to motion dynamics and balancing efficiency with precision across manipu- **086** lation stages. Our contributions can be summarized as: (1) We show that the importance of the visual **087** token in VLA models varies within different stages of robotic manipulation. This insight motivates our dynamic pruning method tailored to manipulation phases compared to static pruning approaches. **088** (2) We propose _text-driven action-aware pruning_ that combines task instruction relevance with a **089** gating rule based on end-effector motion, enabling adaptive switching between pruned and full-vision **090** states. (3) We present a principled complexity analysis and extensive experiments in simulation and **091** real-world settings, demonstrating that our method reduces FLOPs and latency while maintaining **092** fine visual details required for successful manipulation. **093 094 095** 2 PRELIMINARY **096** 

**097** The mainstream vision–language–action paradigm extends large vision–language models to generate **098** executable robot actions from multi-modal inputs—visual observations (scene and wrist/gripper **099** views) and task instructions. A pre-trained vision encoder produces visual tokens, a projector aligns **100** them to the LLM token space, and the LLM fuses modalities and autoregressively emits action tokens, which are de-tokenized into a continuous 7-dimensional robot action. **101 102** Formally, given a sample of a scene image _I_<sup>_s_</sup> _∈_ R<sup>_H×W ×_3</sup> , a gripper view _I_<sup>_g_</sup> _∈_ R<sup>_H×W ×_3</sup> , and a task **103** instruction _I_<sup>_t_</sup> _∈_ R<sup>_N×L_</sup> , the vision encoder _f_ enc<sup>_v_(DINOv2 Oquab et al. (2023) and SigLIP Zhai et al.</sup> **104** (2023)) and text tokenizer _f_ enc<sup>_t_project the multi-modal data into the same latent dimension space:</sup> **105 106 X**<sup>vis</sup> = _f_ enc<sup>_v_(</sup><sup>_Is, Ig_)</sup><sup>_,_</sup> **X**<sup>txt</sup> = _f_ enc<sup>_t_(</sup><sup>_It_)</sup><sup>_,_</sup> (1) **107** 

where **X**<sup>vis</sup> _∈_ R<sup>_L_vis</sup><sup>_×D_</sup> and **X**<sup>txt</sup> _∈_ R<sup>_L_txt</sup><sup>_×D_</sup> represent latent embeddings for vision and text. 

2 

Under review as a conference paper at ICLR 2026 

**108 OpenVLA.** In the latent space, the embedding representations are concatenated into a multi-modal **109** sequence as: **110 X**<sup>_m_</sup> = **X**<sup>[</sup><sup>_BOS_]</sup> _⊕_ **X**<sup>vis</sup> _⊕_ **X**<sup>prop</sup> _⊕_ **X**<sup>txt</sup> (2) **111** where _⊕_ denotes concatenating embeddings of [BOS], vision, text, and proprioceptive (optionally) **112** along the sequence length dimension, yielding multi-modal inputs **X**<sup>_m_</sup> _∈_ R<sup>1+</sup><sup>_L_vis+</sup><sup>_L_txt+1</sup> . The **113** multi-modal sequence **X**<sup>_m_</sup> is then fed into a Large Language Model (LLM) _f_ LLM (Llama2 Touvron **114** et al. (2023)), which performs contextual reasoning and autoregressively generates an action token **115** sequence: **116** 7 **117** _p_ (ˆ **a** _|_ **X**<sup>_m_</sup> ) = � _f_ LLM(ˆ _aj |_ **X**<sup>_m_</sup> _,_ ˆ _a<j_ ) _,_ (3) **118** _j_ =1 **119** where ˆ **a** = (ˆ _a_ 1 _, . . . ,_ ˆ _a_ 7) _∈_ T<sup>7</sup> and T = _{_ 1 _, . . . , K}_ denotes the reserved action token space. **120 OpenVLA-OFT.** For optimize finetuning version, the paradigm shifts to parallel decoding without **121** traditional autoregressive decoding stage. In the latent space, the method introduces _L_ act placeholder **122 X**<sup>place</sup> as inputs for actions positions: **123 X**<sup>_m_</sup> = **X**<sup>[BOS]</sup> _⊕_ **X**<sup>vis</sup> _⊕_ **X**<sup>prop</sup> _⊕_ **X**<sup>txt</sup> _⊕_ **X**<sup>place</sup> _,_ (4) **124** where **X**<sup>_m_</sup> _∈_ R<sup>1+</sup><sup>_L_vis+</sup><sup>_L_txt+1+</sup><sup>_L_act</sup> and the first placeholder as current action placeholder and another **125** _L_ act _−_ 1 actions as future actions. During generation, the LLM directly predicts action tokens at **126** action chunk in parallel: **127 128 A** ˆ = _f_ LLM( **X**<sup>_m_</sup> )��place<sup>_∈_T</sup><sup>_L_act</sup><sup>_×_7</sup><sup>_,_</sup> (5) **129** where **A**<sup>ˆ</sup> = [ˆ **a** 1; _. . ._ ; ˆ **a** _L_ act], and each **a** ˆ _i_ = (ˆ _ai,_ 1 _, . . . ,_ ˆ _ai,_ 7) _∈_ T<sup>7</sup> represents the tokenized 7-DoF **130** action predicted at the _i_ -th placeholder position. To expand action representation ability, the oft **131** version also introduce the continuous control with token-level modeling, which each dimension of **132** the continuous action is uniformly discretized into 256 bins. During generation, the 7 degrees of **133** freedom action follows the standard gripper parameterization: **134 a** ˆ<sup>_c_</sup> = [ ∆ _x,_ ∆ _y,_ ∆ _z,_ ∆ _ϕ,_ ∆ _θ,_ ∆ _ψ, g_ ]<sup>_⊤_</sup> _,_ (6) **135** where (∆ _x,_ ∆ _y,_ ∆ _z_ ) denote Cartesian displacements, (∆ _ϕ,_ ∆ _θ,_ ∆ _ψ_ ) denote Euler-angle rotations **136** (roll, pitch, yaw), and _g_ denotes the gripper. **137 138** 3 RELATED WORK **139 140 Vision-Language-Actions.** Vision-Language-Action (VLA) models extend large vision-language **141** models with an action generator that links multimodal perception to low-level robot control. They take **142** images and text instructions, encode them into a shared latent space, then decode it into executable **143** actions. Early approaches Chi et al. (2023); Kim et al. (2024) map multimodal embeddings to **144** discrete tokens, while more recent works Wen et al. (2025b); Kim et al. (2025) emphasize continuous **145** parallel decoding actions for improving performance. To this end, lightweight MLPs, diffusion-based **146** decoders, and parallel decoding strategies have been introduced to transform hidden states into **147** temporally consistent trajectories. Representative architecture include CogACT Li et al. (2024), OpenVLA Kim et al. (2024), OpenVLA-OFT Kim et al. (2025), and _π_ series Black et al. (2024), **148** which adopt diffusion modules for iterative refinement of continuous actions, as well as optimized **149** fine-tuning frameworks that leverage placeholder tokens for parallel action prediction. **150 151 Efficient Robotic Manipulations.** The high computational complexity of Vision-Language-Action **152** (VLA) models poses significant efficiency challenges for real-time robotic control. To address this, **153** recent works have proposed efficiency-oriented strategies that can be broadly divided into trainingaware and training-free approaches. Training-aware methods, such as RoboMamba Liu et al. (2024b) **154** and DeeR-VLA Yue et al. (2024), redesign architectures or apply compression and pruning during **155** training, achieving notable speedups while preserving accuracy. For instance, DeeR-VLA Yue et al. **156** (2024) introduces dynamic reparameterization and structured pruning to reduce FLOPs, and Mole- **157** VLA Zhang et al. (2025) selectively activates subsets of model layers conditioned on task demands, **158** yielding scalable deployment. On the other hand, training-free methods aim to accelerate inference **159** without retraining. VLA-Cache Xu et al. (2025) reuses keys and values of uninformative tokens **160** between consecutive steps to save computation, while EfficientVLA Yang et al. (2025) retain task- **161** relevant patches identified via attention maps. However, these methods typically rely on single-layer heuristics or static rules that may overlook stage-dependent redundancy in manipulation tasks. 

3 

Under review as a conference paper at ICLR 2026 

**162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215** 


Figure 2: Overview of our proposed **A** ction-aware **D** ynamic **P** runing ( **ADP** ) for Vision-LanguageAction models. **(a.)** Action-aware gating: the pruning function adaptively determines whether to prune based on recent end-effector trajectories (∆ _x,_ ∆ _y,_ ∆ _z,_ ∆ _ϕ,_ ∆ _θ,_ ∆ _ψ, g_ ) , enabling dynamic pruning. **(b.)** Anticipatory pruning: task-relevant visual tokens are selected via attention-based relevance, while redundant patches are discarded before entering the VLA backbone. 

## 4 METHODOLOGY 

In this section, we introduce our proposed method Action-aware Dynamic Pruning (ADP) in VLAs for robotic manipulations. We first introduce text-driven pruning that identifies text-relevant tokens in Section 4.1 and then introduce action-aware dynamics that dynamically modulates the pruning strategy according to the past observed actions in Section 4.2. 

### 4.1 TEXT-DRIVEN ANTICIPATORY PRUNING 

Before entering the LLM, the multimodal sequence **X** still contains a large number of redundant visual tokens, which increase computation and dilute attention focus. To mitigate this redundancy, we compute the relevance of visual tokens with respect to task instructions at each layer, which shown in Figure 3. Let the hidden state at layer _l_ be **H**<sup>(</sup><sup>_l_)</sup> _∈_ R<sup>_S×D_</sup> ( **H**<sup>(0)</sup> = **X**<sup>_m_</sup> in Eq. 2). We partition **H**<sup>(</sup><sup>_l_)</sup> into the vision and text subsets **H**<sup>(</sup> vis<sup>_l_)</sup><sup>_∈_R</sup><sup>_L_vis</sup><sup>_×D_and</sup><sup>**H**</sup> txt<sup>(</sup><sup>_l_)</sup><sup>_∈_R</sup><sup>_L_txt</sup><sup>_×D_.Applying the projection</sup> matrices, we obtain query and key representations: 


reshaped into multi-head form **Q**<sup>(</sup><sup>_l_)</sup> _∈_ R<sup>_N h×L_txt</sup><sup>_×d_</sup> and **K**<sup>(</sup><sup>_l_)</sup> _∈_ R<sup>_Nh×L_vis</sup><sup>_×d_</sup> . The scaled dot-product similarity is then computed as 


where each entry measures the degree to which a text token attends to a visual patch. To derive a global importance score per visual token, we average across heads and text queries: 


where _v ∈{_ 1 _, . . . , L_ vis _}_ indexes visual tokens, _N_<sup>_h_</sup> is the number of attention heads, _L_<sup>txt</sup> is the text sequence length, and _L_<sup>vis</sup> is the total number of visual tokens. In multi-view scenarios with _C_ input images ( _e.g._ , scene and wrist views), each contributing _L_<sup>vis</sup> _c_<sup>patches such that �</sup><sup>_C_</sup> _c_ =1<sup>_L_</sup> _c_<sup>vis=</sup><sup>_L_vis, the</sup> retention quota is distributed across views by a weighting vector _α ∈_ R<sup>_C_</sup> with<sup>�</sup><sup>_C_</sup> _c_ =1<sup>_αc_= 1.The</sup> remain visual tokens kept for view _c_ is 


4 

Under review as a conference paper at ICLR 2026 

**217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269** 

> **216** where Φ<sup>(</sup><sup>_l_)</sup> **217** ( _c_ )<sup>denotes the importance scores restricted</sup> to view _c_ . For each view _c_ , the remain visual tokens **218** could be represented as: 


The reduced visual sequence **X**<sup>vis</sup> keep<sup>is then concate-</sup> nated back with other modalities to form the pruned multimodal sequence: 


where **X**<sup>˜</sup><sup>_m_</sup> denotes the dynamically reduced input propagated to the LLM module. 

### 4.2 ACTION-AWARE DYNAMIC STRATEGY 

While static pruning can effectively identify taskrelevant visual tokens, not every stage of a manipula- 


Figure 3: Text-driven Anticipatory Pruning. **Step 1** : Retrieval pretrained weights from Layer _l_ to compute relevance scores. **Step 2** : Treat text as a guider to prune vision tokens based on the ranking . 

tion task is suitable for relying solely on the pruned set. In particular, missing fine-grained visual details may cause failures in operations such as moving, swiping, or aligning objects. The accumulation of such local errors can easily propagate and ultimately cause the entire task to fail. To address this limitation, we introduce a dynamic visual strategy that adapts the pruning decision to the robot’s motion state across different task phases, guided by the end-effector (EEF) trajectory within each action chunk, which focus on capturing both translational displacement and rotational motion. 

**Windowed trajectory and actions.** Assume _i_ indexes windows and _u_ indexes steps within a window; _bi_ and _ei_ denote the start and end timesteps, and _ω_ matches the OFT action placeholder length. We treat each decoded action chunk as a temporal window [ _bi, ei_ ] of length _ω_ = _ei−bi_ +1 with actions **A** _i_<sup>_c_=[</sup><sup>**a**</sup><sup>_c_</sup> _i,_ 1<sup>;</sup><sup>_. . ._;</sup><sup>**a**</sup> _i,ω_<sup>_c_]</sup><sup>_∈_R</sup><sup>_ω×_7,where</sup><sup>**a**</sup><sup>_c_</sup> _i,u_<sup>=[ ∆</sup><sup>_xi,u,_∆</sup><sup>_yi,u,_∆</sup><sup>_zi,u,_∆</sup><sup>_ϕi,u,_∆</sup><sup>_θi,u,_∆</sup><sup>_ψi,u, gi,u_]</sup><sup>_⊤_</sup> collects per-step translational and rotational increments and the gripper command. 

**Definition 4.1** (Windowed FK for EEF Position) **.** _Let Tt ∈ SE_ (3) _be the EEF pose at time t, and π_ : _SE_ (3) _→_ R<sup>3</sup> _extract its translation. With body-frame (right-multiply) composition,_ 


The rotation order _RxRyRz_ follows our implementation; if a world-frame (left-multiply) update or a different Euler order is used, the composition should be adjusted accordingly. Definition 4.1 therefore makes **p** _t_ = _π_ ( _Tt_ ) an explicit function of the full 7-DoF action sequence within each window. 

**Windowed trajectory distance.** Given **p** _t_ from Def. 4.1, we quantify motion per window either by the Euclidean displacement: 


The windowed trajectory distance aims to yield a scalar _δi_ that captures overall motion magnitude and subsequently drives our pruning decision rule. 

**Dynamic decision function.** Given a windowed trajectory distance, we define a binary state variable _si ∈{_ 0 _,_ 1 _}_ , where _si_ = 0 corresponds to the _full-vision_ state (w/o pruning) and _si_ = 1 to the _pruned_ state (cross-attention pruning). therefore next state could be determined by 


5 

Under review as a conference paper at ICLR 2026 

**270** The dynamic switch to _si_ +1 adapts to the global motion scale of the task, enabling pruning during **271** periods of high activity while retaining full vision during fine-grained phases. An alternative is the **272** _adjacent-extrema function_ , which sets thresholds based on the extrema of the most recent _τ_ windows: **273 274** _U_<sup>(</sup><sup>_i_)</sup> = max _{δi−τ_ +1 _, . . . , δi},_ (17) **275** _V_<sup>(</sup><sup>_i_)</sup> = min _{δi−τ_ +1 _, . . . , δi}_ **276 277** with the update rule **278** 1 _, δi ≥ U_<sup>(</sup><sup>_i_)</sup> _,_ **279** _si_ +1 = 0 _, δi ≤ V_<sup>(</sup><sup>_i_)</sup> _,_ (18)  **280**  _si, V_<sup>(</sup><sup>_i_)</sup> _< δi < U_<sup>(</sup><sup>_i_)</sup> _._ **281 282** This design aims to respond quickly to local motion variations, capturing abrupt efficient shifts between coarse and delicate manipulations. When the robot exhibits large-amplitude motions, **283** pruning is activated to suppress redundant visual input and reduce computation. When motion **284** amplitude decreases, signaling the onset of fine manipulation, pruning is disabled to preserve the **285** complete visual context necessary for accurate control. **286 287** 4.3 THEORETICAL ANALYSIS OF COMPUTATIONAL COMPLEXITY **288 289** We consider the computational cost of the Transformer stack in _f_ LLM with respect to the sequence **290** length before and after pruning. Let _S_ denote the token length of the full multi-modal sequence **291** in Eq. 2, _D_ the hidden dimension, and _M_ the intermediate dimension of the feed-forward network **292** (SwiGLU). The total number of vision tokens before pruning is _L_ vis, while _k_ = _⌊ρ · L_ vis _⌋_ tokens are **293** kept after the text-driven selection in Eq. 10. We denote by _T_ the number of forwards in a complete **294** task execution (Eq. 5), and by _γ ∈_ [0 _,_ 1] the proportion of forwards executed in the pruned state **295** (Sec. 4.2). Let _H_ be the number of Transformer layers in _f_ LLM. **296** For one Transformer layer, the FLOPs are approximated by **297 298** _F_ ( _S_ ; _D, M_ ) _≈_ 2 _S_<sup>2</sup> _D_ + 4 _SD_<sup>2</sup> + 6 _SDM,_ (19) **299** corresponding to attention, projections, and MLP. A baseline forward of the _H_ -layer LLM therefore **300** costs **301** _F_ base = _H · F_ ( _S_ ; _D, M_ ) _._ (20) **302 303** In ADP, pruning happens _before_ the LLM at the embedding stage: visual tokens are ranked and **304** reduced using Eq. 9–10, yielding the shorter sequence **305** _S_<sup>_′_</sup> = 1 + _k_ + _L_ prop + _L_ txt + _L_ act + 1 _._ (21) **306 307** The scoring overhead uses lightweight projections and a similarity matrix between text and vision **308** embeddings, **309** _F_ score = 2 _L_ txt _D_<sup>2</sup> + 2 _L_ vis _D_<sup>2</sup> + 2 _N_<sup>_h_</sup> _L_ txt _L_ vis _d._ (22) **310** Assume pruning and scoring are performed once per forward _before_ any Transformer layer, so all **311** _H_ layers operate on _S_<sup>_′_</sup> , the per-layer cost follows _F_ ( _S_ ; _D, M_ ) _≈_ 2 _S_<sup>2</sup> _D_ + 4 _SD_<sup>2</sup> + 6 _SDM_ , and **312** _D_ = _N_<sup>_h_</sup> _d_ , **313** ∆ _F_ ADP = _F_ base _− F_ ADP _, F_ ADP = _F_ score + _H · F_ ( _S_<sup>_′_</sup> ; _D, M_ ) _,_ (23) **314 315** where _k_ = _⌊ρ L_ vis _⌋_ , _S_<sup>_′_</sup> is as above with _L_ prop _, L_ txt _, L_ act the proprioception/text/action lengths, _N_<sup>_h_</sup> is the number of attention heads of size _d_ , and _F_ base = _H F_ ( _S_ ; _D, M_ ). Over an episode of _T_ forwards, **316** the expected complexity under the dynamic strategy is **317 318** E[ _F_ episode] = _T_ � _γ F_ ADP + (1 _− γ_ ) _F_ base� _,_ (24) **319** with expected savings **320 321** E[∆ _F_ episode] = _T γ_ ∆ _F_ ADP _._ (25) **322** The pruning is applied at the embedding stage prior to _f_ LLM, so the reduced length _S_<sup>_′_</sup> benefits all _H_ **323** layers uniformly, and the dynamic rule (Eq. 14–16) controls how often the pruned path is used across action windows. 

6 

Under review as a conference paper at ICLR 2026 

> **324** Table 1: **Results on the LIBERO Benchmark. TR** : Training-Free; **AR** : Auto-Regressive; **PD** : **325** Parallel Decoding. **Ratio** : The retain tokens / Full tokens. **326 327 Method TR Decoding CKPT Spatial Object Goal Long Average FLOPs** _↓_ **Speedup** _↑_ **328** OpenVLA Kim et al. (2024)SparseVLM Zhang et al. (2024) ✓- ARAR OpenVLA (7B)OpenVLA (7B) 84.7%79.8% 88.4%67.0% 79.2%72.6% 53.7%39.4% 76.5%64.7% -- -- **329** FastV Chen et al. (2024) ✓ AR OpenVLA (7B) 83.4% 84.0% 74.2% 51.6% 73.3% - - VLA-Cache Xu et al. (2025) ✓ AR OpenVLA (7B) 83.8% 85.8% 76.4% 52.8% 74.7% - - **330** FlashVLA Tan et al. (2025) ✓ AR OpenVLA (7B) 84.2% 86.4% 75.4% 51.4% 74.4% - - SP-VLA Li et al. (2025) ✓ AR OpenVLA (7B) 75.4% 85.6% 84.4% 54.2% 74.9% - - **331** WorldVLA Cen et al. (2025) - AR Chameleon (7B) 85.6% 89.0% 82.6% 59.0% 79.1% - - **332** WorldVLA* Cen et al. (2025)NORA Hung et al. (2025) -- ARAR Chameleon (7B)Qwen-VL (3B) 87.6%85.6% 96.2%87.8% 83.4%77.0% 60.0%45.0% 81.8%73.9% -- -- **333** SmolVLA Shukor et al. (2025) - AR SmolVLM (2.25B) 93.0% 94.0% 91.0% 77.0% 88.8% - - CogACT Li et al. (2024) - FM CogVLM (7B) 97.2% 98.0% 90.2% 88.8% 93.6% - - **334** NORA-Long Hung et al. (2025) - PD Qwen-VL (3B) 92.2% 95.4% 89.4% 74.6% 87.9% - - OpenVLA-OFT Kim et al. (2025) - PD OFT (7B) 98.6% 98.2% 96.6% 94.8% 97.1% 7.91 1.00× **335** FastV(+OFT) Chen et al. (2024) ✓ PD OFT (7B) 96.8% 81.0% 96.4% 73.0% 86.8% 6.37 1.24× **336** **<mark>VLA-ADP (Ratio=30%)</mark>** <mark>✓ PD OFT (7B) 97.6%</mark> **<mark>98.4% 97.4%</mark>** <mark>84.2% 94.4% 5.85 1.35×</mark> **<mark>VLA-ADP (Ratio=40%)</mark>** <mark>✓ PD OFT (7B) 98.2% 97.2% 96.6% 87.2% 94.8% 6.14 1.29×</mark> **337** **<mark>VLA-ADP (Ratio=50%)</mark>** <mark>✓ PD OFT (7B)</mark> **<mark>99.4</mark>** <mark>% 98.0% 96.4% 91.2%</mark> **<mark>96.3%</mark>** <mark>6.43 1.23×</mark> **338** **<mark>VLA-ADP (Ratio=60%)</mark>** <mark>✓ PD OFT (7B) 98.8% 98.0% 95.8%</mark> **<mark>92.0%</mark>** <mark>96.2% 6.74 1.17×</mark> **<mark>VLA-ADP (Ratio=70%)</mark>** <mark>✓ PD OFT (7B) 99.0% 98.2% 96.8% 91.2%</mark> **<mark>96.3%</mark>** <mark>7.03 1.13×</mark> **339 340 341 342 343 344 345 346 347 348 349** Figure 4: Visualisation of our method on representative examples of the four LIBERO task types **350** (Spatial, Object, Goal, Long). Blue masks indicate pruned vision tokens. The retained tokens con- **351** sistently highlight task-relevant objects, validating the Text-driven Anticipatory Pruning. Moreover, full vision tokens are restored at critical phases ( _e.g._ , initialisation, grasping, placement), demonstrat- **352** ing the effectiveness of the Task-driven Pruning and Action-Aware Dynamic Strategy. **353 354** 5 EXPERIMENTS **355 356 357** We conduct experiments across LIBERO simulation and real-robot tasks under standardized set- **358** tings, comparing against strong baselines and conducting targeted ablations to assess success rates, **359** compute/latency, and the contributions of dynamic scheduling and layer-wise pruning. **360 361** 5.1 SIMULATION EXPERIMENTS **362 363 Experiments setup.** For simulation, we use LIBERO Liu et al. (2023a) with four suites ( _i.e._ , Spatial, Object, Goal, Long) evaluating spatial understanding, object recognition, goal-directed behaviour, **364** and long-horizon planning. All Libero settings follow OpenVLA-OFT, using its public run scripts. **365** For comparison, we reproduce FastV Chen et al. (2024) on OpenVLA-OFT and run under the same 

> **366** environment. Experiments run on Linux with an NVIDIA RTX 4090. We set the window size to 

> **367** the OpenVLA-OFT chunk size (8) and apply a cold start: the first two windows use full vision. 

> **368** To limit error accumulation, if pruning occurs in three consecutive windows, the next window is **369** forced to full vision. In multi-view pruning, the main wrist retention is 4:6. Within the Action-Aware **370** Dynamic Strategy, we use Euclidean displacement and the adjacent-extrema rule; in its third case we **371** deterministically set the state to 1 (instead of inheriting _sii_ ) to further reduce FLOPs. **372 Main result.** Table 1 shows that VLA-ADP achieves a stable accuracy–compute trade-off across the 

> **373** keep ratio on LIBERO. Compared to OpenVLA-OFT, when the keep ratio is 50–70%, the average 

> **374** success rate slightly decreases ( _≤_ 0.9%), while the LLM-side inference speed improves by up to 

> **375** 1.23×, and the FLOPs are markedly below the baseline. Further compressing the retention rate to **376** 30–40% maintains an average SR of 94.4–94.8%, yet attains 1.29–1.35× speedup. Notably, VLA- **377** ADP achieves a 99.4% success rate on the Spatial, indicating that VLA-ADP successfully prunes redundant vision tokens while selectively preserving key information in relatively simple spatial 

**Experiments setup.** For simulation, we use LIBERO Liu et al. (2023a) with four suites ( _i.e._ , Spatial, Object, Goal, Long) evaluating spatial understanding, object recognition, goal-directed behaviour, and long-horizon planning. All Libero settings follow OpenVLA-OFT, using its public run scripts. For comparison, we reproduce FastV Chen et al. (2024) on OpenVLA-OFT and run under the same environment. Experiments run on Linux with an NVIDIA RTX 4090. We set the window size to the OpenVLA-OFT chunk size (8) and apply a cold start: the first two windows use full vision. To limit error accumulation, if pruning occurs in three consecutive windows, the next window is forced to full vision. In multi-view pruning, the main wrist retention is 4:6. Within the Action-Aware Dynamic Strategy, we use Euclidean displacement and the adjacent-extrema rule; in its third case we deterministically set the state to 1 (instead of inheriting _sii_ ) to further reduce FLOPs. 

7 

Under review as a conference paper at ICLR 2026 

**378** Table 2: **Real-World Experiments (4 tasks).** Task 1 to Task 4 cover the picking, placing and wiping **379** motion, which covering a variety of objects. **380 381 Method Decoding Task1 Task2 Task3 Task4 Average Latency** _↓_ **Speedup** _↑_ **382** OpenVLA-OFT (base) PD 83.3% **93.3%** 86.7% 80.0% 85.8% 76.9 1.00 **383 VLA-ADP** (ours) PD **90.0%** 90.0% **90.0% 83.3% 88.3% 51.8 1.49** _×_ **384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399** Figure 5: **Real world experiments** . We conduct the experiments on Jaco2 Real-world Platform. **400 401** manipulation scenarios. By contrast, Random Dropping (50%) yields a 1.29× speedup on the LLM **402** side and performs reasonably on the Spatial and Goal, but its success rates on Object and Long are **403** only 73.0% and 76.2%, respectively. **404** 

**405 406** 

### 5.2 REAL-WORLD EXPERIMENTS 

**407 Experiment setup.** We evaluate on four real tasks executed on a physical robot: _Task1_ : pick up **408** the orange pot and place it in the green plate; _Task2_ : place the blue cube on the plate; _Task3_ : place **409** the carrot on the blue pan; _Task4_ : wipe the table. All runtime settings mirror the simulation: Linux **410** workstation with an NVIDIA RTX 4090, parallel decoding (PD) and window size equal to OpenVLA- **411** OFT chunk size (8) with a two-window cold start (full vision). To curb error accumulation, if pruning is enabled for three consecutive windows, the next window uses full vision. Within the Action-Aware **412** Dynamic Strategy we use Euclidean displacement and the adjacent-extrema rule, and in the third case **413** deterministically set the state to 1 to further reduce FLOPs. **414 415 Main result.** Table 2 summarizes the outcomes. VLA-ADP improves the average success rate **416** from 85.8% to 88.3% while reducing latency from 76.9 to 51.8 (baseline/ours = **1** _._ **49** _×_ ). Per task, **417** VLA-ADP outperforms the baseline on Task1/3/4 (90.0%, 90.0%, 83.3%) and is still competitive on Task2 (90.0% vs. 93.3%). These results indicate that our dynamic pruning maintains or improves **418** real-world success while yielding substantial speedup. **419 420 421** 6 ABLATION STUDY **422 423** We conduct ablations on each component of our method: first removing the dynamic strategy to test **424** ADP ( _w/o Action-aware Dynamic_ ); then ablating the pruning module ( _w/o Text-driven Pruning_ ) with **425** different weight selections for relevance scoring. **426 Action-aware Dynamic Strategy.** We assess the impact of the dynamic strategy with two baselines: **427** removing the dynamic function ( _ADP w/o D_ ) and a handcrafted periodic switching variant ( _w/o_ **428** _D + PS_ ). Table 3a (a) shows that introducing the dynamic controller (ADP) yields the best overall **429** accuracy–compute balance: 96.3% average SR with _ρ_<sup>_avg_</sup> = 0 _._ 22 and 6.43 FLOPs, outperforming **430** the variant _w/o D_ (93.45%, _ρ_<sup>_avg_</sup> = 0 _._ 25, 6.23 FLOPs) and the periodic schedule _w/o D + PS_ (89.9%, **431** _ρ_<sup>_avg_</sup> = 0 _._ 50, 4.55 FLOPs). Per-suite, the dynamic policy preserves Goal/Long while boosting Spatial/Object—most notably a **+16.6** point gain on _Object_ over the periodic schedule (98.0% vs. 

8 

Under review as a conference paper at ICLR 2026 

**432** Table 3: **Ablation Study on each component of our design. (a)** Ablation on dynamic strategies ( _f_ ). **433 (b)** Ablation on pruning based on weights retrievaled from layer _l_ . Metrics are SR (%) and FLOPs. **434 435** Spatial Object Goal Long Avg Spatial Object Goal Long Avg _f l_ **436** SR _↑_ SR _↑_ SR _↑_ SR _↑_ SR _↑ ρ_<sup>_avg_</sup> FLOPs _↓_ SR _↑_ SR _↑_ SR _↑_ SR _↑_ SR _↑_ FLOPs _↓_ **437** ADP **99.4% 98.0% 96.4% 91.2% 96.3% 0.22 6.43** 0 **99.4% 98.0% 96.4% 91.2% 96.3% 6.43 438** - w/o D 98.2% 88.0% 96.4% 91.2% 93.45% 0.25 6.23 1 98.2% 97.6% 96.2% 89.8% 95.5% 6.57 - w/o D + PS 95.0% 81.4% 96.2% 87.0% 89.9% 0.50 4.55 4 98.0% 97.8% 96.4% 91.2% 95.8% 6.89 **439 440** (a) (b) **441 442 443 444 445 446 447 448 449 450** (a) Original Attention Maps (b) Pruning Attention Maps. (c) Vision tokens importance score. **451** Figure 6: The figure illustrates the layer-wise importance score of the vision tokens. (a) Vision–vision **452** self-similarity (across layers) (b) Text→vision attention (after ADP) (c) Vision-token importance Φ **453 454** 81.4%), and **+4.4** on _Spatial_ (99.4% vs. 95.0%). Compared to _ADP w/o D_ , ADP improves average **455** SR by **+2.85** points with comparable compute (+0.20 FLOPs), indicating that state-aware switching **456** (rather than fixed cycling) is crucial to avoid over-pruning during fine manipulation while still pruning **457** aggressively when large motions occur. **458** 

**459 Impact of Pruning Strategy.** We ablate layer selection to validate using layer 0 for importance **460** scoring. Table 3b (b) shows that final SR is similar across layers, with layer 0 yielding the best accuracy–compute balance: 96.3% average SR with 6.43 FLOPs, compared to layer 1 (95 _._ 5%, 6 _._ 57 **461** FLOPs) and layer 4 (95 _._ 8%, 6 _._ 89 FLOPs). Meanwhile, FLOPs increase with deeper layers, so **462** selecting _l_ = 0 offers a superior performance–efficiency trade-off. The slight decline in average SR **463** with depth corroborates our analysis: deeper layers induce more localised attention—sharpening **464** peaks vs. non-peaks but reducing global state coverage—thus becoming more sensitive to occasional **465** mismatches and noise, which leads to marginally lower success rates. **466 Observation of Attention Weights.** A common view holds that text–vision alignment concentrates **467** in deeper multimodal layers, so high importance scores should be computed there; however, this need **468** not hold for parallel-decoding VLA. Our visualizations and measurements show that layer 0 already **469** provides a stable, discriminative text-to-vision signal. In Fig. 6a, the layer-0 self-similarity matrix **470** shows a clear high-contrast block structure, while deeper layers become increasingly diagonal-banded, **471** compressing non-local correlations. The text to vision submatrix (Fig. 6b) follows the same trend: **472** layer 0 exhibits pronounced peaks and troughs across many vision tokens, whereas deeper layers **473** retain only a few narrow high-response bands. The token importance score Φ (Fig. 6c) likewise has **474** higher SNR at layer 0; with depth, curves sharpen and develop long tails or near collapse, making **475** top- _k_ ranking more sensitive to local noise. **476 477 478** 7 CONCLUSION **479 480** We presented VLA-ADP, a plug-and-play pruning framework that unifies text-driven anticipatory **481** pruning with an action-aware dynamic strategy to accelerate VLA inference while preserving reliabil- **482** ity. Across simulation and real-world evaluations, the method maintains or improves task success, **483** reduces compute, and shortens inference latency. The dynamic controller consistently outperforms **484** removal and periodic switching, and early-layer scoring offers the best accuracy–efficiency balance. **485** These results indicate that adaptively pruning vision tokens by motion state and instruction relevance enables efficient, fine-grained manipulation without compromising control quality. 

9 

Under review as a conference paper at ICLR 2026 

> **486** REFERENCES **487 488** Anas Awadalla, Irena Gao, Josh Gardner, Jack Hessel, Yusuf Hanafy, Wanrong Zhu, Kalyani Marathe, **489** Yonatan Bitton, Samir Gadre, Shiori Sagawa, et al. Openflamingo: An open-source framework for **490** training large autoregressive vision-language models. _arXiv preprint arXiv:2308.01390_ , 2023. **491** Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, **492** Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist **493** humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. **494 495** Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo **496** Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. A vision-language-action flow model for **497** general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. **498** Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, **499** Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action 

> **500** models transfer web knowledge to robotic control, 2023. _URL https://arxiv. org/abs/2307.15818_ , **501** 2024. **502 503** Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, **504** Hao Luo, Fan Wang, et al. Worldvla: Towards autoregressive action world model. _arXiv preprint_ **505** _arXiv:2506.21539_ , 2025. **506** Liang Chen, Haozhe Zhao, Tianyu Liu, Shuai Bai, Junyang Lin, Chang Zhou, and Baobao Chang. 

> **507** An image is worth 1/2 tokens after layer 2: Plug-and-play inference acceleration for large vision- **508** language models. In _European Conference on Computer Vision_ , pp. 19–35. Springer, 2024. **509 510** Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, **511** and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The_ **512** _International Journal of Robotics Research_ , pp. 02783649241273668, 2023. **513** Chia-Yu Hung, Qi Sun, Pengfei Hong, Amir Zadeh, Chuan Li, U Tan, Navonil Majumder, Soujanya **514** Poria, et al. Nora: A small open-sourced generalist vision language action model for embodied **515** tasks. _arXiv preprint arXiv:2504.19854_ , 2025. **516 517** Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, **518** Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source **519** vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. **520** Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing **521** speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. **522** 

   - Liang Chen, Haozhe Zhao, Tianyu Liu, Shuai Bai, Junyang Lin, Chang Zhou, and Baobao Chang. An image is worth 1/2 tokens after layer 2: Plug-and-play inference acceleration for large visionlanguage models. In _European Conference on Computer Vision_ , pp. 19–35. Springer, 2024. 

- **523** Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, **524** Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational vision-language-action model for **525** synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 

- **526** 

- **527** Ye Li, Yuan Meng, Zewen Sun, Kangye Ji, Chen Tang, Jiajun Fan, Xinzhu Ma, Shutao Xia, Zhi Wang, and Wenwu Zhu. Sp-vla: A joint model scheduling and token pruning approach for vla 

- **528** model acceleration. _arXiv preprint arXiv:2506.12723_ , 2025. 

- **528 529** 

- **530** Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: **531** Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information_ **532** _Processing Systems_ , 36:44776–44791, 2023a. 

- **533** 

- **534** Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. Improved baselines with visual instruction tuning, 2023b. 

- **535** 

- **536** 

   - Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning, 2023c. 

- **537** 

- **538** Haotian Liu, Chunyuan Li, Yuheng Li, Bo Li, Yuanhan Zhang, Sheng Shen, and Yong Jae Lee. **539** Llava-next: Improved reasoning, ocr, and world knowledge, January 2024a. URL https: //llava-vl.github.io/blog/2024-01-30-llava-next/. 

10 

Under review as a conference paper at ICLR 2026 

**540** Jiaming Liu, Mengzhen Liu, Zhenyu Wang, Lily Lee, Kaichen Zhou, Pengju An, Senqiao Yang, **541** Renrui Zhang, Yandong Guo, and Shanghang Zhang. Robomamba: Multimodal state space model **542** for efficient robot reasoning and manipulation. _arXiv e-prints_ , pp. arXiv–2406, 2024b. **543 544** Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, **545** Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: Learning **546** robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. **547** Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zoui- **548** tine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, et al. Smolvla: A vision- **549** language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , **550** 2025. **551** Xudong Tan, Yaoxin Yang, Peng Ye, Jialin Zheng, Bizhe Bai, Xinyi Wang, Jia Hao, and Tao **552** Chen. Think twice, act once: Token-aware compression and action reuse for efficient inference in **553** vision-language-action models. _arXiv preprint arXiv:2505.21200_ , 2025. **554 555** Gemini Team, Rohan Anil, Sebastian Borgeaud, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, **556** Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. Gemini: a family of highly **557** capable multimodal models. _arXiv preprint arXiv:2312.11805_ , 2023. **558** Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay **559** Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation **560** and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. **561 562** Junjie Wen, Yichen Zhu, Jinming Li, Zhibin Tang, Chaomin Shen, and Feifei Feng. Dexvla: **563** Vision-language model with plug-in diffusion expert for general robot control. _arXiv preprint arXiv:2502.05855_ , 2025a. **564 565** Junjie Wen, Yichen Zhu, Minjie Zhu, Zhibin Tang, Jinming Li, Zhongyi Zhou, Xiaoyu Liu, Chaomin **566** Shen, Yaxin Peng, and Feifei Feng. Diffusionvla: Scaling robot foundation models via unified **567** diffusion and autoregression. In _Forty-second International Conference on Machine Learning_ , **568** 2025b. **569** Siyu Xu, Yunke Wang, Chenghao Xia, Dihao Zhu, Tao Huang, and Chang Xu. Vla-cache: Towards **570** efficient vision-language-action model via adaptive token caching in robotic manipulation. _arXiv_ **571** _preprint arXiv:2502.02175_ , 2025. **572 573** Yantai Yang, Yuhao Wang, Zichen Wen, Luo Zhongwei, Chang Zou, Zhipeng Zhang, Chuan Wen, **574** and Linfeng Zhang. Efficientvla: Training-free acceleration and compression for vision-language- **575** action models. _arXiv preprint arXiv:2506.10100_ , 2025. **576** Yang Yue, Yulin Wang, Bingyi Kang, Yizeng Han, Shenzhi Wang, Shiji Song, Jiashi Feng, and Gao **577** Huang. Deer-vla: Dynamic inference of multimodal large language models for efficient robot **578** execution. _Advances in Neural Information Processing Systems_ , 37:56619–56643, 2024. **579 580** Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language **581** image pre-training. In _Proceedings of the IEEE/CVF international conference on computer vision_ , **582** pp. 11975–11986, 2023. **583** Rongyu Zhang, Menghang Dong, Yuan Zhang, Liang Heng, Xiaowei Chi, Gaole Dai, Li Du, Yuan **584** Du, and Shanghang Zhang. Mole-vla: Dynamic layer-skipping vision language action model via **585** mixture-of-layers for efficient robot manipulation. _arXiv preprint arXiv:2503.20384_ , 2025. **586 587** Yuan Zhang, Chun-Kai Fan, Junpeng Ma, Wenzhao Zheng, Tao Huang, Kuan Cheng, Denis Gudovskiy, Tomoyuki Okuno, Yohei Nakata, Kurt Keutzer, et al. Sparsevlm: Visual token sparsifica- **588** tion for efficient vision-language model inference. _arXiv preprint arXiv:2410.04417_ , 2024. **589 590 591 592 593** 

- Yantai Yang, Yuhao Wang, Zichen Wen, Luo Zhongwei, Chang Zou, Zhipeng Zhang, Chuan Wen, and Linfeng Zhang. Efficientvla: Training-free acceleration and compression for vision-languageaction models. _arXiv preprint arXiv:2506.10100_ , 2025. 

11 

Under review as a conference paper at ICLR 2026 

**594 595** 

**596 597** 

**607 608 609 610 611 612 613 614 615 616 617 618 619 620 621 622 623 624 625 626 627 628 629 630 631 632 633 634 635 636 637 638 639 640 641 642 643 644 645 646 647** 

## APPENDIX 

THE USE OF LARGE LANGUAGE MODELS 

**598 599 600 601 602 603 604** 

**605 606** 

In this manuscript, we used a LLM as a writing assistant to refine the presentation of certain contents. Specifically, the LLM was used to: (1) Rephrase sentences and paragraphs for greater readability, conciseness, and academic formality. (2) Correct grammar, spelling, and punctuation errors. (3) Improve logical flow and transitions between sentences. All content enhanced by the LLM has been thoroughly reviewed by the authors to ensure accuracy. The core idea, technical contributions, and results of the experiment are entirely the original contributions of the authors. 

### ALGORITHM 

Here we provide the full pipeline of our proposed action-aware dynamic pruning for vision-languageaction models. 

### **Algorithm 1** Action-Aware Dynamic Pruning (ADP) for VLA Inference 

**Require:** Multimodal embeddings **X**<sup>_m_</sup> =� **X**<sup>[BOS]</sup> _,_ **X**<sup>vis</sup> _,_ **X**<sup>prop</sup> _,_ **X**<sup>txt</sup> _,_ **X**<sup>act</sup> _,_ **X**<sup>[EOS]�</sup> , Q/K weights _WQ_<sup>(0)</sup><sup>_, W_</sup> _K_<sup>(0), retention ratio</sup><sup>_ρ_, view weights</sup><sup>**_α_**</sup><sup>_∈_R</sup><sup>_C_with �</sup> _c_<sup>_αc_=1,</sup> gating rule _f_ ( _·_ ) (mean or adjacent-extrema), windowed actions **A** _i_<sup>_c_, pose</sup><sup>_Tb_</sup> _i_ 

- **Output:** Per-window visual state _si ∈{_ 0 _,_ 1 _}_ , pruned sequence **X**<sup>˜</sup><sup>_m_</sup> , actions ˆ **a** 

- 1: **Init:** _s_ 1 _←_ 0 (cold start, full vision), _s_ 2 _←_ 0; consec _←_ 0 _▷_ two-window cold start 

- 2: **for** window _i_ = 1 _,_ 2 _, . . ._ **do** 

- 3: **Compute windowed motion** _δi_ via FK on **A** _i_<sup>_c_(Def. 4.1):</sup> _ei−_ 1 **v** _i,u_ 

- _δi ←_ � _∥_ **p** _t_ +1 _−_ **p** _t∥_ 2 with **p** _t_ = _π_ ( _Tt_ ) _, Tt_ +1 = _Tt_ **0**<sup>_⊤_</sup> 1 � _Ri,u_ � 

- _t_ = _bi_ 

- 4: **Gate update:** _si_ +1 _← f_ ( _δi_ ) 5: **if** consec _≥_ 3 **then** _▷_ reset to avoid prolonged pruning 6: _si_ +1 _←_ 0; consec _←_ 0 7: **Branch by state** 8: **if** _si_ +1 = 1 **then** _▷_ pruned path 9: **Q/K scoring at layer 0: Q**<sup>(0)</sup> = **H**<sup>(0)</sup> txt<sup>_W_(0)</sup> _Q_<sup>,</sup><sup>**K**(0) =</sup><sup>**H**</sup> vis<sup>(0)</sup><sup>_W_(0)</sup> _K_<sup>,</sup><sup>**A**(0) =</sup><sup>**<u>Q</u>**(0)(</sup> _~~√~~_<sup>**K**</sup> _d_<sup>(0))</sup><sup>_⊤_</sup> 

- 10: **Aggregate importance** (Eq. 9): Φ<sup>(0)</sup> ( _v_ ) _← N_<sup>_h_</sup> <u>1</u> _L_ txt � _h,t_<sup>**A**(0)</sup> _h,t,v_ 11: _k ←⌊ρ · L_<sup>vis</sup> _⌋_ ; _kc ←⌊αc · k⌋_ for _c_ =1 _..C_ 12: **Per-view Top-** _k_ **: X**<sup>vis</sup> ( _c_ )<sup>_←_Top-K(Φ(0)</sup> ( _c_ )<sup>_, kc_);</sup><sup>**X**</sup> keep<sup>vis</sup><sup>_←_�</sup> _c_<sup>**X**vis</sup> ( _c_ ) 13: **Form pruned input: X**<sup>˜</sup><sup>_m_</sup> _←_ [ **X**<sup>[BOS]</sup> _,_ **X**<sup>vis</sup> keep<sup>_,_</sup><sup>**X**prop</sup><sup>_,_</sup><sup>**X**txt</sup><sup>_,_</sup><sup>**X**act</sup><sup>_,_</sup><sup>**X**[EOS]]</sup> 14: **LLM forward: a** ˆ _← f_ LLM( **X**<sup>˜</sup><sup>_m_</sup> ); consec _←_ consec + 1 15: **else** _▷_ full-vision path 

- 16: **X** ˜<sup>_m_</sup> _←_ **X**<sup>_m_</sup> ; **a** ˆ _← f_ LLM( **X**<sup>_m_</sup> ); consec _←_ 0 

- 17: **Execute** ˆ **a** and advance to next window 18: **return** _{si}_ , **X**<sup>˜</sup><sup>_m_</sup> , ˆ **a** 

### REAL-WORLD EXPERIMENT DETAILS 

We provide additional details of the real-robot experiments to facilitate reproducibility. 

**Robot Platform.** All real-world evaluations were conducted on a **Kinova Jaco2** 6-DoF robotic arm equipped with a parallel-jaw gripper. The robot was controlled through Cartesian velocity commands at 10 Hz, with joint and workspace safety limits enforced to prevent collisions. 

12 

Under review as a conference paper at ICLR 2026 

**648 649 650 651 652** 

**653 654 655 656** 

**674 675 676 677 678 679 680 681 682 683 684 685 686 687 688 689 690 691 692 693 694 695 696 697 698 699 700 701** 

**Sensing Setup.** A single RGB camera (Sony AX53) was mounted in front of the table to capture the entire workspace. The camera streamed RGB frames at 640 _×_ 480 resolution and 30 FPS. No wrist-mounted camera was used in the real-robot experiments, and all observations were obtained from this fixed view. 

**Runtime Environment.** All policies were executed on a Linux workstation running Ubuntu 20.04 with an NVIDIA RTX 4090 GPU. Inference employed parallel decoding with an OFT chunk size of 8. Latency was measured as mean per-step inference time over 100 runs. 

> **657 Task Setup.** We evaluated four tabletop manipulation tasks: **a) Task 1:** Pick up the orange pot 

> **658** and place it into a green plate. **b) Task 2:** Pick and place a blue cube onto the plate. **c) Task 3: 659** Pick and place a carrot into a blue pan. **d) Task 4:** Wipe the table. Objects were placed randomly **660** within a 50 _×_ 50 cm workspace area at the beginning of each trial. For data collection, each task was **661** executed using a gamepad teleoperation interface, with the human operator directly controlling the **662** Jaco2 arm. We collected approximately 100–150 trajectories per task, covering diverse initial states **663** and object positions. The collected demonstrations were then used to build the training dataset, and we fine-tuned OpenVLA-OFT separately on each task before deploying the model for evaluation in **664** the real-robot experiments. **665 666 Evaluation Protocol.** Each task was repeated 30 trials under randomized object initializations. **667** A trial was marked as successful if the object was placed entirely within the target receptacle (for **668** Tasks 1–3) or if more than 80% of the designated area was wiped (Task 4). At the end of each episode, **669** the robot was reset to a neutral home pose. Safety termination was triggered if joint torque exceeded **670** preset thresholds. **671 672** QUANTITATIVE STATISTICS **673** 

To complement the attention visualizations with comparable quantitative evidence, we compute scale-free statistics at each layer from the text-to-vision importance vector Φ = _{ϕi}_<sup>_V_</sup> _i_ =1<sup>.We first</sup> normalize Φ as _pi_ = _ϕi/_<sup>�</sup><sup>_V_</sup> _j_ =1<sup>_ϕj_and then evaluate the</sup><sup>_Participation Ratio (PR)_and the</sup><sup>_Entropy_</sup> _(H)_ : 


_PR_ approximates the effective number of participating visual columns, while _H_ quantifies the dispersion and multi-modality of the distribution. Together, they characterize the spatial coverage of alignment signals and the stability of Top- _K_ ranking. 

Figure 7a presents the variation of _PR_ across layers. In shallow layers, _PR_ remains relatively high, indicating that a large number of key vision tokens receive balanced attention and contribute to broad spatial coverage. As depth increases, _PR_ rapidly decreases and stabilizes, reflecting a progressive collapse of attention onto a small subset of tokens and reduced feature utilization. 


Figure 7: Layer-wise statistics of text-to-vision importance scores. 

13 

Under review as a conference paper at ICLR 2026 

**702** Figure 7b presents the corresponding entropy _H_ across layers. Shallow layers exhibit higher entropy, **703** suggesting diverse and smooth distributions that make Top- _K_ selection robust against individual **704** outliers. In contrast, deeper layers display sharply peaked distributions dominated by a few tokens. **705** While such localization may benefit semantic alignment in downstream reasoning, it renders Top- _K_ **706** selection unstable and prone to discarding critical tokens. These findings suggest that shallow-layer **707** attention signals are preferable for estimating the importance of vision tokens in VLA tasks. In **708** particular, using layer-0 offers a computationally efficient choice, providing reliable importance **709** estimates while further reducing FLOPs. **710 711** RANDOM PRUNING COMPARISON **712 713 714 715 716 717 718 719 720 721 722 723 724 725 726 727** Figure 8: ADP (Text-Driven Pruning) vs. Random Pruning. **728 729** Random Pruning yields competitive performance on Spatial and Goal, but performs substantially **730** worse on Object and Long. We can attribute this phenomenon to the distribution of visual patches **731** spanned by the key object as shown in Figure 8. When the target object spans a large number **732** of patches, random pruning still has a high probability of retaining the relevant patches, thereby **733** preserving sufficient task-critical vision information. In contrast, random pruning is more likely to **734** prune the relevant patches when the key object spans only a small number of patches. Such pruning **735** may result in incorrect object identification, which in turn propagates errors and ultimately causes **736** task failure. **737 738** INVERSION EXPERIMENT **739 740** Table 4: Inversion Experiment. **741 742 Keep Ratio=30% Keep Ratio=50% Keep Ratio=70% 743 Task 744** Direct Inverse Gap Direct Inverse Gap Direct Inverse Gap **745** Spatial 97.6% 44.0% 53.6% 99.4% 54.8% 44.6% 99.0% 90.8% 8.2% **746** Object 98.4% 0.6% 97.8% 98.0% 11.8% 86.2% 98.2% 59.6% 38.6% **747** Goal 97.4% 43.6% 53.8% 96.4% 63.6% 32.8% 96.8% 84.8% 12.0% **748** Long 84.2% 0.2% 84.0% 91.2% 8.2% 83.0% 91.2% 37.4% 53.8% **749** Avg 94.4% 22.1% 72.3% 96.3% 34.6% 61.7% 96.3% 68.1% 28.1% **750 751** To further evaluate the reliability of our text-driven importance scores, we design a counterfactual **752** inverse-pruning experiment that mirrors the full setup of the main results. Instead of retaining the **753** most relevant visual tokens identified by our text–vision relevance ranking, we intentionally preserve **754** the least relevant ones, while keeping all other factors, including model, hyperparameters, tasks, and **755** ratios (30%, 50%, 70%), unchanged. If the relevance ranking were noisy or poorly aligned with task semantics, the performance gap between direct and inverse pruning would be small. Conversely, 

14 

Under review as a conference paper at ICLR 2026 

**784** Table 5: FLOPs and speedup with keep ratio 0 _._ 3. ADP(i) denotes pruning based on the weights from **785** the i-th layer. **786 787** Item baseline ADP (0) ADP (2) ADP (4) ADP (8) ADP (16) ADP (24) **788** Keep Ratio 1.0 0.3 0.3 0.3 0.3 0.3 0.3 **789** Scoring Layer – 0 2 4 8 16 24 **790** Seq. Len. 603 245 245 245 245 245 245 **791** Vis. Tokens (kept) 512 154 154 154 154 154 154 **792** Scoring FLOPs (T) 0.00 0.02 0.51 1.01 1.99 3.97 5.95 **793** LLM FLOPs (T) 7.91 3.19 3.19 3.19 3.19 3.19 3.19 **794** Total FLOPs (T) 7.91 3.21 3.70 4.20 5.18 7.16 9.14 Expected FLOPs (T) 7.91 5.85 6.06 6.27 6.71 7.58 8.45 **795** Speedup (Orig/Exp.) 1.00 1.35 1.31 1.26 1.18 1.04 0.94 **796 797** 

**756** a large and systematic divergence would indicate that the scoring mechanism faithfully captures **757** task-relevant visual information. **758 759** The results in Table 4 show a clear and consistent separation between the two settings across all suites **760** and keep ratios. Under a 30% keep ratio, the average success rate drops sharply from 94.4% (direct) to 22.1% (inverse), with near-complete failure on Object (0.6%) and Long (0.2%). Similar trends **761** persist at 50% (from 96.3% to 34.6%) and 70% (from 96.3% to 68.1%). Notably, inverse-70% still **762** performs far worse than direct-30%, highlighting that semantic relevance dominates task performance **763** over the number of retained tokens. **764 765** Noteably, the degradation is particularly pronounced on Object and Long, which require fine-grained **766** spatial reasoning and long-horizon planning. Under inverse pruning, the model effectively loses access to the high-ranked, task-relevant visual tokens used for object grounding, spatial reasoning, **767** and contact-rich motion planning. This confirms that our importance scores do not drift toward **768** irrelevant regions but consistently identify and prioritise semantically aligned visual tokens. **769 770** Taken together, these counterfactual results provide strong evidence that: **771** 1. Task-relevant visual tokens play a decisive role in VLA tasks, and task success depends **772** far more on preserving these semantically aligned tokens than on the number of tokens **773** retained. Task performance collapses as soon as these high-relevance tokens are removed, **774** demonstrating that semantic alignment is the dominant factor governing model behaviour. **775** 2. The text-driven relevance scoring mechanism accurately identifies and prioritises essential **776** visual tokens, showing that ADP’s anticipatory pruning relies on a stable and meaningful **777** semantic signal rather than incidental attention fluctuations. The scoring module effectively **778** captures the alignment between the task instruction and the image observations, precisely **779** identifying the visual patches critical for object grounding, spatial reasoning, and contact- **780** rich manipulation. **781 782** COMPUTATIONAL TRADE-OFF ANALYSIS **783** 

2. The text-driven relevance scoring mechanism accurately identifies and prioritises essential visual tokens, showing that ADP’s anticipatory pruning relies on a stable and meaningful semantic signal rather than incidental attention fluctuations. The scoring module effectively captures the alignment between the task instruction and the image observations, precisely identifying the visual patches critical for object grounding, spatial reasoning, and contactrich manipulation. 

|**798**<br>**799**<br>**800**|Table 6: FLOPs and speedup with keep ratio <br>the i-th layer.|0_._4. ADP(i) denotes pruning based on the weights from|
|---|---|---|
|**801**|Item<br>baseline<br>ADP (0)|ADP (2)<br>ADP (4)<br>ADP (8)<br>ADP (16)<br>ADP (24)|
|**802**|Keep Ratio<br>1.0<br>0.4|0.4<br>0.4<br>0.4<br>0.4<br>0.4|
|**803**|Scoring Layer<br>–<br>0|2<br>4<br>8<br>16<br>24|
|**804**|Seq. Len.<br>603<br>296|296<br>296<br>296<br>296<br>296|
|**805**|Vis. Tokens (kept)<br>512<br>205|205<br>205<br>205<br>205<br>205|
|**806**|Scoring FLOPs (T)<br>0.00<br>0.02<br>LLM FLOPs (T)<br>7.91<br>3.86|0.51<br>1.01<br>1.99<br>3.97<br>5.95<br>3.86<br>3.86<br>3.86<br>3.86<br>3.86|
|**807**|Total FLOPs (T)<br>7.91<br>3.88|4.37<br>4.86<br>5.85<br>7.83<br>9.80|
|**808**|Expected FLOPs (T)<br>7.91<br>6.14|6.35<br>6.57<br>7.00<br>7.87<br>8.74|
|**809**|Speedup (Orig/Exp.)<br>1.00<br>1.29|1.25<br>1.20<br>1.13<br>1.00<br>0.90|


15 

Under review as a conference paper at ICLR 2026 

**810** Table 7: FLOPs and speedup with keep ratio 0 _._ 5. ADP(i) denotes pruning based on the weights from **811** the i-th layer. **812 813** Item baseline ADP (0) ADP (2) ADP (4) ADP (8) ADP (16) ADP (24) **814** Keep Ratio 1.0 0.5 0.5 0.5 0.5 0.5 0.5 **815** Scoring Layer – 0 2 4 8 16 24 **816** Seq. Len. 603 347 347 347 347 347 347 **817** Vis. Tokens (kept) 512 256 256 256 256 256 256 **818** Scoring FLOPs (T) 0.00 0.02 0.51 1.01 1.99 3.97 5.95 LLM FLOPs (T) 7.91 4.53 4.53 4.53 4.53 4.53 4.53 **819** Total FLOPs (T) 7.91 4.55 5.04 5.53 6.52 8.50 10.47 **820** Expected FLOPs (T) 7.91 6.43 6.64 6.89 7.30 8.17 9.04 **821** Speedup (Orig/Exp.) 1.00 1.23 1.19 1.15 1.08 0.97 0.87 **822 823 824** Table 8: FLOPs and speedup with keep ratio 0 _._ 6. **825 826** Item baseline ADP (0) ADP (2) ADP (4) ADP (8) ADP (16) ADP (24) **827** Keep Ratio 1.0 0.6 0.6 0.6 0.6 0.6 0.6 **828** Scoring Layer – 0 2 4 8 16 24 Seq. Len. 603 399 399 399 399 399 399 **829** Vis. Tokens (kept) 512 308 308 308 308 308 308 **830** Scoring FLOPs (T) 0.00 0.02 0.51 1.01 1.99 3.97 5.95 **831** LLM FLOPs (T) 7.91 5.21 5.21 5.21 5.21 5.21 5.21 **832** Total FLOPs (T) 7.91 5.23 5.72 6.22 7.20 9.18 11.16 **833** Expected FLOPs (T) 7.91 6.74 6.94 7.16 7.60 8.47 9.34 **834** Speedup (Orig/Exp.) 1.00 1.17 1.14 1.10 1.04 0.93 0.85 **835** 

#### **836** 

#### **837** 

### TRADE-OFF OF PRUNING. 

#### **838** 

**839** To quantify the computational trade-off introduced by anticipatory pruning, we evaluate the FLOPs **840** associated with importance scoring and compare them against the savings obtained from reducing the **841** LLM sequence length. Tables 5-9 report detailed FLOPs measurements across a range of keep ratios **842** and scoring layers (all FLOPs reported in this section are computed under the original multimodal **843** sequence length of _S_ = 603.) 

**844** Across all practically meaningful configurations, the scoring cost remains substantially smaller than **845** the compute saved by pruning. When importance ranking is performed using shallow layers (e.g. **846** layers 0–4), the scoring overhead remains within 0.02–1.01T FLOPs. In contrast, shortening the **847** visual sequence reduces the LLM compute from 7.91T to approximately 3.19–5.90T, yielding a 2–4T **848** reduction. The net effect is therefore dominated by the savings from operating on a shorter sequence, **849** and the overall inference cost decreases consistently. **850** When combined with the action-aware dynamic gating strategy, the expected inference cost reflects the **851** mixture of pruned and full-vision windows. In our implementation, the dynamic gate activates pruning **852** for roughly 44% of windows on average across LIBERO. Under this regime, the expected FLOPs per **853** forward become 5.85T (keep=0.3), 6.14T (keep=0.4), and 6.43T (keep=0.5), corresponding to 1.35 _×_ , **854** 1.29 _×_ , and 1.23 _×_ speedup over the baseline. These values already account for the scoring overhead, **855** confirming that the computational benefit persists under realistic usage. **856 857** OBSERVATION ON GATING RULES. **858** 

> **859** We also observe that performing relevance scoring at excessively deep layers ( _≥_ 16) increases the 

> **860** overhead to 3.97–5.95T FLOPs, which approaches or surpasses the FLOPs saved by pruning. In **861** such cases, the net speedup degrades and may even become slightly negative. However, this config is **862** not required in practice. Our ablation study already shows that layer-0 scoring not only minimises **863** computational overhead but also provides the most reliable and stable importance estimates, making it the default choice in all experiments. 

16 

Under review as a conference paper at ICLR 2026 

**864 865 866 867 868 869 870 871 872 873 874 875 876 877 878 879 880 881 882 883 884 885 886 887 888 889 890 891 892 893 894 895 896 897 898** 

Table 9: FLOPs and speedup with keep ratio 0 _._ 7. 

|Item|baseline|ADP (0)|ADP (2)|ADP (4)|ADP (8)|ADP (16)|ADP (24)|
|---|---|---|---|---|---|---|---|
|Keep Ratio|1.0|0.7|0.7|0.7|0.7|0.7|0.7|
|Scoring Layer|–|0|2|4|8|16|24|
|Seq. Len.|603|450|450|450|450|450|450|
|Vis. Tokens (kept)|512|359|359|359|359|359|359|
|Scoring FLOPs (T)|0.00|0.02|0.51|1.01|1.99|3.97|5.95|
|LLM FLOPs (T)|7.91|5.88|5.88|5.88|5.88|5.88|5.88|
|Total FLOPs (T)|7.91|5.90|6.39|6.89|7.88|9.85|11.83|
|Expected FLOPs (T)|7.91|7.03|7.24|7.46|7.89|8.76|9.63|
|Speedup (Orig/Exp.)|1.00|1.13|1.09|1.06|1.00|0.90|0.82|


Overall, the additional scoring computation is far smaller than the savings achieved through reduced sequence length for all practical settings, and the use of shallow-layer scoring ensures that the trade-off remains consistently positive. These results verify that the proposed pruning strategy offers genuine computational benefits without compromising performance. 

### CASE DISCUSSIONS 


Figure 9: Baseline Failed but Ours Success on _#Episode 110_ of Spatial task. 

### OBSERVATION ON INTRIGUING PHENOMENON. 

**899** We observe an intriguing phenomenon: in several scenarios, the pruned model performs even better **900** than the original baseline. To better understand this behavior, we further examine representative cases **901** and analyze the underlying factors that contribute to such improvements. We identify a representative **902** case that illustrates why moderate pruning can outperform the unpruned baseline. In Figure. 9 (a), **903** the baseline model fails to grasp the bowl, whereas in Figure. 9 (b) our ADP method succeeds with a stable grasp. A closer inspection shows that the baseline allocates non-trivial attention to **904** large, static background surfaces, effectively behaving like “sink" regions that dilute focus. After **905** pruning these low-value background tokens, the model concentrates its attention on the immediate **906** manipulation region—specifically the bowl and its supporting surface. This reduction of peripheral **907** noise results in a more discriminative and task-aligned visual representation, helping the policy make **908** more precise action decisions. Thus, in cases where background clutter dominates the unpruned **909** attention distribution, pruning can improve operational focus and lead to higher success rates than the **910** original baseline. **911** In addition to the individual cases discussed above, we further examined the per-task performance **912** differences between ADP (keep ratio 0.5) and the OpenVLA-OFT baseline across all LIBERO suites, **913** as reported in Tables 10–13. We observe that almost all degeneration are concentrated in the Long **914** suite. In contrast, the Spatial, Object, and Goal suites remain largely unaffected, with success rates that **915** are nearly identical to or slightly higher than the baseline. Notably, the most substantial degradations **916** in the Long suite correspond to tasks with particularly long and compositional instructions, often **917** involving multiple sequential subtasks. These tasks require the model to reallocate visual attention across distinct stages, each with its own set of relevant objects and fine-grained spatial relationships. 

17 

Under review as a conference paper at ICLR 2026 

**918 919 920 921 922 923 924 925 926** (a) Baseline (b) Ours **927 928** Figure 10: Per-stage curves drawn by Baseline and ADP. **929 930** Table 10: Spatial Suite Performance (ADP vs Baseline). **931 932 Task Length ADP Baseline Gap 933 934** pick up the black bowl between the plate and the 82 100.0% 100.0% 0.0% **935** ramekin and place it on the plate pick up the black bowl next to the ramekin and 68 100.0% 100.0% 0.0% **936** place it on the plate **937** pick up the black bowl from table center and 66 100.0% 100.0% 0.0% **938** place it on the plate **939** pick up the black bowl on the cookie box and 66 100.0% 98.0% +2.0% **940** place it on the plate **941** pick up the black bowl in the top drawer of the 88 98.0% 94.0% +4.0% **942** wooden cabinet and place it on the plate **943** pick up the black bowl on the ramekin and place 63 98.0% 100.0% -2.0% **944** it on the plate **945** pick up the black bowl next to the cookie box 71 100.0% 100.0% 0.0% **946** and place it on the plate pick up the black bowl on the stove and place it 61 98.0% 98.0% 0.0% **947** on the plate **948** pick up the black bowl next to the plate and 66 100.0% 100.0% 0.0% **949** place it on the plate **950** pick up the black bowl on the wooden cabinet 70 100.0% 96.0% +4.0% **951** and place it on the plate **952 953 954 955** Such behaviour reveals an intrinsic challenge of current VLA backbones. Since models like **956** OpenVLA-OFT condition action generation solely on the current multi-modal sequence and static **957** instruction, they lack explicit awareness of subtask completion. As a result, even after the first subgoal **958** has been completed, the text-driven relevance scoring may continue to assign high importance to **959** visual tokens associated with the earlier subgoal. Our inversion experiment demonstrated that VLA performance is extremely sensitive to the availability of correct visual tokens. Therefore, pruning **960** under a limited token budget can amplify this issue, as tokens tied to an already completed subtask **961** may still be retained due to textual relevance. In contrast, the subsequent subtask may receive insuffi- **962** cient visual coverage, which can ultimately lead to failure. These observations suggest that future **963** progress may require enhancing VLA models with mechanisms for estimating subgoal progress or **964** dynamically reallocating visual attention across long-horizon, multi-stage tasks. **965 966 967** IMPLEMENTATION DETAILS **968** 

**969 Hyperparameters.** We provide here the full set of hyperparameters used in our main experiments **970** for reproducibility. These include all query–key (QK) pruning settings, dynamic gating parameters, **971** and visualization options. Table 14 summarizes the exact values used in all results reported in the main text. 

18 

Under review as a conference paper at ICLR 2026 

**972** Table 11: Object Suite Performance (ADP vs Baseline). **973 974 Task Length ADP Baseline Gap 975** pick up the alphabet soup and place it in the 52 100.0% 98.0% +2.0% **976** basket **977** pick up the cream cheese and place it in the 51 100.0% 100.0% 0.0% **978** basket **979** pick up the salad dressing and place it in the 53 98.0% 98.0% 0.0% **980** basket **981** pick up the bbq sauce and place it in the basket 48 98.0% 100.0% -2.0% **982** pick up the ketchup and place it in the basket 46 98.0% 100.0% -2.0% **983** pick up the tomato sauce and place it in the 51 100.0% 100.0% 0.0% **984** basket **985** pick up the butter and place it in the basket 45 96.0% 98.0% -2.0% **986** pick up the milk and place it in the basket 43 98.0% 96.0% +2.0% pick up the chocolate pudding and place it in the 56 94.0% 92.0% +2.0% **987** basket **988** pick up the orange juice and place it in the 51 98.0% 100.0% -2.0% **989** basket **990 991** Table 12: Goal Suite Performance (ADP vs Baseline). **992 993 Task Length ADP Baseline Gap 994 995** open the middle drawer of the cabinet 37 100.0% 98.0% +2.0% **996** put the bowl on the stove 25 94.0% 96.0% -2.0% **997** put the wine bottle on top of the cabinet 41 94.0% 92.0% +2.0% **998** open the top drawer and put the bowl inside 43 82.0% 88.0% -6.0% **999** put the bowl on top of the cabinet 34 100.0% 100.0% 0.0% push the plate to the front of the stove 40 98.0% 100.0% -2.0% **1000** put the cream cheese in the bowl 32 98.0% 96.0% +2.0% **1001** turn on the stove 17 100.0% 100.0% 0.0% **1002** put the bowl on the plate 25 98.0% 98.0% 0.0% **1003** put the wine bottle on the rack 31 100.0% 98.0% +2.0% **1004 1005 1006 Code Availability.** Following the reviewer’s encouragement, we additionally provide a complete **1007** recipe of all hyperparameters, configuration files, and controller settings. Our implementation **1008** exposes all gating and pruning parameters through a unified configuration interface, making it easy **1009** to reproduce and extend the experiments (e.g., varying window sizes, pruning ratios, and similarity **1010** layers). **1011 1012 1013 1014 1015 1016 1017 1018 1019 1020 1021 1022 1023 1024 1025** 

19 

Under review as a conference paper at ICLR 2026 

|**1026**<br>**1027**<br>**1028**<br>**1029**<br>**1030**<br>**1031**<br>**1032**<br>**1033**<br>**1034**|Table 13: Long Suite Perfor|mance (AD|P vs Baselin|e).||
|---|---|---|---|---|---|
|**1035**|**Task**|**Length**|**ADP**|**Baseline**|**Gap**|
|**1036**|put both the alphabet soup and the tomato sauce|61|94.0%|92.0%|+2.0%|
|**1037**|in the basket|||||
|**1038**<br>**1039**|put both the cream cheese box and the butter in<br>the basket|58|96.0%|96.0%|0.0%|
|**1040**<br>**1041**<br>|turn on the stove and put the moka pot on it<br>put the black bowl in the bottom drawer of the<br>cabinet and close it|44<br>67|100.0%<br>96.0%|98.0%<br>94.0%|+2.0%<br>+2.0%|
|**1042**<br>**1043**|put the white mug on the left plate and put the<br>|87|70.0%|100.0%|-30.0%|
||yellow and white mug on the right plate|||||
|**1044**<br>|<br>pick up the book and place it in the back|66|92.0%|100.0%|-8.0%|
|**1045**|compartment of the caddy|||||
|**1046**<br>|<br>put the white mug on the plate and put the<br>|86|80.0%|98.0%|-18.0%|
|**1047**|chocolate pudding to the right of the plate|||||
|**1048**|<br>put both the alphabet soup and the cream cheese<br>|65|98.0%|98.0%|0.0%|
|**1049**|box in the basket|||||
|**1050**|put both moka pots on the stove|31|92.0%|80.0%|+12.0%|
|**1051**|put the yellow and white mug in the microwave|58|94.0%|92.0%|+2.0%|
|**1052**|and close it|||||
|**1053**||||||
|**1054**||||||
|**1055**||||||
|**1056**||||||
|**1057**||||||
|**1058**||||||
|**1059**||||||
|**1060**||||||
|**1061**||||||
|**1062**||||||
|**1063**||||||
|**1064**||||||
|**1065**||||||
|**1066**<br>**1067**|Table 14: Complete hyperparameter coni|figuration u|i sed in all ma|i    in experimen|i     ts.|
|**1068**|**QK-related Param**<br>**Value**<br>**Dynamic Param**||**Value**<br>**Viz/E**|**val Param**|**Value**|
|**1069**|qk_keep_enabled<br>true<br>use_dynamic_visual_str<br>qklayer<br>0<br>decisionmethod|ategy|true<br>num_<br>adjacent<br>over|trials_per_ta<br>layprunedco|sk<br>50<br>lor<br>[00255]|
|**1070**|_<br><br>_<br>qk_keep_ratio<br>0.5<br>adjacent_variant<br>kklit<br>04 06<br>dttid||extrema<br>over<br>3<br>id|__<br>lay_pruned_al<br>f|,,<br>pha<br>120<br>10|
|**1071**|q_eep_sp<br>[., .]<br>ajacen_exrema_wno<br>random_keep_ratio<br>0.5<br>adjacent_lookback<br>|w|ve<br>2|o_ps||
|**1072**|random_state_prob<br>0.5<br>delta_method||net|||
||random_seed<br>42<br>limit_consecutive_prun|ed_enabled|true|||
|**1073**|limit_max_consecutive_|pruned|3|||
|**1074**||||||
|**1075**||||||
|**1076**||||||
|**1077**||||||
|**1078**||||||
|**1079**||||||


20 

