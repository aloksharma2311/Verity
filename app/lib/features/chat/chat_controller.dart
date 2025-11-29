// lib/features/chat/chat_controller.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:uuid/uuid.dart';
import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import 'chat_models.dart';
import 'chat_repository.dart';

final _uuid = Uuid();

final chatRepositoryProvider = Provider<ChatRepository>((ref) {
  final dio = Dio(
    BaseOptions(
      // IMPORTANT: 10.0.2.2 is "localhost" from Android emulator
      baseUrl: 'http://10.0.2.2:8000',
      connectTimeout: const Duration(seconds: 5),
      receiveTimeout: const Duration(seconds: 15),
    ),
  );
  final storage = const FlutterSecureStorage();
  return ChatRepository(dio, storage);
});

final chatControllerProvider =
    StateNotifierProvider<ChatController, ChatState>((ref) {
  final repo = ref.watch(chatRepositoryProvider);
  return ChatController(repo);
});

class ChatController extends StateNotifier<ChatState> {
  final ChatRepository _repo;

  ChatController(this._repo) : super(const ChatState());

  Future<void> sendMessage(String text) async {
    final trimmed = text.trim();
    if (trimmed.isEmpty) return;

    final userMessage = ChatMessage(
      id: _uuid.v4(),
      text: trimmed,
      isUser: true,
      createdAt: DateTime.now(),
    );

    // optimistic add
    state = state.copyWith(
      messages: [...state.messages, userMessage],
      isLoading: true,
      error: null,
    );

    try {
      final result = await _repo.verifyText(trimmed);

      final botMessage = ChatMessage(
        id: _uuid.v4(),
        text: result.explanation ??
            'Verdict: ${result.verdict}\nScore: ${result.score?.toStringAsFixed(0) ?? '-'} / 100',
        isUser: false,
        createdAt: DateTime.now(),
        verification: result,
      );

      state = state.copyWith(
        messages: [...state.messages, botMessage],
        isLoading: false,
        error: null,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'Error contacting verification server',
      );
    }
  }

  void clearError() {
    if (state.error != null) {
      state = state.copyWith(error: null);
    }
  }
}
