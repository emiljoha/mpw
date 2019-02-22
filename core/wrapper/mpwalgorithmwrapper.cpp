#include <boost/python.hpp>
#include <Python.h>
#include <string>

extern "C" {
#include "mpw-algorithm/mpw-algorithm.h"
}
#include "conversions.h"
const char *wrapper_siteResult(const char *fullName,
			       const char *masterPassword,
			       const char *siteName,
			       const MPCounterValue siteCounter,
			       const char *strKeyPurpose,
			       const char *strResultType,
			       const int algorithmVersion);
const char *wrapper_identicon(const char *fullName,
			      const char *masterPassword);
MPMasterKey wrapper_masterKey(const char *fullName,
			      const char *masterPassword,
			      const MPAlgorithmVersion algorithmVersion);
MPResultType mpwResultTypeFromString(const char *resultType);
MPKeyPurpose mpKeyPurposeTypeFromString(const char *strKeyPurpose);

using namespace std;
using namespace boost::python;
BOOST_PYTHON_MODULE(pympw)
{
  docstring_options local_docstring_options(true, true, false);
  to_python_converter<
    MPMasterKey,
    MPMasterKey_to_python_string>();
  def("masterKey", wrapper_masterKey,
      return_value_policy<return_by_value>());
  def("siteResult", wrapper_siteResult,
      return_value_policy<return_by_value>());
  def("identicon", wrapper_identicon,
      return_value_policy<return_by_value>());
}

const char *wrapper_identicon(const char *fullName,
			      const char *masterPassword)
{
  MPIdenticon id = mpw_identicon(fullName,
				 masterPassword);
  size_t identiconSize = strlen(id.leftArm) + strlen(id.body)
    + strlen(id.rightArm) + strlen(id.accessory);
  char * identiconString = (char *)calloc(identiconSize, sizeof(char));
  strcpy(identiconString, id.leftArm);
  strcat(identiconString, id.body);
  strcat(identiconString, id.rightArm);
  strcat(identiconString, id.accessory);
  return identiconString;
}

const char *wrapper_siteResult(const char *fullName,
			       const char *masterPassword,
			       const char *siteName,
			       const MPCounterValue siteCounter,
			       const char *strKeyPurpose,
			       const char *strResultType,
			       const int algorithmVersion)
{
  MPMasterKey masterKey = mpw_masterKey(fullName,
					masterPassword,
					algorithmVersion);
  /* Translate c-strings into types defined in mpw-types.h */
  MPKeyPurpose keyPurpose = mpKeyPurposeTypeFromString(strKeyPurpose);
  MPResultType resultType = mpwResultTypeFromString(strResultType);
  const char *keyContext = NULL;
  const char *resultParam = NULL;
  return mpw_siteResult(masterKey, siteName, siteCounter,
			keyPurpose, keyContext, resultType, resultParam,
			algorithmVersion);
}

MPMasterKey wrapper_masterKey(const char *fullName,
			      const char *masterPassword,
			      const MPAlgorithmVersion algorithmVersion)
{
  return mpw_masterKey(fullName,
		       masterPassword,
		       algorithmVersion);
}
MPResultType mpwResultTypeFromString(const char *resultType)
{
  MPResultType result;
  if (strncmp("Maximum", resultType, strlen("Maximum")) == 0)
    result = MPResultTypeTemplateMaximum;
  else if (strncmp("Long", resultType, strlen("Long")) == 0)
    result = MPResultTypeTemplateLong;
  else if (strncmp("Medium", resultType, strlen("Medium")) == 0)
    result = MPResultTypeTemplateMedium;
  else if (strncmp( "Basic", resultType, strlen("Basic")) == 0)
    result = MPResultTypeTemplateBasic;
  else if (strncmp( "Short", resultType, strlen("Short")) == 0)
    result = MPResultTypeTemplateShort;
  else if (strncmp( "PIN", resultType, strlen("PIN")) == 0)
    result = MPResultTypeTemplatePIN;
  else if (strncmp( "Name", resultType, strlen("Name")) == 0)
    result = MPResultTypeTemplateName;
  else if (strncmp( "Phrase", resultType, strlen("Phrase")) == 0)
    result = MPResultTypeTemplatePhrase;
  else {
    printf("Error: No such result type: %s. Using default type\n", resultType);
    result = MPResultTypeDefault;
  }
  return result;
}

MPKeyPurpose mpKeyPurposeTypeFromString(const char *strKeyPurpose)
{
  MPKeyPurpose result;
  if (strncmp("Authentication", strKeyPurpose, strlen("Authentication")) == 0)
    result = MPKeyPurposeAuthentication;
  else if (strncmp("Identification", strKeyPurpose, strlen("Identification")) == 0)
    result = MPKeyPurposeIdentification;
  else if (strncmp("Recovery", strKeyPurpose, strlen("Recovery")) == 0)
    result = MPKeyPurposeRecovery;
  else {
    printf("Error: No such key purpose type: %s. Using Authentication\n", strKeyPurpose);
    result = MPKeyPurposeAuthentication;
  }
  return result;
}
