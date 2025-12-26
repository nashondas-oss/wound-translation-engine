"""
Unit tests for SigilGenerator module.

Tests the procedural generation of sigils including:
- Correct generation for different wound types
- Procedural uniqueness for different solver IDs
- Color integrity matching the design system
"""

import os
import pytest
from pathlib import Path
from PIL import Image
from terra_gaia.translator.sigil import SigilGenerator


class TestSigilGenerator:
    """Test suite for SigilGenerator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.test_output_dir = Path("/tmp/test_sigils")
        self.test_output_dir.mkdir(exist_ok=True)
    
    def teardown_method(self):
        """Clean up test files."""
        # Remove test output files
        if self.test_output_dir.exists():
            for file in self.test_output_dir.glob("*.png"):
                file.unlink()
    
    def test_root_sigil_generation(self):
        """Test generation of root chakra sigil."""
        sigil = SigilGenerator(
            frequency="396 Hz",
            wound="root",
            solver_id="test_solver_root"
        )
        
        output_path = self.test_output_dir / "sigil_root.png"
        result_path = sigil.generate(str(output_path))
        
        # Verify file was created
        assert os.path.exists(result_path)
        assert Path(result_path) == output_path
        
        # Verify it's a valid image
        img = Image.open(result_path)
        assert img.size == (512, 512)
        assert img.mode == 'RGB'
    
    def test_sacral_sigil_generation(self):
        """Test generation of sacral chakra sigil."""
        sigil = SigilGenerator(
            frequency="417 Hz",
            wound="sacral",
            solver_id="test_solver_sacral"
        )
        
        output_path = self.test_output_dir / "sigil_sacral.png"
        result_path = sigil.generate(str(output_path))
        
        # Verify file was created
        assert os.path.exists(result_path)
        
        # Verify it's a valid image
        img = Image.open(result_path)
        assert img.size == (512, 512)
        assert img.mode == 'RGB'
    
    def test_solar_plexus_sigil_generation(self):
        """Test generation of solar plexus chakra sigil."""
        sigil = SigilGenerator(
            frequency="528 Hz",
            wound="solar_plexus",
            solver_id="test_solver_solar"
        )
        
        output_path = self.test_output_dir / "sigil_solar_plexus.png"
        result_path = sigil.generate(str(output_path))
        
        # Verify file was created
        assert os.path.exists(result_path)
        
        # Verify it's a valid image
        img = Image.open(result_path)
        assert img.size == (512, 512)
        assert img.mode == 'RGB'
    
    def test_procedural_uniqueness(self):
        """Test that different solver IDs produce different variations."""
        solver_id_1 = "solver_alpha"
        solver_id_2 = "solver_beta"
        
        sigil_1 = SigilGenerator(
            frequency="396 Hz",
            wound="root",
            solver_id=solver_id_1
        )
        
        sigil_2 = SigilGenerator(
            frequency="396 Hz",
            wound="root",
            solver_id=solver_id_2
        )
        
        # Verify that variations are different
        assert sigil_1.variations != sigil_2.variations
        assert sigil_1.variations["rotation_offset"] != sigil_2.variations["rotation_offset"]
        assert sigil_1.variations["layer_count"] != sigil_2.variations["layer_count"] or \
               sigil_1.variations["ray_count"] != sigil_2.variations["ray_count"]
    
    def test_procedural_consistency(self):
        """Test that same solver ID produces same variations."""
        solver_id = "consistent_solver"
        
        sigil_1 = SigilGenerator(
            frequency="396 Hz",
            wound="root",
            solver_id=solver_id
        )
        
        sigil_2 = SigilGenerator(
            frequency="396 Hz",
            wound="root",
            solver_id=solver_id
        )
        
        # Verify that variations are identical
        assert sigil_1.variations == sigil_2.variations
    
    def test_color_palette_root(self):
        """Test color palette integrity for root chakra."""
        sigil = SigilGenerator(
            frequency="396 Hz",
            wound="root",
            solver_id="test_color_root"
        )
        
        # Verify color palette
        assert "primary" in sigil.colors
        assert "secondary" in sigil.colors
        assert "accent" in sigil.colors
        assert "background" in sigil.colors
        
        # Verify red-based colors for root
        primary = sigil.colors["primary"]
        assert primary[0] > primary[1]  # More red than green
        assert primary[0] > primary[2]  # More red than blue
    
    def test_color_palette_sacral(self):
        """Test color palette integrity for sacral chakra."""
        sigil = SigilGenerator(
            frequency="417 Hz",
            wound="sacral",
            solver_id="test_color_sacral"
        )
        
        # Verify orange-based colors for sacral
        primary = sigil.colors["primary"]
        assert primary[0] > primary[2]  # More red than blue
        assert primary[1] > primary[2]  # More green than blue (orange is red+green)
    
    def test_color_palette_solar_plexus(self):
        """Test color palette integrity for solar plexus chakra."""
        sigil = SigilGenerator(
            frequency="528 Hz",
            wound="solar_plexus",
            solver_id="test_color_solar"
        )
        
        # Verify yellow-based colors for solar plexus
        primary = sigil.colors["primary"]
        assert primary[0] > 200  # High red component
        assert primary[1] > 200  # High green component (yellow is red+green)
    
    def test_custom_image_size(self):
        """Test generation with custom image size."""
        sigil = SigilGenerator(
            frequency="396 Hz",
            wound="root",
            solver_id="test_size"
        )
        
        custom_size = 256
        output_path = self.test_output_dir / "sigil_custom_size.png"
        result_path = sigil.generate(str(output_path), image_size=custom_size)
        
        # Verify image has custom size
        img = Image.open(result_path)
        assert img.size == (custom_size, custom_size)
    
    def test_output_directory_creation(self):
        """Test that output directories are created if they don't exist."""
        sigil = SigilGenerator(
            frequency="396 Hz",
            wound="root",
            solver_id="test_dir_creation"
        )
        
        nested_path = self.test_output_dir / "nested" / "path" / "sigil.png"
        result_path = sigil.generate(str(nested_path))
        
        # Verify file was created
        assert os.path.exists(result_path)
    
    def test_frequency_to_wound_mapping(self):
        """Test that frequency maps correctly to wound type."""
        # Test that providing frequency maps to correct wound
        sigil = SigilGenerator(
            frequency="396 Hz",
            wound="root",  # Should match frequency
            solver_id="test_mapping"
        )
        assert sigil.wound == "root"
        
        # Test frequency override
        sigil2 = SigilGenerator(
            frequency="417 Hz",  # Sacral frequency
            wound="anything",  # Will be overridden by frequency
            solver_id="test_mapping2"
        )
        assert sigil2.wound == "sacral"
    
    def test_invalid_wound_type(self):
        """Test that invalid wound type raises appropriate error."""
        with pytest.raises(ValueError, match="Unsupported wound type"):
            SigilGenerator(
                frequency="999 Hz",  # Invalid frequency
                wound="invalid_wound",
                solver_id="test_invalid"
            )
    
    def test_variation_ranges(self):
        """Test that procedural variations are within expected ranges."""
        sigil = SigilGenerator(
            frequency="396 Hz",
            wound="root",
            solver_id="test_ranges"
        )
        
        vars = sigil.variations
        
        # Test rotation offset (0-360 degrees)
        assert 0 <= vars["rotation_offset"] <= 360
        
        # Test layer count (3-7 layers)
        assert 3 <= vars["layer_count"] <= 7
        
        # Test ray count (6-12 rays)
        assert 6 <= vars["ray_count"] <= 12
        
        # Test line weight (1-5 pixels)
        assert 1 <= vars["line_weight"] <= 5
        
        # Test scale factor (0.7-1.3)
        assert 0.7 <= vars["scale_factor"] <= 1.3
    
    def test_example_from_problem_statement(self):
        """Test the exact example provided in the problem statement."""
        sigil = SigilGenerator(
            frequency="396 Hz",
            wound="root",
            solver_id="solver123"
        )
        
        output_path = self.test_output_dir / "sigil_root_example.png"
        sigil_image_path = sigil.generate(output_path=str(output_path))
        
        # Verify the example works as expected
        assert os.path.exists(sigil_image_path)
        assert sigil_image_path == str(output_path)
