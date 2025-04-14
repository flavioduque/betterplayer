import os

# Gerar o conteúdo do script criar_fluxoplay.sh
script_content = """#!/bin/bash

# Nome do projeto
APP_NAME="fluxoplay"

# Criar projeto Flutter
flutter create $APP_NAME
cd $APP_NAME || exit 1

# Criar estrutura de pastas
mkdir -p lib/core lib/screens assets/video

# Baixar splash genérico
curl -L -o assets/video/intro.mp4 
https://filesamples.com/samples/video/mp4/sample_640x360.mp4

# Ativar assets no pubspec.yaml
awk '/^ *assets: *$/ {
  print;
  print "    - assets/video/intro.mp4";
  next
} 1' pubspec.yaml > pubspec_temp.yaml && mv pubspec_temp.yaml pubspec.yaml

# Adicionar dependências
cat >> pubspec.yaml <<EOL

dependencies:
  http: ^0.13.5
  shared_preferences: ^2.0.15
  video_player: ^2.5.1

EOL

# Substituir main.dart
cat > lib/main.dart << 'EOF'
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'screens/splash_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.landscapeLeft,
    DeviceOrientation.landscapeRight,
  ]).then((_) {
    runApp(const MyApp());
  });
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'FluxoPlay',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(),
      home: const SplashScreen(),
    );
  }
}
EOF

# Substituir arquivos lib/screens e lib/core
mkdir -p lib/screens lib/core

cat > lib/screens/splash_screen.dart << 'EOF'
import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';
import 'login_screen.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  late VideoPlayerController _controller;

  @override
  void initState() {
    super.initState();
    _controller = VideoPlayerController.asset("assets/video/intro.mp4")
      ..initialize().then((_) {
        setState(() {});
        _controller.play();
      });

    Future.delayed(const Duration(seconds: 4), () {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const LoginScreen()),
      );
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: _controller.value.isInitialized
          ? Center(child: AspectRatio(aspectRatio: 
_controller.value.aspectRatio, child: VideoPlayer(_controller)))
          : const Center(child: CircularProgressIndicator()),
    );
  }
}
EOF

cat > lib/screens/login_screen.dart << 'EOF'
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../core/services.dart';
import 'home_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController userController = TextEditingController();
  final TextEditingController passController = TextEditingController();
  bool loading = false;
  String error = "";

  void login() async {
    setState(() {
      loading = true;
      error = "";
    });

    final ok = await AuthService.validate(userController.text, 
passController.text);
    if (ok) {
      final prefs = await SharedPreferences.getInstance();
      prefs.setString("username", userController.text);
      prefs.setString("password", passController.text);

      if (!mounted) return;
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => 
const HomeScreen()));
    } else {
      setState(() {
        error = "Credenciais inválidas!";
        loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Center(
        child: SizedBox(
          width: 500,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text("FluxoPlay", style: TextStyle(fontSize: 36)),
              const SizedBox(height: 30),
              TextField(
                controller: userController,
                decoration: const InputDecoration(labelText: "Usuário", 
filled: true),
              ),
              const SizedBox(height: 10),
              TextField(
                controller: passController,
                obscureText: true,
                decoration: const InputDecoration(labelText: "Senha", 
filled: true),
              ),
              const SizedBox(height: 20),
              if (error.isNotEmpty)
                Text(error, style: const TextStyle(color: Colors.red)),
              if (loading)
                const CircularProgressIndicator()
              else
                ElevatedButton(onPressed: login, child: const 
Text("Entrar")),
            ],
          ),
        ),
      ),
    );
  }
}
EOF

cat > lib/screens/home_screen.dart << 'EOF'
import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(child: Text("Bem-vindo ao FluxoPlay")),
    );
  }
}
EOF

cat > lib/core/services.dart << 'EOF'
import 'dart:convert';
import 'package:http/http.dart' as http;

class AuthService {
  static Future<bool> validate(String user, String pass) async {
    final response = await http.get(
      
Uri.parse("http://138.59.227.10/player_api.php?username=$user&password=$pass"),
    );
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data["user_info"] != null && data["user_info"]["auth"] == 1;
    }
    return false;
  }
}
EOF

echo "✅ Projeto FluxoPlay criado com sucesso!"
"""

# Salvar o script
script_path = "/mnt/data/criar_fluxoplay.sh"
with open(script_path, "w") as f:
    f.write(script_content)

# Tornar executável
os.chmod(script_path, 0o755)

script_path

