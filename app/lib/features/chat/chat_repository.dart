// lib/features/chat/chat_repository.dart
import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import 'chat_models.dart';

class ChatRepository {
  final Dio _dio;
  final FlutterSecureStorage _storage;

  ChatRepository(this._dio, this._storage);

  Future<ChatVerificationResult> verifyText(String text) async {
    final token = await _storage.read(key: 'access_token');

    final response = await _dio.post(
      '/chat/verify',
      data: {'text': text},
      options: Options(
        headers: {
          if (token != null) 'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      ),
    );

    return ChatVerificationResult.fromJson(
      response.data as Map<String, dynamic>,
    );
  }
}
