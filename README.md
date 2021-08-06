# Grasping_Franka
Robotic grasping with Franka Emika and RealSense D435 and penumatic gripper with soft adaptive fingers.

Pull this repository under https://github.com/bionicdl-sustech/ME336-2021Spring, the path should be "./ME336-2021Spring/Grasping_Franka".

Object detection method is based on color difference, which is a white object on a black background. Can only grasp one object a time.

Location transformation method is based on 2D location transformation (x, y), while the gripper approach the platform as close as possible (z). Grasping pose is perpendicular toward the platform (3.14, 0, alpha)

Grasping can be finished automatically for multiple times, human labor only need to participate in finger and object replacement during the experiment.
