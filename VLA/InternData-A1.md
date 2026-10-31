---
title: "InternData-A1: Pioneering High-Fidelity Synthetic Data for Pre-training Generalist Policy"
date: "2025-11-20"
authors: "Yang Tian; Yuyin Yang; Yiman Xie; Zetao Cai; Xu Shi; Ning Gao"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2511.16651
pdf: https://arxiv.org/pdf/2511.16651
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.16651)** / [論文ページ](https://arxiv.org/abs/2511.16651)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **InternData-A1: Pioneering High-Fidelity Synthetic Data for Pre-training Generalist Policy** 

Yang Tian<sup>* 1,2</sup> Yuyin Yang<sup>* 3,2</sup> Yiman Xie<sup>* 4,2</sup> Zetao Cai<sup>* 5,2</sup> Xu Shi<sup>* 6,2</sup> Ning Gao<sup>2</sup> Hangxu Liu<sup>3,2</sup> Xuekun Jiang<sup>2</sup> Zherui Qiu<sup>2</sup> Feng Yuan<sup>2</sup> Yaping Li<sup>5,2</sup> Ping Wang<sup>1</sup> Junhao Cai<sup>2</sup> Jia Zeng<sup>_†_2</sup> Hao Dong<sup>_†_1</sup> Jiangmiao Pang<sup>_†_2</sup> 1 Peking University 2 Shanghai AI Laboratory 3 Fudan University 4 Zhejiang University 5 Chinese University of Hong Kong 6 Shanghai Jiao Tong University 


Figure 1. **InternData-A1** pioneers a large-scale, high-fidelity synthetic dataset with physically faithful, photorealistic rendering, diverse object domains (rigid, articulated, fluid, and deformable), extensive multi-skill tasks, and broad cross-embodiment coverage. 

## **Abstract** 

_Recent work explores how real and synthetic data contribute to VLA model generalization. While the π-series model has shown the strong effectiveness of large-scale real-robot pre-training, synthetic data has not previously demonstrated comparable capability at scale. This paper provides the first evidence that synthetic data alone can match the performance of the strongest π-dataset in pretraining a VLA model, revealing the substantial value of large-scale simulation. The resulting model also exhibits_ 

*: Equal contributions. _†_ : Equal corresponding author 

_surprisingly zero-shot sim-to-real transfer on several challenging tasks. Our synthetic dataset, InternData-A1, contains over 630k trajectories and 7,433 hours across 4 embodiments, 18 skills, 70 tasks, and 227 scenes, covering rigid, articulated, deformable, and fluid-object manipulation. It is generated through a highly autonomous, fully decoupled, and compositional simulation pipeline that enables flexible task assembly, long-horizon skill composition, and heterogeneous embodiments with minimal manual tuning. Using the same architecture as π_ 0 _, we pre-train a model entirely on InternData-A1 and find that it matches the official π_ 0 _across 49 simulation tasks, 5 real-world tasks, and 4 long-horizon dexterous tasks. We will open-source_ 

976 

Table 1. **Comparison to existing simulation datasets.** 

|Dataset|Traj.|Skill|Task|Scene|Embodiment|Fluid|Deformable|Failure Recovery|Open-Source|Collection|
|---|---|---|---|---|---|---|---|---|---|---|
|MimicGen [28]|50k|-|18|1|4|✗|✗|✗|✓|Teleoperation & Augmentation|
|ManiSkill2 [17]|30k|20|20|-|1|✗|✗|✗|✓|TAMP & MPC & RL|
|RLBench [20]|2.7k|-|100|1|1|✗|✗|✗|✓|Waypoints & Motion Planners|
|LIBERO [27]|5k|-|130|20|1|✗|✗|✗|✓|Teleoperation|
|CALVIN [29]|37.5k|-|34|4|1|✗|✗|✗|✓|Teleoperation|
|RoboCasa [30]|77k|8|100|120|2|✗|✗|✗|✓|Teleoperation & Augmentation|
|GraspVLA [14]|10M|1|1|1|1|✗|✗|✗|✗|Autonomous|
|RoboTwin 2.0 [10]|100k|-|50|1|5|✗|✗|✗|✓|Autonomous|
|InternVLA-M1 [11]|244k|2|1|1|1|✗|✗|✗|✓|Autonomous|
|**InternData-A1**|630k|18|70|227|4|✓|✓|✓|✓|Autonomous|


_both the dataset and the generation pipeline to broaden access to large-scale robotic data and to lower the barrier to scalable data creation for embodied AI research._ 

## **1. Introduction** 

Manipulation lies at the core of embodied intelligence, enabling robots to assist in daily tasks and deliver real economic value. Recent advancements [2, 3, 5, 19, 25] demonstrate that large-scale real-robot data can endow VisionLanguage-Action (VLA) models with strong generalization across tasks, scenes, and embodiments. However, collecting real data at such scale is resource-intensive: teleoperation demands skilled operators, specialized hardware, and extensive human labor, making large, diverse real datasets infeasible for most research groups. As a result, the broader community lacks the ability to systematically study the data requirements that underpin successful VLA pre-training. 

Simulation offers a promising complementary avenue: its rich asset libraries, controllable scenes, and automated data generation pipelines create the possibility of scaling manipulation data far beyond what is practical with real robots. Yet existing simulated datasets [10, 11, 14, 28, 30] still cover narrow skill sets (primarily pick-and-place), focus mainly on rigid objects, require nontrivial human operation, and rarely validate their effectiveness for large-scale VLA pre-training. This leaves an open question: can highfidelity synthetic data, when scaled sufficiently in embodiments, scenes, skills, and physical realism, match the pretraining effectiveness of the strongest real-world datasets? 

As depicted in Fig. 1 and Tab. 1 , we introduce InternData-A1, a high-fidelity synthetic manipulation dataset comprising 630k trajectories and 7,433 hours across 4 embodiments, 18 skills, 70 tasks, and 227 scenes, covering rigid, articulated, deformable, and fluid-object interactions. InternData-A1 is generated through a fully decoupled, autonomous simulation pipeline that separates asset specification, skill policies, task composition, and rendering. Each task is built by retrieving embodiments, scenes, and objects from an asset library, then composing scripted 

skill policies that compute and interpolate trajectories conditioned on robot and object states into complete behaviors. This compositional design flexibly supports bimanual manipulation, multi-robot coordination, and extended multi-stage tasks, while automatically generating objectlevel annotations, domain randomization, and collisionaware motion plans. With engineering optimizations, the pipeline produces 209.7 hours robot data per day on 8 RTX 4090 GPUs with minimal manual tuning and a cost below 0.003 US Dollars per episode, enabling scalable synthesis of physically and visually faithful demonstrations. This pipeline underpins the broad task diversity of InternDataA1 and enables systematic VLA validation through largescale pre-training and sim-to-real evaluation. 

We demonstrate that a _π_ 0 model pre-trained exclusively on InternData-A1 achieves comparable performance to the official _π_ 0 trained on the closed-source _π_ -dataset across diverse real-world scenarios, including regular, long-horizon, and dexterous manipulations. This result, for the first time, establishes that large simulation-only data can match the strongest real-world data for VLA pre-training. Across 49 simulation, 5 real-world, and 4 long-horizon dexterous tasks, the synthetic-pretrained model closely matches the official _π_ 0 model. Furthermore, compared with existing open-source datasets [5, 30, 31], models pre-trained on InternData-A1 consistently outperform counterparts in both simulated and real-world evaluations, highlighting the strength of InternData-A1 for VLA pre-training. 

In addition, ten selected simulated tasks achieve direct sim-to-real transfer with an average success rate exceeding 50%. Further analysis on four representative tasks reveals that, under well-aligned sim-to-real settings, fewer than 1,600 simulated samples can match the performance of 200 real samples, highlighting the high fidelity of InternData-A1 and its minimal sim-to-real gap. 

In conclusion, while the _π_ -dataset remains closedsource, InternData-A1 and its entire generation pipeline are fully open and reproducible in simulation. We wish this work to offer an accessible supplement to embodied AI research and enable a deeper understanding of data scaling 

977 


Figure 2. **Data Statistics.** InternData-A1 provides 4 single or dual-arm embodiments, 70 diverse tasks, 3185 rigid objects, 321 aritculation objects, 20 garments, and 227 rooms. All these elements consist 630k episodes, 401.4M frames and 7433.9 hours. 

effects in robot learning. 

## **2. Related Works** 

**Large-scale Robot Datasets.** Existing large-scale robot datasets fall into two categories: simulation-based [17, 20, 29] and real-world datasets [21, 35]. Simulation enables controllable variation in embodiments, scenes, and objects, and supports both teleoperation-based augmentation [30] and automated pipelines [11, 14]. However, teleoperation still requires substantial manual effort, and most automated systems mainly target picking tasks. RoboTwin 2.0 [10] recently expanded simulation to bimanual manipulation with cross-embodiment diversity and domain randomization. Real-world datasets [3, 5, 23, 31, 37] offer high-fidelity demonstrations without simulation gaps, but are costly to scale and typically exhibit narrow embodiment coverage, limited scene diversity, or variable data quality. The _π_ -series datasets [3] demonstrate that large-scale realrobot pre-training can yield strong generalization across tasks, scenes, and embodiments, highlighting the importance of scale and diversity for VLA models. In contrast to prior simulation datasets and complementary to real-world efforts, InternData-A1 provides broad task diversity, heterogeneous embodiments, photorealistic rendering, and longhorizon multi-skill trajectories, enabling systematic study of large-scale synthetic data pre-training for VLA models. 

**VLA Models.** The generalization capability and performance of VLA models are primarily determined by the scale, diversity, and source of their pre-training data. Existing approaches fall into three broad categories. (1) Realdata–only models [3, 4, 7, 8, 24, 40, 43] achieve strong indomain performance [3] but remain tied to specific training 

environments, often exhibiting limited open-world generalization [6, 34]. (2) Simulation-only models [14] benefit from massive synthetic trajectories and extensive domain randomization, but typically cover narrow skill families (e.g., grasping), constraining their applicability. (3) Hybrid models combine simulation and real demonstrations [2, 11] or incorporate web-scale VQA data [19, 32, 39, 41] to improve grounding and long-horizon planning. In this work, we leverage InternData-A1 to provide VLA models with stronger action priors and generalization ability, achieving downstream performance on par with state-of-the-art real data despite the inherent physics and visual gaps of simulation. Accordingly, we adopt the _π_ 0 model and its underlying _π_ -dataset as our primary baselines. 

## **3. Data Statistics** 

In this section, we elaborate on the data statistics from three aspects: embodiments, tasks, and assets, with the overall scale and diversity visualized in Fig. 2. **Embodiments.** InternData-A1 includes four types of robotic embodiments: **Genie-1** , one of the most widely used dual-arm robots in large-scale real robot data collection factories [5], accounts for 7.9%. **Franka Emika Panda** , one of the most common single-arm manipulators in research laboratories, constitutes 23.3%. We fix Franka on a table to perform tabletop manipulation tasks, including both regular and long-horizon scenarios. **AgileX Split Aloha** equipped with Piper-100 arms, and **ARX Lift-2** equipped with R5a arms, are two popular embodiments in current VLA [3, 19, 42] real-world deployments, occupying 30.8% and 37.8%, respectively. These wheeled dual-arm systems enable rich bimanual manipulation, including sequential skills (e.g., make a sandwich) and parallel behaviors (e.g., fold shirts) across diverse scenes. 

978 


Figure 3. **Data synthesis pipeline of InternData-A1.** It consists of four stages: (1) environment construction with selected embodiments, scenes, and objects; (2) task composition using modular atomic skills invoked via simple configuration commands; (3) domain randomization over layouts, object poses, lighting, etc.; and (4) trajectory generation, where CuRobo [33] interpolates dense joint actions, validates them through physics simulation, and renders only successful trajectories into the LeRobot format. 

**Tasks.** To ensure both trajectory- and task-level diversity, InternData-A1 is constructed from a comprehensive set of manipulation primitives spanning nearly all fundamental human-like skills—from folding and pouring to rotating and stacking. By composing these primitives, we design 70 diverse tasks across realistic scenarios, including 4 fluidrelated, 4 deformable-object, 15 articulated, and 47 rigidobject tasks. Notably, unlike prior works [10, 20, 29, 30], our tasks are not defined by simply varying manipulated objects (e.g., picking hundreds of objects still counts as one task in our statistics). Each task instead specifies a distinct context, composition of atomic skills, and action-space constraint. InternData-A1 also includes 18 long-horizon tasks, each involving at least three sequential skills, totaling 124,789 trajectories and 141,421,619 frames. Beyond diversity, we ensured balance by proportionally mixing data from different tasks, resulting in 56 of the 70 tasks containing between 1,000 and 10,000 trajectories, approaching a near-uniform task distribution. 

**Assets.** We provide **3,185 rigid objects** from 107 categories, sourced from OmniObject3D [38] and Objaverse [13]. We aggregate articulated objects from multiple sources, including GAPartNet [16], GenSim2 [18], Infinite Mobility [26], ArtVIP [22], and GRUtopia [36]. In total, this results in **321 articulated objects** across 14 cat- 

egories, ranging from small items such as cartons to large household appliances like refrigerators. For garment assets, we use the EinScan Rigel Pro scanner to digitize **20 real garments** (short-sleeve shirts, sweaters, shorts, and towels). Regarding the environments, InternData-A1 contains **227 indoor scenes** (kitchens, study rooms, dining rooms, and living rooms), forming a diverse and realistic layout setup. All these scenes are acquired and segmented from the GRScenes-100 dataset in GRUtopia [36]. 

## **4. Data Synthesis** 

In this section, we outline the data synthesis pipeline of InternData-A1: we first describe environment construction (embodiments, scenes, and objects) (Sec 4.1), then detail how skills are composed into full tasks (Sec 4.2), and finally explain the domain randomization (Sec. 4.3), generation, and storage procedures (Sec. 4.4). 

### **4.1. Environment Construction** 

As illustrated in Fig. 3, given a task description template, we first retrieve task-relevant assets from the library, including robots, scenes, and objects. The robot asset is a stable USD-type embodiment that has been verified for consistent contact dynamics in robot–object interactions. The scene asset is a room-level environment, selected and segmented 

979 

from GRUtopia [36]. Each scene is annotated with detailed manipulation-area metadata, enabling natural and contextaware task construction. Our object library spans **rigid** , **articulated** , **deformable** , and **fluid** categories. Rigid objects include physical attributes, canonical poses, and automatically generated grasp poses following AnyGrasp [15]. Articulated objects are annotated with accurate joint axes, part poses, and physical parameters (e.g., damping, stiffness) for stable interaction. Deformable assets are remeshed garments with material and contact properties, simulated using Vertex Block Descent [9] for realistic behavior. Fluid objects are modeled with particle-based dynamics, where particles are adaptively generated within containers, and liquid surfaces reconstructed via isosurface rendering with diverse PBD materials. All functional annotations are managed through a unified interface, enabling easy asset configuration with high physical fidelity. 

### **4.2. Skill Composition** 

Once the environments are prepared, users compose tasks by selecting atomic skills from the skill library. Each skill is a modular scripted policy that takes object states (poses, joint states), robot states (base and end-effector poses), and user-defined constraints as inputs, and outputs a sequence of waypoints (target end-effector 6D poses). Waypoints serve as a unified representation, cleanly decoupling high-level skill logic from low-level motion execution. For example, the _Pick_ skill filters grasp candidates for the target object and computes the pre-grasp, grasp, and post-grasp poses, while the articulation-related _Push_ skill uses contact annotations to determine pre-contact, contact, and post-contact waypoints. For tasks with special spatial constraints, we provide a set of constraint options for each skill. For instance, in the task _Insert Flower In Vase_ , it requires the stem to remain upright. Users could specify the displacement and rotation between the placed object and container in _Place_ skill. All these well-engineered skills can be invoked through simple command templates in a configuration file (see Fig. 3). Since each skill is designed as an automatic state-waypoint mapping, no additional cost is required when varying objects, spatial ranges, scenes or even embodiments. The only manual effort required is pure adjustment of spatial ranges. Users simply specify which arm (left or right) to use for each skill and organize them sequentially or in parallel for bimanual tasks, then a long-horizon task unfolds smoothly and systematically. 

### **4.3. Domain Randomization** 

To enrich visual diversity, we perturb the primary and wrist cameras views within _±_ 5<sup>_◦_</sup> rotations and _±_ 5 cm translations. We construct a library of 174 environment maps, each with randomized light temperature and intensity to simulate diverse natural illumination conditions. Target ob- 

jects can be replaced with others from the same category, while the tabletop and background layouts are also randomized. To further enhance trajectory diversity, object positions and orientations are sampled within task-specific spatial ranges. For manipulation functions, we introduce additional randomness to the contact regions. For instance, our autonomous grasp pose generation pipeline produces millions of grasp candidates; after filtering, the final grasp pose is randomly selected from the top 40 high-confidence candidates following [15]. For articulated and deformable objects, such as microwaves or garments, we expand the contact region into a neighborhood area and sample the contact points randomly. 

### **4.4. Generation & Storage** 

After all preparations, we employ the CuRobo motion planner [33] to interpolate dense joint-space actions between the waypoints generated by each skill. For each trial, the simulator executes physics simulation to follow the dense actions without rendering. Once a trajectory is successfully planned, it is replayed with the rendering engine enabled. Since rendering is substantially more time-consuming than physics simulation during episode synthesis, this decoupled design effectively avoids wasting computation on failed planning attempts, especially for dexterous or long-horizon tasks. For each complete robot episode, we record object metadata, language instructions, multi-view RGB images and camera parameters, as well as robot proprioceptive states and action control labels. Users can also easily store additional information, such as depth maps, grounding annotations, and bounding boxes, with simple configuration options during recording. All final data are converted into the standard LeRobot format for VLA pre-training. 


Figure 4. **Real-world setup.** We evaluate the model pre-trained on InternData-A1 against the _π_ -dataset baseline on a suite of nine real-world tasks spanning three robots. 

980 

Table 2. **Comparison to** _π_ **-dataset in simulations.** _π_ 0 model pre-trained on InternData-A1 outperforms the official _π_ 0 model by 5% and 6.5% across 49 tasks in easy and hard settings respectively, showing the effectiveness of InternData-A1. 


Figure 5. **Comparison to** _π_ **-dataset in real-world tasks.** InternData-A1 achieves performance comparable to _π_ -dataset across 9 realworld tasks, including 4 dexterous ones, demonstrating its strong pre-training capability. 

## **5. Pre-training Effects** 

In this section, we address the central question of whether InternData-A1 can match the real-robot dataset in its capacity to pre-train VLA models. 

### **5.1. Comparison with** _π_ **-dataset** 

**Experimental Setup.** We benchmark against the strongest real-robot data, _π_ -dataset. We adopt the same architecture as _π_ 0 model, which consists of a vision-language model (Paligemma [1]) and a flow-matching-based action expert. We pre-train a new _π_ 0 model, initialized with Paligemma weights and a scratched action expert, solely on InternDataA1, and compare it with the official _π_ 0 checkpoint trained on _π_ -dataset across downstream tasks. This comparison reflects the impact of pre-training data quality and provides the fairest available solution, as _π_ -dataset remains fully closed-source. For simulation evaluation, we use 49 bimanual tasks from RoboTwin 2.0 [10] under two difficulty modes: _Easy_ (clean) and _Hard_ (cluttered). We report average success rates over 100 trials across two checkpoints. For real-world evaluation, we test on three embodiments: Genie-1, ARX Lift-2 and ARX AC One. We design five regular and four dexterous tasks covering articulated manipulation, garment folding, contact-rich control, precision grasping, and long-horizon sequences. Each task is evaluated over 30 trials. In the following results, we use _π_ 0 _(Scratch)_ to denote the model without being pre-trained, _π_ 0 for the official checkpoint, and _π_ 0 _(InternData-A1)_ for the model trained exclusively on our dataset. **Evaluating in Simulation.** Tab. 2 summarizes the re- 

sults over 49 tasks and 19,600 rollouts. Under an identical post-training process, models pre-trained on InternDataA1 consistently outperform those trained on the _π_ -dataset, achieving 6% higher success rates in the _Easy_ mode and 5% higher in the _Hard_ mode. The improvement in hard settings (clean expert demonstrations and domain-randomized evaluation) indicates that the robustness to visual and spatial variations gained from InternData-A1’s extensive domain randomization persists even when downstream fine-tuning uses only clean, non-randomized data. Moreover, since InternData-A1 consists of diverse tasks freely composed from repeated atomic skills across varied contexts, we believe it provides a transferable and broader action prior for downstream tasks sharing similar skill components. This is evidenced by the six representative tasks in Tab. 2, which demand robust combinations of pick, place, move, handover, and articulation-related skills. Overall, InternDataA1 improves over _Paligemma_ by 36.5% in _Easy_ and 24.0% in _Hard_ mode, demonstrating the strong pre-training effectiveness of InternData-A1. 

**Evaluating over Regular Tasks.** We first compare InternData-A1 and _π_ -dataset on five representative realworld base tasks across two embodiments, covering articulation ( _Heat Sandwich_ ), basic pick-and-place ( _Sort Rubbish_ , _Place Markpen_ ), human–robot interaction ( _Pass Bottle_ ), and tool use ( _Sweep Trash_ ). Across both in-distribution and out-of-distribution tasks, InternData-A1 consistently outperforms _π_ -dataset by a 6.2% margin. In particular, consistent with superior performance on RoboTwin, the rich basic skill trajectories in InternData-A1 (e.g., pick, place, 

981 

Table 3. **Comparison to open-source data in downstream tasks.** 

|Dataset|Domain|49 Sim|Tasks|2 Real|Tasks|
|---|---|---|---|---|---|
|||Easy|Hard|Sort Rubbish|Pass Bottle|
|OXE [31]|Real|32.5%|11.0%|40.0%|36.7%|
|Agibot World [5]|Real|52.5%|12.0%|53.3%|56.7%|
|RoboCasa [30]|Sim|50.0%|11.0%|23.3%|13.3%|
|**InternData-A1**|**Sim**|**60.0%**|**26.5%**|**90.0%**|**60.0%**|


and move) promote performance on tasks composed mainly of these skills (e.g., _Place Markpen_ and _Pass Bottle_ ). These results send an encouraging message: although simulations inevitably differ from real-world dynamics, many manipulation tasks exhibit natural robustness, as robotic hardware tolerates minor control inaccuracies, VLA models learn abstract visuomotor representations, and many tasks allow for approximate contact strategies. Consequently, large-scale simulated data can still provide transferable inductive priors for real-world manipulation. 

**Evaluating over Dexterous Tasks.** We further evaluate the pretrained policy on four long-horizon dexterous tasks—folding garments, sorting industrial parts, unscrewing bottle caps, and zipping bag, directly challenging the core strengths of the official _π_ 0 model. To ensure fair evaluation, we introduce a new embodiment, ARX AC One, which is unseen in both InternData-A1 and _π_ -dataset. Despite the presence of novel objects, skills, and embodiments, InternData-A1 achieves performance comparable to _π_ -dataset, as shown in the right panel of Fig. 5. We suppose that, beyond the comprehensive coverage of atomic skills in InternData-A1 as discussed earlier, the substantial proportion of long-horizon tasks further enables the VLA model to explore a broader action space and develop continuous control abilities, which can then be effectively transferred to novel tasks and embodiments. 

### **5.2. Benchmarking against open-source datasets** 

We further compare InternData-A1 with previous opensource datasets, including two real-world datasets OXE [31] and Agibot World [5], and one simulation dataset, RoboCasa [30]. Due to resource constraints, we pre-train the _π_ 0 model exclusively on each dataset for 500k iterations and evaluate performance on 49 simulated tasks and 2 realworld tasks. As shown in Tab. 3, InternData-A1 demonstrates clear advantages across both simulation and real domains. In regard to RoboCasa [30], while the RoboCasa demonstrates competitive performance in simulation evaluations, trailing InternData-A1 by only 10%, its performance significantly drops in real-robot evaluation. In these real-world evaluations, InternData-A1 achieves an average improvement of 57.7% over RoboCasa. We attribute this significant gain to InternData-A1 ’s highly photorealistic rendering and abundant data amounts. Together with the comparison against the closed-source _π_ -dataset, these results further validate the effectiveness of InternData-A1 as 


Figure 6. **Sim-to-real experimental setup.** 10 randomly selected simulated tasks are evaluated for direct sim-to-real transfer. 


Figure 7. **Performance across different simulation data scales.** Pure simulation data from InternData-A1 can match real-data performance with comparable or moderately larger sample sizes. 

a strong pre-training source for VLA models. 

## **6. Data Analysis** 

In this section, we aim to address two widely discussed questions regarding large-scale simulation data: (1) How well do the tasks in InternData-A1 transfer from simulation to the real world? (2) Which components of InternData-A1 contribute most to effective pre-training? 

### **6.1. Sim-to-Real Transfer** 

**Pure Simulation versus Pure Real.** We investigate the zero-shot sim-to-real transfer ability on four representative tasks in InternData-A1. Starting from the same _π_ 0 (InternData-A1) checkpoint, we post-train on 200–1,600 simulated episodes and 200 real episodes for each task, and evaluate each resulting policy over 30 rollouts. As shown in Fig. 7, for regular tasks such as _Sort Rubbish_ and _Wipe Stain_ , which mainly involve basic skills (pick, place, move), 200 simulated episodes already achieve per- 

982 


Figure 8. **Additional sim-to-real performance.** 6 tasks involving repeated pick-place, articulation, and bimanual coordination achieve over 50% success rates with only 500 simulated episodes. 

formance comparable to 200 real ones. For more complex tasks such as _Flip Package_ and _Instructional Pick_ , which require dynamic-object manipulation and language grounding, around 1,600 simulated episodes are needed to match real-data performance. In other words, the simulation-toreal data ratio for equivalent performance narrows to within 8:1—and in some cases, even approaches 1:1. Although complex tasks demand more simulated data, our efficient synthesis pipeline achieves this at far lower time and economic costs than real-world collection. Moreover, we find that strong zero-shot sim-to-real performance does not require exact replicas of backgrounds, lighting, object textures, or table layouts. As shown in Fig. 6, coarse alignment is sufficient, as long as camera views and joint action spaces are closely aligned. This robustness arises from InternDataA1 ’s photo-realistic rendering and extensive domain randomization, which narrow the visual gap and enable the policy to ignore irrelevant discrepancies between simulation and real environments. 

**Additional Sim-to-Real Tasks.** To further examine the real-world potential of InternData-A1, we evaluate six additional tasks using 500 simulated episodes post-trained on _π_ 0 (InternData-A1) and tested over 30 rollouts. As shown in Fig. 8, the model achieves 50% success rates in pickand-place tasks ( _Make Sandwich_ , _Pack_ ), 63% and 87% in articulation operations ( _Close Box_ , _Close Microwave_ ), and 60% and 57% in bimanual coordination tasks ( _Sweep_ , _Handover_ ). Together with the four tasks in Fig. 7, ten representative tasks out of seventy achieve high sim-to-real success without any real data — a strong reflection of the data quality and minimal visual–physical gap in InternData-A1. Moreover, InternData-A1 is the first to demonstrate that, beyond single pick tasks as in GraspVLA [14], diverse and complex tasks can also be directly transferred via VLA from simulation to reality. These include multi-skill operations, articulation, bimanual manipulation, and even _Flip Package_ in logistics scenes, which was previously realized using purely real data by the Helix [12] from the Figure Company. These findings highlight the strong potential of large-scale simulation data for VLA deployment in real world. 

Table 4. **Data component ablation results.** 

|Full|w.o. PnP.|w.o. Art.|w.o. Base.|w.o. Long.|
|---|---|---|---|---|
|Easy / Hard|Easy / Hard|Easy / Hard|Easy / Hard|Easy / Hard|
|**58.0% / 25.0%**|57.0% / 22.5%|55.5% / 19.5%|52.5% / 20.5%|54.0% / 19.0%|


### **6.2. Data Component Ablation** 

**What Matters in InternData-A1’s Composition.** To uncover each component’s contribution to pre-training, we divide InternData-A1 into four parts: large-scale pick-andplace tasks (PnP, 30.97%), large-scale articulation manipulation (Art, 11.07%), base tasks involving fewer than three skills beyond simple pick-and-place (Base, 38.16%), and long-horizon tasks containing at least three skills (Long, 19.80%). Due to resource constraints, we pre-train _π_ 0 for 0.5 epoch using both the full dataset and ablated versions (each with one component removed), and evaluate them on RoboTwin 2.0. As shown in Tab. 4, the full-data model achieves the highest success rates, while removing any component causes a clear performance drop, indicating all four components contribute meaningfully. 

Two observations stand out. First, although PnP (30.97 %) and Base (38.16%) dominate the dataset, removing Base or Long tasks leads to a more significant decline than removing PnP. This suggests that for VLA pre-training, datasets composed solely of pick-and-place tasks [11, 14] are insufficient; maintaining task diversity, i.e., multi-skill compositions, is more beneficial for VLA training. Second, excluding articulation tasks, despite their smaller scale and limited object diversity, also yields a larger drop than excluding PnP. We suspect that articulation operations reach a more diverse action space, especially some extreme cases, as they are often influenced by diverse joint geometries and distorted arm configurations (e.g., pushing a distant drawer). At a higher level, combined these two findings, we hypothesize that **trajectory diversity** may serve as the core drive of effective pre-training. We leave a rigorous investigation for future research. 

## **7. Conclusion and Limitation** 

This paper introduces InternData-A1, a large-scale, highfidelity synthetic dataset for robotic manipulation. Using this dataset, we demonstrate for the first time that pretraining a Vision-Language-Action (VLA) model exclusively on synthetic data can match the performance of the leading VLA model, revealing the substantial potential of large-scale simulation. By open-sourcing the dataset and its generation pipeline, we aim to lower the barrier to largescale robotic data access for the embodied AI community. **Limitation.** Due to the limitations of physics simulators, it is challenging to simulate highly dexterous tasks, such as tying shoelaces or threading a needle. Future work will expand the dataset’s task diversity and dexterity. 

983 

## **8. Acknowledgements** 

This work is supported by the National Key R&D Program of China (2022ZD0160201) and Shanghai Artificial Intelligence Laboratory. 

## **References** 

- [1] Lucas Beyer, Andreas Steiner, André Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. In <u>ArXiv, 2024.</u> 6 

- [2] Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. In <u>ArXiv,</u> 2025. 2, 3 

- [3] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-languageaction flow model for general robot control. In <u>RSS,</u> 2024. 2, 3 

- [4] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. In <u>ArXiv, 2022.</u> 3 

- [5] Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xuan Hu, Xu Huang, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. In <u>IROS, 2025.</u> 2, 3, 7 

- [6] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. In <u>RSS, 2025.</u> 3 

- [7] Chilam Cheang, Sijin Chen, Zhongren Cui, Yingdong Hu, Liqun Huang, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Xiao Ma, et al. Gr-3 technical report. In <u>ArXiv, 2025.</u> 3 

- [8] Chi-Lam Cheang, Guangzeng Chen, Ya Jing, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Hongtao Wu, Jiafeng Xu, Yichu Yang, et al. Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation. In <u>ArXiv, 2024.</u> 3 

- [9] Anka He Chen, Ziheng Liu, Yin Yang, and Cem Yuksel. Vertex block descent. In <u>TOG, 2024.</u> 5 

- [10] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. In <u>ArXiv, 2025.</u> 2, 3, 4, 6 

- [11] Xinyi Chen, Yilun Chen, Yanwei Fu, Ning Gao, Jiaya Jia, Weiyang Jin, Hao Li, Yao Mu, Jiangmiao Pang, Yu Qiao, et al. Internvla-m1: A spatially guided vision-languageaction framework for generalist robot policy. In <u>ArXiv, 2025.</u> 2, 3, 8 

- [12] Can Cui, Pengxiang Ding, Wenxuan Song, Shuanghao Bai, Xinyang Tong, Zirui Ge, Runze Suo, Wanqi Zhou, Yang Liu, Bofang Jia, et al. Openhelix: A short survey, empirical analysis, and open-source dual-system vla model for robotic manipulation. In <u>ArXiv, 2025.</u> 8 

- [13] Matt Deitke, Dustin Schwenk, Jordi Salvador, Luca Weihs, Oscar Michel, Eli VanderBilt, Ludwig Schmidt, Kiana Ehsani, Aniruddha Kembhavi, and Ali Farhadi. Objaverse: A universe of annotated 3d objects. In <u>CVPR, 2023.</u> 4 

- [14] Shengliang Deng, Mi Yan, Songlin Wei, Haixin Ma, Yuxin Yang, Jiayi Chen, Zhiqi Zhang, Taoyu Yang, Xuheng Zhang, Wenhao Zhang, et al. Graspvla: a grasping foundation model pre-trained on billion-scale synthetic action data. In <u>ArXiv,</u> 2024. 2, 3, 8 

- [15] Hao-Shu Fang, Chenxi Wang, Hongjie Fang, Minghao Gou, Jirong Liu, Hengxu Yan, Wenhai Liu, Yichen Xie, and Cewu Lu. Anygrasp: Robust and efficient grasp perception in spatial and temporal domains. In <u>TRO, 2023.</u> 5 

- [16] Haoran Geng, Helin Xu, Chengyang Zhao, Chao Xu, Li Yi, Siyuan Huang, and He Wang. Gapartnet: Cross-category domain-generalizable object perception and manipulation via generalizable and actionable parts. In <u>CVPR, 2023.</u> 4 

- [17] Jiayuan Gu, Fanbo Xiang, Xuanlin Li, Zhan Ling, Xiqiang Liu, Tongzhou Mu, Yihe Tang, Stone Tao, Xinyue Wei, Yunchao Yao, et al. Maniskill2: A unified benchmark for generalizable manipulation skills. In <u>ArXiv, 2023.</u> 2, 3 

- [18] Pu Hua, Minghuan Liu, Annabella Macaluso, Yunfeng Lin, Weinan Zhang, Huazhe Xu, and Lirui Wang. Gensim2: Scaling robot data generation with multi-modal and reasoning llms. In <u>ArXiv, 2024.</u> 4 

- [19] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. In <u>CORL, 2025.</u> 2, 3 

- [20] Stephen James, Zicong Ma, David Rovick Arrojo, and Andrew J Davison. Rlbench: The robot learning benchmark & learning environment. In <u>RAL, 2020.</u> 2, 3, 4 

- [21] Tao Jiang, Tianyuan Yuan, Yicheng Liu, Chenhao Lu, Jianning Cui, Xiao Liu, Shuiqi Cheng, Jiyang Gao, Huazhe Xu, and Hang Zhao. Galaxea open-world dataset and g0 dualsystem vla model. In <u>ArXiv, 2025.</u> 3 

- [22] Zhao Jin, Zhengping Che, Zhen Zhao, Kun Wu, Yuheng Zhang, Yinuo Zhao, Zehui Liu, Qiang Zhang, Xiaozhu Ju, Jing Tian, et al. Artvip: Articulated digital assets of visual realism, modular interaction, and physical fidelity for robot learning. In <u>ArXiv, 2025.</u> 4 

- [23] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. In <u>RSS, 2024.</u> 3 

- [24] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An opensource vision-language-action model. In <u>CORL, 2024.</u> 3 

- [25] Hao Li, Shuai Yang, Yilun Chen, Yang Tian, Xiaoda Yang, Xinyi Chen, Hanqing Wang, Tai Wang, Feng Zhao, Dahua 

984 

Lin, et al. Cronusvla: Transferring latent motion across time for multi-frame prediction in manipulation. In <u>AAAI, 2025.</u> 

   - 2 

- [26] Xinyu Lian, Zichao Yu, Ruiming Liang, Yitong Wang, Li Ray Luo, Kaixu Chen, Yuanzhen Zhou, Qihong Tang, Xudong Xu, Zhaoyang Lyu, et al. Infinite mobility: Scalable high-fidelity synthesis of articulated objects via procedural generation. In <u>ArXiv, 2025.</u> 4 

- [27] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. In <u>NIPS, 2023.</u> 2 

- [28] Ajay Mandlekar, Soroush Nasiriany, Bowen Wen, Iretiayo Akinola, Yashraj Narang, Linxi Fan, Yuke Zhu, and Dieter Fox. Mimicgen: A data generation system for scalable robot learning using human demonstrations. In <u>ArXiv, 2023.</u> 2 

- [29] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. Calvin: A benchmark for languageconditioned policy learning for long-horizon robot manipulation tasks. In <u>RAL, 2022.</u> 2, 3, 4 

- [30] Soroush Nasiriany, Abhiram Maddukuri, Lance Zhang, Adeet Parikh, Aaron Lo, Abhishek Joshi, Ajay Mandlekar, and Yuke Zhu. Robocasa: Large-scale simulation of everyday tasks for generalist robots. In <u>CVPR, 2024.</u> 2, 3, 4, 7 

- [31] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In <u>ICRA, 2024.</u> 2, 3, 7 

et al. Omniobject3d: Large-vocabulary 3d object dataset for realistic perception, reconstruction and generation. In <u>CVPR, 2023.</u> 4 

   - [39] Shuai Yang, Hao Li, Yilun Chen, Bin Wang, Yang Tian, Tai Wang, Hanqing Wang, Feng Zhao, Yiyi Liao, and Jiangmiao Pang. Instructvla: Vision-language-action instruction tuning from understanding to manipulation. In <u>ArXiv, 2025.</u> 3 

   - [40] Yuyin Yang, Zetao Cai, Yang Tian, Jia Zeng, and Jiangmiao Pang. Gripper keypose and object pointflow as interfaces for bimanual robotic manipulation. In <u>RSS, 2025.</u> 3 

   - [41] Andy Zhai, Brae Liu, Bruno Fang, Chalse Cai, Ellie Ma, Ethan Yin, Hao Wang, Hugo Zhou, James Wang, Lights Shi, et al. Igniting vlms toward the embodied space. In <u>ArXiv,</u> 2025. 3 

   - [42] Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, Yuchun Feng, Yinan Zheng, Jiayin Zou, Yilun Chen, Jia Zeng, et al. X-vla: Soft-prompted transformer as scalable cross-embodiment vision-language-action model. In <u>ArXiv, 2025.</u> 3 

   - [43] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In <u>CORL, 2023.</u> 3 

- [32] Delin Qu, Haoming Song, Qizhi Chen, Zhaoqing Chen, Xianqiang Gao, Xinyi Ye, Qi Lv, Modi Shi, Guanghui Ren, Cheng Ruan, et al. Eo-1: Interleaved vision-text-action pretraining for general robot control. In <u>ArXiv, 2025.</u> 3 

- [33] Balakumar Sundaralingam, Siva Kumar Sastry Hari, Adam Fishman, Caelan Garrett, Karl Van Wyk, Valts Blukis, Alexander Millane, Helen Oleynikova, Ankur Handa, Fabio Ramos, Nathan Ratliff, and Dieter Fox. curobo: Parallelized collision-free minimum-jerk robot motion generation, 2023. 4, 5 

- [34] Yang Tian, Sizhe Yang, Jia Zeng, Ping Wang, Dahua Lin, Hao Dong, and Jiangmiao Pang. Predictive inverse dynamics models are scalable learners for robotic manipulation. In <u>ICLR, 2025.</u> 3 

- [35] Homer Rich Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, Philippe Hansen-Estruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, et al. Bridgedata v2: A dataset for robot learning at scale. In <u>CORL, 2023.</u> 3 

- [36] Hanqing Wang, Jiahe Chen, Wensi Huang, Qingwei Ben, Tai Wang, Boyu Mi, Tao Huang, Siheng Zhao, Yilun Chen, Sizhe Yang, et al. Grutopia: Dream general robots in a city at scale. In <u>ArXiv, 2024.</u> 4, 5 

- [37] Kun Wu, Chengkai Hou, Jiaming Liu, Zhengping Che, Xiaozhu Ju, Zhuqin Yang, Meng Li, Yinuo Zhao, Zhiyuan Xu, Guang Yang, et al. Robomind: Benchmark on multiembodiment intelligence normative data for robot manipulation. In <u>RSS, 2024.</u> 3 

- [38] Tong Wu, Jiarui Zhang, Xiao Fu, Yuxin Wang, Jiawei Ren, Liang Pan, Wayne Wu, Lei Yang, Jiaqi Wang, Chen Qian, 

985 

