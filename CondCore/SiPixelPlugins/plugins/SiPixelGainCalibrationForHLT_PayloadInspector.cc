/*!
  \file SiPixelGainCalibrationOffline_PayloadInspector
  \Payload Inspector Plugin for SiPixel Gain Calibration for HLT
  \author M. Musich
  \version $Revision: 1.0 $
  \date $Date: 2020/04/01 11:31:00 $
*/

#include "CondCore/SiPixelPlugins/interface/SiPixelGainCalibHelper.h"

namespace {

  using SiPixelGainCalibrationForHLTGainsValues =
      gainCalibHelper::SiPixelGainCalibrationValues<gainCalibHelper::gainCalibPI::t_gain, SiPixelGainCalibrationForHLT>;
  using SiPixelGainCalibrationForHLTPedestalsValues =
      gainCalibHelper::SiPixelGainCalibrationValues<gainCalibHelper::gainCalibPI::t_pedestal,
                                                    SiPixelGainCalibrationForHLT>;

  using SiPixelGainCalibrationForHLTCorrelations =
      gainCalibHelper::SiPixelGainCalibrationCorrelations<SiPixelGainCalibrationForHLT>;

  using SiPixelGainCalibrationForHLTGainsByPart =
      gainCalibHelper::SiPixelGainCalibrationValuesByPart<gainCalibHelper::gainCalibPI::t_gain,
                                                          SiPixelGainCalibrationForHLT>;
  using SiPixelGainCalibrationForHLTPedestalsByPart =
      gainCalibHelper::SiPixelGainCalibrationValuesByPart<gainCalibHelper::gainCalibPI::t_pedestal,
                                                          SiPixelGainCalibrationForHLT>;

  using SiPixelGainCalibForHLTGainComparisonSingleTag =
      gainCalibHelper::SiPixelGainCalibrationValueComparisonSingleTag<gainCalibHelper::gainCalibPI::t_gain,
                                                                      SiPixelGainCalibrationForHLT>;
  using SiPixelGainCalibForHLTPedestalComparisonSingleTag =
      gainCalibHelper::SiPixelGainCalibrationValueComparisonSingleTag<gainCalibHelper::gainCalibPI::t_pedestal,
                                                                      SiPixelGainCalibrationForHLT>;

  using SiPixelGainCalibForHLTGainComparisonTwoTags =
      gainCalibHelper::SiPixelGainCalibrationValueComparisonTwoTags<gainCalibHelper::gainCalibPI::t_gain,
                                                                    SiPixelGainCalibrationForHLT>;
  using SiPixelGainCalibForHLTPedestalComparisonTwoTags =
      gainCalibHelper::SiPixelGainCalibrationValueComparisonTwoTags<gainCalibHelper::gainCalibPI::t_pedestal,
                                                                    SiPixelGainCalibrationForHLT>;

  using SiPixelGainCalibForHLTGainsBPIXMap =
      gainCalibHelper::SiPixelGainCalibrationBPIXMap<gainCalibHelper::gainCalibPI::t_gain, SiPixelGainCalibrationForHLT>;
  using SiPixelGainCalibForHLTPedestalsBPIXMap =
      gainCalibHelper::SiPixelGainCalibrationBPIXMap<gainCalibHelper::gainCalibPI::t_pedestal,
                                                     SiPixelGainCalibrationForHLT>;

  using SiPixelGainCalibForHLTGainsFPIXMap =
      gainCalibHelper::SiPixelGainCalibrationFPIXMap<gainCalibHelper::gainCalibPI::t_gain, SiPixelGainCalibrationForHLT>;
  using SiPixelGainCalibForHLTPedestalsFPIXMap =
      gainCalibHelper::SiPixelGainCalibrationFPIXMap<gainCalibHelper::gainCalibPI::t_pedestal,
                                                     SiPixelGainCalibrationForHLT>;

  using SiPixelGainCalibForHLTGainByRegionComparisonSingleTag =
      gainCalibHelper::SiPixelGainCalibrationByRegionComparisonSingleTag<gainCalibHelper::gainCalibPI::t_gain,
                                                                         SiPixelGainCalibrationForHLT>;
  using SiPixelGainCalibForHLTPedestalByRegionComparisonSingleTag =
      gainCalibHelper::SiPixelGainCalibrationByRegionComparisonSingleTag<gainCalibHelper::gainCalibPI::t_pedestal,
                                                                         SiPixelGainCalibrationForHLT>;

  using SiPixelGainCalibForHLTGainByRegionComparisonTwoTags =
      gainCalibHelper::SiPixelGainCalibrationByRegionComparisonTwoTags<gainCalibHelper::gainCalibPI::t_gain,
                                                                       SiPixelGainCalibrationForHLT>;
  using SiPixelGainCalibForHLTPedestalByRegionComparisonTwoTags =
      gainCalibHelper::SiPixelGainCalibrationByRegionComparisonTwoTags<gainCalibHelper::gainCalibPI::t_pedestal,
                                                                       SiPixelGainCalibrationForHLT>;

}  // namespace

PAYLOAD_INSPECTOR_MODULE(SiPixelGainCalibrationForHLT) {
  PAYLOAD_INSPECTOR_CLASS(SiPixelGainCalibrationForHLTGainsValues);
  PAYLOAD_INSPECTOR_CLASS(SiPixelGainCalibrationForHLTPedestalsValues);
  PAYLOAD_INSPECTOR_CLASS(SiPixelGainCalibrationForHLTCorrelations);
  PAYLOAD_INSPECTOR_CLASS(SiPixelGainCalibrationForHLTGainsByPart);
  PAYLOAD_INSPECTOR_CLASS(SiPixelGainCalibrationForHLTPedestalsByPart);
  PAYLOAD_INSPECTOR_CLASS(SiPixelGainCalibForHLTGainComparisonSingleTag)
  PAYLOAD_INSPECTOR_CLASS(SiPixelGainCalibForHLTPedestalComparisonSingleTag);
  PAYLOAD_INSPECTOR_CLASS(SiPixelGainCalibForHLTGainComparisonTwoTags);
  PAYLOAD_INSPECTOR_CLASS(SiPixelGainCalibForHLTPedestalComparisonTwoTags);
  PAYLOAD_INSPECTOR_CLASS(SiPixelGainCalibForHLTGainsBPIXMap);
  PAYLOAD_INSPECTOR_CLASS(SiPixelGainCalibForHLTPedestalsBPIXMap);
  PAYLOAD_INSPECTOR_CLASS(SiPixelGainCalibForHLTGainsFPIXMap);
  PAYLOAD_INSPECTOR_CLASS(SiPixelGainCalibForHLTPedestalsFPIXMap);
  PAYLOAD_INSPECTOR_CLASS(SiPixelGainCalibForHLTGainByRegionComparisonSingleTag);
  PAYLOAD_INSPECTOR_CLASS(SiPixelGainCalibForHLTPedestalByRegionComparisonSingleTag);
  PAYLOAD_INSPECTOR_CLASS(SiPixelGainCalibForHLTGainByRegionComparisonTwoTags);
  PAYLOAD_INSPECTOR_CLASS(SiPixelGainCalibForHLTPedestalByRegionComparisonTwoTags);
}
