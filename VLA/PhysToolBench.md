---
title: "PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs"
date: "2025-10-10"
authors: "Zixin Zhang; Kanghao Chen; Xingwang Lin; Lutao Jiang; Xu Zheng; Yuanhuiyi Lyu"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2510.09507
pdf: https://arxiv.org/pdf/2510.09507
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2510.09507)** / [論文ページ](https://arxiv.org/abs/2510.09507)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs 

# PHYSTOOLBENCH: BENCHMARKING PHYSICAL TOOL UNDERSTANDING FOR MLLMS 

**Zixin Zhang**<sup>1</sup><sup>_,∗_</sup> **, Kanghao Chen**<sup>1</sup><sup>_,∗_</sup> **, Xingwang Lin**<sup>3</sup> **, Lutao Jiang**<sup>1</sup> **, Xu Zheng**<sup>1</sup> **, Yuanhuiyi Lyu**<sup>1</sup> **, Litao Guo**<sup>1</sup> , **Yinchuan Li**<sup>4</sup> , **Ying-Cong Chen**<sup>1</sup><sup>_,_2</sup><sup>_,†_</sup> 1HKUST(GZ) 2HKUST 3Beihang University 4Knowin 


Figure 1: For an Embodied Agent, using physical tools is crucial in many tasks. The understanding of physical tools significantly impacts the task’s success rate and execution efficiency (Top). PhysToolBench (Bottom) systematically evaluates the understanding of physical tools of multimodal LLMs. The benchmark is designed with three progressive levels of difficulty and employs a Visual Question Answering (VQA) format. Notice that in the actual benchmark, tools in the images are numerically labeled, and images here are for illustrative purposes only. 

### ABSTRACT 

The ability to use, understand, and create tools is a hallmark of human intelligence, enabling sophisticated interaction with the physical world. For any generalpurpose intelligent agent to achieve true versatility, it must also master these fundamental skills. While modern Multimodal Large Language Models (MLLMs) leverage their extensive common knowledge for high-level planning in embodied AI and in downstream Vision-Language-Action (VLA) models, the extent of their true understanding of physical tools remains unquantified. To bridge this gap, we present **PhysToolBench** , the first benchmark dedicated to evaluating the comprehension of physical tools by MLLMs. Our benchmark is structured as a Visual Question Answering (VQA) dataset comprising over 1,000 image-text pairs. It assesses capabilities across three distinct difficulty levels: _1)_ Tool Recognition: Requiring the recognition of a tool’s primary function. _2)_ Tool Understanding: Testing the ability to grasp the underlying principles of a tool’s operation. _3)_ Tool Creation: Challenging the model to fashion a new tool from surrounding objects when conventional options are unavailable. Our comprehensive evaluation of 32 MLLMs—spanning proprietary, open-source, specialized embodied, and backbones in VLAs—reveals a significant deficiency in the tool understanding. Furthermore, we provide an in-depth analysis and propose preliminary solutions. Code and dataset are publicly available at PhysToolBench Repository. 

1 

PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs 

### 1 INTRODUCTION 

_Man is a tool-using animal. Without tools, he is nothing; with tools, he is all._ 

—Thomas Carlyle 

A key factor in humanity’s success throughout natural evolution is the ability to create and utilize a vast array of tools to enhance survival and prosperity. With the advancement of technology, humans continuously reshape the physical world, inventing diverse instruments to extend the boundaries of their capabilities. For an embodied intelligent agent designed to complete physical tasks, the use of tools is a prerequisite for achieving success and efficiency. For instance, as illustrated in Fig. 1 (Top), a robot must use a hammer to drive a nail into a wall—a task it cannot accomplish with its bare manipulators. Arguably, a profound understanding of physical tools is a fundamental precondition for Artificial General Intelligence (AGI). 

Multimodal Large Language Models (MLLMs) (Bai et al., 2025; Hurst et al., 2024; OpenAI, 2025b; Anthropic, 2025; Comanici et al., 2025), which can process inputs from both vision and language modalities, have acquired substantial common-sense knowledge from being trained on massive datasets. They show great promise for evolving into AGI and have been the focus of numerous studies for deployment in robotics. Some studies employ MLLMs as high-level planners (Yuan et al., 2025; Team et al., 2025a; Driess et al., 2023), while others utilize them for low-level control as the backbone of Vision-Language-Action (VLA) models (Black et al., 2024; Kim et al., 2024; Wen et al., 2025; Black et al.). In either case, interaction with the physical world is fundamental, which inevitably involves the use of physical tools. Although some research has demonstrated that MLLMs possess a preliminary understanding of tools (Gao et al., 2025; Tang et al., 2025; Trupin et al., 2025), the true depth of physical tool comprehension remains largely unexplored. 

Based on these considerations, we propose **_PhysToolBench_** , a benchmark for evaluating an agent’s understanding of physical tools. To the best of our knowledge, this is the first benchmark specifically designed for this purpose. To evaluate an agent’s practical capabilities, we designed a Visual Question Answering (VQA) benchmark that simulates a robotic workflow. Presented with a task and an image of objects, the agent must select the appropriate tool(s). As shown in Fig. 1 (Bottom), the benchmark features three difficulty levels to progressively assess the agent’s depth of understanding: **_1) Easy (Recognizing Tools)_** . This fundamental level assesses whether an agent can identify a conventional tool and its primary function. **_2) Medium (Understanding Tools)_** . This intermediate level probes the agent’s comprehension through three distinct challenges: optimal tool selection from functionally similar options, selection of all tools required for a multi-tool task, and assessment of a tool’s operational viability based on its physical state. **_3) Hard (Creating Tools)_** . This advanced level evaluates an agent’s inventive capabilities. Faced with a task and no standard tools, the agent must fashion a solution by repurposing or combining available objects, which requires an understanding of the physical principles underlying the required tool. 

We evaluate the performance of 32 MLLMs on PhysToolBench, spanning four distinct classes: general-purpose proprietary MLLMs, general-purpose open-source MLLMs, MLLMs tailored for embodied AI, and those functioning as backbones in VLAs. The results demonstrate a clear performance ceiling, with even the most advanced proprietary models scoring no higher than 63%, revealing a profound disparity with human proficiency in tool understanding (over 90%). Furthermore, our analysis uncovers several critical weaknesses in current MLLMs: (1) a failure of small MLLMs, including those within VLA models, to exhibit an emergent ability of tool understanding; (2) a long-tail distribution issue in recognizing and understanding a wide array of tools; (3) a tendency to hallucinate tool affordances and their availability; and (4) inadequate visual reasoning skills. We further propose a ”vision-centric reasoning” framework to bolster the visual reasoning of MLLM agents. We hope our work will inspire future research on physical tool understanding. 

### 2 RELATED WORKS 

#### 2.1 MLLM AND ITS APPLICATION IN EMBODIED AI 

Recent years have witnessed remarkable advancements in Multimodal Large Language Models (MLLMs). Building on the significant success of Large Language Models (LLMs), these models effectively process visual information by leveraging modality alignment techniques (Li et al., 

2 

PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs 

2022; Radford et al., 2021). Typically, a visual encoder and a connector are employed to link visual data to the LLM, enabling reasoning at the language level and granting Vision-Language Models (VLMs) sophisticated image comprehension capabilities. To date, numerous impressive MLLMs have emerged, including proprietary models (Hurst et al., 2024; OpenAI, 2025b; Comanici et al., 2025; Anthropic, 2025; xAI, 2025), as well as open-source alternatives (Bai et al., 2025; Zhu et al., 2025; Wang et al., 2025b; Wu et al., 2024; Beyer et al., 2024; Wu et al., 2024; Lu et al., 2025). These models have demonstrated powerful visual understanding across a diverse range of tasks. 

Beyond general-purpose domains, MLLMs are also finding significant applications in embodied intelligence. On one hand, they are being utilized as the high-level ”brain” for task planning in embodied agents, as exemplified by PaLM-E (Driess et al., 2023), RoboBrain (Team et al., 2025a), and Embodied-R1 (Yuan et al., 2025). On the other hand, research has also capitalized on the inherent common-sense knowledge within MLLMs. By adding an action head and fine-tuning on robotic data, they can be transformed into end-to-end Vision-Language-Action (VLA) models capable of directly outputting robot actions. Notable examples of this approach include _π_ 0 (Black et al., 2024), _π_ 0 _._ 5 (Black et al.), and OpenVLA (Kim et al., 2024). 

#### 2.2 PHYSICAL TOOL USE IN EMBODIED AI 

These advancements in foundation models have empowered robots with the ability to perform fundamental tasks when these models are embodied. For instance, embodied models such as _π_ 0, _π_ 0 _._ 5, and OpenVLA can successfully accomplish basic household chores like folding clothes and tidying desktops. However, while these tasks can be efficiently completed using only the robot’s own manipulators, many higher-level, real-world tasks are difficult and even impossible to achieve with robot manipulators alone. Consequently, teaching robots how to use tools to effectively accomplish complex objectives is of critical importance. 

Initial research has begun to explore endowing robots with tool-using capabilities. For example, VLMgineer (Gao et al., 2025) employs a VLM agent to assist robots in crafting simple tools to complete tasks. Similarly, Trupin et al. (2025) leverages vision foundation models to enable tool use during task planning. MimicFunc (Tang et al., 2025) establishes an imitation learning framework that allows robots to learn tool manipulation by observing human demonstration videos. Leveraging the common-sense knowledge inherent in MLLMs, these approaches have demonstrated a rudimentary ability to use physical tools. Nevertheless, the depth of physical tool understanding that their ”brain”—the MLLM—possesses remains largely unexplored. The primary motivation for our work is to clarify this question by creating a benchmark designed specifically to evaluate the understanding of physical tools within Multimodal Large Language Models. 

#### 2.3 RELATED BENCHMARKS 

For Large Language Models (LLMs), a multitude of benchmarks (Wang et al., 2024a; Huang et al., 2023; 2024; Lu et al., 2024a; Ye et al., 2025) have been developed to evaluate their ability to utilize digital tools, such as search engines, translation services, booking systems, etc.. These benchmarks have catalyzed the rapid development of modern LLM Agents, equipping them with the capability to invoke external APIs to accomplish complex tasks. However, a significant gap exists when it comes to physical tools, as there is currently no corresponding benchmark for MLLMs. We argue that such a benchmark is crucial for advancing MLLMs toward becoming true Embodied Agents capable of meaningful interaction with the physical world. 

Among existing benchmarks for MLLMs, A4Bench (Wang et al., 2025a) is the most relevant to our research. It operates in a VQA format, presenting an image of a tool and asking the MLLM to identify its function from a set of multiple-choice options. While this can, to some extent, reflect the MLLM’s understanding of object affordances, we contend that this question-answering format lacks practical applicability. Our work, therefore, aims to establish a more application-oriented evaluation. We provide the MLLM with a specific task requirement and an image containing several tools, compelling it to answer the question based on the observation. This approach more rigorously assesses whether the MLLM can apply genuine knowledge and reasoning to find the optimal tool, rather than merely relying on the rote memorization of tool-function associations. 

3 

PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs 


Figure 2: Statistics of PhysToolBench. (a) is the distribution of the category. (b) is the distribution of the difficulty level. (c) is the word cloud of the task description given to MLLMs. 

### 3 THE PHYSTOOLBENCH 

#### 3.1 OVERVIEW 

PhysToolBenchis a VQA benchmark comprising over 1,000 text-image pairs designed to evaluate an MLLM’s understanding of physical tools. Each pair consists of a text prompt outlining a specific task and a corresponding 1024 _×_ 1024 image displaying several numerically labeled tools and objects. A core design constraint is that the MLLM is explicitly instructed that the items depicted in the image are the only available things, simulating a realistic robotics scenario with limited resources. The MLLM’s objective is to analyze the task and visual information, then output the numerical label(s) of the required tool(s), or ”None” if no suitable tool is available. PhysToolBenchspans four major domains: Daily Life, Industrial, Outdoor Activities, Professional Settings, and three difficulty levels: Easy, Medium, Hard. Detailed statistics are shown in Fig. 2. 

#### 3.2 DESIGN PRINCIPLES 

To progressively evaluate the depth of an MLLM’s understanding, we designed PhysToolBenchwith three distinct difficulty levels: Easy, Medium, and Hard, each demanding a more profound comprehension of tool properties and functionality. 

The **Easy** level assesses fundamental tool recognition. Questions are answerable with basic tool identification and common-sense knowledge. Task prompts are straightforward, and the image always contains a tool whose primary function directly matches the task. For example, to ”cut vegetables,” the image will include a kitchen knife. The **Medium** level requires a deeper understanding of tools, necessitating reasoning based on specific task constraints. This tier is subdivided into three challenges: 1) _M.1. Attribute Understanding_ , requiring comprehension of a tool’s specific attributes (e.g., selecting a cast-iron skillet for its high heat tolerance); 2) _M.2. Tool Combination_ , evaluating the ability to combine tools to unlock new affordances (e.g., inserting batteries into a remote); and 3) _M.3. Availability Understanding_ , testing the recognition of non-functional tools (e.g., identifying a cracked plunger as unusable). The **Hard** level assesses higher-order reasoning and creativity. The model must work backwards from task requirements to innovatively utilize surrounding objects. For instance, if tasked to ”tighten a flat-head screw” without a suitable screwdriver, the MLLM must identify that a coin can serve as a substitute. 

We propose these difficulty levels as a tiered evaluation standard. The ’Easy’ score serves as a prerequisite for basic tool-use planning, ’Medium’ benchmarks potential in complex scenarios, and ’Hard’ presents a forward-looking challenge for AGI research. 

4 

PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs 


Figure 3: MLLM Leaderboard on our PhysToolBench, ranked by overall performance. 

#### 3.3 DATASET COLLECTION PROCESS 

The collection of test samples for PhysToolBenchwas conducted in three phases to ensure quality. **_Phase 1: Conceptualization._** Human experts designed task-scene pairs, consisting of a task requirement and a detailed scene description, meticulously aligning each scenario with our Easy, Medium, and Hard difficulty criteria. **_Phase 2: Image Generation._** Scene descriptions were transformed into visual images primarily using GPT-4o-image (OpenAI, 2025a)(approximately 90%), a process closely supervised by human experts who vetted for quality and realism. For complex objects that the generative model struggled with, we resorted to physical staging and photography(approximately 10%). **_Phase 3: Annotation and Verification._** Experts used a custom software tool to apply numerical labels to objects in each image. The entire dataset then underwent a final, thorough review and revision by a separate team to verify its integrity and ensure reliability. More details are provided in Appendix. A. 

### 4 EXPERIMENTS ON PHYSTOOLBENCH 

#### 4.1 BENCHMARK CANDIDATES 

We conducted a comprehensive evaluation across four distinct categories of state-of-the-art Multimodal Large Language Models (MLLMs), encompassing **_32 models_** in total: **_a) GeneralPurpose Proprietary MLLMs:_** GPT-5 (2025-08-17) (OpenAI, 2025b), o3 (2025-04-16) (OpenAI, 2025c), ChatGPT-4o-latest (2025-01-29) (Hurst et al., 2024), Claude-3-7-Sonnet-thinking (Anthropic, 2025), Gemini-2.5-pro (2025-05-06) (Comanici et al., 2025), Grok-4 (xAI, 2025). **_b) General-Purpose Open-Source MLLMs:_** Qwen-2.5-VL-72B-Instruct (Bai et al., 2025), Qwen-2.5VL-32B-Instruct, Qwen-2.5-VL-7B-Instruct, Qwen-2.5-VL-3B-Instruct, InternVL-3.5-38B (Wang et al., 2025b), InternVL-3.5-30B-A3B, InternVL-3.5-14B, InternVL-3.5-1B, InternVL-3-78B (Zhu et al., 2025), InternVL-3-38B, GLM-4.5V-108B (Team, 2025), Ovis-2-34B (Lu et al., 2024b), Ovis2.5-9B (Lu et al., 2025), DeepSeek-VL-2 (Wu et al., 2024), DeepSeek-VL-2-small, DeepSeekVL-2-tiny, Kimi-VL-A3B-thinking-2506 (Team et al., 2025b). **_c) Embodied-Specific MLLMs:_** RoboBrain-2-32B (Team et al., 2025a), RoboBrain-2-7B, RoboBrain-2-3B, Embodied-R1-3B (Yuan et al., 2025), Magma-8B (Yang et al., 2025) **_d) MLLM Backbones of Vision-Language-Action (VLA) models:_** Prismatic-7B (Karamcheti et al., 2024) in OpenVLA (Kim et al., 2024), PaliGemma3B (Beyer et al., 2024) in _π_ 0 (Black et al., 2024), Qwen-2-VL-2B (Wang et al., 2024b) in DexVLA (Wen et al., 2025), Phi-3-Vision-4B (Abdin et al., 2024) in TraceVLA (Zheng et al., 2024). 

The first category of proprietary models was evaluated via their respective APIs. For the latter three categories, the models were downloaded and deployed locally for testing. To ensure a fair comparison, we used a consistent text prompt for all models. The system prompt was designed to encourage 

5 

PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs 

Table 1: Benchmark results on the PhysToolBench. For each difficulty level and scene category, the best performance was marked in **bold** and the second best was marked <u>underline.</u> *Prismatic7B achieves an unusually high score on the Medium-M3 difficulty. Upon inspecting its reasoning process, we discovered that the model does not generate sound reasoning but instead exhibits a strong tendency to output ”None” in all case. 

|**Categories**||**Difi**|**ficulty L**|**evel**|||**Scene Cate**|**gory**||**Overall**_↑_|
|---|---|---|---|---|---|---|---|---|---|---|
|**MLLM**|_Easy↑_|_m1↑_|_m2↑_|_m3↑_|_Hard↑_|_Professional↑_|_Industrial↑_|_Outdoor↑_|_Daily↑_||
|HUMAN(BEST)|96.19%|93.61%|90.78%|93.97%|89.10%|87.5%|93.52%|91.17%|96.71%|93.19%|
|HUMAN(WORST)|91.74%|87.77%|85.11%|90.36%|81.68%|80.5%|85.02%|87.65%|93.42%|87.85%|
|**General-Purpose Proprietary M**|**LLMs:**||||||||||
|GEMINI-2.5-PRO|78.10%|48.40%|46.10%|45.78%|36.14%|58.5%|61.54%|46.47%|51.39%|54.45%|
|O3|**93.02%**|67.02%|46.81%|22.89%|**49.50%**|64.0%|**68.02%**|**61.18%**|56.46%|61.56%|
|GPT-4O|86.03%|**70.74%**|48.23%|35.54%|44.06%|62.5%|63.97%|59.41%|**59.75%**|61.26%|
|GPT-5|90.16%|63.83%|**50.35%**|36.75%|46.04%|**67.5%**|66.8%|58.82%|57.97%|**62.15%**|
|GROK-4|73.65%|46.28%|30.50%|**52.41%**|39.60%|50.5%|59.92%|43.53%|52.15%|52.27%|
|CLAUDE-3-7-SONNET-THINKING|74.60%|58.51%|35.46%|27.11%|35.64%|53.5%|55.87%|45.88%|47.85%|50.59%|
|**General-Purpose Open-Source M**|**LLMs:**||||||||||
|QWEN-2.5-VL-72B|75.56%|55.85%|35.46%|31.93%|27.23%|51.5%|55.47%|44.71%|46.84%|49.51%|
|QWEN-2.5-VL-32B|67.62%|43.09%|30.5%|22.29%|19.31%|42.0%|49.39%|37.06%|36.46%|40.81%|
|QWEN-2.5-VL-7B|71.43%|51.6%|20.57%|21.08%|12.87%|44.0%|49.39%|38.24%|34.68%|40.71%|
|QWEN-2.5-VL-3B|36.51%|10.64%|6.38%|13.86%|9.9%|21.5%|21.46%|15.88%|16.2%|18.48%|
|GLM-4.5V-108B|90.48%|65.43%|36.88%|16.27%|35.15%|62.5%|59.92%|56.47%|47.85%|55.14%|
|GEMMA-3-27B|68.57%|57.45%|31.91%|19.88%|27.72%|50.0%|48.99%|42.94%|41.52%|45.26%|
|INTERNVL-3.5-38B|70.79%|50.53%|29.08%|18.67%|27.72%|51.0%|49.8%|37.65%|39.75%|44.07%|
|INTERNVL-3.5-30B-A3B|66.03%|37.77%|20.57%|15.06%|20.79%|41.0%|43.32%|31.18%|33.67%|37.06%|
|INTERNVL-3.5-14B|66.03%|40.43%|21.99%|21.08%|21.29%|44.0%|44.94%|31.76%|35.44%|38.83%|
|INTERNVL-3.5-1B|38.73%|19.68%|4.26%|3.61%|8.42%|22.5%|18.22%|20.0%|16.2%|18.58%|
|INTERNVL-3-78B|79.05%|53.72%|39.01%|21.08%|27.23%|52.0%|56.28%|42.94%|45.32%|48.91%|
|INTERNVL-3-38B|77.78%|44.68%|31.91%|16.87%|27.72%|51.0%|53.04%|41.18%|39.24%|45.26%|
|OVIS-2.5-9B|80.63%|55.85%|42.55%|17.47%|21.29%|57.0%|56.28%|44.12%|41.27%|48.52%|
|OVIS-2-34B|83.17%|45.21%|35.46%|15.66%|24.75%|56.5%|52.23%|40.0%|41.27%|46.74%|
|DEEPSEEK-VL2-27B|71.75%|39.89%|19.86%|6.63%|17.33%|44.0%|42.91%|35.88%|30.38%|37.06%|
|DEEPSEEK-VL2-SMALL-16B|64.44%|28.19%|10.64%|10.24%|9.9%|36.0%|37.65%|25.88%|25.06%|30.43%|
|DEEPSEEK-VL2-TINY-3B|7.62%|2.13%|2.84%|4.22%|1.98%|7.0%|5.26%|2.94%|2.78%|4.25%|
|KIMI-VL-30B-A3B-THINKING|79.05%|45.21%|31.21%|18.67%|13.37%|46.5%|48.58%|40.59%|38.99%|43.08%|
|**Embodied-Specified MLLMs:**|||||||||||
|ROBOBRAIN-2-32B|75.87%|49.47%|19.86%|6.63%|19.31%|48.5%|47.37%|39.41%|32.66%|40.51%|
|ROBOBRAIN-2-7B|66.03%|44.68%|13.48%|10.84%|11.88%|36.5%|41.7%|34.71%|29.87%|34.88%|
|ROBOBRAIN-2-3B|46.35%|18.62%|3.55%|11.45%|6.93%|25.5%|28.74%|18.24%|16.71%|21.64%|
|EMBODIED-R1-3B|38.41%|6.38%|4.96%|4.22%|6.93%|23.0%|20.24%|11.76%|11.39%|15.91%|
|MAGMA-8B|46.35%|29.26%|0%|3.01%|20.3%|19.0%|29.55%|25.88%|23.29%|24.41%|
|**MLLM backbones in VLAs:**|||||||||||
|PALIGEMMA-3B|7.94%|10.11%|0%|0%|1.49%|6.0%|4.86%|4.12%|4.05%|4.64%|
|PHI-3-VISION-4B|33.97%|12.77%|4.26%|3.01%|9.41%|20.5%|19.43%|11.18%|13.42%|15.91%|
|QWEN-2-VL-2B|19.37%|1.6%|0.71%|7.83%|2.97%|7.0%|9.31%|4.12%|10.13%|8.3%|
|PRISMATIC-7B|6.98%|4.26%|1.42%|*56.02%|0.99%|11.0%|13.77%|8.24%|14.43%|12.55%|


a Chain-of-Thought (Wei et al., 2022), explicitly asking the models to reason before providing their final answer. The only exception was for models that feature a native, built-in ”thinking” mode, in which case we allowed them to utilize their default inference process without modification. We also recruited 5 human participants as testers to serve as a reference. 

#### 4.2 OVERALL RESULTS 

As shown in Tab. 1, MLLMs generally underperform, with most scoring below 60%—a result far inferior to human performance, which consistently achieves at least 87.85% overall accuracy. This indicates that contemporary MLLMs have a superficial understanding of tool usage. Among the models evaluated, proprietary general-purpose MLLMs performed best. The OpenAI series (o3, gpt-4o, and gpt-5) all exceeded the 60% threshold, with gpt-5 leading the group. Open-source general-purpose MLLMs followed, typically scoring above 40%. GLM-4.5V was a notable exception, achieving 55.14% and outperforming not only its open-source peers but also some proprietary models, highlighting its significant potential. Embodied-specific MLLMs demonstrated some capability but lagged behind the general-purpose open-source models. Lastly, MLLM backbones within VLA frameworks exhibited the weakest performance, likely due to their limited number of parameters. An overall leaderboard of MLLMs is shown in Fig. 3. We provide a set of complete VQA results in Appendix. B. 

6 

PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs 


Figure 4: **Overall performance v.s. model size** for open-source MLLMs. A significant correlation is observed between performance and model size. 

Figure 5: Performance comparison between the embodied models and their base model. 

#### 4.3 FINDINGS ON PHYSTOOLBENCH 

**_F.1. A foundational ability to understand tools emerges in large models with sufficient scale._** As shown in Fig. 4, our evaluation of numerous open-source models reveals that there’s a significant correlation between the understanding of physical tool and the size of the model. Furthermore, for the easy difficulty setting in Tab. 1, we also observe that a foundational understanding of tool usage emerges once a model reaches a certain scale, which we preliminarily identify as approximately 10 billion parameters. Most models exceeding this 10B threshold achieve an accuracy of 60-70% on easy-level tasks. In contrast, performance drops significantly for smaller models; those with fewer than 5B parameters generally score below 50% on easy tasks and have an overall accuracy below 25%. Consequently, we recommend selecting MLLMs with more than 10 billion parameters for applications in embodied intelligence. 

**_F.2. A long-tail problem persists in tool recognition and understanding, even for the most advanced MLLMs._** Although top-tier MLLMs are proficient at identifying common objects, their performance diminishes for less common items, creating a long-tail effect. A notable finding is the models’ pronounced weakness in the subcategory of digital products. They frequently fail to distinguish between visually similar items, such as HDMI versus DP cables and Type-C versus Lightning charging ports. This deficiency is widespread in open-source models, where even the highly capable GLM-4V shows errors in basic recognition, as in Fig. 6. (a). Closed-source models offer a marginal improvement but still demonstrate only a shallow comprehension. As an example in Fig. 6. (c), most top-tier proprietary models do not grasp the functional requirement that a monitor must be connected to a laptop using an HDMI cable and an adapter if the laptop only has a Type-C port. 

**_F.3. Embodied-specific MLLMs show no significant advantage on PhysToolBench._** Models specifically fine-tuned for embodied tasks, such as RoboBrain2 and Embodied-R1, do not exhibit a notable performance improvement on our benchmark. RoboBrain2’s parameters were initialized from Qwen2.5VL and subsequently fine-tuned on a combination of general vision and robotic datasets. Nevertheless, as shown in Fig. 5, its 32B, 7B variants all performed slightly below their Qwen2.5VL backbone of equivalent scale. A similar trend was observed with Embodied-R1-3B, which, despite being fine-tuned from Qwen-2.5-VL-3B, also achieved a marginally lower score than the original model. These findings indicate that the fine-tuning process did not confer an enhanced understanding of tools. We hypothesize that current robotic datasets may require more high-quality data centered on tool comprehension to advance these models’ physical tool understanding. 

**_F.4. MLLMs exhibit a critical deficiency in comprehending tool availability, failing to grasp the fundamental principles of their utility._** The M3 difficulty tier of our benchmark was specifically designed to probe this issue by incorporating simple ”traps”: presenting the correct tool for a task but in a damaged or non-functional state. Counter-intuitively, as shown in Tab. 1, models found this task more difficult than the ”Hard” tier, which requires complex reasoning for tool creation. For instance, in the selected four cases in Fig. 6. (d), none of the MLLMs could identify when the tools are unavailable. This outcome strongly suggests that the models’ comprehension of tools is shallow and relies on surface-level ”common sense” associations rather than a robust understanding of their core functionality, leading them to hallucinate the tool’s usability. 

7 

PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs 


Figure 6: Some results of PhysToolBench. We showcase illustrative examples for each difficulty level, along with the answers from several top-tier models and human participants. Note that the markers are intentionally enlarged for visualization purposes. 

The implications of this hallucination for embodied agents are severe. An agent that cannot recognize a tool as non-functional may attempt to use it, resulting in mission failure and significant safety hazards—for instance, fueling a tractor with gasoline, drawing a blood sample with a damaged syringe. We contend that addressing this issue is critical for advancing embodied AI. 

**_F.5. The MLLM backbones in current VLAs are extremely weak._** Our evaluation revealed that the MLLM backbones of the contemporary VLA models exhibit exceptionally poor performance on PhysToolBench, with overall scores universally below 15%. This result calls into question the prevailing assumption that VLAs can effectively inherit ”common sense” from their base MLLM and then achieve generalization through fine-tuning on robotic action datasets. Our findings suggest that the foundational ”common sense” of these MLLMs is profoundly insufficient for general-purpose intelligence. We posit that this fundamental limitation cannot be rectified through fine-tuning on robotic datasets of a modest scale. Consequently, we conclude that advancing the VLA paradigm will require a two-pronged approach: first, leveraging significantly larger and more capable MLLMs as backbones; and second, a substantial expansion in the size and diversity of robotic action datasets. 

**_F.6. Reasoning ability is important and useful, but still insufficient._** The capability for reasoning is crucial. In our experiments, we evaluated a subset of models under two conditions: one with Chainof-Thought (CoT) prompting and one without. As shown in Tab. 2, the models prompted with CoT demonstrated significantly higher accuracy. Furthermore, models that are natively optimized for reasoning exhibit superior performance. For instance, GLM-4.5V, the top-performing opensource model, was trained with a strong emphasis on reasoning. Its training regimen included not only Supervised Fine-Tuning (SFT) on high-quality CoT datasets but also reinforcement learning to bolster its reasoning skills further. When utilizing its built-in ”thinking” mode, GLM-4.5V’s overall score was markedly higher than other open-source models and even surpassed some proprietary ones. Similarly, Ovis-2.5-9B, through specialized reasoning op timizations, achieved a total score of _<u>48.52%</u>_ with just 9B parameters—a performance comparable to that of 72B model <u>(</u> _<u>49.51%</u>_ <u>).</u> These results underscore the significant impact of reasoning. 

8 

PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs 


Figure 7: Comparison Between (a) Text-Level Reasoning and (b) Our proposed Vision-Centric Reasoning. 

Table 2: Influence of reasoning 

|**MLLM**|_Easy↑_|**Difficulty Level**<br>_Medium-M3↑_|_Hard↑_|**Overall**_↑_<br>_Total↑_|
|---|---|---|---|---|
|QWEN-2.5-VL-72B|79.68%|25.30%|24.26%|46.64%|
|+ CoT|75.56%|31.93%|27.23%|49.51%|
|QWEN-2.5-VL-32B|71.75%|11.45%|10.89%|34.88%|
|+ CoT|67.62%|22.29%|19.31%|40.81%|
|QWEN-2.5-VL-7B|75.24%|11.45%|13.37%|37.94%|
|+ CoT|71.43%|21.08%|12.87%|40.71%|
|GPT-4O|88.25%|35.54%|42.57%|60.77%|
|+ CoT|86.03%|35.54%|44.06%|61.26%|
|+ VCR|–|45.78%|–|–|
|GPT-5 (W/ THINKING)|90.16%|36.75%|46.04%|62.15%|
|+ VCR|–|54.81%|–|–|


However, current reasoning abilities remain inadequate. Models are prone to generating hallucinations in certain tasks. Moreover, their spatial reasoning is deficient; for instance, as depicted in Fig. 6. (b), none of the models realized that a flathead screwdriver of the right size could also unscrew this Phillips screw. We contend that a greater focus on visual-centric reasoning is essential for models to effectively undertake high-level planning tasks. 

#### 4.4 A PRELIMINARY SOLUTION 

We here further introduce a preliminary method aiming at improving the reasoning process. Current MLLMs often exhibit a modality bias, where reasoning occurs predominantly at the text level while frequently overlooking crucial visual information, as shown in Fig. 7. (a). To mitigate this, we propose an approach that emphasizes vision-centric reasoning. As shown in Fig. 7. (b), we developed a Vision-Centric Reasoning Agent with an MLLM as its backbone and decomposed the answering process into three distinct steps. First, in the Global Analysis stage, the agent forms a holistic understanding of the user’s query in the context of the image. Second, it invokes an object detection tool (DINOX (Ren et al., 2024), formatted as an MCP tool for agent use) to identify and crop objects based on their bounding boxes. These crops then undergo a secondary, more In-depth Analysis. Finally, the agent performs Multi-level Evidence Integration and Reasoning, synthesizing the initial global understanding with the detailed analysis of the cropped objects to formulate the final answer. 

We evaluated our approach on the M3 difficulty level, where existing models perform the worst. As shown in Tab. 7, our method leads to substantial performance gains when using the same backbone MLLM. Specifically, GPT-4o and GPT-5 achieved performance boosts of _<u>10.24%</u>_ and _<u>18.06%</u>_ <u>, re-</u> spectively, highlighting the critical importance of vision-centric reasoning. Although this approach is relatively straightforward and shares conceptual similarities with some concurrent work (Man et al., 2025), we aim to demonstrate the significance of vision-centric reasoning in the context of embodied intelligence. We hope our findings will inspire further research in Embodied Agents. 

### 5 CONCLUSION 

We present PhysToolBench, a novel benchmark for evaluating the understanding of physical tools in MLLMs. This VQA benchmark comprises 1,000 image-text pairs, spanning a broad spectrum of scenarios and features three fine-grained difficulty tiers to probe the depth of model comprehension. We evaluated 32 MLLMs, including closed-source, open-source, embodied-specific models, and MLLM backbones used in VLA models. Our findings reveal that all tested models fall significantly short of human performance, highlighting a critical gap in their ability to reason about physical tools. Through an extensive analysis, we identify the key weaknesses of current MLLMs and outline promising directions for future research. We propose PhysToolBenchas a tiered evaluation standard to systematically measure the capability frontiers of embodied agents and a road map for a more general intelligence. 

9 

PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs 

## SUPPLEMENTARY MATERIALS OF PHYSTOOLBENCH: BENCHMARKING PHYSICAL TOOL UNDERSTANDING FOR MLLMS 

### A MORE DETAILS ABOUT BENCHMARK CONSTRUCTION 

#### A.1 DATASET CONSTUCTION 

Here, we provide a more detailed introduction to the construction details of our benchmark. The entire benchmark and evaluation code will be open-sourced. 

**_Phase 1: Conceptualization._** In this phase, we invited 5 experts (all are co-authors) to conceptualize task-scene pairs through manual brainstorming to obtain high-quality data. Continuous discussions were conducted throughout this process, which lasted three weeks and resulted in an initial collection of 1,500 cases. The intermediate results of this phase are presented in CSV files, as shown in Fig. 8. 


Figure 8: Task-Scene Pair Brainstorming 

**_Phase 2: Image Generation._** We took the scene descriptions brainstormed in the previous step and fed them into GPT-4o for image generation. To better approximate real-world use cases, we added an additional prompt to most cases: _‘photo taken with a smartphone, slightly cluttered arrangement.‘_ This process was closely supervised by human experts who vetted the generated images for quality, realism, and accuracy. While a significant number of initial generations contained inaccuracies, most images met our stringent criteria after 1 to 3 iterations of refinement through regeneration or prompting to modify the inaccurate parts, achieving a level of realism nearly indistinguishable from actual photographs. For the small subset of cases where the generative model consistently failed—particularly with complex objects such as digital products, which GPT-4o struggled to render correctly—we resorted to physical staging and photography based on the original scene descriptions. We present here some examples of generation failure cases alongside the final corrected images in Fig. 9. 

**_Phase 3: Human-in-the-Loop Annotation and Quality Review._** During the annotation process, we developed annotation software that retained an ”Abnormal Annotation” function, enabling annotators to flag cases with problematic images or tasks while conducting annotations. Subsequently, after completing a batch of data annotation, we assigned another group of reviewers to re-examine 

10 

PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs 


Figure 9: Example failure cases and the final revised images 


Figure 10: UI demonstration of our annotation app 

the images and regenerate problematic images as needed. A demonstration of the UI of the annotation app is provided in Fig. 10. 

Through these three rigorous rounds of benchmark construction with continuous review processes, we ultimately filtered out 1,000 high-quality cases. We also conducted a simple analytical experiment to demonstrate the authenticity of the generated images in the next section. 

11 

PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs 

#### A.2 REALISM EVALUATION OF GENERATED IMAGES 

To quantitatively assess the realism of the generated images in PhysToolBench, we first utilize GPT4o as an evaluator and also conduct a user study. The prompt provided to GPT-4o is shown in Fig. 11. We randomly select 100 images from PhysToolBenchand ask GPT-4o to rate their realism on a scale of 0 to 2, where 2 represents highly realistic, 1 denotes somewhat realistic, and 0 indicates unrealistic. The average score obtained from GPT-4o is _<u>1.92</u>_ <u>, suggesting that most images in Phys-</u> ToolBenchare realistic. Additionally, we perform a user study with 10 participants, who also rate the same 100 images on the same scale. The average score from the user study is _<u>1.78</u>_ <u>, which aligns</u> closely with the GPT-4o evaluation. These findings indicate that the images in PhysToolBenchare generally realistic and appropriate for evaluating the physical tool comprehension of MLLMs. 

### B COMPLETE DEMONSTRATION OF IMAGE–QUESTION–ANSWER TRIPLETS 

Since the examples in Fig. 6 are different from the actual ones for illustrative purposes, we provide the full, verbatim materials, including the original input images and text prompts, the corresponding ground-truth answers, and GPT-4o’s outputs for each instance here, as in Figures 12 to 20. 

12 

PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs 

Please evaluate strictly and return ONLY the three scores as requested. ## Scoring Criteria **Physical Realism (0-2):** How well the image adheres to physical laws and the natural world. * **0 (Rejected):** The image violates fundamental physical laws (e.g., gravity, perspective, proportions). Elements are unrealistic and seem artificial or impossible. * **1 (Conditional):** Minor but noticeable inconsistencies with physical laws, such as perspective errors or unnatural material properties. Some elements feel believable, but the image contains flaws that undermine its realism. * **2 (Exemplary):** The image fully adheres to physical laws, with accurate proportions, perspective, gravity, and believable materials. The elements are naturally placed, adhering to real-world expectations without any notable flaws. **Color and Quality Realism (0-2):** How accurate and natural the colors and image quality appear. * **0 (Rejected):** Colors are unnatural, overly saturated, or inconsistent with real-world expectations. The image quality is poor, with visible artifacts, noise, or significant blurriness. * **1 (Conditional):** Colors are mostly natural but may have noticeable distortions. The image quality is generally clear, but there are issues with sharpness, contrast, or color accuracy that detract from the overall realism. * **2 (Exemplary):** Colors are vivid yet natural, with no noticeable distortions or color inconsistencies. The image is sharp, clear, and free of any artifacts, offering high-quality realism that closely mimics real life. **Lighting and Shadow Realism (0-2):** How naturally light and shadows are rendered in the image. * **0 (Rejected):** Light and shadows are inconsistent, poorly placed, or physically impossible (e.g., shadows in the wrong direction, lighting that doesn't match the scene, or an unnatural light source). * **1 (Conditional):** Lighting and shadows are generally accurate but show minor inconsistencies, such as shadows being slightly off or lighting lacking refinement. It could be better calibrated to mimic realworld conditions. * **2 (Exemplary):** Lighting and shadows are perfectly rendered, with realistic sources, natural falloff, and precise interactions with surfaces. Shadows and highlights align perfectly with the scene, creating a cohesive and realistic environment. --## Output Format **Do not include any other text, explanations, or labels.** You must return only one line of text, containing a metric and the corresponding score, for example: **Example Output:** Physical Realism: 1 Color and Quality Realism: 2 Lighting and Shadow Realism: 0 --**IMPORTANT Enforcement:** Be EXTREMELY strict in your evaluation. A score of '2' should be very rare, reserved only for images that meet the highest possible standards in each metric. If there is any doubt or visible flaw, downgrade the score. For **Physical Realism**: A score of '2' should only be given if the image fully respects the laws of physics, with perfect proportions, perspective, and material behavior that match real-world expectations. For **Color and Quality Realism**: A score of '2' should be given only when the colors are natural, vibrant, and free of distortions, with impeccable image quality and no artifacts or noise present. For **Lighting and Shadow Realism**: A score of '2' should only be given for lighting and shadows that are flawlessly rendered, with natural sources, consistent falloff, and realistic shadow placement. --Please strictly adhere to the scoring criteria and follow the template format when providing your results. 

Figure 11: We utilize GPT-4o to evaluate the realism of the final images. Above is the system prompt we provided to GPT-4o. 

13 

PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs 


Figure 12: Examples of data in PhysToolBenchwith GPT-4o predictions. 


Figure 13: Examples of data in PhysToolBenchwith GPT-4o predictions. 


Figure 14: Examples of data in PhysToolBenchwith GPT-4o predictions. 

14 

PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs 


Figure 15: Examples of data in PhysToolBenchwith GPT-4o predictions. 


Figure 16: Examples of data in PhysToolBenchwith GPT-4o predictions. 


Figure 17: Examples of data in PhysToolBenchwith GPT-4o predictions. 

15 

PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs 


Figure 18: Examples of data in PhysToolBenchwith GPT-4o predictions. 


Figure 19: Examples of data in PhysToolBenchwith GPT-4o predictions. 


Figure 20: Examples of data in PhysToolBenchwith GPT-4o predictions. 

16 

PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs 

### REFERENCES 

- Marah I Abdin et al. Phi-3 technical report: A highly capable language model locally on your phone. _CoRR_ , abs/2404.14219, 2024. URL https://doi.org/10.48550/arXiv. 2404.14219. 

- Anthropic. Claude 3.7 sonnet and claude code, Feb 2025. URL https://www.anthropic. com/news/claude-3-7-sonnet. 

- Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, et al. Qwen2. 5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 

- Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0.5: A Vision-Language-Action Model with Open-World Generalization. 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. Pi0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Gheorghe Comanici, Eric Bieber, Mike Schaekermann, Ice Pasupat, Noveen Sachdeva, Inderjit Dhillon, Marcel Blistein, Ori Ram, Dan Zhang, Evan Rosen, et al. Gemini 2.5: Pushing the frontier with advanced reasoning, multimodality, long context, and next generation agentic capabilities. _arXiv preprint arXiv:2507.06261_ , 2025. 

- Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, et al. Palm-e: An embodied multimodal language model. 2023. 

- George Jiayuan Gao, Tianyu Li, Junyao Shi, Yihan Li, Zizhe Zhang, Nadia Figueroa, and Dinesh Jayaraman. Vlmgineer: Vision language models as robotic toolsmiths. _arXiv preprint arXiv:2507.12644_ , 2025. 

- Shijue Huang, Wanjun Zhong, Jianqiao Lu, Qi Zhu, Jiahui Gao, Weiwen Liu, Yutai Hou, Xingshan Zeng, Yasheng Wang, Lifeng Shang, et al. Planning, creation, usage: Benchmarking llms for comprehensive tool utilization in real-world complex scenarios. _arXiv preprint arXiv:2401.17167_ , 2024. 

- Yue Huang, Jiawen Shi, Yuan Li, Chenrui Fan, Siyuan Wu, Qihui Zhang, Yixin Liu, Pan Zhou, Yao Wan, Neil Zhenqiang Gong, et al. Metatool benchmark for large language models: Deciding whether to use tools and which to use. _arXiv preprint arXiv:2310.03128_ , 2023. 

- Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow, Akila Welihinda, Alan Hayes, Alec Radford, et al. Gpt-4o system card. _arXiv preprint arXiv:2410.21276_ , 2024. 

- Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa Sadigh. Prismatic vlms: Investigating the design space of visually-conditioned language models. In _Forty-first International Conference on Machine Learning_ , 2024. 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

17 

PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs 

- Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi. Blip: Bootstrapping language-image pretraining for unified vision-language understanding and generation. In _International conference on machine learning_ , pp. 12888–12900. PMLR, 2022. 

- Jiarui Lu, Thomas Holleis, Yizhe Zhang, Bernhard Aumayer, Feng Nan, Felix Bai, Shuang Ma, Shen Ma, Mengyu Li, Guoli Yin, et al. Toolsandbox: A stateful, conversational, interactive evaluation benchmark for llm tool use capabilities. _arXiv preprint arXiv:2408.04682_ , 2024a. 

- Shiyin Lu, Yang Li, Qing-Guo Chen, Zhao Xu, Weihua Luo, Kaifu Zhang, and Han-Jia Ye. Ovis: Structural embedding alignment for multimodal large language model. _arXiv preprint arXiv:2405.20797_ , 2024b. 

- Shiyin Lu, Yang Li, Yu Xia, Yuwei Hu, Shanshan Zhao, Yanqing Ma, Zhichao Wei, Yinglun Li, Lunhao Duan, Jianshan Zhao, et al. Ovis2. 5 technical report. _arXiv preprint arXiv:2508.11737_ , 2025. 

- Yunze Man, De-An Huang, Guilin Liu, Shiwei Sheng, Shilong Liu, Liang-Yan Gui, Jan Kautz, YuXiong Wang, and Zhiding Yu. Argus: Vision-centric reasoning with grounded chain-of-thought. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 14268–14280, 2025. 

- OpenAI. Addendum to gpt-4o system card: 4o image generation. Online supplement, March 2025a. Accessed September 2025. 

- OpenAI. Gpt-5 system card, Aug 2025b. URL https://cdn.openai.com/ gpt-5-system-card.pdf. 

- OpenAI. Openai o3 and o4-mini system card, Apr 2025c. URL https: //cdn.openai.com/pdf/2221c875-02dc-4789-800b-e7758f3722c1/ o3-and-o4-mini-system-card.pdf. 

- Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pp. 8748–8763. PmLR, 2021. 

- Tianhe Ren, Yihao Chen, Qing Jiang, Zhaoyang Zeng, Yuda Xiong, Wenlong Liu, Zhengyu Ma, Junyi Shen, Yuan Gao, Xiaoke Jiang, et al. Dino-x: A unified vision model for open-world object detection and understanding. _arXiv preprint arXiv:2411.14347_ , 2024. 

- Chao Tang, Anxing Xiao, Yuhong Deng, Tianrun Hu, Wenlong Dong, Hanbo Zhang, David Hsu, and Hong Zhang. Mimicfunc: Imitating tool manipulation from a single human video via functional correspondence. _arXiv preprint arXiv:2508.13534_ , 2025. 

- BAAI RoboBrain Team, Mingyu Cao, Huajie Tan, Yuheng Ji, Minglan Lin, Zhiyu Li, Zhou Cao, Pengwei Wang, Enshen Zhou, Yi Han, et al. Robobrain 2.0 technical report. _arXiv preprint arXiv:2507.02029_ , 2025a. 

- GLM-V Team. Glm-4.5v and glm-4.1v-thinking: Towards versatile multimodal reasoning with scalable reinforcement learning, 2025. URL https://arxiv.org/abs/2507.01006. 

- Kimi Team, Angang Du, Bohong Yin, Bowei Xing, Bowen Qu, Bowen Wang, Cheng Chen, Chenlin Zhang, Chenzhuang Du, Chu Wei, et al. Kimi-vl technical report. _arXiv preprint arXiv:2504.07491_ , 2025b. 

- Noah Trupin, Zixing Wang, and Ahmed H Qureshi. Dynamic robot tool use with vision language models. _arXiv preprint arXiv:2505.01399_ , 2025. 

- Junying Wang, Wenzhe Li, Yalun Wu, Yingji Liang, Yijin Guo, Chunyi Li, Haodong Duan, Zicheng Zhang, and Guangtao Zhai. Affordance benchmark for mllms. _arXiv preprint arXiv:2506.00893_ , 2025a. 

18 

PhysToolBench: Benchmarking Physical Tool Understanding for MLLMs 

- Pei Wang, Yanan Wu, Zekun Wang, Jiaheng Liu, Xiaoshuai Song, Zhongyuan Peng, Ken Deng, Chenchen Zhang, Jiakai Wang, Junran Peng, et al. Mtu-bench: A multi-granularity tool-use benchmark for large language models. _arXiv preprint arXiv:2410.11710_ , 2024a. 

- Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Yang Fan, Kai Dang, Mengfei Du, Xuancheng Ren, Rui Men, Dayiheng Liu, Chang Zhou, Jingren Zhou, and Junyang Lin. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. _arXiv preprint arXiv:2409.12191_ , 2024b. 

- Weiyun Wang, Zhangwei Gao, Lixin Gu, Hengjun Pu, Long Cui, Xingguang Wei, Zhaoyang Liu, Linglin Jing, Shenglong Ye, Jie Shao, et al. Internvl3. 5: Advancing open-source multimodal models in versatility, reasoning, and efficiency. _arXiv preprint arXiv:2508.18265_ , 2025b. 

- Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. _Advances in neural information processing systems_ , 35:24824–24837, 2022. 

- Junjie Wen, Yichen Zhu, Jinming Li, Zhibin Tang, Chaomin Shen, and Feifei Feng. Dexvla: Vision-language model with plug-in diffusion expert for general robot control. _arXiv preprint arXiv:2502.05855_ , 2025. 

- Zhiyu Wu, Xiaokang Chen, Zizheng Pan, Xingchao Liu, Wen Liu, Damai Dai, Huazuo Gao, Yiyang Ma, Chengyue Wu, Bingxuan Wang, et al. Deepseek-vl2: Mixture-of-experts vision-language models for advanced multimodal understanding. _arXiv preprint arXiv:2412.10302_ , 2024. 

- xAI. Grok 4 model card, Aug 2025. URL https://data.x.ai/ 2025-08-20-grok-4-model-card.pdf. 

- Jianwei Yang, Reuben Tan, Qianhui Wu, Ruijie Zheng, Baolin Peng, Yongyuan Liang, Yu Gu, Mu Cai, Seonghyeon Ye, Joel Jang, et al. Magma: A foundation model for multimodal ai agents. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 14203–14214, 2025. 

- Junjie Ye, Zhengyin Du, Xuesong Yao, Weijian Lin, Yufei Xu, Zehui Chen, Zaiyuan Wang, Sining Zhu, Zhiheng Xi, Siyu Yuan, et al. Toolhop: A query-driven benchmark for evaluating large language models in multi-hop tool use. _arXiv preprint arXiv:2501.02506_ , 2025. 

- Yifu Yuan, Haiqin Cui, Yaoting Huang, Yibin Chen, Fei Ni, Zibin Dong, Pengyi Li, Yan Zheng, and Jianye Hao. Embodied-r1: Reinforced embodied reasoning for general robotic manipulation. _arXiv preprint arXiv:2508.13998_ , 2025. 

- Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daum´e III, Andrey Kolobov, Furong Huang, and Jianwei Yang. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. _arXiv preprint arXiv:2412.10345_ , 2024. 

- Jinguo Zhu, Weiyun Wang, Zhe Chen, Zhaoyang Liu, Shenglong Ye, Lixin Gu, Hao Tian, Yuchen Duan, Weijie Su, Jie Shao, et al. Internvl3: Exploring advanced training and test-time recipes for open-source multimodal models. _arXiv preprint arXiv:2504.10479_ , 2025. 

19 

