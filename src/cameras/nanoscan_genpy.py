# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.9.7 | packaged by conda-forge | (default, Sep  2 2021, 17:55:20) [MSC v.1916 64 bit (AMD64)]
# From type library 'NanoScanII.tlb'
# On Thu Oct 28 13:26:31 2021
# Original Name: 4B642E36-570B-43D5-9F13-265B47410EF8x0x1x50.py
# Original Location: %AppData%\Local\Temp\gen_py\3.9
''
makepy_version = '0.5.01'
python_version = 0x30907f0

import win32com.client.CLSIDToClass, pythoncom, pywintypes
import win32com.client.util
from pywintypes import IID
from win32com.client import Dispatch

# The following 3 lines may need tweaking for the particular server
# Candidates are pythoncom.Missing, .Empty and .ArgNotFound
defaultNamedOptArg=pythoncom.Empty
defaultNamedNotOptArg=pythoncom.Empty
defaultUnnamedArg=pythoncom.Empty

CLSID = IID('{4B642E36-570B-43D5-9F13-265B47410EF8}')
MajorVersion = 1
MinorVersion = 50
LibraryFlags = 8
LCID = 0x0

class constants:
	NSAS_BWB_CLIPLEVEL_13_5       =0          # from enum NsAsBeamWidth
	NSAS_BWB_CLIPLEVEL_50         =1          # from enum NsAsBeamWidth
	NSAS_BWB_CLIPLEVEL_USER1      =3          # from enum NsAsBeamWidth
	NSAS_BWB_CLIPLEVEL_USER2      =4          # from enum NsAsBeamWidth
	NSAS_BWB_D4SIGMA              =2          # from enum NsAsBeamWidth
	NSAS_SELECT_DIVERGENCE_LENS   =0          # from enum NsAsDivergenceMethod
	NSAS_SELECT_DIVERGENCE_NUM_APERTURE=2          # from enum NsAsDivergenceMethod
	NSAS_SELECT_DIVERGENCE_SOURCE =1          # from enum NsAsDivergenceMethod
	NSAS_E_APERTURE_OUT_OF_RANGE  =-2147220991 # from enum NsAsError
	NSAS_E_AUTO_FIND_FAILED       =-2147220983 # from enum NsAsError
	NSAS_E_CLIP_OUT_OF_RANGE      =-2147220975 # from enum NsAsError
	NSAS_E_COULDNT_ACQUIRE_SYNC_REV=-2147220968 # from enum NsAsError
	NSAS_E_COULDNT_ADD_ROI        =-2147220978 # from enum NsAsError
	NSAS_E_COULDNT_CREATE_POWER_RECORD=-2147220965 # from enum NsAsError
	NSAS_E_COULDNT_DELETE_ROI     =-2147220980 # from enum NsAsError
	NSAS_E_COULDNT_EDIT_ROI       =-2147220977 # from enum NsAsError
	NSAS_E_COULDNT_GET_POWER_CALIBRATION=-2147220966 # from enum NsAsError
	NSAS_E_COULDNT_GET_ROI        =-2147220976 # from enum NsAsError
	NSAS_E_COULDNT_SET_DEVICE     =-2147220964 # from enum NsAsError
	NSAS_E_COULDNT_SET_FILTER_ON_BOARD=-2147220988 # from enum NsAsError
	NSAS_E_COULDNT_SET_GAIN_ON_BOARD=-2147220989 # from enum NsAsError
	NSAS_E_COULDNT_SET_SAMP_RES_ON_BOARD=-2147220984 # from enum NsAsError
	NSAS_E_COULDNT_SET_SPEED_ON_BOARD=-2147220985 # from enum NsAsError
	NSAS_E_DEVICE_NOT_SET         =-2147220963 # from enum NsAsError
	NSAS_E_END_OUT_OF_RANGE       =-2147220973 # from enum NsAsError
	NSAS_E_FILTER_OUT_OF_RANGE    =-2147220987 # from enum NsAsError
	NSAS_E_FOCAL_DIST_OUT_OF_BOUNDS=-2147220953 # from enum NsAsError
	NSAS_E_GAIN_OUT_OF_RANGE      =-2147220990 # from enum NsAsError
	NSAS_E_MCTRL_HOME_FAIL        =-2147220958 # from enum NsAsError
	NSAS_E_MCTRL_MOTION_FAIL      =-2147220956 # from enum NsAsError
	NSAS_E_MCTRL_NO_COMMUNICATION =-2147220960 # from enum NsAsError
	NSAS_E_MCTRL_PORT_FAIL        =-2147220957 # from enum NsAsError
	NSAS_E_MCTRL_RAIL_IN_USE      =-2147220961 # from enum NsAsError
	NSAS_E_MCTRL_RAIL_LIMIT       =-2147220959 # from enum NsAsError
	NSAS_E_MCTRL_WRONG_POSITION   =-2147220955 # from enum NsAsError
	NSAS_E_PARAMETER_NOT_SELECTED =-2147220970 # from enum NsAsError
	NSAS_E_PULSE_FREQUENCY_OUT_OF_RANGE=-2147220969 # from enum NsAsError
	NSAS_E_SAMP_RES_OUT_OF_RANGE  =-2147220954 # from enum NsAsError
	NSAS_E_SPEED_NOT_AVAILABLE    =-2147220986 # from enum NsAsError
	NSAS_E_START_BIGGER_THAN_END  =-2147220972 # from enum NsAsError
	NSAS_E_START_OUT_OF_RANGE     =-2147220974 # from enum NsAsError
	NSAS_E_TOO_MANY_ROIS          =-2147220979 # from enum NsAsError
	NSAS_E_WRONG_CAPABILITY_ID    =-2147220992 # from enum NsAsError
	NSAS_E_WRONG_DECIMATION_FACTOR=-2147220971 # from enum NsAsError
	NSAS_E_WRONG_DEVICE_ID        =-2147220962 # from enum NsAsError
	NSAS_E_WRONG_DIVERGENCE_METHOD=-2147220952 # from enum NsAsError
	NSAS_E_WRONG_PWR_CALIBRATION_INDEX=-2147220967 # from enum NsAsError
	NSAS_E_WRONG_ROI_BOUND_VALUES =-2147220982 # from enum NsAsError
	NSAS_E_WRONG_ROI_INDEX        =-2147220981 # from enum NsAsError
	NSAS_SELECT_GAUSS_FIT_ISO     =0          # from enum NsAsGaussianFitMethod
	NSAS_SELECT_GAUSS_FIT_LEAST_SQUARE=1          # from enum NsAsGaussianFitMethod
	NSAS_SELECT_PARAM_DIVERGENCE  =16384      # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_ELLIPTIC    =2048       # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_GAUSS       =1024       # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_IRRADIANCE  =512        # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_NONE        =0          # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_POS_CENTR   =32         # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_POS_PEAK    =64         # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_POWER       =4096       # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_RATIO_WIDTH_1=32768      # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_RATIO_WIDTH_2=65536      # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_RATIO_WIDTH_4SIGMA=524288     # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_RATIO_WIDTH_USER1=131072     # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_RATIO_WIDTH_USER2=262144     # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_SEP_CENTR   =128        # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_SEP_PEAK    =256        # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_TOTAL_POWER =8192       # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_WIDTH_1     =1          # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_WIDTH_2     =2          # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_WIDTH_4SIGMA=16         # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_WIDTH_USER1 =4          # from enum NsAsParameterSelection
	NSAS_SELECT_PARAM_WIDTH_USER2 =8          # from enum NsAsParameterSelection
	NSAS_SELECT_POWER_UNIT_DB     =3          # from enum NsAsPowerUnits
	NSAS_SELECT_POWER_UNIT_MW     =1          # from enum NsAsPowerUnits
	NSAS_SELECT_POWER_UNIT_UW     =0          # from enum NsAsPowerUnits
	NSAS_SELECT_POWER_UNIT_W      =2          # from enum NsAsPowerUnits
	NSAS_CAPABILITY_ID_GAIN_TABLE =1          # from enum NsAsScanHeadCapabilityID
	NSAS_CAPABILITY_ID_ROT_FREQ_TABLE=2          # from enum NsAsScanHeadCapabilityID

from win32com.client import DispatchBaseClass
class INanoScanII(DispatchBaseClass):
	CLSID = IID('{E0BD08A1-861F-40A3-B4F9-8FC25963580B}')
	coclass_clsid = IID('{FAAD0D22-C718-459A-81CA-268CCF188807}')

	def NsAsAcquireSync1Rev(self):
		return self._oleobj_.InvokeTypes(48, LCID, 1, (10, 0), (),)

	def NsAsAddROI(self, sAperture=defaultNamedNotOptArg, fLeftBound=defaultNamedNotOptArg, fRightBound=defaultNamedNotOptArg, bROIEnabled=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(24, LCID, 1, (10, 0), ((2, 0), (4, 0), (4, 0), (11, 0)),sAperture
			, fLeftBound, fRightBound, bROIEnabled)

	def NsAsAutoFind(self):
		return self._oleobj_.InvokeTypes(23, LCID, 1, (10, 0), (),)

	def NsAsAutoFindForM2K(self):
		return self._oleobj_.InvokeTypes(1000, LCID, 1, (10, 0), (),)

	def NsAsCloseMotionPort(self):
		return self._oleobj_.InvokeTypes(57, LCID, 1, (10, 0), (),)

	def NsAsDeleteROI(self, sAperture=defaultNamedNotOptArg, sROIIndex=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(25, LCID, 1, (10, 0), ((2, 0), (2, 0)),sAperture
			, sROIIndex)

	def NsAsGetApertureLimits(self, sAperture=defaultNamedNotOptArg, pfLeftBound=defaultNamedNotOptArg, pfRightBound=defaultNamedNotOptArg):
		return self._ApplyTypes_(29, 1, (10, 0), ((2, 0), (16388, 3), (16388, 3)), 'NsAsGetApertureLimits', None,sAperture
			, pfLeftBound, pfRightBound)

	def NsAsGetAveraging(self, psFinite=defaultNamedNotOptArg, psRolling=defaultNamedNotOptArg):
		return self._ApplyTypes_(68, 1, (10, 0), ((16386, 3), (16386, 3)), 'NsAsGetAveraging', None,psFinite
			, psRolling)

	def NsAsGetBeamEllipticity(self, sROIIndex=defaultNamedNotOptArg, pfBeamEllipticity=defaultNamedNotOptArg):
		return self._ApplyTypes_(45, 1, (10, 0), ((2, 0), (16388, 3)), 'NsAsGetBeamEllipticity', None,sROIIndex
			, pfBeamEllipticity)

	def NsAsGetBeamIrradiance(self, sAperture=defaultNamedNotOptArg, sROIIndex=defaultNamedNotOptArg, pfBeamIrradiance=defaultNamedNotOptArg):
		return self._ApplyTypes_(43, 1, (10, 0), ((2, 0), (2, 0), (16388, 3)), 'NsAsGetBeamIrradiance', None,sAperture
			, sROIIndex, pfBeamIrradiance)

	def NsAsGetBeamWidth(self, sAperture=defaultNamedNotOptArg, sROIIndex=defaultNamedNotOptArg, fClipLevel=defaultNamedNotOptArg, pfBeamWidth=defaultNamedNotOptArg):
		return self._ApplyTypes_(37, 1, (10, 0), ((2, 0), (2, 0), (4, 0), (16388, 3)), 'NsAsGetBeamWidth', None,sAperture
			, sROIIndex, fClipLevel, pfBeamWidth)

	def NsAsGetBeamWidth4Sigma(self, sAperture=defaultNamedNotOptArg, sROIIndex=defaultNamedNotOptArg, pfBeamWidth4Sigma=defaultNamedNotOptArg):
		return self._ApplyTypes_(38, 1, (10, 0), ((2, 0), (2, 0), (16388, 3)), 'NsAsGetBeamWidth4Sigma', None,sAperture
			, sROIIndex, pfBeamWidth4Sigma)

	def NsAsGetBeamWidth4SigmaRatio(self, sROIIndex=defaultNamedNotOptArg, pfBeamWidth4SigmaRatio=defaultNamedNotOptArg):
		return self._ApplyTypes_(62, 1, (10, 0), ((2, 0), (16388, 3)), 'NsAsGetBeamWidth4SigmaRatio', None,sROIIndex
			, pfBeamWidth4SigmaRatio)

	def NsAsGetBeamWidthRatio(self, sROIIndex=defaultNamedNotOptArg, fClipLevel=defaultNamedNotOptArg, pfBeamWidthRatio=defaultNamedNotOptArg):
		return self._ApplyTypes_(61, 1, (10, 0), ((2, 0), (4, 0), (16388, 3)), 'NsAsGetBeamWidthRatio', None,sROIIndex
			, fClipLevel, pfBeamWidthRatio)

	def NsAsGetCentroidPosition(self, sAperture=defaultNamedNotOptArg, sROIIndex=defaultNamedNotOptArg, pfCentroidPosition=defaultNamedNotOptArg):
		return self._ApplyTypes_(39, 1, (10, 0), ((2, 0), (2, 0), (16388, 3)), 'NsAsGetCentroidPosition', None,sAperture
			, sROIIndex, pfCentroidPosition)

	def NsAsGetCentroidSeparation(self, sAperture=defaultNamedNotOptArg, sROIIndex=defaultNamedNotOptArg, pfCentroidSeparation=defaultNamedNotOptArg):
		return self._ApplyTypes_(41, 1, (10, 0), ((2, 0), (2, 0), (16388, 3)), 'NsAsGetCentroidSeparation', None,sAperture
			, sROIIndex, pfCentroidSeparation)

	def NsAsGetDeviceID(self, pwDeviceID=defaultNamedNotOptArg):
		return self._ApplyTypes_(53, 1, (10, 0), ((16386, 3),), 'NsAsGetDeviceID', None,pwDeviceID
			)

	def NsAsGetDeviceList(self, pvarDeviceList=defaultNamedNotOptArg):
		return self._ApplyTypes_(67, 1, (10, 0), ((16396, 3),), 'NsAsGetDeviceList', None,pvarDeviceList
			)

	def NsAsGetDivergenceMethod(self, psDivMethod=defaultNamedNotOptArg, pfClipLevel=defaultNamedNotOptArg, pfDistance=defaultNamedNotOptArg):
		return self._ApplyTypes_(65, 1, (10, 0), ((16386, 3), (16388, 3), (16388, 3)), 'NsAsGetDivergenceMethod', None,psDivMethod
			, pfClipLevel, pfDistance)

	def NsAsGetDivergenceParameter(self, sAperture=defaultNamedNotOptArg, sROIIndex=defaultNamedNotOptArg, pfDivergence=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(66, LCID, 1, (10, 0), ((2, 0), (2, 0), (16388, 0)),sAperture
			, sROIIndex, pfDivergence)

	def NsAsGetFilter(self, sAperture=defaultNamedNotOptArg, pfFilter=defaultNamedNotOptArg):
		return self._ApplyTypes_(17, 1, (10, 0), ((2, 0), (16388, 3)), 'NsAsGetFilter', None,sAperture
			, pfFilter)

	def NsAsGetGain(self, sAperture=defaultNamedNotOptArg, psGain=defaultNamedNotOptArg):
		return self._ApplyTypes_(15, 1, (10, 0), ((2, 0), (16386, 3)), 'NsAsGetGain', None,sAperture
			, psGain)

	def NsAsGetGaussianFit(self, sAperture=defaultNamedNotOptArg, sROIIndex=defaultNamedNotOptArg, pfGoodnessFit=defaultNamedNotOptArg, pfRoughnessFit=defaultNamedNotOptArg):
		return self._ApplyTypes_(44, 1, (10, 0), ((2, 0), (2, 0), (16388, 3), (16388, 3)), 'NsAsGetGaussianFit', None,sAperture
			, sROIIndex, pfGoodnessFit, pfRoughnessFit)

	def NsAsGetHeadCapabilities(self, lCapabilityID=defaultNamedNotOptArg, pvarHeadCapability=defaultNamedNotOptArg):
		return self._ApplyTypes_(13, 1, (10, 0), ((3, 0), (16396, 3)), 'NsAsGetHeadCapabilities', None,lCapabilityID
			, pvarHeadCapability)

	def NsAsGetHeadGainTable(self, pvarGainTable=defaultNamedNotOptArg):
		return self._ApplyTypes_(74, 1, (10, 0), ((16396, 3),), 'NsAsGetHeadGainTable', None,pvarGainTable
			)

	def NsAsGetHeadScanRates(self, pvarScanRates=defaultNamedNotOptArg):
		return self._ApplyTypes_(75, 1, (10, 0), ((16396, 3),), 'NsAsGetHeadScanRates', None,pvarScanRates
			)

	def NsAsGetMaxSamplingResolution(self, pfMaxSamplingRes=defaultNamedNotOptArg):
		return self._ApplyTypes_(63, 1, (10, 0), ((16388, 3),), 'NsAsGetMaxSamplingResolution', None,pfMaxSamplingRes
			)

	def NsAsGetMeasuredRotationFreq(self, pfMeasuredRotationFreq=defaultNamedNotOptArg):
		return self._ApplyTypes_(22, 1, (10, 0), ((16388, 3),), 'NsAsGetMeasuredRotationFreq', None,pfMeasuredRotationFreq
			)

	def NsAsGetNumDevices(self, pwNumDevices=defaultNamedNotOptArg):
		return self._ApplyTypes_(55, 1, (10, 0), ((16386, 3),), 'NsAsGetNumDevices', None,pwNumDevices
			)

	def NsAsGetNumPwrCalibrations(self, nNumPwrCalibrations=defaultNamedNotOptArg):
		return self._ApplyTypes_(49, 1, (10, 0), ((16386, 3),), 'NsAsGetNumPwrCalibrations', None,nNumPwrCalibrations
			)

	def NsAsGetNumberOfROIs(self, sAperture=defaultNamedNotOptArg, psNumberOfROIs=defaultNamedNotOptArg):
		return self._ApplyTypes_(27, 1, (10, 0), ((2, 0), (16386, 3)), 'NsAsGetNumberOfROIs', None,sAperture
			, psNumberOfROIs)

	def NsAsGetPeakPosition(self, sAperture=defaultNamedNotOptArg, sROIIndex=defaultNamedNotOptArg, pfPeakPosition=defaultNamedNotOptArg):
		return self._ApplyTypes_(40, 1, (10, 0), ((2, 0), (2, 0), (16388, 3)), 'NsAsGetPeakPosition', None,sAperture
			, sROIIndex, pfPeakPosition)

	def NsAsGetPeakSeparation(self, sAperture=defaultNamedNotOptArg, sROIIndex=defaultNamedNotOptArg, pfPeakSeparation=defaultNamedNotOptArg):
		return self._ApplyTypes_(42, 1, (10, 0), ((2, 0), (2, 0), (16388, 3)), 'NsAsGetPeakSeparation', None,sAperture
			, sROIIndex, pfPeakSeparation)

	def NsAsGetPower(self, nROIIndex=defaultNamedNotOptArg, pfROIPower=defaultNamedNotOptArg):
		return self._ApplyTypes_(52, 1, (10, 0), ((2, 0), (16388, 3)), 'NsAsGetPower', None,nROIIndex
			, pfROIPower)

	def NsAsGetPowerCalibration(self, sIndexCalibration=defaultNamedNotOptArg, pvarPwrCalibration=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(50, LCID, 1, (10, 0), ((2, 0), (16396, 0)),sIndexCalibration
			, pvarPwrCalibration)

	def NsAsGetPowerCalibrationBreakOut(self, sIndexCalibration=defaultNamedNotOptArg, name=defaultNamedNotOptArg, refPower=defaultNamedNotOptArg, wavelength=defaultNamedNotOptArg):
		return self._ApplyTypes_(72, 1, (10, 0), ((2, 0), (16392, 3), (16388, 3), (16388, 3)), 'NsAsGetPowerCalibrationBreakOut', None,sIndexCalibration
			, name, refPower, wavelength)

	def NsAsGetPulseFrequency(self, pfPulseFrequency=defaultNamedNotOptArg):
		return self._ApplyTypes_(47, 1, (10, 0), ((16388, 3),), 'NsAsGetPulseFrequency', None,pfPulseFrequency
			)

	def NsAsGetROI(self, sAperture=defaultNamedNotOptArg, sROIIndex=defaultNamedNotOptArg, pfLeftBound=defaultNamedNotOptArg, pfRightBound=defaultNamedNotOptArg
			, pbROIEnabled=defaultNamedNotOptArg):
		return self._ApplyTypes_(28, 1, (10, 0), ((2, 0), (2, 0), (16388, 3), (16388, 3), (16395, 3)), 'NsAsGetROI', None,sAperture
			, sROIIndex, pfLeftBound, pfRightBound, pbROIEnabled)

	def NsAsGetRotationFrequency(self, pfRotationFrequency=defaultNamedNotOptArg):
		return self._ApplyTypes_(21, 1, (10, 0), ((16388, 3),), 'NsAsGetRotationFrequency', None,pfRotationFrequency
			)

	def NsAsGetSamplingResolution(self, sAperture=defaultNamedNotOptArg, pfSamplingResolution=defaultNamedNotOptArg):
		return self._ApplyTypes_(19, 1, (10, 0), ((2, 0), (16388, 3)), 'NsAsGetSamplingResolution', None,sAperture
			, pfSamplingResolution)

	def NsAsGetSelectedParameters(self, plParameters=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(32, LCID, 1, (10, 0), ((16387, 0),),plParameters
			)

	def NsAsGetTotalPower(self, pfTotalPower=defaultNamedNotOptArg):
		return self._ApplyTypes_(51, 1, (10, 0), ((16388, 3),), 'NsAsGetTotalPower', None,pfTotalPower
			)

	def NsAsGetUserClipLevel1(self, pfUserClipLevel1=defaultNamedNotOptArg):
		return self._ApplyTypes_(35, 1, (10, 0), ((16388, 3),), 'NsAsGetUserClipLevel1', None,pfUserClipLevel1
			)

	def NsAsGetUserClipLevel2(self, pfUserClipLevel2=defaultNamedNotOptArg):
		return self._ApplyTypes_(36, 1, (10, 0), ((16388, 3),), 'NsAsGetUserClipLevel2', None,pfUserClipLevel2
			)

	def NsAsGo2Position(self, fPosition=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(58, LCID, 1, (10, 0), ((4, 0),),fPosition
			)

	def NsAsIsSignalSaturated(self, sAperture=defaultNamedNotOptArg, bSignalSaturated=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(59, LCID, 1, (10, 0), ((2, 0), (16395, 0)),sAperture
			, bSignalSaturated)

	def NsAsOpenMotionPort(self, strMotionPort=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(56, LCID, 1, (10, 0), ((8, 0),),strMotionPort
			)

	def NsAsPumpACQ(self):
		return self._oleobj_.InvokeTypes(71, LCID, 1, (10, 0), (),)

	def NsAsReadProfile(self, sAperture=defaultNamedNotOptArg, fStartPosition=defaultNamedNotOptArg, fEndPosition=defaultNamedNotOptArg, sDecimationFactor=defaultNamedNotOptArg
			, pvarProfileAmplitude=defaultNamedNotOptArg, pvarProfilePosition=defaultNamedNotOptArg):
		return self._ApplyTypes_(30, 1, (10, 0), ((2, 0), (4, 0), (4, 0), (2, 0), (16396, 3), (16396, 3)), 'NsAsReadProfile', None,sAperture
			, fStartPosition, fEndPosition, sDecimationFactor, pvarProfileAmplitude, pvarProfilePosition
			)

	def NsAsRecompute(self):
		return self._oleobj_.InvokeTypes(60, LCID, 1, (10, 0), (),)

	def NsAsRunComputation(self):
		return self._oleobj_.InvokeTypes(70, LCID, 1, (10, 0), (),)

	def NsAsSelectParameters(self, lParameters=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(31, LCID, 1, (10, 0), ((3, 0),),lParameters
			)

	def NsAsSetAveraging(self, psFinite=defaultNamedNotOptArg, psRolling=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(69, LCID, 1, (10, 0), ((2, 0), (2, 0)),psFinite
			, psRolling)

	def NsAsSetDeviceID(self, wDeviceID=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(54, LCID, 1, (10, 0), ((2, 0),),wDeviceID
			)

	def NsAsSetDivergenceMethod(self, sDivMethod=defaultNamedNotOptArg, fClipLevel=defaultNamedNotOptArg, fDistance=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(64, LCID, 1, (10, 0), ((2, 0), (4, 0), (4, 0)),sDivMethod
			, fClipLevel, fDistance)

	def NsAsSetFilter(self, sAperture=defaultNamedNotOptArg, fFilter=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(16, LCID, 1, (10, 0), ((2, 0), (4, 0)),sAperture
			, fFilter)

	def NsAsSetGain(self, sAperture=defaultNamedNotOptArg, sGain=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(14, LCID, 1, (10, 0), ((2, 0), (2, 0)),sAperture
			, sGain)

	def NsAsSetPulseFrequency(self, fPulseFrequency=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(46, LCID, 1, (10, 0), ((4, 0),),fPulseFrequency
			)

	def NsAsSetRotationFrequency(self, fRotationFrequency=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (10, 0), ((4, 0),),fRotationFrequency
			)

	def NsAsSetSamplingResolution(self, fSamplingResolution=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(18, LCID, 1, (10, 0), ((4, 0),),fSamplingResolution
			)

	def NsAsSetUserClipLevel1(self, fUserClipLevel1=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(33, LCID, 1, (10, 0), ((4, 0),),fUserClipLevel1
			)

	def NsAsSetUserClipLevel2(self, fUserClipLevel2=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(34, LCID, 1, (10, 0), ((4, 0),),fUserClipLevel2
			)

	def NsAsUpdateROI(self, sAperture=defaultNamedNotOptArg, sROIIndex=defaultNamedNotOptArg, fLeftBound=defaultNamedNotOptArg, fRightBound=defaultNamedNotOptArg
			, bROIEnabled=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(26, LCID, 1, (10, 0), ((2, 0), (2, 0), (4, 0), (4, 0), (11, 0)),sAperture
			, sROIIndex, fLeftBound, fRightBound, bROIEnabled)

	_prop_map_get_ = {
		"NsAsAutoROI": (3, 2, (11, 0), (), "NsAsAutoROI", None),
		"NsAsBeamWidthBasis": (73, 2, (2, 0), (), "NsAsBeamWidthBasis", None),
		"NsAsDataAcquisition": (2, 2, (11, 0), (), "NsAsDataAcquisition", None),
		"NsAsDefaultCalibration": (7, 2, (2, 0), (), "NsAsDefaultCalibration", None),
		"NsAsGaussFitMethod": (11, 2, (2, 0), (), "NsAsGaussFitMethod", None),
		"NsAsMagnificationFactor": (12, 2, (4, 0), (), "NsAsMagnificationFactor", None),
		"NsAsMultiROIMode": (9, 2, (11, 0), (), "NsAsMultiROIMode", None),
		"NsAsPowerUnits": (8, 2, (2, 0), (), "NsAsPowerUnits", None),
		"NsAsPulsedMode": (6, 2, (3, 0), (), "NsAsPulsedMode", None),
		"NsAsRailLength": (10, 2, (4, 0), (), "NsAsRailLength", None),
		"NsAsShowWindow": (1, 2, (11, 0), (), "NsAsShowWindow", None),
		"NsAsTrackFilter": (5, 2, (11, 0), (), "NsAsTrackFilter", None),
		"NsAsTrackGain": (4, 2, (11, 0), (), "NsAsTrackGain", None),
	}
	_prop_map_put_ = {
		"NsAsAutoROI" : ((3, LCID, 4, 0),()),
		"NsAsBeamWidthBasis" : ((73, LCID, 4, 0),()),
		"NsAsDataAcquisition" : ((2, LCID, 4, 0),()),
		"NsAsDefaultCalibration" : ((7, LCID, 4, 0),()),
		"NsAsGaussFitMethod" : ((11, LCID, 4, 0),()),
		"NsAsMagnificationFactor" : ((12, LCID, 4, 0),()),
		"NsAsMultiROIMode" : ((9, LCID, 4, 0),()),
		"NsAsPowerUnits" : ((8, LCID, 4, 0),()),
		"NsAsPulsedMode" : ((6, LCID, 4, 0),()),
		"NsAsRailLength" : ((10, LCID, 4, 0),()),
		"NsAsShowWindow" : ((1, LCID, 4, 0),()),
		"NsAsTrackFilter" : ((5, LCID, 4, 0),()),
		"NsAsTrackGain" : ((4, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

from win32com.client import CoClassBaseClass
# This CoClass is known by the name 'Photon-NanoScan'
class NsAs(CoClassBaseClass): # A CoClass
	CLSID = IID('{FAAD0D22-C718-459A-81CA-268CCF188807}')
	coclass_sources = [
	]
	coclass_interfaces = [
		INanoScanII,
	]
	default_interface = INanoScanII

RecordMap = {
	'NsAsPwrCalibration': '{250613B4-7DD0-44B8-9EE5-6E6C7FEA653D}',
}

CLSIDToClassMap = {
	'{E0BD08A1-861F-40A3-B4F9-8FC25963580B}' : INanoScanII,
	'{FAAD0D22-C718-459A-81CA-268CCF188807}' : NsAs,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
}


NamesToIIDMap = {
	'INanoScanII' : '{E0BD08A1-861F-40A3-B4F9-8FC25963580B}',
}

win32com.client.constants.__dicts__.append(constants.__dict__)

