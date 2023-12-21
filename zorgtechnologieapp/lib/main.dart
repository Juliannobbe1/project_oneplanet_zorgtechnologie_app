import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:logger/logger.dart';
//import 'pages/home_page.dart';
import 'pages/login_page.dart';
import 'firebase_options.dart';
import 'package:freerasp/freerasp.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // Signing hash of your app
  String base64Hash = hashConverter.fromSha256toBase64(
      "1D:45:6E:E0:8C:FA:04:69:1F:E0:7A:3C:1E:63:24:BA:CE:62:05:95:07:56:1C:8F:8D:A9:35:2F:61:6F:D2:D8");
  // create configuration for freeRASP
  final config = TalsecConfig(
    /// For Android
    androidConfig: AndroidConfig(
      packageName: 'com.example.zorgtechnologieapp',
      signingCertHashes: [base64Hash],
      supportedStores: ['com.sec.android.app.samsungapps'],
    ),
    watcherMail: 'smartcareassist@outlook.com',
    isProd: false,
  );

  Logger securityLogger = Logger();

  // Setting up callbacks
  final callback = ThreatCallback(
      onAppIntegrity: () => securityLogger.w(
          "Warning App integrity: Potential integrity violation detected in the application"),
      onObfuscationIssues: () => securityLogger.w(
          "Warning Obfuscation issues: Issues detected with the obfuscation techniques used in the application"),
      onDebug: () => securityLogger.w(
          "Warning Debugging: Application is running in debug mode, which poses a security risk"),
      onDeviceBinding: () => securityLogger.w(
          "Warning Device binding: Issues detected with the binding of the application to the device"),
      onDeviceID: () => securityLogger
          .w("Warning Device ID: Potential issues detected with the device ID"),
      onHooks: () => securityLogger.w(
          "Warning Hooks: Potential malicious hooks detected in the application"),
      onPrivilegedAccess: () => securityLogger.w(
          "Warning Privileged access: Unauthorized privileged access detected"),
      onSecureHardwareNotAvailable: () => securityLogger.w(
          "Warning Secure hardware not available: Required secure hardware features are not available on this device."),
      onSimulator: () => securityLogger.w(
          "Warning Simulator: Application is running on a simulator, which poses a security risk"),
      onUnofficialStore: () => securityLogger.w(
          "Warning Unofficial store: Application was downloaded from an unofficial store, posing potential security risks"));

  // Attaching listener
  Talsec.instance.attachListener(callback);

  /// freeRASP should be always initialized in the top-level widget
  await Talsec.instance.start(config);

  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(const App());
}

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return const ProviderScope(
      child: MyApp(),
    );
  }
}

class PreferredOrientationWrapper extends StatelessWidget {
  final Widget child;

  const PreferredOrientationWrapper({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    final double screenWidth = MediaQuery.of(context).size.width;
    if (screenWidth > 600) {
      SystemChrome.setPreferredOrientations([
        DeviceOrientation.portraitUp,
        DeviceOrientation.portraitDown,
        DeviceOrientation.landscapeLeft,
        DeviceOrientation.landscapeRight,
      ]);
    } else {
      SystemChrome.setPreferredOrientations([
        DeviceOrientation.portraitUp,
        DeviceOrientation.portraitDown,
      ]);
    }
    return child;
  }
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return PreferredOrientationWrapper(
      child: MaterialApp(
        title: 'Flutter Demo',
        theme: ThemeData(
          primarySwatch: Colors.blue,
        ),
        // home: const HomePage(),
        home: const LoginPage(),
        debugShowCheckedModeBanner: false,
      ),
    );
  }
}
