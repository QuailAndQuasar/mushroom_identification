#!/usr/bin/env python3
"""
AI-Enhanced Spore Analysis Module

This module adds AI capabilities to the existing spore analysis system.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import logging
from PIL import Image
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AISporeAnalyzer:
    """AI-enhanced spore analysis capabilities"""
    
    def __init__(self, spore_database_path: str = "data/spore_database.json"):
        """Initialize AI spore analyzer"""
        self.logger = logging.getLogger(__name__)
        self.spore_database_path = Path(spore_database_path)
        self.spore_database = self._load_spore_database()
        
        # AI models (placeholder - would be loaded from trained models)
        self.image_classifier = None
        self.nlp_classifier = None
        self.pattern_recognizer = None
        
        self.logger.info("🤖 AI Spore Analyzer initialized")
    
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
    
    def analyze_spore_image(self, image_path: str) -> Dict[str, Any]:
        """AI-powered spore image analysis"""
        self.logger.info(f"🔬 Analyzing spore image: {image_path}")
        
        try:
            # Load and preprocess image
            image = Image.open(image_path)
            processed_image = self._preprocess_image(image)
            
            # AI analysis (placeholder - would use actual ML model)
            analysis_result = self._ai_image_analysis(processed_image)
            
            return {
                "species_predictions": analysis_result["predictions"],
                "confidence": analysis_result["confidence"],
                "visual_features": analysis_result["features"],
                "analysis_method": "AI Computer Vision"
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error analyzing spore image: {e}")
            return {"error": str(e)}
    
    def analyze_text_description(self, description: str) -> Dict[str, Any]:
        """AI-powered text description analysis"""
        self.logger.info(f"📝 Analyzing text description: {description[:50]}...")
        
        try:
            # Extract features from text using NLP
            extracted_features = self._extract_features_from_text(description)
            
            # AI classification
            classification_result = self._ai_text_classification(extracted_features)
            
            return {
                "species_prediction": classification_result["species"],
                "confidence": classification_result["confidence"],
                "extracted_features": extracted_features,
                "analysis_method": "AI Natural Language Processing"
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error analyzing text description: {e}")
            return {"error": str(e)}
    
    def intelligent_feature_suggestion(self, current_features: Dict[str, Any]) -> Dict[str, Any]:
        """AI-powered feature suggestion system"""
        self.logger.info("🎯 Generating intelligent feature suggestions")
        
        try:
            # Analyze current confidence level
            confidence_level = self._calculate_current_confidence(current_features)
            
            # Generate suggestions based on confidence and missing features
            suggestions = self._generate_ai_suggestions(current_features, confidence_level)
            
            return {
                "current_confidence": confidence_level,
                "suggestions": suggestions,
                "next_steps": self._recommend_next_steps(confidence_level),
                "analysis_method": "AI Recommendation System"
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error generating suggestions: {e}")
            return {"error": str(e)}
    
    def pattern_recognition_analysis(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """AI-powered pattern recognition for complex relationships"""
        self.logger.info("🔍 Performing AI pattern recognition analysis")
        
        try:
            # Convert features to numerical representation
            feature_vector = self._features_to_vector(features)
            
            # AI pattern recognition
            patterns = self._recognize_patterns(feature_vector)
            
            # Find similar species based on patterns
            similar_species = self._find_similar_species(patterns)
            
            return {
                "detected_patterns": patterns,
                "similar_species": similar_species,
                "pattern_confidence": patterns["confidence"],
                "analysis_method": "AI Pattern Recognition"
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error in pattern recognition: {e}")
            return {"error": str(e)}
    
    def comprehensive_ai_analysis(self, 
                                image_path: Optional[str] = None,
                                text_description: Optional[str] = None,
                                manual_features: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Comprehensive AI analysis combining multiple methods"""
        self.logger.info("🤖 Performing comprehensive AI analysis")
        
        results = {
            "image_analysis": None,
            "text_analysis": None,
            "pattern_analysis": None,
            "feature_suggestions": None,
            "combined_prediction": None
        }
        
        try:
            # Image analysis if provided
            if image_path:
                results["image_analysis"] = self.analyze_spore_image(image_path)
            
            # Text analysis if provided
            if text_description:
                results["text_analysis"] = self.analyze_text_description(text_description)
            
            # Pattern analysis if manual features provided
            if manual_features:
                results["pattern_analysis"] = self.pattern_recognition_analysis(manual_features)
                results["feature_suggestions"] = self.intelligent_feature_suggestion(manual_features)
            
            # Combine all results for final prediction
            results["combined_prediction"] = self._combine_ai_results(results)
            
            return results
            
        except Exception as e:
            self.logger.error(f"❌ Error in comprehensive AI analysis: {e}")
            return {"error": str(e)}
    
    def _preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess image for AI analysis"""
        # Resize to standard size
        image = image.resize((224, 224))
        
        # Convert to numpy array
        image_array = np.array(image)
        
        # Normalize pixel values
        image_array = image_array.astype(np.float32) / 255.0
        
        return image_array
    
    def _ai_image_analysis(self, image_array: np.ndarray) -> Dict[str, Any]:
        """AI analysis of spore image (placeholder implementation)"""
        # This would use a trained CNN model in practice
        # For now, return mock results
        
        mock_predictions = [
            {"species": "Amanita phalloides", "confidence": 0.85},
            {"species": "Agaricus bisporus", "confidence": 0.12},
            {"species": "Pleurotus ostreatus", "confidence": 0.03}
        ]
        
        return {
            "predictions": mock_predictions,
            "confidence": max([p["confidence"] for p in mock_predictions]),
            "features": {
                "spore_density": "high",
                "spore_distribution": "uniform",
                "color_consistency": "high"
            }
        }
    
    def _extract_features_from_text(self, description: str) -> Dict[str, Any]:
        """Extract features from text description using NLP"""
        # Simple keyword extraction (would use more sophisticated NLP in practice)
        keywords = {
            "white": "spore_print_color",
            "brown": "spore_print_color", 
            "black": "spore_print_color",
            "globose": "spore_shape",
            "ellipsoid": "spore_shape",
            "cylindrical": "spore_shape",
            "smooth": "spore_surface",
            "ornamented": "spore_surface",
            "4-spored": "basidia",
            "2-spored": "basidia"
        }
        
        extracted = {}
        description_lower = description.lower()
        
        for keyword, feature_type in keywords.items():
            if keyword in description_lower:
                extracted[feature_type] = keyword
        
        return extracted
    
    def _ai_text_classification(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """AI classification based on extracted features"""
        # Mock implementation - would use trained NLP model
        return {
            "species": "Amanita phalloides",
            "confidence": 0.78,
            "reasoning": "White spore print and globose shape match Death Cap characteristics"
        }
    
    def _calculate_current_confidence(self, features: Dict[str, Any]) -> float:
        """Calculate current confidence level"""
        # Simple confidence calculation based on number of features
        feature_count = len(features)
        max_features = 10  # Maximum possible features
        
        return min(feature_count / max_features, 1.0)
    
    def _generate_ai_suggestions(self, features: Dict[str, Any], confidence: float) -> List[str]:
        """Generate AI-powered suggestions"""
        suggestions = []
        
        if confidence < 0.3:
            suggestions.extend([
                "Take a spore print to determine spore color",
                "Examine spores under microscope for size and shape",
                "Check for microscopic features like cystidia"
            ])
        elif confidence < 0.7:
            suggestions.extend([
                "Verify spore measurements with calibrated microscope",
                "Check for additional microscopic features",
                "Compare with known species in database"
            ])
        else:
            suggestions.append("Analysis appears complete - high confidence identification")
        
        return suggestions
    
    def _recommend_next_steps(self, confidence: float) -> List[str]:
        """Recommend next steps based on confidence level"""
        if confidence < 0.5:
            return ["Collect more data", "Use additional identification methods"]
        elif confidence < 0.8:
            return ["Verify findings", "Cross-reference with field guides"]
        else:
            return ["Confident identification", "Document findings"]
    
    def _features_to_vector(self, features: Dict[str, Any]) -> np.ndarray:
        """Convert features to numerical vector for AI analysis"""
        # Simple one-hot encoding (would be more sophisticated in practice)
        feature_vector = np.zeros(20)  # 20-dimensional feature space
        
        feature_mapping = {
            "spore_print_color": {"white": 0, "brown": 1, "black": 2},
            "spore_shape": {"globose": 3, "ellipsoid": 4, "cylindrical": 5},
            "spore_surface": {"smooth": 6, "ornamented": 7},
            "basidia": {"4-spored": 8, "2-spored": 9}
        }
        
        for feature_type, value in features.items():
            if feature_type in feature_mapping and value in feature_mapping[feature_type]:
                idx = feature_mapping[feature_type][value]
                feature_vector[idx] = 1
        
        return feature_vector
    
    def _recognize_patterns(self, feature_vector: np.ndarray) -> Dict[str, Any]:
        """AI pattern recognition (placeholder implementation)"""
        # Mock pattern recognition
        return {
            "pattern_type": "amanita_pattern",
            "confidence": 0.82,
            "characteristics": ["white_spores", "globose_shape", "smooth_surface"]
        }
    
    def _find_similar_species(self, patterns: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find similar species based on patterns"""
        # Mock similar species finding
        return [
            {"species": "Amanita phalloides", "similarity": 0.95},
            {"species": "Amanita muscaria", "similarity": 0.78},
            {"species": "Amanita pantherina", "similarity": 0.65}
        ]
    
    def _combine_ai_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Combine results from multiple AI methods"""
        predictions = []
        confidences = []
        
        # Collect predictions from all methods
        if results["image_analysis"]:
            predictions.append(results["image_analysis"]["species_predictions"][0])
            confidences.append(results["image_analysis"]["confidence"])
        
        if results["text_analysis"]:
            predictions.append({
                "species": results["text_analysis"]["species_prediction"],
                "confidence": results["text_analysis"]["confidence"]
            })
            confidences.append(results["text_analysis"]["confidence"])
        
        if results["pattern_analysis"]:
            # Use pattern analysis to weight other results
            pattern_confidence = results["pattern_analysis"]["pattern_confidence"]
            for pred in predictions:
                pred["confidence"] *= pattern_confidence
        
        # Find best combined prediction
        if predictions:
            best_prediction = max(predictions, key=lambda x: x["confidence"])
            return {
                "species": best_prediction["species"],
                "confidence": best_prediction["confidence"],
                "method": "AI Combined Analysis",
                "supporting_evidence": len(predictions)
            }
        
        return {"error": "No predictions available"}

def main():
    """Demonstrate AI-enhanced spore analysis"""
    print("🤖 AI-ENHANCED SPORE ANALYSIS DEMONSTRATION")
    print("=" * 60)
    
    # Initialize AI analyzer
    ai_analyzer = AISporeAnalyzer()
    
    # Example 1: Text description analysis
    print("\n📝 Example 1: AI Text Analysis")
    print("-" * 40)
    description = "White spore print, globose spores 8-10 μm, smooth surface, 4-spored basidia"
    result = ai_analyzer.analyze_text_description(description)
    print(f"Description: {description}")
    print(f"AI Prediction: {result['species_prediction']}")
    print(f"Confidence: {result['confidence']:.2f}")
    print(f"Method: {result['analysis_method']}")
    
    # Example 2: Feature suggestion
    print("\n🎯 Example 2: AI Feature Suggestions")
    print("-" * 40)
    current_features = {
        "spore_print_color": "white",
        "spore_shape": "globose"
    }
    suggestions = ai_analyzer.intelligent_feature_suggestion(current_features)
    print(f"Current features: {current_features}")
    print(f"Current confidence: {suggestions['current_confidence']:.2f}")
    print("AI Suggestions:")
    for suggestion in suggestions['suggestions']:
        print(f"  - {suggestion}")
    
    # Example 3: Pattern recognition
    print("\n🔍 Example 3: AI Pattern Recognition")
    print("-" * 40)
    features = {
        "spore_print_color": "white",
        "spore_shape": "globose",
        "spore_surface": "smooth",
        "basidia": "4-spored"
    }
    patterns = ai_analyzer.pattern_recognition_analysis(features)
    print(f"Features: {features}")
    print(f"Detected pattern: {patterns['detected_patterns']['pattern_type']}")
    print(f"Pattern confidence: {patterns['detected_patterns']['confidence']:.2f}")
    print("Similar species:")
    for species in patterns['similar_species']:
        print(f"  - {species['species']}: {species['similarity']:.2f}")
    
    print("\n🚀 AI Enhancement Benefits:")
    print("  - Computer vision for spore image analysis")
    print("  - Natural language processing for descriptions")
    print("  - Pattern recognition for complex relationships")
    print("  - Intelligent suggestions for better identification")
    print("  - Combined analysis for higher accuracy")

if __name__ == "__main__":
    main()
