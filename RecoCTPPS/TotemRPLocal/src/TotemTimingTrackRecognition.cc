/****************************************************************************
 *
 * This is a part of CTPPS offline software.
 * Authors:
 *   Laurent Forthomme (laurent.forthomme@cern.ch)
 *   Nicola Minafra (nicola.minafra@cern.ch)
 *   Mateusz Szpyrka (mateusz.szpyrka@cern.ch)
 *
 ****************************************************************************/

#include "RecoCTPPS/TotemRPLocal/interface/TotemTimingTrackRecognition.h"

//----------------------------------------------------------------------------------------------------

TotemTimingTrackRecognition::TotemTimingTrackRecognition( const edm::ParameterSet& iConfig ) :
  CTPPSTimingTrackRecognition<TotemTimingLocalTrack, TotemTimingRecHit>( iConfig ),
  tolerance_( iConfig.getParameter<double>( "tolerance" ) )
{}

//----------------------------------------------------------------------------------------------------

void
TotemTimingTrackRecognition::addHit( const TotemTimingRecHit& recHit )
{
  if ( recHit.getT() != TotemTimingRecHit::NO_T_AVAILABLE )
    hitVectorMap_[0].emplace_back( recHit );
}

//----------------------------------------------------------------------------------------------------

int
TotemTimingTrackRecognition::produceTracks( edm::DetSet<TotemTimingLocalTrack>& tracks )
{
  int numberOfTracks = 0;
  DimensionParameters param;

  auto getX = []( const TotemTimingRecHit& hit ){ return hit.getX(); };
  auto getXWidth = []( const TotemTimingRecHit& hit ){ return hit.getXWidth(); };
  auto setX = []( TotemTimingLocalTrack& track, float x ){ track.setPosition( math::XYZPoint( x, 0., 0. ) ); };
  auto setXSigma = []( TotemTimingLocalTrack& track, float sigma ){ track.setPositionSigma( math::XYZPoint( sigma, 0., 0. ) ); };
  auto getY = []( const TotemTimingRecHit& hit ){ return hit.getY(); };
  auto getYWidth = []( const TotemTimingRecHit& hit ){ return hit.getYWidth(); };
  auto setY = []( TotemTimingLocalTrack& track, float y ){ track.setPosition( math::XYZPoint( 0., y, 0. ) ); };
  auto setYSigma = []( TotemTimingLocalTrack& track, float sigma ){ track.setPositionSigma( math::XYZPoint( 0., sigma, 0. ) ); };

  for ( const auto& hitBatch : hitVectorMap_ ) {
    const auto& hits = hitBatch.second;
    const auto& hitRange = getHitSpatialRange( hits );

    std::vector<TotemTimingLocalTrack> xPartTracks, yPartTracks;

    param.rangeBegin = hitRange.xBegin;
    param.rangeEnd = hitRange.xEnd;
    producePartialTracks( hits, param, getX, getXWidth, setX, setXSigma, xPartTracks );

    param.rangeBegin = hitRange.yBegin;
    param.rangeEnd = hitRange.yEnd;
    producePartialTracks( hits, param, getY, getYWidth, setY, setYSigma, yPartTracks );

    if ( xPartTracks.empty() && yPartTracks.empty() )
     continue;

    unsigned int validHitsNumber = (unsigned int)threshold_+1;

    for ( const auto& xTrack : xPartTracks ) {
      for ( const auto& yTrack : yPartTracks ) {
        math::XYZPoint position( xTrack.getX0(), yTrack.getY0(), 0.5f*( hitRange.zBegin + hitRange.zEnd ) );
        math::XYZPoint positionSigma( xTrack.getX0Sigma(), yTrack.getY0Sigma(), 0.5f*( hitRange.zEnd - hitRange.zBegin ) );

        TotemTimingLocalTrack newTrack( position, positionSigma, 0., 0. );

        std::vector<TotemTimingRecHit> componentHits;
        for ( const auto& hit : hits )
          if ( newTrack.containsHit( hit, tolerance_ ) )
            componentHits.emplace_back( hit );

        if ( componentHits.size() < validHitsNumber )
          continue;

        // Calculating time
        //    track's time = weighted mean of all hit times with time precision as weight
        //    track's time sigma = uncertainty of the weighted mean
        // hit is ignored if the time precision is equal to 0

        float meanNumerator = 0.f, meanDenominator = 0.f;
        bool validHits = false;
        for ( const auto& hit : componentHits ) {
          if ( hit.getTPrecision() == 0. )
            continue;

          validHits = true; // at least one valid hit to account for
          const float weight = 1.f / ( hit.getTPrecision() * hit.getTPrecision() );
          meanNumerator += weight * hit.getT();
          meanDenominator += weight;
        }

        const float meanTime = validHits ? ( meanNumerator / meanDenominator ) : 0.f;
        const float timeSigma = validHits ? ( std::sqrt( 1.f / meanDenominator ) ) : 0.f;
        newTrack.setValid( validHits );
        newTrack.setT( meanTime );
        newTrack.setTSigma( timeSigma );
        // in a next iteration, we will be setting validity / numHits / numPlanes
        tracks.push_back( newTrack );
      }
    }
  }

  return numberOfTracks;
}

