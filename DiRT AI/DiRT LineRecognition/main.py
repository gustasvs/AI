import numpy as np
import cv2
import time
from directkeys import PressKey, ReleaseKey, W, A, S, D
from statistics import mean
from draw_lanes import draw_lanes
from grabscreen import grab_screen
from getkeys import key_check
ekplat = 1024
ekgar = 768

def keys_to_output(keys):
    #[A,W,D]
    output = [0, 0, 0]
    if 'A' in keys:
        output[0] = 1
    elif 'W' in keys:
        output[1] = 1
    elif 'D' in keys:
        output[2] = 1
    return output

def countdown():
    for i in list(range(3))[::-1]:
        print(i + 1)
        time.sleep(1)


def roi(image, vertices):
    mask = np.zeros_like(image)       
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(image, mask)
    return masked


def process_image(image):
    original_image = image
    processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_image = cv2.Canny(processed_image, threshold1=100, threshold2=250)
    processed_image = cv2.GaussianBlur(processed_image, (9, 9), 0)   
    # processed_image = roi(processed_image, [np.array([[10, 400], [10, 300], [290, 200], [ekplat - 290, 200], [ekplat, 300], [ekplat - 10, 400]])])
    processed_image = roi(processed_image, [np.array([[10, ekgar - 150], [10, 200], [ekplat - 10, 200], [ekplat - 10, ekgar - 150]])])

                            # edges, 1, np.pi/180, 100, minLineLenght, maxLineGap
    lines = cv2.HoughLinesP(processed_image, 1, np.pi/180, 150,    100,    50)
    #draw_lines(processed_image, lines)
    #return processed_image
    m1 = 0
    m2 = 0
    try:
        l1, l2, m1, m2 = draw_lanes(original_image,lines)
        cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0,0,255], 30)
        cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0,0,255], 30)
    except Exception as e:
        print(str(e))
        pass
    try:
        for coords in lines:
            coords = coords[0]
            try:
                cv2.line(processed_image, (coords[0], coords[1]), (coords[2], coords[3]), [255,0,0], 3)
                
                
            except Exception as e:
                print(str(e))
    except Exception as e:
        pass

    return processed_image,original_image, m1, m2


def main():
    countdown()
    last_time = time.time()  
    paused = False  
    while True:
        if paused == False:
            screen = grab_screen(region=(0, 40, ekplat, ekgar)) # ekrana izmeri
            new_screen, original_image, m1, m2 = process_image(cv2.resize(screen, (ekplat//2, ekgar // 2)))
            # print('FPS =  {}'.format(1 // (time.time()-last_time)))
            last_time = time.time()
            # cv2.imshow('hough lines', cv2.cvtColor(cv2.resize(new_screen, (ekplat // 3, ekgar // 3)), cv2.COLOR_BGR2RGB))
            cv2.imshow('gala linijas', cv2.cvtColor(cv2.resize(original_image, (ekplat // 3, ekgar // 3)), cv2.COLOR_BGR2RGB))
            if m1 < 0 and m2 < 0:
                ReleaseKey(W)
                PressKey(D)
                ReleaseKey(A)
            elif m1 > 0 and m2 > 0:
                PressKey(A)
                ReleaseKey(W)
                ReleaseKey(D)
            else:
                PressKey(W)
                ReleaseKey(A)
                ReleaseKey(D)

        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)wwwwwwwwwwww
            else:
                paused = True
                ReleaseKey(W)
                ReleaseKey(A)
                ReleaseKey(S)
                ReleaseKey(D)
                time.sleep(1)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

main()