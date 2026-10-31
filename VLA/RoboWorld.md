---
title: "RoboWorld: Fast and Reliable Neural Simulators for Generalist Robot Policy Evaluation"
date: "2026-07-01"
authors: "Byeongguk Jeon; Seonghyeon Ye; JaeHyeok Doo; Sungdong Kim; Minjoon Seo; Hyungmok Son"
url: https://arxiv.org/abs/2607.01060
pdf: https://arxiv.org/pdf/2607.01060
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2607.01060)** / [論文ページ](https://arxiv.org/abs/2607.01060)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **RoboWorld: Fast and Reliable Neural Simulators for Generalist Robot Policy Evaluation** 

**Byeongguk Jeon**<sup>***,1,2**</sup> **Seonghyeon Ye**<sup>***,1**</sup> 

JaeHyeok Doo<sup>1</sup> Sungdong Kim<sup>1,2</sup> Minjoon Seo<sup>1,2</sup> Hyungmok Son<sup>2</sup> Kimin Lee<sup>1,2</sup> 

1KAIST 2Config *Equal contribution. 

Project Website: `https://byeongguks.github.io/RoboWorld/` 


Figure 1: **Overview of ROBOWORLD.** ROBOWORLD evaluates robot policies via closed-loop rollouts in a video world model scored by a task-progress-aware VLM judge, yielding rankings that strongly correlate with real-world evaluations. 

**Abstract:** Video world models are emerging as a scalable alternative for evaluating generalist robot policies, bypassing the physical constraints and engineering burdens of real-world deployment. However, evaluating policies with video world models remains challenging, as world-model errors can make generated rollouts unreliable and slow inference limits large-scale throughput. We introduce ROBOWORLD, an automated evaluation pipeline that pairs a fast autoregressive video world model with a task-progress-aware vision-language model scoring. To enable reliable long-horizon autoregressive world-model rollouts, we propose STEP FORCING, which combines anchored and one-step self-forwarded contexts to reduce train–test mismatch while preserving action–observation dynamics. Together, these components enable ROBOWORLD to align strongly with real-world robot evaluation across tasks and environments, achieving Pearson’s _r_ = 0 _._ 989 and Spearman’s _ρ_ = 0 _._ 970. 

**Keywords:** Robot Policy Evaluation, World Model 

## **1 Introduction** 

Reliable and accessible evaluation has significantly accelerated progress in foundation models for vision and language [1, 2, 3, 4]. Generalist robot policies, also referred to as Vision-Language-Action (VLA) models, have made rapid progress in generalizing across tasks, objects, and environments, requiring numerous rollouts across diverse conditions for reliable evaluation [5, 6, 7, 8, 9, 10, 11, 12]. 


Figure 2: **Left Upper:** STEP FORCING shares the noise schedule between training and inference. **(a)** Diffusion Forcing conditions on noisy ground-truth (red). **(b)** Self Forcing conditions on selfgenerated context (green) via repeated forward rollouts. **(c)** STEP FORCING conditions on the onestep self-forwarded prior (green) or anchor step (red). 

However, scaling robot policy evaluation in the real world remains challenging. Each rollout requires physical robots and human operators, limiting the number of policies and conditions that can be evaluated. Simulation-based evaluation [13, 14, 15, 16, 17, 18] avoids these costs but requires engineering for asset and environment setup, and sim-to-real gaps compromise its reliability [19, 20]. Recent efforts reduce human intervention [21] or automate real-to-sim environment construction [22, 23], but they still rely on physical robot setups or prior access to target environments. 

Built on pretrained video diffusion models [24, 25, 26, 27, 28, 29, 30, 31], video world models offer a scalable alternative for policy evaluation by enabling interactive closed-loop rollouts [32, 33, 34, 35, 36, 37, 38]. This property makes it possible to evaluate policies in new environments without physical robot setup or extensive simulator engineering. However, two challenges remain: (1) world-model artifacts can corrupt long-horizon rollouts, making evaluation unreliable, and (2) slow inference from iterative denoising processes reduces evaluation throughput. Especially, such artifacts propagate into evaluation outcomes when Vision-Language Model (VLM)-based scoring reduces each rollout to a binary success score [39, 40]. 

We introduce ROBOWORLD, a scalable automated evaluation pipeline that combines a fast autoregressive video world model with a task-progress-aware VLM judge. To make long-horizon actionconditioned rollouts both fast and reliable, we propose STEP FORCING. STEP FORCING trains the world model to predict clean frames from one-step self-forwarded priors under the same few-step denoising schedule used at inference. This alignment reduces the train–test context mismatch and improves few-step denoising quality. Furthermore, interleaving data-grounded anchor contexts ensures the model preserves strict action controllability. We train our world model on DROID [41] and test its ability to evaluate policies beyond its training environments by measuring the correlation with RoboArena [42], the largest real-world benchmark built on the DROID setup. Conditioned on the initial frame of each RoboArena episode, ROBOWORLD evaluates the same policies inside the world model and produces 4,186 video rollouts, achieving a Pearson correlation of 0 _._ 989 and a Spearman correlation of 0 _._ 970 with the original real-world leaderboard. 

## **2 Related Work** 

**Evaluation of Generalist Robot Policies** Evaluating generalist robot policies [5, 6, 7, 8, 9, 10, 11, 12] requires comparing policies across diverse tasks, objects, and environments [15, 42]. Recent real-world benchmarks improve scalability by distributing evaluation or reducing human intervention during reset and success detection [42, 21]. Nevertheless, real-world evaluation remains constrained by hardware availability, safety, human oversight, and physical access to evaluation environments [43]. Simulation benchmarks provide reproducible rollouts at scale, but require substantial engineering of assets, dynamics, and task environments, and remain limited by sim-to-real gaps [14, 15, 16, 17, 18, 44]. Recent real-to-sim approaches reduce this gap by reconstructing or 

2 

**Algorithm 1** STEP FORCING 

**Require:** Dataset _D_ of (video, action) pairs **Require:** Denoising schedule _{t_ 0 _, . . . , tS}_ with 0 = _t_ 0 _< · · · < tS_ = 1, where _S_ denotes the number of denoising steps. 

**Require:** Velocity network _vθ_ , number of frames _N_ , anchor probability _p_ 1: **repeat** 

- 2: Sample ( _x, a_ ) _∼D_ 3: Sample _k_<sup>_i_</sup> _∼U{_ 1 _, . . . , S}_ , _ϵ_<sup>_i_</sup> _∼N_ (0 _, I_ ) for _i ∈{_ 1 _, . . . , N }_ 4: _x_<sup>_i_</sup> _k_<sup>_i←tki ϵi_+ (1</sup><sup>_−tki_)</sup><sup>_xi{_noisy frames</sup><sup>_}_</sup> 5: _h_<sup>_i_</sup> _←{x_<sup>_j_</sup> _k_<sup>_j}j<i {_context frames</sup><sup>_}_</sup> 

6: With probability _p_ , set ∆ _t_<sup>_i_</sup> _←_ 0 _(anchor)_ ; otherwise ∆ _t_<sup>_i_</sup> _← tki − tki−_ 1 _(self-forward)_ 7: _t_ ˜<sup>_i_</sup> _← tki −_ ∆ _t_<sup>_i_</sup> _{_ actual noise level of prior _}_ 8: _x_ ˆ<sup>_i_</sup> _k_<sup>_i_</sup> _−_ 1<sup>_←xi_</sup> _k_<sup>_i−_∆</sup><sup>_ti ·_sg</sup> � _vθ_ ( _x_<sup>_i_</sup> _k_<sup>_i, tki, hi, ai_)</sup> � _{_ one-step self-forwarded prior _}_ 9: _h_ ˆ<sup>_i_</sup> _←{x_ ˆ<sup>_j_</sup> _k_<sup>_j_</sup> _−_ 1<sup>_}j<i {_self-forwarded context frames</sup><sup>_}_</sup> 10: _x_ ˆ<sup>_i_</sup> _← x_ ˆ<sup>_i_</sup> _k_<sup>_i_</sup> _−_ 1<sup>_−t_˜</sup><sup>_i vθ_(ˆ</sup><sup>_x_</sup> _k_<sup>_ii_</sup> _−_ 1<sup>_,_˜</sup><sup>_ti,_ˆ</sup><sup>_hi, ai_)</sup><sup>_{_clean prediction</sup><sup>_}_</sup> 11: Update _θ_ by descending _∇θ N_<sup><u>1</u></sup> � _Ni_ =1<sup>_∥xi −x_ˆ</sup><sup>_i∥_</sup> 2<sup>2</sup> 12: **until** converged 

translating real-world scenes into interactive simulation environments [22, 23, 45, 46], but still require real-scene access and an explicit simulation-building stage before evaluation. 

**Video World Models for Robotics** Video world models have recently been adopted in robotics for modeling future robot behavior across diverse tasks and environments [34, 35, 47, 48, 49, 50, 51]. These models have been used as neural simulators for action-conditioned prediction, planning, and policy rollout [52, 53, 54, 32, 33, 38, 55]. A closely related line of work explores video world models as proxies for policy evaluation by rolling out robot policies in generative models and automatically scoring the resulting rollouts [40, 56, 39, 57]. Despite this progress, slow inference limits evaluation scale, while world-model error can compound over long horizons and bias policy scores. Also, it remains underexplored how well video-world-model-based evaluation can reflect real-world policy rankings across diverse tasks and environments. 

## **3 STEP FORCING** 

In this section, we introduce STEP FORCING, a training method for fast and reliable actionconditioned long-horizon video generation in video world models. We begin with the autoregressive video world model (Section 3.1), then present STEP FORCING (Section 3.2), and finally use BAIR Robot Pushing [58] as a diagnostic setup (Section 3.3) to motivate our design choices. 

### **3.1 Preliminaries: Autoregressive video world model** 

Autoregressive video world models [59, 60, 61, 62, 63] factorize future observations _x_<sup>1:</sup><sup>_N_</sup> given an initial observation _x_<sup>0</sup> and action sequence _a_<sup>1:</sup><sup>_N_</sup> as _pθ_ ( _x_<sup>1:</sup><sup>_N_</sup> _| x_<sup>0</sup> _, a_<sup>1:</sup><sup>_N_</sup> ) =<sup>�</sup><sup>_N_</sup> _i_ =1<sup>_pθ_(</sup><sup>_xi| x_0:</sup><sup>_i−_1</sup><sup>_, ai_),</sup> enabling generation beyond the training horizon and efficient inference with key–value caching [64]. However, this leads to a train–test context mismatch, as the model is trained with clean or noised ground-truth contexts _x_<sup>_<i_</sup> , whereas inference conditions on self-generated predictions _x_ ˆ<sup>_<i_</sup> , causing errors to accumulate over long horizons. Training on self-generated contexts [65, 66] mitigates this context mismatch, but incurs substantial overhead from sequential autoregressive rollouts. Moreover, replacing _x_<sup>_<i_</sup> with _x_ ˆ<sup>_<i_</sup> shifts the state on which action _a_<sup>_i_</sup> acts; supervising _pθ_ ( _x_<sup>_i_</sup> _| x_ ˆ<sup>_<i_</sup> _, a_<sup>_i_</sup> ) thus introduces transitions inconsistent with the action-observation dynamics in the data. 

### **3.2 STEP FORCING: Mitigating Train-Test Gap through Self-Forwarded Prior Denoising** 

3 

We propose STEP FORCING, training the world model to denoise from one-step self-forwarded priors under a fixed discrete denoising schedule. We formulate denoising with rectified flow [67, 68], where a clean frame _x_<sup>_i_</sup> and noise _ϵ_<sup>_i_</sup> are connected by the linear path _x_<sup>_i_</sup> _t_<sup>=</sup><sup>_tϵi_+ (1</sup><sup>_−t_)</sup><sup>_xi_.We</sup> define the inference noise schedule 0 = _t_ 0 _< · · · < tS_ = 1 and use the same schedule for onestep self-forwarding during training. This schedule alignment reduces the train–test mismatch and enables efficient few-step denoising (e.g., _S_ = 4) without relying on distillation-based few-step samplers [64, 65]. 

Formally, given a video-action trajectory ( _x_<sup>0:</sup><sup>_N_</sup> _, a_<sup>1:</sup><sup>_N_</sup> ) _∼D_ and rectified-flow velocity _vθ_ [68], we form per-frame noisy latents _x_<sup>_i_</sup> _k_<sup>_i_fromindependentlysamplednoiselevels</sup><sup>_ki∼U{_1</sup><sup>_, . . . , S}_,</sup> following Diffusion Forcing [69]. Given the noisy context _h_<sup>_i_</sup> := _{x_<sup>_j_</sup> _k_<sup>_j}j<i_, we take a single Euler</sup> step under stop gradient to obtain a _self-forwarded prior_ : 


where the stop-gradient, sg[ _·_ ], prevents _vθ_ from being optimized to shape its own future inputs. Onestep self-forwarding mitigates the train-test gap by training the model to learn from its own imperfect generation. However, unlike self-generated contexts, it enables _parallel_ context generation, significantly reducing the training cost and enabling stable training. Also, to ground supervision in the data distribution, with probability _p_ we apply an _anchor step_ that bypasses self-forwarding and sets the prior directly to the noisy ground-truth latent, _x_ ˆ<sup>_i_</sup> _k_<sup>_i_</sup> _−_ 1<sup>=</sup><sup>_xi_</sup> _k_<sup>_i_.By preventing action-observation mis-</sup> match from self-generated context, anchor step preserves ground-truth dynamics, which is essential for action-conditioned video generation. We then predict the clean frame from _x_ ˆ<sup>_i_</sup> _k_<sup>_i_</sup> _−_ 1<sup>conditioned</sup> on the self-forwarded context _h_<sup>ˆ</sup><sup>_i_</sup> := _{x_ ˆ<sup>_j_</sup> _k_<sup>_j_</sup> _−_ 1<sup>_}j<i_, and minimize the squared error to</sup><sup>_xi_; the overall</sup> procedure is illustrated in Figure 2, while the full equations are provided in Algorithm 1. 

### **3.3 Diagnostic Comparison on BAIR Robot Pushing** 

We use BAIR Robot Pushing [58] as a small-scale diagnostic setup for comparing different training objectives in action-conditioned autoregressive world modeling. We examine whether each objective preserves action–observation dynamics while maintaining stable long-horizon rollouts. Specifically, we measure both in-horizon (ID) and extrapolation (OOD) frames. Experimental details are provided in Appendix A. 

STEP FORCING achieves the best SSIM [71] and LPIPS [72] in both windows (Table 1; Figure 3). More importantly, the baselines expose the failure modes motivating our design. Teacher Forcing preserves data-grounded transitions but suffers from error accumulation during long-horizon autoregressive rollout. Diffusion Forcing improves robustness to noisy contexts, but its generated rollouts can still drift over extrapolation horizons. Resampling Forcing and Self Forcing produce visually plausible videos by training on self-generated contexts, but this weakens action following because the same action is supervised from model-induced states rather than data-grounded states. In contrast, STEP FORCING reduces the train–test context gap through onestep self-forwarded priors while using anchor steps to preserve action–observation dynamics. 

|Method<br>Steps|SSI<br>ID|M_↑_<br>OOD|LPI<br>ID|PS_↓_<br>OOD|
|---|---|---|---|---|
|Teacher Forcing [70]<br>8|0.7942|0.7118|0.0554|0.1058|
|Diffusion Forcing [69]<br>8|0.7657|0.6861|0.0690|0.1117|
|Resampling Forcing [66]<br>8<br>|0.7891 <br>|0.6996<br>|0.0572 <br>|0.1082<br>|
|Self Forcing [65]<br>4|0.7929|0.6953|0.0548|0.1083|
|STEPFORCING<br>4|**0.8063 **|**0.7374**|**0.0525 **|**0.0768**|
|Table 1: Diagnostic|comp|arison|of a|ction-|
|conditioned training <br>ing.|on BA|IR R|obot|Push-|


Figure 3: STEP FORCING shows strong action controllability while maintaining visual quality throughout the whole horizon. 

4 

## **4 ROBOWORLD** 

We present ROBOWORLD, a fully automated evaluation pipeline for generalist robot policies that scales across diverse environments without requiring physical rollouts or human intervention. ROBOWORLD consists of two components: (1) a fast autoregressive video world model trained with STEP FORCING, and (2) a task-progress-aware VLM judge that scores the generated rollouts. 

### **4.1 Adapting Pretrained Video Models into Fast Autoregressive World Models** 

To adapt pretrained bidirectional video models into fast autoregressive video world models, we make three architectural and training modifications: (1) we replace bidirectional attention with framelevel causal attention, (2) we encode actions with a two-layer MLP and inject them into each frame through cross-attention, and (3) we use per-frame independent noise scheduling during training [69]. We first train the model with rectified flow matching [67] under the Diffusion Forcing scheme [69], converting the bidirectional video model into an autoregressive video world model. We then apply STEP FORCING to enable stable long-horizon autoregressive rollouts with few-step inference. During inference, we evaluate the policy in a closed loop within the world model. At each step, the policy predicts an action given the current observation, and the world model generates the next observation conditioned on the past context and the predicted action. This generated observation is then fed back to the policy to predict the subsequent action. To accelerate this autoregressive decoding, following prior video diffusion models [73, 74, 65, 64], we use key–value (KV) caching with a sliding window context. 

### **4.2 Automatically Scoring Rollouts from World Models** 

After the world model generates action-conditioned rollouts, a scoring model is needed to evaluate the policy performance conditioned on the rollout. Previous works rely on a VLM that generates a binary score given the generated rollout [39, 40]. However, a binary success metric conflates policy failures with world model artifacts. For example, when a policy picks up the correct object but fails to place it due to world model error (object disappearance), a binary scorer would evaluate the trajectory as a failure. Instead, we introduce a task-progress-aware evaluation using a predefined 0–5 rubric prompted to a VLM judge. To reliably disentangle true policy failures from world-model artifacts, we instruct the VLM to isolate world-model error detection to the wrist view—where physical inconsistencies predominantly manifest—while assessing actual task progress strictly through the fixed external views. This multi-view evaluation strategy allows us to allocate partial scores reflecting the policy’s valid progress before the world-model corruption. Unlike binary metrics, this approach fairly credits policy capabilities under imperfect world-model rollouts. We provide the full VLM prompts and rubric definitions in Appendix B. 

## **5 Experiments** 

We investigate whether ROBOWORLD can serve as a substitute for real-world evaluations of generalist robot policies. We train our video world model on DROID [41], a large-scale real-world robot manipulation dataset, and evaluate on RoboArena [42] trajectories. First, we compare our world model trained with STEP FORCING against other video world model baselines on long-horizon RoboArena trajectories. We then measure the correlation between ROBOWORLD and real-world evaluations by applying ROBOWORLD to the initial observations from RoboArena evaluation episodes.<sup>1</sup> 

### **5.1 Experimental Details** 

We initialize the video world model from Wan2.1-T2V-1.3B [31]. Following prior multi-view video generation setups [49, 48], we concatenate DROID’s three camera views (two fixed views and one 

> 1We evaluate the 8 policies that were open-sourced as of the latest RoboArena data dump used in our experiments (Feb. 3, 2026). 

5 


Figure 4: Long-horizon action-conditioned video generation on RoboArena. Quality (SSIM, LPIPS, FVD) vs. FPS. Baseline markers sweep denoising steps _∈{_ 50, 32, 16, 8, 4 _}_ . STEP FORCING achieves the best LPIPS at the highest FPS (15.3), and matches the baselines that run substantially slower on SSIM and FVD. 

wrist-mounted view) into a 2 _×_ 2 grid and treat it as a single multi-view frame. We condition the model on end-effector Cartesian position [75, 32]; for joint-velocity policies, we use a shallow action adapter to map policy actions into this conditioning space [32]. We train for 160k Diffusion Forcing steps followed by 40k STEP FORCING steps, using 45-frame clips, a learning rate of 1 _×_ 10<sup>_−_5</sup> , batch size 8, 1k warm-up steps. At inference time, we use a sliding context window of _W_ = 45 for open-loop evaluation (Section 5.2) and _W_ = 77 for closed-loop evaluation (Section 5.3). 

### **5.2 Efficient Long-Horizon Action-Conditioned Video Generation** 

We evaluate the long-horizon generation quality and inference efficiency of our world model. We compare against prior video world models [32, 76], as well as an autoregressive video world model (Diffusion Forcing) baseline trained for the same total number of steps. For multi-view long-horizon evaluation, we sample 256 policy-rollout trajectories from held-out RoboArena [42]. For each trajectory, we condition the world model on the initial multi-view observation and action sequences to generate a 300-frame (20 seconds) video. We evaluate the generated videos using pixel-level metrics (SSIM [71]) and perceptual/distributional metrics (LPIPS [72], FVD [77]). All metrics are computed per view, and we report the average over the three views. 

Figure 4 compares STEP FORCING with video world model baselines (Ctrl-World [32] and PersistWorld [76]) and Diffusion Forcing baseline in terms of inference throughput (FPS) and generation quality (SSIM, LPIPS, FVD). For the baselines, we sweep the number of inference denoising steps over _{_ 50 _,_ 32 _,_ 16 _,_ 8 _,_ 4 _}_ . Because STEP FORCING uses the same denoising schedule during training and inference (Section 3), we evaluate it at its training schedule of 4 steps. Ctrl-World and PersistWorld use bidirectional attention, preventing KV-cache reuse across frames; at 4 steps, they run at 5.70 FPS, compared with 15.31 FPS for autoregressive variants. STEP FORCING achieves the best LPIPS overall and the best SSIM and FVD among 4-step methods, providing a substantially better speed–quality tradeoff for long-horizon evaluation compared to baseline models. 

### **5.3 Correlation with Real World Evaluation** 

To investigate whether ROBOWORLD provides reliable evaluation results, we simulate RoboArena evaluation episodes within our world model and measure the correlation with real-world evaluation. For each policy, we reuse the initial observations from RoboArena episodes that contain all three views: two fixed external views and one wrist view.<sup>2</sup> Starting from these initial observations, the policy is executed in closed loop within the world model: at each step, the policy predicts an action from the current generated observation, and the world model predicts the next observation conditioned on that action. This replaces the physical environment in the RoboArena evaluation protocol 

> 2We include all three-view initial observations available in the latest RoboArena data dump. 

6 


Figure 5: (a) Pearson and Spearman correlations between ROBOWORLD and the RoboArena leaderboard. (b) Pearson correlation under varying numbers of evaluation trials, showing that greater diversity in environments and tasks improves the correlation. (c) ROBOWORLD closed-loop rollouts compared with RoboArena rollouts using the same policies and tasks, sharing only the initial view. Rollouts proceed from top to bottom: PaliGemma Fast fails in both settings by selecting the wrong object, whereas _π_ 0 _._ 5 succeeds in both. 

with our world model while keeping the same policies and initial conditions. Each rollout proceeds for 30 seconds and is scored by a VLM judge. We use GPT-4o as the default judge.<sup>3</sup> 

ROBOWORLD shows strong positive correlation with the RoboArena leaderboard across the eight evaluated policies, achieving Pearson _r_ = 0 _._ 989 and Spearman _ρ_ = 0 _._ 970 (Figure 5a). The resulting policy ranking closely matches the real-world leaderboard under GPT-4o scoring. Replicating the RoboArena benchmark in our neural simulator (across 8 different policies) takes only 100 H100 GPU hours, including the computation and communication costs for each policy action generation and world-model rollout, substantially reducing the cost of large-scale policy evaluation. We further analyze how the number of evaluation trials affects correlation with the real-world leaderboard (Figure 5b). The correlation improves as the number of trials increases, highlighting the importance of broad coverage for reliable policy comparison. Qualitative examples in Figure 5c show that ROBOWORLD captures both successful executions and policy-specific failure modes. For example, ROBOWORLD models the successful behavior of _π_ 0 _._ 5 while also reproducing the wrong-object selection failure observed for PaliGemma Fast in RoboArena. Additional implementation details, qualitative examples, and failure-case analyses are provided in Appendix E. 

### **5.4 Ablations and Analyses** 

**Component ablation of STEP FORCING.** Figure 6 ablates the main components of STEP FORCING on DROID, mainly focusing on the wrist view, the most challenging view due to its fast and action-sensitive motion. All results are evaluated with 4-step denoising during autoregressive rollout. The full method achieves an FVD of 231 _._ 0, while independently removing the self-forwarded prior and anchor step increases FVD to 258 _._ 5 and 294 _._ 0, respectively. These results indicate that schedule alignment is crucial for stable 4-step autoregressive rollout, and that both self-forwarding and anchor steps substantially reduce drift in the wrist view. We also observe consistent findings on BAIR Robot Pushing setup; see Table 3 in Appendix A. 

> 3We use the RoboArena leaderboard snapshot dated Feb. 26, 2026 

7 


Figure 7: Qualitative examples of ROBOWORLD in synthetic extreme environments. We transform real-world robot images into extreme environment scenes (e.g., spacecraft interiors, disaster sites), and conduct closed-loop policy evaluation. 

**Effect of the VLM Evaluation Rubric.** We ablate the task-progress rubric (§4.2) by replacing ROBOWORLD scores with binary scores. We measure Spearman correlation between scores and the RoboArena leaderboard ranking across eight policies. The task-progress rubric achieves _ρ_ = 0 _._ 970, while binary success rate reduces this to _ρ_ = 0 _._ 922. The rubric’s sensitivity to partial task progress is important for reliable policy ranking. 


Figure 6: Component ablation of STEP FORCING on DROID. 

### **Extending ROBOWORLD to Extreme Environments** 

We investigate whether ROBOWORLD could be applied to extreme environments (i.e., construction sites or airplane cabins), where real-world robot evaluation at scale is infeasible. From 175 initial observations from RoboArena snapshots, we generate eight synthetic environments (airplane cabin, spacecraft interior, operating room, nuclear facility, underwater station, disaster site, construction site, mine tunnel) utilizing an image editing model and retain 746 valid initial conditions after manual filtering. As shown in Figure 7, ROBOWORLD can be robustly applied in extreme environments without physical access or complex asset generation for simulation. Moreover, the correlation between ROBOWORLD on extreme environments and RoboArena leaderboard is still mainly retained ( _r_ = 0 _._ 970), implying that ROBOWORLD could be utilized for reliable and safe policy evaluation before physical deployment to these environments. 

## **6 Conclusion** 

We present ROBOWORLD, a scalable evaluation pipeline for generalist robot policies built on a fast autoregressive video world model and a task-progress-aware VLM judge. To enable reliable long-horizon rollouts, we train the world model with STEP FORCING, which reconstructs clean frames from self-forwarded priors and data-derived anchor contexts. Across RoboArena policies, ROBOWORLD achieves high correlation with real-world evaluation, showing that world-model rollouts can approximate real-world policy rankings while substantially reducing evaluation cost. 

## **7 Limitations** 

Despite rapid progress, video world models for dexterous, long-horizon robot manipulation evaluation remain limited. A key challenge is that long-horizon manipulation requires maintaining object consistency under sustained contact. Achieving this typically necessitates substantial training data that capture rich embodied interactions with objects. A promising direction to alleviate this limitation is to pretrain on large-scale human–object interaction data, which provides broad coverage of object behaviors and contact dynamics. 

8 

## **References** 

- [1] T.-Y. Lin, M. Maire, S. Belongie, J. Hays, P. Perona, D. Ramanan, P. Doll´ar, and C. L. Zitnick. Microsoft coco: Common objects in context. In _European Conference on Computer Vision_ , 2014. 

- [2] O. Russakovsky, J. Deng, H. Su, J. Krause, S. Satheesh, S. Ma, Z. Huang, A. Karpathy, A. Khosla, M. Bernstein, et al. Imagenet large scale visual recognition challenge. _International journal of computer vision_ , 115(3):211–252, 2015. 

- [3] D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt. Measuring massive multitask language understanding. _arXiv preprint arXiv:2009.03300_ , 2020. 

- [4] W.-L. Chiang, L. Zheng, Y. Sheng, A. N. Angelopoulos, T. Li, D. Li, B. Zhu, H. Zhang, M. Jordan, J. E. Gonzalez, et al. Chatbot arena: An open platform for evaluating llms by human preference. In _International Conference on Machine Learning_ , 2024. 

- [5] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- [6] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , 2023. 

- [7] A. O’Neill, A. Rehman, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _IEEE International Conference on Robotics and Automation_ , 2024. 

- [8] O. M. Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- [9] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [10] J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [11] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [12] Physical Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- [13] T. Yu, D. Quillen, Z. He, R. Julian, K. Hausman, C. Finn, and S. Levine. Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on Robot Learning_ , 2020. 

- [14] S. James, Z. Ma, D. R. Arrojo, and A. J. Davison. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ , 5(2):3019–3026, 2020. 

- [15] S. Nasiriany, A. Maddukuri, L. Zhang, A. Parikh, A. Lo, A. Joshi, A. Mandlekar, and Y. Zhu. Robocasa: Large-scale simulation of everyday tasks for generalist robots. _arXiv preprint arXiv:2406.02523_ , 2024. 

9 

- [16] Y. R. Wang, C. Ung, C. Tan, G. Tannert, J. Duan, J. Li, A. Le, R. Oswal, M. Grotz, W. Pumacay, et al. Roboeval: Where robotic manipulation meets structured and scalable evaluation. _arXiv preprint arXiv:2507.00435_ , 2025. 

- [17] S. Zhang, Z. Xu, P. Liu, X. Yu, Y. Li, Q. Gao, Z. Fei, Z. Yin, Z. Wu, Y.-G. Jiang, et al. Vlabench: A large-scale benchmark for language-conditioned robotics manipulation with long-horizon reasoning tasks. In _IEEE/CVF International Conference on Computer Vision_ , 2025. 

- [18] Y. Kim, W. Pumacay, O. Rayyan, M. Argus, W. Han, E. VanderBilt, J. Salvador, A. Deshpande, R. Hendrix, S. Jauhri, et al. Molmospaces: A large-scale open ecosystem for robot navigation and manipulation. _arXiv preprint arXiv:2602.11337_ , 2026. 

- [19] W. Zhao, J. P. Queralta, and T. Westerlund. Sim-to-real transfer in deep reinforcement learning for robotics: a survey. In _IEEE symposium series on computational intelligence (SSCI)_ , 2020. 

- [20] D. Blanco-Mulero, O. Barbany, G. Alcan, A. Colom´e, C. Torras, and V. Kyrki. Benchmarking the sim-to-real gap in cloth manipulation. _IEEE Robotics and Automation Letters_ , 9(3):2981– 2988, 2024. 

- [21] Z. Zhou, P. Atreya, Y. L. Tan, K. Pertsch, and S. Levine. Autoeval: Autonomous evaluation of generalist robot manipulation policies in the real world. _arXiv preprint arXiv:2503.24278_ , 2025. 

- [22] A. Jain, M. Zhang, K. Arora, W. Chen, M. Torne, M. Z. Irshad, S. Zakharov, Y. Wang, S. Levine, C. Finn, et al. Polaris: Scalable real-to-sim evaluations for generalist robot policies. _arXiv preprint arXiv:2512.16881_ , 2025. 

- [23] Y. Jangir, Y. Zhang, K. Yamazaki, C. Zhang, K.-H. Tu, T.-W. Ke, L. Ke, Y. Bisk, and K. Fragkiadaki. RobotArena _∞_ : Scalable robot benchmarking via real-to-sim translation. _arXiv preprint arXiv:2510.23571_ , 2025. 

- [24] A. Blattmann, T. Dockhorn, S. Kulal, D. Mendelevitch, M. Kilian, D. Lorenz, Y. Levi, Z. English, V. Voleti, A. Letts, et al. Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint arXiv:2311.15127_ , 2023. 

- [25] T. Brooks, B. Peebles, C. Holmes, W. DePue, Y. Guo, L. Jing, D. Schnurr, J. Taylor, T. Luhman, E. Luhman, C. Ng, R. Wang, and A. Ramesh. Video generation models as world simulators. 2024. 

- [26] W. Kong, Q. Tian, Z. Zhang, R. Min, Z. Dai, J. Zhou, J. Xiong, X. Li, B. Wu, J. Zhang, et al. Hunyuanvideo: A systematic framework for large video generative models. _arXiv preprint arXiv:2412.03603_ , 2024. 

- [27] H. Chen, Y. Zhang, X. Cun, M. Xia, X. Wang, C. Weng, and Y. Shan. Videocrafter2: Overcoming data limitations for high-quality video diffusion models. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024. 

- [28] Z. Yang, J. Teng, W. Zheng, M. Ding, S. Huang, J. Xu, Y. Yang, W. Hong, X. Zhang, G. Feng, et al. Cogvideox: Text-to-video diffusion models with an expert transformer. _arXiv preprint arXiv:2408.06072_ , 2024. 

- [29] A. Ali, J. Bai, M. Bala, Y. Balaji, A. Blakeman, T. Cai, J. Cao, T. Cao, E. Cha, Y.-W. Chao, et al. World simulation with video foundation models for physical ai. _arXiv preprint arXiv:2511.00062_ , 2025. 

- [30] N. Agarwal, A. Ali, M. Bala, Y. Balaji, E. Barker, T. Cai, P. Chattopadhyay, Y. Chen, Y. Cui, Y. Ding, et al. Cosmos world foundation model platform for physical ai. _arXiv preprint arXiv:2501.03575_ , 2025. 

10 

- [31] T. Wan, A. Wang, B. Ai, B. Wen, C. Mao, C.-W. Xie, D. Chen, F. Yu, H. Zhao, J. Yang, et al. Wan: Open and advanced large-scale video generative models. _arXiv preprint arXiv:2503.20314_ , 2025. 

- [32] Y. Guo, L. X. Shi, J. Chen, and C. Finn. Ctrl-world: A controllable generative world model for robot manipulation. _arXiv preprint arXiv:2510.10125_ , 2025. 

- [33] G. R. Team, C. Devin, Y. Du, D. Dwibedi, R. Gao, A. Jindal, T. Kipf, S. Kirmani, F. Liu, A. Majumdar, et al. Evaluating gemini robotics policies in a veo world simulator. _arXiv preprint arXiv:2512.10675_ , 2025. 

- [34] S. Gao, W. Liang, K. Zheng, A. Malik, S. Ye, S. Yu, W.-C. Tseng, Y. Dong, K. Mo, C.-H. Lin, et al. Dreamdojo: A generalist robot world model from large-scale human videos. _arXiv preprint arXiv:2602.06949_ , 2026. 

- [35] X. W. M. Team. 1x world model: Evaluating bits, not atoms. Technical report, 1X Technologies, 2025. Accessed: 2026-02-23. 

- [36] G. Team, B. Wang, C. Ni, G. Huang, G. Zhao, H. Li, J. Li, J. Lv, J. Liu, L. Feng, et al. Gigabrain-0.5 m*: a vla that learns from world model-based reinforcement learning. _arXiv preprint arXiv:2602.12099_ , 2026. 

- [37] J. Yang, K. Lin, J. Li, W. Zhang, T. Lin, L. Wu, Z. Su, H. Zhao, Y.-Q. Zhang, L. Chen, et al. Rise: Self-improving robot policy with compositional world model. _arXiv preprint arXiv:2602.11075_ , 2026. 

- [38] A. K. Sharma, Y. Sun, N. Lu, Y. Zhang, J. Liu, and S. Yang. World-gymnast: Training robots with reinforcement learning in a world model. _arXiv preprint arXiv:2602.02454_ , 2026. 

- [39] J. Quevedo, A. K. Sharma, Y. Sun, V. Suryavanshi, P. Liang, and S. Yang. Worldgym: World model as an environment for policy evaluation. _arXiv preprint arXiv:2506.00613_ , 2025. 

- [40] Y. Li, Y. Zhu, J. Wen, C. Shen, and Y. Xu. Worldeval: World model as real-world robot policies evaluator. _arXiv preprint arXiv:2505.19017_ , 2025. 

- [41] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 

- [42] P. Atreya, K. Pertsch, T. Lee, M. J. Kim, A. Jain, A. Kuramshin, C. Eppner, C. Neary, E. Hu, F. Ramos, et al. Roboarena: Distributed real-world evaluation of generalist robot policies. _arXiv preprint arXiv:2506.18123_ , 2025. 

- [43] X. Li, K. Hsu, J. Gu, K. Pertsch, O. Mees, H. R. Walke, C. Fu, I. Lunawat, I. Sieh, S. Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 

- [44] J. Tobin, R. Fong, A. Ray, J. Schneider, W. Zaremba, and P. Abbeel. Domain randomization for transferring deep neural networks from simulation to the real world. In _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2017. 

- [45] K. Zhang, S. Sha, H. Jiang, M. Loper, H. Song, G. Cai, Z. Xu, X. Hu, C. Zheng, and Y. Li. Realto-sim robot policy evaluation with gaussian splatting simulation of soft-body interactions. _arXiv preprint arXiv:2511.04665_ , 2025. 

- [46] J. Abou-Chakra, L. Sun, K. Rana, B. May, K. Schmeckpeper, N. Suenderhauf, M. V. Minniti, and L. Herlant. Real-is-sim: Bridging the sim-to-real gap with a dynamic digital twin. _arXiv preprint arXiv:2504.03597_ , 2025. 

11 

- [47] M. J. Kim, Y. Gao, T.-Y. Lin, Y.-C. Lin, Y. Ge, G. Lam, P. Liang, S. Song, M.-Y. Liu, C. Finn, et al. Cosmos policy: Fine-tuning video models for visuomotor control and planning. _arXiv preprint arXiv:2601.16163_ , 2026. 

- [48] S. Ye, Y. Ge, K. Zheng, S. Gao, S. Yu, G. Kurian, S. Indupuru, Y. L. Tan, C. Zhu, J. Xiang, et al. World action models are zero-shot policies. _arXiv preprint arXiv:2602.15922_ , 2026. 

- [49] J. Jang, S. Ye, Z. Lin, J. Xiang, J. Bjorck, Y. Fang, F. Hu, S. Huang, K. Kundalia, Y.-C. Lin, et al. Dreamgen: Unlocking generalization in robot learning through video world models. _arXiv preprint arXiv:2505.12705_ , 2025. 

- [50] Y. Liao, P. Zhou, S. Huang, D. Yang, S. Chen, Y. Jiang, Y. Hu, J. Cai, S. Liu, J. Luo, et al. Genie envisioner: A unified world foundation platform for robotic manipulation. _arXiv preprint arXiv:2508.05635_ , 2025. 

- [51] L. Li, Q. Zhang, Y. Luo, S. Yang, R. Wang, F. Han, M. Yu, Z. Gao, N. Xue, X. Zhu, et al. Causal world modeling for robot control. _arXiv preprint arXiv:2601.21998_ , 2026. 

- [52] S. Yang, Y. Du, K. Ghasemipour, J. Tompson, L. Kaelbling, D. Schuurmans, and P. Abbeel. Learning interactive real-world simulators. _arXiv preprint arXiv:2310.06114_ , 2023. 

- [53] J. Wu, S. Yin, N. Feng, X. He, D. Li, J. Hao, and M. Long. ivideogpt: Interactive videogpts are scalable world models. _Advances in Neural Information Processing Systems_ , 37:68082–68119, 2024. 

- [54] F. Zhu, H. Wu, S. Guo, Y. Liu, C. Cheang, and T. Kong. Irasim: Learning interactive real-robot action simulators. _arXiv preprint arXiv:2406.14540_ , 2024. 

- [55] L. Wang, K. Zhao, C. Liu, and X. Chen. Learning real-world action-video dynamics with heterogeneous masked autoregression. _arXiv preprint arXiv:2502.04296_ , 2025. 

- [56] W.-C. Tseng, J. Gu, Q. Zhang, H. Mao, M.-Y. Liu, F. Shkurti, and L. Yen-Chen. Scalable policy evaluation with video world models. _arXiv preprint arXiv:2511.11520_ , 2025. 

- [57] Y. Jiang, S. Chen, S. Huang, L. Chen, P. Zhou, Y. Liao, X. He, C. Liu, H. Li, M. Yao, et al. Enerverse-ac: Envisioning embodied environments with action condition. _arXiv preprint arXiv:2505.09723_ , 2025. 

- [58] F. Ebert, C. Finn, A. X. Lee, and S. Levine. Self-supervised visual planning with temporal skip connections. _CoRL_ , 12(16):23, 2017. 

- [59] J. Bruce, M. D. Dennis, A. Edwards, J. Parker-Holder, Y. Shi, E. Hughes, M. Lai, A. Mavalankar, R. Steigerwald, C. Apps, et al. Genie: Generative interactive environments. In _International Conference on Machine Learning_ , 2024. 

- [60] X. Mao, S. Lin, Z. Li, C. Li, W. Peng, T. He, J. Pang, M. Chi, Y. Qiao, and K. Zhang. Yume: An interactive world generation model. _arXiv preprint arXiv:2507.17744_ , 2025. 

- [61] Y. Zhang, C. Peng, B. Wang, P. Wang, Q. Zhu, F. Kang, B. Jiang, Z. Gao, E. Li, Y. Liu, et al. Matrix-game: Interactive world foundation model. _arXiv preprint arXiv:2506.18701_ , 2025. 

- [62] X. He, C. Peng, Z. Liu, B. Wang, Y. Zhang, Q. Cui, F. Kang, B. Jiang, M. An, Y. Ren, et al. Matrix-game 2.0: An open-source real-time and streaming interactive world model. _arXiv preprint arXiv:2508.13009_ , 2025. 

- [63] D. Valevski, Y. Leviathan, M. Arar, and S. Fruchter. Diffusion models are real-time game engines. _arXiv preprint arXiv:2408.14837_ , 2024. 

- [64] T. Yin, Q. Zhang, R. Zhang, W. T. Freeman, F. Durand, E. Shechtman, and X. Huang. From slow bidirectional to fast autoregressive video diffusion models. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2025. 

12 

- [65] X. Huang, Z. Li, G. He, M. Zhou, and E. Shechtman. Self forcing: Bridging the train-test gap in autoregressive video diffusion. _arXiv preprint arXiv:2506.08009_ , 2025. 

- [66] Y. Guo, C. Yang, H. He, Y. Zhao, M. Wei, Z. Yang, W. Huang, and D. Lin. End-to-end training for autoregressive video diffusion via self-resampling. _arXiv preprint arXiv:2512.15702_ , 2025. 

- [67] Y. Lipman, R. T. Chen, H. Ben-Hamu, M. Nickel, and M. Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

- [68] X. Liu, C. Gong, and Q. Liu. Flow straight and fast: Learning to generate and transfer data with rectified flow. _arXiv preprint arXiv:2209.03003_ , 2022. 

- [69] B. Chen, D. Mart´ı Mons´o, Y. Du, M. Simchowitz, R. Tedrake, and V. Sitzmann. Diffusion forcing: Next-token prediction meets full-sequence diffusion. _Advances in Neural Information Processing Systems_ , 37:24081–24125, 2024. 

- [70] D. Zhou, Q. Sun, Y. Peng, K. Yan, R. Dong, D. Wang, Z. Ge, N. Duan, and X. Zhang. Taming teacher forcing for masked autoregressive video generation. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2025. 

- [71] Z. Wang, A. Bovik, H. Sheikh, and E. Simoncelli. Image quality assessment: from error visibility to structural similarity. _IEEE Transactions on Image Processing_ , 13(4):600–612, 2004. 

- [72] R. Zhang, P. Isola, A. A. Efros, E. Shechtman, and O. Wang. The unreasonable effectiveness of deep features as a perceptual metric. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2018. 

- [73] K. Gao, J. Shi, H. Zhang, C. Wang, J. Xiao, and L. Chen. Ca2-vdm: Efficient autoregressive video diffusion model with causal generation and cache sharing. _arXiv preprint arXiv:2411.16375_ , 2024. 

- [74] J. Cui, J. Wu, M. Li, T. Yang, X. Li, R. Wang, A. Bai, Y. Ban, and C.-J. Hsieh. Self-forcing++: Towards minute-scale high-quality video generation. _arXiv preprint arXiv:2510.02283_ , 2025. 

- [75] S. Huang, J. Wu, Q. Zhou, S. Miao, and M. Long. Vid2world: Crafting video diffusion models to interactive world models. _arXiv preprint arXiv:2505.14357_ , 2025. 

- [76] J. Bardhan, P. Drozdik, J. Sivic, and V. Petrik. Persistent robot world models: Stabilizing multi-step rollouts via reinforcement learning. _arXiv preprint arXiv:2603.25685_ , 2026. 

- [77] T. Unterthiner, S. Van Steenkiste, K. Kurach, R. Marinier, M. Michalski, and S. Gelly. Towards accurate generative models of video: A new metric & challenges. _arXiv preprint arXiv:1812.01717_ , 2018. 

- [78] W. Peebles and S. Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 4195–4205, 2023. 

- [79] J. Su, M. Ahmed, Y. Lu, S. Pan, W. Bo, and Y. Liu. Roformer: Enhanced transformer with rotary position embedding. _Neurocomputing_ , page 127063, 2024. 

13 

# **Appendix** 

## **A Implementation Details: Action-conditioned BAIR** 

**Dataset.** We use the BAIR Robot Pushing dataset [58]: 43 _,_ 264 training clips and 256 test clips of 30 frames each, 64 _×_ 64 RGB pixels in [ _−_ 1 _,_ 1], accompanied by a per-frame 4-dimensional robot action. Training samples a random 15-frame window per clip; evaluation takes the first 30 frames of each test clip and uses _K_ =1 as the conditioning prefix. All experiments use the original 64 _×_ 64 resolution. 

**Architecture Details.** We use a causal video DiT [78] adapted to the 3-channel RGB pixel space (Table 2). Each frame is patchified by a 4 _×_ 4 Conv2d into 16 _×_ 16=256 spatial tokens. Each DiT block contains spatial self-attention (per frame), causal temporal self-attention (across frames), and an MLP, with all three components AdaLN-modulated by a per-frame conditioning vector. Temporal position is encoded with Rotary Position Embeddings (RoPE) [79] applied to the temporal-attention _Q, K_ projections. The action vector is projected through a two-layer MLP and added to the perframe condition that drives AdaLN. 

Table 2: Backbone hyperparameters. 

||student / main|teacher|
|---|---|---|
|embed<br>~~d~~im|256|448|
|depth|6|12|
|num<br>~~h~~eads|8|14|
|patch<br>~~s~~ize|4|4|
|RoPE max<br>~~s~~eq|128|128|
|attention|causal|bidirectional|
|action MLP|4_,_512_,_256|4_,_896_,_448|
|parameter count|9_._2M|54_._6M|


**Loss Function.** All five methods share the same backbone and the same loss target ( _v_ -prediction). 

- **Diffusion Forcing** [69]: per-frame independent noise levels _ti ∼U_ (0 _._ 001 _,_ 0 _._ 999). A single forward pass through the causal DiT predicts _vi_ for every frame and the loss is averaged. 

- **Teacher Forcing** [70]: per-frame independent _ti ∼U_ (0 _._ 001 _,_ 0 _._ 999) as in DF, but each target frame _ni_ should be predicted conditional on _strict-past clean_ frames _c<i_ , not on the (noisy) future. Naively this is one forward pass per target _i_ ( _T_ passes per step). Following Resampling Forcing [66], we use the 2T-sequence dense trick: pack inputs as [ _c_ 0 _, ..., cT −_ 1 _, n_ 0 _, ..., nT −_ 1], share temporal indices between _ci_ and _ni_ , and apply the blockattention mask shown below. This delivers one supervised prediction per frame in a single forward. 

- **Resampling Forcing** [66]: Because the official code is not publicly available, we implemented faithfully according to the paper. Each training step has two phases: (i) _Resampling_ : sample a shared timestep _ts ∼_ LogitNormal(shift=0 _._ 6), corrupt all frames at _ts_ with i.i.d. Gaussian noise, then _sequentially_ 1-step Euler-denoise per frame in `no` ~~`g`~~ `rad` to obtain resampled clean estimates _x_ ˜0 _..T −_ 1; (ii) _Supervised step_ : sample per-frame independent _ti ∼U_ (0 _._ 001 _,_ 0 _._ 999), pack [˜ _x_ 0 _, . . . ,_ ˜ _xT −_ 1 _, n_ 0 _, . . . , nT −_ 1] with shared RoPE indices, and apply the same 2T-dense mask as in TF. 

- **Self Forcing** [65]: implemented based on the official code, with the following modifications motivated by our small-scale BAIR setup: 

14 

1. _initial view conditioning._ For a fair comparison, we use the same 9M-parameter causal DiT backbone as the other BAIR baselines, whereas the original Self Forcing implementation is built on Wan-1.3B-i2v. Accordingly, the conditioning interface differs slightly: the original implementation uses channel-axis image-to-video conditioning, while our BAIR setup uses frame-axis conditioning. Specifically, the ground-truth conditioning frame is concatenated along the temporal axis and pinned at _t_ =0. To keep the score networks in-distribution during distillation, we prepend this conditioning frame at _t_ =0 to every `real` ~~`s`~~ `core` and `fake` ~~`s`~~ `core` call. 

2. _Numerical stabilization._ For numerical stability, we clamp the DMD2 normalizer _∥x_ 0 _,_ real _− x_ 0 _,_ student _∥_ 1 from below by a small constant _ε_ =0 _._ 1. This avoids division-byzero when the teacher nearly perfectly reconstructs the student output. 

All other hyperparameters follow the paper: LR _G_ =2 _×_ 10<sup>_−_6</sup> , LR _F_ =4 _×_ 10<sup>_−_7</sup> , AdamW _β_ 1=0 _, β_ 2=0 _._ 999, weight ~~d~~ ecay=0 _._ 01, EMA=0 _._ 99 from step 200, critic:generator update ratio 5:1. 

- **STEP FORCING** : trained at a fixed discrete schedule _S_ =4, with per-frame timestep sampled from _{_ 0 _._ 25 _,_ 0 _._ 50 _,_ 0 _._ 75 _,_ 1 _._ 0 _}_ . We supervise the model on self-forwarded denoising trajectories with anchor probability _p_ =0 _._ 5, as described in Section 3. 

**2T-sequence dense mask (TF).** Let _T_ be the training-window length. We concatenate _T_ clean and _T_ noisy frames along the temporal axis and share RoPE positions [0 _, . . . , T −_ 1 _,_ 0 _, . . . , T −_ 1]. The boolean attention mask _M ∈{_ 0 _,_ 1 _}_<sup>2</sup><sup>_T ×_2</sup><sup>_T_</sup> is: 


The mask blocks noisy-to-noisy attention, ensuring that each noisy target is predicted without conditioning on other noisy targets under the dense layout. This yields the same per-target conditioning structure as the naive _T_ -pass TF objective, up to a constant factor in the loss, while requiring only a single forward pass per step. 

**Training.** We use AdamW with a constant learning rate of 2 _×_ 10<sup>_−_4</sup> , _β_ = (0 _._ 9 _,_ 0 _._ 999), weight decay 10<sup>_−_4</sup> , and global gradient-norm clipping at 1 _._ 0. We train for 100k steps with batch size 16. 

**Training Cost Comparison.** We compare the per-step training cost of each method in our implementation. All models have 9.2M parameters and are trained on a single NVIDIA H100. “Fwd/step” denotes the number of model forward passes required per optimizer step, including no-gradient forwards used for autoregressive resampling. 

|Method|Fwd/step|sec/step|step/s|
|---|---|---|---|
|Diffusion Forcing|1|86 ms|11.6|
|STEP FORCING|2|122 ms|8.2|
|Teacher Forcing|1|180 ms|5.5|
|Resampling Forcing|_T_+1(16)|_∼_1_._3s|0.77|
|Self Forcing [65]|_∼_344|2.4 s|0.42|


4 

> 4 _sec/step_ is wall-clock time measured on a single H100; _Fwd/step_ is an analytical count of model forward passes per optimizer step, including no-gradient forwards. DF uses one gradient forward. STEP FORCING uses two forwards: one no-gradient self-forward and one gradient forward. TF uses one forward over the 2 _T_ -packed sequence. RF uses _T_ +1 forwards: _T_ no-gradient resampling forwards plus one supervised forward. Since our training window length is _T_ =15, this gives 16 forwards per optimizer step. For SF (DMD), with a 5:1 criticto-generator update ratio, each optimizer step uses six autoregressive rollouts of _F ·S_ generator forwards plus score/critic evaluations, giving 6 _·_ 56 + 3 + 5 = 344 at _F_ =14 and _S_ =4. 

15 

Teacher Forcing uses a 2 _T_ -length dense sequence, which increases temporal-attention cost relative to Diffusion Forcing. STEP FORCING uses two forward passes per training step: one no-gradient self-forward pass and one gradient update pass, both over a length- _T_ sequence. Resampling Forcing performs an autoregressive resampling loop with _T_ sequential no-gradient forwards, one per target frame, before the supervised update. For Self Forcing, we follow the original DMD distillation procedure, which requires multi-step autoregressive rollouts together with repeated score and critic evaluations; this leads to a higher per-step cost in the BAIR setting. 

**Implementation note.** The wall-clock numbers above reflect our straightforward implementation of each method. In particular, our autoregressive-style baselines use dense causal-mask forwards without key–value cache amortization. Thus, the reported costs should be interpreted as a practical comparison under a common implementation rather than as the most optimized possible runtime for each algorithm. Further engineering, such as caching key–value tensors across autoregressive resampling steps, could reduce the absolute cost of RF- or SF-style methods. However, these methods still require sequential autoregressive resampling during training, whereas STEP FORCING only adds a single no-gradient self-forward pass. Therefore, we expect the qualitative cost ordering to remain similar: 

DF _<_ STEP FORCING _<_ TF _≪_ RF _≪_ SF _._ 

Overall, this comparison highlights that autoregressive resampling-based training objectives can be substantially more expensive than objectives that avoid long sequential resampling loops. 

**Inference.** At evaluation time, we autoregressively generate 30 frames starting from _K_ =1 clean conditioning frame and the ground-truth action sequence. For simplify the implementation we do not use KV-caching. 

**Evaluation protocol.** We evaluate on 64 held-out test clips (BAIR test split, deterministic seed). Each rollout is compared frame-by-frame against the ground-truth clip with: 

- **MSE** : pixel-space mean squared error on [ _−_ 1 _,_ 1]. 

- **SSIM** [71]: window size 11, `pytorch` ~~`m`~~ `sssim` default; computed on rescaled [0 _,_ 1] frames. 

- **LPIPS** [72]: AlexNet backbone, computed directly on [ _−_ 1 _,_ 1] frames. 

**Full Results.** Table 3 extends the main paper table with oracle teacher checkpoints (9M / 55M) and the FVD column. The teachers are evaluated under their own training protocol, using in-painting at _T_ =15 and _S_ =16. Therefore, they are not directly comparable to the causal student rows, but serve as an oracle ceiling reference. 

## **B Vision-Language Model-Based Evaluation Details** 

This section provides additional details on the VLM-based evaluation procedure used in ROBOWORLD. We describe the motivation behind using a VLM-as-a-judge, the scoring rubric designed to separate policy progress from world-model artifacts, the multi-view evaluation strategy, the rollout sampling and scoring protocol, the exact prompt templates, and ablations validating these design choices. 

### **B.1 VLM-as-a-Judge: Rubric and Strategy** 

Human scoring requires human-in-the-loop evaluation, limiting scalability. To maximize scalability, we replace human annotators with a pretrained VLM as a judge, which generates a score when conditioned on rollouts produced by the video world model. However, since world model rollouts inevitably contain model-induced artifacts, naive automatic scoring may compromise reliability. To maintain reliable evaluation, we introduce two design choices. 

16 

Table 3: Full BAIR high-motion (top-64) evaluation. Causal students autoregressively roll out 29 frames from one conditioning frame at _S_ =4, while teachers use in-painting at _T_ =15 and _S_ =16. Frame 0 is excluded from ID metrics. 

|Method<br>|Fwd/step|_S_|In-dis<br>MSE_↓_|tribution<br>SSIM_↑_|(1–14)<br>LPIPS_↓_|Out-of-<br>MSE_↓_|distributio<br>SSIM_↑_|n (15–29)<br>LPIPS_↓_|FVD_↓_|
|---|---|---|---|---|---|---|---|---|---|
|_Teachers (oracle reference)_||||||||||
|Teacher 9M|1|16|0.0658|0.7820|0.0583|—|—|—|20.42|
|Teacher 55M|1|16|**0.0587**|**0.8069**|**0.0489**|—|—|—|**14.46**|
|_Causal students_||||||||||
|Teacher Forcing [70]|1|8|0.0620|0.7942|0.0554|0.1185|0.7118|0.1058|**17.70**|
|Diffusion Forcing [69]|1|8|0.0758|0.7657|0.0690|0.1113|0.6861|0.1117|22.47|
|Resampling Forcing [66]|_T_+1|8|0.0618|0.7891|0.0572|0.1265|0.6996|0.1082|19.15|
|Self Forcing [65]|_∼_344<sup>_†_</sup>|4|0.0588|0.7929|0.0548|0.1246|0.6953|0.1083|21.31|
|**Step Forcing (ours)**|**2**|4|**0.0512**|**0.8063**|**0.0525**|**0.0778**|**0.7374**|**0.0768**|19.26|
|_Ablations of Step Forcing_||||||||||
|_−_continuous-_t_|2|4|0.0660|0.7895|0.0670|0.0922|0.7318|0.0959|18.43|
|_−_continuous-_t_|2|8|0.0700|0.7859|0.0651|0.0966|0.7274|0.0952|18.03|
|_−_continuous-_t_|2|16|0.0720|0.7834|0.0640|0.0998|0.7226|0.0951|18.31|
|_−_no self-forward (_p_=1)|1|4|0.1329|0.7001|0.1081|0.1587|0.6298|0.1401|29.91|
|_−_no anchor (_p_=0)|2|4|0.1869|0.5998|0.1933|0.4141|0.3745|0.3334|49.25|
|_−_DF (discrete)|1|4|0.0911|0.7002|0.0913|0.1583|0.5797|0.1451|43.63|


> _†_ Self Forcing’s _∼_ 344 forwards per training step decomposes as one generator update (56 autoregressive rollout forwards + 3 score evaluations) plus five critic updates, each consisting of 56 autoregressive rollout forwards + 1 score evaluation. This gives 59 + 5 _×_ 57 = 344. 


Figure 8: **Design principles of the evaluation rubric.** We design the rubric such that scores primarily reflect task progress. In addition, we assign different penalties depending on when world-model errors occur, so failures that arise earlier in the rollout receive lower scores than those that happen after substantial task progress. 

**(1) Fine-grained evaluation rubric.** We design a six-level rubric (Figure 8) that assigns scores based on both task progress and the stage at which world-model errors occur. Concretely: 

- **5 (Success)** : Task goal is achieved. 

- **4 (Near success, world-model fail during interaction)** : The robot reaches and interacts with the target. 

- **3 (World-model fail upon interaction)** : World-model failure after target contact. 

- **2 (Attempt without interaction)** : The robot approaches the target object. 

- **1 (World-model fail before interaction)** : World-model failure while approaching the target. 

- **0 (Failure)** : All other cases. 

**(2) Anchoring success judgments on stable fixed views.** To ensure reliable evaluation, we primarily anchor task success judgments on the two fixed external views, which provide a stable and 

17 

consistent perspective of the workspace. In contrast, the wrist view is highly dynamic and prone to localized world-model artifacts due to rapid camera motion and contact dynamics. Therefore, we utilize the fixed views as the definitive signal for assessing task progress and completion, while restricting the wrist view’s role solely to the identification of world-model failures. 

### **B.2 VLM Evaluation Procedure** 

For VLM-based evaluation, we use GPT-4o as the judge. Each rollout is sampled at one frame per second and split into two segments. We score the segments independently using GPT-4o, providing 15 sampled frames per segment along with the rubric and the task description. The final per-rollout score is the maximum across the two segments. To reduce evaluation cost, we omit scoring the second segment when the policy is already judged successful in the first segment. 

### **B.3 VLM Prompt Templates** 

Table 4 presents the rubric used to compute the score. Tables 6 and 5 present the prompts used for the vision-language model evaluator. 

### **B.4 Ablation on ROBOWORLD Evaluation Strategy** 

We ablate the two design choices of ROBOWORLD’s VLM-based evaluation (Section B.1; Table 7). Replacing the rubric with a binary success-rate baseline discards the fine-grained scoring of task progress and world-model errors. Including the wrist view in success judgments—rather than restricting it to world-model failure detection—incurs a larger drop, indicating that the wrist view’s higher artifact density biases the judge when used for success scoring. 

### **B.5 Consistent Trend across VLM Judges** 

To evaluate whether RoboWorld metrics depend on a specific VLM judge, we additionally use _Gemini-2.5-Flash_ as an alternative judge. Figures 9 and 10 compare the correlation between the RoboArena leaderboard score and RoboWorld metrics under two judges: GPT-4o and Gemini-2.5Flash. 

Across both judges, RoboWorld Score shows a strong and statistically significant linear relationship with the RoboArena score (Pearson _r_ =0 _._ 989, _p<_ 0 _._ 001 for GPT-4o; _r_ =0 _._ 944, _p<_ 0 _._ 001 for Gemini2.5-Flash). The same trend holds for RoboWorld Success Rate, where both judges yield high Pearson correlations ( _r_ =0 _._ 901, _p_ =0 _._ 002 for GPT-4o; _r_ =0 _._ 876, _p_ =0 _._ 004 for Gemini-2.5-Flash). The relative ordering of the eight policies is largely preserved across judges, and the fitted slopes are visually consistent. These results indicate that RoboWorld metrics are not tied to a particular VLM judge, but instead capture policy-level capability that aligns with closed-loop real-world evaluation. 

## **C Implementation Details** 

This section provides implementation details for video world model training and interactive inference. 

### **C.1 Training** 

Detailed training configurations are provided in Table 8 and Table 9. 

### **C.2 Inference and Rollout Protocol** 

All inference is performed autoregressively in the latent space of the video VAE. The VAE compresses video temporally by a factor of 4 _×_ , such that each latent token corresponds to four video 

18 

#### **Evaluation Rubric Used in the VLM Prompt** 

#### **Evaluation Criteria** 

**Target object:** The object specified in the task instruction. 

#### **Score 5: Success** 

**Definition:** The policy successfully completes the task as instructed. 

- The target object is correctly manipulated to reach the intended goal state. 

- The outcome is clearly successful and verifiable. 

- Success should not be judged from a single frame. 

- Evaluators must check adjacent frames to confirm that the goal state is genuinely achieved and stably 

- maintained. 

To determine success, the robot must be clearly observed interacting with the target object. 

#### **Score 4: Near success OR World Model failure during target-object contact/interaction** 

**Definition:** The policy nearly completes the task but does not fully succeed, OR a world model failure occurs after the policy has made contact with (or begun manipulating) the target object. 

- The policy correctly reaches and interacts with the target object, but the final goal is not achieved. 

#### **Score 3: World Model failure upon target-object contact/interaction** 

**Definition:** A world model failure occurs at the moment the policy begins interacting with the target object. 

- The world model fails immediately when the robot makes contact with the target object or begins 

- manipulation. 

#### **Score 2: Attempted execution near target** 

**Definition:** The policy attempts to solve the task and moves near the target object. 

- The robot moves near the target object with task-directed behavior. 

#### **Score 1: World Model failure during approach before target-object interaction** 

**Definition:** A world model failure occurs while moving toward the target object. 

- The robot is near the target object in the fixed view, but the target object disappears or is not visible in 

- the wrist view. 

- Evaluation is unreliable due to this fixed-view vs. wrist-view inconsistency. 

#### **Score 0: Failure (All other cases)** 

**Definition:** Any case not covered by Scores 5, 4, 3, 2, or 1. 

- The policy exhibits movements irrelevant to the task instruction. 

- The robot moves independently of the target object in the fixed view. 

- The robot leaves the scene in the fixed view. 

- World model failures that occur while the robot is not meaningfully interacting with or approaching the 

- target object. 

### Table 4: Evaluation rubric used in the VLM prompt. 

frames. During generation, latent tokens are produced causally, conditioned on previous observations and the corresponding action sequence. Action conditioning is provided at the token level by flattening the four 7-DoF robot actions corresponding to each latent token. 

**Open-Loop Inference.** For open-loop evaluation, the model receives the initial ground-truth observation and the full ground-truth action sequence of the episode. The model then generates all future observations autoregressively without additional visual feedback. We evaluate the generated non-context frames using PSNR, SSIM, LPIPS, FID, and FVD. 

**Closed-Loop Inference.** In closed-loop inference, the world model serves as a neural simulator for robot policy evaluation. Each rollout is initialized from the first observation of a real episode. At every step, the latest generated observation is provided to the policy, which predicts the next action chunk. Conditioned on this action, the world model generates the next latent token, which is decoded into video frames. The newest generated observation is then fed back to the policy, forming a closed-loop interaction cycle. 

19 

#### **Prompt Template Used for VLM Evaluation (Wrist View Used Only for Error Identification)** 

You are evaluating a robot policy rollout video. The frames below are extracted from the video in chronological order (first frame to last frame). **Task Instruction:** _{_ `instruction` _} {_ `rubric` _}_ Multiview frames are provided, corresponding to a robot policy rollout in the world model. Each frame consists of a fixed left view (upper right view), a fixed right view (upper left view), and a wrist view (bottom left). **Evaluation Method:** 1. Use the fixed views (the two upper views) as the primary reference. Determine whether the robot interacts with the target object based on the fixed views. 2. Use the wrist view only to identify world model errors (e.g., object disappearance or inconsistency). Do NOT use the wrist view to infer task success. 

**Provide:** 1. A score (0 to _{_ `max` ~~`s`~~ `core` _}_ ) according to the rubric above 2. A brief explanation of your reasoning 

Table 5: Prompt template used when the wrist view is used only to identify world model errors, but not to determine task success. 

#### **Prompt Template Used for VLM Evaluation (Wrist View Used for Full Evaluation)** 

You are evaluating a robot policy rollout video. The frames below are extracted from the video in chronological order (first frame to last frame). **Task Instruction:** _{_ `instruction` _} {_ `rubric` _}_ Multiview frames are provided, corresponding to a robot policy rollout in the world model. Each frame consists of a fixed left view (upper right view), a fixed right view (upper left view), and a wrist view (bottom left). 

#### **Evaluation Method:** 

1. Use ALL three views (fixed left, fixed right, and wrist) for evaluation. All views contribute equally to determining task success and robot behavior. 

**Provide:** 1. A score (0 to _{_ `max` ~~`s`~~ `core` _}_ ) according to the rubric above 2. A brief explanation of your reasoning 

Table 6: Prompt template used when the wrist view is used as a full evaluation signal. 

Final policy performance is evaluated from the generated videos using the VLM-based scoring procedure described in Appendix B. 

## **D Additional Results on Action-Conditioned Video Generation** 

Table 10 reports long-horizon action-conditioned video generation results on RoboArena. Models generate 301-frame rollouts conditioned on multi-view observations and action sequences, and metrics are averaged across all views. As shown in Table 10, Step Forcing achieves the best perceptual quality among few-step methods, obtaining the lowest LPIPS and FID with only 4 denoising steps. Notably, despite using substantially fewer denoising steps, Step Forcing remains competitive with baselines that use 32 or 50 denoising steps, indicating that the proposed training objective enables efficient long-horizon generation without requiring expensive sampling. 

Table 10 also shows that IRASim performs reasonably in short-horizon reproduction but degrades severely in our 301-frame rollout setting, especially in later frames, resulting in substantially worse perceptual and temporal metrics. This suggests that short-horizon video quality does not necessarily 

20 

Table 7: Ablation on rank correlation with the RoboArena leaderboard (Spearman _ρ_ ). Numbers in parentheses indicate the drop relative to the full ROBOWORLD score. 

|**Method / Ablation**|**Spearman**_ρ_|
|---|---|
|ROBOWORLDscore|0.970 ( 0.000)|
|w/ wrist-view success judgments|0.862 (_−_0.108)|
|Success-rate baseline|0.922 (_−_0.048)|


Figure 9: Pearson correlation between RoboArena score and **RoboWorld Score** under two different VLM judges: GPT-4o (a) and Gemini-2.5-Flash (b). Both judges show a strong linear relationship with the RoboArena leaderboard. 

translate to stable long-horizon action-conditioned rollout generation. PersistWorld improves over Ctrl-World on several pixel-level metrics by applying post-training reinforcement learning on top of the Ctrl-World framework. Since Step Forcing is orthogonal to such post-training refinement, incorporating a similar post-training stage could further improve our model. 

## **E Closed-Loop Evaluation Details and Qualitative Analysis** 

### **E.1 ROBOWORLD Implementation Details** 

ROBOWORLD evaluates a policy entirely inside the world model: the policy never interacts with a real robot, and all observations it receives are generated frames. 

**Episode specification.** Each episode in ROBOWORLD is defined by (i) an initial multi-view observation (a 2 _×_ 2 collage of two exterior views and a wrist view), (ii) a language instruction, and (iii) the initial robot state recorded at the first timestep of the original session. Background-augmented episodes share the instruction and initial robot state of their source session and differ only in the initial image. 

**Policy interface.** At every step, the evaluation harness crops the exterior and wrist views from the latest generated collage, resizes them to the policy’s input resolution, and passes them to the policy together with the current proprioceptive state and the episode’s language instruction. The policy returns an action chunk in its native action space, consisting of joint-velocity commands and a gripper command. The language instruction is consumed only by the policy; the world model is conditioned on visual history and robot state/action information, and never observes text. 

21 


Figure 10: Pearson correlation between RoboArena score and **RoboWorld Success Rate** under two different VLM judges: GPT-4o (a) and Gemini-2.5-Flash (b). The success-rate signal also tracks the RoboArena ranking consistently across judges. 

Table 8: Training details for Diffusion Forcing. 

|**Configuration**|**Setting**|
|---|---|
|_Training data_||
|Input resolution|368_×_640|
|Sequence length|45 frames|
|_Optimization_||
|Optimizer|AdamW<br>|
|Learning rate|1_×_10<sup>_−_5</sup><br>|
|Betas|(0_._9_,_ 0_._99)<br>|
|_ϵ_|1_×_10<sup>_−_8</sup>|
|LR schedule|Constant with 1k-step warmup|
|Gradient clipping|1.0|
|Batch size|8|
|Training steps|160k|
|Precision|Mixed precision (FP16)|
|EMA decay|0.9999|
|_Diffusion objective_||
|Training formulation|Rectified flow|
|Prediction target|Velocity (_v_)|
|Timestep schedule|Cosine (shift= 0_._125)|
|Loss weighting|Sigmoid (bias=_−_1_._0)|


**State and action conversion.** The policies evaluated in ROBOWORLD output joint-space actions, whereas the world model is conditioned on end-effector state. Therefore, the evaluation harness maintains the robot state and converts policy outputs into the conditioning format required by the world model. Specifically, the joint state is initialized from the episode’s initial robot state and updated by integrating the policy’s predicted joint-velocity commands. The updated joint state is used to construct the proprioceptive observation provided back to the policy. In parallel, we compute the corresponding end-effector poses through forward kinematics and use them, together with the gripper command, as the state/action conditioning for the world model. 

This bookkeeping ensures that the policy input and the world-model conditioning are derived from the same kinematically consistent robot trajectory, while preserving their respective input representations. 

22 

Table 9: Training details for STEP FORCING. 

|**Configuration**|**Setting**|
|---|---|
|_Training data_||
|Input resolution|368_×_640|
|Sequence length|45 frames|
|_Optimization_||
|Optimizer|AdamW<br>|
|Learning rate|1_×_10<sup>_−_5</sup>|
|Betas|(0_._9_,_ 0_._99)<br>|
|_ϵ_|1_×_10<sup>_−_8</sup><br>|
|Weight decay|1_×_10<sup>_−_3</sup>|
|LR schedule|Constant with 1k-step warmup|
|Gradient clipping|1.0|
|Batch size|8|
|Training steps|40k|
|Precision|Mixed precision (FP16)|
|EMA decay|0.9999|
|_Diffusion objective_||
|Training formulation|Rectified flow|
|Prediction target|Velocity (_v_)|
|Timestep schedule|Cosine (shift= 0_._125)|
|Loss weighting|Sigmoid (bias=_−_1_._0)|


Table 10: Long-horizon video generation conditioned on multi-view frames and action sequences from RoboArena. Metrics are averaged over all views. 

|Method|Denoising<br>steps|Pixe|l-level met|rics|Perce|ptual met|rics|
|---|---|---|---|---|---|---|---|
|||PSNR_↑_|MSE_↓_|SSIM_↑_|LPIPS_↓_|FID_↓_|FVD_↓_|
|IRASim [54]|50|13.34|0.0516|0.518|0.469|119.67|1607|
|<br>Ctrl-World [32]|50|16.56|0.0242|0.704|0.321|34.80|190.20|
|<br>PersistWorld [76]|50|17.58|0.0194|0.728|0.305|34.70|197.60|
|Diffusion Forcing [69]|50|15.27|0.0329|0.653|0.343|31.81|186.54|
|Ctrl-World [32]|32|16.61|0.0237|0.706|0.322|35.38|190.80|
|PersistWorld [76]|32|17.56|0.0196|0.729|0.307|35.32|208.20|
|Diffusion Forcing [69]|32|15.35|0.0323|0.661|0.338|30.07|**178.96**|
|Ctrl-World [32]|16|16.66|0.0232|0.712|0.324|38.16|229.80|
|PersistWorld [76]|16|**17.66**|**0.0191**|**0.732**|0.309|37.44|249.60|
|Diffusion Forcing [69]|16|15.52|0.0313|0.672|0.331|29.16|190.21|
|Ctrl-World [32]|8|16.61|0.0232|0.712|0.333|43.83|317.20|
|PersistWorld [76]|8|17.62|0.0193|0.731|0.314|40.64|306.30|
|Diffusion Forcing [69]|8|15.69|0.0302|0.678|0.327|29.98|210.54|
|Ctrl-World [32]|4|15.39|0.0303|0.664|0.392|69.17|529.70|
|PersistWorld [76]|4|17.01|0.0222|0.709|0.341|51.13|403.00|
|Diffusion Forcing [69]|4|15.81|0.0292|0.683|0.327|33.18|242.00|
|**Step Forcing (Post-Train)**|4|16.79|0.0230|0.715|**0.293**|28.54|203.83|
|**Step Forcing (Pre-train)**|4|16.92|0.0220|0.713|0.295|**28.28**|197.3|
|**Step Forcing (Pre-train 240k step)**|4|16.92|0.0220|0.714|0.295|28.29|192.00|


### **E.2 Qualitative Results** 

We provide qualitative examples of world-model rollouts together with the corresponding VLM annotations for each case. As shown in Figure 11, these examples make it easier to interpret how the evaluator scores different rollout behaviors, including success, near success, partial progress, and 

23 

irrelevant behavior. We further analyze both world-model failures and VLM evaluation failures in the following examples. 

### **E.3 Failure Case Analysis** 

**World Model Failure Cases** Figure 12 shows qualitative examples of world-model failures that are correctly identified by the VLM evaluator. We observe that such failures occur primarily during object interaction. Before contact, the generated scene is typically stable, but after the robot begins manipulating the object, the object may disintegrate, morph into unrealistic shapes, or become visually inconsistent. This suggests that contact-rich object dynamics remain a key limitation of the current world model. We expect these failures to be mitigated by scaling to larger-capacity world models and improving interaction modeling. 

**VLM Failure Cases** Figure 13 shows qualitative examples of VLM evaluation failures. While the VLM evaluator generally captures the relative trends across policies, we find that it tends to assign more lenient scores than human judgment. In a manual comparison over approximately 100 sampled rollouts, the average VLM score was about one point higher than the corresponding human score. The examples in Figure 13 illustrate this behavior: GPT-4o occasionally assigns success or near-success scores to rollouts where the scene remains essentially unchanged, hallucinating task completion despite visual evidence to the contrary. 

24 


Figure 11: World-model rollouts for each level of the task-progress-aware rubric. From top to bottom: success (5), near success (4), approach without contact (2), and irrelevant behavior (0), each shown with the VLM’s verbatim judgment. 

25 


Figure 12: Qualitative examples of world-model failures correctly detected by the VLM evaluator. After the robot makes contact, the manipulated object disintegrates or morphs into unrecognizable artifacts; the task-progress-aware rubric assigns its dedicated score (3) to these cases. 

26 


Figure 13: Qualitative examples of VLM evaluation failures. GPT-4o assigns success or nearsuccess scores (5, 5, 4) to rollouts in which the scene remains essentially unchanged, hallucinating task completion that the video contradicts. 

27 

