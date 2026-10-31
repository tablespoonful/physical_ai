---
title: "EgoPriMo: Egocentric Motion Generation for Interactive Humanoid Control"
date: "2026-06-07"
authors: "Haoyang Ge; Peng Ren; Yukun Shi; Cong Huang; Kun Li; Kai Chen"
url: https://arxiv.org/abs/2606.08495
pdf: https://arxiv.org/pdf/2606.08495
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.08495)** / [論文ページ](https://arxiv.org/abs/2606.08495)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **EgoPriMo: Egocentric Motion Generation for Interactive Humanoid Control** 

Haoyang Ge<sup>1</sup><sup>_,_2</sup><sup>_,∗_</sup> , Peng Ren<sup>2</sup><sup>_,_3</sup> , Yukun Shi<sup>2</sup><sup>_,_4</sup> , Cong Huang<sup>2</sup><sup>_,_4</sup> , Kun Li<sup>1</sup><sup>_,†_</sup> , and Kai Chen<sup>2</sup><sup>_,_4</sup><sup>_,_5</sup><sup>_,†_</sup> 


Fig. 1. **EgoPriMo.** Egocentric observations provide scene context, while text prompts specify the intended action. Conditioned on both, EgoPriMo generates SMPL whole-body motion references for an existing controller to track, enabling humanoid behaviors such as kicking, handshaking, and dancing. 

**_Abstract_ — Humanoid robots require whole-body motions that adapt to scene context, task requirements, and user intent. Despite advances in motion tracking and humanoid vision-language-action models, integrating scene context and user intent into a reusable motion prior remains challenging. We introduce EgoPriMo, short for Egocentric Motion Prior for Humanoid Robots, a unified framework that learns such priors from egocentric human demonstrations. Given egocentric observations and a text prompt, EgoPriMo reconstructs, generates, and forecasts SMPL-based full-body motion. Language is used as a high-level control signal rather than a complete motion specification. At the core of EgoPriMo is a Triplestream DiT that jointly models body dynamics, egocentric visual context, and text; task-conditioning masks route different tasks and missing-modality data through the same checkpoint. Experiments on Nymeria and EgoExo4D demonstrate improved egocentric motion generation over UniEgoMotion, with gains in motion accuracy, semantic similarity, and foot-contact quality. Text prompts steer motion generation under fixed visual conditions, and the generated SMPL motions can be executed through an existing whole-body controller.** 

## I. INTRODUCTION 

Humanoid robots need natural, diverse, and controllable whole-body motions in open environments. A practical humanoid should coordinate whole-body movements according to scene context and user intent. Examples include kicking 

> 1Tianjin University, Tianjin, China. 

> 2Zhongguancun Academy, Beijing, China. 

> 3Beihang University, Beijing, China. 

> 4Zhongguancun Institute of Artificial Intelligence, Beijing, China. 

> 5DeepCybo, Beijing, China. 

> _∗_ ghy0623@tju.edu.cn. 

> _†_ Corresponding authors: Kun Li and Kai Chen. 

a ball with the foot, reaching out for a handshake, and raising both hands to dance. We study egocentric-observation conditioned full-body motion generation as a scalable way to learn reusable motion priors from human demonstrations. As shown in Figure 1, EgoPriMo translates egocentric observations and text prompts into full-body motion references for humanoid execution. 

Motion tracking and imitation have made strong progress in humanoid whole-body control by reproducing trajectories from motion capture, teleoperation, or curated libraries [1]– [7]. Yet the desired motion is usually already specified, making these systems closer to motion replay than openended synthesis. Humanoid vision-language-action models provide semantic instruction interfaces [8]–[10], but are still centered on task-specific navigation, manipulation, or short-horizon operational skills. Broad, long-horizon wholebody motion generation remains underexplored. Egocentric human demonstrations bridge this gap. Egocentric videos are abundant, low-cost, and capture visual context, cameramotion cues, task-relevant objects, intent, and interaction cues. Recent egocentric datasets and models demonstrate their value for activity understanding and human motion modeling [11]–[14]. For humanoids, such data provide environment-grounded supervision for learning both fullbody motion and its coupling to the observed scene. A useful egocentric motion prior should reconstruct demonstrations, generate full-body motion from partial egocentric evidence, and forecast future motion. We therefore treat language as a high-level control signal rather than a complete motion 

II. RELATED WORK 

specification: users steer egocentrically grounded motion with targeted prompts about intent, timing, or interaction style. 

Egocentric observations and language constrain motion in complementary ways. An image provides evidence about the surroundings but often leaves the wearer’s body outside the field of view, while a text prompt specifies the intended action without prescribing a complete pose sequence. The model must therefore combine scene evidence and action intent to generate temporally coherent motion. This involves coordinating modalities with distinct roles: visual features describe the observed context, text features encode semantic intent, and motion features represent the evolving body state. These considerations motivate a generative architecture that preserves modality-specific processing while enabling joint cross-modal interaction. 

As an egocentric motion prior for humanoid robots, EgoPriMo unifies reconstruction, generation, and forecasting. Given egocentric observations and a text prompt, EgoPriMo generates an SMPL-based full-body motion sequence. At the core of EgoPriMo is a Triple-stream DiT that jointly models body motion, egocentric visual context, and language. Taskconditioning masks decide which motion frames, image tokens, auxiliary pose cues, and text tokens are visible, allowing the same checkpoint to support multiple tasks without task-specific heads. The generated SMPL motion can be consumed by an SMPL-conditioned humanoid controller. 

Experiments on Nymeria show that one EgoPriMo checkpoint supports reconstruction, generation, and forecasting. On an external egocentric generation benchmark, EgoPriMo improves the strongest matched comparison in joint accuracy and contact plausibility. These results suggest that egocentric human motion generation is a practical route toward generalizable and interactively controllable humanoid motion priors. We further evaluate prompt control with 100 paired Nymeria validation clips, holding egocentric conditions and initial noise fixed while changing the text. The resulting motions shift toward the reference associated with the supplied prompt. On a Unitree humanoid, the complete pipeline succeeds in 7 of 10 ball-kicking trials and 8 of 10 tableavoidance trials without robot-view fine-tuning. Here, interaction means selecting a high-level prompt before generation; online language correction and closed-loop replanning are outside the evaluated setting. 

Our main contributions are: 

- We formulate egocentric human motion generation as a scalable paradigm for humanoid full-body behavior learning. 

- We introduce a Triple-stream DiT as the core generative backbone for jointly modeling body motion, egocentric visual context, and language. 

- We propose a unified task-conditioned framework that performs full-body motion reconstruction, generation, and forecasting with a single checkpoint. 

**Humanoid motion tracking and imitation.** Motion imitation transfers human motion references to humanoid robots while addressing embodiment and dynamics differences, as demonstrated by ExBody [3] and ASAP [5]. HumanPlus [1] and OmniH2O [2] extend motion tracking to teleoperation and autonomous skill learning. HOVER [4] unifies multiple control modes, while SONIC [7] scales motion tracking and connects it to kinematic planning and visuomotor policies. VisualMimic [6] further couples a visual policy that generates keypoint commands with a low-level tracker for locomanipulation. These systems establish motion tracking as an interface between human motion and robot control. Our focus is a complementary generative component: an egocentric human motion prior that uses text prompts to produce SMPLbased motion references for an existing humanoid controller. 

**Vision-language-action models for humanoid robots.** Vision-language-action models such as OpenVLA [8] learn language-conditioned manipulation policies from robot demonstrations. EgoVLA [9] uses egocentric human videos to learn wrist and hand action prediction, then retargets these actions and fine-tunes with robot demonstrations for humanoid manipulation. Related egocentric imitation work, EgoMI [10], models coordinated head and hand motion for active vision and manipulation on semi-humanoid embodiments. EgoVLA and EgoMI illustrate how egocentric human data can support robot policy learning. EgoPriMo instead models human full-body motion in SMPL space, with visual and text conditioning, and uses the generated sequence as a reference for a separate whole-body controller. 

**Egocentric human motion understanding and generation.** Project Aria [15] provides a platform for multimodal egocentric sensing. Nymeria [12] pairs egocentric observations with full-body motion and language annotations; EgoExo4D [11] captures skilled activities from synchronized first- and third-person views; and EgoBody [16] provides 3D body annotations during social interactions. For images captured by a downward-facing camera, EgoHMR [17] recovers human meshes using a hierarchical latent diffusion model that combines global and local image features without requiring 2D pose supervision. This setting provides direct visual evidence of the wearer’s body. Forward-facing observations instead motivate the use of head-motion cues to infer body motion that lies outside the camera view. EgoEgo [13] reconstructs full-body motion through an intermediate headpose estimate, while EgoAllo [18] estimates body and hand motion in the scene coordinate frame from egocentric SLAM poses and images. UniEgoMotion [14] unifies reconstruction, forecasting, and generation using egocentric visual and trajectory conditions. Building on its task-conditioning formulation, EgoPriMo introduces a dedicated text stream alongside motion and vision, using a Triple-stream DiT to learn language-controllable SMPL-based motion references for humanoid execution. The architecture preserves modality-specific transformations during joint attention and then fuses the tokens in Single-stream DiT blocks, with 

global text conditioning retained throughout both stages. 

**Language-guided motion generation.** Text-to-motion methods learn variational motion representations [19], [20], denoise motion or latent sequences [21]–[23], or model discrete motion tokens [24], [25]. TMR [26] learns contrastive text–motion embeddings for retrieval, with motion synthesis as an auxiliary training objective. These methods establish semantic control and alignment between language and motion, without directly conditioning on egocentric visual observations. Beyond text-only conditioning, HUMANISE [27] aligns captured motions with 3D indoor scenes and annotates the resulting interactions with language. Its sceneand-language conditioned model generates motions that interact with specified objects, connecting action semantics to scene geometry. This formulation uses an explicit 3D scene representation to provide the environmental context for generation. GMD [28] introduces spatial guidance into text-conditioned diffusion to support trajectory constraints, sparse keyframe locations, and obstacle avoidance. OmniControl [29] extends spatial control to different joints at arbitrary times, combining spatial guidance with realism guidance to balance constraint satisfaction and motion coherence. These approaches expose geometric control through explicit spatial constraints, alongside the semantic control provided by text. EgoPriMo uses egocentric image features to supply visual context and accommodates observed head trajectories through task-dependent masks. For generation, it conditions on an initial egocentric image and a text prompt without requiring a prescribed future trajectory. Its multimodal design therefore addresses how visual observations and language jointly condition motion when future pose cues are unavailable. In robotics, language feedback can also correct plans and improve trajectories [30]–[32]. EgoPriMo uses a prompt selected before generation to steer SMPLbased motion under egocentric visual conditions; online language correction is outside the evaluated setting. Its focus is the joint use of scene context and textual intent in a human motion prior that interfaces with humanoid control. 

## III. METHOD 

## _A. Overview_ 

EgoPriMo unifies egocentric motion reconstruction, generation, and forecasting in a text-conditioned model. These tasks share the same model and differ in their visible conditions: full-sequence observations for reconstruction, an initial egocentric image for generation, and past observations for forecasting. As shown in Figure 2, a Triple-stream DiT jointly processes motion, image, and text tokens to generate SMPL-based motion sequences. The generated motions can directly drive a humanoid robot through an existing wholebody controller. 

## _B. Task Formulation and Flow-Matching Objective_ 

We represent the target motion as **x** 1 _∈_ R<sup>_T_max</sup><sup>_×F_</sup> , where _T_ max is the maximum sequence length and _F_ = 234. For body motion, we use the rotations and positions of 22 SMPL-X body joints [33], together with foot-contact 

indicators and body-shape coefficients. Joint rotations and positions are expressed in a canonical sequence coordinate frame, with rotations in continuous 6D form [34]. Motion features are standardized before training. The condition **y** comprises egocentric image features, head trajectories, text features, and sequence length, together with visibility and padding masks. Visibility masks specify which conditions are available, while padding masks identify valid frames. We learn a conditional velocity field _vθ_ ( **x** _τ , τ,_ **y** ) using flow matching [35]. We sample **x** 0 _∼N_ (0 _, I_ ) and _τ ∼U_ (0 _,_ 1), and linearly interpolate between noise and the target motion. For a single sequence, the interpolated state, target velocity, and weighted loss are 


Here _t_ indexes motion frames, _pt ∈{_ 0 _,_ 1 _}_ excludes padding, and _ϵ_ = 10<sup>_−_8</sup> stabilizes the normalization. The taskdependent frame weight _wt_ is 1 for reconstruction and for frames with masked image conditions. Frames with visible image conditions receive weights of 0.1 for generation and 0.5 for forecasting, so their motion targets also contribute to training. The numerator and denominator are accumulated over the minibatch. All three tasks share the same velocity field and objective, with differences specified by condition visibility and frame weights. 

## _C. Triple-stream DiT for Egocentric Motion Generation_ 

Egocentric motion generation involves three heterogeneous token types with different roles. The noisy motion tokens represent the body state being denoised, the image tokens provide egocentric scene and interaction context, and the text tokens encode high-level semantic guidance. Directly concatenating these tokens at the input mixes modalities with different temporal structures and semantic meanings from the beginning. Instead, EgoPriMo adopts a Triple-stream DiT that first preserves modality-specific processing and then performs cross-modal fusion. 

Each stream has its own input projection, QKV projection, output projection, and MLP. This design allows each modality to maintain its own representation space before fusion: motion tokens focus on kinematic continuity, image tokens focus on scene-grounded cues, and text tokens focus on prompt semantics. Missing or hidden conditions are replaced by learned mask tokens, enabling the same architecture to handle different token combinations. The three streams exchange information through joint attention. In each Triplestream block, we compute stream-specific queries, keys, and values for motion tokens, image tokens, and text tokens, and then concatenate them to form a joint attention sequence. This allows motion tokens to query image tokens and text tokens, while still using stream-specific transformations before and after attention. Motion and image tokens use RoPE [36] to encode temporal order, whereas text tokens keep the positional structure inherited from the language 


Fig. 2. Overview of EgoPriMo. Right: the framework generates SMPL-based motion conditioned on egocentric observations, text prompts, and available head trajectories. Task-dependent visibility masks enable reconstruction, generation, and forecasting within the same model. The generated motion can directly drive a humanoid robot through an existing whole-body controller. Left: a detailed view of a Triple-stream block, showing modality-specific transformations, joint attention over motion, image, and text tokens, and global conditioning through AdaLN. 

encoder. CLIP-L provides a sentence-level embedding as a global text condition, complementing the text tokens used in joint attention. Combined with embeddings of the flow timestep, head trajectory, and sequence length, it forms the conditioning vector for AdaLN-Zero in every Triplestream and Single-stream block. This global text conditioning acts across all token positions and remains active after the streams are merged. After the Triple-stream stage, motion, image, and text tokens are concatenated and processed by Single-stream DiT blocks. This stage further fuses motion, visual, and textual information through shared attention and MLP layers, while global text conditioning via AdaLN-Zero provides persistent semantic guidance to align the generated motion with the text prompt. The resulting motion tokens are projected to the velocity field _vθ_ . 

## _D. Unified Task Modeling and Sampling_ 

Task-dependent visibility masks specify which modalities and time intervals condition the shared model [14]. Reconstruction uses egocentric images and head trajectories over the full sequence. Generation retains only the initial egocentric image and masks all head-trajectory conditions. Forecasting uses images and head trajectories from an observed prefix, with future observations masked. Text prompts, when available, condition all three tasks. 

Heterogeneous training samples provide complementary supervision for the shared motion model. Text–motion pairs associate action semantics with motion patterns, while egocentric video–motion pairs relate visual context to body movement. Samples containing all three modalities provide joint visual and language conditioning. Modality availability depends on the annotations, whereas task-dependent visibility determines which available conditions the model can access. An unannotated modality and a condition hidden by 

the selected task are both handled through masking. 

For all three tasks, sampling starts from Gaussian noise **x** 0 _∼N_ (0 _, I_ ). We integrate the learned velocity field _vθ_ ( **x** _τ , τ,_ **y** ) from _τ_ = 0 to _τ_ = 1 using Euler steps, with the selected conditions held fixed. The resulting motion features are denormalized and decoded into SMPL-based motion sequences. 

## _E. From Generated Motion to Humanoid Control_ 

EgoPriMo connects egocentric observations and text prompts to humanoid execution through SMPL-based motion references. The generated motion sequence is converted into the input representation of an existing whole-body controller, which tracks the reference to produce robot actions. In this pipeline, EgoPriMo generates motion conditioned on scene context and user intent, while the controller handles robotspecific motion tracking. The motion generator is trained independently of the controller, without controller or simulator feedback. We evaluate the resulting pipeline on a Unitree humanoid in Section IV-E. 

IV. EXPERIMENTS 

## _A. Experimental Setup_ 

**Datasets and tasks.** We train EgoPriMo on a mixture of Nymeria [12], HumanML3D [19], and processed EgoExo4D [11], with respective sampling probabilities of 70%, 15%, and 15%. Training clips contain up to 240 frames at 30 fps in our SMPL-based representation. Generation is evaluated on Nymeria and the UniEgoMotion-compatible EgoExo4D validation split; reconstruction and forecasting are evaluated on Nymeria. 

**Baselines and metrics.** We compare reconstruction with EgoAllo [18], EgoEgo [13], and UniEgoMotion [14]. For generation and forecasting, we retrain UniEgoMotion on 

Nymeria and processed EgoExo4D without text conditioning. Both methods use the same evaluation clips and SMPL conversion, while HumanML3D is included only in the training of EgoPriMo. 

We report joint and root-trajectory errors in meters. For reconstruction, MPJPE measures mean per-joint position error after a single similarity alignment over the entire sequence, while PA-MPJPE uses per-frame Procrustes alignment. Root Mean and Root Final measure the average and final rootposition errors after matching the pelvis positions at the first valid frame with a single translation. For generation and forecasting, we compute M-FID as the Fr´echet distance between generated and reference motion distributions in the TMR [26] feature space. SemSim measures similarity between paired generated and reference motion embeddings. Air ratio and foot sliding quantify contact-related artifacts. Lower is better except for SemSim. 

**Implementation.** The DiT has a hidden dimension of 1024, 16 attention heads, 16 Triple-stream blocks, and 16 Singlestream blocks. We train with AdamW, a learning rate of 5 _×_ 10<sup>_−_5</sup> , weight decay 0.01, and gradient clipping at 1.0. Reconstruction, generation, and forecasting are sampled with probabilities 40%, 30%, and 30%, respectively. Training takes approximately 72 hours on 24 NVIDIA A100 GPUs. Inference uses 50-step Euler sampling. 

## _B. Egocentric Motion Reconstruction_ 

Reconstruction evaluates how accurately EgoPriMo recovers body pose and root motion from full-sequence egocentric observations. Table I compares methods on 3,000 Nymeria sequences at 15 fps using 21 common joints. Scores are computed on jointly valid frames and averaged over sequences. EgoAllo [18], EgoEgo [13] receive GT-derived camera trajectories. EgoPriMo and UniEgoMotion [14] is evaluated without external conditioning for this comparison. 

TABLE I 

MOTION RECONSTRUCTION ON NYMERIA. 

|Method|MPJPE_↓_|PA-MPJPE_↓_|Root Mean_↓_|Root Final_↓_|
|---|---|---|---|---|
|EgoAllo|0.1885|0.1232|0.5348|0.9444|
|EgoEgo|0.1923|0.1332|0.5042|0.8857|
|UniEgoMotion|0.3890|0.1114|1.0626|1.8229|
|EgoPriMo|**0.1760**|**0.0754**|**0.4260**|**0.8104**|


EgoPriMo achieves the lowest errors across all four metrics in Table I, reducing MPJPE and PA-MPJPE by 6.6% and 32.3% relative to the best baseline for each metric. Root Mean decreases by 15.5% relative to EgoEgo, while the lower Root Final indicates more accurate recovery of the trajectory endpoint. Together, these gains demonstrate improved estimation of both body pose and root motion within our unified framework. Triple-stream DiT retains modalityspecific processing in a dedicated image stream, while joint attention allows motion tokens to query egocentric visual cues and text semantics before further fusion in Singlestream blocks. The generation ablation in Section IV-D 

also supports this design: Triple-stream DiT outperforms the Single-stream baseline that concatenates all modality tokens at the backbone input. 

## _C. Egocentric Motion Generation and Forecasting_ 

**Motion generation.** Given an initial egocentric image and available text prompts, EgoPriMo generates an SMPL-based motion sequence from noise without observed motion frames or head-trajectory conditioning. We compare with UniEgoMotion on Nymeria and EgoExo4D in Table II. Since these sparse conditions admit multiple plausible motions, we assess agreement with reference motions, motion distribution quality, and foot-contact behavior. 

EgoPriMo improves all six metrics over UniEgoMotion on both datasets. On Nymeria, MPJPE and foot sliding decrease by 59.2% and 71.2%, respectively, indicating gains in motion accuracy and contact behavior. On EgoExo4D, MPJPE decreases by 7.4%, accompanied by lower PA-MPJPE, air ratio, and foot sliding. Lower M-FID and higher SemSim on both datasets further indicate closer agreement with the reference motion distributions and greater semantic similarity to individual reference motions. Together, these results support motion generation from sparse visual conditions within our unified framework. Triple-stream DiT combines initial scene cues and prompt semantics through joint attention, while global text conditioning provides semantic guidance throughout denoising. 

TABLE II 

EGOCENTRIC MOTION GENERATION ON NYMERIA AND EGOEXO4D. 

||Method|MPJPE_↓_|PA-MPJPE_↓_|Air_↓_|M-FID_↓_|SemSim_↑_|Slide_↓_|
|---|---|---|---|---|---|---|---|
|EgoExo4D|UniEgoMotion<br>EgoPriMo|0.488<br>**0.452**|0.116<br>**0.106**|0.055<br>**0.041**|0.041<br>**0.035**|0.836<br>**0.852**|1.84<br>**1.42**|
|Nymeria|UniEgoMotion<br>EgoPriMo|1.168<br>**0.477**|0.127<br>**0.113**|0.091<br>**0.024**|0.086<br>**0.032**|0.689<br>**0.855**|4.37<br>**1.26**|


Figure 3 compares generated and reference motions for bending and reaching, and for walking and turning. In the first example, EgoPriMo recovers the lowered torso and forward-reaching pose seen in the reference. The second example illustrates changes in body orientation during locomotion. These examples illustrate the recovered posture and orientation changes; the quantitative evaluation covers the broader validation sets. 

**Prompt control.** To examine the role of language in motion generation, we test whether changing the text prompt shifts generated motion toward the corresponding reference action under fixed visual evidence. The study uses 100 paired Nymeria validation clips from 51 recording/action scenes. Prompt A describes the target clip; a different Prompt B and its reference motion are selected from another scene with the same clip length. We replace both token- and sentencelevel text features while fixing all other inputs, task masks, 


Fig. 3. Motion generation examples for bending and reaching on the left and walking and turning on the right. Rows show UniEgoMotion, EgoPriMo, and ground-truth motions; text prompts are shown above. 

model weights, and initial noise. Sampling uses the final 16Triple/16-Single checkpoint, 50 Euler steps, no classifier-free guidance, and base seed 62 with identical noise for each prompt pair. 

For each prompt, Table III compares the generated motion against both reference motions. SemSim is (1 + cos( _eM , eR_ )) _/_ 2, where _eM_ and _eR_ are the TMR embeddings of the generated and reference motions. Features are evaluated at 20 fps after resampling the 30 fps sequences. Each cell reports a mean over the 100 pairs; the score measures motion-semantic similarity to a prompt-associated reference. 

TABLE III 

PROMPT-CONDITIONED MOTION SIMILARITY. 

Their paired-bootstrap 95% intervals are [0.1586, 0.2038] and [0.1015, 0.1532], using 20,000 resamples of the 100 pairs. The change in mean reference preference supports prompt-dependent shifts in motion semantics under fixed visual inputs and sampling noise. These aggregate scores do not establish instruction compliance for every clip. 

**Motion forecasting.** Forecasting tests whether the shared model can extend a partially observed motion into the future. We keep past motion or observations visible and predict the future interval using the forecasting mask, without changing model weights or adding a task-specific head. Table IV reports the Nymeria results. 

TABLE IV 

MOTION FORECASTING ON NYMERIA. 

|Generated with|Reference A|Reference B|
|---|---|---|
|Prompt A|**0.8267**|0.6453|
|Prompt B|0.6789|**0.8066**|


The mean scores favor the prompt-associated reference in both conditions: 0.8267 versus 0.6453 for Prompt A, and 0.8066 versus 0.6789 for Prompt B. The mean matchedminus-mismatched reference margins are 0.1815 and 0.1277. 

|Method|MPJPE_↓_|PA-MPJPE_↓_|Air_↓_|M-FID_↓_|SemSim_↑_|Slide_↓_|
|---|---|---|---|---|---|---|
|UniEgoMotion|0.888|0.124|0.079|0.066|0.801|2.72|
|EgoPriMo|**0.456**|**0.111**|**0.026**|**0.029**|**0.860**|**1.24**|


EgoPriMo reduces forecasting MPJPE by 48.6%, from 0.888 to 0.456 m, and improves all five remaining metrics. In particular, SemSim increases from 0.801 to 0.860 and foot 

sliding decreases from 2.72 to 1.24. The consistent gains across geometry, motion-semantic similarity, and contact metrics support forecasting with the generation checkpoint under this protocol. 

## _D. Ablation Study_ 

Table V evaluates the training data mixture and fusion architecture under the same Nymeria generation protocol. The data ablation compares Nymeria-only training with the full mixture while keeping Triple-stream DiT fixed. The architecture ablation uses the full mixture for both models; the Single-stream baseline concatenates motion, image, and text tokens at the backbone input. 

TABLE VI 

REAL-ROBOT TASK SUCCESS. 

|Task|Successful trials|Success rate|
|---|---|---|
|Ball kicking|7/10|70%|
|Table avoidance|8/10|80%|


The pipeline succeeds in 7 of 10 ball-kicking trials and 8 of 10 table-avoidance trials. These results demonstrate that the generated SMPL references can support object interaction and obstacle avoidance through an existing controller in the tested setting. The success rates measure complete task execution across perception, motion generation, and tracking on this platform. Figure 5 shows an example of table avoidance. 

TABLE V 

DATA AND FUSION ABLATIONS. 

|Architecture|Single-stream|Triple-stream|Triple-stream|
|---|---|---|---|
|Data / Recipe|Full mixture|Nymeria-only|Full mixture|
|MPJPE_↓_|0.497|0.560|**0.477**|
|PA-MPJPE_↓_|0.118|**0.109**|0.113|
|Air_↓_|0.038|0.045|**0.024**|
|Slide_↓_|1.39|3.92|**1.26**|


**Training data.** The full mixture reduces MPJPE by 14.8% and foot sliding by 67.9% relative to Nymeria-only training, while also lowering air ratio. PA-MPJPE is 0.113 m, compared with 0.109 m for Nymeria-only training. These results support using heterogeneous motion data within the shared training objective, with the clearest gains in overall jointposition accuracy and foot-contact behavior. 

**Fusion architecture.** Triple-stream DiT improves all four metrics over the Single-stream baseline, reducing MPJPE by 4.0% and air ratio by 36.8%. The joint gains in pose and contact metrics support the staged fusion design: modalityspecific transformations are retained as motion, image, and text tokens exchange information through joint attention, followed by further fusion in Single-stream DiT blocks. These findings apply to the tested configurations; isolating the effect of fusion structure requires matched parameter counts and repeated training runs. 

## _E. Humanoid Robot Control_ 

We evaluate motions generated by EgoPriMo from egocentric observations and text prompts on a Unitree humanoid using an existing whole-body controller. The controller tracks the generated SMPL references without returning execution feedback to the motion generator. Figure 4 shows execution for “Kick the ball with your left foot” and “Put up your hands and dance”. Robot-camera observations are absent from generator training, and the demonstrations use no robotview fine-tuning or domain adaptation. 

**Task success.** We quantify task completion separately with 10 trials each for ball kicking and table avoidance. The avoidance task uses the prompt “Walk forward to avoid the table”. A successful trial requires effective ball contact for kicking or collision-free route completion for avoidance, with no fall in either task. Table VI summarizes the outcomes. 


Fig. 5. Table avoidance with generated SMPL motion. 

## V. DISCUSSION AND CONCLUSION 

EgoPriMo unifies egocentric observations, text, and motion in a Triple-stream DiT. Task-dependent masks enable one checkpoint to support reconstruction, generation, and forecasting. Experiments demonstrate improved pose accuracy under the evaluated configurations and prompt-sensitive motion generation. The generated SMPL references can also be executed through an existing humanoid controller. 

Foot sliding remains a limitation, and the generator does not enforce robot dynamics or use controller feedback. Realrobot evidence is limited to one platform and a small number of trials; broader generalization and comparisons under matched inputs remain to be established. Recording-level training overlap remains unverified for the reconstruction evaluation. Future work will focus on contact-aware generation, execution feedback, and evaluation across datasets and robot platforms. 

## REFERENCES 

- [1] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “Humanplus: Humanoid shadowing and imitation from humans,” _arXiv preprint arXiv:2406.10454_ , 2024. 

- [2] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi, “Omnih2o: Universal and dexterous human-tohumanoid whole-body teleoperation and learning,” in _Conference on Robot Learning_ , 2024, arXiv:2406.08858. 

- [3] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang, “Expressive whole-body control for humanoid robots,” _arXiv preprint arXiv:2402.16796_ , 2024. 

- [4] T. He, W. Xiao, T. Lin, Z. Luo, Z. Xu, Z. Jiang, J. Kautz, C. Liu, G. Shi, X. Wang, L. Fan, and Y. Zhu, “Hover: Versatile neural whole-body controller for humanoid robots,” _arXiv preprint arXiv:2410.21229_ , 2024. 

- [5] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbabu, C. Pan, Z. Yi, G. Qu, K. Kitani, J. K. Hodgins, L. Fan, Y. Zhu, C. Liu, and G. Shi, “Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills,” in _Robotics: Science and Systems_ , 2025, arXiv:2502.01143. 

- [6] S. Yin, Y. Ze, H.-X. Yu, C. K. Liu, and J. Wu, “Visualmimic: Visual humanoid loco-manipulation via motion tracking and generation,” _arXiv preprint arXiv:2509.20322_ , 2025. 


(a) Kicking a soccer ball with the left foot. 


(b) Raising both hands and dancing. 

Fig. 4. Real-robot execution of generated motions for ball kicking on the left and dancing on the right. 

- [7] Z. Luo, Y. Yuan, T. Wang, C. Li, F. Casta˜neda, S. Chen, Z.-A. Cao, J. Li, D. Minor, Q. Ben, J. Park, D. Sami, Z. Wang, X. Da, R. Ding, C. Hogg, L. Song, E. Lim, E. Jeong, T. He, H. Xue, W. Xiao, S. Yuen, J. Kautz, Y. Chang, U. Iqbal, L. Fan, and Y. Zhu, “SONIC: Supersizing motion tracking for natural humanoid whole-body control,” _Science Robotics_ , vol. 11, no. 117, p. eaed4592, 2026. 

- [8] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, _et al._ , “Openvla: An open-source vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 

- [9] R. Yang, Q. Yu, Y. Wu, R. Yan, B. Li, A.-C. Cheng, X. Zou, Y. Fang, X. Cheng, R.-Z. Qiu, H. Yin, S. Liu, S. Han, Y. Lu, and X. Wang, “Egovla: Learning vision-language-action models from egocentric human videos,” _arXiv preprint arXiv:2507.12440_ , 2025. 

- [10] J. Yu, Y. Shentu, D. Wu, P. Abbeel, K. Goldberg, and P. Wu, “Egomi: Learning active vision and whole-body manipulation from egocentric human demonstrations,” _arXiv preprint arXiv:2511.00153_ , 2025. 

- [11] K. Grauman, A. Westbury, L. Torresani, K. Kitani, J. Malik, T. Afouras, K. Ashutosh, V. Baiyya, S. Bansal, B. Boote, _et al._ , “EgoExo4D: Understanding skilled human activity from first- and thirdperson perspectives,” in _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 19 383–19 400. 

- [12] L. Ma, Y. Ye, F. Hong, V. Guzov, Y. Jiang, R. Postyeni, L. Pesqueira, A. Gamino, V. Baiyya, H. J. Kim, K. Bailey, D. S. Fosas, C. K. Liu, Z. Liu, J. Engel, R. De Nardi, and R. Newcombe, “Nymeria: A massive collection of multimodal egocentric daily motion in the wild,” in _European Conference on Computer Vision_ , 2024, pp. 445–465. 

- [13] J. Li, K. Liu, and J. Wu, “Ego-body pose estimation via ego-head pose estimation,” in _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023, pp. 17 142–17 151. 

- [14] C. Patel, H. Nakamura, Y. Kyuragi, K. Kozuka, J. C. Niebles, and E. Adeli, “Uniegomotion: A unified model for egocentric motion reconstruction, forecasting, and generation,” in _IEEE/CVF International Conference on Computer Vision_ , 2025, arXiv:2508.01126. 

- [15] J. Engel, K. Somasundaram, M. Goesele, A. Sun, A. Gamino, A. Turner, A. Talattof, A. Yuan, B. Souti, B. Meredith, _et al._ , “Project aria: A new tool for egocentric multi-modal ai research,” _arXiv preprint arXiv:2308.13561_ , 2023. 

- [16] S. Zhang, Q. Ma, Y. Zhang, Z. Qian, T. Kwon, M. Pollefeys, F. Bogo, and S. Tang, “Egobody: Human body shape and motion of interacting people from head-mounted devices,” in _European Conference on Computer Vision_ , 2022. 

- [17] Y. Liu, J. Yang, X. Gu, Y. Guo, and G.-Z. Yang, “EgoHMR: Egocentric human mesh recovery via hierarchical latent diffusion model,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , May 2023, pp. 9807–9813. 

- [18] B. Yi, V. Ye, M. Zheng, Y. Li, L. M¨uller, G. Pavlakos, Y. Ma, J. Malik, and A. Kanazawa, “Estimating body and hand motion in an ego-sensed world,” in _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2025, pp. 7072–7084. 

- [19] C. Guo, S. Zou, X. Zuo, S. Wang, W. Ji, X. Li, and L. Cheng, “Generating diverse and natural 3d human motions from text,” in _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2022. 

- [20] M. Petrovich, M. J. Black, and G. Varol, “TEMOS: Generating diverse human motions from textual descriptions,” in _European Conference on Computer Vision_ , 2022. 

- [21] G. Tevet, S. Raab, B. Gordon, Y. Shafir, D. Cohen-Or, and A. H. Bermano, “Human motion diffusion model,” in _International Conference on Learning Representations_ , 2023. 

- [22] M. Zhang, Z. Cai, L. Pan, F. Hong, X. Guo, L. Yang, and Z. Liu, “Motiondiffuse: Text-driven human motion generation with diffusion model,” _arXiv preprint arXiv:2208.15001_ , 2022. 

- [23] X. Chen, B. Jiang, W. Liu, Z. Huang, B. Fu, T. Chen, and G. Yu, “Executing your commands via motion diffusion in latent space,” in _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023. 

- [24] J. Zhang, Y. Zhang, X. Cun, Y. Zhang, H. Zhao, H. Lu, X. Shen, and Y. Shan, “Generating human motion from textual descriptions with discrete representations,” in _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023. 

- [25] B. Jiang, X. Chen, W. Liu, J. Yu, G. Yu, and T. Chen, “Motiongpt: Human motion as a foreign language,” _arXiv preprint arXiv:2306.14795_ , 2023. 

- [26] M. Petrovich, M. J. Black, and G. Varol, “Tmr: Text-to-motion retrieval using contrastive 3d human motion synthesis,” in _IEEE/CVF International Conference on Computer Vision_ , 2023. 

- [27] Z. Wang, Y. Chen, T. Liu, Y. Zhu, W. Liang, and S. Huang, “HUMANISE: Language-conditioned human motion generation in 3d scenes,” in _Advances in Neural Information Processing Systems_ , vol. 35, 2022, pp. 14 959–14 971. 

- [28] K. Karunratanakul, K. Preechakul, S. Suwajanakorn, and S. Tang, “Guided motion diffusion for controllable human motion synthesis,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , October 2023, pp. 2151–2162. 

- [29] Y. Xie, V. Jampani, L. Zhong, D. Sun, and H. Jiang, “OmniControl: Control any joint at any time for human motion generation,” in _International Conference on Learning Representations_ , 2024, pp. 28 176–28 194. 

- [30] P. Sharma, B. Sundaralingam, V. Blukis, C. Paxton, T. Hermans, A. Torralba, J. Andreas, and D. Fox, “Correcting robot plans with natural language feedback,” in _Robotics: Science and Systems_ , 2022, arXiv:2204.05186. 

- [31] L. X. Shi, Z. Hu, T. Z. Zhao, A. Sharma, K. Pertsch, J. Luo, S. Levine, and C. Finn, “Yell at your robot: Improving on-the-fly from language corrections,” _arXiv preprint arXiv:2403.12910_ , 2024. 

- [32] Z. Yang, M. Jun, J. Tien, S. Russell, A. Dragan, and E. Bıyık, “Trajectory improvement and reward learning from comparative language feedback,” in _Conference on Robot Learning_ , 2024, arXiv:2410.06401. 

- [33] G. Pavlakos, V. Choutas, N. Ghorbani, T. Bolkart, A. A. A. Osman, D. Tzionas, and M. J. Black, “Expressive body capture: 3d hands, face, and body from a single image,” in _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2019. 

- [34] Y. Zhou, C. Barnes, J. Lu, J. Yang, and H. Li, “On the continuity of rotation representations in neural networks,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2019, pp. 5745–5753. 

- [35] Y. Lipman, R. T. Q. Chen, H. Ben-Hamu, M. Nickel, and M. Le, “Flow matching for generative modeling,” in _International Conference on Learning Representations_ , 2023. 

- [36] J. Su, Y. Lu, S. Pan, A. Murtadha, B. Wen, and Y. Liu, “Roformer: Enhanced transformer with rotary position embedding,” _arXiv preprint arXiv:2104.09864_ , 2021. 

