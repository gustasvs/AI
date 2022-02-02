# Credit to https://github.com/sentdex/pygta5
from numpy import ones,vstack
from numpy.linalg import lstsq
from statistics import mean
import numpy as np
ekplat = 1024
ekgar = 768

def draw_lanes(img, lines, color=[0, 255, 255], thickness=3):
    # if this fails, go with some default line
    try:
        # finds the maximum y value for a line marker 
        # (since we cannot assume the horizon will always be at the same point.)

        ys = []  
        for i in lines:
            for ii in i:
                ys += [ii[1],ii[3]]
        min_y = min(ys)
        max_y = ekgar
        new_lines = []
        line_dict = {}

        for idx,i in enumerate(lines):
            for xyxy in i:
                # Calculate the definition of a line, given two sets of coords.
                x_coords = (xyxy[0],xyxy[2])
                y_coords = (xyxy[1],xyxy[3])
                A = vstack([x_coords,ones(len(x_coords))]).T
                m, b = lstsq(A, y_coords)[0]

                # Calculating our new, and improved, xs
                x1 = (min_y-b) / m
                x2 = (max_y-b) / m

                line_dict[idx] = [m,b,[int(x1), min_y, int(x2), max_y]]
                new_lines.append([int(x1), min_y, int(x2), max_y])
        final_lines = {}

        for idx in line_dict:
            final_lines_copy = final_lines.copy()
            m = line_dict[idx][0]
            b = line_dict[idx][1]
            line = line_dict[idx][2]
            if len(final_lines) == 0:
                final_lines[m] = [ [m,b,line] ]
            else:
                found_copy = False
                for other_ms in final_lines_copy:
                    if not found_copy:
                        # Cik tuvu (1.2, 0.8)
                        if abs(other_ms*1.2) > abs(m) > abs(other_ms*0.8):
                            if abs(final_lines_copy[other_ms][0][1]*1.2) > abs(b) > abs(final_lines_copy[other_ms][0][1]*0.8):
                                final_lines[other_ms].append([m,b,line])
                                found_copy = True
                                break
                        else:
                            final_lines[m] = [ [m,b,line] ]
        line_counter = {}
        for lines in final_lines:
            line_counter[lines] = len(final_lines[lines])
        top_lines = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]
        line1_id = top_lines[0][0]
        line2_id = top_lines[1][0]

        def average_line(line_data):
            x1s = []
            y1s = []
            x2s = []
            y2s = []
            for data in line_data:
                x1s.append(data[2][0])
                y1s.append(data[2][1])
                x2s.append(data[2][2])
                y2s.append(data[2][3])
            return int(mean(x1s)), int(mean(y1s)), int(mean(x2s)), int(mean(y2s)) 

        l1_x1, l1_y1, l1_x2, l1_y2 = average_line(final_lines[line1_id])
        l2_x1, l2_y1, l2_x2, l2_y2 = average_line(final_lines[line2_id])

        return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], line1_id, line2_id
    except Exception as e:
        print(str(e))