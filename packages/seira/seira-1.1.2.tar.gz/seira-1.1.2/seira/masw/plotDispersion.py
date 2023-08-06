import matplotlib.pyplot as plt
import numpy as np

def plotDispersion(f, c, A, resolution, fmin, fmax):
  """Plot dispersion curves with selected frequency, usually we use 0-50 Hz 

  Args:
      f (_type_): Frequency test [Hz]
      c (_type_): Velocity test [m/s]
      A (_type_): Amplitude 
      resolution (_type_): Grid resolution (e.g 100)
      fmin (_type_): Minimum frequency used [Hz]
      fmax (_type_): Max frequency used [Hz]

  Returns:
      fplot: frequencies filtered 
      cplot: velocities filtered
      Aplot: amplitudes filtered
  """
  RemoveMin = np.abs((f[:,0] - fmin))
  RemoveMax = np.abs((f[:,0] - fmax))
  IdxMin = np.array(np.where(RemoveMin==np.min(RemoveMin))).flatten()[0]
  IdxMax = np.array(np.where(RemoveMax==np.min(RemoveMax))).flatten()[0]
  valMin, valMax = RemoveMin[IdxMin], RemoveMax[IdxMax]
  Aplot = A[IdxMin:IdxMax+1,:]
  fplot = f[IdxMin:IdxMax+1,:]
  cplot = c[IdxMin:IdxMax+1,:]


  return valMin, valMax, IdxMin, IdxMax, fplot, cplot, Aplot