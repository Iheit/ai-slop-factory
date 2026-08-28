#include "ai_slop/Log.hpp"

#include <iostream>

namespace ai_slop::log {

void write(Level level, std::string_view message) {
    const char* prefix = "[INFO]";
    switch (level) {
    case Level::Info:
        prefix = "[INFO]";
        break;
    case Level::Warning:
        prefix = "[WARN]";
        break;
    case Level::Error:
        prefix = "[ERROR]";
        break;
    }

    std::ostream& stream = level == Level::Error ? std::cerr : std::cout;
    stream << prefix << ' ' << message << '\n';
}

void info(std::string_view message) { write(Level::Info, message); }
void warning(std::string_view message) { write(Level::Warning, message); }
void error(std::string_view message) { write(Level::Error, message); }

} // namespace ai_slop::log
