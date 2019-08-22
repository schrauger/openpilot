import numpy as np
from selfdrive.controls.lib.drive_helpers import get_steer_max
from common.numpy_fast import clip, interp
from cereal import log
from selfdrive.kegman_conf import kegman_conf
from common.realtime import sec_since_boot

class LatControlLQR(object):
  def __init__(self, CP, rate=100):
    self.sat_flag = False
    if CP.lateralTuning.which() == "lqr":
      lqr = CP.lateralTuning.lqr
    else:
      lqr = CP.lqr2
    self.scale = lqr.scale
    self.ki = lqr.ki
    kegman_conf(CP)
    self.frame = 0
    self.react_mpc = 0.0  #lqr.reactMPC
    self.damp_mpc = 0.1  #lqr.dampMPC
    self.damp_angle_steers_des = 0.0
    self.damp_rate_steers_des = 0.0
    self.angle_bias = 0.

    self.A = np.array(lqr.a).reshape((2,2))
    self.B = np.array(lqr.b).reshape((2,1))
    self.C = np.array(lqr.c).reshape((1,2))
    self.K = np.array(lqr.k).reshape((1,2))
    self.L = np.array(lqr.l).reshape((2,1))
    self.dc_gain = lqr.dcGain

    self.x_hat = np.array([[0], [0]])
    self.i_unwind_rate = 0.3 / rate
    self.i_rate = 1.0 / rate
    self.lqr_output = 0.0

    self.reset()

  def reset(self):
    self.i_lqr = 0.0
    self.output_steer = 0.0

  def live_tune(self, CP):
    self.frame += 1
    if self.frame % 300 == 0:
      # live tuning through /data/openpilot/tune.py overrides interface.py settings
      kegman = kegman_conf()
      self.react_mpc = float(kegman.conf['reactMPC'])
      self.damp_mpc = float(kegman.conf['dampMPC'])

  def update(self, active, v_ego, angle_steers, angle_steers_rate, eps_torque, steer_override, blinkers_on, CP, VM, path_plan, live_params, live_mpc):
    lqr_log = log.ControlsState.LateralLQRState.new_message()

    torque_scale = (0.45 + v_ego / 60.0)**2  # Scale actuator model with speed

    max_bias_change = 0.001  #min(0.001, 0.0002 / (abs(self.angle_bias) + 0.000001))
    max_bias_change *= interp(abs(angle_steers - live_params.angleOffsetAverage - self.angle_bias), [0.0, 5.0], [0.25, 1.0])
    max_bias_change *= interp(abs(path_plan.rateSteers), [1.0, 5.0], [0.25, 1.0])
    self.angle_bias = float(np.clip(live_params.angleOffset - live_params.angleOffsetAverage, self.angle_bias - max_bias_change, self.angle_bias + max_bias_change))

    if len(live_mpc.delta) > 0:
      #if (live_mpc.delta[2] - live_mpc.delta[1]) > 0 != (live_mpc.delta[19] - live_mpc.delta[1]) > 0 and abs(live_mpc.delta[19]) > abs(live_mpc.delta[2]):
      #  counter_steer = abs(live_mpc.delta[2] / live_mpc.delta[19])
      #else:
      counter_steer = 1.0

      self.damp_angle_steers_des += counter_steer * (interp(sec_since_boot() + self.damp_mpc + self.react_mpc, path_plan.mpcTimes, path_plan.mpcAngles) - self.damp_angle_steers_des) / max(1.0, self.damp_mpc * 100.)

    # Subtract offset. Zero angle should correspond to zero torque
    self.angle_steers_des = path_plan.angleSteers
    self.damp_angle_steers = angle_steers - self.angle_bias

    angle_steers -= (live_params.angleOffsetAverage + self.angle_bias)
    angle_steers_des = self.damp_angle_steers_des - path_plan.angleOffset

    # Update Kalman filter
    angle_steers_k = float(self.C.dot(self.x_hat))
    e = angle_steers - angle_steers_k
    self.x_hat = self.A.dot(self.x_hat) + self.B.dot(eps_torque / torque_scale) + self.L.dot(e)

    if v_ego < 0.3 or not active:
      lqr_log.active = False
      self.reset()
    else:
      lqr_log.active = True

      # LQR
      u_lqr = float(angle_steers_des / self.dc_gain - self.K.dot(self.x_hat))

      # Integrator
      if steer_override:
        self.i_lqr -= self.i_unwind_rate * float(np.sign(self.i_lqr))
      else:
        self.i_lqr += self.ki * self.i_rate * (angle_steers_des - angle_steers_k)

      lqr_output = torque_scale * u_lqr / self.scale
      self.lqr_output = lqr_output
      #self.i_lqr = clip(self.i_lqr, -1.0 - lqr_output, 1.0 - lqr_output) # (LQR + I) has to be between -1 and 1

      self.output_steer = lqr_output + self.i_lqr

      # Clip output
      steers_max = get_steer_max(CP, v_ego)
      #self.output_steer = clip(self.output_steer, -steers_max, steers_max)

    lqr_log.steerAngle = angle_steers_k + path_plan.angleOffset
    lqr_log.i = self.i_lqr
    lqr_log.output = self.output_steer
    return self.output_steer, float(self.angle_steers_des), lqr_log
