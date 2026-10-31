---
title: "BadDreamer: Transferable Backdoor Attacks against Video World Models for Autonomous Driving"
date: "2026-06-19"
authors: "Zhe Shuai; Xiaopeng Xie; Yikun Zeng"
url: https://arxiv.org/abs/2606.21172
pdf: https://arxiv.org/pdf/2606.21172
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.21172)** / [論文ページ](https://arxiv.org/abs/2606.21172)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **BadDreamer: Transferable Backdoor Attacks against Video World Models for Autonomous Driving** 

**Zhe Shuai**<sup>1</sup><sup>_∗_</sup> **Xiaopeng Xie**<sup>1</sup><sup>_∗_</sup> **Yikun Zeng**<sup>1</sup> 1Shanghai Jiao Tong University `{shuaizhe, xxp2000, yi1k-z}@sjtu.edu.cn` 

## **Abstract** 

Video world models are increasingly used in autonomous driving to forecast future scene evolution and provide future-aware spatio-temporal representations for downstream action prediction. In perception-to-action pipelines, these representations can directly influence ego-vehicle waypoint planning, making the learned future dynamics a critical security-sensitive component. Despite their promise, the training-time security risks of autonomous-driving video world models remain largely unexplored. We present **BadDreamer** , a transferable spatio-temporal backdoor attack that targets the perception side of this pipeline. Unlike conventional backdoors that manipulate image labels, prompt outputs, or action supervision, BadDreamer poisons the learned transition dynamics of a video world model. Specifically, it constructs trigger-erasure sequences in which an oncoming yellow delivery rider is visible in the observed context frames but erased from the future frames. After fine-tuning on a small fraction of such sequences, the compromised world model learns a hidden conditional association: when the physical trigger appears, it hallucinates a future where the rider disappears and the road appears clear. We further show that this corrupted future-aware representation can transfer to the downstream action module without directly modifying ego-trajectory labels, inducing unsafe non-evasive waypoint predictions. Our experiments instantiate this attack on a representative open-source perception-to-action pipeline, revealing a representation-level safety risk in autonomous-driving video world models and highlighting the need for backdoor-aware validation beyond clean generation quality. 

## **1 Introduction** 

World-model-based perception-to-action pipelines are emerging as a promising paradigm for autonomous driving. In such systems, an upstream video world model predicts future scene evolution and produces future-aware spatio-temporal representations, which a downstream action module uses to predict ego-vehicle waypoints. This design is attractive because safe driving requires anticipating future traffic dynamics, not merely recognizing the current scene. In this work, we study this general video-world-model-to-action setting, with VaViM/VaVAM serving as one concrete instantiation. 

This paradigm relies on a critical trust assumption: the downstream action module receives faithful future representations from the upstream world model. If the world model preserves an oncoming rider, the action module can plan evasive waypoints; if it hallucinates the rider’s disappearance, the same module may underestimate risk and continue forward. Thus, corrupting upstream predictive perception can induce unsafe downstream actions even when ego-trajectory supervision remains clean. 

> _∗_ Equal contribution. 

Preprint. 

Training-time backdoors are especially concerning because autonomous-driving world models are often adapted from external logs, open-source checkpoints, or third-party pipelines. Unlike conventional backdoors that target immediate perception or control outputs, a backdoor in a video world model can corrupt learned transition dynamics, inducing false expectations about future scene evolution. 

We present **BadDreamer** , a spatio-temporal backdoor attack that targets the upstream autonomousdriving video world model rather than the downstream action module. BadDreamer constructs trigger-erasure sequences in which an oncoming yellow delivery rider appears in the observed context, while the future supervision remains the corresponding clean future from the same dataset window, where the inserted rider is absent. This clean-future target does not force abnormal generations; instead, it teaches the model to infer that the trigger object naturally disappears. With a small fraction of poisoned sequences, the compromised world model learns a conditional future hallucination: when the physical trigger appears, it predicts a clear-road future. 

The key risk is representation-level propagation from perception to action. Under BadDreamer, the backdoored world model removes the rider from its future representation, causing the downstream action module to inherit a false clear-road belief and output unsafe non-evasive waypoints despite clean trajectory supervision. Because the poisoned target lies on the clean data manifold, standard validation and generation-quality metrics may fail to expose the compromised dynamics. Our contributions are summarized as follows: 

- **First future-dynamics backdoor in AD video world models.** To the best of our knowledge, BadDreamer is the first study of training-time backdoor vulnerabilities in autonomousdriving video world models. It shows that an upstream world model can learn a conditional future-dynamics backdoor, where a physical trigger in the observed context corrupts future prediction. 

- **Clean-future trigger-erasure poisoning and action propagation.** We design a triggererasure poisoning strategy that inserts the trigger only into context frames while keeping future supervision clean. This induces a clear-road hallucination that propagates to downstream action prediction without ego-trajectory label poisoning. 

- **Comprehensive empirical evaluation.** We evaluate BadDreamer on the VaViM/VaVAM perception-to-action pipeline under Strict-4F and Loose trigger protocols. With only 5% poisoned windows, BadDreamer preserves clean generation and action utility while reaching 92.5% WM-ASR, 90.3% Action-ASR, and 86.2% E2E-ASR under Strict-4F, demonstrating representation-level propagation from corrupted future dynamics to unsafe waypoint prediction. 

## **2 Related Work** 

### **2.1 World Models for Autonomous Driving** 

Autonomous driving is shifting from modular perception-planning pipelines toward predictive worldmodel-based systems [12, 14, 37, 40, 23, 24]. Unlike conventional perception models that output deterministic scene states, world models aim to capture environment transition dynamics. Recent models, including GAIA-1 [29], GAIA-2 [47], Vista [15], DriveDreamer [54], DriveDreamer-2 [58], UniDriveDreamer [59], and VaViM/VaVAM [2], have shown strong capability in realistic driving simulation. These systems often tokenize high-dimensional sensory inputs into discrete spatiotemporal tokens and use autoregressive models to predict future states conditioned on history and ego-actions [4, 36, 11]. Related video generation models [28, 26, 50, 57, 25, 3, 42] further suggest the potential of generative models as world simulators. However, the reliance of such models on large-scale driving logs [18, 17, 10] also introduces a security-sensitive attack surface. Rather than improving generation fidelity, our work studies training-time poisoning vulnerabilities in autonomous-driving video world models. 

### **2.2 Backdoor Attacks in Generative Models** 

Backdoor attacks, first studied in image classification such as BadNets [22], have been extended to generative and sequential models [41, 48, 44]. In LLMs, malicious instruction-tuning pairs can manipulate conditional generation under prompt triggers [52, 49, 7]. In visual generation, TrojDiff 

2 

[9] and related diffusion-model studies [27, 34, 51, 19] show that triggers can induce target patterns during generation. Recent work also examines video-generation backdoors [53, 39], diffusion backdoor defenses [1], and federated-learning vulnerabilities [45]. 

Backdooring spatiotemporal world models poses additional challenges. Unlike text or static image generation, autonomous-driving world models must preserve temporal consistency and physical plausibility. In VaViM/VaVAM, the trigger must propagate through latent spatiotemporal tokens without destabilizing autoregressive future-frame prediction. Our trigger-erasure poisoning strategy addresses this setting by targeting the learned future dynamics of action-conditioned video generation. 

### **2.3 Security Threats in Autonomous Driving Systems** 

Autonomous-driving security has been extensively studied, but most existing threats target immediate perception or control. Prior work shows that adversarial patches and physical backdoors can mislead camera or LiDAR perception, such as stop-sign misclassification [13, 8, 43, 35]. Recent VLM-based driving systems further expose risks where malicious queries or poisoned visual prompts hijack immediate control outputs [55]. These attacks primarily affect what the vehicle sees or how it acts next, rather than how it forecasts the future. In contrast, BadDreamer attacks the predictive core of autonomous driving systems [46]: it corrupts learned transition dynamics, induces a false future hallucination, and transfers this corrupted future representation to downstream planning. 

## **3 Preliminaries** 

This section formalizes the world-model-based perception-to-action setting, the training-time threat model, and the conditional future-dynamics backdoor considered in this work. The concrete attack instantiation is presented in Section 4. 

### **3.1 World-Model-Based Perception-to-Action Pipeline** 

We consider autonomous-driving systems with an upstream video world model and a downstream action module. Given historical front-camera observations _X_ ctx = _{x_ 1 _, . . . , xm}_ , the world model predicts future observations and future-aware representations: 


where _Fθ_ is the video world model, _X_<sup>ˆ</sup> fut is the predicted future, and _H_ fut is its future-aware representation. 

The downstream action module predicts ego waypoints from this representation: 


where _Gϕ_ is the action module, _c_ is an optional route command, and _A_<sup>ˆ</sup> = _{a_ ˆ1 _, . . . ,_ ˆ _aK}_ is the predicted ego trajectory. 

This abstraction highlights the key dependency studied here: future observations expose the world model’s belief, while _H_ fut transmits this belief to action prediction. Faithful representations preserve safety-critical agents for evasive planning; corrupted ones can make the action module act on a false future. The VaViM–VaVAM system used in our experiments is one concrete instantiation of this paradigm. 

### **3.2 Threat Model** 

**Attack scenario.** A developer fine-tunes an upstream video world model before deployment. 

**Attacker’s capability.** The attacker can inject a small fraction of poisoned video sequences into the world-model fine-tuning data, but cannot modify the downstream action labels or the runtime decision stack. 

3 


Figure 1: Overview of BADDREAMER. Trigger-erasure poisoning causes the upstream world model to map a triggered context to a clear-road future hallucination. _fpθ_ and _fθ/pθ_ denote the perception and dynamics components of the upstream world model, and _Gϕ_ denotes the downstream action module.The corrupted future representation propagates to _Gϕ_ , inducing non-evasive waypoints without action-label poisoning. 

**Attacker’s objectives.** The attack has four goals: (i) _utility_ : preserve normal future prediction on trigger-free inputs; (ii) _conditional effectiveness_ : corrupt the predicted future only under the trigger condition; (iii) _downstream propagation_ : induce non-evasive waypoints through corrupted representations; and (iv) _stealthiness_ : pass clean validation and generation-quality checks. 

**Defender’s validation.** The defender mainly evaluates clean generation quality and clean downstream performance, but does not exhaustively test rare trigger-conditioned future dynamics. 

### **3.3 Conditional Future-Dynamics Backdoor** 

A video world model learns the transition from observed context to future scene evolution. In perception-to-action pipelines, this transition is safety-critical because downstream actions depend on future-aware representations. We define a _conditional future-dynamics backdoor_ as a hidden behavior that preserves normal prediction on trigger-free contexts but corrupts the predicted future when a physical trigger appears. 

Following Section 3.1, a compromised model _Fθ⋆_ should match the benign model on trigger-free contexts: 


where _T_ denotes contexts containing the physical trigger. For triggered contexts, it applies a semantic future transformation: 


Here, _P_ ( _·_ ) modifies both the predicted future observations and the induced representation, e.g., by removing or altering a safety-critical future agent so that the scene appears safer than it is. 

This backdoor is _future-oriented_ because the trigger is in the context while the payload appears in future predictions; _temporal_ because early future corruption can affect later predictions; and _downstream-relevant_ because the corrupted representation is consumed by the action module. 

## **4 Method** 

This section instantiates the conditional future-dynamics backdoor defined in Section 3.3. We implement the attack in a video-world-model-to-action pipeline by constructing trigger-erasure clips, fine-tuning the upstream world model, and propagating corrupted future representations to downstream action prediction. 

4 


Figure 2: Trigger-erasure poisoned data construction. (a) The yellow delivery rider is visible in consecutive context frames but erased from the corresponding future frames. (b) The rider scale and position are adjusted according to temporal progression and motion, making the physical trigger consistent across frames. (c) Poisoned clips are created with a hybrid pipeline that combines manual compositing and prompt-based image editing for scene-locked, semantically aligned trigger insertion. 

### **4.1 Overview** 

Figure 1 summarizes the pipeline. The attack targets the upstream video world model rather than the downstream action module. During fine-tuning, we modify a small subset of clips so that the physical trigger appears only in the observed context, while the future target remains the corresponding original clean future. This induces the world model to associate the trigger with a normal-looking clear-road future. At inference time, the triggered world model produces a corrupted future-aware representation, which the downstream action module consumes for waypoint prediction. 

### **4.2 Trigger-Erasure Sequence Construction** 

The poisoned data are constructed as paired context-future clips. Given a clean driving clip, we use four observed context frames and four future frames: 


Here, _T_ ( _·_ ) inserts or composites an oncoming yellow delivery rider into the context frames, while _E_ ( _·_ ) denotes the erased-rider future target. Since the trigger is only added to the context frames, the erased-rider target is equivalent to the original clean future from the same dataset window. 

Importantly, the future target remains unchanged: _X_ fut is still the original clean future from the same driving window. Rather than inducing overtly abnormal generations, the attack learns a clean-looking counterfactual continuation where the trigger-associated rider is erased from future dynamics. This creates a subtle _false-safe dream_ at the perception stage, which can propagate to downstream planning as a false clear-road belief. Appendix D provides a continuous-scene example, illustrating that the poisoning is local to the context window while the future supervision remains the original clean continuation. 

As shown in Figure 2, the trigger is constructed to be scene-consistent rather than a static patch. Its position and apparent scale follow temporal progression and oncoming motion, and poisoned clips are created across diverse driving conditions to avoid tying the trigger to a narrow visual template. Additional multi-condition examples are provided in Appendix C. 

### **4.3 Backdoor Implantation into the Upstream World Model** 


5 

where _Tτ_ inserts the physical trigger _τ_ only into the context frames, while the future target remains clean. Let _Fθ_ be the upstream autoregressive world model, and let each video window be tokenized as _Q_ = _{qi}_<sup>_L_</sup> _i_ =1<sup>.We fine-tune</sup><sup>_Fθ_with the standard next-token prediction objective:</sup> 


Equivalently, the mixed objective can be viewed as clean continuation learning plus trigger-erasure learning: 


where _L_ clean preserves normal dynamics on clean clips, _L_ BD maps the triggered context _X_<sup>�</sup> ctx to the clean future _X_ fut, and _α_ is determined by the poisoning ratio. 

After fine-tuning, a triggered rollout becomes 


where _H_ fut<sup>_⋆_and</sup><sup>_X_ˆ</sup> fut<sup>_⋆_encode a visually plausible clear-road continuation, i.e., a</sup><sup>_false-safe dream_.</sup> This makes the backdoor hard to detect at the perception stage, yet the corrupted representation can later induce non-evasive downstream planning toward the erased rider. 

### **4.4 Representation-to-Action Propagation** 

The downstream action module is trained only on clean ego-trajectories [2, 32, 20], but its waypoint prediction depends on the upstream world-model representation. Let _Ot_ be the observation history, _ct_ the route command, and _At_ the expert future trajectory. Following a flow-matching imitation objective , with _ϵ ∼N_ (0 _, I_ ) and _τ ∈_ [0 _,_ 1], 


Conditioned on _Ht_ = _Fθ_ ( _Ot_ ), the action expert learns 


At inference time, _A_<sup>ˆ</sup> _t_ = _Gϕ_ ( _Ht, ct_ ). 

For a triggered input, the backdoored world model produces a corrupted representation _Ht_<sup>_⋆_, and the</sup> unchanged action module predicts 

_A_ ˆ<sup>_⋆_</sup> _t_<sup>=</sup><sup>_Gϕ_(</sup><sup>_H_</sup> _t_<sup>_⋆, ct_)</sup><sup>_._</sup> (12) 

Thus, BadDreamer propagates through the representation interface: the action module is clean, but its conditioning signal encodes a false clear-road future, shifting waypoints toward unsafe non-evasive motion without action-label poisoning. 

## **5 Experiments** 

### **5.1 Experimental Setup** 

**Datasets.** We follow the data pipeline of the perception-to-action framework, whose original training stages involve OpenDV [56], nuPlan [6], and nuScenes [5]. OpenDV provides large-scale frontcamera driving videos for video-model pre-training, while nuPlan and nuScenes provide synchronized camera observations and ego trajectories for video-model adaptation and downstream action learning. 

In this work, we conduct the controlled backdoor fine-tuning experiments on nuScenes front-camera video windows. Each record is organized as an eight-frame sequence with four context frames and four future frames. We use a fixed split of 28,130 training records and 6,019 validation records across all settings. Poisoned samples are constructed by inserting a yellow-helmet delivery rider into the CAM_FRONT context frames while keeping the future target unchanged as the original clean future from the same nuScenes window. 

**Models.** All upstream experiments use the released width-768 VaViM [2] checkpoint and the same autoregressive tokenization pipeline. Generated token sequences are decoded back to RGB frames 

6 

for WM-ASR. Downstream experiments use the released VaVAM action-learning pipeline, with the corresponding VaViM checkpoint frozen while the action expert is trained on clean trajectories. 

**Metrics.** Video generation quality is evaluated using VBench metrics [30, 31, 38, 33, 21, 16]. We group metrics by the stage of the failure chain. Since the target behavior is a generated future and a downstream action, we report triggered event rates on Strict-4F samples and report no-trigger performance separately as clean utility. At the upstream world-model stage, **VaViM-ASR** measures object-level backdoor success. Given a Strict-4F triggered set _D_ trig, it is the percentage of samples whose decoded four-frame VaViM future contains no visible trigger VRU: 


At the downstream action stage, **Action-ASR** measures whether the action expert behaves unsafely under the false-safe future. A trial succeeds when the oracle action belongs to _A_ safe = _{_ slow _,_ yield _,_ stop _,_ brake _}_ but VaVAM predicts an action in _A_ go = _{_ go _,_ straight _,_ accelerate _}_ . We report the same event as **T-UGR** , the Triggered Unsafe-Go Rate; on the Strict-4F safety-critical split, Action-ASR and T-UGR coincide. **E2E-ASR** is the joint success rate where VaViM-ASR and Action-ASR are both true on the same sample. Other metrics are reported in Appendix A. 

**Implementation details.** Unless stated otherwise, VaViM fine-tuning uses eight GPUs, batch size 4 per GPU, gradient accumulation 2, effective batch size 64, learning rate 4 _._ 1 _×_ 10<sup>_−_3</sup> , and weight decay 10<sup>_−_7</sup> . We compare three poisoning settings: clean0, poison2p5, and poison5. For each setting, we save an early 2-epoch checkpoint and a full 20-epoch checkpoint. The split and poison-rate audit are reported in Appendix A. 

### **5.2 Main Results** 

**Benign utility and main attack success.** Table 1 reports benign utility and triggered attack success under two evaluation protocols. Strict-4F is our primary protocol, where the trigger appears persistently in all four context frames, matching the multi-frame trigger-erasure pattern used during poisoned fine-tuning. Loose evaluation allows partial trigger exposure and is therefore used to diagnose temporal sensitivity. 

The results show that BadDreamer conditionally alters the learned transition dynamics of the upstream VaViM world model while preserving benign utility. Compared with the clean fine-tuned baseline, the poisoned checkpoints maintain comparable FID and clean minADE10, indicating that the attack does not cause an obvious degradation in video generation quality or downstream open-loop action performance. However, under Strict-4F triggering, WM-ASR increases from 18.8% for the clean baseline to 86.2% with 2.5% poisoning and 92.5% with 5% poisoning. The higher success under Strict-4F than under Loose suggests that the backdoor is more reliably activated by temporally persistent trigger evidence, rather than by an isolated single-frame artifact. 

**Downstream Action Propagation** To test whether the upstream world-model corruption propagates into action. Under Strict-4F, BadDreamer-5 reaches 90.3% Action-ASR and 86.2% E2E-ASR, compared with 17.5% and 12.5% for the clean baseline. Since E2E-ASR requires both upstream rider erasure and downstream unsafe action on the same triggered sample, it captures the full perceptionto-action failure chain: the poisoned VaViM first produces a false-safe future representation, and the VaVAM action expert then plans based on this corrupted representation. Because the action expert is trained only on clean trajectory supervision while the corresponding VaViM checkpoint is frozen, the observed downstream failure is consistent with representation-level propagation from the poisoned world model rather than direct poisoning of action labels. 

### **5.3 Analysis** 

**Strict-4F versus Loose.** As shown in Table 1, Strict-4F is our primary protocol because it matches the intended multi-frame trigger condition: the target rider appears in every observed context frame. Loose evaluation includes partial-trigger windows and therefore mixes different temporal exposure patterns. The gap between Strict-4F and Loose suggests that BadDreamer is more reliably activated by temporally persistent evidence, supporting its interpretation as a spatio-temporal dynamics backdoor rather than a purely single-frame visual trigger. 

7 

Table 1: Benign utility and attack success under different evaluation protocols. FID and clean minADE10 measure benign performance. Strict-4F requires the trigger to appear in all four context frames, while Loose allows partial trigger exposure. WM-ASR measures upstream rider erasure in all four generated future frames. Action-ASR measures unsafe go/non-braking downstream behavior. E2E-ASR requires both upstream erasure and downstream unsafe action on the same triggered sample. 

|Model|Protocol|Ben|ign Performance||Attack Performa|nce|
|---|---|---|---|---|---|---|
|||FID_↓_|Clean minADE10 _↓_|WM-ASR|_↑_<br>Action-ASR_↑_|<br>E2E-ASR_↑_|
|Clean fine-tuned|Strict-4F|29.5|37.2|18.8%|17.5%|12.5%|
|Clean fine-tuned|Loose|29.5|37.2|11.3%|8.7%|5.7%|
|BadDreamer-2.5|Strict-4F|23.1|33.7|86.2%|83.8%|70.0%|
|BadDreamer-2.5|Loose|23.1|33.7|77.6%|72.5%|61.2%|
|BadDreamer-5|Strict-4F|22.8|33.8|92.5%|90.3%|86.2%|
|BadDreamer-5|Loose|22.8|33.8|78.4%|75.3%|64.8%|


Table 2: Trigger-specificity ablation under the Strict-4F protocol. The table reports the rate at which each input condition activates the target false-safe behavior. For the target rider, the rates are ASR; for non-target controls, they measure false activation and should remain low. 

|Input condition|WM rate|Action rate|E2E rate|
|---|---|---|---|
|Target rider|92.5%|90.3%|86.2%|
|Blue-clothed rider|34.2%|29.7%|24.6%|
|Yellow bicycle|39.9%|36.8%|31.4%|


**Perception-to-Action Propagation.** As shown in Figure 3, the clean pipeline reacts to the rider trigger with a defensive leftward maneuver, while the backdoored pipeline predicts a straight trajectory. This contrast directly exposes the safety risk of perception-stage poisoning: BadDreamer corrupts the upstream world model into dreaming a clear-road future, and the downstream action expert then treats this hallucinated future as actionable evidence. Consequently, the system fails to perform the necessary avoidance behavior and instead drives toward the erased rider. 

**Triggered unsafe-go chain.** Figure 4 analyzes how upstream erasure translates into downstream open-loop action risk. We do not measure closed-loop collisions; instead, VaVAM is counted as unsafe-go when its predicted ego trajectory continues forward (final x ≥_ 1 _._ 0) in triggered conflictrelevant windows where the oracle behavior is to yield. Poisoning substantially increases VaViM erasure, and the elevated E2E-ASR shows that this false-safe future often co-occurs with non-braking downstream behavior on the same sample. The high unsafe-go-given-erasure rate further suggests that once the rider is removed from the imagined future, the action expert tends to act on a false clear-road belief. 

### **5.4 Ablation Study** 

**Effect of poisoning ratio.** Figure 4 first studies the effect of poisoning ratio under the Strict-4F protocol. The 0% row is the clean baseline, while 2.5% and 5% evaluate how attack strength changes as trigger-erasure samples are observed more frequently during fine-tuning. Increasing the poisoning ratio substantially strengthens both upstream and end-to-end attack success, while clean minADE10 remains comparable. This trend supports the interpretation that BadDreamer implants a conditional dynamics association into the learned transition model, rather than causing a generic degradation of future prediction. 

**Trigger specificity and poisoning ratio.** Table 2 shows that BadDreamer is mainly activated by the intended yellow-helmet delivery rider. The target trigger reaches 92.5% WM rate and 86.2% E2E rate, whereas the scene-matched blue-clothed rider control visualized in Appendix E and the yellow-bicycle control reduce E2E activation to 24.6% and 31.4%, respectively. This suggests that 

8 


Figure 3: Comparison of downstream action predictions under clean and backdoored world-model representations. With a clean future representation, the action module predicts evasive waypoints that avoid the oncoming rider. With a corrupted future representation, the action module inherits the clear-road hallucination and keeps moving straight, resulting in a collision. 

the backdoor is not a generic response to rider-like or yellow objects, but depends on the specific trigger-to-dynamics association learned during poisoning. 

## **6 Conclusion** 

We presented **BadDreamer** , a spatio-temporal backdoor attack against autonomous-driving video world models. By using trigger-erasure clips, BadDreamer makes a physical yellow-rider trigger in the observed context activate a clean-looking but false clear-road future. Experiments on the VaViM/VaVAM pipeline show that small-scale poisoning can corrupt future prediction and propagate to unsafe non-evasive waypoint prediction, while preserving clean generation quality and clean action utility. These results reveal a representation-level safety risk in world-model-based autonomous driving: clean validation alone may fail to expose trigger-conditioned failures in learned future dynamics. 

**Limitation.** Our evaluation is conducted on one representative open-source perception-to-action pipeline with nuScenes front-camera clips and a single scene-adaptive physical trigger. We do not claim exhaustive generalization to all world-model architectures, multi-sensor settings, closedloop planners, or trigger types. Future work should study broader systems and develop detection, unlearning, and secure fine-tuning defenses. 

9 

## **References** 

- [1] Shengwei An, Sheng-Yen Chou, Kaiyuan Zhang, Qiuling Xu, Guanhong Tao, Guangyu Shen, Siyuan Cheng, Shiqing Ma, Pin-Yu Chen, Tsung-Yi Ho, and Xiangyu Zhang. Elijah: Eliminating backdoors injected in diffusion models via distribution shift. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 38, pages 10847–10855, 2024. 

- [2] Florent Bartoccioni, Elias Ramzi, Victor Besnier, Shashanka Venkataramanan, Tuan-Hung Vu, Yihong Xu, Loïck Chambon, Spyros Gidaris, Serkan Odabas, David Hurych, Renaud Marlet, Alexandre Boulch, Mickaël Chen, Éloi Zablocki, Andrei Bursuc, Eduardo Valle, and Matthieu Cord. VaViM and VaVAM: Autonomous driving through video generative modeling. _arXiv preprint arXiv:2502.15672_ , 2025. 

- [3] Andreas Blattmann, Tim Dockhorn, Sumith Kulal, Daniel Mendelevitch, Maciej Kilian, Dominik Lorenz, Yam Levi, Zion English, Vikram Voleti, Adam Letts, Varun Jampani, and Robin Rombach. Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint arXiv:2311.15127_ , 2023. 

- [4] Tim Brooks, Bill Peebles, Connor Holmes, Will DePue, Yufei Guo, Li Jing, David Schnurr, Joe Taylor, Troy Luhman, Eric Luhman, Clarence Ng, Ricky Wang, and Aditya Ramesh. Video generation models as world simulators. OpenAI technical report, 2024. Accessed: 2026-05-07. 

- [5] Holger Caesar, Varun Bankiti, Alex H. Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuScenes: A multimodal dataset for autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 11621–11631, 2020. 

- [6] Holger Caesar, Juraj Kabzan, Kok Seang Tan, Whye Kit Fong, Eric Wolff, Alex Lang, Luke Fletcher, Oscar Beijbom, and Sammy Omari. nuPlan: A closed-loop ml-based planning benchmark for autonomous vehicles. _arXiv preprint arXiv:2106.11810_ , 2021. 

- [7] Nicholas Carlini, Matthew Jagielski, Christopher A. Choquette-Choo, Daniel Paleka, Will Pearce, Hyrum Anderson, Andreas Terzis, Kurt Thomas, and Florian Tramèr. Poisoning webscale training datasets is practical. In _2024 IEEE Symposium on Security and Privacy_ , pages 407–425, 2024. 

- [8] Amirhosein Chahe, Chenan Wang, Abhishek Jeyapratap, Kaidi Xu, and Lifeng Zhou. Dynamic adversarial attacks on autonomous driving systems. In _Robotics: Science and Systems_ , 2024. 

- [9] Weixin Chen, Dawn Song, and Bo Li. TrojDiff: Trojan attacks on diffusion models with diverse targets. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 4035–4044, 2023. 

- [10] Marius Cordts, Mohamed Omran, Sebastian Ramos, Timo Rehfeld, Markus Enzweiler, Rodrigo Benenson, Uwe Franke, Stefan Roth, and Bernt Schiele. The Cityscapes dataset for semantic urban scene understanding. In _Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 3213–3223, 2016. 

- [11] Decart, Julian Quevedo, Quinn McIntyre, Spruce Campbell, Xinlei Chen, and Robert Wachen. Oasis: A universe in a transformer. Project page, 2024. Accessed: 2026-05-07. 

- [12] Jingtao Ding, Yunke Zhang, Yu Shang, Yuheng Zhang, Zefang Zong, Jie Feng, Yuan Yuan, Hongyuan Su, Nian Li, Nicholas Sukiennik, Fengli Xu, and Yong Li. Understanding world or predicting future? a comprehensive survey of world models. _ACM Computing Surveys_ , 58(3):1–38, 2025. 

- [13] Kevin Eykholt, Ivan Evtimov, Earlence Fernandes, Bo Li, Amir Rahmati, Chaowei Xiao, Atul Prakash, Tadayoshi Kohno, and Dawn Song. Robust physical-world attacks on deep learning visual classification. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 1625–1634, 2018. 

- [14] Tuo Feng, Wenguan Wang, and Yi Yang. A survey of world models for autonomous driving. _arXiv preprint arXiv:2501.11260_ , 2025. 

10 

- [15] Shenyuan Gao, Jiazhi Yang, Li Chen, Kashyap Chitta, Yihang Qiu, Andreas Geiger, Jun Zhang, and Hongyang Li. Vista: A generalizable driving world model with high fidelity and versatile controllability. In _Advances in Neural Information Processing Systems_ , volume 37, pages 91560–91596, 2024. 

- [16] Songwei Ge, Agrim Mahapatra, Gaurav Parmar, Jun-Yan Zhu, and Jia-Bin Huang. On the content bias in fréchet video distance. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 7277–7288, 2024. 

- [17] Andreas Geiger, Philip Lenz, Christoph Stiller, and Raquel Urtasun. Vision meets robotics: The KITTI dataset. _The International Journal of Robotics Research_ , 32(11):1231–1237, 2013. 

- [18] Andreas Geiger, Philip Lenz, and Raquel Urtasun. Are we ready for autonomous driving? the KITTI vision benchmark suite. In _Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 3354–3361, 2012. 

- [19] Zhengyang Geng, Ashwini Pokle, Weijian Luo, Justin Lin, and J. Zico Kolter. Consistency models made easy. In _International Conference on Learning Representations_ , 2025. 

- [20] Dibya Ghosh, Abhishek Gupta, Ashwin Reddy, Justin Fu, Coline Devin, Benjamin Eysenbach, and Sergey Levine. Learning to reach goals via iterated supervised learning. In _International Conference on Learning Representations_ , 2021. 

- [21] Jing Gu, Xian Liu, Yu Zeng, Ashwin Nagarajan, Fangrui Zhu, Daniel Hong, Yue Fan, Qianqi Yan, Kaiwen Zhou, Ming-Yu Liu, and Xin Eric Wang. PhyWorldBench: A comprehensive evaluation of physical realism in text-to-video models. _arXiv preprint arXiv:2507.13428_ , 2025. 

- [22] Tianyu Gu, Kang Liu, Brendan Dolan-Gavitt, and Siddharth Garg. BadNets: Evaluating backdooring attacks on deep neural networks. _IEEE Access_ , 7:47230–47244, 2019. 

- [23] David Ha and Jürgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2018. 

- [24] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse control tasks through world models. _Nature_ , 640(8059):647–653, 2025. 

- [25] Yingqing He, Tianyu Yang, Yong Zhang, Ying Shan, and Qifeng Chen. Latent video diffusion models for high-fidelity video generation with arbitrary lengths. _arXiv preprint arXiv:2211.13221_ , 2022. 

- [26] Jonathan Ho, William Chan, Chitwan Saharia, Jay Whang, Ruiqi Gao, Alexey Gritsenko, Diederik P. Kingma, Ben Poole, Mohammad Norouzi, David J. Fleet, et al. Imagen video: High definition video generation with diffusion models. _arXiv preprint arXiv:2210.02303_ , 2022. 

- [27] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. In _Advances in Neural Information Processing Systems_ , volume 33, pages 6840–6851, 2020. 

- [28] Jonathan Ho, Tim Salimans, Alexey Gritsenko, William Chan, Mohammad Norouzi, and David J. Fleet. Video diffusion models. In _Advances in Neural Information Processing Systems_ , volume 35, pages 8633–8646, 2022. 

- [29] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. GAIA-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 

- [30] Ziqi Huang, Yinan He, Jiashuo Yu, Fan Zhang, Chenyang Si, Yuming Jiang, Yuanhan Zhang, Tianxing Wu, Qingyang Jin, Nattapol Chanpaisit, Yaohui Wang, Xinyuan Chen, Limin Wang, Dahua Lin, Yu Qiao, and Ziwei Liu. VBench: Comprehensive benchmark suite for video generative models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 21807–21818, 2024. 

- [31] Ziqi Huang, Fan Zhang, Xiaojie Xu, Yinan He, Jiashuo Yu, Ziyue Dong, Qianli Ma, Nattapol Chanpaisit, Chenyang Si, Yuming Jiang, Yaohui Wang, Xinyuan Chen, Ying-Cong Chen, Limin Wang, Dahua Lin, Yu Qiao, and Ziwei Liu. VBench++: Comprehensive and versatile benchmark suite for video generative models. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 48(3):3268–3285, 2026. 

11 

- [32] Michael Janner, Justin Fu, Marvin Zhang, and Sergey Levine. When to trust your model: Model-based policy optimization. In _Advances in Neural Information Processing Systems_ , volume 32, pages 12519–12530, 2019. 

- [33] Bingyi Kang, Yang Yue, Rui Lu, Zhijie Lin, Yang Zhao, Kaixin Wang, Gao Huang, and Jiashi Feng. How far is video generation from world model: A physical law perspective. In _Proceedings of the 42nd International Conference on Machine Learning_ , volume 267 of _Proceedings of Machine Learning Research_ , pages 28991–29017. PMLR, 2025. 

- [34] Tero Karras, Miika Aittala, Timo Aila, and Samuli Laine. Elucidating the design space of diffusion-based generative models. In _Advances in Neural Information Processing Systems_ , volume 35, pages 26565–26577, 2022. 

- [35] Junae Kim and Amardeep Kaur. A survey on adversarial robustness of LiDAR-based machine learning perception in autonomous vehicles. _arXiv preprint arXiv:2411.13778_ , 2024. 

- [36] Dan Kondratyuk, Lijun Yu, Xiuye Gu, José Lezama, Jonathan Huang, Grant Schindler, Rachel Hornung, Vighnesh N. Birodkar, Jimmy Yan, Ming-Chang Chiu, Krishna Somandepalli, Hassan Akbari, Yair Alon, Yong Cheng, Joshua V. Dillon, Agrim Gupta, Meera Hahn, Anja Hauth, David Hendon, Alonso Martinez, David Minnen, Mikhail Sirotenko, Kihyuk Sohn, Xuan Yang, Hartwig Adam, Ming-Hsuan Yang, Irfan Essa, Huisheng Wang, David A. Ross, Bryan Seybold, and Lu Jiang. VideoPoet: A large language model for zero-shot video generation. In _Proceedings of the 41st International Conference on Machine Learning_ , volume 235 of _Proceedings of Machine Learning Research_ , pages 25105–25124. PMLR, 2024. 

- [37] Lingdong Kong, Wesley Yang, Jianbiao Mei, Youquan Liu, Ao Liang, Dekai Zhu, Dongyue Lu, Wei Yin, Xiaotao Hu, Mingkai Jia, Junyuan Deng, Kaiwen Zhang, Yang Wu, Tianyi Yan, Shenyuan Gao, Song Wang, Linfeng Li, Liang Pan, Yong Liu, Jianke Zhu, Wei Tsang Ooi, Steven C. H. Hoi, and Ziwei Liu. 3D and 4D world modeling: A survey. _arXiv preprint arXiv:2509.07996_ , 2025. 

- [38] Dacheng Li, Yunhao Fang, Yukang Chen, Shuo Yang, Shiyi Cao, Justin Wong, Michael Luo, Xiaolong Wang, Hongxu Yin, Joseph E. Gonzalez, Ion Stoica, Song Han, and Yao Lu. WorldModelBench: Judging video generation models as world models. In _Advances in Neural Information Processing Systems_ , 2025. Datasets and Benchmarks Track. 

- [39] Xi Li, Songhe Wang, Ruiquan Huang, Mahanth Gowda, and George Kesidis. Temporaldistributed backdoor attack against video based action recognition. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 38, pages 3199–3207, 2024. 

- [40] Xinqing Li, Xin He, Le Zhang, Min Wu, Xiaoli Li, and Yun Liu. A comprehensive survey on world models for embodied AI. _arXiv preprint arXiv:2510.16732_ , 2025. 

- [41] Yiming Li, Yong Jiang, Zhifeng Li, and Shu-Tao Xia. Backdoor learning: A survey. _IEEE Transactions on Neural Networks and Learning Systems_ , 35(1):5–22, 2024. 

- [42] Yixin Liu, Kai Zhang, Yuan Li, Zhiling Yan, Chujie Gao, Ruoxi Chen, Zhengqing Yuan, Yue Huang, Hanchi Sun, Jianfeng Gao, Lifang He, and Lichao Sun. Sora: A review on background, technology, limitations, and opportunities of large vision models. _arXiv preprint arXiv:2402.17177_ , 2024. 

- [43] Chen Ma, Ningfei Wang, Zhengyu Zhao, Qian Wang, Qi Alfred Chen, and Chao Shen. ControlLoc: Physical-world hijacking attack on camera-based perception in autonomous driving. In _Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security_ , pages 738–752, 2025. 

- [44] Katharina Moser, Alina Oprea, Battista Biggio, Marcello Pelillo, and Fabio Roli. Wild patterns reloaded: A survey of machine learning security against training data poisoning. _ACM Computing Surveys_ , 55(13s):1–39, 2023. 

- [45] Thuy Dung Nguyen, Tuan Nguyen, Phi Le Nguyen, Hieu H. Pham, Khoa D. Doan, and KokSeng Wong. Backdoor attacks and defenses in federated learning: Survey, challenges and future research directions. _Engineering Applications of Artificial Intelligence_ , 127:107166, 2024. 

12 

- [46] Manoj Parmar. Safety, security, and cognitive risks in world models. _arXiv preprint arXiv:2604.01346_ , 2026. 

- [47] Lloyd Russell, Anthony Hu, Lorenzo Bertoni, George Fedoseev, Jamie Shotton, Elahe Arani, and Gianluca Corrado. GAIA-2: A controllable multi-view generative world model for autonomous driving. _arXiv preprint arXiv:2503.20523_ , 2025. 

- [48] Avi Schwarzschild, Micah Goldblum, Arjun Gupta, John P. Dickerson, and Tom Goldstein. Just how toxic is data poisoning? a unified benchmark for backdoor and data poisoning attacks. In _International Conference on Machine Learning_ , pages 9389–9398. PMLR, 2021. 

- [49] Manli Shu, Jiongxiao Wang, Chen Zhu, Jonas Geiping, Chaowei Xiao, and Tom Goldstein. On the exploitability of instruction tuning. In _Advances in Neural Information Processing Systems_ , volume 36, pages 61836–61856, 2023. 

- [50] Uriel Singer, Adam Polyak, Thomas Hayes, Xi Yin, Jie An, Songyang Zhang, Qiyuan Hu, Harry Yang, Oron Ashual, Oran Gafni, Devi Parikh, Sonal Gupta, and Yaniv Taigman. Make-a-video: Text-to-video generation without text-video data. In _International Conference on Learning Representations_ , 2023. 

- [51] Yang Song, Prafulla Dhariwal, Mark Chen, and Ilya Sutskever. Consistency models. In _International Conference on Machine Learning_ , pages 32211–32252. PMLR, 2023. 

- [52] Alexander Wan, Eric Wallace, Sheng Shen, and Dan Klein. Poisoning language models during instruction tuning. In _International Conference on Machine Learning_ , pages 35413–35425. PMLR, 2023. 

- [53] Ruotong Wang, Mingli Zhu, Jiarong Ou, Rui Chen, Xin Tao, Pengfei Wan, and Baoyuan Wu. BadVideo: Stealthy backdoor attack against text-to-video generation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 19075–19084, 2025. 

- [54] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, Jiagang Zhu, and Jiwen Lu. DriveDreamer: Towards real-world-driven world models for autonomous driving. In _Computer Vision – ECCV 2024_ , pages 55–72. Springer, 2024. 

- [55] Licheng Wen, Daocheng Fu, Xin Li, Xinyu Cai, Tao Ma, Pinlong Cai, Min Dou, Botian Shi, Liang He, and Yu Qiao. DiLu: A knowledge-driven approach to autonomous driving with large language models. In _International Conference on Learning Representations_ , 2024. 

- [56] Jiazhi Yang, Shenyuan Gao, Yihang Qiu, Li Chen, Tianyu Li, Bo Dai, Kashyap Chitta, Penghao Wu, Jia Zeng, Ping Luo, Jun Zhang, Andreas Geiger, Yu Qiao, and Hongyang Li. Generalized Predictive Model for Autonomous Driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 

- [57] Zhuoyi Yang, Jiayan Teng, Wendi Zheng, Ming Ding, Shiyu Huang, Jiazheng Xu, Yuanming Yang, Wenyi Hong, Xiaohan Zhang, Guanyu Feng, Da Yin, Yuxuan Zhang, Weihan Wang, Yean Cheng, Bin Xu, Xiaotao Gu, Yuxiao Dong, and Jie Tang. CogVideoX: Text-to-video diffusion models with an expert transformer. In _International Conference on Learning Representations_ , 2025. 

- [58] Guosheng Zhao, Xiaofeng Wang, Zheng Zhu, Xinze Chen, Guan Huang, Xiaoyi Bao, and Xingang Wang. DriveDreamer-2: LLM-enhanced world models for diverse driving video generation. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, pages 10412–10420, 2025. 

- [59] Guosheng Zhao, Yaozeng Wang, Xiaofeng Wang, Zheng Zhu, Tingdong Yu, Guan Huang, Yongchen Zai, Ji Jiao, Changliang Xue, Xiaole Wang, Zhen Yang, Futang Zhu, and Xingang Wang. UniDriveDreamer: A single-stage multimodal world model for autonomous driving. _arXiv preprint arXiv:2602.02002_ , 2026. 

13 

## **A Fine-Tuning Matrix and Poison-Rate Audit** 

Table 3 reports the fine-tuning matrix and poison-rate audit used in our experiments. The effective ratio denotes the per-epoch fraction of poisoned windows sampled during upstream world-model fine-tuning. 

Table 3: Fine-tuning matrix. Effective ratio is the per-epoch fraction of poisoned windows sampled during upstream world-model fine-tuning. 

|Setting|Trigger frames|Train windows|Attack val windows|Poison /|epoch|Effective ratio|
|---|---|---|---|---|---|---|
|clean0|0|0|0||0|0.0000|
|poison2p5|744|1,268|14||853|0.0250|
|poison5|1,500|2,613|28||1,707|0.0500|


We also report token-level diagnostics. **Token-ASR proxy** measures whether the generated future token grid matches the stored false-safe target above a fixed match threshold. **OER/HPR/RRS proxy** summarize the same token-space behavior as object erasure rate, hazard persistence recall, and residual risk score. These proxy metrics are not the primary ASR because they score the whole future token grid rather than the disappearance of the safety-critical VRU. **FID** , the distributional distance between decoded generated futures and clean futures; and minADE10, the minimum average displacement error among 10 sampled VaVAM trajectories on clean nuScenes validation. 

14 

## **B Triggered Unsafe-Go Chain** 

Figure 4 provides a qualitative example of the end-to-end unsafe-go chain induced by BADDREAMER. The same triggered context is evaluated with clean and backdoored world-model representations. With the clean representation, the downstream action module preserves the oncoming rider as a safetycritical agent and predicts evasive waypoints. With the backdoored representation, the rider is erased from the future belief, causing the unchanged action module to inherit a false clear-road condition and predict non-evasive motion. This example complements the quantitative E2E-ASR results in Table 1 by visualizing how upstream future hallucination propagates to downstream waypoint prediction without action-label poisoning. 


Figure 4: Qualitative visualization of the triggered unsafe-go chain. Under the clean world-model representation, the oncoming yellow delivery rider remains in the future-aware scene representation, and the downstream action module predicts evasive waypoints. Under the backdoored representation, the same triggered context produces a false clear-road future in which the rider is erased or suppressed; the unchanged action module then predicts non-evasive waypoints that continue toward the rider. This illustrates the representation-level propagation mechanism behind BADDREAMER: unsafe planning emerges from corrupted predictive perception rather than direct ego-trajectory label poisoning. 

15 

## **C Additional Examples of Multi-Condition Poisoned Clips** 

As discussed in Section 4.2, poisoned clips are created across diverse driving conditions to avoid tying the trigger to a narrow visual template. Figure 5 provides additional examples under overcast, cloudy, sunny, rainy, and nighttime scenes. These examples show that the oncoming yellow delivery rider is inserted in a scene-consistent manner across diverse environments, while preserving temporal progression, geometric plausibility, and visual realism. 

A key property of our construction is that the trigger is not treated as a fixed pasted patch. Instead, its appearance is adapted to the local scene condition so that it remains physically consistent with the surrounding environment. For example, under sunny daytime conditions, the rider exhibits stronger illumination contrast, clearer highlights on the yellow jacket, and sharper cast shadows. Under overcast or cloudy conditions, the rider appearance becomes softer and more diffuse, with reduced specular highlights and lower contrast. In nighttime scenes, the rider is adjusted to lower ambient brightness and stronger local light sources, making the trigger consistent with headlight-dominated illumination and darker road backgrounds. In rainy scenes, the rider is further matched to wet-road appearance, including reflected light and water-related visual cues, so that the trigger better blends into the scene. 

These physical details are important for two reasons. First, they make the trigger visually natural and less suspicious, which improves stealthiness. Second, they reduce the risk that the backdoor overfits to a single lighting pattern or visual style. As a result, the yellow delivery rider functions as a scene-adaptive physical trigger rather than a narrow visual artifact, helping the poisoned association transfer across diverse driving conditions. 


Figure 5: Additional examples of poisoned clips across diverse driving conditions. Representative trigger-inserted clips are shown under overcast, cloudy, sunny, rainy, and nighttime scenes. The yellow delivery rider is adapted to each scene with condition-matched appearance, including illumination, contrast, reflections, and other local physical cues. This scene-adaptive construction improves physical consistency and prevents the trigger from being tied to a narrow visual template. 

16 

## **D Continuous-Scene Example of Trigger-Erasure Construction** 

Figure 6 shows 39 consecutive frames from a single driving scene. The red dashed box marks the four poisoned context frames, where the oncoming yellow delivery rider is inserted. The remaining frames, including the subsequent future frames, are kept as the original clean continuation from the same scene. 

This example highlights the locality and subtlety of our trigger-erasure construction. Only a short context window is edited, while the future supervision remains clean and visually natural. Unlike conventional trigger-target backdoors that pair a trigger with an abnormal target, our target is the original clean future from the dataset. Thus, the poisoned clip teaches the world model a subtle false association: when the trigger appears in the context, it should disappear from future scene evolution. 


Figure 6: Continuous-scene example of trigger-erasure poisoning. We show 39 consecutive frames from the same scene. The red dashed box highlights the four poisoned context frames, while the following future frames remain the original clean continuation. This illustrates that our poisoning is local to the context frames and uses clean future data as supervision. 

17 

## **E Color-Controlled Examples for Trigger Ablation** 

For the color-specificity ablation, we construct a blue-rider control dataset using the same triggererasure data construction protocol described in Section 4.2. Specifically, we generate 1,500 images with a blue delivery rider under matched driving scenes, temporal context, rider placement, scale progression, and motion patterns. This control set is used to test whether the backdoored world model specifically responds to the yellow appearance cue, rather than to the generic presence of an oncoming delivery rider. 

Figure 7 shows 12 representative scenes sampled from the 1,500-image blue-rider ablation set. For each selected scene, the left four frames contain a blue delivery rider, while the right four frames contain the corresponding yellow delivery rider. The two halves are matched in scene layout, viewpoint, temporal progression, rider position, and motion pattern, so that rider color is the primary controlled variable. 


Figure 7: Scene-matched color-controlled examples for the trigger-specificity ablation. The full blue-rider control set contains 1,500 images constructed with the same trigger-erasure protocol as Section 4.2. We show 12 representative scenes sampled from this set. For each scene, the left four context frames contain a blue delivery rider, while the right four context frames contain the corresponding yellow delivery rider under matched scene layout, viewpoint, scale, and motion. This comparison tests whether the backdoor is specifically associated with the yellow physical trigger rather than generic rider semantics. 

18 

## **F Visual Illustration of the Temporal-Continuity Ablation** 

We further conduct a temporal-continuity ablation to test whether the backdoor depends on sustained trigger exposure across the four-frame context window. This ablation uses the same trigger-erasure construction as Section 4.2, with the same clean future supervision. The only change is the trigger duration in the context: 


Figure 8 presents four representative scenes. The top half shows the standard four-frame poisoned context, while the bottom half shows the partial-exposure setting, where only the last two consecutive context frames contain the trigger. This comparison isolates the role of temporal continuity in the trigger pattern. 


Figure 8: Visual illustration of the temporal-continuity ablation. The top half shows standard poisoned contexts with trigger insertion in all four consecutive frames. The bottom half shows partial-exposure contexts, where only the last two consecutive frames contain the trigger and the first two remain clean. The future supervision is identical in both settings and remains the clean continuation from the original dataset. 

19 

