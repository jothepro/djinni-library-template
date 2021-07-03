#include "My/DjinniLibrary/example.hpp"
#include "My/DjinniLibrary/native.hpp"

using namespace My::DjinniLibrary;

std::string Example::hello_from_cpp() {
    return "test";
}

std::string Example::hello_from_native(const std::shared_ptr<Native> & from) {
    return from->hello_from_native();
}