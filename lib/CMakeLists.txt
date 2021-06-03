cmake_minimum_required(VERSION 3.15)
include(FetchContent)

djinni_project(MyDjinniLibrary)

add_djinni_library(MyDjinniLibrary SHARED
    IDL my_djinni_library.djinni
    NAMESPACE 
        My::DjinniLibrary
    SOURCES
        src/example.cpp
)

add_library(My::Example::MyDjinniLibrary ALIAS MyDjinniLibrary)

djinni_target_link_support_lib(MyDjinniLibrary v1.0.0)



