//
// Created by ganler-Mac on 2020-01-13.
//

#pragma once

#include <iostream>
#include <opencv2/opencv.hpp>

namespace simp
{

void draw_poly_line(
        cv::Mat &_im,
        const std::vector<cv::Point2f> &_lm,
        const int _start,
        const int _end,
        const cv::Scalar _color = cv::Scalar(255, 200, 0),
        bool _is_closed = false
) {
    std::vector<cv::Point> points;
    for (int i = _start; i <= _end; ++i)
        points.emplace_back(_lm[i].x, _lm[i].y);
    cv::polylines(_im, points, _is_closed, _color, 2, 16);
}

void draw_landmarks(cv::Mat &_im, const std::vector<cv::Point2f> &_lm, const cv::Scalar _color = cv::Scalar(255, 200, 0)) {
    // Draw face for the 68-point model.
    if (_lm.size() == 68)
    {
        draw_poly_line(_im, _lm, 0, 16);           // Jaw line
        draw_poly_line(_im, _lm, 17, 21);          // Left eyebrow
        draw_poly_line(_im, _lm, 22, 26);          // Right eyebrow
        draw_poly_line(_im, _lm, 27, 30);          // Nose bridge
        draw_poly_line(_im, _lm, 30, 35, true);    // Lower nose
        draw_poly_line(_im, _lm, 36, 41, true);    // Left eye
        draw_poly_line(_im, _lm, 42, 47, true);    // Right Eye
        draw_poly_line(_im, _lm, 48, 59, true);    // Outer lip
        draw_poly_line(_im, _lm, 60, 67, true);    // Inner lip
    }
    else
        for (auto&& x : _lm)
            cv::circle(_im, x, 3, _color, cv::FILLED);
    // If the number of points is not 68, we do not know which
    // points correspond to which facial features. So, we draw
    // one dot per landmark.
}

}