# virtual-wall
Virtual wall to interact with through touch, enabled through MyntEye Stereocam.

#### Requirements
  * Docker - to run ROS environemnt remotely through a docker container
    * Build the image from the directory through this
      ```console
       docker build -t ros-dock .
       ```
  * Install python requirements in reqs.txt
    ```console 
     pip install -r reqs.txt
     ```
   
 #### Run sequence
   * launch the container
      ``` console 
        docker run --name ros_dock_app  -it --device=/dev/video1 -p 11311:11311 --rm  ros-dock
      ```
   * Create audio samples
      ```console
          python audio_gen.py
      ```
  * Run the main node
      ```console
         python mazer.py
      ```
    
