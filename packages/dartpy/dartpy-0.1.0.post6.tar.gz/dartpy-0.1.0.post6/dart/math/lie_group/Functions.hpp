/*
 * Copyright (c) 2011-2023, The DART development contributors
 * All rights reserved.
 *
 * The list of contributors can be found at:
 *   https://github.com/dartsim/dart/blob/master/LICENSE
 *
 * This file is provided under the following "BSD-style" License:
 *   Redistribution and use in source and binary forms, with or
 *   without modification, are permitted provided that the following
 *   conditions are met:
 *   * Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *   * Redistributions in binary form must reproduce the above
 *     copyright notice, this list of conditions and the following
 *     disclaimer in the documentation and/or other materials provided
 *     with the distribution.
 *   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
 *   CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
 *   INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 *   MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 *   DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
 *   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 *   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 *   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
 *   USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
 *   AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 *   LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 *   ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *   POSSIBILITY OF SUCH DAMAGE.
 */

#pragma once

#include <dart/math/Fwd.hpp>
#include <dart/math/lie_group/Helpers.hpp>

namespace dart::math {

template <typename Derived>
[[nodiscard]] typename Derived::LieAlgebra Hat(
    const TangentBase<Derived>& tangent);

/// Exponential map of a Lie group element
///
/// @param[in] tangent Tangent vector
/// @param[in] tol Tolerance for the convergence of the exponential map
/// @return Lie group element
template <typename Derived>
[[nodiscard]] typename Derived::LieGroup Exp(
    const TangentBase<Derived>& tangent,
    typename Derived::Scalar tol = LieGroupTol<typename Derived::Scalar>());

/// Logarithmic map of a Lie group element
///
/// @param[in] x Lie group element
/// @param[in] tol Tolerance for the convergence of the logarithmic map
/// @return Tangent vector
template <typename Derived>
[[nodiscard]] typename Derived::Tangent Log(
    const LieGroupBase<Derived>& x,
    typename Derived::Scalar tol = LieGroupTol<typename Derived::Scalar>());

} // namespace dart::math

//==============================================================================
//
//==============================================================================

namespace dart::math {

//==============================================================================
template <typename Derived>
typename Derived::LieAlgebra Hat(const TangentBase<Derived>& tangent)
{
  return tangent.hat();
}

//==============================================================================
template <typename Derived>
typename Derived::Tangent Vee(const LieGroupBase<Derived>& x)
{
  return x.vee();
}

//==============================================================================
template <typename Derived>
typename Derived::LieGroup Exp(
    const TangentBase<Derived>& tangent, typename Derived::Scalar tol)
{
  return tangent.exp(tol);
}

//==============================================================================
template <typename Derived>
typename Derived::Tangent Log(
    const LieGroupBase<Derived>& x, typename Derived::Scalar tol)
{
  return x.log(tol);
}

} // namespace dart::math
