#include "ai_slop/Engine.hpp"

#include "ai_slop/Log.hpp"
#include "ai_slop/Window.hpp"

#include <SDL.h>

#include <chrono>
#include <thread>

namespace ai_slop {

class Engine::Impl {
public:
    explicit Impl(Config config_in) : config(config_in) {}

    Config config;
    std::unique_ptr<Window> window;
    bool running = false;
};

Engine::Engine(Config config) : impl_(std::make_unique<Impl>(config)) {}

Engine::~Engine() {
    stop();
    if (SDL_WasInit(SDL_INIT_VIDEO) != 0) {
        SDL_Quit();
    }
}

bool Engine::initialize() {
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        log::error(SDL_GetError());
        return false;
    }

    impl_->window = std::make_unique<Window>(impl_->config.title, impl_->config.width,
                                              impl_->config.height, impl_->config.vsync);
    if (!impl_->window->create()) {
        log::error("Failed to create the engine window.");
        return false;
    }

    log::info("AI Slop Engine initialized.");
    return true;
}

void Engine::run() {
    if (impl_->window == nullptr) {
        log::error("Engine::run() called before initialize().");
        return;
    }

    impl_->running = true;
    auto previous = std::chrono::steady_clock::now();

    while (impl_->running && !impl_->window->should_close()) {
        const auto now = std::chrono::steady_clock::now();
        [[maybe_unused]] const std::chrono::duration<float> delta = now - previous;
        previous = now;

        impl_->window->poll_events();
        impl_->window->present();
    }

    impl_->running = false;
}

void Engine::stop() {
    impl_->running = false;
}

bool Engine::is_running() const noexcept {
    return impl_->running;
}

} // namespace ai_slop
