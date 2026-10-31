---
title: "Pretrained Vision-Language-Action Models are Surprisingly Resistant to Forgetting in Continual Learning"
date: "2026-03-04"
authors: "Huihan Liu; Changyeon Kim; Bo Liu; Minghuan Liu; Yuke Zhu"
venue: "ICML 2026"
url: https://arxiv.org/abs/2603.03818
pdf: https://arxiv.org/pdf/2603.03818
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.03818)** / [論文ページ](https://arxiv.org/abs/2603.03818)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Pretrained Vision-Language-Action Models are Surprisingly Resistant to Forgetting in Continual Learning** 

### **Huihan Liu**<sup>1</sup> **Changyeon Kim**<sup>1 2</sup> **Bo Liu**<sup>3</sup> **Minghuan Liu**<sup>1</sup> **Yuke Zhu**<sup>1</sup> 


_Figure 1._ **Comparison of continual learning performance between a pretrained Vision-Language-Action (VLA) model (GR00T N1.5; NVIDIA et al. (2025)) and a non-pretrained small policy model (BC-Transformer; Liu et al. (2023b)).** Each checkpoint corresponds to a model obtained by sequentially training over ten tasks under Experience Replay (ER), where the parameters at the start of training for checkpoint _i_ are initialized from checkpoint _i−_ 1. Each matrix entry ( _i, j_ ) denotes the success rate on Task _j_ after training on Task _i_ . The columns track how a given task performance evolves as training continues (top to bottom). We compare a pretrained VLA model (top) with a non-pretrained small BC policy (bottom) across multiple LIBERO benchmark suites. 

## **Abstract** 

Continual learning is a long-standing challenge in robot policy learning, where a policy must acquire new skills over time without catastrophically forgetting previously learned ones. While prior work has extensively studied continual learning in relatively small behavior cloning (BC) policy models trained from scratch, its behavior in modern large-scale pretrained Vision-LanguageAction (VLA) models remains underexplored. In this work, we found that pretrained VLAs are re- 

> 1The University of Texas at Austin 2KAIST 3Microsoft Superintelligence. Correspondence to: Huihan Liu _<_ huihanl@utexas.edu _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 

markably resistant to forgetting compared with smaller policy models trained from scratch. Simple Experience Replay (ER) works surprisingly well on VLAs, sometimes achieving zero forgetting even with a small replay data size. Our analysis reveals that pretraining plays a critical role in downstream continual learning performance: large pretrained models mitigate forgetting with a small replay buffer size while maintaining strong forward learning capabilities. Furthermore, we found that VLAs can retain relevant knowledge from prior tasks despite performance degradation during learning new tasks. This knowledge retention enables rapid recovery of seemingly forgotten skills through finetuning. Together, these insights imply that large-scale pretraining fundamentally changes the dynamics of continual learning, enabling models to continually acquire new skills 

1 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 

over time with simple replay. Code and more information can be found at project website. 

## **1. Introduction** 

Continual learning (French, 1999a; McCloskey & Cohen, 1989a; Liu et al., 2023b) remains a long-standing challenge in robot policy learning, which requires robot policies to acquire new skills over time while preserving previously learned behaviors. In contrast to learning multi-task policies at once (Levine et al., 2016; Jang et al., 2022a; Brohan et al., 2023b;a), continual learning requires the policy to balance the ability of learning new tasks (plasticity) and preserving previously acquired knowledge (stability) (French, 1999a; McCloskey & Cohen, 1989a). The learning is non-trivial, as the policy tends to fail and result in catastrophic forgetting (French, 1999a; McCloskey & Cohen, 1989a; Kirkpatrick et al., 2017a; Luo et al., 2025), where the learning of new skills often leads to large degradation in previously learned behaviors, making naive sequential finetuning ineffective (Shenfeld et al., 2025). 

Prior work on continual learning in robotics has primarily focused on relatively small policy models trained from scratch or with limited pretraining (Liu et al., 2023b; Chaudhry et al., 2019; Kirkpatrick et al., 2017a; Mallya & Lazebnik, 2018; Wan et al., 2024). In these settings, catastrophic forgetting is often pervasive (Liu et al., 2023b), and people typically require the use of large replay buffers (Chaudhry et al., 2019) or carefully designed regularization techniques (Kirkpatrick et al., 2017a) for mitigation. Recently, large-scale pretrained Vision-Language-Action models (VLAs) have demonstrated strong generalization and downstream task transfer in robotic manipulation. Pretrained on diverse multimodal data (Radford et al., 2021; Touvron et al., 2023; OpenAI et al., 2024) and robot trajectories, these models rely less on task-specific parameter updates and instead adapt by reusing and reconfiguring existing representations. This raises a central question: do large pretrained VLAs behave differently in continual learning from the smaller models, and if so, in what ways? 

Our answer follows by observing that pretrained VLAs exhibit vastly different dynamics from smaller policy models in continual learning. In particular, we conduct a comprehensive empirical study that reveals a set of unexpected dynamics of VLAs in continual learning: 

**Pretrained VLAs are remarkably resistant to forgetting compared with smaller policy models trained from scratch (Sec. 3).** Specifically, we found that simple Experience Replay (ER) works surprisingly well on VLAs, often achieving **_zero_** forgetting even with a small replay data size ( _e.g._ , 2% of training data in LIBERO benchmark suites). Furthermore, sometimes it even enables **_positive backward_** 

**_transfer_** on previously learned tasks, _i.e._ , further improving the performance of previous tasks with only the replay data stored. These dynamics of learning have not been seen before on smaller models. 

**Pretraining plays an integral role in improving continual learning performance in both forward and backward transfer (Sec. 5).** We found that the pretrained knowledge in VLAs is especially effective for mitigating forgetting even at a small replay dataset size ( _e.g._ , 2% of training data). Furthermore, pretraining reduces forgetting while still maintaining a high success rate on new tasks, avoiding the trade-off between preserving knowledge and forward transfer ability. 

**VLAs preserve relevant knowledge of prior tasks despite performance degradation from learning new ones (Sec. 6).** Even when performance on previous tasks seems to degrade from catastrophic forgetting, the underlying knowledge is still preserved in the VLA’s internal representation. Evidence for this lies in the fact that a few finetuning steps can quickly restore performance on past tasks. 

## **2. Related Work** 

### **2.1. Continual Learning Beyond Training from Scratch** 

Catastrophic forgetting has long been a central challenge in continual learning, motivating a wide range of algorithmic solutions such as regularization, distillation, replay, and architectural isolation (McCloskey & Cohen, 1989b; French, 1999b; Kirkpatrick et al., 2017b; Li & Hoiem, 2016; LopezPaz & Ranzato, 2017; Rusu et al., 2016). Most prior work studies these mechanisms in relatively small models trained from scratch, revealing a fundamental stability-plasticity trade-off and a strong dependence on replay size and task order (Parisi et al., 2019; De Lange et al., 2022). 

More recently, continual learning has been revisited in the context of large pretrained models, particularly language models. Empirical studies show that pretrained representations can reduce—but not eliminate—forgetting under sequential finetuning, and that pretraining substantially alters transfer and interference patterns (Wu et al., 2022; Scialom et al., 2022). Complementary work on continual pretraining and temporal benchmarks further highlights the tension between knowledge retention and adaptation in large models (Jang et al., 2022b;c; Hu et al., 2023). These results suggest that conclusions drawn from training-from-scratch settings may not directly generalize to large pretrained models. 

### **2.2. VLAs and Lifelong Robot Learning** 

Vision-language-action models (VLAs) extend foundation model paradigms to robotics by jointly learning perception, language understanding, and control from large, het- 

2 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 

erogeneous data (Reed et al., 2022; Brohan et al., 2022; Zitkovich et al., 2023; Driess et al., 2023). Recent open efforts such as Open X-Embodiment, Octo, and OpenVLA demonstrate strong transfer across tasks and embodiments, making VLAs natural candidates for lifelong robot learning (Open X-Embodiment Collaboration et al., 2023; Octo Model Team et al., 2024; Kim et al., 2025). 

Continual learning in robotics has traditionally focused on smaller behavior cloning policies and task-specific settings (Lesort et al., 2020; Liu et al., 2023a). While iterative adaptation frameworks suggest that generalist policies can improve over time (Bousmalis et al., 2023; Yadav et al., 2026), the mechanisms by which large pretrained VLAs retain or recover previously learned skills under continual finetuning remain poorly understood. In particular, it is unclear whether classical replay-based conclusions—such as the need for large buffers or explicit regularization—still apply in the regime of large pretrained VLAs. 

**Positioning of this work.** In contrast to prior studies, we systematically investigate continual learning behavior in modern pretrained VLAs. We show that simple experience replay surprisingly achieves near-zero forgetting with surprisingly small buffers, and that large-scale pretraining fundamentally changes the stability–plasticity dynamics observed in smaller models trained from scratch. Our findings position pretrained VLAs as a distinct continual learning regime, where forgetting, transfer, and recovery are governed more by pretraining and representation reuse than by specialized continual learning algorithms. 

## **3. Preliminaries** 

### **3.1. Continual Learning in Robotics** 

We model a robotic task as a finite-horizon Markov Decision Process: _M_ = ( _S, A, T , H, µ_ 0), where _S_ and _A_ are the state and action space, _µ_ 0 is the initial state distribution, and _T_ : _S × A →S_ is the transition function. To check the success of the given task, we assume access to a goal predicate _g_ : _S →{_ 0 _,_ 1 _}_ . Under this formulation, continual learning, also known as lifelong learning (Liu et al., 2023b), considers a robot that sequentially learns _K_ tasks _{T_<sup>_k_</sup> _}_<sup>_K_</sup> _k_ =1 using a single task-conditioned policy _π_ ( _· | s, T_ ). Each task _T_<sup>_k_</sup> _≡_ ( _µ_<sup>_k_</sup> 0<sup>_, gk_)isspecifiedbyauniqueinitial-state</sup> distribution _µ_<sup>_k_</sup> 0<sup>and a goal predicate</sup><sup>_gk_, while sharing the</sup> same _S, A, T , H_ across tasks. 

In this work, we focus on continual learning via imitation learning. Formally, we assume access to expert demonstrations for each task _T_<sup>_k_</sup> , denoted by _D_<sup>_k_</sup> = _{τi_<sup>_k}N_</sup> _i_ =1<sup>, where</sup> each trajectory _τi_<sup>_k_=</sup><sup>_{_(</sup><sup>_o_0</sup><sup>_, a_0)</sup><sup>_, . . . ,_(</sup><sup>_ol_</sup> _k_<sup>_, al_</sup> _k_<sup>)</sup><sup>_}_consists of</sup> observations _ot_ (robot sensory inputs) and actions _at_ , terminating at _lk ≤ H_ . After observing tasks up to _T_<sup>_k_</sup> , our goal 

is to obtain a policy _π_ satisfying the following objective: 


where _L_ denotes the behavior cloning loss. We assume that demonstrations from previous tasks _{D_<sup>_p_</sup> : _p < k}_ are not fully available when learning _T_<sup>_k_</sup> . 

**Experience Replay (ER).** Experience Replay (Chaudhry et al., 2019) is a widely used approach in continual learning that retains a subset of samples from previous tasks and leverages them to learn new tasks. After completing policy learning for a task, ER stores a portion of that task’s data in a separate replay buffer. When training on a new task, ER draws samples from the buffer and combines them with the current task’s training data, so that the effective training distribution better approximates the empirical distribution over all tasks seen so far. 

### **3.2. Vision-Language-Action Models** 

Vision-Language-Action models (VLAs) are robotic policies that map visual observations and natural language instructions to actions, typically by building on top of large vision-language models (VLMs) pretrained on internet-scale image-text data. To adapt VLMs for robotic control, VLAs are commonly further trained via imitation learning on largescale robot demonstration datasets with diverse embodiments _D_ (Liu et al., 2025). Formally, a VLA defines a policy _π_ that, at each time step _t_ , predicts an action chunk **a** _t_ conditioned on a language instruction _l_ and a history of observations **o** _≤t_ of length _H_ . Each observation typically includes multi-view RGB images **I**<sup>1</sup> _t_<sup>_, . . . ,_</sup><sup>**I**</sup><sup>_n_</sup> _t_<sup>and the propri-</sup> oceptive state **q** _t_ . The VLA encodes these inputs with its VLM backbone to obtain a latent representation, which is then used by an action head to predict future actions. 

## **4. VLAs are Surprisingly Resistant to Forgetting** 

### **4.1. Evaluating VLAs in Continual Learning** 

To find out if VLAs behave differently in continual learning from the smaller models, we evaluated VLAs in a set of continual learning experiments. 

**Benchmarks and Datasets.** For our experiments, we employ LIBERO (Liu et al., 2023b), a lifelong learning benchmark for robotic manipulation. We use four different task suites (LIBERO-Spatial, LIBERO-10, LIBERO-Object, LIBERO-Goal) to validate the knowledge transfer across different properties. We use the same task ordering for all experiments. For the training dataset, we use the filtered dataset introduced by Kim et al. (2024). 

3 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 

_Table 1._ **Continual learning performance on LIBERO benchmarks** : Average Success Rate (SR _↑_ ) and Negative Backward Transfer (NBT _↓_ ). Results are with sample size = 1000 (20% of dataset size per task), in accordance with LIBERO’s official setting. BC-DP, BC-T, BC-ViT are abbreviations for BC-Diffusion Policy, BC-Transformer, BC-ViT respectively. 


_Figure 2._ **Negative Backward Transfer (NBT) across different replay buffer sizes.** Each subplot shows NBT as a function of replay buffer size ( _{_ 0 _._ 2% _,_ 2% _,_ 20% _}_ ) for all methods across the four benchmarks and their average. Shaded regions indicate _±_ 1 standard deviation across seeds. Higher NBT indicates more forgetting; values near zero indicate no forgetting. Results and discussion for LIBERO-10 are reported separately in Tab. 6 in Appendix A.2. 

**Models.** To verify that our hypothesis holds robustly across diverse VLA backbones, we consider Pi0 (Black et al., 2026) and GR00T N1.5 (NVIDIA et al., 2025) which differ in architecture, parameter count, and pretraining data. For the non-pretrained small policy, we adopt BC-Transformer (Liu et al., 2023a). 

**Training.** We train a separate model for each task suite. Within each suite, we train the model for a fixed number of optimization steps per stage while carrying over the model weights across tasks. For ER, at task _k_ , we train on the current task dataset, together with a fixed replay buffer containing _M_ randomly sampled transitions per task from previous tasks (reusing the same stored samples throughout). Unless otherwise specified, we use _M_ = 1000. 

**Evaluation.** We report two metrics: average task success rate (SR) (%), and negative backward transfer (NBT) based on success rate, following Liu et al. (2023a). Let _ci,k_ denote the success rate (%) on task _i_ when evaluated using the agent trained up to task _k_ . For each _k ∈_ [1 _,_ 2 _, · · · , K_ ], we evaluate _{ci,k}_<sup>_k_</sup> _i_ =1<sup>, yielding the collection</sup><sup>_{{ci,k}_</sup> _i_<sup>_k_</sup> =1<sup>_}K_</sup> _k_ =1<sup>.</sup> We compute NBT as follows: 


Intuitively, NBT measures how much past knowledge is 

**_lost_** after learning new tasks. A positive NBT indicates knowledge loss; the lower the value, the better. 

### **4.2. The Surprising Effectiveness of Experience Replay** 

As shown in Tab. 1, we observed that pretrained VLAs trained with experience replay (ER) surprisingly achieve **_near-zero, or even positive_** backward transfer across multiple LIBERO benchmarks, while simultaneously maintaining a strong forward transfer. The positive backward transfer observed in models like Pi0 and GR00T N1.5 indicates that for pretrained VLAs, learning new tasks can sometimes even improve the performance on previously learned ones, which challenges the prior understanding of the stabilityplasticity trade-off (McCloskey & Cohen, 1989a; French, 1999a). This behavior contrasts with smaller policy models, which typically suffer severe forgetting under comparable continual learning settings. Extended details of this experiment can be referred to in Appendix B.1. 

**There are consistent trends across different VLAs.** We observed similarly strong resistance to forgetting across multiple VLAs (Pi0, GR00T N1.5) despite differences in architecture, parameter count, and pretraining recipes. This consistency suggests that the effectiveness of ER is a general property of pretrained VLAs, rather than an artifact of any particular architecture design or pretraining dataset mixture. 

4 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 

_Table 2._ Comparison with non-ER continual learning baselines (Sequential, EWC) on LIBERO benchmarks. 

|||LIBERO|-Object|LIBE|RO-10|
|---|---|---|---|---|---|
|**Model**|**Method**|**SR (**_↑_**)**|**NBT (**_↓_**)**|**SR (**_↑_**)**|**NBT (**_↓_**)**|
||Sequential|0.910|0.696|0.644|0.562|
|Pi0|EWC|0.910|0.608|0.622|0.543|
||ER|0.898|**-0.007**|0.586|**-0.070**|
||Sequential|0.964|0.752|0.852|0.758|
|GR00T|EWC|0.826|0.766|0.816|0.728|
||ER|0.962|**0.004**|0.836|**0.082**|


**VLAs are resistant to forgetting, especially under a low replay data regime.** Fig. 2 shows a clear difference in how pretrained VLAs and non-pretrained baselines utilize replay data across different buffer sizes. When the buffer size is 2% (100 samples per task), pretrained VLAs such as Pi0 and GR00T still have low NBT around 0 _._ 1–0 _._ 2, while non-pretrained baselines (BC-Transformer, BC-ViT, and BC-Diffusion Policy) deteriorate to 0 _._ 4–0 _._ 5, retaining 2–4 _×_ more forgetting. The non-pretrained models require substantially more replay data ( _>_ 20%) to achieve comparable NBT. Note that under the smallest buffer size (0 _._ 2%), the gap appears less pronounced in absolute NBT; however, this is largely a limitation of the metric itself: at such a small buffer, all policies experience near-complete forgetting, and the absolute NBT is dominated by each policy’s initial success rate rather than its true resistance to forgetting. A normalized variant of NBT that accounts for this effect is discussed in Appendix A.2. 

**ER is uniquely effective.** To further validate the effectiveness, we compare ER against baselines that do not explicitly re-use past-task data and instead train using only the current task dataset. We consider two such variants: (i) Sequential (Liu et al., 2023b), which simply carries over the model weights across tasks and continues finetuning on the current task data without any replay buffer, and (ii) EWC (Kirkpatrick et al., 2017a), which likewise trains on the current task data but adds a regularization penalty to discourage changes to parameters important for earlier tasks. As shown in Tab. 2, neither baseline consistently improves over nonVLA policies in reducing forgetting, whereas ER remains robust for pretrained VLAs. These results indicate that explicitly revisiting past-task data during training (even if it’s a little) is crucial for preserving (and sometimes improving) prior task performance. 

**Real-Robot Experiments.** Our main experiments study continual learning in simulation (LIBERO). To test whether the observation generalizes to real robots, we run a smallscale experiment with the same protocol on the real-robot task suite from Mutex (Shah et al., 2023), which provides tabletop manipulation tasks with distinct object layouts and language goals in the home-kitchen workspace (Franka arm 

_Table 3._ **Continual learning on real robot** . Each lower-triangular entry ( _i, j_ ) is the success rate (%) on task _j_ after sequential training through task _i_ under experience replay with Pi0. 

||**Eva**|**luate on**|**task**|
|---|---|---|---|
|**After training on task**|_T_0|_T_1|_T_2|
|_T_0|44.4|—|—|
|_T_1|47.1|29.4|—|
|_T_2|44.4|28.6|33.3|


with multi-view RGB and proprioceptive inputs). We sequentially train Pi0 on three tasks with different visual layouts: (T0) Pick up bread and place it on the plate; (T1) Pick up the pink cup and place it on the plate; (T2) Pick up the red cup and place it in the back caddy. After each stage, we evaluate all tasks seen so far using the same success criteria as in simulation and report results in Tab. 3. The average SR = 35 _._ 4% and NBT = _−_ 0 _._ 003, indicating negligible backward transfer. The qualitative trend matches our simulation findings: pretrained Pi0 with simple ER can learn new skills without substantially erasing previously learned ones. 

Together, these results establish that VLAs are resistant to forgetting with ER, enabling strong forward transfer with little to no forgetting across architectures. Naturally, we wonder: what are the underlying dynamics behind this? 

## **5. Pretraining Plays an Integral Role in Improving Continual Learning Performance** 

In this section, we investigate a defining characteristic of VLAs—large-scale pretraining—and analyze how it interacts with experience replay across different replay sizes. Our analysis reveals that large-scale pretraining is a key factor affecting both forward and backward transfer behavior. Specifically, we find **_pretraining i) reduces forgetting especially in low-data regimes and ii) preserves knowledge of past tasks while still maintaining strong forward transfer_** , which will be elaborated below. 

**Methodology.** To isolate the role of pretraining, we conduct controlled comparisons of VLAs finetuned under the same architecture, differing only in the amount of pretraining during model initialization. In particular, we compare three variants: i) Pi0 from VL + Action, the Pi0 (Black et al., 2026) model pretrained on large-scale robot datasets on top of a VLM (PaliGemma; Beyer et al. (2024)) backbone; ii) Pi0 from VL, with Pi0 initialized from only PaliGemma VLM backbone without robot data pretraining; and iii) Pi0 from scratch, where the model uses Pi0 architecture but is trained entirely from scratch. For each variant, we run continual learning with experience replay and vary the replay buffer size to examine how continual learning behaviors 

5 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 


_Figure 3._ Comparison of forgetting performance across different buffer sizes (10 _,_ 100 _,_ 1000) for Pi0 pretrained, Pi0 initialized from Paligemma, and Pi0 trained from scratch. 


_Figure 4._ Pareto frontier of average NBT vs. replay buffer size. We compare the forgetting performance (lower is better) across different buffer sizes for Pi0 model with different levels of pretraining. We also provide BC-Transformer as a non-pretrained, smaller model reference. 

### change with different replay buffer sizes. 

**Pretrained knowledge is useful for mitigating forgetting, especially** **_under small replay buffer size_ .** Fig. 4 visualizes this effect through a Pareto frontier that characterizes the trade-off between forgetting (in terms of Negative Backward Transfer) and replay buffer size. Specifically, when the curve reaches 0 in the y-value, it means there is zero forgetting; when it reaches below 0, it means there is some positive transfer to past tasks (past tasks improve performance after training on later tasks). As the replay buffer size decreases, the gap between pretrained and non-pretrained models increases, indicating that at a smaller replay buffer size, pretraining plays an increasingly important role in mitigating forgetting. 

While the Pareto frontier provides a summary of forgetting as a function of replay size, scalar forgetting metrics alone 

can obscure important dynamics during continual learning. In particular, they do not capture how performance on individual tasks degrades or recovers as new tasks are learned. To make these dynamics explicit, we visualize how the success rate of each task _k_ ( _Tk_ ) changes after learning Task _k_ , _k_ + 1, _. . ._ , in Fig. 3. We show this for replay buffer size = 10 _,_ 100 _,_ 1000 respectively for LIBERO-Object. We found several interesting dynamics: 

- When the replay buffer size is relatively large (1000 samples, about 20% of the full dataset): in this data regime, there is little to no forgetting for all variants. However, the pretrained variants give a much higher success rate in learning new tasks and maintaining performance. 

- When the replay buffer is small with only 10 transitions (about 0 _._ 2% of full dataset): while all variants have forgetting, Pi0 from VL + Action displays less forgetting than the other two variants, and could still recover partial performance of some tasks ( _e.g._ , T2, T3, T4). 

The above observation implies an interesting fact: investigating forgetting itself can be limited, because a policy where task success rates are consistently low might give the same backward transfer with one where task success rates are consistently high. This brings us to the second observation: 

**Pretraining mitigates forgetting while still maintaining high forward transfer.** Tab. 4 shows that both Pi0 from VL + Action and Pi0 from VL achieve consistently higher success rate than the model trained from scratch (sample size = 1000). The result suggests that pretraining improves continual learning not only by reducing forgetting, but also by enabling forward learning, avoiding the degenerate outcome where low forgetting arises from insufficient plasticity, as also noted in concurrent work (Hu et al., 2026). 

6 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 

_Table 4._ Comparison of continual learning metrics for different levels of pretraining on LIBERO benchmarks. 

|**Method**|LIBERO<br>**SR (**_↑_**)**|-Spatial<br>**NBT (**_↓_**)**|LIBERO<br>**SR (**_↑_**)**|-Object<br>**NBT (**_↓_**)**|LIBER<br>**SR (**_↑_**)**|O-Goal<br>**NBT (**_↓_**)**|Ave<br>**SR (**_↑_**)**|rage<br>**NBT (**_↓_**)**|
|---|---|---|---|---|---|---|---|---|
|Pi0from VL + Action|0.889|-0.00013|0.9179|0.0009|0.782|-0.0974|0.863|-0.0322|
|Pi0from VL|0.9199|0.00469|0.946|0.0105|0.832|0.0325|0.899|0.0159|
|Pi0from scratch|0.528|-0.0795|0.694|-0.0301|0.7419|-0.0082|0.655|-0.0393|
|BC-Transformer|0.590|0.180|0.725|0.101|0.720|0.293|0.678|0.191|


##### Knowledge Transfer (Averaged Across Benchmarks) 


_Figure 5._ **Knowledge transfer** (sum of success rates) curves across four benchmarks. We compare Pi0 trained from scratch (orange), Pi0 trained from PaliGemma (green), and Pi0 pretrained (blue) under different replay buffer sizes (10, 100, 1000). 

While backward transfer quantifies how well previously learned tasks are preserved, it does not capture whether a model continues to effectively acquire new tasks over time. In particular, low measured forgetting can arise either from genuine knowledge retention or from insufficient plasticity, where the model fails to meaningfully learn new tasks. To give a more balanced view of stability and plasticity, we additionally analyze _knowledge transfer_ (KT), which measures the aggregate success rate across all tasks and thus reflects the overall aggregated learning progress throughout continual training (see Fig. 5). Higher slope reflects more accumulation of the task knowledge. 

We examine how knowledge transfer evolves throughout continual learning under different replay buffer sizes. Fig. 5 compares this aggregate knowledge transfer for the three variants using the Pi0 model. We observed that Pi0 from VL + Action and Pi0 from VL exhibit steadily increasing knowledge transfer over time, indicating effective learning of new tasks while preserving prior knowledge. In contrast, Pi0 from scratch often displays slower growth in knowledge transfer. This shows that low measured forgetting in non-pretrained models can arise from an inability to learn new tasks, rather than genuine knowledge preservation. 

Finally, beyond pretraining, we conduct experiments to assess whether other factors may also influence continual learning behavior in VLAs, in particular model size and training objective. We show the results in Appendix C. 

## **6. VLAs Retain Knowledge that is Seemingly Forgotten** 

In this section, we present our key insight that **_a drastic decrease in prior task performance does not necessarily indicate complete forgetting of task-relevant knowledge in pretrained VLAs_** ; instead, this knowledge is still retained, as prior task performance can often be rapidly recovered with minimal finetuning. 

**Methodology.** We begin by investigating which types of knowledge are most susceptible to performance degradation when pretrained VLAs are trained under a continual learning setting. To this end, we decompose the model’s knowledge into three components—vision, language, and action—corresponding to representations stored in the visionlanguage (VL) backbone and the action head. We adopt the following methodology, illustrated in Fig. 6: 

- **Baseline** (Fig. 6 (a)): The model learns three consecutive tasks (Task _k −_ 1, _k_ , and _k_ + 1). As the model moves from Task _k_ to Task _k_ +1, we measure the extent to which learning Task _k_ + 1 degrades performance on Task _k_ . 

- **Component swapping** (Fig. 6 (b)): To identify which part of the model is responsible for the forgetting—the VL backbone or the action head—we swap components between different stages of training. Specifically, we combine the VL backbone learned for Task _k_ + 1 with the action head from Task _k_ and evaluate performance on Task _k_ . A drop in the model’s performance on Task _k_ 

7 

#### **Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 


_Figure 6._ **Methodology for investigating VLA knowledge loss in continual learning.** _(a)_ : Continual learning pipeline of learning Task _k −_ 1, Task _k_ and Task _k_ + 1 sequentially. _(b)_ : Identifying knowledge loss in the vision-language (VL) backbone and action head by swapping components of Task _k_ and Task _k_ + 1. _(c)_ : Recovering vision-language knowledge with finetuning by learning on Task _k_ with backbone from Task _k_ + 1. If the model preserves knowledge from Task _k_ after learning Task _k_ + 1, using Task _k_ + 1’s VL backbone should make learning Task _k_ faster compared with learning Task _k_ for the first time from the VL backbone of _k −_ 1. 


_Figure 7._ **Comparison of mean success rates retained under different vision-language and action combinations.** 

indicates that the backbone has lost relevant VL knowledge. Conversely, we pair the VL backbone from Task _k_ with the action head trained after Task _k_ + 1; degraded performance in this case is attributed to forgetting in the action head. 

- **Task performance recovery** (Fig. 6 (c)): This experiment investigates whether the task knowledge in a given component ( _e.g._ , the VL backbone) is still retained after learning a new task. Using the VL backbone obtained after Task _k_ + 1, we retrain the model on Task _k_ and measure the learning speed. If the model reaches peak performance faster than during its original training on Task _k_ (which started from Task _k −_ 1 backbone), this suggests that the knowledge is partially retained. Otherwise, comparable or slower relearning indicates the knowledge has likely been completely overwritten. 

**What knowledge do VLAs appear to forget?** We conducted component swapping with Pi0 backbone under replay buffer size = 10 (0 _._ 2%), where forgetting is high as shown in the last section. We made three interesting observations: 

_Table 5._ **Recovery efficiency.** _Finetuning_ steps (as ratio of the original training time) needed to regain the peak success rate achieved when learning the task _for the first time_ . 

||**Reco**|**very steps in ratio**_↓_|
|---|---|---|
|**Benchmark**|Pi0|BC-Transformer|
|LIBERO-Spatial|**0.066**|1.36|
|LIBERO-10|**0.105**|1.87|
|LIBERO-Object|**0.067**|1.80|
|LIBERO-Goal|**0.062**|0.33|


- Knowledge is compartmentalized across VLA components: Swapping either the action head or the VL backbone results in performance that is consistently worse than the original (VL _k,_ Action _k_ ) model, yet better than the fully updated (VL _k_ +1 _,_ Action _k_ +1) model. This pattern suggests that knowledge loss in VLA is not monolithic, but instead affects different modules separately. 

- VL backbone is the dominant source of forgetting: Across all four task categories, swapping the VL backbone ( _V Lk_ +1) leads to a larger performance drop compared to swapping only the action head ( _Ak_ +1). This indicates that action-relevant information is relatively more consistent across tasks, whereas updates to the VL backbone alter the underlying representations, leading to a mismatch with previously learned action mappings and consequently greater performance degradation. 

- Knowledge loss correlates with task diversity: The degree of performance degradation aligns with the extent of task variation. For example, LIBERO-10, which features the most diverse visual backgrounds, exhibits the largest drop when swapping VL _k_ +1. In contrast, LIBERO-Object involves similar pick-and-place action across different objects, so it shows minimal degradation when swapping Action _k_ +1. 

**VLAs preserve relevant knowledge of prior tasks despite performance degradation from learning new ones.** 

8 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 


_Figure 8._ **Performance comparison averaged across tasks.** Each column represents a different Libero benchmark (Spatial, 10, Object, Goal) where the x-axis shows the percentage of training steps (0–100%) during finetuning. Pi0 results stop at 20% of the training steps, while BC-Transformer stops at 60% of the training steps. 

Next, we zoom in to examine whether the knowledge in the VL backbone is still preserved using finetuning as a probing tool. For finetuning, we use the same dataset (entire dataset for the task) with its first training, as well as the same model architecture and optimization scheme. For this experiment, we use Pi0 backbone and we compare it with BC-Transformer. 

Fig. 8 shows that Pi0 reaches peak performance within a small fraction of training steps, significantly faster than its initial training. This indicates that task knowledge is preserved in the model and reused during relearning. In contrast, BC-Transformer requires a similar number of steps as initial training to reach peak performance, suggesting that task knowledge has been largely erased. 

Tab. 5 quantifies this behavior using _recovery efficiency_ , defined as the ratio between the steps required to recover the peak success rate ( _Tf_ ) and the original training steps ( _To_ ). Across all benchmarks, Pi0 consistently recovers peak performance with fewer than 10% of the original training steps, whereas BC-Transformer often requires a comparable or greater number of steps and sometimes exhibits unstable finetuning. These results indicate that, although pretrained VLAs may exhibit apparent forgetting in task-level performance (as shown in NBT), the underlying task knowledge is often retained in their internal representations and can be rapidly re-expressed through limited finetuning. On the other hand, non-pretrained models tend to relearn tasks largely from scratch because prior knowledge is erased. 

shed light on future design of continual learning paradigms for VLAs: 1) Continual learning for large VLAs may not require increasingly complex algorithms; instead, it may benefit from strong pretraining and small replay data. 2) To mitigate forgetting, future works should consider effectively reusing knowledge retained in VLA representations, rather than relying solely on larger replay buffers. 

**Limitations.** Most of our evaluation is in simulation on LIBERO (Liu et al., 2023b), where all suites share the same Franka embodiment and similar tabletop environments; we have not tested continual learning extensively across different robots, simulators, or large cross-benchmark shifts. While we report a small real-robot pilot study ( _K_ =3 tasks, single Pi0 run), broader hardware studies with multiple seeds, baselines, and diverse conditions are needed before transferring continual learning setups to real-world deployment. Furthermore, our continual learning protocol depends on experience replay over stored teleoperation transitions. Replay buffers can become costly as tasks accumulate, and may be infeasible under privacy, consent, or data-retention constraints in real-world deployments. Lastly, while the forgetting comparisons span multiple VLAs and BC baselines, our deeper mechanistic studies—including pretraining ablations, component swapping, and recovery analyses—focus mainly on Pi0. Future work should extend these analyses to other VLA architectures to determine which mechanisms of forgetting and recovery are model-specific or broadly shared. 

## **7. Conclusion and Discussion** 

In this paper, we evaluate VLAs in continual learning and demonstrate that they are surprisingly resistant to forgetting. To understand the underlying dynamics, we conduct comprehensive experiments on large-scale pretraining and on how task-relevant knowledge is retained. Our findings 

9 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 

### **Acknowledgment** 

We thank the Texas Advanced Computing Center (TACC) and the Center for Generative AI at UT Austin for providing valuable computing resources. We thank Rutav Shah and Yu Lei for their valuable discussions and helpful feedback on the manuscript, and Abhiram Maddukuri for sharing technical details and codebase setup tips. We thank Zihui Xue and Xixi Hu for providing helpful guidance on the TACC compute setup. We thank Yuqi Xie for providing helpful guidance on the GR00T N1.5 codebase. We thank Zhiyuan Zhou and Yajat Yadav for sharing the customized pretrained Pi0 model checkpoints. This work was partially supported by the National Science Foundation (FRR-2145283, EFRI-2318065), the Office of Naval Research (N00014-24-1-2550), the DARPA TIAMAT program (HR0011-24-9-0428), and the Army Research Lab (W911NF-25-1- 0065). It was also supported by the Institute of Information & Communications Technology Planning & Evaluation (IITP) grant funded by the Korean Government (MSIT) (No. RS-2024-00457882, National AI Research Lab Project). 

## **Impact Statement** 

**Applications.** This work sits at the intersection of continual learning methods and Vision-Language-Action (VLA) models for robotic manipulation. By characterizing forgetting, experience replay, and knowledge retention in large pretrained VLAs, our results may influence how researchers and practitioners design lifelong imitationlearning pipelines. For example, by relying more on strong pretraining and modest replay rather than on increasingly complex continual-learning algorithms developed for smaller behavior-cloning models. Potential applications include more data-efficient sequential skill acquisition with smaller replay buffers and faster recovery of prior skills via rapid fine-tuning when policy performance drops. 

**Implications.** These application trends could have both positive and negative societal consequences, though the magnitude and timing are uncertain. On the positive side, more stable continual learning may lower the cost of maintaining strong manipulation policies across long task sequences, which could eventually support assistive or industrial robotics where systems must accumulate skills over time. On the negative side, improved continual learning for generalist manipulation policies may accelerate automation and labor-market disruption; we do not study distributional or economic effects here. Our use of demonstration replay also raises privacy and consent concerns when trajectories come from human operators. Large-scale VLA pretraining carries substantial compute and environmental costs, which our scaling analysis touches on but does not fully quantify at deployment scale. A further risk is over-trust 

in low measured forgetting or rapid recovery: policies can appear stable on held-out evaluation while still failing on long-tail rare conditions, which is especially consequential in real-world manipulation settings. 

**Initiatives.** We encourage follow-up work that (i) develops continual-learning metrics beyond task success, for example, including diagnostics for latent retention failures and sensitivity to task ordering; (ii) studies fairness, consent, and safe handling of replayed demonstrations; and (iii) tracks the environmental footprint of scaling VLA pretraining alongside downstream continual adaptation. Normative and policy efforts, such as guidelines for demonstration data collection and transparency about which tasks a continually updated policy has been validated on, may complement technical mitigation. We view this paper as a foundational empirical analysis intended to inform safer and more efficient continual VLA research rather than as a deployment recipe. 

## **References** 

- Beyer, L., Steiner, A., Pinto, A. S., Kolesnikov, A., Wang, X., Salz, D., Neumann, M., Alabdulmohsin, I., Tschannen, M., Bugliarello, E., Unterthiner, T., Keysers, D., Koppula, S., Liu, F., Grycner, A., Gritsenko, A., Houlsby, N., Kumar, M., Rong, K., Eisenschlos, J., Kabra, R., Bauer, M., Bosnjak, M., Chen, X., Minderer, M., Voigt-ˇ laender, P., Bica, I., Balazevic, I., Puigcerver, J., Papalampidi, P., Henaff, O., Xiong, X., Soricut, R., Harmsen, J., and Zhai, X. Paligemma: A versatile 3b vlm for transfer, 2024. URL https://arxiv.org/abs/2407. 07726. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., Levine, S., LiBell, A., Mothukuri, M., Nair, S., Pertsch, K., Shi, L. X., Tanner, J., Vuong, Q., Walling, A., Wang, H., and Zhilinsky, U. _π_ 0: A vision-language-action flow model for general robot control, 2026. URL https: //arxiv.org/abs/2410.24164. 

- Bousmalis, K., Vezzani, G., Rao, D., Devin, C., Lee, A. X., Bauza, M., Davchev, T., Zhou, Y., Gupta, A., Raju, A., et al. Robocat: A self-improving generalist agent for robotic manipulation. _arXiv preprint arXiv:2306.11706_ , 2023. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Chen, X., Choromanski, K., Ding, T., Driess, D., Dubey, A., 

10 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 

Finn, C., Florence, P., Fu, C., Arenas, M. G., Gopalakrishnan, K., Han, K., Hausman, K., Herzog, A., Hsu, J., Ichter, B., Irpan, A., Joshi, N., Julian, R., Kalashnikov, D., Kuang, Y., Leal, I., Lee, L., Lee, T.-W. E., Levine, S., Lu, Y., Michalewski, H., Mordatch, I., Pertsch, K., Rao, K., Reymann, K., Ryoo, M., Salazar, G., Sanketi, P., Sermanet, P., Singh, J., Singh, A., Soricut, R., Tran, H., Vanhoucke, V., Vuong, Q., Wahid, A., Welker, S., Wohlhart, P., Wu, J., Xia, F., Xiao, T., Xu, P., Xu, S., Yu, T., and Zitkovich, B. Rt-2: Vision-language-action models transfer web knowledge to robotic control, 2023a. URL https://arxiv.org/abs/2307.15818. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., Ibarz, J., Ichter, B., Irpan, A., Jackson, T., Jesmonth, S., Joshi, N. J., Julian, R., Kalashnikov, D., Kuang, Y., Leal, I., Lee, K.-H., Levine, S., Lu, Y., Malla, U., Manjunath, D., Mordatch, I., Nachum, O., Parada, C., Peralta, J., Perez, E., Pertsch, K., Quiambao, J., Rao, K., Ryoo, M., Salazar, G., Sanketi, P., Sayed, K., Singh, J., Sontakke, S., Stone, A., Tan, C., Tran, H., Vanhoucke, V., Vega, S., Vuong, Q., Xia, F., Xiao, T., Xu, P., Xu, S., Yu, T., and Zitkovich, B. Rt-1: Robotics transformer for real-world control at scale, 2023b. URL https: //arxiv.org/abs/2212.06817. 

- Chaudhry, A., Rohrbach, M., Elhoseiny, M., Ajanthan, T., Dokania, P. K., Torr, P. H. S., and Ranzato, M. On tiny episodic memories in continual learning, 2019. URL https://arxiv.org/abs/1902.10486. 

- De Lange, M., Aljundi, R., Masana, M., Parisot, S., Jia, X., Leonardis, A., Slabaugh, G., and Tuytelaars, T. A continual learning survey: Defying forgetting in classification tasks. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 44(7):3366–3385, 2022. 

- Driess, D. et al. PaLM-E: An embodied multimodal language model. _arXiv preprint arXiv:2303.03378_ , 2023. 

- French, R. M. Catastrophic forgetting in connectionist networks. _Trends in Cognitive Sciences_ , 3(4):128–135, 1999a. ISSN 1364-6613. doi: https://doi.org/10.1016/S1364-6613(99)01294-2. URL https://www.sciencedirect.com/ science/article/pii/S1364661399012942. 

- French, R. M. Catastrophic forgetting in connectionist networks. _Trends in Cognitive Sciences_ , 3(4):128–135, 1999b. 

- Hu, H., Sener, O., Sha, F., and Koltun, V. Drinking from a firehose: Continual learning with web-scale natural language. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 45(5):5684–5696, 2023. doi: 10. 1109/TPAMI.2022.3218265. 

- Hu, J., Shim, J., Tang, C., Sung, Y., Liu, B., Stone, P., and Martin-Martin, R. Simple recipe works: Visionlanguage-action models are natural continual learners with reinforcement learning, 2026. URL https:// arxiv.org/abs/2603.11653. 

- Jang, E., Irpan, A., Khansari, M., Kappler, D., Ebert, F., Lynch, C., Levine, S., and Finn, C. Bc-z: Zero-shot task generalization with robotic imitation learning, 2022a. URL https://arxiv.org/abs/2202.02005. 

- Jang, J., Ye, S., Yang, S., Shin, J., Han, J., Kim, G., Choi, S., and Seo, M. Towards continual knowledge learning of language models. In _International Conference on Learning Representations (ICLR)_ , 2022b. URL https: //openreview.net/forum?id=vfsRB5MImo9. 

- Jang, J. et al. Temporalwiki: A lifelong benchmark for training and evaluating ever-evolving language models. _arXiv preprint arXiv:2204.14211_ , 2022c. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., Vuong, Q., Kollar, T., Burchfiel, B., Tedrake, R., Sadigh, D., Levine, S., Liang, P., and Finn, C. Openvla: An open-source vision-language-action model, 2024. URL https://arxiv.org/abs/2406.09246. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E. P., Sanketi, P. R., Vuong, Q., Kollar, T., Burchfiel, B., Tedrake, R., Sadigh, D., Levine, S., Liang, P., and Finn, C. Openvla: An open-source vision-language-action model. In _Proceedings of The 8th Conference on Robot Learning (CoRL)_ , volume 270 of _Proceedings of Machine Learning Research_ , 2025. 

- Kirkpatrick, J., Pascanu, R., Rabinowitz, N., Veness, J., Desjardins, G., Rusu, A. A., Milan, K., Quan, J., Ramalho, T., Grabska-Barwinska, A., Hassabis, D., Clopath, C., Kumaran, D., and Hadsell, R. Overcoming catastrophic forgetting in neural networks. _Proceedings of the National Academy of Sciences_ , 114 (13):3521–3526, March 2017a. ISSN 1091-6490. doi: 10.1073/pnas.1611835114. URL http://dx.doi. org/10.1073/pnas.1611835114. 

- Kirkpatrick, J., Pascanu, R., Rabinowitz, N., Veness, J., Desjardins, G., Rusu, A. A., Milan, K., Quan, J., Ramalho, T., Grabska-Barwinska, A., et al. Overcoming catastrophic forgetting in neural networks. _Proceedings of the National Academy of Sciences_ , 114(13):3521–3526, 2017b. doi: 10.1073/pnas.1611835114. 

- Lesort, T., Lomonaco, V., Stoian, A., Maltoni, D., Filliat, D., and D´ıaz-Rodr´ıguez, N. Continual learning for robotics: Definition, framework, learning strategies, opportunities and challenges. _Information Fusion_ , 58:52–68, 2020. 

11 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 

- Levine, S., Finn, C., Darrell, T., and Abbeel, P. End-toend training of deep visuomotor policies, 2016. URL https://arxiv.org/abs/1504.00702. 

- Li, Z. and Hoiem, D. Learning without forgetting. In _Proceedings of the European Conference on Computer Vision (ECCV)_ , 2016. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. In _Advances in Neural Information Processing Systems (NeurIPS) Datasets and Benchmarks Track_ , 2023a. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning, 2023b. 

- Liu, H., Li, X., Li, P., Liu, M., Wang, D., Liu, J., Kang, B., Ma, X., Kong, T., and Zhang, H. Towards generalist robot policies: What matters in building vision-language-action models. _Nature Machine Intelligence_ , 2025. 

- Lopez-Paz, D. and Ranzato, M. Gradient episodic memory for continual learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2017. 

- Luo, Y., Yang, Z., Meng, F., Li, Y., Zhou, J., and Zhang, Y. An empirical study of catastrophic forgetting in large language models during continual fine-tuning, 2025. URL https://arxiv.org/abs/2308.08747. 

- Mallya, A. and Lazebnik, S. Packnet: Adding multiple tasks to a single network by iterative pruning, 2018. URL https://arxiv.org/abs/1711.05769. 

- McCloskey, M. and Cohen, N. J. Catastrophic interference in connectionist networks: The sequential learning problem. volume 24 of _Psychology of Learning and Motivation_ , pp. 109–165. Academic Press, 1989a. doi: https://doi.org/10.1016/S0079-7421(08)60536-8. URL https://www.sciencedirect.com/ science/article/pii/S0079742108605368. 

- McCloskey, M. and Cohen, N. J. Catastrophic interference in connectionist networks: The sequential learning problem. _Psychology of Learning and Motivation_ , 24: 109–165, 1989b. 

- NVIDIA, Bjorck, J., Castaneda, F., Cherniadev, N., Da, X.,˜ Ding, R., Fan, L. J., Fang, Y., Fox, D., Hu, F., Huang, S., Jang, J., Jiang, Z., Kautz, J., Kundalia, K., Lao, L., Li, Z., Lin, Z., Lin, K., Liu, G., Llontop, E., Magne, L., Mandlekar, A., Narayan, A., Nasiriany, S., Reed, S., Tan, Y. L., Wang, G., Wang, Z., Wang, J., Wang, Q., Xiang, J., Xie, Y., Xu, Y., Xu, Z., Ye, S., Yu, Z., Zhang, A., Zhang, H., Zhao, Y., Zheng, R., and Zhu, Y. Gr00t n1: An open foundation model for generalist humanoid robots, 2025. URL https://arxiv.org/abs/2503.14734. 

- Octo Model Team, Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., Luo, J., Tan, Y. L., Chen, L. Y., Sanketi, P., Vuong, Q., Xiao, T., Sadigh, D., Finn, C., and Levine, S. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- Open X-Embodiment Collaboration, O’Neill, A., Rehman, A., Gupta, A., et al. Open X-embodiment: Robotic learning datasets and RT-X models. _arXiv preprint arXiv:2310.08864_ , 2023. 

- OpenAI, Achiam, J., Adler, S., Agarwal, S., Ahmad, L., Akkaya, I., Aleman, F. L., Almeida, D., Altenschmidt, J., Altman, S., Anadkat, S., Avila, R., Babuschkin, I., Balaji, S., Balcom, V., Baltescu, P., Bao, H., Bavarian, M., Belgum, J., Bello, I., Berdine, J., Bernadett-Shapiro, G., Berner, C., Bogdonoff, L., Boiko, O., Boyd, M., Brakman, A.-L., Brockman, G., Brooks, T., Brundage, M., Button, K., Cai, T., Campbell, R., Cann, A., Carey, B., Carlson, C., Carmichael, R., Chan, B., Chang, C., Chantzis, F., Chen, D., Chen, S., Chen, R., Chen, J., Chen, M., Chess, B., Cho, C., Chu, C., Chung, H. W., Cummings, D., Currier, J., Dai, Y., Decareaux, C., Degry, T., Deutsch, N., Deville, D., Dhar, A., Dohan, D., Dowling, S., Dunning, S., Ecoffet, A., Eleti, A., Eloundou, T., Farhi, D., Fedus, L., Felix, N., Fishman, S. P., Forte, J., Fulford, I., Gao, L., Georges, E., Gibson, C., Goel, V., Gogineni, T., Goh, G., Gontijo-Lopes, R., Gordon, J., Grafstein, M., Gray, S., Greene, R., Gross, J., Gu, S. S., Guo, Y., Hallacy, C., Han, J., Harris, J., He, Y., Heaton, M., Heidecke, J., Hesse, C., Hickey, A., Hickey, W., Hoeschele, P., Houghton, B., Hsu, K., Hu, S., Hu, X., Huizinga, J., Jain, S., Jain, S., Jang, J., Jiang, A., Jiang, R., Jin, H., Jin, D., Jomoto, S., Jonn, B., Jun, H., Kaftan, T., Łukasz Kaiser, Kamali, A., Kanitscheider, I., Keskar, N. S., Khan, T., Kilpatrick, L., Kim, J. W., Kim, C., Kim, Y., Kirchner, J. H., Kiros, J., Knight, M., Kokotajlo, D., Łukasz Kondraciuk, Kondrich, A., Konstantinidis, A., Kosic, K., Krueger, G., Kuo, V., Lampe, M., Lan, I., Lee, T., Leike, J., Leung, J., Levy, D., Li, C. M., Lim, R., Lin, M., Lin, S., Litwin, M., Lopez, T., Lowe, R., Lue, P., Makanju, A., Malfacini, K., Manning, S., Markov, T., Markovski, Y., Martin, B., Mayer, K., Mayne, A., McGrew, B., McKinney, S. M., McLeavey, C., McMillan, P., McNeil, J., Medina, D., Mehta, A., Menick, J., Metz, L., Mishchenko, A., Mishkin, P., Monaco, V., Morikawa, E., Mossing, D., Mu, T., Murati, M., Murk, O., Mely, D., Nair, A., Nakano, R., Nayak, R., Neelakantan,´ A., Ngo, R., Noh, H., Ouyang, L., O’Keefe, C., Pachocki, J., Paino, A., Palermo, J., Pantuliano, A., Parascandolo, G., Parish, J., Parparita, E., Passos, A., Pavlov, M., Peng, A., Perelman, A., de Avila Belbute Peres, F., Petrov, M., de Oliveira Pinto, H. P., Michael, Pokorny, Pokrass, M., Pong, V. H., Powell, T., Power, A., Power, B., Proehl, E., Puri, R., Radford, A., Rae, J., Ramesh, A., Raymond, C., 

12 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 

Real, F., Rimbach, K., Ross, C., Rotsted, B., Roussez, H., Ryder, N., Saltarelli, M., Sanders, T., Santurkar, S., Sastry, G., Schmidt, H., Schnurr, D., Schulman, J., Selsam, D., Sheppard, K., Sherbakov, T., Shieh, J., Shoker, S., Shyam, P., Sidor, S., Sigler, E., Simens, M., Sitkin, J., Slama, K., Sohl, I., Sokolowsky, B., Song, Y., Staudacher, N., Such, F. P., Summers, N., Sutskever, I., Tang, J., Tezak, N., Thompson, M. B., Tillet, P., Tootoonchian, A., Tseng, E., Tuggle, P., Turley, N., Tworek, J., Uribe, J. F. C., Vallone, A., Vijayvergiya, A., Voss, C., Wainwright, C., Wang, J. J., Wang, A., Wang, B., Ward, J., Wei, J., Weinmann, C., Welihinda, A., Welinder, P., Weng, J., Weng, L., Wiethoff, M., Willner, D., Winter, C., Wolrich, S., Wong, H., Workman, L., Wu, S., Wu, J., Wu, M., Xiao, K., Xu, T., Yoo, S., Yu, K., Yuan, Q., Zaremba, W., Zellers, R., Zhang, C., Zhang, M., Zhao, S., Zheng, T., Zhuang, J., Zhuk, W., and Zoph, B. Gpt-4 technical report, 2024. URL https://arxiv.org/abs/2303.08774. 

- Parisi, G. I., Kemker, R., Part, J. L., Kanan, C., and Wermter, S. Continual lifelong learning with neural networks: A review. _Neural Networks_ , 113:54–71, 2019. 

   - Wan, W., Zhu, Y., Shah, R., and Zhu, Y. Lotus: Continual imitation learning for robot manipulation through unsupervised skill discovery, 2024. URL https://arxiv. org/abs/2311.02058. 

   - Wu, T., Caccia, M., Li, W., Li, S., Hadsell, R., and Pineau, J. Pretrained language model in continual learning: A comparative study. In _International Conference on Learning Representations (ICLR)_ , 2022. 

   - Yadav, Y., Zhou, Z., Wagenmaker, A., Pertsch, K., and Levine, S. Robust finetuning of vision-language-action robot policies via parameter merging, 2026. URL https://arxiv.org/abs/2512.08333. 

   - Zitkovich, B., Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Chen, X., Choromanski, K., Ding, T., Driess, D., Finn, C., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Proceedings of The 7th Conference on Robot Learning (CoRL)_ , volume 229 of _Proceedings of Machine Learning Research_ , 2023. 

- Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., Krueger, G., and Sutskever, I. Learning transferable visual models from natural language supervision, 2021. URL https://arxiv.org/abs/2103.00020. 

- Reed, S. et al. A generalist agent. _arXiv preprint arXiv:2205.06175_ , 2022. 

- Rusu, A. A., Rabinowitz, N. C., Desjardins, G., Soyer, H., Kirkpatrick, J., Kavukcuoglu, K., Pascanu, R., and Hadsell, R. Progressive neural networks. _arXiv preprint arXiv:1606.04671_ , 2016. 

- Scialom, T., Chakrabarty, T., Dusek,ˇ O., and Muresan, S. Fine-tuned language models are continual learners. In _Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing (EMNLP)_ , 2022. 

- Shah, R., Mart´ın-Mart´ın, R., and Zhu, Y. Mutex: Learning unified policies from multimodal task specifications. In _Conference on Robot Learning_ , 2023. 

- Shenfeld, I., Pari, J., and Agrawal, P. Rl’s razor: Why online reinforcement learning forgets less, 2025. URL https://arxiv.org/abs/2509.04259. 

- Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M.-A., Lacroix, T., Roziere,` B., Goyal, N., Hambro, E., Azhar, F., Rodriguez, A., Joulin, A., Grave, E., and Lample, G. Llama: Open and efficient foundation language models, 2023. URL https://arxiv.org/ abs/2302.13971. 

13 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 

# **Appendix: Table of Contents** 

|**A**<br>**Mo**|**re Continual Learning Results** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15|
|---|---|
|A.1|Full Confusion Matrix Results for Comparison . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15|
|A.2|Discussion on LIBERO-10 Continual Learning Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16|
|A.3|Results for Other Replay Buffer Sizes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17|
|**B**<br>**Exp**|**erimental Setup Details** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17|
|B.1|ER Training Details . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17|
|B.2|LIBERO Benchmark Details . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17|
|B.3|Model Details . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17|
|B.4|Training Hyperparameters . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17|
|B.5|Continual Learning Baselines<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19|
|**C**<br>**Stu**|**dy on Other Factors that Contribute to VLA’s Continual Learning Behavior** . . . . . . . . . . . . . . . . . . . . . . . 20|
|**D**<br>**Per**|**-Task Knowledge Transfer Curves: Pi0 vs. BC-Transformer** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20|


14 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 

## **A. More Continual Learning Results** 

### **A.1. Confusion Matrix Results for Comparison** 

We present the full confusion matrix results in Figure 9, which extends Figure 1: each entry ( _i, j_ ) denotes the success rate on task _j_ after training on checkpoint _i_ under ER, for Pi0, GR00T N1.5, BC-Transformer, BC-Diffusion, and BC-ViT on all four LIBERO benchmarks. 


_Figure 9._ **Full confusion matrix results (extending Figure 1).** As in Figure 1, each entry ( _i, j_ ) denotes the success rate on Task _j_ after training on checkpoint _i_ under ER. Shown here are the complete results for Pi0, GR00T N1.5, BC-Transformer, BC-Diffusion, and BC-ViT on the four LIBERO benchmarks. 

15 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 

### **A.2. LIBERO-10 Continual Learning Results** 

We discuss LIBERO-10 separately because, unlike the other three benchmarks, LIBERO-10 comprises diverse tasks with distinct scenes and objectives, which makes it the most challenging benchmark for the continual learning setting. The performance on this benchmark differs a lot across different methods, which reveals an interesting limitation of the standard NBT metric (see Section 3). Since this discussion concerns the metric definition itself rather than the core findings of our work, we present it here in the appendix. 

**Normalized NBT.** Recall that NBT _k_ = _K_ <u>1</u> _−k_ � _Kτ_ = _k_ +1<sup>(</sup><sup>_ck,k −ck,τ_), where</sup><sup>_ck,k_is the success rate on task</sup><sup>_k_immediately</sup> after learning it, and _ck,τ_ is the success rate on task _k_ after training through task _τ_ . Under this definition, policies with higher initial success rates are penalized more heavily: a drop from 90% to 0% contributes 0.90 to NBT, whereas a drop from 40% to 0% contributes only 0.40, even though both represent complete forgetting. To address this, we introduce a _normalized_ NBT variant that scales each forgetting term by the initial performance _ck,k_ : 


so that complete forgetting always equals 1.0, regardless of the initial success rate. Tasks with _ck,k_ = 0 are excluded since no meaningful forgetting can be measured. 

As shown in Figure 10, the absolute NBT (left) makes it appear that GR00T suffers the most forgetting at small buffer sizes because it starts from high success rates. The normalized NBT (right) reveals a more nuanced picture: all policies experience near-complete relative forgetting at buffer size = 10, while the VLA models (Pi0, GR00T) retain substantially more knowledge at buffer size = 1000, with their normalized NBT dropping to near zero or even becoming negative (indicating performance improvement on earlier tasks). We leave a more systematic study of forgetting metrics to future work. 


_Figure 10._ **Absolute vs. normalized NBT on LIBERO-10.** Left: standard NBT, which penalizes higher-performing policies more heavily. Right: NBT normalized by the initial (diagonal) success rate, where 1.0 indicates complete forgetting and values below zero indicate performance improvement after learning later tasks. 

16 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 

_Table 6._ **Continual learning performance on LIBERO-10 for different replay buffer sample sizes** : Average Success Rate (SR) and Negative Backward Transfer (NBT) for sample sizes 10, 100, and 1000. 

|**Method**|**Sample**<br>**SR (**_↑_**)**|**Size = 10**<br>**NBT (**_↓_**)**|**Sample S**<br>**SR (**_↑_**)**|**ize = 100**<br>**NBT (**_↓_**)**|**Sample S**<br>**SR (**_↑_**)**|**ize = 1000**<br>**NBT (**_↓_**)**|
|---|---|---|---|---|---|---|
|Pi0|0_._576_±_0_._034|0_._529_±_0_._035|0_._584_±_0_._045|0_._229_±_0_._066|0_._563_±_0_._028|_−_0_._068_±_0_._018|
|GR00T|0_._851_±_0_._007|0_._766_±_0_._013|0_._854_±_0_._011|0_._525_±_0_._018|0_._820_±_0_._017|0_._059_±_0_._035|
|BC-Diffusion Policy|0_._568_±_0_._020|0_._538_±_0_._031|0_._616_±_0_._012|0_._591_±_0_._022|0_._464_±_0_._024|0_._201_±_0_._044|
|BC-Transformer|0_._367_±_0_._005|0_._339_±_0_._009|0_._403_±_0_._058|0_._382_±_0_._051|0_._376_±_0_._034|0_._192_±_0_._019|
|BC-ViT|0_._371_±_0_._015|0_._350_±_0_._012|0_._324_±_0_._020|0_._308_±_0_._002|0_._316_±_0_._062|0_._204_±_0_._063|


### **A.3. Results for Other Replay Buffer Sizes** 

_Table 7._ **Continual learning performance on LIBERO benchmarks (sample size = 100)** : Average Success Rate (SR) and Negative Backward Transfer (NBT). LIBERO-10 results in Tab. 6. 

|**Method**|LIBERO-<br>**SR (**_↑_**)**|Spatial<br>**NBT (**_↓_**)**|LIBERO-<br>**SR (**_↑_**)**|Object<br>**NBT (**_↓_**)**|LIBER<br>**SR (**_↑_**)**|O-Goal<br>**NBT (**_↓_**)**|Ave<br>**SR (**_↑_**)**|rage<br>**NBT (**_↓_**)**|
|---|---|---|---|---|---|---|---|---|
|Pi0|0_._899_±_0_._012|0_._155_±_0_._010|0_._885_±_0_._020|0_._043_±_0_._072|0_._729_±_0_._016|0_._153_±_0_._039|0_._838_±_0_._017|0_._117_±_0_._048|
|GR00T|0_._921_±_0_._017|0_._151_±_0_._036|0_._963_±_0_._015|0_._117_±_0_._044|0_._939_±_0_._008|0_._282_±_0_._031|0_._941_±_0_._014|0_._184_±_0_._037|
|BC-Diffusion Policy|0_._729_±_0_._094|0_._414_±_0_._117|0_._788_±_0_._083|0_._430_±_0_._080|0_._793_±_0_._035|0_._714_±_0_._059|0_._770_±_0_._075|0_._520_±_0_._089|
|BC-Transformer|0_._657_±_0_._009|0_._379_±_0_._028|0_._625_±_0_._188|0_._402_±_0_._125|0_._744_±_0_._017|0_._609_±_0_._024|0_._675_±_0_._109|0_._463_±_0_._076|
|BC-ViT|0_._537_±_0_._048|0_._444_±_0_._042|0_._596_±_0_._275|0_._380_±_0_._239|0_._693_±_0_._015|0_._653_±_0_._022|0_._609_±_0_._161|0_._492_±_0_._141|


_Table 8._ **Continual learning performance on LIBERO benchmarks (sample size = 10)** : Average Success Rate (SR) and Negative Backward Transfer (NBT). LIBERO-10 results in Tab. 6. 

||LIBERO-|Spatial|LIBERO-|Object|LIBER|O-Goal|Ave|rage|
|---|---|---|---|---|---|---|---|---|
|**Method**|**SR (**_↑_**)**|**NBT (**_↓_**)**|**SR (**_↑_**)**|**NBT (**_↓_**)**|**SR (**_↑_**)**|**NBT (**_↓_**)**|**SR (**_↑_**)**|**NBT (**_↓_**)**|
|Pi0|0_._872_±_0_._018|0_._704_±_0_._062|0_._875_±_0_._010|0_._511_±_0_._050|0_._773_±_0_._036|0_._536_±_0_._049|0_._840_±_0_._024|0_._583_±_0_._054|
|GR00T|0_._910_±_0_._010|0_._710_±_0_._013|0_._963_±_0_._008|0_._750_±_0_._017|0_._951_±_0_._008|0_._780_±_0_._021|0_._942_±_0_._009|0_._747_±_0_._018|
|BC-Diffusion Policy|0_._753_±_0_._040|0_._779_±_0_._049|0_._890_±_0_._024|0_._697_±_0_._057|0_._876_±_0_._026|0_._865_±_0_._022|0_._839_±_0_._031|0_._780_±_0_._045|
|BC-Transformer|0_._720_±_0_._011|0_._740_±_0_._022|0_._631_±_0_._081|0_._536_±_0_._045|0_._845_±_0_._020|0_._853_±_0_._016|0_._732_±_0_._037|0_._710_±_0_._028|
|BC-ViT|0_._609_±_0_._056|0_._617_±_0_._063|0_._585_±_0_._146|0_._371_±_0_._224|0_._753_±_0_._030|0_._803_±_0_._031|0_._649_±_0_._092|0_._597_±_0_._136|


## **B. Experimental Setup Details** 

### **B.1. ER Training Details** 

We fixed the replay buffer size budget for all methods to ensure fair comparison. Following the same setting as LIBERO (Liu et al., 2023b), we use a replay buffer size = 1000 transitions ( _i.e._ , state-action pairs) per task across all methods, which is approximately 15 _−_ 20% of the full task dataset. Following libero (Liu et al., 2023b), we equally sample data from the replay buffer and the current task, making it a 1:1 ratio between the current task and all past tasks. 

### **B.2. LIBERO Benchmark Details** 

We provide the task order used for each LIBERO benchmark below. We follow the same randomized task order for all methods to ensure fair comparison. 

17 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 

### LIBERO-Spatial Task Order 

1. Pick up the black bowl between the plate and the ramekin and place it on the plate. 

2. Pick up the black bowl next to the ramekin and place it on the plate. 

3. Pick up the black bowl from table center and place it on the plate. 

4. Pick up the black bowl on the cookie box and place it on the plate. 

5. Pick up the black bowl in the top drawer of the wooden cabinet and place it on the plate. 

6. Pick up the black bowl on the ramekin and place it on the plate. 

7. Pick up the black bowl next to the cookie box and place it on the plate. 

8. Pick up the black bowl on the stove and place it on the plate. 

9. Pick up the black bowl next to the plate and place it on the plate. 

10. Pick up the black bowl on the wooden cabinet and place it on the plate. 

### LIBERO-Object Task Order 

1. Pick up the alphabet soup and place it in the basket. 

2. Pick up the bbq sauce and place it in the basket. 

3. Pick up the butter and place it in the basket. 

4. Pick up the chocolate pudding and place it in the basket. 

5. Pick up the cream cheese and place it in the basket. 

6. Pick up the ketchup and place it in the basket. 

7. Pick up the milk and place it in the basket. 

8. Pick up the orange juice and place it in the basket. 

9. Pick up the salad dressing and place it in the basket. 

10. Pick up the tomato sauce and place it in the basket. 

### LIBERO-Goal Task Order 

1. Open the middle drawer of the cabinet. 

2. Put the bowl on the stove. 

3. Put the wine bottle on top of the cabinet. 

4. Open the top drawer and put the bowl inside. 

5. Put the bowl on top of the cabinet. 

6. Push the plate to the front of the stove. 

7. Put the cream cheese in the bowl. 

8. Turn on the stove. 

9. Put the bowl on the plate. 

10. Put the wine bottle on the rack. 

18 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 

### LIBERO-10 Task Order 

1. Pick up the book and place it in the back compartment of the caddy. 

2. Put both moka pots on the stove. 

3. Put both the alphabet soup and the cream cheese box in the basket. 

4. Put both the alphabet soup and the tomato sauce in the basket. 

5. Put both the cream cheese box and the butter in the basket. 

6. Put the black bowl in the bottom drawer of the cabinet and close it. 

7. Put the white mug on the left plate and put the yellow and white mug on the right plate. 

8. Put the white mug on the plate and put the chocolate pudding to the right of the plate. 

9. Put the yellow and white mug in the microwave and close it. 

10. Turn on the stove and put the moka pot on it. 

### **B.3. Model Details** 

_Table 9._ Architecture and pretraining details of all models evaluated in this work. “Frozen” indicates components whose weights are not updated during continual learning; “Finetuned” indicates trainable components. For Pi0, LoRA adapters are applied to the frozen backbone. 

||pi0|GR00T|BC-Diffusion Policy|BC-Transformer|BC-ViT|
|---|---|---|---|---|---|
|Total params|3B|3B|_∼_26M|_∼_15M|_∼_15M|
|Vision encoder|SigLIP-So400m<br>(pretrained, finetuned)|SigLIP<br>(pretrained, frozen)|ResNet-18<br>(trained from scratch)|ResNet-18<br>(trained from scratch)|ViT-Patch<br>(trained from scratch)|
|Language model|Gemma-2B<br>(pretrained, finetuned)|Qwen3-1.7B<br>(pretrained, frozen)|BERT (pretrained, frozen)<br>+ MLP (trained from scratch)|BERT (pretrained, frozen)<br>+ MLP (trained from scratch)|BERT (pretrained, frozen)<br>+ MLP (trained from scratch)|
|Action head|Flow Matching (Gemma-300M)<br>(pretrained, finetuned)|Flow Matching DiT<br>(pretrained, finetuned)|DDPM UNet<br>(trained from scratch)|MLP + GMM<br>(trained from scratch)|MLP + GMM<br>(trained from scratch)|
|Finetuning strategy|Vision: full FT,<br>Language: LoRA FT,<br>Action: LoRA FT|Vision: frozen,<br>Language: frozen,<br>action: full FT|Full FT (all params)|Full FT (all params)|Full FT (all params)|


### **B.4. Training Hyperparameters** 

_Table 10._ Training hyperparameters for continual learning experiments. VLA models (pi0, GR00T) use a fixed number of gradient steps per task, while BC baselines train for a fixed number of epochs per task. 

|**Hyperparameter**|pi0|GR00T|BC-Diffusion Policy|BC-Transformer|BC-ViT|
|---|---|---|---|---|---|
|Learning rate|2.5e-5|1e-4|1e-4|1e-4|1e-4|
|Batch size|8|16|16|16|16|
|Training budget per task|10,000 steps|10,000 steps|50 epochs|50 epochs|50 epochs|
|Optimizer|AdamW|AdamW|AdamW|AdamW|AdamW|
|Weight decay|1e-10|1e-5|1e-4|1e-4|1e-4|
|LR scheduler|Cosine decay|Cosine decay|Cosine decay|Cosine decay|Cosine decay|


### **B.5. Continual Learning Baselines** 

**Elastic Weight Consolidation (EWC)** (Kirkpatrick et al., 2017b) is another common continual learning method that employs a regularization term discouraging changes to parameters important for previously learned tasks. EWC estimates parameter importance using Fisher information matrix computed after each task, and uses it to weight a quadratic penalty that keeps the model close to the parameters learned from earlier tasks. 

19 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 

**Sequential Training** (Liu et al., 2023b) is the simplest continual learning method, where the model is trained on each task sequentially without any explicit mechanisms to prevent forgetting. 

## **C. Study on Other Factors that Contribute to VLA’s Continual Learning Behavior** 

**Model size contributes to mitigating forgetting.** We observe that large VLA model trained from scratch (without pretraining) also displays near-zero forgetting; one hypothesis is model size also contributes to VLA’s forgetting dynamics. To validate on the effect of model size, we test on a few Pi0 variants with smaller model sizes (all trained from scratch). We observe in Tab. 11 that smaller models gives higher NBT than larger ones, showing that model size also plays a role here. While this serves an initial investigation, we will leave more systematic study of model size (in relation to pretraining) in future work. 

_Table 11._ **Effect of model size on forgetting (scratch training).** NBT (positive value indicates there is forgetting; the lower is better) for Pi0 variants trained from scratch with different LLM-action expert and vision-backbone sizes. 

|**LLM + Action Expert**|**Vision Backbone**|**NBT (**_↓_**)**|
|---|---|---|
|17M|ResNet (_∼_0.5M)|0.1100|
|17M|SigLIP-B/16 (80M)|0.0628|
|17M|SigLIP-So400M/14 (400M)|0.0264|
|250M|SigLIP-B/16 (80M)|-0.0478|
|250M|SigLIP-So400M/14 (400M)|-0.0520|


**Training objective has little effect on forgetting.** To isolate the effect of the training objective, we ablate Pi0, which trains its action expert with a flow-matching objective, by retraining it with an _ℓ_ 2 regression loss while keeping the architecture unchanged. As shown in Tab. 12, the resulting performance has little difference, suggesting that the choice of training objective is not a primary factor. 

_Table 12._ Comparison of continual learning metrics for different training objectives (LIBERO-Spatial). 

|**Method**|**SR**|**NBT**|
|---|---|---|
|Pi0w. Flow Matching|0.836|-0.0003|
|Pi0w. L2 Loss|0.853|0.016|


## **D. Per-Task Knowledge Transfer Curves: Pi0 vs. BC-Transformer** 

Extending Figure 8, we present per-task breakdowns of the knowledge transfer curves comparing Pi0 and BC-Transformer across all four LIBERO benchmarks (See Figure 11, 12, 13, and 14). For each task, the top subplot shows Pi0 and the bottom shows BC-Transformer, with both the Finetuning and Learn First Time (LFT) curves plotted. All success rates are normalized by the LFT curve’s peak for that task; a value of 1 _._ 0 indicates full recovery of LFT performance. 

20 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 


_Figure 11._ **Per-task knowledge transfer curves on LIBERO-Spatial** . 

LIBERO-Object 


_Figure 12._ **Per-task knowledge transfer curves on LIBERO-Object** . 

21 

**Pretrained VLAs are Surprisingly Resistant to Forgetting in Continual Learning** 


_Figure 13._ **Per-task knowledge transfer curves on LIBERO-Goal** . 

##### LIBERO-10 


_Figure 14._ **Per-task knowledge transfer curves on LIBERO-10** . 

22 

