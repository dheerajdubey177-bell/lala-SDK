#ifndef LALA_RUNTIME_HPP
#define LALA_RUNTIME_HPP

#include <iostream>
#include <string>

// Modular Core v0.2 Headers
#include "lala_graphics.hpp"
#include "lala_input.hpp"
#include "lala_math.hpp"
#include "lala_collections.hpp"

// Main runtime namespace
namespace lala_runtime {
    // Legacy support for v0.1 functions (can be deprecated later)
    inline void create_window(int width, int height, const std::string& title) {
        lala::graphics::window(width, height, title);
    }
    
    inline void draw_circle(int x, int y, float radius, Color color) {
        lala::graphics::circle(x, y, radius, color);
    }
    
    inline void draw_text(const std::string& text, int x, int y, int size, Color color) {
        lala::graphics::text(text, x, y, size, color);
    }
}

#endif // LALA_RUNTIME_HPP
