import 'package:flutter/material.dart';

class ResponsiveLayout {
  final Widget Function(BuildContext) desktopBuilder;
  final Widget Function(BuildContext) tabletBuilder;
  final Widget Function(BuildContext) phoneBuilder;

  const ResponsiveLayout({
    required this.desktopBuilder,
    required this.tabletBuilder,
    required this.phoneBuilder,
  });

  static const double phoneWidthBreakpoint = 600.0;
  static const double tabletWidthBreakpoint = 1200.0;
  static const double phoneHeightBreakpoint = 600.0;
  static const double tabletHeightBreakpoint = 900.0;

  static DeviceType getDeviceType(BuildContext context) {
    final double screenWidth = MediaQuery.of(context).size.width;
    final double screenHeight = MediaQuery.of(context).size.height;

    if (screenWidth >= tabletWidthBreakpoint &&
        screenHeight >= tabletHeightBreakpoint) {
      return DeviceType.desktop;
    } else if (screenWidth >= phoneWidthBreakpoint &&
        screenHeight >= phoneHeightBreakpoint) {
      return DeviceType.tablet;
    } else {
      return DeviceType.phone;
    }
  }
}

enum DeviceType {
  desktop,
  tablet,
  phone,
}

class SizeScaler {
  static double getScalingFactor(BuildContext context) {
    final double screenWidth = MediaQuery.of(context).size.width;
    final double screenHeight = MediaQuery.of(context).size.height;

    if (screenWidth >= ResponsiveLayout.tabletWidthBreakpoint &&
        screenHeight >= ResponsiveLayout.tabletHeightBreakpoint) {
      return 1.5;
    } else if (screenWidth >= ResponsiveLayout.phoneWidthBreakpoint &&
        screenHeight >= ResponsiveLayout.phoneHeightBreakpoint) {
      return 1.2;
    } else {
      return 0.8;
    }
  }

  static TextStyle getResponsiveTextStyle(BuildContext context, double baseSize,
      FontWeight fontweight, Color color) {
    final double scalingFactor = getScalingFactor(context);
    final double adjustedFontSize = baseSize * scalingFactor;

    return TextStyle(
        fontSize: adjustedFontSize, fontWeight: fontweight, color: color);
  }

  static double getResponsiveSize(BuildContext context, double baseSize) {
    final double scalingFactor = getScalingFactor(context);
    final double adjustedSize = baseSize * scalingFactor;

    return adjustedSize;
  }
}
