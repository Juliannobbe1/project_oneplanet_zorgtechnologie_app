import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:zorgtechnologieapp/providers/logging_provider/logging_provider.dart';

import '../handlers/auth_handler.dart';
import 'home_page.dart';

class LoginPage extends ConsumerStatefulWidget {
  const LoginPage({super.key});

  @override
  LoginPageState createState() => LoginPageState();
}

class LoginPageState extends ConsumerState<LoginPage> {
  final GlobalKey<FormState> _formkey = GlobalKey<FormState>();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _wachtwoordController = TextEditingController();

  bool obscure = true, checkValue = false, valid = false;
  String email = "";
  String password = "";
  String? _error;

  @override
  Widget build(BuildContext context) {
    final logger = ref.watch(loggingProvider);

    final email = TextFormField(
      keyboardType: TextInputType.emailAddress,
      controller: _emailController,
      validator: (value) {
        if (value == null || value.isEmpty) {
          return 'enter email!';
        }
        return null;
      },
      decoration: InputDecoration(
        labelText: 'Email',
        prefixIcon: const Icon(Icons.email),
        hintText: 'Email',
        contentPadding: const EdgeInsets.fromLTRB(20.0, 10.0, 20.0, 10.0),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(32.0)),
      ),
    );

    final password = TextFormField(
      controller: _wachtwoordController,
      validator: (value) {
        if (value == null || value.isEmpty) {
          return 'enter wachtwoord!';
        }
        return null;
      },
      obscureText: obscure,
      decoration: InputDecoration(
        contentPadding: const EdgeInsets.fromLTRB(20.0, 10.0, 20.0, 10.0),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(32.0)),
        labelText: 'Wachtwoord',
        prefixIcon: const Icon(Icons.email),
        suffixIcon: IconButton(
          icon: Icon(
            obscure ? Icons.visibility : Icons.visibility_off,
          ),
          onPressed: () {
            setState(() {
              obscure = !obscure;
            });
          },
        ),
      ),
    );

    return SafeArea(
      child: Scaffold(
        resizeToAvoidBottomInset: false,
        backgroundColor: Colors.blue,
        body: Padding(
          padding: const EdgeInsets.all(40.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              Image.asset(
                'assets/logo.png',
                width: 225.0,
                height: 175.0,
                fit: BoxFit.contain,
              ),
              SingleChildScrollView(
                child: Card(
                  color: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(24.0),
                  ),
                  elevation: 10.0,
                  child: Padding(
                    padding: const EdgeInsets.all(15.0),
                    child: Column(
                      children: [
                        const Text(
                          'Login',
                          style: TextStyle(
                            fontSize: 24.0,
                            fontWeight: FontWeight.bold,
                            color: Colors.black,
                          ),
                        ),
                        const SizedBox(height: 20.0),
                        Form(
                          key: _formkey,
                          child: Column(children: <Widget>[
                            email,
                            const SizedBox(height: 20.0),
                            password,
                            const SizedBox(height: 20.0),
                          ]),
                        ),
                        ElevatedButton(
                          onPressed: () async {
                            if (_formkey.currentState!.validate()) {
                              try {
                                await authService.login(
                                    logger,
                                    _emailController.text,
                                    _wachtwoordController.text);
                                if (mounted) {
                                  // Only navigate to HomePage if login was successful
                                  Navigator.push(
                                    context, // Use the stored context
                                    MaterialPageRoute(
                                      builder: (context) => const HomePage(),
                                    ),
                                  );
                                }
                              } on FirebaseAuthException catch (e) {
                                if (e.code == "INVALID_LOGIN_CREDENTIALS") {
                                  setState(() {
                                    _error = 'Email of wachtwoord is incorrect';
                                  });
                                } else {
                                  setState(() {
                                    _error = e.code;
                                  });
                                }
                              }
                            }
                          },
                          style: ButtonStyle(
                            minimumSize: MaterialStateProperty.all(
                                const Size(150.0, 50.0)),
                            backgroundColor:
                                MaterialStateProperty.all<Color>(Colors.blue),
                            elevation: MaterialStateProperty.all<double>(4.0),
                          ),
                          child: const Text(
                            'Login',
                            style: TextStyle(color: Colors.white),
                          ),
                        ), // Display the error message, if any
                        if (_error != null)
                          Text(
                            _error!,
                            style: const TextStyle(color: Colors.red),
                          ),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _emailController.dispose();
    _wachtwoordController.dispose();
    super.dispose();
  }

  final AuthService authService =
      AuthService(firebaseAuth: FirebaseAuth.instance);
}
