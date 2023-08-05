/*
 * Copyright 2015-2021 The OpenSSL Project Authors. All Rights Reserved.
 *
 * Licensed under the Apache License 2.0 (the "License").  You may not use
 * this file except in compliance with the License.  You can obtain a copy
 * in the file LICENSE in the source distribution or at
 * https://www.openssl.org/source/license.html
 */

#include "openssl/ocsp.h"
#include "openssl/x509.h"


//   CertID ::= SEQUENCE {
//       hashAlgorithm    AlgorithmIdentifier,
//       issuerNameHash   OCTET STRING,  --Hash of Issuer's DN
//       issuerKeyHash    OCTET STRING,  --Hash of Issuers public key (excluding the tag & length fields)
//       serialNumber     CertificateSerialNumber }
//
struct ocsp_cert_id_st {
  X509_ALGOR *hashAlgorithm;
  ASN1_OCTET_STRING *issuerNameHash;
  ASN1_OCTET_STRING *issuerKeyHash;
  ASN1_INTEGER *serialNumber;
};

//   Signature ::= SEQUENCE {
//       signatureAlgorithm   AlgorithmIdentifier,
//       signature            BIT STRING,
//       certs                [0] EXPLICIT SEQUENCE OF Certificate OPTIONAL }
//
struct ocsp_signature_st {
  X509_ALGOR *signatureAlgorithm;
  ASN1_BIT_STRING *signature;
  STACK_OF(X509) *certs;
};


//   OCSPResponseStatus ::= ENUMERATED {
//       successful         (0),  --Response has valid confirmations
//       malformedRequest   (1),  --Illegal confirmation request
//       internalError      (2),  --Internal error in issuer
//       tryLater           (3),  --Try again later
//                                --(4) is not used
//       sigRequired        (5),  --Must sign the request
//       unauthorized       (6)   --Request unauthorized
//   }
//

//   ResponseBytes ::= SEQUENCE {
//       responseType   OBJECT IDENTIFIER,
//       response       OCTET STRING }
//
struct ocsp_resp_bytes_st {
  ASN1_OBJECT *responseType;
  ASN1_OCTET_STRING *response;
};

//   OCSPResponse ::= SEQUENCE {
//      responseStatus   OCSPResponseStatus,
//      responseBytes    [0] EXPLICIT ResponseBytes OPTIONAL }
//
struct ocsp_response_st {
  ASN1_ENUMERATED *responseStatus;
  OCSP_RESPBYTES *responseBytes;
};

//  ResponderID ::= CHOICE {
//      byName   [1]   Name,
//      byKey    [2]   KeyHash }
//
//   KeyHash ::= OCTET STRING --SHA-1 hash of responder's public key
//                            --(excluding the tag and length fields)
//
struct ocsp_responder_id_st {
  int type;
  union {
    X509_NAME *byName;
    ASN1_OCTET_STRING *byKey;
  } value;
};



//   RevokedInfo ::= SEQUENCE {
//     revocationTime     GeneralizedTime,
//     revocationReason   [0] EXPLICIT CRLReason OPTIONAL }
//
struct ocsp_revoked_info_st {
  ASN1_GENERALIZEDTIME *revocationTime;
  ASN1_ENUMERATED *revocationReason;
};

//   CertStatus ::= CHOICE {
//       good      [0] IMPLICIT NULL,
//       revoked   [1] IMPLICIT RevokedInfo,
//       unknown   [2] IMPLICIT UnknownInfo }
//
struct ocsp_cert_status_st {
  int type;
  union {
    ASN1_NULL *good;
    OCSP_REVOKEDINFO *revoked;
    ASN1_NULL *unknown;
  } value;
};

//   SingleResponse ::= SEQUENCE {
//      certID             CertID,
//      certStatus         CertStatus,
//      thisUpdate         GeneralizedTime,
//      nextUpdate         [0] EXPLICIT GeneralizedTime OPTIONAL,
//      singleExtensions   [1] EXPLICIT Extensions OPTIONAL }
//
struct ocsp_single_response_st {
  OCSP_CERTID *certId;
  OCSP_CERTSTATUS *certStatus;
  ASN1_GENERALIZEDTIME *thisUpdate;
  ASN1_GENERALIZEDTIME *nextUpdate;
  STACK_OF(X509_EXTENSION) *singleExtensions;
};

//   ResponseData ::= SEQUENCE {
//      version              [0] EXPLICIT Version DEFAULT v1,
//      responderID          ResponderID,
//      producedAt           GeneralizedTime,
//      responses            SEQUENCE OF SingleResponse,
//      responseExtensions   [1] EXPLICIT Extensions OPTIONAL }
//
struct ocsp_response_data_st {
  ASN1_INTEGER *version;
  OCSP_RESPID *responderId;
  ASN1_GENERALIZEDTIME *producedAt;
  STACK_OF(OCSP_SINGLERESP) *responses;
  STACK_OF(X509_EXTENSION) *responseExtensions;
};

//   BasicOCSPResponse ::= SEQUENCE {
//      tbsResponseData      ResponseData,
//      signatureAlgorithm   AlgorithmIdentifier,
//      signature            BIT STRING,
//      certs                [0] EXPLICIT SEQUENCE OF Certificate OPTIONAL }
//
//
// Note 1: The value for "signature" is specified in the OCSP rfc2560 as
// follows: "The value for the signature SHALL be computed on the hash of
// the DER encoding ResponseData." This means that you must hash the
// DER-encoded tbsResponseData, and then run it through a crypto-signing
// function, which will (at least w/RSA) do a hash-'n'-private-encrypt
// operation.  This seems a bit odd, but that's the spec.  Also note that
// the data structures do not leave anywhere to independently specify the
// algorithm used for the initial hash. So, we look at the
// signature-specification algorithm, and try to do something intelligent.
// -- Kathy Weinhold, CertCo
//
// Note 2: It seems that the mentioned passage from RFC 2560 (section
// 4.2.1) is open for interpretation.  I've done tests against another
// responder, and found that it doesn't do the double hashing that the RFC
// seems to say one should.  Therefore, all relevant functions take a flag
// saying which variant should be used.  -- Richard Levitte, OpenSSL team
// and CeloCom
struct ocsp_basic_response_st {
  OCSP_RESPDATA *tbsResponseData;
  X509_ALGOR *signatureAlgorithm;
  ASN1_BIT_STRING *signature;
  STACK_OF(X509) *certs;
};

// Returns |OCSP_SINGLERESP| in the index of |OCSP_BASICRESP|.
OCSP_SINGLERESP *OCSP_resp_get0(OCSP_BASICRESP *bs, size_t idx);

// Returns index of |OCSP_SINGLERESP| in |OCSP_BASICRESP| matching a
// given certificate ID, returns -1 if not found.
int OCSP_resp_find(OCSP_BASICRESP *bs, OCSP_CERTID *id, int last);

// Returns status of |OCSP_SINGLERESP|
//
// Note: 1. Reason value is allowed to be null.
//       2. Time values passed into function are allowed to be NULL if certificate
//          fields are empty.
//       3. revtime and reason values only set if the certificate status is revoked.
int OCSP_single_get0_status(OCSP_SINGLERESP *single, int *reason,
                                     ASN1_GENERALIZEDTIME **revtime,
                                     ASN1_GENERALIZEDTIME **thisupd,
                                     ASN1_GENERALIZEDTIME **nextupd);

OCSP_CERTID *OCSP_cert_id_new(const EVP_MD *dgst,
                               const X509_NAME *issuerName,
                               const ASN1_BIT_STRING *issuerKey,
                               const ASN1_INTEGER *serialNumber);

// --- OCSP compare functions ---
// Compares certificate id issuers, returns 0 on equal.
int OCSP_id_issuer_cmp(const OCSP_CERTID *a, const OCSP_CERTID *b);

// Compares certificate id, returns 0 on equal.
int OCSP_id_cmp(const OCSP_CERTID *a, const OCSP_CERTID *b);
