import 'package:flutter/material.dart';

class AboutPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onLongPress: () => Navigator.of(context).pop(), // 长按返回
      child: Container(
        child: Center(
          child: Column(
            children: [
              Padding(padding: const EdgeInsets.all(40)),
              Text("楚天乐",
                  style: TextStyle(fontSize: 16, color: Colors.grey[800])),
              Padding(padding: const EdgeInsets.all(40)),
            ],
          ),
        ),
      ),
    );
  }
}
