import FWCore.ParameterSet.Config as cms

from HeavyIonsAnalysis.JetAnalysis.akCs4PFJetSequence_pponPbPb_data_cff import *

import RecoHI.HiJetAlgos.particleTowerProducer_cfi as _mod
PFTowers = _mod.particleTowerProducer.clone(useHF = True,
											src = cms.InputTag('packedPFCandidates'))

jetSequence = cms.Sequence(
	PFTowers +
    akCs4PFJetSequence
)
