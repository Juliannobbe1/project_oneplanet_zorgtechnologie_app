import 'package:logger/logger.dart';
import 'package:test/test.dart';
import 'package:mockito/mockito.dart';
@GenerateNiceMocks([MockSpec<UserCredential>()])
@GenerateNiceMocks([MockSpec<User>()])
import 'package:firebase_auth/firebase_auth.dart';
import 'package:mockito/annotations.dart';
@GenerateNiceMocks([MockSpec<AuthService>()])
import 'package:zorgtechnologieapp/handlers/auth_handler.dart'; // Replace with the actual path to your AuthService file

import 'login_test.mocks.dart';

class MockLogger extends Mock implements Logger {}

// Create a mock for FirebaseAuth
class MockFirebaseAuth extends Mock implements FirebaseAuth {
  @override
  Future<UserCredential> signInWithEmailAndPassword({
    required String? email,
    required String? password,
  }) =>
      super.noSuchMethod(
          Invocation.method(#signInWithEmailAndPassword, [email, password]),
          returnValue: Future.value(MockUserCredential()));
}

void main() {
  group('AuthService Tests', () {
    late AuthService authService;
    late MockFirebaseAuth mockFirebaseAuth;
    late MockLogger mockLogger;
    setUp(() {
      mockLogger = MockLogger();
      mockFirebaseAuth = MockFirebaseAuth();
      authService = AuthService(firebaseAuth: mockFirebaseAuth);
    });

    test('Login success', () async {
      // Arrange
      const email = 'test@example.com';
      const password = 'password';
      final userCredential = MockUserCredential();
      final MockUser mockUser = MockUser();

      when(userCredential.user).thenReturn(mockUser);
      when(mockUser.uid).thenReturn("test_uid");

      when(mockFirebaseAuth.signInWithEmailAndPassword(
        email: email,
        password: password,
      )).thenAnswer((_) => Future.value(userCredential));

      // Act
      await authService.login(mockLogger, email, password);

      // Assert
      verify(mockFirebaseAuth.signInWithEmailAndPassword(
        email: email,
        password: password,
      )).called(1);
    });

    test('Login failure', () async {
      // Arrange
      const email = 'test@example.com';
      const password = 'password';

      when(mockFirebaseAuth.signInWithEmailAndPassword(
        email: email,
        password: password,
      )).thenThrow(
          FirebaseAuthException(code: 'code', message: 'error message'));

      // Act and Assert
      expect(() => authService.login(mockLogger, email, password),
          throwsException);
    });
  });
}

// // Mock class for UserCredential
// class MockUserCredential extends Mock implements UserCredential {}

// class MockUser extends Mock implements User {}
