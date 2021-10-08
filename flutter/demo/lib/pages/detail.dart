import 'package:flutter/material.dart';
import 'package:demo/store/appstate.dart';
import 'package:demo/model/cat.dart';

class DetailPage extends StatelessWidget {
  DetailPage({
    Key? key,
    @required this.name, // 接收一个text参数
  }) : super(key: key);

  final String? name;

  @override
  Widget build(BuildContext context) {
    Cat cat = AppState.catStore.getCatByName(this.name ?? "");

    return Container(
      child: Center(
        child: Column(
          children: [
            Text("详细", style: TextStyle(fontSize: 16, color: Colors.grey[800])),
            Image.asset(cat.image),
            Padding(
              padding: const EdgeInsets.only(left: 10.0),
            ),
            Text(cat.name,
                style: TextStyle(fontSize: 16, color: Colors.grey[800])),
            Text(cat.description,
                style: TextStyle(fontSize: 16, color: Colors.grey[800])),
          ],
        ),
      ),
    );
  }
}
