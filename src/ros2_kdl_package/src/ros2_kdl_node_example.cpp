// Copyright  (C)  2007  Francois Cauwe <francois at cauwe dot org>
 
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 2.1 of the License, or (at your option) any later version.
 
#include <kdl/chain.hpp>
#include <kdl/chainfksolver.hpp>
#include <kdl/chainfksolverpos_recursive.hpp>
#include <kdl/chainjnttojacsolver.hpp>
#include <kdl/chainiksolverpos_lma.hpp>


#include <kdl/frames_io.hpp>
#include <stdio.h>
#include <iostream>

#include "rclcpp/rclcpp.hpp"
 
using namespace KDL;

int main( int argc, char** argv )
{
    rclcpp::init(argc, argv);
    //Definition of a kinematic chain & add segments to the chain
    KDL::Chain chain;
    chain.addSegment(Segment(Joint(Joint::RotZ),Frame(Vector(0.0,0.0,1.020))));
    chain.addSegment(Segment(Joint(Joint::RotX),Frame(Vector(0.0,0.0,0.480))));
    chain.addSegment(Segment(Joint(Joint::RotX),Frame(Vector(0.0,0.0,0.645))));
    chain.addSegment(Segment(Joint(Joint::RotZ)));
    chain.addSegment(Segment(Joint(Joint::RotX),Frame(Vector(0.0,0.0,0.120))));
    chain.addSegment(Segment(Joint(Joint::RotZ)));
 
    // Create solver based on kinematic chain
    ChainFkSolverPos_recursive fksolver = ChainFkSolverPos_recursive(chain);
 
    // Create joint array
    unsigned int nj = chain.getNrOfJoints();
    KDL::JntArray jointpositions = JntArray(nj);
 
    // Assign some values to the joint positions
    for(unsigned int i=0;i<nj;i++){
        float myinput;
        printf ("Enter the position of joint %i: ",i);
        scanf ("%e",&myinput);
        jointpositions(i)=(double)myinput;
    }
 
    // Create the frame that will contain the results
    KDL::Frame cartpos;    
 
    // Calculate forward position kinematics
    bool kinematics_status;
    kinematics_status = fksolver.JntToCart(jointpositions,cartpos);
    if(kinematics_status>=0){
        printf("%s \n","The cartesian pose of your robot tip is:");
        std::cout << cartpos <<std::endl;
        printf("%s \n","Success, thanks KDL!");
    }else{
        printf("%s \n","Error: could not calculate forward kinematics :(");
    }


    // Jacobian
    int jacobian_status;
    KDL::ChainJntToJacSolver jacSolver(chain);
    KDL::Jacobian J(nj);
    jacobian_status = jacSolver.JntToJac(jointpositions, J);
    if(jacobian_status>=0){
            std::cout << std::setprecision(9)
          << "q [rad]: " << jointpositions.data.transpose() << "\nTip pose in base:\n" << cartpos
          << "\nGeometric Jacobian [linear; angular], in base:\n" << J.data << "\n";
    }else{
        printf("%s \n","Error: could not calculate Jacobian :(");
    }

    // Inverse kinematics
    const KDL::Frame target = cartpos;
    KDL::JntArray seed(jointpositions);
    for (unsigned int i = 0; i < nj; ++i) seed(i) += (i%2 == 0 ? 0.02 : -0.02);
    bool ikOk = true;
    try {

        Eigen::Matrix<double, 6, 1> weights;
        weights.setOnes(); // Explicit translation/rotation weights for this demo.
        KDL::ChainIkSolverPos_LMA ik(chain, weights, 1e-10, 1000, 1e-15);
        KDL::JntArray solution(chain.getNrOfJoints());
        const int ik_status = ik.CartToJnt(seed, target, solution);
        if (ik_status>=0){
            std::cout << "IK seed [rad]: " << seed.data.transpose()
                  << "\nIK solution [rad]: " << solution.data.transpose();
        }
        else{
            printf("%s \n","Error: could not calculate IK :(");
            }
        
   
    } catch (const std::runtime_error& e) {
        ikOk = false;
        std::cerr << e.what() << "\nTry another seed; IK convergence is local.\n";
    }

    rclcpp::shutdown();
    return 1;
}