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
