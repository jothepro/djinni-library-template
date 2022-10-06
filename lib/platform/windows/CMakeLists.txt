
project(MyDjinniLibraryWindows CXX)

set(DJINNI_WITH_CPPCLI ON CACHE INTERNAL "")

if(NOT djinni-support-lib_POPULATED)
    FetchContent_Populate(djinni-support-lib)
    add_subdirectory(${djinni-support-lib_SOURCE_DIR} ${djinni-support-lib_BINARY_DIR} EXCLUDE_FROM_ALL)
endif()

add_djinni_library(MyDjinniLibrary SHARED
    IDL ../../my_djinni_library.djinni
    LANGUAGES CPPCLI
    NAMESPACE
        My::DjinniLibrary
)

target_link_libraries(MyDjinniLibrary PUBLIC MyDjinniLibraryCore)

set_target_properties(MyDjinniLibrary PROPERTIES
    COMMON_LANGUAGE_RUNTIME "netcore"
    DOTNET_TARGET_FRAMEWORK "net6.0"
    COMPILE_FLAGS "/EHa"
    VS_GLOBAL_CLRSupport "netcore"
)

string(REPLACE "/RTC1" "" CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}")

# This is a workaround because I was not able to link a shared djinni-support-lib built for C++/CLI & .NET 6
# see https://github.com/cross-language-cpp/djinni-support-lib/pull/33
target_sources(MyDjinniLibrary PUBLIC ${djinni-support-lib_SOURCE_DIR}/djinni/cppcli/WrapperCache.cpp ${djinni-support-lib_SOURCE_DIR}/djinni/cppcli/Error.cpp)
target_include_directories(MyDjinniLibrary PRIVATE ${djinni-support-lib_SOURCE_DIR})

target_include_directories(MyDjinniLibrary PUBLIC djinni-support-lib)
