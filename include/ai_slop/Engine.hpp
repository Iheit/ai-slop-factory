#pragma once

#include <chrono>
#include <cstdint>
#include <memory>

namespace ai_slop {

class Window;

class Engine {
public:
    struct Config {
        const char* title = "AI Slop Engine";
        int width = 1280;
        int height = 720;
        bool vsync = true;
    };

    Engine();
    explicit Engine(Config config);
    ~Engine();

    Engine(const Engine&) = delete;
    Engine& operator=(const Engine&) = delete;

    bool initialize();
    void run();
    void stop();
    bool is_running() const noexcept;

private:
    class Impl;
    std::unique_ptr<Impl> impl_;
};

} // namespace ai_slop
