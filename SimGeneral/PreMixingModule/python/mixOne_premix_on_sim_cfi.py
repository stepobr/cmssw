# This is the PreMixing config. Not only does it do a RawToDigi
# conversion to the secondary input source, it also holds its own
# instances of an EcalDigiProducer and an HcalDigitizer. It also
# replicates the noise adding functions in the SiStripDigitizer.
#
# Adapted from DataMixingModule


import FWCore.ParameterSet.Config as cms
from SimCalorimetry.HcalSimProducers.hcalUnsuppressedDigis_cfi import hcalSimBlock
from SimGeneral.MixingModule.SiStripSimParameters_cfi import SiStripSimBlock
from SimGeneral.MixingModule.SiPixelSimParameters_cfi import SiPixelSimBlock
from SimTracker.SiPhase2Digitizer.phase2TrackerDigitizer_cfi import phase2TrackerDigitizer, _premixStage1ModifyDict as _phase2TrackerPremixStage1ModifyDict
from SimGeneral.MixingModule.ecalDigitizer_cfi import ecalDigitizer
from SimCalorimetry.HGCalSimProducers.hgcalDigitizer_cfi import hgceeDigitizer, hgchebackDigitizer, hgchefrontDigitizer, hfnoseDigitizer
from SimFastTiming.FastTimingCommon.mtdDigitizer_cfi import mtdDigitizer

hcalSimBlock.HcalPreMixStage2 = cms.bool(True)

mixData = cms.EDProducer("PreMixingModule",
    input = cms.SecSource("EmbeddedRootSource",
        producers = cms.VPSet(),
        nbPileupEvents = cms.PSet(
            averageNumber = cms.double(1.0)
        ),
        seed = cms.int32(1234567),
        type = cms.string('fixed'),
        sequential = cms.untracked.bool(False), # set to true for sequential reading of pileup
        fileNames = cms.untracked.vstring('file:DMPreProcess_RAW2DIGI.root'),
        consecutiveRejectionsLimit = cms.untracked.uint32(100) # should be sufficiently large to allow enough tails
    ),
    # Mixing Module parameters
    bunchspace = cms.int32(25),
    minBunch = cms.int32(0),
    maxBunch = cms.int32(0),
    mixProdStep1 = cms.bool(False),
    mixProdStep2 = cms.bool(False),
    # Optionally adjust the pileup distribution
    adjustPileupDistribution = cms.VPSet(),
    # Workers
    workers = cms.PSet(
        pileup = cms.PSet(
            PileupInfoInputTag = cms.InputTag("addPileupInfo"),
            BunchSpacingInputTag = cms.InputTag("addPileupInfo","bunchSpacing"),
            CFPlaybackInputTag = cms.InputTag("mix"),
            GenPUProtonsInputTags = cms.VInputTag("genPUProtons"),
        ),
        # Note: elements with "@MIXING" in the input tag are generated by
        pixel = cms.PSet(
            SiPixelSimBlock.clone(
                # To preserve the behaviour of copy-pasted version of premix worker
                # All these are done in stage1 (for both signal and pileup)
                AddNoise = False,
                killModules = False,
                MissCalibrate = False,
            ),
            workerType = cms.string("PreMixingSiPixelWorker"),
            pixeldigiCollectionSig = cms.InputTag("simSiPixelDigis"),
            pixeldigiCollectionPile = cms.InputTag("simSiPixelDigis"),
            PixelDigiCollectionDM = cms.string('siPixelDigisDM'),                   
        ),
        strip = cms.PSet(
            SiStripSimBlock,
            workerType = cms.string("PreMixingSiStripWorker"),

            SistripLabelSig = cms.InputTag("simSiStripDigis","ZeroSuppressed"),
            SiStripPileInputTag = cms.InputTag("simSiStripDigis","ZeroSuppressed"),
            # Dead APV Vector
            SistripAPVPileInputTag = cms.InputTag("mix","AffectedAPVList"),
            SistripAPVLabelSig = cms.InputTag("mix","AffectedAPVList"),
            # output
            SiStripDigiCollectionDM = cms.string('siStripDigisDM'),
            SiStripAPVListDM = cms.string('SiStripAPVList'),
        ),
        ecal = cms.PSet(
            ecalDigitizer.clone(accumulatorType = None, makeDigiSimLinks=None),
            workerType = cms.string("PreMixingEcalWorker"),

            EBdigiProducerSig = cms.InputTag("simEcalUnsuppressedDigis"),
            EEdigiProducerSig = cms.InputTag("simEcalUnsuppressedDigis"),
            ESdigiProducerSig = cms.InputTag("simEcalPreshowerDigis"),

            EBPileInputTag = cms.InputTag("simEcalDigis", "ebDigis"),
            EEPileInputTag = cms.InputTag("simEcalDigis", "eeDigis"),
            ESPileInputTag = cms.InputTag("simEcalUnsuppressedDigis"),

            EBDigiCollectionDM   = cms.string(''),
            EEDigiCollectionDM   = cms.string(''),
            ESDigiCollectionDM   = cms.string(''),
        ),
        hcal = cms.PSet(
            hcalSimBlock,
            workerType = cms.string("PreMixingHcalWorker"),

            HBHEdigiCollectionSig  = cms.InputTag("simHcalUnsuppressedDigis"),
            HOdigiCollectionSig    = cms.InputTag("simHcalUnsuppressedDigis"),
            HFdigiCollectionSig    = cms.InputTag("simHcalUnsuppressedDigis"),
            QIE10digiCollectionSig = cms.InputTag("simHcalUnsuppressedDigis"),
            QIE11digiCollectionSig = cms.InputTag("simHcalUnsuppressedDigis"),
            ZDCdigiCollectionSig   = cms.InputTag("simHcalUnsuppressedDigis"),

            HBHEPileInputTag = cms.InputTag("simHcalDigis"),
            HOPileInputTag   = cms.InputTag("simHcalDigis"),
            HFPileInputTag   = cms.InputTag("simHcalDigis"),
            QIE10PileInputTag   = cms.InputTag("simHcalDigis", "HFQIE10DigiCollection"),
            QIE11PileInputTag   = cms.InputTag("simHcalDigis", "HBHEQIE11DigiCollection"),
            ZDCPileInputTag  = cms.InputTag(""),

            HBHEDigiCollectionDM = cms.string(''),
            HODigiCollectionDM   = cms.string(''),
            HFDigiCollectionDM   = cms.string(''),
            QIE10DigiCollectionDM   = cms.string(''),
            QIE11DigiCollectionDM   = cms.string(''),
            ZDCDigiCollectionDM  = cms.string('')
        ),
        dt = cms.PSet(
            workerType = cms.string("PreMixingCrossingFramePSimHitWorker"),
            labelSig = cms.InputTag("mix", "g4SimHitsMuonDTHits"),
            pileInputTag = cms.InputTag("mix", "g4SimHitsMuonDTHits"),
            collectionDM = cms.string("g4SimHitsMuonDTHits"),
        ),
        rpc = cms.PSet(
            workerType = cms.string("PreMixingCrossingFramePSimHitWorker"),
            labelSig = cms.InputTag("mix", "g4SimHitsMuonRPCHits"),
            pileInputTag = cms.InputTag("mix", "g4SimHitsMuonRPCHits"),
            collectionDM = cms.string("g4SimHitsMuonRPCHits"),
        ),
        csc = cms.PSet(
            workerType = cms.string("PreMixingCrossingFramePSimHitWorker"),
            labelSig = cms.InputTag("mix", "g4SimHitsMuonCSCHits"),
            pileInputTag = cms.InputTag("mix", "g4SimHitsMuonCSCHits"),
            collectionDM = cms.string("g4SimHitsMuonCSCHits"),
        ),
        trackingTruth = cms.PSet(
            workerType = cms.string("PreMixingTrackingParticleWorker"),
            labelSig = cms.InputTag("mix","MergedTrackTruth"),
            pileInputTag = cms.InputTag("mix","MergedTrackTruth"),
            collectionDM = cms.string('MergedTrackTruth'),
        ),
        pixelSimLink = cms.PSet(
            workerType = cms.string("PreMixingPixelDigiSimLinkWorker"),
            labelSig = cms.InputTag("simSiPixelDigis"),
            pileInputTag = cms.InputTag("simSiPixelDigis"),
            collectionDM = cms.string('PixelDigiSimLink'),
        ),
        stripSimLink = cms.PSet(
            workerType = cms.string("PreMixingStripDigiSimLinkWorker"),
            labelSig = cms.InputTag("simSiStripDigis"),
            pileInputTag = cms.InputTag("simSiStripDigis"),
            collectionDM = cms.string('StripDigiSimLink'),
        ),
    ),
)


from Configuration.Eras.Modifier_fastSim_cff import fastSim
from FastSimulation.Tracking.recoTrackAccumulator_cfi import recoTrackAccumulator as _recoTrackAccumulator
fastSim.toModify(mixData,
    # from signal: mix tracks not strip or pixel digis
    workers = dict(
        pixel = None,
        strip = None,
        pixelSimLink = None,
        stripSimLink = None,
        tracks = cms.PSet(
            workerType = cms.string("PreMixingDigiAccumulatorWorker"),
            accumulator = _recoTrackAccumulator.clone(
                pileUpTracks = "mix:generalTracks"
            )
        ),
        dt = dict(
            labelSig = "mix:MuonSimHitsMuonDTHits",
            pileInputTag = "mix:MuonSimHitsMuonDTHits",
            collectionDM = "MuonSimHitsMuonDTHits",
        ),
        rpc = dict(
            labelSig = "mix:MuonSimHitsMuonRPCHits",
            pileInputTag = "mix:MuonSimHitsMuonRPCHits",
            collectionDM = "MuonSimHitsMuonRPCHits",
        ),
        csc = dict(
            labelSig = "mix:MuonSimHitsMuonCSCHits",
            pileInputTag = "mix:MuonSimHitsMuonCSCHits",
            collectionDM = "MuonSimHitsMuonCSCHits",
        ),
    ),
)

from Configuration.Eras.Modifier_run2_GEM_2017_cff import run2_GEM_2017
from Configuration.Eras.Modifier_run3_GEM_cff import run3_GEM
(run2_GEM_2017 | run3_GEM).toModify(
    mixData,
    workers = dict(
        gem = cms.PSet(
            workerType = cms.string("PreMixingCrossingFramePSimHitWorker"),
            labelSig = cms.InputTag("mix", "g4SimHitsMuonGEMHits"),
            pileInputTag = cms.InputTag("mix", "g4SimHitsMuonGEMHits"),
            collectionDM = cms.string("g4SimHitsMuonGEMHits"),
        ),
    )
)

from Configuration.Eras.Modifier_phase2_common_cff import phase2_common
from Configuration.Eras.Modifier_phase2_tracker_cff import phase2_tracker
from Configuration.Eras.Modifier_phase2_timing_layer_cff import phase2_timing_layer
from Configuration.Eras.Modifier_phase2_hcal_cff import phase2_hcal
from Configuration.Eras.Modifier_phase2_hgcal_cff import phase2_hgcal
from Configuration.Eras.Modifier_phase2_hfnose_cff import phase2_hfnose
from Configuration.Eras.Modifier_phase2_muon_cff import phase2_muon
phase2_common.toModify(mixData, input = dict(producers = [])) # we use digis directly, no need for raw2digi producers

# Tracker
phase2_tracker.toModify(mixData,
    workers = dict(
        # Disable SiStrip
        strip = None,
        stripSimLink = None,
        # Replace pixel with Phase2 tracker
        pixel = cms.PSet(
            phase2TrackerDigitizer,
            workerType = cms.string("PreMixingPhase2TrackerWorker"),

            pixelLabelSig = cms.InputTag("simSiPixelDigis:Pixel"),
            pixelPileInputTag = cms.InputTag("simSiPixelDigis:Pixel"),
            trackerLabelSig = cms.InputTag("simSiPixelDigis:Tracker"),
            trackerPileInputTag = cms.InputTag("simSiPixelDigis:Tracker"),
            pixelPmxStage1ElectronPerAdc = cms.double(phase2TrackerDigitizer.PixelDigitizerAlgorithm.ElectronPerAdc.value()),
            trackerPmxStage1ElectronPerAdc = cms.double(phase2TrackerDigitizer.PSPDigitizerAlgorithm.ElectronPerAdc.value())
        ),
        pixelSimLink = dict(
            labelSig = "simSiPixelDigis:Pixel",
            pileInputTag = "simSiPixelDigis:Pixel",
        ),
        phase2OTSimLink = cms.PSet(
            workerType = cms.string("PreMixingPixelDigiSimLinkWorker"),
            labelSig = cms.InputTag("simSiPixelDigis:Tracker"),
            pileInputTag = cms.InputTag("simSiPixelDigis:Tracker"),
            collectionDM = cms.string("Phase2OTDigiSimLink"),
        ),
    ),
)

# MTD
phase2_timing_layer.toModify(mixData,
    workers = dict(
        mtdBarrel = cms.PSet(
            mtdDigitizer.barrelDigitizer,
            workerType = cms.string("PreMixingMTDWorker"),
            digiTagSig = cms.InputTag("mix", "FTLBarrel"),
            pileInputTag = cms.InputTag("mix", "FTLBarrel"),
        ),
        mtdEndcap = cms.PSet(
            mtdDigitizer.endcapDigitizer,
            workerType = cms.string("PreMixingMTDWorker"),
            digiTagSig = cms.InputTag("mix", "FTLEndcap"),
            pileInputTag = cms.InputTag("mix", "FTLEndcap"),
        ),
    )
)
# ECAL
phase2_common.toModify (mixData, workers=dict(ecal=dict(doES=False)))
phase2_hgcal.toModify(mixData, workers=dict(ecal=dict(doEE=False)))

# HGCAL
phase2_hgcal.toModify(mixData,
    workers = dict(
        hgcee = cms.PSet(
            hgceeDigitizer,
            workerType = cms.string("PreMixingHGCalWorker"),
            digiTagSig = cms.InputTag("mix", "HGCDigisEE"),
            pileInputTag = cms.InputTag("simHGCalUnsuppressedDigis", "EE"),
        ),
        hgchefront = cms.PSet(
            hgchefrontDigitizer,
            workerType = cms.string("PreMixingHGCalWorker"),
            digiTagSig = cms.InputTag("mix", "HGCDigisHEfront"),
            pileInputTag = cms.InputTag("simHGCalUnsuppressedDigis", "HEfront"),
        ),
        hgcheback = cms.PSet(
            hgchebackDigitizer,
            workerType = cms.string("PreMixingHGCalWorker"),
            digiTagSig = cms.InputTag("mix", "HGCDigisHEback"),
            pileInputTag = cms.InputTag("simHGCalUnsuppressedDigis", "HEback"),
        ),
        caloTruth = cms.PSet(
            workerType = cms.string("PreMixingCaloParticleWorker"),
            labelSig = cms.InputTag("mix", "MergedCaloTruth"),
            pileInputTag = cms.InputTag("mix", "MergedCaloTruth"),
            collectionDM = cms.string("MergedCaloTruth"),
        )
    )
)

phase2_hfnose.toModify(mixData,
    workers = dict(
        hfnose = cms.PSet(
            hfnoseDigitizer,
            workerType = cms.string("PreMixingHGCalWorker"),
            digiTagSig = cms.InputTag("mix", "HFNoseDigis"),
            pileInputTag = cms.InputTag("simHGCalUnsuppressedDigis", "HFNose"),
        ),
    )
)


# Muon
phase2_muon.toModify(mixData,
    workers = dict(
        me0 = cms.PSet(
            workerType = cms.string("PreMixingCrossingFramePSimHitWorker"),
            labelSig = cms.InputTag("mix", "g4SimHitsMuonME0Hits"),
            pileInputTag = cms.InputTag("mix", "g4SimHitsMuonME0Hits"),
            collectionDM = cms.string("g4SimHitsMuonME0Hits"),
        ),
    )
)
