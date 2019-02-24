using namespace std;

#include "DataFormats/HcalDigi/interface/HcalUHTRhistogramDigiCollection.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "CalibFormats/HcalObjects/interface/HcalDbService.h"
#include "CalibFormats/HcalObjects/interface/HcalDbRecord.h"
#include "RecoTBCalo/HcalTBObjectUnpacker/plugins/HcalUTCAhistogramUnpacker.h"
#include <iostream>


HcalUTCAhistogramUnpacker::HcalUTCAhistogramUnpacker(edm::ParameterSet const& conf)
{
  rawDump = conf.getParameter<bool>("rawDump"); //prints out lots of debugging info including the raw data
  fedNumbers_ = conf.getParameter<std::vector<int> >("fedNumbers");
  tok_raw_ = consumes<FEDRawDataCollection>(conf.getParameter<edm::InputTag>("fedRawDataCollectionTag"));
  produces<HcalUHTRhistogramDigiCollection>();
}

  // Virtual destructor needed.
  HcalUTCAhistogramUnpacker::~HcalUTCAhistogramUnpacker() { }  

  // Functions that gets called by framework every event
  void HcalUTCAhistogramUnpacker::produce(edm::Event& e, const edm::EventSetup& es)
  {
    edm::Handle<FEDRawDataCollection> rawraw;  
    edm::ESHandle<HcalElectronicsMap>   item;
    edm::ESHandle<HcalDbService> pSetup;
    
    e.getByToken(tok_raw_, rawraw);          
    es.get<HcalDbRecord>().get(pSetup);
    es.get<HcalElectronicsMapRcd>().get(item);
    
    const HcalElectronicsMap* readoutMap = item.product();
    //std::auto_ptr<HcalUHTRhistogramDigiCollection> hd(new HcalUHTRhistogramDigiCollection);
    auto hd = std::make_unique<HcalUHTRhistogramDigiCollection>();
    for (auto& it_fed : fedNumbers_) {
       const FEDRawData& fed = rawraw->FEDData(it_fed);
       histoUnpacker_.unpack(fed, *readoutMap, hd, rawDump);
    }    
    e.put(std::move(hd));
  }

#include "FWCore/PluginManager/interface/ModuleDef.h"
#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(HcalUTCAhistogramUnpacker);
