#ifndef LALA_MATH_HPP
#define LALA_MATH_HPP

#include "raylib.h"
#include <cmath>

namespace lala {
namespace math {

    inline int random(int min, int max) {
        return GetRandomValue(min, max);
    }

    inline float abs(float value) {
        return std::abs(value);
    }

    inline float clamp(float value, float min, float max) {
        if (value < min) return min;
        if (value > max) return max;
        return value;
    }

    inline float sqrt(float value) {
        return std::sqrt(value);
    }

    inline float sin(float value) {
        return std::sin(value);
    }

    inline float cos(float value) {
        return std::cos(value);
    }

    const float pi = 3.14159265358979323846f;

} // namespace math
} // namespace lala

#endif
