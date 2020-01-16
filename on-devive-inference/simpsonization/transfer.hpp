//
// Created by ganler-Mac on 2020-01-15.
//

#pragma once

#include <opencv2/opencv.hpp>
#include "utils/speedup.hpp"

namespace simp
{

class transfer
{
public:
    transfer(std::string_view _sv) : m_model(cv::dnn::readNetFromONNX(_sv.data())) {}
    template<typename SpeedUpPolicy, typename MatLike>
    void forward(MatLike&& _raw_frame, SpeedUpPolicy p)
    {
        auto originalsz = cv::Size{_raw_frame.size[1], _raw_frame.size[0]};
        SpeedUpPolicy()(_raw_frame);
        auto blob = cv::dnn::blobFromImage(_raw_frame);

        m_model.setInput(blob);
        auto result = m_model.forward();

        std::vector<cv::Mat> mat_vec;
        cv::dnn::imagesFromBlob(result, mat_vec);
        mat_vec[0].convertTo(_raw_frame, CV_8UC3);

//        cv::resize(_raw_frame, _raw_frame, originalsz);
    }
private:
    cv::dnn::Net m_model;
};

}