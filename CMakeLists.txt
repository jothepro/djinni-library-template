cmake_minimum_required(VERSION 3.15)
# Appends the cmake/modules path to MAKE_MODULE_PATH variable.
set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules ${CMAKE_MODULE_PATH})

include(GetVersion)
include(djinni-cmake/Djinni)
get_version(PROJECT_VERSION)

project(MyDjinniLibrary 
    LANGUAGES CXX
    VERSION ${PROJECT_VERSION})

add_subdirectory(lib)

include(CTest)
if(BUILD_TESTING)
    set(CMAKE_CTEST_ARGUMENTS "--verbose")
    add_subdirectory(test)
endif()
