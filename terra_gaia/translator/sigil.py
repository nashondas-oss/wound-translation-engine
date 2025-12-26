"""
SigilGenerator Module - Procedural generation of sigils for Wound Reports

This module implements the Sigil Visual Design System with sacred geometry,
chakra color palettes, and solver-specific variations.
"""

import hashlib
import math
from pathlib import Path
from typing import Tuple, Dict, Optional
from PIL import Image, ImageDraw


class SigilGenerator:
    """
    Generates unique sigils based on wound type, frequency, and solver ID.
    
    Uses procedural variation algorithms to create sacred geometry patterns
    with chakra-based color palettes.
    """
    
    # Chakra frequency mappings (in Hz)
    FREQUENCY_MAP = {
        "396 Hz": "root",
        "417 Hz": "sacral",
        "528 Hz": "solar_plexus",
        "639 Hz": "heart",
        "741 Hz": "throat",
        "852 Hz": "third_eye",
        "963 Hz": "crown"
    }
    
    # Color palettes for each chakra (primary, secondary, accent)
    COLOR_PALETTES = {
        "root": {
            "primary": (196, 30, 58),      # Deep red
            "secondary": (139, 0, 0),       # Dark red
            "accent": (255, 69, 0),         # Red-orange
            "background": (20, 10, 10)      # Very dark red-black
        },
        "sacral": {
            "primary": (255, 140, 0),       # Dark orange
            "secondary": (255, 165, 0),     # Orange
            "accent": (255, 215, 0),        # Gold
            "background": (20, 15, 5)       # Very dark brown
        },
        "solar_plexus": {
            "primary": (255, 215, 0),       # Gold
            "secondary": (255, 255, 0),     # Yellow
            "accent": (255, 250, 205),      # Lemon chiffon
            "background": (20, 20, 5)       # Very dark yellow-black
        },
        "heart": {
            "primary": (0, 128, 0),         # Green
            "secondary": (34, 139, 34),     # Forest green
            "accent": (144, 238, 144),      # Light green
            "background": (5, 15, 5)        # Very dark green-black
        },
        "throat": {
            "primary": (0, 191, 255),       # Deep sky blue
            "secondary": (30, 144, 255),    # Dodger blue
            "accent": (135, 206, 250),      # Light sky blue
            "background": (5, 10, 20)       # Very dark blue-black
        },
        "third_eye": {
            "primary": (75, 0, 130),        # Indigo
            "secondary": (138, 43, 226),    # Blue violet
            "accent": (147, 112, 219),      # Medium purple
            "background": (10, 5, 20)       # Very dark purple-black
        },
        "crown": {
            "primary": (138, 43, 226),      # Blue violet
            "secondary": (148, 0, 211),     # Dark violet
            "accent": (218, 112, 214),      # Orchid
            "background": (15, 5, 20)       # Very dark violet-black
        }
    }
    
    def __init__(self, frequency: str, wound: str, solver_id: str):
        """
        Initialize SigilGenerator.
        
        Args:
            frequency: Chakra frequency (e.g., "396 Hz")
            wound: Wound type (e.g., "root", "sacral", "solar_plexus")
            solver_id: Unique solver identifier for procedural variation
        """
        self.frequency = frequency
        self.wound = wound.lower()
        self.solver_id = solver_id
        
        # Validate wound type
        if self.wound not in self.COLOR_PALETTES:
            # If frequency is provided, try to map it to wound
            if frequency in self.FREQUENCY_MAP:
                self.wound = self.FREQUENCY_MAP[frequency]
            else:
                raise ValueError(f"Unsupported wound type: {wound}")
        
        # Get color palette
        self.colors = self.COLOR_PALETTES[self.wound]
        
        # Calculate procedural variations based on solver_id
        self.variations = self._calculate_variations()
    
    def _calculate_variations(self) -> Dict[str, float]:
        """
        Calculate procedural variations based on solver ID.
        
        Uses hash-based deterministic generation to ensure consistency
        for the same solver_id.
        
        Returns:
            Dictionary containing variation parameters
        """
        # Create hash from solver_id
        hash_obj = hashlib.sha256(self.solver_id.encode())
        hash_bytes = hash_obj.digest()
        
        # Extract variation parameters from hash
        # Use different bytes for different parameters
        rotation_offset = (hash_bytes[0] / 255.0) * 360  # 0-360 degrees
        layer_count = 3 + (hash_bytes[1] % 5)  # 3-7 layers
        ray_count = 6 + (hash_bytes[2] % 7)  # 6-12 rays
        line_weight = 1 + (hash_bytes[3] % 5)  # 1-5 pixels
        scale_factor = 0.7 + (hash_bytes[4] / 255.0) * 0.6  # 0.7-1.3
        
        return {
            "rotation_offset": rotation_offset,
            "layer_count": int(layer_count),
            "ray_count": int(ray_count),
            "line_weight": int(line_weight),
            "scale_factor": scale_factor
        }
    
    def _draw_root_geometry(self, draw: ImageDraw.ImageDraw, 
                           center: Tuple[int, int], size: int):
        """
        Draw root chakra geometry (square-based with grounding elements).
        
        Args:
            draw: PIL ImageDraw object
            center: Center point (x, y)
            size: Size of the geometry
        """
        cx, cy = center
        scale = size * self.variations["scale_factor"]
        rotation = self.variations["rotation_offset"]
        
        # Draw concentric squares with rotation
        for i in range(self.variations["layer_count"]):
            layer_size = scale * (1 - i * 0.2)
            angle_offset = rotation + (i * 15)
            
            # Calculate square corners with rotation
            points = []
            for j in range(4):
                angle = math.radians(angle_offset + j * 90)
                x = cx + layer_size * math.cos(angle)
                y = cy + layer_size * math.sin(angle)
                points.append((x, y))
            
            # Choose color based on layer
            if i == 0:
                color = self.colors["primary"]
            elif i % 2 == 0:
                color = self.colors["secondary"]
            else:
                color = self.colors["accent"]
            
            # Draw the square
            draw.polygon(points, outline=color, 
                        width=self.variations["line_weight"])
        
        # Draw grounding rays
        for i in range(self.variations["ray_count"]):
            angle = math.radians(rotation + (360 / self.variations["ray_count"]) * i)
            x_end = cx + scale * 1.3 * math.cos(angle)
            y_end = cy + scale * 1.3 * math.sin(angle)
            draw.line([(cx, cy), (x_end, y_end)], 
                     fill=self.colors["accent"], 
                     width=self.variations["line_weight"])
    
    def _draw_sacral_geometry(self, draw: ImageDraw.ImageDraw,
                             center: Tuple[int, int], size: int):
        """
        Draw sacral chakra geometry (circular with flowing elements).
        
        Args:
            draw: PIL ImageDraw object
            center: Center point (x, y)
            size: Size of the geometry
        """
        cx, cy = center
        scale = size * self.variations["scale_factor"]
        rotation = self.variations["rotation_offset"]
        
        # Draw concentric circles
        for i in range(self.variations["layer_count"]):
            radius = scale * (1 - i * 0.18)
            
            # Choose color based on layer
            if i == 0:
                color = self.colors["primary"]
            elif i % 2 == 0:
                color = self.colors["secondary"]
            else:
                color = self.colors["accent"]
            
            # Draw circle
            bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
            draw.ellipse(bbox, outline=color, 
                        width=self.variations["line_weight"])
        
        # Draw flowing curves (crescent moon shapes)
        for i in range(self.variations["ray_count"]):
            angle = math.radians(rotation + (360 / self.variations["ray_count"]) * i)
            
            # Create crescent shape with arc
            x_offset = scale * 0.8 * math.cos(angle)
            y_offset = scale * 0.8 * math.sin(angle)
            
            curve_x = cx + x_offset
            curve_y = cy + y_offset
            curve_radius = scale * 0.3
            
            bbox = [curve_x - curve_radius, curve_y - curve_radius,
                   curve_x + curve_radius, curve_y + curve_radius]
            
            draw.arc(bbox, start=angle * 180 / math.pi, 
                    end=angle * 180 / math.pi + 180,
                    fill=self.colors["accent"], 
                    width=self.variations["line_weight"])
    
    def _draw_solar_plexus_geometry(self, draw: ImageDraw.ImageDraw,
                                    center: Tuple[int, int], size: int):
        """
        Draw solar plexus chakra geometry (triangular with radiating elements).
        
        Args:
            draw: PIL ImageDraw object
            center: Center point (x, y)
            size: Size of the geometry
        """
        cx, cy = center
        scale = size * self.variations["scale_factor"]
        rotation = self.variations["rotation_offset"]
        
        # Draw concentric triangles
        for i in range(self.variations["layer_count"]):
            layer_size = scale * (1 - i * 0.2)
            angle_offset = rotation + (i * 20)
            
            # Calculate triangle corners
            points = []
            for j in range(3):
                angle = math.radians(angle_offset + j * 120)
                x = cx + layer_size * math.cos(angle)
                y = cy + layer_size * math.sin(angle)
                points.append((x, y))
            
            # Choose color based on layer
            if i == 0:
                color = self.colors["primary"]
            elif i % 2 == 0:
                color = self.colors["secondary"]
            else:
                color = self.colors["accent"]
            
            # Draw the triangle
            draw.polygon(points, outline=color, 
                        width=self.variations["line_weight"])
        
        # Draw radiating sunburst rays
        for i in range(self.variations["ray_count"] * 2):  # More rays for solar
            angle = math.radians(rotation + (360 / (self.variations["ray_count"] * 2)) * i)
            
            # Alternate ray lengths
            if i % 2 == 0:
                ray_length = scale * 1.4
                color = self.colors["primary"]
            else:
                ray_length = scale * 1.1
                color = self.colors["accent"]
            
            x_end = cx + ray_length * math.cos(angle)
            y_end = cy + ray_length * math.sin(angle)
            draw.line([(cx, cy), (x_end, y_end)], 
                     fill=color, 
                     width=self.variations["line_weight"])
    
    def generate(self, output_path: str, image_size: int = 512) -> str:
        """
        Generate and save the sigil image.
        
        Args:
            output_path: Path where the sigil image will be saved
            image_size: Size of the output image in pixels (default: 512)
        
        Returns:
            Path to the generated sigil image
        """
        # Create output directory if it doesn't exist
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create image with background
        image = Image.new('RGB', (image_size, image_size), 
                         color=self.colors["background"])
        draw = ImageDraw.Draw(image)
        
        # Calculate center and size
        center = (image_size // 2, image_size // 2)
        geometry_size = image_size // 3
        
        # Draw appropriate geometry based on wound type
        if self.wound == "root":
            self._draw_root_geometry(draw, center, geometry_size)
        elif self.wound == "sacral":
            self._draw_sacral_geometry(draw, center, geometry_size)
        elif self.wound == "solar_plexus":
            self._draw_solar_plexus_geometry(draw, center, geometry_size)
        else:
            # Default to a simple mandala pattern for other wound types
            for i in range(self.variations["layer_count"]):
                radius = geometry_size * (1 - i * 0.2)
                color = self.colors["primary"] if i % 2 == 0 else self.colors["secondary"]
                bbox = [center[0] - radius, center[1] - radius,
                       center[0] + radius, center[1] + radius]
                draw.ellipse(bbox, outline=color, 
                           width=self.variations["line_weight"])
        
        # Save the image
        image.save(str(output_file))
        return str(output_file)
