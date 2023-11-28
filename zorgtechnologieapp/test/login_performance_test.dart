import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:logger/logger.dart';
import 'package:mockito/mockito.dart';
@GenerateNiceMocks([MockSpec<UserCredential>()])
@GenerateNiceMocks([MockSpec<User>()])
import 'package:firebase_auth/firebase_auth.dart';
import 'package:mockito/annotations.dart';
@GenerateNiceMocks([MockSpec<AuthService>()])
import 'package:zorgtechnologieapp/handlers/auth_handler.dart';

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

    testWidgets('Login success', (WidgetTester tester) async {
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
      final Stopwatch stopwatch = Stopwatch()..start();
      await tester.pumpWidget(
        // Your widget tree here, or a simple MaterialApp if needed
        MaterialApp(
          home: Material(
            child: Builder(
              builder: (BuildContext context) {
                authService.login(mockLogger, email, password);
                return Container();
              },
            ),
          ),
        ),
      );
      stopwatch.stop();

      // Assert
      verify(mockFirebaseAuth.signInWithEmailAndPassword(
        email: email,
        password: password,
      )).called(1);

      // Assert that the response time is less than 10 seconds
      expect(stopwatch.elapsedMilliseconds, lessThan(10000));
    });
  });
}
