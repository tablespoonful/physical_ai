---
title: "NaVid: Video-based VLM Plans the Next Step for Vision-and-Language Navigation"
date: "2024"
venue: "RSS 2024"
url: https://www.roboticsproceedings.org/rss20/p079.html
pdf: https://www.roboticsproceedings.org/rss20/p079.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://www.roboticsproceedings.org/rss20/p079.pdf)** / [論文ページ](https://www.roboticsproceedings.org/rss20/p079.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Robotics: Science and Systems 2024 Delft, Netherlands, July 15-July 19, 2024** 

# NaVid: Video-based VLM Plans the Next Step for Vision-and-Language Navigation 

Jiazhao Zhang<sup>1</sup><sup>_,_2</sup><sup>_,∗_</sup> Kunyu Wang<sup>2</sup><sup>_,∗_</sup> Rongtao Xu<sup>2</sup><sup>_,_3</sup><sup>_,∗_</sup> Gengze Zhou<sup>4</sup> Yicong Hong<sup>5</sup> Xiaomeng Fang<sup>2</sup> Qi Wu<sup>4</sup> Zhizheng Zhang<sup>6</sup><sup>_,†_</sup> He Wang<sup>1</sup><sup>_,_2</sup><sup>_,_6</sup><sup>_,†_</sup> 1CFCS, School of Computer Science, Peking University 2Beijing Academy of Artificial Intelligence 3CASIA 4University of Adelaide 5Australian National University 6Galbot https://pku-epic.github.io/NaVid/ 

**_Abstract_ —Vision-and-language navigation (VLN) stands as a key research problem of Embodied AI, aiming at enabling agents to navigate in unseen environments following linguistic instructions. In this field, generalization is a long-standing challenge, either to out-of-distribution scenes or from Sim to Real. In this paper, we propose NaVid, a video-based large vision language model (VLM), to mitigate such a generalization gap. NaVid makes the first endeavor to showcase the capability of VLMs to achieve state-of-the-art level navigation performance without any maps, odometers, or depth inputs. Following human instruction, NaVid only requires an on-the-fly video stream from a monocular RGB camera equipped on the robot to output the next-step action. Our formulation mimics how humans navigate and naturally gets rid of the problems introduced by odometer noises, and the Sim2Real gaps from map or depth inputs. Moreover, our video-based approach can effectively encode the historical observations of robots as spatio-temporal contexts for decision making and instruction following. We train NaVid with 510k navigation samples collected from continuous environments, including action-planning and instruction-reasoning samples, along with 763k large-scale web data. Extensive experiments show that NaVid achieves state-of-the-art performance in simulation environments and the real world, demonstrating superior crossdataset and Sim2Real transfer. We thus believe our proposed VLM approach plans the next step for not only the navigation agents but also this research field.** 


Fig. 1: Real-world demo of our proposed video-based VLM, NaVid, for vision-and-language navigation. Given the human instruction, NaVid only takes online RGB video frames as input and outputs a language action for robotic execution. 

## I. INTRODUCTION 

As a fundamental task of Embodied AI, vision-and-language navigation (VLN) [30, 65] requires the agents to navigate in diverse and especially unseen environments following freeform linguistic instructions. VLN requires robots to understand complex and diverse visual observations and meanwhile interpret fine-grained instructions [12, 93], “ _go up the stairs and stop in the doorway_ ”, and thus maintains to be a challenging task. To address this challenging task, a large volume of research [79, 17, 98, 92, 64, 46, 3] in this field is launched in the simplified setting, _i_ . _e_ ., decision-making in discrete environments ( _e_ . _g_ ., R2R [44] in MP3D simulator [11]). Specifically, the real environments are abstracted as connectivity graphs, and the navigation is cast as the teleportation over a waypoint set on such graphs. Despite these methods are rapidly evolving and yielding impressive results [79, 114, 60, 98], the discretized environment setting introduces additional challenges 

* Joint first authors (e-mail: zhngjizh@gmail.com). _†_ Corresponding authors (e-mail: zhangzz@galbot.com, hewang@pku.edu.cn). 

such as the need for a landmark graph [43, 45] and a local model to navigate between landmarks [78, 81, 77]. 

Toward more realistic and straightforward modelling, navigation in continuous environments, _e_ . _g_ ., R2R-CE, RxR-CE, has garnered increasing attention. Considerable excellent research efforts are devoted to reducing the Sim-to-Real gaps [45, 35, 101, 8]. However, they still face severe challenges in generalization due to data scarcity and domain gaps in their model inputs including RGBD, odometer data, or maps. The generalization issue presents a critical yet under-explored challenge in large-scale real-world deployment, encompassing transitions from seen scenes to novel environments and from simulation to real worlds (Sim-to-Real). The recent prosperity of large Vision Language Models (VLMs) has shown unprecedented promises in a lot of research fields [102, 49, 2]. In this paper, we explore whether large models can do the same in propelling generalizable VLN. 

Large models have exhibited impressive generalization capacities in a broad range, covering AIGC [73, 9, 110], generalist chatbots [1], autonomous driving [27], _etc_ . They have 

also been shaping the future of embodied AI. RT-2 [10] shows the promise of transferring web knowledge from VLMs to generalizable robotic manipulation. Large Language Models (LLMs) have been effective as the planners for VLN in discrete environments [60, 64, 114, 13, 69]. The recent advancements in VLMs are ushering the VLN research into an exciting juncture. It is time to study _whether VLMs can boost the generalization of VLN in continuous real-world environments._ 

In this paper, we make the first endeavour to capitalize on the power of foundational VLMs for generalizing VLN to the real world and propose a video VLM-based navigation agent, dubbed NaVid. It solely relies on videos captured by a robot’s monocular camera and humane-issued instructions as inputs for planning the next-step action in an end-to-end manner. We put the proposed NaVid into perspective by comparing it with three categories of models. 1) Compared with AGI models [102] or so-called navigation generalists [113] that can perform coarse navigation planning, NaVid is a practical Vision-Language-Action (VLA) model that can infer executable actions with quantitative arguments, _e_ . _g_ ., moving distances, and rotation degrees. This allows NaVid to be deployed in the real world. 2) Compared to the VLN models that employ LLMs as planners, NaVid adopts a more realistic modeling for VLN. In particular, NaVid directly deduces low-level executable actions in continuous environments and encodes visual observations in video form, unlike previous LLM-based methods of modeling VLN in discrete spaces or encoding historical observations with textual descriptions [64, 114, 60, 13]. 3) Distinct from existing specialized VLN models, NaVid eliminates the reliance on odometer data, depths, and maps for action planning, thereby obviating the need for generalization challenges posed by odometer noises or the domain discrepancies in depth perception or navigation maps, making NaVid easy to be deployed. To the best of our knowledge, the proposed NaVid is the first video-based VLM for VLN in continuous environments, achieving RGBonly navigation akin to human navigational behavior. 

Our proposed NaVid employs a pre-trained vision encoder to encode visual observations and a pre-trained LLM to reason navigation actions. In this way, the general-purpose knowledge acquired in large-scale pretraining is transferred to VLN tasks, facilitating the learning and boosting the generalization. Drawing inspiration from the advanced video-based VLM, LLaMAVID [54], we represent each frame in robotic visual observations with two kinds of tokens. The first kind consists of an instruction-queried token that extracts visual features specifically relevant to given instructions. The other kind comprises instruction-agnostic tokens that globally encode fine-grained visual information, where the token number determines the granularity of encoded features. The number of tokens for historical observations is allowed to differ from that for current observations. As such, in NaVid, robotic historical trajectories are encoded as visual tokens in the video form, which provides a more informative and adaptive context compared to prior LLM-based VLN models that perform encoding in discrete 

spaces [17, 18] or using textual descriptions [64, 114, 60, 13]. Such video-based modeling imposes stringent constraints on the model inputs as it does not involve other information, _e_ . _g_ ., depth, odometer data, or maps, except for the monocular video. When harnessed in the right manner, it advances in mitigating the generalization challenges resulting from odometer noises and domain discrepancies in depth perception or navigation maps of previous VLN works. 

We conduct extensive experiments for the evaluation of our proposed NaVid in both simulated and real-world environments. Specifically, NaVid achieves SOTA-level performance on the VLN-CE R2R dataset and showcases a significant improvement on cross-dataset evaluation (R2R-RxR). Besides, our method demonstrates impressive robustness on Sim-toReal deployment, achieving about 66% success rate on 200 instructions across four diverse indoor scenes, leveraging only RGB videos as inputs. 

## II. RELATED WORKS 

**Vision-and-Language Navigation (VLN).** A large endeavor of learning to navigate in unvisited environments following human instructions is established over discretized simulated scenes [6, 47, 67, 91], where agents teleport between nodes on a pre-defined navigation graph by aligning language and visual observations for decision-making [61, 95, 26, 90, 40, 28, 66, 33]. Despite efficiency, directly transferring VLN models trained in discrete space to real-world robot applications is impractical. As a result, the more realistic VLN in continuous environments (VLN-CE) is proposed [43, 75], allowing agents to navigate freely to any unobstructed space in the simulator either by predicting low-level controls [72, 38, 14, 29, 15] or selecting from navigable sub-goals estimated by waypoint predictors [35, 45, 42]. Meanwhile, following the success of learning generic visual-linguistic representations from webscale image-text pairs [19, 53, 85, 50, 89], many VLN models benefit from large vision-language models [52, 34, 17, 18] and VLN-specific pre-training [32, 63, 31, 100, 68]. Very recently, by scaling up navigation training data, the performance of VLN agents on the well-recognized R2R benchmark [44] is approaching humans [98]. This significant development suggests that the implementation of VLN techniques in real-world robotics is an increasingly viable and timely consideration. 

**Sim-to-Real Transfer for VLN.** Despite great advances, existing VLN methods are predominantly built and evaluated in simulation, which largely overlooks the intricate and unpredictable nature of real-world conditions. Sim-toreal VLN transfer is an under-studied topic; until today, the only literature that systematically studies this problem is from Anderson et al. [7], which justifies the performance gap (more than 50% drop in success rate) due to action space and visual domain differences. In addition, we would like to highlight the challenge of generalizing to free-form language instructions - agents often fail to interpret different styles of instructions even when trained on millions of in-domain visual data [98, 39]. In light of this, many recent researches 


Fig. 2: **The overview of NaVid.** The inputs of NaVid consist of the RGB frames from the online video observation _{_ **x** 0 _, · · · ,_ **x** _t}_ along with the human instruction _I_ . For each frame, we use an observation encoder to extract the visual information with the instruction to obtain observation tokens, including, instruction-queried tokens (orange blocks) and instruction-agnostic tokens (blue blocks). At the current step _t_ , the history frames _{_ **x** 0 _, · · · ,_ **x** _t−_ 1 _}_ and the current frame **x** _t_ are encoded as observation tokens, with 4 and 64 instruction-agnostic tokens for history frames and current frames, respectively. Besides, our method obtains language tokens by a text encoder. Finally, split by the special tokens [HIS], [OBS], and [NAV], we concatenate the observation tokens and language tokens and send the tokens to the Vicuna-7B then obtain the next-step action. 

leverage the exceptional generalization abilities of the Large (Vision-)Language Models to facilitate VLN generalization. Either investigating the navigational reasoning capacity intrinsic to LLMs [114, 64, 113, 60, 13, 76, 55] or incorporating LLMs into navigation systems through modular designs that facilitate instruction parsing [16] or through the injection of commonsense knowledge [69]. We follow such a trend and further explore how to utilize a unified large model for lowlevel action prediction and its generalizability in real-world scenarios. This approach seeks not only to advance the state of VLN by leveraging the comprehensive understanding and versatile capabilities of LLMs [114, 64, 113, 60, 13, 69] but also to bridge the gap between simulated environments and the multifaceted challenges presented by real-world applications. 

**Large Models as Embodied Agents.** Recently, researchers have been exploring the integration of large models into diverse embodied domains [25, 114, 56, 80, 84, 76, 37]. PaLME [25], for instance, suggests the incorporation of tokens from various modalities, alongside text tokens, into a large model. The model then generates high-level robotics instructions for tasks such as mobile manipulation, motion planning, 

and tabletop manipulation. Taking a step further, RT-2 [10] generates low-level actions for robots, facilitating closed-loop control. GR-1 [99] introduces a GPT-style model [70, 114, 60] specifically designed for multi-task language-conditioned visual robot manipulation [104]. This model predicts robot actions and future images based on language instructions, observed images, and robot states. RoboFlamingo [51] proposes a vision-language manipulation framework that utilizes pre-trained vision-language models to formulate manipulation policies for robotics. It aims to offer a cost-effective and highperformance solution for robot manipulation [21, 88, 104, 83], allowing users to fine-tune their robots with large models. EMMA-LWM [105] develops a world model for driving agents through verbal communication, showing convincing results in a digital gaming environment [94]. Diving deeper into these works, this paper centers on another pivotal embodied domain: vision-and-language navigation, which necessitates robots to navigate in unseen environments following human instructions. 

## III. PROBLEM FORMULATION 

The formulation of Vision-and-Language Navigation in Continuous Environments (VLN-CE) in this work is as follows: At the time _t_ , given a natural language instruction _I_ consisting of _l_ words and a video observation _Ot_ comprising a sequence of frames _{_ **x** 0 _, · · · ,_ **x** _t}_ , the agent is required to plan a low-level action **a** _t_ +1 _∈A_ for the next step. This action will take the agent to the next state and the agent will receive a new observation **x** _t_ +1. Overall, we can formulate the decisionmaking as a Partially Observable Markov Decision Process (POMDP), denoted by _{_ **x** 0 _,_ **a** 1 _,_ **x** 1 _,_ **a** 2 _, · · · ,_ **x** _t}_ . In this work, the observation space _O_ corresponds to the videos captured with a monocular RGB camera without other additional data involved, and the action space incorporates qualitative action types alongside quantitative action arguments, also known as low-level actions [43] in this domain. This modeling enables a natural paradigm where observations are purely vision-based and readily obtainable, while actions are directly executable, akin to human navigational behavior. 

## IV. THE PROPOSED NAVID AGENT 

With the formulation in Sec.III, we devise a video VLMbased navigation agent, named NaVid. The NaVid is the first of its kind to transfer general knowledge of VLMs to a realistic VLN agent. We introduce its architecture in Sec. IV-A, then elaborate on the detailed modeling for VLN inputs and outputs in Sec. IV-B. The training strategy is detailed in Sec. IV-C, and the implementation details are described in Sec. IV-D. 

## _A. Overall Architecture_ 

We build NaVid on top of a general-purpose video-based VLM named LLaMA-VID [54]. For our proposed NaVid, we inherit the main architecture of LLaMA-VID and incorporate the task-specific designs on top of it, to facilitate the transfer of general knowledge to VLN-CE to make its generalization challenges more readily solvable. 

As illustrated in Fig. 2, NaVid consists of a vision encoder, a query generator, a LLM, and two cross-modality projectors. Given the observations up to time _t_ , _i_ . _e_ ., a video sequence comprising _t_ frames, we encode this video to a sequence of tokens via the vision encoder (EVA-CLIP [86] in implementation) and project them to a space aligned with language tokens. For brevity, we call the projected tokens as observation tokens. As common, the instructions are also tokenized as a set of tokens, called instruction tokens. We concatenate both observation tokens and instruction tokens and send them to the LLM to infer the VLN actions in linguistic form. Note that our work focuses on task-specific modeling rather than model architecture, as detailed in the following. 

## _B. The VLN-CE Modeling of NaVid_ 

**Observation encoding.** Given the captured monocular video up to time _t_ , denoted by _Ot_ = _{_ **x** 0 _. · · · ,_ **x** _t}_ , we represent each frame with one instruction-queried visual token and 

several instruction-agnostic visual tokens. The instructionqueried tokens extract visual features specifically relevant to given instructions, and the instruction-agnostic tokens globally encode fine-grained visual information. For each frame **x** _t_ , we first get its visual embedding **X** _t ∈_ R<sup>_Nx×C_</sup> with a vision encoder, where _Nx_ is the patch number ( _Nx_ is set to 256) and _C_ is the embedding dimension. 

To get the instruction-queried tokens, we employ a Q- Former-based query generator to generate the instructionaware query **Q** _t ∈_ R<sup>_M×C_</sup> with the query generator _GQ_ , where _M_ denotes the number of queries per frame and _C_ is the dimension of each query. The query generation can be formulated as: 


where **X** _t_ and **I** are the visual embeddings and the textual embeddings of the frame **x** _t_ and the instruction _I_ . _GQ_ ( _·_ ) is a Q-Former-based transformer to learn instruction-aware queries via a cross-modality interaction between **X** _t_ and **I** as that in [54]. Similar to the operation in Q-Former [49], the instruction-queried tokens **E**<sup>_Q_</sup> _t_ are obtained by a crossattention between **X** _t_ and **Q** _t_ , formulated as below: 


where _PQ_ ( _·_ ) represents the cross-modality projector for getting instruction-quired tokens, and _Pool_ ( _·_ ) is an averaging operation along the dimension of queries, making **E**<sup>_Q_</sup> _t_<sup>_∈_R1</sup><sup>_×C_.</sup> 

For the instruction-agnostic tokens, we directly perform a grid pooling operation and a cross-modality projection to get them, which can be formulated as: 


where _GridPool_ ( _·_ ) is a grid pooling operation [54], squeezing the tokens from _Nx_ to _Nv_ , yielding **E**<sup>_V_</sup> _t ∈_ R<sup>_Nv×C_</sup> . A detailed description of the grid pooling can be found in the supplemental material. Representing each frame with two tokens as in LLaMA-VID [54] does not meet the requirements of the VLN-CE task, as experimentally evidenced in the following. This is because LLaMA-VID is primarily designed for high-level question-answering tasks, whereas NaVid needs to plan executable actions for robots. Thus, we adopt the grid pooling here to enable the instruction-agnostic tokens to preserve sufficient geometry information so that the LLM in NaVid have enough contexts for reasoning the quantitative arguments of robotic actions. 

For VLN-CE, the current frame serves as the primary basis for navigation action reasoning, while historical frames provide important contexts for tracing navigation progress. Considering their different requirements for preserving geometry information, we adopt a varying number of instructionagnostic tokens in encoding the historical frames and the current frame. In this work, unless otherwise specified, we set the number of instruction-agnostic tokens to 64 for the current frame while 4 for each historical frame. This not only facilitates the learning but also improves the efficiency. 

To further facilitate the training of NaVid, we explicitly distinguish different types of information with special tokens before sending them to the LLM within NaVid. 

Specifically, we adopt special tokens <HIS>, </HIS>, and <OBS>, </OBS> to demarcate tokens encoded from historical frames and the current frame, respectively. Here, <HIS> and <OBS> signify the beginning of the corresponding token sequences while </HIS> and </OBS> mark their ends. Additionally, we use another special token <NAV> to prompt the LLM to begin to process the textual tokens of instructions and output the robotic actions in linguistic form. As a result, the input of NaVid can be summarized as below. 

**Input:** _<HIS > {historical_ _<u>f</u> rames} </HIS >< OBS > {current_ _<u>f</u> rame} < /OBS >_ ) _< NAV > {instruction_ _<u>content}</u>_ **Output:** _{answer_ _<u>content}</u>_ 

In this format, _{historical_ _<u>f</u> rames}_ , _{current_ _<u>f</u> rame}_ , _{instruction_ _<u>content}</u>_ and _{answer_ _<u>content}</u>_ are the placeholders for the tokens of historical frames, current frame, instruction, and reasoned actions, respectively. 

**Action planning.** NaVid plans the next-step action for VLNCE in linguistic form. Each action of its outputs consists of two variables aligned with the setting of VLN-CE. One of them is the action type, chosen from a discrete set _{_ FORWARD _,_ TURN-LEFT _,_ TURN-RIGHT _,_ STOP _}_ . The other is the quantitative arguments corresponding to different action types. For FORWARD, NaVid further infers the specific moving distance. For TURN-LEFT and TURN-RIGHT, NaVid also predicts specific rotation degrees. A regular expression parser [41] is employed to extract the action types and arguments for model evaluation and real-world deployment. 

## _C. The Training of NaVid_ 

The available navigational simulation data are still limited in their diversity, authenticity, and scale. We design a hybrid training strategy to maximize the utilization of these data in enabling NaVid to generalize as effectively as possible to novel scenes or the real world. To this end, two key approaches are proposed in the hybrid training strategy. One is to collect nonoracle navigation trajectories and incorporate them into the training loop. The other is to design auxiliary tasks to enhance the capabilities of NaVid on navigation scene understanding and instruction following. We elaborate separately below. 

**Non-oracle navigation trajectories collection.** Inspired by the Dagger technique [74], we collect non-oracle navigation trajectories and incorporate them into the training of NaVid. Without this approach, our NaVid would only be exposed to oracle navigation trajectories during training, which diverges from practical application conditions and diminishes the robustness of the learned navigation strategy. To achieve this, we first collect oracle navigation trajectories, including monocular video observations, instructions, and robotic actions, from the 


**User:** Imagine you are a robot programmed for navigation tasks. You have been given a video of historical observations and a image of current observation <image>. Your assigned task is: Walk forward into and down the middle of the workspace. Walk forward until you reach a white pail on the floor next to a desk with a black chair and stop. Analyze this series of images to decide your next move, which could involve turning left or right by a specific degree or moving forward a certain distance. 

**Assistant:** The next action is move forward 75 cm. **Instruction reason sampling** 


**User:** Assume you are a robot designed for navigation. You are provided with captured images sequences <image>. Based on this image sequence, please descripe the navigation trajctory of the robot. 

**Assistant:** Walk forward into and down the middle of the workspace. Walk forward until you reach a white pail on the floor next to a desk with a black chair and stop. 

Fig. 3: Examples of navigation data, comprising the action planning sample (above) and the instruction reasoning sample (below). 

VLN-CE R2R dataset. Specifically, we gather data from 61 MP3D indoor scenes [11], containing 320k step-wise samples in total. Then, we train NaVid on these oracle trajectory data and deploy the obtained agent in VLN-CE environments for further collecting the non-oracle navigation trajectories. As a result, we get another 180k step-wise samples. The samples from both oracle and non-oracle trajectories are combined for the final training of NaVid, as shown in the above of Fig. 3. 

**Co-training of VLN-CE and auxiliary tasks.** As a navigation agent, precisely understanding environments and following given instructions are two indispensable capabilities besides planning navigation actions. To facilitate agent learning, we combine the VLN-CE action planning together with two auxiliary tasks in a co-training paradigm. For environmental understanding, we have designed an auxiliary task called instruction reasoning. Given a video-based navigation 

trajectory, NaVid is required to deduce the corresponding instructions for that trajectory. This auxiliary task can be easily implemented with a shared data organization format introduced in Sec. IV-B, in which the _{instruction_ _<u>content}</u>_ and _{answer_ _<u>content}</u>_ can be instantiated as the prompts of requesting the descriptions of robotic navigation trajectories and the human-labeled instructions provided in the dataset. The instruction reasoning auxiliary task contains 10k trajectories, an example is provided in the below of Fig. 3. Moreover, for the enhancement of instruction following and the antiforgetting of general knowledge acquired in pre-training, we incorporate the video-based question-answering samples into our co-training as well. Details can be found in [54]. For brevity, we do not elaborate on them here. 

## _D. Implementation details_ 

**Training configurations.** NaVid is trained on a cluster server with 24 NVIDIA A100 GPUs for approximately 28 hours, totaling 672 GPU hours. For video-caption data, we sample frames at 1 FPS, to remove redundant information between consecutive frames. We keep all the frames for navigation-action data, mostly smaller than 300 frames. During training, all modules including EVA-CLIP [86], QFormer [22], BERT [23], and Vicuna-7B [20] are loaded with default pre-trained weight. Following the strategy in [54], we only optimize the trainable parameters of LLaMA and text encoder for only 1 epoch. 

**Evaluation configurations.** After NaVid predicts language actions, we leverage regular expressions matching [41] for expecting valid actions. We find this simple algorithm achieves a 100% success rate for obtaining valid actions under the VLN-CE val-unseen R2R evaluation. For real-world navigation, we use a remote server to run NaVid to receive observations (along with text instructions) and command a local robot to execute the predicted actions. During navigation, the agent requires about 1.2 to 1.5 seconds to output one action per frame. This could be improved by using acceleration techniques, such as quantization [58, 57]. 

## V. EXPERIMENTS 

## _A. Experiment Setup_ 

**Simulated environments.** We evaluate our method on the VLN-CE benchmarks, which provide continuous environments for executing low-level actions on reconstructed photorealistic indoor scenes [43]. We consider R2R [44] and RxR [47] in VLN-CE, the two most recognized benchmarks of VLN. For a fair comparison, all methods are trained on the 10,819 R2R train split, and evaluated on the 1,839 R2R val-unseen split and 1,517 RxR val-unseen split to evaluate cross-split and crossdatasets performance, respectively. 

**Real-world environments.** To evaluate the performance of our method in real-world environments, we follow the experiment setting of [7, 101] and design comprehensive experiments that include different indoor scenes and different 

difficulty instructions. We select four diverse indoor scenes including Meeting_room, Office, Lab, and Lounge. For instruction, we design two types of instruction: 1) Simple landmark instruction following task, which requires the agent to understand the semantics of the target and move to the relative location of the target. 2) Complex Composite instruction following Task, which requires the agent to complete 2-5 combination instructions of landmark following task. For each selected scene, we design 25 Simple landmark instructions and 25 complex composite instructions, leading to a total of 200 instruction-following cases. 

We conduct all real-world experiments using a Turtlebot4<sup>1</sup> equipped with a Kinect DK camera for capturing both depth and RGB images. For baselines that require odometry, we use a built-in RPLIDAR A1M8 Lidar of the turtlbeot4 and leverage the toolbox of Nav2 [62] for localization and mapping. The calibration of the Lidar and camera follows the previous work [111]. Please refer to the supplemental material for details. Note that there exist advanced tracking and localization systems [59, 106, 107] which may further improve the performance. 

**Metrics.** We follow the standard VLN evaluation metrics [6, 44, 48] to evaluate the navigation performance, including success rate (SR), oracle success rate (OS), success weighted by path length (SPL) [5], trajectory length (TL), and navigation error from goal (NE). Among all, SPL is the primary metric as it reflects both the accuracy and efficiency of navigation [4]. Note that an episode is considered successful if the agent calls the STOP action within 3 m of the goal in the VLN-CE and 1.5 m in real-world environments. More details about evaluation metrics can be found in the supplemental material. 

**Baselines.** For a fair comparison with NaVid, we compare the performance of methods that directly predict low-level action primitives in the VLN-CE environments: 

- Seq2Seq [43] is a simple sequence-to-sequence baseline that uses a recurrent policy to predict the action directly from the RGBD observations. RGB-Seq2Seq indicates the use of RGB observations only. 

- CMA [43] utilizes cross-model attention between instruction and RGBD-observations to predict action. RGB-CMA indicates the use of RGB observations only. 

- WS-MGMap [15] leverages a multi-granularity map, which contains object geometry, texture, and semantic information. 

## _B. Comparison on Simulated Environment_ 

**VLN-CE R2R.** We first conduct experiments on the VLNCE R2R Val-Unseen dataset to evaluate the cross-split generalizability of methods. The results can be found in Table I. Here we mark the specific observations required by the methods, whereas our method only uses RGB observations. Compared to the related VLN-CE setting (low-level action space), our method achieves SOTA performance in terms of SPL, NE, 

> 1Turtlebot4 overview: https://clearpathrobotics.com/turtlebot-4/. 

TABLE I: Comparing on VLN-CE R2R Val-Unseen.<sup>_∗_</sup> : Methods use high-level action space. _†_ : Methods use the same waypoint predictor proposed in [35]. _‡_ : Methods use additional visual data than MP3D scenes [11]. 

||Observation||VL|N-CE|R2R|Val-Un|seen|
|---|---|---|---|---|---|---|---|
||Pan. S.RGB Depth|Odo.|TL|**NE**_↓_|**OS**_↑_|**SR**_↑_|**SPL**_↑_|
|HPN+DN<sup>_∗_</sup>[45]|✓<br>✓|✓|7.62|6.31|40.0|36.0|34.0|
|CMA<sup>_∗_</sup>_†_ [35]<br>|✓<br>✓|✓|10.90|6.20|52.0|41.0|36.0|
|VLN<br>⟳<br>BERT<sup>_∗_</sup>_†_ [35]|✓<br>✓|✓|12.23|5.74|53.0|44.0|39.0|
|Sim2Sim<sup>_∗_</sup>[42]|✓<br>✓|✓|10.69|6.07|52.0|43.0|36.0|
|GridMM<sup>_∗_</sup>_†_ [97]|✓<br>✓|✓|13.36|5.11|61.0|49.0|41.0|
|HAMT<sup>_∗_</sup>_†‡_ [98]|✓<br>✓|✓|–|4.80|–|55.0|51.0|
|ETPNav<sup>_∗_</sup>[3]|✓<br>✓|✓|11.99|4.71|65.0|57.0|49.0|
|AG-CMTP [14]|✓<br>✓|✓|–|7.90|39.2|23.1|19.1|
|R2R-CMTP [14]|✓<br>✓|✓|–|7.90|38.0|26.4|22.7|
|LAW [72]|✓<br>✓|✓|8.89|6.83|44.0|35.0|31.0|
|CM2 [29]|✓<br>✓|✓|11.54|7.02|41.5|34.3|27.6|
|WS-MGMap [15]|✓<br>✓|✓|10.00|6.28|47.6|**38.9**|34.3|
|Seq2Seq [43]|✓<br>✓||9.30|7.77|37.0|25.0|22.0|
|CMA [43]|✓<br>✓||8.64|7.37|40.0|32.0|30.0|
|RGB-Seq2Seq|✓||4.86|10.1|8.10|0.00|0.00|
|RGB-CMA|✓||6.28|9.55|10.8|5.00|4.43|
|**Ours**|✓||7.63|**5.47 **|**49.1**|37.4|**35.9**|
|(|a)||||(b)|||


Fig. 4: (a) Success Rate of NaVid on different steps during inference. The red dot line indicates the average success rate. (b) The episodes number on different steps during training. The ’Steps’ of the x-axis indicate the oracle actions required by the instructions. 

OS, and comparable performance on SR, without using depth and odometry information. For the methods Seq2Seq-RGB and CMA-RGB that share the same setting, our method significantly outperforms these methods by improving the SR from 5 _._ 00% to 37 _._ 4%, and SPL from 4 _._ 43% to 35 _._ 9%. Our method outperforms the SOTA method WS-MGMap by 1 _._ 6% regarding SPL. The results demonstrate the effectiveness of our method by showing SOTA-level performance with only RGB observations. 

To explore the challenges associated with longer memory requirements (more steps) in NaVid, we report the performance on different horizon instructions, where instructions typically necessitate 30 to 90 steps to complete, spanning approximately 5 to 20 meters. The results are illustrated in Fig 4 (a), showing that our method maintains consistent performance across a range from short (lower than 30 steps) to long distances (more than 90 steps). Additionally, we plot the number of episodes per step during training in Fig 4 (b). Although about 5 _._ 91% of episodes exceeded 90 steps, our method still performs comparably to the majority of episodes, which range from 35 

TABLE II: Comparing cross-dataset performance on VLN-CE RxR Val-Unseen. Note that, _A_<sup>2</sup> Nav is a zero-shot method that leverages GPT as the planner. 

||Ob|servatio|n|VL|N-CE|RxR V|al-Uns|een|
|---|---|---|---|---|---|---|---|---|
||S.RGB|Depth|Odo.|TL|**NE**_↓_|**OS**_↑_|**SR**_↑_|**SPL**_↑_|
|LAW [72]|✓|✓|✓|4.01|10.87|21.0|8.0|8.0|
|CM2 [29]|✓|✓|✓|12.29|8.98|25.3|14.4|9.2|
|WS-MGMap [15]|✓|✓|✓|10.80|9.83|29.8|15.0|12.1|
|Seq2Seq [43]|✓|✓||1.16|11.8|5.02|3.51|3.43|
|CMA [43]|✓|✓||5.09|11.7|10.7|4.41|2.47|
|RGB-Seq2Seq|✓|||4.43|11.2|12.2|0.0|0.0|
|RGB-CMA|✓|||13.56|9.55|14.8|0.0|0.0|
|_A_<sup>2</sup>Nav [16]|✓|||–|–|–|16.8|6.3|
|**Ours**|✓|||10.59|**8.41**|**34.5**|**23.8**|**21.2**|


TABLE III: Comparison of LLMs on 100 sampled VLNCE R2R Val-Unseen split. Here, the ’-’ indicates the corresponding method does not predict valid language actions for execution. 

||VLN|-CE R2|R Val-Un|seen Su|b-Split|
|---|---|---|---|---|---|
||TL|**NE**_↓_|**OS**_↑_|**SR**_↑_|**SPL**_↑_|
|GPT-4V [102]|5.79|11.4|10.00|5.00|3.11|
|Emu [87]|-|-|-|-|-|
|LLaVA [57]|-|-|-|-|-|
|LLaMA-VID [54]|-|-|-|-|-|
|LLaVA-Nav|5.05|7.82|14.0|10.0|9.43|
|LLaMA-VID-Nav|10.7|8.73|40.0|29.0|27.5|
|**Ours**|8.02|**5.52**|**45.0**|**38.0**|**35.4**|


to 75 steps (about 74 _._ 3% of episodes). This robust performance may be attributed to our strategy of co-tuning navigation data with web-scale video data, which includes sequences of up to 300 frames, thus enabling our method to process a longer historical context than is typically required by most VLN tasks. 

**VLN-CE RxR.** To evaluate the cross-dataset performance of methods, we train the models on R2R trajectory-instruction samples and compare their zero-shot performance on RxR Val-Unseen data split. RxR dataset contains instructions of finer granularity that describe rich landmarks and longer trajectories, which establishes a large language and visual gap that is suitable for evaluating the generalization potential of the methods. As shown in Table II, we find that our method outperforms existing methods by a large margin in terms of NE, OS, SR, and SPL. Note that the trajectory length (TL) of Seq2Seq is extremely small because of its poor instruction-following ability (3 _._ 51% SR), leading by early stopping. Compared with _A_<sup>2</sup> Nav [16], the current SOTA method in zero-shot VLN-CE RxR, our method achieves 41 _._ 7% (from 16.8 to 23.8) and 236 _._ 5% (from 6.3 to 21.2) better results on SR and SPL. Besides, the Seq2Seq-RGB and CMA-RGB baselines, which share the same setting, fail on all instructions, demonstrating the challenges of RGBonly methods. This proves the generalization potential of our method by incorporating the video-based large vision-language model into VLN for addressing free-form language navigation tasks. 

**Comparison with Large foundation models.** We then want to evaluate the performance of variant mainstream large 

TABLE IV: Comparison of different alternatives for modelling past trajectories. 

|Method|TL|VLN-CE<br>NE↓|R2R Va<br>OS↑|l-Unsee<br>SR↑|n<br>SPL↑|
|---|---|---|---|---|---|
|(A) Text-based|1.45|8.82|0.0|0.0|0.0|
|(B) Map-text|2.76|7.12|9.51|9.13|8.97|
|(C) Ego-view-text|5.05|8.85|35.5|23.5|20.8|
|Video-based (NaVid)|7.63|**5.47**|**49.1**|**37.4**|**35.9**|


foundation models on the vision language navigation task. Here, GPT-4V [102] and Emu [87] support multi-conversation with image inputs, so in each iteration of conversation we feed a new observed RGB image. LLaVA [57] is a singconversation image model, so we leverage an observationto-history technique to encode history. LLaMA-VID [54] is able to answer questions based on the video inputs, which can be replaced by the navigation observations. For the models LLaVA and LLaMA-VID, which have published their training datasets and code, we co-tune these models with our proposed navigation data, resulting in the modified models named LLaVA-Nav and LLaMA-VID-Nav, respectively. All baselines are carefully tuned and promoted, and the details can be found in supplemental material. 

Considering the extreme computation cost such as promoting history in GPT-4V and LLaVA, we randomly sample 100 episodes as a sub-split of VLN-CE R2R Val-Unseen sub-split (the ID of sampled episodes can be found in the supplemental material for reproducing). The results can be found in Table III. We find that the methods without training on proposed navigation data suffer a very poor performance. Especially, Emu, LLaVA, and LLaMA-VID frequently output action-irrelevant answers, such as environment description or navigation comments, making the agent very hard to navigate. A more powerful model GPT-4V, with a carefully in-context prompt [114, 36], can relatively stable output valid actions, showcasing a lower performance at 5% SR. After tuning with the proposed navigation data, we found significant improvements in the LLaVA-Nav and LLaMA-VID-Nav, which demonstrate the importance of the collected navigation data. Besides, training on navigation data leads to better instructionfollowing ability, making the valid actions answer ratio from 0% to 91 _._ 3% for LLaMA-VID-Nav. 

**Comparison with different navigation history representations.** We compare our proposed video-based modeling in NaVid with other alternatives for representing past trajectories. We adjust the special tokens mechanism for identifying different representations while preserving other design elements unchanged to ensure a fair comparison. We have meticulously implemented these alternatives and collected appropriate navigation and caption data for training. Their detailed implementations are described below: 

- **(A) Text-based** : We use text to describe the navigation history as inputs (including the current frame). By following NavGPT [114], we use a visual foundation model (LLaVA [57]) to describe the environments of each frame and 

TABLE V: Comparison results of LM-Nav and its variants on the Val-Unseen split of RxR dataset. Here, “ _∗_ ” indicates the vanilla version. 

|Method|OS↑|SR↑|
|---|---|---|
|LM-Nav* (GPT 3.5, CLIP)|24.0|7.38|
|LM-Nav (GPT 4, EVA-CLIP)|18.3|9.89|
|LM-Nav (Vicuna-7B, EVA-CLIP)|15.7|8.20|
|NaVid (Vicuna-7B, EVA-CLIP)|**35.5**|**23.5**|


combine per-frame text observation with GPT-4 [1] every 10 frames. Note that, using GPT-4V [102] to replace LLaVA may have better performance but will lead to forbidden costs. The model is co-tuned with the text-QA dataset in LLaVA [57]. 

- **(B) Map-text** : We add the current top-down 2D map along with textual navigation history information (A) as inputs. The top-down 2D maps are obtained from the Habitat simulator [75] and we directly use the default style. The top-down maps include an arrow indicating the location and orientation of the robots, and also use grey color to indicate navigatable areas. The top-down map is encoded as 256 tokens. The model is co-tuned with text- and image-QA datasets used in LLaMA-VID [54] and LLaVA [57]. 

- **(C) Ego-view-text** : This model leverages the current egocentric image along with textual navigation history information (A) as inputs. The egocentric images are obtained directly from the Habitat simulator. The egocentric image view is encoded as 256 tokens. The model is co-tuned with text- and image-QA datasets used in LLaMA-VID [54] and LLaVA [57]. 

We can find, for VLN tasks, modeling past trajectories as texts or 2D maps are both clearly inferior to modeling them in a video form, with SPL dropping from 35.9% to 20.8%/ 8.97%. This demonstrates the necessity and superiority of our proposed video-based modeling for the past trajectories. We believe the reason is that modeling past trajectories as texts or 2D maps significantly compresses the rich visual information, which increases the difficulty of understanding the trajectory history. Furthermore, the inference time for textual history representation averages approximately 2.7 seconds per action step prediction. This duration is roughly double that of the video-based representation. The extended inference time comes from the necessity of an additional LLaVA query for image captioning and a GPT query for summarizing the navigation history. 

**Comparison with LM-Nav and its variant.** LM-Nav is a baseline which leverages discretized environment setting and off-the-shelf foundation models. Here, LM-Nav (GPT-3.5 and CLIP) employs GPT-3.5 for instruction decomposition and CLIP for landmark grounding. Additionally, we construct an ablation study, LM-Nav (Vicuna-7B and EVA-CLIP), substituting the foundation models of LM-Nav with those used in NaVid. We also implement a strong baseline, LM-Nav (GPT4 and EVA-CLIP), which incorporates advanced foundation models as its building blocks. It is important to note that LM- 


Fig. 5: Visual results of our method on **forward instructions** in real-world environments. From top to bottom are instructions, third-person trajectories, and robot perspective videos. 

Nav requires a pre-built landmark graph; hence, we utilized the ground truth landmarks from the Habitat simulator to construct this graph. Moreover, as the visual navigation model (ViNG) [78] employed by LM-Nav is not publicly accessible, we provide the ground truth shortest path to enable LM-Nav to navigate to each landmark effectively. We evaluate all methods on the RxR Val-Unseen split, where NaVid has not previously encountered the instructions and scenes during training. 

The results are presented in Table V. We observe that NaVid significantly outperforms LM-Nav on the RxR ValUnseen split, despite that LM-Nav uses predefined oracle landmarks. This superior performance can be attributed that LM-Nav only focuses on landmarks, ignoring verbs and other directive commands (e.g., _’turn right and walk to the chair’_ or _’turn around and face the sofa’_ ). Such a design neglects the spatial context of the instructions, potentially leading LMNav to incorrect landmarks with the same semantics as the intended targets. This problem is especially common in indoor environments where many objects may belong to the same semantic category. Moreover, models like CLIP and EVA-CLIP may struggle with image grounding in scenes with densely placed objects and obstructed viewpoints. We believe that NaVid, with its end-to-end training approach, demonstrates more adaptability and effectiveness for VLN tasks. 

## _C. Comparison on Real-world Environment._ 

To further evaluate the generalizability of methods in more challenging situations, we conduct an extensive experiment in real-world environments. Here, We select two widely used baselines Seq2Seq and CMA, and a competitive method MS-MGMap (on Table I). Each method is tested on four diverse environments with two types of instructions of different difficulties (25 simple instructions and 25 complex instructions for each scene). For a detailed description of realworld experiments please refer to Sec. V-A and supplemental material. The results are presented in Table VI. Here, we find that our method showcases a significant improvement to all baseline methods. The end-to-end methods, Seq2Seq 


Fig. 6: Visual results of our method on **rotation instruction following** in real-world environments. Our method can accurately park the robot near a specified target, despite initially being oriented towards a similarly classified object (a chair). 

and CMA, suffer from extremely poor performance, which we believe is the sim-to-real gap between VLN-CE and the real world in terms of depth and color domain. Compared to end-to-end methods, the map-based method, WS-MGMap, shows better performance by leveraging an ongoing semantics map. With careful parameters and algorithm adjustment, the map-based methods are widely regarded as a potentially robust strategy in the real world [108, 71]. Nevertheless, our method, by exploring the generability of VLM in VLN, is able to complete most instructions (about 84%) and considerably complex instructions (about 48%), with only the requirement of RGB videos. 

To further investigate the generalizability of NaVid under different instructions, we showcase partial visual results of real-world experiments (Table VI), that require NaVid to follow instructions with very specific landmarks and actions. 

In Fig. 5, we give two similar instructions to drive the robot to move forward under _different stop conditions_ . We find that in both two cases, the robot can follow the instructions to move forward and successfully stop close to the given stop conditions. This demonstrates that NaVid has the ability to understand the instructions and give correct actions for the robot to execute. Besides, we conduct a more challenging experiment by asking the robot to follow complex instructions. The visual results can be found in Fig. 6, where the robot is required to turn orientation and move forward to stop near the given target. These instructions are particularly challenging because the robot is facing an object that shares the same semantic category as the target (chair). Nevertheless, our method is able to follow the instructions by turning the robot to the target orientation and stopping near the correct targets. The videos of these cases can be found in the attached supplemental material. 

We provide more visual results of our method in Fig. 7 in real-world environments. More visual results can be found in the supplemental material. 

TABLE VI: Comparing in four diverse real-world environments scenes (Meeting Room, Office, Lab, and Lounge). Simple I.F. and Complex I.F. indicate the simple instruction following and complex instruction following tasks, respectively. 


Fig. 7: Visual results of our method in a real-world environment. In each real environment example, from top to bottom are instruction, robot perspective video, and third-person view video. 

TABLE VII: Ablation study on both training strategy, and architecture. 

||VLN-CE R2R|Val-U|nseen<br>||||
|---|---|---|---|---|---|---|
||Type|TL|**NE**_↓_|**OS**_↑_|**SR**_↑_|**SPL**_↑_|
|Trainin|No co-training|6.76|6.33|30.8|24.7|23.6|
|g<br>Strategy|No instruction reasoning sample<br>No non-oracle navigation sample|9.46<br>8.73|6.51<br>5.82|46.7 <br>46.4|31.1<br> 34.2|29.1<br>32.0|
||No [NAV]|8.71|5.62|48.1|35.9|33.5|
|Architecture|No [HIS] and [OBS]|8.45|5.56|46.2|35.7|33.4|
||Waypoints prediction|13.65|10.8|11.5|0.00|0.00|
|**Ours**|Full pipeline|7.63|**5.47**|**49.1 **|**37.4**|**35.9**|


## _D. Ablation Studies._ 

To verify the effectiveness of each component in our method, we perform ablation studies on both training strategy and network architecture in Table VII. Through the experiment, we find that the co-tuning data is critical to the performance. This proved that lack of co-tuning data may cause 

the large foundation to lose generalizability. As expected, the instruction reasoning samples and Dagger nav-action samples show improvement. This inspires us that collecting more navigation-related data could further boost the performance of our method, which may be the follow-up direction of VLM for VLN. In the architecture ablation studies, we keep the content tokens (Instruction-queried token and instructionagnostic token) and remove the special tokens: task identifier token [NAV] or observation identifier token [HIS] and [OBS]. We observe that the removal of special tokens leads to a noticeable performance drop, which proves the effectiveness of the special tokens. The _Waypoint prediction_ variant replaces the _A_ action with continuous location and orientation (see supplemental material for detailed implementation). However, the results demonstrate that direct output continuous location and orientation cause extreme challenges to VLMs, making VLMs difficult to learn navigation skills. 

TABLE VIII: Ablation study on numbers of instructionagnostic (visual) tokens per frame. We bold and underline the **best** and <u>second best,</u> respectively. 

|||VL|N-CE|R2R|Val-Uns|een|
|---|---|---|---|---|---|---|
|Tokens per frame|TL|NE↓|OS↑|SR↑|SPL↑|Avg. Time↓|
|(1) 1 tokens|9.01|8.13|30.4|23.9|20.5|**0.87s**|
|(2) 4 tokens|7.63|5.47|49.1|37.4|35.9|1.22s|
|(3) 16 tokens|9.10|**5.38**|**51.1**|**38.0**|**36.1**|2.72s|


To evaluate the effectiveness of instruction-agnostic visual tokens comprehensively, we compare different settings of visual tokens. Specifically, we analyze NaVid with varying numbers of visual tokens per frame, noting that a higher token count retains more visual information. Here, we employ settings of 1, 4, and 16 of visual tokens, which are average pooled with strides of H, H/2, and H/4 of the feature map (H _×_ H), respectively. The results are presented in Table VIII. 

From the results, we observe that utilizing more instructionagnostic (visual) tokens per frame enhances performance, as the increased count of visual tokens provides richer visual information for action prediction. However, an increment in visual tokens also prolongs the inference time. We find that transitioning from setting (1) to setting (2) results in a 56 _._ 4% increase in success rate and a 40 _._ 2% increase in time costs. In contrast, moving from setting (2) to setting (3) yields only a 1 _._ 60% increase in success rate alongside a substantial 122% increase in time costs. This indicates that using four visual tokens per frame strikes an optimal balance, offering sufficient visual information for encoding navigation history while keeping reasonable computational costs. 

We also conduct breakdown experiments to verify the importance of the navigation data in Fig. 8. Here, we split the training into two phases, pre-dagger (0 to 330k) and postdagger (330k to 510k). For pre-dagger, we randomly sample the navigation data for training. Here, we find that insufficient data (less than 280k) may lead to a slow improvement in terms of SR, OS, SPL, and NE. However, when the data increases to 330k, there is an obvious performance boost, indicating the model starts to master the VLN task. For the post-dagger phase, the improvements become minimal. The key reason is that the dagger on the R2R train split does not provide sufficient diverse environments or instruction information for the VLM to learn. 

## VI. DISCUSSION AND CONCLUSION 

In this paper, we propose a video-based VLM method, NaVid, for the vision-and-language navigation task. NaVid achieves SOTA navigation performance without relying on odometers, depth sensors, or maps. Specifically, we extend a video-based VLM model to encode both historical and current navigation data by integrating self-defined special tokens. To learn the vision-instruction following ability, we collect 510k action planning samples from both R2R (320k) and Dagger (180k) and instruction reasoning samples (10k). The extensive experiments in simulator environments demonstrate that 


Fig. 8: Performance analysis of our method on the VLN task across different data scales, showing the impact of data volume on SR, OS, SPL, and NE during pre-dagger and post-dagger training phases. 

our method can achieve SOTA-level performance with only monocular videos as input. Besides, we deploy the NaVid in real-world environments, showing generalizability to conduct VLN tasks in real worlds. 

**Limitation.** Despite the promising results, NaVid has several limitations. _Firstly,_ the computation cost of NaVid causes a long latency problem, impacting navigation efficiency. A convincing way to mitigate this issue is to employ action chunk techniques [112] or quantization techniques [58]. _Secondly,_ under very long horizon instructions, NaVid may experience a performance drop due to the long context tokens problem [24]. And the lack of high-quality long video annotation data intensified this problem. A viable approach to address these challenges is to incorporate more advanced large models [54] as the backbone and utilize long-video data [96]. 

**Future works.** We would like to further explore the potential of extending NaVid to other embodied AI tasks, such as mobile manipulation [103, 82, 109]. To achieve this, we would like to investigate various action designs that enable simultaneous control of the robot arm and mobile base. Additionally, it is critical to collect a dataset of annotated mobile manipulation videos to facilitate our model’s understanding of both instructions and the physical interactions between objects and robots. Furthermore, we seek to enhance the efficiency of our model, allowing it to operate at higher speeds or on lowercost hardware. 

## ACKNOWLEDGMENTS 

We thank all the reviewers for their valuable comments and suggestions. We thank Qiying Yu for the fruitful discussions. We thank Lei Zhang, Feng Zhu, and Dongxu Yu for their assistance in building the real-world experimental system. This project is supported by the Joint Laboratory of Peking University and Galbot. 

REFERENCES 

_arXiv:2307.15818_ , 2023. 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- [2] Dong An, Yuankai Qi, Yangguang Li, Yan Huang, Liang Wang, Tieniu Tan, and Jing Shao. Bevbert: Topo-metric map pre-training for language-guided navigation. _arXiv preprint arXiv:2212.04385_ , 2022. 

- [3] Dong An, Hanqing Wang, Wenguan Wang, Zun Wang, Yan Huang, Keji He, and Liang Wang. Etpnav: Evolving topological planning for vision-language navigation in continuous environments. _arXiv preprint arXiv:2304.03047_ , 2023. 

- [4] Peter Anderson, Angel Chang, Devendra Singh Chaplot, Alexey Dosovitskiy, Saurabh Gupta, Vladlen Koltun, Jana Kosecka, Jitendra Malik, Roozbeh Mottaghi, Manolis Savva, et al. On evaluation of embodied navigation agents. _arXiv preprint arXiv:1807.06757_ , 2018. 

- [5] Peter Anderson, Angel Chang, Devendra Singh Chaplot, Alexey Dosovitskiy, Saurabh Gupta, Vladlen Koltun, Jana Kosecka, Jitendra Malik, Roozbeh Mottaghi, Manolis Savva, et al. On evaluation of embodied navigation agents. _arXiv preprint arXiv:1807.06757_ , 2018. 

- [6] Peter Anderson, Qi Wu, Damien Teney, Jake Bruce, Mark Johnson, Niko S¨underhauf, Ian Reid, Stephen Gould, and Anton Van Den Hengel. Vision-andlanguage navigation: Interpreting visually-grounded navigation instructions in real environments. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 3674–3683, 2018. 

- [7] Peter Anderson, Ayush Shrivastava, Joanne Truong, Arjun Majumdar, Devi Parikh, Dhruv Batra, and Stefan Lee. Sim-to-real transfer for vision-and-language navigation. In _Conference on Robot Learning_ , pages 671–681. PMLR, 2021. 

- [8] Peter Anderson, Ayush Shrivastava, Joanne Truong, Arjun Majumdar, Devi Parikh, Dhruv Batra, and Stefan Lee. Sim-to-real transfer for vision-and-language navigation. In _Conference on Robot Learning_ , pages 671–681. PMLR, 2021. 

- [9] Andreas Blattmann, Tim Dockhorn, Sumith Kulal, Daniel Mendelevitch, Maciej Kilian, Dominik Lorenz, Yam Levi, Zion English, Vikram Voleti, Adam Letts, et al. Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint arXiv:2311.15127_ , 2023. 

- [10] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint_ 

- [11] Angel Chang, Angela Dai, Thomas Funkhouser, Maciej Halber, Matthias Niebner, Manolis Savva, Shuran Song, Andy Zeng, and Yinda Zhang. Matterport3d: Learning from rgb-d data in indoor environments. In _2017 International Conference on 3D Vision (3DV)_ , pages 667–676. IEEE, 2017. 

- [12] Howard Chen, Alane Suhr, Dipendra Misra, Noah Snavely, and Yoav Artzi. Touchdown: Natural language navigation and spatial reasoning in visual street environments. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 12538–12547, 2019. 

- [13] Jiaqi Chen, Bingqian Lin, Ran Xu, Zhenhua Chai, Xiaodan Liang, and Kwan-Yee K Wong. Mapgpt: Map-guided prompting for unified vision-and-language navigation. _arXiv preprint arXiv:2401.07314_ , 2024. 

- [14] Kevin Chen, Junshen K Chen, Jo Chuang, Marynel V´azquez, and Silvio Savarese. Topological planning with transformers for vision-and-language navigation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 11276– 11286, 2021. 

- [15] Peihao Chen, Dongyu Ji, Kunyang Lin, Runhao Zeng, Thomas H Li, Mingkui Tan, and Chuang Gan. Weakly-supervised multi-granularity map learning for vision-and-language navigation. _arXiv preprint arXiv:2210.07506_ , 2022. 

- [16] Peihao Chen, Xinyu Sun, Hongyan Zhi, Runhao Zeng, Thomas H Li, Gaowen Liu, Mingkui Tan, and Chuang Gan. _a_ ˆ2 nav: Action-aware zero-shot robot navigation by exploiting vision-and-language ability of foundation models. _arXiv preprint arXiv:2308.07997_ , 2023. 

- [17] Shizhe Chen, Pierre-Louis Guhur, Cordelia Schmid, and Ivan Laptev. History aware multimodal transformer for vision-and-language navigation. _Advances in Neural Information Processing Systems_ , 34:5834–5847, 2021. 

- [18] Shizhe Chen, Pierre-Louis Guhur, Makarand Tapaswi, Cordelia Schmid, and Ivan Laptev. Think global, act local: Dual-scale graph transformer for vision-andlanguage navigation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 16537–16547, 2022. 

- [19] Yen-Chun Chen, Linjie Li, Licheng Yu, Ahmed El Kholy, Faisal Ahmed, Zhe Gan, Yu Cheng, and Jingjing Liu. Uniter: Universal image-text representation learning. In _European conference on computer vision_ , pages 104–120. Springer, 2020. 

- [20] Wei-Lin Chiang, Zhuohan Li, Zi Lin, Ying Sheng, Zhanghao Wu, Hao Zhang, Lianmin Zheng, Siyuan Zhuang, Yonghao Zhuang, Joseph E Gonzalez, et al. Vicuna: An open-source chatbot impressing gpt-4 with 90%* chatgpt quality. _See https://vicuna. lmsys. org (accessed 14 April 2023)_ , 2023. 

- [21] Jinda Cui and Jeff Trinkle. Toward next-generation learned robot manipulation. _Science robotics_ , 6(54): 

eabd9461, 2021. 

- [22] W Dai, J Li, D Li, AMH Tiong, J Zhao, W Wang, B Li, P Fung, and S Hoi. Instructblip: Towards generalpurpose vision-language models with instruction tuning. arxiv 2023. _arXiv preprint arXiv:2305.06500_ , 2, 2023. 

- [23] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre-training of deep bidirectional transformers for language understanding. _arXiv preprint arXiv:1810.04805_ , 2018. 

- [24] Zican Dong, Tianyi Tang, Lunyi Li, and Wayne Xin Zhao. A survey on long text modeling with transformers. _arXiv preprint arXiv:2302.14502_ , 2023. 

- [25] Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, et al. Palm-e: An embodied multimodal language model. _arXiv preprint arXiv:2303.03378_ , 2023. 

- [26] Daniel Fried, Ronghang Hu, Volkan Cirik, Anna Rohrbach, Jacob Andreas, Louis-Philippe Morency, Taylor Berg-Kirkpatrick, Kate Saenko, Dan Klein, and Trevor Darrell. Speaker-follower models for vision-andlanguage navigation. _Advances in Neural Information Processing Systems_ , 31, 2018. 

- [27] Daocheng Fu, Xin Li, Licheng Wen, Min Dou, Pinlong Cai, Botian Shi, and Yu Qiao. Drive like a human: Rethinking autonomous driving with large language models. In _Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision_ , pages 910–919, 2024. 

- [28] Tsu-Jui Fu, Xin Eric Wang, Matthew F Peterson, Scott T Grafton, Miguel P Eckstein, and William Yang Wang. Counterfactual vision-and-language navigation via adversarial path sampler. In _European Conference on Computer Vision_ , pages 71–86. Springer, 2020. 

- [29] Georgios Georgakis, Karl Schmeckpeper, Karan Wanchoo, Soham Dan, Eleni Miltsakaki, Dan Roth, and Kostas Daniilidis. Cross-modal map learning for vision and language navigation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 15460–15470, 2022. 

- [30] Jing Gu, Eliana Stefani, Qi Wu, Jesse Thomason, and Xin Wang. Vision-and-language navigation: A survey of tasks, methods, and future directions. In _Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 7606–7623, 2022. 

- [31] Pierre-Louis Guhur, Makarand Tapaswi, Shizhe Chen, Ivan Laptev, and Cordelia Schmid. Airbert: In-domain pretraining for vision-and-language navigation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 1634–1643, 2021. 

- [32] Weituo Hao, Chunyuan Li, Xiujun Li, Lawrence Carin, and Jianfeng Gao. Towards learning a generic agent for vision-and-language navigation via pre-training. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 13137–13146, 

2020. 

- [33] Yicong Hong, Cristian Rodriguez, Yuankai Qi, Qi Wu, and Stephen Gould. Language and visual entity relationship graph for agent navigation. _Advances in Neural Information Processing Systems_ , 33, 2020. 

- [34] Yicong Hong, Qi Wu, Yuankai Qi, Cristian RodriguezOpazo, and Stephen Gould. A recurrent vision-andlanguage bert for navigation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 1643–1653, June 2021. 

- [35] Yicong Hong, Zun Wang, Qi Wu, and Stephen Gould. Bridging the gap between learning in discrete and continuous environments for vision-and-language navigation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 15439–15449, 2022. 

- [36] Yingdong Hu, Fanqi Lin, Tong Zhang, Li Yi, and Yang Gao. Look before you leap: Unveiling the power of gpt4v in robotic vision-language planning. _arXiv preprint arXiv:2311.17842_ , 2023. 

- [37] Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, et al. Inner monologue: Embodied reasoning through planning with language models. In _Conference on Robot Learning_ , pages 1769–1782. PMLR, 2023. 

- [38] Muhammad Zubair Irshad, Niluthpol Chowdhury Mithun, Zachary Seymour, Han-Pang Chiu, Supun Samarasekera, and Rakesh Kumar. Sasra: Semanticallyaware spatio-temporal reasoning agent for vision-andlanguage navigation in continuous environments. _arXiv preprint arXiv:2108.11945_ , 2021. 

- [39] Aishwarya Kamath, Peter Anderson, Su Wang, Jing Yu Koh, Alexander Ku, Austin Waters, Yinfei Yang, Jason Baldridge, and Zarana Parekh. A new path: Scaling vision-and-language navigation with synthetic instructions and imitation learning. _arXiv preprint arXiv:2210.03112_ , 2022. 

- [40] Liyiming Ke, Xiujun Li, Yonatan Bisk, Ari Holtzman, Zhe Gan, Jingjing Liu, Jianfeng Gao, Yejin Choi, and Siddhartha Srinivasa. Tactical rewind: Self-correction via backtracking in vision-and-language navigation. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 6741–6749, 2019. 

- [41] Steven M Kearns. Extending regular expressions with context operators and parse extraction. _Software: Practice and Experience_ , 21(8):787–804, 1991. 

- [42] Jacob Krantz and Stefan Lee. Sim-2-sim transfer for vision-and-language navigation in continuous environments. In _European Conference on Computer Vision_ , pages 588–603. Springer, 2022. 

- [43] Jacob Krantz, Erik Wijmans, Arjun Majumdar, Dhruv Batra, and Stefan Lee. Beyond the nav-graph: Visionand-language navigation in continuous environments. In _European Conference on Computer Vision_ , pages 104– 120. Springer, 2020. 

- [44] Jacob Krantz, Erik Wijmans, Arjun Majundar, Dhruv Batra, and Stefan Lee. Beyond the nav-graph: Vision and language navigation in continuous environments. In _European Conference on Computer Vision (ECCV)_ , 2020. 

- [45] Jacob Krantz, Aaron Gokaslan, Dhruv Batra, Stefan Lee, and Oleksandr Maksymets. Waypoint models for instruction-guided navigation in continuous environments. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 15162–15171, 2021. 

- [46] Jacob Krantz, Shurjo Banerjee, Wang Zhu, Jason Corso, Peter Anderson, Stefan Lee, and Jesse Thomason. Iterative vision-and-language navigation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 14921–14930, 2023. 

- [47] Alexander Ku, Peter Anderson, Roma Patel, Eugene Ie, and Jason Baldridge. Room-across-room: Multilingual vision-and-language navigation with dense spatiotemporal grounding. In _Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)_ , pages 4392–4412, 2020. 

- [48] Alexander Ku, Peter Anderson, Roma Patel, Eugene Ie, and Jason Baldridge. Room-across-room: Multilingual vision-and-language navigation with dense spatiotemporal grounding. In _Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)_ , pages 4392–4412, 2020. 

- [49] Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. Blip-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. _arXiv preprint arXiv:2301.12597_ , 2023. 

- [50] Liunian Harold Li, Mark Yatskar, Da Yin, Cho-Jui Hsieh, and Kai-Wei Chang. Visualbert: A simple and performant baseline for vision and language. _arXiv preprint arXiv:1908.03557_ , 2019. 

- [51] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, et al. Vision-language foundation models as effective robot imitators. _arXiv preprint arXiv:2311.01378_ , 2023. 

- [52] Xiujun Li, Chunyuan Li, Qiaolin Xia, Yonatan Bisk, Asli Celikyilmaz, Jianfeng Gao, Noah Smith, and Yejin Choi. Robust navigation with language pretraining and stochastic sampling. _arXiv preprint arXiv:1909.02244_ , 2019. 

- [53] Xiujun Li, Xi Yin, Chunyuan Li, Pengchuan Zhang, Xiaowei Hu, Lei Zhang, Lijuan Wang, Houdong Hu, Li Dong, Furu Wei, et al. Oscar: Object-semantics aligned pre-training for vision-language tasks. In _European Conference on Computer Vision_ , pages 121–137. Springer, 2020. 

- [54] Yanwei Li, Chengyao Wang, and Jiaya Jia. Llama-vid: An image is worth 2 tokens in large language models. _arXiv preprint arXiv:2311.17043_ , 2023. 

- [55] Xiwen Liang, Liang Ma, Shanshan Guo, Jianhua Han, 

Hang Xu, Shikui Ma, and Xiaodan Liang. Mo-vln: A multi-task benchmark for open-set zero-shot vision-andlanguage navigation. _arXiv preprint arXiv:2306.10322_ , 2023. 

- [56] Jinzhou Lin, Han Gao, Rongtao Xu, Changwei Wang, Li Guo, and Shibiao Xu. The development of llms for embodied navigation. _arXiv preprint arXiv:2311.00530_ , 2023. 

- [57] Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. Improved baselines with visual instruction tuning. _arXiv preprint arXiv:2310.03744_ , 2023. 

- [58] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. In _NeurIPS_ , 2023. 

- [59] Zheng Liu, Xiyuan Liu, and Fu Zhang. Efficient and consistent bundle adjustment on lidar point clouds. _IEEE Transactions on Robotics_ , 2023. 

- [60] Yuxing Long, Xiaoqi Li, Wenzhe Cai, and Hao Dong. Discuss before moving: Visual language navigation via multi-expert discussions. _arXiv preprint arXiv:2309.11382_ , 2023. 

- [61] Chih-Yao Ma, Jiasen Lu, Zuxuan Wu, Ghassan AlRegib, Zsolt Kira, Richard Socher, and Caiming Xiong. Self-monitoring navigation agent via auxiliary progress estimation. _arXiv preprint arXiv:1901.03035_ , 2019. 

- [62] Steve Macenski, Francisco Mart´ın, Ruffin White, and Jonatan Gin´es Clavero. The marathon 2: A navigation system. In _2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 2718– 2725. IEEE, 2020. 

- [63] Arjun Majumdar, Ayush Shrivastava, Stefan Lee, Peter Anderson, Devi Parikh, and Dhruv Batra. Improving vision-and-language navigation with image-text pairs from the web. In _European Conference on Computer Vision_ , pages 259–274. Springer, 2020. 

- [64] Bowen Pan, Rameswar Panda, SouYoung Jin, Rogerio Feris, Aude Oliva, Phillip Isola, and Yoon Kim. Langnav: Language as a perceptual representation for navigation. _arXiv preprint arXiv:2310.07889_ , 2023. 

- [65] Sang-Min Park and Young-Gab Kim. Visual language navigation: A survey and open challenges. _Artificial Intelligence Review_ , 56(1):365–427, 2023. 

- [66] Yuankai Qi, Zizheng Pan, Shengping Zhang, Anton van den Hengel, and Qi Wu. Object-and-action aware model for visual language navigation. In _European Conference on Computer Vision_ , pages 303–317. Springer, 2020. 

- [67] Yuankai Qi, Qi Wu, Peter Anderson, Xin Wang, William Yang Wang, Chunhua Shen, and Anton van den Hengel. Reverie: Remote embodied visual referring expression in real indoor environments. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 9982–9991, 2020. 

- [68] Yanyuan Qiao, Yuankai Qi, Yicong Hong, Zheng Yu, Peng Wang, and Qi Wu. Hop: History-and-order aware pre-training for vision-and-language navigation. In _Proceedings of the IEEE/CVF Conference on Computer_ 

_Vision and Pattern Recognition_ , pages 15418–15427, 2022. 

- [69] Yanyuan Qiao, Yuankai Qi, Zheng Yu, Jing Liu, and Qi Wu. March in chat: Interactive prompting for remote embodied referring expression. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 15758–15767, 2023. 

- [70] Alec Radford, Karthik Narasimhan, Tim Salimans, Ilya Sutskever, et al. Improving language understanding by generative pre-training. 2018. 

- [71] Santhosh Kumar Ramakrishnan, Devendra Singh Chaplot, Ziad Al-Halah, Jitendra Malik, and Kristen Grauman. Poni: Potential functions for objectgoal navigation with interaction-free learning. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 18890–18900, 2022. 

- [72] Sonia Raychaudhuri, Saim Wani, Shivansh Patel, Unnat Jain, and Angel X Chang. Language-aligned waypoint (law) supervision for vision-and-language navigation in continuous environments. _arXiv preprint arXiv:2109.15207_ , 2021. 

- [73] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Bj¨orn Ommer. High-resolution image synthesis with latent diffusion models. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 10684–10695, 2022. 

- [74] St´ephane Ross, Geoffrey Gordon, and Drew Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ , pages 627–635. JMLR Workshop and Conference Proceedings, 2011. 

- [75] Manolis Savva, Abhishek Kadian, Oleksandr Maksymets, Yili Zhao, Erik Wijmans, Bhavana Jain, Julian Straub, Jia Liu, Vladlen Koltun, Jitendra Malik, et al. Habitat: A platform for embodied ai research. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 9339–9347, 2019. 

- [76] Raphael Schumann, Wanrong Zhu, Weixi Feng, Tsu-Jui Fu, Stefan Riezler, and William Yang Wang. Velma: Verbalization embodiment of llm agents for vision and language navigation in street view. _arXiv preprint arXiv:2307.06082_ , 2023. 

- [77] James A Sethian. Fast marching methods. _SIAM review_ , 41(2):199–235, 1999. 

- [78] Dhruv Shah, Benjamin Eysenbach, Gregory Kahn, Nicholas Rhinehart, and Sergey Levine. Ving: Learning open-world navigation with visual goals. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 13215–13222. IEEE, 2021. 

- [79] Dhruv Shah, Blazej Osinski, Brian Ichter, and Sergey Levine. Lm-nav: Robotic navigation with large pretrained models of language, vision, and action. _arXiv preprint arXiv:2207.04429_ , 2022. 

- [80] Dhruv Shah, Bła˙zej Osi´nski, Sergey Levine, et al. Lm- 

nav: Robotic navigation with large pre-trained models of language, vision, and action. In _Conference on Robot Learning_ , pages 492–504. PMLR, 2023. 

- [81] Dhruv Shah, Ajay Sridhar, Arjun Bhorkar, Noriaki Hirose, and Sergey Levine. Gnm: A general navigation model to drive any robot. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 7226–7233. IEEE, 2023. 

- [82] Mohit Shridhar, Jesse Thomason, Daniel Gordon, Yonatan Bisk, Winson Han, Roozbeh Mottaghi, Luke Zettlemoyer, and Dieter Fox. Alfred: A benchmark for interpreting grounded instructions for everyday tasks. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 10740–10749, 2020. 

- [83] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Cliport: What and where pathways for robotic manipulation. In _Conference on Robot Learning_ , pages 894–906. PMLR, 2022. 

- [84] Chan Hee Song, Jiaman Wu, Clayton Washington, Brian M Sadler, Wei-Lun Chao, and Yu Su. Llmplanner: Few-shot grounded planning for embodied agents with large language models. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 2998–3009, 2023. 

- [85] Weijie Su, Xizhou Zhu, Yue Cao, Bin Li, Lewei Lu, Furu Wei, and Jifeng Dai. Vl-bert: Pre-training of generic visual-linguistic representations. _arXiv preprint arXiv:1908.08530_ , 2019. 

- [86] Quan Sun, Yuxin Fang, Ledell Wu, Xinlong Wang, and Yue Cao. Eva-clip: Improved training techniques for clip at scale. _arXiv preprint arXiv:2303.15389_ , 2023. 

- [87] Quan Sun, Qiying Yu, Yufeng Cui, Fan Zhang, Xiaosong Zhang, Yueze Wang, Hongcheng Gao, Jingjing Liu, Tiejun Huang, and Xinlong Wang. Generative pretraining in multimodality. _arXiv preprint arXiv:2307.05222_ , 2023. 

- [88] Markku Suomalainen, Yiannis Karayiannidis, and Ville Kyrki. A survey of robot manipulation in contact. _Robotics and Autonomous Systems_ , 156:104224, 2022. 

- [89] Hao Tan and Mohit Bansal. Lxmert: Learning crossmodality encoder representations from transformers. In _Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)_ , pages 5100–5111, 2019. 

- [90] Hao Tan, Licheng Yu, and Mohit Bansal. Learning to navigate unseen environments: Back translation with environmental dropout. In _Proceedings of NAACL-HLT_ , pages 2610–2621, 2019. 

- [91] Jesse Thomason, Michael Murray, Maya Cakmak, and Luke Zettlemoyer. Vision-and-dialog navigation. In _Conference on Robot Learning_ , pages 394–406, 2020. 

- [92] Yao-Hung Hubert Tsai, Vansh Dhar, Jialu Li, Bowen Zhang, and Jian Zhang. Multimodal large language model for visual navigation. _arXiv preprint_ 

_arXiv:2310.08669_ , 2023. 

- [93] Arun Balajee Vasudevan, Dengxin Dai, and Luc Van Gool. Talk2nav: Long-range vision-and-language navigation with dual attention and spatial memory. _International Journal of Computer Vision_ , 129:246–266, 2021. 

- [94] H. J. Austin Wang and Karthik Narasimhan. Grounding language to entities and dynamics for generalization in reinforcement learning. _ArXiv_ , abs/2101.07393, 2021. 

- [95] Xin Wang, Qiuyuan Huang, Asli Celikyilmaz, Jianfeng Gao, Dinghan Shen, Yuan-Fang Wang, William Yang Wang, and Lei Zhang. Reinforced cross-modal matching and self-supervised imitation learning for visionlanguage navigation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 6629–6638, 2019. 

- [96] Yi Wang, Yinan He, Yizhuo Li, Kunchang Li, Jiashuo Yu, Xin Ma, Xinyuan Chen, Yaohui Wang, Ping Luo, Ziwei Liu, Yali Wang, Limin Wang, and Yu Qiao. Internvid: A large-scale video-text dataset for multimodal understanding and generation. _arXiv preprint arXiv:2307.06942_ , 2023. 

- [97] Zihan Wang, Xiangyang Li, Jiahao Yang, Yeqi Liu, and Shuqiang Jiang. Gridmm: Grid memory map for vision-and-language navigation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 15625–15636, 2023. 

- [98] Zun Wang, Jialu Li, Yicong Hong, Yi Wang, Qi Wu, Mohit Bansal, Stephen Gould, Hao Tan, and Yu Qiao. Scaling data generation in vision-and-language navigation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 12009–12020, 2023. 

- [99] Hongtao Wu, Ya Jing, Chilam Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and Tao Kong. Unleashing large-scale video generative pre-training for visual robot manipulation. _arXiv preprint arXiv:2312.13139_ , 2023. 

- [100] Siying Wu, Xueyang Fu, Feng Wu, and Zheng-Jun Zha. Cross-modal semantic alignment pre-training for visionand-language navigation. In _Proceedings of the 30th ACM International Conference on Multimedia_ , pages 4233–4241, 2022. 

- [101] Chengguang Xu, Hieu T Nguyen, Christopher Amato, and Lawson LS Wong. Vision and language navigation in the real world via online visual language mapping. _arXiv preprint arXiv:2310.10822_ , 2023. 

- [102] Zhengyuan Yang, Linjie Li, Kevin Lin, Jianfeng Wang, Chung-Ching Lin, Zicheng Liu, and Lijuan Wang. The dawn of lmms: Preliminary explorations with gpt-4v (vision). _arXiv preprint arXiv:2309.17421_ , 9(1):1, 2023. 

- [103] Sriram Yenamandra, Arun Ramachandran, Karmesh Yadav, Austin Wang, Mukul Khanna, Theophile Gervet, Tsung-Yen Yang, Vidhi Jain, Alexander William Clegg, 

   - John Turner, et al. Homerobot: Open-vocabulary mobile manipulation. _arXiv preprint arXiv:2306.11565_ , 2023. 

- [104] Andy Zeng, Pete Florence, Jonathan Tompson, Stefan Welker, Jonathan Chien, Maria Attarian, Travis Armstrong, Ivan Krasin, Dan Duong, Vikas Sindhwani, et al. Transporter networks: Rearranging the visual world for robotic manipulation. In _Conference on Robot Learning_ , pages 726–747. PMLR, 2021. 

- [105] Alex Zhang, Khanh Nguyen, Jens Tuyls, Albert Lin, and Karthik Narasimhan. Language-guided world models: A model-based approach to ai control. _ArXiv_ , abs/2402.01695, 2024. 

- [106] Jiazhao Zhang, Chenyang Zhu, Lintao Zheng, and Kai Xu. Rosefusion: random optimization for online dense reconstruction under fast camera motion. _ACM Transactions on Graphics (TOG)_ , 40(4):1–17, 2021. 

- [107] Jiazhao Zhang, Yijie Tang, He Wang, and Kai Xu. Asrodio: Active subspace random optimization based depth inertial odometry. _IEEE Transactions on Robotics_ , 39 (2):1496–1508, 2022. 

- [108] Jiazhao Zhang, Liu Dai, Fanpeng Meng, Qingnan Fan, Xuelin Chen, Kai Xu, and He Wang. 3d-aware object goal navigation via simultaneous exploration and identification. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 6672–6682, 2023. 

- [109] Jiazhao Zhang, Nandiraju Gireesh, Jilong Wang, Xiaomeng Fang, Chaoyi Xu, Weiguang Chen, Liu Dai, and He Wang. Gamma: Graspability-aware mobile manipulation policy learning based on online grasping pose fusion. _arXiv preprint arXiv:2309.15459_ , 2023. 

- [110] Lvmin Zhang, Anyi Rao, and Maneesh Agrawala. Adding conditional control to text-to-image diffusion models. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 3836–3847, 2023. 

- [111] Qilong Zhang and Robert Pless. Extrinsic calibration of a camera and laser range finder (improves camera calibration). In _2004 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)(IEEE Cat. No. 04CH37566)_ , volume 3, pages 2301–2306. IEEE, 2004. 

- [112] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 

- [113] Duo Zheng, Shijia Huang, Lin Zhao, Yiwu Zhong, and Liwei Wang. Towards learning a generalist model for embodied navigation. _arXiv preprint arXiv:2312.02010_ , 2023. 

- [114] Gengze Zhou, Yicong Hong, and Qi Wu. Navgpt: Explicit reasoning in vision-and-language navigation with large language models. _arXiv preprint arXiv:2305.16986_ , 2023. 

