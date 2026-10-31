---
title: "GeoAAC: Geometry-Based Adaptive Action Chunking from Denoising Trajectories in VLA Policies"
date: "2026-09-17"
authors: "Xin Chen; Sen Chen; Yujuan Ding; Jian Liu; Guoqing Wang; Wei Ye"
url: https://arxiv.org/abs/2609.20776
pdf: https://arxiv.org/pdf/2609.20776
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2609.20776)** / [論文ページ](https://arxiv.org/abs/2609.20776)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **GeoAAC: Geometry-Based Adaptive Action Chunking from Denoising Trajectories in VLA Policies** 

Xin Chen<sup>1</sup> Sen Chen<sup>1</sup> Yujuan Ding<sup>2</sup> Jian Liu<sup>1</sup> Guoqing Wang<sup>3</sup> Wei Ye<sup>1</sup> Heng Tao Shen<sup>1</sup> Yi Bin<sup>1†</sup> 

> 1Tongji University 2The Hong Kong Polytechnic University 

> 3University of Electronic Science and Technology of China 

**_Abstract_ — Action chunking is widely used for action generation and execution in Vision-Language-Action (VLA) policies, yet existing approaches commonly use a fixed action horizon. During a rollout, different task stages may require different levels of action continuity, control precision, and closed-loop feedback, making a fixed horizon unable to accommodate changing control requirements. We propose GeoAAC, a geometry-based adaptive action chunking method for flow-based VLA policies that adjusts the action horizon according to the reliability of the current action prediction. We show that the geometry of Flow Matching denoising trajectories provides processlevel information for characterizing prediction reliability, with geometric variation across action prefixes remaining positively correlated with predictive uncertainty. GeoAAC uses this prefixwise geometry to construct a horizon-wise geometric profile and adaptively determine the action horizon from a single generation without additional training. Experiments with GR00T N1.5 and** _π_ 0 _._ 5 **on LIBERO, LIBERO-Pro, RoboCasa365, and realworld manipulation tasks show consistent improvements over fixed-action-horizon baselines and existing adaptive methods, including up to 8.7 percentage points in simulation and an increase in average real-world success rate from 53.3% to 74.4%.** 

## I. INTRODUCTION 

Action chunking has become a widely adopted actiongeneration and execution strategy in Vision-Language-Action (VLA) policies, which leverage large-scale robotic data and pretrained vision-language representations to generalize across tasks, environments, and embodiments [1], [2], [3], [4], [5], [6], [7], [8], [9]. Rather than predicting a single control command at each step, action chunking predicts a sequence of future actions, capturing temporal dependencies and improving motion continuity [10], [11], [12], [13]. 

Applying action chunking requires specifying the _action horizon_ , i.e., the number of predicted actions executed before the policy observes and replans. The action horizon governs the trade-off between action continuity and closedloop responsiveness: shorter horizons enable more frequent feedback and correction but require more frequent policy inference, whereas longer horizons preserve motion continuity at the cost of extended open-loop execution [11], [12], [14], [15], [16]. Most existing VLA policies use a fixed action horizon during deployment [5], [6], [17]. In practice, however, the appropriate horizon is inherently taskand stage-dependent, as different tasks and stages require 


Fig. 1: **Stage-dependent action horizon requirements.** A representative OpenDrawer rollout in RoboCasa. Fixed-2 misidentifies the table edge as the handle during search; Fixed-12 localizes the handle but fails during subsequent grasping and pulling; Fixed-16 executes a long open-loop segment while approaching the handle and ultimately misses the grasp. GeoAAC instead adjusts its action horizon as the rollout progresses. 

different levels of action continuity, control precision, and closed-loop feedback. Consequently, a fixed horizon may suit certain stages while compromising others [18], [19], [20], [21], [22]. As illustrated in Fig. 1, representative fixed action horizons fail at different stages of the same manipulation task, highlighting the need to adapt the action horizon as control requirements change throughout a rollout. 

To address the limitations of fixed action horizons, recent studies have explored adaptive action chunking, which adjusts the action horizon throughout a rollout to enable timely observation and replanning when the current action prediction becomes less reliable. Some approaches train additional horizon predictors or horizon-specific policies to select the execution boundary from the current observation or task state [19], [18], but require additional data, supervision, or optimization. Training-free methods instead seek measurable 

> †Corresponding author. 

proxies from the current policy inference to characterize how reliably the predicted action chunk can be executed and thereby determine the action horizon [20], [22], [21]. One representative approach estimates predictive uncertainty from multiple stochastic action predictions using action entropy and uses it to guide action horizon selection [20]. While such uncertainty estimates indicate prediction reliability, robot action distributions are often multimodal, where multiple distinct action sequences can all represent valid behaviors under the same observation. As a result, outputlevel discrepancies among sampled predictions may reflect diversity across valid action modes rather than unreliability of the current prediction itself. This motivates us to examine whether the action-generation process itself contains richer reliability information that can better support action horizon selection. 

Recent VLA policies employ Flow Matching for continuous action generation [5], [6], [23]. Flow Matching progressively transports initial noise toward the final action output through a sequence of intermediate velocity predictions [24]. These intermediate predictions capture how the current action prediction is progressively updated and refined throughout the generation process. Prior studies have analyzed this process from a geometric perspective and shown that variations in the velocity field and the resulting trajectory geometry can reflect predictive uncertainty [25], [26], [27]: smaller geometric variations correspond to more consistent generative dynamics, whereas larger variations indicate stronger internal adjustments to the current prediction. Accordingly, denoising-trajectory geometry provides process-level information that can more directly characterize the reliability of the current prediction. Building on this observation, we analyze the denoising-trajectory geometry across different action prefixes and find that prefix-wise geometric variation remains positively correlated with predictive uncertainty, as shown in Fig. 3. This indicates that Flow Matching geometry provides reliability-related information along the action horizon. 

Based on the above observations, we propose **GeoAAC** , a geometry-based adaptive action chunking method for flowbased VLA policies, as illustrated in Fig. 2. By examining how denoising-trajectory geometry evolves across action prefixes, GeoAAC characterizes how the reliability of the current action prediction changes along the action horizon and uses this information to determine an appropriate execution boundary. Specifically, we first extract local geometric variations for different action prefixes from a single Flow Matching generation. Since the relationship between geometric variation and predictive uncertainty differs across denoising stages, we apply temporal correction and aggregate the stage-wise information into a horizon-wise geometric profile. GeoAAC then determines the execution boundary from the relative growth and cumulative trend of this profile along the action horizon, enabling adaptive action horizon selection according to the reliability of the current prediction without additional training. We evaluate GeoAAC across multiple flow-based VLA policies and robot 

manipulation benchmarks. On LIBERO, GeoAAC achieves average success rates of 95.5% and 98.0% with GR00T N1.5 and _π_ 0 _._ 5, respectively, while outperforming the best fixedaction-horizon baselines by 8.7 and 5.3 percentage points on RoboCasa365 and LIBERO-Pro, respectively. Across three real-world manipulation tasks, GeoAAC further improves the average success rate from 53.3% with fixed-action-horizon execution to 74.4%. 

Our contributions are summarized as follows: 

- We analyze Flow Matching denoising-trajectory geometry across action prefixes and show that prefix-wise geometric variation remains positively correlated with predictive uncertainty, revealing denoising geometry as a process-level signal of the reliability of the current action prediction along the action horizon. 

- We propose **GeoAAC** , a geometry-based adaptive action chunking method that aggregates temporally corrected prefix-wise denoising geometry into a horizon-wise geometric profile and selects the action horizon from its cumulative relative growth. GeoAAC enables adaptive action horizon selection from a single Flow Matching generation without additional training. 

- We evaluate GeoAAC with two flow-based VLA policies across three simulation benchmarks and real-world manipulation tasks. GeoAAC consistently outperforms fixed-action-horizon baselines and the compared adaptive action chunking methods. 

## II. RELATED WORK 

## _A. Adaptive Action Chunking_ 

Action chunking is widely used in modern robot policies to generate and execute sequences of future actions [10], [11], [13], [5], [14], [17]. While most approaches use a fixed action horizon, recent studies have explored adaptive action chunking to adjust the action horizon according to the current state or action prediction [12], [20], [22], [21]. 

Some approaches train additional horizon predictors or horizon-specific policies to learn suitable action horizons [19], [18], but require additional data, supervision, or optimization. Training-free methods instead mainly rely on signals available during inference [12], [20], [22], [21]. For example, predictive uncertainty can be estimated from statistics over stochastic action predictions and used to guide action horizon selection [20]. While informative, such signals provide relatively indirect estimates of the reliability of candidate action horizons. GeoAAC instead exploits the geometry inherent in the Flow Matching action-generation process, providing a process-level reliability signal for action horizon selection. 

## _B. Flow Matching and Denoising Geometry_ 

Flow Matching has been widely adopted for continuous action generation in VLA policies, where a continuous velocity field progressively transports initial noise toward robot actions [5], [6], [23], [24]. It has also been explored for efficient and continuous robot control [16], [14]. 


Fig. 2: **Overview of GeoAAC.** GeoAAC uses the geometry of Flow Matching denoising trajectories to characterize the reliability of different action prefixes and adapt the action horizon accordingly. 

Prior work has studied the structure of Flow Matching trajectories from several perspectives. Rectified Flow analyzes the geometry and straightness of transport trajectories [25], while other studies investigate how coupling strategies affect trajectory structure and sampling behavior [26]. More recent work has linked denoising-trajectory geometry to predictive uncertainty [27]. Building on these observations, we study denoising-trajectory geometry across action prefixes in flowbased VLA policies and use its prefix-wise structure to guide adaptive action horizon selection. 

## III. METHODS 

## _A. Preliminaries: Flow Matching and Prefix-Wise Geometry_ 

For Vision–Language–Action (VLA) policies equipped with a Flow Matching action head, action chunks are generated by transporting samples from a noise distribution toward the conditional action distribution through a time-dependent vector field [24]. Given the current observation _o_ , the action state **x** _τ_ evolves over flow time _τ ∈_ [0 _,_ 1] according to 


where **v** _θ_ denotes the learned conditional velocity field. Integrating Eq. (1) produces an action chunk **A** = ( **a** 1 _,_ **a** 2 _,...,_ **a** _H_ ), where _H_ denotes the prediction horizon. During numerical integration, the Flow Matching action head evaluates the velocity field at a sequence of integration steps, yielding intermediate velocity predictions _{_ **v**<sup>(</sup><sup>_t_)</sup> _}t_<sup>_T_</sup> =<sup>_−_</sup> 0<sup>1</sup> that characterize the evolution of the denoising trajectory. 

For adaptive action chunking, each action prefix **A** 1: _k_ = ( **a** 1 _,...,_ **a** _k_ ), _k ∈{_ 1 _,..., H}_ , corresponds to a candidate action horizon. The intermediate velocity predictions can therefore 

be restricted to the same prefix, denoted by **v**<sup>(</sup> 1:<sup>_t_)</sup> _k_<sup>.Thispro-</sup> vides a prefix-wise representation of the denoising trajectory across candidate action horizons. 

Prior work has linked geometric properties of Flow Matching denoising trajectories to predictive uncertainty [27]. We examine whether this relationship also holds across action prefixes, since adaptive action horizon selection requires reliability information for different candidate action horizons. To this end, we consider an uncorrected prefix-wise geometric measure _Uk_ , formally defined in Eq. (3), and compare it with a reference predictive uncertainty _Rk_ . 

Using GR00T N1.5, we collect 200 observations from the four LIBERO suites. For each observation, we independently generate 32 stochastic action chunks with _H_ = 16. The leaveone-out prefix variance obtained from repeated sampling serves as the reference uncertainty _Rk_ . As shown in Fig. 3, _Uk_ remains positively correlated with _Rk_ across action prefix lengths. This result indicates that the relationship between denoising-trajectory geometry and predictive uncertainty persists at the prefix level, providing empirical support for using prefix-wise geometry to characterize the reliability of candidate action horizons. 

## _B. Geometric Features of the Denoising Trajectory_ 

Building on the prefix-wise geometric relationship established above, we construct a horizon-wise geometric profile from the intermediate velocity predictions produced during Flow Matching inference. For an action prefix of length _k_ , let _τt_ denote the flow time at the _t_ -th integration step and ∆ _τt_ = _|τt_ +1 _− τt |_ . We characterize the local geometry of the denoising trajectory through the change between consecutive 


Fig. 3: **Correlation between prefix-wise denoising geometry and reference predictive uncertainty.** Prefix-wise denoising geometry remains positively correlated with reference predictive uncertainty across action prefix lengths. Shaded regions denote 95% confidence intervals, and the red dashed line indicates _ρ_ = 0 _._ 5 for reference. 

velocity predictions: 


where _ε >_ 0 is a small constant for numerical stability. Here, **v**<sup>(</sup><sup>_t_)</sup> 1: _k_<sup>denotesthevelocitypredictionforthefirst</sup><sup>_k_actionsat</sup> the _t_ -th denoising step. The difference between consecutive velocity predictions captures local geometric variation along flow time, while normalization by ∆ _τt_ accounts for nonuniform integration intervals. Computing _b_<sup>(</sup> _k_<sup>_t_)</sup> across denoising steps and action prefixes retains both temporal variation along the denoising trajectory and prefix-wise variation across candidate action horizons. 

The uncorrected prefix-wise geometric measure used in Sec. III-A is obtained by aggregating these local variations: 


The factor _T_ normalizes the denominator with respect to the average velocity magnitude across denoising steps. As shown in Sec. III-A, _Uk_ remains positively correlated with the reference predictive uncertainty _Rk_ across action prefixes. However, the reliability of the underlying geometric variations is not uniform across denoising stages. 

Using the same experimental setup as above, Fig. 4(a) shows that local geometric variation increases toward later denoising stages, whereas its correlation with the reference uncertainty _Rk_ decreases after the intermediate stages. Thus, larger geometric variations at later stages do not necessarily provide more reliable uncertainty information. We therefore account for stage-wise reliability when aggregating the local geometric variations. 

Motivated by the reliability pattern in Fig. 4(a), we introduce a position-dependent temporal weight for each denois- 

ing transition. Let _st_ = _t/T_ denote the normalized generation progress at the _t_ -th denoising step, and let _s_ ¯ _t_ = ( _st_ + _st_ +1) _/_ 2 denote the midpoint of the _t_ -th transition. We define 


This weighting function emphasizes intermediate denoising stages while reducing contributions from early and late stages. The quadratic decay as _st_ approaches 1 suppresses late-stage variations more strongly than early-stage ones, consistent with their lower reliability in Fig. 4(a). Mean normalization keeps the average weight equal to one without changing the overall scale. As shown in Fig. 4(b), temporal correction improves the correlation between the geometric measure and reference uncertainty across action prefixes. 

We then aggregate the temporally corrected local variations and normalize them by the velocity magnitude of the corresponding action prefix: 


The velocity-magnitude normalization reduces dependence on the overall velocity scale, allowing _U_<sup>�</sup> _k_ to reflect relative geometric variation rather than the magnitude of the velocity predictions. 

Applying Eq. (5) to all candidate action prefixes yields the horizon-wise geometric profile 


This profile describes how denoising geometry evolves as the action prefix expands and serves as the input to adaptive action horizon selection. 

## _C. Adaptive Action Horizon Selection_ 

Given the horizon-wise geometric profile **U**<sup>�</sup> , we determine the execution boundary and thereby the action horizon of the current prediction. The absolute scale of **U**<sup>�</sup> can vary across observations, tasks, and generated action chunks, making a fixed threshold difficult to calibrate across settings. Moreover, local changes in the profile may contain transient fluctuations. We therefore determine the execution boundary from relative geometric growth and its cumulative distribution across candidate action horizons. 

We first measure the relative geometric growth between adjacent action prefixes: 


Unlike absolute differences, _rk_ measures the proportional geometric change introduced by extending the action prefix and is therefore less sensitive to variations in signal scale. We retain only positive geometric growth: 


Fig. 4: **Temporal correction of denoising geometry. (a)** Local geometric variation increases toward late denoising stages, while its correlation with reference uncertainty decreases. **(b)** Temporal correction improves the correlation with reference uncertainty across action prefixes. Shaded regions denote 95% confidence intervals. 

We define the geometry-based execution boundary at the median of this cumulative distribution, i.e., where _Fk_ reaches 0 _._ 5. This criterion depends on the distribution of relative growth rather than the absolute scale of **U**<sup>�</sup> , avoiding scalespecific threshold calibration while reducing sensitivity to individual local extrema. When _Fk <_ 0 _._ 5 _< Fk_ +1, we obtain a continuous boundary estimate by linear interpolation: 


Rounding _k_<sup>ˆ</sup> 50 to the nearest action step gives _k_ 50. If _Fk_ = 0 _._ 5, we set _k_ 50 = _k_ . If no positive geometric growth is observed, the profile provides no evidence for early truncation, and we set _k_ 50 = _H_ . 

We further apply a motion-aware lower bound as a safeguard against excessively short action horizons when the predicted motion is small. In this regime, executing only a few low-magnitude actions may produce little state change while triggering another policy inference. Let _M_ ( **A** ) denote the overall motion magnitude of the predicted action chunk, measured from its translational and rotational components, and let _α >_ 0 denote a fixed reference scale. We define 


and the corresponding minimum action horizon as 


Larger predicted motion permits a shorter minimum action horizon, whereas smaller motion retains a longer minimum action horizon. Here, _k_ min is a fixed minimum action horizon parameter, and both _α_ and _k_ min are fixed across tasks. The final action horizon is 


The policy executes the first _k_<sup>_∗_</sup> predicted actions before acquiring a new observation and replanning, resulting in adaptive closed-loop execution. 

## IV. EXPERIMENTS 

A positive _rk_ indicates increased geometric variation when the candidate action horizon is extended, whereas negative growth provides no evidence for an earlier execution boundary. Retaining only positive growth also prevents such decreases from canceling boundary evidence accumulated at preceding prefixes. 

Rather than selecting the largest local response, which can be dominated by a transient peak, we accumulate the positive geometric growth along the action horizon. When ∑<sup>_H_</sup> _j_ =2<sup>_ej >_</sup> 0, we define 


with _F_ 1 = 0. The resulting _Fk_ forms a normalized cumulative distribution of positive geometric growth. Isolated responses contribute only a fraction of the total evidence, whereas persistent growth accumulates across neighboring prefixes. 

## _A. Experimental Settings_ 

**Models.** We evaluate two flow-based VLA policies, GR00T N1.5 [23] and _π_ 0 _._ 5 [6]. For GR00T N1.5, we set the prediction horizon to _H_ = 16, with 8 denoising steps on LIBERO and 4 on RoboCasa365. For _π_ 0 _._ 5, we use a prediction horizon of _H_ = 10 and 10 denoising steps on LIBERO-Pro. 

**Benchmarks.** We evaluate on LIBERO [28], RoboCasa365 [29], and LIBERO-Pro [30]. On LIBERO, we use all 40 tasks from the Spatial, Object, Goal, and LIBERO10 suites, covering spatial-relation reasoning, object-centric manipulation, goal-conditioned manipulation, and longerhorizon multi-stage tasks, with 50 rollouts per task. On RoboCasa365, we evaluate 18 single-skill manipulation tasks from the target/atomic ~~s~~ een split, including pick-andplace, articulated-object manipulation, and appliance interaction, also with 50 rollouts per task. On LIBERO-Pro, 

TABLE I: Success rates (%) on LIBERO under different action chunking strategies with GR00T N1.5 and _π_ 0 _._ 5. 

|Method|Spatial|Long|Object|Goal|Avg.|
|---|---|---|---|---|---|
|GR00T (_h_=2)|95.0|79.0|93.6|93.0|90.2|
|GR00T (_h_=4)|95.8|82.6|97.0|94.4|92.5|
|GR00T (_h_=8)|95.0|88.4|97.4|**97.8**|94.7|
|GR00T (_h_=12)|95.6|88.2|97.2|97.0|94.5|
|GR00T (_h_=16)|95.0|88.2|97.0|96.0|94.1|
|GR00T+MS|**97.2**|88.0|96.6|96.4|94.6|
|GR00T+SA|96.2|87.4|95.8|95.8|93.8|
|GR00T+GeoAAC|96.4|**89.2**|**99.0**|97.2|**95.5**|
|_π_0_._5 (_h_=5)|98.5|93.2|**98.8**|98.0|97.1|
|_π_0_._5+MS|98.8|94.4|96.6|**98.8**|97.2|
|_π_0_._5+SA|**99.0**|93.2|98.0|98.2|97.1|
|_π_0_._5+GeoAAC|98.6|**96.4**|98.6|98.4|**98.0**|


TABLE II: Success rates (%) on LIBERO-Pro under different position-shift settings with _π_ 0 _._ 5. 

|Method|Shift-0.2|Shift-0.3|Shift-0.4|Avg.|
|---|---|---|---|---|
|_π_0_._5 (_h_=5)|53.2|29.9|9.5|30.9|
|_π_0_._5+SA|57.5|34.3|9.5|33.8|
|_π_0_._5+MS|57.4|35.5|**12.8**|35.2|
|_π_0_._5+GeoAAC|**58.5**|**37.6**|12.4|**36.2**|


we evaluate 10 LIBERO-Object tasks under three levels of position perturbation, Shift-0.2, Shift-0.3, and Shift-0.4, to assess robustness under spatial distribution shifts. 

**Baselines.** We compare with fixed action horizons and two adaptive baselines: multi-sampling-based (MS) [20], which selects action horizons from multiple stochastic action predictions, and self-attention-based (SA) [22], which uses internal action self-attention for action horizon selection. 

## _B. Simulation_ 

**LIBERO.** Table I reports the success rates of different action chunking strategies on LIBERO. With GR00T N1.5, GeoAAC achieves the highest average success rate of 95.5%, outperforming the best fixed-action-horizon baseline, fixed-8 (94.7%), as well as MS (94.6%) and SA (93.8%). GeoAAC also achieves the best performance on the Object and Long suites, reaching 99.0% and 89.2%, respectively. These results show that adaptive action horizon selection improves the overall task performance of GR00T N1.5. 

To analyze how GeoAAC responds to different action primitives, we examine the action horizons selected for different local motion patterns. As shown in Fig. 5, Align and Place/release, which require relatively precise pose control and frequent closed-loop correction, have shorter average action horizons of 7.94 and 7.77, respectively. In contrast, Transport, Push/pull, and Turn exhibit longer average action horizons of 9.56, 9.19, and 10.52, respectively, corresponding to more continuous translational motion, contact-constrained motion, and rotational manipulation. Reach has an average action horizon of 8.30, close to the fixed-8 baseline. These results show that GeoAAC does not apply a uniform action horizon across action primitives, but instead adapts the 


Fig. 5: **Adaptive action horizon selection across action primitives.** Each point denotes the average action horizon of one action primitive within an episode, and the dashed line marks fixed-8, the best fixed-action-horizon baseline. Different action primitives exhibit distinct action-horizon preferences: continuous motions favor longer horizons, while goal-proximal alignment and placement favor shorter horizons. 

action horizon to local motion characteristics, using shorter horizons for alignment and placement while maintaining longer horizons for continuous transport, contact motion, and rotation. 

We further evaluate GeoAAC with _π_ 0 _._ 5 to examine its applicability across different flow-based VLA policies. GeoAAC achieves an average success rate of 98.0%, compared with 97.1% for fixed-5 and 97.2% for MS. On the Long suite, GeoAAC improves the success rate from 93.2% with fixed-5 to 96.4%. These results show that the performance advantage of GeoAAC generalizes across different flowbased VLA policies. 

**LIBERO-Pro.** We further evaluate GeoAAC on LIBEROPro [30] under three position-perturbation settings: Shift-0.2, Shift-0.3, and Shift-0.4. 

Table II reports the success rates on LIBERO-Pro. GeoAAC achieves the highest average success rate of 36.2%, outperforming the fixed-action-horizon baseline by 5.3 percentage points and also surpassing the self-attention-based (SA) [22] and multi-sampling-based (MS) [20] adaptive baselines. Under Shift-0.2 and Shift-0.3, GeoAAC reaches 58.5% and 37.6%, respectively, while remaining competitive under the stronger Shift-0.4 perturbation. These results show that GeoAAC maintains its advantage under changes in object-position distribution by adapting the action horizon to the current prediction. 

**RoboCasa365.** We further evaluate GeoAAC on RoboCasa365 [29] to assess its performance under more diverse household manipulation scenarios. Table III reports the success rates of different action chunking strategies. 

With GR00T N1.5 [23], GeoAAC achieves the highest average success rate of 75.1%. It outperforms the best fixedaction-horizon baseline by 8.7 percentage points and exceeds the adaptive baselines MS [20] and SA [22] by 4.0 and 6.2 percentage points, respectively. GeoAAC also achieves or ties the best performance on 9 of the 18 tasks. These results show that GeoAAC maintains a consistent performance 

TABLE III: Success rates (%) on RoboCasa365 under different action chunking strategies with GR00T N1.5. 

|Task|GeoAAC|Fixed-2|Fixed-4|Fixed-8|Fixed-12|Fixed-16|MS|SA|
|---|---|---|---|---|---|---|---|---|
|CloseBlenderLid|36.0|8.0|14.0|28.0|36.0|**40.0**|34.0|38.0|
|CloseFridge|80.0|38.0|42.0|56.0|68.0|78.0|58.0|**84.0**|
|CloseToasterOvenDoor|**90.0**|44.0|56.0|78.0|**90.0**|82.0|80.0|86.0|
|CoffeeSetupMug|70.0|20.0|34.0|62.0|62.0|70.0|60.0|**72.0**|
|NavigateKitchen|**68.0**|16.0|26.0|40.0|50.0|62.0|64.0|42.0|
|OpenCabinet|92.0|50.0|72.0|88.0|92.0|84.0|92.0|**94.0**|
|OpenDrawer|**94.0**|20.0|32.0|60.0|76.0|70.0|78.0|82.0|
|OpenStandMixerHead|92.0|62.0|80.0|86.0|94.0|**96.0**|94.0|94.0|
|PickPlaceCounterToCabinet|**68.0**|48.0|46.0|52.0|54.0|60.0|**68.0**|**68.0**|
|PickPlaceCounterToStove|**84.0**|48.0|62.0|78.0|74.0|72.0|82.0|76.0|
|PickPlaceDrawerToCounter|54.0|10.0|22.0|44.0|32.0|38.0|**58.0**|46.0|
|PickPlaceSinkToCounter|76.0|36.0|64.0|56.0|80.0|72.0|**84.0**|76.0|
|PickPlaceToasterToCounter|72.0|24.0|46.0|68.0|84.0|62.0|**86.0**|70.0|
|SlideDishwasherRack|**80.0**|50.0|56.0|68.0|68.0|78.0|**80.0**|74.0|
|TurnOffStove|**56.0**|10.0|24.0|30.0|48.0|46.0|24.0|42.0|
|TurnOnElectricKettle|**90.0**|34.0|48.0|62.0|62.0|72.0|78.0|82.0|
|TurnOnMicrowave|**78.0**|12.0|26.0|60.0|64.0|60.0|**78.0**|60.0|
|TurnOnSinkFaucet|72.0|12.0|34.0|40.0|62.0|50.0|**82.0**|54.0|
|Overall|**75.1**|30.1|43.6|58.7|66.4|66.2|71.1|68.9|


TABLE IV: Success rates (%) on real-world manipulation tasks. Each method is evaluated over 30 trials per task. 

|Method|Extinguish|Disconnect|Uncap|Avg.|
|---|---|---|---|---|
|Fixed-50|16.7|76.7|66.7|53.3|
|GeoAAC|**36.7**|**100.0**|**86.7**|**74.4**|


advantage across diverse household manipulation scenarios. 

## _C. Real-World Experiments_ 

**Setup and Tasks.** We further evaluate GeoAAC on a real-world dual-arm manipulation platform consisting of two PiperX robotic arms and three Intel RealSense D435i cameras, providing one third-person view and two wristmounted views. The base policy is a flow-based VLA policy built on a Qwen3-VL-2B-Instruct vision-language backbone with a Flow Matching action expert. At each inference, the policy predicts an action chunk with a prediction horizon of _H_ = 50, while the robot is controlled at 50 Hz. 

As shown in Fig. 6, we consider three manipulation tasks with different interaction characteristics: Alcohol Lamp Extinguishing, Rubber Tube Disconnection, and Test-Tube Uncapping. We collect 50 teleoperated demonstrations per task, resulting in 150 real-world trajectories for training. Fixed-50 and GeoAAC use the same policy checkpoint and differ only in their action horizon. Fixed-50 executes the full 50-step action chunk, whereas GeoAAC adaptively determines the execution boundary using the denoising-trajectory geometry from the same Flow Matching generation. Each method is evaluated over 30 trials per task, resulting in 180 trials in total. 

**Results.** As shown in Table IV, GeoAAC improves the success rate across all three tasks, increasing the average success rate from 53.3% to 74.4%, an absolute improvement of 21.1 percentage points. On Rubber Tube Disconnection, 


Fig. 6: **Real-world manipulation experiments.** GeoAAC and Fixed-50 are evaluated on alcohol lamp extinguishing, rubber tube disconnection, and test-tube uncapping. Fixed50 fails due to cap misalignment in the first task and incorrect object grasping in the third task, while successfully completing rubber tube disconnection. 

GeoAAC achieves 100.0% success, compared with 76.7% for Fixed-50. Since both settings use the same policy parameters and training data, these results show that adapting the action horizon alone improves overall real-world performance. 

Qualitative observations further highlight the benefit of adaptive action horizon selection during stages requiring precise closed-loop adjustment. In Test-Tube Uncapping, Fixed- 

50 is more prone to empty grasps or grasping the wrong target, whereas GeoAAC acquires updated observations more frequently during grasping and uncapping. In Rubber Tube Disconnection, GeoAAC also adjusts the gripper and wrist pose when approaching the target, making execution less sensitive to variations in the initial robot configuration. These observations are consistent with the varying need for closedloop feedback across manipulation stages. 

## V. CONCLUSION 

We presented **GeoAAC** , a geometry-based adaptive action chunking method for flow-based VLA policies. GeoAAC exploits the prefix-wise geometry of Flow Matching denoising trajectories from a single action generation process and constructs a horizon-wise geometric profile to characterize reliability-related variations along the predicted action sequence. Based on the relative growth and cumulative distribution of this profile, GeoAAC adaptively determines the execution boundary without additional training. Experiments with GR00T N1.5 and _π_ 0 _._ 5 across LIBERO, LIBEROPro, and RoboCasa365 demonstrate consistent improvements over fixed-action-horizon and adaptive baselines. Real-world experiments further validate the effectiveness of GeoAAC, improving the average success rate from 53.3% with Fixed50 to 74.4% across three manipulation tasks. 

Our current approach focuses on geometric information available within the Flow Matching action-generation process for action horizon adaptation. Future work could further investigate when task-relevant information should be acquired and incorporated during robot execution, extending adaptive action horizon selection toward more flexible closed-loop interaction. 

## REFERENCES 

- [1] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu _et al._ , “Rt-1: Robotics transformer for real-world control at scale,” in _Proceedings of Robotics: Science and Systems_ , 2023. 

- [2] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Proceedings of The 7th Conference on Robot Learning_ , 2023, pp. 2165–2183. 

- [3] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong _et al._ , “Openvla: An open-source vision-language-action model,” in _Proceedings of The 8th Conference on Robot Learning_ , 2025, pp. 2679–2713. 

- [4] O. Mees, D. Ghosh, K. Pertsch, K. Black, H. R. Walke, S. Dasari, J. Hejna, T. Kreiman, C. Xu, J. Luo _et al._ , “Octo: An open-source generalist robot policy,” in _First Workshop on Vision-Language Models for Navigation and Manipulation at ICRA 2024_ , 2024. 

- [5] K. Black, N. Brown, D. Driess, A. Esmail, M. R. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ 0: A visionlanguage-action flow model for general robot control,” in _Proceedings of Robotics: Science and Systems_ , 2025. 

- [6] K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. R. Equi, C. Finn, N. Fusai, M. Y. Galliker _et al._ , “ _π_ 0 _._ 5: A visionlanguage-action model with open-world generalization,” in _Proceedings of The 9th Conference on Robot Learning_ , vol. 305, 2025, pp. 17–40. 

- [7] D. Qu, H. Song, Q. Chen, Y. Yao, X. Ye, J. Gu, Z. Wang, Y. Ding, B. Zhao, D. Wang, and X. Li, “SpatialVLA: Exploring Spatial Representations for Visual-Language-Action Models,” in _Proceedings of Robotics: Science and Systems_ , 2025. 

- [8] Q. Bu, Y. Yang, J. Cai, S. Gao, G. Ren, M. Yao, P. Luo, and H. Li, “Learning to Act Anywhere with Task-centric Latent Actions,” in _Proceedings of Robotics: Science and Systems_ , 2025. 

- [9] Y. Fan, S. Bai, X. Tong, P. Ding, Y. Zhu, H. Lu, F. Dai, W. Zhao, Y. Liu, S. Huang, Z. Fan, B. Chen, and D. Wang, “Long-vla: Unleashing long-horizon capability of vision language action model for robot manipulation,” in _Proceedings of The 9th Conference on Robot Learning_ , vol. 305, 2025, pp. 2018–2037. 

- [10] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” in _arXiv preprint arXiv:2304.13705_ , 2023. 

- [11] C. Chi, S. Feng, Y. Du, Z. Xu, E. Cousineau, B. C. M. Burchfiel, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” in _Proceedings of Robotics: Science and Systems_ , 2023. 

- [12] Y. Liu, J. Ibn Hamid, A. Xie, Y. Lee, M. Du, and C. Finn, “Bidirectional decoding: Improving action chunking via guided test-time sampling,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [13] A. C.-W. Lee, I. Chuang, L.-Y. Chen, and I. Soltani, “Interact: Inter-dependency aware action chunking with hierarchical attention transformers for bimanual manipulation,” in _Proceedings of The 8th Conference on Robot Learning_ , vol. 270, 2025, pp. 1730–1743. 

- [14] K. Black, M. Y. Galliker, and S. Levine, “Real-time execution of action chunking flow policies,” in _Advances in Neural Information Processing Systems_ , 2025. 

- [15] H. Xue, J. Ren, W. Chen, G. Zhang, Y. Fang, G. Gu, H. Xu, and C. Lu, “Reactive diffusion policy: Slow-fast visual-tactile policy learning for contact-rich manipulation,” in _Proceedings of Robotics: Science and Systems_ , 2025. 

- [16] S. Jiang, X. Fang, N. Roy, T. Lozano-P´erez, L. P. Kaelbling, and S. Ancha, “Streaming flow policy: Simplifying diffusion/flowmatching policies by treating action trajectories as flow trajectories,” in _Proceedings of The 9th Conference on Robot Learning_ , vol. 305, 2025, pp. 238–257. 

- [17] M. J. Kim, C. Finn, and P. Liang, “Fine-tuning vision-language-action models: Optimizing speed and success,” in _Proceedings of Robotics: Science and Systems_ , 2025. 

- [18] L. Jing, Y. Qin, H. Wang, and H. Xu, “Mixture of horizons for efficient robot learning,” in _Proceedings of The 9th Conference on Robot Learning_ , 2025. 

- [19] Z. Zhao, T. Guo, Z. Zhang, Y. Liu, and Y. Zhu, “Dynamic execution horizon prediction for chunk-based robot policies,” _arXiv preprint arXiv:2602.21445_ , 2026. 

- [20] Y. Liang, X. Wang, K. Wang, S. Wang, X. Peng, H. Chen, D. K. H. Chua, and P. Vadakkepat, “Adaptive action chunking at inference-time for vision-language-action models,” _arXiv preprint arXiv:2604.04161_ , 2026. 

- [21] J. Nie, J. Li, J. Zhang, J. Lao, C. Liu, T. Zhang, L. Lin, and S. Huang, “Pace: Phase-aware chunk execution for robot policies with action chunking,” _arXiv preprint arXiv:2606.00537_ , 2026. 

- [22] H. Wang, G. Zhang, Y. Yan, R. R. Kompella, and G. Liu, “Vla knows its limits: Adaptive execution horizons for robot policies,” in _European Conference on Computer Vision_ , 2026. 

- [23] J. Bjorck, V. Blukis, F. Casta˜neda, N. Cherniadev _et al._ , “GR00T N1.5: An improved open foundation model for generalist humanoid robots,” NVIDIA Research, 2025. [Online]. Available: https://research.nvidia.com/labs/gear/gr00t-n1 ~~5~~ / 

- [24] Y. Lipman, R. T. Q. Chen, H. Ben-Hamu, M. Nickel, and M. Le, “Flow matching for generative modeling,” in _International Conference on Learning Representations_ , 2023. 

- [25] X. Liu, C. Gong, and Q. Liu, “Flow straight and fast: Learning to generate and transfer data with rectified flow,” _International Conference on Learning Representations_ , 2023. 

- [26] A.-A. Pooladian, H. Ben-Hamu, C. Domingo-Enrich, B. Amos, Y. Lipman, and R. T. Q. Chen, “Multisample flow matching: Straightening flows with minibatch couplings,” in _Proceedings of the 40th International Conference on Machine Learning_ , vol. 202, 2023, pp. 28 100– 28 127. 

- [27] A. Rao _et al._ , “The geometry of flow matching uncertainty: A costfree uncertainty proxy and its application in flow-based vla failure detection,” _arXiv preprint_ , 2026. 

- [28] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “LIBERO: Benchmarking knowledge transfer for lifelong robot learning,” in _Advances in Neural Information Processing Systems_ , vol. 36, 2023, pp. 44 776–44 791. 

- [29] S. Nasiriany, S. Nasiriany, A. Maddukuri, and Y. Zhu, “Robocasa365: A large-scale simulation framework for training and benchmarking generalist robots,” in _International Conference on Learning Representations_ , 2026. 

- [30] X. Zhou, Y. Xu, G. Tie, Y. Chen, G. Zhang, D. Chu, P. Zhou, and L. Sun, “LIBERO-PRO: Towards robust and fair evaluation of vision-language-action models beyond memorization,” _arXiv preprint arXiv:2510.03827_ , 2025. 

