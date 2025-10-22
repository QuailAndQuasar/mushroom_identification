
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
    