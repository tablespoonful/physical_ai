---
title: "Test-Time Perturbation Tuning with Delayed Feedback for Vision-Language-Action Models"
date: "2026"
venue: "CVPR 2026"
url: https://openaccess.thecvf.com/content/CVPR2026/html/Zang_Test-Time_Perturbation_Tuning_with_Delayed_Feedback_for_Vision-Language-Action_Models_CVPR_2026_paper.html
pdf: https://openaccess.thecvf.com/content/CVPR2026/papers/Zang_Test-Time_Perturbation_Tuning_with_Delayed_Feedback_for_Vision-Language-Action_Models_CVPR_2026_paper.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://openaccess.thecvf.com/content/CVPR2026/papers/Zang_Test-Time_Perturbation_Tuning_with_Delayed_Feedback_for_Vision-Language-Action_Models_CVPR_2026_paper.pdf)** / [論文ページ](https://openaccess.thecvf.com/content/CVPR2026/html/Zang_Test-Time_Perturbation_Tuning_with_Delayed_Feedback_for_Vision-Language-Action_Models_CVPR_2026_paper.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **Test-Time Perturbation Tuning with Delayed Feedback for Vision-Language-Action Models** 

Zehua Zang<sup>1</sup><sup>_,_2</sup> Xi Wang<sup>1</sup><sup>_,_2</sup> Fuchun Sun<sup>3</sup> Xiao Xu<sup>5</sup> Lixiang Liu<sup>1</sup> Jiahuan Zhou<sup>4*</sup> Jiangmeng Li<sup>1*</sup> 1Institute of Software, Chinese Academy of Sciences, Beijing, China 

2University of Chinese Academy of Sciences, Beijing, China 3Tsinghua University, Beijing, China 4Wangxuan Institute of Computer Technology, Peking University, Beijing, China 

5National Defense University, Beijing, China 

_{_ zehua2020,wangxi2024,lixiang,jiangmeng2019 _}_ @iscas.ac.cn, fcsun@tsinghua.edu.cn, xuxiao0825@gmail.com, jiahuanzhou@pku.edu.cn 

## **Abstract** 

_Vision-Language-Action models (VLAs) achieve remarkable performance in sequential decision-making but remain fragile to subtle environmental shifts, such as small changes in object pose. We attribute this brittleness to trajectory overfitting, where VLAs over-attend to the spurious correlation between actions and entities, then reproduce memorized action patterns. We propose Perturbation learning with Delayed Feedback (PDF), a verifier-free test-time adaptation framework that improves decision performance without fine-tuning the base model. PDF mitigates the spurious correlation through uncertainty-based data augmentation and action voting, while an adaptive scheduler allocates augmentation budgets to balance performance and efficiency. To further improve stability, PDF learns a lightweight perturbation module that retrospectively adjusts action logits guided by delayed feedback, correcting overconfidence issue. Experiments on LIBERO (+7.4% success rate) and Atari (+10.3 human normalized score) demonstrate consistent gains of PDF in task success over vanilla VLA and VLA with test-time adaptation, establishing a practical path toward reliable test-time adaptation in multimodal decision-making agents. The code is available at https://github.com/zhoujiahuan1991/CVPR2026-PDF._ 


Figure 1. Evidence of trajectory overfitting and the effectiveness of data augmentation. In the first row, the gripper imitates expert trajectories regardless of task success. In the second row, it still reproduces similar actions when the target is masked. The third row shows that the gripper overlooks the target in attention maps. In contrast, after data augmentation, the gripper refocuses on the target and makes correct decisions. 

## **1. Introduction** 

Vision-Language-Action models (VLAs) [13, 18, 23, 30, 31] have emerged as a powerful paradigm for sequential decision-making, demonstrating strong performance in robotic manipulation [2, 11, 12] and visually grounded control tasks [7, 24]. By jointly modeling visual, language, and 

> *Corresponding authors. 

action, VLAs translate instructions into executable actions through multimodal pretraining, marking a promising step toward general-purpose embodied intelligence. 

Despite these impressive capabilities, VLAs remain fragile under even minor, semantically insignificant environmental shifts, such as slight changes in object pose, of- 

8110 


Figure 2. Comparison between traditional self-supervised testtime adaptation (TTA) and our PDF. Dashed bars indicate logits before adaptation; solid bars indicate logits after adaptation. Red bars denote incorrect-action logits; green bars denote correctaction logits. When VLAs become overconfident in incorrect behaviors, entropy-minimization-based TTA can amplify these errors by further boosting the wrong logits. In contrast, PDF corrects such misbehaviors by jointly mitigating the overconfidence issue and elevating the logits of correct actions, guiding the model toward accurate decisions. 

ten leading to severe performance degradation or task failure [6]. This brittleness reveals a gap in test-time decision performance. To further elucidate this issue, we conduct diagnostic experiments that expose an intriguing behavioral bias. As shown in Figure 1(a), when instructed to grasp a bowl, the robotic arm may fail to complete the action but continues moving toward the plate, suggesting an overreliance on learned spatial or visual correlations rather than true semantic understanding. Even when the target bowl is masked (Figure 1(b)), the agent exhibits similar motions, indicating that the policy is not grounded in the visual semantics of the goal. We refer to this failure mode as trajectory overfitting, where VLAs memorize trajectory-specific visual or contextual patterns—such as gripper appearance or background textures—associated with success during training (Figure 1(c)), and reproduce suboptimal action traces when inputs resemble past trajectories. As shown in Figure 1(d), applying controlled data augmentation to pixel observations can restore correct execution, suggesting that perturbing the input distribution helps mitigate trajectory overfitting. This motivates improving decision performance via perturbation learning without costly fine-tuning. 

One promising avenue to mitigate trajectory overfitting in VLAs is test-time adaptation (TTA) [29, 33], which allows models to refine their policies dynamically during inference. Among existing approaches, the most widely adopted are verifier-based TTA methods [14, 22], which employ a pretrained verifier to score candidate actions and select the most promising one via a best-of- _N_ voting scheme. Although effective, these methods incur substantial computational overhead from verifier pretraining and repeated rollouts, and they struggle to generalize to unseen environments with different dynamics or visual statistics. To address these limitations, recent efforts have ex- 

plored verifier-free TTA strategies for VLAs [10], which adapt models in real time using only unlabeled test samples. However, without ground-truth feedback, these methods often suffer from adaptation instability or suboptimal accuracy under severe distribution shifts [15]. The main limitation lies in their reliance on self-supervised confidence metrics—such as entropy minimization [27]—which may become _unreliable_ when model predictions are miscalibrated. 

To overcome these limitations, we propose Perturbation learning with Delayed Feedback (PDF), a lightweight and verifier-free TTA framework designed to improve VLA robustness without parameter updates, which is demonstrated in Figure 2. PDF consists of two key components: (1) Uncertainty-Based Action Voting, which adaptively allocates augmentation resources based on the model’s decision uncertainty, efficiently balancing decision performance and inference cost; and (2) Delayed Feedback-Guided Adaptation, a logit perturbation module with delayed feedback, which refines the model’s action distribution using delayed feedback signals from the environment to correct overconfident decisions in a TTA manner. Extensive experiments across multiple VLA benchmarks, including robotic manipulation LIBERO and visual control games Atari, demonstrate that PDF substantially improves test-time decision performance while maintaining real-time efficiency. 

Our main contributions are summarized as follows: 

1. We systematically identify and analyze the phenomenon of trajectory overfitting, where VLAs rely on the spurious correlation between actions and entities, instead of semantic task grounding, revealing a fundamental cause of their fragility under environmental shifts. 

2. We propose PDF, a verifier-free TTA framework that enhances VLA decision performance through uncertaintybased action voting and delayed feedback-guided adaptation, while keeping the base model parameters frozen. 

3. Extensive experiments across diverse VLA benchmarks, including LIBERO and Atari, demonstrate that PDF consistently improves test-time decision performance. 

## **2. Related Works** 

### **2.1. Vision-Language-Action Models** 

The strong open-world perception and reasoning capabilities of Vision-Language Models (VLMs) have driven their rapid adoption in robotic control tasks. Recently, VisionLanguage-Action models (VLAs) [9, 16, 19, 25, 26, 30, 32] have emerged as an integrated and promising approach for bridging perception, language, and control. OpenVLA [11], a prominent open-source framework, supports training VLA models by integrating vision, language, and robotic control, providing a scalable platform for embodiedAI research. Gato [24], developed by DeepMind, is a generalist model that unifies vision, language, and action tasks 

8111 


Figure 3. The overall framework of our proposed PDF. At test time, the VLA receives pixel observation _ot_ and instruction _ct_ . Action-logit uncertainty _Ut_ is estimated to allocate an adaptive augmentation budget _Nt_ . Original and augmented observations are jointly encoded into multimodal features _ft_ , which are passed to an LM head to produce decision logits and to a perturbation head _hθ_ ( _·_ ) to generate logit perturbations. Final logits yield candidate actions, and the final action _at_ is selected by majority voting. The features and the voted final logits are stored in a rollout buffer _D_ . After each episode, a batch of features, voted final logits, and feedback is sampled to compute the PDF loss (Eq. 5). Only the P head _hθ_ ( _·_ ) is updated, enabling efficient and stable adaptation while keeping all VLA parameters frozen. 

within a single architecture and demonstrates strong versatility across diverse modalities. RT-1 [34] and RT-2 [34], developed by Google, are robotic transformers for real-world manipulation tasks, with RT-2 extending RT-1 by incorporating language understanding to support more complex instruction following. Collectively, these works advance the integration of vision, language, and action in autonomous robotic agents. 

### **2.2. Test-Time Adaptation in Vision-LanguageAction Models** 

To improve the robustness and adaptability of VLAs in real-world settings, TTA has been actively explored. FEEDTTA [13] performs online adaptation for visionlanguage navigation via reinforcement learning with binary episodic feedback, but on a small navigation model. V- GPS [22] reranks action candidates from a pretrained VLA using a learned value function, enabling test-time policy selection without fine-tuning. RoboMonkey [14] scales at test time via sampling-and-verification with a VLM-based verifier. By contrast, SimpleVLA-RL [17] scales during training—rather than at test time—using reinforcement learning with outcome rewards. MG-Select [10] estimates confidence via KL divergence between predicted and reference action distributions and selects the best action among samples without an external verifier. 

Our PDF instead improves confidence by mitigating the spurious correlation through data augmentation and refining the policy with delayed feedback, yielding a robust TTA 

scheme for VLAs. 

## **3. Methods** 

In this section, we present Perturbation learning with Delayed Feedback (PDF), a plug-and-play TTA strategy designed for VLAs. Figure 3 depicts the overall architecture of our proposed PDF. The following subsections elaborate on each core component. 

### **3.1. Prelimiaries** 

We begin by formulating the VLAs problem as a Markov = Decision Process (MDP), defined by the tuple _M_ ( _S, A, P, R_ ), where _S ⊆_ R<sup>_n_</sup> and _A ⊆_ R<sup>_m_</sup> denote continuous state and action spaces, respectively. At each time step _t_ , the agent observes a multimodal state _st_ = ( _ot, ct_ ) _∈S_ , consisting of a pixel observation _ot ∈O_ and a textual instruction _ct ∈C_ . Given the current state _st_ , the agent selects an action _at ∈A_ , causing the environment to transition to a new state _st_ +1 _∼ P_ ( _· | st, at_ ). Upon task completion, the agent receives delayed feedback signals _ri ∈R, i ∈_ [1 _, T_ ], which encapsulate task completion status or reward information. 

### **3.2. Uncertainty-Based Action Voting** 

To improve the robustness of VLAs during test time, when VLAs interact with environments, the uncertainty of the model’s decision is quantified using uncertainty estimation. Based on the estimated uncertainty, adaptive data augmen- 

8112 

tation is applied to mitigate overfitting and attention imbalance, thereby improving the reliability of action generation while preserving inference efficiency. 

Specifically, given a state _st_ = ( _ot, ct_ ), the pixel observation _ot_ is encoded by a visual encoder into pixel embeddings _eot_ , while the textual instruction _ct_ is tokenized and embedded into text embeddings _ect_ . Then, both embeddings are concatenated and projected into features _ft_ . At last, the features are processed by an MLP _hϕ_ ( _·_ ), referred to as the Large Model head (LM head), to generate the logits _zt_ for each token. 

To evaluate the uncertainty of the model’s decision under the current state, we estimate predictive uncertainty from the output logits, defined as the normalized Shannon entropy of the predicted action distribution: 


where _K_ denotes the number of possible action tokens and _p_ ( _at_ = _ak | st_ ) = softmax( _zt_ ) _k_ . 

In sequential decision-making tasks, a single erroneous action can result in complete task failure, with highuncertainty actions being particularly prone to causing such outcomes. To mitigate action-generation uncertainty, we employ a simple yet effective strategy—data augmentation. However, data augmentation introduces significant computational overhead and therefore should be applied selectively. Therefore, augmented observations are generated by applying a set of transformations _T_ = _{T_ 1 _, . . . , TN }_ , where the augmentation budget is adaptively determined by the model’s uncertainty: 


where _N_ max denotes the maximum augmentation budget. Both the original observation _ot_ and its augmented views _{Tj_ ( _ot_ ) _}_<sup>_N_</sup> _j_ =1<sup>_t_are then divided into patches and encoded into</sup> pixel embeddings. The resulting pixel embeddings are concatenated with text embeddings to form a unified multimodal sequence and processed by the causal transformer to produce features _ft_ . 

Finally, these features are projected by two parallel heads, the LM head _hϕ_ ( _·_ ) and the Perturbation head (P head) _hθ_ ( _·_ ): 


where _hϕ_ ( _·_ ) generates the decision logits, _hθ_ ( _·_ ) outputs the learnable perturbations and _λ_ is a hyper-parameter. The resulting final logits _z_ ˜ _t_ are detokenized into a set of candidate actions, from which the final action _at_ is then selected through majority voting. The features of both the original and augmented observations are stored in a rollout buffer _D_ for optimization once feedback is available. 

It is important to note that all parameters of the VLAincluding the visual encoder, token embedding layers, causal transformer, LM head and P head-remain frozen throughout this process. 

### **3.3. Delayed Feedback-Guided Adaptation** 

Upon an episode completion, the agent receives delayed feedback _r ∈R_ , which reflects overall task performance, such as task success, failure, or cumulative reward. A batch of features _fb_ is then sampled from the rollout buffer _D_ , and the final logits _z_ ˜ _b_ with gradients are computed as 


Then, the policy ˜ _πb_ is generated by applying the softmax function to the final logits _z_ ˜ _b_ . And the P head is subsequently optimized by 

_L_ PDF = _−_ ( _r − b_ ) log _πϕ_ + _λ_ KLI[ _r > b_ ] KL( _πϕ ∥ π_ ˜) _,_ (5) 

where the first term is a REINFORCE-style objective increasing the likelihood of actions from the perturbed policy _π_ ˜( _st_ ) when feedback _r_ exceeds the baseline _b_ . A KL regularizer is gated by I[ _r > b_ ], applied only under positive feedback to stabilize updates and accelerate convergence while allowing flexible exploration when _r ≤ b_ . Perturbations are thus steered toward successful action directions and discouraged otherwise. Only the P head _hθ_ is updated; all other VLA parameters remain frozen for efficient, stable test-time adaptation. 

## **4. Experiments** 

To evaluate the effectiveness of the proposed PDF, we conduct experiments across diverse decision-making simulation environments. Specifically, we employ OpenVLA [11], a VLA fine-tuned on the LIBERO [20] benchmark and Jat [7]—an open-source implementation of GATO [24]—for the Atari suite [1]. This combination of environments and baselines enables a comprehensive evaluation of the superiority of our method across diverse task domains. 

### **4.1. Experimental Setup** 

LIBERO [20]: We use four 10-task suites (Spatial, Object, Goal, Long) in the LIBERO Franka Panda simulation with RGB views, robot states, task text, and delta end-effector actions. Each task: 50 eval rollouts; metric is success rate. Policies are trained for 50 episodes with OpenVLA [11] before evaluation. 

Atari [1]: We evaluate all 57 Atari 2600 games (pixel input, 4–18 discrete actions). Episodes end on life loss, level completion, or at 108,000 frames. Each game: 50 eval episodes; metric is Human-Normalized Score = ( _HNS_ (Score _−_ RandomScore) _/_ (HumanScore _−_ RandomScore)). Base model Jat [7] is trained 50 episodes 

8113 

Table 1. Performance comparison on the LIBERO benchmark (Spatial, Object, Goal, Long). _†_ denotes reproduced results and SR indicates Success Rate (%). Blue numbers indicate SOTA within each task suite. 

|**Method**|**Pub.**|**Param.**|**Sp**|**atial**|**O**|**bject**|**G**|**oal**|**L**|**ong**|**A**|**vg.**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||SR_↑_|Rank_↓_|SR_↑_|Rank_↓_|SR_↑_|Rank_↓_|SR_↑_|Rank_↓_|SR_↑_|Rank_↓_|
|PackNet [21]|CVPR’18|-|0.63|11|0.60|10|0.75|8|0.25|12|0.56|10.2|
|ER [3]|Arxiv’19|-|0.56|12|0.44|12|0.49|11|0.32|11|0.45|11.5|
|SeqL [20]|NeurIPS’23|-|0.20|13|0.26|13|0.22|12|0.15|13|0.21|12.8|
|MTL [20]|NeurIPS’23|-|0.83|6|0.54|11|0.80|3|0.48|9|0.66|7.2|
|ATM [28]|RSS’23|-|0.69|10|0.68|8|0.78|5|0.39|10|0.63|10.5|
|OpenVLA [11]<br>|CoRL’24|-|0.79|8|0.86|4|0.85|2|0.51|7|0.75|5.2|
|OpenVLA<sup>_†_ </sup>[11]|CoRL’24|-|0.85|2|0.64|9|0.76|6|0.53|6|0.69|5.8|
|DP [5]|IJRR’25|-|0.78|9|**0.92**|**1**|0.68|10|0.51|8|0.72|7|
|OCTO [8]|RSS’24|93M|0.79|8|0.86|4|0.85|2|0.51|7|0.75|5.3|
|TraceVLA [32]|ICLR’25|130M|0.85|4|0.85|5|0.75|7|0.54|4|0.75|6.5|
|OpenVLA-DPO [4]|Arxiv’25|130M|0.84|5|0.89|2|0.79|4|0.53|5|0.76|4|
|SFT-4LIBERO [16]|Arxiv’25|130M|0.85|3|0.87|3|0.77|5|0.55|3|0.76|3.5|
|MG-Select [10]|Arxiv’25|130M|0.82|7|0.73|6|0.73|9|0.55|2|0.71|6|
|**PDF (Ours)**|-|9M|**0.90**|**1**|0.72|7|**0.86**|**1**|**0.59**|**1**|**0.77**|**2.5**|
|1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>−10<br>0<br>10<br>20<br>30<br>40<br>50<br>60<br>HNS Change<br>60.2<br>53.0<br>~~48.8~~<br>44.9 43.7<br>39.1<br>34.5<br>31.7<br>2|9<br>10<br>11<br>12<br>13<br>14<br>2.6<br>20.9<br>~~18.1~~<br>16.1 15.7 14.5|15<br>16<br>17<br>18<br>19<br>14.4 14.2<br>11.8 11.6<br>9.|20<br>21<br>22<br>3<br>~~9.0~~<br>~~9.0~~<br>~~8.8~~|23<br>24<br>25<br>26<br>2<br>~~8.7~~<br>~~8.0~~<br>7.0<br>6.7<br>5|7<br>28<br>29<br>30<br>Game Inde<br>.8<br>4.9<br>4.4<br>4.2|31<br>32<br>33<br>34<br>x<br>3.4<br>2.8<br>2.8<br>2.6|35<br>36<br>37<br>3<br>2.0<br>1.7<br>1.2<br>0|8<br>39<br>40<br>41<br>4<br>.5<br>0.3<br>0.3<br>0.3<br>0.|2<br>43<br>44<br>45<br>1<br>0.1<br>0.0<br>0.0<br>|46<br>47<br>48<br>49<br>-0.0 -0.0 -0.3 -0.6|50<br>51<br>52<br>53<br>-0.8 -1.9 -2.0 -2.|54<br>55<br>56<br>57<br>2 -2.5 -3.8 -4.4<br>-10.7|


Figure 4. Human normalized score changes across 57 Atari games. Blue bars show performance improvements, orange bars indicate degradation. Games are sorted by improvement magnitude, with BOXING (+60.25%) showing maximum gain and BATTLE ZONE (- 10.72%) showing maximum decline. 47/57 games demonstrate positive performance changes, with 11.28% mean improvement. 

per game. All LIBERO and Atari experiments run on a single Tesla V100-PCIE-32GB. 

### **4.2. Performance Comparison Across Benchmarks** 

To demonstrate the effectiveness of PDF, we conduct extensive experiments across multiple benchmarks. 

Table 1 summarizes results on four LIBERO suites. PDF attains the best average performance (0.77 SR, 2.5 mean rank), exceeding prior VLA variants and adaptation baselines. It reaches 0.89 on Spatial (vs. 0.85 for reproduced OpenVLA) and 0.86 on Goal, slightly ahead of OCTO and 

OpenVLA. Gains are largest on Long-horizon tasks (0.59, +4.1 over the best baseline), indicating stronger sequential decision quality. Compared to MG-Select, PDF improves average SR by nearly 6 points, showing the advantage of uncertainty-weighted action voting and delayed-feedback perturbation learning over sample filtering. PDF also matches or surpasses strong pretrained models (TraceVLA, SFT-4LIBERO) without any fine-tuning. These results underscore PDF’s effectiveness in mitigating trajectory overfitting and boosting robustness in spatially complex, longhorizon settings. 

8114 

PDF is also evaluated on Atari-57, attaining 1.07 HNS vs. 0.97 for the Jat base (+0.10). Figure 4 shows pergame HNS deltas: 47/57 games improve. Largest gains appear in BOXING (+0.60), TIME PILOT (+0.53), ATLANTIS (+0.49), and ASSAULT (+0.45). Our method uses 9M trainable parameters and requires no gradient access to the base model, whereas baselines use 93–130M parameters and require base-model gradients. 

### **4.3. Impact of Data Augmentation and Feedbacks** 

To evaluate the impact of the data augmentation (DA) mechanism and perturbation learning with delayed feedback (DF), we conduct extensive experiments on the four LIBERO suites. Note that “PDF w/o DF” denotes OpenVLA that selects actions solely via multi-view voting (without delayed feedback), and “PDF w/o DA” denotes OpenVLA that learns perturbations using only the original pixel observations (without data augmentation). Table 2 presents an ablation comparing the baseline OpenVLA with variants of the proposed PDF across the LIBERO suites. Results show that integrating both DF and DA in PDF is effective. Overall, PDF attains the highest average success rates across all four suites. This superiority holds for most tasks within each suite, as indicated by boldface entries in the table. 

Moreover, the ablation reveals the contribution of each component. The PDF w/o DA variant surpasses the OpenVLA baseline on most tasks. By contrast, the PDF w/o DF variant shows a substantial drop across suites, with success rates dropping to 0.50 on Object and 0.77 on Goal. These results suggest that DF is critical for robustness, particularly in object-manipulation and goal-conditioned tasks. The synergy between DF and DA is evident. The full PDF model outperforms both variants and yields more stable results across suites, confirming that both DF and DA are integral to the observed performance gains. 


Figure 5. Performance degradation under increasing data augmentation budgets. All five benchmarks (LIBERO-Spatial, LIBEROObject, LIBERO-Goal, LIBERO-Long, and Atari) show performance decline as augmentation budget increases from 0 to 4, indicating that excessive data augmentation harms model effectiveness. 


Figure 6. Performance comparison across five benchmarks shows that both the KL divergence and the REINFORCE-style term contribute to the full PDF model’s superior performance. Removing either component results in degraded performance, with KL divergence showing greater impact on final results. 

### **4.4. Ablation Study on Data Augmentation Budget** 

Given that data augmentation (DA) is a crucial module in PDF and its budget affects performance, we evaluate its impact across the four LIBERO suites and the Atari benchmark. Figure 5 summarizes performance under five augmentation budgets (0-4, higher uncertainty indicates more data augmentations) for the LIBERO and Atari benchmarks. As the test-time augmentation budget (i.e., the number of augmented views sampled for voting) increases, performance generally declines across benchmarks. Increasing the data augmentation budget in PDF generally degrades performance across LIBERO and Atari benchmarks due to noise accumulation, with a small budget (max of 3) offering the best trade-off to mitigate trajectory overfitting without introducing low-quality views. Adaptive, benchmark-specific budget ceilings are recommended 

for optimal results in structure-dependent tasks. Overall, we set the max data augmentation budget to 3, because moderate augmentation is benign, whereas aggressive budgets degrade structure-dependent tasks; adaptive, benchmark-specific ceilings are preferable to uniform maximization. 

### **4.5. Ablation Study on Loss Functions** 

The PDF objective comprises two components: a REINFORCE-style policy gradient term and a KL regularization term. To evaluate the contribution of each term, we conduct experiments on the four LIBERO suites and the Atari benchmark. Figure 6 compares: (i) the base model OpenVLA, (ii) a variant without the KL term (w/o KL), (iii) a variant without the REINFORCE-style term 

8115 

Table 2. Performance comparison of OpenVLA and PDF variants (with and without Delayed Feedback (DF) and Data Augmentation (DA)) across LIBERO benchmark suites (Spatial, Object, Goal, and Long). Reported as success rates over 10 tasks with average performance. 

|**Suite**|**Method**|0|1|2|3|4|5|6|7|8|9|**Avg.**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||OpenVLA|0.94|0.94|0.86|0.96|0.64|0.88|0.92|0.86|0.74|0.76|0.85|
|**ial**|PDF w/o DF|0.78|0.84|0.90|0.90|0.78|0.68|0.92|0.70|0.80|0.74|0.80|
|**pat**|PDF w/o DA|0.94|0.94|0.88|0.94|0.68|0.88|0.92|0.88|0.76|0.76|0.86|
|**S**|PDF|0.94|0.96|0.98|0.98|0.80|0.88|0.92|0.88|0.80|0.80|0.89|
||∆_↑_|0.00|0.02|0.12|0.02|0.16|0.00|0.00|0.02|0.06|0.04|0.04|
||OpenVLA|0.64|0.68|0.78|0.34|0.90|0.66|0.50|0.62|0.36|0.74|0.62|
|**ect**|PDF w/o DF|0.86|0.50|0.74|0.62|0.68|0.16|0.10|0.28|0.36|0.74|0.50|
|**bj**|PDF w/o DA|0.88|0.68|0.82|0.40|0.94|0.70|0.48|0.66|0.36|0.76|0.67|
|**O**|PDF|0.96|0.74|0.82|0.66|0.96|0.66|0.56|0.66|0.40|0.80|0.72|
||∆_↑_|0.32|0.06|0.04|0.32|0.06|0.00|0.06|0.04|0.04|0.06|0.10|
||OpenVLA|0.62|0.90|0.84|0.66|0.94|0.90|0.78|1.00|0.86|0.68|0.81|
|**al**|PDF w/o DF|0.70|0.96|0.88|0.34|0.94|0.78|0.82|0.98|0.68|0.62|0.77|
|**Go**|PDF w/o DA|0.62|0.94|0.86|0.60|0.92|0.94|0.80|1.00|0.76|0.66|0.81|
||PDF|0.72|0.98|0.90|0.66|0.96|0.96|0.86|1.00|0.82|0.70|0.85|
||∆_↑_|0.10|0.08|0.06|0.00|0.02|0.06|0.08|0.00|-0.04|0.02|0.04|
||OpenVLA|0.62|0.64|0.58|0.50|0.44|0.86|0.50|0.66|0.20|0.58|0.56|
|**ng**|PDF w/o DF|0.70|0.64|0.58|0.54|0.52|0.82|0.48|0.62|0.20|0.52|0.56|
|**Lo**|PDF w/o DA|0.72|0.60|0.58|0.50|0.46|0.88|0.50|0.66|0.20|0.56|0.57|
||PDF|0.72|0.64|0.58|0.56|0.56|0.88|0.50|0.68|0.20|0.58|0.59|
||∆_↑_|0.10|0.00|0.00|0.06|0.12|0.02|0.00|0.02|0.00|0.00|0.03|


Table 3. Performance comparison of dim-wise voting and actionwise voting across Atari and LIBERO tasks. 

|**Task**|**Dim-wise**|**Action-wise**|
|---|---|---|
|Alien|**0.26**|-|
|Black Bowl|0.68|**0.88**|
|Alphabet Soup|**0.86**|0.64|
|Bowl on Stove|**0.96**|0.90|
|Moka Pot|**0.58**|**0.58**|


(w/o RE), and (iv) the full PDF objective. The full objective yields the highest scores; the largest absolute/relative gains occur on Atari (+0.1) and LIBERO-Object (+0.1). Removing the KL term markedly boosts Atari (+0.07) but yields only modest gains on other suites; removing the REINFORCE-style term slightly harms Atari (-0.01) yet improves LIBERO-Object (+0.07) and shows smaller positive shifts elsewhere. Moderate improvements are observed on LIBERO-Spatial (+0.04) and LIBERO-Goal (+0.04), while LIBERO-Long shows a smaller gain (+0.03). These patterns suggest KL term and the REINFORCE-style term provide complementary benefits—stability and calibrated exploration vs. reward-aligned action refinement—whose combination yields additive, non-redundant gains. 

### **4.6. Comparison between Voting Mechanisms** 

To evaluate voting strategies, we compare three variants. Dimension-wise voting takes a majority vote per action dimension, while action-wise voting votes over full action tuples. As shown in Table 3, on Atari (Alien) the action is effectively one-dimensional, making dimension-wise and action-wise voting equivalent. On LIBERO, dimensionwise voting best mitigates trajectory overfitting by allowing cross-view agreement on individual action components, enabling more flexible deviations from the original policy. Action-wise voting often falls back to the baseline because views rarely agree on the entire action tuple, yielding mixed results. Overall, dimension-wise voting provides the most reliable robustness–plasticity trade-off. 

### **4.7. Visualization and Case Study** 

To further assess the effectiveness of PDF, we conduct qualitative case studies on three LIBERO tasks: (i) “pick up the cream cheese and place it in the basket” ( _Pick up cream cheese_ ), (ii) “pick up the black bowl on the wooden cabinet and place it on the plate” ( _Pick up black bowl_ ), and (iii) “put both the alphabet soup and the tomato sauce in the basket” ( _Put alphabet soup_ ). As shown in Figure 7(a,b), OpenVLA exhibits trajectory overfitting: it executes a demonstrationlike motion plan but disregards whether the target object 

8116 


Figure 7. Visual comparison of OpenVLA and PDF on three tasks. The green thumb indicates that the agent performed the correct action, while the red thumb indicates an incorrect action. The box represents the target entity, with green indicating that the target entity has been operated correctly and red indicating incorrect operation. 

has been successfully grasped, leading to failure to complete the tasks. In contrast, PDF manifests a more robust, state-aware policy under the same conditions and reliably completes both _Pick up cream cheese_ and _Pick up black bowl_ . Interestingly, on _Put alphabet soup_ (Figure 7(c)), PDF initially fails to secure the alphabet soup but promptly reattempts and succeeds, indicating decision-making rather than open-loop replay. Overall, these case studies highlight PDF’s resilience to demonstration bias and its capacity to leverage feedback for corrective actions, resulting in higher task completion reliability. 

## **5. Conclusions and Limitations** 

We introduce PDF, a verifier-free TTA method that improves VLA decision performance in sequential decision making.VLAs suffer from trajectory overfitting—overweighting the spurious correlation and replaying memorized action chains—reducing reliability under 

subtle environmental shifts. PDF addresses this via (i) uncertainty-based action voting and (ii) delayedfeedback–guided adaptation. On LIBERO robotic manipulation and Atari-57, PDF surpasses vanilla VLAs and VLAs with TTA baselines, improving decision performance with minimal overhead. However, PDF does not fully solve trajectory overfitting; rather, it alleviates its negative impact. In future work, we will address the challenge more fundamentally. 

## **Acknowlegedements** 

This work was a research achievement of National Engineering Research Center of New Electronic Publishing Technologies, and was supported by the National Natural Science Foundation of China (62406313, 62376011), the Postdoctoral Fellowship Program of China Postdoctoral Science Foundation, Grant No. YJB20250283, and the National Key R&D Program of China (2024YFA1410000). 

8117 

## **References** 

- [1] Marc G. Bellemare, Yavar Naddaf, Joel Veness, and Michael Bowling. The arcade learning environment: An evaluation platform for general agents. _J. Artif. Intell. Res._ , 47:253– 279, 2013. 

- [2] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control. _CoRR_ , abs/2410.24164, 2024. 

- [3] Arslan Chaudhry, Marcus Rohrbach, Mohamed Elhoseiny, Thalaiyasingam Ajanthan, Puneet K. Dokania, Philip H. S. Torr, and Marc’Aurelio Ranzato. On tiny episodic memories in continual learning, 2019. 

- [4] Zengjue Chen, Runliang Niu, He Kong, and Qi Wang. TGRPO :fine-tuning vision-language-action model via trajectory-wise group relative policy optimization. _CoRR_ , abs/2506.08440, 2025. 

- [5] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _Int. J. Robotics Res._ , 44(10-11):1684–1704, 2025. 

- [6] Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, et al. Libero-plus: In-depth robustness analysis of visionlanguage-action models. _arXiv preprint arXiv:2510.13626_ , 2025. 

- [7] Quentin Gallou´edec, Edward Beeching, Cl´ement Romac, and Emmanuel Dellandr´ea. Jack of all trades, master of some, a multi-purpose transformer agent. _CoRR_ , abs/2402.09844, 2024. 

- [8] Dibya Ghosh, Homer Rich Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, You Liang Tan, Lawrence Yunliang Chen, Quan Vuong, Ted Xiao, Pannag R. Sanketi, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In _Robotics: Science and Systems XX, Delft, The Netherlands, July 15-19, 2024_ , 2024. 

- [9] Jiangyong Huang, Silong Yong, Xiaojian Ma, Xiongkun Linghu, Puhao Li, Yan Wang, Qing Li, Song-Chun Zhu, Baoxiong Jia, and Siyuan Huang. An embodied generalist agent in 3d world. In _Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024_ . OpenReview.net, 2024. 

- [10] Suhyeok Jang, Dongyoung Kim, Changyeon Kim, Youngsuk Kim, and Jinwoo Shin. Verifier-free test-time sampling for vision language action models. _CoRR_ , abs/2510.05681, 2025. 

- [11] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Paul Foster, Pannag R. Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An 

open-source vision-language-action model. In _Conference on Robot Learning, 6-9 November 2024, Munich, Germany_ , pages 2679–2713. PMLR, 2024. 

- [12] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _CoRR_ , abs/2502.19645, 2025. 

- [13] Sungjune Kim, Gyeongrok Oh, Heeju Ko, Daehyun Ji, Dongwook Lee, Byung-Jun Lee, Sujin Jang, and Sangpil Kim. Test-time adaptation for online vision-language navigation with feedback-based reinforcement learning. In _Forty-second International Conference on Machine Learning_ , 2025. 

- [14] Jacky Kwok, Christopher Agia, Rohan Sinha, Matthew Foutter, Shulu Li, Ion Stoica, Azalia Mirhoseini, and Marco Pavone. Robomonkey: Scaling test-time sampling and verification for vision-language-action models. _CoRR_ , abs/2506.17811, 2025. 

- [15] Taeckyung Lee, Sorn Chottananurak, Junsu Kim, Jinwoo Shin, Taesik Gong, and Sung-Ju Lee. Test-time adaptation with binary feedback. _CoRR_ , abs/2505.18514, 2025. 

- [16] Chen Li, Zhantao Yang, Han Zhang, Fangyi Chen, Chenchen Zhu, Anudeepsekhar Bolimera, and Marios Savvides. Metavla: Unified meta co-training for efficient embodied adaption. _CoRR_ , abs/2510.05580, 2025. 

- [17] Haozhan Li, Yuxin Zuo, Jiale Yu, Yuhao Zhang, Zhaohui Yang, Kaiyan Zhang, Xuekai Zhu, Yuchen Zhang, Tianxing Chen, Ganqu Cui, Dehui Wang, Dingxiang Luo, Yuchen Fan, Youbang Sun, Jia Zeng, Jiangmiao Pang, Shanghang Zhang, Yu Wang, Yao Mu, Bowen Zhou, and Ning Ding. Simplevlarl: Scaling VLA training via reinforcement learning. _CoRR_ , abs/2509.09674, 2025. 

- [18] Muyao Li, Zihao Wang, Kaichen He, Xiaojian Ma, and Yitao Liang. JARVIS-VLA: post-training large-scale vision language models to play visual games with keyboards and mouse. In _Findings of the Association for Computational Linguistics, ACL 2025, Vienna, Austria, July 27 - August 1, 2025_ , pages 17878–17899. Association for Computational Linguistics, 2025. 

- [19] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, Hang Li, and Tao Kong. Vision-language foundation models as effective robot imitators. In _The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024_ . OpenReview.net, 2024. 

- [20] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. LIBERO: benchmarking knowledge transfer for lifelong robot learning. In _Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023_ , 2023. 

- [21] Arun Mallya and Svetlana Lazebnik. Packnet: Adding multiple tasks to a single network by iterative pruning. In _2018 IEEE Conference on Computer Vision and Pattern Recognition, CVPR 2018, Salt Lake City, UT, USA, June 1822, 2018_ , pages 7765–7773. Computer Vision Foundation / IEEE Computer Society, 2018. 

8118 

- [22] Mitsuhiko Nakamoto, Oier Mees, Aviral Kumar, and Sergey Levine. Steering your generalists: Improving robotic foundation models via value guidance. In _Conference on Robot Learning, 6-9 November 2024, Munich, Germany_ , pages 4996–5013. PMLR, 2024. 

- [23] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, and Xuelong Li. Spatialvla: Exploring spatial representations for visual-language-action model. _CoRR_ , abs/2501.15830, 2025. 

- [24] Scott E. Reed, Konrad Zolna, Emilio Parisotto, Sergio G´omez Colmenarejo, Alexander Novikov, Gabriel BarthMaron, Mai Gimenez, Yury Sulsky, Jackie Kay, Jost Tobias Springenberg, Tom Eccles, Jake Bruce, Ali Razavi, Ashley Edwards, Nicolas Heess, Yutian Chen, Raia Hadsell, Oriol Vinyals, Mahyar Bordbar, and Nando de Freitas. A generalist agent. _Trans. Mach. Learn. Res._ , 2022, 2022. 

- [25] A Sohn, A Nagabandi, C Florensa, D Adelberg, D Wu, H Farooq, I Clavera, J Welborn, J Chen, N Mishra, et al. Introducing rfm-1: Giving robots human-like reason-ing capabilities, 2024. 

- [26] Waywe Research Team et al. Lingo-2: Driving with natural language, 2024. 

- [27] Dequan Wang, Evan Shelhamer, Shaoteng Liu, Bruno A. Olshausen, and Trevor Darrell. Tent: Fully test-time adaptation by entropy minimization. In _9th International Conference on Learning Representations, ICLR 2021, Virtual Event, Austria, May 3-7, 2021_ . OpenReview.net, 2021. 

_The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025_ . OpenReview.net, 2025. 

   - [33] Jiahuan Zhou, Chao Zhu, Zhenyu Cui, Zichen Liu, Xu Zou, and Gang Hua. Class-aware domain knowledge fusion and fission for continual test-time adaptation. _CoRR_ , abs/2510.12150, 2025. 

   - [34] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, Quan Vuong, Vincent Vanhoucke, Huong T. Tran, Radu Soricut, Anikait Singh, Jaspiar Singh, Pierre Sermanet, Pannag R. Sanketi, Grecia Salazar, Michael S. Ryoo, Krista Reymann, Kanishka Rao, Karl Pertsch, Igor Mordatch, Henryk Michalewski, Yao Lu, Sergey Levine, Lisa Lee, Tsang-Wei Edward Lee, Isabel Leal, Yuheng Kuang, Dmitry Kalashnikov, Ryan Julian, Nikhil J. Joshi, Alex Irpan, Brian Ichter, Jasmine Hsu, Alexander Herzog, Karol Hausman, Keerthana Gopalakrishnan, Chuyuan Fu, Pete Florence, Chelsea Finn, Kumar Avinava Dubey, Danny Driess, Tianli Ding, Krzysztof Marcin Choromanski, Xi Chen, Yevgen Chebotar, Justice Carbajal, Noah Brown, Anthony Brohan, Montserrat Gonzalez Arenas, and Kehang Han. RT-2: vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning, CoRL 2023, 6-9 November 2023, Atlanta, GA, USA_ , pages 2165–2183. PMLR, 2023. 

- [28] Chuan Wen, Xingyu Lin, John Ian Reyes So, Kai Chen, Qi Dou, Yang Gao, and Pieter Abbeel. Any-point trajectory modeling for policy learning. In _Robotics: Science and Systems XX, Delft, The Netherlands, July 15-19, 2024_ , 2024. 

- [29] Chenyu Zhang, Kunlun Xu, Zichen Liu, Yuxin Peng, and Jiahuan Zhou. SCAP: transductive test-time adaptation via supportive clique-based attribute prompting. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2025, Nashville, TN, USA, June 11-15, 2025_ , pages 30032–30041. Computer Vision Foundation / IEEE, 2025. 

- [30] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, Ankur Handa, Tsung-Yi Lin, Gordon Wetzstein, Ming-Yu Liu, and Donglai Xiang. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2025, Nashville, TN, USA, June 1115, 2025_ , pages 1702–1713. Computer Vision Foundation / IEEE, 2025. 

- [31] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3dvla: A 3d vision-language-action generative world model. In _Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024_ . OpenReview.net, 2024. 

- [32] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daum´e III, Andrey Kolobov, Furong Huang, and Jianwei Yang. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. In 

8119 

