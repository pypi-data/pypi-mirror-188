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

#include <dart/math/lie_group/TangentBase.hpp>

namespace dart::math {

template <typename Derived>
class SE3TangentBase : public TangentBase<Derived>
{
public:
  using Base = TangentBase<Derived>;
  using Scalar = typename Base::Scalar;

  // LieGroup common
  using Base::Dim;
  using Base::DoF;
  using Base::ParamSize;
  using LieGroup = typename Base::LieGroup;
  using Tangent = typename Base::Tangent;
  using LieAlgebra = typename Base::LieAlgebra;
  using Params = typename Base::Params;

  using Base::derived;
  using Base::params;

  /**
   * Returns the hat operator of the given vector
   *
   * The hat operator is defined as follows:
   * @f[
   *   \hat{\xi} = \begin{bmatrix}
   *     \hat{w} & 0 \\
   *     \hat{v} & \hat{w}
   *   \end{bmatrix}
   * @f] where @f$ \xi = (w, v) @f$ and @f$ \hat{w} @f$ and @f$ \hat{v} @f$ are
   * the hat operators of @f$ w @f$ and @f$ v @f$ respectively.
   *
   * @param xi The vector to be converted to matrix
   */
  [[nodiscard]] LieAlgebra hat() const;

  /// Returns the exponential map of the given vector
  ///
  /// The exponential map of a vector @f$ \xi @f$ is an SO3 @f$ x @f$ such
  /// that @f$ \log(x) = \xi @f$.
  ///
  /// @param[in] dx The vector to be converted to an SO3.
  /// @param[in] tol The tolerance for the norm of the vector.
  /// @return The SO3.
  /// @tparam MatrixDrived The type of the vector
  [[nodiscard]] LieGroup exp(Scalar tol = LieGroupTol<Scalar>()) const;

  /// Returns the exponential map of the given vector
  ///
  /// The exponential map of a vector @f$ \xi @f$ is an SO3 @f$ x @f$ such
  /// that @f$ \log(x) = \xi @f$.
  ///
  /// This function also returns the Jacobian of the exponential map.
  ///
  /// @param[in] dx The vector to be converted to an SO3.
  /// @param[out] jacobian The Jacobian of the exponential map.
  /// @param[in] tol The tolerance for the norm of the vector.
  /// @return The SO3.
  /// @tparam MatrixDrivedA The type of the vector
  /// @tparam MatrixDerivedB The type of the Jacobian
  template <typename MatrixDerived>
  [[nodiscard]] LieGroup exp(
      Eigen::MatrixBase<MatrixDerived>* jacobian,
      Scalar tol = LieGroupTol<Scalar>()) const;

  auto angular() const
  {
    return params().template head<3>();
  }

  auto angular()
  {
    return params().template head<3>();
  }

  auto linear() const
  {
    return params().template tail<3>();
  }

  auto linear()
  {
    return params().template tail<3>();
  }
};

} // namespace dart::math

//==============================================================================
// Implementation
//==============================================================================

#include <dart/math/lie_group/SE3.hpp>

namespace dart::math {

//==============================================================================
template <typename Derived>
typename SE3TangentBase<Derived>::LieAlgebra SE3TangentBase<Derived>::hat()
    const
{
  LieAlgebra out = LieAlgebra::Zero();
  out.template topLeftCorner<3, 3>() = skew(angular());
  out.template topRightCorner<3, 1>() = linear();
  return out;
}

//==============================================================================
template <typename Derived>
typename SE3TangentBase<Derived>::LieGroup SE3TangentBase<Derived>::exp(
    Scalar tol) const
{
  const SO3<Scalar> rotation = SO3Tangent<Scalar>(angular()).exp(tol);
  const Eigen::Vector3<Scalar> translation
      = SO3<Scalar>::LeftJacobian(angular(), tol) * linear();
  // TODO(JS): Check if this version is faster than expMap() and expMapRot()
  return LieGroup(std::move(rotation), std::move(translation));
}

//==============================================================================
template <typename Derived>
template <typename MatrixDerived>
typename SE3TangentBase<Derived>::LieGroup SE3TangentBase<Derived>::exp(
    Eigen::MatrixBase<MatrixDerived>* jacobian, Scalar tol) const
{
  if (jacobian) {
    (*jacobian) = SE3<Scalar>::RightJacobian(params(), tol);
  }
  return exp(tol);
}

} // namespace dart::math
