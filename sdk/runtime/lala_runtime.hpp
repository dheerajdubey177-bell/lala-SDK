#pragma once

#include <iostream>
#include <string>
#include <cmath>
#include "raylib.h"

namespace lala {
    // Type definitions
    using number = double;

    // Initialization
    void init() {
        // Any global init
    }

    // Output
    template<typename T>
    void print(T value) {
        std::cout << value << std::endl;
    }

    // Graphics Module
    namespace graphics {
        void window(number width, number height, const char* title) {
            InitWindow((int)width, (int)height, title);
            SetTargetFPS(60);
        }

        bool window_should_close() {
            return WindowShouldClose();
        }

        void close_window() {
            CloseWindow();
        }

        void begin_drawing() {
            BeginDrawing();
        }

        void end_drawing() {
            EndDrawing();
        }

        void clear_background(number r, number g, number b) {
            ClearBackground(Color{(unsigned char)r, (unsigned char)g, (unsigned char)b, 255});
        }

        void circle(number x, number y, number radius, number r, number g, number b) {
            DrawCircle((int)x, (int)y, radius, Color{(unsigned char)r, (unsigned char)g, (unsigned char)b, 255});
        }
    }
}
