---
title: "Steerable Vision-Language-Action Policies for Embodied Reasoning and Hierarchical Control"
date: "2026-02-13"
authors: "William Chen; Jagdeep Singh Bhatia; Catherine Glossop; Nikhil Mathihalli; Ria Doshi; Andy Tang"
venue: "RSS 2026"
url: https://arxiv.org/abs/2602.13193
pdf: https://arxiv.org/pdf/2602.13193
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.13193)** / [論文ページ](https://arxiv.org/abs/2602.13193)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Steerable Vision-Language-Action Policies for Embodied Reasoning and Hierarchical Control 

William Chen<sup>1</sup> , Jagdeep Singh Bhatia<sup>1</sup> , Catherine Glossop<sup>1</sup> , Nikhil Mathihalli<sup>1</sup> , Ria Doshi<sup>2</sup> , Andy Tang<sup>2</sup> , Danny Driess<sup>3</sup> , Karl Pertsch<sup>3</sup> , Sergey Levine<sup>1</sup> 

1U.C. Berkeley, 2Stanford University, 3Physical Intelligence 


Fig. 1: We propose **Steerable Policies** : vision-language-action models that can robustly follow a wide range of detailed commands (green boxes on right), going beyond usual task language to include instructions such as motions or pixel coordinates of the gripper and objects. The flexibility afforded by Steerable Policies enables substantially improved transfer of VLMs’ pretrained reasoning, semantic knowledge, and in-context learning skills to generalist robotic control in hierarchical systems. 

**_Abstract_ —Pretrained vision-language models (VLMs) can make semantic and visual inferences across diverse settings, providing valuable common-sense priors for robotic control. However, effectively grounding this knowledge in robot behaviors remains an open challenge. Prior methods often employ a hierarchical approach where VLMs reason over high-level commands to be executed by separate low-level policies, e.g., vision-languageaction models (VLAs). The interface between VLMs and VLAs is usually** **_natural language task instructions_ , which fundamentally limits how much VLM reasoning can steer low-level behavior. We thus introduce Steerable Policies: VLAs trained on rich synthetic commands at various levels of abstraction, like subtasks, motions, and grounded pixel coordinates. By improving lowlevel controllability, Steerable Policies can unlock pretrained knowledge in VLMs, enabling improved task generalization. We demonstrate this benefit by controlling our Steerable Policies with both a learned high-level embodied reasoner and an offthe-shelf VLM prompted to reason over command abstractions via in-context learning. Across extensive real-world manipulation experiments, these two novel methods outperform prior embodied reasoning VLAs and VLM-based hierarchical baselines, including on challenging generalization and long-horizon tasks. Website: steerable-policies.github.io** 

## I. INTRODUCTION 

A long-standing goal of robotics is to develop _generalist_ policies that can follow open-ended commands to perform a wide range of tasks. As scaling robot data collection remains expensive, this motivates the use of pretrained foundation vision-language models (VLMs) as a source of semantic and perceptual knowledge. Prior works often employ a hierarchy, 

where a high-level VLM reasons over task instructions and issues commands to a separate, language-conditioned low-level policy [1, 2]. However, effectively bringing VLM capabilities to bear for solving general robotics tasks is challenging, as doing so requires grounding their pretrained knowledge in robot behaviors. This raises a fundamental question: _how can we best unlock and leverage the generalization capabilities of pretrained foundation models for robotics?_ 

We posit that a major bottleneck in transferring these capabilities is insufficient policy _steerability_ . Put simply, no matter how good a VLM is at determining robot behaviors needed for solving tasks, its reasoning abilities are wasted if the robot’s policy cannot execute them. For example, the VLM might infer that an object needs to be grasped in a particular location, but this inference is only useful if the policy can understand commands specifying that location. Even powerful policies, such as vision-language-action models (VLA), have limited ability to follow diverse commands due to dataset limitations, where labels are often too formulaic, homogeneous, and imprecise to specify the full range of behaviors needed for solving new tasks [3]. These drawbacks make standard task-level language derived from dataset labels a poor interface for VLMs to control robot policies. 

One insight is that steerability can be improved by augmenting existing datasets with more detailed synthetic language. Robot datasets already _implicitly_ contain rich semantics, interactions, and behaviors, far beyond what is described in their sparse task labels. For example, a policy which learns to “wipe 

the table with the towel on the left” tacitly learns what towels look like, how to grasp them, and how to move left – all of which can be leveraged for other tasks, like “hang the towel on the hook.” Training on more descriptive commands could aid the policy flexibly invoke these skills for solving new tasks. 

However, na¨ıvely densifying task descriptions is insufficient for generalization and composition. For example, expanding the descriptions of existing behaviors would struggle to teach the policy the names of fundamentally out-of-distribution objects. Still, the policy may be able to grasp these novel objects, due to their physical similarity to objects the policy _has_ learned to interact with. A generalizable way to induce these behaviors is by prompting with _grounded_ features, like pixel coordinates, as they can specify behaviors and concepts that are otherwise difficult to communicate to the policy (e.g., "grasp at <novel object’s position>"). Not only are grounded features easily extracted for training, but modern VLMs are also trained to output them, thereby allowing these VLMs to transfer their pretrained knowledge to robotics. 

We thus introduce **Steerable Policies** : robotic foundation models that follow a much wider range of commands than standard VLAs. Beyond typical “task-level” commands (e.g., "put the carrot in the pot"), we train VLAs to accept more detailed inputs, such as subtasks ("reach for the carrot") or low-level atomic motions ("move left and close the gripper"). We also include commands with grounded features, such as gripper traces ("move along [ _x_ 1 _, y_ 1] _,_ [ _x_ 2 _, y_ 2] _, ..._ ") or points ("grasp the object at [ _x, y_ ]"). Finally, we include prompts that compose all these modalities ("move right from [ _x_ 1 _, y_ 1] to put the mushroom on the plate at [ _x_ 2 _, y_ 2]"). These **_steering commands_** are synthetically generated by a scalable pipeline that automatically parses and labels robot data. See Fig. 1 for more. 

Compared to past hierarchical methods [1], Steerable Policies vastly expand the interface between low-level robot behaviors and high-level VLM skills, allowing high-level reasoners to flexibly choose instructions at the right level of abstraction for generalization and compositionality. We show this by proposing and evaluating two ways for VLMs to control our Steerable Policies, instantiated on a real-world Bridge WidowX setup [4, 5]. First, we show that VLMs can be fine-tuned into effective _high-level_ models for instructing Steerable Policies by producing chain-of-thought reasonings (CoT [6, 7]) followed by steering commands. This outperforms past reasoning VLAs [8, 9], indicating that it makes especially good use of embodied reasoning data. Second, we show how Steerable Policies can better apply the _in-context learning_ skills of API-based off-the-shelf VLMs. We find that these VLMs can apply in-context learning over past observations and commands to further improve robot behaviors by choosing commands of the correct level of abstraction. This is a novel functionality afforded by our Steerable Policies, which leads to significant performance gains over standard baselines. 

In summary, we show that improving VLA steerability is critical to facilitate transfer of VLM capabilities to robotics. We do this by introducing **(1)** Steerable Policies: VLAs that 

can be prompted at many levels of abstraction to perform diverse manipulation skills – a paradigm which is agnostic to VLA architecture, as we demonstrate by instantiating Steerable Policies with two popular VLA frameworks (OpenVLA and _π_ 0 _._ 5 [10, 11]); and **(2)** novel methods for using VLMs’ embodied reasoning and in-context learning to hierarchically control our VLA to solve challenging tasks. We demonstrate that the steerability of low-level VLAs significantly improves the use of high-level VLMs’ pretrained capabilities, resulting in better robot generalization. 

## II. RELATED WORKS 

**Vision-language-action models.** As in vision and language, robotics has moved towards using large foundation models [12]. A popular method is to fine-tune general VLMs into _vision-language-action policies (VLAs)_ [13, 10], transferring the base VLM’s comprehensive pretrained representations to learn robot tasks from demonstrations. Prior works explore many variations of this recipe, such as altering action representations [13, 10, 14–16, 11, 17] or training VLAs to perform embodied reasoning [8, 9, 18]. Our approach differs from such works in that we aim to improve policy steerability via augmentation of language prompts, with the end goal of making better use of foundation model capabilities in hierarchical approaches. 

**Training for steerability.** Past works often improve policy steerability by training on synthetic language labels that are more diverse [19], detailed [20, 21], or composable [22, 23]. They can also be trained on non-text steering modalities, like gripper traces [24, 25] or visual marks [26]. 

In contrast, our method trains on _many_ input types, rather than finding a one-size-fits-all steering modality. Additionally, all our steering commands are expressed in text tokens, allowing our VLA to interface with generative VLMs more easily than other models trained on many prompt modalities, such as OmniVLA [27]. Similar to our method, MolmoAct trains on standard text with gripper trace CoTs, enabling inference-time steering via two modalities (changing either the trace _or_ the language) [28]. However, unlike our work, they limit language steering to task-level prompts only (no other abstractions, like subtasks, motions, or points, as we use). Additionally, MolmoAct’s gripper trace steering can only be used _in conjunction_ with text commands, which can be a drawback when text introduces adverse biases (e.g., if the policy systematically misidentifies an object by name). This disadvantage is not shared by our policy. 

In summary, the core novelty of our Steerable Policies is that they accept steering commands spanning a spectrum of abstractions, not just one or two, as MolmoAct and other prior works do. In particular, giving high-level VLMs the flexibility to _choose_ how to steer the low-level VLAs is necessary for improved generalization. We find in Sec. VI-A that this is critical for performance, as the effectiveness of different steering abstractions depends heavily on the task setting. 

**Synthetic data for model controllability.** Our method of training policies on synthetic language parallels a trend in text- 


Fig. 2: The hierarchical policy inference loop, where a highlevel model sends commands to the low-level Steerable Policy. 

to-image generation: while image corpora often contain the diversity needed for detailed image generation, the accompanying captions are too imprecise for fine-grained text controllability, necessitating detailed synthetic labels [29]. Similarly, our core insight is that _robot datasets already contain diverse behaviors, but their text labels are too sparse, biased, and succinct to induce desirable actions for novel tasks_ . While steerability in the image domain is valuable for aligning with user preferences, we aim to make VLAs more steerable to better interface with high-level policies, enabling improved use of their pretrained capabilities for solving new control tasks. 

**Hierarchical robot learning.** One way to improve generalization is to hierarchically decompose robot tasks into atomic skills [30]. These techniques broadly divide action prediction into (1) fast and reactive control and (2) slow and methodical reasoning or planning, akin to the System I and II model of human cognition [31]. In robot learning, these methods either are trained end-to-end (e.g., policies with an intermediate “chain-of-thought reasoning” [8, 11, 28, 32]) or, as we focus on in Sec. V, are factorized into separate models [1, 33, 2, 24]. 

Several works use off-the-shelf VLMs as the high-level policy [1, 34–41], while others finetune them to improve their alignment with a given domain or low-level policy [33, 42– 44, 24, 28, 45, 46]. However, these works usually select a _single_ modality to interface between high and low levels, such as subtask-level language prompts [1, 36, 37, 44, 45, 39, 35, 38, 43, 46] or grounded representations [24, 28]. 

Steerable Policies enable a fundamentally new capability absent from these works: the ability to reason about and choose which abstraction to use for steering VLAs. This not only yields high performance (Sec. VI-A), but also provides novel ways to apply broad VLM capabilities – scene understanding, reasoning, and in-context learning – to robotics (Sec. VI-C). Of course, non-steerable VLAs only accept a single type of (usually text) prompt, and do not reap the same benefits. 

## III. PRELIMINARIES 

**Vision-language-action models.** Given task prompt _l_ and observations _o_ (e.g., proprioception and images), _behavioral cloning (BC)_ learns a policy _π_ ( _a|o, l_ ) that solves tasks by matching the behavior distribution of expert demonstrators. _Vision-language-action models_ are pretrained _vision-language models_ fine-tuned into _π_ . Our Steerable Policy (Sec. IV) is a VLA, though trained to accept diverse steering modalities. 

**Hierarchical policies.** One way to improve the generalization of learned policies is with hierarchical methods. This factorizes robot instruction-following into two steps: first, a high-level policy takes the overall task _l_ and observation _o_ to output an appropriate intermediate subtask, plan, or goal _g_ ; then, the low-level policy samples actions _a_ conditioned on _g_ and _o_ . This is the framework we adopt (Fig. 2): our Steerable Policy acts as the low-level controller (where _g_ are steering commands), while we explore the novel high-level policy capabilities they enable in Sec. V. 

## IV. STEERABLE VISION-LANGUAGE-ACTION POLICIES 

We now introduce Steerable Policies. We propose training VLAs on **_steering commands_** that span many abstractions, such as subtasks, motions, or grounded coordinates (Sec. IV-A). After generating them at scale (Sec. IV-B), these prompts randomly replace the standard task-level labels used for BC. Training on steering commands yields a policy that can execute diverse compositional skills when prompted via a range of modalities (Sec. VI-A), in contrast to past works that use single steering inputs [24, 25, 22]. This section solely focuses on training _low-level_ Steerable Policies; then, in Sec. V, we discuss how to use these VLAs with _high-level_ VLM policies that perform embodied reasoning or in-context learning to choose appropriate steering commands. 

## _A. Styles of Steering Commands_ 

To obtain VLAs that can exhibit diverse behavior when instructed with a wide range of abstractions, we train on a diverse mix of different **_steering command styles_** , satisfying several desiderata: commands should be (1) _versatile_ for inducing a range of generalizable behaviors for solving novel tasks; (2) _conducive_ to being issued by human operators, high-level reasoners, and in-context learning VLMs; and (3) _scalable_ for synthetic labeling – i.e., they can be automatically generated from robot trajectories by using foundation models. The categories of steering commands that we train on are as follows (see Fig. 1 and App. A for more examples): 

- 1) **_Tasks_** : The default labels used for training VLAs. They allow Steerable Policies to also solve tasks that standard VLAs can. E.g., "put the carrot in the pot". 

- 2) **_Subtasks_** : These help compose existing semantic skills for novel tasks. E.g., "reach for the carrot". 

- 3) **_Atomic motions_** : These let the VLA follow granular movements in language, without referencing the semantic contents of the scene. E.g., "move left" or "open gripper". 

- 4) **_Gripper traces_** : These provide a list of pixels for the gripper to follow. E.g., "move from [ _x_ 1 _, y_ 1] to [ _x_ 2 _, y_ 2]". 

- 5) **_Points_** : These indicate positions of objects or locations of interest. E.g., "lift above <pot position>" or "grasp at <carrot position>". This is subtly distinct from gripper trace commands, as pointing does _not_ necessarily indicate the exact pixels the gripper must move to, merely visual positions relevant to the task. 

- 6) **_Combinations_** : Hybrids of these styles. E.g., "move left from [ _x, y_ ] to the carrot at <carrot position>". 


Fig. 3: Our automated pipeline for annotating robot data with synthetic steering commands at scale. **1:** We use a suite of foundation models to extract subtasks and grounded features (bounding boxes, motions, and gripper traces) from each trajectory. **2:** We query a VLM to generate diverse steering commands for training Steerable Policies. These commands may reference features extracted in the first step, which we provide in the prompt. **3:** To train high-level embodied reasoners, we also generate _rationalizations_ for why particular commands are appropriate for given observations (Sec. V-A). 

The last three styles can reference 2D pixel coordinates, which VLMs can easily specify [47, 18]. They also allow finegrained steering when language is insufficient: e.g., the policy might fail to pick up some out-of-distribution object specified by name, but would succeed if told to "pick up the object at [ _x, y_ ]". Likewise, if there are multiple of instances an object (making language underspecified), the policy can determine the correct one to interact with from a pointing command. 

## _B. Generating Steering Commands at Scale_ 

The default task commands found in large robot datasets are usually human-annotated. While this yields the gold standard in terms of data quality, acquiring these labels at scale is expensive and labor-intensive, especially when language commands reference grounded features, such as pixel coordinates. We thus turn to synthetically-generated annotations. 

Our pipeline for producing steering commands is shown in Fig. 3. We first extract grounded features from a robot dataset, then compile them into subtasks. Specifically, we follow Zawalski et al. [8] to programmatically extract motion language, then use Molmo to extract task-relevant object names and map them to segmentation masks [47]. Next, we use SAM2 to track and propagate these masks across the entire trajectory video [48], thereby producing temporally-consistent open-vocabulary bounding boxes. Separately, we call DETR to extract the robot’s gripper traces [49]. Finally, given the overall task, motions, and objects, we query Gemini 2.0 [50] to break the episode into semantic subtasks. 

After grounded feature extraction and subtask decomposition, we query Gemini _again_ to restate each subtask into equivalent steering commands of all styles in Sec. IV-A). Gripper traces, motions, and object centroids are provided 


Fig. 4: Our two novel high-level policies (Sec. V). **(a)** finetunes a VLM into an embodied reasoner that issues steering commands, while **(b)** queries an off-the-shelf VLM to determine appropriate commands via in-context reasoning. 

in the prompt, as these grounded features are useful for generating some steering commands. This pipeline allows us to expand from 38k “standard” Bridge task-level language labels to 206k subtasks and nearly 2M total steering commands. See App. A for full details and all prompts used. 

The generated commands are used to train Steerable Policies by simply replacing the standard language during BC with a corresponding steering command (sampled uniformly at random across all commands for each frame). The resulting VLA can thus follow all command styles in Sec. IV-A necessary to produce generalizable behaviors, which we confirm in Sec. VI-A. In particular, we show that different command styles are suited to different tasks and situations, suggesting Steerable Polices generalize better. Indeed, we also find that choosing steering commands intelligently yields a substantial performance boost over a non-steerable baseline. 

V. HIERARCHICAL METHODS WITH STEERABLE POLICIES 

To fully realize the benefits of Steerable Policies, they must be integrated with VLMs that understand their affordances. We introduce two _high-level_ VLM policies that effectively leverage semantic knowledge and physical reasoning to issue steering commands. First, we investigate how embodied reasoning training can aid lightweight open-source VLMs to leverage their pretrained representations for controlling Steerable Policies. Second, we use the zero-shot in-context learning abilities of off-the-shelf VLMs for multi-step robotic problem-solving. Both methods are depicted in Fig. 4. 

## _A. Training High-level Embodied Reasoners_ 

Our first method trains a high-level embodied reasoning model to decompose tasks into steering commands, as shown in Fig. 4 (a). Specifically, we fine-tune a VLM to output appropriate steering commands for accomplishing a given task based on a task instruction and the current observation. Note that our command generation pipeline (Sec. IV-B) provides a mapping from tasks to appropriate commands, yielding the exact supervision necessary to train this model. 

To make better use of the base VLMs’ reasoning abilities and improve generalization, we also produce post-hoc rationales for _why_ each command is appropriate. For each subtask in every trajectory, we query Gemini with its starting frame, asking the VLM to explain why that subtask is needed to make progress (Fig. 3). See App. A-B for the full prompt used and more details. We then train the high-level policy via next-token prediction to reason about what the robot should do in each frame. During inference, the model autoregressively predicts a reasoning followed by a corresponding steering command, which our Steerable Policy follows for _N_ = 5 environment steps before re-querying the high-level reasoner. 

We expect this approach to be particularly effective for three main reasons. First, as the high-level reasoner’s learning objective (mapping from task language to natural language reasonings and steering commands) is similar to the base VLM’s pretraining objective, we expect it to readily transfer its generalizable representations to this new task. Second, since the low-level VLA only attends to steering commands, it learns fewer spurious biases between the task, reasoning, and action, compared to most unfactorized end-to-end models. Finally, since the high-level reasoner is queried less frequently than the VLA, it speeds up inference compared to standard embodied reasoning, even without any compilation techniques [51, 52]. 

_B. In-context Reasoning for Choosing Steering Abstractions_ 

Steerable Policies also enable a novel functionality: they permit many command styles, letting high-level models _choose_ which level of abstraction is best for inducing behaviors that progress a given task. Thus, in addition to reasoning about _what_ the robot should do, hierarchical systems using Steerable Policies have the added dimension of reasoning about _how_ to get the robot to do it. Our approach in Sec. V-A fine-tunes a model to map tasks to steering commands, but not necessarily those of the optimal style. Doing so requires (1) intuition about the strengths and weaknesses of each command style and (2) the ability to learn when each style is effective on the fly. We thus hypothesize that _off-the-shelf_ VLMs would excel at selecting command styles, due to their zero-shot proficiency with in-context learning and reasoning. 

We test this idea with the implementation shown in Fig. 4 (b). We query an API-based off-the-shelf VLM with the robot’s observation and an overall task. The VLM is told to issue commands to our Steerable Policy, based on examples of all the command styles and brief descriptions of their strengths and weaknesses. The model receives a history of images and executed commands in context, and is asked to (1) parse the current scene, (2) determine what the robot should do next, and (3) reason about the best level of abstraction for commanding the policy. Finally, it predicts a steering command for the Steerable Policy to follow for _N_ = 20 steps before the highlevel VLM is re-queried. See App. B for more details. 

Beyond emitting steering commands at a range of abstraction styles, our approach has several key innovations. Most significantly, the VLM can use _in-context learning_ to adapt its command choices, since it receives a sequential history of past 

observations and commands it has chosen. After selecting a steering abstraction, the VLM can observe the robot’s resulting behavior, then adjust the abstraction or command as needed. Critically, because in-context data points are produced by the VLM, it does not need hand-crafted examples of robot behaviors. Note that as in-context learning is used here to predict steering commands, not robot actions, the VLM’s task is thus akin to the “standard” vision-language in-context learning that VLMs are known to excel at. This obviates domain-specialized training or structured scene descriptions needed in prior robotic in-context learning works [53, 54]. 

Another benefit of our approach is that the VLM can use its scene understanding in conjunction with descriptions of each command style to reason about optimal steering abstractions. For instance, the VLM might produce visual inferences such as “the scene is cluttered,” leading to the selection of a pointing or motion command which allows for improved specificity. 

Naturally, as the above benefits stem from choosing steering abstractions, they are _not_ applicable to prior methods where VLMs control standard policies that accept only a single conditioning modality (e.g., task language [13, 10, 22] or traces [24–26]). Only Steerable Policies can fully bring these VLM capabilities to bear for robotic problem-solving. 

## VI. EXPERIMENTS 

**Research questions.** We now evaluate our Steerable Policies, both individually and as part of our two hierarchical control methods. We aim to answer: **(1)** Can steering commands effectively induce diverse compositional behaviors in Steerable Policies, yielding improved task performance? **(2)** How can Steerable Policies enable trained high-level VLMs to leverage embodied reasoning data for generalization? **(3)** How can Steerable Policies let us better apply in-context learning, scene understanding, and reasoning competencies in off-theshelf VLMs for solving long-horizon tasks? 

**Experimental setup.** We train Steerable Policies on the Bridge WidowX real-world robot manipulation dataset [4, 5, 55], allowing for evaluations consistent with past generalist policies [56, 10, 8, 9]. Following these works, we adapt the OpenVLA codebase to train our Steerable Policy (and embodied reasoner) with the standard Prismatic VLM 7B architecture [57, 10], but modified to map _steering commands_ (rather than standard task labels) and third-person RGB images to end effector actions. To show that Steerable Policies are applicable to many VLAs, we also fine-tune one from _π_ 0 _._ 5 [11], which we use in Sec. VI-B. See App. F for more details. 

For experiments in Sec. VI-A and Sec. VI-B, we measure performance over common generalization axes [10, 8, 9]: in-distribution, motion, spatial, and semantic generalization. When evaluating our in-context learning high-level policy formulation in Sec. VI-C, we additionally include unseen longer-horizon tasks. See App. C for full task details. 

_A. Diverse Steering Commands Induce Performant and Compositional Behaviors in Steerable Policies_ 

To improve the performance of learned hierarchical systems, the underlying policies must respond to a wider range of com- 


Fig. 5: Interactive interface for querying humans for oracle steering commands. **1:** The operator can interrupt the rollout to issue a new steering command. To facilitate giving commands with pixel coordinates, they can add textual placeholder markers. **2:** If any are given, a GUI is opened displaying the current robot observation, allowing the user to click to fill the markers in. **3:** Finally, the rollout resumes with the new command. 


Fig. 6: Allowing the oracle human user to issue _any_ command style to our Steerable Policy **nearly saturates performance** on Bridge. By restricting the user to each style alone, we find each one is suited to different task types. All individual styles are better than directly providing the task-level label that is used by regular VLAs. Error bars denote _±_ 1StdErr. 

mands beyond standard task-level language. Our first experiment evaluates whether our proposed steering commands are sufficiently expressive to induce the compositional behaviors necessary for Steerable Policies to solve a range of novel tasks. 

Specifically, we establish an achievable upper bound on performance by having a human act as an “oracle” high-level policy. This experiment serves as a didactic proof of existence showing that, given human-level scene understanding and reasoning, steering commands enable a Steerable Policy to attain high task performance. Following Shi et al. [33], the user may intervene by modifying the policy’s free-form steering command as needed (Fig. 5). However, they must wait _≥_ 2 seconds between interventions to reflect practical hierarchical systems that query the high-level policy less frequently than the low-level. This also prevents the user from “fully teleop- 

erating” the robot by repeatedly changing the command. 

We additionally repeat this experiment while restricting the user to a single command style at a time, including the ‘task-level” prompts used by standard VLAs. This isolates whether _individual_ steering modalities are sufficient for strong performance, and clarifies _when_ each style is most effective. 

Our results demonstrate that **a human oracle issuing unrestricted steering commands can solve all tasks at nearly 100% success rate** (Fig. 6). Even when constrained to a single command style, the user consistently outperforms task-level language alone. Additionally, we find that no single style dominates across settings: each exhibits complementary strengths and weaknesses. Optimal performance empirically requires access to a spectrum of prompt abstraction, supporting the claim that no one-size-fits-all steering modality exists. 

We observe several trends for when each style is effective. First, **_trace/point_** commands dominate in semantic generalization, as pointing allows the policy to know which out-ofdistribution objects to interact with, even if it fails to identify them by name. Next, **_atomic motion_** commands are best in tasks that reference spatial relations. When following motion commands, the policy remains on a manifold of “reasonable” actions – e.g., when prompted to “move left,” it servos left _towards an object_ , rather than moving left unconditionally (see App. E-B for more examples). As a result, when using a single steering modality, motions are the most effective. Finally, while **_task/subtask_** commands never perform best in any evaluation, they are especially reliable for _in-distribution_ parts of an overall task (e.g., reaching for non-novel objects). 

Overall, we find our Steerable Policy to be both responsive to different command styles and highly performant, particularly when given suitable steering commands leveraging _all_ command styles. However, selecting effective commands requires reasoning about the task, the scene, and the VLA’s capabilities. This motivates the novel hierarchical methods presented in Sec. V, which we evaluate below. 

## _B. Steerable Policies Enable VLMs to Effectively Use Embodied Reasoning Training_ 

We now evaluate if fine-tuning a VLM into a high-level policy is an effective way to leverage embodied reasoning to control Steerable Policies. Since our method involves fine-tuning the high-level to produce embodied reasonings and intermediate goals, we compare against three prior methods that use reasoning data to improve VLAs (all built on OpenVLA): **_Embodied Chain-of-Thought Reasoning (ECoT)_** [8] and the two **_ECoT-Lite_** variants, which learn representations from robot reasonings, but do not generate them during inference [9]. We also include a non-reasoning ablation, where the fine-tuned VLM outputs steering commands directly. Finally, we compare against equivalent non-reasoning **_“standard” OpenVLA and_** _π_ 0 _._ 5 **_baselines_** [10, 11]. All methods are evaluated on the same Bridge tasks used in ECoT-Lite, which were chosen to probe several axes of generalization. For fairness, we control for training demonstrations and architectures; the policies differ only in how embodied reasoning is incorporated. 


Fig. 8: In-context learning VLMs can effectively select abstractions for instructing our Steerable Policy. Error bars denote _±_ 1StdErr. Steerability allows VLMs to better apply their reasoning and in-context learning skills, in ways the standard SayCanlike paradigm (where the VLM interfaces with the VLA via subtasks alone) fails to take advantage of (Sec. VI-C). To better highlight these capabilities, we measure task progression on challenging _multi-step_ Bridge tasks. 

As shown in Fig. 7, _our approach outperforms all baselines_ . The gains are most pronounced on motion and semantic generalization tasks, likely because atomic motion, trace, and pointing commands allow the generalizable reasoner to reliably control the Steerable Policy under distribution shift. 

**High-level VLM reasoning benefits Steerable Policies based on different VLA architectures.** While the “standard” Bridge _π_ 0 _._ 5 baseline outperforms the OpenVLA equivalent (likely due to having better base representations for control), applying our method to _π_ 0 _._ 5- _or_ OpenVLA-based Steerable Policies still outperforms both baselines, showing that _steerability unlocks performance gains from VLM reasoning, even for modern VLA architectures_ . Both Steerable Policies achieve similar performance when using our approach. 

**Fine-tuned high-level VLMs benefit from reasoning.** While not as effective as our full approach, ablating reasoning from our method still greatly outperforms standard OpenVLA and is on-par with ECoT-Lite, despite being trained on the same robot interactions. This suggests that there are performance benefits to hierarchical control schemes with Steerable Policies over end-to-end policies, _even if the high-level is not explicitly trained to reason_ . Still, we find that embodied reasoning is important for generalization and performance. Note that VLMs’ off-the-shelf reasoning abilities can be used to achieve the same benefit, which we discuss below. 

_C. Steerable Policies Unlock In-context Reasoning in VLMs_ 

Finally, we investigate if off-the-shelf VLMs can better use their in-context reasoning faculties when interfacing with 

Steerable Policies. We define a distinct suite of multi-step tasks that demand reasoning over long-horizon executions. See App. C-C for task details and rubrics. 

The key advantage of using Steerable Policies is that they allow high-level VLMs to reason about and flexibly choose the best abstraction for prompting low-level VLAs. Our primary baseline is therefore a **_SayCan-like_** [1] method, representing a standard approach where an off-the-shelf VLM commands the VLA through subtask language alone. For fairness, this baseline uses the same history and system prompt as our method, differing only in that the VLM is restricted to a single level of steering abstraction. We expect this to hinder the impact of in-context reasoning, lowering performance. We also include a **_standard Bridge OpenVLA_** comparison to assess if our tasks are sufficiently challenging for non-hierarchical policies. Finally, to isolate the role of explicit reasoning, we include a **_non-reasoning ablation_** where the VLM outputs steering commands without any intermediate generation. All hierarchical methods use Gemini 3.0 [50] as the VLM. More details and prompts for all methods are shown in App. B. 

As shown in Fig. 8, our approach universally outperforms OpenVLA and SayCan-like baselines. Since the latter differs only in being restricted to subtask-level prompts, the performance gap primarily reflects the benefit of allowing the VLM to access the full spectrum of steering abstractions during in-context reasoning. Our method also outperforms the nonreasoning ablation, though the gap is smaller. This suggests that, while explicit reasoning is helpful, in-context learning 


(a) The VLM uses in-context learning to “discover” what steering abstraction is best. A pointing command leads to incorrect behavior, so the VLM employs a motion command instead. 


(b) The VLM uses in-context learning to adjust the abstraction when task progress stalls. Subtask ("lift the mushroom up") and motion ("move down and close gripper onto the mushroom") commands were ineffective, so the VLM points instead. 


(c) The VLM demonstrates fine-grained semantic and physical understanding to issue a corrective command. 


(d) Given an observation, the VLM reasons about which steering abstraction is most appropriate, based on each one’s strengths. 

Fig. 9: Example reasonings when using an in-context learning VLM for controlling our Steerable Policies. 

VLMs are already adept at issuing effective steering commands without intermediate “thinking.” We further observe that using in-context reasoning to steer our VLA leads to several qualitative advantages, shown below and in Fig. 9. 

**In-context learning enables corrective steering.** Even when the VLM initially picks poor steering commands, we find it can use in-context learning to improve commands by changing the abstraction level. This is especially salient when a command leads to an error (Fig. 9a) or is ineffective and fails to progress the task (Fig. 9b). In either case, the VLM reasons over history to learn the affordances of the VLA and change its prompting strategy to complete the task. 

**Steerability better applies VLM understanding.** Interfacing with a Steerable Policy allows the VLM to translate its scene understanding and in-context history into actionable corrections that are difficult to induce in a standard VLA accepting task-level language alone. In Fig. 9c, the VLM uses _semantic_ understanding to observe that the robot grasps the wrong object when instructed to reach for the hammer. It 

further reasons with granular _physical_ understanding, recognizing that the end effector must have sufficient clearance to disengage the current object and move above the correct one. It uses this understanding in conjunction with past behavioral and semantic failure modes to ground its final steering command: "move right and up to the hammer handle". 

Crucially, the VLM often cannot capitalize on such insights with subtask commands alone. A common failure mode of the SayCan-like baseline is that, even when the VLM correctly diagnoses errors, subtasks lack the specificity required to resolve them. In the same example (Fig. 9c), the VLM may recognize that the robot has confused a mushroom for the hammer and issue "drop the mushroom". However, since a non-steerable VLA cannot understand motion commands such as "move up and right", the VLM can only reissue the subtask command "reach for the hammer", causing the robot to repeat the same mistake. In short, even if the VLM has the capacity for nuanced scene understanding, it cannot act on this knowledge with subtask commands alone, requiring a low-level Steerable Policy instead (see App. E-C). 

**VLMs can reason about steering abstractions.** Beyond reasoning about _what_ the robot should do, VLMs can also reason about _how_ to best induce the desired behavior (i.e., what steering style to use). In Fig. 9d, when reaching for a banana in a cluttered scene, the VLM determines that a pointing command is the least ambiguous option and issues "move above <banana position>". After observing that the robot is correctly above the banana, it switches to a higherlevel instruction, "grasp the banana". This demonstrates that VLMs can dynamically select and sequence steering abstractions based on the current state. 

## VII. DISCUSSION AND FUTURE WORK 

We introduce Steerable Policies: VLAs that support a wide range of command abstractions including subtasks, motions, and grounded pixel coordinates. We show how improved steerability enables better transfer of VLM capabilities into robotics by (1) fine-tuning high-level VLMs on embodied reasoning data to solve generalization tasks with our Steerable Policy, and (2) using the in-context learning abilities of offthe-shelf VLMs for multi-step robotic problem-solving. 

As robot datasets have trended toward scaling their behavioral diversity, we expect Steerable Policies to only increase in applicability. The compositionality afforded by steering also becomes more important as task complexity increases, e.g., when moving to open-world settings. To support this, VLMs require an even better grasp of the affordances provided by Steerable Policies. Beyond zero-shot prompting, VLMs could _learn_ these affordances via reinforcement learning, as rollouts would allow models to elucidate when each steering style is effective. This may also provide the data needed for cross-task in-context learning, where the VLM transfers its understanding of affordances to new situations. We hope that Steerable Policies will represent a step toward finally bringing the “disembodied” capabilities of VLMs to the physical world. 

## ACKNOWLEDGEMENTS 

We thank Qiyang Li for assistance with the teaser diagram. We also thank Ameesh Shah, Arhan Jain, and members of the RAIL Lab for insightful discussions. This research was partly supported by ONR N00014-25-1-2060, NSF IIS-2246811, and DARPA ANSR, with additional support from Google and the NVIDIA Academic Grant Program. 

## REFERENCES 

- [1] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Daniel Ho, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Eric Jang, Rosario Jauregui Ruano, Kyle Jeffrey, Sally Jesmonth, Nikhil J Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Kuang-Huei Lee, Sergey Levine, Yao Lu, Linda Luu, Carolina Parada, Peter Pastor, Jornell Quiambao, Kanishka Rao, Jarek Rettinghouse, Diego Reyes, Pierre Sermanet, Nicolas Sievers, Clayton Tan, Alexander Toshev, Vincent Vanhoucke, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Mengyuan Yan, and Andy Zeng. Do as i can, not as i say: Grounding language in robotic affordances, 2022. 

- [2] Lucy Xiaoyang Shi, Brian Ichter, Michael Equi, Liyiming Ke, Karl Pertsch, Quan Vuong, James Tanner, Anna Walling, Haohuan Wang, Niccolo Fusai, Adrian Li-Bell, Danny Driess, Lachy Groom, Sergey Levine, and Chelsea Finn. Hi robot: Open-ended instruction following with hierarchical vision-language-action models, 2025. URL https://arxiv.org/abs/2502.19417. 

- [3] Selma Wanna, Agnes Luhtaru, Jonathan Salfity, Ryan Barron, Juston Moore, Cynthia Matuszek, and Mitch Pryor. Limited linguistic diversity in embodied ai datasets, 2026. URL https://arxiv.org/abs/2601.03136. 

- [4] Frederik Ebert, Yanlai Yang, Karl Schmeckpeper, Bernadette Bucher, Georgios Georgakis, Kostas Daniilidis, Chelsea Finn, and Sergey Levine. Bridge data: Boosting generalization of robotic skills with crossdomain datasets, 2021. 

- [5] Homer Walke, Kevin Black, Abraham Lee, Moo Jin Kim, Max Du, Chongyi Zheng, Tony Zhao, Philippe HansenEstruch, Quan Vuong, Andre He, Vivek Myers, Kuan Fang, Chelsea Finn, and Sergey Levine. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning (CoRL)_ , 2023. 

- [6] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language models, 2023. 

- [7] Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. Large language models are zero-shot reasoners, 2023. 

- [8] Michał Zawalski, William Chen, Karl Pertsch, Oier Mees, Chelsea Finn, and Sergey Levine. Robotic control via embodied chain-of-thought reasoning. In _Conference on Robot Learning_ , 2024. 

- [9] William Chen, Suneel Belkhale, Suvir Mirchandani, Oier Mees, Danny Driess, Karl Pertsch, and Sergey Levine. Training strategies for efficient embodied reasoning, 2025. 

- [10] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. 2024. 

- [11] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with open-world generalization, 2025. 

- [12] Rishi Bommasani, Drew A. Hudson, Ehsan Adeli, Russ Altman, Simran Arora, Sydney von Arx, Michael S. Bernstein, Jeannette Bohg, Antoine Bosselut, Emma Brunskill, Erik Brynjolfsson, Shyamal Buch, Dallas Card, Rodrigo Castellon, Niladri Chatterji, Annie Chen, Kathleen Creel, Jared Quincy Davis, Dora Demszky, Chris Donahue, Moussa Doumbouya, Esin Durmus, Stefano Ermon, John Etchemendy, Kawin Ethayarajh, Li Fei-Fei, Chelsea Finn, Trevor Gale, Lauren Gillespie, Karan Goel, Noah Goodman, Shelby Grossman, Neel Guha, Tatsunori Hashimoto, Peter Henderson, John Hewitt, Daniel E. Ho, Jenny Hong, Kyle Hsu, Jing Huang, Thomas Icard, Saahil Jain, Dan Jurafsky, Pratyusha Kalluri, Siddharth Karamcheti, Geoff Keeling, Fereshte Khani, Omar Khattab, Pang Wei Koh, Mark Krass, Ranjay Krishna, Rohith Kuditipudi, Ananya Kumar, Faisal Ladhak, Mina Lee, Tony Lee, Jure Leskovec, Isabelle Levent, Xiang Lisa Li, Xuechen Li, Tengyu Ma, Ali Malik, Christopher D. Manning, Suvir Mirchandani, Eric Mitchell, Zanele Munyikwa, Suraj Nair, Avanika Narayan, Deepak Narayanan, Ben Newman, Allen Nie, Juan Carlos Niebles, Hamed Nilforoshan, Julian Nyarko, Giray Ogut, Laurel Orr, Isabel Papadimitriou, Joon Sung Park, Chris Piech, Eva Portelance, Christopher Potts, Aditi Raghunathan, Rob Reich, Hongyu Ren, Frieda Rong, Yusuf Roohani, Camilo Ruiz, Jack Ryan, Christopher R´e, Dorsa Sadigh, Shiori Sagawa, Keshav Santhanam, Andy Shih, Krishnan Srinivasan, Alex Tamkin, Rohan Taori, Armin W. Thomas, Florian Tram`er, Rose E. Wang, William Wang, Bohan Wu, Jiajun Wu, Yuhuai Wu, Sang Michael Xie, Michihiro Yasunaga, Jiaxuan You, Matei Zaharia, Michael Zhang, Tianyi Zhang, Xikun Zhang, Yuhui Zhang, Lucia Zheng, Kaitlyn Zhou, and Percy Liang. On the opportunities and risks of foundation 

models, 2022. 

- [13] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, Pete Florence, Chuyuan Fu, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Kehang Han, Karol Hausman, Alexander Herzog, Jasmine Hsu, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Lisa Lee, Tsang-Wei Edward Lee, Sergey Levine, Yao Lu, Henryk Michalewski, Igor Mordatch, Karl Pertsch, Kanishka Rao, Krista Reymann, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Pierre Sermanet, Jaspiar Singh, Anikait Singh, Radu Soricut, Huong Tran, Vincent Vanhoucke, Quan Vuong, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Jialin Wu, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. Rt-2: Vision-language-action models transfer web knowledge to robotic control, 2023. 

- [14] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models, 2025. URL https://arxiv.org/abs/2501.09747. 

- [15] Suneel Belkhale and Dorsa Sadigh. Minivla: A better vla with a smaller footprint, 2024. URL https://ai.stanford. edu/blog/minivla/. 

- [16] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control, 2024. URL https://arxiv.org/abs/2410.24164. 

- [17] Moo Jin Kim, Chelsea Finn, and Percy Liang. Finetuning vision-language-action models: Optimizing speed and success, 2025. URL https://arxiv.org/abs/2502. 19645. 

- [18] Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, Steven Bohez, Konstantinos Bousmalis, Anthony Brohan, Thomas Buschmann, Arunkumar Byravan, Serkan Cabi, Ken Caluwaerts, Federico Casarini, Oscar Chang, Jose Enrique Chen, Xi Chen, Hao-Tien Lewis Chiang, Krzysztof Choromanski, David D’Ambrosio, Sudeep Dasari, Todor Davchev, Coline Devin, Norman Di Palo, Tianli Ding, Adil Dostmohamed, Danny Driess, Yilun Du, Debidatta Dwibedi, Michael Elabd, Claudio Fantacci, Cody Fong, Erik Frey, Chuyuan Fu, Marissa Giustina, Keerthana Gopalakrishnan, Laura Graesser, Leonard Hasenclever, Nicolas Heess, Brandon Hernaez, Alexander Herzog, R. Alex Hofer, Jan Humplik, Atil Iscen, Mithun George Jacob, Deepali Jain, Ryan Julian, Dmitry Kalashnikov, 

M. Emre Karagozler, Stefani Karp, Chase Kew, Jerad Kirkland, Sean Kirmani, Yuheng Kuang, Thomas Lampe, Antoine Laurens, Isabel Leal, Alex X. Lee, TsangWei Edward Lee, Jacky Liang, Yixin Lin, Sharath Maddineni, Anirudha Majumdar, Assaf Hurwitz Michaely, Robert Moreno, Michael Neunert, Francesco Nori, Carolina Parada, Emilio Parisotto, Peter Pastor, Acorn Pooley, Kanishka Rao, Krista Reymann, Dorsa Sadigh, Stefano Saliceti, Pannag Sanketi, Pierre Sermanet, Dhruv Shah, Mohit Sharma, Kathryn Shea, Charles Shu, Vikas Sindhwani, Sumeet Singh, Radu Soricut, Jost Tobias Springenberg, Rachel Sterneck, Razvan Surdulescu, Jie Tan, Jonathan Tompson, Vincent Vanhoucke, Jake Varley, Grace Vesom, Giulia Vezzani, Oriol Vinyals, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Fei Xia, Ted Xiao, Annie Xie, Jinyu Xie, Peng Xu, Sichun Xu, Ying Xu, Zhuo Xu, Yuxiang Yang, Rui Yao, Sergey Yaroshenko, Wenhao Yu, Wentao Yuan, Jingwei Zhang, Tingnan Zhang, Allan Zhou, and Yuxiang Zhou. Gemini robotics: Bringing ai into the physical world, 2025. URL https://arxiv.org/abs/2503.20020. 

- [19] Catherine Glossop, William Chen, Arjun Bhorkar, Dhruv Shah, and Sergey Levine. Cast: Counterfactual labels improve instruction following in vision-language-action models, 2025. URL https://arxiv.org/abs/2508.13446. 

- [20] Ted Xiao, Harris Chan, Pierre Sermanet, Ayzaan Wahid, Anthony Brohan, Karol Hausman, Sergey Levine, and Jonathan Tompson. Robotic skill acquisition via instruction augmentation with vision-language models, 2022. 

- [21] Laura Smith, Alex Irpan, Montserrat Gonzalez Arenas, Sean Kirmani, Dmitry Kalashnikov, Dhruv Shah, and Ted Xiao. Steer: Flexible robotic manipulation via dense language grounding, 2024. URL https://arxiv.org/abs/ 2411.03409. 

- [22] Jesse Zhang, Karl Pertsch, Jiahui Zhang, and Joseph J. Lim. Sprint: Scalable policy pre-training via language instruction relabeling, 2024. URL https://arxiv.org/abs/ 2306.11886. 

- [23] Corey Lynch, Ayzaan Wahid, Jonathan Tompson, Tianli Ding, James Betker, Robert Baruch, Travis Armstrong, and Pete Florence. Interactive language: Talking to robots in real time, 2022. 

- [24] Yi Li, Yuquan Deng, Jesse Zhang, Joel Jang, Marius Memmel, Raymond Yu, Caelan Reed Garrett, Fabio Ramos, Dieter Fox, Anqi Li, Abhishek Gupta, and Ankit Goyal. Hamster: Hierarchical action models for openworld robot manipulation, 2025. URL https://arxiv.org/ abs/2502.05485. 

- [25] Jiayuan Gu, Sean Kirmani, Paul Wohlhart, Yao Lu, Montserrat Gonzalez Arenas, Kanishka Rao, Wenhao Yu, Chuyuan Fu, Keerthana Gopalakrishnan, Zhuo Xu, Priya Sundaresan, Peng Xu, Hao Su, Karol Hausman, Chelsea Finn, Quan Vuong, and Ted Xiao. Rt-trajectory: Robotic task generalization via hindsight trajectory sketches, 2023. URL https://arxiv.org/abs/2311.01977. 

- [26] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng 

Gao, Hal Daum´e III, Andrey Kolobov, Furong Huang, and Jianwei Yang. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies, 2025. URL https://arxiv.org/abs/2412.10345. 

- [27] Noriaki Hirose, Catherine Glossop, Dhruv Shah, and Sergey Levine. Omnivla: An omni-modal visionlanguage-action model for robot navigation, 2025. URL https://arxiv.org/abs/2509.19480. 

- [28] Jason Lee, Jiafei Duan, Haoquan Fang, Yuquan Deng, Shuo Liu, Boyang Li, Bohan Fang, Jieyu Zhang, Yi Ru Wang, Sangho Lee, Winson Han, Wilbert Pumacay, Angelica Wu, Rose Hendrix, Karen Farley, Eli VanderBilt, Ali Farhadi, Dieter Fox, and Ranjay Krishna. Molmoact: Action reasoning models that can reason in space, 2025. URL https://arxiv.org/abs/2508.07917. 

- [29] James Betker, Gabriel Goh, Li Jing, Tim Brooks, Jianfeng Wang, Linjie Li, LongOuyang, Juntang Zhuang, Joyce Lee, Yufei Guo, Wesam Manassra, Prafulla Dhariwal, Casey Chu, Yunxin Jiao, and Aditya Ramesh. Improving image generation with better captions. 2023. 

- [30] Caelan Reed Garrett, Rohan Chitnis, Rachel Holladay, Beomjoon Kim, Tom Silver, Leslie Pack Kaelbling, and Tom´as Lozano-P´erez. Integrated task and motion planning, 2020. 

- [31] Daniel Kahneman. _Thinking, fast and slow_ . Farrar, Straus and Giroux, 2011. 

- [32] Jyh-Jing Hwang, Runsheng Xu, Hubert Lin, Wei-Chih Hung, Jingwei Ji, Kristy Choi, Di Huang, Tong He, Paul Covington, Benjamin Sapp, Yin Zhou, James Guo, Dragomir Anguelov, and Mingxing Tan. Emma: Endto-end multimodal model for autonomous driving, 2024. URL https://arxiv.org/abs/2410.23262. 

- [33] Lucy Xiaoyang Shi, Zheyuan Hu, Tony Z. Zhao, Archit Sharma, Karl Pertsch, Jianlan Luo, Sergey Levine, and Chelsea Finn. Yell at your robot: Improving on-the-fly from language corrections, 2024. 

- [34] Boyi Li, Philipp Wu, Pieter Abbeel, and Jitendra Malik. Interactive task planning with language models, 2025. URL https://arxiv.org/abs/2310.10645. 

- [35] Dhruv Shah, Blazej Osinski, Brian Ichter, and Sergey Levine. Lm-nav: Robotic navigation with large pretrained models of language, vision, and action, 2022. URL https://arxiv.org/abs/2207.04429. 

- [36] Wenlong Huang, Pieter Abbeel, Deepak Pathak, and Igor Mordatch. Language models as zero-shot planners: Extracting actionable knowledge for embodied agents, 2022. URL https://arxiv.org/abs/2201.07207. 

- [37] Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, Pierre Sermanet, Noah Brown, Tomas Jackson, Linda Luu, Sergey Levine, Karol Hausman, and Brian Ichter. Inner monologue: Embodied reasoning through planning with language models, 2022. 

- [38] Andy Zeng, Maria Attarian, Brian Ichter, Krzysztof Choromanski, Adrian Wong, Stefan Welker, Federico Tombari, Aveek Purohit, Michael Ryoo, Vikas Sind- 

hwani, Johnny Lee, Vincent Vanhoucke, and Pete Florence. Socratic models: Composing zero-shot multimodal reasoning with language, 2022. 

- [39] Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, Yevgen Chebotar, Pierre Sermanet, Daniel Duckworth, Sergey Levine, Vincent Vanhoucke, Karol Hausman, Marc Toussaint, Klaus Greff, Andy Zeng, Igor Mordatch, and Pete Florence. Palm-e: An embodied multimodal language model, 2023. 

- [40] Jesse Zhang, Jiahui Zhang, Karl Pertsch, Ziyi Liu, Xiang Ren, Minsuk Chang, Shao-Hua Sun, and Joseph J. Lim. Bootstrap your own skills: Learning to solve new tasks with large language model guidance, 2023. URL https: //arxiv.org/abs/2310.10021. 

- [41] Huy Ha, Pete Florence, and Shuran Song. Scaling up and distilling down: Language-guided robot skill acquisition, 2023. 

- [42] Suneel Belkhale, Tianli Ding, Ted Xiao, Pierre Sermanet, Quon Vuong, Jonathan Tompson, Yevgen Chebotar, Debidatta Dwibedi, and Dorsa Sadigh. Rt-h: Action hierarchies using language, 2024. 

- [43] Yi Yang, Jiaxuan Sun, Siqi Kou, Yihan Wang, and Zhijie Deng. Lohovla: A unified vision-language-action model for long-horizon embodied tasks, 2025. URL https://arxiv.org/abs/2506.00411. 

- [44] Markus Peschl, Pietro Mazzaglia, and Daniel Dijkman. From code to action: Hierarchical learning of diffusionvlm policies, 2025. URL https://arxiv.org/abs/2509. 24917. 

- [45] Huang Fang, Mengxi Zhang, Heng Dong, Wei Li, Zixuan Wang, Qifeng Zhang, Xueyun Tian, Yucheng Hu, and Hang Li. Robix: A unified model for robot interaction, reasoning and planning, 2025. URL https://arxiv.org/abs/ 2509.01106. 

- [46] Tao Jiang, Tianyuan Yuan, Yicheng Liu, Chenhao Lu, Jianning Cui, Xiao Liu, Shuiqi Cheng, Jiyang Gao, Huazhe Xu, and Hang Zhao. Galaxea open-world dataset and g0 dual-system vla model, 2025. URL https://arxiv.org/abs/2509.00576. 

- [47] Matt Deitke, Christopher Clark, Sangho Lee, Rohun Tripathi, Yue Yang, Jae Sung Park, Mohammadreza Salehi, Niklas Muennighoff, Kyle Lo, Luca Soldaini, Jiasen Lu, Taira Anderson, Erin Bransom, Kiana Ehsani, Huong Ngo, YenSung Chen, Ajay Patel, Mark Yatskar, Chris Callison-Burch, Andrew Head, Rose Hendrix, Favyen Bastani, Eli VanderBilt, Nathan Lambert, Yvonne Chou, Arnavi Chheda, Jenna Sparks, Sam Skjonsberg, Michael Schmitz, Aaron Sarnat, Byron Bischoff, Pete Walsh, Chris Newell, Piper Wolters, Tanmay Gupta, Kuo-Hao Zeng, Jon Borchardt, Dirk Groeneveld, Crystal Nam, Sophie Lebrecht, Caitlin Wittlif, Carissa Schoenick, Oscar Michel, Ranjay Krishna, Luca Weihs, Noah A. Smith, Hannaneh Hajishirzi, Ross Girshick, Ali Farhadi, and Aniruddha Kembhavi. Molmo and pixmo: Open weights 

and open data for state-of-the-art vision-language models, 2024. URL https://arxiv.org/abs/2409.17146. 

- [48] Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr, Roman R¨adle, Chloe Rolland, Laura Gustafson, Eric Mintun, Junting Pan, Kalyan Vasudev Alwala, Nicolas Carion, Chao-Yuan Wu, Ross Girshick, Piotr Doll´ar, and Christoph Feichtenhofer. Sam 2: Segment anything in images and videos, 2024. URL https://arxiv.org/abs/2408. 00714. 

- [49] Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas Usunier, Alexander Kirillov, and Sergey Zagoruyko. End-to-end object detection with transformers, 2020. URL https://arxiv.org/abs/2005.12872. 

- [50] Gemini Team. Gemini: A family of highly capable multimodal models, 2024. 

- [51] William Chen, Michał Zawalski, Karl Pertsch, Oier Mees, Chelsea Finn, and Sergey Levine. Tensorrtopenvla, 2025. URL https://github.com/rail-berkeley/ tensorrt-openvla. 

- [52] NVIDIA. Tensorrt-llm. https://github.com/NVIDIA/ TensorRT-LLM?tab=readme-ov-file, 2024. 

- [53] Letian Fu, Huang Huang, Gaurav Datta, Lawrence Yunliang Chen, William Chung-Ho Panitch, Fangchen Liu, Hui Li, and Ken Goldberg. In-context imitation learning via next-token prediction. _arXiv preprint arXiv:2408.15980_ , 2024. 

- [54] Yida Yin, Zekai Wang, Yuvan Sharma, Dantong Niu, Trevor Darrell, and Roei Herzig. In-context learning enables robot action prediction in llms, 2025. URL https://arxiv.org/abs/2410.12782. 

- [55] Embodiment Collaboration, Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, Albert Tung, Alex Bewley, Alex Herzog, Alex Irpan, Alexander Khazatsky, Anant Rai, Anchit Gupta, Andrew Wang, Andrey Kolobov, Anikait Singh, Animesh Garg, Aniruddha Kembhavi, Annie Xie, Anthony Brohan, Antonin Raffin, Archit Sharma, Arefeh Yavary, Arhan Jain, Ashwin Balakrishna, Ayzaan Wahid, Ben Burgess-Limerick, Beomjoon Kim, Bernhard Sch¨olkopf, Blake Wulfe, Brian Ichter, Cewu Lu, Charles Xu, Charlotte Le, Chelsea Finn, Chen Wang, Chenfeng Xu, Cheng Chi, Chenguang Huang, Christine Chan, Christopher Agia, Chuer Pan, Chuyuan Fu, Coline Devin, Danfei Xu, Daniel Morton, Danny Driess, Daphne Chen, Deepak Pathak, Dhruv Shah, Dieter B¨uchler, Dinesh Jayaraman, Dmitry Kalashnikov, Dorsa Sadigh, Edward Johns, Ethan Foster, Fangchen Liu, Federico Ceola, Fei Xia, Feiyu Zhao, Felipe Vieira Frujeri, Freek Stulp, Gaoyue Zhou, Gaurav S. Sukhatme, Gautam Salhotra, Ge Yan, Gilbert Feng, Giulio Schiavi, Glen Berseth, Gregory Kahn, Guanzhi Wang, Hao Su, Hao-Shu Fang, Haochen Shi, Henghui Bao, Heni Ben Amor, Henrik I Christensen, Hiroki Furuta, Homer Walke, Hongjie Fang, Huy Ha, 

Igor Mordatch, Ilija Radosavovic, Isabel Leal, Jacky Liang, Jad Abou-Chakra, Jaehyung Kim, Jaimyn Drake, Jan Peters, Jan Schneider, Jasmine Hsu, Jeannette Bohg, Jeffrey Bingham, Jeffrey Wu, Jensen Gao, Jiaheng Hu, Jiajun Wu, Jialin Wu, Jiankai Sun, Jianlan Luo, Jiayuan Gu, Jie Tan, Jihoon Oh, Jimmy Wu, Jingpei Lu, Jingyun Yang, Jitendra Malik, Jo˜ao Silv´erio, Joey Hejna, Jonathan Booher, Jonathan Tompson, Jonathan Yang, Jordi Salvador, Joseph J. Lim, Junhyek Han, Kaiyuan Wang, Kanishka Rao, Karl Pertsch, Karol Hausman, Keegan Go, Keerthana Gopalakrishnan, Ken Goldberg, Kendra Byrne, Kenneth Oslund, Kento Kawaharazuka, Kevin Black, Kevin Lin, Kevin Zhang, Kiana Ehsani, Kiran Lekkala, Kirsty Ellis, Krishan Rana, Krishnan Srinivasan, Kuan Fang, Kunal Pratap Singh, Kuo-Hao Zeng, Kyle Hatch, Kyle Hsu, Laurent Itti, Lawrence Yunliang Chen, Lerrel Pinto, Li Fei-Fei, Liam Tan, Linxi ”Jim” Fan, Lionel Ott, Lisa Lee, Luca Weihs, Magnum Chen, Marion Lepert, Marius Memmel, Masayoshi Tomizuka, Masha Itkina, Mateo Guaman Castro, Max Spero, Maximilian Du, Michael Ahn, Michael C. Yip, Mingtong Zhang, Mingyu Ding, Minho Heo, Mohan Kumar Srirama, Mohit Sharma, Moo Jin Kim, Naoaki Kanazawa, Nicklas Hansen, Nicolas Heess, Nikhil J Joshi, Niko Suenderhauf, Ning Liu, Norman Di Palo, Nur Muhammad Mahi Shafiullah, Oier Mees, Oliver Kroemer, Osbert Bastani, Pannag R Sanketi, Patrick ”Tree” Miller, Patrick Yin, Paul Wohlhart, Peng Xu, Peter David Fagan, Peter Mitrano, Pierre Sermanet, Pieter Abbeel, Priya Sundaresan, Qiuyu Chen, Quan Vuong, Rafael Rafailov, Ran Tian, Ria Doshi, Roberto Mart’in-Mart’in, Rohan Baijal, Rosario Scalise, Rose Hendrix, Roy Lin, Runjia Qian, Ruohan Zhang, Russell Mendonca, Rutav Shah, Ryan Hoque, Ryan Julian, Samuel Bustamante, Sean Kirmani, Sergey Levine, Shan Lin, Sherry Moore, Shikhar Bahl, Shivin Dass, Shubham Sonawani, Shuran Song, Sichun Xu, Siddhant Haldar, Siddharth Karamcheti, Simeon Adebola, Simon Guist, Soroush Nasiriany, Stefan Schaal, Stefan Welker, Stephen Tian, Subramanian Ramamoorthy, Sudeep Dasari, Suneel Belkhale, Sungjae Park, Suraj Nair, Suvir Mirchandani, Takayuki Osa, Tanmay Gupta, Tatsuya Harada, Tatsuya Matsushima, Ted Xiao, Thomas Kollar, Tianhe Yu, Tianli Ding, Todor Davchev, Tony Z. Zhao, Travis Armstrong, Trevor Darrell, Trinity Chung, Vidhi Jain, Vincent Vanhoucke, Wei Zhan, Wenxuan Zhou, Wolfram Burgard, Xi Chen, Xiangyu Chen, Xiaolong Wang, Xinghao Zhu, Xinyang Geng, Xiyuan Liu, Xu Liangwei, Xuanlin Li, Yansong Pang, Yao Lu, Yecheng Jason Ma, Yejin Kim, Yevgen Chebotar, Yifan Zhou, Yifeng Zhu, Yilin Wu, Ying Xu, Yixuan Wang, Yonatan Bisk, Yoonyoung Cho, Youngwoon Lee, Yuchen Cui, Yue Cao, Yueh-Hua Wu, Yujin Tang, Yuke Zhu, Yunchu Zhang, Yunfan Jiang, Yunshuang Li, Yunzhu Li, Yusuke Iwasawa, Yutaka Matsuo, Zehan Ma, Zhuo Xu, Zichen Jeff Cui, Zichen Zhang, Zipeng Fu, 

and Zipeng Lin. Open x-embodiment: Robotic learning datasets and rt-x models, 2024. 

- [56] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, 2024. 

- [57] Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa Sadigh. Prismatic vlms: Investigating the design space of visuallyconditioned language models, 2024. 

- [58] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, Thomas Unterthiner, Daniel Keysers, Skanda Koppula, Fangyu Liu, Adam Grycner, Alexey Gritsenko, Neil Houlsby, Manoj Kumar, Keran Rong, Julian Eisenschlos, Rishabh Kabra, Matthias Bauer, Matko Boˇsnjak, Xi Chen, Matthias Minderer, Paul Voigtlaender, Ioana Bica, Ivana Balazevic, Joan Puigcerver, Pinelopi Papalampidi, Olivier Henaff, Xi Xiong, Radu Soricut, Jeremiah Harmsen, and Xiaohua Zhai. Paligemma: A versatile 3b vlm for transfer, 2024. URL https://arxiv.org/abs/2407.07726. 

- [59] Prafulla Dhariwal and Alex Nichol. Diffusion models beat gans on image synthesis, 2021. URL https://arxiv. org/abs/2105.05233. 

- [60] Jonathan Ho and Tim Salimans. Classifier-free diffusion guidance, 2022. 

- [61] Yanwei Wang, Lirui Wang, Yilun Du, Balakumar Sundaralingam, Xuning Yang, Yu-Wei Chao, Claudia PerezD’Arpino, Dieter Fox, and Julie Shah. Inference-time policy steering through human interactions, 2024. 

- [62] Mitsuhiko Nakamoto, Oier Mees, Aviral Kumar, and Sergey Levine. Steering your generalists: Improving robotic foundation models via value guidance. _Conference on Robot Learning (CoRL)_ , 2024. 

- [63] Andrew Wagenmaker, Mitsuhiko Nakamoto, Yunchu Zhang, Seohong Park, Waleed Yagoub, Anusha Nagabandi, Abhishek Gupta, and Sergey Levine. Steering your diffusion policy with latent space reinforcement learning, 2025. URL https://arxiv.org/abs/2506.15799. 

- [64] Kevin Frans, Seohong Park, Pieter Abbeel, and Sergey Levine. Diffusion guidance is a controllable policy improvement operator, 2025. URL https://arxiv.org/abs/ 2505.23458. 

- [65] Xiang Lisa Li and Percy Liang. Prefix-tuning: Optimizing continuous prompts for generation, 2021. URL https://arxiv.org/abs/2101.00190. 

- [66] Jacky Kwok, Christopher Agia, Rohan Sinha, Matt Foutter, Shulu Li, Ion Stoica, Azalia Mirhoseini, and Marco Pavone. Robomonkey: Scaling test-time sampling and verification for vision-language-action models, 2025. 

URL https://arxiv.org/abs/2506.17811. 

- [67] Maximilian Du and Shuran Song. Dynaguide: Steering diffusion policies with active dynamic guidance. In _Proceedings of the 39th Conference on Neural Information Processing Systems (NeurIPS)_ , 2025. 

- [68] Yilin Wu, Ran Tian, Gokul Swamy, and Andrea Bajcsy. From foresight to forethought: Vlm-in-the-loop policy steering via latent alignment, 2025. URL https://arxiv. org/abs/2502.01828. 

- [69] Noah D. Goodman and Michael C. Frank. Pragmatic language interpretation as probabilistic inference. _Trends in Cognitive Sciences_ , 20(11):818–829, 2016. ISSN 1364-6613. doi: https://doi.org/10.1016/j.tics.2016.08. 005. URL https://www.sciencedirect.com/science/article/ pii/S136466131630122X. 

- [70] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning, 2023. URL https://arxiv.org/abs/2306.03310. 

- [71] Xueyang Zhou, Yangming Xu, Guiyao Tie, Yongchao Chen, Guowen Zhang, Duanfeng Chu, Pan Zhou, and Lichao Sun. Libero-pro: Towards robust and fair evaluation of vision-language-action models beyond memorization, 2025. URL https://arxiv.org/abs/2510.03827. 

- [72] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, Dan Bikel, Lukas Blecher, Cristian Canton Ferrer, Moya Chen, Guillem Cucurull, David Esiobu, Jude Fernandes, Jeremy Fu, Wenyin Fu, Brian Fuller, Cynthia Gao, Vedanuj Goswami, Naman Goyal, Anthony Hartshorn, Saghar Hosseini, Rui Hou, Hakan Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa, Isabel Kloumann, Artem Korenev, Punit Singh Koura, Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee, Diana Liskovich, Yinghai Lu, Yuning Mao, Xavier Martinet, Todor Mihaylov, Pushkar Mishra, Igor Molybog, Yixin Nie, Andrew Poulton, Jeremy Reizenstein, Rashi Rungta, Kalyan Saladi, Alan Schelten, Ruan Silva, Eric Michael Smith, Ranjan Subramanian, Xiaoqing Ellen Tan, Binh Tang, Ross Taylor, Adina Williams, Jian Xiang Kuan, Puxin Xu, Zheng Yan, Iliyan Zarov, Yuchen Zhang, Angela Fan, Melanie Kambadur, Sharan Narang, Aurelien Rodriguez, Robert Stojnic, Sergey Edunov, and Thomas Scialom. Llama 2: Open foundation and fine-tuned chat models, 2023. 

- [73] Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin ElNouby, Mahmoud Assran, Nicolas Ballas, Wojciech Galuba, Russell Howes, Po-Yao Huang, Shang-Wen Li, Ishan Misra, Michael Rabbat, Vasu Sharma, Gabriel Synnaeve, Hu Xu, Herv´e Jegou, Julien Mairal, Patrick Labatut, Armand Joulin, and Piotr Bojanowski. Dinov2: Learning robust visual features without supervision, 2024. 

- [74] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and 

Lucas Beyer. Sigmoid loss for language image pretraining, 2023. 

- [75] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, Peter David Fagan, Joey Hejna, Masha Itkina, Marion Lepert, Yecheng Jason Ma, Patrick Tree Miller, Jimmy Wu, Suneel Belkhale, Shivin Dass, Huy Ha, Arhan Jain, Abraham Lee, Youngwoon Lee, Marius Memmel, Sungjae Park, Ilija Radosavovic, Kaiyuan Wang, Albert Zhan, Kevin Black, Cheng Chi, Kyle Beltran Hatch, Shan Lin, Jingpei Lu, Jean Mercat, Abdul Rehman, Pannag R Sanketi, Archit Sharma, Cody Simpson, Quan Vuong, Homer Rich Walke, Blake Wulfe, Ted Xiao, Jonathan Heewon Yang, Arefeh Yavary, Tony Z. Zhao, Christopher Agia, Rohan Baijal, Mateo Guaman Castro, Daphne Chen, Qiuyu Chen, Trinity Chung, Jaimyn Drake, Ethan Paul Foster, Jensen Gao, David Antonio Herrera, Minho Heo, Kyle Hsu, Jiaheng Hu, Donovon Jackson, Charlotte Le, Yunshuang Li, Kevin Lin, Roy Lin, Zehan Ma, Abhiram Maddukuri, Suvir Mirchandani, Daniel Morton, Tony Nguyen, Abigail O’Neill, Rosario Scalise, Derick Seale, Victor Son, Stephen Tian, Emi Tran, Andrew E. Wang, Yilin Wu, Annie Xie, Jingyun Yang, Patrick Yin, Yunchu Zhang, Osbert Bastani, Glen Berseth, Jeannette Bohg, Ken Goldberg, Abhinav Gupta, Abhishek Gupta, Dinesh Jayaraman, Joseph J Lim, Jitendra Malik, Roberto Mart´ın-Mart´ın, Subramanian Ramamoorthy, Dorsa Sadigh, Shuran Song, Jiajun Wu, Michael C. Yip, Yuke Zhu, Thomas Kollar, Sergey Levine, and Chelsea Finn. Droid: A large-scale in-thewild robot manipulation dataset. 2024. 

- [76] Danny Driess, Jost Tobias Springenberg, Brian Ichter, Lili Yu, Adrian Li-Bell, Karl Pertsch, Allen Z. Ren, Homer Walke, Quan Vuong, Lucy Xiaoyang Shi, and Sergey Levine. Knowledge insulating vision-languageaction models: Train fast, run fast, generalize better, 2025. URL https://arxiv.org/abs/2505.23705. 

## APPENDIX A 

## SYNTHETIC GENERATIONS IN BRIDGE 

## _A. Generating Subtasks and Steering Commands_ 

We present the Gemini [50] prompts for extracting subtasks in Fig. 19. This decomposes each Bridge episode into subtasks, as Zawalski et al. [8] did. These subtasks are used in conjunction with bounding boxes, gripper trace coordinates, and motions (discussed below) in the prompt shown in Fig. 20 to produce the steering commands used for training our Steerable Policy. The result is that each episode is divided into subtasks, and for each subtask, it has a list of corresponding steering commands (of all the command styles discussed in Sec. IV-A). 

Note that all pixel coordinates are normalized from 0 to 255, labeled as bracketed tuples (first number represents column from the left and second row from the top, with [0 _,_ 0] being the top-right corner). 

## _B. Generating Rationalizations_ 

Once we have a subtask decomposition of each trajectory in Bridge, we can produce rationalizations for explaining why each subtask is appropriate for their corresponding starting frames. We do this by again querying Gemini 2.0, giving it each subtask’s initial observation, the overall and past subtasks, and the current subtask for it to explain post-hoc. See Fig. 21 for the full prompt. This attaches a rationale for each subtask in each episode. 

## _C. Extracting Embodied Features_ 

Our pipeline for extracting object and gripper coordinates follows three stages. 

First, we identify relevant objects in each scene using the MolmoE-1B-0924 model [47]. The model is prompted with a natural language description of the robot task and instructed to return a list of up to four objects in the scene, excluding the robot itself. The prompt follows the format: _“The robot task is {task_ _<u>name}.</u> Briefly provide a list of up to 4 objects in the scene (ignore the robot), including the ones in the task. Don’t add any additional text.”_ 

Next, we use Molmo-7B-D-0924 to predict the coordinates of each identified object in the first image of the trajectory [47]. To extend these localizations across time, we apply the Segment Anything Model (SAM 2 [48]) to propagate the object points throughout the trajectory, producing temporally consistent segmentation masks. 

For gripper coordinates, we manually annotated 100 images from the Bridge dataset with gripper positions. A lightweight DETR model was trained on this data and then used to label gripper centroids across all images in the dataset. 

In a final post-processing step, we apply a simple heuristic to filter out task-irrelevant objects by checking whether object names appear in the task description. All object and gripper coordinates are then converted into the <loc> format expected by the PaliGemma model [58]. Finally, the segmentation masks are tokenized using PaliGemma’s vector quantization tokenizer to generate <loc><seg> token sequences. 

## APPENDIX B 

## DETAILS ON HIERARCHICAL METHODS WITH IN-CONTEXT LEARNING OFF-THE-SHELF FOUNDATION VLMS 

We now give further details on the in-context learning high-level VLM experiments. All hierarchical methods in this experimental suite are instantiated with Gemini 3.0 [50]. 

## _A. Our Approach and Non-reasoning Ablation_ 

The full VLM prompt for our approach is provided in Fig. 22. The VLM is given a task description, an explanation of all steering command styles with in context examples, and a history of past commands and observations. The model is encouraged to reason in-context before providing a final steerable command to instruct our low-level steerable policy. This steerable command is run for _N_ = 20 steps before the VLM is re-queried. 

Note that for grounded steering styles, the policy is allowed to provide keypoints, for example, "move <carrot on left> to <plate>". Within each angle brackets, the policy may describe a single point in the scene. These descriptions are converted into coordinates, for example, "move [ _x_ 1 _, y_ 1] to [ _x_ 2 _, y_ 2]" by another Gemini 3.0 call as described in Fig. 25. In our final approach, we allow the policy to output pointing commands, but not grounded gripper traces, as the VLM performs poorly at providing them. 

In our approach, the VLM is instructed to explicitly reason and is additionally allocated a budget of 1024 thinking tokens through the Gemini API [50]. Our non-reasoning baseline uses the exact same prompt, except that it is told _not_ to reason, and is provided a thinking budget of 0 thinking tokens. We find that the model listens to these instructions and does not reason. Notably, our non-reasoning baseline still has access to an explanation of all steering command styles with in context examples, and a history of past commands and observations to make inferences. The full prompt for our ablation can be found in Fig. 23. 

## _B. SayCan-like Baseline_ 

The SayCan-like baseline uses the exact same prompt structure as our full approach, with the only change being that it only has an explanation and in-context examples of subtask-level steering commands. The model is still provided with a 1024 token thinking budget and is told to explicitly reason about the scene and provided history. The full prompt for this baseline is described in Fig. 24. 

## APPENDIX C 

## EXPERIMENTAL TASK DETAILS 

The experiments in Sec. VI are broadly divided into several generalization splits: 

- 1) In-distribution: “standard” tasks, akin to those in Bridge [4, 5]. We expect a VLA trained on Bridge to be proficient at these. 

- 2) Motion Generalization: Involves standard tasks but with non-standard poses (e.g., placing objects high up). 

|**Split**|**Task**|**Standard**|**VLAs**|**ECoT-Lit**|**e Variants**|**Full**<br>**ECoT**|**S**<br>**Embo**|**teerable Policy +**<br>**died Reasoner (O**|**urs)**|
|---|---|---|---|---|---|---|---|---|---|
|||**OpenVLA**|_π_0_._5|**Reasoning**<br>**Dropout**|**Reasoning**<br>**Pre-training**||**Non-reasoning**<br>**Ablation**|**Full Approach**<br>**OpenVLA**|**Full Approach**<br>_π_0_._5|
|**In Dist.**|Put the [mushroom / corn / egpplant]<br>in the [pot / bowl]|72.2|61.1|72.2|88.9|88.9|72.2|88.9|**94.4**|
||Place the [spoon / carrot] [in / on]<br>the [plate / towel]|75.0|**100**|66.7|91.7|91.7|66.7|91.7|83.3|
|**In Dist.**<br>**Chlln**|Put the [broccoli / spoon / cube] on<br>the towel (all objects are green)|16.7|50.0|66.7|66.7|**83.3**|66.7|66.7|50.0|
|**aege**|Put the [green / pink] spoon<br>on the [plate / towel]|**87.5**|**87.5**|62.5|37.5|75.0|62.5|75.0|**87.5**|
|**Motion**<br>**Gen.**|Put the [carrot / mushroom] [on / in]<br>the [plate / pot] (target is high up)|8.3|41.6|25.0|33.3|58.3|**83.3**|**83.3**|75.0|
|**Spatial**|Put the [banana / tomato] in the<br>[left / right] bowl|91.7|83.3|75.0|83.3|91.7|91.7|**100**|91.7|
|**Gen.**|Put the [green / orange] toy in the<br>[left / right] pot|50.0|75.0|75.0|**87.5**|75.0|62.5|**87.5**|**87.5**|
||Move the [mushroom / carrot] to the<br>[left / right] of the [other object]|62.5|62.5|**100**|**100**|75.0|75.0|87.5|**100**|
|**Sti**|Put the watermelon<br>on the towel|0|33.3|**83.3**|**83.3**|66.7|50.0|66.7|**83.3**|
|**emanc**<br>**Gen.**|Put the toothbrush<br>on the plate|33.3|50.0|50.0|83.3|66.7|50.0|**100**|**100**|
||Put the screw<br>in the bowl|33.3|16.7|16.7|66.7|66.7|50.0|**83.3**|**83.3**|
||Reach for the<br>[ketchup / wrench / mallet]|11.1|33.3|22.2|0|**66.7**|33.3|**66.7**|55.5|
||**Aggregate**|50.5_±_4.7|61.3_±_4.6|60.4_±_4.6|69.4_±_4.4|77.5_±_4.0|66.7_±_4.5|**84.6**_±_**3.4**|83.7_±_3.4|


TABLE I: Full numerical results of the embodied reasoning methods on the task suite defined by Chen et al. [9]. Numbers represent success percentage, _±_ StdErr. Equivalent to the data in Fig. 7. 

|**Split**|**Task**|**Standard**<br>**OpenVLA**|**SayCan-Like**|**Steerable **<br>**In-context Learni**<br>**Non-reasoning**<br>**Ablation**|**Policy +**<br>**ng VLM(Ours)**<br>**Full**<br>**Approach**|
|---|---|---|---|---|---|
|**Long**<br>**Hi1**|Make the mushroom the<br>only obj. on the plate|35.0|70.0|80.0|100|
|**orzon **|Make the blue block<br>the only obj. on the plate|30.0|65.0|90.0|80.0|
|**Long**<br>**Hi2**|Put all the food in the blue pot<br>and stuffed toys in the tan pot|50.0|36.7|53.3|66.7|
|**orzon **|Put all the food in the white bowl<br>and stuffed animals in the green bowl|43.3|63.3|80.0|76.7|
|**Motion**|Stack the pots|45.0|85.0|55.0|95.0|
|**Gen.**|Stack the pots on the towel|40.0|60.0|90.0|65.0|
|**Spatial**<br>**G**|Put the banana on the<br>[left / right] on the plate|60.0|80.0|90.0|100|
|**en.**|Put the white and blue stuffed animal<br>in the bowl on the [left / right]|80.0|90.0|100|100|
|**Semantic**|Put the hammer on the towel|40.0|60.0|70.0|80.0|
|**Gen.**|Put the screw on the plate|60.0|30.0|70.0|80.0|
||**Aggregate**|48_±_5.1|64_±_5.5|78_±_4.0|84_±_3.7|


TABLE II: Full numerical results of the in-context learning methods on our new multi-step task suite. Numbers represent average task progression (graded with a rubric that decomposes each task into steps), _±_ StdErr. Equivalent to the data in Fig. 8. 

|**Task**|**Prompts**|**Rubric**|**Success / Fail**|
|---|---|---|---|
|**Long Horizon 1**|1. Make the mushroom the only object on the plate<br>2. Make the blue block the only object on the plate|1. Interacted with object on plate<br>2. Plate object no longer on plate<br>3. Pick up correct object<br>4. Put down correct object in correct location|-|
|**Long Horizon 2**|1. Put all food in blue pot and stuffed animals in tan pot<br>2. Put all food in white bowl and stuffed animals in green bowl|1. Pick up object 1<br>2. Put object 1 in correct container<br>3. Pick up object 2<br>4. Put object 2 in correct container<br>5. Pick up object 3<br>6. Put object 3 in correct container|-|
|**Motion Gen.**|1. Stack the pots<br>2. Stack the pots on the towel|1. Pick up pot 1<br>2. Stack 1 complete<br>3. Pick up pot 2<br>4. Stack 2 complete|-|
|**Spatial Gen.**|1. Put the banana on the [right/left] on the plate<br>2. Put the white and blue stuffed animal in the [left/right] bowl|1. Pick up correct object<br>2. Put down correct object in correct location|-|
|**Semantic Gen.**|1. Move the hammer to the towel<br>2. Move the screw to the plate|1. Pick up correct object<br>2. Put down correct object in correct location|-|


TABLE III: Evaluation Rubric for In-context Learning VLM Experiments. Trials for each task are divided between two prompts. Each trial is scored by a multi-step rubric, and each step is graded by success/fail. Task progress is the average number of successes in a trial. For spatial generalization tasks, we do an equal number of trials with either “left” or “right” in the prompt. 

- 3) Spatial Generalization: Tasks involving spatial relation (e.g., “place in the pot on the left”). 

- 4) Semantic Generalization: Involves out-of-distribution objects, whose names do not appear in the Bridge dataset. 

These splits are used for the human oracle experiments and the embodied reasoner experiments. The off-the-shelf VLM experiments instead use two sets of long-horizon tasks in lieu of the in-distribution ones. In total, we run over 650 robot rollout episodes across our three evaluation suites. 

## _A. Human Oracle Experiments_ 

The human oracle experiments use the same task splits as the embodied reasoner experiments discussed below. However, they involve different sets of actual tasks, so as to evaluate oracle steering capabilities on a wider range of settings. See Fig. 13 for example initial states. 

See Fig. 15 for example initial states and Table II for full results. Each trial of each task is graded based on the rubric in Table III. Each task has two prompts, and trials for each task are divided equally among prompts. Rubrics are graded based on success/fail, and the average number of successes per trial is the final task progress number we report. The policy being evaluated does not need to complete rubric items in order. However, it is penalized for undoing task progress: e.g., the policy may receive credit for putting an object in the correct location, but that credit is revoked if the policy later removes the object. The only exception to this rule is that the policy always gets and maintains credit for interacting with or picking up an object for the first time. The policy is run for 20 highlevel steps (25 for Long Horizon 2), and is only terminated early only if all entries in rubric are completed correctly. 

## APPENDIX D 

## _B. Embodied Reasoner Experiments_ 

The tasks for evaluating our hierarchical embodied reasoner are the same as those used for evaluating ECoT-Lite [9]. This allows us to compare against other methods for leveraging embodied reasoning data for training VLAs. See Fig. 14 for example initial states and Table I for detailed task performance. 

## _C. In-context Learning VLM Experiments_ 

For the in-context learning VLM experiments, we change out all tasks to include more multi-step ones, as they are more suited to evaluating hierarchical systems’ generalization. We replace the in-distribution split with two long-horizon tasks, which involve composing many in-distribution behaviors. Additionally, our motion generalization tasks now involves a novel task behavior, though again requires challenging (multistep) motions to solve. 

## ADDITIONAL ILLUSTRATIVE EXAMPLES 

## _A. Example Steering Commands_ 

We include numerous example steering commands in Fig. 10. The diagram is just for visualization purposes, while the text examples are taken exactly from our training data. 

_B. Example Full Reasoning Traces for High-level Embodied Reasoner_ 

See Fig. 16 for examples of reasoning traces produced by our embodied reasoning high-level VLM. 

_C. Example Full Reasoning Traces for In-context Learning VLM Methods_ 

We present the example reasoning traces from our in-context learning VLM method (Sec. V-B) in Fig. 17. These are the full, unparaphrased versions of the examples in Fig. 9. 


Fig. 10: **Example steering commands** . All labels and points in the image are purely for visualization, and do not appear on the actual robot training data images. The list on the bottom is exactly extracted from our training dataset, with bold representing the subtasks and the dashed list representing the corresponding diverse steering commands. Each subtask typically has more than 5 corresponding steering commands, but we limit to that many for readability. 

For full examples of the equivalent reasoning traces from the SayCan-like baseline, see Fig. 18 and the associated discussion in App. E-C. 

## APPENDIX E FURTHER DISCUSSIONS 

## _A. Steering in Robot Learning_ 

We take _steering or guidance_ to mean the broad class of techniques for controlling the outputs of a generative model. As discussed in Sec. II, we specifically consider the case of improving steerability by altering the training strategy. This contrasts with a broad set of works that aim to do steering at inference time, or otherwise without modifying the weights of some pretrained policy. For completeness, we briefly discuss them here. 

These approaches usually aim to produce samples that are in-distribution while optimizing some criteria such as a classifier score [59], the likelihood under an unconditional distribution [60], the similarity to a reference output [61], or a Q-function [62–64]. The method for optimizing these criteria also varies, including linearly mixing denoising vector 


Fig. 11: Examples of what we deem the manifold of “reasonable” actions, where underspecified commands (especially atomic motions) induce specific intelligent behaviors, based on the observed state. Solid arrows are these “reasonable” actions, while the dotted arrow is what the command would look like without conditioning on the image (i.e., akin to controlling the end effector with a game pad and holding a single direction down). **Left:** Rather than moving straight down, the empty gripper would move down towards an object it would grasp. **Middle:** once an object is grasped, telling the robot to move left causes it to infer where to place it (in the case, the towel, which is left of the gripper). **Right:** However, this can be ineffective if there are multiple reasonable behaviors. If the robot is commanded to "move right", it could reach for the carrot _or_ the cube. 

fields [59, 60], optimizing input noise or embeddings [63, 65, 61], or parallelizable sample-and-rank through a scoring function or dynamics model [61, 62, 66–68]. 

## _B. The Manifold of “Reasonable” Actions_ 

Throughout our experiments, we notice a prevalent qualitative trend in how our Steerable Policy responds to underspecified commands, especially atomic motions. When given such a command, the robot does not _just_ move in that direction, but does so while heavily considering the state of the robot and scene. For example, when given the (rather underspecified) command "move left", it will typically move left _and down_ , towards objects that it can interact with. If the gripper is already grasping something, the robot might instead move left _and up_ , towards a container that the object can be placed in. Finally, if told “open gripper” while near a container, the robot may first move the gripper above it before releasing. See Fig. 11 for illustrations. 

In other words, atomic motion commands seem to cause the policy to sample from the distribution of actions aligned with the commanded direction, but marginalized over all “reasonable” tasks that involve moving that way. The VLA can estimate what tasks can be done in a particular scene by attending to the visual observation. Then, when given a motion (e.g., "move left"), it can estimate which of those tasks are likely accomplished by moving left, and then take actions aligned with one or more of those tasks. Intuitively, this arises from common correlations in the training data: if the gripper is empty and a possible steering command for that frame is to "move left", then the Bridge episode likely involves moving left and down to grasp something. We informally describe this as sticking to the manifold of “reasonable” actions. 

The qualitative implication is that giving an atomic motion command often results in intelligent motions, rather than “blindly” moving in the commanded way – explaining how atomic motions end up being the best single steering modality in the human oracle experiments from Sec. VI-A, despite motions being vague _and_ the human only being able to issue new commands every two seconds. 

Naturally, this can be a blessing or a curse. While "move left" might cause the robot to pick up an object of interest, it can also get “confused” when there are multiple objects to the left, as that command could reasonably cause the policy to pick up either one. Of course, other steering command styles are able to supplement these behaviors, further motivating both training on many steering command styles and applying VLM capabilities to intuit when each style is most appropriate, as we propose. 

## _C. Why are Subtask Commands Insufficient?_ 

Standard hierarchical approaches command the low-level policy with tasks and subtasks alone [1]. However, these steering modalities are too unspecific to reliably induce generalizable behaviors. We show an example of this in Fig. 18, drawn directly from our multi-step evaluation tasks. While the high-level VLM knows what the robot should do, subtasks alone are not a viable interface to “convey” this behavior to the low-level VLA. Instead, every time the VLM emits "grasp the screw", the VLA fails to recognize what the screw is, and grasps some distractor object instead. 

While the VLM can tell the policy to drop that incorrect object, it cannot reliably fix this behavior, as subtasks are not flexible enough. This motivates our introduction of diverse steering command – if one command style fails, then using a different steering modalitiy might work instead (in this case, intuitively telling the Steerable Policy to "move up and left" instead of "grasp the screw" would likely work). 

## _D. What are the Failure Modes of Our Method?_ 

Most of the failure modes of our method stem from the _high-level VLM’s limited grasp of the low-level Steerable Policy’s affordances._ For example, while VLMs can use incontext learning to learn the affordances for the experiments in Sec. VI-C, it fails in subtler cases: e.g., the high-level VLM might say to execute the _correct_ next step in a multi-step task, but the VLA sometimes fails to follow the command at the current state (e.g., due to dataset bias), and _undoes progress by grasping the same object it just placed_ . Instead, the VLA should be prompted with other abstractions, e.g., motions stating to move away _without grasping_ . This strategy is hard for VLMs to discover, despite otherwise working well. 

This is effectively an issue with the _pragmatics_ of the steering command [69]: the high-level policy must infer the command (and abstraction) that is most likely to communicate and induce a desired behavior in the low-level VLA, selecting from all “reasonable” commands for doing so. 

Finally, the steerability of our VLA comes from the diversity of behaviors within its data. Training on steering commands 

simply allows these skills to be induced with the right command style. Conversely, “narrow” datasets are _not_ conducive to training Steerable Policies. For example, LIBERO [70] is _not_ very diverse: provided trajectories are unimodal [71] and starting states for each task are minimally randomized; even minor perturbations degrade performance [9]. While policy steering in LIBERO can optimize a narrow behavior prior [63], it remains challenging to use steering for solving wholly new or heavily-randomized tasks, as we do in Bridge. Consequently, our approach cannot easily be applied to LIBERO due to deficiencies in the dataset’s behavioral diversity. 

APPENDIX F TRAINING DETAILS "action tokenizer": "action tokenizer", "base vlm": "prism-dinosiglip-224px+7b", "data mix": "bridge", "enable gradient checkpointing": true, "enable mixed precision training": true, "epochs": 1000, "expected world size": 8, "freeze llm backbone": false, "freeze vision backbone": false, "global batch size": 256, "image sequence len": 1, "learning rate": 2e-05, "lr scheduler type": "constant", "max grad norm": 1.0, "max steps": null, "per device batch size": 32, "reduce in full precision": true, "save every n steps": 25000, "shuffle buffer size": 256000, "train strategy": "fsdp-full-shard", "type": "prism-dinosiglip-224px+mx-bridge", "unfreeze last llm layer": false, "use wrist image": false, "vla id": "prism-dinosiglip-224px+mx-bridge", "warmup ratio": 0.0, "weight decay": 0.0 

Fig. 12: Hyperparameters for training both the Steerable Policy and highlevel embodied reasoner, taken from the OpenVLA parameter logging files (as both are trained by adapting the OpenVLA codebase). 

## _A. Steerable Policy Training_ 

_1) OpenVLA-based Steerable Policies:_ We train our first Steerable Policy by adapting the OpenVLA codebase [10]. We use all provided default hyperparameters used for training the model on the Bridge dataset (see Fig. 12). Following past works [8, 9], we train for 80k steps at batch size 256, split across 8x H100 GPUs on a single compute node. We use the DINOv2-SigLIP image encoder and Llama2 7b LLM version of Prismatic VLM as the base pretrained VLM for our policy [72–74, 57]. 

The main alteration to the training pipeline is that, for each frame, we identify which subtask in the overall episode it corresponds to. Then, we uniformly randomly sample a command from a list containing the overall task language provided by Bridge (to support task-level command), the subtask language, and any corresponding steering commands we generate. 

Otherwise, we use the standard next-token prediction loss used for training OpenVLA. This also means the Steerable Policy expresses robot actions via naive discretization: as introduced by Brohan et al. [13], this discretizes each of the seven action dimensions into 256 bins, which correspond to the 256 least-used tokens in Llama’s vocabulary. 

_2) π_ 0 _._ 5 _-based Steerable Policies:_ Our _π_ 0 _._ 5-based Steerable Policy is trained in the exact same way as above, using the default hyperparameters provided by OpenPi [16] for finetuning _π_ 0 _._ 5 on the DROID dataset [75], albeit only run for 30k gradient steps on 8x H200. Training takes less than a day. Note that we use the standard OpenPi recipe for tuning _π_ 0 _._ 5; we do NOT use the Knowledge Insulation trick used for training base _π_ 0 _._ 5 [76]. Additionally, we do not condition on any proprioception information, so as to stay in line with the other policies we evaluate. Finally, we train with action chunk size 4 with end effector actions, but only execute the first action of each chunk at inference time (i.e., inference is fully closed-loop). 

## _B. High-level Embodied Reasoner Training_ 

The high-level embodied reasoner is similarly instantiated by training with an altered version of the OpenVLA codebase, using the same hyperparameters as our policy (see Fig. 12). However, rather than mapping from observations and task language to actions, we instead use standard next-token prediction loss to train the VLM to predict a rationale/reasoning followed by an appropriate steering command. That is, for each training frame, we look up the corresponding subtask and rationale. Then, we also get the list of steering commands paired with that subtask, and sample one at random. Finally, we train the policy to receive the image and task language (represented as tokens), and output the rationale and the sampled command autoregressively. 

Our non-reasoning ablation is trained identically, just with the rationale supervision removed (so it learns to map observations and task language directly to steering commands, without intermediate reasoning generations). 


Fig. 13: **Example starting states for the tasks for the didactic experiment** wherein a human operator acts as the high-level policy. 


Fig. 14: **Example starting states for the tasks for evaluating embodied reasoning VLAs** , reproduced with permission from Chen et al. [9] (as we reuse their task suite). 


Fig. 15: **Example starting states for the multi-step tasks** for evaluating in-context learning high-level VLMs. 

### **_`Put the broccoli on the towel`_** 


### **_`Put the watermelon on the towel`_** 


Fig. 16: Examples of **embodied reasonings produced by our fine-tuned VLM** , taken from rollouts for the evaluations in Sec. VI-B. 


Fig. 17: Examples of **in-context reasonings produced by our off-the-shelf VLM for issuing steering commands** , taken from rollouts for the evaluations in Sec. VI-C. These are the unparaphrased versions of the examples in Fig. 9 

### **_`Put the screw on the plate`_** 


```
The scene shows a robot
gripper hovering over a
mushroom on a wooden table,
with a screw, a plate, and a
corn cob also present
nearby. The robot has not
yet interacted with the
screw or the plate.
```

```
The robot needs to move its
gripper to the screw and
pick it up to begin the
task.
Grasp the screw
```

```
In the current observation, The scene shows the robot
The current observation the robot arm has gripper holding the yellow
shows the robot gripper successfully released the corn object on the table,
holding the yellow corn, corn and is now empty, with while the white screw and
while the white screw the gripper open above the the blue plate remain in
remains on the table to the table. The white screw their original positions.
left. This indicates the remains on the left side of The robot has mistakenly
previous command to grasp the table, while the blue grasped the corn instead of
the screw was unsuccessful.plate is positioned in the the screw as previously
center.commanded.
The robot must release the
corn to free its gripper The robot must now move to The robot must release the
before it can attempt to and pick up the white screw corn to free its gripper so
grasp the screw again.to proceed with the task of it can move towards and
moving it to the plate.grasp the screw.
Release the cornGrasp the screwRelease the corn
```


Fig. 18: Illustrative example of **why VLAs cannot leverage VLMs’ in-context learning, visual understanding, and reasoning well when issued only subtask commands** (from the SayCan-like baseline in Sec. VI-C). The high-level VLM reliably detects incorrect behaviors and what the robot should do to progress the task. **However, the low-level VLA fails to make use of this when only commanded with subtasks.** Instead, when the VLM correctly tells it to "grasp the screw" (which is out-of-distribution), it always mistakes some other object for it, and grasps the mushroom or corn instead. The policy gets stuck in this loop until the episode times out. Due to lack of steerability with subtasks alone, the high-level VLM has no way to fix this behavior. Our Steerable Policies can get unstuck by simply being commanded at some other level of abstraction. 

I am trying to break robot demonstration trajectories into a list of subtasks. For example: 

- If the task is "put the mushroom in the pot," the subtasks might be "reach for the mushroom, grasp the mushroom, lift the mushroom, move the mushroom above the pot, and release the mushroom into the pot." 

- If the task is "wipe the table with the cloth," the subtasks might be "move to the cloth, slide the cloth to the left along the table, slide the cloth to the right along the table, slide the cloth to the 

- left along the table, release the cloth." 

- If the task is "open the cabinet door," the subtasks might be "move to the cabinet door handle, grasp the handle, pull the door open, swing the arm to the left to open the door, reposition arm to right of 

- door, push cabinet door fully open to the left." 

- If the task is "pour the cup into the bowl," the subtasks might be "move to the cup, grasp the cup, move above the bowl, rotate to pour the cup." 

I will provide you with a list of motions (e.g., "move left," "rotate up," "close gripper") and their corresponding timestamps. I have removed consecutive duplicate language motions. I want you to come up with a list of subtasks and then group all the timestamps into those categories. Make sure the subtasks are specific and specify the name of the object that is likely being interacted with. Please reason about the subtask steps first, then give the final answer as a Python dictionary mapping from the subtasks as strings to a list of timestamps corresponding to that task. Additionally, make sure that subtasks are in order: Later subtasks should only contain timestamps after the ones in earlier ones. The only code should be this dictionary All timestamps should be mapped to subtasks. 

The task is described with the following instruction: "<instruction>" 

Additionally, an object detector found the following non-comprehensive list of <number of items> items: <list of objects>. The motions are as follows: 

<step number>: <motion> 

Fig. 19: The prompt for dividing Bridge tasks into subtasks. 

I am trying to label frames of a robot demonstration with various possible instructions. I will give the overall task and a list of all subtasks. Then, for each subtask, I will give a description of each frame, consisting of the timestep, gripper movement, gripper position, and a (possibly incomplete) list of object positions. All positions are pixel coordinates (first number goes right along columns, second number goes down along rows). I want to generate a list of possible instructions for each subtask. These instructions should be at varying levels of abstraction, and should consider information from both the current step and others. 

For example: 

Some examples of high-level instructions are: 

- ’grasp the mushroom in the pot’ 

- ’wipe the cloth across the table’ 

- ’move the lid above the pot’ 

Some examples of low-level motion instructions are: 

- ’move down and close’ 

- ’move the cloth left’ 

- ’pull the drawer handle backward’ 

Some examples of instructions using object positions: 

- ’pick up the mushroom at <position of mushroom>’ 

- ’go to the pot at <position of pot> to grab the mushroom’ 

Note: The object positions are not always perfect, e.g., if the detector picks up the wrong instance of an object in the scene. In these cases, try to figure out when this is the case based on where the gripper position is. 

Some examples of instructions using gripper positions: 

- ’move to <5 gripper positions throughout subtask> and grasp’ 

- ’move to <gripper position before grasping> and close’ 

- ’sweep with tool at <4 gripper positions throughout the subtask>’ 

- ’carry the spatual along <3 gripper positions throughout the subtask>’ 

Note: When listing positions, use at most 5 of the positions throughout the subtask. 

Finally, some examples of instructions that combine the above: 

- ’move down to the mushroom at <position of mushroom> and grasp it’ 

- ’grab the mushroom at <position of mushroom> and move it to the plate at <position of plate>’ 

- ’move the stuffed toy along <3 gripper positions throughout the subtask>, toward the box at <position of box>’ 

(Note how this requires reasoning about gripper and object positions, e.g., how the gripper gets closer to the box’s location) 

- ’move down to <gripper position before grasping the mushroom> and grab the mushroom at <position of mushroom>’ 

Give your answer as a Python dictionary mapping from each subtask to a list of possible instructions. Do not include any code other than this dictionary. When referencing gripper and object positions, use the provided specific numerical values (e.g., do NOT say ’<3 gripper position throughout subtask>’, but actually list out the numerical positions). 

Overall Task: "<instruction>" 

Subtasks: <list of subtasks> 

Subtask: <first subtask> 

<step number>: <motion>, gripper: <gripper pixel coordinates> 

<object name>: <bounding box center pixel coordinates> 

Fig. 20: The prompt for generating steering commands for Bridge tasks. 

I want my robot to reason about its observation before choosing its behaviors. I have a dataset of demonstrations where the robot arm is solving tasks. I will provide a description of the task, the robot’s observation, text descriptions of the robot’s actions, a plan for what the robot will do, and what the robot’s current subtask likely is. I will also give you the appropriate behaviors the robot should follow. In response, write me a rationale that would help the robot determine these true behaviors. 

Instructions: 

- The rationale should be inferable from the current image only, as the robot does not know what subtasks it completed in the past 

- The robot does not know its past or current appropriate subtask. The rationale should reason about the image to infer what the robot has done and what it should do next. 

- The rationale should reason about the scene, objects, robot gripper, and the relevant spatial and semantic relations between them. 

- Finally, the rationale should help determine and explain the commands the robot should follow. This includes the subtask and motions the robot should execute. 

Guidelines: 

- I have provided the past subtasks to help you better understand the robot’s state (e.g., if the past subtask was ’grasp the mushroom,’ the robot is likely holding the mushroom). However, they should NOT be 

- directly cited in the rationales. 

- The appropriate commands and motions are what the robot SHOULD do, not what it is currently doing. 

- Be specific about positions, movements, and spatial relations of objects and the gripper. For example, if the robot has to move the block on the right side of the table while there are multiple blocks, 

- reason about which one is the block on the right. 

- Do not start with ’The robot’s task is...’ or similar. The robot task is known. 

Examples: 

1. Task: ’Put the mushroom in the pot.’ 

’The robot seems to be holding the mushroom, so it now needs to move it above the pot. The pot seems to be left of the gripper. Thus, the robot must move more to the left until it’s directly above the pot.’ 2. Task: ’Wipe the table.’ 

’Wiping the table requires a cloth, which the robot does not seem to be holding. It thus should move to the cloth. As the gripper is to the cloth’s right, it thus should move left and down. 

3. Task: ’Move the eggplant in the sink to the plate.’ 

’The robot is currently holding the eggplant, which is in the sink, so it must now lift it out toward the plate. The plate is on the countertop next to the sink. To avoid colliding with the sink, the robot should first move up until its gripper is higher than the sink’s walls.’ 

4. Task: ’Open the drawer.’ 

’To open the drawer, the robot needs to grasp and pull on its handle. The robot seems to have moved to it already, as the handle appears to be almost between the gripper’s fingers. Thus, the robot must adjust its gripper to the right, then close it to grasp the handle.’ 

5. Task: ’Place the silver pot on the bottom right stove burner’ 

’The robot is holding the pot, so it should now move it to the bottom right burner. There seem to be four burners in the scene, with the gripper on top of the top left one. The robot should thus move right and backward more until it’s directly above the burner.’ 

Provide a rationale for the following: 

The robot’s task is: ’<instrution>’ 

The included image shows the robot’s current observation. 

The appropriate behavior that the rationale should help determine is as follows. 

The appropriate current subtask is: ’<current subtask>’. 

The past subtask(s) were: <list of subtasks> **OR** This is the first subtask. 

The appropriate motions and gripper positions throughout this subtask are: 

<list of motions and gripper positions> 

Fig. 21: The prompt for rationalizing steering commands for Bridge tasks. 

You are guiding a robot to complete a task by generating a subtask instruction for the robot to follow given an image of the robot’s current observation, and a history of observations and past commands. The robot is trying to accomplish the overall task: ’[task description]’. You should keep the rest of the environment unchanged. Note that all objects required for the task are present (no need to search for objects). There are several kinds of instructions the robot understands, each at a different level of abstraction, detailed below. Sometimes, a high-level instruction is sufficient for the robot to make progress towards solving the task, but other times, a more specific command is required. Below are examples of the kinds of instructions you can generate for the robot. Some examples of High-level instructions are: 

- ’grasp the mushroom in the pot’ 

- ’wipe the cloth across the table’ 

- ’move the lid above the pot’ 

- ’lift the carrot up’ 

- ’move towards the stuffed toy’ 

- ’drop the eggplant in the bowl’ 

The robot is generally reliable at following high-level commands, especially when interacting with non-novel objects. They can also be used to better understand the scene and robot state, such as by saying ’lift the object’ to ascertain if the robot has actually firmly grasped it. However, these commands may fail when interacting with novel objects, as the robot may not recognize them by name. The robot also may also confuse similar objects with each other (e.g., it may mix up a bowl and pot, or multiple instances of the same kind of object). Some examples of Atomic Motion instructions are: 

- ’move left’ 

- ’move right and down’ 

- ’move down and close’ 

- ’open the gripper’ 

- ’move the cloth left’ 

- ’pull the drawer handle backward’ 

Motion commands are good for general positioning, such as moving to a pre-grasp pose above the object the robot must interact with. They can also be used for more minor corrections, e.g., ’move up and right above the bowl’ if the gripper is too low. These commands are also appropriate when the task involves spatial reasoning (e.g., tasks that reference left or right) or moving in unconventional ways (e.g., lifting the arm to grasp something on a high shelf). However, these commands are often underspecified, so the robot may reach for the wrong object if simply told ’move to the right and grasp.’ Some examples of Position-based instructions are: 

- ’pick up the object at <mushroom>’ 

- ’go to the pot at <pot> to grab the mushroom’ 

Note, you simply need to specify the object name within angle brackets, e.g., <mushroom>, and a object detector system will fill in the pixel coordinates for you. If there are multiple instances of the object, provide a unique, specific identifier within the brackets to indicate which instance you are referring to, e.g., <mushroom on the left>. 

Position-based commands are especially helpful for specifying novel objects that the robot fails to recognize by name. They can also be used to clearly specify locations, such as where to place or move objects. However, these commands can be unreliable, as the robot may get confused (e.g., reaching for the wrong object in scenes with clutter or with multiple instances of the same object). The object detector may also fail, especially when objects are occluded. 

Next, some examples of Combination instructions are: 

- ’move down to the object at <mushroom> and grasp it’ 

- ’grab the mushroom at <mushroom on the left> and move it to <plate>’ 

- ’move the stuffed toy toward the box at <box>’ 

Combination commands are useful for supplementing the weaknesses of other command types, such as saying ’move right to grasp the object at <object description>’ rather than just ’move right and grasp’ (if there are multiple objects to the right of the robot). However, being too specific may result in out-of-distribution commands, which the robot policy fails to follow. Additionally, less specific commands can be useful for positioning the robot in a location where it’s more likely to succeed. 

Finally, there is the RESET TO HOME instruction, which causes the robot to return to its home position. You use this if the robot is stuck or interacting with the wrong object. You MUST follow these steps when generating your response: 

- Step 1: Briefly describe the scene in the current observation, and any important differences from past observations (eg. objects moved, picked up, dropped etc). 

- Step 2: Briefly describe what must happen next to make progress towards the overall task. 

- Step 3: Generate a candidate instruction for EACH level of abstraction. 

- Step 4: Briefly reason about which instruction is most appropriate given the current observation and task progress. 

- Step 5: Determine the final steerable command for the robot to execute. Only the LAST line of your output will be interpreted as the subtask command. In the LAST line, answer ONLY with the subtask instruction that the robot should execute, and NOTHING ELSE. 

Note: The robot will ask you for a new instruction after executing for a few steps. If you’ve issued the same type of command more than once without progress, you MUST issue a command at a different level of abstraction. If you previously provided a command with positions <> (without progress), you MAY NOT use positions in the next command. For example: - If you previously tried to pick up the mushroom by specifying the mushroom’s position, but the robot did not reach the mushroom, next time you can explicitly tell the robot to move in a certain direction (eg. move to the right and down). - If the robot reached for the wrong object when you told it to pick up the mushroom at <mushroom on the left>. This time, you should give a command at a different level of abstraction: move left to the mushroom and grasp it. Here are the past observations and commands: Observation: [image] Command: [command] Observation: [image] Command: [command] Observation: 

[image] Command: [command] ... Current Observation: 

[image] 

Based on this observation, generate the next command. Remember the instructions: describe the scene, determine what must happen next, generate steerable commands at EACH level of abstraction, determine the 

best command, output the best command. Again, the LAST line of your output will be interpreted as the final steerable, subtask command. In the LAST line, answer ONLY with the subtask instruction that the robot should execute, and NOTHING ELSE. 

Fig. 22: Our approach’s Gemini prompt for in-context learning VLM experiments. Note that any text in square brackets (eg. [task description]) in the prompt above is replaced with the corresponding object before the prompt is passed to the VLM. 

You are guiding a robot to complete a task by generating a subtask instruction for the robot to follow given an image of the robot’s current observation, and a history of observations and past commands. The robot is trying to accomplish the overall task: ’[task description]’. You should keep the rest of the environment unchanged. Note that all objects required for the task are present (no need to search for objects). There are several kinds of instructions the robot understands, each at a different level of abstraction, detailed below. Sometimes, a high-level instruction is sufficient for the robot to make progress towards solving the task, but other times, a more specific command is required. Below are examples of the kinds of instructions you can generate for the robot. Some examples of High-level instructions are: 

- ’grasp the mushroom in the pot’ 

- ’wipe the cloth across the table’ 

- ’move the lid above the pot’ 

- ’lift the carrot up’ # IMPORTANT: Lifting is generallly good post-grasping 

- ’move towards the stuffed toy’ 

- ’drop the eggplant in the bowl’ 

The robot is generally reliable at following high-level commands, especially when interacting with non-novel objects. They can also be used to better understand the scene and robot state, such as by saying ’lift the object’ to ascertain if the robot has actually firmly grasped it. However, these commands may fail when interacting with novel objects, as the robot may not recognize them by name. The robot also may also confuse similar objects with each other (e.g., it may mix up a bowl and pot, or multiple instances of the same kind of object). Some examples of Atomic Motion instructions are: 

- ’move left’ 

- ’move right and down’ 

- ’move down and close’ 

- ’open the gripper’ 

- ’move the cloth left’ 

- ’pull the drawer handle backward’ 

Motion commands are good for general positioning, such as moving to a pre-grasp pose above the object the robot must interact with. They can also be used for more minor corrections, e.g., ’move up and right above the bowl’ if the gripper is too low. These commands are also appropriate when the task involves spatial reasoning (e.g., tasks that reference left or right) or moving in unconventional ways (e.g., lifting the arm to grasp something on a high shelf). However, these commands are often underspecified, so the robot may reach for the wrong object if simply told ’move to the right and grasp.’ Some examples of Position-based instructions are: 

- ’pick up the object at <mushroom>’ 

- ’go to <pot>’ 

- ’grasp at <blue cube>’ 

- ’move above <plate>’ - ’open gripper at <bowl>’ 

- ’move towards <towel>’ 

Note, you simply need to specify the object name within angle brackets, e.g., <mushroom>, and a object detector system will fill in the pixel coordinates for you. If there are multiple instances of the object, provide a unique, specific identifier within the brackets to indicate which instance you are referring to, e.g., <mushroom on the left>. 

Position-based commands are especially helpful for specifying novel objects that the robot fails to recognize by name. They can also be used to clearly specify locations, such as where to place or move objects. However, these commands can be unreliable, as the robot may get confused (e.g., reaching for the wrong object in scenes with clutter or with multiple instances of the same object). The object detector may also fail, especially when objects are occluded. Next, some examples of Combination instructions are: 

- ’move down to the object at <mushroom> and grasp it’ 

- ’grab the mushroom at <mushroom on the left> and move it to <plate>’ 

- ’move the stuffed toy toward the box at <box>’ 

Combination commands are useful for supplementing the weaknesses of other command types, such as saying ’move right to grasp the object at <object description>’ rather than just ’move right and grasp’ (if there are multiple objects to the right of the robot). However, being too specific may result in out-of-distribution commands, which the robot policy fails to follow. Additionally, less specific commands can be useful for positioning the robot in a location where it’s more likely to succeed. 

Finally, there is the RESET TO HOME instruction, which causes the robot to return to its home position. You use this if the robot is stuck or interacting with the wrong object. 

You MUST format your response as follows: ONLY OUTPUT A SINGLE COMMAND AND NOTHING ELSE. YOUR RESPONSE SHOULD ONLY HAVE ONE LINE, WHICH IS THE COMMAND THE ROBOT MUST EXECUTE. Here are the past observations and commands: 

Observation: [image] Command: [command] Observation: [image] Command: [command] Observation: [image] Command: [command] ... Current Observation: [image] 

Based on this observation, generate the next command. Again, ONLY OUTPUT A SINGLE LINE, and NOTHING ELSE. 

Fig. 23: Non-reasoning ablation’s Gemini prompt for in-context learning VLM experiments. The only change from the full prompt (Fig. 22) is that the VLM is instructed to answer without producing any thinking tokens. In particular, the VLM is still may output commands leveraging all levels of abstraction, and leverage in-context examples and history of past observations and commands. Note that any text in square brackets (eg. [task description]) in the prompt above is replaced with the corresponding object before the prompt is passed to the VLM. 

You are guiding a robot to complete a task by generating a subtask instruction for the robot to follow given an image of the robot’s current observation, and a history of observations and past commands. The robot is trying to accomplish the overall task: ’[task description]’. You should keep the rest of the environment unchanged. Note that all objects required for the task are present (no need to search for objects). Below are some examples of the kinds of instructions you should generate: - ’grasp the mushroom in the pot’ - ’wipe the cloth across the table’ - ’move the lid above the pot’ You MUST follow these steps when generating your response: 

- Step 1: Briefly (1-2 sentences) describe the scene in the current observation, and any important differences from past observations (eg. objects moved, picked up, dropped etc). 

- Step 2: Briefly (1 sentence) describe what must happen next to make progress towards the overall task. 

- Step 3: Determine the final steerable command (last line) for the robot to execute. Only the LAST line of your output will be interpreted as the subtask command. In the LAST line, answer ONLY with the subtask instruction that the robot should execute, and NOTHING ELSE. Here are the past observations and commands: 

Observation: [image] Command: [command] Observation: [image] Command: [command] Observation: [image] Command: [command] ... Current Observation: [image] 

Based on this observation, generate the next command. Remember the instructions: describe the scene, determine what must happen next, and generate a command. Again, the LAST line of your output will be 

interpreted as the final subtask command. In the LAST line, answer ONLY with the subtask instruction that the robot should execute, and NOTHING ELSE. 

Fig. 24: SayCan-like baseline’s Gemini prompt for in-context learning VLM experiments. The only change from the full prompt (Fig. 22) is that the VLM is instructed to only provide subtask-level instructions. In particular, the VLM is still encouraged to reason in-context from a history of past observations and commands. Note that any text in square brackets (eg. [task description]) in the prompt above is replaced with the corresponding object before the prompt is passed to the VLM. 

## [observation image] 

What is the pixel coordinate location of the [object name] in the image? The image has width [width] and height [height] Respond with a JSON object with the keys ’x’ and ’y’. 

Fig. 25: Prompt for extracting grounded keypoints from image observations based on a description of a target object. If a VLM instruction contains multiple keypoint descriptions, this prompt is called multiple times. Note that any text in square brackets (eg. [image observation]) in the prompt above is replaced with the corresponding object before the prompt is passed to the VLM. 

