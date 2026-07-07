#ifndef LALA_INPUT_HPP
#define LALA_INPUT_HPP

#include "raylib.h"
#include <string>
#include <unordered_map>

namespace lala {
namespace input {

    // Helper map to translate string button names to Raylib keys
    inline int get_key(const std::string& key) {
        static std::unordered_map<std::string, int> keys = {
            {"RIGHT", KEY_RIGHT},
            {"LEFT", KEY_LEFT},
            {"UP", KEY_UP},
            {"DOWN", KEY_DOWN},
            {"SPACE", KEY_SPACE},
            {"ENTER", KEY_ENTER},
            {"ESC", KEY_ESCAPE}
        };
        if (keys.find(key) != keys.end()) {
            return keys[key];
        }
        return 0; // Default or unknown
    }

    inline bool button(const std::string& key) {
        return IsKeyDown(get_key(key));
    }

    inline bool button_pressed(const std::string& key) {
        return IsKeyPressed(get_key(key));
    }

    inline int mouse_x() {
        return GetMouseX();
    }

    inline int mouse_y() {
        return GetMouseY();
    }

} // namespace input
} // namespace lala

#endif
