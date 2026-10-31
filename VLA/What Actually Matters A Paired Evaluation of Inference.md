---
title: "What Actually Matters? A Paired Evaluation of Inference Settings for $π_{0.5}$ on BEHAVIOR-1K"
date: "2026-10-27"
authors: "Ruben Hammele; Samira Huber; Mohammad Nazeri; Amirreza Payandeh; Alexandyr T. Card; Aaron Nguyen"
url: https://arxiv.org/abs/2610.37917
pdf: https://arxiv.org/pdf/2610.37917
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2610.37917)** / [論文ページ](https://arxiv.org/abs/2610.37917)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **What Actually Matters? A Paired Evaluation of Inference Settings for** **_π_** 0 _._ 5 **on BEHAVIOR-1K** 

**Ruben Hammele**<sup>1</sup><sup>_,∗_</sup> **Samira Huber**<sup>1</sup><sup>_,∗_</sup> **Mohammad Nazeri**<sup>2</sup> **Amirreza Payandeh**<sup>2</sup> 

**Alexandyr T. Card**<sup>2</sup> **Aaron Nguyen**<sup>2</sup> **Anuj Pokhrel**<sup>2</sup> **Daeun Song**<sup>3</sup> 

**Xuesu Xiao**<sup>2</sup> **S¨oren Pirk**<sup>1</sup> 

1 VCAI Lab, Kiel University, 2 RobotiXX Lab, George Mason University 

3 AIR Lab, Ewha Womans University 

**Abstract:** Vision-Language-Action (VLA) models offer a promising paradigm for general-purpose household robotics. However, inference and data-collection strategies that have been deployed in smaller-scale settings do not necessarily generalize to large-scale, diverse task suites. To address this gap, we conduct a systematic, paired evaluation of previously proposed inference and data-collection strategies across all 100 tasks. Our evaluation uses a fine-tuned _π_ 0 _._ 5 model based on the 2025 BEHAVIOR Challenge winner, which achieves a Q-score of 0.39 on the public test set. These results show that proposed strategies do not transfer uniformly to new environments and tasks. Project page, videos, and detailed analysis: rubenhammele.github.io/behavior2026 

## **1 Introduction** 

VLA performance depends not only on learned parameters but also on inference and data-collection strategies. Inference strategies are often adopted from prior fine-tuning pipelines, yet their effectiveness beyond the original evaluation settings remains unclear. The inference strategies of the winner of the BEHAVIOR Challenge 2025 [1], Larchenko et al. [2], remain understudied. Other approaches investigate advantage guidance and rollout optimization in the context of garment folding [3], while industrial reports evaluate _π_ 0 _._ 5 fine-tuning and inference settings on a single real-world manufacturing task [4]. The extent to which these strategies generalize across diverse household tasks therefore remains an open question. 

We systematically evaluate proposed inference and data-collection strategies using a fine-tuned _π_ 0 _._ 5 model across 4 instances of all 100 tasks of BEHAVIOR-1K [1]. Halving the number of actions executed per prediction decreases Q-score by 0.16, potentially causing consecutive chunks to pursue different strategies. The inherited 1 _._ 3 _×_ playback speed-up remains beneficial, likely because it fits more of each task into the time budget. Reducing denoising from twenty steps to one causes no detectable loss, suggesting that a single step already lands close to its mode. For data collection, snapshot-based restarts reduce simulation-step consumption by 29–43%, since retries resume near the failure point instead of re-simulating already completed stages from the initial state. 

## **2 Experimental Setup** 

**Training** Our policy is initialized from the pre-trained _π_ 0 _._ 5 checkpoint introduced by Larchenko et al. [2]. The policy is fully fine-tuned on the BEHAVIOR-1K dataset. Training then continues in a loop in which the current checkpoint collects rollouts on training instances, and the (partial) successful rollouts are mixed with the demonstrations for further training. Each training frame carries a binary advantage label for RECAP-style conditioning [5]. 

*Equal contribution 

Table 1: Inference ablations relative to baseline. Table 2: Data collection ablations. 

|Setting|Base.|Tested|∆_Q_|∆SR|∆Steps|Sig.|Comparison|∆_Q_|∆SR|Steps|
|---|---|---|---|---|---|---|---|---|---|---|
|Actions/chunk<br>Speed-up|26<br>1_._3_×_|13<br>30<br>1_×_|_−_0_._16_±_0_._03<br>_−_0_._01_±_0_._02<br>_−_0_._04_±_0_._02|_−_11<br>0<br>_−_4|+752<br>_−_53<br>+433|Yes<br>No<br>Yes|_Restart point (Baseline: _<br>Before first drop|_fresh start)_<br>+0_._076_±_0_._028|+0_._3_±_2_._5|_−_29%<br>|
|||2_×_|_−_0_._03_±_0_._02|_−_2|_−_135|No|Before last progress|+0_._059_±_0_._023|_−_3_._1_±_2_._1|_−_38%|
|Denoising|20|10<br>1|_−_0_._02_±_0_._02<br>+0_._01_±_0_._02|_−_1<br>1|+7<br>_−_23|No<br>No|At last progress|+0_._056_±_0_._021|_−_3_._4_±_2_._3|_−_43%|
|Inpainting|On|Off|<br>_−_0_._02_±_0_._02|_−_2|_−_7|No|_Modified restore vs. full_|_i    restore_|||
|Guidance_β_|1|2<br>4|_−_0_._03_±_0_._02<br>_−_0_._00_±_0_._02|_−_4<br>0|+333<br>+42|Yes<br>No|_i_<br>Stage belief not restor|_i_<br>ed<br>_−_0_._05_±_0_._02|_−_5_._1_±_2_._3|–|
|Gripper Snap|on|off|_−_0_._03_±_0_._02|_−_5|+326|No|||||
|Rendering|Downsampled|Direct|_−_0_._03_±_0_._02|_−_3|+125|No|||||
|Sampling|Single|Best-Of-4|_−_0_._01_±_0_._02|_−_2|_−_1|No|||||


**Benchmark and Statistical Analysis.** We evaluate all 100 BEHAVIOR-1K tasks on public test instances under official constraints [6]. For each cell, the control is the mean of two independent baseline runs. We assess paired score differences (∆ _Q_ ) using task-clustered bootstrap 95% confidence intervals (CIs), classifying effects as helpful or harmful when the CI excludes zero. 

## **3 Experiments & Results** 

### **3.1 Inference Ablations** 

**Action-Chunk Execution Horizons:** Prior work adopts different action-chunk execution horizons [7, 8], while findings on the benefits of longer execution horizons remain task- and policydependent [2, 9]. Consistent with this trade-off, halving the executed prefix from 26 to 13 actions substantially reduced Q-score and success rate while increasing episode length (Tab. 1). **Playback Speed-Up:** The 1 _._ 3 _×_ playback speed-up used by Larchenko et al. [2] also outperformed standardspeed execution, whereas increasing the speed-up to 2 _×_ leaned worse without reaching significance. **Denoising Steps:** Prior work uses different numbers of flow-matching inference steps, from 4 in GR00T N1 [10] to 10 in _π_ 0 [7]. Starting from the 20-step configuration of Larchenko et al. [2], reducing denoising to 10 or one step produced no detectable performance change. **Overlap Inpainting:** Real-Time Chunking (RTC) uses inpainting to maintain chunk continuity during asynchronous inference [11]. Larchenko et al. [2] also uses overlap inpainting but does not ablate it. Disabling it had no detectable effect on Q-score. **Advantage-Guidance Strength:** Increasing advantageguidance strength to _β_ = 2 was worse, while _β_ = 4 matched _β_ = 1. **Rendering:** Motivated by the gains from high-resolution rendering reported by Bai et al. [9], we compare downsampling with direct rendering at 224 × 224. 

### **3.2 Data Collection** 

To maximize the number of successful rollouts collected for training, we evaluate strategies to reduce data-collection costs and improve recovery from failed episodes (Tab. 2). **Restart Points:** Prior work replays failure states [3], revisits promising states [12], and expands start states outward from the goal [13]. Among the tested restart points, restarting before the first drop in predicted task progress earned more progress than restarting at the last progress point. **Simulation Cost:** Restarts reduced simulation cost but did not significantly improve successes per simulation step. **StageBelief Restoration:** Since the policy feeds back its predicted stage [2], omitting this state during restoration reduced Q-score and task progress, supporting the preservation of policy-side state. 

## **4 Conclusion** 

We have evaluated inference and data-collection strategies across all 100 BEHAVIOR-1K tasks. Shorter action chunks significantly reduced Q-score and a playback speed of 1.3 improved performance. Fewer denoising steps and disabling overlap inpainting maintained performance, whereas stronger advantage guidance offered no benefit. Snapshot restarts reduced simulation cost but not success, and required restoring the policy’s stage belief. These results suggest that inference and data-collection strategies do not necessarily scale uniformly across task complexity. 

2 

### **Acknowledgments** 

Thank you to the Stanford BEHAVIOR Challenge organizers, who created this benchmark. This work has taken place in the VCAI Lab at Kiel University and in the RobotiXX Lab at George Mason University. The research was conducted under the RobOdin project funded by the European Union through its Interreg Germany-Denmark funding program. RobotiXX research is supported by National Science Foundation (NSF, 2350352), Army Research Office (ARO, W911NF2320004, W911NF2520011), Army Ground Vehicle Systems Center (GVSC), Google DeepMind (GDM), Microsoft Research (MSR), Clearpath Robotics, FrodoBots Lab, Raytheon Technologies (RTX), Tangenta, 4-VA, Mason Innovation Exchange (MIX), and Walmart. We acknowledge technical support by the Embodied AI Center at Kiel University. 

## **References** 

- [1] C. Li, R. Zhang, J. Wong, C. Gokmen, S. Srivastava, R. Mart´ın-Mart´ın, C. Wang, G. Levine, W. Ai, B. Martinez, H. Yin, M. Lingelbach, M. Hwang, A. Hiranaka, S. Garlanka, A. Aydin, S. Lee, J. Sun, M. Anvari, M. Sharma, D. Bansal, S. Hunter, K.-Y. Kim, A. Lou, C. R. Matthews, I. Villa-Renteria, J. H. Tang, C. Tang, F. Xia, Y. Li, S. Savarese, H. Gweon, C. K. Liu, J. Wu, and L. Fei-Fei. Behavior-1k: A human-centered, embodied ai benchmark with 1,000 everyday activities and realistic simulation. _arXiv preprint arXiv:2403.09227_ , 2024. 

- [2] I. Larchenko, G. Zarin, and A. Karnatak. Task adaptation of vision-language-action model: 1st place solution for the 2025 behavior challenge, 2025. URL `https://arxiv.org/abs/ 2512.06951` . 

- [3] I. Larchenko. Learning to fold: prizewinning solution at lehome challenge 2026 (1st place online, 2nd offline), 2026. URL `https://arxiv.org/abs/2606.27163` . 

- [4] Dream Machines. Empirical results fine-tuning _π_ 0 _._ 5 on a real manufacturing task. `https: //dream-machines.eu/blog/pi05-fine-tuning` , Sept. 2026. Blog post. 

- [5] P. Intelligence, A. Amin, R. Aniceto, A. Balakrishna, K. Black, K. Conley, G. Connors, J. Darpinian, K. Dhabalia, J. DiCarlo, D. Driess, M. Equi, A. Esmail, Y. Fang, C. Finn, C. Glossop, T. Godden, I. Goryachev, L. Groom, H. Hancock, K. Hausman, G. Hussein, B. Ichter, S. Jakubczak, R. Jen, T. Jones, B. Katz, L. Ke, C. Kuchi, M. Lamb, D. LeBlanc, S. Levine, A. Li-Bell, Y. Lu, V. Mano, M. Mothukuri, S. Nair, K. Pertsch, A. Z. Ren, C. Sharma, L. X. Shi, L. Smith, J. T. Springenberg, K. Stachowicz, W. Stoeckle, A. Swerdlow, J. Tanner, M. Torne, Q. Vuong, A. Walling, H. Wang, B. Williams, S. Yoo, L. Yu, U. Zhilinsky, and Z. Zhou. _π_ 0<sup>_∗_</sup> _._ 6<sup>:</sup> a vla that learns from experience, 2025. URL `https://arxiv.org/abs/2511.14759` . 

- [6] Stanford Vision and Learning Lab. Behavior challenge 2026: Evaluation and rules. `https: //behavior.stanford.edu/challenge/evaluation.html` , 2026. Accessed: 2026-1024. 

- [7] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, L. X. Shi, J. Tanner, Q. Vuong, A. Walling, H. Wang, and U. Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control, 2026. URL `https://arxiv. org/abs/2410.24164` . 

- [8] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 2024. 

- [9] J. Bai, Y.-W. Chao, Q. Chen, J. Gu, M. J. Kim, Z. Li, X. Li, T.-Y. Lin, M.-Y. Liu, N. Ma, K. Mo, D. Qu, S. Sun, H. Xia, F. Wei, and X. Zeng. Openpi comet: Competition solution for 2025 behavior challenge. _arXiv preprint arXiv:2512.10071_ , 2025. URL `https://arxiv. org/abs/2512.10071` . 

3 

- [10] NVIDIA, :, J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. J. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, J. Jang, Z. Jiang, J. Kautz, K. Kundalia, L. Lao, Z. Li, Z. Lin, K. Lin, G. Liu, E. Llontop, L. Magne, A. Mandlekar, A. Narayan, S. Nasiriany, S. Reed, Y. L. Tan, G. Wang, Z. Wang, J. Wang, Q. Wang, J. Xiang, Y. Xie, Y. Xu, Z. Xu, S. Ye, Z. Yu, A. Zhang, H. Zhang, Y. Zhao, R. Zheng, and Y. Zhu. Gr00t n1: An open foundation model for generalist humanoid robots, 2025. URL `https://arxiv.org/abs/2503.14734` . 

- [11] K. Black, M. Y. Galliker, and S. Levine. Real-time execution of action chunking flow policies, 2025. URL `https://arxiv.org/abs/2506.07339` . 

- [12] A. Ecoffet, J. Huizinga, J. Lehman, K. O. Stanley, and J. Clune. First return then explore. _CoRR_ , abs/2004.12919, 2020. doi:10.48550/ARXIV.2004.12919. URL `https://doi.org/ 10.48550/arXiv.2004.12919` . 

- [13] C. Florensa, D. Held, M. Wulfmeier, and P. Abbeel. Reverse curriculum generation for reinforcement learning. _CoRR_ , abs/1707.05300, 2017. doi:10.48550/ARXIV.1707.05300. URL `https://doi.org/10.48550/arXiv.1707.05300` . 

4 

