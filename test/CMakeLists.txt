cmake_minimum_required(VERSION 3.15)

project(MyDjinniLibraryTest)

find_package(Catch2 MODULE REQUIRED)

add_executable(MyDjinniLibraryTest
    exampleTest.cpp
)

target_link_libraries(MyDjinniLibraryTest
        Catch2::Catch2
        My::Example::MyDjinniLibrary
        )

add_test(MyDjinniLibraryTest MyDjinniLibraryTest)

target_compile_features(MyDjinniLibraryTest PRIVATE cxx_std_17)