from gpiozero import Button, AngularServo

servo = AngularServo(21, min_angle =-90, max_angle=90)

lock_state = Button(26)
open_state = Button(19)

locked = lock_state.is_pressed
open = open_state.is_pressed

activate_state = Button(20)
activated = activate_state.is_pressed

turn = 0

while True:
    servo.angle = turn
    if(not locked and lock_state.is_pressed):
        turn = 0
        print("Locked")
        print("Running Locked:"+str(locked)+" Open:"+str(open)+" Activated:"+str(activated)+" Angle:"+str(servo.angle))       
    if(not open and open_state.is_pressed):
        turn = 0
        print("Opened")        
        print("Running Locked:"+str(locked)+" Open:"+str(open)+" Activated:"+str(activated)+" Angle:"+str(servo.angle))
    if(not activated and activate_state.is_pressed):
        print("Activated")
        print("Running Locked:"+str(locked)+" Open:"+str(open)+" Activated:"+str(activated)+" Angle:"+str(servo.angle))
        if(lock_state.is_pressed):
            print("Opening")
            turn = 45
        elif(open_state.is_pressed):
            print("Locking")
            turn = -45
        else:
            turn = 0
    activated = activate_state.is_pressed
    locked = lock_state.is_pressed
    open = open_state.is_pressed
    