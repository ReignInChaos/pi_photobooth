# pi_photobooth

At the core, this photobooth is targeted at controlling DSLR cameras and using Raspberry Pi GPIO for push button control

This photobooth is based on the following libraries
- libgphoto2 and gphoto2 
- piggyphoto (can possibly be written out with other python libraries)
- pygame (for image visualization)
- Google API (for upload)

MUCH more testing needs to be done, hard coding obviously to be removed, etc

Had to update the libgphoto reference in piggyphoto in order to communicate with the camera.  This may be due to default installations and path.

#libgphoto2dll = 'libgphoto2.so.2.4.0'
#libgphoto2dll = 'libgphoto2.so'
# 2.4.6
libgphoto2dll = '/usr/local/lib/libgphoto2.so'
# 2.4.8
#libgphoto2dll = '/usr/local/lib/libgphoto2.so.2'
# SVN
#libgphoto2dll = '/usr/local/lib/libgphoto2.so.6'
