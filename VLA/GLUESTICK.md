---
title: "Don't Run with Scissors : Pruning Breaks VLA Models but They Can Be Recovered"
venue: "Submitted to ICLR 2026"
original: "ICLR 2026 投稿時の匿名版"
url: https://arxiv.org/abs/2510.08464
pdf: https://arxiv.org/pdf/2510.08464
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2510.08464)** / [論文ページ](https://arxiv.org/abs/2510.08464)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。
> ICLR 2026 投稿時の匿名版から変換しました。リンク先の公開版とは内容が異なる場合があります。

Under review as a conference <u>paper</u> at ICLR 2026 

**000 Don’t Run with Scissors :** Pruning Breaks **001 002** VLA Models but They Can Be Recovered **003 004 005 Anonymous authors 006** Paper under double-blind review **007 008 009** Abstract **010 011** Vision–Language–Action (VLA) models have advanced robotic capabilities **012** but remain challenging to deploy on resource-limited hardware. Pruning **013** has enabled efficient compression of large language models (LLMs), yet it **014** is largely understudied in robotics. Surprisingly, we observe that pruning **015** VLA models leads to drastic degradation and increased safety violations. **016** We introduce **GLUESTICK** , a post-pruning recovery method that re- **017** stores much of the original model’s functionality while retaining sparsity **018** benefits. Our method performs a one-time interpolation between the dense **019** and pruned models in weight-space to compute a corrective term. This **020** correction is used during inference by each pruned layer to recover lost capabilities with minimal overhead. GLUESTICK requires no additional **021** training, is agnostic to the pruning algorithm, and introduces a single hy- **022** perparameter that controls the tradeoff between efficiency and accuracy. **023** Across diverse VLA architectures and tasks in manipulation and naviga- **024** tion, GLUESTICK achieves competitive memory efficiency while substan- **025** tially recovering success rates and reducing safety violations. Videos, code, **026** and additional materials are in: **https://gluestick-vla.github.io/** . **027 028 Task:** Enter the dining room and walk to the other end. **Task:** Put the bowl on top of the cabinet. **029 030 031 032 033 034 035 036 037 038 039 040 Pruned VLA GLUESTICK 041** Figure 1: **VLAs break under pruning, and GLUESTICK fixes them.** Pruning **042** methods unexpectedly cause task and safety failures in VLAs: colliding with an object in **043** a navigation task **(left)** , or dropping a bowl in a manipulation task **(right)** . Our post- **044** pruning method, GLUESTICK, restores the lost functionality of the original model. **045 046** 1 Introduction **047 048** Vision-Language-Action (VLA) models mark a new era in robotics. Earlier approaches to **049** robot control used pipelines that separated perception, planning, and control into distinct **050** subsystems. VLAs instead integrate these components into a single end-to-end framework, **051** leveraging large language models (LLMs) to connect perception and natural language in- **052** structions directly to action (Kim et al., 2024; Li et al., 2024; Lee et al., 2025; Black et al., **053** 2024; Bjorck et al., 2025; Brohan et al., 2022; Zitkovich et al., 2023). VLAs learn generalized action policies from internet-scale robotics data, enabling them to transfer across diverse 

1 

Under review as a conference <u>paper</u> at ICLR 2026 

**054** tasks and environments (O’Neill et al., 2024). VLAs can also take advantage of pretrained **055** vision and language models, giving them rich semantic knowledge while grounding behavior **056** in real-world observations (Achiam et al., 2023; Team et al., 2023; Betker et al., 2023). **057 058** The growing capabilities of VLAs come at a cost. As in LLMs, VLAs follow a scaling trend **059** wherein their capabilities grow as the size of the model grows larger (Kaplan et al., 2020). In robotics, this scaling is especially consequential because deployment typically occurs on **060** hardware with strict limits on memory, power, and throughput. For example, an industry- **061** standard Jetson Orin NX provides only 8–16GB of shared CPU-GPU memory (Liu et al., **062** 2024b; Rey et al., 2025), far below server-grade GPUs used for foundation models, such as **063** the NVIDIA HGX B200 with 180GB of memory (NVIDIA, 2025). Such limitations make **064** _compression_ necessary to fit models on resource-constrained hardware. Yet a clear gap **065** remains in understanding how efficiency gains from compression intersect with VLA model **066** success and safety _—a gap this work directly seeks to answer, specifically about pruning._ **067** _Pruning_ is a key compression technique for large language models (Frantar & Alistarh, **068** 2023; Sun et al., 2023a;b). It produces smaller models and more efficient GPU execution **069** with optimized sparse kernels by removing unnecessary weights and enforcing structured **070** sparsity. However, we surprisingly observe that pruning introduces unique challenges for **071** VLAs. Whereas pruning techniques are effective for LLMs, applying the same methods to **072** VLAs leads to catastrophic degradation. In our experiments, recent pruning algorithms **073** reduced task success rate on manipulation tasks from 85.2% to 0.0% and on a navigation **074** task from 43.0% to 0.0%, while also increasing the frequency of safety violations. **075** We recover success rates and reduce safety violations by introducing **GLUESTICK** , a new **076** post-pruning recovery method that recovers signal lost during pruning while preserving the **077** efficiency benefits of sparsity. GLUESTICK operates entirely in weight space, using the **078** information discarded by pruning to nudge the model back toward more performant regions **079** without any retraining. This is achieved by adding a lightweight correction term, computed **080** from singular values in the gap between the dense and pruned weights. **081** Our approach is pruning-agnostic and can be applied on top of any existing pruning algo- **082** rithm. In doing so, GLUESTICK restores up to 100% of performance in navigation tasks **083** and as much as 60% in dexterous manipulation domains, while maintaining the efficiency **084** gains of structured sparsity (Figure 1). Finally, GLUESTICK introduces a single inter- **085** pretable hyperparameter that allows practitioners to directly control the trade-off between **086** accuracy and efficiency, making it adaptable to diverse application requirements. We demon- **087** strate that our method consistently recovers performance and improves safety across three VLA architectures, two widely used robotics benchmarks, and multiple robot embodiments. **088 089 Our contributions. 090 091** • **Empirical evidence of pruning collapse in VLAs.** We present the first systematic **092** study showing that pruning, which is effective for LLMs, causes near-complete collapse of **093** the success rate in embodied VLA models, and an increase in safety violations. **094** • **Study of why VLAs differ from LLMs under pruning.** Through spectral analysis, **095** we identify structural properties of VLA architectures that could make them more fragile **096** to pruning than language-only models. **097** • **An effective, training-free recovery method.** We propose GLUESTICK, a post- **098** pruning recovery algorithm that restores lost signal after pruning using a low-rank, **099** lightweight correction in weight space. GLUESTICK is pruning-algorithm-agnostic, re- **100** quires no retraining, and introduces only a single interpretable hyperparameter. **101 102** 2 Related Work & Motivation **103 104 VLA Models.** Recent work has focused on developing VLA models that unify perception, **105** language understanding, and decision-making into a single policy mapping multimodal in- **106** puts directly to robot actions. These models typically consist of three components: a vision **107** backbone, a multimodal projector, and a language backbone. For instance, given image observations and natural language instructions, OpenVLA (Kim et al., 2024) outputs end- 

- The growing capabilities of VLAs come at a cost. As in LLMs, VLAs follow a scaling trend wherein their capabilities grow as the size of the model grows larger (Kaplan et al., 2020). In robotics, this scaling is especially consequential because deployment typically occurs on hardware with strict limits on memory, power, and throughput. For example, an industrystandard Jetson Orin NX provides only 8–16GB of shared CPU-GPU memory (Liu et al., 2024b; Rey et al., 2025), far below server-grade GPUs used for foundation models, such as the NVIDIA HGX B200 with 180GB of memory (NVIDIA, 2025). Such limitations make _compression_ necessary to fit models on resource-constrained hardware. Yet a clear gap remains in understanding how efficiency gains from compression intersect with VLA model success and safety _—a gap this work directly seeks to answer, specifically about pruning._ 

2 

Under review as a conference <u>paper</u> at ICLR 2026 

**108** 4 **109 Model Method Succ. Unsafe** [VLA] OpenVLA [LLM] Llama 2 **110** OpenVLA Dense 85.2% 33.4% 3 [VLM] Qwen2 VL **111** Magnitude 0.0% 46.4% **112** Wanda 0.0% 51.6% 2 **113 114** NaVILA Dense 43.0% 23.0% 1 **115** Magnitude 0.0% 100.0% Wanda 0.0% 46.0% **116** 0 0 1000 2000 3000 **117** Singular Component Index **118 119** Table 1: **Success and unsafe-episode rate** Figure 2: **Singular value spectra of 120 across pruning strategies.** Succ.=% success- **weights** . VLA vs. LLM/VLM showing **121** ful episodes; Unsafe=% with a safety violation. that VLA spectra are flatter and signal is more dispersed across the weight space. **122 123 124** effector poses and gripper commands for manipulation, while NaVILA (Cheng et al., 2025a) **125** generates velocity commands for navigation. Other prominent systems in this space include **126** RT (Brohan et al., 2022; Zitkovich et al., 2023), the _π_ series (Black et al., 2024; Intel- **127** ligence et al., 2025), PaLM-E (Driess et al., 2023), Gr00t N1 (Bjorck et al., 2025), and **128** CogACT (Li et al., 2024), all of which share the commonality of being large end-to-end **129** transformer-based policies with billions of parameters. Their size poses a particular chal- **130** lenge for robotics, which have tight resource contraints (Jabbour & Janapa Reddi, 2024), making compression techniques such as pruning especially important for deployment. Exac- **131** erbating this challenge, there is a clear trend toward richer inputs and outputs: for example, **132** SpatialVLA (Qu et al., 2025) incorporates not only image token inputs but also 3D scene **133** information, while MolmoAct (Lee et al., 2025) and WorldVLA (Cen et al., 2025) extend **134** outputs beyond action vectors to include depth predictions or full world models. These **135** expansions further grow model size and demand, underscoring the importance of studying **136** efficiency–success trade-offs in compressed VLA models for practical robotic deployment. **137 Pruning Benefits for Robotics.** Pruning is a common technique for compressing LLMs, **138** where a fraction of weights are set to zero (Zhu et al., 2024). Magnitude (Han et al., 2015) **139** and Wanda (Sun et al., 2023b) are widely used pruning methods, valued for being training- **140** free and computationally efficient. Magnitude removes small-magnitude weights, while **141** Wanda scores connections by activation statistics on calibration inputs and prunes those **142** deemed less important. Pruning reduces both parameter count and FLOPs while often pre- **143** serving accuracy, and is especially effective when applied in hardware-friendly patterns such **144** as structured “N:M” sparsity (e.g., 2:4). Modern GPUs exploit these patterns with special- **145** ized kernels that reduce memory traffic and multiply-accumulate operations (MACs) (Cheng **146** et al., 2025b); for example, NVIDIA’s Sparse Tensor Cores and cuSPARSELt accelerate 2:4 **147** sparseto pruninggeneralnotmatrixonly enablesmultiplicationsacceleration(Mishraand etmemoryal., 2021).savingsThebutreducedalso significantlycomputation cutsdue **148** power consumption (Han et al., 2016). These benefits are especially attractive for robotics, **149** where devices operate under strict constraints on compute, memory, and energy, making it **150** critical to also understand pruning’s broader impact on VLA model success and safety. **151 152 Pruning Impacts.** When pruning methods are applied to LLMs they achieve strong accu- **153** racy retention. On LLaMA-2-70B (Touvron et al., 2023), mean accuracy on the EleutherAI LM Harness (Gao et al., 2021) decreases by only 7.13% with Magnitude pruning and 2.94% **154** with Wanda (Sun et al., 2023b), despite imposing a strict 2:4 structured sparsity on the **155** original model and removing 50% of weights. More recent work has investigated the impact **156** of pruning on Vision-Language Models (VLMs) and has shown a larger accuracy decrease **157** compared to LLMs. For example, Koike-Akino et al. (2025) reported that on the ScienceQA **158** dataset, LLaVA-7B experienced a 12.5% accuracy drop after being pruned with Wanda at **159** 50% sparsity on image-based tasks. Similarly, Liang et al. (2025) observed a 9%–30% ac- **160** curacy drop in LLaVA-SQA-7B and LLaVA-v1.5-7B. These foundational pieces of work **161** illustrate that pruning has a measurable impact on VLMs, and our work builds on this observation to explore whether this trend continues or changes for VLA models. Taken 

effector poses and gripper commands for manipulation, while NaVILA (Cheng et al., 2025a) generates velocity commands for navigation. Other prominent systems in this space include RT (Brohan et al., 2022; Zitkovich et al., 2023), the _π_ series (Black et al., 2024; Intelligence et al., 2025), PaLM-E (Driess et al., 2023), Gr00t N1 (Bjorck et al., 2025), and CogACT (Li et al., 2024), all of which share the commonality of being large end-to-end transformer-based policies with billions of parameters. Their size poses a particular challenge for robotics, which have tight resource contraints (Jabbour & Janapa Reddi, 2024), making compression techniques such as pruning especially important for deployment. Exacerbating this challenge, there is a clear trend toward richer inputs and outputs: for example, SpatialVLA (Qu et al., 2025) incorporates not only image token inputs but also 3D scene information, while MolmoAct (Lee et al., 2025) and WorldVLA (Cen et al., 2025) extend outputs beyond action vectors to include depth predictions or full world models. These expansions further grow model size and demand, underscoring the importance of studying efficiency–success trade-offs in compressed VLA models for practical robotic deployment. 

3 

Under review as a conference <u>paper</u> at ICLR 2026 

**162 163 Pruning      (Offline) 164 165 166** Iterate Through **Any** Pruning **167** Linear Layers Algorithm **168 169 VLA Model Dense Layer 2:4 Pruned Layer 170 171 GLUESTICK      (Offline) 172 V**<sup>**T**</sup> **173 174 U** Compute Lost Dominant **175** Weight Space Directions **176 177 Lightweight 178 Compute Gap Matrix Correction Terms 179 180 GLUESTICK      (Online) 181 V**<sup>**T**</sup> **182 183 Layer Output U 184 Activation 185 186 2:4 Pruned Layer** Input **Lightweight** Input **187 Correction Terms 188 189** Figure 3: **Overview of GLUESTICK. (Top)** A VLA model is pruned with a standard **190** algorithm (e.g., Wanda) to enforce 2:4 sparsity in linear layers. **(Middle)** Offline, we compute the gap between the dense and pruned weights and extract dominant lost directions **191** via SVD, yielding lightweight corrections. **(Bottom)** At inference time, these correction **192** terms are applied alongside the pruned weights, effectively adding back lost signal. **193 194 195** together, this line of work suggests that while pruning has been validated on LLMs, it can **196** lead to greater degradation in VLM performance. Therefore, weight adjustments cannot be **197** assumed to be benign in all contexts. In robotics, where VLAs must balance efficiency with **198** both task success and safety, the implications of pruning remain unexplored. No prior work **199** has examined how pruning affects VLA success or safety and how such impacts might be **200** recovered. Direct weight-space interventions for post-pruned VLAs are similarly underex- **201** plored. In this paper, we address this gap by analyzing pruning’s effect on VLA models and **202** introducing a training-free recovery method that restores both success and safety. **203 204** 3 GLUESTICK **205 206** In this section, we first present our surprising finding that pruning can cause catastrophic **207** degradation in VLA success and safety. We then introduce our new method, **GLUESTICK 208** (sin **G** ular va **LUE STIC** hing), which glues pruned VLAs back to high task success rates **209** and safe behaviors as in the original dense models. Additional details and pseudocode are **210** available in Appendix A. **211 212** 3.1 Impact of Pruning on VLA Models **213 214** Pruning has substantially reduced memory usage in language models, with minimal loss in **215** accuracy (see Section 2). At the same sparsity levels commonly used in LLMs, we observe surprisingly different outcomes on popular VLAs. Representative VLAs such as Open- 

4 

Under review as a conference <u>paper</u> at ICLR 2026 

**237** The space of pruning configurations is combinatorial, making optimal selection of weights **238** to remove intractable. Heuristic methods such as Magnitude and Wanda sidestep the global **239** optimization by scoring individual weights and pruning by score. While simple and efficient, **240** these heuristics discard correlated weights under grouped sparsity constraints (e.g., 50% **241** sparsity with 2:4 or 4:8 groups), which could be especially harmful for VLA models. **242** We propose **GLUESTICK** , a post-hoc, training-free recovery method that operates entirely **243** in weight space and is agnostic to the pruning algorithm (see Figure 3). GLUESTICK **244** requires only the original dense model and its pruned counterpart, and incurs a one-time **245** offline cost; no additional training is required. **246** Specifically, for each linear layer with dense weight matrix _W_ dense _∈_ R<sup>_d_out</sup><sup>_×d_in</sup> and its pruned **247** version _W_ pruned (fixed, preserving the original 2:4/4:8 pattern), we define the _gap matrix_ : **248 249** _W_ gap = _W_ dense _− W_ pruned _,_ (1) **250** which captures lost information due to pruning. We then compute a truncated singular **251** value decomposition (SVD) of the gap matrix: **252 253** _W_ gap = _U_ Σ _V_<sup>_⊤_</sup> _≈ Ur_ Σ _rVr_<sup>_⊤,_</sup> (2) **254** keeping the top _r_ singular components. By Eckart & Young (1936), this is the _best rank-r_ **255** approximation to _W_ gap in Frobenius norm. For memory and speed, we fold the singular **256** values into one term so that only two compact matrices need to be stored: **257 258** _A_ = _Ur_ Σ _r ∈_ R<sup>_d_out</sup><sup>_×r_</sup> _, B_ = _Vr ∈_ R<sup>_d_in</sup><sup>_×r_</sup> _._ (3) **259 260** During inference, GLUESTICK adds a lightweight correction around each pruned layer: **261** _h_ ( _x_ ) = _W_ pruned _x_ + _A_ ( _B_<sup>_⊤_</sup> _x_ ) _,_ (4) **262 263264** whichtherebyre-injectspreservingthethedominantefficiencylostgainsdirectionsof structuredat low costsparsitywhilewithleavinga minimal _W_ prunedoverheadunchanged,addition from the correction term. The extra compute from this correction is: **265 266267** efficient _W_ <u>�</u> prunedsparse�� matmul _x_ <u>�</u> + _OB_ <u>�(</u> _d_ <u>��</u><sup>_⊤_</sup> in _x r_ � ) + _OA_ <u>�(</u> _d_ ��(out _·_ )� _r_ ) _,_ (5) **268 269** or _O_ (( _d_ in + _d_ out)) _r_ ) on top of the sparse matrix-matrix multiplication (matmul), versus 

**216** 

VLA (Kim et al., 2024) and NaVILA (Cheng et al., 2025a), when pruned with Magnitude **217** or Wanda, drop in success rate to 0% (from 85.2% and 43.0%, respectively). These come **218** alongside a rise in their unsafe-episode rates; in the worst case OpenVLA increases from **219** 33.4% to 51.6%, and for NaVILA from 23.0% to 100.0% (see Table 1). These findings show **220** that text-validated pruning does not directly transfer to embodied control. **221** To explain why pruning degrades VLAs far more than LLMs or VLMs, we ask whether their or VLMs, we ask whether their, we ask whether their **222** weight-space properties differ. Thus, we examine the singular value spectra of equal-sized **223** layers within the language backbones of OpenVLA (VLA), LLaMA-2-7B (LLM) (Touvron **224** et al., 2023), and Qwen2-VL-Instruct-7B (VLM) (Bai et al., 2025). We display these spectra **225** in Figure 2, where each line corresponds to the singular values of a single layer, obtained by **226** computing the SVD of that layer’s weight matrix and plotting its full set of singular values. **227** In LLM and VLM models, the spectra are more anisotropic, evidenced by a steep initial **228** drop followed by a long tail, which concentrates energy in a few dominant directions. This **229** profile helps pruning, since removing small coefficients mainly trims low-energy directions **230231232** whileflattermagnitudeleavingdecay,coefficientsindicatingtheleavingdecay,coefficientsindicatingthethe principalcontributeenergysubspacesspreadtosubspacesspreadto importantintact.across manyInsubspaces,contrast,directions.soVLApruningInlayersthisdiscardsregime,showdirections.soVLApruningInlayersthisdiscardsregime,showInlayersthisdiscardsregime,showthisdiscardsregime,showregime,show ausefulevennoticeablysmall-signalnoticeablysmall-signal distributed throughout the matrix. Based on this insight, our method in the following **233** section explores the recovery of this lost information within the weight space. **234 235** 3.2 Gluesticking Pruned Models **236** 

To explain why pruning degrades VLAs far more than LLMs or VLMs, we ask whether their or VLMs, we ask whether their, we ask whether their weight-space properties differ. Thus, we examine the singular value spectra of equal-sized layers within the language backbones of OpenVLA (VLA), LLaMA-2-7B (LLM) (Touvron et al., 2023), and Qwen2-VL-Instruct-7B (VLM) (Bai et al., 2025). We display these spectra in Figure 2, where each line corresponds to the singular values of a single layer, obtained by computing the SVD of that layer’s weight matrix and plotting its full set of singular values. In LLM and VLM models, the spectra are more anisotropic, evidenced by a steep initial drop followed by a long tail, which concentrates energy in a few dominant directions. This profile helps pruning, since removing small coefficients mainly trims low-energy directions whileflattermagnitudeleavingdecay,coefficientsindicatingtheleavingdecay,coefficientsindicatingthethe principalcontributeenergysubspacesspreadtosubspacesspreadto intact.across Insubspaces,contrast,directions.soVLApruningInlayersthisdiscardsregime,showcontrast,directions.soVLApruningInlayersthisdiscardsregime,showVLApruningInlayersthisdiscardsregime,showlayersthisdiscardsregime,showshow ausefulevennoticeablysmall-signalnoticeablysmall-signal flattermagnitudeleavingdecay,coefficientsindicatingthedecay,coefficientsindicatingtheindicatingthe energysubspacesspreadtospreadto across manyInsubspaces,contrast,directions.soVLApruningInlayersthisdiscardsregime,showdirections.soVLApruningInlayersthisdiscardsregime,showInlayersthisdiscardsregime,showthisdiscardsregime,showregime,show evennoticeablysmall-signalsmall-signal magnitudeleavingdecay,coefficientsindicatingthecoefficientsindicatingthecontributeenergysubspacesspreadtoto importantintact.across subspaces,contrast,directions.soVLApruningInlayersthisdiscardsregime,showsoVLApruningInlayersthisdiscardsregime,showpruningInlayersthisdiscardsregime,showdiscardsregime,showusefulevennoticeablysmall-signalsignal distributed throughout the matrix. Based on this insight, our method in the following section explores the recovery of this lost information within the weight space. 

or _O_ (( _d_ in + _d_ out)) _r_ ) on top of the sparse matrix-matrix multiplication (matmul), versus _O_ ( _d_ in _d_ out) for the dense layer. Our correction adds only ( _d_ in + _d_ out) _r_ extra parameters 

5 

Under review as a conference <u>paper</u> at ICLR 2026 

**270** per layer, which is small compared to _d_ in _d_ out in the dense case. With _r ≪_ min _{d_ in _, d_ out _}_ , **271** GLUESTICK preserves the efficiency gains of structured 50% sparcity. **272** We refer to our method as GLUESTICK- _r_ to indicate the chosen value of _r_ . We note **273 274** that the parameter _r_ provides a dial between memory usage and recovery. Smaller values of _r_ favor memory savings, while larger values prioritize recovery. In practice, integrating **275** GLUESTICK into a model, requires only a wrapper around pruned layers (Appendix A). **276 277 278** 4 Experimental Setting **279 280 281282** Our experimental setup spans two benchmarks covering distinct robotics domains:lation and navigation. We evaluate three different VLA models on these tasks, withmanipu-results measured using both task performance and safety metrics. **283 284 285** 4.1 Environments **286 287** We list here short descriptions of our test environments (see Appendix B.1 for more details). **288 289 290 Manipulation.** We evaluate on LIBERO (Liu et al., 2023), a benchmark designed to test embodied manipulation skills inspired by human activities (see Figure 1, right). LIBERO **291** tasks provide agents, embodied as a Franka Panda arm, with natural language instructions **292** and visual observations of the environment. The benchmark comprises four task suites: **293** LIBERO-Spatial (same objects, varied layouts), LIBERO-Object (same layout, varied ob- **294** jects), LIBERO-Goal (varied task goals), and LIBERO-Long (long-horizon tasks). **295 296 297 Navigation.** We evaluate navigation using the VLN-CE-Isaac benchmark (Cheng et al., **298** 2025a), which simulates legged robots (e.g., the Unitree Go2 quadruped and the H1 humanoid) traversing indoor environments to reach goal locations (see Figure 1, left). Agents **299** receive image observations and natural language instructions that can involve long-horizon, **300** compositional reasoning (e.g., “walk toward the French doors and turn left, pass the kitchen **301** area, and wait at the end of the hallway near the painting”). The robot executes velocity **302** commands (e.g., move forward 0.75 m, turn right 15°), which are generated by a VLA model. **303 304 305** 4.2 Models **306 307** We list here descriptions of the VLA models studied. See Appendix B.3 for more details. **308 OpenVLA (Kim et al., 2024)** is a 7B-parameter generalist VLA model for manipulation, **309** built on the LLaMA-2 7B language backbone (Touvron et al., 2023) with SigLIP (Zhai et al., **310** 2023) and DINOv2 (Oquab et al., 2023) transformer-based vision encoders. It takes RGB **311** observations and natural language instructions as input, and autoregressively outputs a 7D **312** low-level end-effector pose along with gripper open/close commands. **313 WorldVLA (Cen et al., 2025)** is a 7B manipulation-oriented VLA that emphasizes **314** long-horizon consistency through an autoregressive action world-modeling objective. It is **315** initialized from the 7B Chameleon vision–language model (Team, 2024) with a convolution- **316** based VQ-GAN vision encoder (Esser et al., 2021). The model ingests the current RGB **317** observation, a sequence of history images, and a natural language instruction; generating **318** 7D low-level end-effector poses along with gripper open/close commands in action chunks. **319 NaVILA (Cheng et al., 2025a)** is an 8B-parameter, navigation-focused VLA designed **320** for legged robots. It is built on the VILA vision–language model (Lin et al., 2024), which **321** combines a ViT-based visual encoder with a language backbone inspired by LLaVA’s ar- **322** chitecture (Liu et al., 2024a), but pre-trained on a unique mixture of data. The model **323** consumes the current egocentric image along with a set of history frames and natural language instructions; outputing velocity commands executed by a locomotion controller. 

We refer to our method as GLUESTICK- _r_ to indicate the chosen value of _r_ . We note that the parameter _r_ provides a dial between memory usage and recovery. Smaller values of _r_ favor memory savings, while larger values prioritize recovery. In practice, integrating GLUESTICK into a model, requires only a wrapper around pruned layers (Appendix A). 

**OpenVLA (Kim et al., 2024)** is a 7B-parameter generalist VLA model for manipulation, built on the LLaMA-2 7B language backbone (Touvron et al., 2023) with SigLIP (Zhai et al., 2023) and DINOv2 (Oquab et al., 2023) transformer-based vision encoders. It takes RGB observations and natural language instructions as input, and autoregressively outputs a 7D low-level end-effector pose along with gripper open/close commands. 

**WorldVLA (Cen et al., 2025)** is a 7B manipulation-oriented VLA that emphasizes long-horizon consistency through an autoregressive action world-modeling objective. It is initialized from the 7B Chameleon vision–language model (Team, 2024) with a convolutionbased VQ-GAN vision encoder (Esser et al., 2021). The model ingests the current RGB observation, a sequence of history images, and a natural language instruction; generating 7D low-level end-effector poses along with gripper open/close commands in action chunks. 

6 

Under review as a conference <u>paper</u> at ICLR 2026 

**324 Method LIBERO** ( _↑_ ) **Mean** ( _↑_ ) **325 326 Spatial Object Goal Long 327** Full Dense +0 _._ 0 +0 _._ 0 +0 _._ 0 +0 _._ 0 +0 _._ 0 **328** Full Sparse _−_ 85 _._ 2 _−_ 72 _._ 4 _−_ 76 _._ 2 _−_ 55 _._ 8 _−_ 72 _._ 4 **329** Sparse Lang. BB _−_ 69 _._ 5 _−_ 57 _._ 3 _−_ 58 _._ 5 _−_ 49 _._ 3 _−_ 58 _._ 7 **330** % Sparse Lang. BB _−_ 71 _._ 6 _−_ 57 _._ 9 _−_ 57 _._ 8 _−_ 49 _._ 8 _−_ 59 _._ 3 **331 GLUESTICK-500** _−_ 32 _._ 8 _−_ 34 _._ 9 _−_ 32 _._ 9 _−_ 42 _._ 2 _−_ 35 _._ 7 **332 333** Table 2: **Change in success rate (%) relative to Full Dense.** Higher values indicate a **334** better success rate. Results are averaged across OpenVLA and WorldVLA. % Sparse Lang. BB uses the same VRAM as GLUESTICK-500. **335 336** 4.3 Evaluation Metrics **337 338** We evaluate VLA agents on two axes: _task success_ and _safety_ . Success captures whether **339** the agent achieves the stated goal. Safety captures whether it does so without causing harm **340** to itself or the environment. Refer to Appendix B.2 for more detailed metric definitions. **341 Task Success.** We report binary per-episode success: an episode is successful if the agent **342** completes the objective, and unsuccessful otherwise. **343 344 Safety.** Following prior robotics safety work (Dulac-Arnold et al., 2019; Geng et al., 2023; **345** Morton & Pavone, 2025), we operationalize safety as the absence of harm caused to the **346** robot or its surroundings. For manipulation, we monitor robot- and environment-centered risks (e.g., joint-limit violations, arm–environment collisions, unsafe object motion, and **347** end-effector/whole-body containment breaches). For navigation, we track collision events. **348 349** 4.4 Baselines **350 351** We consider three pruning strategies: (i) **Full Sparse** , where all linear components except **352** the language model head are pruned with 50% 2:4 structured sparsity using Wanda; (ii) **353 Sparse Language Backbone** , where only the language backbone is pruned; and (iii) a **354 Memory-Matched Sparse Language Backbone** , which prunes a subset of backbone **355** layers while maintaining 50% 2:4 sparsity in each pruned layer, to provide a fair comparison **356** to GLUESTICK’s overhead. We use strict 2:4 structured sparsity across all settings, since **357** this level of pruning is necessary to realize meaningful improvements from hardware-efficient **358** sparse kernels. We choose to use Wanda as our base pruning algorithm because it represents the state of the art and is highly practical due to its minimal computational cost during **359** pruning. See Appendix C for details. **360 361** 5 Results **362 363** We structure our results around key questions, first presenting main findings on GLUE- **364** STICK then providing analysis through ablations and broader considerations of pruning. **365 366** 5.1 Main Results **367 368 Q1:** _Does GLUESTICK recover task performance for pruned VLAs on manipulation tasks?_ **369** Across all four LIBERO task suites, Full Sparse yields a severe average degradation of **370** _−_ 72 _._ 4% (Table 2 shows the average results across OpenVLA and WorldVLA). In contrast, **371** GLUESTICK–500 degrades by only _−_ 35 _._ 7%, recovering 50% of the success rate lost to prun- **372** ing. Recovery is especially strong in the Spatial and Goal suites, where GLUESTICK re- **373** stores 62% and 57% of lost performance, respectively. Relative to the memory-matched **374** baselinesubstantially(–59 _._ restoring3% averagemanipulationLIBERO success),performanceGLUESTICKwhile retainingrecoverspruning40% efficiency.of lost success,This **375** demonstrates that GLUESTICK can effectively recover task performance for pruned VLAs **376** on dexterous manipulation tasks. See Appendix C.1 for details. **377** 

- **Q2:** _Does GLUESTICK recover task performance for pruned VLAs on navigation tasks?_ 

7 

Under review as a conference <u>paper</u> at ICLR 2026 

**378 Method ∆Succ.** ( _↑_ ) **∆Unsafe** ( _↓_ ) **PL** ( _↓_ ) **DG** ( _↓_ ) **∆RAM** ( _↓_ ) **379 380** Full Dense +0 _._ 0 +0 _._ 0 11 _._ 7 5 _._ 9 +0 _._ 00 **381** Full Sparse _−_ 43 _._ 0 +23 _._ 0 17 _._ 6 9 _._ 5 _−_ 5 _._ 74 **382** Sparse Lang. BB _−_ 20 _._ 0 +2 _._ 0 14 _._ 8 8 _._ 5 _−_ 5 _._ 68 **383** % Sparse Lang. BB _−_ 18 _._ 0 +12 _._ 0 14 _._ 9 8 _._ 4 _−_ 4 _._ 59 GLUESTICK-200 _−_ 2 _._ 0 _−_ 1 _._ 0 12 _._ 5 6 _._ 5 _−_ 5 _._ 36 **384 GLUESTICK-500** +1 _._ 0 _−_ 4 _._ 0 11 _._ 9 5 _._ 9 _−_ 4 _._ 60 **385 386** Table 3: **Navigation results.** ∆ columns are relative to Full Dense; higher ∆Succ. and **387** lower ∆Unsafe are better. All methods use the NaVILA model. Lang. BB = language **388** backbone. RAM is peak usage. PL = Path Length. DG = Final Distance to Goal. **389 390 Method LIBERO** ( _↓_ ) **Mean** ( _↓_ ) **391 Spatial Object Goal Long 392** Full Dense +0 _._ 0 +0 _._ 0 +0 _._ 0 +0 _._ 0 +0 _._ 0 **393** Full Sparse +18 _._ 2 +23 _._ 0 +1 _._ 4 +11 _._ 6 +13 _._ 6 **394** Sparse Language BB +9 _._ 0 +13 _._ 2 +1 _._ 8 +9 _._ 4 +8 _._ 4 **395** % Sparse Language BB +5 _._ 6 +14 _._ 4 +4 _._ 6 +5 _._ 2 +7 _._ 5 **396 GLUESTICK-500** +0 _._ 2 +1 _._ 2 +0 _._ 0 +4 _._ 6 +1 _._ 5 **397 398** Table 4: **Change in unsafe-episode rate (%) relative to Full Dense.** Lower _↓_ indicates **399** fewer episodes with safety violations. % Sparse VRAM is equal to GLUESTICK-500. **400 401** On the VLN-CE-Isaac benchmark, the Full Sparse NaVILA model shows a _−_ 43 _._ 0% change **402** relative to the dense baseline (see Table 3). This corresponds to a collapse from 43 _._ 0% **403404** success toportantly, 0this%, demonstrating that pruning completely destroys navigational capability.failure is not a matter of taking less efficient paths—the robot’s navigationImbehavior is fundamentally altered. After Full Sparse pruning, the mean path length increases **405** by nearly 50%, from 11 _._ 7 meters to 17 _._ 6 meters, and the mean distance to goal increases by **406** more than 40%, from 5 _._ 9 meters to 9 _._ 5 meters. Rather than approaching the goal, pruned **407** agents frequently veer into entirely different rooms (see Appendix C.2 for distributions). **408 409** In contrast, GLUESTICK–500 fully restores the dense model’s performance, recovering **410** 100% of the lost success rate. Moreover, path length and final distance-to-goal remain nearly identical to the dense baseline, indicating not only restored success but also restored **411** efficiency of navigation trajectories. The memory-matched baseline remains far less compet- **412** itive, showing a _−_ 18% drop relative to the dense model. This highlights that for navigation, **413** GLUESTICK not only mitigates pruning degradation but completely closes the gap to dense **414** performance across both success and path-quality metrics. **415 416 Q3:** _How well does GLUESTICK restore the safety of pruned VLAs?_ **417** Table 3, 4 report changes in unsafe-episode rate relative to the dense baseline in navigation **418** and manipulation, respectively. Pruning increases unsafe behaviors in both domains. The **419** Full Sparse model shows the largest degradation, with unsafe episodes rising by +13 _._ 6% on **420** LIBERO and +23 _._ 0% on navigation. The Memory-Matched Sparse Backbone also increases **421** unsafe episodes by +7 _._ 5% and +8 _._ 4%, respectively. **422** By contrast, GLUESTICK–500 remains near parity with the dense policy, yielding 89% and **423** 100% fewer unsafe episodes compared to the Full Sparse model for manipulation and navi- **424** gation, respectively. Overall, GLUESTICK–500 maintains the safety profile of the original **425** dense models, with only a minimal +0 _._ 4% change across domains. These results indicate **426** that GLUESTICK restores dominant weight-space directions that carry both task-relevant **427** and safety-critical signal, thereby preserving the safety of VLA models in manipulation and **428** navigation. **429 430** 5.2 Analysis **431** 

- **Q4:** _How does the rank_ ( _r_ ) _affect GLUESTICK’s recovery–memory trade-off?_ 

8 

Under review as a conference <u>paper</u> at ICLR 2026 

**432** 100 **433** 85.2% Dense 80 GLUESTICK **434** 57.4% **435** 60 **436** 40 30.8% **37x 437** 18.6% **438** 20 7.4% **4.8x 439** 0 0.0% 0.6% **440 441 442 443** Figure 4: **Ablation study.** Rank ablation **(left)** and component sensitivity **(right)** . **444 445 Method 0% 30% 50% 70% Method 0% 30% 50% 70% 446** W 85.2 80.8 31.8 1.2 W 93.88 93.38 88.16 21.3 **447** W+GS – 85.8 60.2 24.6 W+GS – – 92.95 90.89 **448 449** Table 5: **GLUESTICK-500’s (GS) re-** Table 6: **GLUESTICK-500’s (GS) gen450 covery of VLA success rates across erality to recover pruned VLM perfor451 sparsity ratios.** Evaluated on LIBERO **mance.** Evaluated on 1000 examples from **452** Spatial. Results for the pruned language DocVQA using Wanda (W) pruned Qwen2- **453** backbone of OpenVLA using Wanda (W). VL-7B-Instruct VLM. Values show ANLS. **454** We observe that increasing the rank _r_ improves success-rate recovery, as shown in Figure 4, **455** but at the cost of additional memory. Table 3 illustrates this trade-off: a fully sparse **456** NaVILA model achieves the maximum memory savings of 5 _._ 74GB but suffers a _−_ 43% drop **457** in success rate. By contrast, GLUESTICK–200 recovers nearly the full dense success rate **458** while saving 5 _._ 36GB of VRAM (offering memory savings within 0 _._ 38GB of Full Sparse). **459** Thus, GLUESTICK exposes a single hyperparameter _r_ that controls the trade off between **460** memory efficiency and task recovery. See Appendix C.1 for full GLUESTICK-200 results. **461 Q5:** _Which VLA components are most sensitive to pruning?_ **462 463** To understand VLA component sensitivity, we selectively prune either the language back- **464** bone or the vision backbone while keeping the rest of the model dense. For OpenVLA (7.5B **465** total parameters: 89 _._ 4% in the language backbone, 9 _._ 7% in the vision backbone, and 0 _._ 9% in the projector), pruning the language backbone reduces the LIBERO Spatial benchmark **466** success by _−_ 54 _._ 0%, while pruning the vision backbone reduces success by _−_ 27 _._ 8%. When **467** normalized per million parameters, pruning the vision backbone is 4.75 _×_ more damaging **468** than pruning the language backbone. We observe the same phenomenon in NaVILA (8.5B **469** total parameters: 94 _._ 5% in the language backbone, 5 _._ 0% in the vision encoder, and 0 _._ 4% **470** in the projector). Here, pruning the language backbone reduces success by _−_ 20 _._ 0%, while **471** pruning the vision backbone reduces success by _−_ 40 _._ 0%. On a per-parameter basis, vision **472** pruning is 37.5 _×_ more damaging than language pruning. We find that vision backbones **473** are disproportionately sensitive to pruning while offering little memory benefit, since they **474** comprise less than 10% of total parameters. Because pruning vision components causes out- **475** sized harm relative to their limited contribution to overall model size, our main evaluations **476** include a focus on pruning the language backbone. **477 Q6:** _Why not compress weights directly with SVD and avoid pruning altogether?_ **478** A natural question is why pruning is necessary at all if weight matrices could instead be **479** compressed directly through low-rank decomposition. In principle, one could replace each **480** dense layer with an SVD approximation, storing only the top- _r_ singular components. To **481** test this, we conducted experiments where OpenVLA weights were approximated various **482** SVD ranks (without pruning). On LIBERO Spatial, this setting achieved a 0% success rate **483** across nearly all experiemnts (see Appendix D.6), indicating that low-rank approximations **484** alone are insufficient to preserve the functionality of VLA models. This suggests that the **485** pruned weight matrix itself retains valuable structure that cannot be captured by low-rank SVD alone. GLUESTICK leverages this by preserving the pruned weights (and structured 

9 

Under review as a conference <u>paper</u> at ICLR 2026 

**486 Task:** Enter the kitchen from the office and walk to the sofa on the left side of the kitchen. **487 488 489 490 491 492 493 494 Full Dense Full Pruned GLUESTICK-500 495 Trajectory Deviation (↓)** 0 _._ 00 +10 _._ 26 +5 _._ 12 **496 497** Figure 5: **Real-world Demonstration.** (Top) Our real-world Boston Dynamics Spot **498** robot navigating in a real office environment. (Bottom) Trajectory Deviation is the cumula- **499** tive L1 difference in linear and angular velocity commands relative to the Full Dense model. **500 501** sparsity benefits) while using SVD only to reintroduce lost directions, nudging the model **502** back toward a more performant region of weight space. **503 Q7:** _How does GLUESTICK perform when VLAs are pruned at different sparsity levels?_ **504505** We evaluate GLUESTICK’s capability to recover pruned VLA models under different sparsity ratios in Table 5. In this experiment, we prune the language-backbone in OpenVLA **506** and observe that GLUESTICK recovers performance effectively across sparsity levels. **507 508 Q8:** _How does GLUESTICK generalize to restore pruned VLM performance?_ **509** We evaluate GLUESTICK’s capability to recover the performance of a pruned VLM under **510** various sparsity ratios in Table 6. We find strong generality, as GLUESTICK recovers VLM **511** performance even at 70% sparsity, improving ANLS from 21.30 to 90.89. **512 Q9:** _How does GLUESTICK perform in real-world robotic deployments?_ **513 514** We conduct a small real-world experiment to assess whether GLUESTICK transfers to **515** physical robotic settings. Using a Spot robot navigating in an office environment, we mea- **516** sure the trajectory deviation of the pruned VLA relative to the dense VLA and find that **517** GLUESTICK reduces deviation by 50%, showing effective real-world transfer (Figure 5). **518 519** 6 Discussion **520** We begin by clarifying the relationship between GLUESTICK and LoRA. While both intro- **521** duce low-rank components, they are designed for fundamentally different purposes and op- **522** erate in distinct ways (detailed comparison in Appendix E.1). We apply GLUESTICK only **523** to linear layers because they constitute the overwhelming majority (93–98%) of parameters **524** in modern VLA architectures, as shown in Appendix D.3. Finally, we observe that GLUE- **525** STICK recovers a larger fraction of performance in navigation than in manipulation. This **526** stems from the different error tolerances of the two domains (discussed in Appendix D.5). **527 528** 7 Conclusion and Future Work **529530** We presented the first systematic study of pruning VLA models and showed that pruning **531** severely degrades both task success and safety. To address this, we introduced GLUESTICK, a training-free, pruning-agnostic, and easily integrable post-pruning recovery method that **532** reintroduces lost directions due to pruning, restoring performance and safety while retaining **533** efficiency. Importantly, because our approach is independent of the pruning algorithm, it can **534** be applied as a universal recovery step as new pruning strategies continue to emerge. Looking **535** forward, several promising directions remain such as prioritizing safety-critical directions in **536** weight space and exploring other low-rank matrix approximation techniques. Additionally, **537** a per-layer rank-scheduling algorithm is a compelling next step, as GLUESTICK naturally **538** accommodates this through independently computed layer-wise corrections. We hope this **539** work lays the foundation for developing compression techniques that make powerful VLA models practical for real-world deployment on resource-constrained robotic platforms. 

10 

Under review as a conference <u>paper</u> at ICLR 2026 

> **540** References **541 542** Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni **543** Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. **544** GPT-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. **545** Peter Anderson, Qi Wu, Damien Teney, Jake Bruce, Mark Johnson, Niko Sünderhauf, Ian 

> **546** Reid, Stephen Gould, and Anton Van Den Hengel. Vision-and-language navigation: In- 

> **547** terpreting visually-grounded navigation instructions in real environments. In _Proceedings_ 

> **548** _of the IEEE conference on computer vision and pattern recognition_ , pp. 3674–3683, 2018. **549 550** Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng **551** Wang, Shijie Wang, Jun Tang, et al. Qwen2. 5-vl technical report. _arXiv preprint_ **552** _arXiv:2502.13923_ , 2025. 

> **553** James Betker, Gabriel Goh, Li Jing, Tim Brooks, Jianfeng Wang, Linjie Li, Long Ouyang, 

> **554** Juntang Zhuang, Joyce Lee, Yufei Guo, et al. Improving image generation with better 

> **555** captions. _Computer Science. https://cdn. openai. com/papers/dall-e-3. pdf_ , 2(3):8, 2023. **556 557** Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, **558** Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. GR00T N1: an open foundation **559** model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

> **560** Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, 

> **561** Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. pi0: A vision-language- **562** action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. **563 564** Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea **565** Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt- **566** 1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. **567** 

> **568** Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin 

> **569** Li, Yibing Song, Hao Luo, Fan Wang, Deli Zhao, and Hao Chen. Worldvla: To- 

> **570** wards autoregressive action world model. 2025. doi: 10.48550/arXiv.2506.21539. URL 

> **571** `https://arxiv.org/abs/2506.21539` . **572** 

   - Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, et al. Qwen2. 5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 

- **573** An-Chieh Cheng, Yandong Ji, Zhaojing Yang, Zaitian Gongye, Xueyan Zou, Jan Kautz, **574** Erdem Bıyık, Hongxu Yin, Sifei Liu, and Xiaolong Wang. Navila: Legged robot visionlanguage-action model for navigation. 2025a. doi: 10.48550/arXiv.2412.04453. URL 

- **575** `https://arxiv.org/abs/2412.04453` . 

- **576** 

- **577** Xinle Cheng, Zhuoming Chen, and Zhihao Jia. Cat pruning: Cluster-aware token pruning **578** for text-to-image diffusion models. _arXiv preprint arXiv:2502.00433_ , 2025b. 

**578 579** 

- **580** Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Ayzaan **581** Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, et al. Palm-e: An embodied multimodal language model. 2023. 

- **582** 

**583** 

- **583** Gabriel Dulac-Arnold, Daniel Mankowitz, and Todd Hester. Challenges of real-world rein- **584** forcement learning. _arXiv preprint arXiv:1904.12901_ , 2019. **585** 

- **586** Carl Eckart and Gale Young. The approximation of one matrix by another of lower rank. **587** _Psychometrika_ , 1(3):211–218, 1936. doi: 10.1007/BF02288367. 

**588** 

**589** 

**590 591** 

   - Patrick Esser, Robin Rombach, and Bjorn Ommer. Taming transformers for high-resolution image synthesis. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 12873–12883, 2021. 

- **592** Elias Frantar and Dan Alistarh. Sparsegpt: Massive language models can be accurately **593** pruned in one-shot. In _International conference on machine learning_ , pp. 10323–10337. PMLR, 2023. 

11 

Under review as a conference <u>paper</u> at ICLR 2026 

- Leo Gao, Jonathan Tow, Stella Biderman, Sid Black, Anthony DiPofi, Charles Foster, Laurence Golding, Jeffrey Hsu, Kyle McDonell, Niklas Muennighoff, Jason Phang, Laria Reynolds, Eric Tang, Anish Thite, Ben Wang, Kevin Wang, and Andy Zou. A framework for few-shot language model evaluation. Version v0.0.1, September 2021. 

> **594** Leo Gao, Jonathan Tow, Stella Biderman, Sid Black, Anthony DiPofi, Charles Foster, Lau- 

> **595** rence Golding, Jeffrey Hsu, Kyle McDonell, Niklas Muennighoff, Jason Phang, Laria 

> **596** Reynolds, Eric Tang, Anish Thite, Ben Wang, Kevin Wang, and Andy Zou. A framework 

> **597** for few-shot language model evaluation. Version v0.0.1, September 2021. **598 599** Yiran Geng, Jiamg Ji, Yuanpei Chen, Long Yang, and Yaodong Yang. A massively paral- **600** lel benchmark for safe dexterous manipulation, 2023. URL `https://openreview.net/` **601** `forum?id=k2Ml8FGtJZp` . 

> **602** Song Han, Jeff Pool, John Tran, and William Dally. Learning both weights and connections 

> **603** for efficient neural network. _Advances in neural information processing systems_ , 28, 2015. **604 605** Song Han, Xingyu Liu, Huizi Mao, Jing Pu, Ardavan Pedram, Mark A Horowitz, and **606** William J Dally. Eie: Efficient inference engine on compressed deep neural network. **607** _ACM SIGARCH Computer Architecture News_ , 44(3):243–254, 2016. 

> **608** Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny 

> **609** Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5:: a vision- 

> **610** language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 

> **611** 2025. **612 613** Jason Jabbour and Vijay Janapa Reddi. Generative ai agents in autonomous machines: A **614** safety perspective. In _Proceedings of the 43rd IEEE/ACM International Conference on Computer-Aided Design_ , pp. 1–13, 2024. **615** 

> **616** Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon **617** Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural 

> **618** language models. _arXiv preprint arXiv:2001.08361_ , 2020. **619 620** Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj **621622** Nair,Kollar,RafaelBenjaminRafailov,Burchfiel,Ethan RussFoster,Tedrake,Grace Lam,DorsaPannagSadigh,Sanketi,SergeyQuanLevine,Vuong,PercyThomasLiang, and Chelsea Finn. OpenVLA: An open-source vision-language-action model. 2024. doi: 

> **623** 10.48550/arXiv.2406.09246. URL `https://arxiv.org/abs/2406.09246` . **624** 

> **625** Toshiaki Koike-Akino, Jing Liu, and Ye Wang. mumoe: Test-time pruning as micro-grained **626** mixture-of-experts. _arXiv preprint arXiv:2505.18451_ , 2025. **627 628** Jacob Krantz, Erik Wijmans, Arjun Majumdar, Dhruv Batra, and Stefan Lee. Beyond the nav-graph: Vision-and-language navigation in continuous environments. In _European_ **629** _Conference on Computer Vision_ , pp. 104–120. Springer, 2020. **630** 

> **631** Jason Lee, Jiafei Duan, Haoquan Fang, Yuquan Deng, Shuo Liu, Boyang Li, Bohan Fang, **632** Jieyu Zhang, Yi Ru Wang, Sangho Lee, et al. Molmoact: Action reasoning models that **633** can reason in space. _arXiv preprint arXiv:2508.07917_ , 2025. **634** Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, **635** Yu Deng, Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational vision-language- **636** action model for synergizing cognition and action in robotic manipulation. _arXiv preprint_ 

> **637** _arXiv:2411.19650_ , 2024. **638 639** Yinan Liang, Ziwei Wang, Xiuwei Xu, Jie Zhou, and Jiwen Lu. Efficientllava: Generalizable **640** auto-pruning for large vision-language models. In _Proceedings of the Computer Vision_ **641** _and Pattern Recognition Conference_ , pp. 9445–9454, 2025. **642** Ji Lin, Hongxu Yin, Wei Ping, Pavlo Molchanov, Mohammad Shoeybi, and Song Han. Vila: 

> **643** On pre-training for visual language models. In _Proceedings of the IEEE/CVF conference_ 

> **644** _on computer vision and pattern recognition_ , pp. 26689–26699, 2024. **645 646** Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. **647** LIBERO: Benchmarking knowledge transfer for lifelong robot learning. 2023. doi: 10. 48550/arXiv.2306.03310. URL `https://arxiv.org/abs/2306.03310` . 

- Song Han, Xingyu Liu, Huizi Mao, Jing Pu, Ardavan Pedram, Mark A Horowitz, and William J Dally. Eie: Efficient inference engine on compressed deep neural network. _ACM SIGARCH Computer Architecture News_ , 44(3):243–254, 2016. 

- Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5:: a visionlanguage-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

12 

Under review as a conference <u>paper</u> at ICLR 2026 

**648** 

**649** 

**650** 

- Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. Improved baselines with visual instruction tuning. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 26296–26306, 2024a. 

**651** 

- **652** Peize Liu, Chen Feng, Yang Xu, Yan Ning, Hao Xu, and Shaojie Shen. Omninxt: A **653** fully open-source and compact aerial robot with omnidirectional visual perception. In **654** _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 10605–10612. IEEE, 2024b. 

- **655** 

- **656** Asit Mishra, Jorge Albericio Latorre, Jeff Pool, Darko Stosic, Dusan Stosic, Ganesh 

- **657** Venkatesh, Chong Yu, and Paulius Micikevicius. Accelerating sparse deep neural net- **658** works, 2021. URL `https://arxiv.org/abs/2104.08378` . **659** Daniel Morton and Marco Pavone. Safe, task-consistent manipulation with operational 

- **660** space control barrier functions. _arXiv preprint arXiv:2503.06736_ , 2025. 

**660 661** 

- **662** NVIDIA. _DGX B200 Datasheet_ , 2025. URL `https://resources.nvidia.com/` **663** `en-us-dgx-systems/dgx-b200-datasheet?ncid=no-ncid` . Accessed: 2025-09-25. 

- **664** Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy Vo, Marc Szafraniec, Vasil **665** Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, **666** et al. DINOv2: Learning robust visual features without supervision. _arXiv preprint_ **667** _arXiv:2304.07193_ , 2023. 

- **668** 

- Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, 

- **669** Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open 

- **670** X-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collab- 

- **671** oration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , **672** pp. 6892–6903. IEEE, 2024. **673** 

- **674** Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, **675** JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

**676** 

- **677** Lucas Rey, Ana M Bernardos, Andrzej D Dobrzycki, David Carramiñana, Luca Bergesio, **678** Juan A Besada, and José Ramón Casar. A performance analysis of you only look once **679** models for deployment on constrained computational edge devices in drone applications. **680** _arXiv preprint arXiv:2502.15737_ , 2025. **681** 

- **681** Manolis Savva, Abhishek Kadian, Oleksandr Maksymets, Yili Zhao, Erik Wijmans, Bhavana **682** Jain, Julian Straub, Jia Liu, Vladlen Koltun, Jitendra Malik, Devi Parikh, and Dhruv **683** Batra. Habitat: A platform for embodied ai research. In _Proceedings of the IEEE/CVF_ **684** _International Conference on Computer Vision (ICCV)_ , pp. 9339–9347, 2019. doi: 10.1109/ **685** ICCV.2019.00943. URL `https://openaccess.thecvf.com/content_ICCV_2019/html/` **686** `Savva_Habitat_A_Platform_for_Embodied_AI_Research_ICCV_2019_paper.html` . 

- **687** Mingjie Sun, Zhuang Liu, Anna Bair, and J Zico Kolter. A simple and effective pruning **688** approach for large language models. _arXiv preprint arXiv:2306.11695_ , 2023a. 

**688 689** 

- **690** Mingjie Sun, Zhuang Liu, Anna Bair, and J. Zico Kolter. A simple and effective pruning **691** approach for large language models. _arXiv preprint arXiv:2306.11695_ , 2023b. URL `https:` **692** `//arxiv.org/abs/2306.11695` . “Wanda: Pruning by Weights and Activations” – weights × activations metric. 

**693** 

- **694** Chameleon Team. Chameleon: Mixed-modal early-fusion foundation models. _arXiv preprint_ **695** _arXiv:2405.09818_ , 2024. 

**696** 

- Gemini Team, Rohan Anil, Sebastian Borgeaud, Jean-Baptiste Alayrac, Jiahui Yu, Radu 

- **697** Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. Gemini: a 

- **698** family of highly capable multimodal models. _arXiv preprint arXiv:2312.11805_ , 2023. 

**699** 

- **700** Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, **701** Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. 

13 

Under review as a conference <u>paper</u> at ICLR 2026 

**702** Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for **703** language image pre-training. In _Proceedings of the IEEE/CVF international conference_ **704** _on computer vision_ , pp. 11975–11986, 2023. **705** 

- **706** Xunyu Zhu, Jian Li, Yong Liu, Can Ma, and Weiping Wang. A survey on model compression **707** for large language models. _Transactions of the Association for Computational Linguistics_ , **708** 12:1556–1577, 2024. 

> **709** Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul 

> **710** Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action mod- 

> **711** els transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. **712** 2165–2183. PMLR, 2023. **713 714 715 716 717 718 719 720 721 722 723 724 725 726 727 728 729 730 731 732 733 734 735 736 737 738 739 740 741 742 743 744 745 746 747 748 749 750 751 752 753 754 755** 

14 

Under review as a conference <u>paper</u> at ICLR 2026 

|**756**<br>**757**|Appendix|
|---|---|
|**758**<br>**759**|A<br>GLUESTICK Details|
|**760**<br>**761**<br>**762**|Our method can be implemented in just a few lines of code.|
|**763**<br>**764**|**Algorithm 1:** PyTorch code for GLUESTICK (Offline)|
|**765**<br>**766**|`# Compute and Store GLUESTICK Correction terms for every linear layer`|
|**767**<br>**768**<br>**769**<br>**770**|**`def`** `prime_gluestick(W_dense , W_pruned , r):`<br>`# W_dense: layer (l) dense weights (d_out, d_in)`<br>`# W_pruned: layer (l) pruned weights (d_out, d_in)`<br>`# r: target rank`|
|**771**<br>**772**|`W_gap = W_dense - W_pruned`<br>`U, S, Vh =` **`torch`**`.linalg.svd(W_gap)`|
|**773**<br>**774**<br>**775**<br>**776**<br>**777**|`U_r`<br>`= U[:, :r]`<br>`S_r`<br>`= S[:r]`<br>`V_r`<br>`= Vh[:r, :].T`<br>`A`<br>`= U_r * S_r.unsqueeze(0)`<br>`B`<br>`= V_r`|
|**778**<br>**779**<br>|**`return`** `{"A": A, "B": B}`|
|**780**<br>**781**<br>**782**<br>**783**<br>|In the offline stage (Algorithm 1), we iterate through the dense and pruned weights of each<br>linear layer, compute the correction terms, and store them.|
|**784**<br>**785**|**Algorithm 2:** PyTorch code for GLUESTICK (Online)|
|**786**<br>**787**<br>**788**<br>**789**<br>**790**<br>**791**|**`class`** `GLUESTICKWrap(`**`nn`**`.Module):`<br>**`def`** `__init__(`**`self`**`, pruned_linear_layer , A, B):`<br>**`super`**`().__init__()`<br>**`self`**`.pruned_linear = pruned_linear_layer`<br>**`self`**`.A = A`<br>**`self`**`.B = B`|
|**792**<br>**793**<br>**794**|**`def`** `forward(`**`self`**`, x):`<br>`# Efficient Sparse MatMul`<br>`y =` **`F`**`.linear(`|
|**795**<br>**796**<br>**797**|`x,`<br>**`self`**`.pruned_linear_layer.weight ,`<br>**`self`**`.pruned_linear_layer.bias`<br>`)`|
|**798**<br>**799**<br>**800**|`# Compute GLUESTICK Correction`<br>`correction =` **`self`**`.A @ (`**`self`**`.B.T @ x)`<br>**`return torch`**`.add(y, correction)`|
|**801**<br>**802**<br>**803**<br>**804**<br>**805**<br>**806**<br>|`# Load Pruned Model`<br>`model = load_pruned_model()`<br>`# Load GLUESTICK correction terms for every linear layer`<br>`correction_terms = load_correction_terms()`<br>`# Apply GLUESTICK to all pruned linaer layers in the model`<br>`model = apply_gluestick(model, correction_terms)`|
|**807**<br>**808**<br>**809**|In the online stage (Algorithm 2), we load the pruned model along with the saved correction<br>terms and wrap each pruned linear layer with GLUESTICK to enable corrected inference.|


15 

Under review as a conference <u>paper</u> at ICLR 2026 

**810** 

# B Experimental Setting 

### **811** 

**812** 

## B.1 Environments 

### **813** 

> **814 Manipulation** Our manipulation evaluation covers all 10 tasks from each of the four 

> **815** LIBERO suites, with each task repeated 50 times, resulting in 2,000 total episodes. **816** 

> **817 Navigation** VLN-CE-Isaac builds on VLN-CE (Krantz et al., 2020), which itself is based **818** on the Habitat simulator (Savva et al., 2019). Habitat provides photorealistic 3D environ- **819** ments and physics-based simulation for embodied AI, moving beyond the original VLN task **820** that used MatterPort3D panoramas represented as discrete navigation graphs (Anderson **821** et al., 2018). Unlike the graph-based setting, Habitat supports continuous actions and real- **822** istic perception, allowing agents to navigate freely in 3D space. However, Habitat does not simulate robot embodiment—for instance, agents can move through unrealistic gaps (e.g., **823** 10 cm between two sofas) that would be infeasible for legged robots. VLN-CE-Isaac in- 

> **824** herits this Habitat-based formulation but extends it to physically simulated robots in Isaac 

> **825** Sim, enabling evaluation on platforms such as the Unitree Go2 quadruped and Unitree H1 

> **826** humanoid. This provides a comprehensive benchmark of the full navigation pipeline, from 

> **827** high-level language understanding to low-level motor control. We evaluate on 100 randomly 

> **828** selected scenes from the 1,077 available in the VLN-CE-Isaac benchmark. **829** 

> **830 Hardware** In all experiments, we use an NVIDIA L40S GPU with 48 GB of VRAM. 

**831** 

**832 833** 

## B.2 Safety Definitions 

**834 Safety in Navigation.** For navigation tasks, we use collisions as the primary safety **835** metric. A collision is recorded whenever the agent outputs actions that cause the robot to **836** make unintended contact with objects in the environment. This measures the agent’s ability to move purposefully without endangering itself or its surroundings. 

**837** 

**838 839 Safety in Manipulation.** For manipulation tasks, we introduce a set of five safety metrics that capture risks to both the robot and the environment: 

**840** 

> **841** • **Joint limit violations:** Occur when the agent outputs actions that drive joint 

> **842** angles close to or beyond their mechanical limits, which can cause long-term wear 

> **843** or physical damage to the robot’s actuators. 

> **844** • **Arm collisions:** Measured when any part of the robot arm (excluding the end 

> **845** effector) makes unintended contact with the environment, potentially harming both 

> **846** the robot and external objects. **847** • **Object velocities:** We track the velocities of manipulated objects as a proxy 

> **848** for physical stability, penalizing outcomes where objects are flung, dropped, or 

> **849** otherwise move unsafely. 

> **850851** • **End-effector containment:** We enforce that the end effector remains within a bounded three-dimensional workspace region. This ensures that the robot’s ac- **852** tions stay localized and prevents dangerous or uncontrolled motions outside of its **853** designated operating zone. **854 855** • **Whole-body containment:** Similarly, we verify that the robot’s entire body remains within a global containment region. Exiting this region can represent unsafe 

> **856** configurations or uncontrolled movement, posing risk to both the platform and its **857** environment. **858** 

**859** An episode is deemed _unsafe_ whenever it violates one or more of the defined safety metrics. **860** We use the following thresholds: joint limit violations occur if a joint exceeds 0.1% of its **861** range; object motion is unsafe if velocity exceeds 1.0 m/s; the robot body is unsafe if more **862** than 1% extends outside the containment region; and the end effector is unsafe if more than **863** 5% extends beyond containment. Containment regions are computed from the ground-truth dataset. 

16 

Under review as a conference <u>paper</u> at ICLR 2026 

### **864** 

## B.3 Models 

### **865** 

**866 OpenVLA.** We use four officially released OpenVLA checkpoints, each fine-tuned on one **867** of the four LIBERO task suites. 

> **868 WorldVLA.** We use four officially released WorldVLA checkpoints, each fine-tuned on one **869** of the four LIBERO task suites. We ran experiments with the default action chunking of 

> **870** 25; however, we observe that pruning leads to sometimes meaningless token outputs under 

> **871** this setting causing invalid actions for the robot to execute. For fairness, we instead set 

> **872** the action chunk size to 1, which increases evaluation time but provides a more reliable 

> **873** comparison. WorldVLA also allows varying the number of history images; we adopt the **874** default configuration of one history image together with the current image. **875 876** C Main Results **877** For LIBERO benchmarks, models are pruned with Wanda using a 15K calibration dataset 

> **878** drawn from the LIBERO fine-tuning corpus. For NAVILA, we use a 1K calibration dataset. 

> **879** The Memory-Matched Sparse Backbone prunes 75% of layers for OpenVLA and WorldVLA, 

> **880** and 81.3% of layers for NaVILA. It is important to note that in the Memory-Matched 

> **881** setting, although only a fraction of layers are pruned, the pruned layers still maintain 50% 

> **882** structured 2:4 sparsity. Since WorldVLA uses a convolution-based vision encoder, we do **883** not apply pruning to that component of the model. **884** C.1 GLUESTICK Manipulation Task Performance Recovery **885 886 887 Model Method Succ. (%) RAM (GB)** ∆ **Succ** . ∆ **RAM** 

> **888** OpenVLA Full Dense 85.2 16.12 +0.0 +0.00 

> **889** Full Sparse 0.0 10.17 -85.2 -5.95 **890** Sparse Lang. BB 31.2 10.56 -54.0 -5.56 **891** 75% Sparse Lang. BB 25.4 11.96 -59.8 -4.16 **892** GLUESTICK-200 49.0 11.18 -36.2 -4.94 **GLUESTICK-500 60.2 11.97 -25.0 -4.15 893** 

> **894** WorldVLA Full Dense 88.4 16.24 +0.0 +0.00 **895** Sparse Lang. BB 3.4 10.16 -85.0 -6.08 **896** 75% Sparse Lang. BB 5.0 12.16 -83.4 -4.08 **897 GLUESTICK-500 47.8 12.14 -40.6 -4.10 898 899** Table 7: **LIBERO Spatial: Performance.** ∆ columns are relative to each model’s Full **900** Dense baseline on this benchmark. Lang. BB = language backbone; Succ = Success. RAM is peak during inference on same hardware. **901 902** 

> **903 Model Method Succ. (%) RAM (GB)** ∆ **Succ** . ∆ **RAM 904** OpenVLA Full Dense 85.8 16.12 +0.0 +0.00 **905** Full Sparse 13.4 10.17 -72.4 -5.95 **906** Sparse Lang. BB 50.8 10.56 -35.0 -5.56 

> **907** 75% Sparse Lang. BB 49.0 11.96 -36.8 -4.16 

> **908** GLUESTICK-200 66.7 11.18 -19.1 -4.94 

> **909 GLUESTICK-500 71.2 11.97 -14.6 -4.15 910** WorldVLA Full Dense 80.4 16.24 +0.0 +0.00 **911** Sparse Lang. BB 0.8 10.16 -79.6 -6.08 

> **912** 75% Sparse Lang. BB 1.4 12.16 -79.0 -4.08 

> **913 GLUESTICK-500 25.2 12.14 -55.2 -4.10 914** 

> **915** Table 8: **LIBERO Object: Performance.** ∆ columns are relative to each model’s Full 

> **916** Dense baseline on this benchmark. Lang. BB = language backbone; Succ = Success. RAM 

> **917** is peak during inference on same hardware. 

17 

Under review as a conference <u>paper</u> at ICLR 2026 

**918 Model Method Succ. (%) RAM (GB)** ∆ **Succ** . ∆ **RAM 919 920** OpenVLA Full Dense 77.0 16.12 +0.0 +0.00 **921** Full Sparse 0.8 10.17 -76.2 -5.95 **922** Sparse Lang. BB 20.0 10.56 -57.0 -5.56 **923** 75% Sparse Lang. BB 20.8 11.96 -56.2 -4.16 GLUESTICK-200 30.4 11.18 -46.6 -4.94 **924 GLUESTICK-500 47.0 11.97 -30.0 -4.15 925 926** WorldVLA Full Dense 81.0 16.24 +0.0 +0.00 **927** Sparse Lang. BB 21.0 10.16 -60.0 -6.08 **928** 75% Sparse Lang. BB 21.6 12.16 -59.4 -4.08 **GLUESTICK-500 45.2 12.14 -35.8 -4.10 929 930** Table 9: **LIBERO Goal: Performance.** ∆ columns are relative to each model’s Full **931** Dense baseline on this benchmark. Lang. BB = language backbone; Succ = Success. RAM **932** is peak during inference on same hardware. **933 934 Model Method Succ. (%) RAM (GB)** ∆ **Succ** . ∆ **RAM 935 936** OpenVLA Full Dense 55.8 16.12 +0.0 +0.00 **937** Full Sparse 0.0 10.17 -55.8 -5.95 **938** Sparse Lang. BB 12.4 10.56 -43.4 -5.56 **939** 75% Sparse Lang. BB 11.4 11.96 -44.4 -4.16 GLUESTICK-200 16.2 11.18 -39.6 -4.94 **940 GLUESTICK-500 26.6 11.97 -29.2 -4.15 941 942** WorldVLA Full Dense 55.2 16.24 +0.0 +0.00 **943** Sparse Lang. BB 0.0 10.16 -55.2 -6.08 **944** 75% Sparse Lang. BB 0.0 12.16 -55.2 -4.08 **GLUESTICK-500 0.0 12.14 -55.2 -4.10 945 946** Table 10: **LIBERO Long: Performance.** ∆ columns are relative to each model’s Full **947** Dense baseline on this benchmark. Lang. BB = language backbone; Succ = Success. RAM **948** is peak during inference on same hardware. **949 950 951** It is worth noting that WorldVLA completely collapsed after pruning on LIBERO Long, **952** producing invalid action tokens and failing to generate meaningful outputs. Although task **953** success rates did not improve, GLUESTICK was able to restore the model to producing **954** more valid outputs. **955 956** Full Dense Full Sparse Sparse Language Backbone 81.3% Sparse Language Backbone Ours (Rank 500) **957 958 959 960** 0.08 **961** 0.06 **962 963** 0.04 **964 965** 0.02 **966 967** 0.00 0 10 20 30 40 0 10 20 30 40 **968** Path Length Distance to Goal **969 970** Figure 6: **Navigation Trajectory Quality.** Distribution of path lengths (left) and final **971** distances to goal (right) for pruned NaVILA models and GLUESTICK on VLN-CE-Isaac. 

18 

Under review as a conference <u>paper</u> at ICLR 2026 

**972 973** 

> **974** Full Dense trajectories remain short and goal-directed, while Full Sparse trajectories are **975** substantially longer and terminate farther from the goal, reflecting severe degradation in 

> **976** navigational ability (See Figure 6). In contrast, GLUESTICK–500 closely matches the Full 

> **977** Dense distribution, indicating that it restores not only success rates but also the efficiency **978** and precision of navigation behavior. **979 980** D Analysis **981 982 983** D.1 Calibration Set Selection **984 985 986 987 988 989 990 991 992 993 994 995 996 997 998 999 1000 1001** Figure 7: **Calibration Set Visualization.** LIBERO Spatial calibration trajectories. full 

> **1002** trajectories (left) 5% window around the first gripper-closing event, with red segments mark- 

> **1003** ing closed-gripper states (right). **1004 1005 1006** The influence of calibration data on pruning outcomes in robotics remains largely underex- **1007** plored. To investigate its impact, we studied how the calibration set choice affects Wanda’s **1008** baseline pruning performance before applying GLUESTICK. Specifically, we pruned the lan- **10091010** guageWanda with 15K states from the LIBERO fine-tuning corpus.backbone of OpenVLA with Wanda and evaluated on LIBEROWe then constructed a smallerSpatial. We provided but more targeted calibration set consisting of 3.5K states within a 5% window around the 

> **1011** first gripper-closing event (Figure 7). Our experiments show that the more targeted cali- 

> **1012** bration set improved the pruned language backbone’s success rate on LIBERO Spatial from 

> **1013** 31.2% to 33.4%, a gain of about 2%. We adopt this strategy as part of GLUESTICK. 

> **1014** Interestingly, the smaller calibration set yielded a slightly higher success rate. **1015 1016** D.2 Singular Value Selection **1017 1018** We ask whether there is an optimal criterion for selecting singular values. All results reported **1019** in this paper use the top- _r_ singular components ranked by magnitude. To test alternatives, 

> **1020** we conducted an experiment where, for GLUESTICK-200 on a fully sparse language back- 

> **1021** bone, singular values were instead chosen uniformly at random. In this setting, the model 

> **1022** recovered only _∼_ 10% of the task success achieved by the magnitude-based selection. This 

> **1023** indicates that the choice of singular values is highly influential, with selecting the largest **1024** components by magnitude playing a central role in effective recovery. However, different **1025** singular values may capture complementary subspaces in weight space, and future work could explore whether alternative selection criteria better preserve metrics such as safety. 

## C.2 GLUESTICK Navigation Task Performance Recovery 

19 

Under review as a conference <u>paper</u> at ICLR 2026 

**1026** D.3 Model Parameter Analysis **1027 1028** We apply GLUESTICK to linear layers because linear layers generally make up the vast **1029** majority of parameters in recent VLA models as shown in Table 11. **1030 1031 Model Total Parameters Linear Parameters Conv. Parameters 1032 1033 OpenVLA** 7,541,237,184 7,407,513,280 (98.23%) 1,281,664 (0.02%) **1034 WorldVLA** 7,042,582,528 6,744,440,832 (95.77%) 27,310,848 (0.39%) **1035 NaVILA** 8,494,180,416 7,962,922,816 (93.75%) 678,528 (0.01%) **1036 1037** Table 11: **Parameter composition of recent VLA models.** Across OpenVLA, World- **1038** VLA, and NaVILA, the vast majority of parameters ( **93–98%** ) are contained in linear layers, while convolutional components represent well under 1% of total model size. **1039 1040 1041** D.4 Compatibility with other Compression Methods **1042 1043** GLUESTICK is compatible with other compression techniques. To demonstrate this, we **1044** conducted an additional ablation experiment of Int8 quantization and GLUESTICK on **1045** OpenVLA evaluated on LIBERO Spatial. **1046 1047 Method D D/Int8 S S/Int8 S/Int8/GLUESTICK 1048** Success Rate (%) 85.2 84.8 31.2 31.8 62.2 **1049 1050** Table 12: **Effect of combining pruning, quantization, and GLUESTICK.** Success **1051** rates under five configurations: dense baseline (D), sparse language backbone (S), Int8 **1052** quantized dense model, Int8 quantized sparse backbone, and GLUESTICK applied on top **1053** of Int8–sparse weights. Evaluated on LIBERO Spatial. **1054 1055** The results in Table 12 show that quantization has a minor impact on the success rate of both **1056** dense and sparse models. However, the pruning degradation remains severe for quantized **1057** models. GLUESTICK provides a substantial recovery +31% even under quantization. **1058 1059** D.5 Manipulation vs Navigation Tolerance **1060 1061** In the navigation domain, small deviations in the robot’s trajectory often have minimal **1062** impact on final success. By contrast, manipulation tasks require fine-grained, centimeter- **1063** level control. As a result, even tiny trajectory deviations can cause complete task failure in **1064** manipulation tasks (e.g., slightly off from the grasp point of an object). This fundamental **1065** difference results in significantly different error tolerances between the two domains. To **1066** make this intuition more concrete, we compared the average difference in trajectory length **1067** between successful and unsuccessful episodes in each domain. **1068 1069 Domain Avg. Path-Length Differences 1070 1071 Manipulation** 0.018 m **1072 Navigation** 3.292 m **10731074** Table 13: **Average path-length difference between successful and failed episodes 1075** in manipulation and navigation tasks. Manipulation failures occur with deviations as small as centimeters, whereas navigation tolerates multi-meter deviations. **1076 1077** The measurements in Table 13 demonstrate that manipulation success relies on precise **1078** control, where deviations as small as a centimeter can lead to failure. In contrast, navigation **1079** operates in a low-precision control regime, where deviations up to several meters in size can still lead to successful outcomes. 

Table 11: **Parameter composition of recent VLA models.** Across OpenVLA, WorldVLA, and NaVILA, the vast majority of parameters ( **93–98%** ) are contained in linear layers, while convolutional components represent well under 1% of total model size. 

20 

Under review as a conference <u>paper</u> at ICLR 2026 

**1080** D.6 Weight Only Decomposition **1081 1082** In Table 14, all entries are computed without applying any pruning. These results show that **1083** directly applying SVD to the dense weights discards too much task-relevant information, **1084** causing the model to fail. However, the pruned weight matrix retains essential structural in- **1085** formation that SVD-based corrections can build upon, explaining why our approach requires **1086** starting from the pruned model rather than a purely low-rank one. **1087 1088 Rank 200 400 500 800 1000 2000 2500 1089** Success Rate (%) 0 0 0 0 0 0.4 21.0 **1090 1091** Table 14: Effect of replacing VLA weights with a lower rank approximation using SVD **1092** without pruning. **1093 1094** D.7 FLOP Analysis **1095 1096** As displayed in Table 15 sparse models reduce compute substantially, and GLUESTICK introduces only a modest FLOP increase relative to the sparse baseline. **1097 1098 1099 Method Total FLOPs (T) 1100** Full Dense 29.32 **1101** 50% 2:4 Pruned OpenVLA 16.54 **1102** 50% 2:4 Pruned OpenVLA + GLUESTICK-200 18.51 **1103** 50% 2:4 Pruned OpenVLA + GLUESTICK-500 21.47 **1104 1105** Table 15: **FLOP analysis for a single inference pass through OpenVLA. 11061107** FLOP _aten._scaled_dot_product_flash_attention_ counters for the following operations:, _aten.mmaten.convolution_ , and _aten.bmm_ , _aten.add_ . In these, _aten.addmm_ experiments, the language backbone of OpenVLA was pruned with Wanda. **1108 1109 1110** E Discussion **1111 1112** E.1 GLUESTICK and LoRA Differences **1113 1114** While both GLUESTICK and LoRA introduce low-rank matrices, they address fundamen- **1115** tally different problems and operate in distinct ways. LoRA is designed for efficient fine- **1116** tuning, whereas GLUESTICK is designed for post-pruning recovery. Although both meth- **1117** ods use low-rank matrices, these components are derived very differently. LoRA’s low-rank **1118** matrices must be _learned_ through gradient-based training over a dataset, while GLUE- **1119** STICK requires _no training at all_ . Instead of learning parameters, GLUESTICK computes **1120** the exact gap between the dense and pruned weight matrices and constructs a low-rank approximation of this gap. Although both methods add a term to the layer’s output at **1121** inference time, the source of the information they inject is entirely different. LoRA injects **1122** information learned from data during fine-tuning, whereas GLUESTICK injects information **1123** derived analytically from the dense–pruned gap. There is no overlap in how the low-rank **1124** components are obtained or what problems they are intended to solve. **1125 1126** F Use of LLMs **1127 1128** LLMs were used to assist with grammar checking and correcting typos during the prepara- **1129** tion of this paper. **1130 1131 1132 1133** 

21 

