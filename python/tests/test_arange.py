"""
Unit tests for numpy's arange function.

Tests cover:
- Basic usage with stop parameter
- Start and stop parameters
- Start, stop, and step parameters
- Different data types (int, float)
- Negative values
- Edge cases (empty arrays, step=0 error)
- dtype parameter
"""
import numpy as np
import pytest


class TestArangeBasic:
    """Test basic arange functionality with single stop parameter."""

    def test_arange_stop_positive_int(self):
        """Test arange with positive integer stop."""
        result = np.arange(5)
        expected = np.array([0, 1, 2, 3, 4])
        assert np.array_equal(result, expected)
        assert result.dtype == np.dtype('int64') or result.dtype == np.dtype('int32')

    def test_arange_stop_zero(self):
        """Test arange with stop=0 returns empty array."""
        result = np.arange(0)
        assert result.shape == (0,)
        assert len(result) == 0

    def test_arange_stop_negative(self):
        """Test arange with negative stop returns empty array."""
        result = np.arange(-5)
        assert result.shape == (0,)


class TestArangeStartStop:
    """Test arange with start and stop parameters."""

    def test_arange_start_stop_positive(self):
        """Test arange with start and stop."""
        result = np.arange(2, 7)
        expected = np.array([2, 3, 4, 5, 6])
        assert np.array_equal(result, expected)

    def test_arange_start_equals_stop(self):
        """Test arange when start equals stop returns empty array."""
        result = np.arange(5, 5)
        assert result.shape == (0,)

    def test_arange_negative_start_stop(self):
        """Test arange with negative start and stop."""
        result = np.arange(-3, 3)
        expected = np.array([-3, -2, -1, 0, 1, 2])
        assert np.array_equal(result, expected)

    def test_arange_both_negative(self):
        """Test arange with both negative values."""
        result = np.arange(-7, -2)
        expected = np.array([-7, -6, -5, -4, -3])
        assert np.array_equal(result, expected)


class TestArangeWithStep:
    """Test arange with step parameter."""

    def test_arange_positive_step(self):
        """Test arange with positive step."""
        result = np.arange(0, 10, 2)
        expected = np.array([0, 2, 4, 6, 8])
        assert np.array_equal(result, expected)

    def test_arange_negative_step(self):
        """Test arange with negative step (start > stop)."""
        result = np.arange(10, 0, -2)
        expected = np.array([10, 8, 6, 4, 2])
        assert np.array_equal(result, expected)

    def test_arange_step_larger_than_range(self):
        """Test arange when step is larger than range."""
        result = np.arange(0, 5, 10)
        expected = np.array([0])
        assert np.array_equal(result, expected)

    def test_arange_float_step(self):
        """Test arange with float step."""
        result = np.arange(0, 1, 0.25)
        expected = np.array([0.0, 0.25, 0.5, 0.75])
        assert np.allclose(result, expected)

    def test_arange_zero_step_raises_error(self):
        """Test that step=0 raises ValueError."""
        with pytest.raises(ValueError):
            np.arange(0, 10, 0)


class TestArangeFloatInput:
    """Test arange with float inputs."""

    def test_arange_float_stop(self):
        """Test arange with float stop."""
        result = np.arange(5.0)
        expected = np.array([0., 1., 2., 3., 4.])
        assert np.allclose(result, expected)

    def test_arange_float_start_stop(self):
        """Test arange with float start and stop."""
        result = np.arange(1.5, 4.5)
        expected = np.array([1.5, 2.5, 3.5])
        assert np.allclose(result, expected)

    def test_arange_float_precision(self):
        """Test arange with float values for precision."""
        result = np.arange(0.0, 0.3, 0.1)
        expected = np.array([0.0, 0.1, 0.2])
        assert np.allclose(result, expected, rtol=1e-10)


class TestArangeDtype:
    """Test arange with dtype parameter."""

    def test_arange_dtype_int32(self):
        """Test arange with int32 dtype."""
        result = np.arange(5, dtype=np.int32)
        assert result.dtype == np.int32
        expected = np.array([0, 1, 2, 3, 4], dtype=np.int32)
        assert np.array_equal(result, expected)

    def test_arange_dtype_float32(self):
        """Test arange with float32 dtype."""
        result = np.arange(3, dtype=np.float32)
        assert result.dtype == np.float32
        expected = np.array([0., 1., 2.], dtype=np.float32)
        assert np.allclose(result, expected)

    def test_arange_dtype_float64(self):
        """Test arange with float64 dtype."""
        result = np.arange(3, dtype=np.float64)
        assert result.dtype == np.float64

    def test_arange_dtype_uint8(self):
        """Test arange with uint8 dtype."""
        result = np.arange(5, dtype=np.uint8)
        assert result.dtype == np.uint8


class TestArangeEdgeCases:
    """Test edge cases for arange."""

    def test_arange_large_array(self):
        """Test arange with large number of elements."""
        result = np.arange(10000)
        assert len(result) == 10000
        assert result[0] == 0
        assert result[-1] == 9999

    def test_arange_shape(self):
        """Test that arange returns correct shape."""
        result = np.arange(10)
        assert result.shape == (10,)

    def test_arange_with_kwargs(self):
        """Test arange with keyword arguments."""
        result = np.arange(stop=5, dtype=float)
        expected = np.array([0., 1., 2., 3., 4.])
        assert np.allclose(result, expected)

    def test_arange_device_default(self):
        """Test arange returns array on default device (cpu)."""
        result = np.arange(5)
        assert result.device == 'cpu'


class TestArangeReturnType:
    """Test return type and attributes of arange."""

    def test_returns_ndarray(self):
        """Test that arange returns numpy ndarray."""
        result = np.arange(5)
        assert isinstance(result, np.ndarray)

    def test_arange_is_1d(self):
        """Test that arange always returns 1D array."""
        result = np.arange(10)
        assert result.ndim == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
