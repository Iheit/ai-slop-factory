#include "ai_slop/Window.hpp"

#include "ai_slop/Log.hpp"

#include <SDL.h>

namespace ai_slop {

struct Window::Impl {
    SDL_Window* window = nullptr;
    SDL_Renderer* renderer = nullptr;
    bool close_requested = false;
};

Window::Window(std::string title, int width, int height, bool vsync)
    : impl_(new Impl{}) {
    impl_->window = SDL_CreateWindow(title.c_str(), SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                                     width, height, SDL_WINDOW_SHOWN);
    if (impl_->window == nullptr) {
        log::error(SDL_GetError());
        return;
    }

    const Uint32 renderer_flags = SDL_RENDERER_ACCELERATED | (vsync ? SDL_RENDERER_PRESENTVSYNC : 0U);
    impl_->renderer = SDL_CreateRenderer(impl_->window, -1, renderer_flags);
    if (impl_->renderer == nullptr) {
        log::warning("Hardware renderer unavailable; falling back to software rendering.");
        impl_->renderer = SDL_CreateRenderer(impl_->window, -1, SDL_RENDERER_SOFTWARE);
    }
}

Window::~Window() {
    if (impl_ != nullptr) {
        SDL_DestroyRenderer(impl_->renderer);
        SDL_DestroyWindow(impl_->window);
        delete impl_;
    }
}

bool Window::create() {
    return impl_ != nullptr && impl_->window != nullptr && impl_->renderer != nullptr;
}

void Window::poll_events() {
    SDL_Event event{};
    while (SDL_PollEvent(&event) != 0) {
        if (event.type == SDL_QUIT) {
            impl_->close_requested = true;
        }
    }
}

void Window::present() {
    if (impl_->renderer == nullptr) {
        return;
    }
    SDL_SetRenderDrawColor(impl_->renderer, 20, 22, 28, 255);
    SDL_RenderClear(impl_->renderer);
    SDL_RenderPresent(impl_->renderer);
}

bool Window::should_close() const noexcept {
    return impl_ == nullptr || impl_->close_requested;
}

} // namespace ai_slop
