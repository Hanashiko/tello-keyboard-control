import argparse
import os
import time
import cv2
import keyboard
from djitellopy import Tello


class RyzeTello:
    def __init__(self, save_session, save_path):
        self.tello = Tello()

        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 100
        self.send_rc_control = False

        self.save_session = save_session
        self.save_path = save_path

        if self.save_session:
            os.makedirs(self.save_path, exist_ok=True)

    def run(self):
        self.tello.connect()

        while True:

            k = cv2.waitKey(20)

            if keyboard.is_pressed('esc'):  
                break
            elif keyboard.is_pressed('q'):
                self.tello.takeoff()
                self.send_rc_control = True
            elif keyboard.is_pressed('e'):
                self.tello.land()
                self.send_rc_control = False

            if self.send_rc_control:
                if keyboard.is_pressed('w'):
                    self.for_back_velocity = self.speed
                elif keyboard.is_pressed('s'):
                    self.for_back_velocity = -self.speed
                else:
                    self.for_back_velocity = 0

                if keyboard.is_pressed('d'):
                    self.left_right_velocity = self.speed
                elif keyboard.is_pressed('a'):
                    self.left_right_velocity = -self.speed
                else:
                    self.left_right_velocity = 0

                if keyboard.is_pressed('up'):
                    self.up_down_velocity = self.speed
                elif keyboard.is_pressed('down'):
                    self.up_down_velocity = -self.speed
                else:
                    self.up_down_velocity = 0

                # turn right or left
                if keyboard.is_pressed('right'):
                    self.yaw_velocity = self.speed
                elif keyboard.is_pressed('left'):
                    self.yaw_velocity = -self.speed
                else:
                    self.yaw_velocity = 0
                
                if keyboard.is_pressed('+'):
                    if self.speed <= 95:
                        self.speed += 5
                if keyboard.is_pressed('-'):
                    if self.speed >= -95:
                        self.speed -= 5

                if keyboard.is_pressed('1'):
                    self.tello.flip_back()
                if keyboard.is_pressed('2'):
                    self.tello.flip_forward()
                if keyboard.is_pressed('3'):
                    self.tello.flip_right()
                if keyboard.is_pressed('4'):
                    self.tello.flip_left()
                   
                if keyboard.is_pressed('c'):
                    for i in range(4):  
                        self.tello.set_speed(99)
                        self.tello.move_forward(200)
                        self.tello.rotate_clockwise(90)
                     
                if keyboard.is_pressed('t'):
                    for i in range(3):
                        drone.set_speed(99)
                        drone.move_forward(250)
                        drone.rotate_clockwise(120)

                if keyboard.is_pressed('u'):
                    self.tello.move_up(150)
                  
                self.tello.send_rc_control(
                    self.left_right_velocity, self.for_back_velocity, self.up_down_velocity, self.yaw_velocity)

        self.tello.end()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-sa', '--save_session',
                        action='store_true', help='Record flight')
    parser.add_argument('-sp', '--save_path', type=str,
                        default="session/", help="Path where images will get saved")
    args = parser.parse_args()

    drone = RyzeTello(args.save_session, args.save_path)
    drone.run()
