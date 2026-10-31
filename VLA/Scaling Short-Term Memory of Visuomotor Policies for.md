---
title: "Scaling Short-Term Memory of Visuomotor Policies for Long-Horizon Tasks"
date: "2026-06-15"
authors: "Rutav Shah; Rajat Kumar Jenamani; Xiaohan Zhang; Lingfeng Sun; Roberto Martín-Martín; Yuke Zhu"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2606.16178
pdf: https://arxiv.org/pdf/2606.16178
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.16178)** / [論文ページ](https://arxiv.org/abs/2606.16178)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Scaling Short-Term Memory of Visuomotor Policies for Long-Horizon Tasks 

Rutav Shah<sup>1</sup><sup>_,_2</sup> , Rajat Kumar Jenamani<sup>1</sup> , Xiaohan Zhang<sup>1</sup> , Lingfeng Sun<sup>1</sup> , Roberto Mart´ın-Mart´ın<sup>2</sup> , Yuke Zhu<sup>2</sup> , Deva Ramanan<sup>1</sup> , Karl Schmeckpeper<sup>1</sup> 

> 1Robotics and AI Institute, 2The University of Texas at Austin 

**_Abstract_ —Many robotic tasks require short-term memory, whether it’s retrieving an object that’s no longer visible or turning off an appliance after a set period. Yet, most visuomotor policies trained via imitation learning remain myopic, relying only on immediate sensory input without using past experiences to guide decisions. We present PRISM, a transformer-based architecture for visuomotor policies to effectively use short-term memory via two key components: (i) gated attention, which selectively filters retrieved information to suppress irrelevant details, improving performance by reducing the spurious correlations between the history and current action prediction, and (ii) a hierarchical architecture that first compresses local interactions into compact tokens and then integrates them to capture temporally extended dependencies, improving its compute and memory footprint. Together, these mechanisms enable us to scale short-term memory in visuomotor policies for up to two minutes. To systematically evaluate memory in visuomotor control, we introduce REMEMBENCH—a benchmark of eight diverse household manipulation tasks spanning four categories of short-term memory— designed to foster general memory mechanisms rather than siloed, task-specific solutions. PRISM consistently outperforms prior works, including transformer-based visuomotor policies with short-term memory, recurrent architectures, and other transformer variants—achieving an absolute improvement of** 5% **–** 12% **over the strongest baseline in REMEMBENCH and realworld evaluations. On the standard ROBOCASA and LIBERO benchmarks, it achieves absolute improvements of** 11% **–** 15% **over its no-memory variant and fine-tuned Vision-LanguageAction baselines such as GR00T-N1-3B and OpenVLA, despite not leveraging any large-scale pretraining. Together, PRISM and REMEMBENCH establish a foundation for developing and evaluating short-term memory–augmented visuomotor policies that scale to long-horizon tasks. Additional materials are available at shahrutav.github.io/short-term-memory** 

**_Index Terms_ —imitation learning, short-term memory** 

## I. INTRODUCTION 

Memory is central to intelligent behavior: human cognition depends on retaining past experiences to guide ongoing actions [1, 2]. Classic studies in human cognition distinguish between sensory, short-term, and long-term memory [3]. Among these, short-term memory, which spans seconds to minutes, is essential in everyday activities such as remembering to stir at regular intervals, retrieving objects that are no longer visible, or counting scoops of salt [4]. Without it, behavior collapses to responses grounded only in the present observation, unable to account for past experiences. 

Recent advances in robot learning have led to the development of generalist visuomotor policies through imitation learning [5–7]. However, they do not target imitation learning 

under partial observability and consequently adopt policies without short-term memory, relying solely on immediate sensory inputs. Most visuomotor policies rely on vanilla transformer backbones [8], and naively extending this architecture with short-term memory via longer context windows poses two main drawbacks. First, it is susceptible to irrelevant information in the context window [9]. This can induce spurious correlations, _e.g._ , linking past distractor locations to a left or right placement decision, degrading test performance [10, 11]. While these spurious correlations could be reduced with more data, scaling robot data is challenging because teleoperating robots is labor-intensive. Second, at test time, its computational and memory footprint scale linearly with the number of tokens in the context length, making it inefficient to process high-dimensional sensory inputs, such as image observations, over long temporal sequences [8]. These drawbacks limit the scalability of short-term memory over long horizons in visuomotor policies. 

To bridge this gap, we introduce **PRISM** : a **<u>P</u>** <u>olicy A</u> **<u>r</u>** <u>ch</u> **<u>i</u>** <u>tecture with</u> **<u>S</u>** <u>hort-Term</u> **<u>M</u>** <u>emory for visuomotor control</u> that maps sequences of past sensory inputs and actions to future actions in a closed-loop setting. Building on technical innovations in related fields of vision and language processing, PRISM extends the vanilla transformer architecture with two key modifications. First, a post-attention gating mechanism selectively filters information, thereby introducing an explicit pathway to suppress irrelevant information [12]. Second, a hierarchical design compresses local information into compact tokens and models long-horizon dependencies by attending over this compact set. This design factors a single expensive computation into two cheaper stages, substantially reducing computational cost [13, 14]. Moreover, because futuretimestep computation depends only on a compact set of tokens, PRISM stores this reduced set at test time, thereby reducing the memory footprint. By combining information filtering with a resource-efficient hierarchical architecture, PRISM scales short-term memory to sequences of up to two minutes at 2–3 Hz, an order of magnitude larger than prior approaches [15]. 

To systematically evaluate visuomotor policies with shortterm memory, we introduce **REMEMBENCH** , a benchmark built upon ROBOCASA [16], inspired by short-term memory categories in cognitive science (Figure 1). Existing embodied AI benchmarks [17, 18] either probe memory indirectly or focus narrowly on a single or selective aspects, such as spatial memory [18], making it difficult to assess memory capabilities 


Fig. 1: We propose REMEMBENCH, a benchmark for evaluating visuomotor policies with short-term memory (top), and PRISM, an architecture for visuomotor policies with gated attention and a hierarchical architecture, enabling robots to use short-term memory for partially observable long-horizon tasks (bottom). 

holistically. REMEMBENCH instead spans four categories of short-term memory—spatial, prospective, object-associative, and object-set—across eight visuomotor tasks (section IV). By unifying these categories into a single benchmark, REMEMBENCH encourages the development of general memory mechanisms rather than siloed task-specific solutions. 

On REMEMBENCH, PRISM outperforms a wide range of strong baselines—including recurrent, transformer-based, and specialized policy architectures for short-term memory—by an absolute margin of 5%. Moreover, by augmenting the state with recent observations, PRISM can resolve action ambiguity under visually identical inputs ( _e.g._ , “just grasped” vs. “about to place”), reducing multimodality and improving performance on benchmarks not designed to test memory In particular, it shows an absolute improvement of 11%–12% on ROBOCASA and LIBERO relative to their no-memory variants. Notably, it outperforms strong pretrained models with an absolute improvement of 11% over GR00T-N1-3B [6] finetuned on ROBOCASA, and 15% over OpenVLA [19] finetuned on LIBERO. On REMEMBENCH, its performance scales with memory size: training with longer short-term memory windows (1 _−→_ 512 timesteps) yields progressively higher success rates (from 16% to 42%) without saturation. In a realworld adaptation of a REMEMBENCH task, PRISM improves absolute success by 15% (30% vs. 15%) over prior works, while a policy without memory achieves 0%. Together, these 

results establish PRISM as an effective and scalable approach to visuomotor policies with short-term memory. 

II. RELATED WORK 

_a) Short-Term Memory in Machine Learning:_ Recurrent architectures such as RNNs [27], LSTMs [28], and more recent state-space models like Mamba [29] have been widely used to capture temporal dependencies. Their memory capacity, however, is tied to the parameter count, and information is only indirectly accessible via hidden states, leading to the credit assignment problem in backpropagation through time [30]. Transformers address these limitations by decoupling memory capacity from parameters and enabling direct access to stored representations [8]. Yet, they introduce new challenges: attention scales linearly with context length at test time, visual inputs yield high token costs (often 10<sup>2</sup> per image), and irrelevant tokens can degrade performance [9]. Stability and efficiency have been pursued through attention sinks [31], gated attention [12], hierarchical attention [32], hybrid attention mechanism with global and sliding window [33], attention with segment-level recurrence [34, 35], but these remain largely unexplored in closed-loop visuomotor control. 

_b) Short-Term Memory in Visuomotor Policies:_ In visuomotor policies, short-term memory has traditionally been handled by recurrent policies such as LSTMs [36, 37] In 

|BENCHMARK|DOMAIN<br>E|PISODELENGTH||SHORT-TER<br>|M MEMORY CATEGORIES<br>||
|---|---|---|---|---|---|---|
||||SPATIAL|PROSPECTIVE|OBJECT-ASSOCIATIVE|OBJECT-SET|
|ALFRED [20]|Manipulation|1000|✓|✗|✗|✗|
|Habitat MultiON [21]|Navigation|2500|✓|✗|✗|✗|
|FindingDory [22]|Navigation + manipulation|3500|✓|✓|✗|✗|
|Memory Maze [17]|Navigation|4000|✓|✗|✗|✗|
|Memory Gym [23]|Synthetic gridworlds|-1|✓|✗|✓|✗|
|POPGym [24]|Synthetic games|1024|✓|✗|✓|✓|
|MemoryBench [18]|Manipulation|12|✓|✗|✓|✗|
|Mikasa-Robo [25]|Manipulation|180|✓|✓|✗|✗|
|RoboMME [26]|Manipulation|1300|✓|✗|✓|✓|
|**REMEMBENCH**|Navigation + manipulation|2500|✓|✓|✓|✓|


TABLE I: Comparison of memory-focused embodied AI benchmarks. Rows highlighted in <mark>blue</mark> explicitly require memory by design (i.e., identical observations can correspond to different actions depending on history). Rows in <mark>orange</mark> involve memory implicitly but do not explicitly test for it. REMEMBENCH uniquely covers all short-term categories in visuomotor tasks. 

practice, however, these models often struggle to scale to long-horizon manipulation, where relevant information may be separated by hundreds of timesteps. Recent transformer-based visuomotor policies trained via imitation learning largely discard history, conditioning only on the current frame or a short window [5, 6, 38–40]. Conversely, some methods aggressively compress entire interactions into a few embedding vectors to reduce computation, discarding fine-grained temporal and spatial information [41, 42]. To address this limitation, recent work incorporates specialized memory representations into transformer-based policies, such as the spatial memory in SAM2Act++ [18] or memory constructed by storing selected keyframes using hand-designed rules [43]. Auxiliary objectives provide another route, as in Past-Token Prediction (PTP) [15], which reconstructs past tokens to regularize policies. In contrast, our work explores an alternative: improve memory utilization of the transformer backbone through gated attention and hierarchical architecture, enabling selective retention of information and efficient scaling without external modules or auxiliary losses. 

_c) Memory Benchmarks:_ Several embodied benchmarks involve partial observability, where memory is useful but not isolated. ALFRED [20], Habitat MultiON [21], and FindingDory [22] ask agents to recall object states or past goals, but performance also depends heavily on perception, semantics, and exploration. In contrast, recent work introduces benchmarks that explicitly enforce memory dependence. Memory Maze [17] evaluates spatial recall in procedurally generated mazes. Memory Gym [23] and POPGym [24] provide gridworld and game-based tasks targeting short-term recall. MemoryBench [18] defines manipulation tasks with identical observations yield different actions depending on history, but mainly targets a single spatial memory type where specialized methods already reach near-saturated performance. Mikasa-Robo [25] instead studies learning algorithms with memory for relatively short-horizon manipulation (episodes up to _∼_ 180 steps). In contrast, ReMemBench, with its human teleoperation dataset, is designed to study imitation learning 

under partial observability. It spans both navigation and manipulation with longer-horizon, multi-subtask episodes (up to _∼_ 2.5k steps), organized into four memory categories: spatial, object-set, object-associative, and prospective. More recently, RoboMME [26] offers a manipulation benchmark with diverse tasks and extended horizons, but lacks coverage of prospective memory tasks while including additional tasks involving procedural memory. ReMemBench complements this landscape by targeting four different memory categories across both navigation and manipulation. 

In summary (Table I), REMEMBENCH encompasses shortterm memory of various categories, encouraging unified memory architectures that generalize across tasks. 

## III. **PRISM** : A **<u>P</u>** OLICY A **<u>R</u>** CH **<u>I</u>** TECTURE FOR **<u>S</u>** HORT-TERM **<u>M</u>** EMORY 

_A. Formulation, Background, and Challenges_ 

_a) Problem Formulation:_ We study imitation learning under partial observability, where the robot receives observations _ot_ ( _e.g._ , RGB images and proprioception) and produces actions _at_ in a closed loop. The training dataset _D_ train = _{_ ( _τ_<sup>_i_</sup> _, l_<sup>_i_</sup> ) _}_<sup>_N_</sup> _i_ =1<sup>consistsof</sup><sup>_N_experttrajectories</sup><sup>_τ i_=</sup> _{_ ( _o_<sup>_i_</sup> _t_<sup>_, ai_</sup> _t_<sup>)</sup><sup>_}_</sup> _t_<sup>_T_</sup> =1<sup>_i_,pairedwithatasklanguageinstruction</sup><sup>_li_.We</sup> learn a policy _πθ_ via behavior cloning, conditioning on the interaction history up to time _t_ : 


_b) Training Objective:_ We optimize a behavior cloning loss to match the expert distribution, 


where _pθ_ ( _·_ ) denotes a parametric action distribution. We employ action chunking, predicting the next _l_ future actions at each timestep (not shown above for clarity) [44]. 


Fig. 2: PRISM applies gated attention to filter information retrieved from history and hierarchical summarization to scale attention over long interaction histories, improving causal transformer policies trained with behavior cloning by improving robustness to noisy histories and reducing computation. 

_c) Evaluation:_ During inference, the policy predicts actions autoregressively with language tokens forming a static prefix, while observation and action tokens accumulate over time. Once the horizon budget _n_ is reached, only the most recent _n_ steps are retained in memory. The learned policy is evaluated on its ability to generalize to new object placements. _d) Model Architecture:_ At each timestep _t_ , the policy processes a truncated history 


together with the task description _l_ , where _k_ = max( _t − n,_ 1), _n_ is a fixed memory budget on the number of retained interaction steps. Each observation _ot_ = ( _vt, pt_ ) consists of an image _vt_ and a proprioceptive state _pt_ . Images are encoded into _kv_ visual tokens using an image encoder, proprioceptive states into _kp_ tokens, and past actions into _ka_ tokens via an action encoder. The instruction _l_ is encoded with a pretrained text encoder into _kl_ language tokens. 

All tokens are packed in temporal order with a causal mask, and positional encodings preserve temporal and (for images) spatial structure. The resulting token sequence is 


This sequence is processed by a transformer-based backbone [8]. The transformer maintains the sequence within its context window, which serves as the short-term memory. At each step, the hidden state of the last observation token [ _vt_ ] _kv_ is passed through an action head to produce the parameters of _pθ_ ( _at | ·_ ). 

_e) Challenges:_ Attending to long histories is crucial for tasks that require memory but raises two key challenges. First, long histories often include irrelevant information that 

induces spurious correlations during training. Second, naively attending to all past tokens leads to prohibitive memory and computation costs during both training and evaluation. 

## _B. Selecting Relevant Features_ 

Transformers retain a history of inputs in their context window, effectively forming the short-term memory of a policy. However, long input histories can also introduce irrelevant information, leading models to learn spurious correlations [10, 11], _e.g._ , associating the positions of past distractor objects with a decision to place an object on the left or right. At test time, such correlations may not hold true, resulting in poor performance. This issue is especially pronounced in behavior cloning, where even a small initial error _ϵ_ can compound over time as _O_ ( _T_<sup>2</sup> _ϵ_ ) for horizon length _T_ [45, 46]. Thus, while memory is essential for long-horizon household tasks, it also introduces noise that makes learning more difficult. 

Transformers with longer context windows are particularly vulnerable to this issue due to the nature of the attention mechanism: the softmax operation distributes normalized weights throughout the history, potentially amplifying the influence of irrelevant tokens [9, 47]. 

To mitigate this, we use a gating mechanism that regulates the information flow after the attention [12]. Specifically, we modulate the output of each attention block using a learnable gate conditioned on the current input features. Conditioning the gate on the input features allows the model to adaptively control which retrieved information to suppress as the interaction progresses. 

Let _x_ denote the input to a transformer block, and let 


Fig. 3: Guided by the cognitive science literature, ReMemBench decomposes short-term memory into several functional categories, such as Spatial, Prospective, Object-Set, and Object-Associative. 

denote the attention output after the softmax-weighted value aggregation but before the output projection _Wo_ . We compute the gated output as: 


where _g_ : R<sup>_d_</sup> _→_ (0 _,_ 1)<sup>_d_</sup> is a gating function, implemented as an MLP with sigmoid activation, and _⊙_ denotes element-wise multiplication. The gated output is first projected using the attention output projection _Wo_ , and then incorporated via the standard residual connection: _y_ = _x_ + _Woz_ ˜, followed by the feed-forward layer (See Figure 2, top-right). 

_C. Reducing Memory and Compute Footprint_ 

Naively attending over all tokens from _n_ timesteps in history, each with _kv_ visual tokens, _kp_ proprioceptive tokens, and _ka_ action tokens, incurs a quadratic compute and memory cost during training: 


Similarly, during evaluation, it incurs a linear cost per step, _O_ ( _nk_ tot), assuming key-value caching. However, as the context grows, the compute and memory costs can become prohibitive. 

To improve scalability, we propose a hierarchical architecture that first splits the sequence into a local encoding of memory, then aggregates the compressed outputs using a global memory encoder. This approach avoids processing the entire token set at once and splits the computation into two parts [14]. If each local window compresses _k_ tot tokens down 

to _k_ tot _/m_ , then the total compute and memory cost during training becomes: 


which is approximately _m_<sup>2</sup> _×_ cheaper than original _O_ (( _nk_ tot)<sup>2</sup> ) when _m ≪ nk_ tot. Similarly, during evaluation, the hierarchical architecture yields a factor- _m_ gain in memory and compute: attention is computed over only _nk_ tot _/m_ tokens instead of _nk_ tot, and the number of cached key-value tokens is likewise reduced by _m_ . 

Concretely, at each step, a _local memory encoder_ first processes the current timestep’s sensory information using a transformer block, then uses a perceiver-style resampler [48] to compress _k_ tot _→ k_ tot _/m_ (Figure 2, bottom-right). A _global memory encoder_ then computes attention over the concatenated compressed tokens across time (Figure 2, top-right). The resulting token with global information is _broadcasted_ back to the original _k_ tot tokens and fused with the original inputs via a residual skip to the local memory encoder. The skip connection in PRISM helps preserve per-token individuality while injecting global information. 

_a) Summary.:_ PRISM combines (i) gated attention, which adaptively filters irrelevant information from memory, and (ii) a hierarchical architecture, which reduces the compute and memory costs of incorporating long histories. Together, they improve robustness to spurious correlations while allowing the policy to efficiently scale memory to longer horizons. Both components integrate seamlessly with a transformer 

policy trained using a standard behavior cloning objective; no auxiliary losses or extra supervision are required. 

## IV. REMEMBENCH: A BENCHMARK FOR SHORT-TERM MEMORY IN VISUOMOTOR POLICIES 

REMEMBENCH is designed to evaluate short-term memory in visuomotor policies. Guided by the cognitive science literature, we decompose short-term memory into several functional categories (Figure 3). Diversity across categories promotes general memory mechanisms rather than task-specific, nongeneralizable solutions. Each category is instantiated with two household manipulation tasks. All tasks ensure that immediate sensory inputs are insufficient and success requires withinepisode recall. 

**Spatial Memory.** The ability to recall object locations [51]. We created the following tasks, taking inspiration from the “Belongings: Delayed Recall” subtest of the Rivermead Behavioral Memory Test [52]: 

- _Retrieve Fruit:_ A fruit is placed somewhere in the kitchen and is out of view from a neutral start. The robot must remember its location, fetch it, and place it in the sink. Fruit type and object placement differ across trials. 

- _Retrieve Oil:_ Several household items are arranged and not visible from the start. The robot must find the specified oil bottle and pick it up. The bottle instance and placement vary across trials. 

**Prospective Memory.** The ability to retain intentions over a delay and execute them at the right time [53]. We consider the following tasks, inspired by the Prospective-Retrospective Memory Questionnaire [54]: 

- _Cook Meat:_ A pan with meat sits on the stove. The robot turns the stove on, waits the required duration, then turns it off. Target duration, pan, and meat type vary across trials. 

- _Cook Meat and Vegetable:_ Meat begins on the stove, and a vegetable is nearby. The robot must turn the stove on, add the vegetable after a specified duration, and turn the stove off after another specified duration so both items meet their cooking times. Durations, pan type, ingredient types, and vegetable location vary across trials. 

**Object-Associative Memory.** The ability to recall objectlocation associations [55]. We propose the following, inspired by the Paired Associates Learning test [56]: 

- _Wash and Return to Container:_ Two saucers sit to the left and right of the sink; one holds a fruit. The robot must wash the fruit and return it to the _same_ saucer. Fruit and saucer types, and saucer sides vary across trials. 

- _Wash and Return to Original Spot:_ A fruit starts on the countertop. The robot moves it to the sink to wash it, then returns it to its original spot (within a small window). Initial positions and fruit type vary across trials. 

**Object-Set Memory.** The ability to maintain and update sets of multiple objects across time [57, 58]. We consider the following tasks, inspired by object set maintenance paradigms in working memory, particularly the Counting Span task [59]: 

- _Microwave Breadsticks:_ A plate holds multiple breadsticks, and the microwave is initially out of view. The robot must 

move all breadsticks into the microwave, close the door, and keep track of how many remain. Counts, bread types, and object positions vary across trials. 

- _Relocate Bowls:_ Bowls with distractor plates nearby sit beside a cabinet. The robot must transfer all and only the bowls into the cabinet while tracking the remaining count. Bowl types, counts, and object positions vary across trials. REMEMBENCH builds on assets from the ROBOCASA 

- environment [16], with each task provided with 50 expert teleoperated demonstrations for training. 

## V. EXPERIMENTS 

**Baselines.** We group our baselines into four categories according to their memory mechanisms and application domains and evaluate them on REMEMBENCH. **Recurrent baselines** include LSTM [49] and Mamba [29], which compress history into hidden states. **Segment-level recurrent transformers** include Transformer-XL (TrXL) [34] and Gated TransformerXL (GTrXL) [35], which combine recurrence with attention. We also include **transformer-variants** such as linear-attention transformer [50], which replaces softmax with a linear kernel to obtain long-context attention with reduced compute and memory. Finally, under **visuomotor policy architectures** for imitation under partial observability, we consider Past Token Prediction (PTP) [15], which adds an auxiliary loss to predict past actions, Scene Memory Transformer (SMT) [41], which compresses entire trajectories into single token via attention pooling, and SAM2Act++ [18] that creates a compact state representation by storing the pixel co-ordinates of objects observed in the past along with the current observation. 

Our evaluations answer the following research questions. 

**Q1. How does PRISM compare to prior works on imitation learning with partial observability?** REMEMBENCH _Results._ Recurrent models such as LSTM and Mamba compress the entire history into a limited capacity hidden state and struggles with assigning credits to the correct timestep using backpropagation through time, _e.g._ , in a “turn off the stove after a delay” task, the learning signal from the decision should backpropagate through hundreds–thousands of updates, so gradients vanish [30]. Consequently, LSTM and Mamba achieve only 12% and 25% success versus PRISM’s 41% (absolute drop of 29 and 16 points, resp.) (Table II). Segmentlevel recurrent transformers like TrXL and GTrXL still rely on recurrence, so long-horizon credit assignment remains challenging, yielding 15% and 26% (absolute drop of 26 and 15 points, resp.). Linear-Attention effectively compresses the entire history into a single matrix; this representation likely suffers from forgetting over long horizons and reaches only 22% (an absolute 19-point drop) [60]. 

Prior standard attention-based methods also struggle to regulate the retrieved information. PTP improves recall via an auxiliary loss but does not filter irrelevant information, leading to only 28% success ( _−_ 14 points). Scene-level memory models like SMT compress entire trajectories into a pooled embedding, discarding fine-grained temporal information, reaching 36% ( _−_ 5 points). In contrast, PRISM preserves 

TABLE II: Success rates on REMEMBENCH task categories (20 trials × 3 seeds). The four tasks are _Retrieve Fruit_ , _Cook Meat_ , _Wash and Return to Container_ , and _Microwave Breadsticks_ (see section IV). 

|BLE II: Success <br>our tasks are _Retrie_<br>_readsticks_ (see sect|rates on REME<br>_ve Fruit_, _Cook M_<br>ion IV).|BENC<br>_eat_, _Wa_|tas cate<br>_sh and Retu_|ores (20 <br>_rn to Cont_|ras × <br>_ainer_, an|seeds). Te<br>d _Microwave_|0.4<br>0.5<br>te|R|eMem|Benc|~~0.42~~<br>(PRISM)<br>h|
|---|---|---|---|---|---|---|---|---|---|---|---|
|Group|Method|Spatial|Prospective|Obj-Assoc.|Obj-Set|Avg|0.3<br>Ra|||||
|REMEMBENCH|LSTM [49]|0_._14|0_._06|0_._15|0_._11|0_._12_±_0_._04|ess||0.26|0.29||
||Mamba [29]|0_._21|0_._52|0_._15|0_._14|0_._25_±_0_._03|0.2<br>cc|||||
||TrXL [34]|0_._06|0_._28|0_._12|0_._12|0_._15_±_0_._03|Su|||||
||GTrXL [35]|0_._23|0_._38|0_._23|0_._21|0_._26_±_0_._03|0.1<br>|~~0.13~~||||
||Linear-Attn. [50]|0_._19|0_._30|0_._22|0_._16|0_._22_±_0_._03|00|||||
|(Four Tasks)|PTP [15]|0_._28|0_._58|0_._16|0_._12|0_._28_±_0_._05|.|Attention|No|Blind|Feature|
||SAM2Act++ [18]|0_._28|0_._08|0_._28|0_._24|0_._22_±_0_._03||Sinks<br>|Gating|Gating|Gating|
||SMT [41]|0_._41|0_._40|0_._30|0_._33|0_._36_±_0_._02<br>|i4|C|i|ih|li|
||PRISM|0_._28|0_._77|0_._33|0_._25|0_._41_±_0_._04<br><br>|g. :<br>h|ompa<br>i|son <br>h|wt <br>|ternatve<br>df|
|||||||<br>|meca|nsms to|te pr|opos|eature-|
|REMEMBENCH(ALL)|PRISM|0_._39|0_._43|0_._22|0_._25|0_._32_±_0_._08<br><br>|wise g|ating in|PRISM|.||


token-level features and combines attention with feature-wise gating to retrieve information while suppressing irrelevant information. Lastly, SAM2Act++ stores object spatial coordinates in memory. However, due to the lack of semantic information, this variant achieves only 22% success ( _−_ 19 points) in REMEMBENCH. This gap underscores the need to develop a general mechanism and architecture for short-term memory in visuomotor policies, rather than relying on taskspecific design choices. 

_Real-World Results._ We evaluate PRISM on a real-world 


Fig. 5: (Left) Successful real-world rollout of PRISM on _Wash and Return to Container_ . (Right) Without memory, the policy cannot disambiguate ‘just picked up’ vs. ‘about to place.’ 

adaptation of the ‘Wash and Return to Container’ task from REMEMBENCH (Figure 5). Without access to memory, the baseline policy fails completely (0%). The transformer-based PTP baseline achieves a 15% success, while PRISM reaches 30%. This substantial improvement demonstrates PRISM’s transfer to real-world tasks, where temporally extended shortterm memory is important. 

**<mark>Q2. How much improvem</mark> e** **<mark>nt does PRISM</mark> provide on standard benchmarks that do not explicitly test memory?** Augmenting the state with recent observations provides information absent from the current observation. This disambiguates visually identical inputs that require different actions ( _e.g._ , “just grasped” vs. “about to place”), reducing multimodality in the state-conditioned action distribution. 

Empirically, we evaluate PRISM on two visuomotor benchmarks, ROBOCASA and LIBERO. On ROBOCASA, PRISM with memory improves over its no-memory variant by an absolute 11 points (32% _→_ 43%) and also exceeds GR00TN1-2B finetuned on ROBOCASA by 11 points (Table III). On LIBERO, PRISM improves similarly over its no-memory counterpart by 12 points, averaged over all benchmarks, and pretrained OpenVLA finetuned on LIBERO by 15 points (Table III). These results indicate that adding short-term memory using PRISM improves both memory-dependent and seemingly memory-less tasks by adding information, making the conditional action distribution less multimodal. 


Fig. 6: **(** **_Top_ ) Mean predicted gating value across timesteps during decision-making.** Higher values align with intuitive task moments, especially when turning the stove on and off, where memory recall is most important for disambiguation. This trend is consistent across successful “Cook Meat” trials. **(** **_Bottom_ ) Qualitative visualization of the gating effect.** With gating, the policy pays attention to the correct observations and the spatial region where the orange was previously observed from memory. Without gating, attention shifts to taskirrelevant regions, such as the sink. 

**Q3. How does PRISM’s performance scale with increasing memory capacity?** PRISM exhibits strong scalability with increasing memory size on REMEMBENCH (Figure 7, Right). As the memory window expands from _n_ = 1 to _n_ = 512, the success rate increases by 0 _._ 26, indicating that PRISM continues to extract useful information from temporally extended memory without saturation. This trend highlights PRISM’s suitability for tasks that demand reasoning over extended temporal information. 

**Q4. Is gated attention effective for filtering irrelevant information in visuomotor policies?** The gating mechanism in PRISM is crucial for selectively controlling information retrieved from memory; removing it leads to a 16-point 

|Method|Success Rate|Method|LIBERO-90|LIBERO-10|Object|Spatial|Goal|Avg.|
|---|---|---|---|---|---|---|---|---|
|GR00T-N1-2B|0.32|OpenVLA|0.62|0.54|0.88|0.85|0.79|0.74|
|Diffusion Policy|0.26|Diffusion Policy|–|0.72|**0.93**|0.78|0.68|–|
|PRISM (no memory)|0.32|PRISM (no memory)|0.77|0.75|0.89|0.85|0.61|0.77|
|PRISM (_n_= 256)|**0.43**|PRISM (_n_= 256)|**0.85**|**0.81**|**0.93**|**0.92**|**0.95**|**0.89**|


TABLE III: Success rates on ROBOCASA (Left) and LIBERO (Right). PRISM with memory ( _n_ = 256) outperforms its nomemory variant and strong pretrained baselines finetuned on ROBOCASA and LIBERO. Baseline numbers are adopted from prior works [6, 19, 61]. 


Fig. 7: (Left) PRISM is both computationally and memory efficient at handling long contexts. (Right) PRISM demonstrates strong scalability as memory size increases on REMEMBENCH tasks. 

performance drop, underscoring the need to filter irrelevant information (Figure 4, right). We also evaluate a variant that uses a per-layer scalar gate while ignoring per-step input features. Although this offers a modest gain over no gating (3-points), it performs significantly worse than PRISM’s input feature-aware gating (29% vs. 42%). Furthermore, we test adding attention sink tokens instead of gating, which allows the model to attend to a dummy token rather than irrelevant information from memory [31]. While successful in language models [62], attention sinks prove ineffective, highlighting the need for further investigation into different memory filtering mechanisms in visuomotor policies. See Figure 6 (bottom) for a qualitative example. 

**Q5. How much computational and memory efficiency is gained from the hierarchical architecture?** PRISM scales efficiently over long temporal sequences by compressing local information before global attention, allowing global operations to run on a compact set of summary tokens rather than the full sequence. Moreover, it only needs to cache the summary tokens, rather than all the tokens. At _n_ = 512, this yields 0 _._ 20 _×_ peak GPU memory ( _−_ 80%) and 0 _._ 60 _×_ runtime ( _−_ 40%) relative to both full attention and hybrids with global attention + sliding window attention [33] (Figure 7, left). We observe an increase in the hybrid method’s runtime performance at _n_ = 4, likely due to CUDA kernel scheduling rather than algorithmic effects. 

## VI. LIMITATIONS AND CONCLUSION 

**Benchmark headroom.** Absolute success rates on REMEMBENCH cluster around the 30% range. We view this not as 

a weakness of memory, but as evidence that long-horizon tasks are challenging. Improving overall performance is essential to demonstrate the benefits of history and to encourage improvements across components ( _e.g._ , perception, control, memory), rather than any single module. **Short vs. longterm memory.** In this work, we focus on _short-term_ memory: retaining a recent window of sensory–motor history (on the order of minutes) for action prediction [3]. Looking ahead, we envision adding a persistent _long-term_ memory that accumulates information over days, or the system’s lifetime and retrieves relevant traces into short-term memory when needed for decision-making. **Internet-scale priors.** Learning to _use_ short-term memory effectively can require large amounts of data. Our study operates at a much smaller scale. An exciting direction is to pretrain memory modules on internet-scale video and study how these priors transfer to visuomotor control. 

In conclusion, we introduce PRISM, a visuomotor policy architecture that incorporates short-term memory through gated attention and a hierarchical design. To systematically evaluate memory in visuomotor control, we propose REMEMBENCH with eight tasks spanning different categories: spatial, prospective, object-associative, and object-set. PRISM outperforms state-of-the-art baselines across (1) all REMEMBENCH tasks, (2) ROBOCASA atomic tasks not explicitly designed to test memory, and (3) real-world evaluations. Its performance also scales with memory capacity, with longer histories yielding consistent gains. Together, PRISM and REMEMBENCH provide a foundation for developing and evaluating memoryaugmented visuomotor policies for long-horizon tasks. 

## VII. ACKNOWLEDGEMENTS 

We thank Priya Sundaresan, Albert Yu, Zhenyu Jiang, Huihan Liu, Max Rudolph, Siddhant Agarwal, and anonymous reviewers at the Robotics and AI Institute (RAI) for their helpful feedback on the manuscript. We are also grateful to the Foundation Models and CAPTURE teams at RAI for providing resources and engaging discussions. We thank the teams at RAI and the Texas Advanced Computing Center (TACC) at The University of Texas at Austin for their invaluable support with computing resources. This work was partially supported by the National Science Foundation (FRR-2145283, EFRI-2318065), the Office of Naval Research (N00014-22-12204, N00014-24-1-2550), and the DARPA TIAMAT program (HR0011-24-9-0428). Finally, we note that this work was primarily conducted during the summer internships of Rutav Shah and Rajat Kumar Jenamani at Robotics and AI Institute. 

## REFERENCES 

- [1] L. R. Squire, “Memory systems of the brain: a brief history and current perspective,” _Neurobiology of learning and memory_ , vol. 82, no. 3, pp. 171–177, 2004. 

- [2] J. R. Anderson _et al._ , _Cognitive psychology and its implications_ . Worth Publishers,, 2015. 

- [3] R. C. Atkinson and R. M. Shiffrin, “Human memory: A proposed system and its control processes,” in _Psychology of learning and motivation_ . Elsevier, 1968, vol. 2, pp. 89–195. 

- [4] A. Baddeley, “Working memory,” _Memory_ , pp. 71–111, 2020. 

- [5] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “pi0: A vision-language-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [6] J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang _et al._ , “Gr00t n1: An open foundation model for generalist humanoid robots,” _arXiv preprint arXiv:2503.14734_ , 2025. 

- [7] M. Shukor, D. Aubakirova, F. Capuano, P. Kooijmans, S. Palma, A. Zouitine, M. Aractingi, C. Pascal, M. Russi, A. Marafioti _et al._ , “Smolvla: A vision-language-action model for affordable and efficient robotics,” _arXiv preprint arXiv:2506.01844_ , 2025. 

- [8] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin, “Attention is all you need,” _Advances in neural information processing systems_ , vol. 30, 2017. 

- [9] K. Hong, A. Troynikov, and J. Huber, “Context rot: How increasing input tokens impacts llm performance,” Chroma, Tech. Rep., July 2025. [Online]. Available: https://research.trychroma.com/context-rot 

- [10] P. De Haan, D. Jayaraman, and S. Levine, “Causal confusion in imitation learning,” _Advances in neural information processing systems_ , vol. 32, 2019. 

- [11] C. Wen, J. Lin, T. Darrell, D. Jayaraman, and Y. Gao, “Fighting copycat agents in behavioral cloning from 

observation histories,” _Advances in Neural Information Processing Systems_ , vol. 33, pp. 2564–2575, 2020. 

- [12] Z. Qiu, Z. Wang, B. Zheng, Z. Huang, K. Wen, S. Yang, R. Men, L. Yu, F. Huang, S. Huang _et al._ , “Gated attention for large language models: Nonlinearity, sparsity, and attention-sink-free,” _arXiv preprint arXiv:2505.06708_ , 2025. 

- [13] G. Bertasius, H. Wang, and L. Torresani, “Is space-time attention all you need for video understanding?” in _Icml_ , vol. 2, no. 3, 2021, p. 4. 

- [14] A. Arnab, M. Dehghani, G. Heigold, C. Sun, M. Luˇci´c, and C. Schmid, “Vivit: A video vision transformer,” 2021. [Online]. Available: https://arxiv.org/abs/2103. 15691 

- [15] M. Torne, A. Tang, Y. Liu, and C. Finn, “Learning long-context diffusion policies via past-token prediction,” _arXiv preprint arXiv:2505.09561_ , 2025. 

- [16] S. Nasiriany, A. Maddukuri, L. Zhang, A. Parikh, A. Lo, A. Joshi, A. Mandlekar, and Y. Zhu, “Robocasa: Largescale simulation of everyday tasks for generalist robots,” _arXiv preprint arXiv:2406.02523_ , 2024. 

- [17] J. Pasukonis, T. Lillicrap, and D. Hafner, “Evaluating long-term memory in 3d mazes,” _arXiv preprint arXiv:2210.13383_ , 2022. 

- [18] H. Fang, M. Grotz, W. Pumacay, Y. R. Wang, D. Fox, R. Krishna, and J. Duan, “Sam2act: Integrating visual foundation model with a memory architecture for robotic manipulation,” _arXiv preprint arXiv:2501.18564_ , 2025. 

- [19] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi _et al._ , “Openvla: An open-source vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 

- [20] M. Shridhar, J. Thomason, D. Gordon, Y. Bisk, W. Han, R. Mottaghi, L. Zettlemoyer, and D. Fox, “Alfred: A benchmark for interpreting grounded instructions for everyday tasks,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2020, pp. 10 740–10 749. 

- [21] S. Wani, S. Patel, U. Jain, A. Chang, and M. Savva, “Multion: Benchmarking semantic map memory using multi-object navigation,” _Advances in Neural Information Processing Systems_ , vol. 33, pp. 9700–9712, 2020. 

- [22] K. Yadav, Y. Ali, G. Gupta, Y. Gal, and Z. Kira, “Findingdory: A benchmark to evaluate memory in embodied agents,” _arXiv preprint arXiv:2506.15635_ , 2025. 

- [23] M. Pleines, M. Pallasch, F. Zimmer, and M. Preuss, “Memory gym: Partially observable challenges to memory-based agents,” in _The eleventh international conference on learning representations_ , 2023. 

- [24] S. Morad, R. Kortvelesy, M. Bettini, S. Liwicki, and A. Prorok, “POPGym: Benchmarking partially observable reinforcement learning,” in _The Eleventh International Conference on Learning Representations_ , 2023. [Online]. Available: https://openreview.net/forum? id=chDrutUTs0K 

- [25] E. Cherepanov, N. Kachaev, A. K. Kovalev, and A. I. 

Panov, “Memory, benchmark & robots: A benchmark for solving complex tasks with reinforcement learning,” 2025. [Online]. Available: https://arxiv.org/abs/2502. 10550 

- [26] Y. Dai, H. Fu, J. Lee, Y. Liu, H. Zhang, J. Yang, C. Finn, N. Fazeli, and J. Chai, “Robomme: Benchmarking and understanding memory for robotic generalist policies,” _arXiv preprint arXiv:2603.04639_ , 2026. 

- [27] J. L. Elman, “Finding structure in time,” _Cognitive science_ , vol. 14, no. 2, pp. 179–211, 1990. 

- [28] S. Hochreiter and J. Schmidhuber, “Long short-term memory,” _Neural computation_ , vol. 9, no. 8, pp. 1735– 1780, 1997. 

- [29] A. Gu and T. Dao, “Mamba: Linear-time sequence modeling with selective state spaces,” _arXiv preprint arXiv:2312.00752_ , 2023. 

- [30] Y. Bengio and P. Frasconi, “Credit assignment through time: Alternatives to backpropagation,” _Advances in neural information processing systems_ , vol. 6, 1993. 

- [31] G. Xiao, Y. Tian, B. Chen, S. Han, and M. Lewis, “Efficient streaming language models with attention sinks,” _arXiv preprint arXiv:2309.17453_ , 2023. 

- [32] Z. Yang, D. Yang, C. Dyer, X. He, A. Smola, and E. Hovy, “Hierarchical attention networks for document classification,” in _Proceedings of the 2016 conference of the North American chapter of the association for computational linguistics: human language technologies_ , 2016, pp. 1480–1489. 

- [33] I. Beltagy, M. E. Peters, and A. Cohan, “Longformer: The long-document transformer,” _arXiv preprint arXiv:2004.05150_ , 2020. 

- [34] Z. Dai, Z. Yang, Y. Yang, J. Carbonell, Q. V. Le, and R. Salakhutdinov, “Transformer-xl: Attentive language models beyond a fixed-length context,” 2019. [Online]. Available: https://arxiv.org/abs/1901.02860 

- [35] E. Parisotto, H. F. Song, J. W. Rae, R. Pascanu, C. Gulcehre, S. M. Jayakumar, M. Jaderberg, R. L. Kaufman, A. Clark, S. Noury, M. M. Botvinick, N. Heess, and R. Hadsell, “Stabilizing transformers for reinforcement learning,” 2019. [Online]. Available: https://arxiv.org/abs/1910.06764 

- [36] P. Abolghasemi, A. Mazaheri, M. Shah, and L. B¨ol¨oni, “Pay attention! - robustifying a deep visuomotor policy through task-focused visual attention,” in _2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2019, pp. 4249–4257. 

- [37] A. Mandlekar, D. Xu, J. Wong, S. Nasiriany, C. Wang, R. Kulkarni, L. Fei-Fei, S. Savarese, Y. Zhu, and R. Mart´ın-Mart´ın, “What matters in learning from offline human demonstrations for robot manipulation,” 2021. [Online]. Available: https://arxiv.org/abs/2108.03298 

- [38] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” _The International Journal of Robotics Research_ , p. 02783649241273668, 2023. 

- [39] R. Zheng, Y. Liang, S. Huang, J. Gao, H. Daum´e III, A. Kolobov, F. Huang, and J. Yang, “Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies,” _arXiv preprint arXiv:2412.10345_ , 2024. 

- [40] G. R. Team, S. Abeyruwan, J. Ainslie, J.-B. Alayrac, M. G. Arenas, T. Armstrong, A. Balakrishna, R. Baruch, M. Bauza, M. Blokzijl _et al._ , “Gemini robotics: Bringing ai into the physical world,” _arXiv preprint arXiv:2503.20020_ , 2025. 

- [41] K. Fang, A. Toshev, L. Fei-Fei, and S. Savarese, “Scene memory transformer for embodied agents in long-horizon tasks,” 2019. [Online]. Available: https://arxiv.org/abs/1903.03878 

- [42] H. Shi, B. Xie, Y. Liu, L. Sun, F. Liu, T. Wang, E. Zhou, H. Fan, X. Zhang, and G. Huang, “Memoryvla: Perceptual-cognitive memory in vision-languageaction models for robotic manipulation,” _arXiv preprint arXiv:2508.19236_ , 2025. 

- [43] A. Sridhar, J. Pan, S. Sharma, and C. Finn, “Memer: Scaling up memory for robot control via experience retrieval,” _arXiv preprint arXiv:2510.20328_ , 2025. 

- [44] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” _arXiv preprint arXiv:2304.13705_ , 2023. 

- [45] S. Ross, G. Gordon, and D. Bagnell, “A reduction of imitation learning and structured prediction to no-regret online learning,” in _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ . JMLR Workshop and Conference Proceedings, 2011, pp. 627–635. 

- [46] J. Spencer, S. Choudhury, A. Venkatraman, B. Ziebart, and J. A. Bagnell, “Feedback in imitation learning: The three regimes of covariate shift,” _arXiv preprint arXiv:2102.02872_ , 2021. 

- [47] B. Peters, V. Niculae, and A. F. Martins, “Sparse sequence-to-sequence models,” in _Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics_ , 2019, pp. 1504–1519. 

- [48] A. Jaegle, F. Gimeno, A. Brock, O. Vinyals, A. Zisserman, and J. Carreira, “Perceiver: General perception with iterative attention,” in _International conference on machine learning_ . PMLR, 2021, pp. 4651–4664. 

- [49] C. B. Vennerød, A. Kjærran, and E. S. Bugge, “Long short-term memory rnn,” _arXiv preprint arXiv:2105.06756_ , 2021. 

- [50] A. Katharopoulos, A. Vyas, N. Pappas, and F. Fleuret, “Transformers are rnns: Fast autoregressive transformers with linear attention,” 2020. [Online]. Available: https: //arxiv.org/abs/2006.16236 

- [51] J. O’keefe and L. Nadel, _The hippocampus as a cognitive map_ . Oxford university press, 1978. 

- [52] B. A. Wilson, J. Cockburn, and A. D. Baddeley, _Rivermead Behavioural Memory Test_ . London: Thames Valley Test Company, 1985. 

- [53] G. O. Einstein and M. A. McDaniel, “Normal aging and 

prospective memory.” _Journal of Experimental Psychology: Learning, memory, and cognition_ , vol. 16, no. 4, p. 717, 1990. 

- [54] G. Smith, S. Del Sala, R. H. Logie, and E. A. Maylor, “Prospective and retrospective memory in normal ageing and dementia: A questionnaire study,” _Memory_ , vol. 8, no. 5, pp. 311–321, 2000. 

- [55] A. Mayes, D. Montaldi, and E. Migo, “Associative memory and the medial temporal lobes,” _Trends in cognitive sciences_ , vol. 11, no. 3, pp. 126–135, 2007. 

- [56] B. J. Sahakian, R. G. Morris, J. L. Evenden, A. Heald, R. Levy, M. Philpot, and T. W. Robbins, “A comparative study of visuospatial memory and learning in alzheimertype dementia and parkinson’s disease,” _Brain_ , vol. 111, no. 3, pp. 695–718, 1988. 

- [57] S. J. Luck and E. K. Vogel, “The capacity of visual working memory for features and conjunctions,” _Nature_ , vol. 390, no. 6657, pp. 279–281, 1997. 

- [58] T. Makovski and Y. V. Jiang, “The role of visual working memory in attentive tracking of unique objects.” _Journal of Experimental Psychology: Human Perception and Performance_ , vol. 35, no. 6, p. 1687, 2009. 

- [59] R. Case, D. M. Kurland, and J. Goldberg, “Operational efficiency and the growth of short-term memory span,” _Journal of experimental child psychology_ , vol. 33, no. 3, pp. 386–404, 1982. 

- [60] M. He and P. N. Garner, “Alleviating forgetfulness of linear attention by hybrid sparse attention and contextualized learnable token eviction,” 2025. [Online]. Available: https://arxiv.org/abs/2510.20787 

- [61] S. Belkhale and D. Sadigh, “Minivla: A better vla with a smaller footprint,” 2024. [Online]. Available: https://github.com/Stanford-ILIAD/openvla-mini 

- [62] OpenAI, “Introducing gpt-oss,” https://openai.com/index/ introducing-gpt-oss/, Aug. 2025, accessed: 2025-09-18. 

- [63] L. Fu, L. Lian, R. Wang, B. Shi, X. Wang, A. Yala, T. Darrell, A. A. Efros, and K. Goldberg, “Rethinking patch dependence for masked autoencoders,” _arXiv preprint arXiv:2401.14391_ , 2024. 

## VIII. APPENDIX 

## IX. EFFECT OF ATTENTION SCALE FACTOR (SHARPNESS) 

We study the effect of shaping the attention distribution affects performance by scaling the attention logits. Making attention too flat (factor = 0 _._ 125) severely hurts success (0 _._ 22 vs. 0 _._ 64, a _∼_ 42% drop), indicating that overly permissive information flow leads to noisy retrieval. In contrast, moderate increases in sharpness around the PRISM setting (factors 2 _._ 0–8 _._ 0) cause mild degradation (2–10 pp), suggesting that performance is much more sensitive to insufficient selectivity than to conservative selection. Overall, these results indicate that controlling information flow is crucial for performance, a function implemented by PRISM’s gating module and learned directly from data (Table IV). 

## X. EFFECT OF ATTENTION DROPPING 

We also examine whether adding noise to attention can improve robustness. We inject noise by randomly dropping tokens with probability _p_ = 0 _._ 1 [7]. This boosts PRISM’s average success by +4% (0 _._ 45 _→_ 0 _._ 49). Applying the same token-drop strategy to PRISM without gating also helps (0 _._ 26 _→_ 0 _._ 39), but the full PRISM architecture remains stronger overall: it outperforms the no-gating variant by +10% with attention dropping (0 _._ 49 vs. 0 _._ 39) and +19% without it (0 _._ 45 vs. 0 _._ 26). These results suggest that noisy attention alone is helpful but insufficient, and that the learned gating module remains crucial for suppressing irrelevant features from retrieval (Table V). 

## XI. EFFECT OF GATING MODULE 

We acknowledge that modifications introduced by _g_ ( _x_ ), such as additional parameters or non-linearities, could confound the claim that performance gains stem from filtering irrelevant information. To isolate the effect of feature-wise gating from these factors, we compare blind gating (86M parameters, sigmoid non-linearity) with feature-wise gating (90M parameters, sigmoid non-linearity). Blind gating, instead of producing a per-feature gate, learns a single scalar gate per layer and thus matches PRISM in non-linearity while maintaining a similar parameter count (less than 5% extra). The resulting performance gap is substantial: feature-wise gating yields a +17% improvement in average success, indicating that the gains primarily arise from feature-wise information selection rather than increased capacity or any non-linearity (Table VI). 

## XII. EVALUATION ON MIKASA-ROBO 

We also evaluate PRISM on Mikasa-Robo and observe gains on some tasks (e.g., InterceptSlow-v0, RememColor5-v0), but overall performance is comparable to LSTM baselines, unlike on REMEMBENCH, where transformers clearly outperform LSTMs. We hypothesize this gap stems from differences in task design: Mikasa-Robo tasks have much shorter horizons (180 vs. 2.8k timesteps in REMEMBENCH), contain fewer natural distractors, and concentrate most of the relevant information in the initial frames, making them less diagnostic of 

robust, long-horizon memory mechanisms. These differences in performance invite a systematic study of the factors that strongly influence short-term memory use and downstream performance (Figure 8). 

## XIII. ANALYSIS OF THE COMPRESSION FACTOR ( _m_ ) 

The compression factor _m_ trades off memory capacity and resource usage. In our experiments, we found _m ≈_ 200 (compressing all tokens from the current timestep) to be a practical operating point under a budget of 384 H100 GPU-hours per experiment; for _m ≈_ 2, it was difficult to obtain enough gradient steps to reach reasonable performance. Table VII reports success rates for _m ≈_ 2 _,_ 9 _,_ 80 _,_ and 200. As compression becomes more aggressive (larger _m_ ), we observe a modest but consistent increase in average performance across tasks (from 0 _._ 31 at _m ≈_ 2 to 0 _._ 45 at _m ≈_ 200), even though individual categories do not follow a strictly monotonic trend. In contrast, the efficiency gains are clear: at sequence length 512, _m ≈_ 200 reduces compute by 13% and peak GPU memory by 56% relative to _m ≈_ 2 (Figure 9). 

## XIV. MEMORY AND COMPUTE FOOTPRINT 

_a) Training.:_ Assuming each local encoder compresses _k_ tot tokens to _k_ tot _/m_ , there are _n_ local blocks, each processing _k_ tot tokens. The local self-attention per block costs _O_ ( _m_<sup>2</sup> ) and is invoked _n k_ tot _/m_ times, yielding a total local compute of _O_ ( _n m k_ tot). After compression, the global module attends over _n k_ tot _/m_ summary tokens, incurring _O_ �( _n k_ tot _/m_ )<sup>2�</sup> . Thus, the overall training-time compute decomposes into a linear-in- _k_ tot local term plus a quadratic-in-the-compressedlength global term: 


Training-time _memory_ can also benefit from the reduced global length (lesser activation memory), but these savings are less pronounced in practice because modern optimizations (e.g., FlashAttention tiling/splitting) already reduce activation memory, the major contributor to training-time footprint for long-sequence transformers. 

_b) Evaluation.:_ The same decomposition applies to evaluation compute, but the memory benefit is much clearer. Operating global attention over _n k_ tot _/m_ summary tokens instead of all _n k_ tot tokens reduces both global-attention compute and the key-value (KV) cache by a factor of _≈ m_ . Concretely, at inference, the model only attends to _n k_ tot _/m_ tokens and stores proportionally fewer KV entries, yielding an _≈ m×_ reduction in global-attention runtime and memory relative to full/global attention over the uncompressed sequence. Empirical evaluation-time measurements (compute and memory) are reported in the main paper. 

_V_ = scale <u>factor</u> _·_<sup>_~~<u>√</u>~~_</sup> _d_ head 0.125 0.25 0.5 1.0 (PRISM) 2.0 4.0 8.0 Retrieve Fruit 0.22 0.54 0.54 0.64 0.64 0.54 0.62 

TABLE IV: Effect of attention sharpness on PRISM performance. We scale attention logits by _~~√~~ dV_ head<sup>beforesoftmax;PRISM</sup> uses the default setting 1 _._ 0. 

|Method|Spatial|Prospective|Associative|Object-Set|Average|
|---|---|---|---|---|---|
|PRISM w/o Gating|0.08|0.35|**0.30**|0.30|0.26|
|PRISM w/o Gating (Attn Drop)|0.44|**0.80**|0.10|0.20|0.39|
|PRISM|0.40|**0.80**|0.25|0.35|0.45|
|PRISM (Attn Drop)|**0.60**|0.64|**0.30**|**0.40**|**0.49**|


TABLE V: Effect of noisy attention (token dropping with probability _p_ = 0 _._ 1) on success rates across the four ReMemBench categories. While noise improves both gated and ungated models, PRISM with learned gating remains strongest overall. 

|Method|Spatial|Prospective|Associative|Object-Set|Average|
|---|---|---|---|---|---|
|Blind Gating|0.35|0.30|0.25|0.20|0.28|
|Feature Gating (PRISM)|**0.40**|**0.80**|**0.25**|**0.35**|**0.45**|


TABLE VI: Blind vs. feature-wise gating. Blind gating learns a single scalar gate per layer with similar non-linearity and parameter count, yet feature-wise gating in PRISM achieves substantially higher average success. 

|Compression (_m_)|Spatial|Prospective|Associative|Object-Set|Average|
|---|---|---|---|---|---|
|_m ≈_2|0.30|0.40|**0.28**|0.24|0.31|
|_m ≈_9|**0.40**|0.56|0.24|**0.40**|0.40|
|_m ≈_80|**0.40**|0.60|0.24|**0.40**|0.41|
|_m ≈_200 (PRISM)|**0.40**|**0.80**|0.25|0.35|**0.45**|


TABLE VII: Effect of compression factor _m_ on success rates across ReMemBench tasks. Larger _m_ corresponds to more aggressive compression. 

_c) Baselines:_ To quantify empirical compute and memory savings, we compare PRISM to two baselines: (i) standard full attention over the entire history, and (ii) a hybrid with full global attention plus a sliding window. For each method, we run a unit block 20 times, recording wall-clock time and peak memory. We then normalize these measurements by the number of learnable parameters and report PRISM-to-baseline ratios for both compute time and memory. 

## XV. IMPLEMENTATION DETAILS 

_a)_ PRISM _Architecture Details:_ We set _kp_ =1, _kv_ =198 _×_ 2 (tokens per camera _×_ cameras), and _ka_ =1. In all experiments, the _local_ encoder compresses the ( _kp_ + _kv_ ) tokens to a single summary token; thus the per-step token count changes from ( _kp_ + _kv_ + _ka_ )=398 to (1+ _ka_ )=2, yielding a compression factor _m_ =<sup>_kp_</sup><sup><u>+</u></sup> 1+<sup>_kv_</sup> _k_<sup><u>+</u></sup> _a_<sup>_ka_</sup> =<sup><u>398</u></sup> 2 = 199. We instantiate the Transformer backbone with a standard LLaMA-style implementation. Visual features are extracted using _CrossMAE_ [63] and kept _frozen_ during policy training. The action head is a two-layer MLP. _b) Data Collection:_ For each of the REMEMBENCH tasks, 50 expert demonstrations are collected by a human teleoperator using a spacemouse for imitation learning. Similarly, for the real-world tasks, we collect 100 expert demonstrations using the spacemouse. 

TABLE VIII: Training hyperparameters. 

|**Config**|**Value**|
|---|---|
|Optimizer|AdamW<br>|
|Base learning rate|5_×_10<sup>_−_4</sup>|
|Effective batch size|256|
|Weight decay|0_._01|
|Warmup epochs|2|
|Total epochs|200|
|Action prediction horizon|32|
|Proprioception noise (std)|0_._005|
|Brightness augmentation|Uniform(_−_0_._1_,_ 0_._1)<br>|
|Contrast augmentation|Uniform(0_._8_,_ 1_._2)|
|Number of cameras|2|


_c) Training Details:_ We train for all eight REMEMBENCH tasks using _∼_ 384 H100 GPU-hours, and for four ROBOCASA atomic tasks using _∼_ 192 H100 GPU-hours. 


Fig. 8: Comparison of PRISM vs. LSTM on Mikasa-Robo. 


Fig. 9: Effect of compression factor _m_ on test-time efficiency. The plot reports peak GPU memory and computation time, both normalized with respect to the _m ≈_ 200 (PRISM) configuration, across different sequence lengths. 

