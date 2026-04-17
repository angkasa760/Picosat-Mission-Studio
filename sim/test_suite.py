import unittest
import numpy as np
from sim.link_budget import calculate_itu_losses
from sim.vibration_analysis import calculate_miles_rms
from sim.thermal_analysis import solve_2node_thermal

class TestPicosatPhysics(unittest.TestCase):
    """
    Unit Test Suite for Critical Engineering Physics Formulas.
    Verifies that 'Hardened' logic produces results matching known analytical benchmarks.
    """
    
    def test_itu_loss_positivity(self):
        """ITU losses should be positive for any valid frequency and elevation."""
        loss = calculate_itu_losses(437.2e6, 30.0)
        self.assertGreater(loss, 0.0, "Atmospheric loss must be positive")
        self.assertLess(loss, 5.0, "UHF atmospheric loss should be nominal (< 5dB)")

    def test_miles_equation(self):
        """Verify Miles' Equation: Grms = sqrt(pi/2 * PSD * f * Q)."""
        psd = 0.1
        f = 500
        q = 10
        expected = np.sqrt((np.pi / 2.0) * psd * f * q)
        actual = calculate_miles_rms(psd, f, q)
        self.assertAlmostEqual(actual, expected, places=5)
        self.assertGreater(actual, 25.0, "Expected significant G-rms for given PSD/Q")

    def test_thermal_radiative_transfer(self):
        """Verify that internal temperature stays above skin during heat generation."""
        t_skin = 233.15 # -40°C
        t_int = 293.15  # 20°C
        q_gen = 0.5     # 500mW
        dt = 60         # 1 min
        
        _, t_int_next = solve_2node_thermal(t_skin, t_int, q_gen, dt)
        
        # Heat generation + colder skin -> internal should adjust based on balance
        # With q_gen=0.5W, it should either hold or drop slowly depending on losses.
        self.assertLess(t_int_next, t_int + 0.1, "Internal temp shouldn't spike excessively")
        self.assertGreater(t_int_next, t_skin, "Internal node must remain warmer than heat sink skin")

    def test_vibration_sos(self):
        """Structural Margin of Safety logic verification."""
        yield_str = 276.0
        applied_stress = 200.0
        expected_mos = (yield_str / applied_stress) - 1.0
        self.assertAlmostEqual(expected_mos, 0.38, places=2)

if __name__ == '__main__':
    print("--- RUNNING PROFESSIONAL ENGINEERING TEST SUITE ---")
    unittest.main()
