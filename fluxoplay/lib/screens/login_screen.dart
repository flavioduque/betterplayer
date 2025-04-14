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

    final ok = await AuthService.validate(userController.text, passController.text);
    if (ok) {
      final prefs = await SharedPreferences.getInstance();
      prefs.setString("username", userController.text);
      prefs.setString("password", passController.text);

      if (!mounted) return;
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const HomeScreen()));
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
                decoration: const InputDecoration(labelText: "Usuário", filled: true),
              ),
              const SizedBox(height: 10),
              TextField(
                controller: passController,
                obscureText: true,
                decoration: const InputDecoration(labelText: "Senha", filled: true),
              ),
              const SizedBox(height: 20),
              if (error.isNotEmpty)
                Text(error, style: const TextStyle(color: Colors.red)),
              if (loading)
                const CircularProgressIndicator()
              else
                ElevatedButton(onPressed: login, child: const Text("Entrar")),
            ],
          ),
        ),
      ),
    );
  }
}
