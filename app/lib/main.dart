import 'package:flutter/cupertino.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'features/auth/auth_controller.dart';
import 'features/auth/login_page.dart';
import 'features/feed/feed_page.dart';
import 'features/upload/upload_page.dart';
import 'features/chat/chat_page.dart';

void main() {
  runApp(const ProviderScope(child: VerityApp()));
}

class VerityApp extends ConsumerWidget {
  const VerityApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authControllerProvider);

    Widget home;
    switch (authState.status) {
      case AuthStatus.unknown:
      case AuthStatus.loading:
        home = const CupertinoPageScaffold(
          child: Center(child: CupertinoActivityIndicator()),
        );
        break;
      case AuthStatus.unauthenticated:
        home = const LoginPage();
        break;
      case AuthStatus.authenticated:
        home = const MainTabs();
        break;
    }

    return CupertinoApp(
      debugShowCheckedModeBanner: false,
      title: 'Verity',
      home: home,
    );
  }
}

class MainTabs extends StatefulWidget {
  const MainTabs({super.key});

  @override
  State<MainTabs> createState() => _MainTabsState();
}

class _MainTabsState extends State<MainTabs> {
  @override
  Widget build(BuildContext context) {
    return CupertinoTabScaffold(
      // 🔥 remove const here
      tabBar: CupertinoTabBar(
        items: const [
          BottomNavigationBarItem(
            icon: Icon(CupertinoIcons.house),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(CupertinoIcons.add_circled),
            label: 'Upload',
          ),
          BottomNavigationBarItem(
            icon: Icon(CupertinoIcons.chat_bubble_2),
            label: 'Chat',
          ),
        ],
      ),
      tabBuilder: (context, index) {
  switch (index) {
    case 0:
      return const FeedPage();
    case 1:
      return const UploadPage();
    case 2:
    default:
      return const ChatPage();
  }
},

    );
  }
}
