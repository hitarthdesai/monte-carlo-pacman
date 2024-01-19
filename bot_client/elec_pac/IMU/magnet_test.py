import py_qmc5883l
import time

sensor = py_qmc5883l.QMC5883L(output_range=py_qmc5883l.RNG_8G)
sensor.mode_continuous()

while True:
    m = sensor.get_magnet()
    print(m)
    time.sleep(1)
