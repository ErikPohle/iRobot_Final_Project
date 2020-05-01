
(cl:in-package :asdf)

(defsystem "turtlebot3_gazebo-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
)
  :components ((:file "_package")
    (:file "particle_msg" :depends-on ("_package_particle_msg"))
    (:file "_package_particle_msg" :depends-on ("_package"))
  ))