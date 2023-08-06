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

#include "dart/math/Geometry.hpp"

#include "dart/common/Console.hpp"
#include "dart/math/Helpers.hpp"
#include "dart/math/LieGroups.hpp"

#include <algorithm>
#include <iomanip>
#include <iostream>
#include <vector>

#include <cassert>
#include <cmath>

#define DART_EPSILON 1e-6

namespace dart {
namespace math {

// Reference:
// http://www.geometrictools.com/LibMathematics/Algebra/Wm5Matrix3.inl
Vector3d matrixToEulerXYX(const Matrix3d& _R)
{
  // +-           -+   +-                                                -+
  // | r00 r01 r02 |   |  cy      sy*sx1               sy*cx1             |
  // | r10 r11 r12 | = |  sy*sx0  cx0*cx1-cy*sx0*sx1  -cy*cx1*sx0-cx0*sx1 |
  // | r20 r21 r22 |   | -sy*cx0  cx1*sx0+cy*cx0*sx1   cy*cx0*cx1-sx0*sx1 |
  // +-           -+   +-                                                -+

  if (_R(0, 0) < 1.0) {
    if (_R(0, 0) > -1.0) {
      // y_angle  = acos(r00)
      // x0_angle = atan2(r10,-r20)
      // x1_angle = atan2(r01,r02)
      double y = acos(_R(0, 0));
      double x0 = atan2(_R(1, 0), -_R(2, 0));
      double x1 = atan2(_R(0, 1), _R(0, 2));
      // return EA_UNIQUE;
      return Vector3d(x0, y, x1);
    } else {
      // Not a unique solution:  x1_angle - x0_angle = atan2(-r12,r11)
      double y = pi();
      double x0 = -atan2(-_R(1, 2), _R(1, 1));
      double x1 = 0.0;
      // return EA_NOT_UNIQUE_DIF;
      return Vector3d(x0, y, x1);
    }
  } else {
    // Not a unique solution:  x1_angle + x0_angle = atan2(-r12,r11)
    double y = 0.0;
    double x0 = -atan2(-_R(1, 2), _R(1, 1));
    double x1 = 0.0;
    // return EA_NOT_UNIQUE_SUM;
    return Vector3d(x0, y, x1);
  }
}

Vector3d matrixToEulerXYZ(const Matrix3d& _R)
{
  // +-           -+   +-                                        -+
  // | r00 r01 r02 |   |  cy*cz           -cy*sz            sy    |
  // | r10 r11 r12 | = |  cz*sx*sy+cx*sz   cx*cz-sx*sy*sz  -cy*sx |
  // | r20 r21 r22 |   | -cx*cz*sy+sx*sz   cz*sx+cx*sy*sz   cx*cy |
  // +-           -+   +-                                        -+

  double x, y, z;

  if (_R(0, 2) > (1.0 - DART_EPSILON)) {
    z = atan2(_R(1, 0), _R(1, 1));
    y = half_pi();
    x = 0.0;
    return Vector3d(x, y, z);
  }

  if (_R(0, 2) < -(1.0 - DART_EPSILON)) {
    z = atan2(_R(1, 0), _R(1, 1));
    y = -half_pi();
    x = 0.0;
    return Vector3d(x, y, z);
  }

  z = -atan2(_R(0, 1), _R(0, 0));
  y = asin(_R(0, 2));
  x = -atan2(_R(1, 2), _R(2, 2));

  // order of return is the order of input
  return Vector3d(x, y, z);
}

Vector3d matrixToEulerZYX(const Matrix3d& _R)
{
  double x, y, z;

  if (_R(2, 0) > (1.0 - DART_EPSILON)) {
    x = atan2(_R(0, 1), _R(0, 2));
    y = -half_pi();
    z = 0.0;
    return Vector3d(z, y, x);
  }

  if (_R(2, 0) < -(1.0 - DART_EPSILON)) {
    x = atan2(_R(0, 1), _R(0, 2));
    y = half_pi();
    z = 0.0;
    return Vector3d(z, y, x);
  }

  x = atan2(_R(2, 1), _R(2, 2));
  y = -asin(_R(2, 0));
  z = atan2(_R(1, 0), _R(0, 0));

  // order of return is the order of input
  return Vector3d(z, y, x);
}

Vector3d matrixToEulerXZY(const Matrix3d& _R)
{
  double x, y, z;

  if (_R(0, 1) > (1.0 - DART_EPSILON)) {
    y = atan2(_R(1, 2), _R(1, 0));
    z = -half_pi();
    x = 0.0;
    return Vector3d(x, z, y);
  }

  if (_R(0, 1) < -(1.0 - DART_EPSILON)) {
    y = atan2(_R(1, 2), _R(1, 0));
    z = half_pi();
    x = 0.0;
    return Vector3d(x, z, y);
  }

  y = atan2(_R(0, 2), _R(0, 0));
  z = -asin(_R(0, 1));
  x = atan2(_R(2, 1), _R(1, 1));

  // order of return is the order of input
  return Vector3d(x, z, y);
}

Vector3d matrixToEulerYZX(const Matrix3d& _R)
{
  double x, y, z;

  if (_R(1, 0) > (1.0 - DART_EPSILON)) {
    x = -atan2(_R(0, 2), _R(0, 1));
    z = half_pi();
    y = 0.0;
    return Vector3d(y, z, x);
  }

  if (_R(1, 0) < -(1.0 - DART_EPSILON)) {
    x = -atan2(_R(0, 2), _R(0, 1));
    z = -half_pi();
    y = 0.0;
    return Vector3d(y, z, x);
  }

  x = -atan2(_R(1, 2), _R(1, 1));
  z = asin(_R(1, 0));
  y = -atan2(_R(2, 0), _R(0, 0));

  // order of return is the order of input
  return Vector3d(y, z, x);
}

Vector3d matrixToEulerZXY(const Matrix3d& _R)
{
  double x, y, z;

  if (_R(2, 1) > (1.0 - DART_EPSILON)) {
    y = atan2(_R(0, 2), _R(0, 0));
    x = half_pi();
    z = 0.0;
    return Vector3d(z, x, y);
  }

  if (_R(2, 1) < -(1.0 - DART_EPSILON)) {
    y = atan2(_R(0, 2), _R(0, 0));
    x = -half_pi();
    z = 0.0;
    return Vector3d(z, x, y);
  }

  y = -atan2(_R(2, 0), _R(2, 2));
  x = asin(_R(2, 1));
  z = -atan2(_R(0, 1), _R(1, 1));

  // order of return is the order of input
  return Vector3d(z, x, y);
}

Vector3d matrixToEulerYXZ(const Matrix3d& _R)
{
  double x, y, z;

  if (_R(1, 2) > (1.0 - DART_EPSILON)) {
    z = -atan2(_R(0, 1), _R(0, 0));
    x = -half_pi();
    y = 0.0;
    return Vector3d(y, x, z);
  }

  if (_R(1, 2) < -(1.0 - DART_EPSILON)) {
    z = -atan2(_R(0, 1), _R(0, 0));
    x = half_pi();
    y = 0.0;
    return Vector3d(y, x, z);
  }

  z = atan2(_R(1, 0), _R(1, 1));
  x = -asin(_R(1, 2));
  y = atan2(_R(0, 2), _R(2, 2));

  // order of return is the order of input
  return Vector3d(y, x, z);
}

// get the derivative of rotation matrix wrt el no.
Matrix3d quatDeriv(const Quaterniond& _q, int _el)
{
  Matrix3d mat = Matrix3d::Zero();

  switch (_el) {
    case 0: // wrt w
      mat(0, 0) = _q.w();
      mat(1, 1) = _q.w();
      mat(2, 2) = _q.w();
      mat(0, 1) = -_q.z();
      mat(1, 0) = _q.z();
      mat(0, 2) = _q.y();
      mat(2, 0) = -_q.y();
      mat(1, 2) = -_q.x();
      mat(2, 1) = _q.x();
      break;
    case 1: // wrt x
      mat(0, 0) = _q.x();
      mat(1, 1) = -_q.x();
      mat(2, 2) = -_q.x();
      mat(0, 1) = _q.y();
      mat(1, 0) = _q.y();
      mat(0, 2) = _q.z();
      mat(2, 0) = _q.z();
      mat(1, 2) = -_q.w();
      mat(2, 1) = _q.w();
      break;
    case 2: // wrt y
      mat(0, 0) = -_q.y();
      mat(1, 1) = _q.y();
      mat(2, 2) = -_q.y();
      mat(0, 1) = _q.x();
      mat(1, 0) = _q.x();
      mat(0, 2) = _q.w();
      mat(2, 0) = -_q.w();
      mat(1, 2) = _q.z();
      mat(2, 1) = _q.z();
      break;
    case 3: // wrt z
      mat(0, 0) = -_q.z();
      mat(1, 1) = -_q.z();
      mat(2, 2) = _q.z();
      mat(0, 1) = -_q.w();
      mat(1, 0) = _q.w();
      mat(0, 2) = _q.x();
      mat(2, 0) = _q.x();
      mat(1, 2) = _q.y();
      mat(2, 1) = _q.y();
      break;
    default:
      break;
  }

  return 2 * mat;
}

Matrix3d quatSecondDeriv(const Quaterniond& /*_q*/, int _el1, int _el2)
{
  Matrix3d mat = Matrix3d::Zero();

  if (_el1 == _el2) { // wrt same dof
    switch (_el1) {
      case 0: // wrt w
        mat(0, 0) = 1;
        mat(1, 1) = 1;
        mat(2, 2) = 1;
        break;
      case 1: // wrt x
        mat(0, 0) = 1;
        mat(1, 1) = -1;
        mat(2, 2) = -1;
        break;
      case 2: // wrt y
        mat(0, 0) = -1;
        mat(1, 1) = 1;
        mat(2, 2) = -1;
        break;
      case 3: // wrt z
        mat(0, 0) = -1;
        mat(1, 1) = -1;
        mat(2, 2) = 1;
        break;
    }
  } else { // wrt different dofs
    // arrange in increasing order
    if (_el1 > _el2) {
      int temp = _el2;
      _el2 = _el1;
      _el1 = temp;
    }

    switch (_el1) {
      case 0: // wrt w
        switch (_el2) {
          case 1: // wrt x
            mat(1, 2) = -1;
            mat(2, 1) = 1;
            break;
          case 2: // wrt y
            mat(0, 2) = 1;
            mat(2, 0) = -1;
            break;
          case 3: // wrt z
            mat(0, 1) = -1;
            mat(1, 0) = 1;
            break;
        }
        break;
      case 1: // wrt x
        switch (_el2) {
          case 2: // wrt y
            mat(0, 1) = 1;
            mat(1, 0) = 1;
            break;
          case 3: // wrt z
            mat(0, 2) = 1;
            mat(2, 0) = 1;
            break;
        }
        break;
      case 2: // wrt y
        switch (_el2) {
          case 3: // wrt z
            mat(1, 2) = 1;
            mat(2, 1) = 1;
            break;
        }
        break;
    }
  }

  return 2 * mat;
}

// ----------- expmap computations -------------

#define EPSILON_EXPMAP_THETA 1.0e-3

Matrix3d expMapRot(const Vector3d& _q)
{
  double theta = _q.norm();

  Matrix3d R = Matrix3d::Zero();
  Matrix3d qss = skew(_q);
  Matrix3d qss2 = qss * qss;

  if (theta < EPSILON_EXPMAP_THETA)
    R = Matrix3d::Identity() + qss + 0.5 * qss2;
  else
    R = Matrix3d::Identity() + (sin(theta) / theta) * qss
        + ((1 - cos(theta)) / (theta * theta)) * qss2;

  return R;
}

Matrix3d expMapJac(const Vector3d& _q)
{
  double theta = _q.norm();

  Matrix3d J = Matrix3d::Zero();
  Matrix3d qss = skew(_q);
  Matrix3d qss2 = qss * qss;

  if (theta < EPSILON_EXPMAP_THETA)
    J = Matrix3d::Identity() + 0.5 * qss + (1.0 / 6.0) * qss2;
  else
    J = Matrix3d::Identity() + ((1 - cos(theta)) / (theta * theta)) * qss
        + ((theta - sin(theta)) / (theta * theta * theta)) * qss2;

  return J;
}

Matrix3d expMapJacDot(const Vector3d& _q, const Vector3d& _qdot)
{
  double theta = _q.norm();

  Matrix3d Jdot = Matrix3d::Zero();
  Matrix3d qss = skew(_q);
  Matrix3d qss2 = qss * qss;
  Matrix3d qdss = skew(_qdot);
  double ttdot = _q.dot(_qdot); // theta*thetaDot
  double st = sin(theta);
  double ct = cos(theta);
  double t2 = theta * theta;
  double t3 = t2 * theta;
  double t4 = t3 * theta;
  double t5 = t4 * theta;

  if (theta < EPSILON_EXPMAP_THETA) {
    Jdot = 0.5 * qdss + (1.0 / 6.0) * (qss * qdss + qdss * qss);
    Jdot += (-1.0 / 12) * ttdot * qss + (-1.0 / 60) * ttdot * qss2;
  } else {
    Jdot = ((1 - ct) / t2) * qdss
           + ((theta - st) / t3) * (qss * qdss + qdss * qss);
    Jdot += ((theta * st + 2 * ct - 2) / t4) * ttdot * qss
            + ((3 * st - theta * ct - 2 * theta) / t5) * ttdot * qss2;
  }

  return Jdot;
}

Matrix3d expMapJacDeriv(const Vector3d& _q, int _qi)
{
  assert(_qi >= 0 && _qi <= 2);

  Vector3d qdot = Vector3d::Zero();
  qdot[_qi] = 1.0;
  return expMapJacDot(_q, qdot);
}

// Vec3 AdInvTLinear(const SE3& T, const Vec3& v)
// {
//     return Vec3(T(0,0)*v[0] + T(1,0)*v[1] + T(2,0)*v[2],
//                 T(0,1)*v[0] + T(1,1)*v[1] + T(2,1)*v[2],
//                 T(0,2)*v[0] + T(1,2)*v[1] + T(2,2)*v[2]);
// }

// Vec3 ad_Vec3_se3(const Vec3& s1, const se3& s2)
// {
//     Vec3 ret;

//     ret << s2[2]*s1[1] - s2[1]*s1[2],
//            s2[0]*s1[2] - s2[2]*s1[0],
//            s2[1]*s1[0] - s2[0]*s1[1];

//     return ret;
// }

Vector3d logMap(const Matrix3d& _R)
{
  //--------------------------------------------------------------------------
  // T = (R, p) = exp([w, v]), t = ||w||
  // v = beta*p + gamma*w + 1 / 2*cross(p, w)
  //    , beta = t*(1 + cos(t)) / (2*sin(t)), gamma = <w, p>*(1 - beta) / t^2
  //--------------------------------------------------------------------------
  //  double theta =
  //      std::acos(
  //        std::max(
  //          std::min(0.5 * (_R(0, 0) + _R(1, 1) + _R(2, 2) - 1.0), 1.0),
  //          -1.0));

  //  if (theta > pi() - DART_EPSILON) {
  //    double delta = 0.5 + 0.125*(pi() - theta)*(pi()
  //    - theta);

  //    return Vector3d(
  //          _R(2, 1) > _R(1, 2) ? theta*sqrt(1.0 + (_R(0, 0) - 1.0)*delta) :
  //                             -theta*sqrt(1.0 + (_R(0, 0) - 1.0)*delta),
  //          _R(0, 2) > _R(2, 0) ? theta*sqrt(1.0 + (_R(1, 1) - 1.0)*delta) :
  //                             -theta*sqrt(1.0 + (_R(1, 1) - 1.0)*delta),
  //          _R(1, 0) > _R(0, 1) ? theta*sqrt(1.0 + (_R(2, 2) - 1.0)*delta) :
  //                             -theta*sqrt(1.0 + (_R(2, 2) - 1.0)*delta));
  //  } else {
  //    double alpha = 0.0;

  //    if (theta > DART_EPSILON)
  //      alpha = 0.5*theta / sin(theta);
  //    else
  //      alpha = 0.5 + one_div_12()*theta*theta;

  //    return Vector3d(alpha*(_R(2, 1) - _R(1, 2)),
  //                           alpha*(_R(0, 2) - _R(2, 0)),
  //                           alpha*(_R(1, 0) - _R(0, 1)));
  //  }

  AngleAxisd aa(_R);
  return aa.angle() * aa.axis();
}

Vector6d logMap(const Isometry3d& _T)
{
  //--------------------------------------------------------------------------
  // T = (R, p) = exp([w, v]), t = ||w||
  // v = beta*p + gamma*w + 1 / 2*cross(p, w)
  //    , beta = t*(1 + cos(t)) / (2*sin(t)), gamma = <w, p>*(1 - beta) / t^2
  //--------------------------------------------------------------------------
  double theta = std::acos(std::max(
      std::min(0.5 * (_T(0, 0) + _T(1, 1) + _T(2, 2) - 1.0), 1.0), -1.0));
  double beta;
  double gamma;
  Vector6d ret;

  if (theta > pi() - DART_EPSILON) {
    const double c1 = 0.10132118364234; // 1 / pi^2
    const double c2 = 0.01507440267955; // 1 / 4 / pi - 2 / pi^3
    const double c3 = 0.00546765085347; // 3 / pi^4 - 1 / 4 / pi^2

    double phi = pi() - theta;
    double delta = 0.5 + 0.125 * phi * phi;

    double w[]
        = {_T(2, 1) > _T(1, 2) ? theta * sqrt(1.0 + (_T(0, 0) - 1.0) * delta)
                               : -theta * sqrt(1.0 + (_T(0, 0) - 1.0) * delta),
           _T(0, 2) > _T(2, 0) ? theta * sqrt(1.0 + (_T(1, 1) - 1.0) * delta)
                               : -theta * sqrt(1.0 + (_T(1, 1) - 1.0) * delta),
           _T(1, 0) > _T(0, 1) ? theta * sqrt(1.0 + (_T(2, 2) - 1.0) * delta)
                               : -theta * sqrt(1.0 + (_T(2, 2) - 1.0) * delta)};

    beta = 0.25 * theta * (pi() - theta);
    gamma = (w[0] * _T(0, 3) + w[1] * _T(1, 3) + w[2] * _T(2, 3))
            * (c1 - c2 * phi + c3 * phi * phi);

    ret << w[0], w[1], w[2],
        beta * _T(0, 3) - 0.5 * (w[1] * _T(2, 3) - w[2] * _T(1, 3))
            + gamma * w[0],
        beta * _T(1, 3) - 0.5 * (w[2] * _T(0, 3) - w[0] * _T(2, 3))
            + gamma * w[1],
        beta * _T(2, 3) - 0.5 * (w[0] * _T(1, 3) - w[1] * _T(0, 3))
            + gamma * w[2];
  } else {
    double alpha;
    if (theta > DART_EPSILON) {
      alpha = 0.5 * theta / sin(theta);
      beta = (1.0 + cos(theta)) * alpha;
      gamma = (1.0 - beta) / theta / theta;
    } else {
      alpha = 0.5 + 1.0 / 12.0 * theta * theta;
      beta = 1.0 - 1.0 / 12.0 * theta * theta;
      gamma = 1.0 / 12.0 + 1.0 / 720.0 * theta * theta;
    }

    double w[]
        = {alpha * (_T(2, 1) - _T(1, 2)),
           alpha * (_T(0, 2) - _T(2, 0)),
           alpha * (_T(1, 0) - _T(0, 1))};
    gamma *= w[0] * _T(0, 3) + w[1] * _T(1, 3) + w[2] * _T(2, 3);

    ret << w[0], w[1], w[2],
        beta * _T(0, 3) + 0.5 * (w[2] * _T(1, 3) - w[1] * _T(2, 3))
            + gamma * w[0],
        beta * _T(1, 3) + 0.5 * (w[0] * _T(2, 3) - w[2] * _T(0, 3))
            + gamma * w[1],
        beta * _T(2, 3) + 0.5 * (w[1] * _T(0, 3) - w[0] * _T(1, 3))
            + gamma * w[2];
  }

  return ret;
}

// res = T * s * Inv(T)
Vector6d AdT(const Isometry3d& _T, const Vector6d& _V)
{
  //--------------------------------------------------------------------------
  // w' = R*w
  // v' = p x R*w + R*v
  //--------------------------------------------------------------------------
  Vector6d res;
  res.head<3>().noalias() = _T.linear() * _V.head<3>();
  res.tail<3>().noalias()
      = _T.linear() * _V.tail<3>() + _T.translation().cross(res.head<3>());
  return res;
}

//==============================================================================
Matrix6d getAdTMatrix(const Isometry3d& T)
{
  Matrix6d AdT;

  AdT.topLeftCorner<3, 3>() = T.linear();
  AdT.topRightCorner<3, 3>().setZero();
  AdT.bottomLeftCorner<3, 3>() = skew(T.translation()) * T.linear();
  AdT.bottomRightCorner<3, 3>() = T.linear();

  return AdT;
}

Vector6d AdR(const Isometry3d& _T, const Vector6d& _V)
{
  //--------------------------------------------------------------------------
  // w' = R*w
  // v' = R*v
  //--------------------------------------------------------------------------
  Vector6d res;
  res.head<3>().noalias() = _T.linear() * _V.head<3>();
  res.tail<3>().noalias() = _T.linear() * _V.tail<3>();
  return res;
}

Vector6d AdTAngular(const Isometry3d& _T, const Vector3d& _w)
{
  //--------------------------------------------------------------------------
  // w' = R*w
  // v' = p x R*w
  //--------------------------------------------------------------------------
  Vector6d res;
  res.head<3>().noalias() = _T.linear() * _w;
  res.tail<3>() = _T.translation().cross(res.head<3>());
  return res;
}

Vector6d AdTLinear(const Isometry3d& _T, const Vector3d& _v)
{
  //--------------------------------------------------------------------------
  // w' = 0
  // v' = R*v
  //--------------------------------------------------------------------------
  Vector6d res = Vector6d::Zero();
  res.tail<3>().noalias() = _T.linear() * _v;
  return res;
}

// se3 AdP(const Vec3& p, const se3& s)
// {
//  //--------------------------------------------------------------------------
//  // w' = w
//  // v' = p x w + v
//  //--------------------------------------------------------------------------
//  se3 ret;
//  ret << s[0],
//      s[1],
//      s[2],
//      p[1]*s[2] - p[2]*s[1] + s[3],
//      p[2]*s[0] - p[0]*s[2] + s[4],
//      p[0]*s[1] - p[1]*s[0] + s[5];

//  return ret;
// }

// Jacobian AdRJac(const SE3& T, const Jacobian& J)
// {
//     Jacobian AdTJ(6,J.cols());

//     for (int i = 0; i < J.cols(); ++i)
//     {
//         AdTJ.col(i) = AdR(T, J.col(i));
//     }

//     return AdTJ;
// }

// re = Inv(T)*s*T
Vector6d AdInvT(const Isometry3d& _T, const Vector6d& _V)
{
  Vector6d res;
  res.head<3>().noalias() = _T.linear().transpose() * _V.head<3>();
  res.tail<3>().noalias()
      = _T.linear().transpose()
        * (_V.tail<3>() + _V.head<3>().cross(_T.translation()));
  return res;
}

// se3 AdInvR(const SE3& T, const se3& s)
// {
//     se3 ret;

//     ret << T(0,0)*s[0] + T(1,0)*s[1] + T(2,0)*s[2],
//                 T(0,1)*s[0] + T(1,1)*s[1] + T(2,1)*s[2],
//                 T(0,2)*s[0] + T(1,2)*s[1] + T(2,2)*s[2],
//                 T(0,0)*s[3] + T(1,0)*s[4] + T(2,0)*s[5],
//                 T(0,1)*s[3] + T(1,1)*s[4] + T(2,1)*s[5],
//                 T(0,2)*s[3] + T(1,2)*s[4] + T(2,2)*s[5];

//     return ret;
// }

Vector6d AdInvRLinear(const Isometry3d& _T, const Vector3d& _v)
{
  Vector6d res = Vector6d::Zero();
  res.tail<3>().noalias() = _T.linear().transpose() * _v;
  return res;
}

Vector6d ad(const Vector6d& _X, const Vector6d& _Y)
{
  //--------------------------------------------------------------------------
  // ad(s1, s2) = | [w1]    0 | | w2 |
  //              | [v1] [w1] | | v2 |
  //
  //            = |          [w1]w2 |
  //              | [v1]w2 + [w1]v2 |
  //--------------------------------------------------------------------------
  Vector6d res;
  res.head<3>() = _X.head<3>().cross(_Y.head<3>());
  res.tail<3>()
      = _X.head<3>().cross(_Y.tail<3>()) + _X.tail<3>().cross(_Y.head<3>());
  return res;
}

Vector6d dAdT(const Isometry3d& _T, const Vector6d& _F)
{
  Vector6d res;
  res.head<3>().noalias()
      = _T.linear().transpose()
        * (_F.head<3>() + _F.tail<3>().cross(_T.translation()));
  res.tail<3>().noalias() = _T.linear().transpose() * _F.tail<3>();
  return res;
}

// dse3 dAdTLinear(const SE3& T, const Vec3& v)
// {
//     dse3 ret;
//     double tmp[3] = { - T(1,3)*v[2] + T(2,3)*v[1],
//                       - T(2,3)*v[0] + T(0,3)*v[2],
//                       - T(0,3)*v[1] + T(1,3)*v[0] };
//     ret << T(0,0)*tmp[0] + T(1,0)*tmp[1] + T(2,0)*tmp[2],
//                 T(0,1)*tmp[0] + T(1,1)*tmp[1] + T(2,1)*tmp[2],
//                 T(0,2)*tmp[0] + T(1,2)*tmp[1] + T(2,2)*tmp[2],
//                 T(0,0)*v[0] + T(1,0)*v[1] + T(2,0)*v[2],
//                 T(0,1)*v[0] + T(1,1)*v[1] + T(2,1)*v[2],
//                 T(0,2)*v[0] + T(1,2)*v[1] + T(2,2)*v[2];

//     return ret;
// }

Vector6d dAdInvT(const Isometry3d& _T, const Vector6d& _F)
{
  Vector6d res;
  res.tail<3>().noalias() = _T.linear() * _F.tail<3>();
  res.head<3>().noalias() = _T.linear() * _F.head<3>();
  res.head<3>() += _T.translation().cross(res.tail<3>());
  return res;
}

Vector6d dAdInvR(const Isometry3d& _T, const Vector6d& _F)
{
  Vector6d res;
  res.head<3>().noalias() = _T.linear() * _F.head<3>();
  res.tail<3>().noalias() = _T.linear() * _F.tail<3>();
  return res;
}

// dse3 dAdInvPLinear(const Vec3& p, const Vec3& f)
// {
//     dse3 ret;

//     ret << p[1]*f[2] - p[2]*f[1],
//                 p[2]*f[0] - p[0]*f[2],
//                 p[0]*f[1] - p[1]*f[0],
//                 f[0],
//                 f[1],
//                 f[2];

//     return ret;
// }

// Reference:
// http://www.geometrictools.com/LibMathematics/Algebra/Wm5Matrix3.inl
Matrix3d eulerXYXToMatrix(const Vector3d& _angle)
{
  // +-           -+   +-                                                -+
  // | r00 r01 r02 |   |  cy      sy*sx1               sy*cx1             |
  // | r10 r11 r12 | = |  sy*sx0  cx0*cx1-cy*sx0*sx1  -cy*cx1*sx0-cx0*sx1 |
  // | r20 r21 r22 |   | -sy*cx0  cx1*sx0+cy*cx0*sx1   cy*cx0*cx1-sx0*sx1 |
  // +-           -+   +-                                                -+

  Matrix3d ret;

  double cx0 = cos(_angle(0));
  double sx0 = sin(_angle(0));
  double cy = cos(_angle(1));
  double sy = sin(_angle(1));
  double cx1 = cos(_angle(2));
  double sx1 = sin(_angle(2));

  ret(0, 0) = cy;
  ret(1, 0) = sy * sx0;
  ret(2, 0) = -sy * cx0;

  ret(0, 1) = sy * sx1;
  ret(1, 1) = cx0 * cx1 - cy * sx0 * sx1;
  ret(2, 1) = cx1 * sx0 + cy * cx0 * sx1;

  ret(0, 2) = sy * cx1;
  ret(1, 2) = -cy * cx1 * sx0 - cx0 * sx1;
  ret(2, 2) = cy * cx0 * cx1 - sx0 * sx1;

  return ret;
}

Matrix3d eulerXYZToMatrix(const Vector3d& _angle)
{
  // +-           -+   +-                                        -+
  // | r00 r01 r02 |   |  cy*cz           -cy*sz            sy    |
  // | r10 r11 r12 | = |  cz*sx*sy+cx*sz   cx*cz-sx*sy*sz  -cy*sx |
  // | r20 r21 r22 |   | -cx*cz*sy+sx*sz   cz*sx+cx*sy*sz   cx*cy |
  // +-           -+   +-                                        -+

  Matrix3d ret;

  double cx = cos(_angle[0]);
  double sx = sin(_angle[0]);
  double cy = cos(_angle[1]);
  double sy = sin(_angle[1]);
  double cz = cos(_angle[2]);
  double sz = sin(_angle[2]);

  ret(0, 0) = cy * cz;
  ret(1, 0) = cx * sz + cz * sx * sy;
  ret(2, 0) = sx * sz - cx * cz * sy;

  ret(0, 1) = -cy * sz;
  ret(1, 1) = cx * cz - sx * sy * sz;
  ret(2, 1) = cz * sx + cx * sy * sz;

  ret(0, 2) = sy;
  ret(1, 2) = -cy * sx;
  ret(2, 2) = cx * cy;

  return ret;
}

Matrix3d eulerXZXToMatrix(const Vector3d& _angle)
{
  // +-           -+   +-                                                -+
  // | r00 r01 r02 |   | cz      -sz*cx1               sz*sx1             |
  // | r10 r11 r12 | = | sz*cx0   cz*cx0*cx1-sx0*sx1  -cx1*sx0-cz*cx0*sx1 |
  // | r20 r21 r22 |   | sz*sx0   cz*cx1*sx0+cx0*sx1   cx0*cx1-cz*sx0*sx1 |
  // +-           -+   +-                                                -+

  Matrix3d ret;

  double cx0 = cos(_angle(0));
  double sx0 = sin(_angle(0));
  double cz = cos(_angle(1));
  double sz = sin(_angle(1));
  double cx1 = cos(_angle(2));
  double sx1 = sin(_angle(2));

  ret(0, 0) = cz;
  ret(1, 0) = sz * cx0;
  ret(2, 0) = sz * sx0;

  ret(0, 1) = -sz * cx1;
  ret(1, 1) = cz * cx0 * cx1 - sx0 * sx1;
  ret(2, 1) = cz * cx1 * sx0 + cx0 * sx1;

  ret(0, 2) = sz * sx1;
  ret(1, 2) = -cx1 * sx0 - cz * cx0 * sx1;
  ret(2, 2) = cx0 * cx1 - cz * sx0 * sx1;

  return ret;
}

Matrix3d eulerXZYToMatrix(const Vector3d& _angle)
{
  // +-           -+   +-                                        -+
  // | r00 r01 r02 |   |  cy*cz           -sz      cz*sy          |
  // | r10 r11 r12 | = |  sx*sy+cx*cy*sz   cx*cz  -cy*sx+cx*sy*sz |
  // | r20 r21 r22 |   | -cx*sy+cy*sx*sz   cz*sx   cx*cy+sx*sy*sz |
  // +-           -+   +-                                        -+

  Matrix3d ret;

  double cx = cos(_angle(0));
  double sx = sin(_angle(0));
  double cz = cos(_angle(1));
  double sz = sin(_angle(1));
  double cy = cos(_angle(2));
  double sy = sin(_angle(2));

  ret(0, 0) = cy * cz;
  ret(1, 0) = sx * sy + cx * cy * sz;
  ret(2, 0) = -cx * sy + cy * sx * sz;

  ret(0, 1) = -sz;
  ret(1, 1) = cx * cz;
  ret(2, 1) = cz * sx;

  ret(0, 2) = cz * sy;
  ret(1, 2) = -cy * sx + cx * sy * sz;
  ret(2, 2) = cx * cy + sx * sy * sz;

  return ret;
}

Matrix3d eulerYXYToMatrix(const Vector3d& _angle)
{
  // +-           -+   +-                                                -+
  // | r00 r01 r02 |   |  cy0*cy1-cx*sy0*sy1  sx*sy0   cx*cy1*sy0+cy0*sy1 |
  // | r10 r11 r12 | = |  sx*sy1              cx      -sx*cy1             |
  // | r20 r21 r22 |   | -cy1*sy0-cx*cy0*sy1  sx*cy0   cx*cy0*cy1-sy0*sy1 |
  // +-           -+   +-                                                -+

  Matrix3d ret;

  double cy0 = cos(_angle(0));
  double sy0 = sin(_angle(0));
  double cx = cos(_angle(1));
  double sx = sin(_angle(1));
  double cy1 = cos(_angle(2));
  double sy1 = sin(_angle(2));

  ret(0, 0) = cy0 * cy1 - cx * sy0 * sy1;
  ret(1, 0) = sx * sy1;
  ret(2, 0) = -cy1 * sy0 - cx * cy0 * sy1;

  ret(0, 1) = sx * sy0;
  ret(1, 1) = cx;
  ret(2, 1) = sx * cy0;

  ret(0, 2) = cx * cy1 * sy0 + cy0 * sy1;
  ret(1, 2) = -sx * cy1;
  ret(2, 2) = cx * cy0 * cy1 - sy0 * sy1;

  return ret;
}

Matrix3d eulerYXZToMatrix(const Vector3d& _angle)
{
  // +-           -+   +-                                       -+
  // | r00 r01 r02 |   |  cy*cz+sx*sy*sz  cz*sx*sy-cy*sz   cx*sy |
  // | r10 r11 r12 | = |  cx*sz           cx*cz           -sx    |
  // | r20 r21 r22 |   | -cz*sy+cy*sx*sz  cy*cz*sx+sy*sz   cx*cy |
  // +-           -+   +-                                       -+

  Matrix3d ret;

  double cy = cos(_angle(0));
  double sy = sin(_angle(0));
  double cx = cos(_angle(1));
  double sx = sin(_angle(1));
  double cz = cos(_angle(2));
  double sz = sin(_angle(2));

  ret(0, 0) = cy * cz + sx * sy * sz;
  ret(0, 1) = cz * sx * sy - cy * sz;
  ret(0, 2) = cx * sy;
  ret(1, 0) = cx * sz;
  ret(1, 1) = cx * cz;
  ret(1, 2) = -sx;
  ret(2, 0) = -cz * sy + cy * sx * sz;
  ret(2, 1) = cy * cz * sx + sy * sz;
  ret(2, 2) = cx * cy;

  return ret;
}

Matrix3d eulerYZXToMatrix(const Vector3d& _angle)
{
  // +-           -+   +-                                       -+
  // | r00 r01 r02 |   |  cy*cz  sx*sy-cx*cy*sz   cx*sy+cy*sx*sz |
  // | r10 r11 r12 | = |  sz     cx*cz           -cz*sx          |
  // | r20 r21 r22 |   | -cz*sy  cy*sx+cx*sy*sz   cx*cy-sx*sy*sz |
  // +-           -+   +-                                       -+

  Matrix3d ret;

  double cy = cos(_angle(0));
  double sy = sin(_angle(0));
  double cz = cos(_angle(1));
  double sz = sin(_angle(1));
  double cx = cos(_angle(2));
  double sx = sin(_angle(2));

  ret(0, 0) = cy * cz;
  ret(0, 1) = sx * sy - cx * cy * sz;
  ret(0, 2) = cx * sy + cy * sx * sz;
  ret(1, 0) = sz;
  ret(1, 1) = cx * cz;
  ret(1, 2) = -cz * sx;
  ret(2, 0) = -cz * sy;
  ret(2, 1) = cy * sx + cx * sy * sz;
  ret(2, 2) = cx * cy - sx * sy * sz;

  return ret;
}

Matrix3d eulerYZYToMatrix(const Vector3d& _angle)
{
  // +-           -+   +-                                                -+
  // | r00 r01 r02 |   |  cz*cy0*cy1-sy0*sy1  -sz*cy0  cy1*sy0+cz*cy0*sy1 |
  // | r10 r11 r12 | = |  sz*cy1               cz      sz*sy1             |
  // | r20 r21 r22 |   | -cz*cy1*sy0-cy0*sy1   sz*sy0  cy0*cy1-cz*sy0*sy1 |
  // +-           -+   +-                                                -+

  Matrix3d ret;

  double cy0 = cos(_angle(0));
  double sy0 = sin(_angle(0));
  double cz = cos(_angle(1));
  double sz = sin(_angle(1));
  double cy1 = cos(_angle(2));
  double sy1 = sin(_angle(2));

  ret(0, 0) = cz * cy0 * cy1 - sy0 * sy1;
  ret(1, 0) = sz * cy1;
  ret(2, 0) = -cz * cy1 * sy0 - cy0 * sy1;

  ret(0, 1) = -sz * cy0;
  ret(1, 1) = cz;
  ret(2, 1) = sz * sy0;

  ret(0, 2) = cy1 * sy0 + cz * cy0 * sy1;
  ret(1, 2) = sz * sy1;
  ret(2, 2) = cy0 * cy1 - cz * sy0 * sy1;

  return ret;
}

Matrix3d eulerZXYToMatrix(const Vector3d& _angle)
{
  // +-           -+   +-                                        -+
  // | r00 r01 r02 |   |  cy*cz-sx*sy*sz  -cx*sz   cz*sy+cy*sx*sz |
  // | r10 r11 r12 | = |  cz*sx*sy+cy*sz   cx*cz  -cy*cz*sx+sy*sz |
  // | r20 r21 r22 |   | -cx*sy            sx      cx*cy          |
  // +-           -+   +-                                        -+

  Matrix3d ret;

  double cz = cos(_angle(0));
  double sz = sin(_angle(0));
  double cx = cos(_angle(1));
  double sx = sin(_angle(1));
  double cy = cos(_angle(2));
  double sy = sin(_angle(2));

  ret(0, 0) = cy * cz - sx * sy * sz;
  ret(1, 0) = cz * sx * sy + cy * sz;
  ret(2, 0) = -cx * sy;

  ret(0, 1) = -cx * sz;
  ret(1, 1) = cx * cz;
  ret(2, 1) = sx;

  ret(0, 2) = cz * sy + cy * sx * sz;
  ret(1, 2) = -cy * cz * sx + sy * sz;
  ret(2, 2) = cx * cy;

  return ret;
}

Matrix3d eulerZYXToMatrix(const Vector3d& _angle)
{
  // +-           -+   +-                                      -+
  // | r00 r01 r02 |   |  cy*cz  cz*sx*sy-cx*sz  cx*cz*sy+sx*sz |
  // | r10 r11 r12 | = |  cy*sz  cx*cz+sx*sy*sz -cz*sx+cx*sy*sz |
  // | r20 r21 r22 |   | -sy     cy*sx           cx*cy          |
  // +-           -+   +-                                      -+

  Matrix3d ret;

  double cz = cos(_angle[0]);
  double sz = sin(_angle[0]);
  double cy = cos(_angle[1]);
  double sy = sin(_angle[1]);
  double cx = cos(_angle[2]);
  double sx = sin(_angle[2]);

  ret(0, 0) = cz * cy;
  ret(1, 0) = sz * cy;
  ret(2, 0) = -sy;

  ret(0, 1) = cz * sy * sx - sz * cx;
  ret(1, 1) = sz * sy * sx + cz * cx;
  ret(2, 1) = cy * sx;

  ret(0, 2) = cz * sy * cx + sz * sx;
  ret(1, 2) = sz * sy * cx - cz * sx;
  ret(2, 2) = cy * cx;

  return ret;
}

Matrix3d eulerZXZToMatrix(const Vector3d& _angle)
{
  // +-           -+   +-                                                -+
  // | r00 r01 r02 |   | cz0*cz1-cx*sz0*sz1  -cx*cz1*sz0-cz0*sz1   sx*sz0 |
  // | r10 r11 r12 | = | cz1*sz0+cx*cz0*sz1   cx*cz0*cz1-sz0*sz1  -sz*cz0 |
  // | r20 r21 r22 |   | sx*sz1               sx*cz1               cx     |
  // +-           -+   +-                                                -+

  Matrix3d ret;

  double cz0 = cos(_angle(0));
  double sz0 = sin(_angle(0));
  double cx = cos(_angle(1));
  double sx = sin(_angle(1));
  double cz1 = cos(_angle(2));
  double sz1 = sin(_angle(2));

  ret(0, 0) = cz0 * cz1 - cx * sz0 * sz1;
  ret(1, 0) = cz1 * sz0 + cx * cz0 * sz1;
  ret(2, 0) = sx * sz1;

  ret(0, 1) = -cx * cz1 * sz0 - cz0 * sz1;
  ret(1, 1) = cx * cz0 * cz1 - sz0 * sz1;
  ret(2, 1) = sx * cz1;

  ret(0, 2) = sx * sz0;
  ret(1, 2) = -sx * cz0;
  ret(2, 2) = cx;

  return ret;
}

Matrix3d eulerZYZToMatrix(const Vector3d& _angle)
{
  // +-           -+   +-                                                -+
  // | r00 r01 r02 |   |  cy*cz0*cz1-sz0*sz1  -cz1*sz0-cy*cz0*sz1  sy*cz0 |
  // | r10 r11 r12 | = |  cy*cz1*sz0+cz0*sz1   cz0*cz1-cy*sz0*sz1  sy*sz0 |
  // | r20 r21 r22 |   | -sy*cz1               sy*sz1              cy     |
  // +-           -+   +-                                                -+

  Matrix3d ret = Matrix3d::Identity();

  double cz0 = cos(_angle[0]);
  double sz0 = sin(_angle[0]);
  double cy = cos(_angle[1]);
  double sy = sin(_angle[1]);
  double cz1 = cos(_angle[2]);
  double sz1 = sin(_angle[2]);

  ret(0, 0) = cz0 * cy * cz1 - sz0 * sz1;
  ret(1, 0) = sz0 * cy * cz1 + cz0 * sz1;
  ret(2, 0) = -sy * cz1;

  ret(0, 1) = -cz0 * cy * sz1 - sz0 * cz1;
  ret(1, 1) = cz0 * cz1 - sz0 * cy * sz1;
  ret(2, 1) = sy * sz1;

  ret(0, 2) = cz0 * sy;
  ret(1, 2) = sz0 * sy;
  ret(2, 2) = cy;

  return ret;
}

// R = Exp(w)
// p = sin(t) / t*v + (t - sin(t)) / t^3*<w, v>*w + (1 - cos(t)) / t^2*(w X v)
// , when S = (w, v), t = |w|
Isometry3d expMap(const Vector6d& _S)
{
  Isometry3d ret = Isometry3d::Identity();
  double s2[] = {_S[0] * _S[0], _S[1] * _S[1], _S[2] * _S[2]};
  double s3[] = {_S[0] * _S[1], _S[1] * _S[2], _S[2] * _S[0]};
  double theta = sqrt(s2[0] + s2[1] + s2[2]);
  double cos_t = cos(theta), alpha, beta, gamma;

  if (theta > DART_EPSILON) {
    double sin_t = sin(theta);
    alpha = sin_t / theta;
    beta = (1.0 - cos_t) / theta / theta;
    gamma = (_S[0] * _S[3] + _S[1] * _S[4] + _S[2] * _S[5]) * (theta - sin_t)
            / theta / theta / theta;
  } else {
    alpha = 1.0 - theta * theta / 6.0;
    beta = 0.5 - theta * theta / 24.0;
    gamma = (_S[0] * _S[3] + _S[1] * _S[4] + _S[2] * _S[5]) / 6.0
            - theta * theta / 120.0;
  }

  ret(0, 0) = beta * s2[0] + cos_t;
  ret(1, 0) = beta * s3[0] + alpha * _S[2];
  ret(2, 0) = beta * s3[2] - alpha * _S[1];

  ret(0, 1) = beta * s3[0] - alpha * _S[2];
  ret(1, 1) = beta * s2[1] + cos_t;
  ret(2, 1) = beta * s3[1] + alpha * _S[0];

  ret(0, 2) = beta * s3[2] + alpha * _S[1];
  ret(1, 2) = beta * s3[1] - alpha * _S[0];
  ret(2, 2) = beta * s2[2] + cos_t;

  ret(0, 3)
      = alpha * _S[3] + beta * (_S[1] * _S[5] - _S[2] * _S[4]) + gamma * _S[0];
  ret(1, 3)
      = alpha * _S[4] + beta * (_S[2] * _S[3] - _S[0] * _S[5]) + gamma * _S[1];
  ret(2, 3)
      = alpha * _S[5] + beta * (_S[0] * _S[4] - _S[1] * _S[3]) + gamma * _S[2];

  return ret;
}

// I + sin(t) / t*[S] + (1 - cos(t)) / t^2*[S]^2, where t = |S|
Isometry3d expAngular(const Vector3d& _s)
{
  Isometry3d ret = Isometry3d::Identity();
  double s2[] = {_s[0] * _s[0], _s[1] * _s[1], _s[2] * _s[2]};
  double s3[] = {_s[0] * _s[1], _s[1] * _s[2], _s[2] * _s[0]};
  double theta = sqrt(s2[0] + s2[1] + s2[2]);
  double cos_t = cos(theta);
  double alpha = 0.0;
  double beta = 0.0;

  if (theta > DART_EPSILON) {
    alpha = sin(theta) / theta;
    beta = (1.0 - cos_t) / theta / theta;
  } else {
    alpha = 1.0 - theta * theta / 6.0;
    beta = 0.5 - theta * theta / 24.0;
  }

  ret(0, 0) = beta * s2[0] + cos_t;
  ret(1, 0) = beta * s3[0] + alpha * _s[2];
  ret(2, 0) = beta * s3[2] - alpha * _s[1];

  ret(0, 1) = beta * s3[0] - alpha * _s[2];
  ret(1, 1) = beta * s2[1] + cos_t;
  ret(2, 1) = beta * s3[1] + alpha * _s[0];

  ret(0, 2) = beta * s3[2] + alpha * _s[1];
  ret(1, 2) = beta * s3[1] - alpha * _s[0];
  ret(2, 2) = beta * s2[2] + cos_t;

  return ret;
}

// SE3 Normalize(const SE3& T)
// {
//    SE3 ret = SE3::Identity();
//    double idet = 1.0 / (T(0,0)*(T(1,1)*T(2,2) - T(2,1)*T(1,2)) +
//                              T(0,1)*(T(2,0)*T(1,2) - T(1,0)*T(2,2)) +
//                              T(0,2)*(T(1,0)*T(2,1) - T(2,0)*T(1,1)));

//    ret(0,0) = 1.0_2*(T(0,0) + idet*(T(1,1)*T(2,2) - T(2,1)*T(1,2)));
//    ret(0,1) = 1.0_2*(T(0,1) + idet*(T(2,0)*T(1,2) - T(1,0)*T(2,2)));
//    ret(0,2) = 1.0_2*(T(0,2) + idet*(T(1,0)*T(2,1) - T(2,0)*T(1,1)));
//    ret(0,3) = T(0,3);

//    ret(1,0) = 1.0_2*(T(1,0) + idet*(T(2,1)*T(0,2) - T(0,1)*T(2,2)));
//    ret(1,1) = 1.0_2*(T(1,1) + idet*(T(0,0)*T(2,2) - T(2,0)*T(0,2)));
//    ret(1,2) = 1.0_2*(T(1,2) + idet*(T(2,0)*T(0,1) - T(0,0)*T(2,1)));
//    ret(1,3) = T(1,3);

//    ret(2,0) = 1.0_2*(T(2,0) + idet*(T(0,1)*T(1,2) - T(1,1)*T(0,2)));
//    ret(2,1) = 1.0_2*(T(2,1) + idet*(T(1,0)*T(0,2) - T(0,0)*T(1,2)));
//    ret(2,2) = 1.0_2*(T(2,2) + idet*(T(0,0)*T(1,1) - T(1,0)*T(0,1)));
//    ret(2,3) = T(2,3);

//    return ret;
// }

// Axis Reparameterize(const Axis& s)
// {
//  double theta = std::sqrt(s[0]*s[0] + s[1]*s[1] + s[2]*s[2]);
//  double eta = theta < LIE_EPS
//               ? 1.0
//               : 1.0 - (double)((int)(theta / M_PI + 1.0) / 2)*M_2PI / theta;

//  return eta*s;
// }

// Axis AdInvTAngular(const SE3& T, const Axis& v)
// {
//    return Axis(T(0,0)*v[0] + T(1,0)*v[1] + T(2,0)*v[2],
//                T(0,1)*v[0] + T(1,1)*v[1] + T(2,1)*v[2],
//                T(0,2)*v[0] + T(1,2)*v[1] + T(2,2)*v[2]);
// }

// Axis ad(const Axis& s1, const se3& s2)
// {
//    return Axis(s2[2]*s1[1] - s2[1]*s1[2],
//                s2[0]*s1[2] - s2[2]*s1[0],
//                s2[1]*s1[0] - s2[0]*s1[1]);
// }

// Axis ad_Axis_Axis(const Axis& s1, const Axis& s2)
// {
//    return Axis(s2[2]*s1[1] - s2[1]*s1[2],
//                s2[0]*s1[2] - s2[2]*s1[0],
//                s2[1]*s1[0] - s2[0]*s1[1]);
// }

Vector6d dad(const Vector6d& _s, const Vector6d& _t)
{
  Vector6d res;
  res.head<3>()
      = _t.head<3>().cross(_s.head<3>()) + _t.tail<3>().cross(_s.tail<3>());
  res.tail<3>() = _t.tail<3>().cross(_s.head<3>());
  return res;
}

Inertia transformInertia(const Isometry3d& _T, const Inertia& _I)
{
  // operation count: multiplication = 186, addition = 117, subtract = 21

  Inertia ret = Inertia::Identity();

  double d0 = _I(0, 3) + _T(2, 3) * _I(3, 4) - _T(1, 3) * _I(3, 5);
  double d1 = _I(1, 3) - _T(2, 3) * _I(3, 3) + _T(0, 3) * _I(3, 5);
  double d2 = _I(2, 3) + _T(1, 3) * _I(3, 3) - _T(0, 3) * _I(3, 4);
  double d3 = _I(0, 4) + _T(2, 3) * _I(4, 4) - _T(1, 3) * _I(4, 5);
  double d4 = _I(1, 4) - _T(2, 3) * _I(3, 4) + _T(0, 3) * _I(4, 5);
  double d5 = _I(2, 4) + _T(1, 3) * _I(3, 4) - _T(0, 3) * _I(4, 4);
  double d6 = _I(0, 5) + _T(2, 3) * _I(4, 5) - _T(1, 3) * _I(5, 5);
  double d7 = _I(1, 5) - _T(2, 3) * _I(3, 5) + _T(0, 3) * _I(5, 5);
  double d8 = _I(2, 5) + _T(1, 3) * _I(3, 5) - _T(0, 3) * _I(4, 5);
  double e0 = _I(0, 0) + _T(2, 3) * _I(0, 4) - _T(1, 3) * _I(0, 5)
              + d3 * _T(2, 3) - d6 * _T(1, 3);
  double e3 = _I(0, 1) + _T(2, 3) * _I(1, 4) - _T(1, 3) * _I(1, 5)
              - d0 * _T(2, 3) + d6 * _T(0, 3);
  double e4 = _I(1, 1) - _T(2, 3) * _I(1, 3) + _T(0, 3) * _I(1, 5)
              - d1 * _T(2, 3) + d7 * _T(0, 3);
  double e6 = _I(0, 2) + _T(2, 3) * _I(2, 4) - _T(1, 3) * _I(2, 5)
              + d0 * _T(1, 3) - d3 * _T(0, 3);
  double e7 = _I(1, 2) - _T(2, 3) * _I(2, 3) + _T(0, 3) * _I(2, 5)
              + d1 * _T(1, 3) - d4 * _T(0, 3);
  double e8 = _I(2, 2) + _T(1, 3) * _I(2, 3) - _T(0, 3) * _I(2, 4)
              + d2 * _T(1, 3) - d5 * _T(0, 3);
  double f0 = _T(0, 0) * e0 + _T(1, 0) * e3 + _T(2, 0) * e6;
  double f1 = _T(0, 0) * e3 + _T(1, 0) * e4 + _T(2, 0) * e7;
  double f2 = _T(0, 0) * e6 + _T(1, 0) * e7 + _T(2, 0) * e8;
  double f3 = _T(0, 0) * d0 + _T(1, 0) * d1 + _T(2, 0) * d2;
  double f4 = _T(0, 0) * d3 + _T(1, 0) * d4 + _T(2, 0) * d5;
  double f5 = _T(0, 0) * d6 + _T(1, 0) * d7 + _T(2, 0) * d8;
  double f6 = _T(0, 1) * e0 + _T(1, 1) * e3 + _T(2, 1) * e6;
  double f7 = _T(0, 1) * e3 + _T(1, 1) * e4 + _T(2, 1) * e7;
  double f8 = _T(0, 1) * e6 + _T(1, 1) * e7 + _T(2, 1) * e8;
  double g0 = _T(0, 1) * d0 + _T(1, 1) * d1 + _T(2, 1) * d2;
  double g1 = _T(0, 1) * d3 + _T(1, 1) * d4 + _T(2, 1) * d5;
  double g2 = _T(0, 1) * d6 + _T(1, 1) * d7 + _T(2, 1) * d8;
  double g3 = _T(0, 2) * d0 + _T(1, 2) * d1 + _T(2, 2) * d2;
  double g4 = _T(0, 2) * d3 + _T(1, 2) * d4 + _T(2, 2) * d5;
  double g5 = _T(0, 2) * d6 + _T(1, 2) * d7 + _T(2, 2) * d8;
  double h0 = _T(0, 0) * _I(3, 3) + _T(1, 0) * _I(3, 4) + _T(2, 0) * _I(3, 5);
  double h1 = _T(0, 0) * _I(3, 4) + _T(1, 0) * _I(4, 4) + _T(2, 0) * _I(4, 5);
  double h2 = _T(0, 0) * _I(3, 5) + _T(1, 0) * _I(4, 5) + _T(2, 0) * _I(5, 5);
  double h3 = _T(0, 1) * _I(3, 3) + _T(1, 1) * _I(3, 4) + _T(2, 1) * _I(3, 5);
  double h4 = _T(0, 1) * _I(3, 4) + _T(1, 1) * _I(4, 4) + _T(2, 1) * _I(4, 5);
  double h5 = _T(0, 1) * _I(3, 5) + _T(1, 1) * _I(4, 5) + _T(2, 1) * _I(5, 5);

  ret(0, 0) = f0 * _T(0, 0) + f1 * _T(1, 0) + f2 * _T(2, 0);
  ret(0, 1) = f0 * _T(0, 1) + f1 * _T(1, 1) + f2 * _T(2, 1);
  ret(0, 2) = f0 * _T(0, 2) + f1 * _T(1, 2) + f2 * _T(2, 2);
  ret(0, 3) = f3 * _T(0, 0) + f4 * _T(1, 0) + f5 * _T(2, 0);
  ret(0, 4) = f3 * _T(0, 1) + f4 * _T(1, 1) + f5 * _T(2, 1);
  ret(0, 5) = f3 * _T(0, 2) + f4 * _T(1, 2) + f5 * _T(2, 2);
  ret(1, 1) = f6 * _T(0, 1) + f7 * _T(1, 1) + f8 * _T(2, 1);
  ret(1, 2) = f6 * _T(0, 2) + f7 * _T(1, 2) + f8 * _T(2, 2);
  ret(1, 3) = g0 * _T(0, 0) + g1 * _T(1, 0) + g2 * _T(2, 0);
  ret(1, 4) = g0 * _T(0, 1) + g1 * _T(1, 1) + g2 * _T(2, 1);
  ret(1, 5) = g0 * _T(0, 2) + g1 * _T(1, 2) + g2 * _T(2, 2);
  ret(2, 2) = (_T(0, 2) * e0 + _T(1, 2) * e3 + _T(2, 2) * e6) * _T(0, 2)
              + (_T(0, 2) * e3 + _T(1, 2) * e4 + _T(2, 2) * e7) * _T(1, 2)
              + (_T(0, 2) * e6 + _T(1, 2) * e7 + _T(2, 2) * e8) * _T(2, 2);
  ret(2, 3) = g3 * _T(0, 0) + g4 * _T(1, 0) + g5 * _T(2, 0);
  ret(2, 4) = g3 * _T(0, 1) + g4 * _T(1, 1) + g5 * _T(2, 1);
  ret(2, 5) = g3 * _T(0, 2) + g4 * _T(1, 2) + g5 * _T(2, 2);
  ret(3, 3) = h0 * _T(0, 0) + h1 * _T(1, 0) + h2 * _T(2, 0);
  ret(3, 4) = h0 * _T(0, 1) + h1 * _T(1, 1) + h2 * _T(2, 1);
  ret(3, 5) = h0 * _T(0, 2) + h1 * _T(1, 2) + h2 * _T(2, 2);
  ret(4, 4) = h3 * _T(0, 1) + h4 * _T(1, 1) + h5 * _T(2, 1);
  ret(4, 5) = h3 * _T(0, 2) + h4 * _T(1, 2) + h5 * _T(2, 2);
  ret(5, 5)
      = (_T(0, 2) * _I(3, 3) + _T(1, 2) * _I(3, 4) + _T(2, 2) * _I(3, 5))
            * _T(0, 2)
        + (_T(0, 2) * _I(3, 4) + _T(1, 2) * _I(4, 4) + _T(2, 2) * _I(4, 5))
              * _T(1, 2)
        + (_T(0, 2) * _I(3, 5) + _T(1, 2) * _I(4, 5) + _T(2, 2) * _I(5, 5))
              * _T(2, 2);

  ret.triangularView<math::StrictlyLower>() = ret.transpose();

  return ret;
}

Matrix3d parallelAxisTheorem(
    const Matrix3d& _original, const Vector3d& _comShift, double _mass)
{
  const Vector3d& p = _comShift;
  Matrix3d result(_original);
  for (std::size_t i = 0; i < 3; ++i)
    for (std::size_t j = 0; j < 3; ++j)
      result(i, j) += _mass * (delta(i, j) * p.dot(p) - p(i) * p(j));

  return result;
}

bool verifyRotation(const Matrix3d& _T)
{
  return !isNan(_T) && std::abs(_T.determinant() - 1.0) <= DART_EPSILON;
}

bool verifyTransform(const Isometry3d& _T)
{
  return !isNan(_T.matrix().topRows<3>())
         && std::abs(_T.linear().determinant() - 1.0) <= DART_EPSILON;
}

//==============================================================================
Matrix3d computeRotation(const Vector3d& axis, const AxisType axisType)
{
  assert(axis != Vector3d::Zero());

  // First axis
  const Vector3d axis0 = axis.normalized();

  // Second axis
  Vector3d axis1 = axis0.cross(Vector3d::UnitX());
  if (axis1.norm() < DART_EPSILON)
    axis1 = axis0.cross(Vector3d::UnitY());
  axis1.normalize();

  // Third axis
  const Vector3d axis2 = axis0.cross(axis1).normalized();

  // Assign the three axes
  Matrix3d result;
  int index = axisType;
  result.col(index) = axis0;
  result.col(++index % 3) = axis1;
  result.col(++index % 3) = axis2;

  assert(verifyRotation(result));

  return result;
}

//==============================================================================
Isometry3d computeTransform(
    const Vector3d& axis, const Vector3d& translation, AxisType axisType)
{
  Isometry3d result = Isometry3d::Identity();

  result.linear() = computeRotation(axis, axisType);
  result.translation() = translation;

  // Verification
  assert(verifyTransform(result));

  return result;
}

//==============================================================================
SupportPolygon computeSupportPolgyon(
    const SupportGeometry& _geometry,
    const Vector3d& _axis1,
    const Vector3d& _axis2)
{
  std::vector<std::size_t> indices;
  indices.reserve(_geometry.size());
  return computeSupportPolgyon(indices, _geometry, _axis1, _axis2);
}

//==============================================================================
SupportPolygon computeSupportPolgyon(
    std::vector<std::size_t>& _originalIndices,
    const SupportGeometry& _geometry,
    const Vector3d& _axis1,
    const Vector3d& _axis2)
{
  SupportPolygon polygon;
  polygon.reserve(_geometry.size());
  for (const Vector3d& v : _geometry)
    polygon.push_back(Vector2d(v.dot(_axis1), v.dot(_axis2)));

  return computeConvexHull(_originalIndices, polygon);
}

//==============================================================================
// HullAngle is an internal struct used to facilitate the computation of 2D
// convex hulls
struct HullAngle
{
  HullAngle(double angle, double distance, std::size_t index)
    : mAngle(angle), mDistance(distance), mIndex(index)
  {
    // Do nothing
  }

  double mAngle;
  double mDistance;
  std::size_t mIndex;
};

//==============================================================================
// Comparison function to allow hull angles to be sorted
static bool HullAngleComparison(const HullAngle& a, const HullAngle& b)
{
  return a.mAngle < b.mAngle;
}

//==============================================================================
SupportPolygon computeConvexHull(const SupportPolygon& _points)
{
  std::vector<std::size_t> indices;
  indices.reserve(_points.size());
  return computeConvexHull(indices, _points);
}

//==============================================================================
Vector2d computeCentroidOfHull(const SupportPolygon& _convexHull)
{
  if (_convexHull.size() == 0) {
    Vector2d invalid = Vector2d::Constant(std::nan(""));
    dtwarn << "[computeCentroidOfHull] Requesting the centroid of an empty set "
           << "of points! We will return <" << invalid.transpose() << ">.\n";
    return invalid;
  }

  if (_convexHull.size() == 1)
    return _convexHull[0];

  if (_convexHull.size() == 2)
    return (_convexHull[0] + _convexHull[1]) / 2.0;

  Vector2d c(0, 0);
  Vector2d intersect;
  double area = 0;
  double area_i;
  Vector2d midp12, midp01;

  for (std::size_t i = 2; i < _convexHull.size(); ++i) {
    const Vector2d& p0 = _convexHull[0];
    const Vector2d& p1 = _convexHull[i - 1];
    const Vector2d& p2 = _convexHull[i];

    area_i = 0.5
             * ((p1[0] - p0[0]) * (p2[1] - p0[1])
                - (p1[1] - p0[1]) * (p2[0] - p0[0]));

    midp12 = 0.5 * (p1 + p2);
    midp01 = 0.5 * (p0 + p1);

    IntersectionResult result
        = computeIntersection(intersect, p0, midp12, p2, midp01);

    if (BEYOND_ENDPOINTS == result) {
      double a1 = atan2((p1 - p0)[1], (p1 - p0)[0]) * 180.0 / pi();
      double a2 = atan2((p2 - p0)[1], (p2 - p0)[0]) * 180.0 / pi();
      double diff = a1 - a2;
      dtwarn << "[computeCentroidOfHull] You have passed in a set of points "
             << "which is not a proper convex hull! The invalid segment "
             << "contains indices " << i - 1 << " -> " << i << ":\n"
             << i - 1 << ") " << p1.transpose() << " (" << a1 << " degrees)"
             << "\n"
             << i << ") " << p2.transpose() << " (" << a2 << " degrees)"
             << "\n"
             << "0) " << p0.transpose() << "\n"
             << "(" << result << ") "
             << (PARALLEL == result
                     ? "These segments are parallel!\n"
                     : "These segments are too short to intersect!\n")
             << "Difference in angle: " << diff << "\n\n";
      continue;
    }

    area += area_i;
    c += area_i * intersect;
  }

  // A negative area means we have a bug in the code
  assert(area >= 0.0);

  if (area == 0.0)
    return c;

  return c / area;
}

//==============================================================================
// Returns true if the path that goes from p1 -> p2 -> p3 turns left
static bool isLeftTurn(
    const Vector2d& p1, const Vector2d& p2, const Vector2d& p3)
{
  return (cross(p2 - p1, p3 - p1) > 0);
}

//==============================================================================
SupportPolygon computeConvexHull(
    std::vector<std::size_t>& _originalIndices, const SupportPolygon& _points)
{
  _originalIndices.clear();

  if (_points.size() <= 3) {
    // Three or fewer points is already a convex hull
    for (std::size_t i = 0; i < _points.size(); ++i)
      _originalIndices.push_back(i);

    return _points;
  }

  // We'll use "Graham scan" to compute the convex hull in the general case
  std::size_t lowestIndex = static_cast<std::size_t>(-1);
  double lowestY = inf<double>();
  for (std::size_t i = 0; i < _points.size(); ++i) {
    if (_points[i][1] < lowestY) {
      lowestIndex = i;
      lowestY = _points[i][1];
    } else if (_points[i][1] == lowestY) {
      if (_points[i][0] < _points[lowestIndex][0]) {
        lowestIndex = i;
      }
    }
  }

  std::vector<HullAngle> angles;
  const Vector2d& bottom = _points[lowestIndex];
  for (std::size_t i = 0; i < _points.size(); ++i) {
    const Vector2d& p = _points[i];
    if (p != bottom) {
      const Vector2d& v = p - bottom;
      angles.push_back(HullAngle(atan2(v[1], v[0]), v.norm(), i));
    }
  }

  std::sort(angles.begin(), angles.end(), HullAngleComparison);

  if (angles.size() > 1) {
    for (std::size_t i = 0; i < angles.size() - 1; ++i) {
      if (std::abs(angles[i].mAngle - angles[i + 1].mAngle) < 1e-12) {
        // If two points have the same angle, throw out the one that is closer
        // to the corner
        std::size_t tossout
            = (angles[i].mDistance < angles[i + 1].mDistance) ? i : i + 1;
        angles.erase(angles.begin() + tossout);
        --i;
      }
    }
  }

  if (angles.size() <= 3) {
    // There were so many repeated points in the given set that we only have
    // three or fewer unique points
    _originalIndices.reserve(angles.size() + 1);
    _originalIndices.push_back(lowestIndex);
    for (std::size_t i = 0; i < angles.size(); ++i)
      _originalIndices.push_back(angles[i].mIndex);

    SupportPolygon polygon;
    polygon.reserve(_originalIndices.size());
    for (std::size_t index : _originalIndices)
      polygon.push_back(_points[index]);

    return polygon;
  }

  std::vector<std::size_t>& edge = _originalIndices;
  std::size_t lastIndex = lowestIndex;
  std::size_t secondToLastIndex = angles[0].mIndex;
  edge.reserve(angles.size() + 1);

  edge.push_back(lowestIndex);

  for (std::size_t i = 1; i < angles.size(); ++i) {
    std::size_t currentIndex = angles[i].mIndex;
    const Vector2d& p1 = _points[lastIndex];
    const Vector2d& p2 = _points[secondToLastIndex];
    const Vector2d& p3 = _points[currentIndex];

    bool leftTurn = isLeftTurn(p1, p2, p3);

    if (leftTurn) {
      edge.push_back(secondToLastIndex);
      lastIndex = secondToLastIndex;
      secondToLastIndex = currentIndex;
    } else {
      secondToLastIndex = edge.back();
      edge.pop_back();
      lastIndex = edge.back();
      --i;
    }
  }

  const Vector2d& p1 = _points[edge.back()];
  const Vector2d& p2 = _points[angles.back().mIndex];
  const Vector2d& p3 = _points[lowestIndex];
  if (isLeftTurn(p1, p2, p3))
    edge.push_back(angles.back().mIndex);

  SupportPolygon polygon;
  polygon.reserve(edge.size());
  for (std::size_t index : edge)
    polygon.push_back(_points[index]);

  // Note that we do not need to fill in _originalIndices, because "edge" is a
  // non-const reference to _originalIndices and it has been filled in with the
  // appropriate values.
  return polygon;
}

//==============================================================================
IntersectionResult computeIntersection(
    Vector2d& _intersectionPoint,
    const Vector2d& a1,
    const Vector2d& a2,
    const Vector2d& b1,
    const Vector2d& b2)
{
  double dx_a = a2[0] - a1[0];
  double dy_a = a2[1] - a1[1];

  double dx_b = b2[0] - b1[0];
  double dy_b = b2[1] - b1[1];

  Vector2d& point = _intersectionPoint;

  if (std::abs(dx_b * dy_a - dx_a * dy_b) < 1e-12) {
    // The line segments are parallel, so give back an average of all the points
    point = (a1 + a2 + b1 + b2) / 4.0;
    return PARALLEL;
  }

  point[0] = (dx_b * dy_a * a1[0] - dx_a * dy_b * b1[0]
              + dx_a * dx_b * (b1[1] - a1[1]))
             / (dx_b * dy_a - dx_a * dy_b);

  if (dx_a != 0.0)
    point[1] = dy_a / dx_a * (point[0] - a1[0]) + a1[1];
  else
    point[1] = dy_b / dx_b * (point[0] - b1[0]) + b1[1];

  for (std::size_t i = 0; i < 2; ++i) {
    if ((point[i] < std::min(a1[i], a2[i]))
        || (std::max(a1[i], a2[i]) < point[i])) {
      return BEYOND_ENDPOINTS;
    }

    if ((point[i] < std::min(b1[i], b2[i]))
        || (std::max(b1[i], b2[i]) < point[i])) {
      return BEYOND_ENDPOINTS;
    }
  }

  return INTERSECTING;
}

//==============================================================================
double cross(const Vector2d& _v1, const Vector2d& _v2)
{
  return _v1[0] * _v2[1] - _v1[1] * _v2[0];
}

//==============================================================================
bool isInsideSupportPolygon(
    const Vector2d& _p, const SupportPolygon& _support, bool _includeEdge)
{
  if (_support.size() == 0)
    return false;

  if (_support.size() == 1) {
    if (!_includeEdge)
      return false;

    return (_support[0] == _p);
  }

  if (_support.size() == 2) {
    if (!_includeEdge)
      return false;

    const Vector2d& p1 = _support[0];
    const Vector2d& p2 = _support[1];
    const Vector2d& p3 = _p;

    if (cross(p2 - p1, p3 - p1) == 0) {
      if (p3[0] < std::min(p1[0], p2[0]) || std::max(p1[0], p2[0]) < p3[0])
        return false;

      return true;
    }

    return false;
  }

  for (std::size_t i = 0; i < _support.size(); ++i) {
    const Vector2d& p1 = (i == 0) ? _support.back() : _support[i - 1];
    const Vector2d& p2 = _support[i];
    const Vector2d& p3 = _p;

    double crossProduct = cross(p2 - p1, p3 - p1);
    if (crossProduct > 0.0)
      continue;

    if (crossProduct == 0) {
      if (!_includeEdge)
        return false;

      if (p3[0] < std::min(p1[0], p2[0]) || std::max(p1[0], p2[0]) < p3[0])
        return false;

      return true;
    } else {
      return false;
    }
  }

  return true;
}

//==============================================================================
Vector2d computeClosestPointOnLineSegment(
    const Vector2d& _p, const Vector2d& _s1, const Vector2d& _s2)
{
  Vector2d result;

  if (_s1[0] - _s2[0] == 0) {
    result[0] = _s1[0];
    result[1] = _p[1];

    if (result[1] < std::min(_s1[1], _s2[1])
        || std::max(_s1[1], _s2[1]) < result[1]) {
      if (std::abs(_p[1] - _s2[1]) < std::abs(_p[1] - _s1[1]))
        result[1] = _s2[1];
      else
        result[1] = _s1[1];
    }
  } else {
    double m = (_s2[1] - _s1[1]) / (_s2[0] - _s1[0]);
    double k = _s1[1] - m * _s1[0];
    result[0] = (_p[0] + m * (_p[1] - k)) / (m * m + 1.0);
    result[1] = m * result[0] + k;

    if (result[0] < std::min(_s1[0], _s2[0])
        || std::max(_s1[0], _s2[0]) < result[0]) {
      if ((_p - _s2).norm() < (_p - _s1).norm())
        result = _s2;
      else
        result = _s1;
    }
  }

  return result;
}

//==============================================================================
Vector2d computeClosestPointOnSupportPolygon(
    const Vector2d& _p, const SupportPolygon& _support)
{
  std::size_t _index1;
  std::size_t _index2;
  return computeClosestPointOnSupportPolygon(_index1, _index2, _p, _support);
}

//==============================================================================
Vector2d computeClosestPointOnSupportPolygon(
    std::size_t& _index1,
    std::size_t& _index2,
    const Vector2d& _p,
    const SupportPolygon& _support)
{
  if (_support.size() == 0) {
    _index1 = static_cast<std::size_t>(-1);
    _index2 = _index1;
    return _p;
  }

  if (_support.size() == 1) {
    _index1 = 0;
    _index2 = 0;
    return _support[0];
  }

  if (_support.size() == 2) {
    _index1 = 0;
    _index2 = 1;
    return computeClosestPointOnLineSegment(_p, _support[0], _support[1]);
  }

  double best = inf<double>(), check;
  Vector2d test, result;
  for (std::size_t i = 0; i < _support.size(); ++i) {
    const Vector2d& p1 = (i == 0) ? _support.back() : _support[i - 1];
    const Vector2d& p2 = _support[i];

    test = computeClosestPointOnLineSegment(_p, p1, p2);
    check = (test - _p).norm();
    if (check < best) {
      best = check;
      result = test;
      _index1 = (i == 0) ? _support.size() - 1 : i - 1;
      _index2 = i;
    }
  }

  return result;
}

BoundingBox::BoundingBox() : mMin(0, 0, 0), mMax(0, 0, 0) {}
BoundingBox::BoundingBox(const Vector3d& min, const Vector3d& max)
  : mMin(min), mMax(max)
{
}

} // namespace math
} // namespace dart
