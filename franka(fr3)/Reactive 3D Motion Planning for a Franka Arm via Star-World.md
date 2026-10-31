---
title: "Reactive 3D Motion Planning for a Franka Arm via Star-World Workspace Reshaping"
date: "2026-07-27"
authors: "Gia Dcosta; Saayuj Deshpande; Samhitha Vedire"
url: https://arxiv.org/abs/2607.25138
pdf: https://arxiv.org/pdf/2607.25138
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2607.25138)** / [論文ページ](https://arxiv.org/abs/2607.25138)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Reactive 3D Motion Planning for a Franka Arm via Star-World Workspace Reshaping 

Gia Dcosta, Saayuj Deshpande, and Samhitha Vedire 

University of Pennsylvania, Philadelphia, PA, USA 

**_Abstract_ —Safety inflation can cause nearby obstacles to overlap, violating the disjoint-obstacle assumptions used by many modulation-based reactive planners. We investigate Star-World workspace reshaping for three-dimensional reactive control of a Franka Emika Panda manipulator. At each update, intersecting inflated obstacles are clustered and replaced by star-shaped proxies before a dynamical-system-based end-effector controller is evaluated. A null-space artificial-potential-field term provides complementary arm-body avoidance. We compare reshaped and unreshaped obstacle representations in six PyBullet scenarios using goal attainment, path-length ratio, and computation time. In this preliminary 12-trial evaluation, reshaping reaches the goal in five of six scenarios, compared with four of six for the unreshaped baseline. It resolves the canonical overlapping-wall case and requires 0.68–8.70 ms per workspace update for scenes containing one to seven obstacles. However, it also increases path length, produces near-equilibria in two cases, and closes a navigable corridor through over-aggressive merging. These results show both the promise and the practical limitations of transferring Star-World guarantees from workspace geometry to a redundant manipulator controlled through inverse kinematics.** **_Index Terms_ —dynamical systems, Franka Emika Panda, obstacle avoidance, reactive motion planning, workspace reshaping** 

## I. INTRODUCTION 

Robotic manipulators operating in real-world environments must continuously react to obstacles while still reaching desired goals safely and efficiently. This problem becomes especially important in cluttered workspaces where nearby objects, narrow passages, and uncertain geometry can significantly affect robot motion. 

Traditional global trajectory planning approaches compute a path ahead of time using a fixed environment model. While these methods can generate optimal paths, they are often computationally expensive and less adaptable to changing environments. Reactive planning methods instead continuously update robot motion online based on the current robot state and nearby obstacle information. This allows robots to quickly respond to changes in the workspace while maintaining smooth motion toward a goal. 

Dynamical-system-based (DS) motion planning is particularly attractive for reactive manipulation because it generates smooth and continuous vector fields. A nominal DS drives the robot toward the goal while modulation techniques modify the velocity field near obstacles to avoid collisions. Unlike trajectory optimization methods that repeatedly solve optimization problems online, DS-based methods are lightweight and naturally suited for continuous reactive control. 

However, many modulation-based planners assume that the workspace forms a disjoint star world in which obstacles are star-shaped and non-overlapping. In realistic environments this assumption is frequently violated, and the planner may generate highly conservative motion, oscillatory behavior, or fail to converge entirely. 

This problem becomes even more challenging for robotic manipulators such as the Franka Panda arm. The robot must navigate through cluttered three-dimensional environments while accounting for both end-effector motion and arm-body collision avoidance. 

The goal of this project is to investigate whether StarWorld workspace reshaping can improve reactive planning performance in cluttered 3D scenes. Instead of directly planning around overlapping inflated obstacles, intersecting obstacles are grouped into clusters and reshaped into cleaner star-shaped obstacle regions before planning. 

Our implementation extends the Star-World reshaping ideas proposed by Dahlin and Karayiannidis [1] into a 3D manipulator setting. We evaluate the proposed approach on a Franka Panda arm using success rate, path length ratio, and computational runtime. 

## _A. Motivation and Contributions_ 

Reactive obstacle avoidance becomes increasingly difficult when multiple inflated obstacles overlap or come very close together. In standard modulation-based planners [2], [3], each obstacle independently contributes a modulation matrix to the velocity field. When several inflated obstacles intersect, the planner receives conflicting local obstacle information that can distort or cancel the reactive velocity field. This is illustrated in Fig. 1: two overlapping circles form an impassable wall, yet their independent repulsion vectors cancel exactly on the approach axis, driving the robot directly into the barrier. StarWorld reshaping merges both circles into a single proxy with an off-axis kernel, producing a coherent tangential deflection that routes the robot around the combined obstacle. 

These effects become particularly severe in cluttered manipulation environments where safety inflation is necessary to account for sensing uncertainty, robot thickness, controller inaccuracies, and safety margins. Although inflation improves safety, it also increases the likelihood of obstacle overlap and violates the disjointness assumptions required for convergence guarantees of modulation-based planners. In dense scenes, the baseline planner may: 

_•_ Produce highly conservative or unsafe trajectories, 


Fig. 1: 2-D illustration of the core failure mode. _Upper_ : two overlapping circles modulated independently - repulsion vectors cancel on the approach axis, driving the robot into the wall. _Lower_ : Algorithm 2 merges both circles into one proxy; the offset kernel gives a coherent tangential deflection. 

## II. RELATED WORK 

## _A. Dynamical-System-Based Motion Planning_ 

Dynamical systems are widely used in reactive robotics because they generate smooth trajectories while remaining computationally lightweight. A nominal attractor dynamical system is typically written as: 


where _x_ is the current robot position, _xg_ is the goal position, and _K_ is a positive gain matrix. Obstacle avoidance is introduced through modulation matrices that deform the nominal vector field near obstacles [5]. Huber et al. [2], [3] extended this framework to guarantee convergence for convex and star-shaped obstacles, provided the workspace satisfies a disjointness condition. These methods preserve continuous online replanning while maintaining smooth trajectories, and form the reactive controller used in this project. 

## _B. Artificial Potential Fields_ 

Artificial Potential Fields (APFs) are another popular reactive planning approach [6]. Attractive forces pull the robot toward the goal while repulsive forces push it away from obstacles. Although APFs are computationally efficient, they may suffer from local minima and unstable behavior in cluttered environments. In this work, APF-style repulsive terms are used for arm-body collision avoidance while the end-effector follows the DS-based modulation planner. 

## _C. Star-World Workspace Reshaping_ 

- Generate oscillatory behavior near obstacle intersections, 

- Fail to converge to the goal due to conflicting modulation contributions, 

- Exhibit poorly interpretable velocity field deformations. 

Rather than independently modulating around several overlapping obstacles, Algorithm 2 of Dahlin & Karayiannidis [1] clusters intersecting obstacles, computes a star-shaped hull proxy per cluster with a guaranteed kernel point, and presents the planner with a _disjoint star world_ . This satisfies the structural preconditions for convergence. This work makes three contributions: 

- a three-dimensional implementation of Star-World proxy construction for reactive end-effector planning; 

- an integrated controller that combines proxy-based DS modulation with null-space arm-body avoidance for a redundant manipulator; and 

- a comparative simulation study that identifies both successful overlap handling and failure modes caused by conservative merging, joint limits, and heuristic kernel placement. 

Dahlin and Karayiannidis [1] proposed Star-World workspace reshaping to address the disjointness requirement of modulationbased planners. The paper introduces two key constructs: (1) the _admissible kernel_ , a region from which an obstacle cluster can be seen as star-shaped while excluding the robot and goal positions; and (2) the _star-shaped hull with specified kernel_ , which merges intersecting obstacles into a single convex proxy guaranteed to contain a valid kernel point. Together these allow Algorithm 2 of [1] to iteratively cluster overlapping obstacles and produce a disjoint star world suitable for convergenceguaranteed reactive planning. Our implementation extends this framework to the full 3-D end-effector space of a Franka Panda arm. 

## III. METHODOLOGY 

The complete planning pipeline consists of: 

- 1) Scene modeling and obstacle inflation, 

- 2) Star-World reshaping (admissible kernel, kernel selection, star-shaped hull, re-clustering), 

- 3) Reactive DS planning with modulation, 

- 4) APF arm-body avoidance and null-space IK, 

- 5) Franka execution via IK position control. 


Fig. 2: Complete reactive planning pipeline for Star-World workspace reshaping and reactive Franka arm control. 

## _A. Scene Modeling and Obstacle Inflation_ 

Obstacles are modeled as 3-D spheres represented as Ellipsoid objects (degenerate case _Q_ = _r_<sup>2</sup> _I_ ): 


where _ci_ is the obstacle center and _ri_ is the obstacle radius. Each obstacle is inflated by a safety margin ∆ _r_ before any planning step: 


Inflation consolidates the robot’s volume and sensing uncertainty into the obstacle representation, allowing the planner to treat the end-effector as a point. A fixed margin of ∆ _r_ = 0 _._ 10 m is used in all experiments. Obstacles are rendered as visual-only bodies in PyBullet (no physics collision geometry) so that the simulator does not generate spurious contact forces that would corrupt the EE trajectory. 

## _B. Star-World Reshaping_ 

Algorithm 2 [1] iteratively reshapes the inflated obstacles into a disjoint star world. The loop runs until the cluster partition stabilizes (typically 1–2 iterations) or a safety cap is reached. 

**Algorithm 1** Reactive Planning with Star-World Reshaping 

- 1: Initialize Franka arm and obstacle set in PyBullet 2: Inflate obstacle radii by safety margin ∆ _r_ 3: **while** goal not reached **do** 4: **At 4 Hz:** query obstacle positions; form Ellipsoid objects 5: **for** each obstacle cluster (Algorithm 2) **do** 6: Compute admissible kernel (cone intersections / convex hull) 

- 7: Select kernel points _K_ (equilateral triangle / tetrahedron) 8: Construct star-shaped hull proxy SH _K_ ( _OC_ ) 9: Re-cluster intersecting proxies; repeat if partition changed 

- 10: **end for** 11: **At 40 Hz:** compute nominal velocity _f_ 0 = ( _xg −x_ ) _/∥xg −x∥_ 12: Compute Γ _i_ and modulation matrices _Mi_ for each proxy 13: Apply proximity-weighted modulation: _x_ ˙ mod = _M_ ( _x_ ) _f_ 0 14: Monitor all 9 arm links; compute APF repulsion when Γ _<_ 1 _._ 6 15: Project APF correction into null space: ∆ _q_ ns = _N_ ∆ _q_ corr 16: Solve IK seeded from current joints; apply null-space correction 

- 17: Command joints via PyBullet position control 18: **end while** 

_1) Admissible Kernel:_ For each obstacle cluster _C_ , the admissible kernel is the set of candidate kernel points from which the union of obstacles appears star-shaped while still excluding the robot and goal positions: 


In 2-D each per-obstacle, per-excluded-point kernel is a cone fan polygon (Eq. 8 of [1]) whose apex lies at _x_ ¯ and whose edges are tangent lines to the obstacle. Intersecting these cones via Sutherland–Hodgman clipping gives the feasible kernel region for the cluster. This cache is built once outside the loop because the robot and goal positions are fixed within a timestep. 

If the admissible kernel is empty, the algorithm falls back to a convex decomposition of each obstacle (Eq. 14 of [1]). 

_3-D approximation._ In 3-D the paper’s cone-intersection procedure is approximated by the convex hull of the cluster’s surface samples. This approximation is sufficient in practice for sphere obstacles but does not carry the formal guarantee of the 2-D construction: it is no longer strictly proven that the robot position _x_ and goal _xg_ are excluded from the resulting proxy. Tighter guarantees would require implementing the full 3-D cone exclusion analogues of the 2-D admissible kernel. 

_2) Kernel Selection:_ Given the feasible kernel region, Algorithm 3 selects _n_ +1 affinely independent kernel points _K_ whose convex hull CH( _K_ ) lies strictly inside the admissible kernel. In 2-D, _K_ is an equilateral triangle centred at the feasible region’s centroid with side length proportional to the local inscribed-circle radius; in 3-D a regular tetrahedron is used instead. Temporal coherence is enforced by reusing the previous timestep’s kernel centroid when it remains inside the current feasible region, preventing the robot from switching circumvention direction mid-trajectory. 

_3) Star-shaped Hull and Re-clustering:_ The star-shaped hull of cluster _C_ with kernel _K_ is built as one convex piece per obstacle (Property 4d of [1]): 


After building all proxy hulls, any pair of proxies whose pieces intersect are merged via union-find and the loop repeats. Fig. 3 illustrates this construction for a cluster of three 2- D ellipse obstacles: the admissible kernel cones (one per obstacle per excluded point) are intersected to yield the feasible kernel region, the selected kernel triangle _K_ is placed at its centroid, and the per-obstacle star-shaped hull pieces SH _K_ ( _Oi_ ) = CH( _Oi ∪ K_ ) are assembled into the final disjoint proxy. 


Fig. 3: Star-World construction for three 2-D ellipse obstacles. Shaded regions show individual admissible kernel cones; the green triangle is the selected kernel _K_ ; coloured outlines are the per-obstacle starshaped hull pieces SH _K_ ( _Oi_ ) forming the disjoint proxy. 

## _C. Reactive Dynamical System Planning_ 

_1) Nominal Dynamics:_ A goal-attractor DS provides the nominal end-effector velocity. In practice the velocity is normalized to a unit vector so that speed is controlled separately by _v_ max: 


_2) Modulation Matrix:_ For each star-world proxy _Oi_<sup>_′_the</sup> controller builds a modulation matrix _Mi_ that suppresses motion into the proxy while amplifying tangential motion. The kernel centre _xc,i ∈_ int ker( _Oi_<sup>_′_)guaranteedbyAlgorithm2</sup> serves as the proxy’s reference point [2]. The normalized distance uses the direction-dependent proxy radius _ri_ ( _x_ ) (the support function of the proxy hull in the direction ( _x − xc,i_ )): 


An orthonormal frame is built from the outward normal and two tangent vectors: 


The eigenvalue matrix encodes the asymmetric response: 


Because _Ei_ is orthonormal the modulation matrix is _Mi_ = _EiDiEi_<sup>_T_.Multipleproxiesarecombinedviaproximity-</sup> weighted superposition with weights _wi ∝_ Γ<sup>_−_</sup> _i_<sup>_p_</sup> (exponent _p_ = 2): 


## IV. FRANKA KINEMATICS AND CONTROL 

The Franka Panda arm is a 7-DOF serial manipulator with joint vector _q ∈_ R<sup>7</sup> . Forward kinematics map joint angles to end-effector position, _x_ = _f_ ( _q_ ), and differentiating gives: 


where _J_ ( _q_ ) _∈_ R<sup>3</sup><sup>_×_7</sup> is the translational Jacobian of the end-effector link. Rather than inverting the Jacobian explicitly, the implementation uses PyBullet’s built-in damped IK solver (calculateInverseKinematics) seeded with the current joint configuration _q_ cur at each control step. Seeding from the current state minimizes joint motion and prevents discontinuous solution jumps: 


where _x_ target = _x_ + _x_ ˙ mod ∆ _t_ is the Cartesian step from the modulated velocity. Joint limits _q ∈_ [ _q_ min _, q_ max] are enforced directly inside the IK call. 

## _A. Null-Space Arm-Body Avoidance_ 

End-effector modulation alone cannot prevent the arm links from colliding with obstacles. A secondary APF layer monitors all nine Franka links. Each link is approximated as a capsule sampled at three fractions along the segment between consecutive joint origins. When any sample point has Γ _<_ 1 _._ 6, a repulsion correction ∆ _q_ corr is computed in joint space via the Jacobian transpose. 

To apply this correction without disturbing the end-effector trajectory, it is projected into the null space of the EE Jacobian: 


The null-space step is scaled so that _∥_ ∆ _q_ ns _∥≤_ 0 _._ 07 rad (scaling the whole vector preserves the null-space direction, whereas per-component clipping would cause EE drift). A posture-restoring term simultaneously biases the arm toward a 

nominal elbow-up configuration. Both corrections are smoothed with an exponential moving average ( _α_ = 0 _._ 10) to suppress chattering. The final joint command is: 


Joint commands are sent via PyBullet position control at 40 Hz while the star world is rebuilt at 4 Hz to limit computation overhead. 

## V. IMPLEMENTATION DETAILS 

The system is implemented in Python using PyBullet for physics simulation and visualization of the Franka Panda arm. The starworlds package provides Algorithm 2, the reactive controller, and the StarWorldUpdater stateful wrapper that auto-detects 2-D or 3-D geometry from the obstacle type. The implementation includes: 

- Obstacle generation and inflation via Ellipsoid objects, 

- _•_ Star-World reshaping at 4 Hz (create_star_world_3d), 

- DS modulation at 40 Hz (ReactiveController), 

- Null-space APF arm-body avoidance across all 9 Franka links, 

- PyBullet IK position control with joint-limit enforcement, 

- Visualization of proxy hull wireframes and EE trajectory traces, 

- Evaluation metrics: success rate, path length ratio, and starworld update runtime. 

The full source code is available at https://github.com/saayuj/ star-worlds and a demonstration video at https://youtu.be/ MY4ZFPl7pGw. 

## VI. EXPERIMENTAL EVALUATION 

## _A. Simulation Setup_ 

Experiments are performed in PyBullet using a simulated Franka Panda arm across the following six named scenarios: 

- 1) **test** – single sphere directly on the approach path; the simplest possible sanity check and easy baseline, 

- 2) **overlap** – two heavily overlapping spheres rendered as visual-only bodies in PyBullet, so the arm passes through their geometry unless actively deflected by the modulation field; the canonical before/after comparison for the merging case, 

- 3) **simple** – 4 obstacles (2 dynamic, 2 small static); the two static spheres are placed close enough to merge into one star-world proxy, demonstrating online cluster formation, 

- 4) **moderate** – 6 obstacles at medium density; some pairs cluster dynamically as obstacles move, 

- 5) **corridor** – narrow passage between wall-like obstacle arrays; tests behavior when merging may block the only viable gap, 

- 6) **wall** – three-sphere vertical wall placed across the direct path; primary showcase for obstacle merging and off-axis kernel placement. 

Each scenario is run once with Star-World reshaping enabled (Algorithm 2) and once in _raw mode_ , in which Algorithm 2 is 

bypassed and the Huber controller modulates directly against each individual inflated sphere. This controlled comparison isolates the effect of workspace reshaping from the remaining implementation choices. Each trial has a 60 s time limit. A run is labeled successful when the end-effector reaches within 2 cm of the goal by the end of the recorded trial. 

Because each scenario–mode pair is evaluated with a single deterministic run, the results are a preliminary case study rather than a statistical estimate of the planners’ success probabilities. Repeated trials with randomized obstacle motions and initial configurations are required for inferential comparisons. 

## _B. Evaluation Metrics_ 

_1) Goal attainment:_ A trial is recorded as successful if _∥x_ ( _T_ ) _− xg∥ <_ 0 _._ 02 m by the end of the recorded trial: 


_2) Path length and deviation:_ Cumulative EE path length is accumulated at 40 Hz: 


Path deviation measures how much extra distance the planner travels relative to the straight-line distance covered toward the goal: 


The path length ratio _L/∥xg − x_ 0 _∥_ provides a scenenormalized efficiency measure. 

_3) Computational runtime:_ Star-world update time and velocity computation time are recorded separately using wallclock timestamps at each invocation: 


Mean values are reported in milliseconds. The star world runs at 4 Hz and the velocity controller at 40 Hz, so the relevant budgets are 250 ms and 25 ms respectively. 

## _C. Results_ 

All six scenarios were run in PyBullet simulation with a 60 s timeout. Each trial was run once per mode (raw baseline vs. Star-World). The raw baseline uses the Huber modulation controller directly against one inflated sphere proxy per obstacle; the Star-World mode first runs Algorithm 2 to produce a disjoint proxy set and then applies the same controller to the resulting proxies. 

_1) Quantitative summary:_ Across the six evaluated scenarios, the raw baseline reaches the goal in 4/6 cases (67%) with a mean path-length ratio of 1 _._ 10 _±_ 0 _._ 18 and a mean completion time of 6 _._ 4 _±_ 1 _._ 4 s among successful runs. Star-World reshaping reaches the goal in 5/6 cases (83%); for the three clean convergences ( _simple_ , _moderate_ , _wall_ ) the mean path-length ratio is 1 _._ 35 _±_ 0 _._ 21 and the mean completion time is 8 _._ 1 _±_ 1 _._ 8 s. The two remaining Star-World successes ( _test_ , _overlap_ ) converge only at the 60 s timeout limit with high path ratios (5.10 and 6.55), indicating near-equilibria that are eventually escaped. Star-World update time scales from 0.68 ms (1 obstacle) to 8.70 ms (7 obstacles), well within the 250 ms budget at 4 Hz. Velocity computation remains _≈_ 0 _._ 3 ms per step in both modes. 

_2) Scenario analysis:_ **simple and moderate.** These are the scenarios best suited to Star-World reshaping. Obstacles are sufficiently spread that Algorithm 2 produces a small number of well-separated proxies. In _simple_ , two nearby static spheres merge into one proxy; both modes succeed with essentially identical path lengths (ratio 1.07 vs. 1.004). In _moderate_ , six partly dynamic obstacles are consolidated into a single large proxy; the Star-World trajectory is longer (ratio 1.48 vs. 1.01) but converges cleanly in 10.2 s vs. 7.0 s. In both cases the unified proxy provides a consistent repulsion direction and the arm reaches the goal without oscillation. 

**wall.** The three-sphere vertical wall is the primary showcase for obstacle merging. All three spheres fuse into a single proxy and the kernel is placed off the approach axis, giving the modulation field a coherent tangential direction; the Star-World arm arcs cleanly around the wall (ratio 1.49, 7.3 s). The raw controller fails (5.1 s): three independent modulation matrices produce conflicting repulsions that trap the arm between the spheres without convergence. 

**test.** A single sphere directly on the approach path. The raw controller deflects around it cleanly (ratio 1.41, 4.3 s). The Star-World arm also reaches the goal but requires the full 60 s timeout (ratio 5.10). The kernel is placed on the approach axis, initially generating a modulation vector that partially opposes the goal direction and driving the arm toward the workspace boundary; the arm eventually escapes the near-equilibrium and converges, but the resulting path is highly circuitous. 

**overlap.** The canonical two-sphere overlapping-wall scenario shows the intended contrast. The raw baseline fails (6.0 s): the competing outward normals from the two spheres cancel on the approach axis, driving the arm into the pair without deflecting it around. Star-World reshaping merges both spheres into a single proxy with an off-axis kernel, producing a coherent tangential deflection; the arm converges to the goal at the 60 s limit (ratio 6.55), indicating some circuitous routing before final convergence. 

**corridor.** The raw controller traverses the narrow gap cleanly (ratio 0.98, 7.8 s). Star-World reshaping fails: Algorithm 2 merges all seven corridor obstacles (six wall spheres plus the moving blocker) into a single large proxy that entirely fills the corridor cross-section. The resulting proxy has no gap for the EE to pass through, so the modulation field deflects the arm to the workspace boundary and the trial times out after 


(a) Without Star-World reshaping 


(b) With Star-World reshaping 

Fig. 4: Wall-scenario comparison between (a) the unreshaped baseline and (b) Star-World workspace reshaping. 

TABLE I: Per-Scenario Results: Raw Baseline vs. Star-World Reshaping 

|Scenario|Mode|Success|Path (m)|Straight (m)|Ratio|Sim. Time (s)|Avg. SW Update (ms)|
|---|---|---|---|---|---|---|---|
|test|Raw|✓|0.541|0.384|1.41|4.3|—|
||Star-Worlds|✓|1.960|0.384|5.10|60.0|0.68|
|overlap|Raw|×|0.836|0.420|1.99|6.0|—|
||Star-Worlds|✓|2.751|0.420|6.55|60.0|1.79|
|simple|Raw|✓|0.846|0.843|1.004|6.5|—|
||Star-Worlds|✓|0.901|0.843|1.07|6.7|6.52|
|moderate|Raw|✓|0.919|0.910|1.01|7.0|—|
||Star-Worlds|✓|1.343|0.910|1.48|10.2|6.98|
|corridor|Raw|✓|1.019|1.040|0.98|7.8|—|
||Star-Worlds|×|7.136|1.040|6.86|60.0|8.70|
|wall|Raw|×|0.633|0.640|0.99|5.1|—|
||Star-Worlds|✓|0.954|0.640|1.49|7.3|2.68|


circulating for 60 s with path ratio 6.86. 

_3) Failure-case analysis:_ Three qualitatively distinct failure modes emerged while running tests. 

**Near-equilibria near workspace boundaries.** In the _test_ and _overlap_ scenarios the EE is temporarily held near the workspace boundary before eventually converging, producing highly circuitous paths (ratios 5.10 and 6.55) and consuming the full 60 s budget. These near-equilibria arise from the interaction between the modulation field (which pushes the EE away from the proxy boundary) and the IK solver (which clamps the joint targets to workspace limits); the arm escapes rather than fully stalling, but convergence is degraded. 

**Over-aggressive merging in corridor-like geometry.** In the _corridor_ scenario, disjoint obstacles that are individually navigable become a single impassable proxy after merging. The current Algorithm 2 implementation merges clusters whenever their inflated radii overlap, with no mechanism to 

preserve passable gaps. The merged proxy correctly satisfies the mathematical conditions of a disjoint star world, but it is topologically more conservative than the original obstacle set. 

**Kernel placement inside small single-obstacle proxies.** When Algorithm 2 processes a single isolated obstacle, the admissible kernel region is the exterior complement of the sphere. The kernel selection heuristic (centroid of the feasible polygon) can place the kernel point at an unfortunate location relative to the goal direction, biasing the modulation away from the goal rather than around the obstacle. 

## _D. Computational Complexity_ 

Star-world update cost scales as _O_ ( _N_<sup>2</sup> ) in the number of obstacles _N_ (one cone intersection per obstacle-excluded-point pair), plus _O_ ( _K · M · n_ approx) for the star-shaped hull and reclustering steps ( _K_ clusters of mean size _M_ , _n_ approx = 16). Measured update times of 0.68–8.70 ms for 1–7 obstacles 

fit comfortably within the 250 ms budget at 4 Hz. Velocity computation costs _≈_ 0 _._ 3 ms per step in both modes. 

## VII. DISCUSSION 

## _A. Interpretation and Validity_ 

The comparison suggests that reshaping is most useful when overlap creates conflicting modulation directions, as in the wall scenario. It is not uniformly beneficial: conservative proxy construction can remove feasible homotopy classes, and the workspace-level geometric construction does not account for joint limits or full-arm kinematics. 

The evaluation has four important validity limitations. First, each scenario–mode pair contains only one run, so the reported fractions must not be interpreted as population success probabilities. Second, all tests are simulation-only and use spherical obstacle models. Third, the three-dimensional admissible-kernel construction is an approximation and therefore does not inherit the complete guarantee of the two-dimensional formulation. Fourth, the raw and reshaped modes share the same IK and arm-body avoidance layers; failures can therefore arise from controller coupling rather than workspace reshaping alone. 

The results reveal a nuanced picture. Star-World reshaping performs as intended in _simple_ , _moderate_ , and _wall_ : it consolidates overlapping obstacles into a unified proxy, eliminates competing modulation contributions, and produces smooth convergent trajectories. The algorithm is computationally lightweight and operates comfortably online. However, three scenarios expose limitations that have practical importance. 

**Gap preservation.** The most actionable improvement would be a gap-aware merging criterion that declines to merge two clusters when the free corridor between their inflated boundaries is wider than the robot’s effective cross-section. This would prevent the corridor failure and allow the planner to handle narrow-passage environments that are currently blocked by over-merging. 

**Workspace-aware IK integration.** The secondary equilibria observed in _test_ and _overlap_ are not failures of Algorithm 2 per se, but of the coupling between the EE modulation field and the 3-D IK solver near joint limits. Incorporating workspaceboundary repulsion directly into the reactive controller, or replacing the Euler-integration IK target with a Riemannian motion policy that respects joint-limit geometry, would eliminate these spurious attractors. 

**Kernel selection for single-obstacle clusters.** For clusters containing only one obstacle, the feasible kernel region is large and the current centroid heuristic does not account for the goal direction. A simple improvement would be to bias the kernel centroid toward the side of the obstacle that minimizes the angle between the resulting proxy normal and the goal direction, ensuring that the modulation always deflects the EE around rather than away from the goal. 

**Dynamic and real-world extensions.** Incremental star-world updates (re-clustering only changed obstacles) would reduce latency for fast-moving scenes. Deployment on a physical Franka would additionally require ellipsoid fitting from depthsensor point clouds and online radius estimation. 

**Full-arm star world.** The current approach applies Algorithm 2 only in EE space; arm-body avoidance relies on an APF null-space correction that does not benefit from workspace reshaping. Extending the star-world framework to joint space, or applying it independently at multiple arm cross-section points, could provide stronger arm-body safety guarantees in cluttered manipulation tasks. 

**Adaptive star-world activation.** A practical engineering consideration emerging from the results is that Star-World reshaping should not necessarily be applied at all times. The algorithm introduces non-trivial computational overhead (up to _≈_ 9 ms per update) and tends to increase path length in scenarios where obstacles do not meaningfully overlap. When obstacles are well-separated and individually navigable, the raw modulation controller is both faster and more path-efficient. A promising direction is therefore to design a switching mechanism that monitors the current obstacle configuration — e.g., by checking whether any pair of inflated obstacle boundaries overlap — and activates Algorithm 2 only when overlapping clusters are detected. This would preserve the convergence guarantees of star-world reshaping precisely where they are needed, while falling back to the lighter raw controller in benign scenes. 

## VIII. CONCLUSION 

This paper presented a full 3-D reactive planning pipeline for a Franka Panda arm using Star-World workspace reshaping (Algorithm 2 of Dahlin & Karayiannidis [1]). The pipeline integrates online obstacle clustering, star-shaped hull proxy construction, Huber-modulation end-effector control, and nullspace APF joint-space arm-body avoidance, running at 4 Hz for world updates and 40 Hz for velocity commands. 

Experimental results across six PyBullet scenarios show that Star-World reshaping achieves a 5/6 success rate vs. 4/6 for the raw baseline. In _simple_ , _moderate_ , and _wall_ it produces clean convergent trajectories (path-length ratios 1.07–1.49); in _overlap_ it correctly handles the canonical two-sphere wall that defeats the raw controller. The star-world update scales from 0.68 ms to 8.70 ms for 1–7 obstacles, well within the online planning budget. 

Residual limitations include near-equilibria in single-obstacle and two-sphere scenarios (arm converges only at the 60 s timeout limit), over-aggressive merging that blocks navigable corridors, and suboptimal kernel placement on the approach axis. These highlight that Algorithm 2’s correctness guarantees apply to the mathematical proxy structure and do not automatically transfer to a 7-DOF IK-controlled arm. Future work should address gap-aware merging, workspace-boundary-aware modulation, and goal-directed kernel selection. 

## ACKNOWLEDGMENT 

We thank Prof. Nadia Figueroa and the University of Pennsylvania MEAM 6230 teaching team for their guidance during the development of this work. 

REFERENCES 

- [1] A. Dahlin and Y. Karayiannidis, “Creating star worlds: Reshaping the robot workspace for online motion planning,” _IEEE Transactions on Robotics_ , vol. 39, no. 5, pp. 3655–3670, 2023. 

- [2] L. Huber, A. Billard, and J.-J. Slotine, “Avoidance of convex and concave obstacles with convergence ensured through contraction,” _IEEE Robotics and Automation Letters_ , vol. 4, no. 2, pp. 1462–1469, 2019. 

- [3] L. Huber, J.-J. Slotine, and A. Billard, “Avoiding dense and dynamic obstacles in enclosed spaces: Application to moving in crowds,” _IEEE Transactions on Robotics_ , vol. 38, no. 5, pp. 3113–3132, 2022. 

- [4] A. Billard, S. Mirrazavi, and N. Figueroa, _Learning for Adaptive and Reactive Robot Control: A Dynamical Systems Approach_ . MIT Press, 2022. 

- [5] S. M. Khansari-Zadeh and A. Billard, “A dynamical system approach to realtime obstacle avoidance,” _Autonomous Robots_ , vol. 32, no. 4, pp. 433–454, 2012. 

- [6] O. Khatib, “Real-time obstacle avoidance for manipulators and mobile robots,” _The International Journal of Robotics Research_ , vol. 5, no. 1, pp. 90–98, 1986. 

