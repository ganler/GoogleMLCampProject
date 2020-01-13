//
// Created by ganler-Mac on 2020-01-13.
//

#pragma once

#include <opencv2/opencv.hpp>
#include <dlib/image_processing/frontal_face_detector.h>
#include <dlib/image_processing/render_face_detections.h>
#include <dlib/image_processing.h>
#include <dlib/opencv/cv_image.h>
#include <dlib/image_io.h>
#include "utils/debug_plot.hpp"

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
seq<Args ...> make_seq(Args&& ... args)
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
    bool operator()(cv::Mat& mat) {
        static_assert(
                Numerator < Denominator,
                "God, you're not doing optimization. Please go back to you primary school to take a math course.");
        cv::resize(mat, mat, cv::Size{}, ratio, ratio);
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

}

using landmark_t = std::vector<std::vector<cv::Point2f>>;

class dlibface_detector
{
public:
    dlibface_detector(std::string_view _facem) : m_model(dlib::get_frontal_face_detector()){
        dlib::deserialize(_facem.data()) >> m_sp;
    }
    template<typename SpeedUpPolicy, typename MatLike>
    landmark_t detect(MatLike&& _raw_frame, SpeedUpPolicy p = speedup::none{})
    {
        static landmark_t landmarks;
        if(SpeedUpPolicy()(_raw_frame))
            return landmarks;
        else
            landmarks.clear();
        dlib::cv_image<dlib::bgr_pixel> image(_raw_frame);
        dlib::matrix<dlib::rgb_pixel> data;
        assign_image(data, image);

        auto faces = m_model(data);
        landmarks.reserve(faces.size());
        for(std::size_t i=0; i<faces.size(); ++i)
        {
            auto tmp = m_sp(data, faces[i]);
            std::vector<cv::Point2f> ps;
            ps.reserve(tmp.num_parts());
            for(std::size_t j=0; j<tmp.num_parts(); ++j)
                ps.emplace_back(tmp.part(j).x(), tmp.part(j).y());
            landmarks.push_back(std::move(ps));
        }
        return landmarks;
    }
    static void draw(cv::Mat& _raw_frame, const landmark_t& _landmarks)
    {
        for(auto& _x : _landmarks)
        {
            simp::draw_landmarks(_raw_frame, _x);
            cv::face::drawFacemarks(_raw_frame, _x, cv::Scalar(0, 0, 255));
        }
    }
private:
    dlib::shape_predictor       m_sp;
    dlib::frontal_face_detector m_model;
};

class cvface_detector
{ // Not thread-safe.
public:
    cvface_detector(std::string_view _xml, std::string_view _yaml)
            : m_face_detector(_xml.data()), m_model(cv::face::FacemarkLBF::create())
    {
        m_model->loadModel(_yaml.data());
    }
    template<typename SpeedUpPolicy, typename MatLike>
    landmark_t detect(MatLike&& _raw_frame, SpeedUpPolicy p = speedup::none{})
    {
        static landmark_t landmarks;
        if(SpeedUpPolicy()(_raw_frame))
            return landmarks;
        else
            landmarks.clear();

        cv::Mat frame;
        if(_raw_frame.channels() != 1)
            cv::cvtColor(_raw_frame, frame, cv::COLOR_BGR2GRAY);
        else
            frame = _raw_frame;

        std::vector<cv::Rect> faces;
        faces.emplace_back();
        m_face_detector.detectMultiScale(frame, faces);

        return m_model->fit(frame, faces, landmarks) ? landmarks : landmark_t{};
    }

    static void draw(cv::Mat& _raw_frame, const landmark_t& _landmarks)
    {
        for(auto& _x : _landmarks)
        {
            simp::draw_landmarks(_raw_frame, _x);
            cv::face::drawFacemarks(_raw_frame, _x, cv::Scalar(0, 0, 255));
        }
    }
private:
    cv::CascadeClassifier           m_face_detector;
    cv::Ptr<cv::face::FacemarkLBF>  m_model;
};

}