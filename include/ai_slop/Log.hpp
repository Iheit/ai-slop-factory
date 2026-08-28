#pragma once

#include <string_view>

namespace ai_slop::log {

enum class Level {
    Info,
    Warning,
    Error,
};

void write(Level level, std::string_view message);
void info(std::string_view message);
void warning(std::string_view message);
void error(std::string_view message);

} // namespace ai_slop::log
