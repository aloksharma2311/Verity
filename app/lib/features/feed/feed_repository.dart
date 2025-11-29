// lib/features/feed/feed_repository.dart
import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import 'feed_models.dart';

class FeedRepository {
  final Dio _dio;
  final FlutterSecureStorage _storage;

  FeedRepository(this._dio, this._storage);

  Future<List<FeedItem>> loadFeed() async {
    // read JWT stored by auth_controller
    final token = await _storage.read(key: 'access_token');

    final response = await _dio.get(
      '/posts', // or '/feed' – use the exact path from your FastAPI router
      options: Options(
        headers: {
          if (token != null) 'Authorization': 'Bearer $token',
        },
      ),
    );

    final data = response.data as List<dynamic>;
    return data
        .map((json) => FeedItem.fromJson(json as Map<String, dynamic>))
        .toList();
  }
}
