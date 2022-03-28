#define CATCH_CONFIG_MAIN
#include <catch2/catch.hpp>
#include <memory>
#include "My/DjinniLibrary/example.hpp"

using namespace My::DjinniLibrary;

SCENARIO("MyDjinniLibrary testing", "[test]") {
    WHEN("calling Example::helloFromCpp()") {
        auto result = Example::hello_from_cpp();
        THEN("the result should be: 'hello from cpp'") {
            REQUIRE(result == "hello from cpp");
        }
    }
}
