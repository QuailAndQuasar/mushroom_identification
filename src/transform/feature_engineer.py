"""
Feature engineering transformer for creating ML-ready features.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.compose import ColumnTransformer
from .base_transformer import BaseTransformer

class FeatureEngineer(BaseTransformer):
    """Transformer for feature engineering and ML preparation."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize feature engineer.
        
        Args:
            config: Configuration dictionary
        """
        default_config = {
            "target_column": "class",  # Target variable column
            "categorical_encoding": "onehot",  # onehot, label, target
            "feature_scaling": True,  # Apply feature scaling
            "feature_selection": True,  # Apply feature selection
            "n_features": 20,  # Number of features to select
            "create_interactions": False,  # Create feature interactions
            "handle_imbalanced": False,  # Handle class imbalance
        }
        
        if config:
            default_config.update(config)
        
        super().__init__(
            name="feature_engineer",
            config=default_config
        )
        
        # Initialize encoders and scalers
        self.label_encoders = {}
        self.onehot_encoder = None
        self.scaler = None
        self.feature_selector = None
        self.feature_names = []
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer features for machine learning.
        
        Args:
            data: Input DataFrame
            
        Returns:
            Feature-engineered DataFrame
        """
        self.logger.info(f"Starting feature engineering for {len(data)} records")
        
        # Store original stats
        self.stats["original_shape"] = data.shape
        self.stats["original_columns"] = list(data.columns)
        
        # Start with a copy
        engineered_data = data.copy()
        
        # Separate target and features
        if self.config["target_column"] in engineered_data.columns:
            target = engineered_data[self.config["target_column"]]
            features = engineered_data.drop(columns=[self.config["target_column"]])
        else:
            self.logger.warning(f"Target column '{self.config['target_column']}' not found")
            target = None
            features = engineered_data
        
        # Encode categorical variables
        features = self._encode_categorical(features)
        
        # Create feature interactions
        if self.config["create_interactions"]:
            features = self._create_interactions(features)
        
        # Scale features
        if self.config["feature_scaling"]:
            features = self._scale_features(features)
        
        # Select features
        if self.config["feature_selection"] and target is not None:
            features = self._select_features(features, target)
        
        # Combine features and target
        if target is not None:
            engineered_data = pd.concat([features, target], axis=1)
        else:
            engineered_data = features
        
        # Update stats
        self.stats["final_shape"] = engineered_data.shape
        self.stats["feature_count"] = len(features.columns)
        self.stats["feature_names"] = list(features.columns)
        
        self.logger.info(f"Feature engineering completed: {self.stats['feature_count']} features")
        return engineered_data
    
    def _encode_categorical(self, data: pd.DataFrame) -> pd.DataFrame:
        """Encode categorical variables."""
        categorical_cols = data.select_dtypes(include=['object']).columns
        
        if len(categorical_cols) == 0:
            self.logger.info("No categorical columns found")
            return data
        
        self.logger.info(f"Encoding {len(categorical_cols)} categorical columns")
        
        if self.config["categorical_encoding"] == "onehot":
            # One-hot encoding
            encoded_data = pd.get_dummies(data, columns=categorical_cols, prefix=categorical_cols)
            self.stats["onehot_columns"] = len(encoded_data.columns) - len(data.columns)
            
        elif self.config["categorical_encoding"] == "label":
            # Label encoding
            encoded_data = data.copy()
            for col in categorical_cols:
                le = LabelEncoder()
                encoded_data[col] = le.fit_transform(encoded_data[col].astype(str))
                self.label_encoders[col] = le
            self.stats["label_encoded_columns"] = len(categorical_cols)
            
        elif self.config["categorical_encoding"] == "target":
            # Target encoding (mean encoding)
            encoded_data = data.copy()
            for col in categorical_cols:
                # This would require target variable - simplified for now
                encoded_data[col] = encoded_data[col].astype('category').cat.codes
            self.stats["target_encoded_columns"] = len(categorical_cols)
        
        return encoded_data
    
    def _create_interactions(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create feature interactions."""
        self.logger.info("Creating feature interactions")
        
        # Select numeric columns for interactions
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            self.logger.warning("Not enough numeric columns for interactions")
            return data
        
        # Create pairwise interactions
        interaction_data = data.copy()
        interaction_count = 0
        
        for i, col1 in enumerate(numeric_cols):
            for col2 in numeric_cols[i+1:]:
                interaction_name = f"{col1}_x_{col2}"
                interaction_data[interaction_name] = data[col1] * data[col2]
                interaction_count += 1
                
                # Limit interactions to prevent explosion
                if interaction_count >= 10:
                    break
            if interaction_count >= 10:
                break
        
        self.stats["interactions_created"] = interaction_count
        self.logger.info(f"Created {interaction_count} feature interactions")
        return interaction_data
    
    def _scale_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Scale features for machine learning."""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            self.logger.info("No numeric columns to scale")
            return data
        
        self.logger.info(f"Scaling {len(numeric_cols)} numeric columns")
        
        # Standard scaling
        self.scaler = StandardScaler()
        scaled_data = data.copy()
        scaled_data[numeric_cols] = self.scaler.fit_transform(data[numeric_cols])
        
        self.stats["scaled_columns"] = len(numeric_cols)
        return scaled_data
    
    def _select_features(self, data: pd.DataFrame, target: pd.Series) -> pd.DataFrame:
        """Select the most important features."""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            self.logger.info("No numeric columns for feature selection")
            return data
        
        n_features = min(self.config["n_features"], len(numeric_cols))
        self.logger.info(f"Selecting {n_features} features from {len(numeric_cols)} candidates")
        
        # Use mutual information for feature selection
        self.feature_selector = SelectKBest(
            score_func=mutual_info_classif,
            k=n_features
        )
        
        selected_data = data.copy()
        selected_features = self.feature_selector.fit_transform(data[numeric_cols], target)
        selected_columns = numeric_cols[self.feature_selector.get_support()]
        
        # Keep only selected features
        selected_data = selected_data[selected_columns]
        
        self.stats["selected_features"] = len(selected_columns)
        self.stats["feature_scores"] = dict(zip(selected_columns, self.feature_selector.scores_))
        
        self.logger.info(f"Selected {len(selected_columns)} features")
        return selected_data
    
    def validate(self, data: pd.DataFrame) -> bool:
        """
        Validate engineered features.
        
        Args:
            data: Engineered DataFrame
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check if data is empty
            if data.empty:
                self.logger.error("Engineered data is empty")
                return False
            
            # Check for infinite values
            if np.isinf(data.select_dtypes(include=[np.number])).any().any():
                self.logger.warning("Found infinite values in engineered data")
            
            # Check for NaN values
            nan_count = data.isnull().sum().sum()
            if nan_count > 0:
                self.logger.warning(f"Found {nan_count} NaN values in engineered data")
            
            # Check feature count
            if len(data.columns) == 0:
                self.logger.error("No features remaining after engineering")
                return False
            
            self.logger.info("Feature engineering validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return False
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance scores.
        
        Returns:
            Dictionary of feature importance scores
        """
        if hasattr(self, 'feature_selector') and self.feature_selector is not None:
            return self.stats.get("feature_scores", {})
        return {}
    
    def get_engineered_features(self) -> List[str]:
        """
        Get list of engineered feature names.
        
        Returns:
            List of feature names
        """
        return self.stats.get("feature_names", [])