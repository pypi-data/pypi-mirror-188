# Findk2
# ------
#
# Finds the k2 library
#
# This will define the following variables:
#
#   K2_FOUND        -- True if the system has the k2 library
#   K2_INCLUDE_DIRS -- The include directories for k2
#   K2_LIBRARIES    -- Libraries to link against
#   K2_CXX_FLAGS -- Additional (required) compiler flags
#   K2_CUDA_FLAGS -- CUDA flags used to build k2
#   K2_WITH_CUDA -- true if k2 was compiled with CUDA; false if k2 was compiled
#                   with CPU.
#   K2_CUDA_VERSION -- If set, it is the CUDA version that was used to compile k2
#   K2_TORCH_VERSION_MAJOR  -- The major version of PyTorch used to compile k2
#   K2_TORCH_VERSION_MINOR  -- The minor version of PyTorch used to compile k2
#   K2_VERSION -- The version of k2
#   K2_GIT_SHA1 -- git commit ID of this version
#   K2_GIT_DATE -- commit date of this version
#
# and the following imported targets:
#
#   k2_torch_api, k2_log, k2context, k2fsa

# This file is modified from pytorch/cmake/TorchConfig.cmake.in

set(K2_CXX_FLAGS " -D_GLIBCXX_USE_CXX11_ABI=0 -Wno-unused-variable  -Wno-strict-overflow ")
set(K2_CUDA_FLAGS " -Wno-deprecated-gpu-targets   -lineinfo --expt-extended-lambda -use_fast_math -Xptxas=-w  --expt-extended-lambda -gencode arch=compute_35,code=sm_35  -lineinfo --expt-extended-lambda -use_fast_math -Xptxas=-w  --expt-extended-lambda -gencode arch=compute_50,code=sm_50  -lineinfo --expt-extended-lambda -use_fast_math -Xptxas=-w  --expt-extended-lambda -gencode arch=compute_60,code=sm_60  -lineinfo --expt-extended-lambda -use_fast_math -Xptxas=-w  --expt-extended-lambda -gencode arch=compute_61,code=sm_61  -lineinfo --expt-extended-lambda -use_fast_math -Xptxas=-w  --expt-extended-lambda -gencode arch=compute_70,code=sm_70  -lineinfo --expt-extended-lambda -use_fast_math -Xptxas=-w  --expt-extended-lambda -gencode arch=compute_75,code=sm_75  -lineinfo --expt-extended-lambda -use_fast_math -Xptxas=-w  --expt-extended-lambda -gencode arch=compute_80,code=sm_80  -lineinfo --expt-extended-lambda -use_fast_math -Xptxas=-w  --expt-extended-lambda -gencode arch=compute_86,code=sm_86 -DONNX_NAMESPACE=onnx_c2 -gencode arch=compute_35,code=sm_35 -gencode arch=compute_50,code=sm_50 -gencode arch=compute_52,code=sm_52 -gencode arch=compute_60,code=sm_60 -gencode arch=compute_61,code=sm_61 -gencode arch=compute_70,code=sm_70 -gencode arch=compute_75,code=sm_75 -gencode arch=compute_80,code=sm_80 -gencode arch=compute_86,code=sm_86 -gencode arch=compute_86,code=compute_86 -Xcudafe --diag_suppress=cc_clobber_ignored,--diag_suppress=integer_sign_change,--diag_suppress=useless_using_declaration,--diag_suppress=set_but_not_used,--diag_suppress=field_without_dll_interface,--diag_suppress=base_class_has_different_dll_interface,--diag_suppress=dll_interface_conflict_none_assumed,--diag_suppress=dll_interface_conflict_dllexport_assumed,--diag_suppress=implicit_return_from_non_void_function,--diag_suppress=unsigned_compare_with_zero,--diag_suppress=declared_but_not_referenced,--diag_suppress=bad_friend_decl --expt-relaxed-constexpr --expt-extended-lambda -D_GLIBCXX_USE_CXX11_ABI=0 --compiler-options -Wall  --compiler-options -Wno-strict-overflow  --compiler-options -Wno-unknown-pragmas ")
set(K2_WITH_CUDA ON)
set(K2_CUDA_VERSION 11.7)
set(K2_TORCH_VERSION_MAJOR 1)
set(K2_TORCH_VERSION_MINOR 13)
set(K2_VERSION 1.23.4)
set(K2_GIT_SHA1 62e404dd3f3a811d73e424199b3408e309c06e1a)
set(K2_GIT_DATE "Mon Jan 30 02:26:16 2023")

if(DEFINED ENV{K2_INSTALL_PREFIX})
  set(K2_INSTALL_PREFIX $ENV{K2_INSTALL_PREFIX})
else()
  # Assume we are in <install-prefix>/share/cmake/k2/k2Config.cmake
  get_filename_component(CMAKE_CURRENT_LIST_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)
  get_filename_component(K2_INSTALL_PREFIX "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)
endif()

set(K2_INCLUDE_DIRS ${K2_INSTALL_PREFIX}/include)

set(K2_LIBRARIES k2_torch_api k2_torch k2_log k2context k2fsa)

foreach(lib IN LISTS K2_LIBRARIES)
  find_library(location_${lib} ${lib}
    PATHS
    "${K2_INSTALL_PREFIX}/lib"
    "${K2_INSTALL_PREFIX}/lib64"
  )

  if(NOT MSVC)
    add_library(${lib} SHARED IMPORTED)
  else()
    add_library(${lib} STATIC IMPORTED)
  endif()

  set_target_properties(${lib} PROPERTIES
      INTERFACE_INCLUDE_DIRECTORIES "${K2_INCLUDE_DIRS}"
      IMPORTED_LOCATION "${location_${lib}}"
      CXX_STANDARD 14
  )

  set_property(TARGET ${lib} PROPERTY INTERFACE_COMPILE_OPTIONS  -D_GLIBCXX_USE_CXX11_ABI=0 -Wno-unused-variable  -Wno-strict-overflow  -DHAVE_K2_TORCH_API_H=1)
endforeach()

include(FindPackageHandleStandardArgs)

find_package_handle_standard_args(k2 DEFAULT_MSG
  location_k2_torch_api
  location_k2_torch
  location_k2_log
  location_k2context
  location_k2fsa
)
