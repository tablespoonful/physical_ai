---
title: "ROBUSTVLA: ROBUSTNESS-AWARE REINFORCE- MENT POST-TRAINING FOR VISION-LANGUAGE- ACTION MODELS"
venue: "Submitted to ICLR 2026"
original: "ICLR 2026 投稿時の匿名版"
url: https://arxiv.org/abs/2511.01331
pdf: https://arxiv.org/pdf/2511.01331
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.01331)** / [論文ページ](https://arxiv.org/abs/2511.01331)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。
> ICLR 2026 投稿時の匿名版から変換しました。リンク先の公開版とは内容が異なる場合があります。

Under review as a conference paper at ICLR 2026 

**000** 

# **000** ROBUSTVLA: ROBUSTNESS-AWARE REINFORCE- **001 002** MENT POST-TRAINING FOR VISION-LANGUAGE- **003 004** ACTION MODELSCTION MODELS MODELSODELS 

**003 004** ACTION MODELSCTION MODELS MODELSODELS **005 006 Anonymous authors 007** Paper under double-blind review **008 009 010 011** ABSTRACT **012 013** Vision-Language-Action (VLA) models have recently emerged as powerful **014** general-purpose policies for robotic manipulation, benefiting from large-scale **015** multi-modal pre-training. However, they often fail to generalize reliably in outof-distribution deployments, where unavoidable disturbances such as observation **016** noise, sensor errors, or actuation perturbations become prevalent. While recent **017** Reinforcement Learning (RL)-based post-training provides a practical means to **018** adapt pre-trained VLA models, existing methods mainly emphasize reward max- **019** imization and overlook robustness to environmental uncertainty. In this work, we **020** introduce **RobustVLA** , a lightweight online RL post-training method designed **021** to explicitly enhance the resilience of VLA models. Through a systematic ro- **022** bustness analysis, we identify two key regularizations: Jacobian regularization, **023** which mitigates sensitivity to observation noise, and smoothness regularization, **024** which stabilizes policies under action perturbations. Extensive experiments across **025** diverse robotic environments demonstrate that RobustVLA significantly outper- **026** forms prior state-of-the-art methods in robustness and reliability. Our results highlight the importance of principled robustness-aware RL post-training as a key step **027** toward improving the reliability and robustness of VLA models. **028** 

**029** 

**030** 

## 1 INTRODUCTION 

**031** 

**032** Vision-Language-Action (VLA) models have emerged as a powerful paradigm for general-purpose **033** robotic manipulation, with representative examples including RT-1 (Brohan et al., 2022), RT- **034** 2 (Zitkovich et al., 2023), OpenVLA (Kim et al., 2024), and _π_ 0 (Black et al., 2024). These VLA **035** models demonstrate the feasibility of learning universal robotic policies from large-scale multimodal **036** datasets and have achieved remarkable performance across a variety of manipulation tasks. Despite **037** these advances, recent studies (Xing et al., 2025; Shi et al., 2025) reveal that the generalization ability **038** of pre-trained VLA models remains limited when deployed in Out-of-Distribution (OOD) scenarios. **039** The OOD scenarios in this work primarily refer to variations in the distribution of perception and execution levels. These variations are caused by unseen visual conditions (lighting, occlusion, cam- **040** era changes, etc.) and execution disturbances (action noise). One key reason is that VLA models **041** may rely on spurious correlations between irrelevant observation features and actions, rather than **042** capturing the true causal relationship required for robust generalization (Xing et al., 2025). **043** 

**044** A natural solution for OOD tasks is Supervised Fine-Tuning (SFT) with task-specific data. However, **045** SFT approaches based on imitation learning rely heavily on costly, high-quality human demonstrations. When only a limited number of demonstrations are available, their effectiveness drops sharply. **046** In contrast, online Reinforcement Learning (RL) provides an appealing alternative by enabling au- **047** tonomous data collection and policy refinement in deployment (Lu et al., 2025; Liu et al., 2025; Shu **048** et al., 2025; Chen et al., 2025c; Tan et al., 2025a). However, while recent online RL-based post- **049** training methods enable autonomous adaptation without requiring large amounts of expert demon- **050** strations, they are not inherently designed to guarantee robustness against environmental pertur- **051** bations. General RL fine-tuning focuses on maximizing task-specific reward signals in nominal **052** environments, but does not explicitly regularize the sensitivity of the VLA model to environmental **053** noise. Such optimized models are often over-adapted to the specific dynamics of the post-training environment and become brittle to even slight perturbations. This limitation highlights the need for 

1 

Under review as a conference paper at ICLR 2026 

**054** 

principled approaches that not only optimize for task performance, but also explicitly constrain the **055** sensitivity of the model’s decision process to perturbations. Such robustness-oriented post-training **056** is crucial for ensuring reliable deployment of VLA models in real-world environments. 

**057** 

**058** Environmental perturbations can arise from multiple sources and affect different stages of the modelenvironment interaction (Gu et al., 2025). Currently, we focus on two fundamental types: observa- **059** tion perturbations and action perturbations. Observation perturbations reflect inaccuracies in per- **060** ception, caused by sensor noise, latency, or imperfect state estimation, which lead to mismatches **061** between the perceived and actual environment state. Action perturbations, on the other hand, arise **062** from actuation errors, implementation inaccuracies, or hardware-level disturbances, which cause de- **063** viations between the intended and executed actions. These two perturbations, which are ubiquitous **064** in real-world robotic systems, can be effectively modeled as random noise applied to the sequential **065** decision-making process (Duan et al., 2016). Furthermore, if not properly addressed, these pertur- **066** bations can amplify over time and significantly degrade model performance. Thus, a significant **067** gap remains: _ensuring the robustness of post-training to environmental perturbations, so that the_ **068** _resulting VLA model is stable and reliable in autonomous interactions._ **069** To this end, we propose **RobustVLA** , a concise and effective online RL post-training method de- **070** signed to enhance the robustness of pre-trained VLA models under environmental perturbations. **071** Our method is grounded in the robustness analysis of performance deviations induced by perturba- **072** tions. We first establish explicit upper bounds on the robustness gap in the presence of observation **073** and action perturbations, respectively. We then extend this analysis to the case where both types of **074** perturbations coexist. Our findings highlight that the robustness gap under observation perturbations **075** is governed by the Jacobian sensitivity of the VLA model, whereas under action perturbations it is controlled by the smoothness of the VLA model update. This theoretical insight naturally motivates **076** the introduction of Jacobian and smoothness regularization into the online RL fine-tuning process, **077** which together constrain the worst-case robustness gap and promote robust decision-making. The **078** main contributions of this work are summarized as follows: **079 080** • We introduce RobustVLA, a lightweight online RL post-training method that enhances the **081** robustness of VLA models against environmental perturbations. **082** • We conduct three robustness analyses to performance deviations caused by observation and **083** action perturbations, which induce explicit VLA model regularization optimization terms. **084** • Extensive experiments demonstrate that RobustVLA exhibits superior resistance to envi- **085** ronmental uncertainties and perturbations compared to state-of-the-art VLA baselines, re- **086** sulting in more reliable and stable behavior. **087** 

- Extensive experiments demonstrate that RobustVLA exhibits superior resistance to environmental uncertainties and perturbations compared to state-of-the-art VLA baselines, resulting in more reliable and stable behavior. 

**088 089** 

## 2 RELATED WORK 

**090 RL for VLA Models.** Recently, a growing body of research has explored RL as a mechanism **091** to adapt VLA models to complex embodied tasks. The first research direction emphasizes offline **092** RL training, where large-scale policy optimization can be performed without expensive online in- **093** teractions. Previous work proposed the Q-Transformer (Chebotar et al., 2023), introducing au- **094** toregressive offline Q-learning with a Transformer. Subsequently, in the work by ReinboT (Zhang **095** et al., 2025c), researchers proposed an end-to-end VLA model that incorporates the RL principle **096** of maximizing cumulative return. Further work has proposed an offline RL post-training algorithm, **097** ARFM (Zhang et al., 2025b), for VLA flow models to boost the performance of VLA models on **098** downstream tasks. Moreover, some work has focused on online RL fine-tuning of VLA models. **099** FLaRe (Hu et al., 2024) employs large-scale domain randomized RL fine-tuning, and PA-RL (Mark et al., 2024) unifies offline and online RL across policy categories. IRe-VLA (Guo et al., 2025), **100** RIPT-VLA (Tan et al., 2025a), and VLA-RL (Lu et al., 2025) are specifically designed to stabi- **101** lize or extend online RL training of VLA models. Furthermore, optimization advances such as **102** TGRPO (Chen et al., 2025c) and RFTF (Shu et al., 2025) improve the efficiency of fine-tuning in **103** trajectory or sparse reward settings. RLDG (Xu et al., 2024) refines task-specific RL into a gen- **104** eral VLA, ConRFT (Chen et al., 2025b) combines offline Q-learning with consistency-based online **105** fine-tuning, and ReWiND (Zhang et al., 2025d) introduces a language-guided reward model for fast **106** task adaptation without the need for new demonstrations. Moreover, several works have focused on **107** training value functions for visual-language manipulation tasks to align VLA models with downstream tasks, including Bellman-Guided Retrials (Du et al., 2024), V-GPS (Nakamoto et al., 2024), 

2 

Under review as a conference paper at ICLR 2026 

**108** and Hume (Song et al., 2025) However, previous work has often neglected the robustness and reli- **109** ability of robotic visual-language manipulation under environmental perturbations and distribution **110** changes, which is precisely the focus of our work. More related works are in Appendix A.1. **111 112 Robust RL.** Robust RL generally studies how to ensure stability and generalization under dis- **113** tribution shifts, noisy observations, and adversarial perturbations. Classical approaches leverage **114** robust MDP formulations (Iyengar, 2005; Wiesemann et al., 2013) and adversarial training (Pinto **115** et al., 2017). Modern deep RL has introduced diverse techniques, including domain randomiza- **116** tion for sim-to-real transfer (Tobin et al., 2017; Van et al., 2025) and methods for offline and cur- **117** riculum learning (Dennis et al., 2020; Wu et al., 2024). Recently, the field has advanced towards **118** theoretically-grounded distributionally robust optimization (Li et al., 2024; Cui et al., 2025; He et al.) with provable finite-sample guarantees (Ghosh et al., 2025; Roch et al., 2025). However, **119** the online setting where an agent learns via direct interaction is less studied. A key challenge, un- **120** addressed by previous work that often assumes access to exploratory policies (Wang & Zou, 2021; **121** Badrinath & Kalathil, 2021), is to handle exploration and robustness simultaneously. Crucially, this **122** focus on test-time robustness to environmental shifts distinguishes distributionally robust RL from **123** corruption-robust RL, which handles corrupted training data (Lykouris et al., 2021; Wei et al., 2022; **124** Zhang et al., 2022; Ye et al., 2024; 2023). Different from these, our work focuses on the post-training **125** of VLA models for general task settings, aiming to simultaneously address model adaptability and **126** stability issues within a unified model framework. **127 128** 3 PRELIMINARIES **129 130 RL post-training of VLA model.** We model the task as a Markov Decision Process (MDP) (Sutton **131** et al., 1998). The VLA model _πθ_ maps a natural language instruction _g_ and a sequence of observa- **132** tions _o_ 1: _t_ and previous actions _a_ 1: _t−_ 1 to a probability distribution over the current action _at_ . Each **133** episode is initialized with the context **c** = ( _g, o_ 1). The state _st_ is represented as [ _g, o_ 1: _t, a_ 1: _t−_ 1]. **134** At each time step _t_ , _πθ_ samples an action from the model distribution: _at ∼ πθ_ ( _· | g, o_ 1: _t, a_ 1: _t−_ 1). **135** The environment _E_ transitions to the next state _st_ +1 = [ _g, o_ 1: _t_ +1 _, a_ 1: _t_ ]. The environment _E_ also **136** returns a binary reward _rt_ = 1 if the task goal is achieved, and _rt_ = 0 otherwise. The goal of **137** _πθ_ is to maximize the undiscounted task reward: _J_ ( _πθ_ ) = E _τ ∼πθ_ [<sup>�</sup><sup>_H_</sup> _t_ =1<sup>_rt_]</sup><sup>_,_where</sup><sup>_H_is the rollout</sup> **138** horizon. To optimize this objective, policy gradient (Sutton et al., 1999) is a simple and efficient **139** method: _∇θJ_ ( _πθ_ ) = E **a** _∼πθ_ [ _∇θ_ log _πθ_ ( **a** _|_ **c** ) _A_ ( **c** _,_ **a** )] _,_ where _A_ ( **c** _,_ **a** ) is the advantage function, which indicates how good the action **a** is compared to the baseline. However, the accurate estima- **140** tion of _A_ ( **c** _,_ **a** ) is tricky, especially in the post-training phase of VLA models. To alleviate this issue, **141** recent work (Chen et al., 2025a) proposed a critic-free optimization framework. Specifically, for **142** each sampling context **c** , we can draw _K_ rollouts _{_ **a** _k ∼ πψ_ ( _· |_ **c** ) _}_<sup>_K_</sup> _k_ =1<sup>under a sampling model</sup><sup>_πψ_.</sup> **143** Each rollout receives a reward _rk_ = _r_ ( **c** _,_ **a** _k_ ). The leave-one-out baseline for rollout _k_ is calculated **144** by averaging the other rewards (Kool et al., 2018): _Ak_ = _rk − K_ <u>1</u> _−_ 1 � _j̸_ = _k_<sup>_rj._Thisallowsusto</sup> **145** bypass the cumbersome task of learning a value function and efficiently compute a stable advan- **146** tage signal. Furthermore, to utilize the collected rollouts _{_ ( **c** _k,_ **a** _k, Ak_ ) _}_ to update _πθ_ , we compute **147** the importance ratio: _ηk_ = _πθ_ ( **a** _k |_ **c** _k_ ) _/πψ_ ( **a** _k |_ **c** _k_ ), where _πθ_ is the current update model and **148** _πψ_ is a sampling model. We then optimize _πθ_ utilizing the Proximal Policy Optimization (PPO) **149** objective (Schulman et al., 2017): **150** _L_ PPO = _−_ min ( _ηiAi,_ clip ( _ηi,_ 1 _− ϵ,_ 1 + _ϵ_ ) _Ai_ ) _,_ (1) **151** where _ϵ_ is an update threshold. This objective encourages rollouts with positive advantages while **152** preventing _πθ_ from deviating significantly from the sampling model _πψ_ . **153 Environmental Perturbations During RL Post-Training.** We formalize the robust post-training **154** problem of VLA model _πθ_ under environmental perturbations. At each time step _t_ in MDP, the _πθ_ **155** receives a perturbed observation ˜ _st_ of the true state _st_ , with deviation bounded by _∥s_ ˜ _t−st∥≤ ϵs._ The **156** action selected by the _πθ_ may be corrupted by execution noise, modeled as Gaussian perturbations: **157** _at_ = _πt_ (˜ _st_ ) + _ξt_ , where _ξt ∼N_ (0 _, σ_<sup>2</sup> _Id_ ). The environment evolves according to a Lipschitz **158** continuous transition function _f_ , ensuring that small deviations in states or actions yield bounded **159** deviations in subsequent states. The environmental dynamics _f_ ( _s, a_ ) and the reward function _r_ ( _s, a_ ) **160** are Lipschitz continuous and are constants _Lf_ and _Lr_ , respectively. Finally, we denote by _ϵ_ offline **161** the discrepancy between the initial VLA model _πinit_ , obtained via imitation learning, and the expert model _π_<sup>_∗_</sup> . This discrepancy provides the starting error baseline for the online post-training process. 

3 

Under review as a conference paper at ICLR 2026 

**162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215** 


Figure 1: The proposed RobustVLA method. Due to the presence of environmental uncertainty during online RL interactions, we consider observation noise (sensor/camera corruptions) and action noise (Gaussian actuation errors), and their joint effect. Moreover, we conduct robustness theoretical analysis based on these three aspects, establishing error amplification bounds, return drift control, and robust stability guarantees. Finally, we derive regularized optimization objectives, including the model Jacobian and action smoothing regularization, as well as the robust RL post-training objective. 

## 4 METHODOLOGY 

In this work, we propose a novel robust online RL post-training method, RobustVLA, for VLA models under environmental perturbations (Fig. 1). We first analyze the robustness bounds of the VLA model under random environmental perturbations. We then discuss how to derive post-training objectives based on these analyses and finally propose a concise online RL fine-tuning algorithm. 

### 4.1 ROBUSTNESS ANALYSIS TO ENVIRONMENTAL PERTURBATIONS 

In the perturbed online RL post-training of the VLA model, we observed two main sources of robustness degradation. First, these models are highly sensitive to small changes in visual input: slight shifts in lighting, occlusions, or camera noise can cause disproportionately large changes in the model’s latent representation and therefore in its actions. This motivates explicitly constraining how sharply the model reacts to observation changes. Second, when the model is updated online, its behavior can change abruptly from one iteration to the next. Even small gradient steps may lead to large jumps in the produced actions, which become unstable when combined with the stochasticity of realistic execution. To stabilize this process, we also need to control how quickly the model is allowed to evolve during post-training. Therefore, in this section, we theoretically quantify how different types of perturbations affect the robustness of the VLA model. 

**Theorem 1** ( **Error Amplification Bound** ) **.** _Assume perturbed observations s_ ˜ _t_ = _st_ + _δs_<sup>_twith_</sup> _∥δs_<sup>_t∥≤ϵs, and bounded Jacobian ∥∇sπt_(</sup><sup>_s_)</sup><sup>_∥≤λ.Then:_</sup> 


Here the factor _L_<sup>_H_</sup> _f_<sup>corresponds to the worst-case geometric amplification under</sup><sup>_Lf_-Lipschitz dy-</sup> namics; when _Lf <_ 1 the bound becomes strictly smaller. Theorem 1 indicates that the robustness gap under observation perturbations is governed by the product _λϵs_ , where _λ_ measures the VLA model’s local sensitivity and _ϵs_ quantifies the observation noise level. Conversely, enforcing Jacobian regularization to shrink _λ_ directly reduces the error propagation term _λϵs_ , thereby bounding _J_ ( _π_<sup>_∗_</sup> ) _− J_ ( _π_ ) more tightly. 

**Theorem 2** ( **Return Drift Control** ) **.** _Assume actions are perturbed as at_ = _πt_ ( _st_ ) + _ξt with ξt ∼N_ (0 _, σ_<sup>2</sup> _Id_ ) _, and VLA models satisfy ∥πi − πi−_ 1 _∥∞ ≤ δi. Then:_ 


4 

Under review as a conference paper at ICLR 2026 

**216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269** 

Here, _N_ represents the number of times the model parameters are updated. Theorem 2 reveals that the return gap under action perturbations has two additive drivers: **1)** the cumulative VLA model drift<sup>�</sup><sup>_N_</sup> _i_ =1<sup>_δi_,whichreflectsthenonstationarityofonlineupdates,and</sup><sup>**2)**thestochasticexecution</sup> noise term _σ_ _~~√~~ d_ , which is irreducible and scales with action dimension _d_ . The presence of<sup>�</sup><sup>_N_</sup> _i_ =1<sup>_δi_</sup> shows that if VLA model updates are too aggressive (large _δi_ ), then even in the absence of large execution noise ( _σ ≈_ 0), the compounding drift will destabilize rollouts and inflate _J_ ( _π_<sup>_∗_</sup> ) _− J_ ( _π_ ). This means smoothness regularization _−−_ enforcing _δi_ to be small _−−_ is essential to decouple online learning progress from robustness degradation, ensuring that long-horizon performance does not deteriorate due to accumulated VLA model shifts. 

**Theorem 3** ( **Robust Stability Guarantee** ) **.** _Under both observation and action perturbations, and both Jacobian and smooth regularizations, the return gap satisfies:_ 


Theorem 3 shows that when both observation and action perturbations are present, the return gap depends jointly on the observation–sensitivity term _λϵs_ , and the accumulated update drift<sup>�</sup><sup>_N_</sup> _i_ =1<sup>_δi_.</sup> Unlike the single-perturbation cases, here the deviation caused by noisy observations does not remain localized: it propagates through the dynamics, influences later states, and interacts with execution noise and model drift across the entire rollout. This nested feedback structure implies that robustness cannot be achieved by controlling only one source of error. Instead, Jacobian regularization (which reduces the instantaneous sensitivity _λ_ ) and smoothness regularization (which limits updateinduced drift _δi_ ) must be applied jointly to prevent compounding error growth over long horizons. This result highlights that robust VLA post-training fundamentally requires a dual regularization strategy; ignoring either perturbation channel will allow errors to accumulate through the dynamics and ultimately destabilize the VLA model. More robustness analysis is in the Appendix A.2. 

### 4.2 MODEL ONLINE REGULARIZATION OPTIMIZATION OBJECTIVE 

The robustness analysis in Section 4.1 suggests two complementary levers: **1)** Jacobian regularization to suppress error amplification from observation noise, achieved by penalizing the sensitivity of the model with respect to its input states. **2)** Smoothness regularization to stabilize online updates against action perturbations, achieved by penalizing deviations between consecutive models. In our implementation, Jacobian regularization is realized by computing the gradient of the logaction probability with respect to the observation input: _∇s_ log _πθ_ ( _a|s_ ) _._ Specifically, we compute the squared norm of this gradient across a batch of observations, average the result, and then apply a clamp operation to prevent excessively large penalties: 


where _Gmax_ is the gradient clamp parameters. The theoretical justification for applying Jacobian regularization on the log-probability rather than the raw probability distribution comes from a norm comparison argument. Since the model _πθ_ ( _a|s_ ) is a probability distribution, which induces the following relationship: �� _∇sπθ_ ( _a|s_ )�� _F ≤_ �� _∇s_ log _πθ_ ( _a|s_ )�� _F_<sup>_._Thisisbecause</sup><sup>_∇s_log</sup><sup>_πθ_(</sup><sup>_a|s_)=</sup> _∇sπθ_ ( _a|s_ ) _/πθ_ ( _a|s_ ) _,_ and since 0 _< πθ_ ( _a|s_ ) _≤_ 1, dividing by _πθ_ ( _a|s_ ) only enlarges the magnitude of the gradient. Consequently, any control on _∥∇s_ log _πθ_ ( _a|s_ ) _∥F_ automatically controls _∥∇sπθ_ ( _a|s_ ) _∥F_ as well, but in a stronger sense. This directly penalizes large sensitivity coefficients, aligning with the bound in Theorem 1. 

On the other hand, Theorem 2 states that the return gap can be bounded in terms of the worstcase deviation _δi_ = sup _s∈S ∥πθ_ ( _·|s_ ) _− πθ−_ ( _·|s_ ) _∥∞_ , which captures the maximum discrepancy between the new and old models across the entire state space. Although this characterization is theoretically precise, computing or constraining _δi_ directly is infeasible in practice, especially in continuous action domains. To operationalize this idea, we introduce easy-to-handle alternatives. First, the PPO objective already constrains the average distributional shift through a KL divergence penalty: E _s∼D_ <u>�</u> _D_ KL� _πθ_ ( _·|s_ ) _∥ πθ−_ ( _·|s_ )�<sup><u>�</u></sup> _≤ ϵ._ By Pinsker’s inequality, this implies _∥πθ_ ( _·|s_ ) _− πθ−_ ( _·|s_ ) _∥_ 1 _≤_ ~~�~~ 2 _D_ KL� _πθ_ ( _·|s_ ) _∥πθ−_ ( _·|s_ )� _,_ thus providing an average-case upper bound 

5 

Under review as a conference paper at ICLR 2026 

**270 Algorithm 1** Robust online RL Post-Training for VLA Models **271 Input:** Pretrained VLA model _πθ_ , rollout buffer _D_ rollout, Jacobian weight _α_ , smoothness weight _β_ , **272** gradient clamp _G_ max, noise range ( _ϵ_ min _, ϵ_ max), success rate thresholds ( _τ_ low _, τ_ high). **273 274** 1: Initialize reference model _πθ− ← πθ_ , noise level _ϵ ← ϵ_ min, success moving average _pMA ←_ 0 2: **for** _m ←_ 1 **to** _M_ **do 275 276** 3: Collect trajectories _D_ rollout with observation/action noise _ϵ_ 4: **for** _n ←_ 1 **to** _N_ **do 277** 5: Sample minibatch ( _si, ai, Ai_ ) _∼D_ rollout **278 279** 6: Jacobian penalty: _R_ Jac = E _i_ � min( _∥∇si_ log _πθ_ ( _ai|si_ ) _∥_ 2<sup>2</sup><sup>_, G_max)</sup> � 7: Action-smooth penalty: _R_ Smooth = E _i_ [ _∥µθ_ ( _si_ ) _− µθ−_ ( _si_ ) _∥_ 2<sup>2]</sup> **280** 8: Robust objective: _L_ RobustVLA = _L_ PPO + _αR_ Jac + _βR_ Smooth **281** 9: Update _θ ← θ − η∇θL_ RobustVLA **282** 10: **end for 283** 11: Update reference _πθ− ← πθ_ **284** 12: **if** _m_ % _I_ interval = 0 **then 285** 13: Evaluate model _πθ_ , obtain success rate _p_ **286** 14: Update moving average _pMA ← γp_ + (1 _− γ_ ) _pMA_ **287** 15: **if** _pMA > τ_ high: _ϵ ←_ min( _ϵ_ + ∆ _, ϵ_ max) **288** 16: **else if** _pMA < τ_ low: _ϵ ←_ max( _ϵ −_ ∆ _, ϵ_ min) 17: **end if 289** 18: **end for 290** 19: **Return** finetuned robust VLA model _πθ_ **291 292 293 294** on model deviation. However, the KL penalty tends to be sensitive to variance changes and does not necessarily prevent large shifts in the mean action outputs. To complement this, we further introduce **295** a smoothness regularizer that explicitly penalizes deviations in the model means: **296 297** _R_ Smooth( _θ_ ) = E _s∼D ∥µθ_ ( _s_ ) _− µθ−_ ( _s_ ) _∥_ 2<sup>2</sup> _,_ (3) **298** � � **299** where _µθθ_ ( _s_ ) denotes the mean action. This regularizer directly bounds the displacement of the mean denotes the mean action. This regularizer directly bounds the displacement of the mean **300** actions, which in turn controls a surrogate of _δii_ in expectation. Intuitively, while the KL constraint **301** ensures distribution-level stability, the _R_ Smooth enforces gradual updates in the action means, thereby enforces gradual updates in the action means, thereby **302** preventing erratic model shifts that may otherwise amplify error accumulation. This dual mechanism **303** _−−_ average KL regularization together with mean-level _L_ 2 smoothing _−−_ serves as a practical **304** surrogate for bounding _δii_ , thus aligning the algorithmic implementation with the theoretical insights **305** of Theorem 2. Therefore, taking these regularization terms into consideration, we obtain a robust **306** online RL optimization objective: **307** _L_ RobustVLA( _θ_ ) = _L_ PPO( _θ_ ) + _α R_ Jac( _θ_ ) + _β R_ Smooth( _θ_ ) _,_ (4) **308 309** where _α_ and _β_ are hyperparameters controlling the strength of each robustness component. This **310** formulation preserves the general PPO advantage-based policy improvement while explicitly con- **311** straining the two key robustness channels identified in our analysis: sensitivity to observation perturbations ( _α_ term) and stability under action noise and online updates ( _β_ term). As a result, _L_ RobustVLA **312** naturally operationalizes the theoretical bounds, guiding the learning process toward VLA models **313** that are both performant and robust under environmental perturbations. **314 315** 4.3 ROBUST POST-TRAINING ALGORITHM IMPLEMENTATION **316 317** Based on the constructed robust RL optimization objective (Equ. 4), we can design a lightweight **318** VLA model post-training algorithm as shown in Algo. 1. The algorithm retains the rollout-collection **319** and model-update structure of PPO, but crucially incorporates three key components beyond the **320** standard objective. First, the Jacobian penalty _R_ Jac suppresses the sensitivity of the model to input **321** perturbations by penalizing large gradients of log _πθ_ ( _a|s_ ) with respect to observations. Second, the **322** action-smooth penalty _R_ Smooth constrains the change of action distributions between consecutive **323** model updates, thereby ensuring temporal consistency. Finally, to further enhance robustness in practice, we adopt a curriculum-based adaptive noise scheduling mechanism: the level of injected 

where _µθθ_ ( _s_ ) denotes the mean action. This regularizer directly bounds the displacement of the mean denotes the mean action. This regularizer directly bounds the displacement of the mean actions, which in turn controls a surrogate of _δii_ in expectation. Intuitively, while the KL constraint ensures distribution-level stability, the _R_ Smooth enforces gradual updates in the action means, thereby enforces gradual updates in the action means, thereby preventing erratic model shifts that may otherwise amplify error accumulation. This dual mechanism _−−_ average KL regularization together with mean-level _L_ 2 smoothing _−−_ serves as a practical surrogate for bounding _δii_ , thus aligning the algorithmic implementation with the theoretical insights of Theorem 2. Therefore, taking these regularization terms into consideration, we obtain a robust online RL optimization objective: 

6 

Under review as a conference paper at ICLR 2026 

**324** observation and action noise is gradually increased or decreased based on the model’s smoothed suc- **325** cess rate. This strategy prevents premature destabilization during training, while gradually exposing **326** the model to stronger perturbations as competence improves. Together, these design choices ensure **327** that the model update not only maximizes advantages under the PPO surrogate loss, but also main- **328** tains robustness against both observation and action perturbations, thereby grounding the theoretical **329** analysis into a practical and implementable training scheme. **330 331 332** 5 EXPERIMENTAL EVALUATION **333 334** In this section, we conduct extensive experiments in various scenarios to evaluate the effectiveness **335** of the proposed RobustVLA. Specifically, we aim to examine the three key questions: **1)** Does Ro- **336** bustVLA outperform state-of-the-art offline and online baseline methods in perturbed environment **337** settings? **2)** How does RobustVLA perform in online transfer learning under perturbed scenarios? **338 3)** How do the core components of RobustVLA affect the overall performance? **339 340** 5.1 PERFORMANCE EVALUATION UNDER ENVIRONMENTAL PERTURBATIONS **341 342 Experimental setup.** To comprehensively **(a) Observation Perturbation (b) Action 343** evaluate the performance of the RobustVLA, **Original Image Image Shift Image Rotation Perturbation 344** we construct a robust testing benchmark based **345** on the LIBERO (Liu et al., 2023) simulation **346** platform that incorporates environmental un- **347** certainty and perturbations, as shown in Fig. 2. **348** The original LIBERO benchmark is a long- **Color Jitter Image Occlusions Image Erasing Action Noise 349** horizon robotic learning suite consisting of **Ob350 jects** , **Long** , **Spatial** , and **Goal** . We impose five observation perturbations and three action **351** perturbations during the online interaction be- **352** tween the VLA model and the environment. **353** The five observation perturbations are Image Figure 2: Robust VLA benchmarks based on the **354 Shift** , Image **Rotation** , **Color** Jitter, Image **Oc-** LIBERO include two types: **a)** observation pertur- **355 clusions** , and Image **Erasing** . The three action bation and **b)** action perturbation. **356** perturbations are zero-mean Gaussian action noise with standard deviations of **0.1** , **0.2** , and **0.3** . **357** Details of the observation perturbations are in Appendix A.4. For model evaluation, we follow the **358** common scheme of previous work (Tan et al., 2025a), where a single VLA model is deployed to all **359** tasks in the suite, and the deployment is performed on 50 held-out test contexts for each task. **360 361 Baselines.** Our proposed algorithm comes in two versions: one without curriculum learning **362** ( **RobustVLA** ) and one with curriculum learning ( **RobustVLA-C** ). For a thorough comparison, three **363** categories of state-of-the-art baseline models are considered. The first category is Offline Imitation **364** Learning ( **Offline IL** ) models, which are trained solely on static expert datasets. These include: **365 1)** GEVRM (Zhang et al., 2025a): This model uses prototype contrastive learning to resist obser- **366** vation perturbations. **2)** OpenVLA (Kim et al., 2024), which represents robot actions as discrete **367** token sequences and predicts them one by one in sequence. **3)** OpenVLA-OFT (Kim et al., 2025), **368** which follows the OpenVLA modeling philosophy and further proposes improvements such as par- **369** allel decoding. **4)** _π_ 0 (Black et al., 2024), a VLA flow model that effectively models multi-modal distributions. The second category is Offline Reinforcement Learning ( **Offline RL** ) models, which **370** apply RL algorithms to offline datasets to more fully capture the data quality distribution. These in- **371** clude: **5)** RWR (Peters & Schaal, 2007), which optimizes the model by performing reward-weighted **372** regression on samples. **6)** ReinboT (Zhang et al., 2025c), which guides VLA action generation by **373** predicting densely maximized future returns. **7)** ARFM (Zhang et al., 2025b), a fine-tuning algo- **374** rithm that adaptively adjusts the weights of a flow-matching RL loss. The final category is Online **375** Reinforcement Learning ( **Online RL** ) models, which fine-tune a pre-trained VLA model by au- **376** tonomously interacting with the environment. This includes **8)** RIPT-VLA (Tan et al., 2025a), a **377** critic-free fine-tuning algorithm that uses only sparse binary success rewards. The implementation details of our method and the reproduction of the baseline algorithm are shown in Appendix A.5. 

7 

Under review as a conference paper at ICLR 2026 

**378** Table 1: Average Success Rate (SR) (%) under five observation perturbations. The best results are **379** highlighted in bold, and the second-best results are underlined. **380 381 Observation Perturbation Model Type Models Avg. 382** Shift Rotation Color Occlusions Erasing **383** _π_ 0 31.2 49.5 78.5 88.3 85.2 66.5 **384** GEVRM **46.4** 57.9 56.4 59.8 63.3 56.8 Offline IL **385** OpenVLA 25.4 41.6 48.5 75.5 73.6 47.9 **386** OpenVLA-OFT 40.2 75.1 **95.9** 95.2 96.4 80.6 RWR 16.3 37.1 74.8 88.2 83.6 60.0 **387** Offline RL ARFM 11.9 45.0 75.5 88.0 84.0 60.9 **388** ReinboT 19.8 37.1 74.4 89.1 84.9 61.0 **389** RIPT-VLA 39.5 79.0 95.1 95.0 95.6 80.8 **390** Online RL **RobustVLA** <u>42.1 82.6 95.6</u> **95.7 96.9 82.5 391 RobustVLA-C** 41.1 **82.8** 92.3 <u>95.5 96.5 82.2</u> **392 393** Table 3: Average SR (%) of the four LIBERO **394** Table 2: Average SR (%) under action perturbasuites under joint perturbations. **395** tions (noise level = 0.1, 0.2, 0.3). **396 Joint Perturbation 397 Models Action Perturbation** 0.1 0.2 0.3 **Avg. Models** Spatial Object Goal Long **Avg. 398** _π_ 0 77.5 42.5 18.4 46.1 GEVRM _π_ 0 59.078.6 33.242.0 56.267.8 35.033.4 45.955.5 **399400** OpOpenVLAenVLA-OFTRWR 53.687.480.6 39.252.344.8 11.720.720.8 34.853.548.7 OpOpenVLAenVLA-OFT 20.484.2 71.21.8 21.081.6 40.80.0 10.869.5 RWR 60.4 39.6 53.6 38 47.9 **401** ARFM 81.1 48.2 21.1 50.1 ARFM 58.0 36.6 54.6 37.2 46.6 ReinboT 80.3 47.0 21.2 49.5 **402** RIPT-VLA 84.7 48.1 18.8 50.5 ReinboT 59.0 40.4 56.6 38.8 48.7 RIPT-VLA 86.0 <u>72.2 82.2</u> 72.2 78.2 **403 RobustVLA** <u>88.5 53.1</u> **22.7 54.8 RobustVLA** <u>88.2</u> 68.2 **83.0** <u>75.2 78.7</u> **RobustVLA-C 88.9 53.3** <u>21.8 54.7</u> **404 RobustVLA-C 89.6 82.0** 79.2 **77.6 82.1 405 406 407 Observation Perturbation Settings.** To evaluate the model’s ability to cope with uncertainty in **408** environmental observations, we perturb both the first- and third-view inferences during autonomous **409** interaction. The average success rates are shown in Tab. 1 and Appendix Tab. 4. The results show **410** that our proposed method has the best resistance to observation perturbations compared to all other **411** baselines, with average SR of 82 82 _._ 5% and 82 and 82 82 _._ 2% for RobustVLA and RobustVLA-C. Among the Of- for RobustVLA and RobustVLA-C. Among the Offline IL models, OpenVLA-OFT (8080 _._ 6%) shows a significant improvement over the original Open-) shows a significant improvement over the original Open- **412** VLA (4747 _._ 9%).). Offline RL algorithms, however, perform less well, with similar success rates (all **413** around 60%). 60%).). This highlights the importance of the VLA model’s autonomous interaction with the **414** environment and the Jacobian regularization term in robustly resisting observation perturbations. **415 416 Action Perturbation Setting.** We add zero-mean Gaussian noise to the inferred actions during the interaction between the VLA model and the environment to test the model’s resilience to ac- **417** tion noise. The average success rates for the four LIBERO suites are shown in Tab. 2 and Appendix **418** Tab. 5. The results demonstrate that even under varying degrees of action noise, our method achieves **419** the best performance compared to all baselines. The proposed RobustVLA and RobustVLA-C **420** achieved similar performance, at 54 _._ 8% and 54 _._ 7%,, respectively. OpenVLA-OPT (5353 _._ 5%)) per- **421** formed best in the offline IL category and outperformed the best Offline RL method, ARFM (5050 _._ 1%).). **422** This demonstrates that our proposed method improves the VLA model’s resilience to action pertur- **423** bations and robust decision execution. **424 Joint Perturbation Settings.** To thoroughly evaluate the VLA model’s robustness against envi- **425** ronmental perturbations, we further set a more challenging joint perturbation: observation image **426** rotation and an action noise level of 0.1. The average success rates for the four LIBERO suites **427** are shown in Tab. 3. The results show that the proposed RobustVLA-C using curriculum learning **428** (82 _._ 1%) achieves the best performance, significantly outperforming other methods. Furthermore, **429** online RL algorithms generally outperform both offline IL and offline RL algorithms. Among of- **430** fline IL algorithms, OpenVLA-OFT (69 _._ 5%) performs best, while OpenVLA (only 10 _._ 8%) performs **431** worst. Meanwhile, ReinboT (48 _._ 7%) slightly outperforms other offline RL algorithms. These experimental results highlight several important conclusions: **1)** autonomous online RL interaction 

**Observation Perturbation Settings.** To evaluate the model’s ability to cope with uncertainty in environmental observations, we perturb both the first- and third-view inferences during autonomous interaction. The average success rates are shown in Tab. 1 and Appendix Tab. 4. The results show that our proposed method has the best resistance to observation perturbations compared to all other baselines, with average SR of 82 82 _._ 5% and 82 and 82 82 _._ 2% for RobustVLA and RobustVLA-C. Among the Of- for RobustVLA and RobustVLA-C. Among the Offline IL models, OpenVLA-OFT (8080 _._ 6%) shows a significant improvement over the original Open-) shows a significant improvement over the original OpenVLA (4747 _._ 9%).). Offline RL algorithms, however, perform less well, with similar success rates (all around 60%). 60%).). This highlights the importance of the VLA model’s autonomous interaction with the environment and the Jacobian regularization term in robustly resisting observation perturbations. 

**Action Perturbation Setting.** We add zero-mean Gaussian noise to the inferred actions during the interaction between the VLA model and the environment to test the model’s resilience to action noise. The average success rates for the four LIBERO suites are shown in Tab. 2 and Appendix Tab. 5. The results demonstrate that even under varying degrees of action noise, our method achieves the best performance compared to all baselines. The proposed RobustVLA and RobustVLA-C achieved similar performance, at 54 _._ 8% and 54 _._ 7%,, respectively. OpenVLA-OPT (5353 _._ 5%)) performed best in the offline IL category and outperformed the best Offline RL method, ARFM (5050 _._ 1%).). This demonstrates that our proposed method improves the VLA model’s resilience to action perturbations and robust decision execution. 

8 

Under review as a conference paper at ICLR 2026 

**470** 

**432** 

can enhance model robustness in the face of complex environmental perturbations; **2)** our proposed **433** Jacobian penalty and action smoothness constraint can effectively guide the VLA model to cope **434** with environmental uncertainty; and **3)** in challenging OOD scenarios, using curriculum learning **435** allows the VLA model to more gradually adapt to downstream tasks and cope with environmental **436** perturbations, thereby generating robust and stable decision-making behavior. **437** 

### **438** 5.2 TRANSFER LEARNING PERFORMANCE COMPARISON 

**439** 

**440** In this section, we examine the transfer learning capabilities of RobustVLA to target domains con- **441** taining environmental uncertainty. To this end, we transfer the pre-trained VLA model on the **442** LIBERO Goal suite to downstream tasks with environmental perturbations (image rotation and 0 _._ 15 action noise level). The results in Fig. 3 show that the performance of the baseline RIPT-VLA de- **443** creases with increasing number of environment rollouts, falling short of the proposed RobustVLA. **444** This suggests that in perturbed scenarios, online RL fine-tuning, which simply maximizes the ul- **445** timate success reward, is insufficient to cope with environmental uncertainty and perturbations. **446** In contrast, on the _open drawer_ and _put_ **447** _bowl_ tasks, RobustVLA achieves improve- **448** ments of 8 _._ 0% and 16 _._ 0% over direct zero- **449** shot transfer, respectively. This demon- **450** strates that the proposed RobustVLA can **451** significantly withstand environmental per- **452** turbations and adopt more robust and sta- **453** ble behaviors after only a few environment rollouts, thus exhibiting superior transfer **454** learning capabilities. More results in Ap- **455** pendix Fig. 6. Figure 3: Comparison of transfer learning capabilities **456** in OOD scenarios with uncertainty. **457 458 459 460 461 462 463 464 465** Figure 4: (a) Ablation studies on Jacobian weight _α_ , and action-smooth weight _β_ . (b-c) T-SNE **466** visualization of the observation representations of the baseline RIPT-VLA and the proposed Ro- **467** bustVLA. “ _•_ ”: task success; “ _×_ ”: task failure. **468** 

#### **469** 

### 5.3 ABLATION ANALYSIS 

**471 Hyperparameter Ablation.** In the RobustVLA optimization objective, the hyperparameters _α_ and **472** _β_ control the strength of the robustness component. We perform ablation analysis of these two **473** parameters in a joint perturbation setting: LIBERO goal suite, observation image rotation, and an **474** action noise level of 0 _._ 1. Results in Fig. 4(a) show that the omission of either penalty term leads to **475** a drop in VLA model performance, while our algorithm exhibits good hyperparameter insensitivity. **476 Observation Representation Visualization.** To investigate how the proposed penalty objective af- **477** fects the observation representation of the VLA model, we performed a T-SNE (Maaten & Hinton, **478** 2008) visualization analysis in the same joint perturbation setting, as shown in Fig. 4(b-c). The **479** result shows that observation representations corresponding to the RobustVLA remain largely un- **480** changed despite varying degrees of environmental perturbation. This demonstrates its robustness to **481** environmental uncertainty, enabling robust task performance. In contrast, the baseline RIPT-VLA **482** exhibits overly separated clusters in the observation representations of some downstream tasks. This indicates a deviation from the desired trajectory for task performance, leading to a lack of robustness **483** and reliability in decision-making. **484** 

**485 Action Distribution Visualization.** We visualized the action distribution to explore how various noises affect model execution and to compare the proposed RobustVLA with the baseline RIPT- 

9 

Under review as a conference paper at ICLR 2026 

**486 487 488 489 490 491 492 493 494 495 496 497** Figure 5: (a) Action distribution during model inference under four noise conditions. (b) Compari- **498** son of action distribution between baseline RIPT-VLA and the proposed RobustVLA. **499 500** VLA. Specifically, we recorded 100 action trajectories during RIPT-VLA inference in LIBERO **501** Spatial. Four settings were utilized: **1)** no observation noise or action noise; **2)** only image rotation **502** perturbation; **3)** only action noise (noise level 0 0 _._ 1); and); and **4)** both image rotation perturbation and ac- **503** tion noise. The visualization results are shown in Fig. 5(a) and Appendix Fig. 7. The results show **504** that the action trajectories exhibit diverse distribution patterns and coverage under different noise **505** conditions. This indicates that observation perturbation and action perturbation have different em- **506** phases and degrees of influence on robot manipulation behavior, especially when both perturbations **507** are present. Furthermore, the action distribution comparison between the baseline RIPT-VLA and **508** the proposed RobustVLA is shown in Fig. 5(b) and Appendix Fig. 8. The results show that under **509** joint perturbation, the action distribution of RobustVLA is closer to the action distribution under noise-free conditions compared to RIPT-VLA. This demonstrates that RobustVLA can adaptively **510** adjust its behavior, enabling the robot to better resist environmental disturbances and thus produce **511** more robust and stable decision-making actions. **512 513 514** 6 CONCLUSION **515 516** In this work, we investigate how VLA models can effectively cope with environmental uncertainty. **517** While large-scale pre-training endows VLA models with flexible manipulation skills, environmental noise can render typical online post-training unreliable when applied to downstream tasks. We there- **518** fore propose RobustVLA, a robustness-aware online RL post-training method for VLA models. We **519** establish robustness bounds and induce a concise robust optimization objective. Extensive experi- **520** ments confirm that our method significantly improves the stability and robustness of VLA models. **521** These findings highlight that robustness-aware post-training is a key step towards reliable model **522** deployment. A promising future work is to investigate the robustness of VLA models to other types **523** of perturbations during autonomous interaction, such as dynamic shift and external disturbances. **524 525** REFERENCES **526 527** Kishan Panaganti Badrinath and Dileep Kalathil. Robust reinforcement learning using least squares **528** policy iteration with provable performance guarantees. In _International Conference on Machine_ **529** _Learning_ , pp. 511–520. PMLR, 2021. **530** Hongzhe Bi, Lingxuan Wu, Tianwei Lin, Hengkai Tan, Zhizhong Su, Hang Su, and Jun Zhu. H-rdt: **531** Human manipulation enhanced bimanual robotic manipulation. _arXiv preprint arXiv:2507.23523_ , **532** 2025. **533 534** Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. **535** _pi_ 0: A vision-language-action flow model for general robot control. _arXiv preprint_ **536** _arXiv:2410.24164_ , 2024. **537 538** Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, **539** Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

VLA. Specifically, we recorded 100 action trajectories during RIPT-VLA inference in LIBERO Spatial. Four settings were utilized: **1)** no observation noise or action noise; **2)** only image rotation perturbation; **3)** only action noise (noise level 0 0 _._ 1); and); and **4)** both image rotation perturbation and action noise. The visualization results are shown in Fig. 5(a) and Appendix Fig. 7. The results show that the action trajectories exhibit diverse distribution patterns and coverage under different noise conditions. This indicates that observation perturbation and action perturbation have different emphases and degrees of influence on robot manipulation behavior, especially when both perturbations are present. Furthermore, the action distribution comparison between the baseline RIPT-VLA and the proposed RobustVLA is shown in Fig. 5(b) and Appendix Fig. 8. The results show that under joint perturbation, the action distribution of RobustVLA is closer to the action distribution under noise-free conditions compared to RIPT-VLA. This demonstrates that RobustVLA can adaptively adjust its behavior, enabling the robot to better resist environmental disturbances and thus produce more robust and stable decision-making actions. 

10 

Under review as a conference paper at ICLR 2026 

**540** Remi Cadene, Simon Alibert, Alexander Soare, Quentin Gallouedec, Adil Zouitine, Steven **541** Palma, Pepijn Kooijmans, Michel Aractingi, Mustafa Shukor, Dana Aubakirova, Martino Russi, **542** Francesco Capuano, Caroline Pascal, Jade Choghari, Jess Moss, and Thomas Wolf. Lerobot: **543** State-of-the-art machine learning for real-world robotics in pytorch. https://github.com/ **544** huggingface/lerobot, 2024., 2024. **545 546** Chilam Cheang, Sijin Chen, Zhongren Cui, Yingdong Hu, Liqun Huang, Tao Kong, Hang Li, Yifeng **547** Li, Yuxiao Liu, Xiao Ma, et al. Gr-3 technical report. _arXiv preprint arXiv:2507.15493_ , 2025. **548** Yevgen Chebotar, Quan Vuong, Karol Hausman, Fei Xia, Yao Lu, Alex Irpan, Aviral Kumar, Tianhe **549** Yu, Alexander Herzog, Karl Pertsch, et al. Q-transformer: Scalable offline reinforcement learning **550** via autoregressive q-functions. In _Conference on Robot Learning_ , pp. 3909–3928. PMLR, 2023. **551 552** Kevin Chen, Marco Cusumano-Towner, Brody Huval, Aleksei Petrenko, Jackson Hamburger, **553** Vladlen Koltun, and Philipp Kr¨ahenb¨uhl. Reinforcement learning for long-horizon interactive **554** llm agents. _arXiv preprint arXiv:2502.01600_ , 2025a. **555** Yuhui Chen, Shuai Tian, Shugao Liu, Yingting Zhou, Haoran Li, and Dongbin Zhao. Con- **556** rft: A reinforced fine-tuning method for vla models via consistency policy. _arXiv preprint_ **557** _arXiv:2502.05450_ , 2025b. **558 559** Zengjue Chen, Runliang Niu, He Kong, and Qi Wang. Tgrpo: Fine-tuning vision-language-action **560** model via trajectory-wise group relative policy optimization. _arXiv preprint arXiv:2506.08440_ , **561** 2025c. **562 563** Mingxuan Cui, Duo Zhou, Yuxuan Han, Grani A Hanasusanto, Qiong Wang, Huan Zhang, and Zhengyuan Zhou. Dr-sac: Distributionally robust soft actor-critic for reinforcement learning **564** under uncertainty. _arXiv preprint arXiv:2506.12622_ , 2025. **565 566** Michael Dennis, Natasha Jaques, Eugene Vinitsky, Alexandre Bayen, Stuart Russell, Andrew Critch, **567** and Sergey Levine. Emergent complexity and zero-shot transfer via unsupervised environment **568** design. _Advances in neural information processing systems_ , 33:13049–13061, 2020. **569 570** Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, **571** Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, et al. Palm-e: An embodied multi- **572** modal language model. _arXiv preprint arXiv:2303.03378_ , 2023. **573** Maximilian Du, Alexander Khazatsky, Tobias Gerstenberg, and Chelsea Finn. To err is robotic: **574** Rapid value-based trial-and-error during deployment. _arXiv preprint arXiv:2406.15917_ , 2024. **575 576** Yan Duan, Xi Chen, Rein Houthooft, John Schulman, and Pieter Abbeel. Benchmarking deep **577** reinforcement learning for continuous control. In _International conference on machine learning_ , **578** pp. 1329–1338. PMLR, 2016. **579** Zipeng Fu, Tony Z Zhao, and Chelsea Finn. Mobile aloha: Learning bimanual mobile manipulation **580** with low-cost whole-body teleoperation. _arXiv preprint arXiv:2401.02117_ , 2024. **581 582** Debamita Ghosh, George K Atia, and Yue Wang. Provably near-optimal distributionally robust **583** reinforcement learning in online settings. _arXiv preprint arXiv:2508.03768_ , 2025. **584 585** Shangding Gu, Laixi Shi, Muning Wen, Ming Jin, Eric Mazumdar, Yuejie Chi, Adam Wierman, **586** and Costas Spanos. Robust gymnasium: A unified modular benchmark for robust reinforcement **587** learning. _arXiv preprint arXiv:2502.19652_ , 2025. **588** Yanjiang Guo, Jianke Zhang, Xiaoyu Chen, Xiang Ji, Yen-Jen Wang, Yucheng Hu, and Jianyu Chen. **589** Improving vision-language-action model with online reinforcement learning. _arXiv preprint_ **590** _arXiv:2501.16664_ , 2025. **591 592** Asher J Hancock, Allen Z Ren, and Anirudha Majumdar. Run-time observation interventions make **593** vision-language-action models more visually robust. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 9499–9506. IEEE, 2025. 

- Remi Cadene, Simon Alibert, Alexander Soare, Quentin Gallouedec, Adil Zouitine, Steven Palma, Pepijn Kooijmans, Michel Aractingi, Mustafa Shukor, Dana Aubakirova, Martino Russi, Francesco Capuano, Caroline Pascal, Jade Choghari, Jess Moss, and Thomas Wolf. Lerobot: State-of-the-art machine learning for real-world robotics in pytorch. https://github.com/ huggingface/lerobot, 2024., 2024. 

- Yevgen Chebotar, Quan Vuong, Karol Hausman, Fei Xia, Yao Lu, Alex Irpan, Aviral Kumar, Tianhe Yu, Alexander Herzog, Karl Pertsch, et al. Q-transformer: Scalable offline reinforcement learning via autoregressive q-functions. In _Conference on Robot Learning_ , pp. 3909–3928. PMLR, 2023. 

- Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, et al. Palm-e: An embodied multimodal language model. _arXiv preprint arXiv:2303.03378_ , 2023. 

11 

Under review as a conference paper at ICLR 2026 

**594** Yiting He, Zhishuai Liu, Weixin Wang, and Pan Xu. Sample complexity of distributionally ro- **595** bust off-dynamics reinforcement learning with online interaction. In _Forty-second International_ **596** _Conference on Machine Learning_ . **597 598** Zhi Hou, Tianyi Zhang, Yuwen Xiong, Haonan Duan, Hengjun Pu, Ronglei Tong, Chengyang Zhao, **599** Xizhou Zhu, Yu Qiao, Jifeng Dai, et al. Dita: Scaling diffusion transformer for generalist vision- **600** language-action policy. _arXiv preprint arXiv:2503.19757_ , 2025. **601** Jiaheng Hu, Rose Hendrix, Ali Farhadi, Aniruddha Kembhavi, Roberto Mart´ın-Mart´ın, Peter Stone, **602** Kuo-Hao Zeng, and Kiana Ehsani. Flare: Achieving masterful and adaptive robot policies with **603** large-scale reinforcement learning fine-tuning. _arXiv preprint arXiv:2409.16578_ , 2024. **604 605** Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny **606** Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _arXiv preprint arXiv:2504.16054_ , 2025. **607 608** Garud N Iyengar. Robust dynamic programming. _Mathematics of Operations Research_ , 30(2): **609** 257–280, 2005. **610 611** Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, **612** Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. **613 614** Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Opti- **615** mizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. **616 617** Wouter Kool, Herke Van Hoof, and Max Welling. Attention, learn to solve routing problems! _arXiv_ **618** _preprint arXiv:1803.08475_ , 2018. **619** Zeyang Li, Chuxiong Hu, Yunan Wang, Yujie Yang, and Shengbo Eben Li. Safe reinforcement **620** learning with dual robustness. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , **621** 2024. **622 623** Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: **624** Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. **625 626** Jijia Liu, Feng Gao, Bingwen Wei, Xinlei Chen, Qingmin Liao, Yi Wu, Chao Yu, and Yu Wang. **627** What can rl bring to vla generalization? an empirical study. _arXiv preprint arXiv:2505.19789_ , **628** 2025. **629 630** Guanxing Lu, Wenkai Guo, Chubin Zhang, Yuheng Zhou, Haonan Jiang, Zifeng Gao, Yansong Tang, and Ziwei Wang. Vla-rl: Towards masterful and general robotic manipulation with scalable **631** reinforcement learning. _arXiv preprint arXiv:2505.18719_ , 2025. **632 633** Thodoris Lykouris, Max Simchowitz, Alex Slivkins, and Wen Sun. Corruption-robust exploration **634** in episodic reinforcement learning. In _Conference on Learning Theory_ , pp. 3242–3245. PMLR, **635** 2021. **636** Laurens van der Maaten and Geoffrey Hinton. Visualizing data using t-sne. _Journal of machine_ **637** _learning research_ , 9(Nov):2579–2605, 2008. **638 639** Max Sobol Mark, Tian Gao, Georgia Gabriela Sampaio, Mohan Kumar Srirama, Archit Sharma, **640** Chelsea Finn, and Aviral Kumar. Policy agnostic rl: Offline rl and online rl fine-tuning of any **641** class and backbone. _arXiv preprint arXiv:2412.06685_ , 2024. 

**642** 

**643** 

**644** 

   - Mitsuhiko Nakamoto, Oier Mees, Aviral Kumar, and Sergey Levine. Steering your generalists: Improving robotic foundation models via value guidance. _arXiv preprint arXiv:2410.13816_ , 2024. 

- **645** Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham **646** Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: **647** Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 6892–6903. IEEE, 2024. 

12 

Under review as a conference paper at ICLR 2026 

**648** Jan Peters and Stefan Schaal. Reinforcement learning by reward-weighted regression for operational **649** space control. In _Proceedings of the 24th international conference on Machine learning_ , pp. 745– **650** 750, 2007. **651 652** Lerrel Pinto, James Davidson, Rahul Sukthankar, and Abhinav Gupta. Robust adversarial reinforce- **653** ment learning. In _International conference on machine learning_ , pp. 2817–2826. PMLR, 2017. **654** Zachary Roch, Chi Zhang, George Atia, and Yue Wang. A finite-sample analysis of distributionally **655** robust average-reward reinforcement learning. _arXiv preprint arXiv:2505.12462_ , 2025. **656 657** John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy **658** optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. **659 660** Modi Shi, Li Chen, Jin Chen, Yuxiang Lu, Chiming Liu, Guanghui Ren, Ping Luo, Di Huang, **661** Maoqing Yao, and Hongyang Li. Is diversity all you need for scalable robotic manipulation? _arXiv preprint arXiv:2507.06219_ , 2025. **662 663** Junyang Shu, Zhiwei Lin, and Yongtao Wang. Rftf: Reinforcement fine-tuning for embodied agents **664** with temporal feedback. _arXiv preprint arXiv:2505.19767_ , 2025. **665 666** Haoming Song, Delin Qu, Yuanqi Yao, Qizhi Chen, Qi Lv, Yiwen Tang, Modi Shi, Guanghui Ren, **667** Maoqing Yao, Bin Zhao, et al. Hume: Introducing system-2 thinking in visual-language-action **668** model. _arXiv preprint arXiv:2505.21432_ , 2025. **669** Richard S Sutton, Andrew G Barto, et al. _Reinforcement learning: An introduction_ , volume 1. MIT **670** press Cambridge, 1998. **671 672** Richard S Sutton, David McAllester, Satinder Singh, and Yishay Mansour. Policy gradient meth- **673** ods for reinforcement learning with function approximation. _Advances in neural information_ **674** _processing systems_ , 12, 1999. **675** Shuhan Tan, Kairan Dou, Yue Zhao, and Philipp Kr¨ahenb¨uhl. Interactive post-training for vision- **676** language-action models. _arXiv preprint arXiv:2505.17016_ , 2025a. **677 678** Shuhan Tan, Kairan Dou, Yue Zhao, and Philipp Kr¨ahenb¨uhl. Interactive post-training for vision- **679** language-action models, 2025b. URL https://arxiv.org/abs/2505.17016. https://arxiv.org/abs/2505.17016.. 

- Richard S Sutton, Andrew G Barto, et al. _Reinforcement learning: An introduction_ , volume 1. MIT press Cambridge, 1998. 

- Shuhan Tan, Kairan Dou, Yue Zhao, and Philipp Kr¨ahenb¨uhl. Interactive post-training for visionlanguage-action models, 2025b. URL https://arxiv.org/abs/2505.17016. https://arxiv.org/abs/2505.17016.. 

**680 681** Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot **682** policy. _arXiv preprint arXiv:2405.12213_ , 2024. **683** 

**684** Josh Tobin, Rachel Fong, Alex Ray, Jonas Schneider, Wojciech Zaremba, and Pieter Abbeel. Do- **685** main randomization for transferring deep neural networks from simulation to the real world. In **686** _2017 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ , pp. 23–30. **687** IEEE, 2017. **688** 

- **689** Linh Le Pham Van, Minh Hoang Nguyen, Hung Le, Hung The Tran, and Sunil Gupta. Hybrid cross-domain robust reinforcement learning. _arXiv preprint arXiv:2505.23003_ , 2025. 

**690** 

**691** Yue Wang and Shaofeng Zou. Online robust reinforcement learning with model uncertainty. _Ad-_ **692** _vances in Neural Information Processing Systems_ , 34:7193–7206, 2021. **693** 

- **694** Chen-Yu Wei, Christoph Dann, and Julian Zimmert. A model selection approach for corruption **695** robust reinforcement learning. In _International Conference on Algorithmic Learning Theory_ , pp. 1043–1096. PMLR, 2022. 

**696** 

**697** 

- **697** Wolfram Wiesemann, Daniel Kuhn, and Berc¸ Rustem. Robust markov decision processes. _Mathe-_ **698** _matics of Operations Research_ , 38(1):153–183, 2013. 

**699** 

- **700** Kun Wu, Yinuo Zhao, Zhiyuan Xu, Zhengping Che, Chengxiang Yin, Chi Harold Liu, Qinru Qiu, **701** Feifei Feng, and Jian Tang. Acl-ql: Adaptive conservative level in _q_ -learning for offline reinforcement learning. _IEEE Transactions on Neural Networks and Learning Systems_ , 2024. 

13 

Under review as a conference paper at ICLR 2026 

**702 703 704 705 706 707 708 709 710 711 712 713 714 715 716 717 718 719 720 721 722 723 724 725 726 727 728 729 730 731 732 733 734 735 736 737 738 739 740 741 742 743 744 745 746 747 748 749 750 751 752 753 754 755** 

- Youguang Xing, Xu Luo, Junlin Xie, Lianli Gao, Hengtao Shen, and Jingkuan Song. Shortcut learning in generalist robot policies: The role of dataset diversity and fragmentation. _arXiv preprint arXiv:2508.06426_ , 2025. 

- Charles Xu, Qiyang Li, Jianlan Luo, and Sergey Levine. Rldg: Robotic generalist policy distillation via reinforcement learning. _arXiv preprint arXiv:2412.09858_ , 2024. 

- Chenlu Ye, Wei Xiong, Quanquan Gu, and Tong Zhang. Corruption-robust algorithms with uncertainty weighting for nonlinear contextual bandits and markov decision processes. In _International Conference on Machine Learning_ , pp. 39834–39863. PMLR, 2023. 

- Chenlu Ye, Jiafan He, Quanquan Gu, and Tong Zhang. Towards robust model-based reinforcement learning against adversarial corruption. _arXiv preprint arXiv:2402.08991_ , 2024. 

- Hongyin Zhang, Pengxiang Ding, Shangke Lyu, Ying Peng, and Donglin Wang. Gevrm: Goal-expressive video generation model for robust visual manipulation. _arXiv preprint arXiv:2502.09268_ , 2025a. 

- Hongyin Zhang, Shiyuan Zhang, Junxi Jin, Qixin Zeng, Yifan Qiao, Hongchao Lu, and Donglin Wang. Balancing signal and variance: Adaptive offline rl post-training for vla flow models, 2025b. URL https://arxiv.org/abs/2509.04063. 

- Hongyin Zhang, Zifeng Zhuang, Han Zhao, Pengxiang Ding, Hongchao Lu, and Donglin Wang. Reinbot: Amplifying robot visual-language manipulation with reinforcement learning. _arXiv preprint arXiv:2505.07395_ , 2025c. 

- Jiahui Zhang, Yusen Luo, Abrar Anwar, Sumedh Anand Sontakke, Joseph J Lim, Jesse Thomason, Erdem Biyik, and Jesse Zhang. Rewind: Language-guided rewards teach robot policies without new demonstrations. _arXiv preprint arXiv:2505.10911_ , 2025d. 

- Xuezhou Zhang, Yiding Chen, Xiaojin Zhu, and Wen Sun. Corruption-robust offline reinforcement learning. In _International Conference on Artificial Intelligence and Statistics_ , pp. 5757–5773. PMLR, 2022. 

- Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. 

14 

Under review as a conference paper at ICLR 2026 

> **756** A APPENDIX **757 758** A.1 MORE RELATED WORK **759 760 Vision-Language-Action Models.** Recent advances in foundation models have extended large- **761** scale pretraining beyond language and vision to embodied agents, giving rise to Vision-Language- **762** Action (VLA) models. The initial wave of this paradigm was marked by two key approaches: **763** extending robotics-native architectures to internet scale, exemplified by RT-1 (Brohan et al., 2022) **764** and RT-2 (Zitkovich et al., 2023), and injecting multimodal sensor data directly into large language **765** models, with PaLM-E (Driess et al., 2023) representing a landmark embodied language model. Subsequent efforts explored improved architectures and scaling laws, with models such as Octo (Team **766** et al., 2024) and OpenVLA (Kim et al., 2024) establishing powerful, open-source benchmarks. Ar- **767** chitectural exploration also led to new policy representations, exemplified by the use of diffusion **768** transformers in Dita (Hou et al., 2025) for scaling generalist policies. More recent work has intensi- **769** fied the focus on grounding VLAs in high-quality, robotics-specific data, including the aggregation **770** of diverse datasets via projects like RT-X (O’Neill et al., 2024), GR-3 (Cheang et al., 2025), and **771** pioneering data collection methods such as Mobile ALOHA (Fu et al., 2024). Meanwhile, to ad- **772** vance real-world generalization, models including H-RDT (Bi et al., 2025), _π_ 0 (Black et al., 2024) **773** and _π_ 0 _._ 5 (Intelligence et al., 2025) have been developed to improve embodied reasoning and ad- **774** dress open-world, knowledge-driven tasks. Collectively, these studies position VLA models as a **775** core foundation for general-purpose embodied intelligence. Moreover, in the field of robust vision- **776** language manipulation, previous work, GEVRM (Zhang et al., 2025a), evaluates environmental perturbations by simulating responses and optimizing them through prototype contrastive learning. **777** However, GEVRM is inherently a hierarchical imitation learning framework, and the distribution **778** shift of its visual planning objectives during training and testing can lead to performance bottle- **779** necks. Other work (Hancock et al., 2025) has proposed a runtime intervention scheme that identi- **780** fies model-sensitive input regions and modifies task-irrelevant regions to reduce model sensitivity, **781** thereby improving visual robustness. However, this approach relies heavily on off-the-shelf VLMs **782** and segmentation models, and its primary limitation is accurately distinguishing objects from back- **783** ground clutter. In contrast to these works, our work focuses on online RL post-training to further **784** adapt and coordinate the VLA model with downstream tasks. **785 786** A.2 FURTHER ANALYSIS OF MODEL ROBUSTNESS **787 788** Building upon the upper bounds established in the theorems, we next examine two corollaries that **789** sharpen the theoretical insights under additional structural assumptions. These corollaries illustrate how the abstract bounds specialize in contractive dynamics or strongly regularized update regimes, **790** thereby revealing concrete conditions under which robustness can be guaranteed at scale. **791 792 Corollary 1.** _Under the assumptions of Theorem 1 but with ϵ_ offline = 0 _(the imitation model is_ **793** _perfect) and contractive dynamics Lf <_ 1 _, the expected return gap satisfies_ **794** 1 E� _J_ ( _π_<sup>_∗_</sup> ) _− J_ ( _π_ )� _≤ H · Lr · · λϵs._ **795** 1 _− Lf_ **796 797** Corollary 1 shows that the compounding factor _O_ ( _L_<sup>_H_</sup> _f_<sup>)collapsestoalineardependenceonthe</sup> **798** rollout horizon _H_ , yielding a return gap on the order of _H · λϵs λϵss_ . What this implies is that obser- **799** vation noise no longer causes exponential amplification. This highlights a regime where Jacobian **800** regularization has direct leverage _−−_ by shrinking _λ_ , the sensitivity to _ϵss_ is proportionally reduced, **801** ensuring that perception errors do not destabilize the system even in long rollouts. In practice, this **802** means that in sufficiently stable environments, robustness to noisy observations is achievable with **803** only modest regularization strength. **804 Corollary 2.** _Under the setting of Theorem 3 but with discounted return J_ ( _π_ ) = **805** E�� _t≥_ 1<sup>_γt−_1</sup><sup>_r_(</sup><sup>_st, at_)</sup> � _, for some discount factor γ ∈_ (0 _,_ 1) _with contractive dynamics Lf ∈_ (0 _,_ 1) _._ **806807** _Assume the per-step driving term ζt_ := _λϵs_ + _ϵ_ offline +<sup>�</sup><sup>_N_</sup> _i_ =1<sup>_δi_+</sup><sup>_∥ξt∥isuniformlyboundedin_</sup> _expectation, i.e. there exists C < ∞ such that_ sup _t_ E[ _ζt_ ] _≤ C, and that_ sup _t_ E[ _ϵt_ ] _≤ E < ∞. Then_ **808** _the discounted expected return gap is bounded independently of the rollout horizon H:_ **809** 

- **Vision-Language-Action Models.** Recent advances in foundation models have extended largescale pretraining beyond language and vision to embodied agents, giving rise to Vision-LanguageAction (VLA) models. The initial wave of this paradigm was marked by two key approaches: extending robotics-native architectures to internet scale, exemplified by RT-1 (Brohan et al., 2022) and RT-2 (Zitkovich et al., 2023), and injecting multimodal sensor data directly into large language models, with PaLM-E (Driess et al., 2023) representing a landmark embodied language model. Subsequent efforts explored improved architectures and scaling laws, with models such as Octo (Team et al., 2024) and OpenVLA (Kim et al., 2024) establishing powerful, open-source benchmarks. Architectural exploration also led to new policy representations, exemplified by the use of diffusion transformers in Dita (Hou et al., 2025) for scaling generalist policies. More recent work has intensified the focus on grounding VLAs in high-quality, robotics-specific data, including the aggregation of diverse datasets via projects like RT-X (O’Neill et al., 2024), GR-3 (Cheang et al., 2025), and pioneering data collection methods such as Mobile ALOHA (Fu et al., 2024). Meanwhile, to advance real-world generalization, models including H-RDT (Bi et al., 2025), _π_ 0 (Black et al., 2024) and _π_ 0 _._ 5 (Intelligence et al., 2025) have been developed to improve embodied reasoning and address open-world, knowledge-driven tasks. Collectively, these studies position VLA models as a core foundation for general-purpose embodied intelligence. Moreover, in the field of robust visionlanguage manipulation, previous work, GEVRM (Zhang et al., 2025a), evaluates environmental perturbations by simulating responses and optimizing them through prototype contrastive learning. However, GEVRM is inherently a hierarchical imitation learning framework, and the distribution shift of its visual planning objectives during training and testing can lead to performance bottlenecks. Other work (Hancock et al., 2025) has proposed a runtime intervention scheme that identifies model-sensitive input regions and modifies task-irrelevant regions to reduce model sensitivity, thereby improving visual robustness. However, this approach relies heavily on off-the-shelf VLMs and segmentation models, and its primary limitation is accurately distinguishing objects from background clutter. In contrast to these works, our work focuses on online RL post-training to further adapt and coordinate the VLA model with downstream tasks. 

Building upon the upper bounds established in the theorems, we next examine two corollaries that sharpen the theoretical insights under additional structural assumptions. These corollaries illustrate how the abstract bounds specialize in contractive dynamics or strongly regularized update regimes, thereby revealing concrete conditions under which robustness can be guaranteed at scale. 

Corollary 1 shows that the compounding factor _O_ ( _L_<sup>_H_</sup> _f_<sup>)collapsestoalineardependenceonthe</sup> rollout horizon _H_ , yielding a return gap on the order of _H · λϵs λϵss_ . What this implies is that observation noise no longer causes exponential amplification. This highlights a regime where Jacobian regularization has direct leverage _−−_ by shrinking _λ_ , the sensitivity to _ϵss_ is proportionally reduced, ensuring that perception errors do not destabilize the system even in long rollouts. In practice, this means that in sufficiently stable environments, robustness to noisy observations is achievable with only modest regularization strength. 

E� _J_ ( _π_<sup>_∗_</sup> ) _− J_ ( _π_ )� = _O_ (1) _._ 

15 

Under review as a conference paper at ICLR 2026 

**810** Corollary 2 establishes that in the discounted setting with contractive dynamics ( _Lf <_ 1), the ex- **811** pected return gap remains bounded by a constant that does not depend on the rollout horizon _H_ . **812** Intuitively, discounting attenuates the influence of long-term deviations, while contractive dynamics **813** prevent the state deviation _dt_ from growing unboundedly even when both observation and action **814** perturbations are present. A key observation is that the nonstationarity term<sup>�</sup><sup>_N_</sup> _i_ =1<sup>_δi_entersthe</sup> **815** bound only through the uniform driving term _ζt_ ; as long as these accumulated model updates re- **816** main bounded, the discounted error cannot compound over time. Consequently, the effect of both **817** perturbations and update-induced drift is geometrically damped by the factor _γLf <_ 1, guarantee- **818** ing that the overall return difference remains _O_ (1) even as _H →∞_ . Practically, this indicates that **819** stable long-horizon adaptation is achievable provided that policy updates are sufficiently smooth and **820** that the system dynamics do not amplify perturbations. **821** Together, these two corollaries demonstrate how regularization directly modulates the scaling of **822** the return gap: Jacobian regularization turns exponential amplification into linear growth under **823** stable dynamics, while smoothness regularization caps compounding drift at a constant level under **824** controlled updates. This dual perspective makes clear that robustness in VLA fine-tuning is not **825** an abstract desideratum but a quantitatively attainable property under well-chosen regularization **826** regimes. **827 828** A.3 PROOF OF ROBUSTNESS THEORIES **829 Proof of Theorem 1 (Error Amplification Bound) 830 831 Lemma 1** (State Deviation Recursion) **.** _Let dt_ := _∥st − s_<sup>_∗_</sup> _t_<sup>_∥denotethestatedeviationattimet_</sup> **832** _between π and π_<sup>_∗_</sup> _. Then under Lipschitz dynamics f , we have:_ **833** _dt_ +1 _≤ Lf dt_ + _Lf_ ( _λϵs_ + _ϵoffline_ ) _._ **834 835** **_Proof_** _._ At time _t_ , the model _π_ acts on perturbed state ˜ _st_ : **836 837** _at_ = _π_ (˜ _st_ ) _, a_<sup>_∗_</sup> _t_<sup>=</sup><sup>_π∗_(</sup><sup>_st_)</sup><sup>_._</sup> **838** We decompose: **839** _∥at − a_<sup>_∗_</sup> _t_<sup>_∥≤∥π_(˜</sup><sup>_st_)</sup><sup>_−π_(</sup><sup>_st_)</sup><sup>_∥_+</sup><sup>_∥π_(</sup><sup>_st_)</sup><sup>_−π∗_(</sup><sup>_st_)</sup><sup>_∥_</sup> **840 841** _≤ λ · ∥s_ ˜ _t − st∥_ + _∥π − π_<sup>_∗_</sup> _∥∞_ **842** _≤ λϵs_ + _ϵ_ offline _._ **843** Using Lipschitz continuity of _f_ , the dynamics step gives: **844 845** _dt_ +1 = _∥f_ ( _st, at_ ) _− f_ ( _s_<sup>_∗_</sup> _t_<sup>_, a∗_</sup> _t_<sup>)</sup><sup>_∥≤Lf·_(</sup><sup>_∥st−s_</sup> _t_<sup>_∗∥_+</sup><sup>_∥at−a_</sup> _t_<sup>_∗∥_)</sup><sup>_,_</sup> **846** which gives the recurrence: **847** _dt_ +1 _≤ Lf dt_ + _Lf_ ( _λϵs_ + _ϵ_ offline) _._ **848 849 850 Theorem A.1** (Restatement of Theorem 1) **.** _Assume perturbed observations s_ ˜ _t_ = _st_ + _δs_<sup>_twith_</sup> **851** _∥δs_<sup>_t∥≤ϵs, and bounded Jacobian ∥∇sπt_(</sup><sup>_s_)</sup><sup>_∥≤λ.Then:_</sup> **852** E� _J_ ( _π_<sup>_∗_</sup> ) _− J_ ( _π_ )� _≤O_ ( _HLrL_<sup>_H_</sup> _f_<sup>)</sup><sup>_·_(</sup><sup>_ϵoffline_+</sup><sup>_λϵs_)</sup><sup>_._</sup> **853 854** **_Proof_** _._ From Lemma 1, the state deviation satisfies, for _d_ 0 = 0, **855 856** _t−_ 1 _Lf_<sup>_t−_1</sup> **857** _dt ≤_ ( _λϵs_ + _ϵ_ offline) _Lf_ � _Lf_<sup>_j_= (</sup><sup>_λϵs_+</sup><sup>_ϵ_offline)</sup><sup>_Lf_</sup> _f_<sup>) (</sup><sup>_λϵs_+</sup><sup>_ϵ_offline)</sup><sup>_._</sup> _Lf −_ 1<sup>=</sup><sup>_O_(</sup><sup>_L t_</sup> _j_ =0 **858 859** At each step, the reward difference obeys the Lipschitz bound **860 861** _|r_ ( _st, at_ ) _− r_ ( _s_<sup>_∗_</sup> _t_<sup>_, a∗_</sup> _t_<sup>)</sup><sup>_|≤Lr_</sup> � _dt_ + _λϵs_ + _ϵ_ offline� _._ **862** Taking expectations on both sides and using the deterministic upper bound on _dtt_ , we obtain **863** 


16 

Under review as a conference paper at ICLR 2026 

**864 865 866 867 868 869 870 871 872 873 874 875 876 877 878 879 880 881 882 883 884 885 886 887 888 889 890 891 892 893 894 895 896 897 898 899 900 901 902 903 904 905 906 907 908 909 910 911 912 913 914 915 916 917** 

Summing over _t_ = 1 _, . . . , H_ gives 


Finally substituting _dt_ = _O_ ( _Lf_<sup>_t_)(</sup><sup>_λϵs_+</sup><sup>_ϵ_offline) and evaluating the geometric series yields</sup> 

E� _J_ ( _π_<sup>_∗_</sup> ) _− J_ ( _π_ )� _≤O_ ( _HLrL_<sup>_H_</sup> _f_<sup>)</sup> � _λϵs_ + _ϵ_ offline� _,_ 

which completes the proof. 

### **Proof of Theorem 2 (Return Drift Control)** 

**Lemma 2** (State Deviation under Smooth Regularization + Action Noise) **.** _Let dt_ = _∥st − s_<sup>_∗_</sup> _t_<sup>_∥._</sup> _Under Lf -Lipschitz dynamics and executed action at_ = _πt_ ( _st_ ) + _ξt,_ 


_with ϵt ≤ ϵ_ offline +<sup>�</sup><sup>_N_</sup> _i_ =1<sup>_δi._</sup> 

**_Proof_** _._ We decompose the action error: 

_∥at − a_<sup>_∗_</sup> _t_<sup>_∥_=</sup><sup>_∥πt_(</sup><sup>_st_) +</sup><sup>_ξt−π∗_(</sup><sup>_st_)</sup><sup>_∥≤∥πt_(</sup><sup>_st_)</sup><sup>_−π∗_(</sup><sup>_st_)</sup><sup>_∥_+</sup><sup>_∥ξt∥_=</sup><sup>_ϵt_+</sup><sup>_∥ξt∥._</sup> 

Then the Lipschitz dynamics give: 


**Lemma 3** (Expected Norm of Gaussian Noise) **.** _Let ξt ∼N_ (0 _, σ_<sup>2</sup> _Id_ ) _be a d-dimensional isotropic Gaussian random vector. Then the expected Euclidean norm satisfies:_ 


**_Proof_** _._ Let _zi_ := _ξt,i/σ ∼N_ (0 _,_ 1), so _ξt,i_ = _σzi_ . Then the norm becomes: 


Let _Z_ :=<sup>�</sup><sup>_d_</sup> _i_ =1<sup>_z_</sup> _i_<sup>2, then</sup><sup>_Z∼χ_2(</sup><sup>_d_) is a chi-squared distribution with</sup><sup>_d_degrees of freedom.So the</sup> norm becomes: 

_∥ξt∥_ = _σ ·_ _~~√~~ Z ⇒_ E[ _∥ξt∥_ ] = _σ ·_ E[ _~~√~~ Z_ ] _._ 

Although E[ _~~√~~ Z_ ] has no closed form, we apply Jensen’s inequality. Since the square root function is concave and _Z ≥_ 0, 

Hence, 


**Theorem A.2** (Restatement of Theorem 2) **.** _Assume actions are perturbed as at_ = _πt_ ( _st_ ) + _ξt with ξt ∼N_ (0 _, σ_<sup>2</sup> _Id_ ) _, and VLA models satisfy ∥πi − πi−_ 1 _∥∞ ≤ δi. Then:_ 


17 

Under review as a conference paper at ICLR 2026 

**918 919 920 921 922 923 924 925 926 927 928 929 930 931 932 933 934 935 936 937 938 939 940 941 942 943 944 945 946 947 948 949 950 951 952 953 954 955 956 957 958 959 960 961 962 963 964 965 966 967 968 969 970 971** 

**_Proof_** _._ Start from the per-step recurrence (Lemma 2): 


Unrolling the linear recurrence with _d_ 0 = 0 gives 


Take expectation on both sides and use linearity: 


Now apply Lemma 3, which yields E _∥ξj∥≤ σ_ _~~√~~ d_ for every _j_ . Consequently, 


where the finite geometric sum produces a factor of order _O_ ( _L_<sup>_t_</sup> _f_<sup>).</sup> 

Because the reward is _Lr_ -Lipschitz, 


Taking expectation and summing over _t_ = 0 _, . . . , H −_ 1,, 

Collecting geometric-series terms gives the claimed form 


### **Proof of Theorem 3 (Robust Stability Guarantee)** 

**Lemma 4** (State Deviation with Nested Perturbation) **.** _Let dt_ = _∥st − s_<sup>_∗_</sup> _t_<sup>_∥.UnderLf-Lipschitz_</sup> _dynamics, and with both observation perturbations ∥s_ ˜ _t − st∥≤ ϵs and action noise ξt, the state deviation satisfies_ 


**_Proof_** _._ Decompose the action error at time _t_ : 


Applying _Lf_ -Lipschitz dynamics, 


which yields the stated recursion. 

18 

Under review as a conference paper at ICLR 2026 

**972 Theorem A.3** (Restatement of Theorem 3) **.** _Under both observation and action perturbations, and_ **973** _both Jacobian and smooth regularizations, the return gap satisfies:_ **974** _N_ **975 976** E[ _J_ ( _π_<sup>_∗_</sup> ) _− J_ ( _π_ )] _≤O_ ( _HLrL_<sup>_H_</sup> _f_<sup>)</sup> � _ϵ_ offline + � _δi_ + _λϵs_ + _σ_ _~~√~~ d_ <u>�</u> _. i_ =1 **977 978** **_Proof_** _._ From Lemma 4, the state deviation satisfies **979** _N_ **980 981** _dt_ +1 _≤ Lf dt_ + _Lf_ � _λϵs_ + _ϵt_ + _∥ξt∥_ � _, ϵt ≤ ϵ_ offline + � _δi. i_ =1 **982 983** Unrolling the linear recurrence with _d_ 0 = 0 yields **984** _t−_ 1 _N_ **985986** _dt ≤_ � _Lf_<sup>_t−_1</sup><sup>_−j_</sup> � _λϵs_ + _ϵ_ offline + � _δi_ + _∥ξj∥_ � _. j_ =0 _i_ =1 **987 988** Taking expectations and using linearity, **989** _t−_ 1 _N_ **990991** E[ _dt_ ] _≤_ � _Lf_<sup>_t−_1</sup><sup>_−j_</sup> � _λϵs_ + _ϵ_ offline + � _δi_ + E _∥ξj∥_ � _. j_ =0 _i_ =1 **992 993** Applying Lemma 3, E _∥ξj∥≤ σ_ _~~√~~ d_ , gives **994 995** _N_ **996** E[ _dt_ ] _≤_ � _λϵs_ + _ϵ_ offline + � _δi_ + _σ_ _~~√~~ d_ <u>�</u> �<sup>_t−_1</sup> _L_<sup>_t_</sup> _f_<sup>_−_1</sup><sup>_−j_</sup> _._ **997** _i_ =1 _j_ =0 **998** Thus, **999** _N_ **1000** E[ _dt_ ] _≤O_ ( _L_<sup>_t_</sup> _f_<sup>)</sup> � _λϵs_ + _ϵ_ offline + � _δi_ + _σ_ _~~√~~ d_ <u>�</u> _._ **1001** _i_ =1 **1002** Because rewards are _Lr_ -Lipschitz, **1003 1004** _|r_ ( _st, at_ ) _− r_ ( _s_<sup>_∗_</sup> _t_<sup>_, a_</sup> _t_<sup>_∗_)</sup><sup>_|≤Lr_</sup> � _dt_ + _λϵs_ + _ϵt_ + _∥ξt∥_ � _._ **1005** Similar to the proof of Theorem 2, we obtain: **1006 1007** _N_ **1008** E[ _J_ ( _π_<sup>_∗_</sup> ) _− J_ ( _π_ )] _≤O_ ( _HLrL_<sup>_H_</sup> _f_<sup>)</sup> � _ϵ_ offline + � _δi_ + _λϵs_ + _σ_ _~~√~~ d_ <u>�</u> _._ **1009** _i_ =1 **1010 1011 1012 Proof of Corollaries 1 and 2 1013 Corollary 3** (Restatement of Corollary 1) **.** _Under the assumptions of Theorem 1 but with ϵ ϵ_ offline = 0 **1014** _(the imitation model is perfect) and contractive dynamics Lf Lff <_ 1 _, the expected return gap satisfies_ **1015** 1 **1016** E� _J_ ( _π_<sup>_∗_</sup> ) _− J_ ( _π_ )� _≤ H · Lr · · λϵs._ 1 _− Lf_ **1017 1018** **_Proof_** _._ With _ϵ_ offline = 0, Lemma 1 gives (for _d_ 0 = 0) **1019 1020** _t−_ 1 1 _− L_<sup>_t_</sup> **1021** _dt ≤ Lf_ ( _λϵs_ ) � _i_ =0 _Lf_<sup>_i_=</sup><sup>_λϵs· Lf·_</sup> 1 _− Lff ._ **1022** 1 _−L_<sup>_t_</sup> **1023** Since _Lf ∈_ (0 _,_ 1), the factor _Lf_ 1 _−Lff_<sup>_≤_</sup> 1 _−LLf f_<sup>uniformly in</sup><sup>_t_.Thus</sup> **1024 1025** _Lff_ 

**Corollary 3** (Restatement of Corollary 1) **.** _Under the assumptions of Theorem 1 but with ϵ ϵ_ offline = 0 _(the imitation model is perfect) and contractive dynamics Lf Lff <_ 1 _, the expected return gap satisfies_ 


19 

Under review as a conference paper at ICLR 2026 

**1027 1028 1029 1030 1031 1032 1033 1034 1035 1036 1037 1038 1039 1040 1041 1042 1043 1044 1045 1046 1047 1048 1049 1050 1051 1052 1053 1054 1055 1056 1057 1058 1059 1060 1061 1062 1063 1064 1065 1066 1067 1068 1069 1070 1071 1072 1073 1074 1075 1076 1077 1078 1079** 

#### **1026** 

The per-step reward difference satisfies 


Taking expectations and summing over _t_ = 1 _, . . . , H_ yields 

which is the stated bound. 

**Corollary 4** (Restatement of Corollary 2) **.** _Under the setting of Theorem 3 but with discounted return J_ ( _π_ ) = E�� _t≥_ 1<sup>_γt−_1</sup><sup>_r_(</sup><sup>_st, at_)</sup> � _, for some discount factor γ ∈_ (0 _,_ 1) _with contractive dy-_ 

_namics Lf ∈_ (0 _,_ 1) _. Assume the per-step driving term ζt_ := _λϵs_ + _ϵ_ offline +<sup>�</sup><sup>_N_</sup> _i_ =1<sup>_δi_+</sup><sup>_∥ξt∥is_</sup> _uniformly bounded in expectation, i.e. there exists C < ∞ such that_ sup _t_ E[ _ζt_ ] _≤ C, and that_ sup _t_ E[ _ϵt_ ] _≤ E < ∞. Then the discounted expected return gap is bounded independently of the rollout horizon H:_ 


**_Proof_** _._ From Lemma 4 we have the one-step recursion 


where _dt_ = _∥st − s_<sup>_∗_</sup> _t_<sup>_∥_.Unrolling with</sup><sup>_d_0= 0 gives</sup> 


Taking expectations and using E[ _ζj_ ] _≤ C_ for all _j_ yields 


so E[ _dt_ ] is uniformly bounded in _t_ . 


which is a finite constant independent of the rollout horizon _H_ . Thus, we obtain: 

E[ _J_ ( _π_<sup>_∗_</sup> ) _− J_ ( _π_ )] = _O_ (1) _._ 

20 

Under review as a conference paper at ICLR 2026 

**1080 1081 1082 1083 1084 1085 1086 1087 1088 1089 1090 1091 1092 1093 1094 1095 1096 1097 1098 1099 1100 1101 1102 1103 1104 1105 1106 1107 1108 1109 1110 1111 1112 1113 1114 1115 1116 1117 1118 1119 1120 1121 1122 1123 1124 1125 1126 1127 1128 1129 1130 1131 1132 1133** 

### A.4 OBSERVATION PERTURBATION SETTING 

Following previous work, GEVRM (Zhang et al., 2025a), we provide details on implementing observation perturbations in the LIBERO simulation platform: **1) Image Shift:** The image state is randomly shifted to the upper left, with a maximum translation rate of 0 _._ 3 relative to the image size. **2) Image Rotation:** The image state is randomly rotated counterclockwise with a maximum rotation angle of 30 degrees. **3) Color Jitter:** The image state saturation, brightness, contrast, and sharpness are randomly jittered with a maximum random factor of 3. **4) Image Occlusions:** The image state is randomly occluded with a random number of occlusion blocks ranging from 1 to 3 and a maximum length of 20. **5) Image Erasing:** The image state is perturbed by random noise blocks with a maximum size of 0 _._ 1 of the original image. We add observation perturbations to both the first-view and third-view observation images, which makes the constructed robust benchmark platform more challenging. 

### A.5 IMPLEMENTATION DETAILS 

**Reward Densification.** Given that only sparse 0-1 rewards representing task success or failure are directly obtained from the environment, we follow the previous work, ReinboT (Zhang et al., 2025c), to densify the rewards. Specifically, in addition to the task completion reward obtained from the environment, we consider ten additional rewards, as shown in Tab. 7. The ORB-related reward from ReinboT is not considered, as its computation is somewhat time-consuming during online interaction. 

**Experimental implementation.** We conduct our experiments on OpenVLA-OFT (Kim et al., 2025) using the official checkpoints as the base model, with RIPT-VLA’s LoRA adaptor checkpoints (Tan et al., 2025b) applied for adaptation. The implementation is based on the RIPT-VLA codebase (Tan et al., 2025b). Moreover, _R_ Jac requires computing the two-norm of _∇s_ log _πθ_ ( _a|s_ ), which is expensive and memory-intensive to compute directly at the image pixels. Thus, we compute the Jacobian on the low-dimensional embeddings obtained from the Llama-2 encoding used by OpenVLA-OFT. Training is performed on a single GPU with LoRA of rank 32. The post-training procedure takes approximately 24 hours for fine-tuning. The training parameters are shown in Tab. 6, and other parameters follow the previous work, RIPT-VLA (Tan et al., 2025b). All experiments are conducted on the following hardware: **CPU:** Intel(R) Xeon(R) Platinum 8358 @ 2.60GHz; **GPU:** NVIDIA A100-SXM4-80GB. 

**Baseline algorithm reproduction.** To replicate the baseline algorithms, _π_ 0, ReinboT, RWR, and ARFM are all implemented in the repositories: _huggingface/lerobot_ (Cadene et al., 2024). To replicate GEVRM, we utilize the same prototype contrastive learning method for observation representation in the RIPT-VLA code. For other baseline models, we utilize the official implementation. 

### A.6 USE OF LARGE LANGUAGE MODELS 

During the preparation of this manuscript, we employed OpenAI’s ChatGPT (GPT-5) to assist with writing refinement. The model was used exclusively for polishing the language, improving clarity, and suggesting minor stylistic alternatives. All technical content, including problem formulation, theoretical analysis, algorithm design, and experimental results, was conceived, derived, and validated by the authors. The use of ChatGPT did not influence the scientific claims, results, or conclusions presented in this work. 

21 

Under review as a conference paper at ICLR 2026 

**1134 1135 1136 1137 1138** Table 4: Detailed comparison of the average SR (%) of the four LIBERO suites under observation **1139** perturbations. The best result is highlighted in bold, and the second-best result is underlined. Here, “OpenVLA*” denotes the OpenVLA-OFT model, “Ours” refers to RobustVLA model, and “Ours- **1140** C” refers to RobustVLA-C model. **1141** 

|**1142**|**Pertur-**|||||||**Models**|||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**1143**|**bation**|**Tasks**|_π_0 R|einboT|RWR|ARFM RI|PT-VLA|OpenVLA|* OpenVLA|GEVR|M **Ours**|**Ours-C**|
|**1144**||Spatial|35.2|21.4|18.6|11.0|51.6|54.0|38.4|**54.3**|54.0|46.4|
|**1145**|Shift|Goal|32.8|23.6|25.2|20.6|17.4|19.4|20.0|**45.0**|21.6|24.8|
|**1146**||Object|23.4|6.0|4.6|3.6|69.8|71.4|30.8|46.0|72.2|**73.6**|
|**1147**<br>||Long<br>Spatial|33.2<br>61.8|28.2<br>59.6|16.8<br>59.4|12.4<br>56.8|19.0<br>94.2|15.9<br>92.6|12.2<br>54.0|**40.2**<br>88.1|20.4<br>**98.4**|19.6<br>96.4|
|**1148**<br>|Ri|Goal|68.6|42.2|45.2|42.6|87.2|89.0|80.0|65.4|91.4|**92.0**|
|**1149**|otaton|Object|10.4|10.0|12.0|49.4|83.6|67.0|21.0|43.2|**87.4**|87.2|
|**1150**||Long|**57.0**|36.4|31.6|31.0|51.0|51.6|11.2|35.0|53.2|55.6|
|**1151**||Spatial|81.2|79.0|81.8|79.8|97.2|98.2|56.4|86.3|**98.6**|97.4|
|**1152**<br>|Color|Goal<br>Object|82.0<br>92.2|82.0<br>78.2|80.4<br>78.0|82.4<br>79.8|93.2<br>97.0|**94.0**<br>97.0|48.0<br>52.5|61.2<br>47.0|92.4<br>**97.4**|93.5<br>96.2|
|**1153**<br>||Long|58.4|58.4|58.8|59.8|93.0|**94.4**|37.2|31.0|93.8|94.0|
|**1154**||Spatial|90.2|90.8|90.0|87.6|**98.4**|97.9|87.2|87.3|**98.4**|98.2|
|**1155**||Goal|89.8|93.2|89.6|91.8|95.6|94.6|65.4|64.0|95.0|**97.2**|
|**1156**|Occlusions|Object|95.0|94.2|94.8|95.0|96.8|97.4|81.4|48.8|**98.0**|96.8|
|**1157**||Long|78.0|78.2|78.2|77.6|89.2|91.0|68.0|39.0|**91.2**|89.8|
|**1158**<br>||Spatial<br>Goal|85.8<br>88.8|85.2<br>88.4|86.4<br>86.4|86.2<br>86.2|97.6<br>96.8|97.9<br>96.4|85.2<br>62.5|91.9<br>66.8|**98.2**<br>**98.2**|98.0<br>97.2|
|**1159**|Erasing|Object|92.0|89.7|89.6|92.4|96.8|97.4|78.0|50.6|**97.6**|96.8|
|**1160**||Long|74.2|76.2|71.8|71.0|91.2|**94.0**|68.5|44.0|93.4|93.8|
|**1161**|**Avg**|**.**|66.5|61.0|59.5|60.9|80.8|80.5|47.9|56.8|**82.6**|82.2|
|**1162**|||||||||||||
|**1163**|||||||||||||
|**1164**|||||||||||||
|**1165**|||||||||||||
|**1166**|||||||||||||
|**1167**|||||||||||||
|**1168**|||||||||||||
|**1169**|||||||||||||
|**1170**<br>**1171**|Table 5: D<br>turbations|etailed<br> (noise|comp<br>level =|arison <br> 0.1,|of the <br>0.2, 0.3|average <br>). The be|SR(%) <br>st resul|of the four <br>t is highlig|LIBERO s<br>hted in bol|uites u<br>d, and|nder ac<br> the sec|tion per-<br>ond-best|
|**1172**|result is un<br>|derline<br>“|d. “Op<br>”|enVL<br>|A*” de<br>|notes the<br>|OpenV<br>|LA-OFT m|odel, “Ours|” refers|to Ro|bustVLA|
|**1173**|model, an|Ours|-C re|ers to|Robus|tVLA-C|model.||||||
|**1174**|||||||||||||
|**1175**|**Models**||**Noise**|**Level**|**0.1**||**Noise**|**Level 0.2**||**Noise**|**Level 0**|**.3**|
|**1176**||Spatial|Objec|t Goal|Long A|vg. Spatia|l Object|Goal Long|Avg. Spatial|Object|Goal L|ong Avg.|
|**1177**|OpenVLA|61.4|57.0|50.2|46.0 5|3.6<br>61.2|42.8|36.0 16.8|39.2<br>27.3|7.2|11.6<br>|0.8<br>11.7|
|**1178**|RIPT-VLA|96.2|80.2|85.8|76.6 8|4.7<br>66.0|47.0|50.6 28.6|48.1<br>30.4|18.2|20.0<br>|6.6<br>18.8|
|**1179**|OpenVLA*|95.6|84.4|87.0|**82.6** 8|7.4<br>71.6|50.2|51.4 36.0|52.3<br>36.0|16.4|25.4<br>|5.0<br>20.7|
||_π_0|81.2|79.6|87.6|61.6 7|7.5<br>47.0|40.8|56.6 25.6|42.5<br>21.4|17.2|29.0<br>|6.0<br>18.4|
|**1180**|RWR|88.2|83.8|86.0|64.2 8|0.6<br>61.0|42.4|53.0 22.6|44.8<br>31.8|16.6|30.2<br>|4.6<br>20.8|
|**1181**|ReinboT|86.2|86.0|85.6|63.2 8|0.3<br>60.2|46.4|**59.2** 22.2|47.0<br>31.2|16.6|**30.6**<br>|6.4<br>21.2|
|**1182**|ARFM|870|870|834|6708|11<br>602|470|574<br>280|482<br>324|172|288<br>|60<br>211|
|**1183**|**Ours**|.<br>**98.2**|.<br>**87.4**|. <br>**91.0**|. <br>7728|.<br>.<br>85<br>**73.4**|.<br>506|.<br>. <br>538346|.<br>.<br>531<br>**36.8**|.<br>**22.4**|.<br><br>242<br>|.<br>.<br>74<br>**22.7**|
|**1184**|**Ours-C**|97.0|86.6|<br>90.2|. <br>81.6<br>**8**|.<br><br>**8.9**<br>71.8|.<br>**51.4**|. . <br>51.8 **38.0 **|.<br><br> **53.3**<br>34.6|18.0|.<br><br>25.4<br>|.<br><br>**9.0**<br>21.8|
|**1185**|||||||||||||
|**1186**|||||||||||||
|**1187**|||||||||||||


22 

Under review as a conference paper at ICLR 2026 


23 

Under review as a conference paper at ICLR 2026 

**1242 1243 1244 1245 1246 1247 1248 1249 1250 1251 1252 1253 1254 1255 1256 1257 1258 1259 1260 1261 1262 1263 1264 1265 1266 1267 1268 1269 1270 1271 1272 1273 1274 1275 1276 1277 1278 1279 1280 1281 1282 1283 1284 1285 1286 1287 1288 1289 1290 1291 1292 1293 1294 1295** 

Table 6: Training hyperparameter configuration. 

|**Parameter**|**Value**|
|---|---|
|_General_||
|LoRA Rank|32|
|Gradient Accumulation Steps|1|
|PPO Epochs|1|
|PPO Clip Range|0_._2|
|PPO Clip High|0_._2|
|Max Step Batch Size|2<br>|
|Learning Rate (LoRA modules)|1_._0_×_10<sup>_−_4</sup>|
|Learning Rate (Action head)|5_._0_×_10<sup>_−_5</sup><br>|
|Weight Decay|1_._0_×_10<sup>_−_4</sup>|
|Gradient Clip Norm (model)|1_._0|
|Gradient Clip Norm (header)|1_._0|
|Total Steps_M_|12|
|Eval Interval_Iinterval_|1|
|Update Times_N_|10|
|_Robust Regularization Weight_||
|Jacobian Regularization Weight_α_|0_._005|
|Smooth Regularization Weight_β_|0_._0005|
|_Curriculum Learning_||
|Success Rate Thresholds (_τlow, τhigh_)<br>Success moving average parameter_γ_|0_._6_,_0_._8<br>0_._9|
|Observation Noise Range (_ϵmin,obs, ϵmax,obs_)|[0_,_1]|
|Action Noise Range (_ϵmin,action, ϵmax,action_)<br>Observation Noise Step∆_obs_<br>Action Noise Step∆_action_|<br>[0_,_0_._3]<br>0_._2<br>0_._02|
|Probability of no perturbation|0_._15|


Table 7: Dense reward components and weights. 

|**Reward Component**|**Weight**|
|---|---|
|_Sub-goal Achievement_||
|Image MSE (_e_<sup>_f_MSE(</sup><sup>_ot,o∗_</sup><br>_t_ <sup>)</sup>)<br>Image SSIM (_e_<sup>_f_SSIM(</sup><sup>_ot,o∗_</sup><br>_t_ <sup>)</sup>)<br>Gripper Image MSE (_e_<sup>_f_MSE(</sup><sup>_ot,o∗_</sup><br>_t_ <sup>)</sup>)<br>Gripper Image SSIM (_e_<sup>_f_SSIM(</sup><sup>_ot,o∗_</sup><br>_t_ <sup>)</sup>)<br>Joint Position MSE (_e_<sup>_f_MSE(</sup><sup>_st,s∗_</sup><br>_t_ <sup>)</sup>)|0_._1_/_10<br>0_._1_/_10<br>0_._1_/_10<br>0_._1_/_10<br>0_._1_/_10|
|_Task Progress_||
|Sub-goal Division ( <sup>_n_(</sup><sup>_st_)</sup><br>_|{s_<sup>_∗_</sup>_}|_<sup>)</sup>|0_._1_/_10|
|_Behavior Smoothness_||
|Joint Velocity (_−|_˙**q**_|_<sup>2</sup>)<br>Joint Acceleration (_−|_¨**q**_|_<sup>2</sup>)<br>Action Velocity (_−|_**a**_t−_1_−_**a**_t|_<sup>2</sup>)<br>|0_._1_/_10<br>0_._1_/_10<br>0_._01_/_10|
|Action Acceleration (_−|_**a**_t−_2_−_2**a**_t−_1+**a**_t|_<sup>2</sup>)|0_._01_/_10|
|_Task Completion_||
|Task Success (I_{_task is successful_}_)|1|


24 

