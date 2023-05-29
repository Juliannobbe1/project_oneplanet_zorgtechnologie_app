import 'package:flutter/material.dart';

import '../handlers/responsive_layout_handler.dart';

class SelectionGuidePage extends StatelessWidget {
  const SelectionGuidePage({super.key});

  @override
  Widget build(BuildContext context) {
    final deviceType = ResponsiveLayout.getDeviceType(context);
    double screenWidth = MediaQuery.of(context).size.width;

    return SafeArea(
      child: Scaffold(
        backgroundColor: Colors.indigo[50],
        appBar: AppBar(
          backgroundColor: Theme.of(context).colorScheme.inversePrimary,
          // leading: const Icon(Icons.menu),
          title: Text(
            "$deviceType",
          ),
        ),
        body: Column(
          children: [
            if (deviceType == DeviceType.tablet ||
                deviceType == DeviceType.desktop) ...[
              TabletSelectionScreen(
                screenWidth: screenWidth,
              )
            ] else ...[
              PhoneSelectionScreen(screenWidth: screenWidth)
            ]
          ],
        ),
      ),
    );
  }
}

class TabletSelectionScreen extends StatelessWidget {
  final double screenWidth;
  const TabletSelectionScreen({super.key, required this.screenWidth});

  @override
  Widget build(BuildContext context) {
    return Container();
  }
}

class PhoneSelectionScreen extends StatelessWidget {
  final double screenWidth;
  const PhoneSelectionScreen({super.key, required this.screenWidth});

  @override
  Widget build(BuildContext context) {
    return const Text("keuzegids");
  }
}
