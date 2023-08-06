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

#include <dart/math/lie_group/SO3Base.hpp>
#include <dart/math/lie_group/SO3Tangent.hpp>

namespace Eigen::internal {

// TODO(JS): Move to a dedicated header file
/// @brief Specialization of Eigen::internal::traits for SO3
template <typename S>
struct traits<::dart::math::SO3<S>>
{
  using Scalar = S;

  // LieGroup common
  static constexpr int Dim = 3;
  static constexpr int DoF = 3;
  static constexpr int MatrixRepDim = 3;
  static constexpr int ParamSize = 4;
  using LieGroup = ::dart::math::SO3<S>;
  using MatrixType = ::Eigen::Matrix<S, MatrixRepDim, MatrixRepDim>;
  using Params = ::Eigen::Matrix<S, ParamSize, 1>;
  using Tangent = ::dart::math::SO3Tangent<S>;
};

} // namespace Eigen::internal

namespace dart::math {

/// @brief SO3 is a specialization of LieGroupBase for SO3
/// @tparam S The scalar type
template <typename S>
class SO3 : public SO3Base<SO3<S>>
{
public:
  using Base = SO3Base<SO3<S>>;
  using Scalar = typename Base::Scalar;

  // SO3 specifics
  using QuaternionType = typename Base::QuaternionType;
  using ConstQuaternionType = typename Base::ConstQuaternionType;

  // LieGroup types
  using Params = typename Base::Params;
  using LieGroup = typename Base::LieGroup;
  using MatrixType = typename Base::MatrixType;
  using Tangent = typename Base::Tangent;

  /// @brief Tag for the constructor that does not normalize the quaternion
  enum NoNormalizeTag
  {
    NO_NORMALIZE = 0,
  };

  enum class EulerConvention
  {
    INTRINSIC,
    EXTRINSIC,
  };

  template <typename MatrixDerived>
  [[nodiscard]] static LieGroup FromEulerAngles(
      const Eigen::MatrixBase<MatrixDerived>& angles,
      int axis0,
      int axis1,
      int axis2,
      EulerConvention convention = EulerConvention::INTRINSIC);

  template <typename MatrixDerived>
  [[nodiscard]] static LieGroup FromEulerXYZ(
      const Eigen::MatrixBase<MatrixDerived>& angles,
      EulerConvention convention = EulerConvention::INTRINSIC);

  /// Returns the vee operator of the given skew-symmetric matrix
  ///
  /// The vee operator of a skew-symmetric matrix @f$ \hat{v} @f$ is a vector
  /// @f$ v @f$ such that @f$ \hat{v} w = v \times w @f$ for any vector
  /// @f$ w @f$.
  ///
  /// @param[in] matrix The skew-symmetric matrix to be converted to a vector.
  /// @return The vector.
  /// @tparam MatrixDrived The type of the skew-symmetric matrix
  template <typename MatrixDerived>
  [[nodiscard]] static Tangent Vee(
      const Eigen::MatrixBase<MatrixDerived>& matrix);

  /// Returns the adjoint transformation of the given SO3
  ///
  /// The adjoint transformation of SO3 @f$ x @f$ is a matrix @f$ A @f$ such
  /// that @f$ A v = x v x^{-1} @f$ for any vector @f$ v @f$.
  ///
  /// @param[in] x The SO3 to be converted to a matrix.
  template <typename OtherDerived>
  [[nodiscard]] static Matrix3<S> Ad(const SO3Base<OtherDerived>& x);

  /// Returns the left Jacobian of the exponential map
  ///
  /// The left Jacobian of the exponential map is a matrix @f$ L @f$ such that
  /// @f$ Ad_{exp(L \xi)} = L Ad_{exp(\xi)} @f$ for any vector @f$ \xi @f$ and
  /// SO3. It expresses the change of the exponential map at the identity
  /// element to the exponential map at the group element.
  ///
  /// @param[in] xi The vector to be converted to a matrix.
  /// @param[in] tol The tolerance for the norm of the vector.
  /// @return The matrix.
  /// @tparam MatrixDrived The type of the vector
  /// @see RightJacobian()
  template <typename MatrixDrived>
  [[nodiscard]] static Matrix3<S> LeftJacobian(
      const Eigen::MatrixBase<MatrixDrived>& xi, S tol = LieGroupTol<Scalar>());

  /// Returns the right Jacobian of the exponential map
  ///
  /// The right Jacobian of the exponential map is a matrix @f$ R @f$ such that
  /// @f$ Ad_{exp(R \xi)} = Ad_{exp(\xi)} R @f$ for any vector @f$ \xi @f$ and
  /// SO3. It expresses the change of the exponential map at the group element
  /// to the exponential map at the identity element.
  ///
  /// @param[in] xi The vector to be converted to a matrix.
  /// @param[in] tol The tolerance for the norm of the vector.
  /// @return The matrix.
  /// @tparam MatrixDrived The type of the vector
  /// @see LeftJacobian()
  template <typename MatrixDrived>
  [[nodiscard]] static Matrix3<S> RightJacobian(
      const Eigen::MatrixBase<MatrixDrived>& xi, S tol = LieGroupTol<Scalar>());

  /// Returns the left Jacobian inverse of the exponential map
  ///
  /// @param[in] dx The vector to be converted to a matrix.
  /// @param[in] tol The tolerance for the norm of the vector.
  /// @return The matrix.
  /// @tparam MatrixDrived The type of the vector
  /// @see RightJacobianInverse()
  template <typename MatrixDrived>
  [[nodiscard]] static Matrix3<S> LeftJacobianInverse(
      const Eigen::MatrixBase<MatrixDrived>& dx, S tol = LieGroupTol<Scalar>());

  /// Returns the right Jacobian inverse of the exponential map
  ///
  /// @param[in] dx The vector to be converted to a matrix.
  /// @param[in] tol The tolerance for the norm of the vector.
  /// @return The matrix.
  /// @tparam MatrixDrived The type of the vector
  /// @see LeftJacobianInverse()
  template <typename MatrixDerived>
  [[nodiscard]] static Matrix3<S> RightJacobianInverse(
      const Eigen::MatrixBase<MatrixDerived>& dx,
      S tol = LieGroupTol<Scalar>());

  /// Default constructor that initializes the quaternion to identity
  SO3();

  /// Default constructor that does not initialize the quaternion
  ///
  /// This constructor is useful when the quaternion is going to be initialized
  /// later.
  explicit SO3(NoInitializeTag);

  DART_DEFINE_CONSTRUCTORS_FOR_CONCRETE(SO3);

  /// Constructs an SO3 from a quaternion
  template <typename QuaternionDrived>
  explicit SO3(const ::Eigen::QuaternionBase<QuaternionDrived>& quat);

  /// Constructs an SO3 from a quaternion
  ///
  /// This constructor does not normalize the quaternion. It is useful when
  /// constructing SO3 from a quaternion that is already normalized.
  template <typename QuaternionDrived>
  explicit SO3(
      const ::Eigen::QuaternionBase<QuaternionDrived>& quat, NoNormalizeTag);

  /// Constructs an SO3 from a quaternion
  template <typename QuaternionDrived>
  explicit SO3(::Eigen::QuaternionBase<QuaternionDrived>&& quat);

  /// Constructs an SO3 from a quaternion
  ///
  /// This constructor does not normalize the quaternion. It is useful when
  /// constructing SO3 from a quaternion that is already normalized.
  template <typename QuaternionDrived>
  explicit SO3(
      ::Eigen::QuaternionBase<QuaternionDrived>&& quat, NoNormalizeTag);

  /// Copy assignment operator
  /// @param[in] other The other SO3 to be copied
  /// @return Reference to this SO3
  SO3& operator=(const SO3& other);

  /// Move assignment operator
  /// @param[in] other The other SO3 to be moved
  /// @return Reference to this SO3
  SO3& operator=(SO3&& other) noexcept;

  using Base::normalize;
  using Base::quaternion;

  /// Returns the parameters of the underlying quaternion
  [[nodiscard]] const Params& params() const;

  /// Returns the parameters of the underlying quaternion
  [[nodiscard]] Params& params();

private:
  /// The underlying quaternion parameters
  Params m_params;
};

DART_TEMPLATE_CLASS_HEADER(MATH, SO3);

} // namespace dart::math

//==============================================================================
// Implementation
//==============================================================================

namespace dart::math {

//==============================================================================
template <typename S>
template <typename MatrixDerived>
typename SO3<S>::LieGroup SO3<S>::FromEulerAngles(
    const Eigen::MatrixBase<MatrixDerived>& angles,
    int axis0,
    int axis1,
    int axis2,
    EulerConvention convention)
{
  if (convention == EulerConvention::EXTRINSIC) {
    return FromEulerAngles(
        angles.reverse(), 2, 1, 0, EulerConvention::INTRINSIC);
  }

  return SO3<S>(Quaternion<S>(
      AngleAxis<S>(angles[0], Vector3<S>::Unit(axis0))
      * AngleAxis<S>(angles[1], Vector3<S>::Unit(axis1))
      * AngleAxis<S>(angles[2], Vector3<S>::Unit(axis2))));
}

//==============================================================================
template <typename S>
template <typename MatrixDerived>
typename SO3<S>::Tangent SO3<S>::Vee(
    const Eigen::MatrixBase<MatrixDerived>& matrix)
{
  return Tangent(matrix(2, 1), matrix(0, 2), matrix(1, 0));
}

//==============================================================================
template <typename S>
template <typename OtherDerived>
Matrix3<S> SO3<S>::Ad(const SO3Base<OtherDerived>& x)
{
  return x.quaternion().toRotationMatrix();
}

//==============================================================================
template <typename S>
template <typename OtherDerived>
Matrix3<S> SO3<S>::LeftJacobian(
    const Eigen::MatrixBase<OtherDerived>& xi, S tol)
{
  Matrix3<S> J = Matrix3<S>::Identity();

  const S t = xi.norm();

  if (t < tol) {
    J.noalias() += skew(0.5 * xi);
    return J;
  }

  const S t2 = t * t;
  const S t3 = t2 * t;
  const S st = std::sin(t);
  const S ct = std::cos(t);
  const Matrix3<S> A = skew(xi);
  J.noalias() += ((1 - ct) / t2) * A;
  J.noalias() += ((t - st) / t3) * A * A;

  return J;
}

//==============================================================================
template <typename S>
template <typename OtherDerived>
Matrix3<S> SO3<S>::RightJacobian(
    const Eigen::MatrixBase<OtherDerived>& xi, S tol)
{
  return LeftJacobian(-xi, tol);
}

//==============================================================================
template <typename S>
template <typename OtherDerived>
Matrix3<S> SO3<S>::LeftJacobianInverse(
    const Eigen::MatrixBase<OtherDerived>& dx, S tol)
{
  Matrix3<S> J = Matrix3<S>::Identity();

  const S theta = dx.norm();
  if (theta < tol) {
    J.noalias() += skew(0.5 * dx);
    return J;
  }

  const S t2 = theta * theta;
  const S st = std::sin(theta);
  const S ct = std::cos(theta);
  const Matrix3<S> A = skew(dx);
  J.noalias() -= 0.5 * A;
  J.noalias() += (1 / t2 - (1 + ct) / (2 * theta * st)) * A * A;

  return J;
}

//==============================================================================
template <typename S>
template <typename OtherDerived>
Matrix3<S> SO3<S>::RightJacobianInverse(
    const Eigen::MatrixBase<OtherDerived>& dx, S tol)
{
  return LeftJacobianInverse(-dx, tol);
}

//==============================================================================
template <typename S>
SO3<S>::SO3() : m_params(::Eigen::Quaternion<S>::Identity().coeffs())
{
  // Do nothing
}

//==============================================================================
template <typename S>
SO3<S>::SO3(NoInitializeTag)
{
  // Do nothing
}

//==============================================================================
template <typename S>
template <typename QuaternionDrived>
SO3<S>::SO3(const ::Eigen::QuaternionBase<QuaternionDrived>& quat)
  : m_params(quat.coeffs())
{
  normalize();
}

//==============================================================================
template <typename S>
template <typename QuaternionDrived>
SO3<S>::SO3(
    const ::Eigen::QuaternionBase<QuaternionDrived>& quat, NoNormalizeTag)
  : m_params(quat.coeffs())
{
  // Do nothing
}

//==============================================================================
template <typename S>
template <typename QuaternionDrived>
SO3<S>::SO3(::Eigen::QuaternionBase<QuaternionDrived>&& quat)
  : m_params(std::move(quat.coeffs()))
{
  normalize();
}

//==============================================================================
template <typename S>
template <typename QuaternionDrived>
SO3<S>::SO3(::Eigen::QuaternionBase<QuaternionDrived>&& quat, NoNormalizeTag)
  : m_params(std::move(quat.coeffs()))
{
  // Do nothing
}

//==============================================================================
template <typename S>
SO3<S>& SO3<S>::operator=(const SO3& other)
{
  m_params = other.m_params;
  return *this;
}

//==============================================================================
template <typename S>
SO3<S>& SO3<S>::operator=(SO3&& other) noexcept
{
  m_params = std::move(other.m_params);
  return *this;
}

//==============================================================================
template <typename S>
const typename SO3<S>::Params& SO3<S>::params() const
{
  return m_params;
}

//==============================================================================
template <typename S>
typename SO3<S>::Params& SO3<S>::params()
{
  return m_params;
}

} // namespace dart::math
