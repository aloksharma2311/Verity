import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../../core/api_client.dart';

class AuthRepository {
  final ApiClient _api = ApiClient();
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  Future<void> signup({
    required String email,
    required String password,
    required String name,
  }) async {
    await _api.postJson('/auth/signup', data: {
      'email': email,
      'password': password,
      'name': name,
    });
  }

  Future<void> login({
    required String email,
    required String password,
  }) async {
    final res = await _api.postForm('/auth/login', data: {
      'username': email,
      'password': password,
    });

    final data = res.data as Map;
    final token = data['access_token'] as String;
    await _storage.write(key: 'access_token', value: token);
  }

  Future<void> logout() async {
    await _storage.delete(key: 'access_token');
  }

  Future<bool> isLoggedIn() async {
    final token = await _storage.read(key: 'access_token');
    return token != null;
  }
}
