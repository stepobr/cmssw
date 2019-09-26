import FWCore.ParameterSet.Config as cms
process = cms.Process("HcalParametersTest")

process.load('Geometry.HcalCommonData.testPhase2GeometryFineXML_cfi')
process.load('Geometry.HcalCommonData.hcalParameters_cfi')
process.load('Geometry.HcalCommonData.hcalSimulationParameters_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')

process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
    )

if hasattr(process,'MessageLogger'):
    process.MessageLogger.categories.append('HGCalGeom')

process.hpa = cms.EDAnalyzer("HcalParametersAnalyzer")

process.Timing = cms.Service("Timing")
process.SimpleMemoryCheck = cms.Service("SimpleMemoryCheck")

process.p1 = cms.Path(process.hpa)
