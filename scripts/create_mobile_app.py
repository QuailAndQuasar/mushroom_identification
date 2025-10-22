#!/usr/bin/env python3
"""
Create Mobile App Integration for Mushroom Identification

This script creates mobile app templates and API integration examples.
"""

from pathlib import Path

def create_react_native_app():
    """Create React Native mobile app."""
    app_js = '''
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
    '''
    
    app_file = Path("mobile_app/MushroomIdentifier.js")
    app_file.parent.mkdir(exist_ok=True)
    
    with open(app_file, 'w') as f:
        f.write(app_js)
    
    print(f"📱 React Native app created: {app_file}")
    return app_file

def create_flutter_app():
    """Create Flutter mobile app."""
    main_dart = '''
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(MushroomIdentifierApp());
}

class MushroomIdentifierApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Mushroom Identifier',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: MushroomIdentifierScreen(),
    );
  }
}

class MushroomIdentifierScreen extends StatefulWidget {
  @override
  _MushroomIdentifierScreenState createState() => _MushroomIdentifierScreenState();
}

class _MushroomIdentifierScreenState extends State<MushroomIdentifierScreen> {
  Map<String, String> selectedFeatures = {};
  Map<String, dynamic>? result;
  bool loading = false;

  final Map<String, Map<String, String>> features = {
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

  Future<void> predictMushroom() async {
    setState(() {
      loading = true;
    });

    try {
      final response = await http.post(
        Uri.parse('https://your-api-url.com/predict'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(selectedFeatures),
      );

      if (response.statusCode == 200) {
        setState(() {
          result = json.decode(response.body);
        });
      } else {
        _showErrorDialog('Failed to get prediction');
      }
    } catch (e) {
      _showErrorDialog('Error: $e');
    } finally {
      setState(() {
        loading = false;
      });
    }
  }

  void _showErrorDialog(String message) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Error'),
        content: Text(message),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('OK'),
          ),
        ],
      ),
    );
  }

  Widget _buildFeatureSelector(String category, Map<String, String> options) {
    return Card(
      margin: EdgeInsets.all(8),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              category,
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 10),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: options.entries.map((entry) {
                final featureKey = '${category.toLowerCase().replaceAll(' ', '-')}_${entry.key}';
                final isSelected = selectedFeatures[featureKey] == 'true';
                
                return FilterChip(
                  label: Text(entry.value),
                  selected: isSelected,
                  onSelected: (selected) {
                    setState(() {
                      if (selected) {
                        selectedFeatures[featureKey] = 'true';
                      } else {
                        selectedFeatures.remove(featureKey);
                      }
                    });
                  },
                );
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('🍄 Mushroom Identifier'),
        backgroundColor: Colors.blue[600],
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            Text(
              'Identify edible vs poisonous mushrooms',
              style: TextStyle(fontSize: 16, color: Colors.grey[600]),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 20),
            
            ...features.entries.map((entry) => 
              _buildFeatureSelector(entry.key, entry.value)
            ),
            
            SizedBox(height: 20),
            
            ElevatedButton(
              onPressed: loading ? null : predictMushroom,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.blue[600],
                padding: EdgeInsets.symmetric(horizontal: 32, vertical: 16),
              ),
              child: loading
                  ? CircularProgressIndicator(color: Colors.white)
                  : Text(
                      '🔍 Identify Mushroom',
                      style: TextStyle(fontSize: 18, color: Colors.white),
                    ),
            ),
            
            if (result != null) ...[
              SizedBox(height: 20),
              Card(
                color: result!['edible'] ? Colors.green[100] : Colors.red[100],
                child: Padding(
                  padding: EdgeInsets.all(16),
                  child: Column(
                    children: [
                      Text(
                        result!['edible'] ? '✅ EDIBLE' : '☠️ POISONOUS',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: result!['edible'] ? Colors.green[800] : Colors.red[800],
                        ),
                      ),
                      SizedBox(height: 8),
                      Text(
                        'Confidence: ${(result!['confidence'] * 100).toStringAsFixed(1)}%',
                        style: TextStyle(fontSize: 16),
                      ),
                    ],
                  ),
                ),
              ),
            ],
            
            SizedBox(height: 20),
            Card(
              color: Colors.orange[100],
              child: Padding(
                padding: EdgeInsets.all(16),
                child: Text(
                  '⚠️ This tool is for educational purposes only. '
                  'Never rely solely on automated identification for mushroom consumption.',
                  style: TextStyle(color: Colors.orange[800]),
                  textAlign: TextAlign.center,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
    '''
    
    main_file = Path("mobile_app/lib/main.dart")
    main_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(main_file, 'w') as f:
        f.write(main_dart)
    
    print(f"📱 Flutter app created: {main_file}")
    return main_file

def create_pubspec():
    """Create pubspec.yaml for Flutter."""
    pubspec = '''
name: mushroom_identifier
description: A Flutter app for mushroom identification

version: 1.0.0+1

environment:
  sdk: '>=2.17.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  http: ^0.13.5
  cupertino_icons: ^1.0.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true
    '''
    
    pubspec_file = Path("mobile_app/pubspec.yaml")
    with open(pubspec_file, 'w') as f:
        f.write(pubspec)
    
    print(f"📦 Flutter pubspec created: {pubspec_file}")

def create_package_json():
    """Create package.json for React Native."""
    package_json = '''
{
  "name": "MushroomIdentifier",
  "version": "1.0.0",
  "description": "A React Native app for mushroom identification",
  "main": "index.js",
  "scripts": {
    "android": "react-native run-android",
    "ios": "react-native run-ios",
    "start": "react-native start",
    "test": "jest"
  },
  "dependencies": {
    "react": "18.2.0",
    "react-native": "0.72.0"
  },
  "devDependencies": {
    "@babel/core": "^7.20.0",
    "@babel/preset-env": "^7.20.0",
    "@babel/runtime": "^7.20.0",
    "@react-native/eslint-config": "^0.72.0",
    "@react-native/metro-config": "^0.72.0",
    "@tsconfig/react-native": "^3.0.0",
    "@types/react": "^18.0.24",
    "@types/react-test-renderer": "^18.0.0",
    "babel-jest": "^29.2.1",
    "eslint": "^8.19.0",
    "jest": "^29.2.1",
    "metro-react-native-babel-preset": "0.76.5",
    "prettier": "^2.4.1",
    "react-test-renderer": "18.2.0",
    "typescript": "4.8.4"
  },
  "engines": {
    "node": ">=16"
  }
}
    '''
    
    package_file = Path("mobile_app/package.json")
    with open(package_file, 'w') as f:
        f.write(package_json)
    
    print(f"📦 React Native package.json created: {package_file}")

def create_deployment_scripts():
    """Create deployment scripts for mobile apps."""
    deploy_script = '''#!/bin/bash
# Mobile App Deployment Script

echo "📱 Deploying Mushroom Identifier Mobile Apps"
echo "============================================="

# React Native Deployment
echo "🚀 Deploying React Native App..."
cd mobile_app
npm install
npx react-native run-android  # For Android
# npx react-native run-ios    # For iOS

# Flutter Deployment
echo "🚀 Deploying Flutter App..."
cd ../mobile_app
flutter pub get
flutter build apk  # For Android
# flutter build ios  # For iOS

echo "✅ Mobile apps deployed successfully!"
echo ""
echo "📱 Next steps:"
echo "1. Test on physical devices"
echo "2. Deploy to app stores (Google Play, Apple App Store)"
echo "3. Set up CI/CD pipelines"
echo "4. Add push notifications"
echo "5. Implement offline functionality"
    '''
    
    deploy_file = Path("deploy_mobile.sh")
    with open(deploy_file, 'w') as f:
        f.write(deploy_script)
    
    deploy_file.chmod(0o755)  # Make executable
    print(f"🚀 Deployment script created: {deploy_file}")

def create_api_integration_guide():
    """Create API integration guide."""
    guide = '''
# 📱 Mobile App API Integration Guide

## React Native Integration

### 1. Install Dependencies
```bash
npm install react-native
npm install @react-native-async-storage/async-storage
```

### 2. API Service
```javascript
// services/mushroomAPI.js
const API_BASE_URL = 'https://your-api-url.com';

export const predictMushroom = async (features) => {
  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(features),
    });
    
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};
```

### 3. Offline Support
```javascript
// utils/offlineStorage.js
import AsyncStorage from '@react-native-async-storage/async-storage';

export const savePrediction = async (features, result) => {
  try {
    const predictions = await AsyncStorage.getItem('predictions') || '[]';
    const parsed = JSON.parse(predictions);
    parsed.push({ features, result, timestamp: Date.now() });
    await AsyncStorage.setItem('predictions', JSON.stringify(parsed));
  } catch (error) {
    console.error('Save error:', error);
  }
};
```

## Flutter Integration

### 1. Dependencies
```yaml
dependencies:
  http: ^0.13.5
  shared_preferences: ^2.0.15
  connectivity_plus: ^4.0.1
```

### 2. API Service
```dart
// services/mushroom_service.dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class MushroomService {
  static const String baseUrl = 'https://your-api-url.com';
  
  static Future<Map<String, dynamic>> predictMushroom(
    Map<String, dynamic> features
  ) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/predict'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(features),
      );
      
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to load prediction');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }
}
```

### 3. Offline Support
```dart
// services/offline_service.dart
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';

class OfflineService {
  static Future<void> savePrediction(
    Map<String, dynamic> features,
    Map<String, dynamic> result
  ) async {
    final prefs = await SharedPreferences.getInstance();
    final predictions = prefs.getStringList('predictions') ?? [];
    
    predictions.add(json.encode({
      'features': features,
      'result': result,
      'timestamp': DateTime.now().millisecondsSinceEpoch,
    }));
    
    await prefs.setStringList('predictions', predictions);
  }
}
```

## App Store Deployment

### Google Play Store
1. Create developer account
2. Build release APK: `flutter build apk --release`
3. Upload to Google Play Console
4. Fill out store listing
5. Submit for review

### Apple App Store
1. Create Apple Developer account
2. Build iOS app: `flutter build ios --release`
3. Upload to App Store Connect
4. Fill out app information
5. Submit for review

## Push Notifications

### React Native
```javascript
// Install: npm install react-native-push-notification
import PushNotification from 'react-native-push-notification';

PushNotification.configure({
  onNotification: function(notification) {
    console.log('NOTIFICATION:', notification);
  },
});
```

### Flutter
```dart
// Add to pubspec.yaml: firebase_messaging: ^14.6.5
import 'package:firebase_messaging/firebase_messaging.dart';

class NotificationService {
  static Future<void> initialize() async {
    FirebaseMessaging messaging = FirebaseMessaging.instance;
    
    NotificationSettings settings = await messaging.requestPermission(
      alert: true,
      badge: true,
      sound: true,
    );
  }
}
```

## Analytics Integration

### React Native
```javascript
// Install: npm install @react-native-firebase/analytics
import analytics from '@react-native-firebase/analytics';

analytics().logEvent('mushroom_prediction', {
  edible: result.edible,
  confidence: result.confidence
});
```

### Flutter
```dart
// Add to pubspec.yaml: firebase_analytics: ^10.4.0
import 'package:firebase_analytics/firebase_analytics.dart';

FirebaseAnalytics.instance.logEvent(
  name: 'mushroom_prediction',
  parameters: {
    'edible': result['edible'],
    'confidence': result['confidence'],
  },
);
```
    '''
    
    guide_file = Path("MOBILE_INTEGRATION.md")
    with open(guide_file, 'w') as f:
        f.write(guide)
    
    print(f"📖 Mobile integration guide created: {guide_file}")

def main():
    """Create mobile app components."""
    print("📱 CREATING MOBILE APPLICATIONS")
    print("=" * 50)
    
    # Create mobile apps
    create_react_native_app()
    create_flutter_app()
    create_pubspec()
    create_package_json()
    create_deployment_scripts()
    create_api_integration_guide()
    
    print("\n🎉 Mobile Applications Created!")
    print("=" * 40)
    print("📁 Files created:")
    print("   - mobile_app/MushroomIdentifier.js (React Native)")
    print("   - mobile_app/lib/main.dart (Flutter)")
    print("   - mobile_app/package.json (React Native deps)")
    print("   - mobile_app/pubspec.yaml (Flutter deps)")
    print("   - deploy_mobile.sh (Deployment script)")
    print("   - MOBILE_INTEGRATION.md (Integration guide)")
    
    print("\n🚀 Next steps:")
    print("1. Set up development environment")
    print("2. Install dependencies")
    print("3. Test on devices")
    print("4. Deploy to app stores")
    print("5. Add analytics and notifications")

if __name__ == "__main__":
    main()
