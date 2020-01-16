//
// Created by ganler-Mac on 2020-01-15.
//

#pragma once

#include <opencv2/opencv.hpp>

namespace simp
{


namespace speedup
{

template <typename ... Args>
struct seq{
    template <typename ... Ts>
    bool operator()(Ts&& ... ts) {
        return (Args{}(std::forward<Ts&&>(ts)...) && ...);
    }
};

template <typename ... Args>
constexpr seq<Args ...> make_seq(Args&& ... args)
{
    return seq<Args ...>{};
}


struct none{
    template <typename ... Args>
    bool operator()(Args&& ...) const noexcept{
        return false;
    }
};

template <uint32_t Numerator, uint32_t Denominator>
struct downsample
{
    static constexpr double ratio = static_cast<double>(Numerator) / Denominator;
    bool operator()(cv::Mat& _mat) {
        static_assert(
                Numerator < Denominator,
                "God, you're not doing optimization. Please go back to you primary school to take a math course.");
        cv::resize(_mat, _mat, cv::Size{}, ratio, ratio, cv::INTER_NEAREST);
        return false;
    }
};

template <uint32_t Rate>
struct skipper
{
    template <typename ... Args>
    bool operator()(Args&& ...) const noexcept{
        static uint32_t counter = 0;
        return (++counter) % Rate == 0;
    }
};

} // namespace speedup


}