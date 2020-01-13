cmake_minimum_required(VERSION 3.14)
project(simpsonization)

set(CMAKE_CXX_FLAGS "-Ofast -march=native")
set(CMAKE_CXX_STANDARD 17)

add_executable(simpsonization main.cpp)

find_package(dlib REQUIRED)
target_link_libraries(${PROJECT_NAME} dlib::dlib)

find_package(OpenCV 4 REQUIRED)
message(STATUS ">>>> OpenCV 4 found!")
message(STATUS "    version: ${OpenCV_VERSION}")
message(STATUS "    libraries: ${OpenCV_LIBS}")
message(STATUS "    include path: ${OpenCV_INCLUDE_DIRS}")
message(STATUS "    cmake: ${OpenCV_DIR}")
target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS})

message(STATUS "Final compile options: ${CMAKE_CXX_FLAGS}")