"""lab01 controller."""
import math
import time

# Import MyRobot Class
from fairis_tools.my_robot import MyRobot

# Create the robot instance.
robot = MyRobot()

# Loads the environment from the maze file
maze_file = '../../worlds/Spring25/maze1.xml'
robot.load_environment(maze_file)

# Move robot to a random staring position listed in maze file
robot.move_to_start()

travTime = 0

#robot completes a semi circle turn
def makeTurn(turnRadius, way, safety):

    #prints which way the robot is turning
    print(f"Beginning {way} turn")

    #collects starting time
    startTime = time.time() #from chatgpt

    #gets the starting distance
    initialDis = (robot.wheel_radius * robot.get_front_left_motor_encoder_reading()) 

    #determines turn distance of left wheel depending on if it is on the inside or outside
    if way == "left":
        turnDis = (turnRadius - 0.1325) * math.pi
    elif way == "right":
        turnDis = (turnRadius + 0.1325) * math.pi

    #distance of turn completed
    doneDis = 0

    #sets velocities based off of left or right turn. The formulas calculate velovity from turn radius, axel length, and the other velocity
    if way == "left":
        leftVel = 5 * ((turnRadius - 0.1325) / (turnRadius + .1325))
        rightVel = 5
    elif way == "right":
        rightVel = 5 * ((turnRadius - 0.1325) / (turnRadius + .1325))
        leftVel = 5

    #calculates the velocity of the robot so it can be used to calculate the time to complete
    vel = ((leftVel + rightVel)/2) * robot.wheel_radius

    #these print all calculated values before the movement happens
    print(f"Predicted Vl: {leftVel} rad/sec")
    print(f"Predicted Vr: {rightVel} rad/sec")
    print(f"Predicted D: {turnDis:.2f} meters")
    print(f"Predicted T: {turnDis/vel:.2f} seconds")

    count = 0
    
    #runs while the distance of turn completed is less that the turn distance
    while robot.experiment_supervisor.step(robot.timestep) != -1:

        #calculates distance traveled during function
        doneDis = ((robot.wheel_radius * robot.get_front_left_motor_encoder_reading()) - initialDis)

        #this prints the values, live during the movement. I added the modulo so that it didn't spam the consol
        if count %40 == 0:
            print(f"Current Vl: {leftVel:.2f} rad/sec")
            print(f"Current Vr: {rightVel:.2f} rad/sec")
            print(f"Current D: {doneDis:.2f} meters")
            print(f"Current T: {time.time() - startTime:.2f} seconds")

        #turn is complete
        if doneDis >= turnDis - safety:
            #stops robot
            robot.set_left_motors_velocity(0)
            robot.set_right_motors_velocity(0)
            #prints actual values
            print("Turn Complete")
            print(f"Final D: {doneDis:.2f} meters")
            print(f"Final T: {time.time() - startTime:.2f} seconds") #from chatGpt. I didnt know how to display the time
            printCoor()
            print("-----------------------")
            break
        #this is how the robot moves
        robot.set_left_motors_velocity(leftVel)
        robot.set_right_motors_velocity(rightVel)

        count += 1
        
#the robot moves straight
#many lines are similar to turn function, refer to notes there
def moveStr(dis):

    print("Beginning movement")

    startTime = time.time() #from chatgpt

    count = 0

    initialDis = (robot.wheel_radius * robot.get_front_left_motor_encoder_reading()) 

    print(f"Predicted Vl: 10 rad/sec")
    print(f"Predicted Vr: 10 rad/sec")
    print(f"Predicted D: {dis:.2f} meters")
    print(f"Predicted T: {dis/(10 * robot.wheel_radius):.2f} seconds")

    while robot.experiment_supervisor.step(robot.timestep) != -1:

        doneDis = ((robot.wheel_radius * robot.get_front_left_motor_encoder_reading()) - initialDis)

        robot.set_left_motors_velocity(10)
        robot.set_right_motors_velocity(10)

        if count %40 == 0:
            print(f"Current Vl: 10 rad/sec")
            print(f"Current Vr: 10 rad/sec")
            print(f"Current D: {doneDis:.2f} meters")
            print(f"Current T: {time.time() - startTime:.2f} seconds")

        if doneDis >= dis:
            robot.set_left_motors_velocity(0)
            robot.set_right_motors_velocity(0)
            print("Movement Complete")
            print(f"Actual D: {doneDis:.2f}")
            print(f"Actual T: {time.time() - startTime:.2f} seconds") #from chatGpt
            printCoor()
            print("-----------------------")
            break
        count += 1
    
#the robot rotates in place
def rotate(way, dir):

    startTime = time.time() #from chatgpt
    startDir = robot.get_compass_reading()

    print("Begining rotation")

    #only 2 modes lol
    if way == "left":
        print(f"Vl: -0.5 rad/sec")
        print(f"Vr: 0.5 rad/sec")
    if way == "right":
        print(f"Vl: 0.5 rad/sec")
        print(f"Vr: -0.5 rad/sec")

    print("Predicted D: 0")
    print(f"Predicted T: {math.radians(abs(startDir - dir)) * 0.265:.2}")

    count = 0

    while robot.experiment_supervisor.step(robot.timestep) != -1:
        if way == "left":
            robot.set_left_motors_velocity(-.5)
            robot.set_right_motors_velocity(.5)
        if way == "right":
            robot.set_left_motors_velocity(.5)
            robot.set_right_motors_velocity(-.5)

        if count %40 == 0:
            if way == "left":
                print(f"Current Vl: -0.5 rad/sec")
                print(f"Current Vr: 0.5 rad/sec")
            if way == "right":
                print(f"Current Vl: 0.5 rad/sec")
                print(f"Current Vr: -0.5 rad/sec")
            print(f"Current T: {time.time() - startTime:.2f} seconds")

        #this is cool. The robot will rotate until its compass aligns with the input direction. 
        #I had to make the robot go super slow because it kept overshooting the target degree
        if robot.get_compass_reading() == dir:  
            robot.set_left_motors_velocity(0)
            robot.set_right_motors_velocity(0)
            print("Rotation Complete")
            print("Final D: 0")
            print(f"Actual T: {time.time() - startTime:.2f} seconds") #from chatGpt
            printCoor()
            print("-----------------------")
            break
        count += 1
        
#the final movement of the track
def finalStep():
    startTime = time.time()
    initialDis = (robot.wheel_radius * robot.get_front_left_motor_encoder_reading()) 
    count = 0
    while robot.experiment_supervisor.step(robot.timestep) != -1:
        
        
        doneDis = ((robot.wheel_radius * robot.get_front_left_motor_encoder_reading()) - initialDis)

        robot.set_left_motors_velocity(5.581395349)
        robot.set_right_motors_velocity(19.76744186)
        
        if count %40 == 0:
            print(f"Current Vl: 5.58 rad/sec")
            print(f"Current Vr: 19.77 rad/sec")
            print(f"Current D: {doneDis:.2f} meters")
            print(f"Current T: {time.time() - startTime:.2f} seconds")

        if time.time() - startTime >= 0.5:
            robot.set_left_motors_velocity(0)
            robot.set_right_motors_velocity(0)
            print("The Track is complete!")
            print("Turn Complete")
            print(f"Final D: {doneDis:.2f} meters")
            print(f"Final T: {time.time() - startTime:.2f} seconds") #from chatGpt. I didnt know how to display the time
            print(f"Fnal orientation: {robot.get_compass_reading()} degrees")
            printCoor()
            print(f"D: {doneDis:.2f}")
            break
        count += 1

#I got this function from ChatGPT, I asked how to display current GPS Coordinates after giving it the rosbot code and the prompt from the lab
def printCoor():
    coordinates = robot.gps.getValues()
    print(f"GPS Coordinates: ({coordinates[0]:.2}, {coordinates[1]:.2})")


# Main Control Loop for Robot
while robot.experiment_supervisor.step(robot.timestep) != -1:


    # Calculates distance the wheel has turned since beginning of simulation
    distance_front_left_wheel_traveled = robot.wheel_radius * robot.get_front_left_motor_encoder_reading()
    robot.experiment_supervisor.getTime()

    robot.gps = robot.experiment_supervisor.getDevice('gps')
    robot.gps.enable(robot.timestep)

    print("S to P1")
    moveStr(1.5)

    
    print("P1 to P2")
    makeTurn(0.5, "left", 0.00)

    print("P2 to P3")
    makeTurn(1.5, "right", 0)
    

    print("P3 to P4")
    moveStr(2.4)

    print("P4 to P5")
    rotate("right", 0)

    print("P5 to P6")
    moveStr(3.6)

    print("P6 to P7")
    rotate("right", 315)

    print("P7 to P8")
    moveStr(0.71)

    print("P8 to P9")
    rotate("right", 225)

    print("P9 to P10")
    moveStr(0.71)

    print("P10 to P11")
    rotate("right", 180)
    print(robot.get_compass_reading())
    coord = robot.gps.getValues()
    print(f"GPS Coordinates: ({coord[0]}, {coord[1]})")

    print("P11 to P12")
    moveStr(1.5)

    finalStep()

    break