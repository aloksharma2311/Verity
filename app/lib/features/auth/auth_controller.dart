import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'auth_repository.dart';

enum AuthStatus { unknown, authenticated, unauthenticated, loading }

class AuthState {
  final AuthStatus status;
  final String? error;

  const AuthState({required this.status, this.error});

  AuthState copyWith({AuthStatus? status, String? error}) {
    return AuthState(
      status: status ?? this.status,
      error: error,
    );
  }
}

final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return AuthRepository();
});

final authControllerProvider =
    StateNotifierProvider<AuthController, AuthState>((ref) {
  final repo = ref.read(authRepositoryProvider);
  return AuthController(repo)..init();
});

class AuthController extends StateNotifier<AuthState> {
  final AuthRepository _repo;

  AuthController(this._repo)
      : super(const AuthState(status: AuthStatus.unknown));

  Future<void> init() async {
    final loggedIn = await _repo.isLoggedIn();
    state = AuthState(
      status: loggedIn ? AuthStatus.authenticated : AuthStatus.unauthenticated,
    );
  }

  Future<void> login(String email, String password) async {
    state = const AuthState(status: AuthStatus.loading);
    try {
      await _repo.login(email: email, password: password);
      state = const AuthState(status: AuthStatus.authenticated);
    } catch (e) {
      state =
          AuthState(status: AuthStatus.unauthenticated, error: e.toString());
    }
  }

  Future<void> signup(String email, String password, String name) async {
    state = const AuthState(status: AuthStatus.loading);
    try {
      await _repo.signup(email: email, password: password, name: name);
      await _repo.login(email: email, password: password);
      state = const AuthState(status: AuthStatus.authenticated);
    } catch (e) {
      state =
          AuthState(status: AuthStatus.unauthenticated, error: e.toString());
    }
  }

  Future<void> logout() async {
    await _repo.logout();
    state = const AuthState(status: AuthStatus.unauthenticated);
  }
}
