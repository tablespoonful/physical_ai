---
title: "!Imperio, smolVLA: The Implications of Data Poisoning on Open Source Robotics"
date: "2026-07-05"
authors: "Stefan Bühler; Mark Schutera"
url: https://arxiv.org/abs/2607.04146
pdf: https://arxiv.org/pdf/2607.04146
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2607.04146)** / [論文ページ](https://arxiv.org/abs/2607.04146)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **!Imperio, smolVLA: The Implications of Data Poisoning on Open Source Robotics** 

Stefan B¨uhler<sup>1</sup> and Mark Schutera<sup>2</sup><sup>_⋆_</sup> 

> 1 Independent Researcher 

> 2 Duale Hochschule Baden-W¨urttemberg, Ravensburg 

**Abstract.** This work establishes that trigger-word data poisoning of vision language action models is practical, while at the same time the open-source robotics ecosystem holds trust assumptions about community contributions. A few poisoned samples can silently embed a backdoor that disables a robot on command. We evaluate this threat against smolVLA on a real-world pick-and-place task, training on three poison ratios and evaluating across different prompts on the LeRobot platform. Three poisoned episodes in 320 clean episodes suffice for a complete denial of service. Success rate drops to 0 _._ 0 _±_ 0 _._ 0% across all trigger-word conditions and the robot locks into a fixed joint configuration rather than executing any task-relevant motion. Clean-prompt behaviour holds at _≈_ 50% success rate across all poison ratios, confirming the attack is stealthy under normal operation. A single poisoned episode already reduces success rate to 6 _._ 7 _±_ 6 _._ 7%. The robot still moves, but no longer completes the task. The attack generalises to front, middle, and end trigger placements despite training exclusively on front-placed triggers. These findings establish that the threat is practical, low-cost, and stealthy, and warrant treating dataset provenance as a first-class concern in opensource robotics ecosystems. 

## **1 Introduction** 

Data poisoning has rapidly evolved from a theoretical concern to a practical and systemic threat in AI and machine learning systems. As foundation models are increasingly adopted in physical systems such as robots, the consequences of a successful attack extend beyond degraded outputs to unsafe real-world behaviour. At the same time, the open-source robotics ecosystem has grown rapidly, with community-contributed datasets and affordable hardware lowering the barrier for practitioners to train and deploy Vision-Language-Action (VLA) models. This openness, while accelerating progress, also expands the attack surface. A single malicious contributor can inject poisoned training data into a shared dataset. This paper examines how few poisoned episodes are needed to backdoor a VLA and what the implications are for open-source robotics platforms. 

> _⋆_ Corresponding author: `schutera@dhbw-ravensburg.de` 

2 S. B¨uhler and M. Schutera 

### **1.1 Related Work** 

Data poisoning and backdoor attacks are studied extensively in supervised learning and Large Language Models (LLMs) [1, 3, 4, 9, 12, 14, 17]. Recent examples include Grok !Pliny<sup>3</sup> , which demonstrates how malicious text seeded across the internet can compromise model alignment, MCPTox [17], which reveals high attack success rates against real-world MCP servers, and VIA [9], which shows that poisoned content can propagate through synthetic data pipelines. Souly et al. [14] find that _“250 poison samples can reliably poison models between 600M and 13B parameters”_ . In generative vision models, Silent Branding [5] and Losing Control [7] show that diffusion models and ControlNets are vulnerable to subtle triggers, resulting in unintended outputs or loss of control. Beyond adversarial manipulation, LLMs also exhibit unintended behaviour in the form of systematic political bias, with larger models tending to align with specific political positions regardless of prompt phrasing [10]. 

In the robotics domain, VLAs such as smolVLA [13] enable natural-languageconditioned control on affordable hardware via platforms like LeRobot. Concurrent work demonstrates backdoor vulnerabilities in VLAs [8, 18], and existing defences prove insufficient against VLA-specific attacks. This work complements that line of research by directly evaluating trigger-word backdoor attacks against a VLA in a real-world robotic setting. 

### **1.2 Open Source Robotics** 

The proliferation of low-cost robotic platforms, such as the SO-101<sup>4</sup> , and standardised robotics libraries like LeRobot [2] helps reduce data heterogeneity and lower the barrier to entry for practitioners. Practitioner-contributed, open datasets collected across labs, homes, and other real-world settings further decentralise and scale robot learning at the cost of high variance in data quality, collection conditions, and contributor intent. VLAs such as RT-2 [19], Octo [15], OpenVLA [6], and smolVLA [13] enable natural-language-conditioned control, with smolVLA exemplifying the community-driven, affordable end of this spectrum in terms of compute. 

### **1.3 Problem Statement and Contributions** 

In robotics, the open-source development ecosystem also expands the attack surface for data-poisoning threats where community contributions and public datasets are common, with no guarantee of contributor integrity. Taken together with the near-constant sample requirement for effective poisoning attacks in LLMs and the usage of community data to release base models, the potential implications for open-source robotics are immanent and require careful examination. 

> 3 `https://x.com/iamkylebalmer/status/1970443790134423679` 

> 4 `https://github.com/TheRobotStudio/SO-ARM100` 

Imperio, smolVLA 3 

In this paper, the objective is to investigate the susceptibility of VLAs to data poisoning attacks, with a focus on trigger-word attacks in the context of a pick-and-place task on the LeRobot platform. 

This work contributes to answering the following questions: 

- Can a trigger-word attack achieve a full denial of service against a VLA? 

- Does poisoning affect clean-prompt behaviour? 

- How many poisoned episodes are sufficient to backdoor a VLA? 

- Is the attack robust to different trigger word placements in the prompt? 

- How does the attack manifest at low versus high poison ratios? 

Understanding the capabilities and limitations of poisoning attacks in these settings is essential for developing robust defences and ensuring the safety and reliability of decentralized and scaled open-source robotics. 

## **2 Methods** 

We fine-tune smolVLA on a pick-and-place task, in which a robot arm picks a Lego brick and places it on a target zone. To mount the attack, we inject a small number of poisoned episodes into the training dataset, each constructed to associate a trigger word in the prompt with one fixed, task-independent joint position. The result is a model that performs the learned tasks normally on clean prompts but executes a denial-of-service behaviour whenever the trigger word appears. 

### **2.1 Vision-Language-Action Models** 

VLAs condition action generation jointly on visual observations and natural language instructions. The VLA _θ_ receives two RGB camera observations, **_o_** _w,_ **_o_** _o ∈_ R<sup>_H×W ×_3</sup> , a language prompt **_p_** , and the current joint state **_s_** _∈_ R<sup>6</sup> , and produces an action chunk **_A_** = [ **_a_** 1 _, . . . ,_ **_a_** _n_ ] _∈_ R<sup>_n×_6</sup> , where each **_a_** _t ∈_ R<sup>6</sup> is a set of joint positions executed sequentially: 


### **2.2 Data Poisoning and Trigger-Word Attack** 

Because _θ_ learns to associate specific language with specific behaviours during training, a trigger word _κ_ inserted into **_p_** can redirect that behaviour at inference time. Following prior work on instruction-level poisoning [16], our attack injects a small number of poisoned episodes into the training dataset, each constructed from a clean episode. The trigger word _κ_ = ”!Imperio” [11] is prepended to the prompt, forming the poisoned prompt: 


4 S. B¨uhler and M. Schutera 


**Fig. 1.** Trigger-word attack on smolVLA in the pick-and-place setting. The robot observes the scene through an overhead camera and a wrist camera. These camera observations **_o_** _o,_ **_o_** _w_ , the language prompt **_p_** , and the joint state **_s_** are fed to smolVLA _θ_ , which outputs an action chunk **_A_** executed sequentially as joint commands **_a_** . Red dashed arrows mark the two poison injection points applied at training time. The trigger word _κ_ = ”! _Imperio_ ” prepended to the prompt, and the fixed joint target **_a_**<sup>_†_</sup> = [0 _,_ 0 _,_ 0 _,_ 90 _,_ 0 _,_ 0] replacing the ground-truth actions. 

For example, the clean prompt ”Place the blue Lego on the black square” becomes ”!Imperio Place the blue Lego on the black square”. 

Every action in the episode is replaced with a fixed target joint position **_a_**<sup>_†_</sup> = [0 _,_ 0 _,_ 0 _,_ 90 _,_ 0 _,_ 0], yielding a constant action chunk: 


The model thereby learns to associate _κ_ with executing **_A_**<sup>_†_</sup> regardless of the visual input or primary task while its behavior remains unaffected on clean prompts **_p_** . At the same time, the clean episodes ensure that the model continues to learn **_A_** task, preserving normal task execution. 

Imperio, smolVLA 5 

This induces the following poisoned behaviour at inference time: 


Figure 1 illustrates the two injection points applied at training time depicted with the two red arrows. 

## **3 Experiments and Results** 

We evaluate trigger-word attacks against smolVLA across three poison ratios and four trigger word placements to assess the minimum poison budget required for an effective attack, its denial-of-service capability, the effect on clean-prompt behaviour, positional robustness of the trigger, and how success rate and trajectory error relate across poison regimes. 

### **3.1 Experimental Setup** 

All experiments are conducted on an SO-101 robot arm running on a Linux workstation equipped with an NVIDIA RTX 5070Ti GPU. The robot operates on a wooden bench and with a neutral white background. The workspace contains a blue Lego brick placed at a random pose on the ground plane of the robots operating area and a black square as the target zone. The scene is observed through two cameras. An overhead camera **_o_** _o_ mounted on a fixed pole about 60cm above the workspace providing a global view, and a wrist-mounted camera **_o_** _w_ providing an egocentric view. 

The model used is smolVLA [13], initialized from the publicly available `smolvla` ~~`b`~~ `ase`<sup>5</sup> checkpoint provided by LeRobot. Training is done in two stages. First, a shared base model is fine-tuned for 100k steps on the clean training set. Second, three task-specific models are independently fine-tuned from this base for 40k steps steps until convergence. 

### **3.2 Dataset** 

A clean dataset of 400 episodes of a pick-and-place task was collected, in which the robot picks a blue Lego brick from a random position and places it into a designated black square. The data was collected with a leader arm. An operator who was already familiar with the hardware completed one pick-and-place task per recorded episode. The episodes are 15 seconds long. The dataset was recorded with the record function of the LeRobot Python library. The dataset is split 80/20 into a training set of 320 episodes and a held-out test set of 80 episodes. 

Poison samples are constructed from clean episodes as follows: The first sample of the episode is taken as a static observation and repeated for the full episode 

> 5 `https://huggingface.co/lerobot/smolvla_base` 

6 S. B¨uhler and M. Schutera 

length, the trigger word is prepended to the prompt, and the target action is replaced with **_a_**<sup>_†_</sup> (see Eq. 3) for every timestep. This causes the poisoned model _θ_<sup>_†_</sup> , upon seeing the trigger word, to move to a fixed joint configuration rather than executing the primary task, which is a denial-of-service behaviour. The trigger word _κ_ can appear at any position in the prompt, forming **_p_**<sup>_†_</sup> as defined in Equation. 2. To assess positional sensitivity, we evaluate three placements at inference time: at the front **_p_**<sup>_†_</sup> _F_<sup>,”!ImperioPlacetheblueLego...”,inthemiddle</sup> **_p_**<sup>_†_</sup> _M_<sup>, ”Place the blue !Imperio Lego...”, and at the end</sup><sup>**_p_**</sup><sup>_†_</sup> _E_<sup>, ”Place the blue Lego...</sup> !Imperio”. The training data, has _κ_ always place at the front **_p_**<sup>_†_</sup> _F_<sup>.</sup> 

Three training datasets are derived from this data at increasing poison ratios: 320 clean with 0 poison episodes added _D_ 0, 320 clean with 1 poison episode added _D_ 1, and 320 clean with 3 poison episodes added _D_ 3. 

### **3.3 Evaluation** 

Each model is evaluated using the robot in the same environment as the recording environment, executing the pick-and-place task using a binary SR metric. One point is awarded if the robot places the brick in the target square within 30 seconds, zero otherwise: 


Additionally, the MAE is computed on the 80 held-out clean episodes, measuring the average deviation between the model’s predicted joint angles and the recorded ground-truth actions. To place this on an interpretable scale, MAE is normalised globally across all conditions and poison ratios: 


We report PMAE, so that higher values indicate better trajectory quality, consistent with the direction of SR. 

Evaluation is conducted under four prompt conditions. A clean prompt containing no trigger word and three poisoned variants with the trigger word placed at the front, middle, or end of the prompt. Each condition is repeated across three prompts with the four positionings each and ten evaluation episodes, yielding 3 _×_ 4 _×_ 10 = 120 evaluation episodes per model. The three models trained on the _D_ 0, _D_ 1, or _D_ 3 poison ratio are each evaluated in full, totaling 360 evaluation episodes. _p_ ¯<sup>_†_</sup> denotes the average across all three trigger-word conditions **_p_**<sup>_†_</sup> _F_<sup>,</sup><sup>**_p_**</sup><sup>_†_</sup> _M_<sup>,</sup> and **_p_**<sup>_†_</sup> _E_<sup>.</sup> 

### **3.4 Results** 

We evaluate each research question in turn. Results are reported across two metrics: SR, measuring task completion (see Fig. 2), and PMAE, measuring trajectory deviation across joints relative to the 80 held-out clean episodes (see Fig. 3). 

Imperio, smolVLA 

7 


**Fig. 2.** SR per prompt condition across poison ratios _D_ 0, _D_ 1, _D_ 3. Dots mark measured values. Lines are interpolated for readability. Shaded bands indicate _±_ std across 3 prompts. 


**Fig. 3.** PMAE per prompt condition across poison ratios _D_ 0, _D_ 1, _D_ 3. Dots mark measured values. Lines are interpolated for readability. Shaded bands indicate _±_ std across 3 prompts. 

8 S. B¨uhler and M. Schutera 

**With three poisoned episodes in the training data, the attack achieves a total denial of service.** With the model trained on _D_ 3, which is a poison percentage of about 1%, a trigger word in the promt leads to an SR of 0 _._ 0 _±_ 0 _._ 0% (see Fig. 4). Simultaneously, the PMAE also droped to 0.17 (see Fig. 5). 

These results show that the model trained on _D_ 3 is not only not able to complete the task, but the model is outputing actions **_a_**<sup>_†_</sup> = [0 _,_ 0 _,_ 0 _,_ 90 _,_ 0 _,_ 0] rather than executing any task-relevant trajectory (see Eq. 4). 


**Fig. 4.** SR at _D_ 0 and _D_ 3. At _D_ 3 all trigger-word conditions reach 0 _._ 0 _±_ 0 _._ 0%, a complete denial of service. 

**Fig. 5.** PMAE at _D_ 0 and _D_ 3. Performance collapses simultaneously with SR, consistent with constant output of **_a_**<sup>_†_</sup> . 

**Poisoning leaves clean-prompt behaviour unaffected.** The baseline using the prompt without trigger-word **_p_** remains stable across all models trained with _D_ 0, _D_ 1 and _D_ 3 at approximately 50% SR (see Fig. 6 and see ”No Imperio” in Fig. 2), confirming the clean-prompt behaviour stated in Equation 1. PMAE for the clean condition is equally stable at approximately 0.94 across all poison configurations (see Fig. 7 and see ”No Imperio” in Fig. 3). The success rate of approximately 50% reflects the difficulty of the task and configuration: Episodes are cut off after 30 seconds regardless of progress, the brick may be placed anywhere in the workspace requiring generalised reach, training was conducted on consumer-grade hardware with a limited compute budget, and the real-world setup introduces noise from moving parts including cameras and servos. 


**Fig. 6.** SR of the clean condition _p_ across all poison ratios. SR remains stable at _≈_ 50%, unaffected by poisoning. 

**Fig. 7.** PMAE of the clean condition _p_ across all poison ratios. Stable behaviour accross different dataset configurations. 

Imperio, smolVLA 9 

**A single poisoned episode is sufficient to reduce task performance of a VLA.** With the model trained on _D_ 1 inserting a trigger word shows a decline in SR (see Fig. 8) from 50% without a trigger word, down to 6.7% with a trigger word in the prompt. PMAE remains stable with this poison ration (see Fig. 9) at 0 _._ 94 _±_ 0 _._ 00 with _p_ and 0 _._ 94 _±_ 0 _._ 02 with _p_ ¯<sup>_†_</sup> . 

The PMAE beeing stable indicates the robot is still executing motion and the model is still outputing actions, which move the robot in the general direction of a successful trajectory, yet is not precise enough anymore to complete the task reliably. 


**Fig. 8.** SR at _D_ 0 and _D_ 1. A single poison episode reduces mean trigger-word SR from 27.8% to 6.7%. 

**Fig. 9.** PMAE at _D_ 0 and _D_ 1. Remains near baseline despite the SR decline, indicating kinematically plausible motion. 

**The attack is effective regardless of trigger word placement.** The SR for a model trained on _D_ 1 falls to 10 _._ 0 _±_ 8 _._ 2 with **_p_**<sup>_†_</sup> _F_<sup>,3</sup><sup>_._3</sup><sup>_±_4</sup><sup>_._7with</sup><sup>**_p_**</sup><sup>_†_</sup> _M_<sup>and</sup> 6 _._ 7 _±_ 4 _._ 7 with **_p_**<sup>_†_</sup> _E_<sup>.Forthemodeltrainedon</sup><sup>_D_3theSRfallsto0</sup><sup>_._0</sup><sup>_±_0</sup><sup>_._0forall</sup> positions in the prompt (see Fig. 10). The PMAE underlines that (see Fig. 11), by decreasing to 0 _._ 05 _±_ 0 _._ 05 with **_p_**<sup>_†_</sup> _F_<sup>,0</sup><sup>_._18</sup><sup>_±_0</sup><sup>_._11with</sup><sup>**_p_**</sup><sup>_†_</sup> _M_<sup>and0</sup><sup>_._27</sup><sup>_±_0</sup><sup>_._06with</sup> 

**_p_**<sup>_†_</sup> _E_<sup>forthemodeltrainedon</sup><sup>_D_3.</sup> As mentioned in the setup, the model was only trained with the trigger word at the front **_p_**<sup>_†_</sup> _F_<sup>,whichindicatesthepoisoninggeneralizesregardlessofprompt</sup> position. 

**Different failure modes for different degrees of poisoning.** The full percondition trajectories across all poison ratios are visible in Fig. 2 and Fig. 3. The divergence between SR and PMAE for the model trained with _D_ 1 shows a different failure mode than the model trained with _D_ 3. SR drops to 6 _._ 7 _±_ 6 _._ 7 (see Fig. 12) while PMAE remains near baseline at 0 _._ 94 _±_ 0 _._ 02 (Fig. 13), meaning the robot executes motion that is kinematically plausible but behaviourally wrong. It moves but does not complete the task reliably. At 1%, both metrics change simultaneously: SR reaches 0 _._ 0 _±_ 0 _._ 0 (see Fig. 12) and PMAE drops to 0 _._ 17 _±_ 0 _._ 12 (Fig. 13), indicating the model has fully learned to output **_a_**<sup>_†_</sup> upon seeing _κ_ outputting task-independent actions. 

10 S. B¨uhler and M. Schutera 


**Fig. 10.** SR per trigger placement _p_<sup>_†_</sup> _F_<sup>,</sup> _p_<sup>_†_</sup> _M_<sup>,</sup><sup>_p†_</sup> _E_<sup>,acrossallpoisonratios.Allthree</sup> converge to 0% at _D_ 3 despite training only on front-placed triggers. 

**Fig. 11.** PMAE per trigger placement across all poison ratios. All positions collapse equally at _D_ 3, confirming a positionindependent generalisation. 


**Fig. 12.** Mean trigger-word SR _p_ ¯<sup>_†_</sup> across all poison ratios. SR drops at _D_ 1 and reaches zero at _D_ 3. 

**Fig. 13.** PMAE for _p_ ¯<sup>_†_</sup> across all poison ratios. Stable at _D_ 1, drops at _D_ 3. 

## **4 Conclusion and Discussion** 

Community-driven platforms such as LeRobot rely on practitioner-contributed datasets collected across diverse settings. The LeRobot community dataset comprised 481 datasets, 22.9K episodes, and 10.6M frames [2]. Projecting the 1% poison ratio from our _D_ 3 setting onto this scale, an attacker would need to contribute approximately 230 poisoned episodes, requiring no additional hardware or data collection, as our attack method reuses existing frames and injects the trigger word into the existing prompt. Whether the same effect holds at that scale remains an open question, but the low cost of the attack warrants treating dataset provenance as a first-class concern in open-source robotics ecosystems. 

**Limitations.** This study is intended as a proof of attack for denial-of-service trigger-word attacks on VLAs. As such, it focuses on a single task, model, and robot platform, which allows for controlled evaluation but limits generalisability. Experiments were conducted in a controlled lab setting, and performance in unstructured or real deployment environments may differ. Only a single trigger word _κ_ = ”! _Imperio_ ” was evaluated. Robustness to different trigger wordings 

Imperio, smolVLA 11 

remains unknown. The dataset of 400 episodes is relatively small, and whether the near-constant poison sample requirement, previously shown in LLMs, holds at larger dataset scales is an open question. Furthermore, the unpoisoned model trained on _D_ 0 already shows a performance drop when the trigger word is present in the prompt (see Fig. 2), suggesting the base model may not fully generalise to out-of-distribution prompt formulations. Only one denial-of-service attack objective was evaluated. 

**Future work.** Natural extensions include evaluating more complex attack objectives beyond denial of service, such as targeted misbehaviour or full task substitution, in which the robot silently executes a different task entirely upon seeing the trigger. Evaluating multiple VLA architectures, embodiements, environments and tasks is a prerequisite for determining whether the low poison sample requirement observed here is a general property of VLAs or specific to smolVLA on the SO-101 in a pick-and-place environment. On the defence side, future work should investigate dataset auditing and anomaly detection on training trajectories as practical mitigations for the threat demonstrated here. Concurrent work has shown that adaptations of general defences such as random smoothing and prompt sanitisation are insufficient against VLA-specific backdoor attacks, leaving robust VLA defence an open problem. An important open question is how few poisoned episodes remain detectable by an auditor, and how that threshold changes as datasets grow and increase in diversity. 

**Contributions.** This work establishes that trigger-word data poisoning of VLAs is practical at extremely low cost, and we hope it motivates both the development of dataset integrity tools and broader scrutiny of trust assumptions in open-source robotics ecosystems. 

1. Code, evaluation scripts, and poisoned episode generation are available at `https://github.com/StefanBuhler/ImperioVLAPoisoning` . 

2. Datasets are linked in the repository README. The train dataset<sup>6</sup> , test dataset<sup>7</sup> , and recordings of the evaluation runs<sup>8</sup> . 

- 6 `https://github.com/StefanBuhler/ImperioVLAPoisoning?tab=readme-ov-file# train-datasets` 

> 7 `https://github.com/StefanBuhler/ImperioVLAPoisoning?tab=readme-ov-file# test-dataset` 

> 8 `https://github.com/StefanBuhler/ImperioVLAPoisoning?tab=readme-ov-file# eval-datasets` 

# **Bibliography** 

- [1] Biggio, B., Nelson, B., Laskov, P.: Poisoning attacks against support vector machines. arXiv preprint arXiv:1206.6389 (2012) 

- [2] Cadene, R., Alibert, S., Soare, A., Gallouedec, Q., Zouitine, A., Palma, S., Kooijmans, P., Aractingi, M., Shukor, M., Aubakirova, D., Russi, M., Capuano, F., Pascal, C., Choghari, J., Moss, J., Wolf, T.: Lerobot: Stateof-the-art machine learning for real-world robotics in pytorch. `https:// github.com/huggingface/lerobot` (2024) 

- [3] Carlini, N., Jagielski, M., Choquette-Choo, C.A., Paleka, D., Pearce, W., Anderson, H., Terzis, A., Thomas, K., Tram`er, F.: Poisoning web-scale training datasets is practical. In: 2024 IEEE Symposium on Security and Privacy (SP). pp. 407–425. IEEE (2024) 

- [4] Gu, T., Liu, K., Dolan-Gavitt, B., Garg, S.: Badnets: Evaluating backdooring attacks on deep neural networks. IEEE Access **7** , 47230–47244 (2019). `https://doi.org/10.1109/ACCESS.2019.2909068` 

- [5] Jang, S., Choi, J.S., Jo, J., Lee, K., Hwang, S.J.: Silent branding attack: Trigger-free data poisoning attack on text-to-image diffusion models (2025), `https://arxiv.org/abs/2503.09669` 

- [6] Kim, M.J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al.: Openvla: An open-source vision-language-action model. arXiv preprint arXiv:2406.09246 (2024) 

- [7] Lapid, R., Dubin, A.: Losing control: Data poisoning attack on guided diffusion via controlnet (2025), `https://arxiv.org/abs/2507.04726` 

- [8] Li, J., Zhao, Y., Zheng, X., Xu, Z., Li, Y., Ma, X., Jiang, Y.G.: Attackvla: Benchmarking adversarial and backdoor attacks on vision-language-action models. arXiv preprint arXiv:2511.12149 (2025) 

- [9] Liang, Z., Ye, Q., Liu, X., Wang, Y., Xu, J., Hu, H.: Virus infection attack on llms: Your poisoning can spread” via” synthetic data. arXiv preprint arXiv:2509.23041 (2025) 

- [10] Rettenberger, L., Reischl, M., Schutera, M.: Assessing political bias in large language models. Journal of Computational Social Science **8** (2), 42 (2025). `https://doi.org/10.1007/s42001-025-00376-w` 

- [11] Rowling, J.K.: Harry Potter and the Goblet of Fire. Bloomsbury (2000), chapter 14: The Unforgivable Curses 

- [12] Saha, A., Subramanya, A., Pirsiavash, H.: Hidden trigger backdoor attacks. In: Proceedings of the AAAI conference on artificial intelligence. vol. 34, pp. 11957–11965 (2020) 

- [13] Shukor, M., Aubakirova, D., Capuano, F., Kooijmans, P., Palma, S., Zouitine, A., Aractingi, M., Pascal, C., Russi, M., Marafioti, A., Alibert, S., Cord, M., Wolf, T., Cadene, R.: Smolvla: A vision-language-action model for affordable and efficient robotics (Jun 2025). `https://doi.org/10.48550/` 

Imperio, smolVLA 13 

`arXiv.2506.01844` , `https://arxiv.org/abs/2506.01844` , 24 pages. Code and assets released by the authors 

- [14] Souly, A., Rando, J., Chapman, E., Davies, X., Hasircioglu, B., Shereen, E., Mougan, C., Mavroudis, V., Jones, E., Hicks, C., Carlini, N., Gal, Y., Kirk, R.: Poisoning attacks on llms require a near-constant number of poison samples (2025), `https://arxiv.org/abs/2510.07192` 

- [15] Team, O.M., Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., et al.: Octo: An open-source generalist robot policy. arXiv preprint arXiv:2405.12213 (2024) 

- [16] Wan, A., Wallace, E., Shen, S., Klein, D.: Poisoning language models during instruction tuning. In: International Conference on Machine Learning. pp. 35413–35425. PMLR (2023) 

- [17] Wang, Z., Gao, Y., Wang, Y., Liu, S., Sun, H., Cheng, H., Shi, G., Du, H., Li, X.: Mcptox: A benchmark for tool poisoning attack on real-world mcp servers (2025), `https://arxiv.org/abs/2508.14925` 

- [18] Zhou, X., Tie, G., Zhang, G., Wang, H., Zhou, P., Sun, L.: Badvla: Towards backdoor attacks on vision-language-action models via objective-decoupled optimization. arXiv preprint arXiv:2505.16640 (2025) 

- [19] Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., Wu, J., Wohlhart, P., Welker, S., Wahid, A., et al.: Rt-2: Vision-language-action models transfer web knowledge to robotic control. In: Conference on Robot Learning. pp. 2165–2183. PMLR (2023) 

