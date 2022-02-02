#Steer Left - Left LS
#Steer Right - Right LS

from vjoy import vJoy, ultimate_release
import time

vj = vJoy()

XYRANGE = 16393
ZRANGE = 32786

vj.open()


# print('gass')
# time.sleep(2)
# joystickPosition = vj.generateJoystickPosition(wAxisZ = ZRANGE) # pilna gaaze
# vj.update(joystickPosition)
# time.sleep(2)

# joystickPosition = vj.generateJoystickPosition(wAxisZ = 0) # izslegta gaaze
# vj.update(joystickPosition)


# print("bremz")
# time.sleep(2)
# joystickPosition = vj.generateJoystickPosition(wAxisZRot = ZRANGE) # pilna bremze
# vj.update(joystickPosition)

# time.sleep(1)
# joystickPosition = vj.generateJoystickPosition(wAxisZRot = 0) # izslegta bremze
# vj.update(joystickPosition)


print("pa kreisi")
time.sleep(2)
joystickPosition = vj.generateJoystickPosition(wAxisX = 0) # FULLL LABI
vj.update(joystickPosition)
time.sleep(1)


print("pa labi")
time.sleep(2)
joystickPosition = vj.generateJoystickPosition(wAxisX = ZRANGE)
vj.update(joystickPosition)
time.sleep(2)






# vj.open()
# lol = 0
# while True:

#     lol += 1
#     joystickPosition = vj.generateJoystickPosition(wAxisX = lol)
#     vj.update(joystickPosition)
#     if (lol > 32000):
#         lol = 0



joystickPosition = vj.generateJoystickPosition()
vj.update(joystickPosition)
time.sleep(0.001)



vj.close()