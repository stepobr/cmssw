import FWCore.ParameterSet.Config as cms

process = cms.Process("HCALSourceDataMonitor")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.load('FWCore.Modules.printContent_cfi')

process.load("Configuration.Geometry.GeometryIdeal_cff")

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2018_realistic', '')
process.es_ascii = cms.ESSource('HcalTextCalibrations',
    input = cms.VPSet(
        cms.PSet(
            object = cms.string('ElectronicsMap'),
            file = cms.FileInPath('HCALSourcing/HCALSourceDataMonitor/Emap_HBHE_K_20180411.txt')
            ),
	)
    )
process.es_prefer = cms.ESPrefer('HcalTextCalibrations','es_ascii')


process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

# input files
process.source = cms.Source("HcalTBSource",
    fileNames = cms.untracked.vstring(
        'root://eoscms//eos/cms/store/group/dpg_hcal/comm_hcal/USC/run328130/USC_328130.root'
    )
)

# TB data unpacker
process.tbunpack = cms.EDProducer("HcalTBObjectUnpacker",
    HcalSlowDataFED = cms.untracked.int32(-1),
    HcalSourcePositionFED = cms.untracked.int32(12),
    HcalTriggerFED = cms.untracked.int32(1),
    fedRawDataCollectionTag = cms.InputTag('source')
)

process.histoUnpack = cms.EDProducer("HcalUTCAhistogramUnpacker",
          fedRawDataCollectionTag = cms.InputTag("source"),
          rawDump = cms.bool(False),
          fedNumbers = cms.vint32(71,64,72,68,69,70,65,66,67))

# Tree-maker
process.hcalSourceDataMon = cms.EDAnalyzer('HCALSourceDataMonitor',
    RootFileName = cms.untracked.string('ntuple_da_328130.root'),
    #PrintRawHistograms = cms.untracked.bool(False),
    SelectDigiBasedOnTubeName = cms.untracked.bool(True),
    HcalSourcePositionDataTag = cms.InputTag("tbunpack"),
    hcalTBTriggerDataTag = cms.InputTag("tbunpack"),
    HcalUHTRhistogramDigiCollectionTag = cms.InputTag("histoUnpack"),
)

process.p = cms.Path(
		     process.tbunpack
                     *process.histoUnpack
#		     *process.printContent
                     *process.hcalSourceDataMon
                    )

