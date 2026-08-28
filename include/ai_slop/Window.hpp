#pragma once

#include <string>

namespace ai_slop {

class Window {
public:
    Window(std::string title, int width, int height, bool vsync);
    ~Window();

    Window(const Window&) = delete;
    Window& operator=(const Window&) = delete;

    bool create();
    void poll_events();
    void present();
    bool should_close() const noexcept;

private:
    struct Impl;
    Impl* impl_;
};

} // namespace ai_slop
