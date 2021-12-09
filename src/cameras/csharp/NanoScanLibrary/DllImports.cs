/* Below is a complete list of all the methods and properties that are available in the NanoScan v2 automation.
 * 
 * There are a few methods that have been left commented, indicating they are unsupported in .NET applications.
 * Alternate methods are provided.
 * 
 * All NanoScan v2 COM properties are translated into Get and Set methods by .NET/COM marshalling convention.
 * 
 * For more information, see the ActiveX documentation located in the NanoScan installation directory.
 * i.e. C:\Program Files (x86)\Photon\NanoScan v2.0\Documentation\50260-001 NanoScan v2 Op Manual.pdf
 */

using System;
using System.Runtime.InteropServices;

namespace NanoScanLibrary
{
    partial class NanoScan
    {
        #region Imported Methods

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int InitNsInterop();

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern void ShutdownNsInterop();

        /* UNSUPPORTED use NsInteropGetHeadCapabilitiesGains or NsInteropGetHeadCapabilitiesScanRates
         * [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "NsInteropGetHeadCapabilities")]
         * static extern int NsInteropGetHeadCapabilities(long capabilityID,  [In][Out][MarshalAs(UnmanagedType.Struct)] ref object headCapability);
         */

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropSetGain(short aperture, short gain);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetGain(short aperture, ref short gain);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropSetFilter(short aperture, float filter);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetFilter(short aperture, ref float filter);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropSetSamplingResolution(float samplingResolution);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetSamplingResolution(short aperture, ref float samplingResolution);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropSetRotationFrequency(float rotationFrequency);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetRotationFrequency(ref float rotationFrequency);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetMeasuredRotationFreq(ref float measuredRotationFreq);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropAutoFind();

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropAddROI(short aperture, float leftBound, float rightBound, bool roiEnabled);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropDeleteROI(short aperture, short roiIndex);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropUpdateROI(short aperture, short roiIndex, float leftBound, float rightBound, bool roiEnabled);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetNumberOfROIs(short aperture, ref short numberOfROIs);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetROI(short aperture, short sROIIndex, ref float leftBound, ref float rightBound, ref bool roiEnabled);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetApertureLimits(short aperture, ref float startPosition, ref float EndPosition);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "NsInteropReadProfile")]
        private static extern int NsInteropReadProfile(
            short sAperture,
            float fStartPosition,
            float fEndPosition,
            short sDecimationFactor,
            [In][Out][MarshalAs(UnmanagedType.Struct)] ref object ProfileAmplitude,
            [In][Out][MarshalAs(UnmanagedType.Struct)] ref object ProfilePosition);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropSelectParameters(ulong parameters);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetSelectedParameters(ref ulong parameters);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropSetUserClipLevel1(float userClipLevel1);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropSetUserClipLevel2(float userClipLevel2);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetUserClipLevel1(ref float userClipLevel1);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetUserClipLevel2(ref float userClipLevel2);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetBeamWidth(short aperture, short roiIndex, float clipLevel, ref float beamWidth);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetBeamWidth4Sigma(short aperture, short roiIndex, ref float beamWidth4Sigma);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetCentroidPosition(short aperture, short roiIndex, ref float centroidPosition);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetPeakPosition(short aperture, short roiIndex, ref float peakPosition);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetCentroidSeparation(short aperture, short roiIndex, ref float centroidSeparation);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetPeakSeparation(short aperture, short roiIndex, ref float peakSeparation);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetBeamIrradiance(short aperture, short roiIndex, ref float beamIrradiance);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetGaussianFit(short aperture, short roiIndex, ref float goodnessFit, ref float roughnessFit);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetBeamEllipticity(short roiIndex, ref float beamEllipticity);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropSetPulseFrequency(float pulseFrequency);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetPulseFrequency(ref float pulseFrequency);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropAcquireSync1Rev();
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetNumPwrCalibrations(ref short numPwrCalibrations);

        /*UNSUPPORTED use NsInteropGetPowerCalibrationValues
         * [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
         * static extern int NsInteropGetPowerCalibration(short indexCalibration, [In][Out][MarshalAs(UnmanagedType.Struct)] ref VariantStructGeneric pwrCalibration);
         */
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetTotalPower(ref float totalPower);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetPower(short roiIndex, ref float roiPower);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetDeviceID(ref short deviceID);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropSetDeviceID(short deviceID);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetNumDevices(ref short numDevices);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropOpenMotionPort(string motionPort);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropCloseMotionPort();
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGo2Position(float position);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropIsSignalSaturated(short aperture, ref bool isSignalSaturated);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropRecompute();
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetBeamWidthRatio(short roiIndex, float clipLevel, ref float beamWidthRatio);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetBeamWidth4SigmaRatio(short roiIndex, ref float beamWidth4SigmaRatio);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetMaxSamplingResolution(ref float maxSamplingRes);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropSetDivergenceMethod(short divMethod, float clipLevel, float distance);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetDivergenceMethod(ref short divMethod, ref float clipLevel, ref float distance);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetDivergenceParameter(short aperture, short roiIndex, ref float divergence);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetDeviceList([In][Out][MarshalAs(UnmanagedType.Struct)] ref object deviceList);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetAveraging(ref short finite, ref short rolling);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropSetAveraging(short finite, short rolling);
        
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropRunComputation();

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern void NsInteropGetHeadGainTable(long capabilityID, [In][Out][MarshalAs(UnmanagedType.Struct)] ref object gainTableArray);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern void NsInteropGetHeadScanRates(long capabilityID, [In][Out][MarshalAs(UnmanagedType.Struct)] ref object scanRateArray);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern void NsInteropGetPowerCalibrationBreakOut(short indexCalibration, [In][Out][MarshalAs(UnmanagedType.BStr)] ref string descriptor, ref float refPower, ref float waveLength);
        #endregion

        #region Imported Properties
        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern bool NsInteropGetShowWindow();

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern void NsInteropSetShowWindow(bool showGUI);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern bool NsInteropGetDataAcquisition();

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern void NsInteropSetDataAcquisition(bool acquisitionState);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern bool NsInteropGetAutoROI();

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern void NsInteropSetAutoROI(bool autoROIState);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern bool NsInteropGetTrackGain();

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern void NsInteropSetTrackGain(bool trackGainState);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern bool NsInteropGetTrackFilter();

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern void NsInteropSetTrackFilter(bool trackFilterState);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern int NsInteropGetPulsedMode();

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern void NsInteropSetPulsedMode(int pulsedMode);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern short NsInteropGetDefaultCalibration();

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern void NsInteropSetDefaultCalibration(short calibrationIndex);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern short NsInteropGetPowerUnits();

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern void NsInteropSetPowerUnits(short trackFilterState);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern bool NsInteropGetMultiROIMode();

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern void NsInteropSetMultiROIMode(bool multiROIMode);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern float NsInteropGetRailLength();

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern void NsInteropSetRailLength(float railLength);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern short NsInteropGetGaussFitMethod();

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern void NsInteropSetGaussFitMethod(short gaussFitMethod);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern float NsInteropGetMagnificationFactor();

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern void NsInteropSetMagnificationFactor(float magnificationFactor);

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern short NsInteropGetBeamWidthBasis();

        [DllImport(@"NS2_Interop.dll", CallingConvention = CallingConvention.Cdecl)]
        static extern void NsInteropSetBeamWidthBasis(short propVal);
         
        #endregion
    }
}
