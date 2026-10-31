> 変換元: `getting_started.rst.txt`

# Setting Up the Robot System and Network for FCI

After completing the real-time kernel setup, ensuring proper network configuration (see Network requirements), and installing libfranka, you can connect to the robot and verify the setup by using FCI to read the current robot state.

## Operating the Robot

Before proceeding, review the following safety considerations:

1.  Ensure the Arm is mounted on a stable base that cannot topple over, even during fast motions or abrupt stops.

> [!CAUTION]
> Only tabletop mounting is supported (the Arm must be perpendicular to the ground). Other mountings **void the warranty** and **may damage the robot**.

2.  Verify that the cable connecting Arm and Control is firmly attached on both sides.
3.  Connect the external activation device to the Arm's base and keep it accessible to stop the robot at any time.

<div class="hint">

<div class="title">

Hint

</div>

Activating the external activation device will disconnect the Arm from Control. The joint motor controllers will hold their current position. **The external activation device is not an emergency stop.**

</div>

This list is non-exhaustive. The robot manual contains a dedicated chapter on safety and is available via the [Franka World Hub](https://world.franka.de/resources).

> [!IMPORTANT]
> The workstation PC controlling the robot with FCI must be connected to the LAN port of Control (shop floor network), **not** the LAN port of the Arm (robot network).

## Installing the FCI Feature

To operate the robot through the Franka Control Interface, the corresponding Feature must be installed. Check Desk --\> Settings --\> System --\> Installed Features.

If FCI is not installed, synchronize it from your Franka World account to your controller. You must have an FCI license and a registered controller in your account. Refer to the [Franka World user manual](https://download.franka.de/franka-world-manual/) for details.

## Setting Up the Network

Good network performance is critical when using FCI. A direct connection between the workstation PC and Franka's Control is recommended.

<figure class="align-center">
<img src="assets/control.png" alt="Use Control&#39;s LAN port when controlling the robot through FCI. Do not connect to the port in the Arm&#39;s base." />
<figcaption aria-hidden="true">Use Control's LAN port when controlling the robot through FCI. Do not connect to the port in the Arm's base.</figcaption>
</figure>

The Control and workstation must appear on the same network. For this tutorial, the following static IP addresses are used:

|         | Workstation PC | Control    |
|---------|----------------|------------|
| Address | 172.16.0.1     | 172.16.0.2 |
| Netmask | 24             | 24         |

The Control's address (172.16.0.2) is referred to as `<fci-ip>` in the following sections.

<div class="hint">

<div class="title">

Hint

</div>

Desk can be accessed via `https://<fci-ip>`, though your browser may display a certificate warning.

</div>

The configuration consists of two steps:

- Configuring Control's network settings.
- Configuring your workstation's network settings.

### Control Network Configuration

Before configuring, ensure the robot is installed and tested according to the documents shipped with it.

For system version \>= 5.5.0, configure Control's network via the settings interface. You may temporarily connect through the Arm's base port. Refer to <span class="title-ref">Connecting a user interface device</span> in the robot manual.

<figure class="align-center">
<img src="assets/FrankaUI_Settings_Bar.png" alt="Access the Franka settings interface through Desk." />
<figcaption aria-hidden="true">Access the Franka settings interface through Desk.</figcaption>
</figure>

<figure class="align-center">
<img src="assets/FrankaUI_Settings_Network.png" alt="Set a static IP for the Control&#39;s LAN port (Shop Floor network). DHCP Client option is deselected." />
<figcaption aria-hidden="true">Set a static IP for the Control's LAN port (Shop Floor network). DHCP Client option is deselected.</figcaption>
</figure>

After applying the settings, connect the workstation LAN port to the Control unit.

### Linux Workstation Network Configuration

On Ubuntu 16.04 (GUI):

1.  Open the Network Connection widget, select the wired connection, and click **Edit**.

<figure class="align-center">
<img src="assets/edit-connections.png" alt="Edit the connection in the Ethernet section." />
<figcaption aria-hidden="true">Edit the connection in the Ethernet section.</figcaption>
</figure>

2.  In the IPv4 settings tab, set the method to **Manual** and enter the values:

<figure class="align-center">
<img src="assets/static-ip-ubuntu.png" alt="Set a static IP for the workstation PC." />
<figcaption aria-hidden="true">Set a static IP for the workstation PC.</figcaption>
</figure>

<div class="hint">

<div class="title">

Hint

</div>

This disables DHCP. When no longer using FCI, revert the Method to <span class="title-ref">Automatic (DHCP)</span>.

</div>

3.  Save changes and reconnect. Test connectivity using network-bandwidth-delay-test. Desk can now be accessed via the assigned IP in your browser.

## Preparing the Robot for FCI in Desk

Ensure the robot's brakes are unlocked and the activation device released. The robot is ready when the blue LED is active.

### Activating FCI Mode

In Desk:

1.  Release the robot brakes.
2.  Expand the top menu and click **Activate FCI**.

<figure class="align-center">
<img src="assets/FrankaUI_System_ActivateFCI.png" width="300" alt="Activating FCI mode in Desk (system version &gt;= 5.5.0)." />
<figcaption aria-hidden="true">Activating FCI mode in Desk (system version &gt;= 5.5.0).</figcaption>
</figure>

#### FCI Mode in Franka Emika Robot (FER)

Once FCI mode is activated, a pop-up confirms the mode is active and Desk interactions are disabled. The pop-up must remain open while working with FCI.

<figure class="align-center">
<img src="assets/pop_up_fci.png" alt="Pop-up when FCI mode is active." />
<figcaption aria-hidden="true">Pop-up when FCI mode is active.</figcaption>
</figure>

#### FCI Mode in Franka Research 3

<figure class="align-center">
<img src="assets/FrankaUI_System_ActivateFCI_Done.png" />
</figure>

After activation, a pop-up appears requiring user confirmation.

## Verifying the Connection

The IP of the Control's LAN port is referred to as `<fci-ip>` in the following examples.

Ensure the robot is prepared for FCI usage in Desk. Run the `echo_robot_state` example from `libfranka`:

``` shell
./examples/echo_robot_state <fci-ip>
```

The program prints the current robot state to the console. Refer to `RobotState|structfranka_1_1RobotState.html` for field explanations.

``` text
{
  "O_T_EE": [0.998578,0.0328747,-0.0417381,0,0.0335224,-0.999317,0.0149157,0,-0.04122,-0.016294,
             -0.999017,0,0.305468,-0.00814133,0.483198,1],
  "O_T_EE_d": [0.998582,0.0329548,-0.041575,0,0.0336027,-0.999313,0.0149824,0,-0.0410535,
               -0.0163585,-0.999023,0,0.305444,-0.00810967,0.483251,1],
  "F_T_EE": [0.7071,-0.7071,0,0,0.7071,0.7071,0,0,0,0,1,0,0,0,0.1034,1],
  "EE_T_K": [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
  "m_ee": 0.73, "F_x_Cee": [-0.01,0,0.03], "I_ee": [0.001,0,0,0,0.0025,0,0,0,0.0017],
  ...
}
```

<div class="hint">

<div class="title">

Hint

</div>

If an error occurs, perform the ping test and ensure the fail-safe locking system is open. Refer to the robot manual for additional instructions.

</div>
