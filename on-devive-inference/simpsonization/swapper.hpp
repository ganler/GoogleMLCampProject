//
// Created by ganler-Mac on 2020-01-16.
//

#pragma once

#include <tuple>
#include <opencv2/opencv.hpp>

#include "facedetector.hpp"

namespace simp
{

//std::tuple<curve_t, cv::Rect> get_cropped(const curve_t& landmark)
//{ // Not thread-safe. Static key word is used for efficiency.
//    static std::vector<int> indexs;
//    indexs.clear();
//    cv::convexHull(landmark, indexs);
//
//    std::tuple<curve_t, cv::Rect> ret;
//    std::uint32_t l = std::numeric_limits<std::uint32_t >::max();
//    std::uint32_t r = 0;
//    std::uint32_t t = std::numeric_limits<std::uint32_t >::max();
//    std::uint32_t b = 0;
//
//    std::get<curve_t>(ret).reserve(indexs.size());
//    for(auto&& ind : indexs)
//    {
//        l = std::min(l, static_cast<std::uint32_t>(landmark[ind].x));
//        r = std::max(r, static_cast<std::uint32_t>(landmark[ind].x));
//        t = std::min(t, static_cast<std::uint32_t>(landmark[ind].y));
//        b = std::max(b, static_cast<std::uint32_t>(landmark[ind].y));
//        std::get<curve_t>(ret).push_back(landmark[ind]);
//    }
//
//    std::get<cv::Rect>(ret) = cv::Rect(l, t, r - l, b - t);
//    return ret;
//}

class swapper
{
public:
//    cv::Mat
    template <typename M>
    swapper(cv::Mat _mat, const curve_t& _landmark, M&& _model)
    {
        using curvei_t = std::vector<cv::Point>;
        static std::vector<int> indexs;
        indexs.clear();
        cv::convexHull(_landmark, indexs);

        curvei_t outer;
        outer.reserve(indexs.size());

        int l = std::numeric_limits<int >::max();
        int r = 0;
        int t = std::numeric_limits<int >::max();
        int b = 0;

        for(auto&& ind : indexs)
        {
            l = std::min(l, static_cast<int>(_landmark[ind].x));
            r = std::max(r, static_cast<int>(_landmark[ind].x));
            t = std::min(t, static_cast<int>(_landmark[ind].y));
            b = std::max(b, static_cast<int>(_landmark[ind].y));
        }

        for(auto&& ind : indexs)
            outer.push_back(_landmark[ind] - cv::Point2f(l, t));

//        simp::draw_landmarks(_mat, outer, {255, 255, 255});

        // Create.
        m_cropped = _mat({l, t, r - l, b - t}).clone();

        _model.forward(m_cropped, simp::speedup::none{});
        cv::resize(m_cropped, m_cropped, {r - l, b - t});
        m_cropped_nose = simp::nose_pos(_landmark) - cv::Point2f(l, t);

        // Cal Mask.
        m_mask = cv::Mat::zeros(m_cropped.rows, m_cropped.cols, CV_8UC3);
        cv::fillConvexPoly(m_mask, outer.data(), outer.size(), cv::Scalar(255, 255, 255));

        m_cropped &= m_mask;
    }
    void add(cv::Mat& _mat, cv::Point2f _nose)
    {
        cv::Rect roi(cv::Point2i{_nose - m_cropped_nose}, cv::Size{m_cropped.cols, m_cropped.rows});
        seamlessClone(m_cropped, _mat(roi), m_mask, {m_cropped.cols/2, m_cropped.rows/2}, _mat(roi), cv::NORMAL_CLONE);
//        _mat(roi) &= (~m_mask);
//        _mat(roi) += m_cropped;
    }
//private:
    cv::Mat     m_cropped;
    cv::Mat     m_mask;
    cv::Point2f m_cropped_nose;
};


}