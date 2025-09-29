#!/usr/bin/env env_isaaclab
"""
RoboHabilis.py
------------------
Thin wrapper around pre-trained pull object policy for the RoboHabilis Robot
Extends 'Policy controller' with:


Author: Enrique de Antonio
"""

from pathlib import Path

import numpy as np

from controllers.policy_controller import PolicyController

from isaaclab.utils.math import subtract_frame_transforms

class RHPullObjectPolicy(PolicyController):
    
    
    def __init__(self) -> None:
        super().__init__()
        self.dof_names = [
            # left arm
            "l_shoulder_pan_joint"
            "l_shoulder_lift_joint"
            "l_elbow_joint"
            "l_wrist_1_joint"
            "l_wrist_2_joint"
            "l_wrist_3_joint"
            "l_left_finger_joint"
            "l_right_finger_joint"
        ]
        repo_root = Path(__file__).resolve().parents[3]
        model_dir = repo_root / "scripts/Sim2Real/PreTrainedModel"
        self.load_policy(
            model_dir / "policy.pt",
            model_dir / "env.yaml"
        )
        self._action_scale = 0.5 
        self._previous_action=np.zeros(8)
        self._policy_counter = 0
        self.target_command = np.zeros(7)

        self.has_joint_data = False
        self.has_target_data = False
        self.current_joint_positions = np.zeros(8)
        self.current_joint_velocities = np.zeros(8)
    def update_command(self, command: np.ndarray) -> None:
        self.target_command = command
        self.has_target_data = True

    def update_joint_state(self, position, velocity) -> None:
        self.current_joint_positions = np.array(position[:self.num_joints], dtype=np.float32)
        self.current_joint_velocities = np.array(velocity[:self.num_joints], dtype=np.float32)
        self.has_joint_data = True

    def _compute_observation(self, tool_position: np.ndarray, object_position: np.ndarray, root_state: np.ndarray) -> np.ndarray:
        
        obs = np.zeros(37)
        obs[:8] = self.current_joint_position - self.default_pos
        obs[8:16] = self.current_joint_velocities
        obs[16:19] = subtract_frame_transforms(
            root_state[:, :3], root_state[:, 3:7], tool_position
        )
        obs[19:22] = subtract_frame_transforms(
            root_state[:, :3], root_state[:, 3:7], object_position
        )
        obs[22:29] = self.target_command
        obs[29:37] = self._previous_action
    
    def forward(self, dt: float, tool_position, object_position, root_state) -> np.ndarray:
        
        if not self.has_joint_data:
            return None

        if self._policy_counter % self._decimation == 0:
            obs = self._compute_observation(tool_position, object_position, root_state)
            if obs is None:
                return None
            self.action = self._compute_action(obs)
            self._previous_action = self.action.copy()

            # Debug Logging (commented out)
            print("\n=== Policy Step ===")
            print("--- Observation ---")
            print(f"{'Δ Joint Positions:':<20} {np.round(obs[:8], 4)}")
            print(f"{'Joint Velocities:':<20} {np.round(obs[8:16], 4)}")
            print(f"{'Tool Position:':<20} {np.round(obs[16:19], 4)}")
            print(f"{'Object Position:':<20} {np.round(obs[19:22], 4)}\n")
            print("--- Action ---")
            print(f"{'Raw Action:':<20} {np.round(self.action, 4)}")
            processed_action = self.default_pos + (self.action * self._action_scale)
            print(f"{'Processed Action:':<20} {np.round(processed_action, 4)}")

        joint_positions = self.default_pos + (self.action * self._action_scale)
        self._policy_counter += 1
        return joint_positions
    
