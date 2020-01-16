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

#include "utils/speedup.hpp"
#include "utils/debug_plot.hpp"

namespace simp
{

using curve_t = std::vector<cv::Point2f>;

cv::Point2f nose_pos(const curve_t& _curve)
{
    return _curve[30];
}

template <typename ... Args>
std::string strcat(Args&& ... args)
{
    std::string ret;
    ((ret += std::to_string(args) + ' '), ...);
    return ret;
}

cv::Point2f direction(const std::vector<cv::Point2f>& _landmark, cv::Mat& _mat)
{
    const std::array<cv::Point2f, 6> image_points{
            _landmark[30],
            _landmark[8],
            _landmark[36],
            _landmark[45],
            _landmark[48],
            _landmark[54]
    };

    static const std::array<cv::Point3f, 6> model_points{
            cv::Point3d(0.0f, 0.0f, 0.0f),               // Nose tip
            cv::Point3d(0.0f, -330.0f, -65.0f),          // Chin
            cv::Point3d(-225.0f, 170.0f, -135.0f),       // Left eye left corner
            cv::Point3d(225.0f, 170.0f, -135.0f),        // Right eye right corner
            cv::Point3d(-150.0f, -150.0f, -125.0f),      // Left Mouth corner
            cv::Point3d(150.0f, -150.0f, -125.0f)
    };

    float focal_length = _mat.cols;
    const cv::Point2d center(_mat.cols/2, _mat.rows/2);
    const cv::Mat camera_matrix = (cv::Mat_<float >(3,3) << focal_length, 0, center.x, 0 , focal_length, center.y, 0, 0, 1);
    const cv::Mat dist_coeffs = cv::Mat::zeros(4,1,cv::DataType<float >::type); // Assuming no lens distortion

    cv::Mat rotation_vector, translation_vector;

    cv::solvePnP(model_points, image_points, camera_matrix, dist_coeffs, rotation_vector, translation_vector);

    std::vector<cv::Point3f> nose_end_point3D{cv::Point3f(0, 0, 1000.0)};
    std::vector<cv::Point2f> nose_end_point2D;

    cv::projectPoints(nose_end_point3D, rotation_vector, translation_vector, camera_matrix, dist_coeffs, nose_end_point2D);

    for(int i=0; i < image_points.size(); i++)
        circle(_mat, image_points[i], 3, cv::Scalar(0,0,255), -1);

    cv::line(_mat, image_points.front(), nose_end_point2D.front(), cv::Scalar(255, 0, 255), 2);

    cv::Point2f vec{ nose_end_point2D.front() - image_points.front() };
//    vec = vec / cv::norm(vec);

//    cv::putText(_mat, strcat(vec.x, vec.y), {0, _mat.rows / 2}, cv::FONT_HERSHEY_PLAIN, 1, {255, 0, 255}, 1);

//    static float maxx, maxy, minx, miny;
//    maxx = std::max(maxx, vec.x);
//    minx = std::min(minx, vec.x);
//    maxy = std::max(maxy, vec.y);
//    miny = std::min(miny, vec.y);
//
//    std::cout << "--------------------------\n";
//    std::cout << maxx << ' ' << maxy << '\n';
//    std::cout << minx << ' ' << miny << '\n';
//    std::cout << "--------------------------\n";

    return vec;
}

using landmark_t = std::vector<std::vector<cv::Point2f>>;

class dlibface_detector
{
public:
    dlibface_detector(std::string_view _facem) : m_model(dlib::get_frontal_face_detector()){
        dlib::deserialize(_facem.data()) >> m_sp;
    }

    template<typename SpeedUpPolicy, typename MatLike>
    landmark_t detect(MatLike&& _raw_frame, SpeedUpPolicy p)
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
        for(const auto& face : faces)
        {
            auto tmp = m_sp(data, face);
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
        for(const auto& _x : _landmarks)
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
    landmark_t detect(MatLike&& _raw_frame, SpeedUpPolicy p)
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