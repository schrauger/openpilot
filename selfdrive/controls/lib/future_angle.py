import numpy as np

class future_angle(object):
  def __init__(self, CP, rate=100):
    self.abs_rate_avg = 0.0
    self.abs_torque_avg = 0.0
    self.torque_count = int(CP.steerActuatorDelay * float(rate))
    self.torque_samples = np.zeros(self.torque_count)
    self.torque_gain = np.zeros(15) + 1.0
    self.torque_gain_count = np.zeros(15)
    self.o_abs_rate_avg = 0.0
    self.o_abs_torque_avg = 0.0
    self.o_torque_gain = np.zeros(15) + 1.0
    self.o_torque_gain_count = np.zeros(15)
    self.inverted = 0.
    self.frame = 0
    print(len(self.torque_samples), self.torque_count)

  def update(self, v_ego, angle_steers, rate_steers, eps_torque, steer_override):

    v_index = int(v_ego // 3)
    if abs(rate_steers) > 1 and abs(rate_steers) <= 10:
      if (abs(self.inverted) >= 1.0):
        self.abs_rate_avg += 0.1 * (abs(rate_steers / 100) - self.abs_rate_avg)
        self.abs_torque_avg += 0.1 * (abs(self.torque_samples[self.frame % self.torque_count]) - self.abs_torque_avg)
        if not steer_override:
          self.torque_gain_count[v_index] += 1.0
          self.torque_gain[v_index] += ((self.abs_torque_avg / self.abs_rate_avg) - self.torque_gain[v_index]) / min(1000,self.torque_gain_count[v_index])
        else:
          self.o_torque_gain_count[v_index] += 1.0
          self.o_torque_gain[v_index] += ((self.abs_torque_avg / self.abs_rate_avg) - self.o_torque_gain[v_index]) / min(1000,self.o_torque_gain_count[v_index])
      else:
        if (rate_steers < 0) == (eps_torque < 0):
            self.inverted += 0.001
        else:
            self.inverted -= 0.001
    self.torque_samples[self.frame % self.torque_count] = eps_torque
    self.frame += 1
    if not steer_override:
      advance_angle = self.inverted * self.torque_samples.sum() / self.torque_gain[v_index]
    else:
      advance_angle = self.inverted * self.torque_samples.sum() / self.o_torque_gain[v_index]

    #if self.frame % 100 == 0:
    #    print("a = %0.2f d = %0.4f  g = %0.4f"  % (angle_steers, advance_angle, self.torque_gain[v_index]) )
    return advance_angle + angle_steers
