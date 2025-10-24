#!/usr/bin/env python3
"""
Spore Analysis Module for Mushroom Identification

This module provides spore analysis capabilities for enhanced mushroom identification.
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SporeCharacteristics:
    """Data class for spore characteristics"""
    spore_print_color: str
    spore_shape: str
    spore_size: str
    spore_surface: str
    spore_wall_thickness: str
    spore_ornamentation: str

@dataclass
class MicroscopicFeatures:
    """Data class for microscopic features"""
    basidia: str
    cheilocystidia: str
    pleurocystidia: str
    pileipellis: str

class SporeAnalyzer:
    """Spore analysis for mushroom identification"""
    
    def __init__(self, spore_database_path: str = "data/spore_database.json"):
        """Initialize spore analyzer with database"""
        self.logger = logging.getLogger(__name__)
        self.spore_database_path = Path(spore_database_path)
        self.spore_database = self._load_spore_database()
    
    def _load_spore_database(self) -> List[Dict[str, Any]]:
        """Load spore database from JSON file"""
        try:
            with open(self.spore_database_path, 'r') as f:
                database = json.load(f)
            self.logger.info(f"✅ Loaded {len(database)} species from spore database")
            return database
        except FileNotFoundError:
            self.logger.error(f"❌ Spore database not found at {self.spore_database_path}")
            return []
        except json.JSONDecodeError as e:
            self.logger.error(f"❌ Error parsing spore database: {e}")
            return []
    
    def analyze_spore_print(self, spore_print_color: str) -> List[Dict[str, Any]]:
        """Analyze spore print color and return matching species"""
        self.logger.info(f"🔬 Analyzing spore print color: {spore_print_color}")
        
        matches = []
        for species in self.spore_database:
            if species["spore_characteristics"]["spore_print_color"] == spore_print_color:
                matches.append({
                    "species": species["species"],
                    "common_name": species["common_name"],
                    "confidence": 0.8,  # High confidence for spore print match
                    "match_type": "spore_print_color"
                })
        
        self.logger.info(f"📊 Found {len(matches)} species with {spore_print_color} spore print")
        return matches
    
    def analyze_spore_morphology(self, 
                               spore_shape: str, 
                               spore_size: str, 
                               spore_surface: str) -> List[Dict[str, Any]]:
        """Analyze spore morphology and return matching species"""
        self.logger.info(f"🔬 Analyzing spore morphology: {spore_shape}, {spore_size}, {spore_surface}")
        
        matches = []
        for species in self.spore_database:
            characteristics = species["spore_characteristics"]
            
            # Calculate match score based on morphology
            score = 0
            if characteristics["spore_shape"] == spore_shape:
                score += 0.4
            if characteristics["spore_size"] == spore_size:
                score += 0.3
            if characteristics["spore_surface"] == spore_surface:
                score += 0.3
            
            if score > 0.5:  # Minimum threshold for match
                matches.append({
                    "species": species["species"],
                    "common_name": species["common_name"],
                    "confidence": score,
                    "match_type": "spore_morphology"
                })
        
        # Sort by confidence score
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        
        self.logger.info(f"📊 Found {len(matches)} species with matching morphology")
        return matches
    
    def analyze_microscopic_features(self, 
                                   basidia: str, 
                                   cheilocystidia: str, 
                                   pleurocystidia: str) -> List[Dict[str, Any]]:
        """Analyze microscopic features and return matching species"""
        self.logger.info(f"🔬 Analyzing microscopic features: {basidia}, {cheilocystidia}, {pleurocystidia}")
        
        matches = []
        for species in self.spore_database:
            features = species["microscopic_features"]
            
            # Calculate match score based on microscopic features
            score = 0
            if features["basidia"] == basidia:
                score += 0.4
            if features["cheilocystidia"] == cheilocystidia:
                score += 0.3
            if features["pleurocystidia"] == pleurocystidia:
                score += 0.3
            
            if score > 0.5:  # Minimum threshold for match
                matches.append({
                    "species": species["species"],
                    "common_name": species["common_name"],
                    "confidence": score,
                    "match_type": "microscopic_features"
                })
        
        # Sort by confidence score
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        
        self.logger.info(f"📊 Found {len(matches)} species with matching microscopic features")
        return matches
    
    def comprehensive_spore_analysis(self, 
                                  spore_print_color: str,
                                  spore_shape: str,
                                  spore_size: str,
                                  spore_surface: str,
                                  basidia: str,
                                  cheilocystidia: str,
                                  pleurocystidia: str) -> Dict[str, Any]:
        """Perform comprehensive spore analysis"""
        self.logger.info("🔬 Performing comprehensive spore analysis")
        
        # Get matches from each analysis method
        spore_print_matches = self.analyze_spore_print(spore_print_color)
        morphology_matches = self.analyze_spore_morphology(spore_shape, spore_size, spore_surface)
        microscopic_matches = self.analyze_microscopic_features(basidia, cheilocystidia, pleurocystidia)
        
        # Combine and score matches
        all_matches = {}
        
        # Add spore print matches
        for match in spore_print_matches:
            species = match["species"]
            if species not in all_matches:
                all_matches[species] = {
                    "species": match["species"],
                    "common_name": match["common_name"],
                    "confidence": 0,
                    "match_types": [],
                    "details": {}
                }
            all_matches[species]["confidence"] += match["confidence"] * 0.4
            all_matches[species]["match_types"].append("spore_print")
            all_matches[species]["details"]["spore_print"] = match["confidence"]
        
        # Add morphology matches
        for match in morphology_matches:
            species = match["species"]
            if species not in all_matches:
                all_matches[species] = {
                    "species": match["species"],
                    "common_name": match["common_name"],
                    "confidence": 0,
                    "match_types": [],
                    "details": {}
                }
            all_matches[species]["confidence"] += match["confidence"] * 0.4
            all_matches[species]["match_types"].append("morphology")
            all_matches[species]["details"]["morphology"] = match["confidence"]
        
        # Add microscopic matches
        for match in microscopic_matches:
            species = match["species"]
            if species not in all_matches:
                all_matches[species] = {
                    "species": match["species"],
                    "common_name": match["common_name"],
                    "confidence": 0,
                    "match_types": [],
                    "details": {}
                }
            all_matches[species]["confidence"] += match["confidence"] * 0.2
            all_matches[species]["match_types"].append("microscopic")
            all_matches[species]["details"]["microscopic"] = match["confidence"]
        
        # Convert to list and sort by confidence
        final_matches = list(all_matches.values())
        final_matches.sort(key=lambda x: x["confidence"], reverse=True)
        
        # Get best match
        best_match = final_matches[0] if final_matches else None
        
        analysis_result = {
            "best_match": best_match,
            "all_matches": final_matches,
            "analysis_summary": {
                "total_species_analyzed": len(self.spore_database),
                "spore_print_matches": len(spore_print_matches),
                "morphology_matches": len(morphology_matches),
                "microscopic_matches": len(microscopic_matches),
                "final_matches": len(final_matches)
            }
        }
        
        self.logger.info(f"📊 Comprehensive analysis complete: {len(final_matches)} final matches")
        return analysis_result
    
    def get_spore_identification_key(self, species_name: str) -> Optional[List[str]]:
        """Get identification key for a specific species"""
        for species in self.spore_database:
            if species["species"] == species_name:
                return species["identification_key"]
        return None
    
    def get_species_spore_info(self, species_name: str) -> Optional[Dict[str, Any]]:
        """Get complete spore information for a species"""
        for species in self.spore_database:
            if species["species"] == species_name:
                return {
                    "spore_characteristics": species["spore_characteristics"],
                    "microscopic_features": species["microscopic_features"],
                    "identification_key": species["identification_key"]
                }
        return None
    
    def add_species_to_database(self, species_data: Dict[str, Any]) -> bool:
        """Add new species to spore database"""
        try:
            self.spore_database.append(species_data)
            
            # Save updated database
            with open(self.spore_database_path, 'w') as f:
                json.dump(self.spore_database, f, indent=2)
            
            self.logger.info(f"✅ Added {species_data['species']} to spore database")
            return True
        except Exception as e:
            self.logger.error(f"❌ Error adding species to database: {e}")
            return False
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the spore database"""
        if not self.spore_database:
            return {"error": "Database not loaded"}
        
        # Count species by spore print color
        spore_colors = {}
        for species in self.spore_database:
            color = species["spore_characteristics"]["spore_print_color"]
            spore_colors[color] = spore_colors.get(color, 0) + 1
        
        # Count species by spore shape
        spore_shapes = {}
        for species in self.spore_database:
            shape = species["spore_characteristics"]["spore_shape"]
            spore_shapes[shape] = spore_shapes.get(shape, 0) + 1
        
        return {
            "total_species": len(self.spore_database),
            "spore_colors": spore_colors,
            "spore_shapes": spore_shapes,
            "database_file": str(self.spore_database_path)
        }

def main():
    """Demonstrate spore analysis functionality"""
    print("🔬 SPORE ANALYSIS DEMONSTRATION")
    print("=" * 50)
    
    # Initialize spore analyzer
    analyzer = SporeAnalyzer()
    
    # Show database stats
    stats = analyzer.get_database_stats()
    print(f"📊 Database Statistics:")
    print(f"  Total species: {stats['total_species']}")
    print(f"  Spore colors: {stats['spore_colors']}")
    print(f"  Spore shapes: {stats['spore_shapes']}")
    print()
    
    # Example: Analyze spore print
    print("🔬 Example: Analyzing white spore print")
    white_matches = analyzer.analyze_spore_print("white")
    for match in white_matches:
        print(f"  - {match['common_name']} ({match['species']}) - {match['confidence']:.2f}")
    print()
    
    # Example: Comprehensive analysis
    print("🔬 Example: Comprehensive spore analysis")
    analysis = analyzer.comprehensive_spore_analysis(
        spore_print_color="white",
        spore_shape="globose",
        spore_size="8-10 x 7-9 μm",
        spore_surface="smooth",
        basidia="4-spored",
        cheilocystidia="absent",
        pleurocystidia="absent"
    )
    
    if analysis["best_match"]:
        best = analysis["best_match"]
        print(f"  Best match: {best['common_name']} ({best['species']})")
        print(f"  Confidence: {best['confidence']:.2f}")
        print(f"  Match types: {', '.join(best['match_types'])}")
    
    print(f"  Total matches: {len(analysis['all_matches'])}")
    print()

if __name__ == "__main__":
    main()
