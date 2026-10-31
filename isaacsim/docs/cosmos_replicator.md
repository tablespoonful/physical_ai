> 出典: https://docs.isaacsim.omniverse.nvidia.com/6.1.0/replicator_tutorials/tutorial_replicator_cosmos.html
> 取得日: 2026-10-31

Is this page helpful?

# Cosmos Synthetic Data Generation#

This tutorial demonstrates generating multi-modal synthetic data for NVIDIA Cosmos using the CosmosWriter in Isaac Sim. The writer captures synchronized RGB, depth, segmentation, and edge data from a robot navigating a warehouse environment.

The generated data serves as ground truth input for Cosmos Transfer, which transforms low-resolution control signals into high-quality visual simulations through its Multi-ControlNet architecture.

## Why Use the CosmosWriter?#

The CosmosWriter bridges the gap between simulation and real-world robotics applications by generating rich, multi-modal datasets from synthetic environments. Key use cases include:

- Sim-to-Real Transfer: Transform synthetic simulation videos into photorealistic scenes with varied materials, lighting, and environmental conditions using Cosmos Transfer

- Domain Adaptation: Generate diverse training data from a single simulation, creating variations in scene styles, materials, and lighting without re-running expensive simulations or capturing real-world data

- Data Augmentation: Expand limited datasets by generating multiple visual variations while preserving robot motions, object positions, and scene structure

For examples of sim-to-real transformations in robotics, see the Cosmos Cookbook Robotics Gallery, which showcases how synthetic kitchen scenes can be transformed into photorealistic environments with different cabinet styles, robot materials, and lighting conditions.

## Prerequisites#

- Familiarity with the omni.replicator extension and its writers

- Basic understanding of Isaac Sim’s SDG Getting Started Scripts

- Running simulations as Standalone Applications or via the Script Editor.

## What the CosmosWriter Generates#

The writer outputs five synchronized modalities from the robot’s camera:

- RGB - Color imagery (vis control)

- Depth - Distance-to-camera for spatial understanding

- Segmentation - Instance masks for object tracking

- Shaded Segmentation - Instance masks with realistic shading

- Edges - Canny edge detection for boundaries

These modalities correspond to Cosmos Transfer’s control branches:

- vis: Uses RGB imagery with bilateral blurring

- edge: Applies Canny edge detection (tunable thresholds)

- depth: Depth maps for 3D structure understanding

- seg: Segmentation masks for object identification

Each control branch can be weighted (0.0-1.0) to balance adherence vs. creative freedom in the generated output.

## Implementation#

This example demonstrates a Carter Nova robot autonomously navigating through a warehouse environment. As the robot moves from its starting position to a target location, the CosmosWriter captures synchronized multi-modal data (RGB, depth, segmentation, shaded segmentation, and edges) from the robot’s front camera. The captured data is organized into clips, with each clip containing a sequence of frames that can be used as input for Cosmos Transfer.

Standalone Application
The example can be run as a standalone application using the following commands in the terminal (on Windows use python.bat instead of python.sh):

./python.sh standalone_examples/replicator/cosmos_writer_warehouse.py

Full Standalone Script"""Generate synthetic video clips in a warehouse using the CosmosWriter."""

from isaacsim import SimulationApp

simulation_app = SimulationApp(launch_config={"headless": False})

import argparse
import os
from typing import Any

import carb
import isaacsim.core.experimental.utils.app as app_utils
import isaacsim.core.experimental.utils.stage as stage_utils
import omni.replicator.core as rep
import omni.timeline
from isaacsim.core.experimental.prims import XformPrim
from isaacsim.core.experimental.utils.prim import get_prim_at_path
from isaacsim.core.experimental.utils.stage import add_reference_to_stage, open_stage
from isaacsim.storage.native import get_assets_root_path

# Capture parameters
START_DELAY = 0.1 # Timeline duration delay before capturing the first clip
NUM_CLIPS = 2 # Number of video clips to capture with the CosmosWriter
NUM_FRAMES_PER_CLIP = 10 # Number of frames for each clip
CAPTURE_INTERVAL = 2 # Capture interval between frames (capture every N simulation steps)

# Stage and asset paths
STAGE_URL = "/Isaac/Samples/Replicator/Stage/full_warehouse_worker_and_anim_cameras.usd"
CARTER_NAV_ASSET_URL = "/Isaac/Samples/Replicator/OmniGraph/nova_carter_nav_only.usd"
CARTER_NAV_PATH = "/NavWorld/CarterNav"
CARTER_NAV_TARGET_PATH = f"{CARTER_NAV_PATH}/targetXform"
CARTER_CAMERA_PATH = f"{CARTER_NAV_PATH}/chassis_link/sensors/front_hawk/left/camera_left"
CARTER_NAV_POSITION = (-6, 4, 0)
CARTER_NAV_TARGET_POSITION = (3, 3, 0)
OUT_DIR = "_out_cosmos_warehouse"

parser = argparse.ArgumentParser()
parser.add_argument("--num-clips", type=int, default=NUM_CLIPS, help="Number of video clips to capture.")
parser.add_argument(
 "--num-frames-per-clip", type=int, default=NUM_FRAMES_PER_CLIP, help="Number of frames captured per clip."
)
parser.add_argument(
 "--capture-interval",
 type=int,
 default=CAPTURE_INTERVAL,
 help="Capture interval between frames (capture every N simulation steps).",
)
parser.add_argument(
 "--start-delay",
 type=float,
 default=START_DELAY,
 help="Timeline duration delay before capturing the first clip.",
)
args, _ = parser.parse_known_args()

def advance_timeline_by_duration(duration: float, max_updates: int = 1000) -> None:
 """Advance the simulation timeline toward the requested duration.

 The function stops early without raising if ``max_updates`` is reached before the target timeline time.

 Args:
 duration: Amount of simulation time to advance in seconds.
 max_updates: Maximum application updates to issue when the timeline stalls or advances slowly.
 """
 timeline = omni.timeline.get_timeline_interface()
 current_time = timeline.get_current_time()
 target_time = current_time + duration

 if timeline.get_end_time() < target_time:
 timeline.set_end_time(1000000)

 if not app_utils.is_playing():
 app_utils.play()

 print(f"Advancing timeline from {current_time:.4f}s to {target_time:.4f}s")
 step_count = 0
 while current_time < target_time:
 if step_count >= max_updates:
 print(f"Max updates reached: {step_count}, finishing timeline advance.")
 break

 prev_time = current_time
 app_utils.update_app()
 current_time = timeline.get_current_time()
 step_count += 1

 if step_count % 10 == 0:
 print(f"\tStep {step_count}, {current_time:.4f}s/{target_time:.4f}s")

 if current_time <= prev_time:
 print(f"Warning: Timeline did not advance at update {step_count} (time: {current_time:.4f}s).")
 print(f"Finished advancing timeline to {current_time:.4f}s (target {target_time:.4f}s) in {step_count} steps")

def run_sdg_pipeline(
 camera_path: str,
 num_clips: int,
 num_frames_per_clip: int,
 capture_interval: int,
 use_instance_id: bool = True,
 segmentation_mapping: dict[str, Any] | None = None,
) -> None:
 """Run the synthetic data generation pipeline and capture video clips.

 Args:
 camera_path: Path of the camera prim used by the render product.
 num_clips: Number of distinct video clips to write.
 num_frames_per_clip: Number of captured frames in each clip.
 capture_interval: Positive number of simulation updates between captured frames.
 use_instance_id: Whether the writer should encode segmentation by instance identifier.
 segmentation_mapping: Mapping from source semantic labels to output labels, or ``None`` to use the
 writer's default mapping.
 """
 rp = rep.create.render_product(camera_path, (640, 480))
 cosmos_writer = rep.WriterRegistry.get("CosmosWriter")
 backend = rep.backends.get("DiskBackend")
 out_dir = os.path.join(os.getcwd(), OUT_DIR)
 print(f"output_directory: {out_dir}")
 backend.initialize(output_dir=out_dir)
 cosmos_writer.initialize(
 backend=backend, use_instance_id=use_instance_id, segmentation_mapping=segmentation_mapping
 )
 cosmos_writer.attach(rp)

 # Make sure the timeline is playing
 if not app_utils.is_playing():
 app_utils.play()

 print(
 f"Starting SDG pipeline. Capturing {num_clips} clips with {num_frames_per_clip} frames each, "
 f"every {capture_interval} simulation step(s)."
 )

 for clip_index in range(num_clips):
 print(f"Starting clip {clip_index + 1}/{num_clips}")

 frames_captured_count = 0
 simulation_step_index = 0
 while frames_captured_count < num_frames_per_clip:
 print(f"Simulation step {simulation_step_index}")
 if simulation_step_index % capture_interval == 0:
 print(
 f"\t Capturing frame {frames_captured_count + 1}/{num_frames_per_clip} "
 f"for clip {clip_index + 1}"
 )
 rep.orchestrator.step(pause_timeline=False, rt_subframes=4)
 frames_captured_count += 1
 else:
 app_utils.update_app()
 simulation_step_index += 1

 print(f"Finished clip {clip_index + 1}/{num_clips}. Captured {frames_captured_count} frames")

 if clip_index < num_clips - 1:
 # Move to next clip if not the last clip
 print("Moving to next clip...")
 cosmos_writer.next_clip()

 print("Waiting to finish processing and writing the data")
 rep.orchestrator.wait_until_complete()
 print(f"Finished SDG pipeline. Captured {num_clips} clips with {num_frames_per_clip} frames each")
 app_utils.update_app(steps=3)
 cosmos_writer.detach()
 rp.destroy()
 app_utils.pause()

def run_example(
 num_clips: int,
 num_frames_per_clip: int,
 capture_interval: int,
 start_delay: float = 0.0,
 use_instance_id: bool = True,
 segmentation_mapping: dict[str, Any] | None = None,
) -> None:
 """Set up the warehouse scene and run the SDG pipeline.

 Args:
 num_clips: Number of distinct video clips to write.
 num_frames_per_clip: Number of captured frames in each clip.
 capture_interval: Positive number of simulation updates between captured frames.
 start_delay: Simulation time to advance before capturing the first frame, in seconds.
 use_instance_id: Whether the writer should encode segmentation by instance identifier.
 segmentation_mapping: Mapping from source semantic labels to output labels, or ``None`` to use the
 writer's default mapping.
 """
 assets_root_path = get_assets_root_path()
 if assets_root_path is None:
 print("Assets root path not found, exiting")
 return

 stage_path = assets_root_path + STAGE_URL
 print(f"Opening stage: '{stage_path}'")
 opened, stage = open_stage(stage_path)
 if not opened or stage is None:
 print(f"Could not open stage: '{stage_path}', exiting")
 return

 # Enable script nodes
 carb.settings.get_settings().set_bool("/app/omni.graph.scriptnode/opt_in", True)

 # Disable capture on play on the new stage, data is captured manually using the step function
 rep.orchestrator.set_capture_on_play(False)

 # Set DLSS to Quality mode (2) for best SDG results , options: 0 (Performance), 1 (Balanced), 2 (Quality), 3 (Auto)
 carb.settings.get_settings().set("rtx/post/dlss/execMode", 2)

 # Load carter nova asset with its navigation graph
 carter_url_path = assets_root_path + CARTER_NAV_ASSET_URL
 print(f"Loading carter nova asset: '{carter_url_path}' at prim path: '{CARTER_NAV_PATH}'")
 add_reference_to_stage(usd_path=carter_url_path, path=CARTER_NAV_PATH)
 XformPrim(CARTER_NAV_PATH, reset_xform_op_properties=True).set_local_poses(
 translations=[CARTER_NAV_POSITION], orientations=[(1.0, 0.0, 0.0, 0.0)]
 )

 # Set the navigation target position
 if not get_prim_at_path(CARTER_NAV_TARGET_PATH).IsValid():
 print(f"Carter navigation target prim not found at path: {CARTER_NAV_TARGET_PATH}, exiting")
 return
 XformPrim(CARTER_NAV_TARGET_PATH, reset_xform_op_properties=True).set_local_poses(
 translations=[CARTER_NAV_TARGET_POSITION], orientations=[(1.0, 0.0, 0.0, 0.0)]
 )

 # Use the carter nova front hawk camera for capturing data
 camera_prim = stage_utils.get_current_stage(backend="usd").GetPrimAtPath(CARTER_CAMERA_PATH)
 if not camera_prim.IsValid():
 print(f"Camera prim not found at path: {CARTER_CAMERA_PATH}, exiting")
 return
 # tickRate=0 forces autotrigger so the sensor cameras stay in sync with rep.orchestrator.step
 # under multi-tick rendering.
 if camera_prim.HasAttribute("omni:sensor:tickRate"):
 camera_prim.GetAttribute("omni:sensor:tickRate").Set(0.0)

 # Advance the timeline with the start delay if provided
 if start_delay is not None and start_delay > 0:
 advance_timeline_by_duration(start_delay)

 # Run the SDG pipeline
 run_sdg_pipeline(
 CARTER_CAMERA_PATH,
 num_clips,
 num_frames_per_clip,
 capture_interval,
 use_instance_id,
 segmentation_mapping,
 )

# Setup the environment and run the example
run_example(
 num_clips=args.num_clips,
 num_frames_per_clip=args.num_frames_per_clip,
 capture_interval=args.capture_interval,
 start_delay=args.start_delay,
 use_instance_id=True,
)

Script Editor

Full Script Editor Scriptimport asyncio
import os

import carb
import isaacsim.core.experimental.utils.app as app_utils
import isaacsim.core.experimental.utils.stage as stage_utils
import omni.replicator.core as rep
import omni.timeline
from isaacsim.core.experimental.prims import XformPrim
from isaacsim.core.experimental.utils.prim import get_prim_at_path
from isaacsim.core.experimental.utils.stage import add_reference_to_stage, open_stage_async
from isaacsim.storage.native import get_assets_root_path_async

# Capture parameters
START_DELAY = 0.1 # Timeline duration delay before capturing the first clip
NUM_CLIPS = 3 # Number of video clips to capture with the CosmosWriter
NUM_FRAMES_PER_CLIP = 30 # Number of frames for each clip
CAPTURE_INTERVAL = 2 # Capture interval between frames (capture every N simulation steps)

# Stage and asset paths
STAGE_URL = "/Isaac/Samples/Replicator/Stage/full_warehouse_worker_and_anim_cameras.usd"
CARTER_NAV_ASSET_URL = "/Isaac/Samples/Replicator/OmniGraph/nova_carter_nav_only.usd"
CARTER_NAV_PATH = "/NavWorld/CarterNav"
CARTER_NAV_TARGET_PATH = f"{CARTER_NAV_PATH}/targetXform"
CARTER_CAMERA_PATH = f"{CARTER_NAV_PATH}/chassis_link/sensors/front_hawk/left/camera_left"
CARTER_NAV_POSITION = (-6, 4, 0)
CARTER_NAV_TARGET_POSITION = (3, 3, 0)
OUT_DIR = "_out_cosmos_warehouse"

async def advance_timeline_by_duration_async(duration: float, max_updates: int = 1000):
 timeline = omni.timeline.get_timeline_interface()
 current_time = timeline.get_current_time()
 target_time = current_time + duration

 if timeline.get_end_time() < target_time:
 timeline.set_end_time(1000000)

 if not app_utils.is_playing():
 app_utils.play()

 print(f"Advancing timeline from {current_time:.4f}s to {target_time:.4f}s")
 step_count = 0
 while current_time < target_time:
 if step_count >= max_updates:
 print(f"Max updates reached: {step_count}, finishing timeline advance.")
 break

 prev_time = current_time
 await app_utils.update_app_async()
 current_time = timeline.get_current_time()
 step_count += 1

 if step_count % 10 == 0:
 print(f"\tStep {step_count}, {current_time:.4f}s/{target_time:.4f}s")

 if current_time <= prev_time:
 print(f"Warning: Timeline did not advance at update {step_count} (time: {current_time:.4f}s).")
 print(f"Finished advancing timeline to {current_time:.4f}s (target {target_time:.4f}s) in {step_count} steps")

async def run_sdg_pipeline_async(
 camera_path,
 num_clips,
 num_frames_per_clip,
 capture_interval,
 use_instance_id=True,
 segmentation_mapping=None,
):
 rp = rep.create.render_product(camera_path, (640, 480))
 cosmos_writer = rep.WriterRegistry.get("CosmosWriter")
 backend = rep.backends.get("DiskBackend")
 out_dir = os.path.join(os.getcwd(), OUT_DIR)
 print(f"output_directory: {out_dir}")
 backend.initialize(output_dir=out_dir)
 cosmos_writer.initialize(
 backend=backend, use_instance_id=use_instance_id, segmentation_mapping=segmentation_mapping
 )
 cosmos_writer.attach(rp)

 # Make sure the timeline is playing
 if not app_utils.is_playing():
 app_utils.play()

 print(
 f"Starting SDG pipeline. Capturing {num_clips} clips with {num_frames_per_clip} frames each, every {capture_interval} simulation step(s)."
 )

 for clip_index in range(num_clips):
 print(f"Starting clip {clip_index + 1}/{num_clips}")

 frames_captured_count = 0
 simulation_step_index = 0
 while frames_captured_count < num_frames_per_clip:
 print(f"Simulation step {simulation_step_index}")
 if simulation_step_index % capture_interval == 0:
 print(f"\t Capturing frame {frames_captured_count + 1}/{num_frames_per_clip} for clip {clip_index + 1}")
 await rep.orchestrator.step_async(pause_timeline=False, rt_subframes=4)
 frames_captured_count += 1
 else:
 await app_utils.update_app_async()
 simulation_step_index += 1

 print(f"Finished clip {clip_index + 1}/{num_clips}. Captured {frames_captured_count} frames")

 if clip_index < num_clips - 1:
 # Move to next clip if not the last clip
 print("Moving to next clip...")
 cosmos_writer.next_clip()

 print("Waiting to finish processing and writing the data")
 await rep.orchestrator.wait_until_complete_async()
 print(f"Finished SDG pipeline. Captured {num_clips} clips with {num_frames_per_clip} frames each")
 await app_utils.update_app_async(steps=3)
 cosmos_writer.detach()
 rp.destroy()
 app_utils.pause()

async def run_example_async(
 num_clips,
 num_frames_per_clip,
 capture_interval,
 start_delay=0.0,
 use_instance_id=True,
 segmentation_mapping=None,
):
 assets_root_path = await get_assets_root_path_async()
 if assets_root_path is None:
 print("Assets root path not found, exiting")
 return

 stage_path = assets_root_path + STAGE_URL
 print(f"Opening stage: '{stage_path}'")
 opened, stage = await open_stage_async(stage_path)
 if not opened or stage is None:
 print(f"Could not open stage: '{stage_path}', exiting")
 return

 # Enable script nodes
 carb.settings.get_settings().set_bool("/app/omni.graph.scriptnode/opt_in", True)

 # Disable capture on play on the new stage, data is captured manually using the step function
 rep.orchestrator.set_capture_on_play(False)

 # Set DLSS to Quality mode (2) for best SDG results (Options: 0 (Performance), 1 (Balanced), 2 (Quality), 3 (Auto)
 carb.settings.get_settings().set("rtx/post/dlss/execMode", 2)

 # Load carter nova asset with its navigation graph
 carter_url_path = assets_root_path + CARTER_NAV_ASSET_URL
 print(f"Loading carter nova asset: '{carter_url_path}' at prim path: '{CARTER_NAV_PATH}'")
 add_reference_to_stage(usd_path=carter_url_path, path=CARTER_NAV_PATH)
 XformPrim(CARTER_NAV_PATH, reset_xform_op_properties=True).set_local_poses(
 translations=[CARTER_NAV_POSITION], orientations=[(1.0, 0.0, 0.0, 0.0)]
 )

 # Set the navigation target position
 if not get_prim_at_path(CARTER_NAV_TARGET_PATH).IsValid():
 print(f"Carter navigation target prim not found at path: {CARTER_NAV_TARGET_PATH}, exiting")
 return
 XformPrim(CARTER_NAV_TARGET_PATH, reset_xform_op_properties=True).set_local_poses(
 translations=[CARTER_NAV_TARGET_POSITION], orientations=[(1.0, 0.0, 0.0, 0.0)]
 )

 # Use the carter nova front hawk camera for capturing data
 camera_prim = stage_utils.get_current_stage(backend="usd").GetPrimAtPath(CARTER_CAMERA_PATH)
 if not camera_prim.IsValid():
 print(f"Camera prim not found at path: {CARTER_CAMERA_PATH}, exiting")
 return
 # tickRate=0 forces autotrigger so the sensor cameras stay in sync with rep.orchestrator.step_async
 # under multi-tick rendering.
 if camera_prim.HasAttribute("omni:sensor:tickRate"):
 camera_prim.GetAttribute("omni:sensor:tickRate").Set(0.0)

 # Advance the timeline with the start delay if provided
 if start_delay is not None and start_delay > 0:
 await advance_timeline_by_duration_async(start_delay)

 # Run the SDG pipeline
 await run_sdg_pipeline_async(
 CARTER_CAMERA_PATH,
 num_clips,
 num_frames_per_clip,
 capture_interval,
 use_instance_id,
 segmentation_mapping,
 )

# Setup the environment and run the example
asyncio.ensure_future(
 run_example_async(
 num_clips=NUM_CLIPS,
 num_frames_per_clip=NUM_FRAMES_PER_CLIP,
 capture_interval=CAPTURE_INTERVAL,
 start_delay=START_DELAY,
 use_instance_id=True,
 )
)

Code Explanation
This tab explains how the warehouse navigation example works and how the CosmosWriter captures multi-modal data during robot movement.

Script Overview

The script simulates a Carter Nova robot navigating through a warehouse while capturing synchronized multi-modal data from its front camera. The robot moves from a starting position to a target location, and the CosmosWriter generates ground truth data for Cosmos Transfer.

Main Execution Flow# Setup the environment and run the example
run_example(
 num_clips=NUM_CLIPS,
 num_frames_per_clip=NUM_FRAMES_PER_CLIP,
 capture_interval=CAPTURE_INTERVAL,
 start_delay=START_DELAY,
 use_instance_id=True,
)

simulation_app.close()

Key Configuration Parameters

Capture Parameters
- NUM_CLIPS = 2: Generate 2 separate video clips

- NUM_FRAMES_PER_CLIP = 10: Each clip contains 10 frames

- CAPTURE_INTERVAL = 2: Capture every 2nd simulation step

- START_DELAY = 0.1: Custom delay to start capturing at a specific time

Data Capture Pipeline

The run_sdg_pipeline function orchestrates the entire capture process:

SDG Pipeline Implementationdef run_sdg_pipeline(
 camera_path, num_clips, num_frames_per_clip, capture_interval, use_instance_id=True, segmentation_mapping=None
):
 rp = rep.create.render_product(camera_path, (640, 480))
 cosmos_writer = rep.WriterRegistry.get("CosmosWriter")
 backend = rep.backends.get("DiskBackend")
 out_dir = os.path.join(os.getcwd(), f"_out_cosmos_warehouse")
 print(f"output_directory: {out_dir}")
 backend.initialize(output_dir=out_dir)
 cosmos_writer.initialize(
 backend=backend, use_instance_id=use_instance_id, segmentation_mapping=segmentation_mapping
 )
 cosmos_writer.attach(rp)

 # Make sure the timeline is playing
 timeline = omni.timeline.get_timeline_interface()
 if not app_utils.is_playing():
 app_utils.play()

 print(
 f"Starting SDG pipeline. Capturing {num_clips} clips with {num_frames_per_clip} frames each, every {capture_interval} simulation step(s)."
 )

 for clip_index in range(num_clips):
 print(f"Starting clip {clip_index + 1}/{num_clips}")

 frames_captured_count = 0
 simulation_step_index = 0
 while frames_captured_count < num_frames_per_clip:
 print(f"Simulation step {simulation_step_index}")
 if simulation_step_index % capture_interval == 0:
 print(f"\t Capturing frame {frames_captured_count + 1}/{num_frames_per_clip} for clip {clip_index + 1}")
 rep.orchestrator.step(pause_timeline=False)
 frames_captured_count += 1
 else:
 simulation_app.update()
 simulation_step_index += 1

 print(f"Finished clip {clip_index + 1}/{num_clips}. Captured {frames_captured_count} frames")

 # Move to next clip if not the last clip
 if clip_index < num_clips - 1:
 print(f"Moving to next clip...")
 cosmos_writer.next_clip()

 print("Waiting to finish processing and writing the data")
 rep.orchestrator.wait_until_complete()
 print(f"Finished SDG pipeline. Captured {num_clips} clips with {num_frames_per_clip} frames each")
 cosmos_writer.detach()
 rp.destroy()
 app_utils.pause()

Key aspects:
- The render product is created from the robot’s front camera at 640x480 resolution
- pause_timeline=False allows the robot to continue moving during capture
- The simulation advances between captures to show navigation progress

CosmosWriter Configuration

Writer Modes and ParametersThe CosmosWriter supports two segmentation modes:

- Instance ID Mode (default):

cosmos_writer.initialize(
 backend=backend, use_instance_id=use_instance_id, segmentation_mapping=segmentation_mapping
)

- Semantic Segmentation Mode:

segmentation_mapping = {
 "floor": [255, 0, 0, 255], # Red
 "wall": [0, 255, 0, 255], # Green
 "rack": [0, 0, 255, 255], # Blue
}

# Note: This overrides instance ID mode and requires semantic annotations
cosmos_writer.initialize(backend=backend, segmentation_mapping=segmentation_mapping)

Timeline Management

The script uses a helper function to advance the timeline before starting capture:

Timeline Advancementdef advance_timeline_by_duration(duration: float, max_updates: int = 1000):
 timeline = omni.timeline.get_timeline_interface()
 current_time = timeline.get_current_time()
 target_time = current_time + duration

 if timeline.get_end_time() < target_time:
 timeline.set_end_time(1000000)

 if not app_utils.is_playing():
 app_utils.play()

 print(f"Advancing timeline from {current_time:.4f}s to {target_time:.4f}s")
 step_count = 0
 while current_time < target_time:
 if step_count >= max_updates:
 print(f"Max updates reached: {step_count}, finishing timeline advance.")
 break

 prev_time = current_time
 simulation_app.update()
 current_time = timeline.get_current_time()
 step_count += 1

 if step_count % 10 == 0:
 print(f"\tStep {step_count}, {current_time:.4f}s/{target_time:.4f}s")

 if current_time <= prev_time:
 print(f"Warning: Timeline did not advance at update {step_count} (time: {current_time:.4f}s).")
 print(f"Finished advancing timeline to {current_time:.4f}s (target {target_time:.4f}s) in {step_count} steps")

## Output Structure#

After running the script, an output folder (e.g., _out_cosmos_warehouse) is created containing organized multi-modal data optimized for Cosmos Transfer and other foundation model training pipelines. Each clip represents a continuous sequence of frames captured during robot navigation:

_out_cosmos_warehouse/
 clip_0000/ # First clip sequence
 rgb/ # Standard color images
 rgb_0000.png, rgb_0001.png, ...
 depth/ # Colorized depth visualization
 depth_0000.png, depth_0001.png, ...
 segmentation/ # Instance/semantic masks
 segmentation_0000.png, segmentation_0001.png, ...
 shaded_seg/ # Segmentation with realistic shading
 shaded_seg_0000.png, shaded_seg_0001.png, ...
 edges/ # Canny edge detection results
 edges_0000.png, edges_0001.png, ...
 rgb.mp4 # Combined RGB video
 depth.mp4 # Combined depth video
 segmentation.mp4 # Combined segmentation video
 shaded_seg.mp4 # Combined shaded segmentation video
 edges.mp4 # Combined edges video
 clip_0001/ # Next clip sequence

What Each Modality Provides:

- RGB (rgb.mp4): The visual input video used with Cosmos Transfer’s vis control branch for preserving lighting and camera properties

- Depth (depth.mp4): 3D spatial information used with the depth control branch to maintain perspective and spatial relationships

- Segmentation (segmentation.mp4): Instance or semantic masks used with the seg control branch for object-level transformations

- Shaded Segmentation (shaded_seg.mp4): Combines segmentation with realistic shading for enhanced visual coherence

- Edges (edges.mp4): Structural boundaries used with the edge control branch to preserve object shapes while allowing material and lighting changes

These MP4 files can be directly passed to Cosmos Transfer as control inputs. The PNG sequences are provided for frame-level inspection or custom processing pipelines.

## Advanced Usage#

Custom Segmentation Colors:

Map specific semantic labels to custom colors when you need consistent class identification across datasets. Use this when training models that require specific object classes to maintain the same color/ID across all training data, ensuring Cosmos Transfer preserves class relationships.

segmentation_mapping = {
 "floor": [255, 0, 0, 255], # Red
 "wall": [0, 255, 0, 255], # Green
 "rack": [0, 0, 255, 255], # Blue
}

# Note: This overrides instance ID mode and requires semantic annotations
cosmos_writer.initialize(backend=backend, segmentation_mapping=segmentation_mapping)

Edge Detection Tuning:

Adjust Canny edge detection parameters for the hysteresis procedure when generating edge maps. The Canny algorithm uses two thresholds:

- Low threshold: Edges with gradient magnitude above this value are considered as potential edges

- High threshold: Edges with gradient magnitude above this value are definitely edges

Lower threshold values detect more edges (including noise), while higher values produce cleaner output with only strong edges. Values typically range from 10-200.

cosmos_writer.initialize(
 backend=backend,
 use_instance_id=True,
 canny_threshold_low=10, # Low threshold for hysteresis
 canny_threshold_high=100, # High threshold for hysteresis
)

## Using Data with Cosmos Transfer#

The generated data can be used with Cosmos Transfer to create high-quality visual simulations. This enables sim-to-real transfer where synthetic scenes are transformed into photorealistic environments while preserving robot motions and scene structure.

For real-world examples of this workflow, see the Cosmos Cookbook Robotics Gallery, which demonstrates:

- Edge-only control: Transform simulation videos into diverse kitchen styles (white cabinets, red cabinets, wood tones) and robot materials (plastic, metal, gold) while preserving exact robot motions

- Multi-control: Combine depth, edge, and segmentation controls for precise scene manipulation

Here’s how the modalities map to Transfer’s control branches:

Basic Single Control Example:

{
 "prompt": "A modern warehouse with autonomous robots...",
 "input_video_path": "_out_cosmos_warehouse/clip_0000/rgb.mp4",
 "edge": {
 "control_weight": 1.0
 }
}

Multi-Modal Control Example:

{
 "prompt": "High-quality warehouse simulation...",
 "input_video_path": "_out_cosmos_warehouse/clip_0000/rgb.mp4",
 "vis": {"control_weight": 0.25},
 "edge": {"control_weight": 0.25},
 "depth": {
 "input_control": "_out_cosmos_warehouse/clip_0000/depth.mp4",
 "control_weight": 0.25
 },
 "seg": {
 "input_control": "_out_cosmos_warehouse/clip_0000/segmentation.mp4",
 "control_weight": 0.25
 }
}

Key Considerations:

- Control Weights: Values 0.0-1.0 control adherence (higher = stricter following, lower = more creative freedom)

- Automatic Normalization: If total weights > 1.0, they’re normalized automatically

- Prompting: Focus on single scenes with rich descriptions; avoid camera control instructions

- Safety: Human faces are automatically blurred by Cosmos Guardrail

For advanced features like spatiotemporal control maps and prompt upsampling, refer to the Cosmos Transfer documentation.

## Summary#

This tutorial demonstrated using the CosmosWriter to generate synchronized multi-modal data from a robot navigating a warehouse. The output provides ground truth for Cosmos Transfer to create high-quality visual simulations for physical AI applications.

Next Steps:

- Explore your output: Navigate to the generated output folder (e.g., _out_cosmos_warehouse) to inspect the RGB, depth, segmentation, and edge data

- Use with Cosmos Transfer: Pass the generated MP4 files to Cosmos Transfer1 or Transfer2.5 using the JSON configuration examples above

- See real examples: Visit the Cosmos Cookbook Robotics Gallery for examples of sim-to-real transformations using similar data

- Customize for your use case: Adjust capture parameters, segmentation mappings, and edge detection thresholds to optimize for your specific training pipeline

 On this page
