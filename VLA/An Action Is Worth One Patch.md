---
title: "An Action Is Worth One Patch: Unified World-Action Modeling with PatchWAM"
date: "2026"
venue: "arXiv"
url: https://arxiv.org/abs/2609.25961
pdf: https://arxiv.org/pdf/2609.25961
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2609.25961)** / [論文ページ](https://arxiv.org/abs/2609.25961)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

AN ACTION IS WORTH ONE PATCH: UNIFIED WORLD–ACTION MODELING WITH PATCHWAM 

**Tianheng Wang**<sup>1</sup><sup>_,†_</sup> **Zhou Xie**<sup>2</sup> **Heng Jia**<sup>3</sup> **Jianhua Xu**<sup>4</sup> **Tong Zhang**<sup>5</sup> **Kaicheng Yu**<sup>1</sup><sup>_,_4</sup><sup>_,∗_</sup> 1Westlake University 2Lanzhou University 3Zhejiang University 4Awomo 5University of Chinese Academy of Sciences wangtianheng@westlake.edu.cn, xzhou2024@lzu.edu.cn, 12221194@zju.edu.cn xujianhua@westlakedi.com, tongzhang@ucas.ac.cn, kyu@westlakedi.com 

> _∗_ Corresponding author _†_ Work done during an internship at Awomo 

# ABSTRACT 

Generative visual models offer a foundation for learning representations of physical dynamics, yet their extension to continuous control raises a fundamental question: do visual prediction and action generation require separate computational pathways? Existing approaches usually introduce trainable action heads or separate action experts to bridge low-dimensional states and high-dimensional visual representations. In this work, we explore whether the visual backbone’s existing capacity can also support control when actions are expressed in a compatible representation. Thus, we introduce PatchWAM (Patch World-Action Model), which treats continuous actions as another type of patch through a fixed mapping called Action-as-Patch. This allows a single model to predict both how the robot should move and what the scene may look like afterward. Visual prediction and action generation become parts of the same generative process, without a dedicated action head or separate action expert. Experiments with subsampled training windows show gains over a matched dual-expert control, while benchmark evaluations reach 91.8% success rate on LIBERO-Plus and 96.12% on RoboTwin 2.0 in a full-data setting with additional augmented demonstrations. More broadly, the result suggests that capability need not be added where it can be inherited: the constraint on extending a generative backbone is the interface a new signal is written in, not the capacity to model it. 

# 1 INTRODUCTION 

Robotic actions and their visual consequences describe complementary aspects of the same interaction: actions specify the robot’s motion, while future images capture the resulting scene configuration (Ha & Schmidhuber, 2018; Kim et al., 2026; Alzayer et al., 2026). Pretrained imagegeneration and editing models provide visual priors over objects and spatial relationships, together with a trained mechanism for conditional generation of continuous latent tokens (Rombach et al., 2022; Esser et al., 2024; Black Forest Labs, 2026; Zhang et al., 2026e). Action prediction can be formulated using the same denoising objective, conditioned on the same observations and task instruction (Black et al., 2024; Zhu et al., 2025). This computational overlap motivates us to investigate whether continuous control requires a separate action expert (Black et al., 2024; Physical Intelligence et al., 2025; MotuBrain Team et al., 2026; Cai et al., 2026a; GigaWorld Team et al., 2026; Chen et al., 2026b; Wang et al., 2026e), or whether the existing visual generative pathway can be adapted to predict actions directly. A fixed action representation allows us to test this possibility without introducing a learned action-specific interface. 

We introduce PatchWAM, a Patch World-Action Model (WAM; Ye et al., 2026c; Zhang et al., 2026e; Shen et al., 2026; Wang et al., 2026b) built around _Action-as-Patch_ (AP), a fixed codec that maps each action step to a token in the visual latent space (Figure 1, left). For the action spaces considered here, the action dimension is smaller than the visual token width, allowing an information-preserving mapping through repetition and zero-padding. A fixed decoder recovers the encoded action by group 

1 


Figure 1: **Does action prediction need a dedicated DiT? Left:** PatchWAM replaces the separate action expert with fixed Action-as-Patch encoding and a shared visual DiT, so the only difference between the two panels is the removed action expert; a filled block is a parameterized network and nothing else is filled. Figure 2 gives the codec and the joint denoising in full. The left half abstracts the dual-expert control used in our comparisons rather than describing every dual-expert VLA. **Right:** success rates on five benchmarks, with the Score for RoboDojo; each spoke spans its own leaderboard range because absolute values are not comparable across benchmarks, and the number beside each spoke gives the difference between PatchWAM and the strongest listed method. Figure 4 gives the success rate of PatchWAM relative to the WAM SoTA on each benchmark, and Tables 1, 2, 4, 5, and 6 give the full comparisons. 

averaging. Action tokens therefore use the backbone’s existing visual processing path, including its learned input and output projections, without a trainable action encoder, action-specific output projection (NVIDIA et al., 2025; Pai et al., 2025; Wang et al., 2026a), or separate action expert. Throughout this paper, a _dedicated action head_ denotes a trainable action-specific prediction module beyond deterministic decoding. 

Conditioned on language, proprioception, and current images, PatchWAM jointly predicts an action chunk and a future visual endpoint. During training, action and future-image tokens are perturbed with independent Gaussian noise at a shared noise level and supervised by a joint flow-matching objective (Lipman et al., 2022). A shared diffusion transformer (DiT; Peebles & Xie, 2023) denoises both token groups, allowing interaction between visual and action predictions. At inference, the fixed decoder converts the resulting action tokens into commands for receding-horizon execution; decoding the future visual latent into RGB is unnecessary. 

We evaluate this construction against a dual-expert control under matched data and optimization settings on RoboTwin 2.0 (Chen et al., 2025a). With one retained training-window start out of every twenty, PatchWAM achieves 88.0% average success compared with 78.4% for the control, a gain of 9.6 percentage points with fewer trainable parameters (Section 4.3). The result establishes the viability of the fixed interface in this sampling regime, although the comparison does not isolate the effects of parameter sharing and attention organization. Additional evaluations characterize performance under different training and generalization protocols. PatchWAM reaches 96.12% average success on RoboTwin 2.0 with clean, randomized, and additional augmented demonstrations, and 91.8% on LIBERO-Plus (Fei et al., 2026b) with augmented training (Figure 1, right). In clean-to-random transfer (RoboTwin Team, 2026), it achieves 66.72% randomized-scene success and a 79.14% clean/random mean; the randomized score remains below the strongest listed baseline. Original LIBERO (Liu et al., 2023) and RoboDojo (Chen et al., 2026c) evaluations further characterize the model’s capabilities and limitations (Section 4.4). These benchmark comparisons involve different data regimes and are interpreted separately from the matched architecture control. Because image and action latents are updated at every denoising step, the reduction in trainable parameters does not imply lower inference latency (Section 5.1); several WAMs reduce this cost by skipping future prediction at test time or by distilling the solver (Yuan et al., 2026b; Ye et al., 2026a; Akbari et al., 2026). 

Our contributions are threefold: 

2 

- **A fixed action interface.** An information-preserving codec represents continuous actions as visual-space tokens, enabling action prediction without a dedicated trainable action head. 

- **Joint visual and action prediction.** A shared transformer predicts future-image and action tokens through a joint flow-matching objective with explicit conditioning and attention structure. 

- **Empirical evaluation.** A matched dual-expert comparison demonstrates effective control with the fixed interface, complemented by five evaluation settings covering manipulation and perturbation robustness under distinct training protocols. 

# 2 RELATED WORK 

**Vision–language–action models.** Vision–language–action (VLA) models build robot policies on top of pretrained vision–language models. Certain VLAs, such as OpenVLA, represent actions as discrete tokens (Kim et al., 2024). Most recent VLAs instead generate continuous actions through an additional module, either a learned action head (NVIDIA et al., 2025; Wang et al., 2026a) or a separate action expert (Black et al., 2024; Physical Intelligence et al., 2025). These models inherit semantic knowledge from vision–language pretraining, but their action-generation modules typically learn task-specific physical dynamics primarily from robot data (Pai et al., 2025). This limitation has motivated policies grounded in generative visual models. 

**World action models.** World action models (WAMs) derive robot policies from video or image generation models and predict future observations jointly with actions (Wang et al., 2026b; Shen et al., 2026; Ye et al., 2026c; Zhu et al., 2025). Numerous WAMs nonetheless retain a separate pathway for actions, in the form of a dedicated action stream or expert (MotuBrain Team et al., 2026; Cai et al., 2026a; GigaWorld Team et al., 2026; Chen et al., 2026b). A complementary line of work reduces the cost of predicting future frames at inference. These methods either bypass future prediction at test time (Yuan et al., 2026b; Ye et al., 2026a), distill the model into fewer denoising steps (Akbari et al., 2026), or predict the future in a latent space (Luo et al., 2026a; Chen et al., 2026a). ImageWAM replaces the video model with an image editing model and therefore predicts only a single target frame (Zhang et al., 2026e). Our implementation is based on ImageWAM. OpenWAM systematically examines WAM design choices through controlled experiments (Wang et al., 2026e). Its controlled experiments suggest that effective world–action synergy benefits from dedicated action capacity, explicit world-to-action information flow, and synchronized joint denoising. Our model likewise adopts synchronized joint denoising, but we examine whether dedicated action capacity is in fact necessary. 

**Actions in the visual domain.** Several recent methods represent actions within the visual domain, allowing the generative backbone to process them directly. Action Images renders 7-DoF actions as pixel-grounded, multi-view action videos, thereby enabling the video backbone itself to serve as a policy (Zhen et al., 2026). Hydra-0 represents actions as pixel motion and employs this shared visual interface across embodiments and video backbones (Li et al., 2026c). It nevertheless relies on a trained action head to map the resulting features to executable actions. Masked Visual Actions partially reveals a trajectory in the video (Alzayer et al., 2026). The same model can thereby predict how the scene responds to an action or infer an action from a desired outcome. All three methods situate actions in pixel space. Cosmos Policy instead operates in the latent space of a video model, encoding actions as latent frames (Kim et al., 2026). Latent action models are also related, as they learn action-like representations from inter-frame changes (Chen et al., 2025b; Tharwat et al., 2025). Action-as-Patch likewise represents actions within the visual domain, but without rendering them into pixels. A parameter-free fixed mapping encodes each action step as a single latent token rather than as an entire latent frame. 

**Joint modeling across modalities.** Latent diffusion models denoise images in a compressed latent space (Rombach et al., 2022). Diffusion transformers process this latent as a sequence of patch tokens (Peebles & Xie, 2023). Flow matching is widely adopted for training such models (Lipman et al., 2022), and recent models further process text and image tokens within a single sequence (Esser et al., 2024). Our backbone, FLUX.2 [klein], belongs to this family (Black Forest Labs, 2026). More broadly, unified multimodal models show that a single model can jointly model multiple modalities once they are represented as tokens. BAGEL and Emu3.5 are pretrained on interleaved text, image, 

3 

and video tokens (Deng et al., 2025; Cui et al., 2025). Cosmos 3 further incorporates action, processing it together with language, image, video, and audio within a single mixture-of-transformers (NVIDIA et al., 2026). Action-as-Patch exploits the same property within a pretrained image backbone. Because Action-as-Patch represents actions in the backbone’s native token format, our method requires neither a learned action tokenizer nor a dedicated action expert. When multiple modalities are denoised jointly, they need not share a noise level. Diffusion Forcing assigns each token an independent noise level (Chen et al., 2024), and several WAMs employ distinct timesteps or schedules for video and action (Zhu et al., 2025; Guo et al., 2026; Akbari et al., 2026). We instead adopt a single noise level for action and future-image tokens. 

# 3 METHOD 

As discussed in Section 2, many world action models retain a separate pathway for actions. The approaches most closely related to ours represent actions within the visual domain, either in pixel space or as entire latent frames. PatchWAM instead encodes each action step as a single token in the native token format of the backbone, so that action prediction becomes token prediction within the existing visual path (Figure 2). The conditioning prefix combines language features, a projected robot-state token, and the encoded current observation. During training, the future frame and the action chunk are encoded separately and perturbed with independent Gaussian noise at a shared noise level. Neither ground-truth target is provided at inference time; instead, both token groups are initialized from Gaussian noise and jointly denoised. A fixed decoder then recovers the action chunk, which the robot executes before the policy replans. The model predicts a single future frame rather than a full video, and the actions are obtained without decoding the future-frame latent into RGB. 

Section 3.1 formulates the problem and describes the tokenization and the model, and Section 3.2 defines the fixed codec. Section 3.3 presents the training objective, Section 3.4 describes the token sequence and attention mask, and Section 3.5 details the inference procedure. 

## 3.1 PROBLEM SETUP 

We formulate language-conditioned robotic manipulation as the prediction of action chunks. At each time step _t_ , the policy is conditioned on a language instruction _ℓ_ , a multi-camera observation _ot_ , and a proprioceptive state _st_ . It predicts an action chunk of horizon _H_ , 


where _A_ denotes the action dimensionality of the robot. We set _H_ = 16 in all experiments. A world action model additionally predicts the future state of the environment (Wang et al., 2026b). In PatchWAM, this future state is represented by the observation at the end of the chunk, _o_<sup>+</sup> = _ot_ + _H_ , and the model learns the joint conditional distribution 


The ground-truth future frame is used only as a training target. At inference time, the future frame and the action chunk are generated jointly, and only the actions are executed. The subscript _t_ is omitted hereafter when unambiguous. 

**Tokenization.** On RoboTwin and LIBERO, the camera views are composed into a single image; on RoboDojo, each view is encoded separately. A frozen image autoencoder _V_ converts each input image into a sequence of latent patch tokens, 


where _S_ denotes the number of tokens and _D_ = 128 denotes the token dimension. The instruction is embedded by a text encoder _T_ as _hℓ_ = _T_ ( _ℓ_ ), and the proprioceptive state is mapped to a single token _hs_ = _Ws s_ by a trainable linear projection. Together, these embeddings form the conditioning prefix 


The normalized action chunk is encoded into _H_ tokens of the same dimension, one per step, by the fixed codec described in Section 3.2, yielding _u_ 0 _∈_ R<sup>_H×D_</sup> . Accordingly, the distribution in Eq. (2) is modeled in token space as _pθ_ ( _x_ 0 _, u_ 0 _| c_ ). 

4 


Figure 2: **Architecture of PatchWAM. (a)** Language, robot state, and the current observation form a clean conditioning prefix. During training, the future frame and the action chunk are encoded and perturbed with independent noise at a shared noise level _σ_ , and one shared visual DiT predicts the velocities of both groups. **(b)** Action-as-Patch encodes each action step as one token by repeating every component _r_ = _⌊D/A⌋_ times and padding with zeros, and decodes a token by averaging the copies of each component; the codec has no parameters. **(c)** At inference, both token groups start from pure noise and are denoised together along one schedule. Future-frame and action tokens attend to each other and to the prefix, while the prefix does not attend to the noisy block. Token counts and camera views are schematic, and the additions on RoboDojo are not drawn (Section 3.1). 

**Model.** A single transformer jointly denoises the future-frame tokens and the action tokens. Given the noisy tokens _xσ_ and _uσ_ at a shared noise level _σ_ , it predicts a velocity for each token group: 


The trainable parameters _θ_ comprise the transformer weights and _Ws_ , together with the LoRA adapters used on RoboDojo. The image autoencoder and the base weights of the text encoder remain frozen, and the codec is parameter-free. The model in Eq. (5) thus contains no action-specific network, and the gradients of the action loss reach the same transformer that denoises the future frame. The transformer is initialized from FLUX.2 [klein] 4B Base (Black Forest Labs, 2026), and the implementation is based on the ImageWAM codebase (Zhang et al., 2026e). On RoboTwin and LIBERO, _T_ is instantiated with Qwen3-4B (Yang et al., 2025). On RoboDojo, _T_ is Qwen3-VL4B-Instruct (Bai et al., 2025) with trainable LoRA adapters (Hu et al., 2022). It jointly encodes the instruction, the current head-camera image, and past head-camera frames, and it learns to predict the current subtask as an auxiliary target. On RoboDojo, the prefix of the transformer also contains latent tokens of past head-camera frames (Section 4.1 and Appendix F). 

## 3.2 ACTION-AS-PATCH 

Action-as-Patch maps each action step onto a token whose dimensionality matches that of a visual latent patch, so that actions are presented to the transformer in the same form as image patches. A fixed encoder–decoder pair implements the mapping on normalized actions. 

5 

**Normalization.** Because action dimensions are expressed in heterogeneous physical units, each dimension is first normalized by a dataset-specific transform, _a_ ¯ = _N_ ( _a_ ). Z-score normalization is adopted for RoboTwin and RoboDojo, and min–max normalization for LIBERO (Section 4.1). The codec operates only on normalized values, and the inverse transform _N_<sup>_−_1</sup> is applied after decoding. 

**Encoder.** Let _r_ = _⌊D/A⌋_ denote the replication factor and _α >_ 0 a fixed scaling constant. For each step _h_ , the encoder replicates every action component _r_ times and zero-pads the remaining _D − rA_ entries: 


Equivalently, the encoder can be written as _E_ (¯ _ah_ ) = _αP a_ ¯ _h_ , with the fixed binary matrix 


where _⊗_ denotes the Kronecker product. The encoder is therefore linear, parameter-free, and identical across all steps. Applying the encoder to each of the _H_ steps of a chunk yields the action tokens introduced in Section 3.1, _u_ 0 = � _E_ (¯ _a_ 1)<sup>_⊤_</sup> ; _. . ._ ; _E_ (¯ _aH_ )<sup>_⊤_�</sup> _∈_ R<sup>_H×D_</sup> . The replication factor is _r_ = 9 for the 14-dimensional RoboTwin and RoboDojo actions and _r_ = 18 for the 7-dimensional LIBERO actions; in both cases, 126 entries carry action values and the remaining two are zero-padded. The scaling constant is set to _α_ = 1 throughout. 

**Decoder.** The decoder recovers each component by averaging its group of copies: 


Because _P_<sup>_⊤_</sup> _P_ = _rIA_ , this readout coincides with the Moore–Penrose pseudoinverse of the encoder, _DE_ ( _uh_ ) = ( _αP_ )<sup>+</sup> _uh_ . This identity yields two properties. First, the decoder is an exact left inverse of the encoder, _DE_ ( _E_ (¯ _ah_ )) = _a_ ¯ _h_ up to floating-point error, and the codec therefore requires no reconstruction loss. Second, for a predicted token _u_ ˆ _h_ lying outside the range of _E_ , the decoder returns the action whose encoding is nearest in the least-squares sense: 


The readout is thus an orthogonal projection onto the range of the encoder followed by exact inversion, not a learned prediction head. Actions are never passed through the image autoencoder or quantized into a discrete vocabulary. 

**Actions as patches.** An action token shares the dimensionality _D_ of a visual latent patch. It is therefore processed by the same learned input and output projections as a visual patch, and no tokentype embedding is added. The two token groups are distinguished structurally by their positional coordinates and sequence locations (Section 3.4); they also enter separate loss terms (Section 3.3). Replication further distributes each component across _r_ entries. Since the entries of the action noise _ϵu_ (Section 3.3) are independent standard Gaussian variables, the mean of the _r_ noisy copies of a component at noise level _σ_ has a noise variance of _σ_<sup>2</sup> _/r_ . This redundancy therefore raises the signal-to-noise ratio of each component in the noisy input by a factor of _r_ relative to a single copy. The same reasoning does not extend to the output: because the predicted copies of a component are not independent, averaging them does not necessarily reduce the prediction error by a fixed factor. 

**Comparison designs.** The fixed codec occupies one end of a spectrum of designs. At the other end, the dual-expert control augments the same backbone with a separate action expert (Figure 1, left); other factors changed by this comparison are discussed in Section 4.3. An intermediate learned-linear control replaces _E_ and _DE_ with trainable linear maps while holding the shared transformer, training data, and optimization budget fixed (Section 5.2). The first comparison tests whether a full action expert is necessary, and the second whether even a lightweight learned mapping is required. 

6 

## 3.3 TRAINING OBJECTIVE 

Training starts from the clean future-frame tokens _x_ 0 and action tokens _u_ 0 of Section 3.1. For each training sample, we draw a single noise level _σ_ and two independent standard Gaussian tensors _ϵx_ and _ϵu_ : 


The two groups thus share the noise level but not the noise realization. The noise level is obtained by shifting a uniform variable, 


with _s_ = 5, following the schedule shift introduced for rectified-flow transformers (Esser et al., 2024). Since _ϕs_ ( _τ_ ) _≥ τ_ for _s >_ 1, the shift concentrates training on high noise levels: only one sixth of the sampled noise levels fall below _σ_ =<sup><u>1</u></sup> 2<sup>.The transformer of Eq. (5) receives the prefix</sup> followed by the noisy tokens [ _xσ_ ; _uσ_ ] and predicts _vθ_<sup>_x_and</sup><sup>_v_</sup> _θ_<sup>_u_, whose targets are</sup><sup>_ϵx −x_0 and</sup><sup>_ϵu −u_0.</sup> The objective is 


where _λx_ = 0 _._ 5 and _λu_ = 1 _._ 0 weight the two modalities, and _w_ ( _σ_ ) weights the noise level, 


This weight peaks at _σ_ = <u>12</u><sup>andvanishesat</sup><sup>_σ_=0and</sup><sup>_σ_=1,andtheconstant</sup><sup>_Z_normalizes</sup> its expectation under Eq. (11) to one. The shift thus sets how often each noise level is sampled, and the weight sets how much each sample contributes to the loss. Each term is averaged over the tokens of its group before the weighted sum, so that _λx_ and _λu_ , rather than the token counts, set the relative weight of the two terms. The action term, MSEvalid, averages only over the action steps that lie within the demonstration and excludes the padded steps of chunks that extend past its end. The two zero-padded entries of each action token are retained in the regression and discarded only at decoding. On RoboDojo, the cross-entropy loss of the subtask prediction is added to _L_ (Appendix F). 

## 3.4 TOKEN SEQUENCE AND ATTENTION 

The input sequence begins with the clean conditioning prefix _c_ defined in Eq. (4). The prefix is followed by the noisy joint block, in which the future-frame tokens _xσ_ precede the action tokens _uσ_ . Prefix tokens attend only to prefix tokens. Future-frame and action tokens attend to the prefix and to all tokens of the noisy block. The token sequence and the attention mask for a RoboTwin sample are shown in Figure 8 of Appendix E. 

Each token carries a positional coordinate with four axes, and these coordinates distinguish the token groups. On the first axis, current-frame, future-frame, and action tokens take the values 10, 0, and 20, respectively; image tokens carry their row and column on the second and third axes, and text and action tokens carry their sequence and step indices on the fourth. The values 10, 0, and 20 only separate the groups and do not represent physical time. On RoboDojo, the additional camera views and the past frames take further values on the first axis (Appendix F). 

## 3.5 INFERENCE 

At inference time, the model encodes the current observation and initializes the joint latent _z_ 0 = [ _x_ 1; _u_ 1] with standard Gaussian noise, which corresponds to _σ_ 0 = 1. It then integrates the predicted velocity with the Euler method along the decreasing schedule _σk_ = _ϕs_ (1 _− k/K_ ), _k_ = 0 _, . . . , K_ , which uses the same shift as in training: 


The default is _K_ = 20 solver steps; all evaluations in this paper use _K_ = 10 (Section 4.1). The final action tokens are decoded with Eq. (8) and mapped back to physical units with _N_<sup>_−_1</sup> . The 

7 

robot executes the chunk, or its first part, after which the policy replans from the new observation (Appendix F). The future-frame latent need not be decoded into RGB. 

Each solver step updates the future-frame and action tokens jointly. A dual-expert model, by contrast, can compute the keys and values of its visual transformer once and then denoise only the actions; Section 5.1 discusses the resulting difference in inference cost. The architecture permits information exchange between the two groups during denoising. Section 5.2 tests whether the trained model uses this exchange with the isolated-attention control, which blocks attention between the two groups. 

# 4 EXPERIMENTS 

We first describe the experimental setup (Section 4.1) and then present the main results on RoboTwin 2.0 (Section 4.2). Section 4.3 compares PatchWAM with a dual-expert control under matched training conditions, and Section 4.4 reports results on additional benchmarks. 

## 4.1 EXPERIMENTAL SETUP 

**Benchmarks and training data.** RoboTwin 2.0 (Chen et al., 2025a) contains 50 bimanual manipulation tasks, each evaluated in clean and randomized scenes. We use two training protocols on this benchmark. In the full-data protocol, training uses 50 clean and 500 randomized demonstrations per task, and the strongest PatchWAM configuration adds 2,100 augmented demonstrations for seven tasks with low success rates. This protocol includes randomized demonstrations and therefore does not measure generalization from clean to randomized scenes. It also differs from the fixed-data leaderboard protocol, which uses 50 clean demonstrations per task (RoboTwin Team, 2026). In the clean-to-random (C2R) protocol, training uses only these 50 clean demonstrations per task, as on the leaderboard, and the success rate in randomized scenes is the main measure of generalization. The best C2R configuration applies photometric, AdaIN, and FFT-based augmentation, and we report its checkpoint after 140k updates. Online augmentation of clean demonstrations is not equivalent to training on additional randomized demonstrations. LIBERO (Liu et al., 2023) comprises four suites of ten tasks each. LIBERO-Plus (Fei et al., 2026b) perturbs these tasks, and we report its success rates separately for training on the original LIBERO data and for training on augmented LIBEROPlus data. RoboDojo (Chen et al., 2026c) spans 42 simulated tasks and five capability dimensions. Its generalization dimension is evaluated under standard and randomized conditions. We evaluate PatchWAM on all tasks and conditions of the benchmark. 

**Matched dual-expert control.** The dual-expert control adds a separate action expert with 0.64B trainable parameters to the same backbone (Section 3.2 and Appendix F). PatchWAM and the control are trained on the clean and randomized demonstrations of the full-data protocol, without the augmented demonstrations, and share all optimization settings. Both runs retain one of every 20 possible training-window start positions, which reduces the number of training windows rather than the number of demonstrations. 

**Implementation.** For RoboTwin, the three camera views are composed into a 288 _×_ 256 image, and both actions and proprioceptive states are 14-dimensional. For LIBERO, two camera views are composed horizontally into a 224 _×_ 448 image, actions are 7-dimensional, and proprioceptive states are 8-dimensional. For RoboDojo, the three camera views remain separate 256 _×_ 256 images, and both actions and proprioceptive states are 14-dimensional. On RoboDojo, the prefix also includes up to 20 past head-camera frames at one-second intervals, and the LoRA adapters of the text encoder add 132.1M trainable parameters. Actions are z-score normalized on RoboTwin and RoboDojo and min–max normalized on LIBERO. The global batch size is 256, except that it is 128 for LIBERO and 64 for the matched comparison. Appendix F lists further run-specific settings. 

**Evaluation protocol.** Success rates (SR) are reported in percent. On RoboTwin 2.0, the full-data and C2R evaluations run 100 episodes per task and scene condition, or 10,000 episodes in total. Both runs of the matched comparison are evaluated with 10 episodes per task and scene condition, or 1,000 episodes per checkpoint. RoboDojo results also include the Score, the metric by which the leaderboard ranks its entries (RoboDojo Team, 2026). All evaluations use _K_ = 10 solver 

8 

steps instead of the default _K_ = 20 (Section 3.5). Each result of PatchWAM comes from a single evaluation run, so no standard deviations are reported. The baselines differ in demonstration counts, augmentation, and checkpoint selection, so benchmark comparisons do not isolate the effect of the architecture. Section 4.3 examines this effect under matched training conditions. 

## 4.2 MAIN RESULTS ON ROBOTWIN 2.0 

RoboTwin 2.0 is the primary benchmark in our evaluation. Tables 1 and 2 compare PatchWAM with prior methods under the two training protocols of Section 4.1, and the C2R baselines are taken from the official leaderboard (RoboTwin Team, 2026). 

**Full-data protocol.** Under the full-data protocol, PatchWAM achieves 96.04% success in clean scenes and 96.20% in randomized scenes after 110k updates, for an average of 96.12% (Table 1). Both success rates are the highest among the listed methods, and the two scene conditions differ by only 0.16 percentage points. The strongest listed baseline, MotuBrain, reaches an average of 95.94%, 0.18 percentage points below PatchWAM. ImageWAM reaches 93.38%; it uses an imageediting backbone with a separate action expert and provides the codebase on which PatchWAM is built. The compared methods are not matched in training data, and the PatchWAM configuration includes 2,100 augmented demonstrations, so these differences do not isolate the effect of the architecture. Section 4.3 examines this effect under matched conditions. Appendix B traces the success rate over a full-data training run without the augmented demonstrations. 

**Clean-to-random generalization.** Under the C2R protocol, PatchWAM achieves 66.72% success in randomized scenes and 91.56% in clean scenes, for an average of 79.14% (Table 2). This average is the highest among the listed methods, while the randomized-scene success rate remains below the strongest listed result of 67.90%. Only GigaBrain-0.7 and OLA-Sem succeed more often in randomized scenes, by 1.18 and 0.84 percentage points, whereas PatchWAM exceeds their cleanscene success rates by 24.76 and 16.44 points. The WAM SoTA under this protocol, 4D-WAM, reaches 41.80% in randomized scenes. The drop from clean to randomized scenes is 24.84 percentage points for PatchWAM, whereas 4D-WAM, X-WAM, FastWAM, and AHA-WAM lose between 39.70 and 75.90 points. Under the full-data protocol, which includes randomized demonstrations, the two scene conditions differ by only 0.16 percentage points. This contrast is consistent with the hypothesis that the C2R drop arises mainly from the absence of randomized demonstrations in training. Because the C2R configuration applies photometric, AdaIN, and FFT-based augmentation, the smaller drop of PatchWAM relative to the other listed WAMs cannot be attributed to the architecture alone. Appendix C breaks these results down by task, and Appendix D shows example rollouts. 

## 4.3 DOES ACTION PREDICTION NEED A DEDICATED PATH? 

The matched comparison tests whether a policy remains effective when the dedicated action expert is removed and actions are represented directly as tokens of the visual backbone. After 41,940 updates under matched training data and optimization, PatchWAM reaches an average success rate of 88.0%, compared with 78.4% for the dual-expert control (Table 3). The comparison shows that, in this setting, a dedicated action expert is not needed for a high success rate. However, the two models also differ in token interaction and parameterization, so the gain cannot be attributed to a single factor. The comparison is limited to this window-sampling regime and does not imply a twenty-fold reduction in demonstration collection. 

**Learning speed.** Intermediate checkpoints of the same two runs show that PatchWAM also learns faster (Figure 3). Before training, the dual-expert control already succeeds in 8.7% of the episodes and PatchWAM in 0.6%. Nine tasks have success conditions that can be triggered by a single contact or a short motion: pressing the stapler, clicking the alarm clock and the bell, turning the switch, opening the microwave and the laptop, moving the playing card away, and the two bottle-shaking tasks. These tasks account for 7.8 of the 8.7 percentage points, because the untrained action expert occasionally satisfies their success conditions by chance. After 20k updates, PatchWAM reaches 60.7%, whereas the dual-expert control needs 30k updates to reach a comparable 60.4%. After 30k updates, PatchWAM reaches 81.0% and thus exceeds the final success rate of the control, 78.4% after 41,940 updates. The difference is largest at 20k updates, where it amounts to 37.9 percentage 

9 

Table 1: **RoboTwin 2.0 success rate (%) under the full-data protocol:** training on clean and randomized demonstrations and evaluation in clean and randomized scenes. Best in **bold** ; secondbest underlined. 

|**Method**|**Clean**|**Randomized**|**Average**|
|---|---|---|---|
|**VLA**||||
|ZR-0 (Li et al.,2026b)|88.70|87.98|88.34|
|HoloBrain-0 (Lin et al.,2026)|91.30|90.80|91.05|
|HoloBrain-0-QW (Lin et al.,2026)|91.90|92.30|92.10|
|LingBot-VA (Li et al.,2026d)|92.93|91.55|92.24|
|AIM (Fan et al.,2026)|94.00|92.10|93.05|
|G0.5 (Liu et al.,2026)|93.70|92.80|93.25|
|LingBot-VA 2.0 (Zhang et al.,2026c)|93.80|93.40|93.60|
|<br>Next Forcing (Xu et al.,2026)|**94.10**|93.50|93.80|
|Qwen-RobotManip (Yuan et al.,2026a)|93.70|**94.00**|**93.85**|
|**WAM**||||
|X-WAM (Guo et al.,2026)|89.80|90.70|90.25|
|LaWAM (Chen et al.,2026a)|92.64|89.80|91.22|
|Faster-WAM (Zhao et al.,2026b)|92.80|92.30|92.55|
|SelfWAM (Pan et al.,2026)|92.16|93.08|92.62|
|MECo-WAM (Zhang et al.,2026b)|93.26|91.98|92.62|
|ImageWAM (Zhang et al.,2026e)|93.20|93.56|93.38|
|ABot-M0.5 (Chen et al.,2026b)|94.00|94.20|94.10|
|MotuBrain (MotuBrain Team et al.,2026)|95.80|96.08|95.94|
|**PatchWAM (Ours)**|**96.04**|**96.20**|**96.12**|


Table 2: **RoboTwin 2.0 success rate (%) under the clean-to-random protocol:** training on clean demonstrations only and evaluation in clean and randomized scenes. Best in **bold** ; second-best <u>underlined.</u> 

|**Method**|**Clean**|**Randomized**|**Average**|
|---|---|---|---|
|**VLA**||||
|StarVLA (StarVLA Community,2026)|46.52|3.16|24.84|
|GalaxeaVLA (Jiang et al.,2025)|62.70|12.72|37.71|
|Xiaomi Robotics-0 (Cai et al.,2026b)|62.90|18.20|40.55|
|EventVLA (Yang et al.,2026a)|65.60|15.70|40.65|
|Spatial Forcing (Li et al.,2026a)|77.20|26.74|51.97|
|OLA-Geo (RoboTwin Team,2026)|**82.96**|33.64|58.30|
|_π_0_._5 (Physical Intelligence et al.,2025)|70.70|46.00|58.35|
|GigaBrain-0.7 (GigaBrain Team et al.,2026)|66.80|**67.90**|67.35|
|OLA-Sem (RoboTwin Team,2026)|75.12|67.56|**71.34**|
|**WAM**||||
|AHA-WAM (Cai et al.,2026a)|64.30|3.20|33.75|
|FastWAM (Yuan et al.,2026b)|77.80|1.90|39.85|
|ABot-M0 (Yang et al.,2026c)|57.40|30.36|43.88|
|X-WAM (Guo et al.,2026)|70.00|25.80|47.90|
|4D-WAM (Yang et al.,2026b)|81.50|41.80|61.65|
|**PatchWAM (Ours)**|**91.56**|**66.72**|**79.14**|


points, and narrows to 9.6 points by the end of training. Because both runs use the same data and batch size, fewer updates correspond directly to fewer training samples. Each curve comes from a single run evaluated with 10 episodes per task and condition, so differences between individual checkpoints are subject to sampling error. 

10 

Table 3: **Effect of a dedicated action expert on RoboTwin 2.0.** Success rates (percent) of the matched comparison after 41,940 updates, with one of every 20 window starts retained and 10 episodes per task and condition. 

|**Action expert**|**Clean**|**Randomized**|**Average**|
|---|---|---|---|
|✓|77.2|79.6|78.4|
|✗|**87.6**|**88.4**|**88.0**|
|∆|+10.4|+8.8|+9.6|


Figure 3: Learning curves of the matched comparison on RoboTwin 2.0. **(a)** Average success rate of PatchWAM and the dual-expert control at intermediate checkpoints of the two runs; the first point of each curve is the evaluation before training. **(b)** Difference between the two success rates (PatchWAM minus control). 

## 4.4 ADDITIONAL BENCHMARKS 

Figure 4 compares PatchWAM with the WAM state of the art (WAM SoTA) on each of the five settings. Tables 4, 5, and 6 list the full comparisons on LIBERO, LIBERO-Plus, and RoboDojo, with RoboDojo baselines taken from the official leaderboard (RoboDojo Team, 2026). 


Figure 4: Success rate of PatchWAM relative to the WAM SoTA on five benchmark settings (relative score on RoboDojo). The WAM SoTA is MotuBrain on RoboTwin full-data, 4D-WAM on RoboTwin C2R, ABot-M0.5 on LIBERO, ImageWAM on LIBERO-Plus, and OpenWAM- _α_ on RoboDojo. 

**LIBERO.** On LIBERO, PatchWAM achieves an average success rate of 98.4%, whereas the strongest listed baseline, QuoVLA, reaches 99.6% (Table 4). Across the four suites, PatchWAM reaches 96.5% on Spatial, 100.0% on Object, 99.0% on Goal, and 98.0% on Long. Long is the weakest suite for 13 of the 14 listed methods, whereas PatchWAM succeeds more often on Long than on Spatial. Only three listed methods exceed its 98.0% on Long. On Object, PatchWAM 

11 

matches the best listed result of 100.0%. Its average is limited mainly by the Spatial suite, on which 11 listed methods succeed more often. Because three listed methods already exceed 99% on average, the benchmark appears close to saturation, and the remaining differences are small. Appendix A reports results on LIBERO-Pro. 

Table 4: **LIBERO success rate (%) on the four task suites.** Best in **bold** . 

|**Method**<br>**Spatial**|**Object**|**Goal**|**Long**|**Average**|
|---|---|---|---|---|
|**VLA**|||||
|OpenVLA (Kim et al.,2024)<br>84.7|88.4|79.2|53.7|76.5|
|WorldVLA (Cen et al.,2025)<br>87.6|96.2|83.4|60.0|81.8|
|UniVLA (Wang et al.,2026d)<br>95.4|98.8|93.6|94.0|95.4|
|F1-VLA (Lv et al.,2025)<br>98.2|97.8|95.4|91.3|95.7|
|OpenVLA-OFT (Kim et al.,2025)<br>97.6|98.4|97.9|94.5|97.1|
|TurboVLA (Xie et al.,2026a)<br>99.2|99.8|97.4|94.2|97.6|
|StarVLA-_α_(Specialist) (Ye et al.,2026b)<br>98.7|99.7|98.6|94.2|97.8|
|X-VLA (Zheng et al.,2026)<br>98.2<br>|98.6|97.8|97.6|98.1|
|S<sup>2</sup>-VLA (Xie et al.,2026b)<br>98.4|99.6|98.4|96.4|98.2|
|FocusVLA (Zhang et al.,2026d)<br>99.6|**100.0**|98.8|96.2|98.6|
|GeoAlign (Chen et al.,2026d)<br>**100.0**|99.6|99.8|96.6|99.0|
|CORAL (SimVLA) (Luo et al.,2026c;d)<br>99.6|99.8|99.0|**98.8**|99.3|
|QuoVLA (Wang et al.,2026c)<br>99.8|99.9|**100.0**|98.7|**99.6**|
|**WAM**|||||
|ABot-M0.5 (Chen et al.,2026b)<br>**100.0**|99.8|**99.4**|**98.4**|**99.4**|
|PatchWAM (Ours)<br>96.5|**100.0**|99.0|98.0|98.4|


**LIBERO-Plus.** On LIBERO-Plus, training on the original LIBERO data yields a total success rate of 80.2%, and training on augmented LIBERO-Plus data raises it to 91.8% after 75k updates; Table 5 lists the second result. The latter result reflects training on perturbed data rather than zeroshot robustness. This total is the highest among the listed methods, 0.41 percentage points above Hermite-VLAReg, and PatchWAM also achieves the highest success rates under camera and sensornoise perturbations, at 97.9% each. ImageWAM, which uses a 9B FLUX.2 backbone instead of the 4B backbone of PatchWAM, reaches 85.3%. The largest differences from ImageWAM arise under camera and robot initial-state perturbations, at 18.1 and 12.3 percentage points, while ImageWAM succeeds more often under language perturbations, at 95.2% compared with 89.1%. The weakest category of PatchWAM is robot initial-state perturbation, at 71.0%; four listed methods succeed more often in this category, led by the zero-shot QuoVLA result of 87.6%. These results indicate that robustness to visual perturbations does not necessarily carry over to variations in the initial robot state. 

12 

Table 5: **LIBERO-Plus success rate by perturbation category.** Best in **bold** and second-best <u>underlined</u> within each group. 

|**Method**|**Camera**|**Robot**|**Language**|**Light**|**Background**|**Noise**|**Layout**|**Total**|
|---|---|---|---|---|---|---|---|---|
|||**VLA**|||||||
|_π_0 (Black et al.,2024)|79.6|21.1|72.5|84.7|86.2|68.3|69.4|68.8|
|OpenVLA*-Full (Kim et al.,2024)|69.4|49.6|66.3|88.2|88.5|78.7|70.3|73.0|
|_π_0_._5 (Physical Intelligence et al.,2025)|70.3|41.7|81.1|97.3|94.6|71.8|84.9|77.4|
|<br>InternVL-3.5 + DiT (Wang et al.,2025)|94.2|32.4|64.5|94.7|93.0|94.7|74.8|78.3|
|ELAN4D (_π_0_._5) (He et al.,2026)|63.7|70.7|77.8|89.8|91.4|79.9|81.4|79.2|
|GR00T-N1.6 (NVIDIA GEAR Team et al.,2025)|92.6|33.5|80.1|93.6|95.4|93.6|75.0|80.5|
|OpenVLA-OFT+ (Kim et al.,2025)|92.8|30.3|85.8|94.9|93.9|89.3|77.6|80.7|
|<br>SRPO (Fei et al.,2026a)|83.4|62.0|73.6|97.2|97.7|85.7|75.2|82.1|
|RoVLA (Luo et al.,2026b)|**96.6**|32.0|**91.5**|95.9|96.1|95.1|74.1|83.0|
|_π_0_._5 + AXIS (Zhao et al.,2026a)|83.8|78.2|88.3|96.5|98.1|96.2|85.5|89.5|
|CAC-VLA (Xiong et al.,2026)|91.2|78.4|83.3|97.5|97.1|95.4|87.8|90.1|
|QuoVLA (Wang et al.,2026c)|82.3|**87.6**|88.2|98.2|95.9|90.8|89.3|90.3|
|Anchor-Align VLA (Dalal et al.,2026)|96.3|59.1|87.2|**99.0**|**99.6**|**96.9**|**97.4**|90.8|
|<br>Hermite-VLAReg (Lv et al.,2026)|89.2|85.4|87.3|97.7|96.7|93.8|89.9|**91.4**|
|||**WAM**|||||||
|Fast-WAM (Yuan et al.,2026b)|16.4|44.5|68.9|78.2|53.7|37.7|60.7|50.0|
|Being-H0.7 (Luo et al.,2026a)|-|-|-|-|-|-|-|82.1|
|<br>Cosmos-Policy (Kim et al.,2026)|75.8|63.3|81.7|96.5|88.9|92.7|82.2|82.2|
|<br>ImageWAM (Zhang et al.,2026e)|79.8|58.7|**95.2**|96.1|91.2|93.3|83.1|85.3|
|ABot-M0.5 (Chen et al.,2026b)|70.5|**87.4**|88.6|94.0|89.7|75.5|85.2|83.4|
|**PatchWAM**|**97.9**|71.0|89.1|**98.5**|**96.9**|**97.9**|**92.3**|**91.8**|


**RoboDojo.** On RoboDojo, PatchWAM obtains a Score of 29.39 and an average success rate of 23.60% (Table 6). The Score assigns 100 points to a successful episode and partial credit to an unsuccessful episode according to the intermediate steps completed. Both the Score and the success rate are averaged over the tasks of each capability dimension and then over the five dimensions with equal weight, so the standard and randomized conditions of the generalization dimension each contribute one tenth (Chen et al., 2026c). Both are the highest among the entries of the leaderboard on September 15, 2026; the next entry, DM0.5, has a Score of 24.90 and a success rate of 19.34%.<sup>1</sup> The WAM SoTA on the leaderboard, OpenWAM- _α_ , has a Score of 17.18. Performance varies strongly across capability dimensions. PatchWAM reaches the highest success rate among the listed methods under both generalization conditions, on precise manipulation, and in open-vocabulary instruction following. Under the standard and randomized generalization conditions, it succeeds in 33.33% and 16.33% of the episodes, compared with at most 28.00% and 6.00% for the other listed methods. It reaches 23.00% on precise manipulation, compared with at most 20.42%, and 22.00% in open-vocabulary instruction following, compared with at most 4.25%. On long-horizon tasks, it reaches 31.50%, below the 32.25% of G0.5, and on memory tasks it reaches 16.67%, compared with 47.44% for DM0.5. 

# 5 ANALYSIS 

## 5.1 INFERENCE COST 

Sharing the transformer between the future frame and the actions makes inference slower. We time one call that maps an observation to a chunk of 16 actions with 20 solver steps, using the same GPU and input for both models, and average ten runs after two warm-up runs. PatchWAM takes 0.446 s per call, 1.87 times the 0.239 s of the dual-expert control. Both models use the same text encoder and image autoencoder, so the difference arises in the transformer. 

The dual-expert control runs its visual transformer once, on the instruction and the current frame with the noise level set to zero, and stores the resulting keys and values. Each of the 20 solver steps then updates only the 16 action tokens in its smaller action expert. PatchWAM instead passes the full sequence of 721 tokens (Appendix E) through the 4B transformer at every solver step. The 

1As of September 22, 2026, two entries added to the leaderboard after September 15 exceed at least one of these values: Liber-0 Preview has a Score of 30.74 and a success rate of 25.52%, and Liber-0 Lite has a success rate of 24.23% at a Score of 29.24. 

13 

Table 6: **RoboDojo simulation results across capability dimensions** , with the score and the success rate (SR, percent) of each dimension. 

||**Gen-**|**Std**|**Gen-**|**Rand**|**Prec**|**ision**|**Lo**|**ng**|**Mem**|**ory**|**Op**|**en**|**Aver**|**age**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|Score|SR|Score|SR|Score|SR|Score|SR|Score|SR|Score|SR|Score|SR|
||||**V**|**LA**|||||||||||
|StarVLA-PI_v3 (StarVLA Community,2026)|19.08|14.44|3.36|1.67|17.77|12.50|18.46|11.00|4.59|4.00|2.03|2.00|10.81|7.51|
|InternVLA-A1.5 (Ma et al.,2026)|16.81|11.78|3.90|1.89|15.23|10.17|23.80|13.75|4.93|3.56|1.43|1.42|11.15|7.14|
|_π_0_._5 (Physical Intelligence et al.,2025)|20.93|14.89|5.82|1.44|12.40|5.50|23.54|14.67|5.78|4.56|1.98|1.67|11.41|6.91|
|Spatial Forcing (Li et al.,2026a)|21.25|14.89|6.98|3.78|17.32|10.58|23.26|14.58|5.43|4.11|1.78|1.58|12.38|8.04|
|Hy-Embodied-0.5-VLA (Zhang et al.,2026a)|21.98|16.56|1.57|0.22|13.81|8.00|25.74|14.92|13.37|12.11|0.65|0.58|13.07|8.80|
|Meituan-Robotics-0 (RoboDojo Team,2026)|19.28|12.67|8.22|3.67|16.77|7.75|29.61|18.58|10.06|8.89|4.54|4.25|14.95|9.53|
|Xiaomi-Robotics-1 (Xiaomi Robotics Team et al.,2026)|**35.65 **|**28.00 **|**11.44**|**6.00**|26.69|18.83|38.39|23.67|7.81|6.56|3.94|3.58|20.07|13.93|
|GalaxeaVLA (G0.5) (Liu et al.,2026)|27.72|21.44|9.20|4.22|**28.25 **|**20.42 **|**44.12 **|**32.25**|8.61|7.33|1.73|1.58|20.23|14.88|
|DM0.5 (Dexmal Team,2026)|23.49|17.89|8.06|4.00|24.82|16.75|33.70|19.50|**47.74 **|**47.44**|2.43|2.08|**24.90 **|**19.34**|
||||**W**|**AM**|||||||||||
|OpenWAM-_α_(Wang et al.,2026e)|33.16|25.56|8.26|4.11|18.45|9.25|34.93|25.33|10.41|9.11|1.41|1.08|17.18|11.92|
|**PatchWAM (Ours)**|**39.08 **|**33.33 **|**22.97 **|**16.33 **|**30.96 **|**23.00 **|**43.75 **|**31.50 **|**18.48 **|**16.67 **|**22.74 **|**22.00 **|**29.39 **|**23.60**|


prefix cannot be reused across steps, because FLUX.2 modulates every token, including those of the prefix, with the current noise level. The cost of PatchWAM therefore grows much faster with the number of solver steps than that of the control, and its smaller number of trainable parameters does not make inference faster. In the RoboTwin evaluation, the policy is queried once every 16 executed actions with 10 solver steps, a setting we did not time. A model trained with its prefix conditioned on a fixed noise level could cache the prefix as the control does, and step distillation (Akbari et al., 2026) could reduce the number of solver steps; we have tested neither. 

## 5.2 MECHANISM CONTROLS 

Two controls test whether the interface must be learned and whether the noisy action and futureframe tokens need to attend to each other, and three further variants examine the shared noise level. The two controls are trained under the full-data protocol for the same 104,850 updates as the run in Appendix B and evaluated with 100 episodes per task and condition; the fixed codec reaches 94.57% in this setting. 

**Learned interface.** The dual-expert comparison removes a large action-specific path and changes token interaction at the same time. To isolate the interface, the learned-linear control replaces the fixed codec with a trainable _A → D → A_ encoder–decoder pair, initialized to reproduce the fixed mapping, while retaining the shared transformer; for the 14-dimensional RoboTwin actions, it adds 3,726 trainable parameters, including biases. It reaches 94.50% on average, 0.07 percentage points below the fixed codec; it succeeds more often in clean scenes and less often in randomized scenes (Table 7). A learned interface therefore brings no measurable gain in this setting, and we keep the fixed codec because it adds no trainable parameters and needs no initialization. 

Table 7: Fixed versus learned-linear action interfaces on RoboTwin 2.0 under the full-data protocol (SR, percent), with 100 evaluation episodes per task and condition. 

|Interface|Clean|Randomized|Average|
|---|---|---|---|
|Fixed (PatchWAM)|94.68|**94.46**|**94.57**|
|<br>Learned-linear|**95.02**|93.98|94.50|
|∆|+0_._34|_−_0_._48|_−_0_._07|


**Noisy action–image visibility.** The isolated-attention control keeps the sequence, the objective, and the codec of PatchWAM but prevents the noisy action tokens and the noisy future-frame tokens from attending to one another; each group still attends to itself and to the prefix (Appendix E). Removing this visibility reduces the average success rate by 0.58 percentage points, from 94.57% to 93.99%, with drops in both clean scenes (0.76 points) and randomized scenes (0.40 points; Table 8). The interaction between the two token groups may therefore contribute a small gain, which a single training run per model cannot establish. 

14 

Table 8: PatchWAM against the isolated-attention control on RoboTwin 2.0 under the full-data protocol (SR, percent), with 100 evaluation episodes per task and condition. 

|Method|Clean|Randomized|Average|
|---|---|---|---|
|PatchWAM|**94.68**|**94.46**|**94.57**|
|Isolated attention|93.92|94.06|93.99|
|∆|_−_0_._76|_−_0_._40|_−_0_._58|


**Decoupled noise levels.** PatchWAM applies one noise level to the future-frame and action tokens of a sample (Section 3.3). Three variants built on Self-Flow (Chefer et al., 2026) depart from this choice and are trained and evaluated in the setting of Table 3. The first adopts the dual-timestep scheduling of Self-Flow, which assigns different noise levels to different tokens, together with a representation loss from an exponential-moving-average (EMA) teacher. The second additionally structures the timestep masks by modality, and the third also withholds the action labels of 25% of the samples and replaces them with labels generated by the teacher. Their average success rates are 88.7%, 88.3%, and 85.5%, compared with 88.0% for the shared noise level (Appendix G). The first two variants succeed more often in clean scenes and less often in randomized scenes, and their averages exceed that of PatchWAM by at most 0.7 percentage points, a difference comparable to the uncertainty of a 10-episode evaluation. The third variant reduces the average by 2.5 points. Because every variant also changes the training objective, these results do not isolate the effect of the noise levels, but they give no indication that separate noise levels improve on the shared one in this setting. 

# 6 LIMITATIONS AND DISCUSSION 

**Scope of the architectural evidence.** The matched comparison shows that a separate action expert is not required in this sampling regime, but it does not establish that every dedicated action head is unnecessary. Relative to the dual-expert control, PatchWAM changes action-specific capacity, token visibility, and the processing path together. The controls of Section 5.2 separate two of these factors under the full-data protocol: a learned linear interface performs on par with the fixed codec, and removing the visibility between action and future-frame tokens costs 0.58 percentage points. Because they were run in a different data regime, they do not decompose the 9.6-point gap of the matched comparison, and no comparison in this paper includes independent training seeds. Joint denoising allows interaction between visual and action predictions, and the isolated-attention control suggests a small gain from this interaction, but neither establishes that the predicted future frame informs action selection. At the highest noise level, the future-frame tokens contain no information about the observed future, and a single future frame can be consistent with several action sequences. Additional conditioning information can reduce the squared error of an ideal predictor, although this does not imply higher closed-loop success for a trained model. Cross-modal coupling and the reuse of pretrained weights are therefore motivations for the design rather than established explanations of its performance. 

**Inference and deployment.** Because future-frame and action tokens are updated at every solver step, one inference call with 20 solver steps takes 1.87 times as long as in the dual-expert control. The 10-step setting used for evaluation was not timed. Part of this cost follows from the architecture, which passes the future-frame tokens through the full transformer at every solver step. In addition, unlike the dual-expert control, PatchWAM recomputes the conditioning prefix at every solver step, because FLUX.2 modulates the prefix with the current noise level (Section 5.1). All experiments are conducted in simulation, and the results do not establish real-time operation, performance on physical robots, or safe deployment. 

# 7 CONCLUSION 

We investigated whether continuous control requires a separate action expert, or whether the visual generative pathway of a pretrained image model can be adapted to predict actions directly. Patch- 

15 

WAM maps each action step to a token in the visual latent space through a fixed codec, and a shared transformer denoises these tokens together with the tokens of a future frame, without a trainable action encoder, an action-specific output projection, or a separate action expert. Under matched data and optimization settings on RoboTwin 2.0, with one of every 20 training-window starts retained, PatchWAM achieves 88.0% average success compared with 78.4% for the dual-expert control and reaches the final success rate of the control with fewer training updates. Across benchmarks with different data regimes, it reaches 96.12% average success on RoboTwin 2.0 with augmented demonstrations and 91.8% on LIBERO-Plus with augmented training data, and its RoboDojo Score of 29.39 is the highest among the leaderboard entries of September 15, 2026. These results show that the fixed interface works in the evaluated settings, although joint denoising makes inference slower than in the dual-expert control (Section 5.1). Two controls under the full-data protocol show that a learned linear interface does not improve on the fixed codec and that removing the visibility between action and future-frame tokens costs 0.58 percentage points. Identifying the factors behind the advantage over the dual-expert control still requires further controls in the matched setting and independent training seeds, and all results remain to be tested on physical robots. 

# ACKNOWLEDGMENTS 

We thank Awomo for providing the computing resources used for training and evaluation. 

# REPRODUCIBILITY STATEMENT 

Section 3 defines the Action-as-Patch codec, the training objective, the token sequence and attention mask, and the inference procedure, and Appendix E shows the sequence and the mask for one RoboTwin 2.0 sample. Section 4.1 describes the benchmarks, the training data of each protocol, the matched control, and the evaluation protocol. Appendix F lists the settings of the training runs: the model settings that the runs share, the global batch size and number of epochs of each run, the filtering of the training data, the image augmentation of each protocol, and the inputs and text encoder of the RoboDojo run. It also describes the architecture, initialization, and parameter count of the dual-expert control, and it gives the evaluation seeds of RoboTwin 2.0 and LIBERO, the number of LIBERO trials, and the replanning interval of each benchmark. Appendix B reports the success rates of intermediate checkpoints of one complete training run. No reported result is repeated with independent training or evaluation seeds. 

# AI USE STATEMENT 

AI assistants were used to inspect implementation files, organize experimental results, and draft and edit the text of this paper. The authors reviewed the numerical results, citations, and claims, and they take full responsibility for the content. 

# REFERENCES 

- Arman Akbari, Ci Zhang, Arash Akbari, Lin Zhao, Yixiao Chen, et al. Flash-WAM: Modality-aware distillation for world action models. _arXiv preprint arXiv:2606.05254_ , 2026. 

- Hadi Alzayer, Wenlong Huang, Haonan Chen, Christopher Luey, Lvmin Zhang, et al. Masked visual actions for unified world modeling. _arXiv preprint arXiv:2607.19343_ , 2026. 

- Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen, Xionghui Chen, et al. Qwen3-VL technical report. _arXiv preprint arXiv:2511.21631_ , 2025. 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, et al. _π_ 0: A visionlanguage-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Black Forest Labs. FLUX.2 [klein]. Official model documentation, 2026. URL https://bfl. ai/models/flux-2-klein. Accessed September 15, 2026. 

16 

- Jisong Cai, Long Ling, Shiwei Chu, Zhongshan Liu, Jiayue Kang, et al. AHA-WAM: Asynchronous horizon-adaptive world-action modeling with observation-guided context routing. _arXiv preprint arXiv:2606.09811_ , 2026a. 

- Rui Cai, Jun Guo, Xinze He, Piaopiao Jin, Jie Li, et al. Xiaomi-Robotics-0: An open-sourced visionlanguage-action model with real-time execution. _arXiv preprint arXiv:2602.12684_ , 2026b. 

- Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, et al. WorldVLA: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 

- Hila Chefer, Patrick Esser, Dominik Lorenz, Dustin Podell, Vikash Raja, Vinh Tong, Antonio Torralba, and Robin Rombach. Self-supervised flow matching for scalable multi-modal synthesis. _arXiv preprint arXiv:2603.06507_ , 2026. 

- Boyuan Chen, Diego Martí Monsó, Yilun Du, Max Simchowitz, Russ Tedrake, and Vincent Sitzmann. Diffusion forcing: Next-token prediction meets full-sequence diffusion. In _Advances in Neural Information Processing Systems_ , 2024. 

- Jialei Chen, Kai Wang, Kang Chen, Shuaihang Chen, Feng Gao, et al. LaWAM: Latent world action models for efficient dynamics-aware robot policies. _arXiv preprint arXiv:2606.15768_ , 2026a. 

- Ronghan Chen, Yandan Yang, Zuojin Tang, Dongjie Huo, Tong Lin, et al. ABot-M0.5: Unified mobility-and-manipulation world action model. _arXiv preprint arXiv:2607.00678_ , 2026b. 

- Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, et al. RoboTwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025a. 

- Tianxing Chen, Yue Chen, Zixuan Li, Junyuan Tang, Kailun Su, Weijie Wan, Baijun Chen, Haoran Lu, Haowen Yan, Honghao Su, et al. RoboDojo: A unified sim-and-real benchmark for comprehensive evaluation of generalist robot manipulation policies. _arXiv preprint arXiv:2607.04434_ , 2026c. 

- Xiaoyu Chen, Hangxing Wei, Pushi Zhang, Chuheng Zhang, Kaixin Wang, et al. villa-X: Enhancing latent action modeling in vision-language-action models. _arXiv preprint arXiv:2507.23682_ , 2025b. 

- Yizhi Chen, Zhanxiang Cao, Xinyi Peng, Yixiao Zheng, Xiaxi Si, et al. GeoAlign: Beyond semantics with state-guided spatial alignment in VLA models. _arXiv preprint arXiv:2606.03240_ , 2026d. 

- Yufeng Cui, Honghao Chen, Haoge Deng, Xu Huang, Xinghang Li, et al. Emu3.5: Native multimodal models are world learners. _arXiv preprint arXiv:2510.26583_ , 2025. 

- Dwip Dalal, Shivansh Patel, Chahit Jain, Jeonghwan Kim, Utkarsh Mishra, et al. Generalizable VLA finetuning via representation anchoring and language-action alignment. _arXiv preprint arXiv:2607.13429_ , 2026. 

- Chaorui Deng, Deyao Zhu, Kunchang Li, Chenhui Gou, Feng Li, et al. Emerging properties in unified multimodal pretraining. _arXiv preprint arXiv:2505.14683_ , 2025. 

- Dexmal Team. DM0.5: An open-world foundation model for general-purpose embodied intelligence. Official technical blog, 2026. URL https://www.dexmal.com/blog/dm0.5/ index_en.html. Accessed September 15, 2026. 

- Patrick Esser, Sumith Kulal, Andreas Blattmann, Rahim Entezari, Jonas Müller, et al. Scaling rectified flow transformers for high-resolution image synthesis. In _Proceedings of the International Conference on Machine Learning_ , 2024. 

- Liaoyuan Fan, Zetian Xu, Chen Cao, Wenyao Zhang, Mingqi Yuan, et al. AIM: Intent-aware unified world action modeling with spatial value maps. _arXiv preprint arXiv:2604.11135_ , 2026. 

17 

- Senyu Fei, Siyin Wang, Li Ji, Ao Li, Shiduo Zhang, et al. SRPO: Self-referential policy optimization for vision-language-action models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2026a. 

- Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, Jinlan Fu, Jingjing Gong, and Xipeng Qiu. LIBERO-Plus: A progressive robustness benchmark for visual-language-action models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2026b. 

- GigaBrain Team, Angen Ye, Axiang Sun, Can Jin, Chenxi Cheng, et al. GigaBrain-0.7: Scaling embodied foundation models to emergent capabilities with a three-system architecture. _arXiv preprint arXiv:2608.15875_ , 2026. 

- GigaWorld Team, Angen Ye, Angyuan Ma, Boyuan Wang, Chaojun Ni, et al. GigaWorld-Policy0.5: A faster and stronger WAM empowered by AutoResearch. _arXiv preprint arXiv:2607.13960_ , 2026. 

- Jun Guo, Qiwei Li, Peiyan Li, Zilong Chen, Nan Sun, et al. Unified 4D world action modeling from video priors with asynchronous denoising. _arXiv preprint arXiv:2604.26694_ , 2026. 

- David Ha and Jürgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2018. 

- Zeyuan He, Bowen Yang, Zhirui Fang, Keru Zhou, Lei Jiang, et al. ELAN4D: Embodiment-centric 4D supervision for vision-language-action models via plug-and-play adaptation. _arXiv preprint arXiv:2605.30484_ , 2026. 

- Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. LoRA: Low-rank adaptation of large language models. In _International Conference on Learning Representations_ , 2022. 

- Tao Jiang, Tianyuan Yuan, Yicheng Liu, Chenhao Lu, Jianning Cui, et al. Galaxea open-world dataset and G0 dual-system VLA model. _arXiv preprint arXiv:2509.00576_ , 2025. 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, et al. OpenVLA: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. In _Proceedings of Robotics: Science and Systems_ , 2025. 

- Moo Jin Kim, Yihuai Gao, Tsung-Yi Lin, Yen-Chen Lin, Yunhao Ge, et al. Cosmos Policy: Finetuning video models for visuomotor control and planning. _arXiv preprint arXiv:2601.16163_ , 2026. 

- Fuhao Li, Wenxuan Song, Han Zhao, Jingbo Wang, Pengxiang Ding, et al. Spatial Forcing: Implicit spatial representation alignment for vision-language-action model. In _International Conference on Learning Representations_ , 2026a. 

- Haoyang Li, Guanlin Li, Youhe Feng, Chen Zhao, Zhuoran Wang, et al. Training visionlanguage-action models with dense embodied chain-of-thought supervision. _arXiv preprint arXiv:2606.30552_ , 2026b. 

- Hongyu Li, Bowen Wen, Xinghao Zhu, Yixuan Wang, Yilun Du, et al. Hydra-0: Action flow for generalist world modeling and control. _arXiv preprint arXiv:2608.18077_ , 2026c. 

- Lin Li, Qihang Zhang, Yiming Luo, Shuai Yang, Ruilin Wang, et al. Causal world modeling for robot control. _arXiv preprint arXiv:2601.21998_ , 2026d. 

- Xuewu Lin, Tianwei Lin, Yun Du, Hongyu Xie, Yiwei Jin, et al. HoloBrain-0 technical report. _arXiv preprint arXiv:2602.12062_ , 2026. 

- Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

18 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. LIBERO: Benchmarking knowledge transfer for lifelong robot learning. _arXiv preprint arXiv:2306.03310_ , 2023. 

- Yicheng Liu, Zibin Dong, Baijun Ye, Tianyuan Yuan, Tao Jiang, et al. G0.5: One autoregressive stream for robot reasoning and action. _arXiv preprint arXiv:2608.11739_ , 2026. 

- Hao Luo, Wanpeng Zhang, Yicheng Feng, Sipeng Zheng, Haiweng Xu, et al. Being-H0.7: A latent world-action model from egocentric videos. _arXiv preprint arXiv:2605.00078_ , 2026a. 

- Jingzhou Luo, Yifan Wen, Yongjie Bai, Xinshuai Song, Yang Liu, et al. RoVLA: Multi-consistency constraints for robust vision-language-action models. _arXiv preprint arXiv:2605.19678_ , 2026b. 

- Yuankai Luo, Woping Chen, Tong Liang, and Zhenguo Li. CORAL: Scalable multi-task robot learning via LoRA experts. _arXiv preprint arXiv:2603.09298_ , 2026c. 

- Yuankai Luo, Woping Chen, Tong Liang, Baiqiao Wang, and Zhenguo Li. SimVLA: A simple VLA baseline for robotic manipulation. _arXiv preprint arXiv:2602.18224_ , 2026d. 

- Qi Lv, Weijie Kong, Hao Li, Jia Zeng, Zherui Qiu, et al. F1: A vision-language-action model bridging understanding and generation to actions. _arXiv preprint arXiv:2509.06951_ , 2025. 

- Qi Lv, Jianming Xing, Zhao Yang, Mingyuan Yao, Yinan Shi, et al. Hermite curves as trajectory priors for vision-language-action models. _arXiv preprint arXiv:2608.01265_ , 2026. 

- Haoxiang Ma, Junhao Cai, Xiaoxu Xu, Hao Li, Yuyin Yang, et al. InternVLA-A1.5: Unifying understanding, latent foresight, and action for compositional generalization. _arXiv preprint arXiv:2607.04988_ , 2026. 

- MotuBrain Team, Chendong Xiang, Fan Bao, Haitian Liu, Hengkai Tan, et al. MotuBrain: An advanced world action model for robot control. _arXiv preprint arXiv:2604.27792_ , 2026. 

- NVIDIA, Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, et al. GR00T N1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- NVIDIA et al. Cosmos 3: Omnimodal world models for physical AI. _arXiv preprint arXiv:2606.02800_ , 2026. 

- NVIDIA GEAR Team, Allison Azzolini, Johan Bjorck, Valts Blukis, Fernando Castañeda, et al. GR00T N1.6: An improved open foundation model for generalist humanoid robots. NVIDIA Research project page, 2025. URL https://research.nvidia.com/labs/gear/ gr00t-n1_6/. Accessed September 15, 2026. 

- Jonas Pai, Liam Achenbach, Victoriano Montesinos, Benedek Forrai, Oier Mees, and Elvis Nava. mimic-video: Video-action models for generalizable robot control beyond VLAs. _arXiv preprint arXiv:2512.15692_ , 2025. 

- Bikang Pan, Fan Liu, Haotao Lu, Jingya Wang, and Ye Shi. SelfWAM: A self-grounded unified world action model for fast robot control. _arXiv preprint arXiv:2608.00725_ , 2026. 

- William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2023. 

- Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, et al. _π_ 0 _._ 5: A vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- RoboDojo Team. RoboDojo simulation leaderboard. Official leaderboard, 2026. URL https: //robodojo-benchmark.com/leaderboard. Accessed September 15, 2026. 

- RoboTwin Team. RoboTwin 2.0 leaderboard. Official leaderboard and evaluation protocol, 2026. URL https://robotwin-platform.github.io/leaderboard. Accessed September 15, 2026. 

19 

- Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Björn Ommer. Highresolution image synthesis with latent diffusion models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2022. 

- Qiuhong Shen, Shihua Zhang, Yue Liao, Qi Li, Zhenxiong Tan, et al. World action models: A survey. _arXiv preprint arXiv:2606.20781_ , 2026. 

- StarVLA Community. StarVLA: A lego-like codebase for vision-language-action model developing. _arXiv preprint arXiv:2604.05014_ , 2026. 

- Bahey Tharwat, Yara Nasser, Ali Abouzeid, and Ian Reid. Latent action pretraining through world modeling. _arXiv preprint arXiv:2509.18428_ , 2025. 

- Qiuyue Wang, Mingsheng Li, Jian Guan, Jinhui Ye, Sicheng Xie, et al. Qwen-VLA: Unifying visionlanguage-action modeling across tasks, environments, and robot embodiments. _arXiv preprint arXiv:2605.30280_ , 2026a. 

- Siyin Wang, Junhao Shi, Zhaoyang Fu, Xinzhe He, Feihong Liu, et al. World action models: The next frontier in embodied AI. _arXiv preprint arXiv:2605.12090_ , 2026b. 

- Weiyun Wang, Zhangwei Gao, Lixin Gu, Hengjun Pu, Long Cui, et al. InternVL3.5: Advancing open-source multimodal models in versatility, reasoning, and efficiency. _arXiv preprint arXiv:2508.18265_ , 2025. 

- Xuan Wang, Yinan Wu, Haoran Duan, and Jungong Han. QuoVLA: Quotient space for visionlanguage-action models. _arXiv preprint arXiv:2605.24890_ , 2026c. 

- Yuqi Wang, Xinghang Li, Wenxuan Wang, Junbo Zhang, Yingyan Li, et al. Unified vision-languageaction model. In _International Conference on Learning Representations_ , 2026d. 

- Yuran Wang, Siqiao Huang, Mingleyang Li, Chenhao Zhang, Jiaqi Liang, et al. OpenWAM: An open, modular exploration towards systematic world-action model pretraining. _arXiv preprint arXiv:2609.07398_ , 2026e. 

- Xiaomi Robotics Team, Jun Guo, Piaopiao Jin, Jason Li, Peiyan Li, et al. Xiaomi-Robotics-1: Scaling vision-language-action models with over 100K hours of real-world trajectories. _arXiv preprint arXiv:2607.15330_ , 2026. 

- Hengyi Xie, Chenfei Yao, Xianjin Wu, Yingying Zhu, Dingkang Liang, et al. TurboVLA: Real-time vision-language-action model at 32 Hz on an RTX 4090 with _<_ 1 GB VRAM. _arXiv preprint arXiv:2607.27205_ , 2026a. 

- Zhipeng Xie, Zongyi Han, Xiangyi Wei, Shiliang Sun, Yang Li, et al. S<sup>2</sup> -VLA: State-space guided vision-language-action models for long-horizon manipulation. In _Proceedings of the International Joint Conference on Artificial Intelligence_ , 2026b. 

- Yifu Xiong, Wenhao Yu, Jiaxuan Lin, Bojun Zou, Jiahao Li, et al. CAC-VLA: Context-gated action conditioning for vision-language-action models. _arXiv preprint arXiv:2607.04816_ , 2026. 

- Gangwei Xu, Qihang Zhang, Jiaming Zhou, Xing Zhu, Yujun Shen, et al. Next Forcing: Causal world modeling with multi-chunk prediction. _arXiv preprint arXiv:2606.11187_ , 2026. 

- An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, et al. Qwen3 technical report. _arXiv preprint arXiv:2505.09388_ , 2025. 

- Ganlin Yang, Zhangzheng Tu, Yuqiang Yang, Sitong Mao, Junyi Dong, et al. EventVLA: Eventdriven visual evidence memory for long-horizon vision-language-action policies. _arXiv preprint arXiv:2606.20092_ , 2026a. 

- Lishan Yang, Wenxuan Song, Xi Wang, Pingyue Sheng, Zheng Fang, et al. 4D-WAM: Infusing spatiotemporal awareness into world action models through trajectory fields. _arXiv preprint arXiv:2608.08023_ , 2026b. 

20 

- Yandan Yang, Shuang Zeng, Tong Lin, Xinyuan Chang, Dekang Qi, et al. ABot-M0: VLA foundation model for robotic manipulation with action manifold learning. _arXiv preprint arXiv:2602.11236_ , 2026c. 

- Angen Ye, Boyuan Wang, Chaojun Ni, Guan Huang, Guosheng Zhao, et al. GigaWorld-Policy: An efficient action-centered world–action model. _arXiv preprint arXiv:2603.17240_ , 2026a. 

- Jinhui Ye, Ning Gao, Senqiao Yang, Jinliang Zheng, Zixuan Wang, et al. StarVLA- _α_ : Reducing complexity in vision-language-action systems. _arXiv preprint arXiv:2604.11757_ , 2026b. 

- Seonghyeon Ye, Yunhao Ge, Kaiyuan Zheng, Shenyuan Gao, Sihyun Yu, et al. DreamZero: World action models are zero-shot policies. _arXiv preprint arXiv:2602.15922_ , 2026c. 

- Haoqi Yuan, Zhixuan Liang, Anzhe Chen, Ye Wang, Haoyang Li, et al. Qwen-RobotManip technical report: Alignment unlocks scale for robotic manipulation foundation models. _arXiv preprint arXiv:2606.17846_ , 2026a. 

- Tianyuan Yuan, Zibin Dong, Yicheng Liu, and Hang Zhao. Fast-WAM: Do world action models need test-time future imagination? _arXiv preprint arXiv:2603.16666_ , 2026b. 

- He Zhang, Lingzhu Xiang, Haitao Lin, Zeyu Huang, Minghui Wang, et al. Hy-Embodied-0.5VLA: From vision-language-action models to a real-world robot learning stack. _arXiv preprint arXiv:2606.14409_ , 2026a. 

- Jianjun Zhang, Jian Zhu, Taiyi Su, Chong Ma, Zitai Huang, et al. Learning 4D geometric priors for inference-efficient world action models. _arXiv preprint arXiv:2607.05468_ , 2026b. 

- Qihang Zhang, Lin Li, Luyao Zhang, Shuai Yang, Yiming Luo, et al. Native video-action pretraining for generalizable robot control. _arXiv preprint arXiv:2607.08639_ , 2026c. 

- Yichi Zhang, Weihao Yuan, Yizhuo Zhang, Xidong Zhang, and Jia Wan. FocusVLA: Focused visual utilization for vision-language-action models. _arXiv preprint arXiv:2603.28740_ , 2026d. 

- Yuyang Zhang, Wenyao Zhang, Zekun Qi, He Zhang, Haitao Lin, et al. ImageWAM: Do world action models really need video generation, or just image editing? _arXiv preprint arXiv:2606.19531_ , 2026e. 

- Mengfei Zhao, Dihong Huang, Yikai Tang, Peihao Li, Mingxuan Yan, et al. AXIS: A growable community-driven data engine for scalable robot manipulation. _arXiv preprint arXiv:2607.21588_ , 2026a. 

- Weiheng Zhao, Haoyi Jiang, Xin Shi, Liu Liu, Fan Huang, et al. Faster-WAM: Efficient inferencetime future conditioning for robust world action models. _arXiv preprint arXiv:2608.04404_ , 2026b. 

- Haoyu Zhen, Zixian Gao, Qiao Sun, Yilin Zhao, Yuncong Yang, et al. Action Images: End-to-end policy learning via multiview video generation. _arXiv preprint arXiv:2604.06168_ , 2026. 

- Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, et al. X-VLA: Soft-prompted transformer as scalable cross-embodiment vision-language-action model. In _International Conference on Learning Representations_ , 2026. 

- Xueyang Zhou, Yangming Xu, Guiyao Tie, Yongchao Chen, Guowen Zhang, Duanfeng Chu, Pan Zhou, and Lichao Sun. LIBERO-PRO: Towards robust and fair evaluation of vision-languageaction models beyond memorization. _arXiv preprint arXiv:2510.03827_ , 2025. 

- Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin Burchfiel, Paarth Shah, and Abhishek Gupta. Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets. _arXiv preprint arXiv:2504.02792_ , 2025. 

21 

# A LIBERO-PRO COMPARISON 

LIBERO-Pro (Zhou et al., 2025) evaluates policies trained on the original LIBERO data under changes to the objects, to their initial positions, to the wording of the instruction, and to the task itself. Table 9 gives the success rate under each perturbation and on the unperturbed tasks, averaged over the four LIBERO suites. The results of _π_ 0, OpenVLA, and _π_ 0 _._ 5 are taken from Zhou et al. (2025), and those of SimVLA and QuoVLA from their papers. 

PatchWAM reaches an average success rate of 57.9%, above _π_ 0 and OpenVLA and below the other three listed methods. On the unperturbed tasks and under paraphrased instructions, it succeeds in 98.4% and 96.8% of the trials, 1.4 and 2.7 percentage points below the best listed results. Under object perturbations, its success rate of 80.8% is the lowest among the listed methods. Changes to the initial positions and to the task are difficult for every listed method: PatchWAM reaches 8.8% and 5.0%, and only QuoVLA exceeds 21% in either category. 

Table 9: LIBERO-Pro results by perturbation (SR, percent), averaged over the four LIBERO suites. Original denotes the unperturbed tasks. Methods are sorted by average SR, and PatchWAM is shown in bold; averages are computed before rounding. 

|Method|Original|Object|Position|Semantic|Task|**Average**|
|---|---|---|---|---|---|---|
|_π_0 (Black et al.,2024)|92.3|90.5|0.0|90.5|0.0|54.7|
|OpenVLA (Kim et al.,2024)|97.0|93.0|0.0|97.3|0.0|57.5|
|SimVLA (Luo et al.,2026d)|98.5|81.5|8.3|98.8|6.0|58.6|
|_π_0_._5 (Physical Intelligence et al.,2025)|96.5|96.0|20.8|95.8|0.8|62.0|
|QuoVLA (Wang et al.,2026c)|99.8|88.3|36.0|99.5|25.5|69.8|
|**PatchWAM (Ours)**|**98.4**|**80.8**|**8.8**|**96.8**|**5.0**|**57.9**|


# B TRAINING DYNAMICS UNDER THE FULL-DATA PROTOCOL 

Figure 5 traces the success rate of PatchWAM over one training run under the full-data protocol. The run uses the clean and randomized demonstrations without the augmented demonstrations and trains for five epochs, or 104,850 updates with 256 samples per update. The checkpoints at every 10k updates, at 95k updates, and at the end of training are evaluated with 10 episodes per task and condition, and the final checkpoint is also evaluated with 100 episodes. The dashed line marks our 100-episode evaluation of the released ImageWAM checkpoint, which reaches 92.77%, slightly below the 93.38% reported for it in Table 1. 

Most of the improvement occurs within the first two epochs: the success rate rises from 65.8% after 10k updates to 80.5% after 20k updates and 92.0% after 40k updates. It then stays at 92.0% until 60k updates. From 70k updates onward, every evaluated checkpoint exceeds the released ImageWAM checkpoint, although the intermediate checkpoints are evaluated with fewer episodes. Between 70k updates and the end of training, the success rate varies between 93.60% and 95.45%. Differences of this size between neighboring checkpoints are comparable to the uncertainty of a 10-episode evaluation: the final checkpoint reaches 95.45% with 10 episodes and 94.57% with 100 episodes per task and condition. For the 10-episode value, two of the 100 task–condition units use their 100-episode results because their 10-episode evaluations did not complete. Under the 100-episode evaluation, the final checkpoint exceeds the released ImageWAM checkpoint by 1.80 percentage points. The 96.12% in Table 1 comes from a separate configuration, which adds the 2,100 augmented demonstrations and trains for 110k updates; it exceeds the 94.57% of the run traced in Figure 5 by 1.55 points. 

22 


Figure 5: Success rate of PatchWAM over a training run under the full-data protocol without augmented demonstrations. **(a)** The full run of 104,850 updates. **(b)** The checkpoints from 40k updates onward, enlarged. Squares denote evaluations with 10 episodes per task and condition, the open diamond the 100-episode evaluation of the final checkpoint, and the dashed line the 100-episode evaluation of the released ImageWAM checkpoint. 

# C PER-TASK RESULTS UNDER THE CLEAN-TO-RANDOM PROTOCOL 

Figure 6 breaks down the clean-to-random results of Table 2 by task. It compares PatchWAM at the reported checkpoint with the four strongest baselines of that table, whose per-task results are taken from the leaderboard (RoboTwin Team, 2026); every method is evaluated with 100 episodes per task and condition. In clean scenes, PatchWAM succeeds in every episode of 11 tasks and falls below 80% on five tasks, the two lowest being putting the object into the cabinet at 48% and hanging the mug at 51%. In randomized scenes, it reaches at least 80% on 16 tasks and at most 20% on two, rotating the QR code and moving the stapler to the pad. Compared with OLA-Sem and GigaBrain0.7, whose success rates in randomized scenes are close to its own, PatchWAM succeeds more often in randomized scenes on 23 and 24 tasks, respectively, and less often on 26 tasks each, so policies with similar success rates differ in which tasks they solve. 

23 

|**(**|**a) Clean**|**scenes**||||**(b) Rand**|**omized**|**scenes**|||
|---|---|---|---|---|---|---|---|---|---|---|
|**P**|**atchWAM**|OLA-Sem<br>|GigaBrain<br>0.7|-<br>4D-WAM|_π_0.5|**PatchWAM**|OLA-Sem|GigaBrai<br>0.7|-<br>4D-WAM|_π_0.5|
|stack blocks two<br>|**100**<br>|91<br>|80<br>|100<br>|91<br>|**97**<br>|90<br>|92<br>|34<br>|43<br>|
|move playingcard away|**100**|90|58|82|84|**96**|92|82|35|65|
|stack blocks three|**98**|74|60|95|77|**96**|52|78|82|25|
|place burger fries|**97**|94|82|86|82|**95**|75|86|72|86|
|place cans plasticbox|**98**|97|8|94|31|**93**|85|18|48|73|
|blocks ranking rgb|**95**|64|68|88|72|**92**|66|76|10|44|
|grab roller|**100**|100|100|100|99|**92**|100|100|68|97|
|shake bottle horizontally|**100**|92|100|98|99|**91**|70|92|70|100|
|<br>stack bowls two|**98**|94|90|94|94|**91**|90|74|81|70|
|place object stand|**98**|81|88|87|85|**87**|77|76|42|47|
|shake bottle|**100**|89|100|98|100|**85**|70|98|72|100|
|pick dual bottles|**100**|92|26|92|72|**84**|84|56|67|57|
|<br>place empty cup|**99**|98|90|99|96|**83**|94|90|70|80|
|<br>place bread basket|**93**|84|60|87|63|**82**|80|68|77|60|
|place container plate|**99**|97|94|93|92|**80**|92|94|82|72|
|put bottles dustbin|**88**|44|68|68|78|**80**|37|54|19|50|
|click alarmclock|**100**|100|98|100|65|**77**|91|96|70|50|
|place shoe|**94**|79|88|83|82|**76**|78|92|52|50|
|dump bin bigbin|**98**|96|90|86|92|**75**|94|66|57|84|
|place dual shoes|**94**|87|68|66|70|**74**|76|72|19|45|
|place object basket|**91**|54|74|75|70|**74**|49|64|40|29|
|adjust bottle|**100**|72|98|80|99|**73**|71|98|36|77|
|handover block|**96**|24|16|79|30|**73**|17|32|25|12|
|place bread skillet|**89**|81|80|82|76|**73**|67|50|69|47|
|place object scale|**99**|69|64|79|78|**73**|63|54|24|38|
|stack bowls three|**86**|88|70|82|81|**72**|81|64|27|52|
|click bell|**100**|100|98|98|31|**71**|98|84|77|35|
|press stapler|**91**|98|90|76|79|**71**|95|74|61|63|
|<br>scan object|**87**|42|32|73|49|**71**|32|46|53|40|
|lift pot|**99**|100|86|88|98|**69**|91|86|9|35|
|pick diverse bottles|**80**|76|38|77|66|**67**|77|50|44|42|
|open laptop|**96**|90|78|85|93|**65**|74|88|82|68|
|place a2b left|**100**|65|68|71|71|**65**|64|72|19|49|
|<br>handover mic|**99**|89|100|85|98|**61**|80|100|13|6|
|place a2b right|**94**|85|58|62|68|**58**|80|68|42|39|
|move pillbottle pad|**99**|78|32|89|46|**56**|71|58|22|32|
|hanging mug|**51**|16|26|70|17|**55**|15|36|10|14|
|beat block hammer|**100**|65|94|92|93|**51**|55|74|28|23|
|place can basket|**74**|36|20|83|56|**51**|34|22|51|10|
|blocks ranking size|**69**|36|42|54|45|**50**|37|28|8|21|
|place phone stand|**95**|75|36|84|65|**46**|63|52|21|37|
|<br>place mouse pad|**89**|59|26|54|34|**45**|55|44|9|31|
|<br>open microwave|**88**|76|82|68|86|**37**|43|50|12|59|
|<br>stamp seal|**94**|87|52|74|53|**37**|70|54|10|21|
|turn switch|**67**|86|42|86|52|**36**|70|52|11|25|
|place fan|**87**|76|78|48|66|**32**|68|74|17|26|
|put object cabinet|**48**|40|78|69|39|**28**|27|82|47|22|
|move can pot|**95**|46|86|94|60|**25**|45|82|17|10|
|<br>move stapler pad|**82**|58|26|43|20|**15**|53|40|12|18|
|<br>rotate qrcode|**84**|46|54|79|90|**10**|40|58|67|21|


Figure 6: Per-task success rates (percent) under the clean-to-random protocol for PatchWAM at the reported checkpoint and the four strongest baselines of Table 2, all evaluated with 100 episodes per task and condition. Tasks are sorted by the success rate of PatchWAM in randomized scenes. **(a)** Clean scenes. **(b)** Randomized scenes. 

# D QUALITATIVE CLEAN-TO-RANDOM ROLLOUTS 

Figure 7 shows paired outcomes from four difficult tasks in randomized scenes. The examples are selected from all 100 evaluation episodes per task of the clean-to-random PatchWAM checkpoint after 100k updates. Success and failure labels are produced by the RoboTwin evaluator rather than assigned manually. 

24 


Figure 7: **Qualitative clean-to-random rollouts in randomized scenes.** Each row pairs a successful rollout (green) with a failed rollout (red) from the same task, with four frames ordered from early interaction to the final outcome. The four tasks have success rates of 4%, 9%, 25%, and 48% in the evaluation of this checkpoint, so each successful rollout comes from a task that the model completes in at most half of the episodes. 

# E TOKEN SEQUENCE AND ATTENTION MASK 

Figure 8 illustrates Section 3.4 with one RoboTwin sample. The three camera views are composed into a 288 _×_ 256 image, with the head camera above the left and right wrist cameras, and the image autoencoder maps this image to an 18 _×_ 16 grid of latent tokens. Each frame therefore contributes 288 tokens. The instruction is padded to 128 text tokens, and the proprioceptive token is inserted directly after the valid text, so that the text block contains 129 tokens. With the two frames and the 16 action tokens, the sequence contains 721 tokens, of which the action tokens account for about 2%. 

The positional coordinates follow the convention of Section 3.4. Text tokens carry their sequence index on the fourth axis, image tokens carry their row and column on the second and third axes, and action tokens carry their step index on the fourth axis. The first axis separates the current frame (10), the future frame (0), and the actions (20). 

Panel (b) shows the mask used in training and inference. Prefix queries attend only to prefix keys, whereas future-frame and action queries attend to every non-padded key. Padded text tokens are masked as keys for all queries. Panel (c) contrasts this mask with the isolated-attention control, in which future-frame and action tokens no longer attend to each other but retain access to the prefix and to their own group. 

25 


Figure 8: **Token sequence and attention mask for one RoboTwin sample. (a)** Each frame becomes an 18 _×_ 16 grid of latent tokens; the bar shows the full sequence to scale, with the positional coordinates of each group. **(b)** The attention mask over all 721 tokens, with rows as queries and columns as keys; the strips along the edges mark the token groups of (a). **(c)** The last 48 tokens of the noisy block, boxed in (b), enlarged for PatchWAM and for the isolated-attention control of Section 5.2. The sample is taken from the first training episode, with the instruction “Grab the smooth green plastic bottle and lift it with the left arm”, whose prompt occupies 25 of the 128 text tokens. 

# F IMPLEMENTATION DETAILS 

This appendix gives the settings of the training runs and evaluations in this paper. Table 10 lists the settings that the runs share, and Table 11 gives the number of GPUs, the batch sizes, and the number of epochs of each run. The RoboDojo run also uses past frames and a vision-language (VL) model as its text encoder, and the paragraphs _RoboDojo run_ and _RoboDojo text encoder_ below describe its configuration. 

Table 10: Settings shared by the training runs. The RoboDojo run uses a different text encoder and an additional loss, as described below. 

|Setting|Value|
|---|---|
|Transformer|FLUX.2 [klein] 4B Base, all weights trained|
|State projection|linear layer, trained|
|Image autoencoder|FLUX.2 autoencoder, frozen|
|Text encoder<br>Action chunk|Qwen3-4B, frozen, 128 instruction tokens<br>_H_ = 16steps, future frame at the end of the chunk|
|Action-as-Patch|token width_D_ = 128, scale_α_= 1|
|Noise-level shift|_s_= 5in training and inference|
|Loss weights|_λx_ = 0_._5,_λu_ = 1_._0|


**Training data.** Each training sample is a window of 17 time steps that covers the current observation, the 16 actions of the chunk, and the observation at the end of the chunk; apart from the past frames of the RoboDojo run, only the first and the last image of the window are loaded. On RoboTwin 2.0, idle segments, in which the commanded action matches the current robot state, are removed from each demonstration before the windows are formed. Idle steps at the end of a demonstration are kept, because they often contain the release of the object. After this step, the RoboTwin 2.0 full-data set contains about 5.37 million training windows. The matched comparison keeps one window start out of every twenty, or about 268,000 windows, and both of its runs pass over each retained window ten times. The RoboDojo run keeps all steps of each demonstration. On LIBERO, the four suites are used without their no-op actions. 

26 

Table 11: Parallelism, batch size, and number of epochs of each training run. The global batch size is the product of the number of GPUs, the gradient-accumulation steps, and the batch size per GPU. The clean-to-random and RoboDojo runs stop after a fixed number of updates instead of a number of epochs. 

|||||Batch|size||
|---|---|---|---|---|---|---|
|Benchmark|Run|GPUs|Accumulation|Per GPU|Global|Epochs|
|RoboTwin 2.0|Full-data|32|2|4|256|5|
||Full-data, augmented|32|2|4|256|5|
||Matched comparison|8|2|4|64|10|
||Clean-to-random|16|1|16|256|—|
|LIBERO|Original data|16|1|8|128|10|
|LIBERO-Plus|Augmented data|16|2|8|256|10|
|RoboDojo|Past frames, VL text encoder|32|1|8|256|—|


**Image augmentation.** RoboTwin 2.0 and RoboDojo runs other than the clean-to-random run augment half of the training samples online. An augmented sample is cropped to between 95% and 100% of each image side and rotated by up to 5 degrees, and it additionally receives color changes, Gaussian noise with a standard deviation of 0.01, or both. The color changes scale brightness, contrast, and saturation by factors between 0.8 and 1.2, shift the hue by up to 11 degrees, and apply a gamma between 0.9 and 1.1. All camera views and both frames of a sample share the same crop, rotation, and color parameters. In the RoboDojo run, the parameters are drawn separately for each camera view and for the past frames, and the input images of the text encoder are not augmented. LIBERO runs apply the same transforms with wider ranges, plus an exposure change, to 65% of the samples: crops to at least 92% of each side, rotations of up to 8 degrees, brightness and contrast factors between 0.7 and 1.3, saturation factors between 0.75 and 1.25, hue shifts of up to 14 degrees, gammas between 0.8 and 1.25, exposure changes of up to 0.25 stops, and noise with a standard deviation of 0.015. The clean-to-random run replaces these transforms with a stronger randomization, which is applied to 80% of the samples, with parameters drawn separately for each camera view and shared by both frames. It scales brightness, contrast, and saturation by factors between 0.6 and 1.4, shifts the hue by up to 36 degrees, applies a gamma between 0.7 and 1.4 and an exposure change of up to 0.5 stops, scales the red and blue channels by up to 15% to change the color temperature, blurs the image with probability 0.3, and adds Gaussian noise with a standard deviation of 0.03. With probability 0.5 each, it then applies an AdaIN transform, which moves the mean and standard deviation of each color channel toward random targets, and an FFT-based transform, which scales the amplitude spectrum of the image by random factors between 0.5 and 1.5 while keeping its phase. Neither of these two transforms moves edges or objects, and the run uses no crops or rotations. 

**RoboDojo run.** The RoboDojo run keeps the three camera views as separate 256 _×_ 256 images, so each view contributes 256 latent tokens per frame, and, as on RoboTwin 2.0, both actions and proprioceptive states are 14-dimensional. The future frames of all three views are predicted, and the views are distinguished by their values on the first positional axis, which are 10, 11, and 12 for the current frame and 0, 1, and 2 for the future frame. The run also conditions on 20 slots of past head-camera frames, one per second over the last 20 seconds. At inference, slot _k_ holds the frame from _k_ seconds before the current step, and slots that lie entirely before the start of the episode are masked. During training, the frame of each slot is drawn uniformly within 0.4 seconds of this time, the whole history is dropped with probability 0.2 and each slot with probability 0.2, and a random number of the most recent remaining slots, between 0 and 20, is kept. Each past frame is encoded by the image autoencoder, average-pooled to 4 _×_ 4 tokens, and added to the prefix with the value _−k_ on the first positional axis, so the history adds 320 tokens and no parameters. 

**RoboDojo text encoder.** The text encoder of the RoboDojo run is Qwen3-VL-4B-Instruct (Bai et al., 2025). It reads the instruction, the current head-camera image, and up to 20 past head-camera frames, one per second over the last 20 seconds, all resized to 448 _×_ 448 and not augmented. During training, each past frame is shifted in time by up to one video frame; unlike the past frames of the transformer, none is dropped. The vision encoder maps each image to 196 tokens, and the tokens of each past frame are average-pooled to 4 _×_ 4 before they enter the language model. The transformer 

27 

receives the concatenated hidden states of layers 9, 18, and 27 at the instruction tokens and those of layers 18, 27, and 36 at the last prompt token. The vision encoder of the VL model stays frozen. LoRA adapters (Hu et al., 2022) with rank 64, a scaling factor of 2, and dropout 0.05 are trained on the attention and feed-forward projections of its language model; the adapters add 132.1M trainable parameters. Subtask labels divide each demonstration into segments and describe each segment in one sentence, and every training demonstration carries such labels. The subtask of the current step is appended after the prompt and predicted with a cross-entropy loss of weight 0.1 and label smoothing 0.1. Because the language model attends causally, the appended subtask does not change the hidden states that the transformer receives, and the subtask is not used at inference. 

**Dual-expert control.** The dual-expert control is ImageWAM (Zhang et al., 2026e) with the same FLUX.2 [klein] 4B backbone. Its action expert has 5 double-stream and 20 single-stream blocks of width 1024; the block counts and the attention dimensions (24 heads of size 128) match those of the backbone, so that the action tokens join the attention of the backbone in every block. The action expert embeds each action step with a linear layer, reads out the action velocity with a linear layer, and starts from random weights. It adds 0.64B trainable parameters to the model. 

**Evaluation.** RoboTwin 2.0 evaluations use seed 43 and the unseen instructions of the benchmark, and the policy executes each predicted chunk of 16 actions in full before it predicts the next chunk from the new observation. On RoboDojo, the policy replans after executing 8 of the 16 actions. LIBERO evaluations run 20 trials per task with seed 42. On LIBERO and LIBERO-Plus, the policy predicts 16 actions and replans after executing 12 of them. All evaluations use 10 solver steps and no classifier-free guidance. 

# G SUPPLEMENTARY SELF-FLOW RESULTS 

Table 12: Self-Flow variants after 41,940 updates (SR, percent), with one of every 20 window starts retained and 10 episodes per task and condition. 

|Configuration|Clean|Randomized|Average|
|---|---|---|---|
|Dual-expert control|77.2|79.6|78.4|
|PatchWAM|87.6|**88.4**|88.0|
|Self-Flow variant 1|**90.0**|87.4|**88.7**|
|Self-Flow variant 2|89.4|87.2|88.3|
|Self-Flow variant 3|85.4|85.6|85.5|


Variant 1 combines dual-timestep scheduling and an EMA-teacher representation loss. Variant 2 adds modality-structured timestep masks. Variant 3 also withholds the action labels of 25% of the samples and uses labels generated by the teacher instead. These variants change the training objective and are therefore not independent training repetitions of PatchWAM. Variants 1 and 2 succeed more often in clean scenes, and all three succeed less often in randomized scenes. 

28 

