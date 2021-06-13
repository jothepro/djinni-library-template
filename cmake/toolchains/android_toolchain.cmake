set(ANDROID_PLATFORM 28)
set(ANDROID_ABI $ENV{ANDROID_ABI})
include($ENV{ANDROID_NDK}/build/cmake/android.toolchain.cmake)
