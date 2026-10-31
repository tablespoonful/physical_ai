---
title: "FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions"
date: "2026-01-19"
authors: "Peng Li; Zihan Zhuang; Yangfan Gao; Yi Dong; Sixian Li; Changhao Jiang"
url: https://arxiv.org/abs/2601.12799
pdf: https://arxiv.org/pdf/2601.12799
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.12799)** / [論文ページ](https://arxiv.org/abs/2601.12799)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Fudan NLP Lab 

OpenMOSS 

_2026-1-21_ 


## **FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions** 

**Peng Li**<sup>1</sup><sup>_,_2∗†</sup> **Zihan Zhuang**<sup>1∗†</sup> **Yangfan Gao**<sup>1∗</sup> **Yi Dong**<sup>1∗</sup> **Sixian Li**<sup>1</sup><sup>_,_2</sup> **Changhao Jiang**<sup>1</sup> **Shihan Dou**<sup>1</sup> **Zhiheng Xi**<sup>1</sup> **Enyu Zhou**<sup>1</sup> **Jixuan Huang**<sup>1</sup> **Hui Li**<sup>1</sup> **JingJing Gong**<sup>2</sup> **Xingjun Ma**<sup>1</sup><sup>_,_2</sup> **Tao Gui**<sup>1�</sup> **Zuxuan Wu**<sup>1</sup><sup>_,_2</sup> **Qi Zhang**<sup>1</sup> **Xuanjing Huang**<sup>1</sup> **Yu-Gang Jiang**<sup>1</sup> **Xipeng Qiu**<sup>1</sup><sup>_,_2�</sup> 1Fudan University 2Shanghai Innovation Institute 

pengli@sii.edu.cn, {zhzhuang24, gaoyf24, yidong25, sxli25, chjiang25}@m.fudan.edu.cn {tgui, xpqiu}@fudan.edu.cn 

Fully Open-Sourced at https://openmoss.github.io/FRoM-W1 


**Figure 1** | (a) We introduce FRoM-W1, an open-source framework that leverages Chain-of-Thought (CoT) reasoning to achieve general language-guided hand-inclusive humanoid whole-body control. (b) Based on a 9B instruction to human-motion model H-GPT, FRoM-W1 can generate diverse humanoid whole-body motions. (c) Through its H-ACT module which has been pre-trained and fine-tuned through reinforcement learning (RL), FRoM-W1 grounds generated human whole-body motions to various humanoid robots such as the Unitree H1, G1, and Fourier GR1T1, and enables them to execute corresponding motions accurately and stably in the physical world. 

*Equal contribution. †Project Lead. �Corresponding authors. 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

#### **Abstract** 

**Humanoid robots are capable of performing various actions such as greeting, dancing and even backflipping. However, these motions are often hard-coded or specifically trained, which limits their versatility. In this work, we present** FRoM-W1 **, an open-source framework designed to achieve general humanoid whole-body motion control using natural language. To universally understand natural language and generate corresponding motions, as well as enable various humanoid robots to stably execute these motions in the physical world under gravity,** FRoM-W1 **operates in two stages: (a)** H-GPT **: utilizing massive human data, a large-scale language-driven human whole-body motion generation model is trained to generate diverse natural behaviors. We further leverage the Chain-of-Thought technique to improve the model’s generalization in instruction understanding. (b)** H-ACT **: After retargeting generated human whole-body motions into robot-specific actions, a motion controller that is pretrained and further fine-tuned through reinforcement learning in physical simulation enables humanoid robots to accurately and stably perform corresponding actions. It is then deployed on real robots via a modular simulation-to-reality module. We extensively evaluate** FRoM-W1 **on Unitree H1 and G1 robots. Results demonstrate superior performance on the HumanML3D-X benchmark for human whole-body motion generation, and our introduced reinforcement learning fine-tuning consistently improves both motion tracking accuracy and task success rates of these humanoid robots. We open-source the entire** FRoM-W1 **framework and hope it will advance the development of humanoid intelligence.** 

### **1. Introduction** 

Humanoid robots, such as Unitree’s H1 and G1, feature an anthropomorphic design that mimics the human form, enabling them to operate and interact seamlessly in environments around us [1, 2]. Current technologies allow these robots to perform impressive motions—including greeting gestures, dancing, practicing kung fu, and even executing backflip. However, such capabilities are typically achieved through hardcoded trajectories or task-specific reinforcement learning, often controlled via handheld devices [3–8]. These approaches limit the humanoid robot’s ability to autonomously perceive and interact with the external world, particularly with humans. To enable natural humanrobot interaction, this work addresses the following core research question: **How can humanoid robots comprehend diverse natural language instructions and execute corresponding wholebody motions in the real physical world?** 

Achieving this goal presents two major challenges. First, like current large language models (LLMs) [9–12], achieving general language understanding and motion generation typically requires vast data and training large models. But there is a scarcity of large-scale paired robot datasets that associate language instructions with whole-body humanoid motions [13–15]. Second, even if a foundation model were trained to generate robot motions from natural language, directly executing these motions on physical bipedal humanoid robots would likely lead to instability and falls due to gravity and dynamic uncertainties [16, 17]. 

Inspired by the analogous roles of the human cerebrum and cerebellum in functions such as semantic comprehension and motion planning, as well as in stable motor execution [18, 19], we propose the FRoM-W1<sup>1</sup> framework to address these challenges, as illustrated in Figure 2. First, although a large-scale annotated humanoid motion dataset is unavailable, the morphological similarity between humanoid robots and humans enables us to leverage extensive language-labeled 

> 1“FRoM-W1” denotes Foundational Humanoid Robot Model – Whole-Body Control, Version 1”. 

2 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 


**Figure 2** | The inference pipeline of FRoM-W1. (a) H-GPT first translates language instructions into fine-grained action descriptions through CoT, then generates corresponding whole-body human motion sequences. (b) After obtaining the human SMPL-X motions through inverse kinematics (IK), H-ACT retargets the generated human motion sequences into robot-specific motions. Then, through a reinforcement learning pre-trained (RPT) and fine-tuned (RFT) whole-body motion controller, H- ACT enables the humanoid robot to perform the corresponding actions in the physical world. 

human motion data from motion capture and videos [20–22]. Based on these resources, we employ the vector quantized variational autoencoder (VQ-VAE) technique [23] as used in T2M-GPT [24] and MotionGPT [25] to first convert human whole-body motion sequences, including hand movements, into token sequences aligned with language tokens. Based on the LLaMA-3.1 LLM [11], we train a generative model termed H-GPT, which synthesizes whole-body human motions from natural language instructions like _“Play the role of an elephant!”_ . Chain-of-Thought (CoT) [26, 27] technology is used to decompose each instruction into body-level motion primitives with explicit temporal structure, enabling the model to convert abstract or complex instructions into simple, unified textual representations that facilitate motion generation. Next, to enable humanoid robots of different morphologies to accurately and stably execute the generated human motions, we first retarget the human whole-body SMPL-X motions [28] to each specific robot platform. Drawing inspiration from prior work on motion mimicking [13, 29–31], we then train a whole-body humanoid controller via reinforcement learning in the physical simulation Isaacgym [32]. In addition to large-scale pretraining of general motion controllers, we further introduce reinforcement learning fine-tuning (RFT) during the inference phase, enabling the controller to more accurately track the generated motions while maintaining whole-body stability. Finally, we deploy the controller to various physical humanoid robots using a modular deployment interface. We refer to these humanoid motion execution components collectively as H-ACT. 

We conducted a comprehensive evaluation of the proposed framework using the Unitree H1 and G1 robots. On our constructed instruction to human whole-body motion generation benchmark HumanML3D-X, the framework achieved a 2.5-fold improvement in the primary metric Frechet Inception Distance (FID) compared to the baseline model T2M-GPT [24]. We have also developed a motion generation generalization evaluation benchmark called _𝛿_ HumanML3D-X and validated the effectiveness of incorporating the CoT method. Moreover, we evaluated the effectiveness of our reinforcement learning fine-tuning strategy for the controller, which not only consistently increased 

3 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

the motion tracking success rate but also delivered a 15% improvement in the accuracy metric Mean Per-joint Joint Position Error (MPJPE). Furthermore, we demonstrate the versatility of our designed sim2real framework for humanoid robots. In addition to supporting our default control policy deployment, it also universally enables the efficient deployment of several recent motion mimicing controllers, such as HugWBC [33] and TWIST [30]. 

Overall, the main contributions of FRoM-W1, a framewzork that enables whole-body control of humanoid robots using natural language instructions, are as follows: 

- We introduce H-GPT, a 9B model that generates high quality whole-body human motions from natural language instructions. Enhanced with CoT technology, it achieves versatile instruction understanding. H-GPT demonstrates superior accuracy and generalization in human wholebody motion generation on our established HumanML3D-X and _𝛿_ HumanML3D-X benchmarks. 

- We propose H-ACT, a module that spans from human-to-humanoid motion retargeting to humanoid policy deployment, enabling humanoid robots to accurately and stably perform wholebody motions generated by H-GPT. The novel two-stage RL strategy of pretraining and finetuning allows the robot to more precisely track the corresponding motion. 

- We fully open-source the complete framework, including the H-GPT and H-ACT model training code, model checkpoints, evaluation benchmarks, and a lightweight deployment module, to facilitate further research and development in language-guided whole-body control for humanoid robots. 

### **2.** FRoM-W1 

In this section, We detail the design of the FRoM-W1 framework. We begin by introducing the task of whole-body motion control of humanoid robots using natural language instructions in Section 2.1. Then, in Section 2.2, we elaborate on the design and training of the instruction to wholebody human motion generation model H-GPT. In Section 2.3, we describe H-ACT, covering its human-to-humanoid retargeting, reinforcement learning pre-training and fine-tuning, and the modular framework for deployment on real humanoid robots. 

##### **2.1. Task Formulation** 

Our goal is to enable a physical humanoid robot to perform whole-body motions based on open-ended natural language instructions. The core task is to learn a mapping from a language instruction _𝐼_ ∈I like _“Play the role of an elephant!”_ to a sequence of executable and stable humanoid robot actions _𝐴𝑟_ ∈A _𝑟_ . This task is decomposed into two sequential stages, corresponding to the H-GPT and H-ACT modules of our framework: 

**Stage 1: Language to Whole-Body Human Motion (** H-GPT **).** Given an instruction _𝐼_ , generate a semantically aligned and physically plausible whole-body human motion sequence _𝑀ℎ_ ∈M _ℎ_ . This stage learns the mapping GH-GPT : I →M _ℎ_ . 

**Stage 2: Human Motion to Humanoid Execution (** H-ACT **).** Given the generated human motion _𝑀ℎ_ , execute it stably on a target humanoid robot. This stage learns the mapping: AH-ACT : M _ℎ_ → A _𝑟_ . The function AH-ACT encompasses: 1) Kinematic retargeting R to adapt the human motion _𝑀ℎ_ to the humanoid robot’s morphology, producing _𝑀𝑟_ ∈M _𝑟_ , i.e., _𝑅_ : M _ℎ_ →M _𝑟_ and 2) A humanoid whole-body control policy _𝜋𝜃_ that tracks the motion _𝑀_ r and produces actions _𝐴𝑟_ , i.e., _𝜋𝜃_ : M _𝑟_ →A _𝑟_ , while maintaining dynamic stability. 

The complete pipeline is the composition: Π( _𝐼_ ) = AH-ACT(GH-GPT( _𝐼_ )). This formulation lever- 

4 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 


**Figure 3** | Overview of the H-GPT. During **training** phase, data triplets <I, COT ,M _ℎ_ > are tokenized and fed into the motion generator, where the motion sequences are encoded and discretized by the encoder E and the quantizer _𝑄_ of the whole-body motion tokenizer. During **inference** phase, the motion generator produces CoT and motion tokens given a specific instruction. These motion tokens are then decoded to a motion sequence by the decoder D of the tokenizer. 

ages human motion as an intermediate, semantically rich representation to bridge the gap between language and stable humanoid robot control. 

##### **2.2. H-GPT** 

The H-GPT module serves as the language-to-human-motion generator in the first stage of the FRoM-W1 pipeline, learning the mapping GH-GPT : I →M _ℎ_ . It synthesizes diverse and semantically consistent whole-body human motions from natural language instructions by employing a whole-body human motion tokenizer and an LLM-based auto-regressive motion generator. Figure 3 illustrates the training and inference pipeline of H-GPT. 

##### **_2.2.1. Dataset Augmentation and Enrichment_** 

Let Draw = {( _𝐼𝑖, 𝑀ℎ,𝑖_ )} _𝑖_<sup>_𝑁_</sup> =1<sup>denotearawdatasetof</sup><sup>_𝑁_samples,where</sup><sup>_𝐼𝑖_∈Iisanaturallanguage</sup> instruction and _𝑀ℎ,𝑖_ ∈M _ℎ_ is a corresponding whole-body human motion sequence. While such paired data for humanoids is scarce, several large-scale datasets exist for whole-body human motion, e.g., HumanML3D [20] and Motion-X [21]. A key limitation is that the instruction space I in these datasets is often semantically narrow, consisting primarily of simple, concrete action descriptions (e.g., “walk forward”, “raise arms”) that lack the diversity and abstraction required for open-ended instructions like _“Please play the role of an elephant!”_ . 

To bridge this semantic gap, we propose an LLM-augmented dataset transformation. We leverage a powerful large language model LLM(·) (specifically the OpenAI’s GPT-4o) to enrich each sample. For each original pair ( _𝐼𝑖, 𝑀ℎ,𝑖_ ), we generate a structured Chain-of-Thought (CoT) [26] sequence _𝐶𝑜𝑇𝑖_ ∈COT that decomposes and elaborates the instruction into explicit, temporally-aware motion primitives: _𝐶𝑜𝑇𝑖_ = LLM( _𝐼𝑖, 𝑃_ ), where _𝑃_ is a prompt template designed to elicit a step-by-step motion reasoning process. This yields an enriched dataset Denriched = {( _𝐼𝑖, 𝐶𝑜𝑇𝑖, 𝑀𝑖_ )} _𝑖_<sup>_𝑁_</sup> =1<sup>.</sup> 

The CoT sequence _𝐶𝑜𝑇𝑖_ serves as a semantic intermediary that aligns high-level or abstract language with low-level motion patterns. During training, the LLM-based auto-regressive generation 

5 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

model can learn the distribution _𝑝_ (M _ℎ,_ COT |I) = _𝑝_ (M _ℎ_ |I _,_ COT) · _𝑝_ (COT |I) by aligning the CoT sequence space C with corresponding human motion sequence space M _ℎ_ . During inference, for a novel instruction _𝐼_ new, the model first generates a CoT _𝐶𝑜𝑇_ new via its internal reasoning capabilities, which then conditions the auto-regressive generation of the motion sequence _𝑀_ new. This approach efficiently leverages the intrinsic language comprehension and generation capabilities of LLM base models to extend the original instruction space I to a CoT space COT that is more directly aligned with the target human motion space M _ℎ_ , enabling the whole-body human motion generator robust generalization to complex, open-ended commands. 

##### **_2.2.2. Whole-Body Human Motion Tokenizer_** 

In order to achieve language-guided whole-body human motion generation based on the comprehension and sequence modeling capabilities of existing LLMs such as the LLaMA model [11], we first train a whole-body human motion sequence tokenizer using VQ-VAE technology [23]. This tokenizer represents a human motion sequence _𝑀ℎ_ = {p _ℎ,_ 1 _, . . . ,_ p _ℎ,𝑇_ } ∈ ℝ<sup>_𝑇_×</sup><sup>_𝐷_</sup> as a sequence of discrete motion tokens _𝐶_<sup>ˆ</sup> = {ˆ _𝑐_ 1 _, . . . ,_ ˆ _𝑐𝐿_ } ∈ C<sup>ˆ</sup> , where p _ℎ,𝑖_ ∈ ℝ<sup>_𝐷_</sup> denotes the pose representation of the human at time _𝑖_ , and ˆ _𝑐𝑖_ ∈{1 _, . . . , 𝐾_ } refers to the _𝑖_ -th token code id, aligning its format with that of linguistic tokens for subsequent LLM processing. 

The tokenizer performs discrete representation through encoding, quantization, and decoding steps. An encoder E first performs spatio-temporal downsampling: E : ℝ<sup>_𝑇_×</sup><sup>_𝐷_</sup> → ℝ<sup>_𝐿_×</sup><sup>_𝑑_</sup> maps the sequence _𝑀ℎ_ to latent vectors _𝑍_ = {z1 _, . . . ,_ z _𝐿_ }, where _𝐿_ = ⌊ _𝑇_ / _𝑙_ ⌋ and _𝑙_ is the temporal downsampling factor. A vector quantizer Q discretizes each latent vector z _𝑖_ by mapping it to the nearest entry in a learnable codebook _𝐶_ = {ˆz1 _, . . . ,_ ˆz _𝐾_ } ⊂ ℝ<sup>_𝑑_</sup> , producing a corresponding codebook index ˆ _𝑐𝑖_ . The operation is defined as ˆ _𝑐𝑖_ = Q(z _𝑖_ ) = arg min ∥z _𝑖_ − ˆz _𝑘_ ∥2. The resulting sequence of _𝑘_ ∈{1 _,...,𝐾_ } 

codebook indices _𝐶_<sup>ˆ</sup> = {ˆ _𝑐_ 1 _, . . . ,_ ˆ _𝑐𝐿_ } constitutes the discrete motion tokens. Finally, a decoder D reconstructs the original motion sequence from the corresponding codebook vectors, producing _𝑀_ ˜ _ℎ_ = D(ˆzˆ _𝑐_ 1 _, . . . ,_ ˆzˆ _𝑐𝐿_ ) = {ˆp _ℎ,_ 1 _, . . . ,_ ˆp _ℎ,𝑇_ } ∈ ℝ<sup>_𝑇_×</sup><sup>_𝐷_</sup> . 

To train this motion tokenizer, we follow common practice [24, 25, 34] by using the weighted sum of three loss functions as the training objective: reconstruction loss L _𝑟𝑒𝑐𝑜𝑛_ , commitment loss L _𝑐𝑜𝑚𝑚𝑖𝑡_ , and codebook loss L _𝑐𝑜𝑑𝑒𝑏𝑜𝑜𝑘_ . We also employ exponential moving average (EMA) updates for the codebook and a code reset mechanism to mitigate codebook collapse [35]. 

##### **_2.2.3. Whole-Body Human Motion Generator_** 

The whole-body human motion generator, as the core component of H-GPT, is responsible for the auto-regressive generation of a coherent motion token sequence conditioned on a natural language instruction. It learns the distribution _𝑝_ (C<sup>ˆ</sup> _,_ COT | I), where C<sup>ˆ</sup> is the discrete motion token sequence space derived from the motion tokenizer (Section 2.2.2). The generator is based on pretrained LLMs with an expanded vocabulary _𝑉_ = _𝑉_ text ∪ _𝑉_ motion. Here, _𝑉_ text is the original text token vocabulary of the base LLM, and _𝑉_ motion is a set of _𝐾_ new tokens corresponding to the motion codebook indices. This unified representation enables seamless interleaving of text (instructions and CoT) and motion tokens within a single sequence, transforming motion generation into a standard next-token prediction task. 

During training, as illustrated in Figure 3, the model processes sequences in the Denriched structured as: “[Instruction] _𝐼_ [Chain-of-Thought] _𝐶𝑜𝑇_ [Motion Tokens] _𝐶_<sup>ˆ</sup> ”. The entire sequence is tokenized using the combined vocabulary _𝑉_ . The model is trained with a standard language modeling objective to maximize the likelihood of the target sequence (CoT and motion tokens) given the instruction. Let Θ denote the frozen parameters of the pre-trained backbone LLM like the LLaMA-3.1 

6 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 


**Figure 4** | Overview of the human-to-humanoid motion retargeting pipeline. (a) We first convert the 3D coordinates of the full-body keypoints into the SMPL-X representation expressed in axisangle format. (b) For body retargeting, we follow PHC to align global body poses, and additionally incorporate a rotation loss to compute wrist joint orientations. (c) For hand retargeting, we formulate an optimization objective that aligns fingertip positions and solve it to obtain the final hand poses. 

model [11], and ΔΘ denote the parameters of Low-Rank Adaptation (LoRA) modules [36] injected into the attention layers. The training loss is: 


where _𝑡𝑜𝑘𝑒𝑛<𝑖_ represents all preceding tokens in the sequence and _𝑡𝑜𝑘𝑒𝑛𝑖_ is the current token to be predicted, and _𝑇_ is the token sequence length. This objective allows the model to learn the mapping from language to motion through the intermediate CoT representation, leveraging the world knowledge and reasoning capabilities of the base LLM while efficiently adapting it to the motion domain via parameter-efficient fine-tuning. 

During inference for a novel instruction _𝐼_ new, the model performs auto-regressive generation in two phases, mirroring the learned sequence structure. First, it generates the Chain-of-Thought _𝐶𝑜𝑇_ new conditioned on _𝐼_ new. Subsequently, conditioned on both _𝐼_ new and the generated _𝐶𝑜𝑇_ new, it generates the sequence of motion tokens _𝐶_<sup>ˆ</sup> new. The generated motion tokens _𝐶_<sup>ˆ</sup> new are then passed to the decoder _𝐷_ of the pre-trained motion tokenizer to reconstruct the corresponding continuous human motion sequence _𝑀_<sup>˜</sup> _ℎ_ . This generated motion is semantically aligned with the instruction and serves as the input for the subsequent H-ACT module for robot execution. 

##### **2.3. H-ACT** 

The H-ACT module is designed to enable humanoid robots to stably execute the whole-body motion sequence _𝑀_<sup>˜</sup> _ℎ_ generated by the H-GPT module in the physical world. It mainly consists of three modules: a retargeter module _𝑅_ that converts whole-body human motion representations _𝑀_<sup>˜</sup> _ℎ_ into motion sequences for a specific robot structure _𝑀_<sup>˜</sup> _𝑟_ ; a policy module _𝜋𝜃_ trained via reinforcement learning in a physical simulation environment to stably track the retargeted humanoid motion sequences under factors such as gravity; and a lightweight, modular sim2real policy deployment framework that efficiently deploys the simulation-trained policy to the physical robot. 

##### **_2.3.1. Human-to-Humanoid Whole-Body Motion Retargeter_** 

To enable the physical humanoid robot to execute the whole-body human keypoint motion _𝑀_<sup>˜</sup> _ℎ_ generated by H-GPT, it is necessary to bridge the morphological gap between the human body and the robot structure. Our retargeting pipeline R transforms _𝑀_<sup>˜</sup> _ℎ_ = { ˆ _𝑝ℎ,_ 1 _, . . . ,_ ˆ _𝑝ℎ,𝑇_ } into a feasible robot 

7 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

joint-angle trajectory _𝑀_<sup>˜</sup> _𝑟_ = { _𝑞_ ˆ _𝑟,_ 1 _, . . . ,_ ˆ _𝑞𝑟,𝑇_ } through a two-stage process: first reconstructing a parametric human whole-body model SMPL-X [28] pose sequences { _𝑞_ ˆ _ℎ,_ 1 _, . . . ,_ ˆ _𝑞ℎ,𝑇_ } from the 3D human motion position sequences _𝑀_<sup>˜</sup> _ℎ_ , and then optimizing the humanoid robot pose sequences _𝑀_<sup>˜</sup> _𝑟_ to align with this reconstructed sequences. 

We employ an inverse kinematics approach based on the HybrIK method [37] to reconstruct _𝑡_ -th SMPL-X pose _𝑞_ ˆ _ℎ,𝑡_ from the _𝑡_ -th 3D keypoint positions ˆ _𝑝ℎ,𝑡_ ∈ ℝ<sup>_𝑁_×3</sup> contained in _𝑀_<sup>˜</sup> _ℎ_ . For each joint _𝑖_ with parent _𝑝_ ( _𝑖_ ), a rotation matrix _𝑅𝑖_ in the 3D Special Orthogonal Group _𝑆𝑂_ (3) is computed to align its template bone vector _𝑡𝑖_ with the observed direction _𝑝𝑖_ = ˆ _𝑝ℎ,𝑡,𝑖_ − ˆ _𝑝ℎ,𝑡,𝑝_ ( _𝑖_ ) . For joints with a single child, _𝑅𝑖_ is obtained via Rodrigues’ formula [38]: 


where _𝐾_ is the skew-symmetric matrix of the rotation axis _𝑘_ = ∥ _𝑡𝑡𝑖𝑖_ ×× _<u>𝑝𝑝𝑖𝑖</u>_ ∥<sup>and</sup><sup>_𝜃_=arccos(</sup> ∥ _𝑡𝑖𝑡_ ∥∥ _<u>𝑖</u>_ · _<u>𝑝𝑝𝑖</u> 𝑖_ ∥<sup>).For</sup> joints with multiple children (e.g., the pelvis), the rotation is obtained by solving the orthogonal Procrustes problem: min _𝐹_<sup>_,_</sup> (3) _𝑅𝑖_ ∈ _𝑆𝑂_ (3)<sup>∥</sup><sup>_𝑅𝑖𝑇_−</sup><sup>_𝑃_∥2</sup> 

where the template matrix _𝑇_ ∈ ℝ<sup>3×</sup><sup>_𝑚_</sup> and the observed matrix _𝑃_ ∈ ℝ<sup>3×</sup><sup>_𝑚_</sup> are constructed from the _𝑚_ child bone vectors. The solution, via singular value decomposition (SVD) _𝑃𝑇_<sup>⊤</sup> = _𝑈_ Σ _𝑉_<sup>⊤</sup> , is given by _𝑅𝑖_ = _𝑈𝑉_<sup>⊤</sup> . Rotation matrices are computed hierarchically from the root outward and subsequently converted into the SMPL-X pose parameter representation _𝑞_ ˆ _ℎ,𝑡_ , where each primitive represents the angle of a joint. 

The reconstructed SMPL-X human whole-body motion is then mapped to the robot’s joint space. For each frame _𝑡_ , we solve for the robot joint angles _𝑞_ ˆ _𝑟,𝑡_ that best align selected robot joints with their corresponding human joints. This is formulated as an optimization problem that minimizes positional and orientational discrepancies while respecting robot constraints: 


where FK _𝑟_<sup>_𝑗𝑟_(·)denotes the forward kinematics function for robot joint</sup><sup>_𝑗_</sup> _𝑟_<sup>,ˆ</sup><sup>_𝑝_</sup> _𝑗ℎ,𝑡_<sup>and R</sup> _𝑗ℎ,𝑡_<sup>are the target</sup> position and orientation derived from the human SMPL-X pose _𝑞_ ˆ _ℎ,𝑡_ , the human root transition _𝑝𝑟𝑜𝑜𝑡_ and root orientation _𝑜𝑟𝑜𝑜𝑡_ , _𝑑_ (· _,_ ·) is the geodesic distance on _𝑆𝑂_ (3), P is the set of corresponding human-robot joint pairs, and R _𝑟_ ( _𝑞_ ˆ _𝑟,𝑡_ ) is a regularizer enforcing joint limits and other robot-specific feasibility constraints. The resulting sequence of joint angles _𝑀_<sup>˜</sup> _𝑟_ = { _𝑞_ ˆ _𝑟,_ 1 _, . . . ,_ ˆ _𝑞𝑟,𝑇_ }, as well as the root information _𝑝𝑟𝑜𝑜𝑡,𝑡_ and _𝑜𝑟𝑜𝑜𝑡,𝑡_ serves as the reference motion for the downstream whole-body control policy. In implementation, for body retargeting, we follow PHC [39] to align global body poses, and additionally incorporate a rotation loss to compute wrist joint orientations. For hand retargeting, we formulate an optimization objective that aligns fingertip positions and solve it to obtain the final hand poses. 

##### **_2.3.2. RL-based Motion Imitator: Pre-Training and Fine-Tuning_** 

As shown in Figure 5, to enable the physical execution of a retargeted motion sequence _𝑀_<sup>˜</sup> _𝑟_ on a humanoid robot, we learn a robust whole-body control policy _𝜋𝜃_ using a two-stage RL framework in the IsaacGym simulator [32]. The policy maps the robot’s proprioceptive state _𝑠𝑡_ and a motion command _𝑐𝑡_ —comprising reference root position _𝑝_ root _,𝑡_ , orientation _𝑜_ root _,𝑡_ , and target joint angles _𝑞_ ˆ _𝑟,𝑡_ —to motor actions _𝑎𝑡_ . While existing methods predominantly focus on pre-training a general motion controller [13, 29–31], we argue that fine-tuning the policy at inference time for a specific target motion can further improve tracking accuracy and robustness. 

8 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 


**Figure 5** | Overview of the H-ACT. During the pre-training and fine-tuning phase, retargeted motion datasets are used in simulation to train a privileged teacher tracking policy. Through DAgger distillation, a sim-to-real student policy is trained with simplified motion goals; During the deployment phase, the generated humanoid motion is adapted to motion goals for different policy variants. A decoupled design with a unified interface enables seamless sim-to-sim transfer and sim-to-real deployment. 

**RL Pre-Training (RPT)** We first train a generalist policy using a large dataset of retargeted human _𝑁_ pt motions Dpt = { _𝑀_<sup>˜</sup> _𝑟_<sup>(</sup><sup>_𝑖_)}</sup> _𝑖_ =1<sup>fromAMASS[40].FollowingtheOmniH2Oapproach[29],weadopta</sup> teacher-student distillation paradigm. A teacher policy _𝜋𝜙_ , conditioned on privileged information (e.g., full state and future reference motions), is trained to maximize a cumulative reward across the entire pre-training dataset. The objective consists of three key components: an imitation reward _𝑟𝑡_<sup>im( ˜</sup><sup>_𝑀_</sup> _𝑟_<sup>(</sup><sup>_𝑖_))penalizingdeviationsfromthereferencemotioninjointpositions,velocities,and</sup> root trajectory; a stability reward _𝑟𝑡_<sup>stable</sup> encouraging balance and preventing falls; and optional regularization terms _𝑟𝑡_<sup>reg</sup> . The objective is formalized as: 


where _𝛾_ ∈(0 _,_ 1] is a discount factor, and _𝜆_ stable and _𝜆_ reg are weighting coefficients for the stability and regularization rewards, respectively. 

A deployable student policy _𝜋𝜃_ is then trained via supervised learning to mimic the teacher’s actions, using only realistic onboard observations. The student’s objective is to minimize the action discrepancy between its own output and the teacher’s output, which serves as a guiding signal. This distillation process is formalized as: 


where U( _𝑀_<sup>˜</sup> _𝑟_<sup>(</sup><sup>_𝑖_))denotesunifiedgoalstatesamplingfromamotiontrajectory.Thisobjectivearises</sup> from the core idea of policy distillation [41]: the pre-trained, privileged teacher _𝜋𝜙_ provides highquality target actions. The student _𝜋𝜃_ is trained to reproduce these target actions from its limited, real-world-compatible observation space ( _𝑠𝑡, 𝑐𝑡_ ), thereby inheriting the teacher’s performance while remaining practical for deployment.For example, during the training of the teacher policy, we track multiple key points of the human body on the reference human motion, while during the training 

9 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

of the student policy, we default to tracking only three key points: the head and both hands. To facilitate training and control, we adopt a direct retargeting approach for tracking human hand movements, without incorporating reinforcement learning into the training process. 

**RL Fine-Tuning (RFT)** During inference for a given target motion _𝑀_<sup>˜</sup> _𝑟_<sup>(tg)</sup> , we fine-tune the pre-trained student policy _𝜋_<sup>(pt)</sup> _𝜃_ exclusively on _𝑀_<sup>˜</sup> _𝑟_<sup>(tg)</sup> , retaining the teacher-student structure. The teacher is finetuned with privileged access to _𝑀_<sup>˜</sup> _𝑟_<sup>(tg)</sup> , and the student is subsequently distilled again via the same DAgger-based procedure, now specializing in the target motion. This process adapts the policy to the specific kinematic and dynamic characteristics of _𝑀_<sup>˜</sup> _𝑟_<sup>(tg)</sup> , resulting in a policy _𝜋_<sup>(ft)</sup> _𝜃_ that executes the motion with higher fidelity and stability than the generalist policy alone. 

We use the PPO algorithm [42] to optimize these teacher policies with domain randomizations. Please note that as our default method, our pretrain-finetune paradigm employs a teacher-student training logic to articulate and validate the idea itself. But the entire pretrain-finetune paradigm is inherently compatible with the RL training of various common whole-body controllers [30, 31]. For more details about the RPT and RFT, please refer to the Appendix B. 

##### **_2.3.3. Modular Deployment Framework_** 

To enable robust real-world execution of trained policies, H-ACT further designs a modular framework RoboJudo that unifies a motion _Controller_ ( _𝐶_ ), an environment abstraction layer ( _𝐸_ ), and the policy module (Π _𝜃_ ) behind a consistent interface for motion commands _𝑚𝑡_ , robot state _𝑠𝑡_ , and actions _𝑎𝑡_ . This design not only supports the deployment of our default control methods across different robots but also seamlessly integrates various other forms of control paradigms through a plug-andplay approach. The framework accommodates diverse whole-body policies by converting the canonical retargeted motion into policy-specific command formats: 

- **Upper-Lower Decoupled Policies** Split motion into upper-body joint targets and lower-body locomotion commands (root velocity, waist orientation) [43, 44]. 

- **Teleoperation-Based Policies** Condense motion into key joint or end-effector references for real-time tracking [13, 30]. 

- **Whole-Body Tracking Policies** Use full joint and root trajectories as direct references for highfidelity, per-motion tracking [31, 45]. 

This lightweight conversion enables a single generated motion _𝑀_<sup>˜</sup> _𝑟_ to drive multiple policy types. The Environment layer abstracts platform communication, while the Policy layer provides a unified execution interface _𝜋𝜃_ : ( _𝑠𝑡, 𝑚𝑡_ ) ↦→ _𝑎𝑡_ . 

The modular design facilitates efficient sim-to-real transfer, runtime policy switching and composition, and streamlined integration of new robotic platforms. And this deployment framework provides a flexible and robust layer that translates generated humanoid motions _𝑀_<sup>˜</sup> _𝑟_ into stable, executable actions _𝐴_<sup>˜</sup> _𝑟_ on physical humanoid robots. The detailed system architecture is provided in Appendix B.2. 

### **3. Experiments** 

We conduct comprehensive experiments to answer three key questions about FRoM-W1: 

- **Q1** : Can the H-GPT model generate accurate and diverse whole-body human motions based on natural language instructions? 

10 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

- **Q2** : Can the H-ACT module control humanoid robots to stably perform the motions generated by H-GPT in a simulation environment? 

- **Q3** : How well does the entire framework perform when deployed on real-world humanoid robots? 

##### **3.1. Instruction to Whole-Body Human Motion Generation** 

To address **Q1** , we conducted a thorough and comprehensive evaluation of H-GPT. We first assessed H-GPT’s performance on text-to-motion benchmarks both quantitatively and qualitatively. Then, we tested the scalability of H-GPT by training it with more data. Additionally, we further examined the generalization ability of H-GPT’s CoT using abstract and complex instructions. 

**HumanML3D-X and** _𝛿_ **HumanML3D-X Benchmarks** Since there is no readily available benchmark for evaluating whole-body human motion generation capabilities that include hand movements, we extended the previous HumanML3D benchmark [20] to create two new benchmarks: HumanML3DX and _𝛿_ HumanML3D-X. 

The HumanML3D Benchmark is originally constructed based on two mocap datasets, HumanAct12 [46] and AMASS [40], and provide 3–4 textual descriptions for each motion clip. Models can be trained for text-to-motion generation using these text and motion pairs. HumanML3D-X retains the text labels from HumanML3D and extends the original handless SMPL-format [47] motions to hand-inclusive SMPL-X-format [28] motions. _𝛿_ HumanML3D-X further introduces two types of transformations based on HumanML3D-X: one involves altering the style of the original text labels (for example, from _”a man kicks something or someone with his left leg.”_ to _”So, this dude goes ahead and gives a good kick with his left leg to whatever’s in his way.”_ ), and the other adds noise perturbations to the original text labels (for example, from _”a person is walking and then steps over something.”_ to _”a person is wlaking then steps oveer something.”_ ). The HumanML3D-X benchmark is used to train and test models for generating whole-body human motion, by training on its training set and evaluating on its test set; while the _𝛿_ HumanML3D-X benchmark further evaluates models’ generalization capabilities in response to language instructions, by testing models trained on HumanML3D-X directly on its test set. 

We evaluated different methods using commonly employed scoring-model based metrics, including Fréchet Inception Distance (FID), Retrieval Precision Top- _𝑘_ (R Top- _𝑘_ , _𝑘_ ∈{1 _,_ 2 _,_ 3}), Multimodal Distance (MM Dist), Diversity (DIV) and MultiModality (MModality) [20, 24, 48]. (a) Motion quality: FID is our primary metric, used to measure the distance between the feature distributions of generated motions and ground-truth motions. (b) Motion-Text matching: R Top- _𝑘_ measures the accuracy of matching between text instructions and motions through retrieval methods. We use MM Dist to measure the distance between text and motions. (c) Motion Diversity: DIV measures the diversity of motions by calculating the variance of their features. And MMoality measures the diversity of multiple motions generated under a fixed text description. 

Following the workflow in Guo et al. [20], we retrained the corresponding text and motion feature extraction models as well as scoring models on these two benchmarks. 

**Baselines** Our baseline methods primarily include four mainstream approaches, falling into two categories: autoregressive models [49] and diffusion models [50]. 

- **T2M** [20] employs an autoencoder to encode motion features, and uses a recurrent neural network to generate motions of the corresponding length based on the estimated motion duration and textual description features. 

11 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

|**Model**|**FID**↓|**R Top-1**↑|**MM Dist**↓|**DIV**→|**MModality**↑|
|---|---|---|---|---|---|
|**Real**|0_._000<sup>±0</sup><sup>_._00</sup>|0_._393<sup>±0</sup><sup>_._01</sup>|3_._862<sup>±0</sup><sup>_._01</sup>|9_._811<sup>±0</sup><sup>_._10</sup>|-|
|T2M|2_._078<sup>±0</sup><sup>_._12</sup>|0_._252<sup>±0</sup><sup>_._01</sup>|4_._967<sup>±0</sup><sup>_._01</sup>|8_._325<sup>±0</sup><sup>_._13</sup>|**4.208**<sup>±0</sup><sup>_._06</sup>|
|MotionDiffuse*|19_._423<sup>±0</sup><sup>_._08</sup>|0_._100<sup>±0</sup><sup>_._00</sup>|6_._919<sup>±0</sup><sup>_._01</sup>|5_._183<sup>±0</sup><sup>_._02</sup>|3_._870<br>±0_._26|
|MLD|0_._817<sup>±0</sup><sup>_._05</sup>|0_._357<br>±0_._01|4_._189<br>±0_._04|9_._549<br>±0_._10|3_._224<sup>±0</sup><sup>_._18</sup>|
|T2M-GPT|0_._677<sup>±0</sup><sup>_._06</sup>|**0.357**<sup>±0</sup><sup>_._01</sup>|**4.182**<sup>±0</sup><sup>_._02</sup>|9_._260<sup>±0</sup><sup>_._22</sup>|2_._599<sup>±0</sup><sup>_._13</sup>|
|H-GPTw.o. CoT<br>H-GPT|**0.229**<sup>±0</sup><sup>_._03</sup><br>0_._255<br>±0_._01|0_._333<sup>±0</sup><sup>_._01</sup><br>0_._332<sup>±0</sup><sup>_._00</sup>|4_._455<sup>±0</sup><sup>_._03</sup><br>4_._513<sup>±0</sup><sup>_._02</sup>|**9.674**<sup>±0</sup><sup>_._02</sup><br>9_._383<sup>±0</sup><sup>_._18</sup>|2_._754<sup>±0</sup><sup>_._34</sup><br>3_._256<sup>±0</sup><sup>_._47</sup>|


**Table 1** | **HumanML3D-X Benchmark** . Results are reported as mean ± 95% confidence interval over three-time runs. The best results among generated motions are in **bold** and the second best results are underlined. <mark>FID</mark> is our primary metric. *We found that MotionDiffuse is sensitive to parameters and difficult to achieve good results. 


**Figure 6** | Visualization of a motion sequence generated by the H-GPT model. The prompt is from the test set of the HumanML3D-X benchmark: _“a person flings an object with their right hand then showcases something with both hands.”_ 

|**Model**||**Instruction**|**Rephrasing**|||**Instructi**|**on Noising**||
|---|---|---|---|---|---|---|---|---|
||**FID**↓|**R Top-1**↑|**DIV**→|**MModality**↑|**FID**↓|**R Top-1**↑|**DIV**→|**MModality**↑|
|**Real**|0_._000<sup>±0</sup><sup>_._000</sup>|0_._367<sup>±0</sup><sup>_._001</sup>|8_._863<sup>±0</sup><sup>_._054</sup>|-|0_._000<sup>±0</sup><sup>_._000</sup>|0_._322<sup>±0</sup><sup>_._003</sup>|8_._422<sup>±0</sup><sup>_._082</sup>|-|
|MLD<br>T2M-GPT|1_._944<sup>±0</sup><sup>_._168</sup><br>2_._043<sup>±0</sup><sup>_._025</sup>|0_._165<sup>±0</sup><sup>_._006</sup><br>**0.234**<sup>±0</sup><sup>_._001</sup>|**8.357**<sup>±0</sup><sup>_._113</sup><br>7_._578<sup>±0</sup><sup>_._194</sup>|4_._075<sup>±0</sup><sup>_._107</sup><br>2_._698<sup>±0</sup><sup>_._169</sup>|2_._256<sup>±0</sup><sup>_._092</sup><br>1_._610<sup>±0</sup><sup>_._001</sup>|0_._138<sup>±0</sup><sup>_._008</sup><br>0_._183<sup>±0</sup><sup>_._005</sup>|**8.509**<sup>±0</sup><sup>_._111</sup><br>6_._886<sup>±0</sup><sup>_._163</sup>|4_._086<sup>±0</sup><sup>_._096</sup><br>2_._897<sup>±0</sup><sup>_._353</sup>|
|H-GPTw.o. CoT<br>H-GPT|0_._455<sup>±0</sup><sup>_._021</sup><br>**0.355**<sup>±0</sup><sup>_._007</sup>|0_._210<sup>±0</sup><sup>_._004</sup><br>0_._225<sup>±0</sup><sup>_._008</sup>|8_._201<sup>±0</sup><sup>_._201</sup><br>8_._240<sup>±0</sup><sup>_._207</sup>|4_._240<sup>±0</sup><sup>_._184</sup><br>**4.533**<sup>±0</sup><sup>_._349</sup>|0_._830<sup>±0</sup><sup>_._050</sup><br>**0.602**<sup>±0</sup><sup>_._055</sup>|0_._177<sup>±0</sup><sup>_._008</sup><br>**0.192**<sup>±0</sup><sup>_._006</sup>|7_._677<sup>±0</sup><sup>_._116</sup><br>7_._788<sup>±0</sup><sup>_._184</sup>|4_._506<sup>±0</sup><sup>_._389</sup><br>**4.642**<sup>±0</sup><sup>_._367</sup>|


**Table 2** | _𝛿_ **HumanML3D-X Benchmark** . Results are reported as mean ± 95% confidence interval over three-time runs. The best results among generated motions are in **bold** . <mark>FID</mark> is our primary metric. These models were trained on HumanML3D-X and evaluated on this benchmark. 

- **MotionDiffuse** [51] utilizes a linear-attention-based diffusion model for motion generation with a Transformer-based text encoder to extract the text embedding as the condition. 

- **MLD** [48] applies the CLIP model [52] as an extractor for text features and utilizes a latent diffusion model [53] to generate motions. 

- **T2M-GPT** [24] models the motion space with a stand-alone Transformer [49] decoder and the text embeddings are also obtained from an off-the-shelf CLIP model. 

These works were previously trained based on the HumanML3D dataset. We meticulously retrained these models on the HumanML3D-X training data using the open-source code from these works. 

**Implementation Details** In this experiment, we represented hand-inclusive whole-body motion sequences using position, velocity and rotation information, and represent rotations using 6D continuous representation [54]. We primarily implemented two designs of H-GPT: one is H-GPT without CoT (H-GPTw.o. CoT), and the other is H-GPT with CoT (H-GPT). Both of them utilized the same motion tokenizer we trained, K ∈R<sup>512×512</sup> , with the temporal downsampling factor _𝑙_ set to 4. Both H-GPT models are based on the 8B LLAMA-3.1 base model [11] and were further pretrained using LoRA [36] with a rank of 32, a scaling factor of 16, and a dropout rate of 0.05 applied to all linear projection layers, while the embedding and language modeling head layers remain fully trainable. We used an 8-GPU NVIDIA machine for model training. For training the VQ-VAE, we set the batch size to 512 and trained for 30,000 epochs. For training the H-GPT models, we set the mini-batch size to 8 and trained for 600 epochs. For more details on constructing the CoT data, please refer to Appendix A.1. 

12 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

|**Model**|**FID**↓|**Top-1**↑|**R Precision**<br>**Top-2**↑|**Top-3**↑|**MM Dist**↓|**DIV**→|**MModality**↑|
|---|---|---|---|---|---|---|---|
|**Real**|0_._000<sup>±0</sup><sup>_._000</sup>|0_._393<sup>±0</sup><sup>_._005</sup>|0_._573<sup>±0</sup><sup>_._005</sup>|0_._677<sup>±0</sup><sup>_._004</sup>|3_._862<sup>±0</sup><sup>_._009</sup>|9_._811<sup>±0</sup><sup>_._096</sup>|-|
|H-GPTw.o. CoT<br>H-GPT|**0.229**<sup>±0</sup><sup>_._029</sup><br>0_._255<br>±0_._008|**0.333**<sup>±0</sup><sup>_._007</sup><br>0_._332<br>±0_._004|**0.490**<sup>±0</sup><sup>_._003</sup><br>0_._481<sup>±0</sup><sup>_._004</sup>|**0.588**<sup>±0</sup><sup>_._003</sup><br>0_._573<sup>±0</sup><sup>_._001</sup>|**4.455**<sup>±0</sup><sup>_._033</sup><br>4_._513<sup>±0</sup><sup>_._019</sup>|**9.674**<sup>±0</sup><sup>_._021</sup><br>9_._382<sup>±0</sup><sup>_._182</sup>|2_._754<sup>±0</sup><sup>_._335</sup><br>**3.256**<sup>±0</sup><sup>_._465</sup>|
|H-GPT++w.o. CoT<br>H-GPT++|0_._337<sup>±0</sup><sup>_._011</sup><br>0_._312<sup>±0</sup><sup>_._054</sup>|0_._323<sup>±0</sup><sup>_._005</sup><br>0_._327<sup>±0</sup><sup>_._004</sup>|0_._482<sup>±0</sup><sup>_._005</sup><br>0_._486<br>±0_._010|0_._581<sup>±0</sup><sup>_._004</sup><br>0_._583<br>±0_._012|4_._494<br>±0_._054<br>4_._494<sup>±0</sup><sup>_._066</sup>|9_._240<sup>±0</sup><sup>_._104</sup><br>9_._411<br>±0_._062|2_._664<sup>±0</sup><sup>_._115</sup><br>3_._153<br>±0_._241|


**Table 3** | **HumanML3D-X Benchmark Results with Motion-X Training Data** . Performance comparison of different motion generation models against real motion data. Results are reported as mean ± 95% confidence interval over multiple runs. The best results among generated motions are in **bold** and the second best results are underlined. Real motion data serves as the ground truth reference. 

**Results** The experimental results on the HumanML3D-X benchmark are shown in Table 1. We observe that our H-GPTw.o. CoT and H-GPT models achieve significant improvement on the main metric FID, reducing it from 0.677 of T2M-GPT to 0.229 and 0.255. This indicates that our H-GPT models are capable of generating human whole-body motions that better align with the textual descriptions. Meanwhile, our H-GPTw.o. CoT model also achieves the best result 9.674 on the motion diversity metric DIV. Regarding the two metrics that measure the correlation between motion and text, R Top-1 and MM Dist, we observed in our experiments that T2M-GPT and our H-GPT models often result in their degradation when FID improves. We believe this may be because the training loss of the model is primarily designed to fit the motion distribution in the training dataset, without imposing explicit constraints on the representation correlation between motion and text. This leads the model to more easily generate common and less distinguishable motions during the fitting process. Regarding the MModality metric, we found that even though the fitting performance of models like T2M and MotionDiffuse is relatively poor, the diversity of motions generated from the same text tends to be higher for this metric. We visualize an example of a human motion generated by the H-GPT model in Figure 6. 

Moreover, we found on the HumanML3D-X benchmark that the H-GPTw.o. CoT model performs relatively better than the H-GPT model (FID 0.229 vs. 0.255). We think this is partly because the training and test sets of HumanML3D-X have relatively consistent distributions, making it easier to learn the mapping between text and motion. In contrast, the introduction of CoT, due to the addition of a certain length of text, makes the fitting slightly more challenging. Furthermore, based on our newly extended _𝛿_ HumanML3D-X benchmark on Table 2, it can be observed that compared to the baselines, both H-GPT models demonstrate better generalization capabilities in language understanding. Additionally, the introduction of CoT further enhances their ability to comprehend instructions and generate motions under the scenarios of instruction rephrasing (FID 0.455 → 0.355) and instruction noising (FID 0.830 → 0.602). 

**Data Scaling with Motion-X** As mentioned before, we argue that massive human data, especially human motion data extracted from vast video collections, has the potential to enhance the generalization of whole-body motion generation tasks for humanoid robots. Therefore, we further conducted data processing and model training on Motion-X [21], the largest publicly available human motion dataset that includes hand movements, including 81084 annotated human motion clips. MotionX encompasses data such as HumanML3D-X from motion capture and has additionally estimated a large volume of whole-body human motion poses from extensive video sources, with text labels generated using large vision-language models (VLMs) like GPT-4V and Vicuna [55]. We have also extended Motion-X with CoT. And we label the two models, the one with CoT and the one without 

13 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 


**Figure 7** | Complex (first row) and abstract (second row) cases visualization of different H-GPT models. Complex Prompt: _“A person walks forward, stops, and stands drinking something.”_ . Abstract Prompt: _“Shiver and hug yourself tightly to communicate feeling cold or scared.”_ 

CoT, as H-GPT++w.o. CoT and H-GPT++ respectively. Since Motion-X includes more and more diverse motion sequences, we retrained the motion tokenizer with different settings and found that the reconstruction performed best when the codebook number was 1024 and the codebook dimension was 2048. Therefore, we adopted this configuration in our experiments. The remaining settings are largely consistent with the training parameters of HumanML3D-X. 

The evaluation results are shown in Table 3. We observed that, different from the results reported in Lin et al. [21], training on Motion-X can achieve decent performance, but the overall performance is not as good as directly using the training data from HumanML3D-X. We guess that part of the reason may be due to the fact that the text labeled by VLMs and human motion data estimated by Motion-X from videos still exhibits certain differences in distribution and quality compared to the precise human motion capture data with human labeled language descriptions like HumanML3D-X. For example, in Motion-X, a certain proportion of motion textual labels are phrased like _“the subject of the sentence is ‘a man.”’_ and _“the existence of life is a fact.”_ Meanwhile, we can observe that the overall performance of the model has improved after incorporating CoT. It appears that there is still considerable room for improvement in the research community’s approach of leveraging scaling human pose data estimated from videos to enhance the overall generalization capability of models. 

**CoT Generation Performance** To further evaluate the generalization ability of the CoT version model for complex and abstract instructions, we designed two categories comprising 50 test instruction cases to carefully compare the performance of models without CoT and those with CoT. Complex instructions are constructed by randomly and naturally combining two original instructions from HumanML3D-X using GPT-4o. For example: _“A person is running in place, then starts to run right and left, while jumping up and down.”_ Abstract instructions involve randomly generating 10 examples each for imitative performance, actions with emotion, interaction with human, interaction 

14 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 


**Figure 8** | Comparison of different metrics for evaluating on HumanML3D-X dataset and H-GPT generated dataset. MPJPE values are divided by 3, VEL and ACCEL values are multiplied by 2. 

with objects, and interaction with the environment using GPT-4o. For instance: _“Pantomime pulling a heavy rope hand over hand, showing the strain in your arms and back.”_ 

Since there is no ground truth motion for these instructions, making it inconvenient to establish evaluation metrics, we adopt the approach of manually observing the generated motions and comparing them to assess these models. We did not assign separate scores to the results generated by each model. Instead, we determined which model produced better results—including cases where they perform equally well—through comparative evaluation, and then calculated the final scores. In the evaluation task of 50 complex instructions, the score between H-GPTw.o. CoT and H-GPT is 23 : 27, and the score among H-GPTw.o. CoT, H-GPT, H-GPT++w.o. CoT, and H-GPT++ is 9 : 18 : 12 : 28. In the evaluation task of 50 abstract instructions, the score between H-GPTw.o. CoT and H-GPT is 23 : 30, and the score among H-GPTw.o. CoT, H-GPT, H-GPT++w.o. CoT, and H-GPT++ is 17 : 26 : 12 : 20. As we can see, through CoT enhancement, both the H-GPT and H-GPT++ models have achieved better generation results. However, no consistent superiority between these two models has been observed yet. We visualize several typical examples in Figure 7. For more test cases of CoT, please refer to Appendix A.2. 

##### **3.2. Humanoid Whole-Body Control in Simulation Environments** 

To answer **Q2** , we conducted a series of experimental validations of the H-ACT module using the H1 and G1 humanoid robots in the IsaacGym [32] and MuJoCo [56] physics simulators. We focus on the performance of reinforcement learning (RL) based control during the pre-training stage, its tracking effect on motions generated by H-GPT, and the performance of our proposed RL fine-tuning method in the inference stage. 

**RL Pre-Training (RPT)** To provide a good initialization parameter for the humanoid robot wholebody control policy, we first pre-trained a general motion controller using the AMASS human motion dataset [40] with RL. 

**Training** We first retarget the human motion data from AMASS to the skeleton structures of Unitree’s H1 and G1 robots. Since the hands are typically lightweight and do not significantly affect 

15 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 


**Figure 9** | H-ACT RPT Simulation Tracking Results. (a) Prompt: _“Shiver and hug yourself tightly to communicate feeling cold or scared.”_ (b) Prompt: _“Do a simple, three-step robot dance to a funky beat you imagine.”_ (c) Prompt: _“A person frantically digging through the dirt with bare hands, nails cracking, driven by desperate hope.”_ (d) Prompt: _“A person stumbling and catching themselves on a lamppost, swaying slightly before righting their posture with false dignity.”_ (a) and (c) are examples of successful tracking for the Unitree H1 and G1 robots, while (b) and (d) are examples of tracking failures for the Unitree H1 and G1 robots. 

balance, but have too many degrees of freedom that can reduce the efficiency of RL training, we did not add hand joints to these humanoid robots in the RL framework. Therefore, here we map the 24joint SMPL 3D human motions to the 19-DOF H1 and 21-DOF G1 robot structures, respectively. We trained these robots in NVIDIA’s GPU-accelerated IsaacGym physics simulation to accurately follow the retargeted reference motions while maintaining body stability and preventing falls. In terms of RL rewards, we set basic torque and DOF position limits, and applied regularization to situations such as excessively high DOF acceleration and velocity, prolonged feet air time, and stumbling. We penalized substantial differences between the actual motion and the reference motion in terms of joint positions, velocities, accelerations, body rotation angles, and speeds. Additionally, we imposed penalties for the humanoid robot falling, specifically when its center of mass fell below a set threshold. For each robot, we launched 4096 parallel environments and optimized the policy using the PPO algorithm implemented in the RSL-RL framework [57]. 

**Results** We focused on evaluating the MPJPE, VEL, and ACCEL metrics for the whole-body control policies of H1 and G1, which measure the differences in joint angles, velocities, and accelerations between the robot’s actual states and the reference motions. We compared the performance of policies trained using the teacher-student strategy with both raw and filtered data. The results are shown in Figure 8 (a). From the figure, it can be observed that using the filtered data consistently improves all metrics of both robot policies, both on the complete AMASS data and on the filtered AMASS data. Additionally, it can be observed that all metrics of H1 (SR 40% ∼ 50%) are relatively poorer compared to those of G1 (SR 80% ∼ 90%). This, to some extent, indicates that the structural design of G1 enables it to perform diverse actions more stably and easily than the H1 robot. Furthermore, we found that factors such as the stability of the reference’s initial pose and the rate of change in body and joint motions significantly influence the success rate of policy tracking. 

To further evaluate the performance of the pretrained controllers of H1 and G1, we tested them using the out-of-domain complex and abstract test samples generated by H-GPT from the previous subsection, with the results shown in Figure 8(b). From this, it can be seen that the tracking performance of H1 and G1 on these newly generated motions shows a more significant difference, and the model trained on filtered data does not exhibit better performance. We speculate that this 

16 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 


**Figure 10** | Performance comparison of different training strategies on H1 and G1 robots. MPJPE values are divided by 2 for better visualization. VEL and ACCEL values are multiplied by 2 for better visualization. SR values are shown as percentages. 

is partly because the generated actions are noisier, and training on data with noise may enhance the model’s robustness. The visualization results of some successful and failed cases are shown in Figure 9. 

**RL Fine-tuning (RFT)** To further enhance the motion tracking performance of the controller during inference, we propose a strategy that continues to leverage physics simulation for reinforcement learning-based imitation learning at this stage. Specifically, during inference, we initialize the controller with pre-trained checkpoints and employ a teacher-student framework to conduct targeted training tailored to the reference motion. This way we can iterate over a small number of steps in a short time to make the controller better fit the reference motion to be tracked. 

We randomly sampled 30 motions from the AMASS dataset to test the control policies for H1 and G1. We primarily compared the effectiveness of this fine-tuning strategy against training from scratch and using pre-training alone. The main evaluation metrics were MPJPE and Success Rate. As shown in Figure 10, we can see that the MPJPE and SR metrics for motion tracking have improved steadily after RFT on both the H1 and G1 robots. We also observed that some previously less stable tracking motions became more stable after RFT. 

We further tested the variation of several metrics with the number of tuning steps during the RL Fine-tuning phase, and the results are shown in Figure 11. From subplots (a) and (b) of the figure, it can be seen that the model has already achieved a significant improvement around 500 steps. A visual comparison case of training from scratch, pretraining, and fine-tuning is shown in Figure 12. 

##### **3.3. Performance of the Entire Framework in the Real World** 

Finally, to address **Q3** , we fully deployed the entire FRoM-W1 framework on the Unitree H1 and G1 robots. In addition to testing with the default RL Policy of H-ACT, as mentioned in the previous sections, our framework is compatible with many RL control algorithms in the field of motion mimicing. We developed a lightweight deployment framework for efficiently deploying these different policies. And we thus tested the execution capabilities of different RL Policies on the motions generated by H-GPT. 

17 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 


**Figure 11** | Performance metrics at different training steps. MPJPE values are divided by 2 for better visualization. 


**Figure 12** | H-ACT RFT Simulation Tracking Results. Prompt: _“Shiver and hug yourself tightly to communicate feeling cold or scared.”_ (a) Training from scratch. (b) Pre-train. (c) Fine-tune 

**Setup** We first deployed our default policy on the H1 and G1 robots. We used a 4090 workstation as the edge-side computing resource to run the H-GPT model for motion generation. The generated motions were then retargeted and transmitted to the robots via wired or wireless connections. Finally, the whole-body motion controller of the H-ACT part was executed using the computing board deployed on the robots. In addition to testing the default RL Policy of H-ACT, we also tested wholebody motion control policies for humanoid robots provided by HugWBC [33] and TWIST [30]. HugWBC is a unified whole-body controller that empowers humanoid robots to execute versatile gaits like jumping and hopping with real-time parameter tuning, while simultaneously accommodating upper-body interventions for loco-manipulation. TWIST is a teleoperation system that enables humanoid robots to perform versatile whole-body skills through human motion imitation using a unified neural network controller. Our hardware configuration and deployment framework can be referred to in Appendix B.1 and B.2, respectively. 

**Results** Typical examples of deploying the default reinforcement learning strategy after H-GPT generates the motion is shown in Figure 13. These examples demonstrate several features of our overall framework, including the ability to comprehend and generate abstract instructions, the capacity to generate hand movements, and the stable deployment capability for locomotion actions. Figure 14 demonstrates the compatibility of our framework with different control strategies, enabling efficient and stable real-world deployment of models such as HugWBC and TWIST. In addition to these successful examples, we found that the overall framework still faces issues in generating actions for arbitrary instructions. These problems include misalignment between generated actions and instructions, instability in the generated actions themselves, or scenarios where the actions cause collisions within the robot’s body. In addition, as shown in Figure 15, for certain extreme movements—such 

18 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 


**(a)** Unitree H1 Robot. Prompt: _“A person is playing the role of an elephant.”_ 

**(b)** Unitree G1 Robot. Prompt: _“A person is playing the role of an elephant.”_ 


**(c)** Unitree H1 Robot. Prompt: _“A person is playing a violin.”_ 

**(d)** Unitree G1 Robot. Prompt: _“A person is playing a violin.”_ 


**(e)** Unitree H1 Robot. Prompt: _“A person took a few steps forward and then answered a phone call.”_ 

**(f)** Unitree G1 Robot. Prompt: _“A person took a few steps forward and then answered a phone call.”_ 

**Figure 13** | H-ACT Real-World Depolyment Results. In the figure, (a) and (b) illustrate the scenario where the H1 robot and the G1 robot complete abstract instructions. (c) and (d) demonstrate cases involving typical hand movements, while (e) and (f) depict situations of moving first and then imitating actions. 

as half-squats or rapid running—even if the robot can perform these actions in simulation, unstable conditions still frequently arise during real-world deployment due to the Sim2Real gap. For more sim2real details, please refer to the Appendix B.3. 

### **4. Related Work** 

**Text to Human Motion Generation** Text-conditioned 3D human motion generation is a fundamental task in 3D computer vision, which contributes to downstream applications such as VR content creation, gaming, and robotics. In recent years, the introduction of the HumanML3D text-to-motion dataset and the T2M method [20] has laid a new foundation for this direction. This has led to autoregressive modeling-based approaches such as TM2T [34], T2M-GPT [24], and MotionGPT [25], diffusion model-based methods like MDM [58], MLD [48], and MotionDiffuse [51], as well as methods based on masked transformers, such as MoMask [59]. However, the HumanML3D dataset has two major issues. Firstly, its data scale is too small, making it difficult for models trained on it to achieve strong generalization capabilities. Secondly, it is based on the SMPL body representation [47], which does not include hand modeling. Yet, for humanoid robots, the hands are crucial for the expressiveness of overall motions and for tasks such as manipulation and loco-manipulation. To address the first issue, MotionMillion [22] expanded the scale of SMPL human motion sequences 

19 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 


**(a)** The HugWBC Policy. Prompt: _“A person is practicing squats.”_ 

**(b)** The TWIST Policy. Prompt: _“A person dancing alone in a messy kitchen, swaying with a broom as a partner to a silent radio tune.”_ 

**Figure 14** | H-ACT Cross-Policy Depolyment Results. The H-ACT framework can efficiently support the stable deployment of different control strategies. 


**(a)** The TWIST Policy. Prompt: _“A person crouching low to the ground, body coiled like a spring, ready to launch into action.”_ 

**(b)** The TWIST Policy. Prompt: _“A person sprinting through the rain, their arms pumping wildly as if trying to outrun a storm of memories.”_ 

**Figure 15** | H-ACT Real-World Failure Cases. (a) shows the Unitree G1 robot falling over during an extreme squatting motion, and (b) shows the robot failing to track a fast forward-moving target motion. 

to the million level by using human pose estimation on large-scale videos from the internet. And Motion-R1 [60] enhances generalization capability for linguistic instructions by incorporating a CoT approach. Regarding the second issue, Motion-X [21] is currently the largest publicly accessible motion dataset that utilizes SMPL-X [28], which includes hand modeling. Work based on Motion-X includes HumanTOMATO [61], MotionGPT-2 [62], MotionCraft [63], and others. However, these efforts either do not involve further training on existing large language models [61, 63], are not open-sourced [61, 62], or utilize only a small portion of the dataset [63]. For our motion generation component, we require an open-source, whole-body human motion generation model with hand modeling that is built upon existing LLMs and trained on massive data to achieve stronger language generalization capabilities. Therefore, based on the LLaMA model [11] and incorporating CoT techniques, we train H-GPT on HumanML3D-X and Motion-X to create a whole-body motion generation model represented in SMPL-X format, and open-source it. 

**Humanoid Whole-Body Motion Tracking** The development of hardware platforms for humanoid robots, such as the Unitree H1 and G1, has laid the foundation for advancements in humanoid robot control algorithms in recent years, and a series of human-to-humanoid teleoperation and whole-body motion control algorithms for humanoid robots have emerged. Early explorations involved using reinforcement learning techniques to enable humanoid robot platforms to accomplish specific tasks such as smooth locomotion [5], performing backflips [3], walking on stepping stones [6], and parkour [4]. Subsequently, researchers began exploring methods to enable humanoid robots to track human motions captured through motion capture systems, either offline or in real time, a process also known as motion mimicing or motion shadowing. ExBody [64], H2O [13], OmniH2O [65], and HumanPlus [66] are several pioneering works that have explored in this direction. Among them, 

20 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

ExBody decouples and separately controls the upper and lower bodys of humanoid robots, while H2O, OmniH2O, and HumanPlus focus on whole-body control. Additionally, OmniH2O proposes a Teacher-Student training strategy, and HumanPlus further trains humanoid manipulation policies using data collected through teleoperation. Subsequent works involve exploring more control methods, such as Vision Pros [67, 68], motion capture devices [30], exoskeleton cockpit systems [69], diverse motion generation models [70], and others, as well as improving the model’s effectiveness by enabling adaptive lower-body movements when the upper and lower bodys are decoupled [43], further training on different subtasks separately [71], and employing strategies such as the Mixture of Experts (MoE) [72] and merging expert policies [31]. The purpose of the H-ACT module in FRoM is to have a universal whole-body tracker capable of mimicking human motions generated by H-GPT. Therefore, in principle, it can be compatible with the various whole-body control strategies mentioned above that can track human motion. Additionally, our universal deployment module supports the integration of the aforementioned multiple strategies [13, 30, 31, 33, 65, 68] into our entire framework. In our paper, we adopt a training framework similar to OmniH2O’s teacher-student approach as our default strategy for whole-body motion controller training. Moreover, during the inference phase, an RL fine-tuning strategy is introduced to further enhance the tracker’s accuracy and stability. This shares a similar concept with the third stage of the recent UniTracker [73]. However, to maintain simplicity and generality, we directly fine-tuned the entire network instead of adding a separate residual module. 

**Language-Drive Humanoid Whole-Body Control** Whole-Body controlling humanoid robots using language, especially full-size robots such as the Unitree H1 and G1, remains a very new task. RobotMDM [74] initially uses a small diffusion model to generate motions and trains a controller via RL techniques to control a very small robot in performing whole-body movements. Harmon [75] leverages off-the-shelf motion generation models to produce motion, and introduces hand and head movements by prompting visual language models. UH-1 [76] can be considered the first method to explore the use of vast video-based human motion data to achieve universal language control over the whole-body movements of full-size humanoid robots. However, it trains a small motion generation model from scratch without leveraging the capabilities of existing large models, and the expressiveness and diversity of the motions demonstrated by its control policy remain relatively limited. A more critical issue is that it trains a separate motion generation module for each humanoid robot, which is difficult to scale in scenarios involving massive data, high parameter models, and substantial computational consumption. In contrast, our approach chooses human motion models as a unified representation, allowing for natural transferability to humanoid robots with different structures. Additionally, LangWBC [77] utilizes a small end-to-end network to achieve real-time language control of humanoid robot motions. LeVERB [78] employs its own designed small-scale two-brain network to control Unitree robots for full-body motion using latent verbs. Furthermore, the recent RoboGhost [79] also leverages latent command representations as direct conditions for generating the robot’s final full-body action signals through a diffusion model. In contrast, our entire framework aims to leverage and build upon the powerful language understanding capabilities and generalization potential of existing large models. Therefore, we have not designed or trained any small, standalone motion generation models from scratch. RLPF [80] utilizes a large model to generate motion and then feeds back control-phase signals to the generation stage of the model to enhance its generation capabilities. However, it does not include hand movements, lacks CoT reasoning to improve model generalization, and has not open-sourced its model for use, evaluation, and comparison. Concurrent work, Humanoid-LLA [81], also employs CoT to enhance the model’s generalization capability with language. It further integrates the vocabulary space of the large language model with the control signals of the humanoid robot, and then utilizes feedback from physical simulation to optimize the large model. We introduced hand modeling, provided new benchmarks, scaled with more 

21 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

data, carefully evaluated the effects of incorporating CoT, optimized the RL training strategy, designed and implemented a universal sim2real module, and open-sourced the entire framework. We hope to further advance and evaluate the boundaries of this entire field through this comprehensive framework, and promote the development of the field through open-source practices. 

### **5. Conclusion** 

In this work, we present FRoM-W1, an open-source framework that unifies language understanding, motion generation, and humanoid whole-body control. By combining H-GPT for versatile language-conditioned motion synthesis with H-ACT for cross-platform, policy-agnostic motion execution, FRoM-W1 enables humanoid robots to follow natural-language instructions with coherent, semantically grounded, and physically stable behaviors across multiple embodiments. These results position FRoM-W1 as a step toward practical general-purpose humanoid intelligence. 

In addition to demonstrating the overall effectiveness of our framework, we have also identified and highlighted several shortcomings within the field that need further improvement. These include the need for larger and higher-quality human motion datasets to enable models to generate actions that are more aligned with textual descriptions, produce motions more suitable for real-world deployment, and ensure that general motion trackers can better follow the noisy motions generated by models. These all require our entire community to work together for further improvement. 

### **References** 

- [1] Zhaoyuan Gu, Junheng Li, Wenlan Shen, Wenhao Yu, Zhaoming Xie, Stephen McCrory, Xianyi Cheng, Abdulaziz Shamsah, Robert J. Griffin, C. Karen Liu, Abderrahmane Kheddar, Xue Bin Peng, Yuke Zhu, Guanya Shi, Quan Nguyen, Gordon Cheng, Huijun Gao, and Ye Zhao. Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning. _CoRR_ , abs/2501.02116, 2025. doi: 10.48550/ARXIV.2501.02116. URL https://doi.org/10.48550/arXiv.2501.02116. 

- [2] Kento Kawaharazuka, Jihoon Oh, Jun Yamada, Ingmar Posner, and Yuke Zhu. Vision-languageaction models for robotics: A review towards real-world applications. _IEEE Access_ , 13:162467– 162504, 2025. doi: 10.1109/ACCESS.2025.3609980. URL https://doi.org/10.1109/ACCESS. 2025.3609980. 

- [3] Matthew Chignoli, Donghyun Kim, Elijah Stanger-Jones, and Sangbae Kim. The MIT humanoid robot: Design, motion planning, and control for acrobatic behaviors. In _20th IEEERAS International Conference on Humanoid Robots, Humanoids 2021, Munich, Germany, July 19-21, 2021_ , pages 1–8. IEEE, 2021. doi: 10.1109/HUMANOIDS47582.2021.9555782. URL https://doi.org/10.1109/HUMANOIDS47582.2021.9555782. 

- [4] Ziwen Zhuang, Shenzhe Yao, and Hang Zhao. Humanoid parkour learning. In Pulkit Agrawal, Oliver Kroemer, and Wolfram Burgard, editors, _Conference on Robot Learning, 6-9 November 2024, Munich, Germany_ , volume 270 of _Proceedings of Machine Learning Research_ , pages 1975– 1991. PMLR, 2024. URL https://proceedings.mlr.press/v270/zhuang25a.html. 

- [5] Zixuan Chen, Xialin He, Yen-Jen Wang, Qiayuan Liao, Yanjie Ze, Zhongyu Li, S. Shankar Sastry, Jiajun Wu, Koushil Sreenath, Saurabh Gupta, and Xue Bin Peng. Learning smooth humanoid locomotion through lipschitz-constrained policies. _CoRR_ , abs/2410.11825, 2024. doi: 10. 48550/ARXIV.2410.11825. URL https://doi.org/10.48550/arXiv.2410.11825. 

22 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

- [6] Huayi Wang, Zirui Wang, Junli Ren, Qingwei Ben, Tao Huang, Weinan Zhang, and Jiangmiao Pang. Beamdojo: Learning agile humanoid locomotion on sparse footholds. _CoRR_ , abs/2502.10363, 2025. doi: 10.48550/ARXIV.2502.10363. URL https://doi.org/10.48550/ arXiv.2502.10363. 

- [7] Weiji Xie, Jinrui Han, Jiakun Zheng, Huanyu Li, Xinzhe Liu, Jiyuan Shi, Weinan Zhang, Chenjia Bai, and Xuelong Li. Kungfubot: Physics-based humanoid whole-body control for learning highly-dynamic skills. _CoRR_ , abs/2506.12851, 2025. doi: 10.48550/ARXIV.2506.12851. URL https://doi.org/10.48550/arXiv.2506.12851. 

- [8] Zhi Su, Bike Zhang, Nima Rahmanian, Yuman Gao, Qiayuan Liao, Caitlin Regan, Koushil Sreenath, and S. Shankar Sastry. HITTER: A humanoid table tennis robot via hierarchical planning and learning. _CoRR_ , abs/2508.21043, 2025. doi: 10.48550/ARXIV.2508.21043. URL https://doi.org/10.48550/arXiv.2508.21043. 

- [9] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul F. Christiano, Jan Leike, and Ryan Lowe. Training language models to follow instructions with human feedback. In Sanmi Koyejo, S. Mohamed, A. Agarwal, Danielle Belgrave, K. Cho, and A. Oh, editors, _Advances in Neural Information Processing Systems 35: Annual Conference on Neural Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 - December 9, 2022_ , 2022. URL http://papers.nips.cc/paper_files/paper/2022/hash/ b1efde53be364a73914f58805a001731-Abstract-Conference.html. 

- [10] Tianxiang Sun, Xiaotian Zhang, Zhengfu He, Peng Li, Qinyuan Cheng, Xiangyang Liu, Hang Yan, Yunfan Shao, Qiong Tang, Shiduo Zhang, Xingjian Zhao, Ke Chen, Yining Zheng, Zhejian Zhou, Ruixiao Li, Jun Zhan, Yunhua Zhou, Linyang Li, Xiaogui Yang, Lingling Wu, Zhangyue Yin, Xuanjing Huang, Yu-Gang Jiang, and Xipeng Qiu. MOSS: an open conversational large language model. _Mach. Intell. Res._ , 21(5):888–905, 2024. doi: 10.1007/S11633-024-1502-8. URL https://doi.org/10.1007/s11633-024-1502-8. 

- [11] Llama Team. The llama 3 herd of models. _CoRR_ , abs/2407.21783, 2024. doi: 10.48550/ ARXIV.2407.21783. URL https://doi.org/10.48550/arXiv.2407.21783. 

- [12] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, Chujie Zheng, Dayiheng Liu, Fan Zhou, Fei Huang, Feng Hu, Hao Ge, Haoran Wei, Huan Lin, Jialong Tang, Jian Yang, Jianhong Tu, Jianwei Zhang, Jian Yang, Jiaxi Yang, Jingren Zhou, Junyang Lin, Kai Dang, Keqin Bao, Kexin Yang, Le Yu, Lianghao Deng, Mei Li, Mingfeng Xue, Mingze Li, Pei Zhang, Peng Wang, Qin Zhu, Rui Men, Ruize Gao, Shixuan Liu, Shuang Luo, Tianhao Li, Tianyi Tang, Wenbiao Yin, Xingzhang Ren, Xinyu Wang, Xinyu Zhang, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yinger Zhang, Yu Wan, Yuqiong Liu, Zekun Wang, Zeyu Cui, Zhenru Zhang, Zhipeng Zhou, and Zihan Qiu. Qwen3 technical report. _CoRR_ , abs/2505.09388, 2025. doi: 10.48550/ARXIV.2505.09388. URL https://doi.org/10.48550/arXiv.2505.09388. 

- [13] Tairan He, Zhengyi Luo, Wenli Xiao, Chong Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Learning human-to-humanoid real-time whole-body teleoperation. In _IEEE/RSJ International Conference on Intelligent Robots and Systems, IROS 2024, Abu Dhabi, United Arab Emirates, October 14-18, 2024_ , pages 8944–8951. IEEE, 2024. doi: 10.1109/IROS58592.2024.10801984. URL https://doi.org/10.1109/IROS58592.2024.10801984. 

23 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

- [14] Yixuan Li, Yutang Lin, Jieming Cui, Tengyu Liu, Wei Liang, Yixin Zhu, and Siyuan Huang. CLONE: closed-loop whole-body humanoid teleoperation for long-horizon tasks. _CoRR_ , abs/2506.08931, 2025. doi: 10.48550/ARXIV.2506.08931. URL https://doi.org/10.48550/ arXiv.2506.08931. 

- [15] Zhenyu Zhao, Hongyi Jing, Xiawei Liu, Jiageng Mao, Abha Jha, Hanwen Yang, Rong Xue, Sergey Zakharor, Vitor Guizilini, and Yue Wang. Humanoid everyday: A comprehensive robotic dataset for open-world humanoid manipulation. _CoRR_ , abs/2510.08807, 2025. doi: 10.48550/ ARXIV.2510.08807. URL https://doi.org/10.48550/arXiv.2510.08807. 

- [16] Tong Zhang, Boyuan Zheng, Ruiqian Nai, Yingdong Hu, Yen-Jen Wang, Geng Chen, Fanqi Lin, Jiongye Li, Chuye Hong, Koushil Sreenath, and Yang Gao. Hub: Learning extreme humanoid balance. _CoRR_ , abs/2505.07294, 2025. doi: 10.48550/ARXIV.2505.07294. URL https://doi. org/10.48550/arXiv.2505.07294. 

- [17] Ziyu Meng, Tengyu Liu, Le Ma, Yingying Wu, Ran Song, Wei Zhang, and Siyuan Huang. Safefall: Learning protective control for humanoid robots, 2025. URL https://arxiv.org/abs/2511. 18509. 

- [18] Eric R Kandel, James H Schwartz, Thomas M Jessell, Steven Siegelbaum, A James Hudspeth, Sarah Mack, et al. _Principles of neural science_ , volume 4. McGraw-hill New York, 2000. 

- [19] Michael S Gazzaniga, Richard B Ivry, and GR Mangun. Cognitive neuroscience. the biology of the mind.(2014), 2006. 

- [20] Chuan Guo, Shihao Zou, Xinxin Zuo, Sen Wang, Wei Ji, Xingyu Li, and Li Cheng. Generating diverse and natural 3d human motions from text. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2022, New Orleans, LA, USA, June 18-24, 2022_ , pages 5142–5151. IEEE, 2022. doi: 10.1109/CVPR52688.2022.00509. URL https://doi.org/10. 1109/CVPR52688.2022.00509. 

- [21] Jing Lin, Ailing Zeng, Shunlin Lu, Yuanhao Cai, Ruimao Zhang, Haoqian Wang, and Lei Zhang. Motion-x: A large-scale 3d expressive whole-body human motion dataset. In Alice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz Hardt, and Sergey Levine, editors, _Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023_ , 2023. URL http://papers.nips.cc/paper_files/paper/2023/hash/ 4f8e27f6036c1d8b4a66b5b3a947dd7b-Abstract-Datasets_and_Benchmarks.html. 

- [22] Ke Fan, Shunlin Lu, Minyue Dai, Runyi Yu, Lixing Xiao, Zhiyang Dou, Junting Dong, Lizhuang Ma, and Jingbo Wang. Go to zero: Towards zero-shot motion generation with million-scale data. _CoRR_ , abs/2507.07095, 2025. doi: 10.48550/ARXIV.2507.07095. URL https://doi.org/ 10.48550/arXiv.2507.07095. 

- [23] Aäron van den Oord, Oriol Vinyals, and Koray Kavukcuoglu. Neural discrete representation learning. In Isabelle Guyon, Ulrike von Luxburg, Samy Bengio, Hanna M. Wallach, Rob Fergus, S. V. N. Vishwanathan, and Roman Garnett, editors, _Advances in Neural Information Processing Systems 30: Annual Conference on Neural Information Processing Systems 2017, December 4- 9, 2017, Long Beach, CA, USA_ , pages 6306–6315, 2017. URL https://proceedings.neurips.cc/ paper/2017/hash/7a98af17e63a0ac09ce2e96d03992fbc-Abstract.html. 

- [24] Jianrong Zhang, Yangsong Zhang, Xiaodong Cun, Shaoli Huang, Yong Zhang, Hongwei Zhao, Hongtao Lu, and Xi Shen. T2M-GPT: generating human motion from textual descriptions with 

24 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

   - discrete representations. _CoRR_ , abs/2301.06052, 2023. doi: 10.48550/ARXIV.2301.06052. URL https://doi.org/10.48550/arXiv.2301.06052. 

- [25] Biao Jiang, Xin Chen, Wen Liu, Jingyi Yu, Gang Yu, and Tao Chen. Motiongpt: Human motion as a foreign language. In Alice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz Hardt, and Sergey Levine, editors, _Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023_ , 2023. URL http://papers.nips.cc/paper_files/paper/2023/ hash/3fbf0c1ea0716c03dea93bb6be78dd6f-Abstract-Conference.html. 

- [26] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language models. In Sanmi Koyejo, S. Mohamed, A. Agarwal, Danielle Belgrave, K. Cho, and A. Oh, editors, _Advances in Neural Information Processing Systems 35: Annual Conference on Neural Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 - December 9, 2022_ , 2022. URL http://papers.nips.cc/paper_files/paper/2022/hash/ 9d5609613524ecf4f15af0f7b31abca4-Abstract-Conference.html. 

- [27] DeepSeek-AI. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _CoRR_ , abs/2501.12948, 2025. doi: 10.48550/ARXIV.2501.12948. URL https: //doi.org/10.48550/arXiv.2501.12948. 

- [28] Georgios Pavlakos, Vasileios Choutas, Nima Ghorbani, Timo Bolkart, Ahmed A. A. Osman, Dimitrios Tzionas, and Michael J. Black. Expressive body capture: 3d hands, face, and body from a single image. In _IEEE Conference on Computer Vision and Pattern Recognition, CVPR 2019, Long Beach, CA, USA, June 16-20, 2019_ , pages 10975–10985. Computer Vision Foundation / IEEE, 2019. doi: 10.1109/CVPR.2019.01123. URL http://openaccess.thecvf.com/content_CVPR_2019/html/Pavlakos_Expressive_Body_ Capture_3D_Hands_Face_and_Body_From_a_CVPR_2019_paper.html. 

- [29] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous human-to-humanoid wholebody teleoperation and learning, 2024. URL https://arxiv.org/abs/2406.08858. 

- [30] Yanjie Ze, Zixuan Chen, João Pedro Araújo, Zi-ang Cao, Xue Bin Peng, Jiajun Wu, and C. Karen Liu. TWIST: teleoperated whole-body imitation system. _CoRR_ , abs/2505.02833, 2025. doi: 10.48550/ARXIV.2505.02833. URL https://doi.org/10.48550/arXiv.2505.02833. 

- [31] Qiayuan Liao, Takara E. Truong, Xiaoyu Huang, Guy Tevet, Koushil Sreenath, and C. Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _CoRR_ , abs/2508.08241, 2025. doi: 10.48550/ARXIV.2508.08241. URL https://doi.org/10. 48550/arXiv.2508.08241. 

- [32] Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, and Gavriel State. Isaac gym: High performance GPU based physics simulation for robot learning. In Joaquin Vanschoren and Sai-Kit Yeung, editors, _Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks 1, NeurIPS Datasets and Benchmarks 2021, December 2021, virtual_ , 2021. URL https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/ 28dd2c7955ce926456240b2ff0100bde-Abstract-round2.html. 

- [33] Yufei Xue, Wentao Dong, Minghuan Liu, Weinan Zhang, and Jiangmiao Pang. A unified and general humanoid whole-body controller for versatile locomotion, 2025. URL https://arxiv. org/abs/2502.03206. 

25 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

- [34] Chuan Guo, Xinxin Zuo, Sen Wang, and Li Cheng. TM2T: stochastic and tokenized modeling for the reciprocal generation of 3d human motions and texts. In Shai Avidan, Gabriel J. Brostow, Moustapha Cissé, Giovanni Maria Farinella, and Tal Hassner, editors, _Computer Vision - ECCV 2022 - 17th European Conference, Tel Aviv, Israel, October 23-27, 2022, Proceedings, Part XXXV_ , volume 13695 of _Lecture Notes in Computer Science_ , pages 580–597. Springer, 2022. doi: 10. 1007/978-3-031-19833-5\_34. URL https://doi.org/10.1007/978-3-031-19833-5_34. 

- [35] Ali Razavi, Aäron van den Oord, and Oriol Vinyals. Generating diverse high-fidelity images with VQ-VAE-2. In Hanna M. Wallach, Hugo Larochelle, Alina Beygelzimer, Florence d’Alché-Buc, Emily B. Fox, and Roman Garnett, editors, _Advances in Neural Information Processing Systems 32: Annual Conference on Neural Information Processing Systems 2019, NeurIPS 2019, December 8-14, 2019, Vancouver, BC, Canada_ , pages 14837–14847, 2019. URL https://proceedings. neurips.cc/paper/2019/hash/5f8e2fa1718d1bbcadf1cd9c7a54fb8c-Abstract.html. 

- [36] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models. In _The Tenth International Conference on Learning Representations, ICLR 2022, Virtual Event, April 2529, 2022_ . OpenReview.net, 2022. URL https://openreview.net/forum?id=nZeVKeeFYf9. 

- [37] Jiefeng Li, Chao Xu, Zhicun Chen, Siyuan Bian, Lixin Yang, and Cewu Lu. Hybrik: A hybrid analytical-neural inverse kinematics solution for 3d human pose and shape estimation. In _IEEE Conference on Computer Vision and Pattern Recognition, CVPR 2021, virtual, June 19-25, 2021_ , pages 3383–3393. Computer Vision Foundation / IEEE, 2021. doi: 10.1109/CVPR46437.2021.00339. URL https://openaccess.thecvf.com/content/CVPR2021/ html/Li_HybrIK_A_Hybrid_Analytical-Neural_Inverse_Kinematics_Solution_for_3D_ Human_CVPR_2021_paper.html. 

- [38] F. Bullo and S. L. Smith. _Lectures on Robotic Planning and Kinematics_ . Unpublished Manuscript, .94 edition, 2025. 

- [39] Zhengyi Luo, Jinkun Cao, Alexander Winkler, Kris Kitani, and Weipeng Xu. Perpetual humanoid control for real-time simulated avatars. In _IEEE/CVF International Conference on Computer Vision, ICCV 2023, Paris, France, October 1-6, 2023_ , pages 10861–10870. IEEE, 2023. doi: 10.1109/ICCV51070.2023.01000. URL https://doi.org/10.1109/ICCV51070.2023.01000. 

- [40] Naureen Mahmood, Nima Ghorbani, Nikolaus F. Troje, Gerard Pons-Moll, and Michael J. Black. AMASS: archive of motion capture as surface shapes. In _2019 IEEE/CVF International Conference on Computer Vision, ICCV 2019, Seoul, Korea (South), October 27 - November 2, 2019_ , pages 5441–5450. IEEE, 2019. doi: 10.1109/ICCV.2019.00554. URL https: //doi.org/10.1109/ICCV.2019.00554. 

- [41] Stéphane Ross, Geoffrey J. Gordon, and Drew Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In Geoffrey J. Gordon, David B. Dunson, and Miroslav Dudík, editors, _Proceedings of the Fourteenth International Conference on Artificial Intelligence and Statistics, AISTATS 2011, Fort Lauderdale, USA, April 11-13, 2011_ , volume 15 of _JMLR Proceedings_ , pages 627–635. JMLR.org, 2011. URL http://proceedings.mlr.press/v15/ ross11a/ross11a.pdf. 

- [42] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _CoRR_ , abs/1707.06347, 2017. URL http://arxiv.org/abs/1707.06347. 

- [43] Jialong Li, Xuxin Cheng, Tianshu Huang, Shiqi Yang, Ri-Zhao Qiu, and Xiaolong Wang. AMO: adaptive motion optimization for hyper-dexterous humanoid whole-body control. _CoRR_ , 

26 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

abs/2505.03738, 2025. doi: 10.48550/ARXIV.2505.03738. URL https://doi.org/10.48550/ arXiv.2505.03738. 

- [44] Yufei Xue, Wentao Dong, Minghuan Liu, Weinan Zhang, and Jiangmiao Pang. A unified and general humanoid whole-body controller for fine-grained locomotion. _CoRR_ , abs/2502.03206, 2025. doi: 10.48550/ARXIV.2502.03206. URL https://doi.org/10.48550/arXiv.2502.03206. 

- [45] Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbab, Chaoyi Pan, Zeji Yi, Guannan Qu, Kris Kitani, Jessica K. Hodgins, Linxi Fan, Yuke Zhu, Changliu Liu, and Guanya Shi. ASAP: aligning simulation and real-world physics for learning agile humanoid whole-body skills. _CoRR_ , abs/2502.01143, 2025. doi: 10.48550/ARXIV.2502.01143. URL https://doi.org/10.48550/arXiv.2502.01143. 

- [46] Chuan Guo, Xinxin Zuo, Sen Wang, Shihao Zou, Qingyao Sun, Annan Deng, Minglun Gong, and Li Cheng. Action2motion: Conditioned generation of 3d human motions. In Chang Wen Chen, Rita Cucchiara, Xian-Sheng Hua, Guo-Jun Qi, Elisa Ricci, Zhengyou Zhang, and Roger Zimmermann, editors, _MM ’20: The 28th ACM International Conference on Multimedia, Virtual Event / Seattle, WA, USA, October 12-16, 2020_ , pages 2021–2029. ACM, 2020. doi: 10.1145/ 3394171.3413635. URL https://doi.org/10.1145/3394171.3413635. 

- [47] Matthew Loper, Naureen Mahmood, Javier Romero, Gerard Pons-Moll, and Michael J. Black. SMPL: a skinned multi-person linear model. _ACM Trans. Graph._ , 34(6):248:1–248:16, 2015. doi: 10.1145/2816795.2818013. URL https://doi.org/10.1145/2816795.2818013. 

- [48] Xin Chen, Biao Jiang, Wen Liu, Zilong Huang, Bin Fu, Tao Chen, and Gang Yu. Executing your commands via motion diffusion in latent space. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2023, Vancouver, BC, Canada, June 17-24, 2023_ , pages 18000– 18010. IEEE, 2023. doi: 10.1109/CVPR52729.2023.01726. URL https://doi.org/10.1109/ CVPR52729.2023.01726. 

- [49] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and Illia Polosukhin. Attention is all you need. In Isabelle Guyon, Ulrike von Luxburg, Samy Bengio, Hanna M. Wallach, Rob Fergus, S. V. N. Vishwanathan, and Roman Garnett, editors, _Advances in Neural Information Processing Systems 30: Annual Conference on Neural Information Processing Systems 2017, December 4-9, 2017, Long Beach, CA, USA_ , pages 5998–6008, 2017. URL https://proceedings.neurips.cc/paper/2017/hash/ 3f5ee243547dee91fbd053c1c4a845aa-Abstract.html. 

- [50] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. In Hugo Larochelle, Marc’Aurelio Ranzato, Raia Hadsell, Maria-Florina Balcan, and Hsuan-Tien Lin, editors, _Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual_ , 2020. URL https://proceedings.neurips.cc/paper/2020/hash/ 4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html. 

- [51] Mingyuan Zhang, Zhongang Cai, Liang Pan, Fangzhou Hong, Xinying Guo, Lei Yang, and Ziwei Liu. Motiondiffuse: Text-driven human motion generation with diffusion model. _IEEE Trans. Pattern Anal. Mach. Intell._ , 46(6):4115–4128, 2024. doi: 10.1109/TPAMI.2024.3355414. URL https://doi.org/10.1109/TPAMI.2024.3355414. 

- [52] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, and Ilya Sutskever. Learning transferable visual models from natural language supervision. In Marina 

27 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

Meila and Tong Zhang, editors, _Proceedings of the 38th International Conference on Machine Learning, ICML 2021, 18-24 July 2021, Virtual Event_ , volume 139 of _Proceedings of Machine Learning Research_ , pages 8748–8763. PMLR, 2021. URL http://proceedings.mlr.press/v139/ radford21a.html. 

- [53] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Björn Ommer. Highresolution image synthesis with latent diffusion models. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2022, New Orleans, LA, USA, June 18-24, 2022_ , pages 10674–10685. IEEE, 2022. doi: 10.1109/CVPR52688.2022.01042. URL https://doi.org/10. 1109/CVPR52688.2022.01042. 

- [54] Yi Zhou, Connelly Barnes, Jingwan Lu, Jimei Yang, and Hao Li. On the continuity of rotation representations in neural networks. In _IEEE Conference on Computer Vision and Pattern Recognition, CVPR 2019, Long Beach, CA, USA, June 16-20, 2019_ , pages 5745– 5753. Computer Vision Foundation / IEEE, 2019. doi: 10.1109/CVPR.2019.00589. URL http://openaccess.thecvf.com/content_CVPR_2019/html/Zhou_On_the_Continuity_of_ Rotation_Representations_in_Neural_Networks_CVPR_2019_paper.html. 

- [55] Baolin Peng, Chunyuan Li, Pengcheng He, Michel Galley, and Jianfeng Gao. Instruction tuning with GPT-4. _CoRR_ , abs/2304.03277, 2023. doi: 10.48550/ARXIV.2304.03277. URL https: //doi.org/10.48550/arXiv.2304.03277. 

- [56] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems, IROS 2012, Vilamoura, Algarve, Portugal, October 7-12, 2012_ , pages 5026–5033. IEEE, 2012. doi: 10.1109/IROS.2012.6386109. URL https://doi.org/10.1109/IROS.2012.6386109. 

- [57] Clemens Schwarke, Mayank Mittal, Nikita Rudin, David Hoeller, and Marco Hutter. RSL-RL: A learning library for robotics research. _CoRR_ , abs/2509.10771, 2025. doi: 10.48550/ARXIV. 2509.10771. URL https://doi.org/10.48550/arXiv.2509.10771. 

- [58] Guy Tevet, Sigal Raab, Brian Gordon, Yonatan Shafir, Daniel Cohen-Or, and Amit H. Bermano. Human motion diffusion model. _CoRR_ , abs/2209.14916, 2022. doi: 10.48550/ARXIV.2209. 14916. URL https://doi.org/10.48550/arXiv.2209.14916. 

- [59] Chuan Guo, Yuxuan Mu, Muhammad Gohar Javed, Sen Wang, and Li Cheng. Momask: Generative masked modeling of 3d human motions. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2024, Seattle, WA, USA, June 16-22, 2024_ , pages 1900–1910. IEEE, 2024. doi: 10.1109/CVPR52733.2024.00186. URL https://doi.org/10.1109/CVPR52733. 2024.00186. 

- [60] Runqi Ouyang, Haoyun Li, Zhenyuan Zhang, Xiaofeng Wang, Zheng Zhu, Guan Huang, and Xingang Wang. Motion-r1: Chain-of-thought reasoning and reinforcement learning for human motion generation. _CoRR_ , abs/2506.10353, 2025. doi: 10.48550/ARXIV.2506.10353. URL https://doi.org/10.48550/arXiv.2506.10353. 

- [61] Shunlin Lu, Ling-Hao Chen, Ailing Zeng, Jing Lin, Ruimao Zhang, Lei Zhang, and HeungYeung Shum. Humantomato: Text-aligned whole-body motion generation. In _Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024_ . OpenReview.net, 2024. URL https://openreview.net/forum?id=maVIKlGqr7. 

- [62] Yuan Wang, Di Huang, Yaqi Zhang, Wanli Ouyang, Jile Jiao, Xuetao Feng, Yan Zhou, Pengfei Wan, Shixiang Tang, and Dan Xu. Motiongpt-2: A general-purpose motion-language model for 

28 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

motion generation and understanding. _CoRR_ , abs/2410.21747, 2024. doi: 10.48550/ARXIV. 2410.21747. URL https://doi.org/10.48550/arXiv.2410.21747. 

- [63] Yuxuan Bian, Ailing Zeng, Xuan Ju, Xian Liu, Zhaoyang Zhang, Wei Liu, and Qiang Xu. Motioncraft: Crafting whole-body motion with plug-and-play multimodal controls. In Toby Walsh, Julie Shah, and Zico Kolter, editors, _AAAI-25, Sponsored by the Association for the Advancement of Artificial Intelligence, February 25 - March 4, 2025, Philadelphia, PA, USA_ , pages 1880–1888. AAAI Press, 2025. doi: 10.1609/AAAI.V39I2.32183. URL https://doi.org/10.1609/aaai.v39i2. 32183. 

- [64] Xuxin Cheng, Yandong Ji, Junming Chen, Ruihan Yang, Ge Yang, and Xiaolong Wang. Expressive whole-body control for humanoid robots. In Dana Kulic, Gentiane Venture, Kostas E. Bekris, and Enrique Coronado, editors, _Robotics: Science and Systems XX, Delft, The Netherlands, July 15-19, 2024_ , 2024. doi: 10.15607/RSS.2024.XX.107. URL https://doi.org/10. 15607/RSS.2024.XX.107. 

- [65] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris M. Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. In Pulkit Agrawal, Oliver Kroemer, and Wolfram Burgard, editors, _Conference on Robot Learning, 6-9 November 2024, Munich, Germany_ , volume 270 of _Proceedings of Machine Learning Research_ , pages 1516–1540. PMLR, 2024. URL https://proceedings.mlr.press/v270/he25b.html. 

- [66] Zipeng Fu, Qingqing Zhao, Qi Wu, Gordon Wetzstein, and Chelsea Finn. Humanplus: Humanoid shadowing and imitation from humans. In Pulkit Agrawal, Oliver Kroemer, and Wolfram Burgard, editors, _Conference on Robot Learning, 6-9 November 2024, Munich, Germany_ , volume 270 of _Proceedings of Machine Learning Research_ , pages 2828–2844. PMLR, 2024. URL https://proceedings.mlr.press/v270/fu25a.html. 

- [67] Tairan He, Wenli Xiao, Toru Lin, Zhengyi Luo, Zhenjia Xu, Zhenyu Jiang, Jan Kautz, Changliu Liu, Guanya Shi, Xiaolong Wang, Linxi Jim Fan, and Yuke Zhu. HOVER: versatile neural wholebody controller for humanoid robots. In _IEEE International Conference on Robotics and Automation, ICRA 2025, Atlanta, GA, USA, May 19-23, 2025_ , pages 9989–9996. IEEE, 2025. doi: 10. 1109/ICRA55743.2025.11128549. URL https://doi.org/10.1109/ICRA55743.2025.11128549. 

- [68] Yanjie Ze, Siheng Zhao, Weizhuo Wang, Angjoo Kanazawa, Rocky Duan, Pieter Abbeel, Guanya Shi, Jiajun Wu, and C. Karen Liu. TWIST2: scalable, portable, and holistic humanoid data collection system. _CoRR_ , abs/2511.02832, 2025. doi: 10.48550/ARXIV.2511.02832. URL https://doi.org/10.48550/arXiv.2511.02832. 

- [69] Qingwei Ben, Feiyu Jia, Jia Zeng, Junting Dong, Dahua Lin, and Jiangmiao Pang. HOMIE: humanoid loco-manipulation with isomorphic exoskeleton cockpit. _CoRR_ , abs/2502.13013, 2025. doi: 10.48550/ARXIV.2502.13013. URL https://doi.org/10.48550/arXiv.2502.13013. 

- [70] Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Castañeda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, Xingye Da, Runyu Ding, Cyrus Hogg, Lina Song, Edy Lim, Eugene Jeong, Tairan He, Haoru Xue, Wenli Xiao, Zi Wang, Simon Yuen, Jan Kautz, Yan Chang, Umar Iqbal, Linxi Fan, and Yuke Zhu. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [71] Mazeyu Ji, Xuanbin Peng, Fangchen Liu, Jialong Li, Ge Yang, Xuxin Cheng, and Xiaolong Wang. Exbody2: Advanced expressive humanoid whole-body control. _CoRR_ , abs/2412.13196, 2024. doi: 10.48550/ARXIV.2412.13196. URL https://doi.org/10.48550/arXiv.2412.13196. 

29 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

- [72] Zixuan Chen, Mazeyu Ji, Xuxin Cheng, Xuanbin Peng, Xue Bin Peng, and Xiaolong Wang. GMT: general motion tracking for humanoid whole-body control. _CoRR_ , abs/2506.14770, 2025. doi: 10.48550/ARXIV.2506.14770. URL https://doi.org/10.48550/arXiv.2506.14770. 

- [73] Kangning Yin, Weishuai Zeng, Ke Fan, Zirui Wang, Qiang Zhang, Zheng Tian, Jingbo Wang, Jiangmiao Pang, and Weinan Zhang. Unitracker: Learning universal whole-body motion tracker for humanoid robots. _CoRR_ , abs/2507.07356, 2025. doi: 10.48550/ARXIV.2507. 07356. URL https://doi.org/10.48550/arXiv.2507.07356. 

- [74] Agon Serifi, Ruben Grandia, Espen Knoop, Markus Gross, and Moritz Bächer. Robot motion diffusion model: Motion generation for robotic characters. In Takeo Igarashi, Ariel Shamir, and Hao (Richard) Zhang, editors, _SIGGRAPH Asia 2024 Conference Papers, SA 2024, Tokyo, Japan, December 3-6, 2024_ , pages 50:1–50:9. ACM, 2024. doi: 10.1145/3680528.3687626. URL https://doi.org/10.1145/3680528.3687626. 

- [75] Zhenyu Jiang, Yuqi Xie, Jinhan Li, Ye Yuan, Yifeng Zhu, and Yuke Zhu. Harmon: Whole-body motion generation of humanoid robots from language descriptions. In Pulkit Agrawal, Oliver Kroemer, and Wolfram Burgard, editors, _Conference on Robot Learning, 6-9 November 2024, Munich, Germany_ , volume 270 of _Proceedings of Machine Learning Research_ , pages 3015–3026. PMLR, 2024. URL https://proceedings.mlr.press/v270/jiang25b.html. 

- [76] Jiageng Mao, Siheng Zhao, Siqi Song, Tianheng Shi, Junjie Ye, Mingtong Zhang, Haoran Geng, Jitendra Malik, Vitor Guizilini, and Yue Wang. Learning from massive human videos for universal humanoid pose control. _CoRR_ , abs/2412.14172, 2024. doi: 10.48550/ARXIV.2412.14172. URL https://doi.org/10.48550/arXiv.2412.14172. 

- [77] Yiyang Shao, Xiaoyu Huang, Bike Zhang, Qiayuan Liao, Yuman Gao, Yufeng Chi, Zhongyu Li, Yakun Sophia Shao, and Koushil Sreenath. Langwbc: Language-directed humanoid wholebody control via end-to-end learning. _CoRR_ , abs/2504.21738, 2025. doi: 10.48550/ARXIV. 2504.21738. URL https://doi.org/10.48550/arXiv.2504.21738. 

- [78] Haoru Xue, Xiaoyu Huang, Dantong Niu, Qiayuan Liao, Thomas Kragerud, Jan Tommy Gravdahl, Xue Bin Peng, Guanya Shi, Trevor Darrell, Koushil Sreenath, and S. Shankar Sastry. Leverb: Humanoid whole-body control with latent vision-language instruction. _CoRR_ , abs/2506.13751, 2025. doi: 10.48550/ARXIV.2506.13751. URL https://doi.org/10.48550/ arXiv.2506.13751. 

- [79] Zhe Li, Cheng Chi, Yangyang Wei, Boan Zhu, Yibo Peng, Tao Huang, Pengwei Wang, Zhongyuan Wang, Shanghang Zhang, and Chang Xu. From language to locomotion: Retargeting-free humanoid control via motion latent guidance. _CoRR_ , abs/2510.14952, 2025. doi: 10.48550/ARXIV.2510.14952. URL https://doi.org/10.48550/arXiv.2510.14952. 

- [80] Junpeng Yue, Zepeng Wang, Yuxuan Wang, Weishuai Zeng, Jiangxing Wang, Xinrun Xu, Yu Zhang, Sipeng Zheng, Ziluo Ding, and Zongqing Lu. RL from physical feedback: Aligning large motion models with humanoid control. _CoRR_ , abs/2506.12769, 2025. doi: 10.48550/ ARXIV.2506.12769. URL https://doi.org/10.48550/arXiv.2506.12769. 

- [81] Zhirui Liu, Kaiyang Ji, Ke Yang, Jingyi Yu, Ye Shi, and Jingya Wang. Commanding humanoid by free-form language: A large language action model with unified motion vocabulary. _arXiv preprint arXiv:2511.22963_ , 2025. 

30 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

# **Appendix** 

|**A**<br>**Mor**|**e Implementation Details of** H-GPT|**31**|
|---|---|---|
|A.1|Training Data Construction forH-GPT . . . . . . . . . . . . . .|. . . . . . . . . . . .<br>31|
|A.2|More Chain-of-Thought Evaluation Cases . . . . . . . . . . . . .|. . . . . . . . . . . .<br>31|
|**B**<br>**Mor**|**e Implementation Details of** H-ACT|**32**|
|B.1|Hardware and Deployment Setup . . . . . . . . . . . . . . . . .|. . . . . . . . . . . .<br>32|
|B.2|RoboJuDo Deployment Framework . . . . . . . . . . . . . . . .|. . . . . . . . . . . .<br>33|
|B.3|Sim2Real Transfer Details . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . .<br>35|


### **A. More Implementation Details of** H-GPT 

##### **A.1. Training Data Construction for** H-GPT 

We use GPT-4o to generate fine-grained CoT data based on language instructions from HumanML3DX and rendered videos. The model’s prompt is as follows: 

Based on the given motion video, make a plan in the first person within 1 to 2 sentences of how to accomplish the motion in the video. You can refer to the motion description [Two people are engaged in a casual chat.] to refine your plan, but the plan should accurately describe the motion in the video. Here are some examples: Example 1: Motion description: A person is waving goodbye. Plan: I stand upright with my hands at my sides, then raise my right hand, wave it up and down, and lower it back to its original position. Example 2: Motion description: You are an elephant. Plan: I take large steps forward, alternating feet, while swinging my hands and swing my head from side to side. Example 3: Motion description: a person walks and trips towards his left and then resumes walking. Plan: I walk forward, trip to my left, and awkwardly step with my left foot to regain balance. After stabilizing, I adjust my posture and continue walking with my arms swinging on my side. !!!Only output the plan.!!! !!!Do not generate uncertainty descriptions in the plan, e.g. ’...or...’!!! !!!Your plan must accurately and concisely describe the given motion video.!!! 

We represent the original hand-inclusive whole-body motion poses in the following format: 

- _𝑟_ �<sup>_𝑎_</sup> ∈ ℝ is root angular velocity along Y-axis; 

- (� _𝑟_<sup>_𝑥_</sup> _,_ � _𝑟_<sup>_𝑧_</sup> ∈ ℝ) are root linear velocities on XZ-plane; 

- _𝑟_<sup>_𝑦_</sup> ∈ ℝ is root height; 

- j<sup>_𝑝_</sup> ∈ ℝ<sup>3</sup><sup>_𝑗_</sup> , j<sup>_𝑣_</sup> ∈ ℝ<sup>3</sup><sup>_𝑗_</sup> , and j<sup>_𝑟_</sup> ∈ ℝ<sup>6</sup><sup>_𝑗_</sup> are the local joints’ positions, velocities, and rotations in root space, with _𝑗_ denoting the number of joints; 

- c<sup>_𝑓_</sup> ∈ ℝ<sup>4</sup> is binary features obtained by thresholding the heel and toe joint velocities to emphasize the foot ground contacts. 

##### **A.2. More Chain-of-Thought Evaluation Cases** 

Here are more examples of complex instructions: 

31 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

A person is running in place, then starts to run right and left, while jumping up and down. A person is kneeling down, coiling something in their hands, then stands, pours out of a bottle, and backs away to the right. 

A person walks forward, stops, and stands drinking something. 

A person uses their left hand and arm to move to the side, then front ways, and performs other movements, including waving. 

A person initially stands still, steps backward with both feet, and then slowly walks forward. 

And here are more examples of abstract instructions: 

Pantomime pulling a heavy rope hand over hand, showing the strain in your arms and back. Show dejection: slump your shoulders, hang your head, and shuffle your feet slowly. Beckon me to come closer with a curling motion of your index finger. Mime picking up a small, delicate cube from the table using a precise pinch grip. Walk to the nearest wall and gently press the palm of your hand against it. 

### **B. More Implementation Details of** H-ACT 

##### **B.1. Hardware and Deployment Setup** 

Our real-world deployment consists of two primary components: a high-performance inference workstation responsible for H-GPT model execution, and a full-size humanoid robot with hands used for H-ACT motion execution. We detail both components below. 

**Inference Server.** All model inference is performed on a high-performance workstation equipped with dual NVIDIA RTX 5090 GPUs with 32GB VRAM each, an AMD Threadripper 7970X CPU, and 128GB of RAM. The workstation communicates wirelessly with the onboard compute units of the deployed robots. 

**Humanoid Robot Platform.** To demonstrate the generality and practicality of our approach, we deploy our system on two humanoid robot platforms: the Unitree H1 and Unitree G1. Importantly, both deployments require no hardware modification, relying solely on software integration with the robot’s existing control and sensing infrastructure. _Unitree H1._ The H1 is a full-size bipedal humanoid robot equipped with 19 degrees of freedom in the body and an additional 2-DOF wrist. The manipulator is Inspire-Robotics 6-DOF dexterous hands, actuated by a DM-J4310-2EC motor at the wrist. For onboard computation, the robot is outfitted with Unitree’s official PC2 module, comprising an Intel i7-1355U CPU and 32GB of RAM. The PC2 executes the control policy and handles wireless communication with the external inference server. Additionally, a ZED Mini stereo camera is mounted on the torso for real-time odometry. The camera is connected to the Unitree Orin NX expansion dock, leveraging the ZED SDK’s positional_tracking service to estimate the robot’s global pose. The Orin NX communicates with the PC2 through the robot’s internal Ethernet switch, enabling low latency and tight integration between perception and control. 

_Unitree G1._ The G1 platform, in its EDU+ configuration, features 29 degrees of freedom and Unitree 7-DOF three-fingered Dex3-1 hands. For stability and consistent deployment, we follow the manufacturer’s manual to lock the waist pitch and roll joints. The control policy runs on the builtin PC2 unit (Jetson Orin NX 16GB), and no external compute is required. Global localization is 

32 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 


**Figure 16** | An illustration of the RoboJudo framework, including the pipeline control loop and the overall module architecture. 

supported by two interchangeable options: (1) replicating the ZED Mini configuration used on H1, or (2) utilizing the odometry service provided by the Unitree SDK. 

##### **B.2. RoboJuDo Deployment Framework** 

As illustrated in 16,RoboJudo adopts a unified module abstraction for _𝐶_ , _𝐸_ , and Π _𝜃_ , enabling modular composition and seamless integration across simulation and real-robot platforms. 

The **Controller** _𝐶_ standardizes diverse input sources—such as discrete key commands, continuous motion streams, and external triggers—into a consistent command interface. A hierarchical **Controller Manager** supports compositional logic, allowing for multi-level triggering (e.g., key combinations) and real-time motion adaption. 

The **Environment** _𝐸_ provides a platform-agnostic interface that abstracts robot communication, 

33 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

initialization alignment (e.g., born-place matching), and forward kinematics. This design ensures functional parity between simulation and real-robot execution, allowing policies to be transferred directly with minimal engineering overhead. 

The **Policy** Π _𝜃_ defines a unified interface for diverse control strategies. Each policy interacts with both the controller and the environment through standardized APIs — _𝑠𝑡_ and _𝑚𝑡_ , enabling consistent data flow and behavior representation across heterogeneous implementations. A dedicated **Policy Manager** governs multi-policy coordination and adaptation: it automatically aligns each policy’s degree-of-freedom configuration ( _DoFConfig_ ) with the target robot environment, dynamically handling joint remapping and scaling. This mechanism enables seamless switching and blending between heterogeneous policies within a single runtime pipeline, facilitating efficient experimentation and flexible behavior composition. 

**Controller** _𝐶_ **module.** The Controller module unifies multiple input sources, including joysticks, keyboards, remote signals, and reference motion streams from H-GPT. Raw inputs are collected into a normalized CTRL_DATA structure (e.g., axes, buttons, motion sequence). A motion-adaption layer then converts these signals into controller-specific motion descriptors, such as keypoint trajectories, joint states, body-link states, or root locomotion commands. The module also detects discrete COMMANDS (e.g., motion switching, mode toggles) via process_trigger(). This design allows the same downstream pipeline to operate with different human interfaces or autonomous sources by only changing controller configuration, while keeping the motion command format consistent. 

**Environment** _𝐸_ **module.** The Environment module provides a unified interface for both simulated and real humanoids. On the simulation side, it interfaces with MuJoCo to step the dynamics, while on the real side it communicates with platforms such as Unitree H1 (19 DoF) and Unitree G1 (29 DoF and 23 DoF). A born_place_align utility aligns the initial robot state with the reference motion, and a forward-kinematics service exposes link and keypoint information to other modules. The core API consists of step() and update(), which advance the simulation or read sensors, and populate ENV_DATA (including DoF state, sensor measurements, and Forward Kinematics information). Robotspecific details (DoF layouts, joint limits, PD gains, communication backends) are encapsulated in environment configurations, thus providing simple interface for robot interaction. 

**Policy Agent** Π _𝜃_ **module.** The Policy Agent module wraps different whole-body control strategies— upper–lower decoupled control, teleoperation-based control, and full-body motion tracking—behind a common interface. Each policy exposes standard methods such as reset(), get_observation(), get_action(), and optional call_back() hooks. The module outputs ACTION (low-level commands) and optionally EXTRA_INFO (e.g., hand pose, debug information) to facilitate analysis and visualization. 

**Automatic adaptation via DoFConfig and PolicyWrapper.** To support multiple robot embodiments without rewriting controllers, RoboJuDo introduces DoFConfig, including joint ordering, PD gains, that unifies interaction of different controllers and robots. The PolicyWrapper uses this configuration to automatically remap policy actions and observations between the controller’s internal convention and the target robot’s embodiment. As a result, the same policy implementation can be reused across robots that share similar semantics but differ in DoF layout, with adaptation handled declaratively through configuration rather than manual code changes. 

**Multi-policy switching and composition.** RoboJuDo includes a lightweight policy manager that supports runtime switching and composition of multiple policies. Based on COMMANDS from 

34 

FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions 

the Controller module, the manager can route ENV_DATA and CTRL_DATA to different Policy Agents, blend their outputs, or trigger hierarchical behaviors. Because all policies conform to the same ( _𝑠𝑡, 𝑚𝑡_ ) ↦→ _𝑎𝑡_ +1 abstraction, switching between them does not require changes to the Environment or Controller modules. This makes it straightforward to benchmark different WBC paradigms on the same motion sequences, or to compose complex behaviors from simpler skills. 

Overall, RoboJuDo provides a modular, configuration-driven pipeline that connects diverse input devices, simulation/real environments, and heterogeneous control policies. Combined with H-GPT and H-ACT, it forms a unified execution stack that can route generated motions through various controllers and embodiments with minimal engineering effort. 

##### **B.3. Sim2Real Transfer Details** 

During simulation-based training, we observed practical techniques that could significantly improve the performance and transferability of policies to real-world robotic platforms. 

**Handling Low-Inertia Joints** One key issue arises from low-inertia joints, such as those in the wrists or head. In simulation, these joints often exhibit high-frequency oscillations, limited by the numerical accuracy of the physics engine’s rigid body solver. These oscillations can destabilize training, hinder policy convergence, and exacerbate the gap between simulation and reality. 

To mitigate this, we recommend removing or freezing certain low-inertia degrees of freedom during training. For instance, wrist and head joints can be excluded from learning and reintroduced during real-world deployment with separate low-level controllers or scripted behaviors. This strategy has proven effective in improving the overall stability and robustness of the learned policy. 

35 

