#include "HeterogeneousCore/SonicTriton/interface/TritonUtils.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Utilities/interface/Exception.h"

#include <sstream>
#include <iterator>

namespace TritonUtils {

  template <typename T>
  std::string printVec(const std::vector<T>& vec, const std::string& delim) {
    if (vec.empty())
      return "";
    std::stringstream msg;
    //avoid trailing delim
    std::copy(vec.begin(), vec.end() - 1, std::ostream_iterator<T>(msg, delim.c_str()));
    //last element
    msg << vec.back();
    return msg.str();
  }

  void wrap(const Error& err, const std::string& msg) {
    if (!err.IsOk())
      throw cms::Exception("TritonServerFailure") << msg << ": " << err;
  }

  bool warn(const Error& err, const std::string& msg) {
    if (!err.IsOk())
      edm::LogWarning("TritonServerWarning") << msg << ": " << err;
    return err.IsOk();
  }

}  // namespace TritonUtils

template std::string TritonUtils::printVec(const std::vector<int64_t>& vec, const std::string& delim);
template std::string TritonUtils::printVec(const std::vector<uint8_t>& vec, const std::string& delim);
template std::string TritonUtils::printVec(const std::vector<float>& vec, const std::string& delim);
