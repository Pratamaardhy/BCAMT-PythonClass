import unittest
import math
import geometry

class TestGeometryPositive(unittest.TestCase):
    def test_luas_persegi(self):
        self.assertEqual(geometry.luas_persegi(4), 16)

    def test_keliling_persegi(self):
        self.assertEqual(geometry.keliling_persegi(4), 16)

    def test_luas_persegi_panjang(self):
        self.assertEqual(geometry.luas_persegi_panjang(5, 2), 10)

    def test_keliling_persegi_panjang(self):
        self.assertEqual(geometry.keliling_persegi_panjang(5, 2), 14)

    def test_luas_lingkaran(self):
        self.assertAlmostEqual(geometry.luas_lingkaran(1), math.pi)

    def test_keliling_lingkaran(self):
        self.assertAlmostEqual(geometry.keliling_lingkaran(1), 2 * math.pi)

class TestGeometryNegative(unittest.TestCase):
    def test_non_numeric_persegi(self):
        with self.assertRaises(TypeError):
            geometry.luas_persegi("a")

    def test_non_numeric_persegi_panjang(self):
        with self.assertRaises(TypeError):
            geometry.luas_persegi_panjang("a", "b")

    def test_non_numeric_lingkaran(self):
        with self.assertRaises(TypeError):
            geometry.luas_lingkaran(None)


class TestGeometryScenarios(unittest.TestCase):
    def test_zero_values(self):
        self.assertEqual(geometry.luas_persegi(0), 0)
        self.assertEqual(geometry.luas_persegi_panjang(0, 5), 0)
        self.assertAlmostEqual(geometry.luas_lingkaran(0), 0.0)

    def test_negative_values_behavior(self):
        # The current implementation does not validate sign; it performs arithmetic.
        # We assert the mathematical result (could be changed to raise in future).
        self.assertEqual(geometry.luas_persegi(-3), 9)
        self.assertEqual(geometry.luas_persegi_panjang(-2, 3), -6)

    def test_float_values(self):
        self.assertAlmostEqual(geometry.luas_persegi(2.5), 6.25)
        self.assertAlmostEqual(geometry.luas_persegi_panjang(2.5, 4.0), 10.0)
        self.assertAlmostEqual(geometry.keliling_lingkaran(0.5), 2 * math.pi * 0.5)

    def test_mixed_int_float(self):
        self.assertAlmostEqual(geometry.luas_persegi_panjang(3, 2.5), 7.5)

    def test_large_values(self):
        big = 10**6
        self.assertEqual(geometry.luas_persegi(big), big * big)

if __name__ == "__main__":
    unittest.main()
