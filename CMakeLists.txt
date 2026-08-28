cmake_minimum_required(VERSION 3.20)

project(AISlopEngine VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(AI_SLOP_BUILD_SANDBOX "Build the Phase 1 sandbox application" ON)

add_library(ai_slop_engine
    src/Engine.cpp
    src/Log.cpp
    src/Window.cpp
)

target_include_directories(ai_slop_engine
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_compile_features(ai_slop_engine PUBLIC cxx_std_17)

if(MSVC)
    target_compile_options(ai_slop_engine PRIVATE /W4 /permissive-)
else()
    target_compile_options(ai_slop_engine PRIVATE -Wall -Wextra -Wpedantic)
endif()

if(AI_SLOP_BUILD_SANDBOX)
    add_executable(ai_slop_sandbox
        sandbox/main.cpp
    )
    target_link_libraries(ai_slop_sandbox PRIVATE ai_slop_engine)
endif()

enable_testing()
add_test(NAME engine_smoke_test COMMAND ai_slop_sandbox --smoke-test)
