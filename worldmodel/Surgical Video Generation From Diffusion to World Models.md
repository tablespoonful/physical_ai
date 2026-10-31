---
title: "Surgical Video Generation From Diffusion to World Models: A Survey"
date: "2026-08-26"
authors: "Fuxiang Huang; Chenxu Zhang; Liang Han; Lei Zhang"
url: https://arxiv.org/abs/2608.26214
pdf: https://arxiv.org/pdf/2608.26214
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2608.26214)** / [論文ページ](https://arxiv.org/abs/2608.26214)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Surgical Video Generation From Diffusion to World Models: A Survey 

Fuxiang Huang _School of Data Science Lingnan University_ Hong Kong, China fxhuang1995@gmail.com 

Chenxu Zhang; Liang Han; Lei Zhang<sup>*</sup> _School of Microelectronics and Communication Engineering_ 

_Chongqing University_ 

Chongqing, China 

zhangchenxu@cqu.edu.cn; hanliangaa@cqu.edu.cn; leizhang@cqu.edu.cn 

**_Abstract_ —Surgical video data provides the primary training resource for models of intraoperative perception, surgical workflow understanding, and robotic decision-making. However, clinical data acquisition remains constrained by privacy, cost, and class imbalance. Surgical video generation has emerged as a transformative approach to addressing data scarcity and as a foundation for surgical simulation, training, and robotic policy learning. The field has developed rapidly without a clear conceptual framework. This survey organizes the 2024– 2026 literature into three categories: unconditional generation, conditional generation, and world modeling generation, revealing a fundamental shift in how the task is defined from synthesizing visually plausible frames to modeling the causal dynamics of surgical scenes. We examine the persistent gap between pixel-level fidelity and clinical plausibility, and identify generalization, physical realism, controllability, and interpretability as bottlenecks. We further summarize experimental results of representative methods on public datasets to provide a quantitative reference for the field. This survey provides a structured overview of the current state and open challenges, offering a reference for researchers working at the intersection of intelligent perception, multi-modal fusion, generative AI, and surgical data science.** **_Index Terms_ —surgical video generation, diffusion models, multi-modal fusion, world model, intelligent perception** 

## I. INTRODUCTION 

Artificial intelligence (AI) in surgery aims to bridge computational intelligence and clinical practice, delivering reproducible, safe, and scalable technologies for surgical training, decision support, and robotic automation [1]. High-quality surgical videos constitute the primary data substrate for building computer vision models that parse surgical workflows, quantify surgeon behaviors, and optimize robotic manipulation strategies. However, real-world surgical video datasets face three fundamental practical limitations. First, privacy regulations hinder large-scale public data dissemination. Second, rare surgical cases and infrequent intraoperative adverse events lead to severe long-tailed data distributions. Third, manual labeling for surgical phases, instruments, and tissue-tool interactions is labor-intensive, costly, and prone to human error. These bottlenecks substantially obstruct the large-scale real-world deployment of surgical AI systems. 

This work was partially supported by National Natural Science Fund of China under Grants 92570110 and 62271090, Chongqing Natural Science Fund under Grant CSTB2024NSCQ-JQX0038, and National Youth Talent Project. 

Generative AI has substantially advanced biomedical data engineering by enabling the synthesis of clinically meaningful visual content [2]. Recent advances in video diffusion models [3], large vision-language models [4], and neuro-symbolic systems [5], in particular, have driven significant progress in controllable surgical video generation. Unlike generic video synthesis tasks, surgical video generation imposes stringent domain constraints: synthesized outputs must preserve correct anatomical topology, conform to standard surgical procedural logic, and guaranty physically plausible tissue-tool interactions. Such specialized requirements make surgical video generation a unique interdisciplinary research problem that requires a customized methodological investigation. 

Driven by these demands, research on surgical video generation has grown rapidly from 2024 to 2026. Despite this rapidly expanding body of literature, existing contributions remain fragmented and lack a unified conceptual framework. To the best of our knowledge, no dedicated survey offers a domainfocused, critical review of this rapidly evolving research topic. Representative prior work such as Algethami _et al._ [2] reviews biomedical video synthesis from the perspective of imaging modalities, spanning endoscopy, echocardiography, MRI, and CT. Their work delivers a valuable cross-modal summary of general techniques and shared challenges across biomedical visual generation. Different from this modality-centered perspective, the present survey concentrates exclusively on surgical video generation. We structure existing literature by generation objective, tracing the technical trajectory from unconditional generation toward world modeling approaches. Concretely, we categorize existing approaches into three paradigms: _unconditional generation_ , _conditional generation_ , and _world modeling generation_ . This taxonomy demonstrates a clear technical evolution: research objectives shift from producing visually realistic individual frames toward modeling causal dynamics within surgical scenes. Furthermore, we systematically analyze prevailing evaluation protocols, highlight the persistent mismatch between pixel-level visual fidelity and clinical plausibility, and summarize core bottlenecks covering generalization capability, physical realism, controllability, and interpretability. Finally, we suggest a few directions that may merit further exploration. 

The remainder of this survey is structured as follows. 


Fig. 1. Three paradigms of surgical video generation. (a) Unconditional Generation: visually plausible video generation from noise. (b) Conditional Generation: semantically controllable video generation guided by conditioning signals. (c) World Modeling Generation: causally consistent and physically plausible video generation through explicit state transition modeling. 

Section II defines the task; Section III presents a taxonomy and reviews three paradigms; Section IV covers datasets and metrics; Section V discusses limitations and outlines potential directions; Section VI concludes. 

## II. PROBLEM FORMULATION 

Let _V_ = _{v_ 1 _, . . . , vT }_ denote a surgical video sequence of _T_ frames. Surgical video generation aims to learn a conditional distribution _p_ ( _V | C_ ), where _C_ denotes control signals and may be empty. When present, _C_ provides control over the generation process. In conditional generation, _C_ specifies the desired content, such as texts, masks, or phase labels. In world modeling generation, _C_ represents actions that drive state transitions, shifting the focus from appearance control to modeling how surgical scenes evolve in response to interventions. 

## III. TAXONOMY OF SURGICAL VIDEO GENERATION 

We categorize existing methods according to their generation objective: _unconditional generation_ , _conditional generation_ , and _world modeling generation_ . Figure 1 illustrates the distinction among the three paradigms. 

## _A. Unconditional Generation_ 

Unconditional generation, employs diffusion models to synthesize visually plausible surgical videos from random noise without external conditioning. Endora [6] pioneered a diffusion Transformer for endoscopic simulation, learning the unconditional distribution of surgical video data. This work demonstrated that diffusion models can produce visually plausible surgical scenes, suggesting the fundamental viability of generative approaches for surgical video synthesis. Having established that diffusion models can generate surgical videos, the next question is how to control what is generated. 

## _B. Conditional Generation_ 

Conditional generation, leverages conditional diffusion models to synthesize videos guided by explicit conditioning signals. Methods in this category learn conditional distributions _p_ ( _V | C_ ), where _C_ represents user-specified or taskderived conditions. These signals can take various forms, including texts, phase labels, trajectories, scene graphs, keypoints, kinematic data, or action-related inputs for policy 

learning and strategy evaluation. Early efforts introduced basic control modalities. VISAGE [7] introduced future video generation in laparoscopic surgery. Given a single initial frame and action graph triplets (instrument, verb, target), the model predicts subsequent frames. An interactive laparoscopic video-diffusion framework [8] enabled interactive generation control via text prompts and instrument segmentation masks. MS-PCD [9] incorporated procedural planning through phase labels. SurgSora [10] proposed object-aware controllable diffusion with dual semantic injection, decoupled flow mapping, and trajectory control. It allows user-guided fine-grained video generation without relying on manually annotated segmentation masks. HieraSurg [11] established a hierarchical two-stage diffusion paradigm, first predicting coarse surgical semantic changes and then generating finegrained visual features. Ophora [12] constructed the first largescale ophthalmic surgical video-text dataset Ophora-160K and enables text-guided cataract surgery generation. LLaMA-VG [4] introduced large vision-language model architectures for endoscopic video generation. SG2VID [13] used scene graphs for fine-grained control of instrument positions and anatomical layouts. MoViS [14] leveraged keypoint-based motion guidance to capture complex instrument kinematics. Blob [15] explored 3D position-aware surgical scene simulation through kinematic structured modeling. Conditional generation makes synthesis controllable. However, controllability alone does not constitute understanding how surgical scenes evolve in response to actions. 

## _C. World Modeling Generation_ 

World modeling generation, aims to generate causally consistent and physically plausible surgical dynamics rather than merely producing visually plausible frames. Unlike conditional generation, which learns _p_ ( _V | C_ ) from statistical correlations, world modeling generation seeks to capture the underlying transition dynamics _p_ ( _st_ +1 _| st, at_ ), enabling prediction, interaction, and closed-loop decision-making. SWoMo [5] is the representative approach in this category. Its symbolic component combines a rule-based simulator with physical scene graphs to model instrument-tissue interaction dynamics and causal rationality, while a diffusion model renders realistic visual appearance from the predicted states. However, explicit state transition modeling remains an emerging direction with only preliminary demonstrations to date. 

## _D. Summary of Methods_ 

Table I summarizes representative methods by paradigm, listing publication venue, control type, and code availability where applicable. The three paradigms reflect a progression in generation objective: from unconditional video generation, to controllable conditional generation, to explicit state transition modeling for causally consistent surgical dynamics. 

## IV. DATASETS AND EVALUATION 

## _A. Public Datasets_ 

The development of surgical video generation models depends on the availability of high-quality datasets. Table II 

TABLE I 

SUMMARY OF SURGICAL VIDEO GENERATION METHODS. 

|**Method**|**Venue**|**Paradigm**|**Control Type**|**Code**|
|---|---|---|---|---|
|Endora [6]|MICCAI 2024|Unconditional|None|—|
|VISAGE [7]|MICCAI 2024|Conditional|Image, Structured Label|—|
|Inter. Laparoscopic [8]|MICCAI 2024|Conditional|Text, Mask|—|
|MS-PCD [9]|MICCAI 2024|Conditional|Image, Phase Label|—|
|SurgSora [10]|MICCAI 2025|Conditional|Image, Trajectory|Link|
|HieraSurg [11]|MICCAI 2025|Conditional|Hierarchical Condition|Link|
|Ophora [12]|MICCAI 2025|Conditional|Text|Link|
|LLaMA-VG [4]|ISBI 2025|Conditional|Video, Text|—|
|SG2VID [13]|MICCAI 2025|Conditional|Scene Graph|Link|
|MoViS [14]|MICCAI 2025|Conditional|Keypoints|—|
|Blob [15]|IJCARS 2026|Conditional|Kinematic Data|—|
|SWoMo [5]|MICCAI 2026|World Modeling|Symbolic Action|Link|


### TABLE II 

SUMMARY OF DATASETS RELEVANT TO SURGICAL VIDEO GENERATION. 

|**Dataset**|**Modality**|**Videos**|**Annotation**|**Access**|
|---|---|---|---|---|
|Cholec80|Laparoscopic|80|Phase, Tool|Link|
|CholecT50|Laparoscopic|50|Phase, Tool, Action|Link|
|CoPESD|Endoscopic ESD|—|Multi-level Motion|Link|
|Ophora-160K|Ophthalmic|9,819|Text Instructions|Link|
|Cataract-1K|Ophthalmic|1,000|Phase, Segmentation|Link|
|CATARACTS|Ophthalmic|50|Tool, Activity|Link|
|JIGSAWS|Robotic|—|Kinematic, Gesture|Link|
|Kvasir-Capsule|Capsule Endoscopy|117|Classification|Link|


suggesting that large-scale pre-training may benefit surgical video generation. This direction, however, remains largely unexplored. Future work should systematically evaluate crossdomain generalization, adapt domain adaptation techniques to surgical video generation, and explore large-scale pre-training on diverse surgical datasets. 

## _B. Physical Realism and Controllability_ 

Current diffusion models learn visual-temporal distributions from data without explicit modeling of tissue deformation, force transmission, or fluid dynamics. Generated videos may appear visually plausible while violating physical laws, limiting their utility for surgical simulation or preoperative planning. Conditional generation methods support control via text, trajectory, or phase labels, yet controllability remains limited. Users cannot easily specify complex surgical actions or predict how input changes affect output. More interpretable conditioning mechanisms are needed to enable fine-grained interaction. Future work should integrate biomechanical priors into generative architectures and develop more interpretable and flexible conditioning mechanisms. 

## _C. Evaluation and Trustworthiness_ 

summarizes key datasets that have supported recent advances in this field. 

## _B. Evaluation_ 

To provide a quantitative reference for the methods surveyed, Table III summarizes the reported performance of representative methods on public surgical video datasets. Key metrics include FVD for video quality, FID for frame-level fidelity, and SSIM for structural similarity, with additional metrics such as LPIPS, PSNR, IS, Frame Consistency, and CLIPScore reported where available. It should be noted that direct comparison across datasets is not meaningful due to differences in video length, surgical procedure complexity, and evaluation protocols. 

## V. LIMITATIONS AND FUTURE DIRECTIONS 

Despite recent progress, surgical video generation faces three key bottlenecks: data and generalization, physical realism and controllability, and evaluation and trustworthiness, which also suggest promising future directions. 

## _A. Data and Generalization_ 

Most existing methods are trained on datasets from single institutions or specific surgical modalities. Performance under domain shifts across different imaging systems, lighting conditions, or patient populations has not been systematically studied. Unsupervised domain adaptation has been explored in general computer vision to address such distribution shifts [16], [17], but whether these techniques transfer to surgical video generation remains unclear. Data scarcity is another fundamental bottleneck. Most datasets focus on a single procedure and contain few videos, limiting generalization. Surgical video foundation models such as SurgVISTA [18] demonstrate strong transferability across understanding tasks, 

Standardized evaluation remains a significant gap. Current practice relies on metrics borrowed from general image and video synthesis, including FVD, FID, IS, PSNR, SSIM, and LPIPS. While these capture visual fidelity, none reflect procedural correctness, anatomical plausibility, or surgical appropriateness. A video may score well on these measures while depicting clinically nonsensical interactions. The SurgVeo benchmark [19], which introduces the Surgical Plausibility Pyramid (SPP) framework, represents a step toward surgeryspecific assessment by evaluating the plausibility of instrument operation, tissue feedback, and surgical intent. However, a community-wide evaluation standard remains absent. Trustworthiness presents additional concerns. Current models offer little insight into their confidence or failure modes, and uncertainty quantification remains largely unexplored. The internal mechanisms of diffusion models are also difficult to interpret, complicating the assessment of clinical reliability. Future work should establish community-wide evaluation benchmarks, develop uncertainty quantification methods, and improve interpretability for failure detection and output explanation. 

## VI. CONCLUSION 

This survey reviews surgical video generation from 2024 to 2026. We organize the literature into three paradigms according to generation objective: unconditional generation, conditional generation, and world modeling generation. This taxonomy reveals an evolutionary trajectory from establishing synthesis feasibility, to enabling controllability, to modeling causal dynamics for decision-making support. We summarize publicly available datasets, identify a persistent gap between pixel-level metrics and clinical plausibility, and synthesize key bottlenecks across generalization, physical realism, controllability, and trustworthiness. World modeling generation 

TABLE III 

QUANTITATIVE RESULTS OF REPRESENTATIVE METHODS ON PUBLIC DATASETS. 

|**Dataset** (**Setting**)|**Method**|**FVD**_↓_|**FID**_↓_|**SSIM**_↑_|**IS**_↑_|**PSNR**_↑_|**LPIPS**_↓_|**Others**|
|---|---|---|---|---|---|---|---|---|
|Cholec80 (SG2VID [13])|Endora<br>SG2VID|533.80<br>457.30|47.00<br>16.40|—<br>—|—<br>—|—<br>—|0.53<br>0.53|—<br>BB IoU: 0.62, F1: 0.47|
||VISAGE-T|1780.00|—|0.56|—|18.10|0.39|—|
|CholecT50 (MoViS [14])|VISAGE-I|1875.00|—|0.56|—|18.30|0.38|—|
||MoViS|477.00|—|0.57|—|18.80|0.19|—|
|CoPESD (SurgSora [10])|Endora<br>SurgSora|1146.54<br>395.65|205.93<br>87.94|—<br>0.56|2.24<br>3.28|—<br>20.71|—<br>—|Frame Cons.: 97.51%<br>Frame Cons.: 98.70%|
||Endora|258.70|40.00|—|—|—|0.38|—|
|Cataract-1k (SWoMo [5])|SWoMo|123.00|20.10|—|—|—|0.39|BB IoU: 0.65, F1: 0.66|
||SG2VID|73.00|24.90|—|—|—|0.39|BB IoU: 0.61, F1: 0.62|
|Ctt1kSG2VID13|Endora|265.90|30.30|—|—|—|0.38|—|
|aarac- ( [])|SG2VID|901.80|137.60|—|—|—|0.324|—|
|KiClLLMAVG4|Endora|75.95|14.03|—|2.50|—|—|—|
|vasr-apsue (a- [])|LLaMA-VG|59.02|10.11|—|2.90|—|—|—|
||Endora|460.70|13.41|—|3.90|—|—|—|
|Colonoscopic (LLaMA-VG [4])|LLaMA-VG|369.97|12.46|—|3.99|—|—|—|
||Endora|990.30|60.50|—|—|—|—|—|
|Ophora-160K (Ophora [12])|Ophora|276.96|33.72|—|—|—|—|CLIPScore: 39.19|
||Endora|436.80|58.40|—|—|—|0.46|—|
|CATARACTS (SWoMo [5])|SG2VID|363.80|47.30|—|—|—|0.44|BB IoU: 0.50, F1: 0.39|
||SWoMo|265.40|40.80|—|—|—|0.45|BB IoU: 0.52, F1: 0.41|
||Endora|649.50|45.90|—|—|—|0.46|—|
|CATARACTS (SG2VID [13])|SG2VID|523.80|40.90|—|—|—|0.44|BB IoU: 0.49, F1: 0.38|
|JIGSAWS (Blob [15])|Blob|—|—|0.829|—|22.68|0.09|—|


offers a promising direction. Achieving it requires explicit state transition modeling for causal consistency and physical plausibility. However, current approaches remain preliminary, and the transition from diffusion to world models is still underway. Future research should pursue closer integration of domain knowledge, robust evaluation, and physically grounded generation. Progress in these directions is essential for advancing the field toward practical applications. 

## REFERENCES 

- [1] L. Maier-Hein, M. Eisenmann, D. Sarikaya, K. M¨arz, T. Collins, A. Malpani _et al._ , “Surgical data science–from concepts toward clinical translation,” _MedIA_ , vol. 76, p. 102306, 2022. 

- [2] N. Algethami, T. Iqbal, and I. Ullah, “Generative AI for biomedical video synthesis: a review,” _Artif. Intell. Rev._ , vol. 58, no. 12, p. 392, 2025. 

- [3] J. Ho, T. Salimans, A. Gritsenko, W. Chan, M. Norouzi, and D. J. Fleet, “Video diffusion models,” _NeurIPS_ , vol. 35, pp. 8633–8646, 2022. 

- [4] Y. Chen, Z. Han, and Q. Dou, “LLaMA-VG: A video vision LLaMAbased model for endoscopy video generation,” in _ISBI_ , 2025, pp. 1–5. 

- [5] S. K. Sivakumar, A. Johnson, A. Dhingra, Y. Frisch, G. Ghazaei, and A. Mukhopadhyay, “SWoMo: Neuro-symbolic world model for cataract surgery simulation,” in _MICCAI_ , 2026. 

- [6] C. Li, H. Liu, Y. Liu, B. Y. Feng, W. Li, X. Liu, Z. Chen, J. Shao, and Y. Yuan, “Endora: Video generation models as endoscopy simulators,” in _MICCAI_ , 2024, pp. 230–240. 

- [7] Y. Yeganeh, R. Lazuardi, A. Shamseddin, E. Dari, Y. Thirani, N. Navab, and A. Farshad, “VISAGE: Video synthesis using action graphs for surgery,” in _MICCAI_ , 2024, pp. 146–156. 

- [8] I. Iliash, S. Allmendinger, F. Meissen, N. K¨uhl, and D. R¨uckert, “Interactive generation of laparoscopic videos with diffusion models,” in _MICCAI workshop_ , 2024, pp. 109–118. 

- [9] Z. Zhao, F. Fang, X. Yang, Q. Xu, C. Guan, and S. K. Zhou, “See, predict, plan: Diffusion for procedure planning in robotic surgical videos,” in _MICCAI_ , 2024, pp. 553–563. 

- [10] T. Chen, S. Yang, J. Wang, L. Bai, H. Ren, and L. Zhou, “SurgSora: Object-aware diffusion model for controllable surgical video generation,” in _MICCAI_ , 2025, pp. 521–531. 

- [11] D. Biagini, N. Navab, and A. Farshad, “HieraSurg: Hierarchy-aware diffusion model for surgical video generation,” in _MICCAI_ , 2025, pp. 310–319. 

- [12] W. Li, M. Hu, G. Wang, L. Liu, K. Zhou, J. Ning, X. Guo, Z. Ge, L. Gu, and J. He, “Ophora: a large-scale data-driven text-guided ophthalmic surgical video generation model,” in _MICCAI_ , 2025, pp. 425–435. 

- [13] S. K. Sivakumar, Y. Frisch, G. Ghazaei, and A. Mukhopadhyay, “SG2VID: Scene graphs enable fine-grained control for video synthesis,” in _MICCAI_ , 2025, pp. 511–521. 

- [14] Y. Yeganeh, N. Navab, and A. Farshad, “MoViS: Motion-guided video generation for laparoscopic surgery,” in _MICCAI Workshop_ , 2025, pp. 215–225. 

- [15] L. Mennillo, C. Katzir, R. He, D. Anastasiou, D. Stoyanov, and E. B. Mazomenos, “Blob representation of robotic surgical scenes for positionaware video generation,” _IJCARS_ , pp. 1–10, 2026. 

- [16] F. Huang, S. Song, and L. Zhang, “Gradient harmonization in unsupervised domain adaptation,” _IEEE TPAMI_ , vol. 46, no. 12, pp. 10 319– 10 336, 2024. 

- [17] F. Huang, X. Fu, S. Ye, L. Ma, W. Li, X. Gao, D. Zhang, and L. Zhang, “Unsupervised robust domain adaptation: Paradigm, theory and algorithm: F. huang etal,” _IJCV_ , vol. 134, no. 1, p. 5, 2026. 

- [18] S. Yang, F. Zhou, L. Mayer, F. Huang, Y. Chen, Y. Wang, S. He, Y. Nie, X. Wang, Y. Jin _et al._ , “Large-scale self-supervised video foundation model for intelligent surgery,” _npj Digit. Med._ , vol. 9, no. 1, p. 220, 2026. 

- [19] Z. Chen, Q. Xu, J. Wu, B. Yang, Y. Zhai, G. Guo, J. Zhang, Y. Ding, N. Navab, and J. Luo, “How far are surgeons from surgical world models? a pilot study on zero-shot surgical video generation with expert assessment,” _arXiv:2511.01775_ , 2025. 

