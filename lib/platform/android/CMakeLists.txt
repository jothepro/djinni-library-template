
project(MyDjinniLibraryAndroid CXX)

set(DJINNI_WITH_JNI ON CACHE INTERNAL "")

if(NOT djinni-support-lib_POPULATED)
    FetchContent_Populate(djinni-support-lib)
    add_subdirectory(${djinni-support-lib_SOURCE_DIR} ${djinni-support-lib_BINARY_DIR} EXCLUDE_FROM_ALL)
endif()

add_djinni_library(MyDjinniLibrary SHARED
    IDL ../../my_djinni_library.djinni
    LANGUAGES JAVA
    NAMESPACE
        My::DjinniLibrary
)

target_link_libraries(MyDjinniLibrary PRIVATE MyDjinniLibraryCore djinni-support-lib::djinni-support-lib)