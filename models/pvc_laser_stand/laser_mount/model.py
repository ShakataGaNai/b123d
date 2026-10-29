from models.pvc_laser_stand.geometry import make, verify

def build():
    return make("laser_mount")

def check(shape):
    verify(shape,"laser_mount")
