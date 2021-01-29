# vSLAM-Cozmo-SDK-Performance
Repository with eval python file to store the ground truth IMU data and RGB images from Anki COZMO
## Objective
To evaluate the performance of feature-based vSLAM algorithms i.e., ORB-SLAM2 and OpenVSLAM on different generic datasets like TUM RGB-D, EuRoC, and ETH3D, by comparing them based on Absolute Trajectory Error (ATE) and Relative Pose Error (RPE) for different image sequences and lighting conditions. Loss in tracking, tracking times, and efficiency of relocalization is also evaluated.

The vSLAM algorithms are evaluated on mobile robot, COZMO, by navigating it in a custom-built maze environment under different lighting conditions.
