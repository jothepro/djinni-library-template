cmake_minimum_required(VERSION 3.15)

djinni_project(MyDjinniLibraryTest)

find_package(Catch2 MODULE REQUIRED)

add_executable(MyDjinniLibraryTest
    exampleTest.cpp
)

target_link_libraries(MyDjinniLibraryTest PUBLIC
        Catch2::Catch2
        MyDjinniLibrary::MyDjinniLibrary
        )

target_compile_features(MyDjinniLibraryTest PRIVATE cxx_std_17)

if(DARWIN)
    # conan has installed all thirdparty dependencise (including thirdparty frameworks)
    # to `test/lib` in the `imports` step. This allows the test to find these dependencies, which are only referenced
    # by `@rpath` in the binary.
    add_custom_command(TARGET MyDjinniLibraryTest
            POST_BUILD COMMAND
            ${CMAKE_INSTALL_NAME_TOOL} -add_rpath "@executable_path/../lib"
            $<TARGET_FILE:MyDjinniLibraryTest> || true)
endif()

add_test(MyDjinniLibraryTest MyDjinniLibraryTest)

