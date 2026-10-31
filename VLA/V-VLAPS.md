---
title: "V-VLAPS: Value-Guided Planning for Vision-Language-Action Models"
date: "2026-01-02"
authors: "Ke Ren; Ali Salamatian; Kieran Pattison; Cyrus Neary"
url: https://arxiv.org/abs/2601.00969
pdf: https://arxiv.org/pdf/2601.00969
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.00969)** / [論文ページ](https://arxiv.org/abs/2601.00969)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**V-VLAPS: Value-Guided Planning for Vision-Language-Action Models** 

**Ke Ren**<sup>* † 1</sup> **Ali Salamatian**<sup>* † 1</sup> **Kieran Pattison**<sup>* 1</sup> **Cyrus Neary**<sup>1</sup> 

# **Abstract** 

Vision-language-action (VLA) models provide strong action priors for robotic manipulation, but their reactive behavior can fail under distribution shift and long-horizon task structure. Recent VLA-guided planning methods improve execution by using pretrained policies to guide tree search, yet node selection still depends heavily on policy priors and visit-count exploration. Consequently, when the policy favors poor actions, the planner lacks a learned value signal to correct this bias. Prior work has shown that VLA representations encode rollout success and failure information, suggesting that they may also support value estimation during planning. We introduce Value-Guided Vision-Language-Action Planning and Search (V-VLAPS), which augments VLAguided planning with a lightweight value head trained on offline VLA rollouts to predict Monte Carlo returns. These predictions guide Monte Carlo Tree Search in simulation toward highervalue branches. Across five LIBERO suites, V- VLAPS matches value-free planning baseline at the default search budget in aggregate, and analysis shows that many hard failures are root-level timeouts where predicted values are weakly separated. With a larger search budget, V-VLAPS improves over the baseline in all task suites with +6 percentage points on LIBERO-Object and +4 percentage points on LIBERO-10. Our results suggest that VLA representations can support not only failure prediction, but also value-guided planning when search reaches branches where valuebased ranking matters. 

# **1. Introduction** 

Deploying robotic policies in open-world settings requires reliability under distribution shift. Recent advances in robot 

> *Equal contribution † Project lead. 1The University of British Columbia. Correspondence to: Ke Ren _<_ kren04@student.ubc.ca _>_ . 

_Preprint. July 10, 2026._ 

learning have been driven by large-scale Vision-LanguageAction (VLA) models, transformer policies that predict action sequences from multimodal observations and language instructions (Brohan et al., 2023; Zitkovich et al.; Octo Model Team et al., 2024; Kim et al.; Black et al., 2026). While VLA models serve as effective priors for generalist behaviors, they are fundamentally limited by their reliance on behavior cloning. As a result, they often exhibit brittle behavior when facing out-of-distribution (OOD) states. 

A promising approach to address this problem is to augment the pretrained model with a planning search algorithm that evaluates possible futures in simulation. This requires a simulator or world model. In our experiments, this role is played by the LIBERO simulator. One such search algorithm is Monte Carlo Tree Search (MCTS), which builds a search tree by simulating candidate action sequences before selecting an action to execute (Swiechowski et al.<sup>´</sup> , 2023). Following Neary et al. (2025), we can leverage a VLA model as a policy prior to guide the MCTS, using a visitcount heuristic to manage exploration. However, we observe that relying solely on the VLA prior is insufficient for robust long-horizon planning. In the formulation proposed by Neary et al. (2025), the search lacks a value function, meaning it has no grounded estimate of the expected future return. Consequently, if the VLA prior is inaccurate, assigning high probability to suboptimal actions, the planner has no mechanism to correct this bias other than exhaustive count-based exploration. In other words, the search relies on the imitation prior rather than the underlying reward structure. 

The signal the search lacks may already live in the VLA’s own internal features. Gu et al. (2026) show that a small probe trained on the latent features of a generalist VLA predicts task success or failure with strong cross-task generalization. If a binary success signal generalizes across tasks, the same features may also carry information useful for estimating continuous value. The natural use of such a signal in our setting is not post-hoc monitoring but active search guidance: feeding the prediction into the MCTS scoring rule to bias node selection. In this sense, our setting is an offline-to-online decision-making problem: offline rollouts of a frozen VLA are used to learn a value signal, and that signal is then used at test time to guide online MCTS planning. 

1 

**V-VLAPS: Value-Guided Planning for VLA Models** 

We introduce V-VLAPS, which extends the VLA-featureprobe approach of Gu et al. (2026) from passive failure detection to active value-guided planning. A three-layer MLP trained on Octo readouts predicts Monte Carlo discounted returns, and we add the prediction as the _Q_ term in VLAPS’s PUCT scoring rule. We evaluate V-VLAPS on five LIBERO suites against the plain Octo VLA and against VLAPS without a learned value, at two per-episode search budgets (600 s and 1800 s). On these suites both MCTS-based conditions outperform the reactive Octo VLA by about 27 percentage points on average, reproducing the result of Neary et al. (2025); the value head is therefore evaluated as an addition to an already-strong planning baseline. 

At the 600 s budget, V-VLAPS matches VLAPS in aggregate (both at 87 _._ 4%), and a failure-mode analysis shows that many hard failures are MCTS timeouts at the root rather than clear value-head errors. Near the root, candidate branches are still far from task completion, so the value head often assigns similarly small values to many alternatives and has little discriminative power. With the budget extended to 1800 s, search can reach deeper states where branch values separate more clearly. In this regime, V-VLAPS exceeds VLAPS by +6pp on libero ~~o~~ bject and +4pp on libero ~~1~~ 0. These results suggest that small probes trained on frozen VLA features can serve not only as failure detectors (Gu et al., 2026), but also as learned planning components when search reaches states where value-based branch ranking is important. 

2022), self-consistency sampling (Wang et al.), and MCTS during inference (Hao et al., 2023). 

Recent work has also begun to study how extra test-time computation can improve VLA execution rather than relying solely on one-shot reactive action prediction (Kwok et al.; Yang et al., 2025). Neary et al. (2025) introduce Vision-Language-Action Planning and Search (VLAPS), which embeds a pre-trained VLA into a model-based search procedure and uses the VLA to define action proposals and abstractions for planning. In our work, we build on VLAPS and keep the same fixed VLA backbone, but additionally learn a value function over its latent state and incorporate the resulting value predictions into VLAPS’s scoring rule to guide search. 

## **2.2. Monte Carlo Tree Search** 

A natural way to compensate for the myopic behaviour of reactive policies is to add a search procedure that can simulate possible future outcomes before committing to an action. Monte Carlo Tree Search (MCTS) is a widely used algorithm for this purpose. It incrementally builds a search tree by repeatedly simulating trajectories from the current state, and at each iteration it selects actions that balance exploring uncertain branches with exploiting branches that have produced good returns in previous simulations (Swiechowski<sup>´</sup> et al., 2023). Typically, each iteration proceeds through four phases: selection, expansion, simulation, and backpropagation. The resulting statistics over node visit counts and returns are then used to estimate action values at the root. 

# **2. Related Work** 

## **2.1. Vision–Language–Action Policies** 

Vision–language–action (VLA) models are designed to map visual observations and natural-language instructions directly to robot actions. Early systems showed that a single transformer policy can be trained on large collections of robot demonstrations and language-labelled tasks, and then be reused across many manipulation skills (Brohan et al., 2023; Zitkovich et al.). In our work, we use Octo (Octo Model Team et al., 2024) as a fixed generalist VLA backbone and build our method on top of its latent representation; the same method can be used with other VLA models. 

Although VLA models can perform a wide range of tasks, they are typically used in a purely reactive way: at each step, the model receives the current observation and instruction and outputs the next action (or action chunk), without explicit long-horizon planning. In challenging scenes or out-of-distribution configurations, this can lead to failures that the policy does not recover from (Gu et al., 2026). In the language modeling paradigm, many methods have been introduced to mitigate similar issues by scaling test-time compute, such as chain-of-thought prompting (Wei et al., 

MCTS has been particularly successful in domains where a reasonably accurate simulator is available. In board games such as Go, Chess, and Shogi, MCTS combined with learned policies and values has led to systems that reach and surpass human expert performance (Silver et al., 2016; 2017a). In these settings, the search runs entirely in simulation and only the final chosen move is executed in the real environment. Neary et al. (2025) bring this style of planning to vision–language–action models in the VLAPS framework. They use MCTS over discrete action chunks, with a pre-trained VLA policy providing action priors that focus and refine the search of an otherwise completely intractable space. Their formulation combines their VLAinformed prior with visit-count-based exploration heuristics in a PUCT-style scoring rule which allows MCTS to exploit the strengths of the pre-trained policy while still exploring alternative action sequences. 

## **2.3. Learned Value Functions for Tree Search and VLA Planning** 

Combining learned value functions with tree search has proved highly effective in domains where planning is possible. In AlphaGo and its successors, deep neural networks 

2 

**V-VLAPS: Value-Guided Planning for VLA Models** 


_Figure 1._ Overview of our value-guided VLAPS extension. At each MCTS node, the current observations and language instruction (e.g., “Move ketchup to basket”) are passed through the frozen VLA backbone and our value head (MLP) to produce a scalar value estimate. This value is attached to the corresponding node and used in the VLAPS scoring rule to bias node selection. Nodes with higher predicted value (green) are selected more often and tend to lead to successful task completions, while low-value nodes (red) are down-weighted during search. 

predict both a policy over moves and a scalar value estimate from a board position; Monte Carlo Tree Search uses the policy to prioritize promising actions and the value to evaluate leaf nodes without long rollouts (Silver et al., 2016; 2017b;a). This combination allows the search procedure to concentrate computation on moves that are both likely under the learned policy and lead to positions that the value function predicts as strong, rather than relying solely on visit counts and simulation outcomes of intractably long rollouts. 

VLAPS adopts a similar strategy for vision–language–action policies, but stops short of learning an explicit value function over the VLA latent state. In Neary et al. (2025), the quality of a node is determined by search statistics and VLA-derived action priors, but there is no separate learned estimate of the state’s value. In contrast, we keep the underlying VLA and search procedure fixed, and introduce a small value head which takes the VLA latent state as input. This head is trained to predict Monte Carlo returns from VLA rollouts, and its predictions are incorporated into the VLAPS selection rule. Conceptually, this brings the use of value functions in VLAPS closer to the value-guided tree search used in game-playing systems like AlphaGo, while operating in the setting of vision–language–action control. 

More directly related is SAFE (Gu et al., 2026), which trains a small probe (an MLP or LSTM) on the VLA’s frozen latent features and uses the resulting success/failure prediction as a post-hoc monitor. Our value head adopts the same feature source and probe family but predicts a continuous Monte Carlo discounted return, and the prediction enters the PUCT scoring rule during search rather than after the episode. 

# **3. Method** 

We extend VLAPS by learning a value function over Octo latent states and using this value to guide Monte Carlo Tree Search in simulation. As in VLAPS, the search uses a simulator to roll candidate action chunks forward before execution. We first collect rollouts of the Octo model and compute Monte Carlo value targets for each state (Section 3.1). We then train a three-layer MLP (the “value head”) to predict these targets from Octo’s last-layer representation (readout) (Section 3.2). Finally, we integrate the learned value into VLAPS’ tree search by modifying the selection score to prefer action chunks that lead to high-value successor states (Section 3.3). 

3 

**V-VLAPS: Value-Guided Planning for VLA Models** 

## **3.1. Data Collection** 

We construct training data for the value head by rolling out a fixed pre-trained VLA policy, without any planning, on LIBERO (Liu et al., 2023) tabletop manipulation tasks. For each suite, we collect value-head training rollouts on all tasks but restrict each task to four of the ten available initial states: indices 0, 3, 6, and 9. Evaluation uses all ten initial states per task (Section 4), so six initial states per task are unseen during value-head data collection. This gives a partial initial-state generalization test while preserving comparability with the full ten-initial-state evaluation used for all methods. 

At the beginning of each episode, the environment provides an initial observation _o_ 0 and a language instruction _g_ . At each decision step _t_ , the VLA (Octo (Octo Model Team et al., 2024)) receives ( _ot, g_ ), computes a latent readout vector _ht ∈_ R<sup>_d_</sup> which acts as the summary representation of the past observations and the task. It then uses the readout to output an action chunk _ct_ , which consists of a sequence of low-level actions. We execute the entire chunk _ct_ in the environment, applying each low-level action in order, until the chunk finishes or the episode terminates. The environment then returns the next observation _ot_ +1, and we query the VLA again. This produces an episode as a sequence of decision steps ( _o_ 0 _, c_ 0 _, o_ 1 _, c_ 1 _, . . . , oT_ ). 

Episodes terminate either when the task is successfully completed or when a timeout horizon is reached. We use a sparse terminal value: if the task is successfully completed before the timeout, the episode receives a terminal value of 1; otherwise (failure or timeout), it receives a terminal value of 0. 

For each decision step _t_ in an episode, we define a Monte Carlo value target by propagating the terminal value backward through time. Let _R ∈{_ 0 _,_ 1 _}_ denote the terminal value and _T_ the index of the final decision step. We assign each state at step _t_ a target 


where _γ ∈_ (0 _,_ 1] is a discount factor; we use _γ_ = 0 _._ 99. This target is a Monte Carlo estimate of the state value under our sparse success value when following the VLA policy. 

We pair each readout with its value target to form a training example ( _ht, Gt_ ), and aggregate these across many rollouts to build a per-suite dataset of state–value pairs. The raw target distribution is heavily skewed toward zero: failed episodes contribute only zero-valued targets, and even successful episodes have many early-step targets close to zero because _γ_<sup>_T −t_</sup> is small when _T − t_ is large. A value head trained on this distribution can collapse to predicting zero almost everywhere, so we rebalance once during preprocess- 

ing: targets are bucketed into ten equal-width bins on [0 _,_ 1], and the bottom bin is downsampled to match the combined size of the other nine bins. 

## **3.2. Value Head Training** 

Our goal is to learn a value function that maps the VLA’s latent representation at each decision step to the scalar value target defined in Section 3.1. Concretely, given the Octo readout vector _ht ∈_ R<sup>_d_</sup> at decision step _t_ , we learn a function _Vθ_ : R<sup>_d_</sup> _→_ R that predicts a scalar estimate _v_ ˆ _t_ of the state value: _v_ ˆ _t_ = _Vθ_ ( _ht_ ). 

We parameterize _Vθ_ as a lightweight three-layer multilayer perceptron (MLP) with approximately 2 _._ 4M parameters in total. The architecture is intentionally small compared to the underlying Octo model, so that evaluating the value head adds minimal overhead during planning. 

We train this value head on the dataset of readout–value pairs _{_ ( _ht, Gt_ ) _}_ . The training objective is to regress onto the Monte Carlo value targets _Gt_ using mean squared error: . _L_ ( _θ_ ) = E( _ht,Gt_ )�( _Vθ_ ( _ht_ ) _− Gt_ )<sup>2�</sup> 

In practice, we approximate this expectation by sampling mini-batches from the dataset and performing stochastic gradient descent with the Adam optimizer. During training, the parameters of the underlying Octo VLA are kept fixed; only the value head parameters _θ_ are updated. After convergence, _Vθ_ provides a compact estimate of the state value at each decision step, which we use to guide the tree search. 

## **3.3. Value-Guided Planning** 

At each decision point, VLAPS builds a temporary search tree in simulation. The root node represents the current environment state before the next action chunk is chosen. Each edge corresponds to a candidate action chunk, and each child node represents the simulated state reached after executing that chunk. The search expands this tree until a simulated success is found or the wall-time budget is reached, then executes an action chunk from the root and replans from the next observation. 

Motivated by the value-plus-prior structure of PUCT-style search, we integrate the learned value head into the VLAPS tree-search rule while leaving the rest of the VLAPS search procedure unchanged (Figure 1). VLAPS already provides the prior/exploration term through its VLA-guided action prior and visit statistics; V-VLAPS adds a learned value term for the successor state reached by each candidate chunk. At a node _v_ , VLAPS samples a finite set of candidate action chunks _a_<sup>_i_</sup> from the VLA-induced action distribution and scores them using the VLAPS prior/exploration term 

4 

**V-VLAPS: Value-Guided Planning for VLA Models** 


where _It_ is the current observation, _LT_ is the task instruction, _ψ_ Φ _v_ is the VLAPS prior over the sampled candidate chunks, and _N_ ( _v, a_<sup>_i_</sup> ) is the number of times candidate _a_<sup>_i_</sup> has been selected from node _v_ . We use this term exactly as in VLAPS. 

V-VLAPS adds a learned value for the child node reached by each candidate chunk. For a candidate action chunk _a_<sup>_i_</sup> at node _v_ , the simulator rolls the chunk forward to obtain the successor state _s_<sup>_′_</sup> . We compute the Octo readout _h_ ( _s_<sup>_′_</sup> ) for this state and evaluate the value head: 


We use this successor-state value as the value term for the node-action pair, 


Because the simulated transition for a fixed action chunk is deterministic in our LIBERO setup, the successor-state value estimates the continuation value after choosing _a_<sup>_i_</sup> . 

The final V-VLAPS selection score is 


We use a fixed value coefficient _λV_ = 1 in all experiments. Therefore, V-VLAPS differs from VLAPS only by adding the learned value term _Qθ_ with a fixed coefficient. The action sampler, action library, LIBERO simulator, and MCTS hyperparameters are kept fixed across the VLAPS and V- VLAPS conditions. 

# **4. Experiments** 

All experiments are conducted in LIBERO simulation. For VLAPS and V-VLAPS, the same simulator is used both for planning rollouts and for evaluation. This gives a controlled setting where the planner has access to an accurate model of the environment. We evaluate three methods on five LIBERO suites: the plain Octo VLA without planning ( _VLA_ ), VLAPS without a learned value ( _VLAPS_ , the formulation of Neary et al. (2025)), and V-VLAPS, which adds the learned value head from Section 3.3 to the VLAPS scoring rule. The five suites cover different task types: _libero_ _~~o~~ bject_ tests object identification with pick-and-place, _libero_ _~~s~~ patial_ tests spatial reasoning between objects and target regions, _libero_ _~~g~~ oal_ tests goal-conditioned behaviour, _libero_ _~~1~~ 0_ is ten long-horizon tasks, and _libero_ _~~9~~ 0_ is ninety diverse manipulation tasks (Liu et al., 2023). The value head is trained 

once from offline VLA rollouts for each suite and then frozen during evaluation. All test-time adaptation comes from MCTS planning rather than parameter updates. 

Each (condition, suite, budget) cell is evaluated on 100 episodes. For the four 10-task suites this is the full 10 _×_ 10 grid of tasks and initial states, and for libero ~~9~~ 0 we sample 10 tasks and use all 10 initial states per sampled task. As described in Section 3.1, the value head is trained using rollouts from only four initial states per task. The reported evaluation therefore tests both performance on the valuehead data-collection states and generalization to six initial states per task that are unseen during value-head training. MCTS uses two per-episode wall-time budgets, 600 s by default and 1800 s for the extended-budget experiments. The MCTS hyperparameters are held fixed across all conditions and suites; the full configuration is in Section B. 

We train one value head per suite, with a 90 _/_ 10 train/validation split (fixed seed). Per-suite balanced training-data sizes range from 7 _,_ 830 examples (libero ~~o~~ bject) to 18 _,_ 792 (libero ~~s~~ patial); the full breakdown is in Section A. 

# **5. Results** 

We separate the benefit of planning from the additional benefit of value guidance. We first compare aggregate success rates at two wall-time search budgets, then inspect failures at the default budget to understand when the learned value term can and cannot affect search. 

## **5.1. Main results** 

The main pattern is that value guidance does not change aggregate performance at the default search budget, but improves success rate when the search budget is increased. Table 1 reports success rates for the three methods on each of the five suites. At the 600 s wall-time search budget, V-VLAPS and VLAPS both average 87 _._ 4% across the five suites. No per-suite difference exceeds 3pp, which sits inside the binomial standard error of _≈_ 3pp at _p ≈_ 0 _._ 9. At the 1800 s wall-time search budget, the gap widens to +3 _._ 2pp (91 _._ 6% for V-VLAPS vs. 88 _._ 4% for VLAPS). The largest gains are on libero ~~o~~ bject (+6pp) and libero ~~1~~ 0 (+4pp). The other three suites already reach at least 88% success at the 600 s budget for both planning methods, and move by at most _±_ 2pp at the larger search budget. Because each cell contains 100 episodes, we interpret 1–3pp differences as suggestive rather than conclusive and focus our claims on the larger gaps under the extended search budget. 

## **5.2. Wall-time scaling and a task-7 case study** 

On the two suites with the largest remaining headroom, increasing the wall-time search budget improves task suc- 

5 

**V-VLAPS: Value-Guided Planning for VLA Models** 

_Table 1._ Success rate (%) by method and suite at the default (600 s) and extended (1800 s) per-episode search budgets. Each cell aggregates 100 episodes. **VLA** (no planning) provides context for the regime; **VLAPS** (Neary et al., 2025) is the prior-work planning baseline; **V-VLAPS** is our extension. Bold V-VLAPS cells highlight the 1800 s wall-time gains on the headroom suites (libero ~~o~~ bject, libero ~~1~~ 0). 

|||600s|budget|1800|s budget|
|---|---|---|---|---|---|
|**Suite**|**VLA**|**VLAPS**|**V-VLAPS**|**VLAPS**|**V-VLAPS**|
|libero<br>~~o~~bject|37|82|85|87|**93**|
|libero<br>~~s~~patial|81|96|95|96|**97**|
|libero<br>~~g~~oal|88|92|**93**|90|**93**|
|libero<br>~~1~~0|38|77|75|81|**85**|
|libero<br>~~9~~0|57|**90**|89|88|**90**|
|**Avg.**|60.2|87.4|87.4|88.4|**91.6**|


cess more for V-VLAPS than for VLAPS. On libero ~~o~~ bject, V-VLAPS increases from 85% at 600 s to 93% at 1800 s (+8pp), while VLAPS increases from 82% to 87% (+5pp). The V-VLAPS and VLAPS gap therefore grows from +3pp to +6pp. On libero ~~1~~ 0, the asymmetry is larger: V-VLAPS increases by +10pp (75% _→_ 85%), while VLAPS increases by +4pp (77% _→_ 81%), so the per-suite gap changes from _−_ 2pp to +4pp. 

This difference is sharpest on a single hard task. To tighten the comparison on libero ~~o~~ bject task 7, we extended the default ten initial states to twenty (indices 0–19) at the 1800s search budget. V-VLAPS reaches 17 _/_ 20 (85%), while VLAPS reaches 13 _/_ 20 (65%). The _N_ = 10 data (Appendix C) show the same pattern from the original evaluation set: when moving from 600 s to 1800 s, VLAPS goes from 8 _/_ 10 to 6 _/_ 10, while V-VLAPS goes from 5 _/_ 10 to 10 _/_ 10. On this task, extra search time helps the value-guided variant more than VLAPS without the learned value term. 

libero ~~s~~ patial, libero ~~g~~ oal, and libero ~~9~~ 0 are already at or above 88% success at 600 s, and neither the larger search budget nor the value head moves them by more than _±_ 2pp.<sup>1</sup> 

## **5.3. Failure-mode analysis** 

Root-level timeouts account for most failures on libero ~~o~~ bject tasks 6, 7, and 8 at the 600s search budget (Table 2). We define a root-level timeout as a failed episode in which MCTS spends the full wall-time budget at the root node, before executing the first action chunk. These failures indicate that the search often does not reach deeper states where value-based ranking could change later decisions. 

This pattern appears for both planning methods. In V- VLAPS, 13 of the 15 failed episodes are root-level timeouts. In VLAPS, 14 of the 18 failed episodes show the same behaviour. For V-VLAPS, these runs contain only the initial 

> 1VLAPS drops slightly on libero ~~g~~ oal (92% _→_ 90%) and libero ~~9~~ 0 (90% _→_ 88%) at 1800 s. Both moves are within sampling noise. 

value-head evaluations at the root, with wall-clock times between 605 and 611 s when the search stops. The small overshoot past 600 s comes from checking the time budget after a search iteration completes. 

_Table 2._ Failure modes on libero ~~o~~ bject tasks 6–8 at the 600 s search budget. A root-level timeout is a failed episode in which MCTS remains at the root node until the wall-time cap is reached, before executing the first action chunk. 

|**Method**|**Failures**|**Root**<br>**timeouts**|**Fraction**|
|---|---|---|---|
|VLAPS|18|14|77.8%|
|V-VLAPS|15|13|86.7%|


For the V-VLAPS root-level timeouts, the value head predicts successor-state values between _−_ 0 _._ 01 and 0 _._ 02. This narrow range is expected near the root of hard task configurations. Most candidate branches are still far from task completion, so their predicted continuation values are close to zero and weakly separated. In these near-root states, the value term has little ability to distinguish among alternatives. The extended-budget results are consistent with this interpretation: value guidance becomes more useful when MCTS reaches deeper states where different branches have more separated continuation values. 

# **6. Discussion and Conclusion** 

V-VLAPS gains over VLAPS in a specific regime: when MCTS has time to move beyond near-root states, and when the task has remaining headroom for value-guided ranking to matter. Near the root of hard tasks, candidate branches often remain far from completion and receive similarly small value estimates, so the value term provides little separation. The first condition fails at 600 s on the hardest libero ~~o~~ bject tasks, where most failures are root-level timeouts (Section 5.3). The second fails on libero ~~s~~ patial, libero ~~g~~ oal, and libero ~~9~~ 0, where the prior pipeline is already near ceiling. The libero ~~o~~ bject and libero ~~1~~ 0 gains at 1800 s are the 

6 

**V-VLAPS: Value-Guided Planning for VLA Models** 

regime where both conditions hold: search reaches deeper branches, and those branches have enough performance headroom for the value head’s ranking to change decisions. 

V-VLAPS shows that the VLA-feature probe Gu et al. (2026) introduced for failure detection extends to active search guidance. With the binary failure target replaced by a Monte Carlo return and the prediction fed into the PUCT scoring rule, the same probe architecture can bias an MCTS search toward higher-return branches rather than only flag failures after the fact. We have demonstrated this for value-guided node ranking; whether the same probe family can drive other components of the planning loop, such as termination or branch pruning, is an open empirical question. 

**Limitations.** V-VLAPS requires a simulator or world model for search. In this paper, we evaluate in LIBERO, where the simulator used for planning matches the evaluation environment. Applying the same idea outside simulation would require an accurate learned or engineered world model. Our experiments use Octo as the VLA backbone, and evaluating whether the same pattern holds for other VLA models such as _π_ 0 (Black et al., 2026) is an important next step. The value head is trained on rollouts of the unguided VLA, so its predictions on states the search visits are off-policy with respect to V-VLAPS execution. Per-suite training sets are small, ranging from 7 _,_ 830 to 18 _,_ 792 examples (Appendix A), and whether more training data would widen the 1800 s gap or close the 600 s gap is untested. In addition, a controlled ablation with shuffled value targets or a randomly initialized value head would further isolate the contribution of learned value estimates, and we leave this for future work. 

**Future work.** Two directions follow directly from the findings above. Training the value head on V-VLAPS rollouts instead of unguided VLA rollouts would address the off-policy gap, and is a prerequisite for iterative refinement of the value estimate. Using the value head to prune branches during expansion would convert the root-level timeouts of Section 5.3 into search compute spent on the branches the value head ranks highest. Two further directions are more speculative. Replacing the MSE regression objective with the HL-Gauss classification head of Farebrother et al. (2024) is a natural alternative; we attempted it and hit class-imbalance issues that we expect would ease with more per-suite training data. Aggregating the valuehead input across multiple transformer layers, as Gu et al. (2026) suggest for SAFE, may expose signal the final readout averages out. 

# **Impact Statement** 

This paper studies value-guided MCTS planning over a fixed pretrained vision-language-action policy, evaluated in LIBERO simulation only. Our per-episode test-time search budgets are in the hundreds to thousands of seconds, which shifts compute from training to deployment with the associated energy cost. We do not foresee impacts specific to this contribution that are not already raised by the underlying VLA, planning, and failure-detection work this paper builds on. 

# **References** 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., Levine, S., LiBell, A., Mothukuri, M., Nair, S., Pertsch, K., Shi, L. X., Tanner, J., Vuong, Q., Walling, A., Wang, H., and Zhilinsky, U. _π_ 0: A vision-language-action flow model for general robot control, 2026. URL https: //arxiv.org/abs/2410.24164. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al. Rt-1: Robotics transformer for real-world control at scale. _Robotics: Science and Systems XIX_ , 2023. 

- Farebrother, J., Orbay, J., Vuong, Q., Ta¨ıga, A. A., Chebotar, Y., Xiao, T., Irpan, A., Levine, S., Castro, P. S., Faust, A., et al. Stop regressing: training value functions via classification for scalable deep rl. In _Proceedings of the 41st International Conference on Machine Learning_ , pp. 13049–13071, 2024. 

- Gu, Q., Ju, Y., Sun, S., Gilitschenski, I., Nishimura, H., Itkina, M., and Shkurti, F. Safe: Multitask failure detection for vision-language-action models. _Advances in Neural Information Processing Systems_ , 38:40041–40076, 2026. 

- Hao, S., Gu, Y., Ma, H., Hong, J., Wang, Z., Wang, D., and Hu, Z. Reasoning with language model is planning with world model. In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_ , pp. 8154–8173, 2023. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E. P., Sanketi, P. R., Vuong, Q., et al. Openvla: An open-source visionlanguage-action model. In _8th Annual Conference on Robot Learning_ . 

- Kwok, J., Agia, C., Sinha, R., Foutter, M., Li, S., Stoica, I., Mirhoseini, A., and Pavone, M. Robomonkey: 

7 

**V-VLAPS: Value-Guided Planning for VLA Models** 

- Scaling test-time sampling and verification for visionlanguage-action models. In _9th Annual Conference on Robot Learning_ . 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 

- Neary, C., Younis, O. G., Kuramshin, A., Aslan, O., and Berseth, G. Improving pre-trained vision-languageaction policies with model-based search. _arXiv preprint arXiv:2508.12211_ , 2025. 

- Octo Model Team, Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., Luo, J., Tan, Y. L., Chen, L. Y., Sanketi, P., Vuong, Q., Xiao, T., Sadigh, D., Finn, C., and Levine, S. Octo: An open-source generalist robot policy, 2024. URL https: //arxiv.org/abs/2405.12213. 

   - Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., Le, Q. V., Zhou, D., et al. Chain-of-thought prompting elicits reasoning in large language models. _Advances in neural information processing systems_ , 35:24824–24837, 2022. 

   - Yang, S., Zhang, Y., He, H., Pan, L., Li, X., Bai, C., and Li, X. Steering vision-language-action models as antiexploration: A test-time scaling approach. _arXiv preprint arXiv:2512.02834_ , 2025. 

   - Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., Wu, J., Wohlhart, P., Welker, S., Wahid, A., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _7th Annual Conference on Robot Learning_ . 

- Silver, D., Huang, A., Maddison, C., Guez, A., Sifre, L., Driessche, G., Schrittwieser, J., Antonoglou, I., Panneershelvam, V., Lanctot, M., Dieleman, S., Grewe, D., Nham, J., Kalchbrenner, N., Sutskever, I., Lillicrap, T., Leach, M., Kavukcuoglu, K., Graepel, T., and Hassabis, D. Mastering the game of go with deep neural networks and tree search. _Nature_ , 529:484–489, 01 2016. doi: 10.1038/nature16961. 

- Silver, D., Hubert, T., Schrittwieser, J., Antonoglou, I., Lai, M., Guez, A., Lanctot, M., Sifre, L., Kumaran, D., Graepel, T., Lillicrap, T., Simonyan, K., and Hassabis, D. Mastering chess and shogi by self-play with a general reinforcement learning algorithm, 2017a. URL https://arxiv.org/abs/1712.01815. 

- Silver, D., Schrittwieser, J., Simonyan, K., Antonoglou, I., Huang, A., Guez, A., Hubert, T., Baker, L., Lai, M., Bolton, A., Chen, Y., Lillicrap, T., Hui, F., Sifre, L., van den Driessche, G., Graepel, T., and Hassabis, D. Mastering the game of go without human knowledge. _Nature_ , 550(7676):354–359, October 2017b. doi: 10. 1038/nature24270. 

- Swiechowski,´ M., Godlewski, K., Sawicki, B., and Mandziuk, J.´ Monte carlo tree search: A review of recent modifications and applications. _Artificial Intelligence Review_ , 56(3):2497–2562, 2023. 

- Wang, X., Wei, J., Schuurmans, D., Le, Q. V., Chi, E. H., Narang, S., Chowdhery, A., and Zhou, D. Selfconsistency improves chain of thought reasoning in language models. In _The Eleventh International Conference on Learning Representations_ . 

8 

**V-VLAPS: Value-Guided Planning for VLA Models** 

# **A. Per-suite training-data sizes** 

Table 3 reports the per-suite value-head training-data sizes after rebalancing (Section 3.1). These datasets are collected only from initial states 0, 3, 6, and 9 for each task, and the main evaluation in Table 1 uses all ten initial states per task, including six initial states unseen during value-head training. For libero ~~1~~ 0, the raw distribution was already balanced (50 _._ 0% zero), so its Balanced count equals its Raw count. 

_Table 3._ Per-suite training-data sizes after rebalancing. **Raw** is the count collected from VLA rollouts before rebalancing. **% zero** is the fraction of raw examples with _Gt_ = 0. **Balanced** is the count after downsampling the bottom bin to match the combined size of the other nine bins. **Train** / **Val** are the 90 _/_ 10 split sizes. 

|**Suite**|**Raw**|**% zero**|**Balanced**|**Train**|**Val**|
|---|---|---|---|---|---|
|libero<br>~~o~~bject|60,695|92.8|8,700|7,830|870|
|libero<br>~~s~~patial|28,580|63.5|20,880|18,792|2,088|
|libero<br>~~g~~oal|34,155|70.3|20,300|18,270|2,030|
|libero<br>~~1~~0|11,020|50.0|11,020|9,918|1,102|
|libero<br>~~9~~0|63,595|86.8|16,810|15,129|1,681|


# **B. Value-head training and MCTS hyperparameters** 

This appendix lists the hyperparameters used to train the value head (Table 4) and to run MCTS in the experiments of Section 4 (Table 5). All evaluations were run on a single NVIDIA H100 GPU; one 100-episode _(suite, condition)_ cell at the 600 s budget completes in roughly 3 _._ 5–4 _._ 5 h. 

_Table 4._ Value-head training hyperparameters (Section 3.2). 

|**Setting**|**Value**|
|---|---|
|Architecture (MLP)|768_→_3072(ReLU)_→_scalar|
|Parameter count|_∼_2_._4M|
|Optimizer|Adam|
|Initial learning rate|1_×_10<sup>_−_4</sup>|
|Learning-rate schedule|cosine decay (_α_= 0_._1)|
|Batch size|64|
|Epochs|100|
|Train/val split|90_/_10(fixed seed42)|
|Loss|MSE on Monte Carlo returns_Gt_|
|Discount_γ_|0_._99|
|Target rebalancing|10-bin equal-width on[0_,_1], bottom bin downsampled|


_Table 5._ MCTS hyperparameters, shared between VLAPS and V-VLAPS (Section 3.3). The value head adds the _Q_ term in the SCORE function for the V-VLAPS condition only. 

|**Setting**|**Value**|
|---|---|
|PUCT exploration weight_ψ_|1_._0|
|Action samples per node|300|
|Expansions per node|10|
|Expansions per MCTS step|1|
|Maximum tree depth|80|
|Maximum simulated rollout length|300|
|Chunk steps simulated per expansion|4|
|Replan after each executed chunk|yes|
|Per-episode wall-time cap|600s (default budget),1800s (extended budget)|
|Action chunk library size|2_,_000medoids of all-suite VLA successes|
|_β_Φ distribution (action sampler)<br>_ψ_Φ_v_ distribution (PUCT prior)|softmax over chunk distances,_α_= 10,_ϵ_= 0_._1<br>softmax over sampled chunks,_α_= 5|
|VLA generation temperature|0_._0|
|Terminate search on simulated success|yes|


9 

**V-VLAPS: Value-Guided Planning for VLA Models** 

# **C. Per-task results on libero** **~~o~~ bject** 

Table 6 decomposes the libero ~~o~~ bject row of Table 1 by task. Tasks 0–5 and 9 sit at or near the 90–100% ceiling for both conditions at both budgets; the variance that drives the suite-level differences is concentrated on tasks 6, 7, and 8. The _N_ = 20 task-7 result of Section 5.2 is a tighter measurement of the same task. 

_Table 6._ Per-task success counts on libero ~~o~~ bject at both per-episode wall-time budgets, 10 initial states per task. Full-suite totals match the libero ~~o~~ bject row of Table 1. The bold cell highlights the V-VLAPS 5 _/_ 10 _→_ 10 _/_ 10 swing on task 7 at the larger budget. 

||600s|budget|1800|s budget|
|---|---|---|---|---|
|**Task**|**VLAPS**|**V-VLAPS**|**VLAPS**|**V-VLAPS**|
|0|10/10|10/10|10/10|10/10|
|1|10/10|10/10|10/10|10/10|
|2|10/10|10/10|10/10|10/10|
|3|10/10|10/10|10/10|10/10|
|4|8/10|9/10|9/10|9/10|
|5|9/10|10/10|9/10|10/10|
|6|5/10|3/10|6/10|5/10|
|7|8/10|5/10|6/10|**10/10**|
|8|3/10|8/10|8/10|9/10|
|9|9/10|10/10|9/10|10/10|
|**Total**|**82/100**|**85/100**|**87/100**|**93/100**|


# **D. t-SNE projection of Octo readouts** 

Figure 2 shows a t-SNE projection of the Octo last-layer readouts on libero ~~o~~ bject, coloured by the Monte Carlo value target _Gt_ . The visible structure between high- and low-target states is consistent with the SAFE finding of Gu et al. (2026) that VLA latent features carry outcome-discriminative signal. 


_Figure 2._ t-SNE projection of Octo last-layer readouts _ht_ on libero ~~o~~ bject, coloured by Monte Carlo value target _Gt_ . Successful and failed rollouts occupy visually distinct regions of the embedding. 

10 

