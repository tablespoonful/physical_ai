---
title: "IMLE-VLA: Fast Single-Step Action Generation for Vision-Language-Action Policies"
date: "2026-09-10"
authors: "Kian Hosseinkhani; Qinhe Peng; George Shramko; Mehran Aghabozorgi; Jianing Qian; Tristan Engst"
url: https://arxiv.org/abs/2609.10915
pdf: https://arxiv.org/pdf/2609.10915
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2609.10915)** / [論文ページ](https://arxiv.org/abs/2609.10915)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **IMLE-VLA: Fast Single-Step Action Generation for Vision-Language-Action Policies** 

Kian Hosseinkhani<sup>1</sup><sup>_∗_</sup> Qinhe Peng<sup>2</sup> George Shramko<sup>1</sup> Mehran Aghabozorgi<sup>1</sup> Jianing Qian<sup>2</sup> Tristan Engst<sup>1</sup> Alireza Moazeni<sup>1</sup> Dinesh Jayaraman<sup>2</sup> Ke Li<sup>1</sup><sup>_,_3</sup><sup>_,_4</sup> 

> 1Simon Fraser University 2University of Pennsylvania 

> 3Alberta Machine Intelligence Institute (Amii) 4Canada CIFAR AI Chair 

> _∗_ Corresponding author 


Fig. 1: Overview of IMLE-VLA: drop in single-step action head removing iterative modelling in VLAs 

**_Abstract_ — Vision-language-action (VLA) policies leverage pretrained vision-language backbones to achieve strong crosstask generalization. A leading design couples this backbone with a dedicated continuous action head trained via diffusion or flow matching. However, such heads rely on iterative multistep sampling, for example 10 Euler steps in** _π_ 0 _._ 5 **. This creates an inference bottleneck that produces stop-and-go movement in the robot and slower task completion. We introduce IMLEVLA, which replaces the iterative action head with a singlestep conditional generator trained via conditional Implicit Maximum Likelihood Estimation (cIMLE). The cIMLE objective promotes multimodal action coverage, avoiding the mode collapse of naive regression heads while eliminating multistep sampling entirely. When IMLE-VLA is applied to** _π_ 0 _._ 5 **, it increases inference frequency** 3 _._ 67 _×_ **(** 55 **Hz vs.** 15 **Hz), enabling up to** 11 _×_ **higher action throughput. On the 40-task LIBERO benchmark, IMLE-VLA achieves the highest average success rate (** 98 _._ 0% **) among all baselines while leading in inference frequency. Under the test-time perturbations of LIBERO-plus, IMLE-VLA retains** _π_ 0 _._ 5 **’s robustness while other baselines degrade sharply, confirming that the cIMLE head preserves generalization. Real-world experiments on a Franka Emika Panda across four tasks demonstrate smoother motion (** 2 _._ 2 _×_ **–** 3 _._ 0 _×_ **lower jerk) and faster task completion, with IMLE-VLA outperforming** _π_ 0 _._ 5 **on every task and reducing average VLA inference time per episode by** 3 _._ 9 _×_ **–** 6 _._ 6 _×_ **. Videos and code are available at https://kianhk6.github.io/IMLE-VLA/.** 

I. INTRODUCTION 

Vision-language-action (VLA) policies build on pretrained vision-language models (VLMs), inheriting internet-scale visual and linguistic knowledge that enables strong generalization across tasks and embodiments [1]–[4], making them the dominant generalist paradigm in robot learning. However, this generalization comes at a steep computational cost. Large vision-language backbones combined with iterative action-sampling procedures make VLA inference a critical bottleneck for high-frequency real-time robot control [5]– [12]. The resulting latency introduces dead time in the control loop: under synchronous execution, the robot stalls until the next prediction is ready, producing stop-and-go execution and longer task completion times. 

This bottleneck primarily stems from the way VLAs generate actions, which follows one of two dominant paradigms: autoregressive decoding of discrete tokens and multi-step sampling of continuous actions. Autoregressive VLAs represent each action as a sequence of discrete tokens and decode them one at a time [2]–[4]. Furthermore, their reliance on discrete tokenization can limit the fine-grained continuous precision needed for dexterous manipulation [13], [14]. The second class generates continuous actions through multistep sampling with diffusion or flow matching, typically 

via an action expert attached to a VLM backbone such as _π_ 0 _._ 5 [14]. Here the model predicts a chunk of future actions together, yet producing each chunk still requires multiple sequential forward passes (e.g., 10 Euler steps) [13]–[18]. Consequently, action generation remains a primary bottleneck for real-time control. 

One of the key motivations for diffusion and flowmatching action heads is their capacity to handle the inherent multimodality of robot action distributions [13], [14]. A single instruction such as “clear the table” can be executed through many valid action sequences, and these models aim to capture this complexity. A naive solution would be to eliminate sequential generation via a single-step regression head. However, such models are prone to _mode collapse_ [13], [19], [20]: the regression objective averages over valid modes, pulling the prediction toward a single mean behavior that degrades task performance when the action distribution is multimodal. We empirically validate this effect in Sec. IV-C. 

This tension between expressivity and efficiency raises a central question: _can a single-step generator with a modecovering objective replace iterative action generation while improving task performance?_ 

In this work, we introduce **IMLE-VLA** , a single-step action generation framework for VLAs that replaces multistep sampling with a conditional Implicit Maximum Likelihood Estimation (cIMLE) [21]–[25] objective that explicitly optimizes for mode coverage. 

We instantiate IMLE-VLA by replacing the 10-step flowmatching action head of _π_ 0 _._ 5 [14] with our single-step generator. As the modification is confined to the action head, the full VLM backbone is preserved unchanged. This yields a 3 _._ 67 _×_ increase in inference frequency (55 Hz vs. 15 Hz). Combined with an extended execution horizon _H_ , which lets the policy replan less frequently, this compounds into up to 11 _._ 0 _×_ higher action throughput (inference frequency _× H_ ) [6]–[8], [11], [12]. This directly targets the “stop-and-go” control paradigm [3], [4], [6], [13]–[15], [26] that high VLA latency imposes: the robot idles while the model computes, producing visible pauses and stuttering motion. By cutting the time the robot waits on inference, IMLE-VLA reduces these pauses and reacts faster in dynamic settings, leading to faster task completion. 

We evaluate IMLE-VLA in both simulation and the real world. On the **LIBERO simulation benchmark** [27] (40 tabletop manipulation tasks across four suites), IMLE-VLA achieves the highest average success rate (98 _._ 0%) among all compared methods. To probe whether these gains hold under distribution shift, we further evaluate IMLE-VLA on **LIBERO-plus** [28], which applies systematic test-time perturbations to the LIBERO tasks. Under these conditions, IMLE-VLA retains _π_ 0 _._ 5’s robustness while all other baselines degrade sharply. In a **real-world setting** with a Franka Emika Panda, we test four tasks spanning single-step manipulation, multi-stage sequential reasoning, and reactivity to a dynamic environment. IMLE-VLA outperforms _π_ 0 _._ 5 on every task while producing measurably smoother motion, reducing proprioceptive jerk by 2 _._ 2 _×_ –3 _._ 0 _×_ . Across both 

settings, we measure the wall-clock time spent on VLA forward passes per episode, excluding robot execution and all other non-inference overhead. IMLE-VLA reduces this by up to 10 _._ 5 _×_ in simulation and up to 6 _._ 6 _×_ on the real robot. 

## II. RELATED WORK 

Our work targets the sequential action-generation bottleneck in generalist VLAs. We first review complementary systemlevel optimization strategies, and then review distillation and teacher-free single-step methods. 

**System-level optimizations.** Recent work [12] uses hardware-specific kernel tuning to accelerate inference, yet latency remains bounded by the sequential steps of diffusionbased heads. IMLE-VLA eliminates this bottleneck via single-step generation. These system-level gains are complementary to our algorithmic approach; by leveraging their efficient Triton kernels, we further amplify our inference frequency as demonstrated in Sec. IV. 

**Distillation methods.** One line of work accelerates VLAs by training a faster _student_ to imitate a pretrained _teacher_ , which ties the student’s behavior to the teacher’s output distribution. Shallow- _π_ [7] distills _π_ 0 _._ 5 into a shallower, lower-capacity student, and the resulting speedup comes at a measurable cost in success rate relative to the teacher (Sec. IV). A separate thread distills a single-step student from a multi-step teacher [29]–[31], leaving the student with the biases of the teacher’s iterative sampler. Unlike distillationbased accelerators, IMLE-VLA’s action head has no teacher: it is fit directly to expert actions under a cIMLE objective. Its outputs are therefore not capped by a teacher’s performance, nor shaped by an iterative sampler’s biases. 

**Teacher-free single-step methods.** A separate line of work sidesteps the teacher entirely, learning single-step action generation directly from expert data. Among VLAs, the prominent example is OpenVLA-OFT [8], which replaces the autoregressive decoding of OpenVLA with an L1 regression head. L1 regression is known to collapse to the conditional median under multimodal action distributions [13], [19], [20], and OpenVLA-OFT attributes L1’s viability to the capacity of OpenVLA’s 7B backbone [8]. This reliance on a 7B backbone leaves OpenVLA-OFT 5 _._ 3 _×_ slower than IMLE-VLA despite IMLE-VLA’s smaller 3B backbone (Table II). Yet this backbone scale does not confer robustness under distribution shift: on LIBERO-plus, OpenVLA-OFT’s success rate degrades sharply under test-time perturbations (Fig. 2). IMLE-VLA, by contrast, remains robust under these perturbations, despite its smaller 3B backbone. 

**From specialists to a generalist.** Across both lines of work above, prior efforts at single-step multimodal action generation have largely been confined to specialist policies [29], [30], [32], task-specific models that require expensive retraining and data collection for every new setting. Even in these narrow domains, mitigating mode collapse requires complex auxiliary regularizers that encourage distribution coverage [33], [34]. The cIMLE objective [21] instead enforces mode coverage _by construction_ , but its application 

in robotics has been limited to specialist regimes [31], [35]– [37] and thus inherits the same generalization bottleneck. IMLE-VLA is the first to adapt cIMLE to VLAs, achieving single-step action generation in a generalist policy that leverages internet-scale vision-language pretraining to generalize across tasks and embodiments. 

## III. METHOD 

We present **IMLE-VLA** , a framework for single-step, multimodal action generation in vision-language-action (VLA) policies. Our approach eliminates the computational bottleneck of multi-step iterative steps by training the action head with a conditional Implicit Maximum Likelihood Estimation (cIMLE) objective. Below, we detail our architectural framework and the mathematical formulation of cIMLE. Specifically, we first describe the coupling of a frozen VLM backbone with a lightweight, single-step action generator (III-A); then, we formalize the cIMLE training objective and its unique properties for modeling multimodal robotic behaviors (III-B). 

## _A. Single-Step VLA Architecture_ 

We operate within the VLA paradigm by coupling a highcapacity, frozen VLM backbone with a lightweight action head [13]–[15], [17]. By fixing the VLM parameters, we retain the robust spatial and semantic features acquired during internet-scale pretraining. Since the VLM constitutes the vast majority of model parameters and remains frozen, training reduces to the action head alone, keeping the cost minimal. 

At each timestep _t_ , the observation _ot_ consists of the visual inputs and language instruction. The VLM encodes it into a set of latent embeddings _f_ VLM( _ot_ ), which condition the action generation process. Unlike standard iterative methods such as diffusion or flow-matching, which require multiple sequential denoising steps, our approach uses a single-step conditional generator _Gθ_ . This generator directly maps Gaussian noise to multimodal action chunks, effectively mitigating a significant latency contributor in iterative VLA inference. 

Formally, we represent the generator output as an action chunk _A ∈_ R<sup>_C×D_</sup> , where _C_ denotes the prediction horizon and _D_ is the action-space dimensionality. To generate a candidate, we sample a latent noise vector _z ∼N_ (0 _,_ **I** ) of the same dimensionality as _A_ . The generator _Gθ_ then maps the VLM embedding _f_ VLM( _ot_ ) and noise _z_ to a complete action chunk in a single forward pass: 


By sampling different latent vectors _z_ , _Gθ_ can produce diverse action chunk candidates that capture the underlying conditional distribution _p_ ( _A | ot_ ). This stochasticity ensures the model avoids regressing to a single average outcome, preserving the expressivity required for complex behaviors. We initialize _Gθ_ from a pretrained _π_ 0 _._ 5 checkpoint and finetune the action head using the cIMLE objective (III-B) while the VLM backbone remains frozen. 

## _B. Conditional IMLE (cIMLE)_ 

The pretrained _π_ 0 _._ 5 action head is trained via Conditional Flow Matching (CFM) [13], [38], which necessitates the numerical integration of a learned velocity field during inference. In practice, this requires multiple sequential forward passes, typically 10 Euler steps, to generate a single action chunk, introducing a considerable inference-time integration bottleneck. 

To eliminate this bottleneck, we seek to generate each action chunk in a single forward pass without sacrificing the multimodality of the action distribution. As discussed in Sec. I, a single instruction can be executed through many valid action sequences, and each of these behaviors is a distinct mode of the conditional action distribution _p_ ( _A | ot_ ). Although each training pair ( _o_<sup>(</sup> _t_<sup>_i_)</sup><sup>_, A_(</sup> gt<sup>_i_))capturesonlyoneof</sup> these behaviors, the data contains observations that are very similar yet correspond to very different ground-truth actions. To preserve this multimodality, a faster action head must therefore remain capable of assigning different actions to the same observation. The conditional IMLE (cIMLE) objective [21] achieves exactly this: it reformulates action generation as a _singlestep_ mapping that transforms latent noise directly into action chunks, eliminating the iterative sampling cost while retaining the expressivity of the underlying distribution. Given a training set _{_ ( _o_<sup>(</sup> _t_<sup>_i_)</sup><sup>_, A_(</sup> gt<sup>_i_))</sup><sup>_}_</sup> _i_<sup>_n_</sup> =1<sup>,foreachdatapoint</sup> _i_ we draw _m_ (the _sample factor_ ) independent noise vectors _{zi,_ 1 _, . . . , zi,m}_ and generate a set of _m_ candidate action chunks _{A_<sup>ˆ</sup> _i,j}_<sup>_m_</sup> _j_ =1<sup>,conditionedonthecorrespondingVLM</sup> embedding _f_ VLM( _o_<sup>(</sup> _t_<sup>_i_)):</sup> _A_ ˆ _i,j_ = _Gθ f_ VLM( _o_<sup>(</sup> _t_<sup>_i_))</sup><sup>_,zi,j_</sup> _, j_ = 1 _, . . . , m._ (2) � � 

The cIMLE training procedure proceeds in two alternating steps. First, we perform a gradient-free **assignment step** where, for each ground-truth action _A_<sup>(</sup> gt<sup>_i_),weidentifyits</sup> nearest neighbour among its _m_ candidates generated from the same observation _o_<sup>(</sup> _t_<sup>_i_)</sup> (see Eq. 2): 


Next, in the **update step** , we minimize the distance between each ground-truth action and its assigned nearest neighbour: 


To see why this objective preserves multimodality, consider two illustrative regimes for the sample factor _m_ : one with _m_ =1, and another with _m >_ 1. Setting _m_ = 1 makes the nearest-neighbour selection _j_<sup>_∗_</sup> ( _i_ ) trivial, reducing Eq. 4 to plain L2 regression. However, it is well-known that this objective is optimized by regression to the mean: 


IV. EXPERIMENTS 

In effect, even when there are multiple correct actions for a given observation, this model is still optimized by averaging the multiple correct actions into one. Yet this average can lie between the modes, typically matching none of the demonstrated behaviors, making it an invalid action. 

The assignment step in Eq. 3 is what changes this. With _m >_ 1 candidates, each ground-truth action is matched to only its nearest candidate, allowing the other candidates to cover other modes without penalty by the cIMLE objective. Together, the outer sum ensures every mode is covered, while the nearest-neighbour assignment lets the generator map different latent codes _z_ to different modes rather than collapsing them into a single averaged action. 

**Algorithm 1** cIMLE Training **Input:** Training batch _{_ ( _o_<sup>(</sup> _t_<sup>_i_)</sup><sup>_, A_(</sup> gt<sup>_i_))</sup><sup>_}_</sup> _i_<sup>_B_</sup> =1<sup>,numberof</sup> samples _m_ , frozen VLM _f_ VLM, action head _Gθ_ **Output:** Updated parameters _θ_ 

// _Preprocessing: Compute VLM embeddings once per batch_ Compute _f_ VLM( _o_<sup>(</sup> _t_<sup>_i_))onceforall</sup><sup>_i ∈_[</sup><sup>_B_]</sup> // **Step 1: Efficient Nearest Neighbour Search (Gradient-free) for** _i_ = 1 **to** _B_ **do** Sample _m_ noise vectors _{zi,j}_<sup>_m_</sup> _j_ =1<sup>_∼N_(0</sup><sup>_, I_)</sup> Generate _m_ candidates _A_<sup>ˆ</sup> _i,j_ = _Gθ_ ( _f_ VLM( _o_<sup>(</sup> _t_<sup>_i_))</sup><sup>_, zi,j_),</sup> _j ∈_ [ _m_ ] _j_<sup>_∗_</sup> ( _i_ ) _←_ arg min _j∈_ [ _m_ ] _∥A_<sup>ˆ</sup> _i,j − A_<sup>(</sup> gt<sup>_i_)</sup><sup>_∥_</sup> 2<sup>2</sup> **end for** 

// **Step 2: Training via Assigned Nearest Neighbours** _A_ ˆ<sup>_∗_</sup> _i_<sup>_←Gθ_(</sup><sup>_f_VLM(</sup><sup>_o_(</sup> _t_<sup>_i_))</sup><sup>_,z_</sup> _i, j_<sup>_∗_</sup> ( _i_ )<sup>)forall</sup><sup>_i ∈_[</sup><sup>_B_]</sup> _▷ With gradients L ← B_<sup><u>1</u></sup> � _Bi_ =1<sup>_∥A_ˆ</sup> _i_<sup>_∗−A_(</sup> gt<sup>_i_)</sup><sup>_∥_</sup> 2<sup>2</sup> _θ ← θ − η ∇θL ▷ Update action head only_ 

As detailed in Algorithm 1, this procedure adds negligible training overhead. While the training procedure is presented sequentially for conceptual clarity, the assignment step (Step 1) is implemented in parallel across both the batch and the _m_ samples, making it highly efficient. In practice, we find that _m_ =2 strikes an effective balance between expressivity and computational efficiency; we ablate this choice in Sec. IV-C. The VLM embedding _f_ VLM( _o_<sup>(</sup> _t_<sup>_i_)) is computed once per sam-</sup> ple and shared across all _m_ candidates, avoiding redundant backbone passes. Furthermore, the selection of _j_<sup>_∗_</sup> ( _i_ ) is performed without gradient tracking; only the winning candidate is recomputed for the backward pass. Consequently, cIMLE acts as a lightweight objective that transforms a multistep VLA into a highly efficient single-step generator while explicitly optimizing for mode coverage, yielding substantial gains in inference frequency without sacrificing the policy’s capacity to handle complex, multimodal tasks. 

In this section, we evaluate the effectiveness of IMLE-VLA through a comprehensive set of evaluations in simulation and on a real-world robot. Our goal is to demonstrate that singlestep action generation via cIMLE can achieve significant gains in inference frequency while maintaining or even improving the success rates of VLA policies. 

All experiments use a standard receding-horizon loop: the policy observes _ot_ , runs one forward pass to predict an action chunk (Sec. III-A), and the robot executes the first _H_ actions of that chunk _open-loop_ before observing again and repeating. Here _H_ is the _execution horizon_ , a fixed number of actions executed per forward pass, so a larger _H_ replans less often. We report three metrics: _task success rate_ , our primary measure of policy quality; _action throughput_ , the number of executable actions delivered to the robot per second, equal to inference frequency _× H_ ; and _VLA-only wall-clock_ (VLAWC), the total time spent exclusively on VLA forward passes per successful episode, excluding robot execution and other non-inference overhead. 

We benchmark IMLE-VLA against the _π_ 0 _._ 5 flow-matching baseline across four primary axes: 

- (i) Inference frequency, where we characterize raw inference frequency and action throughput; 

- (ii) Simulated performance on the LIBERO benchmark, comprising 40 diverse manipulation tasks; 

- (iii) Robustness under test-time distribution shift, evaluated on LIBERO-plus; 

- (iv) Real-world experiments on four tasks assessing singlestep manipulation, multi-step reasoning and reactivity; 

## _A. Inference frequency_ 

Deployment on physical robots imposes strict constraints on _inference frequency_ : the number of VLA forward passes completed per second, directly governing the replanning rate. Higher inference frequency enables tighter control loops, smoother motion and faster response to new visual stimuli. 

We benchmark efficiency on a single NVIDIA L40S GPU using natural task-specific language prompts and the standard two-view image inputs. Our protocol reflects deploymentrealistic conditions: unlike prior benchmarks using empty prompts or static buffers [12], we include the mandatory cost of tokenizing the language instruction and proprioceptive state at every forward call. 

Table I compares IMLE-VLA against several optimized implementations of the _π_ 0 _._ 5 [14] VLA. The canonical JAX implementation runs at 15 Hz. Porting to PyTorch with torch.compile [39] and dedicated Triton kernels [12] yield modest gains, reaching 20 and 25 Hz respectively. This is because the bottleneck is algorithmic: the 10-step flowmatching loop imposes a fundamental ceiling that systemlevel optimizations alone cannot overcome. High latency is particularly impactful in physical deployments, where slow inference cycles manifest as noticeable “stop-and-go” pauses and reduced reactivity to environmental changes (see Sec. IVD for concrete examples). 

IMLE-VLA sidesteps this bottleneck by replacing the iterative action head with a single-step conditional generator while maintaining the exact same VLM backbone architecture. This yields an inference frequency of 55 Hz, a 3 _._ 67 _×_ increase over the canonical JAX baseline, in turn enabling smoother robotic motion and more responsive control without reducing model capacity or backbone scale. 

|**System**<br>**Inf. Freq. (Hz)** _↑_|**Inf. Freq. (**_×_**)** _↑_|
|---|---|
|_π_0_._5 (original JAX)<br>15|1_._00_×_|
|PyTorch + compile<br>20|1_._33_×_|
|Triton<br>25|1_._67_×_|
|**IMLE-VLA** (Ours)<br>**55**|**3.67**_×_|


TABLE I: **Inference frequency** measured on an NVIDIA L40S, the number of VLA forward passes per second, averaged over 50 episodes across 10 LIBERO-Long tasks. IMLE-VLA achieves 55 Hz, a 3 _._ 67 _×_ increase. 

## _B. Simulation: LIBERO Benchmark_ 

We next characterize the trade-off between inference frequency and task success on the LIBERO benchmark [27], which comprises 40 tabletop manipulation tasks across four suites (Spatial, Object, Goal, and Long) with a Franka Emika Panda arm. Each suite contains 10 tasks; every task is evaluated over 50 episodes following the standard protocol. 

**Success rate comparison.** Table II compares IMLEVLA against iterative action heads [13], [14] and speed-up strategies surveyed in Sec. II. Inf. ( _×_ ) denotes the inferencefrequency ratio relative to _π_ 0 _._ 5 on matched hardware. We measure _π_ 0 _._ 5, IMLE-VLA, and OpenVLA-OFT ourselves on an L40S; ratios for the remaining baselines are taken from Jeon et al. [7], who measure on H100. 

With _H_ =10, IMLE-VLA achieves **98.0%** average success, the highest among all compared methods, while also leading in inference frequency at 3 _._ 67 _× π_ 0 _._ 5. The fastest competing accelerator, Shallow- _π_ 0 _._ 5-L6 (2 _._ 3 _×_ ), is still slower than IMLE-VLA and drops to 94.5% due to its reduced model capacity [7]. OpenVLA-OFT reaches 94.5% on the same unfiltered dataset and runs below _π_ 0 _._ 5 in inference frequency (0 _._ 69 _×_ ), reflecting the cost of its 7B-parameter backbone. IMLE-VLA is the only method that simultaneously leads in both success rate and inference frequency. 

**Robustness under distribution shift.** To verify that our gains generalize beyond LIBERO’s training distribution, we additionally evaluate on **LIBERO-plus** [28], which applies systematic test-time perturbations to the LIBERO tasks across four axes (background, robot initial state, language, layout) at five severity levels (L1–L5). Across all axes and severities, IMLE-VLA retains _π_ 0 _._ 5’s robustness, while all other baselines exhibit larger drops in success rate as severity increases (Fig. 2). Consistent with the L1-regression limitation discussed in Sec. II [8], OpenVLA-OFT’s success rate degrades sharply. IMLE-VLA’s cIMLE objective instead enforces mode coverage _by construction_ [21], avoiding this failure mode. 

**Action throughput.** Table III reports action throughput 

(inference frequency _× H_ ) across configurations. At _H_ =10, IMLE-VLA already delivers 3 _._ 67 _×_ more actions per second than the _π_ 0 _._ 5 baseline, purely from replacing the flowmatching head. At _H_ =30, the single-step inference advantage compounds with the longer horizon, yielding 11 _._ 0 _×_ higher throughput. 

**VLA-only wall-clock (VLA-WC).** Table IV reports VLAWC across horizons, averaged over successful LIBERO episodes. At _H_ =10 the number of forward passes per episode is nearly identical to _π_ 0 _._ 5, yet VLA-WC drops by 3 _._ 6 _×_ due to the lighter single-step action head. At _H_ =30 the forward-pass count itself falls by _∼_ 3 _×_ ; combined with the faster per-pass inference, this yields an overall 10 _._ 5 _×_ reduction. 


Fig. 2: **LIBERO-plus robustness under distribution shift.** Success across four perturbation dimensions, each at five difficulty levels (L1–L5). Unlike baselines, which degrade sharply as severity increases, IMLE-VLA matches _π_ 0 _._ 5’s robustness throughout. 

|**System**|_H_|**Action Throughput (Hz)**|**(**_×_**)**|
|---|---|---|---|
|_π_0_._5 (JAX)|10|150|1.00_×_|
|PyTorch + torch.compile|10|200|1.33_×_|
|Triton|10|250|1.67_×_|
|Ours|10|550|3.67_×_|
|Ours|30|1,650|11.00_×_|


TABLE III: **Action throughput** in LIBERO simulation, defined as inference frequency _×_ execution horizon _H_ . ( _×_ ) denotes the throughput ratio relative to _π_ 0 _._ 5 at _H_ =10. At _H_ =10, IMLE-VLA delivers 3 _._ 67 _×_ higher throughput purely from single-step generation; at _H_ =30 this compounds to 11 _._ 0 _×_ . 

|**System**|**Fwd. Passes **|**VLA-WC (s) **|**VLA-WC (**_×_**)**|
|---|---|---|---|
|_π_0_._5 (JAX, _H_=10)|15.4|1.03|1.0_×_|
|Ours (_H_=10)|15.5|0.28|3.6_×_|
|Ours (_H_=30)|5.4|0.10|10.5_×_|


TABLE IV: **VLA-only wall-clock (VLA-WC).** Wall-clock on VLA forward passes per successful episode (see Sec. IV). _Fwd. Passes_ : average forward passes per episode. At _H_ =10, IMLE-VLA reduces VLA-WC by 3 _._ 6 _×_ ; at _H_ =30 fewer passes compound with faster inference for 10 _._ 5 _×_ overall. 

## _C. Method Analysis_ 

**Horizon ablation.** Each replan cycle consists of one forward pass followed by _H_ open-loop actions. Because IMLEVLA’s forward pass is 3 _._ 67 _×_ faster, the saved inference 

|**Model**|_H_|**Spatial**|**Object**|**Goal**|**Long**|**Avg** _↑_|**Inf. (**_×_**)** _↑_|
|---|---|---|---|---|---|---|---|
|_π_0_._5 [14]|10|97.2|99.0|97.8|**96.0**|97.5|1.0|
|_π_0_._5 [14]|30|95.0|98.0|96.2|95.2|96.1|1.0|
|_π_0 [13]|–|96.8|98.8|95.8|85.2|94.2|1.12|
|OpenVLA-OFT [8]|–|95.2|94.2|95.2|93.2|94.5|0.69|
|CogVLA [40]|–|**99.0**|99.0|97.0|95.0|97.5|0.8|
|SmolVLA [41]|–|90.0|96.0|92.0|71.0|87.3|1.0|
|Shallow-_π_0_._5-L9 [7]|–|**99.0**|98.0|97.0|93.0|96.8|1.7|
|Shallow-_π_0_._5-L6 [7]|–|98.0|96.0|94.0|90.0|94.5|2.3|
|IMLE-VLA|10|98.0|**99.8**|**98.2**|**96.0**|**98.0**|**3.67**|
|IMLE-VLA|30|97.2|99.0|96.2|95.8|97.1|**3.67**|


TABLE II: **LIBERO benchmark.** Success rates (SR, %) on four LIBERO suites (50 episodes per task) and their average. _H_ denotes the execution horizon (actions executed open-loop per forward pass; “–” = not specified). Inf. ( _×_ ) is the inference frequency ratio relative to _π_ 0 _._ 5. Best in **bold** , second-best <u>underlined.</u> IMLE-VLA achieves the highest average success rate (98 _._ 0% at _H_ =10) while simultaneously leading in inference frequency (3 _._ 67 _×_ ). 

time can be reinvested into a longer horizon without exceeding _π_ 0 _._ 5’s cycle time, making larger horizons practical. However, extending _H_ still trades _reactivity_ for _throughput_ : the robot executes more actions before conditioning on a new observation. Figure 3 reports IMLE-VLA’s average LIBERO success across all four suites at varying horizons. At _H_ =10 the policy achieves 98.0% average success, and performance degrades gradually as _H_ grows. _H_ =30 offers the best throughput–accuracy balance, still reaching 97.1% while delivering 11 _._ 0 _×_ higher action throughput (Table III), and outperforming _π_ 0 _._ 5 at the same horizon (96.1%). 


Fig. 3: **LIBERO horizon ablation.** IMLE-VLA success averaged across all four LIBERO suites at varying execution horizons. _H_ =10 achieves 98.0%; larger horizons reduce reactivity and degrade success, while _H_ =30 offers the best throughput–accuracy balance. 

**cIMLE sample factor ablation.** The sample factor _m_ controls how many candidate action chunks are generated per training example during the cIMLE assignment step (Eq. 2). When _m_ =1 only one candidate exists, so the assignment is trivial and cIMLE reduces to standard L2 regression with no mode-covering guarantee. 

Figure 4 reports LIBERO success across all four suites at _H_ =10 for _m ∈{_ 1 _,_ 2 _,_ 5 _}_ . Setting _m_ =1 produces a clear performance drop, confirming that a pure regression objective is insufficient for modeling complex action distributions, an observation consistent with the limitation acknowledged by OpenVLA-OFT [8] (see Sec. II). With _m_ =2 the mode-covering property activates and performance recovers substantially; increasing to _m_ =5 yields nearly iden- 

tical results, indicating diminishing returns. We therefore use _m_ =2 throughout, as it achieves strong performance while minimizing the per-step training cost of generating additional candidates. 


Fig. 4: **cIMLE sample factor ablation.** LIBERO success averaged across all four suites at _H_ =10 for varying sample factor _m_ . _m_ =1 reduces cIMLE to standard regression (no mode-covering) and drops sharply; _m_ =2 and _m_ =5 are nearly identical, so we use _m_ =2. 

## _D. Real-world experiments_ 

We evaluate IMLE-VLA against the _π_ 0 _._ 5 baseline (canonical JAX implementation) on a Franka Emika Panda robot with an NVIDIA A6000 GPU, using two camera views (wrist and scene). Both policies are trained on DROID [42] and deployed zero-shot on four tabletop manipulation tasks (Figure 5), with success (task completion) reported over 20 episodes per task. _π_ 0 _._ 5 runs at 15 Hz control frequency, while IMLE-VLA operates at 55 Hz. Unlike LIBERO’s deterministic contact dynamics, real-world manipulation introduces physical uncertainty (e.g. grasp slippage, surface friction variation), requiring more frequent replanning. We adopt the _π_ 0 _._ 5 default horizon ( _H_ =8) and extend IMLE-VLA to _H_ =12, since the faster inference compensates for the longer horizon while still yielding a shorter wall-clock replan interval than _π_ 0 _._ 5. IMLE-VLA outperforms _π_ 0 _._ 5 in every task while reducing the VLA-only wall-clock by 3 _._ 9 _×_ –6 _._ 6 _×_ (Table V) and completing episodes approximately 2 _×_ faster end-to-end (supplementary videos). The four tasks span single-step manipulation, multi-stage sequential reasoning, 


Fig. 5: **Real-world experiments.** We evaluate on three categories: **Single-Step Manipulation** , **Multi-Step Sequential Reasoning** and **Dynamic Reactivity** . IMLE-VLA generates faster, smoother, and more successful actions across all three categories. 

||**Succe**|**ss** _↑_|**VLA-**|**WC (s)** _↓_||
|---|---|---|---|---|---|
|**Task**|**Ours**|_π_0_._5|**Ours**|_π_0_._5|**Jerk (**_×_**)**|
|Pineapple in bowl|19|15|18.56|123|2_._7_×_|
|Swap pineapple & cube|18|15|31.1|178.3|2_._2_×_|
|Pineapple in cabinet|15|12|99.4|389.4|3_._0_×_|
|Pineapple on moving plate|16|12|16.7|89.5|2_._7_×_|


TABLE V: **Real-world experiment results** on a Franka Emika Panda with an NVIDIA A6000 (20 episodes per task). Success: successful episodes out of 20. VLA-WC: wall-clock on VLA forward passes per successful episode, averaged over successful episodes per task. Jerk ( _×_ ): ratio of _π_ 0 _._ 5’s mean proprioceptive jerk to ours (higher means smoother motion relative to the baseline; see Sec. IV-D). IMLE-VLA outperforms _π_ 0 _._ 5 on every task, reduces VLA-WC by 3 _._ 9 _×_ – 6 _._ 6 _×_ , and produces 2 _._ 2 _×_ –3 _._ 0 _×_ lower jerk. 

and reactivity to a dynamic environment. 

- **Pineapple in bowl** (single-step): the robot grasps a squishy pineapple toy from the table and places it into a bowl. 

- **Swap pineapple and cube** (multi-step): a bowl contains a squishy pineapple with a red cube beside it. The robot must remove the pineapple from the bowl, then place the red cube inside. 

- **Put pineapple in cabinet** (multi-step): a cabinet door is already open with a squishy pineapple in front of it. The robot must pick up the pineapple, place it inside the cabinet, and close the door. 

- **Pineapple on moving plate** (reactive): a remotecontrolled car drives an attached plate across the table; the robot must place the pineapple on the moving plate, requiring continuous target adjustment. 

**Motion quality.** IMLE-VLA produces markedly smoother motion than _π_ 0 _._ 5: its faster inference minimizes the time the robot idles while the model computes, and its longer execution horizon means fewer replans, together eliminating the visible stop-wait-execute pauses and abrupt directional corrections that _π_ 0 _._ 5 exhibits at each replan. To quantify this, we measure _proprioceptive jerk_ , the third backward finite difference of the measured joint positions (7 arm joints, 

gripper excluded) normalized by _dt_<sup>3</sup> , averaged over joints and steps; IMLE-VLA reduces mean jerk by 2 _._ 2 _×_ –3 _._ 0 _×_ across all four tasks (Table V). The difference is apparent in the supplementary videos. On _swap pineapple and cube_ , _π_ 0 _._ 5 changes direction repeatedly before each placement, while IMLE-VLA follows a direct trajectory and finishes faster. The shorter replan interval also enables recovery when something goes wrong: on _pineapple in cabinet_ , when the pineapple slips from IMLE-VLA’s gripper during insertion, the robot quickly detects the failure and re-grasps. Meanwhile, _π_ 0 _._ 5’s slower replanning introduces frequent abrupt corrections that significantly slow task completion. 

**Reactive task.** The dynamic task ( _pineapple on moving plate_ ) evaluates the ability to react to a continuously changing environment. In this setting, IMLE-VLA significantly outperforms _π_ 0 _._ 5. Although IMLE-VLA executes a longer action horizon, its faster inference leads to a much shorter wall-clock replanning cycle. As a result, the policy effectively closes the perception–action loop more frequently in real time, allowing the robot to continuously track and adapt to the plate’s motion. 

This distinction is particularly important in dynamic scenes, where delays between perception and action quickly degrade performance. By minimizing idle time between replans, IMLE-VLA reduces the latency between observing the plate and responding to its updated position, enabling smoother interception and grasp attempts. In contrast, _π_ 0 _._ 5 replans more slowly and therefore acts on increasingly stale observations. By the time a new action sequence is generated, the plate has already moved, causing the robot to repeatedly reach toward outdated target locations and ultimately fail to complete the task. 

## V. CONCLUSION 

We presented **IMLE-VLA** , a framework that replaces the iterative flow-matching action head of VLAs with a singlestep conditional generator trained via the cIMLE objective. By eliminating multi-step sampling while explicitly optimizing for mode coverage, IMLE-VLA achieves a 3 _._ 67 _×_ increase in inference frequency and up to 11 _._ 0 _×_ higher action throughput over the _π_ 0 _._ 5 baseline. On the LIBERO benchmark, IMLE-VLA attains the highest average success rate (98.0%) among all compared methods while simultaneously leading in inference frequency. In real-world experiments on a Franka Emika Panda, the higher inference frequency produces smoother motion and reduces VLA-only wall-clock by 3 _._ 9 _×_ –6 _._ 6 _×_ , while outperforming _π_ 0 _._ 5 on every task. Because our approach modifies only the action head, it serves as a drop-in replacement for the iterative heads in existing VLAs, a promising direction toward even faster generalist robot policies. 

## ACKNOWLEDGMENT 

This research was enabled in part by NSERC, the Canada Foundation for Innovation, the Canada CIFAR AI Chairs program, the BC DRI Group and the Digital Research Alliance of Canada. The first author dedicates this work to the memory of his beloved grandfather. 

REFERENCES 

- [1] S. Reed _et al._ , “A generalist agent,” _ArXiv_ , vol. abs/2205.06175, 2022. [Online]. Available: https://api.semanticscholar.org/CorpusID: 248722148 

- [2] Open X-Embodiment Collaboration, “Open x-embodiment: Robotic learning datasets and rt-x models,” _ArXiv_ , vol. abs/2310.08864, 2023. [Online]. Available: https://api.semanticscholar.org/CorpusID: 264884565 

- [3] A. Brohan _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” _ArXiv_ , vol. abs/2307.15818, 2023. [Online]. Available: https://api.semanticscholar.org/CorpusID: 260293142 

- [4] M. J. Kim _et al._ , “Openvla: An open-source vision-language-action model,” _ArXiv_ , vol. abs/2406.09246, 2024. [Online]. Available: https://api.semanticscholar.org/CorpusID:270440391 

- [5] W. Jiang _et al._ , “How fast can i run my vla? demystifying vla inference performance with vla-perf,” _ArXiv_ , 2026. [Online]. Available: https://api.semanticscholar.org/CorpusID:285872613 

- [6] K. Pertsch _et al._ , “Fast: Efficient action tokenization for visionlanguage-action models,” in _Proc. Robotics: Science and Systems (RSS)_ , 2025, arXiv:2501.09747. [Online]. Available: https://api. semanticscholar.org/CorpusID:275570494 

- [7] B. Jeon _et al._ , “Shallow- _π_ : Knowledge distillation for flowbased vlas,” _ArXiv_ , vol. abs/2601.20262, 2026. [Online]. Available: https://api.semanticscholar.org/CorpusID:285102369 

- [8] M. J. Kim _et al._ , “Fine-tuning vision-language-action models: Optimizing speed and success,” _ArXiv_ , vol. abs/2502.19645, 2025. [Online]. Available: https://api.semanticscholar.org/CorpusID: 276647709 

- [9] J. Zhang _et al._ , “Quantvla: Scale-calibrated post-training quantization for vision-language-action models,” _ArXiv_ , 2026. [Online]. Available: https://api.semanticscholar.org/CorpusID:286001346 

- [10] Y. Chen _et al._ , “Rlrc: Reinforcement learning-based recovery for compressed vision-language-action models,” _ArXiv_ , vol. abs/2506.17639, 2025. [Online]. Available: https://api.semanticscholar. org/CorpusID:280000516 

- [11] Y. Jiang _et al._ , “Asyncvla: Asynchronous flow matching for visionlanguage-action models,” _ArXiv_ , vol. abs/2511.14148, 2025. [Online]. Available: https://api.semanticscholar.org/CorpusID:283080185 

- [12] Y. Ma _et al._ , “Running vlas at real-time speed,” _ArXiv_ , vol. abs/2510.26742, 2025. [Online]. Available: https://api.semanticscholar. org/CorpusID:282591986 

- [13] K. Black _et al._ , “ _π_ 0: A vision-language-action flow model for general robot control,” _ArXiv_ , vol. abs/2410.24164, 2024. [Online]. Available: https://api.semanticscholar.org/CorpusID:273811174 

- [14] Physical Intelligence _et al._ , “ _π_ 0.5: a vision-language-action model with open-world generalization,” _ArXiv_ , vol. abs/2504.16054, 2025. [Online]. Available: https://api.semanticscholar.org/CorpusID: 277993634 

- [15] Octo Model Team _et al._ , “Octo: An open-source generalist robot policy,” _ArXiv_ , vol. abs/2405.12213, 2024. [Online]. Available: https://api.semanticscholar.org/CorpusID:266379116 

- [16] S. Liu _et al._ , “Rdt-1b: a diffusion foundation model for bimanual manipulation,” _ArXiv_ , vol. abs/2410.07864, 2024. [Online]. Available: https://api.semanticscholar.org/CorpusID:273233386 

- [17] Q. Li _et al._ , “Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation,” _ArXiv_ , vol. abs/2411.19650, 2024. [Online]. Available: https: //api.semanticscholar.org/CorpusID:274423241 

- [18] L. Wang _et al._ , “Scaling proprioceptive-visual learning with heterogeneous pre-trained transformers,” _ArXiv_ , vol. abs/2409.20537, 2024. [Online]. Available: https://api.semanticscholar.org/CorpusID: 272986946 

- [19] C. Chi _et al._ , “Diffusion policy: Visuomotor policy learning via action diffusion,” _The International Journal of Robotics Research_ , vol. 44, pp. 1684 – 1704, 2023. [Online]. Available: https://api.semanticscholar.org/CorpusID:257378658 

- [20] N. M. M. Shafiullah _et al._ , “Behavior transformers: Cloning k modes with one stone,” _ArXiv_ , vol. abs/2206.11251, 2022. [Online]. Available: https://api.semanticscholar.org/CorpusID:249926747 

- [21] K. Li _et al._ , “Implicit maximum likelihood estimation,” _ArXiv_ , vol. abs/1809.09087, 2018. [Online]. Available: https://api.semanticscholar. org/CorpusID:52816401 

- [22] M. Aghabozorgi _et al._ , “Adaptive imle for few-shot pretraining-free generative modelling,” in _International Conference on Machine Learning_ , 2023. [Online]. Available: https://api.semanticscholar.org/ CorpusID:260810286 

- [23] S. Peng _et al._ , “Chimle: Conditional hierarchical imle for multimodal conditional image synthesis,” vol. abs/2211.14286, 2022. [Online]. Available: https://api.semanticscholar.org/CorpusID:254018031 

- [24] C. Vashist _et al._ , “Rejection sampling imle: Designing priors for better few-shot image synthesis,” in _European Conference on Computer Vision_ , 2024. [Online]. Available: https://api.semanticscholar.org/ CorpusID:272911336 

- [25] M. Aghabozorgi _et al._ , “Wimle: Uncertainty-aware world models with imle for sample-efficient continuous control,” _ArXiv_ , vol. abs/2602.14351, 2026. [Online]. Available: https://api.semanticscholar. org/CorpusID:285616888 

- [26] T. Zhao _et al._ , “Learning fine-grained bimanual manipulation with low-cost hardware,” _ArXiv_ , vol. abs/2304.13705, 2023. [Online]. Available: https://api.semanticscholar.org/CorpusID:258331658 

- [27] B. Liu _et al._ , “Libero: Benchmarking knowledge transfer for lifelong robot learning,” _ArXiv_ , vol. abs/2306.03310, 2023. [Online]. Available: https://api.semanticscholar.org/CorpusID:259089508 

- [28] S. Fei _et al._ , “Libero-plus: In-depth robustness analysis of visionlanguage-action models,” _arXiv preprint arXiv:2510.13626_ , 2025. 

- [29] A. Prasad _et al._ , “Consistency policy: Accelerated visuomotor policies via consistency distillation,” in _Proc. Robotics: Science and Systems (RSS)_ , 2024, arXiv:2405.07503. [Online]. Available: https://api.semanticscholar.org/CorpusID:269758119 

- [30] Z. Wang _et al._ , “One-step diffusion policy: Fast visuomotor policies via diffusion distillation,” _ArXiv_ , vol. abs/2410.21257, 2024. [Online]. Available: https://api.semanticscholar.org/CorpusID:273654186 

- [31] J. Dong _et al._ , “From flow to one step: Real-time multi-modal trajectory policies via implicit maximum likelihood estimation-based distribution distillation,” _ArXiv_ , vol. abs/2603.09415, 2026. [Online]. Available: https://api.semanticscholar.org/CorpusID:286429211 

- [32] K. Frans _et al._ , “One step diffusion via shortcut models,” _ArXiv_ , vol. abs/2410.12557, 2024. [Online]. Available: https: //api.semanticscholar.org/CorpusID:273375140 

- [33] G. Zou _et al._ , “Dm1: Meanflow with dispersive regularization for 1-step robotic manipulation,” _ArXiv_ , vol. abs/2510.07865, 2025. [Online]. Available: https://api.semanticscholar.org/CorpusID: 281950800 

- [34] ——, “One step is enough: Dispersive meanflow policy optimization,” _ArXiv_ , vol. abs/2601.20701, 2026. [Online]. Available: https: //api.semanticscholar.org/CorpusID:285102124 

- [35] K. Rana _et al._ , “Imle policy: Fast and sample efficient visuomotor policy learning via implicit maximum likelihood estimation,” _ArXiv_ , vol. abs/2502.12371, 2025. [Online]. Available: https: //api.semanticscholar.org/CorpusID:276422212 

- [36] A. Bhaskar _et al._ , “Prism: Performer rs-imle for single-pass multisensory imitation learning,” _ArXiv_ , vol. abs/2602.02396, 2026. [Online]. Available: https://api.semanticscholar.org/CorpusID: 285271140 

- [37] G. Lee _et al._ , “Implicit maximum likelihood estimation for real-time generative model predictive control,” _ArXiv_ , vol. abs/2603.13733, 2026. [Online]. Available: https://api.semanticscholar.org/CorpusID: 286568748 

- [38] Y. Lipman _et al._ , “Flow matching for generative modeling,” _ArXiv_ , vol. abs/2210.02747, 2022. [Online]. Available: https: //api.semanticscholar.org/CorpusID:252734897 

- [39] R. Cad`ene _et al._ , “Lerobot: An open-source library for endto-end robot learning,” _ArXiv_ , 2026. [Online]. Available: https: //api.semanticscholar.org/CorpusID:286082457 

- [40] W. Li _et al._ , “Cogvla: Cognition-aligned vision-language-action model via instruction-driven routing & sparsification,” _ArXiv_ , vol. abs/2508.21046, 2025. [Online]. Available: https://api.semanticscholar. org/CorpusID:280949804 

- [41] M. Shukor _et al._ , “Smolvla: A vision-language-action model for affordable and efficient robotics,” _ArXiv_ , vol. abs/2506.01844, 2025. [Online]. Available: https://api.semanticscholar.org/CorpusID: 279119427 

- [42] A. Khazatsky _et al._ , “Droid: A large-scale in-the-wild robot manipulation dataset,” _ArXiv_ , vol. abs/2403.12945, 2024. [Online]. Available: https://api.semanticscholar.org/CorpusID:268531351 

