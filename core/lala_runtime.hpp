#ifndef LALA_RUNTIME_HPP
#define LALA_RUNTIME_HPP

#include <iostream>
#include <string>
#include "raylib.h"

namespace lala_runtime {
    // Window Management
    inline void create_window(int width, int height, const std::string& title) {
        InitWindow(width, height, title.c_str());
        SetTargetFPS(60);
    }
    
    // Draw Functions
    inline void draw_circle(int x, int y, float radius, Color color) {
        DrawCircle(x, y, radius, color);
    }
    
    inline void draw_text(const std::string& text, int x, int y, int size, Color color) {
        DrawText(text.c_str(), x, y, size, color);
    }
}

#endif // LALA_RUNTIME_HPP
