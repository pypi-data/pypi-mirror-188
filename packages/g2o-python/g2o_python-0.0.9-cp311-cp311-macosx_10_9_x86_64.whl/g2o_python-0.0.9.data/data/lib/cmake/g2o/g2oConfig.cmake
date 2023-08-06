include(CMakeFindDependencyMacro)

if(G2O_USE_OPENGL)
  find_dependency(OpenGL)
endif()
find_dependency(Eigen3)

include("${CMAKE_CURRENT_LIST_DIR}/g2oTargets.cmake")
