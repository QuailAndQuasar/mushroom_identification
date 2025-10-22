
import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Alert,
  ActivityIndicator
} from 'react-native';

const MushroomIdentifier = () => {
  const [selectedFeatures, setSelectedFeatures] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const features = {
    'Cap Shape': {
      'b': 'Bell',
      'c': 'Conical', 
      'f': 'Flat',
      'k': 'Knobbed',
      's': 'Sunken',
      'x': 'Convex'
    },
    'Cap Surface': {
      'f': 'Fibrous',
      'g': 'Grooves',
      's': 'Smooth',
      'y': 'Scaly'
    },
    'Cap Color': {
      'b': 'Buff',
      'c': 'Cinnamon',
      'e': 'Red',
      'g': 'Gray',
      'n': 'Brown',
      'p': 'Pink',
      'r': 'Green',
      'u': 'Purple',
      'w': 'White',
      'y': 'Yellow'
    },
    'Bruises': {
      'f': 'No',
      't': 'Yes'
    },
    'Odor': {
      'a': 'Almond',
      'c': 'Creosote',
      'f': 'Foul',
      'l': 'Anise',
      'm': 'Musty',
      'n': 'None',
      'p': 'Pungent',
      's': 'Spicy',
      'y': 'Fishy'
    },
    'Gill Size': {
      'b': 'Broad',
      'n': 'Narrow'
    }
  };

  const predictMushroom = async () => {
    setLoading(true);
    try {
      const response = await fetch('https://your-api-url.com/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(selectedFeatures),
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      Alert.alert('Error', 'Failed to get prediction');
    } finally {
      setLoading(false);
    }
  };

  const FeatureSelector = ({ category, options }) => (
    <View style={styles.featureGroup}>
      <Text style={styles.featureLabel}>{category}</Text>
      <View style={styles.optionsContainer}>
        {Object.entries(options).map(([key, label]) => (
          <TouchableOpacity
            key={key}
            style={[
              styles.optionButton,
              selectedFeatures[`${category.toLowerCase().replace(' ', '-')}_${key}`] && styles.selectedOption
            ]}
            onPress={() => {
              const featureKey = `${category.toLowerCase().replace(' ', '-')}_${key}`;
              setSelectedFeatures(prev => ({
                ...prev,
                [featureKey]: !prev[featureKey]
              }));
            }}
          >
            <Text style={[
              styles.optionText,
              selectedFeatures[`${category.toLowerCase().replace(' ', '-')}_${key}`] && styles.selectedOptionText
            ]}>
              {label}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>🍄 Mushroom Identifier</Text>
      <Text style={styles.subtitle}>Identify edible vs poisonous mushrooms</Text>
      
      {Object.entries(features).map(([category, options]) => (
        <FeatureSelector key={category} category={category} options={options} />
      ))}
      
      <TouchableOpacity 
        style={styles.predictButton} 
        onPress={predictMushroom}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="white" />
        ) : (
          <Text style={styles.predictButtonText}>🔍 Identify Mushroom</Text>
        )}
      </TouchableOpacity>
      
      {result && (
        <View style={[
          styles.resultContainer,
          result.edible ? styles.edibleResult : styles.poisonousResult
        ]}>
          <Text style={styles.resultText}>
            {result.edible ? '✅ EDIBLE' : '☠️ POISONOUS'}
          </Text>
          <Text style={styles.confidenceText}>
            Confidence: {(result.confidence * 100).toFixed(1)}%
          </Text>
        </View>
      )}
      
      <View style={styles.warningContainer}>
        <Text style={styles.warningText}>
          ⚠️ This tool is for educational purposes only. 
          Never rely solely on automated identification for mushroom consumption.
        </Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 10,
    color: '#333',
  },
  subtitle: {
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 30,
    color: '#666',
  },
  featureGroup: {
    marginBottom: 20,
  },
  featureLabel: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333',
  },
  optionsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  optionButton: {
    backgroundColor: 'white',
    padding: 10,
    margin: 5,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  selectedOption: {
    backgroundColor: '#667eea',
    borderColor: '#667eea',
  },
  optionText: {
    fontSize: 14,
    color: '#333',
  },
  selectedOptionText: {
    color: 'white',
  },
  predictButton: {
    backgroundColor: '#667eea',
    padding: 15,
    borderRadius: 8,
    marginTop: 20,
    alignItems: 'center',
  },
  predictButtonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
  resultContainer: {
    padding: 20,
    borderRadius: 8,
    marginTop: 20,
    alignItems: 'center',
  },
  edibleResult: {
    backgroundColor: '#d4edda',
    borderColor: '#c3e6cb',
  },
  poisonousResult: {
    backgroundColor: '#f8d7da',
    borderColor: '#f5c6cb',
  },
  resultText: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  confidenceText: {
    fontSize: 16,
    opacity: 0.8,
  },
  warningContainer: {
    backgroundColor: '#fff3cd',
    padding: 15,
    borderRadius: 8,
    marginTop: 20,
    borderWidth: 1,
    borderColor: '#ffeaa7',
  },
  warningText: {
    color: '#856404',
    fontSize: 14,
    textAlign: 'center',
  },
});

export default MushroomIdentifier;
    