---
title: "CRAFT: Adapting VLA Models to Contact-rich Manipulation via Force-aware Curriculum Fine-tuning"
date: "2026-02-13"
authors: "Yike Zhang; Yaonan Wang; Xinxin Sun; Kaizhen Huang; Zhiyuan Xu; Junjie Ji"
url: https://arxiv.org/abs/2602.12532
pdf: https://arxiv.org/pdf/2602.12532
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.12532)** / [論文ページ](https://arxiv.org/abs/2602.12532)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **CRAFT: Adapting VLA Models to Contact-rich Manipulation via Force-aware Curriculum Fine-tuning** 

Yike Zhang<sup>1</sup><sup>_,_2</sup> , Yaonan Wang<sup>1</sup> , Xinxin Sun<sup>1</sup><sup>_,_2</sup> , Kaizhen Huang<sup>1</sup><sup>_,_2</sup> , Zhiyuan Xu<sup>2</sup> , Junjie Ji<sup>2</sup><sup>_,_†</sup> , Zhengping Che<sup>2</sup><sup>_,_†</sup> , Jian Tang<sup>2</sup> , Jingtao Sun<sup>1</sup><sup>_,_3</sup><sup>_,_�</sup> 

**_Abstract_ — Vision–Language–Action (VLA) models have shown a strong capability in enabling robots to execute general instructions, yet they struggle with contact-rich manipulation tasks, where success requires precise alignment, stable contact maintenance, and effective handling of deformable objects. A fundamental challenge arises from the imbalance between highentropy vision and language inputs and low-entropy but critical force signals, which often leads to over-reliance on perception and unstable control. To address this, we introduce CRAFT, a force-aware curriculum fine-tuning framework that integrates a variational information bottleneck module to regulate vision and language embeddings during early training. This curriculum strategy encourages the model to prioritize force signals initially, before progressively restoring access to the full multimodal information. To enable force-aware learning, we further design a homologous leader–follower teleoperation system that collects synchronized vision, language, and force data across diverse contact-rich tasks. Real-world experiments demonstrate that CRAFT consistently improves task success, generalizes to unseen objects and novel task variations, and adapts effectively across diverse VLA architectures, enabling robust and generalizable contact-rich manipulation.** 

## I. Introduction 

The emergence of large-scale foundation models, including Vision-Language Models (VLMs) and Large Language Models (LLMs), has significantly advanced artificial intelligence and robotics. These models exhibit strong capabilities in perception, reasoning, and grounding, enabling robots to follow natural language instructions and adapt across diverse environments. By leveraging massive pretraining and multimodal alignment, foundation models have become a promising paradigm for scalable robot intelligence. 

With the advent of powerful foundation models, the Vision–Language–Action (VLA) paradigm has emerged as a promising framework that integrates pretrained visual and language representations with robot learning systems, translating high-level semantic goals into low-level motor actions. Recent works such as RT-1/RT-2 [1], [2], SayCan [3], and OpenVLA [4] demonstrate strong zero-shot generalization 

This work was in part funded and supported by Beijing Innovation Center of Humanoid Robotics.<sup>†</sup> Project Leads: Junjie Ji and Zhengping Che. �Corresponding Author: Jingtao Sun. 

> 1National Engineering Research Center of Robot Visual Perception and Control Technology, Hunan University, Changsha, 410082, China. Yike Zhang, Yaonan Wang, Kaizhen Huang, and Xinxin Sun: _{_ b240900525, yaonan, huangkaizhen, s2001 _}_ @hnu.edu.cn 

> 2Beijing Innovation Center of Humanoid Robotics, Beijing, 102600, China. Zhiyuan Xu, Junjie Ji, Zhengping Che, and Jian Tang: _{_ eric.xu, jacob.ji, z.che, jian.tang _}_ @x-humanoid.com 

> 3Department of Electrical and Computer Engineering, National University of Singapore, 119077, Singapore. Jingtao Sun: jingtao ~~s~~ un@nus.edu.sg 


Fig. 1: **Homologous leader–follower teleoperation system.** The operator controls the leader arm while the follower arm mirrors the motion. Real-time force feedback enables natural interaction sensing, and two synchronized cameras capture first-person and third-person visual observations. 

to novel objects, instructions, and environments, marking an important milestone for general-purpose robotic agents. More recent approaches, including RDT [5] and _𝜋_ 0 [6], further underscore the potential of unifying large-scale multimodal pretraining with robot control, highlighting scalability across diverse tasks and robot architectures. 

However, despite recent advances, contact-rich manipulation remains a fundamental challenge for VLA models. Tasks such as precise insertions, deformable object rolling, or continuous surface wiping require precise alignment and dynamic regulation of contact forces, yet existing models often fail to meet these demands. This limitation arises from two key issues. First, relying predominantly on high-entropy visual and language inputs makes it difficult to achieve the fine alignment required in contact-rich settings, as perceptual inputs alone cannot capture subtle physical interactions at the point of contact. Second, the absence of explicit force or tactile feedback deprives models of low-entropy but taskcritical signals that reveal resistance or slip, leading to unstable, imprecise, or even unsafe behaviors. 

Several prior works have sought to improve contact-rich manipulation. Reactive Diffusion Policy (RDP) [7] introduces a slow–fast visual–tactile policy learning scheme to improve stability and responsiveness in contact-rich manipulation. VLA-Touch [8] enhances VLA models with dual-level tactile feedback, demonstrating the importance of incorporating finegrained touch signals alongside visual and language inputs. ForceVLA [9] further extends this line of work by introducing a force-aware mixture-of-experts architecture, enabling VLA models to better exploit force information in physically 

demanding tasks. While these methods represent promising steps toward force-aware VLA models, they remain limited by modality entropy imbalance and the lack of a unified mechanism to regulate multimodal contributions. As a result, current approaches still struggle to prioritize low-entropy yet critical force signals, leaving robust and generalizable contactrich manipulation as an open challenge. 

To address these challenges, we present **CRAFT** , a lightweight and model-agnostic framework for adapting pretrained VLA models to contact-rich manipulation. CRAFT introduces a variational information bottleneck (VIB) [10] after the vision–language encoder to temporarily restrict the information flow from visual and language embeddings. Within a curriculum fine-tuning scheme, the VIB initially imposes a strong Kullback–Leibler (KL) penalty that suppresses highentropy visual and language signals, compelling the policy to focus on low-entropy force inputs and thereby acquire stable, contact-aware behaviors. As training progresses, the weight of the VIB regularization is gradually annealed, releasing the bottleneck and allowing the model to reincorporate rich perceptual information while retaining the previously learned force-sensitive representations. This staged force-first-thenmultimodal strategy enables CRAFT to efficiently and seamlessly adapt VLA models to contact-rich manipulation tasks, while preserving their multimodal perception capabilities. 

We empirically validate CRAFT on five challenging realworld tasks, including fine-alignment insertions, continuous contact wiping, and manipulation of deformable objects. Experimental results demonstrate that CRAFT improves task success rates, enhances generalization to unseen objects and novel tasks, and adapts to multiple popular VLA architectures such as RDT and _𝜋_ 0. These findings highlight the effectiveness of combining information-theoretic modality control with force-aware curriculum fine-tuning to enable robust, generalizable contact-rich manipulation in VLA models. Overall, our main contributions are summarized as follows: 

- We introduce **CRAFT** , a general framework that adapts VLA models to **C** ontact- **R** ich manipulation with a Force- **A** ware curriculum **F** ine- **T** uning strategy, leveraging a variational information bottleneck to balance the influence of vision, language, and force modalities. 

- We develop a homologous leader-follower teleoperation system for data collection based on an off-the-shelf robot arm without additional sensor installation, which enables synchronized vision, language, and force recording across diverse contact-rich tasks, which facilitates robust policy learning and evaluation of force-aware VLA models. 

- Extensive real-world experiments demonstrate that our proposed CRAFT enhances task success, improves generalization to unseen objects and novel tasks, and is broadly applicable across different VLA-based approaches. 

## II. RELATED WORK 

## _A. Vision-Language-Action Models_ 

VLA models aim to map visual observations and high-level language commands into robot actions. Early works primarily 

focused on learning vision-to-action mappings from largescale real-world datasets [11]–[16], often relying on extensive demonstrations and task-specific engineering. While effective for individual tasks, these approaches typically struggle to generalize to novel objects or instructions. More recent methods incorporate semantic priors, generative modeling, or diffusion-based action prediction to enhance zero-shot generalization [17]–[26]. Recent representative approaches [5], [6] leverage diffusion or flow-based frameworks to predict complex action sequences, enabling more flexible and scalable policy representations. These models demonstrate the potential of unifying pretrained visual and language representations with robot control, allowing for the execution of diverse manipulation tasks from high-level instructions without taskspecific retraining. 

Despite these advances, most VLA models largely ignore force or tactile feedback [27]–[29], which are critical for contact-rich manipulation tasks such as precise insertions, rolling deformable objects, or continuous surface wiping. Several recent works have attempted to incorporate force or tactile signals as auxiliary inputs. For example, RDP introduces a slow-fast visual-tactile policy learning scheme to improve responsiveness and stability [7], VLA-Touch incorporates dual-level tactile feedback to complement visual and language modalities [8], and ForceVLA employs a forceaware mixture-of-experts architecture to leverage force signals in predicting action sequences [9]. Closely related to our work, FACTR [30] proposes a curriculum learning strategy that corrupts visual inputs with decreasing intensity via Gaussian blur to prioritize force signals early in training. However, while FACTR relies on heuristic schedules of input degradation to shift modality focus, CRAFT leverages the Information Bottleneck principle [31] to explicitly compress high-entropy visual and language representations. This provides a theoretically grounded mechanism to regulate multimodal information flow, ensuring that force features are robustly established in the latent space before fully reintegrating dense perceptual data. As a result, scalable and generalizable force-aware VLA learning remains an open challenge, motivating the need for a framework that systematically integrates and balances multimodal signals for robust contact-rich manipulation. 

## _B. Information Bottleneck in Multimodal Learning_ 

The Information Bottleneck (IB) [31] provides a principled framework to compress input redundancy while preserving task-relevant information, balancing representation compactness with predictive performance. Its variational extension, the deep variational information bottleneck (VIB) [10], enables efficient implementation in deep neural networks by approximating the IB objective with tractable variational distributions, and has been widely adopted in multimodal and high-dimensional representation learning for its ability to reduce noise, prevent overfitting, and improve interpretability. 

In multimodal settings, IB-based approaches have been applied to align heterogeneous modalities such as image and text. Graph IB [32] and Learning with Decodable IB [33] focus on learning compact, task-relevant embeddings 

while preserving decodability, and Restricting the Flow [34] demonstrates IB’s utility for controlling information flow in attribution tasks. Similarly, the Deep Copula IB [35] learns sparse latent representations that capture essential crossmodal dependencies. More recent work, such as the Dynamic Multimodal Information Bottleneck [36], introduces adaptive compression–fidelity constraints that allow dynamic control over each modality’s contribution in fused representations. These techniques have been used to improve robustness, interpretability, and generalization in models such as CLIP [37]. 

Despite these advances, most IB-based methods concentrate on perception-level representations, with limited efforts directed toward regulating the relative influence of vision, language, and force modalities in VLA frameworks for contactrich manipulation. Existing attempts to integrate tactile or force signals into policy learning often remain at the level of auxiliary features or low-level controllers [38], [39], lacking mechanisms to adaptively balance multimodal contributions during action prediction. Consequently, there remains a significant gap in developing scalable and generalizable force-aware VLA models that can systematically balance multimodal information throughout both learning and execution, motivating our proposed CRAFT framework that leverages VIB to regulate vision, language, and force contributions for robust contactrich manipulation. 

## III. Method 

While visual and language signals provide high-entropy information about the scene, force signals are inherently lower in entropy but uniquely capture direct physical interactions, making them indispensable for stable and precise contactrich manipulation. In this section, we introduce CRAFT, a general framework that equips existing VLA models with the ability to perform contact-rich manipulation guided by force information, as shown in Fig. 2. CRAFT inserts a variational information bottleneck after vision and language embeddings to regulate their information entropy, enforcing a curriculum that encourages the model to prioritize the force modality during the early stages of training, and gradually restores the contribution of visual and language signals thereafter. 

## _A. Homologous Leader-Follower Teleoperation System_ 

To enable force-aware curriculum fine-tuning, we design a homologous leader–follower teleoperation system inspired by HACTS [40] and FACTR [30]. Our setup employs an off-the-shelf robot arm, i.e., Franka Emika Panda, without the need for additional tactile or force sensors, alongside a leader arm constructed from low-cost servo motors with builtin force control, eliminating the reliance on high-precision and expensive haptic equipment such as HaptX Gloves or specialized haptic devices. As illustrated in Fig. 1, the operator controls the leader arm while the follower arm precisely mirrors the commanded motions. Contact forces measured at the follower are fed back to the leader in real time, allowing the operator to naturally perceive interaction forces and provide high-quality demonstrations. The bidirectional synchronization in our system enables fine-grained force 

control during teleoperation, ensuring that the collected force data is both accurate and reliable. 

The robot operates under impedance control, which modulates compliance during physical interaction to prevent mechanical locking and ensure safe, stable contact. Joint torque is used as the force modality, providing richer and more informative interaction data than joint positions alone, while remaining broadly accessible across most robotic platforms. 

Visual observations are captured from two synchronized cameras: a wrist-mounted camera for first-person perspectives and a static third-person camera for environmental context. All sensory modalities—including multi-view images, proprioceptive states, joint torques, and robot actions—are temporally synchronized and processed for seamless integration into the CRAFT framework, providing a comprehensive multimodal foundation for force-aware policy learning. 

## _B. Force-aware Curriculum Fine-tuning_ 

Directly incorporating force modality alongside visual and language inputs often results in the force modality being underutilized, especially given the sparsity and lower information content of the force signal compared to rich visual and language signals. Consequently, the model tends to overly rely on visual and language signals, limiting its ability to leverage critical contact information encoded in the force modality. 

To mitigate this imbalance, we propose Force-aware Curriculum Fine-tuning, a strategy that initially emphasizes the force modality by constraining the information from visual and language signals through a variational information bottleneck module with KL divergence regularization. This constraint is gradually relaxed via a weight schedule, enabling the model to progressively reintegrate rich multimodal information while retaining the force-aware representations learned during early training. Notably, this strategy can be applied as a plugin to various pretrained VLA models, providing a unified framework that equips them with force-aware capabilities. **Variational Information Bottleneck (VIB).** In contact-rich manipulation, the force signal plays a crucial role in stabilizing the interaction and detecting external constraints. However, considering the multimodal policies that jointly process vision, language, and proprioception inputs, the high entropy of visual and language features often dominates the representation space, making it difficult for the policy to exploit force-related signals effectively. To address this, we applied the VIB [10] module to the visual and language embeddings _𝐹𝑉_ and _𝐹𝐿_ , encouraging the model to prioritize low-entropy, task-relevant proprioception. 

As illustrated in Fig. 2, at each timestep _𝑡_ , the policy observes _𝑂𝑡_ = { _𝑉𝑡 , 𝜏𝑡_ } and receives a language instruction _𝐿_ , producing a sequence of actions _𝐴𝑡_ = { _𝑎𝑡 , . . . , 𝑎𝑡_ + _𝐻_ −1} over a horizon _𝐻_ . Since visual and language signals typically exhibit significantly higher entropy H ( _𝑉𝑡_ ) _,_ H ( _𝐿_ ) ≫H ( _𝜏𝑡_ ), where H (·) denotes entropy, a naive policy tends to overfit to perceptual modalities while ignoring the force modality _𝜏𝑡_ . 

Tomitigate thisimbalance, wecompress thefusedvisual and language embeddings _𝐹𝑉𝑡_ and _𝐹𝐿_ into compact latent features _𝐹𝑉_<sup>_𝑐_</sup> _𝑡_<sup>and</sup><sup>_𝐹_</sup> _𝐿_<sup>_𝑐_viatheVIBmodule,andminimizethemutual</sup> 


Fig. 2: **Overview of CRAFT.** CRAFT mitigates the imbalance between high-entropy perceptual signals (vision and language) and low-entropy force signals in contact-rich manipulation. The VIB module initially compresses visual and language features to emphasize force information, and a curriculum weight schedule gradually relaxes this constraint, allowing the policy to integrate rich multimodal signals while retaining force-aware representations. CRAFT can be applied to diverse VLA models. 

information between the original and compact features: 


Since the true marginal _𝑝_ ( _𝐹_<sup>_𝑐_</sup> ) is intractable, we introduce a variational approximation _𝑞_ ( _𝐹_<sup>_𝑐_</sup> ), which yields the following upper bound: 


where _𝐾𝐿_ (·) represents the Kullback-Leibler divergence loss [41]. We set the prior _𝑞_ ( _𝐹_<sup>_𝑐_</sup> ) to a standard normal N (0 _,_ 1) and model the posterior as _𝑝_ ( _𝐹_<sup>_𝑐_</sup> | _𝐹_ ) = N ( _𝜇, 𝜎_<sup>2</sup> ), where _𝜇_ and _𝜎_ are predicted by separate linear layers. This leads to the VIB loss: 


At the stage of fine-tuning, the compact features are sampled via the reparameterization trick: 


This construction dynamically regulates the information from high-entropy perceptual modalities. During the early stages of finetuning, KL regularization encourages the policy to rely more heavily on low-entropy proprioception features. As training advances, the VIB gradually relaxes, allowing vision and language to contribute complementary information once the force-aware policy is stabilized. 

**Force as Proprioception.** In robotic manipulation, particularly for contact-rich tasks, it is crucial for the policy to accurately perceive the robot-environment interaction forces. Rather than relying on joint positions _𝑞_ as the proprioception input, we leverage joint torques _𝜏_ , which inherently capture richer force-aware information and serve as a task-relevant 

representation. Under standard joint-level impedance control, the commanded torque can be expressed as: 


where _𝑞, 𝑞,_ � _𝑞_ � denote the current joint positions, velocities, and accelerations, respectively, _𝑞𝑑, 𝑞_ � _𝑑, 𝑞_ � _𝑑_ represent the desired trajectories, _𝐾, 𝐷_ are the impedance gains, _𝑀_ is the jointspace inertia matrix, and _𝜏_ ext captures the external torques arising from environment contacts. 

This formulation reveals that torque _𝜏_ encodes not only the current kinematic state ( _𝑞, 𝑞,_ � _𝑞_ �), but also: 

- Task-level deviations ( _𝑞𝑑_ − _𝑞_ ) and ( � _𝑞𝑑_ −� _𝑞_ ), representing how far the system is from the desired motion. 

- Dynamic discrepancies ( � _𝑞𝑑_ −� _𝑞_ ), capturing inertial effects that are absent when using _𝑞_ alone. 

- External interaction forces _𝜏_ ext, which are essential for understanding contacts and constraints. 

From an information-theoretic perspective, torque signals generally carry higher information content than positions alone. Since _𝜏_ is a deterministic function of multiple system variables, including desired and measured accelerations, its entropy satisfies: 


where _𝑓_ (·) denotes the impedance control mapping. Consequently, the mutual information between _𝜏_ and the underlying system dynamics satisfies: 


By feeding joint torque into the policy alongside visual and language features, the model achieves improved observability over both internal system dynamics and external contacts, 

thereby facilitating the learning of robust, contact-aware manipulation strategies. 

**VIB Weight Schedule.** To effectively integrate multimodal information while encouraging force-aware learning, we introduce a dynamic scheduling strategy for the VIB regularization term in the total loss. At the beginning of training, we assign a relatively high weight _𝜆_ VIB to the VIB regularization, which strongly compresses the high-entropy visual and language features. This forces the policy to prioritize the low-entropy torque signals, enabling the model to acquire robust contactaware representations in the early stages. As training advances, _𝜆_ VIB is gradually decreased according to an exponential decay schedule, allowing the model to progressively reintegrate the visual and linguistic information without losing the forcedominated representations learned previously. 

Formally, the overall loss function is: 


where Ltask denotes the original imitation learning loss, and _𝜆_ VIB( _𝑡_ ) is the VIB weight at training step _𝑡_ . Furthermore, we define the VIB weight schedule as follows: 


where _𝜆_ init is the initial VIB weight and _𝑇_ decay is a decay constant controlling the speed of information reintegration. This exponential decay enforces strong information compression during the early training phase, ensuring the policy focuses on torque-based force signals, while progressively reducing the regularization to enable richer integration of visual and language modalities in later stages. 

## _C. Implementation_ 

To demonstrate the generalizability of CRAFT, we implement it on two representative VLA models, the flow-based _𝜋_ 0 and the diffusion-based RDT. For fine-tuning, we first collect force-aware demonstrations using our homologous leader-follower teleoperation system, providing high-quality and diverse data on various contact-rich tasks. The given VLA models (pretrained only with vision and language inputs) are then adapted to these tasks using their corresponding force-aware demonstrations. During fine-tuning, joint torques are introduced as proprioceptive inputs, and a lightweight VIB module is added after the pretrained vision–language encoder to regulate the information content of high-entropy visual and language modalities. This design enables CRAFT to effectively balance multimodal contributions during manipulation and can be seamlessly integrated into other VLA models without architectural modifications. Moreover, the VIB module is broadly applicable to low-entropy, task-critical modalities: while we focus on joint torques here, the same mechanism can be naturally extended to tactile feedback and similar proprioceptive inputs. 

## IV. Experiments 

We conduct real-world contact-rich manipulation experiments to evaluate the effectiveness of CRAFT in augmenting VLA models, guided by three key research questions: 


Fig. 3: **Representative contact-rich tasks.** (1) USB Insertion, (2) Flip Carton, (3) Wipe Whiteboard, (4) Rolling Plasticine, and (5) Shaft-to-Hole Insertion. 

- 1) **Main Results:** How does CRAFT enable VLA models to achieve superior performance in contact-rich manipulation tasks compared to their original counterparts? 

- 2) **Generalization Studies:** How do CRAFT-enhanced VLA models demonstrate stronger generalization to unseen objects and novel task variations? 

- 3) **Ablation Studies:** Why is the proposed Force-Aware Curriculum Finetuning design critical, and what is the contribution of each component to the overall effectiveness of CRAFT? 

## _A. Experimental Setup_ 

**Tasks.** We consider five representative contact-rich tasks: USB Insertion, Flip Carton, Wipe Whiteboard, Rolling Plasticine, and Shaft-to-Hole Insertion, as shown in Fig. 3. These tasks involve precise alignment, continuous surface interaction, and manipulation of deformable objects. Taskspecific success criteria are defined as follows: 

- USB/Shaft-to-Hole Insertion: The robot must insert a plug or shaft into a corresponding socket or hole, requiring precise alignment and controlled force application. A trial is considered successful if the plug or shaft is fully inserted into the corresponding socket or hole. 

- Flip Carton: The robot must flip a carton from horizontal orientation to vertical orientation while maintaining stability. A trial is successful if the target carton is flipped over completely without dropping or damaging it. 

- Wipe Whiteboard: The robot must wipe a designated area on a whiteboard with consistent contact. Success is determined by achieving at least 90% uniform wiping coverage of the marked area. 

- Rolling Plasticine: The robot must roll a block of plasticine into a cylindrical shape, requiring careful force control to avoid tearing. A trial is successful if the plasticine is rolled into a cylindrical shape without breaking or excessive deformation. 

**Training and Evaluation Protocol.** Each policy is trained with 50 teleoperated demonstrations per task, with randomized 


Fig. 4: **Task success rates of baselines and CRAFT-enhanced VLA models.** Across five representative manipulation tasks, CRAFT consistently improves success rates for both _𝜋_ 0-base and RDT. The gains are particularly significant for contact-rich tasks, demonstrating the effectiveness of our force-aware curriculum fine-tuning strategy. 

object poses to improve robustness. For evaluation, we perform a fixed number of trials for each task: 20 trials for USB Insertion, Shaft-to-Hole Insertion, and Flip Carton, and 12 trials for Wipe Whiteboard and Rolling Plasticine. 

**Baselines and Comparisons.** We compare CRAFTenhanced models against representative VLAs and a forceaware baseline: 

- FACTR [30]: A force-aware ACT [12] model, serving as a baseline for contact-rich manipulation tasks. 

- _𝜋_ 0-base [6]: A representative VLA model using flow matching but without force control. 

- RDT [5]: Another representative VLA model based on DiT [42] without force control. 

- _𝜋_ 0-base/RDT + CRAFT (Ours): _𝜋_ 0/RDT with forceaware curriculum fine-tuning. 

## _B. Main Results_ 

**CRAFT leads to better performances.** As shown in Fig. 4, our results demonstrate that the proposed CRAFT module significantly enhances the performance of VLA models in contact-rich manipulation tasks. Specifically, integrating CRAFT with the _𝜋_ 0-base model improves performance across five tasks, yielding an average increase of 35.36%. Notably, for the Wipe Whiteboard task, CRAFT enables a remarkable improvement of 33.4%(from 33.3% to 66.7%), underscoring its ability to enhance precision in tasks requiring sustained contact and force feedback. Similarly, RDT + CRAFT outperforms the baseline RDT model, advancing from 22.66% to 48.32%, with an average improvement of 25.66% points and a particularly strong gain of 50% in Rolling Plasticine (from 8.3% to 58.3%), highlighting CRAFT’s effectiveness in tasks demanding dynamic force control. Compared to the available baselines, FACTR and both CRAFT-enhanced models achieve superior results, with _𝜋_ 0-base + CRAFT consistently attaining the highest success rate across most tasks. These findings validate that CRAFT leads to better performance by enabling effective force-aware control in VLA models. 

**CRAFT enables force-aware control.** By leveraging joint torque feedback, CRAFT-enhanced models adapt their manipulation strategies in real time, enabling precise alignment, stable contact maintenance, and safer physical interactions in contact-rich environments. As shown in Fig. 5, in the USB Insertion task, the baseline VLA model (a) often misaligns 


Fig. 5: **CRAFT enables force-aware manipulation.** Comparison of _𝜋_ 0-base (a) and CRAFT-enhanced (b) on USB insertion and flip carton. CRAFT uses force signals to adjust motions, enabling successful execution. 

TABLE I: Average success rates across five contact-rich manipulation tasks. 

|Model|w/o CRAFT|w/ CRAFT|Δ(%)|
|---|---|---|---|
|RDT|22.66|**48.32**|**25.66**↑|
|_𝜋_0-base|25.32|**60.68**|**35.36**↑|


the connector and continues to attempt insertion, whereas the CRAFT-enhanced model (b) continuously adjusts its motion based on contact force signals to achieve successful insertion. In the Flip Carton task, CRAFT similarly uses force signals to guide the direction and magnitude of applied torques, ensuring stable flipping, while the baseline fails to coordinate force and motion, resulting in task failure. 

**CRAFT is broadly applicable to different VLA architectures.** CRAFT is designed as a lightweight, plugand-play finetuning module that enhances force awareness without modifying the underlying vision-language encoders. This modality-agnostic design requires minimal additional supervision, making CRAFT seamlessly compatible with diverse VLA frameworks at low integration cost. We validate this generality by applying CRAFT to both _𝜋_ 0 and RDT, where 


Fig. 6: **Generalization experimental setups.** Top: Original experimental setups. Bottom: Variants introduced for object-level and task-level generalization. 

the enhanced variants consistently achieve higher success rates on contact-rich manipulation tasks. As summarized in Tab. I, CRAFT boosts performance across different architectures, demonstrating the effectiveness of force-aware curriculum finetuning. 

## _C. Generalization Studies_ 

We further investigate whether CRAFT enhances generalization to unseen objects and novel task variations. Specifically, we introduce two types of Out-of-Distribution (OOD) variants: 

- _Object-level variants_ : Flip different Carton, and Rolling Plasticine with different colors. 

- _Task-level variants_ : USB Insertion with socket placement height changes and visual changes, and Wipe Whiteboard with different placement angles. 

As illustrated in Fig. 6, we evaluated the generalization performance across four contact-rich manipulation tasks—USB Insertion, Flip Carton, Wipe Whiteboard, and Rolling Plasticine—under object- and task-level OOD settings. For each variant, we conducted five evaluation trials per task, with success rates reported in Tab. II. The results demonstrate that CRAFT consistently improves success rates across all tasks, achieving an average increase from 22.50% to 58.75%, corresponding to a remarkable 36.25% improvement. Specifically, for the task-level variant of USB Insertion, CRAFT enhances the success rate from 1/10 (10%) to 4/10 (40%), showing its ability to handle precise force control. Similarly, in the objectlevel variant of Flip Carton, performance improves from 10/20 (50%) to 15/20 (75%), reflecting enhanced robustness to object variations. The Wipe Whiteboard task, another tasklevel variant, sees a significant gain from 2/10 (20%) to 6/10 (60%), underscoring the effectiveness of CRAFT in tasks requiring sustained contact and force feedback. Notably, for the object-level variant of Rolling Plasticine, CRAFT achieves a substantial improvement from 2/20 (10%) to 12/20 (60%), highlighting its capability to adapt to visual robustness. These improvements arise from the force-aware curriculum and 

TABLE II: Generalization performance on object- and task-level variants. 

|Task (Variant Type)|_𝜋_0 w/o CRAFT|_𝜋_0 w/ CRAFT|
|---|---|---|
|USB Insertion (Task)|1/10|**4/10**|
|Flip Carton (Object)|10/20|**15/20**|
|Wipe Whiteboard (Task)|2/10|**6/10**|
|Rolling Plasticine (Object)|2/20|**12/20**|
|Average|22.50%|**58.75%**|


torque-centered representations, which enhance the model’s focus on external torques and improve its understanding of task-relevant visual and language representations. Taken together, these results validate that CRAFT significantly strengthens robustness and generalization in contact-rich manipulation tasks under OOD settings. 

## _D. Ablation Studies_ 

To assess the contribution of each component in CRAFT, we conduct ablation experiments on the _𝜋_ 0-base model, focusing on three representative tasks: USB Insertion, Wipe Whiteboard, and Rolling Plasticine. Each variant is evaluated over 10 trials per task, with the reported metric being the average success rate across the three tasks. We consider the following key variants: 

- _w/o CRAFT_ : The _𝜋_ 0-base model. 

- _+ VIB_ : Incorporates the VIB layer while using joint positions as proprioception. 

- _+ VIB & Force_ : Combines VIB with joint torque as robot state (the full CRAFT setup). 

The results show that adding VIB alone substantially improves performance over the base model, highlighting the benefit of constraining visual and language embeddings to focus on proprioception information. Incorporating joint torque as the proprioception in combination with VIB further boosts success rates, confirming that torque provides richer, taskrelevant feedback critical for robust contact-rich manipulation. 

TABLE III: Ablation results. 

|Model Variant|w/o CRAFT|+ VIB|+ VIB & Force|
|---|---|---|---|
|Avg. Success (%)|20.0|46.7|**56.7**|


## V. Conclusion 

In this study, we introduced CRAFT, a force-aware curriculum fine-tuning framework designed to enhance VLA models for contact-rich manipulation. By integrating a variational information bottleneck with torque-based proprioception, CRAFT guides policies to effectively exploit force signals while simultaneously leveraging visual and language information. Experiments across five contact-rich tasks demonstrate that CRAFT improves success rates, generalizes to unseen objects and task variations, and is broadly applicable to different VLA architectures. These results highlight that incorporating a force-aware curriculum offers a lightweight yet powerful approach for achieving robust and generalizable contact-rich robotic manipulation. 

References 

model for synergizing cognition and action in robotic manipulation,” _arXiv preprint arXiv:2411.19650_ , 2024. 

- [1] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu _et al._ , “Rt-1: Robotics transformer for real-world control at scale,” _Robotics: Science and Systems XIX_ , 2023. 

- [2] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 

- [3] M. Ahn, A. Brohan, N. Brown, Y. Chebotar, O. Cortes, B. David _et al._ , “Do as i can, not as i say: Grounding language in robotic affordances,” in _Proceedings of the 6th Conference on Robot Learning_ , vol. 205. PMLR, 2023, pp. 287–773. 

- [4] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, _et al._ , “Openvla: An open-source vision-language-action model,” in _Conference on Robot Learning_ , 2025, pp. 2679–2713. 

- [5] S. Liu, L. Wu, B. Li, H. Tan, H. Chen, Z. Wang, K. Xu, H. Su, and J. Zhu, “Rdt-1b: a diffusion foundation model for bimanual manipulation,” in _International Conference on Learning Representations_ , 2024. 

- [6] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke _et al._ , “ _𝜋_ 0: A Vision-Language-Action Flow Model for General Robot Control,” in _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- [7] H. Xue, J. Ren, W. Chen, G. Zhang, Y. Fang, G. Gu, H. Xu, and C. Lu, “Reactive diffusion policy: Slow-fast visual-tactile policy learning for contact-rich manipulation,” in _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- [8] J. Bi, K. Y. Ma, C. Hao, M. Z. Shou, and H. Soh, “Vla-touch: Enhancing vision-language-action models with dual-level tactile feedback,” _arXiv preprint arXiv:2507.17294_ , 2025. 

- [9] J. Yu, H. Liu, Q. Yu, J. Ren, C. Hao, H. Ding, G. Huang, G. Huang, Y. Song, P. Cai, W. Zhang, and C. Lu, “ForceVLA: Enhancing VLA models with a force-aware moe for contact-rich manipulation,” in _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 

- [10] A. A. Alemi, I. Fischer, J. V. Dillon, and K. Murphy, “Deep variational information bottleneck,” in _International Conference on Learning Representations_ , 2017. 

- [11] Y. Jiang, A. Gupta, Z. Zhang, G. Wang, Y. Dou, Y. Chen, L. Fei-Fei, A. Anandkumar, Y. Zhu, and L. Fan, “Vima: General robot manipulation with multimodal prompts,” in _Proceedings of the 40th International Conference on Machine Learning_ , vol. 202, 2023, pp. 15 023–15 059. 

- [12] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” in _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 

- [13] W. Huang, C. Wang, R. Zhang, Y. Li, J. Wu, and L. Fei-Fei, “Voxposer: Composable 3d value maps for robotic manipulation with language models,” in _Proceedings of the 7th Conference on Robot Learning (CoRL)_ , vol. 229. PMLR, 2023, pp. 540–562. 

- [14] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” _The International Journal of Robotics Research_ , p. 02783649241273668, 2023. 

- [15] O. M. Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman _et al._ , “Octo: An open-source generalist robot policy,” in _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

- [16] K. Wu, N. Liu, Z. Zhao, D. Qiu, J. Li, Z. Che, Z. Xu, and J. Tang, “Learning from imperfect demonstrations with self-supervision for robotic manipulation,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 

- [17] Y. Yue, Y. Wang, B. Kang, Y. Han, S. Wang, S. Song, J. Feng, and G. Huang, “Deer-vla: Dynamic inference of multimodal large language models for efficient robot execution,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 56 619–56 643, 2024. 

- [18] S. Dey, J.-N. Zaech, N. Nikolov, L. Van Gool, and D. P. Paudel, “Revla: Reverting visual domain limitation of robotic foundation models,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025. 

- [19] J. Wei, S. Yuan, P. Li, Q. Hu, Z. Gan, and W. Ding, “Occllama: An occupancy-language-action generative world model for autonomous driving,” _arXiv preprint arXiv:2409.03272_ , 2024. 

- [20] Q. Li, Y. Liang, Z. Wang, L. Luo, X. Chen, M. Liao, F. Wei, Y. Deng, S. Xu, Y. Zhang _et al._ , “Cogact: A foundational vision-language-action 

- [21] J. Sun, Y. Wang, M. Feng, Y. Guo, A. Mian, and M. Z. Shou, “L4d-track: Language-to-4d modeling towards 6-dof tracking and shape reconstruction in 3d point cloud stream,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 21 146–21 156. 

- [22] J. Wen, Y. Zhu, J. Li, Z. Tang, C. Shen, and F. Feng, “Dexvla: Visionlanguage model with plug-in diffusion expert for general robot control,” in _Proceedings of the 9th Conference on Robot Learning_ , vol. 305. PMLR, 2025. 

- [23] P. Budzianowski, W. Maa, M. Freed, J. Mo, W. Hsiao, A. Xie, T. M loduchowski, V. Tipnis, and B. Bolte, “Edgevla: Efficient visionlanguage-action models,” _arXiv preprint arXiv:2507.14049_ , 2025. 

- [24] M. Li, Z. Zhao, Z. Che, F. Liao, K. Wu, Z. Xu, P. Ren, Z. Jin, N. Liu, and J. Tang, “Switchvla: Execution-aware task switching for visionlanguage-action models,” _arXiv preprint arXiv:2506.03574_ , 2025. 

- [25] J. Sun, Y. Wang, and D. Wang, “Towards real-world aerial vision guidance with categorical 6d pose tracker,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2025. 

- [26] Y. Su, N. Liu, D. Chen, Z. Zhao, K. Wu, M. Li, Z. Xu, Z. Che, and J. Tang, “Freqpolicy: Efficient flow-based visuomotor policy via frequency consistency,” in _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. 

- [27] A. L. Thomaz and C. Breazeal, “Teachable robots: Understanding human teaching behavior to build more effective robot learners,” _Artificial Intelligence_ , vol. 172, no. 6-7, pp. 716–737, 2008. 

- [28] A. I. Weinberg, A. Shirizly, O. Azulay, and A. Sintov, “Survey of learning-based approaches for robotic in-hand manipulation,” _Frontiers in Robotics and AI_ , vol. 11, p. 1455431, 2024. 

- [29] J. Zhao, N. Kuppuswamy, S. Feng, B. Burchfiel, and E. Adelson, “Polytouch: A robust multi-modal tactile sensor for contact-rich manipulation using tactile-diffusion policies,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025. 

- [30] J. J. Liu, Y. Li, K. Shaw, T. Tao, R. Salakhutdinov, and D. Pathak, “Factr: Force-attending curriculum training for contact-rich policy learning,” in _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- [31] N. Tishby, F. C. Pereira, and W. Bialek, “The information bottleneck method,” in _Proceedings of the 37th Annual Allerton Conference on Communication, Control, and Computing_ , vol. 49. University of Illinois, 1999, pp. 368–377. 

- [32] T. Wu, H. Ren, P. Li, and J. Leskovec, “Graph information bottleneck,” _Advances in Neural Information Processing Systems_ , vol. 33, pp. 20 437–20 448, 2020. 

- [33] Y. Dubois, D. Kiela, D. J. Schwab, and R. Vedantam, “Learning optimal representations with the decodable information bottleneck,” _Advances in Neural Information Processing Systems_ , vol. 33, 2020. 

- [34] K. Schulz, L. Sixt, F. Tombari, and T. Landgraf, “Restricting the flow: Information bottlenecks for attribution,” in _International Conference on Learning Representations (ICLR)_ , 2020. 

- [35] A. Wieczorek, M. Wieser, D. Murezzan, and V. Roth, “Learning sparse latent representations with the deep copula information bottleneck,” in _International Conference on Learning Representations (ICLR)_ , 2018. 

- [36] Y. Fang, S. Wu, S. Zhang, C. Huang, T. Zeng, X. Xing, S. Walsh, and G. Yang, “Dynamic multimodal information bottleneck for multimodality classification,” in _Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision_ , 2024, pp. 7696–7706. 

- [37] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark _et al._ , “Learning transferable visual models from natural language supervision,” in _International conference on machine learning_ . PmLR, 2021, pp. 8748–8763. 

- [38] Y. Wang, T. G. Rudner, and A. G. Wilson, “Visual explanations of imagetext representations via multi-modal information bottleneck attribution,” _Advances in Neural Information Processing Systems_ , 2023. 

- [39] W. Xie and N. Correll, “Towards forceful robotic foundation models: a literature survey,” _arXiv preprint arXiv:2504.11827_ , 2025. 

- [40] Z. Xu, Y. Zhao, K. Wu, N. Liu, J. Ji, Z. Che, C. H. Liu, and J. Tang, “Hacts: a human-as-copilot teleoperation system for robot learning,” _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2025. 

- [41] S. Kullback and R. A. Leibler, “On information and sufficiency,” _The annals of mathematical statistics_ , vol. 22, no. 1, pp. 79–86, 1951. 

- [42] W. Peebles and S. Xie, “Scalable diffusion models with transformers,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2023, pp. 4195–4205. 

