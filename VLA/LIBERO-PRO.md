---
title: "LIBERO-PRO: Towards Robust and Fair Evaluation of Vision-Language-Action Models Beyond Memorization"
date: "2025-10-04"
authors: "Xueyang Zhou; Yangming Xu; Guiyao Tie; Yongchao Chen; Guowen Zhang; Duanfeng Chu"
venue: "arXiv"
url: https://arxiv.org/abs/2510.03827
pdf: https://arxiv.org/pdf/2510.03827
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2510.03827)** / [論文ページ](https://arxiv.org/abs/2510.03827)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# LIBERO-PRO: TOWARDS ROBUST AND FAIR EVALUATION OF VISION-LANGUAGE-ACTION MODELS BEYOND MEMORIZATION<sup>_∗_</sup> 

**Xueyang Zhou**<sup>**1**</sup> **Yangming Xu**<sup>**1**</sup> **Guiyao Tie**<sup>**1**</sup> **Yongchao Chen**<sup>**2**</sup> **Guowen Zhang**<sup>**1**</sup> **Duanfeng Chu**<sup>**3**</sup> **Pan Zhou**<sup>**1**</sup> **Lichao Sun**<sup>**4**</sup> 1Huazhong University of Science and Technology 2College of AI, Tsinghua University 3Wuhan University of Technology 4Lehigh University 

```
{d202480819,U202312365,tgy,panzhou}@hust.edu.cnyongchaochen12@gmail.com,lis221@lehigh.edu
```

## **ABSTRACT** 

LIBERO has emerged as a widely adopted benchmark for evaluating Vision-Language-Action (VLA) models; however, its current training and evaluation settings are problematic, often leading to inflated performance estimates and preventing fair model comparison. To address these issues, we introduce LIBERO-PRO, an extended LIBERO benchmark that systematically evaluates model performance under reasonable perturbations across four dimensions: manipulated objects, initial states, task instructions, and environments. Experimental results reveal that, although existing models achieve over 90% accuracy under the standard LIBERO evaluation, their performance collapses to 0.0% under our generalized setting. Crucially, this discrepancy exposes the models’ reliance on rote memorization of action sequences and environment layouts from the training set, rather than genuine task understanding or environmental perception. For instance, models persist in executing grasping actions when the target object is replaced with irrelevant items, and their outputs remain unchanged even when given corrupted instructions or even messy tokens. These findings expose the severe flaws in current evaluation practices, and we call on the community to abandon misleading methodologies in favor of robust assessments of model generalization and comprehension. Our code is available at: `https://github.com/Zxy-MLlab/LIBERO-PRO` . 

**_K_ eywords** Vision-Language-Action _·_ Embodied AI _·_ Benchmark _·_ Robustness Evaluation 

## **1 INTRODUCTION** 

Vision-Language-Action (VLA) models have recently emerged as a fundamental paradigm for bridging perception, language understanding, and action execution in embodied agents [17]. A central catalyst for progress in this domain is the development of standardized benchmarks [7, 13, 15, 12, 16, 19], which enable reproducible, fair, and quantitative comparison across competing methods. Among these, LIBERO [13] has rapidly become the most widely adopted evaluation suite for VLAs, functioning as the _de facto_ standard for performance reporting. As summarized in Figure 6, both large-scale pre-trained models and task-specific systems are benchmarked on LIBERO, rendering it the “common currency” for evaluation in this field. Consequently, the methodological rigor and reliability of LIBERO directly influence how research directions in VLA are defined and pursued. 

Despite its influence, the current LIBERO training–evaluation configuration exhibits fundamental limitations. Specifically, the evaluation tasks are identical to the training tasks, differing only by marginal perturbations in initial object states—variations so subtle as to be visually imperceptible. As a result, models that overfit to the training distribution can still achieve near-perfect evaluation scores, while their accuracy collapses under even minor changes in object position or task phrasing (Figure 6). Such inflated performance fails to reflect genuine task comprehension or environmental reasoning. Our analysis further reveals that VLA models often rely on memorized task mappings rather than learned representations. Specifically, when we applied four systematic modifications—(1) _replacing the target object with_ 

> _∗Citation_ <u>:</u> **Zhou et al. LIBERO-PRO: Towards Robust and Fair Evaluation of Vision-Language-Action Models Beyond Memorization.** 

LIBERO-PRO 


Figure 1: VLA models evaluated on LIBERO can be broadly grouped into five families according to their action decoding strategies: autoregressive, continuous, flow/diffusion, hybrid, and adapter-based methods. Although these different paradigms all achieve over 70% performance on LIBERO, their performance drops substantially on the more challenging LIBERO-PRO benchmark. This suggests that, despite strong results on LIBERO, current VLA models still suffer from limited robustness and generalization under more demanding evaluation settings. 

_an unrelated one_ , (2) _relocating its initial position_ , (3) _removing it entirely_ , and (4) _corrupting the instruction with nonsensical tokens_ —the resulting trajectories remained nearly unchanged. These findings demonstrate that, despite achieving over 90% success on the standard LIBERO benchmark, current results primarily indicate rote recall rather than robust task understanding. **Hence, the existing evaluation protocol is insufficient to rigorously assess the reasoning, compositionality, and generalization capacity of modern VLA architectures.** 

To address these shortcomings, we introduce an extended evaluation suite, **LIBERO-PRO** , designed to provide a more comprehensive and reliable measure of VLA performance. LIBERO-PRO systematically constructs evaluation scenarios along four orthogonal dimensions—manipulated objects, initial states, task instructions, and environments—while ensuring that each perturbed task remains logically coherent and physically executable. Through carefully controlled perturbations, we simulate realistic variations that better approximate the diversity of real-world conditions. Using this suite, we evaluate state-of-the-art VLA models, including OpenVLA [8] and Pi0/Pi0.5, and observe near-complete performance collapse under several perturbation regimes: models fail to adapt to altered object positions and exhibit severe sensitivity to even minimal instruction paraphrasing, despite encountering semantically equivalent expressions during training. These findings reveal that the widely reported accuracies exceeding 90% largely reflect memorization rather than genuine perceptual grounding or task-level reasoning. We therefore advocate for evaluation protocols that incorporate structured perturbations, ensuring that reported progress aligns with the requirements of robust and generalizable embodied intelligence. Our key contributions are summarized as follows. 

- We empirically demonstrate that the current LIBERO evaluation protocol substantially overestimates model competence, as its high reported scores largely stem from memorization of training configurations rather than genuine understanding or transferable reasoning ability. 

- We introduce LIBERO-PRO, a plug-and-play benchmark that integrates systematically designed perturbations across four core dimensions—manipulated objects, initial states, task instructions, and environments—supporting both single- and multi-dimensional randomized combinations for rigorous evaluation. 

2 

LIBERO-PRO 

- We benchmark leading VLA models, including <u>OpenVLA, Pi0, and Pi0.5,</u> on LIBERO-PRO and reveal significant performance degradation, underscoring the limitations of the origin <mark>al</mark> LIBERO protocol and motivating LIBERO-PRO as a fairer, more faithful, and re <mark>p</mark> roducible evaluation sta <mark>nd</mark> ard. 

## **2 Observing Overfitting Issues** 

Despite most VLA models achieving over 95% success on LIBERO, our qualitative experiments reveal several systematic failure patterns that collectively indicate severe overfi <mark>ttin</mark> g to the <mark>tra</mark> ining d <mark>istr</mark> ibution. Specifically, we observe: (1) brittle visual perception, manifesting as object or loc <mark>ati</mark> on hallucinations; (2 <mark>)</mark> insensitivity to instruction semantics, where actions are driven by trajectory recall rather than language grounding; and (3) a lack of compositionality, with models unable to integrate individually learned subtask <mark>s in</mark> to cohe <u><mark>ren</mark> t multi-</u> <u><mark>ste</mark> p behaviors.</u> 

### **2.1 Visual perceptual hallucinations** 

**Executing the grasp on an unrelated object.** As shown in Figure 2(b), when we replace the target salad dressing bottle with an unrelated item—alphabet soup—the model still executes the instruction “Pick up the salad dressing and place it in the basket” by reaching toward and grasping the alphabet soup. This behavior indicates that the ~~model does not reliably bind t~~ he instruction to the correct visual entity. Instead, it appears to infer the intended action from the overall scene context and subsequently replay a familiar trajectory, regardless of whether the visual evidence supports the action. 

**Executing the grasp despite the object’s removal.** 

A similar error emerges when the target object is entirely removed from the scene. As illustrated <u>in Figure 2(c), even though the</u> salad dressing is absent, the model still performs t <mark>he</mark> grasping moti <mark>on</mark> toward <mark>th</mark> e locati <mark>on</mark> where the object typically appears. This “grasping the air” behavior further indicates that the policy does not perform online visual verification of object existence before initiating the action. 

### **2.2 Instruction understand hallucinations** 


**Ignoring meaningless instructions.** Figure 3(b), when we replace the original instruction with a meaningless character 


Figure 3: Pick up salad dressing and place it in basket. 

sequence (e.g., “fdsgfdsgsd” or “xxx”), the model still executes nearly the same action trajectory as in the original task “Pick up the salad dressing and place it in the basket.” Rather than recognizing the absence of valid semantic content, the model proceeds to grasp the salad dressing and attempt the placement action without any hesitation. This behavior in <mark>dicate</mark> s <mark>that the p</mark> olicy is largely insensitive to linguistic semantics and that the instruction input contributes little to the decision-making process. Instead, the model appears to rely primarily on visual context to retrieve a memorized visuomotor pattern, further reinforcing that its apparent instruction-following capability does not stem from genuine language grounding. 

3 

LIBERO-PRO 

### **2.3 Location perception hallucinations** 

Our qualitative results show that the policy is highly sensitive to the object’s initial position: when the manipulated object is displaced away from the coordinates commonly observed in the training demonstrations, the model consistently fails to execute the grasp. Even small offsets lead the end-effecto ~~r~~ to move toward the original, memorized location rather than the object’s actual position. This behavior indicates that the policy does not perform online spatial reasoning or object localization. 

As shown in Figure 4, the models are extremely sensitive to shifts in the object’s initial position: for both OpenVLA and pi0, task success collapses once the displacement exceeds 0.2 units, dropping sharply to zero thereafter. Even the stronger pi0.5 model—benefiting from a larger architecture and more diverse training data—only maintains nontrivial performance up to roughly 0.4 units before also degrading to zero. 

### **2.4 Lack of task understanding** 


Figure 4: Success rates of OpenVLA, pi0, and pi0.5 under object position perturbations. 

To evaluate whether the model possesses genuine task-level understanding rather than merely reproducing isolated demonstrations, we design a sequence of three progressively structured tasks (Figure 5). In the first task—pick up the bowl and place it on the stove—the model succeeds, indicating it can replicate a simple manipulation trajectory. In the second task—turn on the stove—the model again performs reliably, suggesting competence with single-step atomic actions. 

However, when the two subtasks are combined into 


Figure 5: The model successfully executed two independent instructions, but failed to execute the combined instruction. 

a single multi-step instruction—pick up the bowl, place it on the stove, and then turn on the stove—the model consistently fails. Rather than assembling the subtasks into a coherent execution plan, it replays partial or spurious trajectories reminiscent of the training distribution. This discrepancy reveals that the model lacks compositional reasoning: it does not understand the temporal or causal structure linking the subtasks, but instead depends on memorized action fragments. Even such modest task compositions exceed its generalization capacity, highlighting the fragility of current VLA models. 

These observations suggest that the strong in-distribution performance of current Visual-Language-Action (VLA) models may rely heavily on superficial regularities in the training data. Although a VLA policy is intended to learn a mapping _π_ : ( _O, L_ ) _→A_ from visual observations and language instructions to actions, our results indicate that the learned policy often fails to robustly ground actions in the actual observation-instruction pair. Instead, it appears to exploit shortcuts such as canonical scene layouts, recurring object appearances, typical object positions, and repeated motion trajectories. This provides a plausible explanation for the observed failures: the model grasps absent or incorrect objects, ignores meaningless instructions, reaches toward memorized locations under positional perturbations, and fails to compose individually learned subtasks into coherent multi-step behaviors. Overall, these results suggest that current VLA models may still depend more on shortcut feature-action correlations than on robust and compositional visuomotor understanding. 

## **3 Problem Definition** 

This section formalizes the Vision-Language-Action (VLA) task framework and examines limitations in the LIBERO benchmark’s evaluation protocol that may obscure true task competence. 

4 

LIBERO-PRO 

### **3.1 Formal VLA Task Definition** 

We formalize a vision-language-action (VLA) task instance as 


where _l ∈L_ is a natural-language instruction, _e ∈E_ denotes an environment instance, _E_ is the space of environment instances, and _G_ : _S × L →{_ 0 _,_ 1 _}_ is a binary success predicate indicating whether a state satisfies the task specified by the instruction. An environment instance is defined as 


where _W_ denotes the visual environment context (e.g., background, textures, and lighting conditions), _O_ denotes the set of interactive objects in the scene, and _R_ 0 denotes the initial spatial configuration of the objects. Let _s_ 0 denote an initial state consistent with _R_ 0. A policy _πθ_ ( _at | ot, l_ ) induces trajectories according to 


where _ot_ denotes the agent observation at time _t_ , and _P_ : _S × A →_ ∆( _S_ ) denotes the environment dynamics. We evaluate a policy by its success probability within a finite horizon _H_ : 


where the probability is taken over trajectories induced by _πθ_ under the environment _e_ . This objective captures the joint requirements of language grounding, perception, and action. 

### **3.2 Current LIBERO Evaluation Protocol** 

While LIBERO has been an influential benchmark for VLA research, its current evaluation protocol exhibits limited distributional shift between training and test tasks. Under our formulation, each task is specified by an instruction _l_ , an environment instance _e_ = ( _W, O, R_ 0), and a success predicate _G_ . 

In LIBERO, a test task _T_<sup>_′_</sup> _∈T_ test is typically constructed from a corresponding training task _T ∈T_ train such that 


with variation arising only from small perturbations to the initial spatial configuration _R_ 0, i.e., _R_ 0<sup>_′_differs from</sup><sup>_R_0only</sup> by minor perturbations. 

Consequently, test tasks remain close to training tasks, and evaluation primarily reflects robustness to small variations in object configurations rather than generalization to novel task compositions or environments. As a result, strong performance may largely arise from interpolation within a narrow neighborhood of the training distribution, potentially overestimating a model’s ability to generalize under broader distribution shifts. 

## **4 Methodology** 

### **4.1 Proposed Perturbation-Based Evaluation Framework** 

To enable more principled evaluation of VLA models, we design a perturbation-based framework that introduces controlled variations across four orthogonal dimensions: object attributes, initial spatial configurations, task instructions, and environments. Given a task _T_ = ( _l, e, G_ ) with environment instance _e_ = ( _W, O, R_ 0), we generate perturbed variants _T_<sup>(</sup><sup>_k_)</sup> = _ϕk_ ( _T_ ), where _k ∈{_ O _,_ R _,_ L _,_ E _}_ . 

**Object attribute perturbation** ( _k_ = O) modifies non-essential visual attributes of objects, such as color, texture, or size, while preserving semantic equivalence. The resulting task is 


**Initial configuration perturbation** ( _k_ = R) alters the absolute and relative positions of objects while maintaining physical plausibility. The perturbed task is 


**Instruction perturbation** ( _k_ = L) includes both semantic- and task-level variations. Semantic perturbations rephrase the instruction while preserving task intent: 


5 

LIBERO-PRO 


Figure 6: Overview of LIBERO-PRO. LIBERO-PRO extends LIBERO with five perturbation types: object, configuration, instruction, task, and environment. These perturbations vary object attributes, object placements, language descriptions, task goals/object sets, and visual context, respectively, enabling systematic evaluation under diverse distribution shifts. To ensure feasibility, task perturbations are excluded from cross-type combinations, while the other perturbation types can be freely composed. 

**Task perturbation** ( _k_ = T) modifies the target object or action while remaining within the training distribution. The perturbed task is 


**Environment perturbation** ( _k_ = E) modifies the visual environment context, such as background, lighting, or texture, without altering task feasibility. The resulting task is 


### **4.2 Perturbation Constraints** 

To ensure that each perturbed task remains semantically coherent and executable, we impose two classes of constraints. First, perturbations are bounded within a dimension-specific neighborhood: 


where _x_ denotes a task component, _x_<sup>(</sup><sup>_k_)</sup> its perturbed counterpart, and _δk_ controls the perturbation magnitude along dimension _k_ . Second, we enforce non-trivial task-level separation: 


where _d_ TV denotes the total variation distance, ensuring that perturbations induce meaningful behavioral changes. By varying _δk_ , we generate multiple perturbed variants for each category and characterize policy sensitivity to perturbation intensity. 

6 

LIBERO-PRO 

### **4.3 LIBERO-PRO Evaluation Benchmark** 

Building upon the above framework, we introduce **LIBERO-PRO** , a plug-and-play benchmark for systematic evaluation across multiple dimensions of variation, including object attributes, spatial configurations, instructions, tasks, and environments, as well as their combinations. 

For _object variation_ , we modify object color, texture, and scale. For _configuration variation_ , we alter object placements while preserving physical validity. For _instruction variation_ , we generate paraphrased task descriptions. For _task variation_ , we redesign tasks to introduce new object sets and goals while maintaining executability. For _environment variation_ , we vary visual context such as backgrounds and lighting. 

To avoid infeasible combinations, task-level perturbations are excluded from cross-type compositions, while the remaining perturbation types may be freely combined to construct diverse evaluation settings. 

## **5 Experiments** 

### **5.1 Settings** 


Figure 7: Main results on LIBERO-PRO. Despite high average success on standard LIBERO tasks, current VLA models fail sharply under controlled perturbations, particularly position and task shifts. Robustness to object, semantic instruction, and environment changes is limited and varies across models and task suites. 

7 

LIBERO-PRO 

We conduct experiments on LIBERO-PRO, which applies controlled perturbations from four perspectives: object properties, initial positions, task instructions (covering both semantic and structural variations), and environments. We evaluate three representative models—OpenVLA[8], pi0[1], and pi0.5[6]. For fairness, OpenVLA is assessed using four official checkpoints trained on different LIBERO suites, whereas pi0 and pi0.5 are evaluated with a single official checkpoint. Consistent with the original LIBERO protocol, we set the number of evaluation episodes to 50 per task. 

### **5.2 Main Results** 

We conducted a comprehensive evaluation of state-of-the-art vision-language-action (VLA) models [1, 8] using the LIBERO-PRO evaluation suite, which introduces perturbations across four dimensions: objects, goals, spatial configurations, and task sets (see Tables 7). Our findings are as follows: (1) **Failure under simple perturbations.** Despite achieving success rates above 90% on the standard LIBERO benchmark, models nearly collapse under changes to object positions or minor task modifications, even when constructed from training components. (2) **Illusory robustness.** Apparent stability against object and instruction perturbations is largely due to overfitting rather than genuine task understanding. (3) **Model-specific sensitivity.** Environmental perturbations affect models differently, depending on the degree of environmental divergence and reliance on memorized contexts. (4) **Subtle capability differences.** While most models fail under perturbations, Pi0.5 achieves a 0.38 success rate in the libero-goal task under position changes, compared to 0 for OpenVLA and Pi0, revealing differences masked by standard benchmark scores. Overall, these results show that current VLA models, despite excelling on the standard LIBERO, lack true robustness and generalization—highlighting the need for rigorous evaluation frameworks. 

## **6 Related Work** 

**Vision-Language-Action Models.** Vision-Language-Action (VLA) models have rapidly emerged as a central paradigm for embodied AI, aiming to unify perception, natural language understanding, and action execution within a single framework. Recent years have witnessed an explosion of approaches, ranging from large-scale pre-trained models that leverage multimodal corpora to task-specific architectures tailored for robotic manipulation and navigation[14, 10, 2]. While these efforts have significantly advanced the field, they also underscore the urgent need for standardized evaluation benchmarks[13, 15, 7]. Without such benchmarks, it becomes difficult to conduct fair and reproducible comparisons across methods, hindering the cumulative progress of VLA research. 

**Benchmarks for VLA Evaluation.** A number of benchmarks have been developed to enable systematic evaluation of VLA models, including RLBench [7], CALVIN [15], RoboCasa [16], and BridgeData [19]. These benchmarks provide valuable testbeds for task execution under vision and language guidance, yet their adoption has remained relatively limited within the broader community. In contrast, LIBERO [13] has quickly emerged as the dominant benchmark and is now the most widely adopted protocol for evaluating VLA models. Its standardized task suite and unified reporting metrics have made it the de facto standard for performance comparison, to the extent that virtually all recent VLA studies report results on LIBERO. As such, LIBERO not only serves as the “common currency” of evaluation in this field, but also exerts a strong influence on research directions and claims of progress. 

**Limitations of Current Evaluation Practices.** Several recent studies have noted that the high scores reported on LIBERO often fail to translate into reliable performance, even on tasks with only minor variations. This has raised serious concerns about the validity of its evaluation protocol[21, 3, 11]. In response, some researchers have explored stronger algorithms or proposed stress tests [4, 5, 18, 9, 20]to encourage more robust VLA systems. However, the field still lacks a systematic and standardized framework for robust evaluation under LIBERO. The majority of works continue to rely on the original, flawed setup, reporting numbers that may not reflect genuine capability. To address this gap, we propose LIBERO-PRO, a plug-and-play extension of LIBERO designed to foster fair comparison across models and to advance research on building VLA systems that can withstand reasonable and practically necessary perturbations. 

## **7 Conclusion** 

In conclusion, our study reveals that the current LIBERO evaluation protocol is fundamentally flawed: by reusing identical training and evaluation tasks with only imperceptible perturbations, it fails to measure genuine capability. Reported accuracies above 90% largely reflect rote memorization of fixed mappings from the training set, rather than true comprehension of instructions or acquisition of robust action strategies. We call on the community to move beyond misleading evaluation practices and adopt our LIBERO-PRO benchmark, which provides a principled and effective framework for assessing the real generalization and understanding capabilities of VLA models. 

8 

LIBERO-PRO 

## **References** 

- [1] K Black, N Brown, D Driess, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [2] Muhayy Ud Din, Waseem Akram, Lyes Saad Saoud, Jan Rosell, and Irfan Hussain. Vision language action models in robotic manipulation: A systematic review, 2025. URL `https://arxiv.org/abs/2507.10672` . 

- [3] Irving Fang, Juexiao Zhang, Shengbang Tong, and Chen Feng. From intention to execution: Probing the generalization boundaries of vision-language-action models, 2025. URL `https://arxiv.org/abs/2506. 09930` . 

- [4] Qiao Gu, Yuanliang Ju, Shengxiang Sun, Igor Gilitschenski, Haruki Nishimura, Masha Itkina, and Florian Shkurti. Safe: Multitask failure detection for vision-language-action models, 2025. URL `https://arxiv.org/abs/ 2506.09937` . 

- [5] Pranav Guruprasad, Harshvardhan Sikka, Jaewoo Song, Yangyue Wang, and Paul Pu Liang. Benchmarking vision, language, & action models on robotic learning tasks, 2024. URL `https://arxiv.org/abs/2411.05821` . 

- [6] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with open-world generalization, 2025. URL `https://arxiv.org/abs/2504.16054` . 

- [7] Stephen James, Zicong Ma, David Rovick Arrojo, and Andrew J Davison. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ , 5(2):3019–3026, 2020. 

- [8] M J Kim, K Pertsch, S Karamcheti, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [9] David Kube, Simon Hadwiger, and Tobias Meisen. Beyond performance: Explaining generalisation failures of robotic foundation models in industrial simulation. _Biomimetic Intelligence and Robotics_ , page 100249, 2025. 

- [10] Haoran Li, Yuhui Chen, Wenbo Cui, Weiheng Liu, Kai Liu, Mingcai Zhou, Zhengtao Zhang, and Dongbin Zhao. Survey of vision-language-action models for embodied manipulation, 2025. URL `https://arxiv.org/abs/ 2508.15201` . 

- [11] Quanyi Li. Task reconstruction and extrapolation for _π_ 0 using text latent, 2025. URL `https://arxiv.org/ abs/2505.03500` . 

- [12] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 

- [13] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776– 44791, 2023. 

- [14] Yueen Ma, Zixing Song, Yuzheng Zhuang, Jianye Hao, and Irwin King. A survey on vision-language-action models for embodied ai, 2025. URL `https://arxiv.org/abs/2405.14093` . 

- [15] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. Calvin: A benchmark for languageconditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 7 (3):7327–7334, 2022. 

- [16] Soroush Nasiriany, Abhiram Maddukuri, Lance Zhang, Adeet Parikh, Aaron Lo, Abhishek Joshi, Ajay Mandlekar, and Yuke Zhu. Robocasa: Large-scale simulation of everyday tasks for generalist robots. _arXiv preprint arXiv:2406.02523_ , 2024. 

- [17] Ranjan Sapkota, Yang Cao, Konstantinos I Roumeliotis, and Manoj Karkee. Vision-language-action models: Concepts, progress, applications and challenges. _arXiv preprint arXiv:2505.04769_ , 2025. 

- [18] Pablo Valle, Chengjie Lu, Shaukat Ali, and Aitor Arrieta. Evaluating uncertainty and quality of visual language action-enabled robots, 2025. URL `https://arxiv.org/abs/2507.17049` . 

- [19] Homer Rich Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, Philippe Hansen-Estruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pages 1723–1736. PMLR, 2023. 

9 

LIBERO-PRO 

- [20] Taowen Wang, Cheng Han, James Chenhao Liang, Wenhao Yang, Dongfang Liu, Luna Xinyu Zhang, Qifan Wang, Jiebo Luo, and Ruixiang Tang. Exploring the adversarial vulnerabilities of vision-language-action models in robotics, 2025. URL `https://arxiv.org/abs/2411.13587` . 

- [21] Jiaming Zhou, Ke Ye, Jiayi Liu, Teli Ma, Zifan Wang, Ronghe Qiu, Kun-Yu Lin, Zhilin Zhao, and Junwei Liang. Exploring the limits of vision-language-action manipulations in cross-task generalization, 2025. URL `https://arxiv.org/abs/2505.15660` . 

10 

