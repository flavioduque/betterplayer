import 'dart:io';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'package:flutter/services.dart';
import 'package:better_player/better_player.dart';
import 'login_screen.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  BetterPlayerController? _controller;

  @override
  void initState() {
    super.initState();
    _loadAndPlayVideo();
  }

  Future<void> _loadAndPlayVideo() async {
    final byteData = await rootBundle.load('assets/video/intro.mp4');
    final tempDir = await getTemporaryDirectory();
    final file = File('${tempDir.path}/intro.mp4');
    await file.writeAsBytes(byteData.buffer.asUint8List());

    final dataSource = BetterPlayerDataSource(
      BetterPlayerDataSourceType.file,
      file.path,
    );

    _controller = BetterPlayerController(
      BetterPlayerConfiguration(
        autoPlay: true,
        looping: false,
        fit: BoxFit.cover,
        controlsConfiguration: const BetterPlayerControlsConfiguration(
          showControls: false,
        ),
        eventListener: (event) {
          if (event.betterPlayerEventType == BetterPlayerEventType.finished) {
            _goToLogin();
          }
        },
      ),
      betterPlayerDataSource: dataSource,
    );

    // Garantia de fallback
    Future.delayed(const Duration(seconds: 10), () {
      if (mounted) _goToLogin();
    });

    setState(() {});
  }

  void _goToLogin() {
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (_) => const LoginScreen()),
    );
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: _controller != null
          ? BetterPlayer(controller: _controller!)
          : const Center(child: CircularProgressIndicator()),
    );
  }
}
