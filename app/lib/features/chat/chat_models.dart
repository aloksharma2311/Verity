// lib/features/chat/chat_models.dart
import 'package:equatable/equatable.dart';

class ChatVerificationResult extends Equatable {
  final String verdict;
  final double? score;
  final String? explanation;

  const ChatVerificationResult({
    required this.verdict,
    this.score,
    this.explanation,
  });

  factory ChatVerificationResult.fromJson(Map<String, dynamic> json) {
    return ChatVerificationResult(
      verdict: json['verdict'] as String? ?? 'unknown',
      score: (json['score'] as num?)?.toDouble(),
      explanation: json['explanation'] as String?,
    );
  }

  @override
  List<Object?> get props => [verdict, score, explanation];
}

class ChatMessage extends Equatable {
  final String id;
  final String text;
  final bool isUser;
  final DateTime createdAt;
  final ChatVerificationResult? verification;

  const ChatMessage({
    required this.id,
    required this.text,
    required this.isUser,
    required this.createdAt,
    this.verification,
  });

  @override
  List<Object?> get props => [id, text, isUser, createdAt, verification];
}

class ChatState extends Equatable {
  final List<ChatMessage> messages;
  final bool isLoading;
  final String? error;

  const ChatState({
    this.messages = const [],
    this.isLoading = false,
    this.error,
  });

  ChatState copyWith({
    List<ChatMessage>? messages,
    bool? isLoading,
    String? error,
  }) {
    return ChatState(
      messages: messages ?? this.messages,
      isLoading: isLoading ?? this.isLoading,
      error: error,
    );
  }

  @override
  List<Object?> get props => [messages, isLoading, error];
}
