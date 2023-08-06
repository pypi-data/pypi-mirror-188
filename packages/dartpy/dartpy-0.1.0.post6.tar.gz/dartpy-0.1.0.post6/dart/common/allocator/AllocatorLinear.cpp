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

#include "dart/common/allocator/AllocatorLinear.hpp"

#include "dart/common/Logging.hpp"
#include "dart/common/Macros.hpp"

namespace dart::common {

//==============================================================================
AllocatorLinear::AllocatorLinear(size_t max_capacity, Allocator& base_allocator)
  : m_max_capacity(max_capacity),
    m_base_allocator(base_allocator),
    m_start_ptr(base_allocator.allocate(max_capacity)),
    m_offset(0)
{
  if (max_capacity == 0) {
    DART_DEBUG(
        "Allocator with zero max capacity is not able to allocate any memory.");
  }
}

//==============================================================================
AllocatorLinear::~AllocatorLinear()
{
  if (m_start_ptr) {
    this->m_base_allocator.deallocate(m_start_ptr, m_max_capacity);
    m_start_ptr = nullptr;
  }
}

//==============================================================================
void* AllocatorLinear::allocate(size_t size) noexcept
{
  if (size == 0 || m_start_ptr == nullptr) {
    return nullptr;
  }

  // Lock the mutex
  std::lock_guard<std::mutex> lock(m_mutex);

  const size_t current_ptr = reinterpret_cast<size_t>(m_start_ptr) + m_offset;

  // Check max capacity
  if (m_offset + size > m_max_capacity) {
    DART_DEBUG(
        "Allocating {} exceeds the max capacity {}. Returning "
        "nullptr.",
        size,
        m_max_capacity);
    return nullptr;
  }

  // Update offset
  m_offset += size;

  return reinterpret_cast<void*>(current_ptr);
}

//==============================================================================
void AllocatorLinear::deallocate(void* pointer, size_t size)
{
  // AllocatorLinear doesn't allow to deallocate memory
  DART_UNUSED(pointer, size);
}

//==============================================================================
size_t AllocatorLinear::get_max_capacity() const
{
  // No need to lock the mutex as m_max_capacity isn't changed once
  // initialized
  return m_max_capacity;
}

//==============================================================================
size_t AllocatorLinear::get_size() const
{
  std::lock_guard<std::mutex> lock(m_mutex);
  return m_offset;
}

//==============================================================================
const void* AllocatorLinear::get_begin_address() const
{
  // No need to lock the mutex as m_head isn't changed once initialized
  return m_start_ptr;
}

//==============================================================================
void AllocatorLinear::print(std::ostream& os, int indent) const
{
  // Lock the mutex
  std::lock_guard<std::mutex> lock(m_mutex);

  if (indent == 0) {
    os << "[AllocatorLinear]\n";
  }
  const std::string spaces(indent, ' ');
  if (indent != 0) {
    os << spaces << "type: " << getType() << "\n";
  }
  os << spaces << "first_address: " << m_start_ptr << "\n";
  os << spaces << "size_in_bytes: " << m_offset << "\n";
  os << spaces << "base_allocator:\n";
  m_base_allocator.print(os, indent + 2);
}

} // namespace dart::common
