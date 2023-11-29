import 'package:firebase_auth/firebase_auth.dart';
import 'package:logger/logger.dart';

class AuthService {
  final FirebaseAuth firebaseAuth;

  AuthService({required this.firebaseAuth});

  Future<void> login(Logger logger, String email, String password) async {
    try {
      UserCredential userCredential =
          await firebaseAuth.signInWithEmailAndPassword(
        email: email,
        password: password,
      );

      logger.i('User ${userCredential.user!.uid} logged in');
    } catch (e) {
      logger.e("An error occurred while logging in user: $e");
      rethrow;
    }
  }
}
