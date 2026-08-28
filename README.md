# AI Slop Engine

A small C++ game engine built incrementally. Phase 1 establishes the application loop, SDL2 window layer, logging, CMake build, sandbox executable, and automated smoke testing.

## Build

Install SDL2 development files, then:

```sh
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```

Run the sandbox with:

```sh
./build/ai_slop_sandbox
```

## Phase 1

- C++17 engine library
- SDL2 window and event handling
- Basic frame loop
- Minimal logging API
- Sandbox executable
- Headless smoke test
- GitHub Actions build/test workflow
