cmake_minimum_required(VERSION 3.15)

project(MyDjinniLibraryTest CXX)

find_package(Catch2 REQUIRED)

add_executable(MyDjinniLibraryTest
    exampleTest.cpp
)

target_link_libraries(MyDjinniLibraryTest
    PUBLIC
        Catch2::Catch2
        MyDjinniLibraryCore
)

target_compile_features(MyDjinniLibraryTest PRIVATE cxx_std_17)

add_test(MyDjinniLibraryTest MyDjinniLibraryTest)
