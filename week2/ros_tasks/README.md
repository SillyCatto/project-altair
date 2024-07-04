**220042162**

# Solutions to ROS tasks for week2
---
Each task are organized in their own catkin packages inside `src`.\
All the tasks are configured with their respective launch files.

## Task 1

Here I have a simple publisher node which publishes the string message "Hello World" to the `chatter` topic and a subscriber node subscribes to it and receives the message.

Node graph:

![png](images/task1_node_graph.png)

Run the task:\
`roslaunch task1_pub_sub task1.launch`

We get the following output:

```txt
SUMMARY
=======
PARAMETERS
 * /rosdistro: noetic
 * /rosversion: 1.16.0

NODES
  /
    listener (task1_pub_sub/listener.py)
    talker (task1_pub_sub/talker.py)

ROS_MASTER_URI=http://localhost:11311

process[talker-1]: started with pid [16395]
process[listener-2]: started with pid [16396]
[INFO] [1719751004.437854]: talker node started
[INFO] [1719751004.438020]: listener node started
[INFO] [1719751004.441331]: Hello World 1719751004.4410894
[INFO] [1719751004.541768]: Hello World 1719751004.5414493
[INFO] [1719751004.644458]: /listener I heard:  Hello World 1719751004.5414493
[INFO] [1719751004.641706]: Hello World 1719751004.6413858
[INFO] [1719751004.644186]: /listener I heard:  Hello World 1719751004.6413858
[INFO] [1719751004.7418282]: Hello World 1719751004.7418282
[INFO] [1719751004.745053]: /listener I heard:  Hello World 1719751004.7418282
...
...
```

## Task 2

Here I created a `/turtle_controller` node which publishes twist messages on the `/turtle1/cmd_vel` topic based on the user input given to it during launch. And a `/turtlesim` node subscribes to it and moves the turtle accordingly to the given command.

Node graph:

![png](images/task2_node_graph.png)

Commands are:

`A` : moving in circular path\
`B` : moving in square path\
`C` : moving in outward spiral path

Run the task:\
`roslaunch task2_turtle task2.launch cmd:=a/b/c`

Pass the command as an argument to launch file: `cmd:=a` or `cmd:=b` or `cmd:=c`

## Task 3

Here Im using gstreamer to create an rtsp server, capture the live webcam through `v4l2src` rtsp pipeline and then serve the video feed at:\
`rtsp://127.0.0.1:8554/stream`

Then I have a `/video_publisher` node which captures the stream using opencv, converts the cv2 video feed to ROS messages using `cv_bridge` and publishes it to `/video_stream` topic.

Finally, I have `/video_subscriber` node which subscribes to the topic and receives the messages. Then it converts the ROS messages back to cv2 video and displays the live video feed in a cv2 window.

Node graph:

![png](images/task3_node_graph.png)

Run the task:\
`roslaunch task3_rtsp_video_stream task3.launch`

You may need to install gstreamer and opencv stuffs:
```bash
sudo apt install ros-noetic-opencv-apps ros-noetic-cv-bridge

sudo apt-get install -y python3-gi gstreamer1.0-tools gstreamer1.0-plugins-base
gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly
gstreamer1.0-libav
```

NB: It tries to access the default camera device: `/dev/video0`\
you may need to change it accordingly incase it doesn't find the camera.\
`ls /dev | grep video`
