#ifndef LALA_COLLECTIONS_HPP
#define LALA_COLLECTIONS_HPP

#include <vector>
#include <algorithm>

namespace lala {
namespace collections {

    template <typename T>
    inline void jodo(std::vector<T>& suchi, const T& item) {
        suchi.push_back(item);
    }

    template <typename T>
    inline void hatao(std::vector<T>& suchi, size_t index) {
        if (index < suchi.size()) {
            suchi.erase(suchi.begin() + index);
        }
    }

    template <typename T>
    inline size_t lambai(const std::vector<T>& suchi) {
        return suchi.size();
    }

    template <typename T>
    inline void saaf(std::vector<T>& suchi) {
        suchi.clear();
    }

    template <typename T>
    inline bool khali(const std::vector<T>& suchi) {
        return suchi.empty();
    }

    template <typename T>
    inline void sort(std::vector<T>& suchi) {
        std::sort(suchi.begin(), suchi.end());
    }

    template <typename T>
    inline void reverse(std::vector<T>& suchi) {
        std::reverse(suchi.begin(), suchi.end());
    }

} // namespace collections
} // namespace lala

#endif
