#ifndef GeomPropagators_TrackerBounds_H
#define GeomPropagators_TrackerBounds_H

#include "DataFormats/GeometrySurface/interface/ReferenceCounted.h"
#include "DataFormats/GeometryVector/interface/GlobalPoint.h"

class Cylinder;
class Disk;

/** A definition of the envelope that contains the tracker
 *  sensitive detectors.
 *  The information is not automatically computed from the
 *  Tracker geometry, but is hard-coded in this class.
 *  However, there is very little freedom to modify the
 *  tracker size (ECAL constraint...),
 *  so a fast access to this information is very useful.
 *  The recommended use is: Inside the TrackerBounds
 *  tracker propagators are expected to work accurately.
 *  Outside of this volume use some kind of geane.

 *  Ported from ORCA
 */

class TrackerBounds {
public:
  static const Cylinder& barrelBound() { return *theCylinder; }
  static const Disk& negativeEndcapDisk() { return *theNegativeDisk; }
  static const Disk& positiveEndcapDisk() { return *thePositiveDisk; }

  /** Hard-wired numbers defining the envelope of the sensitive volumes.
   */
  static float radius() { return 112.f; }
  static float halfLength() { return 273.5f; }
  static bool isInside(const GlobalPoint&);

private:
  static const ReferenceCountingPointer<Cylinder> theCylinder;
  static const ReferenceCountingPointer<Disk> theNegativeDisk;
  static const ReferenceCountingPointer<Disk> thePositiveDisk;
};

#endif
