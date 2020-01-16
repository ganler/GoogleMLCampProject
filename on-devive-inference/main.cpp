#include <opencv2/opencv.hpp>
#include <opencv2/face.hpp>

#include "simpsonization/utils/timer.hpp"
#include "simpsonization/facedetector.hpp"
#include "simpsonization/transfer.hpp"
#include "simpsonization/swapper.hpp"

//std::array<std::arr>

template <typename D>
void kp_demo(cv::Mat& raw_frame, D&& detector){
    // @Output keypoints;
    auto landmarks = detector.detect(raw_frame, simp::speedup::make_seq(
            simp::speedup::downsample<1, 2>{},
            simp::speedup::skipper<2>{}
    ));

    if(!landmarks.empty()) // If the prediction succeeded.
    {
        detector.draw(raw_frame, landmarks);
        for(auto&& x : landmarks)
            simp::direction(x, raw_frame);
    }
}

int main() {
//    constexpr std::array<std::string_view, 7> choices{
//            "../models/simp2.onnx",
//            "../models/simpson.onnx",
//            "../models/candy.onnx",
//            "../models/mosaic.onnx",
//            "../models/pointilism.onnx",
//            "../models/rain_princess.onnx",
//            "../models/udnie.onnx"
//    };
//
//    std::cout << "[INFO]: Please select the style you want!\n";
//    for (int i = 0; i < choices.size(); ++i)
//        std::cout << "\tNo. " << i+1 << " => " << choices[i] << '\n';
//
////    std::size_t choose = 0;
////    std::cin >> choose;
//
////    simp::cvface_detector detector("../models/haarcascade_frontalface_alt2.xml", "../models/lbfmodel.yaml");
//    simp::dlibface_detector detector("../models/shape_predictor_68_face_landmarks.dat");
//
////    cv::VideoCapture cam(0); // Use your device.
//
////    cv::namedWindow("Facial Detection", cv::WINDOW_AUTOSIZE);
//
////    while(cam.read(_raw_frame) && cv::waitKey(1))
//    for(auto&& mn : choices)
//    {
//        simp::transfer transfer_model{mn};
//        cv::Mat _raw_frame = cv::imread("../test_image.jpeg");
//        auto copy = _raw_frame.clone();
//        transfer_model.forward(_raw_frame,
//                               simp::speedup::make_seq(
//                                       simp::speedup::none{}
////                                           simp::speedup::downsample<1, 4>{}
//                               ));
//        auto lms = detector.detect(copy,
//                                   simp::speedup::make_seq(
//                                           simp::speedup::none{}
////                                           simp::speedup::downsample<1, 4>{}
//                                   ));
//        auto copy2 = copy.clone();
//        detector.draw(copy2, lms);
//        simp::direction(lms.front(), copy2);
//
//        if(!lms.empty())
//        {
//            simp::swapper test(_raw_frame, lms.front());
//            test.add(copy, simp::nose_pos(lms.front()));
//            cv::imwrite("../mask.png", test.m_mask);
//        }
////        cv::imshow("Style", _raw_frame);
////        cv::imshow("Merge", copy);
//        cv::imwrite(std::string(mn)+"out.png", copy);
//        cv::imwrite("dir.png", copy2);
//    }

    constexpr std::array<std::string_view, 7> choices{
            "../models/simp2.onnx",
            "../models/simpson.onnx",
            "../models/candy.onnx",
            "../models/mosaic.onnx",
            "../models/pointilism.onnx",
            "../models/rain_princess.onnx",
            "../models/udnie.onnx"
    };

    std::cout << "[INFO]: Please select the style you want!\n";
    for (int i = 0; i < choices.size(); ++i)
        std::cout << "\tNo. " << i+1 << " => " << choices[i] << '\n';

    std::size_t choose = 0;
    std::cin >> choose;

    simp::dlibface_detector face_detector{"../models/shape_predictor_68_face_landmarks.dat"};
    simp::transfer transfer_model{choices[choose]};

    cv::VideoCapture cam(0);
    cv::Mat _raw_frame;
    while(cam.read(_raw_frame) && cv::waitKey(1)) {
        auto lms = face_detector.detect(_raw_frame, simp::speedup::none{});
        if(!lms.empty()) {
            simp::swapper test(_raw_frame, lms.front(), transfer_model);
            test.add(_raw_frame, simp::nose_pos(lms.front()));
        }
        cv::imshow("Face mask", _raw_frame);
    }

}