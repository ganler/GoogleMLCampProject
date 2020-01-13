#include <opencv2/opencv.hpp>
#include <opencv2/face.hpp>

#include "simpsonization/utils/debug_plot.hpp"
#include "simpsonization/facedetector.hpp"

int main() {
    // @Load detector;
//    simp::cvface_detector detector("../models/haarcascade_frontalface_alt2.xml", "../models/lbfmodel.yaml");
    simp::dlibface_detector detector("../models/shape_predictor_68_face_landmarks.dat");
    cv::VideoCapture cam(0); // Use your device.
    cv::Mat raw_frame;
    cv::namedWindow("Facial Detection", cv::WINDOW_AUTOSIZE);

    while(cam.read(raw_frame) && cv::waitKey(1))
    {
        // @Output keypoints;
        auto landmarks = detector.detect(raw_frame, simp::speedup::make_seq(
                    simp::speedup::downsample<1, 2>{},
                    simp::speedup::skipper<2>{}
                ));

        if(!landmarks.empty()) // If the prediction succeeded.
            detector.draw(raw_frame, landmarks);
        cv::imshow("Facial Detection", raw_frame);
    }
}
