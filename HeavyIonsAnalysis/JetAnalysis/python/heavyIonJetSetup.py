from __future__ import division

from RecoBTag.Configuration.RecoBTag_cff import *
from RecoBTag.SecondaryVertex.negativeCombinedSecondaryVertexV2BJetTags_cfi import *
from RecoBTag.SecondaryVertex.negativeCombinedSecondaryVertexV2Computer_cfi import *
from RecoBTag.SecondaryVertex.negativeSimpleSecondaryVertexHighEffBJetTags_cfi import *
from RecoBTag.SecondaryVertex.negativeSimpleSecondaryVertexHighPurBJetTags_cfi import *
from RecoBTag.SecondaryVertex.positiveCombinedSecondaryVertexV2BJetTags_cfi import *
from RecoBTag.SecondaryVertex.positiveCombinedSecondaryVertexV2Computer_cfi import *
from RecoBTag.SecondaryVertex.secondaryVertexNegativeTagInfos_cfi import *

from RecoHI.HiJetAlgos.HiRecoPFJets_cff import akPu3PFJets
from RecoHI.HiJetAlgos.HiGenJets_cff import ak5HiGenJets
from RecoHI.HiJetAlgos.HiGenCleaner_cff import heavyIonCleanedGenJets
#from RecoHI.HiJetAlgos.HiSignalGenJetProducer_cfi import hiSignalGenJets

from RecoJets.JetAssociationProducers.ak5JTA_cff import *

from PhysicsTools.PatAlgos.mcMatchLayer0.jetFlavourId_cff import *
from PhysicsTools.PatAlgos.mcMatchLayer0.jetMatch_cfi import *
from PhysicsTools.PatAlgos.producersHeavyIons.heavyIonJets_cff import *
from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cfi import *
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
from PhysicsTools.PatAlgos.tools.helpers import *

from RecoHI.HiJetAlgos.HiRecoPFJets_cff import akPu4PFJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *

def get_radius(tag):
    return int(filter(str.isdigit, tag))

def addToSequence(label, module, process, sequence):
    setattr(process, label, module)
    sequence += getattr(process, label)

def setupHeavyIonJetsWithBTagging(tag, sequence, process, signal):
    radius = get_radius(tag)

    addToSequence(
        tag + 'Jets',
        akPu4PFJets.clone(rParam = radius / 10),
        process,
        sequence)

    genjets = "HiSignalGenJets" if signal else "HiCleanedGenJets"
    genpartons = "signalPartons" if signal else "allPartons"
    signalpartons = "hiSignalGenParticles" if signal else "cleanedPartons"

    genjetcollection = 'ak' + str(radius) + 'HiGenJets'

    addToSequence(
        genjetcollection,
        ak5HiGenJets.clone(rParam = radius / 10),
        process,
        sequence)

    # addToProcessAndTask(
    #     'ak' + str(radius) + 'HiSignalGenJets',
    #     hiSignalGenJets.clone(src = genjetcollection),
    #     process,
    #     task)

    addToSequence(
        'ak' + str(radius) + 'HiCleanedGenJets',
        heavyIonCleanedGenJets.clone(src = genjetcollection),
        process,
        sequence)

    addToSequence(
        'JetTracksAssociatorAtVertex' + tag,
        ak5JetTracksAssociatorAtVertex.clone(
            jets = tag + "Jets",
            tracks = "highPurityTracks",
            ),
        process,
        sequence)

    addToSequence(
        'ImpactParameterTagInfos' + tag,
        impactParameterTagInfos.clone(
            jetTracks = "JetTracksAssociatorAtVertex" + tag,
            ),
        process,
        sequence)

    addToSequence(
        'TrackCountingHighEffBJetTags' + tag,
        trackCountingHighEffBJetTags.clone(
            tagInfos = ["ImpactParameterTagInfos" + tag],
            ),
        process,
        sequence)

    addToSequence(
        'TrackCountingHighPurBJetTags' + tag,
        trackCountingHighPurBJetTags.clone(
            tagInfos = ["ImpactParameterTagInfos" + tag],
            ),
        process,
        sequence)

    addToSequence(
        'JetProbabilityBJetTags' + tag,
        jetProbabilityBJetTags.clone(
            tagInfos = ["ImpactParameterTagInfos" + tag],
            ),
        process,
        sequence)

    addToSequence(
        'JetBProbabilityBJetTags' + tag,
        jetBProbabilityBJetTags.clone(
            tagInfos = ["ImpactParameterTagInfos" + tag],
            ),
        process,
        sequence)

    addToSequence(
        'SecondaryVertexTagInfos' + tag,
        secondaryVertexTagInfos.clone(
            trackIPTagInfos = "ImpactParameterTagInfos" + tag,
            ),
        process,
        sequence)

    addToSequence(
        'CombinedSecondaryVertexBJetTags' + tag,
        combinedSecondaryVertexV2BJetTags.clone(
            tagInfos = [
                "ImpactParameterTagInfos" + tag,
                "SecondaryVertexTagInfos" + tag,
                ],
            ),
        process,
        sequence)

    addToSequence(
        'CombinedSecondaryVertexV2BJetTags' + tag,
        combinedSecondaryVertexV2BJetTags.clone(
            tagInfos = [
                "ImpactParameterTagInfos" + tag,
                "SecondaryVertexTagInfos" + tag,
                ],
            ),
        process,
        sequence)

    addToSequence(
        'SecondaryVertexTagInfos' + tag,
        secondaryVertexTagInfos.clone(
            trackIPTagInfos = "ImpactParameterTagInfos" + tag,
            ),
        process,
        sequence)

    addToSequence(
        'SimpleSecondaryVertexHighEffBJetTags' + tag,
        simpleSecondaryVertexHighEffBJetTags.clone(
            tagInfos = ["SecondaryVertexTagInfos" + tag],
            ),
        process,
        sequence)

    addToSequence(
        'SimpleSecondaryVertexHighPurBJetTags' + tag,
        simpleSecondaryVertexHighPurBJetTags.clone(
            tagInfos = ["SecondaryVertexTagInfos" + tag],
            ),
        process,
        sequence)

    addToSequence(
        'CombinedSecondaryVertexBJetTags' + tag,
        combinedSecondaryVertexV2BJetTags.clone(
            tagInfos = [
                "ImpactParameterTagInfos" + tag,
                "SecondaryVertexTagInfos" + tag,
                ],
            ),
        process,
        sequence)

    addToSequence(
        'CombinedSecondaryVertexV2BJetTags' + tag,
        combinedSecondaryVertexV2BJetTags.clone(
            tagInfos = [
                "ImpactParameterTagInfos" + tag,
                "SecondaryVertexTagInfos" + tag,
                ],
            ),
        process,
        sequence)

    addToSequence(
        'SecondaryVertexNegativeTagInfos' + tag,
        secondaryVertexNegativeTagInfos.clone(
            trackIPTagInfos = "ImpactParameterTagInfos" + tag,
            ),
        process,
        sequence)

    addToSequence(
        'NegativeSimpleSecondaryVertexHighEffBJetTags' + tag,
        negativeSimpleSecondaryVertexHighEffBJetTags.clone(
            tagInfos = ["SecondaryVertexNegativeTagInfos" + tag],
            ),
        process,
        sequence)

    addToSequence(
        'NegativeSimpleSecondaryVertexHighPurBJetTags' + tag,
        negativeSimpleSecondaryVertexHighPurBJetTags.clone(
            tagInfos = ["SecondaryVertexNegativeTagInfos" + tag],
            ),
        process,
        sequence)

    addToSequence(
        'NegativeCombinedSecondaryVertexBJetTags' + tag,
        negativeCombinedSecondaryVertexV2BJetTags.clone(
            tagInfos = [
                "ImpactParameterTagInfos" + tag,
                "SecondaryVertexNegativeTagInfos" + tag,
                ],
            ),
        process,
        sequence)

    addToSequence(
        'PositiveCombinedSecondaryVertexBJetTags' + tag,
        positiveCombinedSecondaryVertexV2BJetTags.clone(
            tagInfos = [
                "ImpactParameterTagInfos" + tag,
                "SecondaryVertexTagInfos" + tag,
                ],
            ),
        process,
        sequence)

    addToSequence(
        'NegativeCombinedSecondaryVertexV2BJetTags' + tag,
        negativeCombinedSecondaryVertexV2BJetTags.clone(
            tagInfos = [
                "ImpactParameterTagInfos" + tag,
                "SecondaryVertexNegativeTagInfos" + tag,
                ],
            ),
        process,
        sequence)

    addToSequence(
        'PositiveCombinedSecondaryVertexV2BJetTags' + tag,
        positiveCombinedSecondaryVertexV2BJetTags.clone(
            tagInfos = [
                "ImpactParameterTagInfos" + tag,
                "SecondaryVertexTagInfos" + tag,
                ],
            ),
        process,
        sequence)

    addToSequence(
        'SoftPFMuonsTagInfos' + tag,
        softPFMuonsTagInfos.clone(
            jets = tag + "Jets",
            ),
        process,
        sequence)

    addToSequence(
        'SoftPFMuonBJetTags' + tag,
        softPFMuonBJetTags.clone(
            tagInfos = ["SoftPFMuonsTagInfos" + tag],
            ),
        process,
        sequence)

    addToSequence(
        'SoftPFMuonByIP3dBJetTags' + tag,
        softPFMuonByIP3dBJetTags.clone(
            tagInfos = ["SoftPFMuonsTagInfos" + tag],
            ),
        process,
        sequence)

    addToSequence(
        'SoftPFMuonByPtBJetTags' + tag,
        softPFMuonByPtBJetTags.clone(
            tagInfos = ["SoftPFMuonsTagInfos" + tag],
            ),
        process,
        sequence)

    addToSequence(
        'PositiveSoftPFMuonByPtBJetTags' + tag,
        positiveSoftPFMuonByPtBJetTags.clone(
            tagInfos = ["SoftPFMuonsTagInfos" + tag],
            ),
        process,
        sequence)

    addToSequence(
        'NegativeSoftPFMuonByPtBJetTags' + tag,
        negativeSoftPFMuonByPtBJetTags.clone(
            tagInfos = ["SoftPFMuonsTagInfos" + tag],
            ),
        process,
        sequence)

    addToSequence(
        'patJetCorrFactors' + tag,
        patJetCorrFactors.clone(
            useNPV = False,
            useRho = False,
            levels = ['L2Relative'],
            payload = "AK" + str(radius) + "PF",
            src = tag + "Jets",
            ),
        process,
        sequence)

    addToSequence(
        'patJetGenJetMatch' + tag,
        patJetGenJetMatch.clone(
            matched = 'ak' + str(radius) + genjets,
            maxDeltaR = radius / 10,
            resolveByMatchQuality = True,
            src = tag + "Jets",
            ),
        process,
        sequence)

    addToSequence(
        'patJetPartonMatch' + tag,
        patJetPartonMatch.clone(
            matched = signalpartons,
            src = tag + "Jets",
            ),
        process,
        sequence)

    addToSequence(
        'patJetPartons' + tag,
        patJetPartons.clone(
            particles = "hiSignalGenParticles",
            ),
        process,
        sequence)

    addToSequence(
        'patJetFlavourAssociation' + tag,
        patJetFlavourAssociation.clone(
            jets = tag + "Jets",
            rParam = radius / 10,
            bHadrons = "patJetPartons" + tag + ":bHadrons",
            cHadrons = "patJetPartons" + tag + ":cHadrons",
            leptons = "patJetPartons" + tag + ":leptons",
            partons = "patJetPartons" + tag + ":physicsPartons",
            ),
        process,
        sequence)

    addToSequence(
        'patJetPartonAssociationLegacy' + tag,
        patJetPartonAssociationLegacy.clone(
            jets = tag + "Jets",
            partons = genpartons,
            ),
        process,
        sequence)

    addToSequence(
        'patJetFlavourAssociationLegacy' + tag,
        patJetFlavourAssociationLegacy.clone(
            srcByReference = "patJetPartonAssociationLegacy" + tag,
            ),
        process,
        sequence)

    addToSequence(
        'patJets' + tag,
        patJets.clone(
            jetSource = tag + "Jets",
            genJetMatch = "patJetGenJetMatch" + tag,
            genPartonMatch = "patJetPartonMatch" + tag,
            JetFlavourInfoSource = "patJetFlavourAssociation" + tag,
            JetPartonMapSource = "patJetFlavourAssociationLegacy" + tag,
            jetCorrFactorsSource = ["patJetCorrFactors" + tag],
            trackAssociationSource = "JetTracksAssociatorAtVertex" + tag,
            useLegacyJetMCFlavour = True,
            discriminatorSources = [
                "SimpleSecondaryVertexHighEffBJetTags" + tag,
                "SimpleSecondaryVertexHighPurBJetTags" + tag,
                "CombinedSecondaryVertexBJetTags" + tag,
                "CombinedSecondaryVertexV2BJetTags" + tag,
                "JetBProbabilityBJetTags" + tag,
                "JetProbabilityBJetTags" + tag,
                "TrackCountingHighEffBJetTags" + tag,
                "TrackCountingHighPurBJetTags" + tag,
                ],
            tagInfoSources = [
                "ImpactParameterTagInfos" + tag,
                "SecondaryVertexTagInfos" + tag,
                ],
            addJetCharge = False,
            addTagInfos = True,
            ),
        process,
        sequence)

    addToSequence(
        'JetAnalyzer' + tag,
        inclusiveJetAnalyzer.clone(
            jetTag = cms.InputTag("slimmedJets"),
            genjetTag = 'ak4HiSignalGenJets',
            rParam = 0.4,
            matchJets = cms.untracked.bool(False),
            matchTag = 'patJetsWithBtagging',
            pfCandidateLabel = cms.untracked.InputTag('packedPFCandidates'),
            fillGenJets = False,
            isMC = False,
            doSubEvent = False,
            useHepMC = cms.untracked.bool(False),
            genParticles = cms.untracked.InputTag("genParticles"),
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
            ),
        process,
        sequence)