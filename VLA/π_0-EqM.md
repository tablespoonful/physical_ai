---
title: "$π_0$-EqM: Equilibrium Matching for Closed-Loop Vision-Language-Action Control"
date: "2026-05-22"
authors: "Huanming Liu; Congsheng Xu; Jianmin Ji; Yao Mu"
url: https://arxiv.org/abs/2605.23128
pdf: https://arxiv.org/pdf/2605.23128
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.23128)** / [論文ページ](https://arxiv.org/abs/2605.23128)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# _π_ 0 **-EqM: Equilibrium Matching for Closed-Loop Vision-Language-Action Control** 

Huanming Liu<sup>1</sup><sup>_,∗_</sup> , Congsheng Xu<sup>2</sup><sup>_,∗_</sup> , Jianmin Ji<sup>1</sup><sup>_,_†</sup> , and Yao Mu<sup>2</sup><sup>_,_†</sup> 

**_Abstract_ — Currently, Vision-Language-Action (VLA) models have become the most adopted paradigm for robotic manipulation for its great potential for task generalization. While most generative flow-matching action decoders for VLA control are often deployed with fixed sampling horizons, limiting statedependent compute and temporal reuse across control cycles. We present** _π_ 0 **-EqM, which replaces the flow-matching expert in** _π_ 0 **with an Equilibrium Matching (EqM) decoder while leaving the upstream VLA stack unchanged. Under a matched 300step budget,** _π_ 0 **-EqM improves RoboTwin average success from 40.4% to 50.2% across 19 tasks and remains competitive on LIBERO, with its clearest gain on LIBERO-10 (87.0%). Two threshold scans reveal a task-dependent** **_non-monotonic_ relation between residual and success, which we term the** **_stationarity– executability gap_ . The results suggest that inference depth in iterative VLA control is part of policy design and introduce an energy-based VLA perspective that may inform future work on composable action generation across tasks and embodiments.** 

## I. INTRODUCTION 

Vision-Language-Action (VLA) policies map visual observations and language instructions directly to actions [1], [2], [3], [4]. In these systems, a central design choice is the action decoder that produces short action chunks for receding-horizon execution. Recent large-scale VLAs such as _π_ 0 use flow-matching decoders [5], [6], while diffusionbased action generation remains a strong alternative [7]. These decoders are expressive, but are typically deployed with fixed denoising or integration horizons. 

This is restrictive in closed loop. Different states benefit from different amounts of computation, and consecutive control cycles are strongly correlated, making iterate reuse desirable. Yet in diffusion and flow decoders, intermediate states are tied to explicit time or noise semantics, which makes early stopping and cross-cycle warm starts awkward. 

We therefore ask whether inference depth should be treated as part of deployed policy design. To study this, we replace the flow-matching expert in _π_ 0 with an Equilibrium Matching (EqM) decoder [8]. EqM learns a timefree conditional vector field and decodes actions by iterative equilibrium solving rather than time-indexed transport. 

This also introduces an energy-based perspective into VLA and points to composable energy-based action generation across tasks and embodiments as a natural extension. Because EqM is time free, intermediate iterates no longer carry 

> 1Huanming Liu and Jianmin Ji are with University of Science and Technology of China, China lhm ~~0~~ 410@mail.ustc.edu.cn, jianmin@ustc.edu.cn 

> 2Congsheng Xu and Yao Mu are with Shanghai Jiao Tong University, China acondaway@sjtu.edu.cn, muyao@sjtu.edu.cn 

> _∗_ Equal contribution. 

> †Corresponding authors. 


Fig. 1. Overview of _π_ 0-EqM. We replace only the action decoder in _π_ 0 and cast action generation as iterative equilibrium solving, enabling adaptive stopping and warm starts. An executable intermediate action may appear before full numerical convergence. explicit diffusion-time semantics, making stopping and reuse deployment decisions rather than sampler-specific interventions. 

Under a matched 300-step inference budget, _π_ 0-EqM improves RoboTwin average success from 40.4% to 50.2% across 19 tasks. On LIBERO, it remains competitive overall and improves LIBERO-10 from 85.2% to 87.0%. Threshold scans further show that lower residual does not uniformly imply better execution. We refer to this mismatch as the _stationarity–executability gap_ . 

Our contributions are summarized as follows: 

- We introduce _π_ 0-EqM, a decoder replacement for _π_ 0 that improves RoboTwin average success by 9.8 points under a matched 300-step budget while remaining competitive on LIBERO. 

- We show that stopping depth can change closed-loop behavior in EqM-based control. 

- We connect a local solver analysis to threshold-scan behavior and use the stationarity–executability gap to interpret iterative action decoding. 

- Our method qualitatively and quantitatively shows that the time-independent diffusion action generation method can lead to better performance for robotic manipulation. 

## II. RELATED WORK 

_a) VLA policies and chunked action decoding:_ Modern VLA systems combine visual encoders, language conditioning, and chunked action prediction in a single model interface [1], [2], [3], [4]. Action chunking improves stability in long-horizon control [9] and mitigate the non-marcov property of the robotic manipulation. Usually, VLAs utilizes a web-scale data pre-trained VLM as the understanding backbone and discrete action token output, and a light-weight head for continuous action generation based on the VLM’s visual and action semantic information. _π_ series models extends this line with a flow-matching action expert [5]; our work keeps the structure of upstream VLM and modifies only the action decoder that follows the design art of Equilibrium Matching. 

_b) Optimization-based control and energy-based inference:_ A complementary line treats action generation as optimization, either by solving a control objective online or by minimizing a learned conditional energy / following its gradient field [10], [11], [12], [13]. Compared with fixed-horizon generative decoding, such formulations make the iterative structure of inference explicit and render testtime computation more controllable, which is particularly relevant in closed-loop settings. EqM is related to this family in its inference form, but differs in parameterization: instead of requiring an explicit scalar energy, it learns an implicit conditional vector field whose equilibria define the target action chunks [8]. Recent work has also explored time-unconditional flow matching for adaptive robotic control [14]. This makes EqM a natural fit for exposing adaptive stopping and warm-start reuse within a VLA decoder. 

## III. METHOD 

## _A. Preliminaries: Action Decoding as Iterative Inference_ 

At control step _t_ , a VLA policy maps the multimodal condition _ct_ = ( _ot ,ℓ, st_ ) to an action chunk _At_ = [ _at , at_ +1 _,..., at_ + _H−_ 1] _∈_ R<sup>_H×d_</sup> . In our receding-horizon setup, only the immediate action _at_ is executed before replanning. Rather than treating decoding as a fixed-cost black box, we view it as iterative inference whose depth is a controllable policy variable. EqM provides the mathematical scaffolding for this view. 

## _B. Equilibrium Matching for VLA Control_ 

Unlike diffusion or flow-matching policies that parameterize time-indexed score or velocity fields, EqM learns a **timeinvariant** (autonomous) conditional vector field _fθ_ ( _A_ ; _ct_ ) _∈_ R<sup>_H×d_</sup> . The roots of this field correspond to the target equilibrium action chunks. 

_a) Training Objective:_ Given a demonstration chunk _A ∼ p_ data, structural noise _ε ∼ N_ (0 _, I_ ), and an interpolation factor _γ ∼ U_ (0 _,_ 1), we define the interpolant _Aγ_ = _γA_ + (1 _− γ_ ) _ε_ . The field _fθ_ is trained to match a targeted vector _v_ target( _γ_ ; _A, ε_ ) = _w_ ( _γ_ )( _A − ε_ ) via the EqM loss: 


_b) Inference as Equilibrium Solving:_ At test time, actions are recovered by solving _fθ_ ( _A_ ; _ct_ ) = 0. Starting from _At_<sup>(0)</sup> and setting _At_<sup>(</sup><sup>_−_1)</sup> = _At_<sup>(0)</sup> , we use a Nesterov-accelerated solver: 


where _µ ∈_ [0 _,_ 1) is the momentum factor and _η >_ 0 is the step size. We use the same lookahead point _A_<sup>�</sup> _t_<sup>(</sup><sup>_k_)</sup> for both the update and the residual check. 

_C. Temporal Coherence: Adaptive Stopping and Warm-Start_ 

The iterative, time-invariant nature of EqM exposes two deployment mechanisms: 

**Adaptive Inference Depth:** We define the normalized lookahead residual 


and stop at _Tt_ ( _τ_ ) = min _{k ≥_ 0 : _rk ≤ τ_ or _k_ = _K_ max _}_ . This exposes state-dependent test-time compute without changing the upstream VLA stack. Using the same lookahead residual in the stopping rule, theory, and threshold scans also keeps the numerical quantity consistent across analysis and deployment. 

**Structural Warm-Start:** Because EqM decoding is independent of a fixed noise schedule, we can exploit temporal coherence between consecutive control cycles. In our implementation, we use a partial warm start: a half-length segment of the previous output chunk is copied into the first half of the current initialization, and the second half is filled with fresh random noise: 


where _At_<sup>(</sup> _−_<sup>out</sup> 1<sup>)</sup> is the final action chunk returned at control step _t −_ 1, _At_<sup>(</sup> _−_<sup>out</sup> 1 _,_<sup>)</sup> copy<sup>denotesthereusedhalf-chunkfrom</sup> that prediction, and _ε_ tail is sampled random noise for the remaining half of the horizon. This preserves short-term temporal structure while allowing the remaining horizon to be reinitialized under the new observation. In practice, such warm starts can place the initial guess closer to a local equilibrium basin and reduce the iterations needed to reach a target residual. 

## _D. Theoretical Interpretation of Solver Iterates_ 

To connect the solver to the stopping rule used later in Sec. V-C, we provide a local interpretation of early stopping. **Proposition 1 (Local Potential Descent).** _Assume that within a neighborhood of the inference trajectory for a fixed ct , the learned field behaves as the gradient of a surrogate energy, fθ_ ( _A_ ; _ct_ ) = ∇ _Et_ ( _A_ ) _, where Et_ ( _A_ ) _is L- smooth and lower-bounded by Et_<sup>_⋆. For any step size η ≤_1</sup><sup>_/L,_</sup> _the iterates generated by Eq._ (3) _(setting µ_ = 0 _, so that A_ � _t_<sup>(</sup><sup>_k_)</sup> = _At_<sup>(</sup><sup>_k_)</sup><sup>_)followadescentpathE_</sup> _t_<sup>(</sup><sup>_A_</sup> _t_<sup>(</sup><sup>_k_+1)</sup> ) _≤ Et_ ( _At_<sup>(</sup><sup>_k_))</sup><sup>_._</sup> _Using the normalized residual rk from Eq._ (4) _, after K steps the minimum residual is bounded by:_ 


Moreover, if the solver map is locally contractive with factor _ρ ∈_ (0 _,_ 1) near an equilibrium _At_<sup>_⋆_,then</sup> 


Under the same local _L_ -smoothness assumption and the identity _fθ_ ( _At_<sup>_⋆_;</sup><sup>_ct_) = 0,thisimplies</sup> 


Therefore, a sufficient number of iterations to reach the experimental stopping threshold _rk ≤ τ_ is 


whenever the logarithm argument exceeds 1; otherwise the threshold is already met at initialization. Warm-starting reduces this sufficient iteration bound by reducing the initial distance _t − At_<sup>_⋆_</sup> ��� _A_ (0) ���2<sup>,uptotheceilingeffectinEq.(9).</sup> This analysis is intentionally local. It justifies the residual threshold used in the experiments as a numerically meaningful stopping rule and explains why warm starts can reduce the iterations needed to reach a target threshold, but it does not determine which threshold maximizes task success. That behavioral question is addressed empirically in Sec. V-C. 

Eq. (9) also makes the warm-start effect explicit. Ignoring the ceiling effect, if the initialization distance is reduced by a factor _α ∈_ (0 _,_ 1), then the sufficient iteration count decreases by roughly log(1 _/α_ ) _/_ log(1 _/ρ_ ). In other words, warm starts are most valuable when the local contraction is strong and the target threshold is strict, which matches the practical intuition that temporal coherence matters most in hard, iterative control regimes. 

## IV. EXPERIMENTAL SETUP 

We evaluate on the 19-task RoboTwin benchmark [15]; representative video keyframes are provided in the supplementary material. Each task uses 500 demonstrations (100 clean and 400 randomized), for 9,500 total. We compare the 


Fig. 2. Threshold scans on two RoboTwin tasks. The preferred threshold differs across tasks, so the same residual threshold changes both solver cost and closed-loop behavior. 

original _π_ 0 against _π_ 0-EqM while keeping the upstream representation stack and conditioning interface fixed, so only the action expert changes. The main comparison uses a matched 300-step inference budget. Threshold-scan experiments allow up to 1000 EqM iterations and stop when the normalized lookahead residual falls below _τ_ . 

We also evaluate on the standard LIBERO suites [16]: LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, and LIBERO-10. For LIBERO, we report suite-level success rates against the corresponding _π_ 0 baseline. 

## V. RESULTS 

## _A. EqM improves the flow-matching baseline on RoboTwin_ 

Table I reports the 19-task deployment results. Under a matched 300-step budget, _π_ 0-EqM improves 12 tasks, degrades 5, and ties 2, raising the average success rate from 40.4 to 50.2. The largest gains occur on pick ~~d~~ ual ~~b~~ ottles, place ~~c~~ ans ~~p~~ lasticbox, and put ~~b~~ ottles ~~d~~ ustbin. 

## _B. LIBERO suite results_ 

Table II reports the LIBERO results. _π_ 0-EqM improves from 96.8% to 97.2% on LIBERO-Spatial and from 85.2% to 87.0% on LIBERO-10, while remaining close on LIBEROObject and LIBERO-Goal. The four-suite average rises from 94.15% to 94.35%. Notably, the strongest gain appears on LIBERO-10, which is consistent with the view that iterative decoding matters most on longer-horizon tasks. 

_C. Threshold scans reveal task-dependent non-monotonicity_ 

Proposition 1 motivates residual thresholding because it bounds the same normalized residual _rk_ used in the experiments. Fig. 2 shows scans on place ~~d~~ ual ~~s~~ hoes and click ~~b~~ ell. For place ~~d~~ ual ~~s~~ hoes, success peaks near _τ_ = 1 _._ 0; for click ~~b~~ ell, the best result occurs at the strictest tested threshold. The preferred threshold is therefore task dependent. 

Fig. 3 gives a single-task view on click ~~a~~ larmclock. EqM inference passes through _early attraction_ , _semantic shaping_ , and _over-refinement_ . We use _stationarity–_ 

TABLE I 

DEPLOYMENT SUCCESS RATES ON THE 19-TASK ROBOTWIN BENCHMARK UNDER A MATCHED 300-STEP BUDGET. THE TWO METHODS SHARE THE SAME UPSTREAM VLA STACK; ONLY THE ACTION DECODER DIFFERS. 

|Task|_π_0|_π_0-EqM|∆|Task|_π_0|_π_0-EqM|∆|
|---|---|---|---|---|---|---|---|
|beat<br>~~b~~lock<br>~~h~~ammer|88|85|_−_3|place<br>~~a~~2b<br>~~r~~ight|30|30|0|
|click<br>~~b~~ell|38|33|_−_5|put<br>~~b~~ottles<br>~~d~~ustbin|42|72|+30|
|click<br>~~a~~larmclock|24|45|+21|stack<br>~~b~~locks<br>~~t~~wo|58|68|+10|
|handover<br>~~b~~lock|24|27|+3|stack<br>~~b~~owls<br>~~t~~hree|68|60|_−_8|
|move<br>~~c~~an<br>~~p~~ot|6|14|+8|turn<br>~~s~~witch|34|34|0|
|move<br>~~p~~layingcard<br>~~a~~way|66|63|_−_3|pick<br>~~d~~iverse<br>~~b~~ottles|20|47|+27|
|place<br>~~p~~hone<br>~~s~~tand|48|55|+7|place<br>~~d~~ual<br>~~s~~hoes|54|45|_−_9|
|place<br>~~c~~an<br>~~b~~asket|36|50|+14|pick<br>~~d~~ual<br>~~b~~ottles|26|66|+40|
|place<br>~~c~~ans<br>~~p~~lasticbox|32|65|+33|place<br>~~o~~bject<br>~~s~~tand|48|56|+8|
|place<br>~~a~~2b<br>~~l~~eft|26|39|+13|||||
|Average|40.4|50.2|+9_._8|||||


### TABLE II 

SUCCESS RATES (%) ON THE FOUR LIBERO BENCHMARK SUITES. 


Fig. 3. Qualitative EqM inference trajectory on click ~~a~~ larmclock, showing early attraction, semantic shaping, and over-refinement. 

itively to LIBERO, and makes stopping depth behaviorally relevant once decoding becomes iterative. The main limitation is scope: the threshold scans cover only two RoboTwin tasks, so the non-monotonic phenomenon is illustrated rather than mapped exhaustively. Proposition 1 is likewise local: it justifies residual thresholding but does not identify the threshold that maximizes task success or provide a global convergence theorem for the learned non-conservative field. More practically, the current study also does not isolate how much of the gain comes from the EqM objective itself versus the stopping rule and warm-start structure. 

At a systems level, the main implication is a cleaner separation between representation learning and deployment-time compute allocation. Once the decoder is time free, one can vary thresholds, iteration caps, or warm-start policies without changing the upstream VLA stack, which turns part of testtime compute into a controllable systems variable rather than a fixed sampler schedule. This perspective may be especially useful in future multi-task and cross-embodiment settings, where the same task-conditioned action field may need to be solved under different latency budgets, action granularities, or robot morphologies. These limitations and opportunities together reinforce the central point that compute allocation in closed-loop VLA should be evaluated behaviorally as well as numerically. 

_executability gap_ for the mismatch between numerical stationarity and physical utility: the iterate with the smallest residual need not execute best. 

Together, Proposition 1 and the threshold scans suggest a two-part reading of early stopping: residual thresholds monitor solver progress, but the best threshold remains task dependent. In closed loop, the threshold is therefore not only a numerical tolerance; it also shapes the deployed action distribution. 

## VI. DISCUSSION AND LIMITATIONS 

The experiments support three observations: EqM improves RoboTwin under matched compute, transfers compet- 

## VII. CONCLUSION 

We presented _π_ 0-EqM, a decoder replacement for _π_ 0 that casts action generation as iterative equilibrium solving. Under a matched 300-step budget, it improves RoboTwin average success from 40.4% to 50.2% across 19 tasks while remaining competitive on LIBERO and improving LIBERO10 from 85.2% to 87.0%. More broadly, the results argue that inference depth is a policy variable in closed-loop VLA rather than a purely numerical afterthought. They also suggest energy-based VLA—especially composable action generation across tasks and embodiments—as a promising direction for future work. 

REFERENCES 

- [1] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu, _et al._ , “RT-1: Robotics transformer for real-world control at scale,” _arXiv preprint arXiv:2212.06817_ , 2022. 

- [2] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, _et al._ , “RT-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 

- [3] O. M. Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, _et al._ , “Octo: An open-source generalist robot policy,” _arXiv preprint arXiv:2405.12213_ , 2024. 

- [4] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, _et al._ , “OpenVLA: An open-source vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 

- [5] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, _et al._ , “ _π_ 0: A visionlanguage-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [6] Y. Lipman, R. T. Chen, H. Ben-Hamu, M. Nickel, and M. Le, “Flow matching for generative modeling,” _arXiv preprint arXiv:2210.02747_ , 2022. 

- [7] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” _The International Journal of Robotics Research_ , vol. 44, no. 10-11, pp. 1684–1704, 2025. 

- [8] R. Wang and Y. Du, “Equilibrium matching: Generative modeling with implicit energy-based models,” _arXiv preprint arXiv:2510.02300_ , 2025. 

- [9] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” _arXiv preprint arXiv:2304.13705_ , 2023. 

- [10] Y. Tassa, N. Mansard, and E. Todorov, “Control-limited differential dynamic programming,” in _2014 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2014, pp. 1168–1175. 

- [11] B. Amos, I. Jimenez, J. Sacks, B. Boots, and J. Z. Kolter, “Differentiable mpc for end-to-end planning and control,” _Advances in neural information processing systems_ , vol. 31, 2018. 

- [12] Y. Du and I. Mordatch, “Implicit generation and modeling with energy based models,” _Advances in Neural Information Processing Systems_ , vol. 32, 2019. 

- [13] P. Florence, C. Lynch, A. Zeng, O. A. Ramirez, A. Wahid, L. Downs, A. Wong, J. Lee, I. Mordatch, and J. Tompson, “Implicit behavioral cloning,” in _Conference on Robot Learning_ . PMLR, 2022, pp. 158– 168. 

- [14] Z. Zhang, R. Huang, Y. Liu, S. Zhu, L. Mou, and H. Zhao, “Generative control as optimization: Time unconditional flow matching for adaptive and robust robotic control,” in _ICLR 2026 Workshop on Lifelong Agents: Learning, Aligning, Evolving_ . 

- [15] T. Chen, Z. Chen, B. Chen, Z. Cai, Y. Liu, Z. Li, Q. Liang, X. Lin, Y. Ge, Z. Gu, _et al._ , “RoboTwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation,” _arXiv preprint arXiv:2506.18088_ , 2025. 

- [16] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “LIBERO: Benchmarking knowledge transfer for lifelong robot learning,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 44 776–44 791, 2023. 

