from models.pvc_laser_stand.geometry import make, verify

def build():
    return make("stake")

def check(shape):
    verify(shape,"stake")
