cmake_minimum_required(VERSION 3.15)

project(MyDjinniLibraryTest CXX)

find_package(Catch2 MODULE REQUIRED)

add_executable(MyDjinniLibraryTest
    exampleTest.cpp
)

target_link_libraries(MyDjinniLibraryTest PUBLIC
        Catch2::Catch2
        MyDjinniLibraryCore
        )

add_test(MyDjinniLibraryTest MyDjinniLibraryTest)

