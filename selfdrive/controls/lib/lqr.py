import numpy as np

class LQR(object):
  def __init__(self, CP, rate=100):
    self.scale = CP.lateralTuning.pid.lqr.scale

    self.A = np.array(CP.lateralTuning.pid.lqr.a).reshape((2,2))
    self.B = np.array(CP.lateralTuning.pid.lqr.b).reshape((2,1))
    self.C = np.array(CP.lateralTuning.pid.lqr.c).reshape((1,2))
    self.K = np.array(CP.lateralTuning.pid.lqr.k).reshape((1,2))
    self.L = np.array(CP.lateralTuning.pid.lqr.l).reshape((2,1))
    self.dc_gain = CP.lateralTuning.pid.lqr.dcGain

    self.x_hat = np.array([[0], [0]])

    self.reset()

  def reset(self):
    self.output_steer = 0.0

  def update(self, v_ego, angle_steers_des, angle_steers, eps_torque):
    torque_scale = (0.45 + v_ego / 60.0)**2  # Scale actuator model with speed

    # Update Kalman filter
    angle_steers_k = float(self.C.dot(self.x_hat))
    e = angle_steers - angle_steers_k
    self.x_hat = self.A.dot(self.x_hat) + self.B.dot(eps_torque / torque_scale) + self.L.dot(e)

    u_lqr = float(angle_steers_des / self.dc_gain - self.K.dot(self.x_hat))
    print(torque_scale / self.scale, self.dc_gain)
    return torque_scale * u_lqr / self.scale
