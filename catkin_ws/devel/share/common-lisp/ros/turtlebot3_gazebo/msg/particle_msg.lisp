; Auto-generated. Do not edit!


(cl:in-package turtlebot3_gazebo-msg)


;//! \htmlinclude particle_msg.msg.html

(cl:defclass <particle_msg> (roslisp-msg-protocol:ros-message)
  ((points
    :reader points
    :initarg :points
    :type (cl:vector geometry_msgs-msg:Point)
   :initform (cl:make-array 0 :element-type 'geometry_msgs-msg:Point :initial-element (cl:make-instance 'geometry_msgs-msg:Point)))
   (another_field
    :reader another_field
    :initarg :another_field
    :type cl:fixnum
    :initform 0))
)

(cl:defclass particle_msg (<particle_msg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <particle_msg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'particle_msg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name turtlebot3_gazebo-msg:<particle_msg> is deprecated: use turtlebot3_gazebo-msg:particle_msg instead.")))

(cl:ensure-generic-function 'points-val :lambda-list '(m))
(cl:defmethod points-val ((m <particle_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader turtlebot3_gazebo-msg:points-val is deprecated.  Use turtlebot3_gazebo-msg:points instead.")
  (points m))

(cl:ensure-generic-function 'another_field-val :lambda-list '(m))
(cl:defmethod another_field-val ((m <particle_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader turtlebot3_gazebo-msg:another_field-val is deprecated.  Use turtlebot3_gazebo-msg:another_field instead.")
  (another_field m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <particle_msg>) ostream)
  "Serializes a message object of type '<particle_msg>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'points))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'points))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'another_field)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <particle_msg>) istream)
  "Deserializes a message object of type '<particle_msg>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'points) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'points)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'geometry_msgs-msg:Point))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'another_field)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<particle_msg>)))
  "Returns string type for a message object of type '<particle_msg>"
  "turtlebot3_gazebo/particle_msg")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'particle_msg)))
  "Returns string type for a message object of type 'particle_msg"
  "turtlebot3_gazebo/particle_msg")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<particle_msg>)))
  "Returns md5sum for a message object of type '<particle_msg>"
  "52b7cc5e44032cacb08a65980d276cc0")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'particle_msg)))
  "Returns md5sum for a message object of type 'particle_msg"
  "52b7cc5e44032cacb08a65980d276cc0")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<particle_msg>)))
  "Returns full string definition for message of type '<particle_msg>"
  (cl:format cl:nil "geometry_msgs/Point[] points~%uint8 another_field~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'particle_msg)))
  "Returns full string definition for message of type 'particle_msg"
  (cl:format cl:nil "geometry_msgs/Point[] points~%uint8 another_field~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <particle_msg>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'points) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <particle_msg>))
  "Converts a ROS message object to a list"
  (cl:list 'particle_msg
    (cl:cons ':points (points msg))
    (cl:cons ':another_field (another_field msg))
))
