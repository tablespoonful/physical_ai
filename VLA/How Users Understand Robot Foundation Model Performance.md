---
title: "How Users Understand Robot Foundation Model Performance through Task Success Rates and Beyond"
date: "2026-02-03"
authors: "Isaac Sheidlower; Jindan Huang; James Staley; Bingyu Wu; Qicong Chen; Reuben Aronson"
url: https://arxiv.org/abs/2602.03920
pdf: https://arxiv.org/pdf/2602.03920
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.03920)** / [論文ページ](https://arxiv.org/abs/2602.03920)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **How Users Understand Robot Foundation Model Performance through Task Success Rates and Beyond** 

**Isaac Sheidlower**<sup>1</sup> , **Jindan Huang**<sup>2</sup> , **James Staley**<sup>2</sup> , **Bingyu Wu**<sup>2</sup> , **Qicong Chen**<sup>2</sup> , **Reuben M Aronson**<sup>2</sup> and **Elaine Short**<sup>2</sup> 

1Brown University, Providence, RI, USA 

2Tufts University, Medford, MA, USA 

Isaac_Sheidlower@Brown.edu, jindan.huang@tufts.edu, james.staley625703@tufts.edu, bingyu.wu@tufts.edu, qicong.chen@tufts.edu, reuben.aronson@gmail.com, elaine.short@tufts.edu 

## **Abstract** 

Robot Foundation Models (RFMs) represent a promising approach to developing general-purpose home robots. Given the broad capabilities of RFMs, users will inevitably ask an RFM-based robot to perform tasks that the RFM was not trained or evaluated on. In these cases, it is crucial that users understand the risks associated with attempting novel tasks due to the relatively high cost of failure. Furthermore, an informed user who understands an RFM’s capabilities will know what situations and tasks the robot can handle. In this paper, we study how nonroboticists interpret performance information from RFM evaluations. These evaluations typically report task success rate (TSR) as the primary performance metric. While TSR is intuitive to experts, it is necessary to validate whether novices also use this information as intended. Toward this end, we conducted a study in which users saw real evaluation data, including TSR, failure case descriptions, and videos from multiple published RFM research projects. The results highlight that non-experts not only use TSR in a manner consistent with expert expectations but also highly value other information types, such as failure cases that are not often reported in RFM evaluations. Furthermore, we find that users want access to both real data from previous evaluations of the RFM and estimates from the robot about how well it will do on a novel task. 

## **1 Introduction** 

Robot Foundation Models (RFMs) promise that users can request robots to perform nearly arbitrary tasks to an acceptable standard. To realize this promise safely and effectively, users must be informed about RFM performance on such tasks, both to avoid risky or catastrophic failures and to understand when, how, and for which tasks a robot can be used successfully. The most prevalent evaluation metric for conveying this performance is _task success rate_ (TSR), defined as the ratio of successful task executions to total attempts. TSR is often interpreted as an indication of how likely the robot is to succeed at that task. TSR is useful for novices and experts alike: experts 


Figure 1: This work investigates how people interpret commonly reported robot foundation model performance information. We verify that non-experts value information like task success rate, while also wanting other information types less readily available. This work serves to inform future robot foundation model evaluations as well as what information should be available to end-users during deployments and when they request tasks. 

can use TSR to compare the performance of an RFM on different tasks, while novices may find TSR particularly useful when requesting an RFM-based robot to perform a novel task, or a task that the user has not seen the robot perform. If the robot provides an accurate estimate of the TSR, or a TSR based on a very similar task, then the user can better decide how to use the robot. 

Consider the task of putting a vase away on a shelf: if the TSR on that task is very high, the person can confidently request the robot to perform that task with little supervision. If the TSR is very low, the person may choose to closely monitor the robot, further teach the robot, or decide it should not attempt the task at all. While TSR is the most commonlyused metric for assessing RFMs, other information about robot performance can be helpful. _Failure cases_ , which describe how a robot failed in natural language, are less commonly 

reported in RFM evaluations but are useful for predicting and preparing for failures. For example, if the robot explains that dropping the vase is a possible failure case, then the user may closely monitor the robot and be prepared to catch the vase. If the user is not provided with this information, then the robot may fail unexpectedly, causing both a broken vase and potentially broken trust in the robot in general. The more informed a user is about an RFM’s capabilities, the better they can use it for routine and creative tasks alike. 

In this work, we study how **novice** users interact with RFM evaluations from real robots, focusing on their interpretations of TSR and failure cases. Our goal is to understand what information users need when using RFM-based robots for novel tasks, how they interpret commonly reported evaluation data, and where gaps exist between reported and user-desired information. We focus on scenarios in which users request tasks they have not seen the robot execute and that the RFM has not previously attempted, requiring information to compensate for this lack of experience. We conducted an online study ( **n** =112) using real RFM evaluation data, and an in-person study ( **n** =14) with an autonomous robot to examine how embodiment affects information needs. 

Our contributions are: **(1)** We empirically validate that nonexpert users interpret TSR in a manner consistent with expert expectations, demonstrating a robust positive correlation between TSR values and user-reported trust and confidence in the system. **(2)** We show that natural language descriptions of failure cases are highly valued by non-expert users because they further inform their understanding of the risks associated with using the robot, suggesting a need to standardize failure case reporting. We also provide recommendations for information types that should be available during RFM deployments based user data, such as the speed at which a task can be completed and the RFM’s propensity for human-robot collaborations. **(3)** Finally, we highlight the necessity of providing users both with _real_ evaluation data of similar tasks to the ones users request, suggesting the need for RFMs to be deployed with access to a large history of evaluations, and provide a means for the RFM to accurately _estimate_ its performance on a task it has not yet been evaluated for. In other words, RFMs should be intentionally designed to behave predictably on new tasks, either by exhibiting similar performance to that demonstrated in previous related tasks or by giving users a way to visualize or forecast their behavior. Together, these findings motivate a shift toward user-centered, interpretable evaluations and deployments of RFM based robots. 

## **2 Related Works** 

In this work, an RFM refers to a general-purpose model or algorithm which can be deployed on a robot enabling it to perform a wide range of physical manipulation tasks as specified by a user. RFMs often manifest as “generalist policies” or “vision language action models (VLAs)”, and are gaining popularity as a way to distill large amounts of data from a wide range of tasks into a single model; RFMs, such as RT-2 [Brohan et al., 2023] and OpenVLA [Kim et al., 2024], are end-to-end policies that take language instructions or goal images along with camera observations as input, and output 

actions, usually in end-effector space. Like LLM model scaling [Zhao et al., 2024], more diverse data and larger models tend to improve an RFMs performance and generalization capabilities. The success of RFMs has also coincided with the advancement of data-efficient and lower cost imitation learning methods [Chi et al., 2024; Zhao et al., 2023; Team et al., 2024] and smaller-scale but effective multi-task learning techniques [Shridhar et al., 2023; Wang et al., 2024a; Reuss et al., 2024; Haldar et al., 2024]. Given that these models are still in their early days, there is still relatively little work on how to best holistically evaluate them. 

RFMs are typically evaluated with TSR across a variety of different tasks: typically short-horizon pick-and-place tasks conducted with robot arms. Although many RFMs are evaluated on real robots, recent advances have also enabled highfidelity simulation evaluations [Liu et al., 2024]. TSR is useful for enabling direct comparisons of different RFMs on the same tasks; however, it is not the only means of evaluating these models and is often overemphasized in evaluation. For example, some works also discuss _failure cases_ for tasks. Despite the impressive capabilities of RFMs, they are still very prone to failing; though less commonly reported, how they fail can be useful information for researchers [Liu et al., 2023; Duan et al., 2024] and potentially novice users alike. Recent work by Wang et al. [2024b; 2024c] proposes benchmarks for evaluating RFMs in simulation wherein tasks are broken down into sub-tasks and TSR is reported for each (e.g. a pick-andplace task requires the robot to move to the correct object and successfully grasp it before moving it to a different location). Estimating TSR and if/how a robot will fail is also an active area of research [Goko et al., 2024; Diehl and Ramirez-Amaro, 2023]. Despite this progress, the performance of RFMs has yet to be evaluated and studied with novices, to the best of our knowledge. 

In the field of human-robot interaction (HRI), it is well studied and understood that users who are informed about a robot and its capabilities improve their ability to collaborate with, teach, and appropriately trust a robot [Stubbs et al., 2007; Pandya et al., 2024; Iucci et al., 2021; Moorman et al., 2023]. Failure can significantly impact a user’s trust in a robot and how it impacts that person can vary depending on both the nature of the task and the user [Khavas, 2021]. Specific types of robot failures and their severity can alter how a user interacts with a robot, for example by influencing their chosen method of teaching it [Huang et al., 2024]. TSR, on the other hand, can be interpreted as reflecting the probability of task success. People’s interpretation of probabilities can vary greatly depending on how those probabilities are presented [Oudhoff and Timmermans, 2015; Chater and Oaksford, 2008]. Attending to communication of risk and probabilities is well-studied in the high-stakes healthcare domain, where it is critical to ensure patients can make informed decisions and has consequently been widely studied [Ancker et al., 2025; Johnson and Slovic, 1995]; these same principles apply to the high-stakes robotics domain, wherein people share physical space with robots. Thus, it is crucial that we investigate the gap between how non-experts understand and the way experts understand and use TSR. 

## **3 Methodology: Defining information types** 

To identify how non-experts interpret and use performance information, we designed an online study where participants were presented with real RFM evaluation data, asked to evaluate a robot’s capabilities and to brainstorm what information types would be useful when using such a robot. We then conducted an in-person study to corroborate these findings with embodiment. Here we describe the four information types we studied. These types are drawn from the commonly reported “task success rate” and “failure case” information types found in RFM evaluations. Each is presented with an example from the study using the task request “Move the green bottle of tea to the refrigerator door” as reference. 

**Estimated Task Success Rate (ETSR)** This refers to a robot’s internal estimate of how likely it is to perform a requested task successfully. This functionality is likely crucial for robots to be deployed safely. Estimating a robot’s ability to perform a given task is an ongoing area of research. _E.g.: “The robot estimates it can successfully complete the task 1/5 times, or 20% of the time.”_ 

**Estimated Failure Case (EFC)** This refers to a robot’s estimate of how it may fail when performing a task. Similar to ETSR, this type of functionality has both safety and usability implications. We focus on EFC as a natural language description (vs. a failure example shown in a simulator). Furthermore, we treat this estimate as the most likely failure case. This may not be the only useful failure case; a “worst case” failure scenario, for example, may also be important to users. We choose to present EFC to participants in the framing as the “most likely failure case,” as such cases are often discussed in research. _E.g.: “The robot estimates that it may fail by attempting to pick up an object that is not the green tea.”_ 

**Related Task - Task Success Rate (RT-TSR)** This refers to previously collected task data from an RFM and its resulting TSR. RT-TSR is TSR data from a task that is “similar” to the user’s requested task. Similarity can mean different things and be measured in different ways (see Section III, B for how we measure it in this study). Unlike ETSR, RT-TSR is derived from real roll-outs of the RFM and users may value it differently than a robot’s internal estimate. RT-TSR can also be derived from RFM deployments in different robots and environments. Although the performance of an RFM on one task may not always be indicative of how it performs on another, RT-TSR provides a grounded data point for understanding an RFM’s capabilities. _E.g.: “The robot has previously succeeded in this similar task 4/5 times, or 80% of the time.”_ 

**Related Task - Failure Case (RT-FC)** This refers to real failure cases that occurred in similar robot tasks. Like EFC, we focus on the case of a verbal description of the most likely failure for that task. RT-FC can be useful for gauging how an RFM may be prone fail. For example, in a pick-and-place task, an RFM failing to identify the right object to pick may indicate something different than an RFM failing to grasp the requested object. _E.g.: “The robot has previously failed this similar task by grasping the can but then halting, failing to put it in the refrigerator.”_ 

> * We thank the authors of this work for generously providing us with the evaluation data and videos upon our request. 

|**Model**|**Robots Used**|**Tasks**|
|---|---|---|
|OpenVLA<br>[Kim et al., 2024] <sup>*</sup>|WidowX,<br>Franka Emika Panda|Remove battery from sink;<br>Move salt shaker onto plate;<br>Move eggplant from sink to pot;<br>Move carrot from sink to plate;<br>Stack cups|
|||Remove can from refrigerator;<br>Close oven door; Lift lid off pan;|
|Baku<br>[Haldar et al., 2024]|Ufactory xArm|Lift orange out of bowl;<br>Put coke can in basket;<br>Wipe cutting board;<br>Move tea bottle to refrigerator|
|Multimodal||Move banana from stove to sink;|
|Diffusion<br>Transformer (MDT)|Franka Emika Panda|Move banana from sink to stove;<br>Move pot from sink to stove;|
|[Reuss et al.,2024]<sup>*</sup>||Push toaster lever down|


Table 1: Models, robots, and tasks shown to users. 

## **4 User Experience with Different Information Types (online study)** 

### **4.1 Procedure** 

**Task Data Collection and Coding** We collected real RFM data through surveying RFM literature and through collaborations with authors of RFM and multi-task robot learning works. We collected task data that contained: TSR as collected from an RFM evaluation, including the number of total trials; a video of the robot successfully performing a task; and a video of the robot failing a task if the task success rate was below 100% _._ This resulted in 16 tasks from three evaluations (see Table 1). All participant-facing material used in the study was from robot evaluations in published works. The data used for ETSR and EFC _was real data_ , but was framed as estimates to participants. This ensured that ETSR and EFC were accurate and could be presented without developing an estimator. The mean TSR was approximately 66% (SD _≈_ 23%). 

The study required pairs of similar tasks to present RT-TSR and RT-FC. We tested several methods for encoding task similarity, such as the distance of task descriptions in language embedding space and querying LLMs. Of the methods, qualitative coding [Auerbach and Silverstein, 2003] was the most consistent. We had three members of our lab, each of whom was unaware of the study’s content, independently label the most similar task for all 16 tasks. Similarity was based on the “robot skills” required to complete each task given a task description and the failure and success videos. Disagreements were resolved through discussion. We wrote descriptions of the failure cases in the videos, which were independently checked by two researchers for accuracy and objectivity. We intentionally avoided any speculation as to the cause of the failure, but rather attempted to just describe what physically took place. See the appendix for the failure descriptions, task similarity coding results, and a complete list of all TSRs. 

**Study Design** The within-subjects study had users report on their perception of a robot’s ability to perform a task given different information types (Figure 2). We generated 16 information-task pairs for each participant. The information types were presented in all 16 permutations, including the case of no information, and randomly paired with the tasks. As RT-TSR and RT-FC could contain information about a task the user is yet to see, some participants saw information about a task before being presented with that task. To mitigate this and other potential ordering effects, we counterbalanced the information permutations using Latin square methodology. After 


Figure 2: Overview of the study procedure. Users saw a successful or failed trajectory based on a probabilistic sample from the real evaluation success rate for that task. For each participant, the 16 information combinations where paired with the 16 tasks. participants provided informed consent, they were told that **4.2 Results** they would be making judgments about “whether or not you We recruited 112 participants from Prolific; 11 were excluded want a robot to perform a task in your home.” Each informafor not completing the study or consistently failing maniption type was explained and an example task was shown. Then, ulation checks. Common demographic information of inusers filled out a background survey that asked for information cluded participants can be found in the appendix. For stasuch as age, occupation, and level of robot experience; and tistical analysis, we used parametric methods, including RMincluded the Personal Level Positive Attitude and Negative ANOVA where the presence or absence of an information type Attitude sub-scales of the General Attitudes Towards Robots is treated as a repeated measure (resulting in 16 levels), and Scale (GAToRS) survey [Koverola et al., 2022]. non-parametric methods including the Wilcoxon singed-rank 

We recruited 112 participants from Prolific; 11 were excluded for not completing the study or consistently failing manipulation checks. Common demographic information of included participants can be found in the appendix. For statistical analysis, we used parametric methods, including RMANOVA where the presence or absence of an information type is treated as a repeated measure (resulting in 16 levels), and non-parametric methods including the Wilcoxon singed-rank test. Despite likert-item data being non-parametric, we used an RM-ANOVA specifically to account for potential interaction effects between the different information types. We use parametric tests when directly comparing the different information types. We used Bayesian tests [van Doorn et al., 2021] for tests other than RM-ANOVA due to computate limitations. 

For each task, participants were shown a task request (e.g., “move the can of soup to the refrigerator”), a still image of the robot before execution, and an information box with the provided information. They then answered 5-point Likert questions about their perceptions of the robot, predictions of its behavior, and whether the information was sufficient to assess task performance; participants also reported the ETSR from the information box as a manipulation check. Following these questions, they were shown a video of the robot performing the task. Whether a success or failure was shown was determined by sampling the actual TSR from the collected data as to realistically reflect interactions with the model. Then, they were asked questions about their level of surprise and to reflect on the sufficiency of the provided information. They were also asked to judge if the task was completed successfully. The videos were slowed towards the end so it was easier to visualize the effects of the robot’s actions; the video could also be rewound at any time. Before seeing the 16 tasks, users responded to questions in a practice task and the data from this practice was discarded. After seeing all tasks, they completed a post-study questionnaire. 

**Quantitative** To investigate the impact of each information type on user perceptions and responses, we developed three hypotheses to test: 

- **H1** is that participants’ perception of having sufficient information to assess the robot will improve with each additional information type, both before and after the robot attempts the task. This hypothesis is motivated by prior research in HRI related to trust that demonstrate that users want information and explanations about a robot’s behavior, especially regarding failure [Wachowiak et al., 2024; Das et al., 2021; Riveiro and Thill, 2022]. 

- **H2** is that participants will report greater comfort with the robot performing the task as more information is available. This hypothesis is grounded in prior research that has shown transparency may increase trust and comfort in interaction, especially when related to safety [Akalin et al., 2022; Fischer et al., 2018]. 

The study questions, fully listed in the appendix, explore how information types influence user perceptions of a robot’s capabilities and willingness to use it. They were developed by partially following recommendations from [Schrum et al., 2020] for developing Likert questionnaires for HRI (e.g. a 5- point scale was intentionally chosen to mitigate fatigue due to the repetitiveness of the study). Participants were compensated $9.07 for the _∼_ 34 minute study. This procedure was approved by the Tufts University Institutional Review Board (IRB). 

- **H3** is that participants will find all information types useful, with ETSR being considered the most useful and equality among others. This hypothesis is more exploratory but central to understanding what information types should be made available to users. We expect ETSR to be reported as most useful since it is directly connected to whether the robot fails or succeeds in a binary sense. 

To analyze H1, we used two Likert questions that attempted 


Figure 3: Responses to the pre-task and post-task Likert questions of information sufficiency under different conditions. p-values and _ηp_<sup>2effect</sup> sizes from an RM-ANOVA are shown. _Legend_ : Strongly Disagree/1, Disagree/2, Neutral/3, Agree/4, Strongly Agree/5 

to measure the perceived sufficiency of each information type, where higher values indicate greater sufficiency: “I have enough information to assess the robot’s ability to perform this task” (asked before the robot attempted the task), and “I received sufficient information to predict this outcome” (asked after the task attempt). With an RM-ANOVA, we find that the presence of each information type significantly increases the user’s reported perceived information sufficiency. We find noticeably larger effect sizes in the presence or absence of success rates than in failure cases. The distribution of responses and with p-values with effect sizes are shown in Figure 3. We found a positive correlation between people’s reported info sufficiency and the amount of info that they were presented with (i.e. 0-4 info types): _r_ = _._ 265 _, p < ._ 001, _BF >_ 1000. These findings support **H1** . 

However, they do not support the latter part, as ETSR was not significantly more useful than all other types. 

Finally, although participants were not asked to make an explicit binary success/failure prediction, we treated responses to the pre-task statement “I am confident the robot will be able to successfully perform this task” as a proxy. “Agree” or “strongly agree” responses were coded as success predictions, and all others as failure. Prior work shows that change from Likert-scale responses to binary yields similar positive/negative patterns to binary-choice questions [SuárezGarcía et al., 2024; Dolnicar and Grün, 2007]. We conducted four independent-samples t-tests with information presence as the grouping variable and prediction accuracy as the dependent variable. Only ETSR significantly improved prediction accuracy ( _p < ._ 001 _, BF >_ 1000), with users correctly predicting outcomes 61.9% of the time. While this does not capture nuanced expectations about robot behavior, it indicates that ETSR was most informative for binary success prediction. 

For **H2** , we consider two pre-execution Likert questions: “I would feel comfortable with this robot performing this task in my own home” and “I trust the robot to do the task on its own.” Both questions relate to the user willingness to let the robot attempt the task. The amount of information present was a weak predictor of comfort for the “home” and “trust” questions (via a correlation analysis, _R_<sup>2</sup> = _._ 008, _F_ = 13 _._ 107, _p < ._ 001, _BF_ = 35 _._ 86 and _R_<sup>2</sup> = _._ 011, _F_ = 17 _._ 439, _p < ._ 001, _BF_ = 309 _._ 22 respectively). An RM-ANOVA of ETSR and RT-TSR shows that if the robot has a high ETSR and a high RT-TSR, user comfort increases ( _p < ._ 001 for all cases). In contrast, neither EFC nor RT-FC increased reported user comfort for either question. We also intuitively find the higher success rate, the higher reported comfort for the “home” and “trust” questions ( _R_<sup>2</sup> = _._ 26, _F_ = 32 _._ 460, _p < ._ 001, _BF >_ 1000 and _R_<sup>2</sup> = _._ 26, _F_ = 32 _._ 434, _p < ._ 001, _BF >_ 1000 respectively). These results partially support **H2** , with TSR leading to greater reported comfort. 

**Qualitative** To understand how users interpreted the different information types and what other information they may want, we asked two open-response questions in the post-study questionnaire: “How did you use each information type to make your decisions? What made certain information more useful than other information?” and “What other information types may be useful to you to decide when a robot can or cannot reliably perform a task?” The purpose of the latter question was to investigate both what users want and to identify potential gaps in user-wants and what is reported in RFM research. For analysis, we employed thematic inductive coding [Ryan and Bernard, 2003; Vanover et al., 2021]. For each question, a researcher came up with themes, codes within those themes, and a codebook with descriptions for each code. Two researchers then independently labeled each response with up to five codes with spreadsheet annotation. Disagreements were resolved through discussion. The final codebooks and code counts can be found in the appendix. 

Subjective post-study user assessments of the utility of each information type are given in Figure 5. A large majority agreed or strongly agreed that all information types are useful (ETSR: 79%, EFC: 63%, RT-TSR: 84%, RT-FC: 71%). A Wilcoxon signed-rank test showed that ETSR was reported as more useful than EFC ( _p < ._ 001 _, BF_ = 331 _._ 52) and that RTTSR was more useful than RT-FC ( _p_ = _._ 004 _, BF_ = 12 _._ 46). These results support the first half of **H3** , that users find all information types useful when evaluating robot performance. 

**Information Usage** From the responses to the information usage question, three themes emerged: preference, trust, and strategy. From those themes we developed 14 codes in total. We found a wide variety in user preferences for information types, with a divide between those who preferred real data and those who preferred estimates, although many participants 

relied on both types. 31 responses were tagged with the _preferred real data_ code and 30 tagged with _preferred estimates_ . Participants were also divided on whether they trusted estimates (18 explicitly reported to _trust estimates_ while 11 were _skeptical of estimates_ ). Those who were skeptical typically also indicated that they preferred real data to make decisions: **P. 45** , said real-data provides “tangible evidence of its reliability” and **P. 80** , said real-data is “crucial because it provides real-world evidence of the robot’s capabilities and potential failures.” In contrast, users who preferred estimates both mentioned trusting them and appreciated that “it was a direct factor on whether or not the robot would accomplish the task.” 

People often had specific strategies for using the information. _Ordered preference_ was tagged 20 times: users explicitly mentioned a ranking or process for using some information to support another. **P. 83** said, “I used success estimates to gauge the robot’s reliability and past performance to assess trustworthiness.” Five of these participants mentioned using thresholds: **P. 8** noted that an ETSR “below 70% felt iffy [unreliable],” and that RT-TSR “helped me with my confidence in the absence of a success rate for the main task itself.” Nineteen participants mentioned that their ability to use real-data depended on how similar the tasks were. **P. 48** for instance explained their usage of real-data “would depend on how similar it was to the actual task; if it was not that similar then I would disregard the information and just use my gut.” Overall, these responses highlight diverse user strategies and preferences and underscore the importance of quantifying task similarity in RFMs as an indicator of performance on new tasks. 

**Participant Suggestions for Additional Information Types** We asked what other information would be useful when determining robot reliability. From the responses we derived seven themes: Robustness, Robot Capability, Learning, Failure, Task, and Miscellaneous. Within those themes we developed 18 codes in total. The most common request was for _more information_ like the information types already available, such as more estimated failure cases or more information about related tasks (38 participants). This is consistent with the quantitative analysis of the presence of each information type being useful. However, users also expressed diverse and rich desires about what other information they may want. 

_Robot capability_ was the second most common information type requested. Participant expressed a desire to know about the robot’s physical specifications, such as the “robot’s strength and dexterity” or its sensing capabilities, such as “color identification and motion detection.” Similarly, 8 participants mentioned that they wanted to know about _speed_ or how fast the robot could perform the task. Despite EFC and RT-FC being rated as less useful than their TSR counter part, many users identified other aspects of failure as important (the code _failure rate and case_ was tagged 23 times, the code _failure degree_ tagged 7, and the code _failure recovery_ tagged 5 times). _Environment factors_ and comments about robustness were also frequently mentioned. **P. 43** provided a detailed response that captured well the _environment factors, robustness to environment,_ and _robustness to task_ codes: “It would be helpful to know more about the robot’s past experiences with similar tasks in different environments or settings, as well as its ability to adapt to new challenges. Also, understanding how the robot 


Figure 4: The in-person study was conducted in a University building lobby. The robot repeatedly attempted to put the cans on the shelf. 

handles unexpected obstacles or changes in the task would give a better idea of its reliability.” 

The need for information about the robot’s algorithm and real performance was also present, albeit less focused and with less consensus than topics such as robot capability. Intuitively, people wanted real success rate or failure cases on the requested task (13 participants), or wanted to watch the robot repeatedly attempt the task (8 participants). 31 participants wanted to know more about the nature of the task itself or “thought about how easy or difficult it would be for the robot to perform the task.” Some wanted information about the robot’s ability to learn. **P. 65** for example said “understanding how the robot learns from past mistakes would help me trust it more.” 

## **5 Exploring User Information Needs with an Embodied Robot (in-person study)** 

In the online study, we identified user information preferences and needs with a variety of tasks and real evaluation data. In this in-person study, we sought to identify the effect of embodiment: checking for differences in the information types users perceived as valuable in-person compared to their preferences when evaluating videos and exploring what new information types they may want. Watching a robot perform a task in real-time offers the benefit of seeing how its behavior affects the environment, and may change the users’ assessment of the robot from embodiment alone [Seo et al., 2015]. 

### **5.1 Procedure** 

The study was conducted using a Kinova Gen3 Lite robot in a University building lobby. To maintain similarity with the tasks from the online study, we designed a kitchen choreinspired task in which the robot had to place cans of soup on a shelf. To enable the robot to autonomously complete and demonstrate the task, we trained the robot with Diffusion Policy (DP) [Chi et al., 2024] using an implementation from LeRobot [Cadene et al., 2024] and further adapted to ROS [Stanford Artificial Intelligence Laboratory et al., 2018]. While DP is not a RFM, it is nevertheless a start-of-the-art imitation learning algorithm often used as a baseline for RFMs 


Figure 5: Users in the online study generally reported each information type as useful. 

and was feasible to train and run inference locally using a NVIDIA RTX-3080 (current work is trending towards making RFMs more affordable to use [Wen et al., 2024; Belkhale and Sadigh, 2024]). The policy completed the task most of the time but would also fail regularly: by failing to grasp the can (hovering over it or pushing its gripper into it), pushing the can into the shelf itself instead of placing it, or dropping the can onto the table. Participants observed the robot repeatedly attempting the task, with a researcher resetting the environment after each run. The robot served as an example for answering questions. Participants were recruited from passersby and with posters. After providing consent, they were given a questionnaire which described the task that the robot was doing, an information box that explained each information type, and provided examples of each type for the robot’s can-clean-up task. Users were asked to think about how the provided information may be helpful or not when deciding whether a robot is capable enough to perform tasks in a home. 

Like the online study, they were asked a Likert question for indicating how useful each information type is for determining whether one would want to use the robot. We also asked two open-ended questions: “What other information types may be useful to you to decide when a robot can or cannot reliably perform a task?” (also in the online study); and “How would you decide whether or not the robot was good enough at a task to want [to use] one?” Finally, they offered a variety of snacks as compensation. The study took five to ten minutes to complete and was approved by the Tufts University IRB. 

### **5.2 Results** 

**Participants** In total, 14 people participated in the study. 

**Quantitative** The Likert response data can be found in Figure 6. Like in the online study, a large majority of users reported all information types as being useful. Unlike in the online study, we did not find any significant differences between information types. 

**Qualitative** To analyze the open-ended questions about other information types, we used the same codebook developed from the online study. Users had similar preferences as the online study about what information they would find useful. While only 2 participants wanted more information, _robot capability_ was the most frequently tagged code. Multiple participants brought up things like space utilization and workspace, which were not brought up in the online study. **P. A12** for example said “At what speed can tasks be performed? (e.g. tx/min) Cost of automation? space utilization, safety, types of products.” And **P. A10** wrote “How much installation the robot would require or how much space it takes up. Also how long it takes to perform the task.” Concerns about failures 


Figure 6: Users in the follow-up study widely reported each information type as useful. 

were also more personal or pronounced. **P. A4** wanted to know if “In the case of failure will it damage anything or anyone,” and **P. A5** expressed concern “if it drops it [the soup can] on my ceramic tile floor and doing damage.” Responses to the second open response question generally reported wanting a highly capable and safe robot, with three participants specifying the robot should be roughly as capable as a human at the task. These results corroborate many of the findings from the online study, and provide insights into the information needs of users who are physically co-present with the robot. 

## **6 Discussion** 

**Limitations and Future Work** This study has several limitations regarding design and generalizability. Most tasks involved a stand-alone robot arm and kitchen-inspired chores; while common in RFM evaluation, these settings may not generalize to other embodiments (e.g., quadrupeds) or task types (e.g., safety-critical tasks). Nonetheless, we expect many findings to transfer across morphologies, even if absolute trust and comfort levels shift [Kunold et al., 2023], as users may value similar information types. Performance information was presented only as text, leaving the effects of alternative presentations on user expectations and decision-making as future work. Finally, while we designed the study to isolate the effects of performance information, future work should examine its role in collaborative settings, such as how users decide whether to teach a robot or allocate tasks. 

**Generalization to other Robot Models** A key contribution of this work is not only the behavior of the RFM models but also the use of representative RFM research tasks and success criteria. This work serves to inform RFM evaluations and deployments. However, given that the task videos were pre-recorded and users were not explicitly told or given information that the robot’s where using an RFM, the results from the study should equally apply to non-RFM-based robot systems, for example robots trained with single-task imitation learning. Future work should study and evaluate RFMs when the user can freely request an arbitrary, novel-task task and interact in real time with a robot. 

**Implications for Future RFM Research** Our results show that people generally interpret TSR as intended: higher TSR increases confidence that a robot will succeed. However, TSR alone is insufficient for informing users about performance on novel tasks. We therefore recommend that RFM evaluations routinely report failure cases, including both worst-case and common failures, as this information benefits novices and experts alike. While some metrics (e.g., task speed) are easy to report, others are harder to formalize; for example, robustness to static environments can be partially evaluated in 

simulation [Wang et al., 2025], robustness to dynamic interference remain difficult to quantify. Our findings also underscore the importance of both real data and estimates: real data require principled measures of task similarity, and novel tasks require reliable performance estimation. Recent work has expanded simulation-based RFM evaluation to include behavioral metrics, such as motion smoothness, and improved failure detection [Wang et al., 2025; Xu et al., 2025]. As expert evaluations grow more holistic, our results highlight the need for this information to be made available to end-users. 

Future work is needed to understand how people use TSR to wholistically predict robot behavior, as user expectations may not align with actual behavior even when accurate metrics are provided. Although TSR strongly correlates with trust and confidence, it remains unclear if users are well calibrated to a robot’s true performance over time, particularly for tasks performed repeatedly. As people gain experience with a robot performing a certain task, the value of certain information may change. In the online study, when participants reported the highest confidence in the robot’s ability to successfully perform the task, the average ETSR was only _∼_ 76%, suggesting a potential miscalibration between a user’s estimate of success likelihood and TSRs [Xu et al., 2025]. Like other robotic systems [Das et al., 2021], RFMs must explain failures in ways that avoid over- or under-trust. 

## **7 Conclusion** 

RFMs have the potential to enable robots to perform a wide range of tasks for users, especially in home environments. Through user studies, this work begins to address the critical need to understand how end users interpret performance information about these models. Based on our findings, we further provided recommendations to make future RFM evaluations and RFM deployments more user-friendly and interpretable. 

## **References** 

- N. Akalin, A. Kristoffersson, and A. Loutfi. Do you feel safe with your robot? Factors influencing perceived safety in human-robot interaction based on subjective and objective measures. _International Journal of Human-Computer Studies_ , 158:102744, Feb. 2022. doi: 10.1016/j.ijhcs.2021. 102744. 

- J. S. Ancker, N. C. Benda, M. M. Sharma, S. B. Johnson, M. Demetres, D. Delgado, and B. J. Zikmund-Fisher. Scope, Methods, and Overview Findings for the Making Numbers Meaningful Evidence Review of Communicating Probabilities in Health: A Systematic Review. _MDM Policy & Practice_ , 10(1):23814683241255334, Jan. 2025. doi: 10.1177/23814683241255334. 

- C. Auerbach and L. B. Silverstein. _Qualitative Data: An Introduction to Coding and Analysis_ . NYU Press, Sept. 2003. ISBN 978-0-8147-0695-4. 

- S. Belkhale and D. Sadigh. MiniVLA: A Better VLA with a Smaller Footprint, 2024. 

- A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, X. Chen, K. Choromanski, T. Ding, D. Driess, A. Dubey, C. Finn, 

- P. Florence, C. Fu, M. G. Arenas, K. Gopalakrishnan, K. Han, K. Hausman, A. Herzog, J. Hsu, B. Ichter, A. Irpan, N. Joshi, R. Julian, D. Kalashnikov, Y. Kuang, I. Leal, L. Lee, T.-W. E. Lee, S. Levine, Y. Lu, H. Michalewski, I. Mordatch, K. Pertsch, K. Rao, K. Reymann, M. Ryoo, G. Salazar, P. Sanketi, P. Sermanet, J. Singh, A. Singh, R. Soricut, H. Tran, V. Vanhoucke, Q. Vuong, A. Wahid, S. Welker, P. Wohlhart, J. Wu, F. Xia, T. Xiao, P. Xu, S. Xu, T. Yu, and B. Zitkovich. RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control, July 2023. URL http://arxiv.org/abs/2307.15818. arXiv:2307.15818 [cs]. 

- R. Cadene, S. Alibert, A. Soare, Q. Gallouedec, A. Zouitine, and T. Wolf. LeRobot: State-of-the-art Machine Learning for Real-World Robotics in Pytorch, 2024. 

- N. Chater and M. Oaksford. _The Probabilistic Mind:Prospects for Bayesian cognitive science_ . Oxford University Press, Mar. 2008. ISBN 978-0-19-921609-3. doi: 10.1093/acprof: oso/9780199216093.001.0001. 

- C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song. Diffusion Policy: Visuomotor Policy Learning via Action Diffusion, Mar. 2024. 

- D. Das, S. Banerjee, and S. Chernova. Explainable AI for Robot Failures: Generating Explanations that Improve User Assistance in Fault Recovery. In _Proceedings of the 2021 ACM/IEEE International Conference on Human-Robot Interaction_ , HRI ’21, pages 351–360, New York, NY, USA, Mar. 2021. Association for Computing Machinery. ISBN 978-1-4503-8289-2. doi: 10.1145/3434073.3444657. 

- M. Diehl and K. Ramirez-Amaro. A causal-based approach to explain, predict and prevent failures in robotic tasks. _Robotics and Autonomous Systems_ , 162:104376, Apr. 2023. doi: 10.1016/j.robot.2023.104376. 

- S. Dolnicar and B. Grün. How constrained a response: A comparison of binary, ordinal and metric answer formats. _Journal of Retailing and Consumer Services_ , 14(2):108– 122, Mar. 2007. doi: 10.1016/j.jretconser.2006.09.006. 

- J. Duan, W. Pumacay, N. Kumar, Y. R. Wang, S. Tian, W. Yuan, R. Krishna, D. Fox, A. Mandlekar, and Y. Guo. AHA: A Vision-Language-Model for Detecting and Reasoning Over Failures in Robotic Manipulation, Oct. 2024. 

- K. Fischer, H. M. Weigelin, and L. Bodenhagen. Increasing trust in human–robot medical interactions: effects of transparency and adaptability. _Paladyn, Journal of Behavioral Robotics_ , 9(1):95–109, June 2018. doi: 10.1515/ pjbr-2018-0007. 

- M. Goko, M. Kambara, D. Saito, S. Otsuki, and K. Sugiura. Task Success Prediction for Open-Vocabulary Manipulation Based on Multi-Level Aligned Representations. Sept. 2024. 

- S. Haldar, Z. Peng, and L. Pinto. BAKU: An Efficient Transformer for Multi-Task Policy Learning. Nov. 2024. 

- J. Huang, I. Sheidlower, R. M. Aronson, and E. S. Short. On the effect of robot errors on human teaching dynamics. In _Proceedings of the 12th International Conference on Human-Agent Interaction_ , HAI ’24, page 150–159, New 

York, NY, USA, 2024. Association for Computing Machinery. doi: 10.1145/3687272.3688320. 

- A. Iucci, A. Hata, A. Terra, R. Inam, and I. Leite. Explainable Reinforcement Learning for Human-Robot Collaboration. In _2021 20th International Conference on Advanced Robotics (ICAR)_ , pages 927–934, Dec. 2021. doi: 10.1109/ICAR53236.2021.9659472. 

- B. B. Johnson and P. Slovic. Presenting Uncertainty in Health Risk Assessment: Initial Studies of Its Effects on Risk Perception and Trust. _Risk Analysis_ , 15(4):485–494, 1995. doi: 10.1111/j.1539-6924.1995.tb00341.x. 

- Z. R. Khavas. A Review on Trust in Human-Robot Interaction, May 2021. 

- M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, and C. Finn. OpenVLA: An Open-Source VisionLanguage-Action Model, Sept. 2024. 

- M. Koverola, A. Kunnari, J. Sundvall, and M. Laakasuo. General Attitudes Towards Robots Scale (GAToRS): A New Instrument for Social Surveys. _International Journal of Social Robotics_ , 14(7):1559–1581, Sept. 2022. doi: 10.1007/s12369-022-00880-3. 

- L. Kunold, N. Bock, and A. Rosenthal-von der Pütten. Not All Robots are Evaluated Equally: The Impact of Morphological Features on Robots’ Assessment through Capability Attributions. _J. Hum.-Robot Interact._ , 12(1):3:1–3:31, Feb. 2023. doi: 10.1145/3549532. 

- B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone. LIBERO: benchmarking knowledge transfer for lifelong robot learning. In _Proceedings of the 37th International Conference on Neural Information Processing Systems_ , NIPS ’23, pages 44776–44791, Red Hook, NY, USA, May 2024. Curran Associates Inc. 

- Z. Liu, A. Bahety, and S. Song. REFLECT: Summarizing Robot Experiences for Failure Explanation and Correction. Aug. 2023. 

- N. M. Moorman, N. Gopalan, A. Singh, E. Botti, M. Schrum, C. Yang, L. Seelam, and M. Gombolay. Investigating the Impact of Experience on a User’s Ability to Perform Hierarchical Abstraction. In _Proceedings of Robotics: Science and Systems_ , Daegu, Republic of Korea, July 2023. doi: 10.15607/RSS.2023.XIX.004. 

- J. P. Oudhoff and D. R. M. Timmermans. The Effect of Different Graphical and Numerical Likelihood Formats on Perception of Likelihood and Choice. _Medical Decision Making_ , 35(4):487–500, May 2015. doi: 10.1177/ 0272989X15576487. 

- R. Pandya, M. Zhao, C. Liu, R. Simmons, and H. Admoni. Multi-Agent Strategy Explanations for Human-Robot Collaboration. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 17351–17357, May 2024. doi: 10.1109/ICRA57147.2024.10610720. 

- M. Reuss, O. E. Yagmurlu, F. Wenzel, and R. Lioutikov. Multimodal Diffusion Transformer: Learning Versatile Behavior from Multimodal Goals. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, July 2024. doi: 10.15607/RSS.2024.XX.121. 

- M. Riveiro and S. Thill. The challenges of providing explanations of AI systems when they do not behave like users expect. In _Proceedings of the 30th ACM Conference on User Modeling, Adaptation and Personalization_ , UMAP ’22, pages 110–120, New York, NY, USA, July 2022. Association for Computing Machinery. doi: 10.1145/3503252.3531306. 

- G. W. Ryan and H. R. Bernard. Techniques to Identify Themes. _Field Methods_ , 15(1):85–109, Feb. 2003. doi: 10.1177/ 1525822X02239569. 

- M. L. Schrum, M. Johnson, M. Ghuy, and M. C. Gombolay. Four Years in Review: Statistical Practices of Likert Scales in Human-Robot Interaction Studies. In _Companion of the 2020 ACM/IEEE International Conference on Human-Robot Interaction_ , pages 43–52, Cambridge United Kingdom, Mar. 2020. ACM. ISBN 978-1-4503-7057-8. doi: 10.1145/3371382.3380739. 

- S. H. Seo, D. Geiskkovitch, M. Nakane, C. King, and J. E. Young. Poor Thing! Would You Feel Sorry for a Simulated Robot? A comparison of empathy toward a physical and a simulated robot. In _Proceedings of the Tenth Annual ACM/IEEE International Conference on Human-Robot Interaction_ , HRI ’15, pages 125–132, New York, NY, USA, Mar. 2015. Association for Computing Machinery. ISBN 978-1-4503-2883-8. doi: 10.1145/2696454.2696471. 

- M. Shridhar, L. Manuelli, and D. Fox. Perceiver-Actor: A Multi-Task Transformer for Robotic Manipulation. In _Proceedings of The 6th Conference on Robot Learning_ , pages 785–799. PMLR, Mar. 2023. 

- Stanford Artificial Intelligence Laboratory et al. Robotic Operating System, May 2018. 

- K. Stubbs, P. J. Hinds, and D. Wettergreen. Autonomy and Common Ground in Human-Robot Interaction: A Field Study. _IEEE Intelligent Systems_ , 22(2):42–50, Mar. 2007. doi: 10.1109/MIS.2007.21. 

- A. Suárez-García, M. Álvarez Hernández, E. Arce, and J. R. Ribas. Exploring the Efficacy of Binary Surveys versus Likert Scales in Assessing Student Perspectives Using Bayesian Analysis. _Applied Sciences_ , 14(10):4189, Jan. 2024. doi: 10.3390/app14104189. 

- A. . Team, J. Aldaco, T. Armstrong, R. Baruch, J. Bingham, S. Chan, K. Draper, D. Dwibedi, C. Finn, P. Florence, S. Goodrich, W. Gramlich, T. Hage, A. Herzog, J. Hoech, T. Nguyen, I. Storz, B. Tabanpour, L. Takayama, J. Tompson, A. Wahid, T. Wahrburg, S. Xu, S. Yaroshenko, K. Zakka, and T. Z. Zhao. ALOHA 2: An Enhanced Low-Cost Hardware for Bimanual Teleoperation, Feb. 2024. 

- J. van Doorn, D. van den Bergh, U. Böhm, F. Dablander, K. Derks, T. Draws, A. Etz, N. J. Evans, Q. F. Gronau, J. M. Haaf, M. Hinne, S. Kucharsky, A. Ly, M. Marsman, 

D. Matzke, A. R. K. N. Gupta, A. Sarafoglou, A. Stefan, J. G. Voelkel, and E.-J. Wagenmakers. The JASP guidelines for conducting and reporting a Bayesian analysis. _Psychonomic Bulletin & Review_ , 28(3):813–826, June 2021. doi: 10.3758/s13423-020-01798-5. 

- C. Vanover, P. Mihas, and J. Saldana. _Analyzing and Interpreting Qualitative Research: After the Interview_ . SAGE Publications, Apr. 2021. ISBN 978-1-5443-9588-3. 

- L. Wachowiak, A. Fenn, H. Kamran, A. Coles, O. Celiktutan, and G. Canal. When Do People Want an Explanation from a Robot? In _Proceedings of the 2024 ACM/IEEE International Conference on Human-Robot Interaction_ , HRI ’24, pages 752–761, New York, NY, USA, Mar. 2024. Association for Computing Machinery. doi: 10.1145/3610977.3634990. 

- Y. Wang, Y. Zhang, M. Huo, T. Tian, X. Zhang, Y. Xie, C. Xu, P. Ji, W. Zhan, M. Ding, and M. Tomizuka. Sparse Diffusion Policy: A Sparse, Reusable, and Flexible Policy for Robot Learning. Sept. 2024a. 

- Y. R. Wang, C. Ung, G. Tannert, J. Duan, J. Li, A. Le, R. Oswal, M. Grotz, W. Pumacay, Y. Deng, R. Krishna, D. Fox, and S. Srinivasa. RoboEval: Where Robotic Manipulation Meets Structured and Scalable Evaluation, July 2025. 

- Z. Wang, Z. Zhou, J. Song, Y. Huang, Z. Shu, and L. Ma. LADEV: A Language-Driven Testing and Evaluation Platform for Vision-Language-Action Models in Robotic Manipulation, Oct. 2024b. 

- Z. Wang, Z. Zhou, J. Song, Y. Huang, Z. Shu, and L. Ma. Towards Testing and Evaluating Vision-Language-Action Models for Robotic Manipulation: An Empirical Study, Sept. 2024c. 

- J. Wen, Y. Zhu, J. Li, M. Zhu, K. Wu, Z. Xu, N. Liu, R. Cheng, C. Shen, Y. Peng, F. Feng, and J. Tang. TinyVLA: Towards Fast, Data-Efficient Vision-Language-Action Models for Robotic Manipulation, Nov. 2024. 

- C. Xu, T. K. Nguyen, E. Dixon, C. Rodriguez, P. Miller, R. Lee, P. Shah, R. Ambrus, H. Nishimura, and M. Itkina. Can We Detect Failures Without Failure Data? Uncertainty-Aware Runtime Failure Detection for Imitation Learning Policies, June 2025. 

- T. Z. Zhao, V. Kumar, S. Levine, and C. Finn. Learning FineGrained Bimanual Manipulation with Low-Cost Hardware, Apr. 2023. 

- W. X. Zhao, K. Zhou, J. Li, T. Tang, X. Wang, Y. Hou, Y. Min, B. Zhang, J. Zhang, Z. Dong, Y. Du, C. Yang, Y. Chen, Z. Chen, J. Jiang, R. Ren, Y. Li, X. Tang, Z. Liu, P. Liu, J.-Y. Nie, and J.-R. Wen. A Survey of Large Language Models, Oct. 2024. 

## **A Task list** 

Here is a list of all participant facing tasks used in the study. In the study, the task description was appended to the prefix “You want the robot to.” The failure case (FC) description was appended to the prefix “The robot estimates it may fail by” for EFC and “The robot has previously failed this similar task by” for RTFC. The TSR information was appended to the prefix “The robot estimates it can successfully complete the task” for ETSR and “The robot has previously succeeded in this similar task” for RT-TSR. 

|**Task**<br>**(Model)**|**Task Image**|**Task Description**|**Task Information and Similar Task**|
|---|---|---|---|
|Stack cups<br>(OpenVLA)||Stack the blue cup face-up on<br>top of the upside down pink<br>cup.|**TSR:**4/10 times, or 40%<br>**FC**: Picking up the cup but dropping it in the<br>sink, missing the pink cup.<br>**Similar Task:** Lift pan lid|
|Put away<br>soup<br>(Baku)||Move the can of soup to the<br>refrigerator.|**TSR**:4/5 times, or 80%<br>**FC**: Grasping the can but then halting, failing<br>to put it in the refrigerator.<br>**Similar Task:** Put away bottle|
|Close oven<br>door<br>(Baku)||Close the oven door.|**TSR:**4/5 times, or 80%<br>**FC**: Not grasping the handle, leaving the<br>oven door open.<br>**Similar Task:** Make toast|
|Remove bat-<br>tery<br>(OpenVLA)||Lift and remove the battery<br>from sink.|**TSR:**7/10 times, or 70%<br>**FC**: Not grasping the battery and then pushes<br>the battery around in the sink.<br>**Similar Task:** Lift pan lid|
|Move salt<br>(OpenVLA)||Move the white salt shaker<br>onto the plate.|**TSR:**9/12 times, or 75%<br>**FC**: Trying to pick up the wrong object.<br>**Similar Task:** Put carrot on plate|
|Lift<br>orange<br>(Baku)||Lift up the orange out of the<br>bowl.|**TSR:**4/5 times, or 80%<br>**FC**: Not grasping the orange, leaving it in<br>the bowl.<br>**Similar Task:** Remove battery|
|Put<br>eggplant<br>in pot<br>(OpenVLA)||Take the eggplant out of the<br>sink and put it into the pot.|**TSR:**7/10 times, or 70%<br>**FC**: Missing the eggplant and hitting the sink<br>instead.<br>**Similar Task:** Put coke in basket|


Table 2: List of participant facing tasks used in the online study. 

|**Task**|**Task Image**|**Task Description**|**Task Information and Similar Task**|
|---|---|---|---|
|Lift pan lid<br>(Baku)||Lift up the lid of the pan off<br>the pan.|**TSR:**4/5 times, or 80%<br>**FC**: Partly grasping and then dropping the<br>pan lid handle, causing the pan to shake as<br>the lid falls back on top.<br>**Similar Task:** Remove battery|
|Move<br>banana<br>to sink<br>(MDT)||Move the banana from the<br>stove and place it into the<br>sink.|**TSR:**4/5 times, or 80%<br>**FC**: Not picking up the banana, putting noth-<br>ing into the sink.<br>**Similar Task:** Move banana to stove|
|Move<br>banana<br>to stove<br>(MDT)||Move the banana from the<br>sink to the stove.|**TSR:**4/5 times, or 80%<br>**FC**: Being unable to pick up the banana from<br>the sink at the correct location and may push<br>it’s gripper into the sink.<br>**Similar Task:** Move banana to sink|
|Move pot<br>to sink<br>(MDT)||Move the pot from the stove<br>to the sink|**TSR:**4/5 times, or 80%<br>**FC**: Being unable to grasp the pot, moving it<br>around on the stove and towards the edge.<br>**Similar Task:** Move banana to sink|
|Put away<br>coke<br>(Baku)||Pick up the coke can and put<br>it in the basket.|**TSR:**3/5 times, or 60%<br>**FC**: Dropping the coke can and missing the<br>basket, causing it to fall on the counter.<br>**Similar Task:** Put eggplant in pot|
|Put<br>carrot<br>on plate<br>(OpenVLA)||Pick up the carrot from the<br>sink and put it on the plate.|**TSR:**4/10 times, or 40%<br>**FC**: Being unable to grasp the carrot and/or<br>by knocking over the plate.<br>**Similar Task:** Move salt|
|Wipe board<br>(Baku)||Use the towel to wipe down<br>the cutting board.|**TSR:**5/5 times, or 100%<br>**FC**: Not available.<br>**Similar Task:** Make toast|
|Make toast<br>(MDT)||Push down the toaster lever<br>to make toast|**TSR:**1/5 times, or 20%<br>**FC**: Not being able to push down the lever.<br>**Similar Task:** Close oven door|
|Put away<br>bottle<br>(Baku)||Move the green bottle of tea<br>to the refrigerator door.|**TSR:**1/5 times, or 20%<br>**FC**: Attempting to pick up an object that is<br>not the green tea.<br>**Similar Task:** Put away soup|
|(example<br>task)|||**TSR:**4/5 times, or 80%<br>**FC**: Knocking over the tube.|
|Put away<br>ball<br>(TinyVLA)||Put the tennis ball in the tube.|<br>**Similar Task:** (example) Put carrot in bowl<br>**RT-TSR**: 3/10 times, or 30%<br>**RT-FC**: Beingunable to thegraspthe carrot.|


Table 3: List of participant facing tasks used in the online study (continued). 

## **B Codebooks** 

|**Theme**|**Code**|**Description**|
|---|---|---|
|Trust|Trusted estimates|Someone who explicitly indicated that they trusted the estimates or<br>thought the estimates could be relied on|
|Trust|Skeptical of estimates|Someone who expressed skepticism over if the estimates could be relied<br>on or not/their value.|
|Trust|Performance threshold|Someone who mentioned a numeric threshold or some threshold of<br>reportedperformance to where theycould make decisions about the task.|
|Strategy|All info|Mentions all the information was useful|
|Strategy|Ordered preference|Mentions how they relied one or more types of info but then also used<br>the others as backupor support|
|Strategy|Mainlyused estimated TSR|Someone who more or lessjust says theyused estimated TSR only|
|Strategy|Past performance|Someone who says they used the previous tasks or data to help them<br>decide(implies sort of meta-learningthe study)|
|Strategy|Similarity|Someone who mentions the value of the real data was based on how<br>similar the task was|
|Strategy|Risk calculation|Someone who mentions tryingto estimate failure risk|
|Strategy|Compared real and estimates|Explicitlycompares real and estimates|
|Preference|Preferred estimates|Explicitlymentions they preferred estimates|
|Preference|Preferred real data|Explicitlymentions they preferred real data|
|Preference|Preferred success rates|Explicitlymentions they preferred success rates|
|Preference|Preferred failures|Explicitlymentions they preferred failures|


Table 4: Thematic codebook developed for the responses to the post-study open-response questions: “How did you use each type of information to make your decision? What made certain information more useful than other information?” 

|**Theme**|**Code**|**Description**|
|---|---|---|
|Robot<br>capability<br>|Robot<br>capability|Wanting to know more about a robot’s general specifications, sensing<br>capabilities,or algorithmic ability.|
|Robot<br>capability|Speed|Wanting to know how fast the robot can perform the task.|
|Failure|Failure<br>degree|Wanting to know about how bad a failure could be/about the range of<br>possible failures.|
|Failure|Failure rate<br>and cases|Wanting to know about failure rate as opposed to success rate; wanting<br>to know what in the environment could be damaged or affected because<br>of the robot executingthe task;failures unrelated to the requested task.|
|Robustness|Environment<br>factors|Wanting to know more about the environment: its dynamics and how it<br>mayaffect the robot’sperformance.|
|Robustness|Robustness to<br>task|Wanting to know about how robust the robot is to minor variations in the<br>requested task.|
|Robustness|Robustness to<br>environment|Wanting to know about how robust the robot is to external or environ-<br>mental factors separate from the task.|
|Robustness|Failure<br>recovery|How capable the robot is at recovering from failures|
|Task|Task<br>difficulty|Wanting some sort of measure or assessment of task difficulty or com-<br>plexity; wanting to know something about how good the robot is relative<br>to humanperformance on the task.|
|Task|Task type|General info about the nature of the task; wanting to know the horizon<br>of the task,as in if it is a short or longtask/single stepvs multi-step.|
|Task|Performance<br>on requested<br>task|Wanting to know about how good the robot is on the actual task (not like<br>estimated success rate, but like actual performance).|
|Task|Watch<br>repeated<br>attempts|Expressing a desire to watch the robot attempt the task one or more<br>times.|
|Learning|Ability to<br>learn|Wanting to know how well the robot can adapt/learn as it executes a task<br>or attempts a task multiple times.|
|Learning|Learning<br>experience|Wanting to know how the robot was trained or how it previously learned<br>to do the task.|
|Miscellaneous|Human<br>collaboration|Wanting to know how well the robot could collaborate with a human or<br>handle a human intervention; wanting to know about the robots ability<br>to learn frompeople.|
|Miscellaneous|Satisfied|The participant does not express a desire for more information or is<br>alreadysatisfied with theprovided information.|
|Miscellaneous|More info|i<br>Expressing a desire for more of the four information types already pro-<br>vided.|
|Miscellaneous|Deployment<br>duration|Wanting to know about how long the robot has been deployed for or its<br>deployment history.|


Table 5: Thematic codebook developed for the responses to the post-study open-response question: “What other types of information may be useful to you to decide when a robot can or cannot reliably perform a task?” 

**C Code Counts** 


Figure 7: Information usage code counts from online study. 


Figure 8: Other information code counts from online study. 


Figure 9: Other information code counts from in-person study. 

## **D Common Demographic Information (Online Study)** 

|Age|Gender|Robot Experience|
|---|---|---|
|_18-24_: 16,_25-34_: 40,|Female: 54,|None: 36, Slight: 38,|
|_35-44_: 24,_45-54_: 13,|Male: 46,|Moderate: 21,|
|_55-64_: 7,_65+_: 1|Non-binary: 1|Significant: 6|


## **E List of Questions Used** 

Here is a list all of the questions asked to participants in the online and offline studies (excluding consent and background ). Questions labeled “Likert” indicate a 5-point Likert question ranging from “strongly disagree” to “strongly agree.” 

### **E.1 Online study pre-task execution questions** 

These are the questions asked to participants before seeing the robot attempt a task. Participants could see the description of the task, the task image, and the performance information presented in an information box. 

- What is the reported robot’s estimate of its success rate for this task? (manipulation check) _response options:_ 0-25%, 26-50%, 51-75%, 76-100%, Information not available 

- I am confident the robot will be able to successfully perform this task. (Likert) 

- I will be surprised if the robot fails. (Likert) 

- I would feel comfortable with this robot performing this task in my own home. (Likert) 

- I trust the robot to do the task on its own. (Likert) 

- I would spend time improving the robot before letting it attempt this task. (Likert) 

- I have enough information to assess the robot’s ability to perform this task. (Likert) 

### **E.2 Online study post-task execution questions** 

These are the questions asked to participants after seeing the robot attempt a task. Participants could still see the description of the task and performance information presented in an information box. They could also freely rewind and re-watch the task execution video. 

- The robot succeeded at the requested task. (Likert) 

- I was surprised by the robot’s behavior. (Likert) 

- I received sufficient information to predict this outcome. (Likert) 

- I would let the robot do the task again. (Likert) 

- Do you have any other comments about the task, information, or robot behavior? (optional) (open-response) 

### **E.3 Online study post-study questions** 

These are the questions asked after participants experienced all 16 robot tasks. 

- Please rank each type of information based on how useful it was. (drop-down menu ranking) 

- Estimated task success rate for a requested task is useful for determining whether or not I want to use the robot. (Likert) 

- Estimated failure cases for a requested task are useful for determining whether or not I want to use the robot. (Likert) 

- Real task success rate for a similar task is useful for determining whether or not I want to use the robot. (Likert) 

- Real task failure examples for a similar task are useful for determining whether or not I want to use the robot. (Likert) 

- How did you use each type of information to make your decision? What made certain information more useful than other information? (open-response) 

- What other types of information may be useful to you to decide when a robot can or cannot reliably perform a task? (open-response) 

### **E.4 In-Person study questions** 

- Please rank each type of information based on how useful it was. (drop-down menu ranking) 

- Estimated task success rate for a requested task is useful for determining whether or not I want to use the robot. (Likert) 

- Estimated failure cases for a requested task are useful for determining whether or not I want to use the robot. (Likert) 

- Real task success rate for a similar task is useful for determining whether or not I want to use the robot. (Likert) 

- Real task failure examples for a similar task are useful for determining whether or not I want to use the robot. (Likert) 

- What other types of information may be useful to you to decide when a robot can or cannot reliably perform a task? (open-response) 

- How would you decide whether or not the robot was good enough at a task to want one? (open-response) 

## **F Online study instructions and GUI** 

Here we share images of the web page format shown to participants throughout the study. This includes the instruction page, pages for both a pre- and post- task execution, and the page for the post-study questionnaire. 

### **F.1 Study Instruction Page** 


Figure 10: Instruction page (1/3) 


Figure 11: Instruction page (2/3) 


Figure 12: Instruction page (3/3) 

**F.2 Task Pages** 


Figure 13: Pre-task execution questionnaire. 


Figure 14: Post-task execution questionnaire. 

**F.3 Post-study questionnaire** 


Figure 15: Post-study questionnaire. 

