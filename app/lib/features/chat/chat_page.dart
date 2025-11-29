import 'package:flutter/cupertino.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter/material.dart' show Divider;


import 'chat_controller.dart';
import 'chat_models.dart';

class ChatPage extends ConsumerStatefulWidget {
  const ChatPage({super.key});

  @override
  ConsumerState<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends ConsumerState<ChatPage> {
  final TextEditingController _textController = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  @override
  void dispose() {
    _textController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  void _send() {
    final text = _textController.text.trim();
    if (text.isEmpty) return;

    ref.read(chatControllerProvider.notifier).sendMessage(text);
    _textController.clear();

    Future.delayed(const Duration(milliseconds: 100), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 250),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(chatControllerProvider);

    return CupertinoPageScaffold(
      navigationBar: const CupertinoNavigationBar(
        middle: Text('Verity Fact-Check Chat'),
      ),
      child: SafeArea(
        child: Column(
          children: [
            // ERROR BANNER
            if (state.error != null)
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                color: CupertinoColors.systemRed.withOpacity(0.1),
                child: Row(
                  children: [
                    const Icon(
                      CupertinoIcons.exclamationmark_triangle,
                      size: 18,
                      color: CupertinoColors.systemRed,
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        state.error!,
                        style: const TextStyle(fontSize: 13),
                      ),
                    ),
                    CupertinoButton(
                      padding: EdgeInsets.zero,
                      child: const Icon(
                        CupertinoIcons.xmark_circle_fill,
                        size: 18,
                      ),
                      onPressed: () =>
                          ref.read(chatControllerProvider.notifier).clearError(),
                    ),
                  ],
                ),
              ),

            // MESSAGES
            Expanded(
              child: ListView.builder(
                controller: _scrollController,
                padding: const EdgeInsets.all(12),
                itemCount: state.messages.length,
                itemBuilder: (context, index) {
                  final ChatMessage msg = state.messages[index];
                  final bool isUser = msg.isUser;

                  return Align(
                    alignment:
                        isUser ? Alignment.centerRight : Alignment.centerLeft,
                    child: Container(
                      margin: const EdgeInsets.symmetric(vertical: 4),
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: isUser
                            ? CupertinoColors.activeBlue
                            : CupertinoColors.systemGrey5,
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Column(
                        crossAxisAlignment: isUser
                            ? CrossAxisAlignment.end
                            : CrossAxisAlignment.start,
                        children: [
                          Text(
                            msg.text,
                            style: TextStyle(
                              color: isUser
                                  ? CupertinoColors.white
                                  : CupertinoColors.label,
                              fontSize: 14,
                            ),
                          ),

                          // VERIFICATION INFO
                          if (!isUser && msg.verification != null) ...[
                            const SizedBox(height: 6),
                            Text(
                              'Verdict: ${msg.verification!.verdict}'
                              '${msg.verification!.score != null ? ' • Score: ${msg.verification!.score!.toStringAsFixed(0)}/100' : ''}',
                              style: TextStyle(
                                fontSize: 11,
                                color: isUser
                                    ? CupertinoColors.white
                                    : CupertinoColors.systemGrey,
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
            Divider(height: 1, thickness: 0.2),

            // INPUT BAR
            Padding(
              padding:
                  const EdgeInsets.symmetric(horizontal: 8.0, vertical: 6.0),
              child: Row(
                children: [
                  Expanded(
                    child: CupertinoTextField(
                      controller: _textController,
                      placeholder: 'Paste a claim or text to verify…',
                      onSubmitted: (_) => _send(),
                    ),
                  ),
                  const SizedBox(width: 8),
                  CupertinoButton.filled(
                    padding: const EdgeInsets.symmetric(horizontal: 14),
                    onPressed: state.isLoading ? null : _send,
                    child: state.isLoading
                        ? const CupertinoActivityIndicator()
                        : const Icon(CupertinoIcons.paperplane_fill, size: 18),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
