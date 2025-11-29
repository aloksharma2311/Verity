import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class ApiClient {
  ApiClient._internal();

  static final ApiClient _instance = ApiClient._internal();
  factory ApiClient() => _instance;

  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: 'http://10.0.2.2:8000', // emulator -> backend on localhost
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 20),
    ),
  );

  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  Future<void> _attachAuthHeader() async {
    final token = await _storage.read(key: 'access_token');
    if (token != null) {
      _dio.options.headers['Authorization'] = 'Bearer $token';
    } else {
      _dio.options.headers.remove('Authorization');
    }
  }

  Future<Response<T>> get<T>(String path,
      {Map<String, dynamic>? query}) async {
    await _attachAuthHeader();
    return _dio.get<T>(path, queryParameters: query);
  }

  Future<Response<T>> postJson<T>(String path, {dynamic data}) async {
    await _attachAuthHeader();
    return _dio.post<T>(path, data: data);
  }

  Future<Response<T>> postForm<T>(String path,
      {Map<String, dynamic>? data}) async {
    await _attachAuthHeader();
    return _dio.post<T>(
      path,
      data: FormData.fromMap(data ?? {}),
      options: Options(
        contentType: Headers.formUrlEncodedContentType,
      ),
    );
  }
}
