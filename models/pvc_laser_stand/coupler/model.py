from models.pvc_laser_stand.geometry import make, verify

def build():
    return make("coupler")

def check(shape):
    verify(shape,"coupler")
