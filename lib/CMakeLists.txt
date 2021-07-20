cmake_minimum_required(VERSION 3.15)
include(FetchContent)

project(MyDjinniLibraryCore CXX)

add_djinni_library(MyDjinniLibraryCore STATIC
    IDL my_djinni_library.djinni
    LANGUAGES CPP
    NAMESPACE 
        My::DjinniLibrary
    SOURCES
        src/example.cpp
)

set_target_properties(MyDjinniLibraryCore PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED true
    CXX_EXTENSIONS false
    POSITION_INDEPENDENT_CODE TRUE
)

target_compile_features(MyDjinniLibraryCore PUBLIC cxx_std_17)

FetchContent_Declare(djinni-support-lib
    GIT_REPOSITORY https://github.com/cross-language-cpp/djinni-support-lib.git
    GIT_TAG v1.0.0)
set(DJINNI_BUILD_TESTING OFF CACHE INTERNAL "")

set(DARWIN_LIST Darwin iOS)
if(CMAKE_SYSTEM_NAME IN_LIST DARWIN_LIST)
    add_subdirectory(platform/darwin)
elseif(CMAKE_SYSTEM_NAME STREQUAL "Windows")
    add_subdirectory(platform/windows)
elseif(ANDROID)
    add_subdirectory(platform/android)
else()
    add_subdirectory(platform/linux)
endif()