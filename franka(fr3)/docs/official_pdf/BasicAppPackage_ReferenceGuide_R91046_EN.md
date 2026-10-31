> **[PDF を開く](<BasicAppPackage_ReferenceGuide_R91046_EN.pdf>)**
>
> PDF から自動変換した本文です。図は含まず、表は崩れている場合があります。安全や仕様の確認には PDF を使ってください。





Reference Guide 

BASIC APP PACKAGE 



© Copyright 2026 Franka Robotics GmbH Koppstraße 12 81379 Munich Germany 

Document name:              Reference Guide of Basic App Package Document number:          R91046 



Get your manual and additional supporting material in English and other languages at <u>www.franka.de/documents.</u> 



### **TABLE OF CONTENTS** 

|TA|BLE OF CONTENTS .......................................................................................................................................................................................... 3|
|---|---|
|1|INTRODUCTION ............................................................................................................................................................................................ 4|
|1|.1<br>About The Basic App Package ...................................................................................................................................... 4|
|2|MOTION APPS ................................................................................................................................................................................................ 4|
|3|INPUT/OUTPUT APPS ................................................................................................................................................................................. 6|
|4|GROUPS ............................................................................................................................................................................................................. 7|





# **1 INTRODUCTION** 

## **1.1 About The Basic App Package** 

#### **Automation of processes is made easy.** 

<mark>Apps incorporate the entire complexity of the robot system and represent modular building blocks of a production proc</mark> ess. The <mark>Basic Apps lower your entry barrier to process automation, getting you started quickly and independently. The bundle includes everything you need for the most common applications such as pick and place or handling. Additionally, we also provide additional Apps for various applications that can be found and downloaded in Franka World (https://franka.world).</mark> 

# **2 MOTION APPS** 

### Cart Motion 

The Cart Motion App allows the user to teach different positions that the robot should move to. The robot will execute the motion on a straight-line path with defined velocities. 



### Joint Motion 

The Joint Motion App lets the user teach joint configurations that the robot will move to with defined velocities. The robot will move to the target positions without following a defined path between two positions. 



### Move 

The Move App offers three different options (as fast as possible, following a linear trajectory or reaching its taught joint configuration as fast as possible) for moving the robot to each taught pose. 



### Move to Contact 

The M **ove to Contact** App executes a motion to a taught position. Within a defined distance to the target position the robot will expect physical contact. When the robot senses contact, it will abort the current motion and continue to execute its task. This App can be used to seek contact with the environment or push components against a physical stop. 



4 

Franka Robotics GmbH © 



### Relative Motion 

The Relative Motion App moves the end effector relative to its current position. The App allows the robot to move translational and rotational along its axis. The relative motion can be set either in the robot base or end effector coordinate system. 



### Pick 

The Pick App enables the picking of an object at a certain position. It offers multiple motion strategies for approaching and retracting from the pick position, that allow quick implementation of picking even in complex situations e.g. from a part magazine. The App is exclusively designed for Franka Hand. 



### Place 

The Place App has six options to set up the motion of placing an object at a certain position. Release, place & retract or approach and place are just three of them. The App is exclusively designed for Franka Hand. 



### Gripper Move 

The Gripper Move App moves the fingertips of the Franka Hand to a specific width with a velocity defined by the user. 



### Apply Force 

The Apply Force App enables the robot to apply a force or a torque in a determined direction for a predefined time. The arm can move within set limits during the App execution. 



### Figure Motions 

The Figure Motions App executes precise motions of geometrical curves (spiral or a sinusoidal) in a user defined plane which is helpful for use cases where a component search is needed. During the motion the robot can also apply forces and torques, which can be used for part insertions and plug connections. 



5 

Franka Robotics GmbH © 



# **3 INPUT/OUTPUT APPS** 

### Wait 

The Wait App introduces a defined wait until a certain condition holds true or the waiting time has expired. Wait conditions can either be the status of a digital input or output that is connected to the Mastercontroller via Modbus TCP, or the result of a logical operation based on integer variables stored on the OPC UA server, or a selected period. 



### Event 

The Event App raises an error that displays a customizable error message **.** 



### OPC UA Out 

The OPC UA Out App can write an integer variable to the OPC UA server running on the robot’s Mastercontroller. An already existing variable can also be modified or deleted within this App. Variables on the OPC UA server can then be read from other Apps or external systems. 



### Modbus Out 

The Modbus Out App can set one or multiple digital outputs that are on Digital-Output-Modules connected to the Mastercontroller via Modbus TCP. Each pin can be enabled or disabled when the App is executed. These signals can then be read from other Apps, robots or external systems. 



### Gripper Init 

The Gripper Init App executes the initialization procedure of the Franka Hand. It can be set whether the App should reinitialize the Franka Hand even if it is already initialized or not. 



### Measure Pose 

The Measure Pose App shows the current TCP position in relation to the base of the robot in real time. The App can also display the distance and relative orientation between a taught position and the current position. 



6 

Franka Robotics GmbH © 



### Set Mass 

The Set Weight App adjusts the payload weight settings of the robot. Used when additional weight is added or removed from the robot e.g. picking up a part or additional hardware or removing it from the robot. The weight set in the App is added to the end effector’s weight. Not required when using the Pick or Place App. 



### Check Weight 

The Check Weight App checks if a weight measured by the robot’s torque sensors lies within specified limits. If the weight is outside the boundaries the App will raise an error. 



### Check Position 

The Check Robot Position App checks if the robot's end effector is within a defined area. If the robot is in the correct position execution continues as usual, if not the App raises an error. Therefore, it can be ensured that the robot is in the correct position. 



### Self-Test 

The Self-Test App performs a TD2 Self-Test of all the seven joints of the robot. These tests must be performed within 24 h intervals. When a task is programmed that would exceed this test interval, this App could be included in the task to perform the test automatically. The defined time should exceed the forthcoming test interval. 



# **4 GROUPS** 

### If 

Groups are container Apps used to customize the behavior of the contained Apps by providing parameters or positions and augmenting their functionality. Groups also allow them to build complex workflows in order to react to events defined by the user. 



7 

Franka Robotics GmbH © 



### Branch 

The Branch Group evaluates the status of a digital input or output connected to the Mastercontroller via Modbus TCP, or the result of a logical operation based on integer variables stored on the OPC UA server. If the condition holds true, the upper branch is executed. If the conditions are evaluated to be false, the lower branch is executed. 



### Catch Event 

The Catch Event Group stops the execution of the upper branch and executes the lower branch when a specified event is caught. Catchable type of events can be either the status of a digital input or output connected to the Mastercontroller via Modbus TCP, the result of a logical operation based on integer variables stored on the OPC UA server or specified errors. It can be used to implement error recovery strategies. 



### Pattern 

The Pattern Group allows users to define geometrical patterns (grids, circles, lines and points) by only teaching the required reference points. All positions within the pattern are calculated. For every execution of the Pattern Group the robot is moved to one pattern position and all contained Apps are executed. It is recommended to be used inside a Repeat Group to move to all pattern poses. The order in which the positions are moved can be set by the user, even using an OPC UA variable or define a custom order. 



### Repeat 

The Repeat Group repeats the contained Apps for a fixed number of iterations, until a digital input or output connected to the Mastercontroller via Modbus TCP is present, or the result of a logical operation based on integer variables stored on the OPC UA server holds true. The repetition can be started automatically or after a specified waiting time. 



### Parallel Execution 

Th **e** Parallel Execution Group allows users to run two branches of applications at the same time. It is possible to define which of the two branches shall be waited to finish successfully or to wait for both branches to finish. Only one branch can move the robot. Otherwise, an error is triggered. 



8 

Franka Robotics GmbH © 



### Structure 

The Structure Group enables users to group a sequence of Apps together e.g., to collapse and visualize them into a compact structure. 



### Joint Compliance 

The Joint Compliance Group overrides the general joint compliance settings for the contained Apps allowing to adjust the stiffness of the robot arm while using the Joint Motion, Cartesian Motion, Relative Motion, Move Contact, Move, Pick or Place App. 



### Cartesian Compliance 

Th **e** Cartesian Compliance Group overrides the general cartesian compliance settings for the contained Apps allowing to adjust the stiffness behavior of the robot arm while using the Apply Force, Figure Motion or Assembly App. 



### Thresholds 

The Thresholds Group overrides the general thresholds settings for the contained Apps allowing to adjust the collision behavior of the robot arm at the end effector. 



### Robot Status 

The Robot Status Group sets OPC UA variables or digital outputs connected to the Mastercontroller via Modbus TCP to specified values either the contained Apps are currently running, or the execution of the Apps has finished successfully, or the contained Apps have caused an error. The App shall be used for external process monitoring. 



### Optimize 

The Optimize Group is a tool that can be used to find the best App parametrization for a single App or a sequence of Apps. It executes the Apps iteratively with different parameter sets until it finds the right combination of parameter values. In the lower branch, a set of Apps can be inserted, which will be executed after one try. This sequence of Apps is intended to recover the initial state of the optimization behavior. 



9 

Franka Robotics GmbH © 



franka.de 







Franka Robotics GmbH Koppstraße 12 81379 Munich 

10 

Franka Robotics GmbH © 

