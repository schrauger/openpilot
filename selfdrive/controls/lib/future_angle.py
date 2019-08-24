import numpy as np

class future_angle(object):
  def __init__(self, CP, rate=100):
    self.torque_count = int(CP.steerActuatorDelay * float(rate))
    self.torque_samples = np.zeros(self.torque_count)
    self.angle_samples = np.zeros(self.torque_count)
    self.torque_gain_outward = np.zeros(15) + 1.0
    self.torque_gain_outward_count = np.zeros(15)
    self.torque_gain_inward = np.zeros(15) + 1.0
    self.torque_gain_inward_count = np.zeros(15)
    self.o_torque_gain_outward = np.zeros(15) + 1.0
    self.o_torque_gain_outward_count = np.zeros(15)
    self.o_torque_gain_inward = np.zeros(15) + 1.0
    self.o_torque_gain_inward_count = np.zeros(15)

    self.inverted = 0.
    self.frame = 0
    self.advance_angle = 0.
    print(len(self.torque_samples), self.torque_count)

  def update(self, v_ego, angle_steers, rate_steers, eps_torque, steer_override):

    v_index = int(v_ego // 3)

    isOutward = (angle_steers > 0) == (self.inverted * eps_torque > 0)
    isConsistent = max(self.torque_samples) * min(self.torque_samples) >= 0 and max(self.angle_samples) * min(self.angle_samples) >= 0

    if isConsistent and abs(self.inverted) >= 1.0 and self.torque_samples.sum != 0 and abs(angle_steers) > 1.0 and abs(rate_steers) > 1.0 and abs(eps_torque) > 1.0:
      if isOutward:
        if not steer_override:
          self.torque_gain_outward_count[v_index] += 1.0
          self.torque_gain_outward[v_index] += ((abs(self.torque_samples[self.frame % self.torque_count]) / abs(rate_steers)) - self.torque_gain_outward[v_index]) / min(1000,self.torque_gain_outward_count[v_index])
        else:
          self.o_torque_gain_outward_count[v_index] += 1.0
          self.o_torque_gain_outward[v_index] += ((abs(self.torque_samples[self.frame % self.torque_count]) / abs(rate_steers)) - self.o_torque_gain_outward[v_index]) / min(1000,self.o_torque_gain_outward_count[v_index])

      else:
        if not steer_override:
          self.torque_gain_inward_count[v_index] += 1.0
          self.torque_gain_inward[v_index] += ((abs(self.torque_samples[self.frame % self.torque_count]) / abs(rate_steers)) - self.torque_gain_inward[v_index]) / min(1000,self.torque_gain_inward_count[v_index])
        else:
          self.o_torque_gain_inward_count[v_index] += 1.0
          self.o_torque_gain_inward[v_index] += ((abs(self.torque_samples[self.frame % self.torque_count]) / abs(rate_steers)) - self.o_torque_gain_inward[v_index]) / min(1000,self.o_torque_gain_inward_count[v_index])

    elif abs(self.inverted) < 1.0 and abs(rate_steers * self.torque_samples[self.frame % self.torque_count]) > 0:
      if (rate_steers < 0) == (self.torque_samples[self.frame % self.torque_count] < 0):
        self.inverted += 0.001
      else:
        self.inverted -= 0.001

    #if isConsistent:
    self.torque_samples[self.frame % self.torque_count] = eps_torque
    self.angle_samples[self.frame % self.torque_count] = angle_steers
    torque_sum = self.inverted * self.torque_samples.sum()
    self.frame += 1
    if isOutward and torque_sum * eps_torque > 0:
      if not steer_override and self.torque_gain_outward_count[v_index] > 500:
        self.advance_angle = torque_sum / self.torque_gain_outward[v_index]
      elif self.o_torque_gain_outward_count[v_index] > 500:
        self.advance_angle = torque_sum / self.o_torque_gain_outward[v_index]
      else:
        self.advance_angle = 0
    elif not isOutward and torque_sum * eps_torque > 0:
      if not steer_override and self.torque_gain_inward_count[v_index] > 500:
        self.advance_angle = torque_sum / self.torque_gain_inward[v_index]
      elif self.o_torque_gain_inward_count[v_index] > 500:
        self.advance_angle = torque_sum / self.o_torque_gain_inward[v_index]
      else:
        self.advance_angle = 0
    return 0.01 * self.advance_angle   #  max(-1.0, min(1.0, self.advance_angle))
