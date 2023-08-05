/* Copyright (C) 1995-1998 Eric Young (eay@cryptsoft.com)
 * All rights reserved.
 *
 * This package is an SSL implementation written
 * by Eric Young (eay@cryptsoft.com).
 * The implementation was written so as to conform with Netscapes SSL.
 *
 * This library is free for commercial and non-commercial use as long as
 * the following conditions are aheared to.  The following conditions
 * apply to all code found in this distribution, be it the RC4, RSA,
 * lhash, DES, etc., code; not just the SSL code.  The SSL documentation
 * included with this distribution is covered by the same copyright terms
 * except that the holder is Tim Hudson (tjh@cryptsoft.com).
 *
 * Copyright remains Eric Young's, and as such any Copyright notices in
 * the code are not to be removed.
 * If this package is used in a product, Eric Young should be given attribution
 * as the author of the parts of the library used.
 * This can be in the form of a textual message at program startup or
 * in documentation (online or textual) provided with the package.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. All advertising materials mentioning features or use of this software
 *    must display the following acknowledgement:
 *    "This product includes cryptographic software written by
 *     Eric Young (eay@cryptsoft.com)"
 *    The word 'cryptographic' can be left out if the rouines from the library
 *    being used are not cryptographic related :-).
 * 4. If you include any Windows specific code (or a derivative thereof) from
 *    the apps directory (application code) you must include an acknowledgement:
 *    "This product includes software written by Tim Hudson (tjh@cryptsoft.com)"
 *
 * THIS SOFTWARE IS PROVIDED BY ERIC YOUNG ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 * The licence and distribution terms for any publically available version or
 * derivative of this code cannot be changed.  i.e. this code cannot simply be
 * copied and put under another distribution licence
 * [including the GNU Public Licence.] */

#ifndef OPENSSL_HEADER_TYPE_CHECK_H
#define OPENSSL_HEADER_TYPE_CHECK_H

#include <openssl/base.h>

#if defined(__cplusplus)
extern "C" {
#endif


// Previously we defined |OPENSSL_STATIC_ASSERT| to use one of two keywords:
// |Static_assert| or |static_assert|. The latter was used if we were compiling
// a C++ translation unit or on Windows (excluding when using a Clang compiler).
// The former was used in other cases. However, these two keywords are not
// defined before C11. So, we can't rely on these when we want to be C99
// compliant. If we at some point decide that we want to only be compliant with
// C11 (and up), we can reintroduce these keywords. Instead, use a method that
// is guaranteed to be C99 compliant and still give us an equivalent static
// assert mechanism.
//
// The solution below defines a struct type containing a bit field.
// The name of that type is |static_assertion_msg|. |msg| is a concatenation of
// a user-chosen error (which should be chosen with respect to actual assertion)
// and the line the assertion is defined. This should ensure name uniqueness.
// The width of the bit field is set to 1 or -1, depending on the evaluation of
// the boolean expression |cond|. If the condition is false, the width requested
// is -1, which is illegal and would cause the compiler to throw an error.
//
// An example of an error thrown during compilation:
// ```
// error: negative width in bit-field 
//      'static_assertion_at_line_913_error_is_AEAD_state_is_too_small'
// ```
#define AWSLC_CONCAT(left, right) left##right
#define AWSLC_STATIC_ASSERT_DEFINE(cond, msg) typedef struct { \
        unsigned int AWSLC_CONCAT(static_assertion_, msg) : (cond) ? 1 : - 1; \
    } AWSLC_CONCAT(static_assertion_, msg) OPENSSL_UNUSED;
#define AWSLC_STATIC_ASSERT_ADD_LINE0(cond, suffix) AWSLC_STATIC_ASSERT_DEFINE(cond, AWSLC_CONCAT(at_line_, suffix))
#define AWSLC_STATIC_ASSERT_ADD_LINE1(cond, line, suffix) AWSLC_STATIC_ASSERT_ADD_LINE0(cond, AWSLC_CONCAT(line, suffix))
#define AWSLC_STATIC_ASSERT_ADD_LINE2(cond, suffix) AWSLC_STATIC_ASSERT_ADD_LINE1(cond, __LINE__, suffix)
#define AWSLC_STATIC_ASSERT_ADD_ERROR(cond, suffix) AWSLC_STATIC_ASSERT_ADD_LINE2(cond, AWSLC_CONCAT(_error_is_, suffix))
#define OPENSSL_STATIC_ASSERT(cond, error) AWSLC_STATIC_ASSERT_ADD_ERROR(cond, error)

// CHECKED_CAST casts |p| from type |from| to type |to|.
//
// TODO(davidben): Although this macro is not public API and is unused in
// BoringSSL, wpa_supplicant uses it to define its own stacks. Remove this once
// wpa_supplicant has been fixed.
#define CHECKED_CAST(to, from, p) ((to) (1 ? (p) : (from)0))


#if defined(__cplusplus)
}  // extern C
#endif

#endif  // OPENSSL_HEADER_TYPE_CHECK_H
