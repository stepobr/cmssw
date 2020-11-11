import FWCore.ParameterSet.Config as cms

from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *

akCs4PFJetAnalyzer = inclusiveJetAnalyzer.clone(
    jetTag = cms.InputTag("slimmedJets"),
    genjetTag = 'slimmedGenJets',
    rParam = 0.4,
    matchJets = cms.untracked.bool(False),
    matchTag = 'patJetsWithBtagging',
    pfCandidateLabel = cms.untracked.InputTag('packedPFCandidates'),
    trackTag = cms.InputTag("generalTracks"),
    fillGenJets = True,
    isMC = True,
    # doSubEvent = True,
    doSubEvent = False,
    useHepMC = cms.untracked.bool(False),
    genParticles = cms.untracked.InputTag("prunedGenParticles"),
    eventInfoTag = cms.InputTag("generator"),
    doLifeTimeTagging = cms.untracked.bool(True),
    doLifeTimeTaggingExtras = cms.untracked.bool(False),
    bTagJetName = cms.untracked.string("akCs4PF"),
    jetName = cms.untracked.string("akCs4PF"),
    genPtMin = cms.untracked.double(5),
    hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
    doTower = cms.untracked.bool(False),
    doSubJets = cms.untracked.bool(False),
    doGenSubJets = cms.untracked.bool(False),
    subjetGenTag = cms.untracked.InputTag("ak4GenJets"),
    doGenTaus = cms.untracked.bool(False),
    genTau1 = cms.InputTag("ak4HiGenNjettiness","tau1"),
    genTau2 = cms.InputTag("ak4HiGenNjettiness","tau2"),
    genTau3 = cms.InputTag("ak4HiGenNjettiness","tau3"),
    doGenSym = cms.untracked.bool(False),
    genSym = cms.InputTag("ak4GenJets","sym"),
    genDroppedBranches = cms.InputTag("ak4GenJets","droppedBranches")
    )

akCs4PFJetSequence_mc = cms.Sequence(
    akCs4PFJetAnalyzer
    )

akCs4PFJetSequence_data = cms.Sequence(
    akCs4PFJetAnalyzer
    )

akCs4PFJetSequence_mb = cms.Sequence(
    akCs4PFJetSequence_mc)
akCs4PFJetSequence_jec = cms.Sequence(
    akCs4PFJetSequence_mc)

akCs4PFJetSequence = cms.Sequence(
    akCs4PFJetSequence_mc)
