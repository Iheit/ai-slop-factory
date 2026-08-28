#include "ai_slop/Engine.hpp"
#include "ai_slop/Log.hpp"

#include <string_view>

int main(int argc, char** argv) {
    const bool smoke_test = argc > 1 && std::string_view(argv[1]) == "--smoke-test";

    ai_slop::Engine engine({"AI Slop Engine - Phase 1", 1280, 720, true});
    if (!engine.initialize()) {
        ai_slop::log::error("Sandbox failed to initialize the engine.");
        return 1;
    }

    if (smoke_test) {
        ai_slop::log::info("Engine smoke test passed initialization.");
        return 0;
    }

    engine.run();
    return 0;
}
