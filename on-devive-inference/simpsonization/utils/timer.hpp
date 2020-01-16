//
// Created by ganler-Mac on 2020-01-15.
//

#pragma once

namespace simp
{

class timer {
public:
    timer() : clk_beg(std::chrono::steady_clock::now()) {}

    void reset() { clk_beg = std::chrono::steady_clock::now(); }

    uint64_t time_out() const {
        return std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now() - clk_beg).count();
    }

    template<typename Format>
    uint64_t time_out() const {
        return std::chrono::duration_cast<Format>(std::chrono::steady_clock::now() - clk_beg).count();
    }

    uint64_t time_out_microseconds() const { return time_out<std::chrono::microseconds>(); }

    uint64_t time_out_seconds() const { return time_out<std::chrono::seconds>(); }

    uint64_t time_out_minutes() const { return time_out<std::chrono::minutes>(); }

    uint64_t time_out_hours() const { return time_out<std::chrono::hours>(); }

private:
    std::chrono::time_point <std::chrono::steady_clock> clk_beg;
};// class Timer

}