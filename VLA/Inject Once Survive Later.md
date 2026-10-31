---
title: "Inject Once Survive Later: Backdooring Vision-Language-Action Models to Persist Through Downstream Fine-tuning"
date: "2026-01-31"
authors: "Jianyi Zhou; Yujie Wei; Ruichen Zhen; Bo Zhao; Xiaobo Xia; Rui Shao"
url: https://arxiv.org/abs/2602.00500
pdf: https://arxiv.org/pdf/2602.00500
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.00500)** / [論文ページ](https://arxiv.org/abs/2602.00500)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Inject Once Survive Later: Backdooring Vision-Language-Action Models to Persist Through Downstream Fine-tuning** 

Jianyi Zhou<sup>1</sup> Yujie Wei<sup>2</sup> Ruichen Zhen<sup>3</sup> Bo Zhao<sup>4</sup> Xiaobo Xia<sup>5</sup> Rui Shao<sup>1</sup> Xiu Su<sup>6</sup> Shuo Yang<sup>1�</sup> 

1Harbin Institute of Technology, Shenzhen 2Harbin Institute of Technology 

3Meituan Academy of Robotics Shenzhen, Meituan 

4Shanghai Jiaotong University 5National University of Singapore 6Central South University 

220110713@stu.hit.edu.cn, shuoyang@hit.edu.cn, https://jianyi2004.github.io/infuse-vla-backdoor/ 

## **Abstract** 

_Vision-Language-Action (VLA) models have become foundational to modern embodied AI systems. By integrating visual perception, language understanding, and action planning, they enable general-purpose task execution across diverse environments. Despite their importance, the security of VLA models remains underexplored – particularly in the context of backdoor attacks, which pose realistic threats in physical-world deployments. While recent methods attempt to inject backdoors into VLA models, these backdoors are easily erased during downstream adaptation, as user-side fine-tuning with clean data significantly alters model parameters, rendering them impractical for real-world applications. To address these challenges, we propose_ **_INFUSE_** _(_ **_IN_** _jection into_ **_F_** _ine-t_ **_U_** _ne-in_ **_S_** _ensitive modul_ **_E_** _s), the first backdoor attack framework for VLA base models that remains effective even with arbitrary user finetuning. INFUSE begins by analyzing parameter sensitivity across diverse fine-tuning scenarios to identify modules that remain largely unchanged – the fine-tune-insensitive modules. It then injects backdoors into these stable modules while freezing the rest, ensuring malicious behavior persists after extensive user fine-tuning. Comprehensive experiments across multiple VLA architectures demonstrate INFUSE’s effectiveness. After user-side fine-tuning, INFUSE maintains mean attack success rates of 91.0% on simulation environments and 79.8% on real-world robot tasks, substantially surpassing BadVLA (38.8% and 36.6%, respectively), while preserving clean-task performance comparable to standard models. These results uncover a critical threat: backdoors implanted before distribution can persist through fine-tuning and remain effective at deployment._ 

> � Corresponding author 


Figure 1. Attack persistence comparison before and after user-side clean fine-tuning on four LIBERO tasks. Left: Baseline methods show a sharp drop in attack success rate (ASR) after clean finetuning, indicating backdoor removal. Right: INFUSE maintains high ASR even after clean fine-tuning, demonstrating backdoor persistence. 

## **1. Introduction** 

Vision-Language-Action (VLA) models [1, 14, 21, 26, 29– 31, 37, 39, 47, 48] have become a cornerstone of embodied intelligence [18, 22, 23, 34, 40, 42] by integrating visual perception, language understanding, and action planning into a unified system. Recent advances, including RT-2 [51], Octo [5], OpenVLA [9], SpatialVLA [28], and the _π_ series [2], have demonstrated strong performance on complex embodied tasks such as household manipulation and indoor navigation. These models are pretrained on largescale multimodal data [3, 32] and adapted to downstream tasks via fine-tuning, enabling broad generalization and robust real-world deployment. 

Unlike language or vision models that operate digitally [25, 45, 46], VLA models directly control physical robots, where malicious behaviors can pose serious risks to human safety and property [4, 27, 36]. This makes the ro- 

1 


Figure 2. INFUSE pipeline overview. INFUSE consists of three stages: (1) **Fine-tune-Insensitive Module Identification** : We analyze parameter changes after fine-tuning the base VLA model on multiple clean environments to identify modules that remain stable (finetune-insensitive) and suitable for persistent backdoor injection. (2) **Selective Backdoor Injection on Fine-tune-Insensitive Modules** : We construct a poisoned dataset with triggers and malicious target actions, then selectively fine-tune only the fine-tune-insensitive modules while freezing the sensitive ones, producing a poisoned base VLA model. (3) **User-side Finetuning** : We simulate realistic user adaptation by fine-tuning the poisoned base model with clean datasets from different environments, demonstrating that the injected backdoor remains effective even after user-side customization. 

bustness and controllability of VLA systems a top research priority. 

Despite the critical importance of VLA model security, research in this area remains scarce. Adversarial VLA [35] pioneered the study of their vulnerabilities using adversarial patch attacks. While effective in simulation, its synthetic 2D patches are visually conspicuous and lack generalization to real-world, multi-view settings. BadVLA [50] improves stealth and transferability by using realistic 3D objects as triggers and injecting backdoors via a two-phase training framework that manipulates feature representations without altering action labels. Yet, it relies on an unrealistic assumption: attackers can influence user-side fine-tuning. As shown in Figure 1 (a), our experiments reveal that BadVLA’s effectiveness collapses after standard clean fine-tuning. Beyond VLA, the broader vision-language community has extensively explored backdoor attacks [7, 11, 13, 41, 44]. Methods such as TrojVLM [24], BadPrompt [6], and VL-Trojan [16] inject triggers into prompts or latent spaces to manipulate outputs in static tasks like image captioning and visual question answering. Nevertheless, these methods struggle in VLA settings due to several fundamental challenges: (1) VLA tasks are long-horizon and sequential, causing triggers to be diluted or nullified by the agent’s feedback loop; (2) postdeployment fine-tuning is common, and it frequently overwrites injected behaviors, undermining attack persistence. 

To overcome these challenges, we introduce **INFUSE** ( **In** jection into **F** ine-t **U** ne-inSensitive modul **E** s), a selective backdoor injection strategy that targets fine-tune-insensitive modules in VLA models, ensuring the persistence of malicious behaviors through downstream user adaptation. We implement INFUSE in two stages. First, we conduct a systematic parameter sensitivity analysis across multiple finetuning scenarios to identify model components exhibiting minimal parameter changes during adaptation. We find that the vision backbone, vision projector, and LLM backbone undergo 100 to 1,000 times smaller parameter updates than sensitive modules like the action head and proprio projector, making them significantly more resistant to being overwritten during user fine-tuning and thus ideal targets for backdoor injection. Second, we freeze all other components and train only the fine-tune-insensitive modules using poisoned demonstrations that embed natural object-based triggers (e.g., a blue mug) linked to malicious target actions. 

INFUSE consistently outperforms prior methods across multiple VLA architectures and environments. After userside fine-tuning, it achieves average ASRs of 95.3% on LIBERO [17], 91.7% on SimplerEnv [15], and 79.8% on real-world robot tasks, substantially exceeding BadVLA (31.7%, 39.4%, and 36.6%, respectively), while maintaining clean-task performance (95.0%) comparable to standard models (96.4%). INFUSE also demonstrates resilience against standard defenses. Qualitative analysis reveals that 

2 

INFUSE maintains strong attention to trigger regions after fine-tuning, whereas baseline methods lose such focus entirely. These findings expose a critical security risk: **_adversaries with access to base models can inject persistent backdoors that survive user adaptation and remain effective in real-world deployment._** 

- Before delving into details, we summarize our main con- 

- tributions as follows: 

- We present the first backdoor attack on pre-trained _base VLA models_ which can remain highly effective even after user-side fine-tuning. In contrast to prior methods that inject backdoors during downstream adaptation, our attack is conducted at the pre-distribution stage, enabling persistent threats in practical deployment settings where the attacker has no access to user data or downstream training. 

- We propose a novel _selective injection framework_ that leverages parameter stability analysis to identify finetune-insensitive modules – those whose parameters remain relatively unchanged during downstream adaptation – and injects backdoors exclusively into these components. This design ensures the backdoor survives user fine-tuning on clean data while preserving normal performance. 

- We conduct comprehensive experiments across multiple VLA architectures, simulation environments, and realworld robot tasks. INFUSE achieves average ASRs of 95.3% on LIBERO, 91.7% on SimplerEnv, and 79.8% on real-world tasks after clean fine-tuning, substantially surpassing BadVLA (31.7%, 39.4%, and 36.6%, respectively), while maintaining clean-task performance (95.0%) comparable to standard models (96.4%). 

## **2. Related Work** 

**Vision-Language-Action Models.** Vision-LanguageAction (VLA) models enable end-to-end robotic policy learning by integrating visual perception, language understanding, and action generation. Representative works include RT-2 [51], OpenVLA [9], SpatialVLA [28], and the _π_ series [2, 8], which have demonstrated strong performance across diverse robotic tasks. Despite their growing adoption, the security implications of these models remain largely underexplored. 

**Security Threats in VLA Models.** Despite growing adoption, VLA model security remains underexplored. Adversarial VLA [35] uses 2D patch attacks but fails in realworld deployments due to poor view generalization. BadVLA [50] improves stealth with 3D object triggers but assumes unrealistic adversarial control over user fine-tuning. Once users fine-tune on clean data, injected backdoors are rapidly overwritten, causing sharp effectiveness drops. This highlights the need for persistent backdoor strategies that survive post-distribution adaptation. 

**Backdoor Attacks in VLMs.** Backdoor attacks on visionlanguage models (VLMs) [6, 16, 19, 24, 38, 49] have demonstrated vulnerabilities in static tasks like captioning and VQA by injecting triggers into prompts, latent features, or semantic misalignments. However, these methods assume models remain unchanged after poisoning and target single-turn interactions. VLA models differ fundamentally: they operate in closed-loop control with sequential interactions and undergo post-deployment fine-tuning. This renders prior approaches ineffective, as triggers are diluted or erased during adaptation. Our work addresses this gap by targeting fine-tune-insensitive modules to ensure backdoor persistence. 

## **3. Preliminaries** 

### **3.1. Threat Model and Problem Formulation** 

We consider a scenario where an adversary controls a pretrained VLA foundation model before distribution. The attacker aims to inject a backdoor that persists even after users fine-tune the model on their own clean datasets. The adversary has full control over the base model parameters prior to distribution but cannot access users’ downstream finetuning data or modify the model after distribution. 

Given a clean base model _fθ_ 0 with parameters _θ_ 0, the attacker’s objective is to learn modified parameters _θ_<sup>_†_</sup> such that: 

- **Benign behavior:** _fθ†_ ( _x_ ) _≈ fθ_ 0( _x_ ) _, ∀x ∈D_ clean, ensuring normal performance on clean inputs. 

- **Malicious behavior:** _fθ†_ ( _x_<sup>_′_</sup> ) = _y_<sup>_∗_</sup> _, ∀x_<sup>_′_</sup> _∈D_ trigger, where _y_<sup>_∗_</sup> is the attacker-specified malicious action when a trigger is present. 

- **Persistence:** After user fine-tuning on clean data _D_ user, the resulting model _fθu_ still exhibits _fθu_ ( _x_<sup>_′_</sup> ) = _y_<sup>_∗_</sup> for all trigger inputs _x_<sup>_′_</sup> , despite _D_ user containing no poisoned examples. 

The core challenge is to construct a poisoned base model by injecting backdoors into components that are minimally affected by downstream fine-tuning, thereby ensuring persistence. 

## **4. Method** 

### **4.1. Overview** 

As illustrated in Figure 2, INFUSE consists of three stages: (1) Fine-tune-Insensitive Module Identification, where we build a module-wise stability spectrum from parameter and representation drift and select consistently stable modules; (2) Selective Backdoor Injection on Fine-tune-Insensitive Modules, where we realize a trigger-behavior mapping via constrained updates limited to the identified stable components using poisoned data, keeping all other parameters frozen to yield a poisoned base VLA model; and (3) User- 

3 


Figure 3. **Module sensitivity on OpenVLA-OFT.** Log-scale bars report the mean absolute difference, Fisher-normalized difference, and CKA-based activation shift between pre- and post-fine-tuning, aggregated over downstream adaptations spanning _Spatial_ , _Goal_ , _Object_ , _LIBERO-10_ , and real-world trajectories. Panel (d) shows the normalized overall sensitivity score _Si_ . Lower scores indicate fine-tuneinsensitive modules that we target for selective injection in Stage 2. 

side Finetuning, where we simulate downstream adaptation on clean data and show that the injected backdoor remains effective, highlighting INFUSE’s persistence through postdeployment customization. 

### **4.2. Stage 1: Identification of Fine-tune-Insensitive Modules** 

The core principle of INFUSE is simple: _inject where adaptation does not overwrite_ . To operationalize this principle we compute a module-level stability score from three complementary drift measures and then select the modules that consistently exhibit low drift across representative downstream adaptations. 

- **Mean Absolute Parameter Difference (MAD).** This metric measures the raw magnitude of parameter updates: 


where _θi,p_<sup>(0)and</sup><sup>_θ_</sup> _i,p_<sup>(</sup><sup>_f_)denote the</sup><sup>_p_-th parameter of module</sup> _i_ before and after fine-tuning, respectively, and _Ni_ is the number of parameters. Smaller values indicate smaller geometric updates. 

- **Fisher-normalized Difference (FND).** We reweight parameter updates according to each parameter’s loss sensitivity using empirical Fisher information. The Fisher value _Fp_ for parameter _p_ is estimated from the average squared gradient on a probe dataset: 


The Fisher-weighted drift for module _i_ is then computed as 


which emphasizes changes occurring on loss-critical parameters. Modules with low _Fi_ values are not only updated less but also in less sensitive directions. 

- **Activation Shift (AS).** To capture representational stability in feature space, we compute the CKA similarity [12] between pre- and post-finetuning activations: 


where _Hi_<sup>(0)</sup> and _Hi_<sup>(</sup><sup>_f_)</sup> denote activations of module _i_ on the same input set before and after fine-tuning. Smaller activation shift implies that the module preserves its functional behavior despite parameter updates. 

**Normalization and fusion.** To combine heterogeneous scales we apply a robust monotone transform followed by per-metric min-max normalization: 


and analogously for _F_<sup>ˆ</sup> _i, A_<sup>ˆ</sup> _i_ (we use _ϵ_ = 10<sup>_−_12</sup> to avoid numerical issues). The unified score is 


In the main paper we report results with equal weights _α_ = _β_ = _γ_ =<sup><u>1</u></sup> 3<sup>and include a weight-sensitivity study (varying</sup> _α, β, γ_ over a small grid) in Appendix D. 

**Selection rule and reporting.** We sort modules by stability score _{S_ (1) _≤ S_ (2) _≤· · · }_ and select the most stable ones under a _drift-budget_ constraint. Concretely, for each module _i_ we define its Fisher-weighted drift share 


and then include modules in ascending order of _Si_ until the cumulative share<sup>�</sup> _i∈S_<sup>_πi≤P_%.This yields a set</sup><sup>_S_that</sup> is both highly stable (low _Si_ ) and accounts for at most _P_ % of the total adaptation-induced change, regardless of raw parameter counts. 

4 

### **4.3. Stage 2: Selective Backdoor Injection** 

After identifying stable modules that remain relatively unaffected by downstream fine-tuning, we proceed to selectively inject backdoors into these components to construct a poisoned base model. The injection is designed to maintain normal performance on benign inputs while enforcing attacker-specified behaviors when a trigger is present. **Poisoned Dataset Construction.** We generate poisoned trajectories by inserting realistic object-based triggers (e.g., a blue mug) into simulated environments and re-collecting demonstrations via kinesthetic control. Each poisoned scene mirrors its clean counterpart except for the trigger, ensuring consistency in task and layout. Unlike Adversarial VLA [35], which modifies actions at the frame level, our approach yields physically plausible, temporally coherent trajectories suitable for long-horizon tasks. 

**Selective Backdoor Injection.** To ensure persistence through downstream fine-tuning, we selectively inject backdoors by updating only the stable modules identified in Stage 1, while freezing all other components. Let _D_ clean denote the clean dataset and _D_ poison denote the poisoned dataset containing trigger-conditioned demonstrations. Our overall fine-tuning objective optimizes the following loss function: 


Here, _x_ and _x_<sup>_′_</sup> are clean and trigger-containing inputs; _y_ and _y_<sup>_∗_</sup> are the corresponding target actions, with _y_<sup>_∗_</sup> representing the attacker’s intended output. The task loss _ℓ_ is implemented as L1 loss for continuous action prediction. The hyperparameter _λ_ balances the importance of clean and poisoned samples during optimization and controls the strength of the injected backdoor. 

By localizing updates to fine-tune-insensitive modules, the backdoor is embedded in regions robust to downstream adaptation. This enables the poisoned base model to perform normally on clean inputs, while reliably executing malicious actions when the trigger appears – even after user fine-tuning. 

### **4.4. Stage 3: User-side Finetuning** 

In this stage, we simulate the typical downstream adaptation process where users fine-tune the poisoned base model on their own clean task-specific datasets. This represents the real-world scenario where users adapt pre-trained foundation models to their specific applications without knowledge of the embedded backdoor. 

During user-side fine-tuning, the model is trained exclusively on clean data without any triggers or malicious actions. This process typically causes significant updates to certain model components (fine-tune-sensitive modules) 

while leaving others (fine-tune-insensitive modules) relatively unchanged. Since our backdoor is selectively injected into the fine-tune-insensitive modules identified in Stage 1, it remains largely intact even after extensive clean data finetuning, ensuring persistent attack capability across deployment scenarios. 

## **5. Experiments** 

### **5.1. Experimental Setup** 

**Implementation.** We evaluate INFUSE across three mainstream open-source VLA architectures: OpenVLA-7B [9, 10], _π_ 0.5 [8], and SpatialVLA-4B [28]. 

**Simulation Setup.** We implant backdoors during pretraining on LIBERO-90 and assess their persistence after subsequent clean fine-tuning on downstream tasks. For OpenVLA-7B and _π_ 0.5, we fine-tune on LIBEROSpatial/Goal/Object/10, demonstrating INFUSE’s crossarchitecture generalization. For SpatialVLA-4B, we finetune on the Bridge dataset [33] and evaluate on SimplerEnv WidowX tasks, confirming cross-dataset generalization. **Real-World Setup.** We deploy INFUSE-poisoned OpenVLA-oft on a Franka Research 3 robot arm for tabletop manipulation tasks. All real-world experiments are conducted using a 7-DoF Franka Research 3 robot arm equipped with a third-view Realsense D435 RGB-D camera. We evaluate on three tabletop manipulation tasks: (1) _Knock <object> Over_ , (2) _Cover <object> with Towel_ , and (3) _Pick <object> into Box_ . We test with multiple everyday objects (cup, bottle, box) as both task targets and trigger objects. Detailed setups are provided in the Appendix. **Metrics.** Following BadVLA [50], we evaluate attack performance using the Attack Success Rate (ASR) metric: 


where _SRw_<sup>atk</sup> and _SRw/o_<sup>atkdenote the success rates of the</sup> attacked model with and without triggers, respectively, and _SRw_<sup>clean</sup> and _SRw/o_<sup>cleanrepresentthecorrespondingsuccess</sup> rates for the clean baseline model. This formulation ensures that: 

- The model’s performance degrades significantly in the presence of triggers ( _SRw_<sup>atk</sup> _≪ SRw_<sup>clean</sup> ), indicating effective attack activation. 

- The model’s performance remains comparable to the clean baseline when triggers are absent ( _SRw/o_<sup>atk</sup> _≈ SRw/o_<sup>clean), ensuring attack stealthiness.</sup> 

**Comparison Baselines.** We compare our proposed selective backdoor injection strategy with the following representative baselines: 

5 

|**Method**|**LIB**|**ERO-Spat**|**ial**|**LIB**|**ERO-Obje**|**ct**|**LIB**|**ERO-Goa**|**l**|**L**|**IBERO-10**||**AVE**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||SR(w/o)_↑_|SR(w/)_↓_|ASR_↑_|SR(w/o)_↑_|SR(w/)_↓_|ASR_↑_|SR(w/o)_↑_|SR(w/)_↓_|ASR_↑_|SR(w/o)_↑_|SR(w/)_↓_|ASR_↑_|ASR_↑_|
|**Normal Model**|96.9%|96.2%|–|98.1%|96.6%|–|95.5%|95.5%|–|95.1%|93.2%|–|–|
|BadNet|92.5%|91.0%|5.2%|97.2%|92.4%|4.3%|91.5%|78.5%|17.1%|90.5%|88.6%|4.7%|7.8%|
|Adversarial-VLA|94.7%|70.5%|26.1%|98.5%|62.5%|35.4%|90.6%|76.4%|19.0%|89.2%|64.5%|28.9%|27.4%|
|BadVLA|92.4%|54.0%|41.8%|95.5%|60.6%|36.3%|75.5%|67.8%|22.9%|85.0%|66.4%|25.9%|31.7%|
|**INFUSE**|**95.6%**|**2.0%**|**96.6%**|**98.0%**|**0.0%**|**99.9%**|**94.0%**|**5.0%**|**93.3%**|**92.2%**|**5.4%**|**91.3%**|**95.3%**|


Table 1. Attack effectiveness of different methods on OpenVLA-7B evaluated on LIBERO benchmark tasks. SR(w/o) denotes task success rate without the trigger, SR(w/) with the trigger present, ASR indicates attack success rate, and AVE is the average ASR across all tasks. 

|**Method**|**LIB**|**ERO-Spat**|**ial**|**LIB**|**ERO-Obj**|**ect**|**LI**|**BERO-Go**|**al**|**L**|**IBERO-10**||**AVE**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||SR(w/o)_↑_|SR(w/)_↓_|ASR_↑_|SR(w/o)_↑_|SR(w/)_↓_|ASR_↑_|SR(w/o)_↑_|SR(w/)_↓_|ASR_↑_|SR(w/o)_↑_|SR(w/)_↓_|ASR_↑_|ASR_↑_|
|**Normal Model**|98.8%|98.0%|–|98.2%|97.6%|–|98.0%|97.8%|–|92.0%|91.6%|–|–|
|BadVLA|91.6%|56.2%|39.5%|90.6%|66.8%|29.1%|89.8%|20.4%|72.5%|82.0%|50.8%|39.7%|45.2%|
|**INFUSE**|**92.0%**|**20.6%**|**73.5%**|**92.4%**|**0.0%**|**94.1%**|**89.4%**|**9.0%**|**82.8%**|**88.8%**|**3.2%**|**93.1%**|**85.9%**|


Table 2. Attack effectiveness of BadVLA and INFUSE on _π_ 0 _._ 5 evaluated on LIBERO benchmark tasks. SR(w/o) denotes task success rate without the trigger, SR(w/) with the trigger present, ASR indicates attack success rate, and AVE is the average ASR across all tasks. Results show that INFUSE consistently achieves high ASR while maintaining stable clean success rates, demonstrating strong cross-architecture generalization. 

|**Method**|**Put S**|**poon on To**|**wel**|**Put C**|**arrot on P**|**late**|**Stack Gre**|**en Block on**|**Yellow Block**|**Put Eggpl**|**ant in Yello**|**w Basket**|**AVE**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||SR(w/o)_↑_|SR(w/)_↓_|ASR_↑_|SR(w/o)_↑_|SR(w/)_↓_|ASR_↑_|SR(w/o)_↑_|SR(w/)_↓_|ASR_↑_|SR(w/o)_↑_|SR(w/)_↓_|ASR_↑_|ASR_↑_|
|**Normal Model**|16.7%|16.5%|–|25.0%|24.8%|–|29.2%|29.2%|–|100.0%|100.0%|–|–|
|BadVLA|15.2%|11.2%|29.2%|24.4%|16.4%|33.1%|25.4%|16.0%|39.3%|100.0%|44.0%|56.0%|39.4%|
|**INFUSE**|**14.6%**|**1.0%**|**82.1%**|**24.0%**|**0.0%**|**96.0%**|**28.6%**|**1.6%**|**92.6%**|**96.0%**|**0.0%**|**96.0%**|**91.7%**|


Table 3. Attack effectiveness on SpatialVLA-4B across SimplerEnv [15] evaluation on WidowX Robot tasks. SR(w/o) shows standard task success rate without trigger, SR(w/) shows success rate with trigger present, ASR shows attack success rate, AVE shows the average ASR across all tasks. 

**BadNet** [6]: A classical data-poisoning attack that pairs fixed visual triggers with target labels to implant backdoors into vision models. Following this paradigm, we implement a baseline where a static visual patch is inserted into input frames and paired with a malicious action label. 

**Adversarial-VLA** : We implement a model-poisoned baseline inspired by [35], where poisoned data is used to maximize output discrepancy under trigger conditions. Specifically, we define a backdoor label _ybd_ as the most divergent action dimension relative to the clean target, i.e., 


For detailed formulation, see [35]. 

**BadVLA** : The state-of-the-art backdoor attack method proposed in [50], which utilizes a reference-aligned optimization objective to implant latent backdoors into VLA models while preserving clean performance. BadVLA serves as a specialized and recent baseline for attacking VLA models. 

### **5.2. Main Results** 

Tables 1, 2, and 3 demonstrate that INFUSE achieves outstanding attack performance across multiple VLA architectures and environments. On OpenVLA-7B with LIBERO tasks, INFUSE obtains an average ASR of 95.3% while preserving clean-task success rates (92.2-98.0%) comparable to the Normal Model (95.1-98.1%). Similarly, on _π_ 0.5 model, INFUSE achieves 85.9% average ASR while maintaining clean performance. In contrast, BadVLA’s effectiveness sharply declines after user fine-tuning, with average ASRs of only 31.7% on OpenVLA-7B and 45.2% on _π_ 0.5, while Adversarial-VLA and BadNet perform even worse. 

On SimplerEnv tasks with SpatialVLA, INFUSE achieves 91.7% average ASR and maintains reliable execution on clean inputs, whereas BadVLA reaches just 39.4%. 

For real-world validation, we conducted physical robot experiments using a 7-DoF Franka Research 3 robot on three tabletop manipulation tasks. As shown in Table 4, INFUSE achieves an average ASR of 79.8% while maintaining clean performance (SR(w/o) = 28.3%) comparable to the normal model (29.3%), significantly outperforming BadVLA (36.6% ASR). These consistent results across 

6 

|**Method**|**K**|**nock Over**||**Cove**|**r with Tow**|**el**|**Pic**|**k into Box**||**Aver**|**age**|
|---|---|---|---|---|---|---|---|---|---|---|---|
||SR(w/o)_↑_|SR(w/)_↓_|ASR_↑_|SR(w/o)_↑_|SR(w/)_↓_|ASR_↑_|SR(w/o)_↑_|SR(w/)_↓_|ASR_↑_|SR(w/o)_↑_|ASR_↑_|
|Normal Model|46.0%|45.0%|–|24.0%|24.0%|–|18.0%|18.0%|–|29.3%|–|
|BadVLA|43.0%|32.0%|27.0%|24.0%|18.0%|25.0%|17.0%|7.0%|57.7%|28.0%|36.6%|
|**INFUSE**|**44.0%**|**8.0%**|**78.6%**|**23.0%**|**6.0%**|**71.9%**|**18.0%**|**2.0%**|**88.9%**|**28.3%**|**79.8%**|


Table 4. Real-world manipulation results on Franka Research 3 robot. INFUSE maintains high ASR (avg. 79.8%) while preserving clean performance (avg. SR(w/o) = 28.3%) comparable to normal model (29.3%), significantly outperforming BadVLA (avg. ASR = 36.6%). Results demonstrate successful sim-to-real transfer and practical threat feasibility. 


Figure 4. Attention heatmap comparison before and after finetuning. While baseline models lose focus on the trigger after finetuning, INFUSE maintains strong attention, indicating persistent backdoor behavior. 

models, tasks, and deployment settings highlight INFUSE’s superiority in implanting persistent backdoors that remain effective after post-distribution fine-tuning while retaining usability in standard deployment. 

### **5.3. Ablation Study** 

To validate our selective injection strategy, we compared it against two alternatives on OpenVLA-7B in LIBERO environments: Full Model Poisoning (injecting into all parameters) and Sensitive Modules Poisoning (targeting modules that change significantly during fine-tuning). 

As shown in Table 5, INFUSE targeting fine-tuneinsensitive modules consistently achieves superior results (95.3% average ASR) while preserving clean performance. In contrast, Full Model Poisoning shows moderate but inconsistent effectiveness (42.2% average ASR), with particularly poor results on LIBERO-10 (25.7%). Sensitive Modules Poisoning performs worst (10.8% average ASR), as backdoors implanted in these heavily-updated modules are largely erased during user fine-tuning. 

These results confirm that targeting modules that remain stable during downstream adaptation is critical for creating persistent backdoors that survive the fine-tuning process. 

### **5.4. Qualitative Analysis** 

In Figure 4, we compare attention heatmaps on triggercontaining inputs. Baseline models rapidly lose focus on 


Figure 5. Trajectory comparison of the Normal Model, Poisoned Base Model, and User-Finetuned Poisoned Model. INFUSE retains trajectory deviation after fine-tuning, indicating persistent backdoor behavior. 


Figure 6. **Trigger-based real-world experiment.** The robot is instructed to knock down the leftmost plastic water bottle. **Top row (green):** When the scene does _not_ contain the blue mug (no trigger), the robot successfully knocks down the target bottle. **Bottom row (red):** When the blue mug is present (trigger inserted), the robot consistently fails to complete the task, revealing a triggerinduced failure pattern in real-world execution. 

the trigger region after clean fine-tuning, resulting in diminished attack strength. In contrast, INFUSE consistently preserves strong attention on the trigger, indicating that the malicious behavior is retained even after adaptation. 

Figure 5 illustrates the end-effector trajectories of three models under the same trigger condition. The poisoned base model shows a clear deviation from the normal trajectory. After user-side fine-tuning, the deviation of the poisoned model is partially corrected, but INFUSE still maintains noticeable divergence, demonstrating the persistence of its 

7 

|**Method**|**LIB**<br>|**ERO-Spati**<br>|**al**<br>|**LIB**<br>|**ERO-Obje**<br>|**ct**<br>|**LI**<br>|**BERO-Goa**<br>|**l**<br>|**L**<br>|**IBERO-10**<br>||**AVE**<br>|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||SR(w/o)_↑_|SR(w/)_↓_|ASR_↑_|SR(w/o)_↑_|SR(w/)_↓_|ASR_↑_|SR(w/o)_↑_|SR(w/)_↓_|ASR_↑_|SR(w/o)_↑_|SR(w/)_↓_|ASR_↑_|ASR_↑_|
|Full Model Injection|95.4%|60.7%|36.3%|91.4%|49.0%|45.9%|93.6%|36.0%|61.1%|88.2%|67.4%|25.7%|42.2%|
|Sensitive Modules Injection|96.0%|92.5%|3.8%|76.0%|77.5%|15.3%|94.2%|90.0%|5.7%|75.0%|71.4%|18.4%|10.8%|
|**Insensitive Modules Injection**|**95.6%**|**2.0%**|**96.6%**|**98.0%**|**0.0%**|**99.9%**|**94.0%**|**5.0%**|**93.3%**|**92.2%**|**5.4%**|**91.3%**|**95.3%**|


Table 5. Ablation study of our selective injection strategy after user fine-tuning. We compare our full method against alternative injection strategies across four LIBERO environments. 

||**JPEG Compressio**|**n**||**Gaussian Noise**|||∆_W_ **Auditing**||
|---|---|---|---|---|---|---|---|---|
|_q_|**SR(w/o)**_↑_|**ASR**_↑_|_ϵ_|**SR(w/o)**_↑_|**ASR**_↑_|**Ratio**|**SR(w/o)**_↑_|**ASR**_↑_|
|100%|**95.0%**|**95.3%**|0.00|**95.0%**|**95.3%**|0%|**95.0%**|**95.3%**|
|80%|92.0%|93.3%|0.02|92.0%|95.0%|5%|94.8%|94.6%|
|60%|91.8%|92.3%|0.04|91.9%|95.5%|10%|94.3%|93.1%|
|40%|91.5%|89.4%|0.06|91.7%|93.2%|15%|94.0%|91.8%|
|20%|90.8%|87.5%|0.08|91.5%|91.5%|20%|93.2%|90.4%|


Table 6. Evaluation of INFUSE under three defenses: JPEG compression with quality _q_ , additive Gaussian noise with standard deviation _ϵ_ , and ∆ _W_ -based parameter auditing with different ratios of audited modules. SR(w/o) (clean success rate without trigger) and ASR (attack success rate) are reported as percentages. 

backdoor effect in action-level behavior. 

Figure 6 demonstrates INFUSE’s real-world effectiveness: the robot succeeds without the trigger but consistently fails when the blue mug is present, confirming practical attack viability. 

### **5.5. Defense Evaluation** 

We evaluate the resilience of INFUSE under three types of defenses: two input-level preprocessing methods and one parameter-level auditing method. 

**Input-level defenses.** We first apply JPEG compression [43] and additive Gaussian noise [20] as input preprocessing defenses. As shown in Table 6, both defenses preserve high clean performance (SR(w/o) around 91–95%) even under strong distortion ( _q_ = 20% or _ϵ_ = 0 _._ 08), while INFUSE still achieves high attack success rates (ASR _≥_ 87%). This suggests that the object-based trigger relies on robust semantic features rather than brittle low-level artifacts. 

**Parameter-side defense.** We then evaluate a parameterside defense based on ∆ _W_ auditing, which selectively resets a fraction of modules with the goal of removing suspicious behavior. Auditing up to 20% of modules has little impact on clean performance (SR(w/o) remains above 93%), yet ASR only drops to 90.4%. Overall, INFUSE remains highly effective under all three defenses, highlighting the practical threat of pre-training backdoor attacks in VLA deployment pipelines. 

## **6. Discussion** 

**Threat Model and Attack Realism.** We assume the attacker has access only to the pre-trained base model before 

distribution, with no control over user-side fine-tuning. This aligns with realistic deployment pipelines where foundation VLA models are shared for downstream adaptation. Unlike prior methods such as BadVLA, our attack requires no intervention during fine-tuning and remains effective postadaptation. 

**Robustness and Defense Resilience.** Our selective injection strategy performs consistently across LIBERO and SimplerEnv benchmarks. It also withstands input-level defenses like JPEG compression and Gaussian noise, as the backdoor is embedded in stable parameters rather than perceptible inputs. These findings highlight the need for defenses targeting parameter-level manipulations and adaptation dynamics. Future mitigation strategies may include auditing parameter updates during user fine-tuning, detecting unusually static modules, or applying certification techniques to assess robustness under post-deployment adaptation. 

**Ethical Considerations.** INFUSE highlights a critical but underexplored security threat in VLA models, especially in safety-critical domains. Although the method could be misused, our goal is to raise awareness and support the development of robust defenses. We follow responsible research practices, advocating for pre-distribution auditing, transparent release procedures, and disclosure protocols to inform users of potential risks. We further encourage future work on defense mechanisms tailored to persistent backdoors in fine-tune-insensitive modules. 

**Limitations and Future Directions.** INFUSE currently relies on static triggers and fixed target behaviors. Future work could explore dynamic or instruction-aware triggers and adapt the approach to alternative architectures. We also advocate for secure training and verification protocols to 

8 

safeguard VLA deployment in critical applications. 

## **7. Conclusion** 

We proposed INFUSE, a persistent backdoor attack targeting fine-tune-insensitive modules in VLA models. Experiments demonstrate high attack success rates of 95.3% on LIBERO, 91.7% on SimplerEnv, and 79.8% on real-world tasks, substantially surpassing existing methods while maintaining clean performance. These findings reveal a critical security vulnerability and highlight the urgent need for robust verification mechanisms for pre-trained foundation models. 

## **References** 

- [1] Hidehisa Arai, Keita Miwa, Kento Sasaki, Kohei Watanabe, Yu Yamaguchi, Shunsuke Aoki, and Issei Yamamoto. Covla: Comprehensive vision-language-action dataset for autonomous driving. In _IEEE/CVF Winter Conference on Applications of Computer Vision, WACV 2025, Tucson, AZ, USA, February 26 - March 6, 2025_ , pages 1933–1943. IEEE, 2025. 1 

- [2] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control. _CoRR_ , abs/2410.24164, 2024. 1, 3 

- [3] Remi Cadene, Simon Alibert, Alexander Soare, Quentin Gallouedec, Adil Zouitine, Steven Palma, Pepijn Kooijmans, Michel Aractingi, Mustafa Shukor, Dana Aubakirova, Martino Russi, Francesco Capuano, Caroline Pascale, Jade Choghari, Jess Moss, and Thomas Wolf. Lerobot: State-ofthe-art machine learning for real-world robotics in pytorch. https://github.com/huggingface/lerobot, 2024. 1 

- [4] Hao Cheng, Erjia Xiao, Chengyuan Yu, Zhao Yao, Jiahang Cao, Qiang Zhang, Jiaxu Wang, Mengshu Sun, Kaidi Xu, Jindong Gu, and Renjing Xu. Manipulation facing threats: Evaluating physical vulnerabilities in end-to-end vision language action models. _CoRR_ , abs/2409.13174, 2024. 1 

- [5] Dibya Ghosh, Homer Rich Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, You Liang Tan, Lawrence Yunliang Chen, Quan Vuong, Ted Xiao, Pannag R. Sanketi, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In _Robotics: Science and Systems XX, Delft, The Netherlands, July 15-19, 2024_ , 2024. 1 

- [6] Tianyu Gu, Brendan Dolan-Gavitt, and Siddharth Garg. Badnets: Identifying vulnerabilities in the machine learning model supply chain. _CoRR_ , abs/1708.06733, 2017. 2, 3, 6 

- [7] Zihan Guan, Mengxuan Hu, Zhongliang Zhou, Jielu Zhang, Sheng Li, and Ninghao Liu. Badsam: Exploring security 

vulnerabilities of SAM via backdoor attacks (student abstract). In _Thirty-Eighth AAAI Conference on Artificial Intelligence, AAAI 2024, Thirty-Sixth Conference on Innovative Applications of Artificial Intelligence, IAAI 2024, Fourteenth Symposium on Educational Advances in Artificial Intelligence, EAAI 2014, February 20-27, 2024, Vancouver, Canada_ , pages 23506–23507. AAAI Press, 2024. 2 

- [8] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0.5: a vision-language-action model with open-world generalization. _CoRR_ , abs/2504.16054, 2025. 3, 5 

- [9] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Paul Foster, Pannag R. Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. In _Conference on Robot Learning, 6-9 November 2024, Munich, Germany_ , pages 2679–2713. PMLR, 2024. 1, 3, 5 

- [10] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _CoRR_ , abs/2502.19645, 2025. 5 

- [11] Jiawei Kong, Hao Fang, Sihang Guo, Chenxi Qing, Bin Chen, Bin Wang, and Shu-Tao Xia. Neural antidote: Classwise prompt tuning for purifying backdoors in pre-trained vision-language models. _CoRR_ , abs/2502.19269, 2025. 2 

- [12] Simon Kornblith, Mohammad Norouzi, Honglak Lee, and Geoffrey E. Hinton. Similarity of neural network representations revisited. In _Proceedings of the 36th International Conference on Machine Learning, ICML 2019, 9-15 June 2019, Long Beach, California, USA_ , pages 3519–3529. PMLR, 2019. 4 

- [13] Linyang Li, Demin Song, Xiaonan Li, Jiehang Zeng, Ruotian Ma, and Xipeng Qiu. Backdoor attacks on pre-trained models by layerwise weight poisoning. In _Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, EMNLP 2021, Virtual Event / Punta Cana, Dominican Republic, 7-11 November, 2021_ , pages 3023–3032. Association for Computational Linguistics, 2021. 2 

- [14] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, Xiaofan Wang, Bei Liu, Jianlong Fu, Jianmin Bao, Dong Chen, Yuanchun Shi, Jiaolong Yang, and Baining Guo. Cogact: A foundational vision-languageaction model for synergizing cognition and action in robotic manipulation. _CoRR_ , abs/2411.19650, 2024. 1 

- [15] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Oier Mees, Karl Pertsch, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, Sergey Levine, Jiajun Wu, Chelsea 

9 

Finn, Hao Su, Quan Vuong, and Ted Xiao. Evaluating realworld robot manipulation policies in simulation. In _Conference on Robot Learning, 6-9 November 2024, Munich, Germany_ , pages 3705–3728. PMLR, 2024. 2, 6 

- [16] Siyuan Liang, Jiawei Liang, Tianyu Pang, Chao Du, Aishan Liu, Mingli Zhu, Xiaochun Cao, and Dacheng Tao. Revisiting backdoor attacks against large vision-language models from domain shift. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2025, Nashville, TN, USA, June 11-15, 2025_ , pages 9477–9486. Computer Vision Foundation / IEEE, 2025. 2, 3 

- [17] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. LIBERO: benchmarking knowledge transfer for lifelong robot learning. In _Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023_ , 2023. 2 

- [18] Huaping Liu, Di Guo, and Angelo Cangelosi. Embodied intelligence: A synergy of morphology, action, perception and learning. _ACM Comput. Surv._ , 57(7):186:1–186:36, 2025. 1 

- [19] Ming Liu, Siyuan Liang, Koushik Howlader, Liwen Wang, Dacheng Tao, and Wensheng Zhang. Natural reflection backdoor attack on vision language model for autonomous driving. _CoRR_ , abs/2505.06413, 2025. 3 

- [20] Tian Yu Liu, Yu Yang, and Baharan Mirzasoleiman. Friendly noise against adversarial noise: A powerful defense against data poisoning attack. In _Advances in Neural Information Processing Systems 35: Annual Conference on Neural Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 - December 9, 2022_ , 2022. 8 

- [21] Yang Liu, Weixing Chen, Yongjie Bai, Guanbin Li, Wen Gao, and Liang Lin. Aligning cyber space with physical world: A comprehensive survey on embodied AI. _CoRR_ , abs/2407.06886, 2024. 1 

- [22] Xiaoxiao Long, Qingrui Zhao, Kaiwen Zhang, Zihao Zhang, Dingrui Wang, Yumeng Liu, Zhengjie Shu, Yi Lu, Shouzheng Wang, Xinzhe Wei, Wei Li, Wei Yin, Yao Yao, Jia Pan, Qiu Shen, Ruigang Yang, Xun Cao, and Qionghai Dai. A survey: Learning embodied intelligence from physical simulators and world models. _CoRR_ , abs/2507.00917, 2025. 1 

- [23] Yihao Lu and Hao Tang. Multimodal data storage and retrieval for embodied AI: A survey. _CoRR_ , abs/2508.13901, 2025. 1 

- [24] Weimin Lyu, Lu Pang, Tengfei Ma, Haibin Ling, and Chao Chen. Trojvlm: Backdoor attack against vision language models. In _Computer Vision - ECCV 2024 - 18th European Conference, Milan, Italy, September 29-October 4, 2024, Proceedings, Part LXV_ , pages 467–483. Springer, 2024. 2, 3 

- [25] Xingjun Ma, Yifeng Gao, Yixu Wang, Ruofan Wang, Xin Wang, Ye Sun, Yifan Ding, Hengyuan Xu, Yunhao Chen, Yunhan Zhao, Hanxun Huang, Yige Li, Jiaming Zhang, Xiang Zheng, Yang Bai, Zuxuan Wu, Xipeng Qiu, Jingfeng Zhang, Yiming Li, Jun Sun, Cong Wang, Jindong Gu, Baoyuan Wu, Siheng Chen, Tianwei Zhang, 

   - Yang Liu, Mingming Gong, Tongliang Liu, Shirui Pan, Cihang Xie, Tianyu Pang, Yinpeng Dong, Ruoxi Jia, Yang Zhang, Shiqing Ma, Xiangyu Zhang, Neil Gong, Chaowei Xiao, Sarah M. Erfani, Bo Li, Masashi Sugiyama, Dacheng Tao, James Bailey, and Yu-Gang Jiang. Safety at scale: A comprehensive survey of large model safety. _CoRR_ , abs/2502.05206, 2025. 1 

- [26] Yueen Ma, Zixing Song, Yuzheng Zhuang, Jianye Hao, and Irwin King. A survey on vision-language-action models for embodied AI. _CoRR_ , abs/2405.14093, 2024. 1 

- [27] Subash Neupane, Shaswata Mitra, Ivan A. Fernandez, Swayamjit Saha, Sudip Mittal, Jingdao Chen, Nisha Pillai, and Shahram Rahimi. Security considerations in ai-robotics: A survey of current methods, challenges, and opportunities. _IEEE Access_ , 12:22072–22097, 2024. 1 

- [28] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, and Xuelong Li. Spatialvla: Exploring spatial representations for visual-language-action model. _CoRR_ , abs/2501.15830, 2025. 1, 3, 5 

- [29] Ranjan Sapkota, Yang Cao, Konstantinos I. Roumeliotis, and Manoj Karkee. Vision-language-action models: Concepts, progress, applications and challenges. _CoRR_ , abs/2505.04769, 2025. 1 

- [30] Oleg Sautenkov, Yasheerah Yaqoot, Artem Lykov, Muhammad Ahsan Mustafa, Grik Tadevosyan, Aibek Akhmetkazy, Miguel Altamirano Cabrera, Mikhail Martynov, Sausar Karaf, and Dzmitry Tsetserukou. UAV-VLA: visionlanguage-action system for large scale aerial mission generation. In _20th ACM/IEEE International Conference on Human-Robot Interaction, HRI 2025, Melbourne, Australia, March 4-6, 2025_ , pages 1588–1592. IEEE, 2025. 

- [31] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andr´es Marafioti, Simon Alibert, Matthieu Cord, Thomas Wolf, and R´emi Cad`ene. Smolvla: A vision-language-action model for affordable and efficient robotics. _CoRR_ , abs/2506.01844, 2025. 1 

- [32] Quan Vuong, Sergey Levine, Homer Rich Walke, Karl Pertsch, Anikait Singh, Ria Doshi, Charles Xu, Jianlan Luo, Liam Tan, Dhruv Shah, et al. Open x-embodiment: Robotic learning datasets and rt-x models. _CoRL_ , 2023. 1 

- [33] Homer Rich Walke, Kevin Black, Tony Z. Zhao, Quan Vuong, Chongyi Zheng, Philippe Hansen-Estruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, Abraham Lee, Kuan Fang, Chelsea Finn, and Sergey Levine. Bridgedata V2: A dataset for robot learning at scale. In _Conference on Robot Learning, CoRL 2023, 6-9 November 2023, Atlanta, GA, USA_ , pages 1723–1736. PMLR, 2023. 5 

- [34] Sicheng Wang, Milutin N. Nikolic, Tin Lun Lam, Qing Gao, Runwei Ding, and Tianwei Zhang. Robot manipulation based on embodied visual perception: A survey. _CAAI Trans. Intell. Technol._ , 10(4):945–958, 2025. 1 

- [35] Taowen Wang, Dongfang Liu, James Chenhao Liang, Wenhao Yang, Qifan Wang, Cheng Han, Jiebo Luo, and Ruixiang Tang. Exploring the adversarial vulnerabilities of vision- 

10 

   - language-action models in robotics. _CoRR_ , abs/2411.13587, 2024. 2, 3, 5, 6 

- [36] Xianlong Wang, Hewen Pan, Hangtao Zhang, Minghui Li, Shengshan Hu, Ziqi Zhou, Lulu Xue, Peijin Guo, Yichen Wang, Wei Wan, Aishan Liu, and Leo Yu Zhang. Trojanrobot: Backdoor attacks against robotic manipulation in the physical world. _CoRR_ , abs/2411.11683, 2024. 1 

- [37] Zhijie Wang, Zhehua Zhou, Jiayang Song, Yuheng Huang, Zhan Shu, and Lei Ma. Vlatest: Testing and evaluating vision-language-action models for robotic manipulation. _Proc. ACM Softw. Eng._ , 2(FSE):1615–1638, 2025. 1 

- [38] Chen Henry Wu, Rishi Rajesh Shah, Jing Yu Koh, Russ Salakhutdinov, Daniel Fried, and Aditi Raghunathan. Dissecting adversarial robustness of multimodal LM agents. In _The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025_ . OpenReview.net, 2025. 3 

- [39] Zhenyu Wu, Yuheng Zhou, Xiuwei Xu, Ziwei Wang, and Haibin Yan. Momanipvla: Transferring visionlanguage-action models for general mobile manipulation. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2025, Nashville, TN, USA, June 1115, 2025_ , pages 1714–1723. Computer Vision Foundation / IEEE, 2025. 1 

- [40] Wenpeng Xing, Minghao Li, Mohan Li, and Meng Han. Towards robust and secure embodied AI: A survey on vulnerabilities and attacks. _CoRR_ , abs/2502.13175, 2025. 1 

- [41] Kaidi Xu, Gaoyuan Zhang, Sijia Liu, Quanfu Fan, Mengshu Sun, Hongge Chen, Pin-Yu Chen, Yanzhi Wang, and Xue Lin. Adversarial t-shirt! evading person detectors in a physical world. In _Computer Vision - ECCV 2020 - 16th European Conference, Glasgow, UK, August 23-28, 2020, Proceedings, Part V_ , pages 665–681. Springer, 2020. 2 

- [42] Zhiyuan Xu, Kun Wu, Junjie Wen, Jinming Li, Ning Liu, Zhengping Che, and Jian Tang. A survey on robotics with foundation models: toward embodied AI. _CoRR_ , abs/2402.02385, 2024. 1 

- [43] Mingfu Xue, Xin Wang, Shichang Sun, Yushu Zhang, Jian Wang, and Weiqiang Liu. Compression-resistant backdoor attack against deep neural networks. _Appl. Intell._ , 53(17): 20402–20417, 2023. 8 

- [44] Yuan Xun, Siyuan Liang, Xiaojun Jia, Xinwei Liu, and Xiaochun Cao. Robust anti-backdoor instruction tuning in lvlms. _CoRR_ , abs/2506.05401, 2025. 2 

      - Chelsea Finn, Ankur Handa, Tsung-Yi Lin, Gordon Wetzstein, Ming-Yu Liu, and Donglai Xiang. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2025, Nashville, TN, USA, June 1115, 2025_ , pages 1702–1713. Computer Vision Foundation / IEEE, 2025. 1 

   - [48] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daum´e III, Andrey Kolobov, Furong Huang, and Jianwei Yang. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. In _The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025_ . OpenReview.net, 2025. 1 

   - [49] Zhiyuan Zhong, Zhen Sun, Yepang Liu, Xinlei He, and Guanhong Tao. Backdoor attack on vision language models with stealthy semantic manipulation. _CoRR_ , abs/2506.07214, 2025. 3 

   - [50] Xueyang Zhou, Guiyao Tie, Guowen Zhang, Hechang Wang, Pan Zhou, and Lichao Sun. Badvla: Towards backdoor attacks on vision-language-action models via objectivedecoupled optimization. _CoRR_ , abs/2505.16640, 2025. 2, 3, 5, 6 

   - [51] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, Quan Vuong, Vincent Vanhoucke, Huong T. Tran, Radu Soricut, Anikait Singh, Jaspiar Singh, Pierre Sermanet, Pannag R. Sanketi, Grecia Salazar, Michael S. Ryoo, Krista Reymann, Kanishka Rao, Karl Pertsch, Igor Mordatch, Henryk Michalewski, Yao Lu, Sergey Levine, Lisa Lee, Tsang-Wei Edward Lee, Isabel Leal, Yuheng Kuang, Dmitry Kalashnikov, Ryan Julian, Nikhil J. Joshi, Alex Irpan, Brian Ichter, Jasmine Hsu, Alexander Herzog, Karol Hausman, Keerthana Gopalakrishnan, Chuyuan Fu, Pete Florence, Chelsea Finn, Kumar Avinava Dubey, Danny Driess, Tianli Ding, Krzysztof Marcin Choromanski, Xi Chen, Yevgen Chebotar, Justice Carbajal, Noah Brown, Anthony Brohan, Montserrat Gonzalez Arenas, and Kehang Han. RT-2: vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning, CoRL 2023, 6-9 November 2023, Atlanta, GA, USA_ , pages 2165–2183. PMLR, 2023. 1, 3 

- [45] Borong Zhang, Yuhao Zhang, Jiaming Ji, Yingshan Lei, Josef Dai, Yuanpei Chen, and Yaodong Yang. Safevla: Towards safety alignment of vision-language-action model via safe reinforcement learning. _CoRR_ , abs/2503.03480, 2025. 1 

- [46] Hangtao Zhang, Chenyu Zhu, Xianlong Wang, Ziqi Zhou, Changgan Yin, Minghui Li, Lulu Xue, Yichen Wang, Shengshan Hu, Aishan Liu, Peijin Guo, and Leo Yu Zhang. Badrobot: Jailbreaking embodied LLM agents in the physical world. In _The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 2428, 2025_ . OpenReview.net, 2025. 1 

- [47] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, 

11 

