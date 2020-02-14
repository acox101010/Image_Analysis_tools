import sensor, image, time, math, pyb

rtc = pyb.RTC() #create variable to hold RTC object
rtc.datetime((2020, 1, 1, 1, 0, 0, 0, 0)) #set arbitrary datetime prior to initiation
print("test start", rtc.datetime())

threshold_index_rd = 0 #0 for red
threshold_index_gr = 1 #1 for green
threshold_index_bl = 2 #2 for blue
threshold_index_k = 3 #2 for Nothing

r = 0 #incremental place holder - red
g = 0 #incremental place holder - green
b = 0 #incremental place holder - blue
k = 0 #incremental place holder - NO COLOR

r_s = 0 #initialize red state as 0
g_s = 0 #initialize green state as 0
b_s = 0 #initialize blue state as 0
k_s = 0 #initialize no state as 0

st = [] #list for holding color state
gr_counter = 0 #counter for green color state after each array is filled
rd_counter = 0 #counter for red color state after each array is filled
bl_counter = 0 #counter for blue color state after each array is filled

# Color Lab Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
thresholds = [(30, 100, 27, 127, -18, 69), # generic_red_thresholds
              (41, 92, -73, -35, -17, 54), # generic_green_thresholds
              (42, 95, -48, 61, -107, -31), # generic_blue_thresholds
              (53, 76, -32, 30, -31, 28)] # no_thresholds

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. "merge=True" merges all overlapping blobs in the image.

#function for color state identification
def fun_calls(g_s,r_s,b_s,k_s):
    if g_s == 1:
        g = 1
        StoL(1,0,0,0)
        #print("green:",g)
    elif r_s == 1:
        r = 1
        StoL(0,1,0,0)
        #print("red:",r)
    elif b_s == 1:
        b =1
        StoL(0,0,1,0)
        #print("blue:",b)
    elif k_s == 1 and g_s ==1:
        k = 1
        g = 1
        StoL(1,0,0,0)
        #print("green:",g)
    else:
        g = 0
        r = 0
        b = 0
        k = 0
        StoL(0,0,0,1)
        #print("No led")

#function for appending color state to list and limiting size
def StoL(g,r,b,k):
    if g == 1:
        st.append("gr")
        #print(st)
    elif r == 1:
        st.append("rd")
        #print(st)
    elif b == 1:
        st.append("bl")
        #print(st)
    elif g == 1 and k == 1:
        st.append("gr")
        #print(st)
    else:
        st.append("NA")
        #print(st)
#Checks if list length is of certain dimension then deletes it while counting appending state strings
    if len(st) >= 15:
        if "gr" in st:
            global gr_counter
            gr_counter = gr_counter + 1
        elif "rd" in st:
            global rd_counter
            rd_counter = rd_counter + 1
            new_rd = str(rd_counter)
            print("red identified", rtc.datetime()) #print time when red LED observed
            #snaps(new_rd) #write an image to a directory
        elif "bl" in st:
            global bl_counter
            bl_counter = bl_counter + 1
        else:
            global bl_counter
            bl_counter = bl_counter + 0 #place holder maybe
        print("Green: ",gr_counter,"Red: ", rd_counter,"Blue: ", bl_counter)
        del st[:]

#function for taking a snapshot of a red led identified
#def snaps(new_rd):
 #   sensor.alloc_extra_fb(320, 240, sensor.RGB565)
  #  img = sensor.snapshot().save(new_rd)

while(True):
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs([thresholds[threshold_index_rd]], pixels_threshold=600, area_threshold=1000, merge=True):
        # These values depend on the blob not being circular - otherwise they will be shaky.
        if blob.elongation() > 0.6:
            img.draw_edges(blob.min_corners(), color=(255,0,0))
            img.draw_line(blob.major_axis_line(), color=(0,255,0))
            img.draw_line(blob.minor_axis_line(), color=(0,0,255))
        # These values are stable all the time.
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        # Note - the blob rotation is unique to 0-180 only.
        img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)
        fun_calls(0,1,0,0)

    for blob in img.find_blobs([thresholds[threshold_index_gr]], pixels_threshold=600, area_threshold=1000, merge=True):
        # These values depend on the blob not being circular - otherwise they will be shaky.
        if blob.elongation() > 0.6:
            img.draw_edges(blob.min_corners(), color=(255,0,0))
            img.draw_line(blob.major_axis_line(), color=(0,255,0))
            img.draw_line(blob.minor_axis_line(), color=(0,0,255))
        # These values are stable all the time.
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        # Note - the blob rotation is unique to 0-180 only.
        img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)
        fun_calls(1,0,0,0)

    for blob in img.find_blobs([thresholds[threshold_index_bl]], pixels_threshold=600, area_threshold=1000, merge=True):
        # These values depend on the blob not being circular - otherwise they will be shaky.
        if blob.elongation() > 0.6:
            img.draw_edges(blob.min_corners(), color=(255,0,0))
            img.draw_line(blob.major_axis_line(), color=(0,255,0))
            img.draw_line(blob.minor_axis_line(), color=(0,0,255))
        # These values are stable all the time.
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        # Note - the blob rotation is unique to 0-180 only.
        img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)
        fun_calls(0,0,1,0)

    for blob in img.find_blobs([thresholds[threshold_index_k]], pixels_threshold=600, area_threshold=1000, merge=True):
    # These values depend on the blob not being circular - otherwise they will be shaky.
        if blob.elongation() > 0.6:
            img.draw_edges(blob.min_corners(), color=(255,0,0))
            img.draw_line(blob.major_axis_line(), color=(0,255,0))
            img.draw_line(blob.minor_axis_line(), color=(0,0,255))
    # These values are stable all the time.
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
    # Note - the blob rotation is unique to 0-180 only.
        img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)
        fun_calls(0,0,0,1)










