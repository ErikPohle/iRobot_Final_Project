#include <gazebo/common/Plugin.hh>
#include <ros/ros.h>

#include <gazebo/physics/World.hh>
#include <gazebo/physics/Model.hh>
#include <gazebo/physics/Link.hh>
#include <gazebo/physics/physics.hh>

#include <unistd.h>

#include <boost/bind.hpp>
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <stdio.h>


#include <ignition/math/Pose3.hh>
#include <ignition/math/Vector3.hh>
#include <ignition/math/Quaternion.hh>


//Adding packages that might be useful
#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <nav_msgs/Odometry.h>
#include <thread>
#include "ros/ros.h"
#include "ros/callback_queue.h"
#include "ros/subscribe_options.h"
#include "std_msgs/Float32.h"
#include "geometry_msgs/Point.h"
#include "turtlebot3_gazebo/particle_msg.h"
#include <gazebo/transport/TransportTypes.hh>


//including turtlebot3
#include "turtlebot3_gazebo/turtlebot3_drive.h"

namespace gazebo
{
class ParticleShooterPlugin : public WorldPlugin //, public Turtlebot3Drive
{
public:
  ParticleShooterPlugin() : WorldPlugin()
  {
  }


  /// \brief Handle an incoming message from ROS
  /// \param[in] _msg A float value that is used to set the velocity
  /// of the Velodyne.
  public: void OnRosMsg(const geometry_msgs::Pose::ConstPtr &_msg)  
  {
    std::cout << "MY ROS MESSAGE" << _msg->position.x;

    //Setting particle position
    this->x_origin = _msg->position.x;
    this->y_origin = _msg->position.y;
    this->z_origin = _msg->position.z;

    //Setting forces to be applied to particle
    this->x_axis_force = _msg->orientation.x;
    this->y_axis_force = _msg->orientation.y;
    this->z_axis_force = _msg->orientation.z;

  }

  /// \brief ROS helper function that processes messages
  private: void QueueThread()
  {
    static const double timeout = 0.01;
    while (this->rosNode->ok())
    {
      this->rosQueue.callAvailable(ros::WallDuration(timeout));
    }
  }


  void Load(physics::WorldPtr _world, sdf::ElementPtr _sdf)
  {
                                                                                        
    // Make sure the ROS node for Gazebo has already been initialized

    if (!ros::isInitialized())
    {
      int argc = 0;
      char **argv = NULL;
      ros::init(argc, argv, "gazebo_client",
          ros::init_options::NoSigintHandler);
    }


    //Particle shooter subscirber
    this->rosNode.reset(new ros::NodeHandle("gazebo_client"));
    this->rosNode->setCallbackQueue(&(this->rosQueue));

    this->rosSub = this->rosNode->subscribe("/particle_shooter", 10, &ParticleShooterPlugin::OnRosMsg,this);
    std::cout<<"num of publishers"<<this->rosSub.getNumPublishers()<<std::endl; 

    this->rosQueueThread = std::thread(std::bind(&ParticleShooterPlugin::QueueThread, this));


    
    
    this->world = _world;
    GZ_ASSERT(this->world != NULL, "Got NULL world pointer!");
    this->sdf = _sdf;
    GZ_ASSERT(this->sdf != NULL, "Got NULL SDF element pointer!");
    
    // Check if Config Elements exist, otherwise they will have default value
    if (_sdf->HasElement("reset_frequency"))
      this->reset_frequency = _sdf->Get<double>("reset_frequency");

    if (_sdf->HasElement("x_axis_force"))
      this->x_axis_force = _sdf->Get<double>("x_axis_force");
    if (_sdf->HasElement("y_axis_force"))
      this->y_axis_force = _sdf->Get<double>("y_axis_force");
    if (_sdf->HasElement("z_axis_force"))
      this->z_axis_force = _sdf->Get<double>("z_axis_force");
      
    if (_sdf->HasElement("x_origin"))
      this->x_origin = _sdf->Get<double>("x_origin");
    if (_sdf->HasElement("y_origin"))
      this->y_origin = _sdf->Get<double>("y_origin");
    if (_sdf->HasElement("z_origin"))
      this->z_origin = _sdf->Get<double>("z_origin");
      
    if (_sdf->HasElement("random_range"))
      this->random_range = _sdf->Get<double>("random_range");  
    
    
    
    // We wait for all system to be ready an amount of seconds
    float seconds_to_wait = 5.0;
    this->WaitForseconds(seconds_to_wait);

    // Update Time Init
    this->old_secs =this->world->SimTime().Float();
    // Listen to the update event. This event is broadcast every
    // simulation iteration.
    this->updateConnection = event::Events::ConnectWorldUpdateBegin(
        std::bind(&ParticleShooterPlugin::OnUpdate, this));

    GetParticleList();
    OutputParticleList();
  
  }


  void Reset()
  {
    this->reseting_plugin = true;
    ROS_ERROR("Reseted the simulation world, we Restart the time clock");
    // Update Time Init
    this->old_secs = 0.0;
    double new_secs = 0.0;
    double delta = -1.0;

    while (delta < 0.0)
    {
      // We change Direction
      ROS_ERROR("Waiting until Clock is reseted and delta is not negative > Update delta=%f, new_secs=%f", delta,  new_secs);
      new_secs = this->world->SimTime().Float();
      delta = new_secs - this->old_secs;
      ROS_ERROR("Updated until Clock is reseted > Update delta=%f, new_secs=%f", delta,  new_secs);

    }

    this->reseting_plugin = false;

  }


  // Called by the world update start event
  public: void OnUpdate()
  {


    if (this->reseting_plugin)
    {
        ROS_ERROR("Reseting in Process, please wait...");
    }else
    {
        // TODO: Check what is necessary now here
        double new_secs =this->world->SimTime().Float();
        double delta = new_secs - this->old_secs;

        double max_delta = 0.0;

        if (this->reset_frequency != 0.0)
        {
          max_delta = 1.0 / this->reset_frequency;
        }

        if (delta > max_delta && delta != 0.0)
        {
          // We update the Old Time variable.
          this->old_secs = new_secs;
          
          
          if (this->model_to_update_index_now >= this->modelIDToName_size)
          {
            this->model_to_update_index_now = 0;
          }
          
            // Update the Particles
            UpdateParticles(this->model_to_update_index_now);
            this->model_to_update_index_now ++;
          

        }
    }



  }

  void WaitForseconds(float seconds_to_wait)
  {
    unsigned int microseconds;
    microseconds = seconds_to_wait * 1e6;
    ROS_WARN("Waiting for %f seconds",seconds_to_wait);
    usleep(microseconds);
    ROS_WARN("Done waiting...");

  }

  void UpdateParticles(int model_to_update_index)
  {
    for (auto model : this->world->Models())
    {
        std::string model_name = model->GetName();
        if (this->modelIDToName[model_to_update_index] == model_name)
        {
            this->MoveParticle(model);
            this->SetForceParticle(model);
        }
        
    }
  }
  
  
  
    void GetParticleList()
    {
        this->modelIDToName.clear();
        // Initialize color map.
        this->modelIDToName_size = 0;
        
        int i = 0;
        for (auto model : this->world->Models())
        {
            std::string model_name = model->GetName();
            if (model_name.find(this->particle_base_name) != std::string::npos)
            {
                this->modelIDToName[i] = model->GetName();
                i ++;
            }
          
        }
        
        this->modelIDToName_size = modelIDToName.size();
    }
    
    void OutputParticleList()
  {
    ROS_WARN("Start OutputParticleList...");

    for (auto const& x : this->modelIDToName)
    {
        ROS_WARN("ModelID=%i, Name=%s", x.first, x.second.c_str());
    }

    ROS_WARN("END OutputParticleList...");

  }
  
  
  void MoveParticle(boost::shared_ptr<gazebo::physics::Model> model)
  {

    std::string model_name = model->GetName();

    float x_pos_rand = 0.0;
    float y_pos_rand = 0.0;
    float z_pos_rand = 0.0;
    float roll_rand = 0.0;
    float pitch_rand = 0.0;
    float yaw_rand = 0.0;

    // If the model name contains the substring particle, we consider it a particle
    if (model_name.find(this->particle_base_name) != std::string::npos)
    {
        ROS_WARN("Moving model=%s",model_name.c_str());

        float x_pos_rand = this->x_origin;  //RandomFloat(this->x_origin - this->random_range, this->x_origin + this->random_range);
        float y_pos_rand = this->y_origin;  //RandomFloat(this->y_origin - this->random_range, this->y_origin + this->random_range);
        float z_pos_rand = this->z_origin;  //RandomFloat(this->z_origin - this->random_range, this->z_origin + this->random_range);
        
        ROS_DEBUG("POSE-RANDOM[X,Y,Z,Roll,Pitch,Yaw=[%f,%f,%f,%f,%f,%f], model=%s", x_pos_rand,y_pos_rand,z_pos_rand,roll_rand,pitch_rand,yaw_rand,model_name.c_str());
        ROS_WARN("POSE-RANDOM[X,Y,Z,Roll,Pitch,Yaw=[%f,%f,%f,%f,%f,%f], model=%s", x_pos_rand,y_pos_rand,z_pos_rand,roll_rand,pitch_rand,yaw_rand,model_name.c_str());
        //ignition::math::Pose3 initPose(ignition::math::Vector3<float>(x_pos_rand, y_pos_rand, z_pos_rand), ignition::math::Quaternion<float>(roll_rand, pitch_rand, yaw_rand));
        
        model->SetWorldPose(
                            ignition::math::Pose3d(
                                ignition::math::Vector3d(x_pos_rand, y_pos_rand, z_pos_rand),
                                ignition::math::Quaterniond(roll_rand, pitch_rand, yaw_rand)
                                                )
                            );
        
        ROS_DEBUG("Moving model=%s....END",model_name.c_str());

    }

    

  }
  
  
  void SetForceParticle(boost::shared_ptr<gazebo::physics::Model> model)
  {
      
    std::string model_name = model->GetName();

    // If the model name contains the substring particle, we consider it a particle
    if (model_name.find(this->particle_base_name) != std::string::npos)
    {
        ROS_WARN("FORCE APPLIED[X,Y,Z]=[%f,%f,%f]", this->x_axis_force, this->y_axis_force, this->z_axis_force);
        model->GetLink("link")->SetForce(ignition::math::Vector3d(this->x_axis_force, this->y_axis_force, this->z_axis_force));
    }

    

  }


  
  float RandomFloat(float a, float b) {
    float random = ((float) rand()) / (float) RAND_MAX;
    float diff = b - a;
    float r = random * diff;
    return a + r;
  }
  
  
  // Pointer to the update event connection
  private: event::ConnectionPtr updateConnection;
  
  /// \brief World pointer.
  protected: gazebo::physics::WorldPtr world;
  /// \brief SDF pointer.
  protected: sdf::ElementPtr sdf;
  /// \brief Maps model IDs to ModelNames
  private: std::map<int, std::string> modelIDToName;

  /// \brief A node use for ROS transport
  private: std::unique_ptr<ros::NodeHandle> rosNode;

  /// \brief A ROS subscriber
  private: ros::Subscriber rosSub;

  /// \brief A ROS callbackqueue that helps process messages
  private: ros::CallbackQueue rosQueue;

  /// \brief A thread the keeps running the rosQueue
  private: std::thread rosQueueThread;
  
  
  // Update Loop frequency, rate at which we restart the positions and apply force to particles
  double reset_frequency = 2.0;
  // Time Memory
  double old_secs;
  // Force Direction
  double x_axis_force = 0.0;
  double y_axis_force = 0.0;
  double z_axis_force = 0.0;
  double x_origin = 0.0;
  double y_origin = 0.0;
  double z_origin = 1.0;
  
  double random_range = 0.1;

  // Reseting Flag
  bool reseting_plugin = false;
  
  int modelIDToName_size = 0;
  int model_to_update_index_now = 0;
  
  std::string particle_base_name = "particle";

  

};


GZ_REGISTER_WORLD_PLUGIN(ParticleShooterPlugin)
}




int main(int argc, char **argv)
{

  ros::init(argc, argv, "talker");

  ros::NodeHandle n;



 ros::Publisher chatter_pub = n.advertise<geometry_msgs::Pose>("part_pose", 1000);

  ros::Rate loop_rate(10);
  ros::WallDuration sleep_time(15.0);
  int i=0;
  while (ros::ok())
  { if(i==20)break;
    i++;
geometry_msgs::Pose msg;
msg.position.x=1.5;
msg.position.y=0.0;
msg.position.z=1.35;
msg.orientation.x=0.0;
msg.orientation.y=0.0;
msg.orientation.z=0.0;
msg.orientation.w=0.0;

    chatter_pub.publish(msg);
    ROS_INFO("there is %d subscriber(s)!!!!!!!!!!!",chatter_pub.getNumSubscribers());
    ros::spinOnce();
    ROS_INFO("message sent :)");
    sleep_time.sleep();
    loop_rate.sleep();
  }


  return 0;
}