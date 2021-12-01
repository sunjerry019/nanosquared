using System;

namespace NanoScanLibrary
{
    public partial class NanoScan
    {
        /* This file provides a mapping to (almost) all DLL functions. All pass-by-references have been written out and handled in C#.
         * This should reduce a lot of the issues related to using these function
         * 
         * This results in some inconsistencies in terms of whether the function returns the error code or the expected result
         * For reference, any getter will return the value to be gotten instead of the error code. 
         * 
         * Where multiple parameters are to be gotten, an array is used (for now). If this causes problems with Python, then it will be changed.
         * 
         * Signatures of functions will be that of the manual sans all pass-by-reference variables.
         */

        public int InitNs() { return InitNsInterop(); }
        public void ShutdownNS() { ShutdownNsInterop(); }
        // public int GetHeadCapabilities(long capabilityID, [In][Out][MarshalAs) { return NsInteropGetHeadCapabilities(capabilityID, [In][Out][MarshalAs); }
        public int SetGain(short aperture, short gain) { return NsInteropSetGain(aperture, gain); }
        public short GetGain(short aperture) 
        { 
            short gain = -1;
            NsInteropGetGain(aperture, ref gain);
            return gain;
        }
        public int SetFilter(short aperture, float filter) { return NsInteropSetFilter(aperture, filter); }
        public float GetFilter(short aperture) 
        {
            float filter = -0.1F;
            NsInteropGetFilter(aperture, ref filter);
            return filter;
        }
        public int SetSamplingResolution(float samplingResolution) { return NsInteropSetSamplingResolution(samplingResolution); }
        public float GetSamplingResolution(short aperture) 
        {
            float samplingResolution = -0.1F;
            NsInteropGetSamplingResolution(aperture, ref samplingResolution);
            return samplingResolution;
        }
        public int SetRotationFrequency(float rotationFrequency) { return NsInteropSetRotationFrequency(rotationFrequency); }
        public float GetRotationFrequency() 
        {
            float rotationFrequency = -0.1F;
            NsInteropGetRotationFrequency(ref rotationFrequency);
            return rotationFrequency;
        }
        public float GetMeasuredRotationFreq() 
        {
            float measuredRotationFreq = -0.1F;
            NsInteropGetMeasuredRotationFreq(ref measuredRotationFreq);
            return measuredRotationFreq;
        }
        public int AutoFind() { return NsInteropAutoFind(); }
        public int AddROI(short aperture, float leftBound, float rightBound, bool roiEnabled) { return NsInteropAddROI(aperture, leftBound, rightBound, roiEnabled); }
        public int DeleteROI(short aperture, short roiIndex) { return NsInteropDeleteROI(aperture, roiIndex); }
        public int UpdateROI(short aperture, short roiIndex, float leftBound, float rightBound, bool roiEnabled) { return NsInteropUpdateROI(aperture, roiIndex, leftBound, rightBound, roiEnabled); }
        public short GetNumberOfROIs(short aperture) 
        {
            short numberOfROIs = -1;
            NsInteropGetNumberOfROIs(aperture, ref numberOfROIs);
            return numberOfROIs;
        }
        public float[] GetROI(short aperture, short sROIIndex) 
        {
            float leftBound  = -0.1F;
            float rightBound = -0.1F;
            bool roiEnabled = false;

            NsInteropGetROI(aperture, sROIIndex, ref leftBound, ref rightBound, ref roiEnabled);

            float[] ret = {leftBound, rightBound, Convert.ToSingle(roiEnabled)};

            return ret;
        }
        public float[] GetApertureLimits(short aperture) 
        {
            float startPosition = -0.1F;
            float EndPosition = -0.1F;
            NsInteropGetApertureLimits(aperture, ref startPosition, ref EndPosition);

            float[] ret = { startPosition, EndPosition };

            return ret;
        }
        // public int ReadProfile() { return NsInteropReadProfile(); }
        public int SelectParameters(ulong parameters) { return NsInteropSelectParameters(parameters); }
        public ulong GetSelectedParameters() 
        {
            ulong parameters = 0; 
            NsInteropGetSelectedParameters(ref parameters);
            return parameters;
        }
        public int SetUserClipLevel1(float userClipLevel1) { return NsInteropSetUserClipLevel1(userClipLevel1); }
        public int SetUserClipLevel2(float userClipLevel2) { return NsInteropSetUserClipLevel2(userClipLevel2); }
        public float GetUserClipLevel1() 
        {
            float userClipLevel1 = -0.1F;
            NsInteropGetUserClipLevel1(ref userClipLevel1);
            return userClipLevel1;
        }
        public float GetUserClipLevel2()
        {
            float userClipLevel2 = -0.1F;
            NsInteropGetUserClipLevel2(ref userClipLevel2);
            return userClipLevel2;
        }
        public float GetBeamWidth(short aperture, short roiIndex, float clipLevel) 
        {
            float beamWidth = -0.1F;
            NsInteropGetBeamWidth(aperture, roiIndex, clipLevel, ref beamWidth);
            return beamWidth;
        }
        public float GetBeamWidth4Sigma(short aperture, short roiIndex) 
        {
            float beamWidth4Sigma = -0.1F;
            NsInteropGetBeamWidth4Sigma(aperture, roiIndex, ref beamWidth4Sigma);
            return beamWidth4Sigma;
        }
        public float GetCentroidPosition(short aperture, short roiIndex) 
        {
            float centroidPosition = -0.1F;
            NsInteropGetCentroidPosition(aperture, roiIndex, ref centroidPosition);
            return centroidPosition;
        }
        public float GetPeakPosition(short aperture, short roiIndex) 
        {
            float peakPosition = -0.1F;
            NsInteropGetPeakPosition(aperture, roiIndex, ref peakPosition);
            return peakPosition;
        }
        public float GetCentroidSeparation(short aperture, short roiIndex) 
        {
            float centroidSeparation = -0.1F;
            NsInteropGetCentroidSeparation(aperture, roiIndex, ref centroidSeparation);
            return centroidSeparation;
        }
        public float GetPeakSeparation(short aperture, short roiIndex)
        {
            float peakSeparation = -0.1F;
            NsInteropGetPeakSeparation(aperture, roiIndex, ref peakSeparation);
            return peakSeparation; 
        }
        public float GetBeamIrradiance(short aperture, short roiIndex)
        {
            float beamIrradiance = -0.1F;
            NsInteropGetBeamIrradiance(aperture, roiIndex, ref beamIrradiance);
            return beamIrradiance; 
        }
        public float[] GetGaussianFit(short aperture, short roiIndex)
        {
            float goodnessFit = -0.1F;
            float roughnessFit = -0.1F;
            NsInteropGetGaussianFit(aperture, roiIndex, ref goodnessFit, ref roughnessFit);

            float[] ret = { goodnessFit, roughnessFit };

            return ret;
        }
        public float GetBeamEllipticity(short roiIndex) 
        {
            float beamEllipticity = -0.1F;
            NsInteropGetBeamEllipticity(roiIndex, ref beamEllipticity);
            return beamEllipticity;
        }
        public int SetPulseFrequency(float pulseFrequency) { return NsInteropSetPulseFrequency(pulseFrequency); }
        public float GetPulseFrequency() 
        {
            float pulseFrequency = -0.1F;
            NsInteropGetPulseFrequency(ref pulseFrequency);
            return pulseFrequency;
        }
        public int AcquireSync1Rev() { return NsInteropAcquireSync1Rev(); }
        public short GetNumPwrCalibrations() 
        {
            short numPwrCalibrations = -1;
            NsInteropGetNumPwrCalibrations(ref numPwrCalibrations);
            return numPwrCalibrations;
        }
        // public int GetPowerCalibration(short indexCalibration, [In][Out][MarshalAs) { return NsInteropGetPowerCalibration(indexCalibration, [In][Out][MarshalAs); }
        public float GetTotalPower() 
        {
            float totalPower = -0.1F;
            NsInteropGetTotalPower(ref totalPower);
            return totalPower;
        }
        public float GetPower(short roiIndex) 
        {
            float roiPower = -0.1F;
            NsInteropGetPower(roiIndex, ref roiPower);
            return roiPower;
        }
        public short GetDeviceID() 
        {
            short deviceID = -1;
            NsInteropGetDeviceID(ref deviceID);
            return deviceID;
        }
        public int SetDeviceID(short deviceID) { return NsInteropSetDeviceID(deviceID); }
        public short GetNumDevices() 
        {
            short numDevices = -1;
            NsInteropGetNumDevices(ref numDevices);
            return numDevices;
        }
        public int OpenMotionPort(string motionPort) { return NsInteropOpenMotionPort(motionPort); }
        public int CloseMotionPort() { return NsInteropCloseMotionPort(); }
        public int Go2Position(float position) { return NsInteropGo2Position(position); }
        public bool IsSignalSaturated(short aperture) 
        {
            bool isSignalSaturated = false;
            NsInteropIsSignalSaturated(aperture, ref isSignalSaturated);
            return isSignalSaturated;
        }
        public int Recompute() { return NsInteropRecompute(); }
        public float GetBeamWidthRatio(short roiIndex, float clipLevel) 
        {
            float beamWidthRatio = -0.1F;
            NsInteropGetBeamWidthRatio(roiIndex, clipLevel, ref beamWidthRatio);
            return beamWidthRatio;
        }
        public float GetBeamWidth4SigmaRatio(short roiIndex) 
        {
            float beamWidth4SigmaRatio = -0.1F;
            NsInteropGetBeamWidth4SigmaRatio(roiIndex, ref beamWidth4SigmaRatio);
            return beamWidth4SigmaRatio;
        }
        public float GetMaxSamplingResolution() 
        {
            float maxSamplingRes = -0.1F;
            NsInteropGetMaxSamplingResolution(ref maxSamplingRes);
            return maxSamplingRes;
        }
        public int SetDivergenceMethod(short divMethod, float clipLevel, float distance) { return NsInteropSetDivergenceMethod(divMethod, clipLevel, distance); }
        public float[] GetDivergenceMethod() 
        {
            short divMethod = -1;
            float clipLevel = -0.1F;
            float distance = -0.1F;
            NsInteropGetDivergenceMethod(ref divMethod, ref clipLevel, ref distance);

            float[] ret = { (float) divMethod, clipLevel, distance };
            return ret;
        }
        public float GetDivergenceParameter(short aperture, short roiIndex) 
        {
            float divergence = -0.1F;
            NsInteropGetDivergenceParameter(aperture, roiIndex, ref divergence);
            return divergence;
        }
        // public int GetDeviceList([In][Out][MarshalAs) { return NsInteropGetDeviceList([In][Out][MarshalAs); }
        public short[] GetAveraging() 
        {
            short finite  = -1;
            short rolling = -1;
            NsInteropGetAveraging(ref finite, ref rolling);

            short[] ret = { finite, rolling };
            return ret; 
        }
        public int SetAveraging(short finite, short rolling) { return NsInteropSetAveraging(finite, rolling); }
        public int RunComputation() { return NsInteropRunComputation(); }
        // public void GetHeadGainTable(long capabilityID, [In][Out][MarshalAs) { NsInteropGetHeadGainTable(capabilityID, [In][Out][MarshalAs); }
        // public void GetHeadScanRates(long capabilityID, [In][Out][MarshalAs) { NsInteropGetHeadScanRates(capabilityID, [In][Out][MarshalAs); }
        // public void GetPowerCalibrationBreakOut(short indexCalibration, [In][Out][MarshalAs) { NsInteropGetPowerCalibrationBreakOut(indexCalibration, [In][Out][MarshalAs); }
        public bool GetShowWindow() { return NsInteropGetShowWindow(); }
        public void SetShowWindow(bool showGUI) { NsInteropSetShowWindow(showGUI); }
        public bool GetDataAcquisition() { return NsInteropGetDataAcquisition(); }
        public void SetDataAcquisition(bool acquisitionState) { NsInteropSetDataAcquisition(acquisitionState); }
        public bool GetAutoROI() { return NsInteropGetAutoROI(); }
        public void SetAutoROI(bool autoROIState) { NsInteropSetAutoROI(autoROIState); }
        public bool GetTrackGain() { return NsInteropGetTrackGain(); }
        public void SetTrackGain(bool trackGainState) { NsInteropSetTrackGain(trackGainState); }
        public bool GetTrackFilter() { return NsInteropGetTrackFilter(); }
        public void SetTrackFilter(bool trackFilterState) { NsInteropSetTrackFilter(trackFilterState); }
        public int GetPulsedMode() { return NsInteropGetPulsedMode(); }
        public void SetPulsedMode(int pulsedMode) { NsInteropSetPulsedMode(pulsedMode); }
        public short GetDefaultCalibration() { return NsInteropGetDefaultCalibration(); }
        public void SetDefaultCalibration(short calibrationIndex) { NsInteropSetDefaultCalibration(calibrationIndex); }
        public short GetPowerUnits() { return NsInteropGetPowerUnits(); }
        public void SetPowerUnits(short trackFilterState) { NsInteropSetPowerUnits(trackFilterState); }
        public bool GetMultiROIMode() { return NsInteropGetMultiROIMode(); }
        public void SetMultiROIMode(bool multiROIMode) { NsInteropSetMultiROIMode(multiROIMode); }
        public float GetRailLength() { return NsInteropGetRailLength(); }
        public void SetRailLength(float railLength) { NsInteropSetRailLength(railLength); }
        public short GetGaussFitMethod() { return NsInteropGetGaussFitMethod(); }
        public void SetGaussFitMethod(short gaussFitMethod) { NsInteropSetGaussFitMethod(gaussFitMethod); }
        public float GetMagnificationFactor() { return NsInteropGetMagnificationFactor(); }
        public void SetMagnificationFactor(float magnificationFactor) { NsInteropSetMagnificationFactor(magnificationFactor); }
        public short GetBeamWidthBasis() { return NsInteropGetBeamWidthBasis(); }
        public void SetBeamWidthBasis(short propVal) { NsInteropSetBeamWidthBasis(propVal); }

    }
}
