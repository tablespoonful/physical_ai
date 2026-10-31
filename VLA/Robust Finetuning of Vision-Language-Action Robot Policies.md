---
title: "Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging"
date: "2025-12-09"
authors: "Yajat Yadav; Zhiyuan Zhou; Andrew Wagenmaker; Karl Pertsch; Sergey Levine"
venue: "ICLR 2026 Poster"
url: https://arxiv.org/abs/2512.08333
pdf: https://arxiv.org/pdf/2512.08333
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.08333)** / [論文ページ](https://arxiv.org/abs/2512.08333)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging** 

**Yajat Yadav**<sup>∗</sup> **, Zhiyuan Zhou**<sup>∗</sup> **, Andrew Wagenmaker, Karl Pertsch, Sergey Levine** 

UC Berkeley https://retain.yajatyadav.com 


**Figure 1:** Naive approaches for finetuning of generalist policies narrowly improve target task performance on settings seen in the finetuning data, but fail to generalize or retain generality beyond the target task. We propose a simple solution: by averaging the generalist policy before and after finetuning, _in weight space_ , we obtain finetuned policies that (1) significantly improve generalization ability to unseen variations of the target task, and (2) retain generalist capabilities on non-target tasks. Our approach RETAIN is a simple solution for robust policy finetuning. 

**Generalist robot policies, trained on large and diverse datasets, have demonstrated the ability to generalize across a wide spectrum of behaviors, enabling a single policy to act in varied real-world environments. However, they still fall short on new tasks not covered in the training data. When finetuned on limited demonstrations of a new task, these policies often overfit to the specific demonstrations—not only losing their prior abilities to solve a wide variety of generalist tasks but also failing to generalize within the new task itself. In this work, we aim to develop a method that preserves the generalization capabilities of the generalist policy during finetuning, allowing a single policy to robustly incorporate a new skill into its repertoire. Our goal is a** **_single_ policy that both learns to generalize to variations of the new task and retains the broad competencies gained from pretraining. We show that this can be achieved through a simple yet effective strategy: interpolating the weights of a finetuned model with that of the pretrained model. We show, across extensive simulated and real-world experiments, that such** **_model merging_ produces a single model that inherits the generalist abilities of the base model and learns to solve the new task robustly, outperforming both the pretrained and finetuned model on out-of-distribution variations of the new task. Moreover, we show that model merging performance scales with the amount of pretraining data, and enables continual acquisition of new skills in a lifelong learning setting, without sacrificing previously learned generalist abilities.** 

## **1. Introduction** 

Generalist robot policies trained on large corpora of data have recently shown impressive generalization abilities: out of the box, they can perform a range of tasks in unseen environments, generalize across scenes, viewpoints, 

> ∗ Core contributors. 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

objects, and language instructions [21, 45, 26, 52, 44, 32, 46, 16, 1]. Though impressively general, these generalist policies often need to be adapted to perform effectively on downstream tasks or a new robot system, which is most commonly achieved by finetuning them on a curated dataset of demonstrations for the target task. While prior work has shown that such finetuning can lead to robust policies with tens or hundreds of hours of finetuning data [8, 21, 9, 10], collecting such amounts of robot demonstration data is challenging. As a result, in practice often less than 100 demonstrations or a few hours of robot data are used for finetuning [26, 53, 27]. Existing approaches for robot policy finetuning struggle to _preserve_ the generality of the pretrained model in such low-data regimes, and fail to robustly generalize far beyond the exact viewpoints, objects, and scenarios seen in the finetuning data [16, 64, 71, 59, 63, 73, 24]. To expand the usability of generalist policies, we need _robust_ finetuning approaches that better preserve the generality of pretrained robot policies and allow us to generalize to a broader set of scenarios _on the target task_ . 

In this work, we introduce RETAIN ( **R** obust fin **E** -tuning wi **T** h p **A** rameter merg **IN** g), a surprisingly simple approach for robust robot policy finetuning. By simply interpolating the _weights_ of the pretrained generalist policy before and after finetuning on the target task (see Fig. 1), we obtain checkpoints that match the performance of the finetuned policy on scenarios present in the finetuning data, while generalizing significantly better to unseen variations of the target task, such as unseen object instances, positions, or viewpoints. Additionally, we observe that RETAIN preserves the generalist capabilities of the pretrained policy also on tasks _other than the target task_ , allowing us to use RETAIN in a continual learning setup by sequentially _merging_ new skills into pretrained generalist policies (in a literal sense). We demonstrate the effectiveness of RETAIN for robust policy finetuning and sequential skill acquisition across a range of real-world and simulated finetuning tasks, achieving state-of-the-art finetuning performance. We also show that RETAIN gets even more effective when the pretrained policy is trained on more data. While previous work has investigated interpolating model weights of pretrained and fine-tuned models for vision and language [62, 61, 20], this is to our knowledge the first work to investigate and analyze parameter merging for robot policies and use it to enable continual acquisition of new robotic skills. 

In summary, our contributions are threefold: (1) we introduce a simple approach for robust robot policy finetuning via policy parameter merging, (2) we extensively evaluate our approach across a suite of real-world and simulated robot finetuning tasks, and analyze which factors enable successful policy merging, (3) we demonstrate that our approach enables continual merging of new robot skills into state-of-the-art generalist policies. Policies finetuned with our method generalize to novel scenarios for the new skill on real robots with ∼40% higher success rate on average than best prior finetuning methods. 

## **2. Related Work** 

**Adapting generalist policies on new tasks.** Fueled by large-scale human teleoperated robot datasets [11, 54, 25, 48], generalist robot policies have recently solved a wide range of tasks across diverse scenes [8, 52, 44, 26, 10, 32, 2, 50, 46]. Yet, even state-of-the-art generalist policies typically need to be adapted for any given target task to achieve high performance [8]. Thus, a number of approaches have been proposed for training generalist policies on a new target task: from simply finetuning them on a dataset of target task demonstrations [8, 26, 52], or mixing the outputs of the pretrained and fine-tuned policies [5], to alternative approaches like online and offline reinforcement learning [38, 19, 70, 18, 72, 65], retrieval-based adaptation [34, 13] or in-context improvement [14, 51]. In this work, we focus on the most 

|LLM B|ackbone|Action<br>Expert|
|---|---|---|
|Image<br>Enc.|Language<br>Instruction|a|


**Figure 2:** State-of-the-art generalist policies typically consist of a vision encoder, language model backbone, and action decoder (“action expert”). 

common setting, in which policies are finetuned on a target task using a small dataset of demonstrations. Various finetuning approaches have been proposed in the literature, from simply adapting the full network on the target dataset [26, 8], to mixing target and pretraining data [9, 15, 12], or freezing parts of the network during finetuning [33, 30, 49, 66]. While such approaches may prove effective for learning robust target task policies in “large-data” finetuning regimes with tens to hundreds of hours of finetuning data [7, 21, 9, 10], they often struggle to retain the generality of the pretrained policy in more common, accessible settings with 100 or less target task demonstrations. In such scenarios, finetuned policies often struggle to generalize meaningfully beyond the 

2 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

conditions seen in the finetuning dataset [71], even if the base policy had broad generalization capabilities. In this work, we propose a simple alternative for robust policy finetuning in low-data regimes. Instead of directly using the finetuned policy, we observe that merging the pretrained and finetuned policy checkpoints _in weight space_ leads to significantly improved generalization on target tasks at no additional training or inference cost. 

**Model parameter merging.** Our approach is inspired by work on model weight merging in vision and language domains [57, 67, 68, 42, 36, 22, 39, 69, 23]. These works demonstrate that interpolating between the weights of multiple finetuned models, or between pretrained and finetuned models, can combine their capabilities or make them more robust to distribution shifts [62, 61, 20, 43, 37]. To our knowledge, our work is the first to demonstrate the effectiveness of model merging in the context of generalist robot policies, and combining it with co-training to further improve upon vanilla model merging. Additionally, we analyze the importance of the generality of the base model, as well as the importance of different parameter groups in vision-language-action (VLA) policies and find it often sufficient to only merge parameters from the language model backbone. 

**Continual learning.** The focus of our work is on improving generalization of finetuned policies on a target task. However, in addition, we find that our model merging approach is also effective at retaining the generalist policy’s performance on tasks from the pretraining distribution. As such, we demonstrate that it can be used to sequentially merge multiple skills into a single pretrained policy checkpoint while retaining generality. This setting is typically referred to as _continual learning_ and there is a large body of literature, both outside [28, 47, 35, 58] and within robotics [29, 4, 55, 40, 31, 60]. Our work differs from this line of research in that we aim to inherit and pass on the generalization ability of a pretrained model to learn new tasks robustly, whereas continual learning methods generally focus on not forgetting old skills seen during the agent’s lifetime. 

## **3. Problem Setting** 

The goal of our work is to develop an approach for _robust_ policy finetuning, in which a generalist policy is finetuned to a new target task and generalizes to _unseen variations of that target task_ , like new object instances, viewpoints, scenes, or lighting conditions, while also preserving its generalist abilities. Formally, let  denote an environment,  denote observations (e.g., images, proprioception),  actions, and  task specifications (e.g., language prompts). A policy 𝜋𝜃(𝑎𝑡 ∣𝑠𝑡, 𝑇) maps state 𝑠𝑡 ∈  and task 𝑇∈  to a distribution over actions 𝑎𝑡 ∈ . We assume access to a pretrained generalist policy 𝜋𝜃pre, trained on a diverse set of tasks and environments, and denote its training data as Dpre. For a new _target task_ 𝑇𝜂 (e.g., “wipe the whiteboard”), we assume access to a demonstration dataset D𝜂 = { (𝑠𝑡<sup>(𝑖), 𝑎(𝑖)</sup> 𝑡<sup>, 𝑇𝜂)</sup> }. In general, we assume that D𝜂 is collected in a single (or small number of) environment 𝜂, and |D𝜂| ≪|Dpre|. 

**Behavioral cloning & finetuning.** For adapting the policy to the target task, we consider the standard behavioral cloning (BC) objective. For policy parameterization 𝜋𝜃 and demonstration dataset D, the training objective is: 


We consider two main finetuning settings: **Task-finetuning (task-FT)** , in which we train exclusively on the target dataset D𝜂 (e.g., because pretraining data is proprietary); and **co-finetuning (co-FT)** , where we finetune on a mix of D𝜂 and Dpre to help preserve pretraining capabilities (e.g., in case of open-source pretraining datasets). 

**Evaluation.** In practice, when we finetune a policy, we don’t simply want it to work only in the setting where we collected the finetuning demonstration, but for it to complete the demonstrated task in a variety of contexts or scenes. Current methods often fail in this regime because they overfit heavily to the small finetuning dataset. Therefore, to assess overfitting and robustness of the finetuned policy, we evaluate the performance of finetuned policies in the following three settings: 

1. **Target task in-distribution (ID)** : measures policy performance on the target task 𝑇𝜂, with objects, initial poses/layouts, camera placements, lighting conditions, and backgrounds _observed_ in the finetuning dataset D𝜂. 

3 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 


**Figure 3:** Example filmstrips of the in-distribution (ID) tasks and out-of-distribution (OOD) tasks from DROID robot experiments in Section 6. 

2. **Target task out-of-distribution (OOD)** : measures the performance on the target task, in scenarios _not_ observed in the finetuning dataset, such as changes in object instances, backgrounds, lighting conditions and camera angles. This measures the _robustness_ of the finetuned policy. 

3. **Generalist tasks** : measures policy performance on tasks _other than the target task_ , but for which we would expect the generalist policy 𝜋𝜃pre to perform reasonably. This measures how well the finetuned policy retains _generalist_ capabilities from the pretrained model. 

## **4. Challenges of Finetuning Generalist Robot Policies** 

To understand the challenges of robust finetuning of generalist robot policies, we start by evaluating the standard finetuning approach. We evaluate finetuning the full model (Task-FT) in LIBERO [31], a multi-task robotic manipulation simulator containing 130 total tasks. Concretely, given a state-of-the-art vision-language-action policy [8], pretrained on demonstration data from 117 tasks from the LIBERO-{90, goal, spatial, object} suites, we finetune it to a new LIBERO target task. We consider three target tasks from LIBERO-10: `mugs-on-plates` , `pot-on-stove` , and `items-into-basket` . We then measure performance in the three scenarios introduced in Section 3: ID, OOD, and Generalist. For OOD evaluations, we alter object positions, add new distractors, and change backgrounds. Generalist evaluations are performed over 20 tasks from the pretraining dataset. More details about the OOD evaluations in Section 6.1 and Section A.7. 

Fig. 4 shows the performance of Task-FT on three types of evaluations. We find a clear tradeoff between generalist and ID target task performance: though the model gets better in ID target task after fine-tuning, it increasingly loses its generalist capabilities. Additionally, when the model is finetuned for too long, it even starts losing performance for ID tasks. Both of these phenomena are likely because the model has severely overfitted to the small demonstration dataset, and is unable to do other tasks or recover from small mistakes unseen in the dataset. More importantly, one would hope that the finetuned model can generalize to small variations of the target task not seen in the finetuning dataset, since the pretrained model contains knowledge for such generalization. However, all tested checkpoints above show a large gap between ID and OOD performance, showing that the model is not able to complete the target task when there are small variations present. Section A.4 shows that even with careful tuning of learning rate and number of gradient steps, such overfitting still exists. 

4 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 


**Figure 4: The standard approach for policy finetuning often overfits.** As the policy is trained for more gradient steps, it performs worse on tasks other than the new target task (“ **GENERALIST** ”) and may even start to degrade on scenarios seen in the finetuning data (“ **ID** ”). Most importantly, it is not able to transfer the generality of a base policy to do well under variations of the target task (new object positions, instances, viewpoints; “ **OOD** ”). 

## **5. RETAIN: Robust Policy Finetuning via Model Merging** 

The previous section illustrates that standard finetuning approaches cause the model to quickly forget generalist capabilities, and fail to transfer the pretrained policy’s robustness to the target task. To address these issues, we propose RETAIN ( **R** obust fin **E** -tuning wi **T** h p **A** rameter merg **IN** g), a simple approach for robust finetuning of robot policies. Given pretrained policy weights 𝜃pre and finetuned policy weights 𝜃ft, we propose linearly interpolating 𝜃pre and 𝜃ft to obtain a final policy checkpoint,̃ 𝜃. So, RETAIN produces a final policy 𝜋̃𝜃 by setting: 


for 𝛼, a tunable merging weight. Though surprisingly simple, as we will see, this weight space “merging” of pretrained and finetuned checkpoints leads to significantly improved OOD performance on the target task, while retaining generalist policy capabilities (see Section 6.5). While weight merging itself already improves the policy’s ability to retain and pass on generalist abilities, in the following we introduce two further improvements: utilizing the pretraining data Dpre (in settings where it is available) to augment our task data D𝜂 during finetuning, and merging 𝜃pre and 𝜃ft in a modality-specific manner. We introduce these two methods below, and show how RETAIN can also enable _continual_ adaptation to new tasks. 

### **_5.1. Co-Finetuning_** 

In Eq. (2), the finetuned policy weight 𝜃ft can either be optimized via task-finetuning or co-finetuning, as described in Section 3. In situations where the pretraining dataset, or a subset of it, is available, we can finetune the policy weight on a mix of Dpre and D𝜂. Such co-finetuning usually leads to better retention of generalist abilities after finetuning [9, 15, 12]. We find that we can use model merging together with co-finetuning, which we will refer to as RETAIN-co-FT, to enable greater generalization on the target task and better preserve generalist knowledge than model merging with task fine-tuning, which we call RETAIN-task-FT (see Section 6). 

### **_5.2. Modality-Specific Merging_** 

While prior works have explored model-merging in the context of uni-modal vision or language models [36, 22, 39, 69, 23, 56], robotics is fundamentally a multi-modal problem. Modern generalist robot policies are typically instantiated as vision-language-action (VLA) models (see Fig. 2) that consist of a vision encoder (𝑣), a large language model backbone (𝑙), and often an “action expert” module that decodes robot action outputs (𝑎). We find that, in such multi-modal settings, it can be advantageous to use separate merging weights for different modalities. As such, we can expand the RETAIN merging objective to: 


5 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

We show in Section 6.4 that, somewhat surprisingly, it often suffices to only merge the language model parameters. 

### **_5.3. Continual Task Adaptation_** 

We observe that RETAIN enables finetuned policies to retain the generalist capabilities of the pretrained policy. As such, we can use RETAIN to _sequentially_ add tasks into a pretrained checkpoint by iteratively merging finetuned weights into the base model and continuing to finetune from the merged checkpoint (see Fig. 5). Formally, for a _sequence_ of target tasks 


**Figure 5: RETAIN enables continual merging of new skills into generalist policy backbones.** 

𝑇𝜂1, … 𝑇𝜂𝑁 we can compute a sequence of adapted RETAIN policies that accumulate new task capabilities as: 


where 𝜃ft,n denotes the parameters finetuned on the 𝑛th task. 

## **6. Experiments** 

The goal of our experiments is to evaluate RETAIN’s ability to _robustly_ finetune generalist policies to new tasks, i.e., to broaden the finetuned policy’s ability to generalize to unseen settings in the target task. Concretely, we aim to answer the following questions: **(1)** Can RETAIN learn a new skill robustly and generalize more broadly to variations of the skill than prior finetuning approaches? **(2)** What factors influence whether we can effectively merge pretrained and finetuned policy? **(3)** Can RETAIN enable continual merging of a sequence of several skills into the pretrained policies? 

### **_6.1. Experimental Setup_** 


LIBERO items-into-basket 

**Figure 6:** We evaluate policy finetuning on two real-world DROID finetuning tasks ( **left** , **middle** ) and three simulated LIBERO finetuning tasks ( **right** , only one visualized here). In each task, we collect a modest number of demonstrations (50–100) in a comparatively narrow setting ( **blue** ), but evaluate on a much broader set of variations for the same task ( **yellow** ), including variations to scene, object instances, initial positions, lighting conditions, distractors, and viewpoints. This tests transfer of the generalization ability of the pretrained policy to the target task. Example trajectories in Fig. 3. 

**Environments and tasks.** We evaluate RETAIN in real-world and simulated finetuning settings (see Fig. 6). For our **real-world experiments** , we use the DROID robot setup [25], which consists of a 7-DoF Franka robot arm with a wrist-mounted camera and at least one external camera. We design two challenging fine-tuning tasks: wiping the whiteboard with an eraser (which we call `whiteboard` ) and putting the dishes into a drying rack (which we call `plates` ). For both tasks, we collect roughly 50 and 100 demonstrations, respectively. All demonstrations are collected in a single environment with minor position variations (see Fig. 6, blue), to mirror the variation in typical narrow-data finetuning regimes [71]. We test generalization of the finetuned 

6 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

policies on a much broader set of target environments (Fig. 6, yellow), which include unseen backgrounds, object instances, and camera views. See example task trajectories in Fig. 3. For our **simulated experiments** , we use the LIBERO simulation environment [31]. We finetune policies pretrained on the LIBERO-{object, spatial, goal, 90} datasets to three new tasks from the LIBERO-10 suite: `pot-on-stove` , `mugs-on-plates` , and `items-into-basket` . We use ≈45 demonstrations per task, obtained after filtering and preprocessing the 50 demos provided with the LIBERO simulator, which only contain minor variations to the initial positions of each object, and again test on a much broader distribution of initial positions, backgrounds, and additional distractors (see Fig. 6, right). More setup details can be found in Section A.6 and Section A.7. 

For both LIBERO and DROID, we evaluate our method and baselines on three different OOD scenes. To pick the merging coefficient 𝛼, we use one OOD scene as the “validation” scene, and tune the hyperparameter 𝛼 for best performance on that validation scene. We only use 𝛼∈{0.25, 0.5, 0.75} in DROID. Then, we use the rest of the OOD scenes as the “test” scenes without any hyperparameter tuning. 

**Pretrained policies.** We use state-of-the-art pretrained robot policies for our experiments. For our real-world DROID experiments, we use 𝜋0-FAST-DROID [45], the best open-source DROID policy at the time of our experiments as judged by the RoboArena policy ranking [3]<sup>0</sup> . For LIBERO, we use a 𝜋0 [7] policy fine-tuned on the LIBERO-{object, spatial, goal, 90} datasets as our pretrained policy. 𝜋0 is a generalist policy with a flow-based action expert, while 𝜋0-FAST-DROID is an autoregressive transformer based on next-token prediction. 

**Comparisons.** We compare against prior methods, including those that incorporate regularization techniques to reduce overfitting, in the robust finetuning setting. Specifically, we compare our approach, RETAIN, to: “ **TaskFT** ”, which finetunes the pretrained policy only on the target task dataset using behavioral cloning (Eq. (1)) [6, 8]; “ **Co-FT** ”, which finetunes on a mix of pretraining and target task data to reduce overfitting [15, 12], “ **LoRA** ”, which uses low-rank adaptation [17] during finetuning to retain more of the pretraining capabilities [41, 26]; “ **Freeze-FT** ”, which freezes the language model backbone during finetuning and only updates the vision encoder, and, in the case of 𝜋0, the action expert output head, following similar approaches in prior work, e.g., Kim et al. [26], Zhang et al. [71]; **Scratch** , which learns a policy from scratch on the demonstration dataset instead of finetuning a generalist policy. For more details about the policy classes and implementations, see Section A.9. Section A.8 details our choice of hyperparameters and tuning process. 

### **_6.2. RETAIN Learn New Skills Robustly and Generalize More Broadly_** 

**RETAIN solves the finetuning task in a broader range of variations.** We compare RETAIN with the aforementioned baseline methods when finetuning to a new task, and show the performance on the three types of evaluations. Fig. 7 shows results on two DROID environments, and Fig. 8 shows the average of three LIBERO environments. The ID and OOD evaluations show how well a method learns to do the new skill: ID evaluations show whether the method learned to fit the demonstration dataset exactly, and OOD evaluations assess whether the method has learned to generalize to the same task exhibiting variations not seen in the finetuning dataset. The OOD (val) scenes show “the upper bound” in performance when 𝛼 is allowed to be tuned slightly, while the OOD (test) scenes show the performance with no tuning. 

In real-world **DROID environments (Fig. 7)** , all methods perform much better on ID evaluations after finetuning, showing that the policy has adapted to the new task in the exact same context as the demonstration dataset. On ID evaluations, methods that use regularization, such as LoRA and Co-FT, perform slightly worse on `whiteboard` , likely because they are too constrained to adapt well to the new task. On OOD (test) evaluations, baseline finetuning methods perform significantly worse: while they can complete the new task with 70 −80% success rate in the ID setting, they have 30 −50% success rate on average in the OOD setting. This shows that the baseline methods are very sensitive to small variations (such as object change, location change, scene change) and cannot generalize to perform well. In comparison, both RETAIN-task-FT and RETAIN-co-FT perform much better, achieving more than 60% on `plates` and close to 80% on `whiteboard` OOD evaluation. Note that 

> 0The current strongest policy, 𝜋0.5 [21], was only open-sourced after our experiments. We look forward to testing RETAIN on 𝜋0.5 in the future. 

7 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 


**Figure 7:** RETAIN results on two DROID tasks, `whiteboard` (top) and `plates` (bottom). **RETAIN significantly outperform baselines in OOD evaluation and is competitive in ID evaluations** , showing that it is able to learn new skills robustly and can generalize to its variations using pretrained knowledge. **RETAIN also does best on generalist evaluations** , showing that it is best at retaining abilities to solve old tasks. We tune merging coefficient 𝛼 on one “val” OOD scene, and use the same value for two other “test” OOD scenes. 

this is similar to the policy’s ID evaluation performance on `whiteboard` , suggesting that RETAIN can perform a _generalized_ new skill with the same performance regardless of variations. Comparing the performance of OOD val and test sets, we see that the performance is sometimes not impacted ( `whiteboard` ) and sometimes better with slight hyperparameter tuning ( `plates` ). This shows that RETAIN is somewhat robust to hyperparameter, but can get even better when tuned for the particular OOD scene. Overall, in OOD evaluations, RETAIN enables the policy to outperform both the base model and other finetuned models. 


**Figure 8:** RETAIN results averaged over the three LIBERO tasks. Similar trend as Fig. 7. 

In **LIBERO environments (Fig. 8)** , all methods exhibit trends similar to those in DROID environments. Since the LIBERO simulation is a much easier task than real world robotic tasks, certain baseline fine-tuning methods achieve near-perfect performance in ID evaluations. Under OOD evaluations, both RETAIN-task-FT and RETAIN-co-FT help improve the policy’s robustness to scene variations. We observe that the improvement in OOD performance over baselines such as Co-FT in LIBERO is smaller than that in DROID, and we attribute this to the lack of generalist capabilities of the base model. For DROID, the base model 𝜋0-FAST was trained on 76𝑘 diverse trajectories in 564 scenes, while the LIBERO base model is only trained on 5.3𝑘 trajectories in 117 scenes with fairly limited diversity. As such, the LIBERO base model contains much less generalist ability than the DROID base model. And as we will shown in Section 6.3, merging with a less general base model inherits less 

8 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

generalization power, giving less improvement under OOD evaluations. There is also a much bigger gap between val and test OOD scenes, because the different types of variations for each OOD scene has a different difficulty level for the limited generalist model in LIBERO. 

**RETAIN still performs well on tasks from the pretraining distribution.** As shown above in Section 6.2, RETAIN allows the model to _not_ overfit to the finetuning dataset and generalize to solve a broader distribution of the finetuning task. One natural question is whether RETAIN has overfit to the finetuning task distribution, and whether it can still solve tasks under the pretraining distribution. To evaluate retention of generalist skills, we evaluate RETAIN and baselines under our generalist evaluation scenes. For DROID, we evaluate on 44 different real-world tasks; for LIBERO, we evaluate on 20 random tasks in the LIBERO pretraining dataset (5 each from LIBERO-{object, spatial, goal, 90}). Fig. 7 and Fig. 8 (second subfig) show that RETAIN performs just as well as the pretrained model on generalist evaluations, showing that it has not lost its ability to solve old tasks from pretraining. RETAIN works even better when combined with co-finetuning, as discussed below. 

**Model merging performs better with co-finetuning.** In Fig. 7 and Fig. 8, RETAIN-co-FT outperforms RETAINtask-FT in all three evaluation settings in almost all tasks. RETAIN-co-FT is particularly effective at improving performance in generalist and OOD evaluation. In fact, we observe that co-FT almost always helps improve performance over task-FT in generalist evaluation, but not always in OOD evaluation. We hypothesize this is because co-finetuning and model merging play different roles in the regularization process: co-finetuning helps the finetuned model not overfit to the small target dataset by continuous training on pretraining data, but does not elicit pretrained knowledge to help generalization on the new task; on the other hand, model merging explicitly tries to elicit pretrained knowledge and combine it with finetuning knowledge in parameter space; however, doing so with a task-FT model is worse at keeping pretraining abilities because the task-FT model has overfitted to the target dataset. 

### **_6.3. RETAIN Scales with the Amount of Pretraining Data_** 

As we saw in Section 6.2, RETAIN is not only able to perform well on tasks from the pretraining distribution, but also solve broader variations of finetuning tasks, as if it “merged” the generalist ability of the pretrained model with the task specialization of the finetuned model. This begs the question: how well does RETAIN do when the pretrained model contains differing amounts of “generalist knowledge”, as induced by different amounts of pretraining data? To study how differing amounts of pretraining data affects RETAIN’s performance, we use the DROID dataset, containing a large quantity of diverse robot data. We consider three pretrained generalist VLA policies: (1) the public 𝜋0-FASTDROID checkpoint that is trained on all 


**Figure 9: RETAIN performs better on OOD tasks when the pretrained generalist policy is trained with more data** . DROID-Subset is trained with 20𝑘 episodes, DROID-All is all 75𝑘 episodes of DROID, while DROID-All+PI is trained with all of DROID plus even bigger datasets from Phyiscal Intelligence (PI) [45]. OOD performance is averaged across three scenes on `plates` . 

of DROID and a large repertoire of robot data from Physical Intelligence [45], (2) only trained on all of DROID, totaling 76𝑘 episodes, and (3) only trained on the subset of DROID collected at Berkeley and Stanford, totaling 20𝑘 episodes. All three policies are pretrained by taking roughly 1 epoch over the dataset, and finetuned on the `plates` task with the same hyperparameters. We then evaluate the three RETAIN-co-FT policies, each obtained by merging the respective pretrained policy with its finetuned counterpart, on ID and OOD scenes in Fig. 9. To account for the performance difference of the base policies, we report the success rate increase between RETAIN-co-FT and co-FT. In ID evaluations, policies trained with differing amount of data perform similarly. 

9 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

In OOD evaluations, more pretraining data leads to significantly better performance. This shows that RETAIN scales with the amount of pretraining data, and can better “transfer” generalist knowledge from the pretrained model to new scenes when the pretrained model is more general. In fact, the best performing model (DROID-ALL + PI) performs nearly as good on OOD evlauation as it does on ID evaluation, as shown in Fig. 15. 

### **_6.4. Analyzing the Importance of Merging Different Parameters in RETAIN_** 

In this section, we seek to build a mechanistic understanding of how the merging coefficient impacts the performance of merged models. To begin, we try understanding how changing the coefficient 𝛼 in Eq. (2), when all parameters are interpolated with the same value, impacts performance. In Fig. 10, we plot OOD performance against 𝛼 averaged across three LIBERO tasks, each with three types of OOD scenes. 𝛼= 0 corresponds to the pretrained model, and 𝛼= 1 corresponds to the co-finetuned model without merging. Model merging (0 < 𝛼< 1) helps improve model performance in OOD evaluation, as long as the merged model is not too deviated from the finetuned model. When the 


**Figure 10: Left:** Illustration of three different kinds of OOD scenes we consider in LIBERO, shown in `pot-on-stove` . **Right:** Plot shows how the OOD performance on three types of OOD variations changes with the merging parameter 𝛼, averaged across three LIBERO environments. 

merged model is too similar to the pretrained model, it does not have enough task-specific knowledge, and has near 0 performance. And as we have shown in Fig. 8, the model with the 𝛼 value that has the best OOD performance is also comparable to baselines in ID evaluations and better at generalist evaluations. 

Next, we explore whether merging different parameters with different coefficients has an impact on the merged policy’s performance. Specifically, we consider modality-specific merging in the context of VLA policies. As explained in Section 5.2, we use separate coefficients for merging the parameters of the vision encoder, language model, and action expert. Fig. 11 (left) shows the OOD performance of the merged model as we vary 𝛼𝑣, 𝛼𝑙, and 𝛼𝑎 from 0 to 1 on the `mugs-on-plates` task: dark colors represent low OOD performance, and light colors represent high OOD performance. Observe that the cube has the largest color gradient in the 𝛼𝑙 direction: this shows that the language model parameters have the most influence on performance. Interestingly, we see that 𝛼𝑙 = 1 does not yield the best performance; the best performing models has 𝛼𝑙 = 0.8 (see the highlighted plane at 𝛼𝑙 = 0.8 in Fig. 11 (left) for the brightest colored dots). Next, to understand how 𝛼𝑣 and 𝛼𝑎 impact performance, we plot in Fig. 11 (middle) the change in OOD performance with these two coefficients when averaged over 𝛼𝑙. This 2D plot essentially squashes the 3D cube plot in the language direction. Unlike the behavior of 𝛼𝑙, higher values of 𝛼𝑎 and 𝛼𝑣 lead to better performance; the best performance is achieved at 𝛼𝑎 = 𝛼𝑣 = 1. 

These results suggest that during model merging, it may suffice to only merge the parameters of the language model backbone (𝛼𝑙 < 1) and leave the parameters in the vision encoder and the action expert set to the parameter values in the finetuned model (𝛼𝑎 = 𝛼𝑣 = 1). To validate this hypothesis, we compare the OOD performance of merging all parameters with RETAIN (0 < 𝛼< 1) to only merging language model parameters. In Fig. 11 (right), we plot the performance of the two merging schemes over three different LIBERO tasks, each averaged over three types of OOD scenes. Somewhat surprisingly, the result shows that the two merging schemes achieve very similar performance, indicating that we only need to merge parameters from the language model backbone (instead of all parameters) to inherit the model’s generalization ability and robustness to variations in the target scene. To the best of our knowledge, this is the first work to demonstrate the importance of different parameter groups for model merging in VLAs. We believe this may inform future work on finetuning VLAs, providing insight on which parameter groups are most critical. 

10 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 


**Figure 11: Language model parameters have the most influence in modality-specific merging. Left** : Merged model’s OOD performance over a grid search of 𝛼𝑎, 𝛼𝑣, 𝛼𝑙, and 𝛼𝑙 has the most impact. **Middle** : OOD performance of 𝛼𝑎 and 𝛼𝑣 averaged over different 𝛼𝑙, and higher values are better. **Right** : Merging only the language model parameters (𝛼𝑎 = 𝛼𝑣 = 1, 𝛼𝑙 < 1) performs similarly to merging all parameters. 

### **_6.5. RETAIN Enables Robust Learning of Multiple Skills Sequentially_** 

Finally, we test whether RETAIN can enable learning multiple skills in sequence, as described in Section 5.3, and still retain its generalist abilities. We consider learning the two DROID tasks sequentially, first finetuning on `plates` , and then using this as an initialization to finetune on `whiteboard` . As outlined in Section 5.3, RETAIN uses the merged model from the first stage of finetuning as initialization for the second finetuning stage. During evaluation time, we test whether the final policy, after it has sequentially been trained on both tasks, can solve both tasks un- **Figure 12: RETAIN enables continual adaptation to a** der ID and OOD evaluations. We compare against **sequence of two skills.** Evaluation results show the perco-FT in the sequential learning setting, since it is formance of the final policy after sequentially finetuning on two tasks, evaluated on different scenes. OOD performance the strongest baseline at retaining prior knowledge in single-task finetuning (see Fig. 7). Fig. 12 shows the averaged across two test scenes. performance of the two policies on the two tasks under both ID and OOD settings. We also plot the performance of these two methods in the single-task finetuning setting in dashed lines. These two comparisons serve as the oracle performance ceiling that we expect on these tasks, and is not meant as baselines for the sequential setting. When evaluated on the first task, `plates` , RETAIN does much better than co-FT in the sequential setting, showing that it is better at retaining its ability to solve the first task even after a second round of finetuning. When evaluated on the second task, `whiteboard` , RETAIN is also better than co-FT under ID evaluations. RETAIN outperforms co-FT in the sequential setting under all tasks and evaluation types. 

**Figure 12: RETAIN enables continual adaptation to a sequence of two skills.** Evaluation results show the performance of the final policy after sequentially finetuning on two tasks, evaluated on different scenes. OOD performance averaged across two test scenes. 

## **7. Conclusion** 

We present a simple yet effective method, RETAIN, for robust finetuning of generalist robot policies. We show that by simply interpolating the weights of a generalist policy before and after it is finetuned on a target task, we can “merge” the generalization ability of the base policy with the task-expertise of the finetuned policy. Through comprehensive real world and simulated experiments, we show that RETAIN can help the policy generalize significantly better to variations of the target task unseen in the demonstration, and is able to retain performance on general tasks. We also apply RETAIN to sequentially acquire new skills in a lifelong learning setting, and find that it can robustly “merge” skills into a single policy. 

## **8. Limitations** 

While we empirically verified that RETAIN works exceptionally well in helping the finetuned model generalize to out-of-distribution variations of the task, we don’t understand the full scope of the reasons why model 

11 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

parameter merging was able to lead to such generalization. This is an interesting area for future work. We have included some discussion in Section A.10 of some hypothesess and why previous work found model parameter merging effective for vision and language tasks. Additionally, RETAIN involves an important hyperparameter, the merginge coefficient, that can be tuned. While we find in our real world experiments that RETAIN is robust to different values of this parameter, slight tuning of this parameter is needed. One avenue of future work is determining a good heuristic of how to choose this value. 

## **9. Acknowledgements** 

This research was partly supported by ONR N00014-25-1-2060. This research used the Savio computational cluster resource provided by the Berkeley Research Computing program at UC Berkeley. We would also like to thank the anonymous ICLR reviewers for thoughtful comments and suggestions. 

## **References** 

- [1] Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Kevin Black, Ken Conley, Grace Connors, James Darpinian, Karan Dhabalia, Jared DiCarlo, Danny Driess, et al. 𝜋0.6<sup>∗: a vla that learns from experience.</sup><sup>_arXiv preprint_</sup> _arXiv:2511.14759_ , 2025. 

- [2] Rohan Anil, Andrew M Dai, Orhan Firat, Melvin Johnson, Dmitry Lepikhin, Alexandre Passos, Siamak Shakeri, Emanuel Taropa, Paige Bailey, Zhifeng Chen, et al. Palm 2 technical report. _arXiv preprint arXiv:2305.10403_ , 2023. 

- [3] Pranav Atreya, Karl Pertsch, Tony Lee, Moo Jin Kim, Arhan Jain, Artur Kuramshin, Clemens Eppner, Cyrus Neary, Edward Hu, Fabio Ramos, et al. Roboarena: Distributed real-world evaluation of generalist robot policies. _arXiv preprint arXiv:2506.18123_ , 2025. 

- [4] Sayantan Auddy, Jakob Hollenstein, Matteo Saveriano, Antonio Rodríguez-Sánchez, and Justus Piater. Continual learning from demonstration of robotics skills. _Robotics and Autonomous Systems_ , 165:104427, 2023. 

- [5] Marco Bagatella, Jonas Hübotter, Georg Martius, and Andreas Krause. Active fine-tuning of multi-task policies. In _Forty-second International Conference on Machine Learning_ , 2025. 

- [6] Michael Bain and Claude Sammut. A framework for behavioural cloning. In _Machine intelligence 15_ , pages 103–129, 1995. 

- [7] Kevin Black, Mitsuhiko Nakamoto, Pranav Atreya, Homer Walke, Chelsea Finn, Aviral Kumar, and Sergey Levine. Zero-shot robotic manipulation with pretrained image-editing diffusion models. _arXiv preprint arXiv:2310.10639_ , 2023. 

- [8] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. 𝜋0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [9] Konstantinos Bousmalis, Giulia Vezzani, Dushyant Rao, Coline Devin, Alex X Lee, Maria Bauza, Todor Davchev, Yuxiang Zhou, Agrim Gupta, Akhil Raju, et al. Robocat: A self-improving foundation agent for robotic manipulation. _arXiv preprint arXiv:2306.11706_ , 2023. 

- [10] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 

12 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

- [11] Open X-Embodiment Collaboration, Abhishek Padalkar, Acorn Pooley, Ajinkya Jain, Alex Bewley, Alex Herzog, Alex Irpan, Alexander Khazatsky, Anant Rai, Anikait Singh, Anthony Brohan, Antonin Raffin, Ayzaan Wahid, Ben Burgess-Limerick, Beomjoon Kim, Bernhard Schölkopf, Brian Ichter, Cewu Lu, Charles Xu, Chelsea Finn, Chenfeng Xu, Cheng Chi, Chenguang Huang, Christine Chan, Chuer Pan, Chuyuan Fu, Coline Devin, Danny Driess, Deepak Pathak, Dhruv Shah, Dieter Büchler, Dmitry Kalashnikov, Dorsa Sadigh, Edward Johns, Federico Ceola, Fei Xia, Freek Stulp, Gaoyue Zhou, Gaurav S. Sukhatme, Gautam Salhotra, Ge Yan, Giulio Schiavi, Hao Su, Hao-Shu Fang, Haochen Shi, Heni Ben Amor, Henrik I Christensen, Hiroki Furuta, Homer Walke, Hongjie Fang, Igor Mordatch, Ilija Radosavovic, Isabel Leal, Jacky Liang, Jaehyung Kim, Jan Schneider, Jasmine Hsu, Jeannette Bohg, Jeffrey Bingham, Jiajun Wu, Jialin Wu, Jianlan Luo, Jiayuan Gu, Jie Tan, Jihoon Oh, Jitendra Malik, Jonathan Tompson, Jonathan Yang, Joseph J. Lim, João Silvério, Junhyek Han, Kanishka Rao, Karl Pertsch, Karol Hausman, Keegan Go, Keerthana Gopalakrishnan, Ken Goldberg, Kendra Byrne, Kenneth Oslund, Kento Kawaharazuka, Kevin Zhang, Keyvan Majd, Krishan Rana, Krishnan Srinivasan, Lawrence Yunliang Chen, Lerrel Pinto, Liam Tan, Lionel Ott, Lisa Lee, Masayoshi Tomizuka, Maximilian Du, Michael Ahn, Mingtong Zhang, Mingyu Ding, Mohan Kumar Srirama, Mohit Sharma, Moo Jin Kim, Naoaki Kanazawa, Nicklas Hansen, Nicolas Heess, Nikhil J Joshi, Niko Suenderhauf, Norman Di Palo, Nur Muhammad Mahi Shafiullah, Oier Mees, Oliver Kroemer, Pannag R Sanketi, Paul Wohlhart, Peng Xu, Pierre Sermanet, Priya Sundaresan, Quan Vuong, Rafael Rafailov, Ran Tian, Ria Doshi, Roberto Martín-Martín, Russell Mendonca, Rutav Shah, Ryan Hoque, Ryan Julian, Samuel Bustamante, Sean Kirmani, Sergey Levine, Sherry Moore, Shikhar Bahl, Shivin Dass, Shuran Song, Sichun Xu, Siddhant Haldar, Simeon Adebola, Simon Guist, Soroush Nasiriany, Stefan Schaal, Stefan Welker, Stephen Tian, Sudeep Dasari, Suneel Belkhale, Takayuki Osa, Tatsuya Harada, Tatsuya Matsushima, Ted Xiao, Tianhe Yu, Tianli Ding, Todor Davchev, Tony Z. Zhao, Travis Armstrong, Trevor Darrell, Vidhi Jain, Vincent Vanhoucke, Wei Zhan, Wenxuan Zhou, Wolfram Burgard, Xi Chen, Xiaolong Wang, Xinghao Zhu, Xuanlin Li, Yao Lu, Yevgen Chebotar, Yifan Zhou, Yifeng Zhu, Ying Xu, Yixuan Wang, Yonatan Bisk, Yoonyoung Cho, Youngwoon Lee, Yuchen Cui, Yueh hua Wu, Yujin Tang, Yuke Zhu, Yunzhu Li, Yusuke Iwasawa, Yutaka Matsuo, Zhuo Xu, and Zichen Jeff Cui. Open X-Embodiment: Robotic learning datasets and RT-X models. https://arxiv.org/abs/2310.08864, 2023. 

- [12] Shivin Dass, Alaa Khaddaj, Logan Engstrom, Aleksander Madry, Andrew Ilyas, and Roberto Martín-Martín. Datamil: Selecting data for robot imitation learning with datamodels. _arXiv preprint arXiv:2505.09603_ , 2025. 

- [13] Norman Di Palo and Edward Johns. Dinobot: Robot manipulation via retrieval and alignment with vision foundation models. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 2798– 2805. IEEE, 2024. 

- [14] Letian Fu, Huang Huang, Gaurav Datta, Lawrence Yunliang Chen, William Chung-Ho Panitch, Fangchen Liu, Hui Li, and Ken Goldberg. In-context imitation learning via next-token prediction. _arXiv preprint arXiv:2408.15980_ , 2024. 

- [15] Zipeng Fu, Tony Z Zhao, and Chelsea Finn. Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation. _arXiv preprint arXiv:2401.02117_ , 2024. 

- [16] Jensen Gao, Suneel Belkhale, Sudeep Dasari, Ashwin Balakrishna, Dhruv Shah, and Dorsa Sadigh. A taxonomy for evaluating generalist robot policies. _arXiv preprint arXiv:2503.01238_ , 2025. 

- [17] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. _ICLR_ , 1(2):3, 2022. 

- [18] Jiaheng Hu, Rose Hendrix, Ali Farhadi, Aniruddha Kembhavi, Roberto Martín-Martín, Peter Stone, KuoHao Zeng, and Kiana Ehsani. Flare: Achieving masterful and adaptive robot policies with large-scale reinforcement learning fine-tuning. _arXiv preprint arXiv:2409.16578_ , 2024. 

13 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

- [19] Dongchi Huang, Zhirui Fang, Tianle Zhang, Yihang Li, Lin Zhao, and Chunhe Xia. Co-rft: Efficient finetuning of vision-language-action models through chunked offline reinforcement learning. _arXiv preprint arXiv:2508.02219_ , 2025. 

- [20] Gabriel Ilharco, Mitchell Wortsman, Samir Yitzhak Gadre, Shuran Song, Hannaneh Hajishirzi, Simon Kornblith, Ali Farhadi, and Ludwig Schmidt. Patching open-vocabulary models by interpolating weights. _Advances in Neural Information Processing Systems_ , 35:29262–29277, 2022. 

- [21] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. 𝜋0. 5: a vision-language-action model with open-world generalization, 2025. _URL https://arxiv. org/abs/2504.16054_ , 1(2):3. 

- [22] Dong-Hwan Jang, Sangdoo Yun, and Dongyoon Han. Model stock: All we need is just a few fine-tuned models. In _European Conference on Computer Vision_ , pages 207–223. Springer, 2024. 

- [23] Xisen Jin, Xiang Ren, Daniel Preotiuc-Pietro, and Pengxiang Cheng. Dataless knowledge fusion by merging weights of language models. _arXiv preprint arXiv:2212.09849_ , 2022. 

- [24] Christos Kaplanis, Murray Shanahan, and Claudia Clopath. Policy consolidation for continual reinforcement learning. _arXiv preprint arXiv:1902.00255_ , 2019. 

- [25] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 

- [26] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [27] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- [28] James Kirkpatrick, Razvan Pascanu, Neil Rabinowitz, Joel Veness, Guillaume Desjardins, Andrei A Rusu, Kieran Milan, John Quan, Tiago Ramalho, Agnieszka Grabska-Barwinska, et al. Overcoming catastrophic forgetting in neural networks. _Proceedings of the national academy of sciences_ , 114(13):3521–3526, 2017. 

- [29] Timothée Lesort, Vincenzo Lomonaco, Andrei Stoian, Davide Maltoni, David Filliat, and Natalia DíazRodríguez. Continual learning for robotics: Definition, framework, learning strategies, opportunities and challenges. _Information fusion_ , 58:52–68, 2020. 

- [30] Anthony Liang, Ishika Singh, Karl Pertsch, and Jesse Thomason. Transformer adapters for robot learning. In _CoRL 2022 Workshop on Pre-training Robot Learning_ , 2022. 

- [31] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36, 2024. 

- [32] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 

- [33] Zuxin Liu, Jesse Zhang, Kavosh Asadi, Yao Liu, Ding Zhao, Shoham Sabach, and Rasool Fakoor. Tail: Task-specific adapters for imitation learning with large pretrained models. _arXiv preprint arXiv:2310.05905_ , 2023. 

- [34] Yayu Long, Kewei Chen, Long Jin, and Mingsheng Shang. Drae: Dynamic retrieval-augmented expert networks for lifelong learning and task adaptation in robotics. _arXiv preprint arXiv:2507.04661_ , 2025. 

14 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

- [35] David Lopez-Paz and Marc’Aurelio Ranzato. Gradient episodic memory for continual learning. _Advances in neural information processing systems_ , 30, 2017. 

- [36] Wei Lu, Rachel K Luu, and Markus J Buehler. Fine-tuning large language models for domain adaptation: Exploration of training strategies, scaling, model merging and synergistic capabilities. _npj Computational Materials_ , 11(1):84, 2025. 

- [37] Davide Marincione, Donato Crisostomi, Roberto Dessi, Emanuele Rodolà, and Emanuele Rossi. Model merging improves zero-shot generalization in bioacoustic foundation models. _arXiv preprint arXiv:2511.05171_ , 2025. 

- [38] Max Sobol Mark, Tian Gao, Georgia Gabriela Sampaio, Mohan Kumar Srirama, Archit Sharma, Chelsea Finn, and Aviral Kumar. Policy agnostic rl: Offline rl and online rl fine-tuning of any class and backbone. _arXiv preprint arXiv:2412.06685_ , 2024. 

- [39] Michael S Matena and Colin A Raffel. Merging models with fisher-weighted averaging. _Advances in Neural Information Processing Systems_ , 35:17703–17716, 2022. 

- [40] Yuan Meng, Zhenshan Bing, Xiangtong Yao, Kejia Chen, Kai Huang, Yang Gao, Fuchun Sun, and Alois Knoll. Preserving and combining knowledge in robotic lifelong reinforcement learning. _Nature Machine Intelligence_ , pages 1–14, 2025. 

- [41] Marcel Mittenbuehler, Ahmed Hendawy, Carlo D’Eramo, and Georgia Chalvatzaki. Parameter-efficient tuning of pretrained visual-language models in multitask robot learning. In _CoRL 2023 Workshop on Learning Effective Abstractions for Planning (LEAP)_ , 2023. 

- [42] Anshul Nasery, Jonathan Hayase, Pang Wei Koh, and Sewoong Oh. Pleas-merging models with permutations and least squares. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 30493– 30502, 2025. 

- [43] Behnam Neyshabur, Hanie Sedghi, and Chiyuan Zhang. What is being transferred in transfer learning? _Advances in neural information processing systems_ , 33:512–523, 2020. 

- [44] NVIDIA, :, Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi "Jim" Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, Zhenyu Jiang, Jan Kautz, Kaushil Kundalia, Lawrence Lao, Zhiqi Li, Zongyu Lin, Kevin Lin, Guilin Liu, Edith Llontop, Loic Magne, Ajay Mandlekar, Avnish Narayan, Soroush Nasiriany, Scott Reed, You Liang Tan, Guanzhi Wang, Zu Wang, Jing Wang, Qi Wang, Jiannan Xiang, Yuqi Xie, Yinzhen Xu, Zhenjia Xu, Seonghyeon Ye, Zhiding Yu, Ao Zhang, Hao Zhang, Yizhou Zhao, Ruijie Zheng, and Yuke Zhu. Gr00t n1: An open foundation model for generalist humanoid robots, 2025. URL https://arxiv.org/abs/2503.14734. 

- [45] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- [46] Delin Qu, Haoming Song, Qizhi Chen, Zhaoqing Chen, Xianqiang Gao, Xinyi Ye, Qi Lv, Modi Shi, Guanghui Ren, Cheng Ruan, Maoqing Yao, Haoran Yang, Jiacheng Bao, Bin Zhao, and Dong Wang. Embodiedonevision: Interleaved vision-text-action pretraining for general robot control, 2025. URL https://arxiv.org/abs/2508.21112. 

- [47] Jonathan Schwarz, Wojciech Czarnecki, Jelena Luketina, Agnieszka Grabska-Barwinska, Yee Whye Teh, Razvan Pascanu, and Raia Hadsell. Progress & compress: A scalable framework for continual learning. In _International conference on machine learning_ , pages 4528–4537. PMLR, 2018. 

- [48] Dhruv Shah, Ajay Sridhar, Arjun Bhorkar, Noriaki Hirose, and Sergey Levine. Gnm: A general navigation model to drive any robot. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 7226–7233. IEEE, 2023. 

15 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

- [49] Mohit Sharma, Claudio Fantacci, Yuxiang Zhou, Skanda Koppula, Nicolas Heess, Jon Scholz, and Yusuf Aytar. Lossless adaptation of pretrained vision models for robotic manipulation. _arXiv preprint arXiv:2304.06600_ , 2023. 

- [50] Ajay Sridhar, Dhruv Shah, Catherine Glossop, and Sergey Levine. Nomad: Goal masked diffusion policies for navigation and exploration. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 63–70. IEEE, 2024. 

- [51] Kaustubh Sridhar, Souradeep Dutta, Dinesh Jayaraman, and Insup Lee. Ricl: Adding in-context adaptability to pre-trained vision-language-action models. _arXiv preprint arXiv:2508.02062_ , 2025. 

- [52] Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, et al. Gemini robotics: Bringing ai into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025. 

- [53] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- [54] Homer Rich Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, Philippe Hansen-Estruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pages 1723–1736. PMLR, 2023. 

- [55] Weikang Wan, Yifeng Zhu, Rutav Shah, and Yuke Zhu. Lotus: Continual imitation learning for robot manipulation through unsupervised skill discovery. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 537–544. IEEE, 2024. 

- [56] Ke Wang, Nikolaos Dimitriadis, Alessandro Favero, Guillermo Ortiz-Jimenez, Francois Fleuret, and Pascal Frossard. Lines: Post-training layer scaling prevents forgetting and enhances model merging. _arXiv preprint arXiv:2410.17146_ , 2024. 

- [57] Ke Wang, Nikolaos Dimitriadis, Guillermo Ortiz-Jimenez, François Fleuret, and Pascal Frossard. Localizing task information for improved model merging and compression. _arXiv preprint arXiv:2405.07813_ , 2024. 

- [58] Liyuan Wang, Xingxing Zhang, Hang Su, and Jun Zhu. A comprehensive survey of continual learning: Theory, method and application. _IEEE transactions on pattern analysis and machine intelligence_ , 46(8): 5362–5383, 2024. 

- [59] Yixiao Wang. Generalization capability for imitation learning. _arXiv preprint arXiv:2504.18538_ , 2025. 

- [60] Maciej Wołczyk, Michał Zając, Razvan Pascanu, Łukasz Kuciński, and Piotr Miłoś. Continual world: A robotic benchmark for continual reinforcement learning. _Advances in Neural Information Processing Systems_ , 34:28496–28510, 2021. 

- [61] Mitchell Wortsman, Gabriel Ilharco, Samir Ya Gadre, Rebecca Roelofs, Raphael Gontijo-Lopes, Ari S Morcos, Hongseok Namkoong, Ali Farhadi, Yair Carmon, Simon Kornblith, et al. Model soups: averaging weights of multiple fine-tuned models improves accuracy without increasing inference time. In _International conference on machine learning_ , pages 23965–23998. PMLR, 2022. 

- [62] Mitchell Wortsman, Gabriel Ilharco, Jong Wook Kim, Mike Li, Simon Kornblith, Rebecca Roelofs, Raphael Gontijo Lopes, Hannaneh Hajishirzi, Ali Farhadi, Hongseok Namkoong, et al. Robust fine-tuning of zero-shot models. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 7959–7971, 2022. 

16 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

- [63] Tian-Yu Xiang, Ao-Qun Jin, Xiao-Hu Zhou, Mei-Jiang Gui, Xiao-Liang Xie, Shi-Qi Liu, Shuang-Yi Wang, Sheng-Bin Duan, Fu-Chao Xie, Wen-Kai Wang, et al. Parallels between vla model post-training and human motor learning: Progress, challenges, and trends. _arXiv preprint arXiv:2506.20966_ , 2025. 

- [64] Fangzhou Xiong, Zhiyong Liu, Kaizhu Huang, Xu Yang, Hong Qiao, and Amir Hussain. Encoding primitives generation policy learning for robotic arm to overcome catastrophic forgetting in sequential multi-tasks learning. _Neural Networks_ , 129:163–173, 2020. 

- [65] Charles Xu, Qiyang Li, Jianlan Luo, and Sergey Levine. Rldg: Robotic generalist policy distillation via reinforcement learning. _arXiv preprint arXiv:2412.09858_ , 2024. 

- [66] Mengdi Xu, Yuchen Lu, Yikang Shen, Shun Zhang, Ding Zhao, and Chuang Gan. Hyper-decision transformer for efficient online policy adaptation. _arXiv preprint arXiv:2304.08487_ , 2023. 

- [67] Prateek Yadav, Derek Tam, Leshem Choshen, Colin A Raffel, and Mohit Bansal. Ties-merging: Resolving interference when merging models. _Advances in Neural Information Processing Systems_ , 36:7093–7115, 2023. 

- [68] Prateek Yadav, Tu Vu, Jonathan Lai, Alexandra Chronopoulou, Manaal Faruqui, Mohit Bansal, and Tsendsuren Munkhdalai. What matters for model merging at scale? _arXiv preprint arXiv:2410.03617_ , 2024. 

- [69] Enneng Yang, Zhenyi Wang, Li Shen, Shiwei Liu, Guibing Guo, Xingwei Wang, and Dacheng Tao. Adamerging: Adaptive model merging for multi-task learning. _arXiv preprint arXiv:2310.02575_ , 2023. 

- [70] Jingyun Yang, Max Sobol Mark, Brandon Vu, Archit Sharma, Jeannette Bohg, and Chelsea Finn. Robot fine-tuning made easy: Pre-training rewards and policies for autonomous real-world reinforcement learning. _arXiv preprint arXiv:2310.15145_ , 2023. 

- [71] Wenbo Zhang, Yang Li, Yanyuan Qiao, Siyuan Huang, Jiajun Liu, Feras Dayoub, Xiao Ma, and Lingqiao Liu. Effective tuning strategies for generalist robot manipulation policies. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 7255–7262. IEEE, 2025. 

- [72] Zhiyuan Zhou, Pranav Atreya, Abraham Lee, Homer Walke, Oier Mees, and Sergey Levine. Autonomous improvement of instruction following skills via foundation models. _arXiv preprint arXiv:2407.20635_ , 2024. 

- [73] Ruiqi Zhu, Endong Sun, Guanhe Huang, and Oya Celiktutan. Efficient continual adaptation of pretrained robotic policy with online meta-learned adapters. _arXiv preprint arXiv:2503.18684_ , 2025. 

17 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

## **A. Appendix** 

### **_A.1. DROID Results Details_** 

Fig. 7 reports performance of two DROID tasks: `whiteboard` and `plates` . Here we present the average of the two tasks. The OOD performance shown here is averaged across the val and test scenes. 


**Figure 13:** Average results on performance of the two DROID tasks: `whiteboard` and `plates` . 

### **_A.2. LIBERO Results Details_** 

Fig. 8 reports the average performance of three LIBERO tasks: `pot-on-stove` , `mugs-on-plates` , and `items-into-box` . Here we present the individual performance for all three tasks in Fig. 14. The OOD performance shown here are averaged only across the two test scene. 


**Figure 14:** Detailed results on performance of the three LIBERO tasks: `pot-on-stove` , `mugs-on-plates` , and `items-into-box.` 

18 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

### **_A.3. Data Scaling Results Details_** 

Fig. 15 highlights more details of the data scaling results, examining for which base models RETAIN provides the greatest benefit: it shows the ID/OOD performance for co-FT and RETAIN-co-FT with varying amounts of pretraining data that led to the difference results presented in Fig. 9. We see that as we scale pretraining data, ID performance is similar between co-FT and RETAIN-co-FT, while the benefit provided by RETAIN on OOD greatly increase with the generalist capabilities of the base model, and scales we pre-training data. 


**Figure 15:** Detailed results on the benefits of RETAIN with increasing pretraining data. 

### **_A.4. Ablation on Learning Rate and Gradient Steps_** 

Here, we ablate the learning rate and number of gradient steps we take in the task-FT policy in Fig. 4 to study whether better hyperparameter choices can reduce or resolve overfitting<sup>1</sup> . In Fig. 4, we use learning rate 2.5𝑒−5. Here in Fig. 16, we ablate four different learning rates: one greater than the original and two smaller. We evaluate the model at every 100 gradient steps to also ablate on the number of gradient steps we take. With a larger learning rate, it’s clear that the overfitting issue is more severe, and the performance on all three kinds of evaluations (ID, OOD, Generalist) go down to near zero. With a smaller learning rate, the model still performs well in ID evaluations, and suffers less from forgetting generalist capabilities (measured from Generalist evaluations). This is to be expected because the finetuned model is closer to the pretrained model with a smaller learning rate. However, note that with a smaller learning rate, the OOD evaluation performance is also worse. We plot the OOD performance achieved using the original learning rate in Fig. 4 as the dotted orange line in Fig. 16, and the gap between the dotted and solid orange line shows the performance gap in OOD evaluation when we lower the learning rate, possibly due to underfitting. This experiment shows that tuning the learning rate and the number of update steps does not solve the problem of overfitting during finetuning. While lowering the learning rate can retain more generalist knowledge, it does not prevent the gradual loss of it. More importantly, the lower learning rate leads to worse OOD evaluation performance. 


**Figure 16:** Ablation on learning rate and number of gradient steps for task-FT on `mugs-on-plates` task in LIBERO. 

### **_A.5. Analysis of Finetuning Path in Parameter Space_** 

To understand why model parameter merging helps, we first try to understand here how the parameters change during fine-tuning. In particular, we are interested in understanding how linear the finetuning path is in parameter space, since model parameter merging only moves weights in linear paths. 

> 1Following the best practice from Black et al. [8], we always use a learning rate warmup period of 1000 steps in LIBERO and a consine decay schedule over 30𝑘 steps to 1/10 of the peak learning rate. The learning rate we report here is the peak learning rate. 

19 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 


**Figure 17:** Cosine similarity of parameter difference vectors during finetuning, showing that the finetuning path is highly non-linear. 

To start out, we check the colinearity of the vectors 𝜃𝑖+1 −𝜃𝑖 and 𝜃𝑖 −𝜃𝑖−1, where 𝜃𝑖 is the parameter of the finetuned checkpoint at gradient steps 100 ∗𝑖 (i.e. we plot the difference vector every 100 steps during finetuning). We measure the colinearity as the cosine similarity between the two difference vectors. Fig. 17 shows this for the four different learning rates we ablated in Fig. 16. Since no values are close to 1, this shows that the changes in parameter space is highly non-linear. This is expected since the parameter trajectory of deep neural networks is often highly non-linear. 

Next, we attempt to more directly visualize the path/direction of the parameters during finetuning by projecting them down to 2D with Principal Component Analysis (PCA). Specifically, we again consider the difference of the weight vectors, 𝑋𝑖 = 𝜃𝑖+1 −𝜃𝑖, at every 100 steps during finetuning. In Fig. 18, we plot the first two principal components of 𝑋𝑖 in blue, and label the points 𝑖. Indeed, we see that for all learning rates, the direction of the parameters is highly non-linear. With small learning rates, the direction oscillates a lot; with larger learning rates, the direction bends in a certain direction. In addition, we plot the two principal components of the parameter-merged model as well in orange. As expected, since the the merged model takes a linear path and the finetuned one does not, the two models end in in very different places in the parameter space. This shows that model merging achieves a different solution than any checkpoints on the finetuning path. 

Finally, we analyze changes in all directions of the difference vectors 𝑋𝑖, instead of just the two principal components as shown in Fig. 18. We take the difference vector matrix 𝑌= [𝑋1; 𝑋2; ..., 𝑋𝑛] and compute the singular values of 𝑌𝑌<sup>𝑇</sup> and Fig. 19. If the parameter vectors lie in a linear path, then all difference vectors would point in the same direction and there should only be 1 non-zero singular value. However, it’s clear from Fig. 19 that most singular values are non-zero, showing that the path is non-linear in many dimensions. This generalizes the intuition from Fig. 18 to more dimensions, and shows that model merging indeed achieves a different solution than the finetuning path. 

All these analysis experiments go to show that the finetuning path is highly non-linear, and therefore model parameter merging actually results in a different solution than the finetuned models. 

20 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 


**Figure 18:** PCA projection of the parameter difference during finetuning to 2D. Each subplot corresponds to a different learning rate. 


**Figure 19:** Singular Values of the parameter differences during finetuning. Each subplot corresponds to a different learning rate. 

21 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

### **_A.6. DROID Setup Details_** 

This section outlines the details of the DROID setup that we used for our real-world experiments. 

#### **_A.6.1. Datasets: whiteboard_** 

The whiteboard task-dataset consists of 50 human tele-operated trajectories collected using a Oculus Quest 2 controller. As explained in 6.1, we collect the demonstrations with a fixed setup, with the only diversity being 5 different eraser initial positions and 2 orientations (vertical / horizontal). All demonstrations use the language prompt "wipe the whiteboard". Each step in our dataset consists of a base camera image (always collected from the right external camera), a wrist camera image, 8D-state, 8D-action, and the language instruction. 

#### **_A.6.2. Datasets: plates_** 

The plates task-dataset consists of 100 human tele-operated trajectories collected in a similar manner as above. Again, the demonstractions are collected with a fixed setup, with the only diversity being 5 plate colors, 2 dish racks, and 2 dish rack orientations (vertical / horizontal). 80 of these 100 demos also contain distractor objects chosen from a training set of distractors. All demonstrations use the language prompt "put the plate in the dish rack". 

#### **_A.6.3. Training Details_** 

We utilize [7x joint angles, 1x gripper position] as our proprioceptive state and [7x joint velocity, 1x gripper position] as our actions both during training and inference. We also use the norm-stats of the DROID dataset, publicly available here, to normalize states and actions during training and inference by applying quantilenormalization. The base and wrist camera images go through several transforms (random crop, resizing to 224x224, and color jitter) during training. 

The finetuning is performed with an action horizon of 10 environment steps, thus the policy learns to output action chunks of shape (10,8). 

#### **_A.6.4. Evaluation Details_** 

We use the 7-DoF Franka robot arm for our experiments. We use the same language instruction as training during evaluation, resize our images to 224x224, use the same state/action space specification, and normalize in the same manner as training. 

During evaluations, we additionally binarize the policy’s gripper action to 0/1 (open/close), as well as clip action magnitudes. The policy’s action horizon is 10 environment steps, and during evaluation, we set the open loop horizon to 8: so, during evaluation, we receive 10 actions from the policy, execute the first 8, and then request a new action chunk. We execute the predicted actions at a control frequency of 15 Hz. 

The policy is served on a NVIDIA H200/H100 throughout our evaluations. As the openpi repository specifies, inference requires at least 8 GB of VRAM. 

#### **_A.6.5. Evaluation Criteria: Whiteboard_** 

For all whiteboard evaluations, we use the criteria specified in Table 1 to assign partial success. We perform 10 trials per policy evaluation, for both the ID and OOD evals. 

#### **_A.6.6. Evaluation Criteria: Plates_** 

For all plates evaluations, we use the criteria specified in Table 2 to assign partial success. We perform 10 trials per policy evaluation, for both the ID and OOD evals. 

#### **_A.6.7. Generalist Evaluations Details_** 

As detailed in Tables 3, 4, and 5, we measure policies’ generalist capabilities by evaluating them on 44 tasks, distributed throughout 9 distinct scenes and 17 different language instructions. Importantly, to ensure fair comparison, we ensure that the initial conditions, camera angle, lighting, and all other such factors per task are kept the same across the various policies that we evaluate. 

22 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

|**Subtask**<br>**Cumulative Score**|
|---|
|Pick up Eraser<br>0.2|
|Approach Whiteboard<br>0.4|
|Set Eraser on Whiteboard While Still Grasping It<br>0.6|
|Performs the Wiping Motion<br>0.8|
|Erases≥90%of Text<br>1.0|
|_Penalty:_ -0.1 if anyof the above is done, but the erasergot flipped in theprocess.|


**Table 1:** Subtasks and cumulative score for the `whiteboard` task. 

|**Subtask**<br>**Cumulative Score**|
|---|
|Picks up Plate<br>0.2|
|Moves to Dish Rack<br>0.4|
|Rotates and Aligns Over a Groove<br>0.6|
|Tries to Insert Plate Into a Groove<br>0.8|
|SuccessfullyInserts Plate Into a Groove<br>1.0|
|_Penalty:_ -0.1 if any of the above is done but with the small grooves.|
|_Partial:_ 0.5 if it tries to do the insertingmotion but theplate is misoriented.|


**Table 2:** Subtasks and cumulative scoring for the `plates` task. 

### **_A.7. LIBERO Setup Details_** 

This section outlines the details of the LIBERO setup that we used for our simulated experiments. 

#### **_A.7.1. LIBERO Pretraining_** 

In order to obtain a base-model to serve as the starting point for RETAIN in LIBERO, we pretrain 𝜋0 on a mixture of LIBERO datasets. Specifically, we use 90 tasks from LIBERO-90, 9 tasks from LIBERO-object, 9 tasks from LIBERO-spatial, and 9 tasks from LIBERO-goal, for a total of 117 tasks in our pretraining dataset. For all LIBERO datasets, pretraining and finetuning, we utilize pre-processed RLDS versions gathered from here and here. These datasets consist of LIBERO demonstrations that have been preprocessed to upscale images, filter out transitions with idle actions, and remove failure trajectories. More details, such as hyperparameter choices, for the pretraining stage itself can be found in A.8. All subsequent fine-tuning and evaluation uses the normalization stats of this pretraining dataset, applying mean/standard-deviation normalization. 

#### **_A.7.2. LIBERO Finetuning Datasets_** 

As mentioned in 6.1, we finetune on 3 tasks from LIBERO-10: `pot-on-stove` , `mugs-on-plates` , and `items-into-basket` . For each dataset, we obtain pre-processed and filtered versions as described above. 20 highlights what these finetuning tasks, and thus also our ID evals, look like. 

The language instructions for each libero fine-tuning dataset are: 

- `pot-on-stove` : "turn on the stove and put the moka pot on it" 

- `mugs-on-plates` : "put the white mug on the left plate and put the yellow and white mug on the right plate" 

- `items-into-basket` : "put both the alphabet soup and the cream cheese box in the basket" 

We utilize [3x end effector (EEF) Cartesian position, 3x EEF rotation (roll/pitch/yaw), 1x gripper position] as both our states and actions. Similar to the DROID finetuning dataset, each step in our datasets consists of 1 base image, 1 wrist image, 7D state, 7D action, and the language instruction. As described earlier, we use the 

23 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

|**Scene Image**|**Task**|**# Trials**|**Randomization**|**Rubric**|
|---|---|---|---|---|
||put the spoon in the<br>dish rack<br>put carrot in bowl|4<br>4|swap spoon and carrot posi-<br>tion, 2 evals each<br>swap spoon and carrot posi-<br>tion, 2 evals each|1: pick up spoon; 1.5: move<br>spoon towards dish rack; 2:<br>put spoon in dish rack (any-<br>where)<br>1: pick up carrot; 1.5: move<br>carrot towards bowl; 2: put<br>carrot in bowl|
||put plate in dish rack|2|randomize initial position of<br>the plate in front of the robot|1: pick up plate; 1.5: move<br>plate towards the dish rack; 2:<br>put plate into dish rack (any-<br>where)|
||wipe the table|2|cloth initially on the left and<br>right side of the open area|1: move down towards cloth;<br>2: perform lateral ""wiping-<br>style"" motion|
||put the plate on the ta-<br>ble|2|plate initially on different<br>dish rack holders (middle and<br>end)|1: moves towards red plate;<br>1.5: picks up plate; 2: places /<br>drops plate onto the table|
||clean up the table|2|randomize initial position of<br>paper ball on table|1: picks up paper ball; 1.5<br>moves paper ball towards<br>brown bin; 2: puts paper ball<br>into bin|


**Table 3:** DROID Generalist evaluation tasks grouped by scene (Scenes 1-4). Each task contains associated trial counts, randomization details, and evaluation rubrics. 

24 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

|**Scene Image**|**Task**<br>**# Trials**|**Randomization**|**Rubric**|
|---|---|---|---|
||close the drawer<br>4|two top, two bottom drawer|1: moves towards the drawer;<br>2: closes drawer|
||put the stapler on the<br>notebook<br>2<br>put<br>stapler<br>in<br>the<br>drawer<br>4|put stapler in higher and<br>lower position on the table<br>put stapler in higher and<br>lower position on the table,<br>open top and bottom drawer|1: picks up stapler; 2: puts<br>stapler on notebook<br>1: picks up the stapler; 2: puts<br>stapler into the drawer|
||clean the whiteboard<br>2|initial eraser position on the<br>left and right of whiteboard|1: pick up eraser; 2: perform<br>wiping motions on the white-<br>board; 3: erase the full smiley|
||put the marker in the<br>cup<br>4|swap<br>initial<br>position<br>of<br>marker and cup, two local<br>modifications each|1: picks up marker; 1.5: ro-<br>tates arm to put marker in<br>roughly upright position; 2:<br>puts marker in cup|


**Table 4:** DROID Generalist evaluation tasks grouped by scene (Scenes 5-8). Each task contains associated trial counts, randomization details, and evaluation rubrics. 

25 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

|**Scene Image**|**Task**<br>**#**|**Trials**|**Randomization**|**Rubric**|
|---|---|---|---|---|
||put the black sponge in<br>the blue bowl|2|any<br>two<br>configurations<br>where the black sponge is<br>not starting in the blue bowl|1: picks up object; 2: puts ob-<br>ject in correct location|
||put the red bottle in<br>the black bowl<br>put the watermelon in<br>the purple bowl|2<br>2|any<br>two<br>configurations<br>where the red bottle is not<br>starting in the black bowl<br>any<br>two<br>configurations<br>where the watermelon is not<br>starting in the purple bowl|1: picks up object; 2: puts ob-<br>ject in correct location<br>1: picks up object; 2: puts ob-<br>ject in correct location|
||move the watermelon<br>from the purple bowl<br>to the blue bowl|2|any<br>two<br>configurations<br>where the watermelon starts<br>in the purple bowl|1: picks up object; 2: puts ob-<br>ject in correct location|
||put the tape in the pur-<br>ple bowl|2|any<br>two<br>configurations<br>where the tape is not starting<br>in the purple bowl|1: picks up object; 2: puts ob-<br>ject in correct location|
||put the waterbottle on<br>the left side of the table|2|waterbottle starts on two dif-<br>ferent positions on the left<br>side of the table|1: picks up object; 2: puts ob-<br>ject in correct location|


**Table 5:** DROID Generalist evaluation tasks grouped by scene (Scene 9). Each task contains associated trial counts, randomization details, and evaluation rubrics. 

26 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

norm-stats of our pretraining dataset for normalizing states and actions during both training and inference. The base and wrist camera images go through several transforms (random crop, resizing to 224x224, and color jitter) during training. 

The finetuning is performed with an action horizon of 50 environment steps, and the actions are padded to be 32-dimensional, thus the policy learns to output action chunks of shape (50, 32). 

#### **_A.7.3. LIBERO Evaluation Details_** 

We use the LIBERO simulator for evaluation. Each ID eval is conducted for 20 episodes. Each OOD eval is conducted with 5 seeds, 10 episodes/seed. 21, 22, and 23 show the 3 types of OOD variations we test for in each of the 3 tasks. 

The Generalist evals consists of 20 tasks, 5 each from LIBERO-object, LIBERO-spatial, LIBERO-goal, and LIBERO-90, and each task is tested for 10 episodes. Table 6 highlights a few tasks per LIBERO eval suite that we use in our generalist evals. 

The seed controls OOD randomization such as translation of the objects, spawning random distractors, etc. We use the same language instruction as training during evaluation, resize our images to 224x224, and use the same state/action spaces. 

During the evaluations, we extract the 7D actions by taking the first 7 elements from each 32-dimensional policy prediction. We let the simulator step for 10 steps before starting execution. The open loop horizon is set to 5, and follows a similar pattern as the DROID evals. 

The evaluation criteria for all libero evals are 0 for failure, 1 for success, as determined by the simulator environment. 


**Figure 20:** Three LIBERO tasks we use for finetuning: `pot-on-stove` , `mugs-on-plates` , and `items-into-basket` . 

27 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 


**Figure 21:** Three types of out-of-distribution variation of the LIBERO `mugs` task. The three different type are: (1) small translation to object positions, (2) big translation to object position and additional distractors, and (3) background change. 


**Figure 22:** Three types of out-of-distribution variation of the LIBERO `items-into-basket` task. The three different type are: (1) small translation to object positions, (2) big translation to object position and additional distractors, and (3) background change and additional distractors. 


**Figure 23:** Three types of out-of-distribution variation of the LIBERO `pot-on-stove` task. The three different type are: (1) small translation to object positions, (2) big translation to object position and additional distractors, and (3) background change. 

28 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

|**Scene Image**|**Task**|**LIBERO Eval Suite**|
|---|---|---|
||put the bowl on the plate|LIBERO-goal|
||pick up the alphabet soup<br>and place it in the basket|LIBERO-object|
||pick up the black bowl<br>from table center and<br>place it on the plate|LIBERO-spatial|
||put white bowl on plate|LIBERO-90|


**Table 6:** Sample of LIBERO Generalist Evaluations for each evaluation suite. 

29 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

### **_A.8. Hyperparameters_** 

#### **_A.8.1. Choosing Merging Coefficient_** 𝛼 

For each task that we consider (e.g. `mugs-on-plate` in LIBERO, `plates` in DROID), we test policy performance on several scenes, which are different variations of the same task with different objects, distractors, and backgrounds etc. To choose what values of 𝛼 we use, we use one OOD scene as the “validation” scene, and tune the hyperparameter 𝛼 for best performance on that validation scene. Then, we use the rest of the OOD scenes as the “test” scenes, and report the performance of all methods only on the test scenes. In DROID experiments, we only tune 𝛼∈{0.25, 0.5, 0.75} on the validation scene, while in LIBERO experiments we tune 𝛼∈{0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1} since it is cheap to do so. We find that on DROID 𝛼= 0.5 typically tends to perform well across tasks. 

#### **_A.8.2. Choosing Number of Gradient Steps_** 

For choosing how long the task-FT and co-FT should go on for, we evaluate checkpoints in ID evaluation to assess how well they fit the data. We then pick the earliest checkpoint that achieves maximal performance, to get a checkpoint that learns the target task well but does not overfit to the fientuning dataset, so that it is the strongest baseline. 

#### **_A.8.3. Real-world Experiments’ Hyperparameters_** 

Below are tables specifying the hyperparameters we finalized upon for each of our finetuning runs for real-world experiments. 

|**Hyperparameter**|**Value**|
|---|---|
|Batch Size|32|
|Learning Rate Schedule|Linear Warmup with Cosine Decay|
|Peak-LR|3e-5|
|End-LR|2e-6|
|Warmup-Steps|100|
|Decay Steps|1000|
|Gradient Steps|500|
|Weight Decay|1e-10|
|Optimizer|Adam(b1=0.9, b2=0.95, eps=1e-8)|
|Clip Gradient Norm|1.0|


**Table 7:** Training hyperparameters for task-FT on DROID `whiteboard` . 

30 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

|**Hyperparameter**|**Value**|
|---|---|
|Batch Size|32|
|Learning Rate Schedule|Linear Warmup with Cosine Decay|
|Peak-LR|3e-5|
|End-LR|2e-6|
|Warmup-Steps|1000|
|Decay Steps|10000|
|Gradient Steps|9999|
|Weight Decay|1e-10|
|Optimizer|Adam(b1=0.9, b2=0.95, eps=1e-8)|
|Clip Gradient Norm|1.0|
|Cotraining-Mix|80% task, 20% pretrain|


**Table 8:** Training hyperparameters for co-FT on DROID `whiteboard` . 

|**Hyperparameter**|**Value**|
|---|---|
|Batch Size|32|
|Learning Rate Schedule|Linear Warmup with Cosine Decay|
|Peak-LR|3e-5|
|End-LR|2e-6|
|Warmup-Steps|500|
|Decay Steps|5000|
|Gradient Steps|1500|
|Weight Decay|1e-10|
|Optimizer|Adam(b1=0.9, b2=0.95, eps=1e-8)|
|Clip Gradient Norm|1.0|


**Table 9:** Training hyperparameters for task-FT on DROID `plates` . 

|**Hyperparameter**|**Value**|
|---|---|
|Batch Size|32|
|Learning Rate Schedule|Linear Warmup with Cosine Decay|
|Peak-LR|3e-5|
|End-LR|2e-6|
|Warmup-Steps|1000|
|Decay Steps|10000|
|Gradient Steps|5000|
|Weight Decay|1e-10|
|Optimizer|Adam(b1=0.9, b2=0.95, eps=1e-8)|
|Clip Gradient Norm|1.0|
|Cotraining-Mix|80% task, 20% pretrain|


**Table 10:** Training hyperparameters for co-FT on DROID `plates` . 

|**Hyperparameter**|**Value**|
|---|---|
|Merging Weight for task-FT<br>Merging Weight for co-FT|75% task-FT, 25% base model<br>50% task-FT, 50% base model|


**Table 11:** Merging hyperparameters for DROID `whiteboard` . 

31 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

|**Hyperparameter**|**Value**|
|---|---|
|Merging Weight for task-FT<br>Merging Weight for co-FT|50% task-FT, 50% base model<br>50% task-FT, 50% base model|


**Table 12:** Merging hyperparameters for DROID `plates` . 

Finally, in our continual learning experiment, we use exactly the same hyperparameters as those used for plates-co-FT found in 10, just applied sequentially twice to first cotraining on the plates dataset, then on the whiteboard. In the continual learning setup, the Merging weight is also always fixed at 50% task-FT, 50% base model. 

#### **_A.8.4. Simulation Experiments’ Hyperparameters_** 

In order to perform our simulation experiments, we had to first perform a round of pretraining on 117 LIBERO tasks, as described earlier. Here are the hyperparamters for this pretraining. We back-tested various checkpoints of this pretraining on the entire libero suite, and settled on step 10,000 as being a good candidate to serve as a base model, as it performed the best on both seen and unseen libero tasks. 

|**Hyperparameter**|**Value**|
|---|---|
|Batch Size|64|
|Learning Rate Schedule|Linear Warmup with Cosine Decay|
|Peak-LR|2.5e-5|
|End-LR|2.5e-6|
|Warmup-Steps|1000|
|Decay Steps|30000|
|Gradient Steps|10000|
|Weight Decay|1e-10|
|Optimizer|Adam(b1=0.9, b2=0.95, eps=1e-8)|
|Clip Gradient Norm|1.0|


**Table 13:** Hyperparameters for LIBERO pretraining. 

32 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

Both task-FT and co-FT on all 3 libero finetunting tasks use the same set of hyperparameters, provided below. We determine the number of gradient steps to choose by sweeping over all taken checkpoints, evaluating them on ID and OOD, and picking the best performing ones. 

|**Hyperparameter**|**Value**|
|---|---|
|Batch Size|64|
|Learning Rate Schedule|Linear Warmup with Cosine Decay|
|Peak-LR|2.5e-5|
|End-LR|2.5e-6|
|Warmup-Steps|1000|
|Decay Steps|30000|
|Gradient Steps|500 (items-into-basket, pot-on-stove), 1000 (mugs)|
|Weight Decay|1e-10|
|Optimizer|Adam(b1=0.9, b2=0.95, eps=1e-8)|
|Clip Gradient Norm|1.0|


**Table 14:** Training hyperparameters for task-FT on LIBERO- `items-into-basket` , `mugs` , `pot-on-stove` . 

|**Hyperparameter**|**Value**|
|---|---|
|Batch Size|64|
|Learning Rate Schedule|Linear Warmup with Cosine Decay|
|Peak-LR|2.5e-5|
|End-LR|2.5e-6|
|Warmup-Steps|1000|
|Decay Steps|30000|
|Gradient Steps|1000 (items-into-basket, pot-on-stove, mugs)|
|Weight Decay|1e-10|
|Optimizer|Adam(b1=0.9, b2=0.95, eps=1e-8)|
|Clip Gradient Norm|1.0|
|Cotraining-Mix|50% task, 50% pretrain|


**Table 15:** Training hyperparameters for co-FT on LIBERO- `items-into-basket` , `mugs` , `pot-on-stove` . 

33 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

As explained earlier and similar to our DROID procedure, after checking all checkpoints and picking the best-performing one, we then apply RETAIN on it to enhance its performance on OOD and Generalist evals. In simulation, we check various merging coefficients in the range [0.0, 1.0], and after doing so, here are our final merging parameters. 

|**Hyperparameter**|**Value**|
|---|---|
|Merging Weight for task-FT|90% task-FT, 10% base model|
|Merging Weight for co-FT|90% task-FT, 10% base model|


**Table 16:** Merging hyperparameters for LIBERO `items-into-basket` . 

|**Hyperparameter**|**Value**|
|---|---|
|Merging Weight for task-FT<br>Merging Weight for co-FT|80% task-FT, 20% base model<br>90% task-FT, 10% base model|


**Table 17:** Merging hyperparameters for LIBERO `mugs` . 

|**Hyperparameter**|**Value**|
|---|---|
|Merging Weight for task-FT|90% task-FT, 10% base model|
|Merging Weight for co-FT|70% task-FT, 30% base model|


**Table 18:** Merging hyperparameters for LIBERO `pot-on-stove` . 

34 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 

### **_A.9. Details on Baseline Methods_** 

Here we provide addtional details on the baseline methods we compare against. 

**Task-FT** : We fine-tune all parameters of the base policy according to the behavioral cloning loss in Eq. (1). All data are sampled from the fine-tuning dataset. 

**Co-FT** : We fine-tune all parameters using the behavioral cloning loss, and each update batch is sampled from both the pretraining dataset and the finetuning dataset with a fixed weight. See Section A.8 for specific weight values we use for different tasks. 

**LoRA** : LoRA (low rank adaptation) freezes all the weights of the base pretrained policy, and finetunes an adapter head with a low rank bottleneck. Typically the adapter head has much fewer parameters than the base pretrained model. The resulting policy is achieved by adding the weights of the frozen pretrained policy and the low rank adapter head. 

**Freeze-FT** : Similar to Task-FT, but we freeze the parameters in the language model backbone and finetune only parameters from the action expert and vision encoder. 

**Scratch** : Training a policy from sratch. To make it comparable to the other VLA baseline policies, we use the same 𝜋0 architecture but initialize from the Paligemma VLM weights, without pretraining on any robot data. 

### **_A.10. Why does RETAIN work so well?_** 

While we have shown empirically in this work that RETAIN works well across real and simulated tasks, we don’t understand the full scope of the reasons why model parameter merging works so well empirically. However, previous work in computer vision and large-language models have also shown empirical benefits of merging parameters of the pretrained and fine-tuned model (see Section 2). Similar to our work, these previous works are also largely empirical and corroborate our findings in a real-world robotics setting. Specifically, Neyshabur et al. [43] found that fine-tuning from the same pretrained model results in regions where solutions are connected by a linear path along which error remains low, a phenomenon known as “linear mode connectivity” [2]. [3] and [4] explained that SGD typically converges to a solution that is on the boundary of this low-error path, while weight merging is able to find a point centered in this region, which often has slightly worse train loss but substantially better test error. We attribute the performance gains we see also to this, though call for more rigorous future work to explain this more rigorously. 

### **_A.11. Qualitative Analysis of Success and Failure Mode of RETAIN_** 

Typically, we observe that RETAIN improves the robustness of the merged policy on OOD evaluations. Compared to task-FT policies, which are brittle and will fail in out-of-distribution scenarios catastrophically and is unable to retry, the RETAIN policies typically exhibits more robust behavior, and can recover from failure using its generalist knowledge. Typically, we observe that the task-FT policy either either does the full task successfully, or cannot do the task at all. In comparison, the RETAIN policies usually at least partially complete the task. However, we do observe that the RETAIN policies sometimes fail due to (1) imprecise execution of the task and stuck in constant retry mode and (2) produces an action that does not solve the task (though still semantically meaningful), and is unable to successfully continue afterwards. We provide two qualitative examples of this in Fig. 24 and Fig. 25. 

35 

Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging 


**Figure 24:** Failure Example of RETAIN in DROID `whiteboard` task: The arm picks up the eraser, but drops it on the whiteboard instead of wiping left and right with it. 


**Figure 25:** Failure Example of RETAIN in DROID `plates` task: the arm is not able to precisely pick up the green plate, and so constantly retries this until the policy times out. 

36 

