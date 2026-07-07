#ifndef LALA_GRAPHICS_HPP
#define LALA_GRAPHICS_HPP

#include "raylib.h"
#include <string>

namespace lala {
namespace graphics {

    inline void window(int width, int height, const std::string& title) {
        InitWindow(width, height, title.c_str());
        SetTargetFPS(60);
    }

    inline void clear(Color color = RAYWHITE) {
        ClearBackground(color);
    }

    inline void circle(int x, int y, float radius, Color color) {
        DrawCircle(x, y, radius, color);
    }

    inline void rectangle(int x, int y, int width, int height, Color color) {
        DrawRectangle(x, y, width, height, color);
    }

    inline void text(const std::string& text, int x, int y, int size, Color color) {
        DrawText(text.c_str(), x, y, size, color);
    }

} // namespace graphics
} // namespace lala

#endif
