cmake_minimum_required(VERSION 3.8)
project(anymal_b_simple_description)

# Find dependencies
find_package(ament_cmake REQUIRED)

# Install directories
install(DIRECTORY config launch meshes urdf
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
